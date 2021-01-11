import pytest
import numpy as np
from ansys.mapdl.core import examples

try:
    result = examples.downloads._download_solid239_240()
except:
    result = None


@pytest.mark.skipif(result is None, reason="Requires example files")
def test_load():
    assert np.any(result.grid.cells)
    assert np.any(result.grid.points)
