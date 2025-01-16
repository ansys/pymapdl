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

import pytest

from ansys.mapdl.core.launcher.tools import (
    ALLOWABLE_LAUNCH_MAPDL_ARGS,
    check_kwargs,
    pre_check_args,
)
from ansys.mapdl.core.mapdl_core import _ALLOWED_START_PARM
from conftest import NullContext

_ARGS_VALIDS = ALLOWABLE_LAUNCH_MAPDL_ARGS.copy()
_ARGS_VALIDS.extend(_ALLOWED_START_PARM)
_ARGS = _ARGS_VALIDS.copy()
_ARGS.extend(["asdf", "non_valid_argument"])


@pytest.mark.parametrize("arg", _ARGS)
def test_check_kwargs(arg):
    if arg in _ARGS_VALIDS:
        context = NullContext()
    else:
        context = pytest.raises(ValueError)

    with context:
        check_kwargs({"kwargs": {arg: None}})


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
        pre_check_args(args)
