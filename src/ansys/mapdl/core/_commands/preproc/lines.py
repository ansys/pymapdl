from ansys.mapdl.core._commands import parse


class Lines:
    def bsplin(
        self,
        p1="",
        p2="",
        p3="",
        p4="",
        p5="",
        p6="",
        xv1="",
        yv1="",
        zv1="",
        xv6="",
        yv6="",
        zv6="",
        **kwargs,
    ) -> int:
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

        Notes
        -----
        One line is generated between keypoint P1 and the last
        keypoint entered.  The line will pass through each entered
        keypoint.  Solid modeling in a toroidal coordinate system is
        not recommended.

        Examples
        --------
        Generate a spline through ``(0, 0, 0)``, ``(0, 1, 0)`` and
        ``(1, 2, 0)``

        >>> k0 = mapdl.k("", 0, 0, 0)
        >>> k1 = mapdl.k("", 0, 1, 0)
        >>> k2 = mapdl.k("", 1, 2, 0)
        >>> lnum = mapdl.bsplin(k0, k1, k2)

        """
        command = (
            f"BSPLIN,{p1},{p2},{p3},{p4},{p5},{p6},{xv1},{yv1},{zv1},{xv6},{yv6},{zv6}"
        )
        return parse.parse_line_no(self.run(command, **kwargs))

    def circle(
        self, pcent="", rad="", paxis="", pzero="", arc="", nseg="", **kwargs
    ) -> list:
        """Generate circular arc lines.

        APDL Command: CIRCLE

        Generates circular arc lines (and their corresponding
        keypoints).  Keypoints are generated at regular angular
        locations (based on a maximum spacing of 90 degrees).  Arc lines are
        generated connecting the keypoints.  Keypoint and line numbers
        are automatically assigned, beginning with the lowest
        available values [NUMSTR].  Adjacent lines use a common
        keypoint.  Line shapes are generated as arcs, regardless of
        the active coordinate system.  Line shapes are invariant with
        coordinate system after they are generated.

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

        """
        command = f"CIRCLE,{pcent},{rad},{paxis},{pzero},{arc},{nseg}"
        return parse.parse_line_nos(self.run(command, **kwargs))

    def l(
        self,
        p1="",
        p2="",
        ndiv="",
        space="",
        xv1="",
        yv1="",
        zv1="",
        xv2="",
        yv2="",
        zv2="",
        **kwargs,
    ) -> int:
        """Define a line between two keypoints.

        APDL Command: L

        Defines a line between two keypoints from P1 to P2.  The line
        shape may be generated as "straight" (in the active coordinate
        system) or curved.  The line shape is invariant with
        coordinate system after it is generated.  Note that solid
        modeling in a toroidal coordinate system is not recommended.
        A curved line is limited to 180 degrees.  Lines may be redefined only
        if not yet attached to an area.

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

        """
        command = f"L,{p1},{p2},{ndiv},{space},{xv1},{yv1},{zv1},{xv2},{yv2},{zv2}"
        return parse.parse_line_no(self.run(command, **kwargs))

    def l2ang(
        self, nl1="", nl2="", ang1="", ang2="", phit1="", phit2="", **kwargs
    ) -> int:
        """Generates a line at an angle with two existing lines.

        APDL Command: L2ANG

        Generates a straight line (PHIT1-PHIT2) at an angle (ANG1)
        with an existing line NL1 (P1-P2) and which is also at an
        angle (ANG2) with another existing line NL2 (P3-P4).  If the
        angles are zero the generated line is tangent to the two
        lines.  The PHIT1 and PHIT2 locations on the lines are
        automatically calculated.  Line P1-P2 becomes P1-PHIT1, P3-P4
        becomes P3-PHIT2, and new lines PHIT1-P2, PHIT2-P4, and
        PHIT1-PHIT2 are generated.  Line divisions are set to zero
        (use LESIZE, etc. to modify).

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

        """
        command = f"L2ANG,{nl1},{nl2},{ang1},{ang2},{phit1},{phit2}"
        msg = self.run(command, **kwargs)
        if msg:
            return parse.parse_line_no(msg)

    def l2tan(self, nl1="", nl2="", **kwargs) -> int:
        """Generates a line tangent to two lines.

        APDL Command: L2TAN

        Generates a line (P2-P3) tangent at point P2 to line NL1
        (P1-P2) and tangent at point P3 to line NL2 (P3-P4).

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

        """
        command = f"L2TAN,{nl1},{nl2}"
        return parse.parse_line_no(self.run(command, **kwargs))

    def lang(self, nl1="", p3="", ang="", phit="", locat="", **kwargs) -> int:
        """Generate a straight line at an angle with a line.

        APDL Command: LANG

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

        """
        command = f"LANG,{nl1},{p3},{ang},{phit},{locat}"
        return parse.parse_line_no(self.run(command, **kwargs))

    def larc(self, p1="", p2="", pc="", rad="", **kwargs) -> int:
        """Define a circular arc.

        APDL Command: LARC

        Defines a circular arc line from P1 to P2.  The line shape is
        generated as circular, regardless of the active coordinate
        system.  The line shape is invariant with coordinate system
        after it is generated.

        When dealing with a large radius arc (1e3), or if the location
        of the arc you create is far away from the origin of your
        coordinate system, anomalies may occur. You can prevent this
        by creating the arc at a smaller scale, and then scaling the
        model back to full size (LSSCALE).

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

        """
        command = f"LARC,{p1},{p2},{pc},{rad}"
        return parse.parse_line_no(self.run(command, **kwargs))

    def larea(self, p1="", p2="", narea="", **kwargs) -> int:
        """Generate the shortest line between two keypoints on an area.

        APDL Command: LAREA

        Generates the shortest line between two keypoints, P1 and P2,
        both of which lie on an area.  The generated line will also
        lie on the area.  P1 and P2 may also be equidistant (in global
        Cartesian space) from the area (and on the same side of the
        area), in which case a line parallel to the area is generated.

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

        """
        command = f"LAREA,{p1},{p2},{narea}"
        return parse.parse_line_no(self.run(command, **kwargs))

    def lcomb(self, nl1="", nl2="", keep="", **kwargs) -> int:
        """Combines adjacent lines into one line.

        APDL Command: LCOMB

        Combines adjacent lines into one line (the output line).  This
        operation will effectively "undo" the LDIV operation.  Line
        divisions are set to zero (use LESIZE, etc. to modify).  Lines
        attached to the same area(s) can also be combined.  See also
        the LCCAT command for line concatenation capability.

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

        """
        command = f"LCOMB,{nl1},{nl2},{keep}"
        return parse.parse_line_no(self.run(command, **kwargs))

    def ldele(self, nl1="", nl2="", ninc="", kswp="", **kwargs):
        """Deletes unmeshed lines.

        APDL Command: LDELE

        Parameters
        ----------
        nl1, nl2, ninc
            Delete lines from NL1 to NL2 (defaults to NL1) in steps of NINC
            (defaults to 1).  If NL1 = ALL, NL2 and NINC are ignored and all
            selected lines [LSEL] are deleted.  If NL1 = P, graphical picking
            is enabled and all remaining command fields are ignored (valid only
            in the GUI).  A component name may also be substituted for NL1 (NL2
            and NINC are ignored).

        kswp
            Specifies whether keypoints are also to be deleted:

            0 - Delete lines only.

            1 - Delete lines, as well as keypoints attached to lines but not attached to other
                lines.

        Notes
        -----
        A line attached to an area cannot be deleted unless the area is first
        deleted.
        """
        command = f"LDELE,{nl1},{nl2},{ninc},{kswp}"
        return self.run(command, **kwargs)

    def ldiv(self, nl1="", ratio="", pdiv="", ndiv="", keep="", **kwargs) -> str:
        """Divides a single line into two or more lines.

        APDL Command: LDIV

        Divides a single line NL1 (defined from keypoint P1 to
        keypoint P2) into two or more lines.  Line NL1 becomes the new
        line beginning with keypoint P1 and new lines are generated
        ending at keypoint P2.  If the line is attached to an area,
        the area will also be updated.  Line divisions are set to zero
        (use LESIZE, etc. to modify).

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

        """
        command = f"LDIV,{nl1},{ratio},{pdiv},{ndiv},{keep}"
        return self.run(command, **kwargs)

    def ldrag(
        self,
        nk1="",
        nk2="",
        nk3="",
        nk4="",
        nk5="",
        nk6="",
        nl1="",
        nl2="",
        nl3="",
        nl4="",
        nl5="",
        nl6="",
        **kwargs,
    ):
        """Generates lines by sweeping a keypoint pattern along  path.

        APDL Command: LDRAG

        Parameters
        ----------
        nk1, nk2, nk3, . . . , nk6
            List of keypoints in the pattern to be dragged (6 maximum if using
            keyboard entry).  If NK1 = P, graphical picking is enabled and all
            remaining command fields are ignored (valid only in the GUI).  If
            NK1 = ALL, all selected keypoints (except those that define the
            drag path) will be swept along the path.  A component name may also
            be substituted for NK1.

        nl1, nl2, nl3, . . . , nl6
            List of lines defining the path along which the pattern is to be
            dragged (6 maximum if using keyboard entry).  Must be a continuous
            set of lines.

        Notes
        -----
        Generates lines (and their corresponding keypoints) by sweeping a given
        keypoint pattern along a characteristic drag path.  If the drag path
        consists of multiple lines, the drag direction is determined by the
        sequence in which the path lines are input (NL1, NL2, etc.).  If the
        drag path is a single line (NL1), the drag direction is from the
        keypoint on the drag line that is closest to the first keypoint of the
        given pattern to the other end of the drag line.

        The magnitude of the vector between the keypoints of the given pattern
        and the first path keypoint remains constant for all generated keypoint
        patterns and the path keypoints.  The direction of the vector relative
        to the path slope also remains constant so that patterns may be swept
        around curves.  Keypoint and line numbers are automatically assigned
        (beginning with the lowest available values [NUMSTR]).  For best
        results, the entities to be dragged should be orthogonal to the start
        of the drag path.  Drag operations that produce an error message may
        create some of the desired entities prior to terminating.
        """
        command = f"LDRAG,{nk1},{nk2},{nk3},{nk4},{nk5},{nk6},{nl1},{nl2},{nl3},{nl4},{nl5},{nl6}"
        return self.run(command, **kwargs)

    def lextnd(self, nl1="", nk1="", dist="", keep="", **kwargs) -> int:
        """Extends a line at one end by using its slope.

        APDL Command: LEXTND

        Extends a line at one end by using its slope.  Lines may be
        redefined only if not yet attached to an area.  Line divisions
        are set to zero (use LESIZE, etc. to modify).  Note that solid
        modeling in a toroidal coordinate system is not recommended.

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

        """
        command = f"LEXTND,{nl1},{nk1},{dist},{keep}"
        return parse.parse_line_no(self.run(command, **kwargs))

    def lfillt(self, nl1="", nl2="", rad="", pcent="", **kwargs) -> int:
        """Generate a fillet line between two intersecting lines.

        APDL Command: LFILLT

        Generates a fillet line between two intersecting lines NL1
        (P1-PINT) and NL2 (P2-PINT).  Three keypoints may be
        generated, two at the fillet tangent points (PTAN1 and PTAN2)
        and one (optional) at the fillet arc center (PCENT).  Line
        P1-PINT becomes P1-PTAN1, P2-PINT becomes P2-PTAN2, and new
        arc line PTAN1-PTAN2 is generated.  Generated keypoint and
        line numbers are automatically assigned (beginning with the
        lowest available values [NUMSTR]).  Line divisions are set to
        zero (use LESIZE, etc. to modify).

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

        """
        command = f"LFILLT,{nl1},{nl2},{rad},{pcent}"
        return parse.parse_line_no(self.run(command, **kwargs))

    def lgen(
        self,
        itime="",
        nl1="",
        nl2="",
        ninc="",
        dx="",
        dy="",
        dz="",
        kinc="",
        noelem="",
        imove="",
        **kwargs,
    ):
        """Generates additional lines from a pattern of lines.

        APDL Command: LGEN

        Parameters
        ----------
        itime
            Do this generation operation a total of ITIMEs, incrementing all
            keypoints in the given pattern automatically (or by KINC) each time
            after the first.  ITIME must be > 1 for generation to occur.

        nl1, nl2, ninc
            Generate lines from pattern beginning with NL1 to NL2 (defaults to
            NL1) in steps of NINC (defaults to 1).  If NL1 = ALL, NL2 and NINC
            are ignored and pattern is all selected lines [LSEL].  If NL1 = P,
            graphical picking is enabled and all remaining command fields are
            ignored (valid only in the GUI).  A component name may also be
            substituted for NL1 (NL2 and NINC are ignored).

        dx, dy, dz
            Keypoint location increments in the active coordinate system (--,
            Dθ, DZ for cylindrical, --, Dθ, -- for spherical).

        kinc
            Keypoint increment between generated sets.  If zero, the lowest
            available keypoint numbers are assigned [NUMSTR].

        noelem
            Specifies if elements and nodes are also to be generated:

            0 - Generate nodes and elements associated with the original lines, if they exist.

            1 - Do not generate nodes and elements.

        imove
            Specifies whether to redefine the existing lines:

            0 - Generate additional lines as requested with the ITIME argument.

            1 - Move original lines to new position retaining the same keypoint numbers (ITIME,
                KINC, and NOELM are ignored).  Valid only if the old lines are
                no longer needed at their original positions.  Corresponding
                meshed items are also moved if not needed at their original
                position.

        Notes
        -----
        Generates additional lines (and their corresponding keypoints and mesh)
        from a given line pattern.  The MAT, TYPE, REAL, and ESYS attributes
        are based upon the lines in the pattern and not upon the current
        settings.  End slopes of the generated lines remain the same (in the
        active coordinate system) as those of the given pattern.  For example,
        radial slopes remain radial, etc.  Generations which produce lines of a
        size or shape different from the pattern (i.e., radial generations in
        cylindrical systems, radial and phi generations in spherical systems,
        and theta generations in elliptical systems) are not allowed.  Note
        that solid modeling in a toroidal coordinate system is not recommended.
        New line numbers are automatically assigned (beginning with the lowest
        available values [NUMSTR]).
        """
        command = (
            f"LGEN,{itime},{nl1},{nl2},{ninc},{dx},{dy},{dz},{kinc},{noelem},{imove}"
        )
        return self.run(command, **kwargs)

    def llist(self, nl1="", nl2="", ninc="", lab="", **kwargs):
        """Lists the defined lines.

        APDL Command: LLIST

        Parameters
        ----------
        nl1, nl2, ninc
            List lines from NL1 to NL2 (defaults to NL1) in steps of NINC
            (defaults to 1).  If NL1 = ALL (default), NL2 and NINC are ignored
            and all selected lines [LSEL] are listed.  If NL1 = P, graphical
            picking is enabled and all remaining command fields are ignored
            (valid only in the GUI).  A component name may also be substituted
            for NL1 (NL2 and NINC are ignored).

        lab
            Determines what type of listing is used (one of the following):

            (blank) - Prints information about all lines in the specified range.

            RADIUS - Prints the radius of certain circular arcs, along with the keypoint numbers of
                     each line.  Straight lines, non-circular curves, and
                     circular arcs not internally identified as arcs (which
                     depends upon how each arc is created) will print a radius
                     value of zero.

            LAYER - Prints layer-mesh control specifications.

            HPT - Prints information about only those lines that contain hard points. HPT is not
                  supported in the GUI.

            ORIENT - Prints a list of lines, and identifies any orientation keypoints and any cross
                     section IDs that are associated with the lines.  Used for
                     beam meshing with defined orientation nodes and cross
                     sections.

        Notes
        -----
        There are 2 listings for the number of element divisions and the
        spacing ratio. The first listing shows assignments from LESIZE only,
        followed by the "hard" key (KYNDIV). See LESIZE for more information.
        The second listing shows NDIV and SPACE for the existing mesh, if one
        exists. Whether this existing mesh and the mesh generated by LESIZE
        match at any given point depends upon meshing options and the sequence
        of meshing operations.

        A "-1" in the "nodes" column indicates that the line has been meshed
        but that there are no interior nodes.

        An attribute (TYPE, MAT, REAL, or ESYS) listed as a zero is unassigned;
        one listed as a positive value indicates that the attribute was
        assigned with the LATT command (and will not be reset to zero if the
        mesh is cleared); one listed as a negative value indicates that the
        attribute was assigned using the attribute pointer [TYPE, MAT, REAL, or
        ESYS] that was active during meshing (and will be reset to zero if the
        mesh is cleared).

        This command is valid in any processor.
        """
        command = f"LLIST,{nl1},{nl2},{ninc},{lab}"
        return self.run(command, **kwargs)

    def lplot(self, nl1="", nl2="", ninc="", **kwargs):
        """Displays the selected lines.

        APDL Command: LPLOT

        Parameters
        ----------
        nl1, nl2, ninc
            Display lines from NL1 to NL2 (defaults to NL1) in steps of NINC
            (defaults to 1).  If NL1 = ALL (default), NL2 and NINC are ignored
            and display all selected lines [LSEL].

        Notes
        -----
        Mesh divisions on plotted lines are controlled by the LDIV option of
        the /PSYMB command.

        This command is valid in any processor.
        """
        command = f"LPLOT,{nl1},{nl2},{ninc}"
        return self.run(command, **kwargs)

    def lreverse(self, lnum="", noeflip="", **kwargs):
        """Reverses the normal of a line, regardless of its connectivity or mesh

        APDL Command: LREVERSE
        status.

        Parameters
        ----------
        lnum
            Line number of the line whose normal direction is to be reversed.
            If LNUM = ALL, the normals of all selected lines will be reversed.
            If LNUM = P, graphical picking is enabled.  A component name may
            also be substituted for LNUM.

        noeflip
            Indicates whether you want to change the normal direction of the
            existing elements on the reversed line(s) so that they are
            consistent with each line's new normal direction.

            0 - Make the normal direction of existing elements on the reversed line(s)
                consistent with each line's new normal direction (default).

            1 - Do not change the normal direction of existing elements on the reversed
                line(s).

        Notes
        -----
        You cannot use the LREVERSE command to change the normal direction of
        any element that has a body or surface load.  We recommend that you
        apply all of your loads only after ensuring that the element normal
        directions are acceptable.

        Real constants (such as nonuniform shell thickness and tapered beam
        constants) may be invalidated by an element reversal.

        For more information, see Revising Your Model in the Modeling and
        Meshing Guide.
        """
        command = f"LREVERSE,{lnum},{noeflip}"
        return self.run(command, **kwargs)

    def lrotat(
        self,
        nk1="",
        nk2="",
        nk3="",
        nk4="",
        nk5="",
        nk6="",
        pax1="",
        pax2="",
        arc="",
        nseg="",
        **kwargs,
    ):
        """Generates circular lines by rotating a keypoint pattern about an axis.

        APDL Command: LROTAT

        Parameters
        ----------
        nk1, nk2, nk3, . . . , nk6
            List of keypoints in the pattern to be rotated (6 maximum if using
            keyboard entry).  If NK1 = P, graphical picking is enabled and all
            remaining command fields are ignored (valid only in the GUI).  If
            NK1 = ALL, all selected keypoints (except PAX1 and PAX2) will
            define the pattern to be rotated.  A component name may also be
            substituted for NK1.

        pax1, pax2
            Keypoints defining the axis about which the keypoint pattern is to
            be rotated.

        arc
            Arc length (in degrees).  Positive follows right-hand rule about
            PAX1-PAX2 vector.  Defaults to 360.

        nseg
            Number of lines (8 maximum) around circumference.  Defaults to
            minimum required for 90° (maximum) arcs, i.e., 4 for 360°, 3 for
            270°, etc.

        Notes
        -----
        Generates circular lines (and their corresponding keypoints) by
        rotating a keypoint pattern about an axis.  Keypoint patterns are
        generated at regular angular locations (based on a maximum spacing of
        90°).  Line patterns are generated at the keypoint patterns.  Keypoint
        and line numbers are automatically assigned (beginning with the lowest
        available values [NUMSTR]).
        """
        command = (
            f"LROTAT,{nk1},{nk2},{nk3},{nk4},{nk5},{nk6},{pax1},{pax2},{arc},{nseg}"
        )
        return self.run(command, **kwargs)

    def lsscale(
        self,
        nl1="",
        nl2="",
        ninc="",
        rx="",
        ry="",
        rz="",
        kinc="",
        noelem="",
        imove="",
        **kwargs,
    ):
        """Generates a scaled set of lines from a pattern of lines.

        APDL Command: LSSCALE

        Parameters
        ----------
        nl1, nl2, ninc
            Set of lines (NL1 to NL2 in steps of NINC) that defines the pattern
            to be scaled.  NL2 defaults to NL1, NINC defaults to 1.  If NL1 =
            ALL, NL2 and NINC are ignored and the pattern is defined by all
            selected lines.  If NL1 = P, graphical picking is enabled and all
            remaining command fields are ignored (valid only in the GUI).  A
            component name may also be substituted for NL1 (NL2 and NINC are
            ignored).

        rx, ry, rz
            Scale factors to be applied to the X, Y, Z keypoint coordinates in
            active coordinate system (RR, Rθ, RZ for cylindrical; RR, Rθ, RΦ
            for spherical).  Note that the Rθ and RΦ scale factors are
            interpreted as angular offsets.  For example, for CSYS,1, RR, Rθ,
            RZ input of (1.5,10,3) would scale the specified keypoints 1.5
            times in the radial and 3 times in the Z direction, while adding an
            offset of 10 degrees to the keypoints.  Zero, blank, or negative
            scale factor values are assumed to be 1.0.  Zero or blank angular
            offsets have no effect.

        kinc
            Increment to be applied to keypoint numbers for generated set.  If
            zero, the lowest available keypoint numbers will be assigned
            [NUMSTR].

        noelem
            Specifies whether nodes and elements are also to be generated:

            0 - Nodes and line elements associated with the original lines will be generated
                (scaled) if they exist.

            1 - Nodes and line elements will not be generated.

        imove
            Specifies whether lines will be moved or newly defined:

            0 - Additional lines will be generated.

            1 - Original lines will be moved to new position (KINC and NOELEM are ignored).
                Use only if the old lines are no longer needed at their
                original positions.  Corresponding meshed items are also moved
                if not needed at their original position.

        Notes
        -----
        Generates a scaled set of lines (and their corresponding keypoints and
        mesh) from a pattern of lines.  The MAT, TYPE, REAL, and ESYS
        attributes are based on the lines in the pattern and not the current
        settings.  Scaling is done in the active coordinate system.  Lines in
        the pattern could have been generated in any coordinate system.
        """
        command = f"LSSCALE,{nl1},{nl2},{ninc},{rx},{ry},{rz},{kinc},{noelem},{imove}"
        return self.run(command, **kwargs)

    def lstr(self, p1="", p2="", **kwargs) -> int:
        """Define a straight line irrespective of the active coordinate system.

        APDL Command: LSTR

        Defines a straight line from P1 to P2 using the global
        Cartesian coordinate system.  The active coordinate system
        will be ignored.  The line shape is invariant with the
        coordinate system after it is generated.  Lines may be
        redefined only if not yet attached to an area.

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

        """
        command = f"LSTR,{p1},{p2}"
        return parse.parse_line_no(self.run(command, **kwargs))

    def lsum(self, **kwargs):
        """Calculates and prints geometry statistics of the selected lines.

        APDL Command: LSUM

        Notes
        -----
        Calculates and prints geometry statistics (length, centroid, moments of
        inertia, etc.) associated with the selected lines.  Geometry items are
        reported in the global Cartesian coordinate system.  A unit density is
        assumed, irrespective of any material associations [LATT, MAT].  Items
        calculated by LSUM and later retrieved by a ``*GET`` or ``*VGET`` command are
        valid only if the model is not modified after the LSUM command is
        issued.
        """
        command = f"LSUM,"
        return self.run(command, **kwargs)

    def lsymm(
        self,
        ncomp="",
        nl1="",
        nl2="",
        ninc="",
        kinc="",
        noelem="",
        imove="",
        **kwargs,
    ):
        """Generates lines from a line pattern by symmetry reflection.

        APDL Command: LSYMM

        Parameters
        ----------
        ncomp
            Symmetry key:

            X - X symmetry (default).

            Y - Y symmetry.

            Z - Z symmetry.

        nl1, nl2, ninc
            Reflect lines from pattern beginning with NL1 to NL2 (defaults to
            NL1) in steps of NINC (defaults to 1).  If NL1 = ALL, NL2 and NINC
            are ignored and pattern is all selected lines [LSEL].  If NL1 = P,
            graphical picking is enabled and all remaining command fields are
            ignored (valid only in the GUI).  A component name may also be
            substituted for NL1 (NL2 and NINC are ignored).

        kinc
            Keypoint increment between sets.  If zero, the lowest available
            keypoint  numbers are assigned [NUMSTR].

        noelem
            Specifies whether nodes and elements are also to be generated:

            0 - Generate nodes and elements associated with the original lines, if they exist.

            1 - Do not generate nodes and elements.

        imove
            Specifies whether areas will be moved or newly defined:

            0 - Generate additional lines.

            1 - Move original lines to new position retaining the same keypoint numbers (KINC
                and NOELEM are ignored).  Valid only if the old lines are no
                longer needed at their original positions.  Corresponding
                meshed items are also moved if not needed at their original
                position.

        Notes
        -----
        Generates a reflected set of lines (and their corresponding keypoints
        and mesh) from a given line pattern by a symmetry reflection (see
        analogous node symmetry command, NSYM).  The MAT, TYPE, REAL, and ESYS
        attributes are based upon the lines in the pattern and not upon the
        current settings.  Reflection is done in the active coordinate system
        by changing a particular coordinate sign.  The active coordinate system
        must be Cartesian.  Lines in the pattern may have been generated in any
        coordinate system.  However, solid modeling in a toroidal coordinate
        system is not recommended.  Lines are generated as described in the
        LGEN command.

        See the ESYM command for additional information about symmetry
        elements.
        """
        command = f"LSYMM,{ncomp},{nl1},{nl2},{ninc},{kinc},{noelem},{imove}"
        return self.run(command, **kwargs)

    def ltan(self, nl1="", p3="", xv3="", yv3="", zv3="", **kwargs) -> int:
        """Generate a line at the end of, and tangent to, an existing line.

        APDL Command: LTAN

        Generates a line (P2-P3) tangent at end point (P2) of line NL1
        (P1-P2).

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

        """
        command = f"LTAN,{nl1},{p3},{xv3},{yv3},{zv3}"
        return parse.parse_line_no(self.run(command, **kwargs))

    def ltran(
        self,
        kcnto="",
        nl1="",
        nl2="",
        ninc="",
        kinc="",
        noelem="",
        imove="",
        **kwargs,
    ):
        """Transfers a pattern of lines to another coordinate system.

        APDL Command: LTRAN

        Parameters
        ----------
        kcnto
            Reference number of coordinate system where the pattern is to be
            transferred.  Transfer occurs from the active coordinate system.
            The coordinate system type and parameters of KCNTO must be the same
            as the active system.

        nl1, nl2, ninc
            Transfer lines from pattern beginning with NL1 to NL2 (defaults to
            NL1) in steps of NINC (defaults to 1).  If NL1 = ALL, NL2 and NINC
            are ignored and pattern is all selected lines [LSEL].  If NL1 = P,
            graphical picking is enabled and all remaining command fields are
            ignored (valid only in the GUI).  A component name may also be
            substituted for NL1 (NL2 and NINC are ignored).

        kinc
            Keypoint increment between sets.  If zero, the lowest available
            keypoint numbers are assigned [NUMSTR].

        noelem
            Specifies whether nodes and elements are also to be generated:

            0 - Generate nodes and elements associated with the original lines, if they exist.

            1 - Do not generate nodes and elements.

        imove
            Specifies whether lines will be moved or newly defined:

            0 - Generate additional lines.

            1 - Move original lines to new position retaining the same keypoint numbers (KINC
                and NOELM are ignored).  Valid only if the old lines are no
                longer needed at their original positions.  Corresponding
                meshed items are also moved if not needed at their original
                position.

        Notes
        -----
        Transfers a pattern of lines (and their corresponding keypoints and
        mesh) from one coordinate system to another (see analogous node
        transfer command, TRANSFER).  The MAT, TYPE, REAL, and ESYS attributes
        are based upon the lines in the pattern and not upon the current
        settings.  Coordinate systems may be translated and rotated relative to
        each other.  Initial pattern may be generated in any coordinate system.
        However, solid modeling in a toroidal coordinate system is not
        recommended.  Coordinate and slope values are interpreted in the active
        coordinate system and are transferred directly.  Lines are generated as
        described in the LGEN command.
        """
        command = f"LTRAN,{kcnto},{nl1},{nl2},{ninc},{kinc},{noelem},{imove}"
        return self.run(command, **kwargs)

    def spline(
        self,
        p1="",
        p2="",
        p3="",
        p4="",
        p5="",
        p6="",
        xv1="",
        yv1="",
        zv1="",
        xv6="",
        yv6="",
        zv6="",
        **kwargs,
    ) -> list:
        """Generate a segmented spline through a series of keypoints.

        APDL Command: SPLINE

        The output from this command is a series of connected lines
        (one line between each pair of keypoints) that together form a
        spline.  Note that solid modeling in a toroidal coordinate
        system is not recommended.

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

        """
        command = (
            f"SPLINE,{p1},{p2},{p3},{p4},{p5},{p6},{xv1},{yv1},{zv1},{xv6},{yv6},{zv6}"
        )
        return parse.parse_line_nos(self.run(command, **kwargs))

    def ssln(self, fact="", size="", **kwargs):
        """Selects and displays small lines in the model.

        APDL Command: SSLN

        Parameters
        ----------
        fact
            Factor used to determine small lines.  FACT times the average line
            length in the model is used as the line length limit below which
            lines will be selected.

        size
            Line length limit for line selection.  Lines that have a length
            less than or equal to SIZE will be selected.  Used only if FACT is
            blank.

        Notes
        -----
        SSLN invokes a predefined ANSYS macro for selecting small lines in a
        model.  Lines that are smaller than or equal to the specified limit
        (FACT or SIZE) are selected and line numbers are displayed.  This
        command macro is useful for detecting very small lines in a model that
        may cause problems (i.e., poorly shaped elements or a meshing failure)
        during meshing.  All lines that are not "small" will be unselected and
        can be reselected with the LSEL command.
        """
        command = f"SSLN,{fact},{size}"
        return self.run(command, **kwargs)
