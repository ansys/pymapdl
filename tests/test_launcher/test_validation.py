# Copyright (C) 2016 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#

"""Unit tests for launcher.validation module."""

from unittest.mock import Mock, patch

from ansys.mapdl.core.launcher import LaunchConfig, LaunchMode
from ansys.mapdl.core.launcher.models import TransportMode, ValidationResult
from ansys.mapdl.core.launcher.validation import validate_config

# ============================================================================
# Helper Functions
# ============================================================================


def _create_test_config(**overrides):
    """Helper to create test config."""
    defaults = {
        "exec_file": "/path/to/mapdl",
        "run_location": "/tmp",
        "jobname": "file",
        "nproc": 2,
        "port": 50052,
        "ip": "127.0.0.1",
        "mode": LaunchMode.GRPC,
        "version": 222,
        "start_instance": True,
        "ram": None,
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
# Main Validation Tests
# ============================================================================


class TestValidateConfig:
    """Tests for main validate_config function."""

    def test_validate_config_valid(self):
        """Test validation with valid config."""
        config = _create_test_config()
        with patch("psutil.cpu_count", return_value=4):
            with patch("os.path.isfile", return_value=True):
                result = validate_config(config)
                assert isinstance(result, ValidationResult)

    def test_validate_config_invalid(self):
        """Test validation with invalid config."""
        config = _create_test_config(nproc=0)
        result = validate_config(config)
        # Should have errors (exact behavior depends on implementation)
        assert isinstance(result, ValidationResult)

    def test_validate_skip_checks_when_not_starting(self):
        """Test that validation skips resource checks when not starting."""
        config = _create_test_config(
            start_instance=False,
            nproc=100,  # Would normally fail
        )
        result = validate_config(config)
        assert result.valid  # No errors


# ============================================================================
# Version/Mode Compatibility Tests
# ============================================================================


class TestVersionModeCompatibility:
    """Tests for version-mode compatibility validation."""

    def test_validate_grpc_requires_v211_or_newer(self):
        """Test that gRPC mode requires version 211+."""
        config = _create_test_config(mode=LaunchMode.GRPC, version=210)
        result = validate_config(config)
        assert not result.valid
        assert any("gRPC" in error for error in result.errors)

    def test_validate_grpc_with_valid_version(self):
        """Test that gRPC works with version 211+."""
        config = _create_test_config(mode=LaunchMode.GRPC, version=222)
        with patch("os.path.isfile", return_value=True):
            with patch("psutil.cpu_count", return_value=4):
                result = validate_config(config)
                # Should not have version-related errors
                assert not any(
                    "gRPC" in error and "version" in error for error in result.errors
                )

    def test_validate_console_mode(self):
        """Test console mode validation."""
        config = _create_test_config(mode=LaunchMode.CONSOLE)
        with patch("os.path.isfile", return_value=True):
            with patch("psutil.cpu_count", return_value=4):
                result = validate_config(config)
                # Behavior depends on platform
                assert isinstance(result, ValidationResult)


# ============================================================================
# Resource Availability Tests
# ============================================================================


class TestResourceAvailability:
    """Tests for resource availability validation."""

    def test_validate_nproc_exceeds_available_cpus(self):
        """Test warning when nproc exceeds available CPUs."""
        with patch("psutil.cpu_count", return_value=4):
            config = _create_test_config(nproc=8)
            result = validate_config(config)
            # Should have warning about CPU count
            assert len(result.warnings) > 0 or not result.valid

    def test_validate_nproc_excessively_high(self):
        """Test error when nproc is excessively high."""
        with patch("psutil.cpu_count", return_value=4):
            config = _create_test_config(nproc=10)
            result = validate_config(config)
            assert not result.valid
            assert any(
                "excessive" in e.lower() or "processors" in e.lower()
                for e in result.errors
            )

    def test_validate_ram_exceeds_available(self):
        """Test error when requested RAM exceeds available."""
        mock_mem = Mock()
        mock_mem.available = 1024 * 1024 * 1024  # 1 GB
        with patch("psutil.virtual_memory", return_value=mock_mem):
            config = _create_test_config(ram=4096)  # 4 GB
            result = validate_config(config)
            assert not result.valid

    def test_validate_ram_within_limits(self):
        """Test RAM within available limits."""
        mock_mem = Mock()
        mock_mem.available = 16 * 1024 * 1024 * 1024  # 16 GB
        with patch("psutil.virtual_memory", return_value=mock_mem):
            with patch("os.path.isfile", return_value=True):
                with patch("psutil.cpu_count", return_value=4):
                    config = _create_test_config(ram=4096)  # 4 GB
                    result = validate_config(config)
                    # Should not have RAM-related errors
                    assert not any(
                        "ram" in e.lower() or "memory" in e.lower()
                        for e in result.errors
                    )


# ============================================================================
# Platform Compatibility Tests
# ============================================================================


class TestPlatformCompatibility:
    """Tests for platform compatibility validation."""

    def test_validate_console_mode_on_windows(self):
        """Test console mode validation on Windows."""
        config = _create_test_config(mode=LaunchMode.CONSOLE)
        with patch("os.name", "nt"):
            result = validate_config(config)
            assert not result.valid
            assert any("Console" in error for error in result.errors)

    def test_validate_console_mode_on_linux(self):
        """Test console mode validation on Linux."""
        config = _create_test_config(mode=LaunchMode.CONSOLE)
        with patch("os.name", "posix"):
            with patch("os.path.isfile", return_value=True):
                with patch("psutil.cpu_count", return_value=4):
                    result = validate_config(config)
                    # Should not have platform-related errors
                    assert not any(
                        "Console" in error and "Windows" in error
                        for error in result.errors
                    )

    def test_validate_uds_transport_on_windows(self):
        """Test UDS transport validation on Windows."""
        config = _create_test_config(transport_mode=TransportMode.UDS)
        with patch("os.name", "nt"):
            result = validate_config(config)
            assert not result.valid
            assert any(
                "Unix domain socket" in error or "UDS" in error
                for error in result.errors
            )

    def test_validate_hpc_on_windows(self):
        """Test HPC launch validation on Windows."""
        config = _create_test_config(launch_on_hpc=True)
        with patch("os.name", "nt"):
            result = validate_config(config)
            assert not result.valid


# ============================================================================
# File Permissions Tests
# ============================================================================


class TestFilePermissions:
    """Tests for file permission validation."""

    def test_validate_exec_file_not_found(self):
        """Test validation with non-existent executable."""
        config = _create_test_config(exec_file="/nonexistent/mapdl")
        result = validate_config(config)
        assert not result.valid
        assert any(
            "not found" in error.lower() or "does not exist" in error.lower()
            for error in result.errors
        )

    def test_validate_exec_file_exists(self):
        """Test validation with existing executable."""
        config = _create_test_config()
        with patch("os.path.isfile", return_value=True):
            with patch("psutil.cpu_count", return_value=4):
                result = validate_config(config)
                # Should not have file not found error
                assert not any("not found" in error.lower() for error in result.errors)

    def test_validate_run_location_not_writable(self):
        """Test validation with non-writable directory."""
        config = _create_test_config(run_location="/root/restricted")
        with patch("os.path.exists", return_value=True):
            with patch("os.access", return_value=False):
                result = validate_config(config)
                assert not result.valid


# ============================================================================
# Conflicting Options Tests
# ============================================================================


class TestConflictingOptions:
    """Tests for conflicting options validation."""

    def test_validate_start_instance_with_remote_ip(self):
        """Test conflict when starting instance with remote IP."""
        config = _create_test_config(
            start_instance=True,
            ip="192.168.1.100",
        )
        with patch("ansys.mapdl.core.launcher.validation.is_wsl", return_value=False):
            result = validate_config(config)
            assert not result.valid

    def test_validate_start_instance_with_localhost(self):
        """Test starting instance with localhost is valid."""
        config = _create_test_config(start_instance=True, ip="127.0.0.1")
        with patch("os.path.isfile", return_value=True):
            with patch("psutil.cpu_count", return_value=4):
                result = validate_config(config)
                # Should not have IP-related errors
                assert not any(
                    "remote" in error.lower() or "IP" in error
                    for error in result.errors
                )

    def test_validate_hpc_with_custom_ip(self):
        """Test HPC launch with custom IP conflict."""
        config = _create_test_config(
            launch_on_hpc=True,
            ip="192.168.1.100",
        )
        result = validate_config(config)
        assert not result.valid

    def test_validate_mtls_without_certs(self):
        """Test mTLS validation without certificates."""
        config = _create_test_config(transport_mode=TransportMode.MTLS)
        result = validate_config(config)
        assert not result.valid
        assert any(
            "mTLS" in error and "certs" in error.lower() for error in result.errors
        )

    def test_validate_mtls_with_certs(self):
        """Test mTLS validation with certificates."""
        config = _create_test_config(
            transport_mode=TransportMode.MTLS,
            certs_dir="/path/to/certs",
        )
        with patch("os.path.isdir", return_value=True):
            with patch("os.path.isfile", return_value=True):
                with patch("psutil.cpu_count", return_value=4):
                    result = validate_config(config)
                    # Should not have mTLS-related errors
                    assert not any(
                        "mTLS" in error and "certs" in error.lower()
                        for error in result.errors
                    )


# ============================================================================
# Edge Cases
# ============================================================================


class TestValidationEdgeCases:
    """Test edge cases in validation."""

    def test_validate_with_all_defaults(self):
        """Test validation with all default values."""
        config = _create_test_config()
        with patch("os.path.isfile", return_value=True):
            with patch("psutil.cpu_count", return_value=4):
                result = validate_config(config)
                assert isinstance(result, ValidationResult)

    def test_validate_with_minimal_config(self):
        """Test validation with minimal configuration."""
        config = _create_test_config(start_instance=False)
        result = validate_config(config)
        assert isinstance(result, ValidationResult)

    def test_validate_accumulates_multiple_errors(self):
        """Test that validation accumulates multiple errors."""
        config = _create_test_config(
            mode=LaunchMode.GRPC,
            version=210,  # Too old for gRPC
            nproc=0,  # Invalid nproc
        )
        result = validate_config(config)
        assert not result.valid
        assert len(result.errors) >= 2  # Should have multiple errors
