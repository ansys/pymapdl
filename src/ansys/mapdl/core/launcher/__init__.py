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

"""MAPDL Launcher - Domain-Driven Architecture.

This module provides the main entry point for launching or connecting
to MAPDL instances. It orchestrates configuration resolution, validation,
process launching, and client creation.

Architecture:
    - models: Data structures
    - config: Configuration resolution
    - validation: Input validation
    - environment: Platform detection and setup
    - network: Port management
    - process: Process lifecycle
    - hpc: HPC cluster integration
    - connection: Client connection

Public API:
    - launch_mapdl: Main entry point
    - launch_mapdl_process: Launch MAPDL process only
    - LaunchConfig: Configuration model (for advanced use)
"""

import os
import platform
from typing import TYPE_CHECKING, Any, Dict, Optional, Union

from ansys.mapdl.core import LOG

from .config import LOCALHOST, MAPDL_DEFAULT_PORT, resolve_launch_config  # noqa: F401
from .connection import (
    connect_to_existing,
    create_console_client,
    create_grpc_client,
)
from .connection import close_all_local_instances  # noqa: F401
from .environment import prepare_environment
from .errors import ConfigurationError, LaunchError
from .hpc import (
    detect_slurm_environment,
)
from .hpc import (
    resolve_slurm_resources,
)
from .hpc import launch_on_hpc as _launch_on_hpc_fn
from .models import LaunchConfig, LaunchMode, TransportMode
from .process import _create_queue_for_std
from .process import launch_mapdl_process as _launch_mapdl_process
from .validation import validate_config

if TYPE_CHECKING:
    from ansys.mapdl.core.mapdl_console import MapdlConsole
    from ansys.mapdl.core.mapdl_grpc import MapdlGrpc

__all__ = [
    "launch_mapdl",
    "launch_mapdl_process",
    "LaunchConfig",
    "ConfigurationError",
    "LaunchError",
    "LOCALHOST",
    "generate_start_parameters",
    "_create_queue_for_std",
]


def generate_start_parameters(kwargs: dict) -> dict:
    """Generate start parameters dict (backward compatibility shim)."""
    return {k: v for k, v in kwargs.items()}


def _launch_mapdl_common(
    exec_file: Optional[str],
    run_location: Optional[str],
    jobname: str,
    nproc: Optional[int],
    port: Optional[int],
    ip: Optional[str],
    mode: Optional[str],
    version: Optional[int],
    start_instance: Optional[bool],
    ram: Optional[int],
    timeout: Optional[int],
    cleanup_on_exit: bool,
    clear_on_connect: bool,
    override: bool,
    remove_temp_dir_on_exit: bool,
    set_no_abort: bool,
    additional_switches: str,
    license_type: Optional[str],
    launch_on_hpc: bool,
    running_on_hpc: bool,
    scheduler_options: Optional[Dict[str, Any]],
    loglevel: str,
    log_apdl: Optional[str],
    print_com: bool,
    mapdl_output: Optional[str],
    transport_mode: Optional[str],
    uds_dir: Optional[str],
    uds_id: Optional[str],
    certs_dir: Optional[str],
    add_env_vars: Optional[Dict[str, str]],
    replace_env_vars: Optional[Dict[str, str]],
    license_server_check: bool,
    force_intel: bool,
    graphics_backend: Optional[str],
    start_timeout: Optional[int],
    channel: Optional[Any] = None,
):
    """Common logic for launch_mapdl and launch_mapdl_process.

    Returns:
        Tuple of (config, process_info) where process_info is None if not launching a new instance
    """
    # Step 1: Resolve configuration from arguments, env vars, and defaults
    try:
        config = resolve_launch_config(
            exec_file=exec_file,
            run_location=run_location,
            jobname=jobname,
            nproc=nproc,
            port=port,
            ip=ip,
            mode=mode,
            version=version,
            start_instance=start_instance,
            ram=ram,
            timeout=timeout,
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
            transport_mode=transport_mode,
            uds_dir=uds_dir,
            uds_id=uds_id,
            certs_dir=certs_dir,
            add_env_vars=add_env_vars,
            replace_env_vars=replace_env_vars,
            license_server_check=license_server_check,
            force_intel=force_intel,
            graphics_backend=graphics_backend,
            start_timeout=start_timeout,
            channel=channel,
        )
    except ConfigurationError as e:
        LOG.error(f"Configuration error: {e}")
        raise LaunchError(f"Invalid launch configuration: {e}") from e

    # Step 2: Validate configuration
    try:
        validation_result = validate_config(config)
        if not validation_result.valid:
            error_header = "Configuration validation failed with the following errors:"
            formatted_errors = [f"- {err}" for err in validation_result.errors]
            error_body = "\n".join(formatted_errors)
            full_message = (
                f"{error_header}\n{error_body}" if formatted_errors else error_header
            )
            LOG.error(full_message)
            raise LaunchError(full_message)

        # Log warnings
        for warning in validation_result.warnings:
            LOG.warning(warning)

    except LaunchError:
        raise
    except Exception as e:
        LOG.error(f"Validation error: {e}")
        raise LaunchError(f"Configuration validation error: {e}") from e

    # Step 3: Handle connection to existing instance (if applicable)
    if not config.start_instance:
        return config, None

    # Step 4: Prepare environment
    try:
        env_config = prepare_environment(config)
        process_env = env_config.variables
    except Exception as e:
        LOG.error(f"Environment preparation failed: {e}")
        raise LaunchError(f"Failed to prepare environment: {e}") from e

    # For UDS transport (Linux default), tell MAPDL which directory to
    # create its socket in via ANSYS_MAPDL_UDS_PATH.  MAPDL always names
    # the socket "mapdl-{PORT}.sock" inside that directory.
    if (
        platform.system() == "Linux"
        and config.transport_mode == TransportMode.UDS
        and config.uds_dir
    ):
        os.makedirs(config.uds_dir, exist_ok=True)
        process_env.setdefault("ANSYS_MAPDL_UDS_PATH", str(config.uds_dir))
        LOG.debug(f"UDS transport: setting ANSYS_MAPDL_UDS_PATH={config.uds_dir}")

    # Step 5: Launch MAPDL process (local or HPC)
    process_info = None
    try:
        if config.launch_on_hpc:
            # Resolve SLURM resources if available
            if detect_slurm_environment():
                config = resolve_slurm_resources(config)

            # Launch on HPC
            LOG.info("Launching MAPDL on HPC cluster...")
            process_info = _launch_on_hpc_fn(config, process_env)
        else:
            # Launch locally
            LOG.info("Launching MAPDL locally...")
            process_info = _launch_mapdl_process(config, process_env)

    except Exception as e:
        LOG.error(f"Process launch failed: {e}")
        raise LaunchError(f"Failed to launch MAPDL: {e}") from e

    return config, process_info


def launch_mapdl(
    exec_file: Optional[str] = None,
    run_location: Optional[str] = None,
    jobname: str = "file",
    *,
    nproc: Optional[int] = None,
    port: Optional[int] = None,
    ip: Optional[str] = None,
    channel: Optional[Any] = None,
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
    **kwargs: Any,
) -> Union["MapdlGrpc", "MapdlConsole"]:
    """Launch MAPDL or connect to existing instance.

    This is the main entry point for all MAPDL launching operations.
    It uses the domain-driven modular architecture while maintaining
    100% backward compatibility with the legacy launcher API.

    When ``start_instance=True`` (the default), this function launches a
    new MAPDL instance and returns a client for interacting with it.
    When ``start_instance=False``, this function connects to an existing
    MAPDL instance running at the specified ``ip`` and ``port``.

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
        Defaults to a temporary working directory with name ``'ansys_'`` and
        a random string. The temporary directory is removed when MAPDL exits
        if ``cleanup_on_exit`` is :class:`True`.

    jobname : str
        MAPDL jobname. Defaults to ``'file'``.

    nproc : Optional[int]
        Number of processors. If running on an HPC cluster, this value is
        adjusted to the number of CPUs allocated to the job, unless
        ``running_on_hpc=False``. Defaults to ``2`` CPUs.

    port : Optional[int]
        Port to launch MAPDL gRPC on. Can also be set via environment variable
        :envvar:`PYMAPDL_PORT`. Argument has precedence. Defaults to ``50052``.

    ip : Optional[str]
        IP address of MAPDL instance. Used only when ``start_instance=False``.
        Can also be set via environment variable :envvar:`PYMAPDL_IP`.
        Defaults to ``'127.0.0.1'`` (localhost).

    channel : Optional[Any]
        Communication channel to use. It cannot be used with `ip` and `port` arguments.

    mode : Optional[str]
        Launch mode. Must be one of:

        - ``'grpc'`` - Recommended for ANSYS 2021R1 or newer
        - ``'console'`` - Legacy console mode, Linux only, not recommended

        The gRPC mode provides the best performance and stability.

    version : Optional[int]
        MAPDL version to launch. Can be provided as integers (``version=222``)
        or floats (``version=22.2``). Can also be set via environment variable
        :envvar:`PYMAPDL_MAPDL_VERSION`. Defaults to latest installed version.

    start_instance : Optional[bool]
        When :class:`False`, connect to existing MAPDL at ``ip`` and ``port``.
        When :class:`True`, launch a new MAPDL instance locally.
        Can also be set via environment variable :envvar:`PYMAPDL_START_INSTANCE`.
        Defaults to start locally (:class:`True`).

    ram : Optional[int]
        Total workspace (memory) in megabytes for initial allocation.
        Specify a negative number to force a fixed size throughout the run.
        Defaults to :class:`None` (2048 MB).

    timeout : Optional[int]
        Maximum time to connect to MAPDL server in seconds.
        Defaults to 45 seconds (90 seconds if running on HPC).

    cleanup_on_exit : bool
        Exit MAPDL when Python exits or MAPDL instance is garbage collected.
        Defaults to :class:`True`.

    clear_on_connect : bool
        Provide a fresh environment when connecting to MAPDL.
        Defaults to :class:`True`.

    override : bool
        Delete the lock file at ``run_location`` if it exists.
        Useful when a prior session exited prematurely.
        Defaults to :class:`False`.

    remove_temp_dir_on_exit : bool
        Delete temporary directory created for MAPDL launch when exiting.
        Defaults to :class:`False`. Note: Not available on HPC.

    set_no_abort : bool
        Set MAPDL to not abort at first error in /BATCH mode.
        *(Development use only)*. Defaults to :class:`True`.

    additional_switches : str
        Additional MAPDL command-line switches. For example, ``'-aa_r'`` for
        academic research license. Avoid switches like ``-i``, ``-o``, ``-b``
        as they are already set. Common switches include:

        - ``'-smp'`` - Shared-memory parallelism
        - ``'-dmp'`` - Distributed-memory parallelism
        - ``'-mpi intelmpi'`` - Specify Intel MPI
        - ``'-mpi msmpi'`` - Specify Microsoft MPI
        - ``'-acc gpu'`` - GPU acceleration
        - ``'-amfg'`` - Additive manufacturing capability

        Defaults to empty string.

    license_type : Optional[str]
        License type to request. Can be a license name (e.g., ``'meba'``,
        ``'ansys'``) or description (e.g., "enterprise solver").
        Legacy licenses (e.g., ``'aa_t_a'``) are supported but may raise warnings.
        Defaults to :class:`None` (server decides).

    launch_on_hpc : bool
        Launch on HPC cluster using SLURM scheduler (SLURM only).
        Pass ``scheduler_options`` to specify scheduler arguments.
        Defaults to :class:`False`.

    running_on_hpc : bool
        Whether to detect if PyMAPDL is running on an HPC cluster.
        Currently only SLURM is supported.
        Can be overridden via :envvar:`PYMAPDL_RUNNING_ON_HPC`.
        Defaults to :class:`False`.

    scheduler_options : Optional[Dict[str, Any]]
        HPC scheduler options as dictionary or string.
        Example: ``{"nodes": "2", "ntasks-per-node": "8"}``

    loglevel : str
        PyMAPDL logging level. Options:

        - ``'DEBUG'`` - All logs
        - ``'INFO'`` - Informational
        - ``'WARNING'`` - Warnings only
        - ``'ERROR'`` - Errors only

        Defaults to ``'ERROR'``.

    log_apdl : Optional[str]
        Log APDL commands to file. Path to output file (e.g.,
        ``'pymapdl_log.txt'``) or :class:`True` to use ``'apdl.log'``.
        Useful for recording commands to replay in MAPDL without PyMAPDL.
        Defaults to :class:`None` (disabled).

    print_com : bool
        Print ``/COM`` command arguments to console output.
        Defaults to :class:`False`.

    mapdl_output : Optional[str]
        Redirect MAPDL console output to file. Useful for debugging.
        Overwritten if file exists. Can include path.
        Defaults to :class:`None` (not redirected).

    transport_mode : Optional[str]
        gRPC transport mode. Options: ``'insecure'``, ``'uds'``,
        ``'wnua'``, ``'mtls'``.
        Defaults to :class:`None` (auto-select based on platform).

    uds_dir : Optional[str]
        Directory for Unix Domain Socket (UDS) files with ``'uds'`` transport.
        Defaults to :class:`None` (uses ``~/.conn``).

    uds_id : Optional[str]
        Identifier for UDS socket file with ``'uds'`` transport.
        Defaults to :class:`None` (uses ``mapdl-{port}``).

    certs_dir : Optional[str]
        Directory containing certificates for ``'mtls'`` transport.
        Defaults to :class:`None`.

    add_env_vars : Optional[Dict[str, str]]
        Environment variables to add to MAPDL process.
        Extends system environment variables.
        Defaults to :class:`None`.

    replace_env_vars : Optional[Dict[str, str]]
        Environment variables to replace system ones.

        .. warning:: Use with caution.
           Replaces ALL system environment variables including MPI and
           license-related ones. Manually inject them if needed.

        Defaults to :class:`None` (uses system environment).

    license_server_check : bool
        Check if license server is available if MAPDL fails to start.
        Only on ``mode='grpc'``. Defaults to :class:`False`.

    force_intel : bool
        Force Intel MPI in ANSYS versions 2021R0-2022R2.
        *(Development use only)*. Defaults to :class:`False`.

    graphics_backend : Optional[str]
        Graphics backend to use. Defaults to :class:`None`.

    start_timeout : Optional[int]
        **Deprecated. Use ``timeout`` instead.**
        Maintained for backward compatibility, will be removed in future version.

    **kwargs : Any
        Additional arguments. Unknown arguments generate warnings.

    Returns
    -------
    Union[MapdlGrpc, MapdlConsole]
        MAPDL client instance for interaction. Type depends on ``mode``.

    Raises
    ------
    ConfigurationError
        Invalid configuration or conflicting settings.
    LaunchError
        Launch failed or MAPDL failed to start.
    ConnectionError
        Cannot connect to existing MAPDL instance.

    Examples
    --------
    Launch MAPDL using recommended settings:

    >>> from ansys.mapdl.core import launch_mapdl
    >>> mapdl = launch_mapdl()

    Launch with specific version and processor count:

    >>> mapdl = launch_mapdl(version=222, nproc=4)

    Run with shared-memory parallelism at specific location:

    >>> exec_file = 'C:/Program Files/ANSYS Inc/v252/ansys/bin/winx64/ANSYS252.exe'
    >>> mapdl = launch_mapdl(
    ...     exec_file=exec_file,
    ...     additional_switches='-smp'
    ... )

    Connect to an existing MAPDL instance:

    >>> mapdl = launch_mapdl(
    ...     start_instance=False,
    ...     ip='192.168.1.30',
    ...     port=50001
    ... )

    Run MAPDL in console mode (Linux only, not recommended):

    >>> mapdl = launch_mapdl(
    ...     '/ansys_inc/v194/ansys/bin/ansys194',
    ...     mode='console'
    ... )

    Launch with custom environment variables:

    >>> my_env = {"MY_VAR": "true", "ANSYS_LOCK": "FALSE"}
    >>> mapdl = launch_mapdl(add_env_vars=my_env)

    Launch on HPC with SLURM options:

    >>> mapdl = launch_mapdl(
    ...     launch_on_hpc=True,
    ...     nproc=16,
    ...     scheduler_options={'nodes': '2', 'ntasks-per-node': '8'}
    ... )

    Notes
    -----

    **Ansys Student Version**

    If an Ansys Student version is detected, PyMAPDL automatically
    launches MAPDL in shared-memory parallelism (SMP) mode unless
    another option is specified.

    **Additional Switches**

    Commonly used MAPDL switches (as of ANSYS 2020R2+):

    ``-acc <device>``
        Enable GPU hardware acceleration. See GPU Accelerator Capability
        in the Parallel Processing Guide.

    ``-amfg``
        Enable additive manufacturing. Requires appropriate license.

    ``-ansexe <executable>``
        Activate a custom mechanical APDL executable.

    ``-db value``
        Initial memory allocation. Default is 1024 MB.
        Negative number forces fixed size throughout run.

    ``-dis``
        Enable Distributed ANSYS. See Parallel Processing Guide.

    ``-dvt``
        Enable ANSYS DesignXplorer advanced task (requires DesignXplorer).

    ``-l <language>``
        Specify language file for non-English localization.

    ``-m <workspace>``
        Total workspace size in MB. Default is 2048 MB.
        Negative number forces fixed size throughout run.

    ``-machines <IP>``
        Distributed machines for Distributed ANSYS analysis.

    ``-mpi <value>``
        MPI type: ``intelmpi``, ``msmpi``, ``openmpi``, etc.

    ``-mpifile <appfile>``
        Existing MPI file for Distributed ANSYS.

    ``-na <value>``
        Number of GPU accelerator devices per machine/node.

    ``-name <value>``
        Define APDL parameters at startup.

    ``-p <productname>``
        ANSYS session product (e.g., ``'meba'``, ``'ansys'``).

    ``-ppf <license_feature>``
        HPC license feature. See HPC Licensing in Parallel Processing Guide.

    ``-smp``
        Enable shared-memory parallelism.

    **PyPIM Integration**

    If the environment is configured for `PyPIM
    <https://pypim.docs.pyansys.com>`_ and ``start_instance=True``,
    MAPDL startup is delegated to PyPIM and most launch options are ignored.

    **Architecture**

    This implementation uses the domain-driven modular architecture:

    - **Configuration resolution** (``config.resolve_launch_config()``)
    - **Validation** (``validation.validate_config()``)
    - **Environment setup** (``environment.prepare_environment()``)
    - **Process launching**:

      - Local: ``process.launch_mapdl_process()``
      - HPC: ``hpc.launch_on_hpc()``

    - **Client creation**:

      - gRPC: ``connection.create_grpc_client()``
      - Console: ``connection.create_console_client()``
    """
    import warnings

    # Warn about any remaining unknown keyword arguments
    if kwargs:
        warnings.warn(
            f"Unknown arguments ignored: {list(kwargs.keys())}",
            stacklevel=3,
        )

    config, process_info = _launch_mapdl_common(
        exec_file=exec_file,
        run_location=run_location,
        jobname=jobname,
        nproc=nproc,
        port=port,
        ip=ip,
        mode=mode,
        version=version,
        start_instance=start_instance,
        ram=ram,
        timeout=timeout,
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
        transport_mode=transport_mode,
        uds_dir=uds_dir,
        uds_id=uds_id,
        certs_dir=certs_dir,
        add_env_vars=add_env_vars,
        replace_env_vars=replace_env_vars,
        license_server_check=license_server_check,
        force_intel=force_intel,
        graphics_backend=graphics_backend,
        start_timeout=start_timeout,
        channel=channel,
    )

    # Handle connection to existing instance
    if process_info is None:
        LOG.info(f"Connecting to existing MAPDL instance at {config.ip}:{config.port}")
        try:
            return connect_to_existing(config)
        except Exception as e:
            LOG.error(f"Failed to connect to existing instance: {e}")
            raise

    # Create and return client
    try:
        if config.mode == LaunchMode.CONSOLE:
            LOG.debug("Creating MapdlConsole client")
            return create_console_client(config)
        else:
            LOG.debug("Creating MapdlGrpc client")
            return create_grpc_client(config, process_info)
    except Exception as e:
        LOG.error(f"Client creation failed: {e}")
        raise LaunchError(f"Failed to create MAPDL client: {e}") from e


def launch_mapdl_process(
    exec_file: Optional[str] = None,
    run_location: Optional[str] = None,
    jobname: str = "file",
    *,
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
    **kwargs: Any,
) -> tuple[str, int, Optional[int]]:
    """Launch MAPDL process and return connection info without creating client.

    This is the specialized entry point for CLI and programmatic use cases that
    need the process to be launched without immediately creating a client
    connection. Unlike ``launch_mapdl()``, this function:

    - Does NOT connect to an existing instance
    - Returns connection info tuple ``(ip, port, pid)`` instead of a client
    - Does NOT create a client object
    - Requires ``start_instance=True``

    This function is primarily used by the CLI to launch MAPDL without
    creating a client connection. The caller is responsible for managing
    the launched process lifecycle.

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
        Defaults to a temporary working directory with name ``'ansys_'`` and
        a random string.

    jobname : str
        MAPDL jobname. Defaults to ``'file'``.

    nproc : Optional[int]
        Number of processors. If running on an HPC cluster, adjusted to
        allocated CPUs unless ``running_on_hpc=False``.
        Defaults to ``2`` CPUs.

    port : Optional[int]
        Port for MAPDL gRPC. Can be set via :envvar:`PYMAPDL_PORT`.
        Argument has precedence. Defaults to ``50052``.

    ip : Optional[str]
        IP address to bind MAPDL to. For HPC, typically left empty.
        Defaults to ``'127.0.0.1'``.

    mode : Optional[str]
        Launch mode. Options:

        - ``'grpc'`` - Recommended for ANSYS 2021R1 or newer
        - ``'console'`` - Legacy console mode, Linux only (not recommended)

        This parameter is largely ignored as gRPC is enforced.

    version : Optional[int]
        MAPDL version to launch. Can be provided as integers (``version=222``)
        or floats (``version=22.2``).
        Can be set via environment variable :envvar:`PYMAPDL_MAPDL_VERSION`.
        Defaults to latest installed version.

    start_instance : Optional[bool]
        **MUST be :class:`True` for this function.**
        This function always requires launching a new instance.
        Can be set via environment variable :envvar:`PYMAPDL_START_INSTANCE`.
        Defaults to :class:`True`.

    ram : Optional[int]
        Total workspace (memory) in megabytes. Negative number forces fixed size.
        Defaults to :class:`None` (2048 MB).

    timeout : Optional[int]
        Maximum time to connect to MAPDL server in seconds.
        Defaults to 45 seconds (90 seconds on HPC).

    cleanup_on_exit : bool
        Exit MAPDL when Python exits. Defaults to :class:`True`.

    clear_on_connect : bool
        Provide fresh environment when connecting. Defaults to :class:`True`.

    override : bool
        Delete lock file at ``run_location`` if it exists.
        Defaults to :class:`False`.

    remove_temp_dir_on_exit : bool
        Delete temporary directory when exiting.
        Defaults to :class:`False`. Not available on HPC.

    set_no_abort : bool
        Do not abort at first error in /BATCH mode.
        *(Development use only)*. Defaults to :class:`True`.

    additional_switches : str
        Additional MAPDL command-line switches. Avoid ``-i``, ``-o``, ``-b``.
        Examples: ``'-smp'``, ``'-dmp'``, ``'-mpi intelmpi'``.
        Defaults to empty string.

    license_type : Optional[str]
        License type to request (e.g., ``'meba'``, ``'ansys'``).
        Defaults to :class:`None` (server decides).

    launch_on_hpc : bool
        Launch on HPC cluster using SLURM scheduler.
        Defaults to :class:`False`.

    running_on_hpc : bool
        Whether to detect if running on HPC cluster.
        Can override with :envvar:`PYMAPDL_RUNNING_ON_HPC`.
        Defaults to :class:`False`.

    scheduler_options : Optional[Dict[str, Any]]
        HPC scheduler options. Example: ``{"nodes": "2", "ntasks-per-node": "8"}``

    loglevel : str
        PyMAPDL logging level: ``'DEBUG'``, ``'INFO'``, ``'WARNING'``, ``'ERROR'``.
        Defaults to ``'ERROR'``.

    log_apdl : Optional[str]
        Log APDL commands to file. Path or :class:`True` for ``'apdl.log'``.
        Defaults to :class:`None` (disabled).

    print_com : bool
        Print ``/COM`` command arguments. Defaults to :class:`False`.

    mapdl_output : Optional[str]
        Redirect MAPDL console output to file. Useful for debugging.
        Defaults to :class:`None` (not redirected).

    transport_mode : Optional[str]
        gRPC transport mode: ``'insecure'``, ``'uds'``, ``'wnua'``, ``'mtls'``.
        Defaults to :class:`None` (auto-select).

    uds_dir : Optional[str]
        Directory for Unix Domain Socket (UDS) files.
        Defaults to :class:`None` (``~/.conn``).

    uds_id : Optional[str]
        Identifier for UDS socket file. Defaults to :class:`None` (``mapdl-{port}``).

    certs_dir : Optional[str]
        Directory with certificates for ``'mtls'`` transport.
        Defaults to :class:`None`.

    add_env_vars : Optional[Dict[str, str]]
        Environment variables to add. Extends system environment.
        Defaults to :class:`None`.

    replace_env_vars : Optional[Dict[str, str]]
        Environment variables to replace system ones.

        .. warning:: Use with caution.
           Replaces ALL system environment variables including MPI and
           license-related ones. Manually inject if needed.

        Defaults to :class:`None` (uses system environment).

    license_server_check : bool
        Check license server availability on MAPDL startup failure.
        Only on ``mode='grpc'``. Defaults to :class:`False`.

    force_intel : bool
        Force Intel MPI for ANSYS 2021R0-2022R2.
        *(Development use only)*. Defaults to :class:`False`.

    graphics_backend : Optional[str]
        Graphics backend to use. Defaults to :class:`None`.

    start_timeout : Optional[int]
        **Deprecated. Use ``timeout`` instead.**

    **kwargs : Any
        Additional arguments. Unknown arguments generate warnings.

    Returns
    -------
    tuple[str, int, Optional[int]]
        Tuple of ``(ip, port, pid)`` for the launched MAPDL instance:

        - ``ip`` - IP address where MAPDL is listening
        - ``port`` - gRPC port number
        - ``pid`` - Process ID (or None for remote/HPC launches)

    Raises
    ------
    ConfigurationError
        Invalid configuration or conflicting settings.
    LaunchError
        Launch failed or MAPDL failed to start.

    Examples
    --------
    Launch MAPDL process and get connection info:

    >>> from ansys.mapdl.core.launcher import launch_mapdl_process
    >>> ip, port, pid = launch_mapdl_process(nproc=4)
    >>> print(f"MAPDL listening at {ip}:{port} (PID: {pid})")
    MAPDL listening at 127.0.0.1:50052 (PID: 12345)

    Use with specific version and switches:

    >>> ip, port, pid = launch_mapdl_process(
    ...     version=222,
    ...     nproc=4,
    ...     additional_switches='-smp'
    ... )

    Launch on HPC and get connection info:

    >>> ip, port, pid = launch_mapdl_process(
    ...     launch_on_hpc=True,
    ...     nproc=16,
    ...     scheduler_options={'nodes': '2', 'ntasks-per-node': '8'}
    ... )

    Notes
    -----
    This function is primarily used by the CLI to launch MAPDL without
    creating a client connection. The caller is responsible for:

    - Managing the launched process
    - Creating a client connection if needed
    - Cleaning up resources

    For most use cases, ``launch_mapdl()`` is recommended as it automatically
    creates and manages the client connection.

    **Example CLI workflow:**

    >>> ip, port, pid = launch_mapdl_process(nproc=8)
    >>> # Pass connection info to other processes or store it
    >>> # When ready to connect:
    >>> from ansys.mapdl.core import launch_mapdl
    >>> mapdl = launch_mapdl(start_instance=False, ip=ip, port=port)
    """
    import warnings

    if kwargs:
        warnings.warn(
            f"Unknown arguments ignored: {list(kwargs.keys())}",
            stacklevel=2,
        )

    # Use common launch logic
    _, process_info = _launch_mapdl_common(
        exec_file=exec_file,
        run_location=run_location,
        jobname=jobname,
        nproc=nproc,
        port=port,
        ip=ip,
        mode=mode,
        version=version,
        start_instance=start_instance,
        ram=ram,
        timeout=timeout,
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
        transport_mode=transport_mode,
        uds_dir=uds_dir,
        uds_id=uds_id,
        certs_dir=certs_dir,
        add_env_vars=add_env_vars,
        replace_env_vars=replace_env_vars,
        license_server_check=license_server_check,
        force_intel=force_intel,
        graphics_backend=graphics_backend,
        start_timeout=start_timeout,
    )

    # For process-only launching, ensure we're starting a new instance
    if process_info is None:
        raise LaunchError(
            "launch_mapdl_process() requires start_instance=True. "
            "Use launch_mapdl() to connect to existing instances."
        )

    # Return connection info tuple (ip, port, pid)
    return (process_info.ip, process_info.port, process_info.pid)
