import shutil
import os

import numpy as np
import pytest
from pyvista.plotting.renderer import CameraPosition

import pyansys


@pytest.fixture(scope='module')
def thermal_solution(mapdl):
    mapdl.clear()

    # create a simple beam and impose some thermal conditions on it
    mapdl.prep7()
    mapdl.mp('kxx', 1, 45)
    mapdl.et(1, 90)
    mapdl.block(-0.3, 0.3, -0.46, 1.34, -0.2, -0.2 + 0.02)
    mapdl.vsweep(1)
    # mapdl.eplot()
    mapdl.finish()
    mapdl.run('/SOLU')
    mapdl.asel('S', vmin=3)
    mapdl.nsla()
    mapdl.d('all', 'temp', 5)
    mapdl.asel('S', vmin=4)
    mapdl.nsla()
    mapdl.d('all', 'temp', 100)
    mapdl.allsel()

    mapdl.solve()
    mapdl.finish()
    mapdl.post1()
    mapdl.set(1, 1)


def test_not_all_found(thermal_solution, mapdl, tmpdir):
    filename = os.path.join(mapdl.path, 'file0.rth')

    tmp_file = os.path.join(mapdl.path, 'tmp0.rth')
    shutil.copy(filename, tmp_file)
    with pytest.raises(FileNotFoundError):
        dist_rst = pyansys.read_binary(tmp_file)


def test_temperature(thermal_solution, mapdl, tmpdir):
    ans_temp = mapdl.post_processing.nodal_temperature

    dist_rst = pyansys.read_binary(os.path.join(mapdl.path, 'file0.rth'))

    # normal result should match
    rst = mapdl.result  # normally not distributed
    nnum, rst_temp = rst.nodal_temperature(0)
    assert np.allclose(rst_temp, ans_temp)

    # distributed result should match
    dist_nnum, dist_temp = dist_rst.nodal_temperature(0)
    assert np.allclose(dist_temp, ans_temp)


def test_plot_temperature(thermal_solution, mapdl):
    dist_rst = pyansys.read_binary(os.path.join(mapdl.path, 'file0.rth'))
    cpos = dist_rst.plot_nodal_temperature(0)
    assert isinstance(cpos, CameraPosition)
