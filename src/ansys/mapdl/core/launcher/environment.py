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
    """Detect if running on Windows Subsystem for Linux (WSL).

    Checks for WSL-specific environment variables to determine if the code
    is executing within a WSL environment.

    Returns
    -------
    bool
        True if running on WSL, False otherwise

    Examples
    --------
    Check if running on WSL:

    >>> from ansys.mapdl.core.launcher.environment import is_wsl
    >>> if is_wsl():
    ...     print("Running on WSL")
    ... else:
    ...     print("Not on WSL")

    Notes
    -----
    - This check relies on environment variables set by WSL
    - May not work with older WSL versions (pre-WSL2)
    - Requires posix-compatible OS (will return False on Windows native)
    """
    if os.name != "posix":
        return False

    # Check WSL-specific environment variables
    return bool(os.environ.get("WSL_DISTRO_NAME") or os.environ.get("WSL_INTEROP"))


def is_ubuntu() -> bool:
    """Detect if running on Ubuntu Linux distribution.

    Attempts to determine if the system is running Ubuntu by checking
    the lsb_release module first, then falling back to platform string analysis.

    Returns
    -------
    bool
        True if running on Ubuntu, False otherwise

    Examples
    --------
    Check if running on Ubuntu:

    >>> from ansys.mapdl.core.launcher.environment import is_ubuntu
    >>> if is_ubuntu():
    ...     print("Running on Ubuntu")
    ... else:
    ...     print("Not on Ubuntu")

    Notes
    -----
    - Returns False on non-POSIX systems (Windows native)
    - Uses multiple detection methods for robustness
    - May incorrectly identify Ubuntu-based distributions as Ubuntu
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
    """Prepare environment variables for MAPDL process execution.

    Applies platform-specific configurations and user overrides to create
    a complete environment configuration. If user-provided environment
    variables are specified, they are used in replace mode. Otherwise,
    platform-specific settings are applied to system environment.

    Parameters
    ----------
    config : LaunchConfig
        Launch configuration containing env_vars and platform information

    Returns
    -------
    EnvironmentConfig
        Environment configuration with all variables set and replace mode flag

    Examples
    --------
    Prepare environment for MAPDL process:

    >>> from ansys.mapdl.core.launcher.models import LaunchConfig
    >>> from ansys.mapdl.core.launcher.environment import prepare_environment
    >>> config = LaunchConfig(...)
    >>> env_config = prepare_environment(config)
    >>> "ANS_CMD_NODIAG" in env_config.variables
    True

    Use custom environment variables:

    >>> config = LaunchConfig(env_vars={"ANS_CMD": "NODIAG", "MY_VAR": "value"})
    >>> env_config = prepare_environment(config)
    >>> env_config.replace_all
    True

    Notes
    -----
    - Ubuntu-specific MPI settings are applied automatically
    - The ANS_CMD_NODIAG variable is always set for MAPDL
    - User-provided variables completely replace system environment
    - System environment is preserved when user doesn't specify env_vars
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
    """Get Windows host IP address when running on WSL.

    Uses the 'ip route' command to find the Windows host gateway IP address.
    This is useful for connecting from WSL to services running on the Windows
    host machine.

    Returns
    -------
    Optional[str]
        Windows host IP address (e.g., '172.24.176.1') if detected, None if
        not on WSL or cannot be determined

    Raises
    ------
    None
        Errors are logged but not raised; the function returns None on failure

    Examples
    --------
    Get Windows host IP from WSL:

    >>> from ansys.mapdl.core.launcher.environment import get_windows_host_ip
    >>> host_ip = get_windows_host_ip()
    >>> if host_ip:
    ...     print(f"Windows host IP: {host_ip}")

    Notes
    -----
    - Only works when running on WSL (Windows Subsystem for Linux)
    - Returns None when running on native Linux or Windows
    - Uses subprocess call to 'ip route' command
    - Network timeout is set to 5 seconds
    - Errors are logged at WARNING level and function returns None
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
    """Parse 'ip route' command output to extract default gateway IP.

    Extracts the default gateway IP address from the output of the
    'ip route' command. This IP typically represents the Windows host
    when running on WSL.

    Parameters
    ----------
    output : str
        Raw output from 'ip route' command

    Returns
    -------
    Optional[str]
        Default gateway IP address if found, None otherwise

    Raises
    ------
    None
        Returns None if parsing fails

    Examples
    --------
    Parse IP route output:

    >>> from ansys.mapdl.core.launcher.environment import _parse_ip_route
    >>> output = "default via 172.24.176.1 dev eth0"
    >>> _parse_ip_route(output)
    '172.24.176.1'

    >>> output = "default via 192.168.1.1 dev eth0\\n192.168.1.0/24 dev eth0"
    >>> _parse_ip_route(output)
    '192.168.1.1'

    Notes
    -----
    - Searches for "default via" prefix to find the default route
    - This function delegates to ansys.mapdl.core.misc.parse_ip_route
    - Internal utility function; use get_windows_host_ip() in public API
    """
    from ansys.mapdl.core.misc import parse_ip_route

    return parse_ip_route(output)
