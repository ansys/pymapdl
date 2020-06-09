import glob
import os

import pytest
import numpy as np
import pyansys
from pyansys.mapdl_console import MapdlConsole

path = os.path.dirname(os.path.abspath(__file__))

LINUX = os.name == 'posix'
rver = '194'
ans_root = '/usr/ansys_inc'
MAPDLBIN = os.path.join(ans_root, 'v%s' % rver, 'ansys', 'bin', 'ansys%s' % rver)

if 'PYANSYS_IGNORE_ANSYS' in os.environ:
    HAS_ANSYS = False
else:
    HAS_ANSYS = os.path.isfile(MAPDLBIN)


RSETS = list(zip(range(1, 9), [1]*8))

@pytest.fixture(scope='module')
def mapdl():
    mapdl_instance = pyansys.launch_mapdl(MAPDLBIN,
                                          override=True,
                                          additional_switches='-smp',  # for Linux
                                          prefer_pexpect=True)
    assert isinstance(mapdl_instance, MapdlConsole)
    return mapdl_instance


@pytest.mark.skipif(not HAS_ANSYS, reason="Requires ANSYS installed")
@pytest.mark.skipif(not LINUX, reason="ConsoleMapdl requires linux")
def test_COM(mapdl):
    comment = 'COMMENT'
    resp = mapdl.run('/COM,%s' % comment)
    assert comment in resp
    resp_func = mapdl.com(comment)
    assert resp_func == resp


@pytest.mark.skipif(not HAS_ANSYS, reason="Requires ANSYS installed")
@pytest.mark.skipif(not LINUX, reason="ConsoleMapdl requires linux")
def test_clear(mapdl):
    mapdl.prep7()
    assert mapdl.processor == 'PREP7'
    mapdl.clear()
    assert 'BEGIN' in mapdl.processor


def test_logging(mapdl, tmpdir):
    filename = str(tmpdir.mkdir("tmpdir").join('tmp.inp'))
    with pytest.raises(RuntimeError):
        mapdl.open_apdl_log(filename, mode='w')

    mapdl.prep7()
    mapdl.k(1, 0, 0, 0)
    mapdl.k(2, 1, 0, 0)
    mapdl.k(3, 1, 1, 0)
    mapdl.k(4, 0, 1, 0)

    mapdl._apdl_log.flush()

    out = open(mapdl._apdl_log.name).read().strip().split()[-5:]
    assert 'PREP7' in out[0]
    assert 'K,4,0,1,0' in out[-1]


@pytest.mark.skipif(not HAS_ANSYS, reason="Requires ANSYS installed")
@pytest.mark.skipif(not LINUX, reason="ConsoleMapdl requires linux")
def test_exit(mapdl):
    mapdl.exit()
    with pytest.raises(RuntimeError):
        mapdl.prep7()
    assert not os.path.isfile(mapdl._lockfile)
