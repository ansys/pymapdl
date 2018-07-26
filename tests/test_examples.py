import pytest
import pyansys
from pyansys import examples
from vtkInterface.plotting import RunningXServer

@pytest.mark.skipif(not RunningXServer(), reason="Requires active X Server")
def test_cylinderansys():
    assert examples.CylinderANSYS(as_test=True)  # <-- includes assertions
