from typing import Optional, Union

from ansys.mapdl.core._commands import parse
from ansys.mapdl.core.mapdl_types import MapdlInt


class Volumes:
    def extopt(
        self,
        lab: str = "",
        val1: Union[str, int] = "",
        val2: Union[str, int] = "",
        val3: MapdlInt = "",
        val4: MapdlInt = "",
        **kwargs,
    ) -> Optional[str]:
        """Controls options relating to the generation of volume elements from area elements.

        APDL Command: EXTOPT

        Parameters
        ----------
        lab
            Label identifying the control option. The meanings of
            Val1, Val2, and Val3 will vary depending on Lab.

            ON - Sets carryover of the material attributes, real
                 constant attributes, and element coordinate system
                 attributes of the pattern area elements to the
                 generated volume elements.  Sets the pattern
                 area mesh to clear when volume generations are done.
                 Val1, Val2, and Val3 are ignored.

            OFF - Removes all settings associated with this command.
                  Val1, Val2, and Val3 are ignored.

            STAT - Shows all settings associated with this command.
                   Val1, Val2, Val3, and Val4 are ignored.

            ATTR - Sets carryover of particular pattern area attributes
                   (materials, real constants, and element coordinate
                   systems) of the pattern area elements to the
                   generated volume elements. (See 2.) Val1 can be:

                0 - Sets volume elements to use
                    current MAT command settings.

                1 - Sets volume elements to use material
                    attributes of the pattern area elements.

            Val2 can be:

                0 - Sets volume elements to use current REAL
                    command settings.

                1 - Sets volume elements to use real constant attributes
                    of the pattern area elements.

            Val3 can be:

                0 - Sets volume elements to use current ESYS command
                    settings.

                1 - Sets volume elements to use element coordinate
                    system attributes of the pattern area elements.

            Val4 can be:

                0 - Sets volume elements to use current SECNUM command
                    settings.

                1 - Sets volume elements to use section attributes of
                    the pattern area elements.

            ESIZE - Val1 sets the number of element divisions in the
                    direction of volume generation or volume sweep.
                    For VDRAG and VSWEEP, Val1 is overridden by the
                    LESIZE command NDIV setting. Val2 sets the spacing
                    ratio (bias) in the direction of volume generation
                    or volume sweep. If positive, Val2 is the nominal
                    ratio of last division size to first division size
                    (if > 1.0, sizes increase, if < 1.0, sizes
                    decrease). If negative, Val2 is the nominal ratio of
                    center division(s) size to end divisions size. Ratio
                    defaults to 1.0 (uniform spacing).
                    Val3 and Val4 are ignored.

            ACLEAR - Sets clearing of pattern area mesh.
                     (See 3.) Val1 can be:

                0 - Sets pattern area to remain meshed when volume
                    generation is done.

                1 - Sets pattern area mesh to clear when volume
                    generation is done. Val2, Val3, and Val4 are
                    ignored.

            VSWE - Indicates that volume sweeping options will be set
                   using Val1 and Val2. Settings specified with EXTOPT,
                   VSWE will be used the next time the VSWEEP command
                   is invoked. If Lab = VSWE, Val1 becomes a label.
                   Val1 can be:

            AUTO - Indicates whether you will be prompted for the source
                   and target used by VSWEEP or if VSWE should
                   automatically determine the source and target.
                   If Val1 = AUTO, Val2 is ON by default. VSWE will
                   automatically determine the source and target for
                   VSWEEP. You will be allowed to pick more than one
                   volume for sweeping. When Val2 = OFF, the user will
                   be prompted for the source and target for VSWEEP.
                   You will only be allowed to pick one volume for
                   sweeping.

            TETS - Indicates whether VSWEEP will tet mesh non-sweepable
                   volumes or leave them unmeshed. If Val1 = TETS,
                   Val2 is OFF by default. Non-sweepable volumes will be
                   left unmeshed. When Val2 = ON, the non-sweepable
                   volumes will be tet meshed if the assigned element
                   type supports tet shaped elements.

        val1, val2, val3, val4
            Additional input values as described under each option for
            Lab.

        Notes
        -----
        EXTOPT controls options relating to the generation of volume
        elements from pattern area elements using the VEXT, VROTAT,
        VOFFST, VDRAG, and VSWEEP commands.  (When using VSWEEP,
        the pattern area is referred to as the source area.)

        Enables carryover of the attributes  of the pattern area
        elements to the generated volume elements when you are using
        VEXT, VROTAT, VOFFST, or VDRAG. (When using VSWEEP, since the
        volume already exists, use the VATT command to assign attributes
        before sweeping.)

        When you are using VEXT, VROTAT, VOFFST, or VDRAG, enables
        clearing of the pattern area mesh when volume generations are
        done. (When you are using VSWEEP, if selected, the area meshes
        on the pattern (source), target, and/or side areas clear when
        volume sweeping is done.)

        Neither EXTOPT,VSWE,AUTO nor EXTOPT,VSWE,TETS will be affected
        by EXTOPT,ON or EXTOPT, OFF.
        """
        command = f"EXTOPT,{lab},{val1},{val2},{val3},{val4}"
        return self.run(command, **kwargs)

    def v(
        self, p1="", p2="", p3="", p4="", p5="", p6="", p7="", p8="", **kwargs
    ) -> int:
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

        """
        command = f"V,{p1},{p2},{p3},{p4},{p5},{p6},{p7},{p8}"
        return parse.parse_v(self.run(command, **kwargs))

    def va(
        self,
        a1="",
        a2="",
        a3="",
        a4="",
        a5="",
        a6="",
        a7="",
        a8="",
        a9="",
        a10="",
        **kwargs,
    ) -> int:
        """Generate a volume bounded by existing areas.

        APDL Command: VA

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

        Notes
        -----
        This command conveniently allows generating volumes from
        regions having more than eight keypoints (which is not allowed
        with the V command).  Areas may be input in any order.  The
        exterior surface of a VA volume must be continuous, but holes
        may pass completely through it.

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

        """
        command = f"VA,{a1},{a2},{a3},{a4},{a5},{a6},{a7},{a8},{a9},{a10}"
        return parse.parse_v(self.run(command, **kwargs))

    def vdele(self, nv1="", nv2="", ninc="", kswp="", **kwargs):
        """Deletes unmeshed volumes.

        APDL Command: VDELE

        Parameters
        ----------
        nv1, nv2, ninc
            Delete volumes from NV1 to NV2 (defaults to NV1) in steps of NINC
            (defaults to 1).  If NV1 = ALL, NV2 and NINC are ignored and all
            selected volumes [VSEL] are deleted.  If NV1 = P, graphical picking
            is enabled and all remaining command fields are ignored (valid only
            in the GUI).  A component name may also be substituted for NV1 (NV2
            and NINC are ignored).

        kswp
            Specifies whether keypoints, lines, and areas are also deleted:

            0 - Delete volumes only (default).

            1 - Delete volumes, as well as keypoints, lines, and areas attached to the
                specified volumes but not shared by other volumes.
        """
        command = f"VDELE,{nv1},{nv2},{ninc},{kswp}"
        return self.run(command, **kwargs)

    def vdgl(self, nv1="", nv2="", ninc="", **kwargs):
        """Lists keypoints of a volume that lie on a parametric degeneracy.

        APDL Command: VDGL

        Parameters
        ----------
        nv1, nv2, ninc
            List keypoints that lie on a parametric degeneracy on volumes from
            NV1 to NV2 (defaults to NV1) in steps of NINC (defaults to 1).  If
            NV1 = ALL (default), NV2 and NINC will be ignored and keypoints on
            all selected volumes [VSEL] will be listed.  If NV1 = P, graphical
            picking is enabled and all remaining command fields are ignored
            (valid only in the GUI).  You may also substitute a component name
            for NV1 (ignore NV2 and NINC).

        Notes
        -----
        See the Modeling and Meshing Guide for details about parametric
        degeneracies.

        This command is valid in any processor.
        """
        command = f"VDGL,{nv1},{nv2},{ninc}"
        return self.run(command, **kwargs)

    def vdrag(
        self,
        na1="",
        na2="",
        na3="",
        na4="",
        na5="",
        na6="",
        nlp1="",
        nlp2="",
        nlp3="",
        nlp4="",
        nlp5="",
        nlp6="",
        **kwargs,
    ) -> str:
        """Generate volumes by dragging an area pattern along a path.

        APDL Command: VDRAG

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

        """
        command = f"VDRAG,{na1},{na2},{na3},{na4},{na5},{na6},{nlp1},{nlp2},{nlp3},{nlp4},{nlp5},{nlp6}"
        return self.run(command, **kwargs)

    def vext(
        self,
        na1="",
        na2="",
        ninc="",
        dx="",
        dy="",
        dz="",
        rx="",
        ry="",
        rz="",
        **kwargs,
    ) -> str:
        """Generate additional volumes by extruding areas.

        APDL Command: VEXT

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

        """
        command = f"VEXT,{na1},{na2},{ninc},{dx},{dy},{dz},{rx},{ry},{rz}"
        return self.run(command, **kwargs)

    def vgen(
        self,
        itime="",
        nv1="",
        nv2="",
        ninc="",
        dx="",
        dy="",
        dz="",
        kinc="",
        noelem="",
        imove="",
        **kwargs,
    ):
        """Generates additional volumes from a pattern of volumes.

        APDL Command: VGEN

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

        .. warning::
           Use of the VEXT command can produce unexpected results when
           operating in a non-Cartesian coordinate system.  For a
           detailed description of the possible problems that may
           occur, see Solid Modeling in the Modeling and Meshing
           Guide.

        Parameters
        ----------
        itime
            Do this generation operation a total of ITIMEs, incrementing all
            keypoints in the given pattern automatically (or by KINC) each time
            after the first.  ITIME must be > 1 for generation to occur.

        nv1, nv2, ninc
            Generate volumes from pattern beginning with NV1 to NV2 (defaults
            to NV1) in steps of NINC (defaults to 1).  If NV1 = ALL, NV2 and
            NINC are ignored and the pattern is all selected volumes [VSEL].
            If NV1 = P, graphical picking is enabled and all remaining command
            fields are ignored (valid only in the GUI).  A component name may
            also be substituted for NV1 (NV2 and NINC are ignored).

        dx, dy, dz
            Keypoint location increments in the active coordinate system (--,
            Dθ, DZ for cylindrical, --, Dθ, -- for spherical).

        kinc
            Keypoint increment between generated sets.  If zero, the lowest
            available keypoint numbers are assigned [NUMSTR].

        noelem
            Specifies if elements and nodes are also to be generated:

            0 - Generate nodes and elements associated with the original volumes, if they
                exist.

            1 - Do not generate nodes and elements.

        imove
            Specifies whether to redefine the existing volumes:

            0 - Generate additional volumes as requested with the ITIME argument.

            1 - Move original volumes to new position retaining the same keypoint line, and
                area numbers (ITIME, KINC, and NOELEM are ignored).
                Corresponding meshed items are also moved if not needed at
                their original position.

        Notes
        -----
        Generates additional volumes (and their corresponding keypoints, lines,
        areas and mesh) from a given volume pattern.  The MAT, TYPE, REAL, and
        ESYS attributes are based upon the volumes in the pattern and not upon
        the current settings of the pointers.  End slopes of the generated
        lines remain the same (in the active coordinate system) as those of the
        given pattern.  For example, radial slopes remain radial, etc.
        Generations which produce volumes of a size or shape different from the
        pattern (i.e., radial generations in cylindrical systems, radial and
        phi generations in spherical systems, and theta generations in
        elliptical systems) are not allowed.  Note that solid modeling in a
        toroidal coordinate system is not recommended.  Volume, area, and line
        numbers are automatically assigned (beginning with the lowest available
        values [NUMSTR]).
        """
        command = (
            f"VGEN,{itime},{nv1},{nv2},{ninc},{dx},{dy},{dz},{kinc},{noelem},{imove}"
        )
        return self.run(command, **kwargs)

    def vlist(self, nv1="", nv2="", ninc="", **kwargs):
        """Lists the defined volumes.

        APDL Command: VLIST

        Parameters
        ----------
        nv1, nv2, ninc
            List volumes from NV1 to NV2 (defaults to NV1) in steps of NINC
            (defaults to 1).  If NV1 = ALL (default), NV2 and NINC are ignored
            and all selected volumes [VSEL] are listed.  If NV1 = P, graphical
            picking is enabled and all remaining command fields are ignored
            (valid only in the GUI).  A component name may also be substituted
            for NV1 (NV2 and NINC are ignored).

        Notes
        -----
        An attribute (TYPE, MAT, REAL, or ESYS) listed as a zero is unassigned;
        one listed as a positive value indicates that the attribute was
        assigned with the VATT command (and will not be reset to zero if the
        mesh is cleared); one listed as a negative value indicates that the
        attribute was assigned using the attribute pointer [TYPE, MAT, REAL, or
        ESYS] that was active during meshing (and will be reset to zero if the
        mesh is cleared).  A "-1" in the "nodes" column indicates that the
        volume has been meshed but there are no interior nodes.  The volume
        size is listed only if a VSUM command has been performed on the volume.
        Volume orientation attributes (KZ1 and KZ2) are listed only if a
        VEORIENT command was previously used to define an orientation for the
        volume.

        This command is valid in any processor.
        """
        command = f"VLIST,{nv1},{nv2},{ninc}"
        return self.run(command, **kwargs)

    def vlscale(
        self,
        nv1="",
        nv2="",
        ninc="",
        rx="",
        ry="",
        rz="",
        kinc="",
        noelem="",
        imove="",
        **kwargs,
    ):
        """Generates a scaled set of volumes from a pattern of volumes.

        APDL Command: VLSCALE

        Parameters
        ----------
        nv1, nv2, ninc
            Set of volumes (NV1 to NV2 in steps of NINC) that defines the
            pattern to be scaled.  NV2 defaults to NV1, NINC defaults to 1.  If
            NV1 = ALL, NV2 and NINC are ignored and the pattern is defined by
            all selected volumes.  If NV1 = P, graphical picking is enabled and
            all remaining command fields are ignored (valid only in the GUI).
            A component name may also be substituted for NV1 (NV2 and NINC are
            ignored).

        rx, ry, rz
            Scale factors to be applied to the X, Y, and Z keypoint coordinates
            in active coordinate system (RR, Rθ, RZ for cylindrical; RR, Rθ, RΦ
            for spherical).  Note that the Rθ and RΦ scale factors are
            interpreted as angular offsets.  For example, if CSYS = 1, RX, RY,
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

            0 - Nodes and elements associated with the original volumes will be generated
                (scaled) if they exist.

            1 - Nodes and elements will not be generated.

        imove
            Specifies whether volumes will be moved or newly defined:

            0 - Additional volumes will be generated.

            1 - Original volumes will be moved to new position (KINC and NOELEM are ignored).
                Use only if the old volumes are no longer needed at their
                original positions.  Corresponding meshed items are also moved
                if not needed at their original position.

        Notes
        -----
        Generates a scaled set of volumes (and their corresponding keypoints,
        lines, areas,  and mesh) from a pattern of volumes.  The MAT, TYPE,
        REAL, and ESYS attributes are based on the volumes in the pattern and
        not the current settings.  Scaling is done in the active coordinate
        system.  Volumes in the pattern could have been generated in any
        coordinate system.  However, solid modeling in a toroidal coordinate
        system is not recommended.
        """
        command = f"VLSCALE,{nv1},{nv2},{ninc},{rx},{ry},{rz},{kinc},{noelem},{imove}"
        return self.run(command, **kwargs)

    def voffst(self, narea="", dist="", kinc="", **kwargs):
        """Generates a volume, offset from a given area.

        APDL Command: VOFFST

        Parameters
        ----------
        narea
            Area from which generated volume is to be offset.  If NAREA = P,
            graphical picking is enabled and all remaining command fields are
            ignored (valid only in the GUI).

        dist
            Distance normal to given area at which keypoints for generated
            volume are to be located.  Positive normal is determined from the
            right-hand rule keypoint order.

        kinc
            Increment to be applied to the keypoint numbers between sets.  If
            zero, keypoint numbers will be automatically assigned beginning
            with the lowest available value [NUMSTR].

        Notes
        -----
        Generates a volume (and its corresponding keypoints, lines, and areas)
        by offsetting from an area.  The direction of the offset varies with
        the given area normal.  End slopes of the generated lines remain the
        same as those of the given pattern.

        If element attributes have been associated with the input area via the
        AATT command, the opposite area generated by the VOFFST operation will
        also have those attributes (i.e., the element attributes from the input
        area are copied to the opposite area).  Note that only the area
        opposite the input area will have the same attributes as the input
        area; the areas adjacent to the input area will not.

        If the areas are meshed or belong to meshed volumes, a 3-D mesh can be
        extruded with this command.  Note that the NDIV argument on the ESIZE
        command should be set before extruding the meshed areas.
        """
        command = f"VOFFST,{narea},{dist},{kinc}"
        return self.run(command, **kwargs)

    def vplot(self, nv1="", nv2="", ninc="", degen="", scale="", **kwargs):
        """Displays the selected volumes.

        APDL Command: VPLOT

        Parameters
        ----------
        nv1, nv2, ninc
            Display volumes from NV1 to NV2 (defaults to NV1) in steps of NINC
            (defaults to 1).  If NV1 = ALL (default), NV2 and NINC are ignored
            and all selected volumes [VSEL] are displayed.

        degen
            Degeneracy marker:

            (blank) - No degeneracy marker is used (default).

            DEGE - A red star is placed on keypoints at degeneracies (see the Modeling and Meshing
                   Guide).  Not available if /FACET,WIRE is set.

        scale
            Scale factor for the size of the degeneracy-marker star.  The scale
            is the size in window space (-1 to 1 in both directions) (defaults
            to .075).

        Notes
        -----
        Displays selected volumes.  (Only volumes having areas within the
        selected area set [ASEL] will be plotted.)  With PowerGraphics on
        [/GRAPHICS,POWER], VPLOT will display only the currently selected
        areas. This command is also a utility command, valid anywhere.  The
        degree of tessellation used to plot the volumes is set through the
        /FACET command.
        """
        command = f"VPLOT,{nv1},{nv2},{ninc},{degen},{scale}"
        return self.run(command, **kwargs)

    def vrotat(
        self,
        na1="",
        na2="",
        na3="",
        na4="",
        na5="",
        na6="",
        pax1="",
        pax2="",
        arc="",
        nseg="",
        **kwargs,
    ) -> str:
        """Generate cylindrical volumes by rotating an area pattern about an axis.

        APDL Command: VROTAT

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

        """
        command = (
            f"VROTAT,{na1},{na2},{na3},{na4},{na5},{na6},{pax1},{pax2},{arc},{nseg}"
        )
        return self.run(command, **kwargs)

    def vsum(self, lab="", **kwargs):
        """Calculates and prints geometry statistics of the selected volumes.

        APDL Command: VSUM

        Parameters
        ----------
        lab
            Controls the degree of tessellation used in the calculation of area
            properties.  If LAB = DEFAULT, area calculations will use the
            degree of tessellation set through the /FACET command.  If LAB =
            FINE, area calculations are based on a finer tessellation.

        Notes
        -----
        Calculates and prints geometry statistics (volume, centroid location,
        moments of inertia, etc.) associated with the selected volumes.
        Geometry items are reported in the global Cartesian coordinate system.
        A unit density is assumed unless the volumes have a material
        association via the VATT command.  Items calculated by VSUM and later
        retrieved by a ``*GET`` or ``*VGET`` command are valid only if the model is not
        modified after the VSUM command is issued.

        Setting a finer degree of tessellation will provide area calculations
        with greater accuracy, especially for thin, hollow models.  However,
        using a finer degree of tessellation requires longer processing.

        For very thin volumes, such that the ratio of the minimum to the
        maximum dimension is less than 0.01, the VSUM command can provide
        erroneous volume information.  To ensure that such calculations are
        accurate, make certain that you subdivide such volumes so that the
        ratio of the minimum to the maximum is at least 0.05.
        """
        command = f"VSUM,{lab}"
        return self.run(command, **kwargs)

    def vsymm(
        self,
        ncomp="",
        nv1="",
        nv2="",
        ninc="",
        kinc="",
        noelem="",
        imove="",
        **kwargs,
    ) -> str:
        """Generate volumes from a volume pattern by symmetry reflection.

        APDL Command: VSYMM

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

        """
        command = f"VSYMM,{ncomp},{nv1},{nv2},{ninc},{kinc},{noelem},{imove}"
        return self.run(command, **kwargs)

    def vtran(
        self,
        kcnto="",
        nv1="",
        nv2="",
        ninc="",
        kinc="",
        noelem="",
        imove="",
        **kwargs,
    ):
        """Transfers a pattern of volumes to another coordinate system.

        APDL Command: VTRAN

        Parameters
        ----------
        kcnto
            Reference number of coordinate system where the pattern is to be
            transferred.  Transfer occurs from the active coordinate system.
            The coordinate system type and parameters of KCNTO must be the same
            as the active system.

        nv1, nv2, ninc
            Transfer volumes from pattern beginning with NV1 to NV2 (defaults
            to NV1) in steps of NINC (defaults to 1).  If NV1 = ALL, NV2 and
            NINC are ignored and the pattern is all selected volumes [VSEL].
            If NV1 = P, graphical picking is enabled and all remaining command
            fields are ignored (valid only in the GUI).  A component name may
            also be substituted for NV1 (NV2 and NINC are ignored).

        kinc
            Keypoint increment between sets.  If zero, the lowest available
            keypoint numbers are assigned [NUMSTR].

        noelem
            Specifies whether elements and nodes are also to be generated:

            0 - Generate nodes and elements associated with the original volumes, if they
                exist.

            1 - Do not generate nodes and elements.

        imove
            Specifies whether to redefine the existing volumes:

            0 - Generate additional volumes.

            1 - Move original volumes to new position retaining the same keypoint numbers (KINC
                and NOELEM are ignored).  Corresponding meshed items are also
                moved if not needed at their original position.

        Notes
        -----
        Transfers a pattern of volumes (and their corresponding keypoints,
        lines, areas and mesh) from one coordinate system to another (see
        analogous node transfer command, TRANSFER).  The MAT, TYPE, REAL, and
        ESYS attributes are based upon the volumes in the pattern and not upon
        the current settings.  Coordinate systems may be translated and rotated
        relative to each other.  Initial pattern may be generated in any
        coordinate system.  However, solid modeling in a toroidal coordinate
        system is not recommended.  Coordinate and slope values are interpreted
        in the active coordinate system and are transferred directly.  Volumes
        are generated as described in the VGEN command.
        """
        command = f"VTRAN,{kcnto},{nv1},{nv2},{ninc},{kinc},{noelem},{imove}"
        return self.run(command, **kwargs)
