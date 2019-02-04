import os

import pytest
import numpy as np

import pyansys
from pyansys.examples import hexarchivefile
from pyansys.examples import rstfile
from pyansys.examples import fullfile
from vtki.plotting import running_xserver

test_path = os.path.dirname(os.path.abspath(__file__))
testfiles_path = os.path.join(test_path, 'testfiles')


def test_loadresult():
    result = pyansys.ResultReader(rstfile)

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


@pytest.mark.skipif(not running_xserver(), reason="Requires active X Server")
def test_animate_nodal_solution(tmpdir):
    result = pyansys.ResultReader(rstfile)
    temp_movie = str(tmpdir.mkdir("tmpdir").join('tmp.mp4'))
    result.animate_nodal_solution(0, nangles=20, movie_filename=temp_movie,
                                interactive=False)
    assert np.any(result.grid.points)
    assert os.path.isfile(temp_movie)
    

def test_loadbeam():
    linkresult = os.path.join(testfiles_path, 'link1.rst')
    result = pyansys.ResultReader(linkresult)
    assert np.any(result.grid.cells)


def test_fullreader():
    fobj = pyansys.FullReader(fullfile)
    dofref, k, m = fobj.load_km()
    assert dofref.size
    assert k.size
    assert m.size

