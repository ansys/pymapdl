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
    - LaunchConfig: Configuration model (for advanced use)
"""

from typing import TYPE_CHECKING, Any, Callable, Dict, Optional, Union

from ansys.mapdl.core import LOG

from .config import resolve_launch_config
from .connection import connect_to_existing, create_console_client, create_grpc_client
from .environment import prepare_environment
from .errors import ConfigurationError, LaunchError
from .hpc import (
    detect_slurm_environment,
)
from .hpc import (
    resolve_slurm_resources,
)
from .hpc import launch_on_hpc as _launch_on_hpc_fn
from .models import LaunchConfig, LaunchMode
from .process import launch_mapdl_process
from .validation import validate_config

if TYPE_CHECKING:
    from ansys.mapdl.core.mapdl_console import MapdlConsole
    from ansys.mapdl.core.mapdl_grpc import MapdlGrpc

__all__ = [
    "launch_mapdl",
    "LaunchConfig",
    "ConfigurationError",
    "LaunchError",
]

# Re-export legacy functions for backward compatibility
# Import from _launcher_legacy.py (renamed old launcher.py)
try:
    from ansys.mapdl.core._launcher_legacy import (
        _HAS_ATC,
        LOCALHOST,
        MAPDL_DEFAULT_PORT,
        _check_server_is_alive,
        _create_queue_for_std,
        _get_std_output,
        _get_windows_host_ip,
        _is_ubuntu,
        check_kwargs,
        check_lock_file,
        check_mapdl_launch,
        check_mapdl_launch_on_hpc,
        check_mode,
        check_ports,
        check_valid_ansys,
        check_valid_ip,
        check_valid_port,
        close_all_local_instances,
        configure_ubuntu,
        create_gallery_instances,
        force_smp_in_student,
        generate_mapdl_launch_command,
        generate_sbatch_command,
        generate_start_parameters,
        get_cpus,
        get_default_ansys,
        get_default_ansys_path,
        get_default_ansys_version,
        get_exec_file,
        get_hostname_from_scontrol,
        get_hostname_host_cluster,
        get_ip,
        get_ip_env_var,
        get_jobid,
        get_port,
        get_process_at_port,
        get_run_location,
        get_slurm_options,
        get_start_instance,
        get_start_instance_arg,
        get_state_from_scontrol,
        get_version,
        handle_launch_exceptions,
        inject_additional_switches,
        is_ansys_process,
        is_running_on_slurm,
        kill_job,
        launch_grpc,
    )
    from ansys.mapdl.core._launcher_legacy import (
        launch_mapdl as _legacy_launch_mapdl,  # Legacy launch_mapdl implementation used as a fallback by the new launcher API.
    )
    from ansys.mapdl.core._launcher_legacy import (
        launch_mapdl_on_cluster,
        launch_remote_mapdl,
        pack_arguments,
        port_in_use,
        port_in_use_using_psutil,
        port_in_use_using_socket,
        pre_check_args,
        remove_err_files,
        send_scontrol,
        set_license_switch,
        set_MPI_additional_switches,
        submitter,
        update_env_vars,
        version_from_path,
    )

    # Add legacy exports to __all__
    __all__.extend(
        [
            "_create_queue_for_std",
            "_check_server_is_alive",
            "_get_std_output",
            "handle_launch_exceptions",
            "LOCALHOST",
            "MAPDL_DEFAULT_PORT",
            "_HAS_ATC",
            "check_valid_ip",
            "check_valid_port",
            "_is_ubuntu",
            "close_all_local_instances",
            "check_ports",
            "port_in_use",
            "port_in_use_using_socket",
            "port_in_use_using_psutil",
            "is_ansys_process",
            "get_process_at_port",
            "get_default_ansys",
            "get_default_ansys_path",
            "get_default_ansys_version",
            "check_valid_ansys",
            "version_from_path",
            "generate_mapdl_launch_command",
            "launch_grpc",
            "check_mapdl_launch",
            "launch_remote_mapdl",
            "get_start_instance",
            "check_mode",
            "update_env_vars",
            "set_license_switch",
            "set_MPI_additional_switches",
            "configure_ubuntu",
            "force_smp_in_student",
            "check_lock_file",
            "launch_mapdl_on_cluster",
            "generate_sbatch_command",
            "get_hostname_host_cluster",
            "get_hostname_from_scontrol",
            "get_state_from_scontrol",
            "get_jobid",
            "check_mapdl_launch_on_hpc",
            "kill_job",
            "send_scontrol",
            "submitter",
            "is_running_on_slurm",
            "get_slurm_options",
            "generate_start_parameters",
            "pack_arguments",
            "get_ip_env_var",
            "get_ip",
            "get_start_instance_arg",
            "get_port",
            "get_version",
            "get_exec_file",
            "get_run_location",
            "get_cpus",
            "inject_additional_switches",
            "remove_err_files",
            "check_kwargs",
            "pre_check_args",
            "_get_windows_host_ip",
            "create_gallery_instances",
        ]
    )
except ImportError as e:
    # If legacy launcher doesn't exist or has errors, warn but continue
    import warnings

    warnings.warn(
        f"Could not import legacy launcher functions: {e}. "
        f"Some backward compatibility may be limited."
    )


def launch_mapdl(
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
    It uses the new modular architecture while maintaining 100% backward
    compatibility with the legacy launcher API.

    Parameters:
        exec_file: Path to MAPDL executable
        run_location: Working directory for MAPDL
        jobname: MAPDL job name
        nproc: Number of processors
        port: gRPC server port
        ip: IP address to bind/connect
        mode: Launch mode (grpc or console)
        version: MAPDL version
        start_instance: Whether to start new instance
        ram: RAM allocation in MB
        timeout: Launch timeout in seconds
        cleanup_on_exit: Clean up on exit
        clear_on_connect: Clear database on connection
        override: Override existing lock file
        remove_temp_dir_on_exit: Remove temp directory on exit
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
        add_env_vars: Environment variables to add
        replace_env_vars: Environment variables to replace
        license_server_check: Check license server
        force_intel: Force Intel MPI
        graphics_backend: Graphics backend
        start_timeout: Deprecated. Use ``timeout`` instead.
        **kwargs: Additional arguments

    Returns:
        MapdlGrpc or MapdlConsole client instance

    Raises:
        ConfigurationError: Invalid configuration
        LaunchError: Launch failed
        ConnectionError: Cannot connect to MAPDL

    Examples:
        Launch new instance:
        >>> from ansys.mapdl.core.launcher import launch_mapdl
        >>> mapdl = launch_mapdl(nproc=4)

        Connect to existing:
        >>> mapdl = launch_mapdl(start_instance=False, ip="192.168.1.100", port=50053)

        Launch on HPC:
        >>> mapdl = launch_mapdl(
        ...     launch_on_hpc=True,
        ...     nproc=16,
        ...     scheduler_options={"nodes": 2, "ntasks-per-node": 8}
        ... )

    Notes:
        This implementation uses the domain-driven modular architecture:
        - Configuration resolution: config.resolve_launch_config()
        - Validation: validation.validate_config()
        - Environment setup: environment.prepare_environment()
        - Process launching: process.launch_mapdl_process() (local) or
          hpc.launch_on_hpc() (HPC cluster)
        - Client connection: connection.create_grpc_client() or
          connection.create_console_client()
    """
    # Merge environment variable dictionaries
    env_vars_merged = None
    if add_env_vars or replace_env_vars:
        env_vars_merged = {}
        if add_env_vars:
            env_vars_merged.update(add_env_vars)
        if replace_env_vars:
            env_vars_merged.update(replace_env_vars)

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
            env_vars=env_vars_merged,
            license_server_check=license_server_check,
            force_intel=force_intel,
            graphics_backend=graphics_backend,
            start_timeout=start_timeout,
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

    # Step 3: Handle connection to existing instance
    if not config.start_instance:
        LOG.info(f"Connecting to existing MAPDL instance at {config.ip}:{config.port}")
        try:
            return connect_to_existing(config)
        except Exception as e:
            LOG.error(f"Failed to connect to existing instance: {e}")
            raise

    # Step 4: Prepare environment
    try:
        env_config = prepare_environment(config)
        process_env = env_config.variables
    except Exception as e:
        LOG.error(f"Environment preparation failed: {e}")
        raise LaunchError(f"Failed to prepare environment: {e}") from e

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
            process_info = launch_mapdl_process(config, process_env)

    except Exception as e:
        LOG.error(f"Process launch failed: {e}")
        raise LaunchError(f"Failed to launch MAPDL: {e}") from e

    # Step 6: Create and return client
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
