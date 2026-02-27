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

"""Client connection management for MAPDL.

Functions for creating MapdlGrpc and MapdlConsole client instances.
"""

from typing import TYPE_CHECKING, Optional

from ansys.mapdl.core import LOG
from ansys.mapdl.core.mapdl_grpc import MapdlGrpc

from .models import LaunchConfig, ProcessInfo

if TYPE_CHECKING:
    from ansys.mapdl.core.mapdl_console import MapdlConsole


def create_grpc_client(
    config: LaunchConfig, process_info: Optional[ProcessInfo] = None
) -> MapdlGrpc:
    """Create and connect to a MapdlGrpc client instance.

    Establishes a connection to the MAPDL gRPC server using the provided
    configuration. If process_info is provided, uses its IP and port;
    otherwise uses the configuration's IP and port. The database is cleared
    upon connection if configured.

    Parameters
    ----------
    config : LaunchConfig
        Launch configuration containing connection parameters and behavior flags
    process_info : Optional[ProcessInfo], default: None
        Process information from a locally started instance. If provided,
        the IP and port from this will override config's IP and port

    Returns
    -------
    MapdlGrpc
        Connected and initialized MapdlGrpc client instance

    Raises
    ------
    ConnectionError
        If unable to establish connection to the MAPDL gRPC server
    socket.error
        If network connection fails

    Examples
    --------
    Connect using process information from local launch:

    >>> from ansys.mapdl.core.launcher.models import LaunchConfig, ProcessInfo
    >>> config = LaunchConfig(ip='127.0.0.1', port=50052)
    >>> process_info = ProcessInfo(port=50052, ip='127.0.0.1', process=None)
    >>> mapdl = create_grpc_client(config, process_info)

    Connect to existing instance:

    >>> config = LaunchConfig(ip='192.168.1.100', port=50052)
    >>> mapdl = create_grpc_client(config)

    Notes
    -----
    - If `clear_on_connect` is True in config, the MAPDL database will be
      cleared immediately after connection
    - The timeout from config applies to the connection attempt
    - Additional gRPC channel parameters can be configured via the config object
    """
    # Determine IP and port
    if process_info:
        ip = process_info.ip
        port = process_info.port
    else:
        ip = config.ip
        port = config.port

    LOG.info(f"Connecting to MAPDL gRPC server at {ip}:{port}")

    # Create client
    client = MapdlGrpc(
        ip=ip,
        port=port,
        cleanup_on_exit=config.cleanup_on_exit,
        loglevel=config.loglevel,
        log_apdl=config.log_apdl,
        print_com=config.print_com,
        set_no_abort=config.set_no_abort,
        timeout=config.timeout,
        remove_temp_dir_on_exit=config.remove_temp_dir_on_exit,
        process=process_info.process if process_info else None,
        # channel=config.grpc_channel,
        # transport_mode=config.transport_mode,
        # uds_dir=config.uds_dir,
        # uds_id=config.uds_id,
        # certs_dir=config.certs_dir,
    )

    # Clear database if requested
    if config.clear_on_connect:
        LOG.debug("Clearing MAPDL database")
        client.clear()

    LOG.info("Successfully connected to MAPDL")
    return client


def create_console_client(config: LaunchConfig) -> "MapdlConsole":
    """Create MapdlConsole client instance for legacy console mode.

    Creates a console-based MAPDL client for use with older MAPDL versions
    or environments where gRPC is not available. This is a legacy interface
    maintained for backward compatibility.

    Parameters
    ----------
    config : LaunchConfig
        Launch configuration with console-specific parameters including
        exec_file, run_location, jobname, and other settings

    Returns
    -------
    MapdlConsole
        Created and initialized MapdlConsole instance

    Raises
    ------
    FileNotFoundError
        If exec_file does not exist
    OSError
        If working directory cannot be created or accessed

    Examples
    --------
    Create and use console client:

    >>> from ansys.mapdl.core.launcher.models import LaunchConfig, LaunchMode
    >>> config = LaunchConfig(mode=LaunchMode.CONSOLE, ...)
    >>> mapdl = create_console_client(config)

    Notes
    -----
    - This mode is deprecated in favor of gRPC mode for new code
    - Console mode may have limited functionality compared to gRPC
    - Available only on Linux systems
    - Useful for MAPDL versions before 2021R1
    """
    from ansys.mapdl.core.mapdl_console import MapdlConsole

    LOG.info("Creating MAPDL console client (legacy mode)")

    client = MapdlConsole(
        exec_file=config.exec_file,
        run_location=config.run_location,
        jobname=config.jobname,
        nproc=config.nproc,
        additional_switches=config.additional_switches,
        start_timeout=config.timeout,
        loglevel=config.loglevel,
        log_apdl=config.log_apdl,
        cleanup_on_exit=config.cleanup_on_exit,
    )

    LOG.info("MAPDL console client created")
    return client


def connect_to_existing(config: LaunchConfig) -> MapdlGrpc:
    """Connect to an existing MAPDL instance without starting a new one.

    Establishes a connection to an already running MAPDL instance specified
    by IP address and port. This is useful for connecting to MAPDL instances
    running on remote machines or HPC clusters.

    Parameters
    ----------
    config : LaunchConfig
        Configuration object with IP address and port of existing instance.
        Must have start_instance=False

    Returns
    -------
    MapdlGrpc
        Connected MapdlGrpc client to existing instance

    Raises
    ------
    ConnectionError
        If unable to establish connection to the specified instance
    socket.error
        If network connection fails

    Examples
    --------
    Connect to remote MAPDL instance:

    >>> from ansys.mapdl.core.launcher.models import LaunchConfig
    >>> config = LaunchConfig(
    ...     start_instance=False,
    ...     ip="192.168.1.100",
    ...     port=50052
    ... )
    >>> mapdl = connect_to_existing(config)

    Connect to MAPDL on localhost:

    >>> config = LaunchConfig(
    ...     start_instance=False,
    ...     ip="127.0.0.1",
    ...     port=50052
    ... )
    >>> mapdl = connect_to_existing(config)

    Notes
    -----
    - The target MAPDL instance must be running and listening on the
      specified IP and port
    - Ensure network connectivity and firewall rules allow connection
    - Default timeout from config will be used for connection attempts
    """
    LOG.info(f"Connecting to existing MAPDL instance at {config.ip}:{config.port}")
    return create_grpc_client(config, process_info=None)
