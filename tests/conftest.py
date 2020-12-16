import socket
import os

import pytest
import pyvista

from pyansys.misc import get_ansys_bin
import pyansys
from pyansys.errors import MapdlExitedError


pyvista.OFF_SCREEN = True

# check for a valid MAPDL install with CORBA
valid_rver = ['202', '201', '195', '194', '193', '192', '191', '190', '182']
EXEC_FILE = None
for rver in valid_rver:
    if os.path.isfile(get_ansys_bin(rver)):
        EXEC_FILE = get_ansys_bin(rver)
        break

if 'PYANSYS_IGNORE_ANSYS' in os.environ:
    HAS_ANSYS = False
else:
    HAS_ANSYS = EXEC_FILE is not None


skip_no_ansys = pytest.mark.skipif(not HAS_ANSYS, reason="Requires ANSYS installed")


modes = ['corba']
# if os.name == 'posix':  # console only for linux
#     modes.append('console')


collect_ignore = []
if not HAS_ANSYS:
    collect_ignore.append("test_post.py")


@pytest.fixture(scope="session", params=modes)
def mapdl():

    # launch in shared memory parallel for Windows VM
    # configure shared memory parallel for VM
    additional_switches = ''
    if os.name == 'nt' and socket.gethostname() == 'WIN-FRDMRVG7QAB':
        additional_switches = '-smp'
    elif os.name == 'posix':
        os.environ['I_MPI_SHM_LMT'] = 'shm'  # necessary on ubuntu and dmp

    mapdl = pyansys.launch_mapdl(EXEC_FILE, override=True, mode='corba',
                                 additional_switches=additional_switches)
    mapdl._show_matplotlib_figures = False  # don't show matplotlib figures
    yield mapdl

    ### test exit ###
    # must be after yield as this uses a module scoped fixture
    mapdl.exit()
    assert mapdl._exited
    with pytest.raises(RuntimeError):
        mapdl.prep7()

    assert not os.path.isfile(mapdl._lockfile)
    assert 'MAPDL exited' in str(mapdl)

    with pytest.raises(MapdlExitedError):
        mapdl.prep7()
