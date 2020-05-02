import os
import numpy as np

import pyansys
import pytest


@pytest.fixture(scope='module')
def result():
    test_path = os.path.dirname(os.path.abspath(__file__))
    testfiles_path = os.path.join(test_path, 'testfiles')
    testfile = os.path.join(testfiles_path, 'time_hist-nsl_acc_vel-component.rst')
    return pyansys.read_binary(testfile)


@pytest.mark.parametrize("time_hist_key", ['NSL', 'VEL', 'ACC'])
def test_time_history(time_hist_key, result):
    nnum, values = result.nodal_time_history(time_hist_key)
    assert np.allclose(nnum, result.nnum)
    assert values.ndim == 3
    assert values.shape[1] == nnum.size
