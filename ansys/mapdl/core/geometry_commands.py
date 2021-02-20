"""Parse the entity numbers from various MAPDL geometry commands"""

import re


numeric_const_pattern = r"""
[-+]? # optional sign
(?:
(?: \d* \. \d+ ) # .1 .12 .123 etc 9.1 etc 98.1 etc
|
(?: \d+ \.? ) # 1. 12. 123. etc 1 12 123 etc
)
# followed by optional exponent part if desired
(?: [Ee] [+-]? \d+ ) ?
"""


NUM_PATTERN = re.compile(numeric_const_pattern, re.VERBOSE)


def parse_kpoint(msg):
    if msg:
        res = re.search(r'kpoint=\s+(\d+)\s+', msg)
        if res is not None:
            return int(res.group(1))


def parse_output_areas(msg):
    """Parse create area message and return area number"""
    if msg:
        res = re.search(r"(OUTPUT AREAS =\s*)([0-9]+)", msg)
        if res is not None:
            return int(res.group(2))


def parse_a(msg):
    """Parse create area message and return area number"""
    if msg:
        res = re.search(r"(AREA NUMBER =\s*)([0-9]+)", msg)
        if res is not None:
            return int(res.group(2))


def parse_line_no(msg):
    """Parse create area message and return area number"""
    if msg:
        res = re.search(r"LINE NO[.]=\s+(\d+)", msg)
        if res is not None:
            return int(res.group(1))


def parse_v(msg):
    """Parse volume message and return volume number"""
    if msg:
        res = re.search(r"(VOLUME NUMBER =\s*)([0-9]+)", msg)
        if res is not None:
            return int(res.group(2))


def parse_output_volume_area(msg):
    """Parse create area message and return area or volume number"""
    if msg:
        res = re.search(r"OUTPUT (AREA|VOLUME|AREAS) =\s*([0-9]+)", msg)
        if res is not None:
            return int(res.group(2))


# Wrap MAPDL geometry commands
class _MapdlGeometryCommands():

    def bsplin(self, p1="", p2="", p3="", p4="", p5="", p6="", xv1="", yv1="",
               zv1="", xv6="", yv6="", zv6="", **kwargs):
        """Generate a single line from a spline fit to a series of keypoints.

        APDL Command: BSPLIN

        Parameters
        ----------
        p1, p2, p3, p4, p5, p6
            Keypoints through which a spline is fit.  At least two
            keypoints must be defined.

        XV1, YV1, ZV1
            Orientation point of an outward vector tangent to line at
            P1. Vector coordinate system has its origin at the
            keypoint. Coordinate interpretation corresponds to the
            active coordinate system type, i.e., X is R for
            cylindrical, etc. Defaults to zero curvature slope.

        XV6, YV6, ZV6
            Orientation point of an outward vector tangent to a line
            at P6 (or the last keypoint specified if fewer than six
            specified). Defaults to zero curvature slope.

        Returns
        -------
        int
            Line number of the spline generated from the spline fit.

        Examples
        --------
        Generate a spline through (0, 0, 0), (0, 1, 0) and (1, 2, 0)

        >>> k0 = mapdl.k("", 0, 0, 0)
        >>> k1 = mapdl.k("", 0, 1, 0)
        >>> k2 = mapdl.k("", 1, 2, 0)
        >>> lnum = mapdl.bsplin(k0, k1, k2)

        Notes
        -----
        One line is generated between keypoint P1 and the last keypoint
        entered.  The line will pass through each entered keypoint.  Solid
        modeling in a toroidal coordinate system is not recommended.
        """
        command = "BSPLIN,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (str(p1),
                                                                  str(p2),
                                                                  str(p3),
                                                                  str(p4),
                                                                  str(p5),
                                                                  str(p6),
                                                                  str(xv1),
                                                                  str(yv1),
                                                                  str(zv1),
                                                                  str(xv6),
                                                                  str(yv6),
                                                                  str(zv6))
        return parse_line_no(self.run(command, **kwargs))

    def k(self, npt="", x="", y="", z="", **kwargs):
        """Define a keypoint.

        APDL Command: K

        Parameters
        ----------
        npt
            Reference number for keypoint.  If zero, the lowest
            available number is assigned [NUMSTR].

        x, y, z
            Keypoint location in the active coordinate system (may be
            R, θ, Z or R, θ, Φ).  If X = P, graphical picking is
            enabled and all other fields (including NPT) are ignored
            (valid only in the GUI).

        Returns
        -------
        int
            The keypoint number of the created keypoint.

        Examples
        --------
        Create keypoint at (0, 1, 2)

        >>> knum = mapdl.k('', 0, 1, 2)
        >>> knum
        1

        Create keypoint at (10, 11, 12) while specifying the keypoint
        number.

        >>> knum = mapdl.k(5, 10, 11, 12)
        >>> knum
        5

        Notes
        -----
        Defines a keypoint in the active coordinate system [CSYS] for
        line, area, and volume descriptions.  A previously defined
        keypoint of the same number will be redefined.  Keypoints may
        be redefined only if it is not yet attached to a line or is
        not yet meshed.  Solid modeling in a toroidal system is not
        recommended.
        """
        command = "K,%s,%s,%s,%s" % (str(npt), str(x), str(y), str(z))
        msg = self.run(command, **kwargs)

        if msg:
            if not re.search(r"KEYPOINT NUMBER", msg):
                res = re.search(r"(KEYPOINT\s*)([0-9]+)", msg)
            else:
                res = re.search(r"(KEYPOINT NUMBER =\s*)([0-9]+)", msg)

            if res:
                return int(res.group(2))

    def circle(self, pcent="", rad="", paxis="", pzero="", arc="", nseg="",
               **kwargs):
        """Generates circular arc lines.

        APDL Command: CIRCLE

        Parameters
        ----------
        pcent
            Keypoint defining the center of the circle (in the plane
            of the circle).

        rad
            Radius of the circle.  If RAD is blank and PCENT = P, the
            radius is the distance from PCENT to PZERO.

        paxis
            Keypoint defining axis of circle (along with PCENT).  If
            PCENT = P and PAXIS is omitted, the axis is normal to the
            working plane.

        pzero
            Keypoint defining the plane normal to circle (along with
            PCENT and PAXIS) and the zero degree location.  Need not
            be in the plane of the circle. This value is not required
            if PAXIS is defined along the Y axis (that is, a circle in
            the XZ plane).

        arc
            Arc length (in degrees).  Positive follows right-hand rule
            about PCENT-PAXIS vector.  Defaults to 360°.

        nseg
            Number of lines around circumference (defaults to minimum
            required for 90°-maximum arcs, i.e., 4 for 360°).  Number
            of keypoints generated is NSEG for 360° or NSEG + 1 for
            less than 360°.

        Returns
        -------
        list
            List of lines of the circular arcs generated from this
            command.

        Examples
        --------
        Create a full circle containing four circular arcs.  Circle
        centered at (0, 0, 0) and generated in the XY plane.  Return
        the lines generated from the circle.

        >>> k0 = mapdl.k("", 0, 0, 0)
        >>> k1 = mapdl.k("", 0, 0, 1)
        >>> carc0 = mapdl.circle(k0, 1, k1)
        >>> carc0
        [1, 2, 3, 4]

        Notes
        -----
        Generates circular arc lines (and their corresponding
        keypoints).  Keypoints are generated at regular angular
        locations (based on a maximum spacing of 90°).  Arc lines are
        generated connecting the keypoints.  Keypoint and line numbers
        are automatically assigned, beginning with the lowest
        available values [NUMSTR].  Adjacent lines use a common
        keypoint.  Line shapes are generated as arcs, regardless of
        the active coordinate system.  Line shapes are invariant with
        coordinate system after they are generated.
        """
        command = "CIRCLE,%s,%s,%s,%s,%s,%s" % (str(pcent), str(rad), str(paxis),
                                                str(pzero), str(arc), str(nseg))
        msg = self.run(command, **kwargs)
        if msg:
            matches = re.findall(r"LINE NO.=\s*(\d*)", msg)
            if matches:
                return [int(match) for match in matches]

    def l(self, p1="", p2="", ndiv="", space="", xv1="", yv1="", zv1="",
          xv2="", yv2="", zv2="", **kwargs):
        """Define a line between two keypoints.

        APDL Command: L

        Parameters
        ----------
        p1
            Keypoint at the beginning of line.

        p2
            Keypoint at the end of line.

        ndiv
            Number of element divisions within this line.  Normally
            this field is not used; specifying divisions with LESIZE,
            etc. is recommended.

        space
            Spacing ratio.  Normally this field is not used, as
            specifying spacing ratios with the LESIZE command is
            recommended.  If positive, space is the nominal ratio of
            the last division size (at P2) to the first division size
            (at P1).  If the ratio is greater than 1, the division
            sizes increase from P1 to P2, and if less than 1, they
            decrease.  If space is negative, then ``space`` is the
            nominal ratio of the center division size to those at the
            ends.

        Returns
        -------
        int
            The line number of the created line.

        Examples
        --------
        Create a line between the two keypoints (0, 0, 0) and (1, 0, 0)

        >>> k0 = mapdl.k("", 0, 0, 0)
        >>> k1 = mapdl.k("", 1, 0, 0)
        >>> lnum = mapdl.l(k0, k1)
        >>> lnum
        1

        Notes
        -----
        Defines a line between two keypoints from P1 to P2.  The line
        shape may be generated as "straight" (in the active coordinate
        system) or curved.  The line shape is invariant with
        coordinate system after it is generated.  Note that solid
        modeling in a toroidal coordinate system is not recommended.
        A curved line is limited to 180°.  Lines may be redefined only
        if not yet attached to an area.
        """
        command = "L,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (str(p1),
                                                       str(p2),
                                                       str(ndiv),
                                                       str(space),
                                                       str(xv1),
                                                       str(yv1),
                                                       str(zv1),
                                                       str(xv2),
                                                       str(yv2),
                                                       str(zv2))
        return parse_line_no(self.run(command, **kwargs))

    def a(self, p1="", p2="", p3="", p4="", p5="", p6="", p7="", p8="", p9="",
          p10="", p11="", p12="", p13="", p14="", p15="", p16="", p17="",
          p18="", **kwargs):
        """Define an area by connecting keypoints.

        APDL Command: A

        Parameters
        ----------
        p1, p2, p3, . . . , p18
            List of keypoints defining the area (18 maximum if using keyboard
            entry).  At least 3 keypoints must be entered.  If P1 = P,
            graphical picking is enabled and all remaining arguments are
            ignored (valid only in the GUI).

        Returns
        -------
        int
            The area number of the created area.

        Examples
        --------
        Create a simple triangle in the XY plane using three keypoints.

        >>> k0 = mapdl.k("", 0, 0, 0)
        >>> k1 = mapdl.k("", 1, 0, 0)
        >>> k2 = mapdl.k("", 0, 1, 0)
        >>> a0 = mapdl.a(k0, k1, k2)
        >>> a0
        1

        Notes
        -----
        Keypoints (P1 through P18) must be input in a clockwise or
        counterclockwise order around the area.  This order also
        determines the positive normal direction of the area according
        to the right-hand rule.  Existing lines between adjacent
        keypoints will be used; missing lines are generated "straight"
        in the active coordinate system and assigned the lowest
        available numbers [NUMSTR].  If more than one line exists
        between two keypoints, the shorter one will be chosen.  If the
        area is to be defined with more than four keypoints, the
        required keypoints and lines must lie on a constant coordinate
        value in the active coordinate system (such as a plane or a
        cylinder).  Areas may be redefined only if not yet attached to
        a volume.  Solid modeling in a toroidal coordinate system is
        not recommended.
        """
        command = f"A,{p1},{p2},{p3},{p4},{p5},{p6},{p7},{p8},{p9},{p10},{p11},{p12},{p13},{p14},{p15},{p16},{p17},{p18}"
        return parse_a(self.run(command, **kwargs))

    def v(self, p1="", p2="", p3="", p4="", p5="", p6="", p7="", p8="",
          **kwargs):
        """Defines a volume through keypoints.

        APDL Command: V

        Parameters
        ----------
        p1
            Keypoint defining starting corner of volume.

        p2
            Keypoint defining second corner of volume.

        p3
            Keypoint defining third corner of volume.

        p4
            Keypoint defining fourth corner of volume.

        p5
            Keypoint defining fifth corner of volume.

        p6
            Keypoint defining sixth corner of volume.

        p7
            Keypoint defining seventh corner of volume.

        p8
            Keypoint defining eighth corner of volume.

        Examples
        --------
        Create a simple cube volume.

        >>> k0 = mapdl.k("", 0, 0, 0)
        >>> k1 = mapdl.k("", 1, 0, 0)
        >>> k2 = mapdl.k("", 1, 1, 0)
        >>> k3 = mapdl.k("", 0, 1, 0)
        >>> k4 = mapdl.k("", 0, 0, 1)
        >>> k5 = mapdl.k("", 1, 0, 1)
        >>> k6 = mapdl.k("", 1, 1, 1)
        >>> k7 = mapdl.k("", 0, 1, 1)
        >>> v0 = mapdl.v(k0, k1, k2, k3, k4, k5, k6, k7)
        >>> v0
        1

        Create a triangular prism

        >>> k0 = mapdl.k("", 0, 0, 0)
        >>> k1 = mapdl.k("", 1, 0, 0)
        >>> k2 = mapdl.k("", 1, 1, 0)
        >>> k3 = mapdl.k("", 0, 1, 0)
        >>> k4 = mapdl.k("", 0, 0, 1)
        >>> k5 = mapdl.k("", 1, 0, 1)
        >>> k6 = mapdl.k("", 1, 1, 1)
        >>> k7 = mapdl.k("", 0, 1, 1)
        >>> v1 = mapdl.v(k0, k1, k2, k2, k4, k5, k6, k6)
        >>> v1
        2

        Create a tetrahedron
        V,P1,P2,P3,P3,P5,P5,P5,P5  for a tetrahedron.

        >>> k0 = mapdl.k("", 0, 0, 0)
        >>> k1 = mapdl.k("", 1, 0, 0)
        >>> k2 = mapdl.k("", 1, 1, 0)
        >>> k3 = mapdl.k("", 0, 0, 1)
        >>> v2 = mapdl.v(k0, k1, k2, k2, k3, k3, k3, k3)
        >>> v2
        3

        Notes
        -----
        Defines a volume (and its corresponding lines and areas)
        through eight (or fewer) existing keypoints.  Keypoints must
        be input in a continuous order.  The order of the keypoints
        should be around the bottom and then the top.  Missing lines
        are generated "straight" in the active coordinate system and
        assigned the lowest available numbers [NUMSTR].  Missing areas
        are generated and assigned the lowest available numbers.

        Solid modeling in a toroidal coordinate system is not recommended.

        Certain faces may be condensed to a line or point by repeating
        keypoints.   For example, use V,P1,P2,P3,P3,P5,P6,P7,P7   for a
        triangular prism or V,P1,P2,P3,P3,P5,P5,P5,P5  for a tetrahedron.

        Using keypoints to produce partial sections in CSYS = 2 can generate
        anomalies; check the resulting volumes carefully.
        """
        command = f"V,{p1},{p2},{p3},{p4},{p5},{p6},{p7},{p8}"
        return parse_v(self.run(command, **kwargs))

    def n(self, node="", x="", y="", z="", thxy="", thyz="", thzx="",
          **kwargs):
        """Define a node.

        APDL Command: N

        Parameters
        ----------
        node
            Node number to be assigned.  A previously defined node of
            the same number will be redefined.  Defaults to the
            maximum node number used +1.

        x, y, z
            Node location in the active coordinate system (R, θ, Z for
            cylindrical, R, θ, Φ for spherical or toroidal).  If X =
            P, graphical picking is enabled and all remaining command
            fields are ignored (valid only in the GUI).

        thxy
            First rotation about nodal Z (positive X toward Y).

        thyz
            Second rotation about nodal X (positive Y toward Z).

        thzx
            Third rotation about nodal Y (positive Z toward X).

        Examples
        --------
        Create a node at (0, 1, 1)

        >>> nnum = mapdl.n("", 0, 1, 1)
        >>> nnum
        1

        Create a node at (4, 5, 1) with a node ID of 10

        >>> nnum = mapdl.n(10, 4, 5, 1)
        >>> nnum
        10

        Notes
        -----
        Defines a node in the active coordinate system [CSYS].  The
        nodal coordinate system is parallel to the global Cartesian
        system unless rotated.  Rotation angles are in degrees and
        redefine any previous rotation angles.  See the NMODIF, NANG,
        NROTAT, and NORA commands for other rotation options.
        """
        command = f"N,{node},{x},{y},{z},{thxy},{thyz},{thzx}"
        msg = self.run(command, **kwargs)
        if msg:
            res = re.search(r"(NODE\s*)([0-9]+)", msg)
            if res is not None:
                return int(res.group(2))

    def al(self, l1="", l2="", l3="", l4="", l5="", l6="", l7="", l8="", l9="",
           l10="", **kwargs):
        """Generate an area bounded by previously defined lines.

        APDL Command: AL

        Parameters
        ----------
        l1, l2, l3, . . . , l10
            List of lines defining area.  The minimum number of lines
            is 3.  The positive normal of the area is controlled by
            the direction of L1 using the right-hand rule.  A negative
            value of L1 reverses the normal direction.  If L1 = ALL,
            use all selected lines with L2 defining the normal (L3 to
            L10 are ignored and L2 defaults to the lowest numbered
            selected line).  A component name may also be substituted
            for L1.

        Returns
        -------
        result : int
            Returns the area number of the created area.

        Examples
        --------
        Create an area from four lines

        >>> k0 = mapdl.k("", 0, 0, 0)
        >>> k1 = mapdl.k("", 1, 0, 0)
        >>> k2 = mapdl.k("", 1, 1, 0)
        >>> k3 = mapdl.k("", 0, 1, 0)
        >>> l0 = mapdl.l(k0, k1)
        >>> l1 = mapdl.l(k1, k2)
        >>> l2 = mapdl.l(k2, k3)
        >>> l3 = mapdl.l(k3, k0)
        >>> anum = mapdl.al(l0, l1, l2, l3)
        >>> anum
        1

        Notes
        -----
        Lines may be input (once each) in any order and must form a
        simply connected closed curve.  If the area is defined with
        more than four lines, the lines must also lie in the same
        plane or on a constant coordinate value in the active
        coordinate system (such as a plane or a cylinder).

        Solid modeling in a toroidal coordinate system is not
        recommended.  Areas may be redefined only if not yet attached
        to a volume.

        This command is valid in any processor.
        """
        command = f"AL,{l1},{l2},{l3},{l4},{l5},{l6},{l7},{l8},{l9},{l10}"
        return parse_a(self.run(command, **kwargs))

    def blc4(self, xcorner="", ycorner="", width="", height="", depth="",
             **kwargs):
        """APDL Command: BLC4

        Creates a rectangular area or block volume by corner points.

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

        Examples
        --------
        Create a block with dimensions 1 x 2 x 10 with one corner of
        the block at (0, 0) of the current working plane.

        >>> anum = mapdl.blc4(1, 1, 1, 2, 10)
        >>> anum
        1

        Notes
        -----
        Defines a rectangular area anywhere on the working plane or a
        hexahedral volume with one face anywhere on the working plane.
        A rectangle will be defined with four keypoints and four
        lines.  A volume will be defined with eight keypoints, twelve
        lines, and six areas, with the top and bottom faces parallel
        to the working plane.  See the BLC5, RECTNG, and BLOCK
        commands for alternate ways to create rectangles and blocks.
        """
        command = f"BLC4,{xcorner},{ycorner},{width},{height},{depth}"
        return parse_output_volume_area(self.run(command, **kwargs))

    def cyl4(self, xcenter="", ycenter="", rad1="", theta1="", rad2="",
             theta2="", depth="", **kwargs):
        """Creates a circular area or cylindrical volume anywhere on
        the working plane.

        APDL Command: CYL4


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
            angle defaults to 0° and the ending angle defaults to
            360°.  See the Modeling and Meshing Guide for an
            illustration.

        depth
            The perpendicular distance (either positive or negative
            based on the working plane Z direction) from the working
            plane representing the depth of the cylinder.  If DEPTH =
            0 (default), a circular area is created on the working
            plane.

        Examples
        --------
        Create a solid cylinder with a depth of 10 at the center of
        the working plane.

        >>> vnum = mapdl.cyl4(0, 0, 1, depth=10)
        >>> vnum
        1

        Create a cylinder with an inner radius of 1.9 and an outer of
        2.0 with a height of 5 centered at the working plane.

        >>> vnum = mapdl.cyl4(0, 0, rad1=1.9, rad2=2.0, depth=10)
        2

        Notes
        -----
        Defines a circular area anywhere on the working plane or a
        cylindrical volume with one face anywhere on the working
        plane.  For a solid cylinder of 360°, the top and bottom faces
        will be circular (each area defined with four lines) and they
        will be connected with two surface areas (each spanning 180°).
        See the CYL5, PCIRC, and CYLIND commands for alternate ways to
        create circles and cylinders.

        When working with a model imported from an IGES file (DEFAULT
        import option), you must provide a value for DEPTH or the
        command will be ignored.
        """
        command = f"CYL4,{xcenter},{ycenter},{rad1},{theta1},{rad2},{theta2},{depth}"
        return parse_output_volume_area(self.run(command, **kwargs))

    def asba(self, na1="", na2="", sepo="", keep1="", keep2="", **kwargs):
        """Subtracts areas from areas.

        APDL Command: ASBA

        Parameters
        ----------
        na1
            Area (or areas, if picking is used) to be subtracted from.
            If ALL, use all selected areas.  Areas specified in this
            argument are not available for use in the NA2 argument.  A
            component name may also be substituted for NA1.

        na2
            Area (or areas, if picking is used) to subtract.  If ALL,
            use all selected areas (except those included in the NA1
            argument).  A component name may also be substituted for
            NA2.

        sepo
            Behavior if the intersection of the NA1 areas and the NA2 areas is
            a line or lines:

            (blank) - The resulting areas will share line(s) where they touch.

            SEPO - The resulting areas will have separate, but
                   coincident line(s) where they touch.

        keep1
            Specifies whether NA1 areas are to be deleted:

            (blank) - Use the setting of KEEP on the BOPTN command.

            DELETE - Delete NA1 areas after ASBA operation (override
            BOPTN command settings).

            KEEP - Keep NA1 areas after ASBA operation (override BOPTN
            command settings).

        keep2
            Specifies whether NA2 areas are to be deleted:

            (blank) - Use the setting of KEEP on the BOPTN command.

            DELETE - Delete NA2 areas after ASBA operation (override
            BOPTN command settings).

            KEEP - Keep NA2 areas after ASBA operation (override BOPTN
            command settings).

        Examples
        --------
        Subtract a 0.5 x 0.5 rectangle from a 1 x 1 rectangle.

        >>> anum0 = mapdl.blc4(0, 0, 1, 1)
        >>> anum1 = mapdl.blc4(0.25, 0.25, 0.5, 0.5)
        >>> aout = mapdl.asba(anum0, anum1)
        >>> aout
        3

        Notes
        -----
        Generates new areas by subtracting the regions common to both
        NA1 and NA2 areas (the intersection) from the NA1 areas.  The
        intersection can be an area(s) or line(s).  If the
        intersection is a line and SEPO is blank, the NA1 area is
        divided at the line and the resulting areas will be connected,
        sharing a common line where they touch.  If SEPO is set to
        SEPO, NA1 is divided into two unconnected areas with separate
        lines where they touch.  See Solid Modeling in the Modeling
        and Meshing Guide for an illustration.  See the BOPTN command
        for an explanation of the options available to Boolean
        operations.  Element attributes and solid model boundary
        conditions assigned to the original entities will not be
        transferred to the new entities generated.  ASBA,ALL,ALL will
        have no effect since all the areas (in NA1) will be
        unavailable as NA2 areas.
        """
        command = f"ASBA,{na1},{na2},{sepo},{keep1},{keep2}"
        return parse_output_volume_area(self.run(command, **kwargs))

    def kbetw(self, kp1="", kp2="", kpnew="", type="", value="", **kwargs):
        """Creates a keypoint between two existing keypoints.

        APDL Command: KBETW

        Parameters
        ----------
        kp1
            First keypoint.

        kp2
            Second keypoint.

        kpnew
            Number assigned to the new keypoint.  Defaults to the
            lowest available keypoint number.

        type
            Type of input for VALUE.

            RATIO - Value is the ratio of the distances between keypoints as follows:
                    ``(KP1-KPNEW)/(KP1-KP2)``.

            DIST - Value is the absolute distance between KP1 and
                   KPNEW (valid only if current coordinate system is
                   Cartesian).

        value
            Location of new keypoint, as defined by Type (defaults to
            0.5).  If VALUE is a ratio (Type = RATIO) and is less than
            0 or greater than 1, the keypoint is created on the
            extended line.  Similarly, if VALUE is a distance (Type =
            DIST) and is less than 0 or greater than the distance
            between KP1 and KP2, the keypoint is created on the
            extended line.

        Examples
        --------
        Create a keypoint exactly centered between two keypoints.

        >>> k0 = mapdl.k("", 0, 0, 0)
        >>> k1 = mapdl.k("", 1, 0, 0)
        >>> k2 = mapdl.kbetw(k0, k1)
        >>> k2
        3

        Notes
        -----
        Placement of the new keypoint depends on the currently active
        coordinate system [CSYS].  If the coordinate system is
        Cartesian, the keypoint will lie on a straight line between
        KP1 and KP2.  If the system is not Cartesian (e.g.,
        cylindrical, spherical, etc.), the keypoint will be located as
        if on a line (which may not be straight) created in the
        current coordinate system between KP1 and KP2.  Note that
        solid modeling in a toroidal coordinate system is not
        recommended.
        """
        command = f"KBETW,{kp1},{kp2},{kpnew},{type},{value}"
        return parse_kpoint(self.run(command, **kwargs))

    def kcenter(self, type="", val1="", val2="", val3="", val4="", kpnew="",
                **kwargs):
        """Creates a keypoint at the center of a circular arc defined
        by three locations.

        APDL Command: KCENTER

        Parameters
        ----------
        type
            Type of entity used to define the circular arc.  The
            meaning of VAL1 through VAL4 will vary depending on Type.

            KP - Arc is defined by keypoints.

            LINE - Arc is defined by locations on a line.

        val1, val2, val3, val4
            Values used to specify three locations on the arc (see table
            below).

        kpnew
            Number assigned to new keypoint.  Defaults to the lowest available
            keypoint number.

        Examples
        --------
        Create a keypoint at the center of a circle centered at (0, 0, 0)

        >>> k0 = mapdl.k("", 0, 1, 0)
        >>> k1 = mapdl.k("", 1, 0, 0)
        >>> k2 = mapdl.k("", 0, -1, 0)
        >>> k3 = mapdl.kcenter('KP', k0, k1, k2)
        >>> k3
        4

        Notes
        -----
        KCENTER should be used in the Cartesian coordinate system
        (CSYS,0) only.  This command provides three methods to define
        a keypoint at the center of three locations.  As shown below,
        the center point can be calculated based on a) three
        keypoints, b) three keypoints and a radius, or c) three
        locations on a line.  Note that for method c, if a circular
        line is specified by VAL1, VAL2 through VAL4 are not needed.
        """
        command = f"KCENTER,{type},{val1},{val2},{val3},{val4},{kpnew}"
        return parse_kpoint(self.run(command, **kwargs))

    def kdist(self, kp1="", kp2="", **kwargs):
        """Calculates and lists the distance between two keypoints.

        APDL Command: KDIST

        Parameters
        ----------
        kp1
            First keypoint in distance calculation.

        kp2
            Second keypoint in distance calculation.

        Examples
        --------
        Compute the distance between two keypoints points

        >>> kp0 = (0, 10, -3)
        >>> kp1 = (1, 5, 10)
        >>> knum0 = mapdl.k("", *kp0)
        >>> knum1 = mapdl.k("", *kp1)
        >>> dist = mapdl.kdist(knum0, knum1)
        >>> dist
        [1.0, -5.0, 13.0]

        Notes
        -----
        KDIST lists the distance between keypoints KP1 and KP2, as
        well as the current coordinate system offsets from KP1 to KP2,
        where the X, Y, and Z locations of KP1 are subtracted from the
        X, Y, and Z locations of KP2 (respectively) to determine the
        offsets.  KDIST is valid in any coordinate system except
        toroidal [CSYS,3].

        This command is valid in any processor.
        """
        msg = self.run(f"KDIST,{kp1},{kp2}", **kwargs)
        if msg:
            finds = re.findall(NUM_PATTERN, msg)[-3:]
            if len(finds) == 3:
                return [float(val) for val in finds]

    def kl(self, nl1="", ratio="", nk1="", **kwargs):
        """Generates a keypoint at a specified location on an existing line.

        APDL Command: KL

        Parameters
        ----------
        nl1
            Number of the line.  If negative, the direction of line
            (as interpreted for RATIO) is reversed.

        ratio
            Ratio of line length to locate keypoint.  Must be between
            0.0 and 1.0.  Defaults to 0.5 (divide the line in half).

        nk1
            Number to be assigned to keypoint generated at division
            location (defaults to lowest available keypoint number
            [NUMSTR]).

        Examples
        --------
        Create a keypoint on a line from (0, 0, 0) and (10, 0, 0)

        >>> kp0 = (0, 0, 0)
        >>> kp1 = (10, 0, 0)
        >>> knum0 = mapdl.k("", *kp0)
        >>> knum1 = mapdl.k("", *kp1)
        >>> lnum = mapdl.l(knum0, knum1)
        >>> lnum
        1

        """
        msg = self.run(f"KL,{nl1},{ratio},{nk1}", **kwargs)
        if msg:
            res = re.search(r'KEYPOINT\s+(\d+)\s+', msg)
            if res is not None:
                return int(res.group(1))

    def knode(self, npt="", node="", **kwargs):
        """Defines a keypoint at an existing node location.

        APDL Command: KNODE

        Parameters
        ----------
        npt
            Arbitrary reference number for keypoint.  If zero, the
            lowest available number is assigned [NUMSTR].

        node
            Node number defining global X, Y, Z keypoint location.  A
            component name may also be substituted for NODE.

        Examples
        --------
        Create a keypoint at a node at (1, 2, 3)

        >>> nnum = mapdl.n('', 1, 2, 3)
        >>> knum1 = mapdl.knode('', nnum)
        >>> knum1
        1

        """
        msg = self.run(f"KNODE,{npt},{node}", **kwargs)
        if msg:
            res = re.search(r'KEYPOINT NUMBER =\s+(\d+)', msg)
            if res is not None:
                return int(res.group(1))

    def l2ang(self, nl1="", nl2="", ang1="", ang2="", phit1="", phit2="",
              **kwargs):
        """Generates a line at an angle with two existing lines.

        APDL Command: L2ANG

        Parameters
        ----------
        nl1
            Number of the first line to be hit (touched by the end of
            the new line).  If negative, assume P1 (see below) is the
            second keypoint of the line instead of the first.

        nl2
            Number of the second line to be hit.  If negative, assume
            P3 is the second keypoint of the line instead of the
            first.

        ang1
            Angle of intersection (usually zero or 180) of generated
            line with tangent to first line.

        ang2
            Angle of intersection (usually zero or 180) of generated
            line with tangent to second line.

        phit1
            Number to be assigned to keypoint generated at hit
            location on first line (defaults to lowest available
            keypoint number [NUMSTR]).

        phit2
            Number to be assigned to keypoint generated at hit
            location on second line (defaults to lowest available
            keypoint number [NUMSTR]).

        Examples
        --------
        Create two circles and join them with a line.

        >>> k0 = mapdl.k("", 0, 0, 0)
        >>> k1 = mapdl.k("", 0, 0, 1)
        >>> k2 = mapdl.k("", 0, 0, 0.5)
        >>> carc0 = mapdl.circle(k0, 1, k1)
        >>> carc1 = mapdl.circle(k2, 1, k1)
        >>> lnum = mapdl.l2ang(carc0[0], carc1[0], 90, 90)
        >>> lnum
        9

        Notes
        -----
        Generates a straight line (PHIT1-PHIT2) at an angle (ANG1)
        with an existing line NL1 (P1-P2) and which is also at an
        angle (ANG2) with another existing line NL2 (P3-P4).  If the
        angles are zero the generated line is tangent to the two
        lines.  The PHIT1 and PHIT2 locations on the lines are
        automatically calculated.  Line P1-P2 becomes P1-PHIT1, P3-P4
        becomes P3-PHIT2, and new lines PHIT1-P2, PHIT2-P4, and
        PHIT1-PHIT2 are generated.  Line divisions are set to zero
        (use LESIZE, etc. to modify).
        """
        command = f"L2ANG,{nl1},{nl2},{ang1},{ang2},{phit1},{phit2}"
        msg = self.run(command, **kwargs)
        if msg:
            return parse_line_no(msg)

    def l2tan(self, nl1="", nl2="", **kwargs):
        """Generates a line tangent to two lines.

        APDL Command: L2TAN

        Parameters
        ----------
        nl1
            Number of the first line generated line is tangent to.  If
            negative, assume P1 (see below) is the second keypoint of
            the line instead of the first.  If NL1 = P, graphical
            picking is enabled and all remaining command fields are
            ignored (valid only in the GUI).

        nl2
            Number of the second line generated line is tangent to.
            If negative, assume P3 is the second keypoint of the line
            instead of the first.

        Examples
        --------
        Create two circular arcs and connect them with a spline.

        >>> k0 = mapdl.k("", 0, 0, 0)
        >>> k1 = mapdl.k("", 0, 0, 1)
        >>> k2 = mapdl.k("", -1.5, 1.5, 0)
        >>> k3 = mapdl.k("", -1.5, 1.5, 1)
        >>> carc0 = mapdl.circle(k0, 1, k1, arc=90)
        >>> carc1 = mapdl.circle(k2, 1, k3, arc=90)
        >>> lnum = mapdl.l2tan(1, 2)
        3

        Plot these lines

        >>> mapdl.lplot(cpos='xy')

        Notes
        -----
        Generates a line (P2-P3) tangent at point P2 to line NL1
        (P1-P2) and tangent at point P3 to line NL2 (P3-P4).
        """
        command = "L2TAN,%s,%s" % (str(nl1), str(nl2))
        return parse_line_no(self.run(command, **kwargs))
