# Copyright (C) 2016 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#

"""Unit tests for launch_mapdl_process function in launcher module."""

from unittest.mock import Mock, patch

import pytest

from ansys.mapdl.core.launcher import (
    ConfigurationError,
    LaunchError,
    LaunchMode,
    launch_mapdl_process,
)
from ansys.mapdl.core.launcher.models import (
    EnvironmentConfig,
    ProcessInfo,
    ValidationResult,
)

# ============================================================================
# launch_mapdl_process Tests
# ============================================================================


class TestLaunchMapdlProcessOnly:
    """Tests for launch_mapdl_process function."""

    def _create_test_config(self, **overrides):
        """Create a test LaunchConfig."""
        from ansys.mapdl.core.launcher.models import LaunchConfig

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
            "env_vars": {},
        }
        defaults.update(overrides)
        return LaunchConfig(**defaults)

    def _create_test_env_config(self):
        """Create a test EnvironmentConfig."""
        return EnvironmentConfig(
            variables={"PATH": "/usr/bin", "LD_LIBRARY_PATH": "/lib"}
        )

    def _create_test_process_info(self, **overrides):
        """Create a test ProcessInfo."""
        defaults = {
            "process": Mock(),
            "port": 50052,
            "ip": "127.0.0.1",
            "pid": 12345,
        }
        defaults.update(overrides)
        return ProcessInfo(**defaults)

    def test_process_only_returns_tuple(self):
        """Test that launch_mapdl_process returns (ip, port, pid) tuple."""
        with (
            patch(
                "ansys.mapdl.core.launcher.resolve_launch_config"
            ) as mock_resolve_config,
            patch("ansys.mapdl.core.launcher.validate_config") as mock_validate,
            patch("ansys.mapdl.core.launcher.prepare_environment") as mock_prep_env,
            patch(
                "ansys.mapdl.core.launcher.launch_mapdl_process"
            ) as mock_launch_process,
        ):
            # Setup mocks
            mock_resolve_config.return_value = self._create_test_config()
            mock_validate.return_value = ValidationResult(
                valid=True, errors=[], warnings=[]
            )
            mock_prep_env.return_value = self._create_test_env_config()
            mock_launch_process.return_value = self._create_test_process_info()

            # Call function
            result = launch_mapdl_process(
                exec_file="/path/to/mapdl",
                nproc=4,
                port=50052,
            )

            # Verify result is a tuple
            assert isinstance(result, tuple)
            assert len(result) == 3
            assert result == ("127.0.0.1", 50052, 12345)

    def test_process_only_with_no_pid(self):
        """Test launch_mapdl_process when process has no PID (HPC case)."""
        with (
            patch(
                "ansys.mapdl.core.launcher.resolve_launch_config"
            ) as mock_resolve_config,
            patch("ansys.mapdl.core.launcher.validate_config") as mock_validate,
            patch("ansys.mapdl.core.launcher.prepare_environment") as mock_prep_env,
            patch(
                "ansys.mapdl.core.launcher.launch_mapdl_process"
            ) as mock_launch_process,
        ):
            # Setup mocks - no PID for HPC
            mock_resolve_config.return_value = self._create_test_config()
            mock_validate.return_value = ValidationResult(
                valid=True, errors=[], warnings=[]
            )
            mock_prep_env.return_value = self._create_test_env_config()
            mock_launch_process.return_value = self._create_test_process_info(pid=None)

            # Call function
            result = launch_mapdl_process(
                exec_file="/path/to/mapdl",
                nproc=4,
            )

            # Verify result includes None PID
            assert result == ("127.0.0.1", 50052, None)

    def test_process_only_raises_error_if_not_starting_instance(self):
        """Test that launch_mapdl_process raises error if start_instance=False."""
        with (
            patch(
                "ansys.mapdl.core.launcher.resolve_launch_config"
            ) as mock_resolve_config,
        ):
            # Setup mocks - start_instance=False
            mock_resolve_config.return_value = self._create_test_config(
                start_instance=False
            )

            # Call function - should raise LaunchError
            with pytest.raises(LaunchError) as exc_info:
                launch_mapdl_process(
                    exec_file="/path/to/mapdl",
                    start_instance=False,
                    ip="127.0.0.1",
                    port=50052,
                )

            assert "start_instance=True" in str(exc_info.value)

    def test_process_only_configuration_error_handling(self):
        """Test that configuration errors are properly handled."""
        with patch(
            "ansys.mapdl.core.launcher.resolve_launch_config"
        ) as mock_resolve_config:
            # Setup mocks - raise ConfigurationError
            mock_resolve_config.side_effect = ConfigurationError("Invalid config")

            # Call function - should raise LaunchError
            with pytest.raises(LaunchError) as exc_info:
                launch_mapdl_process(
                    exec_file="/path/to/mapdl",
                )

            assert "Invalid launch configuration" in str(exc_info.value)

    def test_process_only_validation_error_handling(self):
        """Test that validation errors are properly handled."""
        with (
            patch(
                "ansys.mapdl.core.launcher.resolve_launch_config"
            ) as mock_resolve_config,
            patch("ansys.mapdl.core.launcher.validate_config") as mock_validate,
        ):
            # Setup mocks - validation failure
            mock_resolve_config.return_value = self._create_test_config()
            mock_validate.return_value = ValidationResult(
                valid=False,
                errors=["Missing exec_file", "Invalid port"],
                warnings=[],
            )

            # Call function - should raise LaunchError
            with pytest.raises(LaunchError) as exc_info:
                launch_mapdl_process(
                    exec_file="/path/to/mapdl",
                )

            error_msg = str(exc_info.value)
            assert "Configuration validation failed" in error_msg
            assert "Missing exec_file" in error_msg
            assert "Invalid port" in error_msg

    def test_process_only_environment_prep_error_handling(self):
        """Test that environment preparation errors are properly handled."""
        with (
            patch(
                "ansys.mapdl.core.launcher.resolve_launch_config"
            ) as mock_resolve_config,
            patch("ansys.mapdl.core.launcher.validate_config") as mock_validate,
            patch("ansys.mapdl.core.launcher.prepare_environment") as mock_prep_env,
        ):
            # Setup mocks - environment prep failure
            mock_resolve_config.return_value = self._create_test_config()
            mock_validate.return_value = ValidationResult(
                valid=True, errors=[], warnings=[]
            )
            mock_prep_env.side_effect = RuntimeError("Failed to prepare environment")

            # Call function - should raise LaunchError
            with pytest.raises(LaunchError) as exc_info:
                launch_mapdl_process(
                    exec_file="/path/to/mapdl",
                )

            assert "Failed to prepare environment" in str(exc_info.value)

    def test_process_only_launch_process_error_handling(self):
        """Test that process launch errors are properly handled."""
        with (
            patch(
                "ansys.mapdl.core.launcher.resolve_launch_config"
            ) as mock_resolve_config,
            patch("ansys.mapdl.core.launcher.validate_config") as mock_validate,
            patch("ansys.mapdl.core.launcher.prepare_environment") as mock_prep_env,
            patch(
                "ansys.mapdl.core.launcher.launch_mapdl_process"
            ) as mock_launch_process,
        ):
            # Setup mocks - process launch failure
            mock_resolve_config.return_value = self._create_test_config()
            mock_validate.return_value = ValidationResult(
                valid=True, errors=[], warnings=[]
            )
            mock_prep_env.return_value = self._create_test_env_config()
            mock_launch_process.side_effect = RuntimeError("Failed to start MAPDL")

            # Call function - should raise LaunchError
            with pytest.raises(LaunchError) as exc_info:
                launch_mapdl_process(
                    exec_file="/path/to/mapdl",
                )

            assert "Failed to launch MAPDL" in str(exc_info.value)

    def test_process_only_with_additional_switches(self):
        """Test launch_mapdl_process with additional switches."""
        with (
            patch(
                "ansys.mapdl.core.launcher.resolve_launch_config"
            ) as mock_resolve_config,
            patch("ansys.mapdl.core.launcher.validate_config") as mock_validate,
            patch("ansys.mapdl.core.launcher.prepare_environment") as mock_prep_env,
            patch(
                "ansys.mapdl.core.launcher.launch_mapdl_process"
            ) as mock_launch_process,
        ):
            # Setup mocks
            mock_resolve_config.return_value = self._create_test_config(
                additional_switches="aa_r"
            )
            mock_validate.return_value = ValidationResult(
                valid=True, errors=[], warnings=[]
            )
            mock_prep_env.return_value = self._create_test_env_config()
            mock_launch_process.return_value = self._create_test_process_info()

            # Call function
            result = launch_mapdl_process(
                exec_file="/path/to/mapdl",
                additional_switches="aa_r",
            )

            # Verify resolve_launch_config was called with correct args
            mock_resolve_config.assert_called_once()
            call_kwargs = mock_resolve_config.call_args[1]
            assert call_kwargs["additional_switches"] == "aa_r"

            # Verify result
            assert result == ("127.0.0.1", 50052, 12345)

    def test_process_only_with_custom_port(self):
        """Test launch_mapdl_process with custom port."""
        with (
            patch(
                "ansys.mapdl.core.launcher.resolve_launch_config"
            ) as mock_resolve_config,
            patch("ansys.mapdl.core.launcher.validate_config") as mock_validate,
            patch("ansys.mapdl.core.launcher.prepare_environment") as mock_prep_env,
            patch(
                "ansys.mapdl.core.launcher.launch_mapdl_process"
            ) as mock_launch_process,
        ):
            # Setup mocks with custom port
            mock_resolve_config.return_value = self._create_test_config(port=50053)
            mock_validate.return_value = ValidationResult(
                valid=True, errors=[], warnings=[]
            )
            mock_prep_env.return_value = self._create_test_env_config()
            mock_launch_process.return_value = self._create_test_process_info(
                port=50053
            )

            # Call function
            result = launch_mapdl_process(
                exec_file="/path/to/mapdl",
                port=50053,
            )

            # Verify result
            assert result[1] == 50053

    def test_process_only_with_env_vars(self):
        """Test launch_mapdl_process with environment variables."""
        with (
            patch(
                "ansys.mapdl.core.launcher.resolve_launch_config"
            ) as mock_resolve_config,
            patch("ansys.mapdl.core.launcher.validate_config") as mock_validate,
            patch("ansys.mapdl.core.launcher.prepare_environment") as mock_prep_env,
            patch(
                "ansys.mapdl.core.launcher.launch_mapdl_process"
            ) as mock_launch_process,
        ):
            # Setup mocks
            mock_resolve_config.return_value = self._create_test_config()
            mock_validate.return_value = ValidationResult(
                valid=True, errors=[], warnings=[]
            )
            mock_prep_env.return_value = self._create_test_env_config()
            mock_launch_process.return_value = self._create_test_process_info()

            # Call function with environment variables
            result = launch_mapdl_process(
                exec_file="/path/to/mapdl",
                add_env_vars={"MY_VAR": "value1"},
                replace_env_vars={"REPLACE_VAR": "value2"},
            )

            # Verify resolve_launch_config was called with merged env vars
            call_kwargs = mock_resolve_config.call_args[1]
            env_vars = call_kwargs["env_vars"]
            assert env_vars is not None
            assert "MY_VAR" in env_vars
            assert "REPLACE_VAR" in env_vars

            # Verify result
            assert result == ("127.0.0.1", 50052, 12345)

    def test_process_only_with_license_type(self):
        """Test launch_mapdl_process with license type."""
        with (
            patch(
                "ansys.mapdl.core.launcher.resolve_launch_config"
            ) as mock_resolve_config,
            patch("ansys.mapdl.core.launcher.validate_config") as mock_validate,
            patch("ansys.mapdl.core.launcher.prepare_environment") as mock_prep_env,
            patch(
                "ansys.mapdl.core.launcher.launch_mapdl_process"
            ) as mock_launch_process,
        ):
            # Setup mocks
            mock_resolve_config.return_value = self._create_test_config(
                license_type="ansys"
            )
            mock_validate.return_value = ValidationResult(
                valid=True, errors=[], warnings=[]
            )
            mock_prep_env.return_value = self._create_test_env_config()
            mock_launch_process.return_value = self._create_test_process_info()

            # Call function
            result = launch_mapdl_process(
                exec_file="/path/to/mapdl",
                license_type="ansys",
            )

            # Verify resolve_launch_config was called with correct license type
            call_kwargs = mock_resolve_config.call_args[1]
            assert call_kwargs["license_type"] == "ansys"

            # Verify result
            assert result == ("127.0.0.1", 50052, 12345)

    def test_process_only_ignores_kwargs(self):
        """Test that launch_mapdl_process ignores unknown kwargs."""
        with (
            patch(
                "ansys.mapdl.core.launcher.resolve_launch_config"
            ) as mock_resolve_config,
            patch("ansys.mapdl.core.launcher.validate_config") as mock_validate,
            patch("ansys.mapdl.core.launcher.prepare_environment") as mock_prep_env,
            patch(
                "ansys.mapdl.core.launcher.launch_mapdl_process"
            ) as mock_launch_process,
        ):
            # Setup mocks
            mock_resolve_config.return_value = self._create_test_config()
            mock_validate.return_value = ValidationResult(
                valid=True, errors=[], warnings=[]
            )
            mock_prep_env.return_value = self._create_test_env_config()
            mock_launch_process.return_value = self._create_test_process_info()

            # Call function with unknown kwargs
            result = launch_mapdl_process(
                exec_file="/path/to/mapdl",
                unknown_param="should_be_ignored",
                another_unknown=42,
            )

            # Verify result is still correct
            assert result == ("127.0.0.1", 50052, 12345)

    def test_process_only_all_parameters_passed_through(self):
        """Test that all documented parameters are passed to resolve_launch_config."""
        with (
            patch(
                "ansys.mapdl.core.launcher.resolve_launch_config"
            ) as mock_resolve_config,
            patch("ansys.mapdl.core.launcher.validate_config") as mock_validate,
            patch("ansys.mapdl.core.launcher.prepare_environment") as mock_prep_env,
            patch(
                "ansys.mapdl.core.launcher.launch_mapdl_process"
            ) as mock_launch_process,
        ):
            # Setup mocks
            mock_resolve_config.return_value = self._create_test_config()
            mock_validate.return_value = ValidationResult(
                valid=True, errors=[], warnings=[]
            )
            mock_prep_env.return_value = self._create_test_env_config()
            mock_launch_process.return_value = self._create_test_process_info()

            # Call with various parameters
            launch_mapdl_process(
                exec_file="/path/to/mapdl",
                run_location="/tmp/mapdl",
                jobname="myjob",
                nproc=8,
                port=50053,
                ram=8192,
                timeout=60,
                override=True,
                version=231,
                license_type="enterprise",
            )

            # Verify resolve_launch_config was called with all parameters
            call_kwargs = mock_resolve_config.call_args[1]
            assert call_kwargs["exec_file"] == "/path/to/mapdl"
            assert call_kwargs["run_location"] == "/tmp/mapdl"
            assert call_kwargs["jobname"] == "myjob"
            assert call_kwargs["nproc"] == 8
            assert call_kwargs["port"] == 50053
            assert call_kwargs["ram"] == 8192
            assert call_kwargs["timeout"] == 60
            assert call_kwargs["override"] is True
            assert call_kwargs["version"] == 231
            assert call_kwargs["license_type"] == "enterprise"
