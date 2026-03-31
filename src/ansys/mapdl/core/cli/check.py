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

import sys

import click


@click.command(
    short_help="Check a running MAPDL instance and print diagnostic information.",
    help="""Connect to a running MAPDL gRPC server and display diagnostic information.

\b
Examples:
  pymapdl check
  pymapdl check --ip 192.168.1.10 --port 50052
  pymapdl check --json
""",
)
@click.option(
    "--ip",
    default="127.0.0.1",
    type=str,
    show_default=True,
    help="IP address of the MAPDL gRPC server.",
)
@click.option(
    "--port",
    default=50052,
    type=int,
    show_default=True,
    help="Port of the MAPDL gRPC server.",
)
@click.option(
    "--timeout",
    default=10,
    type=int,
    show_default=True,
    help="Seconds to wait when connecting.",
)
@click.option(
    "--json",
    "as_json",
    is_flag=True,
    default=False,
    help="Output diagnostic information as a JSON object.",
)
def check(ip: str, port: int, timeout: int, as_json: bool) -> None:
    """Connect to a running MAPDL instance and print diagnostic information.

    Parameters
    ----------
    ip : str
        IP address of the MAPDL gRPC server.
    port : int
        Port of the MAPDL gRPC server.
    timeout : int
        Seconds to wait when establishing the gRPC connection.
    as_json : bool
        When :class:`True`, output all information as a JSON object instead of
        human-readable text.
    """
    import json
    import logging

    from ansys.mapdl.core import LOG

    LOG.setLevel(logging.CRITICAL + 1)
    if LOG.std_out_handler:
        LOG.std_out_handler.setLevel(logging.CRITICAL + 1)

    try:
        from ansys.mapdl.core.launcher.config import resolve_launch_config
        from ansys.mapdl.core.launcher.connection import connect_to_existing

        config = resolve_launch_config(
            ip=ip,
            port=port,
            start_instance=False,
            clear_on_connect=False,
            timeout=timeout,
        )
        mapdl = connect_to_existing(config)

    except Exception as e:
        click.echo(
            click.style("ERROR:", fg="red")
            + f" Could not connect to MAPDL at {ip}:{port} — {e}",
            err=True,
        )
        sys.exit(1)

    from ansys.mapdl.core.information import get_mapdl_info

    data = get_mapdl_info(mapdl)

    if as_json:
        click.echo(json.dumps(data, indent=2))
    else:
        conn = data.get("connection", {})
        _print_info_human_readable(data)


def _print_info_human_readable(data: dict) -> None:
    """Render ``get_mapdl_info`` output as formatted text.

    Parameters
    ----------
    data : dict
        Nested dictionary returned by :func:`get_mapdl_info`.
    """
    W = 24  # key column width

    def row(key: str, value) -> None:
        click.echo(f"  {key.ljust(W)}{value}")

    def section(title: str) -> None:
        click.echo("")
        click.echo(click.style(title, bold=True))

    conn = data.get("connection", {})
    section("Connection")
    if "error" in conn:
        row("Error", conn["error"])
    else:
        row("Name:", conn.get("name", ""))
        row("IP:", conn.get("ip", ""))
        row("Port:", conn.get("port", ""))
        row("Status:", conn.get("status", ""))
        row("Version:", conn.get("version", ""))
        row("Platform:", conn.get("platform", ""))
        row("Directory:", conn.get("directory", ""))
        row("Jobname:", conn.get("jobname", ""))
        row("Is local:", conn.get("is_local", ""))

    inf = data.get("information", {})
    section("Information")
    if "error" in inf:
        row("Error", inf["error"])
    else:
        row("Product:", inf.get("product", ""))
        row("MAPDL version:", inf.get("mapdl_version", ""))
        row("  Build:", inf.get("mapdl_version_build", ""))
        row("  Update:", inf.get("mapdl_version_update", ""))
        row("PyMAPDL version:", inf.get("pymapdl_version", ""))
        row("Title:", inf.get("title", ""))
        units = inf.get("units", {})
        if isinstance(units, dict) and units:
            row("Units:", next(iter(units.values()), "").upper() or "")
        else:
            row("Units:", "")

    geo = data.get("geometry", {})
    section("Geometry")
    if "error" in geo:
        row("Error", geo["error"])
    else:
        row("Keypoints:", geo.get("n_keypoint", 0))
        row("Lines:", geo.get("n_line", 0))
        row("Areas:", geo.get("n_area", 0))
        row("Volumes:", geo.get("n_volu", 0))

    mesh = data.get("mesh", {})
    section("Mesh")
    if "error" in mesh:
        row("Error", mesh["error"])
    else:
        row("Nodes:", mesh.get("n_node", 0))
        row("Elements:", mesh.get("n_elem", 0))

    post = data.get("post_processing", {})
    section("Post Processing")
    if "error" in post:
        row("Error", post["error"])
    else:
        row("Available:", post.get("available", False))
        if post.get("available"):
            row("Result sets:", post.get("nsets", 0))
