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

def parse_a(msg):
    """Parse create area message and return area number"""
    res = re.search(r"(AREA NUMBER =\s*)([0-9]+)", msg)
    if res is not None:
        return int(res.group(2))


def parse_v(msg):
    """Parse volume message and return volume number"""
    res = re.search(r"(VOLUME NUMBER =\s*)([0-9]+)", msg)
    if res is not None:
        return int(res.group(2))


class _MapdlGeometryCommands():
    """Wraps MAPDL geometry commands"""

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
        keypoint. Coordinate interpretation corresponds to the active
        coordinate system type, i.e., X is R for cylindrical,
        etc. Defaults to zero curvature slope.

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
        msg = self.run(command, **kwargs)
        res = re.search(r"(LINE NO\.=\s*)([0-9]+)", msg)
        if res is not None:
            return int(res.group(2))

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
            recommended.  If positive, SPACE is the nominal ratio of
            the last division size (at P2) to the first division size
            (at P1).  If the ratio is greater than 1, the division
            sizes increase from P1 to P2, and if less than 1, they
            decrease.  If SPACE is negative, then |SPACE| is the
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
        msg = self.run(command, **kwargs)
        res = re.search(r"(LINE NO\.=\s*)([0-9]+)", msg)
        if res is not None:
            return int(res.group(2))

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


def parse_output_area(msg):
    """Parse create area message and return area number"""
    res = re.search(r"(OUTPUT AREA =\s*)([0-9]+)", msg)
    if res is not None:
        return int(res.group(2))


def parse_output_areas(msg):
    """Parse create area message and return area number"""
    res = re.search(r"(OUTPUT AREAS =\s*)([0-9]+)", msg)
    if res is not None:
        return int(res.group(2))


def parse_n(msg):
    """Parse create node message and return node number"""
    res = re.search(r"(NODE\s*)([0-9]+)", msg)
    if res is not None:
        return int(res.group(2))


def parse_al(msg):
    """Parse create area message and return area number"""
    return parse_a(msg)


def parse_kpoint(msg):
    res = re.search(r'kpoint=\s+(\d+)\s+', msg)
    if res is not None:
        return int(res.group(1))


def parse_kdist(msg):
    """Return xyz distance from KDIST

    For example:
    The distance between keypoints 10 and 11 in coordinate system 0
    is:
    DIST              DX (KP2-KP1)      DY (KP2-KP1)      DZ (KP2-KP1)
    1.0000000000E+10 -1.0000000000E+10   0.000000000       0.000000000

    Will return: [-10000000000.0, 0.0, 0.0]

    """
    finds = re.findall(NUM_PATTERN, msg)[-3:]
    if len(finds) == 3:
        return [float(val) for val in finds]


def parse_kl(msg):
    """Return keypoint number from ``kl``

    MAPDL message
    GENERATE KEYPOINT ON LINE      1 AT RATIO=  0.500000

    KEYPOINT    26   X,Y,Z=   5.00000       0.00000       0.00000      IN CSYS=  0

    Return: 25

    """
    res = re.search(r'KEYPOINT\s+(\d+)\s+', msg)
    if res is not None:
        return int(res.group(1))


def parse_knode(msg):
    """Return keypoint number from ``KNODE``

    MAPDL message:
    KEYPOINT         0 FROM NODE         4

    CSYS 0 LOCATION (X,Y,Z)=   0.00000       0.00000       0.00000
    KEYPOINT NUMBER =      5

    Return: 5

    """
    res = re.search(r'KEYPOINT\s+(\d+)\s+', msg)
    if res is not None:
        return int(res.group(1))



geometry_commands = {'N': parse_n,
                     'AL': parse_al,
                     'BLC4': parse_output_area,
                     'CYL4': parse_output_area,
                     'ASBA': parse_output_areas,
                     'KBET': parse_kpoint,
                     'KCEN': parse_kpoint,
                     'KDIS': parse_kdist,
                     'KL': parse_kl,
                     'KNOD': parse_knode,
}
