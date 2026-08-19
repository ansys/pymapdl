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

"""Unit tests for the ``Mapdl.do`` and ``Mapdl.while_`` loop context managers.

These tests do not require a live MAPDL instance: they exercise the context
manager logic against a lightweight fake that mimics only the bits of
:class:`Mapdl <ansys.mapdl.core.mapdl.MapdlBase>` that ``do``/``while_`` rely
on.
"""

from unittest.mock import MagicMock

import pytest

from ansys.mapdl.core.errors import MapdlDoLoopLimitError
from ansys.mapdl.core.mapdl_extended import MAX_DO_LOOP_LEVEL, _MapdlExtended


class _FakeNonInteractive:
    """Minimal stand-in for ``Mapdl._non_interactive``."""

    def __init__(self, parent):
        self._parent = parent

    def __enter__(self):
        self._parent._store_commands = True
        self._parent.non_interactive_entries += 1

    def __exit__(self, *args):
        self._parent._store_commands = False
        self._parent.non_interactive_exits.append(args)


class FakeMapdl(_MapdlExtended):
    """Lightweight double implementing just enough of ``Mapdl`` for testing.

    It bypasses :class:`_MapdlCore.__init__ <ansys.mapdl.core.mapdl_core._MapdlCore>`
    entirely, since that requires a real (or gRPC) connection.
    """

    def __init__(self):
        self._do_loop_level = 0
        self._store_commands = False
        self.commands = []
        self.non_interactive_entries = 0
        self.non_interactive_exits = []
        self._log = MagicMock()

    def run(self, command, **kwargs):
        self.commands.append(command)
        return command

    @property
    def non_interactive(self):
        return _FakeNonInteractive(self)


@pytest.fixture
def fake_mapdl():
    return FakeMapdl()


def test_do_emits_do_and_enddo(fake_mapdl):
    with fake_mapdl.do("i", 1, 10, 2):
        fake_mapdl.run("N,i,i,0,0")

    assert fake_mapdl.commands == ["*DO,i,1,10,2", "N,i,i,0,0", "*ENDDO"]
    assert fake_mapdl._do_loop_level == 0


def test_while_emits_dowhile_and_enddo(fake_mapdl):
    with fake_mapdl.while_("cont"):
        fake_mapdl.run("cont = cont - 1")

    assert fake_mapdl.commands == ["*DOWHILE,cont", "cont = cont - 1", "*ENDDO"]
    assert fake_mapdl._do_loop_level == 0


def test_do_enters_and_exits_non_interactive_when_not_already_active(fake_mapdl):
    assert fake_mapdl._store_commands is False

    with fake_mapdl.do("i", 1, 10):
        assert fake_mapdl._store_commands is True

    assert fake_mapdl._store_commands is False
    assert fake_mapdl.non_interactive_entries == 1
    assert len(fake_mapdl.non_interactive_exits) == 1


def test_do_does_not_reenter_non_interactive_when_already_active(fake_mapdl):
    with fake_mapdl.non_interactive:
        assert fake_mapdl.non_interactive_entries == 1

        with fake_mapdl.do("i", 1, 10):
            fake_mapdl.run("body")

        # The nested ``do`` did not touch non-interactive mode itself.
        assert fake_mapdl.non_interactive_entries == 1
        assert fake_mapdl._store_commands is True

    assert fake_mapdl._store_commands is False
    assert fake_mapdl.non_interactive_entries == 1
    assert len(fake_mapdl.non_interactive_exits) == 1


def test_nested_do_and_while_share_the_same_loop_counter(fake_mapdl):
    with fake_mapdl.do("i", 1, 10):
        assert fake_mapdl._do_loop_level == 1
        with fake_mapdl.while_("j"):
            assert fake_mapdl._do_loop_level == 2
            fake_mapdl.run("body")
        assert fake_mapdl._do_loop_level == 1

    assert fake_mapdl._do_loop_level == 0
    assert fake_mapdl.commands == [
        "*DO,i,1,10,",
        "*DOWHILE,j",
        "body",
        "*ENDDO",
        "*ENDDO",
    ]


def test_do_loop_nesting_limit_is_enforced(fake_mapdl):
    contexts = [fake_mapdl.do("i", 1, 2) for _ in range(MAX_DO_LOOP_LEVEL + 1)]

    entered = []
    with pytest.raises(MapdlDoLoopLimitError):
        for context in contexts:
            context.__enter__()
            entered.append(context)

    assert fake_mapdl._do_loop_level == MAX_DO_LOOP_LEVEL

    # Clean up the loops we did manage to open.
    for context in reversed(entered):
        context.__exit__(None, None, None)

    assert fake_mapdl._do_loop_level == 0


def test_do_loop_level_is_restored_after_the_limit_is_hit(fake_mapdl):
    for _ in range(MAX_DO_LOOP_LEVEL):
        fake_mapdl.do("i", 1, 2).__enter__()

    with pytest.raises(MapdlDoLoopLimitError):
        with fake_mapdl.do("i", 1, 2):
            pass  # pragma: no cover - should never execute the body

    # The failed attempt to open a loop must not have incremented the
    # counter.
    assert fake_mapdl._do_loop_level == MAX_DO_LOOP_LEVEL


def test_exception_in_do_loop_skips_enddo_and_discards_commands(fake_mapdl):
    with pytest.raises(ValueError, match="boom"):
        with fake_mapdl.do("i", 1, 10):
            fake_mapdl.run("body")
            raise ValueError("boom")

    assert fake_mapdl.commands == ["*DO,i,1,10,", "body"]
    assert fake_mapdl._do_loop_level == 0
    assert fake_mapdl._store_commands is False

    # The non-interactive context was exited with the exception info, so it
    # did not flush.
    assert len(fake_mapdl.non_interactive_exits) == 1
    assert fake_mapdl.non_interactive_exits[0][0] is ValueError
