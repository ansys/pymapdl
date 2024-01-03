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

import re

import psutil
import pytest

from conftest import requires


@pytest.fixture
@requires("click")
@requires("nostudent")
def run_cli():
    def do_run(arguments=""):
        from click.testing import CliRunner

        from ansys.mapdl.core.cli import launch_mapdl

        if arguments:
            args = list(arguments.split(" "))
        else:
            args = []

        runner = CliRunner()
        result = runner.invoke(launch_mapdl, args)

        assert result.exit_code == 0
        return result.output

    return do_run


@requires("click")
@requires("local")
@requires("nostudent")
def test_launch_mapdl_cli(run_cli):
    output = run_cli()

    # In local
    assert "Success: Launched an MAPDL instance " in output

    # grab ips and port
    pid = int(re.search(r"\(PID=(\d+)\)", output).groups()[0])

    output = run_cli(f"stop --pid {pid}")

    try:
        p = psutil.Process(pid)
        assert not p.status()
    except:
        # An exception means the process is dead?
        pass


@requires("click")
@requires("local")
@requires("nostudent")
def test_launch_mapdl_cli_config(run_cli):
    cmds_ = ["start", "--port 50090", "--jobname myjob"]
    cmd_warnings = [
        "ip",
        "license_server_check",
        "mode",
        "loglevel",
        "cleanup_on_exit",
        "start_instance",
        "clear_on_connect",
        "log_apdl",
        "remove_temp_files",
        "remove_temp_dir_on_exit",
        "verbose_mapdl",
        "print_com",
        "add_env_vars",
        "replace_env_vars",
    ]

    cmd = " ".join(cmds_)
    cmd_warnings_ = ["--" + each + " True" for each in cmd_warnings]

    cmd = cmd + " " + " ".join(cmd_warnings_)

    output = run_cli(cmd)

    assert "Launched an MAPDL instance" in output
    assert "50090" in output

    # assert warnings
    for each in cmd_warnings:
        assert (
            f"The following argument is not allowed in CLI: '{each}'" in output
        ), f"Warning about '{each}' not printed"

    # grab ips and port
    pid = int(re.search(r"\(PID=(\d+)\)", output).groups()[0])
    p = psutil.Process(pid)
    cmdline = " ".join(p.cmdline())

    assert "50090" in cmdline
    assert "myjob" in cmdline

    run_cli(f"stop --pid {pid}")


@requires("click")
@requires("local")
@requires("nostudent")
def test_launch_mapdl_cli_list(run_cli):
    output = run_cli("list")
    assert "running" in output
    assert "Is Instance" in output
    assert len(output.splitlines()) > 2
    assert "ansys" in output.lower() or "mapdl" in output.lower()

    output = run_cli("list -i")
    assert "running" in output
    assert "Is Instance" not in output
    assert len(output.splitlines()) > 2
    assert "ansys" in output.lower() or "mapdl" in output.lower()

    output = run_cli("list -c")
    assert "running" in output
    assert "Command line" in output
    assert "Is Instance" in output
    assert len(output.splitlines()) > 2
    assert "ansys" in output.lower() or "mapdl" in output.lower()

    output = run_cli("list -cwd")
    assert "running" in output
    assert "Command line" not in output
    assert "Working directory" in output
    assert "Is Instance" in output
    assert len(output.splitlines()) > 2
    assert "ansys" in output.lower() or "mapdl" in output.lower()

    output = run_cli("list -l")
    assert "running" in output
    assert "Is Instance" in output
    assert "Command line" in output
    assert len(output.splitlines()) > 2
    assert "ansys" in output.lower() or "mapdl" in output.lower()
