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

from typing import Any, Dict, List, Optional

import psutil


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


def _get_process_user(proc: psutil.Process) -> Optional[str]:
    """Get the username of a process, handling permission errors.

    Parameters
    ----------
    proc : psutil.Process
        The process to check

    Returns
    -------
    Optional[str]
        Username of the process owner, or None if inaccessible
    """
    import getpass
    import platform

    try:
        current_user = getpass.getuser()
        process_user = proc.username()
        
        # On Windows, username may include domain (e.g., "DOMAIN\\username")
        if platform.system() == "Windows" and "\\" in process_user:
            process_user = process_user.split("\\")[-1]
        
        return process_user
    except (psutil.AccessDenied, psutil.NoSuchProcess):
        return None


def _is_current_user_process(proc: psutil.Process) -> bool:
    """Check if a process belongs to the current user.

    Parameters
    ----------
    proc : psutil.Process
        The process to check

    Returns
    -------
    bool
        True if the process belongs to the current user, False otherwise
    """
    import getpass

    try:
        current_user = getpass.getuser()
        process_user = _get_process_user(proc)
        
        if process_user is None:
            return False
        
        return current_user == process_user
    except Exception:
        return False


def get_mapdl_instances() -> List[Dict[str, Any]]:
    """Get list of MAPDL instances with minimal data.
    
    This function safely handles permission errors when accessing process information.
    If a process belongs to another user and cannot be accessed, it is skipped.
    If a process belongs to the current user but cmdline/cwd cannot be accessed,
    it is listed with partial information.
    """
    instances = []

    for proc in psutil.process_iter(attrs=["name"]):
        name = proc.info["name"]
        if not is_valid_ansys_process_name(name):
            continue

        try:
            status = proc.status()
            if not is_alive_status(status):
                continue

            # Try to get cmdline - this may fail due to permissions
            cmdline = None
            try:
                cmdline = proc.cmdline()
            except (psutil.AccessDenied, PermissionError):
                # If we can't access cmdline, check if it's our process
                if not _is_current_user_process(proc):
                    # Skip processes owned by other users
                    continue
                # For our own processes, we'll try to list with partial info
                cmdline = []

            # If we got cmdline, check for -grpc flag
            if cmdline and "-grpc" not in cmdline:
                continue
            
            # If cmdline is empty (permission error on our own process),
            # we can't determine if it's gRPC, so skip it
            if not cmdline:
                continue

            # Get port from cmdline
            port = None
            try:
                ind_grpc = cmdline.index("-port")
                port = int(cmdline[ind_grpc + 1])
            except (ValueError, IndexError):
                continue

            # Try to get children count - may fail due to permissions
            is_instance = False
            try:
                children = proc.children(recursive=True)
                is_instance = len(children) >= 2
            except (psutil.AccessDenied, PermissionError):
                # Can't determine if it's an instance, default to False
                pass

            # Try to get cwd - may fail due to permissions
            cwd = None
            try:
                cwd = proc.cwd()
            except (psutil.AccessDenied, PermissionError):
                # If we can't get cwd, use empty string
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
            # Process no longer exists or is a zombie
            continue
        except psutil.AccessDenied:
            # General access denied - check if it's our process
            if not _is_current_user_process(proc):
                # Skip processes owned by other users
                continue
            # For our own processes that we can't fully access, skip them
            continue

    return instances


def get_ansys_process_from_port(port: int):
    import socket

    import psutil

    from ansys.mapdl.core.cli.core import is_alive_status, is_valid_ansys_process_name

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
