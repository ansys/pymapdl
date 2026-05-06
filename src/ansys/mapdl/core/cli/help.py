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
from docutils import nodes
from docutils.core import publish_doctree

_MAPDL_CMD_RE = re.compile(r"Mechanical APDL Command: `([^\s<`]+)")

# ---------------------------------------------------------------------------
# RST → terminal formatter
# ---------------------------------------------------------------------------

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


class _TerminalVisitor(nodes.NodeVisitor):
    """Walk a docutils document tree and produce ANSI-styled terminal output.

    Uses ``click.style()`` for all colour/bold formatting so that click's
    automatic colour-stripping applies when stdout is not a TTY.
    ``rich`` is used only for table rendering (captured to a string).
    """

    # Allow visiting node types that have no explicit handler without raising.
    # Override unknown_visit/unknown_departure so unrecognised nodes are skipped.

    def unknown_visit(self, node: nodes.Node) -> None:
        pass

    def unknown_departure(self, node: nodes.Node) -> None:
        pass

    def __init__(self, document: nodes.document) -> None:
        super().__init__(document)
        self.output: list[str] = []
        self._indent: int = 0
        # Stack of inline string buffers.  Block nodes push a new list on
        # entry; inline nodes append styled text to the top list; block nodes
        # pop + emit on departure.
        self._inline_stack: list[list[str]] = [[]]
        # Stack of list types: None → bullet, int → current enum counter.
        self._list_stack: list[int | None] = []
        # Prefix to inject before the very next _emit call (used by list items).
        self._pending_prefix: str = ""
        # Depth inside list items — suppresses the trailing blank after paragraphs.
        self._list_item_depth: int = 0
        # URL from the "Mechanical APDL Command:" hyperlink, used to emit a
        # "see online docs" hint before the first section.
        self._cmd_url: str = ""
        self._cmd_url_hint_emitted: bool = False

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _emit(self, text: str = "") -> None:
        """Append *text* (with current indentation) to output."""
        if not text:
            # Avoid consecutive blank lines.
            if not self.output or self.output[-1] == "":
                return
            self.output.append("")
            return
        prefix = " " * self._indent
        lines = text.splitlines()
        for i, line in enumerate(lines):
            if i == 0 and self._pending_prefix:
                # The indent already accounts for the prefix width; subtract it
                # so the first line starts at the outer indentation level.
                outer = " " * max(0, self._indent - len(self._pending_prefix))
                self.output.append(outer + self._pending_prefix + line)
                self._pending_prefix = ""
            else:
                self.output.append(prefix + line)

    def _push_inline(self) -> None:
        self._inline_stack.append([])

    def _pop_inline(self) -> str:
        return "".join(self._inline_stack.pop())

    def _append_inline(self, text: str) -> None:
        self._inline_stack[-1].append(text)

    # ------------------------------------------------------------------
    # Text node
    # ------------------------------------------------------------------

    def visit_Text(self, node: nodes.Text) -> None:
        # docutils uses \x00 internally as an escape marker (e.g. \* → \x00*)
        # and it can leak into Text nodes.  Strip it so terminals never see ^@.
        self._append_inline(str(node).replace("\x00", ""))

    def depart_Text(self, node: nodes.Text) -> None:
        pass

    # ------------------------------------------------------------------
    # Document / section structure
    # ------------------------------------------------------------------

    def visit_document(self, node: nodes.document) -> None:
        pass

    def depart_document(self, node: nodes.document) -> None:
        pass

    def visit_section(self, node: nodes.section) -> None:
        if self._cmd_url and not self._cmd_url_hint_emitted:
            self._cmd_url_hint_emitted = True
            hint = click.style(
                "💡 For better formatting, open the link above in your browser.",
                fg="bright_black",
            )
            self._emit(hint)
            self._emit()

    def depart_section(self, node: nodes.section) -> None:
        pass

    def visit_title(self, node: nodes.title) -> None:
        self._push_inline()

    def depart_title(self, node: nodes.title) -> None:
        text = self._pop_inline()
        self._emit(click.style(text, bold=True, fg="cyan"))
        self._emit()

    def visit_subtitle(self, node: nodes.subtitle) -> None:
        self._push_inline()

    def depart_subtitle(self, node: nodes.subtitle) -> None:
        text = self._pop_inline()
        self._emit(click.style(text, bold=True))
        self._emit()

    def visit_rubric(self, node: nodes.rubric) -> None:
        self._push_inline()

    def depart_rubric(self, node: nodes.rubric) -> None:
        text = self._pop_inline()
        self._emit(click.style(text, bold=True, fg="cyan"))
        self._emit()

    def visit_transition(self, node: nodes.transition) -> None:
        self._emit(click.style("─" * 40, fg="white", dim=True))
        self._emit()
        raise nodes.SkipNode

    # ------------------------------------------------------------------
    # Body elements
    # ------------------------------------------------------------------

    def visit_paragraph(self, node: nodes.paragraph) -> None:
        self._push_inline()

    def depart_paragraph(self, node: nodes.paragraph) -> None:
        text = self._pop_inline()
        self._emit(text)
        # Suppress blank line between compact list items.
        if self._list_item_depth == 0:
            self._emit()

    def visit_block_quote(self, node: nodes.block_quote) -> None:
        self._indent += 4

    def depart_block_quote(self, node: nodes.block_quote) -> None:
        self._indent -= 4

    def visit_literal_block(self, node: nodes.literal_block) -> None:
        code = node.astext()
        self._indent += 4
        for line in code.splitlines():
            self._emit(click.style(line, fg="bright_black"))
        self._indent -= 4
        self._emit()
        raise nodes.SkipNode

    def visit_line_block(self, node: nodes.line_block) -> None:
        pass

    def depart_line_block(self, node: nodes.line_block) -> None:
        self._emit()

    def visit_line(self, node: nodes.line) -> None:
        self._push_inline()

    def depart_line(self, node: nodes.line) -> None:
        self._emit(self._pop_inline())

    # ------------------------------------------------------------------
    # Inline markup
    # ------------------------------------------------------------------

    def visit_strong(self, node: nodes.strong) -> None:
        self._push_inline()

    def depart_strong(self, node: nodes.strong) -> None:
        self._append_inline(click.style(self._pop_inline(), bold=True))

    def visit_emphasis(self, node: nodes.emphasis) -> None:
        self._push_inline()

    def depart_emphasis(self, node: nodes.emphasis) -> None:
        self._append_inline(click.style(self._pop_inline(), italic=True))

    def visit_literal(self, node: nodes.literal) -> None:
        self._push_inline()

    def depart_literal(self, node: nodes.literal) -> None:
        self._append_inline(click.style(f"`{self._pop_inline()}`", bold=True))

    def visit_subscript(self, node: nodes.subscript) -> None:
        self._push_inline()

    def depart_subscript(self, node: nodes.subscript) -> None:
        self._append_inline(f"_{self._pop_inline()}")

    def visit_superscript(self, node: nodes.superscript) -> None:
        self._push_inline()

    def depart_superscript(self, node: nodes.superscript) -> None:
        self._append_inline(f"^{self._pop_inline()}")

    def visit_reference(self, node: nodes.reference) -> None:
        self._push_inline()

    def depart_reference(self, node: nodes.reference) -> None:
        text = self._pop_inline()
        url = node.get("refuri", "")
        if url and not self._cmd_url:
            self._cmd_url = url
        self._append_inline(_hyperlink(url, text) if url else text)

    def visit_title_reference(self, node: nodes.title_reference) -> None:
        self._push_inline()

    def depart_title_reference(self, node: nodes.title_reference) -> None:
        self._append_inline(self._pop_inline())

    def visit_problematic(self, node: nodes.problematic) -> None:
        # Sphinx roles (e.g. :class:, :func:, :ref:) that docutils cannot
        # parse natively become problematic nodes containing the raw role text.
        # Push a buffer so we can strip the role syntax on departure.
        self._push_inline()

    def depart_problematic(self, node: nodes.problematic) -> None:
        text = self._pop_inline()
        # Strip :role:`label <target>` → 'label', or :role:`text` → 'text'.
        text = re.sub(r":\w[\w.:-]*:`([^`<>]+)\s*<[^>]*>`", r"'\1'", text)
        text = re.sub(r":\w[\w.:-]*:`([^`]+)`", r"'\1'", text)
        self._append_inline(text)

    def visit_inline(self, node: nodes.inline) -> None:
        self._push_inline()

    def depart_inline(self, node: nodes.inline) -> None:
        self._append_inline(self._pop_inline())

    # ------------------------------------------------------------------
    # Lists
    # ------------------------------------------------------------------

    def visit_bullet_list(self, node: nodes.bullet_list) -> None:
        self._list_stack.append(None)

    def depart_bullet_list(self, node: nodes.bullet_list) -> None:
        self._list_stack.pop()
        self._emit()

    def visit_enumerated_list(self, node: nodes.enumerated_list) -> None:
        self._list_stack.append(0)

    def depart_enumerated_list(self, node: nodes.enumerated_list) -> None:
        self._list_stack.pop()
        self._emit()

    def visit_list_item(self, node: nodes.list_item) -> None:
        self._list_item_depth += 1
        if self._list_stack:
            top = self._list_stack[-1]
            if top is None:
                self._pending_prefix = "• "
            else:
                counter = top + 1
                self._list_stack[-1] = counter
                self._pending_prefix = f"{counter}. "
        else:
            self._pending_prefix = "• "
        self._indent += len(self._pending_prefix)

    def depart_list_item(self, node: nodes.list_item) -> None:
        self._list_item_depth -= 1
        # Determine prefix length to restore indent.  The prefix was set in
        # visit_list_item; by now it may have been consumed (cleared) or not.
        if self._list_stack:
            top = self._list_stack[-1]
            prefix_len = len(f"{top}. ") if isinstance(top, int) else len("• ")
        else:
            prefix_len = len("• ")
        self._indent -= prefix_len
        self._pending_prefix = ""

    # ------------------------------------------------------------------
    # Definition lists
    # ------------------------------------------------------------------

    def visit_definition_list(self, node: nodes.definition_list) -> None:
        pass

    def depart_definition_list(self, node: nodes.definition_list) -> None:
        self._emit()

    def visit_definition_list_item(self, node: nodes.definition_list_item) -> None:
        pass

    def depart_definition_list_item(self, node: nodes.definition_list_item) -> None:
        pass

    def visit_term(self, node: nodes.term) -> None:
        self._push_inline()

    def depart_term(self, node: nodes.term) -> None:
        self._emit(click.style(self._pop_inline(), bold=True))

    def visit_classifier(self, node: nodes.classifier) -> None:
        self._push_inline()

    def depart_classifier(self, node: nodes.classifier) -> None:
        # Append to the last emitted term line
        classifier_text = click.style(f" : {self._pop_inline()}", fg="bright_black")
        if self.output:
            self.output[-1] += classifier_text

    def visit_definition(self, node: nodes.definition) -> None:
        self._indent += 4

    def depart_definition(self, node: nodes.definition) -> None:
        self._indent -= 4

    # ------------------------------------------------------------------
    # Field lists (numpydoc Parameters, Returns, …)
    # ------------------------------------------------------------------

    def visit_field_list(self, node: nodes.field_list) -> None:
        pass

    def depart_field_list(self, node: nodes.field_list) -> None:
        self._emit()

    def visit_field(self, node: nodes.field) -> None:
        pass

    def depart_field(self, node: nodes.field) -> None:
        pass

    def visit_field_name(self, node: nodes.field_name) -> None:
        self._push_inline()

    def depart_field_name(self, node: nodes.field_name) -> None:
        self._emit(click.style(self._pop_inline(), bold=True))

    def visit_field_body(self, node: nodes.field_body) -> None:
        self._indent += 4

    def depart_field_body(self, node: nodes.field_body) -> None:
        self._indent -= 4

    # ------------------------------------------------------------------
    # Admonitions (note, warning, caution, danger, tip, important)
    # ------------------------------------------------------------------

    def _visit_admonition(self, node: nodes.Admonition, name: str) -> None:
        color = _DIRECTIVE_COLORS.get(name, "blue")
        label = click.style(f"[{name.upper()}]", bold=True, fg=color)
        self._emit(label)
        self._indent += 2

    def _depart_admonition(self, node: nodes.Admonition) -> None:
        self._indent -= 2
        self._emit()

    def visit_note(self, node: nodes.note) -> None:
        self._visit_admonition(node, "note")

    def depart_note(self, node: nodes.note) -> None:
        self._depart_admonition(node)

    def visit_warning(self, node: nodes.warning) -> None:
        self._visit_admonition(node, "warning")

    def depart_warning(self, node: nodes.warning) -> None:
        self._depart_admonition(node)

    def visit_caution(self, node: nodes.caution) -> None:
        self._visit_admonition(node, "caution")

    def depart_caution(self, node: nodes.caution) -> None:
        self._depart_admonition(node)

    def visit_danger(self, node: nodes.danger) -> None:
        self._visit_admonition(node, "danger")

    def depart_danger(self, node: nodes.danger) -> None:
        self._depart_admonition(node)

    def visit_tip(self, node: nodes.tip) -> None:
        self._visit_admonition(node, "tip")

    def depart_tip(self, node: nodes.tip) -> None:
        self._depart_admonition(node)

    def visit_important(self, node: nodes.important) -> None:
        self._visit_admonition(node, "important")

    def depart_important(self, node: nodes.important) -> None:
        self._depart_admonition(node)

    def visit_admonition(self, node: nodes.admonition) -> None:
        # Generic admonition (with a custom title child node).
        self._emit(click.style("[NOTE]", bold=True, fg="blue"))
        self._indent += 2

    def depart_admonition(self, node: nodes.admonition) -> None:
        self._indent -= 2
        self._emit()

    # ------------------------------------------------------------------
    # Tables — rendered via rich (only rich usage in this module)
    # ------------------------------------------------------------------

    def visit_table(self, node: nodes.table) -> None:
        from io import StringIO

        from rich.console import Console
        from rich.table import Table

        rich_table = Table(show_header=True, header_style="bold cyan")

        # Navigate: table > tgroup > thead/tbody
        tgroup = node.first_child_matching_class(nodes.tgroup)
        if tgroup is None:
            raise nodes.SkipNode

        tgroup_node = node.children[tgroup]
        thead_idx = tgroup_node.first_child_matching_class(nodes.thead)
        tbody_idx = tgroup_node.first_child_matching_class(nodes.tbody)

        def _row_texts(row_node: nodes.row) -> list[str]:
            return [entry.astext() for entry in row_node.children]

        if thead_idx is not None:
            for row in tgroup_node.children[thead_idx].children:
                for col_text in _row_texts(row):
                    rich_table.add_column(col_text)
        else:
            # No header row: infer column count from first body row.
            if tbody_idx is not None and tgroup_node.children[tbody_idx].children:
                for _ in _row_texts(tgroup_node.children[tbody_idx].children[0]):
                    rich_table.add_column("")

        if tbody_idx is not None:
            for row in tgroup_node.children[tbody_idx].children:
                rich_table.add_row(*_row_texts(row))

        buf = StringIO()
        Console(file=buf, highlight=False).print(rich_table)
        rendered = buf.getvalue().rstrip("\n")
        self._emit(rendered)
        self._emit()
        raise nodes.SkipNode

    # ------------------------------------------------------------------
    # Nodes to skip silently
    # ------------------------------------------------------------------

    def visit_target(self, node: nodes.target) -> None:
        raise nodes.SkipNode

    def visit_comment(self, node: nodes.comment) -> None:
        raise nodes.SkipNode

    def visit_system_message(self, node: nodes.system_message) -> None:
        raise nodes.SkipNode

    def visit_raw(self, node: nodes.raw) -> None:
        raise nodes.SkipNode

    def visit_meta(self, node: nodes.meta) -> None:
        raise nodes.SkipNode

    def visit_decoration(self, node: nodes.decoration) -> None:
        raise nodes.SkipNode

    def visit_image(self, node: nodes.image) -> None:
        raise nodes.SkipNode

    def visit_footnote(self, node: nodes.footnote) -> None:
        raise nodes.SkipNode

    def visit_citation(self, node: nodes.citation) -> None:
        raise nodes.SkipNode

    def visit_pending(self, node: nodes.pending) -> None:
        raise nodes.SkipNode


def _format_rst_for_terminal(text: str) -> str:
    """Format a numpydoc RST docstring for terminal output.

    Parses the RST using docutils and walks the document tree with
    :class:`_TerminalVisitor` to produce ANSI-styled text via
    ``click.style()``.

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
    # Collapse multi-line RST hyperlinks so docutils can parse them.
    # Matches: `display text\n    <url>`_
    text = re.sub(
        r"`([^`<\n]+?)\s*\n\s*<([^>]+)>`(_+)",
        r"`\1 <\2>`\3",
        text,
    )
    document = publish_doctree(text, settings_overrides={"report_level": 5})
    visitor = _TerminalVisitor(document)
    document.walkabout(visitor)
    # Strip trailing blank lines then join.
    lines = visitor.output
    while lines and not lines[-1].strip():
        lines.pop()
    return "\n".join(lines)


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
