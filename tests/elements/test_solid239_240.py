"""

"""
import os

import pytest
import numpy as np
import pyansys
from pyansys import examples


@pytest.fixture(scope='module')
def result():
    return pyansys.examples.downloads._download_solid239_240()


def test_load(result):
    assert np.any(result.grid.cells)
    assert np.any(result.grid.points)
