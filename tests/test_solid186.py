# import pytest
import numpy as np
import os
import pyansys
from pyansys import examples

test_path = os.path.dirname(os.path.abspath(__file__))
testfiles_path = os.path.join(test_path, 'testfiles', 'solid186')

class TestResultReader(object):
    result = pyansys.ResultReader(examples.rstfile)
    archive = pyansys.Archive(examples.hexarchivefile)

    def test_geometry_elements(self):
        r_elem = self.result.geometry['elem'][self.result.sidx_elem]
        a_elem = self.archive.raw['elem']
        assert np.allclose(r_elem, a_elem)

    def test_geometry_nodes(self):
        r_node = self.result.geometry['nodes']
        a_node = self.archive.raw['nodes']
        assert np.allclose(r_node, a_node)

    def test_geometry_nodenum(self):
        r_values = self.result.geometry['nnum']
        a_values = self.archive.raw['nnum']
        assert np.allclose(r_values, a_values)

    def test_results_displacement(self):
        textfile = os.path.join(testfiles_path, 'prnsol_u.txt')
        nnum, r_values = self.result.nodal_solution(0)
        a_values = np.loadtxt(textfile, skiprows=2)[:, 1:4]
        assert np.allclose(r_values, a_values)

    def test_results_stress(self):
        r_nnum, r_values = self.result.nodal_stress(0)
        textfile = os.path.join(testfiles_path, 'prnsol_s.txt')
        a_values = np.loadtxt(textfile, skiprows=2)[:, 1:]

        # ignore nan
        nanmask = ~np.isnan(r_values).any(1)
        assert np.allclose(r_values[nanmask], a_values, atol=1E-1)

    def test_results_pstress(self):
        r_nnum, r_values = self.result.principal_nodal_stress(0)
        textfile = os.path.join(testfiles_path, 'prnsol_s_prin.txt')
        a_values = np.loadtxt(textfile, skiprows=2)[:, 1:]

        # ignore nan
        nanmask = ~np.isnan(r_values).any(1)
        assert np.allclose(r_values[nanmask], a_values, atol=100)
