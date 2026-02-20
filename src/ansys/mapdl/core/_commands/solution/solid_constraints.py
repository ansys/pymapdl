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


class SolidConstraints:

    def da(
        self,
        area: str = "",
        lab: str = "",
        value1: str = "",
        value2: str = "",
        **kwargs,
    ):
        r"""Defines degree-of-freedom constraints on areas.

        Mechanical APDL Command: `DA <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_DA.html>`_

        Parameters
        ----------
        area : str
            Area on which constraints are to be specified. If ALL, apply to all selected areas ( :ref:`asel`
            ). If ``AREA`` = P, graphical picking is enabled and all remaining command fields are ignored
            (valid only in the GUI). A component name may also be substituted for ``AREA``.

        lab : str
            Symmetry label (see :ref:`da_LabFootnotes_1` below) :

            * ``SYMM`` - Generate symmetry constraints. Requires no ``Value1`` or ``Value2``.

            * ``ASYM`` - Generate antisymmetry constraints. Requires no ``Value1`` or ``Value2``.

            Mechanical APDL degree-of-freedom labels:

            * ``UX`` - Displacement in X direction.

            * ``UY`` - Displacement in Y direction.

            * ``UZ`` - Displacement in Z direction.

            * ``ROTX`` - Rotation about X axis.

            * ``ROTY`` - Rotation about Y axis.

            * ``ROTZ`` - Rotation about Z axis.

            * ``HDSP`` - Hydrostatic pressure.

            * ``PRES`` - Pressure.

            * ``TEMP, TBOT, TE2, TE3, ..., TTOP`` - Temperature.

            * ``MAG`` - Magnetic scalar potential (see :ref:`da_LabFootnotes_2` below).

            * ``VOLT`` - Electric scalar potential (see :ref:`da_LabFootnotes_3` below).

            * ``AZ`` - Magnetic vector potential in Z direction (see :ref:`da_LabFootnotes_4` below).

            * ``CONC`` - Concentration.

            * ``ALL`` - Applies all appropriate degree-of-freedom labels except HDSP.

            This command contains some tables and extra information which can be inspected in the original
            documentation pointed above.

        value1 : str
            Value of degree of freedom or table name reference on the area. Valid for all degree-of-freedom
            labels. To specify a table, enclose the table name in % signs (for example, :ref:`da`,
            ``AREA``,TEMP,``tabname``). Use the :ref:`dim` command to define a table.

        value2 : str
            For MAG and VOLT degrees of freedom:

            Value of the imaginary component of the degree of freedom.

        Notes
        -----

        .. _DA_notes:

        You can transfer constraints from areas to nodes via :ref:`dtran` or :ref:`sbctran`. See :ref:`dk`
        for information about generating other constraints on areas.

        Tabular boundary conditions ( ``VALUE`` = ``tabname``) are available only for the following degree-
        of-freedom labels: Electric (VOLT), Structural (UX, UY, UZ, ROTX, ROTY, ROTZ), Acoustic (PRES, UX,
        UY, UZ), and temperature (TEMP, TBOT, TE2, TE3,..., TTOP).

        Constraints specified by the :ref:`da` command can conflict with other specified constraints. See
        Resolution of Conflicting Constraint Specifications \ in the `Basic Analysis Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/Hlp_G_BAS19.html>`_ for details.

        This command is also valid in PREP7.
        """
        command = f"DA,{area},{lab},{value1},{value2}"
        return self.run(command, **kwargs)

    def dadele(self, area: str = "", lab: str = "", **kwargs):
        r"""Deletes degree-of-freedom constraints on an area.

        Mechanical APDL Command: `DADELE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_DADELE.html>`_

        Parameters
        ----------
        area : str
            Area for which constraints are to be deleted. If ALL, delete for all selected areas (
            :ref:`asel` ). If ``AREA`` = P, graphical picking is enabled and all remaining command fields
            are ignored (valid only in the GUI). You can substitute a component name for ``AREA``.

        lab : str
            Valid constraint labels are:

            * ``ALL`` - All constraints.

            * ``SYMM`` - Symmetry constraints.

            * ``ASYM`` - Antisymmetry constraints.

            * ``UX`` - Displacement in X direction.

            * ``UY`` - Displacement in Y direction.

            * ``UZ`` - Displacement in Z direction.

            * ``ROTX`` - Rotation about X axis.

            * ``ROTY`` - Rotation about Y axis.

            * ``ROTZ`` - Rotation about Z axis.

            * ``PRES`` - Pressure.

            * ``TEMP, TBOT, TE2, TE3, ..., TTOP`` - Temperature.

            * ``MAG`` - Magnetic scalar potential.

            * ``VOLT`` - Electric scalar potential.

            * ``AZ`` - Magnetic vector potential in Z direction (see notes).

            * ``CONC`` - Concentration.

        Notes
        -----

        .. _DADELE_notes:

        Deletes the degree of freedom constraints at an area (and all corresponding finite element
        constraints) previously specified with the :ref:`da` command. See the :ref:`ddele` command for
        delete details.

        If the multiple species labels have been changed to user-defined labels via the MSSPEC command, use
        the user-defined labels.

        See the :ref:`da` or the :ref:`da` commands for details on element applicability.

        .. warning::

            On previously meshed areas, **all** constraints on affected nodes will be deleted, whether or
            not they were specified by the :ref:`da` command.

        This command is also valid in PREP7.
        """
        command = f"DADELE,{area},{lab}"
        return self.run(command, **kwargs)

    def dalist(self, area: str = "", **kwargs):
        r"""Lists the DOF constraints on an area.

        Mechanical APDL Command: `DALIST <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_DALIST.html>`_

        Parameters
        ----------
        area : str
            List constraints for this area. If ALL (default), list for all selected areas ( :ref:`asel` ).
            If ``P1`` = P, graphical picking is enabled and all remaining command fields are ignored (valid
            only in the GUI). A component name may also be substituted for ``AREA``.

        Notes
        -----

        .. _DALIST_notes:

        Lists the degree of freedom constraints on an area previously specified with the :ref:`da` command.

        This command is valid in any processor.
        """
        command = f"DALIST,{area}"
        return self.run(command, **kwargs)

    def dk(
        self,
        kpoi: str = "",
        lab: str = "",
        value: str = "",
        value2: str = "",
        kexpnd: int | str = "",
        lab2: str = "",
        lab3: str = "",
        lab4: str = "",
        lab5: str = "",
        lab6: str = "",
        **kwargs,
    ):
        r"""Defines DOF constraints at keypoints.

        Mechanical APDL Command: `DK <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_DK.html>`_

        Parameters
        ----------
        kpoi : str
            Keypoint at which constraint is to be specified. If ALL, apply to all selected keypoints (
            :ref:`ksel` ). If ``KPOI`` = P, graphical picking is enabled and all remaining command fields
            are ignored (valid only in the GUI). A component name may also be substituted for ``KPOI``.

        lab : str
            Additional degree of freedom labels. The same values are applied to the keypoints for these
            labels.

        value : str
            Degree of freedom value or table name reference for tabular boundary conditions. To specify a
            table, enclose the table name in percent signs (%) (for example,
            :ref:`dk`,NODE,TEMP,``tabname``). Use the :ref:`dim` command to define a table.

        value2 : str
            Second degree of freedom value (if any). If the analysis type and the degree of freedom allow a
            complex input, ``VALUE`` (above) is the real component and ``VALUE2`` is the imaginary
            component.

        kexpnd : int or str
            Expansion key:

            * ``0`` - Constraint applies only to the node at this keypoint.

            * ``1`` - Flags this keypoint for constraint expansion.

        lab2 : str
            Additional degree of freedom labels. The same values are applied to the keypoints for these
            labels.

        lab3 : str
            Additional degree of freedom labels. The same values are applied to the keypoints for these
            labels.

        lab4 : str
            Additional degree of freedom labels. The same values are applied to the keypoints for these
            labels.

        lab5 : str
            Additional degree of freedom labels. The same values are applied to the keypoints for these
            labels.

        lab6 : str
            Additional degree of freedom labels. The same values are applied to the keypoints for these
            labels.

        Notes
        -----

        .. _DK_notes:

        A keypoint may be flagged using ``KEXPND`` to allow its constraints to be expanded to nodes on the
        attached solid model entities having similarly flagged keypoint constraints. Constraints are
        transferred from keypoints to nodes with the :ref:`dtran` or :ref:`sbctran` commands. The expansion
        uses interpolation to apply constraints to the nodes on the lines between flagged keypoints. If all
        keypoints of an area or volume region are flagged and the constraints (label and values) are equal,
        the constraints are applied to the interior nodes of the region. See the :ref:`d` command for a
        description of nodal constraints.

        Tabular boundary conditions ( ``VALUE`` = ``tabname``) are available only for the following degree
        of freedom labels: Electric (VOLT), structural (UX, UY, UZ, ROTX, ROTY, ROTZ), Acoustic (PRES, UX,
        UY, UZ), and temperature (TEMP, TBOT, TE2, TE3,..., TTOP).

        Constraints specified by the :ref:`dk` command can conflict with other specified constraints. See
        Resolution of Conflicting Constraint Specifications in the `Basic Analysis Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/Hlp_G_BAS19.html>`_ for details.

        This command is also valid in PREP7.
        """
        command = f"DK,{kpoi},{lab},{value},{value2},{kexpnd},{lab2},{lab3},{lab4},{lab5},{lab6}"
        return self.run(command, **kwargs)

    def dkdele(self, kpoi: str = "", lab: str = "", **kwargs):
        r"""Deletes DOF constraints at a keypoint.

        Mechanical APDL Command: `DKDELE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_DKDELE.html>`_

        Parameters
        ----------
        kpoi : str
            Keypoint for which constraint is to be deleted. If ALL, delete for all selected keypoints (
            :ref:`ksel` ). If ``KPOI`` = P, graphical picking is enabled and all remaining command fields
            are ignored (valid only in the GUI). A component name may also be substituted for ``KPOI``.

        lab : str
            Valid degree of freedom label. If ALL, use all appropriate labels. Structural labels: UX, UY, or
            UZ (displacements); ROTX, ROTY, or ROTZ (rotations); WARP (warping). Thermal labels: TEMP, TBOT,
            TE2, TE3,..., TTOP (temperature). Acoustic labels: PRES (pressure); UX, UY, or UZ (displacements
            for FSI coupled elements). Electric label: VOLT (voltage). Magnetic labels: MAG (scalar magnetic
            potential); AZ (vector magnetic potential). Diffusion label: CONC (concentration).

        Notes
        -----

        .. _DKDELE_notes:

        Deletes the degree of freedom constraints (and all corresponding finite element constraints) at a
        keypoint. See the :ref:`ddele` command for details.

        This command is also valid in PREP7.
        """
        command = f"DKDELE,{kpoi},{lab}"
        return self.run(command, **kwargs)

    def dklist(self, kpoi: str = "", **kwargs):
        r"""Lists the DOF constraints at keypoints.

        Mechanical APDL Command: `DKLIST <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_DKLIST.html>`_

        Parameters
        ----------
        kpoi : str
            List constraints for this keypoint. If ALL (default), list for all selected keypoints (
            :ref:`ksel` ). If ``KPOI`` = P, graphical picking is enabled and all remaining command fields
            are ignored (valid only in the GUI). A component name may also be substituted for ``KPOI``.

        Notes
        -----

        .. _DKLIST_notes:

        Listing applies to the selected keypoints ( :ref:`ksel` ) and the selected degree of freedom labels
        ( :ref:`dofsel` ).

        This command is valid in any processor.
        """
        command = f"DKLIST,{kpoi}"
        return self.run(command, **kwargs)

    def dl(
        self,
        line: str = "",
        area: str = "",
        lab: str = "",
        value1: str = "",
        value2: str = "",
        **kwargs,
    ):
        r"""Defines DOF constraints on lines.

        Mechanical APDL Command: `DL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_DL.html>`_

        Parameters
        ----------
        line : str
            Line at which constraints are to be specified. If ALL, apply to all selected lines ( :ref:`lsel`
            ). If ``LINE`` = P, graphical picking is enabled and all remaining command fields are ignored
            (valid only in the GUI). A component name may also be substituted for ``LINE``.

        area : str
            Area containing line. The normal to the symmetry or antisymmetry surface is assumed to lie on
            this area. Defaults to the lowest numbered selected area containing the line number.

        lab : str
            Symmetry label (see :ref:`DL_LabFootnotes_1` below) :

            * ``SYMM`` - Generate symmetry constraints.

            * ``ASYM`` - Generate antisymmetry constraints.

            Mechanical APDL degree-of-freedom labels:

            * ``UX`` - Displacement in X direction.

            * ``UY`` - Displacement in Y direction.

            * ``UZ`` - Displacement in Z direction.

            * ``ROTX`` - Rotation about X axis.

            * ``ROTY`` - Rotation about Y axis.

            * ``ROTZ`` - Rotation about Z axis.

            * ``HDSP`` - Hydrostatic pressure.

            * ``WARP`` - Warping magnitude.

            * ``TEMP, TBOT, TE2, TE3, ..., TTOP`` - Temperature

            * ``VOLT`` - Electric scalar potential (see :ref:`DL_LabFootnotes_2` ).

            * ``AZ`` - Magnetic vector potential in Z direction.

            * ``CONC`` - Concentration.

            * ``ALL`` - Applies all appropriate DOF labels except HDSP.

            This command contains some tables and extra information which can be inspected in the original
            documentation pointed above.

        value1 : str
            Value of DOF (real part) or table name reference on the line. Valid for all DOF labels. To
            specify a table, enclose the table name in % signs (for example, :ref:`dl`, ``LINE``,
            ``AREA``,TEMP,``tabname``). Use the :ref:`dim` command to define a table.

        value2 : str
            For VOLT DOFs:

            Actual value of the imaginary component of the degree of freedom.

        Notes
        -----

        .. _DL_notes:

        You can transfer constraints from lines to nodes with the :ref:`dtran` or :ref:`sbctran` commands.
        See the :ref:`dk` command for information about generating other constraints at lines.

        Tabular boundary conditions ( ``Value1`` = ``tabname``) are available only for the following degree
        of freedom labels: Electric (VOLT), Structural (UX, UY, UZ, ROTX, ROTY, ROTZ), Acoustic (PRES, UX,
        UY, UZ), and temperature (TEMP, TBOT, TE2, TE3,..., TTOP).

        Constraints specified with this command can conflict with other specified constraints. For more
        information, see Resolution of Conflicting Constraint Specifications.

        This command is also valid in PREP7.
        """
        command = f"DL,{line},{area},{lab},{value1},{value2}"
        return self.run(command, **kwargs)

    def dldele(self, line: str = "", lab: str = "", **kwargs):
        r"""Deletes DOF constraints on a line.

        Mechanical APDL Command: `DLDELE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_DLDELE.html>`_

        Parameters
        ----------
        line : str
            Line for which constraints are to be deleted. If ALL, delete for all selected lines (
            :ref:`lsel` ). If ``LINE`` = P, graphical picking is enabled and all remaining command fields
            are ignored (valid only in the GUI). A component name may also be substituted for ``LINE``

        lab : str
            Constraint label:

            * ``ALL`` - All constraints.

            * ``SYMM`` - Symmetry constraints.

            * ``ASYM`` - Antisymmetry constraints.

            * ``UX`` - Displacement in X direction.

            * ``UY`` - Displacement in Y direction.

            * ``UZ`` - Displacement in Z direction.

            * ``ROTX`` - Rotation about X axis.

            * ``ROTY`` - Rotation about Y axis.

            * ``ROTZ`` - Rotation about Z axis.

            * ``WARP`` - Warping magnitude.

            * ``PRES`` - Pressure.

            * ``TEMP, TBOT, TE2, TE3, ..., TTOP`` - Temperature.

            * ``VOLT`` - Electric scalar potential.

            * ``AZ`` - Magnetic vector potential in Z direction.

            * ``CONC`` - Concentration.

        Notes
        -----

        .. _DLDELE_notes:

        Deletes the degree of freedom constraints (and all corresponding finite element constraints) on a
        line previously specified with the :ref:`dl` command. See the :ref:`ddele` command for delete
        details.

        .. warning::

            On previously meshed lines, all constraints on affected nodes will also be deleted, whether or
            not they were specified by the :ref:`dl` command.

        This command is also valid in PREP7.
        """
        command = f"DLDELE,{line},{lab}"
        return self.run(command, **kwargs)

    def dllist(self, line: str = "", **kwargs):
        r"""Lists DOF constraints on a line.

        Mechanical APDL Command: `DLLIST <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_DLLIST.html>`_

        Parameters
        ----------
        line : str
            List constraints for this line. If ALL (default), list for all selected lines ( :ref:`lsel` ).
            If ``LINE`` = P, graphical picking is enabled and all remaining command fields are ignored
            (valid only in the GUI). A component name may also be substituted for ``LINE``.

        Notes
        -----

        .. _DLLIST_notes:

        Lists the degree of freedom constraints on a line previously specified with the :ref:`dl` command.

        This command is valid in any processor.
        """
        command = f"DLLIST,{line}"
        return self.run(command, **kwargs)

    def dtran(self, **kwargs):
        r"""Transfers solid model DOF constraints to the finite element model.

        Mechanical APDL Command: `DTRAN <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_DTRAN.html>`_

        Notes
        -----

        .. _DTRAN_notes:

        Constraints are transferred only from selected solid model entities to selected nodes. The
        :ref:`dtran` operation is also done if the :ref:`sbctran` command is issued, and is automatically
        done upon initiation of the solution calculations ( :ref:`solve` ).

        This command is also valid in PREP7.
        """
        command = "DTRAN"
        return self.run(command, **kwargs)
