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

"""``pymapdl convert`` sub-command implementation."""

import sys
from typing import Optional, TextIO, Union

import click

from ansys.mapdl.core.plotting import GraphicsBackend


def convert(
    apdl_strings: str,
    loglevel: str = "WARNING",
    auto_exit: bool = True,
    line_ending: Optional[str] = None,
    exec_file: Optional[str] = None,
    macros_as_functions: bool = True,
    use_function_names: bool = True,
    show_log: bool = False,
    add_imports: bool = True,
    comment_solve: bool = False,
    cleanup_output: bool = True,
    header: Union[bool, str] = True,
    print_com: bool = True,
    only_commands: bool = False,
    graphics_backend: Optional[Union[str, GraphicsBackend]] = None,
    clear_at_start: bool = False,
    check_parameter_names: bool = False,
) -> str:
    """Convert an APDL script to PyMAPDL code.

    Parameters
    ----------
    apdl_strings : str
        APDL code to convert.
    loglevel : str, default: "WARNING"
        Logging level of the MAPDL object in the generated script.
    auto_exit : bool, default: True
        Whether to add a line at the end of the script to exit MAPDL.
    line_ending : str, optional
        Line ending of the generated script. When ``None``, ``"\\n"`` is used.
    exec_file : str, optional
        Location of the MAPDL executable to include in the generated
        ``launch_mapdl`` call.
    macros_as_functions : bool, default: True
        Whether to convert MAPDL macros to Python functions.
    use_function_names : bool, default: True
        Whether to convert MAPDL commands to
        :class:`ansys.mapdl.core.Mapdl` methods. When ``True``, the MAPDL
        command ``K`` becomes ``mapdl.k``, otherwise ``mapdl.run("k")``.
    show_log : bool, default: False
        Whether to print the converted commands through a logger.
    add_imports : bool, default: True
        Whether to add the import and ``launch_mapdl`` lines at the beginning
        of the generated script. Overrides *auto_exit*.
    comment_solve : bool, default: False
        Whether to comment out the lines containing ``"SOLVE"`` or ``"/EOF"``.
    cleanup_output : bool, default: True
        Whether to format the output with ``autopep8``, which must be
        installed.
    header : bool or str, default: True
        When ``True``, the default header is written in the first line of the
        output. When a string, it is used as the header.
    print_com : bool, default: True
        Whether to print ``/COM`` arguments to the Python console.
    only_commands : bool, default: False
        Whether to convert only the commands, without header, imports, or exit
        commands. Overrides *header*, *add_imports*, and *auto_exit*.
    graphics_backend : str or GraphicsBackend, optional
        Graphics backend to set on the generated MAPDL object. Accepts a
        :class:`ansys.mapdl.core.plotting.GraphicsBackend` member or its name,
        which is case insensitive. When ``None``, the
        :class:`ansys.mapdl.core.Mapdl` default is used.
    clear_at_start : bool, default: False
        Whether to add a ``mapdl.clear()`` call after the MAPDL object is
        created.
    check_parameter_names : bool, default: False
        Whether the generated MAPDL object checks parameter names, raising an
        exception on leading underscores.

    Returns
    -------
    str
        The converted PyMAPDL code.

    Raises
    ------
    ValueError
        When *graphics_backend* does not name a valid graphics backend.

    Examples
    --------
    Convert a small APDL block:

    >>> from ansys.mapdl.core.cli.convert import convert
    >>> print(convert("/prep7", only_commands=True))
    mapdl.prep7()

    """
    from ansys.mapdl.core.convert import convert_apdl_block

    return convert_apdl_block(
        apdl_strings=apdl_strings,
        loglevel=loglevel,
        auto_exit=auto_exit,
        line_ending=line_ending,
        exec_file=exec_file,
        macros_as_functions=macros_as_functions,
        use_function_names=use_function_names,
        show_log=show_log,
        add_imports=add_imports,
        comment_solve=comment_solve,
        cleanup_output=cleanup_output,
        header=header,
        print_com=print_com,
        only_commands=only_commands,
        graphics_backend=resolve_graphics_backend(graphics_backend),
        clear_at_start=clear_at_start,
        check_parameter_names=check_parameter_names,
    )


def resolve_graphics_backend(
    graphics_backend: Optional[Union[str, GraphicsBackend]],
) -> Optional[GraphicsBackend]:
    """Coerce a graphics backend name to a :class:`GraphicsBackend` member.

    Parameters
    ----------
    graphics_backend : str or GraphicsBackend, optional
        Backend name, which is case insensitive, or an already resolved
        member. When ``None``, no backend is requested.

    Returns
    -------
    GraphicsBackend or None
        The resolved backend, or ``None`` when *graphics_backend* is ``None``.

    Raises
    ------
    ValueError
        When *graphics_backend* does not name a valid graphics backend.

    Examples
    --------
    >>> from ansys.mapdl.core.cli.convert import resolve_graphics_backend
    >>> resolve_graphics_backend("pyvista")
    <GraphicsBackend.PYVISTA: 0>

    """
    if graphics_backend is None:
        return None

    allowed_backends = GraphicsBackend.__members__

    if (
        isinstance(graphics_backend, str)
        and graphics_backend.upper() in allowed_backends
    ):
        return GraphicsBackend[graphics_backend.upper()]

    if graphics_backend in list(allowed_backends.values()):
        return graphics_backend

    allowed_backend_string = ", ".join(
        [str(each) for each in allowed_backends.values()]
    )
    raise ValueError(
        f"Invalid graphics backend '{graphics_backend}'. "
        f"Allowed values are: {allowed_backend_string}."
    )


# ---------------------------------------------------------------------------
# Click wrapper
# ---------------------------------------------------------------------------


@click.command(
    short_help="Convert APDL code to PyMAPDL code.",
    help="""PyMAPDL CLI tool for converting MAPDL scripts to PyMAPDL scripts.

    USAGE:

    This example demonstrates the main use of this tool:

        $ pymapdl convert -f mapdl.dat -o python.py

    If you omit the output argument, the converted code is shown on the screen.

    You can use any option from ``ansys.mapdl.core.convert.convert_apdl_block`` function:

        $ pymapdl convert -f mapdl.dat --auto-exit False
        \"\"\"Script generated by ansys-mapdl-core version 0.69.dev0\"\"\"

        from ansys.mapdl.core import launch_mapdl
        mapdl = launch_mapdl(loglevel="WARNING", print_com=True, check_parameter_names=False)
        mapdl.prep7()

        mapdl.exit()

    You can skip the imports, and the launching and exit calls if the option `--only-code` (`-oc`)
    is given.

        $ pymapdl convert -f mapdl.dat -oc
        mapdl.prep7()

    You can also pipe content from files o command line into the converter.

        $ echo -ne "/prep7" | pymapdl convert -oc
        mapdl.prep7()

        $ echo -ne "/prep7" > my_file.inp
        $ pymapdl convert -oc < my_file.inp
        mapdl.prep7()
""",
)
@click.option(
    "--file",
    "-f",
    help="Name of the APDL input file to convert to PyMAPDL code.",
    type=click.File("r"),
    default=sys.stdin,
)
@click.option(
    "--output",
    "-o",
    default=sys.stdout,
    type=click.File("at"),
    help="Name of the output Python script.",
)
@click.option(
    "--loglevel",
    "-ll",
    default="WARNING",
    type=str,
    help="Logging level of the ansys object within the script.",
)
@click.option(
    "--auto_exit",
    "-ae",
    default=True,
    type=bool,
    help="Adds a line to the end of the script to exit MAPDL. Default ``True``",
)
@click.option(
    "--line_ending",
    "-le",
    type=str,
    default=None,
    help="When None, automatically is ``\n.``",
)
@click.option(
    "--exec_file",
    "-e",
    default=None,
    type=str,
    help="Specify the location of the ANSYS executable and include it in the converter output ``launch_mapdl`` call.",
)
@click.option(
    "--macros_as_functions",
    "-mf",
    default=True,
    type=bool,
    help="Attempt to convert MAPDL macros to python functions.",
)
@click.option(
    "--use_function_names",
    "-fn",
    default=True,
    type=bool,
    help="Convert MAPDL functions to ansys.mapdl.core.Mapdl class methods.  When ``True``, the MAPDL command ``K`` will be converted to ``mapdl.k``.  When ``False``, it will be converted to ``mapdl.run('k')``.",
)
@click.option(
    "--show_log",
    "-sl",
    default=False,
    type=bool,
    help="Print the converted commands using a logger (from ``logging`` Python module).",
)
@click.option(
    "--add_imports",
    "-ai",
    default=True,
    type=bool,
    help='If ``True``, add the lines ``from ansys.mapdl.core import launch_mapdl`` and ``mapdl = launch_mapdl(loglevel="WARNING")`` to the beginning of the output file. This option is useful if you are planning to use the output script from another mapdl session. See examples section. This option overrides ``auto_exit``.',
)
@click.option(
    "--comment_solve",
    "-cs",
    default=False,
    type=bool,
    help='If ``True``, it will pythonically comment the lines that contain ``"SOLVE"`` or ``"/EOF"``.',
)
@click.option(
    "--cleanup_output",
    "-co",
    default=True,
    type=bool,
    help="If ``True`` the output is formatted using ``autopep8`` before writing the file or returning the string. This requires ``autopep8`` to be installed.",
)
@click.option(
    "--header",
    "-h",
    default=True,
    type=bool,
    help="If ``True``, the default header is written in the first line of the output. If a string is provided, this string will be used as header.",
)
@click.option(
    "--print_com",
    "-pc",
    default=True,
    type=bool,
    help="Print command ``/COM`` arguments to python console. Defaults to ``True``.",
)
@click.option(
    "--only_commands",
    "-oc",
    default=False,
    is_flag=True,
    flag_value=True,
    type=bool,
    help="""If ``True``, it converts only the commands, meaning that header
(``header=False``), imports (``add_imports=False``),
and exit commands are NOT included (``auto_exit=False``).
Overrides ``header``, ``add_imports`` and ``auto_exit``.""",
)
@click.option(
    "--graphics_backend",
    default=None,
    type=str,
    help="""It sets the `mapdl.graphics_backend` argument depending on
this value. Defaults to `None` which is Mapdl class default.""",
)
@click.option(
    "--clear_at_start",
    default=False,
    type=bool,
    help="""Add a `mapdl.clear()` after the Mapdl object initialization. Defaults to
`False`.""",
)
@click.option(
    "--check_parameter_names",
    "--cpn",
    default=False,
    type=bool,
    help="""Set MAPDL object to avoid parameter name checks (do not raise leading underscored parameter exceptions). Defaults to `False`.""",
)
def convert_cli(
    file: TextIO,
    output: TextIO,
    loglevel: str,
    auto_exit: bool,
    line_ending: str,
    exec_file: str,
    macros_as_functions: bool,
    use_function_names: bool,
    show_log: bool,
    add_imports: bool,
    comment_solve: bool,
    cleanup_output: bool,
    header: str,
    print_com: bool,
    only_commands: bool,
    graphics_backend: str,
    clear_at_start: bool,
    check_parameter_names: bool,
) -> None:
    """Convert MAPDL code to PyMAPDL"""
    try:
        backend = resolve_graphics_backend(graphics_backend)
    except ValueError as err:
        raise click.BadParameter(str(err), param_hint="'--graphics_backend'") from err

    click.echo(
        convert(
            apdl_strings=file.read(),
            loglevel=loglevel,
            auto_exit=auto_exit,
            line_ending=line_ending,
            exec_file=exec_file,
            macros_as_functions=macros_as_functions,
            use_function_names=use_function_names,
            show_log=show_log,
            add_imports=add_imports,
            comment_solve=comment_solve,
            cleanup_output=cleanup_output,
            header=header,
            print_com=print_com,
            only_commands=only_commands,
            graphics_backend=backend,
            clear_at_start=clear_at_start,
            check_parameter_names=check_parameter_names,
        ),
        file=output,
    )
