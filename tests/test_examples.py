import os

import pytest
import pyansys
from pyansys import examples
from pyvista.plotting import system_supports_plotting

try:
    shaft = pyansys.download_shaft_modal()
except:
    shaft = None


@pytest.mark.skipif(not system_supports_plotting(), reason="Requires active X Server")
def test_show_hex_archive():
    examples.show_hex_archive(off_screen=True)


def test_load_result():
    examples.load_result()


@pytest.mark.skipif(not system_supports_plotting(), reason="Requires active X Server")
def test_show_displacement():
    examples.show_displacement(off_screen=True)


@pytest.mark.skipif(not system_supports_plotting(), reason="Requires active X Server")
def test_show_stress():
    examples.show_stress(off_screen=True)


def test_load_km():
    examples.load_km()


@pytest.mark.skipif(not system_supports_plotting(), reason="Requires active X Server")
def test_show_cell_qual():
    examples.show_cell_qual(meshtype='tet', off_screen=True)
    examples.show_cell_qual(meshtype='hex', off_screen=True)


@pytest.mark.skipif(not system_supports_plotting(), reason="Requires active X Server")
def test_cylinderansys_182():
    exec_file = '/usr/ansys_inc/v182/ansys/bin/ansys182'
    if os.path.isfile(exec_file):
        assert examples.ansys_cylinder_demo(as_test=True)


@pytest.mark.skipif(not system_supports_plotting(), reason="Requires active X Server")
def test_cylinderansys_150():
    exec_file = '/usr/ansys_inc/v150/ansys/bin/ansys150'
    if os.path.isfile(exec_file):
        assert examples.ansys_cylinder_demo(exec_file, as_test=True)


@pytest.mark.skipif(not system_supports_plotting(), reason="Requires active X Server")
@pytest.mark.skipif(shaft is None, reason="Requires example file")
def test_shaft_animate(tmpdir):
    filename = str(tmpdir.mkdir("tmpdir").join('tmp.mp4'))
    shaft.animate_nodal_solution(5, node_components='SHAFT_MESH',
                                 max_disp=10, comp='norm',
                                 show_edges=True, off_screen=True,
                                 movie_filename=filename)


@pytest.mark.skipif(not system_supports_plotting(), reason="Requires active X Server")
def test_shaft_plot_screenshot(tmpdir):
    filename = str(tmpdir.mkdir("tmpdir").join('tmp.png'))
    shaft.plot_nodal_solution(0, off_screen=True, screenshot=filename)
    assert os.path.isfile(filename)
