import pytest
import pyansys
from pyansys import examples
from vtkInterface.plotting import RunningXServer
import os

@pytest.mark.skipif(not RunningXServer(), reason="Requires active X Server")
def test_cylinderansys_182():
    exec_file = '/usr/ansys_inc/v182/ansys/bin/ansys182'
    if os.path.isfile(exec_file):
        assert examples.CylinderANSYS(as_test=True)


@pytest.mark.skipif(not RunningXServer(), reason="Requires active X Server")
def test_cylinderansys_150():
    exec_file = '/usr/ansys_inc/v150/ansys/bin/ansys150'
    if os.path.isfile(exec_file):
        assert examples.CylinderANSYS(exec_file, as_test=True)
