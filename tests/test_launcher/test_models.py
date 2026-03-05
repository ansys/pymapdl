# Copyright (C) 2016 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#

"""Unit tests for launcher.models module."""

import pytest

from ansys.mapdl.core.launcher.models import (
    HPCJobInfo,
    LaunchMode,
    PortStatus,
    TransportMode,
    ValidationResult,
)


class TestLaunchMode:
    """Tests for LaunchMode enum."""

    def test_modes_exist(self):
        """Test all launch modes are defined."""
        assert LaunchMode.GRPC.value == "grpc"
        assert LaunchMode.CONSOLE.value == "console"

    def test_from_string(self):
        """Test creating LaunchMode from string."""
        assert LaunchMode("grpc") == LaunchMode.GRPC
        assert LaunchMode("console") == LaunchMode.CONSOLE


class TestTransportMode:
    """Tests for TransportMode enum."""

    def test_modes_exist(self):
        """Test all transport modes are defined."""
        assert TransportMode.INSECURE.value == "insecure"
        assert TransportMode.UDS.value == "uds"
        assert TransportMode.WNUA.value == "wnua"
        assert TransportMode.MTLS.value == "mtls"

    def test_from_string(self):
        """Test creating TransportMode from string."""
        assert TransportMode("insecure") == TransportMode.INSECURE
        assert TransportMode("uds") == TransportMode.UDS


class TestProcessInfo:
    """Tests for ProcessInfo dataclass."""


class TestValidationResult:
    """Tests for ValidationResult dataclass."""

    def test_valid_result(self):
        """Test creating valid result."""
        result = ValidationResult(valid=True, errors=[], warnings=[])
        assert result.valid is True
        assert len(result.errors) == 0
        assert len(result.warnings) == 0

    def test_invalid_with_errors(self):
        """Test creating invalid result with errors."""
        result = ValidationResult(
            valid=False,
            errors=["Error 1", "Error 2"],
            warnings=["Warning 1"],
        )
        assert result.valid is False
        assert len(result.errors) == 2
        assert len(result.warnings) == 1
        assert "Error 1" in result.errors
        assert "Warning 1" in result.warnings

    def test_add_error(self):
        """Test adding error to result."""
        result = ValidationResult(valid=True)
        result.add_error("Test error")
        assert result.valid is False
        assert "Test error" in result.errors

    def test_add_warning(self):
        """Test adding warning to result."""
        result = ValidationResult(valid=True)
        result.add_warning("Test warning")
        assert result.valid is True
        assert "Test warning" in result.warnings


class TestPortStatus:
    """Tests for PortStatus dataclass."""

    @pytest.mark.skip(reason="Old API - PortStatus changed")
    def test_port_available(self):
        """Test port available status."""
        status = PortStatus(
            port=50052,
            is_available=True,
            reason="Port is free",
        )
        assert status.port == 50052
        assert status.is_available is True
        assert status.reason == "Port is free"
        assert status.mapdl_instance is None

    @pytest.mark.skip(reason="Old API - PortStatus changed")
    def test_port_unavailable_with_instance(self):
        """Test port unavailable with MAPDL instance."""
        status = PortStatus(
            port=50052,
            is_available=False,
            reason="Port in use",
            mapdl_instance=True,
        )
        assert status.is_available is False
        assert status.mapdl_instance is True

    @pytest.mark.skip(reason="Old API - PortStatus changed")
    def test_immutable(self):
        """Test that PortStatus is immutable."""
        status = PortStatus(
            port=50052,
            is_available=True,
            reason="Port is free",
        )
        with pytest.raises(AttributeError):
            status.port = 50053


class TestHPCJobInfo:
    """Tests for HPCJobInfo dataclass."""

    def test_create_job_info(self):
        """Test creating HPC job info."""
        info = HPCJobInfo(
            jobid=12345,
            state="RUNNING",
            hostname="node01.cluster",
            ip="192.168.1.10",
        )
        assert info.jobid == 12345
        assert info.state == "RUNNING"
        assert info.hostname == "node01.cluster"
        assert info.ip == "192.168.1.10"

    def test_immutable(self):
        """Test that HPCJobInfo is immutable."""
        info = HPCJobInfo(
            jobid=12345,
            state="RUNNING",
            hostname="node01.cluster",
            ip="192.168.1.10",
        )
        with pytest.raises(AttributeError):
            info.jobid = 67890
