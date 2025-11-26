# Copyright (C) 2016 - 2025 ANSYS, Inc. and/or its affiliates.
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
import subprocess
import sys
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from ansys.mapdl.core import Mapdl

from conftest import ON_LOCAL


class MapdlInProcessRunner:
    def __init__(self, wdir: str, version: float, exec_path: str | None = None) -> None:
        self.wdir = str(wdir)
        self.version = version
        self.completed_process: subprocess.CompletedProcess[bytes] | None = None
        self._exec_path: str | None = exec_path
        self._output: str | None = None

        # Detecting the venv
        if sys.prefix == sys.base_prefix:
            pytest.warns("Running from global python interpreter is not recommended.")
        os.environ["MAPDL_PYTHON_ENV"] = sys.prefix

    @property
    def exec_path(self) -> str:
        if self._exec_path is None:

            self._exec_path = os.getenv("PYMAPDL_MAPDL_EXEC")
            if self._exec_path is None:
                from ansys.tools.common.path import get_mapdl_path

                version: float | None = (
                    float(os.getenv("PYMAPDL_MAPDL_VERSION", 0)) or None
                )
                self._exec_path = get_mapdl_path(version=version)

        if self._exec_path is None:
            raise ValueError(
                "MAPDL executable path is not set. Set the PYMAPDL_MAPDL_EXEC "
                "environment variable or use get_mapdl_path() to find it."
            )

        return self._exec_path

    @property
    def stdout(self) -> str | None:
        """Return the standard output of the completed process. If the process fail, this returns None."""
        if self.completed_process:
            return self.completed_process.stdout.decode()

    @property
    def stderr(self) -> str | None:
        """Return the standard error output of the completed process. If the process fail, this returns None."""
        if self.completed_process:
            return self.completed_process.stderr.decode()

    @property
    def status_code(self) -> float | None:
        """Return the status code of the completed process. If the process fail, this returns None."""
        if self.completed_process:
            return float(self.completed_process.returncode)

    @property
    def exist_output(self) -> bool:
        """Return True if the output file exists, False otherwise."""
        return os.path.exists(os.path.join(self.wdir, "out.out"))

    def output(self) -> str | None:
        if not self._output and self.exist_output:
            with open(os.path.join(self.wdir, "out.out"), "r") as f:
                self._output = f.read()
        return self._output

    def run(self, cmds: str) -> str | None:
        """Run commands in MAPDL on batch mode."""
        with open(os.path.join(self.wdir, "input.mac"), "w") as f:
            f.write(cmds)

        exec_path = self.exec_path
        # Security: Validate the executable path
        if not os.path.isabs(exec_path) or not os.path.isfile(exec_path):
            raise ValueError(
                "MAPDL executable path must be an absolute path to an existing file."
            )

        try:
            args = [
                exec_path,
                "-b",
                "-i",
                "input.mac",
                "-o",
                "out.out",
                os.getenv("PYMAPDL_ADDITIONAL_SWITCHES", ""),
            ]

            self.completed_process = subprocess.run(
                args=args,
                cwd=self.wdir,
                check=True,
                capture_output=True,
                # # it does not support shell=True, because it does not
                # # generate the out.out file
                # # TODO: Why shell should be false in order to generate the output file?
                shell=False,  # nosec B603
            )

        except subprocess.CalledProcessError as e:
            error_msg = (
                f"MAPDL execution failed with return code {e.returncode}.\n"
                f"Command: {' '.join(e.cmd)}\n"
                f"Stdout:\n{e.stdout.decode() if e.stdout else ''}\n"
                f"Stderr:\n{e.stderr.decode() if e.stderr else ''}\n"
            )
            pytest.fail(error_msg)

        return self.output()


@pytest.fixture()
def mapdl_version(mapdl: "Mapdl"):
    return mapdl.version


@pytest.fixture()
def mapdl_inprocess(mapdl_version: float, tmp_path: str) -> MapdlInProcessRunner:

    # check if MAPDL has *PYTHON
    if mapdl_version < 25.2:
        pytest.skip("To test InProcess interface MAPDL 25.2 or higher is required")

    if not ON_LOCAL:
        pytest.skip("InProcess interface can only be tested on local machines")

    if not (os.getenv("TEST_INPROCESS", "").lower() == "true"):
        pytest.skip("Set TEST_INPROCESS environment variable to run them.")

    mapdl_inprocess = MapdlInProcessRunner(tmp_path, version=mapdl_version)

    return mapdl_inprocess


def test_python_path(mapdl_inprocess: MapdlInProcessRunner):
    """This test makes sure we are using the correct Python venv"""
    cmds = """
/com, Testing Python path
*PYTHON
import shutil
print(shutil.which("python"))
*ENDPY
/com, test ends
"""
    output_content = mapdl_inprocess.run(cmds)
    assert mapdl_inprocess.status_code == 0
    assert output_content is not None
    assert "Testing Python path" in output_content
    assert sys.executable.replace("\\\\", "\\").lower() in output_content.lower()
    assert "test ends" in output_content


def test_start_python_from_pymapdl(
    mapdl: "Mapdl", mapdl_inprocess: MapdlInProcessRunner
):
    # calling mapdl_inprocess just to make sure we do not
    # run it in PyMAPDL versions below 25.2
    output = mapdl.input_strings(
        """
*PYTHON
print("Hello from MAPDL")
*ENDPY
"""
    )

    assert output is not None
    assert "START PYTHON COMMAND BLOCK" in output
    assert "Hello from MAPDL" in output
    assert "END PYTHON COMMAND BLOCK" in output


def test_start_python_from_mapdl(mapdl_inprocess: MapdlInProcessRunner):
    """Test that MAPDL starts Python correctly."""
    cmds = """
/com, Starting Python commands
*PYTHON
print('Hello from MAPDL!')
*ENDPY
/com, test ends
"""
    output_content = mapdl_inprocess.run(cmds)
    assert mapdl_inprocess.status_code == 0

    assert output_content is not None
    assert "Starting Python commands" in output_content
    assert "Hello from MAPDL!" in output_content
    assert "test ends" in output_content
