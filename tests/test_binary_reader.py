import shutil
import os

import pytest
from pyvista.plotting import system_supports_plotting

import numpy as np
import pyvista as pv

import pyansys
from pyansys import examples
from pyansys._rst_keys import element_index_table_info


try:
    __file__
except:
    __file__ = '/home/alex/afrl/python/source/pyansys/tests/test_binary_reader.py'


test_path = os.path.dirname(os.path.abspath(__file__))
testfiles_path = os.path.join(test_path, 'testfiles')

@pytest.fixture(scope='module')
def example_result():
    return pyansys.read_binary(examples.rstfile)


result_types = ['ENS', 'EPT', 'ETH', 'EEL', 'ENG']# 'ENF']
@pytest.mark.parametrize("result_type", result_types)
def test_save_as_vtk(tmpdir, example_result, result_type):
    filename = str(tmpdir.mkdir("tmpdir").join('tmp.vtk'))
    example_result.save_as_vtk(filename, result_types=[result_type])

    grid = pv.UnstructuredGrid(filename)
    for i in range(example_result.nsets):
        key = 'Nodal Solution %d' % i
        assert key in grid.point_arrays
        arr = grid.point_arrays[key]
        assert np.allclose(arr, example_result.nodal_solution(i)[1], atol=1E-5)
        # breakpoint()

        key = '%s %d' % (element_index_table_info[result_type], i)
        assert key in grid.point_arrays
        arr = grid.point_arrays[key]
        _, rst_arr = example_result._nodal_result(i, result_type)
        if rst_arr.shape[1] == 1:
            rst_arr = rst_arr.ravel()
        assert np.allclose(arr, rst_arr, atol=1E-5, equal_nan=True)


@pytest.mark.skipif(not system_supports_plotting(), reason="Requires active X Server")
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
    result.plot_principal_nodal_stress(0, 'EQV',
                                       node_components=components, off_screen=True)


def test_file_close(tmpdir):
    tmpfile = str(tmpdir.mkdir("tmpdir").join('tmp.vtk'))
    shutil.copy(examples.rstfile, tmpfile)
    rst = pyansys.read_binary(tmpfile)
    nnum, stress = rst.nodal_stress(0)
    os.remove(tmpfile)


# def test_memory_leak(example_result):
#     process = psutil.Process(os.getpid())
#     gc.collect()
#     init = process.memory_info().rss
#     for _ in range(100):
#         example_result._nodal_result(0, 'ENS')

#     gc.collect()
#     assert (process.memory_info().rss - init) == 0
