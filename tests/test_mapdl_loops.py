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

"""Unit tests for the ``Mapdl.do`` and ``Mapdl.dowhile`` loop context managers.

These tests do not require a live MAPDL instance: they exercise the context
manager logic against a lightweight fake that mimics only the bits of
:class:`Mapdl <ansys.mapdl.core.mapdl.MapdlBase>` that ``do``/``dowhile`` rely
on. Notably, ``FakeMapdl`` does **not** stub out
:class:`Mapdl.non_interactive <ansys.mapdl.core.mapdl_core._MapdlCore>`: it
relies on the real, inherited :class:`_non_interactive
<ansys.mapdl.core.mapdl_core._MapdlCore._non_interactive>` implementation, so
these tests also guard against a partial ``*DO``/``*DOWHILE`` block leaking
into a later flush through the shared ``_stored_commands`` buffer.
"""

import logging
from unittest.mock import MagicMock

import pytest

from ansys.mapdl.core.errors import MapdlDoLoopLimitError
from ansys.mapdl.core.mapdl_extended import MAX_DO_LOOP_LEVEL, _MapdlExtended


class FakeMapdl(_MapdlExtended):
    """Lightweight double implementing just enough of ``Mapdl`` for testing.

    It bypasses :class:`_MapdlCore.__init__ <ansys.mapdl.core.mapdl_core._MapdlCore>`
    entirely, since that requires a real (or gRPC) connection, but keeps the
    real ``_store_commands``/``_stored_commands``/``non_interactive``
    machinery from :class:`_MapdlCore <ansys.mapdl.core.mapdl_core._MapdlCore>`
    so the actual buffering (and discarding) behavior is exercised.
    """

    def __init__(self):
        self._do_loop_level = 0
        self._store_commands = False
        self._stored_commands = []
        # Commands that were actually "sent" to MAPDL, either directly or
        # through a flush of ``_stored_commands``.
        self.sent_commands = []
        self._log = MagicMock()
        # Avoid the ``self._parent().com(...)`` debug-only branch in
        # ``_non_interactive.__enter__``, since ``com`` is not implemented
        # on this fake.
        self._log.logger.level = logging.WARNING

    def run(self, command, **kwargs):
        if self._store_commands:
            self._stored_commands.append(command)
            return None
        self.sent_commands.append(command)
        return command

    def _flush_stored(self):
        """Mimic ``_MapdlCore._flush_stored`` without touching real MAPDL."""
        self.sent_commands.extend(self._stored_commands)
        self._store_commands = False
        self._stored_commands = []


@pytest.fixture
def fake_mapdl():
    return FakeMapdl()


def test_do_emits_do_and_enddo(fake_mapdl):
    with fake_mapdl.do("i", 1, 10, 2):
        fake_mapdl.run("N,i,i,0,0")

    assert fake_mapdl.sent_commands == ["*DO,i,1,10,2", "N,i,i,0,0", "*ENDDO"]
    assert fake_mapdl._do_loop_level == 0
    assert fake_mapdl._stored_commands == []


def test_dowhile_emits_dowhile_and_enddo(fake_mapdl):
    with fake_mapdl.dowhile("cont"):
        fake_mapdl.run("cont = cont - 1")

    assert fake_mapdl.sent_commands == ["*DOWHILE,cont", "cont = cont - 1", "*ENDDO"]
    assert fake_mapdl._do_loop_level == 0
    assert fake_mapdl._stored_commands == []


def test_do_enters_and_exits_non_interactive_when_not_already_active(fake_mapdl):
    assert fake_mapdl._store_commands is False

    with fake_mapdl.do("i", 1, 10):
        assert fake_mapdl._store_commands is True
        assert fake_mapdl._stored_commands == ["*DO,i,1,10,"]

    assert fake_mapdl._store_commands is False
    assert fake_mapdl._stored_commands == []
    assert fake_mapdl.sent_commands == ["*DO,i,1,10,", "*ENDDO"]


def test_do_does_not_reenter_non_interactive_when_already_active(fake_mapdl):
    with fake_mapdl.non_interactive:
        assert fake_mapdl._store_commands is True

        with fake_mapdl.do("i", 1, 10):
            fake_mapdl.run("body")

        # The nested ``do`` did not flush or exit non-interactive mode
        # itself: everything is still buffered.
        assert fake_mapdl._store_commands is True
        assert fake_mapdl._stored_commands == ["*DO,i,1,10,", "body", "*ENDDO"]
        assert fake_mapdl.sent_commands == []

    assert fake_mapdl._store_commands is False
    assert fake_mapdl._stored_commands == []
    assert fake_mapdl.sent_commands == ["*DO,i,1,10,", "body", "*ENDDO"]


def test_nested_do_and_dowhile_share_the_same_loop_counter(fake_mapdl):
    with fake_mapdl.do("i", 1, 10):
        assert fake_mapdl._do_loop_level == 1
        with fake_mapdl.dowhile("j"):
            assert fake_mapdl._do_loop_level == 2
            fake_mapdl.run("body")
        assert fake_mapdl._do_loop_level == 1

    assert fake_mapdl._do_loop_level == 0
    assert fake_mapdl.sent_commands == [
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

    assert fake_mapdl._do_loop_level == 0
    assert fake_mapdl._store_commands is False

    # No '*ENDDO' was ever queued, and nothing was actually sent to MAPDL:
    # the whole (invalid, unterminated) block was discarded on exit.
    assert fake_mapdl.sent_commands == []

    # Regression: the buffer backing 'non_interactive' must be truncated,
    # not just marked inactive, so the incomplete '*DO' block cannot survive
    # to leak into a later, unrelated flush.
    assert fake_mapdl._stored_commands == []


def test_partial_do_block_does_not_leak_into_a_later_flush(fake_mapdl):
    """A failed ``do`` loop must not poison a subsequent, unrelated one."""
    with pytest.raises(ValueError, match="boom"):
        with fake_mapdl.do("i", 1, 10):
            fake_mapdl.run("body")
            raise ValueError("boom")

    assert fake_mapdl._stored_commands == []
    assert fake_mapdl.sent_commands == []

    # A later, successful loop must only contain its own commands: none of
    # the aborted '*DO,i,1,10,'/'body' fragments should have leaked in.
    with fake_mapdl.do("j", 1, 5):
        fake_mapdl.run("N,j,j,0,0")

    assert fake_mapdl.sent_commands == ["*DO,j,1,5,", "N,j,j,0,0", "*ENDDO"]
    assert fake_mapdl._stored_commands == []


def test_exception_inside_user_owned_non_interactive_discards_everything(fake_mapdl):
    """A nested ``do`` raising inside a user-owned ``non_interactive`` block
    must not leave a dangling partial block behind either."""
    with pytest.raises(ValueError, match="boom"):
        with fake_mapdl.non_interactive:
            with fake_mapdl.do("i", 1, 10):
                fake_mapdl.run("body")
            raise ValueError("boom")

    # The inner loop closed cleanly, but the outer, user-owned block never
    # got to flush because of the exception raised after it: nothing must
    # have been sent, and the buffer must be empty afterward.
    assert fake_mapdl.sent_commands == []
    assert fake_mapdl._stored_commands == []
    assert fake_mapdl._store_commands is False

    # A later, unrelated 'do' loop must not see any leftovers either.
    with fake_mapdl.do("k", 1, 3):
        fake_mapdl.run("N,k,k,0,0")

    assert fake_mapdl.sent_commands == ["*DO,k,1,3,", "N,k,k,0,0", "*ENDDO"]
