import os

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


def test_load_emat():
    emat_file = pyansys.read_binary(emat_filename)
    assert isinstance(emat_file, EmatFile)


def test_load_element():
    emat_file = pyansys.read_binary(emat_filename)
    dof_idx, element_data = emat_file.read_element(0)
    assert 'stress' in element_data
    assert 'mass' in element_data


def test_global_applied_force():
    emat_file = pyansys.read_binary(emat_filename)
    force = emat_file.global_applied_force()
    assert np.allclose(force, 0)
