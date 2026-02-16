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

import click

from ansys.mapdl.core.cli import main


@main.command(
    short_help="List MAPDL running instances.",
    help="""This command list MAPDL instances""",
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
def list_instances(instances, long, cmd, location) -> None:
    return _list_instances(instances, long, cmd, location)


def _list_instances(instances, long, cmd, location):
    from tabulate import tabulate

    from ansys.mapdl.core.cli.helpers import get_mapdl_instances

    # Assuming all ansys processes have -grpc flag
    mapdl_instances = get_mapdl_instances()

    # printing
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
    for each_p in mapdl_instances:
        if instances and not each_p.get("is_instance", False):
            # Skip child processes if only printing instances
            continue

        proc_line = []
        proc_line.append(each_p["name"])

        if not instances:
            proc_line.append(each_p.get("is_instance", False))

        proc_line.extend([each_p["status"], each_p["port"], each_p["pid"]])

        if cmd:
            proc_line.append(" ".join(each_p["cmdline"]))

        if location:
            proc_line.append(each_p["cwd"])

        table.append(proc_line)

    print(tabulate(table, headers))
