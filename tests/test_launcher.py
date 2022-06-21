"""Test the mapdl launcher"""
import os
import weakref

import pytest

from ansys.mapdl import core as pymapdl
from ansys.mapdl.core.launcher import (
    _validate_add_sw,
    _version_from_path,
    get_start_instance,
    is_common_executable_path,
    is_valid_executable_path,
    launch_mapdl,
    save_ansys_path,
    update_env_vars,
    warn_uncommon_executable_path,
)
from ansys.mapdl.core.licensing import LICENSES
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
    "211",  # 2021R1
    "212",  # 2021R2
]

valid_versions = []
for version in versions:
    exec_file = get_ansys_bin(version)
    if os.path.isfile(get_ansys_bin(version)):
        valid_versions.append(version)

V150_EXEC = get_ansys_bin("150")

if not valid_versions:
    pytestmark = pytest.mark.skip("Requires MAPDL")

paths = [
    ("/usr/dir_v2019.1/slv/ansys_inc/v211/ansys/bin/ansys211", 211),
    ("C:/Program Files/ANSYS Inc/v202/ansys/bin/win64/ANSYS202.exe", 202),
    ("/usr/ansys_inc/v211/ansys/bin/mapdl", 211),
]


@pytest.mark.skipif(
    not get_start_instance(), reason="Skip when start instance is disabled"
)
@pytest.mark.skipif(os.name != "nt", reason="Requires Windows")
def test_validate_sw():
    # ensure that windows adds msmpi
    # fake windows path
    exec_path = "C:/Program Files/ANSYS Inc/v211/ansys/bin/win64/ANSYS211.exe"
    add_sw = _validate_add_sw("", exec_path)
    assert "msmpi" in add_sw


@pytest.mark.skipif(
    not get_start_instance(), reason="Skip when start instance is disabled"
)
@pytest.mark.parametrize("path_data", paths)
def test_version_from_path(path_data):
    exec_file, version = path_data
    assert _version_from_path(exec_file) == version


@pytest.mark.skipif(
    not get_start_instance(), reason="Skip when start instance is disabled"
)
def test_catch_version_from_path():
    with pytest.raises(RuntimeError):
        _version_from_path("abc")


@pytest.mark.skipif(
    not get_start_instance(), reason="Skip when start instance is disabled"
)
@pytest.mark.skipif(os.name != "posix", reason="Requires Linux")
@pytest.mark.skipif(not versions, reason="Requires ANSYS install")
def test_find_ansys_linux():
    # assuming ansys is installed, should be able to find it on linux
    # without env var
    bin_file, ver = pymapdl.launcher.find_ansys()
    assert os.path.isfile(bin_file)
    assert isinstance(ver, float)


@pytest.mark.skipif(
    not get_start_instance(), reason="Skip when start instance is disabled"
)
def test_invalid_mode():
    with pytest.raises(ValueError):
        exec_file = get_ansys_bin(valid_versions[0])
        pymapdl.launch_mapdl(exec_file, mode="notamode")


@pytest.mark.skipif(
    not get_start_instance(), reason="Skip when start instance is disabled"
)
@pytest.mark.skipif(not os.path.isfile(V150_EXEC), reason="Requires v150")
def test_old_version():
    exec_file = get_ansys_bin("150")
    with pytest.raises(ValueError):
        pymapdl.launch_mapdl(exec_file, mode="corba")


@pytest.mark.skipif(
    not get_start_instance(), reason="Skip when start instance is disabled"
)
@pytest.mark.skipif(not os.name == "nt", reason="Requires windows")
@pytest.mark.console
def test_failed_console():
    exec_file = get_ansys_bin(valid_versions[0])
    with pytest.raises(ValueError):
        pymapdl.launch_mapdl(exec_file, mode="console")


@pytest.mark.skipif(
    not get_start_instance(), reason="Skip when start instance is disabled"
)
@pytest.mark.parametrize("version", valid_versions)
@pytest.mark.console
@pytest.mark.skipif(os.name != "posix", reason="Only supported on Linux")
def test_launch_console(version):
    exec_file = get_ansys_bin(version)
    mapdl = pymapdl.launch_mapdl(exec_file, mode="console")
    assert mapdl.version == int(version) / 10


@pytest.mark.skipif(
    not get_start_instance(), reason="Skip when start instance is disabled"
)
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


@pytest.mark.skipif(
    not get_start_instance(), reason="Skip when start instance is disabled"
)
def test_license_type_keyword():
    # This test might became a way to check available licenses, which is not the purpose.

    checks = []
    for license_name, license_description in LICENSES.items():
        mapdl = launch_mapdl(license_type=license_name)

        # Using first line to ensure not picking up other stuff.
        checks.append(license_description in mapdl.__str__().split("\n")[0])
        mapdl.exit()

    assert any(checks)

    dummy_license_name = "dummy"
    # I had to scape the parenthesis because the match argument uses regex.
    expected_warn = f"The keyword argument 'license_type' value \('{dummy_license_name}'\) is not a recognized license name or has been deprecated"
    with pytest.warns(UserWarning, match=expected_warn):
        mapdl = launch_mapdl(license_type=dummy_license_name)
        # regardless the license specification, it should lunch.
        assert mapdl.is_alive
    mapdl.exit()


@pytest.mark.skipif(
    not get_start_instance(), reason="Skip when start instance is disabled"
)
def test_license_type_keyword_names():
    # This test might became a way to check available licenses, which is not the purpose.

    successful_check = False
    for license_name, license_description in LICENSES.items():
        mapdl = launch_mapdl(license_type=license_name)

        # Using first line to ensure not picking up other stuff.
        successful_check = (
            license_description in mapdl.__str__().split("\n")[0] or successful_check
        )
        assert license_description in mapdl.__str__().split("\n")[0]
        mapdl.exit()

    assert successful_check  # if at least one license is ok, this should be true.


@pytest.mark.skipif(
    not get_start_instance(), reason="Skip when start instance is disabled"
)
def test_license_type_additional_switch():
    # This test might became a way to check available licenses, which is not the purpose.
    successful_check = False
    for license_name, license_description in LICENSES.items():
        mapdl = launch_mapdl(additional_switches=" -p" + license_name)

        # Using first line to ensure not picking up other stuff.
        successful_check = (
            license_description in mapdl.__str__().split("\n")[0] or successful_check
        )
        mapdl.exit()

    assert successful_check  # if at least one license is ok, this should be true.

    dummy_license_name = "dummy"
    # I had to scape the parenthesis because the match argument uses regex.
    expected_warn = f"The additional switch product value \('-p {dummy_license_name}'\) is not a recognized license name or has been deprecated"
    with pytest.warns(UserWarning, match=expected_warn):
        mapdl = launch_mapdl(additional_switches=f" -p {dummy_license_name}")
        # regardless the license specification, it should lunch.
        assert mapdl.is_alive
    mapdl.exit()


@pytest.mark.parametrize(
    "exe_loc",
    [
        pytest.param(None, id="Normal execution. Return path"),
    ],
)
def test_save_ansys_path(exe_loc):
    path_ = save_ansys_path(exe_loc)

    assert isinstance(path_, str)
    assert os.path.exists(path_)


@pytest.mark.parametrize(
    "file,result",
    [
        ("ansys221", True),
        ("ansy212", False),
        ("ansys22", False),
        ("ansys", False),
        ("ger123", False),
    ],
)
def test_is_valid_executable_path(tmpdir, file, result):
    filename = str(tmpdir.mkdir("tmpdir").join(file))

    with open(filename, "w") as fid:
        fid.write("")

    assert is_valid_executable_path(filename) == result


@pytest.mark.parametrize(
    "file_path,result",
    [
        pytest.param(
            "random/v221/ansys/bin/ansys221", True, id="Normal successful case."
        ),
        pytest.param("random/random/ansys/bin/ans221", False, id="No vXXX directory"),
        pytest.param("random/v221/random/bin/ans221", False, id="No ansys directory"),
        pytest.param("random/v221/ansys/random/ans221", False, id="No bin directory"),
        pytest.param(
            "random/v221/ansys/bin/ansys22", False, id="version number incomplete"
        ),
        pytest.param("random/v221/ansys/bin/ansys222", False, id="Different version"),
    ],
)
def test_is_common_executable_path(tmpdir, file_path, result):
    path = os.path.normpath(file_path)
    path = path.split(os.sep)

    filename = str(
        tmpdir.mkdir(path[0]).mkdir(path[1]).mkdir(path[2]).mkdir(path[3]).join(path[4])
    )

    with open(filename, "w") as fid:
        fid.write("")

    assert is_common_executable_path(filename) == result


def test_warn_uncommon_executable_path():
    with pytest.warns(
        UserWarning, match="does not match the usual ansys executable path style"
    ):
        warn_uncommon_executable_path("")


def test_env_injection():

    assert update_env_vars(None, None) is None

    assert "myenvvar" in update_env_vars({"myenvvar": "True"}, None)

    _env_vars = update_env_vars(None, {"myenvvar": "True"})
    assert len(_env_vars) == 1
    assert "myenvvar" in _env_vars

    with pytest.raises(ValueError):
        update_env_vars({"myenvvar": "True"}, {"myenvvar": "True"})

    with pytest.raises(TypeError):
        update_env_vars("asdf", None)

    with pytest.raises(TypeError):
        update_env_vars(None, "asdf")
