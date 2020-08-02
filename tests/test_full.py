import os

import scipy
import pytest
import numpy as np

import pyansys
from pyansys.examples import fullfile

test_path = os.path.dirname(os.path.abspath(__file__))
testfiles_path = os.path.join(test_path, 'testfiles')


@pytest.fixture()
def sparse_full():
    filename = os.path.join(testfiles_path, 'sparse.full')
    return pyansys.read_binary(filename)


def test_fullreader():
    fobj = pyansys.read_binary(fullfile)
    dofref, k, m = fobj.load_km()
    assert dofref.size
    assert k.size
    assert m.size


def test_full_sparse(sparse_full):
    str_rep = str(sparse_full)
    assert '20.1' in str_rep
    assert 'MAPDL Full File' in str_rep
    assert '345' in str_rep


def test_full_sparse_k(sparse_full):
    assert isinstance(sparse_full.k, scipy.sparse.csc.csc_matrix)
    neqn = sparse_full._header['neqn']
    assert sparse_full.k.shape == (neqn, neqn)


def test_full_sparse_m(sparse_full):
    assert isinstance(sparse_full.m, scipy.sparse.csc.csc_matrix)
    neqn = sparse_full._header['neqn']
    assert sparse_full.m.shape == (neqn, neqn)


def test_full_sparse_dof_ref(sparse_full):
    # tests if sorted ascending
    assert (np.diff(sparse_full.dof_ref[:, 0]) >= 0).all()
    assert np.allclose(np.unique(sparse_full.dof_ref[:, 1]), [0, 1, 2])


def test_full_sparse_const(sparse_full):
    assert not sparse_full.const.any()


def test_full_load_km(sparse_full):
    dof_ref, k, m = sparse_full.load_km()
    assert not (np.diff(dof_ref[:, 0]) >= 0).all()
    neqn = sparse_full._header['neqn']
    assert k.shape == (neqn, neqn)
    assert m.shape == (neqn, neqn)

    # make sure internal values are not overwritten
    assert (np.diff(sparse_full.dof_ref[:, 0]) >= 0).all()


def test_load_vector(sparse_full):
    assert not sparse_full.load_vector.any()
