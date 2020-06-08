import glob
import os

import pytest
import numpy as np
import pyansys

from pyvista.plotting import system_supports_plotting
path = os.path.dirname(os.path.abspath(__file__))


rver = '194'
if os.name == 'nt':
    ans_root = 'c:/Program Files/ANSYS Inc/'
    MAPDLBIN = os.path.join(ans_root, 'v%s' % rver, 'ansys', 'bin', 'winx64',
                            'ANSYS%s.exe' % rver)
else:
    ans_root = '/usr/ansys_inc'
    MAPDLBIN = os.path.join(ans_root, 'v%s' % rver, 'ansys', 'bin',
                            'ansys%s' % rver)

if 'PYANSYS_IGNORE_ANSYS' in os.environ:
    HAS_ANSYS = False
else:
    HAS_ANSYS = os.path.isfile(MAPDLBIN)


RSETS = list(zip(range(1, 9), [1]*8))


@pytest.fixture(scope='module')
def mapdl():
    mapdl = pyansys.Mapdl(MAPDLBIN,
                          override=True,
                          additional_switches='-smp',
                          prefer_pexpect=False)

    # build the cyclic model
    mapdl.prep7()
    mapdl.shpp('off')
    mapdl.cdread('db', pyansys.examples.sector_archive_file)
    mapdl.prep7()
    mapdl.cyclic()

    # set material properties
    mapdl.mp('NUXY', 1, 0.31)
    mapdl.mp('DENS', 1, 4.1408E-04)
    mapdl.mp('EX', 1, 16900000)
    mapdl.emodif('ALL', 'MAT', 1)

    # setup and solve
    mapdl('/SOLU')
    mapdl.Antype(2, 'new')
    mapdl.Modopt('lanb', 1, 1, 100000)
    mapdl.Eqslv('SPARSE')
    mapdl.Lumpm(0)
    mapdl.Pstres(0)
    mapdl.Bcsoption('INCORE')
    mapdl.mxpand(elcalc='YES')
    mapdl.solve()
    mapdl.finish()

    # setup ansys for output without line breaks
    mapdl.post1()
    mapdl.header('OFF', 'OFF', 'OFF', 'OFF', 'OFF', 'OFF')
    nsigfig = 10
    mapdl.format('', 'E', nsigfig + 9, nsigfig)
    mapdl.page(1E9, '', -1, 240)

    return mapdl


@pytest.fixture(scope='function')
def cleared(mapdl):
    mapdl.finish()
    mapdl.clear()
    mapdl.prep7()
    yield


###############################################################################
# Testing binary reader
###############################################################################
@pytest.mark.parametrize("rset", RSETS)
@pytest.mark.skipif(not HAS_ANSYS, reason="Requires ANSYS installed")
def test_prnsol_u(mapdl, rset):
    mapdl.set(*rset)
    # verify cyclic displacements
    table = mapdl.prnsol('u').splitlines()
    if mapdl._using_corba:
        array = np.genfromtxt(table[8:])
    else:
        array = np.genfromtxt(table[9:])
    ansys_nnum = array[:, 0].astype(np.int)
    ansys_disp = array[:, 1:-1]

    nnum, disp = mapdl.result.nodal_solution(rset)

    # cyclic model will only output the master sector
    ansys_nnum = ansys_nnum[:nnum.size]
    ansys_disp = ansys_disp[:nnum.size]

    assert np.allclose(ansys_nnum, nnum)
    assert np.allclose(ansys_disp, disp)


@pytest.mark.parametrize("rset", RSETS)
@pytest.mark.skipif(not HAS_ANSYS, reason="Requires ANSYS installed")
def test_presol_s(mapdl, rset):
    mapdl.set(*rset)

    # verify element stress
    element_stress, _, enode = mapdl.result.element_stress(rset)
    element_stress = np.vstack(element_stress)
    enode = np.hstack(enode)

    # parse ansys result
    table = mapdl.presol('S').splitlines()
    ansys_element_stress = []
    line_length = len(table[15])
    for line in table:
        if len(line) == line_length:
            ansys_element_stress.append(line)

    ansys_element_stress = np.genfromtxt(ansys_element_stress)
    ansys_enode = ansys_element_stress[:, 0].astype(np.int)
    ansys_element_stress = ansys_element_stress[:, 1:]

    arr_sz = element_stress.shape[0]
    assert np.allclose(element_stress, ansys_element_stress[:arr_sz])
    assert np.allclose(enode, ansys_enode[:arr_sz])


@pytest.mark.parametrize("rset", RSETS)
@pytest.mark.skipif(not HAS_ANSYS, reason="Requires ANSYS installed")
def test_prnsol_s(mapdl, rset):
    mapdl.set(*rset)

    # verify cyclic displacements
    table = mapdl.prnsol('s').splitlines()
    if mapdl._using_corba:
        array = np.genfromtxt(table[8:])
    else:
        array = np.genfromtxt(table[10:])
    ansys_nnum = array[:, 0].astype(np.int)
    ansys_stress = array[:, 1:]

    nnum, stress = mapdl.result.nodal_stress(rset)

    # v150 includes nodes in the geometry that aren't in the result
    mask = np.in1d(nnum, ansys_nnum)
    nnum = nnum[mask]
    stress = stress[mask]

    arr_sz = nnum.shape[0]
    assert np.allclose(nnum, ansys_nnum[:arr_sz])
    assert np.allclose(stress, ansys_stress[:arr_sz])


@pytest.mark.parametrize("rset", RSETS)
@pytest.mark.skipif(not HAS_ANSYS, reason="Requires ANSYS installed")
def test_prnsol_prin(mapdl, rset):
    mapdl.set(*rset)

    # verify principal stress
    table = mapdl.prnsol('prin').splitlines()
    if mapdl._using_corba:
        array = np.genfromtxt(table[8:])
    else:
        array = np.genfromtxt(table[10:])
    ansys_nnum = array[:, 0].astype(np.int)
    ansys_stress = array[:, 1:]

    nnum, stress = mapdl.result.principal_nodal_stress(rset)

    # v150 includes nodes in the geometry that aren't in the result
    mask = np.in1d(nnum, ansys_nnum)
    nnum = nnum[mask]
    stress = stress[mask]

    arr_sz = nnum.shape[0]
    assert np.allclose(nnum, ansys_nnum[:arr_sz])
    assert np.allclose(stress, ansys_stress[:arr_sz], atol=1E-5, rtol=1E-3)


def test_read_para():
    para_path = os.path.join(path, 'testfiles', 'para')
    para_files = glob.glob(os.path.join(para_path, '*.txt'))
    from pyansys.mapdl import load_parameters
    for para_file in para_files:
        arr, parm = load_parameters(para_file)


###############################################################################
# Building elements
###############################################################################
@pytest.mark.skipif(not HAS_ANSYS, reason="Requires ANSYS installed")
def test_e(mapdl, cleared):
    mapdl.et("", 183)
    n0 = mapdl.n("", 0, 0, 0)
    n1 = mapdl.n("", 1, 0, 0)
    n2 = mapdl.n("", 1, 1, 0)
    n3 = mapdl.n("", 0, 1, 1)
    n4 = mapdl.n("", 0, 1, -1)
    e0 = mapdl.e(n0, n1, n2, n3)
    assert e0 == 1
    e1 = mapdl.e(n0, n1, n2, n4)
    assert e1 == 2


@pytest.mark.skipif(not HAS_ANSYS, reason="Requires ANSYS installed")
def test_et(mapdl, cleared):
    n_plane183 = mapdl.et("", "PLANE183")
    assert n_plane183 == 1
    n_compare = int(mapdl.get_float("ETYP", 0, "NUM", "MAX"))
    assert n_plane183 == n_compare
    n_plane183 = mapdl.et(17, "PLANE183")
    assert n_plane183 == 17



###############################################################################
# Building geometry
###############################################################################
@pytest.mark.skipif(not HAS_ANSYS, reason="Requires ANSYS installed")
def test_k(cleared, mapdl):
    k0 = mapdl.k("", 0, 0, 0)
    assert k0 == 1
    k1 = mapdl.k(2, 0, 0, 1)
    assert k1 == 2


@pytest.mark.skipif(not HAS_ANSYS, reason="Requires ANSYS installed")
def test_l(cleared, mapdl):
    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 1, 0, 0)
    l0 = mapdl.l(k0, k1)
    assert l0 == 1


@pytest.mark.skipif(not HAS_ANSYS, reason="Requires ANSYS installed")
def test_a(cleared, mapdl):
    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 1, 0, 0)
    k2 = mapdl.k("", 0, 1, 0)
    a0 = mapdl.a(k0, k1, k2)
    assert a0 == 1


@pytest.mark.skipif(not HAS_ANSYS, reason="Requires ANSYS installed")
def test_v(cleared, mapdl):
    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 1, 0, 0)
    k2 = mapdl.k("", 0, 1, 0)
    k3 = mapdl.k("", 0, 0, 1)
    v0 = mapdl.v(k0, k1, k2, k3)
    assert v0 == 1


@pytest.mark.skipif(not HAS_ANSYS, reason="Requires ANSYS installed")
def test_n(cleared, mapdl):
    n0 = mapdl.n("", 0, 0, 0)
    assert n0 == 1
    n1 = mapdl.n(2, 0, 0, 1)
    assert n1 == 2


@pytest.mark.skipif(not HAS_ANSYS, reason="Requires ANSYS installed")
def test_bsplin(cleared, mapdl):
    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 1, 0, 0)
    k2 = mapdl.k("", 2, 1, 0)
    l0 = mapdl.bsplin(k0, k1, k2)
    assert l0 == 1


@pytest.mark.skipif(not HAS_ANSYS, reason="Requires ANSYS installed")
def test_a(cleared, mapdl):
    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 1, 0, 0)
    k2 = mapdl.k("", 1, 1, 0)
    k3 = mapdl.k("", 0, 1, 0)
    a0 = mapdl.a(k0, k1, k2, k3)
    assert a0 == 1


@pytest.mark.skipif(not HAS_ANSYS, reason="Requires ANSYS installed")
def test_al(cleared, mapdl):
    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 1, 0, 0)
    k2 = mapdl.k("", 1, 1, 0)
    k3 = mapdl.k("", 0, 1, 0)
    l0 = mapdl.l(k0, k1)
    l1 = mapdl.l(k1, k2)
    l2 = mapdl.l(k2, k3)
    l3 = mapdl.l(k3, k0)
    a0 = mapdl.al(l0, l1, l2, l3)
    assert a0 == 1


@pytest.mark.skipif(not HAS_ANSYS, reason="Requires ANSYS installed")
def test_invalid():
    with pytest.raises(Exception):
        mapdl.a(0, 0, 0, 0)


@pytest.mark.skipif(not HAS_ANSYS, reason="Requires ANSYS installed")
def test_al(cleared, mapdl):
    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 1, 0, 0)
    k2 = mapdl.k("", 1, 1, 0)
    k3 = mapdl.k("", 0, 1, 0)
    l0 = mapdl.l(k0, k1)
    l1 = mapdl.l(k1, k2)
    l2 = mapdl.l(k2, k3)
    l3 = mapdl.l(k3, k0)
    a0 = mapdl.al(l0, l1, l2, l3)
    mapdl.enable_interactive_plotting()
    mapdl._show_matplotlib_figures = False
    mapdl.aplot()
