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

"""Tests for ``blocked_commands`` that do not need a running MAPDL"""

import pytest

from ansys.mapdl.core.mapdl_core import _find_blocked_command, _MapdlCore

BLOCKED = frozenset({"/SYS", "/SYP", "/INP"})


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("/SYS,ls", "/SYS"),
        ("/sys,ls", "/SYS"),
        ("  /SYS,ls", "/SYS"),
        ("/S YS,ls", "/SYS"),
        ("/S\tYP,ls", "/SYP"),
        ("'/SYP',ls", "/SYP"),
        ('"/SYS",ls', "/SYS"),
        ("FINISH$/SYP,ls", "/SYP"),
        ("FINISH$ /s yp ,ls", "/SYP"),
        ("RESUME,beam$/S YP,ls,db", "/SYP"),
        ("FINISH\n/INPUT,file,inp", "/INP"),
        ("/INPUT,f,inp", "/INP"),
    ],
)
def test_find_blocked_command_denies(text, expected):
    assert _find_blocked_command(text, BLOCKED) == expected


@pytest.mark.parametrize(
    "text",
    [
        "FINISH ! /SYS,ls",
        "! /SYS",
        "/COM,mentions /SYS",
        "/COM,# x$/SYP,ls",
        "/SY,x",
        "/SYX,x",
        "/IN,x",
        "RESUME,/sysdata/model,db",
        "*USE,macro",
        "/TITLE,/SYS is data",
        "S/SYS,x",
    ],
)
def test_find_blocked_command_allows(text):
    assert _find_blocked_command(text, BLOCKED) is None


def test_find_blocked_command_no_blocked_names_allows_everything():
    assert _find_blocked_command("/SYS,ls$/SYP,ls", frozenset()) is None


def test_find_blocked_command_short_prefix_matches_exactly():
    assert _find_blocked_command("K,1,0,0", frozenset({"K"})) == "K"
    assert _find_blocked_command("KP,1", frozenset({"K"})) is None


def test_find_blocked_command_checks_com_head_itself():
    assert _find_blocked_command("/COM,x$/SYP,ls", frozenset({"/COM"})) == "/COM"


@pytest.fixture
def core():
    # Only the property is exercised; no MAPDL connection is needed.
    return _MapdlCore.__new__(_MapdlCore)


def test_blocked_commands_default_is_empty(core):
    assert core.blocked_commands == frozenset()


def test_blocked_commands_normalizes_names(core):
    core.blocked_commands = ["/input", " /SYS "]
    assert core.blocked_commands == frozenset({"/INP", "/SYS"})


def test_blocked_commands_clears_with_empty_iterable(core):
    core.blocked_commands = ["/SYS"]
    core.blocked_commands = []
    assert core.blocked_commands == frozenset()


def test_blocked_commands_rejects_bare_string(core):
    with pytest.raises(ValueError, match="not a single string"):
        core.blocked_commands = "/SYS"


@pytest.mark.parametrize("names", [[""], ["/SYS", "   "]])
def test_blocked_commands_rejects_empty_name(core, names):
    with pytest.raises(ValueError, match="Invalid blocked command name"):
        core.blocked_commands = names
