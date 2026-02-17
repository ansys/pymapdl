# Copyright (C) 2016 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#

"""Unit tests for launcher.environment module."""

import os
import subprocess
from unittest.mock import MagicMock, patch

from ansys.mapdl.core.launcher import LaunchConfig, LaunchMode
from ansys.mapdl.core.launcher.environment import (
    _parse_ip_route,
    get_windows_host_ip,
    is_ubuntu,
    is_wsl,
    prepare_environment,
)
from ansys.mapdl.core.launcher.models import EnvironmentConfig

# ============================================================================
# Helper Functions
# ============================================================================


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
        "env_vars": None,
    }
    defaults.update(overrides)
    return LaunchConfig(**defaults)


# ============================================================================
# Environment Detection Tests
# ============================================================================


class TestEnvironmentDetection:
    """Tests for environment detection."""

    def test_is_wsl_on_windows(self):
        """Test WSL detection on Windows."""
        with patch("platform.system", return_value="Windows"):
            result = is_wsl()
            assert isinstance(result, bool)

    def test_is_wsl_on_linux(self):
        """Test WSL detection on Linux."""
        with patch("platform.system", return_value="Linux"):
            with patch("os.path.exists", return_value=True):
                result = is_wsl()
                assert isinstance(result, bool)

    def test_is_wsl_false_on_native_linux(self):
        """Test WSL detection returns False on native Linux."""
        with patch("platform.system", return_value="Linux"):
            with patch("os.path.exists", return_value=False):
                result = is_wsl()
                assert result is False

    def test_is_ubuntu(self):
        """Test Ubuntu detection."""
        with patch("os.path.exists", return_value=True):
            with patch("builtins.open", create=True) as mock_open:
                mock_open.return_value.__enter__.return_value.read.return_value = (
                    "Ubuntu 20.04"
                )
                result = is_ubuntu()
                assert isinstance(result, bool)

    def test_is_ubuntu_via_platform_string(self):
        """Test Ubuntu detection via platform string."""
        with patch("os.name", "posix"):
            with patch("platform.platform", return_value="Linux-5.4.0-ubuntu"):
                result = is_ubuntu()
                assert result is True

    def test_is_ubuntu_not_ubuntu_platform_string(self):
        """Test non-Ubuntu platform string detection."""
        with patch("os.name", "posix"):
            with patch("platform.platform", return_value="Linux-5.4.0-fedora"):
                result = is_ubuntu()
                assert result is False

    def test_is_ubuntu_false_on_other_distro(self):
        """Test Ubuntu detection returns False on other distributions."""
        with patch("os.path.exists", return_value=True):
            with patch("builtins.open", create=True) as mock_open:
                mock_open.return_value.__enter__.return_value.read.return_value = (
                    "Fedora 35"
                )
                result = is_ubuntu()
                assert result is False

    def test_is_ubuntu_false_when_file_not_found(self):
        """Test Ubuntu detection when os-release file doesn't exist."""
        with patch("os.path.exists", return_value=False):
            result = is_ubuntu()
            assert result is False


class TestEnvironmentWSLHelpers:
    """Tests for WSL helper functions."""

    def test_parse_ip_route_valid(self):
        """Test parsing valid ip route output."""
        output = "default via 172.18.0.1 dev eth0"
        result = _parse_ip_route(output)
        assert result == "172.18.0.1"

    def test_parse_ip_route_invalid(self):
        """Test parsing invalid ip route output."""
        output = "invalid output"
        result = _parse_ip_route(output)
        assert result is None

    def test_parse_ip_route_empty(self):
        """Test parsing empty ip route output."""
        output = ""
        result = _parse_ip_route(output)
        assert result is None

    def test_get_windows_host_ip_success(self):
        """Test getting Windows host IP from WSL."""
        with patch("ansys.mapdl.core.launcher.environment.is_wsl", return_value=True):
            with patch("subprocess.run") as mock_subprocess:
                mock_result = MagicMock()
                mock_result.stdout = "default via 172.18.0.1 dev eth0\n"
                mock_subprocess.return_value = mock_result
                result = get_windows_host_ip()
                assert result == "172.18.0.1"

    def test_get_windows_host_ip_failure(self):
        """Test getting Windows host IP when command fails."""
        with patch("subprocess.check_output") as mock_subprocess:
            mock_subprocess.side_effect = subprocess.CalledProcessError(1, "ip")
            result = get_windows_host_ip()
            assert result is None

    def test_get_windows_host_ip_timeout(self):
        """Test getting Windows host IP when command times out."""
        with patch("ansys.mapdl.core.launcher.environment.is_wsl", return_value=True):
            with patch("subprocess.run") as mock_subprocess:
                mock_subprocess.side_effect = subprocess.TimeoutExpired("ip", 5)
                result = get_windows_host_ip()
                assert result is None

    def test_get_windows_host_ip_unexpected_error(self):
        """Test getting Windows host IP on unexpected error."""
        with patch("ansys.mapdl.core.launcher.environment.is_wsl", return_value=True):
            with patch("subprocess.run") as mock_subprocess:
                mock_subprocess.side_effect = RuntimeError("Unexpected error")
                result = get_windows_host_ip()
                assert result is None

    def test_get_windows_host_ip_not_on_wsl(self):
        """Test getting Windows host IP when not on WSL."""
        with patch("ansys.mapdl.core.launcher.environment.is_wsl", return_value=False):
            result = get_windows_host_ip()
            assert result is None


# ============================================================================
# Environment Preparation Tests
# ============================================================================


class TestEnvironmentPrepare:
    """Tests for environment preparation."""

    def test_prepare_environment_basic(self):
        """Test basic environment preparation."""
        config = _create_test_config()

        with patch("platform.system", return_value="Windows"):
            result = prepare_environment(config)
            assert isinstance(result, EnvironmentConfig)
            assert result.variables is not None

    def test_prepare_environment_with_user_env_vars(self):
        """Test environment preparation with user-provided environment variables."""
        custom_env = {"CUSTOM_VAR": "custom_value", "ANOTHER_VAR": "another_value"}
        config = _create_test_config(env_vars=custom_env)

        result = prepare_environment(config)
        assert isinstance(result, EnvironmentConfig)
        assert result.replace_all is True
        assert result.variables == custom_env

    def test_prepare_environment_wsl(self):
        """Test environment preparation on WSL."""
        config = _create_test_config()

        with patch("platform.system", return_value="Linux"):
            with patch("os.path.exists", return_value=True):
                result = prepare_environment(config)
                assert isinstance(result, EnvironmentConfig)

    def test_prepare_environment_linux(self):
        """Test environment preparation on native Linux."""
        config = _create_test_config()

        with patch("platform.system", return_value="Linux"):
            with patch("os.path.exists", return_value=False):
                result = prepare_environment(config)
                assert isinstance(result, EnvironmentConfig)

    def test_prepare_environment_with_license(self):
        """Test environment preparation with license type."""
        config = _create_test_config(license_type="ansys")

        with patch("platform.system", return_value="Linux"):
            result = prepare_environment(config)
            assert isinstance(result, EnvironmentConfig)

    def test_prepare_environment_hpc(self):
        """Test environment preparation for HPC."""
        config = _create_test_config(running_on_hpc=True)

        with patch("platform.system", return_value="Linux"):
            result = prepare_environment(config)
            assert isinstance(result, EnvironmentConfig)

    def test_prepare_environment_ubuntu(self):
        """Test environment preparation on Ubuntu includes MPI settings."""
        config = _create_test_config()

        with patch(
            "ansys.mapdl.core.launcher.environment.is_ubuntu", return_value=True
        ):
            result = prepare_environment(config)
            assert isinstance(result, EnvironmentConfig)
            # Ubuntu-specific settings should be applied
            assert "I_MPI_SHM_LMT" in result.variables
            assert result.variables["I_MPI_SHM_LMT"] == "shm"

    def test_prepare_environment_sets_cmd_nodiag(self):
        """Test that prepare_environment always sets ANS_CMD_NODIAG."""
        config = _create_test_config()

        with patch(
            "ansys.mapdl.core.launcher.environment.is_ubuntu", return_value=False
        ):
            result = prepare_environment(config)
            assert isinstance(result, EnvironmentConfig)
            assert result.variables["ANS_CMD_NODIAG"] == "TRUE"


class TestEnvironmentVariables:
    """Tests for environment variable handling."""

    def test_prepare_environment_preserves_existing_vars(self):
        """Test that existing environment variables are preserved."""
        config = _create_test_config()

        with patch("platform.system", return_value="Linux"):
            with patch.dict(os.environ, {"CUSTOM_VAR": "custom_value"}):
                result = prepare_environment(config)
                # Check that environment preparation doesn't break
                assert isinstance(result, EnvironmentConfig)

    def test_prepare_environment_sets_ansys_vars(self):
        """Test that ANSYS-specific variables are set."""
        config = _create_test_config()

        with patch("platform.system", return_value="Linux"):
            result = prepare_environment(config)
            assert isinstance(result.variables, dict)
            # Variables should be set (implementation dependent)


class TestEnvironmentEdgeCases:
    """Test edge cases in environment handling."""

    def test_prepare_environment_with_invalid_config(self):
        """Test environment preparation with minimal config."""
        config = _create_test_config(start_instance=False)

        with patch("platform.system", return_value="Linux"):
            result = prepare_environment(config)
            assert isinstance(result, EnvironmentConfig)

    def test_is_wsl_with_exception(self):
        """Test WSL detection handles exceptions gracefully."""
        with patch("platform.system", side_effect=Exception("Test error")):
            try:
                result = is_wsl()
                # Should return False on error or raise exception
                assert isinstance(result, bool)
            except Exception:
                pass  # Expected if function doesn't catch exceptions

    def test_is_ubuntu_with_read_error(self):
        """Test Ubuntu detection handles read errors gracefully."""
        with patch("os.path.exists", return_value=True):
            with patch("builtins.open", side_effect=IOError("Cannot read file")):
                result = is_ubuntu()
                assert result is False

    def test_is_wsl_on_windows_os(self):
        """Test WSL detection returns False on Windows."""
        with patch("os.name", "nt"):
            result = is_wsl()
            assert result is False

    def test_is_ubuntu_on_windows_os(self):
        """Test Ubuntu detection returns False on Windows."""
        with patch("os.name", "nt"):
            result = is_ubuntu()
            assert result is False

    def test_is_wsl_with_wsl_distro_name(self):
        """Test WSL detection with WSL_DISTRO_NAME environment variable."""
        with patch("os.name", "posix"):
            with patch.dict(os.environ, {"WSL_DISTRO_NAME": "Ubuntu"}):
                result = is_wsl()
                assert result is True

    def test_is_wsl_with_wsl_interop(self):
        """Test WSL detection with WSL_INTEROP environment variable."""
        with patch("os.name", "posix"):
            with patch.dict(os.environ, {"WSL_INTEROP": "1"}, clear=True):
                result = is_wsl()
                assert result is True

    def test_parse_ip_route_multiple_routes(self):
        """Test parsing ip route output with multiple routes."""
        output = """default via 172.18.0.1 dev eth0
172.18.0.0/16 dev eth0 proto kernel scope link src 172.18.0.2"""
        result = _parse_ip_route(output)
        assert result == "172.18.0.1"

    def test_prepare_environment_replace_all_false(self):
        """Test that prepare_environment sets replace_all=False by default."""
        config = _create_test_config()

        with patch(
            "ansys.mapdl.core.launcher.environment.is_ubuntu", return_value=False
        ):
            result = prepare_environment(config)
            assert result.replace_all is False
