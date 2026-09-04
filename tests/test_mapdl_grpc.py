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

import gc
import subprocess
import threading
import time
from types import MethodType
from unittest.mock import MagicMock, Mock, patch
import weakref

from ansys.api.mapdl.v0 import mapdl_pb2 as pb_types
import grpc
import pytest

from ansys.mapdl.core import mapdl_grpc
from ansys.mapdl.core.errors import MapdlExitedError
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
    m._channel = None
    m._connectivity_callback = None
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

    def test_exiting_suppresses_logging_when_thread_does_not_exit(self):
        """``exiting=True`` suppresses the "did not exit in time" debug log."""
        mock = _make_mock_mapdl()
        t = MagicMock(spec=threading.Thread)
        t.is_alive.side_effect = [True, True]  # alive before AND after join
        t.name = "_stdout_thread"
        mock._stdout_thread = t

        MapdlGrpc._join_pipe_drainer_threads(mock, exiting=True)

        t.join.assert_called_once_with(timeout=2)
        mock._log.debug.assert_not_called()


class TestKillProcess:
    """Tests for MapdlGrpc._kill_process (orchestrator)."""

    def test_no_op_when_no_process(self):
        """_kill_process is a no-op when _mapdl_process is None."""
        mock = _make_mock_mapdl()
        mock._terminate_process = Mock()

        MapdlGrpc._kill_process(mock)

        mock._terminate_process.assert_not_called()

    def test_terminates_when_process_set(self):
        """_terminate_process is called; joining is deferred to _close_process."""
        mock = _make_mock_mapdl()
        mock._mapdl_process = _make_mock_process()
        mock._terminate_process = Mock()

        MapdlGrpc._kill_process(mock)

        mock._terminate_process.assert_called_once_with(mock._mapdl_process)

    def test_lock_prevents_concurrent_double_teardown(self):
        """Concurrent calls serialize: the second waits for the first."""
        mock = _make_mock_mapdl()
        call_log = []
        t1_started = threading.Event()
        release_t1 = threading.Event()

        def slow_terminate(proc):
            call_log.append("start")
            t1_started.set()
            # t1 holds _process_close_lock for the whole call, so t2 is
            # guaranteed to block on it until release_t1 is set below,
            # regardless of scheduling — no arbitrary sleep needed.
            release_t1.wait(timeout=2)
            call_log.append("end")

        mock._terminate_process = slow_terminate
        mock._mapdl_process = _make_mock_process()

        t1 = threading.Thread(target=MapdlGrpc._kill_process, args=(mock,))
        t2 = threading.Thread(target=MapdlGrpc._kill_process, args=(mock,))
        t1.start()
        assert t1_started.wait(timeout=2)

        t2.start()
        release_t1.set()

        t1.join(timeout=2)
        t2.join(timeout=2)

        # The two "start"/"end" pairs must not interleave
        assert call_log == ["start", "end", "start", "end"]


class TestGetProcessExitSignal:
    """Tests for MapdlGrpc._get_process_exit_signal."""

    def test_no_process_handle(self):
        """Returns None when no process handle is stored."""
        mock = _make_mock_mapdl()
        mock._mapdl_process = None

        assert MapdlGrpc._get_process_exit_signal(mock) is None

    def test_handle_without_poll(self):
        """Returns None when the handle has no 'poll' method (e.g. a bare
        psutil.Process from a remote/heuristic match)."""
        mock = _make_mock_mapdl()
        mock._mapdl_process = object()

        assert MapdlGrpc._get_process_exit_signal(mock) is None

    def test_process_still_running(self):
        """Returns None when poll() reports the process is still alive."""
        mock = _make_mock_mapdl()
        mock._mapdl_process = _make_mock_process(poll_return=None)

        assert MapdlGrpc._get_process_exit_signal(mock) is None

    def test_process_exited_normally(self):
        """Returns None for a non-negative (non-signal) return code."""
        mock = _make_mock_mapdl()
        mock._mapdl_process = _make_mock_process(poll_return=0)

        assert MapdlGrpc._get_process_exit_signal(mock) is None

    def test_process_killed_by_sigkill(self):
        """Returns 9 (SIGKILL) when poll() reports -9."""
        mock = _make_mock_mapdl()
        mock._mapdl_process = _make_mock_process(poll_return=-9)

        assert MapdlGrpc._get_process_exit_signal(mock) == 9

    def test_process_killed_by_other_signal(self):
        """Returns the signal number for any other negative return code."""
        mock = _make_mock_mapdl()
        mock._mapdl_process = _make_mock_process(poll_return=-11)  # SIGSEGV

        assert MapdlGrpc._get_process_exit_signal(mock) == 11


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
        mock._stub.SendCommand.future.return_value.result.return_value = resp

        result = MapdlGrpc._send_command(mock, "/PREP7")

        assert result == "OK"
        mock._stub.SendCommand.future.assert_called_once()


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

    def test_unsubscribes_callback_before_closing(self):
        """The connectivity callback is removed before the channel is closed."""
        mock = _make_mock_mapdl()
        channel = Mock()
        callback = lambda connectivity: None  # noqa: E731
        mock._channel = channel
        mock._connectivity_callback = callback

        MapdlGrpc._close_grpc_channel(mock)

        channel.unsubscribe.assert_called_once_with(callback)
        channel.close.assert_called_once()
        assert mock._connectivity_callback is None
        # Enforce ordering: unsubscribe() must happen strictly before close(),
        # so a regression that swaps the order is caught even though both
        # methods are still called exactly once.
        method_names = [call[0] for call in channel.mock_calls]
        assert method_names.index("unsubscribe") < method_names.index("close")

    def test_unsubscribe_failure_does_not_prevent_close(self):
        """A failing unsubscribe() is logged and close() still runs."""
        mock = _make_mock_mapdl()
        channel = Mock()
        channel.unsubscribe.side_effect = RuntimeError("not subscribed")
        mock._channel = channel
        mock._connectivity_callback = lambda connectivity: None  # noqa: E731

        MapdlGrpc._close_grpc_channel(mock)  # must not raise

        channel.close.assert_called_once()

    def test_exiting_suppresses_close_error_logging(self):
        """``exiting=True`` suppresses debug logging, even on close() failure."""
        mock = _make_mock_mapdl()
        channel = Mock()
        channel.close.side_effect = RuntimeError("channel already gone")
        mock._channel = channel

        MapdlGrpc._close_grpc_channel(mock, exiting=True)  # must not raise

        mock._log.debug.assert_not_called()
        assert mock._channel is None

    def test_exiting_suppresses_unsubscribe_error_logging(self):
        """``exiting=True`` also suppresses logging of unsubscribe() failures."""
        mock = _make_mock_mapdl()
        channel = Mock()
        channel.unsubscribe.side_effect = RuntimeError("not subscribed")
        mock._channel = channel
        mock._connectivity_callback = lambda connectivity: None  # noqa: E731

        MapdlGrpc._close_grpc_channel(mock, exiting=True)  # must not raise

        mock._log.debug.assert_not_called()
        channel.close.assert_called_once()


class TestConnectivityCallbackDoesNotLeakInstance:
    """The gRPC poll thread must not keep the MapdlGrpc instance alive.

    The callback registered by ``_subscribe_to_channel`` is held by gRPC for as
    long as the subscription lasts.  A strong reference to ``self`` there makes
    the instance uncollectable, so ``__del__`` never runs and the channel is
    never closed.
    """

    def test_callback_holds_only_a_weak_reference(self):
        """The instance is garbage-collected even while the callback lives on."""

        class _Dummy:
            """Minimal stand-in exposing what _subscribe_to_channel touches."""

            def __init__(self, channel):
                self._log = MagicMock()
                self._channel = channel
                self._channel_state = None
                self._connectivity_callback = None
                self._start_ping_abuse_probe = MagicMock()

            _subscribe_to_channel = MapdlGrpc._subscribe_to_channel

        channel = Mock()
        dummy = _Dummy(channel)
        dummy._subscribe_to_channel()

        # gRPC keeps the callback alive; emulate that.
        callback = channel.subscribe.call_args[0][0]
        ref = weakref.ref(dummy)

        del dummy
        gc.collect()

        assert ref() is None, "the connectivity callback leaked the instance"

        # A callback firing after collection must not raise.
        callback("READY")

    def test_callback_updates_state_while_instance_is_alive(self):
        """The weak reference still forwards updates for a live instance."""

        class _Dummy:
            def __init__(self, channel):
                self._log = MagicMock()
                self._channel = channel
                self._channel_state = None
                self._connectivity_callback = None
                self._start_ping_abuse_probe = MagicMock()

            _subscribe_to_channel = MapdlGrpc._subscribe_to_channel

        channel = Mock()
        dummy = _Dummy(channel)
        dummy._subscribe_to_channel()

        callback = channel.subscribe.call_args[0][0]
        callback("READY")

        assert dummy._channel_state == "READY"
        assert dummy._connectivity_callback is callback


class TestConnectivityCancelsInFlightCall:
    """The connectivity callback cancels a call once the channel is confirmed
    dead, instead of leaving it to hang until MAPDL eventually answers."""

    class _Dummy:
        """Minimal stand-in exposing what the connectivity callback touches."""

        def __init__(self, channel):
            self._log = MagicMock()
            self._channel = channel
            self._channel_state = None
            self._connectivity_callback = None
            self._current_call = None
            self._current_call_lock = threading.Lock()
            self._start_ping_abuse_probe = MagicMock()

        _subscribe_to_channel = MapdlGrpc._subscribe_to_channel
        _cancel_call_if_pending = MapdlGrpc._cancel_call_if_pending

    def test_cancels_call_when_channel_becomes_transient_failure(self):
        """A pending call is cancelled once the channel goes unhealthy."""
        channel = Mock()
        dummy = self._Dummy(channel)
        dummy._subscribe_to_channel()
        callback = channel.subscribe.call_args[0][0]

        call = Mock()
        call.done.return_value = False
        dummy._current_call = call

        callback(grpc.ChannelConnectivity.TRANSIENT_FAILURE)

        call.cancel.assert_called_once()

    def test_cancels_call_when_channel_shuts_down(self):
        """A pending call is cancelled once the channel shuts down."""
        channel = Mock()
        dummy = self._Dummy(channel)
        dummy._subscribe_to_channel()
        callback = channel.subscribe.call_args[0][0]

        call = Mock()
        call.done.return_value = False
        dummy._current_call = call

        callback(grpc.ChannelConnectivity.SHUTDOWN)

        call.cancel.assert_called_once()

    def test_does_not_cancel_on_ready(self):
        """A healthy transition must not touch any tracked call."""
        channel = Mock()
        dummy = self._Dummy(channel)
        dummy._subscribe_to_channel()
        callback = channel.subscribe.call_args[0][0]

        call = Mock()
        call.done.return_value = False
        dummy._current_call = call

        callback(grpc.ChannelConnectivity.READY)

        call.cancel.assert_not_called()

    def test_does_not_cancel_an_already_completed_call(self):
        """A call that already finished must not be cancelled."""
        channel = Mock()
        dummy = self._Dummy(channel)
        dummy._subscribe_to_channel()
        callback = channel.subscribe.call_args[0][0]

        call = Mock()
        call.done.return_value = True
        dummy._current_call = call

        callback(grpc.ChannelConnectivity.TRANSIENT_FAILURE)

        call.cancel.assert_not_called()

    def test_no_error_when_no_call_is_in_flight(self):
        """The callback must not raise when nothing is currently tracked."""
        channel = Mock()
        dummy = self._Dummy(channel)
        dummy._subscribe_to_channel()
        callback = channel.subscribe.call_args[0][0]

        callback(grpc.ChannelConnectivity.TRANSIENT_FAILURE)  # must not raise


class TestTrackCallAndUntrackCall:
    """``_track_call``/``_untrack_call`` are the only two places allowed to
    mutate '_current_call', both funnelling through '_current_call_lock'."""

    class _Dummy:
        """Minimal stand-in exposing what these methods touch."""

        def __init__(self):
            self._current_call = None
            self._current_call_lock = threading.Lock()

        _track_call = MapdlGrpc._track_call
        _untrack_call = MapdlGrpc._untrack_call

    def test_track_call_records_the_call(self):
        """Tracking a call exposes it as '_current_call'."""
        dummy = self._Dummy()
        call = Mock()

        dummy._track_call(call)

        assert dummy._current_call is call

    def test_untrack_call_clears_its_own_call(self):
        """Untracking the currently tracked call clears it."""
        dummy = self._Dummy()
        call = Mock()
        dummy._track_call(call)

        dummy._untrack_call(call)

        assert dummy._current_call is None

    def test_untrack_call_does_not_clear_a_newer_call(self):
        """A newer call tracked by a concurrent invocation is not cleared by
        an older one being untracked afterwards."""
        dummy = self._Dummy()
        call_a = Mock()
        call_b = Mock()
        dummy._track_call(call_a)

        # Simulate a second, concurrent call replacing the tracked call
        # before the first one is untracked.
        dummy._track_call(call_b)
        dummy._untrack_call(call_a)

        assert dummy._current_call is call_b


class TestWatchedCall:
    """``_watched_call`` tracks and releases the in-flight call."""

    class _Dummy:
        """Minimal stand-in exposing what '_watched_call' touches."""

        def __init__(self):
            self._current_call = None
            self._current_call_lock = threading.Lock()

        _track_call = MapdlGrpc._track_call
        _untrack_call = MapdlGrpc._untrack_call
        _watched_call = MapdlGrpc._watched_call

    def test_tracks_call_and_clears_it_afterwards(self):
        """The call is exposed as '_current_call' only while inside the
        context manager."""
        dummy = self._Dummy()

        call = Mock()
        with dummy._watched_call(call) as tracked:
            assert tracked is call
            assert dummy._current_call is call

        assert dummy._current_call is None

    def test_clears_only_its_own_call(self):
        """A newer call tracked by a concurrent invocation is not cleared."""
        dummy = self._Dummy()

        call_a = Mock()
        call_b = Mock()
        with dummy._watched_call(call_a):
            # Simulate a second, concurrent call replacing the tracked call
            # before the first one's context manager exits.
            dummy._current_call = call_b

        assert dummy._current_call is call_b


class TestPingAbuseProbe:
    """The background probe thread keeps long-running calls from tripping the
    MAPDL gRPC server's ping-abuse protection (see ``PING_ABUSE_INTERVAL_S``).
    """

    class _Dummy:
        """Minimal stand-in exposing what the probe methods touch."""

        def __init__(self):
            self._log = MagicMock()
            self._ping_probe_stop_event = threading.Event()
            self._ping_probe_thread = None
            self._ctrl = MagicMock()

        _ping_abuse_probe_loop = MapdlGrpc._ping_abuse_probe_loop
        _start_ping_abuse_probe = MapdlGrpc._start_ping_abuse_probe
        _stop_ping_abuse_probe = MapdlGrpc._stop_ping_abuse_probe

    def test_start_spawns_a_daemon_thread(self):
        """Starting the probe creates a running daemon thread."""
        dummy = self._Dummy()

        dummy._start_ping_abuse_probe()

        assert dummy._ping_probe_thread is not None
        assert dummy._ping_probe_thread.is_alive()
        assert dummy._ping_probe_thread.daemon

        dummy._stop_ping_abuse_probe()

    def test_start_is_a_noop_when_already_running(self):
        """Calling start twice does not replace a live thread."""
        dummy = self._Dummy()
        dummy._start_ping_abuse_probe()
        first_thread = dummy._ping_probe_thread

        dummy._start_ping_abuse_probe()

        assert dummy._ping_probe_thread is first_thread

        dummy._stop_ping_abuse_probe()

    def test_stop_joins_and_clears_the_thread(self):
        """Stopping the probe joins the thread and clears the reference."""
        dummy = self._Dummy()
        dummy._start_ping_abuse_probe()

        dummy._stop_ping_abuse_probe()

        assert dummy._ping_probe_thread is None
        assert dummy._ping_probe_stop_event.is_set()

    def test_stop_is_a_noop_when_never_started(self):
        """Stopping a probe that was never started must not raise."""
        dummy = self._Dummy()

        dummy._stop_ping_abuse_probe()  # must not raise

        assert dummy._ping_probe_thread is None

    def test_loop_probes_with_ctrl_version_and_survives_rpc_errors(self):
        """Each wake-up issues a bounded ``Ctrl("VERSION")`` probe; a failure
        is logged, not raised, so the loop keeps running."""
        dummy = self._Dummy()
        dummy._ctrl.side_effect = grpc.RpcError("boom")

        # Make the stop event "time out" exactly once, then report a stop
        # request, so the loop body runs exactly one iteration.
        wait_calls = []

        def fake_wait(timeout):
            wait_calls.append(timeout)
            return len(wait_calls) > 1

        dummy._ping_probe_stop_event.wait = fake_wait

        dummy._ping_abuse_probe_loop()

        dummy._ctrl.assert_called_once()
        assert dummy._ctrl.call_args[0][0] == "VERSION"
        assert "timeout" in dummy._ctrl.call_args[1]
        assert dummy._log.debug.called


class TestDisconnectButLeaveMapdlRunning:
    """``exit()`` always releases the client side, even when MAPDL survives.

    Closing a gRPC channel does not stop the MAPDL server, so the paths that
    deliberately leave MAPDL running must still release the channel and the
    PIPE-drainer threads, otherwise their daemon threads leak.
    """

    @staticmethod
    def _mock_for_exit(start_instance=True, launched=True):
        mock = _make_mock_mapdl()
        mock.exited = False
        mock._exited = False
        mock._exiting = False
        mock._path = ""
        mock._start_instance = start_instance
        mock._launched = launched
        return mock

    @pytest.mark.parametrize(
        "start_instance,launched", [(False, True), (True, False), (False, False)]
    )
    def test_disconnects_when_pymapdl_did_not_launch_mapdl(
        self, start_instance, launched
    ):
        """MAPDL is left running, but the channel is released."""
        mock = self._mock_for_exit(start_instance, launched)

        MapdlGrpc.exit(mock)

        mock._disconnect_but_leave_mapdl_running.assert_called_once()
        mock._release_resources.assert_not_called()

    def test_disconnects_when_building_the_gallery(self):
        """Each gallery example owns its instance, so the channel must close."""
        mock = self._mock_for_exit()

        with patch("ansys.mapdl.core.BUILDING_GALLERY", True):
            MapdlGrpc.exit(mock)

        mock._disconnect_but_leave_mapdl_running.assert_called_once()
        mock._release_resources.assert_not_called()

    def test_force_still_releases_everything(self):
        """force=True performs the full teardown instead."""
        mock = self._mock_for_exit(start_instance=False, launched=False)

        MapdlGrpc.exit(mock, force=True)

        mock._release_resources.assert_called_once()
        mock._disconnect_but_leave_mapdl_running.assert_not_called()

    def test_closes_channel_joins_threads_and_marks_exited(self):
        """The helper releases both resources and reports the instance dead."""
        mock = _make_mock_mapdl()
        mock._exited = False

        MapdlGrpc._disconnect_but_leave_mapdl_running(mock)

        mock._close_grpc_channel.assert_called_once()
        mock._join_pipe_drainer_threads.assert_called_once()
        assert mock._exited is True

    def test_a_failing_close_does_not_prevent_the_join(self):
        """Each step is independent so one failure cannot leak the other."""
        mock = _make_mock_mapdl()
        mock._exited = False
        mock._close_grpc_channel.side_effect = RuntimeError("boom")

        MapdlGrpc._disconnect_but_leave_mapdl_running(mock)

        mock._join_pipe_drainer_threads.assert_called_once()
        assert mock._exited is True

    def test_a_failing_join_is_logged_on_the_deterministic_path(self):
        """A failure joining the PIPE-drainer threads is logged when exiting=False.

        Complements ``test_a_failing_close_does_not_prevent_the_join``, which
        only exercises the channel-close failure branch: this covers the
        analogous failure branch for ``_join_pipe_drainer_threads``.
        """
        mock = _make_mock_mapdl()
        mock._exited = False
        mock._join_pipe_drainer_threads.side_effect = RuntimeError("boom")

        MapdlGrpc._disconnect_but_leave_mapdl_running(mock)

        mock._close_grpc_channel.assert_called_once()
        mock._log.debug.assert_called_once()
        assert mock._exited is True

    def test_exiting_is_forwarded_to_channel_close_and_thread_join(self):
        """``exiting=True`` is forwarded to both helper calls.

        Regression test for https://github.com/ansys/pymapdl/issues/4728:
        ``__del__``'s early-exit branch relies on this forwarding to suppress
        logging that is unreliable during interpreter shutdown.
        """
        mock = _make_mock_mapdl()
        mock._exited = False

        MapdlGrpc._disconnect_but_leave_mapdl_running(mock, exiting=True)

        mock._close_grpc_channel.assert_called_once_with(exiting=True)
        mock._join_pipe_drainer_threads.assert_called_once_with(exiting=True)
        assert mock._exited is True

    def test_exiting_suppresses_own_error_logging(self):
        """``exiting=True`` suppresses this method's own debug logging."""
        mock = _make_mock_mapdl()
        mock._exited = False
        mock._close_grpc_channel.side_effect = RuntimeError("boom")
        mock._join_pipe_drainer_threads.side_effect = RuntimeError("boom too")

        MapdlGrpc._disconnect_but_leave_mapdl_running(mock, exiting=True)

        mock._log.debug.assert_not_called()
        assert mock._exited is True

    def test_already_exited_still_releases_the_client_side(self):
        """A crashed instance flagged by an error handler must still be freed."""
        mock = self._mock_for_exit()
        mock.exited = True
        mock._exited = True

        MapdlGrpc.exit(mock)

        mock._disconnect_but_leave_mapdl_running.assert_called_once()
        mock._release_resources.assert_not_called()


class TestEnsureChannel:
    """A closed gRPC channel cannot be reopened; it must be rebuilt."""

    def test_rebuilds_and_resubscribes_when_the_channel_was_closed(self):
        """'_close_grpc_channel' clears '_channel', so reconnecting rebuilds it."""
        mock = _make_mock_mapdl()
        mock._channel = None
        mock._ip = "127.0.0.1"
        mock._port = 50052
        new_channel = Mock()
        mock._create_channel.return_value = new_channel

        MapdlGrpc._ensure_channel(mock)

        mock._create_channel.assert_called_once_with("127.0.0.1", 50052)
        assert mock._channel is new_channel
        mock._subscribe_to_channel.assert_called_once()

    def test_is_a_no_op_when_the_channel_is_still_open(self):
        """An open channel must never be replaced underneath a live session."""
        mock = _make_mock_mapdl()
        channel = Mock()
        mock._channel = channel

        MapdlGrpc._ensure_channel(mock)

        mock._create_channel.assert_not_called()
        mock._subscribe_to_channel.assert_not_called()
        assert mock._channel is channel

    def test_reconnect_rebuilds_the_channel_and_clears_exited(self):
        """'reconnect_to_mapdl' resurrects an instance released by 'exit()'."""
        mock = _make_mock_mapdl()
        mock._timeout = 5
        mock._exited = True

        MapdlGrpc.reconnect_to_mapdl(mock)

        mock._connect_to_mapdl.assert_called_once_with(5)
        assert mock._exited is False

    def test_connect_to_mapdl_ensures_the_channel_first(self):
        """The channel must exist before '_multi_connect' uses it."""
        mock = _make_mock_mapdl()

        MapdlGrpc._connect_to_mapdl(mock, timeout=5)

        mock._ensure_channel.assert_called_once()
        mock._multi_connect.assert_called_once_with(timeout=5)


class TestCtrlExitHardTimeout:
    """``_ctrl("exit")`` must never hang forever, even if the underlying
    gRPC channel/transport does not honor its own per-call deadline once the
    server process has died (observed on Windows/WNUA)."""

    class _Dummy:
        """Minimal stand-in exposing what '_ctrl' touches for the EXIT path."""

        def __init__(self, stub):
            self._log = MagicMock()
            self._stub = stub
            self.transport_mode = "wnua"

        _ctrl = MapdlGrpc._ctrl

    def test_returns_promptly_when_the_stub_raises_the_expected_error(self):
        """The common case: the connection drops and the stub raises the
        expected gRPC error almost immediately."""
        stub = Mock()
        # Make it look like the expected type (used by MapdlGrpc._ctrl)
        from ansys.mapdl.core.mapdl_grpc import _InactiveRpcError

        stub.Ctrl.side_effect = _InactiveRpcError(MagicMock())
        dummy = self._Dummy(stub)

        dummy._ctrl("exit")

        stub.Ctrl.assert_called_once()

    def test_reraises_unexpected_errors(self):
        """Any error other than the expected gRPC "connection closed" family
        must still propagate to the caller."""
        stub = Mock()
        stub.Ctrl.side_effect = ValueError("boom")
        dummy = self._Dummy(stub)

        with pytest.raises(ValueError, match="boom"):
            dummy._ctrl("exit")

    def test_does_not_hang_when_the_stub_call_never_returns(self):
        """If the blocking 'stub.Ctrl' call never returns (simulating a
        transport that does not honor its own deadline), '_ctrl' must give
        up after its own hard wall-clock timeout instead of hanging
        forever."""
        never_return = threading.Event()

        def blocking_call(*args, **kwargs):
            # Block far longer than the hard timeout used below; the
            # calling thread must not wait for this.
            never_return.wait(30)
            return None

        stub = Mock()
        stub.Ctrl.side_effect = blocking_call
        dummy = self._Dummy(stub)

        start = time.time()
        dummy._ctrl("exit", timeout=0.1)
        elapsed = time.time() - start

        # hard_timeout = timeout (0.1) + buffer (5.0) = 5.1s; give some slack
        assert elapsed < 8.0
        dummy._log.warning.assert_called_once()

        never_return.set()


class TestCloseGrpcChannelHardTimeout:
    """``_close_grpc_channel`` must never hang forever.

    ``grpc.Channel.close`` cancels the outstanding calls and then waits,
    without any timeout of its own, for gRPC's channel-spin thread to drain
    ``integrated_call_states`` and ``connectivity_due``.  When that daemon
    thread cannot run any more, the wait never ends.  This was observed in
    CI as a job that stalled for the whole job budget after the test session
    had already reported success, with the main thread blocked in
    ``__del__`` -> ``_close_grpc_channel`` -> ``grpc.Channel.close``.
    """

    @staticmethod
    def _dummy(channel):
        """Build a minimal stand-in exposing what '_close_grpc_channel' touches."""
        dummy = Mock()
        dummy._channel = channel
        dummy._connectivity_callback = Mock()
        dummy._close_grpc_channel = MethodType(MapdlGrpc._close_grpc_channel, dummy)
        return dummy

    def test_closes_the_channel_and_clears_the_references(self):
        """The healthy path still unsubscribes and closes the channel."""
        channel = Mock()
        dummy = self._dummy(channel)
        callback = dummy._connectivity_callback

        dummy._close_grpc_channel()

        channel.unsubscribe.assert_called_once_with(callback)
        channel.close.assert_called_once()
        assert dummy._channel is None
        assert dummy._connectivity_callback is None

    def test_is_a_noop_without_a_channel(self):
        """Calling it twice, or on an instance that never connected, is safe."""
        dummy = self._dummy(None)

        dummy._close_grpc_channel()

        assert dummy._channel is None

    def test_does_not_hang_when_close_never_returns(self):
        """A wedged 'channel.close' must not block the calling thread."""
        never_return = threading.Event()
        channel = Mock()
        channel.close.side_effect = lambda *args, **kwargs: never_return.wait(30)
        dummy = self._dummy(channel)

        start = time.time()
        with patch.object(mapdl_grpc, "CHANNEL_CLOSE_TIMEOUT_S", 0.5):
            dummy._close_grpc_channel()
        elapsed = time.time() - start

        assert elapsed < 5.0
        assert dummy._channel is None

        never_return.set()

    def test_skips_closing_while_the_interpreter_is_finalizing(self):
        """During finalization gRPC's spin thread is parked, so both
        'unsubscribe' and 'close' would deadlock instead of raising.  The
        process is exiting anyway, so the channel must simply be dropped."""
        channel = Mock()
        dummy = self._dummy(channel)

        with patch.object(mapdl_grpc.sys, "is_finalizing", return_value=True):
            dummy._close_grpc_channel(exiting=True)

        channel.close.assert_not_called()
        channel.unsubscribe.assert_not_called()
        assert dummy._channel is None
        assert dummy._connectivity_callback is None
