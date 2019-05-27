# import pytest
import numpy as np
import os
import pyansys
from pyansys import examples

try:
    __file__
except NameError:
    __file__ = '/home/alex/afrl/python/source/pyansys/tests/test_solid186.py'


test_path = os.path.dirname(os.path.abspath(__file__))
testfiles_path = os.path.join(test_path, 'testfiles', 'solid186')

result = pyansys.read_binary(examples.rstfile)
archive = pyansys.Archive(examples.hexarchivefile)


def test_geometry_elements():
    r_elem = result.geometry['elem'][result.sidx_elem]
    a_elem = archive.raw['elem']
    assert np.allclose(r_elem, a_elem)


def test_geometry_nodes():
    r_node = result.geometry['nodes']
    a_node = archive.raw['nodes']
    assert np.allclose(r_node, a_node)


def test_geometry_nodenum():
    r_values = result.geometry['nnum']
    a_values = archive.raw['nnum']
    assert np.allclose(r_values, a_values)


def test_results_displacement():
    textfile = os.path.join(testfiles_path, 'prnsol_u.txt')
    nnum, r_values = result.nodal_solution(0)
    a_values = np.loadtxt(textfile, skiprows=2)[:, 1:4]
    assert np.allclose(r_values, a_values)


def test_results_stress():
    _, r_values = result.nodal_stress(0)
    textfile = os.path.join(testfiles_path, 'prnsol_s.txt')
    a_values = np.loadtxt(textfile, skiprows=2)[:, 1:]

    # ignore nan
    nanmask = ~np.isnan(r_values).any(1)
    assert np.allclose(r_values[nanmask], a_values, atol=1E-1)


def test_results_pstress():
    r_nnum, r_values = result.principal_nodal_stress(0)
    textfile = os.path.join(testfiles_path, 'prnsol_s_prin.txt')
    a_values = np.loadtxt(textfile, skiprows=2)[:, 1:]

    # ignore nan
    nanmask = ~np.isnan(r_values).any(1)
    assert np.allclose(r_values[nanmask], a_values, atol=100)
