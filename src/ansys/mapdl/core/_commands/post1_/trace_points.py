class TracePoints:
    def pltrac(
        self,
        analopt="",
        item="",
        comp="",
        trpnum="",
        name="",
        mxloop="",
        toler="",
        option="",
        escl="",
        mscl="",
        **kwargs,
    ):
        """Displays a particle flow or charged particle trace on an element

        APDL Command: PLTRAC
        display.

        Parameters
        ----------
        analopt
            Analysis option

            FLUID - Particle trace in fluid flow (default)

            ELEC - Particle trace in electric field

            MAGN - Particle trace in magnetic field

            EMAG - Particle trace in presence of both electric and magnetic fields

        item
            Label identifying the item to be contoured.  Valid item labels are
            shown in Table 222: PLTRAC - Valid Item and Component Labels
            below.  Some items also require a component label.  If Item is
            blank, display only the path trajectory.

        comp
            Component of the item (if required).  Valid component labels are
            shown in Table 222: PLTRAC - Valid Item and Component Labels below.

        trpnum
            Trace point number for storing trajectory data for use with PATH
            logic. Defaults to 0 (no trajectory path data is stored for further
            processing with PATH logic).

        name
            Name of prefix of array variable. Defaults to TRAC. NamePOIN stores
            trajectory path points for trace point number TRPNum. If Analopt =
            ELEC, MAGN, or EMAG, two additional array parameters, NameDATA and
            NameLABL, store trajectory path data and labels for the same
            TRPNum.

        mxloop
            Maximum number of loops traced by a particle.  Defaults to 25 for
            Opt = FLUID; otherwise, defaults to 1000.

        toler
            Length tolerance used for particle trajectory geometry calculation.
            Valid only for Analopt = ELEC, MAGN, or EMAG.  If particle trace
            appears to terminate inside an element, adjusting the length
            tolerance may be necessary.  Defaults to 1.0 x 10-8.

        option
            Flow trace option:

            0 - Use the undeformed mesh for computing the flow trace.

            1 - Use the deformed mesh for computing the flow trace.

        escl
            Electric field scale factor. Setting this scale factor affects only
            the tracing, not the field solution results. A negative factor
            corresponds to the opposite vector direction. Valid only for
            Analopt = ELEC or EMAG. Defaults to 1.

        mscl
            Magnetic field scale factor. Setting this scale factor affects only
            the tracing, not the field solution results. A negative factor
            corresponds to the opposite vector direction. Valid only for
            Analopt = MAGN or EMAG. Defaults to 1.

        Notes
        -----
        For a specified item, the variation of the item is displayed along the
        particle trace as a color-contoured ribbon.  The TRPOIN command must be
        used to define a point on the trajectory path.  Multiple traces may be
        displayed simultaneously by defining multiple trace points.  Issue the
        TRPLIS command to list the current tracing points.  Issue the TRPDEL
        command to delete tracing points defined earlier.   Use the PAPUT
        command with the POIN option to retrieve the particle trajectory points
        as path points.

        The model must be 3-D for the ELEC, MAGN, and EMAG analysis options.

        Three array parameters are created at the time of the particle trace:
        TRACPOIN, TRACDATA and TRACLABL. These array parameters can be used to
        put the particle velocity and the elapsed time into path form.   The
        procedure to put the arrays into a path named PATHNAME is as follows:

        Not used if Analopt = FLUID.  If working in the GUI, use the "All
        information" option to retrieve information from all three arrays at
        once.

        If OPTION is set to 1, the deformed mesh is based on the displacement
        degrees of freedom UX, UY, and UZ, which must be available in the load
        step.

        Table: 222:: : PLTRAC - Valid Item and Component Labels

        See the Basic Analysis Guide for more information on particle flow and
        charged particle traces.  See Animation in the Basic Analysis Guide for
        information on particle trace animation.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"PLTRAC,{analopt},{item},{comp},{trpnum},{name},{mxloop},{toler},{option},{escl},{mscl}"
        return self.run(command, **kwargs)

    def trpdel(self, ntrp1="", ntrp2="", trpinc="", **kwargs):
        """Deletes particle flow or charged particle trace points.

        APDL Command: TRPDEL

        Parameters
        ----------
        ntrp1, ntrp2, trpinc
            Delete points from NTRP1 to NTRP2 (defaults to NTRP1) in steps of
            TRPINC (defaults to 1).  If NTRP1 = ALL, NTRP2 and TRPINC are
            ignored and all trace points are deleted.  If NTRP1 = P, graphical
            picking is enabled and all remaining command fields are ignored
            (valid only in the GUI).

        Notes
        -----
        Deletes particle flow or charged particle trace points defined with the
        TRPOIN command.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"TRPDEL,{ntrp1},{ntrp2},{trpinc}"
        return self.run(command, **kwargs)

    def trplis(self, ntrp1="", ntrp2="", trpinc="", opt="", **kwargs):
        """Lists the particle flow or charged particle trace points.

        APDL Command: TRPLIS

        Parameters
        ----------
        ntrp1, ntrp2, trpinc
            List points from NTRP1 to NTRP2 (defaults to NTRP1) in steps of
            TRPINC (defaults to 1).  If NTRP1 = ALL, NTRP2 and TRPINC are
            ignored and all trace points are listed.  If NTRP1 = P, graphical
            picking is enabled and all remaining command fields are ignored
            (valid only in the GUI).

        opt
            Opt = LOC lists the trace point number location (X, Y, Z). Default.

        Notes
        -----
        Lists the particle flow or charged particle trace points in the active
        display coordinate system [DSYS].  Trace points are defined with the
        TRPOIN command.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"TRPLIS,{ntrp1},{ntrp2},{trpinc},{opt}"
        return self.run(command, **kwargs)

    def trpoin(self, x="", y="", z="", vx="", vy="", vz="", chrg="", mass="", **kwargs):
        """Defines a point through which a particle flow or charged particle trace

        APDL Command: TRPOIN
        will travel.

        Parameters
        ----------
        x, y, z
            Coordinate location of the trace point (in the active coordinate
            system).  If X = P, graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI).

        vx, vy, vz
            Particle velocities in the X, Y and Z directions (in the active
            coordinate system).

        chrg
            Particle charge.

        mass
            Particle mass.

        Notes
        -----
        Defines a point through which a particle flow or charged particle trace
        [PLTRAC] will travel.  Multiple points (50 maximum) may be defined
        which will result in multiple flow traces.  Use TRPLIS to list the
        currently defined trace points and TRPDEL to delete trace points.

        The VX, VY, VZ, CHRG, and MASS arguments only apply to charged
        particles.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"TRPOIN,{x},{y},{z},{vx},{vy},{vz},{chrg},{mass}"
        return self.run(command, **kwargs)
