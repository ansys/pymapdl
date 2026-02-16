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

"""Configuration resolution for MAPDL launcher.

This module contains pure functions that resolve configuration from:
1. Explicit function arguments
2. Environment variables
3. System defaults

All functions are pure (same input → same output) and raise
ConfigurationError for invalid states.
"""

import os
import tempfile
from typing import Any, Dict, Optional

from ansys.mapdl.core import _HAS_ATC, LOG

from .errors import ConfigurationError
from .models import LaunchConfig, LaunchMode, TransportMode

# Constants
LOCALHOST = "127.0.0.1"
MAPDL_DEFAULT_PORT = 50052
DEFAULT_TIMEOUT = 45


def resolve_launch_config(
    exec_file: Optional[str] = None,
    run_location: Optional[str] = None,
    jobname: str = "file",
    nproc: Optional[int] = None,
    port: Optional[int] = None,
    ip: Optional[str] = None,
    mode: Optional[str] = None,
    version: Optional[int] = None,
    start_instance: Optional[bool] = None,
    ram: Optional[int] = None,
    timeout: Optional[int] = None,
    cleanup_on_exit: bool = True,
    clear_on_connect: bool = True,
    override: bool = False,
    remove_temp_dir_on_exit: bool = False,
    set_no_abort: bool = True,
    additional_switches: str = "",
    license_type: Optional[str] = None,
    launch_on_hpc: bool = False,
    running_on_hpc: bool = True,
    scheduler_options: Optional[Dict[str, Any]] = None,
    loglevel: str = "ERROR",
    log_apdl: Optional[str] = None,
    print_com: bool = False,
    mapdl_output: Optional[str] = None,
    transport_mode: Optional[str] = None,
    uds_dir: Optional[str] = None,
    uds_id: Optional[str] = None,
    certs_dir: Optional[str] = None,
    env_vars: Optional[Dict[str, str]] = None,
    license_server_check: bool = False,
    force_intel: bool = False,
    graphics_backend: Optional[str] = None,
    **kwargs: Any,
) -> LaunchConfig:
    """Resolve complete launch configuration.

    Resolution order for each parameter:
    1. Explicit argument (if not None)
    2. Environment variable (if set)
    3. Default value

    Parameters:
        exec_file: Path to MAPDL executable
        run_location: Working directory
        jobname: MAPDL job name
        nproc: Number of processors
        port: gRPC port
        ip: IP address
        mode: Launch mode
        version: MAPDL version
        start_instance: Whether to start new instance
        ram: RAM allocation in MB
        timeout: Launch timeout in seconds
        cleanup_on_exit: Clean up on exit
        clear_on_connect: Clear on connection
        override: Override existing instance
        remove_temp_dir_on_exit: Remove temp dir on exit
        set_no_abort: Set NO_ABORT flag
        additional_switches: Additional command line switches
        license_type: License type
        launch_on_hpc: Launch on HPC cluster
        running_on_hpc: Running on HPC
        scheduler_options: HPC scheduler options
        loglevel: Logging level
        log_apdl: APDL log file path
        print_com: Print commands
        mapdl_output: Redirect MAPDL output
        transport_mode: gRPC transport mode
        uds_dir: Unix domain socket directory
        uds_id: Unix domain socket ID
        certs_dir: Certificates directory
        env_vars: Environment variables
        license_server_check: Check license server
        force_intel: Force Intel MPI
        graphics_backend: Graphics backend
        **kwargs: Additional arguments

    Returns:
        Complete, validated LaunchConfig

    Raises:
        ConfigurationError: If configuration is invalid or conflicting

    Examples:
        >>> config = resolve_launch_config(nproc=4, version=222)
        >>> config.nproc
        4
        >>> config.version
        222
    """
    # Resolve start_instance first (affects other resolution)
    resolved_start_instance = resolve_start_instance(start_instance, ip)

    # Resolve version early (needed for mode resolution)
    resolved_exec_file = resolve_exec_file(exec_file, version, resolved_start_instance)
    resolved_version = resolve_version(version, resolved_exec_file)

    # Resolve core parameters
    resolved_run_location = resolve_run_location(run_location)
    resolved_port = resolve_port(port)
    resolved_ip = resolve_ip(ip, resolved_start_instance)
    resolved_mode = resolve_mode(mode, resolved_version)
    resolved_nproc = resolve_nproc(nproc)

    # Resolve resource parameters
    resolved_ram = resolve_ram(ram)
    resolved_timeout = resolve_timeout(timeout, launch_on_hpc)

    # Resolve transport mode
    resolved_transport_mode = resolve_transport_mode(transport_mode)

    # Resolve environment variables
    resolved_env_vars = env_vars if env_vars else {}

    return LaunchConfig(
        exec_file=resolved_exec_file,
        run_location=resolved_run_location,
        jobname=jobname,
        nproc=resolved_nproc,
        port=resolved_port,
        ip=resolved_ip,
        mode=resolved_mode,
        version=resolved_version,
        start_instance=resolved_start_instance,
        ram=resolved_ram,
        timeout=resolved_timeout,
        cleanup_on_exit=cleanup_on_exit,
        clear_on_connect=clear_on_connect,
        override=override,
        remove_temp_dir_on_exit=remove_temp_dir_on_exit,
        set_no_abort=set_no_abort,
        additional_switches=additional_switches,
        license_type=license_type,
        launch_on_hpc=launch_on_hpc,
        running_on_hpc=running_on_hpc,
        scheduler_options=scheduler_options,
        loglevel=loglevel,
        log_apdl=log_apdl,
        print_com=print_com,
        mapdl_output=mapdl_output,
        transport_mode=resolved_transport_mode,
        uds_dir=uds_dir,
        uds_id=uds_id,
        certs_dir=certs_dir,
        env_vars=resolved_env_vars,
        license_server_check=license_server_check,
        force_intel=force_intel,
        graphics_backend=graphics_backend,
    )


def resolve_exec_file(
    exec_file: Optional[str], version: Optional[int], start_instance: bool
) -> str:
    """Resolve MAPDL executable path.

    Resolution order:
    1. Explicit exec_file argument
    2. PYMAPDL_MAPDL_EXEC environment variable
    3. Auto-detect from version
    4. Auto-detect latest installed

    Parameters:
        exec_file: Explicit path to executable
        version: MAPDL version to find
        start_instance: Whether starting new instance

    Returns:
        Absolute path to MAPDL executable

    Raises:
        ConfigurationError: If executable cannot be found or is invalid
    """
    # If not starting instance, exec_file not needed
    if not start_instance:
        return ""

    # Priority 1: Explicit argument
    if exec_file:
        if not os.path.isfile(exec_file):
            raise ConfigurationError(
                f'Invalid MAPDL executable at "{exec_file}". File does not exist.'
            )
        return os.path.abspath(exec_file)

    # Priority 2: Environment variable
    env_exec = os.getenv("PYMAPDL_MAPDL_EXEC")
    if env_exec:
        if not os.path.isfile(env_exec):
            raise ConfigurationError(
                f'Invalid MAPDL executable from PYMAPDL_MAPDL_EXEC: "{env_exec}". '
                f"File does not exist."
            )
        return os.path.abspath(env_exec)

    # Priority 3: Auto-detect
    if not _HAS_ATC:
        raise ConfigurationError(
            "Cannot auto-detect MAPDL executable. Please either:\n"
            "1. Install 'ansys-tools-common' package, or\n"
            "2. Specify exec_file argument, or\n"
            "3. Set PYMAPDL_MAPDL_EXEC environment variable"
        )

    try:
        from ansys.tools.common.path import get_mapdl_path

        detected_exec = get_mapdl_path(version=version)
        if detected_exec:
            LOG.debug(f"Auto-detected MAPDL executable: {detected_exec}")
            return detected_exec
    except Exception as e:
        raise ConfigurationError(f"Failed to auto-detect MAPDL executable: {e}")

    raise ConfigurationError(
        "MAPDL executable not found. Please specify exec_file argument "
        "or set PYMAPDL_MAPDL_EXEC environment variable."
    )


def resolve_port(port: Optional[int]) -> int:
    """Resolve port number.

    Resolution order:
    1. Explicit port argument
    2. PYMAPDL_PORT environment variable
    3. Default port (50052)

    Note: Port availability is checked separately in validation.

    Parameters:
        port: Explicit port number

    Returns:
        Port number

    Raises:
        ConfigurationError: If port is invalid (<1 or >65535)
    """
    # Priority 1: Explicit argument
    if port is not None:
        if not (1 <= port <= 65535):
            raise ConfigurationError(
                f"Invalid port: {port}. Port must be between 1 and 65535."
            )
        return port

    # Priority 2: Environment variable
    env_port = os.getenv("PYMAPDL_PORT")
    if env_port:
        try:
            port_int = int(env_port)
            if not (1 <= port_int <= 65535):
                raise ConfigurationError(
                    f"Invalid port from PYMAPDL_PORT: {port_int}. "
                    f"Port must be between 1 and 65535."
                )
            LOG.debug(f"Using port from PYMAPDL_PORT env var: {port_int}")
            return port_int
        except ValueError:
            raise ConfigurationError(
                f"Invalid port from PYMAPDL_PORT: '{env_port}'. Must be an integer."
            )

    # Priority 3: Default
    LOG.debug(f"Using default port: {MAPDL_DEFAULT_PORT}")
    return MAPDL_DEFAULT_PORT


def resolve_ip(ip: Optional[str], start_instance: bool) -> str:
    """Resolve IP address.

    Resolution order:
    1. Explicit ip argument
    2. PYMAPDL_IP environment variable
    3. WSL host detection (if on WSL)
    4. Localhost (127.0.0.1)

    Parameters:
        ip: Explicit IP address
        start_instance: Whether starting new instance

    Returns:
        IP address

    Raises:
        ConfigurationError: If IP is invalid or cannot be resolved
    """
    import socket

    # Priority 1: Explicit argument
    if ip:
        try:
            # Convert hostname to IP if needed
            resolved_ip = socket.gethostbyname(ip)
            LOG.debug(f"Using explicit IP: {resolved_ip}")
            return resolved_ip
        except socket.gaierror:
            raise ConfigurationError(f"Cannot resolve hostname or IP: {ip}")

    # Priority 2: Environment variable
    env_ip = os.getenv("PYMAPDL_IP", "").strip()
    if env_ip:
        try:
            resolved_ip = socket.gethostbyname(env_ip)
            LOG.debug(f"Using IP from PYMAPDL_IP env var: {resolved_ip}")
            return resolved_ip
        except socket.gaierror:
            raise ConfigurationError(
                f"Cannot resolve hostname or IP from PYMAPDL_IP: {env_ip}"
            )

    # Priority 3: WSL host detection
    from .environment import get_windows_host_ip, is_wsl

    if is_wsl() and start_instance:
        wsl_ip = get_windows_host_ip()
        if wsl_ip:
            LOG.debug(f"On WSL: Using Windows host IP: {wsl_ip}")
            return wsl_ip
        else:
            raise ConfigurationError(
                "Running on WSL but cannot determine Windows host IP address. "
                "Please specify ip argument explicitly."
            )

    # Priority 4: Default localhost
    LOG.debug(f"Using default IP: {LOCALHOST}")
    return LOCALHOST


def resolve_mode(mode: Optional[str], version: Optional[int]) -> LaunchMode:
    """Resolve launch mode.

    Validates mode compatibility with MAPDL version.

    Parameters:
        mode: Requested mode ("grpc" or "console")
        version: MAPDL version

    Returns:
        Validated LaunchMode

    Raises:
        ConfigurationError: If mode incompatible with version/platform
    """
    # Explicit mode
    if mode:
        mode_lower = mode.lower()
        if mode_lower == "grpc":
            return LaunchMode.GRPC
        elif mode_lower == "console":
            # Console mode only on Linux
            if os.name == "nt":
                raise ConfigurationError(
                    "Console mode is only supported on Linux. Use mode='grpc' on Windows."
                )
            return LaunchMode.CONSOLE
        else:
            raise ConfigurationError(
                f"Invalid mode: '{mode}'. Must be 'grpc' or 'console'."
            )

    # Auto-detect based on version
    if version and version < 211:
        # Old version, use console if on Linux
        if os.name == "posix":
            LOG.debug("Auto-selected console mode for older MAPDL version on Linux")
            return LaunchMode.CONSOLE
        else:
            raise ConfigurationError(
                f"MAPDL version {version} does not support gRPC mode. "
                f"Please use version 211 (2021R1) or newer."
            )

    # Default to gRPC (modern mode)
    LOG.debug("Auto-selected gRPC mode")
    return LaunchMode.GRPC


def resolve_nproc(nproc: Optional[int]) -> int:
    """Resolve number of processors.

    Resolution order:
    1. Explicit nproc argument
    2. PYMAPDL_NPROC environment variable
    3. Default: 2

    Parameters:
        nproc: Explicit processor count

    Returns:
        Number of processors

    Raises:
        ConfigurationError: If nproc invalid
    """
    # Priority 1: Explicit argument
    if nproc is not None:
        if nproc < 1:
            raise ConfigurationError(f"Invalid nproc: {nproc}. Must be at least 1.")
        return nproc

    # Priority 2: Environment variable
    env_nproc = os.getenv("PYMAPDL_NPROC")
    if env_nproc:
        try:
            nproc_int = int(env_nproc)
            if nproc_int < 1:
                raise ConfigurationError(
                    f"Invalid nproc from PYMAPDL_NPROC: {nproc_int}. Must be at least 1."
                )
            LOG.debug(f"Using nproc from PYMAPDL_NPROC env var: {nproc_int}")
            return nproc_int
        except ValueError:
            raise ConfigurationError(
                f"Invalid nproc from PYMAPDL_NPROC: '{env_nproc}'. Must be an integer."
            )

    # Priority 3: Default
    default_nproc = 2
    LOG.debug(f"Using default nproc: {default_nproc}")
    return default_nproc


def resolve_version(version: Optional[int], exec_file: str) -> Optional[int]:
    """Resolve MAPDL version.

    Resolution order:
    1. Explicit version argument
    2. PYMAPDL_MAPDL_VERSION environment variable
    3. Extract from exec_file path

    Parameters:
        version: Explicit version
        exec_file: Path to executable

    Returns:
        Version in XYZ format (e.g., 222) or None
    """
    # Priority 1: Explicit argument
    if version is not None:
        return version

    # Priority 2: Environment variable
    env_version = os.getenv("PYMAPDL_MAPDL_VERSION")
    if env_version:
        try:
            version_int = int(env_version)
            LOG.debug(
                f"Using version from PYMAPDL_MAPDL_VERSION env var: {version_int}"
            )
            return version_int
        except ValueError:
            LOG.warning(
                f"Invalid version from PYMAPDL_MAPDL_VERSION: '{env_version}'. "
                f"Attempting to extract from executable path."
            )

    # Priority 3: Extract from exec_file
    if exec_file and _HAS_ATC:
        try:
            from ansys.tools.common.path import version_from_path

            detected_version = version_from_path("mapdl", exec_file)
            if detected_version:
                LOG.debug(f"Detected MAPDL version from executable: {detected_version}")
                return detected_version
        except Exception as e:
            LOG.debug(f"Could not extract version from executable path: {e}")

    # Could not determine version
    LOG.debug("MAPDL version could not be determined")
    return None


def resolve_run_location(run_location: Optional[str]) -> str:
    """Resolve working directory for MAPDL.

    Resolution order:
    1. Explicit run_location argument
    2. Create temporary directory

    Parameters:
        run_location: Explicit working directory

    Returns:
        Absolute path to working directory

    Raises:
        ConfigurationError: If directory cannot be created
    """
    if run_location:
        # Ensure directory exists
        if not os.path.exists(run_location):
            try:
                os.makedirs(run_location, exist_ok=True)
                LOG.debug(f"Created run location directory: {run_location}")
            except Exception as e:
                raise ConfigurationError(
                    f"Cannot create run_location directory '{run_location}': {e}"
                )
        return os.path.abspath(run_location)

    # Create temporary directory
    try:
        temp_dir = tempfile.mkdtemp(prefix="ansys_")
        LOG.debug(f"Created temporary run location: {temp_dir}")
        return temp_dir
    except Exception as e:
        raise ConfigurationError(f"Cannot create temporary directory: {e}")


def resolve_ram(ram: Optional[int]) -> Optional[int]:
    """Resolve RAM allocation.

    Parameters:
        ram: Explicit RAM in MB

    Returns:
        RAM in MB or None

    Raises:
        ConfigurationError: If RAM is invalid
    """
    if ram is not None:
        if ram < 1:
            raise ConfigurationError(f"Invalid ram: {ram}. Must be at least 1 MB.")
        return ram
    return None


def resolve_timeout(timeout: Optional[int], launch_on_hpc: bool) -> int:
    """Resolve launch timeout.

    Parameters:
        timeout: Explicit timeout in seconds
        launch_on_hpc: Whether launching on HPC

    Returns:
        Timeout in seconds
    """
    if timeout is not None:
        if timeout < 1:
            raise ConfigurationError(
                f"Invalid timeout: {timeout}. Must be at least 1 second."
            )
        return timeout

    # HPC launches take longer
    if launch_on_hpc:
        return DEFAULT_TIMEOUT * 2

    return DEFAULT_TIMEOUT


def resolve_start_instance(start_instance: Optional[bool], ip: Optional[str]) -> bool:
    """Resolve whether to start new instance.

    Resolution order:
    1. Explicit start_instance argument
    2. PYMAPDL_START_INSTANCE environment variable
    3. Infer from ip (if ip specified, default to False)
    4. Default: True

    Parameters:
        start_instance: Explicit start instance flag
        ip: IP address (affects default)

    Returns:
        Whether to start new instance
    """
    # Priority 1: Explicit argument
    if start_instance is not None:
        if ip is not None:
            LOG.warning(
                "Both start_instance and ip are specified. start_instance will take precedence."
            )
        return start_instance

    # Priority 2: Environment variable
    env_start = os.getenv("PYMAPDL_START_INSTANCE", "").strip().lower()
    if env_start:
        if env_start in ("true", "1", "yes"):
            LOG.debug("Using start_instance=True from PYMAPDL_START_INSTANCE env var")
            return True
        elif env_start in ("false", "0", "no"):
            LOG.debug("Using start_instance=False from PYMAPDL_START_INSTANCE env var")
            return False

    # Priority 3: Infer from ip
    env_ip = os.getenv("PYMAPDL_IP", "").strip()
    if ip or env_ip:
        # IP specified, likely connecting to existing instance
        LOG.debug("IP specified, defaulting start_instance to False")
        return False

    # Priority 4: Default to True
    LOG.debug("Defaulting start_instance to True")
    return True


def resolve_transport_mode(transport_mode: Optional[str]) -> Optional[TransportMode]:
    """Resolve gRPC transport mode.

    Parameters:
        transport_mode: Explicit transport mode

    Returns:
        TransportMode enum or None

    Raises:
        ConfigurationError: If transport mode is invalid
    """
    if transport_mode is None:
        return None

    mode_lower = transport_mode.lower()
    if mode_lower == "insecure":
        return TransportMode.INSECURE
    elif mode_lower == "uds":
        return TransportMode.UDS
    elif mode_lower == "wnua":
        return TransportMode.WNUA
    elif mode_lower == "mtls":
        return TransportMode.MTLS
    else:
        raise ConfigurationError(
            f"Invalid transport_mode: '{transport_mode}'. "
            f"Must be one of: insecure, uds, wnua, mtls"
        )
