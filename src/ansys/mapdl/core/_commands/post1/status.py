# Copyright (C) 2016 - 2025 ANSYS, Inc. and/or its affiliates.
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


class Status:

    def calc(self, **kwargs):
        r"""Specifies "Calculation settings" as the subsequent status topic.

        Mechanical APDL Command: `CALC <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CALC.html>`_

        Notes
        -----

        .. _CALC_notes:

        This is a status ( :ref:`stat` ) topic command. Status topic commands are generated by the GUI and
        will appear in the log file ( :file:`Jobname.LOG` ) if status is requested for some items under
        Utility Menu> List> Status. This command will be immediately followed by a :ref:`stat` command,
        which will report the status for the specified topic.

        If entered directly into the program, the :ref:`stat` command should immediately follow this
        command.
        """
        command = "CALC"
        return self.run(command, **kwargs)

    def datadef(self, **kwargs):
        r"""Specifies "Directly defined data status" as the subsequent status topic.

        Mechanical APDL Command: `DATADEF <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_DATADEF.html>`_

        Notes
        -----

        .. _DATADEF_notes:

        This is a status ( :ref:`stat` ) topic command. Status topic commands are generated by the GUI and
        will appear in the log file ( :file:`Jobname.LOG` ) if status is requested for some items under
        Utility Menu> List> Status. This command will be immediately followed by a :ref:`stat` command,
        which will report the status for the specified topic.

        If entered directly into the program, the :ref:`stat` command should immediately follow this
        command.
        """
        command = "DATADEF"
        return self.run(command, **kwargs)

    def define(self, **kwargs):
        r"""Specifies "Data definition settings" as the subsequent status topic.

        Mechanical APDL Command: `DEFINE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_DEFINE.html>`_

        Notes
        -----

        .. _DEFINE_notes:

        This is a status ( :ref:`stat` ) topic command. Status topic commands are generated by the GUI and
        will appear in the log file ( :file:`Jobname.LOG` ) if status is requested for some items under
        Utility Menu> List> Status. This command will be immediately followed by a :ref:`stat` command,
        which will report the status for the specified topic.

        If entered directly into the program, the :ref:`stat` command should immediately follow this
        command.
        """
        command = "DEFINE"
        return self.run(command, **kwargs)

    def display(self, **kwargs):
        r"""Specifies "Display settings" as the subsequent status topic.

        Mechanical APDL Command: `DISPLAY <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_DISPLAY.html>`_

        Notes
        -----

        .. _DISPLAY_notes:

        This is a status ( :ref:`stat` ) topic command. Status topic commands are generated by the GUI and
        will appear in the log file ( :file:`Jobname.LOG` ) if status is requested for some items under
        Utility Menu> List> Status. This command will be immediately followed by a :ref:`stat` command,
        which will report the status for the specified topic.

        If entered directly into the program, the :ref:`stat` command should immediately follow this
        command.
        """
        command = "DISPLAY"
        return self.run(command, **kwargs)

    def lccalc(self, **kwargs):
        r"""Specifies "Load case settings" as the subsequent status topic.

        Mechanical APDL Command: `LCCALC <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_LCCALC.html>`_

        Notes
        -----

        .. _LCCALC_notes:

        This is a status ( :ref:`stat` ) topic command. Status topic commands are generated by the GUI and
        will appear in the log file ( :file:`Jobname.LOG` ) if status is requested for some items under
        Utility Menu> List> Status. This command will be immediately followed by a :ref:`stat` command,
        which will report the status for the specified topic.

        If entered directly into the program, the :ref:`stat` command should immediately follow this
        command.

        This command is also valid for `rezoning
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_nlad/Hlp_G_ADVRZSMP.html>`_.
        """
        command = "LCCALC"
        return self.run(command, **kwargs)

    def point(self, **kwargs):
        r"""Specifies "Point flow tracing settings" as the subsequent status topic.

        Mechanical APDL Command: `POINT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_POINT.html>`_

        Notes
        -----

        .. _POINT_notes:

        This is a status ( :ref:`stat` ) topic command. Status topic commands are generated by the GUI and
        will appear in the log file ( :file:`Jobname.LOG` ) if status is requested for some items under
        Utility Menu> List> Status. This command will be immediately followed by a :ref:`stat` command,
        which will report the status for the specified topic.

        If entered directly into the program, the :ref:`stat` command should immediately follow this
        command.
        """
        command = "POINT"
        return self.run(command, **kwargs)

    def print(self, **kwargs):
        r"""Specifies "Print settings" as the subsequent status topic.

        Mechanical APDL Command: `PRINT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PRINT.html>`_

        Notes
        -----

        .. _PRINT_notes:

        This is a status ( :ref:`stat` ) topic command. Status topic commands are generated by the GUI and
        will appear in the log file ( :file:`Jobname.LOG` ) if status is requested for some items under
        Utility Menu> List> Status. This command will be immediately followed by a :ref:`stat` command,
        which will report the status for the specified topic.

        If entered directly into the program, the :ref:`stat` command should immediately follow this
        command.
        """
        command = "PRINT"
        return self.run(command, **kwargs)

    def sort(self, **kwargs):
        r"""Specifies "Sort settings" as the subsequent status topic.

        Mechanical APDL Command: `SORT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SORT.html>`_

        Notes
        -----

        .. _SORT_notes:

        This is a status ( :ref:`stat` ) topic command. Status topic commands are generated by the GUI and
        will appear in the log file ( :file:`Jobname.LOG` ) if status is requested for some items under
        Utility Menu> List> Status. This command will be immediately followed by a :ref:`stat` command,
        which will report the status for the specified topic.

        If entered directly into the program, the :ref:`stat` command should immediately follow this
        command.
        """
        command = "SORT"
        return self.run(command, **kwargs)

    def spec(self, **kwargs):
        r"""Specifies "Miscellaneous specifications" as the subsequent status topic.

        Mechanical APDL Command: `SPEC <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SPEC.html>`_

        Notes
        -----

        .. _SPEC_notes:

        This is a status ( :ref:`stat` ) topic command. Status topic commands are generated by the GUI and
        will appear in the log file ( :file:`Jobname.LOG` ) if status is requested for some items under
        Utility Menu> List> Status. This command will be immediately followed by a :ref:`stat` command,
        which will report the status for the specified topic.

        If entered directly into the program, the :ref:`stat` command should immediately follow this
        command.
        """
        command = "SPEC"
        return self.run(command, **kwargs)
