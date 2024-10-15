# Copyright (C) 2016 - 2024 ANSYS, Inc. and/or its affiliates.
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
from unittest.mock import patch
import warnings

import psutil
import pytest

from ansys.mapdl import core as pymapdl
from ansys.mapdl.core.errors import (
    NotEnoughResources,
    PortAlreadyInUseByAnMAPDLInstance,
)
from ansys.mapdl.core.launcher import (
    _HAS_ATP,
    LOCALHOST,
    _is_ubuntu,
    _parse_ip_route,
    force_smp_in_student,
    generate_mapdl_launch_command,
    get_slurm_options,
    get_start_instance,
    get_version,
    is_on_slurm,
    launch_mapdl,
    set_license_switch,
    set_MPI_additional_switches,
    update_env_vars,
)
from ansys.mapdl.core.licensing import LICENSES
from conftest import ON_LOCAL, QUICK_LAUNCH_SWITCHES, NullContext, requires

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
    add_sw = set_MPI_additional_switches("", exec_path)
    assert "msmpi" in add_sw

    add_sw = set_MPI_additional_switches("-mpi intelmpi", exec_path)
    assert "msmpi" in add_sw and "intelmpi" not in add_sw

    add_sw = set_MPI_additional_switches("-mpi INTELMPI", exec_path)
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
@requires("ansys-tools-path")
@pytest.mark.parametrize("license_name", LICENSES)
def test_license_type_keyword_names(mapdl, monkeypatch, license_name):
    exec_file = find_ansys()[0]
    args = launch_mapdl(
        exec_file=exec_file, license_type=license_name, _debug_no_launch=True
    )
    assert f"-p {license_name}" in args["additional_switches"]


# @requires("local")
@pytest.mark.parametrize("license_name", LICENSES)
def test_license_type_additional_switch(mapdl, license_name):
    args = launch_mapdl(
        additional_switches=QUICK_LAUNCH_SWITCHES + " -p " + license_name,
        _debug_no_launch=True,
    )
    assert f"-p {license_name}" in args["additional_switches"]


@requires("ansys-tools-path")
def test_license_type_dummy(mapdl):
    dummy_license_type = "dummy"
    with pytest.warns(
        UserWarning,
        match="Still PyMAPDL will try to use it but in older MAPDL versions you might experience",
    ):
        launch_mapdl(
            start_instance=False,
            port=mapdl.port + 1,
            additional_switches=f" -p {dummy_license_type} " + QUICK_LAUNCH_SWITCHES,
            start_timeout=start_timeout,
            license_server_check=False,
            _debug_no_launch=True,
        )


@requires("local")
@requires("nostudent")
def test_remove_temp_dir_on_exit(mapdl):
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
    if path.startswith(ans_temp_dir):
        assert not os.path.isdir(path)
    else:
        assert os.path.isdir(path)


@requires("local")
@requires("nostudent")
def test_remove_temp_dir_on_exit_fail(tmpdir, mapdl):
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
installed_mapdl_versions.extend(list(versions.keys()))
installed_mapdl_versions.extend([each / 10 for each in versions.keys()])
installed_mapdl_versions.extend([str(each) for each in list(versions.keys())])
installed_mapdl_versions.extend([str(each / 10) for each in versions.keys()])
installed_mapdl_versions.extend(list(versions.values()))


@pytest.mark.parametrize("version", installed_mapdl_versions)
def test__verify_version_pass(version):
    ver = get_version(version)
    assert isinstance(ver, int)
    assert min(versions.keys()) <= ver <= max(versions.keys())


def test__verify_version_latest():
    assert get_version("latest") is None


@requires("ansys-tools-path")
@requires("local")
def test_find_ansys(mapdl):
    assert find_ansys() is not None

    # Checking ints
    version = int(mapdl.version * 10)
    assert find_ansys(version=version) is not None

    # Checking floats
    with pytest.raises(ValueError):
        find_ansys(version=22.2)

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
    assert str(version) in str(launching_arg["version"])


@requires("local")
def test_raise_exec_path_and_version_launcher(mapdl):
    with pytest.raises(ValueError):
        get_version("asdf", "asdf")


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
def test_launching_on_busy_port(mapdl, monkeypatch):
    monkeypatch.delenv("PYMAPDL_PORT", raising=False)
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
                "PYMAPDL_NPROC": 5,
                "SLURM_JOB_NAME": "myawesomejob",
                "SLURM_NTASKS": 2,
                "SLURM_CPUS_PER_TASK": 2,
                "SLURM_NPROCS": 1,
                "SLURM_CPUS_ON_NODE": None,
                "SLURM_MEM_PER_NODE": None,
                "SLURM_NODELIST": None,
            },
            {"nproc": 5, "jobname": "myawesomejob"},
            id="Testing PYMAPDL_NPROC and SLURM_JOB_NAME",
        ),
        pytest.param(
            {
                "PYMAPDL_NPROC": 5,
                "SLURM_JOB_NAME": "myawesomejob",
                "SLURM_NTASKS": 2,
                "SLURM_CPUS_PER_TASK": 2,
                "SLURM_NPROCS": 1,
                "SLURM_CPUS_ON_NODE": None,
                "SLURM_MEM_PER_NODE": None,
                "SLURM_NODELIST": None,
                "PYMAPDL_MAPDL_EXEC": "asdf/qwer/poiu",
            },
            {"nproc": 5, "jobname": "myawesomejob", "exec_file": "asdf/qwer/poiu"},
            id="Testing PYMAPDL_NPROC and SLURM_JOB_NAME",
        ),
    ),
    indirect=["set_env_var_context"],
)
def test_get_slurm_options(set_env_var_context, validation):
    """test slurm env vars"""
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


@pytest.mark.parametrize("slurm_env_var", ["True", "false", ""])
@pytest.mark.parametrize("slurm_job_name", ["True", "false", ""])
@pytest.mark.parametrize("slurm_job_id", ["True", "false", ""])
@pytest.mark.parametrize("detect_slurm_config", [True, False, None])
def test_is_on_slurm(
    monkeypatch, fs, slurm_env_var, slurm_job_name, slurm_job_id, detect_slurm_config
):
    monkeypatch.setenv("PYMAPDL_ON_SLURM", slurm_env_var)
    monkeypatch.setenv("SLURM_JOB_NAME", slurm_job_name)
    monkeypatch.setenv("SLURM_JOB_ID", slurm_job_id)

    flag = is_on_slurm(args={"detect_slurm_config": detect_slurm_config})

    if detect_slurm_config is not True:
        assert not flag

    else:
        if slurm_env_var.lower() == "false":
            assert not flag

        else:
            if slurm_job_name != "" and slurm_job_id != "":
                assert flag
            else:
                assert not flag

    # Fake MAPDL installation to avoid errors.
    exec_file = r"/ansys_inc/v241/ansys/bin/mapdl"
    fs.create_file(exec_file)

    assert (
        launch_mapdl(
            exec_file=exec_file,
            detect_slurm_config=detect_slurm_config,
            _debug_no_launch=True,
        )["ON_SLURM"]
        == flag
    )


@pytest.mark.parametrize(
    "start_instance,context",
    [
        pytest.param(True, NullContext(), id="Boolean true"),
        pytest.param(False, NullContext(), id="Boolean false"),
        pytest.param("true", NullContext(), id="String true"),
        pytest.param("TRue", NullContext(), id="String true weird capitalization"),
        pytest.param("2", pytest.raises(ValueError), id="String number"),
        pytest.param(2, pytest.raises(ValueError), id="Int"),
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
@requires("ansys-tools-path")
@pytest.mark.parametrize("start_instance", [True, False])
def test_launcher_start_instance(monkeypatch, start_instance):
    if "PYMAPDL_START_INSTANCE" in os.environ:
        monkeypatch.delenv("PYMAPDL_START_INSTANCE")
    options = launch_mapdl(
        exec_file=find_ansys()[0], start_instance=start_instance, _debug_no_launch=True
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
    if not _HAS_ATP and not os.environ.get("PYMAPDL_MAPDL_EXEC"):
        # if start_instance and not ip:
        with pytest.raises(
            ModuleNotFoundError,
            match="If you don't have 'ansys-tools-path' library installed, you need",
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
    with warnings.catch_warnings():
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


def mycpucount(**kwargs):
    return 10  # faking 10 cores


@patch("os.name", "nt")
@patch("psutil.cpu_count", mycpucount)
def test_generate_mapdl_launch_command_windows():
    assert os.name == "nt"  # Checking mocking is properly done

    exec_file = "C:/Program Files/ANSYS Inc/v242/ansys/bin/winx64/ANSYS242.exe"
    jobname = "myjob"
    nproc = 10
    port = 1000
    ram = 2
    additional_switches = "-my_add=switch"

    cmd = generate_mapdl_launch_command(
        exec_file=exec_file,
        jobname=jobname,
        nproc=nproc,
        port=port,
        ram=ram,
        additional_switches=additional_switches,
    )

    assert f'"{exec_file}" ' in cmd
    assert f" -j {jobname} " in cmd
    assert f" -port {port} " in cmd
    assert f" -m {ram*1024} " in cmd
    assert f" -np {nproc} " in cmd
    assert " -grpc" in cmd
    assert f" {additional_switches} " in cmd
    assert f" -b -i .__tmp__.inp " in cmd
    assert f" -o .__tmp__.out " in cmd


def test_generate_mapdl_launch_command_linux():
    assert os.name != "nt"  # Checking mocking is properly done

    exec_file = "/ansys_inc/v242/ansys/bin/ansys242"
    jobname = "myjob"
    nproc = 10
    port = 1000
    ram = 2
    additional_switches = "-my_add=switch"

    cmd = generate_mapdl_launch_command(
        exec_file=exec_file,
        jobname=jobname,
        nproc=nproc,
        port=port,
        ram=ram,
        additional_switches=additional_switches,
    )

    assert f'"{exec_file}" ' in cmd
    assert f" -j {jobname} " in cmd
    assert f" -port {port} " in cmd
    assert f" -m {ram*1024} " in cmd
    assert f" -np {nproc} " in cmd
    assert " -grpc" in cmd
    assert f" {additional_switches} " in cmd

    assert f" -i .__tmp__.inp " not in cmd
    assert f" -o .__tmp__.out " not in cmd
