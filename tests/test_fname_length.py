# Copyright (C) 2016 - 2026 ANSYS, Inc. and/or its affiliates.
# Copyright (C) 2016 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
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

"""Tests for the file name length guard that do not need a running MAPDL"""

import pytest

from ansys.mapdl.core.mapdl_core import _MapdlCore

LONG = "a" * 249
MAX = "a" * 248

# One command per filename field that MAPDL crashes or mangles on (issue #4849).
TOO_LONG = [
    f"SAVE,{LONG},db",
    f"RESUME,{LONG},db",
    f"/OUTPUT,{LONG},out",
    f"/INPUT,{LONG},inp",
    f"/INPUT,f,inp,{LONG}",
    f"*CFOPEN,{LONG},txt",
    f"CDWRITE,DB,'{LONG}',cdb",
    f"CDWRITE,ALL,f,cdb,,{LONG},iges",
    f"/COPY,{LONG},db,,f,db",
    f"/COPY,f,db,,{LONG},db",
    f"  save , {LONG}",
]

FITS = [
    f"SAVE,{MAX},db",
    f"CDWRITE,DB,'{MAX}',cdb",
    f"/COPY,{MAX},db,,{MAX},db",
    f"/TITLE,{LONG}",
    "SAVE",
]


@pytest.fixture
def core():
    mapdl = _MapdlCore.__new__(_MapdlCore)
    mapdl._MapdlCore__exited = False
    mapdl._store_commands = True
    mapdl._stored_commands = []
    return mapdl


@pytest.mark.parametrize("command", TOO_LONG)
def test_run_rejects_long_fname(core, command):
    with pytest.raises(ValueError, match="249 characters"):
        core.run(command)
    assert core._stored_commands == []


@pytest.mark.parametrize("command", FITS)
def test_run_accepts_fname_within_limit(core, command):
    core.run(command)
    assert core._stored_commands == [command]


def test_input_strings_rejects_long_fname(core):
    with pytest.raises(ValueError, match="249 characters"):
        core.input_strings(f"/PREP7\nSAVE,{LONG},db")
    assert core._stored_commands == []
