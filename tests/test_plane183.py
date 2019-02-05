"""
Test loading results from plane183

Need to add ansys results for verification...

"""
import os
import numpy as np
import pyansys

test_path = os.path.dirname(os.path.abspath(__file__))
testfiles_path = os.path.join(test_path, 'testfiles')


class TestLoad183():
    filename = os.path.join(testfiles_path, 'plane183.rst')
    result = pyansys.ResultReader(filename)

    def test_load(self):
        assert np.any(self.result.grid.cells)
        assert np.any(self.result.grid.points)

    # def test_displacement():
        
