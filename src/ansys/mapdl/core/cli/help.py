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

import inspect
import re
import sys

import click

_MAPDL_CMD_RE = re.compile(r"Mechanical APDL Command: `([^\s<`]+)")


def _build_command_map() -> dict[str, str]:
    """Build a mapping from normalised MAPDL command names to Python method names.

    Iterates over all non-private callables on the :class:`Mapdl` class and
    extracts the MAPDL command name from each docstring via the pattern::

        Mechanical APDL Command: `<name> <url>`_

    The extracted key is normalised by stripping any leading ``\\``, ``/``, or
    ``*`` characters and converting to uppercase.

    Returns
    -------
    dict[str, str]
        Mapping of ``NORMALISED_CMD_NAME`` → ``python_method_name``.

    Examples
    --------
    Build the map and look up the method for the ``PREP7`` command:

    >>> cmd_map = _build_command_map()
    >>> cmd_map["PREP7"]
    'prep7'

    """
    from ansys.mapdl.core import Mapdl

    mapping: dict[str, str] = {}
    for attr_name in dir(Mapdl):
        if attr_name.startswith("_"):
            continue
        attr = getattr(Mapdl, attr_name, None)
        if not callable(attr):
            continue
        doc = getattr(attr, "__doc__", None) or ""
        m = _MAPDL_CMD_RE.search(doc)
        if not m:
            continue
        raw_cmd = m.group(1)
        # Strip leading backslash, slash, or asterisk then uppercase
        normalised = raw_cmd.lstrip("\\/*").upper()
        if normalised:
            mapping[normalised] = attr_name
    return mapping


def _normalise_user_input(command: str) -> str:
    """Normalise a user-supplied MAPDL command name for lookup.

    Strips any leading ``/``, ``*``, or ``\\*`` characters and converts the
    result to uppercase.

    Parameters
    ----------
    command : str
        Raw command name as typed by the user (e.g. ``/PREP7``, ``*ABBR``,
        ``K``).

    Returns
    -------
    str
        Normalised uppercase key suitable for use with the map returned by
        :func:`_build_command_map`.

    Examples
    --------
    >>> _normalise_user_input("/PREP7")
    'PREP7'
    >>> _normalise_user_input("*ABBR")
    'ABBR'
    >>> _normalise_user_input("k")
    'K'

    """
    return command.lstrip("\\/*").upper()


@click.command(
    name="help",
    short_help="Print the docstring for a MAPDL command.",
    help="""Print the Python docstring for a MAPDL command.

COMMAND is the MAPDL command name.  Leading ``/``, ``*``, or ``\\*``
prefixes are accepted and silently stripped before the lookup, so all
of the following are equivalent:

\b
Examples:
  pymapdl help PREP7
  pymapdl help /PREP7
  pymapdl help K
  pymapdl help *ABBR
  pymapdl help ABBR
""",
)
@click.argument("command")
def help_cmd(command: str) -> None:
    """Print the Python docstring for a MAPDL command.

    Parameters
    ----------
    command : str
        MAPDL command name to look up.  Leading ``/``, ``*``, or ``\\*``
        prefixes are stripped automatically before the lookup.

    Examples
    --------
    Print the docstring for the ``/PREP7`` command:

        pymapdl help /PREP7

    Print the docstring for the ``*ABBR`` command:

        pymapdl help *ABBR

    Print the docstring for the ``K`` command:

        pymapdl help K

    """
    from ansys.mapdl.core import Mapdl

    key = _normalise_user_input(command)
    cmd_map = _build_command_map()

    method_name = cmd_map.get(key)
    if method_name is None:
        click.echo(
            click.style("ERROR:", fg="red")
            + f" No PyMAPDL method found for MAPDL command {command!r}.\n"
            "Use 'pymapdl help <COMMAND>' where COMMAND is a valid MAPDL command name.",
            err=True,
        )
        sys.exit(1)

    method = getattr(Mapdl, method_name)
    doc = inspect.getdoc(method)
    if not doc:
        click.echo(
            click.style("ERROR:", fg="red")
            + f" Method {method_name!r} has no docstring.",
            err=True,
        )
        sys.exit(1)

    click.echo(doc)
