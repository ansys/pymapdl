import os

import pytest
import numpy as np

import pyansys
from pyansys.examples import rstfile
from pyvista.plotting import system_supports_plotting


test_path = os.path.dirname(os.path.abspath(__file__))
testfiles_path = os.path.join(test_path, 'testfiles')


HAS_FFMPEG = True
try:
    import imageio_ffmpeg
except ImportError:
    HAS_FFMPEG = False


@pytest.fixture(scope='module')
def result():
    return pyansys.read_binary(rstfile)


def test_loadresult(result):
    # check result is loaded
    assert result.nsets
    assert result.nnum.size

    # check geometry is genreated
    grid = result.grid
    assert grid.points.size
    assert grid.cells.size
    assert 'ansys_node_num' in grid.point_arrays

    # check results can be loaded
    nnum, disp = result.nodal_solution(0)
    assert nnum.size
    assert disp.size

    nnum, disp = result.nodal_solution(0)
    assert nnum.size
    assert disp.size

    nnum, disp = result.principal_nodal_stress(0)
    assert nnum.size
    assert disp.size

    nnum, disp = result.nodal_stress(0)
    assert nnum.size
    assert disp.size

    element_stress, enum, enode = result.element_stress(0)
    assert element_stress[0].size
    assert enum.size
    assert enode[0].size

    element_stress, enum, enode = result.element_stress(0, principal=True)
    assert element_stress[0].size
    assert enum.size
    assert enode[0].size


@pytest.mark.skipif(not system_supports_plotting(), reason="Requires active X Server")
@pytest.mark.skipif(not HAS_FFMPEG, reason="requires imageio_ffmpeg")
def test_animate_nodal_solution(tmpdir, result):
    temp_movie = str(tmpdir.mkdir("tmpdir").join('tmp.mp4'))
    result.animate_nodal_solution(0, nangles=20, movie_filename=temp_movie,
                                  off_screen=True)
    assert np.any(result.grid.points)
    assert os.path.isfile(temp_movie)


def test_loadbeam():
    linkresult_path = os.path.join(testfiles_path, 'link1.rst')
    linkresult = pyansys.read_binary(linkresult_path)
    assert np.any(linkresult.grid.cells)
