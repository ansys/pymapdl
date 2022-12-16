class Special:
    def bfint(
        self,
        fname1="",
        ext1="",
        fname2="",
        ext2="",
        kpos="",
        clab="",
        kshs="",
        tolout="",
        tolhgt="",
        **kwargs,
    ):
        """Activates the body force interpolation operation.

        APDL Command: BFINT

        Parameters
        ----------
        fname1
            File name and directory path (248 characters maximum,
            including directory) from which to read data for
            interpolation. If you do not specify a directory path, it
            will default to your working directory and you can use all
            248 characters for the file name.

        ext1
            Filename extension (eight-character maximum).

        fname2
            File name and directory path (248 characters maximum,
            including directory) to which BF commands are written. If
            you do not specify a directory path, it will default to
            your working directory and you can use all 248 characters
            for the file name.

        ext2
            Filename extension (eight-character maximum).

        kpos
            Position on Fname2 to write block of BF commands:

            0 - Beginning of file (overwrite existing file).

            1 - End of file (append to existing file).

        clab
            Label (8 characters maximum, including the colon) for this
            block of BF commands in Fname2.  This label is appended to
            the colon (:).  Defaults to BFn, where n is the cumulative
            iteration number for the data set currently in the
            database.

        kshs
            Shell-to-solid submodeling key:

            0 - Solid-to-solid or shell-to-shell submodel.

            1 - Shell-to-solid submodel.

        tolout
            Extrapolation tolerance about elements, based on a
            fraction of the element dimension. Submodel nodes outside
            the element by more than TOLOUT are not accepted as
            candidates for DOF extrapolation.  Defaults to 0.5 (50%).

        tolhgt
            Height tolerance above or below shell elements, in units
            of length.  Used only for shell-to-shell submodeling (KSHS
            = 0). Submodel nodes off the element surface by more than
            TOLHGT are not accepted as candidates for DOF
            interpolation or extrapolation. Defaults to 0.0001 times
            the maximum element dimension.

        Notes
        -----
        File Fname1 should contain a node list for which body forces are to be
        interpolated [NWRITE].  File Fname2 is created, and contains
        interpolated body forces written as a block of nodal BF commands.

        Body forces are interpolated from elements having TEMP as a valid body
        force or degree of freedom, and only the label TEMP is written on the
        nodal BF commands.  Interpolation is performed for all nodes on file
        Fname1 using the results data currently in the database. For layered
        elements, use the LAYER command to select the locations of the
        temperatures to be used for interpolation. Default locations are the
        bottom of the bottom layer and the top of the top layer.

        The block of BF commands begins with an identifying colon label command
        and ends with a /EOF command.  The colon label command is of the form
        :Clab, where Clab is described above.  Interpolation from multiple
        results sets can be performed by looping through the results file in a
        user-defined macro.  Additional blocks can be appended to Fname2 by
        using KPOS and unique colon labels.  A /INPUT command, with the
        appropriate colon label, may be used to read the block of commands.

        If the model has coincident (or very close) nodes, BFINT must be
        applied to each part of the model separately to ensure that the mapping
        of the nodes is correct.  For example, if nodes belonging to two
        adjacent parts linked by springs are coincident, the operation should
        be performed on each part of the model separately.
        """
        command = f"BFINT,{fname1},{ext1},,{fname2},{ext2},,{kpos},{clab},{kshs},{tolout},{tolhgt}"
        return self.run(command, **kwargs)

    def cbdof(
        self,
        fname1="",
        ext1="",
        fname2="",
        ext2="",
        kpos="",
        clab="",
        kshs="",
        tolout="",
        tolhgt="",
        tolthk="",
        **kwargs,
    ):
        """Activates cut-boundary interpolation (for submodeling).

        APDL Command: CBDOF

        Parameters
        ----------
        fname1
            File name and directory path (248 characters maximum,
            including directory) from which to read boundary node
            data. If no specified directory path exists, the path
            defaults to your working directory and you can use all 248
            characters for the file name.

        ext1
            Filename extension (eight-character maximum).

        fname2
            File name and directory path (248 characters maximum,
            including directory) to which cut-boundary D commands are
            written. If no specified directory path exists, the path
            defaults to your working directory and you can use all 248
            characters for the file name.

        ext2
            Filename extension (eight-character maximum).

        kpos
            Position on Fname2 to write block of D commands:

            0 - Beginning of file (overwrite existing file).

            1 - End of file (append to existing file).

        clab
            Label (eight characters maximum, including the colon) for
            this block of D commands on Fname2.  his label is appended
            to the colon (:).  Defaults to CBn, where n is the
            cumulative iteration number for the data set currently in
            the database.  For imaginary data (see KIMG on the ``*SET``
            command), Clab defaults to CIn.

        kshs
            Shell-to-solid submodeling key:

            0 - Solid-to-solid or shell-to-shell submodel.

            1 - Shell-to-solid submodel.

        tolout
            Extrapolation tolerance about elements, based on a
            fraction of the element dimension. Submodel nodes outside
            the element by more than TOLOUT are not accepted as
            candidates for DOF extrapolation.  Defaults to 0.5 (50
            percent).

        tolhgt
            Height tolerance above or below shell elements, in units
            of length.  Used only for shell-to-shell submodeling (KSHS
            = 0). Submodel nodes off the element surface by more than
            TOLHGT are not accepted as candidates for
            degree-of-freedom interpolation or extrapolation.
            Defaults to 0.0001 times the maximum element dimension.

        tolthk
            Height tolerance above or below shell elements, based on a
            fraction of the shell element thickness. Used only for
            shell-to-solid submodeling (KSHS = 1). Submodel nodes off
            the element surface by more than TOLTHK are not accepted
            as candidates for DOF interpolation or
            extrapolation. Defaults to 0.1 times the average shell
            thickness.

        Notes
        -----
        File Fname1 should contain a node list for which boundary
        conditions are to be interpolated (NWRITE).  File Fname2 is
        created to contain interpolated boundary conditions written as
        a block of D commands.

        Boundary conditions are written for the active
        degree-of-freedom set for the element from which interpolation
        is performed. Interpolation occurs on the selected set of
        elements.  The block of D commands begins with an identifying
        colon label and ends with a /EOF command.  The colon label is
        of the form :Clab (described above).

        Interpolation from multiple results sets can be performed by
        looping through the results file in a user-defined macro.
        Additional blocks can be appended to Fname2 by using KPOS and
        unique colon labels.  To read the block of commands, issue the
        /INPUT command with the appropriate colon label.

        If the model has coincident (or very close) nodes, the CBDOF
        must be applied to each part of the model separately to ensure
        that the mapping of the nodes is correct.  For example, if
        nodes belonging to two adjacent parts linked by springs are
        coincident, the operation should be performed on each part of
        the model separately.

        Resume the coarse model database at the beginning of the
        cut-boundary procedure. The database should have been saved
        after the first coarse model solution, as the number of nodes
        in the database and the results file must match, and internal
        nodes are sometimes created during the solution.

        Caution: Relaxing the TOLHGT or TOLTHK tolerances to allow
        submodel nodes to be "found" can produce poor submodel
        results.
        """
        command = f"CBDOF,{fname1},{ext1},,{fname2},{ext2},,{kpos},{clab},{kshs},{tolout},{tolhgt},{tolthk}"
        return self.run(command, **kwargs)

    def cmsfile(self, option="", fname="", ext="", cmskey="", **kwargs):
        """Specifies a list of component mode synthesis (CMS) results files for

        APDL Command: CMSFILE
        plotting results on the assembly.

        Parameters
        ----------
        option
            Specifies the command operation:

            ADD - Add the specified component results file (Fname) to the list of files to plot.
                  This option is the default.

            DELETE - Remove the specified component results file (Fname) from the list of files to
                     plot.

            LIST - List all specified component results files.

            CLEAR - Clear all previous files added.

            ALL - Add all component results (.rst) files from the working directory to the list
                  of files to plot.

        fname
            The file name (with full directory path) of the component results
            file. The default file name is the Jobname (specified via the
            /FILNAME command).

        ext
            The file name (Fname) extension. The default extension is .rst.

        cmskey
            Valid only when adding a results file (Option = ADD or ALL), this
            key specifies whether or not to check the specified .rst file to
            determine if it was created via a CMS expansion pass:

            ON - Check (default).

            OFF - Do not check.

        Notes
        -----
        The CMSFILE command specifies the list of component mode synthesis
        (CMS) results files to include when plotting the mode shape of an
        assembly.

        During postprocessing (/POST1) of a CMS analysis, issue the CMSFILE
        command to point to component results files of interest. (You can issue
        the command as often as needed to include all or some of the component
        results files.) Issue the SET command to acquire the frequencies and
        mode shapes from substeps for all specified results files. Execute a
        plot (PLNSOL) or print (PRNSOL) operation to display the mode shape of
        the entire assembly.

        When you specify a results file to add to the plot list, the default
        behavior of the command (CmsKey = ON) is to first verify that the file
        is from a CMS analysis and that the frequencies of the result sets on
        the file match the frequencies on the first file in the list. If CmsKey
        = OFF, you can add any .rst file to the list of files to plot, even if
        the file was not expanded via a CMS expansion pass.

        If CmsKey = ON (default), output from the command appears as: ADD CMS
        FILE = filename.rst. : If CmsKey = OFF, output from the command appears
        as: ADD FILE = filename.rst.

        If Option = DELETE or CLEAR, you must clear the database (/CLEAR), then
        re-enter the postprocessor (/POST1) and issue a SET command for the
        change to take effect on subsequent plots.

        Clearing the database does not clear the list of files specified via
        the CMSFILE command. Specify Option = CLEAR to clear the list of files.
        """
        command = f"CMSFILE,{option},{fname},{ext},{cmskey}"
        return self.run(command, **kwargs)

    def cyccalc(self, fileprefix="", fileformat="", **kwargs):
        """Calculates results from a cyclic harmonic mode-superposition analysis

        APDL Command: CYCCALC
        using the specifications defined by CYCSPEC.

        Parameters
        ----------
        fileprefix
            Each result table (corresponding to each CYCSPEC specification) is
            written to a file beginning with FilePrefix. If blank (default),
            the result tables are written to the output file.

        fileformat
            If FilePrefix is specified, then use FileFormat to specify the
            format of the file to be written:

            FORM - Formatted file (default)

            CSV - Comma-separated value file

        Notes
        -----
        CYCCALC loops through the specification given by CYCSPEC and computes
        the requested outputs. The outputs are given in a table format, with
        the rows corresponding to each frequency solution from the harmonic
        analysis, and the columns corresponding to each sector. The table
        entries are the maximum value of the specified quantity at the
        specified location in the sector. In addition, columns containing the
        maximum value at the frequency, the sector in which it occurs, and the
        node in the sector at which it occurs are output.

        If FilePrefix is specified, a file is created for each output table
        with the name FilePrefix_node_type.ext, where node is the node number
        or component name, type is the item/component requested, and the file
        extension .ext is either .txt or .csv, depending on FileFormat.

        A SET command must precede the CYCCALC command.

        The CYCCALC results are based on the currently active RSYS, SHELL,
        LAYER, and AVPRIN settings.
        """
        command = f"CYCCALC,{fileprefix},{fileformat}"
        return self.run(command, **kwargs)

    def cycfiles(self, fnamerst="", extrst="", fnamerfrq="", extrfrq="", **kwargs):
        """Specifies the data files where results are to be found for a cyclic

        APDL Command: CYCFILES
        symmetry mode-superposition harmonic analysis.

        Parameters
        ----------
        fnamerst
            The file name and directory path of the results file from the
            cyclic modal solution. Defaults to Jobname.

        extrst
            File name extension for FnameRst. Defaults to rst.

        fnamerfrq
            The file name and directory path of the results file from the
            cyclic mode-superposition harmonic solution. Defaults to the value
            of the FnameRst argument.

        extrfrq
            File name extension for FnameRfrq. Defaults to rfrq.
        """
        command = f"CYCFILES,{fnamerst},{extrst},{fnamerfrq},{extrfrq}"
        return self.run(command, **kwargs)

    def cycphase(self, type_="", option="", **kwargs):
        """Provides tools for determining minimum and maximum possible result

        APDL Command: CYCPHASE
        values from frequency couplets produced in a modal cyclic symmetry
        analysis.

        Parameters
        ----------
        type\_
            The type of operation requested:

            DISP - Calculate the maximum and minimum possible displacement at each node in the
                   original sector model.  Store the values and the phase angle
                   at which they occurred.

            STRESS - Calculate the maximum and minimum possible stresses at each node in the
                     original sector model.  Store the values and the phase
                     angle at which they occurred.

            STRAIN - Calculate the maximum and minimum possible strains at each node in the original
                     sector model.  Store the values and the phase angle at
                     which they occurred.

            ALL - Calculate the maximum and minimum possible displacement, stress and strain at
                  each node in the original sector model.  Store the values and
                  the phase angle at which they occurred.

            GET - Places the value of a MAX or MIN item into the _CYCVALUE parameter, the node
                  for that value in the _CYCNODE parameter, and the phase angle
                  for the value in the _CYCPHASE parameter.

            PUT - Put resulting sweep values for printing (via the PRNSOL command ) or plotting
                  (via the PLNSOL command).

            LIST - List the current minimum/maximum displacement, stress and strain nodal values.

            STAT - Summarize the results of the last phase sweep.

            CLEAR - Clear phase-sweep information from the database.

        option
            If TYPE = DISP, STRAIN, STRESS or ALL, controls the sweep angle
            increment to use in the search:

            Angle - The sweep angle increment in degrees, greater than 0.1 and less than 10. The
                    default is 1.

        Notes
        -----
        When you expand the results of a modal cyclic symmetry analysis (via
        the /CYCEXPAND or EXPAND command), ANSYS combines the real and
        imaginary results for a given nodal diameter, assuming no phase shift
        between them; however, the modal response can occur at any phase shift.

        CYCPHASE response results are valid only for the first cyclic sector.
        To obtain the response at any part of the expanded model, ANSYS, Inc.
        recommends using cyclic symmetry results expansion at the phase angle
        obtained via CYCPHASE.

        The phase angles returned by CYCPHASE contain the minimum and maximum
        values for USUM, SEQV and other scalar principal stress and strain
        quantities; however, they do not always return the true minimum and
        maximum values for directional quantities like UX or SX unless the
        values fall in the first sector.

        CYCPHASE does not consider midside node values when evaluating maximum
        and minimum values, which may affect DISPLAY quantities but no others.
        (Typically, ANSYS ignores midside node stresses and strains during
        postprocessing.)

        Issuing CYCPHASE,PUT clears the result values for midside nodes on high
        order elements; therefore, this option sets element faceting (/EFACET)
        to 1. The command reports that midside nodal values are set to zero and
        indicates that element faceting is set to 1.

        If the sweep values are available after issuing a CYCPHASE,PUT command,
        the PRNSOL or PLNSOL command will print or plot (respectively) the
        sweep values of structure displacement Ux, Uy, Uz, component
        stress/strain X, Y, Z, XY, YZ, ZX, principal stress/strain 1, 2, 3 and
        equivalent stress/strain EQV.  The vector sum of displacement (USUM)
        and stress/strain intensity (SINT) are not valid phase-sweep results.

        You can specify any coordinate system via the RSYS command for
        displaying or printing CYCPHASE results. However, after CYCPHASE
        results have been extracted, you cannot then transform them via the
        RSYS command. If you try to do so, ANSYS issues a warning message.

        The CYCPHASE command is valid in /POST1 and for cyclically symmetric
        models only.

        To learn more about analyzing a cyclically symmetric structure, see the
        Cyclic Symmetry Analysis Guide.
        """
        command = f"CYCPHASE,{type_},{option}"
        return self.run(command, **kwargs)

    def cycspec(self, label="", node="", item="", comp="", **kwargs):
        """Defines the set of result items for a subsequent CYCCALC command in

        APDL Command: CYCSPEC
        postprocessing a cyclic harmonic mode-superposition analysis.

        Parameters
        ----------
        label
            One of the following labels:

            ADD - Adds a new specification to the set (default). The maximum number of
                  specifications that can be defined is 50.

            LIST - Lists the current set of specifications. Node, Item, Comp are ignored.

            ERASE - Erases the current set of specifications. Node, Item, Comp are ignored.

            DELETE - Deletes an existing specification. Item, Comp are ignored.

        node
            The node at which to evaluate the results. If Node is a nodal
            component, then all nodes in the component are included. All
            sectors containing this node (or set of nodes) are evaluated.

        item
            Specifies the type of values to evaluate:

            U - Displacement

            S - Stress

            EPEL - Elastic strain

        comp
            Specifies the specific component of displacement, stress, or strain
            to evaluate:

            X,Y,Z - Direct components

            XY,YZ,XZ - Shear components (stress and strain only)

            1,2,3 - Principal values (stress and strain only)

            EQV - Equivalent value (stress and strain only)

            SUM - Vector sum (displacement only)

            NORM - L2 norm for the set of nodes (displacement only)

        Notes
        -----
        Up to 50 specifications can be defined for use in a subsequent CYCCALC
        command. If more than 50 specifications are desired, erase the table
        after the CYCCALC operation and add new specifications and repeat the
        CYCCALC command. All the specified nodes, items, and components are
        evaluated for all sectors and the maximum amplitude value output. For
        combined stresses and strains (Comp = 1,2,3 or EQV) or displacement
        vector sum (Comp = SUM), a 360 degree phase sweep is performed at each
        location to determine the maximum.

        Additional POST1 controls are used to refine the specification. For
        component values, components are in the RSYS direction. For shell
        elements, the results are at the SHELL location. For EPEL,EQV, the
        results are based on the EFFNU value on the AVPRIN command. The
        controls active when the CYCCALC command is issued determine the result
        values. If results at another SHELL location are desired, issue the new
        SHELL command and then re-issue the CYCCALC command.

        If a single node is input, the Item/Comp value at that location in each
        sector is output. If a node component is given, then the maximum
        Item/Comp value within the set of nodes of each sector is output, one
        value for each sector (the node of the maximum may vary from sector to
        sector). For stress and strain items, only corner nodes are valid.

        For the displacement norm option (Item = U, Comp = NORM), the L2 norm
        computed from all the nodes in the component is output, one per sector.
        """
        command = f"CYCSPEC,{label},{node},{item},{comp}"
        return self.run(command, **kwargs)

    def exoption(self, ldtype="", option="", value="", **kwargs):
        """Specifies the EXPROFILE options for the Mechanical APDL to ANSYS CFX profile file transfer.

        APDL Command: EXOPTION

        Parameters
        ----------
        ldtype
            Load type:

            * ``"SURF"`` : Surface load

            * ``"VOLU"`` : Volume load

        option
            Surface options:

            * ``"Precision"`` : Number of significant digits for the
              fractional part of real data

            * ``"Connectivity"`` : Key to include face connectivity in the
              exported profile file

            * ``"Precision"`` : Number of significant digits after the
              decimal for real data

        value
            Specify the value for either Precision or Connectivity.

            For Precision, specify the number of significant digits. Can
            be any value between 1 to 20, default 8. When 0 or an invalid
            value is specified, the program will use the default value of
            8 and issue a warning message.

            For Connectivity, specify the key to include the element face
            connectivity data for surface loads (does not support volume
            loads):

            * ``"OFF"`` : Do not include the connectivity data in the exported file (default)

            * ``"ON"`` : Include the connectivity data in the exported file

        Notes
        -----
        This command is not supported in Distributed ANSYS.
        """
        return self.run(f"EXOPTION,{ldtype},{option},{value}", **kwargs)

    def expand(self, nrepeat="", hindex="", icsys="", sctang="", phase="", **kwargs):
        """Displays the results of a modal cyclic symmetry analysis.

        APDL Command: EXPAND

        Parameters
        ----------
        nrepeat
            Number of sector repetitions for expansion. The default is 0 (no
            expansion).

        modal
            Specifies that the expansion is for a modal cyclic symmetry
            analysis.

        hindex
            The harmonic index ID for the results to expand.

        icsys
            The coordinate system number used in the modal cyclic symmetry
            solution. The default is the global cylindrical coordinate system
            (specified via the CSYS command where KCN = 1).

        sctang
            The sector angle in degrees, equal to 360 divided by the number of
            cyclic sectors.

        --
            This field is reserved for future use.

        phase
            The phase angle in degrees to use for the expansion. The default is
            0. Typically, the value is the peak displacement (or stress/strain)
            phase angle obtained via the CYCPHASE command.

        Notes
        -----
        Issue this command to display the results of a modal cyclic symmetry
        analysis.

        When you issue the EXPAND,Nrepeat command, subsequent SET commands read
        data from the results file and expand them to Nrepeat sectors. As long
        as no entities have been modified, this expansion can be negated (that
        is, reverted to single sector) by issuing EXPAND with no arguments. If
        you modify entities and wish to return to the partial model, use the
        Session Editor (see Restoring Database Contents in the Operations
        Guide).

        EXPAND displays the results and allows you to print them, as if for a
        full model. The harmonic index (automatically retrieved from the
        results file) appears in the legend column.

        When plotting or printing element strain energy (SENE), the EXPAND
        command works with brick or tet models only. Element kinetic energy
        (KENE) plotting or printing is not supported.

        EXPAND is a specification command valid only in POST1.  It is
        significantly different from the /CYCEXPAND command in several
        respects, (although you can use either command to display the results
        of a modal cyclic symmetry analysis):

        EXPAND has none of the limitations of the /CYCEXPAND command.

        EXPAND changes the database by modifying the geometry, the nodal
        displacements, and element stresses as they are read from the results
        file, whereas the /CYCEXPAND command does not change the database.

        Caution:: : The EXPAND command creates new nodes and elements;
        therefore, saving (or issuing the /EXIT, ALL command) after issuing the
        EXPAND command can result in large databases.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"EXPAND,{nrepeat},{hindex},{icsys},{sctang},{phase}"
        return self.run(command, **kwargs)

    def exprofile(
        self,
        ldtype="",
        load="",
        value="",
        pname="",
        fname="",
        fext="",
        fdir="",
        **kwargs,
    ):
        """Exports interface loads or loads on selected nodes to an ANSYS CFX

        APDL Command: EXPROFILE
        Profile file.

        Parameters
        ----------
        ldtype
            Load type:

            SURF  - Surface load.

            VOLU  - Volumetric load.

        load
            Surface loads:

            DISP  - Displacement (in a static analysis) or mode shape and global parameters (in a
                    modal analysis).

            MODE  - Normalized mode shape and global parameters (in a modal analysis only).

            TEMP  - Temperature.

            HFLU  - Heat flux.

        value
            If a positive integer, specifies the number of the surface or
            volume interface. If 0 (zero), the selected nodes or Named
            Selection are used.

        pname
            Field name in CFX Profile file (32-character maximum). Defaults to
            jobname_bcploadnumber for a surface load and jobname_subdloadnumber
            for volumetric load.

        fname
            The CFX Profile filename (248-character maximum). Defaults to
            jobname_bcploadnumber for a surface load and jobname_subdloadnumber
            for a volumetric load.

        fext
            The Profile file extension (8-character maximum). Defaults to.csv.

        fdir
            The Profile file directory (8-character maximum). Defaults to
            current directory.

        Notes
        -----
        By default, the EXPROFILE command assumes the data it writes to the
        Profile file are in SI units. For models not described in SI units,
        issue the EXUNIT command as needed to write the correct unit labels on
        the Profile file.

        For a modal analysis, if Load = DISP or MODE, global parameters
        including mass, frequency, and maximum displacement are also written to
        the ANSYS CFX Profile file. You should therefore issue the EXUNIT
        command for DISP, TIME, and MASS.

        Verify that the coordinate system is set to the global Cartesian
        (RSYS,0) before using this command.

        To transfer multiple loads across an interface, specify a unique file
        name and extension for each load.

        Force (FORC) and heat generation (HGEN) are per-unit volume.

        For modal analysis, this command does not support the following mode-
        extraction methods (MODOPT): unsymmetric matrix (UNSYM), the damped
        system (DAMP), or the QR-damped system (QRDAMP).

        To write the normalized (instead of non-normalized) mode shapes from a
        modal analysis to the file:

        Use Load = MODE.

        Verify that the mode shapes are normalized to the mass matrix
        (MODOPT,,,,,,OFF), the default behavior.

        Verify that the scale factor is set to 1.0 (SET,,,1.0), the default
        value.

        For loads not specified directly via commands (such as SF and BF),
        loads must first be read into the database (SET or LCASE).

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"EXPROFILE,{ldtype},{load},{value},{pname},{fname},{fext},{fdir}"
        return self.run(command, **kwargs)

    def exunit(self, ldtype="", load="", untype="", name="", **kwargs):
        """Specifies the interface load unit labels to be written to the export

        APDL Command: EXUNIT
        file for ANSYS to CFX transfer.

        Parameters
        ----------
        ldtype
            Load type:

            SURF  - Surface load.

            VOLU  - Volumetric load.

        load
            Surface loads:

            DISP  -  Displacement in a static analysis. Mode shape in a modal analysis.

            TIME  - Time. The unit for frequency is the inverse of the unit for time.

            MASS  -  Mass.

            TEMP  - Temperature.

            HFLU  - Heat flux.

        untype
            Unit type:

            COMM  - Predefined unit

            USER  - User-specified unit

        name
            Commonly used predefined unit name or user-specified unit name.

            SI - International System of units (meter-kilogram-second) (default)

            FT -  English System of units (feet-pound-second)

        Notes
        -----
        This command only specifies which unit labels are to be written to the
        file when the EXPROFILE is issued. It does not perform unit
        conversions.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"EXUNIT,{ldtype},{load},{untype},{name}"
        return self.run(command, **kwargs)

    def fssparm(self, port1="", port2="", **kwargs):
        """Calculates reflection and transmission properties of a frequency

        APDL Command: FSSPARM
        selective surface.

        Parameters
        ----------
        port1
            Port number of input port. Defaults to 1.

        port2
            Port number of output port. Defaults to 1.

        Notes
        -----
        FSSPARM calculates reflection and transmission coefficients, power
        reflection and transmission coefficients, and return and insertion
        losses of a frequency selective surface.
        """
        command = f"FSSPARM,{port1},{port2}"
        return self.run(command, **kwargs)

    def fsum(self, lab="", item="", **kwargs):
        """Sums the nodal force and moment contributions of elements.

        APDL Command: FSUM

        Parameters
        ----------
        lab
            Coordinate system in which to perform summation.

            (blank) - Sum all nodal forces in global Cartesian coordinate system (default).

            RSYS - Sum all nodal forces in the currently active RSYS coordinate system.

        item
            Selected set of nodes.

            (blank) - Sum all nodal forces for all selected nodes (default), excluding contact
                      elements.

            CONT - Sum all nodal forces for contact nodes only.

            BOTH - Sum all nodal forces for all selected nodes, including contact elements.

        Notes
        -----
        Sums and prints, in each component direction for the total selected
        node set, the nodal force and moment contributions of the selected
        elements attached to the node set. Selecting a subset of nodes [NSEL]
        and then issuing this command will give the total force acting on that
        set of nodes (default), excluding surface-to-surface, node-to-surface,
        line-to-line, and line-to-surface contact elements (TARGE169, TARGE170,
        CONTA171, CONTA172, CONTA173, CONTA174, CONTA175, CONTA176, and
        CONTA177).

        Setting ITEM = CONT sums the nodal forces and moment contributions of
        the selected contact elements (CONTA171, CONTA172, CONTA173, CONTA174,
        CONTA175, CONTA176, and CONTA177). Setting ITEM = BOTH sums the nodal
        forces for all selected nodes, including contact elements.

        Nodal forces associated with surface loads are not included. The
        effects of nodal coupling and constraint equations are ignored. Moment
        summations are about the global origin unless another point is
        specified with the SPOINT command. This vector sum is printed in the
        global Cartesian system unless it is transformed [RSYS] and a point is
        specified with the SPOINT command. By default, the sum is done in
        global Cartesian, and the resulting vector is transformed to the
        requested system.

        The LAB = RSYS option transforms each of the nodal forces into the
        active coordinate system before summing and printing. The FORCE command
        can be used to specify which component (static, damping, inertia, or
        total) of the nodal load is to be used. This command output is included
        in the NFORCE command.

        The command should not be used with axisymmetric elements because it
        might calculate a moment where none exists. Consider, for example, the
        axial load on a pipe modeled with an axisymmetric shell element.  The
        reaction force on the end of the pipe is the total force (for the full
        360 degrees) at that location. The net moment about the centerline of
        the pipe would be zero, but the program would incorrectly calculate a
        moment at the end of the element as the force multiplied by the radius.

        The command is not valid for elements that operate solely within the
        nodal coordinate system with 1-D option activated and rotated nodes
        (NROTAT).
        """
        command = f"FSUM,{lab},{item}"
        return self.run(command, **kwargs)

    def hfang(self, lab="", phi1="", phi2="", theta1="", theta2="", **kwargs):
        """Defines or displays spatial angles of a spherical radiation surface for

        APDL Command: HFANG
        sound radiation parameter calculations.

        Parameters
        ----------
        lab
            Spatial angle label.

            ANGLE - Define spatial angles (default).

            STATE - Display spatial angles. PHI1, PHI2, THETA1, and THETA2 are ignored.

        phi1, phi2
            Starting and ending ϕ angles (degrees) in the spherical coordinate
            system. Defaults to 0.

        theta1, theta2
            Starting and ending θ angles (degrees) in the spherical coordinate
            system. Defaults to 0.

        Notes
        -----
        Defines or displays spatial angles of a spherical radiation surface.

        Use this command only with PLFAR,Lab = PRES, or PRFAR,Lab = PRES.
        """
        command = f"HFANG,{lab},{phi1},{phi2},{theta1},{theta2}"
        return self.run(command, **kwargs)

    def hfsym(self, kcn="", xkey="", ykey="", zkey="", **kwargs):
        """Indicates the presence of symmetry planes for the computation of

        APDL Command: HFSYM
        acoustic fields in the near and far field domains (beyond the finite
        element region).

        Parameters
        ----------
        kcn
            Coordinate system reference number. KCN may be 0 (Cartesian), or
            any previously defined local Cartesian coordinate system number
            (>10). Defaults to 0.

        xkey
            Key for acoustic field boundary condition, as prescribed for the
            solution, corresponding to the x = constant plane:

            None - No sound soft or sound hard boundary conditions (default).

            SSB - Sound soft boundary (pressure = 0).

            SHB - Sound hard boundary (normal velocity = 0).

        ykey
            Key for acoustic field boundary condition, as prescribed for the
            solution, corresponding to the y = constant plane:

            None - No sound soft or sound hard boundary conditions (default).

            SSB - Sound soft boundary (pressure = 0).

            SHB - Sound hard boundary (normal velocity = 0).

        zkey
            Key for acoustic field boundary condition, as prescribed for the
            solution, corresponding to the z = constant plane:

            None - No sound soft or sound hard boundary conditions (default).

            SSB - Sound soft boundary (pressure = 0).

            SHB - Sound hard boundary (normal velocity = 0).

        Notes
        -----
        HFSYM uses the image principle to indicate symmetry planes (x, y, or z
        = constant plane) for acoustic field computations outside the modeled
        domain. A sound hard boundary condition must be indicated even though
        it occurs as a natural boundary condition.

        No menu paths are available for acoustic applications.
        """
        command = f"HFSYM,{kcn},{xkey},{ykey},{zkey}"
        return self.run(command, **kwargs)

    def intsrf(self, lab="", **kwargs):
        """Integrates nodal results on an exterior surface.

        APDL Command: INTSRF

        Parameters
        ----------
        lab
            Label indicating degree of freedom to be integrated:

            PRES - Pressure.

            TAUW - Wall shear stress.

            FLOW - Both pressure and wall shear stress.

        Notes
        -----
        Integrates nodal results on a surface.  Use node selection (such as the
        EXT option of the NSEL command) to indicate the surface(s) of element
        faces to be used in the integration.  A surface can be "created" by
        unselecting elements (such as unselecting non-fluid elements that are
        adjacent to fluid elements for the postprocessing of fluid flow
        result).  Element faces attached to the selected nodes will be
        automatically determined.  All nodes on a face must be selected for the
        face to be used.  The integration results will cancel for nodes on
        common faces of adjacent selected elements.

        Integration results are in the active coordinate system (see the RSYS
        command). The type of results coordinate system must match the type
        used in the analysis. However, you may translate and rotate forces and
        moments as needed. Use the ``*GET`` command (Utility Menu> Parameters> Get
        Scalar Data) to retrieve the results.
        """
        command = f"INTSRF,{lab}"
        return self.run(command, **kwargs)

    def kcalc(self, kplan="", mat="", kcsym="", klocpr="", **kwargs):
        """Calculates stress intensity factors in fracture mechanics analyses.

        APDL Command: KCALC

        Parameters
        ----------
        kplan
            Key to indicate stress state for calculation of stress intensity
            factors:

            0 - Plane strain and axisymmetric condition (default).

            1 - Plane stress condition.

        mat
            Material number used in the extrapolation (defaults to 1).

        kcsym
            Symmetry key:

            0 or 1  - Half-crack model with symmetry boundary conditions [DSYM] in the crack-tip
                      coordinate system.  KII = KIII = 0.  Three nodes are
                      required on the path.

            2 - Like 1 except with antisymmetric boundary conditions (KI = 0).

            3 - Full-crack model (both faces).  Five nodes are required on the path (one at the
                tip and two on each face).

        klocpr
            Local displacements print key:

            0 - Do not print local crack-tip displacements.

            1 - Print local displacements used in the extrapolation technique.

        Notes
        -----
        Calculates the stress intensity factors (KI, KII, and KIII) associated
        with homogeneous isotropic linear elastic fracture mechanics.  A
        displacement extrapolation method is used in the calculation (see POST1
        -  Crack Analysis in the Mechanical APDL Theory Reference). This method
        assumes that the displacement calculations are for the plane strain
        state. If the displacement calculations are performed using a plane
        stress formulation, the calculation of the stress intensity factors can
        be converted to the plane strain state by using KPLAN = 1. ANSYS Uses
        minor Poisson's ratio (MP,NUXY) for the stress intensity factor
        calculation, therefore the material's Poisson's ratio must be defined
        using MP,NUXY command. The PATH and PPATH commands must be used to
        define a path with the crack face nodes (NODE1 at the crack tip, NODE2
        and NODE3 on one face, NODE4 and NODE5 on the other (optional) face).
        A crack-tip coordinate system, having x parallel to the crack face (and
        perpendicular to the crack front) and y perpendicular to the crack
        face, must be the active RSYS and CSYS before KCALC is issued.
        """
        command = f"KCALC,{kplan},{mat},{kcsym},{klocpr}"
        return self.run(command, **kwargs)

    def nforce(self, item="", **kwargs):
        """Sums the nodal forces and moments of elements attached to nodes.

        APDL Command: NFORCE

        Parameters
        ----------
        item
            Specifies the selected set of nodes for summing forces and moments
            for contact elements.

            (blank) - Sums the nodal forces of elements for all selected nodes and excludes contact
                      elements (elements 169-177).

            CONT - Sums the nodal forces of elements for contact nodes only.

            BOTH - Sums the nodal forces of elements for all selected nodes, including contact
                   elements.

        Notes
        -----
        Sums and prints, in each component direction for each selected node,
        the nodal force and moment contributions of the selected elements
        attached to the node.  If all elements are selected, the sums are
        usually zero except where constraints or loads are applied.  The nodal
        forces and moments may be displayed [/PBC,FORC and /PBC,MOME].  Use
        PRESOL to print nodal forces and moments on an element-by-element
        basis.  You can use the FORCE command to specify which component
        (static, damping, inertia, or total) of the nodal load is to be used.
        Nodal forces associated with surface loads are not included.

        This vector sum is printed in the global Cartesian system. Moment
        summations are about the global origin unless another point is
        specified with the SPOINT command.  The summations for each node are
        printed in the global Cartesian system unless transformed [RSYS].  This
        command is generally not applicable to axisymmetric models because
        moment information from the NFORCE command is not correct for
        axisymmetric elements.

        Selecting a subset of elements [ESEL] and then issuing this command
        will give the forces and moments required to maintain equilibrium of
        that set of elements.  The effects of nodal coupling and constraint
        equations are ignored. The option ITEM = CONT provides the forces and
        moments for the contact elements (CONTA171, CONTA172, CONTA173,
        CONTA174, CONTA175, CONTA176, and CONTA177). Setting ITEM = BOTH
        provides the forces and moments for all selected nodes, including
        contact elements.

        This command also includes the FSUM command function which vectorially
        sums and prints, in each component direction for the total selected
        node set, the nodal force and moment contributions of the selected
        elements attached to the selected node set.
        """
        command = f"NFORCE,{item}"
        return self.run(command, **kwargs)

    def nldpost(self, label="", key="", fileid="", prefix="", **kwargs):
        """Gets element component information from nonlinear diagnostic files.

        APDL Command: NLDPOST

        Parameters
        ----------
        label
            Specifies the type of command operation:

            EFLG - Element flag for nonlinear diagnostics.

            NRRE - Newton-Raphson residuals.

        key
            Specifies the command action:

            STAT - List information about the diagnostic files (Jobname.ndxxx or Jobname.nrxxx) in
                   the current directory.

            For Label = EFLG, the listing gives a summary that associates the loadstep, substep, time, equilibrium iteration number, cumulative iteration number, and the number of elements that fail each criteria with a specific file ID (Jobname.ndxxx). Use the list to create element components (via the CM option) based on the cumulative iteration number. - For Label = NRRE, the listing provides a summary that associates the loadstep,
                              substep, time, equilibrium iteration number, and
                              cumulative iteration number with a specific file
                              ID (Jobname.nrxxx).  Use the list to identify the
                              respective file ID for creating Newton-Raphson
                              residual contour plots (PLNSOL,NRRE,…,FileID).

            DEL - Delete Jobname.ndxxx or Jobname.nrxxx files in the working directory, if any
                  exist.

            CM - Create components for elements that violate criteria. This value is valid only
                 when Label = EFLG.

        fileid
            Valid only when Label = EFLG and Key = CM, this value specifies
            file IDs:

            IDnum - The file ID number. Creates the element components from the diagnostic files
                    corresponding to the specified file ID number in the
                    working directory.

            ALL - Creates element components from all available diagnostic files residing in the
                  working directory. This value is the default if you do not
                  specify an IDnum value.

        prefix
            Sets the prefix name for components. Specify up to 21 alphanumeric
            characters.

        Notes
        -----
        Based on the nonlinear diagnostic results (created via the NLDIAG,EFLG
        command), the NLDPOST command creates element components with
        predefined names.

        The following table lists the diagnostic criteria and component names
        (with specified prefix and without). Here xxx corresponds to the file
        ID (FileID) of Jobname.ndxxx or Jobname.nrxxx.

        If you have trouble viewing specific element components, see Viewing
        Hidden Element Components in the Basic Analysis Guide.

        For more information, see Performing Nonlinear Diagnostics.
        """
        command = f"NLDPOST,{label},{key},{fileid},{prefix}"
        return self.run(command, **kwargs)

    def plcamp(
        self,
        option="",
        slope="",
        unit="",
        freqb="",
        cname="",
        stabval="",
        keyallfreq="",
        keynegfreq="",
        **kwargs,
    ):
        """Plots Campbell diagram data for applications involving rotating

        APDL Command: PLCAMP
        structure dynamics.

        Parameters
        ----------
        option
            Flag to activate or deactivate sorting of forward or backward whirl
            frequencies:

            0 (OFF or NO) - No sorting.

            1 (ON or YES) - Sort. This value is the default.

        slope
            The slope of the line to be printed. This value must be positive.

            SLOPE > 0  - The line represents the number of excitations per revolution of the rotor. For
                         example, SLOPE = 1 represents one excitation per
                         revolution, usually resulting from unbalance.

            SLOPE = 0  - The line represents the stability threshold for stability values or logarithmic
                         decrements printout (STABVAL = 1 or 2)

        unit
            Specifies the unit of measurement for rotational angular
            velocities:

            RDS - Rotational angular velocities in radians per second (rad/s). This value is the
                  default.

            RPM - Rotational angular velocities in revolutions per minute (RPMs).

        freqb
            The beginning, or lower end, of the frequency range of interest.
            The default is zero.

        cname
            The rotating component name.

        stabval
            Flag to plot the stability values:

            0 (OFF or NO) - Plot the frequencies (the imaginary parts of the eigenvalues in Hz). This value
                            is the default.

            1 (ON or YES) - Plot the stability values (the real parts of the eigenvalues in Hz).

            2 - Plot the logarithmic decrements.

        keyallfreq
            Key to specify if all frequencies above FREQB are plotted:

            0 (OFF or NO) - A maximum of 10 frequencies are plotted. This value is the default.

            1 (ON or YES) - All frequencies are plotted.

        keynegfreq
            Key to specify if the negative frequencies are plotted. It only
            applies to solutions obtained with the damped eigensolver (Method =
            DAMP on the MODOPT command):

            0 (OFF or NO) - Only positive frequencies are plotted. This value is the default.

            1 (ON or YES) - Negative and positive frequencies are plotted.

        Notes
        -----
        The following items are required when generating a Campbell diagram:

        Take the gyroscopic effect into account by issuing the CORIOLIS command
        in the SOLUTION module.

        Run a modal analysis using the QR damped (MODOPT,QRDAMP) or damped
        (MODOPT,DAMP) method. Complex eigenmodes are necessary
        (MODOPT,QRDAMP,,,,Cpxmod  = ON), and you must specify the number of
        modes to expand (MXPAND).

        Define two or more load step results with an ascending order of
        rotational velocity (OMEGA or CMOMEGA).

        In some cases where modes are not in the same order from one load step
        to the other, sorting the frequencies (Option = 1) can help to obtain a
        correct plot. Sorting is based on the comparison between complex mode
        shapes calculated at two successive load steps.

        At each load step, the application compares the mode shape to the loads
        at other load steps to determine whirl direction at the load step. If
        applicable, a label appears (in the plot legend) representing each
        whirl mode (BW for backward whirl and FW for forward whirl).

        At each load step, the program checks for instability (based on the
        sign of the real part of the eigenvalue). The labels "stable" or
        "unstable" appear in the plot legend for each frequency curve.

        The rotational velocities of a named component (Cname) are displayed on
        the X-axis.

        For information on plotting a Campbell diagram for a prestressed
        structure, see Solving for a Subsequent Campbell Analysis of a
        Prestressed Structure Using the Linear Perturbation Procedure in the
        Rotordynamic Analysis Guide.

        In general, plotting a Campbell diagram is recommended only when your
        analysis is performed in a stationary reference frame
        (CORIOLIS,,,,RefFrame = ON).

        For a usage example of the PLCAMP command, see Campbell Diagram in the
        Rotordynamic Analysis Guide.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"PLCAMP,{option},{slope},{unit},{freqb},{cname},{stabval},{keyallfreq},{keynegfreq}"
        return self.run(command, **kwargs)

    def plcfreq(self, spec="", sectbeg="", sectend="", **kwargs):
        """Plots the frequency response for the given CYCSPEC specification.

        APDL Command: PLCFREQ

        Parameters
        ----------
        spec
            CYCSPEC specification number (ordered 1 to N in the order input;
            use CYCSPEC,LIST to view the current list order). Defaults to 1.

        sectbeg
            Beginning sector number to plot. Defaults to 1.

        sectend
            Ending sector number to plot. Defaults to the total number of
            sectors expanded (/CYCEXPAND).

        Notes
        -----
        Following a cyclic mode-superposition harmonic analysis, this command
        plots the result item given by a CYCSPEC specification versus the
        harmonic frequency, one curve for each of the specified sectors. A
        CYCCALC command must have been issued prior to this command.
        """
        command = f"PLCFREQ,{spec},{sectbeg},{sectend}"
        return self.run(command, **kwargs)

    def plchist(self, spec="", freqpt="", **kwargs):
        """Plots a histogram of the frequency response of each sector for the

        APDL Command: PLCHIST
        given CYCSPEC specification.

        Parameters
        ----------
        spec
            CYCSPEC specification number (ordered 1 to N in the order input;
            use CYCSPEC,LIST to view the current list order). Defaults to 1.

        freqpt
            Harmonic frequency point to plot (the data set number NSET or
            CUMULATIVE on SET,LIST). Defaults to the current SET frequency.

        Notes
        -----
        Following a cyclic mode-superposition harmonic analysis, this command
        creates a histogram plot of the result item given by a CYCSPEC
        specification versus the sector number. A CYCCALC command must have
        been issued prior to this command.
        """
        command = f"PLCHIST,{spec},{freqpt}"
        return self.run(command, **kwargs)

    def plfar(
        self,
        lab="",
        option="",
        phi1="",
        phi2="",
        nph1="",
        theta1="",
        theta2="",
        ntheta="",
        val1="",
        val2="",
        val3="",
        **kwargs,
    ):
        """Plots pressure far fields and far field parameters.

        APDL Command: PLFAR

        Parameters
        ----------
        lab
            Parameters to plot :

            PRES - Acoustic parameters

            PROT - Acoustic parameters with the y-axis rotated extrusion

        option
            Plot option, based on the specified plot parameter type:

        phi1, phi2
            Starting and ending φ angles (degrees) in the spherical coordinate
            system. Defaults to 0.

        nphi
            Number of divisions between the starting and ending φ angles for
            data computations. Defaults to 0.

        theta1, theta2
            Starting and ending θ angles (degrees) in the spherical coordinate
            system. Defaults to 0 in 3-D and 90 in 2-D.

        ntheta
            Number of divisions between the starting and ending θ angles for
            data computations. Defaults to 0.

        val1
            Radius of the sphere surface. Used only when Option = SUMC, SUMP,
            PHSC, PHSP, SPLC, SPLP, SPAC, SPAP, PSCT, PSPL, TSCT, or TSPL.

        val2
            When Option = SPLC, SPLP, SPAC, or SPAP: Reference rms sound
            pressure. Defaults to 2x10-5 Pa.

        val3
            When Lab = PRES: Thickness of 2-D model extrusion in the z
            direction (no default).

        Notes
        -----
        The PLFAR command plots pressure far fields and far field parameters as
        determined by the equivalent source principle. Use this command to plot
        pressure and acoustic    parameters. See the HFSYM command for the
        model symmetry and the     HFANG command for spatial radiation angles.

        When Option = PWL no plot is generated, but the sound power level
        appears in the output.

        To retrieve saved equivalent source data, issue the
        SET,Lstep,Sbstep,,REAL command.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"PLFAR,{lab},{option},{phi1},{phi2},{nph1},{theta1},{theta2},{ntheta},{val1},{val2},{val3}"
        return self.run(command, **kwargs)

    def plmc(
        self,
        lstep="",
        sbstep="",
        timfrq="",
        kimg="",
        hibeg="",
        hiend="",
        **kwargs,
    ):
        """Plots the modal coordinates from a mode-superposition solution.

        APDL Command: PLMC

        Parameters
        ----------
        lstep, sbstep
            Plot the solution identified as load step LSTEP and substep SBSTEP

        timfrq
            As an alternative to LSTEP and SBSTEP, plot the solution at the
            time value TIMFRQ (for ANTYPE,TRANS) or frequency value TIMFRQ (for
            ANTYPE,HARMIC). LSTEP and SBSTEP should be left blank.

        kimg
            If 0 (or blank), plot the real solution. If 1, plot the imaginary
            solution. Only valid for ANTYPE,HARMIC.

        hibeg, hiend
            For cyclic symmetry solutions, plot the solutions in the harmonic
            index solution range HIbeg to HIend. Defaults to all harmonic
            indices (all modes).

        Notes
        -----
        PLMC plots a histogram of the modal coordinates (the response
        amplitudes applied to each mode shape) at a certain time point
        (transient analyses) or frequency point (harmonic analyses). The
        absolute values of the modal coordinates are plotted. Use /XRANGE to
        plot only modes in a certain range, if desired.

        For transient analyses, the Jobname.RDSP file must be available. For
        harmonic analyses, the Jobname.RFRQ must be available. No SET command
        is required and no expansion pass is required.

        For a cyclic harmonic mode-superposition analysis, use the CYCFILES
        command to identify the Jobname.RFRQ and modal Jobname.RST file. You
        may limit the plot to display only those modes in a certain harmonic
        index range. The modes having the same harmonic index are each plotted
        in a unique color. If there are less than 10 harmonic indices, they are
        identified in the graphics legend.

        This is a graphical representation of the optional Jobname.MCF text
        file. (see the TRNOPT and HROPT commands). For more information on
        modal coordinates, see Mode-Superposition Method in the Mechanical APDL
        Theory Reference.
        """
        command = f"PLMC,{lstep},{sbstep},{timfrq},{kimg},{hibeg},{hiend}"
        return self.run(command, **kwargs)

    def plnear(
        self,
        lab="",
        opt="",
        kcn="",
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
        """Plots the pressure in the near zone exterior to the equivalent source

        APDL Command: PLNEAR
        surface.

        Parameters
        ----------
        lab
            Plot the maximum pressure or sound pressure level:

            SPHERE - on the spherical structure

            PATH - along the path

        opt
            PSUM

            PSUM  - Maximum complex pressure for acoustics.

            PHAS  - Phase angle of complex pressure for acoustics.

            SPL  - Sound pressure level for acoustics.

            SPLA - A-weighted sound pressure level for acoustics (dBA).

        kcn
            KCN is the coordinate system reference number. It may be 0
            (Cartesian) or any previously defined local coordinate system
            number (>10). Defaults to 0.

        val1, val2, val3, . . . , val9
            For LAB = SPHERE:

            VAL1 - Radius of spherical surface in spherical coordinate system.

            VAL2 - Starting φ angle (degree) in the spherical coordinate system. Defaults to 0.

            VAL3 - Ending φ angle (degree) in the spherical coordinate system. Defaults to 0.

            VAL4 - Number of divisions between the starting and ending φ angles for data
                   computations. Defaults to 0.

            VAL5 - Starting θ angle (degrees) in the spherical coordinate system. Defaults to 0 in
                   3-D and 90 in 2-D extension.

            VAL6 - Ending θ angle (degrees) in the spherical coordinate system. Defaults to 0 in
                   3-D and 90 in 2-D extension.

            VAL7 - Number of divisions between the starting and ending θ angles for data
                   computations. Defaults to 0.

            VAL8 - Reference rms sound pressure. Defaults to 2x10-5 Pa.

            VAL9 - Thickness of 2-D model extension in z direction (defaults to 0).

        Notes
        -----
        PLNEAR uses the equivalent source principle to calculate the pressure
        in the near zone exterior to the equivalent source surface (flagged
        with the Maxwell surface flag in the preprocessor) for one of the
        following locations:

        A spherical surface in the KCN coordinate system

        A path defined by the PATH and PPATH commands

        To plot the pressure results for a path, use the PLPAGM or PLPATH
        commands. See the HFSYM command for the model symmetry.

        To retrieve saved equivalent source data, issue the
        SET,Lstep,Sbstep,,REAL command.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"PLNEAR,{lab},{opt},{kcn},{val1},{val2},{val3},{val4},{val5},{val6},{val7},{val8},{val9}"
        return self.run(command, **kwargs)

    def plzz(self, rotvel="", deltarotvel="", **kwargs):
        """Plots the interference diagram from a cyclic modal analysis.

        APDL Command: PLZZ

        Parameters
        ----------
        rotvel
            Rotational speed in revolutions per minute (RPM) used to define the
            speed line. If blank, use the rotational speed (from OMEGA)
            specified in the prestressing step of the linear perturbation
            analysis. If explicitly input as 0, or if the linear perturbation
            was not used, no speed lines are plotted.

        deltarotvel
            Adds speed lines about the RotVel speed line corresponding to
            RotVel ± DeltaRotVel. Only plotted if RotVel is known.

        Notes
        -----
        PLZZ plots the cyclic modal frequencies as points on a frequency vs.
        harmonic index (nodal diameter) graph. If rotational speed (RotVel) is
        provided, the speed line is also plotted, leading to the interference
        diagram (also known as the SAFE or ZZENF diagram). If DeltaRotVel is
        also provided, two additional speed lines are plotted, enveloping the
        safe speed line itself.

        For more information, see Postprocessing a Modal Cyclic Symmetry
        Analysis in the Cyclic Symmetry Analysis Guide.
        """
        command = f"PLZZ,{rotvel},{deltarotvel}"
        return self.run(command, **kwargs)

    def pras(self, quantity="", loadstep="", substep="", **kwargs):
        """Calculates a specified acoustic quantity on the selected exterior

        APDL Command: PRAS
        surface or the frequency-band sound pressure level (SPL).

        Parameters
        ----------
        quantity
            The acoustic quantity to calculate:

            SIMP - Specific acoustic impedance on the selected surface.

            AIMP  - Acoustic impedance on the selected surface.

            MIMP  - Mechanical impedance on the selected surface.

            PRES  - Average pressure on the selected surface.

            FORC  - Force on the selected surface.

            POWE  - Acoustic power on the selected surface.

            BSPL  - Frequency-band sound pressure level.

            BSPA  - A-weighted frequency-band sound pressure level.

        loadstep
            Specified load step. Default = 1.

        substep
            Specified substep. Default = All substeps at the specified load
            step. Not valid for Quantity = BSPL or BSPA.

        Notes
        -----
        The PRAS command calculates a specified acoustic quantity on the
        selected exterior surface in postprocessing. The calculation is based
        on the pressure and velocity solution or the frequency-band sound
        pressure level (SPL).

        The total pressure and velocity are used if the selected surface is the
        excitation source surface. To calculate the incoming and outgoing
        acoustic power, and other sound power parameters, on the excitation
        source surface, issue the SF,,PORT and SPOWER commands.

        The sound pressure level of the octave bands and general frequency band
        (defined via the HARFRQ command) is calculated at the selected nodes in
        the model.
        """
        command = f"PRAS,{quantity},{loadstep},{substep}"
        return self.run(command, **kwargs)

    def prcamp(
        self,
        option="",
        slope="",
        unit="",
        freqb="",
        cname="",
        stabval="",
        keyallfreq="",
        keynegfreq="",
        **kwargs,
    ):
        """Prints Campbell diagram data for applications involving rotating

        APDL Command: PRCAMP
        structure dynamics.

        Parameters
        ----------
        option
            Flag to activate or deactivate sorting of forward or backward whirl
            frequencies:

            0 (OFF or NO) - No sorting.

            1 (ON or YES) - Sort. This value is the default.

        slope
            The slope of the line to be printed. This value must be positive.

            SLOPE > 0  - The line represents the number of excitations per revolution of the rotor. For
                         example, SLOPE = 1 represents one excitation per
                         revolution, usually resulting from unbalance.

            SLOPE = 0  - The line represents the stability threshold for stability values or logarithmic
                         decrements printout (STABVAL = 1 or 2)

        unit
            Specifies the unit of measurement for rotational angular
            velocities:

            RDS - Rotational angular velocities in radians per second (rad/s). This value is the
                  default.

            RPM - Rotational angular velocities in revolutions per minute (RPMs).

        freqb
            The beginning, or lower end, of the frequency range of interest.
            The default is zero.

        cname
            The rotating component name.

        stabval
            Flag to print the stability values:

            0 (OFF or NO) - Print the frequencies (the imaginary parts of the eigenvalues in Hz). This
                            value is the default.

            1 (ON or YES) - Print the stability values (the real parts of the eigenvalues in Hz).

            2 - Print the logarithmic decrements.

        keyallfreq
            Key to specify if all frequencies above FREQB are printed out:

            0 (OFF or NO) - A maximum of 10 frequencies are printed out. They correspond to the frequencies
                            displayed via the PLCAMP command. This value is the
                            default.

            1 (ON or YES) - All frequencies are printed out.

        keynegfreq
            Key to specify if the negative frequencies are printed out. It only
            applies to solutions obtained with the damped eigensolver
            (Method=DAMP on the MODOPT command):

            0 (OFF or NO) - Only positive frequencies are printed out. This value is the default.

            1 (ON or YES) - Negative and positive frequencies are printed out.

        Notes
        -----
        The following items are required when generating a Campbell diagram:

        Take the gyroscopic effect into account by issuing the CORIOLIS command
        in the SOLUTION module.

        Run a modal analysis using the QR damped (MODOPT,QRDAMP) or damped
        (MODOPT,DAMP) method. Complex eigenmodes are necessary
        (MODOPT,QRDAMP,,,,Cpxmod  = ON), and you must specify the number of
        modes to expand (MXPAND).

        Define two or more load step results with an ascending order of
        rotational velocity (OMEGA or CMOMEGA).

        In some cases where modes are not in the same order from one load step
        to the other, sorting the frequencies (Option = 1) can help to obtain a
        correct printout. Sorting is based on the comparison between complex
        mode shapes calculated at two successive load steps.

        At each load step, the application compares the mode shape to the loads
        to determine the whirl direction. If applicable, a label appears (on
        the rows of output data) representing the whirl mode (BW for backward
        whirl and FW for forward whirl).

        If you specify a non-zero slope (SLOPE > 0), the command prints the
        critical speeds corresponding to the intersection points of the
        frequency curves and the added line. In the case of a named component
        (Cname), critical speeds relate to the rotational velocity of the
        component. Critical speeds are available only if the frequencies are
        printed (STABVAL = OFF).

        If you specify a zero slope (SLOPE = 0), the command prints the
        stability threshold corresponding to the sign change of the stability
        values (or logarithmic decrements). In the case of a named component
        (Cname), stability thresholds relate to the rotational velocity of the
        component. Stability thresholds are available only if the stability
        values or logarithmic decrements are printed (STABVAL = 1 or 2).

        At each load step, the program checks for instability (based on the
        sign of the real part of the eigenvalue). The label "U" appears on the
        printout for each unstable frequency.

        If specified, the rotational velocities of the named component (Cname)
        are printed out along with the natural frequencies.

        In general, printing a Campbell diagram is recommended only when your
        analysis is performed in a stationary reference frame
        (CORIOLIS,,,,RefFrame = ON).

        For information on printing a Campbell diagram for a prestressed
        structure, see Solving for a Subsequent Campbell Analysis of a
        Prestressed Structure Using the Linear Perturbation Procedure in the
        Rotordynamic Analysis Guide.

        For a usage example of the companion command PLCAMP (used for plotting
        a Campbell diagram), see Example Campbell Diagram Analysis.

        For more information on Campbell diagram generation, see Campbell
        Diagram in the Rotordynamic Analysis Guide.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"PRCAMP,{option},{slope},{unit},{freqb},{cname},{stabval},{keyallfreq},{keynegfreq}"
        return self.run(command, **kwargs)

    def prfar(
        self,
        lab="",
        option="",
        phi1="",
        phi2="",
        nph1="",
        theta1="",
        theta2="",
        ntheta="",
        val1="",
        val2="",
        val3="",
        **kwargs,
    ):
        """Prints pressure far fields and far field parameters.

        APDL Command: PRFAR

        Parameters
        ----------
        lab
            Parameters to print:

            PRES - Acoustic parameters

            PROT - Acoustic parameters with the y-axis rotated extrusion

        option
            Print option, based on the specified print parameter type:

        phi1, phi2
            Starting and ending φ angles (degrees) in the spherical coordinate
            system. Defaults to 0.

        nphi
            Number of divisions between the starting and ending φ angles for
            data computations. Defaults to 0.

        theta1, theta2
            Starting and ending θ angles (degrees) in the spherical coordinate
            system. Defaults to 0 in 3-D and 90 in 2-D.

        ntheta
            Number of divisions between the starting and ending θ angles for
            data computations. Defaults to 0.

        val1
            Radius of the sphere surface. Used only when Option = SUMC, PHSC,
            SPLC, SPAC, PSCT, or TSCT.

        val2
            When Option = SPLC or SPAC: Reference rms sound pressure. Defaults
            to 2x10-5 Pa.

        val3
            When Lab = PRES: Thickness of 2-D model extrusion in the z
            direction (no default).

        Notes
        -----
        The PRFAR command prints pressure far fields and far field parameters
        as    determined by the equivalent source principle. Use this command
        to print pressure and acoustic    parameters. See the HFSYM command for
        the model symmetry and the     HFANG command for spatial radiation
        angles.

        To retrieve saved equivalent source data, issue the
        SET,Lstep,Sbstep,,REAL command.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"PRFAR,{lab},{option},{phi1},{phi2},{nph1},{theta1},{theta2},{ntheta},{val1},{val2},{val3}"
        return self.run(command, **kwargs)

    def prnear(
        self,
        lab="",
        opt="",
        kcn="",
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
        """Prints the pressure in the near zone exterior to the equivalent source

        APDL Command: PRNEAR
        surface.

        Parameters
        ----------
        lab
            Print the maximum pressure or sound pressure level:

            POINT - at the point (x,y,z)

            SPHERE - on the spherical structure

            PATH - along the path

        opt
            PSUM

            PSUM  - Maximum complex pressure for acoustics.

            PHAS  - Phase angle of complex pressure for acoustics.

            SPL  - Sound pressure level for acoustics.

            SPLA - A-weighted sound pressure level for acoustics (dBA).

        kcn
            KCN is the coordinate system reference number. It may be 0
            (Cartesian) or any previously defined local coordinate system
            number (>10). Defaults to 0.

        val1, val2, val3, . . . , val9
            For Lab = POINT:

            VAL1 - x coordinate value

            VAL2 - y coordinate value

            VAL3 - z coordinate value

            VAL4 - VAL8 - not used

            VAL9 - Thickness of model in z direction (defaults to 0).

        Notes
        -----
        The command uses the equivalent source principle to calculate the
        pressure in the near zone exterior to the equivalent source surface
        (flagged with the Maxwell surface flag in the preprocessor) for one of
        the following locations:

        A point X, Y, Z in the KCN coordinate system

        A spherical surface in the KCN coordinate system

        A path defined by the PATH and PPATH commands

        To list the pressure results for a path, use the PRPATH command. See
        HFSYM command for the model symmetry.

        To retrieve saved equivalent source data, issue the
        SET,Lstep,Sbstep,,REAL command.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"PRNEAR,{lab},{opt},{kcn},{val1},{val2},{val3},{val4},{val5},{val6},{val7},{val8},{val9}"
        return self.run(command, **kwargs)

    def reswrite(self, fname="", cflag="", **kwargs):
        """Appends results data from the database to a results file.

        APDL Command: RESWRITE

        Parameters
        ----------
        fname
            File name and directory path (248 characters maximum,
            including the characters needed for the directory
            path). An unspecified directory path defaults to the
            working directory; in this case, you can use all 248
            characters for the file name.  The file name extension
            varies as follows:

            - .RST for structural, fluid, or coupled-field analyses
            - .RTH for thermal or electrical analyses
            - .RMG for magnetic analyses

        cflag
            0 - The complex results flag is set to 0 in the results
            file header. This is the default option.

            1 - The complex results flag is set to 1 in the results
            file header.

        Notes
        -----
        The RESWRITE command appends a data set to the specified file
        by writing the results data currently in the database. If the
        intended results file does not exist, it will be created and
        will include the geometry records. The current load step,
        substep, and time (or frequency) value are maintained. All
        data (summable and nonsummable) are written.

        When complex results are appended, cFlag must be set to 1 so
        that the header is consistent with the results written on the
        file.

        The command is primarily intended for use in a top-down
        substructuring analysis, where the full model is resumed and
        the results data read from the use pass results file (SET),
        and subsequently from all substructure expansion pass results
        files (APPEND). The full set of data in memory can then be
        written out via the RESWRITE command to create a complete
        results file (as though you had run a nonsubstructured
        analysis).

        The RESWRITE command can also be used to write a global
        results file for a distributed parallel (Distributed ANSYS)
        solution. This should only be necessary if the RESCOMBINE
        command was used to combine results from local results files
        into the database. The RESWRITE command can then be used to
        write the combined results into a new results file.  This new
        results file will essentially contain the current set of
        results data for the entire (i.e., global) model.
        """

        return self.run(f"RESWRITE,{fname},,,,{cflag}", **kwargs)

    def rmflvec(self, **kwargs):
        """Writes eigenvectors of fluid nodes to a file for use in damping

        APDL Command: RMFLVEC
        parameter extraction.

        Notes
        -----
        RMFLVEC extracts the modal information from the modal results file for
        all nodes specified in a node component called 'FLUN'. This component
        should include all nodes which are located at the fluid-structural
        interface. Mode shapes, element normal orientation, and a scaling
        factor are computed and stored in a file Jobname.EFL. For damping
        parameter extraction, use the DMPEXT command macro. See Introduction
        for more information on thin film analyses.

        FLUID136 and FLUID138 are used to model the fluid interface. Both the
        structural and fluid element types must be active. The fluid interface
        nodes must be grouped into a component 'FLUN'. A results file of the
        last modal analysis must be available.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"RMFLVEC,"
        return self.run(command, **kwargs)

    def rsplit(
        self,
        option="",
        label="",
        name1="",
        name2="",
        name3="",
        name4="",
        name5="",
        name6="",
        name7="",
        name8="",
        name9="",
        name10="",
        name11="",
        name12="",
        name13="",
        name14="",
        name15="",
        name16="",
        **kwargs,
    ):
        """Creates one or more results file(s) from the current results file based

        APDL Command: RSPLIT
        on subsets of elements.

        Parameters
        ----------
        option
            Specify which results to include for the subset of elements.

            ALL  - Write all nodal and element results based on the subset of elements (default).

            EXT  - Write only the nodal and element results that are on the exterior surface of
                   the element subset. The results data will be averaged as in
                   PowerGraphics (see AVRES) when this results file is brought
                   into POST1. Only valid for solid elements.

        label
            Define where the element subset is coming from.

            ALL  - Use all selected element components (CMSEL) (default).

            ESEL  - Use the currently selected (ESEL) set of elements. Name1 defines the results
                    file name.

            LIST - Use Name1 to Name16 to list the element component and/or assembly names (that
                   contain element components).

        name1, name2, name3, . . . , name16
            Up to 16 element component and/or assembly names (that contain
            element components).

        Notes
        -----
        Results files will be named based on the element component or assembly
        name, e.g., Cname.rst, except for the ESEL option, for which you must
        specify the results file name (no extension) using the Name1 field.
        Note that the .rst filename will be written in all uppercase letters
        (CNAME.rst) (unless using the ESEL option); when you read the file, you
        must specify the filename using all uppercase letters (i.e.,
        file,CNAME). You may repeat the RSPLIT command as often as needed. All
        results sets on the results file are processed. Use /AUX3 to produce a
        results file with just a subset of the results sets.

        Use INRES to limit the results data written to the results files.

        The subset geometry is also written so that no database file is
        required to postprocess the subset results files. You must not resume
        any database when postprocessing one of these results files. The input
        results file must have geometry written to it (i.e., do not use
        /CONFIG,NORSTGM,1).

        Applied forces and reaction forces are not apportioned if their nodes
        are shared by multiple element subsets. Their full values are written
        to each results file.

        Each results file renumbers its nodes and elements starting with 1.

        This feature is useful when working with large models. For more
        information on the advantages and uses of the RSPLIT command, see
        Splitting Large Results Files in the Basic Analysis Guide.
        """
        command = f"RSPLIT,{option},{label},{name1},{name2},{name3},{name4},{name5},{name6},{name7},{name8},{name9},{name10},{name11},{name12},{name13},{name14},{name15},{name16}"
        return self.run(command, **kwargs)

    def rstmac(
        self,
        file1="",
        lstep1="",
        sbstep1="",
        file2="",
        lstep2="",
        sbstep2="",
        maclim="",
        cname="",
        keyprint="",
        **kwargs,
    ):
        """APDL Command: RSTMAC

        Calculates modal assurance criterion (MAC) and matches nodal solutions
        from two results files or from one results file and one universal
        format file.

        Parameters
        ----------
        file1
            File name (32 characters maximum) corresponding to the first
            results file (.rst or .rstp file). If the file name does not
            contain the extension, it defaults to .rst.

        lstep1
            Load step number of the results to be read in File1.

            N  - Reads load step N. Defaults to 1.

        sbstep1
            Substep number of the results to be read in File1.

            N  - Reads substep N.

            All  - Reads all substeps. This value is the default.

        file2
            File name (32 characters maximum) corresponding to the second file
            (.rst, .rstp, or .unv file). If the file name does not contain the
            extension, it defaults to .rst.

        lstep2
            Load step number of the results to be read in File2.

            N  - Reads load step N. Defaults to 1.

        sbstep2
            Substep number of the results to be read in File2.

            N  - Reads substep N.

            All  - Reads all substeps. This value is the default.

        maclim
            Smallest acceptable MAC value. Must be  0 and  1. The default value
            is 0.90.

        cname
            Name of the component from the first file (File1). The component
            must be based on nodes. If unspecified, all nodes are matched and
            used for MAC calculations. If a component name is specified, only
            nodes included in the specified component are used. Not applicable
            to node mapping (TolerN=-1).

        keyprint
            Printout options:

            0  - Printout matched solutions table. This value is the default.

            1  - Printout matched solutions table and full MAC table.

            2  - Printout matched solutions table, full MAC table and matched nodes table.

        Notes
        -----
        The RSTMAC command allows the comparison of the solutions from
        either:

        Two different results files

        One result file and one universal format file

        The modal assurance criterion (MAC) is used.

        The meshes read on File1 and File2 may be different. If TolerN>0,
        the nodes are matched. This is the default. If TolerN = -1, the
        nodes are mapped and the solutions are interpolated from File1.

        Units and coordinate systems must be the same for both
        models. When a universal format file is used, the nodal
        coordinates can be scaled using UNVscale.

        The corresponding database file (.db) for File1 must be resumed
        before running the command only if a component (Cname) is used or
        if the nodes are mapped (TolerN = -1).

        Results may be real or complex; however, if results from File1
        have a different type from results in File2, only the real parts
        of the solutions are taken into account in MAC calculations. The
        analysis type can be arbitrary.

        Only structural degrees of freedom are considered. Degrees of
        freedom can vary between File1 and File2, but at least one common
        degree of freedom must exist.

        When node mapping and solution interpolation is performed
        (TolerN=-1), File1 must correspond to a model meshed in solid
        and/or shell elements.  Other types of elements can be present but
        the node mapping is not performed for those
        elements. Interpolation is performed on UX, UY, and UZ degrees of
        freedom.

        The solutions read on the results files are not all written to the
        database, therefore, subsequent plotting or printing of solutions
        is not possible.  A SET command must be issued after the RSTMAC
        command to post-process each solution.

        RSTMAC comparison on cyclic symmetry analysis works only if the
        number of sectors on File1 and File2 are the same. Also comparison
        cannot be made between cyclic symmetry results and full 360 degree
        model results (File1 – cyclic solution, File2 – full 360 degree
        model solution).  Comparing cyclic symmetry solutions written on
        selected set of node (OUTRES) is not supported.

        The modal assurance criterion values can be retrieved as
        parameters using the ``*GET`` command (Entity = RSTMAC).

        For more information and an example, see Comparing Nodal Solutions
        From Two Models (RSTMAC) in the Basic Analysis Guide.
        """
        command = f"RSTMAC,{file1},{lstep1},{sbstep1},{file2},{lstep2},{sbstep2},,{maclim},{cname},{keyprint}"
        return self.run(command, **kwargs)

    def spoint(self, node="", x="", y="", z="", **kwargs):
        """Defines a point for moment summations.

        APDL Command: SPOINT

        Parameters
        ----------
        node
            Node number of the desired point.  If zero, use X,Y,Z to describe
            point.

        x, y, z
            Global Cartesian coordinates of the desired summation point.  Used
            if NODE is 0.  Defaults to (0,0,0).

        Notes
        -----
        Defines a point (any point other than the origin) about which the
        tabular moment summations are computed [NFORCE, FSUM].  If force
        summations are desired in other than the global Cartesian directions, a
        node number must be specified on the NODE field, and the desired
        coordinate system must be activated with RSYS.
        """
        command = f"SPOINT,{node},{x},{y},{z}"
        return self.run(command, **kwargs)

    def spmwrite(
        self,
        method="",
        nmode="",
        inputs="",
        inputlabels="",
        outputs="",
        outputlabels="",
        nic="",
        velacckey="",
        fileformat="",
        **kwargs,
    ):
        """Calculates the state-space matrices and writes them to the SPM file.

        APDL Command: SPMWRITE

        Parameters
        ----------
        method
            Reduction method for the calculation of the state-space matrices.

            MODAL - Method based on modal analysis results from LANB, LANPCG, SNODE, or SUBSP
                    eigensolver (default).

        nmode
            Number of modes to be used. Defaults to all modes.

        inputs
            Definition of the inputs. Defaults to all load vectors on the MODE
            file.

        inputlabels
            Definition of the input labels. Defaults to the load vector numbers
            or input definition (node and degree of freedom array parameter),
            depending on the Inputs specification.

        outputs
            Definition of the outputs. Defaults to the inputs.

        outputlabels
            Definition of the output labels. Defaults to the output definition
            (node and degree of freedom) if used, else defaults to the
            InputLabels.

        nic
            Load vector on the MODE file used for the calculation of the
            initial conditions. Defaults to no initial condition.

        velacckey
            Output velocities and accelerations key.

            OFF - Output displacements only (default).

            ON - Output displacements, velocities and accelerations.

        fileformat
            The format of the SPM file.

            0 - Dense format.

            1 - Matrix Market Exchange format (non-zero terms only).

            2 - Simplorer SML format without reference (default).

            3 - Simplorer SML format with common reference.

            4 - Simplorer SML format with independent references.

        Notes
        -----
        The SPMWRITE generates the file Jobname.SPM containing the state-space
        matrices and other information.

        The following applies to the SML formats (FileFormat = 2, 3, and 4):

        For conservative systems where the outputs are equal to the inputs
        (Outputs is left blank):

        The labels for the inputs (InputLabels) are required.

        The Inputs must use the array parameter option so that the input
        degrees of freedom (DOFs) are known.

        For non-conservative systems where the outputs are not equal to the
        inputs:

        The labels for the outputs (OutputLabels) are required.

        The file formats with references (FileFormat = 3 and 4) do not apply.

        Velocity and acceleration results are not included in the state-space
        matrices calculation (VelAccKey = OFF)

        File format with common reference (FileFormat = 3) does not apply if
        the inputs are based on DOFs of a different nature.  All input DOFs
        must be either all rotational or all translational and not a mix of the
        two.

        A graphics file (Jobname_SPM.PNG) is generated. It contains an element
        plot of the model.

        For more details about the reduction method and the generation of the
        state-space matrices, see Reduced-Order Modeling for State-Space
        Matrices Export in the Mechanical APDL Theory Reference.

        For examples of the command usage, see State-Space Matrices Export.
        """
        command = f"SPMWRITE,{method},{nmode},{inputs},{inputlabels},{outputs},{outputlabels},{nic},{velacckey},{fileformat}"
        return self.run(command, **kwargs)
