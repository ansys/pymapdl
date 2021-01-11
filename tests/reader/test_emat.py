import os

import pytest
import numpy as np

import ansys.mapdl.core as pymapdl
from ansys.mapdl.core.emat import EmatFile


test_path = os.path.dirname(os.path.abspath(__file__))
testfiles_path = os.path.join(test_path, 'testfiles')
emat_filename = os.path.join(testfiles_path, 'file.emat')


@pytest.fixture(scope='module')
def emat():
    emat_bin = pymapdl.read_binary(emat_filename)
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
