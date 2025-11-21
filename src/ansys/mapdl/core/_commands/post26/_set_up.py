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

from ansys.mapdl.core._commands import CommandsBase


class SetUp(CommandsBase):

    def gapf(self, nvar: str = "", num: str = "", name: str = "", **kwargs):
        r"""Defines the gap force data to be stored in a variable.

        Mechanical APDL Command: `GAPF <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_GAPF.html>`_

        Parameters
        ----------
        nvar : str
            Arbitrary reference number assigned to this variable (2 to ``NV`` on :ref:`numvar` ). Overwrites
            any existing results for this variable.

        num : str
            Number identifying gap number for which the gap force is to be stored. Issue the :ref:`gplist`
            command to display gap numbers.

        name : str
            Thirty-two character name for identifying the item on the printout and displays (defaults to the
            name :ref:`gapf` ).

        Notes
        -----

        .. _GAPF_notes:

        Defines the gap force data to be stored in a variable. Applicable only to the expansion pass of the
        mode-superposition linear transient dynamic ( :ref:`antype`,TRANS) analysis. The data is usually on
        :file:`FnameRDSP`.

        .. warning::

            This command is archived in the latest version of the software.
        """
        command = f"GAPF,{nvar},{num},{name}"
        return self.run(command, **kwargs)
