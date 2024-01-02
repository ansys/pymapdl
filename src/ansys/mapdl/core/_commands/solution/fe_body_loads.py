class FeBodyLoads:
    def bf(
        self,
        node="",
        lab="",
        val1="",
        val2="",
        val3="",
        val4="",
        val5="",
        val6="",
        **kwargs,
    ):
        """Defines a nodal body force load.

        APDL Command: BF

        Parameters
        ----------
        node
            Node to which body load applies.  If Node = ALL, apply to all
            selected nodes [NSEL].  A component name may also be substituted
            for Node.

        lab
            Valid body load label. Load labels are listed under "Body Loads" in
            the input table for each element type in the Element Reference.

        val1, val2, val3, val4, val5, val6
            Value associated with the Lab item or table name reference for
            tabular boundary conditions. To specify a table, enclose the table
            name in percent signs (%) (e.g., BF,Node,TEMP,%tabname%). Use the
            ``*DIM`` command to define a table. Use only VAL1 for TEMP, FLUE, HGEN,
            DGEN, MVDI, CHRGD. If Lab = CHRGD for acoustics, VAL1 is the static
            pressure for a non-uniform acoustic medium calculation.

            VAL1 - Mass source with units kg/(m3s) in a harmonic analysis, or mass source rate
                   with units kg/( m3s2) in a transient analysis

            VAL2 - Phase angle in degrees

            VAL3 - Not used

            VAL4 - Not used

            VAL5 - Not used

            VAL6 - Not used

        Notes
        -----
        Defines a nodal body force load (such as temperature in a structural
        analysis, heat generation rate in a thermal analysis, etc.). Nodal body
        loads default to the BFUNIF values, if they were previously specified.

        Table names are valid for Lab value (VALn) inputs in these cases only:

        VAL = %tabname% for temperatures (TEMP), diffusing substance generation
        rates (DGEN), heat generation rates (HGEN), and nodal body force
        densities (FORC).

        VAL1 = %tabname1%, VAL2 = %tabname2%, VAL3 = %tabname3%, VAL4 =
        %tabname4%, VAL5 = %tabname5%, and VAL6 = %tabname6% for velocities or
        accelerations (VELO).

        VAL1 = %tabname1% and VAL2 = %tabname2% for mass sources or mass source
        rates (MASS).

        The heat generation rate loads specified with the BF command are
        multiplied by the weighted nodal volume of each element adjacent to
        that node. This yields the total heat generation at that node.

        Graphical picking is available only via the listed menu paths.

        Body load labels VELO and MASS cannot be accessed from a menu.

        This command is also valid in PREP7.
        """
        command = f"BF,{node},{lab},{val1},{val2},{val3},{val4},{val5},{val6}"
        return self.run(command, **kwargs)

    def bfcum(self, lab="", oper="", fact="", tbase="", **kwargs):
        """Specifies that nodal body force loads are to be accumulated.

        APDL Command: BFCUM

        Parameters
        ----------
        lab
            Valid body load label.  If ALL, use all appropriate labels.

        oper
            Accumulation key:

            REPL - Subsequent values replace the previous values (default).

            ADD - Subsequent values are added to the previous values.

            IGNO - Subsequent values are ignored.

        fact
            Scale factor for the nodal body load values.  Zero (or blank)
            defaults to 1.0.  Use a small number for a zero scale factor.  The
            scale factor is not applied to body load phase angles.

        tbase
            Used (only with Lab = TEMP) to calculate the temperature used in
            the add or replace operation (see Oper) as:

        Notes
        -----
        Allows repeated nodal body force loads to be replaced, added, or
        ignored.  Nodal body loads are applied with the BF command.  Issue the
        BFLIST command to list the nodal body loads.  The operations occur when
        the next body loads are defined.  For example, issuing the BF command
        with a temperature of 250 after a previous BF command with a
        temperature of 200 causes the new value of the temperature to be 450
        with the add operation, 250 with the replace operation, or 200 with the
        ignore operation.  A scale factor is also available to multiply the
        next value before the add or replace operation.  A scale factor of 2.0
        with the previous "add" example results in a temperature of 700.  The
        scale factor is applied even if no previous values exist.  Issue
        BFCUM,STAT to show the current label, operation, and scale factors.
        Solid model boundary conditions are not affected by this command, but
        boundary conditions on the FE model are affected.

        Note:: : FE boundary conditions may still be overwritten by existing
        solid model boundary conditions if a subsequent boundary condition
        transfer occurs.

        BFCUM does not work for tabular boundary conditions.

        This command is also valid in PREP7.
        """
        command = f"BFCUM,{lab},{oper},{fact},{tbase}"
        return self.run(command, **kwargs)

    def bfdele(self, node="", lab="", **kwargs):
        """Deletes nodal body force loads.

        APDL Command: BFDELE

        Parameters
        ----------
        node
            Node at which body load is to be deleted.  If ALL, delete for all
            selected nodes [NSEL].  If NODE = P, graphical picking is enabled
            and all remaining command fields are ignored (valid only in the
            GUI).  A component name may also be substituted for NODE.

        lab
            Valid body load label. If ALL, use all appropriate labels. See the
            BF command for labels. In an explicit dynamic analysis, the only
            valid body load label is TEMP.

        Notes
        -----
        Deletes nodal body force loads for a specified node and label.  Nodal
        body loads may be defined with the BF command (except in an explicit
        dynamic analysis).

        The command BFDELE,TEMP can be used in an explicit dynamic analysis to
        delete temperature loads that are read in by the LDREAD command. BFDELE
        cannot be used to delete temperature loads defined by the EDLOAD
        command (use EDLOAD,DELE to delete this type of load).

        This command is also valid in PREP7.
        """
        command = f"BFDELE,{node},{lab}"
        return self.run(command, **kwargs)

    def bfe(
        self,
        elem="",
        lab="",
        stloc="",
        val1="",
        val2="",
        val3="",
        val4="",
        **kwargs,
    ):
        """Defines an element body force load.

        APDL Command: BFE

        Parameters
        ----------
        elem
            The element to which body load applies.  If ALL, apply to all
            selected elements (ESEL). A component name may also be substituted
            for Elem.

        lab
            Valid body load label. Valid labels are also listed for each
            element type in the Element Reference under "Body Loads" in the
            input table.

        stloc
            Starting location for entering VAL data, below.  For example, if
            STLOC = 1, data input in the VAL1 field applies to the first
            element body load item available for the element type, VAL2 applies
            to the second element item, etc. If STLOC = 5, data input in the
            VAL1 field applies to the fifth element item, etc.  Defaults to 1.

        val1, val2, val3, val4
            For Lab = TEMP, FLUE, DGEN, HGEN, and CHRGD, VAL1--VAL4 represent
            body load values at the starting location and subsequent locations
            (usually nodes) in the element.  VAL1 can also represent a table
            name for use with tabular boundary conditions. Enter only VAL1 for
            a uniform body load across the element.  For nonuniform loads, the
            values must be input in the same order as shown in the input table
            for the element type.  Values initially default to the BFUNIF value
            (except for CHRGD which defaults to zero).  For subsequent
            specifications, a blank leaves a previously specified value
            unchanged; if the value was not previously specified, the default
            value as described in the Element Reference is used.

        Notes
        -----
        Defines an element body force load (such as temperature in a structural
        analysis, heat generation rate in a thermal analysis, etc.). Body loads
        and element specific defaults are described for each element type in
        the Element Reference. If both the BF and BFE commands are used to
        apply a body load to an element, the BFE command takes precedence.

        For heat-generation (HGEN) loading on layered thermal solid elements
        SOLID278 / SOLID279 (KEYOPT(3) = 1 or 2), or layered thermal shell
        elements SHELL131 / SHELL132 (KEYOPT(3) = 1), STLOC refers to the layer
        number (not the node). In such cases, use VAL1 through VAL4 to specify
        the heat-generation values for the appropriate layers. Heat generation
        is constant over the layer.

        Specifying a Table

        You can specify a table name (VAL1) when using temperature (TEMP),
        diffusing substance generation rate (DGEN), heat generation rate
        (HGEN), and current density (JS) body load labels.

        Enclose the table name (tabname) in percent signs (%), as shown:

        BFE,Elem, Lab,STLOC,%tabname%

        Use the ``*DIM`` command to define a table.

        For Lab = TEMP, each table defines NTEMP temperatures, as follows:

        For layered elements, NTEMP is the number of layer interface corners
        that allow temperature input.

        For non-layered elements, NTEMP is the number of corner nodes.

        The temperatures apply to element items with a starting location of
        STLOC + n, where n is the value field location (VALn) of the table name
        input.

        For layered elements, a single BFE command returns temperatures for one
        layer interface. Multiple BFE commands are necessary for defining all
        layered temperatures.

        For beam, pipe and elbow elements that allow multiple temperature
        inputs per node, define the tabular load for the first node only (Node
        I), as loads on the remaining nodes are applied automatically. For
        example, to specify a tabular temperature load on a PIPE288 element
        with the through-wall-gradient option (KEYOPT(1) = 0), the BFE command
        looks like this:

        BFE,Elem,TEMP,1,%tabOut%, %tabIn%

        When a tabular function load is applied to an element, the load does
        not vary according to the positioning of the element in space.

        Graphical picking is available only via the listed menu paths.

        This command is also valid in PREP7.
        """
        command = f"BFE,{elem},{lab},{stloc},{val1},{val2},{val3},{val4}"
        return self.run(command, **kwargs)

    def bfecum(self, lab="", oper="", fact="", tbase="", **kwargs):
        """Specifies whether to ignore subsequent element body force loads.

        APDL Command: BFECUM

        Parameters
        ----------
        lab
            Valid body load label.  If ALL, use all appropriate labels.

        oper
            Replace or ignore key:

            REPL - Subsequent values replace the previous values (default).

            IGNO - Subsequent values are ignored.

        fact
            Scale factor for the element body load values.  Zero (or blank)
            defaults to 1.0.  Use a small number for a zero scale factor.  The
            scale factor is not applied to body load phase angles.

        tbase
            Used (only with  Lab = TEMP) to calculate the temperature used in
            the add or replace operation (see Oper) as:

        Notes
        -----
        Allows repeated element body force loads to be replaced or ignored.
        Element body loads are applied with the BFE command.  Issue the BFELIST
        command to list the element body loads.  The operations occur when the
        next body loads are defined.  For example, issuing the BFE command with
        a temperature value of 25 after a previous BFE command with a
        temperature value of 20 causes the new value of that temperature to be
        25 with the replace operation, or 20 with the ignore operation.  A
        scale factor is also available to multiply the next value before the
        replace operation.  A scale factor of 2.0 with the previous "replace"
        example results in a temperature of 50.  The scale factor is applied
        even if no previous values exist.  Issue BFECUM,STAT to show the
        current label, operation, and scale factors.

        BFECUM does not work for tabular boundary conditions.

        This command is also valid in PREP7.
        """
        command = f"BFECUM,{lab},{oper},{fact},{tbase}"
        return self.run(command, **kwargs)

    def bfedele(self, elem="", lab="", **kwargs):
        """Deletes element body force loads.

        APDL Command: BFEDELE

        Parameters
        ----------
        elem
            Element at which body load is to be deleted.  If ALL, delete for
            all selected elements [  A component name may also be substituted
            for ELEM.

        lab
            Valid body load label. If ALL, use all appropriate labels. See BFE
            command for labels.

        Notes
        -----
        Deletes element body force loads for a specified element and label.
        Element body loads may be defined with the BFE commands.

        Graphical picking is available only via the listed menu paths.

        This command is also valid in PREP7.
        """
        command = f"BFEDELE,{elem},{lab}"
        return self.run(command, **kwargs)

    def bfelist(self, elem="", lab="", **kwargs):
        """Lists the element body force loads.

        APDL Command: BFELIST

        Parameters
        ----------
        elem
            Element at which body load is to be listed.  If ALL (or blank),
            list for all selected elements [ESEL].  If ELEM = P, graphical
            picking is enabled and all remaining command fields are ignored
            (valid only in the GUI).  A component name may also be substituted
            for ELEM.

        lab
            Valid body load label. If ALL (or blank), use all appropriate
            labels. See BFE command for labels.

        Notes
        -----
        Lists the element body force loads for the specified element and label.
        Element body loads may be defined with the BFE command.

        This command is valid in any processor.
        """
        command = f"BFELIST,{elem},{lab}"
        return self.run(command, **kwargs)

    def bfescal(self, lab="", fact="", tbase="", **kwargs):
        """Scales element body force loads.

        APDL Command: BFESCAL

        Parameters
        ----------
        lab
            Valid body load label.  If ALL, use all appropriate labels.

        fact
            Scale factor for the element body load values.  Zero (or blank)
            defaults  to 1.0.  Use a small number for a "zero" scale factor.
            The scale factor is not applied to body load phase angles.

        tbase
            Base temperature for temperature difference.  Used only with Lab =
            TEMP.  Scale factor is applied to the temperature difference (T -
            TBASE)  and then added to TBASE.  T is the current temperature.

        Notes
        -----
        Scales element body force loads on the selected elements in the
        database.  Issue the BFELIST command to list the element body loads.
        Solid model boundary conditions are not scaled by this command, but
        boundary conditions on the FE model are scaled.  (Note that such scaled
        FE boundary conditions may still be overwritten by unscaled solid model
        boundary conditions if a subsequent boundary condition transfer
        occurs.)

        BFESCAL does not work for tabular boundary conditions.

        This command is also valid in PREP7.
        """
        command = f"BFESCAL,{lab},{fact},{tbase}"
        return self.run(command, **kwargs)

    def bflist(self, node="", lab="", **kwargs):
        """Lists the body force loads on nodes.

        APDL Command: BFLIST

        Parameters
        ----------
        node
            Node at which body load is to be listed.  If ALL (or blank), list
            for all selected nodes [NSEL].  If NODE = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in
            the GUI).  A component name may also be substituted for NODE.

        lab
            Valid body load label. If ALL (or blank), use all appropriate
            labels. See the BF command for labels. In an explicit dynamic
            analysis, the only valid body load label is TEMP.

        Notes
        -----
        Lists the body force loads for the specified node and label.  Nodal
        body loads may be defined with the BF command (except in an explicit
        dynamic analysis).

        The command BFLIST,TEMP can be used in an explicit dynamic analysis to
        list temperature loads that are read in by the LDREAD command. BFLIST
        cannot be used to list temperature loads defined by the EDLOAD command
        (use EDLOAD,LIST to list this type of load).

        This command is valid in any processor.
        """
        command = f"BFLIST,{node},{lab}"
        return self.run(command, **kwargs)

    def bfscale(self, lab="", fact="", tbase="", **kwargs):
        """Scales body force loads at nodes.

        APDL Command: BFSCALE

        Parameters
        ----------
        lab
            Valid body load label.  If ALL, use all appropriate labels.

        fact
            Scale factor for the nodal body load values.  Zero (or blank)
            defaults  to 1.0.  Use a small number for a zero scale factor.  The
            scale factor is not applied to body load phase angles.

        tbase
            Base temperature for temperature difference.  Used only with Lab =
            TEMP.  Scale factor is applied to the temperature difference (T -
            TBASE)  and then added to TBASE.  T is the current temperature.

        Notes
        -----
        Scales body force loads in the database on the selected nodes.  Issue
        the BFLIST command to list the nodal body loads.  Solid model boundary
        conditions are not scaled by this command, but boundary conditions on
        the FE model are scaled.

        Note:: : Such scaled FE boundary conditions may still be overwritten by
        unscaled solid model boundary conditions if a subsequent boundary
        condition transfer occurs.

        BFSCALE does not work for tabular boundary conditions.

        This command is also valid in PREP7.
        """
        command = f"BFSCALE,{lab},{fact},{tbase}"
        return self.run(command, **kwargs)

    def bfunif(self, lab="", value="", **kwargs):
        """Assigns a uniform body force load to all nodes.

        APDL Command: BFUNIF

        Parameters
        ----------
        lab
            Valid body load label.  If ALL, use all appropriate labels.

        value
            Uniform value associated with Lab item, or table name when
            specifying tabular boundary conditions.  To specify a table,
            enclose the table name in percent signs (%), e.g.,
            BFUNIF,Lab,%tabname%.

        Notes
        -----
        In a transient or nonlinear thermal analysis, the uniform temperature
        is used during the first iteration of a solution as follows:  (a) as
        the starting nodal temperature (except where temperatures are
        explicitly specified [D, DK]), and (b) to evaluate temperature-
        dependent material properties.  In a structural analysis or explicit
        dynamic analysis, the uniform temperature is used as the default
        temperature for thermal strain calculations and material property
        evaluation (except where body load temperatures are specified [BF, BFE,
        BFK, LDREAD]).  In other scalar field analyses, the uniform temperature
        is used for material property evaluation.

        When the command BFUNIF,TEMP is used in an explicit dynamic analysis,
        you cannot use the EDLOAD,TEMP command to apply temperature loading.
        Furthermore, any temperature loading defined by BFUNIF cannot be listed
        or deleted by the EDLOAD command.

        An alternate command, TUNIF, may be used to set the uniform temperature
        instead of BFUNIF,TEMP. Since TUNIF (or BFUNIF,TEMP) is step-applied in
        the first iteration, you should use BF, ALL, TEMP, Value to ramp on a
        uniform temperature load.

        You can specify a table name only when using temperature (TEMP), heat
        generation rate (HGEN), and diffusing substance generation rate (DGEN)
        body load labels. When using TEMP, you can define a one-dimensional
        table that varies with respect to time (TIME) only. When defining this
        table, enter TIME as the primary variable. No other primary variables
        are valid. Tabular boundary conditions cannot be used in an explicit
        dynamic analysis.

        This command is also valid in PREP7.
        """
        command = f"BFUNIF,{lab},{value}"
        return self.run(command, **kwargs)

    def ldread(
        self,
        lab="",
        lstep="",
        sbstep="",
        time="",
        kimg="",
        fname="",
        ext="",
        **kwargs,
    ):
        """Reads results from the results file and applies them as loads.

        APDL Command: LDREAD

        Parameters
        ----------
        lab
            Valid load label:

            TEMP - Temperatures from a thermal analysis are applied as body force nodal loads (BF)
                   in a structural analysis, an explicit dynamic analysis, or
                   other type of analysis.

            If the thermal analysis uses SHELL131 or SHELL132, temperatures are applied as body force element loads (BFE). In most cases, only the top and bottom temperatures from SHELL131 and SHELL132 are used by the structural shell elements; any interior temperatures are ignored.  - All temperatures are used for SHELL181 using section input, and SHELL281 using
                              section input; for these elements, therefore, the
                              number of temperature points at a node generated
                              in the thermal model must match the number of
                              temperature points at a node needed by the
                              structural model.

            When using SHELL131 or SHELL132 information for the LDREAD operation, all element types should specify the same set of thermal degrees of freedom. - When used in conjunction with KIMG=1 and KIMG=2, temperatures can be applied to
                              a subsequent thermal analysis as nodal loads (D)
                              or initial conditions (IC), respectively.

            FORC - Forces from an electromagnetic analysis are applied as force loads (F) in a
                   structural analysis. LDREAD,FORC reads coupling forces. See
                   the discussion on force computation in the Low-Frequency
                   Electromagnetic Analysis Guide.

              For a full harmonic magnetic analysis, FORC represents the time-averaged force (use in conjunction with KIMG = 2).  Values are in the nodal coordinate system for the force loads (F). - HGEN

            Heat generations from an electromagnetic analysis are applied as body force loads (BFE) in a thermal analysis.  For a full harmonic analysis, HGEN represents the time-averaged heat generation load (use in conjunction with KIMG = 2). - JS

            Source current density from a current-conduction analysis are applied as body force loads (BFE).  Values are in the global Cartesian coordinate system. - EF

            Electric field element centroid values from an electrostatic analysis are applied as body force loads (BFE) in a magnetic analysis. Values are in the global Cartesian coordinate system. - REAC

            Reaction loads from any analysis are applied as force loads (F) in any analysis.  Values are in the nodal coordinate system. - CONC

        lstep
            Load step number of the data set to be read.  Defaults to 1.  If
            LAST, ignore SBSTEP and TIME and read the last data set.

        sbstep
            Substep number (within LSTEP).  If zero (or blank), LSTEP
            represents the last substep of the load step.

        time
            Time-point identifying the data set to be read.  Used only if both
            LSTEP and SBSTEP are zero (or blank).  If TIME is between two
            solution time points on the results file, a linear interpolation is
            done between the two data sets.  If TIME is beyond the last time
            point on the file, use the last time point.

        kimg
            When used with results from harmonic analyses (ANTYPE,HARMIC) KIMG
            establishes which set of data to read:

            0 - Read the real part of the solution.  Valid also for Lab = EHFLU to read in
                time-average heat flux.

            1 - Read the imaginary part of the solution.

            2 - Calculate and read the time-average part. Meaningful for Lab = HGEN or FORC.

        fname
            File name and directory path (248 characters maximum, including the
            characters needed for the directory path).  An unspecified
            directory path defaults to the working directory; in this case, you
            can use all 248 characters for the file name.

        ext
            Filename extension (eight-character maximum).

        Notes
        -----
        The LDREAD command reads results data from the results file and applies
        them as loads.

        The command can also apply results from an analysis defined with one
        physics environment as loads on a second analysis using a different
        physics environment. Results values are applied as loads for field-
        coupling effects (for example, output temperatures from a thermal
        analysis as input to a structural analysis).

        The command works based on the assumption that the meshes have not
        changed.

        Nodal loads are applied only to selected nodes. Element loads are
        applied only to selected elements. Element surface loads are applied
        only to selected elements where all face nodes for that surface are
        selected.

        To assure proper distribution of the surface loads, select only the
        nodes on the element face where the surface load is to be applied.

        Scaling and accumulation specifications are applied as the loads are
        read via the following commands:

        BFCUM for body force loads. (Heat-generation loads are not
        accumulated.)
        """
        command = f"LDREAD,{lab},{lstep},{sbstep},{time},{kimg},{fname},{ext}"
        return self.run(command, **kwargs)

    def rimport(
        self,
        source="",
        type_="",
        loc="",
        lstep="",
        sbstep="",
        fname="",
        ext="",
        spscale="",
        mscale="",
        **kwargs,
    ):
        """Imports initial stresses from an explicit dynamics run into ANSYS.

        APDL Command: RIMPORT

        Parameters
        ----------
        source
            The type of analysis run from which stresses are imported.

            OFF - Ignore initial stresses.

            DYNA - Get initial stresses from an earlier explicit
            (ANSYS LS-DYNA) run (default).

        type\_
            Type of data imported.  Note that this is an ANSYS-defined
            field; the only valid value is STRESS.

        loc
            Location where the data is imported.  Note that this is an
            ANSYS- defined field; the only valid value is ELEM (data
            imported at the element integration points).

        lstep
            Load step number of data to be imported.  Defaults to the
            last load step.

        sbstep
            Substep number of data to be imported.  Defaults to the
            last substep.

        fname
            File name and directory path (248 characters maximum,
            including the characters needed for the directory path).
            An unspecified directory path defaults to the working
            directory; in this case, you can use all 248 characters
            for the file name.

        ext
            Filename extension (eight-character maximum).

        spscale
            Stabilization factor. This factor is used in a springback
            analysis to scale (up or down) the initial stiffness of
            the applied spring.  No default; input a value only if you
            want to activate stabilization. If SPSCALE is blank,
            stabilization is not activated.

        mscale
            Acceptable stabilization stiffness (defaults to 1.0 X
            10--4). In a springback analysis, iterations will stop
            when the applied spring stiffness comes down to this
            value. MSCALE is not used if SPSCALE is blank.

        Notes
        -----
        This command imports initial stress information into ANSYS
        from an earlier explicit (ANSYS LS-DYNA) run.  The stress
        state from SHELL163 and SOLID164 elements in the explicit
        analysis is imported to the corresponding SHELL181 and
        SOLID185 implicit elements. For the shell elements, the
        current shell element thickness is also imported. This command
        is valid only before the first SOLVE command of the implicit
        analysis (which comes after the explicit analysis) and is
        ignored if issued after subsequent SOLVE commands (that is,
        stresses will not be re-imported).

        RIMPORT is typically used to perform springback analysis of
        sheet metal forming. We recommend that you use SHELL163
        elements in the explicit analysis with 3 to 5 integration
        points through the thickness. This ensures that the
        through-thickness stress distribution is transferred
        accurately to the SHELL181 elements. If more than 5
        integration points are used, ANSYS imports resultants (forces
        and moments) to the SHELL181 elements. This implies that
        linearization of the through-thickness stress distribution is
        assumed in SHELL181 elements. If SHELL163 uses full
        integration in the shell plane, stress and thickness data are
        averaged and then transferred. For the solid elements, the
        stress at the SOLID164 element centroid is transferred to the
        SOLID185 element centroid. If SOLID164 has full integration,
        the stress is averaged and then transferred.

        When the SPSCALE argument is specified, artificial springs
        with exponentially decaying stiffness (as a function of
        iterations) are applied. This technique is recommended only
        for those cases in which there are severe convergence
        difficulties. In general, you should first attempt a
        springback analysis without using the stabilization factors
        SPSCALE and MSCALE. (For more information on springback
        stabilization, see the ANSYS LS-DYNA User's Guide.)

        This command is not written to the Jobname.CDB file when the
        CDWRITE command is issued. Further, the RIMPORT information is
        not saved to the database; therefore, the RIMPORT command must
        be reissued if the database is resumed.

        This command is also valid in PREP7.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"RIMPORT,{source},{type_},{loc},{lstep},{sbstep},{fname},{ext},,{spscale},{mscale}"
        return self.run(command, **kwargs)

    def tunif(self, temp="", **kwargs):
        """Assigns a uniform temperature to all nodes.

        APDL Command: TUNIF

        Parameters
        ----------
        temp
            Uniform temperature assigned to the nodes. If a TEMP value is not
            specified, the uniform temperature is set to zero.

        Notes
        -----
        TUNIF is a convenient form of the more general BFUNIF command.

        In a transient or nonlinear thermal analysis, the uniform temperature
        is used during the first iteration of a solution as follows:

        as the starting nodal temperature (except where temperatures are
        explicitly specified [D, DK]),

        to evaluate temperature-dependent material properties.

        In a structural analysis or an explicit dynamic analysis, the uniform
        temperature is used as the default temperature for thermal strain
        calculations and material property evaluation (except where body load
        temperatures are specified (BF, BFE, BFK, LDREAD). In other scalar
        field analyses, the uniform temperature is used for material property
        evaluation.

        Because TUNIF (or BFUNIF,TEMP) is step-applied in the first iteration,
        issue a BF,ALL,TEMP,Value command to ramp on a uniform temperature
        load.

        When the TUNIF command is used in an explicit dynamic analysis, you
        cannot apply temperature loading via the EDLOAD,,TEMP command.
        Furthermore, temperature loading defined by TUNIF cannot be listed or
        deleted by the EDLOAD command.

        The command default sets the uniform temperature to the reference
        temperature defined via the TREF command only (and not the MP,REFT
        command).

        If using the command default to set the uniform temperature (to the
        reference temperature set via TREF), you can convert temperature-
        dependent secant coefficients of thermal expansion (SCTEs) from the
        definition temperature to the uniform temperature. To do so, issue the
        MPAMOD command.

        This command is also valid in PREP7.
        """
        command = f"TUNIF,{temp}"
        return self.run(command, **kwargs)
