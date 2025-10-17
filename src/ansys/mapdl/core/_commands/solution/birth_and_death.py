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


class BirthAndDeath:

    def ealive(self, elem: str = "", **kwargs):
        r"""Reactivates an element (for the birth and death capability).

        Mechanical APDL Command: `EALIVE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_EALIVE.html>`_

        Parameters
        ----------
        elem : str
            Element to be reactivated. If ALL, reactivate all selected elements ( :ref:`esel` ). If ``ELEM``
            = P, graphical picking is enabled and all remaining command fields are ignored (valid only in
            the GUI). A component name may also be substituted for ``ELEM``. To specify a table, enclose the
            table name in percent signs (%), e.g. :ref:`ealive`,``tabname``.

        Notes
        -----

        .. _EALIVE_notes:

        Reactivates the specified element when the birth and death capability is being used. An element can
        be reactivated only after it has been deactivated ( :ref:`ekill` ).

        Reactivated elements have a zero strain (or thermal heat storage, etc.) state.

        The usage of tabular input is described in in the `Advanced Analysis Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_adv/advoceanloading.html>`_.

        This command is also valid in PREP7.
        """
        command = f"EALIVE,{elem}"
        return self.run(command, **kwargs)

    def ekill(self, elem: str = "", **kwargs):
        r"""Deactivates an element (for the birth and death capability).

        Mechanical APDL Command: `EKILL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_EKILL.html>`_

        Parameters
        ----------
        elem : str
            Element to be deactivated. If ALL, deactivate all selected elements ( :ref:`esel` ). If ``ELEM``
            = P, graphical picking is enabled and all remaining command fields are ignored (valid only in
            the GUI). A component name may also be substituted for ``ELEM``. To specify a table, enclose the
            table name in percent signs (%), e.g. :ref:`ekill`,``tabname``.

        Notes
        -----

        .. _EKILL_notes:

        Deactivates the specified element when the birth and death capability is being used. A deactivated
        element remains in the model but contributes a near-zero stiffness (or conductivity, etc.) value (
        :ref:`estif` ) to the overall matrix. Any solution-dependent state variables (such as stress,
        plastic strain, creep strain, etc.) are set to zero. Deactivated elements contribute nothing to the
        overall mass (or capacitance, etc.) matrix, and do not generate a load vector (pressures,
        convections, gravity, etc.).

        The usage of tabular input is described in in the `Advanced Analysis Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_adv/advoceanloading.html>`_.

        The element can be reactivated with the :ref:`ealive` command.

        This command is also valid in PREP7.
        """
        command = f"EKILL,{elem}"
        return self.run(command, **kwargs)

    def estif(self, kmult: str = "", **kwargs):
        r"""Specifies the matrix multiplier for deactivated elements.

        Mechanical APDL Command: `ESTIF <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ESTIF.html>`_

        **Command default:**

        .. _ESTIF_default:

        Use 1.0E-6 as the multiplier.

        Parameters
        ----------
        kmult : str
            Stiffness matrix multiplier for deactivated elements (defaults to 1.0E-6).

        Notes
        -----

        .. _ESTIF_notes:

        Specifies the stiffness matrix multiplier for elements deactivated with the :ref:`ekill` command
        (birth and death).

        This command is also valid in PREP7.
        """
        command = f"ESTIF,{kmult}"
        return self.run(command, **kwargs)
