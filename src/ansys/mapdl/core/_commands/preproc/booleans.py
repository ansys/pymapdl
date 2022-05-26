from ansys.mapdl.core._commands import parse


class Booleans:
    def aadd(
        self,
        na1="",
        na2="",
        na3="",
        na4="",
        na5="",
        na6="",
        na7="",
        na8="",
        na9="",
        **kwargs,
    ):
        """Adds separate areas to create a single area.

        APDL Command: AADD

        Parameters
        ----------
        na1, na2, na3, . . . , na9
            Numbers of areas to be added.  If NA1 = ALL, add all selected areas
            and ignore NA2 to NA9.  If NA1 = P, graphical picking is enabled
            and all remaining arguments are ignored (valid only in the GUI).  A
            component name may also be substituted for NA1.

        Notes
        -----
        The areas must be coplanar.  The original areas (and their
        corresponding lines and keypoints) will be deleted by default.
        See the BOPTN command for the options available to Boolean
        operations.  Element attributes and solid model boundary
        conditions assigned to the original entities will not be
        transferred to the new entities generated.  Concatenated entities
        are not valid with this command.

        Examples
        --------
        Generate two areas and combine them.

        >>> a1 = mapdl.rectng(2.5, 3.5, 0, 10)
        >>> a2 = mapdl.cyl4(0, 10, 2.5, 0, 3.5, 90)
        >>> a_comb = mapdl.aadd(a1, a2)
        >>> a_comb
        3

        """
        command = f"AADD,{na1},{na2},{na3},{na4},{na5},{na6},{na7},{na8},{na9}"
        return parse.parse_output_areas(self.run(command, **kwargs))

    def aglue(
        self,
        na1="",
        na2="",
        na3="",
        na4="",
        na5="",
        na6="",
        na7="",
        na8="",
        na9="",
        **kwargs,
    ):
        """Generates new areas by "gluing" areas.

        APDL Command: AGLUE

        Parameters
        ----------
        na1, na2, na3, . . . , na9
            Numbers of the areas to be glued.  If NA1 = ALL, all selected areas
            will be glued (NA2 to NA9 will be ignored).  If NA1 = P, graphical
            picking is enabled and all remaining arguments are ignored (valid
            only in the GUI).  A component name may also be substituted for
            NA1.

        Notes
        -----
        Use of the AGLUE command generates new areas by "gluing" input areas.
        The glue operation redefines the input areas so that they share lines
        along their common boundaries.  The new areas encompass the same
        geometry as the original areas.  This operation is only valid if the
        intersection of the input areas are lines along the boundaries of those
        areas.  See the Modeling and Meshing Guide for an illustration.  See
        the BOPTN command for an explanation of the options available to
        Boolean operations.  Element attributes and solid model boundary
        conditions assigned to the original entities will not be transferred to
        new entities generated.

        The AGLUE command results in the merging of lines and keypoints at the
        common area boundaries. The lines and keypoints of the lower numbered
        area will be kept. This means one must be aware of area numbering when
        multiple AGLUE commands are applied to avoid any "ungluing" of
        geometry.
        """
        command = f"AGLUE,{na1},{na2},{na3},{na4},{na5},{na6},{na7},{na8},{na9}"
        return self.run(command, **kwargs)

    def aina(
        self,
        na1="",
        na2="",
        na3="",
        na4="",
        na5="",
        na6="",
        na7="",
        na8="",
        na9="",
        **kwargs,
    ):
        """Finds the intersection of areas.

        APDL Command: AINA

        Parameters
        ----------
        na1, na2, na3, . . . , na9
            Numbers of areas to be intersected.  If NA1 = ALL, NA2 to NA9 are
            ignored and the intersection of all selected areas is found.  If
            NA1 = P, graphical picking is enabled and all remaining arguments
            are ignored (valid only in the GUI).  A component name may also be
            substituted for NA1.

        Notes
        -----
        Finds the common (not pairwise) intersection of areas.  The common
        intersection is defined as the regions shared (in common) by all areas
        listed on this command.  New areas will be generated where the original
        areas intersect.  If the regions of intersection are only lines, new
        lines will be generated instead.  See the Modeling and Meshing Guide
        for an illustration.  See the BOPTN command for the options available
        to Boolean operations.  Element attributes and solid model boundary
        conditions assigned to the original entities will not be transferred to
        the new entities generated.
        """
        command = f"AINA,{na1},{na2},{na3},{na4},{na5},{na6},{na7},{na8},{na9}"
        return self.run(command, **kwargs)

    def ainp(
        self,
        na1="",
        na2="",
        na3="",
        na4="",
        na5="",
        na6="",
        na7="",
        na8="",
        na9="",
        **kwargs,
    ):
        """Finds the pairwise intersection of areas.

        APDL Command: AINP

        Parameters
        ----------
        na1, na2, na3, . . . , na9
            Numbers of areas to be intersected pairwise.  If NA1 = ALL, NA2 to
            NA9 are ignored and the pairwise intersection of all selected areas
            is found.  If NA1 = P, graphical picking is enabled and all
            remaining arguments are ignored (valid only in the GUI).  A
            component name may be substituted for NA1.

        Notes
        -----
        Finds the pairwise intersection of areas.  The pairwise intersection is
        defined as all regions shared by any two or more areas listed on this
        command.  New areas will be generated where the original areas
        intersect pairwise.  If the regions of pairwise intersection are only
        lines, new lines will be generated.  See the Modeling and Meshing Guide
        for an illustration.  See the BOPTN command for the options available
        to Boolean operations.  Element attributes and solid model boundary
        conditions assigned to the original entities will not be transferred to
        the new entities generated.
        """
        command = f"AINP,{na1},{na2},{na3},{na4},{na5},{na6},{na7},{na8},{na9}"
        return self.run(command, **kwargs)

    def ainv(self, na="", nv="", **kwargs):
        """Finds the intersection of an area with a volume.

        APDL Command: AINV

        Parameters
        ----------
        na
            Number of area to be intersected.  If P, graphical picking is
            enabled and all remaining arguments are ignored (valid only in the
            GUI).

        nv
            Number of volume to be intersected.

        Notes
        -----
        New areas will be generated where the areas intersect the volumes.  If
        the regions of intersection are only lines, new lines will be generated
        instead.  See the Modeling and Meshing Guide for an illustration.  See
        the BOPTN command for the options available to Boolean operations.
        Element attributes and solid model boundary conditions assigned to the
        original entities will not be transferred to the new entities
        generated.
        """
        command = f"AINV,{na},{nv}"
        return self.run(command, **kwargs)

    def aovlap(
        self,
        na1="",
        na2="",
        na3="",
        na4="",
        na5="",
        na6="",
        na7="",
        na8="",
        na9="",
        **kwargs,
    ):
        """Overlaps areas.

        APDL Command: AOVLAP

        Parameters
        ----------
        na1, na2, na3, . . . , na9
            Numbers of areas to be operated on.  If NA1 = ALL, use all selected
            areas and ignore NA2 to NA9.  If NA1 = P, graphical picking is
            enabled and all remaining arguments are ignored (valid only in the
            GUI).  A component name may also be substituted for NA1.

        Notes
        -----
        Generates new areas which encompass the geometry of all the input
        areas. The new areas are defined by the regions of intersection of the
        input areas, and by the complementary (non-intersecting) regions.  See
        Solid Modeling in the Modeling and Meshing Guide for an illustration.
        This operation is only valid when the region of intersection is an
        area.  See the BOPTN command for an explanation of the options
        available to Boolean operations.  Element attributes and solid model
        boundary conditions assigned to the original entities will not be
        transferred to the new entities generated.
        """
        command = f"AOVLAP,{na1},{na2},{na3},{na4},{na5},{na6},{na7},{na8},{na9}"
        return self.run(command, **kwargs)

    def aptn(
        self,
        na1="",
        na2="",
        na3="",
        na4="",
        na5="",
        na6="",
        na7="",
        na8="",
        na9="",
        **kwargs,
    ):
        """Partitions areas.

        APDL Command: APTN

        Parameters
        ----------
        na1, na2, na3, . . . , na9
            Numbers of areas to be operated on.  If NA1 = ALL, NA2 to NA9 are
            ignored and all selected areas are used.  If NA1 = P, graphical
            picking is enabled and all remaining arguments are ignored (valid
            only in the GUI).  A component name may be substituted for NA1.

        Notes
        -----
        Partitions areas that intersect.  This command is similar to the
        combined functionality of the ASBA and AOVLAP commands.  If the
        intersection of two or more areas is an area (i.e., planar), new areas
        will be created with boundaries that conform to the area of
        intersection and to the boundaries of the non-intersecting portions of
        the input areas [AOVLAP].  If the intersection is a line (i.e., not
        planar), the areas will be subtracted, or divided, along the line(s) of
        intersection [ASBA].  Both types of intersection can occur during a
        single APTN operation.  Areas that do not intersect will not be
        modified.  See the Modeling and Meshing Guide for an illustration.  See
        the BOPTN command for an explanation of the options available to
        Boolean operations.  Element attributes and solid model boundary
        conditions assigned to the original entities will not be transferred to
        the new entities generated.
        """
        command = f"APTN,{na1},{na2},{na3},{na4},{na5},{na6},{na7},{na8},{na9}"
        return self.run(command, **kwargs)

    def asba(self, na1="", na2="", sepo="", keep1="", keep2="", **kwargs) -> int:
        """Subtracts areas from areas.

        APDL Command: ASBA

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

        """
        command = f"ASBA,{na1},{na2},{sepo},{keep1},{keep2}"
        return parse.parse_output_volume_area(self.run(command, **kwargs))

    def asbl(self, na="", nl="", keepa="", keepl="", **kwargs):
        """Subtracts lines from areas.

        APDL Command: ASBL

        Parameters
        ----------
        na
            Area (or areas, if picking is used) to be subtracted from.  If ALL,
            use all selected areas.  If P, graphical picking is enabled (valid
            only in the GUI) and remaining fields are ignored.  A component
            name may also be substituted for NA.

        nl
            Line (or lines, if picking is used) to subtract.  If ALL, use all
            selected lines.    A component name may also be substituted for NL.

        keepa
            Specifies whether NA areas are to be deleted:

            (blank) - Use the setting of KEEP on the BOPTN command.

            DELETE - Delete NA areas after ASBL operation (override BOPTN command settings).

            KEEP - Keep NA areas after ASBL operation (override BOPTN command settings).

        keepl
            Specifies whether NL lines are to be deleted:

            (blank) - Use the setting of KEEP on the BOPTN command.

            DELETE - Delete NL lines after ASBL operation (override BOPTN command settings).

            KEEP - Keep NL lines after ASBL operation (override BOPTN command settings).

        Notes
        -----
        Generates new areas by subtracting the regions common to both the areas
        and lines (the intersection) from the NA areas.  The intersection will
        be a line(s).  See Solid Modeling in the Modeling and Meshing Guide for
        an illustration.  See the BOPTN command for an explanation of the
        options available to Boolean operations.  Element attributes and solid
        model boundary conditions assigned to the original entities will not be
        transferred to the new entities generated.
        """
        command = f"ASBL,{na},{nl},{keepa},{keepl}"
        return self.run(command, **kwargs)

    def asbv(self, na="", nv="", sepo="", keepa="", keepv="", **kwargs):
        """Subtracts volumes from areas.

        APDL Command: ASBV

        Parameters
        ----------
        na
            Area (or areas, if picking is used) to be subtracted from.  If ALL,
            use all selected areas.  If P, graphical picking is enabled (valid
            only in the GUI) and remaining fields are ignored.  A component
            name may also be substituted for NA.

        nv
            Volume (or volumes, if picking is used) to subtract.  If ALL, use
            all selected volumes.  A component name may also be substituted for
            NV.

        sepo
            Behavior if the intersection of the areas and the volumes is a line
            or lines:

            (blank) - The resulting areas will share line(s) where they touch.

            SEPO - The resulting areas will have separate, but coincident line(s) where they
                   touch.

        keepa
            Specifies whether NA areas are to be deleted:

            (blank) - Use the setting of KEEP on the BOPTN command.

            DELETE - Delete NA areas after ASBV operation (override BOPTN command settings).

            KEEP - Keep NA areas after ASBV operation (override BOPTN command settings).

        keepv
            Specifies whether NV volumes are to be deleted:

            (blank) - Use the setting of KEEP on the BOPTN command.

            DELETE - Delete volumes after ASBV operation (override BOPTN command settings).

            KEEP - Keep volumes after ASBV operation (override BOPTN command settings).

        Notes
        -----
        Generates new areas by subtracting the regions common to both NA areas
        and NV volumes (the intersection) from the NA areas.  The intersection
        can be an area(s) or line(s).  If the intersection is a line and SEPO
        is blank, the NA area is divided at the line and the resulting areas
        will be connected, sharing a common line where they touch.  If SEPO is
        set to SEPO, NA is divided into two unconnected areas with separate
        lines where they touch.  See Solid Modeling in the Modeling and Meshing
        Guide for an illustration.  See the BOPTN command for an explanation of
        the options available to Boolean operations.  Element attributes and
        solid model boundary conditions assigned to the original entities will
        not be transferred to the new entities generated.
        """
        command = f"ASBV,{na},{nv},{sepo},{keepa},{keepv}"
        return self.run(command, **kwargs)

    def asbw(self, na="", sepo="", keep="", **kwargs):
        """Subtracts the intersection of the working plane from areas (divides

        APDL Command: ASBW
        areas).

        Parameters
        ----------
        na
            Area (or areas, if picking is used) to be subtracted from.  If NA =
            ALL, use all selected areas.  If NA = P, graphical picking is
            enabled (valid only in the GUI).  A component name may also be
            input for NA.

        sepo
            Behavior of the created boundary.

            (blank) - The resulting areas will share line(s) where they touch.

            SEPO - The resulting areas will have separate, but coincident line(s).

        keep
            Specifies whether NA areas are to be deleted.

            (blank) - Use the setting of KEEP on the BOPTN command.

            DELETE - Delete NA areas after ASBW operation (override BOPTN command settings).

            KEEP - Keep NA areas after ASBW operation (override BOPTN command settings).

        Notes
        -----
        Generates new areas by subtracting the intersection of the working
        plane from the NA areas.  The intersection will be a line(s).  The
        working plane must not be in the same plane as the NA areas(s).  If
        SEPO is blank, the NA area is divided at the line and the resulting
        areas will be connected, sharing a common line where they touch.  If
        SEPO is set to SEPO, NA is divided into two unconnected areas with
        separate lines.  The SEPO option may cause unintended consequences if
        any keypoints exist along the cut plane. See Solid Modeling in the
        Modeling and Meshing Guide for an illustration.  See the BOPTN command
        for an explanation of the options available to Boolean operations.
        Element attributes and solid model boundary conditions assigned to the
        original entities will not be transferred to the new entities
        generated.

        Issuing the ASBW command under certain conditions may generate a
        topological degeneracy error. Do not issue the command if:

        A sphere or cylinder has been scaled. (A cylinder must be scaled
        unevenly in the XY plane.)

        A sphere or cylinder has not been scaled but the work plane has been
        rotated.
        """
        command = f"ASBW,{na},{sepo},{keep}"
        return self.run(command, **kwargs)

    def boptn(self, lab="", value="", **kwargs):
        """Specifies Boolean operation options.

        APDL Command: BOPTN

        Parameters
        ----------
        lab
            Default/status key:

            DEFA  - Resets settings to default values.

            STAT  - Lists status of present settings.

        value
            Option settings if Lab = KEEP:

            NO  - Delete entities used as input with a Boolean operation (default).  Entities
                  will not be deleted if meshed or if attached to a higher
                  entity.

            YES  - Keep input solid modeling entities.

        Notes
        -----
        Boolean operations at Revision 5.2 may produce a different number of
        entities than previous revisions of ANSYS.   When running input files
        created at earlier revisions of ANSYS, match the Boolean compatibility
        option (VERSION) to the revision originally used. For instance,  if you
        are running Revision 5.2 and are reading an input file (/INPUT) created
        at Revision 5.1, it is recommended that you set VERSION to RV51 before
        reading the input.

        See the Modeling and Meshing Guide for further details on the functions
        of the RV51 and RV52 labels.

        This command is valid in any processor.
        """
        command = f"BOPTN,{lab},{value}"
        return self.run(command, **kwargs)

    def btol(self, ptol="", **kwargs):
        """Specifies the Boolean operation tolerances.

        APDL Command: BTOL

        Parameters
        ----------
        ptol
            Point coincidence tolerance.  Points within this distance to each
            other will be assumed to be coincident during Boolean operations.
            Loosening the tolerance will increase the run time and storage
            requirements, but will allow more Boolean intersections to succeed.
            Defaults to 0.10E-4.

        Notes
        -----
        Use BTOL,DEFA to reset the setting to its default value.  Use BTOL,STAT
        to list the status of the present setting.
        """
        command = f"BTOL,{ptol}"
        return self.run(command, **kwargs)

    def lcsl(
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
        """Divides intersecting lines at their point(s) of intersection.

        APDL Command: LCSL

        Parameters
        ----------
        nl1, nl2, nl3, . . . , nl9
            Numbers of lines to be intersected.  If NL1 = ALL, NL2 to NL9 are
            ignored and the intersection of all selected lines is found.  If
            NL1 = P, use graphical picking to specify lines (NL2 to NL9 are
            ignored).

        Notes
        -----
        Divides intersecting (classifies) lines at their point(s) of
        intersection.  The original lines (and their corresponding keypoint(s))
        will be deleted by default.  See the BOPTN command for the options
        available to Boolean operations.  Element attributes and solid model
        boundary conditions assigned to the original entities will not be
        transferred to the new entities generated.
        """
        command = f"LCSL,{nl1},{nl2},{nl3},{nl4},{nl5},{nl6},{nl7},{nl8},{nl9}"
        return self.run(command, **kwargs)

    def lglue(
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
        """Generates new lines by "gluing" lines.

        APDL Command: LGLUE

        Parameters
        ----------
        nl1, nl2, nl3, . . . , nl9
            Numbers of the lines to be glued.  If NL1 = ALL, all selected lines
            will be glued (NL2 to NL9 will be ignored).  If NL1 = P, graphical
            picking is enabled and all remaining command fields are ignored
            (valid only in the GUI).  A component name may also be substituted
            for NL1.

        Notes
        -----
        Use of the LGLUE command generates new lines by "gluing" input lines.
        The glue operation redefines the input lines so that they share
        keypoints at their common ends.  The new lines encompass the same
        geometry as the original lines.  This operation is only valid if the
        intersections of the input lines are keypoints at the ends of those
        lines.  See the Modeling and Meshing Guide for an illustration.  See
        the BOPTN command for an explanation of the options available to
        Boolean operations.  Element attributes and solid model boundary
        conditions assigned to the original entities will not be transferred to
        the new entities generated.

        The LGLUE command results in the merging of keypoints at the common end
        of the lines. The keypoints of the lower numbered line will be kept.
        This means one must be aware of line numbering when multiple LGLUE
        commands are applied to avoid any "ungluing" of geometry.
        """
        command = f"LGLUE,{nl1},{nl2},{nl3},{nl4},{nl5},{nl6},{nl7},{nl8},{nl9}"
        return self.run(command, **kwargs)

    def lina(self, nl="", na="", **kwargs):
        """Finds the intersection of a line with an area.

        APDL Command: LINA

        Parameters
        ----------
        nl
            Number of line to be intersected.  If NL = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in
            the GUI).

        na
            Number of area to be intersected.

        Notes
        -----
        Finds the intersection of a line with an area.  New lines will be
        generated where the lines intersect the areas.  If the regions of
        intersection are only points, new keypoints will be generated instead.
        See the Modeling and Meshing Guide for an illustration.  See the BOPTN
        command for the options available to Boolean operations.  Element
        attributes and solid model boundary conditions assigned to the original
        entities will not be transferred to the new entities generated.
        """
        command = f"LINA,{nl},{na}"
        return self.run(command, **kwargs)

    def linl(
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
        """Finds the common intersection of lines.

        APDL Command: LINL

        Parameters
        ----------
        nl1, nl2, nl3, . . . , nl9
            Numbers of lines to be intersected.  If NL1 = ALL, find the
            intersection of all selected lines and NL2 to NL9 are ignored.  If
            NL1 = P, graphical picking is enabled and all remaining command
            fields are ignored (valid only in the GUI).  A component name may
            also be substituted for NL1.

        Notes
        -----
        Finds the common (not pairwise) intersection of lines.  The common
        intersection is defined as the regions shared (in common) by all lines
        listed on this command.  New lines will be generated where the original
        lines intersect.  If the regions of intersection are only points, new
        keypoints will be generated instead.  See the Modeling and Meshing
        Guide for an illustration.  See the BOPTN command for the options
        available to Boolean operations.  Element attributes and solid model
        boundary conditions assigned to the original entities will not be
        transferred to the new entities generated.
        """
        command = f"LINL,{nl1},{nl2},{nl3},{nl4},{nl5},{nl6},{nl7},{nl8},{nl9}"
        return self.run(command, **kwargs)

    def linp(
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
        """Finds the pairwise intersection of lines.

        APDL Command: LINP

        Parameters
        ----------
        nl1, nl2, nl3, . . . , nl9
            Numbers of lines to be intersected pairwise.  If NL1 =  ALL, find
            the pairwise intersection of all selected lines and NL2 to NL9 are
            ignored.  If NL1 = P, graphical picking is enabled and all
            remaining command fields are ignored (valid only in the GUI).  A
            component name may be substituted for NL1.

        Notes
        -----
        Finds the pairwise intersection of lines.  The pairwise intersection is
        defined as any and all regions shared by at least two lines listed on
        this command.  New lines will be generated where the original lines
        intersect pairwise.  If the regions of pairwise intersection are only
        points, new keypoints will be generated.  See the Modeling and Meshing
        Guide for an illustration.  See the BOPTN command for the options
        available to Boolean operations.  Element attributes and solid model
        boundary conditions assigned to the original entities will not be
        transferred to the new entities generated.
        """
        command = f"LINP,{nl1},{nl2},{nl3},{nl4},{nl5},{nl6},{nl7},{nl8},{nl9}"
        return self.run(command, **kwargs)

    def linv(self, nl="", nv="", **kwargs):
        """Finds the intersection of a line with a volume.

        APDL Command: LINV

        Parameters
        ----------
        nl
            Number of line to be intersected.  If NL = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in
            the GUI).

        nv
            Number of volume to be intersected.

        Notes
        -----
        Finds the intersection of a line with a volume.  New lines will be
        generated where the lines intersect the volumes.  If the regions of
        intersection are only points, new keypoints will be generated instead.
        See the Modeling and Meshing Guide for an illustration.  See the BOPTN
        command for the options available to Boolean operations.  Element
        attributes and solid model boundary conditions assigned to the original
        entities will not be transferred to the new entities generated.
        """
        command = f"LINV,{nl},{nv}"
        return self.run(command, **kwargs)

    def lovlap(
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
        """Overlaps lines.

        APDL Command: LOVLAP

        Parameters
        ----------
        nl1, nl2, nl3, . . . , nl9
            Numbers of lines to be overlapped.  If NL1 = ALL, NL2 to NL9 are
            ignored and all selected lines are overlapped.  If NL1 = P,
            graphical picking is enabled and all remaining command fields are
            ignored (valid only in the GUI).  A component name may also be
            substituted for NL1.

        Notes
        -----
        Overlaps lines. Generates new lines which encompass the geometry of all
        the input lines.  The new lines are defined by the regions of
        intersection of the input lines, and by the complementary (non-
        intersecting) regions.  See the Modeling and Meshing Guide for an
        illustration.  This operation is only valid when the region of
        intersection is a line.  See the BOPTN command for an explanation of
        the options available to Boolean operations.  Element attributes and
        solid  model boundary conditions assigned to the original entities will
        not be transferred to the new entities generated.
        """
        command = f"LOVLAP,{nl1},{nl2},{nl3},{nl4},{nl5},{nl6},{nl7},{nl8},{nl9}"
        return self.run(command, **kwargs)

    def lptn(
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
        """Partitions lines.

        APDL Command: LPTN

        Parameters
        ----------
        nl1, nl2, nl3, . . . , nl9
            Numbers of lines to be operated on.  If NL1 = ALL, NL2 to NL9 are
            ignored all selected lines are used.  If NL1 = P, graphical picking
            is enabled and all remaining command fields are ignored (valid only
            in the GUI).  A component name may be substituted for NL1.

        Notes
        -----
        Partitions lines.  Generates new lines which encompass the geometry of
        all the input lines.  The new lines are defined by both the regions of
        intersection of the input lines and the complementary (non-
        intersecting) regions.  See the Modeling and Meshing Guide for an
        illustration. See the BOPTN command for an explanation of the options
        available to Boolean operations.  Element attributes and solid model
        boundary conditions assigned to the original entities will not be
        transferred to the new entities generated.
        """
        command = f"LPTN,{nl1},{nl2},{nl3},{nl4},{nl5},{nl6},{nl7},{nl8},{nl9}"
        return self.run(command, **kwargs)

    def lsba(self, nl="", na="", sepo="", keepl="", keepa="", **kwargs):
        """Subtracts areas from lines.

        APDL Command: LSBA

        Parameters
        ----------
        nl
            Line (or lines, if picking is used) to be subtracted from.  If ALL,
            use all selected lines.  If NL = P, graphical picking is enabled
            and all remaining command fields are ignored (valid only in the
            GUI).  A component name may also be substituted for NL.

        na
            Area (or areas, if picking is used) to be subtracted.  If ALL, use
            all selected areas.  A component name may also be substituted for
            NA.

        sepo
            Behavior if the intersection of the lines and the areas is a
            keypoint or keypoints:

            (blank) - The resulting lines will share keypoint(s) where they touch.

            SEPO - The resulting lines will have separate, but coincident keypoint(s) where they
                   touch.

        keepl
            Specifies whether NL lines are to be deleted:

            (blank) - Use the setting of KEEP on the BOPTN command.

            DELETE - Delete NL lines after LSBA operation (override BOPTN command settings).

            KEEP - Keep NL lines after LSBA operation (override BOPTN command settings).

        keepa
            Specifies whether NA areas are to be deleted:

            (blank) - Use the setting of KEEP on the BOPTN command.

            DELETE - Delete areas after LSBA operation (override BOPTN command settings).

            KEEP - Keep areas after LSBA operation (override BOPTN command settings).

        Notes
        -----
        Generates new lines by subtracting the regions common to both NL lines
        and NA areas (the intersection) from the NL lines.  The intersection
        can be a line(s) or keypoint(s).  If the intersection is a keypoint and
        SEPO is blank, the NL line is divided at the keypoint and the resulting
        lines will be connected, sharing a common keypoint where they touch.
        If SEPO is set to SEPO, NL is divided into two unconnected lines with
        separate keypoints where they touch.  See the Modeling and Meshing
        Guide for an illustration.  See the BOPTN command for an explanation of
        the options available to Boolean operations.  Element attributes and
        solid model boundary conditions assigned to the original entities will
        not be transferred to the new entities generated.
        """
        command = f"LSBA,{nl},{na},{sepo},{keepl},{keepa}"
        return self.run(command, **kwargs)

    def lsbl(self, nl1="", nl2="", sepo="", keep1="", keep2="", **kwargs):
        """Subtracts lines from lines.

        APDL Command: LSBL

        Parameters
        ----------
        nl1
            Line (or lines, if picking is used) to be subtracted from.  If ALL,
            use all selected lines.  Lines specified in this argument are not
            available for use in the NL2 argument.  If P, graphical picking is
            enabled (valid only in the GUI) and all remaining fields are
            ignored.  A component name may also be substituted for NL1.

        nl2
            Line (or lines, if picking is used) to subtract.  If ALL, use all
            selected lines (except those included in the NL1 argument).  A
            component name may also be substituted for NL2.

        sepo
            Behavior if the intersection of the NL1 lines and the NL2 lines is
            a keypoint or keypoints:

            (blank) - The resulting lines will share keypoint(s) where they touch.

            SEPO - The resulting lines will have separate, but coincident keypoint(s) where they
                   touch.

        keep1
            Specifies whether NL1 lines are to be deleted:

            (blank) - Use the setting of KEEP on the BOPTN command.

            DELETE - Delete NL1 lines after LSBL operation (override BOPTN command settings).

            KEEP - Keep NL1 lines after LSBL operation (override BOPTN command settings).

        keep2
            Specifies whether NL2 lines are to be deleted:

            (blank) - Use the setting of KEEP on the BOPTN command.

            DELETE - Delete NL2 lines after LSBL operation (override BOPTN command settings).

            KEEP - Keep NL2 lines after LSBL operation (override BOPTN command settings).

        Notes
        -----
        Generates new lines by subtracting the regions common to both NL1 and
        NL2 lines (the intersection) from the NL1 lines.  The intersection can
        be a line(s) or point(s).  If the intersection is a point and SEPO is
        blank, the NL1 line is divided at the point and the resulting lines
        will be connected, sharing a common keypoint where they touch.  If SEPO
        is set to SEPO, NL1 is divided into two unconnected lines with separate
        keypoints where they touch.  See the Modeling and Meshing Guide for an
        illustration.  See the BOPTN command for an explanation of the options
        available to Boolean operations.  Element attributes and solid model
        boundary conditions assigned to the original entities will not be
        transferred to the new entities generated.  LSBL,ALL,ALL will have no
        effect since all the lines (in NL1) will be unavailable as NL2 lines.
        """
        command = f"LSBL,{nl1},{nl2},{sepo},{keep1},{keep2}"
        return self.run(command, **kwargs)

    def lsbv(self, nl="", nv="", sepo="", keepl="", keepv="", **kwargs):
        """Subtracts volumes from lines.

        APDL Command: LSBV

        Parameters
        ----------
        nl
            Line (or lines, if picking is used) to be subtracted from.  If ALL,
            use all selected lines.  If NL = P, graphical picking is enabled
            and all remaining command fields are ignored (valid only in the
            GUI).  A component name may also be substituted for NL.

        nv
            Volume (or volumes, if picking is used) to be subtracted.  If ALL,
            use all selected volumes.  A component name may also be substituted
            for NV.

        sepo
            Behavior if the intersection of the NL lines and the NV volumes is
            a keypoint or keypoints:

            (blank) - The resulting lines will share keypoint(s) where they touch.

            SEPO - The resulting lines will have separate, but coincident keypoint(s) where they
                   touch.

        keepl
            Specifies whether NL lines are to be deleted:

            (blank) - Use the setting of KEEP on the BOPTN command.

            DELETE - Delete NL lines after LSBV operation (override BOPTN command settings).

            KEEP - Keep NL lines after LSBV operation (override BOPTN command settings).

        keepv
            Specifies whether NV volumes are to be deleted:

            (blank) - Use the setting of KEEP on the BOPTN command.

            DELETE - Delete NV volumes after LSBV operation (override BOPTN command settings).

            KEEP - Keep NV volumes after LSBV operation (override BOPTN command settings).

        Notes
        -----
        Generates new lines by subtracting the regions common to both NL lines
        and NV volumes (the intersection) from the NL lines.  The intersection
        can be a line(s) or point(s).  If the intersection is a point and SEPO
        is blank, the NL1 line is divided at the point and the resulting lines
        will be connected, sharing a common keypoint where they touch.  If SEPO
        is set to SEPO, NL1 is divided into two unconnected lines with separate
        keypoints where they touch.  See the Modeling and Meshing Guide for an
        illustration.  See the BOPTN command for an explanation of the options
        available to Boolean operations.  Element attributes and solid model
        boundary conditions assigned to the original entities will not be
        transferred to the new entities generated.  LSBL,ALL,ALL will have no
        effect since all the lines (in NL1) will be unavailable as NL2 lines.
        """
        command = f"LSBV,{nl},{nv},{sepo},{keepl},{keepv}"
        return self.run(command, **kwargs)

    def lsbw(self, nl="", sepo="", keep="", **kwargs):
        """Subtracts the intersection of the working plane from lines (divides

        APDL Command: LSBW
        lines).

        Parameters
        ----------
        nl
            Line (or lines, if picking is used) to be subtracted from.  If NL =
            ALL, use all selected lines.  If NL = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in
            the GUI).  A component name may also be input for NL.

        sepo
            Behavior of the created boundary.

            (blank) - The resulting lines will share keypoint(s) where they touch.

            SEPO - The resulting lines will have separate, but coincident keypoint(s).

        keep
            Specifies whether NL lines are to be deleted:

            (blank) - Use the setting of KEEP on the BOPTN command.

            DELETE - Delete NL lines after LSBW operation (override BOPTN command settings).

            KEEP - Keep NL lines after LSBW operation (override BOPTN command settings).

        Notes
        -----
        Generates new lines by subtracting the intersection of the working
        plane from the NL lines.  The intersection will be a keypoint(s).  The
        working plane must not be in the same plane as the NL line(s).  If SEPO
        is blank, the NL line is divided and the resulting lines will be
        connected, sharing a common keypoint where they touch.  If SEPO is set
        to SEPO, NL is divided into two unconnected lines with separate
        keypoints.  See the Modeling and Meshing Guide for an illustration.
        See the BOPTN command for an explanation of the options available to
        Boolean operations.  Element attributes and solid model boundary
        conditions assigned to the original entities will not be transferred to
        the new entities generated.  Areas that completely contain the input
        lines will be updated if the lines are divided by this operation.
        """
        command = f"LSBW,{nl},{sepo},{keep}"
        return self.run(command, **kwargs)

    def vadd(
        self,
        nv1="",
        nv2="",
        nv3="",
        nv4="",
        nv5="",
        nv6="",
        nv7="",
        nv8="",
        nv9="",
        **kwargs,
    ):
        """Adds separate volumes to create a single volume.

        APDL Command: VADD

        Parameters
        ----------
        nv1, nv2, nv3, . . . , nv9
            Numbers of volumes to be added.  If NV1 = ALL, add all selected
            volumes and ignore NV2 to NV9.  If NV1 = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in
            the GUI).  A component name may also be substituted for NV1.

        Notes
        -----
        Adds separate volumes to create a single volume.  The original volumes
        (and their corresponding areas, lines and keypoints) will be deleted by
        default [BOPTN].  See the BOPTN command for the options available to
        Boolean operations.  Element attributes and solid model boundary
        conditions assigned to the original entities will not be transferred to
        the new entities generated.  Concatenated entities are not valid with
        this command.
        """
        command = f"VADD,{nv1},{nv2},{nv3},{nv4},{nv5},{nv6},{nv7},{nv8},{nv9}"
        return self.run(command, **kwargs)

    def vglue(
        self,
        nv1="",
        nv2="",
        nv3="",
        nv4="",
        nv5="",
        nv6="",
        nv7="",
        nv8="",
        nv9="",
        **kwargs,
    ):
        """Generates new volumes by "gluing" volumes.

        APDL Command: VGLUE

        Parameters
        ----------
        nv1, nv2, nv3, . . . , nv9
            Numbers of the volumes to be glued.  If NV1 = ALL, all selected
            volumes will be glued (NV2 to NV9 will be ignored).  If NV1 = P,
            graphical picking is enabled and all remaining command fields are
            ignored (valid only in the GUI).  A component name may also be
            substituted for NV1.

        Notes
        -----
        Use of the VGLUE command generates new volumes by "gluing" input
        volumes.  The glue operation redefines the input volumes so that they
        share areas along their common boundaries.  The new volumes encompass
        the same geometry as the original volumes.  This operation is only
        valid if the intersections of the input volumes are areas along the
        boundaries of those volumes.  See the Modeling and Meshing Guide for an
        illustration.  See the BOPTN command for an explanation of the options
        available to Boolean operations.  Element attributes and solid model
        boundary conditions assigned to the original entities will not be
        transferred to the new entities generated.

        The VGLUE command results in the merging of areas, lines, and keypoints
        at the common volume boundaries. The areas, lines, and keypoints of the
        lower numbered volume will be kept. This means one must be aware of
        volume numbering when multiple VGLUE commands are applied to avoid any
        "ungluing" of geometry.
        """
        command = f"VGLUE,{nv1},{nv2},{nv3},{nv4},{nv5},{nv6},{nv7},{nv8},{nv9}"
        return self.run(command, **kwargs)

    def vinp(
        self,
        nv1="",
        nv2="",
        nv3="",
        nv4="",
        nv5="",
        nv6="",
        nv7="",
        nv8="",
        nv9="",
        **kwargs,
    ):
        """Finds the pairwise intersection of volumes.

        APDL Command: VINP

        Parameters
        ----------
        nv1, nv2, nv3, . . . , nv9
            Numbers of volumes to be intersected pairwise.  If NV1 = ALL, NV2
            to NV9 are ignored and the pairwise intersection of all selected
            volumes is found.  If NV1 = P, graphical picking is enabled and all
            remaining command fields are ignored (valid only in the GUI).  A
            component name may also be substituted for NV1.

        Notes
        -----
        Finds the pairwise intersection of volumes.  The pairwise intersection
        is defined as all regions shared by any two or more volumes listed on
        this command.  New volumes will be generated where the original volumes
        intersect pairwise.  If the regions of pairwise intersection are only
        areas, new areas will be generated.  See the Modeling and Meshing Guide
        for an illustration.  See the BOPTN command for an explanation of the
        options available to Boolean operations.  Element attributes and solid
        model boundary conditions assigned to the original entities will not be
        transferred to the new entities generated.
        """
        command = f"VINP,{nv1},{nv2},{nv3},{nv4},{nv5},{nv6},{nv7},{nv8},{nv9}"
        return self.run(command, **kwargs)

    def vinv(
        self,
        nv1="",
        nv2="",
        nv3="",
        nv4="",
        nv5="",
        nv6="",
        nv7="",
        nv8="",
        nv9="",
        **kwargs,
    ):
        """Finds the intersection of volumes.

        APDL Command: VINV

        Parameters
        ----------
        nv1, nv2, nv3, . . . , nv9
            Numbers of volumes to be intersected.  If NV1 = ALL, NV2 to NV9 are
            ignored, and the intersection of all selected volumes is found.  If
            NV1 = P, graphical picking is enabled and all remaining command
            fields are ignored (valid only in the GUI).  A component name may
            also be substituted for NV1.

        Notes
        -----
        Finds the common (not pairwise) intersection of volumes.  The common
        intersection is defined as the regions shared (in common) by all
        volumes listed on this command.  New volumes will be generated where
        the original volumes intersect.  If the regions of intersection are
        only areas, new areas will be generated instead.  See the Modeling and
        Meshing Guide for an illustration.  See the BOPTN command for an
        explanation of the options available to Boolean operations.  Element
        attributes and solid model boundary conditions assigned to the original
        entities will not be transferred to the new entities generated.
        """
        command = f"VINV,{nv1},{nv2},{nv3},{nv4},{nv5},{nv6},{nv7},{nv8},{nv9}"
        return self.run(command, **kwargs)

    def vovlap(
        self,
        nv1="",
        nv2="",
        nv3="",
        nv4="",
        nv5="",
        nv6="",
        nv7="",
        nv8="",
        nv9="",
        **kwargs,
    ):
        """Overlaps volumes.

        APDL Command: VOVLAP

        Parameters
        ----------
        nv1, nv2, nv3, . . . , nv9
            Numbers of volumes to be operated on.  If NV1 = ALL, NV2 to NV9 are
            ignored and all selected volumes are used.  If NV1 = P, graphical
            picking is enabled and all remaining command fields are ignored
            (valid only in the GUI).  A component name may also be substituted
            for NV1.

        Notes
        -----
        Overlaps volumes. Generates new volumes which encompass the geometry of
        all  the input volumes.  The new volumes are defined by the regions of
        intersection  of the input volumes, and by the complementary (non-
        intersecting) regions.   See the Modeling and Meshing Guide for an
        illustration.  This operation is only valid  when the region of
        intersection is a volume.  See the BOPTN command for an explanation of
        the options available to Boolean operations.  Element attributes and
        solid model boundary conditions assigned to the original entities will
        not be transferred to the new entities generated.
        """
        command = f"VOVLAP,{nv1},{nv2},{nv3},{nv4},{nv5},{nv6},{nv7},{nv8},{nv9}"
        return self.run(command, **kwargs)

    def vptn(
        self,
        nv1="",
        nv2="",
        nv3="",
        nv4="",
        nv5="",
        nv6="",
        nv7="",
        nv8="",
        nv9="",
        **kwargs,
    ):
        """Partitions volumes.

        APDL Command: VPTN

        Parameters
        ----------
        nv1, nv2, nv3, . . . , nv9
            Numbers of volumes to be operated on.  If NV1 = ALL, NV2 to NV9 are
            ignored and all selected volumes are used.  If NV1  = P, graphical
            picking is enabled and all remaining command fields are ignored
            (valid only in the GUI).  A component name may also be substituted
            for NV1.

        Notes
        -----
        Partitions volumes.  Generates new volumes which encompass the geometry
        of all the input volumes.  The new volumes are defined by the regions
        of intersection of the input volumes, and by the complementary (non-
        intersecting) regions.  See the Modeling and Meshing Guide for an
        illustration. See the BOPTN command for an explanation of the options
        available to Boolean operations.  Element attributes and solid model
        boundary conditions assigned to the original entities will not be
        transferred to the new entities generated.
        """
        command = f"VPTN,{nv1},{nv2},{nv3},{nv4},{nv5},{nv6},{nv7},{nv8},{nv9}"
        return self.run(command, **kwargs)

    def vsba(self, nv="", na="", sepo="", keepv="", keepa="", **kwargs):
        """Subtracts areas from volumes.

        APDL Command: VSBA

        Parameters
        ----------
        nv
            Volume (or volumes, if picking is used) to be subtracted from.  If
            ALL, use all selected volumes.  If P, graphical picking is enabled
            (valid only in the GUI) and remaining fields are ignored.  A
            component name may also be substituted for NV.

        na
            Area (or areas, if picking is used) to subtract.  If ALL, use all
            selected areas.  A component name may also be substituted for NA.

        sepo
            Behavior of the touching boundary:

            (blank) - The resulting volumes will share area(s) where they touch.

            SEPO - The resulting volumes will have separate, but coincident area(s) where they
                   touch.

        keepv
            Specifies whether NV volumes are to be deleted:

            (blank) - Use the setting of KEEP on the BOPTN command.

            DELETE - Delete NV volumes after VSBA operation (override BOPTN command settings).

            KEEP - Keep NV volumes after VSBA operation (override BOPTN command settings).

        keepa
            Specifies whether NA areas are to be deleted:

            (blank) - Use the setting of KEEP on the BOPTN command.

            DELETE - Delete NA areas after VSBA operation (override BOPTN command settings).

            KEEP - Keep NA areas after VSBA operation (override BOPTN command settings).

        Notes
        -----
        Generates new volumes by subtracting the regions common to both the
        volumes and areas (the intersection) from the NV volumes.  The
        intersection will be an area(s).  If SEPO is blank, the volume is
        divided at the area and the resulting volumes will be connected,
        sharing a common area where they touch.  If SEPO is set to SEPO, the
        volume is divided into two unconnected volumes with separate areas
        where they touch.  See the Modeling and Meshing Guide for an
        illustration.  See the BOPTN command for an explanation of the options
        available to Boolean operations.  Element attributes and solid model
        boundary conditions assigned to the original entities will not be
        transferred to the new entities generated.
        """
        command = f"VSBA,{nv},{na},{sepo},{keepv},{keepa}"
        return self.run(command, **kwargs)

    def vsbv(self, nv1="", nv2="", sepo="", keep1="", keep2="", **kwargs):
        """Subtracts volumes from volumes.

        APDL Command: VSBV

        Parameters
        ----------
        nv1
            Volume (or volumes, if picking is used) to be subtracted
            from.  If ALL, use all selected volumes.  Volumes
            specified in set NV2 are removed from set NV1.  If P,
            graphical picking is enabled (valid only in the GUI) and
            remaining fields are ignored.  A component name may also
            be substituted for NV1.

        nv2
            Volume (or volumes, if picking is used) to subtract.  If
            ALL, use all selected volumes (except those included in
            the NV1 argument).  A component name may also be
            substituted for NV2.

        sepo
            Behavior if the intersection of the NV1 volumes and the
            NV2 volumes is an area or areas:

            (blank) - The resulting volumes will share area(s) where they touch.

            SEPO - The resulting volumes will have separate, but
                   coincident area(s) where they touch.

        keep1
            Specifies whether NV1 volumes are to be deleted:

            (blank) - Use the setting of KEEP on the BOPTN command.

            DELETE - Delete NV1 volumes after VSBV operation (override
                     BOPTN command settings).

            KEEP - Keep NV1 volumes after VSBV operation (override
                   BOPTN command settings).

        keep2
            Specifies whether NV2 volumes are to be deleted:

            (blank) - Use the setting of KEEP on the BOPTN command.

            DELETE - Delete NV2 volumes after VSBV operation (override
                     BOPTN command settings).

            KEEP - Keep NV2 volumes after VSBV operation (override
                   BOPTN command settings).

        Notes
        -----
        Generates new volumes by subtracting the regions common to
        both NV1 and NV2 volumes (the intersection) from the NV1
        volumes.  The intersection can be a volume(s) or area(s).  If
        the intersection is an area and SEPO is blank, the NV1 volume
        is divided at the area and the resulting volumes will be
        connected, sharing a common area where they touch.  If SEPO is
        set to SEPO, NV1 is divided into two unconnected volumes with
        separate areas where they touch.  See the Modeling and Meshing
        Guide for an illustration.  See the BOPTN command for an
        explanation of the options available to Boolean operations.
        Element attributes and solid model boundary conditions
        assigned to the original entities will not be transferred to
        the new entities generated.  VSBV,ALL,ALL will have no effect
        because all the volumes in set NV1will have been moved to set
        NV2.
        """
        command = f"VSBV,{nv1},{nv2},{sepo},{keep1},{keep2}"
        return self.run(command, **kwargs)

    def vsbw(self, nv="", sepo="", keep="", **kwargs):
        """Subtracts intersection of the working plane from volumes.

        APDL Command: VSBW

        Parameters
        ----------
        nv
            Volume (or volumes, if picking is used) to be subtracted from.  If
            NV = ALL, use all selected volumes.  If NV = P, graphical picking
            is enabled (valid only in the GUI).  A component name may also be
            input for NV.

        sepo
            Behavior of the created boundary.

            (blank) - The resulting volumes will share area(s) where they touch.

            SEPO - The resulting volumes will have separate, but coincident area(s).

        keep
            Specifies whether NV volumes are to be deleted.

            (blank) - Use the setting of KEEP on the BOPTN command.

            DELETE - Delete NV volumes after VSBW operation (override BOPTN command settings).

            KEEP - Keep NV volumes after VSBW operation (override BOPTN command settings).

        Notes
        -----
        Generates new volumes by subtracting the intersection of the working
        plane from the NV volumes.  The intersection will be an area(s).  If
        SEPO is blank, the volume is divided at the area and the resulting
        volumes will be connected, sharing a common area where they touch.  If
        SEPO is set to SEPO, the volume is divided into two unconnected volumes
        with separate areas.  The SEPO option may cause unintended consequences
        if any keypoints exist along the cut plane. See the Modeling and
        Meshing Guide for an illustration.  See the BOPTN command for an
        explanation of the options available to Boolean operations.  Element
        attributes and solid model boundary conditions assigned to the original
        entities will not be transferred to the new entities generated.

        Issuing the VSBW command under certain conditions may generate a
        topological degeneracy error. Do not issue the command if:

        A sphere or cylinder has been scaled. (A cylinder must be scaled
        unevenly in the XY plane.)

        A sphere or cylinder has not been scaled but the work plane has been
        rotated.
        """
        command = f"VSBW,{nv},{sepo},{keep}"
        return self.run(command, **kwargs)
