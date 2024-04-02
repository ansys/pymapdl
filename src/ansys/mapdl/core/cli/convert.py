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

import click


@click.command(
    short_help="Convert APDL code to PyMAPDL code.",
    help="""PyMAPDL CLI tool for converting MAPDL scripts to PyMAPDL scripts.

    USAGE:

    This example demonstrates the main use of this tool:

        $ pymapdl convert mapdl.dat -o python.py

        File mapdl.dat successfully converted to python.py.

    The output argument is optional, in which case the "py" extension is used:

        $ pymapdl convert mapdl.dat

        File mapdl.dat successfully converted to mapdl.py.

    You can use any option from ``ansys.mapdl.core.convert.convert_script`` function:

        $ pymapdl convert mapdl.dat --auto-exit False

        File mapdl.dat successfully converted to mapdl.py.

        $ pymapdl convert mapdl.dat --filename_out mapdl.out --add_imports False

        File mapdl.dat successfully converted to mapdl.out.""",
)
@click.argument("filename_in")
@click.option("-o", default=None, help="Name of the output Python script.")
@click.option("--filename_out", default=None, help="Name of the output Python script.")
@click.option(
    "--loglevel",
    default="WARNING",
    help="Logging level of the ansys object within the script.",
)
@click.option(
    "--auto_exit",
    default=True,
    help="Adds a line to the end of the script to exit MAPDL. Default ``True``",
)
@click.option("--line_ending", default=None, help="When None, automatically is ``\n.``")
@click.option(
    "--exec_file",
    default=None,
    help="Specify the location of the ANSYS executable and include it in the converter output ``launch_mapdl`` call.",
)
@click.option(
    "--macros_as_functions",
    default=True,
    help="Attempt to convert MAPDL macros to python functions.",
)
@click.option(
    "--use_function_names",
    default=True,
    help="Convert MAPDL functions to ansys.mapdl.core.Mapdl class methods.  When ``True``, the MAPDL command ``K`` will be converted to ``mapdl.k``.  When ``False``, it will be converted to ``mapdl.run('k')``.",
)
@click.option(
    "--show_log",
    default=False,
    help="Print the converted commands using a logger (from ``logging`` Python module).",
)
@click.option(
    "--add_imports",
    default=True,
    help='If ``True``, add the lines ``from ansys.mapdl.core import launch_mapdl`` and ``mapdl = launch_mapdl(loglevel="WARNING")`` to the beginning of the output file. This option is useful if you are planning to use the output script from another mapdl session. See examples section. This option overrides ``auto_exit``.',
)
@click.option(
    "--comment_solve",
    default=False,
    help='If ``True``, it will pythonically comment the lines that contain ``"SOLVE"`` or ``"/EOF"``.',
)
@click.option(
    "--cleanup_output",
    default=True,
    help="If ``True`` the output is formatted using ``autopep8`` before writing the file or returning the string. This requires ``autopep8`` to be installed.",
)
@click.option(
    "--header",
    default=True,
    help="If ``True``, the default header is written in the first line of the output. If a string is provided, this string will be used as header.",
)
@click.option(
    "--print_com",
    default=True,
    help="Print command ``/COM`` arguments to python console. Defaults to ``True``.",
)
def convert(
    filename_in: str,
    o: str,
    filename_out: str,
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
):
    """Convert MAPDL code to PyMAPDL"""
    from ansys.mapdl.core.convert import convert_script

    if o:
        filename_out = o

    convert_script(
        filename_in,
        filename_out,
        loglevel,
        auto_exit,
        line_ending,
        exec_file,
        macros_as_functions,
        use_function_names,
        show_log,
        add_imports,
        comment_solve,
        cleanup_output,
        header,
        print_com,
    )

    if filename_out:
        click.echo(
            click.style("Success: ", fg="green")
            + f"File {filename_in} successfully converted to {filename_out}."
        )
    else:
        click.echo(
            click.style("Success: ", fg="green")
            + f"File {filename_in} successfully converted to {os.path.splitext(filename_in)[0] + '.py'}."
        )
