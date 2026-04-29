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
import shutil
import sys

import click

_MAPDL_CMD_RE = re.compile(r"Mechanical APDL Command: `([^\s<`]+)")

# ---------------------------------------------------------------------------
# RST → terminal formatter
# ---------------------------------------------------------------------------

_RST_SECTION_UNDERLINE = re.compile(r"^[-=~^\"'`#+*]+\s*$")
_RST_ANCHOR = re.compile(r"^\s*\.\.\s+_[\w-]+:\s*$")
_RST_DIRECTIVE = re.compile(
    r"^(\s*)\.\.\s+(note|warning|caution|danger|tip|important)::\s*(.*)$",
    re.IGNORECASE,
)
_RST_RUBRIC = re.compile(r"^\s*\.\.\s+rubric::\s*(.+)$")
_MAPDL_CMD_LINE = re.compile(r"^(Mechanical APDL Command:)\s+(.+)$")

_DIRECTIVE_COLORS: dict[str, str] = {
    "note": "blue",
    "tip": "green",
    "important": "green",
    "warning": "yellow",
    "caution": "yellow",
    "danger": "red",
}


def _hyperlink(url: str, text: str) -> str:
    """Wrap *text* in an OSC 8 terminal hyperlink pointing to *url*.

    Terminals that support OSC 8 (iTerm2, GNOME Terminal, Windows Terminal,
    Konsole, …) render this as a clickable link.  Terminals that do not
    support OSC 8 silently ignore the escape sequences and display *text*
    as plain text.
    """
    return f"\x1b]8;;{url}\x1b\\{text}\x1b]8;;\x1b\\"


def _apply_inline_transforms(line: str) -> str:
    """Apply inline RST → terminal substitutions to a single line.

    Transformations are applied in specificity order so that more specialised
    patterns take precedence over generic ones.
    """
    line = re.sub(r":sub:`([^`]+)`", r"_\1", line)
    line = re.sub(r":sup:`([^`]+)`", r"^\1", line)
    # Explicit-title role: :role:`label <target>` → label
    line = re.sub(r":\w[\w.:-]*:`([^`<>]+)\s*<[^>]*>`", r"\1", line)
    # Generic role: :role:`text` → text
    line = re.sub(r":\w[\w.:-]*:`([^`]+)`", r"\1", line)
    # RST hyperlink: `text <url>`_ → OSC 8 clickable link
    line = re.sub(
        r"`([^`<]+?)\s*<([^>]+)>`_+",
        lambda m: _hyperlink(m.group(2).strip(), m.group(1).strip()),
        line,
    )
    # Double backtick code span: ``x`` → bold `x`
    line = re.sub(
        r"``([^`]+)``", lambda m: click.style(f"`{m.group(1)}`", bold=True), line
    )
    # RST bold: **text** → ANSI bold
    line = re.sub(r"\*\*(.+?)\*\*", lambda m: click.style(m.group(1), bold=True), line)
    # RST bullet list item: "* text" → "• text"
    line = re.sub(r"^(\s*)\* ", r"\1• ", line)
    return line


def _format_rst_for_terminal(text: str) -> str:
    """Lightly format a numpydoc RST docstring for terminal output.

    This is a best-effort formatter that handles the patterns commonly found in
    PyMAPDL command docstrings.  It does **not** require any additional
    dependencies beyond *click*.

    Parameters
    ----------
    text : str
        Raw numpydoc RST docstring (as returned by :func:`inspect.getdoc`).

    Returns
    -------
    str
        The formatted string with ANSI escape sequences suitable for a colour
        terminal.  When colour is unavailable (e.g. piped output), click strips
        the escape codes automatically.
    """
    # Collapse multi-line RST hyperlinks so the single-line regex in
    # _apply_inline_transforms can handle them.  The pattern matches a
    # backtick-delimited link whose URL is on the following (possibly
    # indented) line:  `display text\n    <url>`_
    text = re.sub(
        r"`([^`<\n]+?)\s*\n\s*<([^>]+)>`(_+)",
        r"`\1 <\2>`\3",
        text,
    )

    lines = text.splitlines()
    result: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        next_line = lines[i + 1] if i + 1 < len(lines) else ""

        # Section header: non-empty line followed by an RST underline row of
        # sufficient length.
        if (
            line.strip()
            and _RST_SECTION_UNDERLINE.match(next_line)
            and len(next_line.strip()) >= max(len(line.strip()) - 2, 1)
        ):
            result.append(click.style(line, bold=True, fg="cyan"))
            i += 2  # consume the underline row
            continue

        # RST label anchor (.. _name:) – not meaningful in a terminal
        if _RST_ANCHOR.match(line):
            i += 1
            continue

        # Admonition directives: .. note::, .. warning::, etc.
        m = _RST_DIRECTIVE.match(line)
        if m:
            indent, dtype, rest = m.groups()
            color = _DIRECTIVE_COLORS.get(dtype.lower(), "blue")
            label = click.style(f"[{dtype.upper()}]", bold=True, fg=color)
            rest = _apply_inline_transforms(rest)
            result.append(indent + label + (" " + rest if rest else ""))
            i += 1
            continue

        # .. rubric:: title – treat as a sub-section header
        m = _RST_RUBRIC.match(line)
        if m:
            title = _apply_inline_transforms(m.group(1))
            result.append(click.style(title, bold=True, fg="cyan"))
            i += 1
            continue

        # "Mechanical APDL Command: `CMD <url>`_" – bold the label
        m = _MAPDL_CMD_LINE.match(line)
        if m:
            lbl, rest = m.groups()
            rest = _apply_inline_transforms(rest)
            result.append(click.style(lbl, bold=True) + " " + rest)
            i += 1
            continue

        result.append(_apply_inline_transforms(line))
        i += 1

    return "\n".join(result)


def _echo_doc(formatted: str) -> None:
    """Output *formatted* to stdout, using a pager for long content on a TTY."""
    if sys.stdout.isatty():
        terminal_height = shutil.get_terminal_size(fallback=(80, 24)).lines
        if formatted.count("\n") + 1 > terminal_height - 2:
            click.echo_via_pager(formatted)
            return
    click.echo(formatted)


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
    from ansys.mapdl.core.commands import Commands

    mapping: dict[str, str] = {}
    for attr_name in dir(Commands):
        if attr_name.startswith("_"):
            continue
        attr = getattr(Commands, attr_name, None)
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

    _echo_doc(_format_rst_for_terminal(doc))
