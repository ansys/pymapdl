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

import importlib.metadata
import os
import pathlib
import subprocess
import sys
from typing import TYPE_CHECKING

from packaging.requirements import Requirement
from packaging.version import Version
import pytest

if TYPE_CHECKING:
    from ansys.mapdl.core import Mapdl

from conftest import ON_LOCAL

# This should be updated
REQUIREMENTS_STAR_PYTHON = """
ansys-api-mapdl==0.5.2
ansys-mapdl-core==0.70.1
ansys-tools-path==0.7.1
pyansys-tools-versioning==0.6.0
platformdirs==4.3.8 #already in CommonFiles on windows
click==8.1.8
"""


def check_requirements(
    req_file: str | None = None,
) -> dict[str, tuple[bool, Version | None, Version | None]]:
    if req_file is None:
        req_text = REQUIREMENTS_STAR_PYTHON
    else:
        req_text = pathlib.Path(req_file).read_text()

    reqs = req_text.splitlines()
    results: dict[str, tuple[bool, Version | None, Version | None]] = {}

    for req_line in reqs:
        if not req_line.strip() or req_line.strip().startswith("#"):
            # skip blanks/comments
            continue

        # Removing trailing comments
        req_line = req_line.split("#", 1)[0].strip()

        requirement = Requirement(req_line)
        try:
            installed_version = Version(importlib.metadata.version(requirement.name))
        except importlib.metadata.PackageNotFoundError:
            results[requirement.name] = (False, None, None)
            continue

        # Extract the *minimum required version* (if any)
        min_required = None
        for spec in requirement.specifier:
            if spec.operator in (">=", "=="):
                candidate = Version(spec.version)
                if min_required is None or candidate > min_required:
                    min_required = candidate

        if min_required is None or installed_version >= min_required:
            results[requirement.name] = (True, installed_version, min_required)
        else:
            results[requirement.name] = (False, installed_version, min_required)

    return results


class MapdlInProcessRunner:
    def __init__(self, wdir: str, exec_path: str | None = None) -> None:
        self.wdir = str(wdir)
        self.completed_process: subprocess.CompletedProcess[bytes] | None = None
        self._exec_path: str | None = exec_path
        self._output: str | None = None

        venv = os.getenv("MAPDL_PYTHON_ENV", None)
        if not venv:
            # Detecting the venv
            if sys.prefix == sys.base_prefix:
                pytest.warns(
                    "Running from global python interpreter is not recommended."
                )
            venv = sys.prefix

        self.venv = venv

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

    def run(self, cmds: str) -> str:
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
                env={"MAPDL_PYTHON_ENV": self.venv},
                # it does not support shell=True, because it does not
                # generate the out.out file
                # TODO: Why shell should be false in order to generate the output file?
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

        return self.output


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

    mapdl_inprocess = MapdlInProcessRunner(tmp_path)

    return mapdl_inprocess


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

    assert "Starting Python commands" in output_content
    assert "Hello from MAPDL!" in output_content
    assert "test ends" in output_content


def test_python_path(mapdl_inprocess: MapdlInProcessRunner):
    """This test makes sure we are using the correct Python venv"""
    cmds = """
/com, Testing Python path
*PYTHON
import sys
print(sys.executable)
*ENDPY
/com, test ends
"""
    output_content = mapdl_inprocess.run(cmds)
    assert mapdl_inprocess.status_code == 0

    assert "Testing Python path" in output_content
    assert sys.executable in output_content
    assert "test ends" in output_content


@pytest.mark.parametrize("pkg, data", list(check_requirements().items()))
def test_venv_requirements(
    mapdl_inprocess: MapdlInProcessRunner,
    pkg: str,
    data: tuple[bool, Version | None, Version | None],
):
    """Test that the virtual environment has the required packages."""
    ok, installed, required = data
    # Example usage
    for pkg, (ok, installed, required) in check_requirements().items():
        if not ok:
            pytest.fail(f"{pkg} {installed} (needs >= {required})")
