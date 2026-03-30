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
from typing import Optional, Tuple

import click


@click.command(
    short_help="Run MAPDL commands on a running instance.",
    help="""Send MAPDL commands to a running MAPDL instance and print the output.

Commands can be supplied in three mutually exclusive ways:

\b
  1. Repeated --command / -c options (recommended for scripting and LLM use):
       pymapdl run -c /prep7 -c "BLOCK,0,1,0,1,0,1" -c SAVE
  2. File — read commands from an APDL script file:
       pymapdl run --file my_script.inp
  3. Stdin — pass ``-`` as the positional argument and pipe commands in:
       echo "/prep7" | pymapdl run -

The instance is targeted by ``--ip`` and ``--port`` (defaults: 127.0.0.1:50052).
MAPDL output is written to stdout so it can be consumed by scripts or LLM agents.
""",
)
@click.argument("stdin_marker", metavar="[-]", default=None, required=False)
@click.option(
    "--command",
    "-c",
    "commands",
    multiple=True,
    help="An APDL command to send.  May be repeated to build a multi-command block: "
    '-c /prep7 -c "BLOCK,0,1,0,1,0,1" -c SAVE',
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
    default=50052,
    type=int,
    show_default=True,
    help="Port of the running MAPDL gRPC server.",
)
@click.option(
    "--ip",
    default="127.0.0.1",
    type=str,
    show_default=True,
    help="IP address of the running MAPDL gRPC server.",
)
@click.option(
    "--clear-on-connect",
    is_flag=True,
    default=False,
    help="Clear the MAPDL database upon connecting.  Off by default so that "
    "successive ``pymapdl run`` calls share the same model state.",
)
@click.option(
    "--timeout",
    default=10,
    type=int,
    show_default=True,
    help="Seconds to wait when establishing the gRPC connection to the running instance.",
)
def run(
    stdin_marker: Optional[str],
    commands: Tuple[str, ...],
    script_file: Optional[str],
    port: int,
    ip: str,
    clear_on_connect: bool,
    timeout: int,
) -> None:
    """Run MAPDL commands on an already-running instance.

    Parameters
    ----------
    stdin_marker : str, optional
        Pass ``-`` to read commands from stdin.
    commands : tuple of str
        APDL commands supplied via repeated ``-c`` / ``--command`` options.
        Each value is one APDL command; they are joined with newlines before
        being sent as a single block.
    script_file : str, optional
        Path to an APDL script file.  Mutually exclusive with *commands* and
        stdin.
    port : int
        gRPC port of the running MAPDL instance.
    ip : str
        IP address of the running MAPDL instance.
    clear_on_connect : bool
        When :class:`True`, clear the MAPDL database upon connecting.
    timeout : int
        Seconds to wait when establishing the gRPC connection.
    """
    import logging

    # ------------------------------------------------------------------ #
    # Resolve the command source                                           #
    # ------------------------------------------------------------------ #

    use_stdin = stdin_marker == "-"
    n_sources = sum([bool(commands), script_file is not None, use_stdin])

    if stdin_marker is not None and stdin_marker != "-":
        raise click.UsageError(
            f"Unexpected positional argument {stdin_marker!r}.  "
            "Use '-' to read from stdin, or supply commands via -c / --file."
        )
    if n_sources == 0:
        raise click.UsageError(
            "Provide commands via '-c CMD', '--file PATH', or pipe them via stdin ('-')."
        )
    if n_sources > 1:
        raise click.UsageError(
            "Only one input source may be used at a time: '-c', '--file', or stdin ('-')."
        )

    if script_file is not None:
        with open(script_file, "r") as fh:
            cmd_block = fh.read()
    elif use_stdin:
        cmd_block = sys.stdin.read()
    else:
        cmd_block = "\n".join(commands)

    if not cmd_block.strip():
        raise click.UsageError("No commands to run (input is empty).")

    # ------------------------------------------------------------------ #
    # Suppress all PyMAPDL/grpc logging to keep stdout clean              #
    # ------------------------------------------------------------------ #
    from ansys.mapdl.core import LOG

    LOG.setLevel(logging.CRITICAL + 1)
    if LOG.std_out_handler:
        LOG.std_out_handler.setLevel(logging.CRITICAL + 1)

    # ------------------------------------------------------------------ #
    # Connect to the existing MAPDL instance                              #
    # ------------------------------------------------------------------ #
    try:
        from ansys.mapdl.core.launcher.config import resolve_launch_config
        from ansys.mapdl.core.launcher.connection import connect_to_existing

        config = resolve_launch_config(
            ip=ip,
            port=port,
            start_instance=False,
            clear_on_connect=clear_on_connect,
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

    # ------------------------------------------------------------------ #
    # Execute commands and stream output                                  #
    # ------------------------------------------------------------------ #
    try:
        output = mapdl.input_strings(cmd_block)
        if output:
            click.echo(output)

    except Exception as e:
        click.echo(
            click.style("ERROR:", fg="red") + f" Command execution failed — {e}",
            err=True,
        )
        sys.exit(1)
