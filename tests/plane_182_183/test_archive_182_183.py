import os
import numpy as np
import pyansys

try:
    testfiles_path = os.path.dirname(os.path.abspath(__file__))
except:
    testfiles_path = '/home/alex/afrl/python/source/pyansys/tests/'


class TestLoadArchive182_183():

    filename = os.path.join(testfiles_path, 'archive.cdb')
    archive = pyansys.Archive(filename)
    assert archive.raw['nnum'].size == 12484
    assert archive.raw['elem'].shape[0] == 6000

    def test_parse(self):
        nnode = self.archive.raw['nnum'].size
        nelem = self.archive.raw['elem'].shape[0]
        grid = self.archive.parse_vtk()
        assert grid.n_points == nnode
        assert grid.n_cells == nelem
        assert np.sum(grid.celltypes == 9) == 3000
        assert np.sum(grid.celltypes == 23) == 3000
        assert np.allclose(self.archive.raw['nodes'][:, :3], grid.points)
