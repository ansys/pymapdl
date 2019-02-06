import pytest
import pyansys
from pyansys import examples
from vtki.plotting import running_xserver
import os


@pytest.mark.skipif(not running_xserver(), reason="Requires active X Server")
def test_show_hex_archive():
    examples.show_hex_archive(off_screen=True)


def test_load_result():
    examples.load_result()


@pytest.mark.skipif(not running_xserver(), reason="Requires active X Server")
def test_show_displacement():
    examples.show_displacement(interactive=False)


@pytest.mark.skipif(not running_xserver(), reason="Requires active X Server")
def test_show_stress():
    examples.show_stress(interactive=False)


def test_load_km():
    examples.load_km()


@pytest.mark.skipif(not running_xserver(), reason="Requires active X Server")
def test_show_cell_qual():
    examples.show_cell_qual(meshtype='tet', off_screen=True)
    examples.show_cell_qual(meshtype='hex', off_screen=True)


@pytest.mark.skipif(not running_xserver(), reason="Requires active X Server")
def test_cylinderansys_182():
    exec_file = '/usr/ansys_inc/v182/ansys/bin/ansys182'
    if os.path.isfile(exec_file):
        assert examples.ansys_cylinder_demo(as_test=True)


@pytest.mark.skipif(not running_xserver(), reason="Requires active X Server")
def test_cylinderansys_150():
    exec_file = '/usr/ansys_inc/v150/ansys/bin/ansys150'
    if os.path.isfile(exec_file):
        assert examples.ansys_cylinder_demo(exec_file, as_test=True)
