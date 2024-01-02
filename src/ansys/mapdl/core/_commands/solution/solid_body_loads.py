class SolidBodyLoads:
    def bfa(self, area="", lab="", val1="", val2="", val3="", val4="", **kwargs):
        """Defines a body force load on an area.

        APDL Command: BFA

        Parameters
        ----------
        area
            Area to which body load applies.  If ALL, apply to all selected
            areas [ASEL]. A component name may also be substituted for Area.

        lab
            Valid body load label. Load labels are listed under "Body Loads" in
            the input table for each element type in the Element Reference.

        val1, val2, val3
            Value associated with the Lab item or a table name for specifying
            tabular boundary conditions. Use only VAL1 for TEMP, FLUE, HGEN,
            CHRGD. For Lab = JS in magnetics, use VAL1, VAL2, and VAL3 for the
            X, Y, and Z components. For acoustics, if Lab = JS, use VAL1 for
            mass source in a harmonic analysis or mass source rate in a
            transient analysis, and ignore VAL2 and VAL3. For Lab = VLTG, VAL1
            is the voltage drop and VAL2 is the phase angle. If Lab = IMPD,
            VAL1 is the resistance and VAL2 is the reactance in ohms/square.
            When specifying a table name, you must enclose the table name in
            percent signs (%), e.g., BFA,Area,Lab,%tabname%. Use the ``*DIM``
            command to define a table.

        val4
            If Lab = JS, VAL4 is the phase angle in degrees.

        Notes
        -----
        Defines a body force load (such as temperature in a structural
        analysis, heat generation rate in a thermal analysis, etc.) on an area.
        Body loads may be transferred from areas to area elements (or to nodes
        if area elements do not exist) with the BFTRAN or SBCTRAN commands.
        Body loads default to the value specified on the BFUNIF command, if it
        was previously specified.

        You can specify a table name only when using temperature (TEMP) and
        heat generation rate (HGEN) body load labels.

        Body loads specified by the BFA command can conflict with other
        specified body loads.  See Resolution of Conflicting Body Load
        Specifications in the Basic Analysis Guide for details.

        Graphical picking is available only via the listed menu paths.

        This command is also valid in PREP7.
        """
        command = f"BFA,{area},{lab},{val1},{val2},{val3},{val4}"
        return self.run(command, **kwargs)

    def bfadele(self, area="", lab="", **kwargs):
        """Deletes body force loads on an area.

        APDL Command: BFADELE

        Parameters
        ----------
        area
            Area at which body load is to be deleted.  If ALL, delete for all
            selected areas [ASEL]. A component name may also be substituted for
            AREA.

        lab
            Valid body load label. If ALL, use all appropriate labels. Load
            labels are listed under "Body Loads" in the input table for each
            element type in the Element Reference. See the BFA command for
            labels.

        Notes
        -----
        Deletes body force loads (and all corresponding finite element loads)
        for a specified area and label.  Body loads may be defined on an area
        with the BFA command.

        Graphical picking is available only via the listed menu paths.

        This command is also valid in PREP7.
        """
        command = f"BFADELE,{area},{lab}"
        return self.run(command, **kwargs)

    def bfalist(self, area="", lab="", **kwargs):
        """Lists the body force loads on an area.

        APDL Command: BFALIST

        Parameters
        ----------
        area
            Area at which body load is to be listed.  If ALL (or blank), list
            for all selected areas [ASEL].  If AREA = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in
            the GUI).  A component name may also be substituted for AREA.

        lab
            Valid body load label. If ALL, use all appropriate labels. Load
            labels are listed under "Body Loads" in the input table for each
            element type in the Element Reference. See the BFA command for
            labels.

        Notes
        -----
        Lists the body force loads for the specified area and label.  Body
        loads may be defined on an area with the BFA command.

        This command is valid in any processor.
        """
        command = f"BFALIST,{area},{lab}"
        return self.run(command, **kwargs)

    def bfk(self, kpoi="", lab="", val1="", val2="", val3="", phase="", **kwargs):
        """Defines a body force load at a keypoint.

        APDL Command: BFK

        Parameters
        ----------
        kpoi
            Keypoint to which body load applies.  If ALL, apply to all selected
            keypoints [KSEL].  A component name may also be substituted for
            Kpoi.

        lab
            Valid body load label. Load labels are listed under "Body Loads" in
            the input table for each element type in the Element Reference.

        val1, val2, val3
            Value associated with the Lab item or a table name for specifying
            tabular boundary conditions.  Use only VAL1 for TEMP, FLUE, HGEN,
            MVDI and CHRGD.  For magnetics, use VAL1, VAL2, and VAL3 for the X,
            Y, and Z components of JS . For acoustics, if Lab = JS,  use VAL1
            for mass source in a harmonic analysis or mass source rate in a
            transient analysis, and ignoreVAL2 and VAL3. When specifying a
            table name, you must enclose the table name in percent signs (%),
            e.g., BFK,Kpoi,Lab,%tabname%.  Use the ``*DIM`` command to define a
            table.

        phase
            Phase angle in degrees associated with the JS label.

        Notes
        -----
        Defines a body force load (such as temperature in a structural
        analysis, heat generation rate in a thermal analysis, etc.) at a
        keypoint.  Body loads may be transferred from keypoints to nodes with
        the BFTRAN or SBCTRAN commands.  Interpolation will be used to apply
        loads to the nodes on the lines between keypoints.  All keypoints on a
        given area (or volume) must have the same BFK specification, with the
        same values, for the loads to be transferred to interior nodes in the
        area (or volume).  If only one keypoint on a line has a BFK
        specification, the other keypoint defaults to the value specified on
        the BFUNIF command.

        You can specify a table name only when using temperature (TEMP) and
        heat generation rate (HGEN) body load labels.

        Body loads specified by the BFK command can conflict with other
        specified body loads.  See Resolution of Conflicting Body Load
        Specifications in the Basic Analysis Guide for details.

        Graphical picking is available only via the listed menu paths.

        This command is also valid in PREP7.
        """
        command = f"BFK,{kpoi},{lab},{val1},{val2},{val3},{phase}"
        return self.run(command, **kwargs)

    def bfkdele(self, kpoi="", lab="", **kwargs):
        """Deletes body force loads at a keypoint.

        APDL Command: BFKDELE

        Parameters
        ----------
        kpoi
            Keypoint at which body load is to be deleted.  If ALL, delete for
            all selected keypoints [KSEL]. A component name may also be
            substituted for KPOI.

        lab
            Valid body load label. If ALL, use all appropriate labels. Load
            labels are listed under "Body Loads" in the input table for each
            element type in the Element Reference. See the BFK command for
            labels.

        Notes
        -----
        Deletes body force loads (and all corresponding finite element loads)
        for a specified keypoint and label.  Body loads may be defined at a
        keypoint with the BFK command.

        Graphical picking is available only via the listed menu paths.

        This command is also valid in PREP7.
        """
        command = f"BFKDELE,{kpoi},{lab}"
        return self.run(command, **kwargs)

    def bfklist(self, kpoi="", lab="", **kwargs):
        """Lists the body force loads at keypoints.

        APDL Command: BFKLIST

        Parameters
        ----------
        kpoi
            Keypoint at which body load is to be listed.  If ALL (or blank),
            list for all selected keypoints [KSEL].  If KPOI = P, graphical
            picking is enabled and all remaining command fields are ignored
            (valid only in the GUI).  A component name may also be substituted
            for KPOI

        lab
            Valid body load label. If ALL, use all appropriate labels. Load
            labels are listed under "Body Loads" in the input table for each
            element type in the Element Reference. See the BFK command for
            labels.

        Notes
        -----
        Lists the body force loads for the specified keypoint and label.
        Keypoint body loads may be defined with the BFK command.

        This command is valid in any processor.
        """
        command = f"BFKLIST,{kpoi},{lab}"
        return self.run(command, **kwargs)

    def bfl(self, line="", lab="", val1="", val2="", val3="", val4="", **kwargs):
        """Defines a body force load on a line.

        APDL Command: BFL

        Parameters
        ----------
        line
            Line to which body load applies.  If ALL, apply to all selected
            lines [LSEL]. A component name may also be substituted for Line.

        lab
            Valid body load label. Load labels are listed under "Body loads" in
            the input table for each element type in the Element Reference.

        val1, val2, val3
            Value associated with the Lab item or a table name for specifying
            tabular boundary conditions.  Use only VAL1 for TEMP, FLUE, HGEN,
            and CHRGD. For acoustics, if Lab = JS,  use VAL1 for mass source in
            a harmonic analysis or mass source rate in a transient analysis,
            and ignoreVAL2 and VAL3. When specifying a table name, you must
            enclose the table name in percent signs (%), e.g.,
            BFL,Line,Lab,%tabname%.  Use the ``*DIM`` command to define a table.

        val4
            If Lab = JS, VAL4 is the phase angle in degrees.

        Notes
        -----
        Defines a body force load (such as temperature in a structural
        analysis, heat generation rate in a thermal analysis, etc.) on a line.
        Body loads may be transferred from lines to line elements (or to nodes
        if line elements do not exist) with the BFTRAN or SBCTRAN commands.

        You can specify a table name only when using temperature (TEMP) and
        heat generation rate (HGEN) body load labels.

        Body loads specified by the BFL command can conflict with other
        specified body loads.  See Resolution of Conflicting Body Load
        Specifications in the Basic Analysis Guide for details.

        Graphical picking is available only via the listed menu paths.

        This command is also valid in PREP7.
        """
        command = f"BFL,{line},{lab},{val1},{val2},{val3},{val4}"
        return self.run(command, **kwargs)

    def bfldele(self, line="", lab="", **kwargs):
        """Deletes body force loads on a line.

        APDL Command: BFLDELE

        Parameters
        ----------
        line
            Line at which body load is to be deleted.  If ALL, delete for all
            selected lines [LSEL].  A component name may also be substituted
            for LINE.

        lab
            Valid body load label. If ALL, use all appropriate labels. Load
            labels are listed under "Body Loads" in the input table for each
            element type in the Element Reference. See the BFL command for
            labels.

        Notes
        -----
        Deletes body force loads (and all corresponding finite element loads)
        for a specified line and label.  Body loads may be defined on a line
        with the BFL command.

        Graphical picking is available only via the listed menu paths.

        This command is also valid in PREP7.
        """
        command = f"BFLDELE,{line},{lab}"
        return self.run(command, **kwargs)

    def bfllist(self, line="", lab="", **kwargs):
        """Lists the body force loads on a line.

        APDL Command: BFLLIST

        Parameters
        ----------
        line
            Line at which body load is to be listed.  If ALL (or blank), list
            for all selected lines [LSEL].  If LINE = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in
            the GUI).  A component name may also be substituted for LINE.

        lab
            Valid body load label. If ALL, use all appropriate labels. Load
            labels are listed under "Body Loads" in the input table for each
            element type in the Element Reference. See the BFL command for
            labels.

        Notes
        -----
        Lists the body force loads for the specified line and label.  Body
        loads may be defined on a line with the BFL command.

        This command is valid in any processor.
        """
        command = f"BFLLIST,{line},{lab}"
        return self.run(command, **kwargs)

    def bftran(self, **kwargs):
        """Transfers solid model body force loads to the finite element model.

        APDL Command: BFTRAN

        Notes
        -----
        Body loads are transferred from selected keypoints and lines to
        selected nodes and from selected areas and volumes to selected
        elements.  The BFTRAN operation is also done if the SBCTRAN command is
        either explicitly issued or automatically issued upon initiation of the
        solution calculations [SOLVE].

        This command is also valid in PREP7.
        """
        command = f"BFTRAN,"
        return self.run(command, **kwargs)

    def bfv(self, volu="", lab="", val1="", val2="", val3="", phase="", **kwargs):
        """Defines a body force load on a volume.

        APDL Command: BFV

        Parameters
        ----------
        volu
            Volume to which body load applies.  If ALL, apply to all selected
            volumes [VSEL]. A component name may also be substituted for Volu.

        lab
            Valid body load label. Load labels are listed under "Body Loads" in
            the input table for each element type in the Element Reference.

        val1, val2, val3
            Value associated with the Lab item or a table name for specifying
            tabular boundary conditions.  Use only VAL1 for TEMP, FLUE, HGEN,
            and CHRGD.  Use VAL1, VAL2, and VAL3 for the X, Y, and Z components
            of JS.  For Lab = JS in magnetics, use VAL1, VAL2, and VAL3 for the
            X, Y, and Z components. For acoustics, if Lab = JS,  use VAL1 for
            mass source in a harmonic analysis or mass source rate in a
            transient analysis, and ignoreVAL2 and VAL3. For Lab = VLTG, VAL1
            is the voltage drop and VAL2 is the phase angle.  When specifying a
            table name, you must enclose the table name in percent signs (%),
            e.g., BFV,Volu,Lab,%tabname%.  Use the ``*DIM`` command to define a
            table.

        phase
            Phase angle in degrees associated with the JS label.

        Notes
        -----
        Defines a body force load (such as temperature in a structural
        analysis, heat generation rate in a thermal analysis, etc.) on a
        volume.  Body loads may be transferred from volumes to volume elements
        (or to nodes if volume elements do not exist) with the BFTRAN or
        SBCTRAN commands.  Body loads default to the value specified on the
        BFUNIF command, if it was previously specified.

        You can specify a table name only when using temperature (TEMP) and
        heat generation rate (HGEN) body load labels.

        Body loads specified by the BFV command can conflict with other
        specified body loads.  See Resolution of Conflicting Body Load
        Specifications in the Basic Analysis Guide for details.

        Graphical picking is available only via the listed menu paths.

        This command is also valid in PREP7.

        Examples
        --------
        Set heat generation 1e4 on all selected volumes.

        >>> mapdl.bfv('ALL', 'HGEN', 1e4)
        """
        command = f"BFV,{volu},{lab},{val1},{val2},{val3},{phase}"
        return self.run(command, **kwargs)

    def bfvdele(self, volu="", lab="", **kwargs):
        """Deletes body force loads on a volume.

        APDL Command: BFVDELE

        Parameters
        ----------
        volu
            Volume at which body load is to be deleted.  If ALL, delete for all
            selected volumes [VSEL]. A component name may also be substituted
            for VOLU.

        lab
            Valid body load label. If ALL, use all appropriate labels. Load
            labels are listed under "Body Loads" in the input table for each
            element type in the Element Reference. See the BFV command for
            labels.

        Notes
        -----
        Deletes body force loads (and all corresponding finite element loads)
        for a specified volume and label.  Body loads may be defined on a
        volume with the BFV command.

        Graphical picking is available only via the listed menu paths.

        This command is also valid in PREP7.
        """
        command = f"BFVDELE,{volu},{lab}"
        return self.run(command, **kwargs)

    def bfvlist(self, volu="", lab="", **kwargs):
        """Lists the body force loads on a volume.

        APDL Command: BFVLIST

        Parameters
        ----------
        volu
            Volume at which body load is to be listed.  If ALL (or blank), list
            for all selected volumes [VSEL].  If VOLU = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in
            the GUI).  A component name may also be substituted for VOLU.

        lab
            Valid body load label. If ALL, use all appropriate labels. Load
            labels are listed under "Body Loads" in the input table for each
            element type in the Element Reference. See the BFV command for
            labels.

        Notes
        -----
        Lists the body force loads for the specified volume and label.  Body
        loads may be defined on a volume with the BFV command.

        This command is valid in any processor.
        """
        command = f"BFVLIST,{volu},{lab}"
        return self.run(command, **kwargs)
