"""Test the mapdl launcher"""

import os
import tempfile
import weakref

import pytest

from ansys.mapdl import core as pymapdl
from ansys.mapdl.core.errors import LicenseServerConnectionError
from ansys.mapdl.core.launcher import (
    _check_license_argument,
    _force_smp_student_version,
    _validate_MPI,
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
from ansys.mapdl.core._version import SUPPORTED_ANSYS_VERSIONS as versions

valid_versions = []
for version in versions:
    exec_file = get_ansys_bin(version)
    if os.path.isfile(get_ansys_bin(version)):
        valid_versions.append(version)

V150_EXEC = get_ansys_bin("150")

paths = [
    ("/usr/dir_v2019.1/slv/ansys_inc/v211/ansys/bin/ansys211", 211),
    ("C:/Program Files/ANSYS Inc/v202/ansys/bin/win64/ANSYS202.exe", 202),
    ("/usr/ansys_inc/v211/ansys/bin/mapdl", 211),
]

skip_on_ci = pytest.mark.skipif(
    os.environ.get("ON_CI", "").upper() == "TRUE", reason="Skipping on CI"
)


@pytest.mark.skipif(
    get_start_instance() is False,
    reason="Skip when start instance is disabled",
)
@pytest.mark.skipif(not valid_versions, reason="Requires MAPDL installed.")
@pytest.mark.skipif(os.name != "nt", reason="Requires Windows")
def test_validate_sw():
    # ensure that windows adds msmpi
    # fake windows path
    exec_path = "C:/Program Files/ANSYS Inc/v211/ansys/bin/win64/ANSYS211.exe"
    add_sw = _validate_MPI("", exec_path)
    assert "msmpi" in add_sw

    add_sw = _validate_MPI("-mpi intelmpi", exec_path)
    assert "msmpi" in add_sw and "intelmpi" not in add_sw


@pytest.mark.skipif(
    get_start_instance() is False,
    reason="Skip when start instance is disabled",
)
@pytest.mark.skipif(not valid_versions, reason="Requires MAPDL installed.")
@pytest.mark.parametrize("path_data", paths)
def test_version_from_path(path_data):
    exec_file, version = path_data
    assert _version_from_path(exec_file) == version


@pytest.mark.skipif(
    get_start_instance() is False,
    reason="Skip when start instance is disabled",
)
@pytest.mark.skipif(not valid_versions, reason="Requires MAPDL installed.")
def test_catch_version_from_path():
    with pytest.raises(RuntimeError):
        _version_from_path("abc")


@pytest.mark.skipif(
    get_start_instance() is False,
    reason="Skip when start instance is disabled",
)
@pytest.mark.skipif(not valid_versions, reason="Requires MAPDL installed.")
@pytest.mark.skipif(os.name != "posix", reason="Requires Linux")
def test_find_ansys_linux():
    # assuming ansys is installed, should be able to find it on linux
    # without env var
    bin_file, ver = pymapdl.launcher.find_ansys()
    assert os.path.isfile(bin_file)
    assert isinstance(ver, float)


@pytest.mark.skipif(
    get_start_instance() is False,
    reason="Skip when start instance is disabled",
)
@pytest.mark.skipif(not valid_versions, reason="Requires MAPDL installed.")
def test_invalid_mode():
    with pytest.raises(ValueError):
        exec_file = get_ansys_bin(valid_versions[0])
        pymapdl.launch_mapdl(exec_file, mode="notamode")


@pytest.mark.skipif(
    get_start_instance() is False,
    reason="Skip when start instance is disabled",
)
@pytest.mark.skipif(not valid_versions, reason="Requires MAPDL installed.")
@pytest.mark.skipif(not os.path.isfile(V150_EXEC), reason="Requires v150")
def test_old_version():
    exec_file = get_ansys_bin("150")
    with pytest.raises(ValueError):
        pymapdl.launch_mapdl(exec_file, mode="corba")


@pytest.mark.skipif(
    get_start_instance() is False,
    reason="Skip when start instance is disabled",
)
@pytest.mark.skipif(not valid_versions, reason="Requires MAPDL installed.")
@pytest.mark.skipif(not os.name == "nt", reason="Requires windows")
@pytest.mark.console
def test_failed_console():
    exec_file = get_ansys_bin(valid_versions[0])
    with pytest.raises(ValueError):
        pymapdl.launch_mapdl(exec_file, mode="console")


@pytest.mark.skipif(
    get_start_instance() is False,
    reason="Skip when start instance is disabled",
)
@pytest.mark.skipif(not valid_versions, reason="Requires MAPDL installed.")
@pytest.mark.parametrize("version", valid_versions)
@pytest.mark.console
@pytest.mark.skipif(os.name != "posix", reason="Only supported on Linux")
def test_launch_console(version):
    exec_file = get_ansys_bin(version)
    mapdl = pymapdl.launch_mapdl(exec_file, mode="console")
    assert mapdl.version == int(version) / 10


@pytest.mark.skipif(
    get_start_instance() is False,
    reason="Skip when start instance is disabled",
)
@pytest.mark.skipif(not valid_versions, reason="Requires MAPDL installed.")
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
    get_start_instance() is False,
    reason="Skip when start instance is disabled",
)
@pytest.mark.skipif(not valid_versions, reason="Requires MAPDL installed.")
def test_license_type_keyword():
    # This test might became a way to check available licenses, which is not the purpose.

    checks = []
    for license_name, license_description in LICENSES.items():
        mapdl = launch_mapdl(license_type=license_name)

        # Using first line to ensure not picking up other stuff.
        checks.append(license_description in mapdl.__str__().split("\n")[0])
        mapdl.exit()

    assert any(checks)


@pytest.mark.skipif(
    get_start_instance() is False,
    reason="Skip when start instance is disabled",
)
@pytest.mark.skipif(not valid_versions, reason="Requires MAPDL installed.")
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
    get_start_instance() is False,
    reason="Skip when start instance is disabled",
)
@pytest.mark.skipif(not valid_versions, reason="Requires MAPDL installed.")
@skip_on_ci
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


@pytest.mark.skipif(
    get_start_instance() is False,
    reason="Skip when start instance is disabled",
)
@pytest.mark.skipif(not valid_versions, reason="Requires MAPDL installed.")
def test_license_type_dummy():
    dummy_license_type = "dummy"
    with pytest.raises(LicenseServerConnectionError):
        launch_mapdl(additional_switches=f" -p {dummy_license_type}")


@pytest.mark.skipif(not valid_versions, reason="Requires MAPDL installed.")
def test_remove_temp_files():
    """Ensure the working directory is removed when run_location is not set."""
    mapdl = launch_mapdl(remove_temp_files=True)

    # possible MAPDL is installed but running in "remote" mode
    path = mapdl.directory
    mapdl.exit()

    tmp_dir = tempfile.gettempdir()
    ans_temp_dir = os.path.join(tmp_dir, "ansys_")
    if path.startswith(ans_temp_dir):
        assert not os.path.isdir(path)
    else:
        assert os.path.isdir(path)


@pytest.mark.flaky(reruns=3, reruns_delay=2)
@pytest.mark.skipif(True, reason="Requires MAPDL installed.")
def test_remove_temp_files_fail(tmpdir):
    """Ensure the working directory is not removed when the cwd is changed."""
    try:
        mapdl = launch_mapdl(remove_temp_files=True)
        old_path = mapdl.directory
        assert os.path.isdir(str(tmpdir))
        mapdl.cwd(str(tmpdir))
        path = mapdl.directory
        mapdl.exit()
        assert os.path.isdir(path)
    finally:
        # ensure no state change
        mapdl.cwd(old_path)


@pytest.mark.skipif(not valid_versions, reason="Requires MAPDL installed.")
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


@pytest.mark.skipif(not valid_versions, reason="Requires MAPDL installed.")
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


@pytest.mark.skipif(not valid_versions, reason="Requires MAPDL installed.")
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


@pytest.mark.requires_gui
def test_open_gui(mapdl):

    mapdl.open_gui()
    mapdl.open_gui(include_result=True)
    mapdl.open_gui(inplace=True)

    mapdl.open_gui(include_result=False)
    mapdl.open_gui(inplace=False)

    mapdl.open_gui(include_result=True, inplace=False)
    mapdl.open_gui(include_result=False, inplace=True)

    mapdl.open_gui(include_result=False, inplace=False)
    mapdl.open_gui(include_result=True, inplace=True)


def test__force_smp_student_version():
    add_sw = ""
    exec_path = (
        r"C:\Program Files\ANSYS Inc\ANSYS Student\v222\ansys\bin\winx64\ANSYS222.exe"
    )
    assert "-smp" in _force_smp_student_version(add_sw, exec_path)

    add_sw = "-mpi"
    exec_path = (
        r"C:\Program Files\ANSYS Inc\ANSYS Student\v222\ansys\bin\winx64\ANSYS222.exe"
    )
    assert "-smp" not in _force_smp_student_version(add_sw, exec_path)

    add_sw = "-dmp"
    exec_path = (
        r"C:\Program Files\ANSYS Inc\ANSYS Student\v222\ansys\bin\winx64\ANSYS222.exe"
    )
    assert "-smp" not in _force_smp_student_version(add_sw, exec_path)

    add_sw = ""
    exec_path = r"C:\Program Files\ANSYS Inc\v222\ansys\bin\winx64\ANSYS222.exe"
    assert "-smp" not in _force_smp_student_version(add_sw, exec_path)

    add_sw = "-smp"
    exec_path = r"C:\Program Files\ANSYS Inc\v222\ansys\bin\winx64\ANSYS222.exe"
    assert "-smp" in _force_smp_student_version(add_sw, exec_path)


@pytest.mark.parametrize(
    "license_short,license_name",
    [[each_key, each_value] for each_key, each_value in LICENSES.items()],
)
def test_license_product_argument(license_short, license_name):
    additional_switches = _check_license_argument(license_name, "qwer")
    assert f"qwer -p {license_short}" in additional_switches


@pytest.mark.parametrize("unvalid_type", [1, {}, ()])
def test_license_product_argument_type_error(unvalid_type):
    with pytest.raises(TypeError):
        _check_license_argument(unvalid_type, "")


def test_license_product_argument_warning():
    with pytest.warns(UserWarning):
        assert "-p asdf" in _check_license_argument("asdf", "qwer")


@pytest.mark.parametrize(
    "license_short,license_name",
    [[each_key, each_value] for each_key, each_value in LICENSES.items()],
)
def test_license_product_argument_p_arg(license_short, license_name):
    assert f"qw1234 -p {license_short}" == _check_license_argument(
        None, f"qw1234 -p {license_short}"
    )


def test_license_product_argument_p_arg_warning():
    with pytest.warns(UserWarning):
        assert "qwer -p asdf" in _check_license_argument(None, "qwer -p asdf")
