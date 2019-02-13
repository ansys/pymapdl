import numpy as np
import vtki
import pyansys
from pyansys import examples


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
