# Copyright (C) 2016 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#

"""Unit tests for launcher.errors module."""

import pytest

from ansys.mapdl.core.launcher.errors import ConfigurationError, LaunchError


class TestConfigurationError:
    """Tests for ConfigurationError exception."""

    def test_raise_configuration_error(self):
        """Test raising ConfigurationError."""
        with pytest.raises(ConfigurationError):
            raise ConfigurationError("Test configuration error")

    def test_configuration_error_message(self):
        """Test ConfigurationError message."""
        msg = "Invalid configuration"
        with pytest.raises(ConfigurationError) as exc_info:
            raise ConfigurationError(msg)
        assert msg in str(exc_info.value)

    def test_configuration_error_inheritance(self):
        """Test ConfigurationError inherits from Exception."""
        assert issubclass(ConfigurationError, Exception)


class TestLaunchError:
    """Tests for LaunchError exception."""

    def test_raise_launch_error(self):
        """Test raising LaunchError."""
        with pytest.raises(LaunchError):
            raise LaunchError("Test launch error")

    def test_launch_error_message(self):
        """Test LaunchError message."""
        msg = "Failed to launch MAPDL"
        with pytest.raises(LaunchError) as exc_info:
            raise LaunchError(msg)
        assert msg in str(exc_info.value)

    def test_launch_error_inheritance(self):
        """Test LaunchError inherits from Exception."""
        assert issubclass(LaunchError, Exception)
