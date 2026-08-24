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

"""``pymapdl stop`` sub-command implementation."""

from typing import List, Optional

import psutil

from ansys.mapdl.core.cli.constants import MAPDL_DEFAULT_PORT
from ansys.mapdl.core.cli.helpers import (
    can_access_process,
    get_ansys_process_from_port,
)

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
    ValueError
        When *pid* cannot be converted to an integer.

    Examples
    --------
    Stop the instance running on the default port:

    >>> from ansys.mapdl.core.cli.stop import stop
    >>> stop()
    [23644]

    Stop every running instance:

    >>> stop(all=True)
    [23644, 23645]

    """
    if all:
        return _stop_all_instances()

    if pid and not port:
        return _stop_process_tree(pid)

    return _stop_instance_on_port(port or MAPDL_DEFAULT_PORT)


def _stop_all_instances() -> List[int]:
    """Kill every MAPDL process the current user owns.

    Returns
    -------
    list of int
        Process IDs of the processes that have been killed.
    """
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
        Process IDs that are confirmed to have terminated. The parent PID is
        only included when the process is gone before the timeout elapses.
        An empty list means that the process could not be found or that
        nothing could be killed.

    Raises
    ------
    ValueError
        When *pid* cannot be converted to an integer.
    """
    try:
        pid = int(pid)
    except (TypeError, ValueError) as err:
        raise ValueError("PID provided could not be converted to int.") from err

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


# ---------------------------------------------------------------------------
# Click wrapper
# ---------------------------------------------------------------------------

import click


@click.command(
    short_help="Stop MAPDL instances.",
    help="""This command stop MAPDL instances running on a given port or with a given process id (PID).

By default, it stops instances running on the port 50052.""",
)
@click.option(
    "--port",
    default=None,
    type=int,
    help="Port where the MAPDL instance is running.",
)
@click.option(
    "--pid",
    default=None,
    type=int,
    help="Process PID where the MAPDL instance is running.",
)
@click.option(
    "--all",
    is_flag=True,
    flag_value=True,
    type=bool,
    default=False,
    help="Kill all MAPDL instances",
)
def stop_cli(port: Optional[int], pid: Optional[int], all: bool) -> None:
    """Stop MAPDL instances running on a given port or with a given process id (PID).

    This command stops MAPDL instances running on a given port or with a given process id (PID).
    By default, it stops instances running on the port 50052.

    Parameters
    ----------
    port : int
        Port where the MAPDL instance is running.
    pid : Optional[int]
        PID of the MAPDL instance
    all : bool
        If :class:`True`, kill all the instances regardless their port or PID.
    """
    try:
        stopped = stop(port=port, pid=pid, all=all)
    except ValueError as err:
        click.echo(click.style("ERROR: ", fg="red") + str(err))
        return

    if pid and not port and not all:
        if pid in stopped:
            click.echo(
                click.style("Success: ", fg="green")
                + f"The process with PID {pid} and its children have been stopped."
            )
        else:
            click.echo(
                click.style("ERROR: ", fg="red")
                + f"The process with PID {pid} and its children could not be killed."
            )
        return

    target = "" if all else f" running on port {port or MAPDL_DEFAULT_PORT}"

    if stopped:
        click.echo(
            click.style("Success: ", fg="green")
            + "Ansys instances"
            + target
            + " have been stopped."
        )
    else:
        click.echo(
            click.style("ERROR: ", fg="red")
            + "No Ansys instances"
            + target
            + " have been found."
        )
