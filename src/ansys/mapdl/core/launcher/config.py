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
    running_on_hpc: bool = False,
    scheduler_options: Optional[Dict[str, Any]] = None,
    loglevel: str = "ERROR",
    log_apdl: Optional[str] = None,
    print_com: bool = False,
    mapdl_output: Optional[str] = None,
    transport_mode: Optional[str] = None,
    uds_dir: Optional[str] = None,
    uds_id: Optional[str] = None,
    certs_dir: Optional[str] = None,
    add_env_vars: Optional[Dict[str, str]] = None,
    replace_env_vars: Optional[Dict[str, str]] = None,
    license_server_check: bool = False,
    force_intel: bool = False,
    graphics_backend: Optional[str] = None,
    start_timeout: Optional[int] = None,
    channel: Optional[Any] = None,
    **kwargs: Any,
) -> LaunchConfig:
    """Resolve complete launch configuration.

    Resolution order for each parameter:
    1. Explicit argument (if not None)
    2. Environment variable (if set)
    3. Default value

    This function combines user-provided arguments, environment variable
    overrides, and system defaults to produce a complete ``LaunchConfig``
    object suitable for launching or connecting to MAPDL.

    Parameters
    ----------
    exec_file : Optional[str]
        The location of the MAPDL executable. For instance, on Windows:

        - ``C:\\Program Files\\ANSYS Inc\\v252\\ansys\\bin\\mapdl.exe``

        And on Linux:

        - ``/usr/ansys_inc/v252/ansys/bin/mapdl``

        By default (:class:`None`), uses the cached location unless the
        environment variable :envvar:`PYMAPDL_MAPDL_EXEC` is set.

    run_location : Optional[str]
        MAPDL working directory. If the directory doesn't exist, one is created.
        Defaults to a temporary working directory created in the directory
        obtained by ``tempfile.gettempdir()`` and starting with ``'ansys_'``
        and a random string. The temporary directory is removed when MAPDL
        exits if ``cleanup_on_exit`` is :class:`True`.

    jobname : str
        MAPDL jobname. Defaults to ``'file'``.

    nproc : Optional[int]
        Number of processors. If running on an HPC cluster, this value is
        adjusted to the number of CPUs allocated to the job, unless the
        ``running_on_hpc`` argument is set to ``False``.
        Defaults to ``2`` CPUs.

    port : Optional[int]
        Port to launch MAPDL gRPC on. You can also provide this value through
        the environment variable :envvar:`PYMAPDL_PORT`.
        However, the argument (if specified) has precedence over the environment
        variable. Defaults to ``50052``.

    ip : Optional[str]
        Specify the IP address of the MAPDL instance to connect to.
        Used only when ``start_instance`` is :class:`False`.
        You can also provide this value through the environment variable
        :envvar:`PYMAPDL_IP`. Defaults to ``'127.0.0.1'`` (localhost).

    mode : Optional[str]
        Mode to launch MAPDL. Must be one of:

        - ``'grpc'`` - Recommended, available on ANSYS 2021R1 or newer
        - ``'console'`` - Legacy console mode, Linux only, not recommended

        The gRPC mode is available on ANSYS 2021R1 or newer and provides
        the best performance and stability.

    version : Optional[int]
        Version of MAPDL to launch. Versions can be provided as integers
        (i.e. ``version=222``) or floats (i.e. ``version=22.2``).
        You can also provide this value through the environment variable
        :envvar:`PYMAPDL_MAPDL_VERSION`. Defaults to latest available version.

    start_instance : Optional[bool]
        When :class:`False`, connect to an existing MAPDL instance at ``ip``
        and ``port``. When :class:`True`, launch a local instance of MAPDL.
        You can also provide this value through the environment variable
        :envvar:`PYMAPDL_START_INSTANCE`. Defaults to start locally (:class:`True`).

    ram : Optional[int]
        Total size in megabytes of the workspace (memory) used for the initial
        allocation. To force a fixed size throughout the run, specify a negative
        number. The default is :class:`None`, in which case 2 GB (2048 MB) is used.

    timeout : Optional[int]
        Maximum allowable time to connect to the MAPDL server.
        By default it is 45 seconds, however, it is increased to 90 seconds
        if running on HPC.

    cleanup_on_exit : bool
        Exit MAPDL when Python exits or the MAPDL Python instance is
        garbage collected. Defaults to :class:`True`.

    clear_on_connect : bool
        Defaults to :class:`True`, giving you a fresh environment when
        connecting to MAPDL. When ``start_instance`` is :class:`False`,
        it defaults to :class:`True`.

    override : bool
        Attempts to delete the lock file at the ``run_location``.
        Useful when a prior MAPDL session has exited prematurely and
        the lock file has not been deleted. Defaults to :class:`False`.

    remove_temp_dir_on_exit : bool
        When this parameter is :class:`True`, the directory created to launch
        MAPDL on temporary location will be deleted when MAPDL is exited.
        Defaults to :class:`False`. Note: This option is not available
        when running on HPC.

    set_no_abort : bool
        Sets MAPDL to not abort at the first error within /BATCH mode.
        *(Development use only)*. Defaults to :class:`True`.

    additional_switches : str
        Additional switches for MAPDL, for example ``'aa_r'`` (academic
        research license). Avoid adding switches like ``-i``, ``-o`` or ``-b``
        as these are already included to start up the MAPDL server.
        Defaults to an empty string.

    license_type : Optional[str]
        Enable license type selection. You can input a string for its
        license name (for example ``'meba'`` or ``'ansys'``) or its description
        ("enterprise solver" or "enterprise" respectively).
        Defaults to :class:`None`, which means no specific license is requested.

    launch_on_hpc : bool
        If :class:`True`, uses the implemented scheduler (SLURM only) to
        launch an MAPDL instance on the HPC. Pass the ``scheduler_options``
        argument to specify scheduler options.
        Defaults to :class:`False`.

    running_on_hpc : bool
        Whether to detect if PyMAPDL is running on an HPC cluster.
        Currently only SLURM clusters are supported.
        This option can be bypassed if the :envvar:`PYMAPDL_RUNNING_ON_HPC`
        environment variable is set to :class:`True`.
        Defaults to :class:`False`.

    scheduler_options : Optional[Dict[str, Any]]
        HPC scheduler options as a dictionary. For example:
        ``{"nodes": "1", "ntasks-per-node": "16"}``.
        See the HPC documentation for supported options.

    loglevel : str
        Sets which messages from the PyMAPDL Logger are printed to the console.

        - ``'DEBUG'`` - Prints all PyMAPDL logs
        - ``'INFO'`` - Informational messages only
        - ``'WARNING'`` - Messages containing ANSYS warnings
        - ``'ERROR'`` - Error messages only

        Defaults to ``'ERROR'``.

    log_apdl : Optional[str]
        Enables logging of every APDL command to a file. This can be used
        to "record" all the commands that are sent to MAPDL via PyMAPDL.
        This argument is the path of the output file (e.g.
        ``log_apdl='pymapdl_log.txt'``), or a boolean value. If it is
        :class:`True`, the file will be created in the current working
        directory with the name ``"apdl.log"``.
        Defaults to :class:`None` (disabled).

    print_com : bool
        Print the command ``/COM`` arguments to the standard output.
        Defaults to :class:`False`.

    mapdl_output : Optional[str]
        Redirect the MAPDL console output to a file. This is useful to check
        the MAPDL output in case of errors. The file is created in the working
        directory unless the path is included in the filename. If the file
        already exists, it will be overwritten.
        Defaults to :class:`None` (output not redirected).

    transport_mode : Optional[str]
        Transport mode for gRPC channel creation. Supported modes are:
        ``'insecure'``, ``'uds'``, ``'wnua'``, ``'mtls'``.
        Defaults to :class:`None`, which selects the appropriate mode based
        on platform and environment variables.

    uds_dir : Optional[str]
        Directory for Unix Domain Socket (UDS) files when using ``'uds'``
        transport. Defaults to :class:`None`, which uses ``~/.conn``.

    uds_id : Optional[str]
        Identifier for UDS socket file when using ``'uds'`` transport.
        Defaults to :class:`None`, which uses ``mapdl-{port}``.

    certs_dir : Optional[str]
        Directory containing certificates for ``'mtls'`` transport.
        Defaults to :class:`None`.

    add_env_vars : Optional[Dict[str, str]]
        Environment variables to add to the MAPDL process.
        Extends system environment variables.
        Defaults to :class:`None`.

    replace_env_vars : Optional[Dict[str, str]]
        Environment variables to replace system ones.

        .. warning:: Use with caution.
           Replaces ALL system environment variables including MPI and
           license-related ones. Manually inject them if needed.

        Defaults to :class:`None` (uses system environment).

    license_server_check : bool
        Check if the license server is available if MAPDL fails to start.
        Only available on ``mode='grpc'``. Defaults to :class:`False`.

    force_intel : bool
        Forces the use of Intel MPI in versions between ANSYS 2021R0 and 2022R2.
        *(Development use only)*. Defaults to :class:`False`.

    graphics_backend : Optional[str]
        Graphics backend to use. Defaults to :class:`None`.

    start_timeout : Optional[int]
        **Deprecated. Use ``timeout`` instead.**
        This parameter is maintained for backward compatibility and will be
        removed in a future version.

    **kwargs : Any
        Additional arguments. Unknown arguments are ignored with a warning.

    Returns
    -------
    LaunchConfig
        Complete, validated ``LaunchConfig`` object ready for launching MAPDL.

    Raises
    ------
    ConfigurationError
        If the configuration is invalid or contains conflicting settings.

    Examples
    --------
    Create a basic configuration for a local launch:

    >>> config = resolve_launch_config(nproc=4, version=222)
    >>> config.nproc
    4
    >>> config.version
    222

    Create a configuration for connecting to an existing instance:

    >>> config = resolve_launch_config(
    ...     start_instance=False,
    ...     ip="192.168.1.100",
    ...     port=50053
    ... )
    >>> config.ip
    '192.168.1.100'

    Create a configuration for HPC launch:

    >>> config = resolve_launch_config(
    ...     launch_on_hpc=True,
    ...     nproc=16,
    ...     scheduler_options={"nodes": "2", "ntasks-per-node": "8"}
    ... )
    >>> config.launch_on_hpc
    True
    """
    import warnings

    # Handle deprecated start_timeout parameter
    if start_timeout is not None:
        warnings.warn(
            "The 'start_timeout' parameter is deprecated and will be removed in a future version. "
            "Use 'timeout' instead.",
            DeprecationWarning,
            stacklevel=3,
        )
        # Use start_timeout if timeout is not explicitly provided
        if timeout is None:
            timeout = start_timeout

    # Resolve scheduler_options (validates that nproc is set when scheduler_options given)
    resolved_scheduler_options = resolve_scheduler_options(scheduler_options, nproc)

    # Resolve channel (validates mutual exclusivity with port/ip)
    resolved_channel = resolve_channel(channel, port, ip)

    # When a channel is provided, force start_instance=False and skip
    # exec_file auto-detection (no local process is needed).
    if resolved_channel is not None:
        start_instance = False

    # Resolve start_instance first (affects other resolution)
    resolved_start_instance = resolve_start_instance(
        start_instance, ip, launch_on_hpc=launch_on_hpc
    )

    # Resolve version early (needed for mode resolution)
    resolved_exec_file = resolve_exec_file(
        exec_file, version, resolved_start_instance, launch_on_hpc=launch_on_hpc
    )
    resolved_version = resolve_version(version, resolved_exec_file)

    # Resolve core parameters
    resolved_run_location = resolve_run_location(run_location)
    resolved_port = resolve_port(port)
    resolved_ip = resolve_ip(ip, resolved_start_instance, launch_on_hpc=launch_on_hpc)
    resolved_mode = resolve_mode(mode, resolved_version)
    resolved_nproc = resolve_nproc(nproc)

    # Resolve resource parameters
    resolved_ram = resolve_ram(ram)
    resolved_timeout = resolve_timeout(timeout, launch_on_hpc)

    # Resolve transport mode
    resolved_transport_mode = resolve_transport_mode(transport_mode)

    # Resolve additional switches (explicit arg or PYMAPDL_ADDITIONAL_SWITCHES env var)
    resolved_additional_switches = resolve_additional_switches(additional_switches)

    # Resolve environment variables — keep the two modes separate so
    # prepare_environment can decide whether to extend or replace.
    resolved_replace_env_vars: Dict[str, str] = {}
    resolved_add_env_vars: Dict[str, str] = {}
    if replace_env_vars is not None:
        resolved_replace_env_vars = dict(replace_env_vars)
    elif add_env_vars is not None:
        resolved_add_env_vars = dict(add_env_vars)

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
        additional_switches=resolved_additional_switches,
        license_type=license_type,
        launch_on_hpc=launch_on_hpc,
        running_on_hpc=running_on_hpc,
        scheduler_options=resolved_scheduler_options,
        loglevel=loglevel,
        log_apdl=log_apdl,
        print_com=print_com,
        mapdl_output=mapdl_output,
        transport_mode=resolved_transport_mode,
        uds_dir=uds_dir,
        uds_id=uds_id,
        certs_dir=certs_dir,
        env_vars=resolved_replace_env_vars,
        add_env_vars=resolved_add_env_vars,
        license_server_check=license_server_check,
        force_intel=force_intel,
        graphics_backend=graphics_backend,
        channel=resolved_channel,
    )


def resolve_scheduler_options(
    scheduler_options: Optional[Dict[str, Any]],
    nproc: Optional[int],
) -> Optional[Dict[str, Any]]:
    """Resolve and validate HPC scheduler options.

    When ``scheduler_options`` is provided, ``nproc`` must also be explicitly
    set because PyMAPDL does not infer the number of cores from the scheduler
    options dict.

    Parameters
    ----------
    scheduler_options : Optional[Dict[str, Any]]
        HPC scheduler options passed by the caller.
    nproc : Optional[int]
        Explicit number of processors passed by the caller (before resolution).

    Returns
    -------
    Optional[Dict[str, Any]]
        The scheduler options unchanged.

    Raises
    ------
    ConfigurationError
        If ``scheduler_options`` is provided without ``nproc``.
    """
    if scheduler_options and nproc is None:
        raise ConfigurationError(
            "PyMAPDL does not read the number of cores from the 'scheduler_options'. "
            "Hence you need to specify the number of cores you want to use using "
            "the argument 'nproc' in 'launch_mapdl'."
        )
    return scheduler_options


def resolve_channel(
    channel: Optional[Any],
    port: Optional[int],
    ip: Optional[str],
) -> Optional[Any]:
    """Resolve and validate the optional gRPC channel argument.

    A pre-built gRPC channel is mutually exclusive with ``port`` and ``ip``
    because those parameters are used to *construct* a channel internally.
    Providing both would be ambiguous.

    Parameters
    ----------
    channel : Optional[Any]
        Pre-built gRPC channel to reuse, or ``None``.
    port : Optional[int]
        Explicit port argument passed by the caller.
    ip : Optional[str]
        Explicit IP argument passed by the caller.

    Returns
    -------
    Optional[Any]
        The channel unchanged, or ``None`` if not provided.

    Raises
    ------
    ConfigurationError
        If ``channel`` is combined with ``port`` or ``ip``.
    """
    if channel is not None and (port is not None or ip is not None):
        raise ConfigurationError(
            "'channel' cannot be used together with 'port' or 'ip'."
        )
    return channel


def resolve_exec_file(
    exec_file: Optional[str],
    version: Optional[int],
    start_instance: bool,
    launch_on_hpc: bool = False,
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
    # Cannot specify both exec_file and version simultaneously
    if exec_file and version:
        raise ConfigurationError("Cannot specify both 'exec_file' and 'version'.")

    # If not starting instance, exec_file not needed
    if not start_instance:
        return exec_file or ""

    # Priority 1: Explicit argument
    if exec_file:
        if not os.path.isfile(exec_file):
            if launch_on_hpc:
                # For HPC launches the executable lives on the remote cluster, not
                # locally.  Emit a warning so the caller is aware, but do NOT raise.
                import warnings as _warnings

                _warnings.warn(
                    f"PyMAPDL could not find the ANSYS executable at '{exec_file}'. "
                    "This is acceptable for HPC launches where the executable resides "
                    "on the remote cluster.",
                    UserWarning,
                    stacklevel=6,
                )
                return exec_file
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
        if not isinstance(port, int):
            try:
                port = int(port)
            except (TypeError, ValueError):
                raise ConfigurationError(
                    f"Invalid port: {port!r}. Port must be an integer between 1 and 65535."
                )
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


def resolve_ip(
    ip: Optional[str],
    start_instance: bool,
    launch_on_hpc: bool = False,
) -> str:
    """Resolve IP address.

    Resolution order:
    1. Explicit ip argument
    2. PYMAPDL_IP environment variable
    3. WSL host detection (if on WSL)
    4. Localhost (127.0.0.1)

    Parameters:
        ip: Explicit IP address
        start_instance: Whether starting new instance
        launch_on_hpc: Whether launching on an HPC cluster

    Returns:
        IP address

    Raises:
        ConfigurationError: If IP is invalid, conflicts with HPC launch, or cannot be resolved
    """
    import socket

    # Cannot specify a non-local IP when launching on HPC
    if launch_on_hpc and ip and ip not in ("127.0.0.1", "localhost"):
        raise ConfigurationError(
            "PyMAPDL cannot ensure a specific IP will be used when launching "
            "MAPDL on a cluster. Please remove the 'ip' argument."
        )

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
            # Hostname cannot be resolved at configuration time (e.g. Docker
            # service name before the container is fully registered in DNS).
            # Return as-is so the gRPC layer can attempt DNS resolution when
            # the connection is actually made.
            LOG.warning(
                f"Cannot resolve hostname from PYMAPDL_IP: '{env_ip}'. "
                "Using it as-is; DNS resolution will be attempted at connection time."
            )
            return env_ip

    # Priority 3: WSL host detection
    from .environment import get_windows_host_ip, is_wsl

    if is_wsl() and start_instance:
        wsl_ip = get_windows_host_ip()
        if wsl_ip:
            LOG.debug(f"On WSL: Using Windows host IP: {wsl_ip}")
            return wsl_ip
        else:
            LOG.warning(
                "Running on WSL but cannot determine Windows host IP address. "
                "Falling back to localhost. If you need the Windows host IP, "
                "please specify the 'ip' argument explicitly."
            )
            return LOCALHOST

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


def resolve_start_instance(
    start_instance: Optional[bool],
    ip: Optional[str],
    launch_on_hpc: bool = False,
) -> bool:
    """Resolve whether to start new instance.

    Resolution order:
    1. Explicit start_instance argument
    2. PYMAPDL_START_INSTANCE environment variable
    3. Infer from ip argument or PYMAPDL_IP environment variable (default False)
    4. Default: True

    When ``launch_on_hpc=True`` the ``start_instance=True`` + ``ip`` combination
    is permitted because the instance is launched on the remote cluster, not
    locally.

    Parameters:
        start_instance: Explicit start instance flag
        ip: IP address (affects inference when no explicit flag or env var)
        launch_on_hpc: Whether launching via HPC scheduler

    Returns:
        Whether to start new instance
    """
    import warnings as _warnings

    # Priority 1: Explicit argument
    if start_instance is not None:
        # Cannot start a local instance while also targeting a remote IP —
        # unless we are launching on HPC where MAPDL starts on a cluster node.
        if start_instance is True and ip and not launch_on_hpc:
            raise ConfigurationError(
                "When providing a value for the argument 'ip', the argument "
                "'start_instance' must be False or None. "
                "Cannot start a local MAPDL instance while also specifying a remote IP."
            )
        if ip is not None:
            LOG.warning(
                "Both start_instance and ip are specified. start_instance will take precedence."
            )
        # Warn when explicit start_instance=True conflicts with the env var
        if start_instance is True:
            env_start = os.getenv("PYMAPDL_START_INSTANCE", "").strip().lower()
            if env_start:
                _warnings.warn(
                    f"Both 'start_instance=True' argument and "
                    f"PYMAPDL_START_INSTANCE='{env_start}' environment variable are set. "
                    "The explicit argument takes precedence.",
                    UserWarning,
                    stacklevel=5,
                )
        return start_instance

    # Priority 2: PYMAPDL_START_INSTANCE environment variable.
    # This takes precedence over IP-based inference so that explicitly setting
    # PYMAPDL_START_INSTANCE=True is not silently overridden when PYMAPDL_IP is
    # also present in the environment.
    env_start = os.getenv("PYMAPDL_START_INSTANCE", "").strip().lower()
    if env_start:
        if env_start in ("true", "1", "yes"):
            LOG.debug("Using start_instance=True from PYMAPDL_START_INSTANCE env var")
            return True
        elif env_start in ("false", "0", "no"):
            LOG.debug("Using start_instance=False from PYMAPDL_START_INSTANCE env var")
            return False

    # Priority 3: Infer from explicit ip argument or PYMAPDL_IP env var.
    env_ip = os.getenv("PYMAPDL_IP", "").strip()
    if ip or env_ip:
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


def _shares_substring(a: str, b: str, min_len: int = 4) -> bool:
    """Return True if *a* and *b* share any common substring of length >= *min_len*."""
    for i in range(len(a) - min_len + 1):
        token = a[i : i + min_len]
        if token in b:
            return True
    return False


def resolve_additional_switches(additional_switches: str) -> str:
    """Resolve additional MAPDL command line switches.

    Resolution order:
    1. Explicit ``additional_switches`` argument (if non-empty)
    2. ``PYMAPDL_ADDITIONAL_SWITCHES`` environment variable
    3. Default: empty string

    When both the explicit argument and ``PYMAPDL_ADDITIONAL_SWITCHES`` are
    provided, a general warning is issued.  If the two strings also share a
    common substring of at least 4 characters, an additional warning is raised
    to alert the user about possible duplicated or contradicting switches.

    Parameters
    ----------
    additional_switches : str
        Explicit additional switches string.

    Returns
    -------
    str
        Resolved additional switches string.
    """
    # Priority 1: Explicit argument
    if additional_switches:
        env_switches = os.environ.get("PYMAPDL_ADDITIONAL_SWITCHES")
        if env_switches:
            LOG.warning(
                "Skipping injecting additional switches from env var because the "
                "'additional_switches' argument is already set."
            )
            if _shares_substring(additional_switches, env_switches):
                LOG.warning(
                    "The 'additional_switches' argument and the "
                    "'PYMAPDL_ADDITIONAL_SWITCHES' environment variable share "
                    "common substrings. The environment variable might be "
                    "injecting duplicated or contradicting switches."
                )

        return additional_switches

    # Priority 2: Environment variable
    env_switches = os.environ.get("PYMAPDL_ADDITIONAL_SWITCHES")
    if env_switches:
        LOG.debug(
            f"Injecting additional switches from 'PYMAPDL_ADDITIONAL_SWITCHES' env var: "
            f"{env_switches}"
        )
        return env_switches

    # Priority 3: Default
    return additional_switches
