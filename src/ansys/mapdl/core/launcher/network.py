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
    """Check if a port is available.

    Uses both socket binding and psutil process checking to determine
    if a port is available and if it's used by MAPDL.

    Parameters:
        port: Port number to check
        host: Host address to check

    Returns:
        PortStatus with availability and usage information

    Examples:
        >>> status = check_port_status(50052)
        >>> if status.available:
        ...     print("Port is free")
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
    """Find an available port starting from start_port.

    Parameters:
        start_port: Port to start searching from
        max_attempts: Maximum number of ports to try

    Returns:
        First available port number

    Raises:
        RuntimeError: If no port available after max_attempts

    Examples:
        >>> port = find_available_port()
        >>> port >= 50052
        True
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
    """Check port availability via socket binding.

    Parameters:
        port: Port number
        host: Host address

    Returns:
        True if port is available (can bind), False otherwise
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.bind((host, port))
            return True
        except socket.error:
            return False


def _get_process_at_port(port: int) -> Optional[psutil.Process]:
    """Get process listening on port (returns psutil.Process).

    Parameters:
        port: Port number

    Returns:
        Process object or None if no process found
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
    """Check if process is MAPDL.

    Parameters:
        process: Process to check

    Returns:
        True if process is MAPDL
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
