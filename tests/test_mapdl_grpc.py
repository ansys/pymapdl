# Copyright (C) 2016 - 2026 ANSYS, Inc. and/or its affiliates.
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

import subprocess
import threading
from unittest.mock import MagicMock, Mock, patch

from ansys.api.mapdl.v0 import mapdl_pb2 as pb_types
import pytest

from ansys.mapdl.core.mapdl_grpc import MapdlGrpc, MapdlRuntimeError


def _make_mock_mapdl():
    """Return a MagicMock that carries the real instance attributes needed by
    the process-teardown family of methods.

    Calling ``MapdlGrpc.<method>(mock, ...)`` runs the real method body with
    the mock as ``self``.
    """
    m = MagicMock(spec=MapdlGrpc)
    m._process_close_lock = threading.Lock()
    m._log = MagicMock()
    m._stdout_thread = None
    m._stderr_thread = None
    m._startup_stdout_thread = None
    m._mapdl_process = None
    return m


def _make_mock_process(poll_return=None):
    """Return a mock subprocess.Popen with open, closable stdout/stderr."""
    proc = MagicMock(spec=subprocess.Popen)
    proc.poll.return_value = poll_return
    proc.stdout = Mock()
    proc.stdout.closed = False
    proc.stderr = Mock()
    proc.stderr.closed = False
    proc._stdout_file_handle = None
    return proc


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


# ============================================================================
# Unit tests for MapdlGrpc process-teardown methods
# These tests never require a live MAPDL instance.
# ============================================================================


class TestCloseProcessPipes:
    """Tests for MapdlGrpc._close_process_pipes."""

    def test_closes_open_stdout_and_stderr(self):
        """Open stdout and stderr PIPE handles are both closed."""
        mock = _make_mock_mapdl()
        proc = _make_mock_process()

        MapdlGrpc._close_process_pipes(mock, proc)

        proc.stdout.close.assert_called_once()
        proc.stderr.close.assert_called_once()

    def test_skips_already_closed_streams(self):
        """Already-closed streams are not closed again."""
        mock = _make_mock_mapdl()
        proc = _make_mock_process()
        proc.stdout.closed = True
        proc.stderr.closed = True

        MapdlGrpc._close_process_pipes(mock, proc)

        proc.stdout.close.assert_not_called()
        proc.stderr.close.assert_not_called()

    def test_skips_none_streams(self):
        """None stdout/stderr (e.g. file redirect) do not raise."""
        mock = _make_mock_mapdl()
        proc = _make_mock_process()
        proc.stdout = None
        proc.stderr = None

        MapdlGrpc._close_process_pipes(mock, proc)  # must not raise

    def test_oserror_is_logged_not_raised(self):
        """An OSError on close is logged at debug level and not re-raised."""
        mock = _make_mock_mapdl()
        proc = _make_mock_process()
        proc.stdout.close.side_effect = OSError("broken pipe")

        MapdlGrpc._close_process_pipes(mock, proc)  # must not raise

        mock._log.debug.assert_called()

    def test_closes_stdout_file_handle(self):
        """The _stdout_file_handle redirect is closed and nulled out."""
        mock = _make_mock_mapdl()
        proc = _make_mock_process()
        fh = Mock()
        fh.closed = False
        proc._stdout_file_handle = fh

        MapdlGrpc._close_process_pipes(mock, proc)

        fh.close.assert_called_once()
        assert proc._stdout_file_handle is None

    def test_skips_already_closed_file_handle(self):
        """An already-closed _stdout_file_handle is not closed again."""
        mock = _make_mock_mapdl()
        proc = _make_mock_process()
        fh = Mock()
        fh.closed = True
        proc._stdout_file_handle = fh

        MapdlGrpc._close_process_pipes(mock, proc)

        fh.close.assert_not_called()


class TestTerminateProcess:
    """Tests for MapdlGrpc._terminate_process."""

    def test_terminate_called_when_process_running(self):
        """SIGTERM is sent when the process is still alive (poll() is None)."""
        mock = _make_mock_mapdl()
        proc = _make_mock_process(poll_return=None)

        MapdlGrpc._terminate_process(mock, proc)

        proc.terminate.assert_called_once()

    def test_terminate_skipped_when_process_already_exited(self):
        """SIGTERM is not sent when the process has already exited."""
        mock = _make_mock_mapdl()
        proc = _make_mock_process(poll_return=0)

        MapdlGrpc._terminate_process(mock, proc)

        proc.terminate.assert_not_called()

    def test_pipes_are_closed(self):
        """_close_process_pipes is called to close the pipes."""
        mock = _make_mock_mapdl()
        proc = _make_mock_process(poll_return=None)
        mock._close_process_pipes = Mock()

        MapdlGrpc._terminate_process(mock, proc)

        mock._close_process_pipes.assert_called_once_with(proc)

    def test_sigkill_sent_on_timeout(self):
        """SIGKILL is sent when the process does not exit within 2 s."""
        mock = _make_mock_mapdl()
        proc = _make_mock_process(poll_return=None)
        proc.wait.side_effect = [
            subprocess.TimeoutExpired(cmd="mapdl", timeout=2),
            None,
        ]

        MapdlGrpc._terminate_process(mock, proc)

        proc.kill.assert_called_once()

    def test_logs_debug_when_sigkill_also_times_out(self):
        """A debug message is logged when SIGKILL wait also times out."""
        mock = _make_mock_mapdl()
        proc = _make_mock_process(poll_return=None)
        proc.wait.side_effect = [
            subprocess.TimeoutExpired(cmd="mapdl", timeout=2),
            subprocess.TimeoutExpired(cmd="mapdl", timeout=2),
        ]

        MapdlGrpc._terminate_process(mock, proc)

        mock._log.debug.assert_called()


class TestJoinPipeDrainerThreads:
    """Tests for MapdlGrpc._join_pipe_drainer_threads."""

    def test_joins_all_alive_threads(self):
        """All three drainer threads are joined when alive."""
        mock = _make_mock_mapdl()
        for attr in ("_stdout_thread", "_stderr_thread", "_startup_stdout_thread"):
            t = MagicMock(spec=threading.Thread)
            t.is_alive.return_value = True
            setattr(mock, attr, t)

        MapdlGrpc._join_pipe_drainer_threads(mock)

        for attr in ("_stdout_thread", "_stderr_thread", "_startup_stdout_thread"):
            getattr(mock, attr).join.assert_called_once_with(timeout=2)

    def test_skips_none_threads(self):
        """None thread references are silently skipped."""
        mock = _make_mock_mapdl()
        # All three remain None

        MapdlGrpc._join_pipe_drainer_threads(mock)  # must not raise

    def test_skips_dead_threads(self):
        """Threads that are not alive are not joined."""
        mock = _make_mock_mapdl()
        t = MagicMock(spec=threading.Thread)
        t.is_alive.return_value = False
        mock._stdout_thread = t

        MapdlGrpc._join_pipe_drainer_threads(mock)

        t.join.assert_not_called()

    def test_logs_debug_when_thread_does_not_exit(self):
        """A debug message is logged when a thread is still alive after join."""
        mock = _make_mock_mapdl()
        t = MagicMock(spec=threading.Thread)
        t.is_alive.side_effect = [True, True]  # alive before AND after join
        t.name = "_stdout_thread"
        mock._stdout_thread = t

        MapdlGrpc._join_pipe_drainer_threads(mock)

        mock._log.debug.assert_called()


class TestKillProcess:
    """Tests for MapdlGrpc._kill_process (orchestrator)."""

    def test_no_op_when_no_process(self):
        """_kill_process is a no-op when _mapdl_process is None."""
        mock = _make_mock_mapdl()
        mock._terminate_process = Mock()
        mock._join_pipe_drainer_threads = Mock()

        MapdlGrpc._kill_process(mock)

        mock._terminate_process.assert_not_called()
        mock._join_pipe_drainer_threads.assert_called_once()

    def test_terminates_and_joins_when_process_set(self):
        """_terminate_process and _join_pipe_drainer_threads are both called."""
        mock = _make_mock_mapdl()
        mock._mapdl_process = _make_mock_process()
        mock._terminate_process = Mock()
        mock._join_pipe_drainer_threads = Mock()

        MapdlGrpc._kill_process(mock)

        mock._terminate_process.assert_called_once_with(mock._mapdl_process)
        mock._join_pipe_drainer_threads.assert_called_once()

    def test_lock_prevents_concurrent_double_teardown(self):
        """Concurrent calls serialize: the second waits for the first."""
        import time as _time

        mock = _make_mock_mapdl()
        call_log = []

        def slow_terminate(proc):
            call_log.append("start")
            _time.sleep(0.05)
            call_log.append("end")

        mock._terminate_process = slow_terminate
        mock._join_pipe_drainer_threads = Mock()
        mock._mapdl_process = _make_mock_process()

        t1 = threading.Thread(target=MapdlGrpc._kill_process, args=(mock,))
        t2 = threading.Thread(target=MapdlGrpc._kill_process, args=(mock,))
        t1.start()
        _time.sleep(0.01)
        t2.start()
        t1.join(timeout=2)
        t2.join(timeout=2)

        # The two "start"/"end" pairs must not interleave
        assert call_log == ["start", "end", "start", "end"]


class TestCloseGrpcChannel:
    """Tests for MapdlGrpc._close_grpc_channel."""

    def test_closes_channel_and_nulls_reference(self):
        """The channel's close() is called and _channel is set to None."""
        mock = _make_mock_mapdl()
        channel = Mock()
        mock._channel = channel

        MapdlGrpc._close_grpc_channel(mock)

        channel.close.assert_called_once()
        assert mock._channel is None

    def test_noop_when_channel_is_none(self):
        """No error when _channel is already None."""
        mock = _make_mock_mapdl()
        mock._channel = None

        MapdlGrpc._close_grpc_channel(mock)  # must not raise

    def test_idempotent_second_call(self):
        """Calling twice is safe — second call is a no-op."""
        mock = _make_mock_mapdl()
        channel = Mock()
        mock._channel = channel

        MapdlGrpc._close_grpc_channel(mock)
        MapdlGrpc._close_grpc_channel(mock)

        channel.close.assert_called_once()

    def test_exception_on_close_is_logged_not_raised(self):
        """An exception from channel.close() is logged, not re-raised."""
        mock = _make_mock_mapdl()
        channel = Mock()
        channel.close.side_effect = RuntimeError("channel already gone")
        mock._channel = channel

        MapdlGrpc._close_grpc_channel(mock)  # must not raise

        mock._log.debug.assert_called()
        assert mock._channel is None


class TestSendCommandExitedGuard:
    """Tests that _send_command raises MapdlExitedError when the instance has exited."""

    def test_raises_mapdle_exited_error_when_exited(self):
        """_send_command raises MapdlExitedError when _exited is True."""
        from ansys.mapdl.core.errors import MapdlExitedError

        mock = _make_mock_mapdl()
        mock._exited = True

        with pytest.raises(MapdlExitedError):
            MapdlGrpc._send_command(mock, "/PREP7")

    def test_does_not_raise_when_not_exited(self):
        """_send_command proceeds normally when _exited is False."""
        from unittest.mock import MagicMock

        mock = _make_mock_mapdl()
        mock._exited = False
        mock._stub = MagicMock()
        resp = MagicMock()
        resp.response = "OK"
        mock._stub.SendCommand.return_value = resp

        result = MapdlGrpc._send_command(mock, "/PREP7")

        assert result == "OK"
        mock._stub.SendCommand.assert_called_once()

    def test_send_command_stream_raises_when_exited(self):
        """_send_command_stream raises MapdlExitedError when _exited is True."""
        from ansys.mapdl.core.errors import MapdlExitedError

        mock = _make_mock_mapdl()
        mock._exited = True

        with pytest.raises(MapdlExitedError):
            MapdlGrpc._send_command_stream(mock, "/PREP7")
