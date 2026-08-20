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
from unittest.mock import MagicMock, Mock, patch
import weakref

from ansys.api.mapdl.v0 import mapdl_pb2 as pb_types
import pytest

from ansys.mapdl.core.errors import MapdlExitedError
from ansys.mapdl.core.mapdl_grpc import (
    ENV_RPC_TIMEOUT,
    MapdlGrpc,
    MapdlRuntimeError,
    resolve_rpc_timeout,
)


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
    m._rpc_timeout = None
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

            _subscribe_to_channel = MapdlGrpc._subscribe_to_channel

        channel = Mock()
        dummy = _Dummy(channel)
        dummy._subscribe_to_channel()

        callback = channel.subscribe.call_args[0][0]
        callback("READY")

        assert dummy._channel_state == "READY"
        assert dummy._connectivity_callback is callback


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


class TestRPCTimeout:
    """A deadline on each gRPC call turns a dead MAPDL into an exception."""

    def test_no_deadline_by_default(self, monkeypatch):
        monkeypatch.delenv(ENV_RPC_TIMEOUT, raising=False)

        assert resolve_rpc_timeout() is None

    def test_read_from_the_environment(self, monkeypatch):
        monkeypatch.setenv(ENV_RPC_TIMEOUT, "45.5")

        assert resolve_rpc_timeout() == 45.5

    def test_argument_wins_over_the_environment(self, monkeypatch):
        monkeypatch.setenv(ENV_RPC_TIMEOUT, "10")

        assert resolve_rpc_timeout(30) == 30.0

    @pytest.mark.parametrize("value", ["not-a-number", 0, -1])
    def test_invalid_deadlines_are_rejected(self, value):
        with pytest.raises(ValueError, match="gRPC timeout must be a"):
            resolve_rpc_timeout(value)

    def test_property_can_disable_the_deadline(self, monkeypatch):
        """Assigning 'None' must clear the deadline, environment or not."""
        monkeypatch.setenv(ENV_RPC_TIMEOUT, "60")
        mock = MagicMock(spec=MapdlGrpc)
        mock._rpc_timeout = resolve_rpc_timeout()

        assert MapdlGrpc.rpc_timeout.fget(mock) == 60.0

        MapdlGrpc.rpc_timeout.fset(mock, None)
        assert mock._rpc_timeout is None

        MapdlGrpc.rpc_timeout.fset(mock, 5)
        assert mock._rpc_timeout == 5.0

    def test_send_command_applies_the_deadline(self):
        mock = MagicMock(spec=MapdlGrpc)
        mock._rpc_timeout = 12.0
        mock._stub = MagicMock()

        MapdlGrpc._send_command(mock, "/PREP7")

        assert mock._stub.SendCommand.call_args.kwargs["timeout"] == 12.0

    def test_streamed_command_applies_the_deadline(self):
        mock = MagicMock(spec=MapdlGrpc)
        mock._rpc_timeout = 12.0
        mock._stub = MagicMock()
        mock._stub.SendCommandS.return_value = []
        mock._get_time_step_stream.return_value = 100

        MapdlGrpc._send_command_stream(mock, "/PREP7")

        assert mock._stub.SendCommandS.call_args.kwargs["timeout"] == 12.0
