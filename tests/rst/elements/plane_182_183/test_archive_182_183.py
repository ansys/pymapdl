import os

import pytest
import numpy as np
import pyansys

testfiles_path = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture(scope='module')
def archive():
    filename = os.path.join(testfiles_path, 'archive.cdb')
    return pyansys.Archive(filename)


def test_archive_load(archive):
    assert archive.nnum.size == 12484
    assert len(archive.elem) == 6000


def test_parse(archive):
    nnode = archive.nnum.size
    nelem = len(archive.elem)
    assert archive.grid.n_points == nnode
    assert archive.grid.n_cells == nelem
    assert np.sum(archive.grid.celltypes == 9) == 3000
    assert np.sum(archive.grid.celltypes == 23) == 3000
    assert np.allclose(archive.nodes, archive.grid.points)
