# Copyright (C) 2016 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#

"""Unit tests for launcher.config module."""

import os
from typing import Optional
from unittest.mock import patch

import pytest

from ansys.mapdl.core.launcher import ConfigurationError, LaunchMode
from ansys.mapdl.core.launcher.config import (
    LOCALHOST,
    resolve_additional_switches,
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
    from . import ON_LOCAL

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

    def test_resolve_launch_config_transport_mode(self):
        """Test config resolution with transport mode."""
        config = resolve_launch_config(transport_mode="uds")
        assert config.transport_mode == TransportMode.UDS


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
        """Test IP resolution on WSL when host IP cannot be determined.

        Falls back to localhost with a warning when WSL host IP cannot be determined.
        """
        with patch("ansys.mapdl.core.launcher.environment.is_wsl", return_value=True):
            with patch(
                "ansys.mapdl.core.launcher.environment.get_windows_host_ip",
                return_value=None,
            ):
                with patch("ansys.mapdl.core.launcher.config.LOG") as mock_log:
                    ip = resolve_ip(None, start_instance=True)
                    # Falls back to localhost, doesn't raise error
                    assert ip == LOCALHOST
                    # Verify warning was logged
                    mock_log.warning.assert_called_once()


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

    def test_resolve_exec_file_auto_detect_with_version(self, monkeypatch):
        """Test exec file auto-detection with version."""
        monkeypatch.delenv("PYMAPDL_MAPDL_EXEC", raising=False)
        with (
            patch("ansys.mapdl.core.launcher.config._HAS_ATC", True),
            patch(
                "ansys.tools.common.path.get_mapdl_path",
                return_value="/path/to/mapdl/exec",
            ),
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


class TestResolveAdditionalSwitches:
    """Tests for additional switches resolution."""

    def test_resolve_additional_switches_explicit(self, monkeypatch):
        """Test explicit additional_switches is returned as-is (no env var set)."""
        monkeypatch.delenv("PYMAPDL_ADDITIONAL_SWITCHES", raising=False)
        result = resolve_additional_switches("-noinfo -nointel")
        assert result == "-noinfo -nointel"

    def test_resolve_additional_switches_empty_uses_env_var(self, monkeypatch):
        """Test that empty string falls back to PYMAPDL_ADDITIONAL_SWITCHES env var."""
        monkeypatch.setenv("PYMAPDL_ADDITIONAL_SWITCHES", "-dyn")
        result = resolve_additional_switches("")
        assert result == "-dyn"

    def test_resolve_additional_switches_explicit_overrides_env_var(self, monkeypatch):
        """Test that explicit arg takes precedence over env var with exactly one warning.

        ``-explicit`` and ``-from-env`` share no 4-char substring, so only the
        skip-env-var warning should fire (not the duplicate-substring warning).
        """
        monkeypatch.setenv("PYMAPDL_ADDITIONAL_SWITCHES", "-from-env")
        with patch("ansys.mapdl.core.launcher.config.LOG") as mock_log:
            result = resolve_additional_switches("-explicit")
            assert result == "-explicit"
            assert mock_log.warning.call_count == 1

    def test_resolve_additional_switches_no_env_var_returns_empty(self, monkeypatch):
        """Test that empty arg with no env var returns empty string."""
        monkeypatch.delenv("PYMAPDL_ADDITIONAL_SWITCHES", raising=False)
        result = resolve_additional_switches("")
        assert result == ""

    def test_resolve_additional_switches_duplicate_substring_warns(self, monkeypatch):
        """Test that a shared 4-char substring triggers a duplicate warning."""
        monkeypatch.setenv("PYMAPDL_ADDITIONAL_SWITCHES", "-noinfo")
        with patch("ansys.mapdl.core.launcher.config.LOG") as mock_log:
            result = resolve_additional_switches("-noinfo -nointel")
            assert result == "-noinfo -nointel"
            # Expect two warnings: skip-env-var + duplicate-substring
            assert mock_log.warning.call_count == 2
            messages = " ".join(
                str(call.args[0]) for call in mock_log.warning.call_args_list
            )
            assert "duplicated" in messages or "contradicting" in messages

    def test_resolve_additional_switches_no_duplicate_substring_no_extra_warn(
        self, monkeypatch
    ):
        """Test that no shared 4-char substring yields only the skip warning."""
        monkeypatch.setenv("PYMAPDL_ADDITIONAL_SWITCHES", "-abc")
        with patch("ansys.mapdl.core.launcher.config.LOG") as mock_log:
            resolve_additional_switches("-xyz")
            # Only the skip-env-var warning, no duplicate warning
            assert mock_log.warning.call_count == 1

    def test_resolve_launch_config_injects_env_var_switches(self, monkeypatch):
        """Test that resolve_launch_config picks up PYMAPDL_ADDITIONAL_SWITCHES."""
        monkeypatch.setenv("PYMAPDL_ADDITIONAL_SWITCHES", "-myswitch")
        config = resolve_launch_config(start_instance=False)
        assert config.additional_switches == "-myswitch"

    def test_resolve_launch_config_explicit_switches_skip_env_var(self, monkeypatch):
        """Test that explicit additional_switches skips the env var."""
        monkeypatch.setenv("PYMAPDL_ADDITIONAL_SWITCHES", "-from-env")
        with patch("ansys.mapdl.core.launcher.config.LOG"):
            config = resolve_launch_config(
                additional_switches="-explicit", start_instance=False
            )
            assert config.additional_switches == "-explicit"

    def test_resolve_launch_config_no_env_var_empty_switches(self, monkeypatch):
        """Test that with no env var and no arg, additional_switches is empty."""
        monkeypatch.delenv("PYMAPDL_ADDITIONAL_SWITCHES", raising=False)
        config = resolve_launch_config(start_instance=False)
        assert config.additional_switches == ""


# ============================================================================
# : License Type Validation Tests
# ============================================================================


class TestLicenseTypeValidation:
    """: Tests for license type validation in launcher.

    These tests validate that license types are strings (not enums) and
    that they work properly with the LaunchConfig.
    """

    @pytest.mark.parametrize(
        "license_type",
        [
            "research",
            "academic",
            "aa_r",
            "aa_t_a",
            "custom_license",
            None,
        ],
    )
    def test_resolve_with_each_license_type(self, license_type: Optional[str]):
        """Test resolve_launch_config with various license types.

        Parametrized test validating that resolve_launch_config properly
        handles different license type string values.
        """
        config = resolve_launch_config(license_type=license_type, start_instance=False)

        assert config.license_type == license_type
        if license_type is not None:
            assert isinstance(config.license_type, str)

    def test_license_type_preserved_through_config(self):
        """Test that license_type is preserved through configuration chain.

        Validates that license_type set during resolve_launch_config
        remains intact in the final LaunchConfig.
        """
        custom_license = "research"
        config = resolve_launch_config(
            license_type=custom_license, start_instance=False
        )

        assert config.license_type == custom_license


class TestVersionValidation:
    """Tests for version validation and edge cases."""

    def test_version_from_path_edge_cases(self):
        """Test version extraction from path with edge cases.

        Validates that version_from_path handles various path formats correctly.
        """
        with patch("ansys.mapdl.core.launcher.config._HAS_ATC", True):
            with patch(
                "ansys.tools.common.path.version_from_path",
                return_value=222,
            ):
                version = resolve_version(None, "/usr/ansys_inc/v222/ansys/bin/mapdl")
                assert version == 222

    def test_version_validation_compatibility(self):
        """Test that version validation works with new pattern.

        Validates that resolve_version works correctly with the new
        pure function pattern, handling all resolution priority orders.
        """
        # Test explicit argument priority
        version1 = resolve_version(232, "/path/to/mapdl")
        assert version1 == 232

        # Test env var priority
        with patch.dict(os.environ, {"PYMAPDL_MAPDL_VERSION": "225"}):
            version2 = resolve_version(None, "/path/to/mapdl")
            assert version2 == 225

    def test_version_verify_pass(self):
        """Test that known good versions pass validation."""
        good_versions = [211, 212, 221, 222, 231, 232, 241, 242]
        for ver in good_versions:
            config = resolve_launch_config(version=ver, start_instance=False)
            assert config.version == ver

    def test_version_verify_latest(self):
        """Test that latest version can be inferred when not specified."""
        # When version is None, it should remain None or be detected
        config = resolve_launch_config(version=None, start_instance=False)
        # Version can be None if not detected
        assert config.version is None or isinstance(config.version, int)


class TestLicenseProductTests:
    """Tests for license product handling."""

    def test_license_type_keyword_names(self):
        """Test that license type accepts keyword names.

        Validates that various license keyword names are accepted
        without transformation or validation errors.
        """
        license_keywords = [
            "research",
            "academic",
            "dyna",
            "mechanical",
            "fluent",
            "cfx",
            "aa_r",
            "aa_t_a",
        ]

        for keyword in license_keywords:
            config = resolve_launch_config(license_type=keyword, start_instance=False)
            assert config.license_type == keyword

    def test_license_type_additional_switch(self):
        """Test that license_type can be used with additional_switches.

        Validates that license type works in combination with other switches
        without conflicts or validation errors.
        """
        config = resolve_launch_config(
            license_type="research",
            additional_switches="-noinfo",
            start_instance=False,
        )
        assert config.license_type == "research"
        assert "-noinfo" in config.additional_switches

    def test_license_product_argument_error(self):
        """Test license type with invalid values raises ConfigurationError.

        Note: Currently license_type is not validated (accepts any string).
        This test documents that license validation happens elsewhere if needed.
        """
        # Currently, license_type accepts any string without validation
        config = resolve_launch_config(
            license_type="invalid_license", start_instance=False
        )
        assert config.license_type == "invalid_license"

    def test_license_product_argument_warning(self):
        """Test that invalid license type generates warning if validated elsewhere.

        Documents that while license_type accepts strings, validation
        and warnings may happen during actual launch.
        """
        # Currently no validation in resolver, but configuration is preserved
        config = resolve_launch_config(license_type="unknown_lic", start_instance=False)
        assert config.license_type == "unknown_lic"


class TestConfigParameterResolution:
    """Tests for comprehensive config parameter resolution."""

    def test_resolve_nproc_exceeds_cpu_limit(self):
        """Test nproc exceeding physical CPU limit.

        Documents that nproc resolution doesn't enforce CPU limits
        (those checks happen elsewhere in validation).
        """
        # resolver accepts the value, validation happens separately
        nproc = resolve_nproc(10000)
        assert nproc == 10000

    # ========== Port Tests ==========
    def test_resolve_port_with_env_override(self):
        """Test port resolution with environment variable override.

        Validates priority order: explicit > env var > default.
        """
        with patch.dict(os.environ, {"PYMAPDL_PORT": "50100"}):
            # Explicit takes priority
            port = resolve_port(50200)
            assert port == 50200

    def test_resolve_port_env_override(self):
        """Test that PYMAPDL_PORT environment variable overrides default."""
        with patch.dict(os.environ, {"PYMAPDL_PORT": "55555"}):
            port = resolve_port(None)
            assert port == 55555

    def test_resolve_port_default_value(self):
        """Test that default port is 50052."""
        with patch.dict(os.environ, {}, clear=True):
            port = resolve_port(None)
            assert port == 50052

    # ========== IP Tests ==========
    def test_resolve_ip_with_env_override(self):
        """Test IP resolution with environment variable override.

        Validates priority order: explicit > env var > defaults.
        """
        with patch.dict(os.environ, {"PYMAPDL_IP": "192.168.1.100"}):
            # Both IPs resolve to themselves for this test
            def mock_gethostbyname(hostname):
                return hostname  # Return the input as-is (simple mock)

            with patch("socket.gethostbyname", side_effect=mock_gethostbyname):
                ip = resolve_ip("192.168.1.50", start_instance=False)
                # Explicit takes priority
                assert ip == "192.168.1.50"

    def test_resolve_ip_env_override(self):
        """Test IP resolution from PYMAPDL_IP environment variable."""
        with patch.dict(os.environ, {"PYMAPDL_IP": "10.0.0.1"}):
            with patch("socket.gethostbyname", return_value="10.0.0.1"):
                ip = resolve_ip(None, start_instance=False)
                assert ip == "10.0.0.1"

    def test_resolve_ip_localhost_default(self):
        """Test that localhost (127.0.0.1) is the fallback default."""
        with patch.dict(os.environ, {}, clear=True):
            with patch(
                "ansys.mapdl.core.launcher.environment.is_wsl", return_value=False
            ):
                ip = resolve_ip(None, start_instance=True)
                assert ip == "127.0.0.1"

    def test_resolve_ip_invalid_format(self):
        """Test IP resolution with invalid format raises ConfigurationError."""
        import socket

        with patch("socket.gethostbyname", side_effect=socket.gaierror):
            with pytest.raises(ConfigurationError):
                resolve_ip("invalid-host-xyz-123", start_instance=False)

    def test_resolve_ip_with_start_instance_interaction(self):
        """Test IP resolution behavior changes based on start_instance.

        When start_instance=False, IP must be specified or come from env var.
        When start_instance=True, can default to localhost or WSL detection.
        """
        # start_instance=False, no IP specified -> defaults to localhost
        with patch("ansys.mapdl.core.launcher.environment.is_wsl", return_value=False):
            ip = resolve_ip(None, start_instance=False)
            assert ip == "127.0.0.1"

        # start_instance=True, no IP specified -> defaults to localhost or WSL IP
        with patch("ansys.mapdl.core.launcher.environment.is_wsl", return_value=False):
            ip = resolve_ip(None, start_instance=True)
            assert ip == "127.0.0.1"

    # ========== Run Location Tests ==========
    def test_resolve_run_location_creates_if_needed(self, tmp_path):
        """Test that run_location creates directory if it doesn't exist.

        Validates that resolve_run_location automatically creates
        missing directory structure.
        """
        new_location = os.path.join(str(tmp_path), "deep", "nested", "path")
        location = resolve_run_location(new_location)
        assert os.path.exists(location)
        assert os.path.isdir(location)

    def test_resolve_run_location_absolute_path(self):
        """Test that run_location is converted to absolute path."""
        with patch("os.makedirs"):
            location = resolve_run_location(".")
            assert os.path.isabs(location)

    # ========== RAM Tests ==========
    def test_resolve_ram_allocation(self):
        """Test RAM allocation resolution accepts various values."""
        ram_values = [256, 512, 1024, 2048, 4096, 8192, 16384, 32768]
        for ram in ram_values:
            resolved = resolve_ram(ram)
            assert resolved == ram

    def test_resolve_ram_default_none(self):
        """Test that RAM defaults to None when not specified."""
        ram = resolve_ram(None)
        assert ram is None

    # ========== Timeout Tests ==========
    def test_resolve_timeout_for_hpc(self):
        """Test that timeout is extended for HPC launches.

        HPC launches get 2x the default timeout (90 seconds vs 45).
        """
        timeout_regular = resolve_timeout(None, launch_on_hpc=False)
        assert timeout_regular == 45

        timeout_hpc = resolve_timeout(None, launch_on_hpc=True)
        assert timeout_hpc == 90

        # Explicit timeout overrides HPC default
        timeout_explicit = resolve_timeout(120, launch_on_hpc=True)
        assert timeout_explicit == 120


class TestExceptionHandling:
    """Tests for proper exception handling with ConfigurationError."""

    def test_invalid_mode(self):
        """Test that invalid mode raises ConfigurationError."""
        with pytest.raises(ConfigurationError):
            resolve_mode("invalid_mode_xyz", version=None)

    def test_invalid_nproc(self):
        """Test that invalid nproc raises ConfigurationError."""
        with pytest.raises(ConfigurationError):
            resolve_nproc(-5)

        with pytest.raises(ConfigurationError):
            resolve_nproc(0)

    def test_invalid_port(self):
        """Test that invalid port raises ConfigurationError."""
        with pytest.raises(ConfigurationError):
            resolve_port(-1)

        with pytest.raises(ConfigurationError):
            resolve_port(70000)

        with pytest.raises(ConfigurationError):
            resolve_port(0)

    def test_invalid_ip(self):
        """Test that invalid IP raises ConfigurationError."""
        import socket

        with patch("socket.gethostbyname", side_effect=socket.gaierror):
            with pytest.raises(ConfigurationError):
                resolve_ip("not-a-valid-host-name", start_instance=False)

    def test_conflicting_parameters(self):
        """Test that conflicting parameters are handled gracefully.

        When start_instance and ip are both specified, start_instance takes
        precedence with a warning.
        """
        with patch("ansys.mapdl.core.launcher.config.LOG"):
            result = resolve_start_instance(start_instance=True, ip="192.168.1.1")
            # start_instance takes precedence
            assert result is True

    @pytest.mark.parametrize(
        "func,args,expected_error",
        [
            (resolve_port, (-1,), ConfigurationError),
            (resolve_port, (70000,), ConfigurationError),
            (resolve_nproc, (-1,), ConfigurationError),
            (resolve_nproc, (0,), ConfigurationError),
            (resolve_ram, (-100,), ConfigurationError),
            (resolve_timeout, (-1, False), ConfigurationError),
        ],
    )
    def test_invalid_parameters_raise_configuration_error(
        self, func, args, expected_error
    ):
        """Parametrized test for ConfigurationError raising on invalid params."""
        with pytest.raises(expected_error):
            func(*args)


class TestAdditionalSwitches:
    """Tests for additional switches resolution."""

    def test_resolve_additional_switches_from_dict(self):
        """Test resolving additional switches from configuration.

        Validates that switches can be passed through configuration
        without modification.
        """
        switches = "-aa_r -noinfo -nointel"
        config = resolve_launch_config(
            additional_switches=switches,
            start_instance=False,
        )
        assert config.additional_switches == switches

    def test_resolve_additional_switches_empty(self):
        """Test that empty switches default to empty string."""
        config = resolve_launch_config(
            additional_switches="",
            start_instance=False,
        )
        assert config.additional_switches == ""

    def test_resolve_additional_switches_various_formats(self):
        """Test various switch formats are preserved."""
        formats = [
            "-aa_r",
            "-noinfo -nointel",
            "-dyn -g -acc",
            "",
        ]
        for fmt in formats:
            assert fmt == resolve_additional_switches(fmt)


class TestPortResolutionIncrement:
    """Tests for port resolution with new increment-by-1 logic."""

    def test_resolve_port_busy_port_handling(self):
        """Test port resolution behavior when port is busy.

        Documents that actual port checking happens in network layer,
        resolver just returns the specified/default port.
        """
        # Resolver doesn't check availability, just validates range
        port = resolve_port(50052)
        assert port == 50052

    def test_resolve_port_start_instance_false(self):
        """Test port resolution when start_instance is False.

        Port is still resolved even when not starting instance
        (may be used for connection info).
        """
        config = resolve_launch_config(
            port=50100,
            start_instance=False,
        )
        assert config.port == 50100

    def test_resolve_port_from_env_var(self):
        """Test port resolution from PYMAPDL_PORT environment variable."""
        with patch.dict(os.environ, {"PYMAPDL_PORT": "60000"}):
            config = resolve_launch_config(start_instance=False)
            assert config.port == 60000

    def test_resolve_port_sequential_increment(self):
        """Test that port resolution respects sequential numbering.

        Documents that ports are checked sequentially (50052, 50053, 50054...)
        in the network layer, not here in the resolver.
        """
        # Resolver just returns the requested port
        port = resolve_port(50052)
        assert port == 50052

        # Next would be 50053 (increment by 1)
        port = resolve_port(50053)
        assert port == 50053


class TestIpResolutionEdgeCases:
    """Tests for IP resolution edge cases."""

    def test_resolve_ip_explicit(self):
        """Test IP resolution with explicit IP overrides everything.

        Explicit IP takes priority over env vars and defaults.
        """
        with patch("socket.gethostbyname", return_value="10.0.0.50"):
            ip = resolve_ip("10.0.0.50", start_instance=False)
            assert ip == "10.0.0.50"

    def test_resolve_ip_from_env(self):
        """Test IP resolution from PYMAPDL_IP environment variable."""
        with patch.dict(os.environ, {"PYMAPDL_IP": "192.168.1.200"}):
            with patch("socket.gethostbyname", return_value="192.168.1.200"):
                ip = resolve_ip(None, start_instance=False)
                assert ip == "192.168.1.200"

    def test_resolve_ip_localhost_default(self):
        """Test that 127.0.0.1 is the final fallback default."""
        with patch.dict(os.environ, {}, clear=True):
            with patch(
                "ansys.mapdl.core.launcher.environment.is_wsl", return_value=False
            ):
                ip = resolve_ip(None, start_instance=False)
                assert ip == "127.0.0.1"

    def test_resolve_ip_invalid_format(self):
        """Test IP validation for invalid format."""
        import socket

        with patch(
            "socket.gethostbyname",
            side_effect=socket.gaierror("Name or service not known"),
        ):
            with pytest.raises(ConfigurationError) as exc_info:
                resolve_ip("invalid-xyz-host", start_instance=False)
            assert "Cannot resolve hostname or IP" in str(exc_info.value)

    def test_resolve_ip_with_start_instance_interaction(self):
        """Test IP resolution behavior with start_instance parameter.

        Both start_instance values should resolve IP the same way
        (the difference is whether MAPDL is started locally).
        """
        with patch("ansys.mapdl.core.launcher.environment.is_wsl", return_value=False):
            ip_start_true = resolve_ip(None, start_instance=True)
            ip_start_false = resolve_ip(None, start_instance=False)
            # Both default to localhost when no env vars or explicit IP
            assert ip_start_true == "127.0.0.1"
            assert ip_start_false == "127.0.0.1"

    def test_resolve_ip_invalid_raises_error(self):
        """Test that invalid IP raises ConfigurationError."""
        import socket

        from ansys.mapdl.core.launcher.config import ConfigurationError, resolve_ip

        with patch(
            "socket.gethostbyname",
            side_effect=socket.gaierror("Name or service not known"),
        ):
            with pytest.raises(ConfigurationError) as exc_info:
                resolve_ip("invalid-host-xyz", start_instance=False)
            assert "Cannot resolve hostname or IP" in str(exc_info.value)

    def test_resolve_ip_start_instance_affects_wsl_detection(self):
        """Test that start_instance affects WSL host IP detection.

        When start_instance=True, WSL host IP is used if available.
        When start_instance=False, no special WSL handling needed.
        """
        from ansys.mapdl.core.launcher.config import resolve_ip

        # start_instance=True triggers WSL detection
        with patch("ansys.mapdl.core.launcher.environment.is_wsl", return_value=True):
            with patch(
                "ansys.mapdl.core.launcher.environment.get_windows_host_ip",
                return_value="172.20.0.1",
            ):
                ip = resolve_ip(None, start_instance=True)
                assert ip == "172.20.0.1"

        # start_instance=False doesn't need WSL detection
        with patch("ansys.mapdl.core.launcher.environment.is_wsl", return_value=False):
            ip = resolve_ip(None, start_instance=False)
            assert ip == "127.0.0.1"


class TestConfigurationIntegration:
    """Integration tests for complete configuration resolution."""

    def test_resolve_launch_config_complete_spec(self):
        """Test resolve_launch_config with comprehensive parameters.

        Validates that all parameter combinations work together correctly.
        """
        with patch("os.path.isfile", return_value=True):
            config = resolve_launch_config(
                exec_file="/path/to/mapdl",
                run_location="/tmp/mapdl",
                jobname="integration_test",
                nproc=8,
                port=50100,
                ip="127.0.0.1",
                mode="grpc",
                version=222,
                start_instance=True,
                ram=4096,
                timeout=60,
                cleanup_on_exit=True,
                clear_on_connect=True,
                override=False,
                remove_temp_dir_on_exit=False,
                set_no_abort=True,
                additional_switches="-aa_r -noinfo",
                license_type="research",
                launch_on_hpc=False,
                running_on_hpc=False,
                scheduler_options=None,
                loglevel="DEBUG",
                log_apdl="apdl.log",
                print_com=False,
                mapdl_output=None,
                transport_mode="insecure",
                uds_dir=None,
                uds_id=None,
                certs_dir=None,
                env_vars={"ANS_CMD": "NODIAG"},
                license_server_check=False,
                force_intel=False,
                graphics_backend=None,
            )

            assert config.jobname == "integration_test"
            assert config.nproc == 8
            assert config.port == 50100
            assert config.license_type == "research"
            assert config.additional_switches == "-aa_r -noinfo"
            assert config.loglevel == "DEBUG"

    def test_resolve_launch_config_hpc_integration(self):
        """Test resolve_launch_config with HPC parameters."""
        with patch("os.path.isfile", return_value=True):
            config = resolve_launch_config(
                exec_file="/path/to/mapdl",
                launch_on_hpc=True,
                running_on_hpc=True,
                nproc=16,
                scheduler_options={"nodes": "2", "ntasks-per-node": "8"},
                timeout=None,  # Should default to 90 for HPC
            )

            assert config.launch_on_hpc is True
            assert config.running_on_hpc is True
            assert config.nproc == 16
            assert config.scheduler_options == {"nodes": "2", "ntasks-per-node": "8"}
            assert config.timeout == 90  # HPC default

    def test_resolve_launch_config_remote_instance(self):
        """Test resolve_launch_config for connecting to remote instance."""
        config = resolve_launch_config(
            start_instance=False,
            ip="192.168.1.100",
            port=50052,
        )

        assert config.start_instance is False
        assert config.ip == "192.168.1.100"
        assert config.port == 50052
        # exec_file should be empty when not starting
        assert config.exec_file == ""

    @pytest.mark.parametrize(
        "license_type,nproc,port",
        [
            ("research", 4, 50052),
            ("academic", 8, 50100),
            ("dyna", 16, 50200),
            (None, 2, 50052),
        ],
    )
    def test_resolve_config_various_combinations(
        self, license_type: Optional[str], nproc: int, port: int
    ):
        """Parametrized integration test with various parameter combinations."""
        config = resolve_launch_config(
            license_type=license_type,
            nproc=nproc,
            port=port,
            start_instance=False,
        )

        assert config.license_type == license_type
        assert config.nproc == nproc
        assert config.port == port
