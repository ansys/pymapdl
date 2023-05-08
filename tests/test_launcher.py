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
    _is_ubuntu,
    _validate_MPI,
    _verify_version,
    find_ansys,
    get_default_ansys,
    get_start_instance,
    launch_mapdl,
    update_env_vars,
    version_from_path,
)
from ansys.mapdl.core.licensing import LICENSES

try:
    import ansys_corba  # noqa: F401

    HAS_CORBA = True
except:
    HAS_CORBA = False

# CORBA and console available versions
from ansys.tools.path import get_available_ansys_installations

from ansys.mapdl.core._version import SUPPORTED_ANSYS_VERSIONS as versions

valid_versions = list(get_available_ansys_installations().keys())

try:
    V150_EXEC = find_ansys("150")[0]
except ValueError:
    V150_EXEC = ""

paths = [
    ("/usr/dir_v2019.1/slv/ansys_inc/v211/ansys/bin/ansys211", 211),
    ("C:/Program Files/ANSYS Inc/v202/ansys/bin/win64/ANSYS202.exe", 202),
    ("/usr/ansys_inc/v211/ansys/bin/mapdl", 211),
]

skip_on_ci = pytest.mark.skipif(
    os.environ.get("ON_CI", "").upper() == "TRUE", reason="Skipping on CI"
)

skip_on_not_local = pytest.mark.skipif(
    not os.environ.get("RUN_LOCAL", "").upper() == "TRUE",
    reason="Skipping because not on local",
)

start_timeout = 30  # Seconds


@pytest.fixture
def fake_local_mapdl(mapdl):
    """Fixture to execute asserts before and after a test is run"""
    # Setup: fill with any logic you want
    mapdl._local = True

    yield True  # this is where the testing happens

    # Teardown : fill with any logic you want
    mapdl._local = False


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
    assert version_from_path("mapdl", exec_file) == version


@pytest.mark.skipif(
    get_start_instance() is False,
    reason="Skip when start instance is disabled",
)
@pytest.mark.skipif(not valid_versions, reason="Requires MAPDL installed.")
def test_catch_version_from_path():
    with pytest.raises(RuntimeError):
        version_from_path("mapdl", "abc")


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
        exec_file = find_ansys(valid_versions[0])[0]
        pymapdl.launch_mapdl(exec_file, mode="notamode", start_timeout=start_timeout)


@pytest.mark.skipif(
    get_start_instance() is False,
    reason="Skip when start instance is disabled",
)
@pytest.mark.skipif(not valid_versions, reason="Requires MAPDL installed.")
@pytest.mark.skipif(not os.path.isfile(V150_EXEC), reason="Requires v150")
def test_old_version():
    exec_file = find_ansys("150")[0]
    with pytest.raises(ValueError):
        pymapdl.launch_mapdl(exec_file, mode="corba", start_timeout=start_timeout)


@pytest.mark.skipif(
    get_start_instance() is False,
    reason="Skip when start instance is disabled",
)
@pytest.mark.skipif(not valid_versions, reason="Requires MAPDL installed.")
@pytest.mark.skipif(not os.name == "nt", reason="Requires windows")
@pytest.mark.console
def test_failed_console():
    exec_file = find_ansys(valid_versions[0])[0]
    with pytest.raises(ValueError):
        pymapdl.launch_mapdl(exec_file, mode="console", start_timeout=start_timeout)


@pytest.mark.skipif(
    get_start_instance() is False,
    reason="Skip when start instance is disabled",
)
@pytest.mark.skipif(not valid_versions, reason="Requires MAPDL installed.")
@pytest.mark.parametrize("version", valid_versions)
@pytest.mark.console
@pytest.mark.skipif(os.name != "posix", reason="Only supported on Linux")
def test_launch_console(version):
    exec_file = find_ansys(version)[0]
    mapdl = pymapdl.launch_mapdl(exec_file, mode="console", start_timeout=start_timeout)
    assert mapdl.version == int(version) / 10


@pytest.mark.skipif(
    get_start_instance() is False,
    reason="Skip when start instance is disabled",
)
@pytest.mark.skipif(not valid_versions, reason="Requires MAPDL installed.")
@pytest.mark.corba
@pytest.mark.parametrize("version", valid_versions)
def test_launch_corba(version):
    mapdl = pymapdl.launch_mapdl(
        find_ansys(version)[0], mode="corba", start_timeout=start_timeout
    )
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
    checks = []
    for license_name, license_description in LICENSES.items():
        mapdl = launch_mapdl(license_type=license_name, start_timeout=start_timeout)

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
        mapdl = launch_mapdl(license_type=license_name, start_timeout=start_timeout)

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
def test_license_type_additional_switch():
    # This test might became a way to check available licenses, which is not the purpose.
    successful_check = False
    for license_name, license_description in LICENSES.items():
        mapdl = launch_mapdl(
            additional_switches=" -p " + license_name, start_timeout=start_timeout
        )

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
        launch_mapdl(
            additional_switches=f" -p {dummy_license_type}", start_timeout=start_timeout
        )


@pytest.mark.skipif(not valid_versions, reason="Requires MAPDL installed.")
@skip_on_not_local
def test_remove_temp_files():
    """Ensure the working directory is removed when run_location is not set."""
    mapdl = launch_mapdl(remove_temp_files=True, start_timeout=start_timeout)

    # possible MAPDL is installed but running in "remote" mode
    path = mapdl.directory
    mapdl.exit()

    tmp_dir = tempfile.gettempdir()
    ans_temp_dir = os.path.join(tmp_dir, "ansys_")
    if path.startswith(ans_temp_dir):
        assert not os.path.isdir(path)
    else:
        assert os.path.isdir(path)


@skip_on_not_local
def test_remove_temp_files_fail(tmpdir):
    """Ensure the working directory is not removed when the cwd is changed."""
    mapdl = launch_mapdl(remove_temp_files=True, start_timeout=start_timeout)
    old_path = mapdl.directory
    assert os.path.isdir(str(tmpdir))
    mapdl.cwd(str(tmpdir))
    path = mapdl.directory
    mapdl.exit()
    assert os.path.isdir(path)

    # Checking no changes in the old path
    assert os.path.isdir(old_path)
    assert os.listdir(old_path)


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
@pytest.mark.parametrize(
    "include_result,inplace,to_check",
    (
        [None, None, "GUI can be opened."],
        [None, True, "Working directory is in the pytest directory."],
        [None, False, "Working directory is NOT in the pytest directory."],
        [True, None, "There is a result file, and WDIR is a temp dir."],
        pytest.param(
            True, True, "Both options (`True`) is not allowed.", marks=pytest.mark.xfail
        ),
        [True, False, "There is a result file, and WDIR is in a temp dir."],
        [False, None, "There is NOT a result file, and WDIR is in a temp dir."],
        [False, True, "There is NOT a result file, and WDIR is in pytest dir."],
        [False, False, "There is NOT a result file, and WDIR is in a temp dir."],
    ),
)
def test_open_gui(
    mapdl, fake_local_mapdl, cube_solve, inplace, include_result, to_check
):
    print(to_check)  # in case we use -s flat with pytest
    mapdl.open_gui(inplace=inplace, include_result=include_result)


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


valid_versions = []
valid_versions.extend(list(versions.keys()))
valid_versions.extend([each / 10 for each in versions.keys()])
valid_versions.extend([str(each) for each in list(versions.keys())])
valid_versions.extend([str(each / 10) for each in versions.keys()])
valid_versions.extend(list(versions.values()))


@pytest.mark.parametrize("version", valid_versions)
def test__verify_version_pass(version):
    ver = _verify_version(version)
    assert isinstance(ver, int)
    assert min(versions.keys()) <= ver <= max(versions.keys())


@pytest.mark.skipif(
    get_start_instance() is False,
    reason="Skip when start instance is disabled",
)
def test_find_ansys(mapdl):
    assert find_ansys() is not None

    # Checking ints
    version = int(mapdl.version * 10)
    assert find_ansys(version=version) is not None

    # Checking floats
    assert find_ansys(version=22.2) is not None
    assert find_ansys(version=mapdl.version) is not None

    with pytest.raises(ValueError):
        assert find_ansys(version="11")


@pytest.mark.skipif(
    get_start_instance() is False,
    reason="Skip when start instance is disabled",
)
def test_version(mapdl):
    version = int(10 * mapdl.version)
    mapdl_ = launch_mapdl(version=version, start_timeout=start_timeout)
    mapdl_.exit()


@pytest.mark.skipif(
    get_start_instance() is False,
    reason="Skip when start instance is disabled",
)
def test_raise_exec_path_and_version_launcher():
    with pytest.raises(ValueError):
        launch_mapdl(exec_file="asdf", version="asdf", start_timeout=start_timeout)


@pytest.mark.skipif(
    not (
        os.environ.get("ON_LOCAL", "false").lower() == "true"
        and os.environ.get("ON_UBUNTU", "false").lower() == "true"
    ),
    reason="Skip when start instance is disabled",
)
def test_is_ubuntu():
    assert _is_ubuntu()


@pytest.mark.skipif(
    get_start_instance() is False,
    reason="Skip when start instance is disabled",
)
def test_get_default_ansys():
    assert get_default_ansys() is not None


def test_launch_mapdl_non_recognaised_arguments():
    with pytest.raises(ValueError, match="my_fake_argument"):
        launch_mapdl(my_fake_argument="my_fake_value")


def test_mapdl_non_recognaised_arguments():
    with pytest.raises(ValueError, match="my_fake_argument"):
        pymapdl.Mapdl(my_fake_argument="my_fake_value")
