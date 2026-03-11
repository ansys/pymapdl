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

"""Custom exceptions for MAPDL launcher."""


class ConfigurationError(Exception):
    """Raised when configuration is invalid or contains conflicting options.

    This exception is raised during configuration validation when there are
    issues that prevent MAPDL from being launched, such as invalid parameter
    combinations or missing required files.

    Parameters
    ----------
    *args : Any
        Arguments passed to the base Exception class

    Attributes
    ----------
    args : tuple
        Exception arguments

    Examples
    --------
    Catch configuration errors:

    >>> from ansys.mapdl.core.launcher.errors import ConfigurationError
    >>> try:
    ...     validate_config(bad_config)
    ... except ConfigurationError as e:
    ...     print(f"Configuration error: {e}")

    Raise configuration error:

    >>> raise ConfigurationError("Invalid IP address specified")

    Notes
    -----
    - This is a fatal error that prevents launch
    - Check validation results before attempting to launch
    - See validate_config() for detailed error messages
    """

    pass


class LaunchError(Exception):
    """Raised when MAPDL process fails to launch or start successfully.

    This exception is raised when MAPDL cannot be started, either due to
    process startup failure, timeout, or other runtime issues that prevent
    the process from reaching a ready state.

    Parameters
    ----------
    *args : Any
        Arguments passed to the base Exception class

    Attributes
    ----------
    args : tuple
        Exception arguments

    Examples
    --------
    Catch launch errors:

    >>> from ansys.mapdl.core.launcher.errors import LaunchError
    >>> try:
    ...     process_info = launch_mapdl_process(config, env_vars)
    ... except LaunchError as e:
    ...     print(f"Failed to launch MAPDL: {e}")

    Raise launch error:

    >>> raise LaunchError("MAPDL process exited unexpectedly")

    Notes
    -----
    - This error typically indicates a runtime problem during launch
    - Check system resources and permissions if this occurs
    - Detailed error messages are usually logged before the exception
    - Related to MapdlDidNotStart from core.errors module
    """

    pass
