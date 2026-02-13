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

"""Configuration validation for MAPDL launcher.

All validation functions are pure and return ValidationResult objects.
No exceptions are raised - all issues are collected as errors/warnings.
"""

import os

import psutil

from ansys.mapdl.core import LOG

from .environment import is_wsl
from .models import LaunchConfig, LaunchMode, ValidationResult


def validate_config(config: LaunchConfig) -> ValidationResult:
    """Validate complete launch configuration.

    Checks:
    - Version compatibility with mode
    - Resource availability (CPU, RAM)
    - Port availability
    - File permissions
    - Conflicting options
    - Platform compatibility

    Parameters:
        config: Complete launch configuration

    Returns:
        ValidationResult with errors and warnings

    Examples:
        >>> config = LaunchConfig(...)
        >>> result = validate_config(config)
        >>> if not result.valid:
        ...     raise ConfigurationError(result.errors)
    """
    result = ValidationResult(valid=True)

    # Run all validation checks
    _validate_version_mode_compatibility(config, result)
    _validate_resource_availability(config, result)
    _validate_port_availability(config, result)
    _validate_file_permissions(config, result)
    _validate_conflicting_options(config, result)
    _validate_platform_compatibility(config, result)

    return result


def _validate_version_mode_compatibility(
    config: LaunchConfig, result: ValidationResult
) -> None:
    """Validate version-mode compatibility.

    Parameters:
        config: Launch configuration
        result: ValidationResult to update
    """
    if config.mode == LaunchMode.GRPC and config.version:
        if config.version < 211:
            result.add_error(
                f"gRPC mode requires MAPDL version 211 (2021R1) or newer. "
                f"Current version: {config.version}. Please use mode='console' "
                f"for older versions on Linux."
            )


def _validate_resource_availability(
    config: LaunchConfig, result: ValidationResult
) -> None:
    """Validate CPU and RAM availability.

    Parameters:
        config: Launch configuration
        result: ValidationResult to update
    """
    if not config.start_instance:
        # No need to check resources if not starting instance
        return

    # Check CPU availability
    try:
        available_cpus = psutil.cpu_count(logical=False) or psutil.cpu_count() or 1

        if config.nproc > available_cpus:
            result.add_warning(
                f"Requested {config.nproc} processors but only {available_cpus} "
                f"physical CPUs available. Performance may be degraded."
            )

        # Soft limit: warn if excessive
        if config.nproc > available_cpus * 2:
            result.add_error(
                f"Requested {config.nproc} processors but only {available_cpus} "
                f"physical CPUs available. This is excessive and will likely fail."
            )
    except Exception as e:
        LOG.debug(f"Could not check CPU availability: {e}")

    # Check RAM availability
    if config.ram:
        try:
            available_ram_mb = psutil.virtual_memory().available // (1024**2)

            if config.ram > available_ram_mb:
                result.add_error(
                    f"Requested {config.ram} MB RAM but only {available_ram_mb} MB available."
                )
            elif config.ram > available_ram_mb * 0.9:
                result.add_warning(
                    f"Requested {config.ram} MB RAM but only {available_ram_mb} MB available. "
                    f"System may become unstable."
                )
        except Exception as e:
            LOG.debug(f"Could not check RAM availability: {e}")


def _validate_port_availability(config: LaunchConfig, result: ValidationResult) -> None:
    """Validate port is available if starting new instance.

    Parameters:
        config: Launch configuration
        result: ValidationResult to update
    """
    if not config.start_instance:
        # If not starting instance, port validation is less critical
        # We'll still check if we can connect, but that's done elsewhere
        return

    # Import here to avoid circular dependency
    from .network import check_port_status

    try:
        status = check_port_status(config.port, config.ip)

        if not status.available:
            if status.used_by_mapdl:
                result.add_error(
                    f"Port {config.port} is already in use by another MAPDL instance. "
                    f"Please specify a different port or stop the existing instance."
                )
            else:
                result.add_error(
                    f"Port {config.port} is already in use by another process. "
                    f"Please specify a different port."
                )
    except Exception as e:
        LOG.debug(f"Could not check port availability: {e}")
        result.add_warning(
            f"Could not verify port {config.port} availability. "
            f"Launch may fail if port is in use."
        )


def _validate_file_permissions(config: LaunchConfig, result: ValidationResult) -> None:
    """Validate file system permissions.

    Parameters:
        config: Launch configuration
        result: ValidationResult to update
    """
    if not config.start_instance:
        return

    # Check exec_file exists and is executable
    if config.exec_file:
        if not os.path.isfile(config.exec_file):
            result.add_error(f"MAPDL executable not found: {config.exec_file}")
        elif not os.access(config.exec_file, os.X_OK) and os.name == "posix":
            result.add_error(f"MAPDL executable is not executable: {config.exec_file}")

    # Check run_location is writable
    if config.run_location:
        if not os.path.exists(config.run_location):
            # Will be created, check parent directory
            parent = os.path.dirname(config.run_location)
            if parent and not os.access(parent, os.W_OK):
                result.add_error(
                    f"Cannot create run_location: parent directory not writable: {parent}"
                )
        elif not os.access(config.run_location, os.W_OK):
            result.add_error(f"Run location is not writable: {config.run_location}")


def _validate_conflicting_options(
    config: LaunchConfig, result: ValidationResult
) -> None:
    """Validate no conflicting options are set.

    Parameters:
        config: Launch configuration
        result: ValidationResult to update
    """
    # start_instance + ip conflict (except on WSL or localhost)
    if config.start_instance and config.ip not in ("127.0.0.1", "localhost"):
        if not is_wsl():
            result.add_error(
                "Cannot specify 'ip' when 'start_instance' is True (except on WSL). "
                "Either set start_instance=False to connect to remote instance, "
                "or remove ip argument to launch locally."
            )

    # HPC + ip conflict
    if config.launch_on_hpc and config.ip not in ("127.0.0.1", "localhost", ""):
        result.add_error(
            "Cannot specify custom 'ip' when launching on HPC. "
            "IP will be determined from HPC job allocation."
        )

    # HPC + exec_file on Windows
    if config.launch_on_hpc and os.name == "nt":
        result.add_error(
            "HPC launch is not supported on Windows. "
            "Please run from Linux HPC login node."
        )


def _validate_platform_compatibility(
    config: LaunchConfig, result: ValidationResult
) -> None:
    """Validate platform compatibility.

    Parameters:
        config: Launch configuration
        result: ValidationResult to update
    """
    # Console mode only on Linux
    if config.mode == LaunchMode.CONSOLE and os.name == "nt":
        result.add_error("Console mode is only supported on Linux.")

    # Transport modes validation
    if config.transport_mode:
        # UDS only on Linux
        from .models import TransportMode

        if config.transport_mode == TransportMode.UDS and os.name == "nt":
            result.add_error("Unix domain socket transport is only supported on Linux.")

        # mTLS requires certificates
        if config.transport_mode == TransportMode.MTLS and not config.certs_dir:
            result.add_error(
                "mTLS transport mode requires 'certs_dir' to be specified."
            )
