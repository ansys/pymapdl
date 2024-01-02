class SolidSurfaceLoads:
    def sfa(self, area="", lkey="", lab="", value="", value2="", **kwargs):
        """Specifies surface loads on the selected areas.

        APDL Command: SFA

        Parameters
        ----------
        area
            Area to which surface load applies.  If ALL, apply load to all
            selected areas [ASEL].  A component may be substituted for Area.

        lkey
            Load key associated with surface load (defaults to 1).  Load keys
            (1,2,3, etc.) are listed under "Surface Loads" in the input data
            table for each element type in the Element Reference.  LKEY is
            ignored if the area is the face of a volume region meshed with
            volume elements.

        lab
            Valid surface load label.  Load labels are listed under "Surface
            Loads" in the input table for each area type in the Element
            Reference.

        value
            Surface load value or table name reference for specifying tabular
            boundary conditions.

        value2
            Second surface load value (if any).

        Notes
        -----
        Surface loads may be transferred from areas to elements with the SFTRAN
        or SBCTRAN commands.  See the SFGRAD command for an alternate tapered
        load capability.

        Tabular boundary conditions (VALUE = %tabname% and/or VALUE2 =
        %tabname%) are available for the following surface load labels (Lab)
        only: : PRES (real and/or imaginary components), CONV (film coefficient
        and/or bulk temperature) or HFLUX, and RAD (surface emissivity and
        ambient temperature). Use the ``*DIM`` command to define a table.

        This command is also valid in PREP7.

        Examples
        --------
        Select areas with coordinates in the range ``0.4 < Y < 1.0``

        >>> mapdl.asel('S', 'LOC', 'Y', 0.4, 1.0)

        Set pressure to 250e3 on all areas.

        >>> mapdl.sfa('ALL', '', 'PRES', 250e3)
        """
        command = f"SFA,{area},{lkey},{lab},{value},{value2}"
        return self.run(command, **kwargs)

    def sfadele(self, area="", lkey="", lab="", **kwargs):
        """Deletes surface loads from areas.

        APDL Command: SFADELE

        Parameters
        ----------
        area
            Area to which surface load deletion applies.  If ALL, delete load
            from all selected areas [ASEL].  A component name may be substituted for AREA.

        lkey
            Load key associated with surface load (defaults to 1).  See the SFA
            command for details.

        lab
            Valid surface load label.  If ALL, use all appropriate labels.  See
            the SFA command for labels.

        Notes
        -----
        Deletes surface loads (and all corresponding finite element loads) from
        selected areas.

        This command is also valid in PREP7.

        Examples
        --------
        Delete all convections applied to all areas where ``-1 < X < -0.5``

        >>> mapdl.asel('S', 'LOC', 'X', -1, -0.5)
        >>> mapdl.sfadele('ALL', 'CONV')
        """
        command = f"SFADELE,{area},{lkey},{lab}"
        return self.run(command, **kwargs)

    def sfalist(self, area="", lab="", **kwargs):
        """Lists the surface loads for the specified area.

        APDL Command: SFALIST

        Parameters
        ----------
        area
            Area at which surface load is to be listed.  If ALL (or blank),
            list for all selected areas [ASEL].  If AREA = P, graphical picking
            is enabled and all remaining command fields are ignored (valid only
            in the GUI).  A component name may be substituted for AREA.

        lab
            Valid surface load label.  If ALL (or blank), use all appropriate
            labels.  See the SFA command for labels.

        Notes
        -----
        This command is valid in any processor.
        """
        command = f"SFALIST,{area},{lab}"
        return self.run(command, **kwargs)

    def sfl(self, line="", lab="", vali="", valj="", val2i="", val2j="", **kwargs):
        """Specifies surface loads on lines of an area.

        APDL Command: SFL

        Parameters
        ----------
        line
            Line to which surface load applies.  If ALL, apply load to all
            selected lines [LSEL].  If Line = P, graphical picking is enabled
            and all remaining command fields are ignored (valid only in the
            GUI).  A component name may be substituted for Line.

        lab
            Valid surface load label.  Load labels are listed under "Surface
            Loads" in the input table for each element type in the Element
            Reference.

        vali, valj
            Surface load values at the first keypoint (VALI) and at the second
            keypoint (VALJ) of the line, or table name for specifying tabular
            boundary conditions.  If VALJ is blank, it defaults to VALI.  If
            VALJ is zero, a zero is used.  If Lab = CONV, VALI and VALJ are the
            film coefficients and VAL2I and VAL2J are the bulk temperatures.
            To specify a table, enclose the table name in percent signs (%),
            e.g., %tabname%.  Use the ``*DIM`` command to define a table.  If Lab =
            CONV and VALI = -N, the film coefficient may be a function of
            temperature and is determined from the HF property table for
            material N [MP].  If Lab = RAD, VALI and VALJ values are surface
            emissivities and VAL2I and VAL2J are ambient temperatures.  The
            temperature used to evaluate the film coefficient is usually the
            average between the bulk and wall temperatures, but may be user
            defined for some elements.  If Lab = RDSF, VALI is the emissivity
            value; the following condition apply: If VALI = -N, the emissivity
            may be a function of the temperature and is determined from the
            EMISS property table for material N [MP]. If Lab = FSIN in a Multi-
            field solver (single or multiple code coupling) analysis, VALI is
            the surface interface number. If Lab = FSIN in a unidirectional
            ANSYS to CFX analysis, VALJ is the surface interface number (not
            available from within the GUI) and VALI is not used unless the
            ANSYS analysis is performed using the Multi-field solver.

        val2i, val2j
            Second surface load values (if any).  If Lab = CONV, VAL2I and
            VAL2J are the bulk temperatures. If Lab = RAD, VAL2I and VAL2J are
            the ambient temperatures. If Lab = RDSF, VAL2I is the enclosure
            number. Radiation will occur between surfaces flagged with the same
            enclosure numbers. If the enclosure is open, radiation will occur
            to the ambient. VAL2I and VAL2J are not used for other surface load
            labels.  If VAL2J is blank, it defaults to VAL2I.  If VAL2J is
            zero, a zero is used.  To specify a table (Lab = CONV), enclose the
            table name in percent signs (%), e.g., %tabname%.  Use the ``*DIM``
            command to define a table.

        Notes
        -----
        Specifies surface loads on the selected lines of area regions.  The
        lines represent either the edges of area elements or axisymmetric shell
        elements themselves.  Surface loads may be transferred from lines to
        elements with the SFTRAN or SBCTRAN commands.  See the SFE command for
        a description of surface loads.  Loads input on this command may be
        tapered.  See the SFGRAD command for an alternate tapered load
        capability.

        You can specify a table name only when using structural (PRES) and
        thermal (CONV [film coefficient and/or bulk temperature], HFLUX), and
        surface emissivity and ambient temperature (RAD) surface load labels.
        VALJ and VAL2J are ignored for tabular boundary conditions.

        This command is also valid in PREP7.
        """
        command = f"SFL,{line},{lab},{vali},{valj},{val2i},{val2j}"
        return self.run(command, **kwargs)

    def sfldele(self, line="", lab="", **kwargs):
        """Deletes surface loads from lines.

        APDL Command: SFLDELE

        Parameters
        ----------
        line
            Line to which surface load deletion applies.  If ALL, delete load
            from all selected lines [LSEL].  If LINE = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in
            the GUI).  A component name may be substituted for LINE.

        lab
            Valid surface load label.  If ALL, use all appropriate labels.  See
            the SFL command for labels.

        Notes
        -----
        Deletes surface loads (and all corresponding finite element loads) from
        selected lines.

        This command is also valid in PREP7.
        """
        command = f"SFLDELE,{line},{lab}"
        return self.run(command, **kwargs)

    def sfllist(self, line="", lab="", **kwargs):
        """Lists the surface loads for lines.

        APDL Command: SFLLIST

        Parameters
        ----------
        line
            Line at which surface load is to be listed.  If ALL (or blank),
            list for all selected lines [LSEL].  If LINE = P, graphical picking
            is enabled and all remaining command fields are ignored (valid only
            in the GUI).  A component name may be substituted for LINE.

        lab
            Valid surface load label.  If ALL (or blank), use all appropriate
            labels.  See the SFL command for labels.

        Notes
        -----
        Lists the surface loads for the specified line.

        This command is valid in any processor.
        """
        command = f"SFLLIST,{line},{lab}"
        return self.run(command, **kwargs)

    def sftran(self, **kwargs):
        """Transfer the solid model surface loads to the finite element model.

        APDL Command: SFTRAN

        Notes
        -----
        Surface loads are transferred only from selected lines and areas to all
        selected elements.  The SFTRAN operation is also done if the SBCTRAN
        command is issued or automatically done upon initiation of the solution
        calculations [SOLVE].

        This command is also valid in PREP7.
        """
        command = f"SFTRAN,"
        return self.run(command, **kwargs)
