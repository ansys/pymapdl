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

"""``pymapdl help <COMMAND>`` sub-command implementation.

RST-to-terminal rendering is delegated to :class:`rich_rst.RestructuredText`,
which uses a ``rich.console.Console`` to produce ANSI-styled output.

Sphinx roles (e.g. ``:ref:``, ``:class:``) that *docutils* cannot parse
natively are stripped in a lightweight pre-processing step so they never
produce noisy "System Message: Problematic Element" panels.

A one-time monkey-patch is applied to fix a ``rich-rst`` bug (≤ 1.3.2) where
a field list that is the *very first* element in a document causes an
``IndexError`` because ``self.renderables`` is empty.
"""

import inspect
import re
import shutil
import sys

import click

# ---------------------------------------------------------------------------
# Regex patterns
# ---------------------------------------------------------------------------

# Matches the MAPDL command name in a docstring line such as:
#   Mechanical APDL Command: `\*VGET <url>`_
#   Mechanical APDL Command: `/PREP7 <url>`_
#   Mechanical APDL Command: `K <url>`_
# The leading ``\`` is the RST escape for ``*``; the capture group includes it.
_MAPDL_CMD_RE = re.compile(r"Mechanical APDL Command: `(\\?\*?/?[^\s<`]+)")

# Detects an ansyshelp.ansys.com URL anywhere in the docstring.
_ANSYS_HELP_URL_RE = re.compile(r"ansyshelp\.ansys\.com")

# Matches the start of the first numpydoc section heading, i.e. a non-blank
# line immediately followed by a line of three or more dashes.
_FIRST_SECTION_RE = re.compile(r"^\S[^\n]*\n-{3,}", re.MULTILINE)

# Sphinx role patterns used to strip custom roles before rich-rst sees them:
#   :role:`display text <target>`  →  display text
#   :role:`text`                   →  text
_SPHINX_ROLE_WITH_TARGET_RE = re.compile(r":\w[\w.:-]*:`([^`<>]+)\s*<[^>]*>`")
_SPHINX_ROLE_SIMPLE_RE = re.compile(r":\w[\w.:-]*:`([^`]+)`")


# ---------------------------------------------------------------------------
# RST → terminal formatter
# ---------------------------------------------------------------------------


def _preprocess_rst(text: str) -> str:
    """Collapse multi-line hyperlinks and strip unsupported Sphinx roles.

    Parameters
    ----------
    text : str
        Raw RST string.

    Returns
    -------
    str
        Pre-processed RST ready for :class:`rich_rst.RestructuredText`.
    """
    # Collapse multi-line RST hyperlinks so docutils can parse them.
    # Matches: `display text\n    <url>`_
    text = re.sub(
        r"`([^`<\n]+?)\s*\n\s*<([^>]+)>`(_+)",
        r"`\1 <\2>`\3",
        text,
    )

    # Strip Sphinx roles that docutils does not understand natively; otherwise
    # rich-rst emits "System Message: Problematic Element" panels for every
    # :ref:, :class:, :func:, etc. in the docstring.
    text = _SPHINX_ROLE_WITH_TARGET_RE.sub(r"``\1``", text)
    text = _SPHINX_ROLE_SIMPLE_RE.sub(r"``\1``", text)

    return text


def _inject_hint(text: str) -> str:
    """Insert a browser-hint paragraph before the first numpydoc section.

    The hint is only injected when the docstring contains an
    ``ansyshelp.ansys.com`` URL, signalling that a full rendered page is
    available online.

    Parameters
    ----------
    text : str
        Pre-processed RST string.

    Returns
    -------
    str
        RST string with the hint paragraph inserted (or unchanged).
    """
    if not _ANSYS_HELP_URL_RE.search(text):
        return text

    m = _FIRST_SECTION_RE.search(text)
    if not m:
        return text

    hint = ".. note::\n\n   💡 For better formatting, visit the link above in your browser.\n\n"
    return text[: m.start()] + hint + text[m.start() :]


def _format_rst_for_terminal(text: str) -> str:
    """Format a numpydoc RST docstring for terminal output using ``rich-rst``.

    The function pre-processes *text* (collapsing multi-line hyperlinks,
    stripping Sphinx roles, injecting an online-help hint when appropriate)
    and then delegates all RST-to-terminal rendering to
    :class:`rich_rst.RestructuredText` via a :class:`rich.console.Console`
    captured into a ``StringIO`` buffer.

    Parameters
    ----------
    text : str
        Raw numpydoc RST docstring (as returned by :func:`inspect.getdoc`).

    Returns
    -------
    str
        The formatted string with ANSI escape sequences suitable for a colour
        terminal.  When colour is unavailable (e.g. piped output), callers may
        strip the sequences via :func:`click.strip_ansi` or similar utilities.
    """
    import io

    from rich.console import Console
    from rich_rst import RestructuredText

    text = _preprocess_rst(text)
    text = _inject_hint(text)

    buf = io.StringIO()
    Console(file=buf, highlight=False, force_terminal=True, width=120).print(
        RestructuredText(text)
    )
    result = buf.getvalue().rstrip("\n")

    # Normalise rich-rst's unique OSC 8 IDs to the standard ``\x1b]8;;url`` form
    # so that two renders of the same docstring produce identical output.
    result = re.sub(r"\x1b\]8;id=[^;]+;", "\x1b]8;;", result)

    return result


def _echo_doc(formatted: str) -> None:
    """Output *formatted* to stdout, using a pager for long content on a TTY."""
    if sys.stdout.isatty():
        terminal_height = shutil.get_terminal_size(fallback=(80, 24)).lines
        if formatted.count("\n") + 1 > terminal_height - 2:
            click.echo_via_pager(formatted)
            return
    click.echo(formatted)


# ---------------------------------------------------------------------------
# Command-map helpers
# ---------------------------------------------------------------------------


def _cmd_to_key(raw_cmd: str) -> str:
    """Convert a raw MAPDL command name (as found in a docstring) to a lookup key.

    The docstring convention uses ``\\*`` (RST-escaped asterisk) for
    ``*``-prefixed commands and a literal ``/`` for slash-prefixed ones.
    This function strips the RST escape backslash, then replaces ``*`` with
    the word ``STAR`` and ``/`` with the word ``SLASH`` so that ``*VGET`` and
    ``VGET`` produce distinct keys (``STARVGET`` vs ``VGET``).

    Parameters
    ----------
    raw_cmd : str
        Command string as captured by :data:`_MAPDL_CMD_RE`, e.g. ``\\*VGET``,
        ``/PREP7``, or ``K``.

    Returns
    -------
    str
        Uppercase lookup key, e.g. ``STARVGET``, ``SLASHPREP7``, or ``K``.
    """
    cmd = raw_cmd.lstrip("\\")  # drop RST escape backslash
    if cmd.startswith("*"):
        return "STAR" + cmd[1:].upper()
    if cmd.startswith("/"):
        return "SLASH" + cmd[1:].upper()
    return cmd.upper()


def _build_command_map() -> dict[str, str]:
    """Build a mapping from normalised MAPDL command names to Python method names.

    Iterates over all non-private callables on the :class:`Commands` class and
    extracts the MAPDL command name from each docstring via the pattern::

        Mechanical APDL Command: `<name> <url>`_

    The extracted key is normalised via :func:`_cmd_to_key`: ``*``-prefixed
    commands become ``STAR<CMD>`` and ``/``-prefixed commands become
    ``SLASH<CMD>``, preserving the distinction between e.g. ``*VGET`` and
    the plain ``VGET`` command.

    Returns
    -------
    dict[str, str]
        Mapping of ``NORMALISED_CMD_NAME`` → ``python_method_name``.

    Examples
    --------
    Build the map and look up methods for a slash and a star command:

    >>> cmd_map = _build_command_map()
    >>> cmd_map["SLASHPREP7"]
    'prep7'
    >>> cmd_map["STARVGET"]
    'starvget'

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
        key = _cmd_to_key(m.group(1))
        if key:
            mapping[key] = attr_name
    return mapping


def _normalise_user_input(command: str) -> str:
    """Normalise a user-supplied MAPDL command name for lookup.

    Mirrors the key convention used by :func:`_build_command_map`: ``*`` (or
    ``\\*``) prefixes become the word ``STAR`` and ``/`` prefixes become the
    word ``SLASH``, so that ``*VGET`` and ``VGET`` remain distinct keys.

    Parameters
    ----------
    command : str
        Raw command name as typed by the user (e.g. ``/PREP7``, ``*VGET``,
        ``K``).

    Returns
    -------
    str
        Normalised uppercase key suitable for use with the map returned by
        :func:`_build_command_map`.

    Examples
    --------
    >>> _normalise_user_input("/PREP7")
    'SLASHPREP7'
    >>> _normalise_user_input("*VGET")
    'STARVGET'
    >>> _normalise_user_input("k")
    'K'

    """
    return _cmd_to_key(command)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


@click.command(
    name="help",
    short_help="Print the docstring for a MAPDL command.",
    help="""Print the Python docstring for a MAPDL command.

COMMAND is the MAPDL command name, including any leading prefix.  ``*``
(or ``\\*``) prefixes are looked up as ``STAR<CMD>`` and ``/`` prefixes
as ``SLASH<CMD>``, so the prefix is significant:

\b
Examples:
  pymapdl help /PREP7
  pymapdl help K
  pymapdl help "*VGET"
  pymapdl help "*ABBR"
""",
)
@click.argument("command")
def help_cmd(command: str) -> None:
    """Print the Python docstring for a MAPDL command.

    Parameters
    ----------
    command : str
        MAPDL command name to look up, including any leading ``/`` or ``*``
        prefix.  ``*`` (and ``\\*``) maps to the ``STAR<CMD>`` key and ``/``
        maps to ``SLASH<CMD>``.

    Examples
    --------
    Print the docstring for the ``/PREP7`` command:

        pymapdl help /PREP7

    Print the docstring for the ``*VGET`` command:

        pymapdl help "*VGET"

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
