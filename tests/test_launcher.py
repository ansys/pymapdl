"""Test the mapdl launcher"""
import os
import weakref

import pytest
from ansys.mapdl import core as pymapdl
from ansys.mapdl.core.launcher import _version_from_path, get_start_instance
from ansys.mapdl.core.misc import get_ansys_bin

try:
    import ansys_corba  # noqa: F401
    HAS_CORBA = True
except:
    HAS_CORBA = False

# CORBA and console available versions
versions = [
    "170",  # 17.0
    "182",  # 18.2
    "182",  # 18.2
    "190",  # 19.0
    "191",  # 19.1
    "192",  # 19.2
    "193",  # 2019R1
    "194",  # 2019R2
    "195",  # 2019R3
    "201",  # 2020R1
    "202",  # 2020R2
]

valid_versions = []
for version in versions:
    exec_file = get_ansys_bin(version)
    if os.path.isfile(get_ansys_bin(version)):
        valid_versions.append(version)

V150_EXEC = get_ansys_bin("150")

# skip entire module when using static server
if not get_start_instance():
    pytest.skip("Skip when start instance is disabled", allow_module_level=True)

if not valid_versions:
    pytestmark = pytest.mark.skip("Requires MAPDL")

paths = [
    ("/usr/dir_v2019.1/slv/ansys_inc/v211/ansys/bin/ansys211", 211),
    ("C:/Program Files/ANSYS Inc/v202\\ansys/bin/win64/ANSYS202.exe", 202),
    ("/usr/ansys_inc/v211/ansys/bin/mapdl", 211),
]


@pytest.mark.parametrize("path_data", paths)
def test_version_from_path(path_data):
    exec_file, version = path_data
    assert _version_from_path(exec_file) == version


def test_catch_version_from_path():
    with pytest.raises(RuntimeError):
        _version_from_path("abc")


@pytest.mark.skipif(os.name != "posix", reason="Requires Linux")
@pytest.mark.skipif(not versions, reason="Requires ANSYS install")
def test_find_ansys_linux():
    # assuming ansys is installed, should be able to find it on linux
    # without env var
    bin_file, ver = pymapdl.launcher.find_ansys()
    assert os.path.isfile(bin_file)
    assert isinstance(ver, float)


def test_invalid_mode():
    with pytest.raises(ValueError):
        exec_file = get_ansys_bin(valid_versions[0])
        pymapdl.launch_mapdl(exec_file, mode="notamode")


@pytest.mark.skipif(not os.path.isfile(V150_EXEC), reason="Requires v150")
def test_old_version():
    exec_file = get_ansys_bin("150")
    with pytest.raises(ValueError):
        pymapdl.launch_mapdl(exec_file, mode="corba")


@pytest.mark.skipif(not os.name == "nt", reason="Requires windows")
@pytest.mark.console
def test_failed_console():
    exec_file = get_ansys_bin(valid_versions[0])
    with pytest.raises(ValueError):
        pymapdl.launch_mapdl(exec_file, mode="console")


@pytest.mark.parametrize("version", valid_versions)
@pytest.mark.console
@pytest.mark.skipif(os.name != "posix", reason="Only supported on Linux")
def test_launch_console(version):
    exec_file = get_ansys_bin(version)
    mapdl = pymapdl.launch_mapdl(exec_file, mode="console")
    assert mapdl.version == int(version) / 10


@pytest.mark.corba
@pytest.mark.parametrize("version", valid_versions)
def test_launch_corba(version):
    mapdl = pymapdl.launch_mapdl(get_ansys_bin(version), mode="corba")
    assert mapdl.version == int(version) / 10
    # mapdl.exit() # exit is already tested for in test_mapdl.py.
    # Instead, test collection

    mapdl_ref = weakref.ref(mapdl)
    del mapdl
    assert mapdl_ref() is None
