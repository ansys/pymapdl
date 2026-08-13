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

from unittest.mock import MagicMock, Mock, patch

from ansys.api.mapdl.v0 import mapdl_pb2 as pb_types
import pytest

from ansys.mapdl.core.errors import MapdlExitedError
from ansys.mapdl.core.mapdl_grpc import MapdlGrpc, MapdlRuntimeError


def _make_mock_mapdl():
    """Return a MagicMock carrying the real instance attributes needed by
    the ``_run``/``_send_command`` family of methods.

    Calling ``MapdlGrpc.<method>(mock, ...)`` runs the real method body with
    the mock as ``self``.
    """
    m = MagicMock(spec=MapdlGrpc)
    m._log = MagicMock()
    return m


def test_get_float(mapdl):
    response = pb_types.GetResponse(type=1, dval=123.456)

    with patch.object(mapdl, "_stub", autospec=True) as mock_stub:
        mock_stub.Get.return_value = response
        result = mapdl._get(entity="NODE", entnum="1", item1="U", it1num=1)
        assert result == 123.456


def test_get_string(mapdl):
    response = pb_types.GetResponse(type=2, sval="test_string")

    with patch.object(mapdl, "_stub", autospec=True) as mock_stub:
        mock_stub.Get.return_value = response
        result = mapdl._get(entity="NODE", entnum="1", item1="U", it1num=1)
        assert result == "test_string"


def test_get_fallback(mapdl):
    response = pb_types.GetResponse(type=0)

    with (
        patch.object(mapdl, "_stub", autospec=True) as mock_stub,
        patch.object(mapdl, "run") as mock_run,
    ):

        mock_run.return_value = "VALUE= 789.012"
        mock_stub.Get.return_value = response

        result = mapdl._get(entity="NODE", entnum="1", item1="U", it1num=1)
        assert result == 789.012


def test_get_fallback_string(mapdl):
    response = pb_types.GetResponse(type=0)

    with (
        patch.object(mapdl, "_stub", autospec=True) as mock_stub,
        patch.object(mapdl, "run") as mock_run,
    ):

        mock_run.return_value = "VALUE= test_value"
        mock_stub.Get.return_value = response

        result = mapdl._get(entity="NODE", entnum="1", item1="U", it1num=1)
        assert result == "test_value"


def test_get_lock(mapdl):
    mapdl._get_lock = True

    with pytest.raises(MapdlRuntimeError):
        mapdl._get(entity="NODE", entnum="1", item1="U", it1num=1, timeout=0.5)

    mapdl._get_lock = False


def test_get_invalid_response_type(mapdl):
    response = pb_types.GetResponse(type=3)

    with patch.object(mapdl, "_stub", autospec=True) as mock_stub:
        mock_stub.Get.return_value = response

        with pytest.raises(MapdlRuntimeError):
            mapdl._get(entity="NODE", entnum="1", item1="U", it1num=1)


def test_get_non_interactive_mode(mapdl):
    mapdl._store_commands = True

    with pytest.raises(MapdlRuntimeError):
        mapdl._get(entity="NODE", entnum="1", item1="U", it1num=1)

    # reset
    mapdl._store_commands = False


class TestRunExitedGuard:
    """The liveness guards live in ``_run``, ahead of ``self._busy = True``."""

    @staticmethod
    def _mock_for_run(channel_state="READY", exited=False):
        mock = _make_mock_mapdl()
        mock._mute = False
        mock._channel = Mock()
        mock.channel_state = channel_state
        mock.exited = exited
        mock._exited = exited
        mock._busy = False
        return mock

    @pytest.mark.parametrize("state", ["SHUTDOWN", "TRANSIENT_FAILURE"])
    def test_raises_on_fatal_channel_state(self, state):
        """A dead channel marks the instance exited and raises."""
        mock = self._mock_for_run(channel_state=state)

        with pytest.raises(MapdlExitedError, match=state):
            MapdlGrpc._run(mock, "/PREP7")

        assert mock._exited is True
        mock._send_command.assert_not_called()

    @pytest.mark.parametrize("state", ["IDLE", "READY", "CONNECTING"])
    def test_non_terminal_channel_state_is_not_fatal(self, state):
        """'CONNECTING' is a normal transient and must not kill the instance."""
        mock = self._mock_for_run(channel_state=state)
        mock._send_command.return_value = "OK"

        assert MapdlGrpc._run(mock, "/PREP7") == "OK"
        assert mock._exited is False

    def test_raises_when_already_exited(self):
        """An exited instance refuses to run commands."""
        mock = self._mock_for_run(exited=True)

        with pytest.raises(MapdlExitedError):
            MapdlGrpc._run(mock, "/PREP7")

        mock._send_command.assert_not_called()

    def test_guard_does_not_issue_an_rpc_per_command(self):
        """The guard reads the cached channel state, it does not call '_ctrl'."""
        mock = self._mock_for_run()
        mock._send_command.return_value = "OK"

        MapdlGrpc._run(mock, "/PREP7")

        mock._ctrl.assert_not_called()
        mock.is_alive.assert_not_called()

    def test_busy_is_cleared_when_the_command_raises(self):
        """'_busy' must not stay latched, or the guard is disabled forever."""
        mock = self._mock_for_run()
        mock._send_command.side_effect = MapdlRuntimeError("boom")

        with pytest.raises(MapdlRuntimeError):
            MapdlGrpc._run(mock, "/PREP7")

        assert mock._busy is False


class TestSendCommand:
    """``_send_command`` no longer carries a guard; it just sends."""

    def test_sends_the_command(self):
        """The command reaches the stub and the response is returned."""
        mock = _make_mock_mapdl()
        mock._exited = False
        mock._stub = MagicMock()
        resp = MagicMock()
        resp.response = "OK"
        mock._stub.SendCommand.return_value = resp

        result = MapdlGrpc._send_command(mock, "/PREP7")

        assert result == "OK"
        mock._stub.SendCommand.assert_called_once()
