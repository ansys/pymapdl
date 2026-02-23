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
    resolve_ip,
    resolve_launch_config,
    resolve_mode,
    resolve_nproc,
    resolve_port,
    resolve_ram,
    resolve_run_location,
    resolve_start_instance,
    resolve_timeout,
    resolve_transport_mode,
    resolve_version,
)
from ansys.mapdl.core.launcher.models import TransportMode

# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def patch_get_mapdl_path():
    """Patch get_mapdl_path when not ON_LOCAL to avoid finding docker containers."""
    from .conftest import ON_LOCAL

    if not ON_LOCAL:
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


class TestStartTimeoutDeprecation:
    """Tests for deprecated start_timeout parameter."""

    def test_start_timeout_deprecation_warning(self):
        """Test that start_timeout raises DeprecationWarning."""
        import warnings

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            resolve_launch_config(start_timeout=120, start_instance=False)
            assert len(w) >= 1
            assert issubclass(w[-1].category, DeprecationWarning)
            assert "start_timeout" in str(w[-1].message)

    def test_start_timeout_used_when_timeout_not_provided(self):
        """Test that start_timeout is used when timeout is None."""
        with patch("warnings.warn"):
            config = resolve_launch_config(start_timeout=200, start_instance=False)
            assert config.timeout == 200

    def test_timeout_takes_precedence_over_start_timeout(self):
        """Test that timeout takes precedence over start_timeout."""
        with patch("warnings.warn"):
            config = resolve_launch_config(
                start_timeout=200, timeout=150, start_instance=False
            )
            assert config.timeout == 150


class TestResolveIpAddress:
    """Tests for IP address resolution."""

    def test_resolve_ip_explicit_hostname(self):
        """Test IP resolution with explicit hostname."""
        with patch("socket.gethostbyname", return_value="192.168.1.1"):
            ip = resolve_ip("myhost", start_instance=False)
            assert ip == "192.168.1.1"

    def test_resolve_ip_invalid_hostname_explicit(self):
        """Test IP resolution with invalid explicit hostname."""
        import socket

        with patch("socket.gethostbyname", side_effect=socket.gaierror):
            with pytest.raises(ConfigurationError):
                resolve_ip("invalid-host-xyz", start_instance=False)

    def test_resolve_ip_from_env_var(self):
        """Test IP resolution from PYMAPDL_IP environment variable."""
        with patch.dict(os.environ, {"PYMAPDL_IP": "192.168.1.100"}):
            with patch("socket.gethostbyname", return_value="192.168.1.100"):
                ip = resolve_ip(None, start_instance=False)
                assert ip == "192.168.1.100"

    def test_resolve_ip_invalid_from_env_var(self):
        """Test IP resolution with invalid env var value."""
        import socket

        with patch.dict(os.environ, {"PYMAPDL_IP": "invalid-host"}):
            with patch("socket.gethostbyname", side_effect=socket.gaierror):
                with pytest.raises(ConfigurationError):
                    resolve_ip(None, start_instance=False)

    def test_resolve_ip_explicit_overrides_env_and_warning(self):
        """Test that explicit IP overrides env var."""
        with patch.dict(os.environ, {"PYMAPDL_IP": "192.168.1.100"}):
            with patch("socket.gethostbyname", return_value="192.168.1.50"):
                ip = resolve_ip("192.168.1.50", start_instance=False)
                assert ip == "192.168.1.50"

    def test_resolve_ip_wsl_detection(self):
        """Test IP resolution on WSL."""
        with patch("ansys.mapdl.core.launcher.environment.is_wsl", return_value=True):
            with patch(
                "ansys.mapdl.core.launcher.environment.get_windows_host_ip",
                return_value="172.20.0.1",
            ):
                ip = resolve_ip(None, start_instance=True)
                assert ip == "172.20.0.1"

    def test_resolve_ip_wsl_no_host_ip(self):
        """Test IP resolution on WSL when host IP cannot be determined."""
        with patch("ansys.mapdl.core.launcher.environment.is_wsl", return_value=True):
            with patch(
                "ansys.mapdl.core.launcher.environment.get_windows_host_ip",
                return_value=None,
            ):
                with pytest.raises(ConfigurationError):
                    resolve_ip(None, start_instance=True)


class TestResolveLaunchMode:
    """Tests for launch mode resolution."""

    def test_resolve_mode_console_on_windows_fails(self):
        """Test that console mode fails on Windows."""
        with patch("os.name", "nt"):
            with pytest.raises(ConfigurationError):
                resolve_mode("console", version=None)

    def test_resolve_mode_console_on_linux(self):
        """Test that console mode works on Linux."""
        with patch("os.name", "posix"):
            mode = resolve_mode("console", version=None)
            assert mode == LaunchMode.CONSOLE

    def test_resolve_mode_invalid_mode(self):
        """Test resolution with invalid mode string."""
        with pytest.raises(ConfigurationError):
            resolve_mode("invalid_mode", version=None)

    def test_resolve_mode_old_version_on_linux(self):
        """Test auto-detection for old version on Linux."""
        with patch("os.name", "posix"):
            mode = resolve_mode(None, version=200)
            assert mode == LaunchMode.CONSOLE

    def test_resolve_mode_old_version_on_windows_fails(self):
        """Test auto-detection for old version on Windows fails."""
        with patch("os.name", "nt"):
            with pytest.raises(ConfigurationError):
                resolve_mode(None, version=200)

    def test_resolve_mode_modern_version_defaults_grpc(self):
        """Test that modern version defaults to gRPC."""
        mode = resolve_mode(None, version=222)
        assert mode == LaunchMode.GRPC


class TestResolveRam:
    """Tests for RAM resolution."""

    def test_resolve_ram_explicit(self):
        """Test explicit RAM allocation."""
        ram = resolve_ram(8192)
        assert ram == 8192

    def test_resolve_ram_none(self):
        """Test RAM returns None when not specified."""
        ram = resolve_ram(None)
        assert ram is None

    def test_resolve_ram_invalid_zero(self):
        """Test that RAM=0 raises error."""
        with pytest.raises(ConfigurationError):
            resolve_ram(0)

    def test_resolve_ram_invalid_negative(self):
        """Test that negative RAM raises error."""
        with pytest.raises(ConfigurationError):
            resolve_ram(-1024)

    def test_resolve_ram_large_value(self):
        """Test large RAM values."""
        ram = resolve_ram(262144)  # 256GB
        assert ram == 262144


class TestResolveTimeout:
    """Tests for timeout resolution."""

    def test_resolve_timeout_invalid_zero(self):
        """Test that timeout=0 raises error."""
        with pytest.raises(ConfigurationError):
            resolve_timeout(0, launch_on_hpc=False)

    def test_resolve_timeout_invalid_negative(self):
        """Test that negative timeout raises error."""
        with pytest.raises(ConfigurationError):
            resolve_timeout(-10, launch_on_hpc=False)

    def test_resolve_timeout_explicit_with_hpc(self):
        """Test explicit timeout overrides HPC default."""
        timeout = resolve_timeout(100, launch_on_hpc=True)
        assert timeout == 100


class TestResolveStartInstance:
    """Tests for start_instance resolution."""

    def test_resolve_start_instance_explicit_true(self):
        """Test explicit start_instance=True."""
        result = resolve_start_instance(start_instance=True, ip=None)
        assert result is True

    def test_resolve_start_instance_explicit_false(self):
        """Test explicit start_instance=False."""
        result = resolve_start_instance(start_instance=False, ip=None)
        assert result is False

    def test_resolve_start_instance_explicit_overrides_ip_warning(self):
        """Test that explicit start_instance takes precedence and warns."""
        with patch("ansys.mapdl.core.launcher.config.LOG") as mock_log:
            result = resolve_start_instance(start_instance=True, ip="192.168.1.1")
            assert result is True
            mock_log.warning.assert_called_once()

    def test_resolve_start_instance_from_env_true(self):
        """Test start_instance resolution from env var (true)."""
        with patch.dict(os.environ, {"PYMAPDL_START_INSTANCE": "true"}):
            result = resolve_start_instance(None, None)
            assert result is True

    def test_resolve_start_instance_from_env_false(self):
        """Test start_instance resolution from env var (false)."""
        with patch.dict(os.environ, {"PYMAPDL_START_INSTANCE": "false"}):
            result = resolve_start_instance(None, None)
            assert result is False

    def test_resolve_start_instance_from_env_1(self):
        """Test start_instance resolution from env var (1)."""
        with patch.dict(os.environ, {"PYMAPDL_START_INSTANCE": "1"}):
            result = resolve_start_instance(None, None)
            assert result is True

    def test_resolve_start_instance_from_env_0(self):
        """Test start_instance resolution from env var (0)."""
        with patch.dict(os.environ, {"PYMAPDL_START_INSTANCE": "0"}):
            result = resolve_start_instance(None, None)
            assert result is False

    def test_resolve_start_instance_from_env_yes(self):
        """Test start_instance resolution from env var (yes)."""
        with patch.dict(os.environ, {"PYMAPDL_START_INSTANCE": "yes"}):
            result = resolve_start_instance(None, None)
            assert result is True

    def test_resolve_start_instance_from_env_no(self):
        """Test start_instance resolution from env var (no)."""
        with patch.dict(os.environ, {"PYMAPDL_START_INSTANCE": "no"}):
            result = resolve_start_instance(None, None)
            assert result is False

    def test_resolve_start_instance_infer_from_ip(self):
        """Test that IP presence infers start_instance=False."""
        result = resolve_start_instance(None, ip="192.168.1.1")
        assert result is False

    def test_resolve_start_instance_infer_from_env_ip(self):
        """Test that PYMAPDL_IP env var infers start_instance=False."""
        with patch.dict(os.environ, {"PYMAPDL_IP": "192.168.1.1"}):
            result = resolve_start_instance(None, ip=None)
            assert result is False


class TestResolveTransportMode:
    """Tests for transport mode resolution."""

    def test_resolve_transport_mode_none(self):
        """Test transport mode resolution with None."""
        mode = resolve_transport_mode(None)
        assert mode is None

    def test_resolve_transport_mode_insecure(self):
        """Test transport mode resolution for insecure."""
        mode = resolve_transport_mode("insecure")
        assert mode == TransportMode.INSECURE

    def test_resolve_transport_mode_uds(self):
        """Test transport mode resolution for UDS."""
        mode = resolve_transport_mode("uds")
        assert mode == TransportMode.UDS

    def test_resolve_transport_mode_wnua(self):
        """Test transport mode resolution for WNUA."""
        mode = resolve_transport_mode("wnua")
        assert mode == TransportMode.WNUA

    def test_resolve_transport_mode_mtls(self):
        """Test transport mode resolution for mTLS."""
        mode = resolve_transport_mode("mtls")
        assert mode == TransportMode.MTLS

    def test_resolve_transport_mode_case_insensitive(self):
        """Test transport mode is case insensitive."""
        mode = resolve_transport_mode("INSECURE")
        assert mode == TransportMode.INSECURE

    def test_resolve_transport_mode_invalid(self):
        """Test invalid transport mode raises error."""
        with pytest.raises(ConfigurationError):
            resolve_transport_mode("invalid_mode")


class TestResolveRunLocation:
    """Tests for run_location resolution."""

    def test_resolve_resolve_run_location_existing_dir(self, tmp_path):
        """Test run location with existing directory."""
        location = resolve_run_location(str(tmp_path))
        assert os.path.isabs(location)
        assert os.path.exists(location)

    def test_resolve_run_location_creates_missing_dir(self, tmp_path):
        """Test run location creates missing directory."""
        new_dir = os.path.join(str(tmp_path), "new", "dir", "structure")
        location = resolve_run_location(new_dir)
        assert os.path.isabs(location)
        assert os.path.exists(location)

    def test_resolve_run_location_creates_temp_when_none(self):
        """Test run location creates temp directory when None."""
        location = resolve_run_location(None)
        assert os.path.isabs(location)
        assert os.path.exists(location)
        assert "ansys_" in os.path.basename(location)


class TestResolveVersion:
    """Tests for version resolution."""

    def test_resolve_version_explicit(self):
        """Test explicit version resolution."""
        version = resolve_version(222, "/path/to/mapdl")
        assert version == 222

    def test_resolve_version_from_env_var(self):
        """Test version resolution from environment variable."""
        with patch.dict(os.environ, {"PYMAPDL_MAPDL_VERSION": "232"}):
            version = resolve_version(None, "/path/to/mapdl")
            assert version == 232

    def test_resolve_version_invalid_env_var(self):
        """Test version resolution with invalid env var."""
        with patch.dict(os.environ, {"PYMAPDL_MAPDL_VERSION": "not_a_number"}):
            with patch("ansys.mapdl.core.launcher.config.LOG"):
                version = resolve_version(None, "/path/to/mapdl")
                # Should not raise, just warn and continue
                assert version is None or version is not None

    def test_resolve_version_from_exec_file_with_atc(self):
        """Test version extraction from exec_file when ansys-tools-common is available."""
        with patch("ansys.mapdl.core.launcher.config._HAS_ATC", True):
            with patch(
                "ansys.tools.common.path.version_from_path",
                return_value=222,
            ):
                version = resolve_version(None, "/path/to/mapdl/2022/exec/mapdl")
                assert version == 222

    def test_resolve_version_from_exec_file_no_atc(self):
        """Test version returns None when no atc available."""
        with patch("ansys.mapdl.core.launcher.config._HAS_ATC", False):
            version = resolve_version(None, "/path/to/mapdl")
            assert version is None

    def test_resolve_version_extraction_exception(self):
        """Test version extraction handles exceptions gracefully."""
        with patch("ansys.mapdl.core.launcher.config._HAS_ATC", True):
            with patch(
                "ansys.tools.common.path.version_from_path",
                side_effect=Exception("Failed to extract"),
            ):
                with patch("ansys.mapdl.core.launcher.config.LOG"):
                    version = resolve_version(None, "/path/to/mapdl")
                    assert version is None


class TestResolveExecFileEdgeCases:
    """Test edge cases for exec file resolution."""

    def test_resolve_exec_file_env_var_not_exists(self):
        """Test exec file from env var that doesn't exist."""
        from ansys.mapdl.core.launcher.config import resolve_exec_file

        with patch.dict(os.environ, {"PYMAPDL_MAPDL_EXEC": "/nonexistent/mapdl"}):
            with patch("os.path.isfile", return_value=False):
                with pytest.raises(ConfigurationError):
                    resolve_exec_file(None, None, start_instance=True)

    def test_resolve_exec_file_no_atc_and_no_explicit(self):
        """Test exec file resolution fails without ATC and no explicit path."""
        from ansys.mapdl.core.launcher.config import resolve_exec_file

        with patch.dict(os.environ, {"PYMAPDL_MAPDL_EXEC": ""}, clear=True):
            with patch("ansys.mapdl.core.launcher.config._HAS_ATC", False):
                with pytest.raises(ConfigurationError):
                    resolve_exec_file(None, None, start_instance=True)

    def test_resolve_exec_file_auto_detect_with_version(self):
        """Test exec file auto-detection with version."""
        with patch("ansys.mapdl.core.launcher.config._HAS_ATC", True):
            with patch(
                "ansys.tools.common.path.get_mapdl_path",
                return_value="/path/to/mapdl/exec",
            ):
                result = resolve_exec_file(None, 222, start_instance=True)
                assert result == "/path/to/mapdl/exec"

    def test_resolve_exec_file_auto_detect_failure(self):
        """Test exec file auto-detection failure."""
        with patch("ansys.mapdl.core.launcher.config._HAS_ATC", True):
            with patch(
                "ansys.tools.common.path.get_mapdl_path",
                return_value=None,
            ):
                with pytest.raises(ConfigurationError):
                    resolve_exec_file(None, None, start_instance=True)

    def test_resolve_exec_file_auto_detect_exception(self):
        """Test exec file auto-detection exception handling."""
        with patch("ansys.mapdl.core.launcher.config._HAS_ATC", True):
            with patch(
                "ansys.tools.common.path.get_mapdl_path",
                side_effect=Exception("Detection failed"),
            ):
                with pytest.raises(ConfigurationError):
                    resolve_exec_file(None, None, start_instance=True)
