class MiscellaneousLoads:
    def anpres(self, nfram="", delay="", ncycl="", refframe="", **kwargs):
        """Produces an animated sequence of the time-harmonic pressure variation

        APDL Command: ANPRES
        of an engine-order excitation in a cyclic harmonic analysis.

        Parameters
        ----------
        nfram
            Number of frame captures per cycle. Defaults to 3 times the number
            of sectors.

        delay
            Time delay (seconds) during animation. Defaults to 0.1 seconds.

        ncycl
            Number of animation cycles. Defaults to 5.

        refframe
            Reference frame for the model rotation.

            0 - Rotating reference frame (default). The model remains fixed in space and the
                pressure revolve around the model.

            1 - Stationary reference frame. The model rotates and the pressure locations remain
                fixed in space.

        Notes
        -----
        ANPRES invokes a macro which produces an animated sequence of the time-
        harmonic applied pressure in the case of a mode-superposition harmonic
        analysis (ANTYPE,HARMIC with CYCOPT,MSUP,ON). The engine-order
        excitation must also have been specified (CYCFREQ,EO). While pressure
        loads are not accepted as valid loading in a mode-superposition
        analysis (they must be applied in the modal analysis and the modal load
        vector applied in the mode-superposition analysis) you can apply them
        for the purposes of this animation.

        For RefFrame = 1 (stationary reference frame), the rotational velocity
        from the Linear Perturbation step, or the current OMEGA or CGOMGA
        value, is used to determine the rotation direction about the cyclic
        cylindrical axis, otherwise a positive rotation is assumed.

        You may use /HBC,,ON to hide overlapping pressure faces, and use
        /GLINE,,-1 to suppress the element outlines if desired.
        """
        command = f"ANPRES,{nfram},{delay},{ncycl},{refframe}"
        return self.run(command, **kwargs)

    def aport(
        self,
        portnum="",
        label="",
        kcn="",
        pres="",
        phase="",
        val1="",
        val2="",
        val3="",
        val4="",
        **kwargs,
    ):
        """Specifies input data for plane wave and acoustic duct ports.

        APDL Command: APORT

        Parameters
        ----------
        portnum
            Port number. This number is associated with an exterior port
            or interior port previously specified by the SF and BF family
            of commands, respectively. The number must be between 1 and
            50.

        Label

            * ``"PLAN"`` : Incident plane wave.
            * ``"RECT"`` : Rectangular duct.
            * ``"CIRC"`` : Circular duct.
            * ``"COAX"`` : Coaxial duct.
            * ``"LIST"`` : List the port settings. If PortNum = ALL, list the port settings for all defined ports.
            * ``"DELE"`` : Delete defined ports. If PortNum = ALL, delete all defined ports.

        kcn
            A previously-defined local (KCN >10) or global (KCN = 0)
            Cartesian coordinate system number used to specify the
            geometric properties of the duct. Defaults to the global
            Cartesian coordinate system (0). The local Z-direction must be
            the direction of wave propagation. The origin of the local
            coordinate system must be centered about the face of the duct
            port without considering symmetry.

        pres
            Zero-to-peak amplitude of the pressure. If blank, the port
            will appear as a matching impedance.

        phase
            Phase angle of the applied pressure in degrees. Defaults to 0.

        VAL1, VAL2, VAL3, VAL4
            Additional input. The meaning of VAL1 through VAL4 varies
            depending on the specified Label.  If ``label="PLAN"``:

            * ``"VAL1"`` : angle from positive X-axis to positive Y-axis
              in the local Cartesian coordinates (KCN).

            * ``"VAL2"`` : angle away from positive Z-axis in the local
              Cartesian coordinates (KCN).

            if ``label="RECT"``:

            * ``"VAL1"`` : Width of the rectangular duct.
            * ``"VAL2"`` : Height of the rectangular duct.
            * ``"VAL3"`` : Mode index for pressure variation along the
              width (defaults to 0).
            * ``"VAL4"`` : Mode index for pressure variation along the
              height (defaults to 0).

            if ``label="CIRC"``:

            * ``"VAL1"`` : Radius of the circular duct.
            * ``"VAL2"`` : Not used.
            * ``"VAL3"`` : Mode index for pressure variation along the
              azimuth (defaults to 0).
            * ``"VAL4"`` : Mode index for pressure variation along the
              radii (defaults to 0).

            if ``label="COAX"``:

            * ``"VAL1"`` : Inner radius of the coaxial duct.
            * ``"VAL2"`` : Outer radius of the coaxial duct.
            * ``"VAL3"`` : Mode index for pressure variation along the
              azimuth (defaults to 0).
            * ``"VAL4"`` : Mode index for pressure variation along the
              radii (defaults to 0).

        Notes
        -----
        Use the APORT command to launch a specified analytic acoustic mode
        into a guided duct.

        The low-order FLUID30 element does not support the higher modes in
        the coaxial duct ``label="COAX"``.

        For more information, see Specified Mode Excitation in an Acoustic
        Duct in the Acoustic Analysis Guide, and Analytic Port Modes in a
        Duct in the Mechanical APDL Theory Reference.
        """
        command = (
            f"APORT,{portnum},{label},{kcn},{pres},{phase},,{val1},{val2},{val3},{val4}"
        )
        return self.run(command, **kwargs)

    def asifile(
        self,
        opt="",
        fname="",
        ext="",
        oper="",
        kdim="",
        kout="",
        limit="",
        **kwargs,
    ):
        """Writes or reads one-way acoustic-structural coupling data.

        APDL Command: ASIFILE

        Parameters
        ----------
        opt
            Command behavior option:

            WRITE  - Write the structural results to the specified file.

            READ  - Read the structural results from the specified file.

        fname
            File name and directory path of a one-way acoustic-structural
            coupling data file (248 characters maximum, including the
            characters needed for the directory path). An unspecified directory
            path defaults to the working directory; in this case, you can use
            all 248 characters for the file name (defaults to jobname).

        ext
            File name extension of the one-way acoustic-structural coupling
            data file (defaults to .asi).

        oper
            Command operation:

            NOMAP  - No mapping occurs between the structural and acoustic models when reading the
                     structural results from the specified file (default).

            MAP  - Maps the results from the structural to the acoustic model. (See "Notes".)

        kdim
            Interpolation criteria. Valid only when Oper = MAP.

        kout
            Outside region results. Valid only when Oper = MAP.

        limit
            Number of nearby nodes considered for interpolation. Valid only
            when Oper = MAP.

        Notes
        -----
        The ASIFILE command writes to, or reads from, a file containing one-way
        acoustic-structural coupling data.

        Results data on the one-way coupling interface (defined by the
        SF,,FSIN) in the structural model are written to the one-way coupling
        result data file during the structural solution.

        One-way coupling results data are read into the acoustic model as the
        velocity (harmonic) or acceleration (transient) excitation during the
        sequential acoustic solution.

        If Oper = NOMAP, both structural and acoustic models must share the
        same node number on the one-way coupling interface.

        If Oper = MAP:

        The one-way coupling interface must be defined in the acoustic model
        (SF,,FSIN) such that it corresponds to the field-surface interface
        number (FSIN) in the structural model.

        The output points are correct only if they are within the boundaries
        set via the specified input points.

        Calculations for out-of-bound points require much more processing time
        than do points that are within bounds.

        For each point in the acoustic destination mesh, the command searches
        all possible triangles in the structural source mesh to find the best
        triangle containing each point, then performs a linear interpolation
        inside this triangle. For faster and more accurate results, consider
        your interpolation method and search criteria carefully (see LIMIT).

        One-way coupling excitation can be applied to multiple frequencies or
        time steps.
        """
        command = f"ASIFILE,{opt},{fname},{ext},{oper},{kdim},{kout},{limit}"
        return self.run(command, **kwargs)

    def awave(
        self,
        wavenum="",
        wavetype="",
        opt1="",
        opt2="",
        val1="",
        val2="",
        val3="",
        val4="",
        val5="",
        val6="",
        val7="",
        val8="",
        val9="",
        val10="",
        val11="",
        val12="",
        val13="",
        **kwargs,
    ):
        """Specifies input data for an acoustic incident wave.

        APDL Command: AWAVE

        Parameters
        ----------
        wavenum
            Wave number. You specify the integer number for an acoustic
            incident wave inside or outside the model.  The number must be
            between 1 and 20.

        wavetype
            Wave type:

            PLAN - Planar incident wave

            MONO - Monopole or pulsating sphere incident wave

            DIPO - Dipole incident wave

            BACK - Back enclosed loudspeaker

            BARE - Bare loudspeaker

            STATUS - Displays the status of the acoustic wave settings if Wavenum = a number between
                     1 and 20 or ALL.

            DELE - Deletes the acoustic wave settings if Wavenum = a number between 1 and 20 or
                   ALL.

        opt1
            PRES

            PRES - Pressure

            VELO - Velocity

        opt2
            EXT

            EXT - Incident wave outside the model.

            INT - Incident wave inside the model. This option is only available for pure
                  scattered pressure formulation.

        val1, val2, val3, . . . , val13
            If Wavetype = PLAN, MONO, DIPO, BACK, or BARE:

            VAL1 - Amplitude of pressure or normal velocity to the sphere surface.

            VAL2 - Phase angle of the applied pressure or velocity (in degrees). Defaults to 0
                   degrees.

        Notes
        -----
        Use the ASOL command to activate the scattered field algorithm and the
        ASCRES command for output control with the scattered field algorithm.
        Refer to Acoustics in the Mechanical APDL Theory Reference for more
        information about pure scattered field formulation.
        """
        command = f"AWAVE,{wavenum},{wavetype},{opt1},{opt2},{val1},{val2},{val3},{val4},{val5},{val6},{val7},{val8},{val9},{val10},{val11},{val12},{val13}"
        return self.run(command, **kwargs)

    def biot(self, label="", **kwargs):
        """Calculates the Biot-Savart source magnetic field intensity.

        APDL Command: BIOT

        Parameters
        ----------
        label
            Controls the Biot-Savart calculation:

            NEW - Calculate the magnetic source field intensity (Hs) from the selected set of
                  source elements to the selected set of nodes.  Overwrite any
                  existing Hs field values.

            SUM - Calculate the Hs field from the selected set of source elements to the selected
                  set of nodes.  Accumulate with any existing Hs field values.

        Notes
        -----
        Calculates the Biot-Savart source magnetic field intensity (Hs) at the
        selected nodes from the selected source elements.  The calculation is
        done at the time the BIOT command is issued.

        Source elements include primitives described by element SOURC36, and
        coupled-field elements SOLID5, LINK68, and SOLID98.  Current conduction
        elements do not have a solved-for current distribution from which to
        calculate a source field until after the first substep.  Inclusion of a
        current conduction element Hs field will require a subsequent BIOT,SUM
        command (with SOURC36 elements unselected) and a SOLVE command.

        The units of Hs are as specified by the current EMUNIT command setting.

        This command is also valid in PREP7.
        """
        command = f"BIOT,{label}"
        return self.run(command, **kwargs)

    def dfswave(
        self,
        kcn="",
        radius="",
        psdref="",
        dens="",
        sonic="",
        incang="",
        npara="",
        sampopt="",
        **kwargs,
    ):
        """Specifies the incident planar waves with random phases for a diffuse

        APDL Command: DFSWAVE
        sound field.

        Parameters
        ----------
        kcn
            Local coordinate system:

            N - Coordinate system number. Default = 0.

            DELETE - Delete defined incident diffused planar waves.

        radius
            Radius of the reference sphere on which the incident planar waves
            are distributed with equal energy. Defaults to 50 x the half-
            maximum dimension of the structural panel.

        psdref
            Reference power spectral density. Default = 1.

        dens
            Mass density of incident planar wave media. Default = 2041 kg/m3.

        sonic
            Sound speed in incident planar wave media. Default = 343.24 m/s)

        incang
            Maximum incident angle (0o <= degree <= 180o) against the positive
            z axis in the local coordinate system KCN. Default = 0o.

        npara
            Number of divisions on the reference sphere with cutting planes
            parallel to the x-y coordinate plane of the local coordinate
            system. Default = 20.

        sampopt
            Random sampling option:

            ALL - Initializes the random generator of incident planar wave phases and samples the
                  phases at each solving frequency.

            MULT - Initializes the random generator of incident planar wave phases at the first
                   frequency and samples the phases at each solving frequency.

            MONO - Initializes the random generator of incident planar wave phases and samples the
                   phases only once at first solving frequency so that the same
                   phases are used over the whole frequency range for each
                   incident planar wave.

        Notes
        -----
        Issue the DFSWAVE command to activate a diffuse sound field. (The AWAVE
        command does not activate a diffuse sound field.)

        The SURF154 surface element must be defined on the surface of the
        structural solid element for the excitation.

        The acoustic elements and the absorbing boundary condition must be
        defined in the open acoustic domain. Do not define the acoustic domain
        on the excitation side.

        The PLST command calculates the average transmission loss for multiple
        sampling phases at each frequency over the frequency range.

        The symmetry of a panel structure cannot be used to reduce the
        simulation size, as the incident plane waves have varying random phase
        angles. The z axis of the Cartesian coordinate system (KCN) must be
        consistent with the panel’s outward normal unit vector at the center of
        the panel’s sending side.
        """
        command = (
            f"DFSWAVE,{kcn},{radius},{psdref},{dens},{sonic},{incang},{npara},{sampopt}"
        )
        return self.run(command, **kwargs)

    def fluread(
        self, fname="", ext="", kdim="", kout="", limit="", listopt="", **kwargs
    ):
        """Reads one-way Fluent-to-Mechanical APDL coupling data via a .cgns file

        APDL Command: FLUREAD
        with one-side fast Fourier transformation complex pressure peak value.

        Parameters
        ----------
        --
            Reserved.

        fname
            File name and directory path of a one-way Fluent-to-Mechanical APDL
            coupling data file (248 characters maximum, including the
            characters needed for the directory path). An unspecified directory
            path defaults to the working directory; in this case, you can use
            all 248 characters for the file name. Defaults to jobname.

        ext
            File name extension of the one-way Fluent-to-Mechanical APDL
            coupling data file. Defaults to .cgns).

        kdim
            Interpolation data for mapping. A value of 0 (default) or 2 applies
            2-D interpolation (where interpolation occurs on a surface).

        kout
            Outside region results for mapping:

            0 - Use the value(s) of the nearest region point for points outside of the region.
                This behavior is the default.

            1 - Set results extrapolated outside of the region to zero.

        limit
            Number of nearby nodes considered for mapping interpolation.
            Minimum = 5. Default = 20.

        listopt
            Type of items picked:

            (blank) - No listing (default).

            SOURCE - List the node coordinates and complex pressure values on the Fluent source side
                     during the solution.

            TARGET - List the node coordinates and complex pressure values on the mapped Mechanical
                     APDL target side during the solution.

            BOTH - List the node coordinates and complex pressure values on both the Fluent source
                   side and the mapped Mechanical APDL target side during the
                   solution.

        Notes
        -----
        The FLUREAD command reads one-way Fluent-to-Mechanical APDL coupling
        data from a .cgns file. The Fluent one-side fast Fourier transformation
        (FFT) peak complex pressure values are mapped to the Mechanical APDL
        structure model during the acoustic-structural solution at each FFT
        frequency.

        The command can be used only for the model with the acoustic elements.

        To apply complex pressure to the structure model, define the SURF154
        surface element, then define the one-way coupling interface (SF,,FSIN)
        on the element.

        You can define the solving frequency range via the HARFRQ command. The
        solver selects the FFT frequencies between the beginning and ending
        frequencies. The number of substeps is determined by the number of FFT
        frequencies over the frequency range. The number of substeps defined
        via the NSUBST command is overwritten.

        For better mapping performance, consider the following:

        Calculations for out-of-bound points require much more processing time
        than do points that are within bounds.

        For each point in the structural destination mesh, the command searches
        all possible triangles in the Fluent source mesh to find the best
        triangle containing each point, then performs a linear interpolation
        inside this triangle. For faster and more accurate results, consider
        your interpolation method and search criteria carefully. (See LIMIT.)

        It is possible to apply one-way coupling excitation to multiple
        frequencies. The one-side FFT peak complex pressure values are
        necessary to do so.
        """
        command = f"FLUREAD,{fname},{ext},{kdim},{kout},{limit},{listopt}"
        return self.run(command, **kwargs)

    def ic(self, node="", lab="", value="", value2="", nend="", ninc="", **kwargs):
        """Specifies initial conditions at nodes.

        APDL Command: IC

        Parameters
        ----------
        node
            Node at which initial condition is to be specified.  If ALL, apply
            to all selected nodes (NSEL).  If NODE = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in
            the GUI). A component name may be substituted for NODE.

        lab
            Degree-of-freedom label for which the initial condition is to be
            specified.  If ALL, use all appropriate labels.

        value
            Initial value of the degree of freedom (first-order value).
            Defaults to the program default for that degree of freedom (0.0 for
            structural analysis, TUNIF for thermal analysis, etc.). Values are
            in the nodal coordinate system and in radians for rotational
            degrees of freedom.

        value2
            Second-order degree of freedom value, mainly used to specify
            initial structural velocity.  Defaults to the program default for
            that degree of freedom (0.0 for structural analysis).  Values are
            in the nodal coordinate system and in radians/time for rotational
            degrees of freedom.

        nend, ninc
            Specifies the same initial condition values at the range of nodes
            from NODE to NEND (defaults to NODE), in steps of NINC (defaults to
            1).

        Notes
        -----
        The IC command specifies initial conditions, which are the initial
        values of the specified degrees of freedom. It is valid only for a
        static analysis and full method transient analysis (TIMINT,ON and
        TRNOPT,FULL). For the transient, the initial value is specified at the
        beginning of the first load step, that is, at time = 0.0.

        Initial conditions should always be step applied (KBC,1) and not
        ramped.

        If constraints (D, DSYM, etc.) and initial conditions are applied at
        the same node, the constraint specification overrides. Exercise caution
        when specifying constraints. The degree-of-freedom values start from
        zero, or the first value given in the table when table name is
        specified. To match the nonzero initial condition value with the
        initial value for degree-of-freedom constraint, use a table for the
        degree-of-freedom constraint.

        For thermal analyses, any TUNIF specification should be applied before
        the IC command; otherwise, the TUNIF specification is ignored.  If the
        IC command is input before any TUNIF specification, use the ICDELE
        command and then reissue any TUNIF specification and then follow with
        the IC command.

        When issuing the IC command for elements SOLID278 Layered Thermal Solid
        and SOLID279 Layered Thermal Solid with through-the-thickness degrees
        of freedom (KEYOPT(3) = 2), layers are always interpolated linearly
        based on the location of the degrees of freedom.

        Define consistent initial conditions. For example, if you define an
        initial velocity at a single degree of freedom, the initial velocity at
        every other degree of freedom will be 0.0, potentially leading to
        conflicting initial conditions. In most cases, you should define
        initial conditions at every unconstrained degree of freedom in your
        model. If you define an initial condition for any degree of freedom at
        the pilot node of a rigid body (see Modeling Rigid Bodies in the
        Contact Technology Guide for the definition of rigid body), then the
        same initial condition must also be defined for the same degree of
        freedom on all other nodes of the rigid body.

        After a solution has been performed, the specified initial conditions
        are overwritten by the actual solution and are no longer available. You
        must respecify them if you want to perform a subsequent analysis. You
        may want to keep a database file saved prior to the first solution for
        subsequent reuse.

        If you use the CDWRITE command to archive your model, first-order
        values (initial displacements, temperatures, etc.) specified via the IC
        command are not written to the archive file; however, second-order
        (structural velocity) terms are written.

        This command is also valid in PREP7.
        """
        command = f"IC,{node},{lab},{value},{value2},{nend},{ninc}"
        return self.run(command, **kwargs)

    def icdele(self, **kwargs):
        """Deletes initial conditions at nodes.

        APDL Command: ICDELE

        Notes
        -----
        Deletes all initial conditions previously specified with the IC command
        at all nodes.

        This command is also valid in PREP7.
        """
        command = f"ICDELE,"
        return self.run(command, **kwargs)

    def iclist(self, node1="", node2="", ninc="", lab="", **kwargs):
        """Lists the initial conditions.

        APDL Command: ICLIST

        Parameters
        ----------
        node1, node2, ninc
            List initial conditions for nodes NODE1 to NODE2 (defaults to
            NODE1) in steps of NINC (defaults to 1).  If NODE1 = ALL (default),
            NODE2 and NINC are ignored and initial conditions for all selected
            nodes [NSEL] are listed.  If NODE1 = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in
            the GUI).  A component name may be substituted for NODE1 (NODE2 and
            NINC are ignored).

        lab
            Velocity key:

            DISP - Specification is for first order degree of freedom value (displacements,
                   temperature, etc.) (default).

            VELO - Specification is for second order degree of freedom value (velocities).

        Notes
        -----
        Lists the initial conditions specified by the IC command.  Listing
        applies to all the selected nodes [NSEL] and DOF labels.  ICLIST is not
        the same as the DLIST command.  All the initial conditions including
        the default conditions are listed for the selected nodes.

        This command is valid in any processor.
        """
        command = f"ICLIST,{node1},{node2},{ninc},{lab}"
        return self.run(command, **kwargs)

    def icrotate(
        self,
        node="",
        omega="",
        x1="",
        y1="",
        z1="",
        x2="",
        y2="",
        z2="",
        vx="",
        vy="",
        vz="",
        accel="",
        **kwargs,
    ):
        """Specifies initial velocity at nodes as a sum of rotation about an axis and translation.

        APDL Command: ICROTATE

        Parameters
        ----------
        NODE
            Node at which the initial velocity is to be specified. If ALL,
            apply to all selected nodes NSEL.  A component name may be
            input for NODE.

        OMEGA
            Scalar rotational velocity about the rotational axis.

        X1, Y1, Z1
            Coordinates (in the global Cartesian coordinate system) of the
            beginning point of the rotational axis vector.

        X2, Y2, Z2
            Coordinates (in the global Cartesian coordinate system) of the
            end point of the rotational axis vector.

        Vx
            Initial translational velocity in direction x of the nodal
            coordinate system.

        Vy
            Initial translational velocity in direction y of the nodal
            coordinate system.

        Vz
            Initial translational velocity in direction z of the nodal
            coordinate system.

        accel
            Key to initialize acceleration due to centrifugal effects:

            * ``""`` : (blank) Do not initialize acceleration (default).
            * ``"CENT"`` : Initialize acceleration due to centrifugal
              effects along with the initial velocity.

        Notes
        -----
        The ICROTATE command specifies initial velocity for all
        translational degrees of freedom of the specified nodes. The
        velocity value is a combination of velocity due to rotation about
        an axis and translation.
        """
        command = f"ICROTATE,{node},{omega},{x1},{y1},{z1},{x2},{y2},{z2},{vx},{vy},{vz},{accel}"
        return self.run(command, **kwargs)

    def mrpm(self, val1="", **kwargs):
        """Defines the revolutions per minute (RPM) for a machine rotation.

        APDL Command: MRPM

        Parameters
        ----------
        val1
            The RPM value (no default).

        Notes
        -----
        A different RPM value can be defined at each load step. The RPM
        value is used to postprocess the equivalent radiated power from
        the structural surface (the PRAS and PLAS commands) or the
        radiated sound power level (the PRFAR and PLFAR commands).
        """
        return self.run(f"MRPM,{val1}", **kwargs)

    def outpr(self, item="", freq="", cname="", **kwargs):
        """Controls the solution printout.

        APDL Command: OUTPR

        Parameters
        ----------
        item
            Item for print control:

            BASIC - Basic quantities (nodal DOF solution, nodal reaction loads, and element
                    solution) (default).

            NSOL - Nodal DOF solution.

            RSOL - Nodal reaction loads.

            ESOL - Element solution.

            NLOAD - Element nodal loads. When nonlinear stabilization is active, the stabilization
                    force/moments are also printed.

            SFOR - Stabilization force/moment at the applicable nodes (valid only when nonlinear
                   stabilization is active).

            VENG - Element energies. When nonlinear stabilization is active, the energy
                   dissipation due to stabilization is also printed.

            V - Nodal velocity (applicable to structural transient analysis  only
                (ANTYPE,TRANS)).

            A - Nodal acceleration (applicable to structural transient analysis only
                (ANTYPE,TRANS)).

            ALL - All of the above solution items.

        freq
            Print solution for this item every Freqth (and the last) substep of
            each load step.  If -n, print up to n equally spaced solutions
            (only applies to static or full transient analyses when automatic
            time stepping is enabled).  If NONE, suppress all printout for this
            item for this load step.  If ALL, print solution for this item for
            every substep.  If LAST, print solution for this item only for the
            last substep of each load step.  For a modal analysis, use NONE or
            ALL.

        cname
            Name of the component, created with the CM command, defining the
            selected set of nodes or elements for which this specification is
            active.  If blank, the set is all entities.

        Notes
        -----
        Controls the solution items to be printed, the frequency with which
        they are printed (in static, transient, or full harmonic analyses), and
        the set of nodes or elements to which this specification applies (in
        static, transient, or full harmonic analyses).  An item is associated
        with either a node (NSOL, RFORCE, V, and A items) or an element (all of
        the remaining items).  The specifications are processed in the order
        that they are input.  Up to 50 specifications (OUTPR and  OUTRES
        commands combined) may be defined.  Use OUTPR,STAT to list the current
        specifications and use OUTPR,ERASE to erase all the current
        specifications.

        As described above, OUTPR writes some or all items (depending on
        analysis type) for all elements.  To restrict the solution printout,
        use OUTPR to selectively suppress (Freq = NONE) the writing of solution
        data, or first suppress the writing of all solution data
        (OUTPR,ALL,NONE) and then selectively turn on the writing of solution
        data with subsequent OUTPR commands.

        If the generalized plane strain feature is active and OUTPR is issued,
        the change of fiber length at the ending point during deformation and
        the rotation of the ending plane about X and Y during deformation will
        be printed if any displacement at the nodes is printed. The reaction
        forces at the ending point will be printed if any reaction force at the
        nodes is printed.

        Nodal reaction loads (Item = RSOL) are processed according to the
        specifications listed for the PRRSOL command.

        Result printouts for interactive sessions are suppressed for models
        with more than 10 elements.

        This command is also valid in PREP7.
        """
        command = f"OUTPR,{item},{freq},{cname}"
        return self.run(command, **kwargs)

    def outres(self, item="", freq="", cname="", nsvar="", dsubres="", **kwargs):
        """Controls the solution data written to the database.

        APDL Command: OUTRES

        Parameters
        ----------
        item
            Results item for database and file write control:

            ALL - All solution items except LOCI and SVAR. This behavior is the default.

            CINT - All available results generated by the CINT command

            ERASE - Resets OUTRES specifications to their default values.

            STAT - Lists the current OUTRES specifications.

            BASIC - Write only NSOL, RSOL, NLOAD, STRS, FGRAD, and FFLUX records to the results
                    file and database.

            NSOL - Nodal DOF solution.

            RSOL - Nodal reaction loads.

            V - Nodal velocity (applicable to structural full transient analysis only
                (ANTYPE,TRANS)).

            A - Nodal acceleration (applicable to structural full transient analysis only
                (ANTYPE,TRANS)).

            ESOL - Element solution (includes all items following):

            NLOAD - Element nodal, input constraint, and force loads (also used with the /POST1
                    commands PRRFOR, NFORCE, and FSUM to calculate reaction
                    loads).

            STRS - Element nodal stresses.

            EPEL - Element elastic strains.

            EPTH - Element thermal, initial, and swelling strains.

            EPPL - Element plastic strains.

            EPCR - Element creep strains.

            EPDI - Element diffusion strains.

            FGRAD - Element nodal gradients.

            FFLUX - Element nodal fluxes.

            LOCI - Integration point locations.

            SVAR - State variables (used only by UserMat).

            MISC - Element miscellaneous data (SMISC and NMISC items of the ETABLE command).

        freq
            Specifies how often (that is, at which substeps) to write the
            specified solution results item. The following values are valid:

        cname
            The name of the component, created with the CM command, defining
            the selected set of elements or nodes for which this specification
            is active.  If blank, the set is all entities.  A component name is
            not allowed with the ALL, BASIC, or RSOL items.

        --
            Reserved for future use.

        nsvar
            The number of user-defined state variables (TB,STATE) to be written
            to the results file. Valid only when Item = SVAR and user-defined
            state variables exist. The specified value cannot exceed the total
            number of state variables defined; if no value is specified, all
            user-defined state variables are written to the results file. This
            argument acts on all sets of user-defined state variables that
            exist for the model.

        dsubres
            Specifies whether to write additional results in Jobname.DSUB
            during a substructure or CMS use pass in transient or harmonic
            analysis.

            Blank - Write the nodal DOF solution in Jobname.DSUB (default).

            ALL - In addition to the nodal DOF solution, also write necessary data to compute
                  quantities using nodal velocity and nodal acceleration
                  (damping force, inertial force, kinetic energy, etc.) in the
                  subsequent expansion pass. For more information, see Step 3:
                  Expansion Pass in the Substructuring Analysis Guide.

        Notes
        -----
        The OUTRES command allows you to specify the following:

        The solution item (Item) to write to the database (and to the reduced
        displacement and results files)

        The frequency (Freq) at which the solution item is written (applicable
        to static, transient, or full harmonic analyses)

        The set of elements or nodes (Cname) to which your specification
        applies.
        """
        command = f"OUTRES,{item},{freq},{cname},{nsvar},{dsubres}"
        return self.run(command, **kwargs)

    def rescontrol(
        self,
        action="",
        ldstep="",
        frequency="",
        maxfiles="",
        maxtotalfiles="",
        filetype="",
        **kwargs,
    ):
        """Controls file writing for multiframe restarts.

        APDL Command: RESCONTROL

        Parameters
        ----------
        action
            Command action. Valid options are:

            DEFINE
                Issuing the command specifies how frequently the ``.Xnnn`` restart files are
                written for a load step (default).

            FILE_SUMMARY
                Issuing the command prints the substep and load step information for all ``.Xnnn``
                files for the current jobname in the current
                directory. If this option is specified, all other
                arguments are ignored.

            STATUS
                Issuing the command lists the current status in the tables of restart controls
                specified previously by RESCONTROL. If this option is
                specified, all other arguments are ignored.

            NORESTART
                Issuing the command cleans up some of the restart files after a Distributed
                ANSYS solution. The host process will not have the
                following files in the working directory at the end of
                the run: ``.ESAV``, ``.OSAV``, ``.Xnnn``, ```, `.LDHI``. The slave
                processes will not have the following files in the
                working directory at the end of the run: ``.ESAV``, ``.OSAV``,
                ``.Xnnn``, ``.RST`` (or ``.RTH``, etc.). Some of the restart files
                are never written, some are removed upon leaving ``/SOLU``
                (for example, upon FINISH), and some are removed upon
                exiting the program.

                This option is useful for cleaning up files written by all of the Distributed
                ANSYS processes, particularly when you know that these restart files will not
                be needed later on. If this option is specified, all other arguments are ignored.

                If this option is used in shared-memory parallel ANSYS, most of the restart
                files in the working directory are removed. It
                has the same effect as issuing ``RESCONTROL,,NONE``.

            LINEAR
                Issuing the command specifies the same actions as Action = DEFINE. However,
                this option is intended for linear static applications.
                For a linear static analysis, the restart capability is
                normally not needed. However, it is typically needed when
                a subsequent linear perturbation analysis is desired. By
                default, none of the restart files are written for a
                linear static analysis.

            DELETE
                Delete the restart control specification corresponding to the ``Ldstep`` label on a
                previous ``RESCONTROL,DEFINE`` command.

        ldstep
            Specifies how the ``.Xnnn`` files are written for the specified load
            steps. This option also affects how often the load history
            information is written to the ``.LDHI`` file.

            ALL
                Write the ``.Xnnn`` files at the same substep Frequency for all load steps; write
                the load history information to the ``.LDHI`` file for all load
                steps.

            LAST
                Write the ``.Xnnn`` files for the last load step only; write load history
                information to the ``.LDHI`` file for the last load step only.
                This option is the default for nonlinear static and full
                transient analyses. The remaining arguments are ignored.

            N
                Number that indicates how often the ``.Xnnn`` file is written.

                Input a positive number to write the ``.Xnnn`` files at the substep ``Frequency``
                indicated only for load step N.
                Other load steps will be written at the default substep frequency or at a frequency
                defined by a previous ``RESCONTROL`` specification.
                Load history information is written to the ``.LDHI`` file only for load steps N.

                Specifying a negative number (-N) to write the ``.Xnnn`` files for every Nth load step
                at the specified substep Frequency. The load
                history information is written to the ``.LDHI`` file
                every Nth load step. This option is suitable for
                restart applications in which more than a few
                hundred load steps are required. Compared to the
                ALL and positive N options, it can save disk
                space since the ``.LDHI`` file is smaller and fewer
                ``.Xnnn`` files are written.

                If Ldstep = -N, all other Ldstep options specified by ``RESCONTROL`` are
                ignored and the program follows the -N option (write load history information every Nth load step).
                If you want to change this pattern, issue ``RESCONTROL,DELETE, -N`` and then issue another
                ``RESCONTROL`` command with the desired Ldstep option.

            NONE
                No multiframe restart files (``.RDB`` [restart database file], ``.LDHI`` [load history file],
                ``.Xnnn``) are created. This option is the default for mode-superposition analyses.
                The remaining arguments are ignored.

                For nonlinear static, linear static, and full transient analyses, this option
                allows a restart to be done at the last or abort
                point using the same procedure as in ANSYS 5.5 or
                earlier (using the ``.EMAT``, ``.ESAV`` or ``.OSAV``, and ``.DB``
                files).

        frequency
            Frequency at which the ``.Xnnn`` files are written at the substep
            level.

            NONE
                Do not write any ``.Xnnn`` files for this load step.

            LAST
                Write the ``.Xnnn`` files for the last substep of the load step only (default for
                nonlinear static and full transient analyses).

            N
                If ``N`` is positive, write the ``.Xnnn`` file every Nth substep of a load step. If ``N``
                is negative, write ``N`` equally spaced ``.Xnnn`` files within a load step.

                In nonlinear static and full transient analyses, negative ``N`` is valid only when ``AUTOTS,ON``.
                In mode-superposition analyses, negative ``N`` is always valid.

        maxfiles
            Maximum number of ``.Xnnn`` files to save for Ldstep.

            \-1
                Overwrite existing ``.Xnnn`` files (default). The total maximum number of ``.Xnnn``
                files for one run is 999. If this number is reached before the analysis is complete,
                the program will reset the ``.Xnnn`` file numbering back to 1 and continue to write
                ``.Xnnn`` files; the program keeps the newest 999 restart files and overwrites the
                oldest restart files.

            0
                Do not overwrite any existing ``.Xnnn`` files. The total maximum number of ``.Xnnn``
                files for one run is 999. If this number is reached before the
                analysis is complete, the analysis continues but no longer
                writes any ``.Xnnn`` files.

            N
                Maximum number of ``.xnnn`` files to keep for each load step. When ``N.xnnn`` files have
                been written for a load step, the program overwrites the first ``.xnnn`` file of that load step
                for subsequent substeps.

                .. warning:: ``N`` must be <= 999. If a total of 999 restart files is reached before
                   the analysis is complete, the analysis continues but writes no additional ``.xnnn`` files.

        maxtotalfiles
            Total number of restart files to keep. ``Default = 999`` for ``.xnnn`` files and 99 for ``.rdnn`` files. This
            option is valid only when ``MAXFILES`` = -1 (default).
            Valid ``maxtotalfiles`` values are 1 through 999 for ``.xnnn`` files, and 1 through 99 for ``.rdnn`` files.

            When the total number of restart files written exceeds ``maxtotalfiles``, the program resets the
            ``.xnnn`` or ``.rdnn`` file numbering back to 1 and continues to write ``.xnnn`` or ``.rdnn`` files. The
            newest files are retained and the oldest files are overwritten.

            The ``maxtotalfiles`` value specified applies to all subsequent load steps. To reset it to the default,
            reissue the command with ``maxtotalfiles`` = 0 or some negative value.

            If ``maxtotalfiles`` is set to different values at different load steps, and if the value of ``maxtotalfiles``
            specified in the prior load step is larger than that of the current load step, the program can
            only overwrite the current number of maximum restart files up to the number ``maxtotalfiles``
            currently specified (which is smaller than the previous number).

            The recommended way to control the maximum number of restart files is to specify ``maxtotalfiles``
            at the first load step and not vary it in subsequent load steps. Also, ``maxtotalfiles`` is best used
            when Ldstep = -N or ALL.

        filetype
            The type of restart file to be controlled by this command. Valid only when Action = DEFINE:

            * **XNNN**: Control ``.xnnn`` files (default).
            * **RDNN**: Control ``.rdnn`` remeshing database files. Needed only for a nonlinear mesh adaptivity analysis.

        Notes
        -----

        **COMMAND DEFAULT**

        If the ``RESCONTROL`` command is not issued during a structural analysis, the ``.RDB`` and ``.LDHI`` files are
        written as described in Restarting an Analysis.

        **For nonlinear static and full transient analysis:**

        The default behavior is multiframe restart: ``RESCONTROL,DEFINE,LAST,LAST``
        The ``.xnnn`` file is written at the last substep of the last load step. An ``.rnnn`` file is also written at
        the iteration prior to the abort point of the run if a ``jobname.abt`` file was used (or the **Stop** button
        was pressed in the GUI), or if the job terminated because of a failure to reach convergence or some
        other solution error. No information at the aborted substep is saved to the ``.xnnn`` file.

        **For nonlinear mesh adaptivity analysis:**

        The default behavior for ``.rdnn`` files written is: ``RESCONTROL,DEFINE,ALL,LAST,,,,RDNN``
        The ``.rdnn`` file is written at the last remesh of every load step by default.
        The ``.rdnn`` and ``.rnnn`` files interact with each other. Generally, ``.rdnn`` file writing is superior to
        that of ``.rnnn`` file writing. For example, if no RESCONTROL,DEFINE command is issued, the default
        behavior is that both ``.rdnn`` and ``.rnnn`` files are written at the last occurrence of every load step
        (equivalent to ``RESCONTROL,DEFINE,ALL,LAST`` and ``RESCONTROL,DEFINE,ALL,LAST,,,,RDNN``)


        **NOTES**

        ``RESCONTROL`` sets up the restart parameters for a multiframe restart, enabling you to restart an analysis
        from any load step and substep for which there is an ``.xnnn`` file. You can perform a multiframe restart
        for static and transient (full or mode-superposition method) analyses only. For more information about
        multiframe restarts and descriptions of the contents of the files used, see *Restarting an Analysis* in the
        *Basic Analysis Guide*.

        **Syntax**

        Multiframe restart files are generically indicated here as ``.xnnn`` files. They correspond to .rnnn
        files for nonlinear static and full transient analyses, and ``.mnnn`` files for mode-superposition
        analyses.
        Remeshing database files are indicated as ``.rdnn`` files. This type of restart file is needed only
        after remeshing during a *nonlinear mesh adaptivity* analysis.
        When ``Action = DEFINE``, the specified Filetype determines the type of file (``.xnnn`` or
        ``.rdnn``) controlled by this command.

        **Number of Restart Files Allowed**

        The total number of restart files for any analysis cannot exceed 999 (for example, ``jobname.r001``
        to ``jobname.r999``).
        The total number of remeshing database files cannot exceed 99 (for example, ``jobname.rd01``
        to ``jobname.rd99``).

        **Considerations for Nonlinear Mesh Adaptivity Analysis**

        To control both ``.xnnn`` and ``.rdnn`` file writing (``Filetype = XNNN`` and ``Filetype = RDNN``,
        respectively), separate ``RESCONTROL`` commands are necessary.
        ``Action = NORESTART`` and ``Ldstep = NONE`` are not valid and will cause the analysis to fail.
        ``Ldstep = -N`` is not valid for controlling ``.xnnn`` files.

        **Limiting the Number of Files Saved**

        If you have many substeps for each load step and are writing ``.xnnn`` files frequently, you may
        want to set ``maxfiles`` to limit the number of ``.xnnn`` files saved, as they can fill your disk
        quickly.
        You can specify ``maxfiles`` and ``Frequency`` for individual load steps. These arguments take
        on the default value or the value defined by ``RESCONTROL,,ALL,Frequency,maxfiles`` if they
        are not explicitly defined for a specific load step.
        When ``.xnnn`` files are written over many load steps, you may want to further limit the number
        of ``.xnnn`` files by setting ``maxtotalfiles``.

        **Maximum Number of Load Steps**

        You can specify a maximum of ten load steps; that is, you can issue the ``RESCONTROL,,N``
        command a maximum of ten times. Specified load steps cannot be changed in a restart.

        **Specifying Ldstep = LAST or Ldstep = -N**

        The program accepts only one occurrence of ``RESCONTROL`` with ``Ldstep = LAST``. If you issue
        ``RESCONTROL,,LAST,Frequency,maxfiles`` multiple times, the last specification overwrites
        the previous one.
        The program accepts only one occurrence of ``RESCONTROL`` with a negative ``Ldstep`` value
        (``RESCONTROL,,N`` where ``N`` is a negative number). If you issue ``RESCONTROL`` multiple times
        with a negative ``Ldstep`` value, the last specification overwrites the previous one.

        """
        command = f"RESCONTROL, {action}, {ldstep}, {frequency}, {maxfiles}, , {maxtotalfiles}, {filetype}"
        return self.run(command, **kwargs)

    def sbclist(self, **kwargs):
        """Lists solid model boundary conditions.

        APDL Command: SBCLIST

        Notes
        -----
        Lists all solid model boundary conditions for the selected solid model
        entities.  See also DKLIST, DLLIST, DALIST, FKLIST, SFLLIST, SFALIST,
        BFLLIST, BFALIST, BFVLIST, and BFKLIST to list items separately.

        This command is valid in any processor.
        """
        command = f"SBCLIST,"
        return self.run(command, **kwargs)

    def sbctran(self, **kwargs):
        """Transfers solid model loads and boundary conditions to the FE model.

        APDL Command: SBCTRAN

        Notes
        -----
        Causes a manual transfer of solid model loads and boundary conditions
        to the finite element model.  Loads and boundary conditions on
        unselected keypoints, lines, areas, and volumes are not transferred.
        Boundary conditions and loads will not be transferred to unselected
        nodes or elements.  The SBCTRAN operation is also automatically done
        upon initiation of the solution calculations [SOLVE].

        This command is also valid in PREP7.
        """
        command = f"SBCTRAN,"
        return self.run(command, **kwargs)

    def wsprings(self, **kwargs):
        """Creates weak springs on corner nodes of a bounding box of the currently

        APDL Command: WSPRINGS
        selected elements.

        Notes
        -----
        WSPRINGS invokes a predefined ANSYS macro that is used during the
        import of loads from the ADAMS program into the ANSYS program. WSPRINGS
        creates weak springs on the corner nodes of the bounding box of the
        currently selected elements. The six nodes of the bounding box are
        attached to ground using COMBIN14 elements. The stiffness is chosen as
        a small number and can be changed by changing the real constants of the
        COMBIN14 elements. This command works only for models that have a
        geometric extension in two or three dimensions. One dimensional
        problems (pure beam in one axis) are not supported.

        For more information on how WSPRINGS is used during the transfer of
        loads from the ADAMS program to ANSYS, see Import Loads into ANSYS in
        the Substructuring Analysis Guide.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"WSPRINGS,"
        return self.run(command, **kwargs)
