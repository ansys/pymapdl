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

"""``pymapdl check`` sub-command implementation."""

import sys
from typing import Any, Callable, Dict, List

import click

from ansys.mapdl.core.cli.constants import (
    DEFAULT_TIMEOUT,
    MAPDL_DEFAULT_IP,
    MAPDL_DEFAULT_PORT,
)
from ansys.mapdl.core.cli.helpers import connect_to_instance

# Width of the key column of the human-readable report.
_KEY_WIDTH = 24


def check(
    ip: str = MAPDL_DEFAULT_IP,
    port: int = MAPDL_DEFAULT_PORT,
    timeout: int = DEFAULT_TIMEOUT,
) -> Dict[str, Any]:
    """Collect diagnostic information from a running MAPDL instance.

    Parameters
    ----------
    ip : str, default: "127.0.0.1"
        IP address of the MAPDL gRPC server.
    port : int, default: 50052
        Port of the MAPDL gRPC server.
    timeout : int, default: 10
        Seconds to wait when establishing the gRPC connection.

    Returns
    -------
    dict
        Nested dictionary with the ``connection``, ``information``,
        ``geometry``, ``mesh``, and ``post_processing`` sections, as returned
        by :func:`ansys.mapdl.core.information.get_mapdl_info`.

    Raises
    ------
    MapdlConnectionError
        When no MAPDL instance can be reached at the given address.

    Examples
    --------
    Report the version of the instance running on the default port:

    >>> from ansys.mapdl.core.cli.check import check
    >>> check()["information"]["mapdl_version"]
    '2021 R2'

    """
    from ansys.mapdl.core.information import get_mapdl_info

    mapdl = connect_to_instance(ip=ip, port=port, timeout=timeout)
    return get_mapdl_info(mapdl)


def format_info(data: Dict[str, Any], style: Callable[[str], str] = str) -> str:
    """Render the output of :func:`check` as a human-readable report.

    Parameters
    ----------
    data : dict
        Nested dictionary as returned by :func:`check`.
    style : callable, default: str
        Callable applied to every section title, used to highlight them. The
        default leaves the titles unchanged.

    Returns
    -------
    str
        Multi-line report ready to be printed.

    Examples
    --------
    Render a report without any highlighting:

    >>> from ansys.mapdl.core.cli.check import check, format_info
    >>> print(format_info(check()))

    """
    lines: List[str] = []

    for section, content in data.items():
        lines.append("")
        lines.append(style(_titleize(section)))

        if "error" in content:
            lines.append(_row("Error", content["error"]))
            continue

        for key, value in content.items():
            if isinstance(value, dict):
                lines.append("")
                lines.append(style(f"  {_titleize(key)}"))
                lines.extend(
                    _row(_titleize(subkey), subvalue, indent=4)
                    for subkey, subvalue in value.items()
                )
            else:
                lines.append(_row(_titleize(key), value))

    return "\n".join(lines)


def _titleize(key: str) -> str:
    """Turn a snake_case key into a human-readable title.

    Parameters
    ----------
    key : str
        Key to convert.

    Returns
    -------
    str
        The key with underscores replaced by spaces and capitalized.
    """
    return key.replace("_", " ").capitalize()


def _row(key: str, value: Any, indent: int = 2) -> str:
    """Format a single ``key``/``value`` line of the report.

    Parameters
    ----------
    key : str
        Name shown in the left column.
    value : any
        Value shown in the right column.
    indent : int, default: 2
        Number of leading spaces.

    Returns
    -------
    str
        The formatted line.
    """
    return f"{' ' * indent}{key.ljust(_KEY_WIDTH)}{value}"


# ---------------------------------------------------------------------------
# Click wrapper
# ---------------------------------------------------------------------------


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
def check_cli(ip: str, port: int, timeout: int, as_json: bool) -> None:
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

    from ansys.mapdl.core.cli.helpers import silence_logging
    from ansys.mapdl.core.errors import MapdlConnectionError

    silence_logging()

    try:
        data = check(ip=ip, port=port, timeout=timeout)
    except MapdlConnectionError as err:
        click.echo(click.style("ERROR:", fg="red") + f" {err}", err=True)
        sys.exit(1)

    if as_json:
        click.echo(json.dumps(data, indent=2))
    else:
        click.echo(format_info(data, style=lambda text: click.style(text, bold=True)))
