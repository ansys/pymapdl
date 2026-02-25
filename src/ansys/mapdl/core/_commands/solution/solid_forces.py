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

from ansys.mapdl.core._commands import CommandsBase


class SolidForces(CommandsBase):

    def fk(
        self, kpoi: str = "", lab: str = "", value: str = "", value2: str = "", **kwargs
    ):
        r"""Defines force loads at keypoints.

        Mechanical APDL Command: `FK <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_FK.html>`_

        Parameters
        ----------
        kpoi : str
            Keypoint at which force is to be specified. If ALL, apply to all selected keypoints (
            :ref:`ksel` ). If ``KPOI`` = P, graphical picking is enabled and all remaining command fields
            are ignored (valid only in the GUI). A component name may also be substituted for ``KPOI``.

        lab : str
            Valid force labels are:

            * **Structural labels** : FX, FY, or FZ (forces); MX, MY, or MZ (moments).
            * **Thermal labels** : HEAT, HBOT, HE2, HE3,..., HTOP (heat flow).
            * **Fluid label** : FLOW (fluid flow).
            * **Electric labels** : AMPS (current flow), CHRG (electric charge).
            * **Magnetic labels** : FLUX (magnetic flux); CSGZ (magnetic current segment).
            * **Diffusion label** : RATE (diffusion flow rate).

        value : str
            Force value or table name reference for specifying tabular boundary conditions. To specify a
            table, enclose the table name in percent signs (%), for example, :ref:`fk`, ``KPOI``,
            HEAT,``tabname``). Use the :ref:`dim` command to define a table.

        value2 : str
            Second force value (if any). If the analysis type and the force allow a complex input, ``VALUE``
            (above) is the real component and ``VALUE2`` is the imaginary component.

        Notes
        -----

        .. _FK_notes:

        Forces may be transferred from keypoints to nodes with the :ref:`ftran` or :ref:`sbctran` commands.
        See the :ref:`f` command for a description of force loads.

        Tabular boundary conditions ( ``VALUE`` = ``tabname``) are available only for the following labels:
        Fluid (FLOW), Electric (AMPS), Structural force (FX, FY, FZ, MX, MY, MZ), and Thermal (HEAT, HBOT,
        HE2, HE3,..., HTOP).

        This command is also valid in PREP7.
        """
        command = f"FK,{kpoi},{lab},{value},{value2}"
        return self.run(command, **kwargs)

    def fkdele(self, kpoi: str = "", lab: str = "", **kwargs):
        r"""Deletes force loads at a keypoint.

        Mechanical APDL Command: `FKDELE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_FKDELE.html>`_

        Parameters
        ----------
        kpoi : str
            Keypoint at which force is to be deleted. If ALL, delete forces at all selected keypoints (
            :ref:`ksel` ). If ``KPOI`` = P, graphical picking is enabled and all remaining command fields
            are ignored (valid only in the GUI). A component name may also be substituted for ``KPOI``.

        lab : str
            Valid force label. If ALL, use all appropriate labels. See the :ref:`fdele` command for labels.

        Notes
        -----

        .. _FKDELE_notes:

        Deletes force loads (and all corresponding finite element loads) at a keypoint. See the :ref:`fdele`
        command for details.

        This command is also valid in PREP7.
        """
        command = f"FKDELE,{kpoi},{lab}"
        return self.run(command, **kwargs)

    def fklist(self, kpoi: str = "", lab: str = "", **kwargs):
        r"""Lists the forces at keypoints.

        Mechanical APDL Command: `FKLIST <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_FKLIST.html>`_

        Parameters
        ----------
        kpoi : str
            List forces at this keypoint. If ALL (default), list for all selected keypoints ( :ref:`ksel` ).
            If ``KPOI`` = P, graphical picking is enabled and all remaining command fields are ignored
            (valid only in the GUI). A component name may also be substituted for ``KPOI``.

        lab : str
            Force label to be listed (defaults to ALL). See the :ref:`dofsel` command for labels.

        Notes
        -----

        .. _FKLIST_notes:

        Listing applies to the selected keypoints ( :ref:`ksel` ) and the selected force labels (
        :ref:`dofsel` ).

        This command is valid in any processor.
        """
        command = f"FKLIST,{kpoi},{lab}"
        return self.run(command, **kwargs)

    def ftran(self, **kwargs):
        r"""Transfers solid model forces to the finite element model.

        Mechanical APDL Command: `FTRAN <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_FTRAN.html>`_

        Notes
        -----

        .. _FTRAN_notes:

        Forces are transferred only from selected keypoints to selected nodes. The :ref:`ftran` operation is
        also done if the :ref:`sbctran` command is issued or automatically done upon initiation of the
        solution calculations ( :ref:`solve` ).

        This command is also valid in PREP7.
        """
        command = "FTRAN"
        return self.run(command, **kwargs)
