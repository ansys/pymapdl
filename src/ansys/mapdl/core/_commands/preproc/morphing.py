class Morphing:
    def morph(
        self,
        option="",
        remeshopt="",
        elemset="",
        armax="",
        voch="",
        arch="",
        step="",
        time="",
        stropt="",
        **kwargs,
    ):
        """Specifies morphing and remeshing controls.

        APDL Command: MORPH

        Parameters
        ----------
        option
            OFF - Turns off morphing for field elements (default).

            ON - Turns on morphing for field elements.

        remeshopt
            OFF - Do not remesh (default).

            ON - Remesh when element qualities fall below values
                 specified by ARMAX, VOCH, or ARCH as explained
                 below. Valid only when Option is ON.

        elemset
            ALL - Remesh all selected elements if the quality of the
                  worst defined element falls below any quality
                  requirement (default when Remeshopt = ON).

            CompName - Specify a component name, up to 32
                        characters. All elements included in this
                        component name are remeshed if the quality of
                        the worst element falls below any quality
                        requirement.

        armax
            The maximum allowable element generalized aspect ratio. Defaults to
            5.

        voch
            The maximum allowable change of element size (area or volume).
            Defaults to 3.

        arch
            The maximum allowable element aspect ratio change.  Defaults to 3.

        step
            The frequency of element quality checking, based on time steps. A
            quality check takes place at the intervals defined by STEP.
            Defaults to 1 (quality check at every step).

        time
            A quality check takes place at the time point specified. Defaults
            to -1 (a quality check at every time point).

        stropt
            NO

            NO - There are no structural elements in the model (default).

            YES - There are no structural elements in the model and the morphing happens after
                  the structural solution.

        Notes
        -----
        MORPH is applicable to any non-structural field analysis (not including
        fluid elements). It activates displacement degrees of freedom for non-
        structural elements so that boundary conditions may be placed on the
        field mesh to constrain the movement of the non-structural mesh during
        morphing. It morphs the non-structural mesh using displacements
        transferred at the surface interface between the structural field and
        the non-structural field.  The displacements of non-structural elements
        are mesh displacements to avoid mesh distortion, but have no physical
        meaning except at the interface. MORPH does not support surface, link,
        or shell elements, or any element shape other than triangles, quads,
        tets, and bricks. Morphed fields must be in the global Cartesian system
        (CSYS = 0).

        After each remesh, new databases and results files are written with the
        extensions .rth0n and .db0n, where n is the remesh file number
        (FieldName.rth01, FieldName.rth02, ... and FieldName.db01,
        FieldName.db02, etc.).   The original database file is FieldName.dbo.
        The FieldName.db01, FieldName.db02, etc. files have elements that are
        detached from the solid model.

        Remeshing has the following restrictions:

        Valid only for the electrostatic elements (PLANE121, SOLID122, and
        SOLID123)

        Limited to triangle (2-D) and tetrahedral (3-D) options of these
        elements

         Valid only for the MFS solver

        No body loads allowed in the interior nodes of the remeshing domain

        Nodes on the boundary cannot be remeshed; remeshing will not work if
        morphing failed on the surface nodes

        Not suitable for extreme area or volume changes

        This command is also valid in SOLUTION.
        """
        command = f"MORPH,{option},,{remeshopt},{elemset},{armax},{voch},{arch},{step},{time},{stropt}"
        return self.run(command, **kwargs)

    def damorph(self, area="", xline="", rmshky="", **kwargs):
        """Move nodes in selected areas to conform to structural displacements.

        APDL Command: DAMORPH

        Parameters
        ----------
        area
            Non-structural area to which mesh movement (morph) applies.  If
            ALL, apply morphing to all selected areas [ASEL].  If AREA = P,
            graphical picking is enabled.  A component may be substituted for
            AREA.

        xline
            Lines to be excluded from morphing.  If ALL, exclude all selected
            lines [LSEL] from morphing.  If XLINE = P, graphical picking is
            enabled.  A component may be substituted for XLINE.  If XLINE is
            blank (default), allow morphing of nodes attached to lines of the
            selected areas (AREA) which are not shared by unselected areas.
            See Notes for clarification.

        rmshky
            Remesh flag option:

            0 - Remesh the selected non-structural areas only if mesh morphing fails.

            1 - Remesh the selected non-structural areas and bypass mesh morphing.

            2 - Perform mesh morphing only and do not remesh.

        Notes
        -----
        The selected areas should include only non-structural regions adjacent
        to structural regions. DAMORPH will morph the non-structural areas to
        coincide with the deflections of the structural regions.

        Nodes in the structural regions move in accordance with computed
        displacements. Displacements from a structural analysis must be in the
        database prior to issuing DAMORPH.

        By default, nodes attached to lines can move along the lines, or off
        the lines (if a line is interior to the selected areas). You can use
        XLINE to restrain nodes on certain lines.

        By default (RMSHKEY = 0), DAMORPH will remesh the selected non-
        structural areas entirely if a satisfactory morphed mesh cannot be
        provided.

        If boundary conditions and loads are applied directly to nodes and
        elements, the DAMORPH command requires that these be removed before
        remeshing can take place.

        Exercise care with initial conditions defined by the IC command. Before
        a structural analysis is performed for a sequentially coupled analysis,
        the DAMORPH command requires that initial conditions be removed from
        all null element type nodes in the non-structural regions. Use ICDELE
        to delete the initial conditions.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"DAMORPH,{area},{xline},{rmshky}"
        return self.run(command, **kwargs)

    def demorph(self, elem="", dimn="", rmshky="", **kwargs):
        """Move nodes in selected elements to conform to structural displacements.

        APDL Command: DEMORPH

        Parameters
        ----------
        elem
            Non-structural elements to which mesh movement (morph) applies.
            If ALL, apply morphing to all selected elements [ESEL]. If ELEM =
            P, graphical picking is enabled.  A component may be substituted
            for ELEM.

        dimn
            Problem dimensionality.  Use "2" for a 2-D problem and "3" for a
            3-D problem (no default).

        rmshky
            Remesh flag option:

            0 - Remesh the selected non-structural regions only if mesh morphing fails.

            1 - Remesh the selected non-structural regions and bypass mesh morphing.

            2 - Perform mesh morphing only and do not remesh.

        Notes
        -----
        The selected elements should include only non-structural regions
        adjacent to structural regions. The exterior nodes of the selected
        elements will usually be on the boundary of the region which will have
        node positions displaced. For DIMN = 2, elements must lie on a flat
        plane. The DEMORPH command requires a single domain grouping of
        elements be provided (multiple domains of elements are not permitted).
        Exterior nodes will be assumed fixed (no nodes will be morphed) unless
        they coincide with structural nodes having nonzero displacements.

        Nodes in the structural regions move in accordance with computed
        displacements. Displacements from a structural analysis must be in the
        database prior to issuing DEMORPH.

        By default (RMSHKY = 0), DEMORPH will remesh the selected non-
        structural regions entirely if a satisfactory morphed mesh cannot be
        provided.

        If boundary conditions and loads are applied directly to nodes and
        elements, the DEMORPH command requires that these be removed before
        remeshing can take place.

        Exercise care with initial conditions defined by the IC command. Before
        a structural analysis is performed for a sequentially coupled analysis,
        the DEMORPH command requires that initial conditions be removed from
        all null element type nodes in the non-structural regions. Use ICDELE
        to delete the initial conditions.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"DEMORPH,{elem},{dimn},{rmshky}"
        return self.run(command, **kwargs)

    def dvmorph(self, volu="", xarea="", rmshky="", **kwargs):
        """Move nodes in selected volumes to conform to structural displacements.

        APDL Command: DVMORPH

        Parameters
        ----------
        volu
            Non-structural volume to which mesh movement (morph) applies.  If
            ALL, apply morphing to all selected volumes [VSEL]. If VOLU  = P,
            graphical picking is enabled. A component may be substituted for
            VOLU.

        xarea
            Areas to be excluded from morphing. If ALL, exclude all selected
            areas [ASEL].  If XAREA = P, graphical picking is enabled. A
            component may be substituted for XAREA. If XAREA is blank
            (default), allow morphing of nodes attached to areas of the
            selected volumes (VOLU) which are not shared by unselected volumes.
            (See Notes for clarification).

        rmshky
            Remesh flag option:

            0 - Remesh the selected non-structural volumes only if mesh morphing fails.

            1 - Remesh the selected non-structural volumes and bypass mesh morphing.

            2 - Perform mesh morphing only and do not remesh.

        Notes
        -----
        The selected volumes should include only non-structural regions
        adjacent to structural regions. DVMORPH will morph the non-structural
        volumes to coincide with the deflections of the structural regions.

        Nodes in the structural regions move in accordance with computed
        displacements. Displacements from a structural analysis must be in the
        database prior to issuing DVMORPH.

        By default, nodes attached to areas can move along the areas. You can
        use XAREA to restrain nodes on certain areas.

        By default (RMSHKY = 0), DVMORPH will remesh the selected non-
        structural volumes entirely if a satisfactory morphed mesh cannot be
        provided.

        If boundary conditions and loads are applied directly to nodes and
        elements, the DVMORPH command requires that these be removed before
        remeshing can take place.

        Exercise care with initial conditions defined by the IC command. Before
        a structural analysis is performed for a sequentially coupled analysis,
        the DVMORPH command requires that initial conditions be removed from
        all null element type nodes in the non-structural regions. Use ICDELE
        to delete the initial conditions.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"DVMORPH,{volu},{xarea},{rmshky}"
        return self.run(command, **kwargs)
