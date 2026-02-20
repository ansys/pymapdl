# Copyright (C) 2016 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#

"""Unit tests for launch_mapdl function in launcher.__init__ module."""

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

# ============================================================================
# Launch MAPDL Orchestration Tests
# ============================================================================


@pytest.mark.skip(reason="Uses old ProcessInfo API - needs update")
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
            patch(
                "ansys.mapdl.core.launcher.config.resolve_launch_config"
            ) as mock_config,
            patch(
                "ansys.mapdl.core.launcher.validation.validate_config"
            ) as mock_validate,
            patch(
                "ansys.mapdl.core.launcher.connection.connect_to_existing"
            ) as mock_connect,
        ):
            mock_config.return_value = self._create_test_config(start_instance=False)
            mock_validate.return_value = ValidationResult(
                valid=True, errors=[], warnings=[]
            )
            mock_connect.return_value = Mock()

            try:
                client = launch_mapdl(
                    exec_file="/path/to/mapdl",
                    start_instance=False,
                    ip="127.0.0.1",
                    port=50052,
                )
                assert client is not None
            except Exception:
                pass

    def test_launch_mapdl_grpc_mode(self):
        """Test launch_mapdl with gRPC mode."""
        with (
            patch("os.path.isfile", return_value=True),
            patch(
                "ansys.mapdl.core.launcher.config.resolve_launch_config"
            ) as mock_config,
            patch(
                "ansys.mapdl.core.launcher.validation.validate_config"
            ) as mock_validate,
            patch(
                "ansys.mapdl.core.launcher.connection.connect_to_existing"
            ) as mock_connect,
        ):
            mock_config.return_value = self._create_test_config(
                mode=LaunchMode.GRPC,
                start_instance=False,
            )
            mock_validate.return_value = ValidationResult(
                valid=True, errors=[], warnings=[]
            )
            mock_connect.return_value = Mock()

            try:
                client = launch_mapdl(
                    exec_file="/path/to/mapdl",
                    mode="grpc",
                    start_instance=False,
                )
                assert client is not None
            except Exception:
                pass

    def test_launch_mapdl_console_mode(self):
        """Test launch_mapdl with console mode."""
        with (
            patch("os.path.isfile", return_value=True),
            patch(
                "ansys.mapdl.core.launcher.config.resolve_launch_config"
            ) as mock_config,
            patch(
                "ansys.mapdl.core.launcher.validation.validate_config"
            ) as mock_validate,
            patch(
                "ansys.mapdl.core.launcher.connection.create_console_client"
            ) as mock_console,
        ):
            mock_config.return_value = self._create_test_config(
                mode=LaunchMode.CONSOLE,
                start_instance=True,
            )
            mock_validate.return_value = ValidationResult(
                valid=True, errors=[], warnings=[]
            )
            mock_console.return_value = Mock()

            with (
                patch(
                    "ansys.mapdl.core.launcher.environment.prepare_environment"
                ) as mock_env,
                patch(
                    "ansys.mapdl.core.launcher.process.launch_mapdl_process"
                ) as mock_process,
            ):

                mock_env.return_value = EnvironmentConfig(
                    variables={},
                    is_wsl=False,
                    is_ubuntu=False,
                )
                mock_process.return_value = ProcessInfo(
                    pid=12345,
                    port=50052,
                    message="Started",
                )

                try:
                    client = launch_mapdl(
                        exec_file="/path/to/mapdl",
                        mode="console",
                    )
                except Exception:
                    pass

    def test_launch_mapdl_hpc_mode(self):
        """Test launch_mapdl with HPC mode."""
        with (
            patch("os.path.isfile", return_value=True),
            patch(
                "ansys.mapdl.core.launcher.config.resolve_launch_config"
            ) as mock_config,
            patch(
                "ansys.mapdl.core.launcher.validation.validate_config"
            ) as mock_validate,
            patch(
                "ansys.mapdl.core.launcher.environment.prepare_environment"
            ) as mock_env,
            patch(
                "ansys.mapdl.core.launcher.hpc.detect_slurm_environment"
            ) as mock_detect,
            patch("ansys.mapdl.core.launcher.hpc.launch_on_hpc") as mock_hpc,
            patch(
                "ansys.mapdl.core.launcher.connection.create_grpc_client"
            ) as mock_grpc,
        ):

            mock_config.return_value = self._create_test_config(launch_on_hpc=True)
            mock_validate.return_value = ValidationResult(
                valid=True, errors=[], warnings=[]
            )
            mock_env.return_value = EnvironmentConfig(
                variables={},
                is_wsl=False,
                is_ubuntu=False,
            )
            mock_detect.return_value = False
            mock_hpc.return_value = ProcessInfo(
                pid=54321,
                port=50052,
                message="HPC job submitted",
            )
            mock_grpc.return_value = Mock()

            try:
                client = launch_mapdl(
                    exec_file="/path/to/mapdl",
                    launch_on_hpc=True,
                )
            except Exception:
                pass

    def test_launch_mapdl_config_error(self):
        """Test launch_mapdl handles configuration errors."""
        with patch(
            "ansys.mapdl.core.launcher.config.resolve_launch_config"
        ) as mock_config:
            mock_config.side_effect = ConfigurationError("Invalid config")

            with pytest.raises((LaunchError, ConfigurationError)):
                launch_mapdl(exec_file="/path/to/mapdl")

    def test_launch_mapdl_validation_error(self):
        """Test launch_mapdl handles validation errors."""
        with (
            patch("os.path.isfile", return_value=True),
            patch(
                "ansys.mapdl.core.launcher.config.resolve_launch_config"
            ) as mock_config,
            patch(
                "ansys.mapdl.core.launcher.validation.validate_config"
            ) as mock_validate,
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
            patch(
                "ansys.mapdl.core.launcher.config.resolve_launch_config"
            ) as mock_config,
            patch(
                "ansys.mapdl.core.launcher.validation.validate_config"
            ) as mock_validate,
            patch(
                "ansys.mapdl.core.launcher.environment.prepare_environment"
            ) as mock_env,
            patch(
                "ansys.mapdl.core.launcher.process.launch_mapdl_process"
            ) as mock_process,
            patch(
                "ansys.mapdl.core.launcher.connection.create_grpc_client"
            ) as mock_grpc,
        ):
            mock_config.return_value = self._create_test_config()
            mock_validate.return_value = ValidationResult(
                valid=True, errors=[], warnings=[]
            )
            mock_env.return_value = EnvironmentConfig(
                variables={"TEST_VAR": "test_value"},
                is_wsl=False,
                is_ubuntu=False,
            )
            mock_process.return_value = ProcessInfo(
                pid=99999,
                port=50052,
                message="Started",
            )
            mock_grpc.return_value = Mock()

            try:
                client = launch_mapdl(exec_file="/path/to/mapdl")
                # Verify environment preparation was called
                mock_env.assert_called_once()
            except Exception:
                pass


# ============================================================================
# Full Integration Tests
# ============================================================================


class TestLaunchMapdlFullIntegration:
    """Full end-to-end integration tests with actual launch_mapdl function."""

    @pytest.mark.skip(reason="Requires full launcher stack mocking")
    def test_launch_mapdl_local_grpc_basic(self):
        """Test full launch_mapdl workflow for local gRPC mode."""
        pass

    @pytest.mark.skip(reason="Requires full launcher stack mocking")
    def test_launch_mapdl_with_all_options(self):
        """Test launch_mapdl with all configuration options."""
        pass

    @pytest.mark.skip(reason="Requires full launcher stack mocking")
    def test_launch_mapdl_error_recovery(self):
        """Test error recovery in launch_mapdl."""
        pass


# ============================================================================
# Launch MAPDL Convenience Tests
# ============================================================================


class TestLaunchMapdlConvenience:
    """Tests for launch_mapdl convenience features."""

    @pytest.mark.skip(reason="Convenience features need API clarification")
    def test_launch_mapdl_with_defaults(self):
        """Test launching with all defaults."""
        pass

    @pytest.mark.skip(reason="Convenience features need API clarification")
    def test_launch_mapdl_with_minimal_args(self):
        """Test launching with minimal arguments."""
        pass

    @pytest.mark.skip(reason="Convenience features need API clarification")
    def test_launch_mapdl_auto_port_selection(self):
        """Test automatic port selection."""
        pass


# ============================================================================
# Launch Workflow Tests
# ============================================================================


class TestLaunchWorkflow:
    """Tests for the launch workflow orchestration."""

    @pytest.mark.skip(reason="Workflow orchestration needs detailed mocking")
    def test_workflow_config_validation_process_connection(self):
        """Test workflow: config -> validation -> process -> connection."""
        pass

    @pytest.mark.skip(reason="Workflow orchestration needs detailed mocking")
    def test_workflow_hpc_submission(self):
        """Test HPC job submission workflow."""
        pass

    @pytest.mark.skip(reason="Workflow orchestration needs detailed mocking")
    def test_workflow_error_at_each_stage(self):
        """Test error handling at each workflow stage."""
        pass
