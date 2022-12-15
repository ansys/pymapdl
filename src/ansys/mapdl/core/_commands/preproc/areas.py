from ansys.mapdl.core._commands import parse


class Areas:
    def a(
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
        p10="",
        p11="",
        p12="",
        p13="",
        p14="",
        p15="",
        p16="",
        p17="",
        p18="",
        **kwargs,
    ) -> int:
        """Define an area by connecting keypoints.

        APDL Command: A

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

        """
        command = f"A,{p1},{p2},{p3},{p4},{p5},{p6},{p7},{p8},{p9},{p10},{p11},{p12},{p13},{p14},{p15},{p16},{p17},{p18}"
        return parse.parse_a(self.run(command, **kwargs))

    def aatt(self, mat="", real="", type_="", esys="", secn="", **kwargs):
        """Associates element attributes with the selected, unmeshed areas.

        APDL Command: AATT

        Areas subsequently generated from the areas will also have these
        attributes.  These element attributes will be used when the areas are
        meshed.  If an area does not have attributes associated with it (by
        this command) at the time it is meshed, the attributes are obtained
        from the then current MAT, REAL, TYPE, ESYS, and SECNUM command
        settings.  Reissue the AATT command (before areas are meshed) to change
        the attributes.  A zero (or blank) argument removes the corresponding
        association. If any of the arguments MAT, REAL, TYPE, ESYS, or SECN are
        defined as -1, then that value will be left unchanged in the selected
        set.

        In some cases, ANSYS can proceed with an area meshing operation even
        when no logical element type has been assigned via AATT,,,TYPE or TYPE.
        For more information, see the discussion on setting element attributes
        in Meshing Your Solid Model in the Modeling and Meshing Guide.

        Parameters
        ----------
        mat
            The material number to be associated with selected, unmeshed areas.

        real
            The real constant set number to be associated with selected,
            unmeshed areas.

        type\_
            The type number to be associated with selected, unmeshed areas.

        esys
            The coordinate system number to be associated with selected,
            unmeshed areas.

        secn
            The section number to be associated with selected unmeshed areas.

        """
        command = f"AATT,{mat},{real},{type_},{esys},{secn}"
        return self.run(command, **kwargs)

    def adele(self, na1="", na2="", ninc="", kswp="", **kwargs):
        """Deletes unmeshed areas.

        APDL Command: ADELE

        Parameters
        ----------
        na1, na2, ninc
            Delete areas from NA1 to NA2 (defaults to NA1) in steps of NINC
            (defaults to 1).  If NA1 = ALL, NA2 and NINC are ignored and all
            selected areas [ASEL] are deleted.  If NA1 = P, graphical picking
            is enabled and all remaining arguments are ignored (valid only in
            the GUI).  A component name may also be substituted for NA1 (NA2
            and NINC are ignored).

        kswp
            Specifies whether keypoints and lines are also to be deleted:

            0 - Delete areas only (default).

            1 - Delete areas, as well as keypoints and lines attached
                to specified areas but not shared by other areas.

        Notes
        -----
        An area attached to a volume cannot be deleted unless the volume is
        first deleted.
        """
        command = f"ADELE,{na1},{na2},{ninc},{kswp}"
        return self.run(command, **kwargs)

    def adgl(self, na1="", na2="", ninc="", **kwargs):
        """Lists keypoints of an area that lie on a parametric degeneracy.

        APDL Command: ADGL

        Parameters
        ----------
        na1, na2, ninc
            List keypoints that lie on a parametric degeneracy on areas from
            NA1 to NA2 (defaults to NA1) in steps of NINC (defaults to 1).  If
            NA1 = ALL (default), NA2 and NINC will be ignored and keypoints on
            all selected areas [ASEL] will be listed.  If NA1 = P, graphical
            picking is enabled and all remaining arguments are ignored (valid
            only in the GUI).  A component name may be substituted in NA1 (NA2
            and NINC will be ignored).

        Notes
        -----
        See the Modeling and Meshing Guide for details on parametric
        degeneracies.

        This command is valid in any processor.
        """
        command = f"ADGL,{na1},{na2},{ninc}"
        return self.run(command, **kwargs)

    def adrag(
        self,
        nl1="",
        nl2="",
        nl3="",
        nl4="",
        nl5="",
        nl6="",
        nlp1="",
        nlp2="",
        nlp3="",
        nlp4="",
        nlp5="",
        nlp6="",
        **kwargs,
    ) -> str:
        """Generate areas by dragging a line pattern along a path.

        APDL Command: ADRAG

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

        """
        command = f"ADRAG,{nl1},{nl2},{nl3},{nl4},{nl5},{nl6},{nlp1},{nlp2},{nlp3},{nlp4},{nlp5},{nlp6}"
        return self.run(command, **kwargs)

    def afillt(self, na1="", na2="", rad="", **kwargs):
        """Generates a fillet at the intersection of two areas.

        APDL Command: AFILLT

        Generates an area of constant fillet radius at the
        intersection of two areas using a series of Boolean
        operations.  Corresponding lines and keypoints are also
        generated.  See BOPTN command for an explanation of the
        options available to Boolean operations.  If areas do not
        initially intersect at a common line, use the AINA command.

        Parameters
        ----------
        na1
            Number of the first intersecting area.

        na2
            Number of the second intersecting area.

        rad
            Radius of fillet to be generated.

        """
        command = f"AFILLT,{na1},{na2},{rad}"
        return self.run(command, **kwargs)

    def agen(
        self,
        itime="",
        na1="",
        na2="",
        ninc="",
        dx="",
        dy="",
        dz="",
        kinc="",
        noelem="",
        imove="",
        **kwargs,
    ):
        """Generates additional areas from a pattern of areas.

        APDL Command: AGEN

        Generates additional areas (and their corresponding keypoints, lines
        and mesh) from a given area pattern.  The MAT, TYPE, REAL, ESYS, and
        SECNUM attributes of the new areas are based upon the areas in the
        pattern and not upon the current settings of the pointers.  End slopes
        of the generated lines remain the same (in the active coordinate
        system) as those of the given pattern.  For example, radial slopes
        remain radial.  Generations which produce areas of a size or shape
        different from the pattern (i.e., radial generations in cylindrical
        systems, radial and phi generations in spherical systems, and theta
        generations in elliptical systems) are not allowed.  Solid modeling in
        a toroidal coordinate system is not recommended.  Area and line numbers
        are automatically assigned, beginning with the lowest available values
        [NUMSTR].

        Parameters
        ----------
        itime
            Do this generation operation a total of ITIMEs, incrementing all
            keypoints in the given pattern automatically (or by KINC) each time
            after the first.  ITIME must be more than 1 for generation to
            occur.

        na1, na2, ninc
            Generate areas from the pattern of areas NA1 to NA2 (defaults to
            NA1) in steps of NINC (defaults to 1).  If NA1 = ALL, NA2 and NINC
            are ignored and the pattern is all selected areas [ASEL].  If NA1 =
            P, graphical picking is enabled and all remaining arguments are
            ignored (valid only in the GUI).  A component name may also be
            substituted for NA1 (NA2 and NINC are ignored).

        dx, dy, dz
            Keypoint location increments in the active coordinate system (--,
            D θ, DZ for cylindrical;  --, D θ, -- for spherical).

        kinc
            Keypoint number increment between generated sets.  If zero, the
            lowest available keypoint numbers are assigned [NUMSTR].

        noelem
            Specifies if elements and nodes are also to be generated:

            0 - Generate nodes and elements associated with the original areas, if they exist.

            1 - Do not generate nodes and elements.

        imove
            Specifies whether to redefine the existing areas:

            0 - Generate new areas as requested with the ITIME argument.

            1 - Move original areas to new position, retaining the same keypoint numbers
                (ITIME, KINC, and NOELEM are ignored).  If the original areas
                are needed in the original position (e.g.,  they may be
                attached to a volume), they are not moved, and new areas are
                generated instead.  Meshed items corresponding to moved areas
                are also moved if not needed at their original position.

        """
        command = (
            f"AGEN,{itime},{na1},{na2},{ninc},{dx},{dy},{dz},{kinc},{noelem},{imove}"
        )
        return self.run(command, **kwargs)

    def al(
        self,
        l1="",
        l2="",
        l3="",
        l4="",
        l5="",
        l6="",
        l7="",
        l8="",
        l9="",
        l10="",
        **kwargs,
    ) -> int:
        """Generate an area bounded by previously defined lines.

        APDL Command: AL

        Lines may be input (once each) in any order and must form a
        simply connected closed curve.  If the area is defined with
        more than four lines, the lines must also lie in the same
        plane or on a constant coordinate value in the active
        coordinate system (such as a plane or a cylinder).

        Solid modeling in a toroidal coordinate system is not
        recommended.  Areas may be redefined only if not yet attached
        to a volume.

        This command is valid in any processor.

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

        """
        command = f"AL,{l1},{l2},{l3},{l4},{l5},{l6},{l7},{l8},{l9},{l10}"
        return parse.parse_a(self.run(command, **kwargs))

    def alist(self, na1="", na2="", ninc="", lab="", **kwargs):
        """Lists the defined areas.

        APDL Command: ALIST

        Parameters
        ----------
        na1, na2, ninc
            List areas from NA1 to NA2 (defaults to NA1) in steps of NINC
            (defaults to 1).  If NA1 = ALL (default), NA2 and NINC are ignored
            and all selected areas [ASEL] are listed.  If NA1 = P, graphical
            picking is enabled and all remaining arguments are ignored (valid
            only in the GUI).  A component name may also be substituted for NA1
            (NA2 and NINC are ignored).

        lab
            Determines what type of listing is used (one of the following):

            (blank) - Prints information about all areas in the specified range.

            HPT - Prints information about only those areas that
            contain hard points.

        Notes
        -----
        An attribute (TYPE, MAT, REAL, or ESYS) listed as a zero is unassigned;
        one listed as a positive value indicates that the attribute was
        assigned with the AATT command (and will not be reset to zero if the
        mesh is cleared); one listed as a negative value indicates that the
        attribute was assigned using the attribute pointer [TYPE, MAT, REAL, or
        ESYS] that was active during meshing (and will be reset to zero if the
        mesh is cleared).  A "-1" in the "nodes" column indicates that the area
        has been meshed but there are no interior nodes.  The area size is
        listed only if an ASUM command has been performed on the area.
        """
        command = f"ALIST,{na1},{na2},{ninc},{lab}"
        return self.run(command, **kwargs)

    def anorm(self, anum="", noeflip="", **kwargs):
        """Reorients area normals.

        APDL Command: ANORM

        Parameters
        ----------
        anum
            Area number having the normal direction that the reoriented areas
            are to match.

        noeflip
            Indicates whether you want to change the normal direction of the
            existing elements on the reoriented area(s) so that they are
            consistent with each area's new normal direction.

            0 - Make the normal direction of existing elements on the reoriented area(s)
                consistent with each area's new normal direction (default).

            1 - Do not change the normal direction of existing elements on the reoriented
                area(s).

        Notes
        -----
        Reorients areas so that their normals are consistent with that of a
        specified area.

        If any of the areas have inner loops, the ANORM command will consider
        the inner loops when it reorients the area normals.

        You cannot use the ANORM command to change the normal direction of any
        element that has a body or surface load.  We recommend that you apply
        all of your loads only after ensuring that the element normal
        directions are acceptable.

        Real constants (such as nonuniform shell thickness and tapered beam
        constants) may be invalidated by an element reversal.

        See Revising Your Model of the Modeling and Meshing Guide for more
        information.
        """
        command = f"ANORM,{anum},{noeflip}"
        return self.run(command, **kwargs)

    def aoffst(self, narea="", dist="", kinc="", **kwargs):
        """Generates an area, offset from a given area.

        APDL Command: AOFFST

        Parameters
        ----------
        narea
            Area from which generated area is to be offset.  If NAREA = ALL,
            offset from all selected areas [ASEL].  If NAREA = P, graphical
            picking is enabled and all remaining arguments are ignored (valid
            only in the GUI).

        dist
            Distance normal to given area at which keypoints for generated area
            are to be located.  Positive normal is determined from the right-
            hand-rule keypoint order.

        kinc
            Keypoint increment between areas.  If zero, the lowest available
            keypoint numbers are assigned [NUMSTR].

        Notes
        -----
        Generates an area (and its corresponding keypoints and lines) offset
        from a given area.  The direction of the offset varies with the given
        area normal.  End slopes of the generated lines remain the same as
        those of the given pattern.  Area and line numbers are automatically
        assigned, beginning with the lowest available values [NUMSTR].
        """
        command = f"AOFFST,{narea},{dist},{kinc}"
        return self.run(command, **kwargs)

    def aplot(self, na1="", na2="", ninc="", degen="", scale="", **kwargs):
        """Displays the selected areas.

        APDL Command: APLOT

        Parameters
        ----------
        na1, na2, ninc
            Displays areas from NA1 to NA2 (defaults to NA1) in steps of NINC
            (defaults to 1).  If NA1 = ALL (default), NA2 and NINC are ignored
            and all selected areas [ASEL] are displayed.

        degen
            Degeneracy marker:

            (blank) - No degeneracy marker is used (default).

            DEGE - A red star is placed on keypoints at degeneracies (see the Modeling and Meshing
                   Guide ).  Not available if /FACET,WIRE is set.

        scale
            Scale factor for the size of the degeneracy-marker star.  The scale
            is the size in window space (-1 to 1 in both directions) (defaults
            to .075).

        Notes
        -----
        This command is valid in any processor.  The degree of tessellation
        used to plot the selected areas is set through the /FACET command.
        """
        command = f"APLOT,{na1},{na2},{ninc},{degen},{scale}"
        return self.run(command, **kwargs)

    def areverse(self, anum="", noeflip="", **kwargs):
        """Reverses the normal of an area, regardless of its connectivity or mesh

        APDL Command: AREVERSE
        status.

        Parameters
        ----------
        anum
            Area number of the area whose normal is to be reversed.  If ANUM =
            ALL, the normals of all selected areas will be reversed.  If ANUM =
            P, graphical picking is enabled.  A component name may also be
            substituted for ANUM.

        noeflip
            Indicates whether you want to change the normal direction of the
            existing elements on the reversed area(s) so that they are
            consistent with each area's new normal direction.

            0 - Make the normal direction of existing elements on the reversed area(s)
                consistent with each area's new normal direction (default).

            1 - Do not change the normal direction of existing elements on the reversed
                area(s).

        Notes
        -----
        You cannot use the AREVERSE command to change the normal direction of
        any element that has a body or surface load.  We recommend that you
        apply all of your loads only after ensuring that the element normal
        directions are acceptable. Also, you cannot use this command to change
        the normal direction for areas attached to volumes because IGES and ANF
        data is unchanged by reversal. Reversed areas that are attached to
        volumes need to be reversed again when imported.

        Real constants (such as nonuniform shell thickness and tapered beam
        constants) may be invalidated by an element reversal.

        See Revising Your Model in the Modeling and Meshing Guide for more
        information.
        """
        command = f"AREVERSE,{anum},{noeflip}"
        return self.run(command, **kwargs)

    def arotat(
        self,
        nl1="",
        nl2="",
        nl3="",
        nl4="",
        nl5="",
        nl6="",
        pax1="",
        pax2="",
        arc="",
        nseg="",
        **kwargs,
    ):
        """Generates cylindrical areas by rotating a line pattern about an axis.

        APDL Command: AROTAT

        Parameters
        ----------
        nl1, nl2, nl3, . . . , nl6
            List of lines in the pattern to be rotated (6 maximum if using
            keyboard entry of NL1 to NL6).  The lines must lie in the plane of
            the axis of rotation.  If NL1 = P, graphical picking is enabled and
            all remaining arguments are ignored (valid only in the GUI).  If
            NL1 = ALL, all selected lines will define the pattern to be
            rotated.  A component name may also be substituted for NL1.

        pax1, pax2
            Keypoints defining the axis about which the line pattern is to be
            rotated.

        arc
            Arc length (in degrees).  Positive follows right-hand rule about
            PAX1-PAX2 vector.  Defaults to 360°.

        nseg
            Number of areas (8 maximum) around circumference.  Defaults to
            minimum number required for 90° -maximum arcs, i.e., 4 for 360°, 3
            for 270°, etc.

        Notes
        -----
        Generates cylindrical areas (and their corresponding keypoints and
        lines) by rotating a line pattern (and its associated keypoint pattern)
        about an axis.  Keypoint patterns are generated at regular angular
        locations, based on a maximum spacing of 90°.  Line patterns are
        generated at the keypoint patterns.  Arc lines are also generated to
        connect the keypoints circumferentially.  Keypoint, line, and area
        numbers are automatically assigned, beginning with the lowest available
        values [NUMSTR].  Adjacent lines use a common keypoint.  Adjacent areas
        use a common line.
        """
        command = (
            f"AROTAT,{nl1},{nl2},{nl3},{nl4},{nl5},{nl6},{pax1},{pax2},{arc},{nseg}"
        )
        return self.run(command, **kwargs)

    def arscale(
        self,
        na1="",
        na2="",
        ninc="",
        rx="",
        ry="",
        rz="",
        kinc="",
        noelem="",
        imove="",
        **kwargs,
    ):
        """Generates a scaled set of areas from a pattern of areas.

        APDL Command: ARSCALE

        Parameters
        ----------
        na1, na2, ninc
            Set of areas, NA1 to NA2 in steps of NINC, that defines the pattern
            to be scaled.  NA2 defaults to NA1, NINC defaults to 1.  If NA1 =
            ALL, NA2 and NINC are ignored and the pattern is defined by all
            selected areas.  If NA1 = P, graphical picking is enabled and all
            remaining arguments are ignored (valid only in the GUI).  A
            component name may also be substituted for NA1 (NA2 and NINC are
            ignored).

        rx, ry, rz
            Scale factors to be applied to the X, Y, and Z keypoint coordinates
            in the active coordinate system.  (RR, R θ, RZ for cylindrical; RR,
            R θ, R Φ for spherical).  Note that the R θ and R Φ scale factors
            are interpreted as angular offsets.  For example, if CSYS = 1, RX,
            RY, RZ input of (1.5,10,3) would scale the specified keypoints 1.5
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

            0 - Nodes and elements associated with the original areas will be generated
                (scaled) if they exist.

            1 - Nodes and elements will not be generated.

        imove
            Specifies whether areas will be moved or newly defined:

            0 - Additional areas will be generated.

            1 - Original areas will be moved to new position (KINC and NOELEM are ignored).
                Use only if the old areas are no longer needed at their
                original positions.  Corresponding meshed items are also moved
                if not needed at their original position.

        Notes
        -----
        Generates a scaled set of areas (and their corresponding keypoints,
        lines, and mesh) from a pattern of areas.  The MAT, TYPE, REAL, and
        ESYS attributes are based on the areas in the pattern and not the
        current settings.  Scaling is done in the active coordinate system.
        Areas in the pattern could have been generated in any coordinate
        system.  However, solid modeling in a toroidal coordinate system is not
        recommended.
        """
        command = f"ARSCALE,{na1},{na2},{ninc},{rx},{ry},{rz},{kinc},{noelem},{imove}"
        return self.run(command, **kwargs)

    def arsym(
        self,
        ncomp="",
        na1="",
        na2="",
        ninc="",
        kinc="",
        noelem="",
        imove="",
        **kwargs,
    ):
        """Generates areas from an area pattern by symmetry reflection.

        APDL Command: ARSYM

        Parameters
        ----------
        ncomp
            Symmetry key:

            X - X symmetry (default).

            Y - Y symmetry.

            Z - Z symmetry.

        na1, na2, ninc
            Reflect areas from pattern beginning with NA1 to NA2 (defaults to
            NA1) in steps of NINC (defaults to 1).  If NA1 = ALL, NA2 and NINC
            are ignored and the pattern is all selected areas [ASEL].  If Ncomp
            = P, use graphical picking to specify areas and ignore NL2 and
            NINC.  A component name may also be substituted for NA1 (NA2 and
            NINC are ignored).

        kinc
            Keypoint increment between sets.  If zero, the lowest available
            keypoint numbers are assigned [NUMSTR].

        noelem
            Specifies whether nodes and elements are also to be generated:

            0 - Generate nodes and elements associated with the original areas, if they exist.

            1 - Do not generate nodes and elements.

        imove
            Specifies whether areas will be moved or newly defined:

            0 - Generate additional areas.

            1 - Move original areas to new position retaining the same keypoint numbers (KINC
                and NOELEM are ignored).  Valid only if the old areas are no
                longer needed at their original positions.  Corresponding
                meshed items are also moved if not needed at their original
                position.

        Notes
        -----
        Generates a reflected set of areas (and their corresponding keypoints,
        lines and mesh) from a given area pattern by a symmetry reflection (see
        analogous node symmetry command, NSYM).  The MAT, TYPE, REAL, ESYS, and
        SECNUM attributes are based upon the areas in the pattern and not upon
        the current settings.  Reflection is done in the active coordinate
        system by changing a particular coordinate sign.  The active coordinate
        system must be a Cartesian system.  Areas in the pattern may have been
        generated in any coordinate system.  However, solid modeling in a
        toroidal coordinate system is not recommended.  Areas are generated as
        described in the AGEN command.

        See the ESYM command for additional information about symmetry
        elements.
        """
        command = f"ARSYM,{ncomp},{na1},{na2},{ninc},{kinc},{noelem},{imove}"
        return self.run(command, **kwargs)

    def askin(
        self,
        nl1="",
        nl2="",
        nl3="",
        nl4="",
        nl5="",
        nl6="",
        nl7="",
        nl8="",
        nl9="",
        **kwargs,
    ):
        """Generates an area by "skinning" a surface through guiding lines.

        APDL Command: ASKIN

        Parameters
        ----------
        nl1
            The first guiding line forming the skinned area.  If NL1 = P,
            graphical picking is enabled and all remaining arguments are
            ignored (valid only in the GUI).  A component name may also be
            substituted for NL1.  If NL1 is negative, the line beginnings and
            ends will be used to direct the skinning of the remaining lines
            (see "Changing the ASKIN Algorithm" below).

        nl2, nl3, nl4, . . . , nl9
            The additional guiding lines for the skinned area (up to 9 total
            lines, including NL1, if using keyboard entry).  If negative (and
            NL1 is negative), the line beginning and end will be temporarily
            interchanged for the skinning operation (see "Changing the ASKIN
            Algorithm" below).

        Notes
        -----
        Generates an area by "skinning" a surface through specified guiding
        lines.  The lines act as a set of "ribs" over which a surface is
        "stretched."  Two opposite edges of the area are framed by the first
        (NL1) and last (NLn) guiding lines specified.  The other two edges of
        the area are framed by splines-fit lines which the program
        automatically generates through the ends of all guiding lines.  The
        interior of the area is shaped by the interior guiding lines.  Once the
        area has been created, only the four edge lines will be attached to it.
        In rare cases, it may be necessary to change the default algorithm used
        by the ASKIN command (see "Changing the ASKIN Algorithm" below).

        When skinning from one guiding line to the next, the program can create
        the transition area in one of two ways:  one more spiraled and one less
        spiraled ("flatter").  By default, the program attempts to produce the
        flatter transition, instead of the more spiraled transition.  This
        algorithm can be changed by inputting NL1 as a negative number, in
        which case the program connects all the keypoints at the line
        "beginnings" (/PSYMB,LDIR command) as one edge of the area, and all the
        line "ends" as the opposite edge, irrespective of the amount of
        spiraling produced in each transition area.

        To further control the geometry of the area (if NL1 is negative), the
        beginning and end of any specified line (other than NL1) can be
        temporarily interchanged (for the skinning operation only) by inputting
        that line number as negative.  See Solid Modeling in the Modeling and
        Meshing Guide for an illustration.
        """
        command = f"ASKIN,{nl1},{nl2},{nl3},{nl4},{nl5},{nl6},{nl7},{nl8},{nl9}"
        return self.run(command, **kwargs)

    def asub(self, na1="", p1="", p2="", p3="", p4="", **kwargs):
        """Generates an area using the shape of an existing area.

        APDL Command: ASUB

        Parameters
        ----------
        na1
            Existing area number whose shape is to be used.  If P1 = P,
            graphical picking is enabled and all remaining arguments are
            ignored (valid only in the GUI).

        p1
            Keypoint defining starting corner of area.

        p2
            Keypoint defining second corner of area.

        p3
            Keypoint defining third corner of area.

        p4
            Keypoint defining fourth corner of area (defaults to P3).

        Notes
        -----
        The new area will overlay the old area.  Often used when the area to be
        subdivided consists of a complex shape that was not generated in a
        single coordinate system.  Keypoints and any corresponding lines must
        lie on the existing area.  Missing lines are generated to lie on the
        given area.  The active coordinate system is ignored.
        """
        command = f"ASUB,{na1},{p1},{p2},{p3},{p4}"
        return self.run(command, **kwargs)

    def asum(self, lab="", **kwargs):
        """Calculates and prints geometry statistics of the selected areas.

        APDL Command: ASUM

        Parameters
        ----------
        lab
            Controls the degree of tessellation used in the calculation of area
            properties.  If LAB = DEFAULT, area calculations will use the
            degree of tessellation set through the /FACET command.  If LAB =
            FINE, area calculations are based on a finer tessellation.

        Notes
        -----
        Calculates and prints geometry statistics (area, centroid location,
        moments of inertia, volume, etc.) associated with the selected areas.
        ASUM should only be used on perfectly flat areas.

        Geometry items are reported in the global Cartesian coordinate system.
        A unit thickness is assumed unless the areas have a non-zero total
        thickness defined by real constant or section data.

        For layered areas, a unit density is always assumed. For single-layer
        areas, a unit density is assumed unless the areas have a valid material
        (density).

        The thickness and density are associated to the areas via the AATT
        command.

        Items calculated via ASUM and later retrieved via a ``*GET`` or ``*VGET``
        command are valid only if the model is not modified after issuing the
        ASUM command.

        Setting a finer degree of tessellation will provide area calculations
        with greater accuracy, especially for thin, hollow models.  However,
        using a finer degree of tessellation requires longer processing.

        For very narrow (sliver) areas, such that the ratio of the minimum to
        the maximum dimension is less than 0.01, the ASUM command can provide
        erroneous area information.  To ensure that the calculations are
        accurate, subdivide such areas so that the ratio of the minimum to the
        maximum is at least 0.05.
        """
        command = f"ASUM,{lab}"
        return self.run(command, **kwargs)

    def atran(
        self,
        kcnto="",
        na1="",
        na2="",
        ninc="",
        kinc="",
        noelem="",
        imove="",
        **kwargs,
    ):
        """Transfers a pattern of areas to another coordinate system.

        APDL Command: ATRAN

        Parameters
        ----------
        kcnto
            Reference number of coordinate system where the pattern is to be
            transferred.  Transfer occurs from the active coordinate system.
            The coordinate system type and parameters of KCNTO must be the same
            as the active system.

        na1, na2, ninc
            Transfer area pattern beginning with NA1 to NA2 (defaults to NA1)
            in steps of NINC (defaults to 1).  If NA1 = ALL, NA2 and NINC are
            ignored and the pattern is all selected areas [ASEL].  If NA1 = P,
            graphical picking is enabled and all remaining arguments are
            ignored (valid only in the GUI).  A component name may also be
            substituted for NA1 (NA2 and NINC are ignored).

        kinc
            Keypoint increment between sets.  If zero, the lowest available
            keypoint numbers are assigned [NUMSTR].

        noelem
            Specifies whether elements and nodes are also to be generated:

            0 - Generate nodes and elements associated with the original areas, if they exist.

            1 - Do not generate nodes and elements.

        imove
            Specifies whether to redefine the existing areas:

            0 - Generate additional areas.

            1 - Move original areas to new position retaining the same keypoint numbers (KINC
                and NOELEM are ignored).  Valid only if the old areas are no
                longer needed at their original positions.  Corresponding
                meshed items are also moved if not needed at their original
                position.

        Notes
        -----
        Transfers a pattern of areas (and their corresponding lines, keypoints
        and mesh) from one coordinate system to another (see analogous node
        TRANSFER command).  The MAT, TYPE, REAL, and ESYS attributes are based
        upon the areas in the pattern and not upon the current settings.
        Coordinate systems may be translated and rotated relative to each
        other.  Initial pattern may be generated in any coordinate system.
        However, solid modeling in a toroidal coordinate system is not
        recommended.  Coordinate and slope values are interpreted in the active
        coordinate system and are transferred directly.  Areas are generated as
        described in the AGEN command.
        """
        command = f"ATRAN,{kcnto},{na1},{na2},{ninc},{kinc},{noelem},{imove}"
        return self.run(command, **kwargs)

    def gsum(self, **kwargs):
        """Calculates and prints geometry items.

        APDL Command: GSUM

        Notes
        -----
        Calculates and prints geometry items (centroid location, moments of
        inertia, length, area, volume etc.) associated with the selected
        keypoints, lines, areas, and volumes. Geometry items are reported in
        the global Cartesian coordinate system.   For volumes, a unit density
        is assumed unless the volumes have a material association via the VATT
        command.  For areas, a unit density (and thickness) is assumed unless
        the areas have a material (and real constant) association via the AATT
        command.  For lines and keypoints, a unit density is assumed,
        irrespective of any material associations [LATT, KATT, MAT].  Items
        calculated by GSUM and later retrieved by a ``*GET`` or ``*VGET`` commands are
        valid only if the model is not modified after the GSUM command is
        issued.  This command combines the functions of the KSUM, LSUM, ASUM,
        and VSUM commands.
        """
        command = f"GSUM,"
        return self.run(command, **kwargs)

    def splot(self, na1="", na2="", ninc="", mesh="", **kwargs):
        """Displays the selected areas and a faceted view of their underlying

        APDL Command: SPLOT
        surfaces

        Parameters
        ----------
        na1
            Starting area for display of areas and underlying surfaces. If NA1
            = ALL (default), NA2 and NINC are ignored and all selected areas
            are displayed (ASEL command).

        na2
            Last area to be displayed.

        ninc
            Numeric value setting steps between NA1 and NA2 for display.
            Default value is (1).

        mesh
            Specifies a rectangular mesh density used to display the underlying
            surface (default 4, i.e. 4 x 4).

        Notes
        -----
        This command is valid in any processor. The plot output displays the
        external and internal trim curves and underlying surface. You cannot
        obtain a faceted view of your surface areas when you are using the
        /EXPAND command to create larger graphics displays.

        Use APLOT for trimmed surface display.
        """
        command = f"SPLOT,{na1},{na2},{ninc},{mesh}"
        return self.run(command, **kwargs)
