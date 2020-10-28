"""Test the mapdl launcher"""
import weakref
import socket
import os
import pytest

import pyansys
from pyansys.misc import get_ansys_bin

# using CORBA available versions
versions = ['182',
            '190',  # 19.0
            '191',  # 19.1
            '192',  # 19.2
            '193',  # 2019R1
            '194',  # 2019R2
            '195',  # 2019R3
            '201',  # 2020R1
            '202']  # 2020R2
valid_versions = []
for version in versions:
    exec_file = get_ansys_bin(version)
    if os.path.isfile(get_ansys_bin(version)):
        valid_versions.append(version)

V150_EXEC = get_ansys_bin('150')


if not valid_versions:
    pytestmark = pytest.mark.skip("Requires MAPDL")


@pytest.mark.skipif(os.name != 'posix', reason="Requires Linux")
@pytest.mark.skipif(not versions, reason="Requires ANSYS install")
def test_find_ansys_linux():
    # assuming ansys is installed, should be able to find it on linux
    # without env var
    bin_file, ver = pyansys.launcher.find_ansys()
    assert os.path.isfile(bin_file)
    assert isinstance(ver, float)


def test_invalid_mode():
    with pytest.raises(ValueError):
        exec_file = get_ansys_bin(valid_versions[0])
        pyansys.launch_mapdl(exec_file, override=True, mode='notamode')


@pytest.mark.skipif(not os.path.isfile(V150_EXEC), reason="Requires v150")
def test_old_version():
    exec_file = get_ansys_bin('150')
    with pytest.raises(ValueError):
        pyansys.launch_mapdl(exec_file, override=True, mode='corba')


@pytest.mark.skipif(not os.name=='nt', reason="Requires windows")
def test_failed_console():
    exec_file = get_ansys_bin(valid_versions[0])
    with pytest.raises(ValueError):
        pyansys.launch_mapdl(exec_file, override=True, mode='console')


@pytest.mark.parametrize('version', valid_versions)
@pytest.mark.skipif(os.name != 'posix', reason="Only supported on Linux")
def test_launch_pexpect(version):
    exec_file = get_ansys_bin(version)
    mapdl = pyansys.launch_mapdl(exec_file, override=True, mode='console')
    assert mapdl.version == int(version)/10


@pytest.mark.parametrize('version', valid_versions)
def test_launch_corba(version):
    exec_file = get_ansys_bin(version)

    # configure shared memory parallel for VM
    additional_switches = ''
    if os.name == 'nt' and socket.gethostname() == 'WIN-FRDMRVG7QAB':
        additional_switches = '-smp'
    elif os.name == 'posix':
        os.environ['I_MPI_SHM_LMT'] = 'shm'  # necessary on ubuntu and dmp

    mapdl = pyansys.launch_mapdl(exec_file, override=True, mode='corba',
                                 additional_switches=additional_switches)
    assert mapdl.version == int(version)/10
    # mapdl.exit() # exit is already tested for in test_mapdl.py.
    # Instead, test collection

    mapdl_ref = weakref.ref(mapdl)
    del mapdl
    assert mapdl_ref() is None
