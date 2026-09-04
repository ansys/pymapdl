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

"""``pymapdl exec`` sub-command implementation."""

import select
import sys
from typing import Optional, Sequence, Tuple

import click

from ansys.mapdl.core.cli.constants import DEFAULT_TIMEOUT
from ansys.mapdl.core.cli.helpers import connect_to_instance

STDIN_MARKER = "-"

NO_SOURCE_ERROR = (
    "Provide commands via positional COMMANDS, '-c CMD', '--file PATH', "
    "or stdin ('-')."
)
MULTIPLE_SOURCES_ERROR = (
    "Only one input source may be used at a time: "
    "positional COMMANDS, '-c', '--file', or stdin ('-')."
)
EMPTY_INPUT_ERROR = "No commands to run (input is empty)."


def exec_commands(
    input_arg: Optional[str] = None,
    commands: Sequence[str] = (),
    script_file: Optional[str] = None,
    port: Optional[int] = None,
    ip: Optional[str] = None,
    clear_on_connect: bool = False,
    timeout: int = DEFAULT_TIMEOUT,
) -> str:
    """Send APDL commands to a running MAPDL instance and return its output.

    Exactly one command source must be given: *input_arg*, *commands*,
    *script_file*, or stdin.

    Parameters
    ----------
    input_arg : str, optional
        One or more inline APDL commands, separated by newlines, or ``"-"`` to
        read the commands from stdin. When ``None`` and no other source is
        given, stdin is read as long as it is a pipe carrying data.
    commands : sequence of str, default: ()
        APDL commands. Each item may itself hold several commands separated by
        newlines. All items are joined with newlines and sent as a single
        block.
    script_file : str, optional
        Path to an APDL script file whose content is sent to MAPDL.
    port : int, optional
        gRPC port of the running MAPDL instance. Defaults to ``50052``, or to
        the ``PYMAPDL_PORT`` environment variable when it is set.
    ip : str, optional
        IP address of the running MAPDL instance. Defaults to ``"127.0.0.1"``,
        or to the ``PYMAPDL_IP`` environment variable when it is set.
    clear_on_connect : bool, default: False
        Whether to clear the MAPDL database upon connecting. Off by default so
        that successive calls share the same model state.
    timeout : int, default: 10
        Seconds to wait when establishing the gRPC connection.

    Returns
    -------
    str
        Output returned by MAPDL. Can be empty.

    Raises
    ------
    ValueError
        When no command source or more than one command source is given, or
        when the resolved command block is empty.
    MapdlConnectionError
        When no MAPDL instance can be reached at the given address.
    MapdlRuntimeError
        When MAPDL fails while running the commands.

    Examples
    --------
    Send two commands to the instance running on the default port:

    >>> from ansys.mapdl.core.cli.exec import exec_commands
    >>> print(exec_commands(commands=["/prep7", "BLOCK,0,1,0,1,0,1"]))

    """
    from ansys.mapdl.core.errors import MapdlRuntimeError

    command_block = resolve_command_block(
        input_arg=input_arg, commands=commands, script_file=script_file
    )

    mapdl = connect_to_instance(
        ip=ip, port=port, clear_on_connect=clear_on_connect, timeout=timeout
    )

    try:
        return mapdl.input_strings(command_block) or ""
    except Exception as err:
        raise MapdlRuntimeError(f"Command execution failed — {err}") from err


def resolve_command_block(
    input_arg: Optional[str] = None,
    commands: Sequence[str] = (),
    script_file: Optional[str] = None,
) -> str:
    """Build the APDL command block from the available command sources.

    Parameters
    ----------
    input_arg : str, optional
        Inline APDL commands, or ``"-"`` to read the commands from stdin.
    commands : sequence of str, default: ()
        APDL commands to join with newlines.
    script_file : str, optional
        Path to an APDL script file.

    Returns
    -------
    str
        The APDL commands to send to MAPDL.

    Raises
    ------
    ValueError
        When no source or more than one source is given, or when the resulting
        block is empty.

    Examples
    --------
    >>> from ansys.mapdl.core.cli.exec import resolve_command_block
    >>> resolve_command_block(commands=["/prep7", "SAVE"])
    '/prep7\\nSAVE'

    """
    use_stdin = input_arg == STDIN_MARKER or (
        input_arg is None and not commands and script_file is None and _stdin_has_data()
    )
    use_inline = input_arg is not None and input_arg != STDIN_MARKER

    n_sources = sum([bool(commands), script_file is not None, use_stdin, use_inline])
    if n_sources == 0:
        raise ValueError(NO_SOURCE_ERROR)
    if n_sources > 1:
        raise ValueError(MULTIPLE_SOURCES_ERROR)

    if script_file is not None:
        with open(script_file, "r") as fid:
            command_block = fid.read()
    elif use_stdin:
        command_block = sys.stdin.read()
    elif use_inline:
        command_block = input_arg or ""
    else:
        command_block = "\n".join(commands)

    if not command_block.strip():
        raise ValueError(EMPTY_INPUT_ERROR)

    return command_block


def _stdin_has_data() -> bool:
    """Return ``True`` only when stdin is non-interactive *and* data is ready.

    Uses a zero-timeout ``select`` call so the function never blocks.  Four
    cases are handled:

    * **Normal TTY** – user is typing interactively → ``False``.
    * **In-memory stream** (e.g. Click's ``CliRunner`` in tests) – ``fileno()``
      raises ``io.UnsupportedOperation``.  The stream is fully in-memory so
      data is always available → ``True``.
    * **Real OS pipe/redirect on Unix** – ``select.select`` with a 0-second
      timeout reports whether data is ready → result of the poll.
    * **Windows pipe** – ``select.select`` does not support non-socket file
      handles and raises ``OSError``.  We cannot check data availability, so
      we return ``True`` and let stdin be read normally (may block if nothing
      is piped).

    Returns
    -------
    bool
        Whether stdin can be read without blocking on user input.
    """
    if sys.stdin.isatty():
        return False

    try:
        fd = sys.stdin.fileno()
    except Exception:
        # In-memory stream (StringIO / BytesIO) used by CliRunner or other
        # programmatic callers – always readable, never blocking.
        return True

    try:
        readable, _, _ = select.select([fd], [], [], 0)
        return bool(readable)
    except OSError:
        # Windows: select() only supports sockets.  Cannot check data
        # availability, so fall through to stdin — may block if nothing is
        # piped, but that is the expected behaviour on Windows.
        return True


# ---------------------------------------------------------------------------
# Click wrapper
# ---------------------------------------------------------------------------


@click.command(
    short_help="Execute MAPDL commands on a running instance.",
    help="""Send MAPDL commands to a running MAPDL instance and print the output.

Commands can be supplied via three mutually exclusive sources:

\b
  1. --command / -c  — one or more APDL commands (may be repeated):
       a. Single -c with embedded newlines (most compact):
            bash/zsh:   pymapdl exec -c $'/prep7\\nBLOCK,0,1,0,1,0,1\\nSAVE'
            PowerShell: pymapdl exec -c "/prep7`nBLOCK,0,1,0,1,0,1`nSAVE"
       b. Repeated -c, one command per flag:
            pymapdl exec -c /prep7 -c "BLOCK,0,1,0,1,0,1" -c SAVE
  2. --file / -f  — read commands from an APDL script file:
       pymapdl exec --file my_script.inp
  3. Stdin  — pipe commands in (pass ``-`` explicitly, or omit when piping):
       echo "/prep7" | pymapdl exec
       echo "/prep7" | pymapdl exec -

The instance is targeted by ``--ip`` and ``--port`` (defaults: 127.0.0.1:50052).
MAPDL output is written to stdout so it can be consumed by scripts or LLM agents.
""",
)
@click.argument("input_arg", metavar="[COMMANDS|-]", default=None, required=False)
@click.option(
    "--command",
    "-c",
    "commands",
    multiple=True,
    help="An APDL command to send.  May be repeated to build a multi-command block: "
    '-c /prep7 -c "BLOCK,0,1,0,1,0,1" -c SAVE.  '
    "Alternatively, embed multiple commands in a single value by separating them "
    r"with newlines: -c $'/prep7\nBLOCK,0,1,0,1,0,1' (Bash) or "
    r'"/prep7`nBLOCK,0,1,0,1,0,1" (PowerShell).',
)
@click.option(
    "--file",
    "-f",
    "script_file",
    default=None,
    type=click.Path(exists=True, readable=True, dir_okay=False),
    help="Path to an APDL script file whose contents will be sent to MAPDL.",
)
@click.option(
    "--port",
    default=None,
    type=int,
    show_default=True,
    help="Port of the running MAPDL gRPC server.",
)
@click.option(
    "--ip",
    default=None,
    type=str,
    show_default=True,
    help="IP address of the running MAPDL gRPC server.",
)
@click.option(
    "--clear-on-connect",
    is_flag=True,
    default=False,
    help="Clear the MAPDL database upon connecting.  Off by default so that "
    "successive ``pymapdl exec`` calls share the same model state.",
)
@click.option(
    "--timeout",
    default=10,
    type=int,
    show_default=True,
    help="Seconds to wait when establishing the gRPC connection to the running instance.",
)
def exec_cli(
    input_arg: Optional[str],
    commands: Tuple[str, ...],
    script_file: Optional[str],
    port: int,
    ip: str,
    clear_on_connect: bool,
    timeout: int,
) -> None:
    """Execute MAPDL commands on an already-running instance.

    Parameters
    ----------
    input_arg : str, optional
        Pass ``-`` to read from stdin explicitly.  When omitted and stdin is a
        pipe (i.e. not a TTY), stdin is read automatically — so
        ``echo "/prep7" | pymapdl exec`` works without the ``-``.  Passing
        ``-`` when running interactively is still supported for clarity.
        One or more inline APDL commands, or ``-`` to read from stdin.
        The string is passed to MAPDL exactly as received from the shell —
        no escape sequences are interpreted.  To embed multiple commands,
        use your shell's quoting to produce real newlines:

        - bash/zsh: ``$'/prep7\\nBLOCK,0,1,0,1,0,1'``
        - PowerShell: ``"/prep7`nBLOCK,0,1,0,1,0,1"``

        Windows paths (e.g. ``C:\\new\\file``) are safe because the shell
        passes the backslash characters through unchanged.
    commands : tuple of str
        APDL commands supplied via ``-c`` / ``--command`` options.
        Each value may be a single APDL command **or** multiple commands
        separated by newline characters (e.g.
        ``-c $'/prep7\\nBLOCK,0,1,0,1,0,1'`` in Bash or
        ``-c "/prep7`nBLOCK,0,1,0,1,0,1"`` in PowerShell).
        All values are joined with newlines and sent as a single block.
        Mutually exclusive with *script_file* and stdin.
    script_file : str, optional
        Path to an APDL script file.  Mutually exclusive with *commands* and
        stdin.
    port : Optional[int]
        gRPC port of the running MAPDL instance. Defaults to 50052, unless overridden by the PYMAPDL_PORT environment variable.
    ip : Optional[str]
        IP address of the running MAPDL instance. Defaults to localhost (127.0.0.1), unless overridden by the PYMAPDL_IP environment variable.
    clear_on_connect : bool
        When :class:`True`, clear the MAPDL database upon connecting.
    timeout : int
        Seconds to wait when establishing the gRPC connection.
    """
    from ansys.mapdl.core.cli.helpers import silence_logging
    from ansys.mapdl.core.errors import MapdlRuntimeError

    # Keep stdout clean so that the MAPDL output can be piped.
    silence_logging()

    try:
        output = exec_commands(
            input_arg=input_arg,
            commands=commands,
            script_file=script_file,
            ip=ip,
            port=port,
            clear_on_connect=clear_on_connect,
            timeout=timeout,
        )
    except ValueError as err:
        raise click.UsageError(str(err)) from err
    except MapdlRuntimeError as err:
        click.echo(click.style("ERROR:", fg="red") + f" {err}", err=True)
        sys.exit(1)

    if output:
        click.echo(output)
