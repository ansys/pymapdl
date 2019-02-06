import os
import numpy as np
import pyansys

test_path = os.path.dirname(os.path.abspath(__file__))
testfiles_path = os.path.join(test_path, 'testfiles')


class TestLoadArchive182_183():

    filename = os.path.join(testfiles_path, 'plane182_183.cdb')
    archive = pyansys.Archive(filename)
    assert archive.raw['nnum'].size == 6242
    assert archive.raw['elem'].shape[0] == 3000

    def test_parse(self):
        nnode = self.archive.raw['nnum'].size
        nelem = self.archive.raw['elem'].shape[0]
        grid = self.archive.parse_vtk()
        assert grid.n_points == nnode
        assert grid.n_cells == nelem
        assert np.sum(grid.celltypes == 9) == 1500
        assert np.sum(grid.celltypes == 23) == 1500
        assert np.allclose(self.archive.raw['nodes'][:, :3], grid.points)
