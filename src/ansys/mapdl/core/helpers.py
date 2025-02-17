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

"""Module for helper functions"""

from functools import namedtuple
import importlib
import os
import sys
from warnings import warn

from ansys.mapdl.core import LOG


def is_installed(package_name: str) -> bool:
    """Check if a package is installed"""
    package_name = package_name.replace("-", ".")

    try:
        importlib.import_module(package_name)

        return True
    except ModuleNotFoundError:  # pragma: no cover
        LOG.debug(f"The module '{package_name}' is not installed.")
        return False


def get_python_version() -> namedtuple:
    return sys.version_info


def run_first_time() -> None:
    """Run this function the first time PyMAPDL is imported"""
    from ansys.mapdl.core import (
        DEPRECATING_MINIMUM_PYTHON_VERSION,
        MINIMUM_PYTHON_VERSION,
        USER_DATA_PATH,
    )

    first_time_file: str = os.path.join(USER_DATA_PATH, ".firstime")

    # Run the first time only
    if not os.path.exists(first_time_file):  # pragma: no cover

        # Create USER_DATA_PATH directory
        if not os.path.exists(USER_DATA_PATH):  # pragma: no cover
            os.makedirs(USER_DATA_PATH)

        # Show warning about Python compatibility
        version_info = get_python_version()

        py_ver = f"{version_info[0]}.{version_info[1]}"
        py_ver_min = f"{MINIMUM_PYTHON_VERSION[0]}.{MINIMUM_PYTHON_VERSION[1]}"

        if (
            version_info[1] == MINIMUM_PYTHON_VERSION[1]
            and DEPRECATING_MINIMUM_PYTHON_VERSION
        ):
            warn(
                f"Support for Python {py_ver} will be dropped in the next minor "
                "release."
            )

        if version_info[1] < MINIMUM_PYTHON_VERSION[1]:
            warn(
                f"Python {py_ver} is not being tested or officially supported. "
                "It is recommended you use a newer version of Python. "
                f"The mininimum supported and tested version is {py_ver_min}.\n\n"
                "**This warning is shown only the first time you run PyMAPDL.**\n"
            )

        with open(first_time_file, "w") as fid:
            fid.write("")


def run_every_import() -> None:
    # Run every time we import PyMAPDL
    from ansys.mapdl.core import _HAS_VISUALIZER, RUNNING_TESTS

    # Apply custom theme
    if _HAS_VISUALIZER:
        from ansys.mapdl.core.plotting.theme import _apply_default_theme

        _apply_default_theme()

    # In case we want to do something specific for testing.
    if RUNNING_TESTS:  # pragma: no cover
        LOG.debug("Running tests on Pytest")
