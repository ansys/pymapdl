class WorkingPlane:
    def kwpave(
        self,
        p1="",
        p2="",
        p3="",
        p4="",
        p5="",
        p6="",
        p7="",
        p8="",
        p9="",
        **kwargs,
    ):
        """Moves the working plane origin to the average location of keypoints.

        APDL Command: KWPAVE

        Parameters
        ----------
        p1, p2, p3, . . . , p9
            Keypoints used in calculation of the average.  At least one must be
            defined.  If P1 = P, graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI).

        Notes
        -----
        Moves the origin of the working plane to the average of the specified
        keypoints.  Averaging is based on the active coordinate system.

        This command is valid in any processor.
        """
        command = f"KWPAVE,{p1},{p2},{p3},{p4},{p5},{p6},{p7},{p8},{p9}"
        return self.run(command, **kwargs)

    def kwplan(self, wn="", korig="", kxax="", kplan="", **kwargs):
        """Defines the working plane using three keypoints.

        APDL Command: KWPLAN

        Parameters
        ----------
        wn
            Window number whose viewing direction will be modified to be normal
            to the working plane (defaults to 1).  If WN is a negative value,
            the viewing direction will not be modified.  If fewer than three
            points are used, the viewing direction of window WN will be used
            instead to define the normal to the working plane.

        korig
            Keypoint number defining the origin of the working plane coordinate
            system.  If KORIG = P, graphical picking is enabled and all
            remaining command fields are ignored (valid only in the GUI).

        kxax
            Keypoint number defining the x-axis orientation (defaults to the
            x-axis being parallel to the global X-axis; or if the normal to the
            working plane is parallel to the global X-axis, then defaults to
            being parallel to the global Y-axis).

        kplan
            Keypoint number defining the working plane (the normal defaults to
            the present display view [/VIEW] of window WN).

        Notes
        -----
        Defines a working plane to assist in picking operations using three
        keypoints as an alternate to the WPLANE command.  The three keypoints
        also define the working plane coordinate system.  A minimum of one
        keypoint (at the working plane origin) is required.  Immediate mode may
        also be active.  See WPSTYL command to set the style of working plane
        display.

        This command is valid in any processor.
        """
        command = f"KWPLAN,{wn},{korig},{kxax},{kplan}"
        return self.run(command, **kwargs)

    def lwplan(self, wn="", nl1="", ratio="", **kwargs):
        """Defines the working plane normal to a location on a line.

        APDL Command: LWPLAN

        Parameters
        ----------
        wn
            Window number whose viewing direction will be modified to be normal
            to the working plane (defaults to 1).  If WN is a negative value,
            the viewing direction will not be modified.

        nl1
            Number of line to be used.  If NL1 = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in
            the GUI).

        ratio
            Location on NL1, specified as a ratio of the line length.  Must be
            between 0.0 and 1.0.  If RATIO = P, use graphical picking to
            specify location on the line.

        Notes
        -----
        Defines a working plane (to assist in picking operations) normal to a
        location on a line.  See WPSTYL command to set the style of working
        plane display.

        This command is valid in any processor.
        """
        command = f"LWPLAN,{wn},{nl1},{ratio}"
        return self.run(command, **kwargs)

    def nwpave(
        self,
        n1="",
        n2="",
        n3="",
        n4="",
        n5="",
        n6="",
        n7="",
        n8="",
        n9="",
        **kwargs,
    ):
        """Moves the working plane origin to the average location of nodes.

        APDL Command: NWPAVE

        Parameters
        ----------
        n1, n2, n3, . . . , n9
            Nodes used in calculation of the average.  At least one must be
            defined.  If N1 = P, graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI).

        Notes
        -----
        Averaging is based on the active coordinate system.

        This command is valid in any processor.
        """
        command = f"NWPAVE,{n1},{n2},{n3},{n4},{n5},{n6},{n7},{n8},{n9}"
        return self.run(command, **kwargs)

    def nwplan(self, wn="", norig="", nxax="", nplan="", **kwargs):
        """Defines the working plane using three nodes.

        APDL Command: NWPLAN

        Parameters
        ----------
        wn
            Window number whose viewing direction will be modified to be normal
            to the working plane (defaults to 1).  If WN is a negative value,
            the viewing direction will not be modified.  If fewer than three
            points are used, the viewing direction of window WN will be used
            instead to define the normal to the working plane.

        norig
            Node number defining the origin of the working plane coordinate
            system.  If NORIG = P, graphical picking is enabled and all
            remaining command fields are ignored (valid only in the GUI).

        nxax
            Node number defining the x-axis orientation (defaults to the x-axis
            being parallel to the global X-axis; or if the normal to the
            working plane is parallel to the global X-axis, then defaults to
            being parallel to the global Y-axis).

        nplan
            Node number defining the working plane (the normal defaults to the
            present display view [/VIEW] of window WN).

        Notes
        -----
        Defines a working plane to assist in picking operations using three
        nodes as an alternate to the WPLANE command.  The three nodes also
        define the working plane coordinate system.  A minimum of one node (at
        the working plane origin) is required.  Immediate mode may also be
        active.  See the WPSTYL command to set the style of the working plane
        display.

        This command is valid in any processor.
        """
        command = f"NWPLAN,{wn},{norig},{nxax},{nplan}"
        return self.run(command, **kwargs)

    def wpave(
        self,
        x1="",
        y1="",
        z1="",
        x2="",
        y2="",
        z2="",
        x3="",
        y3="",
        z3="",
        **kwargs,
    ):
        """Moves the working plane origin to the average of specified points.

        APDL Command: WPAVE

        Parameters
        ----------
        x1, y1, z1
            Coordinates (in the active coordinate system) of the first point.
            If X1 = P, graphical picking is enabled and all remaining command
            fields are ignored (valid only in the GUI).

        x2, y2, z2
            Coordinates (in the active coordinate system) of the second point.

        x3, y3, z3
            Coordinates (in the active coordinate system) of the third point.

        Notes
        -----
        Moves the origin of the working plane to the average of the specified
        points.  A point is considered specified only if at least one of its
        coordinates is non-blank, and at least one point (1, 2, or 3) must be
        specified.  Blank coordinates of a specified point are assumed to be
        zero.  Averaging is based on the active coordinate system.

        This command is valid in any processor.
        """
        command = f"WPAVE,{x1},{y1},{z1},{x2},{y2},{z2},{x3},{y3},{z3}"
        return self.run(command, **kwargs)

    def wpcsys(self, wn="", kcn="", **kwargs):
        """Defines the working plane location based on a coordinate system.

        APDL Command: WPCSYS

        Parameters
        ----------
        wn
            Window number whose viewing direction will be modified to be normal
            to the working plane (defaults to 1).  If WN is a negative value,
            the viewing direction will not be modified.

        kcn
            Coordinate system number.  KCN may be 0,1,2 or any previously
            defined local coordinate system number (defaults to the active
            system).

        Notes
        -----
        Defines a working plane location and orientation based on an existing
        coordinate system.  If a Cartesian system is used as the basis (KCN)
        for the working plane, the working plane will also be Cartesian, in the
        X-Y plane of the base system.  If a cylindrical, spherical, or toroidal
        base system is used, the working plane will be a polar system in the
        R-θ plane of the base system.

        If working plane tracking has been activated (CSYS,WP or CSYS,4), the
        updated active coordinate system will be of a similar type, except that
        a toroidal system will be updated to a cylindrical system.  See the
        Modeling and Meshing Guide for more information on working plane
        tracking.

        This command is valid in any processor.

        Some primitive generation commands will not honor R-theta
        transformations for non-cartesian coordinate systems. Refer to the
        primitive commands table for more information.
        """
        command = f"WPCSYS,{wn},{kcn}"
        return self.run(command, **kwargs)

    def wplane(
        self,
        wn="",
        xorig="",
        yorig="",
        zorig="",
        xxax="",
        yxax="",
        zxax="",
        xplan="",
        yplan="",
        zplan="",
        **kwargs,
    ):
        """Defines a working plane to assist in picking operations.

        APDL Command: WPLANE

        Parameters
        ----------
        wn
            Window number whose viewing direction will be modified to be normal
            to the working plane (defaults to 1).  If WN is a negative value,
            the viewing direction will not be modified.  If fewer than three
            points are used, the viewing direction of window WN will be used
            instead to define the normal to the working plane.

        xorig, yorig, zorig
            Global Cartesian coordinates of the origin of the working plane
            coordinate system.

        xxax, yxax, zxax
            Global Cartesian coordinates of a point defining the x-axis
            orientation.  The x-axis aligns with the projection of the line
            from this orientation point to the origin.

        xplan, yplan, zplan
            Global Cartesian coordinates of the third point defining the
            working plane.  This point will also define the location of the
            positive XY-sector of the working plane coordinate system.

        Notes
        -----
        Defines a working plane to assist in picking operations using the
        coordinates of three noncolinear points.  The three points also define
        the working plane coordinate system.  A minimum of one point (the
        working plane origin) is required.  Immediate mode may also be active.
        See WPSTYL command to set the style of working plane display.

        This command is valid in any processor.
        """
        command = f"WPLANE,{wn},{xorig},{yorig},{zorig},{xxax},{yxax},{zxax},{xplan},{yplan},{zplan}"
        return self.run(command, **kwargs)

    def wpoffs(self, xoff="", yoff="", zoff="", **kwargs):
        """Offsets the working plane.

        APDL Command: WPOFFS

        Parameters
        ----------
        xoff, yoff, zoff
            Offset increments defined in the working plane coordinate system.
            If only ZOFF is used, the working plane will be redefined parallel
            to the present plane and offset by ZOFF.

        Notes
        -----
        Changes the origin of the working plane by translating the working
        plane along its coordinate system axes.

        This command is valid in any processor.
        """
        command = f"WPOFFS,{xoff},{yoff},{zoff}"
        return self.run(command, **kwargs)

    def wprota(self, thxy="", thyz="", thzx="", **kwargs):
        """Rotates the working plane.

        APDL Command: WPROTA

        Parameters
        ----------
        thxy
            First rotation about the working plane Z axis (positive X toward
            Y).

        thyz
            Second rotation about working plane X axis (positive Y toward Z).

        thzx
            Third rotation about working plane Y axis (positive Z toward X).

        Notes
        -----
        The specified angles (in degrees) are relative to the orientation of
        the working plane.

        This command is valid in any processor.
        """
        command = f"WPROTA,{thxy},{thyz},{thzx}"
        return self.run(command, **kwargs)

    def wpstyl(
        self,
        snap="",
        grspac="",
        grmin="",
        grmax="",
        wptol="",
        wpctyp="",
        grtype="",
        wpvis="",
        snapang="",
        **kwargs,
    ):
        """Controls the display and style of the working plane.

        APDL Command: WPSTYL

        Parameters
        ----------
        snap
            Snap increment for a locational pick (1E-6 minimum).  If -1, turn
            off snap capability.  For example, a picked location of 1.2456 with
            a snap of 0.1 gives 1.2, with 0.01 gives 1.25, with 0.001 gives
            1.246, and with 0.025 gives 1.250 (defaults to 0.05).

        grspac
            Graphical spacing between grid points.  For graphical
            representation only and not related to snap points  (defaults to
            0.1).

        grmin, grmax
            Defines the size of a square grid (if WPCTYP = 0) to be displayed
            over a portion of the working plane.  The opposite corners of the
            grid will be located at grid points nearest the working plane
            coordinates of (GRMIN,GRMIN) and (GRMAX,GRMAX).  If a polar system
            (WPCTYP = 1), GRMAX is the outside radius of grid and GRMIN is
            ignored.  If GRMIN = GRMAX, no grid will be displayed (defaults to
            -1.0 and 1.0 for GRMIN and GRMAX respectively).

        wptol
            The tolerance that an entity's location can deviate from the
            specified working plane, while still being considered on the plane.
            Used only for locational picking of vertices for polygons and
            prisms (defaults to 0.003).

        wpctyp
            Working plane coordinate system type:

            0 - Cartesian (default).  If working plane tracking is on [CSYS,4], the updated
                active coordinate system will also be Cartesian.

            1 - Polar.  If working plane tracking is on, the updated active coordinate system
                will be cylindrical.

            2 - Polar.  If working plane tracking is on, the updated active coordinate system
                will be spherical.

        grtype
            Grid type:

            0 - Grid and WP triad.

            1 - Grid only.

            2 - WP triad only (default).

        wpvis
            Grid visibility:

            0 - Do not show GRTYPE entities (grid and/or triad) (default).

            1 - Show GRTYPE entities.  Cartesian working planes will be displayed with a
                Cartesian grid, polar with a polar grid.

        snapang
            Snap angle (0--180) in degrees.  Used only if WPCTYP = 1 or 2.
            Defaults to 5 degrees.

        Notes
        -----
        Use WPSTYL,DEFA to reset the working plane to its default location and
        style.  Use WPSTYL,STAT to list the status of the working plane.  Blank
        fields will keep present settings.

        It is possible to specify SNAP and WPTOL values that will cause
        conflicts during picking operations. Check your values carefully, and
        if problems are noted, revert to the default values.

        WPSTYL with no arguments will toggle the grid on and off.  The working
        plane can be displayed in the non-GUI interactive mode only after
        issuing a /PLOPTS,WP,1 command.  See the Modeling and Meshing Guide for
        more information on working plane tracking.  See /PLOPTS command for
        control of hidden line working plane.

        This command is valid in any processor.
        """
        command = f"WPSTYL,{snap},{grspac},{grmin},{grmax},{wptol},{wpctyp},{grtype},{wpvis},{snapang}"
        return self.run(command, **kwargs)
