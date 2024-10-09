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

import re
import subprocess

import psutil
import pytest

from conftest import VALID_PORTS, requires

if VALID_PORTS:
    PORT1 = max(VALID_PORTS) + 1
else:
    PORT1 = 50090


@pytest.fixture
@requires("click")
@requires("nostudent")
def run_cli():
    def do_run(arguments=""):
        from click.testing import CliRunner

        from ansys.mapdl.core.cli import main

        if arguments:
            args = list(arguments.split(" "))
        else:
            args = []

        runner = CliRunner()
        result = runner.invoke(main, args)

        assert result.exit_code == 0
        return result.output

    return do_run


@requires("click")
@requires("local")
@requires("nostudent")
@pytest.mark.parametrize("start_instance", [None, True, False])
def test_launch_mapdl_cli(monkeypatch, run_cli, start_instance):
    if start_instance is not None:
        monkeypatch.setenv("PYMAPDL_START_INSTANCE", str(start_instance))
    else:
        monkeypatch.delenv("PYMAPDL_START_INSTANCE", raising=False)

    # Setting a port so it does not collide with the already running instance for testing
    output = run_cli(f"start --port {PORT1}")

    assert "Success: Launched an MAPDL instance " in output
    assert str(PORT1) in output

    # grab ips and port
    pid = int(re.search(r"\(PID=(\d+)\)", output).groups()[0])

    output = run_cli(f"stop --port {PORT1}")
    assert "success" in output.lower()


@requires("click")
@requires("local")
@requires("nostudent")
def test_launch_mapdl_cli_config(run_cli):
    cmds_ = ["start", f"--port {PORT1}", "--jobname myjob"]
    cmd_warnings = [
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
    ]

    cmd = " ".join(cmds_)
    cmd_warnings_ = ["--" + each + " True" for each in cmd_warnings]

    cmd = cmd + " " + " ".join(cmd_warnings_)

    try:
        output = run_cli(cmd)

        assert "Launched an MAPDL instance" in output
        assert str(PORT1) in output

        # assert warnings
        for each in cmd_warnings:
            assert (
                f"The following argument is not allowed in CLI: '{each}'" in output
            ), f"Warning about '{each}' not printed"

        # grab ips and port
        pid = int(re.search(r"\(PID=(\d+)\)", output).groups()[0])
        p = psutil.Process(pid)
        cmdline = " ".join(p.cmdline())

        assert str(PORT1) in cmdline
        assert "myjob" in cmdline

    finally:
        output = run_cli(f"stop --port {PORT1}")
        assert "Success" in output
        assert (
            f"Success: Ansys instances running on port {PORT1} have been stopped"
            in output
        )


@requires("click")
@requires("local")
@requires("nostudent")
@pytest.mark.xfail(reason="Flaky test. See #2435")
def test_launch_mapdl_cli_list(run_cli):

    output = run_cli(f"start --port {PORT1}")

    assert "Success: Launched an MAPDL instance " in output
    assert str(PORT1) in output

    output = run_cli("list")
    assert "running" in output or "sleeping" in output
    assert "Is Instance" in output
    assert len(output.splitlines()) > 2
    assert "ansys" in output.lower() or "mapdl" in output.lower()

    output = run_cli("list -i")
    assert "running" in output or "sleeping" in output
    assert "Is Instance" not in output
    assert len(output.splitlines()) > 2
    assert "ansys" in output.lower() or "mapdl" in output.lower()

    output = run_cli("list -c")
    assert "running" in output or "sleeping" in output
    assert "Command line" in output
    assert "Is Instance" in output
    assert len(output.splitlines()) > 2
    assert "ansys" in output.lower() or "mapdl" in output.lower()

    output = run_cli("list -cwd")
    assert "running" in output or "sleeping" in output
    assert "Command line" not in output
    assert "Working directory" in output
    assert "Is Instance" in output
    assert len(output.splitlines()) > 2
    assert "ansys" in output.lower() or "mapdl" in output.lower()

    output = run_cli("list -l")
    assert "running" in output or "sleeping" in output
    assert "Is Instance" in output
    assert "Command line" in output
    assert len(output.splitlines()) > 2
    assert "ansys" in output.lower() or "mapdl" in output.lower()

    output = run_cli(f"stop --port {PORT1}")
    assert "Success" in output
    assert str(PORT1) in output
    assert (
        f"Success: Ansys instances running on port {PORT1} have been stopped" in output
    )


@requires("click")
def test_convert(run_cli, tmpdir):
    from ansys.mapdl.core._version import __version__

    input_file = str(tmpdir.join("input.apdl"))
    output_file = str(tmpdir.join("output.pymapdl"))

    with open(input_file, "w") as fid:
        fid.write(
            """/prep7
BLOCK,0,1,0,1,0,1
"""
        )

    output = run_cli(f"convert {input_file} -o {output_file}")

    assert input_file in output
    assert output_file in output
    assert "successfully converted" in output

    with open(output_file, "r") as fid:
        converted = fid.read()

    assert "Script generated by ansys-mapdl-core version" in converted
    assert str(__version__) in converted
    assert "from ansys.mapdl.core import launch_mapdl" in converted

    assert (
        """
mapdl.prep7()
mapdl.block(0, 1, 0, 1, 0, 1)"""
        in converted
    )


@requires("click")
def test_convert_pipe():
    cmd = ["echo", "/prep7"]
    cmd2 = ["pymapdl", "convert"]

    process_echo = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    process_pymapdl = subprocess.Popen(
        cmd2, stdin=process_echo.stdout, stdout=subprocess.PIPE
    )

    process_echo.stdout.close()

    stdout = process_pymapdl.stdout.read().decode()

    assert "mapdl.prep7" in stdout
    assert "Script generated by ansys-mapdl-core version" in stdout
    assert "mapdl.exit()" in stdout
