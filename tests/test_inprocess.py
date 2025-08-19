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
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from ansys.mapdl.core import Mapdl

from conftest import ON_LOCAL


class MapdlInProcessRunner:
    def __init__(self, wdir: str, exec_path: str | None = None) -> None:
        self.wdir = str(wdir)
        self.completed_process: subprocess.CompletedProcess[bytes] | None = None
        self._exec_path: str | None = exec_path

    @property
    def exec_path(self) -> str:
        if self._exec_path is None:

            self._exec_path = os.getenv("PYMAPDL_MAPDL_EXEC")
            if self._exec_path is None:
                from ansys.tools.path import get_mapdl_path

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
        if self.completed_process:
            return self.completed_process.stdout.decode()

    @property
    def stderr(self) -> str | None:
        if self.completed_process:
            return self.completed_process.stderr.decode()

    def run(self, cmds: str) -> str:
        """Simulate running commands in MAPDL."""
        # This is a placeholder for the actual implementation

        with open(os.path.join(self.wdir, "input.mac"), "w") as f:
            f.write(cmds)

        self.completed_process = subprocess.run(
            args=[
                self.exec_path,
                "-b",
                "-i",
                "input.mac",
                "-o",
                "out.out",
                "-dir",
                self.wdir,
            ],
            check=True,
            capture_output=True,
        try:
            self.completed_process = subprocess.run(
                args=[
                    self.exec_path,
                    "-b",
                    "-i",
                    "input.mac",
                    "-o",
                    "out.out",
                    "-dir",
                    self.wdir,
                ],
                check=True,
                capture_output=True,
            )
        except subprocess.CalledProcessError as e:
            error_msg = (
                f"MAPDL execution failed with return code {e.returncode}.\n"
                f"Command: {' '.join(e.cmd)}\n"
                f"Stdout:\n{e.stdout.decode() if e.stdout else ''}\n"
                f"Stderr:\n{e.stderr.decode() if e.stderr else ''}\n"
            )
            pytest.fail(error_msg)

        with open(os.path.join(self.wdir, "out.out"), "r") as f:
            self.output = f.read()

        return self.output


@pytest.fixture()
def mapdl_inprocess(mapdl: "Mapdl", tmp_path) -> MapdlInProcessRunner:

    # check if MAPDL has *PYTHON
    if mapdl.version < 25.2:
        pytest.skip("To test InProcess interface MAPDL 25.2 or higher is required")

    if not ON_LOCAL:
        pytest.skip("InProcess interface can only be tested on local machines")

    if not os.getenv("TEST_INPROCESS", "").lower() != "true":
        pytest.skip(
            "Skipping InProcess tests, set TEST_INPROCESS environment variable to run them"
        )

    mapdl_inprocess = MapdlInProcessRunner(tmp_path)

    return mapdl_inprocess


def test_start_python_from_pymapdl(mapdl, mapdl_inprocess):
    # calling mapdl_inprocess just to make sure we do not
    # run it in PyMAPDL versions below 25.2
    mapdl.input_strings(
        """
    *PYTHON
    print("Hello from MAPDL")
    *ENDPY
    """
    )


def test_start_python(mapdl_inprocess):
    """Test that MAPDL starts Python correctly."""
    cmds = """
    /com, Starting Python commands
    *PYTHON
    print('Hello from MAPDL!')
    *ENDPY
    /com, test ends
    """
    output_content = mapdl_inprocess.run(cmds)

    assert (
        "Hello from MAPDL!" in output_content
    ), "MAPDL did not start Python correctly."
