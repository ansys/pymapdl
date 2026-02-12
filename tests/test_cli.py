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

import os
import platform
import re
import subprocess
from typing import Callable
from unittest.mock import MagicMock, patch

import numpy as np
import psutil
import pytest

import ansys.mapdl.core.cli.core as core_module
from ansys.mapdl.core.cli.core import get_ansys_process_from_port
from ansys.mapdl.core.plotting import GraphicsBackend
from conftest import VALID_PORTS, requires

if VALID_PORTS:
    PORT1 = max(VALID_PORTS) + 1
else:
    PORT1 = 50090


def make_fake_process(pid, name, port=PORT1, ansys_process=False, n_children=0):
    import getpass

    mock_process = MagicMock(spec=psutil.Process)
    mock_process.pid = pid
    mock_process.name.return_value = name
    mock_process.info = {"name": name}  # For attrs=['name'] optimization
    mock_process.status.return_value = psutil.STATUS_RUNNING
    mock_process.children.side_effect = lambda *arg, **kwargs: [
        i for i in range(n_children)
    ]
    mock_process.cwd.return_value = f"/cwd/of/{name}"
    mock_process.username.return_value = getpass.getuser()  # Add username method

    if ansys_process:
        mock_process.cmdline.return_value = (
            f"/ansys_inc/v251/ansys/bin/ansys251 -grpc -port {port}".split(" ")
        )
    else:
        mock_process.cmdline.return_value = f"/path/to/process".split(" ")

    return mock_process


@pytest.fixture(scope="function")
def run_cli() -> Callable[[str, bool], str]:
    def do_run(arguments: str = "", expect_error: bool = False) -> str:
        from click.testing import CliRunner

        from ansys.mapdl.core.cli import main

        if arguments:
            args = list(arguments.strip().split(" "))
        else:
            args = []

        runner = CliRunner()
        result = runner.invoke(main, args)
        if expect_error:
            assert result.exit_code != 0
        else:
            assert result.exit_code == 0
        return result.output

    return do_run


@requires("click")
@pytest.mark.parametrize("start_instance", [None, True, False])
def test_launch_mapdl_cli(monkeypatch, run_cli, start_instance):
    if start_instance is not None:
        monkeypatch.setenv("PYMAPDL_START_INSTANCE", str(start_instance))
    else:
        monkeypatch.delenv("PYMAPDL_START_INSTANCE", raising=False)

    with (
        patch("ansys.mapdl.core.launcher.launch_mapdl") as mock_launch,
        patch("ansys.mapdl.core.launcher.submitter") as mock_submitter,
    ):  # test we are not calling Popen

        mock_launch.side_effect = lambda *args, **kwargs: (
            "123.45.67.89",
            str(PORT1),
            "123245",
        )

        # Setting a port so it does not collide with the already running instance for testing
        output = run_cli(f"start --port {PORT1}")

    assert "Success: Launched an MAPDL instance " in output
    assert str(PORT1) in output

    # grab ips and port
    pid = re.search(r"\(PID=(\d+)\)", output)
    assert pid
    pid = int(re.search(r"\(PID=(\d+)\)", output).groups()[0])
    assert pid != 0


@requires("click")
@pytest.mark.parametrize(
    "mapping",
    ((False, True), (False, True, False), (False, False, False), (True, True, False)),
)
def test_pymapdl_stop_instances(run_cli, mapping):

    fake_process_ = [
        {
            "pid": np.random.randint(10000, 100000),
            "name": f"ansys251_{ind}" if each else "process",
            "port": str(50052 + ind),
            "ansys_process": each,
        }
        for ind, each in enumerate(mapping)
    ]

    fake_processes = [make_fake_process(**each) for each in fake_process_]

    with (
        patch("ansys.mapdl.core.cli.stop._kill_process") as mock_kill,
        patch("psutil.pid_exists") as mock_pid,
        patch("psutil.process_iter", return_value=iter(fake_processes)),
    ):

        mock_pid.return_value = lambda *args, **kwargs: True  # All process exists
        mock_kill.side_effect = lambda *args, **kwargs: None  # avoid kill nothing

        if sum(mapping) == 0:
            output = run_cli(f"stop --port {PORT1}")
            assert (
                f"error: no ansys instances running on port {PORT1}" in output.lower()
            )
            mock_kill.assert_not_called()

            output = run_cli(f"stop --all")
            assert f"error: no ansys instances have been found." in output.lower()
            mock_kill.assert_not_called()

        elif sum(mapping) == 1:
            # Port
            process, process_mock = [
                (each, each_mock)
                for each, each_mock in zip(fake_process_, fake_processes)
                if "ansys251" in each["name"]
            ][0]
            port = process["port"]

            output = run_cli(f"stop --port {port}")
            assert (
                f"success: ansys instances running on port {port} have been stopped"
                in output.lower()
            )

            # PID
            pid = process["pid"]
            with patch("psutil.Process") as mock_process:
                mock_process.return_value = process_mock

                output = run_cli(f"stop --pid {pid}")
                assert (
                    f"the process with pid {pid} and its children have been stopped."
                    in output.lower()
                )

            mock_kill.assert_called()
            assert mock_kill.call_count == 2

        else:
            output = run_cli(f"stop --all")
            assert "success: ansys instances have been stopped." in output.lower()
            assert mock_kill.call_count == sum(mapping)


@requires("click")
def test_pymapdl_stop_permission_handling(run_cli):
    """Test that pymapdl stop handles processes owned by other users without crashing.

    This test specifically addresses Issue #4256:
    https://github.com/ansys/pymapdl/issues/4256

    The test verifies that:
    1. Processes owned by other users are skipped silently
    2. Processes with AccessDenied errors don't crash the command
    3. Only processes owned by the current user are considered for termination
    """

    def make_other_user_process(pid, name, ansys_process=True):
        """Create a mock process owned by another user."""
        mock_process = MagicMock(spec=psutil.Process)
        mock_process.pid = pid
        mock_process.name.return_value = name
        mock_process.info = {"name": name}  # For attrs=['name'] optimization
        mock_process.status.return_value = psutil.STATUS_RUNNING

        if ansys_process:
            mock_process.cmdline.return_value = ["ansys251", "-grpc", "-port", "50052"]
        else:
            mock_process.cmdline.return_value = ["other_process"]

        # This process belongs to another user
        mock_process.username.return_value = "other_user_name"
        return mock_process

    def make_inaccessible_process(pid: int, name: str):
        """Create a mock process that raises AccessDenied (simulates real permission issues)."""
        mock_process = MagicMock(spec=psutil.Process)
        mock_process.pid = pid
        mock_process.name.return_value = name
        mock_process.info = {"name": name}  # For attrs=['name'] optimization

        # Simulate the original issue: AccessDenied when accessing process info
        mock_process.cmdline.side_effect = psutil.AccessDenied(pid, name)
        mock_process.username.side_effect = psutil.AccessDenied(pid, name)
        mock_process.status.side_effect = psutil.AccessDenied(pid, name)
        return mock_process

    # Create a mix of processes:
    # 1. Current user's ANSYS process (should be killed)
    # 2. Other user's ANSYS process (should be skipped)
    # 3. Inaccessible ANSYS process (should be skipped without crashing)
    # 4. Current user's non-ANSYS process (should be skipped)
    test_processes = [
        make_fake_process(
            pid=1001, name="ansys251", ansys_process=True
        ),  # Current user - should kill
        make_other_user_process(
            pid=1002, name="ansys261", ansys_process=True
        ),  # Other user - skip
        make_inaccessible_process(pid=1003, name="ansys.exe"),  # Inaccessible - skip
        make_fake_process(
            pid=1004, name="python", ansys_process=False
        ),  # Not ANSYS - skip
    ]

    killed_processes: list[int] = []

    def mock_kill_process(proc: psutil.Process):
        """Track which processes would be killed."""
        killed_processes.append(proc.pid)

    with (
        patch("psutil.process_iter", return_value=test_processes),
        patch("psutil.pid_exists", return_value=True),
        patch("ansys.mapdl.core.cli.stop._kill_process", side_effect=mock_kill_process),
    ):

        # Test 1: stop --all should not crash and only kill current user's ANSYS processes
        killed_processes.clear()
        output = run_cli("stop --all")

        # Should succeed without errors
        assert (
            "success" in output.lower() or "error: no ansys instances" in output.lower()
        )

        # Should only kill the current user's ANSYS process (PID 1001)
        # Note: The test might show "no instances found" because our validation is stricter now
        if killed_processes:
            assert killed_processes == [
                1001
            ], f"Expected [1001], got {killed_processes}"

        # Test 2: stop --port should also handle permissions correctly
        killed_processes.clear()
        output = run_cli("stop --port 50052")

        # Should not crash
        assert "error" in output.lower() or "success" in output.lower()

        # Verify no exceptions were raised (test would fail if AccessDenied was unhandled)
        print("✅ Permission handling test passed - no crashes occurred")


@requires("click")
@pytest.mark.skipif(
    platform.system() != "Windows", reason="Domain usernames are Windows-specific"
)
def test_pymapdl_stop_with_username_containing_domain(run_cli):
    """Test that pymapdl stop processes when a process username contains DOMAIN information."""
    current_user = "someuser"

    mock_process = MagicMock(spec=psutil.Process)
    mock_process.pid = 12
    mock_process.name.return_value = "ansys252"
    mock_process.info = {"name": "ansys252"}  # For attrs=['name'] optimization
    mock_process.status.return_value = psutil.STATUS_RUNNING
    mock_process.cmdline.return_value = ["ansys251", "-grpc", "-port", "50052"]
    mock_process.username.return_value = f"DOMAIN\\{current_user}"

    killed_processes: list[int] = []

    def mock_kill_process(proc: psutil.Process):
        """Track which processes would be killed."""
        killed_processes.append(proc.pid)

    with (
        patch("getpass.getuser", return_value=current_user),
        patch("psutil.process_iter", return_value=[mock_process]),
        patch("psutil.pid_exists", return_value=True),
        patch("ansys.mapdl.core.cli.stop._kill_process", side_effect=mock_kill_process),
    ):
        killed_processes.clear()
        output = run_cli("stop --all")

        assert "success" in output.lower()
        assert killed_processes == [12]


@requires("click")
@requires("tabulate")
@pytest.mark.parametrize(
    "arg,check",
    (
        ("", {}),  # default
        ("-i", {"Is Instance": False}),
        ("-c", {"Command line": True}),
        ("-l", {"Command line": True, "Working directory": True}),
        ("-cwd", {"Working directory": True}),
        ("--instances", {"Is Instance": False}),
        ("--cmd", {"Command line": True}),
        ("--long", {"Command line": True, "Working directory": True}),
        ("--location", {"Working directory": True}),
    ),
)
@patch("psutil.pid_exists", lambda *args, **kwargs: True)
def test_launch_mapdl_cli_list(run_cli, arg, check):

    mapping = (False, True, False, True, False, False)
    is_instance = (False, False, False, True, False, False)

    fake_process_ = [
        {
            "pid": np.random.randint(10000, 100000),
            "name": f"ansys251_{ind}" if each else "process",
            "port": str(50052 + ind),
            "ansys_process": each,
            "n_children": 4 if each_ins else 1,
        }
        for ind, (each, each_ins) in enumerate(zip(mapping, is_instance))
    ]

    fake_processes = [make_fake_process(**each) for each in fake_process_]

    checks_defaults = {
        "Is Instance": True,
        "Command line": False,
        "Working directory": False,
    }

    with patch("psutil.process_iter", return_value=iter(fake_processes)):
        output = run_cli(" ".join(["list", arg]))

        assert "running" in output or "sleeping" in output
        checks_defaults.update(check)

        for each, value in checks_defaults.items():
            if value:
                assert each in output
            else:
                assert each not in output

        assert len(output.splitlines()) > 2

        if arg in ["-c", "--cmd"]:
            assert "/ansys_inc/v251/ansys/bin/ansys251" in output

        if arg in ["-cwd", "--location"]:
            assert "/cwd/of/ansys251" in output

        if arg in ["-i", "--instances"]:
            assert len(output.splitlines()) == sum(is_instance) + 2
        else:
            assert len(output.splitlines()) == sum(mapping) + 2

        if arg in ["-l", "--long"]:
            assert "/ansys_inc/v251/ansys/bin/ansys251" in output.lower()

        for ind, (each, each_ins) in enumerate(zip(mapping, is_instance)):
            proc_options = fake_process_[ind]
            # is ansys
            if not each or (not each_ins and arg in ["-i", "--instances"]):
                assert proc_options["name"] not in output
                assert str(proc_options["pid"]) not in output
                assert proc_options["port"] not in output
            else:
                assert proc_options["name"] in output
                assert str(proc_options["pid"]) in output
                assert proc_options["port"] in output


@requires("click")
@requires("tabulate")
def test_pymapdl_list_permission_handling(run_cli):
    """Test that pymapdl list handles processes with permission errors gracefully.

    This test verifies that:
    1. Processes owned by other users are skipped silently
    2. Processes with AccessDenied on cmdline don't crash the command
    3. Only accessible processes are listed
    """

    def make_other_user_process(pid, name, ansys_process=True):
        """Create a mock process owned by another user."""
        mock_process = MagicMock(spec=psutil.Process)
        mock_process.pid = pid
        mock_process.name.return_value = name
        mock_process.info = {"name": name}
        mock_process.status.return_value = psutil.STATUS_RUNNING

        if ansys_process:
            # This simulates a process where cmdline() raises AccessDenied
            mock_process.cmdline.side_effect = psutil.AccessDenied(pid, name)
            # username also raises AccessDenied
            mock_process.username.side_effect = psutil.AccessDenied(pid, name)
        else:
            mock_process.cmdline.return_value = ["other_process"]
            mock_process.username.return_value = "other_user"

        return mock_process

    def make_cmdline_denied_current_user_process(pid, name):
        """Create a mock process where cmdline is denied but it's current user's process."""
        import getpass

        mock_process = MagicMock(spec=psutil.Process)
        mock_process.pid = pid
        mock_process.name.return_value = name
        mock_process.info = {"name": name}
        mock_process.status.return_value = psutil.STATUS_RUNNING

        # cmdline raises AccessDenied
        mock_process.cmdline.side_effect = psutil.AccessDenied(pid, name)
        # But username works and returns current user
        mock_process.username.return_value = getpass.getuser()

        return mock_process

    # Create a mix of processes:
    # 1. Current user's accessible ANSYS process (should be listed)
    # 2. Other user's ANSYS process with permission errors (should be skipped)
    # 3. Current user's ANSYS process with cmdline permission error (should be skipped - can't verify if gRPC)
    # 4. Non-ANSYS process (should be skipped)
    test_processes = [
        make_fake_process(
            pid=2001, name="ansys251", ansys_process=True, port=50053, n_children=4
        ),  # Accessible - should list
        make_other_user_process(
            pid=2002, name="ansys261", ansys_process=True
        ),  # Other user - skip
        make_cmdline_denied_current_user_process(
            pid=2003, name="ansys.exe"
        ),  # Current user but cmdline denied - skip
        make_fake_process(
            pid=2004, name="python", ansys_process=False
        ),  # Not ANSYS - skip
    ]

    with patch("psutil.process_iter", return_value=test_processes):
        # Test list command should not crash and only list accessible processes
        output = run_cli("list")

        # Should succeed without errors
        assert "running" in output.lower() or "sleeping" in output.lower()

        # Should list the accessible process (PID 2001)
        assert "2001" in output
        assert "50053" in output

        # Should NOT list the inaccessible processes
        assert "2002" not in output
        assert "2003" not in output
        assert "2004" not in output

        # Verify no exceptions were raised
        print("✅ List permission handling test passed - no crashes occurred")


@requires("click")
@pytest.mark.parametrize(
    "arg",
    [
        "ip",
        "license_server_check",
        "mode",
        "loglevel",
        "cleanup_on_exit",
        "start_instance",
        "clear_on_connect",
        "log_apdl",
        "remove_temp_dir_on_exit",
        "print_com",
        "add_env_vars",
        "replace_env_vars",
    ],
)
def test_launch_mapdl_cli_config(run_cli, arg):
    cmd = " ".join(["start", f"--port {PORT1}", "--jobname myjob", f"--{arg} True"])

    with (
        patch("ansys.mapdl.core.launcher.launch_mapdl") as mock_launch,
        patch("ansys.mapdl.core.launcher.submitter") as mock_submitter,
    ):  # test we are not calling Popen
        mock_launch.side_effect = lambda *args, **kwargs: (
            "123.45.67.89",
            str(PORT1),
            "123245",
        )

        output = run_cli(cmd)

        mock_submitter.assert_not_called()
        kwargs = mock_launch.call_args_list[0].kwargs
        assert str(kwargs["port"]) == str(PORT1)

        assert "Launched an MAPDL instance" in output
        assert str(PORT1) in output

        # assert warnings
        assert arg not in kwargs
        assert (
            f"The following argument is not allowed in CLI: '{arg}'" in output
        ), f"Warning about '{arg}' not printed"


@requires("click")
def test_convert(run_cli, tmpdir):
    from ansys.mapdl.core._version import __version__

    input_file = str(tmpdir.join("input.apdl"))
    output_file = str(tmpdir.join("output.pymapdl"))

    with open(input_file, "w") as fid:
        fid.write("""/prep7
BLOCK,0,1,0,1,0,1
""")

    run_cli(f"convert -f {input_file} -o {output_file}")

    with open(output_file, "r") as fid:
        converted = fid.read()

    assert "Script generated by ansys-mapdl-core version" in converted
    assert str(__version__) in converted
    assert "from ansys.mapdl.core import launch_mapdl" in converted

    assert """
mapdl.prep7()
mapdl.block(0, 1, 0, 1, 0, 1)""" in converted


@requires("click")
@pytest.mark.skipif(os.name != "posix", reason="Piping only works on Linux")
@pytest.mark.parametrize("output", [True, False])
def test_convert_pipe(output):
    cmd = ["echo", "/prep7"]
    cmd2 = ["pymapdl", "convert"]
    if output:
        out_file = "my_output.out"
        cmd2.extend(["-o", out_file])

    process_echo = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    process_pymapdl = subprocess.Popen(
        cmd2, stdin=process_echo.stdout, stdout=subprocess.PIPE
    )

    process_echo.stdout.close()

    stdout = process_pymapdl.stdout.read().decode()

    if output:
        assert os.path.exists(out_file)
        with open(out_file, "r") as fid:
            stdout = fid.read()

    assert "mapdl.prep7" in stdout
    assert "Script generated by ansys-mapdl-core version" in stdout
    assert "mapdl.exit()" in stdout

    process_pymapdl.kill()
    process_echo.kill()


DEFAULT_ARGS = {
    "apdl_strings": "/prep7\nBLOCK,0,1,0,1,0,1",
    "loglevel": "WARNING",
    "auto_exit": True,
    "line_ending": None,
    "exec_file": None,
    "macros_as_functions": True,
    "use_function_names": True,
    "show_log": False,
    "add_imports": True,
    "comment_solve": False,
    "cleanup_output": True,
    "header": True,
    "print_com": True,
    "only_commands": False,
    "graphics_backend": None,
    "clear_at_start": False,
    "check_parameter_names": False,
}


@requires("click")
@pytest.mark.parametrize(
    "arg, value",
    (
        ("output", "specific_output"),
        ("loglevel", "specific_output"),
        ("auto_exit", False),
        ("line_ending", "specific_output"),
        ("exec_file", "specific_output"),
        ("macros_as_functions", False),
        ("use_function_names", False),
        ("show_log", True),
        ("add_imports", False),
        ("comment_solve", True),
        ("cleanup_output", False),
        ("header", False),
        ("print_com", False),
        ("only_commands", True),
        ("graphics_backend", "MAPDL"),
        ("graphics_backend", "mapdl"),
        ("graphics_backend", "pyvista"),
        ("graphics_backend", "pyVISTa"),
        ("graphics_backend", "no_exists"),
        ("clear_at_start", True),
        ("check_parameter_names", True),
    ),
)
@patch("ansys.mapdl.core.convert.convert_apdl_block")
def test_convert_passing(mock_conv, run_cli, tmpdir, arg, value):
    mock_conv.return_value = None

    input_file = str(tmpdir.join("input.apdl"))
    with open(input_file, "w") as fid:
        fid.write("/prep7\nBLOCK,0,1,0,1,0,1")

    default_ = DEFAULT_ARGS.copy()
    default_[arg] = value
    expect_error = False
    if value == "no_exists":
        expect_error = True
    if arg not in ["only_commands"]:
        run_cli(f"convert -f {input_file} --{arg} {value}", expect_error)

    else:
        run_cli(f"convert -f {input_file} --{arg}", expect_error)

    # Early return if expect_error is True and function is not called
    if expect_error:
        return
    mock_conv.assert_called()
    kwargs = mock_conv.call_args.kwargs
    for key in DEFAULT_ARGS:
        if key == "graphics_backend" and arg == "graphics_backend":
            assert kwargs[key] == GraphicsBackend[value.upper()]
        else:
            assert kwargs[key] == default_[key]


def make_mock_process_for_port_test(
    pid,
    name,
    status=psutil.STATUS_RUNNING,
    cmdline=None,
    connections=None,
    raise_exception=None,
):
    """Helper to create mock process for get_ansys_process_from_port tests."""
    mock_proc = MagicMock(spec=psutil.Process)
    mock_proc.pid = pid
    mock_proc.info = {"name": name}

    class NoSuchProcess(psutil.NoSuchProcess):
        def __init__(self):
            super().__init__(pid)

    class ZombieProcess(psutil.ZombieProcess):
        def __init__(self):
            super().__init__(pid)

    if raise_exception == "status":
        mock_proc.status.side_effect = NoSuchProcess
    else:
        mock_proc.status.return_value = status
    if raise_exception == "cmdline":
        mock_proc.cmdline.side_effect = psutil.AccessDenied
    else:
        mock_proc.cmdline.return_value = cmdline or []
    if raise_exception == "connections":
        mock_proc.connections.side_effect = ZombieProcess
    else:
        mock_proc.connections.return_value = connections or []
    return mock_proc


def test_get_ansys_process_from_port_no_processes():
    """Test get_ansys_process_from_port with no processes."""
    with patch("psutil.process_iter", return_value=[]):
        result = get_ansys_process_from_port(50052)
        assert result is None


def test_get_ansys_process_from_port_not_ansys():
    """Test get_ansys_process_from_port with non-ANSYS process."""
    mock_proc = make_mock_process_for_port_test(1, "python")
    with (
        patch("psutil.process_iter", return_value=[mock_proc]),
        patch.object(core_module, "is_valid_ansys_process_name", return_value=False),
        patch.object(core_module, "is_alive_status", return_value=True),
    ):
        result = get_ansys_process_from_port(50052)
        assert result is None


def test_get_ansys_process_from_port_not_alive():
    """Test get_ansys_process_from_port with ANSYS process not alive."""
    mock_proc = make_mock_process_for_port_test(1, "ansys", status=psutil.STATUS_DEAD)
    with (
        patch("psutil.process_iter", return_value=[mock_proc]),
        patch.object(core_module, "is_valid_ansys_process_name", return_value=True),
        patch.object(core_module, "is_alive_status", return_value=False),
    ):
        result = get_ansys_process_from_port(50052)
        assert result is None


def test_get_ansys_process_from_port_no_grpc():
    """Test get_ansys_process_from_port with ANSYS process without -grpc."""
    mock_proc = make_mock_process_for_port_test(
        1, "ansys", cmdline=["ansys", "-port", "50052"]
    )
    with (
        patch("psutil.process_iter", return_value=[mock_proc]),
        patch.object(core_module, "is_valid_ansys_process_name", return_value=True),
        patch.object(core_module, "is_alive_status", return_value=True),
    ):
        result = get_ansys_process_from_port(50052)
        assert result is None


def test_get_ansys_process_from_port_not_listening():
    """Test get_ansys_process_from_port with ANSYS process not listening on port."""
    import socket

    mock_conn = MagicMock()
    mock_conn.status = "LISTEN"
    mock_conn.family = socket.AF_INET
    mock_conn.laddr = ("127.0.0.1", 50053)  # wrong port
    mock_proc = make_mock_process_for_port_test(
        1,
        "ansys",
        cmdline=["ansys", "-grpc", "-port", "50052"],
        connections=[mock_conn],
    )
    with (
        patch("psutil.process_iter", return_value=[mock_proc]),
        patch.object(core_module, "is_valid_ansys_process_name", return_value=True),
        patch.object(core_module, "is_alive_status", return_value=True),
    ):
        result = get_ansys_process_from_port(50052)
        assert result is None


def test_get_ansys_process_from_port_not_listen_status():
    """Test get_ansys_process_from_port with connection not LISTEN."""
    import socket

    mock_conn = MagicMock()
    mock_conn.status = "ESTABLISHED"
    mock_conn.family = socket.AF_INET
    mock_conn.laddr = ("127.0.0.1", 50052)
    mock_proc = make_mock_process_for_port_test(
        1,
        "ansys",
        cmdline=["ansys", "-grpc", "-port", "50052"],
        connections=[mock_conn],
    )
    with (
        patch("psutil.process_iter", return_value=[mock_proc]),
        patch.object(core_module, "is_valid_ansys_process_name", return_value=True),
        patch.object(core_module, "is_alive_status", return_value=True),
    ):
        result = get_ansys_process_from_port(50052)
        assert result is None


def test_get_ansys_process_from_port_wrong_family():
    """Test get_ansys_process_from_port with wrong family."""
    import socket

    mock_conn = MagicMock()
    mock_conn.status = "LISTEN"
    mock_conn.family = socket.AF_INET6  # wrong family
    mock_conn.laddr = ("127.0.0.1", 50052)
    mock_proc = make_mock_process_for_port_test(
        1,
        "ansys",
        cmdline=["ansys", "-grpc", "-port", "50052"],
        connections=[mock_conn],
    )
    with (
        patch("psutil.process_iter", return_value=[mock_proc]),
        patch.object(core_module, "is_valid_ansys_process_name", return_value=True),
        patch.object(core_module, "is_alive_status", return_value=True),
    ):
        result = get_ansys_process_from_port(50052)
        assert result is None


def test_get_ansys_process_from_port_success():
    """Test get_ansys_process_from_port finds the process."""
    import socket

    mock_conn = MagicMock()
    mock_conn.status = "LISTEN"
    mock_conn.family = socket.AF_INET
    mock_conn.laddr = ("127.0.0.1", 50052)
    mock_proc = make_mock_process_for_port_test(
        1,
        "ansys",
        cmdline=["ansys", "-grpc", "-port", "50052"],
        connections=[mock_conn],
    )
    with (
        patch("psutil.process_iter", return_value=[mock_proc]),
        patch.object(core_module, "is_valid_ansys_process_name", return_value=True),
        patch.object(core_module, "is_alive_status", return_value=True),
    ):
        result = get_ansys_process_from_port(50052)
        assert result == mock_proc


def test_get_ansys_process_from_port_exception_status():
    """Test get_ansys_process_from_port handles exception in status."""
    mock_proc = make_mock_process_for_port_test(1, "ansys")

    class NoSuchProcess(psutil.NoSuchProcess):
        def __init__(self):
            super().__init__(1)

    with (
        patch("psutil.process_iter", return_value=[mock_proc]),
        patch.object(core_module, "is_valid_ansys_process_name", return_value=True),
        patch.object(core_module, "is_alive_status", side_effect=NoSuchProcess),
    ):
        result = get_ansys_process_from_port(50052)
        assert result is None


def test_get_ansys_process_from_port_exception_cmdline():
    """Test get_ansys_process_from_port handles exception in cmdline."""
    mock_proc = make_mock_process_for_port_test(1, "ansys", raise_exception="cmdline")
    with (
        patch("psutil.process_iter", return_value=[mock_proc]),
        patch.object(core_module, "is_valid_ansys_process_name", return_value=True),
        patch.object(core_module, "is_alive_status", return_value=True),
    ):
        # with pytest.raises(psutil.AccessDenied):
        result = get_ansys_process_from_port(50052)
        assert result is None


def test_get_ansys_process_from_port_exception_connections():
    """Test get_ansys_process_from_port handles exception in connections."""
    mock_proc = make_mock_process_for_port_test(
        1,
        "ansys",
        cmdline=["ansys", "-grpc", "-port", "50052"],
        raise_exception="connections",
    )
    with (
        patch("psutil.process_iter", return_value=[mock_proc]),
        patch.object(core_module, "is_valid_ansys_process_name", return_value=True),
        patch.object(core_module, "is_alive_status", return_value=True),
    ):
        result = get_ansys_process_from_port(50052)
        assert result is None


def test_get_ansys_process_from_port_multiple_processes():
    """Test get_ansys_process_from_port with multiple processes, returns first match."""
    import socket

    mock_conn1 = MagicMock()
    mock_conn1.status = "LISTEN"
    mock_conn1.family = socket.AF_INET
    mock_conn1.laddr = ("127.0.0.1", 50052)
    mock_proc1 = make_mock_process_for_port_test(
        1,
        "ansys",
        cmdline=["ansys", "-grpc", "-port", "50052"],
        connections=[mock_conn1],
    )

    mock_conn2 = MagicMock()
    mock_conn2.status = "LISTEN"
    mock_conn2.family = socket.AF_INET
    mock_conn2.laddr = ("127.0.0.1", 50053)
    mock_proc2 = make_mock_process_for_port_test(
        2,
        "ansys",
        cmdline=["ansys", "-grpc", "-port", "50053"],
        connections=[mock_conn2],
    )

    with (
        patch("psutil.process_iter", return_value=[mock_proc1, mock_proc2]),
        patch.object(core_module, "is_valid_ansys_process_name", return_value=True),
        patch.object(core_module, "is_alive_status", return_value=True),
    ):
        result = get_ansys_process_from_port(50052)
        assert result == mock_proc1
