"""
Sample result file generated with

import os
from pyansys import examples
import pyansys

os.environ['I_MPI_SHM_LMT'] = 'shm'
mapdl = pyansys.launch_mapdl(override=True)

mapdl.cdread('db', examples.hexarchivefile)
mapdl.esel('s', 'ELEM', vmin=5, vmax=20)
mapdl.cm('ELEM_COMP', 'ELEM')
mapdl.nsel('s', 'NODE', vmin=5, vmax=20)
mapdl.cm('NODE_COMP', 'NODE')

# boundary conditions
mapdl.allsel()

# dummy steel properties
mapdl.prep7()
mapdl.mp('EX', 1, 200E9)  # Elastic moduli in Pa (kg/(m*s**2))
mapdl.mp('DENS', 1, 7800)  # Density in kg/m3
mapdl.mp('NUXY', 1, 0.3)  # Poissons Ratio
mapdl.emodif('ALL', 'MAT', 1)

# fix one end of the beam
mapdl.nsel('S', 'LOC', 'Z')
mapdl.d('all', 'all')
mapdl.allsel()

mapdl.modal_analysis(nmode=1)

"""
import os

import numpy as np
import pytest
from pyvista.plotting import system_supports_plotting

from pyansys.examples.downloads import _download_and_read as download_and_read
import pyansys

try:
    vm33 = pyansys.download_verification_result(33)
except:
    vm33 = None

try:
    vm240 = pyansys.download_verification_result(240)
except:
    vm240 = None

try:
    vm240_sparse = download_and_read('vm240_sparse.rst')
except:
    vm240_sparse = None


try:
    pontoon = pyansys.download_pontoon()
except:
    pontoon = None


test_path = os.path.dirname(os.path.abspath(__file__))
testfiles_path = os.path.join(test_path, 'testfiles')

is16_filename = os.path.join(testfiles_path, 'is16.rst')
is16_known_result = os.path.join(testfiles_path, 'is16.npz')
if os.path.isfile(is16_filename):
    is16 = pyansys.read_binary(is16_filename)
else:
    is16 = None

temperature_rst = os.path.join(testfiles_path, 'temp_v13.rst')
temperature_known_result = os.path.join(testfiles_path, 'temp_v13.npz')

@pytest.fixture(scope='module')
def hex_pipe_corner():
    filename = os.path.join(testfiles_path, 'rst', 'cyc_stress.rst')
    return pyansys.read_binary(filename)


@pytest.fixture(scope='module')
def hex_rst():
    filename = os.path.join(testfiles_path, 'hex_201.rst')
    return pyansys.read_binary(filename)


@pytest.mark.skipif(vm33 is None, reason="Requires example files")
def test_write_tables(tmpdir):
    filename = str(tmpdir.mkdir("tmpdir").join('vm33.txt'))
    vm33.write_tables(filename)
    assert os.path.isfile(filename)


@pytest.mark.skipif(vm33 is None, reason="Requires example files")
def test_nodal_displacement():
    nnum, result = vm33.nodal_solution(0)
    nnum_, result_ = vm33.nodal_displacement(0)
    assert np.allclose(nnum, nnum_)
    assert np.allclose(result, result_)


def test_read_volume():
    rst_file = os.path.join(testfiles_path, 'vol_test.rst')
    rst = pyansys.read_binary(rst_file)
    enum, edata, enode = rst.element_solution_data(0, datatype='ENG')
    edata = np.asarray(edata)
    volume = edata[:, 0]

    enum_vtk = np.sort(rst.grid.cell_arrays['ansys_elem_num'])
    assert np.allclose(enum, enum_vtk)
    assert np.allclose(volume, 291895460.0)


@pytest.mark.skipif(vm33 is None, reason="Requires example files")
def nodal_displacement():
    nnum, disp = vm33.nodal_displacement(0)
    assert isinstance(nnum, np.ndarray)
    assert isinstance(disp, np.ndarray)


@pytest.mark.skipif(vm33 is None, reason="Requires example files")
def test_nodal_thermal_strain():
    _, tstrain = vm33.nodal_thermal_strain(0)
    assert np.any(tstrain)
    assert tstrain.shape == (vm33.grid.n_points, 8)


@pytest.mark.skipif(not system_supports_plotting(), reason="Requires active X Server")
@pytest.mark.skipif(vm33 is None, reason="Requires example files")
def test_plot_nodal_thermal_strain():
    vm33.plot_nodal_thermal_strain(0, 'X', off_screen=True)


@pytest.mark.skipif(not system_supports_plotting(), reason="Requires active X Server")
@pytest.mark.skipif(vm33 is None, reason="Requires example files")
def test_plot_nodal_thermal_strain():
    vm33._animate_time_solution('ENS', off_screen=True)


@pytest.mark.skipif(pontoon is None, reason="Requires example files")
def test_nodal_elastic_strain():
    _, estrain = pontoon.nodal_elastic_strain(0)
    assert np.any(estrain)
    assert estrain.shape == (pontoon.grid.n_points, 7)


@pytest.mark.skipif(not system_supports_plotting(), reason="Requires active X Server")
@pytest.mark.skipif(pontoon is None, reason="Requires example files")
def test_plot_nodal_elastic_strain():
    pontoon.plot_nodal_elastic_strain(0, 'X', off_screen=True)


@pytest.mark.skipif(not system_supports_plotting(), reason="Requires active X Server")
@pytest.mark.skipif(pontoon is None, reason="Requires example files")
def test_plot_pontoon():
    pontoon.plot(off_screen=True)


@pytest.mark.skipif(not system_supports_plotting(), reason="Requires active X Server")
@pytest.mark.skipif(pontoon is None, reason="Requires example files")
def test_plot_pontoon_nodal_displacement():
    pontoon.plot_nodal_solution(0, show_displacement=True,
                                overlay_wireframe=True, off_screen=True)


@pytest.mark.skipif(not system_supports_plotting(), reason="Requires active X Server")
@pytest.mark.skipif(pontoon is None, reason="Requires example files")
def test_plot_pontoon_nodal_displacement():
    pontoon.plot_nodal_displacement(0, show_displacement=True,
                                    overlay_wireframe=True, off_screen=True)


@pytest.mark.skipif(pontoon is None, reason="Requires example files")
def test_print_pontoon_components():
    assert isinstance(pontoon.node_components, dict)


@pytest.mark.skipif(pontoon is None, reason="Requires example files")
def test_repr():
    assert 'Title' in str(pontoon)


@pytest.mark.skipif(pontoon is None, reason="Requires example files")
def test_available_results():
    assert 'ENS' in pontoon.available_results


@pytest.mark.skipif(vm33 is None, reason="Requires example files")
def test_solution_info():
    info = vm33.solution_info(0)
    assert 'omega_a_x' in info


@pytest.mark.skipif(vm240 is None or vm240_sparse is None,
                    reason="Requires example files")
def test_sparse_nodal_solution():
    nnum, stress = vm240.nodal_stress(0)
    sparse_nnum, sparse_stress = vm240_sparse.nodal_stress(0)
    assert np.allclose(sparse_stress, stress, equal_nan=True)
    assert np.allclose(nnum, sparse_nnum)


@pytest.mark.skipif(is16 is None, reason="Requires example files")
def test_is16():
    npz_rst = np.load(is16_known_result)
    nnum, data = is16.nodal_solution(0)
    assert np.allclose(data, npz_rst['data'], atol=1E-6)
    assert np.allclose(nnum, npz_rst['nnum'])


@pytest.mark.skipif(not os.path.isfile(temperature_rst),
                    reason="Requires example files")
def test_read_temperature():
    temp_rst = pyansys.read_binary(temperature_rst)
    nnum, temp = temp_rst.nodal_temperature(0)

    npz_rst = np.load(temperature_known_result)
    assert np.allclose(nnum, npz_rst['nnum'])
    assert np.allclose(temp, npz_rst['temp'])


@pytest.mark.skipif(not system_supports_plotting(), reason="Requires active X Server")
@pytest.mark.skipif(not os.path.isfile(temperature_rst),
                    reason="Requires example files")
def test_plot_nodal_temperature():
    temp_rst = pyansys.read_binary(temperature_rst)
    temp_rst.plot_nodal_temperature(0, off_screen=True)


def test_rst_node_components(hex_rst):
    assert 'ELEM_COMP' not in hex_rst.node_components
    np.allclose(hex_rst.node_components['NODE_COMP'].nonzero()[0],
                np.arange(4, 20))


def test_rst_node_components(hex_rst):
    assert 'NODE_COMP' not in hex_rst.element_components
    np.allclose(hex_rst.element_components['ELEM_COMP'].nonzero()[0],
                np.arange(4, 20))


def test_rst_beam4_shell63():
    filename = os.path.join(testfiles_path, 'shell63_beam4.rst')

    # check geometry can load
    rst = pyansys.read_binary(filename)
    assert isinstance(rst.grid.points, np.ndarray)
    assert isinstance(rst.grid.cells, np.ndarray)
    assert (rst.grid.cells >= 0).all()
    assert (rst.grid.cells <= 50).all()

    # not a great test, but verifies results load
    assert np.any(rst.nodal_displacement(0)[1] > 0)


def test_cyl_stress(hex_pipe_corner):
    # ANSYS results generated with
    # RSYS, 0
    # PRNSOL, S
    # RSYS, 1
    # PRNSOL, S

    filename = os.path.join(testfiles_path, 'rst', 'cyc_stress.rst')
    nnum, my_stress = hex_pipe_corner.cylindrical_nodal_stress(0)

    ans_stress = np.load(os.path.join(testfiles_path, 'rst', 'cyc_stress.npy'))
    assert np.allclose(my_stress[-114:], ans_stress, atol=1E-7)


@pytest.mark.skipif(not system_supports_plotting(), reason="Requires active X Server")
def test_plot_cyl_stress(hex_pipe_corner):
    # ANSYS results generated with
    # RSYS, 0
    # PRNSOL, S
    # RSYS, 1
    # PRNSOL, S

    with pytest.raises(ValueError):
        cpos = hex_pipe_corner.plot_cylindrical_nodal_stress(0, off_screen=True)
    with pytest.raises(ValueError):
        cpos = hex_pipe_corner.plot_cylindrical_nodal_stress(0, comp='X',
                                                             off_screen=True)    
    cpos = hex_pipe_corner.plot_cylindrical_nodal_stress(0, comp='R', off_screen=True)
    assert cpos
