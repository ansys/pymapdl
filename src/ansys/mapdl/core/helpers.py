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

"""Module for helper functions"""

import importlib
import os
from warnings import warn

from ansys.mapdl.core import LOG


def is_installed(package_name: str) -> bool:
    """Check if a package is installed"""
    try:
        importlib.import_module(package_name)

        return True
    except ModuleNotFoundError:  # pragma: no cover
        LOG.debug(f"The module '{package_name}' is not installed.")
        return False


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
        py_ver = f"{sys.version_info[0]}.{sys.version_info[1]}"
        py_ver_min = f"{MINIMUM_PYTHON_VERSION[0]}.{MINIMUM_PYTHON_VERSION[1]}"

        if (
            sys.version_info[1] == MINIMUM_PYTHON_VERSION[1]
            and DEPRECATING_MINIMUM_PYTHON_VERSION
        ):
            warn(
                f"Support for Python {py_ver} will be dropped in the next minor "
                "release."
            )

        if sys.version_info[1] <= MINIMUM_PYTHON_VERSION[1]:
            warn(
                f"Python {py_ver} is not being tested or officially supported. "
                "It is recommended you use a newer version of Python. "
                f"The mininimum supported and tested version is {py_ver_min}.\n\n"
                "**This warning is shown only the first time you run PyMAPDL.**\n"
            )

        with open(first_time_file, "w") as fid:
            fid.write("")
