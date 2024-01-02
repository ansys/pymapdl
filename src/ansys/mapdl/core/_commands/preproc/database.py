"""
These PREP7 commands are used to read model data into the database,
list out the database, and control the numbering of entities in the
database.

"""


class Database:
    def aflist(self, **kwargs):
        """Lists the current data in the database.

        APDL Command: AFLIST

        Notes
        -----
        Lists the current data and specifications in the database.  If batch,
        lists all appropriate data.  If interactive, lists only summaries.
        """
        command = "AFLIST,"
        return self.run(command, **kwargs)

    def cdread(self, option="", fname="", ext="", fnamei="", exti="", **kwargs):
        """Reads a file of solid model and database information into the database.

        APDL Command: CDREAD

        Parameters
        ----------
        option
            Selects which data to read:

            ALL
                Read all geometry, material property, load, and
                component data (default).  Solid model geometry and loads
                will be read from the file ``Fnamei.Exti``.  All other data
                will be read from the file ``Fname.Ext``.

            DB
                Read all database information contained in file
                ``Fname.Ext``. This file should contain all information
                mentioned above except the solid model loads.
                If reading a ``.CDB`` file written with the ``GEOM`` option
                of the ``CDWRITE`` command, element types [``ET``] compatible with the
                connectivity of the elements on the file must be defined
                prior to reading.

            SOLID
                Read the solid model geometry and solid model
                loads from the file ``Fnamei.Exti``.
                This file could have been written by the ``CDWRITE`` or ``IGESOUT`` command.

            COMB
                Read the combined solid model and database
                information from the file ``Fname.Ext``.

        fname
            File name and directory path (248 characters maximum, including the
            characters needed for the directory path).
            An unspecified directory path defaults to the working directory;
            in this case, you can use all 248 characters for the file name.

        ext
            Filename extension (eight-character maximum). If there is an extension in
            ``fname``, this option is ignored.

        fnamei
            Name of the IGES file and its directory path (248 characters
            maximum, including directory). If you do not specify a directory
            path, it will default to your working directory and you can use all
            248 characters for the file name.

        exti
            Filename extension (eight-character maximum).

        Notes
        -----
        This command causes coded files of solid model (in IGES format) and
        database (in command format) information to be read.  These files are
        normally written by the ``CDWRITE`` or ``IGESOUT`` command.  Note that the
        active coordinate system in these files has been reset to Cartesian
        (``CSYS,0``).

        If a set of data exists prior to the ``CDREAD`` operation, that data set is
        offset upward to allow the new data to fit without overlap. The
        ``NOOFFSET`` command allows this offset to be ignored on a set-by-set
        basis, causing the existing data set to be overwritten with the new
        data set.

        When you write the geometry data using the ``CDWRITE,GEOM`` option, you use
        the ``CDREAD,DB`` option to read the geometry information.

        Using the ``CDREAD,COMB`` option will not write ``NUMOFF`` commands to offset
        entity ID numbers if there is no solid model in the database.

        Multiple CDB file imports cannot have elements with real constants in
        one file and section definitions in another. The section attributes
        will override the real constant attributes.  If you use ``CDREAD`` to
        import multiple CDB files, define all of the elements using only real
        constants, or using only section definitions.  Combining real constants
        and section definitions is not recommended.

        This command is valid in any processor.
        """
        return self.run(f"CDREAD,{option},{fname},{ext},,{fnamei},{exti}", **kwargs)

    def cdwrite(
        self, option="", fname="", ext="", fnamei="", exti="", fmat="", **kwargs
    ):
        """Writes geometry and load database items to a file.

        APDL Command: CDWRITE

        Parameters
        ----------
        option
            Selects which data to write:

            ALL - Write all appropriate geometry, material property,
                  load, and component data (default). Two files will
                  be produced. Fname.Ext will contain all data items
                  mentioned in "Notes", except the solid model
                  data. Fnamei.Exti will contain the solid model
                  geometry and solid model loads data in the form of
                  IGES commands. This option is not valid when
                  CDOPT,ANF is active.

            COMB - Write all data mentioned, but to a single file,
                   Fname.Ext. Solid model geometry data will be
                   written in either IGES or ANF format as specified
                   in the CDOPT command, followed by the remainder of
                   the data in the form of ANSYS commands. More
                   information on these (IGES/ANF) file formats is
                   provided in "Notes".

            DB - Write all database information except the solid model
                 and solid model loads to Fname.Ext in the form of
                 ANSYS commands. This option is not valid when
                 CDOPT,ANF is active.

            SOLID - Write only the solid model geometry and solid
                    model load data. This output will be in IGES or
                    ANF format, as specified in the CDOPT
                    command. More information on these (IGES/ANF) file
                    formats is provided in "Notes".

            GEOM - Write only element and nodal geometry data. Neither
                   solid model geometry nor element attribute data
                   will be written. One file, Fname.Ext, will be
                   produced. Use CDREAD,DB to read in a file written
                   with this option. Element types [ET] compatible
                   with the connectivity of the elements on the file
                   must first be defined before reading the file in
                   with CDREAD,DB.

            CM - Write only node and element component and geometry
            data to Fname.Ext.

            MAT - Write only material property data (both linear and
            nonlinear) to Fname.Ext.

            LOAD - Write only loads for current load step to
            Fname.Ext.

            SECT - Write only section data to Fname.Ext. Pretension
            sections are not included.

        fname
            File name and directory path (248 characters maximum,
            including the characters needed for the directory path).
            An unspecified directory path defaults to the working
            directory; in this case, you can use all 248 characters
            for the file name.

        ext
            Filename extension (eight-character maximum).

        fnamei
            Name of the IGES file and its directory path (248
            characters maximum, including directory). If you do not
            specify a directory path, it will default to your working
            directory and you can use all 248 characters for the file
            name.

        exti
            Filename extension (eight-character maximum).

        fmat
            Format of the output file (defaults to BLOCKED).

            BLOCKED - Blocked format. This format allows faster
                      reading of the output file. The time savings is
                      most significant when BLOCKED is used to read
                      .cdb files associated with very large models.

            UNBLOCKED - Unblocked format.

        Returns
        -------
        str
            Mapdl command output.

        Notes
        -----
        Load data includes the current load step only. Loads applied
        to the solid model (if any) are automatically transferred to
        the finite element model when this command is issued. CDWRITE
        writes out solid model loads for meshed models only. If the
        model is not meshed, the solid model loads cannot be
        saved. Component data include component definitions, but not
        assembly definitions. Appropriate NUMOFF commands are included
        at the beginning of the file; this is to avoid overlap of an
        existing database when the file is read in.

        Element order information (resulting from a WAVES command) is
        not written. The data in the database remain untouched.

        Solution control commands are typically not written to the
        file unless you specifically change a default solution
        setting.

        CDWRITE does not support the GSBDATA and GSGDATA commands, and
        these commands are not written to the file.

        The data may be reread (on a different machine, for example)
        with the CDREAD command. Caution: When the file is read in,
        the NUMOFF,MAT command may cause a mismatch between material
        definitions and material numbers referenced by certain loads
        and element real constants. See NUMOFF for details. Also, be
        aware that the files created by the CDWRITE command explicitly
        set the active coordinate system to Cartesian (CSYS,0).

        You should generally use the blocked format (Fmat = BLOCKED)
        when writing out model data with CDWRITE. This is a compressed
        data format that greatly reduces the time required to read
        large models through the CDREAD command. The blocked and
        unblocked formats are described in Chapter 3 of the Guide to
        Interfacing with ANSYS.

        If you use CDWRITE in any of the derived products (ANSYS Emag,
        ANSYS Professional), then before reading the file, you must
        edit the Jobname.cdb file to remove commands that are not
        available in the respective component product.

        The CDWRITE command writes PART information for any ANSYS
        LS-DYNA input file to the Jobname.cdb file via the EDPREAD
        command. (EDPREAD is not a documented command; it is written
        only when the CDWRITE command is issued.) The PART information
        can be automatically read in via the CDREAD command; however,
        if more than one Jobname.cdb file is read, the PART list from
        the last Jobname.cdb file overwrites the existing PART list of
        the total model. This behavior affects all PART-related
        commands contained in the Jobname.cdb file. You can join
        models, but not PART-related inputs, which you must modify
        using the newly-created PART numbers. In limited cases, an
        update of the PART list (EDWRITE,PUPDATE) is possible; doing
        so requires that no used combination of MAT/TYPE/REAL appears
        more than once in the list.

        The CDWRITE command does not support (for beam meshing) any
        line operation that relies on solid model associativity. For
        example, meshing the areas adjacent to the meshed line,
        plotting the line that contains the orientation nodes, or
        clearing the mesh from the line that contains orientation
        nodes may not work as expected. For more information about
        beam meshing, see Meshing Your Solid Model in the Modeling and
        Meshing Guide.

        IGES and ANF File Formats for Solid Model Geometry Information

        The format used for solid model geometry information is
        determined by the current CDOPT command setting. The default
        format is IGES.

        IGES option (default) to write solid model information (CDOPT,
        IGS):

        Before writing solid model entities, select all corresponding
        lower level entities (ALLSEL,BELOW,ALL).

        Examples
        --------
        Create a basic block and save it to disk.

        >>> mapdl.prep7()
        >>> mapdl.block(0, 1, 0, 1, 0, 1)
        >>> mapdl.et(1, 186)
        >>> mapdl.esize(0.25)
        >>> mapdl.vmesh('ALL')
        >>> mapdl.cdwrite('DB', '/tmp/mesh.cdb')
         TITLE =
         NUMBER OF ELEMENT TYPES =      1
                64 ELEMENTS CURRENTLY SELECTED.  MAX ELEMENT NUMBER =   64
               425 NODES CURRENTLY SELECTED.     MAX NODE NUMBER =     425
                 8 KEYPOINTS CURRENTLY SELECTED. MAX KEYPOINT NUMBER =   8
                12 LINES CURRENTLY SELECTED.     MAX LINE NUMBER =      12
                 6 AREAS CURRENTLY SELECTED.     MAX AREA NUMBER =       6
                 1 VOLUMES CURRENTLY SELECTED.   MAX VOL. NUMBER =       1
         WRITE ANSYS DATABASE AS AN ANSYS INPUT FILE: /tmp/mesh.cdb

        Optionally load the mesh into Python using the archive reader.

        >>> from ansys.mapdl import reader as pymapdl_reader
        >>> mesh = pymapdl_reader.Archive('/tmp/mesh.cdb')
        >>> mesh
        ANSYS Archive File mesh.cdb
         Number of Nodes:              425
         Number of Elements:           64
         Number of Element Types:      1
         Number of Node Components:    0
         Number of Element Components: 0

        """
        command = f"CDWRITE,{option},'{fname}',{ext},,{fnamei},{exti},{fmat}"
        return self.run(command, **kwargs)

    def cdopt(self, option="", **kwargs):
        """Specifies format to be used for archiving geometry.

        APDL Command: CDOPT

        Parameters
        ----------
        option
            IGES

            IGES - Write solid model geometry information using IGES format (default).

            ANF - Write solid model geometry information using ANSYS Neutral File format.

            STAT - Print out the current format setting.

        Notes
        -----
        This command controls your solid model geometry format for CDWRITE
        operations. The ANF option affects only the COMB and SOLID options of
        the CDWRITE command. All other options remain unaffected.

        This option setting is saved in the database.
        """
        command = "CDOPT,%s" % (str(option))
        return self.run(command, **kwargs)

    def cecheck(self, itemlab="", tolerance="", dof="", **kwargs):
        """Check constraint equations and couplings for rigid body motions.

        APDL Command: CECHECK

        Parameters
        ----------
        itemlab
            Item indicating what is to be checked:

            CE - Check constraint equations only

            CP - Check couplings only

            ALL - Check both CE and CP

        tolerance
            Allowed amount of out-of-balance for any constraint equation or
            coupled set. The default value of 1.0e-6 is usually good.

        dof
            Specifies which DOF is to be checked. Default is RIGID, the usual
            option. Other choices are individual DOF such as UX, ROTZ, etc. or
            THERM. The THERM option will check the constraint equations or
            coupled sets for free thermal expansions, whereas the individual
            DOFs check under rigid body motions. ALL is RIGID and THERM.

        Notes
        -----
        This command imposes a rigid body motion on the nodes attached to the
        constraint equation or coupled set and makes sure that no internal
        forces are generated for such rigid body motions. Generation of
        internal forces by rigid body motions usually indicates an error in the
        equation specification (possibly due to nodal coordinate rotations).
        The THERM option does a similar check to see that no internal forces
        are created by the equations if the body does a free thermal expansion
        (this check assumes a single isotropic coefficient of expansion).
        """
        command = "CECHECK,%s,%s,%s" % (str(itemlab), str(tolerance), str(dof))
        return self.run(command, **kwargs)

    def check(self, sele="", levl="", **kwargs):
        """Checks current database items for completeness.

        APDL Command: CHECK

        Parameters
        ----------
        sele
            Specifies which elements are to be checked:

            (blank) - Check all data.

            ESEL - Check only elements in the selected set and unselect any elements not producing
                   geometry check messages.  The remaining elements (those
                   producing check messages) can then be displayed and
                   corrected.  A null set results if no elements produce a
                   message.  Issue ESEL,ALL to select all elements before
                   proceeding.

        levl
            Used only with Sele = ESEL:

            WARN - Select elements producing warning and error messages.

            ERR - Select only elements producing error messages (default).

        Notes
        -----
        This command will not work if SHPP,OFF has been set. A similar,
        automatic check of all data is done before the solution begins.

        If the "Check Elements" option is invoked through the GUI (menu path
        Main Menu> Preprocessor> Meshing> Check Elems), the CHECK,ESEL logic is
        used to highlight elements in the following way:  good elements are
        blue, elements having warnings are yellow, and bad (error) elements are
        red.

        Note:: : The currently selected set of elements is not changed by this
        GUI function.

        This command is also valid in PREP7.
        """
        command = "CHECK,%s,%s" % (str(sele), str(levl))
        return self.run(command, **kwargs)

    def igesout(self, fname="", ext="", att="", **kwargs):
        """Writes solid model data to a file in IGES Version 5.1 format.

        APDL Command: IGESOUT

        Parameters
        ----------
        fname
            File name and directory path (248 characters maximum, including the
            characters needed for the directory path).  An unspecified
            directory path defaults to the working directory; in this case, you
            can use all 248 characters for the file name.

        ext
            Filename extension (eight-character maximum).

        att
            Attribute key:

            0 - Do not write assigned numbers and attributes of the
                solid model entities to the IGES file (default).

            1 - Write assigned numbers and attributes of solid model
                entities (keypoints, lines, areas, volumes) to the
                IGES file.  Attributes include MAT, TYPE, REAL, and
                ESYS specifications as well as associated solid model
                loads and meshing (keypoint element size, number of
                line divisions and spacing ratio) specifications.

        Notes
        -----
        Causes the selected solid model data to be written to a coded
        file in the IGES Version 5.1 format.  Previous data on this
        file, if any, are overwritten.  Keypoints that are not
        attached to any line are written to the output file as IGES
        entity 116 (Point).  Lines that are not attached to any area
        are written to the output file as either IGES Entity 100
        (Circular Arc), 110 (Line), or 126 (Rational B-Spline Curve)
        depending upon whether the ANSYS entity was defined as an arc,
        straight line, or spline.  Areas are written to the output
        file as IGES Entity 144 (Trimmed Parametric Surface).  Volumes
        are written to the output file as IGES entity 186 (Manifold
        Solid B-Rep Object).  Solid model entities to be written must
        have all corresponding lower level entities selected (use
        ALLSEL,BELOW,ALL) before issuing command.  Concatenated lines
        and areas are not written to the IGES file; however, the
        entities that make up these concatenated entities are written.

        Caution:: : Section properties assigned to areas, lines and
        other solid model entities will not be maintained when the
        model is exported using IGESOUT.

        If you issue the IGESOUT command after generating a beam mesh
        with orientation nodes, the orientation keypoints that were
        specified for the line (LATT) are no longer associated with
        the line and are not written out to the IGES file.  The line
        does not recognize that orientation keypoints were ever
        assigned to it, and the orientation keypoints do not "know"
        that they are orientation keypoints.  Thus the IGESOUT command
        does not support (for beam meshing) any line operation that
        relies on solid model associativity.  For example, meshing the
        areas adjacent to the meshed line, plotting the line that
        contains the orientation nodes, or clearing the mesh from the
        line that contains orientation nodes may not work as expected.
        See Meshing Your Solid Model in the Modeling and Meshing Guide
        for more information about beam meshing.
        """
        return self.run(f"IGESOUT,{fname},{ext},,{att}", **kwargs)

    def mfimport(self, fnumb="", option="", fname="", ext="", **kwargs):
        """Imports a new field into a current ANSYS Multi-field solver analysis.

        APDL Command: MFIMPORT

        Parameters
        ----------
        fnumb
            Field number specified by the MFELEM command.

        option
            Selects data to read.

            DB - Reads a CDB file. The CDB file name and extension are specified by Fname and
                 Ext.

        fname
            File name and directory path (248 characters maximum, including the
            characters needed for the directory path).  An unspecified
            directory path defaults to the working directory; in this case, you
            can use all 248 characters for the file name.

        ext
            Filename extension (eight-character maximum).

        Notes
        -----
        The field to be imported should be written to a CDB file (CDWRITE
        command). This file is read into the database, offsetting all existing
        element type numbers, node numbers, etc. in order to accommodate the
        imported field. (See the NUMOFF command for information on offset
        capabilities.) It then updates all of the previously issued MFxx
        commands to the new element type numbers. A new field is created using
        the specified field number, which must not currently exist. If there
        are no ANSYS Multi-field solver command files written for the existing
        fields in the database, one will be written for each field with the
        default name (see the MFCMMAND command). A MFCMMAND will be issued for
        the imported field as well.

        Repeat the MFIMPORT command to import additional fields.

        See Multi-field Commands in the Coupled-Field Analysis Guide for a list
        of all ANSYS Multi-field solver commands and their availability for MFS
        and MFX analyses.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = "MFIMPORT,%s,%s,%s,%s" % (
            str(fnumb),
            str(option),
            str(fname),
            str(ext),
        )
        return self.run(command, **kwargs)

    def nooffset(self, label="", **kwargs):
        """Prevents the CDREAD command from offsetting specified data items

        APDL Command: NOOFFSET

        Parameters
        ----------
        label
            Specifies items not to be offset.

            - ``"NODE"`` : Node numbers
            - ``"ELEM"`` : Element numbers
            - ``"KP"`` : Keypoint numbers
            - ``"LINE"`` : Line numbers
            - ``"AREA"`` : Area numbers
            - ``"VOLU"`` : Volume numbers
            - ``"MAT"`` : Material numbers
            - ``"TYPE"`` : Element type numbers
            - ``"REAL"`` : Real constant numbers
            - ``"CSYS"`` : Coordinate system numbers
            - ``"SECN"`` : Section numbers
            - ``"CP"`` : Coupled set numbers
            - ``"CE"`` : Constraint equation numbers
            - ``"CLEAR"`` : All items will be offset
            - ``"STATUS"`` : Shows which items are specified not to be offset.

        Notes
        -----
        The NOOFFSET command specifies data items not to be offset by a set of
        data read from a CDREAD command.
        """
        command = "NOOFFSET,%s" % (str(label))
        return self.run(command, **kwargs)

    def numcmp(self, label="", **kwargs):
        """Compresses the numbering of defined items.

        APDL Command: NUMCMP

        Parameters
        ----------
        label
            Items to be compressed:

            NODE - Node numbers

            ELEM - Element numbers

            KP - Keypoint numbers

            LINE - Line numbers

            AREA - Area numbers

            VOLU - Volume numbers

            MAT - Material numbers

            TYPE - Element type numbers

            REAL - Real constant numbers

            CP - Coupled set numbers

            SECN - Section numbers

            CE - Constraint equation numbers

            ALL - All item numbers

        Notes
        -----
        The NUMCMP command effectively compresses out unused item
        numbers by renumbering all the items, beginning with one and
        continuing throughout the model.  The renumbering order
        follows the initial item numbering order (that is, compression
        lowers the maximum number by "sliding" numbers down to take
        advantage of unused or skipped numbers).  All defined items
        are renumbered, regardless of whether or not they are actually
        used or selected.  Applicable related items are also checked
        for renumbering as described for the merge operation (NUMMRG).

        Compressing material numbers (NUMCMP,ALL or NUMCMP,MAT) does
        not update the material number referenced by either of the
        following:

        A temperature-dependent convection or surface-to-surface
        radiation load (SF, SFE, SFL, SFA)

        Real constants for multi-material elements (such as SOLID65)

        Compression is usually not required unless memory space is limited and
        there are large gaps in the numbering sequence.
        """
        command = "NUMCMP,%s" % (str(label))
        return self.run(command, **kwargs)

    def nummrg(self, label="", toler="", gtoler="", action="", switch="", **kwargs):
        """Merges coincident or equivalently defined items.

        APDL Command: NUMMRG

        Parameters
        ----------
        label
            Items to be merged:

            NODE - Nodes

            ELEM - Elements

            KP - Keypoints (will also merge lines, areas, and volumes)

            MAT - Materials

            TYPE - Element types

            REAL - Real constants

            CP - Coupled sets

            CE - Constraint equations

            ALL - All items

        toler
            Range of coincidence.  For Label = NODE and KP, defaults to 1.0E-4
            (based on maximum Cartesian coordinate difference between nodes or
            keypoints).  For Label = MAT, REAL, and CE, defaults to 1.0E-7
            (based on difference of the values normalized by the values).  Only
            items within range are merged.  (For keypoints attached to lines,
            further restrictions apply.  See the GTOLER field and Merging Solid
            Model Entities below.)

        gtoler
            Global solid model tolerance -- used only when merging keypoints
            attached to lines.  If specified, GTOLER will override the internal
            relative solid model tolerance.  See Merging Solid Model Entities
            below.

        action
            Specifies whether to merge or select coincident items.

            SELE - Select coincident items but do not merge. Action = SELE is only valid for Label
                   = NODE.

            (Blank) - Merge the coincident items (default).

        switch
            Specifies whether the lowest or highest numbered coincident item is
            retained after the merging operation.  This option does not apply
            to keypoints; i.e., for Label = KP, the lowest numbered keypoint is
            retained regardless of the Switch setting.

            LOW - Retain the lowest numbered coincident item after the merging operation
                  (default).

            HIGH - Retain the highest numbered coincident item after the merging operation.

        Notes
        -----
        After issuing the command, the area and volume sizes (ASUM and VSUM)
        may give slightly different results. In order to obtain the same
        results as before, use /FACET, /NORMAL, and ASUM / VSUM.

        The merge operation is useful for tying separate, but coincident, parts
        of a model together. If not all items are to be checked for merging,
        use the select commands (NSEL, ESEL, etc.) to select items.  Only
        selected items are included in the merge operation for nodes,
        keypoints, and elements.

        By default, the merge operation retains the lowest numbered coincident
        item.  Higher numbered coincident items are deleted.  Set Switch to
        HIGH to retain the highest numbered coincident item after the merging
        operation.  Applicable related items are also checked for deleted item
        numbers and if found, are replaced with the retained item number.  For
        example, if nodes are merged, element connectivities (except
        superelements), mesh item range associativity, coupled degrees of
        freedom, constraint equations, master degrees of freedom, gap
        conditions, degree of freedom constraints, nodal force loads, nodal
        surface loads, and nodal body force loads are checked.  Merging
        material numbers [NUMMRG,ALL or NUMMRG,MAT] does not update the
        material number referenced:

        By temperature-dependent film coefficients as part of convection load
        or a temperature-dependent emissivity as part of a surface-to-surface
        radiation load [SF, SFE, SFL, SFA]

        By real constants for multi-material elements (such as SOLID65)

        If a unique load is defined among merged nodes, the value is kept and
        applied to the retained node.  If loads are not unique (not
        recommended), only the value on the lowest node (or highest if Switch =
        HIGH) will be kept, except for "force" loads for which the values will
        be summed if they are not defined using tabular boundary conditions.

        Note:: The unused nodes (not recommended) in elements, couplings,
        constraint equations, etc. may become active after the merge operation.

        The Action field provides the option of visualizing the coincident
        items before the merging operation.

        Caution:: When merging entities in a model that has already been
        meshed, the order in which you issue multiple NUMMRG commands is
        significant.  If you want to merge two adjacent meshed regions that
        have coincident nodes and keypoints, always merge nodes [NUMMRG,NODE]
        before merging keypoints [NUMMRG,KP].  Merging keypoints before nodes
        can result in some of the nodes becoming "orphaned"; that is, the nodes
        lose their association with the solid model.  Orphaned nodes can cause
        certain operations (such as boundary condition transfers, surface load
        transfers, and so on) to fail. However, using NUMMRG should be avoided
        if at all possible, as the procedure outlined above may even cause
        meshing failure, especially after multiple merging and meshing
        operations.

        After a NUMMRG,NODE, is issued, some nodes may be attached to more than
        one solid entity. As a result, subsequent attempts to transfer solid
        model loads to the elements may not be successful. Issue NUMMRG,KP to
        correct this problem. Do NOT issue VCLEAR before issuing NUMMRG,KP.

        For NUMMRG,ELEM, elements must be identical in all aspects, including
        the direction of the element coordinate system.

        For certain solid and shell elements (181, 185, 190, etc) ANSYS will
        interpret coincident faces as internal and eliminate them. To prevent
        this from occurring, shrink the entities by a very small factor to
        delineate coincident items (/SHRINK, 0.0001) and no internal nodes,
        lines, areas or elements will be eliminated.

        When working with solid models, you may have better success with the
        gluing operations (AGLUE, LGLUE, VGLUE). Please read the following
        information when attempting to merge solid model entities.

        Gluing Operations vs. Merging Operations

        Adjacent, touching regions can be joined by gluing them (AGLUE, LGLUE,
        VGLUE) or by merging coincident keypoints (NUMMRG,KP, which also causes
        merging of identical lines, areas, and volumes).  In many situations,
        either approach will work just fine. Some factors, however, may lead to
        a preference for one method over the other.

        Geometric Configuration

        Gluing is possible regardless of the initial alignment or offset of the
        input entities. Keypoint merging is  possible only if each keypoint on
        one side of the face to be joined is matched by a coincident keypoint
        on the other side. This is commonly the case after a symmetry
        reflection (ARSYM or VSYMM) or a copy (AGEN or VGEN),  especially for a
        model built entirely in ANSYS rather than imported from a CAD system.
        When the geometry is  extremely precise, and the configuration is
        correct for  keypoint merging, NUMMRG is more efficient and robust than
        AGLUE or VGLUE.
        """
        command = "NUMMRG,%s,%s,%s,%s,%s" % (
            str(label),
            str(toler),
            str(gtoler),
            str(action),
            str(switch),
        )
        return self.run(command, **kwargs)

    def numoff(self, label="", value="", **kwargs):
        """Adds a number offset to defined items.

        APDL Command: NUMOFF

        Parameters
        ----------
        label
            Apply offset number to one of the following sets of items:

            NODE - Nodes

            ELEM - Elements

            KP - Keypoints

            LINE - Lines

            AREA - Areas

            VOLU - Volumes

            MAT - Materials

            TYPE - Element types

            REAL - Real constants

            CP - Coupled sets

            SECN - Section numbers

            CE - Constraint equations

            CSYS - Coordinate systems

        value
            Offset number value (cannot be negative).

        Notes
        -----
        Useful for offsetting current model data to prevent overlap if another
        model is read in. CDWRITE automatically writes the appropriate NUMOFF
        commands followed by the model data to File.CDB.  Therefore, when the
        file is read, any model already existing in the database is offset
        before the model data on the file is read.

        Offsetting material numbers with this command  [NUMOFF,MAT] does not
        update the material number referenced by either of the following:

        A temperature-dependent convection or surface-to-surface radiation load
        [SF, SFE, SFL, SFA]

        Real constants for multi-material elements (such as SOLID65).

        Therefore, a mismatch may exist between the material definitions and
        the material numbers referenced.
        """
        command = "NUMOFF,%s,%s" % (str(label), str(value))
        return self.run(command, **kwargs)

    def numstr(self, label="", value="", **kwargs):
        """Establishes starting numbers for automatically numbered items.

        APDL Command: NUMSTR

        Parameters
        ----------
        label
            Apply starting number to one of the following sets of items:

            NODE - Node numbers.  Value defaults (and is continually reset) to 1 + maximum node
                   number in model.  Cannot be reset lower.

            ELEM - Element numbers.  Value defaults (and is continually reset) to 1 + maximum
                   element number in model.  Cannot be reset lower.

            KP - Keypoint numbers.  Value defaults to 1.  Only undefined numbers are used.
                 Existing keypoints are not overwritten.

            LINE - Line numbers.  Value defaults to 1.  Only undefined numbers are used.  Existing
                   lines are not overwritten.

            AREA - Area numbers.  Value defaults to 1.  Only undefined numbers are used.  Existing
                   areas are not overwritten.

            VOLU - Volume numbers.  Value defaults to 1.  Only undefined numbers are used.
                   Existing volumes are not overwritten.

            DEFA - Default.  Returns all starting numbers to their default values.

        value
            Starting number value.

        Notes
        -----
        Establishes starting numbers for various items that may have numbers
        automatically assigned (such as element numbers with the EGEN command,
        and node and solid model entity numbers with the mesh [AMESH, VMESH,
        etc.] commands).  Use NUMSTR,STAT to display settings.  Use NUMSTR,DEFA
        to reset all specifications back to defaults.  Defaults may be lowered
        by deleting and compressing items (i.e., NDELE and NUMCMP,NODE for
        nodes, etc.).

        Note:: : A mesh clear operation (VCLEAR, ACLEAR, LCLEAR, and KCLEAR)
        automatically sets starting node and element numbers to the highest
        unused numbers.  If a specific starting node or element number is
        desired, issue NUMSTR after the clear operation.
        """
        command = "NUMSTR,%s,%s" % (str(label), str(value))
        return self.run(command, **kwargs)
