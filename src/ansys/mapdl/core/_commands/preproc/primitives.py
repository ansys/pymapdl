from ansys.mapdl.core._commands import parse


class Primitives:
    def blc4(
        self, xcorner="", ycorner="", width="", height="", depth="", **kwargs
    ) -> int:
        """Creates a rectangular area or block volume by corner points.

        APDL Command: BLC4

        Defines a rectangular area anywhere on the working plane or a
        hexahedral volume with one face anywhere on the working plane.
        A rectangle will be defined with four keypoints and four
        lines.  A volume will be defined with eight keypoints, twelve
        lines, and six areas, with the top and bottom faces parallel
        to the working plane.  See the BLC5, RECTNG, and BLOCK
        commands for alternate ways to create rectangles and blocks.

        Parameters
        ----------
        xcorner, ycorner
            Working plane X and Y coordinates of one corner of the
            rectangle or block face.

        width
            The distance from XCORNER on or parallel to the working
            plane X-axis that, together with YCORNER, defines a second
            corner of the rectangle or block face.

        height
            The distance from YCORNER on or parallel to the working
            plane Y-axis that, together with XCORNER, defines a third
            corner of the rectangle or block face.

        depth
            The perpendicular distance (either positive or negative
            based on the working plane Z direction) from the working
            plane representing the depth of the block.  If DEPTH = 0
            (default), a rectangular area is created on the working
            plane.

        Returns
        -------
        int
            Volume or area number of the block or rectangle.

        Examples
        --------
        Create a block with dimensions 1 x 2 x 10 with one corner of
        the block at (0, 0) of the current working plane.

        >>> vnum = mapdl.blc4(1, 1, 1, 2, 10)
        >>> vnum
        1

        """
        command = f"BLC4,{xcorner},{ycorner},{width},{height},{depth}"
        return parse.parse_output_volume_area(self.run(command, **kwargs))

    def blc5(
        self, xcenter="", ycenter="", width="", height="", depth="", **kwargs
    ) -> int:
        """Create a rectangular area or block volume by center and corner points.

        APDL Command: BLC5

        Defines a rectangular area anywhere on the working plane or a
        hexahedral volume with one face anywhere on the working plane
        by specifying the center and corner points.  A rectangle will
        be defined with four keypoints and four lines.  A volume will
        be defined with eight keypoints, twelve lines, and six areas,
        with the top and bottom faces parallel to the working plane.
        See the ``BLC4``, ``RECTNG``, and ``BLOCK`` commands for
        alternate ways to create rectangles and blocks.

        Parameters
        ----------
        xcenter, ycenter
            Working plane X and Y coordinates of the center of the
            rectangle or block face.

        width
            The total distance on or parallel to the working plane
            X-axis defining the width of the rectangle or block face.

        height
            The total distance on or parallel to the working plane
            Y-axis defining the height of the rectangle or block face.

        depth
            The perpendicular distance (either positive or negative
            based on the working plane Z direction) from the working
            plane representing the depth of the block.  If ``depth=0``
            (default), a rectangular area is created on the working
            plane.

        Returns
        -------
        int
            Volume or area number of the block or rectangle.

        Examples
        --------
        Create a square centered at ``(0, 0)`` with a width of 0.5 and
        a height of 0.5

        >>> anum = mapdl.blc5(width=0.5, height=0.5)
        >>> anum
        1

        >>> vnum = mapdl.blc5(width=1, height=4, depth=9)
        >>> vnum
        1

        """
        command = f"BLC5,{xcenter},{ycenter},{width},{height},{depth}"
        return parse.parse_output_volume_area(self.run(command, **kwargs))

    def block(self, x1="", x2="", y1="", y2="", z1="", z2="", **kwargs):
        """Create a block volume based on working plane coordinates.

        APDL Command: BLOCK

        Defines a hexahedral volume based on the working plane.  The
        block must have a spatial volume greater than zero (i.e., this
        volume primitive command cannot be used to create a degenerate
        volume as a means of creating an area.)  The volume will be
        defined with eight keypoints, twelve lines, and six areas,
        with the top and bottom faces parallel to the working plane.
        See the ``BLC4`` and ``BLC5`` commands for alternate ways to
        create blocks.

        Parameters
        ----------
        x1, x2
            Working plane X coordinates of the block.

        y1, y2
            Working plane Y coordinates of the block.

        z1, z2
            Working plane Z coordinates of the block.

        Returns
        -------
        int
            Volume number of the block.

        Examples
        --------
        Create a block volume based on working plane coordinates with
        the size ``(1 x 2 x 3)``.

        >>> vnum = mapdl.block(0, 1, 0, 2, 1, 4)
        >>> vnum
        1

        """
        command = f"BLOCK,{x1},{x2},{y1},{y2},{z1},{z2}"
        return parse.parse_output_volume_area(self.run(command, **kwargs))

    def con4(self, xcenter="", ycenter="", rad1="", rad2="", depth="", **kwargs) -> int:
        """Create a conical volume anywhere on the working plane.

        APDL Command: CON4

        Defines a solid conical volume with either the vertex or a
        face anywhere on the working plane.  The cone must have a
        spatial volume greater than zero.  (i.e., this volume
        primitive command cannot be used to create a degenerate volume
        as a means of creating an area.)  The face or faces will be
        circular (each area defined with four lines), and they will be
        connected with two areas (each spanning 180 degrees).  See the CONE
        command for an alternate way to create cones.

        Parameters
        ----------
        xcenter, ycenter
            Working plane X and Y coordinates of the center axis of
            the cone.

        rad1, rad2
            Radii of the faces of the cone.  RAD1 defines the bottom
            face and will be located on the working plane.  RAD2
            defines the top face and is parallel to the working plane.
            A value of zero or blank for either RAD1 or RAD2 defines a
            degenerate face at the center axis (i.e., the vertex of
            the cone).  The same value for both RAD1 and RAD2 defines
            a cylinder instead of a cone.

        depth
            The perpendicular distance (either positive or negative
            based on the working plane Z direction) from the working
            plane representing the depth of the cone.  DEPTH cannot be
            zero.

        Returns
        -------
        int
            Volume number of the cone.

        Examples
        --------
        Create a cone with a bottom radius of 3 and a height of 10.

        >>> vnum = mapdl.con4(rad1=3, rad2=0, depth=10)
        >>> vnum
        1

        """
        command = f"CON4,{xcenter},{ycenter},{rad1},{rad2},{depth}"
        return parse.parse_output_volume_area(self.run(command, **kwargs))

    def cone(
        self, rbot="", rtop="", z1="", z2="", theta1="", theta2="", **kwargs
    ) -> int:
        """Create a conical volume centered about the working plane origin.

        APDL Command: CONE

        Defines a solid conical volume centered about the working
        plane origin.  The non-degenerate face (top or bottom) is
        parallel to the working plane but not necessarily coplanar
        with (i.e., "on") the working plane.  The cone must have a
        spatial volume greater than zero. (i.e., this volume primitive
        command cannot be used to create a degenerate volume as a
        means of creating an area.)

        For a cone of 360, top and bottom faces will be circular (each
        area defined with four lines), and they will be connected with
        two areas (each spanning 180 degrees).  See the ``CON4``
        command for an alternate way to create cones.

        Parameters
        ----------
        rbot, rtop
            Radii of the bottom and top faces of the cone.  A value of
            zero or blank for either RBOT or RTOP defines a degenerate
            face at the center axis (i.e., the vertex of the cone).
            The same value for both RBOT and RTOP defines a cylinder
            instead of a cone.

        z1, z2
            Working plane Z coordinates of the cone.  The smaller
            value is always associated with the bottom face.

        theta1, theta2
            Starting and ending angles (either order) of the cone.
            Used for creating a conical sector.  The sector begins at
            the algebraically smaller angle, extends in a positive
            angular direction, and ends at the larger angle.  The
            starting angle defaults to 0 degrees and the ending angle
            defaults to 360 degrees.  See the Modeling and Meshing Guide for
            an illustration.

        Returns
        -------
        int
            Volume number of the cone.

        Examples
        --------
        Create a quarter cone with a bottom radius of 3, top radius of 1 and
        a height of 10 centered at ``(0, 0)``.

        >>> vnum = mapdl.cone(rbot=5, rtop=1, z1=0, z2=10, theta1=180, theta2=90)
        >>> vnum
        1

        """
        command = f"CONE,{rbot},{rtop},{z1},{z2},{theta1},{theta2}"
        return parse.parse_output_volume_area(self.run(command, **kwargs))

    def cyl4(
        self,
        xcenter="",
        ycenter="",
        rad1="",
        theta1="",
        rad2="",
        theta2="",
        depth="",
        **kwargs,
    ) -> int:
        """Creates a circular area or cylindrical volume anywhere on
        the working plane.

        APDL Command: CYL4

        Defines a circular area anywhere on the working plane or a
        cylindrical volume with one face anywhere on the working
        plane.  For a solid cylinder of 360 degrees, the top and bottom faces
        will be circular (each area defined with four lines) and they
        will be connected with two surface areas (each spanning 180 degrees).
        See the CYL5, PCIRC, and CYLIND commands for alternate ways to
        create circles and cylinders.

        When working with a model imported from an IGES file (DEFAULT
        import option), you must provide a value for DEPTH or the
        command will be ignored.

        Parameters
        ----------
        xcenter, ycenter
            Working plane X and Y coordinates of the center of the
            circle or cylinder.

        rad1, rad2
            Inner and outer radii (either order) of the circle or
            cylinder.  A value of zero or blank for either RAD1 or
            RAD2, or the same value for both RAD1 and RAD2, defines a
            solid circle or cylinder.

        theta1, theta2
            Starting and ending angles (either order) of the circle or
            faces of the cylinder.  Used for creating a partial
            annulus or partial cylinder.  The sector begins at the
            algebraically smaller angle, extends in a positive angular
            direction, and ends at the larger angle.  The starting
            angle defaults to 0 degrees and the ending angle defaults to
            360 degrees.  See the Modeling and Meshing Guide for an
            illustration.

        depth
            The perpendicular distance (either positive or negative
            based on the working plane Z direction) from the working
            plane representing the depth of the cylinder.  If DEPTH =
            0 (default), a circular area is created on the working
            plane.

        Returns
        -------
        int
            Volume or area number of the block or rectangle.

        Examples
        --------
        Create a half arc centered at the origin with an outer radius
        of 2 and an inner radius of 1

        >>> anum = mapdl.cyl4(xcenter=0, ycenter=0, rad1=1,
                              theta1=0, rad2=2, theta2=180)
        >>> anum

        Create a solid cylinder with a depth of 10 at the center of
        the working plane.

        >>> vnum = mapdl.cyl4(0, 0, 1, depth=10)
        >>> vnum
        1

        Create a cylinder with an inner radius of 1.9 and an outer of
        2.0 with a height of 5 centered at the working plane.

        >>> vnum = mapdl.cyl4(0, 0, rad1=1.9, rad2=2.0, depth=10)
        2

        """
        command = f"CYL4,{xcenter},{ycenter},{rad1},{theta1},{rad2},{theta2},{depth}"
        return parse.parse_output_volume_area(self.run(command, **kwargs))

    def cyl5(
        self, xedge1="", yedge1="", xedge2="", yedge2="", depth="", **kwargs
    ) -> int:
        """Create a circular area or cylindrical volume by end points.

        APDL Command: CYL5

        Defines a circular area anywhere on the working plane or a
        cylindrical volume with one face anywhere on the working plane
        by specifying diameter end points.  For a solid cylinder of
        360°, the top and bottom faces will be circular (each area
        defined with four lines) and they will be connected with two
        surface areas (each spanning 180°).  See the CYL4, PCIRC, and
        CYLIND commands for alternate ways to create circles and
        cylinders.

        Parameters
        ----------
        xedge1, yedge1
            Working plane X and Y coordinates of one end of the circle
            or cylinder face.

        xedge2, yedge2
            Working plane X and Y coordinates of the other end of the
            circle or cylinder face.

        depth
            The perpendicular distance (either positive or negative
            based on the working plane Z direction) from the working
            plane representing the depth of the cylinder.  If DEPTH =
            0 (default), a circular area is created on the working
            plane.

        Returns
        -------
        int
            Volume or area number of the circular area of cylindrical
            volume.

        Examples
        --------
        Create a circular with one point of the circle at ``(1, 1)``
        and the other point at ``(2, 2)``

        >>> anum = mapdl.cyl5(xedge1=1, yedge1=1, xedge2=2, yedge2=2)
        >>> anum
        1

        Create a cylinder with one point of the circle at ``(X, Y) ==
        (1, 1)`` and the other point at ``(X, Y) == (2, 2)`` with a
        height of 3.

        >>> vnum = mapdl.cyl5(xedge1=1, yedge1=1, xedge2=2, yedge2=2, depth=5)
        >>> vnum
        1

        """
        command = f"CYL5,{xedge1},{yedge1},{xedge2},{yedge2},{depth}"
        return parse.parse_output_volume_area(self.run(command, **kwargs))

    def cylind(
        self, rad1="", rad2="", z1="", z2="", theta1="", theta2="", **kwargs
    ) -> int:
        """Create a cylindrical volume centered about the working plane origin.

        APDL Command: CYLIND

        Defines a cylindrical volume centered about the working plane
        origin.  The top and bottom faces are parallel to the working
        plane but neither face need be coplanar with (i.e., "on") the
        working plane.  The cylinder must have a spatial volume
        greater than zero. (i.e., this volume primitive command cannot
        be used to create a degenerate volume as a means of creating
        an area.)

        For a solid cylinder of 360°, the top and bottom faces will be
        circular (each area defined with four lines), and they will be
        connected with two areas (each spanning 180°.)  See the CYL4
        and CYL5 commands for alternate ways to create cylinders.

        Parameters
        ----------
        rad1, rad2
            Inner and outer radii (either order) of the cylinder.  A
            value of zero or blank for either RAD1 or RAD2, or the
            same value for both RAD1 and RAD2, defines a solid
            cylinder.

        z1, z2
            Working plane Z coordinates of the cylinder.  If either Z1
            or Z2 is zero, one of the faces of the cylinder will be
            coplanar with the working plane.

        theta1, theta2
            Starting and ending angles (either order) of the cylinder.
            Used for creating a cylindrical sector.  The sector begins
            at the algebraically smaller angle, extends in a positive
            angular direction, and ends at the larger angle.  The
            starting angle defaults to 0.0° and the ending angle
            defaults to 360.0°.  See the Modeling and Meshing Guide
            for an illustration.

        Returns
        -------
        int
            Volume number of the cylinder.

        Examples
        --------
        Create a hollow cylinder with an inner radius of 0.9 and an
        outer radius of 1.0 with a height of 5

        >>> vnum = mapdl.cylind(0.9, 1, z1=0, z2=5)
        >>> vnum
        1

        """
        command = f"CYLIND,{rad1},{rad2},{z1},{z2},{theta1},{theta2}"
        return parse.parse_output_volume_area(self.run(command, **kwargs))

    def pcirc(self, rad1="", rad2="", theta1="", theta2="", **kwargs) -> int:
        """Create a circular area centered about the working plane origin.

        APDL Command: PCIRC

        Defines a solid circular area or circular sector centered
        about the working plane origin.  For a solid circle of 360°,
        the area will be defined with four keypoints and four lines.
        See the ``cyl4`` and ``cyl5`` commands for alternate ways to
        create circles.

        Parameters
        ----------
        rad1, rad2
            Inner and outer radii (either order) of the circle.  A
            value of either zero or blank for either ``rad1`` or
            ``rad2``, or the same value for both ``rad1`` and
            ``rad2``, defines a solid circle.

        theta1, theta2
            Starting and ending angles (either order) of the circular
            area.  Used for creating a circular sector.  The sector
            begins at the algebraically smaller angle, extends in a
            positive angular direction, and ends at the larger angle.
            The starting angle defaults to 0.0° and the ending angle
            defaults to 360.0°.  See the Modeling and Meshing Guide
            for an illustration.

        Returns
        -------
        int
            Area number of the new circular area.

        Examples
        --------
        In this example a circular area with an inner radius of 0.95
        and an outer radius of 1 is created.

        >>> anum = mapdl.pcirc(0.95, 1)
        >>> anum
        1

        """
        command = f"PCIRC,{rad1},{rad2},{theta1},{theta2}"
        return parse.parse_output_volume_area(self.run(command, **kwargs))

    def poly(self, **kwargs):
        """Creates a polygonal area based on working plane coordinate pairs.

        APDL Command: POLY

        Defines a polygonal area on the working plane.  The area will be
        defined with NPT keypoints and NPT lines, where NPT (must be at least
        3) is the number of coordinate pairs defined with the PTXY command.
        See the RPOLY and RPR4 commands for other ways to create polygons.
        """
        command = f"POLY,"
        return self.run(command, **kwargs)

    def pri2(self, p51x="", z1="", z2="", **kwargs):
        """Creates a polygonal area or a prism volume by vertices (GUI).

        APDL Command: PRI2

        Creates a polygonal area or a prism volume using the vertices as input.
        This is a command generated by the Graphical User Interface (GUI) and
        will appear in the log file (Jobname.LOG) if graphical picking is used.
        This command is not intended to be typed in directly in an ANSYS
        session (although it can be included in an input file for batch input
        or for use with the /INPUT command).

        For polygons, the PRI2 command will appear in the log file as
        PRI2,P51X,0.0,0.0 preceded by FITEM commands that define the vertices
        (in global Cartesian coordinates).  For prisms, the PRI2 command will
        appear in the log file as PRI2,P51X preceded by FITEM commands that
        define the vertices and the Z-end of the prism.

        See the RPOLY, POLY, RPRISM, PRISM, and RPR4 commands for other ways to
        create polygons and prisms.
        """
        command = f"PRI2,{p51x},{z1},{z2}"
        return self.run(command, **kwargs)

    def prism(self, z1="", z2="", **kwargs):
        """Creates a prism volume based on working plane coordinate pairs.

        APDL Command: PRISM

        Defines a prism volume based on the working plane. The top and bottom
        areas will each be defined with NPT keypoints and NPT lines, where NPT
        (must be at least 3) is the number of coordinate pairs defined with
        PTXY command.  Also, a line will be defined between each point pair on
        the top and bottom face.  See the RPRISM and RPR4 commands for other
        ways to create prisms.

        Parameters
        ----------
        z1, z2
            Working plane Z coordinates of the top and bottom of the prism.

        """
        command = f"PRISM,{z1},{z2}"
        return self.run(command, **kwargs)

    def ptxy(self, x1="", y1="", x2="", y2="", x3="", y3="", x4="", y4="", **kwargs):
        """Defines coordinate pairs for use in polygons and prisms.

        APDL Command: PTXY

        Defines coordinate pairs for use in polygons and prisms [POLY, RPRISM].
        The coordinates must be in the Cartesian coordinate system.  The
        coordinate pairs must be input in a continuous order.  PTXY  may be
        repeated (up to 100 pairs) until the required pairs have been defined.
        The pairs will be saved until either the POLY or PRISM command is
        entered.  Use PTXY,STAT to list the saved coordinate pairs.  Use
        PTXY,DELE to delete all the saved coordinate pairs.  See the RPOLY,
        RPRISM, and RPR4 commands for other ways to create polygons and prisms.

        Parameters
        ----------
        x1, y1, x2, y2, x3, y3, x4, y4
            X and Y coordinate pairs on the working plane.

        """
        command = f"PTXY,{x1},{y1},{x2},{y2},{x3},{y3},{x4},{y4}"
        return self.run(command, **kwargs)

    def rectng(self, x1="", x2="", y1="", y2="", **kwargs):
        """Create a rectangular area anywhere on the working plane.

        APDL Command: RECTNG

        The area will be defined with four keypoints and four lines.
        See the ``blc4`` and ``blc5`` commands for alternate ways to
        create rectangles.

        Parameters
        ----------
        x1, x2
            Working plane X coordinates of the rectangle.

        y1, y2
            Working plane Y coordinates of the rectangle.

        """
        command = f"RECTNG,{x1},{x2},{y1},{y2}"
        return parse.parse_output_volume_area(self.run(command, **kwargs))

    def rpoly(self, nsides="", lside="", majrad="", minrad="", **kwargs):
        """Creates a regular polygonal area centered about the working plane origin.

        APDL Command: RPOLY

        Defines a regular polygonal area on the working plane.  The polygon
        will be centered about the working plane origin, with the first
        keypoint defined at : θ = 0°.  The area will be defined with NSIDES
        keypoints and NSIDES lines.  See the RPR4 and POLY commands for other
        ways to create polygons.


        Parameters
        ----------
        nsides
            Number of sides in the regular polygon.  Must be greater than 2.

        lside
            Length of each side of the regular polygon.

        majrad
            Radius of the major (or circumscribed) circle of the polygon.  Not
            used if LSIDE is input.

        minrad
            Radius of the minor (or inscribed) circle of the polygon.  Not used
            if LSIDE or MAJRAD is input.

        """
        command = f"RPOLY,{nsides},{lside},{majrad},{minrad}"
        return self.run(command, **kwargs)

    def rpr4(
        self,
        nsides="",
        xcenter="",
        ycenter="",
        radius="",
        theta="",
        depth="",
        **kwargs,
    ):
        """Creates a regular polygonal area or prism volume anywhere on the working plane.

        APDL Command: RPR4

        Defines a regular polygonal area anywhere on the working plane or prism
        volume with one face anywhere on the working plane.  The top and bottom
        faces of the prism are polygonal areas.  See the RPOLY, POLY, RPRISM,
        and PRISM commands for other ways to create polygons and prisms.

        Parameters
        ----------
        nsides
            The number of sides in the polygon or prism face.  Must be greater
            than 2.

        xcenter, ycenter
            Working plane X and Y coordinates of the center of the polygon or
            prism face.

        radius
            Distance (major radius) from the center to a vertex of the polygon
            or prism face (where the first keypoint is defined).

        theta
            Angle (in degrees) from the working plane X-axis to the vertex of
            the polygon or prism face where the first keypoint is defined.
            Used to orient the polygon or prism face.  Defaults to zero.

        depth
            The perpendicular distance (either positive or negative based on
            the working plane Z direction) from the working plane representing
            the depth of the prism.  If DEPTH = 0 (default), a polygonal area
            is created on the working plane.

        """
        command = f"RPR4,{nsides},{xcenter},{ycenter},{radius},{theta},{depth}"
        return self.run(command, **kwargs)

    def rprism(self, z1="", z2="", nsides="", lside="", majrad="", minrad="", **kwargs):
        """Creates a regular prism volume centered about the working plane origin.

        Defines a regular prism volume centered about the working plane origin.
        The prism must have a spatial volume greater than zero. (i.e., this
        volume primitive command cannot be used to create a degenerate volume
        as a means of creating an area.)  The top and bottom faces are
        polygonal areas that are parallel to the working plane but neither face
        need be coplanar with (i.e., "on") the working plane. The first
        keypoint defined for each face is at : θ = 0°.  See the RPR4 and PRISM
        commands for other ways to create prisms.

        APDL Command: RPRISM

        Parameters
        ----------
        z1, z2
            Working plane Z coordinates of the prism.

        nsides
            Number of sides in the polygon defining the top and bottom faces of
            the prism.  Must be greater than 2.

        lside
            Length of each side of the polygon defining the top and bottom
            faces of the prism.

        majrad
            Radius of the major (or circumscribed) circle of the polygon
            defining the top and bottom faces of the prism.  Not used if LSIDE
            is input.

        minrad
            Radius of the minor (or inscribed circle) of the polygon defining
            the top and bottom faces of the prism.  Not used if LSIDE or MAJRAD
            is input.

        """
        command = f"RPRISM,{z1},{z2},{nsides},{lside},{majrad},{minrad}"
        return self.run(command, **kwargs)

    def sph4(self, xcenter="", ycenter="", rad1="", rad2="", **kwargs) -> int:
        """Create a spherical volume anywhere on the working plane.

        APDL Command: SPH4

        Defines either a solid or hollow spherical volume anywhere on
        the working plane.  The sphere must have a spatial volume
        greater than zero.  (i.e., this volume primitive command
        cannot be used to create a degenerate volume as a means of
        creating an area.)  A sphere of 360° will be defined with two
        areas, each consisting of a hemisphere.  See the ``sphere``
        and ``sph5`` commands for other ways to create spheres.

        When working with a model imported from an IGES file (DEFAULT
        import option), you can create only solid spheres.  If you
        enter a value for both ``rad1`` and ``rad2`` the command is
        ignored.

        Parameters
        ----------
        xcenter, ycenter
            Working plane X and Y coordinates of the center of the
            sphere.

        rad1, rad2
            Inner and outer radii (either order) of the sphere.  A
            value of zero or blank for either ``rad1`` or ``rad2``
            defines a solid sphere.

        Returns
        -------
        int
            Volume number of the sphere.

        Examples
        --------
        This example creates a hollow sphere with an inner radius of
        0.9 and an outer radius of 1.0 centered at ``(0, 0)``

        >>> vnum = mapdl.sph4(0, 0, rad1=0.9, rad2=1.0)
        >>> vnum
        1

        """
        command = f"SPH4,{xcenter},{ycenter},{rad1},{rad2}"
        return parse.parse_output_volume_area(self.run(command, **kwargs))

    def sph5(self, xedge1="", yedge1="", xedge2="", yedge2="", **kwargs) -> int:
        """Create a spherical volume by diameter end points.

        APDL Command: SPH5

        Defines a solid spherical volume anywhere on the working plane
        by specifying diameter end points.  The sphere must have a
        spatial volume greater than zero.  (i.e., this volume
        primitive command cannot be used to create a degenerate volume
        as a means of creating an area.)  A sphere of 360° will be
        defined with two areas, each consisting of a hemisphere.  See
        the ``sphere`` and ``sph4`` commands for other ways to create
        spheres.

        Parameters
        ----------
        xedge1, yedge1
            Working plane X and Y coordinates of one edge of the sphere.

        xedge2, yedge2
            Working plane X and Y coordinates of the other edge of the
            sphere.

        Returns
        -------
        int
            Volume number of the sphere.

        Examples
        --------
        This example creates a sphere with one point at ``(1, 1)`` and
        one point at ``(2, 2)``

        >>> vnum = mapdl.sph5(xedge1=1, yedge1=1, xedge2=2, yedge2=2)
        >>> vnum
        1

        """
        command = f"SPH5,{xedge1},{yedge1},{xedge2},{yedge2}"
        return parse.parse_output_volume_area(self.run(command, **kwargs))

    def sphere(self, rad1="", rad2="", theta1="", theta2="", **kwargs) -> int:
        """Create a spherical volume centered about the working plane origin.

        APDL Command: SPHERE

        Defines either a solid or hollow sphere or spherical sector
        centered about the working plane origin.  The sphere must have
        a spatial volume greater than zero. (i.e., this volume
        primitive command cannot be used to create a degenerate volume
        as a means of creating an area.)  Inaccuracies can develop
        when the size of the object you create is much smaller than
        the relative coordinate system values (ratios near to or
        greater than 1000). If you require an exceptionally small
        sphere, create a larger object, and scale it down to the
        appropriate size.

        For a solid sphere of 360°, you define it with two areas, each
        consisting of a hemisphere.  See the ``sph4`` and ``sph5``
        commands for the other ways to create spheres.

        Parameters
        ----------
        rad1, rad2
            Inner and outer radii (either order) of the sphere.  A
            value of zero or blank for either ``rad1`` or ``rad2``
            defines a solid sphere.

        theta1, theta2
            Starting and ending angles (either order) of the sphere.
            Used for creating a spherical sector.  The sector begins
            at the algebraically smaller angle, extends in a positive
            angular direction, and ends at the larger angle.  The
            starting angle defaults to 0.0° and the ending angle
            defaults to 360.0°.  See the Modeling and Meshing Guide
            for an illustration.

        Returns
        -------
        int
            Volume number of the sphere.

        Examples
        --------
        >>> vnum = mapdl.sphere(rad1=0.95, rad2=1.0, theta1=90, theta2=270)
        >>> vnum
        1

        """
        command = f"SPHERE,{rad1},{rad2},{theta1},{theta2}"
        return parse.parse_output_volume_area(self.run(command, **kwargs))

    def torus(self, rad1="", rad2="", rad3="", theta1="", theta2="", **kwargs):
        """Create a toroidal volume.

        APDL Command: TORUS

        Defines a toroidal volume centered about the working plane
        origin.  A solid torus of 360° will be defined with four
        areas, each area spanning 180° around the major and minor
        circumference.

        Parameters
        ----------
        rad1, rad2, rad3
            Three values that define the radii of the torus.  You can
            specify the radii in any order.  The smallest of the
            values is the inner minor radius, the intermediate value
            is the outer minor radius, and the largest value is the
            major radius.  (There is one exception regarding the order
            of the radii values--if you want to create a solid torus,
            specify zero or blank for the inner minor radius, in which
            case the zero or blank must occupy either the ``rad1`` or
            ``rad2`` position.)

            At least two of the values that you specify must be
            positive values; they will be used to define the outer
            minor radius and the major radius.  See the diagram in the
            Notes section for a view of a toroidal sector showing all
            radii.

        theta1, theta2
            Starting and ending angles (either order) of the torus.
            Used for creating a toroidal sector.  The sector begins at
            the algebraically smaller angle, extends in a positive
            angular direction, and ends at the larger angle.  The
            starting angle defaults to 0° and the ending angle
            defaults to 360°.

        Returns
        -------
        int
            Volume number of the torus.


        Examples
        --------
        This example creates a torus with an inner minor radius of 1, an
        intermediate radii of 2, and a major radius of 5.  The values
        0 and 180 define the starting and ending angles of the torus.

        >>> vnum = mapdl.torus(rad1=5, rad2=1, rad3=2, theta1=0, theta2=180)
        >>> vnum
        1

        """
        command = f"TORUS,{rad1},{rad2},{rad3},{theta1},{theta2}"
        return parse.parse_output_volume_area(self.run(command, **kwargs))
