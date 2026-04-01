# Copyright (C) 2016 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#

"""Unit tests for launcher.network module."""

import os
from unittest.mock import MagicMock, patch

import psutil
import pytest

from ansys.mapdl.core.launcher.models import PortStatus
from ansys.mapdl.core.launcher.network import (
    _check_port_socket,
    _get_process_at_port,
    _is_mapdl_process,
    check_port_status,
    find_available_port,
)


class TestNetworkPortStatus:
    """Tests for port status checking."""

    def test_check_port_status_available(self):
        """Test checking available port."""
        with patch("socket.socket") as mock_socket:
            mock_instance = MagicMock()
            mock_socket.return_value = mock_instance
            mock_instance.connect_ex.return_value = 1  # Connection refused = available

            result = check_port_status(50100, host="127.0.0.1")
            assert result.available is True

    def test_check_port_status_with_ipv6(self):
        """Test port checking with IPv6."""
        with patch("socket.socket") as mock_socket:
            mock_instance = MagicMock()
            mock_socket.return_value = mock_instance
            mock_instance.connect_ex.return_value = 0

            result = check_port_status(50052, host="::1")
            assert result is not None


class TestNetworkFindAvailablePort:
    """Tests for finding available ports."""

    def test_find_available_port(self):
        """Test finding available port."""
        with patch("ansys.mapdl.core.launcher.network.check_port_status") as mock_check:
            # First call: port in use, second call: port available
            mock_check.side_effect = [
                PortStatus(port=50052, available=False, used_by_mapdl=False),
                PortStatus(port=50053, available=True, used_by_mapdl=False),
            ]

            result = find_available_port(start_port=50052)
            assert result is not None and result > 50052

    def test_find_available_port_range(self):
        """Test finding available port in range."""
        with patch("ansys.mapdl.core.launcher.network.check_port_status") as mock_check:
            # All ports in use except 50100
            def check_port(port):
                return PortStatus(
                    port=port,
                    available=(port >= 50100),
                    used_by_mapdl=False,
                    process=None,
                )

            mock_check.side_effect = check_port

            result = find_available_port(start_port=50050)
            assert result is not None

    def test_find_available_port_with_start(self):
        """Test finding available port with custom start port."""
        with patch("ansys.mapdl.core.launcher.network.check_port_status") as mock_check:
            mock_check.return_value = PortStatus(
                port=60000, available=True, used_by_mapdl=False
            )

            result = find_available_port(start_port=60000)
            assert result == 60000


class TestNetworkEdgeCases:
    """Test edge cases in network module."""

    def test_check_port_invalid_port_number(self):
        """Test checking invalid port number."""
        # Port 99999 is out of valid range (0-65535)
        # Function will raise OverflowError from underlying socket operations
        with pytest.raises(OverflowError):
            check_port_status(99999, host="127.0.0.1")

    def test_check_port_invalid_host(self):
        """Test checking with invalid host."""
        with patch("socket.socket") as mock_socket:
            mock_instance = MagicMock()
            mock_socket.return_value = mock_instance
            mock_instance.connect_ex.return_value = 1

            # Should handle invalid host gracefully
            check_port_status(50052, host="invalid.host.name")


class TestCheckPortSocket:
    """Tests for _check_port_socket function."""

    def test_check_port_socket_available(self):
        """Test socket check when port is available."""
        with patch("ansys.mapdl.core.launcher.network.socket.socket") as mock_socket:
            mock_instance = MagicMock()
            mock_socket.return_value.__enter__.return_value = mock_instance
            mock_instance.bind.return_value = None

            result = _check_port_socket(50052, "127.0.0.1")
            assert result is True

    def test_check_port_socket_in_use(self):
        """Test socket check when port is in use."""
        with patch("ansys.mapdl.core.launcher.network.socket.socket") as mock_socket:
            mock_instance = MagicMock()
            mock_socket.return_value.__enter__.return_value = mock_instance
            import socket as socket_module

            mock_instance.bind.side_effect = socket_module.error("Address in use")

            result = _check_port_socket(50052, "127.0.0.1")
            assert result is False

    def test_check_port_socket_different_host(self):
        """Test socket check with different host."""
        with patch("ansys.mapdl.core.launcher.network.socket.socket") as mock_socket:
            mock_instance = MagicMock()
            mock_socket.return_value.__enter__.return_value = mock_instance
            mock_instance.bind.return_value = None

            result = _check_port_socket(60000, "0.0.0.0")
            assert result is True


class TestGetProcessAtPort:
    """Tests for _get_process_at_port function."""

    def test_get_process_at_port_found(self):
        """Test finding a process at a port."""
        mock_proc = MagicMock(spec=psutil.Process)
        mock_conn = MagicMock()
        mock_conn.laddr.port = 50052

        mock_proc.net_connections.return_value = [mock_conn]

        with patch("psutil.process_iter") as mock_iter:
            mock_iter.return_value = [mock_proc]

            result = _get_process_at_port(50052)
            assert result == mock_proc

    def test_get_process_at_port_not_found(self):
        """Test when no process is found at port."""
        mock_proc = MagicMock(spec=psutil.Process)
        mock_conn = MagicMock()
        mock_conn.laddr.port = 50053

        mock_proc.net_connections.return_value = [mock_conn]

        with patch("psutil.process_iter") as mock_iter:
            mock_iter.return_value = [mock_proc]

            result = _get_process_at_port(50052)
            assert result is None

    def test_get_process_at_port_access_denied(self):
        """Test handling AccessDenied exception."""
        mock_proc = MagicMock(spec=psutil.Process)
        mock_proc.net_connections.side_effect = psutil.AccessDenied()

        with patch("psutil.process_iter") as mock_iter:
            mock_iter.return_value = [mock_proc]

            result = _get_process_at_port(50052)
            assert result is None

    def test_get_process_at_port_no_such_process(self):
        """Test handling NoSuchProcess exception."""
        mock_proc = MagicMock(spec=psutil.Process)
        mock_proc.net_connections.side_effect = psutil.NoSuchProcess(999)

        with patch("psutil.process_iter") as mock_iter:
            mock_iter.return_value = [mock_proc]

            result = _get_process_at_port(50052)
            assert result is None

    def test_get_process_at_port_multiple_connections(self):
        """Test with process having multiple connections."""
        mock_proc = MagicMock(spec=psutil.Process)
        mock_conn1 = MagicMock()
        mock_conn1.laddr.port = 50051
        mock_conn2 = MagicMock()
        mock_conn2.laddr.port = 50052

        mock_proc.net_connections.return_value = [mock_conn1, mock_conn2]

        with patch("psutil.process_iter") as mock_iter:
            mock_iter.return_value = [mock_proc]

            result = _get_process_at_port(50052)
            assert result == mock_proc

    def test_get_process_at_port_empty_process_list(self):
        """Test with no processes."""
        with patch("psutil.process_iter") as mock_iter:
            mock_iter.return_value = []

            result = _get_process_at_port(50052)
            assert result is None


class TestIsMapdlProcess:
    """Tests for _is_mapdl_process function."""

    def test_is_mapdl_process_true(self):
        """Test identifying MAPDL process."""
        mock_proc = MagicMock(spec=psutil.Process)
        mock_proc.name.return_value = "ansys.exe"
        mock_proc.cmdline.return_value = ["ansys.exe", "-grpc", "-port", "50052"]

        result = _is_mapdl_process(mock_proc)
        assert result is True

    def test_is_mapdl_process_with_mapdl_name(self):
        """Test identifying MAPDL process with 'mapdl' in name."""
        mock_proc = MagicMock(spec=psutil.Process)
        mock_proc.name.return_value = "mapdl.exe"
        mock_proc.cmdline.return_value = ["mapdl.exe", "-grpc"]

        result = _is_mapdl_process(mock_proc)
        assert result is True

    def test_is_mapdl_process_false_no_grpc(self):
        """Test non-MAPDL process (no -grpc flag)."""
        mock_proc = MagicMock(spec=psutil.Process)
        mock_proc.name.return_value = "ansys.exe"
        mock_proc.cmdline.return_value = ["ansys.exe", "-port", "50052"]

        result = _is_mapdl_process(mock_proc)
        assert result is False

    def test_is_mapdl_process_false_not_ansys(self):
        """Test non-ANSYS process."""
        mock_proc = MagicMock(spec=psutil.Process)
        mock_proc.name.return_value = "notepad.exe"
        mock_proc.cmdline.return_value = ["notepad.exe"]

        result = _is_mapdl_process(mock_proc)
        assert result is False

    def test_is_mapdl_process_access_denied(self):
        """Test handling AccessDenied exception."""
        mock_proc = MagicMock(spec=psutil.Process)
        mock_proc.name.side_effect = psutil.AccessDenied()

        result = _is_mapdl_process(mock_proc)
        assert result is False

    def test_is_mapdl_process_no_such_process(self):
        """Test handling NoSuchProcess exception."""
        mock_proc = MagicMock(spec=psutil.Process)
        mock_proc.name.side_effect = psutil.NoSuchProcess(999)

        result = _is_mapdl_process(mock_proc)
        assert result is False

    def test_is_mapdl_process_cmdline_access_denied(self):
        """Test handling AccessDenied on cmdline access."""
        mock_proc = MagicMock(spec=psutil.Process)
        mock_proc.name.return_value = "ansys.exe"
        mock_proc.cmdline.side_effect = psutil.AccessDenied()

        result = _is_mapdl_process(mock_proc)
        assert result is False

    def test_is_mapdl_process_uppercase_name(self):
        """Test case-insensitive process name matching."""
        mock_proc = MagicMock(spec=psutil.Process)
        mock_proc.name.return_value = "ANSYS.EXE"
        mock_proc.cmdline.return_value = ["ANSYS.EXE", "-grpc"]

        result = _is_mapdl_process(mock_proc)
        assert result is True


class TestCheckPortStatusAdvanced:
    """Advanced tests for check_port_status function."""

    def test_check_port_status_with_process_found(self):
        """Test check_port_status when process is found at port."""
        mock_proc = MagicMock(spec=psutil.Process)
        mock_proc.name.return_value = "ansys.exe"
        mock_proc.cmdline.return_value = ["ansys.exe", "-grpc"]

        with patch(
            "ansys.mapdl.core.launcher.network._check_port_socket"
        ) as mock_socket:
            with patch(
                "ansys.mapdl.core.launcher.network._get_process_at_port"
            ) as mock_get:
                with patch(
                    "ansys.mapdl.core.launcher.network._is_mapdl_process"
                ) as mock_is_mapdl:
                    mock_socket.return_value = False
                    mock_get.return_value = mock_proc
                    mock_is_mapdl.return_value = True

                    result = check_port_status(50052)
                    assert result.port == 50052
                    assert result.available is False
                    assert result.used_by_mapdl is True
                    assert result.process == mock_proc

    def test_check_port_status_with_non_mapdl_process(self):
        """Test check_port_status when non-MAPDL process uses port."""
        mock_proc = MagicMock(spec=psutil.Process)

        with patch(
            "ansys.mapdl.core.launcher.network._check_port_socket"
        ) as mock_socket:
            with patch(
                "ansys.mapdl.core.launcher.network._get_process_at_port"
            ) as mock_get:
                with patch(
                    "ansys.mapdl.core.launcher.network._is_mapdl_process"
                ) as mock_is_mapdl:
                    mock_socket.return_value = False
                    mock_get.return_value = mock_proc
                    mock_is_mapdl.return_value = False

                    result = check_port_status(50052)
                    assert result.port == 50052
                    assert result.available is False
                    assert result.used_by_mapdl is False
                    assert result.process == mock_proc

    def test_check_port_status_socket_available_no_process(self):
        """Test when socket shows available and no process found."""
        with patch(
            "ansys.mapdl.core.launcher.network._check_port_socket"
        ) as mock_socket:
            with patch(
                "ansys.mapdl.core.launcher.network._get_process_at_port"
            ) as mock_get:
                mock_socket.return_value = True
                mock_get.return_value = None

                result = check_port_status(50052)
                assert result.port == 50052
                assert result.available is True
                assert result.used_by_mapdl is False
                assert result.process is None


class TestFindAvailablePortAdvanced:
    """Advanced tests for find_available_port function."""

    def test_find_available_port_max_attempts_exceeded(self):
        """Test RuntimeError when no port available within max_attempts."""
        with patch("ansys.mapdl.core.launcher.network.check_port_status") as mock_check:
            # All ports in use
            mock_check.return_value = PortStatus(
                port=50052, available=False, used_by_mapdl=False
            )

            with pytest.raises(RuntimeError) as exc_info:
                find_available_port(start_port=50052, max_attempts=5)

            assert "No available port found" in str(exc_info.value)
            assert "50052" in str(exc_info.value)

    def test_find_available_port_first_attempt_succeeds(self):
        """Test finding available port on first attempt."""
        with patch("ansys.mapdl.core.launcher.network.check_port_status") as mock_check:
            mock_check.return_value = PortStatus(
                port=50052, available=True, used_by_mapdl=False
            )

            result = find_available_port(start_port=50052, max_attempts=1)
            assert result == 50052

    def test_find_available_port_high_port_number(self):
        """Test finding available port with high starting port."""
        with patch("ansys.mapdl.core.launcher.network.check_port_status") as mock_check:
            mock_check.return_value = PortStatus(
                port=65000, available=True, used_by_mapdl=False
            )

            result = find_available_port(start_port=65000, max_attempts=10)
            assert result == 65000

    def test_find_available_port_default_parameters(self):
        """Test find_available_port with default parameters."""
        with patch("ansys.mapdl.core.launcher.network.check_port_status") as mock_check:
            mock_check.return_value = PortStatus(
                port=50052, available=True, used_by_mapdl=False
            )

            result = find_available_port()
            assert result == 50052
            mock_check.assert_called_once_with(50052)

    def test_find_available_port_multiple_attempts(self):
        """Test finding available port after multiple attempts."""
        with patch("ansys.mapdl.core.launcher.network.check_port_status") as mock_check:
            # Simulate: first 3 ports in use, 4th port available
            mock_check.side_effect = [
                PortStatus(port=50052, available=False, used_by_mapdl=False),
                PortStatus(port=50053, available=False, used_by_mapdl=False),
                PortStatus(port=50054, available=False, used_by_mapdl=False),
                PortStatus(port=50055, available=True, used_by_mapdl=False),
            ]

            result = find_available_port(start_port=50052, max_attempts=10)
            assert result == 50055
            assert mock_check.call_count == 4


# ============================================================================
# PHASE 1: Port Busy Detection Tests
# ============================================================================


class TestPhase1PortBusyDetection:
    """Phase 1: Tests for find_available_port() with busy ports detection.

    These tests validate the increment-by-1 behavior and max_attempts parameter
    for the new launcher architecture.
    """

    def test_find_available_port_when_ports_busy(self):
        """Test finding available port when first ports are busy.

        Validates that find_available_port increments port by 1 and finds
        the next available port when initial ports are in use.
        """
        with patch("ansys.mapdl.core.launcher.network.check_port_status") as mock_check:
            # Simulate: 50052 busy, 50053 busy, 50054 available
            mock_check.side_effect = [
                PortStatus(port=50052, available=False, used_by_mapdl=False),
                PortStatus(port=50053, available=False, used_by_mapdl=False),
                PortStatus(port=50054, available=True, used_by_mapdl=False),
            ]

            result = find_available_port(start_port=50052, max_attempts=10)
            assert result == 50054

            # Verify calls were made for correct ports (increments by 1)
            calls = mock_check.call_args_list
            assert len(calls) == 3
            assert calls[0][0][0] == 50052
            assert calls[1][0][0] == 50053
            assert calls[2][0][0] == 50054

    def test_find_available_port_no_available_ports(self):
        """Test RuntimeError when no available ports found within max_attempts.

        Validates that find_available_port raises RuntimeError when all ports
        in the search range are busy and max_attempts is reached.
        """
        with patch("ansys.mapdl.core.launcher.network.check_port_status") as mock_check:
            # All ports in use
            mock_check.return_value = PortStatus(
                port=50052, available=False, used_by_mapdl=False
            )

            with pytest.raises(RuntimeError) as exc_info:
                find_available_port(start_port=50052, max_attempts=5)

            assert "No available port found" in str(exc_info.value)

    def test_find_available_port_max_attempts(self):
        """Test max_attempts parameter limits port search attempts.

        Validates that find_available_port respects the max_attempts parameter
        and stops searching after that many attempts.
        """
        with patch("ansys.mapdl.core.launcher.network.check_port_status") as mock_check:
            # All ports busy
            mock_check.return_value = PortStatus(
                port=50052, available=False, used_by_mapdl=False
            )

            with pytest.raises(RuntimeError):
                find_available_port(start_port=50052, max_attempts=3)

            # Should have made exactly 3 attempts
            assert mock_check.call_count == 3

    @pytest.mark.parametrize("max_attempts", [1, 5, 10, 100])
    def test_find_available_port_respects_max_attempts_parameter(
        self, max_attempts: int
    ):
        """Test that max_attempts parameter is respected.

        Parametrized test validating max_attempts behavior for various values.
        """
        with patch("ansys.mapdl.core.launcher.network.check_port_status") as mock_check:
            mock_check.return_value = PortStatus(
                port=50052, available=False, used_by_mapdl=False
            )

            with pytest.raises(RuntimeError):
                find_available_port(start_port=50052, max_attempts=max_attempts)

            assert mock_check.call_count == max_attempts

    def test_check_port_status_with_process(self):
        """Test check_port_status when port has an associated process.

        Validates that check_port_status correctly identifies when a port
        is in use by a process and returns process information.
        """
        mock_proc = MagicMock(spec=psutil.Process)
        mock_proc.name.return_value = "notepad.exe"

        with patch(
            "ansys.mapdl.core.launcher.network._check_port_socket"
        ) as mock_socket:
            with patch(
                "ansys.mapdl.core.launcher.network._get_process_at_port"
            ) as mock_get:
                mock_socket.return_value = False
                mock_get.return_value = mock_proc

                result = check_port_status(50052)
                assert result.port == 50052
                assert result.available is False
                assert result.process == mock_proc

    def test_find_available_port_increment_by_one_sequence(self):
        """Test that port increments by 1 for each attempt (not by 2).

        New launcher behavior: increment by 1 instead of old behavior of 2.
        This test verifies the sequence: 50052 → 50053 → 50054
        """
        with patch("ansys.mapdl.core.launcher.network.check_port_status") as mock_check:
            # Track which ports are checked
            ports_checked = []

            def track_ports(port):
                ports_checked.append(port)
                return PortStatus(
                    port=port, available=(port == 50055), used_by_mapdl=False
                )

            mock_check.side_effect = track_ports

            result = find_available_port(start_port=50052, max_attempts=10)

            assert result == 50055
            # Verify increment by 1: 50052, 50053, 50054, 50055
            assert ports_checked == [50052, 50053, 50054, 50055]


# ============================================================================
# PHASE 2: Port Resolution Tests (New Increment-by-1 Logic)
# ============================================================================


class TestPhase2PortResolutionLogic:
    """Phase 2: Tests for new port resolution with increment-by-1 logic.

    Documents the new behavior:
    - Ports increment by 1 (not 2 as in old launcher)
    - find_available_port() handles the search logic
    - resolve_port() just returns the specified/default port
    """

    def test_resolve_port_busy_port_handling(self):
        """Test port handling when port is busy.

        Documents that resolve_port() doesn't check availability,
        just validates range. Availability checking is done via find_available_port().
        """
        from ansys.mapdl.core.launcher.config import resolve_port

        port = resolve_port(50052)
        assert port == 50052

    def test_resolve_port_start_instance_false(self):
        """Test port resolution when start_instance is False.

        Port is still resolved even when not starting instance.
        """
        from ansys.mapdl.core.launcher.config import resolve_launch_config

        config = resolve_launch_config(
            port=50100,
            start_instance=False,
        )
        assert config.port == 50100

    def test_find_available_port_busy_mapdl_port(self):
        """Test finding port when default MAPDL port is busy.

        When port 50052 is busy, find_available_port should check 50053, etc.
        """
        with patch("ansys.mapdl.core.launcher.network.check_port_status") as mock_check:
            # Simulate: 50052 busy (MAPDL), 50053 available
            mock_check.side_effect = [
                PortStatus(port=50052, available=False, used_by_mapdl=True),
                PortStatus(port=50053, available=True, used_by_mapdl=False),
            ]

            result = find_available_port(start_port=50052)
            assert result == 50053

    def test_find_available_port_start_instance_false_skips_checks(self):
        """Test that port checking can be skipped when not starting instance.

        When start_instance=False, port availability might not be checked.
        """
        from ansys.mapdl.core.launcher.config import resolve_launch_config

        config = resolve_launch_config(
            port=50052,
            start_instance=False,
        )
        # Port is used as-is without availability checks
        assert config.port == 50052

    def test_port_resolution_sequential_increment(self):
        """Test that port resolution increments sequentially by 1.

        NEW: Increment is 1 (was 2 in Phase 1)
        Sequence: 50052 → 50053 → 50054 → 50055...
        """
        with patch("ansys.mapdl.core.launcher.network.check_port_status") as mock_check:
            ports_checked = []

            def track_port(port):
                ports_checked.append(port)
                return PortStatus(
                    port=port, available=(port >= 50055), used_by_mapdl=False
                )

            mock_check.side_effect = track_port

            result = find_available_port(start_port=50052, max_attempts=10)

            # Verify sequential increment by 1
            assert ports_checked == [50052, 50053, 50054, 50055]
            assert result == 50055


class TestPhase2NetworkIntegration:
    """Phase 2: Integration tests for network configuration."""

    def test_port_and_ip_together(self):
        """Test port and IP resolution working together.

        Validates that port and IP can be specified together without conflicts.
        """
        from ansys.mapdl.core.launcher.config import resolve_launch_config

        with patch("socket.gethostbyname", return_value="192.168.1.100"):
            config = resolve_launch_config(
                port=50100,
                ip="192.168.1.100",
                start_instance=False,
            )
            assert config.port == 50100
            assert config.ip == "192.168.1.100"

    def test_port_resolution_with_available_port_check(self):
        """Test complete flow: resolve port then check availability.

        Documents the workflow:
        1. resolve_port() returns port number
        2. find_available_port() checks availability if needed
        """
        from ansys.mapdl.core.launcher.config import resolve_port

        port = resolve_port(50052)
        assert port == 50052

        # If needed, caller can then check availability (with mocking)
        with patch(
            "ansys.mapdl.core.launcher.network._check_port_socket"
        ) as mock_socket:
            with patch(
                "ansys.mapdl.core.launcher.network._get_process_at_port"
            ) as mock_get:
                mock_socket.return_value = True  # Port is available
                mock_get.return_value = None  # No process at port

                status = check_port_status(50052)
                assert status.available is True
                assert status.used_by_mapdl is False

    def test_default_port_and_localhost(self):
        """Test default port (50052) and localhost (127.0.0.1).

        Validates the most common configuration: local instance on default port.
        """
        from ansys.mapdl.core.launcher.config import resolve_launch_config

        with patch.dict(os.environ, {"PYMAPDL_IP": "", "PYMAPDL_PORT": ""}):
            with patch(
                "ansys.mapdl.core.launcher.config.resolve_exec_file",
                return_value="/fake/mapdl",
            ):
                with patch(
                    "ansys.mapdl.core.launcher.environment.is_wsl", return_value=False
                ):
                    config = resolve_launch_config(start_instance=True)
                    assert config.port == 50052
                    assert config.ip == "127.0.0.1"


# ============================================================================
# PHASE 4: Port max_attempts Edge Case Tests
# ============================================================================


class TestPhase4PortMaxAttemptsEdgeCases:
    """Phase 4: Edge case tests for find_available_port max_attempts parameter.

    Tests boundary conditions and error scenarios for the max_attempts parameter.
    """

    def test_find_available_port_max_attempts_zero(self):
        """Test max_attempts=0 edge case.

        When max_attempts is 0, the loop should not execute any iterations,
        resulting in a RuntimeError immediately.
        """
        with patch("ansys.mapdl.core.launcher.network.check_port_status") as mock_check:
            with pytest.raises(RuntimeError) as exc_info:
                find_available_port(start_port=50052, max_attempts=0)

            assert "No available port found" in str(exc_info.value)
            # Should not have checked any ports
            mock_check.assert_not_called()

    def test_find_available_port_max_attempts_one(self):
        """Test max_attempts=1 edge case (single attempt only).

        When max_attempts is 1, only the start_port should be checked.
        """
        with patch("ansys.mapdl.core.launcher.network.check_port_status") as mock_check:
            # First port available
            mock_check.return_value = PortStatus(
                port=50052, available=True, used_by_mapdl=False
            )

            result = find_available_port(start_port=50052, max_attempts=1)
            assert result == 50052
            assert mock_check.call_count == 1

    def test_find_available_port_max_attempts_one_unavailable(self):
        """Test max_attempts=1 when single port unavailable.

        When max_attempts is 1 and start_port is unavailable, should fail immediately.
        """
        with patch("ansys.mapdl.core.launcher.network.check_port_status") as mock_check:
            mock_check.return_value = PortStatus(
                port=50052, available=False, used_by_mapdl=False
            )

            with pytest.raises(RuntimeError) as exc_info:
                find_available_port(start_port=50052, max_attempts=1)

            assert "No available port found" in str(exc_info.value)
            assert mock_check.call_count == 1

    def test_find_available_port_max_attempts_large(self):
        """Test max_attempts with large value (1000+ attempts).

        Validates that large max_attempts values are handled correctly
        without performance issues.
        """
        with patch("ansys.mapdl.core.launcher.network.check_port_status") as mock_check:
            # Available at port 50052 + 500 offset = 50552
            def check_port(port):
                return PortStatus(
                    port=port, available=(port == 50552), used_by_mapdl=False
                )

            mock_check.side_effect = check_port

            result = find_available_port(start_port=50052, max_attempts=1000)
            assert result == 50552
            assert mock_check.call_count == 501  # Checked 50052-50552 (501 ports)

    def test_find_available_port_early_exit_when_found(self):
        """Test that search exits early when port found (doesn't check remaining).

        When an available port is found, the search should stop immediately
        without checking the remaining max_attempts.
        """
        with patch("ansys.mapdl.core.launcher.network.check_port_status") as mock_check:
            # Port 50053 is available
            def check_port(port):
                return PortStatus(
                    port=port, available=(port == 50053), used_by_mapdl=False
                )

            mock_check.side_effect = check_port

            result = find_available_port(start_port=50052, max_attempts=100)

            # Should only have checked 50052 and 50053
            assert result == 50053
            assert mock_check.call_count == 2
            # Should NOT have checked 50054, 50055, etc. (early exit)

    @pytest.mark.parametrize(
        "max_attempts,expected_calls",
        [
            (1, 1),
            (5, 5),
            (10, 10),
            (50, 50),
            (100, 100),
            (500, 500),
            (1000, 1000),
        ],
    )
    def test_find_available_port_max_attempts_boundary_parametrized(
        self, max_attempts: int, expected_calls: int
    ):
        """Test max_attempts boundary values with parametrization.

        Validates that max_attempts correctly limits the number of port checks
        across a range of values from 1 to 1000.
        """
        with patch("ansys.mapdl.core.launcher.network.check_port_status") as mock_check:
            # All ports unavailable
            mock_check.return_value = PortStatus(
                port=50052, available=False, used_by_mapdl=False
            )

            with pytest.raises(RuntimeError):
                find_available_port(start_port=50052, max_attempts=max_attempts)

            # Exactly max_attempts calls should have been made
            assert mock_check.call_count == expected_calls

    def test_find_available_port_exhaust_range_error_message(self):
        """Test that error message includes full range when exhausted.

        When all ports in range are unavailable, error message should show
        the port range that was checked.
        """
        start_port = 50052
        max_attempts = 5

        with patch("ansys.mapdl.core.launcher.network.check_port_status") as mock_check:
            mock_check.return_value = PortStatus(
                port=50052, available=False, used_by_mapdl=False
            )

            with pytest.raises(RuntimeError) as exc_info:
                find_available_port(start_port=start_port, max_attempts=max_attempts)

            error_msg = str(exc_info.value)
            assert "No available port found" in error_msg
            assert f"{start_port}" in error_msg
            assert f"{start_port + max_attempts}" in error_msg

    def test_find_available_port_sequential_port_checking(self):
        """Test that ports are checked sequentially from start_port.

        Validates that find_available_port checks ports in sequential order:
        start_port, start_port+1, start_port+2, ... up to start_port+max_attempts-1
        """
        start_port = 50052
        max_attempts = 5
        ports_checked = []

        with patch("ansys.mapdl.core.launcher.network.check_port_status") as mock_check:

            def track_port(port):
                ports_checked.append(port)
                return PortStatus(port=port, available=False, used_by_mapdl=False)

            mock_check.side_effect = track_port

            with pytest.raises(RuntimeError):
                find_available_port(start_port=start_port, max_attempts=max_attempts)

            # Verify sequential checking
            expected_ports = [start_port + i for i in range(max_attempts)]
            assert ports_checked == expected_ports

    def test_find_available_port_max_attempts_respects_boundary(self):
        """Test that max_attempts boundary is strictly enforced.

        Port at start_port + max_attempts should NOT be checked (off by one guard).
        """
        start_port = 50052
        max_attempts = 5

        with patch("ansys.mapdl.core.launcher.network.check_port_status") as mock_check:
            # Available at port beyond max_attempts
            def check_port(port):
                return PortStatus(
                    port=port,
                    available=(port == start_port + max_attempts),
                    used_by_mapdl=False,
                )

            mock_check.side_effect = check_port

            # Should fail because port at boundary is not checked
            with pytest.raises(RuntimeError):
                find_available_port(start_port=start_port, max_attempts=max_attempts)

            # Verify exactly max_attempts were checked (not max_attempts+1)
            assert mock_check.call_count == max_attempts

    def test_find_available_port_max_attempts_default_value(self):
        """Test that default max_attempts value is 100.

        Validates the default parameter value for max_attempts.
        """
        with patch("ansys.mapdl.core.launcher.network.check_port_status") as mock_check:
            mock_check.return_value = PortStatus(
                port=50052, available=False, used_by_mapdl=False
            )

            with pytest.raises(RuntimeError):
                # Don't specify max_attempts, use default
                find_available_port(start_port=50052)

            # Should have checked exactly 100 ports (default)
            assert mock_check.call_count == 100

    def test_find_available_port_very_small_range(self):
        """Test port search with very restricted range (max_attempts=1).

        Edge case where only single port can be checked.
        """
        with patch("ansys.mapdl.core.launcher.network.check_port_status") as mock_check:
            mock_check.return_value = PortStatus(
                port=65534, available=True, used_by_mapdl=False
            )

            result = find_available_port(start_port=65534, max_attempts=1)
            assert result == 65534

    def test_find_available_port_near_port_max(self):
        """Test port search near maximum valid port (65535).

        Edge case where available port might be at or near max valid port.
        """
        with patch("ansys.mapdl.core.launcher.network.check_port_status") as mock_check:
            # Port 65534 is available
            def check_port(port):
                return PortStatus(
                    port=port, available=(port == 65534), used_by_mapdl=False
                )

            mock_check.side_effect = check_port

            # Search from 65530 with range allowing to reach 65534
            result = find_available_port(start_port=65530, max_attempts=5)
            assert result == 65534

    def test_find_available_port_alternating_availability(self):
        """Test with alternating port availability pattern.

        Simulates scenario where ports are available/unavailable in alternating pattern.
        """
        with patch("ansys.mapdl.core.launcher.network.check_port_status") as mock_check:
            # Ports alternate: busy, free, busy, free, ...
            def check_port(port):
                is_available = (port % 2) == 0  # Even ports available
                return PortStatus(
                    port=port, available=is_available, used_by_mapdl=False
                )

            mock_check.side_effect = check_port

            # Start from odd port (unavailable), should find next even port
            result = find_available_port(start_port=50053, max_attempts=10)
            assert result == 50054  # First even port
            assert result % 2 == 0

    def test_find_available_port_all_mapdl_used(self):
        """Test when all checked ports show used_by_mapdl=True.

        Validates behavior when multiple MAPDL instances are running.
        """
        with patch("ansys.mapdl.core.launcher.network.check_port_status") as mock_check:
            # All ports used by MAPDL
            def check_port(port):
                return PortStatus(port=port, available=False, used_by_mapdl=True)

            mock_check.side_effect = check_port

            with pytest.raises(RuntimeError) as exc_info:
                find_available_port(start_port=50052, max_attempts=5)

            assert "No available port found" in str(exc_info.value)
            assert mock_check.call_count == 5
