import os
import pytest
import pyansys
from pyansys.examples import sector_result_file, rstfile

from vtki.plotting import running_xserver

def test_non_cyclic():
    with pytest.raises(Exception):
        pyansys.CyclicResult(rstfile)


result = pyansys.ResultReader(sector_result_file)
def test_is_cyclic():
    assert hasattr(result, 'rotor')


@pytest.mark.skipif(not running_xserver(), reason="Requires active X Server")
def test_animate_nodal_solution(tmpdir):
    temp_movie = str(tmpdir.mkdir("tmpdir").join('tmp.mp4'))
    result.animate_nodal_solution(0, nangles=20, movie_filename=temp_movie,
                                interactive=False)
    assert os.path.isfile(temp_movie)

