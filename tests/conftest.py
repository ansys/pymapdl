import os

import pyansys
import pyvista
import pytest

# ensure pyvista always plots off_screen
pyvista.OFF_SCREEN = True


def get_ansys_bin(rver):
    if os.name == 'nt':
        ans_root = 'c:/Program Files/ANSYS Inc/'
        mapdlbin = os.path.join(ans_root, 'v%s' % rver, 'ansys', 'bin', 'winx64',
                                'ANSYS%s.exe' % rver)
    else:
        ans_root = '/usr/ansys_inc'
        mapdlbin = os.path.join(ans_root, 'v%s' % rver, 'ansys', 'bin',
                                'ansys%s' % rver)

    return mapdlbin


@pytest.fixture(scope="module", params=['console', 'corba'])
def mapdl(request):
    os.environ['I_MPI_SHM_LMT'] = 'shm'  # necessary on ubuntu

    mode = request.param
    if mode == 'corba':
        # v200 and newer don't work
        # v194 has issues exiting
        rver = '182'
    else:
        rver = '202'

    # if mode == 'grpc':
    #     from pyansys.mapdl_grpc import MapdlGrpc
    #     mapdl = MapdlGrpc(cleanup_on_exit=False)
    # else:
    mapdl = pyansys.launch_mapdl(get_ansys_bin(rver), override=True, mode=mode)
    mapdl._show_matplotlib_figures = False
    return mapdl


@pytest.fixture(scope='function')
def cleared(mapdl):
    mapdl.finish()
    mapdl.clear('NOSTART')  # *MUST* be NOSTART.  With START fails after 20 calls...
    mapdl.prep7()
    yield
