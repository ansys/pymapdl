class PathOperations:
    def padele(self, delopt="", **kwargs):
        """Deletes a defined path.

        APDL Command: PADELE

        Parameters
        ----------
        delopt
            Path delete option (one of the following):

            ALL - Delete all defined paths.

            NAME - Delete a specific path from the list of path definitions.  (Substitute the
                   actual path name for NAME.)

        Notes
        -----
        Paths are identified by individual path names.  To review the current
        list of path names, issue the command PATH,STATUS.

        This command is valid in the general postprocessor.
        """
        command = f"PADELE,{delopt}"
        return self.run(command, **kwargs)

    def paget(self, parray="", popt="", **kwargs):
        """Writes current path information into an array variable.

        APDL Command: PAGET

        Parameters
        ----------
        parray
            The name of the array parameter that the ANSYS program creates to
            store the path information.  If the array parameter already exists,
            it will be replaced with the current path information.

        popt
            Determines how data will be stored in the parameter specified with
            PARRAY:

            POINTS - Store the path points, the nodes (if any), and coordinate system.  (For
                     information on defining paths and path points, see the
                     descriptions of the PATH and PPATH commands.)

            TABLE - Store the path data items.  (See the PDEF command description for path data
                    items.)

            LABEL - Stores path data labels.

        Notes
        -----
        Use the PAGET command together with the PAPUT command to store and
        retrieve path data in array variables for archiving purposes.  When
        retrieving path information, restore the path points (POINTS option)
        first, then the path data (TABLE option), and then the path labels
        (LABEL option).
        """
        command = f"PAGET,{parray},{popt}"
        return self.run(command, **kwargs)

    def paput(self, parray="", popt="", **kwargs):
        """Retrieves path information from an array variable.

        APDL Command: PAPUT

        Parameters
        ----------
        parray
            Name of the array variable containing the path information.

        popt
            Specifies which path data to retrieve:

            POINTS - Retrieve path point information (specified with the PPATH command and stored
                     with the PAGET,POINTS command).  The path data name will
                     be assigned to the path points.

            TABLE - Retrieve path data items (defined via the PDEF command and stored with the
                    PAGET,,TABLE command).

            LABEL - Retrieve path labels stored with the PAGET,,LABEL command.

        Notes
        -----
        When retrieving path information, restore path points (POINTS option)
        first, then the path data (TABLE option), and then the path labels
        (LABEL option).
        """
        command = f"PAPUT,{parray},{popt}"
        return self.run(command, **kwargs)

    def paresu(self, lab="", fname="", ext="", **kwargs):
        """Restores previously saved paths from a file.

        APDL Command: PARESU

        Parameters
        ----------
        lab
            Read operation:

            S - Saves only selected paths.

            ALL - Read all paths from the selected file (default).

            Pname - Saves the named path (from the PSEL command).

        fname
            File name and directory path (248 characters maximum,
            including the characters needed for the directory path).
            An unspecified directory path defaults to the working
            directory; in this case, you can use all 248 characters
            for the file name.

            The file name defaults to Jobname.

        ext
            Filename extension (eight-character maximum).  The
            extension defaults to PATH if Fname is blank.

        Notes
        -----
        This command removes all paths from virtual memory and then
        reads path data from a file written with the PASAVE command.
        All paths on the file will be restored.  All paths currently
        in memory will be deleted.
        """
        command = f"PARESU,{lab},{fname},{ext}"
        return self.run(command, **kwargs)

    def pasave(self, lab="", fname="", ext="", **kwargs):
        """Saves selected paths to an external file.

        APDL Command: PASAVE

        Parameters
        ----------
        lab
            Write operation:

            S - Saves only selected paths.

            ALL - Saves all paths (default).

            Pname - Saves the named path (from the PSEL command).

        fname
            File name and directory path (248 characters maximum, including the
            characters needed for the directory path).  An unspecified
            directory path defaults to the working directory; in this case, you
            can use all 248 characters for the file name.

        ext
            Filename extension (eight-character maximum).

        Notes
        -----
        Saves the paths selected with the PSEL command to an external file
        (Jobname.path by default).  Previous paths on this file, if any, will
        be overwritten.  The path file may be read with the PARESU command.

        This command is valid in POST1.
        """
        command = f"PASAVE,{lab},{fname},{ext}"
        return self.run(command, **kwargs)

    def path(self, name="", npts="", nsets="", ndiv="", **kwargs):
        """Defines a path name and establishes parameters for the path.

        APDL Command: PATH

        Parameters
        ----------
        name
            Name for this path (eight characters maximum. If nPts is blank, set
            the current path to the path with this name. If nPts is greater
            than zero, create a path of this name. If a path with this name
            already exists, replace it with a new path. If the NAME value is
            STATUS, display the status for path settings.

        npts
            The number of points used to define this path.  The minimum number
            is two, and the maximum is 1000. Default is 2.

        nsets
            The number of sets of data which you can map to this path.  You
            must specify at least four:  X, Y, Z, and S.  Default is 30.

        ndiv
            The number of divisions between adjacent points.  Default is 20.
            There is no maximum number of divisions.

        Notes
        -----
        The PATH command is used to define parameters for establishing a path.
        The path geometry is created by the PPATH command.  Multiple paths may
        be defined and named; however, only one path may be active for data
        interpolation [PDEF] and data operations [PCALC, etc.].  Path geometry
        points and data are stored in memory while in POST1.  If you leave
        POST1, the path information is erased.  Path geometry and data may be
        saved in a file by archiving the data using the PASAVE command.  Path
        information may be restored by retrieving the data using the PARESU
        command.

        For overlapping nodes, the lowest numbered node is assigned to the
        path.

        The number of divisions defined using nDiv does NOT affect the number
        of divisions used by PLSECT and PRSECT.

        For information on displaying paths you have defined, see  the Basic
        Analysis Guide.
        """
        command = f"PATH,{name},{npts},{nsets},{ndiv}"
        return self.run(command, **kwargs)

    def pcalc(
        self,
        oper="",
        labr="",
        lab1="",
        lab2="",
        fact1="",
        fact2="",
        const="",
        **kwargs,
    ):
        """Forms additional labeled path items by operating on existing path

        APDL Command: PCALC
        items.

        Parameters
        ----------
        oper
            Type of operation to be performed.  See "Notes" below for specific
            descriptions of each operation:

            ADD - Adds two existing path items.

            MULT - Multiplies two existing path items.

            DIV - Divides two existing path items (a divide by zero results in a value of zero).

            EXP - Exponentiates and adds existing path items.

            DERI - Finds a derivative.

            INTG - Finds an integral.

            SIN - Sine.

            COS - Cosine.

            ASIN - Arcsine.

            ACOS - Arccosine.

            LOG - Natural log.

        labr
            Label assigned to the resulting path item.

        lab1
            First labeled path item in operation.

        lab2
            Second labeled path item in operation.  Lab2 must not be blank for
            the MULT, DIV, DERI, and INTG operations.

        fact1
            Factor applied to Lab1. A (blank) or '0' entry defaults to 1.0.

        fact2
            Factor applied to Lab2. A (blank) or '0' entry defaults to 1.0.

        const
            Constant value (defaults to 0.0).

        Notes
        -----
        If Oper = ADD, the command format is:

        PCALC,ADD,LabR,Lab1,Lab2,FACT1,FACT2,CONST

        This operation adds two existing path items according to the operation:

        LabR = (FACT1   x Lab1) + (FACT2 x Lab2) + CONST

        It may be used to scale the results for a single path item.

        If Oper = MULT, the command format is:

        PCALC,MULT,LabR,Lab1,Lab2,FACT1

        Lab2 must not be blank.  This operation multiplies two existing path
        items according to the operation:

        LabR = Lab1 x Lab2 x FACT1

        If Oper = DIV, the command format is:

        PCALC,DIV,LabR,Lab1,Lab2,FACT1

        Lab2 must not be blank.  This operation divides two existing path items
        according to the operation:

        LabR = (Lab1/Lab2) x FACT1

        If Oper = EXP, the command format is:

        PCALC,EXP,LabR,Lab1,Lab2,FACT1,FACT2

        This operation exponentiates and adds existing path items according to
        the operation:

        ``LabR = (|Lab1|FACT1) + (|Lab2|FACT2|)``

        If Oper = DERI, the command format is:

        ``PCALC,DERI,LabR,Lab1,Lab2,FACT1``

        Lab2 must not be blank.  This operation finds a derivative according to
        the operation:

        ``LabR = FACT1 x d(Lab1)/d(Lab2)``

        If Oper = INTG, the command format is:

        ``PCALC,INTG,LabR,Lab1,Lab2,FACT1``

        Lab2 must not be blank.  This operation finds an integral according to
        the operation:

        Use S for Lab2 to integrate Lab1 with respect to the path length.  S,
        the distance along the path, is automatically calculated by the program
        when a path item is created with the PDEF command.

        If Oper = SIN, COS, ASIN, ACOS, or LOG, the command format is:

        ``PCALC,Oper,LabR,Lab1,,FACT1,CONST``

        where the function (SIN, COS, ASIN, ACOS or LOG) is substituted for
        Oper and Lab2 is blank.

        The operation finds the resulting path item according to one of the
        following formulas:

        ``LabR = FACT2 x sin(FACT1 x Lab1) + CONST``

        ``LabR = FACT2 x cos(FACT1 x Lab1) + CONST``

        ``LabR = FACT2 x sin-1(FACT1 x Lab1) + CONST``

        ``LabR = FACT2 x cos-1(FACT1 x Lab1) + CONST``

        ``LabR = FACT2 x log(FACT1 x Lab1) + CONST``
        """
        command = f"PCALC,{oper},{labr},{lab1},{lab2},{fact1},{fact2},{const}"
        return self.run(command, **kwargs)

    def pcross(
        self,
        labxr="",
        labyr="",
        labzr="",
        labx1="",
        laby1="",
        labz1="",
        labx2="",
        laby2="",
        labz2="",
        **kwargs,
    ):
        """Calculates the cross product of two path vectors along the current

        APDL Command: PCROSS
        path.

        Parameters
        ----------
        labxr
            Label assigned to X-component of resultant vector.

        labyr
            Label assigned to Y-component of resultant vector.

        labzr
            Label assigned to Z-component of resultant vector.

        labx1
            X-component of first vector label (labeled path item).

        laby1
            Y-component of first vector label.

        labz1
            Z-component of first vector label.

        labx2
            X-component of second vector label (labeled path item).

        laby2
            Y-component of second vector label.

        labz2
            Z-component of second vector label.
        """
        command = f"PCROSS,{labxr},{labyr},{labzr},{labx1},{laby1},{labz1},{labx2},{laby2},{labz2}"
        return self.run(command, **kwargs)

    def pdef(self, lab="", item="", comp="", avglab="", **kwargs):
        """Interpolates an item onto a path.

        APDL Command: PDEF

        Parameters
        ----------
        lab
            Label assigned to the resulting path item (8 characters maximum).
            This item may be used as input for other path operations.

        item
            Label identifying the item for interpolation.  Valid item labels
            are shown in Table 216: PDEF - valid Item and Component Labels
            below.  Some items also require a component label.

        comp
            Component of the item (if required).  Valid component labels are
            shown in Table 216: PDEF - valid Item and Component Labels below.

        avglab
            Option to average across element boundaries:

            AVG - Average element results across elements (default).

            NOAV - Do not average element results across elements.  If the parameter DISCON = MAT
                   on the PMAP command, this option is automatically invoked.

        Notes
        -----
        Defines and interpolates a labeled path item along a predefined path
        (PATH).  Path item results are in the global Cartesian coordinate
        directions unless transformed (RSYS).  A path item must be defined
        before it can be used with other path operations.  Additional path
        items may be defined from the PVECT, PCALC, PDOT, and PCROSS commands.
        Path items may be listed (PRPATH) or displayed (PLPATH, PLPAGM).  A
        maximum number of path items permitted is established by the nSets
        argument specified with the PATH command.

        When you create the first path item (PDEF or PVECT), the program
        automatically interpolates four path items which are used to describe
        the geometry of the path.  These predefined items are the position of
        the interpolated path points (labels XG, YG, and ZG) in global
        Cartesian coordinates, and the path length (label S).  For alternate
        methods of mapping the path geometry (to include, for example, material
        discontinuity) see the PMAP command.  These items may also be listed or
        displayed with the PRPATH, PLPATH, and PLPAGM commands.

        If specifying that load case operations act on principal/equivalent
        stresses (SUMTYPE,PRIN), derived quantities (principal and equivalent
        stresses/strains) will be zero for path plots. A typical use for such a
        case involves mode combinations in a response spectrum analysis.

        The number of interpolation points on the path is defined by the nDiv
        argument on the PATH command.  See Mapping Nodal and Element Data onto
        the Path in the Mechanical APDL Theory Reference for details.  Use
        PDEF,STAT to list the path item labels.  Use PDEF,CLEAR to erase all
        labeled path items, except the path geometry items (XG, YG, ZG, S).

        For SHELL131 and SHELL132 elements with KEYOPT(3) = 0 or 1, use the
        labels TBOT, TE2, TE3, ..., TTOP instead of TEMP.

        For more information on the meaning of contact status and its possible
        values, see Reviewing Results in POST1 in the Contact Technology Guide.
        """
        command = f"PDEF,{lab},{item},{comp},{avglab}"
        return self.run(command, **kwargs)

    def pdot(
        self,
        labr="",
        labx1="",
        laby1="",
        labz1="",
        labx2="",
        laby2="",
        labz2="",
        **kwargs,
    ):
        """Calculates the dot product of two path vectors along the current path.

        APDL Command: PDOT

        Parameters
        ----------
        labr
            Label assigned to dot product result.

        labx1
            X-component of first vector label (labeled path item).

        laby1
            Y-component of first vector label (labeled path item).

        labz1
            Z-component of first vector label (labeled path item).

        labx2
            X-component of second vector label (labeled path item).

        laby2
            Y-component of second vector label (labeled path item).

        labz2
            Z-component of second vector label (labeled path item).
        """
        command = f"PDOT,{labr},{labx1},{laby1},{labz1},{labx2},{laby2},{labz2}"
        return self.run(command, **kwargs)

    def plpagm(self, item="", gscale="", nopt="", **kwargs):
        """Displays path items along the path geometry.

        APDL Command: PLPAGM

        Parameters
        ----------
        item
            The path data item to be displayed on the currently active path
            (defined by the PATH command).  Valid path items are those defined
            with the PDEF or PLNEAR commands.

        gscale
            Scale factor for the offset from the path for the path data item
            displays.  Defaults to 1.0.

        nopt
            Determines how data is displayed:

            (blank) - Do not display nodes, and scale the display based on the currently selected
                      node set (default).

            NODE - Display path item data along with the currently selected set of nodes.  The
                   display geometry is scaled to the selected node set.

        Notes
        -----
        You can use the Gscale argument to scale the contour display offset
        from the path for clarity. You need to type all six characters to issue
        this command.
        """
        command = f"PLPAGM,{item},{gscale},{nopt}"
        return self.run(command, **kwargs)

    def plpath(self, lab1="", lab2="", lab3="", lab4="", lab5="", lab6="", **kwargs):
        """Displays path items on a graph.

        APDL Command: PLPATH

        Parameters
        ----------
        lab1, lab2, lab3, . . . , lab6
            Labels identifying the path items to be displayed.  Up to six items
            may be drawn per frame.  Predefined path geometry items XG, YG, ZG,
            and S [PDEF] may also be displayed.

        Notes
        -----
        The path must have been defined by the PATH and PPATH commands.  Path
        items and their labels must have been defined with the PDEF, PVECT,
        PCALC, PDOT, PCROSS, or PLNEAR commands.  Path items may also be
        printed with the PRPATH command.  Graph scaling may be controlled with
        the /XRANGE, /YRANGE, and PRANGE commands. You need to type all six
        characters to issue this command.
        """
        command = f"PLPATH,{lab1},{lab2},{lab3},{lab4},{lab5},{lab6}"
        return self.run(command, **kwargs)

    def plsect(self, item="", comp="", rho="", kbr="", **kwargs):
        """Displays membrane and membrane-plus-bending linearized stresses.

        APDL Command: PLSECT

        Parameters
        ----------
        item
            Label identifying the item to be processed.  Valid item labels are
            shown in Table 221: PLSECT - Valid Item and Component Labels below.
            Items also require a component label.

        comp
            Component of the item.  Valid component labels are shown in
            Table 221: PLSECT - Valid Item and Component Labels below.

        rho
            In-plane (X-Y) average radius of curvature of the inside and
            outside surfaces of an axisymmetric section.  If zero (or blank), a
            plane or 3-D structure is assumed.  If nonzero, an axisymmetric
            structure is assumed.  Use a very large number (or -1) for an
            axisymmetric straight section.

        kbr
            Through-thickness bending stresses key for an axisymmetric analysis
            (RHO ≠ 0):

            0 - Include the thickness-direction bending stresses.

            1 - Ignore the thickness-direction bending stresses.

            2 - Include the thickness-direction bending stress using the same formula as the Y
                (axial direction ) bending stress. Also use the same formula
                for the shear stress.

        Notes
        -----
        Calculates and displays the membrane and membrane-plus-bending
        linearized stresses (as described for the PRSECT command) along a path
        section [PATH] as a graph.  The path section is defined by two points
        specified with the PPATH command. For linearized stress calculations,
        the path must be defined with nodes. The path must be entirely within
        the selected elements (that is, there must not be any element gaps
        along the path). The total stress (equivalent to the PLPATH display) is
        also displayed.  This command always uses 48 divisions along the path,
        regardless of the number of divisions defined by PATH.

        Portions of this command are not supported by PowerGraphics
        [/GRAPHICS,POWER].

        Table: 221:: : PLSECT - Valid Item and Component Labels
        """
        command = f"PLSECT,{item},{comp},{rho},{kbr}"
        return self.run(command, **kwargs)

    def pmap(self, form="", discon="", **kwargs):
        """Creates mapping of the path geometry by defining path interpolation

        APDL Command: PMAP
        division points.

        Parameters
        ----------
        form
            Defines the mapping method:

            UNIFORM - Maps uniform divisions (specified on the nDiv argument of the PATH command)
                      between specified points.  This is the default.

            ACCURATE - Map geometry using a small division at the beginning and end of each segment.
                       This gives you accurate derivatives, integrals,
                       tangents, and normals for curves which do not have
                       continuous slopes at the specified points. To create
                       nonuniform divisions, the nDiv argument of the PATH
                       command must be greater than 2.

        discon
            Sets mapping for discontinuities in the field.  The divisions are
            modified to put a point just before and just after the
            discontinuity.  The valid label is MAT, for a material
            discontinuity.  No discontinuity is the default.  Discontinuity
            mapping involves the NOAV option on the PDEF command.
        """
        command = f"PMAP,{form},{discon}"
        return self.run(command, **kwargs)

    def ppath(self, point="", node="", x="", y="", z="", cs="", **kwargs):
        """Defines a path by picking or defining nodes, or locations on the

        APDL Command: PPATH
        currently active working plane, or by entering specific coordinate
        locations.

        Parameters
        ----------
        point
            The point number.  It must be greater than zero and less than or
            equal to the nPts value specified on the PATH command if graphical
            picking is not being used.

        node
            The node number defining this point.  If blank, use the X, Y, Z
            coordinates to define the point.  A valid node number will override
            X, Y, Z coordinate arguments.

        x, y, z
            The location of the point in the global Cartesian coordinate
            system.  Use these arguments only if you omit the NODE argument.

        cs
            The coordinate system for interpolation of the path between the
            previous point and this point.  Omit this argument if you wish to
            use the currently active (CSYS) coordinate system.  If the
            coordinate system of two adjacent points is different, the CS value
            of the latter point will be used.

        Notes
        -----
        For linearized stress calculations, the path must be defined with
        nodes.

        This command is designed and works best in interactive (GUI) mode,
        using the menu paths listed below. For command line operations, issue
        PPATH,P to define your path by picking nodes.

        For information on displaying paths you have defined, see Defining Data
        to be Retrieved in the Basic Analysis Guide.
        """
        command = f"PPATH,{point},{node},{x},{y},{z},{cs}"
        return self.run(command, **kwargs)

    def prange(self, linc="", vmin="", vmax="", xvar="", **kwargs):
        """Determines the path range.

        APDL Command: PRANGE

        Parameters
        ----------
        linc, vmin, vmax
            Set the range for listing or displaying the table locations between
            a minimum value (VMIN) and a maximum value (VMAX) of the path
            distance with a location increment of LINC (defaults to 1).  The
            first location begins at VMIN.

        xvar
            Path variable item to be used as the x-axis plot variable.  Any
            valid path variable may be used (PDEF command).  Default variable
            is the path distance, S.

        Notes
        -----
        Determines the path distance range for use with the PRPATH and PLPATH
        commands.
        """
        command = f"PRANGE,{linc},{vmin},{vmax},{xvar}"
        return self.run(command, **kwargs)

    def prpath(self, lab1="", lab2="", lab3="", lab4="", lab5="", lab6="", **kwargs):
        """Prints path items along a geometry path.

        APDL Command: PRPATH

        Parameters
        ----------
        lab1, lab2, lab3, . . . , lab6
            Labels identifying the path items to be printed.  Up to six items
            may be printed at a time.  Predefined path geometry items XG, YZ,
            ZG, and S [PDEF] may also be printed.

        Notes
        -----
        Prints path items with respect to a geometry path (as defined by the
        PATH  and PPATH commands).  Path items and their labels must have been
        defined with the PDEF, PVECT, PCALC, PDOT, PCROSS, or PRNEAR commands.
        Path items may also be displayed with the PLPATH and PLPAGM commands.
        See the PRANGE command for range control of the path.
        """
        command = f"PRPATH,{lab1},{lab2},{lab3},{lab4},{lab5},{lab6}"
        return self.run(command, **kwargs)

    def prsect(self, rho="", kbr="", **kwargs):
        """Calculates and prints linearized stresses along a section path.

        APDL Command: PRSECT

        Parameters
        ----------
        rho
            In-plane (X-Y) average radius of curvature of the inside and
            outside surfaces of an axisymmetric section.  If zero (or blank), a
            plane or 3-D structure is assumed.  If nonzero, an axisymmetric
            structure is assumed.  Use any large number (or -1) for an
            axisymmetric straight section.

        kbr
            Through-thickness bending stresses key for an axisymmetric analysis
            (RHO  ≠ 0):

            0 - Include the thickness-direction bending stresses.

            1 - Ignore the thickness-direction bending stresses.

            2 - Include the thickness-direction bending stress using the same formula as the Y
                (axial direction ) bending stress. Also use the same formula
                for the shear stress.

        Notes
        -----
        You may choose to linearize the stresses through a section and separate
        them into categories for various code calculations.  PRSECT calculates
        and reports linearized stresses along a section path.  The linearized
        stresses are also separated into membrane, bending, membrane plus
        bending, peak, and total stress categories.

        First, define your section path using the PATH and PPATH (with the NODE
        option) commands.  Your path must lie entirely within the selected set
        of elements (that is, there must be no element gaps along the path).
        PATH and PPATH are used only to retrieve the two end nodes.  The path
        data is not retained.  The section path is defined by the two end
        nodes, and by 47 intermediate points that are automatically determined
        by linear interpolation in the active display coordinate system [DSYS].
        The number and location of the intermediate points are not affected by
        the number of divisions set by PATH,,,,nDiv.

        Your  linearized component stress values are obtained by interpolating
        each element’s  average corner nodal values along the section path
        points within each path element.  PRSECT reports the linearized
        component and principal stresses for each stress category at the
        beginning, mid-length, and end of the section path.  PRPATH can be used
        to report the total stresses at the intermediate points.

        Section paths may be through any set of solid (2-D plane, 2-D
        axisymmetric or 3-D) elements.  However, section paths are usually
        defined to be through the thickness of the structure and normal to the
        inner and outer structure surfaces.  Section paths (in-plane only) may
        also be defined for shell element structures.  See the Mechanical APDL
        Theory Reference for details.

        If the RHO option is set to indicate the axisymmetric option (non-
        zero), PRSECT reports the linearized stresses in the section
        coordinates (SX – along the path, SY – normal to the path, and SZ –
        hoop direction).  If the RHO option is set to indicate the 2-D planar
        or 3-D option (zero or blank), PRSECT reports the linearized stresses
        in the active results coordinate system [RSYS].  If the RHO option is
        zero or blank and either RSYS, SOLU or RSYS, -1 are active, the
        linearized stresses are calculated and reported in the global Cartesian
        coordinate system.  It is recommended that linearized stress
        calculations be performed in a rectangular coordinate system.
        Principal stresses are recalculated from the component stresses and are
        invariant with the coordinate system as long as SX is in the same
        direction at all points along the defined path.  The PLSECT command
        displays the linearized stresses in the same coordinate system as
        reported by PRSECT.

        Stress components through the section are linearized by a line integral
        method and separated into constant membrane stresses, bending stresses
        varying linearly between end points, and peak stresses (defined as the
        difference between the actual (total) stress and the membrane plus
        bending combination).

        For nonaxisymmetric structures,  the bending stresses are calculated
        such that the neutral axis is at the midpoint of the path.
        Axisymmetric results include the effects of both the radius of
        revolution (automatically determined from the node locations) and the
        in-plane average radius of curvature of the section surfaces (user
        input).

        For axisymmetric cases, Mechanical APDL calculates the linearized
        bending stress in the through-thickness direction as the difference
        between the total outer fiber stress and the membrane stress if KBR =
        1. The calculation method may be conservative for locations with a
        highly nonlinear variation of stress in the through-thickness
        direction.  Alternatively, you can specify KBR = 2 to calculate the
        bending stress using the same method and formula as the Y (axial
        direction) bending stress. For more information, see the discussion of
        axisymmetric cases (specifically Equation: 17–40) in the Mechanical
        APDL Theory Reference.

        Portions of this command are not supported by PowerGraphics
        [/GRAPHICS,POWER].
        """
        command = f"PRSECT,{rho},{kbr}"
        return self.run(command, **kwargs)

    def psel(
        self,
        type_="",
        pname1="",
        pname2="",
        pname3="",
        pname4="",
        pname5="",
        pname6="",
        pname7="",
        pname8="",
        pname9="",
        pname10="",
        **kwargs,
    ):
        """Selects a path or paths.

        APDL Command: PSEL

        Parameters
        ----------
        type\_
            Label identifying the type of select:

            S - Select a new path.

            R - Reselect a path from the current set of paths.

            A - Additionally select a path and extend the current set of paths.

            U - Unselect a path from the current set of paths.

            ALL - Restore the full set of paths.

            NONE - Unselect the full set of paths.

            INV - Invert the current set of paths (selected becomes unselected and vice versa).

        pname1, pname2, pname3, . . . , pname10
            Name of existing path(s).

        Notes
        -----
        Selects a path or multiple paths, up to ten.  Data are flagged as
        selected and unselected; no data are actually deleted from the
        database.  There is no default for this command; you must specify a
        type and pathname.
        """
        command = f"PSEL,{type_},{pname1},{pname2},{pname3},{pname4},{pname5},{pname6},{pname7},{pname8},{pname9},{pname10}"
        return self.run(command, **kwargs)

    def pvect(self, oper="", labxr="", labyr="", labzr="", **kwargs):
        """Interpolates a set of items onto a path.

        APDL Command: PVECT

        Parameters
        ----------
        oper
            Valid operations for geometry operations along a path are:

            NORM - Defines a unit normal vector at each interpolation point in the direction of
                   the cross product of the tangent to the path and the active
                   Z axis.  Resulting vector components are in the active
                   coordinate system (which must be Cartesian).

            TANG - Defines a unit vector tangent to the path at each interpolation point.  Vector
                   components are in the active coordinate system (which must
                   be Cartesian).

            RADI - Defines the position vector of each interpolation point of the path from the
                   center of the active coordinate system (which must be
                   Cartesian).

        labxr
            Label (8 characters maximum) assigned to X-component of the
            resulting vector.

        labyr
            Label (8 characters maximum) assigned to Y-component of the
            resulting vector.

        labzr
            Label (8 characters maximum) assigned to Z-component of the
            resulting vector.

        Notes
        -----
        Defines and interpolates a set of labeled path items along predefined
        path [PATH] and performs various geometric operations on these path
        items.  A path item must be defined before it can be used with other
        path operations.  Additional path items may be defined with the PDEF,
        PCALC, PDOT, and PCROSS commands.  Path items may be listed or
        displayed with the PLPATH, PLPAGM and PRPATH commands.  Path geometry
        items (XG, YG, ZG, S) are automatically interpolated (in the active
        CSYS) if not done so previously with the PDEF command.
        """
        command = f"PVECT,{oper},{labxr},{labyr},{labzr}"
        return self.run(command, **kwargs)
