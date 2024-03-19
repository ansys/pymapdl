import re

from ansys.mapdl.core._commands import parse


class KeyPoints:
    def k(self, npt="", x="", y="", z="", **kwargs) -> int:
        """Define a keypoint.

        APDL Command: K

        Defines a keypoint in the active coordinate system [CSYS] for
        line, area, and volume descriptions.  A previously defined
        keypoint of the same number will be redefined.  Keypoints may
        be redefined only if it is not yet attached to a line or is
        not yet meshed.  Solid modeling in a toroidal system is not
        recommended.

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

        """
        command = f"K,{npt},{x},{y},{z}"
        msg = self.run(command, **kwargs)

        if msg:
            if not re.search(r"KEYPOINT NUMBER", msg):
                res = re.search(r"(KEYPOINT\s*)([0-9]+)", msg)
            else:
                res = re.search(r"(KEYPOINT NUMBER =\s*)([0-9]+)", msg)

            if res:
                return int(res.group(2))

    def kbetw(self, kp1="", kp2="", kpnew="", type_="", value="", **kwargs) -> int:
        """Creates a keypoint between two existing keypoints.

        APDL Command: KBETW

        Placement of the new keypoint depends on the currently active
        coordinate system [CSYS].  If the coordinate system is
        Cartesian, the keypoint will lie on a straight line between
        KP1 and KP2.  If the system is not Cartesian (e.g.,
        cylindrical, spherical, etc.), the keypoint will be located as
        if on a line (which may not be straight) created in the
        current coordinate system between KP1 and KP2.  Note that
        solid modeling in a toroidal coordinate system is not
        recommended.

        Parameters
        ----------
        kp1
            First keypoint.

        kp2
            Second keypoint.

        kpnew
            Number assigned to the new keypoint.  Defaults to the
            lowest available keypoint number.

        type\_
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

        """
        command = f"KBETW,{kp1},{kp2},{kpnew},{type_},{value}"
        return parse.parse_kpoint(self.run(command, **kwargs))

    def kcenter(
        self, type_="", val1="", val2="", val3="", val4="", kpnew="", **kwargs
    ) -> int:
        """Creates a keypoint at the center of a circular arc defined
        by three locations.

        APDL Command: KCENTER

        KCENTER should be used in the Cartesian coordinate system
        (CSYS,0) only.

        Parameters
        ----------
        type\_
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

        """
        command = f"KCENTER,{type_},{val1},{val2},{val3},{val4},{kpnew}"
        return parse.parse_kpoint(self.run(command, **kwargs))

    def kdele(self, np1="", np2="", ninc="", **kwargs):
        """Deletes unmeshed keypoints.

        APDL Command: KDELE

        Deletes selected keypoints.  A keypoint attached to a line cannot be
        deleted unless the line is first deleted.

        Parameters
        ----------
        np1, np2, ninc
            Delete keypoints from NP1 to NP2 (defaults to NP1) in steps of NINC
            (defaults to 1).  If NP1 = ALL, NP2 and NINC are ignored and all
            selected keypoints [KSEL] are deleted.  If NP1 = P, graphical
            picking is enabled and all remaining command fields are ignored
            (valid only in the GUI).  A component name may also be substituted
            for NP1 (NP2 and NINC are ignored).

        """
        command = f"KDELE,{np1},{np2},{ninc}"
        return self.run(command, **kwargs)

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
            ``[DIST, X, Y, Z]`` distance between two keypoints.

        Notes
        -----
        KDIST lists the distance between keypoints KP1 and KP2, as
        well as the current coordinate system offsets from KP1 to KP2,
        where the X, Y, and Z locations of KP1 are subtracted from the
        X, Y, and Z locations of KP2 (respectively) to determine the
        offsets.  KDIST is valid in any coordinate system except
        toroidal [CSYS,3].
        This command is valid in any processor.

        Examples
        --------
        Compute the distance between two keypoints.

        >>> kp0 = (0, 10, -3)
        >>> kp1 = (1, 5, 10)
        >>> knum0 = mapdl.k("", *kp0)
        >>> knum1 = mapdl.k("", *kp1)
        >>> dist = mapdl.kdist(knum0, knum1)
        >>> dist
        [13.96424004376894, 1.0, -5.0, 13.0]

        """
        return parse.parse_kdist(self.run(f"KDIST,{kp1},{kp2}", **kwargs))

    def kfill(self, np1="", np2="", nfill="", nstrt="", ninc="", space="", **kwargs):
        """Generates keypoints between two keypoints.

        APDL Command: KFILL

        Generates keypoints (in the active coordinate system) between two
        existing keypoints.  The two keypoints may have been defined in any
        coordinate system. However, solid modeling in a toroidal coordinate
        system is not recommended.   Any number of keypoints may be filled in
        and any keypoint numbering sequence may be assigned.

        Parameters
        ----------
        np1, np2
            Beginning and ending keypoints for fill-in.  NP1 defaults to next
            to last keypoint specified, NP2 defaults to last keypoint
            specified.  If NP1 = P, graphical picking is enabled and all
            remaining command fields are ignored (valid only in the GUI).

        nfill
            Fill NFILL keypoints between NP1 and NP2 (defaults to ``|NP2-NP1|-1``).
            NFILL must be positive.

        nstrt
            Keypoint number assigned to first filled-in keypoint (defaults to
            NP1 + NINC).

        ninc
            Add this increment to each of the remaining filled-in keypoint
            numbers (may be positive or negative).  Defaults to
            ``(NP2-NP1)/(NFILL + 1)``, i.e., linear interpolation.

        space
            Spacing ratio.  Ratio of last division size to first division size.
            If > 1.0, divisions increase.  If < 1.0, divisions decrease.  Ratio
            defaults to 1.0 (uniform spacing).

        """
        command = f"KFILL,{np1},{np2},{nfill},{nstrt},{ninc},{space}"
        return self.run(command, **kwargs)

    def kgen(
        self,
        itime="",
        np1="",
        np2="",
        ninc="",
        dx="",
        dy="",
        dz="",
        kinc="",
        noelem="",
        imove="",
        **kwargs,
    ):
        """Generates additional keypoints from a pattern of keypoints.

        APDL Command: KGEN

        Parameters
        ----------
        itime
            Do this generation operation a total of ITIME times, incrementing
            all keypoints in the given pattern automatically (or by KINC) each
            time after the first.  ITIME must be more than 1 for generation to
            occur.

        np1, np2, ninc
            Generate keypoints from the pattern of keypoints beginning
            with NP1 to NP2 (defaults to NP1) in steps of NINC
            (defaults to 1).  If NP1 = ALL, NP2 and NINC are ignored
            and the pattern is all selected keypoints [KSEL].  If NP1
            is negative, NP2 and NINC are ignored and the last
            ``|NP1|`` keypoints (in sequence from the highest keypoint
            number) are used as the pattern to be repeated.  A
            component name may also be substituted for NP1 (NP2 and
            NINC are ignored).

        dx, dy, dz
            Keypoint location increments in the active coordinate system (DR,
            Dθ, DZ for cylindrical, DR, Dθ, DΦ for spherical).

        kinc
            Keypoint increment between generated sets.  If zero, the lowest
            available keypoint numbers are assigned [NUMSTR].

        noelem
            Specifies if elements and nodes are also to be generated:

            0 - Generate nodes and point elements associated with the
                original keypoints, if they exist.

            1 - Do not generate nodes and elements.

        imove
            Specifies whether keypoints will be moved or newly defined:

            0 - Generate additional keypoints as requested with the
                ITIME argument.

            1 - Move original keypoints to new position retaining the
                same keypoint numbers (ITIME, KINC, and NOELEM are
                ignored).  Valid only if the old keypoints are no
                longer needed at their original positions.
                Corresponding meshed items are also moved if not
                needed at their original position.

        Notes
        -----
        Generates additional keypoints (and corresponding mesh) from a given
        keypoint pattern.  The MAT, TYPE, REAL, and ESYS attributes are based
        upon the keypoints in the pattern and not upon the current settings.
        Generation is done in the active coordinate system.  Keypoints in the
        pattern may have been defined in any coordinate system.  However, solid
        modeling in a toroidal coordinate system is not recommended.
        """
        command = (
            f"KGEN,{itime},{np1},{np2},{ninc},{dx},{dy},{dz},{kinc},{noelem},{imove}"
        )
        return self.run(command, **kwargs)

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
            res = re.search(r"KEYPOINT\s+(\d+)\s+", msg)
            if res is not None:
                return int(res.group(1))

    def klist(self, np1="", np2="", ninc="", lab="", **kwargs):
        """Lists the defined keypoints or hard points.

        APDL Command: KLIST

        Lists keypoints in the active display coordinate system [DSYS].  An
        attribute (TYPE, MAT, REAL, or ESYS) listed as a zero is unassigned;
        one listed as a positive value indicates that the attribute was
        assigned with the KATT command (and will not be reset to zero if the
        mesh is cleared); one listed as a negative value indicates that the
        attribute was assigned using the attribute pointer [TYPE, MAT, REAL, or
        ESYS] that was active during meshing (and will be reset to zero if the
        mesh is cleared).

        This command is valid in any processor.

        Parameters
        ----------
        np1, np2, ninc
            List keypoints from NP1 to NP2 (defaults to NP1) in steps of NINC
            (defaults to 1).  If NP1 = ALL (default), NP2 and NINC are ignored
            and all selected keypoints [KSEL] are listed.  If NP1 = P,
            graphical picking is enabled and all remaining command fields are
            ignored (valid only in the GUI).  A component name may also be
            substituted for NP1 (NP2 and NINC are ignored).

        lab
            Coordinate listing key:

            (blank) - List all keypoint information.

            COORD - Suppress all but the keypoint coordinates (shown to a higher degree of accuracy
                    than when displayed with all information).

            HPT - List only hard point information.

        """
        command = f"KLIST,{np1},{np2},{ninc},{lab}"
        return self.run(command, **kwargs)

    def kmodif(self, npt="", x="", y="", z="", **kwargs):
        """Modifies an existing keypoint.

        APDL Command: KMODIF

        Parameters
        ----------
        npt
            Modify coordinates of this keypoint.  If NPT = ALL, modify
            coordinates of all selected keypoints [KSEL].  If NPT = P,
            graphical picking is enabled and all remaining command fields are
            ignored (valid only in the GUI).  A component name may also be
            substituted for NPT.

        x, y, z
            Replace the previous coordinate values assigned to this keypoint
            with these corresponding coordinate values.  Values are interpreted
            according to the active coordinate system (R, θ, Z for cylindrical,
            R, θ,Φ for spherical).  If X = P, graphical picking is used to
            locate keypoint and Y and Z are ignored.  A blank retains the
            previous value.  You cannot specify Y = P.

        Notes
        -----
        Lines, areas, and volumes attached to the modified keypoint (if any)
        must all be selected and will be redefined using the active coordinate
        system.  However, solid modeling in a toroidal coordinate system is not
        recommended.

        Caution:: : Redefined entities may be removed from any defined
        components and assemblies. Nodes and elements will be automatically
        cleared from any redefined keypoints, lines, areas, or volumes.

        The KMODIF command moves keypoints for geometry modification without
        validating underlying entities. To merge keypoints and update higher
        order entities, issue the NUMMRG command instead.
        """
        command = f"KMODIF,{npt},{x},{y},{z}"
        return self.run(command, **kwargs)

    def kmove(
        self,
        npt="",
        kc1="",
        x1="",
        y1="",
        z1="",
        kc2="",
        x2="",
        y2="",
        z2="",
        **kwargs,
    ):
        """Calculates and moves a keypoint to an intersection.

        APDL Command: KMOVE

        Parameters
        ----------
        npt
            Move this keypoint.  If NPT = P, graphical picking is enabled and
            all remaining command fields are ignored (valid only in the GUI).
            A component name may also be substituted for NPT.

        kc1
            First coordinate system number.  Defaults to 0 (global Cartesian).

        x1, y1, z1
            Input one or two values defining the location of the keypoint in
            this coordinate system.  Input "U" for unknown value(s) to be
            calculated and input "E" to use an existing coordinate value.
            Fields are R1, θ1, Z1 for cylindrical, or R1, θ1, ϕ1 for spherical.

        kc2
            Second coordinate system number.

        x2, y2, z2
            Input two or one value(s) defining the location of the keypoint in
            this coordinate system.  Input "U" for unknown value(s) to be
            calculated and input "E" to use an existing coordinate value.
            Arguments are R2, θ2, Z2 for cylindrical, or R2, θ2, ϕ2 for
            spherical.

        Notes
        -----
        Calculates and moves a keypoint to an intersection location.  The
        keypoint must have been previously defined (at an approximate location)
        or left undefined (in which case it is internally defined at the SOURCE
        location).  The actual location is calculated from the intersection of
        three surfaces (implied from three coordinate constants in two
        different coordinate systems).  Note that solid modeling in a toroidal
        coordinate system is not recommended.  See the MOVE command for surface
        and intersection details.  The three (of six) constants easiest to
        define should be used.  The program will calculate the remaining three
        coordinate constants.  All arguments, except KC1, must be input.  Use
        the repeat command [``*REPEAT``] after the KMOVE command to move a series
        of keypoints, if desired.
        """
        command = f"KMOVE,{npt},{kc1},{x1},{y1},{z1},{kc2},{x2},{y2},{z2}"
        return self.run(command, **kwargs)

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
            res = re.search(r"KEYPOINT NUMBER =\s+(\d+)", msg)
            if res is not None:
                return int(res.group(1))

    def kplot(self, np1="", np2="", ninc="", lab="", **kwargs):
        """Displays the selected keypoints.

        APDL Command: KPLOT

        Parameters
        ----------
        np1, np2, ninc
            Display keypoints from NP1 to NP2 (defaults to NP1) in steps of
            NINC (defaults to 1).  If NP1 = ALL (default), NP2 and NINC are
            ignored and all selected keypoints [KSEL] are displayed.

        lab
            Determines what keypoints are plotted (one of the following):

            (blank) - Plots all keypoints.

            HPT - Plots only those keypoints that are hard points.

        Notes
        -----
        This command is valid in any processor.
        """
        command = f"KPLOT,{np1},{np2},{ninc},{lab}"
        return self.run(command, **kwargs)

    def kpscale(
        self,
        np1="",
        np2="",
        ninc="",
        rx="",
        ry="",
        rz="",
        kinc="",
        noelem="",
        imove="",
        **kwargs,
    ):
        """Generates a scaled set of (meshed) keypoints from a pattern of

        APDL Command: KPSCALE
        keypoints.

        Parameters
        ----------
        np1, np2, ninc
            Set of keypoints (NP1 to NP2 in steps of NINC) that defines the
            pattern to be scaled.  NP2 defaults to NP1, NINC defaults to 1.  If
            NP1 = ALL, NP2 and NINC are ignored and the pattern is defined by
            all selected keypoints.  If NP1 = P, graphical picking is enabled
            and all remaining command fields are ignored (valid only in the
            GUI).  A component name may also be substituted for NP1 (NP2 and
            NINC are ignored).

        rx, ry, rz
            Scale factors to be applied to the X, Y, Z keypoint coordinates in
            the active coordinate system (RR, Rθ, RZ for cylindrical; RR, Rθ,
            RΦ for spherical).  The Rθ and RΦ scale factors are interpreted as
            angular offsets.  For example, if CSYS = 1, an RX, RY, RZ input of
            (1.5,10,3) would scale the specified keypoints 1.5 times in the
            radial and 3 times in the Z direction, while adding an offset of 10
            degrees to the keypoints.)  Zero, blank, or negative scale factor
            values are assumed to be 1.0.  Zero or blank angular offsets have
            no effect.

        kinc
            Increment to be applied to the keypoint numbers for generated set.
            If zero, the lowest available keypoint numbers will be assigned
            [NUMSTR].

        noelem
            Specifies whether nodes and elements are also to be generated:

            0 - Nodes and point elements associated with the original keypoints will be
                generated (scaled) if they exist.

            1 - Nodes and point elements will not be generated.

        imove
            Specifies whether keypoints will be moved or newly defined:

            0 - Additional keypoints will be generated.

            1 - Original keypoints will be moved to new position (KINC and NOELEM are ignored).
                Use only if the old keypoints are no longer needed at their
                original positions.  Corresponding meshed items are also moved
                if not needed at their original position.

        Notes
        -----
        Generates a scaled set of keypoints (and corresponding mesh) from a
        pattern of keypoints.  The MAT, TYPE, REAL, and ESYS attributes are
        based on the keypoints in the pattern and not the current settings.
        Scaling is done in the active coordinate system.  Keypoints in the
        pattern could have been generated in any coordinate system.  However,
        solid modeling in a toroidal coordinate system is not recommended.
        """
        command = f"KPSCALE,{np1},{np2},{ninc},{rx},{ry},{rz},{kinc},{noelem},{imove}"
        return self.run(command, **kwargs)

    def kscale(self, kinc="", np1="", np2="", ninc="", rx="", ry="", rz="", **kwargs):
        """Generates a scaled pattern of keypoints from a given keypoint pattern.

        APDL Command: KSCALE

        Parameters
        ----------
        kinc
            Do this scaling operation one time, incrementing all keypoints in
            the given pattern by KINC.  If KINC = 0, keypoints will be
            redefined at the scaled locations.

        np1, np2, ninc
            Scale keypoints from pattern beginning with NP1 to NP2 (defaults to
            NP1) in steps of NINC (defaults to 1).  If NP1 = ALL, NP2 and NINC
            are ignored and pattern is all selected keypoints [KSEL].  If NP1 =
            P, graphical picking is enabled and all remaining command fields
            are ignored (valid only in the GUI).  A component name may also be
            substituted for NP1 (NP2 and NINC are ignored).

        rx, ry, rz
            Scale factor ratios.  Scaling is relative to the origin of the
            active coordinate system (RR, Rθ, RZ for cylindrical, RR, Rθ, RΦ
            for spherical).  If > 1.0, pattern is enlarged.  If < 1.0, pattern
            is reduced.  Ratios each default to 1.0.

        Notes
        -----
        Generates a scaled pattern of keypoints from a given keypoint pattern.
        Scaling is done in the active coordinate system (see analogous node
        scaling [NSCALE]).  Solid modeling in a toroidal coordinate system is
        not recommended.
        """
        command = f"KSCALE,{kinc},{np1},{np2},{ninc},{rx},{ry},{rz}"
        return self.run(command, **kwargs)

    def ksum(self, **kwargs):
        """Calculates and prints geometry statistics of the selected keypoints.

        APDL Command: KSUM

        Notes
        -----
        Calculates and prints geometry statistics (centroid location, moments
        of inertia, etc.) associated with the selected keypoints.  Geometry
        items are reported in the global Cartesian coordinate system.  A unit
        density is assumed, irrespective of any material associations [KATT,
        MAT].  Items calculated by KSUM and later retrieved by a ``*GET`` or ``*VGET``
        command are valid only if the model is not modified after the KSUM
        command is issued.
        """
        command = f"KSUM,"
        return self.run(command, **kwargs)

    def ksymm(
        self,
        ncomp="",
        np1="",
        np2="",
        ninc="",
        kinc="",
        noelem="",
        imove="",
        **kwargs,
    ):
        """Generates a reflected set of keypoints.

        APDL Command: KSYMM

        Parameters
        ----------
        ncomp
            Symmetry key:

            X - X (or R) symmetry (default).

            Y - Y (or θ) symmetry.

            Z - Z (or Φ) symmetry.

        np1, np2, ninc
            Reflect keypoints from pattern beginning with NP1 to NP2 (defaults
            to NP1) in steps of NINC (defaults to 1).  If NP1 = ALL, NP2 and
            NINC are ignored and pattern is all selected keypoints [KSEL].  If
            Ncomp = P, graphical picking is enabled and all remaining command
            fields are ignored (valid only in the GUI).  A component name may
            also be substituted for NP1 (NP2 and NINC are ignored).

        kinc
            Keypoint increment between sets.  If zero, the lowest available
            keypoint numbers are assigned [NUMSTR].

        noelem
            Specifies whether nodes and elements are also to be generated:

            0 - Generate nodes and point elements associated with the original keypoints, if
                they exist.

            1 - Do not generate nodes and elements.

        imove
            Specifies whether keypoints will be moved or newly defined:

            0 - Generate additional keypoints.

            1 - Move original keypoints to new position retaining the same keypoint numbers
                (KINC and NOELEM are ignored).  Valid only if the old keypoints
                are no longer needed at their original positions.
                Corresponding meshed items are also moved if not needed at
                their original position.

        Notes
        -----
        Generates a reflected set of keypoints (and corresponding mesh) from a
        given keypoint pattern by a symmetry reflection (see analogous node
        symmetry command, NSYM).  The MAT, TYPE, REAL, and ESYS attributes are
        based upon the keypoints in the pattern and not upon the current
        settings.  Reflection is done in the active coordinate system by
        changing a particular coordinate sign.  Keypoints in the pattern may
        have been generated in any coordinate system.  However, solid modeling
        in a toroidal coordinate system is not recommended.
        """
        command = f"KSYMM,{ncomp},{np1},{np2},{ninc},{kinc},{noelem},{imove}"
        return self.run(command, **kwargs)

    def ktran(
        self,
        kcnto="",
        np1="",
        np2="",
        ninc="",
        kinc="",
        noelem="",
        imove="",
        **kwargs,
    ):
        """Transfers a pattern of keypoints to another coordinate system.

        APDL Command: KTRAN

        Parameters
        ----------
        kcnto
            Reference number of coordinate system where the pattern is to be
            transferred.  Transfer occurs from the active coordinate system.

        np1, np2, ninc
            Transfer keypoints from pattern beginning with NP1 to NP2 (defaults
            to NP1) in steps of NINC (defaults to 1).  If NP1 = ALL, NP2 and
            NINC are ignored and pattern is all selected keypoints [KSEL].  If
            NP1 = P, graphical picking is enabled and all remaining command
            fields are ignored (valid only in the GUI).  A component name may
            also be substituted for NP1 (NP2 and NINC are ignored).

        kinc
            Keypoint increment between sets.  If zero, the lowest available
            keypoint numbers are assigned [NUMSTR].

        noelem
            Specifies whether nodes and elements are also to be generated:

            0 - Generate nodes and point elements associated with the original keypoints, if
                they exist.

            1 - Do not generate nodes and elements.

        imove
            Specifies whether keypoints will be moved or newly defined:

            0 - Generate additional keypoints.

            1 - Move original keypoints to new position retaining the same keypoint numbers
                (KINC and NOELEM are ignored).  Valid only if the old keypoints
                are no longer needed at their original positions.
                Corresponding meshed items are also moved if not needed at
                their original position.

        Notes
        -----
        Transfers a pattern of keypoints (and corresponding mesh) from one
        coordinate system to another (see analogous node transfer command,
        TRANSFER).  The MAT, TYPE, REAL, and ESYS attributes are based upon the
        keypoints in the pattern and not upon the current settings.  Coordinate
        systems may be translated and rotated relative to each other.  Initial
        pattern may be generated in any coordinate system.  Coordinate values
        are interpreted in the active coordinate system and are transferred
        directly.  Solid modeling in a toroidal coordinate system is not
        recommended.
        """
        command = f"KTRAN,{kcnto},{np1},{np2},{ninc},{kinc},{noelem},{imove}"
        return self.run(command, **kwargs)

    def source(self, x="", y="", z="", **kwargs):
        """Defines a default location for undefined nodes or keypoints.

        APDL Command: SOURCE

        Parameters
        ----------
        x, y, z
            Global Cartesian coordinates for source nodes or keypoints
            (defaults to the origin).

        Notes
        -----
        Defines a global Cartesian location for undefined nodes or keypoints
        moved during intersection calculations [MOVE or KMOVE].
        """
        command = f"SOURCE,{x},{y},{z}"
        return self.run(command, **kwargs)
