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


def parse_line_nos(msg):
    if msg:
        matches = re.findall(r"LINE NO[.]=\s*(\d*)", msg)
        if matches:
            return [int(match) for match in matches]


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
               zv1="", xv6="", yv6="", zv6="", **kwargs) -> int:
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
        Generate a spline through ``(0, 0, 0)``, ``(0, 1, 0)`` and
        ``(1, 2, 0)``

        >>> k0 = mapdl.k("", 0, 0, 0)
        >>> k1 = mapdl.k("", 0, 1, 0)
        >>> k2 = mapdl.k("", 1, 2, 0)
        >>> lnum = mapdl.bsplin(k0, k1, k2)

        Notes
        -----
        One line is generated between keypoint P1 and the last
        keypoint entered.  The line will pass through each entered
        keypoint.  Solid modeling in a toroidal coordinate system is
        not recommended.
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

    def k(self, npt="", x="", y="", z="", **kwargs) -> int:
        """Define a keypoint.

        APDL Command: K

        Parameters
        ----------
        npt
            Reference number for keypoint.  If zero, the lowest
            available number is assigned [NUMSTR].

        x, y, z
            Keypoint location in the active coordinate system (may be
            R, θ, Z or R, θ, Φ).

        Returns
        -------
        int
            The keypoint number of the generated keypoint.

        Examples
        --------
        Create keypoint at ``(0, 1, 2)``

        >>> knum = mapdl.k('', 0, 1, 2)
        >>> knum
        1

        Create keypoint at ``(10, 11, 12)`` while specifying the
        keypoint number.

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
               **kwargs) -> list:
        """Generate circular arc lines.

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
            about PCENT-PAXIS vector.  Defaults to 360 degrees.

        nseg
            Number of lines around circumference (defaults to minimum
            required for 90 degrees-maximum arcs, i.e., 4 for 360 degrees).  Number
            of keypoints generated is NSEG for 360 degrees or NSEG + 1 for
            less than 360 degrees.

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
        locations (based on a maximum spacing of 90 degrees).  Arc lines are
        generated connecting the keypoints.  Keypoint and line numbers
        are automatically assigned, beginning with the lowest
        available values [NUMSTR].  Adjacent lines use a common
        keypoint.  Line shapes are generated as arcs, regardless of
        the active coordinate system.  Line shapes are invariant with
        coordinate system after they are generated.
        """
        command = f"CIRCLE,{pcent},{rad},{paxis},{pzero},{arc},{nseg}"
        return parse_line_nos(self.run(command, **kwargs))

    def l(self, p1="", p2="", ndiv="", space="", xv1="", yv1="", zv1="",
          xv2="", yv2="", zv2="", **kwargs) -> int:
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
            The line number of the generated line.

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
        A curved line is limited to 180 degrees.  Lines may be redefined only
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
          p18="", **kwargs) -> int:
        """Define an area by connecting keypoints.

        APDL Command: A

        Parameters
        ----------
        p1, p2, p3, . . . , p18
            List of keypoints defining the area (18 maximum if using
            keyboard entry).  At least 3 keypoints must be entered.

        Returns
        -------
        int
            The area number of the generated area.

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
          **kwargs) -> int:
        """Define a volume through keypoints.

        APDL Command: V

        Parameters
        ----------
        p1 : int, optional
            Keypoint defining starting corner of volume.

        p2 : int, optional
            Keypoint defining second corner of volume.

        p3 : int, optional
            Keypoint defining third corner of volume.

        p4 : int, optional
            Keypoint defining fourth corner of volume.

        p5 : int, optional
            Keypoint defining fifth corner of volume.

        p6 : int, optional
            Keypoint defining sixth corner of volume.

        p7 : int, optional
            Keypoint defining seventh corner of volume.

        p8 : int, optional
            Keypoint defining eighth corner of volume.

        Returns
        -------
        int
            Volume number of the generated volume.

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

    def al(self, l1="", l2="", l3="", l4="", l5="", l6="", l7="", l8="", l9="",
           l10="", **kwargs) -> int:
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
        int
            Area number of the generated area.

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
             **kwargs) -> int:
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
             theta2="", depth="", **kwargs) -> int:
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

        Notes
        -----
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
        """
        command = f"CYL4,{xcenter},{ycenter},{rad1},{theta1},{rad2},{theta2},{depth}"
        return parse_output_volume_area(self.run(command, **kwargs))

    def asba(self, na1="", na2="", sepo="", keep1="", keep2="", **kwargs) -> int:
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

        Returns
        -------
        int
            Area number of the new area (if applicable)

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

    def kbetw(self, kp1="", kp2="", kpnew="", type="", value="", **kwargs) -> int:
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

        Returns
        -------
        int
            Keypoint number of the generated keypoint.

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
                **kwargs) -> int:
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

        Returns
        -------
        int
            Keypoint number of the generated keypoint.

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
        a keypoint at the center of three locations.

        Three keypoints:

                 , - ~ ~ ~ - ,
             ,(x)(VAL2)        ' , <--- imaginary circluar arc
           ,                       ,
          ,                         ,
         ,                           ,
        (x)(VAL1)     (x)(KPNEW)    (x)(VAL3)

        """
        command = f"KCENTER,{type},{val1},{val2},{val3},{val4},{kpnew}"
        return parse_kpoint(self.run(command, **kwargs))

    def kdist(self, kp1="", kp2="", **kwargs) -> list:
        """Calculates and lists the distance between two keypoints.

        APDL Command: KDIST

        Parameters
        ----------
        kp1
            First keypoint in distance calculation.

        kp2
            Second keypoint in distance calculation.

        Returns
        -------
        list
            ``[X, Y, Z]`` distance between two keypoints.

        Examples
        --------
        Compute the distance between two keypoints.

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

    def kl(self, nl1="", ratio="", nk1="", **kwargs) -> int:
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

        Returns
        -------
        int
            Keypoint number of the generated keypoint.

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

    def knode(self, npt="", node="", **kwargs) -> int:
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

        Returns
        -------
        int
            Keypoint number of the generated keypoint.

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
              **kwargs) -> int:
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

        Returns
        -------
        int
            Line number of the generated line.

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

    def l2tan(self, nl1="", nl2="", **kwargs) -> int:
        """Generates a line tangent to two lines.

        APDL Command: L2TAN

        Parameters
        ----------
        nl1
            Number of the first line generated line is tangent to.  If
            negative, assume P1 (see below) is the second keypoint of
            the line instead of the first.

        nl2
            Number of the second line generated line is tangent to.
            If negative, assume P3 is the second keypoint of the line
            instead of the first.

        Returns
        -------
        int
            Line number of the generated line.

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

    def lang(self, nl1="", p3="", ang="", phit="", locat="", **kwargs) -> int:
        """Generate a straight line at an angle with a line.

        APDL Command: LANG

        Parameters
        ----------
        nl1
            Number of the line to be hit (touched by the end of the
            new line).  If negative, assume P1 (see below) is the
            second keypoint of the line instead of the first.

        p3
            Keypoint at which generated line must end.

        ang
            Angle of intersection of generated line PHIT-P3 with
            tangent to line P1-P2 at PHIT.  If 0 (default), the
            generated line is tangent to NL1 toward end P1; if 90, the
            generated line is perpendicular to NL1.  If 180, the
            generated line is tangent to NL1 toward end P2.  ANG can
            be any value, but is adjusted to the corresponding acute
            angle with respect to LOCAT. See "Notes" for a discussion
            of accuracy.

        phit
            Number to be assigned to keypoint generated at hit
            location (defaults to lowest available keypoint number
            [NUMSTR]).

        locat
            Approximate location of PHIT in terms of the ratio of the
            distance along the line (NL1) to the length of the line.
            LOCAT can range from 0 to 1.  If LOCAT is blank, the point
            will be located with less speed and accuracy, and an
            arbitrary location may result.

        Returns
        -------
        int
            Line number of the generated line.

        Examples
        --------
        Create a line from a line from (0, 0, 0) to (1, 0, 0) to a
        keypoint at (1, 1, 1) at an angle of 60 degrees.

        >>> k0 = mapdl.k("", 0, 0, 0)
        >>> k1 = mapdl.k("", 1, 0, 0)
        >>> lnum = mapdl.l(k0, k1)
        >>> k2 = mapdl.k("", 1, 1, 0)
        >>> lnum = mapdl.lang(lnum, k2, 60)
        >>> lnum
        2

        Notes
        -----
        Generates a straight line (PHIT-P3) at an angle (ANG) with a
        line NL1 (P1-P2).  The location of PHIT on the line is
        automatically calculated.  Line P1-P2 becomes P1-PHIT and new
        lines PHIT-P2 and PHIT-P3 are generated.  Line divisions are
        set to zero (use LESIZE, etc. to modify).

        PHIT is positioned closest to LOCAT for the given angle, ANG.
        To ensure better performance, it is recommended that LOCAT be
        input, even if it is 0.

        The program uses an iterative procedure to position PHIT.  The
        procedure is not exact, with the result that the actual value
        of ANG will sometimes differ slightly from the specified
        value.
        """
        command = f"LANG,{nl1},{p3},{ang},{phit},{locat}"
        return parse_line_no(self.run(command, **kwargs))

    def larc(self, p1="", p2="", pc="", rad="", **kwargs) -> int:
        """Define a circular arc.

        APDL Command: LARC

        Parameters
        ----------
        p1
            Keypoint at one end of circular arc line.

        p2
            Keypoint at other end of circular arc line.

        pc
            Keypoint defining plane of arc and center of curvature
            side (with positive radius).  Must not lie along the
            straight line from P1 to P2.  PC need not be at the center
            of curvature.

        rad
            Radius of curvature of the arc.  If negative, assume
            center of curvature side is opposite to that defined by
            PC.  If RAD is blank, RAD will be calculated from a curve
            fit through P1, PC, and P2.

        Returns
        -------
        int
            Line number of the arc.

        Examples
        --------
        Create a circular arc that travels between (0, 0, 0) and
        (1, 1, 0) with a radius of curvature of 2.

        >>> k0 = mapdl.k("", 0, 0, 0)
        >>> k1 = mapdl.k("", 1, 1, 0)
        >>> k2 = mapdl.k("", 0, 1, 0)
        >>> lnum = mapdl.larc(k0, k1, k2, 2)
        1

        Notes
        -----
        Defines a circular arc line from P1 to P2.  The line shape is
        generated as circular, regardless of the active coordinate
        system.  The line shape is invariant with coordinate system
        after it is generated.

        When dealing with a large radius arc (1e3), or if the location
        of the arc you create is far away from the origin of your
        coordinate system, anomalies may occur. You can prevent this
        by creating the arc at a smaller scale, and then scaling the
        model back to full size (LSSCALE).
        """
        command = f"LARC,{p1},{p2},{pc},{rad}"
        return parse_line_no(self.run(command, **kwargs))

    def larea(self, p1="", p2="", narea="", **kwargs) -> int:
        """Generate the shortest line between two keypoints on an area.

        APDL Command: LAREA

        Parameters
        ----------
        p1
            First keypoint of line to be generated.

        p2
            Second keypoint of line to be generated.

        narea
            Area containing P1 and P2, or area to which generated line
            is to be parallel.

        Returns
        -------
        int
            Line number of the generated line.

        Examples
        --------
        Generate a line on a square between its two corners.

        >>> k0 = mapdl.k("", 0, 0, 0)
        >>> k1 = mapdl.k("", 1, 0, 0)
        >>> k2 = mapdl.k("", 1, 1, 0)
        >>> k3 = mapdl.k("", 0, 1, 0)
        >>> a0 = mapdl.a(k0, k1, k2, k3)
        >>> lnum = mapdl.larea(k0, k2, a0)
        >>> lnum
        1

        Notes
        -----
        Generates the shortest line between two keypoints, P1 and P2,
        both of which lie on an area.  The generated line will also
        lie on the area.  P1 and P2 may also be equidistant (in global
        Cartesian space) from the area (and on the same side of the
        area), in which case a line parallel to the area is generated.
        """
        command = f"LAREA,{p1},{p2},{narea}"
        return parse_line_no(self.run(command, **kwargs))

    def lcomb(self, nl1="", nl2="", keep="", **kwargs) -> int:
        """Combines adjacent lines into one line.

        APDL Command: LCOMB

        Parameters
        ----------
        nl1
            Number of the first line to be combined.  If NL1 = ALL,
            NL2 is ignored and all selected lines [LSEL] are combined.
            A component name may also be substituted for NL1 (NL2 is
            ignored).

        nl2
            Number of the second line to be combined.

        keep
            Specifies whether to keep the input entities:

            0 - Delete lines NL1 and NL2 and their common keypoint.
                Keypoints will not be deleted if they are meshed or if
                they are attached to other lines.  Lines will not be
                deleted if they are attached to different areas.

            1 - Keep NL1, NL2, and their common keypoint.  (The common
                keypoint will not be attached to the output line.)

        Returns
        -------
        int
            Line number of the combined line.

        Examples
        --------
        Create two lines and combine them.

        >>> k0 = mapdl.k("", 0, 0, 0)
        >>> k1 = mapdl.k("", 1, 0, 0)
        >>> k2 = mapdl.k("", 2, 0, 0)
        >>> l0 = mapdl.l(k0, k1)
        >>> l1 = mapdl.l(k0, k2)
        >>> lout = mapdl.lcomb(l0, l1)
        >>> lout
        1

        Notes
        -----
        Combines adjacent lines into one line (the output line).  This
        operation will effectively "undo" the LDIV operation.  Line
        divisions are set to zero (use LESIZE, etc. to modify).  Lines
        attached to the same area(s) can also be combined.  See also
        the LCCAT command for line concatenation capability.
        """
        command = f"LCOMB,{nl1},{nl2},{keep}"
        return parse_line_no(self.run(command, **kwargs))

    def ldiv(self, nl1="", ratio="", pdiv="", ndiv="", keep="", **kwargs) -> str:
        """Divides a single line into two or more lines.

        APDL Command: LDIV

        Parameters
        ----------
        nl1
            Number of the line to be divided.  If negative, assume P1
            (see below) is the second keypoint of the line instead of
            the first for RATIO.  If ALL, divide all selected lines
            [LSEL].  A component name may also be substituted for NL1.

        ratio
            Ratio of line length P1-PDIV to line length P1-P2.  Must
            be between 0.0 and 1.0. Input ignored if NDIV > 2.

        pdiv
            Number to be assigned to keypoint generated at division
            location (defaults to lowest available keypoint number
            [NUMSTR]).  Input ignored if NL1 = ALL or NDIV > 2.  If
            PDIV already exists and lies on line NL1, divide line at
            PDIV (RATIO must also be 0.0).  If PDIV already exists and
            does not lie on line NL1, PDIV is projected and moved to
            the nearest point on line NL1 (if possible). PDIV cannot
            be attached to another line, area, or volume.

        ndiv
            The number of new lines to be generated from old line
            (defaults to 2).

        keep
            Specifies whether to keep the input entities:

            0 - Modify old line to use new keypoints and slopes.

            1 - Do not modify old line.  New lines will overlay old
                line and have unique keypoints.

        Returns
        -------
        str
            MAPDL command output.

        Examples
        --------
        Create a single line and divide it exactly half.

        >>> k0 = mapdl.k("", 0, 0, 0)
        >>> k1 = mapdl.k("", 1, 0, 0)
        >>> l0 = mapdl.l(k0, k1)
        >>> output = mapdl.ldiv(l0, ratio=0.5)
        >>> print(output)
        DIVIDE LINE      1       RATIO=  0.50000       NEW KEYPOINT=     0
          NUMBER OF LINES DIVIDED =      1


        Create a single line and divide it into 5 pieces.

        >>> k0 = mapdl.k("", 0, 0, 0)
        >>> k1 = mapdl.k("", 1, 0, 0)
        >>> l0 = mapdl.l(k0, k1)
        >>> mapdl.ldiv(l0, ndiv=5)

        Notes
        -----
        Divides a single line NL1 (defined from keypoint P1 to
        keypoint P2) into two or more lines.  Line NL1 becomes the new
        line beginning with keypoint P1 and new lines are generated
        ending at keypoint P2.  If the line is attached to an area,
        the area will also be updated.  Line divisions are set to zero
        (use LESIZE, etc. to modify).
        """
        command = f"LDIV,{nl1},{ratio},{pdiv},{ndiv},{keep}"
        return self.run(command, **kwargs)

    def lextnd(self, nl1="", nk1="", dist="", keep="", **kwargs) -> int:
        """Extends a line at one end by using its slope.

        APDL Command: LEXTND

        Parameters
        ----------
        nl1
            Number of the line to be extended.

        nk1
            Number of keypoint at the end of line NL1 to be extended.

        dist
            Distance that the line will be extended.

        keep
            Specifies whether to keep the input entities:

            0 - Modify old line to use new keypoints and slopes.

            1 - Do not modify old line.  New line will overlay old
                line and have unique keypoints.

        Returns
        -------
        int
            Line number of the generated line.

        Examples
        --------
        Create a circular arc and extend it at one of its keypoints

        >>> k0 = mapdl.k("", 0, 0, 0)
        >>> k1 = mapdl.k("", 0, 0, 1)
        >>> carcs = mapdl.circle(k0, 1, k1, arc=90)
        >>> lnum = mapdl.lextnd(carcs[0], 3, 1)
        >>> lnum
        1

        Notes
        -----
        Extends a line at one end by using its slope.  Lines may be
        redefined only if not yet attached to an area.  Line divisions
        are set to zero (use LESIZE, etc. to modify).  Note that solid
        modeling in a toroidal coordinate system is not recommended.
        """
        command = f"LEXTND,{nl1},{nk1},{dist},{keep}"
        return parse_line_no(self.run(command, **kwargs))

    def lfillt(self, nl1="", nl2="", rad="", pcent="", **kwargs) -> int:
        """Generate a fillet line between two intersecting lines.

        APDL Command: LFILLT

        Parameters
        ----------
        nl1
            Number of the first intersecting line.

        nl2
            Number of the second intersecting line.

        rad
            Radius of fillet to be generated.  Radius should be less than the
            lengths of the two lines specified with NL1 and NL2.

        pcent
            Number to be assigned to generated keypoint at fillet arc center.
            If zero (or blank), no keypoint is generated.

        Returns
        -------
        int
            Line number of the generated line.

        Examples
        --------
        Create two intersecting lines at a right angle and add a
        fillet between them.

        >>> k0 = mapdl.k("", 0, 0, 0)
        >>> k1 = mapdl.k("", 0, 1, 0)
        >>> k2 = mapdl.k("", 1, 0, 0)
        >>> l0 = mapdl.l(k0, k1)
        >>> l1 = mapdl.l(k0, k2)
        >>> lnum = mapdl.lfillt(l0, l1, 0.25)
        3

        Notes
        -----
        Generates a fillet line between two intersecting lines NL1
        (P1-PINT) and NL2 (P2-PINT).  Three keypoints may be
        generated, two at the fillet tangent points (PTAN1 and PTAN2)
        and one (optional) at the fillet arc center (PCENT).  Line
        P1-PINT becomes P1-PTAN1, P2-PINT becomes P2-PTAN2, and new
        arc line PTAN1-PTAN2 is generated.  Generated keypoint and
        line numbers are automatically assigned (beginning with the
        lowest available values [NUMSTR]).  Line divisions are set to
        zero (use LESIZE, etc. to modify).
        """
        command = f"LFILLT,{nl1},{nl2},{rad},{pcent}"
        return parse_line_no(self.run(command, **kwargs))

    def lstr(self, p1="", p2="", **kwargs) -> int:
        """Define a straight line irrespective of the active coordinate system.

        APDL Command: LSTR

        Parameters
        ----------
        p1
            Keypoint at the beginning of line.

        p2
            Keypoint at the end of line.

        Returns
        -------
        int
            Line number of the generated line.

        Examples
        --------
        Create a cartesian straight line regardless of the coordinate
        system being in cylindrical.

        >>> mapdl.csys(1)
        >>> k0 = mapdl.k("", 0, 0, 0)
        >>> k1 = mapdl.k("", 1, 1, 1)
        >>> lnum = mapdl.lstr(k0, k1)
        >>> lnum
        1

        Notes
        -----
        Defines a straight line from P1 to P2 using the global
        Cartesian coordinate system.  The active coordinate system
        will be ignored.  The line shape is invariant with the
        coordinate system after it is generated.  Lines may be
        redefined only if not yet attached to an area.
        """
        command = f"LSTR,{p1},{p2}"
        return parse_line_no(self.run(command, **kwargs))

    def ltan(self, nl1="", p3="", xv3="", yv3="", zv3="", **kwargs) -> int:
        """Generate a line at the end of, and tangent to, an existing line.

        APDL Command: LTAN

        Parameters
        ----------
        nl1
            Number of the line the generated line is tangent to.  If
            negative, assume P1 (see below), instead of P2, is the
            second keypoint of line NL1.

        p3
            Keypoint at which generated line must end.

        Returns
        -------
        int
            Line number of the line generated.

        Examples
        --------
        Create a circular arc and generate a tangent spline at the end
        of it directed to a new keypoint.

        >>> k0 = mapdl.k("", 0, 0, 0)
        >>> k1 = mapdl.k("", 0, 0, 1)
        >>> k2 = mapdl.k("", -1, 1.5, 0)
        >>> carc = mapdl.circle(k0, 1, k1, arc=90)
        >>> lnum = mapdl.ltan(carc[0], k2)
        >>> lnum
        2

        Notes
        -----
        Generates a line (P2-P3) tangent at end point (P2) of line NL1
        (P1-P2).
        """
        command = f"LTAN,{nl1},{p3},{xv3},{yv3},{zv3}"
        return parse_line_no(self.run(command, **kwargs))

    def spline(self, p1="", p2="", p3="", p4="", p5="", p6="", xv1="", yv1="",
               zv1="", xv6="", yv6="", zv6="", **kwargs) -> list:
        """Generate a segmented spline through a series of keypoints.

        APDL Command: SPLINE

        Parameters
        ----------
        p1, p2, p3, . . . , p6
            Keypoints through which the spline is fit.  At least two
            must be defined.

        Returns
        -------
        list
            List of line numbers generated.

        Examples
        --------
        Create a spline with 5 keypoints.

        >>> k0 = mapdl.k('', 0, 0, 0)
        >>> k1 = mapdl.k('', 0.2, 0.2, 0)
        >>> k2 = mapdl.k('', 0.4, 0.3, 0)
        >>> k3 = mapdl.k('', 0.6, 0.5, 0)
        >>> k4 = mapdl.k('', 0.8, 0.3, 0)
        >>> lines = mapdl.spline(k0, k1, k2, k3, k4)
        >>> lines
        [1, 2, 3, 4]

        Notes
        -----
        The output from this command is a series of connected lines
        (one line between each pair of keypoints) that together form a
        spline.  Note that solid modeling in a toroidal coordinate
        system is not recommended.
        """
        command = f"SPLINE,{p1},{p2},{p3},{p4},{p5},{p6},{xv1},{yv1},{zv1},{xv6},{yv6},{zv6}"
        return parse_line_nos(self.run(command, **kwargs))

    def adrag(self, nl1="", nl2="", nl3="", nl4="", nl5="", nl6="", nlp1="",
              nlp2="", nlp3="", nlp4="", nlp5="", nlp6="", **kwargs) -> str:
        """Generate areas by dragging a line pattern along a path.

        APDL Command: ADRAG

        Parameters
        ----------
        nl1, nl2, nl3, . . . , nl6
            List of lines in the pattern to be dragged (6 maximum if
            using keyboard entry).  Lines should form a continuous
            pattern (no more than two lines connected to any one
            keypoint.  If NL1 = ALL, all selected lines (except those
            that define the drag path) will be swept along the path.
            A component name may also be substituted for NL1.

        nlp1, nlp2, nlp3, . . . , nlp6
            List of lines defining the path along which the pattern is
            to be dragged (6 maximum if using keyboard entry).  Must
            be a continuous set of lines.

        Returns
        -------
        str
            MAPDL command output.

        Examples
        --------
        Drag a circle between two keypoints to create an area

        >>> k0 = mapdl.k("", 0, 0, 0)
        >>> k1 = mapdl.k("", 0, 0, 1)
        >>> carc = mapdl.circle(k0, 1, k1, arc=90)
        >>> l0 = mapdl.l(k0, k1)
        >>> output = mapdl.adrag(carc[0], nlp1=l0)
        >>> print(output)
        DRAG LINES:
             1,
        ALONG LINES
             2,

        Notes
        -----
        Generates areas (and their corresponding keypoints and lines)
        by sweeping a given line pattern along a characteristic drag
        path.  If the drag path consists of multiple lines, the drag
        direction is determined by the sequence in which the path
        lines are input (NLP1, NLP2, etc.).  If the drag path is a
        single line (NLP1), the drag direction is from the keypoint on
        the drag line that is closest to the first keypoint of the
        given line pattern to the other end of the drag line.

        The magnitude of the vector between the keypoints of the given
        pattern and the first path keypoint remains constant for all
        generated keypoint patterns and the path keypoints.  The
        direction of the vector relative to the path slope also
        remains constant so that patterns may be swept around curves.

        Keypoint, line, and area numbers are automatically assigned
        (beginning with the lowest available values [NUMSTR]).
        Adjacent lines use a common keypoint.  Adjacent areas use a
        common line.  For best results, the entities to be dragged
        should be orthogonal to the start of the drag path.  Drag
        operations that produce an error message may create some of
        the desired entities prior to terminating.
        """
        command = f"ADRAG,{nl1},{nl2},{nl3},{nl4},{nl5},{nl6},{nlp1},{nlp2},{nlp3},{nlp4},{nlp5},{nlp6}"
        return self.run(command, **kwargs)

    def vdrag(self, na1="", na2="", na3="", na4="", na5="", na6="", nlp1="",
              nlp2="", nlp3="", nlp4="", nlp5="", nlp6="", **kwargs) -> str:
        """APDL Command: VDRAG

        Generate volumes by dragging an area pattern along a path.

        Parameters
        ----------
        na1, na2, na3, . . . , na6
            List of areas in the pattern to be dragged (6 maximum if
            using keyboard entry).  If NA1 = ALL, all selected areas
            will be swept along the path.  A component name may also
            be substituted for NA1.

        nlp1, nlp2, nlp3, . . . , nlp6
            List of lines defining the path along which the pattern is
            to be dragged (6 maximum if using keyboard entry).  Must
            be a continuous set of lines.  To be continuous, adjacent
            lines must share the connecting keypoint (the end keypoint
            of one line must also be first keypoint of the next line).

        Returns
        -------
        str
            MAPDL command output.

        Examples
        --------
        Create a square with a hole in it and drag it along an arc.

        >>> anum0 = mapdl.blc4(0, 0, 1, 1)
        >>> anum1 = mapdl.blc4(0.25, 0.25, 0.5, 0.5)
        >>> aout = mapdl.asba(anum0, anum1)
        >>> k0 = mapdl.k("", 0, 0, 0)
        >>> k1 = mapdl.k("", 1, 0, 1)
        >>> k2 = mapdl.k("", 1, 0, 0)
        >>> l0 = mapdl.larc(k0, k1, k2, 2)
        >>> output = mapdl.vdrag(aout, nlp1=l0)
        >>> print(output)
        DRAG AREAS
          3,
        ALONG LINES
          9


        Notes
        -----
        Generates volumes (and their corresponding keypoints, lines,
        and areas) by sweeping a given area pattern along a
        characteristic drag path.  If the drag path consists of
        multiple lines, the drag direction is determined by the
        sequence in which the path lines are input (NLP1, NLP2, etc.).
        If the drag path is a single line (NLP1), the drag direction
        is from the keypoint on the drag line that is closest to the
        first keypoint of the given area pattern to the other end of
        the drag line.

        The magnitude of the vector between the keypoints of the given
        pattern and the first path keypoint remains constant for all
        generated keypoint patterns and the path keypoints.  The
        direction of the vector relative to the path slope also
        remains constant so that patterns may be swept around curves.
        Lines are generated with the same shapes as the given pattern
        and the path lines.

        Keypoint, line, area, and volume numbers are automatically
        assigned (beginning with the lowest available values
        [NUMSTR]).  Adjacent lines use a common keypoint, adjacent
        areas use a common line, and adjacent volumes use a common
        area.  For best results, the entities to be dragged should be
        orthogonal to the start of the drag path.  Drag operations
        that produce an error message may create some of the desired
        entities prior to terminating.

        If element attributes have been associated with the input area
        via the AATT command, the opposite area generated by the VDRAG
        operation will also have those attributes (i.e., the element
        attributes from the input area are copied to the opposite
        area).  Note that only the area opposite the input area will
        have the same attributes as the input area; the areas adjacent
        to the input area will not.

        If the input areas are meshed or belong to a meshed volume,
        the area(s) can be extruded to a 3-D mesh.  Note that the NDIV
        argument of the ESIZE command should be set before extruding
        the meshed areas.  Alternatively, mesh divisions can be
        specified directly on the drag line(s) (LESIZE).  See the
        Modeling and Meshing Guide for more information.

        You can use the VDRAG command to generate 3-D interface
        element meshes for elements INTER194 and INTER195. When
        generating interface element meshes using VDRAG, you must
        specify the line divisions to generate one interface element
        directly on the drag line using the LESIZE command.  The
        source area to be extruded becomes the bottom surface of the
        interface element. Interface elements must be extruded in what
        will become the element's local x direction, that is, bottom
        to top.
        """
        command = f"VDRAG,{na1},{na2},{na3},{na4},{na5},{na6},{nlp1},{nlp2},{nlp3},{nlp4},{nlp5},{nlp6}"
        return self.run(command, **kwargs)

    def va(self, a1="", a2="", a3="", a4="", a5="", a6="", a7="", a8="", a9="",
           a10="", **kwargs) -> int:
        """APDL Command: VA

        Generate a volume bounded by existing areas.

        Parameters
        ----------
        a1, a2, a3, . . . , a10
            List of areas defining volume.  The minimum number of
            areas is 4.  If A1 = ALL, use all selected [ASEL] areas
            and ignore A2 to A10.  A component name may also be
            substituted for A1.

        Returns
        -------
        int
            Volume number of the volume.


        Examples
        --------
        Create a simple tetrahedral bounded by 4 areas.

        >>> k0 = mapdl.k('', -1, 0, 0)
        >>> k1 = mapdl.k('', 1, 0,  0)
        >>> k2 = mapdl.k('', 1, 1, 0)
        >>> k3 = mapdl.k('', 1, 0.5, 1)
        >>> a0 = mapdl.a(k0, k1, k2)
        >>> a1 = mapdl.a(k0, k1, k3)
        >>> a2 = mapdl.a(k1, k2, k3)
        >>> a3 = mapdl.a(k0, k2, k3)
        >>> vnum = mapdl.va(a0, a1, a2, a3)
        >>> vnum
        1

        Notes
        -----
        This command conveniently allows generating volumes from
        regions having more than eight keypoints (which is not allowed
        with the V command).  Areas may be input in any order.  The
        exterior surface of a VA volume must be continuous, but holes
        may pass completely through it.
        """
        command = f"VA,{a1},{a2},{a3},{a4},{a5},{a6},{a7},{a8},{a9},{a10}"
        return parse_v(self.run(command, **kwargs))

    def vext(self, na1="", na2="", ninc="", dx="", dy="", dz="", rx="", ry="",
             rz="", **kwargs) -> str:
        """APDL Command: VEXT

        Generate additional volumes by extruding areas.

        Parameters
        ----------
        na1, na2, ninc
            Set of areas (NA1 to NA2 in steps of NINC) that defines
            the pattern to be extruded.  NA2 defaults to NA1, NINC
            defaults to 1.  If NA1 = ALL, NA2 and NINC are ignored and
            the pattern is defined by all selected areas.  A component
            name may also be substituted for NA1 (NA2 and NINC are
            ignored).

        dx, dy, dz
            Increments to be applied to the X, Y, and Z keypoint
            coordinates in the active coordinate system (DR, Dθ, DZ
            for cylindrical; DR, Dθ, DΦ for spherical).

        rx, ry, rz
            Scale factors to be applied to the X, Y, and Z keypoint
            coordinates in the active coordinate system (RR, Rθ, RZ
            for cylindrical; RR, Rθ, RΦ for spherical).  Note that the
            Rθ and RΦ scale factors are interpreted as angular
            offsets.  For example, if CSYS = 1, RX, RY, RZ input of
            (1.5,10,3) would scale the specified keypoints 1.5 times
            in the radial and 3 times in the Z direction, while adding
            an offset of 10 degrees to the keypoints.  Zero, blank, or
            negative scale factor values are assumed to be 1.0.  Zero
            or blank angular offsets have no effect.

        Returns
        -------
        str
            MAPDL command output.

        Examples
        --------
        Create a basic cylinder by extruding a circle.

        >>> k0 = mapdl.k("", 0, 0, 0)
        >>> k1 = mapdl.k("", 0, 0, 1)
        >>> k2 = mapdl.k("", 0, 0, 0.5)
        >>> carc0 = mapdl.circle(k0, 1, k1)
        >>> a0 = mapdl.al(*carc0)
        >>> mapdl.vext(a0, dz=4)

        Create a tapered cylinder.

        >>> mapdl.vdele('all')
        >>> mapdl.vext(a0, dz=4, rx=0.3, ry=0.3, rz=1)

        Notes
        -----
        Generates additional volumes (and their corresponding
        keypoints, lines, and areas) by extruding and scaling a
        pattern of areas in the active coordinate system.

        If element attributes have been associated with the input area
        via the AATT command, the opposite area generated by the VEXT
        operation will also have those attributes (i.e., the element
        attributes from the input area are copied to the opposite
        area).  Note that only the area opposite the input area will
        have the same attributes as the input area; the areas adjacent
        to the input area will not.

        If the areas are meshed or belong to meshed volumes, a 3-D
        mesh can be extruded with this command.  Note that the NDIV
        argument on the ESIZE command should be set before extruding
        the meshed areas.

        Scaling of the input areas, if specified, is performed first,
        followed by the extrusion.

        In a non-Cartesian coordinate system, the VEXT command locates
        the end face of the volume based on the active coordinate
        system.  However, the extrusion is made along a straight line
        between the end faces.  Note that solid modeling in a toroidal
        coordinate system is not recommended.

        Caution:: : Use of the VEXT command can produce unexpected
        results when operating in a non-Cartesian coordinate system.
        For a detailed description of the possible problems that may
        occur, see Solid Modeling in the Modeling and Meshing Guide.
        """
        command = f"VEXT,{na1},{na2},{ninc},{dx},{dy},{dz},{rx},{ry},{rz}"
        return self.run(command, **kwargs)

    def vrotat(self, na1="", na2="", na3="", na4="", na5="",
               na6="", pax1="", pax2="", arc="", nseg="",
               **kwargs) -> str:
        """APDL Command: VROTAT

        Generate cylindrical volumes by rotating an area pattern about
        an axis.

        Parameters
        ----------
        na1, na2, na3, . . . , na6
            List of areas in the pattern to be rotated (6 maximum if
            using keyboard entry).  Areas must lie to one side of, and
            in the plane of, the axis of rotation.  If NA1 = ALL,
            all selected areas will define the pattern to be rotated.
            A component name may also be substituted for NA1.

        pax1, pax2
            Keypoints defining the axis about which the area pattern
            is to be rotated.

        arc
            Arc length (in degrees).  Positive follows right-hand rule
            about PAX1-PAX2 vector.  Defaults to 360.

        nseg
            Number of volumes (8 maximum) around circumference.
            Defaults to minimum required for 90 degrees (maximum) arcs, i.e.,
            4 for 360 degrees, 3 for 270 degrees, etc.

        Returns
        -------
        str
            MAPDL command output.

        Examples
        --------
        Rotate a circle about the Z axis to create a hoop.

        First, create a circle offset from origin on the XZ plane.

        >>> hoop_radius = 10
        >>> hoop_thickness = 0.5
        >>> k0 = mapdl.k("", hoop_radius, 0, 0)
        >>> k1 = mapdl.k("", hoop_radius, 1, 0)
        >>> k2 = mapdl.k("", hoop_radius, 0, hoop_thickness)
        >>> carc0 = mapdl.circle(k0, 1, k1)
        >>> a0 = mapdl.al(*carc0)

        Create a hoop by rotating it about an axis defined by two
        keypoints.

        >>> k_axis0 = mapdl.k("", 0, 0, 0)
        >>> k_axis1 = mapdl.k("", 0, 0, 1)
        mapdl.vrotat(a0, pax1=k_axis0, pax2=k_axis1)

        Notes
        -----
        Generates cylindrical volumes (and their corresponding
        keypoints, lines, and areas) by rotating an area pattern (and
        its associated line and keypoint patterns) about an axis.
        Keypoint patterns are generated at regular angular locations
        (based on a maximum spacing of 90 degrees).  Line patterns are
        generated at the keypoint patterns.  Arc lines are also
        generated to connect the keypoints circumferentially.
        Keypoint, line, area, and volume numbers are automatically
        assigned (beginning with the lowest available values).
        Adjacent lines use a common keypoint, adjacent areas use a
        common line, and adjacent volumes use a common area.

        To generate a single volume with an arc greater than 180 degrees,
        NSEG must be greater than or equal to 2.

        If element attributes have been associated with the input area
        via the AATT command, the opposite area generated by the
        VROTAT operation will also have those attributes (i.e., the
        element attributes from the input area are copied to the
        opposite area).  Note that only the area opposite the input
        area will have the same attributes as the input area; the
        areas adjacent to the input area will not.

        If the given areas are meshed or belong to meshed volumes, the
        2-D mesh can be rotated (extruded) to a 3-D mesh. See the
        Modeling and Meshing Guide for more information.  Note that
        the NDIV argument on the ESIZE command should be set before
        extruding the meshed areas.
        """
        command = f"VROTAT,{na1},{na2},{na3},{na4},{na5},{na6},{pax1},{pax2},{arc},{nseg}"
        return self.run(command, **kwargs)

    def vsymm(self, ncomp="", nv1="", nv2="", ninc="", kinc="", noelem="",
              imove="", **kwargs) -> str:
        """APDL Command: VSYMM

        Generate volumes from a volume pattern by symmetry reflection.

        Parameters
        ----------
        ncomp
            Symmetry key:

            - ``'X'`` : X symmetry (default).
            - ``'Y'`` : Y symmetry.
            - ``'Z'`` : Z symmetry.

        nv1, nv2, ninc
            Reflect volumes from pattern beginning with NV1 to NV2
            (defaults to NV1) in steps of NINC (defaults to 1).  If
            NV1 = ALL, NV2 and NINC are ignored and the pattern is all
            selected volumes [VSEL].  A component name may also be
            substituted for NV1 (NV2 and NINC are ignored).

        kinc
            Keypoint increment between sets.  If zero, the lowest
            available keypoint numbers are assigned [NUMSTR].

        noelem
            Specifies whether nodes and elements are also to be generated:

            0 - Generate nodes and elements associated with the
                original volumes, if they exist.

            1 - Do not generate nodes and elements.

        imove
            Specifies whether volumes will be moved or newly defined:

            0 - Generate additional volumes.

            1 - Move original volumes to new position retaining the
                same keypoint numbers (KINC and NOELEM are ignored).
                Corresponding meshed items are also moved if not
                needed at their original position.

        Returns
        -------
        str
            MAPDL command output.

        Examples
        --------
        Create four blocks by reflecting a single block across the X
        component and then the Y component.

        >>> vnum = mapdl.blc4(1, 1, 1, 1, depth=1)
        >>> mapdl.vsymm('X', vnum)
        >>> output = mapdl.vsymm('Y', 'ALL')
        >>> print(output)
        SYMMETRY TRANSFORMATION OF VOLUMES       USING COMPONENT  Y
           SET IS ALL SELECTED VOLUMES

        Notes
        -----
        Generates a reflected set of volumes (and their corresponding
        keypoints, lines, areas and mesh) from a given volume pattern
        by a symmetry reflection (see analogous node symmetry command,
        NSYM).  The MAT, TYPE, REAL, and ESYS attributes are based
        upon the volumes in the pattern and not upon the current
        settings.  Reflection is done in the active coordinate system
        by changing a particular coordinate sign.  The active
        coordinate system must be a Cartesian system.  Volumes in the
        pattern may have been generated in any coordinate system.
        However, solid modeling in a toroidal coordinate system is not
        recommended.  Volumes are generated as described in the VGEN
        command.

        See the ESYM command for additional information about symmetry
        elements.
        """
        command = f"VSYMM,{ncomp},{nv1},{nv2},{ninc},{kinc},{noelem},{imove}"
        return self.run(command, **kwargs)

    def blc5(self, xcenter="", ycenter="", width="", height="", depth="",
             **kwargs) -> int:
        """APDL Command: BLC5

        Create a rectangular area or block volume by center and corner
        points.

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

        Notes
        -----
        Defines a rectangular area anywhere on the working plane or a
        hexahedral volume with one face anywhere on the working plane
        by specifying the center and corner points.  A rectangle will
        be defined with four keypoints and four lines.  A volume will
        be defined with eight keypoints, twelve lines, and six areas,
        with the top and bottom faces parallel to the working plane.
        See the ``BLC4``, ``RECTNG``, and ``BLOCK`` commands for
        alternate ways to create rectangles and blocks.
        """
        command = f"BLC5,{xcenter},{ycenter},{width},{height},{depth}"
        return parse_output_volume_area(self.run(command, **kwargs))

    def block(self, x1="", x2="", y1="", y2="", z1="", z2="", **kwargs):
        """APDL Command: BLOCK

        Create a block volume based on working plane coordinates.

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

        Notes
        -----
        Defines a hexahedral volume based on the working plane.  The
        block must have a spatial volume greater than zero (i.e., this
        volume primitive command cannot be used to create a degenerate
        volume as a means of creating an area.)  The volume will be
        defined with eight keypoints, twelve lines, and six areas,
        with the top and bottom faces parallel to the working plane.
        See the ``BLC4`` and ``BLC5`` commands for alternate ways to
        create blocks.
        """
        command = f"BLOCK,{x1},{x2},{y1},{y2},{z1},{z2}"
        return parse_output_volume_area(self.run(command, **kwargs))

    def con4(self, xcenter="", ycenter="", rad1="", rad2="", depth="",
             **kwargs) -> int:
        """Create a conical volume anywhere on the working plane.

        APDL Command: CON4

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
            zero (see "Notes" below).

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

        Notes
        -----
        Defines a solid conical volume with either the vertex or a
        face anywhere on the working plane.  The cone must have a
        spatial volume greater than zero.  (i.e., this volume
        primitive command cannot be used to create a degenerate volume
        as a means of creating an area.)  The face or faces will be
        circular (each area defined with four lines), and they will be
        connected with two areas (each spanning 180 degrees).  See the CONE
        command for an alternate way to create cones.
        """
        command = f"CON4,{xcenter},{ycenter},{rad1},{rad2},{depth}"
        return parse_output_volume_area(self.run(command, **kwargs))

    def cone(self, rbot="", rtop="", z1="", z2="", theta1="", theta2="",
             **kwargs) -> int:
        """Create a conical volume centered about the working plane origin.

        APDL Command: CONE

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

        Notes
        -----
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
        """
        command = f"CONE,{rbot},{rtop},{z1},{z2},{theta1},{theta2}"
        return parse_output_volume_area(self.run(command, **kwargs))

    def cyl5(self, xedge1="", yedge1="", xedge2="", yedge2="", depth="",
             **kwargs) -> int:
        """Create a circular area or cylindrical volume by end points.

        APDL Command: CYL5

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

        Notes
        -----
        Defines a circular area anywhere on the working plane or a
        cylindrical volume with one face anywhere on the working plane
        by specifying diameter end points.  For a solid cylinder of
        360°, the top and bottom faces will be circular (each area
        defined with four lines) and they will be connected with two
        surface areas (each spanning 180°).  See the CYL4, PCIRC, and
        CYLIND commands for alternate ways to create circles and
        cylinders.
        """
        command = f"CYL5,{xedge1},{yedge1},{xedge2},{yedge2},{depth}"
        return parse_output_volume_area(self.run(command, **kwargs))

    def cylind(self, rad1="", rad2="", z1="", z2="", theta1="", theta2="",
               **kwargs) -> int:
        """Create a cylindrical volume centered about the working plane origin.

        APDL Command: CYLIND

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

        Notes
        -----
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
        """
        command = f"CYLIND,{rad1},{rad2},{z1},{z2},{theta1},{theta2}"
        return parse_output_volume_area(self.run(command, **kwargs))

    def pcirc(self, rad1="", rad2="", theta1="", theta2="", **kwargs) -> int:
        """Create a circular area centered about the working plane origin.

        APDL Command: PCIRC

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

        Notes
        -----
        Defines a solid circular area or circular sector centered
        about the working plane origin.  For a solid circle of 360°,
        the area will be defined with four keypoints and four lines.
        See the ``cyl4`` and ``cyl5`` commands for alternate ways to
        create circles.
        """
        command = f"PCIRC,{rad1},{rad2},{theta1},{theta2}"
        return parse_output_volume_area(self.run(command, **kwargs))

    def rectng(self, x1="", x2="", y1="", y2="", **kwargs):
        """Create a rectangular area anywhere on the working plane.

        APDL Command: RECTNG

        Parameters
        ----------
        x1, x2
            Working plane X coordinates of the rectangle.

        y1, y2
            Working plane Y coordinates of the rectangle.

        Notes
        -----
        The area will be defined with four keypoints and four lines.
        See the ``blc4`` and ``blc5`` commands for alternate ways to
        create rectangles.
        """
        command = f"RECTNG,{x1},{x2},{y1},{y2}"
        return parse_output_volume_area(self.run(command, **kwargs))

    def sph4(self, xcenter="", ycenter="", rad1="", rad2="", **kwargs) -> int:
        """Create a spherical volume anywhere on the working plane.

        APDL Command: SPH4

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

        Notes
        -----
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
        """
        command = f"SPH4,{xcenter},{ycenter},{rad1},{rad2}"
        return parse_output_volume_area(self.run(command, **kwargs))

    def sphere(self, rad1="", rad2="", theta1="", theta2="", **kwargs) -> int:
        """Create a spherical volume centered about the working plane origin.

        APDL Command: SPHERE

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

        Notes
        -----
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
        """
        command = f"SPHERE,{rad1},{rad2},{theta1},{theta2}"
        return parse_output_volume_area(self.run(command, **kwargs))

    def sph5(self, xedge1="", yedge1="", xedge2="", yedge2="", **kwargs) -> int:
        """Create a spherical volume by diameter end points.

        APDL Command: SPH5

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

        Notes
        -----
        Defines a solid spherical volume anywhere on the working plane
        by specifying diameter end points.  The sphere must have a
        spatial volume greater than zero.  (i.e., this volume
        primitive command cannot be used to create a degenerate volume
        as a means of creating an area.)  A sphere of 360° will be
        defined with two areas, each consisting of a hemisphere.  See
        the ``sphere`` and ``sph4`` commands for other ways to create
        spheres.
        """
        command = f"SPH5,{xedge1},{yedge1},{xedge2},{yedge2}"
        return parse_output_volume_area(self.run(command, **kwargs))

    def torus(self, rad1="", rad2="", rad3="", theta1="", theta2="", **kwargs):
        """Create a toroidal volume.

        APDL Command: TORUS

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

        Notes
        -----
        Defines a toroidal volume centered about the working plane
        origin.  A solid torus of 360° will be defined with four
        areas, each area spanning 180° around the major and minor
        circumference.
        """
        command = f"TORUS,{rad1},{rad2},{rad3},{theta1},{theta2}"
        return parse_output_volume_area(self.run(command, **kwargs))
