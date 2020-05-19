"""
Test loading results from plane183

Need to add ansys results for verification...

"""
import os

import pytest
import numpy as np
import pyansys

testfiles_path = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture(scope='module')
def result():
    filename = os.path.join(testfiles_path, 'pyansys_182_183_42_82.rst')
    return pyansys.read_binary(filename)


def test_load(result):
    assert np.any(result.grid.cells)
    assert np.any(result.grid.points)


def test_displacement(result):
    nnum, disp = result.nodal_solution(0)
    ansys_nnum = np.load(os.path.join(testfiles_path, 'prnsol_u_nnum.npy'))
    ansys_disp = np.load(os.path.join(testfiles_path, 'prnsol_u.npy'))
    assert np.allclose(nnum, ansys_nnum)
    assert np.allclose(disp, ansys_disp, rtol=1E-4)  # rounding in text file


def test_stress(result):
    ansys_nnum = np.load(os.path.join(testfiles_path, 'prnsol_s_nnum.npy'))
    ansys_stress = np.load(os.path.join(testfiles_path, 'prnsol_s.npy'))
    nnum, stress = result.nodal_stress(0)
    mask = np.in1d(nnum, ansys_nnum)
    assert np.allclose(stress[mask], ansys_stress, atol=1E-6)
