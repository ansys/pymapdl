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


class FailureCriteria:

    def fctyp(self, oper: str = "", lab: str = "", **kwargs):
        r"""Activates or removes failure-criteria types for postprocessing.

        Mechanical APDL Command: `FCTYP <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_FCTYP.html>`_

        Parameters
        ----------
        oper : str
            Operation key:

            * ``ADD`` - Activate failure-criteria types. This option is the default behavior.

            * ``DELE`` - Remove failure-criteria types.

        lab : str
            Valid failure-criteria labels. If ALL, select all available (including user-defined) failure
            criteria.

            * ``EMAX`` - Maximum strain criterion (default)

            * ``SMAX`` - Maximum stress criterion (default)

            * ``TWSI`` - Tsai-Wu strength index (default)

            * ``TWSR`` - Inverse of Tsai-Wu strength ratio index (default)

            * ``HFIB`` - Hashin fiber failure criterion

            * ``HMAT`` - Hashin matrix failure criterion

            * ``PFIB`` - Puck fiber failure criterion

            * ``PMAT`` - Puck inter-fiber (matrix) failure criterion

            * ``L3FB`` - LaRc03 fiber failure criterion

            * ``L3MT`` - LaRc03 matrix failure criterion

            * ``L4FB`` - LaRc04 fiber failure criterion

            * ``L4MT`` - LaRc04 matrix failure criterion

            * ``USR1 through USR9`` - User-defined failure criteria

        Notes
        -----

        .. _FCTYP_notes:

        The :ref:`fctyp` command modifies the list of active failure criteria.

        By default, active failure criteria include EMAX, SMAX, TWSI, and TWSR.

        The command affects any subsequent postprocessing listing and plotting commands (such as
        :ref:`presol`, :ref:`prnsol`, :ref:`plesol`, :ref:`plnsol`, and :ref:`etable` ).

        A single :ref:`fctyp` command allows up to six failure-criteria labels. If needed, reissue the
        command to activate or remove additional failure-criteria types.
        """
        command = f"FCTYP,{oper},{lab}"
        return self.run(command, **kwargs)
