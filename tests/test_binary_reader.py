import socket
import shutil
import os

import pytest
from pyvista.plotting import system_supports_plotting

import numpy as np
import pyvista as pv

import pyansys
from pyansys import examples
from pyansys._rst_keys import element_index_table_info
from pyansys.misc import get_ansys_bin


HAS_FFMPEG = True
try:
    import imageio_ffmpeg
except ImportError:
    HAS_FFMPEG = False


test_path = os.path.dirname(os.path.abspath(__file__))
testfiles_path = os.path.join(test_path, 'testfiles')


# check for a valid MAPDL install with CORBA
valid_rver = ['182', '190', '191', '192', '193', '194', '195', '201']
EXEC_FILE = None
for rver in valid_rver:
    if os.path.isfile(get_ansys_bin(rver)):
        EXEC_FILE = get_ansys_bin(rver)

if 'PYANSYS_IGNORE_ANSYS' in os.environ:
    HAS_ANSYS = False
else:
    HAS_ANSYS = EXEC_FILE is not None


skip_no_ansys = pytest.mark.skipif(not HAS_ANSYS, reason="Requires ANSYS installed")


skip_no_xserver = pytest.mark.skipif(not system_supports_plotting(),
                                     reason="Requires active X Server")

RSETS = list(zip(range(1, 9), [1]*8))


@pytest.fixture(scope='module')
def result():
    return pyansys.read_binary(examples.rstfile)


@pytest.fixture(scope='module')
def static_canteliver_bc():
    filename = os.path.join(testfiles_path, 'rst', 'beam_static_bc.rst')
    return pyansys.read_binary(filename)



@pytest.fixture(scope="module")
def cyclic_modal(mapdl):
    # build the cyclic model
    mapdl.clear()
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


@pytest.mark.parametrize("rset", RSETS)
@skip_no_ansys
def test_prnsol_u(mapdl, cyclic_modal, rset):
    mapdl.set(*rset)
    # verify cyclic displacements
    table = mapdl.prnsol('u').splitlines()
    if isinstance(mapdl, pyansys.mapdl_corba.MapdlCorba):
        array = np.genfromtxt(table[8:])
    elif isinstance(mapdl, pyansys.mapdl_console.MapdlConsole):
        array = np.genfromtxt(table[9:])
    else:
        raise RuntimeError('Only MapdlCorba and MapdlConsole supported')
    ansys_nnum = array[:, 0].astype(np.int)
    ansys_disp = array[:, 1:-1]

    nnum, disp = mapdl.result.nodal_solution(rset)

    # cyclic model will only output the master sector
    ansys_nnum = ansys_nnum[:nnum.size]
    ansys_disp = ansys_disp[:nnum.size]

    assert np.allclose(ansys_nnum, nnum)
    assert np.allclose(ansys_disp, disp)


@pytest.mark.parametrize("rset", RSETS)
@skip_no_ansys
def test_presol_s(mapdl, cyclic_modal, rset):
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
@skip_no_ansys
def test_prnsol_s(mapdl, cyclic_modal, rset):
    mapdl.set(*rset)

    # verify cyclic displacements
    table = mapdl.prnsol('s').splitlines()
    if isinstance(mapdl, pyansys.mapdl_corba.MapdlCorba):
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
@skip_no_ansys
def test_prnsol_prin(mapdl, cyclic_modal, rset):
    mapdl.set(*rset)

    # verify principal stress
    table = mapdl.prnsol('prin').splitlines()
    if isinstance(mapdl, pyansys.mapdl_corba.MapdlCorba):
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


def test_loadresult(result):
    # check result is loaded
    assert result.nsets
    assert result.mesh.nnum.size

    # check geometry is genreated
    grid = result.grid
    assert grid.points.size
    assert grid.cells.size
    assert 'ansys_node_num' in grid.point_arrays

    # check results can be loaded
    nnum, disp = result.nodal_solution(0)
    assert nnum.size
    assert disp.size

    nnum, disp = result.nodal_solution(0)
    assert nnum.size
    assert disp.size

    nnum, disp = result.principal_nodal_stress(0)
    assert nnum.size
    assert disp.size

    nnum, disp = result.nodal_stress(0)
    assert nnum.size
    assert disp.size

    element_stress, enum, enode = result.element_stress(0)
    assert element_stress[0].size
    assert enum.size
    assert enode[0].size

    element_stress, enum, enode = result.element_stress(0, principal=True)
    assert element_stress[0].size
    assert enum.size
    assert enode[0].size


def test_boundary_conditions(static_canteliver_bc):
    nnum, dof, bc = static_canteliver_bc.nodal_boundary_conditions(0)
    assert np.allclose(nnum, np.array([3, 3, 3, 25, 26, 27]))
    assert np.allclose(dof, np.array([1, 2, 3, 1, 2, 3]))
    assert np.allclose(bc, np.array([0., 0., 0., 0.001, 0.0011, 0.0012]))


def test_force(static_canteliver_bc):
    nnum, dof, force = static_canteliver_bc.nodal_input_force(0)
    assert np.allclose(nnum, np.array([71, 52, 127]))
    assert np.allclose(dof, np.array([2, 1, 3]))
    assert np.allclose(force, np.array([30., 20., 40.]))


def test_dof(result):
    assert result.result_dof(0) == ['UX', 'UY', 'UZ']


result_types = ['ENS', 'EPT', 'ETH', 'EEL', 'ENG']# 'ENF']
@pytest.mark.parametrize("result_type", result_types)
def test_save_as_vtk(tmpdir, result, result_type):
    filename = str(tmpdir.mkdir("tmpdir").join('tmp.vtk'))
    result.save_as_vtk(filename, result_types=[result_type])

    grid = pv.UnstructuredGrid(filename)
    for i in range(result.nsets):
        key = 'Nodal Solution %d' % i
        assert key in grid.point_arrays
        arr = grid.point_arrays[key]
        assert np.allclose(arr, result.nodal_solution(i)[1], atol=1E-5)

        key = '%s %d' % (element_index_table_info[result_type], i)
        assert key in grid.point_arrays
        arr = grid.point_arrays[key]
        _, rst_arr = result._nodal_result(i, result_type)
        if rst_arr.shape[1] == 1:
            rst_arr = rst_arr.ravel()
        assert np.allclose(arr, rst_arr, atol=1E-5, equal_nan=True)


@skip_no_xserver
def test_plot_component():
    """
    # create example file for component plotting
    ansys = pyansys.ANSYS('/usr/ansys_inc/v182/ansys/bin/ansys182')
    ansys.Cdread('db', examples.hexarchivefile)
    # ansys.open_gui()
    ansys.Esel('S', 'ELEM', vmin=1, vmax=20)
    ansys.Nsle('S', 1)
    ansys.Cm('MY_COMPONENT', 'NODE')

    ansys.Nsel('S', 'NODE', '', 1, 40)
    ansys.Cm('MY_OTHER_COMPONENT', 'NODE')

    ansys.Allsel()

    # Aluminum properties (or something)
    ansys.Prep7()
    ansys.Mp('ex', 1, 10e6)
    ansys.Mp('nuxy', 1, 0.3)
    ansys.Mp('dens', 1, 0.1/386.1)
    ansys.Mp('dens', 2, 0)

    ansys.Run("/SOLU")
    ansys.Antype(2, "NEW")
    ansys.Run("BCSOPT,,INCORE")
    ansys.Modopt("LANB", 1)
    ansys.Mxpand(elcalc='YES')
    ansys.Run("/GOPR")
    ansys.Solve()
    ansys.Finish()
    ansys.exit()
    """

    filename = os.path.join(testfiles_path, 'comp_hex_beam.rst')
    result = pyansys.read_binary(filename)

    components = ['MY_COMPONENT', 'MY_OTHER_COMPONENT']
    result.plot_nodal_solution(0, node_components=components,
                               off_screen=True, sel_type_all=False)
    result.plot_nodal_stress(0, 'x', node_components=components, off_screen=True)
    result.plot_principal_nodal_stress(0, 'SEQV',
                                       node_components=components, off_screen=True)


def test_file_close(tmpdir):
    tmpfile = str(tmpdir.mkdir("tmpdir").join('tmp.rst'))
    shutil.copy(examples.rstfile, tmpfile)
    rst = pyansys.read_binary(tmpfile)
    nnum, stress = rst.nodal_stress(0)
    os.remove(tmpfile)  # tests file has been correctly closed


@skip_no_xserver
@pytest.mark.skipif(not HAS_FFMPEG, reason="requires imageio_ffmpeg")
def test_animate_nodal_solution(tmpdir, result):
    temp_movie = str(tmpdir.mkdir("tmpdir").join('tmp.mp4'))
    result.animate_nodal_solution(0, nangles=20, movie_filename=temp_movie,
                                  loop=False, off_screen=True)
    assert np.any(result.grid.points)
    assert os.path.isfile(temp_movie)


def test_loadbeam():
    linkresult_path = os.path.join(testfiles_path, 'link1.rst')
    linkresult = pyansys.read_binary(linkresult_path)
    assert np.any(linkresult.grid.cells)


def test_reaction_forces():
    rst = pyansys.read_binary(os.path.join(testfiles_path, 'vm1.rst'))
    nnum, forces = rst.nodal_static_forces(0)
    assert np.allclose(nnum, [1, 2, 3, 4])
    assert np.allclose(forces[:, 1], [-600, 250, 500, -900])
