import os

import pytest
import numpy as np

import pyansys
from pyansys.emat import EmatFile

try:
    __file__
except NameError:
    __file__ = '/home/alex/afrl/python/source/pyansys/tests/test_emat.py'

test_path = os.path.dirname(os.path.abspath(__file__))
testfiles_path = os.path.join(test_path, 'testfiles')
emat_filename = os.path.join(testfiles_path, 'file.emat')


@pytest.fixture(scope='module')
def emat():
    emat_bin = pyansys.read_binary(emat_filename)
    assert isinstance(emat_bin, EmatFile)
    return emat_bin


def test_load_element(emat):
    dof_idx, element_data = emat.read_element(0)
    assert 'stress' in element_data
    assert 'mass' in element_data


def test_global_applied_force(emat):
    force = emat.global_applied_force()
    assert np.allclose(force, 0)


def test_eeqv(emat):
    assert np.allclose(np.sort(emat.eeqv), emat.enum)


def test_neqv(emat):
    assert np.allclose(np.sort(emat.neqv), emat.nnum)
