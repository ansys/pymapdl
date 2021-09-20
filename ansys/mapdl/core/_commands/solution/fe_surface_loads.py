class FeSurfaceLoads:
    def sf(self, nlist="", lab="", value="", value2="", **kwargs):
        """Specifies surface loads on nodes.

        APDL Command: SF

        Parameters
        ----------
        nlist
            Nodes defining the surface upon which the load is to be applied.
            Use the label ALL or P, or a component name.  If ALL, all selected
            nodes [NSEL] are used (default).  If P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in
            the GUI).

        lab
            Valid surface load label. Load labels are listed under "Surface
            Loads" in the input table for each element type in the Element
            Reference.

        value
            Surface load value or table name reference for specifying tabular
            boundary conditions.

        value2
            Second surface load value (if any).

        Notes
        -----
        Individual nodes may not be entered for this command.  The node list is
        to identify a surface and the Nlist field must contain a sufficient
        number of nodes to define an element surface.  The loads are internally
        stored on element faces defined by the specified nodes.  All nodes on
        an element face (including midside nodes, if any) must be specified for
        the face to be used, and the element must be selected.

        If all nodes defining a face are shared by an adjacent face of another
        selected element, the face is not free and will not have a load
        applied.  If more than one element can share the same nodes (for
        example, a surface element attached to a solid element), select the
        desired element type before issuing the SF command. The SF command
        applies only to area and volume elements.

        For shell elements, if the specified nodes include face one (which is
        usually the bottom face) along with other faces (such as edges), only
        face one is used.  Where faces cannot be uniquely determined from the
        nodes, or where the face does not fully describe the load application,
        use the SFE command.  A load key of 1 (which is typically the first
        loading condition on the first face) is used if the face determination
        is not unique.  A uniform load value is applied over the element face.
        """
        command = f"SF,{nlist},{lab},{value},{value2}"
        return self.run(command, **kwargs)

    def sfbeam(
        self,
        elem="",
        lkey="",
        lab="",
        vali="",
        valj="",
        val2i="",
        val2j="",
        ioffst="",
        joffst="",
        lenrat="",
        **kwargs,
    ):
        """Specifies surface loads on beam and pipe elements.

        APDL Command: SFBEAM

        Parameters
        ----------
        elem
            Element to which surface load is applied.  If ALL, apply load to
            all selected beam elements (ESEL).  If Elem = P, graphical picking
            is enabled and all remaining command fields are ignored (valid only
            in the GUI).  A component name may be substituted in Elem.

        lkey
            Load key associated with surface load (defaults to 1).  Load keys
            (1, 2, 3, etc.) are listed under "Surface Loads" in the input table
            for each element type in the Element Reference.  For beam and some
            pipe elements, the load key defines the load orientation.

        lab
            Valid surface load label.  Load labels are listed under "Surface
            Loads" in the input table for each element type in the Element
            Reference.  Structural labels:  PRES (pressure).

        vali, valj
            Surface load values at nodes I and J.  If VALJ is blank, it
            defaults to VALI.  If VALJ is zero, a zero is used.

        val2i, val2j
            Second surface load values at nodes I and J.  Currently not used.

        ioffst, joffst
            Offset distance from node I (toward node J) where VALI is applied,
            and offset distance from node J (toward node I) where VALJ is
            applied, respectively.

        lenrat
            Offset distance flag:

            0  - Offset is in terms of length units (default).

            1  - Offset is in terms of a length ratio (0.0 to 1.0).

        Notes
        -----
        Specifies surface loads on the selected beam elements. Distributed
        loads are applied on a force-per-length basis (that is, the width of
        the underlying element is not considered). To list and delete surface
        loads applied with this command, use the SFELIST and SFEDELE commands,
        respectively.

        If no offset values (IOFFSET and JOFFSET) are specified, the load is
        applied over the full element length. Values may also be input as
        length fractions, depending on the LENRAT setting. For example,
        assuming a line length of 5.0, an IOFFST of 2.0 with LENRAT = 0 or an
        IOFFST of 0.4 with LENRAT = 1 represent the same point.  If JOFFST =
        -1, VALI is assumed to be a point load at the location specified via
        IOFFST, and VALJ is ignored. (IOFFSET cannot be equal to -1.) The
        offset values are stepped even if you issue a KBC,0 command.

        Offsets are only available for element types BEAM188 and PIPE288 if
        using the cubic shape function (KEYOPT(3) = 3) for those element types.

        To accumulate (add) surface loads applied with this command, use the
        SFCUM,,ADD command. Use the same offset values used on the previous
        SFBEAM command (for a given element face); otherwise, the loads do not
        accumulate. If no offsets are specified, the command applies the
        previous offset values.

        This command is also valid in PREP7.
        """
        command = f"SFBEAM,{elem},{lkey},{lab},{vali},{valj},{val2i},{val2j},{ioffst},{joffst},{lenrat}"
        return self.run(command, **kwargs)

    def sfcum(self, lab="", oper="", fact="", fact2="", **kwargs):
        """Specifies that surface loads are to be accumulated.

        APDL Command: SFCUM

        Parameters
        ----------
        lab
            Valid surface load label.  If ALL, use all appropriate labels.

        oper
            Accumulation key:

            REPL - Subsequent values replace the previous values (default).

            ADD - Subsequent values are added to the previous values.

            IGNO - Subsequent values are ignored.

        fact
            Scale factor for the first surface load value. A (blank) or '0'
            entry defaults to 1.0.

        fact2
            Scale factor for the second surface load value. A (blank) or '0'
            entry defaults to 1.0.

        Notes
        -----
        Allows repeated surface loads (pressure, convection, etc.) to be
        replaced, added, or ignored.  Surface loads are applied with the SF,
        SFE, and SFBEAM commands.  Issue the SFELIST command to list the
        surface loads.  The operations occur when the next surface load
        specifications are defined.  For example, issuing the SF command with a
        pressure value of 25 after a previous SF command with a pressure value
        of 20 causes the current value of that pressure to be 45 with the add
        operation, 25 with the replace operation, or 20 with the ignore
        operation.  All new pressures applied with SF after the ignore
        operation will be ignored, even if no current pressure exists on that
        surface.

        Scale factors are also available to multiply the next value before the
        add or replace operation.  A scale factor of 2.0 with the previous
        "add" example results in a pressure of 70.  Scale factors are applied
        even if no previous values exist.  Issue SFCUM,STAT to show the current
        label, operation, and scale factors.  Solid model boundary conditions
        are not affected by this command, but boundary conditions on the FE
        model are affected.

        Note:: : The FE boundary conditions may still be overwritten by
        existing solid model boundary conditions if a subsequent boundary
        condition transfer occurs.

        SFCUM does not work for tabular boundary conditions.

        This command is also valid in PREP7.
        """
        command = f"SFCUM,{lab},{oper},{fact},{fact2}"
        return self.run(command, **kwargs)

    def sfdele(self, nlist="", lab="", **kwargs):
        """Deletes surface loads.

        APDL Command: SFDELE

        Parameters
        ----------
        nlist
            Label defining where to find the list of nodes:

            ALL - Use all selected nodes [NSEL].  If P, use graphical picking in GUI.  A
                  component label may be substituted for Nlist.

        lab
            Valid surface load label.  If ALL, use all appropriate labels.  See
            the SF command for labels.

        Notes
        -----
        Deletes surface loads as applied with the SF command.  Loads are
        deleted only for the specified nodes on external faces of selected area
        and volume elements.  For shell elements, if the specified nodes
        include face one (which is usually the bottom face) along with other
        faces (such as edges), only the loads on face one will be deleted.  The
        element faces are determined from the list of selected nodes as
        described for the SF command.  See the SFEDELE command for deleting
        loads explicitly by element faces.

        This command is also valid in PREP7.
        """
        command = f"SFDELE,{nlist},{lab}"
        return self.run(command, **kwargs)

    def sfe(
        self,
        elem="",
        lkey="",
        lab="",
        kval="",
        val1="",
        val2="",
        val3="",
        val4="",
        **kwargs,
    ):
        """Specifies surface loads on elements.

        APDL Command: SFE

        Parameters
        ----------
        elem
            Element to which surface load applies.  If ALL, apply load to all
            selected elements [ESEL].  If Elem = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in
            the GUI).  A component name may be substituted for Elem.

        lkey
            Load key or face number associated with surface load (defaults to
            1).  Load keys (1,2,3, etc.) are listed under "Surface Loads" in
            the input data table for each element type in the Element
            Reference.

        lab
            Valid surface load label.  Load labels are listed under "Surface
            Loads" in the input table for each element type in the Element
            Reference.

        kval
            Value key.  If Lab = PRES:

            0 or 1 - VAL1 through VAL4 are used as real components of pressures.

            2 - VAL1 through VAL4 are used as imaginary components of pressures.

        val1
            First surface load value (typically at the first node of the face)
            or the name of a table for specifying tabular boundary conditions.
            Face nodes are listed in the order given for "Surface Loads" in the
            input data table for each element type in the Element Reference.
            For example, for SOLID185, the item 1-JILK associates LKEY = 1
            (face 1) with nodes J, I, L, and K.  Surface load value VAL1 then
            applies to node J of face 1.  To specify a table, enclose the table
            name in percent signs (%), e.g., %tabname%.  Use the ``*DIM`` command
            to define a table.  Only one table can be specified, and it must be
            specified in the VAL1 position; tables specified in the VAL2, VAL3,
            or VAL4 positions will be ignored. VAL2 applies to node I, etc.
        """
        command = f"SFE,{elem},{lkey},{lab},{kval},{val1},{val2},{val3},{val4}"
        return self.run(command, **kwargs)

    def sfedele(self, elem="", lkey="", lab="", **kwargs):
        """Deletes surface loads from elements.

        APDL Command: SFEDELE

        Parameters
        ----------
        elem
            Element to which surface load deletion applies.  If ALL, delete
            load from all selected elements [ESEL].  If ELEM = P, graphical
            picking is enabled and all remaining command fields are ignored
            (valid only in the GUI).  A component name may be substituted for
            ELEM.

        lkey
            Load key associated with surface load (defaults to 1).  If ALL,
            delete surface loads for all load keys.

        lab
            Valid surface load label.  If ALL, use all appropriate labels.  See
            the SFE command for labels.

        Notes
        -----
        Deletes surface loads from selected elements.  See the SFDELE command
        for an alternate surface load deletion capability based upon selected
        nodes.

        This command is also valid in PREP7.
        """
        command = f"SFEDELE,{elem},{lkey},{lab}"
        return self.run(command, **kwargs)

    def sfelist(self, elem="", lab="", **kwargs):
        """Lists the surface loads for elements.

        APDL Command: SFELIST

        Parameters
        ----------
        elem
            Element at which surface load is to be listed.  If ALL (or blank),
            list loads for all selected elements [ESEL].  If ELEM = P,
            graphical picking is enabled and all remaining command fields are
            ignored (valid only in the GUI).  A component name may be
            substituted for ELEM.

        lab
            Valid surface load label.  If ALL (or blank), use all appropriate
            labels.

        Notes
        -----
        The surface loads listed correspond to the current database values. The
        database is not updated for surface loads in POST1. Surface loads
        specified in tabular form, however, do list their values corresponding
        to the current results set in POST1.

        For SURF151 or SURF152 elements with an extra node for radiation and/or
        convection calculations (KEYOPT(5) = 1), the bulk temperature listed is
        the temperature of the extra node. If the thermal solution does not
        converge, the extra node temperature is not available for listing.

        Film effectiveness and free stream temperatures specified by the SFE
        command (Lab = CONV) can only be listed by this command. The command
        lists film coefficients and bulk temperatures first and then film
        effectiveness and free stream temperatures below those values.

        Distributed ANSYS Restriction: In Distributed ANSYS within the SOLUTION
        processor, SFELIST support is not available for elements SURF151 and
        SURF152 when surface loading is applied via extra nodes (KEYOPT(5 > 0).
        If the command is issued under these circumstances, the resulting
        surface loads shown are not reliable.

        This command is valid in any processor.
        """
        command = f"SFELIST,{elem},{lab}"
        return self.run(command, **kwargs)

    def sffun(self, lab="", par="", par2="", **kwargs):
        """Specifies a varying surface load.

        APDL Command: SFFUN

        Parameters
        ----------
        lab
            Valid surface load label.  Load labels are listed under "Surface
            Loads" in the input table for each element type in the Element
            Reference.  Issue SFFUN,STATUS to list current command settings.

        par
            Parameter containing list of surface load values.  If Lab = CONV,
            values are typically the film coefficients and Par2 values (below)
            are typically the bulk temperatures.

        par2
            Parameter containing list of second surface load values (if any).
            If Lab = CONV, the Par2 values are typically the bulk temperatures.
            Par2 is not used for other surface load labels.

        Notes
        -----
        Specifies a surface load "function" to be used when the SF or SFE
        command is issued.  The function is supplied through an array parameter
        vector which contains nodal surface load values.  Node numbers are
        implied from the sequential location in the array parameter.  For
        example, a value in location 11 applies to node 11.  The element faces
        are determined from the implied list of nodes when the SF or SFE
        command is issued.  Zero values should be supplied for nodes that have
        no load.  A tapered load value may be applied over the element face.
        These loads are in addition to any loads that are also specified with
        the SF or SFE commands.  Issue SFFUN (with blank remaining fields) to
        remove this specification.  Issue SFFUN,STATUS to list current
        settings.

        Starting array element numbers must be defined for each array parameter
        vector.  For example, SFFUN,CONV,A(1,1),A(1,2) reads the first and
        second columns of array A (starting with the first array element of
        each column) and associates the values with the nodes.  Operations
        continue on successive column array elements until the end of the
        column. Another example to show the order of the commands:

        SFFUN does not work for tabular boundary conditions.

        This command is also valid in PREP7.
        """
        command = f"SFFUN,{lab},{par},{par2}"
        return self.run(command, **kwargs)

    def sfgrad(self, lab="", slkcn="", sldir="", slzer="", slope="", **kwargs):
        """Specifies a gradient (slope) for surface loads.

        APDL Command: SFGRAD

        Parameters
        ----------
        lab
            Valid surface load label.  Load labels are listed under "Surface
            Loads" in the input table for each element type in the Element
            Reference.

        slkcn
            Reference number of slope coordinate system (used with Sldir and
            SLZER to determine COORD).  Defaults to 0 (the global Cartesian
            coordinate system).

        sldir
            Slope direction in coordinate system SLKCN:

            X - Slope is along X direction (default).  Interpreted as R direction for non-
                Cartesian coordinate systems.

            Y - Slope is along Y direction.  Interpreted as  θ direction for non-Cartesian
                coordinate systems.

            Z - Slope is along Z direction.  Interpreted as Φ direction for spherical or
                toroidal coordinate systems.

        slzer
            Coordinate location (degrees for angular input) where slope
            contribution is zero (CVALUE = VALUE).  Allows the slope
            contribution to be shifted along the slope direction.  For angular
            input, SLZER should be between ±180° if the singularity [CSCIR]  is
            at 180° and should be between 0° and 360° if the singularity is at
            0°.

        slope
            Slope value (load per unit length or per degree).

        Notes
        -----
        Specifies a gradient (slope) for surface loads.  All surface loads
        issued with the SF, SFE, SFL, or SFA commands while this specification
        is active will have this gradient applied (for complex pressures, only
        the real component will be affected; for convections, only the bulk
        temperature will be affected).  The load value, CVALUE, calculated at
        each node is:

        CVALUE = VALUE + (SLOPE X (COORD-SLZER))

        where VALUE is the load value specified on the subsequent SF, SFE, SFL,
        or SFA commands and COORD is the coordinate value (in the Sldir
        direction of coordinate system SLKCN) of the node.  Only one SFGRAD
        specification may be active at a time (repeated use of this command
        replaces the previous specification with the new specification).  Issue
        SFGRAD (with blank fields) to remove the specification.  Issue
        SFGRAD,STAT to show the current command status.  The SFGRAD
        specification (if active) is removed when the LSREAD (if any) command
        is issued.

        SFGRAD does not work for tabular boundary conditions.

        This command is also valid in PREP7.
        """
        command = f"SFGRAD,{lab},{slkcn},{sldir},{slzer},{slope}"
        return self.run(command, **kwargs)

    def sflist(self, node="", lab="", **kwargs):
        """Lists surface loads.

        APDL Command: SFLIST

        Parameters
        ----------
        node
            Node at which surface load is to be listed.  If ALL (or blank),
            list for all selected nodes [NSEL].  If NODE = P, graphical picking
            is enabled and all remaining command fields are ignored (valid only
            in the GUI).  A component name may be substituted for NODE.

        lab
            Valid surface load label.  If ALL (or blank), use all appropriate
            labels.

        Notes
        -----
        Lists the surface loads as applied with the SF command.  Loads are
        listed only for the specified nodes on external faces of selected area
        and volume elements.  Use SFELIST for line elements. The surface loads
        listed correspond to the current database values. The database is not
        updated for surface loads in POST1. Surface loads specified in tabular
        form, however, do list their values corresponding to the current
        results set in POST1.

        For SURF151 or SURF152 elements with an extra node for radiation and/or
        convection calculations (KEYOPT(5) = 1), the bulk temperature listed is
        the temperature of the extra node. If the thermal solution does not
        converge, the extra node temperature is not available for listing.

        This command is valid in any processor.
        """
        command = f"SFLIST,{node},{lab}"
        return self.run(command, **kwargs)

    def sfscale(self, lab="", fact="", fact2="", **kwargs):
        """Scales surface loads on elements.

        APDL Command: SFSCALE

        Parameters
        ----------
        lab
            Valid surface load label.  If ALL, use all appropriate labels.

        fact
            Scale factor for the first surface load value.  Zero (or blank)
            defaults  to 1.0.  Use a small number for a zero scale factor.

        fact2
            Scale factor for the second surface load value.  Zero (or blank)
            defaults  to 1.0.  Use a small number for a zero scale factor.

        Notes
        -----
        Scales surface loads (pressure, convection, etc.) in the database on
        the selected elements.  Surface loads are applied with the SF, SFE, or
        SFBEAM commands.  Issue the SFELIST command to list the surface loads.
        Solid model boundary conditions are not scaled by this command, but
        boundary conditions on the FE model are scaled.

        Note:: : Such scaled FE boundary conditions may still be overwritten by
        unscaled solid model boundary conditions if a subsequent boundary
        condition transfer occurs.

        SFSCALE does not work for tabular boundary conditions.

        This command is also valid in PREP7 and in the /MAP processor.
        """
        command = f"SFSCALE,{lab},{fact},{fact2}"
        return self.run(command, **kwargs)
