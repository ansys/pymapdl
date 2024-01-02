class SolidConstraints:
    def da(self, area="", lab="", value1="", value2="", **kwargs):
        """Defines degree-of-freedom constraints on areas.

        APDL Command: DA

        Parameters
        ----------
        area
            Area on which constraints are to be specified.  If ALL, apply to
            all selected areas [ASEL].  A component name may also be substituted for AREA.

        lab
            Symmetry label (see below):

            SYMM - Generate symmetry constraints. Requires no Value1 or Value2.

            ASYM - Generate antisymmetry constraints. Requires no Value1 or Value2.

            ANSYS DOF labels:

            UX - Displacement in X direction.

            UY - Displacement in Y direction.

            UZ - Displacement in Z direction.

            ROTX - Rotation about X axis.

            ROTY - Rotation about Y axis.

            ROTZ - Rotation about Z axis.

            HDSP - Hydrostatic pressure.

            PRES - Pressure.

            TEMP, TBOT, TE2, TE3, . . ., TTOP - Temperature.

            MAG - Magnetic scalar potential (see 2 below).

            VOLT - Electric scalar potential (see 3 below).

            AZ - Magnetic vector potential in Z direction (see 4 below).

            CONC - Concentration.

            ALL - Applies all appropriate DOF labels except HDSP.

        value1
            Value of DOF or table name reference on the area.  Valid for all
            DOF labels.  To specify a table, enclose the table name in % signs
            (e.g., DA,AREA,TEMP,%tabname%).  Use the ``*DIM`` command to define a
            table.

        value2
            For MAG and VOLT DOFs:

        Notes
        -----
        For elements SOLID236 and SOLID237, if Lab = AZ and Value1 = 0, this
        sets the flux-parallel condition for the edge formulation.  (A flux-
        normal condition is the natural boundary condition.)  Do not use the DA
        command to set the edge-flux DOF, AZ to a nonzero value.

        If Lab = MAG and Value1 = 0, this sets the flux-normal condition for
        the magnetic scalar potential formulations (MSP) (A flux-parallel
        condition is the natural boundary condition for MSP.)

        If Lab = VOLT and Value1 = 0, the J-normal condition is set (current
        density (J) flow normal to the area). (A J-parallel condition is the
        natural boundary condition.)

        You can transfer constraints from areas to nodes with the DTRAN or
        SBCTRAN commands.  See the DK command for information about generating
        other constraints on areas.

        Symmetry and antisymmetry constraints are generated as described for
        the DSYM command.

        Tabular boundary conditions (VALUE = %tabname%) are available only for
        the following degree of freedom labels: Electric (VOLT), Structural
        (UX, UY, UZ, ROTX, ROTY, ROTZ), Acoustic (PRES, UX, UY, UZ), and
        temperature (TEMP, TBOT, TE2, TE3, . . ., TTOP).

        Constraints specified by the DA command can conflict with other
        specified constraints.  See Resolution of Conflicting Constraint
        Specifications in the Basic Analysis Guide for details.

        The DA command is also valid in PREP7.

        Examples
        --------
        Select all areas with a z-coordinate of 0, then set value for all
        degrees of freedom to be 0 on the selected areas.

        >>> mapdl.asel('S', 'LOC', 'Z', 0)
        >>> mapdl.da('ALL', 'ALL')

        Apply symmetric boundary conditions on area 2.

        >>> mapdl.da(2, 'SYMM')

        Allow x-displacement on area 2.

        >>> mapdl.da(2, 'UX', 1)
        """
        command = f"DA,{area},{lab},{value1},{value2}"
        return self.run(command, **kwargs)

    def dadele(self, area="", lab="", **kwargs):
        """Deletes degree-of-freedom constraints on an area.

        APDL Command: DADELE

        Parameters
        ----------
        area
            Area for which constraints are to be deleted.  If ALL, delete for
            all selected areas [ASEL].  If AREA = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in
            the GUI).  You can substitute a component name  for AREA.

        lab
            Valid constraint labels are:

            ALL - All constraints.

            SYMM - Symmetry constraints.

            ASYM - Antisymmetry constraints.

            UX - Displacement in X direction.

            UY - Displacement in Y direction.

            UZ - Displacement in Z direction.

            ROTX - Rotation about X axis.

            ROTY - Rotation about Y axis.

            ROTZ - Rotation about Z axis.

            PRES - Pressure.

            TEMP, TBOT, TE2, TE3, . . ., TTOP - Temperature.

            MAG - Magnetic scalar potential.

            VOLT - Electric scalar potential.

            AX - Magnetic vector potential in X direction (see notes).

            AY - Magnetic vector potential in Y direction.

            AZ - Magnetic vector potential in Z direction (see notes).

            CONC - Concentration.

        Notes
        -----
        Deletes the degree of freedom constraints at an area (and all
        corresponding finite element constraints) previously specified with the
        DA command. See the DDELE command for delete details.

        If the multiple species labels have been changed to user-defined labels
        via the MSSPEC command, use the user-defined labels.

        See the DA or the DA commands for details on element applicability.

        Warning:: : On previously meshed areas, all constraints on affected
        nodes will be deleted, whether or not they were specified by the DA
        command.

        This command is also valid in PREP7.
        """
        command = f"DADELE,{area},{lab}"
        return self.run(command, **kwargs)

    def dalist(self, area="", **kwargs):
        """Lists the DOF constraints on an area.

        APDL Command: DALIST

        Parameters
        ----------
        area
            List constraints for this area.  If ALL (default), list for all
            selected areas [ASEL].  If P1 = P, graphical picking is enabled and
            all remaining command fields are ignored (valid only in the GUI).
            A component name may also be substituted for AREA.

        Notes
        -----
        Lists the degree of freedom constraints on an area previously specified
        with the DA command.

        This command is valid in any processor.
        """
        command = f"DALIST,{area}"
        return self.run(command, **kwargs)

    def dk(
        self,
        kpoi="",
        lab="",
        value="",
        value2="",
        kexpnd="",
        lab2="",
        lab3="",
        lab4="",
        lab5="",
        lab6="",
        **kwargs,
    ):
        """Defines DOF constraints at keypoints.

        APDL Command: DK

        Parameters
        ----------
        kpoi
            Keypoint at which constraint is to be specified.  If ALL, apply to
            all selected keypoints [KSEL].  If KPOI = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in
            the GUI).  A component name may also be substituted for KPOI.

        lab
            Valid degree of freedom label.  If ALL, use all appropriate labels
            except HDSP.  Structural labels:  UX, UY, or UZ (displacements);
            ROTX, ROTY, or ROTZ (rotations); WARP (warping); HDSP (hydrostatic
            pressure).  Thermal labels: TEMP, TBOT, TE2, TE3, . . ., TTOP
            (temperature). Acoustic labels:  PRES (pressure); UX, UY, or UZ
            (displacements for FSI coupled elements). Electric labels:  VOLT
            (voltage). Magnetic labels:  MAG (scalar magnetic potential); AX,
            AY, or AZ (vector magnetic potentials). Diffusion labels: CONC
            (concentration).

        value
            Degree of freedom value or table name reference for tabular
            boundary conditions.  To specify a table, enclose the table name in
            percent signs (%) (e.g., DK,NODE,TEMP,%tabname%).  Use the ``*DIM``
            command to define a table.

        value2
            Second degree of freedom value (if any).  If the analysis type and
            the degree of freedom allow a complex input, VALUE (above) is the
            real component and VALUE2 is the imaginary component.

        kexpnd
            Expansion key:

            0 - Constraint applies only to the node at this keypoint.

            1 - Flags this keypoint for constraint expansion.

        lab2, lab3, lab4, . . . ,  lab6
            Additional degree of freedom labels.  The same values are applied
            to the keypoints for these labels.

        Notes
        -----
        A keypoint may be flagged using KEXPND to allow its constraints to be
        expanded to nodes on the attached solid model entities having similarly
        flagged keypoint constraints.  Constraints are transferred from
        keypoints to nodes with the DTRAN or SBCTRAN commands.  The expansion
        uses interpolation to apply constraints to the nodes on the lines
        between flagged keypoints.  If all keypoints of an area or volume
        region are flagged and the constraints (label and values) are equal,
        the constraints are applied to the interior nodes of the region.  See
        the D command for a description of nodal constraints.

        Tabular boundary conditions (VALUE = %tabname%) are available only for
        the following degree of freedom labels: Electric (VOLT), structural
        (UX, UY, UZ, ROTX, ROTY, ROTZ), Acoustic (PRES, UX, UY, UZ), and
        temperature (TEMP, TBOT, TE2, TE3, . . ., TTOP).

        Constraints specified by the DK command can conflict with other
        specified constraints.  See Resolution of Conflicting Constraint
        Specifications in the Basic Analysis Guide for details.

        This command is also valid in PREP7.
        """
        command = f"DK,{kpoi},{lab},{value},{value2},{kexpnd},{lab2},{lab3},{lab4},{lab5},{lab6}"
        return self.run(command, **kwargs)

    def dkdele(self, kpoi="", lab="", **kwargs):
        """Deletes DOF constraints at a keypoint.

        APDL Command: DKDELE

        Parameters
        ----------
        kpoi
            Keypoint for which constraint is to be deleted.  If ALL, delete for
            all selected keypoints [KSEL].  If KPOI = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in
            the GUI).  A component name may also be substituted for KPOI.

        lab
            Valid degree of freedom label.  If ALL, use all appropriate labels.
            Structural labels:  UX, UY, or UZ (displacements); ROTX, ROTY, or
            ROTZ (rotations); WARP (warping).  Thermal labels: TEMP, TBOT, TE2,
            TE3, . . ., TTOP (temperature). Acoustic labels:  PRES (pressure);
            UX, UY, or UZ (displacements for FSI coupled elements). Electric
            label:  VOLT (voltage).  Magnetic labels:  MAG (scalar magnetic
            potential); AX, AY, or AZ (vector magnetic potentials).  Diffusion
            label: CONC (concentration).

        Notes
        -----
        Deletes the degree of freedom constraints (and all corresponding finite
        element constraints) at a keypoint.  See the DDELE command for details.

        This command is also valid in PREP7.
        """
        command = f"DKDELE,{kpoi},{lab}"
        return self.run(command, **kwargs)

    def dklist(self, kpoi="", **kwargs):
        """Lists the DOF constraints at keypoints.

        APDL Command: DKLIST

        Parameters
        ----------
        kpoi
            List constraints for this keypoint.  If ALL (default), list for all
            selected keypoints [KSEL].  If KPOI = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in
            the GUI).  A component name may also be substituted for KPOI.

        Notes
        -----
        Listing applies to the selected keypoints [KSEL] and the selected
        degree of freedom labels [DOFSEL].

        This command is valid in any processor.
        """
        command = f"DKLIST,{kpoi}"
        return self.run(command, **kwargs)

    def dl(self, line="", area="", lab="", value1="", value2="", **kwargs):
        """Defines DOF constraints on lines.

        APDL Command: DL

        Parameters
        ----------
        line
            Line at which constraints are to be specified. If ALL, apply to all
            selected lines [LSEL]. If LINE = P, graphical picking is enabled
            and all remaining command fields are ignored (valid only in the
            GUI). A component name may also be substituted for LINE.

        area
            Area containing line. The normal to the symmetry or antisymmetry
            surface is assumed to lie on this area. Defaults to the lowest
            numbered selected area containing the line number.

        lab
            Symmetry label (see 2):

            SYMM - Generate symmetry constraints.

            ASYM - Generate antisymmetry constraints.

        value1
            Value of DOF (real part) or table name reference on the line.
            Valid for all DOF labels.  To specify a table, enclose the table
            name in % signs (e.g., DL,LINE,AREA,TEMP,%tabname%).  Use the ``*DIM``
            command to define a table.

        value2
            For VOLT DOFs:

        Notes
        -----
        You can transfer constraints from lines  to nodes with the  DTRAN or
        SBCTRAN commands.  See the DK command for information about generating
        other constraints at lines.

        Symmetry and antisymmetry constraints are generated as described on the
        DSYM command.

        Setting Lab = VOLT and Value1 = 0 applies the J-normal boundary
        condition (current density vector (J) flows normal to the line).  No
        input is required for the J-parallel condition because it is the
        natural boundary condition.

        Tabular boundary conditions (Value1 = %tabname%) are available only for
        the following degree of freedom labels: Electric (VOLT), Structural
        (UX, UY, UZ, ROTX, ROTY, ROTZ), Acoustic (PRES, UX, UY, UZ), and
        temperature (TEMP, TBOT, TE2, TE3, . . ., TTOP).

        Constraints specified by the DL command can conflict with other
        specified constraints.  See Resolution of Conflicting Constraint
        Specifications in the Basic Analysis Guide for details.

        This command is also valid in PREP7.
        """
        command = f"DL,{line},{area},{lab},{value1},{value2}"
        return self.run(command, **kwargs)

    def dldele(self, line="", lab="", **kwargs):
        """Deletes DOF constraints on a line.

        APDL Command: DLDELE

        Parameters
        ----------
        line
            Line for which constraints are to be deleted.  If ALL, delete for
            all selected lines [LSEL].  If LINE = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in
            the GUI).  A component name may also be substituted for LINE

        lab
            Constraint label:

            ALL - All constraints.

            SYMM - Symmetry constraints.

            ASYM - Antisymmetry constraints.

            UX - Displacement in X direction.

            UY - Displacement in Y direction.

            UZ - Displacement in Z direction.

            ROTX - Rotation about X axis.

            ROTY - Rotation about Y axis.

            ROTZ - Rotation about Z axis.

            WARP - Warping magnitude.

            PRES - Pressure.

            TEMP, TBOT, TE2, TE3, . . ., TTOP - Temperature.

            VOLT - Electric scalar potential.

            AX - Magnetic vector potential in X direction.

            AY - Magnetic vector potential in Y direction.

            AZ - Magnetic vector potential in Z direction.

            CONC - Concentration.

        Notes
        -----
        Deletes the degree of freedom constraints (and all corresponding finite
        element constraints) on a line previously specified with the DL
        command.  See the DDELE command for delete details.

        Warning:: : On previously meshed lines, all constraints on affected
        nodes will also be deleted, whether or not they were specified by the
        DL command.

        This command is also valid in PREP7.
        """
        command = f"DLDELE,{line},{lab}"
        return self.run(command, **kwargs)

    def dllist(self, line="", **kwargs):
        """Lists DOF constraints on a line.

        APDL Command: DLLIST

        Parameters
        ----------
        line
            List constraints for this line.  If ALL (default), list for all
            selected lines [LSEL].  If LINE = P, graphical picking is enabled
            and all remaining command fields are ignored (valid only in the
            GUI).  A component name may also be substituted for LINE.

        Notes
        -----
        Lists the degree of freedom constraints on a line previously specified
        with the DL command.

        This command is valid in any processor.
        """
        command = f"DLLIST,{line}"
        return self.run(command, **kwargs)

    def dtran(self, **kwargs):
        """Transfers solid model DOF constraints to the finite element model.

        APDL Command: DTRAN

        Notes
        -----
        Constraints are transferred only from selected solid model entities to
        selected nodes.  The DTRAN operation is also done if the SBCTRAN
        command is issued, and is automatically done upon initiation of the
        solution calculations [SOLVE].

        This command is also valid in PREP7.
        """
        command = f"DTRAN,"
        return self.run(command, **kwargs)
