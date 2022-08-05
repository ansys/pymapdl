from typing import Optional

from ansys.mapdl.core.mapdl_types import MapdlInt


class Setup:
    def ansol(
        self,
        nvar="",
        node="",
        item="",
        comp="",
        name="",
        mat="",
        real="",
        ename="",
        **kwargs,
    ):
        """Specifies averaged nodal data to be stored from the results file in the

        APDL Command: ANSOL
        solution coordinate system.

        Parameters
        ----------
        nvar
            Arbitrary reference number assigned to this variable (2 to NV
            [NUMVAR]). Overwrites any existing results for this variable.

        node
            Node number for which data are to be stored.

        item
            Label identifying the item. General item labels are shown in
            Table 126: ANSOL - General Item and Component Labels below. Some
            items also require a component label.

        comp
            Component of the item (if required). General component labels are
            shown in Table 126: ANSOL - General Item and Component Labels
            below.

        name
            Thirty-two character name for identifying the item on the printout
            and displays. Defaults to an eight character label formed by
            concatenating the first four characters of the Item and Comp
            labels.

        mat
            The material number. Average will be computed based on the subset
            of elements with the specified material number. DEFAULT: Use all
            elements in the active set unless Real and/or Ename is specified.

        real
            The real number. Average will be computed based on the subset of
            elements with the specified real number. DEFAULT: Use all elements
            in the active set unless Mat and/or Ename is specified.

        ename
            The element type name. Average will be computed based on the subset
            of elements with the specified element type name. DEFAULT: Use all
            elements in the active set unless Mat and/or Real is specified.

        Notes
        -----
        Valid item and component labels for averaged nodal results are listed
        in Table: 126:: ANSOL - General Item and Component Labels, below.

        All element nodal quantities are obtained in RSYS, Solu and then
        averaged.

        The ANSOL command defines averaged nodal results data to be stored from
        a results file [FILE]. Not all items are valid for all nodes. See the
        input and output summary tables of the Element Reference of each
        element that is attached to the node for the available items.

        COORDINATE SYSTEMS: All element nodal results used by ANSOL for
        averaging are in the element coordinate system, except for layered
        elements. Layered element results are in the layer coordinate system.
        You can further specify the element nodal results, for some elements,
        with the SHELL, LAYERP26, and FORCE commands.

        ANSOL does not transform results from RSYS, SOLU to other coordinate
        systems. Verify that all elements attached to the subject node have the
        same coordinate system before using ANSOL.

        SHELL ELEMENTS: The default shell element coordinate system is based on
        node ordering. For shell elements the adjacent elements could have a
        different RSYS,SOLU, making the resultant averaged data inconsistent. A
        note to this effect is issued when ANSOL is used in models containing
        shell elements. Ensure that consistent coordinate systems are active
        for all associated elements used by the ANSOL command.

        DERIVED QUANTITIES: Some of the result items supported by ANSOL (see
        Table: 126:: ANSOL - General Item and Component Labels) are derived
        from the component quantities. Use AVPRIN to specify the principal and
        vector sum quantity averaging methods.

        DEFAULT: If Mat, Real , and Ename are not specified, all of the
        elements attached to the node will be considered. When a material ID,
        real constant ID, or element type discontinuity is detected at a node,
        a note is issued. For example, in a FSI analysis, a FLUID30 element at
        the structure interface would be considered. But since it contains no
        SX result, it will not be used during STORE operations.

        Table: 126:: : ANSOL - General Item and Component Labels

        For more information on the meaning of contact status and its possible
        values, see Reviewing Results in POST1 in the Contact Technology Guide.
        """
        command = f"ANSOL,{nvar},{node},{item},{comp},{name},{mat},{real},{ename}"
        return self.run(command, **kwargs)

    def cisol(self, n="", id_="", node="", cont="", dtype="", **kwargs):
        """Stores fracture parameter information in a variable.

        APDL Command: CISOL

        Parameters
        ----------
        n
            Arbitrary reference number or name assigned to this variable.
            Number must be >1 but </= NUMVAR.

        id\_
            Crack ID number.

        node
            Crack tip node number.

        cont
            Contour number.

        dtype
            Data type to output:

            JINT - J-integral

            IIN1 - Interaction integral 1

            IIN2  - Interaction integral 2

            IIN3 - Interaction integral 3

            K1 - Mode 1 stress-intensity factor

            K2 - Mode 2 stress-intensity factor

            K3 - Mode 3 stress-intensity factor

            G1 - Mode 1 energy release rate

            G2  - Mode 2 energy release rate

            G3  - Mode 3 energy release rate

            GT - Total energy release rate

            MFTX - Total material force X

            MFTY - Total material force Y

            MFTZ - Total material force Z

            CEXT - Crack extension
        """
        command = f"CISOL,{n},{id_},{node},{cont},{dtype}"
        return self.run(command, **kwargs)

    def data(self, ir="", lstrt="", lstop="", linc="", name="", kcplx="", **kwargs):
        """Reads data records from a file into a variable.

        APDL Command: DATA

        Parameters
        ----------
        ir
            Arbitrary reference number assigned to the resulting variable (2 to
            NV [NUMVAR]).  If this number is the same as for a previously
            defined variable, the previously defined variable will be
            overwritten with this result.

        lstrt
            Start at location LSTRT (defaults to 1).

        lstop
            Stop at location LSTOP (defaults to LSTRT).  Maximum location
            available is determined from data previously stored.

        linc
            Fill every LINC location between LSTRT and LSTOP (defaults to 1).

        name
            Eight character name for identifying the variable on the printout
            and displays.  Embedded blanks are compressed upon output.

        kcplx
            Complex number key:

            0 - Data stored as the real part of the complex number.

            1 - Data stored as the imaginary part of the complex number.

        Notes
        -----
        This command must be followed by a format statement (on the next line)
        and the subsequent data records, and all must be on the same file (that
        may then be read with the /INPUT command).  The format specifies the
        number of fields to be read per record, the field width, and the
        placement of the decimal point (if one is not included in the data
        value).  The read operation follows the available FORTRAN FORMAT
        conventions of the system.  See the system FORTRAN manual for details.
        Any standard FORTRAN real format (such as (4F6.0), (F2.0,2X,F12.0),
        etc.) may be used.  Integer (I), character (A), and list-directed (*)
        descriptors may not be used.  The parentheses must be included in the
        format.  Up to 80 columns per record may be read.  Locations may be
        filled within a range.  Previous data in the range will be overwritten.
        """
        command = f"DATA,{ir},{lstrt},{lstop},{linc},{name},{kcplx}"
        return self.run(command, **kwargs)

    def edread(self, nstart="", label="", num="", step1="", step2="", **kwargs):
        """Reads explicit dynamics output into variables for time-history

        APDL Command: EDREAD
        postprocessing.

        Parameters
        ----------
        nstart
            Starting reference number assigned to the first variable. Allowed
            range is 2 (the default) to NV [NUMVAR].  (NV defaults to 30 for an
            explicit dynamics analysis.)

        label
            Label identifying the output file to be read. No default.

            GLSTAT - Read data from the GLSTAT file.

            MATSUM - Read data from the MATSUM file.

            SPCFORC - Read data from the SPCFORC file.

            RCFORC - Read data from the RCFORC file.

            SLEOUT - Read data from the SLEOUT file.

            NODOUT - Read data from the NODOUT file.

            RBDOUT - Read data from the RBDOUT file.

        num
            Number identifying the data set to be read in (defaults to 1). If
            Label = GLSTAT, NUM is ignored. If Label = MATSUM or RBDOUT, NUM is
            the PART number [EDPART] for which output is desired. If Label =
            SPCFORC or NODOUT, NUM is the node number for which output is
            desired. If Label  = SLEOUT or RCFORC, NUM is the number of the
            contact entity for which output is desired.

        step1, step2
            Load step range of data to be read in. If STEP1 and STEP2 are
            blank, all load steps are read in.

        Notes
        -----
        EDREAD reads data from the specified ascii output file so that it may
        be used during postprocessing. After EDREAD, you must issue the STORE
        command to store the data in time history variables. Once stored, the
        variables can be viewed as plots of output item versus time.

        The number of variables stored depends on the file specified. The
        following table shows the items in each file and the order in which
        they are stored.  If data items were previously stored in variables
        NSTART to NSTART+15, they will be overwritten. If more variables are
        needed, change NV on the NUMVAR command. (Note that hourglass energy
        will not be available if it was not specified for the model
        [EDENERGY,1].)

        The following items under MATSUM are listed in the MATSUM ASCII file
        (in the Mat no. field) for each part number at time intervals specified
        by the EDHTIME command. Use EDREAD,,MATSUM,NUM to specify the part
        number that corresponds to the mat number in the MATSUM file.

        Resultant contact forces and sliding interface energies are available
        from the RCFORC and SLEOUT files, respectively. The RCFORC file is
        written for surface based contact types that include target and contact
        (master and slave) definitions.  You should ensure that this file
        contains valid force results before issuing EDREAD,,RCFORC. Only the
        resultant contact forces on the master surface are available for time-
        history postprocessing.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"EDREAD,{nstart},{label},{num},{step1},{step2}"
        return self.run(command, **kwargs)

    def enersol(self, nvar="", item="", name="", **kwargs):
        """Specifies the total energies to be stored.

        APDL Command: ENERSOL

        Parameters
        ----------
        nvar
            Arbitrary reference number assigned to this variable (2 to NV).
        """
        command = f"ENERSOL,{nvar},{item},{name}"
        return self.run(command, **kwargs)

    def esol(
        self,
        nvar: MapdlInt = "",
        elem: MapdlInt = "",
        node: MapdlInt = "",
        item: str = "",
        comp: str = "",
        name: str = "",
        **kwargs,
    ) -> Optional[str]:
        """Specify element data to be stored from the results file.

        /POST26 APDL Command: ESOL

        Parameters
        ----------
        nvar
            Arbitrary reference number assigned to this variable (2 to
            NV [NUMVAR]). Overwrites any existing results for this
            variable.

        elem
            Element for which data are to be stored.

        node
            Node number on this element for which data are to be
            stored. If blank, store the average element value (except
            for FMAG values, which are summed instead of averaged).

        item
            Label identifying the item. General item labels are shown
            in Table 134: ESOL - General Item and Component Labels
            below. Some items also require a component label.

        comp
            Component of the item (if required). General component
            labels are shown in Table 134: ESOL - General Item and
            Component Labels below.  If Comp is a sequence number (n),
            the NODE field will be ignored.

        name
            Thirty-two character name for identifying the item on the
            printout and displays.  Defaults to a label formed by
            concatenating the first four characters of the Item and
            Comp labels.

        Notes
        -----
        See Table: 134:: ESOL - General Item and Component Labels for
        a list of valid item and component labels for element (except
        line element) results.

        The ESOL command defines element results data to be stored
        from a results file (FILE). Not all items are valid for all
        elements. To see the available items for a given element,
        refer to the input and output summary tables in the
        documentation for that element.

        Two methods of data access are available via the ESOL
        command. You can access some simply by using a generic label
        (component name method), while others require a label and
        number (sequence number method).

        Use the component name method to access general element data
        (that is, element data generally available to most element
        types or groups of element types).

        The sequence number method is required for data that is not
        averaged (such as pressures at nodes and temperatures at
        integration points), or data that is not easily described in a
        generic fashion (such as all derived data for structural line
        elements and contact elements, all derived data for thermal
        line elements, and layer data for layered elements).

        Element results are in the element coordinate system, except
        for layered elements where results are in the layer coordinate
        system.  Element forces and moments are in the nodal
        coordinate system. Results are obtainable for an element at a
        specified node. Further location specifications can be made
        for some elements via the SHELL, LAYERP26, and FORCE commands.

        For more information on the meaning of contact status and its
        possible values, see Reviewing Results in POST1 in the Contact
        Technology Guide.

        Examples
        --------
        Switch to the time-history postprocessor

        >>> mapdl.post26()

        Store the stress in the X direction for element 1 at node 1

        >>> nvar = 2
        >>> mapdl.esol(nvar, 1, 1, 'S', 'X')

        Move the value to an array and access it via mapdl.parameters

        >>> mapdl.dim('ARR', 'ARRAY', 1)
        >>> mapdl.vget('ARR', nvar)
        >>> mapdl.parameters['ARR']
        array(-1991.40234375)

        """
        command = f"ESOL,{nvar},{elem},{node},{item},{comp},{name}"
        return self.run(command, **kwargs)

    def gapf(self, nvar="", num="", name="", **kwargs):
        """Defines the gap force data to be stored in a variable.

        APDL Command: GAPF

        Parameters
        ----------
        nvar
            Arbitrary reference number assigned to this variable (2 to NV
            [NUMVAR]).  Overwrites any existing results for this variable.

        num
            Number identifying gap number for which the gap force is to be
            stored.  Issue the GPLIST command to display gap numbers.

        name
            Thirty-two character name for identifying the item on the printout
            and displays (defaults to the name GAPF).

        Notes
        -----
        Defines the gap force data to be stored in a variable. Applicable only
        to the expansion pass of the mode-superposition linear transient
        dynamic (ANTYPE,TRANS) analysis. The data is usually on Fname.RDSP.
        """
        command = f"GAPF,{nvar},{num},{name}"
        return self.run(command, **kwargs)

    def gssol(self, nvar="", item="", comp="", name="", **kwargs):
        """Specifies which results to store from the results file when using

        APDL Command: GSSOL
        generalized plane strain.

        Parameters
        ----------
        nvar
            Arbitrary reference number or name assigned to this variable.
            Variable numbers can be 2 to NV (NUMVAR) while the name can be an
            eight byte character string. Overwrites any existing results for
            this variable.

        item
            Label identifying item to be stored.

            LENGTH - Change of fiber length at the ending point.

            ROT - Rotation of the ending plane during deformation.

            F - Reaction force at the ending point in the fiber direction.

            M - Reaction moment applied on the ending plane.

        comp
            Component of the item, if Item = ROT or M.

            X - The rotation angle or reaction moment of the ending plane about X.

            Y - The rotation angle or reaction moment of the ending plane about Y.

        name
            Thirty-two character name identifying the item on the printout and
            display. Defaults to the label formed by concatenating the first
            four characters of the Item and Comp labels.

        Notes
        -----
        This command stores the results (new position of the ending plane after
        deformation) for generalized plane strain. All outputs are in the
        global Cartesian coordinate system. For more information about the
        generalized plane strain feature, see Generalized Plane Strain Option
        of Current-Technology Solid Elements in the Element Reference.
        """
        command = f"GSSOL,{nvar},{item},{comp},{name}"
        return self.run(command, **kwargs)

    def jsol(self, nvar="", elem="", item="", comp="", name="", **kwargs):
        """Specifies result items to be stored for the joint element.

        APDL Command: JSOL

        Parameters
        ----------
        nvar
            Arbitrary reference number or name assigned to this variable.
            Variable numbers can be 2 to NV (NUMVAR) while the name can be an
            eight-byte character string. Overwrites any existing results for
            this variable.

        elem
            Element number for which to store results.

        item
            Label identifying the item.  Valid item labels are shown in
            Table 202: JSOL - Valid Item and Component Labels below.

        comp
            Component of the Item (if required).  Valid component labels are
            shown in Table 202: JSOL - Valid Item and Component Labels below.

        name
            Thirty-two character name identifying the item on printouts and
            displays.  Defaults to a label formed by concatenating the first
            four characters of the Item and Comp labels.

        Notes
        -----
        This command is valid for the MPC184 joint elements. The values stored
        are for the free or unconstrained degrees of freedom of a joint
        element. Relative reaction forces and moments are available only if
        stiffness, damping, or friction is associated with the joint element.

        Table: 202:: : JSOL - Valid Item and Component Labels


        """
        command = f"JSOL,{nvar},{elem},{item},{comp},{name}"
        return self.run(command, **kwargs)

    def nsol(self, nvar="", node="", item="", comp="", name="", sector="", **kwargs):
        """Specifies nodal data to be stored from the results file.

        APDL Command: NSOL

        Parameters
        ----------
        nvar
            Arbitrary reference number or name assigned to this variable.
            Variable numbers can be 2 to NV (NUMVAR) while the name can be an
            eight byte character string. Overwrites any existing results for
            this variable.

        node
            Node for which data are to be stored.

        item
            Label identifying the item.  Valid item labels are shown in the
            table below.  Some items also require a component label.

        comp
            Component of the item (if required).  Valid component labels are
            shown in the table below.

        name
            Thirty-two character name identifying the item on printouts and
            displays.  Defaults to a label formed by concatenating the first
            four characters of the Item and Comp labels.

        sector
            For a full harmonic cyclic symmetry solution, the sector number for
            which the results from NODE are to be stored.

        Notes
        -----
        Stores nodal degree of freedom and solution results in a variable. For
        more information, see Data Interpreted in the Nodal Coordinate System
        in the Modeling and Meshing Guide.

        For SECTOR>1, the result is in the nodal coordinate system of the base
        sector, and it is rotated to the expanded sector’s location. Refer to
        Using the /CYCEXPAND Command in the Cyclic Symmetry Analysis Guide for
        more information.

        For SHELL131 and SHELL132 elements with KEYOPT(3) = 0 or 1, use the
        labels TBOT, TE2, TE3, . . ., TTOP instead of TEMP.
        """
        command = f"NSOL,{nvar},{node},{item},{comp},{name},{sector}"
        return self.run(command, **kwargs)

    def nstore(self, tinc="", **kwargs):
        """Defines which time points are to be stored.

        APDL Command: NSTORE

        Parameters
        ----------
        tinc
            Store data associated with every TINC time (or frequency) point(s),
            within the previously defined range of TMIN to TMAX [TIMERANGE].
            (Defaults to 1)

        Notes
        -----
        Defines which time (or frequency) points within the range are to be
        stored.
        """
        command = f"NSTORE,{tinc}"
        return self.run(command, **kwargs)

    def numvar(self, nv="", **kwargs):
        """Specifies the number of variables allowed in POST26.

        APDL Command: NUMVAR

        Parameters
        ----------
        nv
            Allow storage for NV variables.  200 maximum are allowed.  Defaults
            to 10 (except for an explicit dynamics analysis, which defaults to
            30).  TIME (variable 1) should also be included in this number.

        Notes
        -----
        Specifies the number of variables allowed for data read from the
        results file and for data resulting from an operation (if any).  For
        efficiency, NV should not be larger than necessary.  NV cannot be
        changed after data storage begins.
        """
        command = f"NUMVAR,{nv}"
        return self.run(command, **kwargs)

    def reset(self, **kwargs):
        """Resets all POST1 or POST26 specifications to initial defaults.

        APDL Command: RESET

        Notes
        -----
        Has the same effect as entering the processor the first time within the
        run.  In POST1, resets all specifications to initial defaults, erases
        all element table items, path table data, fatigue table data, and load
        case pointers.  In POST26, resets all specifications to initial
        defaults, erases all variables defined, and zeroes the data storage
        space.
        """
        command = f"RESET,"
        return self.run(command, **kwargs)

    def rforce(self, nvar="", node="", item="", comp="", name="", **kwargs):
        """Specifies the total reaction force data to be stored.

        APDL Command: RFORCE

        Parameters
        ----------
        nvar
            Arbitrary reference number assigned to this variable (2 to NV
            [NUMVAR]). Overwrites any existing results for this variable.

        node
            Node for which data are to be stored.  If NODE = P, graphical
            picking is enabled (valid only in the GUI).

        item
            Label identifying the item.  Valid item labels are shown in the
            table below.  Some items also require a component label.

        comp
            Component of the item (if required).  Valid component labels are
            shown in the table below.

        name
            Thirty-two character name identifying the item on printouts and
            displays. Defaults to an eight character label formed by
            concatenating the first four characters of the Item and Comp
            labels.

        Notes
        -----
        Defines the total reaction force data (static, damping, and inertial
        components) to be stored from single pass (ANTYPE,STATIC or TRANS)
        solutions or from the expansion pass of mode-superposition
        (ANTYPE,HARMIC or TRANS) solutions.

        Table: 228:: : RFORCE - Valid Item and Component Labels

        For SHELL131 and SHELL132 elements with KEYOPT(3) = 0 or 1, use the
        labels HBOT, HE2, HE3, . . ., HTOP instead of HEAT.
        """
        command = f"RFORCE,{nvar},{node},{item},{comp},{name}"
        return self.run(command, **kwargs)

    def rgb(
        self,
        kywrd="",
        pred="",
        pgrn="",
        pblu="",
        n1="",
        n2="",
        ninc="",
        ncntr="",
        **kwargs,
    ):
        """Specifies the RGB color values for indices and contours.

        APDL Command: /RGB

        Parameters
        ----------
        kywrd
            Determines how RGB modifications will be applied.

            INDEX - Specifies that subsequent color values apply to ANSYS color indices (0-15).

            CNTR - Specifies that subsequent color values apply to contours (1-128).  Applies to
                   C-option devices only (i.e. X11C or Win32C).

        pred
            Intensity of the color red, expressed as a percentage.

        pgrn
            Intensity of the color green, expressed as a percentage.

        pblu
            Intensity of the color blue, expressed as a percentage.

        n1
            First index (0-15), or contour (1-128) to which the designated RGB
            values apply.

        n2
            Final index (0-15), or contour (1-128) to which the designated RGB
            values apply.

        ninc
            The step increment between the values N1 and N2 determining which
            contours or indices will be controlled by the specified RGB values.

        ncntr
            The new maximum number of contours (1-128).

        Notes
        -----
        Issuing the /CMAP command (with no filename) will restore the default
        color settings.
        """
        command = f"/RGB,{kywrd},{pred},{pgrn},{pblu},{n1},{n2},{ninc},{ncntr}"
        return self.run(command, **kwargs)

    def solu(self, nvar="", item="", comp="", name="", **kwargs):
        """Specifies solution summary data per substep to be stored.

        APDL Command: SOLU

        Parameters
        ----------
        nvar
            Arbitrary reference number assigned to this variable (2 to NV
            [NUMVAR]).

        item
            Label identifying the item.  Valid item labels are shown in the
            table below.  Some items may also require a component label.

        comp
            Component of the item (if required).  Valid component labels are
            shown in the table below.  None are currently required.

        name
            Thirty-two character name identifying the item on printouts and
            displays.  Defaults to an eight character label formed by
            concatenating the first four characters of the Item and Comp
            labels.

        Notes
        -----
        See also the PRITER command of POST1 to display some of these items
        directly.  Valid for a static or full transient analysis. All other
        analyses have zeros for the data. Valid item and component labels for
        solution summary values are:
        """
        command = f"SOLU,{nvar},{item},{comp},{name}"
        return self.run(command, **kwargs)

    def store(self, lab="", npts="", **kwargs):
        """Stores data in the database for the defined variables.

        APDL Command: STORE

        Parameters
        ----------
        lab
            Valid labels:

            MERGE - Merge data from results file for the time points in memory with the existing
                    data using current specifications (default).

            NEW - Store a new set of data, replacing any previously stored data with current
                  result file specifications and deleting any previously-
                  calculated (OPER) variables. Variables defined using the
                  ANSOL command are also deleted.

            APPEN - Append data from results file to the existing data.

            ALLOC - Allocate (and zero) space for NPTS data points.

            PSD - Create a new set of frequency points for PSD calculations (replacing any
                  previously stored data and erasing any previously calculated
                  data).

        npts
            The number of time points (or frequency points) for storage (used
            only with Lab = ALLOC or PSD).  The value may be input when using
            POST26 with data supplied from other than a results file.  This
            value is automatically determined from the results file data with
            the NEW, APPEN, and MERGE options.  For the PSD option, NPTS
            determines the resolution of the frequency vector (valid numbers
            are between 1 and 10, defaults to 5).

        Notes
        -----
        This command stores data from the results file in the database for the
        defined variables [NSOL, ESOL, SOLU, JSOL] per specification [FORCE,
        LAYERP26, SHELL].  See the Basic Analysis Guide for more information.

        The STORE,PSD command will create a new frequency vector (variable 1)
        for response PSD calculations [RPSD].  This command should first be
        issued before defining variables [NSOL, ESOL, RFORCE] for which
        response PSD's are to be calculated.
        """
        command = f"STORE,{lab},{npts}"
        return self.run(command, **kwargs)

    def timerange(self, tmin="", tmax="", **kwargs):
        """Specifies the time range for which data are to be stored.

        APDL Command: TIMERANGE

        Parameters
        ----------
        tmin
            Minimum time (defaults to first time (or frequency) point on the
            file).

        tmax
            Maximum time (defaults to last time (or frequency) point on the
            file).

        Notes
        -----
        Defines the time (or frequency) range for which data are to be read
        from the file and stored in memory.  Use the NSTORE command to define
        the time increment.

        Use PRTIME or PLTIME to specify the time (frequency) range for cyclic
        mode-superposition harmonic analyses.
        """
        command = f"TIMERANGE,{tmin},{tmax}"
        return self.run(command, **kwargs)

    def vardel(self, nvar="", **kwargs):
        """Deletes a variable (GUI).

        APDL Command: VARDEL

        Parameters
        ----------
        nvar
            The reference number of the variable to be deleted.  NVAR is as
            defined by NSOL, ESOL, etc.

        Notes
        -----
        Deletes a POST26 solution results variable.  This is a command
        generated by the Graphical User Interface (GUI).  It will appear in the
        log file (Jobname.LOG) if a POST26 variable is deleted from the
        "Defined Time-History Variables" dialog box.  This command is not
        intended to be typed in directly in an ANSYS session (although it can
        be included in an input file for batch input or for use with the /INPUT
        command).
        """
        command = f"VARDEL,{nvar}"
        return self.run(command, **kwargs)

    def varnam(self, ir="", name="", **kwargs):
        """Names (or renames) a variable.

        APDL Command: VARNAM

        Parameters
        ----------
        ir
            Reference number of the variable (2 to NV [NUMVAR]).

        name
            Thirty-two character name for identifying variable on printouts and
            displays.  Embedded blanks are compressed for output.
        """
        command = f"VARNAM,{ir},{name}"
        return self.run(command, **kwargs)
