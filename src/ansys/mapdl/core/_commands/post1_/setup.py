class Setup:
    def append(
        self,
        lstep="",
        sbstep="",
        fact="",
        kimg="",
        time="",
        angle="",
        nset="",
        **kwargs,
    ):
        """Reads data from the results file and appends it to the database.

        APDL Command: APPEND

        Parameters
        ----------
        lstep
            Load step number of the data set to be read.  Defaults to 1.  If
            FIRST, ignore SBSTEP and TIME and read the first data set.  If
            LAST, ignore SBSTEP and TIME and read the last data set.  If NEXT,
            ignore SBSTEP and TIME and read the next data set.  If already at
            the last data set, the next set is the first data set.  If NEAR,
            ignore SBSTEP and read the data set nearest to TIME.  If TIME is
            blank, read the first data set.  If LIST, scan the results file to
            produce a summary of each load step (FACT, KIMG, TIME  and ANGLE
            are ignored).

        sbstep
            Substep number (within LSTEP) (defaults to last substep of load
            step).   For the Buckling (ANTYPE,BUCKLE) or Modal (ANTYPE,MODAL)
            analysis, the substep corresponds to the mode number (defaults to
            first mode).  If LSTEP = LIST, SBSTEP = 0 or 1 will list the basic
            load step information;  SBSTEP = 2 will also list the load step
            title, and label the imaginary data sets if they exist.

        fact
            Scale factor applied to data read from the file.  If zero (or
            blank), a value of 1.0 is used.  Harmonic velocities or
            accelerations may be calculated from the displacement results from
            a modal or harmonic (ANTYPE,HARMIC) analyses.  If FACT = VELO, the
            harmonic velocities (v) are calculated from the displacements (d)
            at a particular frequency (f) according to the relationship v =
            2 πfd.  Similarly, if FACT = ACEL, the harmonic accelerations (a)
            are calculated as a = (2 πf)2d.

        kimg
            Used only with results from complex analyses:

            0 - Store real part of complex solution.

            1 - Store imaginary part.

        time
            Time-point identifying the data set to be read.  For harmonic
            analyses, time corresponds to the frequency.  For the buckling
            analysis, time corresponds to the load factor.  Used only in the
            following cases:  If LSTEP is NEAR, read the data set nearest to
            TIME.   If both LSTEP and SBSTEP are zero (or blank), read data set
            at time = TIME.  If TIME is between two solution time points on the
            results file, a linear interpolation is done between the two data
            sets.  Solution items not written to the results file [OUTRES] for
            either data set will result in a null item after data set
            interpolation.  If TIME is beyond the last time point on the file,
            the last time point is used.

        angle
            Circumferential location (0° to 360°).  Defines the circumferential
            location for the harmonic calculations used when reading from the
            results file.  The harmonic factor (based on the circumferential
            angle) is applied to the harmonic elements (PLANE25, PLANE75,
            PLANE78, PLANE83, and SHELL61) of the load case.  See the
            Mechanical APDL Theory Reference for details.  Note that factored
            values of applied constraints and loads will overwrite any values
            existing in the database.

        nset
            Data set number of the data set to be read.  If a positive value
            for NSET is entered, LSTEP, SBSTEP, KIMG, and TIME are ignored.
            Available set numbers can be determined by APPEND,LIST.  To
            determine if data sets are real or imaginary, issue APPEND,LIST,2
            which labels imaginary data sets.

        Notes
        -----
        Reads a data set from the results file and appends it to the existing
        data in the database for the selected model only.  The existing
        database is not cleared (or overwritten in total), allowing the
        requested results data to be merged into the database.  Various
        operations may also be performed during the read operation.  The
        database must have the model geometry available (or used the RESUME
        command before the APPEND command to restore the geometry from
        File.DB).
        """
        command = f"APPEND,{lstep},{sbstep},{fact},{kimg},{time},{angle},{nset}"
        return self.run(command, **kwargs)

    def desol(
        self,
        elem="",
        node="",
        item="",
        comp="",
        v1="",
        v2="",
        v3="",
        v4="",
        v5="",
        v6="",
        **kwargs,
    ):
        """Defines or modifies solution results at a node of an element.

        APDL Command: DESOL

        Parameters
        ----------
        elem
            Element number for which results are defined or modified.  If ALL,
            apply to all selected elements [ESEL].

        node
            Node of element (actual node number, not the position) to which
            results are specified.  If ALL, specify results for all selected
            nodes [NSEL] of element.  If NODE = P, graphical picking is enabled
            and all remaining command fields are ignored (valid only in the
            GUI).  A component name may also be substituted for NODE.

        item
            Label identifying results.  Valid item labels are shown in
            Table 129: DESOL - Valid Item and Component Labels below.  Some
            items also require a component label (Comp).

        comp
            Component of the item (if required); see Table 129: DESOL - Valid
            Item and Component Labels.

        v1
            Value (in the element coordinate system) assigned to the database
            item (and component, if any).  If zero, a zero value will be
            assigned.  If blank, value remains unchanged.

        v2, v3, v4, . . . , v6
            Additional values (if any) assigned to the remaining components (in
            the order corresponding to the Comp list shown below) for the
            specified Item (starting from the specified Comp label and
            proceeding to the right).

        Notes
        -----
        The DESOL command defines or modifies solution results in the database
        at a node of an area or volume element.  For example,
        DESOL,35,50,S,X,1000,2000,1000 assigns values 1000, 2000, and 1000 to
        SX, SY, and SZ (respectively) of node 50 of element 35.

        The settings of the POST1 FORCE, SHELL, and LAYER commands, if
        applicable, further specify which database items are affected.

        For layered composite shells, specify the current element layer (LAYER)
        before issuing the DESOL command.

        All data is stored in the solution coordinate system but is displayed
        in the results coordinate system (RSYS). To list the current results,
        use the PRESOL command.

        Modified solution results are not saved automatically. To save separate
        records of modified results, use either the RAPPND or LCWRITE command.

        Result items are available depending on element type; check the
        individual element for availability. Valid item and component labels
        for element results are:

        Table: 129:: : DESOL - Valid Item and Component Labels
        """
        command = f"DESOL,{elem},{node},{item},{comp},{v1},{v2},{v3},{v4},{v5},{v6}"
        return self.run(command, **kwargs)

    def dnsol(
        self,
        node="",
        item="",
        comp="",
        v1="",
        v2="",
        v3="",
        v4="",
        v5="",
        v6="",
        **kwargs,
    ):
        """Defines or modifies solution results at a node.

        APDL Command: DNSOL

        Parameters
        ----------
        node
            Node for which results are specified.  If ALL, apply to all
            selected nodes [NSEL].  If NODE = P, graphical picking is enabled
            and all remaining command fields are ignored (valid only in the
            GUI).  A component name may also be substituted for NODE.

        item
            Label identifying results, see Table 131: DNSOL - Valid Item and
            Component Labels.   Items also require a component label.

        comp
            Component of the item.  Valid component labels are shown
            Table 131: DNSOL - Valid Item and Component Labels below.

        v1, v2, v3, . . . , v6
            Value assigned to result.  If zero, a zero value will be assigned.
            If blank, the value remains unchanged.  Additional values (if any)
            assigned to the remaining components (in the order corresponding to
            the Comp list shown below for the specified Item (starting from the
            specified Comp label and proceeding to the right).

        Notes
        -----
        DNSOL can be used only with FULL graphics activated (/GRAPHICS,FULL);
        it will not work correctly with PowerGraphics activated.

        DNSOL defines or modifies solution results in the database at a node.
        For example, DNSOL,35,U,X,.001,.002,.001 assigns values 0.001, 0.002,
        and 0.001 to UX, UY, and UZ (respectively) for node 35.  All results
        that are changed in the database, including the nodal degree of freedom
        results, are available for all subsequent operations.   All data is
        stored in the solution coordinate system, but will be displayed in the
        results coordinate system [RSYS].  Use the PRNSOL command to list the
        current results.

        Data input by DNSOL is stored in temporary space and does not replace
        information in the database. Therefore, data input by this command may
        be overwritten if a change is made to the selected set of nodes.

        Issuing the DNSOL command or its GUI equivalent requires you to place
        the data type (stress/strain) in the element nodal records.  To get
        around this requirement, use the DESOL command or equivalent path to
        add a "dummy" element stress/strain record.

        Result items are available depending on element type; check the
        individual element for availability. Valid item and component labels
        for element results are:

        Table: 131:: : DNSOL - Valid Item and Component Labels

        For SHELL131 and SHELL132 elements with KEYOPT(3) = 0 or 1, use the
        labels TBOT, TE2, TE3, ..., TTOP instead of TEMP.
        """
        command = f"DNSOL,{node},{item},{comp},{v1},{v2},{v3},{v4},{v5},{v6}"
        return self.run(command, **kwargs)

    def hrcplx(
        self,
        loadstep="",
        substep="",
        omegat="",
        firstlc_ase="",
        secondlc_ase="",
        **kwargs,
    ):
        """Computes and stores in the database the time-harmonic solution at a

        APDL Command: HRCPLX
        prescribed phase angle.

        Parameters
        ----------
        loadstep
            Load step number of the data set to be read (defaults to 1).

        substep
            Substep number within LOADSTEP.

        omegat
            Angle in degrees (Ω (angle) times T (time)).

        1stlcase
            First load case number (defaults to 1).

        2ndlcase
            Second load case number (defaults to 2).

        Notes
        -----
        HRCPLX invokes a macro that combines the real and imaginary parts of
        the solution. If the angle is specified, it produces the following:

        Where:

        RR and RI are, respectively, the real and imaginary parts of the
        results quantity (e.g. the nodal displacements, the reaction forces,
        ...).

        α is the angle (OMEGAT).

        1STLCASE and 2NDLCASE are internally generated load cases. You may want
        to specify these to avoid overwriting an existing load case number 1 or
        2.

        Not all results computed by this command are valid. See Summable, Non-
        Summable and Constant Data in the Basic Analysis Guide for more
        information. When the amplitude of the solution is requested (OMEGAT >=
        360°), averaged values (such as the nodal component stresses, which are
        an average of element nodal component stresses) are calculated by
        averaging the amplitudes. Because the degrees of freedom results have
        different phases, derived results (such as the equivalent stress SEQV)
        are not valid. See POST1 and POST26 – Complex Results Postprocessing
        for more details about post-processing complex results.

        For postprocessing amplitudes, the only appropriate coordinate system
        is the solution coordinate system (RSYS ,SOLU).  When displaying the
        displacement amplitudes, use a contour display (PLNSOL command).
        Because a deformed shape display (PLDISP command) could lead to a non-
        physical shape, the displacement scaling is off by default
        (/DSCALE,,OFF).

        For postprocessing cylindrical geometry, it is suggested that you
        rotate the element coordinate systems into the appropriate cylindrical
        system (EMODIF,,ESYS) before running the solution and then view the
        results in this system (RSYS,SOLU) in POST1.

        Since HRCPLX performs load case combinations, it alters most of the
        data in the database. In particular, it alters applied loads such as
        forces and imposed displacements. To restore the original loads in the
        database for a subsequent analysis, reissue the SET command in POST1 to
        retrieve the real and imaginary set data.

        To animate the solution over one period, use the ANHARM command.

        OMEGAT is not equal to the phase shift.

        This command is not supported after a cyclic symmetry analysis; use
        /CYCEXPAND,,PHASEANG instead.
        """
        command = f"HRCPLX,{loadstep},{substep},{omegat},{firstlc_ase},{secondlc_ase}"
        return self.run(command, **kwargs)

    def rescombine(
        self,
        numfiles="",
        fname="",
        ext="",
        lstep="",
        sbstep="",
        fact="",
        kimg="",
        time="",
        angle="",
        nset="",
        order="",
        **kwargs,
    ):
        """Reads results from local results files into the database after a

        APDL Command: RESCOMBINE
        distributed memory parallel (Distributed ANSYS) solution.

        Parameters
        ----------
        numfiles
            Number of local results files that are to be read into the database
            from the distributed memory parallel solution. This number should
            be equal to the number of processes used in the parallel solution.

        fname
            File name (jobname) used during the distributed parallel solution.
            The file name must be an alphanumeric string (up to 32 characters)
            enclosed in single quotes.

        ext
            File extension for the results files (for example, RST, RTH, RMG,
            etc.). The file extension must be an alphanumeric string (up to 8
            characters) enclosed in single quotes.

        lstep
            Load step number of the data set to be read (defaults to 1):

            N - Read load step N.

            FIRST - Read the first data set (Sbstep and TIME are ignored).

            LAST - Read the last data set (Sbstep and TIME are ignored).

            NEXT - Read the next data set (Sbstep and TIME are ignored).  If at the last data set,
                   the first data set will be read as the next.

            PREVIOUS - Read the previous data set (Sbstep and TIME are ignored).  If at the first data
                       set, the last data set will be read as the previous.

            NEAR - Read the data set nearest to TIME (Sbstep is ignored).  If TIME is blank, read
                   the first data set.

            LIST - Scan the results files and list a summary of each load step (KIMG, TIME, ANGLE,
                   NSET, and ORDER are ignored.)

        sbstep
            Substep number within Lstep (defaults to the last substep of the
            load step). For a buckling (ANTYPE,BUCKLE) or modal (ANTYPE,MODAL)
            analysis, Sbstep corresponds to the mode number (defaults to the
            first mode). Specify Sbstep = LAST to store the last substep for
            the specified load step.

        fact
            Scale factor applied to data read from the files. If zero (or
            blank), a value of 1.0 is used. A nonzero factor excludes non-
            summable items. Harmonic velocities or accelerations may be
            calculated from the displacement results from a modal
            (ANTYPE,MODAL) or harmonic (ANTYPE,HARMIC) analysis. If Fact =
            VELO, the harmonic velocities (v) are calculated from the
            displacements (d) at a particular frequency (f) according to the
            relationship v = 2πfd. Similarly, if Fact = ACEL, the harmonic
            accelerations (a) are calculated as a = (2πf)2d.

        kimg
            Used only with complex results (harmonic and complex modal
            analyses).

            0 or REAL - Store the real part of a complex solution (default).

            1, 2 or IMAG - Store the imaginary part of a complex solution.

            3 or AMPL - Store the amplitude.

            4 or PHAS - Store the phase angle. The angle value, expressed in degrees, will be between
                        -180°  and +180°.

        time
            Time-point identifying the data set to be read. For a harmonic
            analysis, time corresponds to the frequency. For a buckling
            analysis, time corresponds to the load factor.  Used only in the
            following cases:  If Lstep = NEAR, read the data set nearest to
            TIME. If both Lstep and Sbstep are zero (or blank), read data set
            at time = TIME. If TIME is between two solution time points on the
            results file, a linear interpolation is done between the two data
            sets. Solution items not written to the results file (OUTRES) for
            either data set will result in a null item after data set
            interpolation. If TIME is beyond the last time point on the file,
            the last time point will be used.

        angle
            Circumferential location (0.0 to 360°). Defines the circumferential
            location for the harmonic calculations used when reading from the
            results file. The harmonic factor (based on the circumferential
            angle) is applied to the harmonic elements (PLANE25, PLANE75,
            PLANE78, PLANE83, and SHELL61) of the load case. See the Mechanical
            APDL Theory Reference for details. Note that factored values of
            applied constraints and loads will overwrite any values existing in
            the database.

        nset
            Data set number of the data set to be read. If a positive value for
            NSET is entered, Lstep, Sbstep, KIMG, and TIME are ignored.
            Available set numbers can be determined by RESCOMBINE,,,,LIST.

        order
            Key to sort the harmonic index results. This option applies to
            cyclic symmetry buckling and modal analyses only, and is valid only
            when Lstep = FIRST, LAST, NEXT, PREVIOUS, NEAR or LIST.

            ORDER  - Sort the harmonic index results in ascending order of eigenfrequencies or
                     buckling load multipliers.

            (blank)  - No sorting takes place.

        Notes
        -----
        RESCOMBINE is an ANSYS command macro that allows you to combine results
        from a distributed memory parallel (Distributed ANSYS) solution. In a
        distributed memory parallel solution, a global results file is saved by
        default. However, if you issued DMPOPTION,RST,NO in the parallel
        solution, no global results file is written and all local results files
        will be kept. In this case, you can use the RESCOMBINE command macro in
        the general postprocessor (/POST1) to read results into the database
        for postprocessing.

        In order to use the RESCOMBINE command, all local results files from
        the distributed memory parallel solution must be in the current working
        directory. If running on a single machine, the local results files are
        saved in the working directory by default. If running on a cluster, the
        local results files are kept in the working directory on each compute
        node. For this latter case, you must copy the local results files to
        the working directory on the primary compute node.

        Similar to the SET command, the RESCOMBINE command macro defines the
        data set to be read from the results files into the database. Various
        operations may also be performed during the read operation (see the SET
        command for more details). The database must have the model data
        available (or use the RESUME command before the RESCOMBINE command to
        restore the geometry from Jobname.DB).

        After a set of data is combined into the database using RESCOMBINE, the
        RESWRITE command can be used to write this set of data into a new
        results file. This new results file will essentially contain the
        current set of results data for the entire (i.e., global) model.
        """
        command = f"RESCOMBINE,{numfiles},{fname},{ext},{lstep},{sbstep},{fact},{kimg},{time},{angle},{nset},{order}"
        return self.run(command, **kwargs)

    def set(
        self,
        lstep="",
        sbstep="",
        fact="",
        kimg="",
        time="",
        angle="",
        nset="",
        order="",
        **kwargs,
    ):
        """Defines the data set to be read from the results file.

        APDL Command: SET

        Parameters
        ----------
        lstep
            Load step number of the data set to be read (defaults to 1):

            N
              Read load step N.

            FIRST
              Read the first data set (``Sbstep`` and ``TIME`` are ignored).

            LAST
              Read the last data set (``Sbstep`` and ``TIME`` are ignored).

            NEXT
              Read the next data set (``Sbstep`` and ``TIME`` are ignored). If at the last data set,
              the first data set will be read as the next.

            PREVIOUS
              Read the previous data set (``Sbstep`` and ``TIME`` are ignored). If at the first data
              set, the last data set will be read as the previous.

            NEAR
              Read the data set nearest to ``TIME`` (``Sbstep`` is ignored). If ``TIME`` is blank, read
              the first data set.

            LIST
              Scan the results file and list a summary of each load step.  (``KIMG``, ``TIME``,
              ``ANGLE``, and ``NSET`` are ignored.)

              .. versionchanged:: 0.64
                From version 0.64 you can use the methods ``to_list`` and
                ``to_array`` on the object returning from ``mapdl.set("list")``.

        sbstep
            Substep number (within Lstep). Defaults to the last substep of the
            load step (except in a buckling or modal analysis). For a buckling
            (``ANTYPE,BUCKLE``) or modal (``ANTYPE,MODAL``) analysis, ``Sbstep``
            corresponds to the mode number. Specify ``Sbstep = LAST`` to store the
            last substep for the specified load step (that is, issue a
            ``SET,Lstep,LAST`` command).

        fact
            Scale factor applied to data read from the file. If zero (or
            blank), a value of 1.0 is used. This scale factor is only applied
            to displacement and stress results. A nonzero factor excludes non-
            summable items.

        kimg
            Used only with complex results (harmonic and complex modal
            analyses).

            0 or REAL
              Store the real part of complex solution (default).

            1, 2 or IMAG
              Store the imaginary part of a complex solution.

            3 or AMPL
              Store the amplitude

            4 or PHAS
              Store the phase angle. The angle value, expressed in degrees,
              will be between -180°  and +180°.

        time
            Time-point identifying the data set to be read.  For a harmonic
            analyses, time corresponds to the frequency.

        angle
            Circumferential location (0.0 to 360°).  Defines the
            circumferential location for the harmonic calculations used when
            reading from the results file.

        nset
            Data set number of the data set to be read.  If a positive value
            for ``NSET`` is entered, ``Lstep``, ``Sbstep``, ``KIMG``, and ``TIME`` are ignored.
            Available set numbers can be determined by ``SET,LIST``.

        order
            Key to sort the harmonic index results. This option applies to
            cyclic symmetry buckling and modal analyses only, and is valid only
            when ``Lstep = FIRST, LAST, NEXT, PREVIOUS, NEAR or LIST``.

            ORDER
              Sort the harmonic index results in ascending order of eigenfrequencies or
              buckling load multipliers.

            (blank)
              No sorting takes place.

        Notes
        -----
        Defines the data set to be read from the results file into the
        database.  Various operations may also be performed during the read
        operation.  The database must have the model geometry available (or use
        the ``RESUME`` command before the ``SET`` command to restore the geometry from
        ``<Jobname.DB>``).  Values for applied constraints [``D``] and loads [``F``] in the
        database will be replaced by their corresponding values on the results
        file, if available. (See the description of the ``OUTRES`` command.)  In a
        single load step analysis, these values are usually the same, except
        for results from harmonic elements. (See the description of the ANGLE
        value above.)

        In an interactive run, the sorted list (``ORDER`` option) is also available
        for results-set reading via a GUI pick option.

        You can postprocess results without issuing a ``SET`` command if the
        solution results were saved to the database file (``<Jobname.DB>``).
        Distributed ANSYS, however, can only postprocess using the results file
        (for example, Jobname.RST) and cannot use the ``<Jobname.DB>`` file since no
        solution results are written to the database. Therefore, you must issue
        a ``SET`` command or a ``RESCOMBINE`` command before postprocessing in
        Distributed ANSYS.
        """
        command = f"SET,{lstep},{sbstep},{fact},{kimg},{time},{angle},{nset},{order}"
        return self.run(command, **kwargs)

    def subset(
        self,
        lstep="",
        sbstep="",
        fact="",
        kimg="",
        time="",
        angle="",
        nset="",
        **kwargs,
    ):
        """Reads results for the selected portions of the model.

        APDL Command: SUBSET

        Parameters
        ----------
        lstep
            Load step number of the data set to be read (defaults to 1):

            N
              Read load step N.

            FIRST
              Read the first data set (``SBSTEP`` and ``TIME`` are ignored).

            LAST
              Read the last data set (``SBSTEP`` and ``TIME`` are ignored).

            NEXT
              Read the next data set (``SBSTEP`` and ``TIME`` are ignored).  If at the last data set,
              the first data set will be read as the next.

            NEAR
              Read the data set nearest to ``TIME`` (``SBSTEP`` is ignored).  If ``TIME`` is blank, read
              the first data set.

            LIST
              Scan the results file and list a summary of each load step.  (``FACT``, ``KIMG``, ``TIME``
              and ``ANGLE`` are ignored.)

        sbstep
            Substep number (within Lstep).   For the buckling (``ANTYPE,BUCKLE``)
            analysis or the modal (``ANTYPE,MODAL``) analysis, the substep
            corresponds to the mode number.  Defaults to last substep of load
            step (except for ``ANTYPE,BUCKLE or MODAL``).  If ``Lstep = LIST, SBSTEP
            = 0 or 1`` lists the basic step information, whereas ``SBSTEP = 2`` also
            lists the load step title, and labels imaginary data sets if they
            exist.

        fact
            Scale factor applied to data read from the file.  If zero (or
            blank), a value of 1.0 is used.  Harmonic velocities or
            accelerations may be calculated from the displacement results from
            a modal (``ANTYPE,MODAL``) or harmonic (``ANTYPE,HARMIC``) analyses.  If
            ``FACT = VELO``, the harmonic velocities (v) are calculated from the
            displacements (d) at a particular frequency (f) according to the
            relationship v = 2 πfd.  Similarly, if ``FACT = ACEL``, the harmonic
            accelerations (a) are calculated as a = (2 πf)2d.

        kimg
            Used only with results from complex analyses:

            0
              Store real part of complex solution

            1
              Store imaginary part.

        time
            Time-point identifying the data set to be read.  For harmonic
            analyses, time corresponds to the frequency.  For the buckling
            analysis, time corresponds to the load factor.  Used only in the
            following cases:  If Lstep is ``NEAR``, read the data set nearest to
            ``TIME``.   If both Lstep and ``SBSTEP`` are zero (or blank), read data set
            at time = ``TIME``.  If ``TIME`` is between two solution time points on the
            results file, a linear interpolation is done between the two data
            sets.  Solution items not written to the results file [OUTRES] for
            either data set will result in a null item after data set
            interpolation.  If ``TIME`` is beyond the last time point on the file,
            use the last time point.

        angle
            Circumferential location (0.0 to 360°).  Defines the
            circumferential location for the harmonic calculations used when
            reading from the results file.  The harmonic factor (based on the
            circumferential angle) is applied to the harmonic elements
            (``PLANE25``, ``PLANE75``, ``PLANE78``, ``PLANE83``, and ``SHELL61``) of the load case.
            See the Mechanical APDL Theory Reference for details.  Note that
            factored values of applied constraints and loads will overwrite any
            values existing in the database.

        nset
            Data set number of the data set to be read.  If a positive value
            for ``NSET`` is entered, ``Lstep``, ``SBSTEP``, ``KIMG``, and ``TIME`` are ignored.
            Available set numbers can be determined by ``*SET,LIST``.

        Notes
        -----
        Reads a data set from the results file into the database for the
        selected portions of the model only.  Data that has not been specified
        for retrieval from the results file by the ``INRES`` command will be listed
        as having a zero value.  Each time that the ``SUBSET`` command is issued,
        the data currently in the database will be overwritten with a new set
        of data.  Various operations may also be performed during the read
        operation.  The database must have the model geometry available (or
        used the RESUME command before the ``SUBSET`` command to restore the
        geometry from ``File.DB``).
        """
        command = f"SUBSET,{lstep},{sbstep},{fact},{kimg},{time},{angle},{nset}"
        return self.run(command, **kwargs)
