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

try:
    import click  # noqa: F401

    _HAS_CLICK = True
except ImportError:  # pragma: no cover
    _HAS_CLICK = False

if _HAS_CLICK:
    ###################################
    # PyMAPDL CLI

    class _AliasedGroup(click.Group):
        """Click Group that resolves command aliases without showing them in help.

        Aliases are silently mapped to their canonical name so users can type
        either form, but ``pymapdl --help`` only lists the canonical name once.
        """

        _ALIASES: dict[str, str] = {
            "skill": "skills",
        }

        def get_command(self, ctx: click.Context, cmd_name: str):
            return super().get_command(ctx, self._ALIASES.get(cmd_name, cmd_name))

        def resolve_command(self, ctx: click.Context, args: list):
            if args:
                args[0] = self._ALIASES.get(args[0], args[0])
            return super().resolve_command(ctx, args)

    @click.group(cls=_AliasedGroup, invoke_without_command=True)
    @click.pass_context
    def main(ctx: click.Context):
        pass

    from ansys.mapdl.core.cli.check import check as check_cmd
    from ansys.mapdl.core.cli.convert import convert as convert_cmd
    from ansys.mapdl.core.cli.exec import exec_cmd
    from ansys.mapdl.core.cli.list_instances import list_instances
    from ansys.mapdl.core.cli.skills import skills as skills_cmd
    from ansys.mapdl.core.cli.start import start as start_cmd
    from ansys.mapdl.core.cli.stop import stop as stop_cmd

    main.add_command(check_cmd, name="check")
    main.add_command(convert_cmd, name="convert")
    main.add_command(exec_cmd, name="exec")
    main.add_command(list_instances, name="list")
    main.add_command(skills_cmd, name="skills")
    main.add_command(start_cmd, name="start")
    main.add_command(stop_cmd, name="stop")


else:

    def main():
        print("PyMAPDL CLI requires 'click' Python package to be installed.")


def old_pymapdl_convert_script_entry_point():
    print("""This CLI function has been deprecated. Use the following instead:

pymapdl convert input_file.inp -o output_file.out ...

Go to https://mapdl.docs.pyansys.com/version/dev/user_guide/cli.html for more information.
""")
