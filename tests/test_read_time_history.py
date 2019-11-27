import os
import numpy as np

import pyansys
import pytest


TEST_PATH = os.path.dirname(os.path.abspath(__file__))
TESTFILES_PATH = os.path.join(TEST_PATH, 'testfiles')
TESTFILE = os.path.join(TESTFILES_PATH, 'time_hist-nsl_acc_vel-component.rst')
RESULT = pyansys.read_binary(TESTFILE)


@pytest.mark.parametrize("time_hist_key", ['NSL', 'VEL', 'ACC'])
def test_time_history(time_hist_key):
    nnum, values = RESULT.nodal_time_history(time_hist_key)
    assert np.allclose(nnum, RESULT.nnum)
    assert values.ndim == 3
    assert values.shape[1] == nnum.size
