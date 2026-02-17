# Copyright (C) 2016 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#

"""Unit tests for launcher.config module."""

import os
from unittest.mock import patch

import pytest

from ansys.mapdl.core.launcher import ConfigurationError, LaunchConfig, LaunchMode
from ansys.mapdl.core.launcher.config import (
    resolve_exec_file,
    resolve_launch_config,
    resolve_nproc,
    resolve_port,
    resolve_timeout,
)
from ansys.mapdl.core.launcher.models import TransportMode

# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def patch_get_mapdl_path():
    """Patch get_mapdl_path when not ON_LOCAL to avoid finding docker containers."""
    if not os.getenv("ON_LOCAL"):
        with patch("ansys.tools.common.path.get_mapdl_path") as mock_get_mapdl:
            mock_get_mapdl.return_value = "/mock/path/to/mapdl"
            # Also patch os.path.isfile for the mock path
            original_isfile = os.path.isfile

            def mock_isfile(path):
                if path == "/mock/path/to/mapdl":
                    return True
                return original_isfile(path)

            with patch("os.path.isfile", side_effect=mock_isfile):
                yield mock_get_mapdl
    else:
        yield None


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
    }
    defaults.update(overrides)
    return LaunchConfig(**defaults)


# ============================================================================
# Config Resolution Tests
# ============================================================================


class TestConfigResolveExecFile:
    """Tests for resolve_exec_file."""

    def test_resolve_exec_file_not_starting_instance(self):
        """Test exec_file when not starting instance."""
        exec_file = resolve_exec_file(None, None, start_instance=False)
        assert exec_file == ""

    def test_resolve_exec_file_with_explicit_path(self):
        """Test resolve_exec_file with explicit path."""
        test_path = "C:\\test\\path\\to\\mapdl"
        with patch("os.path.isfile", return_value=True):
            result = resolve_exec_file(test_path, None, start_instance=True)
            assert result is not None

    def test_resolve_exec_file_from_env_var(self):
        """Test exec_file from PYMAPDL_MAPDL_EXEC env var."""
        env_path = "/env/path/to/mapdl"
        with patch.dict(os.environ, {"PYMAPDL_MAPDL_EXEC": env_path}):
            with patch("os.path.isfile", return_value=True):
                result = resolve_exec_file(None, None, start_instance=True)
                assert result is not None

    def test_resolve_exec_file_not_found(self):
        """Test resolve_exec_file when file not found."""
        with patch("os.path.isfile", return_value=False):
            with pytest.raises(ConfigurationError):
                resolve_exec_file("/nonexistent/mapdl", None, start_instance=True)

    def test_exec_file_with_spaces(self):
        """Test exec file path with spaces."""
        exec_file = "/Program Files/ANSYS Inc/v222/bin/mapdl.exe"
        with patch("os.path.isfile", return_value=True):
            result = resolve_exec_file(exec_file, None, start_instance=True)
            assert "mapdl" in result.lower()

    def test_exec_file_with_special_chars(self):
        """Test exec file path with special characters."""
        exec_file = "/path/to/mapdl-v222_test.exe"
        with patch("os.path.isfile", return_value=True):
            result = resolve_exec_file(exec_file, None, start_instance=True)
            assert result is not None


class TestConfigPort:
    """Tests for port resolution."""

    def test_resolve_port_explicit(self):
        """Test port resolution with explicit value."""
        port = resolve_port(50100)
        assert port == 50100

    def test_resolve_port_from_env_var(self):
        """Test port resolution from environment variable."""
        with patch.dict(os.environ, {"PYMAPDL_PORT": "50100"}):
            port = resolve_port(None)
            assert port == 50100

    def test_resolve_port_invalid_type(self):
        """Test port resolution with invalid type."""
        with pytest.raises((ConfigurationError, TypeError, ValueError)):
            resolve_port("invalid")

    def test_resolve_port_invalid(self):
        """Test that invalid port raises error."""
        with pytest.raises((ConfigurationError, ValueError)):
            resolve_port(70000)

    def test_resolve_port_negative(self):
        """Test that negative port raises error."""
        with pytest.raises((ConfigurationError, ValueError)):
            resolve_port(-1)

    def test_resolve_port_zero_value(self):
        """Test port resolution rejects zero."""
        with pytest.raises((ConfigurationError, ValueError)):
            resolve_port(0)

    def test_resolve_port_default(self):
        """Test port resolution with default."""
        with patch.dict(os.environ, {}, clear=True):
            port = resolve_port(None)
            assert port is not None and port > 0


class TestConfigNproc:
    """Tests for nproc resolution."""

    def test_resolve_nproc_explicit(self):
        """Test nproc with explicit value."""
        nproc = resolve_nproc(8)
        assert nproc == 8

    def test_resolve_nproc_from_env_var(self):
        """Test nproc from environment variable."""
        with patch.dict(os.environ, {"PYMAPDL_NPROC": "16"}):
            nproc = resolve_nproc(None)
            assert nproc == 16

    def test_resolve_nproc_default(self):
        """Test nproc default value."""
        with patch.dict(os.environ, {}, clear=True):
            nproc = resolve_nproc(None)
            assert nproc is not None and nproc > 0

    def test_resolve_nproc_zero_invalid(self):
        """Test that nproc=0 raises error."""
        with pytest.raises((ConfigurationError, ValueError)):
            resolve_nproc(0)

    def test_resolve_nproc_negative_invalid(self):
        """Test that negative nproc raises error."""
        with pytest.raises((ConfigurationError, ValueError)):
            resolve_nproc(-1)

    def test_nproc_single_processor(self):
        """Test nproc with single processor."""
        nproc = resolve_nproc(1)
        assert nproc == 1

    def test_nproc_large_value(self):
        """Test nproc with large value (many cores)."""
        nproc = resolve_nproc(512)
        assert nproc == 512


class TestConfigTimeout:
    """Tests for timeout resolution."""

    def test_resolve_timeout_default(self):
        """Test timeout default value."""
        timeout = resolve_timeout(None, launch_on_hpc=False)
        assert timeout == 45

    def test_resolve_timeout_hpc_extended(self):
        """Test timeout is extended for HPC."""
        timeout = resolve_timeout(None, launch_on_hpc=True)
        assert timeout == 90  # Double the default for HPC

    def test_resolve_timeout_explicit(self):
        """Test explicit timeout override."""
        timeout = resolve_timeout(120, launch_on_hpc=False)
        assert timeout == 120


class TestConfigResolution:
    """Tests for complete configuration resolution."""

    @pytest.fixture(autouse=True)
    def _patch_get_mapdl_path_auto(self, patch_get_mapdl_path):
        """Auto-apply get_mapdl_path patch to all tests in this class."""
        pass

    def test_resolve_launch_config_all_specified(self):
        """Test resolve_launch_config with all parameters specified."""
        with patch("os.path.isfile", return_value=True):
            config = resolve_launch_config(
                exec_file="/path/to/mapdl",
                run_location="/tmp",
                jobname="test",
                nproc=8,
                port=50100,
                ip="192.168.1.1",
                mode="grpc",
                version=232,
                start_instance=True,
                ram=8192,
                timeout=60,
            )
            assert config.nproc == 8
            assert config.port == 50100
            assert config.version == 232
            assert config.ram == 8192
            assert config.timeout == 60

    def test_resolve_launch_config_with_hpc(self):
        """Test resolve_launch_config with HPC options."""
        with patch("os.path.isfile", return_value=True):
            config = resolve_launch_config(
                exec_file="/path/to/mapdl",
                launch_on_hpc=True,
                running_on_hpc=True,
                scheduler_options={"nodes": "2", "ntasks-per-node": "4"},
            )
            assert config.launch_on_hpc is True
            assert config.running_on_hpc is True
            assert config.scheduler_options == {"nodes": "2", "ntasks-per-node": "4"}

    def test_resolve_launch_config_env_vars_fallback(self):
        """Test resolve_launch_config uses env vars as fallback."""
        with patch.dict(
            os.environ,
            {
                "PYMAPDL_PORT": "50200",
                "PYMAPDL_NPROC": "16",
            },
        ):
            with patch("os.path.isfile", return_value=True):
                config = resolve_launch_config(exec_file="/path/to/mapdl")
                assert config.port == 50200
                assert config.nproc == 16

    def test_resolve_launch_config_with_version(self):
        """Test config resolution with version."""
        with patch("os.path.isfile", return_value=True):
            config = resolve_launch_config(version=222, start_instance=False)
            assert config.version == 222

    def test_resolve_launch_config_with_ram(self):
        """Test config resolution with RAM."""
        config = resolve_launch_config(ram=4096)
        assert config.ram == 4096

    def test_resolve_launch_config_with_jobname(self):
        """Test config resolution with custom jobname."""
        config = resolve_launch_config(jobname="myfile")
        assert config.jobname == "myfile"

    def test_resolve_launch_config_with_timeout(self):
        """Test config resolution with timeout."""
        config = resolve_launch_config(timeout=120)
        assert config.timeout == 120

    def test_resolve_launch_config_with_license_type(self):
        """Test config resolution with license type."""
        config = resolve_launch_config(license_type="dyna")
        assert config.license_type == "dyna"

    def test_resolve_launch_config_with_custom_switches(self):
        """Test config resolution with additional switches."""
        config = resolve_launch_config(additional_switches="-noinfo -nointel")
        assert "-noinfo" in config.additional_switches

    def test_resolve_launch_config_transport_mode(self):
        """Test config resolution with transport mode."""
        config = resolve_launch_config(transport_mode="uds")
        assert config.transport_mode == TransportMode.UDS

    def test_resolve_launch_config_uds_settings(self):
        """Test config resolution with UDS settings."""
        config = resolve_launch_config(
            transport_mode="uds",
            uds_dir="/tmp/mapdl",
            uds_id="mapdl-1",
        )
        assert config.uds_dir == "/tmp/mapdl"
        assert config.uds_id == "mapdl-1"

    def test_resolve_launch_config_mtls_with_certs(self):
        """Test config resolution with mTLS and certificates."""
        config = resolve_launch_config(
            transport_mode="mtls",
            certs_dir="/path/to/certs",
        )
        assert config.transport_mode == TransportMode.MTLS
        assert config.certs_dir == "/path/to/certs"

    def test_resolve_launch_config_logging_settings(self):
        """Test config resolution with logging settings."""
        config = resolve_launch_config(
            loglevel="DEBUG",
            log_apdl="custom.log",
            print_com=True,
        )
        assert config.loglevel == "DEBUG"
        assert config.log_apdl == "custom.log"
        assert config.print_com is True

    def test_resolve_launch_config_cleanup_flags(self):
        """Test config resolution with cleanup flags."""
        config = resolve_launch_config(
            cleanup_on_exit=False,
            remove_temp_dir_on_exit=True,
        )
        assert config.cleanup_on_exit is False
        assert config.remove_temp_dir_on_exit is True

    def test_jobname_max_length(self):
        """Test jobname with maximum length."""
        long_jobname = "a" * 32  # MAPDL job name limit
        config = resolve_launch_config(jobname=long_jobname)
        assert config.jobname == long_jobname


class TestConfigEdgeCases:
    """Test edge cases in configuration."""

    def test_resolve_port_invalid_env_var(self):
        """Test port resolution with invalid env var."""
        with patch.dict(os.environ, {"PYMAPDL_PORT": "not_a_number"}):
            with pytest.raises((ConfigurationError, ValueError)):
                resolve_port(None)

    def test_resolve_nproc_invalid_env_var(self):
        """Test nproc resolution with invalid env var."""
        with patch.dict(os.environ, {"PYMAPDL_NPROC": "invalid"}):
            with pytest.raises((ConfigurationError, ValueError)):
                resolve_nproc(None)
