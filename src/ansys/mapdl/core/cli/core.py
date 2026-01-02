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
    """Get list of MAPDL instances with minimal data"""
    instances = []

    for proc in psutil.process_iter(attrs=["name"]):
        name = proc.info["name"]
        if not is_valid_ansys_process_name(name):
            continue

        try:
            status = proc.status()
            if not is_alive_status(status):
                continue

            cmdline = proc.cmdline()
            if "-grpc" not in cmdline:
                continue

            # Get port from cmdline
            port = None
            try:
                ind_grpc = cmdline.index("-port")
                port = int(cmdline[ind_grpc + 1])
            except (ValueError, IndexError):
                continue

            children = proc.children(recursive=True)
            is_instance = len(children) >= 2

            cwd = proc.cwd()
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

        except (psutil.NoSuchProcess, psutil.ZombieProcess, psutil.AccessDenied):
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
