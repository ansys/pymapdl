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

"""
Minimal core functionality for CLI operations.
This module avoids importing heavy dependencies like pandas, numpy, etc.
"""

from typing import Any, Dict, List

import psutil


def can_access_process(proc):
    """Check if we have permission to access and interact with a process.

    Returns True if:
    1. We can access the process information (no AccessDenied)
    2. The process belongs to the current user

    Parameters
    ----------
    proc : psutil.Process
        The process to check

    Returns
    -------
    bool
        True if we can safely access the process
    """
    import getpass
    import platform

    try:
        # Check if we can access basic process info and if it belongs to current user
        current_user = getpass.getuser()
        process_user = proc.username()
        if platform.system() == "Windows" and "\\" in process_user:
            return current_user == process_user.split("\\")[-1]
        return process_user == current_user
    except (psutil.AccessDenied, psutil.NoSuchProcess):
        # Cannot access process or process doesn't exist
        return False


def is_valid_ansys_process_name(name: str) -> bool:
    """Check if process name indicates ANSYS/MAPDL"""
    return ("ansys" in name.lower()) or ("mapdl" in name.lower())


def is_alive_status(status) -> bool:
    """Check if process status indicates alive"""
    return status in [
        psutil.STATUS_RUNNING,
        psutil.STATUS_IDLE,
        psutil.STATUS_SLEEPING,
    ]


def get_mapdl_instances() -> List[Dict[str, Any]]:
    """Get list of MAPDL instances with minimal data.

    This function safely handles permission errors when accessing process information.
    Processes owned by other users are skipped. For current user's processes,
    we attempt to gather information but skip if critical data is inaccessible.
    """
    instances = []

    for proc in psutil.process_iter(attrs=["name"]):
        name = proc.info["name"]
        if not is_valid_ansys_process_name(name):
            continue

        try:
            # Check if alive
            status = proc.status()
            if not is_alive_status(status):
                continue

            # Try to get cmdline
            try:
                cmdline = proc.cmdline()
            except (psutil.AccessDenied, PermissionError):
                # Can't access cmdline - check if it's our process
                if not can_access_process(proc):
                    # Not our process, skip it
                    continue
                # Our process but can't get cmdline - skip (can't verify if gRPC)
                continue

            # Check if it's a gRPC process
            if "-grpc" not in cmdline:
                continue

            # Get port from cmdline
            try:
                port_index = cmdline.index("-port")
                port = int(cmdline[port_index + 1])
            except (ValueError, IndexError):
                continue

            # Get number of children (for is_instance flag)
            try:
                children = proc.children(recursive=True)
                is_instance = len(children) >= 2
            except (psutil.AccessDenied, PermissionError):
                is_instance = False

            # Get working directory (with fallback to empty string on permission issues)
            try:
                cwd = proc.cwd()
            except (psutil.AccessDenied, PermissionError):
                cwd = ""

            instances.append(
                {
                    "name": name,
                    "status": status,
                    "port": port,
                    "pid": proc.pid,
                    "cmdline": cmdline,
                    "is_instance": is_instance,
                    "cwd": cwd,
                }
            )

        except (psutil.NoSuchProcess, psutil.ZombieProcess):
            # Process disappeared or is zombie, skip it
            continue

        except (psutil.AccessDenied, PermissionError):
            # We don't have permission to access this process, skip it
            continue

    return instances


def get_ansys_process_from_port(port: int):
    import socket

    # Filter by name first
    potential_procs = []
    for proc in psutil.process_iter(attrs=["name"]):
        name = proc.info["name"]
        if is_valid_ansys_process_name(name):
            potential_procs.append(proc)

    for proc in potential_procs:
        try:
            status = proc.status()
            if not is_alive_status(status):
                continue
            cmdline = proc.cmdline()
            if "-grpc" not in cmdline:
                continue
            # Check if listening on the port
            connections = proc.connections()
            for conn in connections:
                if (
                    conn.status == "LISTEN"
                    and conn.family == socket.AF_INET
                    and conn.laddr[1] == port
                ):
                    return proc
        except (psutil.NoSuchProcess, psutil.ZombieProcess, psutil.AccessDenied):
            continue
