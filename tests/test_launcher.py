# Copyright (C) 2016 - 2026 ANSYS, Inc. and/or its affiliates.
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
import subprocess
import tempfile
from time import sleep
from unittest.mock import MagicMock, Mock, patch
import warnings

import psutil
from pyfakefs.fake_filesystem import OSType
import pytest

from ansys.mapdl import core as pymapdl
from ansys.mapdl.core.errors import (
    IncorrectMPIConfigurationError,
    MapdlDidNotStart,
    NotAvailableLicenses,
    NotEnoughResources,
    PortAlreadyInUseByAnMAPDLInstance,
    VersionError,
)
from ansys.mapdl.core.launcher import (
    _HAS_ATC,
    LOCALHOST,
    _is_ubuntu,
    check_mapdl_launch_on_hpc,
    check_mode,
    force_smp_in_student,
    generate_mapdl_launch_command,
    generate_sbatch_command,
    generate_start_parameters,
    get_cpus,
    get_exec_file,
    get_hostname_host_cluster,
    get_ip,
    get_jobid,
    get_port,
    get_run_location,
    get_slurm_options,
    get_start_instance,
    get_version,
    inject_additional_switches,
    is_running_on_slurm,
    kill_job,
    launch_grpc,
    launch_mapdl,
    launch_mapdl_on_cluster,
    remove_err_files,
    send_scontrol,
    set_license_switch,
    set_MPI_additional_switches,
    submitter,
    update_env_vars,
)
from ansys.mapdl.core.licensing import LICENSES
from ansys.mapdl.core.misc import check_has_mapdl, parse_ip_route, stack
from conftest import (
    ON_LOCAL,
    PATCH_MAPDL,
    PATCH_MAPDL_START,
    QUICK_LAUNCH_SWITCHES,
    TESTING_MINIMAL,
    NullContext,
    requires,
)

try:
    from ansys.tools.common.path import (
        find_mapdl,
        get_available_ansys_installations,
        version_from_path,
    )

    from ansys.mapdl.core.launcher import get_default_ansys

    installed_mapdl_versions = list(get_available_ansys_installations().keys())
except:
    from conftest import MAPDL_VERSION

    installed_mapdl_versions = [MAPDL_VERSION]


from ansys.mapdl.core._version import SUPPORTED_ANSYS_VERSIONS as versions

paths = [
    ("/usr/dir_v2019.1/slv/ansys_inc/v211/ansys/bin/ansys211", 211),
    ("C:/Program Files/ANSYS Inc/v202/ansys/bin/win64/ANSYS202.exe", 202),
    ("/usr/ansys_inc/v211/ansys/bin/mapdl", 211),
]

start_timeout = 30  # Seconds


def get_fake_process(message_stdout, message_stderr="", time_sleep=0):
    class stdout:
        def read(self):
            return message_stdout.encode()

    class stderr:
        def read(self):
            return message_stderr.encode()

    class myprocess:
        pass

    process = myprocess()
    process.stdout = stdout()
    process.stderr = stderr()

    sleep(time_sleep)

    return process


@pytest.fixture
def my_fs(fs):
    # fs.add_real_directory("/proc", lazy_read=False)
    yield fs


@pytest.fixture
def fake_local_mapdl(mapdl):
    """Fixture to execute asserts before and after a test is run"""
    # Setup: fill with any logic you want
    mapdl._local = True

    yield True  # this is where the testing happens

    # Teardown : fill with any logic you want
    mapdl._local = False


@patch("os.name", "nt")
def test_validate_sw():
    # ensure that windows adds msmpi
    # fake windows path
    version = 211
    add_sw = set_MPI_additional_switches("", version=version)
    assert "msmpi" in add_sw

    with pytest.warns(
        UserWarning, match="Due to incompatibilities between this MAPDL version"
    ):
        add_sw = set_MPI_additional_switches("-mpi intelmpi", version=version)
        assert "msmpi" in add_sw and "intelmpi" not in add_sw

    with pytest.warns(
        UserWarning, match="Due to incompatibilities between this MAPDL version"
    ):
        add_sw = set_MPI_additional_switches("-mpi INTELMPI", version=version)
        assert "msmpi" in add_sw and "INTELMPI" not in add_sw


@requires("ansys-tools-common")
@pytest.mark.parametrize("path_data", paths)
def test_version_from_path(path_data):
    exec_file, version = path_data
    assert version_from_path("mapdl", exec_file) == version


@requires("ansys-tools-common")
def test_catch_version_from_path():
    with pytest.raises(RuntimeError):
        version_from_path("mapdl", "abc")


@pytest.mark.parametrize(
    "path,version,raises",
    [
        ["/ansys_inc/v221/ansys/bin/ansys221", 22.1, None],
        ["/ansys_inc/v222/ansys/bin/mapdl", 22.2, None],
        ["/usr/ansys_inc/v231/ansys/bin/mapdl", 23.1, None],
        ["/usr/ansys_inc/v232/ansys/bin/mapdl", 23.2, None],
        ["/usr/ansys_inc/v241/ansys/bin/mapdl", 24.1, None],
        ["/ansysinc/v242/ansys/bin/ansys2", 24.2, ValueError],
        ["/ansysinc/v242/ansys/bin/mapdl", 24.2, ValueError],
    ],
)
@requires("ansys-tools-common")
def test_find_mapdl_linux(my_fs, path, version, raises):
    my_fs.os = OSType.LINUX
    my_fs.create_file(path)

    from ansys.tools.common.path import find_mapdl

    bin_file, ver = find_mapdl()

    if raises:
        assert not bin_file
        assert not ver

    else:
        assert bin_file.startswith(path.replace("mapdl", ""))
        assert isinstance(ver, float)
        assert ver == version


@requires("ansys-tools-common")
@patch("psutil.cpu_count", lambda *args, **kwargs: 2)
@patch("ansys.mapdl.core.launcher._is_ubuntu", lambda *args, **kwargs: True)
@patch("ansys.mapdl.core.launcher.get_process_at_port", lambda *args, **kwargs: None)
def test_invalid_mode(mapdl, my_fs, cleared, monkeypatch):
    monkeypatch.delenv("PYMAPDL_START_INSTANCE", False)
    monkeypatch.delenv("PYMAPDL_IP", False)
    monkeypatch.delenv("PYMAPDL_PORT", False)

    my_fs.create_file("/ansys_inc/v241/ansys/bin/ansys241")
    with pytest.raises(ValueError):
        exec_file = find_mapdl()[0]
        pymapdl.launch_mapdl(
            exec_file, port=mapdl.port + 1, mode="notamode", start_timeout=start_timeout
        )


@requires("ansys-tools-common")
@pytest.mark.parametrize("version", [120, 170, 190])
@patch("psutil.cpu_count", lambda *args, **kwargs: 2)
@patch("ansys.mapdl.core.launcher._is_ubuntu", lambda *args, **kwargs: True)
@patch("ansys.mapdl.core.launcher.get_process_at_port", lambda *args, **kwargs: None)
def test_old_version_not_version(mapdl, my_fs, cleared, monkeypatch, version):
    monkeypatch.delenv("PYMAPDL_START_INSTANCE", False)
    monkeypatch.delenv("PYMAPDL_IP", False)
    monkeypatch.delenv("PYMAPDL_PORT", False)

    exec_file = f"/ansys_inc/v{version}/ansys/bin/ansys{version}"
    my_fs.create_file(exec_file)
    assert exec_file == find_mapdl()[0]

    with pytest.raises(
        ValueError, match="The MAPDL gRPC interface requires MAPDL 20.2 or later"
    ):
        pymapdl.launch_mapdl(
            exec_file=exec_file,
            port=mapdl.port + 1,
            mode="grpc",
            start_timeout=start_timeout,
        )


@requires("ansys-tools-common")
@pytest.mark.parametrize("version", [203, 213, 351])
@patch("psutil.cpu_count", lambda *args, **kwargs: 2)
@patch("ansys.mapdl.core.launcher._is_ubuntu", lambda *args, **kwargs: True)
@patch("ansys.mapdl.core.launcher.get_process_at_port", lambda *args, **kwargs: None)
def test_not_valid_versions(mapdl, my_fs, cleared, monkeypatch, version):
    monkeypatch.delenv("PYMAPDL_START_INSTANCE", False)
    monkeypatch.delenv("PYMAPDL_IP", False)
    monkeypatch.delenv("PYMAPDL_PORT", False)

    exec_file = f"/ansys_inc/v{version}/ansys/bin/ansys{version}"
    my_fs.create_file(exec_file)

    assert exec_file == find_mapdl()[0]
    with pytest.raises(ValueError, match="MAPDL version must be one of the following"):
        pymapdl.launch_mapdl(
            exec_file=exec_file,
            port=mapdl.port + 1,
            mode="grpc",
            start_timeout=start_timeout,
        )


@requires("ansys-tools-common")
@requires("local")
@requires("linux")
@requires("console")
@pytest.mark.skipif(True, reason="Skipping this console test. See issue #3791")
def test_failed_console():
    exec_file = find_mapdl(str(installed_mapdl_versions[0]))[0]
    with pytest.raises(ValueError):
        pymapdl.launch_mapdl(exec_file, mode="console", start_timeout=start_timeout)


@requires("ansys-tools-common")
@requires("local")
@requires("console")
@requires("linux")
@pytest.mark.parametrize("version", installed_mapdl_versions)
def test_launch_console(version):
    exec_file = find_mapdl(version)[0]
    mapdl = pymapdl.launch_mapdl(exec_file, mode="console", start_timeout=start_timeout)
    assert mapdl.version == int(version) / 10


@requires("local")
@requires("nostudent")
@requires("ansys-tools-common")
@pytest.mark.parametrize("license_name", LICENSES)
def test_license_type_keyword_names(monkeypatch, license_name):
    exec_file = find_mapdl()[0]
    args = launch_mapdl(
        exec_file=exec_file, license_type=license_name, _debug_no_launch=True
    )
    assert f"-p {license_name}" in args["additional_switches"]


@pytest.mark.parametrize("license_name", LICENSES)
def test_license_type_additional_switch(license_name):
    args = launch_mapdl(
        additional_switches=QUICK_LAUNCH_SWITCHES + " -p " + license_name,
        _debug_no_launch=True,
    )
    assert f"-p {license_name}" in args["additional_switches"]


@stack(*PATCH_MAPDL_START)
@requires("ansys-tools-common")
def test_license_type_dummy(mapdl, cleared):
    dummy_license_type = "dummy"
    with pytest.warns(
        UserWarning,
        match="Still PyMAPDL will try to use it but in older MAPDL versions you might experience",
    ):
        launch_mapdl(
            start_instance=True,
            additional_switches=f" -p {dummy_license_type} " + QUICK_LAUNCH_SWITCHES,
            start_timeout=start_timeout,
            license_server_check=False,
            _debug_no_launch=True,
        )


@requires("local")
@requires("nostudent")
def test_remove_temp_dir_on_exit(mapdl, cleared):
    """Ensure the working directory is removed when run_location is not set."""
    mapdl_ = launch_mapdl(
        port=mapdl.port + 1,
        remove_temp_dir_on_exit=True,
        start_timeout=start_timeout,
        additional_switches=QUICK_LAUNCH_SWITCHES,
    )

    # possible MAPDL is installed but running in "remote" mode
    path = mapdl_.directory
    mapdl_.exit()

    tmp_dir = tempfile.gettempdir()
    ans_temp_dir = os.path.join(tmp_dir, "ansys_")
    if str(path).startswith(ans_temp_dir):
        assert not os.path.isdir(path)
    else:
        assert os.path.isdir(path)


@requires("local")
@requires("nostudent")
def test_remove_temp_dir_on_exit_fail(mapdl, cleared, tmpdir):
    """Ensure the working directory is not removed when the cwd is changed."""
    mapdl_ = launch_mapdl(
        port=mapdl.port + 1,
        remove_temp_dir_on_exit=True,
        start_timeout=start_timeout,
        additional_switches=QUICK_LAUNCH_SWITCHES,
    )
    old_path = mapdl_.directory
    assert os.path.isdir(str(tmpdir))
    mapdl_.cwd(str(tmpdir))
    path = mapdl_.directory
    mapdl_.exit()
    assert os.path.isdir(path)

    # Checking no changes in the old path
    assert os.path.isdir(old_path)
    assert os.listdir(old_path)


def test_env_injection():
    no_inject = update_env_vars(None, None)
    assert no_inject == os.environ.copy()  # return os.environ

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


@requires("gui")
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


def test_force_smp_in_student():
    add_sw = ""
    exec_path = (
        r"C:\Program Files\ANSYS Inc\ANSYS Student\v222\ansys\bin\winx64\ANSYS222.exe"
    )
    assert "-smp" in force_smp_in_student(add_sw, exec_path)

    add_sw = "-mpi"
    exec_path = (
        r"C:\Program Files\ANSYS Inc\ANSYS Student\v222\ansys\bin\winx64\ANSYS222.exe"
    )
    assert "-smp" not in force_smp_in_student(add_sw, exec_path)

    add_sw = "-dmp"
    exec_path = (
        r"C:\Program Files\ANSYS Inc\ANSYS Student\v222\ansys\bin\winx64\ANSYS222.exe"
    )
    assert "-smp" not in force_smp_in_student(add_sw, exec_path)

    add_sw = ""
    exec_path = r"C:\Program Files\ANSYS Inc\v222\ansys\bin\winx64\ANSYS222.exe"
    assert "-smp" not in force_smp_in_student(add_sw, exec_path)

    add_sw = "-SMP"
    exec_path = r"C:\Program Files\ANSYS Inc\v222\ansys\bin\winx64\ANSYS222.exe"
    assert "-SMP" in force_smp_in_student(add_sw, exec_path)


@pytest.mark.parametrize(
    "license_short,license_name",
    [[each_key, each_value] for each_key, each_value in LICENSES.items()],
)
def test_license_product_argument(license_short, license_name):
    additional_switches = set_license_switch(license_name, "qwer")
    assert f"qwer -p {license_short}" in additional_switches


@pytest.mark.parametrize("unvalid_type", [1, {}, ()])
def test_license_product_argument_type_error(unvalid_type):
    with pytest.raises(TypeError):
        set_license_switch(unvalid_type, "")


def test_license_product_argument_warning():
    with pytest.warns(UserWarning):
        assert "-p asdf" in set_license_switch("asdf", "qwer")


@pytest.mark.parametrize(
    "license_short,license_name",
    [[each_key, each_value] for each_key, each_value in LICENSES.items()],
)
def test_license_product_argument_p_arg(license_short, license_name):
    assert f"qw1234 -p {license_short}" == set_license_switch(
        None, f"qw1234 -p {license_short}"
    )


def test_license_product_argument_p_arg_warning():
    with pytest.warns(UserWarning):
        assert "qwer -p asdf" in set_license_switch(None, "qwer -p asdf")


installed_mapdl_versions = []
installed_mapdl_versions.extend([int(each) for each in list(versions.keys())])
installed_mapdl_versions.extend([float(each / 10) for each in versions.keys()])
installed_mapdl_versions.extend([str(each) for each in list(versions.keys())])
installed_mapdl_versions.extend([str(each / 10) for each in versions.keys()])
installed_mapdl_versions.extend(list(versions.values()))
installed_mapdl_versions.extend([None])


@pytest.mark.parametrize("version", installed_mapdl_versions)
def test__verify_version_pass(version):
    ver = get_version(version)
    if version:
        assert isinstance(ver, int)
        assert min(versions.keys()) <= ver <= max(versions.keys())
    else:
        assert ver is None


def test__verify_version_latest():
    assert get_version("latest") is None


@requires("ansys-tools-common")
@requires("local")
def test_find_ansys(mapdl, cleared):
    assert find_mapdl() is not None

    # Checking ints
    version = int(mapdl.version * 10)
    assert find_mapdl(version=version) is not None

    # Checking floats
    with pytest.raises(ValueError):
        find_mapdl(version=22.2)

    assert find_mapdl(version=mapdl.version) is not None

    with pytest.raises(ValueError):
        assert find_mapdl(version="11")


@requires("local")
def test_version(mapdl, cleared):
    version = int(10 * mapdl.version)
    launching_arg = launch_mapdl(
        port=mapdl.port + 1,
        version=version,
        start_timeout=start_timeout,
        additional_switches=QUICK_LAUNCH_SWITCHES,
        _debug_no_launch=True,
    )
    assert str(version) in str(launching_arg["version"])


@requires("local")
def test_raise_exec_path_and_version_launcher(mapdl, cleared):
    with pytest.raises(ValueError):
        get_version("asdf", "asdf")


@requires("linux")
@requires("local")
def test_is_ubuntu():
    assert _is_ubuntu()


@requires("ansys-tools-common")
@requires("local")
def test_get_default_ansys():
    assert get_default_ansys() is not None


def test_launch_mapdl_non_recognaised_arguments(mapdl, cleared):
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

    assert "172.25.192.1" == parse_ip_route(output)

    output = """
default via 172.23.112.1 dev eth0 proto kernel
172.23.112.0/20 dev eth0 proto kernel scope link src 172.23.121.145"""

    assert "172.23.112.1" == parse_ip_route(output)


def test_launched(mapdl, cleared):
    if ON_LOCAL:
        assert mapdl.launched
    else:
        assert not mapdl.launched


@requires("local")
def test_launching_on_busy_port(mapdl, cleared, monkeypatch):
    monkeypatch.delenv("PYMAPDL_PORT", raising=False)
    with pytest.raises(PortAlreadyInUseByAnMAPDLInstance):
        launch_mapdl(port=mapdl.port)


def test_fail_channel_port():
    with pytest.raises(ValueError):
        launch_mapdl(channel="something", port="something")


def test_fail_channel_ip():
    with pytest.raises(ValueError):
        launch_mapdl(channel="something", ip="something")


@pytest.mark.parametrize(
    "set_env_var_context,validation",
    (
        pytest.param(
            {
                "SLURM_NNODES": None,
                "SLURM_NTASKS": None,
                "SLURM_CPUS_PER_TASK": None,
                "SLURM_NPROCS": None,
                "SLURM_CPUS_ON_NODE": None,
                "SLURM_MEM_PER_NODE": None,
                "SLURM_NODELIST": None,
            },
            {"nproc": 1},
            id="No parameters supplied",
        ),
        pytest.param(
            {
                "SLURM_NNODES": 5,
                "SLURM_NTASKS": 1,
                "SLURM_CPUS_PER_TASK": 1,
                "SLURM_NPROCS": 1,
                "SLURM_CPUS_ON_NODE": 1,
                "SLURM_MEM_PER_NODE": None,
                "SLURM_NODELIST": None,
            },
            {"nproc": 5},
            id="Testing NNODE only",
        ),
        pytest.param(
            {
                "SLURM_NNODES": 5,
                "SLURM_NTASKS": 1,
                "SLURM_CPUS_PER_TASK": 1,
                "SLURM_NPROCS": 1,
                "SLURM_CPUS_ON_NODE": 2,
                "SLURM_MEM_PER_NODE": None,
                "SLURM_NODELIST": None,
            },
            {"nproc": 10},
            id="Testing NNODE and CPUS_ON_NODE only",
        ),
        pytest.param(
            {
                "SLURM_NNODES": 1,
                "SLURM_NTASKS": 5,
                "SLURM_CPUS_PER_TASK": 1,
                "SLURM_NPROCS": 1,
                "SLURM_CPUS_ON_NODE": 1,
                "SLURM_MEM_PER_NODE": None,
                "SLURM_NODELIST": None,
            },
            {"nproc": 5},
            id="Testing NTASKS only",
        ),
        pytest.param(
            {
                "SLURM_NNODES": 1,
                "SLURM_NTASKS": 5,
                "SLURM_CPUS_PER_TASK": 2,
                "SLURM_NPROCS": 1,
                "SLURM_CPUS_ON_NODE": 1,
                "SLURM_MEM_PER_NODE": None,
                "SLURM_NODELIST": None,
            },
            {"nproc": 10},
            id="Testing NTASKS only",
        ),
        pytest.param(
            {
                "SLURM_NNODES": 2,
                "SLURM_NTASKS": 2,
                "SLURM_CPUS_PER_TASK": 2,
                "SLURM_NPROCS": 18,
                "SLURM_CPUS_ON_NODE": None,
                "SLURM_MEM_PER_NODE": None,
                "SLURM_NODELIST": None,
            },
            {"nproc": 18},
            id="Testing NPROCS only",
        ),
        pytest.param(
            # This test probably does not do a good memory mapping between
            # MEM_PER_NODE and "ram"
            {
                "SLURM_NNODES": 4,
                "SLURM_NTASKS": 2,
                "SLURM_CPUS_PER_TASK": 2,
                "SLURM_NPROCS": None,
                "SLURM_CPUS_ON_NODE": None,
                "SLURM_MEM_PER_NODE": "1000",
                "SLURM_NODELIST": None,
            },
            {"nproc": 4, "ram": 1000},
            id="Testing NNODES and MEM_PER_NODE",
        ),
        pytest.param(
            {
                "SLURM_JOB_NAME": "myawesomejob",
                "SLURM_NTASKS": 2,
                "SLURM_CPUS_PER_TASK": 2,
                "SLURM_NPROCS": 1,
                "SLURM_CPUS_ON_NODE": None,
                "SLURM_MEM_PER_NODE": None,
                "SLURM_NODELIST": None,
            },
            {"nproc": 4, "jobname": "myawesomejob"},
            id="Testing SLURM_JOB_NAME",
        ),
        pytest.param(
            {
                "SLURM_JOB_NAME": "myawesomejob",
                "SLURM_NTASKS": 2,
                "SLURM_CPUS_PER_TASK": 2,
                "SLURM_NPROCS": 1,
                "SLURM_CPUS_ON_NODE": None,
                "SLURM_MEM_PER_NODE": None,
                "SLURM_NODELIST": None,
                "PYMAPDL_MAPDL_EXEC": "asdf/qwer/poiu",
            },
            {"nproc": 4, "jobname": "myawesomejob", "exec_file": "asdf/qwer/poiu"},
            id="Testing PYMAPDL_MAPDL_EXEC and SLURM_JOB_NAME",
        ),
    ),
    indirect=["set_env_var_context"],
)
def test_get_slurm_options(set_env_var_context, validation, monkeypatch):
    """test slurm env vars"""
    if "PYMAPDL_NPROC" in os.environ:
        monkeypatch.delenv("PYMAPDL_NPROC")

    for each_key, each_value in set_env_var_context.items():
        if each_value:
            assert os.environ.get(each_key) == str(each_value)

    args = {
        "exec_file": None,
        "jobname": "",
        "nproc": None,
        "ram": None,
        "additional_switches": "",
        "start_timeout": 45,
    }
    kwargs = {}
    get_slurm_options(args, kwargs)
    assert args["nproc"] == validation["nproc"]

    if args["ram"]:
        assert args["ram"] == validation["ram"]

    if args["jobname"] != "file":
        assert args["jobname"] == validation["jobname"]

    if args["exec_file"] and validation.get("exec_file", None):
        assert args["exec_file"] == validation["exec_file"]


@pytest.mark.parametrize(
    "ram,expected,context",
    [
        ["2048k", 2, NullContext()],
        ["10M", 10, NullContext()],
        ["100G", 100 * 1024, NullContext()],
        ["1T", 1024**2, NullContext()],
        ["100", 100, NullContext()],
        [
            "100E",
            "",
            pytest.raises(
                ValueError, match="The memory defined in 'SLURM_MEM_PER_NODE' env var"
            ),
        ],
    ],
)
def test_slurm_ram(monkeypatch, ram, expected, context):
    monkeypatch.setenv("SLURM_MEM_PER_NODE", str(ram))
    monkeypatch.setenv("PYMAPDL_MAPDL_EXEC", "asdf/qwer/poiu")

    args = {
        "exec_file": None,
        "jobname": "",
        "ram": None,
        "nproc": None,
        "additional_switches": "",
        "start_timeout": 45,
    }
    with context:
        args = get_slurm_options(args, {})
        assert args["ram"] == expected


@pytest.mark.parametrize("slurm_env_var", ["True", "false", ""])
@pytest.mark.parametrize("slurm_job_name", ["True", "false", ""])
@pytest.mark.parametrize("slurm_job_id", ["True", "false", ""])
@pytest.mark.parametrize("running_on_hpc", [True, False, None])
def test_is_running_on_slurm(
    monkeypatch, slurm_env_var, slurm_job_name, slurm_job_id, running_on_hpc
):
    monkeypatch.setenv("PYMAPDL_RUNNING_ON_HPC", slurm_env_var)
    monkeypatch.setenv("SLURM_JOB_NAME", slurm_job_name)
    monkeypatch.setenv("SLURM_JOB_ID", slurm_job_id)

    flag = is_running_on_slurm(args={"running_on_hpc": running_on_hpc})

    if running_on_hpc is not True:
        assert not flag

    else:
        if slurm_env_var.lower() == "false":
            assert not flag

        else:
            if slurm_job_name != "" and slurm_job_id != "":
                assert flag
            else:
                assert not flag

    if ON_LOCAL:
        assert (
            launch_mapdl(
                running_on_hpc=running_on_hpc,
                _debug_no_launch=True,
            )["running_on_hpc"]
            == flag
        )


@pytest.mark.parametrize(
    "start_instance,context",
    [
        pytest.param(True, NullContext(), id="Boolean true"),
        pytest.param(False, NullContext(), id="Boolean false"),
        pytest.param("true", NullContext(), id="String true"),
        pytest.param("TRue", NullContext(), id="String true weird capitalization"),
    ],
)
def test_get_start_instance_argument(monkeypatch, start_instance, context):
    if "PYMAPDL_START_INSTANCE" in os.environ:
        monkeypatch.delenv("PYMAPDL_START_INSTANCE")
    with context:
        if "true" in str(start_instance).lower():
            assert get_start_instance(start_instance)
        else:
            assert not get_start_instance(start_instance)


@pytest.mark.parametrize(
    "start_instance, context",
    [
        pytest.param("true", NullContext()),
        pytest.param("TRue", NullContext()),
        pytest.param("False", NullContext()),
        pytest.param("FaLSE", NullContext()),
        pytest.param("asdf", pytest.raises(OSError)),
        pytest.param("1", pytest.raises(OSError)),
        pytest.param("", NullContext()),
    ],
)
def test_get_start_instance_envvar(monkeypatch, start_instance, context):
    monkeypatch.setenv("PYMAPDL_START_INSTANCE", start_instance)
    with context:
        if "true" in start_instance.lower() or start_instance == "":
            assert get_start_instance(start_instance=None)
        else:
            assert not get_start_instance(start_instance=None)


@requires("local")
@requires("ansys-tools-common")
@pytest.mark.parametrize("start_instance", [True, False])
def test_launcher_start_instance(monkeypatch, start_instance):
    if "PYMAPDL_START_INSTANCE" in os.environ:
        monkeypatch.delenv("PYMAPDL_START_INSTANCE")
    options = launch_mapdl(
        exec_file=find_mapdl()[0], start_instance=start_instance, _debug_no_launch=True
    )
    assert start_instance == options["start_instance"]


@pytest.mark.parametrize("start_instance", [None, True, False])
@pytest.mark.parametrize("start_instance_envvar", [None, True, False])
@pytest.mark.parametrize("ip", [None, "", "123.1.1.1"])
@pytest.mark.parametrize("ip_envvar", [None, "", "123.1.1.1"])
def test_ip_and_start_instance(
    monkeypatch, start_instance, start_instance_envvar, ip, ip_envvar
):
    # For more information, visit https://github.com/ansys/pymapdl/issues/2910

    ###################
    # Removing env var coming from CICD.
    if "PYMAPDL_START_INSTANCE" in os.environ:
        monkeypatch.delenv("PYMAPDL_START_INSTANCE")

    ###################
    # Injecting env vars for the test
    if start_instance_envvar is not None:
        monkeypatch.setenv("PYMAPDL_START_INSTANCE", str(start_instance_envvar))
    if ip_envvar is not None:
        monkeypatch.setenv("PYMAPDL_IP", str(ip_envvar))

    # Skip if PyMAPDL cannot detect where MAPDL is installed.
    if not _HAS_ATC and not os.environ.get("PYMAPDL_MAPDL_EXEC"):
        # if start_instance and not ip:
        with pytest.raises(
            ModuleNotFoundError,
            match="If you don't have 'ansys-tools-common' library installed, you need",
        ):
            options = launch_mapdl(
                exec_file=None,
                start_instance=start_instance,
                ip=ip,
                _debug_no_launch=True,
            )
        return  # Exit early the test

    ###################
    # Exception case: start_instance and ip are passed as args.
    if start_instance and ip:
        with pytest.raises(
            ValueError,
            match="When providing a value for the argument 'ip', the argument ",
        ):
            options = launch_mapdl(
                start_instance=start_instance,
                ip=ip,
                _debug_no_launch=True,
            )
        return  # Exit early the test

    ###################
    # Faking MAPDL launching and returning args
    if start_instance_envvar is not None and start_instance is True:
        context = pytest.warns(UserWarning)
    else:
        context = warnings.catch_warnings(record=True)

    with context:
        options = launch_mapdl(
            start_instance=start_instance,
            ip=ip,
            _debug_no_launch=True,
        )

    ###################
    # Checking logic
    # The start instance arg has precedence over the env var

    if start_instance is True:
        assert options["start_instance"]
    elif start_instance is False:
        assert not options["start_instance"]
    else:
        #  start_instance is None, checking env var:
        if ip or ip_envvar:
            assert options["start_instance"] is False

        elif start_instance_envvar is True:
            assert options["start_instance"] is True

        elif start_instance_envvar is False:
            assert options["start_instance"] is False

        else:
            # start_instance is None.
            # No IP env var or arg:
            if ip:
                # the ip is given either using the env var or the arg:
                assert not options["start_instance"]
            else:
                assert options["start_instance"]

    if ip_envvar:
        # Getting IP from env var
        assert options["ip"] == ip_envvar
    else:
        # From argument
        if ip:
            assert options["ip"] == ip
        else:
            # Using default
            assert options["ip"] in (LOCALHOST, "0.0.0.0", "127.0.0.1")


@patch("os.name", "nt")
@patch("psutil.cpu_count", lambda *args, **kwargs: 10)
def test_generate_mapdl_launch_command_windows():
    assert os.name == "nt"  # Checking mocking is properly done

    exec_file = "C:/Program Files/ANSYS Inc/v242/ansys/bin/winx64/ANSYS242.exe"
    jobname = "myjob"
    nproc = 10
    port = 1000
    ram = 2024
    additional_switches = "-my_add=switch"

    cmd = generate_mapdl_launch_command(
        exec_file=exec_file,
        jobname=jobname,
        nproc=nproc,
        port=port,
        ram=ram,
        additional_switches=additional_switches,
    )

    assert isinstance(cmd, list)

    assert f"{exec_file}" in cmd
    assert "-j" in cmd
    assert f"{jobname}" in cmd
    assert "-port" in cmd
    assert f"{port}" in cmd
    assert "-m" in cmd
    assert f"{ram}" in cmd
    assert "-np" in cmd
    assert f"{nproc}" in cmd
    assert "-grpc" in cmd
    assert f"{additional_switches}" in cmd
    assert "-b" in cmd
    assert "-i" in cmd
    assert ".__tmp__.inp" in cmd
    assert "-o" in cmd
    assert ".__tmp__.out" in cmd

    cmd = " ".join(cmd)
    assert f"{exec_file}" in cmd
    assert f" -j {jobname} " in cmd
    assert f" -port {port} " in cmd
    assert f" -m {ram} " in cmd
    assert f" -np {nproc} " in cmd
    assert " -grpc" in cmd
    assert f" {additional_switches} " in cmd
    assert f" -b -i .__tmp__.inp " in cmd
    assert f" -o .__tmp__.out " in cmd


@patch("os.name", "posix")
def test_generate_mapdl_launch_command_linux():
    assert os.name != "nt"  # Checking mocking is properly done

    exec_file = "/ansys_inc/v242/ansys/bin/ansys242"
    jobname = "myjob"
    nproc = 10
    port = 1000
    ram = 2024
    additional_switches = "-my_add=switch"

    cmd = generate_mapdl_launch_command(
        exec_file=exec_file,
        jobname=jobname,
        nproc=nproc,
        port=port,
        ram=ram,
        additional_switches=additional_switches,
    )
    assert isinstance(cmd, list)
    assert all([isinstance(each, str) for each in cmd])

    assert isinstance(cmd, list)

    assert f"{exec_file}" in cmd
    assert "-j" in cmd
    assert f"{jobname}" in cmd
    assert "-port" in cmd
    assert f"{port}" in cmd
    assert "-m" in cmd
    assert f"{ram}" in cmd
    assert "-np" in cmd
    assert f"{nproc}" in cmd
    assert "-grpc" in cmd
    assert f"{additional_switches}" in cmd

    assert "-b" not in cmd
    assert "-i" not in cmd
    assert ".__tmp__.inp" not in cmd
    assert "-o" not in cmd
    assert ".__tmp__.out" not in cmd

    cmd = " ".join(cmd)
    assert f"{exec_file} " in cmd
    assert f" -j {jobname} " in cmd
    assert f" -port {port} " in cmd
    assert f" -m {ram} " in cmd
    assert f" -np {nproc} " in cmd
    assert " -grpc" in cmd
    assert f" {additional_switches} " in cmd

    assert f" -i .__tmp__.inp " not in cmd
    assert f" -o .__tmp__.out " not in cmd


def test_generate_start_parameters_console():
    args = {"mode": "console", "start_timeout": 90}

    new_args = generate_start_parameters(args)
    assert "start_timeout" in new_args
    assert "ram" not in new_args
    assert "override" not in new_args
    assert "timeout" not in new_args


@patch("ansys.mapdl.core.launcher._HAS_ATC", False)
def test_get_exec_file(monkeypatch):
    monkeypatch.delenv("PYMAPDL_MAPDL_EXEC", False)

    args = {"exec_file": None, "start_instance": True}

    with pytest.raises(ModuleNotFoundError):
        get_exec_file(args)


def test_get_exec_file_not_found(monkeypatch):
    monkeypatch.delenv("PYMAPDL_MAPDL_EXEC", False)

    args = {"exec_file": "my/fake/path", "start_instance": True}

    with pytest.raises(FileNotFoundError):
        get_exec_file(args)


def _get_application_path(*args, **kwargs):
    return None


@requires("ansys-tools-common")
@patch("ansys.tools.common.path.path._get_application_path", _get_application_path)
def test_get_exec_file_not_found_two(monkeypatch):
    monkeypatch.delenv("PYMAPDL_MAPDL_EXEC", False)
    args = {"exec_file": None, "start_instance": True}
    with pytest.raises(
        FileNotFoundError, match="Invalid exec_file path or cannot load cached "
    ):
        get_exec_file(args)


@pytest.mark.parametrize("run_location", [None, True])
@pytest.mark.parametrize("remove_temp_dir_on_exit", [None, False, True])
def test_get_run_location(tmpdir, remove_temp_dir_on_exit, run_location):
    if run_location:
        new_path = os.path.join(str(tmpdir), "my_new_path")
        assert not os.path.exists(new_path)
    else:
        new_path = None

    args = {
        "run_location": new_path,
        "remove_temp_dir_on_exit": remove_temp_dir_on_exit,
    }

    get_run_location(args)

    assert os.path.exists(args["run_location"])

    assert "remove_temp_dir_on_exit" in args

    if run_location:
        assert not args["remove_temp_dir_on_exit"]
    elif remove_temp_dir_on_exit:
        assert args["remove_temp_dir_on_exit"]
    else:
        assert not args["remove_temp_dir_on_exit"]


def fake_os_access(*args, **kwargs):
    return False


@patch("os.access", lambda *args, **kwargs: False)
def test_get_run_location_no_access(tmpdir):
    with pytest.raises(IOError, match="Unable to write to ``run_location``:"):
        get_run_location({"run_location": str(tmpdir)})


@pytest.mark.parametrize(
    "args,match",
    [
        [
            {"start_instance": True, "ip": True, "on_pool": False},
            "When providing a value for the argument 'ip', the argument",
        ],
        [
            {"exec_file": True, "version": True},
            "Cannot specify both ``exec_file`` and ``version``.",
        ],
        [
            {"scheduler_options": True},
            "PyMAPDL does not read the number of cores from the 'scheduler_options'.",
        ],
        [
            {"launch_on_hpc": True, "ip": "111.22.33.44"},
            "PyMAPDL cannot ensure a specific IP will be used when launching",
        ],
    ],
)
def test_pre_check_args(args, match):
    with pytest.raises(ValueError, match=match):
        launch_mapdl(**args)


def test_remove_err_files(tmpdir):
    run_location = str(tmpdir)
    jobname = "jobname"
    err_file = os.path.join(run_location, f"{jobname}.err")
    with open(err_file, "w") as fid:
        fid.write("Dummy")

    assert os.path.isfile(err_file)
    remove_err_files(run_location, jobname)
    assert not os.path.isfile(err_file)


def myosremove(*args, **kwargs):
    raise IOError("Generic error")


@patch("os.remove", myosremove)
def test_remove_err_files_fail(tmpdir):
    run_location = str(tmpdir)
    jobname = "jobname"
    err_file = os.path.join(run_location, f"{jobname}.err")
    with open(err_file, "w") as fid:
        fid.write("Dummy")

    assert os.path.isfile(err_file)
    with pytest.raises(IOError):
        remove_err_files(run_location, jobname)
    assert os.path.isfile(err_file)


# testing on windows to account for temp file
@patch("os.name", "nt")
@pytest.mark.parametrize("launch_on_hpc", [None, False, True])
@patch("subprocess.Popen", lambda *args, **kwargs: kwargs)
def test_launch_grpc(tmpdir, launch_on_hpc):
    if launch_on_hpc:
        cmd = ["sbatch", "--wrap", "'ansys.exe -b -i my_input.inp -o my_output.inp'"]
    else:
        cmd = "ansys.exe -b -i my_input.inp -o my_output.inp".split(" ")
    run_location = str(tmpdir)
    kwargs = launch_grpc(cmd, run_location, launch_on_hpc=launch_on_hpc)

    inp_file = os.path.join(run_location, "my_input.inp")

    if launch_on_hpc:
        assert "sbatch" in kwargs["args"]
        assert "--wrap" in kwargs["args"]
        assert " ".join(cmd) == " ".join(kwargs["args"])
    else:
        assert cmd == kwargs["args"]
        assert os.path.exists(inp_file)
        with open(inp_file, "r") as fid:
            assert "FINISH" in fid.read()

    assert not kwargs["shell"]
    assert "TRUE" == kwargs["env"].pop("ANS_CMD_NODIAG")
    assert not kwargs["env"]
    assert isinstance(kwargs["stdin"], type(subprocess.DEVNULL))
    assert isinstance(kwargs["stdout"], type(subprocess.PIPE))
    assert isinstance(kwargs["stderr"], type(subprocess.PIPE))


@patch("psutil.cpu_count", lambda *args, **kwags: 5)
@pytest.mark.parametrize("arg", [None, 3, 10])
@pytest.mark.parametrize("env", [None, 3, 10])
def test_get_cpus(monkeypatch, arg, env):
    if env:
        monkeypatch.setenv("PYMAPDL_NPROC", str(env))

    context = NullContext()
    cores_machine = psutil.cpu_count(logical=False)  # it is patched

    if (arg and arg > cores_machine) or (arg is None and env and env > cores_machine):
        context = pytest.raises(NotEnoughResources)

    args = {"nproc": arg, "running_on_hpc": False}
    with context:
        get_cpus(args)

    if arg:
        assert args["nproc"] == arg
    elif env:
        assert args["nproc"] == env
    else:
        assert args["nproc"] == 2


@patch("psutil.cpu_count", lambda *args, **kwags: 1)
def test_get_cpus_min(monkeypatch):
    if "PYMAPDL_NPROC" in os.environ:
        monkeypatch.delenv("PYMAPDL_NPROC")

    args = {"nproc": None, "running_on_hpc": False}
    get_cpus(args)
    assert args["nproc"] == 1


@pytest.mark.parametrize(
    "scheduler_options",
    [None, "-N 10", {"N": 10, "nodes": 10, "-tasks": 3, "--ntask-per-node": 2}],
)
def test_generate_sbatch_command(scheduler_options):
    cmd = [
        "/ansys_inc/v242/ansys/bin/ansys242",
        "-j",
        "myjob",
        "-np",
        "10",
        "-m",
        "1024",
        "-port",
        "50052",
        "-my_add=switch",
    ]

    cmd_post = generate_sbatch_command(cmd, scheduler_options)

    assert cmd_post[0] == "sbatch"
    if scheduler_options:
        if isinstance(scheduler_options, dict):
            assert (
                cmd_post[1] == "-N='10' --nodes='10' --tasks='3' --ntask-per-node='2'"
            )
        else:
            assert cmd_post[1] == scheduler_options

    assert cmd_post[-2] == "--wrap"
    assert cmd_post[-1] == f"""'{" ".join(cmd)}'"""


@pytest.mark.parametrize(
    "scheduler_options",
    [None, "--wrap '/bin/bash", {"--wrap": "/bin/bash", "nodes": 10}],
)
def test_generate_sbatch_wrap_in_arg(scheduler_options):
    cmd = ["/ansys_inc/v242/ansys/bin/ansys242", "-grpc"]
    if scheduler_options:
        context = pytest.raises(
            ValueError,
            match="The sbatch argument 'wrap' is used by PyMAPDL to submit the job.",
        )
    else:
        context = NullContext()

    with context:
        cmd_post = generate_sbatch_command(cmd, scheduler_options)
        assert cmd[0] in cmd_post[-1]


def myfakegethostbyname(*args, **kwargs):
    return "mycoolhostname"


def myfakegethostbynameIP(*args, **kwargs):
    return "123.45.67.89"


@pytest.mark.parametrize(
    "message_stdout, message_stderr",
    [
        ["Submitted batch job 1001", ""],
        ["Submission failed", "Something very bad happened"],
    ],
)
@patch("socket.gethostbyname", myfakegethostbynameIP)
@patch("ansys.mapdl.core.launcher.get_hostname_host_cluster", myfakegethostbyname)
def test_check_mapdl_launch_on_hpc(message_stdout, message_stderr):

    process = get_fake_process(message_stdout, message_stderr)

    start_parm = {}
    if "Submitted batch job" in message_stdout:
        context = NullContext()

    else:
        context = pytest.raises(
            MapdlDidNotStart,
            match=f"stdout:\n{message_stdout}\nstderr:\n{message_stderr}",
        )

    with context:
        assert check_mapdl_launch_on_hpc(process) == 1001


@patch("ansys.mapdl.core.Mapdl._exit_mapdl", lambda *args, **kwargs: None)
@patch("ansys.mapdl.core.mapdl_grpc.MapdlGrpc.kill_job")
def test_exit_job(mock_popen, mapdl, cleared):
    # Setting to exit
    mapdl._mapdl_on_hpc = True
    mapdl.finish_job_on_exit = True
    prev_rem = mapdl.remove_temp_dir_on_exit
    mapdl.remove_temp_dir_on_exit = False

    mock_popen.return_value = lambda *args, **kwargs: True

    mapdl._jobid = 1001
    assert mapdl.jobid == 1001

    mapdl.exit(force=True)

    # Returning to state
    mapdl._jobid = None
    mapdl._exited = False
    mapdl._mapdl_on_hpc = False
    mapdl.finish_job_on_exit = True
    mapdl.remove_temp_dir_on_exit = prev_rem

    # Checking
    mock_popen.assert_called_once_with(1001)


@requires("ansys-tools-common")
@patch(
    "ansys.tools.common.path.path._get_application_path",
    lambda *args, **kwargs: "path/to/mapdl/executable",
)
@patch("ansys.tools.common.path.path._version_from_path", lambda *args, **kwargs: 242)
@stack(*PATCH_MAPDL_START)
@patch("ansys.mapdl.core.launcher.launch_grpc")
@patch("ansys.mapdl.core.launcher.send_scontrol")
def test_launch_on_hpc_found_ansys(mck_ssctrl, mck_launch_grpc, monkeypatch):
    monkeypatch.delenv("PYMAPDL_START_INSTANCE", False)

    mck_launch_grpc.return_value = get_fake_process("Submitted batch job 1001")
    mck_ssctrl.return_value = get_fake_process(
        "a long scontrol...\nJobState=RUNNING\n...\nBatchHost=myhostname\n...\nin message"
    )

    mapdl_a = launch_mapdl(
        launch_on_hpc=True,
    )
    with patch.object(mapdl_a, "kill_job") as mck_del:
        mapdl_a.exit()
        mck_del.assert_called_once()

    mck_launch_grpc.assert_called_once()
    cmd = mck_launch_grpc.call_args_list[0][1]["cmd"]
    env_vars = mck_launch_grpc.call_args_list[0][1]["env_vars"]

    assert "sbatch" in cmd
    assert "--wrap" in cmd
    assert "path/to/mapdl/executable" in cmd[-1]
    assert "-grpc" in cmd[-1]

    assert env_vars.get("ANS_MULTIPLE_NODES") == "1"
    assert env_vars.get("HYDRA_BOOTSTRAP") == "slurm"

    mck_ssctrl.assert_called_once()
    assert "show" in mck_ssctrl.call_args[0][0]
    assert "1001" in mck_ssctrl.call_args[0][0]


@stack(*PATCH_MAPDL_START)
@patch("ansys.mapdl.core.mapdl_grpc.MapdlGrpc.kill_job")
@patch("ansys.mapdl.core.launcher.launch_grpc")
@patch("ansys.mapdl.core.launcher.send_scontrol")
def test_launch_on_hpc_not_found_ansys(mck_sc, mck_lgrpc, mck_kj, monkeypatch):
    monkeypatch.delenv("PYMAPDL_START_INSTANCE", False)
    exec_file = "path/to/mapdl/v242/executable/ansys242"

    mck_lgrpc.return_value = get_fake_process("Submitted batch job 1001")
    mck_kj.return_value = None
    mck_sc.return_value = get_fake_process(
        "a long scontrol...\nJobState=RUNNING\n...\nBatchHost=myhostname\n...\nin message"
    )

    if TESTING_MINIMAL:
        context = NullContext()
    else:
        context = pytest.warns(
            UserWarning, match="PyMAPDL could not find the ANSYS executable."
        )

    with context:
        mapdl = launch_mapdl(
            launch_on_hpc=True,
            exec_file=exec_file,
        )
        with patch.object(mapdl, "kill_job") as mck_kj:
            mapdl.exit()
            del mapdl
            mck_kj.assert_called_once()

    mck_lgrpc.assert_called_once()
    cmd = mck_lgrpc.call_args_list[0][1]["cmd"]
    env_vars = mck_lgrpc.call_args_list[0][1]["env_vars"]

    assert "sbatch" in cmd
    assert "--wrap" in cmd
    assert exec_file in cmd[-1]
    assert "-grpc" in cmd[-1]

    assert env_vars.get("ANS_MULTIPLE_NODES") == "1"
    assert env_vars.get("HYDRA_BOOTSTRAP") == "slurm"

    mck_sc.assert_called_once()
    assert "show" in mck_sc.call_args[0][0]
    assert "1001" in mck_sc.call_args[0][0]


def test_launch_on_hpc_exception_launch_mapdl(monkeypatch):
    monkeypatch.delenv("PYMAPDL_START_INSTANCE", False)
    exec_file = "path/to/mapdl/v242/ansys/bin/executable/ansys242"

    process = get_fake_process("ERROR")

    with patch("ansys.mapdl.core.launcher.launch_grpc") as mock_launch_grpc:
        with patch("ansys.mapdl.core.launcher.kill_job") as mock_popen:

            mock_launch_grpc.return_value = process

            with pytest.raises(
                Exception, match="PyMAPDL failed to submit the sbatch job:"
            ):
                launch_mapdl(
                    launch_on_hpc=True,
                    exec_file=exec_file,
                )

    mock_launch_grpc.assert_called_once()
    cmd = mock_launch_grpc.call_args_list[0][1]["cmd"]
    env_vars = mock_launch_grpc.call_args_list[0][1]["env_vars"]

    assert "sbatch" in cmd
    assert "--wrap" in cmd
    assert exec_file in cmd[-1]
    assert "-grpc" in cmd[-1]

    assert env_vars.get("ANS_MULTIPLE_NODES") == "1"
    assert env_vars.get("HYDRA_BOOTSTRAP") == "slurm"

    # Popen wi
    mock_popen.assert_not_called()


def test_launch_on_hpc_exception_successfull_sbatch(monkeypatch):
    monkeypatch.delenv("PYMAPDL_START_INSTANCE", False)
    exec_file = "path/to/mapdl/v242/ansys/bin/executable/ansys242"

    def raise_exception(*args, **kwargs):
        raise Exception("Fake exception when launching MAPDL")

    process_launch_grpc = get_fake_process("Submitted batch job 1001")

    process_scontrol = get_fake_process("Submitted batch job 1001")
    process_scontrol.stdout.read = raise_exception

    with patch("ansys.mapdl.core.launcher.launch_grpc") as mock_launch_grpc:
        with patch("ansys.mapdl.core.launcher.send_scontrol") as mock_scontrol:
            with patch("ansys.mapdl.core.launcher.kill_job") as mock_kill_job:

                mock_launch_grpc.return_value = process_launch_grpc
                mock_scontrol.return_value = process_scontrol

                with pytest.raises(
                    Exception, match="Fake exception when launching MAPDL"
                ):
                    launch_mapdl(
                        launch_on_hpc=True,
                        exec_file=exec_file,
                        replace_env_vars={"myenvvar": "myenvvarvalue"},
                    )

    mock_launch_grpc.assert_called_once()
    cmd = mock_launch_grpc.call_args_list[0][1]["cmd"]

    assert "sbatch" in cmd
    assert "--wrap" in cmd
    assert exec_file in cmd[-1]
    assert "-grpc" in cmd[-1]

    envvars = mock_launch_grpc.call_args_list[0][1]["env_vars"]

    assert envvars["ANS_MULTIPLE_NODES"] == "1"
    assert envvars["HYDRA_BOOTSTRAP"] == "slurm"
    assert envvars["myenvvar"] == "myenvvarvalue"

    mock_scontrol.assert_called_once()
    args = mock_scontrol.call_args_list[0][0][0]

    assert "show" in args
    assert "jobid" in args
    assert "1001" in args

    mock_kill_job.assert_called_once()


@pytest.mark.parametrize(
    "args,context",
    [
        [
            {"nproc": 10, "mode": "console"},
            pytest.raises(
                ValueError,
                match="The only mode allowed for launch MAPDL on an HPC cluster is gRPC.",
            ),
        ],
        [
            {"nproc": 10, "ip": "123.11.22.33"},
            pytest.raises(
                ValueError,
                match="PyMAPDL cannot ensure a specific IP will be used when launching MAPDL on a cluster",
            ),
        ],
        [
            {"nproc": 10, "start_instance": False},
            pytest.raises(
                ValueError,
                match="The 'start_instance' argument must be 'True' when launching on HPC.",
            ),
        ],
        [{"nproc": 10}, NullContext()],
    ],
)
@patch("ansys.mapdl.core.launcher.launch_mapdl", lambda *args, **kwargs: kwargs)
def test_launch_mapdl_on_cluster_exceptions(args, context):
    with context:
        ret = launch_mapdl_on_cluster(**args)
        assert ret["launch_on_hpc"]
        assert ret["nproc"] == 10


@patch(
    "socket.gethostbyname",
    lambda *args, **kwargs: "123.45.67.89" if args[0] != LOCALHOST else LOCALHOST,
)
@pytest.mark.parametrize(
    "ip,ip_env",
    [[None, None], [None, "123.45.67.89"], ["123.45.67.89", "111.22.33.44"]],
)
def test_get_ip(monkeypatch, ip, ip_env):
    monkeypatch.delenv("PYMAPDL_IP", False)
    if ip_env:
        monkeypatch.setenv("PYMAPDL_IP", ip_env)
    args = {"ip": ip}

    get_ip(args)

    if ip:
        assert args["ip"] == ip
    else:
        if ip_env:
            assert args["ip"] == ip_env
        else:
            assert args["ip"] == LOCALHOST


@pytest.mark.parametrize(
    "port,port_envvar,start_instance,port_busy,result",
    (
        [None, None, True, False, 50052],  # Standard case
        [None, None, True, True, 50054],
        [None, 50053, True, True, 50053],
        [None, 50053, False, False, 50053],
        [50054, 50053, True, False, 50054],
        [50054, 50053, True, False, 50054],
        [50054, None, False, False, 50054],
    ),
)
def test_get_port(monkeypatch, port, port_envvar, start_instance, port_busy, result):
    # Settings
    pymapdl._LOCAL_PORTS = []  # Resetting

    monkeypatch.delenv("PYMAPDL_PORT", False)
    if port_envvar:
        monkeypatch.setenv("PYMAPDL_PORT", str(port_envvar))

    # Testing
    if port_busy:
        # Success after the second retry, it should go up to 2.
        # But for some reason, it goes up 3.
        side_effect = [True, True, False]
    else:
        side_effect = [False]

    context = patch("ansys.mapdl.core.launcher.port_in_use", side_effect=side_effect)

    with context:
        assert get_port(port, start_instance) == result


@pytest.mark.parametrize("stdout", ["Submitted batch job 1001", "Something bad"])
def test_get_jobid(stdout):
    if "1001" in stdout:
        context = NullContext()
    else:
        context = pytest.raises(
            ValueError, match="PyMAPDL could not retrieve the job id"
        )

    with context:
        jobid = get_jobid(stdout)
        assert jobid == 1001


@patch("socket.gethostbyname", lambda *args, **kwargs: "111.22.33.44")
@pytest.mark.parametrize(
    "jobid,timeout,time_to_stop,state,hostname, hostname_msg, raises",
    [
        [1001, 30, 2, "RUNNING", "myhostname", "BatchHost=myhostname", None],
        [
            1002,
            2,
            3,
            "CONFIGURING",
            "otherhostname",
            "BatchHost=otherhostname",
            MapdlDidNotStart,
        ],
        [1002, 2, 3, "CONFIGURING", "", "BatchHost=", MapdlDidNotStart],
        [1002, 2, 3, "CONFIGURING", None, "Batch", MapdlDidNotStart],
    ],
)
def test_get_hostname_host_cluster(
    jobid, timeout, time_to_stop, state, hostname, hostname_msg, raises
):
    def fake_proc(*args, **kwargs):
        assert f"show jobid -dd {jobid}" == args[0]
        return get_fake_process(
            f"a long scontrol...\nJobState={state}\n...\n{hostname_msg}\n...\nin message",
            "",
            time_to_stop,
        )

    with patch("ansys.mapdl.core.launcher.send_scontrol", fake_proc) as mck_sc:

        if raises:
            context = pytest.raises(raises)
        else:
            context = NullContext()

        with context as excinfo:
            batchhost, batchhost_ip = get_hostname_host_cluster(
                job_id=jobid, timeout=timeout
            )

        if raises:
            assert f"The HPC job (id: {jobid})" in excinfo.value.args[0]
            assert f"(timeout={timeout})." in excinfo.value.args[0]
            assert f"The job state is '{state}'. " in excinfo.value.args[0]

            if hostname:
                assert f"The BatchHost for this job is '{hostname}'"
            else:
                assert (
                    "PyMAPDL couldn't get the BatchHost hostname"
                    in excinfo.value.args[0]
                )

        else:
            assert batchhost == "myhostname"
            assert batchhost_ip == "111.22.33.44"


@requires("ansys-tools-common")
@patch(
    "ansys.tools.common.path.path._version_from_path",
    side_effect=lambda *args, **kwargs: 201,
)
@patch("ansys.mapdl.core._HAS_ATC", True)
def test_get_version_version_error(monkeypatch):
    monkeypatch.delenv("PYMAPDL_MAPDL_VERSION", False)

    with pytest.raises(
        VersionError, match="The MAPDL gRPC interface requires MAPDL 20.2 or later"
    ):
        get_version(None, "/path/to/executable")


@pytest.mark.parametrize("version", [211, 221, 232])
def test_get_version_env_var(monkeypatch, version):
    monkeypatch.setenv("PYMAPDL_MAPDL_VERSION", str(version))

    assert version == get_version(None)
    assert version != get_version(241)


@pytest.mark.parametrize(
    "mode, version, osname, context, res",
    [
        [None, None, None, NullContext(), "grpc"],  # default
        [
            "grpc",
            201,
            "nt",
            pytest.raises(
                VersionError, match="gRPC mode requires MAPDL 2020R2 or newer on Window"
            ),
            None,
        ],
        [
            "grpc",
            202,
            "posix",
            pytest.raises(
                VersionError, match="gRPC mode requires MAPDL 2021R1 or newer on Linux."
            ),
            None,
        ],
        ["grpc", 212, "nt", NullContext(), "grpc"],
        ["grpc", 221, "posix", NullContext(), "grpc"],
        ["grpc", 221, "nt", NullContext(), "grpc"],
        [
            "console",
            221,
            "nt",
            pytest.raises(ValueError, match="Console mode requires Linux."),
            None,
        ],
        [
            "console",
            221,
            "posix",
            pytest.warns(
                UserWarning,
                match="Console mode not recommended in MAPDL 2021R1 or newer.",
            ),
            "console",
        ],
        [
            "nomode",
            221,
            "posix",
            pytest.raises(ValueError, match=f'Invalid MAPDL server mode "nomode"'),
            None,
        ],
        [None, 211, "posix", NullContext(), "grpc"],
        [None, 211, "nt", NullContext(), "grpc"],
        [None, 202, "nt", NullContext(), "grpc"],
        [
            None,
            201,
            "nt",
            pytest.raises(VersionError, match="Running MAPDL as a service requires"),
            None,
        ],
        [None, 202, "posix", NullContext(), "console"],
        [None, 201, "posix", NullContext(), "console"],
        [
            None,
            110,
            "posix",
            pytest.warns(
                UserWarning,
                match="MAPDL as a service has not been tested on MAPDL < v13",
            ),
            "console",
        ],
        [
            None,
            110,
            "nt",
            pytest.raises(VersionError, match="Running MAPDL as a service requires"),
            None,
        ],
        [
            "anymode",
            None,
            "posix",
            pytest.warns(UserWarning, match="PyMAPDL couldn't detect MAPDL version"),
            "anymode",
        ],
    ],
)
def test_check_mode(mode, version, osname, context, res):
    with patch("os.name", osname):
        with context as cnt:
            assert res == check_mode(mode, version)


@pytest.mark.parametrize("jobid", [1001, 2002])
@patch("subprocess.Popen", lambda *args, **kwargs: None)
def test_kill_job(jobid):
    with patch("ansys.mapdl.core.launcher.submitter") as mck_sub:
        assert kill_job(jobid) is None
        mck_sub.assert_called_once()
        arg = mck_sub.call_args_list[0][0][0]
        assert arg[0] == "scancel"
        assert arg[1] == str(jobid)


@pytest.mark.parametrize("jobid", [1001, 2002])
@patch(
    "ansys.mapdl.core.launcher.submitter", lambda *args, **kwargs: kwargs
)  # return command
def test_send_scontrol(jobid):
    with patch("ansys.mapdl.core.launcher.submitter") as mck_sub:
        args = f"my args {jobid}"
        assert send_scontrol(args)

        mck_sub.assert_called_once()
        arg = mck_sub.call_args_list[0][0][0]
        assert " ".join(arg) == f"scontrol my args {jobid}"
        assert "scontrol" in arg
        assert f"{jobid}" in arg


@pytest.mark.parametrize(
    "cmd,executable,shell,cwd,stdin,stdout,stderr,envvars",
    [
        ["mycmd", None, True, "my_cwd", None, None, None, None],
        [["my", "cmd"], None, True, "my_cwd", None, None, None, None],
        [
            ["mycmd"],
            "exec",
            False,
            "my_other_cwd",
            "other_obj",
            "other_obj",
            "other_obj",
            {"aaa": 1},
        ],
        [
            ["my", "cmd"],
            "exec",
            False,
            "my_single_cwd",
            "other_obj",
            "other_obj",
            "other_obj",
            {"a": "b", "b": "c"},
        ],
    ],
)
def test_submitter(cmd, executable, shell, cwd, stdin, stdout, stderr, envvars):
    def return_everything(*arg, **kwags):
        return arg, kwags

    with patch("subprocess.Popen", return_everything) as mck_popen:
        args, kwargs = submitter(
            cmd=cmd,
            executable=executable,
            shell=shell,
            cwd=cwd,
            stdin=stdin,
            stdout=stdout,
            stderr=stderr,
            env_vars=envvars,
        )

        if executable:
            if isinstance(cmd, str):
                assert kwargs["args"] == [executable, cmd]
            else:  # list
                assert kwargs["args"] == [executable] + cmd
        else:
            assert kwargs["args"] == cmd

        assert kwargs["shell"] == shell
        assert kwargs["cwd"] == cwd

        if stdin:
            assert kwargs["stdin"] == stdin
        else:
            assert isinstance(kwargs["stdin"], type(subprocess.DEVNULL))

        if stdout:
            assert kwargs["stdout"] == stdout
        else:
            assert isinstance(kwargs["stdout"], type(subprocess.PIPE))

        if stderr:
            assert kwargs["stderr"] == stderr
        else:
            assert isinstance(kwargs["stderr"], type(subprocess.PIPE))

        assert kwargs["env"] == envvars


@requires("ansys-tools-common")
@patch(
    "ansys.tools.common.path.path._get_application_path",
    lambda *args, **kwargs: "path/to/mapdl/executable",
)
@patch("ansys.tools.common.path.path._version_from_path", lambda *args, **kwargs: 242)
@stack(*PATCH_MAPDL)
@pytest.mark.parametrize(
    "arg,value,method",
    [
        ("start_timeout", 88, "_timeout"),
        ("start_timeout", 1099, "_timeout"),
        ("cleanup_on_exit", False, "_cleanup"),
        ("cleanup_on_exit", True, "_cleanup"),
        ("jobname", "myjobnamestrange", "_jobname"),
        ("jobid", 1088, "_jobid"),
        ("finish_job_on_exit", True, "finish_job_on_exit"),
        ("finish_job_on_exit", False, "finish_job_on_exit"),
    ],
)
def test_args_pass(monkeypatch, arg, value, method):
    monkeypatch.delenv("PYMAPDL_START_INSTANCE", False)

    kwargs = {arg: value}

    mapdl = launch_mapdl(**kwargs)
    meth = getattr(mapdl, method)
    assert meth == value

    mapdl._ctrl = lambda *args, **kwargs: None
    mapdl.kill_job = lambda *args, **kwargs: None
    del mapdl


def test_check_has_mapdl():
    if TESTING_MINIMAL:
        assert check_has_mapdl() is False
    else:
        assert check_has_mapdl() == ON_LOCAL


def raising():
    raise Exception("An error")


@patch("ansys.mapdl.core.launcher.check_valid_ansys", raising)
def test_check_has_mapdl_failed():
    assert check_has_mapdl() is False


@requires("local")
@patch("ansys.mapdl.core.launcher._is_ubuntu", lambda *args, **kwargs: True)
@patch("ansys.mapdl.core.launcher.check_mapdl_launch", lambda *args, **kwargs: None)
def test_mapdl_output_pass_arg(tmpdir):
    def submitter(*args, **kwargs):
        from _io import FileIO

        # Checking we are passing the arguments
        assert isinstance(kwargs["stdout"], FileIO)
        assert kwargs["stderr"] is subprocess.STDOUT

        return

    with patch("ansys.mapdl.core.launcher.submitter", submitter) as mck_sub:
        mapdl_output = os.path.join(tmpdir, "apdl.txt")
        args = launch_mapdl(just_launch=True, mapdl_output=mapdl_output)

    assert isinstance(args, list)


@requires("local")
@requires("nostudent")
@requires("grpc")
def test_mapdl_output(tmpdir):
    mapdl_output = os.path.join(tmpdir, "apdl.txt")
    mapdl = launch_mapdl(mapdl_output=mapdl_output, port=50058)

    assert os.path.exists(mapdl_output)

    mapdl.prep7()
    mapdl.exit(force=True)

    with open(mapdl_output, "r") as fid:
        content = fid.read()

    assert "Beta activation of the GRPC server." in content
    assert "Server listening on" in content
    try:
        # before gRPC transport updates
        assert "### START GRPC SERVER      ###" in content
    except AssertionError:
        assert "GRPC SERVER STARTED" in content
        assert mapdl.transport_mode.upper() in content
        assert "Transport Mode" in content


def test_check_server_is_alive_no_queue():
    from ansys.mapdl.core.launcher import _check_server_is_alive

    assert _check_server_is_alive(None, 30) is None


def test_get_std_output_no_queue():
    from ansys.mapdl.core.launcher import _get_std_output

    assert _get_std_output(None, 30) == ""


def test_create_queue_for_std_no_queue():
    from ansys.mapdl.core.launcher import _create_queue_for_std

    assert _create_queue_for_std(None) == (None, None)


def test_inject_additional_switches(monkeypatch):
    """
    Test the inject_additional_switches function.
    """
    envvar = "-my-add=switch --other_switch -b"
    monkeypatch.setenv("PYMAPDL_ADDITIONAL_SWITCHES", envvar)
    args = {"additional_switches": "-my_add=switch --other_switch -b"}

    new_args = inject_additional_switches(args)
    assert args["additional_switches"] in new_args["additional_switches"]
    # The env var is ignored if the argument is used
    assert envvar not in new_args["additional_switches"]


@pytest.mark.parametrize(
    "msg,match,exception_type",
    [
        (
            "mpirun: command not found",
            "Please ensure that MPI is installed and configured correctly",
            IncorrectMPIConfigurationError,
        ),
        (
            "ERROR - ANSYS license not available",
            "Please ensure that you have a valid license",
            NotAvailableLicenses,
        ),
        (
            "Other message",
            "Other message",
            # This will raise a generic Exception
            Exception,
        ),
    ],
)
def test_handle_launch_exceptions(msg, match, exception_type):
    from ansys.mapdl.core.launcher import handle_launch_exceptions

    exception = exception_type(msg)
    with pytest.raises(exception_type, match=match):
        raise handle_launch_exceptions(exception)


def test_env_vars_propagation_in_launch_mapdl():
    """Test that env_vars are propagated to start_parm in launch_mapdl."""
    env_vars = {"MY_VAR": "test_value", "ANOTHER_VAR": "another_value"}

    args = launch_mapdl(
        env_vars=env_vars,
        _debug_no_launch=True,
    )

    # Check that env_vars are in the returned args
    assert "env_vars" in args
    assert args["env_vars"]["MY_VAR"] == "test_value"
    assert args["env_vars"]["ANOTHER_VAR"] == "another_value"


def test_env_vars_with_slurm_bootstrap(monkeypatch):
    """Test that SLURM env_vars are set correctly when launch_on_hpc is True."""
    # This test verifies that when replace_env_vars is used with launch_on_hpc,
    # SLURM-specific environment variables are added
    monkeypatch.delenv("PYMAPDL_START_INSTANCE", False)

    env_vars_input = {"CUSTOM_VAR": "custom_value"}

    # Capture what env_vars are passed to launch_grpc
    captured_env_vars = None

    def mock_launch_grpc(cmd, run_location, env_vars=None, **kwargs):
        nonlocal captured_env_vars
        captured_env_vars = env_vars
        # Mock process object
        from tests.test_launcher import get_fake_process

        return get_fake_process("Submitted batch job 1001")

    with (
        patch("ansys.mapdl.core.launcher.launch_grpc", mock_launch_grpc),
        patch("ansys.mapdl.core.launcher.send_scontrol") as mock_scontrol,
        patch("ansys.mapdl.core.launcher.kill_job"),
    ):
        # Mock scontrol to avoid timeout
        mock_scontrol.return_value = get_fake_process(
            "JobState=RUNNING\nBatchHost=testhost\n"
        )

        try:
            launch_mapdl(
                launch_on_hpc=True,
                replace_env_vars=env_vars_input,  # Use replace_env_vars instead of env_vars
                exec_file="/fake/path/to/ansys242",
                nproc=2,
            )
        except Exception:  # nosec B703
            # We expect this to fail, we just want to capture env_vars
            pass

    # Verify the env_vars that were passed to launch_grpc
    assert captured_env_vars is not None
    assert "CUSTOM_VAR" in captured_env_vars
    assert captured_env_vars["CUSTOM_VAR"] == "custom_value"
    assert captured_env_vars["ANS_MULTIPLE_NODES"] == "1"
    assert captured_env_vars["HYDRA_BOOTSTRAP"] == "slurm"


def test_mapdl_grpc_launch_uses_provided_start_parm():
    """Test that MapdlGrpc._launch uses provided start_parm over instance _start_parm."""
    from ansys.mapdl.core.mapdl_grpc import MapdlGrpc

    # Create mock instance
    mapdl_grpc = Mock(spec=MapdlGrpc)
    mapdl_grpc._exited = True
    mapdl_grpc._local = True  # Add _local attribute
    mapdl_grpc._start_parm = {
        "exec_file": "/original/path/to/ansys242",
        "jobname": "original_job",
        "nproc": 2,
        "ram": 1024,
        "port": 50052,
        "additional_switches": "",
        "mode": "grpc",
        "run_location": "/default/run/location",
    }
    mapdl_grpc._env_vars = None
    mapdl_grpc._connect = MagicMock()
    mapdl_grpc._mapdl_process = None  # Add _mapdl_process attribute

    # Custom start_parm that should be used
    custom_start_parm = {
        "exec_file": "/custom/path/to/ansys242",
        "jobname": "custom_job",
        "nproc": 4,
        "ram": 2048,
        "port": 50053,
        "additional_switches": "-custom",
        "mode": "grpc",
        "env_vars": {"CUSTOM_VAR": "custom_value"},
        "run_location": "/custom/run/location",
    }

    # Mock the launch_grpc function to capture what parameters are used
    # Note: launch_grpc is in launcher module, not mapdl_grpc module
    with patch("ansys.mapdl.core.launcher.launch_grpc") as mock_launch_grpc:
        # Bind the real _launch method
        mapdl_grpc._launch = MapdlGrpc._launch.__get__(mapdl_grpc, type(mapdl_grpc))

        # Call _launch with custom start_parm
        mapdl_grpc._launch(start_parm=custom_start_parm, timeout=10)

        # Verify launch_grpc was called
        mock_launch_grpc.assert_called_once()

        # Get the cmd argument passed to launch_grpc
        call_args = mock_launch_grpc.call_args
        cmd_used = call_args[1]["cmd"]

        # Verify the command uses custom_start_parm values
        assert "/custom/path/to/ansys242" in " ".join(cmd_used)
        assert "custom_job" in " ".join(cmd_used)


def test_open_gui_with_mocked_call(mapdl, fake_local_mapdl):
    """Test that open_gui uses the correct exec_file with mocked subprocess.call."""
    from contextlib import ExitStack

    custom_exec_file = "/custom/test/path/ansys242"
    captured_call_args = None

    def mock_call(*args, **kwargs):
        nonlocal captured_call_args
        captured_call_args = args[0] if args else None
        return 0

    with ExitStack() as stack:
        # Mock _local to True so open_gui doesn't raise "can only be called from local"
        stack.enter_context(patch.object(mapdl, "_local", True))

        # Mock pathlib.Path to return a mock that has is_file() return True
        mock_path = MagicMock()
        mock_path.is_file.return_value = True
        stack.enter_context(
            patch("ansys.mapdl.core.mapdl_core.pathlib.Path", return_value=mock_path)
        )

        # Mock the call function imported in mapdl_core
        stack.enter_context(
            patch("ansys.mapdl.core.mapdl_core.call", side_effect=mock_call)
        )

        # IMPORTANT: Mock exit, finish, save, _launch, resume to prevent killing the MAPDL instance
        stack.enter_context(patch.object(mapdl, "exit"))
        stack.enter_context(patch.object(mapdl, "finish"))
        stack.enter_context(patch.object(mapdl, "save"))
        stack.enter_context(patch.object(mapdl, "_cache_routine"))
        stack.enter_context(patch.object(mapdl, "_launch"))
        stack.enter_context(patch.object(mapdl, "resume"))

        try:
            # Call open_gui with custom exec_file
            mapdl.open_gui(exec_file=custom_exec_file, inplace=True)
        except Exception:  # nosec B703
            # open_gui might fail for various reasons after the call
            # We're only interested in verifying the call arguments
            pass

    # Verify that subprocess.call was called with the custom exec_file
    assert captured_call_args is not None, "subprocess.call was not called"
    assert (
        custom_exec_file in captured_call_args
    ), f"Expected {custom_exec_file} in call args, but got {captured_call_args}"
    assert "-g" in captured_call_args, "Expected -g flag for GUI mode"
    assert mapdl.jobname in " ".join(
        str(arg) for arg in captured_call_args
    ), f"Expected jobname {mapdl.jobname} in call args"


def test_open_gui_complete_flow_with_mocked_methods(mapdl, fake_local_mapdl):
    """Test complete open_gui flow: call, _launch, and reconnection methods are invoked."""

    custom_exec_file = "/custom/test/path/ansys242"

    # Track what methods were called
    call_invoked = False
    launch_invoked = False

    def mock_call(*args, **kwargs):
        nonlocal call_invoked
        call_invoked = True
        return 0

    def mock_launch(start_parm, timeout=10):
        nonlocal launch_invoked
        launch_invoked = True
        # Verify start_parm is passed
        assert start_parm is not None
        assert "exec_file" in start_parm

    # Mock the call function imported in mapdl_core
    with patch("ansys.mapdl.core.mapdl_core.call", side_effect=mock_call):
        # Mock _local to True so open_gui doesn't raise "can only be called from local"
        with patch.object(mapdl, "_local", True):
            # Mock pathlib.Path to return a mock that has is_file() return True
            mock_path = MagicMock()
            mock_path.is_file.return_value = True
            with patch(
                "ansys.mapdl.core.mapdl_core.pathlib.Path", return_value=mock_path
            ):
                # Store original _launch to restore later
                original_launch = mapdl._launch

                try:
                    # Replace _launch with our mock
                    mapdl._launch = mock_launch

                    # Mock methods that open_gui calls before and after
                    with (
                        patch.object(mapdl, "finish") as mock_finish,
                        patch.object(mapdl, "save") as mock_save,
                        patch.object(mapdl, "exit") as mock_exit,
                        patch.object(mapdl, "resume") as mock_resume,
                        patch.object(mapdl, "_cache_routine") as mock_cache,
                    ):
                        try:
                            # Call open_gui with custom exec_file
                            mapdl.open_gui(exec_file=custom_exec_file, inplace=True)
                        except Exception:  # nosec B703
                            # Some methods might fail, but we verify they were called
                            pass

                        # Verify the flow of method calls
                        assert (
                            mock_finish.called
                        ), "finish() should be called before GUI"
                        assert mock_save.called, "save() should be called before GUI"
                        assert mock_exit.called, "exit() should be called before GUI"
                        assert call_invoked, "subprocess.call should be invoked for GUI"
                        assert launch_invoked, "_launch() should be called to reconnect"
                        assert (
                            mock_resume.called
                        ), "resume() should be called after reconnection"
                        assert (
                            mock_cache.called
                        ), "_cache_routine() should be called after reconnection"
                finally:
                    # Restore original _launch
                    mapdl._launch = original_launch
