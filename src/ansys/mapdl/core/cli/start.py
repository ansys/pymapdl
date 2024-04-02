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

import os
from typing import Dict, Union

import click


@click.command(
    short_help="Launch MAPDL instances.",
    help="""This command aims to replicate the behavior of :func:`ansys.mapdl.core.launcher.launch_mapdl`

For more information see :func:`ansys.mapdl.core.launcher.launch_mapdl`.""",
)
@click.option(
    "--exec_file",
    default=None,
    type=str,
    help="The location of the MAPDL executable.  Will use the cached location when left at the default ``None`` and no environment variable is set. The executable path can be also set through the environment variable ``PYMAPDL_MAPDL_EXEC``.",
)
@click.option(
    "--run_location",
    default=None,
    type=str,
    help="MAPDL working directory.  Defaults to a temporary working directory.  If directory doesn't exist, one is created.",
)
@click.option(
    "--jobname",
    default="file",
    type=str,
    help="MAPDL jobname.  Defaults to ``'file'``.",
)
@click.option(
    "--nproc", type=int, default=2, help="Number of processors.  Defaults to 2."
)
@click.option(
    "--ram",
    default=None,
    type=int,
    help="Fixed amount of memory to request for MAPDL.  If ``None``, then MAPDL will use as much as available on the host machine.",
)
@click.option(
    "--mode",
    type=str,
    default=None,
    help="Argument not allowed in CLI. It will be ignored.",
)
@click.option(
    "--override",
    default=False,
    type=bool,
    help="Attempts to delete the lock file at the ``run_location``. Useful when a prior MAPDL session has exited prematurely and the lock file has not been deleted.",
)
@click.option(
    "--loglevel",
    default="",
    type=str,
    help="Argument not allowed in CLI. It will be ignored.",
)
@click.option(
    "--additional_switches",
    default="",
    type=str,
    help="Additional switches for MAPDL, for example ``'aa_r'``, the academic research license. Avoid adding switches like ``-i``, ``-o`` or ``-b`` as these are already included to start up the MAPDL server.",
)
@click.option(
    "--start_timeout",
    default=45,
    type=int,
    help="Maximum allowable time to connect to the MAPDL server.",
)
@click.option(
    "--port",
    default=None,
    type=int,
    help="Port to launch MAPDL gRPC on.  Final port will be the first port available after (or including) this port.  Defaults to 50052. You can also override the port default with the environment variable ``PYMAPDL_PORT=<VALID PORT>`` This argument has priority over the environment variable.",
)
@click.option(
    "--cleanup_on_exit",
    default=False,
    type=bool,
    help="Argument not allowed in CLI. It will be ignored.",
)
@click.option(
    "--start_instance",
    default=None,
    type=bool,
    help="Argument not allowed in CLI. It will be ignored.",
)
@click.option(
    "--ip",
    default=None,
    type=str,
    help="Argument not allowed in CLI. It will be ignored",
)
@click.option(
    "--clear_on_connect",
    default=False,
    type=bool,
    help="Argument not allowed in CLI. It will be ignored",
)
@click.option(
    "--log_apdl",
    default=None,
    type=str,
    help="Argument not allowed in CLI. It will be ignored.",
)
@click.option(
    "--remove_temp_files",
    default=None,
    type=str,
    help="Argument not allowed in CLI. It will be ignored.",
)
@click.option(
    "--remove_temp_dir_on_exit",
    default=False,
    type=bool,
    help="Argument not allowed in CLI. It will be ignored.",
)
@click.option(
    "--verbose_mapdl",
    default=None,
    type=str,
    help="Argument not allowed in CLI. It will be ignored.",
)
@click.option(
    "--license_server_check",
    default=False,
    type=bool,
    help="Argument not allowed in CLI. It will be ignored.",
)
@click.option(
    "--license_type",
    default=None,
    type=str,
    help="Enable license type selection. You can input a string for its license name (for example ``'meba'`` or ``'ansys'``) or its description ('enterprise solver' or 'enterprise' respectively). You can also use legacy licenses (for example ``'aa_t_a'``) but it will also raise a warning. If it is not used (``None``), no specific license will be requested, being up to the license server to provide a specific license type. Default is ``None``.",
)
@click.option(
    "--print_com",
    default=False,
    type=bool,
    help="Argument not allowed in CLI. It will be ignored.",
)
@click.option(
    "--add_env_vars",
    default=None,
    type=str,
    help="Argument not allowed in CLI. It will be ignored.",
)
@click.option(
    "--replace_env_vars",
    default=None,
    type=str,
    help="Argument not allowed in CLI. It will be ignored.",
)
@click.option(
    "--version",
    default=None,
    type=str,
    help="Version of MAPDL to launch. If ``None``, the latest version is used. Versions can be provided as integers (i.e. ``version=222``) or floats (i.e. ``version=22.2``). To retrieve the available installed versions, use the function :meth:`ansys.tools.path.path.get_available_ansys_installations`.",
)
def start(
    exec_file: str,
    run_location: str,
    jobname: str,
    nproc: Union[int, str],
    ram: Union[int, str],
    mode: str,  # ignored
    override: bool,
    loglevel: str,  # ignored
    additional_switches: str,
    start_timeout: Union[int, str],
    port: Union[int, str],
    cleanup_on_exit: bool,  # ignored
    start_instance: bool,  # ignored
    ip: str,
    clear_on_connect: bool,  # ignored
    log_apdl: bool,  # ignored
    remove_temp_files: bool,  # ignored
    remove_temp_dir_on_exit: bool,  # ignored
    verbose_mapdl: bool,  # ignored
    license_server_check: bool,  # ignored
    license_type: str,
    print_com: bool,  # ignored
    add_env_vars: Dict[str, str],  # ignored
    replace_env_vars: Dict[str, str],  # ignored
    version: Union[int, str],
):
    from ansys.mapdl.core.launcher import launch_mapdl

    if mode:
        click.echo(
            click.style("Warn:", fg="yellow")
            + " The following argument is not allowed in CLI: 'mode'.\nIgnoring argument."
        )

    if loglevel:
        click.echo(
            click.style("Warn:", fg="yellow")
            + " The following argument is not allowed in CLI: 'loglevel'.\nIgnoring argument."
        )

    if cleanup_on_exit:
        click.echo(
            click.style("Warn:", fg="yellow")
            + " The following argument is not allowed in CLI: 'cleanup_on_exit'.\nIgnoring argument."
        )

    if start_instance:
        click.echo(
            click.style("Warn:", fg="yellow")
            + " The following argument is not allowed in CLI: 'start_instance'.\nIgnoring argument."
        )

    if ip:
        click.echo(
            click.style("Warn:", fg="yellow")
            + " The following argument is not allowed in CLI: 'ip'.\nIgnoring argument."
        )

    if clear_on_connect:
        click.echo(
            click.style("Warn:", fg="yellow")
            + " The following argument is not allowed in CLI: 'clear_on_connect'.\nIgnoring argument."
        )

    if log_apdl:
        click.echo(
            click.style("Warn:", fg="yellow")
            + " The following argument is not allowed in CLI: 'log_apdl'.\nIgnoring argument."
        )

    if remove_temp_files:
        click.echo(
            click.style("Warn:", fg="yellow")
            + " The following argument is not allowed in CLI: 'remove_temp_files'.\nIgnoring argument."
        )

    if remove_temp_dir_on_exit:
        click.echo(
            click.style("Warn:", fg="yellow")
            + " The following argument is not allowed in CLI: 'remove_temp_dir_on_exit'.\nIgnoring argument."
        )

    if verbose_mapdl:
        click.echo(
            click.style("Warn:", fg="yellow")
            + " The following argument is not allowed in CLI: 'verbose_mapdl'.\nIgnoring argument."
        )

    if print_com:
        click.echo(
            click.style("Warn:", fg="yellow")
            + " The following argument is not allowed in CLI: 'print_com'.\nIgnoring argument."
        )

    if add_env_vars:
        click.echo(
            click.style("Warn:", fg="yellow")
            + " The following argument is not allowed in CLI: 'add_env_vars'.\nIgnoring argument."
        )

    if replace_env_vars:
        click.echo(
            click.style("Warn:", fg="yellow")
            + " The following argument is not allowed in CLI: 'replace_env_vars'.\nIgnoring argument."
        )

    if license_server_check:
        click.echo(
            click.style("Warn:", fg="yellow")
            + " The following argument is not allowed in CLI: 'license_server_check'.\nIgnoring argument."
        )

    # Ignoring env var if using CLI
    if "PYMAPDL_START_INSTANCE" in os.environ:
        os.environ.pop("PYMAPDL_START_INSTANCE")

    out = launch_mapdl(
        exec_file=exec_file,
        just_launch=True,
        run_location=run_location,
        jobname=jobname,
        nproc=nproc,
        ram=ram,
        override=override,
        additional_switches=additional_switches,
        start_timeout=start_timeout,
        port=port,
        license_server_check=license_server_check,
        license_type=license_type,
        version=version,
    )

    if len(out) == 3:
        header = f"Launched an MAPDL instance (PID={out[2]}) at "
    else:
        header = "Launched an MAPDL instance at "

    click.echo(click.style("Success: ", fg="green") + header + f"{out[0]}:{out[1]}")
