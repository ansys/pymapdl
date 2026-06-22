# Copyright (C) 2016 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
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
