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

"""Environment detection and configuration.

Functions for detecting platform, setting up environment variables,
and configuring platform-specific settings.
"""

import os
import platform
import subprocess  # nosec B404
from typing import Optional

from ansys.mapdl.core import LOG

from .models import EnvironmentConfig, LaunchConfig


def is_wsl() -> bool:
    """Detect if running on Windows Subsystem for Linux.

    Returns:
        True if running on WSL

    Examples:
        >>> is_wsl()
        False
    """
    if os.name != "posix":
        return False

    # Check WSL-specific environment variables
    return bool(os.environ.get("WSL_DISTRO_NAME") or os.environ.get("WSL_INTEROP"))


def is_ubuntu() -> bool:
    """Detect if running on Ubuntu.

    Returns:
        True if running on Ubuntu

    Examples:
        >>> is_ubuntu()
        False
    """
    if os.name != "posix":
        return False

    # Check via lsb_release module
    try:
        import lsb_release

        info = lsb_release.get_distro_information()
        return info.get("ID", "").lower() == "ubuntu"
    except (ImportError, AttributeError):
        pass

    # Check platform string
    platform_str = platform.platform().lower()
    return "ubuntu" in platform_str


def prepare_environment(config: LaunchConfig) -> EnvironmentConfig:
    """Prepare environment variables for MAPDL process.

    Applies platform-specific configurations and user overrides.

    Parameters:
        config: Launch configuration

    Returns:
        EnvironmentConfig with all variables set

    Examples:
        >>> config = LaunchConfig(...)
        >>> env_config = prepare_environment(config)
        >>> "ANS_CMD_NODIAG" in env_config.variables
        True
    """
    if config.env_vars:
        # User provided explicit env vars (replace mode)
        LOG.debug("Using user-provided environment variables")
        return EnvironmentConfig(variables=config.env_vars, replace_all=True)

    # Start with system environment
    env = os.environ.copy()

    # Apply platform-specific settings
    if is_ubuntu():
        env["I_MPI_SHM_LMT"] = "shm"
        LOG.debug("Applied Ubuntu-specific MPI settings")

    # Apply MAPDL-specific settings
    env["ANS_CMD_NODIAG"] = "TRUE"

    # Could add more configuration based on config parameters
    # For example, license server, memory settings, etc.

    return EnvironmentConfig(variables=env, replace_all=False)


def get_windows_host_ip() -> Optional[str]:
    """Get Windows host IP when running on WSL.

    Uses 'ip route' command to find the Windows host gateway IP.

    Returns:
        Windows host IP address or None if cannot be determined

    Examples:
        >>> get_windows_host_ip()  # On WSL
        '172.24.176.1'
        >>> get_windows_host_ip()  # On native Linux
        None
    """
    if not is_wsl():
        return None

    try:
        # Run ip route command to get default gateway
        result = subprocess.run(  # nosec B603, B607
            ["ip", "route"],
            capture_output=True,
            text=True,
            timeout=5,
            check=True,
        )

        output = result.stdout
        return _parse_ip_route(output)
    except subprocess.TimeoutExpired:
        LOG.warning("Timeout while detecting Windows host IP via 'ip route'")
        return None
    except subprocess.CalledProcessError as e:
        LOG.warning(f"Failed to detect Windows host IP: {e}")
        return None
    except Exception as e:
        LOG.warning(f"Unexpected error detecting Windows host IP: {e}")
        return None


def _parse_ip_route(output: str) -> Optional[str]:
    """Parse ip route output to extract default gateway.

    Parameters:
        output: Output from 'ip route' command

    Returns:
        Default gateway IP address or None

    Examples:
        >>> output = "default via 172.24.176.1 dev eth0"
        >>> _parse_ip_route(output)
        '172.24.176.1'
    """
    from ansys.mapdl.core.misc import parse_ip_route

    return parse_ip_route(output)
