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
    """Create MapdlGrpc client instance.

    Parameters:
        config: Launch configuration
        process_info: Process info (if started locally)

    Returns:
        Connected MapdlGrpc instance

    Raises:
        ConnectionError: If cannot connect to MAPDL

    Examples:
        >>> config = LaunchConfig(...)
        >>> process_info = ProcessInfo(...)
        >>> mapdl = create_grpc_client(config, process_info)
        >>> mapdl.version
        '22.2'
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
    """Create MapdlConsole client instance (legacy).

    Parameters:
        config: Launch configuration

    Returns:
        Connected MapdlConsole instance

    Examples:
        >>> config = LaunchConfig(mode=LaunchMode.CONSOLE, ...)
        >>> mapdl = create_console_client(config)
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
    """Connect to existing MAPDL instance.

    Parameters:
        config: Configuration with ip and port

    Returns:
        Connected MapdlGrpc instance

    Raises:
        ConnectionError: If cannot connect

    Examples:
        >>> config = LaunchConfig(start_instance=False, ip="192.168.1.100", ...)
        >>> mapdl = connect_to_existing(config)
    """
    LOG.info(f"Connecting to existing MAPDL instance at {config.ip}:{config.port}")
    return create_grpc_client(config, process_info=None)
