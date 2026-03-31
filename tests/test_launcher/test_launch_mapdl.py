# Copyright (C) 2016 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#

"""Unit tests for launch_mapdl function in launcher.__init__ module."""

import os
from unittest.mock import Mock, patch

import pytest

from ansys.mapdl.core.launcher import (
    ConfigurationError,
    LaunchConfig,
    LaunchError,
    LaunchMode,
    launch_mapdl,
)
from ansys.mapdl.core.launcher.models import (
    EnvironmentConfig,
    ProcessInfo,
    ValidationResult,
)

try:
    from conftest import QUICK_LAUNCH_SWITCHES, requires
except ImportError:
    from tests.conftest import QUICK_LAUNCH_SWITCHES, requires

# ============================================================================
# Launch MAPDL Orchestration Tests
# ============================================================================


class TestLaunchMapdlOrchestration:
    """Tests for main launch_mapdl orchestration."""

    def _create_test_config(self, **overrides):
        """Create a test LaunchConfig."""
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

    def test_launch_mapdl_connection_only(self):
        """Test launch_mapdl with start_instance=False."""
        with (
            patch("os.path.isfile", return_value=True),
            patch("ansys.mapdl.core.launcher.resolve_launch_config") as mock_config,
            patch("ansys.mapdl.core.launcher.validate_config") as mock_validate,
            patch("ansys.mapdl.core.launcher.connect_to_existing") as mock_connect,
        ):
            mock_config.return_value = self._create_test_config(start_instance=False)
            mock_validate.return_value = ValidationResult(
                valid=True, errors=[], warnings=[]
            )
            mock_connect.return_value = Mock()

            client = launch_mapdl(
                exec_file="/path/to/mapdl",
                start_instance=False,
                ip="127.0.0.1",
                port=50052,
            )
            assert client is not None

    def test_launch_mapdl_grpc_mode(self):
        """Test launch_mapdl with gRPC mode."""
        with (
            patch("os.path.isfile", return_value=True),
            patch("ansys.mapdl.core.launcher.resolve_launch_config") as mock_config,
            patch("ansys.mapdl.core.launcher.validate_config") as mock_validate,
            patch("ansys.mapdl.core.launcher.connect_to_existing") as mock_connect,
        ):
            mock_config.return_value = self._create_test_config(
                mode=LaunchMode.GRPC,
                start_instance=False,
            )
            mock_validate.return_value = ValidationResult(
                valid=True, errors=[], warnings=[]
            )
            mock_connect.return_value = Mock()

            client = launch_mapdl(
                exec_file="/path/to/mapdl",
                mode="grpc",
                start_instance=False,
            )
            assert client is not None

    def test_launch_mapdl_console_mode(self):
        """Test launch_mapdl with console mode."""
        with (
            patch("os.path.isfile", return_value=True),
            patch("ansys.mapdl.core.launcher.resolve_launch_config") as mock_config,
            patch("ansys.mapdl.core.launcher.validate_config") as mock_validate,
            patch("ansys.mapdl.core.launcher.prepare_environment") as mock_env,
            patch("ansys.mapdl.core.launcher._launch_mapdl_process") as mock_process,
            patch("ansys.mapdl.core.launcher.create_console_client") as mock_console,
            patch("os.name", "posix"),
        ):
            mock_config.return_value = self._create_test_config(
                mode=LaunchMode.CONSOLE,
                start_instance=True,
            )
            mock_validate.return_value = ValidationResult(
                valid=True, errors=[], warnings=[]
            )
            mock_env.return_value = EnvironmentConfig(
                variables={},
            )
            mock_process.return_value = ProcessInfo(
                process=Mock(),
                ip="123.45.67.89",
                pid=12345,
                port=50052,
            )
            mock_console.return_value = Mock()

            launch_mapdl(
                exec_file="/path/to/mapdl",
                mode="console",
            )

    def test_launch_mapdl_hpc_mode(self):
        """Test launch_mapdl with HPC mode."""
        with (
            patch("os.path.isfile", return_value=True),
            patch("ansys.mapdl.core.launcher.resolve_launch_config") as mock_config,
            patch("ansys.mapdl.core.launcher.validate_config") as mock_validate,
            patch("ansys.mapdl.core.launcher.prepare_environment") as mock_env,
            patch("ansys.mapdl.core.launcher.detect_slurm_environment") as mock_detect,
            patch("ansys.mapdl.core.launcher._launch_on_hpc_fn") as mock_hpc,
            patch("ansys.mapdl.core.launcher.create_grpc_client") as mock_grpc,
            patch("os.name", "posix"),
            patch("os.access", Mock(return_value=True)),
        ):

            mock_config.return_value = self._create_test_config(launch_on_hpc=True)
            mock_validate.return_value = ValidationResult(
                valid=True, errors=[], warnings=[]
            )
            mock_env.return_value = EnvironmentConfig(
                variables={},
            )
            mock_detect.return_value = False
            mock_hpc.return_value = ProcessInfo(
                process=Mock,
                ip="123.45.67.89",
                pid=54321,
                port=50052,
            )
            mock_grpc.return_value = Mock()

            launch_mapdl(
                exec_file="/path/to/mapdl",
                launch_on_hpc=True,
            )

    def test_launch_mapdl_config_error(self):
        """Test launch_mapdl handles configuration errors."""
        with patch("ansys.mapdl.core.launcher.resolve_launch_config") as mock_config:
            mock_config.side_effect = ConfigurationError("Invalid config")

            with pytest.raises((LaunchError, ConfigurationError)):
                launch_mapdl(exec_file="/path/to/mapdl")

    def test_launch_mapdl_validation_error(self):
        """Test launch_mapdl handles validation errors."""
        with (
            patch("os.path.isfile", return_value=True),
            patch("ansys.mapdl.core.launcher.resolve_launch_config") as mock_config,
            patch("ansys.mapdl.core.launcher.validate_config") as mock_validate,
        ):
            mock_config.return_value = self._create_test_config()
            mock_validate.return_value = ValidationResult(
                valid=False,
                errors=["Invalid nproc"],
                warnings=[],
            )

            with pytest.raises((LaunchError, ConfigurationError)):
                launch_mapdl(exec_file="/path/to/mapdl")

    def test_launch_mapdl_env_preparation(self):
        """Test launch_mapdl prepares environment."""
        with (
            patch("os.path.isfile", return_value=True),
            patch("ansys.mapdl.core.launcher.resolve_launch_config") as mock_config,
            patch("ansys.mapdl.core.launcher.validate_config") as mock_validate,
            patch("ansys.mapdl.core.launcher.prepare_environment") as mock_env,
            patch("ansys.mapdl.core.launcher._launch_mapdl_process") as mock_process,
            patch("ansys.mapdl.core.launcher.create_grpc_client") as mock_grpc,
        ):
            mock_config.return_value = self._create_test_config()
            mock_validate.return_value = ValidationResult(
                valid=True, errors=[], warnings=[]
            )
            mock_env.return_value = EnvironmentConfig(
                variables={"TEST_VAR": "test_value"},
            )
            mock_process.return_value = ProcessInfo(
                process=Mock,
                ip="123.45.67.89",
                pid=99999,
                port=50052,
            )
            mock_grpc.return_value = Mock()

            launch_mapdl(exec_file="/path/to/mapdl")
            # Verify environment preparation was called
            mock_env.assert_called_once()


# ============================================================================
# Integration Tests (require a live MAPDL instance)
# ============================================================================


@requires("local")
@requires("linux")
@requires("grpc")
def test_launch_uds_transport(monkeypatch):
    """Test that MAPDL defaults to UDS transport when launched locally on Linux.

    UDS (Unix Domain Sockets) is the default gRPC transport for local Linux
    connections. This test verifies that ``launch_mapdl`` produces an instance
    whose ``transport_mode`` is ``"uds"`` when no explicit transport is requested
    and no related environment variables override the default.
    """
    monkeypatch.delenv("PYMAPDL_GRPC_TRANSPORT", raising=False)
    monkeypatch.delenv("ANSYS_MAPDL_GRPC_TRANSPORT", raising=False)

    mapdl_ = None
    try:
        mapdl_ = launch_mapdl(
            additional_switches=QUICK_LAUNCH_SWITCHES,
            port=int(os.getenv("PYMAPDL_TEST_PORT", "50052")) + 20,
        )
        assert mapdl_.transport_mode == "uds"

    finally:
        if mapdl_ is not None:
            mapdl_.exit(force=True)
