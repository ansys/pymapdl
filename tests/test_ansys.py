import glob
import os

import pytest
import numpy as np
import pyansys

from pyvista.plotting import system_supports_plotting

path = os.path.dirname(os.path.abspath(__file__))

# rver = 'v150'
rver = 'v182'
# rver = 'v182'
# rver = 'v194'
# rver = 'v201'
MAPDLBIN = {'v150': '/usr/ansys_inc/v150/ansys/bin/ansys150',
            'v182': '/usr/ansys_inc/v182/ansys/bin/ansys182',
            'v194': '/usr/ansys_inc/v194/ansys/bin/ansys194',
            'v201': '/usr/ansys_inc/v201/ansys/bin/ansys201',
            'v202': '/usr/ansys_inc/v202/ansys/bin/ansys202'}

HAS_ANSYS = os.path.isfile(MAPDLBIN[rver])


@pytest.fixture(scope='module')
def mapdl():
    mapdl = pyansys.Mapdl(MAPDLBIN[rver],
                          override=True, jobname=rver,
                          loglevel='ERROR',
                          interactive_plotting=False,
                          prefer_pexpect=True)

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
    mapdl.Modopt('lanb', 3, 1, 10000)
    mapdl.Eqslv('SPARSE')
    mapdl.Lumpm(0)
    mapdl.Pstres(0)
    mapdl.Bcsoption('INCORE')
    mapdl.mxpand(elcalc='YES')
    mapdl.solve()
    mapdl.finish()

    # setup ansys for output without line breaks
    mapdl.post1()
    mapdl.set(1, 1)
    mapdl.header('OFF', 'OFF', 'OFF', 'OFF', 'OFF', 'OFF')
    nsigfig = 10
    mapdl.format('', 'E', nsigfig + 9, nsigfig)
    mapdl.page(1E9, '', -1, 240)

    return mapdl


@pytest.mark.skipif(not pyansys.has_ansys, reason="Requires ANSYS installed")
def test_prnsol_u(mapdl):
    # verify cyclic displacements
    table = mapdl.prnsol('u').splitlines()
    if mapdl.using_corba:
        array = np.genfromtxt(table[7:])
    else:
        array = np.genfromtxt(table[9:])
    ansys_nnum = array[:, 0].astype(np.int)
    ansys_disp = array[:, 1:-1]

    nnum, disp = mapdl.result.nodal_solution(0)

    # cyclic model will only output the master sector
    ansys_nnum = ansys_nnum[:nnum.size]
    ansys_disp = ansys_disp[:nnum.size]

    assert np.allclose(ansys_nnum, nnum)
    assert np.allclose(ansys_disp, disp)


@pytest.mark.skipif(not pyansys.has_ansys, reason="Requires ANSYS installed")
def test_presol_s(mapdl):
    # verify element stress
    element_stress, _, enode = mapdl.result.element_stress(0)
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

    assert np.allclose(element_stress, ansys_element_stress)
    assert np.allclose(enode, ansys_enode)


@pytest.mark.skipif(not pyansys.has_ansys, reason="Requires ANSYS installed")
def test_prnsol_s(mapdl):
    # verify cyclic displacements
    table = mapdl.prnsol('s').splitlines()
    if mapdl.using_corba:
        array = np.genfromtxt(table[7:])
    else:
        array = np.genfromtxt(table[10:])
    ansys_nnum = array[:, 0].astype(np.int)
    ansys_stress = array[:, 1:]

    nnum, stress = mapdl.result.nodal_stress(0)

    # v150 includes nodes in the geometry that aren't in the result
    mask = np.in1d(nnum, ansys_nnum)
    nnum = nnum[mask]
    stress = stress[mask]

    assert np.allclose(ansys_nnum, nnum)
    assert np.allclose(ansys_stress, stress)


@pytest.mark.skipif(not pyansys.has_ansys, reason="Requires ANSYS installed")
def test_prnsol_prin(mapdl):
    # verify principal stress
    table = mapdl.prnsol('prin').splitlines()
    if mapdl.using_corba:
        array = np.genfromtxt(table[7:])
    else:
        array = np.genfromtxt(table[10:])
    ansys_nnum = array[:, 0].astype(np.int)
    ansys_stress = array[:, 1:]

    nnum, stress = mapdl.result.principal_nodal_stress(0)

    # v150 includes nodes in the geometry that aren't in the result
    mask = np.in1d(nnum, ansys_nnum)
    nnum = nnum[mask]
    stress = stress[mask]

    assert np.allclose(ansys_nnum, nnum)
    assert np.allclose(ansys_stress, stress, atol=1E-5, rtol=1E-4)


# @pytest.mark.skipif(not system_supports_plotting(), reason="Requires active X Server")
# def test_plot(self):
#     filename = '/tmp/temp.png'
#     self.result.plot_nodal_solution(0, screenshot=filename,
#                                   off_screen=True)

#     # self.result.plot_nodal_stress(0, 'Sx', screenshot=filename,
#     #                             off_screen=True)

#     self.result.plot_principal_nodal_stress(0, 'EQV', screenshot=filename,
#                                             off_screen=True)


def test_read_para():
    para_path = os.path.join(path, 'testfiles', 'para')
    para_files = glob.glob(os.path.join(para_path, '*.txt'))
    from pyansys.mapdl import load_parameters
    for para_file in para_files:
        arr, parm = load_parameters(para_file)


@pytest.mark.skipif(not pyansys.has_ansys, reason="Requires ANSYS installed")
def test_v150():
    mapdl = pyansys.Mapdl(MAPDLBIN['v150'], override=True)
    mapdl.prep7()
    mapdl.exit()


@pytest.mark.skipif(not pyansys.has_ansys, reason="Requires ANSYS installed")
def test_v182():
    mapdl = pyansys.Mapdl(MAPDLBIN['v182'], override=True)
    mapdl.prep7()
    mapdl.exit()


@pytest.mark.skipif(not pyansys.has_ansys, reason="Requires ANSYS installed")
def test_v194():
    mapdl = pyansys.Mapdl(MAPDLBIN['v194'], override=True)
    mapdl.prep7()
    mapdl.exit()
