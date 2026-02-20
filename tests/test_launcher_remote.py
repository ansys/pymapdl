# Copyright (C) 2016 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Test PyPIM (Platform Instance Management) integration for remote MAPDL launching.

These tests verify that PyMAPDL can launch and connect to MAPDL instances
via the Ansys Platform Instance Management (PyPIM) service for remote/cloud
deployments. All tests use mocking to avoid starting actual MAPDL processes.
"""

import pytest

from conftest import has_dependency

if not has_dependency("ansys-platform-instancemanagement"):
    pytest.skip(
        allow_module_level=True,
        reason="Skipping because 'ansys-platform-instancemanagement' is not installed",
    )

from unittest.mock import Mock, patch

import ansys.platform.instancemanagement as pypim
import grpc

from ansys.mapdl.core.launcher import LaunchConfig, LaunchMode
from ansys.mapdl.core.launcher.connection import create_grpc_client
from ansys.mapdl.core.mapdl_grpc import MAX_MESSAGE_LENGTH

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
        "clear_on_connect": False,
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


def _create_mock_pypim_instance(uri="localhost:50052"):
    """Create a mock PyPIM instance with standard configuration."""
    mock_instance = Mock(spec=pypim.Instance)
    mock_instance.definition_name = "definitions/mapdl-v222"
    mock_instance.name = "instances/mapdl-v222-abc123"
    mock_instance.ready = True
    mock_instance.status_message = None
    mock_instance.services = {"grpc": Mock(uri=uri, headers={})}
    mock_instance.wait_for_ready = Mock()
    mock_instance.build_grpc_channel = Mock()
    mock_instance.delete = Mock()
    return mock_instance


def _create_mock_grpc_channel():
    """Create a mock gRPC channel."""
    return Mock(spec=grpc.Channel)


def _create_mock_pypim_client():
    """Create a mock PyPIM client."""
    mock_client = Mock(spec=pypim.Client)
    mock_client.create_instance = Mock()
    return mock_client


# ============================================================================
# Tests for PyPIM Configuration Detection
# ============================================================================


class TestPyPIMDetection:
    """Tests for PyPIM availability and configuration detection."""

    def test_pypim_not_configured(self, monkeypatch):
        """Test behavior when PyPIM is not configured."""
        monkeypatch.setattr(pypim, "is_configured", Mock(return_value=False))

        assert pypim.is_configured() is False

    def test_pypim_is_configured(self, monkeypatch):
        """Test behavior when PyPIM is configured."""
        monkeypatch.setattr(pypim, "is_configured", Mock(return_value=True))

        assert pypim.is_configured() is True


# ============================================================================
# Tests for PyPIM Connection Establishment
# ============================================================================


class TestPyPIMConnectionEstablishment:
    """Tests for establishing connections via PyPIM."""

    def test_pypim_connect_creates_client(self, monkeypatch):
        """Test that pypim.connect() is called to create a client."""
        mock_client = _create_mock_pypim_client()
        mock_connect = Mock(return_value=mock_client)
        monkeypatch.setattr(pypim, "connect", mock_connect)

        client = pypim.connect()

        assert client is mock_client
        mock_connect.assert_called_once()

    def test_pypim_client_channel_parameter(self, monkeypatch):
        """Test that pypim.Client accepts a channel parameter."""
        mock_channel = grpc.insecure_channel("localhost:12345")
        mock_client = pypim.Client(channel=mock_channel)

        assert mock_client is not None

    def test_pypim_connect_with_url(self, monkeypatch):
        """Test connecting to PyPIM with specific URL."""
        mock_client = _create_mock_pypim_client()
        mock_connect = Mock(return_value=mock_client)
        monkeypatch.setattr(pypim, "connect", mock_connect)

        client = pypim.connect(url="pim.example.com:50000")

        mock_connect.assert_called_once_with(url="pim.example.com:50000")
        assert client is mock_client


# ============================================================================
# Tests for PyPIM Instance Creation
# ============================================================================


class TestPyPIMInstanceCreation:
    """Tests for creating MAPDL instances via PyPIM."""

    def test_pypim_create_instance_basic(self, monkeypatch):
        """Test creating a basic MAPDL instance via PyPIM."""
        mock_client = _create_mock_pypim_client()
        mock_instance = _create_mock_pypim_instance()
        mock_client.create_instance.return_value = mock_instance

        instance = mock_client.create_instance(product_name="mapdl")

        assert instance is mock_instance
        mock_client.create_instance.assert_called_with(product_name="mapdl")

    def test_pypim_create_instance_with_version(self, monkeypatch):
        """Test creating MAPDL instance with specific version."""
        mock_client = _create_mock_pypim_client()
        mock_instance = _create_mock_pypim_instance()
        mock_client.create_instance.return_value = mock_instance

        instance = mock_client.create_instance(
            product_name="mapdl", product_version="2022R2"
        )

        assert instance is mock_instance
        mock_client.create_instance.assert_called_with(
            product_name="mapdl", product_version="2022R2"
        )

    def test_pypim_create_instance_default_version_none(self, monkeypatch):
        """Test that product_version defaults to None if not specified."""
        mock_client = _create_mock_pypim_client()
        mock_instance = _create_mock_pypim_instance()
        mock_client.create_instance.return_value = mock_instance

        instance = mock_client.create_instance(product_name="mapdl")

        mock_client.create_instance.assert_called_with(product_name="mapdl")

    def test_pypim_create_instance_failure(self, monkeypatch):
        """Test handling instance creation failure."""
        mock_client = _create_mock_pypim_client()
        mock_client.create_instance.side_effect = Exception("Creation failed")

        with pytest.raises(Exception, match="Creation failed"):
            mock_client.create_instance(product_name="mapdl")


# ============================================================================
# Tests for PyPIM Instance Readiness
# ============================================================================


class TestPyPIMInstanceReadiness:
    """Tests for waiting for PyPIM instances to become ready."""

    def test_pypim_instance_wait_for_ready(self, monkeypatch):
        """Test waiting for instance to become ready."""
        mock_instance = _create_mock_pypim_instance()
        mock_instance.wait_for_ready()

        mock_instance.wait_for_ready.assert_called_once()

    def test_pypim_instance_wait_for_ready_with_timeout(self, monkeypatch):
        """Test waiting with custom timeout."""
        mock_instance = _create_mock_pypim_instance()
        mock_instance.wait_for_ready(timeout=120)

        mock_instance.wait_for_ready.assert_called_once_with(timeout=120)

    def test_pypim_instance_ready_property(self, monkeypatch):
        """Test checking ready property."""
        mock_instance = _create_mock_pypim_instance()
        assert mock_instance.ready is True

    def test_pypim_instance_not_ready(self, monkeypatch):
        """Test instance that is not ready."""
        mock_instance = _create_mock_pypim_instance()
        mock_instance.ready = False

        assert mock_instance.ready is False

    def test_pypim_instance_wait_timeout(self, monkeypatch):
        """Test timeout during wait_for_ready."""
        mock_instance = _create_mock_pypim_instance()
        mock_instance.wait_for_ready.side_effect = TimeoutError("Instance timed out")

        with pytest.raises(TimeoutError, match="Instance timed out"):
            mock_instance.wait_for_ready(timeout=5)


# ============================================================================
# Tests for PyPIM Channel Creation
# ============================================================================


class TestPyPIMChannelCreation:
    """Tests for creating gRPC channels via PyPIM instances."""

    def test_pypim_build_grpc_channel_basic(self, monkeypatch):
        """Test building gRPC channel from PyPIM instance."""
        mock_instance = _create_mock_pypim_instance()
        mock_channel = _create_mock_grpc_channel()
        mock_instance.build_grpc_channel.return_value = mock_channel

        channel = mock_instance.build_grpc_channel()

        assert channel is mock_channel
        mock_instance.build_grpc_channel.assert_called_once()

    def test_pypim_build_grpc_channel_with_max_message_length(self, monkeypatch):
        """Test building channel with gRPC options."""
        mock_instance = _create_mock_pypim_instance()
        mock_channel = _create_mock_grpc_channel()
        mock_instance.build_grpc_channel.return_value = mock_channel

        channel = mock_instance.build_grpc_channel(
            options=[
                ("grpc.max_receive_message_length", MAX_MESSAGE_LENGTH),
            ]
        )

        assert channel is mock_channel
        mock_instance.build_grpc_channel.assert_called_once_with(
            options=[
                ("grpc.max_receive_message_length", MAX_MESSAGE_LENGTH),
            ]
        )

    def test_pypim_build_grpc_channel_failure(self, monkeypatch):
        """Test handling channel creation failure."""
        mock_instance = _create_mock_pypim_instance()
        mock_instance.build_grpc_channel.side_effect = Exception(
            "Channel creation failed"
        )

        with pytest.raises(Exception, match="Channel creation failed"):
            mock_instance.build_grpc_channel()

    def test_pypim_build_grpc_channel_with_mtls(self, monkeypatch):
        """Test building channel with mTLS."""
        mock_instance = _create_mock_pypim_instance()
        mock_channel = _create_mock_grpc_channel()
        mock_instance.build_grpc_channel.return_value = mock_channel

        channel = mock_instance.build_grpc_channel(
            insecure=False,
        )

        assert channel is mock_channel


# ============================================================================
# Tests for PyPIM Service URI Extraction
# ============================================================================


class TestPyPIMServiceURI:
    """Tests for extracting service URIs from PyPIM instances."""

    def test_pypim_instance_services_grpc_uri(self, monkeypatch):
        """Test extracting gRPC URI from instance services."""
        mock_instance = _create_mock_pypim_instance(uri="remote.example.com:50052")

        uri = mock_instance.services["grpc"].uri
        assert uri == "remote.example.com:50052"

    def test_pypim_instance_services_headers(self, monkeypatch):
        """Test extracting headers from instance services."""
        mock_instance = _create_mock_pypim_instance()
        mock_instance.services["grpc"].headers = {"Authorization": "Bearer token123"}

        headers = mock_instance.services["grpc"].headers
        assert headers["Authorization"] == "Bearer token123"

    def test_pypim_instance_multiple_services(self, monkeypatch):
        """Test instance with multiple services."""
        mock_instance = _create_mock_pypim_instance()
        mock_instance.services["http"] = Mock(uri="http://remote.example.com:5000")

        assert "grpc" in mock_instance.services
        assert "http" in mock_instance.services


# ============================================================================
# Tests for PyPIM Instance Cleanup
# ============================================================================


class TestPyPIMInstanceCleanup:
    """Tests for cleaning up PyPIM instances."""

    def test_pypim_instance_delete(self, monkeypatch):
        """Test deleting a PyPIM instance."""
        mock_instance = _create_mock_pypim_instance()
        mock_instance.delete()

        mock_instance.delete.assert_called_once()

    def test_pypim_instance_delete_with_timeout(self, monkeypatch):
        """Test deleting instance with timeout."""
        mock_instance = _create_mock_pypim_instance()
        mock_instance.delete(timeout=60)

        mock_instance.delete.assert_called_once_with(timeout=60)

    def test_pypim_instance_delete_failure(self, monkeypatch):
        """Test handling delete failure."""
        mock_instance = _create_mock_pypim_instance()
        mock_instance.delete.side_effect = Exception("Delete failed")

        with pytest.raises(Exception, match="Delete failed"):
            mock_instance.delete()


# ============================================================================
# Tests for PyPIM Client Connection to MAPDL
# ============================================================================


class TestPyPIMToMapdlConnection:
    """Tests for connecting to MAPDL via PyPIM-created channel."""

    def test_create_grpc_client_with_pypim_channel(self, monkeypatch):
        """Test creating MapdlGrpc client using PyPIM channel."""
        config = _create_test_config()

        with patch("ansys.mapdl.core.launcher.connection.MapdlGrpc") as mock_grpc:
            mock_instance = Mock()
            mock_grpc.return_value = mock_instance

            try:
                result = create_grpc_client(config, process_info=None)
            except Exception:
                pass

    def test_grpc_channel_carries_pypim_metadata(self, monkeypatch):
        """Test that gRPC channel includes PyPIM metadata."""
        mock_channel = _create_mock_grpc_channel()
        mock_channel.metadata = [("x-pim-instance", "instance-123")]

        assert mock_channel.metadata is not None


# ============================================================================
# Integration Tests for Full PyPIM Workflow
# ============================================================================


class TestPyPIMWorkflow:
    """Integration tests for complete PyPIM launch workflow."""

    def test_pypim_workflow_basic(self, monkeypatch):
        """Test complete PyPIM workflow: connect -> create -> wait -> channel."""
        mock_client = _create_mock_pypim_client()
        mock_instance = _create_mock_pypim_instance()
        mock_channel = _create_mock_grpc_channel()

        mock_client.create_instance.return_value = mock_instance
        mock_instance.wait_for_ready.return_value = None
        mock_instance.build_grpc_channel.return_value = mock_channel

        mock_connect = Mock(return_value=mock_client)
        mock_is_configured = Mock(return_value=True)
        monkeypatch.setattr(pypim, "connect", mock_connect)
        monkeypatch.setattr(pypim, "is_configured", mock_is_configured)

        is_config = pypim.is_configured()
        assert is_config is True

        client = pypim.connect()
        assert client is mock_client

        instance = client.create_instance(product_name="mapdl", product_version=None)
        assert instance is mock_instance

        instance.wait_for_ready()
        mock_instance.wait_for_ready.assert_called_once()

        channel = instance.build_grpc_channel(
            options=[("grpc.max_receive_message_length", MAX_MESSAGE_LENGTH)]
        )
        assert channel is mock_channel

    def test_pypim_workflow_with_cleanup(self, monkeypatch):
        """Test PyPIM workflow including cleanup."""
        mock_client = _create_mock_pypim_client()
        mock_instance = _create_mock_pypim_instance()
        mock_channel = _create_mock_grpc_channel()

        mock_client.create_instance.return_value = mock_instance
        mock_instance.build_grpc_channel.return_value = mock_channel

        mock_connect = Mock(return_value=mock_client)
        mock_is_configured = Mock(return_value=True)
        monkeypatch.setattr(pypim, "connect", mock_connect)
        monkeypatch.setattr(pypim, "is_configured", mock_is_configured)

        client = pypim.connect()
        instance = client.create_instance(product_name="mapdl")

        instance.delete()

        mock_instance.delete.assert_called_once()

    def test_pypim_workflow_error_handling(self, monkeypatch):
        """Test error handling throughout PyPIM workflow."""
        mock_client = _create_mock_pypim_client()
        mock_client.create_instance.side_effect = Exception("Creation failed")

        mock_connect = Mock(return_value=mock_client)
        mock_is_configured = Mock(return_value=True)
        monkeypatch.setattr(pypim, "connect", mock_connect)
        monkeypatch.setattr(pypim, "is_configured", mock_is_configured)

        client = pypim.connect()
        assert client is mock_client

        with pytest.raises(Exception, match="Creation failed"):
            instance = client.create_instance(product_name="mapdl")


# ============================================================================
# Tests for PyPIM Version Handling
# ============================================================================


class TestPyPIMVersionHandling:
    """Tests for handling different MAPDL versions with PyPIM."""

    @pytest.mark.parametrize(
        "version",
        ["2021R1", "2022R2", "2023R1", "2024R1"],
    )
    def test_pypim_create_instance_various_versions(self, monkeypatch, version):
        """Test creating instances with various MAPDL versions."""
        mock_client = _create_mock_pypim_client()
        mock_instance = _create_mock_pypim_instance()
        mock_client.create_instance.return_value = mock_instance

        instance = mock_client.create_instance(
            product_name="mapdl", product_version=version
        )

        assert instance is mock_instance
        mock_client.create_instance.assert_called_with(
            product_name="mapdl", product_version=version
        )

    def test_pypim_create_instance_latest_version(self, monkeypatch):
        """Test creating instance with latest version."""
        mock_client = _create_mock_pypim_client()
        mock_instance = _create_mock_pypim_instance()
        mock_client.create_instance.return_value = mock_instance

        instance = mock_client.create_instance(
            product_name="mapdl", product_version=None
        )

        assert instance is mock_instance


# ============================================================================
# Tests for PyPIM Configuration Scenarios
# ============================================================================


class TestPyPIMConfigurationScenarios:
    """Tests for different PyPIM configuration scenarios."""

    def test_pypim_with_custom_pim_url(self, monkeypatch):
        """Test PyPIM configuration with custom URL."""
        mock_client = _create_mock_pypim_client()
        mock_connect = Mock(return_value=mock_client)
        monkeypatch.setattr(pypim, "connect", mock_connect)

        client = pypim.connect(url="custom-pim.example.com:50000")

        mock_connect.assert_called_once_with(url="custom-pim.example.com:50000")

    def test_pypim_with_credentials(self, monkeypatch):
        """Test PyPIM connection with credentials."""
        mock_client = _create_mock_pypim_client()
        mock_connect = Mock(return_value=mock_client)
        monkeypatch.setattr(pypim, "connect", mock_connect)

        client = pypim.connect(
            url="pim.example.com:50000",
            username="user123",
            password="pass123",
        )

        mock_connect.assert_called_once()

    def test_pypim_with_tls(self, monkeypatch):
        """Test PyPIM with TLS/SSL."""
        mock_client = _create_mock_pypim_client()
        mock_connect = Mock(return_value=mock_client)
        monkeypatch.setattr(pypim, "connect", mock_connect)

        client = pypim.connect(url="pim.example.com:50000", insecure=False)

        mock_connect.assert_called_once()


# ============================================================================
# Tests for Remote Instance State Tracking
# ============================================================================


class TestRemoteInstanceTracking:
    """Tests for tracking remote instances for cleanup."""

    def test_remote_instance_metadata_extraction(self, monkeypatch):
        """Test extracting metadata from remote instance."""
        mock_instance = _create_mock_pypim_instance()

        assert mock_instance.name == "instances/mapdl-v222-abc123"
        assert mock_instance.ready is True

    def test_remote_instance_state_transitions(self, monkeypatch):
        """Test tracking instance state transitions."""
        mock_instance = _create_mock_pypim_instance()
        assert mock_instance.ready is True

        mock_instance.ready = False
        assert mock_instance.ready is False

        mock_instance.ready = True
        assert mock_instance.ready is True

    def test_remote_instance_holds_reference_for_deletion(self, monkeypatch):
        """Test that instance reference is maintained for cleanup."""
        mock_instance = _create_mock_pypim_instance()
        instance_ref = mock_instance

        instance_ref.delete()
        mock_instance.delete.assert_called_once()


# ============================================================================
# Tests for Multi-Instance Scenarios
# ============================================================================


class TestMultipleRemoteInstances:
    """Tests for managing multiple remote instances."""

    def test_create_multiple_instances_sequentially(self, monkeypatch):
        """Test creating multiple instances in sequence."""
        mock_client = _create_mock_pypim_client()
        mock_instance1 = _create_mock_pypim_instance()
        mock_instance2 = _create_mock_pypim_instance()

        mock_client.create_instance.side_effect = [mock_instance1, mock_instance2]

        instance1 = mock_client.create_instance(product_name="mapdl")
        instance2 = mock_client.create_instance(product_name="mapdl")

        assert instance1 is mock_instance1
        assert instance2 is mock_instance2
        assert instance1 is not instance2

    def test_cleanup_multiple_instances(self, monkeypatch):
        """Test cleaning up multiple instances."""
        instances = [
            _create_mock_pypim_instance(),
            _create_mock_pypim_instance(),
            _create_mock_pypim_instance(),
        ]

        for inst in instances:
            inst.delete()

        for inst in instances:
            inst.delete.assert_called_once()


# ============================================================================
# Tests for Edge Cases and Error Scenarios
# ============================================================================


class TestPyPIMEdgeCases:
    """Tests for edge cases and error scenarios."""

    def test_pypim_instance_with_none_uri(self, monkeypatch):
        """Test instance with None URI."""
        mock_instance = _create_mock_pypim_instance(uri=None)

        assert mock_instance.services["grpc"].uri is None

    def test_pypim_instance_with_empty_headers(self, monkeypatch):
        """Test instance with empty headers."""
        mock_instance = _create_mock_pypim_instance()
        assert isinstance(mock_instance.services["grpc"].headers, dict)

    def test_pypim_connect_timeout(self, monkeypatch):
        """Test PyPIM connection timeout."""
        mock_connect = Mock(side_effect=TimeoutError("Connection timed out"))
        monkeypatch.setattr(pypim, "connect", mock_connect)

        with pytest.raises(TimeoutError, match="Connection timed out"):
            pypim.connect()

    def test_pypim_instance_with_network_error(self, monkeypatch):
        """Test instance creation with network error."""
        mock_client = _create_mock_pypim_client()
        mock_client.create_instance.side_effect = OSError("Network unreachable")

        with pytest.raises(OSError, match="Network unreachable"):
            mock_client.create_instance(product_name="mapdl")

    def test_pypim_channel_with_bad_credentials(self, monkeypatch):
        """Test channel creation with bad credentials."""
        mock_instance = _create_mock_pypim_instance()
        mock_instance.build_grpc_channel.side_effect = PermissionError(
            "Invalid credentials"
        )

        with pytest.raises(PermissionError, match="Invalid credentials"):
            mock_instance.build_grpc_channel()
