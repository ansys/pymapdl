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

"""``pymapdl stop`` sub-command implementation.

The click-independent :func:`stop` implementation lives in
:mod:`ansys.mapdl.core.launcher.connection` so it can be reused from regular
Python scripts (for example by
:func:`ansys.mapdl.core.launcher.connection.close_all_local_instances`)
without importing ``click``. It is re-exported here for backward
compatibility and for the ``pymapdl stop`` click command below.
"""

from typing import Optional

import click

from ansys.mapdl.core.cli.constants import MAPDL_DEFAULT_PORT
from ansys.mapdl.core.launcher.connection import stop  # noqa: F401


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
    except (ValueError, TypeError) as err:
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
