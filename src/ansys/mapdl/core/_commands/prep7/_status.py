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

    def fatigue(self, **kwargs):
        r"""Specifies "Fatigue data status" as the subsequent status topic.

        Mechanical APDL Command: `FATIGUE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_FATIGUE.html>`_

        Notes
        -----

        .. _FATIGUE_notes:

        This is a status ( :ref:`stat` ) topic command that appears in the log file ( :file:`Jobname.LOG` )
        if status is requested for some items. This command is followed immediately by a :ref:`stat`
        command, which reports the status for the specified topic.

        If entered directly into the program, the :ref:`stat` command should immediately follow this
        command.

        .. warning::

            This command is archived in the latest version of the software.

        """
        command = "FATIGUE"
        return self.run(command, **kwargs)
