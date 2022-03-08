class Results:
    def nsort(self, item="", comp="", order="", kabs="", numb="", sel="", **kwargs):
        """Sorts nodal data.

        APDL Command: NSORT

        Parameters
        ----------
        item
            Label identifying the item to be sorted on.  Valid item labels are
            shown in the table below.  Some items also require a component
            label.

        comp
            Component of the item (if required).  Valid component labels are
            shown in the table below.

        order
            Order of sort operation:

            0 - Sort into descending order.

            1 - Sort into ascending order.

        kabs
            Absolute value key:

            0 - Sort according to real value.

            1 - Sort according to absolute value.

        numb
            Number of nodal data records to be sorted in ascending or
            descending order (ORDER) before sort is stopped (remainder will be
            in unsorted sequence) (defaults to all nodes).

        sel
            Allows selection of nodes in the sorted field.

            (blank) - No selection (default).

            SELECT - Select the nodes in the sorted list.

        Notes
        -----
        Values are in the active coordinate system [CSYS for input data or RSYS
        for results data].  Various element results also depend upon the
        recalculation method and the selected results location [AVPRIN, RSYS,
        SHELL, ESEL, and NSEL].  If simultaneous load cases are stored, the
        last sorted sequence formed from any load case applies to all load
        cases.  Use NUSORT to restore the original order.   This command is not
        valid with PowerGraphics.

        Table: 213:: : NSORT - Valid Item and Component Labels

        Table: 214:: : NSORT - Valid Item and Component Labels for Nodal DOF
        Result Values

        Table: 215:: : NSORT - Valid Item and Component Labels for Element
        Result Values

        Works only if failure criteria information is provided. (For more
        information, see the documentation for the FC and TB commands.)

        Must be added via the FCTYP command first.
        """
        command = f"NSORT,{item},{comp},{order},{kabs},{numb},{sel}"
        return self.run(command, **kwargs)

    def nusort(self, **kwargs):
        """Restores original order for nodal data.

        APDL Command: NUSORT

        Notes
        -----
        This command restores the nodal data to its original order (sorted in
        ascending node number sequence) after an NSORT command.  Changing the
        selected nodal set [NSEL] also restores the original nodal order.
        """
        command = f"NUSORT,"
        return self.run(command, **kwargs)

    def plcint(self, action="", id_="", node="", cont="", dtype="", **kwargs):
        """Plots the fracture parameter (CINT) result data.

        APDL Command: PLCINT

        Parameters
        ----------
        action
            PATH

            PATH - Plots CINT quantities according to path number (default).

            FRONT - Plots CINT quantities distribution along the crack front.

        id\_
            Crack ID number.

        node
            Crack tip node number (default = ALL).

        cont
            Contour number (Default = ALL).

        dtype
            Data type to output:

            JINT - J-integral (default)

            IIN1 - Interaction integral 1

            IIN2 - Interaction integral 2

            IIN3 - Interaction integral 3

            K1 - Mode 1 stress-intensity factor

            K2 - Mode 2 stress-intensity factor

            K3 - Mode 3 stress-intensity factor

            G1 - Mode 1 energy release rate

            G2 - Mode 2 energy release rate

            G3 - Mode 3 energy release rate

            GT - Total energy release rate

            MFTX - Total material force X

            MFTY - Total material force Y

            MFTZ - Total material force Z

            TSTRESS - T-stress

            CEXT - Crack extension

            CSTAR - C*-integral

        Notes
        -----
        The PLCINT command is not available for XFEM-based crack growth
        analyses results processing.
        """
        command = f"PLCINT,{action},{id_},{node},{cont},{dtype}"
        return self.run(command, **kwargs)

    def pldisp(self, kund="", **kwargs):
        """Displays the displaced structure.

        APDL Command: PLDISP

        Parameters
        ----------
        kund
            Undisplaced shape key:

            0 - Display only displaced structure.

            1 - Overlay displaced display with similar undisplaced
                display (appearance is system-dependent).

            2 - Same as 1 except overlay with undisplaced edge display
                (appearance is system-dependent).

        Notes
        -----
        Displays the displaced structure for the selected elements.

        For information on true scale plots, refer to the description of the
        /DSCALE command [/DSCALE,,1.0].
        """
        command = f"PLDISP,{kund}"
        return self.run(command, **kwargs)

    def plesol(self, item="", comp="", kund="", fact="", **kwargs):
        """Displays the solution results as discontinuous element contours.

        APDL Command: PLESOL

        Parameters
        ----------
        item
            Label identifying the item.  Valid item labels are shown in
            Table 219: PLESOL - Valid Item and Component Labels for Element
            Results below.  Some items also require a component label.

        comp
            Component of the item (if required).  Valid component labels are
            shown in Table 219: PLESOL - Valid Item and Component Labels for
            Element Results below.

        kund
            Undisplaced shape key:

            0 - Do not overlay undeformed structure display

            1 - Overlay displaced contour plot with undeformed display (appearance is system-
                dependent)

            2 - Overlay displaced contour plot  with undeformed edge display (appearance is
                system-dependent)

        fact
            Scale factor for 2-D display of contact items (defaults to 1). A
            negative scaling factor may be used to invert the display.

        Notes
        -----
        Displays the solution results as element contours discontinuous across
        element boundaries for the selected elements.  For example, PLESOL,S,X
        displays the X component of stress S (that is, the SX stress
        component).  Various element results depend on the calculation method
        and the selected results location (AVPRIN, RSYS, and ESEL).  Contours
        are determined by linear interpolation within each element, unaffected
        by the surrounding elements (i.e., no nodal averaging is performed).
        The discontinuity between contours of adjacent elements is an
        indication of the gradient across elements.  Component results are
        displayed in the active results coordinate system [RSYS] (default is
        the global Cartesian).  See the ETABLE and PLETAB commands for
        displaying items not available through this command (such as line
        element results).

        For PowerGraphics displays [/GRAPHICS,POWER], results are plotted only
        for the model exterior surface.  The items marked with [1] in Table:
        219:: PLESOL - Valid Item and Component Labels for Element Results are
        not supported by PowerGraphics.

        Table: 219:: : PLESOL - Valid Item and Component Labels for Element
        Results
        """
        command = f"PLESOL,{item},{comp},{kund},{fact}"
        return self.run(command, **kwargs)

    def plnsol(self, item="", comp="", kund="", fact="", fileid="", **kwargs):
        """Displays results as continuous contours.

        APDL Command: PLNSOL

        Parameters
        ----------
        item
            Label identifying the item.  Valid item labels are shown in
            Table 220: PLNSOL - Valid Item and Component Labels below.  Some
            items also require a component label.

        comp
            Component of the item (if required).  Valid component labels are
            shown in  Table 220: PLNSOL - Valid Item and Component Labels
            below.

        kund
            Undisplaced shape key:

            0 - Do not overlay undeformed structure display

            1 - Overlay displaced contour plot with undeformed display (appearance is system-
                dependent)

            2 - Overlay displaced contour plot with undeformed edge display (appearance is
                system-dependent)

        fact
            Scale factor for 2-D display for contact items.  Default value is
            1.  A negative scaling factor may be used to invert the display.

        fileid
            The file index number (obtained via the NLDIAG,NRRE,ON command).
            Valid only for Item = NRRE.

        Notes
        -----
        Displays the solution results as continuous contours across element
        boundaries for the selected nodes and elements. For example, PLNSOL,S,X
        displays the X component of stress S (that is,  the SX stress
        component). Various element results depend upon the recalculation
        method and the selected results location [AVPRIN, RSYS, LAYER, SHELL,
        and NSEL].  Contours are determined by linear interpolation within each
        element from the nodal values, which are averaged at a node whenever
        two or more elements connect to the same node (except for FMAG, which
        is summed at the node).

        For PowerGraphics displays [/GRAPHICS,POWER], results are plotted only
        for the model exterior surface.  The items marked with [2] are not
        supported by PowerGraphics. To plot midside nodes, you must first issue
        /EFACET,2.

        Table: 220:: : PLNSOL - Valid Item and Component Labels
        """
        command = f"PLNSOL,{item},{comp},{kund},{fact},{fileid}"
        return self.run(command, **kwargs)

    def plorb(self, **kwargs):
        """Displays the orbital motion of a rotating structure

        APDL Command: PLORB

        Notes
        -----
        When a structure is rotating and the Coriolis or gyroscopic effect is
        taken into account (CORIOLIS), nodes lying on the rotation axis
        generally exhibit an elliptical orbital motion. The PLORB command
        displays the orbit of each rotating node as well as the deformed shape
        at time t = 0 (the real part of the solution).

        To print the characteristics of the orbital path traversed by each
        node, issue the PRORB command.

        The PLORB command is valid for line elements (such as BEAM188, BEAM189,
        PIPE288, and PIPE289).

        Your model must also involve a rotational velocity (OMEGA or CMOMEGA)
        with Coriolis enabled in a stationary reference frame
        (CORIOLIS,,,,RefFrame = ON).

        A SET command should be issued after PLORB to ensure proper output for
        subsequent postprocessing commands.

        The coordinate system for displaying nodal results must be global
        Cartesian (RSYS,KCN = 0).
        """
        command = f"PLORB,"
        return self.run(command, **kwargs)

    def prenergy(
        self,
        energytype="",
        cname1="",
        cname2="",
        cname3="",
        cname4="",
        cname5="",
        cname6="",
        **kwargs,
    ):
        """Prints the total energies of a model or the energies of the specified

        APDL Command: PRENERGY
        components.

        Parameters
        ----------
        energytype
            Type of energies to be printed:

            ALL - All energies are printed: potential, kinetic, artificial hourglass/drill
                  stiffness, contact stabilization energy, and artificial
                  stabilization energy when applicable. This is the default.

            SENE - Potential energy.

            KENE - Kinetic energy.

        cname1, cname2, cname3,…
            Component names for energies of the components printout.

        Notes
        -----
        The PRENERGY command prints out either the total energies of the entire
        model or the energies of the components depending on the Cname1
        specification.

        Only existing components based on elements (defined with the CM
        command) are supported when component energies are listed.

        This command applies to structural elements only.
        """
        command = f"PRENERGY,{energytype},{cname1},{cname2},{cname3},{cname4},{cname5},{cname6}"
        return self.run(command, **kwargs)

    def prorb(self, **kwargs):
        """Prints the orbital motion characteristics of a rotating structure

        APDL Command: PRORB

        Notes
        -----
        When a structure is rotating and the Coriolis or gyroscopic effect is
        taken into account (CORIOLIS), nodes lying on the rotation axis
        generally exhibit an elliptical orbital motion. The PRORB command
        prints out the orbit characteristics A, B, PSI, PHI, YMAX and ZMAX of
        each rotating node, where

        Angles PSI and PHI are in degrees and within the range of -180 through
        +180. For more information about orbit definition, see Orbits in the
        Advanced Analysis Guide.

        To display the characteristics of the orbital path traversed by each
        node, issue the PLORB command.

        The PRORB command is valid for line elements (such as BEAM188, BEAM189,
        PIPE288, and PIPE289).

        Your model must also involve a rotational velocity (OMEGA or CMOMEGA)
        with Coriolis enabled in a stationary reference frame
        (CORIOLIS,,,,RefFrame = ON).

        A SET command should be issued after PRORB to ensure proper output for
        subsequent postprocessing commands.

        The coordinate system for displaying nodal results must be global
        Cartesian (RSYS,KCN = 0).
        """
        command = f"PRORB,"
        return self.run(command, **kwargs)

    def plvect(
        self,
        item="",
        lab2="",
        lab3="",
        labp="",
        mode="",
        loc="",
        edge="",
        kund="",
        **kwargs,
    ):
        """Displays results as vectors.

        APDL Command: PLVECT

        Parameters
        ----------
        item
            Predefined vector item (from Table 223: PLVECT - Valid Item Labels
            below) or a label identifying the i-component of a user-defined
            vector.

        lab2
            Label identifying the j-component of a user-defined vector. In most
            cases, this value must be blank if Item is selected from
            Table 223: PLVECT - Valid Item Labels. Individual principal
            stresses (Item = S) or principal strains (Item = EPxx) may be
            plotted by specifying the value as 1, 2, or 3.

        lab3
            Label identifying the k-component of a user-defined vector.  Must
            be blank if Item is selected from list below or for 2-D user
            defined vector.

        labp
            Label assigned to resultant vector for display labeling (defaults
            to Item).

        mode
            Vector or raster mode override key:

            (blank) - Use the setting of KEY on the /DEVICE command.

            RAST - Use raster mode for PLVECT displays.

            VECT - Use vector mode for PLVECT displays.

        loc
            Vector location for display of field element results:

            ELEM - Display at element centroid (default).

            NODE - Display at element nodes.

        edge
            Edge display override key:

            (blank) - Use the setting of Key on the /EDGE  command.

            OFF - Deactivate the edge display.

            ON - Activate the edge display.

        kund
            Undisplaced shape key:

            0 - Display vectors on undeformed mesh or geometry.

            1 - Display vectors on deformed mesh or geometry.

        Notes
        -----
        Displays various solution results as vectors (arrows) for the selected
        nodes and/or elements (elements must contain at least three nodes that
        are not colinear).  For example, PLVECT,U displays the displacement
        vector for all selected nodes.  For section displays [/TYPE], the
        vectors are shown only on the section face (i.e., cutting plane).  The
        PLVECT display of principal strains and stresses  (Item = S, EPTO,
        EPEL, EPPL, EPCR, or EPTH) on a "cut" of the model (/TYPE,,1 ,5,7,8, or
        9) is not supported.  The resulting plot displays the vectors on all
        selected elements, not on just the sliced surface.  See the /VSCALE
        command to scale vector lengths. Vector magnitudes may be shown as a
        contour display with the PLNSOL command.  Various results also depend
        upon the recalculation method and the selected results location [LAYER,
        SHELL, and NSEL].

        Items may be selected from a set of recognized vector labels (Item) or
        a vector may be defined from up to three scalar labels
        (Item,Lab2,Lab3).  Scalar labels may be user-defined with the ETABLE
        command.  The vectors appear on an element display as arrows showing
        the relative magnitude of the vector and its direction.  The predefined
        items will be shown either at the node or at the element centroid,
        depending on what item is being displayed and depending on the Loc
        setting.  User defined ETABLE items will be shown at the element
        centroid, regardless of the Loc setting. Stress vectors appear as
        arrows at the element centroid, with the arrowheads pointing away from
        each other for tension and toward each other for compression.

        For PowerGraphics, vector arrow displays are generated in Global
        Cartesian (RSYS = 0). All subsequent displays will revert to your
        original coordinate system.

        When vector mode is active (Mode = VECT), use the Z-buffered display
        type [/TYPE,,6] to maximize speed of PLVECT plots  (other hidden
        display types may make plotting slow). For PowerGraphics
        [/GRAPHICS,POWER], the items marked with [1] are not supported  by
        PowerGraphics.

        It is possible to plot principal stresses (Item = S) or principal
        strains (Item = EPxx) individually. To do so, specify a Lab2 value of
        1, 2, or 3. For example, the following are valid commands:

        Table: 223:: : PLVECT - Valid Item Labels

        Not supported by PowerGraphics
        """
        command = f"PLVECT,{item},{lab2},{lab3},{labp},{mode},{loc},{edge},{kund}"
        return self.run(command, **kwargs)

    def prcint(self, id_="", node="", dtype="", **kwargs):
        """Lists the fracture parameter (CINT) results data.

        APDL Command: PRCINT

        Parameters
        ----------
        id\_
            Crack ID number.

        node
            Crack tip node number. Default = ALL. Valid only for 3-D analysis.

        dtype
            Data type to output:

            JINT - J-integral

            IIN1 - Interaction integral 1

            IIN2 - Interaction integral 2

            IIN3 - Interaction integral 3

            K1 - Mode 1 stress-intensity factor

            K2 - Mode 2 stress-intensity factor

            K3 - Mode 3 stress-intensity factor

            G1 - Mode 1 energy release rate

            G2 - Mode 2 energy release rate

            G3 - Mode 3 energy release rate

            GT - Total energy release rate

            MFTX - Total material force X

            MFTY - Total material force Y

            MFTZ - Total material force Z

            TSTRESS - T-stress

            CEXT - Crack extension

            CSTAR - C*-integral

            STTMAX - Maximum circumferential stress

            PSMAX - Maximum circumferential stress when

        Notes
        -----
        When a crack tip node is defined, the values associated with the
        specified node are listed.

        Dtype = STTMAX or PSMAX are valid for XFEM-based crack growth analyses
        only.

        In an XFEM-based analysis, issue the command using this syntax:

        PRCINT, ID, , STTMAX (or PSMAX)
        """
        command = f"PRCINT,{id_},{node},{dtype}"
        return self.run(command, **kwargs)

    def presol(self, item="", comp="", **kwargs):
        """Prints the solution results for elements.

        APDL Command: PRESOL

        Parameters
        ----------
        item
            Label identifying the item.  Valid item labels are shown in
            Table 224: PRESOL - Valid Item and Component Labels for Element
            Results below.  Some items also require a component label.

        comp
            Component of the item (if required).  Valid component labels are
            shown in Table 224: PRESOL - Valid Item and Component Labels for
            Element Results below.

        Notes
        -----
        Prints the solution results for the selected elements in the sorted
        sequence.  For example, PRESOL,S prints the stress items SX, SY, SZ,
        SXY, SYZ, and SXZ for the node locations of the element.  Component
        results are in the global Cartesian coordinate directions unless
        transformed (RSYS).

        Shell elements print values at the top, then bottom of the element (or
        layer). If KEYOPT(8) = 2 (for SHELL181, SHELL208, SHELL209, SHELL281,
        or ELBOW290), the results are printed in the order TOP, BOT and then
        MID of each element, (or layer). The MID value will be the actual value
        as written to the results file.

        Items are listed as columns of a table versus element number.  An
        exception occurs for item ELEM which uses an element format (all
        applicable line element results are listed per element) instead of a
        tabular format.

        The FORCE command can be used to define which component of the nodal
        load is to be used (static, damping, inertia, or total).  See the
        ETABLE and PRETAB commands for printing items not available through
        this command (such as line element results).

        For PowerGraphics [/GRAPHICS,POWER], results are listed only for the
        element surface.  The items marked with [1] are not supported  by
        PowerGraphics.

        Table: 224:: : PRESOL - Valid Item and Component Labels for Element
        Results

        Failure criteria for virgin material [1][2].

        Default components: Maximum of all failure criteria defined at current
        location (MAX), maximum strain (EMAX), maximum stress (SMAX), Tsai-Wu
        Strength Index (TWSI), inverse of Tsai-Wu Strength Ratio Index (TWSR).

        Other available components: Hashin Fiber Failure (HFIB), Hashin Matrix
        Failure (HMAT), Puck Fiber Failure (PFIB), Puck Matrix Failure (PMAT),
        LaRc03 Fiber Failure (L3FB),  LaRc03 Matrix Failure (L3MT), LaRc04
        Fiber Failure (L4FB), LaRc04 Matrix Failure (L4MT), and any user-
        defined failure criteria (USR1 through USR9) [4].

        Issue the FCTYP command to activate or remove failure criteria.

        Failure criteria based on the effective stresses in the damaged
        material.

        Components: Maximum of all failure criteria defined at current location
        (MAX), fiber tensile failure (FT), fiber compressive failure (FC),
        matrix tensile failure (MT), and matrix compressive (MC).

        Progressive damage parameters.

        Components: Damage status (STAT, 0 - undamaged, 1 - damaged, 2 -
        complete damage), fiber tensile damage variable (FT), fiber compressive
        damage variable (FC), matrix tensile damage variable (MT), matrix
        compressive damage variable (MC), shear damage variable (S),  energy
        dissipated per unit volume (SED), energy per unit volume due to viscous
        damping (SEDV).
        """
        command = f"PRESOL,{item},{comp}"
        return self.run(command, **kwargs)

    def prjsol(self, item="", comp="", **kwargs):
        """Prints joint element output.

        APDL Command: PRJSOL

        Parameters
        ----------
        item
            Label identifying the item. Some items also require a component
            label.

            DISP - Relative displacements.

            ROT - Relative rotations.

            VEL - Relative linear velocities.

            OMG - Relative angular velocities.

            ACC - Relative linear accelerations.

            DMG - Relative angular accelerations.

            SMISC - Summable miscellaneous quantities.

        comp
            Component of the item (if required). For Item = DISP, ROT, VEL,
            OMG, ACC, and DMG, enter the direction label, X, Y, or Z. For Item
            = SMISC, enter a valid number.

        Notes
        -----
        Prints element output for the MPC184 joint element. The joint element
        quantities printed are the values for the free or unconstrained
        relative degrees of freedom.

        This command is valid in POST1 only.
        """
        command = f"PRJSOL,{item},{comp}"
        return self.run(command, **kwargs)

    def prnld(self, lab="", tol="", item="", **kwargs):
        """Prints the summed element nodal loads.

        APDL Command: PRNLD

        Parameters
        ----------
        lab
            Nodal reaction load type.  If blank, use the first ten of all
            available labels.  Valid labels are:

        tol
            Tolerance value about zero within which loads are not printed, as
            follows:

            > 0  - Relative tolerance about zero within which loads are not printed. In this case,
                   the tolerance is TOL * Load, where Load is the absolute
                   value of the maximum load on the selected nodes.

             0  -  Print all nodal loads.

            > 0  - Absolute tolerance about zero within which loads are not printed.

        item
            Selected set of nodes.

            (blank) - Prints the summed element nodal loads for all selected nodes (default),
                      excluding contact elements.

            CONT - Prints the summed element nodal loads for contact nodes only.

            BOTH - Prints the summed element nodal loads for all selected nodes, including contact
                   nodes.

        Notes
        -----
        Prints the summed element nodal loads (forces, moments, heat flows,
        flux, etc.) for the selected nodes in the sorted sequence.  Results are
        in the global Cartesian coordinate directions unless transformed
        [RSYS].  Zero values (within a tolerance range) are not printed.  Loads
        applied to a constrained degree of freedom are not included.  The FORCE
        command can be used to define which component of the nodal load is to
        be used (static, damping, inertia, or total).

        By default, PRNLD excludes elements TARGE169 - CONTA177. Setting ITEM =
        CONT will only account for nodal forces on selected contact elements
        (CONTA171 - CONTA177). Setting ITEM = BOTH will account for nodal
        forces on all selected nodes, including contact nodes.
        """
        command = f"PRNLD,{lab},{tol},{item}"
        return self.run(command, **kwargs)

    def prnsol(self, item="", comp="", **kwargs):
        """Prints nodal solution results.

        APDL Command: PRNSOL

        Parameters
        ----------
        item
            Label identifying the item.  Valid item labels are shown in
            Table 225: PRNSOL - Valid Item and Component Labels below.  Some
            items also require a component label.

        comp
            Component of the item (if required).  Valid component labels are
            shown in Table 225: PRNSOL - Valid Item and Component Labels below.
            Defaults to COMP.

        Notes
        -----
        Prints the nodal solution results for the selected nodes in the sorted
        sequence. For example, PRNSOL,U,X prints the X component of
        displacement vector U (that is, the UX degree of freedom). Component
        results are in the global Cartesian coordinate directions unless
        transformed (RSYS). Various element results also depend upon the
        recalculation method and the selected results location (AVPRIN, RSYS,
        LAYER, SHELL, and NSEL). If the LAYER command is issued, then the
        resulting output is listed in full graphics mode (/GRAPHICS,FULL). You
        can use the FORCE command to define which component of the nodal load
        (static, damping, inertia, or total) should be used.

        PowerGraphics can affect your nodal solution listings. For
        PowerGraphics (/GRAPHICS,POWER), results are listed only for the model
        exterior surfaces.

        When shell element types are present, results are output on a surface-
        by-surface basis. For shell elements, such as SHELL181 or SHELL281, and
        for ELBOW290, printed output is for both the top and bottom surfaces.
        For solid elements such as SOLID185, the output is averaged for each
        surface and printed as follows:

        For a node at a vertex, three lines are output (one printed line for
        each surface).

        For a node on an edge, two lines are output (one printed line for each
        surface).

        For nodes on a face, one value is output.

        For nodes interior to the volume, no printed values are output.

        If a node is common to more than one element, or if a geometric
        discontinuity exists, several conflicting listings may result. For
        example, a corner node incorporating results from solid elements and
        shell elements could yield as many as nine different results; the
        printed output would be averages at the top and bottom for the three
        shell surfaces plus averages at the three surfaces for the solid, for a
        total of nine lines of output. ANSYS does not average result listings
        across geometric discontinuities when shell element types are present.
        It is important to analyze the listings at discontinuities to ascertain
        the significance of each set of data.

        The printed output for full graphics (/GRAPHICS,FULL) follows the
        standard ANSYS convention of averaging results at the node.  For shell
        elements, the default for display is TOP so that the results for the
        top of the shell are averaged with the other elements attached to that
        node.

        If an NSORT, ESORT or /ESHAPE command is issued with PowerGraphics
        activated, then the PRNSOL listings will be the same as in full
        graphics mode (/GRAPHICS,FULL). The items marked with [2] are not
        supported by PowerGraphics. To print midside nodes, you must first
        issue an /EFACET,2 command.

        Table: 225:: : PRNSOL - Valid Item and Component Labels

        Failure criteria  [2][4].

        Default components: Maximum of all failure criteria defined at current
        location (MAX), maximum strain (EMAX), maximum stress (SMAX), Tsai-Wu
        Strength Index (TWSI), inverse of Tsai-Wu Strength Ratio Index (TWSR).
        """
        command = f"PRNSOL,{item},{comp}"
        return self.run(command, **kwargs)

    def prrfor(self, lab="", **kwargs):
        """Prints the constrained node reaction solution. Used with the FORCE

        APDL Command: PRRFOR
        command.

        Parameters
        ----------
        lab
            Nodal reaction load type.  If blank, use the first ten of all
            available labels. Valid labels are:

        Notes
        -----
        PRRFOR has the same functionality as the PRRSOL command; use PRRFOR
        instead of PRRSOL when a FORCE command has been issued.

        In a non-spectrum analysis, if either contact or pretension elements
        exist in the model, PRRFOR uses the PRRSOL command internally and the
        FORCE setting is ignored.

        Because modal displacements cannot be used to calculate contact element
        nodal forces,: those forces are not included in the spectrum and PSD
        analyses reaction solution. As a consequence, the: PRRFOR: command is
        not supported when constraints on contact element pilot nodes are
        present.
        """
        command = f"PRRFOR,{lab}"
        return self.run(command, **kwargs)

    def prrsol(self, lab="", **kwargs):
        """Prints the constrained node reaction solution.

        APDL Command: PRRSOL

        Parameters
        ----------
        lab
            Nodal reaction load type.  If blank, use the first ten of all
            available labels. Valid labels are:

        Notes
        -----
        Prints the constrained node reaction solution for the selected nodes in
        the sorted sequence.  For coupled nodes and nodes in constraint
        equations, the sum of all reactions in the coupled or constraint
        equation set  appears at the primary node of the set.  Results are in
        the global Cartesian coordinate directions unless transformed (RSYS).

        PRRSOL is not valid if any load is applied to a constrained node in the
        direction of the constraint and any of the following is true:

        LCOPER has been used.

        LCASE has been used to read from a load case file.

        The applied loads and constraints in the database are not the ones used
        to create the results data being processed.

        PRRSOL provides the total reaction solution (static, plus damping, plus
        inertial, as appropriate based on the analysis type); however, modal
        reactions include only the static contribution.

        Use PRRFOR instead of PRRSOL with the FORCE command to obtain only the
        static, damping, or inertial components.
        """
        command = f"PRRSOL,{lab}"
        return self.run(command, **kwargs)

    def prvect(self, item="", lab2="", lab3="", labp="", **kwargs):
        """Prints results as vector magnitude and direction cosines.

        APDL Command: PRVECT

        Parameters
        ----------
        item
            Predefined vector item (from Table 226: PRVECT - Valid Item and
            Component Labels below) or a label identifying the i-component of a
            user-defined vector.

        lab2
            Label identifying the j-component of a user-defined vector. In most
            cases, this value must be blank if Item is selected from
            Table 226: PRVECT - Valid Item and Component Labels. Individual
            principal stresses (Item = S) or principal strains (Item = EPxx)
            may be printed by specifying the value as 1, 2, or 3.

        lab3
            Label identifying the k-component of a user-defined vector.  Must
            be blank if Item is selected from list below or for 2-D user
            defined vector.

        labp
            Label assigned to resultant vector for printout labeling (defaults
            to Item).

        Notes
        -----
        Prints various solution results as vector magnitude and direction
        cosines for the selected nodes and/or elements.  For example, PRVECT,U
        prints the displacement magnitude and its direction cosines for all
        selected nodes.  For nodal degree of freedom vector results, direction
        cosines are with respect to the results coordinate system RSYS. For
        element results, direction cosines are with respect to the global
        Cartesian system. Item components may be printed with the PRNSOL
        command.  Various results also depend upon the recalculation method and
        the selected results location [LAYER, SHELL, NSEL, and ESEL].  Items
        may be selected from a set of recognized vector labels (Item) or a
        vector may be defined from up to three scalar labels (Item,Lab2,Lab3).
        Scalar labels may be user-defined with the ETABLE command.

        Portions of this command are not supported by PowerGraphics
        [/GRAPHICS,POWER].

        Table: 226:: : PRVECT - Valid Item and Component Labels
        """
        command = f"PRVECT,{item},{lab2},{lab3},{labp}"
        return self.run(command, **kwargs)

    def sumtype(self, label="", **kwargs):
        """Sets the type of summation to be used in the following load case

        APDL Command: SUMTYPE
        operations.

        Parameters
        ----------
        label
            Summation type

            COMP - Combine element component stresses only.  Stresses such as average nodal
                   stresses, principal stresses, equivalent stresses, and
                   stress intensities are derived from the combined element
                   component stresses. Default.

            PRIN - Combine principal stress, equivalent stress, and stress intensity directly as
                   stored on the results file.  Component stresses are not
                   available with this option.

        Notes
        -----
        Issue SUMTYPE,PRIN when you want to have a load case operation (LCOPER)
        act on the principal / equivalent stresses instead of the component
        stresses. Also issue SUMTYPE,PRIN when you want to read in load cases
        (LCASE). Note that the SUMTYPE setting is not maintained between /POST1
        sessions.

        SUMTYPE,PRIN also causes principal nodal values to be the average of
        the contibuting principal element nodal values (see AVPRIN,1).

        BEAM188 and BEAM189 elements compute principal stress, equivalent
        stress, and stress intensity values on request instead of storing them
        on the results file;  SUMTYPE,PRIN does not apply for these elements.
        """
        command = f"SUMTYPE,{label}"
        return self.run(command, **kwargs)
