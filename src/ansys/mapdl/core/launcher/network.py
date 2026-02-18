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

"""Network and port management for MAPDL launcher.

Functions for checking port availability, finding free ports,
and managing network connections.
"""

import socket
from typing import Optional

import psutil

from ansys.mapdl.core import LOG

from .models import PortStatus


def check_port_status(port: int, host: str = "127.0.0.1") -> PortStatus:
    """Check if a network port is available and in use.

    Uses both socket binding and psutil process checking to determine
    if a port is available and if it's used by a MAPDL instance. This
    provides comprehensive port status information.

    Parameters
    ----------
    port : int
        Port number to check (typically 50052 for MAPDL)
    host : str, default: "127.0.0.1"
        Host address to check (127.0.0.1 for local, 0.0.0.0 for all interfaces)

    Returns
    -------
    PortStatus
        Status object containing availability, MAPDL usage, and process information

    Raises
    ------
    None
        Function handles all errors gracefully

    Examples
    --------
    Check if default MAPDL port is free:

    >>> from ansys.mapdl.core.launcher.network import check_port_status
    >>> status = check_port_status(50052)
    >>> if status.available:
    ...     print("Port is free, safe to use for MAPDL")

    Check port and identify using process:

    >>> status = check_port_status(50052)
    >>> if not status.available:
    ...     if status.used_by_mapdl:
    ...         print("Port used by MAPDL, stop MAPDL first")
    ...     else:
    ...         proc_name = status.process.name() if status.process else "unknown"
    ...         print(f"Port used by {proc_name}")

    Notes
    -----
    - Returns immediately with status, doesn't block
    - psutil may require elevated permissions for full process info
    - MAPDL process identification checks for ansys/mapdl name and -grpc flag
    """
    # Try socket binding
    socket_available = _check_port_socket(port, host)

    # Check via psutil
    process = _get_process_at_port(port)

    if process:
        is_mapdl = _is_mapdl_process(process)
        return PortStatus(
            port=port,
            available=False,
            used_by_mapdl=is_mapdl,
            process=process,
        )

    return PortStatus(
        port=port,
        available=socket_available,
        used_by_mapdl=False,
        process=None,
    )


def find_available_port(start_port: int = 50052, max_attempts: int = 100) -> int:
    """Find an available network port starting from a base port.

    Searches for an available port by incrementing from start_port up to
    max_attempts times. Useful for automatically finding a free port when
    the default is in use.

    Parameters
    ----------
    start_port : int, default: 50052
        Base port number to start searching from (default MAPDL gRPC port)
    max_attempts : int, default: 100
        Maximum number of ports to check before raising error

    Returns
    -------
    int
        First available port number

    Raises
    ------
    RuntimeError
        If no port available within the search range
        (start_port to start_port + max_attempts)

    Examples
    --------
    Find available port starting from default:

    >>> from ansys.mapdl.core.launcher.network import find_available_port
    >>> port = find_available_port()
    >>> print(f"Using port: {port}")

    Find available port in specific range:

    >>> port = find_available_port(start_port=50100, max_attempts=50)
    >>> config = LaunchConfig(port=port, ...)

    Notes
    -----
    - Each port is checked using check_port_status()
    - Linear search, so may be slow for large max_attempts
    - Found port is logged at DEBUG level
    """
    for offset in range(max_attempts):
        port = start_port + offset
        status = check_port_status(port)
        if status.available:
            LOG.debug(f"Found available port: {port}")
            return port

    raise RuntimeError(
        f"No available port found in range {start_port}-{start_port + max_attempts}"
    )


def _check_port_socket(port: int, host: str) -> bool:
    """Check port availability via socket binding attempt.

    Attempts to bind a socket to the specified port and host to determine
    if the port is available. This is the most direct method of checking.

    Parameters
    ----------
    port : int
        Port number to check
    host : str
        Host address to attempt binding to

    Returns
    -------
    bool
        True if port is available (bind succeeds), False otherwise

    Raises
    ------
    None
        Socket errors are caught and False is returned

    Examples
    --------
    Check if port is bindable:

    >>> from ansys.mapdl.core.launcher.network import _check_port_socket
    >>> if _check_port_socket(50052, "127.0.0.1"):
    ...     print("Port 50052 is available")

    Notes
    -----
    - Internal utility function
    - Fast, non-blocking check
    - Does not identify what process is using the port
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.bind((host, port))
            return True
        except socket.error:
            return False


def _get_process_at_port(port: int) -> Optional[psutil.Process]:
    """Get the process listening on a specific port.

    Iterates through all running processes to find one that has a network
    connection listening on the specified port. Handles permission errors
    gracefully.

    Parameters
    ----------
    port : int
        Port number to search for

    Returns
    -------
    Optional[psutil.Process]
        Process object if found, None if no process found or inaccessible

    Raises
    ------
    None
        Permission errors (psutil.AccessDenied, psutil.NoSuchProcess) are
        caught and iteration continues

    Examples
    --------
    Find process using a port:

    >>> from ansys.mapdl.core.launcher.network import _get_process_at_port
    >>> proc = _get_process_at_port(50052)
    >>> if proc:
    ...     print(f"Process {proc.name()} is using port 50052")

    Notes
    -----
    - Internal utility function
    - May be slow on systems with many processes
    - Requires appropriate system permissions for process information
    - Returns None if any process cannot be accessed (e.g., system processes)
    """
    for proc in psutil.process_iter():
        try:
            # Check if we can access the process connections
            connections = proc.net_connections()
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            continue

        # Check if any connection uses the port
        for conn in connections:
            if conn.laddr.port == port:
                return proc

    return None


def _is_mapdl_process(process: psutil.Process) -> bool:
    """Check if a process is an ANSYS MAPDL instance.

    Examines the process name and command line to determine if it's a MAPDL
    process. Checks for ansys/mapdl name and -grpc flag in command.

    Parameters
    ----------
    process : psutil.Process
        Process object to check

    Returns
    -------
    bool
        True if process is MAPDL with gRPC mode, False otherwise

    Raises
    ------
    None
        Permission errors (psutil.AccessDenied, psutil.NoSuchProcess) result
        in False return

    Examples
    --------
    Identify MAPDL process:

    >>> from ansys.mapdl.core.launcher.network import _is_mapdl_process
    >>> import psutil
    >>> for proc in psutil.process_iter(['name']):
    ...     if _is_mapdl_process(proc):
    ...         print(f"Found MAPDL: {proc.name()}")

    Notes
    -----
    - Internal utility function
    - Checks both process name (ansys, mapdl) and -grpc flag
    - Returns False if process info cannot be accessed
    """
    try:
        name = process.name().lower()
        cmdline = process.cmdline()

        # Check if it's an ANSYS/MAPDL process with gRPC flag
        is_ansys_name = name.startswith(("ansys", "mapdl"))
        has_grpc_flag = "-grpc" in cmdline

        return is_ansys_name and has_grpc_flag
    except (psutil.AccessDenied, psutil.NoSuchProcess):
        return False
