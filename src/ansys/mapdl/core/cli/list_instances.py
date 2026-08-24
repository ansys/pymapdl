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

"""``pymapdl list`` sub-command implementation."""

from typing import Any, Dict, List

import click

from ansys.mapdl.core.cli.helpers import get_mapdl_instances


def list_instances(
    instances: bool = False,
    long: bool = False,
    cmd: bool = False,
    location: bool = False,
) -> str:
    """Render a table with the MAPDL processes running on this machine.

    Parameters
    ----------
    instances : bool, default: False
        Whether to list only the main processes (the instances), hiding their
        children.
    long : bool, default: False
        Whether to include every available field. Implies *cmd* and
        *location*.
    cmd : bool, default: False
        Whether to include the command line each process was started with.
    location : bool, default: False
        Whether to include the working directory of each process.

    Returns
    -------
    str
        Table ready to be printed. The table is empty when no MAPDL process
        is running.

    Examples
    --------
    Print the running MAPDL instances:

    >>> from ansys.mapdl.core.cli.list_instances import list_instances
    >>> print(list_instances(instances=True))
    Name          Status      gRPC port    PID
    ------------  --------  -----------  -----
    ANSYS241.exe  running         50052  41644

    """
    from tabulate import tabulate

    if long:
        cmd = True
        location = True

    if instances:
        headers = ["Name", "Status", "gRPC port", "PID"]
    else:
        headers = ["Name", "Is Instance", "Status", "gRPC port", "PID"]

    if cmd:
        headers.append("Command line")
    if location:
        headers.append("Working directory")

    table = []
    for each_proc in get_mapdl_instances():
        if instances and not each_proc.get("is_instance", False):
            continue

        table.append(_process_row(each_proc, instances, cmd, location))

    return tabulate(table, headers)


def _process_row(
    proc: Dict[str, Any], instances: bool, cmd: bool, location: bool
) -> List[Any]:
    """Build the table row describing a single MAPDL process.

    Parameters
    ----------
    proc : dict
        Process information as returned by
        :func:`ansys.mapdl.core.cli.helpers.get_mapdl_instances`.
    instances : bool
        Whether the ``Is Instance`` column is omitted.
    cmd : bool
        Whether the command line column is included.
    location : bool
        Whether the working directory column is included.

    Returns
    -------
    list
        Values of the row, in the same order as the table headers.
    """
    row: List[Any] = [proc["name"]]

    if not instances:
        row.append(proc.get("is_instance", False))

    row.extend([proc["status"], proc["port"], proc["pid"]])

    if cmd:
        row.append(" ".join(proc["cmdline"]))

    if location:
        row.append(proc["cwd"])

    return row


# ---------------------------------------------------------------------------
# Click wrapper
# ---------------------------------------------------------------------------


@click.command(
    short_help="List MAPDL running instances.",
    help="""This command lists MAPDL instances.""",
)
@click.option(
    "--instances",
    "-i",
    is_flag=True,
    flag_value=True,
    type=bool,
    default=False,
    help="Do not print the child process, only the main processes (instances).",
)
@click.option(
    "--long",
    "-l",
    is_flag=True,
    flag_value=True,
    type=bool,
    default=False,
    help="Print all info.",
)
@click.option(
    "--cmd",
    "-c",
    is_flag=True,
    flag_value=True,
    type=bool,
    default=False,
    help="Print cmd",
)
@click.option(
    "--location",
    "-cwd",
    is_flag=True,
    flag_value=True,
    type=bool,
    default=False,
    help="Print running location info.",
)
def list_instances_cli(instances: bool, long: bool, cmd: bool, location: bool) -> None:
    """List the MAPDL processes running on this machine.

    Parameters
    ----------
    instances : bool
        If :class:`True`, print only the main processes (the instances).
    long : bool
        If :class:`True`, print all the available information.
    cmd : bool
        If :class:`True`, print the command line of each process.
    location : bool
        If :class:`True`, print the working directory of each process.
    """
    click.echo(
        list_instances(instances=instances, long=long, cmd=cmd, location=location)
    )
