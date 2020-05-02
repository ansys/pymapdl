import os

import pytest
import numpy as np
import pyansys

try:
    testfiles_path = os.path.dirname(os.path.abspath(__file__))
except:
    testfiles_path = '/home/alex/afrl/python/source/pyansys/tests/'

@pytest.fixture(scope='module')
def archive():
    filename = os.path.join(testfiles_path, 'archive.cdb')
    return pyansys.Archive(filename)


def test_archive_load(archive):
    assert archive.raw['nnum'].size == 12484
    assert archive.raw['elem'].shape[0] == 6000


def test_parse(archive):
    nnode = archive.raw['nnum'].size
    nelem = archive.raw['elem'].shape[0]
    grid = archive.parse_vtk()
    assert grid.n_points == nnode
    assert grid.n_cells == nelem
    assert np.sum(grid.celltypes == 9) == 3000
    assert np.sum(grid.celltypes == 23) == 3000
    assert np.allclose(archive.raw['nodes'][:, :3], grid.points)
