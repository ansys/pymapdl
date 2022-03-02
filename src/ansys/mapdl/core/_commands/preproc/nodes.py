import re

from ansys.mapdl.core._commands import parse


class Nodes:
    def center(self, node="", node1="", node2="", node3="", radius="", **kwargs):
        """Defines a node at the center of curvature of 2 or 3 nodes.

        APDL Command: CENTER

        Parameters
        ----------
        node
            Number to be assigned to the node generated at the center of
            curvature.

        node1, node2, node3
            Three nodes used to calculated the center of curvature, as
            described under RADIUS.

        radius
            Used to control the interpretation of NODE1, NODE2 and NODE3:

            0 - NODE1, NODE2 and NODE3 lie on a circular arc.  The program will calculate the
                center of curvature (and radius) (default).

            ≠0 - NODE1 and NODE2 are the endpoints of an arc, and RADIUS is the radius of
                 curvature.  The program will locate the center of curvature on
                 the NODE3 side of the NODE1-NODE2 line if RADIUS > 0, and
                 opposite to NODE3 if RADIUS < 0.
        """
        command = f"CENTER,{node},{node1},{node2},{node3},{radius}"
        return self.run(command, **kwargs)

    def fill(
        self,
        node1="",
        node2="",
        nfill="",
        nstrt="",
        ninc="",
        itime="",
        inc="",
        space="",
        **kwargs,
    ):
        """Generates a line of nodes between two existing nodes.

        APDL Command: FILL

        Parameters
        ----------
        node1, node2
            Beginning and ending nodes for fill-in.  NODE1 defaults to next to
            last node specified, NODE2 defaults to last node specified.  If
            NODE1 = P, graphical picking is enabled and all remaining command
            fields are ignored (valid only in the GUI).

        nfill
            Fill NFILL nodes between NODE1 and NODE2 (defaults to
            ``|NODE2-NODE1|-1``).  NFILL must be positive.

        nstrt
            Node number assigned to first filled-in node (defaults to ``NODE1 +
            NINC``).

        ninc
            Add this increment to each of the remaining filled-in node numbers
            (may be positive or negative).  Defaults to the integer result of
            ``(NODE2-NODE1)/(NFILL + 1)``, i.e., linear interpolation.  If the
            default evaluates to zero, or if zero is input, NINC is set to 1.

        itime, inc
            Do fill-in operation a total of ITIMEs, incrementing NODE1, NODE2
            and NSTRT by INC each time after the first.  ITIME and INC both
            default to 1.

        space
            Spacing ratio.  Ratio of last division size to first division size.
            If > 1.0, divisions increase.  If < 1.0, divisions decrease.  Ratio
            defaults to 1.0 (uniform spacing).

        Notes
        -----
        Generates a line of nodes (in the active coordinate system) between two
        existing nodes.  The two nodes may have been defined in any coordinate
        system.  Nodal locations and rotation angles are determined by
        interpolation.  Any number of nodes may be filled-in and any node
        number sequence may be assigned.  See the CSCIR command when filling
        across the 180° singularity line in a non-Cartesian system.
        """
        command = f"FILL,{node1},{node2},{nfill},{nstrt},{ninc},{itime},{inc},{space}"
        return self.run(command, **kwargs)

    def move(
        self,
        node="",
        kc1="",
        x1="",
        y1="",
        z1="",
        kc2="",
        x2="",
        y2="",
        z2="",
        **kwargs,
    ):
        """Calculates and moves a node to an intersection.

        APDL Command: MOVE

        Parameters
        ----------
        node
            Move this node.  If NODE = P, graphical picking is enabled and all
            remaining command fields are ignored (valid only in the GUI).  A
            component name may also be substituted for NODE.

        kc1
            First coordinate system number.  Defaults to 0 (global Cartesian).

        x1, y1, z1
            Input one or two values defining the location of the node in this
            coordinate system.  Input "U" for unknown value(s) to be calculated
            and input "E" to use an existing coordinate value.  Fields are R1,
            θ1, Z1 for cylindrical, or R1, θ1, Φ1 for spherical or toroidal.

        kc2
            Second coordinate system number.

        x2, y2, z2
            Input two or one value(s) defining the location of the node in this
            coordinate system.  Input "U" for unknown value(s) to be calculated
            and input "E" to use an existing coordinate value.  Fields are R2,
            θ2, Z2 for cylindrical, or R2,  θ2, Φ2 for spherical or toroidal.

        Notes
        -----
        Calculates and moves a node to an intersection location.  The node may
        have been previously defined (at an approximate location) or left
        undefined (in which case it is internally defined at the SOURCE
        location).  The actual location is calculated from the intersection of
        three surfaces (implied from three coordinate constants in two
        different coordinate systems).  The three (of six) constants easiest to
        define should be used.  The program will calculate the remaining three
        coordinate constants.  All arguments, except KC1, must be input.  Use
        the repeat command [``*REPEAT``] after the MOVE command to define a line of
        intersection by repeating the move operation on all nodes of the line.

        Surfaces of constant value are implied by some commands by specifying a
        single coordinate value.  Implied surfaces are used with various
        commands [MOVE, KMOVE, NSEL, etc.].  Three surfaces are available with
        each of the four coordinate system types.  Values or X, Y, or Z may be
        constant for the Cartesian coordinate system; values of R,: θ, or Z for
        the cylindrical system; and values of R, θ,: Φ for the spherical and
        toroidal systems.  For example, an X value of 3 represents the Y-Z
        plane (or surface) at X=3.  In addition, the parameters for the
        cylindrical and spherical coordinate systems may be adjusted [CS,
        LOCAL] to form elliptical surfaces.  For surfaces in elliptical
        coordinate systems, a surface of "constant" radius is defined by the
        radius value at the X-axis.  Surfaces of constant value may be located
        in local coordinate systems [LOCAL, CLOCAL, CS, or CSKP] to allow for
        any orientation.

        The intersection calculation is based on an iterative procedure (250
        iterations maximum) and a tolerance of 1.0E-4.  The approximate
        location of a node should be sufficient to determine a unique
        intersection if more than one intersection point is possible.  Tangent
        "intersections" should be avoided.  If an intersection is not found,
        the node is placed at the last iteration location.

        This command is also valid in the /MAP processor.
        """
        command = f"MOVE,{node},{kc1},{x1},{y1},{z1},{kc2},{x2},{y2},{z2}"
        return self.run(command, **kwargs)

    def n(self, node="", x="", y="", z="", thxy="", thyz="", thzx="", **kwargs) -> int:
        """Define a node.

        APDL Command: N

        Defines a node in the active coordinate system [CSYS].  The
        nodal coordinate system is parallel to the global Cartesian
        system unless rotated.  Rotation angles are in degrees and
        redefine any previous rotation angles.  See the NMODIF, NANG,
        NROTAT, and NORA commands for other rotation options.

        Parameters
        ----------
        node
            Node number to be assigned.  A previously defined node of
            the same number will be redefined.  Defaults to the
            maximum node number used +1.

        x, y, z
            Node location in the active coordinate system (R, θ, Z for
            cylindrical, R, θ, Φ for spherical or toroidal).

        thxy
            First rotation about nodal Z (positive X toward Y).

        thyz
            Second rotation about nodal X (positive Y toward Z).

        thzx
            Third rotation about nodal Y (positive Z toward X).

        Returns
        -------
        int
            Node number of the generated node.

        Examples
        --------
        Create a node at ``(0, 1, 1)``

        >>> nnum = mapdl.n("", 0, 1, 1)
        >>> nnum
        1

        Create a node at ``(4, 5, 1)`` with a node ID of 10

        >>> nnum = mapdl.n(10, 4, 5, 1)
        >>> nnum
        10

        """
        command = f"N,{node},{x},{y},{z},{thxy},{thyz},{thzx}"
        msg = self.run(command, **kwargs)
        if msg:
            res = re.search(r"(NODE\s*)([0-9]+)", msg)
            if res is not None:
                return int(res.group(2))

    def naxis(self, action="", val="", **kwargs):
        """Generates nodes for general axisymmetric element sections.

        APDL Command: NAXIS

        Parameters
        ----------
        action
            Specifies one of the following command behaviors:

            GEN - Generates nodes around the axis of an axisymmetric section (default).

            CLEAR - Clears all nodes around the axis of an axisymmetric section.

            EFACET - Specifies the number of facets per edge between nodal planes and integration
                     planes in the circumferential direction to display using
                     PowerGraphics.  This option is only valid with /ESHAPE,1
                     and RSYS,SOLU commands.

        val
            Tolerance value or number of facets per edge:

            TOLER - When Action = GEN, the tolerance to use for merging the generated nodes around
                    the axis.

            NUM - When Action = EFACET, the number of facets per element edge for element plots:

            AUTO - Use program-chosen facets per edge (default).

            1 - Use 1 facet per edge (default for elements with 9, 10, 11, or 12 nodal planes).
                Shows nodal and integration planes only.

            2 - Use 2 facets per edge (default for elements with 5, 6, 7, or 8 nodal planes,
                and maximum for elements with 9, 10, 11, or 12 nodal planes).

            3 - Use 3 facets per edge (default for elements with 3 or 4 nodal planes, and
                maximum for elements with 6, 7, or 8 nodal planes).

            4 - Use 4 facets per edge (maximum for elements with 5 nodal planes).

            5 - Use 5 facets per edge (maximum for elements with 4 nodal planes).

            6 - Use 6 facets per edge (maximum for elements with 3 nodal planes).

        Notes
        -----
        The NAXIS command generates or clears the nodes for general
        axisymmetric element sections. The command applies to elements SURF159,
        SOLID272, and SOLID273.

        The generate option (Action = GEN) operates automatically on any
        current-technology axisymmetric element. Any nodes within the tolerance
        value (TOLER) of the axis are merged into a single node. The default
        tolerance is 1.0e-4.

        If you want to change the number of nodes, use the clear option (Action
        = CLEAR) before regenerating the nodes.

        To cause the 3-D element plot to appear more like the actual 3-D model,
        use NAXIS,EFACET,NUM, where NUM > 1. In this case, the coordinate
        system specified for displaying element and nodal results (RSYS) must
        be solution (RSYS,SOLU); otherwise, ANSYS resets NUM to 1.
        """
        command = f"NAXIS,{action},{val}"
        return self.run(command, **kwargs)

    def nang(
        self,
        node="",
        x1="",
        x2="",
        x3="",
        y1="",
        y2="",
        y3="",
        z1="",
        z2="",
        z3="",
        **kwargs,
    ):
        """Rotates a nodal coordinate system by direction cosines.

        APDL Command: NANG

        Parameters
        ----------
        node
            Rotate coordinate system of this node.

        x1, x2, x3
            Global X, Y, Z components of a unit vector in new nodal X
            direction.

        y1, y2, y3
            Global X, Y, Z components of a unit vector in new nodal Y
            direction.

        z1, z2, z3
            Global X, Y, Z components of a unit vector in new nodal Z
            direction.

        Notes
        -----
        Rotates a nodal coordinate system to the orientation specified by the
        X, Y and Z direction cosines.  Existing rotation specifications on the
        node are redefined.  If only two of the three unit vectors are
        specified, the third is defined according to the right hand rule.  It
        is the responsibility of the user to ensure that input direction
        cosines are orthogonal in a right-handed system.

        See the NMODIF, NROTAT, and NORA commands for other rotation options.
        """
        command = f"NANG,{node},{x1},{x2},{x3},{y1},{y2},{y3},{z1},{z2},{z3}"
        return self.run(command, **kwargs)

    def ndele(self, node1="", node2="", ninc="", **kwargs):
        """Deletes nodes.

        APDL Command: NDELE

        Parameters
        ----------
        node1, node2, ninc
            Delete nodes from NODE1 to NODE2 (defaults to NODE1) in steps of
            NINC (defaults to 1).  If NODE1 = ALL, NODE2 and NINC are ignored
            and all selected nodes [NSEL] are deleted.  If NODE1 = P, graphical
            picking is enabled and all remaining command fields are ignored
            (valid only in the GUI).  A component name may also be substituted
            for NODE1.

        Notes
        -----
        Deletes selected nodes that are not connected to elements.  Nodes may
        also be redefined instead of deleted, if desired.  Boundary conditions
        (displacements, forces, etc.) as well as any coupling or constraint
        equations containing the deleted nodes are also deleted.

        This command is also valid in the /MAP processor.
        """
        command = f"NDELE,{node1},{node2},{ninc}"
        return self.run(command, **kwargs)

    def ndist(self, nd1="", nd2="", **kwargs):
        """Calculates and lists the distance between two nodes.

        APDL Command: NDIST

        Parameters
        ----------
        nd1
            First node in distance calculation.  If ND1 = P, graphical picking
            is enabled and all remaining command fields are ignored (valid only
            in the GUI).
        nd2
            Second node in distance calculation.

        Returns
        -------
        list
            ``[DIST, X, Y, Z]`` distance between two nodes.

        Notes
        -----
        NDIST lists the distance between nodes ND1 and ND2, as well as the
        current coordinate system offsets from ND1 to ND2, where the X, Y, and
        Z locations of ND1 are subtracted from the X, Y, and Z locations of ND2
        (respectively) to determine the offsets.  NDIST is valid in any
        coordinate system except toroidal [CSYS,3].
        NDIST returns a variable, called "_RETURN," which contains the distance
        value. You can use this value for various purposes, such as the
        calculation of distributed loads. In interactive mode, you can access
        this command by using the Model Query Picker (Utility Menu> List>
        Picked Entities), where you can also access automatic annotation
        functions and display the value on your model.
        This command is valid in any processor.

        Examples
        --------
        Compute the distance between two nodes.

        >>> node1 = (0, 8, -3)
        >>> node2 = (13, 5, 7)
        >>> node_num1 = mapdl.n("", *node1)
        >>> node_num2 = mapdl.n("", *node2)
        >>> node_dist = mapdl.ndist(node_num1, node_num2)
        >>> node_dist
        [16.673332000533065, 13.0, -3.0, 10.0]

        """

        return parse.parse_ndist(self.run(f"NDIST,{nd1},{nd2}", **kwargs))

    def ngen(
        self,
        itime="",
        inc="",
        node1="",
        node2="",
        ninc="",
        dx="",
        dy="",
        dz="",
        space="",
        **kwargs,
    ):
        """Generates additional nodes from a pattern of nodes.

        APDL Command: NGEN

        Parameters
        ----------
        itime, inc
            Do this generation operation a total of ITIME times, incrementing
            all nodes in the given pattern by INC each time after the first.
            ITIME must be > 1 for generation to occur.

        node1, node2, ninc
            Generate nodes from the pattern of nodes beginning with NODE1 to
            NODE2 (defaults to NODE1) in steps of NINC (defaults to 1).  If
            NODE1 = ALL, NODE2 and NINC are ignored and the pattern is all
            selected nodes [NSEL].  If NODE1 = P, graphical picking is enabled
            and all remaining command fields are ignored (valid only in the
            GUI).  A component name may also be substituted for NODE1 (NODE2
            and NINC are ignored).

        dx, dy, dz
            Node location increments in the active coordinate system (DR, Dθ,
            DZ for cylindrical, DR, Dθ, DΦ for spherical or toroidal).

        space
            Spacing ratio.  Ratio of last division size to first division size.
            If > 1.0, divisions increase.  If < 1.0, divisions decrease.  Ratio
            defaults to 1.0 (uniform spacing).

        Notes
        -----
        Generates additional nodes from a given node pattern.  Generation is
        done in the active coordinate system.  Nodes in the pattern may have
        been generated in any coordinate system.

        This command is also valid in the /MAP processor.
        """
        command = f"NGEN,{itime},{inc},{node1},{node2},{ninc},{dx},{dy},{dz},{space}"
        return self.run(command, **kwargs)

    def nkpt(self, node="", npt="", **kwargs):
        """Defines a node at an existing keypoint location.

        APDL Command: NKPT

        Parameters
        ----------
        node
            Arbitrary reference number for node.  If zero or blank, defaults to
            the highest node number +1 [NUMSTR].

        npt
            Keypoint number defining global X, Y, Z  location.  If NPT = All,
            then a node will be placed at each selected keypoint.  If NPT = P,
            graphical picking is enabled and all remaining command fields are
            ignored (valid only in the GUI).  A component name may also be
            substituted for NPT.
        """
        command = f"NKPT,{node},{npt}"
        return self.run(command, **kwargs)

    def nlist(
        self,
        node1="",
        node2="",
        ninc="",
        lcoord="",
        sort1="",
        sort2="",
        sort3="",
        kinternal="",
        **kwargs,
    ):
        """Lists nodes.

        APDL Command: NLIST

        Parameters
        ----------
        node1, node2, ninc
            List nodes from NODE1 to NODE2 (defaults to NODE1) in steps of NINC
            (defaults to 1).  If NODE1 = ALL (default), NODE2 and NINC are
            ignored and all selected nodes [NSEL] are listed.  If NODE1 = P,
            graphical picking is enabled and all remaining command fields are
            ignored (valid only in the GUI).  A component name may also be
            substituted for NODE1 (NODE2 and NINC are ignored).

        lcoord
            Coordinate listing key:

            (blank) - List all nodal information

            COORD - Suppress all but the XYZ coordinates (shown to a higher degree of accuracy than
                    when displayed with all information).

        sort1
            First item on which to sort.  Valid item names are NODE, X, Y, Z,
            THXY, THYZ, THXZ

        sort2, sort3
            Second and third items on which to sort.  Valid item names are the
            same as for SORT1.

        kinternal
            Internal nodes listing key:

            (blank) - List only external nodes.

            INTERNAL - List all nodes, including internal nodes.

        Notes
        -----
        Lists nodes in the active display coordinate system [DSYS].  Nodal
        coordinate rotation angles are also listed (relative to the global
        Cartesian coordinate system).

        Node listing can be in a sorted order (ascending).  SORT2, for example,
        will be carried out on nodes having equal values of SORT1.

        This command is valid in any processor.
        """
        command = (
            f"NLIST,{node1},{node2},{ninc},{lcoord},{sort1},{sort2},{sort3},{kinternal}"
        )
        return self.run(command, **kwargs)

    def nmodif(self, node="", x="", y="", z="", thxy="", thyz="", thzx="", **kwargs):
        """Modifies an existing node.

        APDL Command: NMODIF

        Parameters
        ----------
        node
            Modify coordinates of this node.  If ALL, modify coordinates of all
            selected nodes [NSEL].  If NODE = P, graphical picking is enabled
            and all remaining command fields are ignored (valid only in the
            GUI).  A component name may also be substituted for NODE.

        x, y, z
            Replace the previous coordinate values assigned to this node with
            these corresponding coordinate values.  Values are interpreted in
            the active coordinate system (R, θ, Z for cylindrical; R, θ, Φ for
            spherical or toroidal).  Leaving any of these fields blank retains
            the previous value(s).

        thxy
            First rotation of nodal coordinate system about nodal Z (positive X
            toward Y). Leaving this field blank retains the previous value.

        thyz
            Second rotation of nodal coordinate system about nodal X (positive
            Y toward Z). Leaving this field blank retains the previous value.

        thzx
            Third rotation of nodal coordinate system about nodal Y (positive Z
            toward X). Leaving this field blank retains the previous value.

        Notes
        -----
        Modifies an existing node.  Nodal coordinate system rotation angles are
        in degrees and redefine any existing rotation angles.  Nodes can also
        be redefined with the N command.

        See the NROTAT, NANG, and NORA commands for other rotation options.

        This command is also valid in the /MAP processor.
        """
        command = f"NMODIF,{node},{x},{y},{z},{thxy},{thyz},{thzx}"
        return self.run(command, **kwargs)

    def nora(self, area="", ndir="", **kwargs):
        """Rotates nodal coordinate systems to surface normal

        APDL Command: NORA

        Parameters
        ----------
        area
            The area number containing the nodes to be rotated to their
            normals. If ALL, applies to all selected areas (see the ASEL
            command). If AREA = P, graphical picking is enabled.

        ndir
            Direction of the normal. If NDIR = -1, the nodal coordinate system
            is rotated in the opposite direction of the surface normal. The
            default is the same direction as the surface normal.

        Notes
        -----
        The NORA command rotates the X-axis of the nodal coordinate system to
        the surface normal. The rotated nodal coordinate systems may be
        displayed through the /PSYMB command. In case multiple areas are
        selected, there could be conflicts at the boundaries. If a node belongs
        to two areas that have a different normal, its nodal coordinate system
        will be rotated to the area normal with the lowest number. You can use
        the AREVERSE and ANORM commands to rotate the surface normals in the
        appropriate direction. Keep the following in mind when using the NORA
        command:

        If the nodal coordinate system is parallel to the global Cartesian
        system, it is not displayed through the /PSYMB command.

        Previously specified rotation on the selected nodes are overridden.
        """
        command = f"NORA,{area},{ndir}"
        return self.run(command, **kwargs)

    def norl(self, line="", area="", ndir="", **kwargs):
        """APDL Command: NORL

        Rotates nodal coordinate systems perpendicular to line normal

        Parameters
        ----------
        line
            Line number containing the nodes to be rotated. If ALL, applies to
            all selected lines (see the LSEL command). If LINE = P, graphical
            picking is enabled.

        area
            The area number containing the selected lines. The normal of the
            line(s) selected is supposed to lie on this area. Defaults to the
            lowest numbered selected area containing the line number.

        ndir
            Direction of the normal. If NDIR = -1, the nodal coordinate system
            is rotated in the opposite direction of the line normal. The
            default is the same direction as the surface normal.

        Notes
        -----
        The NORL command rotates the X-axis of the nodal coordinate
        perpendicular to the line normal. The rotated nodal coordinate systems
        may be displayed through the /PSYMB command. In case multiple lines are
        selected, there could be conflicts at the boundaries. If a node belongs
        to two lines that have a different normal, its nodal coordinate system
        will be rotated to the line normal with the lowest number. Keep the
        following in mind when using the NORL command:

        If the nodal coordinate system is parallel to the global Cartesian
        system, it is not displayed through the /PSYMB command.

        Previously specified rotation on the selected nodes are overridden.
        """
        command = f"NORL,{line},{area},{ndir}"
        return self.run(command, **kwargs)

    def nplot(self, knum="", **kwargs):
        """Displays nodes.

        APDL Command: NPLOT

        Parameters
        ----------
        knum
            Node number key:

            0 - No node numbers on display.

            1 - Include node numbers on display.  See also /PNUM command.

        Notes
        -----
        Produces a node display.  Only selected nodes [NSEL] are displayed.
        Elements need not be defined.  See the DSYS command for display
        coordinate system.

        This command is valid in any processor.
        """
        command = f"NPLOT,{knum}"
        return self.run(command, **kwargs)

    def nread(self, fname="", ext="", **kwargs):
        """Reads nodes from a file.

        APDL Command: NREAD

        Parameters
        ----------
        fname
            File name and directory path (248 characters maximum, including the
            characters needed for the directory path).  An unspecified
            directory path defaults to the working directory; in this case, you
            can use all 248 characters for the file name.

        ext
            Filename extension (eight-character maximum).

        Notes
        -----
        The read operation is not necessary in a standard ANSYS run but is
        provided as a convenience to users wanting to read a coded node file,
        such as from another mesh generator or from a CAD/CAM program.  Data
        should be formatted as produced with the NWRITE command. Only nodes
        that are within the node range specified with the NRRANG command are
        read from the file.  Duplicate nodes already in the database will be
        overwritten.  The file is rewound before and after reading.  Reading
        continues until the end of the file.
        """
        command = f"NREAD,{fname},{ext}"
        return self.run(command, **kwargs)

    def nrotat(self, node1="", node2="", ninc="", **kwargs):
        """Rotates nodal coordinate systems into the active system.

        APDL Command: NROTAT

        Parameters
        ----------
        node1, node2, ninc
            Rotate nodes from NODE1 to NODE2 (defaults to NODE1) in steps of
            NINC (defaults to 1).  If NODE1 = ALL, NODE2 and NINC are ignored
            and all selected nodes [NSEL] are rotated.  If NODE1 = P, graphical
            picking is enabled and all remaining command fields are ignored
            (valid only in the GUI).  A component name may also be substituted
            for NODE1 (NODE2 and NINC are ignored).

        Notes
        -----
        Rotates nodal coordinate systems into the active coordinate system.
        Nodal coordinate systems may be automatically rotated into the active
        (global or local) coordinate system as follows:  Rotations in Cartesian
        systems will have nodal x directions rotated parallel to the Cartesian
        X direction.  Rotations in cylindrical, spherical or toroidal systems
        will have the nodal x directions rotated parallel to the R direction.
        Nodes at (or near) a zero radius location should not be rotated.  Nodal
        coordinate directions may be displayed [/PSYMB].  Nodal forces and
        constraints will also appear rotated when displayed if the nodal
        coordinate system is rotated.

        ANSYS LS-DYNA (explicit dynamics) does not support the NROTAT command.
        If you have rotated nodes in the implicit phase of an implicit-to-
        explicit sequential solution, you must rotate the nodes back to the
        global Cartesian direction before switching from implicit to explicit
        elements (ETCHG,ITE). Use the EDNROT command in the explicit run to
        maintain the same displacement constraints as were used on rotated
        nodes in the implicit run.

        Note:: : When the  nodal coordinate systems are defined, they remain
        parallel to the global Cartesian system unless subsequently rotated.

        Previously specified rotations on the specified nodes are overridden.

        See the NMODIF, NANG, and NORA commands for other rotation options.
        """
        command = f"NROTAT,{node1},{node2},{ninc}"
        return self.run(command, **kwargs)

    def nrrang(self, nmin="", nmax="", ninc="", **kwargs):
        """Specifies the range of nodes to be read from the node file.

        APDL Command: NRRANG

        Parameters
        ----------
        nmin, nmax, ninc
            Node range is defined from NMIN (defaults to 1) to NMAX (defaults
            to 99999999) in steps of NINC (defaults to 1).

        Notes
        -----
        Defines the range of nodes to be read [NREAD] from the node file.  Also
        implies an element range since only elements fully attached to these
        nodes will be read from the element file.
        """
        command = f"NRRANG,{nmin},{nmax},{ninc}"
        return self.run(command, **kwargs)

    def nscale(
        self, inc="", node1="", node2="", ninc="", rx="", ry="", rz="", **kwargs
    ):
        """Generates a scaled set of nodes from a pattern of nodes.

        APDL Command: NSCALE

        Parameters
        ----------
        inc
            Do this scaling operation one time, incrementing all nodes in the
            given pattern by INC.  If INC = 0, nodes will be redefined at the
            scaled locations.

        node1, node2, ninc
            Scale nodes from pattern of nodes beginning with NODE1 to NODE2
            (defaults to NODE1) in steps of NINC (defaults to 1).  If  NODE1 =
            ALL, NODE2 and NINC are ignored and pattern is all selected nodes
            [NSEL].  If NODE1 = P, graphical picking is enabled and all
            remaining command fields are ignored (valid only in the GUI).  A
            component name may also be substituted for NODE1 (NODE2 and NINC
            are ignored).

        rx, ry, rz
            Scale factor ratios.  Scaling is relative to the origin of the
            active coordinate system (RR, Rθ, RZ for cylindrical, RR, Rθ, RΦ
            for spherical or toroidal).  If absolute value of ratio > 1.0,
            pattern is enlarged.  If < 1.0, pattern is reduced.  Ratios default
            to 1.0 (each).

        Notes
        -----
        Generates a scaled pattern of nodes from a given node pattern.  Scaling
        is done in the active coordinate system.  Nodes in the pattern may have
        been generated in any coordinate system.

        This command is also valid in the /MAP processor.
        """
        command = f"NSCALE,{inc},{node1},{node2},{ninc},{rx},{ry},{rz}"
        return self.run(command, **kwargs)

    def nsmooth(self, npass="", **kwargs):
        """Smooths selected nodes among selected elements.

        APDL Command: NSMOOTH

        Parameters
        ----------
        npass
            Number of smoothing passes. Defaults to 3.

        Notes
        -----
        Repositions each selected node at the average position of its immediate
        neighbors on the selected elements. The node positions converge after
        some number of smoothing passes. For some initial conditions, NPASS may
        need to be much larger than 3. If the boundary of a mesh is to be
        undisturbed (usually desirable), the boundary nodes should be
        unselected before issuing NSMOOTH.
        """
        command = f"NSMOOTH,{npass}"
        return self.run(command, **kwargs)

    def nsym(self, ncomp="", inc="", node1="", node2="", ninc="", **kwargs):
        """Generates a reflected set of nodes.

        APDL Command: NSYM

        Parameters
        ----------
        ncomp
            Symmetry key:

            X - X (or R) symmetry (default).

            Y - Y (or θ) symmetry.

            Z - Z (or Φ) symmetry.

        inc
            Increment all nodes in the given pattern by INC to form the
            reflected node pattern.

        node1, node2, ninc
            Reflect nodes from pattern beginning with NODE1 to NODE2 (defaults
            to NODE1) in steps of NINC (defaults to 1).  If  NODE1 = ALL, NODE2
            and NINC are ignored and pattern is all selected nodes [NSEL].  If
            NODE1 = P, graphical picking is enabled and all remaining command
            fields are ignored (valid only in the GUI).  A component name may
            also be substituted for NODE1 (NODE2 and NINC are ignored).

        Notes
        -----
        Generates nodes from a given node pattern by a symmetry reflection.
        Reflection is done in the active coordinate system by changing a
        particular coordinate sign.  Nodes in the pattern may have been
        generated in any coordinate system.   Nodal rotation angles are not
        reflected.

        Symmetry reflection may be used with any node pattern, in any
        coordinate system, as many times as desired.  Reflection is
        accomplished by a coordinate sign change (in the active coordinate
        system).  For example, an X-reflection in a Cartesian coordinate system
        generates additional nodes from a given pattern, with a node increment
        added to each node number, and an X coordinate sign change.  An
        R-reflection in a cylindrical coordinate system gives a reflected
        "radial" location by changing the "equivalent" Cartesian (i.e., the
        Cartesian system with the same origin as the active cylindrical system)
        X and Y coordinate signs.  An R-reflection in a spherical coordinate
        system gives a reflected "radial" location by changing the equivalent
        Cartesian X, Y, and Z coordinate location signs.  Nodal coordinate
        system rotation angles are not reflected.
        """
        command = f"NSYM,{ncomp},{inc},{node1},{node2},{ninc}"
        return self.run(command, **kwargs)

    def nwrite(self, fname="", ext="", kappnd="", **kwargs):
        """Writes nodes to a file.

        APDL Command: NWRITE

        Parameters
        ----------
        fname
            File name and directory path (248 characters maximum,
            including the characters needed for the directory path).
            An unspecified directory path defaults to the working
            directory; in this case, you can use all 248 characters
            for the file name.

        ext
            Filename extension (eight-character maximum).

        kappnd
            Append key:

            0 - Rewind file before the write operation.

            1 - Append data to the end of the existing file.

        Notes
        -----
        Writes selected nodes [NSEL] to a file.  The write operation
        is not necessary in a standard ANSYS run but is provided as a
        convenience to users wanting a coded node file.  Data are
        written in a coded format.  The format used is (I8, 6G20.13)
        to write out NODE,X,Y,Z,THXY,THYZ,THZX.  If the last number is
        zero (i.e., THZX = 0), or the last set of numbers are zero,
        they are not written but are left blank. Therefore, you must
        use a formatted read to process this file.  Coordinate values
        are in the global Cartesian system.
        """
        return self.run(f"NWRITE,{fname},{ext},,{kappnd}", **kwargs)

    def quad(
        self,
        node1="",
        nintr="",
        node2="",
        nfill="",
        nstrt="",
        ninc="",
        pkfac="",
        **kwargs,
    ):
        """Generates a quadratic line of nodes from three nodes.

        APDL Command: QUAD

        Parameters
        ----------
        node1
            Begin fill-in from this node location.  If NODE1 = P, graphical
            picking is enabled and all remaining command fields are ignored
            (valid only in the GUI).

        nintr
            Intermediate or guiding node.  Quadratic curve will pass through
            this location.  NINTR may have any node number and any location.
            If the quadratic line also generates a node with number NINTR, the
            generated location overrides the previous NINTR location.

        node2
            End quadratic fill-in at this node location.

        nfill
            Fill-in NFILL nodes between NODE1 and NODE2 (defaults to
            ``|NODE2-NODE1|-1``).  NFILL must be positive.

        nstrt
            Node number assigned to first filled-in node (defaults to NODE1 +
            NINC).

        ninc
            Add this increment to each of the remaining filled-in node numbers
            (may be positive or negative).  Defaults to ``(NODE2-NODE1)/(NFILL +
            1)``, i.e., linear interpolation.

        pkfac
            Peak location factor.  If PKFAC=0.5, the peak of the quadratic
            shape occurs at the NINTR location.  If 0.0 < PKFAC < 0.5, the peak
            occurs to the NODE2 side of the NINTR location.  If 0.5 < PKFAC <
            1.0, the peak occurs to the NODE1 side of the NINTR location.
            Defaults to 0.5.

        Notes
        -----
        Generates a quadratic line of nodes (in the active coordinate system)
        from three nodes.  The three nodes determine the plane of the curve and
        may have been defined in any coordinate system.  Any number of nodes
        may be filled-in and any node number sequence may be assigned.

        The quadratic line feature uses three nodes (NODE1,NINTR,NODE2) to
        determine the plane of the curve.  The curve passes through the three
        points, beginning from NODE1, through the intermediate (or guiding)
        point NINTR, and toward NODE2.

        Generated nodes are also quadratically spaced.  If the guiding node
        number is within the set being generated, it will be relocated
        according to the quadratic spacing.

        The peak location factor is used to determine how the quadratic fits
        through the three points.  Various nodal progressions can be obtained
        by different combinations of PKFAC and the guiding node location.  If
        the guiding node is at mid-length between NODE1 and NODE2, 0.293:
        PKFAC< 0.707 will ensure that all generated nodes fall within the
        NODE1,NODE2 bounds.  In the limit, as PKFAC approaches 0.0, the peak
        approaches the line through NODE1 and NINTR at an infinite distance
        from NODE1.  The QUAD command generates quadratic lines of nodes, which
        in turn may be used as a base line for generating irregular surfaces of
        nodes (by repeating [``*REPEAT``], generating [NGEN, NSCALE], etc.).
        Irregular surfaces may also be generated with the meshing commands.
        """
        command = f"QUAD,{node1},{nintr},{node2},{nfill},{nstrt},{ninc},{pkfac}"
        return self.run(command, **kwargs)

    def transfer(self, kcnto="", inc="", node1="", node2="", ninc="", **kwargs):
        """Transfers a pattern of nodes to another coordinate system.

        APDL Command: TRANSFER

        Parameters
        ----------
        kcnto
            Reference number of coordinate system where the pattern is to be
            transferred.  Transfer occurs from the active coordinate system.

        inc
            Increment all nodes in the given pattern by INC to form the
            transferred node pattern.

        node1, node2, ninc
            Transfer nodes from pattern beginning with NODE1 to NODE2 (defaults
            to NODE1) in steps of NINC (defaults to 1).  If NODE1 = ALL, NODE2
            and NINC are ignored and the pattern is all selected nodes [NSEL].
            If NODE1 = P, graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI).  A component
            may be substituted for NODE1 (NODE2 and NINC are ignored).

        Notes
        -----
        Transfers a pattern of nodes from one coordinate system to another.
        Coordinate systems may be translated and rotated relative to each
        other.  Initial pattern may be generated in any coordinate system.
        Coordinate values are interpreted in the active coordinate system and
        are transferred directly.

        A model generated in one coordinate system may be transferred to
        another coordinate system.  The user may define several coordinate
        systems (translated and rotated from each other), generate a model in
        one coordinate system, and then repeatedly transfer the model to other
        coordinate systems.  The model may be generated in any type of
        coordinate system (Cartesian, cylindrical, etc.) and transferred to any
        other type of coordinate system.  Coordinate values (X, Y, Z, or R,: θ,
        Z, or etc.) of the model being transferred are interpreted in the
        active coordinate system type, regardless of how they were generated.
        Values are transferred directly and are interpreted according to the
        type of coordinate system being transferred to.  For example,
        transferring from a Cartesian coordinate system to a cylindrical
        coordinate system (not recommended) would cause X = 2.0 and Y = 3.0
        values to be directly interpreted as R = 2.0 and θ = 3.0 values,
        respectively.

        This command is also valid in the /MAP processor.
        """
        command = f"TRANSFER,{kcnto},{inc},{node1},{node2},{ninc}"
        return self.run(command, **kwargs)
