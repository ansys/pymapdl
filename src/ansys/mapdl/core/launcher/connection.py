# Copyright (C) 2016 - 2026 ANSYS, Inc. and/or its affiliates.
# Copyright (C) 2016 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
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

from typing import TYPE_CHECKING, List, Optional

import psutil

from ansys.mapdl.core import LOG
from ansys.mapdl.core.mapdl_grpc import MapdlGrpc

from .models import LaunchConfig, ProcessInfo

if TYPE_CHECKING:
    from ansys.mapdl.core.mapdl_console import MapdlConsole

# Process statuses from which a process can be killed normally. Statuses such
# as ``STATUS_ZOMBIE``, ``STATUS_STOPPED`` or ``STATUS_TRACING_STOP`` are
# deliberately excluded because those processes cannot be terminated cleanly.
_PROCESS_OK_STATUS = (
    psutil.STATUS_RUNNING,
    psutil.STATUS_SLEEPING,
    psutil.STATUS_DISK_SLEEP,
    psutil.STATUS_DEAD,
    psutil.STATUS_PARKED,  # Linux
    psutil.STATUS_IDLE,  # Linux, macOS and FreeBSD
)

# Seconds to wait for a process to disappear after it has been killed.
_TERMINATION_TIMEOUT = 5.0


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
        channel=config.channel,
        jobname=config.jobname,
        jobid=(process_info.jobid if process_info else None) or config.jobid,
        finish_job_on_exit=config.finish_job_on_exit,
        run_location=config.run_location,
        launched=process_info is not None,
        transport_mode=(config.transport_mode.value if config.transport_mode else None),
        uds_dir=config.uds_dir,
        certs_dir=(str(config.certs_dir) if config.certs_dir else None),
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

    Establishes a connection to an already running MAPDL instance. When
    ``config.channel`` is set the pre-built gRPC channel is reused directly;
    otherwise the connection is made via ``config.ip`` and ``config.port``.

    Parameters
    ----------
    config : LaunchConfig
        Configuration object with IP address and port of existing instance
        (or a pre-built ``channel``). Must have ``start_instance=False``.

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

    Connect using a pre-built gRPC channel:

    >>> import grpc
    >>> channel = grpc.insecure_channel("localhost:50052")
    >>> config = LaunchConfig(start_instance=False, channel=channel, ...)
    >>> mapdl = connect_to_existing(config)

    Notes
    -----
    - The target MAPDL instance must be running and listening on the
      specified IP and port
    - When ``channel`` is provided, you should not use ``ip`` and ``port`` for
      the actual connection
    - Default timeout from config will be used for connection attempts
    """
    LOG.info(f"Connecting to existing MAPDL instance at {config.ip}:{config.port}")
    return create_grpc_client(config, process_info=None)


def close_all_local_instances(port_range: range | None = None) -> None:
    """Close all MAPDL instances within a port_range.

    This function can be used when cleaning up from a failed pool or
    batch run.

    Parameters
    ----------
    port_range : list, optional
        Defaults to all ports. Expand this range if
        there are many potential instances of MAPDL in gRPC mode.

    Examples
    --------
    Close all instances on in the range of 50000 and 50199.

    >>> import ansys.mapdl.core as pymapdl
    >>> pymapdl.close_all_local_instances()
    """
    if port_range is None:
        stop(all=True)
    else:
        for port in port_range:
            stop(port=port)


def stop(
    port: Optional[int] = None, pid: Optional[int] = None, all: bool = False
) -> List[int]:
    """Stop MAPDL instances running on a given port or with a given process ID.

    When neither *port* nor *pid* is given, the instance running on port
    ``50052`` is stopped.

    Parameters
    ----------
    port : int, optional
        Port where the MAPDL instance to stop is running.
    pid : int, optional
        Process ID of the MAPDL instance to stop. The whole process tree
        is stopped, children first.
    all : bool, default: False
        Whether to stop every MAPDL instance owned by the current user,
        regardless of its port or process ID. Takes precedence over *port*
        and *pid*.

    Returns
    -------
    list of int
        Process IDs of the instances that have been stopped. An empty list
        means that no matching instance was found or that none could be
        killed.

    Raises
    ------
    TypeError
        When *pid* is given but is not an int.

    Examples
    --------
    Stop the instance running on the default port:

    >>> from ansys.mapdl.core.launcher.connection import stop
    >>> stop()
    [23644]

    Stop every running instance:

    >>> stop(all=True)
    [23644, 23645]

    """
    from .config import MAPDL_DEFAULT_PORT

    if all:
        return _stop_all_instances()

    if pid and not port:
        if not isinstance(pid, int):
            raise TypeError(f"'pid' must be an int, got {type(pid).__name__!r}.")
        return _stop_process_tree(pid)

    return _stop_instance_on_port(port or MAPDL_DEFAULT_PORT)


def _stop_all_instances() -> List[int]:
    """Kill every MAPDL process the current user owns.

    Returns
    -------
    list of int
        Process IDs of the processes that have been killed.
    """
    from .network import can_access_process

    stopped: List[int] = []

    for proc in psutil.process_iter():
        try:
            if not can_access_process(proc):
                continue

            if not _is_valid_ansys_process(proc):
                continue

            try:
                _kill_process(proc)
            except psutil.NoSuchProcess:
                continue

            stopped.append(proc.pid)

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return stopped


def _stop_instance_on_port(port: int) -> List[int]:
    """Kill the MAPDL instance listening on *port*.

    Parameters
    ----------
    port : int
        Port where the MAPDL instance is running.

    Returns
    -------
    list of int
        Process ID of the killed instance, or an empty list when no instance
        is running on *port*.
    """
    from .network import get_ansys_process_from_port

    proc = get_ansys_process_from_port(port)
    if proc is None:
        return []

    try:
        _kill_process(proc)
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return []

    return [proc.pid]


def _stop_process_tree(pid: int) -> List[int]:
    """Kill the process *pid* and all its children.

    Any :class:`psutil.NoSuchProcess` or :class:`psutil.AccessDenied` raised
    while looking up, killing, or waiting on a process is treated the same
    way as elsewhere in this module: the process is skipped rather than the
    exception being propagated.

    Parameters
    ----------
    pid : int
        Process ID of the parent process.

    Returns
    -------
    list of int
        Process IDs that were killed. Only the parent PID is confirmed to
        have actually terminated, because :meth:`psutil.Process.wait` is
        called on it before it is added to the result; children are killed
        but not waited on individually, so a killed child may still be in
        the process of exiting when its PID is returned. An empty list means
        that the process could not be found or that nothing could be
        killed.
    """
    try:
        proc = psutil.Process(pid)
    except psutil.NoSuchProcess:
        return []

    stopped: List[int] = []

    try:
        children = proc.children(recursive=True)
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        children = []

    for child in children:
        try:
            _kill_process(child)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
        stopped.append(child.pid)

    try:
        _kill_process(proc)
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return stopped

    try:
        proc.wait(timeout=_TERMINATION_TIMEOUT)
    except psutil.TimeoutExpired:
        return stopped
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass

    stopped.append(pid)
    return stopped


def _kill_process(proc: psutil.Process) -> None:
    """Kill *proc*.

    Parameters
    ----------
    proc : psutil.Process
        Process to kill.
    """
    proc.kill()


def _is_valid_ansys_process(proc: psutil.Process) -> bool:
    """Return whether *proc* is a live MAPDL process that can be killed.

    Parameters
    ----------
    proc : psutil.Process
        Process to check.

    Returns
    -------
    bool
        ``True`` when the process exists, is in a killable state, and is a
        MAPDL process.
    """
    from ansys.mapdl.core.launcher.network import _is_mapdl_process

    return (
        psutil.pid_exists(proc.pid)
        and proc.status() in _PROCESS_OK_STATUS
        and _is_mapdl_process(proc)
    )
