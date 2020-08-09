"""Test gRPC MAPDL on a local instance"""

import os

import pytest

import pyansys

rver = '202'
if os.name == 'nt':
    ans_root = 'c:/Program Files/ANSYS Inc/'
    MAPDLBIN = os.path.join(ans_root, 'v%s' % rver, 'ansys', 'bin', 'winx64',
                            'ANSYS%s.exe' % rver)
else:
    ans_root = '/usr/ansys_inc'
    MAPDLBIN = os.path.join(ans_root, 'v%s' % rver, 'ansys', 'bin',
                            'ansys%s' % rver)

skip_no_mapdl = pytest.mark.skipif(not os.path.isfile(MAPDLBIN),
                                   reason="Requires MAPDL")

@pytest.fixture(scope='module')
def mapdl():
    if os.name == 'posix':
        os.environ['I_MPI_SHM_LMT'] = 'shm'  # necessary on ubuntu
    return pyansys.launch_mapdl(MAPDLBIN, override=True, cleanup_on_exit=False)


@pytest.fixture(scope='function')
def cleared(mapdl):
    mapdl.finish()
    mapdl.clear()
    mapdl.prep7()
    yield


def test_init(mapdl):
    resp = mapdl.finish()
    assert os.path.isfile(mapdl._lockfile)


@skip_no_mapdl
def test_str(mapdl):
    assert 'ANSYS Mechanical' in str(mapdl)


@skip_no_mapdl
def test_exit(mapdl):
    mapdl.exit()
    assert mapdl._exited
    assert not os.path.isfile(mapdl._lockfile)
