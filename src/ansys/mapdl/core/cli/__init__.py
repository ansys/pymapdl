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

try:
    import click

    _HAS_CLICK = True

except ModuleNotFoundError:
    _HAS_CLICK = False


if _HAS_CLICK:
    ###################################
    # PyMAPDL CLI

    @click.group(invoke_without_command=True)
    @click.pass_context
    def main(ctx):
        pass

    from ansys.mapdl.core.cli.convert import convert
    from ansys.mapdl.core.cli.list_instances import list_instances
    from ansys.mapdl.core.cli.start import start
    from ansys.mapdl.core.cli.stop import stop

    main.add_command(convert)
    main.add_command(start)
    main.add_command(stop)
    main.add_command(list_instances, name="list")


else:

    def main():
        print("PyMAPDL CLI requires 'click' Python package to be installed.")


def old_pymapdl_convert_script_entry_point():
    print(
        """This CLI function has been deprecated. Use the following instead:

pymapdl convert input_file.inp -o output_file.out ...

Go to https://mapdl.docs.pyansys.com/version/dev/user_guide/cli.html for more information.
"""
    )
