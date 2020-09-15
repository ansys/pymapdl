import socket
import os
from pyansys.misc import get_ansys_bin
import pyansys

import pytest
import pyvista
pyvista.OFF_SCREEN = True

# check for a valid MAPDL install with CORBA
valid_rver = ['182', '190', '191', '192', '193', '194', '195', '201']
EXEC_FILE = None
for rver in valid_rver:
    if os.path.isfile(get_ansys_bin(rver)):
        EXEC_FILE = get_ansys_bin(rver)

if 'PYANSYS_IGNORE_ANSYS' in os.environ:
    HAS_ANSYS = False
else:
    HAS_ANSYS = EXEC_FILE is not None


skip_no_ansys = pytest.mark.skipif(not HAS_ANSYS, reason="Requires ANSYS installed")



@pytest.fixture(scope="session")
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

    return mapdl
