import os

import pytest
import numpy as np
import pyansys
from pyansys import examples


try:
    result = pyansys.examples.downloads._download_solid239_240()
except:
    result = None

@pytest.mark.skipif(result is None, reason="Requires example files")
def test_load(result):
    assert np.any(result.grid.cells)
    assert np.any(result.grid.points)
