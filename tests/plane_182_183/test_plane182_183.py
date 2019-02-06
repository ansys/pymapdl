"""
Test loading results from plane183

Need to add ansys results for verification...

"""
import os
import numpy as np
import pyansys

try:
    testfiles_path = os.path.dirname(os.path.abspath(__file__))
except:
    testfiles_path = '/home/alex/afrl/python/source/pyansys/tests/plane_182_183/'


class TestLoad182_183():
    filename = os.path.join(testfiles_path, 'pyansys_182_183_42_82.rst')
    result = pyansys.ResultReader(filename)

    def test_load(self):
        assert np.any(self.result.grid.cells)
        assert np.any(self.result.grid.points)

    def test_displacement(self):
        nnum, disp = self.result.nodal_solution(0)
        ansys_nnum = np.load(os.path.join(testfiles_path, 'prnsol_u_nnum.npy'))
        ansys_disp = np.load(os.path.join(testfiles_path, 'prnsol_u.npy'))
        assert np.allclose(nnum, ansys_nnum)
        assert np.allclose(disp, ansys_disp, rtol=1E-4)  # rounding in text file

    def test_stress(self):
        ansys_nnum = np.load(os.path.join(testfiles_path, 'prnsol_s_nnum.npy'))
        ansys_stress = np.load(os.path.join(testfiles_path, 'prnsol_s.npy'))
        nnum, stress = self.result.nodal_stress(0)        
        mask = np.in1d(nnum, ansys_nnum)
        assert np.allclose(stress[mask], ansys_stress, atol=1E-6)
