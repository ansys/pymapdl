import glob
import os
import sys

import pytest
import numpy as np
import pyansys

if sys.platform != 'darwin':
    from pyansys.mapdl_corba import MapdlCorba

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
    mapdl = pyansys.launch_mapdl(MAPDLBIN,
                                 override=True,
                                 additional_switches='-smp',  # for Linux
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
    mapdl.run('/SOLU')
    mapdl.antype(2, 'new')
    mapdl.modopt('lanb', 1, 1, 100000)
    mapdl.eqslv('SPARSE')
    mapdl.lumpm(0)
    mapdl.pstres(0)
    mapdl.bcsoption('INCORE')
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


def test_str(mapdl):
    assert 'ANSYS Mechanical' in str(mapdl)


###############################################################################
# Testing binary reader
###############################################################################
@pytest.mark.parametrize("rset", RSETS)
@pytest.mark.skipif(not HAS_ANSYS, reason="Requires ANSYS installed")
def test_prnsol_u(mapdl, rset):
    mapdl.set(*rset)
    # verify cyclic displacements
    table = mapdl.prnsol('u').splitlines()
    if isinstance(mapdl, MapdlCorba):
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
    if isinstance(mapdl, MapdlCorba):
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
    if isinstance(mapdl, MapdlCorba):
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
    response = mapdl.aplot()
    assert 'WRITTEN TO FILE' in response


@pytest.mark.skipif(not HAS_ANSYS, reason="Requires ANSYS installed")
def test_logging(mapdl, tmpdir):
    filename = str(tmpdir.mkdir("tmpdir").join('tmp.inp'))
    with pytest.raises(RuntimeError):
        mapdl.open_apdl_log(filename, mode='w')

    mapdl.prep7()
    mapdl.k(1, 0, 0, 0)
    mapdl.k(2, 1, 0, 0)
    mapdl.k(3, 1, 1, 0)
    mapdl.k(4, 0, 1, 0)

    mapdl._apdl_log.flush()

    out = open(mapdl._apdl_log.name).read().strip().split()[-5:]
    assert 'PREP7' in out[0]
    assert 'K,4,0,1,0' in out[-1]


def test_nodes(cleared, mapdl):
    mapdl.prep7()
    mapdl.cdread('db', pyansys.examples.sector_archive_file)
    archive = pyansys.Archive(pyansys.examples.sector_archive_file, parse_vtk=False)
    mapdl.nwrite('/tmp/ansys/tmp.nodes')
    assert np.allclose(mapdl.nodes, archive.nodes)


def test_nnum(cleared, mapdl):
    mapdl.prep7()
    mapdl.n(1, 0, 0, 0)
    mapdl.n(11, 10, 0, 0)
    mapdl.fill(1, 11, 9)
    assert mapdl._nblock_cache is None
    assert np.allclose(mapdl.nnum, range(1, 12))
    assert mapdl._nblock_cache is not None


@pytest.mark.parametrize("knum", [True, False])
def test_nplot_vtk(cleared, mapdl, knum):
    mapdl.enable_interactive_plotting()
    mapdl.prep7()
    mapdl.n(1, 0, 0, 0)
    mapdl.n(11, 10, 0, 0)
    mapdl.fill(1, 11, 9)
    mapdl.nplot(vtk=True, knum=knum, background='w', color='k', off_screen=True)


def test_elements(cleared, mapdl):
    mapdl.et(1, 188)
    mapdl.n(1, 0, 0, 0)
    mapdl.n(2, 1, 0, 0)
    mapdl.n(3, 2, 0, 0)
    mapdl.n(4, 3, 0, 0)
    mapdl.e(1, 2)
    mapdl.e(2, 3)
    mapdl.e(3, 4)

    expected = np.array([[1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 2],
                         [1, 1, 1, 1, 0, 0, 0, 0, 2, 0, 2, 3],
                         [1, 1, 1, 1, 0, 0, 0, 0, 3, 0, 3, 4]])

    assert np.allclose(np.array(mapdl.elements), expected)

@pytest.mark.parametrize("arr", ([1, 2, 3],
                                 [[1, 2, 3], [1, 2, 3]],
                                 np.random.random((10)),
                                 np.random.random((10, 3)),
                                 np.random.random((10, 3, 3))))
def test_load_array(cleared, mapdl, arr):
    mapdl.load_array(arr, 'MYARR')
    parm, mapdl_arrays = mapdl.load_parameters()
    assert np.allclose(mapdl_arrays['MYARR'], arr)


def test_load_array_err(cleared, mapdl):
    with pytest.raises(TypeError):
        mapdl.load_array(['apple'], 'MYARR')

    with pytest.raises(ValueError):
        mapdl.load_array(np.empty((1, 1, 1, 1)), 'MYARR')


# must be at end as this uses a scoped fixture
@pytest.mark.skipif(not HAS_ANSYS, reason="Requires ANSYS installed")
def test_exit(mapdl):
    mapdl.exit()
    with pytest.raises(RuntimeError):
        mapdl.prep7()

    assert not os.path.isfile(mapdl._lockfile)
