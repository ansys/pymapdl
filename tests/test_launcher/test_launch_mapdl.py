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
    TransportMode,
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
# UDS Environment Variable Tests
# ============================================================================


class TestUdsEnvVarInjection:
    """Tests for the ANSYS_MAPDL_UDS_PATH injection in _launch_mapdl_common."""

    def _create_uds_config(
        self, transport_mode=TransportMode.UDS, uds_dir="/tmp/.conn"
    ):
        """Create a LaunchConfig with UDS transport defaults."""
        return LaunchConfig(
            exec_file="/path/to/mapdl",
            run_location="/tmp",
            jobname="file",
            nproc=2,
            port=50052,
            ip="127.0.0.1",
            mode=LaunchMode.GRPC,
            version=222,
            start_instance=True,
            ram=None,
            timeout=45,
            cleanup_on_exit=True,
            clear_on_connect=True,
            override=False,
            remove_temp_dir_on_exit=False,
            set_no_abort=True,
            additional_switches="",
            license_type=None,
            launch_on_hpc=False,
            running_on_hpc=False,
            scheduler_options=None,
            loglevel="ERROR",
            log_apdl=None,
            print_com=False,
            mapdl_output=None,
            transport_mode=transport_mode,
            uds_dir=uds_dir,
            uds_id=None,
            certs_dir=None,
        )

    def test_uds_env_var_set_on_linux_with_uds_dir(self, tmp_path):
        """ANSYS_MAPDL_UDS_PATH is injected when platform=Linux, transport=UDS, uds_dir set."""
        uds_dir = str(tmp_path / ".conn")
        env_vars = {}

        with (
            patch("ansys.mapdl.core.launcher.resolve_launch_config") as mock_config,
            patch("ansys.mapdl.core.launcher.validate_config") as mock_validate,
            patch("ansys.mapdl.core.launcher.prepare_environment") as mock_env,
            patch("ansys.mapdl.core.launcher._launch_mapdl_process") as mock_process,
            patch("ansys.mapdl.core.launcher.create_grpc_client") as mock_grpc,
            patch("ansys.mapdl.core.launcher.platform") as mock_platform,
        ):
            mock_platform.system.return_value = "Linux"
            mock_config.return_value = self._create_uds_config(
                transport_mode=TransportMode.UDS, uds_dir=uds_dir
            )
            mock_validate.return_value = ValidationResult(
                valid=True, errors=[], warnings=[]
            )
            mock_env.return_value = EnvironmentConfig(variables=env_vars)
            mock_process.return_value = ProcessInfo(
                process=Mock(), ip="127.0.0.1", pid=12345, port=50052
            )
            mock_grpc.return_value = Mock()

            launch_mapdl(exec_file="/path/to/mapdl")

        assert "ANSYS_MAPDL_UDS_PATH" in env_vars
        assert env_vars["ANSYS_MAPDL_UDS_PATH"] == uds_dir

    def test_uds_env_var_not_set_on_non_linux(self, tmp_path):
        """ANSYS_MAPDL_UDS_PATH is NOT injected when platform is not Linux."""
        uds_dir = str(tmp_path / ".conn")
        env_vars = {}

        with (
            patch("ansys.mapdl.core.launcher.resolve_launch_config") as mock_config,
            patch("ansys.mapdl.core.launcher.validate_config") as mock_validate,
            patch("ansys.mapdl.core.launcher.prepare_environment") as mock_env,
            patch("ansys.mapdl.core.launcher._launch_mapdl_process") as mock_process,
            patch("ansys.mapdl.core.launcher.create_grpc_client") as mock_grpc,
            patch("ansys.mapdl.core.launcher.platform") as mock_platform,
        ):
            mock_platform.system.return_value = "Darwin"
            mock_config.return_value = self._create_uds_config(
                transport_mode=TransportMode.UDS, uds_dir=uds_dir
            )
            mock_validate.return_value = ValidationResult(
                valid=True, errors=[], warnings=[]
            )
            mock_env.return_value = EnvironmentConfig(variables=env_vars)
            mock_process.return_value = ProcessInfo(
                process=Mock(), ip="127.0.0.1", pid=12345, port=50052
            )
            mock_grpc.return_value = Mock()

            launch_mapdl(exec_file="/path/to/mapdl")

        assert "ANSYS_MAPDL_UDS_PATH" not in env_vars

    def test_uds_env_var_not_set_for_non_uds_transport(self, tmp_path):
        """ANSYS_MAPDL_UDS_PATH is NOT injected when transport mode is not UDS."""
        uds_dir = str(tmp_path / ".conn")
        env_vars = {}

        with (
            patch("ansys.mapdl.core.launcher.resolve_launch_config") as mock_config,
            patch("ansys.mapdl.core.launcher.validate_config") as mock_validate,
            patch("ansys.mapdl.core.launcher.prepare_environment") as mock_env,
            patch("ansys.mapdl.core.launcher._launch_mapdl_process") as mock_process,
            patch("ansys.mapdl.core.launcher.create_grpc_client") as mock_grpc,
            patch("ansys.mapdl.core.launcher.platform") as mock_platform,
        ):
            mock_platform.system.return_value = "Linux"
            mock_config.return_value = self._create_uds_config(
                transport_mode=TransportMode.INSECURE, uds_dir=uds_dir
            )
            mock_validate.return_value = ValidationResult(
                valid=True, errors=[], warnings=[]
            )
            mock_env.return_value = EnvironmentConfig(variables=env_vars)
            mock_process.return_value = ProcessInfo(
                process=Mock(), ip="127.0.0.1", pid=12345, port=50052
            )
            mock_grpc.return_value = Mock()

            launch_mapdl(exec_file="/path/to/mapdl")

        assert "ANSYS_MAPDL_UDS_PATH" not in env_vars

    def test_uds_env_var_not_set_when_uds_dir_is_none(self):
        """ANSYS_MAPDL_UDS_PATH is NOT injected when uds_dir is None."""
        env_vars = {}

        with (
            patch("ansys.mapdl.core.launcher.resolve_launch_config") as mock_config,
            patch("ansys.mapdl.core.launcher.validate_config") as mock_validate,
            patch("ansys.mapdl.core.launcher.prepare_environment") as mock_env,
            patch("ansys.mapdl.core.launcher._launch_mapdl_process") as mock_process,
            patch("ansys.mapdl.core.launcher.create_grpc_client") as mock_grpc,
            patch("ansys.mapdl.core.launcher.platform") as mock_platform,
        ):
            mock_platform.system.return_value = "Linux"
            mock_config.return_value = self._create_uds_config(
                transport_mode=TransportMode.UDS, uds_dir=None
            )
            mock_validate.return_value = ValidationResult(
                valid=True, errors=[], warnings=[]
            )
            mock_env.return_value = EnvironmentConfig(variables=env_vars)
            mock_process.return_value = ProcessInfo(
                process=Mock(), ip="127.0.0.1", pid=12345, port=50052
            )
            mock_grpc.return_value = Mock()

            launch_mapdl(exec_file="/path/to/mapdl")

        assert "ANSYS_MAPDL_UDS_PATH" not in env_vars

    def test_uds_env_var_does_not_overwrite_existing(self, tmp_path):
        """setdefault ensures ANSYS_MAPDL_UDS_PATH is not overwritten if already set."""
        uds_dir = str(tmp_path / ".conn")
        existing_value = "/custom/uds/path"
        env_vars = {"ANSYS_MAPDL_UDS_PATH": existing_value}

        with (
            patch("ansys.mapdl.core.launcher.resolve_launch_config") as mock_config,
            patch("ansys.mapdl.core.launcher.validate_config") as mock_validate,
            patch("ansys.mapdl.core.launcher.prepare_environment") as mock_env,
            patch("ansys.mapdl.core.launcher._launch_mapdl_process") as mock_process,
            patch("ansys.mapdl.core.launcher.create_grpc_client") as mock_grpc,
            patch("ansys.mapdl.core.launcher.platform") as mock_platform,
        ):
            mock_platform.system.return_value = "Linux"
            mock_config.return_value = self._create_uds_config(
                transport_mode=TransportMode.UDS, uds_dir=uds_dir
            )
            mock_validate.return_value = ValidationResult(
                valid=True, errors=[], warnings=[]
            )
            mock_env.return_value = EnvironmentConfig(variables=env_vars)
            mock_process.return_value = ProcessInfo(
                process=Mock(), ip="127.0.0.1", pid=12345, port=50052
            )
            mock_grpc.return_value = Mock()

            launch_mapdl(exec_file="/path/to/mapdl")

        # setdefault must not overwrite an already-set value
        assert env_vars["ANSYS_MAPDL_UDS_PATH"] == existing_value

    def test_uds_makedirs_called_on_linux_uds(self, tmp_path):
        """os.makedirs is called to create uds_dir on Linux UDS launch."""
        uds_dir = str(tmp_path / "new_conn_dir")
        env_vars = {}

        with (
            patch("ansys.mapdl.core.launcher.resolve_launch_config") as mock_config,
            patch("ansys.mapdl.core.launcher.validate_config") as mock_validate,
            patch("ansys.mapdl.core.launcher.prepare_environment") as mock_env,
            patch("ansys.mapdl.core.launcher._launch_mapdl_process") as mock_process,
            patch("ansys.mapdl.core.launcher.create_grpc_client") as mock_grpc,
            patch("ansys.mapdl.core.launcher.platform") as mock_platform,
            patch("ansys.mapdl.core.launcher.os.makedirs") as mock_makedirs,
        ):
            mock_platform.system.return_value = "Linux"
            mock_config.return_value = self._create_uds_config(
                transport_mode=TransportMode.UDS, uds_dir=uds_dir
            )
            mock_validate.return_value = ValidationResult(
                valid=True, errors=[], warnings=[]
            )
            mock_env.return_value = EnvironmentConfig(variables=env_vars)
            mock_process.return_value = ProcessInfo(
                process=Mock(), ip="127.0.0.1", pid=12345, port=50052
            )
            mock_grpc.return_value = Mock()

            launch_mapdl(exec_file="/path/to/mapdl")

        mock_makedirs.assert_called_once_with(uds_dir, exist_ok=True)


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
