# Copyright (C) 2024 ANSYS, Inc. and/or its affiliates.
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
    help="Print only instances",
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
def list_instances(instances, long, cmd, location):
    import psutil
    from tabulate import tabulate

    # Assuming all ansys processes have -grpc flag
    mapdl_instances = []
    for proc in psutil.process_iter():
        if (
            "ansys" in proc.name().lower() or "mapdl" in proc.name().lower()
        ) and "-grpc" in proc.cmdline():
            if len(proc.children(recursive=True)) < 2:
                proc.ansys_instance = False
            else:
                proc.ansys_instance = True
            mapdl_instances.append(proc)

    # printing
    table = []

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

    def get_port(proc):
        cmdline = proc.cmdline()
        ind_grpc = cmdline.index("-port")
        return cmdline[ind_grpc + 1]

    table = []
    for each_p in mapdl_instances:
        if instances and not each_p.ansys_instance:
            continue

        proc_line = []
        proc_line.append(each_p.name())

        if not instances:
            proc_line.append(each_p.ansys_instance)

        proc_line.extend([each_p.status(), get_port(each_p), each_p.pid])

        if cmd:
            proc_line.append(" ".join(each_p.cmdline()))

        if location:
            proc_line.append(each_p.cwd())

        table.append(proc_line)

    print(tabulate(table, headers))
