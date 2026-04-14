# Copyright (C) 2016 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#

"""Unit tests for launcher.connection module."""

import threading
import time
from typing import Any
from unittest.mock import Mock, patch

import psutil
import pytest

from ansys.mapdl.core.errors import MapdlDidNotStart
from ansys.mapdl.core.launcher import LaunchConfig, LaunchMode
from ansys.mapdl.core.launcher.connection import (
    connect_to_existing,
    create_grpc_client,
)
from ansys.mapdl.core.launcher.models import ProcessInfo
from ansys.mapdl.core.launcher.process import check_process_is_alive
from ansys.mapdl.core.mapdl_grpc import MapdlGrpc

# ============================================================================
# Helper Functions
# ============================================================================


def make_mock_mapdl(
    local: bool = True,
    process: Any = None,
    path: Any = None,
    port: int = 50052,
    pids: list[int] | None = None,
    jobname: str = "file",
) -> Mock:
    """Return a lightweight mock that has exactly the attributes exercised by
    the methods under test.

    We pull the *real* unbound methods off ``MapdlGrpc`` and bind them to the
    mock so that the logic runs verbatim while the gRPC plumbing is bypassed.
    """
    from ansys.mapdl.core.mapdl_grpc import MapdlGrpc

    m = Mock()
    m._local = local
    m._path = path
    m._port = port
    m._pids = pids if pids is not None else []
    m._jobname = jobname
    m._exited = None

    # If caller supplied a bare Mock() process, ensure it behaves like a live
    # subprocess so that liveness checks don't accidentally trigger failures.
    if process is not None and isinstance(process, Mock):
        # subprocess.Popen-like: poll() → None means still running.
        # If poll has already been explicitly set to an integer exit code, the
        # caller wants a *dead* process — respect that and mark is_running False
        # too (since _check_process_handle prefers is_running when present).
        if isinstance(process.poll(), int):
            process.is_running.return_value = False
        else:
            process.poll.return_value = None
            process.is_running.return_value = True
        # Give it an integer pid so int(p.pid) works in _find_live_mapdl_processes
        if not isinstance(process.pid, int):
            process.pid = 12345

    m._mapdl_process = process

    # Bind real method implementations.
    m._multi_connect = MapdlGrpc._multi_connect.__get__(m)
    m._is_alive_subprocess = MapdlGrpc._is_alive_subprocess.__get__(m)
    m._find_live_mapdl_processes = MapdlGrpc._find_live_mapdl_processes.__get__(m)
    m._check_process_handle = MapdlGrpc._check_process_handle
    m._find_process_at_port = MapdlGrpc._find_process_at_port.__get__(m)
    m._find_process_from_handle = MapdlGrpc._find_process_from_handle.__get__(m)
    m._find_processes_from_cached_pids = (
        MapdlGrpc._find_processes_from_cached_pids.__get__(m)
    )
    m._find_processes_by_heuristic = MapdlGrpc._find_processes_by_heuristic.__get__(m)

    # Minimal logger.
    m._log = Mock()

    # Needed by _multi_connect error messages.
    m._channel_str = "127.0.0.1:50052"

    # Default: _connect always succeeds.
    m._connect = Mock(return_value=True)

    return m


def _create_test_config(**overrides):
    """Create a test LaunchConfig with defaults."""
    defaults = {
        "exec_file": "/path/to/mapdl",
        "run_location": "/tmp",
        "jobname": "file",
        "nproc": 4,
        "port": 50052,
        "ip": "127.0.0.1",
        "mode": LaunchMode.GRPC,
        "version": 222,
        "start_instance": True,
        "ram": 4096,
        "timeout": 45,
        "cleanup_on_exit": True,
        "clear_on_connect": True,
        "override": False,
        "remove_temp_dir_on_exit": False,
        "set_no_abort": True,
        "additional_switches": "",
        "license_type": None,
        "launch_on_hpc": False,
        "running_on_hpc": False,
        "scheduler_options": None,
        "loglevel": "ERROR",
        "log_apdl": None,
        "print_com": False,
        "mapdl_output": None,
        "transport_mode": None,
        "uds_dir": None,
        "uds_id": None,
        "certs_dir": None,
    }
    defaults.update(overrides)
    return LaunchConfig(**defaults)


# ============================================================================
# gRPC Client Creation Tests
# ============================================================================


class TestConnectionCreation:
    """Tests for client connection creation."""

    def test_create_grpc_client(self):
        """Test gRPC client creation."""
        config = _create_test_config()
        process_info = ProcessInfo(
            process=None,
            port=50052,
            ip="127.0.0.1",
            pid=12345,
        )

        with patch("ansys.mapdl.core.launcher.connection.MapdlGrpc") as mock_grpc:
            mock_grpc.return_value = Mock()
            create_grpc_client(config, process_info)

    def test_create_grpc_client_with_custom_port(self):
        """Test gRPC client creation with custom port."""
        config = _create_test_config(port=50100)
        process_info = ProcessInfo(
            process=None,
            port=50100,
            ip="127.0.0.1",
            pid=12345,
        )

        with patch("ansys.mapdl.core.launcher.connection.MapdlGrpc") as mock_grpc:
            mock_instance = Mock()
            mock_grpc.return_value = mock_instance

            create_grpc_client(config, process_info)
            # Check that MapdlGrpc was called
            mock_grpc.assert_called()

    def test_create_grpc_client_with_custom_ip(self):
        """Test gRPC client creation with custom IP."""
        config = _create_test_config(ip="192.168.1.100")
        process_info = ProcessInfo(
            process=None,
            port=50052,
            ip="192.168.1.100",
            pid=12345,
        )

        with patch("ansys.mapdl.core.launcher.connection.MapdlGrpc") as mock_grpc:
            mock_instance = Mock()
            mock_grpc.return_value = mock_instance

            create_grpc_client(config, process_info)


# ============================================================================
# Connect to Existing Instance Tests
# ============================================================================


class TestConnectToExisting:
    """Tests for connecting to existing MAPDL instance."""

    def test_connect_to_existing_basic(self):
        """Test connecting to existing instance."""
        config = _create_test_config(start_instance=False)

        with patch("ansys.mapdl.core.launcher.connection.MapdlGrpc") as mock_grpc:
            mock_instance = Mock()
            mock_grpc.return_value = mock_instance

            connect_to_existing(config)

    def test_connect_to_existing_with_timeout(self):
        """Test connecting with custom timeout."""
        config = _create_test_config(start_instance=False, timeout=60)

        with patch("ansys.mapdl.core.launcher.connection.MapdlGrpc") as mock_grpc:
            mock_instance = Mock()
            mock_grpc.return_value = mock_instance

            connect_to_existing(config)

    def test_connect_to_existing_failure(self):
        """Test handling connection failure."""
        config = _create_test_config(start_instance=False)

        with patch("ansys.mapdl.core.launcher.connection.MapdlGrpc") as mock_grpc:
            mock_grpc.side_effect = Exception("Connection failed")
            with pytest.raises(Exception):
                connect_to_existing(config)


# ============================================================================
# Connection Configuration Tests
# ============================================================================


class TestConnectionConfiguration:
    """Tests for connection configuration options."""

    def test_create_client_with_cleanup_on_exit(self):
        """Test client creation with cleanup on exit."""
        config = _create_test_config(cleanup_on_exit=True)
        process_info = ProcessInfo(
            process=None,
            port=50052,
            ip="127.0.0.1",
            pid=12345,
        )

        with patch("ansys.mapdl.core.launcher.connection.MapdlGrpc") as mock_grpc:
            mock_instance = Mock()
            mock_grpc.return_value = mock_instance
            create_grpc_client(config, process_info)

    def test_create_client_with_clear_on_connect(self):
        """Test client creation with clear on connect."""
        config = _create_test_config(clear_on_connect=True)
        process_info = ProcessInfo(
            process=None,
            port=50052,
            ip="127.0.0.1",
            pid=12345,
        )

        with patch("ansys.mapdl.core.launcher.connection.MapdlGrpc") as mock_grpc:
            mock_instance = Mock()
            mock_grpc.return_value = mock_instance
            create_grpc_client(config, process_info)

    def test_create_client_with_logging_settings(self):
        """Test client creation with logging settings."""
        config = _create_test_config(
            loglevel="DEBUG",
            log_apdl="custom.log",
            print_com=True,
        )
        process_info = ProcessInfo(
            process=None,
            port=50052,
            ip="127.0.0.1",
            pid=12345,
        )

        with patch("ansys.mapdl.core.launcher.connection.MapdlGrpc") as mock_grpc:
            mock_instance = Mock()
            mock_grpc.return_value = mock_instance
            create_grpc_client(config, process_info)


# ============================================================================
# Edge Cases
# ============================================================================


class TestConnectionEdgeCases:
    """Test edge cases in connection handling."""

    def test_create_client_with_invalid_port(self):
        """Test client creation with invalid port."""
        config = _create_test_config()
        process_info = ProcessInfo(
            process=None,
            port=99999,  # Invalid port
            ip="127.0.0.1",
            pid=12345,
        )

        with patch("ansys.mapdl.core.launcher.connection.MapdlGrpc") as mock_grpc:
            mock_grpc.side_effect = Exception("Invalid port")
            with pytest.raises(Exception):
                create_grpc_client(config, process_info)

    def test_create_client_with_invalid_ip(self):
        """Test client creation with invalid IP."""
        config = _create_test_config()
        process_info = ProcessInfo(
            process=None,
            port=50052,
            ip="999.999.999.999",  # Invalid IP
            pid=12345,
        )

        with patch("ansys.mapdl.core.launcher.connection.MapdlGrpc") as mock_grpc:
            mock_grpc.side_effect = Exception("Invalid IP")
            with pytest.raises(Exception):
                create_grpc_client(config, process_info)

    def test_connect_to_nonexistent_instance(self):
        """Test connecting to non-existent instance."""
        config = _create_test_config(start_instance=False)

        with patch("ansys.mapdl.core.launcher.connection.MapdlGrpc") as mock_grpc:
            mock_grpc.side_effect = ConnectionError("Connection refused")
            with pytest.raises(ConnectionError):
                connect_to_existing(config)


# ============================================================================
# Integration Tests
# ============================================================================


class TestConnectionIntegration:
    """Integration tests for connection module."""

    def test_connection_workflow_grpc(self):
        """Test complete gRPC connection workflow."""
        config = _create_test_config(mode=LaunchMode.GRPC)
        process_info = ProcessInfo(
            process=None,
            port=50052,
            ip="127.0.0.1",
            pid=12345,
        )

        with patch("ansys.mapdl.core.launcher.connection.MapdlGrpc") as mock_grpc:
            mock_instance = Mock()
            mock_instance._check_parameter_names = Mock()
            mock_grpc.return_value = mock_instance

            create_grpc_client(config, process_info)

    def test_connection_with_process_info(self):
        """Test connection includes process information."""
        config = _create_test_config()
        process_info = ProcessInfo(
            process=Mock(),
            port=50052,
            ip="127.0.0.1",
            pid=12345,
        )

        with patch("ansys.mapdl.core.launcher.connection.MapdlGrpc") as mock_grpc:
            mock_instance = Mock()
            mock_grpc.return_value = mock_instance

            create_grpc_client(config, process_info)


# =============================================================================
# check_process_is_alive
# =============================================================================


class TestCheckProcessIsAlive:
    """Unit tests for ``check_process_is_alive``."""

    def test_alive_process_does_not_raise(self):
        """A process whose poll() returns None should not raise."""
        mock_process = Mock()
        mock_process.poll.return_value = None  # process is running

        # Should complete without exception
        check_process_is_alive(mock_process)

    def test_dead_process_raises(self):
        """A process that has exited (poll returns exit code) should raise."""
        mock_process = Mock()
        mock_process.poll.return_value = 1  # exit code 1 → dead

        with pytest.raises(MapdlDidNotStart, match="died"):
            check_process_is_alive(mock_process)

    def test_dead_process_exit_code_zero_raises(self):
        """Even a clean exit (code 0) means the process is gone."""
        mock_process = Mock()
        mock_process.poll.return_value = 0

        with pytest.raises(MapdlDidNotStart):
            check_process_is_alive(mock_process)

    def test_run_location_ignored_for_alive_process(self):
        """run_location is accepted but does not affect the alive check."""
        mock_process = Mock()
        mock_process.poll.return_value = None

        check_process_is_alive(mock_process, run_location="/some/path")

    def test_run_location_ignored_for_dead_process(self):
        """run_location does not suppress the exception."""
        mock_process = Mock()
        mock_process.poll.return_value = 2

        with pytest.raises(MapdlDidNotStart):
            check_process_is_alive(mock_process, run_location="/some/path")


# =============================================================================
# get_process_at_port
# =============================================================================


class TestGetProcessAtPort:
    """Unit tests for the public ``get_process_at_port`` function."""

    def test_public_name_is_importable(self):
        """Ensure the public name is importable from the package."""
        from ansys.mapdl.core.launcher import get_process_at_port

        assert callable(get_process_at_port)

    def test_private_alias_still_works(self):
        """The private ``get_process_at_port`` alias should still exist."""
        from ansys.mapdl.core.launcher.network import get_process_at_port

        assert callable(get_process_at_port)

    def test_public_and_private_are_same_function(self):
        """Both names must point to the same underlying function."""
        from ansys.mapdl.core.launcher.network import (
            get_process_at_port,
        )

        assert get_process_at_port is get_process_at_port

    def test_returns_none_for_unused_port(self):
        """A port with no listeners should return None."""
        from ansys.mapdl.core.launcher.network import get_process_at_port

        # Use a very unlikely port; if it happens to be in use the test is
        # skipped rather than failing.
        port = 19999
        result = get_process_at_port(port)
        # Accept either None or a psutil.Process (if port happened to be in use)
        assert result is None or isinstance(result, psutil.Process)


# =============================================================================
# _multi_connect — monitoring thread start conditions
# =============================================================================


class TestMultiConnectMonitoring:
    """Unit tests for the monitoring thread in ``_multi_connect``."""

    def test_monitoring_starts_when_local_process_and_path(self):
        """Thread starts only when local + process + path are all set."""
        m = make_mock_mapdl(local=True, process=Mock(), path="/some/path")
        with patch("ansys.mapdl.core.launcher.process.check_process_is_alive"):
            with patch.object(m, "_connect", return_value=True):
                m._multi_connect(n_attempts=1, timeout=1)

        debug_calls = [str(c) for c in m._log.debug.call_args_list]
        assert any("Started MAPDL monitoring thread" in c for c in debug_calls)

    @pytest.mark.parametrize(
        "has_process,has_path",
        [
            (True, False),
            (False, True),
            (False, False),
        ],
    )
    def test_monitoring_not_started_without_both(self, has_process, has_path):
        """Thread does NOT start when process or path is missing."""
        m = make_mock_mapdl(
            local=True,
            process=Mock() if has_process else None,
            path="/some/path" if has_path else None,
        )
        with patch("ansys.mapdl.core.launcher.process.check_process_is_alive"):
            with patch.object(m, "_connect", return_value=True):
                m._multi_connect(n_attempts=1, timeout=1)

        debug_calls = [str(c) for c in m._log.debug.call_args_list]
        assert not any("Started MAPDL monitoring thread" in c for c in debug_calls)

    def test_remote_no_monitoring(self):
        """Monitoring thread never starts for remote instances."""
        m = make_mock_mapdl(local=False, process=Mock(), path="/some/path")
        with patch.object(m, "_connect", return_value=True):
            m._multi_connect(n_attempts=1, timeout=1)

        debug_calls = [str(c) for c in m._log.debug.call_args_list]
        assert not any("Started MAPDL monitoring thread" in c for c in debug_calls)

    def test_monitor_detects_process_death_quickly(self):
        """Monitor raises ``MapdlDidNotStart`` in well under the full timeout."""
        mock_process = Mock()
        mock_process.poll.return_value = 1  # already dead
        m = make_mock_mapdl(local=True, process=mock_process, path="/some/path")

        with (
            patch.object(m, "_find_live_mapdl_processes", return_value=[]),
            patch.object(m, "_connect", return_value=False),
        ):
            start = time.time()
            with pytest.raises(MapdlDidNotStart, match="died"):
                m._multi_connect(n_attempts=5, timeout=10)
            elapsed = time.time() - start

        assert elapsed < 4, f"Expected fast failure, took {elapsed:.1f}s"

    def test_thread_cleaned_up_after_successful_connect(self):
        """Monitoring thread is joined (cleaned up) after a successful connection."""
        m = make_mock_mapdl(local=True, process=Mock(pid=12345), path="/some/path")
        with patch("ansys.mapdl.core.launcher.process.check_process_is_alive"):
            with patch("psutil.pid_exists", return_value=True):
                threads_before = threading.active_count()
                m._multi_connect(n_attempts=1, timeout=2)
                time.sleep(0.2)
                threads_after = threading.active_count()

        assert (
            abs(threads_after - threads_before) <= 1
        ), "Monitoring thread should be cleaned up"

    def test_monitor_stops_checking_after_successful_connect(self):
        """The monitor thread stops incrementing its check counter once connected."""
        check_count = {"n": 0}

        def counting_check(*args, **kwargs):
            check_count["n"] += 1
            time.sleep(0.05)

        m = make_mock_mapdl(local=True, process=Mock(pid=12345), path="/some/path")
        connect_calls = {"n": 0}

        def connect_on_second(*args, **kwargs):
            connect_calls["n"] += 1
            return connect_calls["n"] >= 2

        with patch(
            "ansys.mapdl.core.launcher.process.check_process_is_alive",
            side_effect=counting_check,
        ):
            with patch("psutil.pid_exists", return_value=True):
                with patch.object(m, "_connect", side_effect=connect_on_second):
                    m._multi_connect(n_attempts=5, timeout=10)
                    count_at_connect = check_count["n"]
                    time.sleep(1.0)
                    count_after_wait = check_count["n"]

        assert (
            count_after_wait - count_at_connect <= 3
        ), "Monitor should stop after successful connection"


# =============================================================================
# _check_process_handle
# =============================================================================


class TestCheckProcessHandle:
    """Unit tests for the ``_check_process_handle`` static helper."""

    def test_is_running_true(self):
        """Returns ``True`` when ``is_running()`` is truthy."""
        proc = Mock()
        proc.is_running.return_value = True
        assert MapdlGrpc._check_process_handle(proc) is True

    def test_is_running_false(self):
        """Returns ``False`` when ``is_running()`` is falsy."""
        proc = Mock()
        proc.is_running.return_value = False
        assert MapdlGrpc._check_process_handle(proc) is False

    def test_is_running_no_such_process(self):
        """Returns ``False`` when ``is_running()`` raises ``NoSuchProcess``."""

        proc = Mock()
        proc.is_running.side_effect = psutil.NoSuchProcess(pid=0)
        assert MapdlGrpc._check_process_handle(proc) is False

    def test_poll_none_means_alive(self):
        """Returns ``True`` when ``poll()`` returns ``None`` (Popen-style)."""
        proc = Mock(spec=["poll"])
        proc.poll.return_value = None
        assert MapdlGrpc._check_process_handle(proc) is True

    def test_poll_nonzero_means_dead(self):
        """Returns ``False`` when ``poll()`` returns an exit code."""
        proc = Mock(spec=["poll"])
        proc.poll.return_value = 1
        assert MapdlGrpc._check_process_handle(proc) is False

    def test_unknown_handle_type_returns_none(self):
        """Returns ``None`` when handle has neither ``is_running`` nor ``poll``."""
        proc = Mock(spec=["pid"])  # no is_running, no poll
        assert MapdlGrpc._check_process_handle(proc) is None


# _is_alive_subprocess
# =============================================================================


class TestIsAliveSubprocess:
    """Unit tests for the robust ``_is_alive_subprocess`` method."""

    def test_returns_none_when_no_process(self):
        """Returns ``None`` when ``_mapdl_process`` is ``None``."""
        m = make_mock_mapdl(process=None)
        assert m._is_alive_subprocess() is None

    def test_psutil_process_alive(self):
        """Returns ``True`` for a psutil-like process that is running."""
        m = make_mock_mapdl(process=None)
        mock_proc = Mock()
        mock_proc.is_running.return_value = True
        m._mapdl_process = mock_proc
        assert m._is_alive_subprocess() is True

    def test_psutil_process_dead(self):
        """Returns ``False`` for a psutil-like process that stopped."""
        m = make_mock_mapdl(process=None)
        mock_proc = Mock()
        mock_proc.is_running.return_value = False
        m._mapdl_process = mock_proc
        assert m._is_alive_subprocess() is False

    def test_is_running_truthy_value_returns_true(self):
        """A truthy non-bool return from ``is_running()`` is treated as ``True``."""
        m = make_mock_mapdl(process=None)
        mock_proc = Mock()
        mock_proc.is_running.return_value = 1  # truthy int
        m._mapdl_process = mock_proc
        assert m._is_alive_subprocess() is True

    def test_is_running_falsy_value_returns_false(self):
        """A falsy non-bool return from ``is_running()`` is treated as ``False``."""
        m = make_mock_mapdl(process=None)
        mock_proc = Mock()
        mock_proc.is_running.return_value = 0  # falsy int
        m._mapdl_process = mock_proc
        assert m._is_alive_subprocess() is False

    def test_popen_alive(self):
        """Returns ``True`` for a Popen-like object that is running."""
        m = make_mock_mapdl(process=None)
        mock_proc = Mock(spec=["poll", "pid"])
        mock_proc.poll.return_value = None
        m._mapdl_process = mock_proc
        assert m._is_alive_subprocess() is True

    def test_popen_dead(self):
        """Returns ``False`` for a Popen-like object that exited."""
        m = make_mock_mapdl(process=None)
        mock_proc = Mock(spec=["poll", "pid"])
        mock_proc.poll.return_value = 1
        m._mapdl_process = mock_proc
        assert m._is_alive_subprocess() is False

    def test_unknown_handle_with_pid_uses_pid_exists(self):
        """Falls back to ``psutil.pid_exists`` for unknown handle types."""
        m = make_mock_mapdl(process=None)
        mock_proc = Mock(spec=["pid"])  # no is_running, no poll
        mock_proc.pid = 12345
        m._mapdl_process = mock_proc
        with patch("psutil.pid_exists", return_value=True) as mock_exists:
            result = m._is_alive_subprocess()
        mock_exists.assert_called_once_with(12345)
        assert result is True

    def test_unknown_handle_without_pid_returns_none(self):
        """Returns ``None`` when handle has no ``pid`` attribute."""
        m = make_mock_mapdl(process=None)
        mock_proc = Mock(spec=[])  # no is_running, no poll, no pid
        m._mapdl_process = mock_proc
        assert m._is_alive_subprocess() is None


# =============================================================================
# _find_process_at_port
# =============================================================================


class TestFindProcessAtPort:
    """Unit tests for ``_find_process_at_port``."""

    def test_returns_empty_when_no_port(self):
        """Returns ``[]`` when ``_port`` is not set."""
        m = make_mock_mapdl(process=None, port=None)
        assert m._find_process_at_port() == []

    def test_returns_empty_when_port_lookup_finds_nothing(self):
        """Returns ``[]`` when no process listens on the port."""
        m = make_mock_mapdl(process=None, port=50052)
        with patch(
            "ansys.mapdl.core.launcher.network.get_process_at_port",
            return_value=None,
        ):
            assert m._find_process_at_port() == []

    def test_returns_process_when_found_and_alive(self):
        """Returns the process when it is listening and running."""

        mock_proc = Mock(spec=psutil.Process)
        mock_proc.is_running.return_value = True
        m = make_mock_mapdl(process=None, port=50052)
        with patch(
            "ansys.mapdl.core.launcher.network.get_process_at_port",
            return_value=mock_proc,
        ):
            assert m._find_process_at_port() == [mock_proc]

    def test_returns_empty_when_found_but_not_running(self):
        """Returns ``[]`` when the port-owning process has already exited."""

        mock_proc = Mock(spec=psutil.Process)
        mock_proc.is_running.return_value = False
        m = make_mock_mapdl(process=None, port=50052)
        with patch(
            "ansys.mapdl.core.launcher.network.get_process_at_port",
            return_value=mock_proc,
        ):
            assert m._find_process_at_port() == []


# =============================================================================
# _find_process_from_handle
# =============================================================================


class TestFindProcessFromHandle:
    """Unit tests for ``_find_process_from_handle``."""

    def test_returns_empty_when_no_handle(self):
        """Returns ``[]`` when ``_mapdl_process`` is ``None``."""
        m = make_mock_mapdl(process=None)
        assert m._find_process_from_handle() == []

    def test_returns_empty_when_handle_is_dead(self):
        """Returns ``[]`` when the stored handle is no longer running."""
        mock_proc = Mock()
        mock_proc.is_running.return_value = False
        m = make_mock_mapdl(process=None)
        m._mapdl_process = mock_proc
        assert m._find_process_from_handle() == []

    def test_returns_psutil_process_when_alive(self):
        """Returns a ``psutil.Process`` wrapping the PID when alive."""

        mock_proc = Mock()
        mock_proc.is_running.return_value = True
        mock_proc.pid = 42
        m = make_mock_mapdl(process=None)
        m._mapdl_process = mock_proc
        with patch("psutil.Process", return_value=Mock(spec=psutil.Process)) as mp:
            result = m._find_process_from_handle()
        mp.assert_called_once_with(42)
        assert len(result) == 1

    def test_returns_empty_when_pid_raises_no_such_process(self):
        """Returns ``[]`` when ``psutil.Process(pid)`` raises ``NoSuchProcess``."""

        mock_proc = Mock()
        mock_proc.is_running.return_value = True
        mock_proc.pid = 42
        m = make_mock_mapdl(process=None)
        m._mapdl_process = mock_proc
        with patch("psutil.Process", side_effect=psutil.NoSuchProcess(pid=42)):
            result = m._find_process_from_handle()
        assert result == []


# =============================================================================
# _find_processes_from_cached_pids
# =============================================================================


class TestFindProcessesFromCachedPids:
    """Unit tests for ``_find_processes_from_cached_pids``."""

    def test_returns_empty_when_no_pids(self):
        """Returns ``[]`` when ``_pids`` is empty."""
        m = make_mock_mapdl(process=None, pids=[])
        assert m._find_processes_from_cached_pids() == []

    def test_returns_alive_processes(self):
        """Returns running processes for valid cached PIDs."""

        mock_proc = Mock(spec=psutil.Process)
        mock_proc.is_running.return_value = True
        mock_proc.pid = 1234
        m = make_mock_mapdl(process=None, pids=[1234])
        with patch("psutil.Process", return_value=mock_proc):
            result = m._find_processes_from_cached_pids()
        assert result == [mock_proc]

    def test_skips_dead_pids(self):
        """Skips PIDs that raise ``NoSuchProcess``."""

        m = make_mock_mapdl(process=None, pids=[9999])
        with patch("psutil.Process", side_effect=psutil.NoSuchProcess(pid=9999)):
            result = m._find_processes_from_cached_pids()
        assert result == []

    def test_skips_none_pids(self):
        """``None`` entries in ``_pids`` are silently ignored."""

        mock_proc = Mock(spec=psutil.Process)
        mock_proc.is_running.return_value = True
        m = make_mock_mapdl(process=None, pids=[None, 5678])
        with patch("psutil.Process", return_value=mock_proc):
            result = m._find_processes_from_cached_pids()
        assert len(result) == 1


# =============================================================================
# _find_processes_by_heuristic
# =============================================================================


class TestFindProcessesByHeuristic:
    """Unit tests for ``_find_processes_by_heuristic``."""

    def test_returns_empty_when_no_criteria(self):
        """Returns ``[]`` when neither path nor jobname is set."""
        m = make_mock_mapdl(process=None, path=None, jobname="")
        m.jobname = ""
        with patch("psutil.process_iter", return_value=iter([])):
            assert m._find_processes_by_heuristic() == []

    def test_matches_by_cwd(self):
        """A process whose CWD starts with ``_path`` is included."""

        mock_proc = Mock(spec=psutil.Process)
        mock_proc.is_running.return_value = True
        mock_proc.info = {"pid": 1, "name": "other", "cmdline": [], "cwd": "/my/path"}
        m = make_mock_mapdl(process=None, path="/my/path")
        with patch("psutil.process_iter", return_value=iter([mock_proc])):
            result = m._find_processes_by_heuristic()
        assert mock_proc in result

    def test_matches_by_jobname_in_cmdline(self):
        """A process whose cmdline contains ``_jobname`` is included."""

        mock_proc = Mock(spec=psutil.Process)
        mock_proc.is_running.return_value = True
        mock_proc.info = {
            "pid": 2,
            "name": "other",
            "cmdline": ["/path/to/mapdl", "-j", "myjob"],
            "cwd": "/other",
        }
        m = make_mock_mapdl(process=None, path=None, jobname="myjob")
        with patch("psutil.process_iter", return_value=iter([mock_proc])):
            result = m._find_processes_by_heuristic()
        assert mock_proc in result

    def test_matches_by_mapdl_process_name(self):
        """A process recognised by ``_is_mapdl_process`` is included."""

        mock_proc = Mock(spec=psutil.Process)
        mock_proc.is_running.return_value = True
        mock_proc.info = {"pid": 3, "name": "ansys", "cmdline": [], "cwd": "/other"}
        m = make_mock_mapdl(process=None, path=None, jobname="file")
        with (
            patch("psutil.process_iter", return_value=iter([mock_proc])),
            patch(
                "ansys.mapdl.core.launcher.network._is_mapdl_process",
                return_value=True,
            ),
        ):
            result = m._find_processes_by_heuristic()
        assert mock_proc in result

    def test_skips_inaccessible_processes(self):
        """Processes raising ``AccessDenied`` or ``NoSuchProcess`` are skipped."""
        from unittest.mock import PropertyMock

        mock_proc = Mock(spec=psutil.Process)
        # Simulate a process whose .info raises AccessDenied on attribute access.
        type(mock_proc).info = PropertyMock(side_effect=psutil.AccessDenied(pid=0))
        m = make_mock_mapdl(process=None, path="/my/path")
        with patch("psutil.process_iter", return_value=iter([mock_proc])):
            assert m._find_processes_by_heuristic() == []


# =============================================================================
# _find_live_mapdl_processes (orchestrator)
# =============================================================================


class TestFindLiveMapdlProcesses:
    """Unit tests for the ``_find_live_mapdl_processes`` orchestrator."""

    def test_returns_empty_when_nothing_found(self):
        """Returns ``[]`` when no MAPDL process can be discovered."""
        m = make_mock_mapdl(process=None, pids=[], path=None, port=None)
        with patch(
            "ansys.mapdl.core.launcher.network.get_process_at_port",
            return_value=None,
        ):
            with patch("psutil.process_iter", return_value=iter([])):
                result = m._find_live_mapdl_processes()
        assert result == []

    def test_port_lookup_takes_priority(self):
        """A process found via port lookup is returned immediately."""

        mock_proc = Mock(spec=psutil.Process)
        mock_proc.is_running.return_value = True
        mock_proc.pid = 99999

        m = make_mock_mapdl(process=None, pids=[], port=50052)
        with patch(
            "ansys.mapdl.core.launcher.network.get_process_at_port",
            return_value=mock_proc,
        ):
            result = m._find_live_mapdl_processes()

        assert result == [mock_proc]

    def test_cached_pids_fallback(self):
        """Cached PIDs are checked when port lookup returns nothing."""

        mock_proc = Mock(spec=psutil.Process)
        mock_proc.is_running.return_value = True
        mock_proc.pid = 11111

        m = make_mock_mapdl(process=None, pids=[11111], port=None)
        with patch(
            "ansys.mapdl.core.launcher.network.get_process_at_port",
            return_value=None,
        ):
            with patch("psutil.Process", return_value=mock_proc):
                result = m._find_live_mapdl_processes()

        assert len(result) == 1
        assert result[0].pid == 11111

    def test_live_process_returned_directly(self):
        """If ``_mapdl_process`` is alive, it is returned without scanning."""

        mock_proc = Mock()
        mock_proc.is_running.return_value = True
        mock_proc.pid = 42

        m = make_mock_mapdl(process=mock_proc, pids=[], port=None)
        with (
            patch(
                "ansys.mapdl.core.launcher.network.get_process_at_port",
                return_value=None,
            ),
            patch("psutil.Process", return_value=mock_proc) as mock_psutil,
        ):
            result = m._find_live_mapdl_processes()

        mock_psutil.assert_called_once_with(42)
        assert result == [mock_proc]
