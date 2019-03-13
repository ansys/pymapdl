import os

import numpy as np
import vtki
import pyansys
from pyansys import examples

try:
    __file__
except:
    __file__ = '/home/alex/afrl/python/source/pyansys/tests/test_binary_reader.py'

test_path = os.path.dirname(os.path.abspath(__file__))
testfiles_path = os.path.join(test_path, 'testfiles')

def test_save_as_vtk(tmpdir):
    filename = str(tmpdir.mkdir("tmpdir").join('tmp.vtk'))
    result = pyansys.ResultReader(examples.rstfile)
    result.save_as_vtk(filename)

    grid = vtki.UnstructuredGrid(filename)
    for i in range(result.nsets):
        assert 'nodal_solution%03d' % i in grid.point_arrays
        arr = grid.point_arrays['nodal_solution%03d' % i]
        assert np.allclose(arr, result.nodal_solution(i)[1], atol=1E-5)

        assert 'nodal_stress%03d' % i in grid.point_arrays
        arr = grid.point_arrays['nodal_stress%03d' % i]
        assert np.allclose(arr, result.nodal_stress(i)[1], atol=1E-5, equal_nan=True)


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
    ansys.Modopt("LANB", 10)
    ansys.Run("/GOPR")
    ansys.Solve()
    ansys.Finish()
    ansys.Exit()
    """

    filename = os.path.join(testfiles_path, 'comp_hex_beam.rst')
    result = pyansys.ResultReader(filename)

    components = ['MY_COMPONENT', 'MY_OTHER_COMPONENT']
    result.plot_nodal_solution(0, node_components=components, interactive=False)
