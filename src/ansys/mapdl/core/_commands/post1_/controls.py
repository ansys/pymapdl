class Controls:
    def avprin(self, key="", effnu="", **kwargs):
        """Specifies how principal and vector sums are to be calculated.

        APDL Command: AVPRIN

        Parameters
        ----------
        key
            Averaging key:

            0 - Average the component values from the elements at a common node, then calculate
                the principal or vector sum from the averaged components
                (default).

            1 - Calculate the principal or vector sum values on a per element basis, then
                average these values from the elements at a common node.

        effnu
            Effective Poisson's ratio used for computing the von Mises
            equivalent strain (EQV). This command option is intended for use
            with line elements or in load case operations (LCOPER) only; ANSYS
            automatically selects the most appropriate effective Poisson's
            ratio, as discussed below.

        Notes
        -----
        Selects the method of combining components for certain derived nodal
        results when two or more elements connect to a common node.  The
        methods apply to the calculations of derived nodal principal stresses,
        principal strains, and vector sums for selects, sorts, and output
        [NSEL, NSORT, PRNSOL, PLNSOL, etc.].

        This command also defines the effective Poisson's ratio (EFFNU) used
        for equivalent strain calculations.  If you use EFFNU, the default
        effective Poisson's ratios shown below will be overridden for all
        elements by the EFFNU value. To return to the default settings, issue
        the RESET command. The default value for EFFNU is:

        Poisson's ratio as defined on the MP commands for EPEL and EPTH

        0.5 for EPPL and EPCR

        0.5 if the referenced material is hyperelastic

        0.0 for line elements (includes beam, link, and pipe elements, as well
        as discrete elements), cyclic symmetry analysis, mode superposition
        analyses (with MSUPkey = YES on the MXPAND command), and load case
        operations (LCOPER).

        For the von Mises equivalent strain (EQV), it is always computed using
        the average of the equivalent strains from the elements at a common
        node irrespective of the value of the averaging KEY. If EFFNU is input,
        though, the calculation will be performed according to the KEY setting.

        For a random vibration (PSD) analysis, issuing either AVPRIN,0 or
        AVPRIN,1 calculates the principal stresses using the appropriate
        averaging method. They are then used to determine SEQV.  The output
        will have non-zero values for the principal stresses.

        If AVPRIN is not issued, the Segalman-Fulcher method is used to
        calculate SEQV. This method does not calculate principal stresses, but
        directly calculates SEQV from the component stresses; therefore, the
        output will have zero values for the principal stresses. Beam and pipe
        elements are excluded

        This command is also valid in POST26, where applicable.

        See Combined Stresses and Strains in the Mechanical APDL Theory
        Reference for more information.
        """
        command = f"AVPRIN,{key},{effnu}"
        return self.run(command, **kwargs)

    def avres(self, key="", opt="", **kwargs):
        """Specifies how results data will be averaged when PowerGraphics is

        APDL Command: AVRES
        enabled.

        Parameters
        ----------
        key
            Averaging key.

            1 - Average results at all common subgrid locations.

            2 - Average results at all common subgrid locations except where material type
                [MAT] discontinuities exist. This option is the default.

            3 - Average results at all common subgrid locations except where real constant
                [REAL] discontinuities exist.

            4 - Average results at all common subgrid locations except where material type
                [MAT] or real constant [REAL] discontinuities exist.

        opt
            Option to determine how results data are averaged.

            (blank) - Average surface results data using only the exterior element faces (default).

            FULL - Average surface results data using the exterior face and interior element data.

        Notes
        -----
        The AVRES command specifies how results data will be averaged at
        subgrid locations that are common to 2 or more elements.  The command
        is valid only when PowerGraphics is enabled (via the /GRAPHICS,POWER
        command).

        With PowerGraphics active (/GRAPHICS,POWER), the averaging scheme for
        surface data with interior element data included (AVRES,,FULL) and
        multiple facets per edge (/EFACET,2 or /EFACET,4) will yield differing
        minimum and maximum contour values depending on the  Z-Buffering
        options (/TYPE,,6 or /TYPE,,7).  When the Section data is not included
        in the averaging schemes (/TYPE,,7), the resulting absolute value for
        the midside node is significantly smaller.

        PowerGraphics does not average your stresses across discontinuous
        surfaces. The normals for various planes and facets are compared to a
        tolerance to determine continuity. The ANGLE value you specify in the
        /EDGE command is the tolerance for classifying surfaces as continuous
        or "coplanar."

        The command affects nodal solution contour plots (PLNSOL), nodal
        solution printout (PRNSOL), and subgrid solution results accessed
        through the Query Results function (under General Postprocessing) in
        the GUI.

        The command has no effect on the nodal degree of freedom solution
        values (UX, UY, UZ, TEMP, etc.).

        For cyclic symmetry mode-superposition harmonic solutions, AVRES,,FULL
        is not supported. Additionally, averaging does not occur across
        discontinuous surfaces, and the ANGLE value on the /EDGE command has no
        effect.

        The command is also available in /SOLU.
        """
        command = f"AVRES,{key},{opt}"
        return self.run(command, **kwargs)

    def efacet(self, num="", **kwargs):
        """Specifies the number of facets per element edge for PowerGraphics

        APDL Command: /EFACET
        displays.

        .. warning::
           This will not change element plotting within PyMapdl with
           ``eplot(vtk=True)``

        Parameters
        ----------
        num
            Number of facets per element edge for element plots.

            1 - Use 1 facet per edge (default for h-elements).

            2 - Use 2 facets per edge.

            4 - Use 4 facets per edge.

        Notes
        -----
        /EFACET is valid only when PowerGraphics is enabled [/GRAPHICS,POWER],
        except that it can be used in FULL graphics mode for element CONTA174.
        (See the /GRAPHICS command and element CONTA174 in the Element
        Reference for more information.) The /EFACET command is only applicable
        to element type displays.

        /EFACET controls the fineness of the subgrid that is used for element
        plots. The element is subdivided into smaller portions called facets.
        Facets are piecewise linear surface approximations of the actual
        element face. In their most general form, facets are warped planes in
        3-D space.  A greater number of facets will result in a smoother
        representation of the element surface for element plots. /EFACET may
        affect results averaging. See Contour Displays in the Basic Analysis
        Guide for more information.

        For midside node elements, use NUM = 2; if NUM = 1, no midside node
        information is output. For non-midside node elements, NUM should be set
        to 1. See the PLNSOL and PRNSOL commands for more information.

        With PowerGraphics active (/GRAPHICS,POWER), the averaging scheme for
        surface data with interior element data included (AVRES,,FULL) and
        multiple facets per edge (/EFACET,2 or /EFACET,4) will yield differing
        minimum and maximum contour values depending on the  Z-Buffering
        options (/TYPE,,6 or /TYPE,,7).  When the Section data is not included
        in the averaging schemes (/TYPE,,7), the resulting absolute value for
        the midside node is significantly smaller.

        For cyclic symmetry mode-superposition harmonic solutions, only NUM = 1
        is supported in postprocessing.

        Caution:: : If you specify /EFACET,1, PowerGraphics does not plot
        midside nodes. You must use /EFACET,2 to make the nodes visible.

        This command is valid in any processor.
        """
        command = f"/EFACET,{num}"
        return self.run(command, **kwargs)

    def ernorm(self, key="", **kwargs):
        """Controls error estimation calculations.

        APDL Command: ERNORM

        Parameters
        ----------
        key
            Control key:

            ON - Perform error estimation (default). This option is
            not valid for PowerGraphics.

            OFF - Do not perform error estimation.

        Notes
        -----
        Especially for thermal analyses, program speed increases if
        error estimation is suppressed.  Therefore, it might be
        desirable to use error estimation only when needed.  The value
        of the ERNORM key is not saved on file.db. Consequently, you
        need to reissue the ERNORM key after a RESUME if you wish to
        deactivate error estimation again.
        """
        return self.run("ERNORM,%s" % (str(key)), **kwargs)

    def inres(
        self,
        item1="",
        item2="",
        item3="",
        item4="",
        item5="",
        item6="",
        item7="",
        item8="",
        **kwargs,
    ):
        """Identifies the data to be retrieved from the results file.

        APDL Command: INRES

        Parameters
        ----------
        item1, item2, item3, . . . , item8
            Data to be read into the database from the results file.  May
            consist of any of the following labels:

            ALL - All solution items (default).

            BASIC - NSOL, RSOL, NLOAD, STRS, FGRAD, and FFLUX items.

            NSOL - Nodal DOF solution.

            RSOL - Nodal reaction loads.

            ESOL - Element solution items (includes all of the following):

            NLOAD - Element nodal loads.

            STRS - Element nodal stresses.

            EPEL - Element elastic strains.

            EPTH - Element thermal, initial, and swelling strains.

            EPPL - Element plastic strains.

            EPCR - Element creep strains.

            FGRAD - Element nodal gradients.

            FFLUX - Element nodal fluxes.

            MISC - Element miscellaneous data (SMISC and NMISC).

        Notes
        -----
        Identifies the type of data to be retrieved from the results file for
        placement into the database through commands such as SET, SUBSET, and
        APPEND.  INRES is a companion command to the OUTRES command controlling
        data written to the database and the results file.  Since the INRES
        command can only flag data that has already been written to the results
        file, care should be taken when using the OUTRES command to include all
        data you wish to retrieve for postprocessing later on.
        """
        command = (
            f"INRES,{item1},{item2},{item3},{item4},{item5},{item6},{item7},{item8}"
        )
        return self.run(command, **kwargs)

    def layer(self, num="", **kwargs):
        """Specifies the element layer for which data are to be processed.

        APDL Command: LAYER

        Parameters
        ----------
        num
            Layer-processing mode:

            N - The layer number to process. The default value is 0.

            FCMAX - Processes the layer with the largest failure criteria.

        Notes
        -----
        Specifies the element layer for which results data are to be listed,
        plotted, or otherwise processed.

        Applies to stress and strain data for layered elements SHELL163,
        SHELL181, SHELL281, ELBOW290, SOLID185, SOLID186, SOLSH190, SHELL208,
        SHELL209, REINF264, and REINF265; heat flux and heat gradient for
        SHELL131 and SHELL132.

        The SHELL command may then be used (with shell elements) to specify a
        location (TOP, MID, BOT) within the layer for output. (The SHELL
        command does not apply to thermal shell elements SHELL131 and
        SHELL132.) Transverse shear stresses for MID are linearly averaged from
        TOP and BOT, and do not reflect a parabolic distribution. Setting
        KEYOPT(8) = 2 for SHELL181, SHELL281, SHELL208, SHELL209, and ELBOW290
        writes the mid-surface values directly to the results file and yields
        more accurate values than linear averaging.

        Because energy is a per-element quantity, you cannot use this command
        for energy output.

        When using the LAYER command with SHELL181, SOLID185, SOLID186,
        SOLSH190, SHELL208, SHELL209, SHELL281, and ELBOW290, KEYOPT(8) must be
        set to 1 (or 2 for SHELL181, SHELL281, ELBOW290, SHELL208, and
        SHELL209) in order to store results for all layers.

        When NUM = FCMAX, you must provide the failure criterion input. If
        specifying input via the FC command, all structural elements are
        processed. For more information, see the documentation for the FC
        command.

        Use this command with RSYS,LSYS to display results in the layer
        coordinate system for a particular layer.

        For the ANSYS LS-DYNA product, this command works differently than
        described above.  For SHELL163, you must first use EDINT during the
        solution phase to define the integration points for which you want
        output data.  Be aware that the output location for SHELL163 data is
        always at the integration point, so "top" and "bottom" refer to the top
        or bottom integration point, not necessarily the top or bottom surface.
        For more information, see the ANSYS LS-DYNA User's Guide.
        """
        command = f"LAYER,{num}"
        return self.run(command, **kwargs)

    def rsys(self, kcn="", **kwargs):
        """Activates a coordinate system for printout or display of element and

        APDL Command: RSYS
        nodal results.

        Parameters
        ----------
        kcn
            The coordinate system to use for results output:

            0 - Global Cartesian coordinate system (default, except for spectrum analyses).

            1 - Global cylindrical coordinate system.

            2 - Global spherical coordinate system.

            > 10 - Any existing local coordinate system.

            SOLU - Solution coordinate systems. For element quantities, these are the element
                   coordinate system for each element.  For nodal quantities,
                   these are the nodal coordinate systems. If an element or
                   nodal coordinate system is not defined, ANSYS uses the
                   global Cartesian coordinate system. If you issue a LAYER,N
                   command (where N refers to a layer number), the results
                   appear in the layer coordinate system. (SOLU is the default
                   for spectrum analyses.)

            LSYS - Layer coordinate system. For layered shell and solid elements, the results
                   appear in their respective layer coordinate systems.  For a
                   specific layer of interest, issue a LAYER,N command (where N
                   refers to a layer number). If a model has both nonlayered
                   and layered elements, you can use RSYS,SOLU and RSYS,LSYS
                   simultaneously (with RSYS,SOLU applicable to nonlayered
                   elements and RSYS,LSYS applicable to layered elements).  To
                   reverse effects of the LSYS option, issue an RSYS,0 command.
                   LSYS is the default for spectrum analysis.

        Notes
        -----
        The RSYS command activates a coordinate system for printing or
        displaying element results data such as stresses and heat fluxes, and
        nodal results data such as degrees of freedom and reactions. ANSYS
        rotates the results data to the specified coordinate system during
        printout, display, or element table operations (such as PRNSOL, PRESOL,
        PLNSOL, and ETABLE). You can define coordinate systems with various
        ANSYS commands such as LOCAL, CS, CLOCAL, and CSKP.

        If you issue RSYS with KCN > 10 (indicating a local coordinate system),
        and the specified system is subsequently redefined, you must reissue
        RSYS for results to be rotated into the redefined system.

        Note:: : The default coordinate system for certain elements, notably
        shells, is not global Cartesian and is frequently not aligned at
        adjacent elements.

        The use of RSYS,SOLU with these elements can make nodal averaging of
        component element results, such as SX, SY, SZ, SXY, SYZ, and SXZ,
        invalid and is not recommended.

        The RSYS command has no effect on beam or pipe stresses, which ANSYS
        displays (via /ESHAPE,1 and PowerGraphics) in the element coordinate
        system.

        Element results such as stresses and heat fluxes are in the element
        coordinate systems when KCN = SOLU. Nodal requests for element results
        (for example, PRNSOL,S,COMP) average the element values at the common
        node; that is, the orientation of the node is not a factor in the
        output of element quantities.  For nearly all solid elements, the
        default element coordinate systems are parallel to the global Cartesian
        coordinate system. For shell elements and the remaining solid elements,
        the default element coordinate system can differ from element to
        element. For layered shell and layered solid elements, ANSYS initially
        selects the element coordinate system when KCN = SOLU; you can then
        select the layer coordinate system via the LAYER command.

        Nodal results such as degrees of freedom and reactions can be properly
        rotated only if the resulting component set is consistent with the
        degree-of-freedom set at the node. (The degree-of-freedom set at a node
        is determined by the elements attached to the node.) For example, if a
        node does not have a UZ degree of freedom during solution, then any Z
        component resulting from a rotation does not print or display in POST1.
        Therefore, results at nodes with a single degree-of-freedom (UY only,
        for example) should not be rotated; that is, they should be viewed only
        in the nodal coordinate system or a system parallel to the nodal
        system. (The global Cartesian system--the RSYS command default--may not
        be parallel to the nodal system.) Results at nodes with a 2-D degree-
        of-freedom set (UX and UY, for example) should not be rotated out of
        the 2-D plane.

        PowerGraphics

        For PowerGraphics, ANSYS plots PLVECT vector arrow displays (such
        temperature, velocity, and force) in the global Cartesian coordinate
        system (RSYS = 0). Subsequent operations revert to your original
        coordinate system.

        PGR File

        When you generate a .PGR file in SOLUTION, you can use the Results
        Viewer to display your stresses only in the coordinate system in which
        you write your .PGR file. To view stresses in other coordinate systems,
        load your results file into the Results Viewer and regenerate the data.

        Large Deflections

        If large deflection is active (NLGEOM,ON), ANSYS rotates the element
        component result directions by the amount of rigid body rotation.

        ANSYS displays the element component results in the initial global
        coordinate system for the following elements: SHELL181, SHELL281,
        ELBOW290, PLANE182, PLANE183, SOLID185, SOLID186, SOLID187, SOLID272,
        SOLID273, SOLID285, SOLSH190, SHELL208, and SHELL209. All other element
        result transformations are, therefore, also relative to the initial
        global system. Nodal degree-of-freedom results are based on the initial
        (and not the updated) geometry. For all other element types, component
        results displayed in the co-rotated coordinate system include the
        element rigid body rotation from the initial global coordinate system,
        and all other element result transformations are relative to the
        rotated global system.

        LS-DYNA

        You can use the RSYS command to rotate stress data for all explicit
        (ANSYS LS-DYNA) elements except BEAM161, COMBI165, and composite
        SHELL163 (KEYOPT(3) = 1). In models that contain these element types
        combined with other explicit elements, you must unselect the
        unsupported elements before issuing the RSYS command. The command does
        not support strain data for any explicit element types. If you request
        strain results for explicit elements when RSYS is not set to the global
        Cartesian coordinate system (KCN = 0), ANSYS ignores the printing or
        plotting command. (ANSYS always rotates displacements into the results
        coordinate system, independent of the explicit element type.)
        """
        command = f"RSYS,{kcn}"
        return self.run(command, **kwargs)
