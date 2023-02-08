class SpecialPurpose:
    def aerocoeff(
        self,
        aeromodetype="",
        aeromappedfilenames="",
        aerospecs="",
        aeroscalar="",
        nblades="",
        autofileread="",
        **kwargs,
    ):
        """Computes the aero-damping and stiffness coefficients and
        writes them to an APDL array.

        APDL Command: AEROCOEFF

        Parameters
        ----------
        aeromodetype
            Mode type to be used.

            * ``"blade"`` : Non-cyclic cantilevered blade mode (default)

        aeromappedfiles
            Name of string array containing file names of mapped pressures
            from CFD. The file names should be ordered to correspond to
            the AeroSpecs array.

        aerospecs
            Name of numerical array containing data organized to correspond to
            the AeroMappedFiles array.

        aeroscalar
            Scaling value(s) to handle any modal scaling difference
            between structural and CFD modes. The values can be entered as
            a scalar or 1-dimensional array. (each scaling value defaults
            to 1)

        nblades
            Number of blades.

        autofileread
            Key to automatically read and use values from CFD file header.

            *  0 (OFF or NO) : Do not read scaling values or nodal diameter
               from the CFD file header. (default)
            * 1 (ON or YES) : Read scaling values (labeled Mode Multiplier
              in CFD file) from CFD file header. The scaling values read
              will be used in calculations and the AeroScalar input will
              be ignored. The nodal diameter values will be used to cross
              check the value of i (input through AeroSpecs array).

        Notes
        -----
        The AEROCOEFF command is designed to generate an array of
        aerodynamic coefficients that can be used in a cyclic
        mode-superposition harmonic response analysis using the CYCFREQ
        , AERO command to represent aerodynamic stiffness and
        damping. These aerodynamic coefficients can also be used in a damped
        modal analysis phase (CYCFREQ, MODAL) of a cyclic
        mode-superposition harmonic solve. An APDL array called
        JobnameAeroArray is generated using the AEROCOEFF command.  This array
        is compatible with the array needed for the CYCFREQ, AERO command.
        The format of the written array follows that of the CYCFREQ, AERO
        command. The array is formatted as follows:
        ``i, m, n, V_real, V_imag``

        where
        ``i`` = the i th interblade phase angle (IBPA)
        ``m`` = the m th vibrating blade mode
        ``n`` = the n th blade mode generating the pressure oscillations

        ``Vreal`` and ``V_imag`` = the real and imaginary coefficients.

        Prior to issuing the AEROCOEFF command, a non-cyclic cantilevered
        blade modal analysis must be run, either stress-free or
        prestressed using linear perturbation. For more information, see
        Modal Analysis in the Structural Analysis Guide. The file
        requirements for the AEROCOEFF command are the same as those
        needed for modal restart as described in Modal Analysis Restart.
        The AeroSpecs values are specified in a 3×r array ``*DIM``,
        where r is a positive integer equal to the number of interblade
        phase angles and the pressure modes solved for in the CFD
        analysis.

        Each row has the structure: ``i, m, n``
        where
        ``i`` = the i th interblade phase angle (IBPA)
        ``m`` = the m th vibrating blade mode
        ``n`` = the n th blade mode generating the pressure oscillations

        At least one aerodynamic damping coefficient must be specified for
        each IBPA (equal to the number of blades) while keeping and
        constant. If a value is not specified, the program writes an array
        value of zero for both and . The values of and are relative to the
        modes computed in the re- quired modal analysis.

        The number of AeroScalar values must be equal to the number of
        pressure modes ( from Aero- Specs). If the number of AeroScalar
        values is greater than 1, the values must be entered by defining
        an array ``*DIM`` and entering the array name in the AeroScalar
        field. For a discussion of how AeroScalar values are computed, see
        Scaling Aerodynamic Coupling Coefficients.

        The value for nBlades should be equal to the number of sectors of
        the system. If there are multiple blades per cyclic sector, then
        the combination of blades on the single sector will have an aero
        coefficient value. In this case, each blade will not have a
        distinct aero coefficient.
        """
        command = f"AEROCOEFF,{aeromodetype},{aeromappedfilenames},{aerospecs},{aeroscalar},{nblades},{autofileread}"
        return self.run(command, **kwargs)

    def cint(
        self,
        action="",
        par1="",
        par2="",
        par3="",
        par4="",
        par5="",
        par6="",
        par7="",
        **kwargs,
    ):
        """Defines parameters associated with fracture parameter calculations

        APDL Command: CINT

        Parameters
        ----------
        action
            Specifies action for defining or manipulating initial crack data:

            NEW - Initiate a new calculation and assign an ID.

            CTNC - Define the crack tip node component.

            CENC - Define the crack extension node component, the crack tip node, and the crack
                   extension direction.

            TYPE - Define the type of calculation to perform.

            DELE - Delete the CINT object associated with the specified ID.

            NCON - Define the number of contours to be calculated in the contour-integral
                   calculation.

            SYMM - Indicate whether the crack is on a symmetrical line or plane.

            NORM - Define the crack plane normal.

            UMM - Activate or deactivate the unstructured mesh method.

            EDIR - Crack-assist extension direction.

            PLOT - Plots crack front and crack tip coordinate system.

            CXFE - Define the crack tip element or crack front element set. Valid for XFEM-based
                   crack-growth analysis only.

            RADIUS - Define the radius at which the given value is to be evaluated. Valid for XFEM-
                     based crack-growth analysis only.

            RSWEEP - Define the minimum and maximum sweep angle from existing crack direction. Valid
                     for XFEM-based crack-growth analysis only.
        """
        command = f"CINT,{action},{par1},{par2},{par3},{par4},{par5},{par6},{par7}"
        return self.run(command, **kwargs)

    def cycfreq(
        self,
        option="",
        value1="",
        value2="",
        value3="",
        value4="",
        value5="",
        **kwargs,
    ):
        """Specifies solution options for a cyclic symmetry mode-superposition

        APDL Command: CYCFREQ
        harmonic analysis.

        Parameters
        ----------
        option
            One of the following options:

            AERO - Specify the array containing the aerodynamic damping coefficients.

            Value1 - The name of the array containing the aerodynamic stiffness damping
                     coefficients.

            BLADE - Blade information required for a mistuning analysis.

            Value1 - The name of the nodal component containing the blade boundary nodes at the
                     blade-to-disk interface. Also include boundary nodes at
                     any shroud interfaces.

            Value2 - The name of the element component containing the blade elements.

            Value3 - The number of blade modes to include in the CMS reduction.

            Value4 - The lower bound of the frequency range of interest. This value is optional.

            Value5 - The upper bound of the frequency range of interest. This value is optional.

            DEFAULT - Set the default cyclic harmonic solution settings.

            EO - Excitation engine order.

            Value1 - The value of the excitation order, which must be an integer. The loadings on
                     the other sectors will be related to the loading on the
                     basic sector based on the engine order phase shift.

            MIST - Mistuning parameters.

            Value1 - The type of mistuning:

            K - Stiffness (frequency) mistuning

            Value2 - The name of the array containing the stiffness mistuning parameters.

            MODAL - Specifies if a damped modal analysis should be performed on the reduced system.

            Value1 - On/Off key.

            0 (OFF or NO) - No modal solution. Perform the harmonic solution.

            1 (ON or YES) - Perform a damped modal analysis of the reduced system in order to obtain the
                            complex frequencies. The harmonic solution is not
                            performed.

            Value2 - Number of modes for the damped modal analysis.

            Value3 - The beginning, or lower end, of the frequency range of interest (in Hz).

            Value4 - The ending, or upper end, of the frequency range of interest (in Hz).

            RESTART - Defines the point at which to restart the harmonic analysis.

            Value1 - The restart point:

            OFF - No restart (default)

            SWEEP - Restart for a new frequency sweep range (HARFRQ)

            MIST - Restart for new mistuning parameters (new mistuning arrays)

            USER - Causes the program to call for a user-defined solution.

            Value1-5 - Values passed down to the user-defined solution.

            STATUS - List the harmonic solution option settings active for the cyclic model.

        Notes
        -----
        The program solves a cyclically symmetric model (set up via the CYCLIC
        command during preprocessing) at the harmonic indices specified via the
        CYCOPT command.

        The aerodynamic coefficients are specified in a 5×(N×r) array (``*DIM``),
        where N is the number of blades and r can be any positive integer. Each
        column has the structure:

        where:

        One aerodynamic damping coefficient must be specified for each IBPA
        (equal to the number of blades) while keeping m and n constant.

        For constant (frequency-independent) mistuning, the stiffness
        parameters are specified in an N×1 array (``*DIM``) where N is the number
        of blades.

        For stiffness mistuning, each row entry represents the deviation of
        Young’s modulus from nominal,  (or equivalently, the ratio of the
        frequency deviation squared). Each frequency can also be independently
        mistuned, in which case the array is N×M, where M is the number of
        blade frequencies (Value3 of CYCFREQ,BLADE). The entries in each row
        therefore correspond to the ratio of the mistuned frequency to the
        tuned frequency squared minus one:

        The USER option activates the solution macro CYCMSUPUSERSOLVE.MAC. The
        normal solution is skipped. You may implement your own mistuning
        solution using APDL and APDL Math operations, or call your own program
        for the solution.

        The CYCFREQ command is valid in the preprocessing and solution stages
        of an analysis.

        The CYCFREQ,MODAL,ON command writes modal frequencies to the output
        file. No other postprocessing is available for this modal solve.

        When using CYCFREQ,RESTART, only mistuning parameters or frequency
        range may be changed. All other changes in parameters are ignored.

        To learn more about analyzing a cyclically symmetric structure, see the
        Cyclic Symmetry Analysis Guide.
        """
        command = f"CYCFREQ,{option},{value1},{value2},{value3},{value4},{value5}"
        return self.run(command, **kwargs)

    def cyclic(
        self,
        nsector="",
        angle="",
        kcn="",
        name="",
        usrcomp="",
        usrnmap="",
        **kwargs,
    ):
        """Specifies a cyclic symmetry analysis.

        APDL Command: CYCLIC

        Parameters
        ----------
        nsector
            The number of sectors in the full 360 degrees, or one of the
            following options:

            STATUS - Indicates the current cyclic status.

            OFF - Resets model to normal (non-cyclic) status and removes the duplicate sector if
                  it exists. This option also deletes automatically detected
                  edge components (generated when USRCOMP = 0).

            UNDOUBLE - Removes the duplicate sector if it exists. The duplicate sector is created
                       during the solution (SOLVE) stage of a modal cyclic
                       symmetry analysis.

        angle
            The sector angle in degrees.

        kcn
            An arbitrary reference number assigned to the cyclic coordinate
            system.  The default value of 0 specifies automatic detection.

        name
            The root name of sector low- and high-edge components (line, area,
            or node components). The default root name (when USRCOMP = 0) is
            "CYCLIC". A root name that you specify can contain up to 11
            characters.

        usrcomp
            The number of pairs of user-defined low- and high-edge components
            on the cyclic sector (if any). The default value of 0 specifies
            automatic detection of sector edges; however, the automatic setting
            is not valid in all cases. (For more information, see the Notes
            section below.) If the value is greater than 0, no verification of
            user-defined components occurs.

        usrnmap
            The name of a user-defined array specifying the matching node pairs
            between the sector low and high edges. Valid only when USRCOMP = 0.
            Skips the automatic detection of sector edges. Node pairs may be
            input in any order, but the low edge node must be the first entry
            in each pair.

        Notes
        -----
        You can input your own value for NSECTOR, ANGLE or KCN; if you do so,
        the command verifies argument values before executing.

        When USRCOMP = 0 and USRNMAP = blank (default), the CYCLIC command
        automatically detects low- and high-edge components for models
        comprised of any combination of line, area, or volume elements. If a
        solid model exists, however, the  command uses only the lines, areas,
        and/or volumes to determine the  low- and high-edge components; the
        elements, if any, are ignored.

        Nodes will be automatically rotated unless CYCOPT,USERROT,YES has been
        specified.

        If you issue a CYCOPT,TOLER command to set a tolerance for edge-
        component pairing before issuing the CYCLIC command, the CYCLIC command
        uses the specified tolerance when performing automatic edge-component
        detection.

        For 2-D models, autodetection does not consider the CSYS,5 or CSYS,6
        coordinate system specification.  Autodetection for 180 degree (two-
        sector) models is not possible unless a central hole exists.

        The CYCLIC command sets values and keys so that, if possible, the area-
        mesh (AMESH) or volume-mesh (VMESH) command meshes the sector with
        matching node and element face patterns on the low and high edges. (The
        command has no effect on any other element-creation command.)

        Issue the CYCLIC command prior to the meshing command to, if possible,
        produce a mesh with identical node and element patterns on the low and
        high sector edges. Only the AMESH or VMESH commands can perform
        automated matching. (Other meshing operation commands such as VSWEEP
        cannot.) If you employ a meshing operation other than AMESH or VMESH,
        you should ensure that node and element face patterns match, if
        desired. The CYCLIC command output indicates whether each edge-
        component pair has or can produce a matching node pair.

        A cyclic solution (via the SOLVE command) allows dissimilar mesh
        patterns on the extreme boundaries of a cyclically symmetric model. The
        allowance for dissimilar patterns is useful when you have only finite-
        element meshes for your model but not the geometry data necessary to
        remesh it to obtain identical node patterns. In such cases, it is
        possible to obtain solution results, although perhaps at the expense of
        accuracy. A warning message appears because results may be degraded
        near the sector edges.

        The constraint equations (CEs) that tie together the low and high edges
        of your model are generated at the solution stage of the analysis from
        the low- and high-edge components (and nowhere else). You should verify
        that automatically detected components are in the correct  locations
        and that you can account for all components; to do so, you can list
        (CMLIST) or plot (CMPLOT) the components.

        If you issue the CYCLIC command after meshing and have defined element
        types with rotational degrees of freedom (DOFs), ANSYS generates cyclic
        CEs for rotational DOFs that may not exist on the sector boundaries.
        Issue the CYCOPT,DOF command to prevent unused rotational terms from
        being generated.

        Modal cyclic symmetry analysis is supported by the following
        eigensolvers:

        Block Lanczos (MODOPT,LANB)

        PCG Lanczos (MODOPT,LANPCG)

        Super Node (MODOPT,SNODE)

        Subspace (MODOPT,SUBSP)

        To learn more about analyzing a cyclically symmetric structure, see the
        Cyclic Symmetry Analysis Guide.

        When using the: CYCLIC: command to automatically detect the sector, if
        an area is defined with the: AL: command, the lines need to be oriented
        to form the closed curve.
        """
        command = f"CYCLIC,{nsector},{angle},{kcn},{name},{usrcomp},{usrnmap}"
        return self.run(command, **kwargs)

    def cycopt(
        self,
        option="",
        value1="",
        value2="",
        value3="",
        value4="",
        value5="",
        value6="",
        value7="",
        **kwargs,
    ):
        """Specifies solution options for a cyclic symmetry analysis.

        APDL Command: CYCOPT

        Parameters
        ----------
        option
            One of the following options:

            BCMULT - Controls whether cyclic sector array parameter names are reused or created new
                     for multiple entities.

            Value1 - The flag value.

            0 (OFF or NO) - Create new array parameter names (default)

            1(ON or YES) - Reuse array parameter names

            COMBINE - For linear static cyclic symmetry analysis with non-cyclically symmetric
                      loading only, expands and combines all harmonic index
                      solutions and writes them to the results file during the
                      solution phase of the analysis.

            Value1 - The flag value.

            0 (OFF or NO) - Disable combining of harmonic index solutions (default)

            1 (ON or YES) - Enable combining of harmonic index solutions

            DEFAULT - Set the default cyclic solution settings.

            DOF - The degrees of freedom to couple from the nodes on the low sector boundary to
                  nodes on the high boundary:

            Value1 - The component pair ID number.

            Value2, Value3, Value4,  . . . ,  Value7 - The constraint-equation/-coupling degree of freedom (DOF) for this pair. Repeat
                              the command to add other DOFs. The default is
                              constraint-equation/-coupling all applicable
                              DOFs.

            FACETOL - Tolerance for inclusion of surface nodes into your basic sector. Autodetect
                      defaults to 15°, accommodating most sections. Specify a
                      new Value1 only when extreme cut angles or complex model
                      geometry cause surface nodes to be excluded. See Notes
                      (below) for more information.

            ANSYS, Inc. recommends that successful auto-detection depends more on the value of ANGTOL than the value of FACETOL. Please refer to CYCOPT Auto Detection Tolerance Adjustments for Difficult Cases for more information about auto-detection and the CYCOPT command. - Value1

            The face tolerance applies only to auto detection from node/element models (already meshed and no solid model), and it defaults to 15°.   - HINDEX

            The harmonic index solution ranges for modal or buckling cyclic symmetry analyses. The SOLVE command initiates a cyclic symmetry solution sequence at the harmonic indices specified. (By default, the SOLVE command solves for all available harmonic indices.) Static and harmonic cyclic symmetry solutions always use all harmonic indices required for the applied loads. - EVEN / ODD

            For low-frequency electromagnetic analysis only, EVEN specifies a symmetric solution and ODD specifies an antisymmetric solution.  - The value you specify is based on the harmonic index: EVEN (default) indicates
                              harmonic index = 0, and ODD indicates harmonic
                              index = N / 2 (where N is an integer representing
                              the number of sectors in 360°). A value of ODD
                              applies only when N is an even number.

            The CYCOPT command with this HINDEX option is cumulative. To remove an option (for example, EVEN), issue this command: CYCOPT,HINDEX,EVEN,,,-1 - ALL

            Solve all applicable harmonic indices. - Note:  Value2 must be blank.

            Value1, Value2, Value3 - Solve harmonic indices in range Value1 through Value2 in steps of Value3.
                              Repeat the command to add other ranges. The
                              default solves all applicable harmonic indices.

            Value4 - The only valid value is -1. If specified, it removes Value1 through Value2 in
                     steps of Value3 from the set to solve. By default, if
                     Value4 = -1 then Value1 = 0, Value2 = 0, and Value3 = 1.

            Value5 - For static and harmonic analyses, the tolerance for determining if a Fourier
                     contribution of a load contributes to the response
                     (default = 1.0E-5).

            If Value5=STATIC, it forces the program to solve only the specified harmonic indices (even if a load may have a Fourier contribution in an index not specified). - LDSECT

            Restricts subsequently defined force loads and surface loads to a specified sector. The restriction remains in effect until you change or reset it. This option is not available for harmonic analyses based on mode-superposition (CYCOPT,MSUP,1) - Value1

            The sector number. A value other than 0 (default) is valid for a cyclic symmetry analysis with non-cyclically symmetric loading only. A value of 0 (or ALL) resets the default behavior for cyclic loading (where the loads are identical on all sectors). - MOVE

            Specifies if the program should move high- or low-edge component nodes paired within the specified tolerance (TOLER) to create precisely matching pairs.  - Value1

            The flag value. - 0

            Do not move edge component nodes (default) - 1 or HIGH

            Move the high-edge component nodes to precisely match the low-edge component nodes - -1 or LOW

            Move the low-edge component nodes to precisely match the high-edge component nodes - MSUP

            For modal cyclic symmetry analysis only, this flag is used to limit the results written to the Jobname.MODE and Jobname.RST files in preparation for a subsequent mode-superposition-based analysis. In a linear perturbation modal analysis, this option must be specified in the first load step of the preceding base analysis.  - m
        """
        command = f"CYCOPT,{option},{value1},{value2},{value3},{value4},{value5},{value6},{value7}"
        return self.run(command, **kwargs)

    def emsym(self, nsect="", **kwargs):
        """Specifies circular symmetry for electromagnetic sources.

        APDL Command: EMSYM

        Parameters
        ----------
        nsect
            The number of circular symmetry sections (defaults to 1).

        Notes
        -----
        Specifies the number of times to repeat electromagnetic sources for
        circular symmetry. Applies to SOURC36 elements and to coupled-field
        elements with electric current conduction results in the database.
        Sources are assumed to be equally spaced over 360° about the global
        Cartesian Z axis.

        This command is also valid in SOLUTION.
        """
        command = f"EMSYM,{nsect}"
        return self.run(command, **kwargs)

    def mstole(self, method="", namesurf="", namefluid="", **kwargs):
        """Adds two extra nodes from FLUID116 elements to SURF151 or SURF152

        APDL Command: MSTOLE
        elements for convection analyses.

        Parameters
        ----------
        method
            Mapping method:

            0 - Hybrid method (default).

            1 - Projection method.

            2 - Minimum centroid distance method.

        namesurf
            Component name for a group of SURF151 or SURF152 elements. The name
            must be enclosed in single quotes (e.g., 'COM152') when the MSTOLE
            command is manually typed in.

        namefluid
            Component name for a group of FLUID116 elements. The name must be
            enclosed in single quotes (e.g., 'COM116') when the MSTOLE command
            is manually typed in.

        Notes
        -----
        For convection analyses, the MSTOLE command adds two extra nodes from
        FLUID116 elements to SURF151 or SURF152 elements by employing the
        specified mapping method. In the hybrid method, the projection method
        is tried first and if it fails the centroid distance method is used.
        The SURF151 or SURF152 elements and the FLUID116 elements must be
        grouped into components and named using the CM command.

        The SURF151 or SURF152 extra node option must be set for two extra
        nodes (KEYOPT(5) = 2).

        For more information, see Using the Surface Effect Elements in the
        Thermal Analysis Guide.
        """
        command = f"MSTOLE,{method},{namesurf},{namefluid}"
        return self.run(command, **kwargs)

    def perbc2d(
        self,
        loc1="",
        loc2="",
        loctol="",
        r1="",
        r2="",
        tolr="",
        opt="",
        plnopt="",
        **kwargs,
    ):
        """Generates periodic constraints for 2-D planar magnetic field analyses.

        APDL Command: PERBC2D

        Parameters
        ----------
        loc1
            Constant coordinate location of the first plane of nodes.  For
            PLNOPT = 1 or 2, the constant coordinate location is the global
            Cartesian coordinate system [CSYS,0] location in the X or Y
            direction respectively.  For PLNOPT = 0, the location is the angle
            in the global cylindrical coordinate system [CSYS,1].

        loc2
            Constant coordinate location of the second plane of nodes.  For
            PLNOPT  = 1 or 2, the constant coordinate location is the global
            Cartesian coordinate system [CSYS,0] location in the X or Y
            direction respectively.  For PLNOPT = 0, the location is the angle
            (in degrees) in the global cylindrical coordinate system [CSYS,1].

        loctol
            Tolerance on the constant coordinate location for node selection.
            Defaults to .00001 for PLNOPT  = 1 or 2 and .001 degrees for PLNOPT
            = 0.

        r1
            Minimum coordinate location along the second plane of nodes.  For
            PLNOPT = 1 or 2, the coordinate location is the global Cartesian
            coordinate system location in the Y or X direction respectively.
            For PLNOPT = 0, the coordinate location is the radial coordinate
            value in the global cylindrical coordinate system.   Periodic
            conditions are not applied to nodes at this location.

        r2
            Maximum coordinate location along the second plane of nodes.  For
            PLNOPT = 1 or 2, the coordinate location is the global Cartesian
            coordinate system location in the Y or X direction respectively.
            For PLNOPT = 0, the coordinate location is the radial coordinate
            value in the global cylindrical coordinate system. Periodic
            conditions are not applied to nodes at this location.

        tolr
            Tolerance dimension on node selection along the plane of nodes.
            Defaults to .00001.

        opt
            Periodic option:

            0 - Odd symmetry (default).  Apply constraint equations such that AZ(i) = -AZ(j).

            1 - Even symmetry.  Apply node coupling such that AZ(i) = AZ(j).

        plnopt
            Symmetry plane option:

            0 - Planes of constant angle in the global cylindrical coordinate system [CSYS,1].

            1 - Planes parallel to the global Cartesian X axis [CSYS,0].

            2 - Planes parallel to the global Cartesian Y axis [CSYS,0].

        Notes
        -----
        PERBC2D invokes an ANSYS macro which generates periodic boundary
        condition constraints for 2-D planar magnetic field analysis.  The
        macro is restricted to node pairs sharing common coordinate values
        along symmetry planes separated by a constant coordinate value.  Planes
        (or lines) must lie at either constant  angles (PLNOPT = 0), constant X
        values (PLNOPT = 1), or constant Y values (PLNOPT = 2).  PERBC2D
        applies constraint equations (OPT = 0, odd symmetry) or node coupling
        (OPT = 1, even symmetry) to each node pair sharing a common coordinate
        value along the symmetry planes.  By default, periodic conditions are
        not applied at the first and last node pairs on the symmetry planes
        unless the input location values, R1 and R2, are adjusted to be less
        than or greater than the actual node coordinate values.  Nodes are
        selected for application of the constraints using the NSEL command with
        tolerances on the constant coordinate location (LOCTOL) and the
        coordinate location along the plane (RTOL).

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"PERBC2D,{loc1},{loc2},{loctol},{r1},{r2},{tolr},{opt},{plnopt}"
        return self.run(command, **kwargs)

    def physics(self, option="", title="", fname="", ext="", **kwargs):
        """Writes, reads, or lists all element information

        APDL Command: PHYSICS

        Parameters
        ----------
        option
            Specifies what to do with element information:

            WRITE - Write all appropriate element types, key options,
                    real constants, material properties, solution
                    analysis options, load step options, constraint
                    equations, coupled nodes, defined components, and
                    GUI preference settings to the file specified with
                    the Fname and Ext arguments.

            READ - Deletes all solution information (material
                   properties, solution options, load step options,
                   constraint equations, coupled nodes, results, and
                   GUI preference settings) then reads all the
                   information listed above into the ANSYS database
                   from the location specified by the Fname and Ext
                   arguments.

            LIST - Lists currently defined physics files and their titles.

            DELETE - Deletes a specified physics file and its title
                     from the database.

            CLEAR - Deletes all material properties, solution options,
                    load step options, constraint equations, coupled
                    nodes, results, and GUI preference settings from
                    the database. Does NOT clear the active physics
                    file title from the database.

            STATUS - Displays information about all active elements
                     and settings.

        title
            A user-defined title that quickly identifies a set of
            physics settings.  For example, you might use "Fluid,"
            "Structural," or "Magnetic" as titles.  A title can
            contain up to 64 characters. It can be entered in lower or
            upper case. Lower case is internally converted to upper
            case within the program.

        fname
            File name and directory path (248 characters maximum,
            including the characters needed for the directory path).
            An unspecified directory path defaults to the working
            directory; in this case, you can use all 248 characters
            for the file name.

        ext
            Filename extension (eight-character maximum).

        Notes
        -----
        Use the PHYSICS command when you are performing a multiphysics
        analysis that involves two different disciplines (for example,
        magnetic and structural analyses) and you cannot solve both
        analyses simultaneously.  Once you have set up physics
        environments for both analyses, you can use the PHYSICS,READ
        command to change between the defined physics environments.
        For more information about doing multiphysics analyses, see
        Sequential Coupled-Field Analysis in the Coupled-Field
        Analysis Guide.

        The PHYSICS command outputs all solution information,
        including analysis options, to the Jobname.PHn file described
        above.  Although it also outputs components, the ANSYS program
        does not list entities (nodes, elements, lines, etc.).

        PHYSICS,WRITE will overwrite existing physics files with the
        same title (even if the name is different). In other words, if
        the directory has a physics file with the same title as the
        active physics file title, but a different name, the
        PHYSICS,WRITE command will overwrite the existing physics file
        and use the existing filename, not the filename specified on
        the PHYSICS,WRITE command.
        """
        command = f"PHYSICS,{option},{title},{fname},{ext}"
        return self.run(command, **kwargs)

    def race(self, xc="", yc="", rad="", tcur="", dy="", dz="", cname="", **kwargs):
        """Defines a "racetrack" current source.

        APDL Command: RACE

        Parameters
        ----------
        xc
            Location of the mid-thickness of the vertical leg along the working
            plane X-axis.

        yc
            Location of the mid-thickness of the horizontal leg along the
            working plane Y-axis.

        rad
            Radius of curvature of the mid-thickness of the curves in the
            racetrack source.  Defaults to .501 * DY

        tcur
            Total current, amp-turns (MKS), flowing in the source.

        dy
            In-plane thickness of the racetrack source.

        dz
            Out-of-plane thickness (depth) of the racetrack source.

        cname
            An alphanumeric name assigned as a component name to the group of
            SOURC36 elements created by the command macro.  Cname must be
            enclosed in single quotes in the RACE command line.  Cname may be
            up to 32 characters, beginning with a letter and containing only
            letters, numbers, and underscores.  Component names beginning with
            an underscore (e.g., _LOOP) are reserved for use by ANSYS and
            should be avoided.  If blank, no component name is assigned.

        Notes
        -----
        RACE invokes an ANSYS macro which defines a "racetrack" current source
        in the working plane coordinate system.  The current source is
        generated from bar and arc source primitives using the SOURC36 element
        (which is assigned the next available element type number).  The macro
        is valid for use in 3-D magnetic field analysis using a scalar
        potential formulation.  Current flows in a counterclockwise direction
        with respect  to the working plane.

        The diagram below shows you a racetrack current source.
        """
        return self.run(f"RACE,{xc},{yc},{rad},{tcur},{dy},{dz},,,{cname}", **kwargs)

    def sstate(
        self,
        action="",
        cm_name="",
        val1="",
        val2="",
        val3="",
        val4="",
        val5="",
        val6="",
        val7="",
        val8="",
        val9="",
        **kwargs,
    ):
        """Defines a steady-state analysis.

        APDL Command: SSTATE

        Parameters
        ----------
        action
            Action to perform for defining or manipulating steady-state
            analysis data:

            DEFINE - Define steady-state analysis data

            LIST - List current steady-state analysis data

            DELETE - Delete steady-state analysis data

        cm_name
            Element component name

        val1, ..., val9
            Input values (based on the Action type)

        Notes
        -----
        The SSTATE command specifies steady-state analysis parameters for the
        given element component. The program runs the steady-state analysis if
        the corresponding element key option is enabled for that element
        component.

        The command supports the following elements:

        SOLID185

        3-D 8-Node Structural Solid

        SOLID186

        3-D 20-Node Structural Solid

        SOLID187

        3-D 10-Node Tetrahedral Structural Solid

        SOLSH190

        3-D 8-Node Structural Solid Shell

        Degenerated shape (prism) option not supported.

        SOLID285

        3-D 4-Node Tetrahedral Structural Solid with Nodal Pressures

        For information about steady-state rolling for rebar and solid
        elements, see Steady State Rolling in the Mechanical APDL Theory
        Reference.

        The following data types can be defined:

        SPIN -- Steady-state spinning motion

        TRANSLATE -- Rigid body motion (velocity) that the spinning component
        is undergoing

        Define the steady-state spinning motion:

        SSTATE, DEFINE, CM_Name, SPIN, OMEGA, Method, Val4, Val5, Val6, Val7,
        Val8, Val9

        Spin velocity

        Method to use for defining the spin axis:

        Define the spin axis using two points:

        Val4, Val5, Val6 -- Coordinates of the first point

        Val7, Val8, Val9 -- Coordinates of the second point

        This definition method is currently the only option.

        This command defines a steady state spinning motion of 120 rad/s around
        the spin axis:

        In this case, two points with coordinates (0,0,0) and (0,1,0) define
        the spin axis in the global Y direction.

        Define the rigid body motion (velocity):

        SSTATE, DEFINE, CM_Name, TRANSLATE, Val2, Val3, Val4

        SSTATE, LIST, CM_Name

        Lists all steady-state analysis data defined on the specified element
        component. All data is listed if no component (CM_Name) is specified.

        SSTATE, DELETE, CM_Name

        Deletes all steady-state analysis data defined on the specified element
        component. All data is deleted if no component (CM_Name) is specified.
        """
        command = f"SSTATE,{action},{cm_name},{val1},{val2},{val3},{val4},{val5},{val6},{val7},{val8},{val9}"
        return self.run(command, **kwargs)

    def xfdata(self, enrichmentid="", elemnum="", nodenum="", phi="", **kwargs):
        """Defines a crack in the model by specifying nodal level set values

        APDL Command: XFDATA

        Parameters
        ----------
        enrichmentid
            Name of the enrichment specified via the associated XFENRICH
            command.

        lsm (or blank)
            Specify LSM to indicate that level set values (PHI and optional
            PSI) are specified.

        elemnum
            Element number.

        nodenum
            Node number associated with the specified element ELNUM.

        phi
            Signed normal distance of the node from the crack.

        Notes
        -----
        Issue the XFDATA command multiple times as needed to specify nodal
        level set values for all nodes of an element.

        This command is valid in PREP7 (/PREP7) only.
        """
        command = f"XFDATA,{enrichmentid},{elemnum},{nodenum},{phi}"
        return self.run(command, **kwargs)

    def xfenrich(self, enrichmentid="", compname="", matid="", **kwargs):
        """Defines parameters associated with crack propagation using XFEM

        APDL Command: XFENRICH

        Parameters
        ----------
        enrichmentid
            An alphanumeric name assigned to identify the enrichment. The name
            can contain up to 32 characters and must begin with an alphabetic
            character. Alphabetic characters, numbers, and underscores are
            valid.

        compname
            Name of the element set component for which initial cracks are
            defined and possibly propagated.

        matid
            Material ID number referring to cohesive zone material behavior on
            the initial crack. If 0 or not specified, the initial crack is
            assumed to be free of cohesive zone behavior.

        Notes
        -----
        If MatID is specified, the cohesive zone behavior is described by the
        bilinear cohesive law.

        This command is valid in PREP7 (/PREP7) only.
        """
        command = f"XFENRICH,{enrichmentid},{compname},{matid}"
        return self.run(command, **kwargs)

    def xflist(self, enrichmentid="", **kwargs):
        """Lists enrichment details and associated crack information

        APDL Command: XFLIST

        Parameters
        ----------
        enrichmentid or (blank)
            Name of the enrichment specified via the associated XFENRICH
            command. Specifying EnrichmentID is optional.

        Notes
        -----
        This command is valid in PREP7 (/PREP7) and SOLUTION (/SOLU).
        """
        command = f"XFLIST,{enrichmentid}"
        return self.run(command, **kwargs)
