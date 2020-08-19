import os

import pyvista
import pytest

import pyansys
from pyansys.misc import get_ansys_bin

# ensure pyvista always plots off_screen
pyvista.OFF_SCREEN = True


@pytest.fixture(scope="module", params=['console', 'corba'])
def mapdl(request):
    os.environ['I_MPI_SHM_LMT'] = 'shm'  # necessary on ubuntu

    mode = request.param
    rver = '202'
    mapdl = pyansys.launch_mapdl(get_ansys_bin(rver), override=True, mode=mode)
    mapdl._show_matplotlib_figures = False
    return mapdl


@pytest.fixture(scope='function')
def cleared(mapdl):
    mapdl.finish()
    mapdl.clear('NOSTART')  # *MUST* be NOSTART.  With START fails after 20 calls...
    mapdl.prep7()
    yield
