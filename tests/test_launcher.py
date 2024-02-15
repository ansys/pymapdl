# Copyright (C) 2024 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Test the mapdl launcher"""

import os
import tempfile
from time import sleep

import psutil
import pytest

from ansys.mapdl import core as pymapdl
from ansys.mapdl.core.errors import (
    DeprecationError,
    LicenseServerConnectionError,
    MapdlDidNotStart,
    NotEnoughResources,
    PortAlreadyInUseByAnMAPDLInstance,
)
from ansys.mapdl.core.launcher import (
    _check_license_argument,
    _force_smp_student_version,
    _is_ubuntu,
    _parse_ip_route,
    _validate_MPI,
    _verify_version,
    launch_grpc,
    launch_mapdl,
    update_env_vars,
)
from ansys.mapdl.core.licensing import LICENSES
from conftest import ON_LOCAL, QUICK_LAUNCH_SWITCHES, requires

try:
    from ansys.tools.path import (
        find_ansys,
        get_available_ansys_installations,
        version_from_path,
    )

    from ansys.mapdl.core.launcher import get_default_ansys

    installed_mapdl_versions = list(get_available_ansys_installations().keys())
    try:
        V150_EXEC = find_ansys("150")[0]
    except ValueError:
        V150_EXEC = ""
except:
    from conftest import MAPDL_VERSION

    installed_mapdl_versions = [MAPDL_VERSION]
    V150_EXEC = ""

from ansys.mapdl.core._version import SUPPORTED_ANSYS_VERSIONS as versions

paths = [
    ("/usr/dir_v2019.1/slv/ansys_inc/v211/ansys/bin/ansys211", 211),
    ("C:/Program Files/ANSYS Inc/v202/ansys/bin/win64/ANSYS202.exe", 202),
    ("/usr/ansys_inc/v211/ansys/bin/mapdl", 211),
]

start_timeout = 30  # Seconds


@pytest.fixture
def fake_local_mapdl(mapdl):
    """Fixture to execute asserts before and after a test is run"""
    # Setup: fill with any logic you want
    mapdl._local = True

    yield True  # this is where the testing happens

    # Teardown : fill with any logic you want
    mapdl._local = False


@requires("local")
@requires("windows")
def test_validate_sw():
    # ensure that windows adds msmpi
    # fake windows path
    exec_path = "C:/Program Files/ANSYS Inc/v211/ansys/bin/win64/ANSYS211.exe"
    add_sw = _validate_MPI("", exec_path)
    assert "msmpi" in add_sw

    add_sw = _validate_MPI("-mpi intelmpi", exec_path)
    assert "msmpi" in add_sw and "intelmpi" not in add_sw

    add_sw = _validate_MPI("-mpi INTELMPI", exec_path)
    assert "msmpi" in add_sw and "INTELMPI" not in add_sw


@requires("ansys-tools-path")
@requires("local")
@pytest.mark.parametrize("path_data", paths)
def test_version_from_path(path_data):
    exec_file, version = path_data
    assert version_from_path("mapdl", exec_file) == version


@requires("ansys-tools-path")
@requires("local")
def test_catch_version_from_path():
    with pytest.raises(RuntimeError):
        version_from_path("mapdl", "abc")


@requires("ansys-tools-path")
@requires("local")
@requires("linux")
def test_find_ansys_linux():
    # assuming ansys is installed, should be able to find it on linux
    # without env var
    bin_file, ver = pymapdl.launcher.find_ansys()
    assert os.path.isfile(bin_file)
    assert isinstance(ver, float)


@requires("ansys-tools-path")
@requires("local")
def test_invalid_mode(mapdl):
    with pytest.raises(ValueError):
        exec_file = find_ansys(installed_mapdl_versions[0])[0]
        pymapdl.launch_mapdl(
            exec_file, port=mapdl.port + 1, mode="notamode", start_timeout=start_timeout
        )


@requires("ansys-tools-path")
@requires("local")
@pytest.mark.skipif(not os.path.isfile(V150_EXEC), reason="Requires v150")
def test_old_version(mapdl):
    exec_file = find_ansys("150")[0]
    with pytest.raises(ValueError):
        pymapdl.launch_mapdl(
            exec_file, port=mapdl.port + 1, mode="console", start_timeout=start_timeout
        )


@requires("ansys-tools-path")
@requires("local")
@requires("linux")
@requires("console")
def test_failed_console():
    exec_file = find_ansys(installed_mapdl_versions[0])[0]
    with pytest.raises(ValueError):
        pymapdl.launch_mapdl(exec_file, mode="console", start_timeout=start_timeout)


@requires("ansys-tools-path")
@requires("local")
@requires("console")
@requires("linux")
@pytest.mark.parametrize("version", installed_mapdl_versions)
def test_launch_console(version):
    exec_file = find_ansys(version)[0]
    mapdl = pymapdl.launch_mapdl(exec_file, mode="console", start_timeout=start_timeout)
    assert mapdl.version == int(version) / 10


@requires("local")
@requires("nostudent")
def test_license_type_keyword():
    checks = []
    for license_name, license_description in LICENSES.items():
        try:
            mapdl = launch_mapdl(
                license_type=license_name,
                start_timeout=start_timeout,
                additional_switches=QUICK_LAUNCH_SWITCHES,
            )

            # Using first line to ensure not picking up other stuff.
            checks.append(license_description in mapdl.__str__().split("\n")[0])
            mapdl.exit()
            del mapdl
            sleep(2)

        except MapdlDidNotStart as e:
            if "ANSYS license not available" in str(e):
                continue
            else:
                raise e

    assert any(checks)


@requires("local")
@requires("nostudent")
def test_license_type_keyword_names():
    # This test might became a way to check available licenses, which is not the purpose.

    successful_check = False
    for license_name, license_description in LICENSES.items():
        mapdl = launch_mapdl(
            license_type=license_name,
            start_timeout=start_timeout,
            additional_switches=QUICK_LAUNCH_SWITCHES,
        )

        # Using first line to ensure not picking up other stuff.
        successful_check = (
            license_description in mapdl.__str__().split("\n")[0] or successful_check
        )
        assert license_description in mapdl.__str__().split("\n")[0]
        mapdl.exit()

    assert successful_check  # if at least one license is ok, this should be true.


@requires("local")
@requires("nostudent")
def test_license_type_additional_switch():
    # This test might became a way to check available licenses, which is not the purpose.
    successful_check = False
    for license_name, license_description in LICENSES.items():
        mapdl = launch_mapdl(
            additional_switches=QUICK_LAUNCH_SWITCHES + " -p " + license_name,
            start_timeout=start_timeout,
        )

        # Using first line to ensure not picking up other stuff.
        successful_check = (
            license_description in mapdl.__str__().split("\n")[0] or successful_check
        )
        mapdl.exit()

    assert successful_check  # if at least one license is ok, this should be true.


@requires("ansys-tools-path")
@requires("local")
def test_license_type_dummy(mapdl):
    dummy_license_type = "dummy"
    with pytest.raises(LicenseServerConnectionError):
        launch_mapdl(
            port=mapdl.port + 1,
            additional_switches=f" -p {dummy_license_type}" + QUICK_LAUNCH_SWITCHES,
            start_timeout=start_timeout,
        )


@requires("local")
@requires("nostudent")
def test_remove_temp_files(mapdl):
    """Ensure the working directory is removed when run_location is not set."""
    mapdl = launch_mapdl(
        port=mapdl.port + 1,
        remove_temp_files=True,
        start_timeout=start_timeout,
        additional_switches=QUICK_LAUNCH_SWITCHES,
    )

    # possible MAPDL is installed but running in "remote" mode
    path = mapdl.directory
    mapdl.exit()

    tmp_dir = tempfile.gettempdir()
    ans_temp_dir = os.path.join(tmp_dir, "ansys_")
    if path.startswith(ans_temp_dir):
        assert not os.path.isdir(path)
    else:
        assert os.path.isdir(path)


@requires("local")
@requires("nostudent")
def test_remove_temp_files_fail(tmpdir, mapdl):
    """Ensure the working directory is not removed when the cwd is changed."""
    mapdl = launch_mapdl(
        port=mapdl.port + 1,
        remove_temp_files=True,
        start_timeout=start_timeout,
        additional_switches=QUICK_LAUNCH_SWITCHES,
    )
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
            True, True, "Both options (`True`) is not allowed.", marks=pytest.mark.fail
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

    add_sw = "-SMP"
    exec_path = r"C:\Program Files\ANSYS Inc\v222\ansys\bin\winx64\ANSYS222.exe"
    assert "-SMP" in _force_smp_student_version(add_sw, exec_path)


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


installed_mapdl_versions = []
installed_mapdl_versions.extend(list(versions.keys()))
installed_mapdl_versions.extend([each / 10 for each in versions.keys()])
installed_mapdl_versions.extend([str(each) for each in list(versions.keys())])
installed_mapdl_versions.extend([str(each / 10) for each in versions.keys()])
installed_mapdl_versions.extend(list(versions.values()))


@pytest.mark.parametrize("version", installed_mapdl_versions)
def test__verify_version_pass(version):
    ver = _verify_version(version)
    assert isinstance(ver, int)
    assert min(versions.keys()) <= ver <= max(versions.keys())


def test__verify_version_latest():
    assert _verify_version("latest") is None


@requires("ansys-tools-path")
@requires("local")
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


@requires("local")
def test_version(mapdl):
    version = int(10 * mapdl.version)
    launching_arg = launch_mapdl(
        port=mapdl.port + 1,
        version=version,
        start_timeout=start_timeout,
        additional_switches=QUICK_LAUNCH_SWITCHES,
        _debug_no_launch=True,
    )
    assert str(version) in launching_arg["start_parm"]["exec_file"]


@requires("local")
def test_raise_exec_path_and_version_launcher(mapdl):
    with pytest.raises(ValueError):
        launch_mapdl(
            exec_file="asdf",
            port=mapdl.port + 1,
            version="asdf",
            start_timeout=start_timeout,
            additional_switches=QUICK_LAUNCH_SWITCHES,
        )


@requires("linux")
@requires("local")
def test_is_ubuntu():
    assert _is_ubuntu()


@requires("ansys-tools-path")
@requires("local")
def test_get_default_ansys():
    assert get_default_ansys() is not None


def test_launch_mapdl_non_recognaised_arguments(mapdl):
    with pytest.raises(ValueError, match="my_fake_argument"):
        launch_mapdl(
            port=mapdl.port + 1,
            my_fake_argument="my_fake_value",
            additional_switches=QUICK_LAUNCH_SWITCHES,
        )


def test_mapdl_non_recognaised_arguments():
    with pytest.raises(ValueError, match="my_fake_argument"):
        pymapdl.Mapdl(
            my_fake_argument="my_fake_value", additional_switches=QUICK_LAUNCH_SWITCHES
        )


def test__parse_ip_route():
    output = """default via 172.25.192.1 dev eth0 proto kernel <<<=== this
172.25.192.0/20 dev eth0 proto kernel scope link src 172.25.195.101 <<<=== not this"""

    assert "172.25.192.1" == _parse_ip_route(output)

    output = """
default via 172.23.112.1 dev eth0 proto kernel
172.23.112.0/20 dev eth0 proto kernel scope link src 172.23.121.145"""

    assert "172.23.112.1" == _parse_ip_route(output)


def test_launched(mapdl):
    if ON_LOCAL:
        assert mapdl.launched
    else:
        assert not mapdl.launched


@requires("local")
def test_launching_on_busy_port(mapdl):
    with pytest.raises(PortAlreadyInUseByAnMAPDLInstance):
        launch_mapdl(port=mapdl.port)


@requires("local")
def test_cpu_checks():
    machine_cores = psutil.cpu_count(logical=False)
    with pytest.raises(NotEnoughResources):
        launch_mapdl(nproc=machine_cores + 2)


def test_fail_channel_port():
    with pytest.raises(ValueError):
        launch_mapdl(channel="something", port="something")


def test_fail_channel_ip():
    with pytest.raises(ValueError):
        launch_mapdl(channel="something", ip="something")


def test_deprecate_verbose():
    with pytest.raises(DeprecationError):
        launch_mapdl(verbose_mapdl=True)

    with pytest.raises(ValueError):
        launch_mapdl(verbose=True)

    with pytest.raises(DeprecationError):
        launch_grpc(verbose=True)
