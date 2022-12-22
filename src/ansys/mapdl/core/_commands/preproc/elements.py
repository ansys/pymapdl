from typing import Optional, Union

from ansys.mapdl.core._commands.parse import parse_e
from ansys.mapdl.core.mapdl_types import MapdlFloat, MapdlInt


class Elements:
    def afsurf(self, sarea="", tline="", **kwargs):
        """Generates surface elements overlaid on the surface of existing solid elements.

        APDL Command: AFSURF

        This assigns extra nodes to the closest fluid element node.

        This command macro is used to generate surface effect elements overlaid
        on the surface of existing  solid elements and, based on proximity, to
        determine and assign the extra node for each surface element.  The
        underlying volumes of the solid region and the fluid lines must be
        meshed prior to calling this command macro. The active element type
        must be SURF152 with appropriate settings for KEYOPT(4), KEYOPT(5),
        KEYOPT(6), and KEYOPT(8).

        The surface areas of the solid and the target lines of the fluid are
        grouped into components and named using the CM command.  The names must
        be enclosed in single quotes (e.g., 'SAREA') when the AFSURF command is
        manually typed in.

        When using the GUI method, node and element components are created
        through the picking dialog boxes associated with this command.

        The macro is applicable for the SURF152 and FLUID116 element types.

        Parameters
        ----------
        sarea
            Component name for the surface areas of the meshed solid volumes.

        tline
            Component name for the target lines meshed with fluid elements.

        """
        command = f"AFSURF,{sarea},{tline}"
        return self.run(command, **kwargs)

    def e(
        self,
        i: MapdlInt = "",
        j: MapdlInt = "",
        k: MapdlInt = "",
        l: MapdlInt = "",
        m: MapdlInt = "",
        n: MapdlInt = "",
        o: MapdlInt = "",
        p: MapdlInt = "",
        **kwargs,
    ) -> Optional[int]:
        """Defines an element by node connectivity.

        APDL Command: E

        Defines an element by its nodes and attribute values. Up to 8
        nodes may be specified with the :meth:`e` command.  If more nodes
        are needed for the element, use the :meth:`emore` command. The
        number of nodes required and the order in which they should be
        specified are described in Chapter 4 of the Element Reference for
        each element type.  Elements are automatically assigned a number
        [NUMSTR] as generated. The current (or default) MAT, TYPE, REAL,
        SECNUM and ESYS attribute values are also assigned to the element.

        When creating elements with more than 8 nodes using this command
        and the EMORE command, it may be necessary to turn off shape
        checking using the SHPP command before issuing this command. If a
        valid element type can be created without using the additional
        nodes on the :meth:`emore` command, this command will create that
        element. The :meth:`emore` command will then modify the element to
        include the additional nodes. If shape checking is active, it will
        be performed before the :meth:`emore` command is issued.
        Therefore, if the shape checking limits are exceeded, element
        creation may fail before the :meth:`emore` command modifies the
        element into an acceptable shape.

        Parameters
        ----------
        i
            Number of node assigned to first nodal position (node
            ``i``).

        j, k, l, m, n, o, p
            Number assigned to second (node ``j``) through eighth
            (node ``p``) nodal position, if any.

        Examples
        --------
        Create a single SURF154 element.

        >>> mapdl.prep7()
        >>> mapdl.et(1, 'SURF154')
        >>> mapdl.n(1, 0, 0, 0)
        >>> mapdl.n(2, 1, 0, 0)
        >>> mapdl.n(3, 1, 1, 0)
        >>> mapdl.n(4, 0, 1, 0)
        >>> mapdl.e(1, 2, 3, 4)
        1

        Create a single hexahedral SOLID185 element

        >>> mapdl.et(2, 'SOLID185')
        >>> mapdl.type(2)
        >>> mapdl.n(5, 0, 0, 0)
        >>> mapdl.n(6, 1, 0, 0)
        >>> mapdl.n(7, 1, 1, 0)
        >>> mapdl.n(8, 0, 1, 0)
        >>> mapdl.n(9, 0, 0, 1)
        >>> mapdl.n(10, 1, 0, 1)
        >>> mapdl.n(11, 1, 1, 1)
        >>> mapdl.n(12, 0, 1, 1)
        >>> mapdl.e(5, 6, 7, 8, 9, 10, 11, 12)
        2

        """
        command = f"E,{i},{j},{k},{l},{m},{n},{o},{p}"
        return parse_e(self.run(command, **kwargs))

    def ecpchg(self, **kwargs):
        """Optimizes degree-of-freedom usage in a coupled acoustic model.

        APDL Command: ECPCHG

        The ECPCHG command converts uncoupled acoustic element types to
        coupled acoustic element types that are attached to the
        fluid-structure interaction interface. Or it converts coupled
        acoustic element types to uncoupled acoustic element types that
        are not attached to the fluid-structure interaction
        interface. Issuing ECPCHG can dramatically reduce the size of the
        Jobname.EMAT file, compared to the model fully meshed with the
        coupled acoustic elements.

        Performing the ECPCHG conversion on meshed volumes can create
        circumstances in which more than one element type is defined for a
        single volume.

        If the acoustic elements are coupled with shell elements (SHELL181
        or SHELL281), you must set the fluid-structure interaction (FSI)
        flag by issuing the SF,,FSI command before the ECPCHG command.

        ECPCHG may add new element types to your model, or it may change
        the element type for existing acoustic elements. You should verify
        the defined element types with ETLIST and the element attributes
        with ELIST after using this command.
        """
        return self.run("ECPCHG", **kwargs)

    def edele(
        self,
        iel1: MapdlInt = "",
        iel2: MapdlInt = "",
        inc: MapdlInt = "",
        **kwargs,
    ) -> Optional[str]:
        """Deletes selected elements from the model.

        APDL Command: EDELE

        Deleted elements are replaced by null or "blank"
        elements. Null elements are used only for retaining the
        element numbers so that the element numbering sequence for the
        rest of the model is not changed by deleting elements. Null
        elements may be removed (although this is not necessary) with
        the NUMCMP command. If related element data (pressures, etc.)
        are also to be deleted, delete that data before deleting the
        elements. EDELE is for unattached elements only. You can use
        the xCLEAR family of commands to remove any attached elements
        from the database.

        Parameters
        ----------
        iel1, iel2, inc
            Delete elements from ``iel1`` to ``iel2`` (defaults to
            ``iel1``) in steps of ``inc`` (defaults to 1). If
            ``iel1='ALL'``, ``iel2`` and ``inc`` are ignored and all
            selected elements [ESEL] are deleted.  A component name
            may also be substituted for ``iel1`` (``iel2`` and ``inc``
            are ignored).

        Examples
        --------
        Delete the elements 10 through 25

        >>> mapdl.edele(10, 25)
        'DELETE SELECTED ELEMENTS FROM         10 TO         25 BY          1'

        """
        return self.run(f"EDELE,{iel1},{iel2},{inc}", **kwargs)

    def eextrude(
        self,
        action="",
        nelem="",
        space="",
        dist="",
        theta="",
        tfact="",
        bckey="",
        **kwargs,
    ):
        """Extrudes 2-D plane elements into 3-D solids.

        APDL Command: EEXTRUDE

        Parameters
        ----------
        action
            Specifies one of the following command behaviors:

            AUTO - Extrudes plane elements (PLANE182 and PLANE183)
                   based on the KEYOPT(3) setting.  Complementary
                   elements are also extruded. (See Notes for more
                   information.) This behavior is the default.

            PLANE - Extrudes elements in the global Z
                    direction. KEYOPT(3) of the parent elements is
                    ignored.

            AXIS - Extrudes elements about the global Y
                   axis. KEYOPT(3) of the parent elements is ignored.

            TANGENT - Similar to Action = AXIS, except that target
                      elements are extruded in the global Z direction.

        nelem
            Number of elements to generate in the extruded direction. If you do
            not specify a number, the program calculates a number automatically
            based on the average element size and extrusion distance.

        space
            Spacing ratio. If positive, this value is the nominal
            ratio of the last division size to the first division size
            (if > 1.0, sizes increase, if < 1.0, sizes decrease). If
            negative, ``|SPACE|`` is the nominal ratio of the center
            division size to the end division size.  The default value
            is 1.0 (uniform spacing).

        dist
            Distance to extrude in the global Z direction for the plane strain
            case (Action = PLANE). The default is 1.

        theta
            Ending angle (in degrees) to extrude about the global Y axis for
            the axisymmetric case (Action = AXIS). The beginning angle is
            always 0 degrees. The ending angle defaults to 360 degrees.

        tfact
            Factor for increasing the rigid target size. The size of the
            extruded rigid target elements is determined automatically based on
            the size of the contact elements. The default value is 0.2.

        bckey
            Controls the nodal orientation in the third direction and
            boundary-condition mapping (Action = AXIS or TIRE only)

            * 0 : All nodes are rotated to a local Cartesian
                coordinate system where X is the radial, Y axial and Z
                circumferential direction. All loads and displacements
                are mapped from the 2-D model to the 3-D model in the
                local coordinate system.

                If applying rotation ROTY in axisymmetric cases with
                torsion on the 2-D model, this value sets UZ = 0 at
                all corresponding 3-D nodes.  This value is the
                default

            * 1 : Only nodes with applied loads and/or displacements
                are rotated to a local Cartesian co- ordinate system
                where X is the radial, Y axial and Z circumferential
                direction. All loads are mapped to the 3-D model and
                all applied displacements are reset to zero.

        Notes
        -----
        The EEXTRUDE command extrudes current-technology elements PLANE182 and
        PLANE183. Complementary elements TARGE169, CONTA171, CONTA172, and
        REINF263 will also extrude. Extrusion operates automatically on
        elements in the selected element set.

        For automatic PLANE182 and PLANE183 extrusion (Action = AUTO), based on
        the element behavior of the plane elements, the command performs as
        follows:

        Plane stress; the element is ignored.

        Axisymmetric; the element is extruded 360 degrees about the Y-axis.
        THETA is ignored.

        Plane strain (Z strain = 0.0); the element is extruded a unit distance
        in the global Z direction.

        Plane stress with thickness input; the element is extruded in the
        Z-direction as specified by the thickness input via a real constant.

        Generalized plane strain; the element is ignored.

        For an axisymmetric extrusion (Action = AUTO with KEYOPT(3) = 1, Action
        = AXIS, or Action = TANGENT), the command merges any nodes within the
        specified tolerance (SELTOL,TOLER) of the axis into a single node, then
        forms degenerate tetrahedrons, pyramids, or wedges. The default
        tolerance value is 1.0E-6.

        When issuing the EEXTRUDE command within the MAP2DTO3D environment
        using KEYOPT(3) = 3, mapping results do not provide the correct 3-D
        results state; therefore, KEYOPT(3) = 3 is suggested only as a tool for
        extruding the mesh itself as a geometric feature.

        For an axisymmetric extrusion, SHELL208 and SHELL209 will extrude.

        You can control shape-checking options via the SHPP command.

        The extrusion behavior of accompanying contact (CONTA171 and CONTA172)
        is determined by the plane element settings. Rigid target (TARGE169)
        elements are extruded in the global Z direction unless axisymmetric
        extrusion (Action = AXIS) is in effect.

        The following table shows each 2-D element capable of extrusion and its
        corresponding post-extrusion 3-D element:

        All element properties are also transferred consistently during
        extrusion. For example, a  2-D element is extruded to a  3-D element,
        and a mixed u-P 2-D element is extruded to a mixed u-P 3-D element.
        """
        command = f"EEXTRUDE,{action},{nelem},{space},{dist},{theta},{tfact},,{bckey}"
        return self.run(command, **kwargs)

    def egen(
        self,
        itime: MapdlInt = "",
        ninc: MapdlInt = "",
        iel1: Union[str, int] = "",
        iel2: MapdlInt = "",
        ieinc: MapdlInt = "",
        minc: MapdlInt = "",
        tinc: MapdlInt = "",
        rinc: MapdlInt = "",
        cinc: MapdlInt = "",
        sinc: MapdlInt = "",
        dx: MapdlFloat = "",
        dy: MapdlFloat = "",
        dz: MapdlFloat = "",
        **kwargs,
    ) -> Optional[str]:
        """Generates elements from an existing pattern.

        APDL Command: EGEN

        Parameters
        ----------
        itime, ninc
            Do this generation operation a total of ITIMEs,
            incrementing all nodes in the given pattern by NINC each
            time after the first. ITIME must be >1 if generation is
            to occur. NINC may be positive, zero, or negative.
            If DX, DY, and/or DZ is specified, NINC should be set
            so any existing nodes (as on NGEN) are not overwritten.

        iel1, iel2, ieinc
            Generate elements from selected pattern beginning with
            IEL1 to IEL2 (defaults to IEL1) in steps of IEINC (
            defaults to 1). If IEL1 is negative, IEL2 and IEINC are
            ignored and the last \|IEL1\| elements
            (in sequence backward from the maximum element number)
            are used as the pattern to be repeated.  If IEL1 = ALL,
            IEL2 and IEINC are ignored and use all selected elements
            [ESEL] as pattern to be repeated. A component name may
            also be substituted for IEL1 (IEL2 and INC are
            ignored).

        minc
            Increment material number of all elements in the given
            pattern by
            MINC each time after the first.

        tinc
            Increment type number by TINC.

        rinc
            Increment real constant table number by RINC.

        cinc
            Increment element coordinate system number by CINC.

        sinc
            Increment section ID number by SINC.

        dx, dy, dz
            Define nodes that do not already exist but are needed by
            generated
            elements (as though the NGEN,ITIME,INC,NODE1,,,DX,DY,
            DZ were issued
            before EGEN). Zero is a valid value. If blank, DX, DY,
            and DZ are
            ignored.

        Notes
        -----
        A pattern may consist of any number of previously defined
        elements. The MAT, TYPE, REAL, ESYS, and SECNUM numbers of
        the new elements are based upon the elements in the pattern
        and not upon the current specification settings.

        You can use the EGEN command to generate interface elements (
        INTER192, INTER193, INTER194, and INTER195) directly.
        However, because interface elements require that the element
        connectivity be started from the bottom surface, you must
        make sure that you use the correct element node connectivity.
        See the element descriptions for INTER192, INTER193,
        INTER194, and INTER195 for the correct element node definition.
        """
        command = (
            f"EGEN,{itime},{ninc},{iel1},{iel2},{ieinc},{minc},"
            f"{tinc},{rinc},{cinc},{sinc},{dx},{dy},{dz}"
        )
        return self.run(command, **kwargs)

    def einfin(
        self, compname: str = "", pnode: MapdlInt = "", **kwargs
    ) -> Optional[str]:
        """Generates structural infinite elements from selected nodes.

        APDL Command: EINFIN

        Parameters
        ----------
        compname
            Component name containing one node to be used as the pole
            node for generating INFIN257 structural infinite
            elements. The pole node is generally located at or near
            the geometric center of the finite element domain.

        pnode
            Node number for the direct input of the pole node. A
            parameter or parametric expression is also valid. Specify
            this value when no CompName has been specified. If
            CompName is specified, this value is ignored.

        Notes
        -----
        The EINFIN command generates structural infinite elements
        (INFIN257) directly from the selected face of valid base
        elements (existing standard elements in your model). The
        command scans all base elements for the selected nodes and
        generates a compatible infinite element type for each base
        element. A combination of different base element types is
        allowed if the types are all compatible with the infinite
        elements.

        The infinite element type requires no predefinition (ET).

        The faces of base elements are determined from the selected
        node set (NSEL), and the geometry of the infinite element is
        determined based on the shape of the face. Element
        characteristics and options are determined according to the
        base element. For the face to be used, all nodes on the face
        of a base element must be selected

        Use base elements to model the near-field domain that
        interacts with the solid structures or applied loads. To
        apply the truncated far-field effect, a single layer of
        infinite elements must be attached to the near-field domain.
        The outer surface of the near-field domain
        must be convex.

        After the EINFIN command executes, you can verify the newly
        created infinite element types and elements (ETLIST, ELIST,
        EPLOT).

        Infinite elements do not account for any subsequent
        modifications made to the base elements. It is good practice
        to issue the EINFIN
        command only after the base elements are finalized. If you
        delete or modify base elements, remove all affected infinite
        elements and reissue the EINFIN command; doing so prevents
        inconsistencies.
        """
        command = f"EINFIN,{compname},{pnode}"
        return self.run(command, **kwargs)

    def eintf(
        self,
        toler: MapdlFloat = "",
        k: MapdlInt = "",
        tlab: str = "",
        kcn: str = "",
        dx: MapdlFloat = "",
        dy: MapdlFloat = "",
        dz: MapdlFloat = "",
        knonrot: MapdlInt = "",
        **kwargs,
    ) -> Optional[str]:
        """Defines two-node elements between coincident or offset nodes.

        APDL Command: EINTF

        Parameters
        ----------
        toler
            Tolerance for coincidence (based on maximum Cartesian
            coordinate difference for node locations and on angle
            differences for node orientations). Defaults to 0.0001.
            Only nodes within the tolerance are considered to be
            coincident.

        k
            Only used when the type of the elements to be generated is
            PRETS179. K is the pretension node that is common to the
            pretension section that is being created. If K is not
            specified, it will be created by ANSYS automatically and
            will have an ANSYS-assigned node number. If K is
            specified but does not already exist, it will be
            created automatically but will have the user-specified
            node number. K cannot be connected to any existing element.

        tlab
            Nodal number ordering. Allowable values are:

            LOW - The 2-node elements are generated from the lowest
                  numbered node to the highest numbered node.

            HIGH - The 2-node elements are generated from the highest
                   numbered node to the lowest numbered node.

            REVE - Reverses the orientation of the selected 2-node
                   element.

        kcn
            In coordinate system KCN, elements are created between
            node 1 and node 2 (= node 1 + dx dy dz).

        dx, dy, dz
            Node location increments that define the node offset in
            the active coordinate system (DR, Dθ, DZ for cylindrical
            and DR, Dθ, DΦ for spherical or toroidal).

        knonrot
            When KNONROT = 0, the nodes coordinate system is not
            rotated. When KNONROT = 1, the nodes belonging to the
            elements created are rotated into coordinate system KCN
            (see NROTAT command description).

        Notes
        -----
        Defines 2-node elements (such as gap elements) between
        coincident or offset nodes (within a tolerance). May be used,
        for example, to "hook" together elements interfacing at a
        seam, where the seam consists of a series of node pairs. One
        element is generated for each set of two coincident nodes.
        For more than two coincident or offset nodes in a cluster,
        an element is generated from the lowest numbered
        node to each of the other nodes in the cluster. If fewer than
        all nodes are to be checked for coincidence, use the NSEL
        command to select the nodes. Element numbers are incremented
        by one from the highest previous element number. The element
        type must be set [ET] to a 2-node element before issuing this
        command. Use the CPINTF command to connect nodes by
        coupling instead of by elements. Use the CEINTF command to
        connect the nodes by constraint equations instead of by
        elements.

        For contact element CONTA178, the tolerance is based on the
        maximum Cartesian coordinate difference for node locations
        only. The angle differences for node orientations are not
        checked.
        """
        command = f"EINTF,{toler},{k},{tlab}," f"{kcn},{dx},{dy}," f"{dz},{knonrot}"
        return self.run(command, **kwargs)

    def elist(
        self,
        iel1: Union[str, int] = "",
        iel2: MapdlInt = "",
        inc: MapdlInt = "",
        nnkey: MapdlInt = "",
        rkey: MapdlInt = "",
        ptkey: MapdlInt = "",
        **kwargs,
    ) -> Optional[str]:
        """Lists the elements and their attributes.

        APDL Command: ELIST

        Parameters
        ----------
        iel1, iel2, inc
            Lists elements from IEL1 to IEL2 (defaults to IEL1) in
            steps of INC (defaults to 1). If IEL1 = ALL (default),
            IEL2 and INC are ignored and all selected elements [ESEL]
            are listed. A component name may also be substituted
            for IEL1 (IEL2 and INC are ignored).

        nnkey
            Node listing key:

            0 - List attribute references and nodes.

            1 - List attribute references but not nodes.

        rkey
            Real constant listing key:

            0 - Do not show real constants for each element.

            1 - Show real constants for each element. This includes
                default values chosen for
                the element.

        ptkey
            LS-DYNA part number listing key (applicable to ANSYS
            LS-DYNA only):

            0 - Do not show part ID number for each element.

            1 - Show part ID number for each element.

        Notes
        -----
        Lists the elements with their nodes and attributes (MAT,
        TYPE, REAL, ESYS, SECNUM, PART). See also the LAYLIST command
        for listing layered elements.

        This command is valid in any processor.
        """
        command = f"ELIST,{iel1},{iel2},{inc},{nnkey},{rkey},{ptkey}"
        return self.run(command, **kwargs)

    def emid(self, key="", edges="", **kwargs):
        """Adds or removes midside nodes.

        APDL Command: EMID

        Parameters
        ----------
        key
            Add or remove key:

            ADD - Add midside node to elements (default).

            REMOVE - Remove midside nodes from elements.

        edges
            ALL

            ALL - Add (or remove) midside nodes to (from) all edges of all selected elements,
                  independent of which nodes are selected (default).

            EITHER - Add (or remove) midside nodes only to (from) element edges which have either
                     corner node selected.

            BOTH - Add (or remove) midside nodes only to (from) element edges which have both
                   corner nodes selected.

        Notes
        -----
        This command adds midside nodes to (or removes midside nodes from) the
        selected elements. For this to occur, the selected elements must be
        midside node capable, the active element type [TYPE] must allow midside
        node capability, and the relationship between the finite element model
        and the solid model (if any) must first be disassociated [MODMSH].

        By default, EMID generates a midside node wherever a zero (or missing)
        midside node occurs for that element. You can control this and add (or
        remove) midside nodes selectively by using the Edges argument. Nodes
        are located midway between the two appropriate corner nodes based on a
        linear Cartesian interpolation. Nodal coordinate system rotation angles
        are also linearly interpolated. Connected elements share the same
        midside node. Node numbers are generated sequentially from the maximum
        node number.

        The EMID command is useful for transforming linear element types to
        quadratic element types having the same corner node connectivity.

        EMID is also useful for transforming elements created outside of the
        program.
        """
        command = f"EMID,{key},{edges}"
        return self.run(command, **kwargs)

    def emodif(
        self,
        iel: Union[str, int] = "",
        stloc: Union[str, int] = "",
        i1: MapdlInt = "",
        i2: MapdlInt = "",
        i3: MapdlInt = "",
        i4: MapdlInt = "",
        i5: MapdlInt = "",
        i6: MapdlInt = "",
        i7: MapdlInt = "",
        i8: MapdlInt = "",
        **kwargs,
    ) -> Optional[str]:
        """Modifies a previously defined element.

        APDL Command: EMODIF

        Parameters
        ----------
        iel
            Modify nodes and/or attributes for element number IEL.  If
            ALL, modify all selected elements [ESEL]. A component name
            may also be substituted for IEL.

        stloc
            Starting location (n) of first node to be modified or the
            attribute label.

        i1, i2, i3, i4, i5, i6, i7, i8
            Replace the previous node numbers assigned to this element
            with these corresponding values. A (blank) retains the
            previous value (except in the I1 field, which resets the
            STLOC node number to zero).

        Notes
        -----
        The nodes and/or attributes (MAT, TYPE, REAL, ESYS, and SECNUM
        values) of an existing element may be changed with this
        command.

        Examples
        --------
        Modify all elements to have a material number of 2.

        >>> mapdl.clear()
        >>> mapdl.prep7()
        >>> mp_num = 2
        >>> mapdl.mp('EX', mp_num, 210E9)
        >>> mapdl.mp('DENS', mp_num, 7800)
        >>> mapdl.mp('NUXY', mp_num, 0.3)
        >>> mapdl.block(0, 1, 0, 1, 0, 1)
        >>> mapdl.et(1, 'SOLID186')
        >>> mapdl.vmesh('ALL')
        >>> mapdl.emodif('ALL', 'MAT', i1=mp_num)
        'MODIFY ALL SELECTED ELEMENTS TO HAVE  MAT  =         2'

        Use `emodif` to modify all of volume 2's elements
        after meshing.

        >>> mapdl.vmesh('S', 'VOLU', '', 2)
        >>> mapdl.allsel('BELOW', 'VOLU')
        >>> mapdl.emodif('ALL', 'MAT', 2)

        """
        command = f"EMODIF,{iel},{stloc},{i1},{i2},{i3},{i4},{i5},{i6},{i7},{i8}"
        return self.run(command, **kwargs)

    def emore(
        self,
        q: MapdlInt = "",
        r: MapdlInt = "",
        s: MapdlInt = "",
        t: MapdlInt = "",
        u: MapdlInt = "",
        v: MapdlInt = "",
        w: MapdlInt = "",
        x: MapdlInt = "",
        **kwargs,
    ) -> Optional[str]:
        """Add more nodes to the just-defined element.

        APDL Command: EMORE

        Repeat this method for up to 4 additional nodes (20
        maximum). Nodes are added after the last nonzero node of the
        element.  Node numbers defined with this command may be
        zeroes.

        Parameters
        ----------
        q, r, s, t, u, v, w, x
            Numbers of nodes typically assigned to ninth (node Q)
            through sixteenth (node X) nodal positions, if any.

        Examples
        --------
        Generate a single quadratic element.

        >>> mapdl.prep7()
        >>> mapdl.et(1, 'SOLID186')
        >>> mapdl.n(1, -1, -1, -1)
        >>> mapdl.n(2,  1, -1, -1)
        >>> mapdl.n(3,  1,  1, -1)
        >>> mapdl.n(4, -1,  1, -1)
        >>> mapdl.n(5, -1, -1,  1)
        >>> mapdl.n(6,  1, -1,  1)
        >>> mapdl.n(7,  1,  1,  1)
        >>> mapdl.n(8, -1,  1,  1)
        >>> mapdl.n(9,  0, -1, -1)
        >>> mapdl.n(10,  1,  0, -1)
        >>> mapdl.n(11,  0,  1, -1)
        >>> mapdl.n(12, -1,  0, -1)
        >>> mapdl.n(13,  0, -1,  1)
        >>> mapdl.n(14,  1,  0,  1)
        >>> mapdl.n(15,  0,  1,  1)
        >>> mapdl.n(16, -1,  0,  1)
        >>> mapdl.n(17, -1, -1,  0)
        >>> mapdl.n(18,  1, -1,  0)
        >>> mapdl.n(19,  1,  1,  0)
        >>> mapdl.n(20, -1,  1,  0)
        >>> mapdl.e(1, 2, 3, 4, 5, 6, 7, 8)
        >>> mapdl.emore(9, 10, 11, 12, 13, 14, 15, 16)
        >>> output = mapdl.emore(17, 18, 19, 20)
        'ELEMENT 1  1  2  3  4  5  6  7  8
                    9 10 11 12 13 14 15 16
                   17 18 19 20

        """
        command = f"EMORE,{q},{r},{s},{t},{u},{v},{w},{x}"
        return self.run(command, **kwargs)

    def emtgen(
        self,
        ncomp="",
        ecomp="",
        pncomp="",
        dof="",
        gap="",
        gapmin="",
        fkn="",
        epzero="",
        **kwargs,
    ):
        """Generates a set of TRANS126 elements.

        APDL Command: EMTGEN

        Parameters
        ----------
        ncomp
            Component name of the surface nodes of a structure which attach to
            the TRANS126 elements. You must enclose name-strings in single
            quotes in the EMTGEN command line.

        ecomp
            Component name of the TRANS126 elements generated. You must
            enclose name-strings in single quotes in the EMTGEN command line.
            Defaults to EMTELM.

        pncomp
            Component name of the plane nodes generated by the command at an
            offset (GAP) from the surface nodes. You must enclose name-strings
            in single quotes in the EMTGEN command line. Defaults to EMTPNO.

        dof
            Active structural degree of freedom (DOF) for TRANS126 elements
            (UX, UY, or UZ) in the Cartesian coordinate system. You must
            enclose the DOF in single quotes.

        gap
            Initial gap distance from the surface nodes to the plane. Be sure
            to use the correct sign with respect to Ncomp node location.

        gapmin
            Minimum gap distance allowed (GAPMIN real constant) for TRANS126
            elements. Defaults to the absolute value of (GAP)*0.05.

        fkn
            Contact stiffness factor used as a multiplier for a contact
            stiffness appropriate for bulk deformation. Defaults to 0.1.

        epzero
            Free-space permittivity. Defaults to 8.854e-6 (μMKS units).

        Notes
        -----
        The EMTGEN command generates a set of TRANS126 elements between the
        surface nodes of a moveable structure and a plane of nodes, typically
        representing a ground plane. The plane of nodes are created by the
        command at a specified offset (GAP). Each element attaches to a surface
        node and to a corresponding node representing the plane. The created
        elements are set to the augmented stiffness method (KEYOPT(6) = 1),
        which can help convergence. The generated plane nodes should be
        constrained appropriately for the analysis.

        You can use TRANS126 elements for simulating fully coupled
        electrostatic structural coupling between a MEMS device and a plane, if
        the gap distance between the device and the plane is small compared to
        the overall surface area dimensions of the device. This assumption
        allows for a point-wise closed-form solution of capacitance between the
        surface nodes and the plane; i.e. CAP = ``EPZERO*AREA/GAP``, where EPZERO
        if the free-space permittivity, AREA is the area associated with the
        node, and GAP is the gap between the node and the plane. The area for
        each node is computed using the ARNODE function in ANSYS. See the ``*GET``
        command description for more information on the ARNODE function.

        With a distributed set of TRANS126 elements attached directly to the
        structure and a plane (such as a ground plane), you can perform a full
        range of coupled electrostatic-structural simulations, including:

        Static analysis (due to a DC voltage or a mechanical load)

        Prestressed modal analysis (eigenfrequencies, including frequency-shift
        effects of a DC bias voltage)

        Prestressed harmonic analysis (system response to a small-signal AC
        excitation with a DC bias voltage or mechanical load)

        Large signal transient analysis (time-transient solution due to an
        arbitrary time-varying voltage or mechanical excitation)

        The TRANS126 element also employs a node-to-node gap feature so you can
        perform contact-type simulations where the structure contacts a plane
        (such as a ground plane). The contact stiffness factor, FKN, is used to
        control contact penetration once contact is initiated. A smaller value
        provides for easier convergence, but with more penetration.
        """
        command = f"EMTGEN,{ncomp},{ecomp},{pncomp},{dof},{gap},{gapmin},{fkn},{epzero}"
        return self.run(command, **kwargs)

    def en(
        self,
        iel: MapdlInt = "",
        i: MapdlInt = "",
        j: MapdlInt = "",
        k: MapdlInt = "",
        l: MapdlInt = "",
        m: MapdlInt = "",
        n: MapdlInt = "",
        o: MapdlInt = "",
        p: MapdlInt = "",
        **kwargs,
    ) -> Optional[str]:
        """Defines an element by its number and node connectivity.

        APDL Command: EN

        Parameters
        ----------
        iel
            Number assigned to element being defined.

        i
            Number of node assigned to first nodal position (node I).

        j, k, l, m, n, o, p
            Number assigned to second (node J) through eighth (node
            P) nodal position, if any.

        Notes
        -----
        Defines an element by its nodes and attribute values. Similar
        to the E command except it allows the element number (IEL) to be defined
        explicitly. Element numbers need not be consecutive. Any
        existing element already having this number will be redefined.

        Up to 8 nodes may be specified with the EN command. If more
        nodes are needed for the element, use the
        :meth:`emore` command. The number of nodes required and the
        order in which they should be specified are described in the
        Element Reference for each element type.  The current (or
        default) MAT, TYPE, REAL, SECNUM, and ESYS attribute values
        are also assigned to the element.

        When creating elements with more than 8 nodes using this
        command and the :meth:`emore` command, it may be necessary to
        turn off shape checking using the SHPP command before
        issuing this command. If a valid element type can be created
        without using the additional nodes on the :meth:`emore`
        command, this command will create that element. The
        :meth:`emore` command will then modify the element to include
        the additional nodes. If shape checking is active, it will be
        performed before the :meth:`emore` command is issued.
        Therefore, if the shape checking limits are exceeded, element
        creation may fail before the :meth:`emore` command modifies
        the element into an acceptable shape.
        """
        command = f"EN,{iel},{i},{j},{k},{l},{m},{n},{o},{p}"
        return self.run(command, **kwargs)

    def endrelease(self, tolerance="", dof1="", dof2="", dof3="", dof4="", **kwargs):
        """Specifies degrees of freedom to be decoupled for end release.

        APDL Command: ENDRELEASE

        Parameters
        ----------
        tolerance
            Angle tolerance (in degrees) between adjacent elements. Defaults to
            20°. Set TOLERANCE to -1 to indicate all selected elements.

        dof1, dof2, dof3, dof4
            Degrees of freedom to release. If Dof1 is blank, WARP is assumed
            and Dof2, Dof3, and Dof4 are ignored.

            WARP - Release the warping degree of freedom (default).

            ROTX - Release rotations in the X direction.

            ROTY - Release rotations in the Y direction.

            ROTZ - Release rotations in the Z direction.

            UX - Release displacements in the X direction.

            UY - Release displacements in the Y direction.

            UZ - Release displacements in the Z direction.

            BALL - Create ball joints (equivalent to releasing WARP,
            ROTX, ROTY, and ROTZ).

        Notes
        -----
        This command specifies end releases for the BEAM188, BEAM189, PIPE288,
        and PIPE289 elements. The command works on currently selected nodes and
        elements. It creates end releases on any two connected beam elements
        whose angle at connection exceeds the specified tolerance. From within
        the GUI, the Picked node option generates an end release at the
        selected node regardless of the angle of connection (angle tolerance is
        set to -1).

        Use the CPLIST command to list the coupled sets generated by the
        ENDRELEASE command.

        Note:: : You should exercise due engineering judgement when using this
        command, as improper use may result in mechanics that render a solution
        impossible.
        """
        command = f"ENDRELEASE,,{tolerance},{dof1},{dof2},{dof3},{dof4}"
        return self.run(command, **kwargs)

    def engen(
        self,
        iinc: MapdlInt = "",
        itime: MapdlInt = "",
        ninc: MapdlInt = "",
        iel1: MapdlInt = "",
        iel2: MapdlInt = "",
        ieinc: MapdlInt = "",
        minc: MapdlInt = "",
        tinc: MapdlInt = "",
        rinc: MapdlFloat = "",
        cinc: MapdlInt = "",
        sinc: MapdlInt = "",
        dx: MapdlInt = "",
        dy: MapdlInt = "",
        dz: MapdlInt = "",
        **kwargs,
    ) -> Optional[str]:
        """Generates elements from an existing pattern.

        APDL Command: ENGEN

        Parameters
        ----------
        iinc
            Increment to be added to element numbers in pattern.

        itime, ninc
            Do this generation operation a total of ITIMEs,
            incrementing all nodes in the given pattern by NINC each
            time after the first. ITIME must be > 1 if generation is
            to occur. NINC may be positive, zero, or negative.

        iel1, iel2, ieinc
            Generate elements from the pattern that begins with IEL1
            to IEL2 (defaults to IEL1) in steps of IEINC (defaults to
            1). If IEL1 is negative, IEL2 and IEINC are ignored and
            use the last \|IEL1\| elements (in sequence backward from
            the maximum element number) as the pattern to be
            repeated.  If IEL1 = ALL, IEL2 and IEINC are ignored and
            all selected elements [ESEL] are used as the
            pattern to be repeated. A component name may also be
            substituted for IEL1 (IEL2 and IEINC are ignored).

        minc
            Increment material number of all elements in the given
            pattern by MINC each time after the first.

        tinc
            Increment type number by TINC.

        rinc
            Increment real constant table number by RINC.

        cinc
            Increment element coordinate system number by CINC.

        sinc
            Increment section ID number by SINC.

        dx, dy, dz
            Define nodes that do not already exist but are needed by
            generated elements (NGEN,ITIME,INC,NODE1,,,DX,DY,
            DZ). Zero is a valid value. If blank, DX, DY, and DZ are
            ignored.

        Notes
        -----
        Same as the EGEN command except it allows element numbers to be
        explicitly incremented (IINC) from the generated set. Any
        existing elements already having these numbers will be
        redefined.
        """
        command = (
            f"ENGEN,{iinc},{itime},{ninc},{iel1},{iel2},"
            f"{ieinc},{minc},{tinc},{rinc},{cinc},{sinc},{dx},"
            f"{dy},{dz}"
        )
        return self.run(command, **kwargs)

    def enorm(self, enum: Union[str, int] = "", **kwargs) -> Optional[str]:
        """Reorients shell element normals or line element node connectivity.

        APDL Command: ENORM

        Parameters
        ----------
        enum
            Element number having the normal direction that the
            reoriented elements are to match.

        Notes
        -----
        Reorients shell elements so that their outward normals are
        consistent with that of a specified element. ENORM can also be
        used to reorder nodal connectivity of line elements so that
        their nodal ordering is consistent with that of a specified
        element.

        For shell elements, the operation reorients the element by
        reversing and shifting the node connectivity pattern. For
        example, for a 4-node shell element, the nodes in positions I,
        J, K and L of the original element are placed in positions J,
        I, L and K of the reoriented element. All 3-D shell elements
        in the selected set are considered for reorientation, and no
        element is reoriented more than once during the
        operation. Only shell elements adjacent to the lateral (side)
        faces are considered.

        The command reorients the shell element normals on the same
        panel as the specified shell element. A panel is the geometry
        defined by a subset of shell elements bounded by free edges or
        T-junctions (anywhere three or more shell edges share common
        nodes).

        Reorientation progresses within the selected set until either
        of the following conditions is true:

        - The edge of the model is reached.

        - More than two elements (whether selected or unselected) are
          adjacent to a lateral face.

        In situations where unselected elements might undesirably
        cause case b to control, consider using ENSYM,0,,0,ALL instead
        of ENORM.  It is recommended that reoriented elements be
        displayed and graphically reviewed.

        You cannot use the ENORM command to change the normal
        direction of any element that has a body or surface load. We
        recommend that you apply all of your loads only after ensuring
        that the element normal directions are acceptable.

        Real constant values are not reoriented and may be invalidated
        by an element reversal.

        Examples
        --------
        >>> mapdl.enorm(1)

        """
        return self.run(f"ENORM,{enum}", **kwargs)

    def ensym(
        self,
        iinc: MapdlInt = "",
        ninc: MapdlInt = "",
        iel1: MapdlInt = "",
        iel2: MapdlInt = "",
        ieinc: MapdlInt = "",
        **kwargs,
    ) -> Optional[str]:
        """Generates elements by symmetry reflection.

        APDL Command: ENSYM

        Parameters
        ----------
        iinc
            Increment to be added to element numbers in existing set.

        ninc
            Increment nodes in the given pattern by NINC.

        iel1, iel2, ieinc
            Reflect elements from pattern beginning with IEL1 to IEL2
            (defaults to IEL1) in steps of IEINC (defaults to 1). If
            IEL1 = ALL, IEL2 and IEINC are ignored and pattern is all
            selected elements [ESEL]. A component name may also be
            substituted for IEL1 (IEL2 and IEINC are ignored).

        Notes
        -----
        This command is the same as the ESYM command except it allows
        explicitly assigning element numbers to the generated set (in
        terms of an increment IINC). Any existing elements already
        having these numbers will be redefined.

        The operation generates a new element by incrementing the
        nodes on the original element, and reversing and shifting the
        node connectivity pattern.  For example, for a 4-node 2-D
        element, the nodes in positions I, J, K and L of the original
        element are placed in positions J, I, L and K of the reflected
        element.

        Similar permutations occur for all other element types. For
        line elements, the nodes in positions I and J of the original
        element are placed in positions J and I of the reflected
        element. In releases prior to ANSYS 5.5, no node pattern
        reversing and shifting occurred for line elements generated by
        ENSYM. To achieve the same results as you did in releases
        prior to ANSYS 5.5, use the ENGEN command instead.

        See the ESYM command for additional information about symmetry
        elements.

        The ENSYM command also provides a convenient way to reverse
        shell element normals. If the IINC and NINC argument fields
        are left blank, the effect of the reflection is to reverse the
        direction of the outward normal of the specified elements. You
        cannot use the ENSYM command to change the normal direction of
        any element that has a body or surface load. We recommend that
        you apply all of your loads only after ensuring that the
        element normal directions are acceptable. Also note that real
        constants (such as nonuniform shell thickness and tapered beam
        constants) may be invalidated by an element reversal. See
        Revising Your Model in the Modeling and Meshing Guide for more
        information about controlling element normals.
        """
        return self.run(f"ENSYM,{iinc},,{ninc},{iel1},{iel2},{ieinc}", **kwargs)

    def eplot(self, **kwargs):
        """Plots the currently selected elements.

        APDL Command: EPLOT

        Notes
        ------
        Produces an element display of the selected elements. In full
        graphics, only those elements faces with all of their corresponding
        nodes selected are plotted. In PowerGraphics, all element faces of the selected
        element set are plotted irrespective of the nodes selected. However,
        for both full graphics and Power Graphics, adjacent or otherwise
        duplicated faces of 3-D solid elements will not be displayed in an attempt
        to eliminate plotting of interior facets. See the ``DSYS`` command for display
        coordinate system issues.
        This command will display curvature in midside node elements when PowerGraphics is activated
        [``/GRAPHICS ,POWER``] and ``/EFACET,2`` or ``/EFACET,4`` are enabled. (To display
        curvature, two facets per edge is recommended [``/EFACET,2``]). When you specify ``/EFACET,1``,
        PowerGraphics does not display midside nodes. ``/EFACET`` has no effect on EPLOT for non-midside
        node elements.
        This command is valid in any processor.

        """
        return self.run("EPLOT", **kwargs)

    def eread(self, fname: str = "", ext: str = "", **kwargs) -> Optional[str]:
        """Reads elements from a file.

        APDL Command: EREAD

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

        Notes
        -----
        This read operation is not necessary in a standard ANSYS run
        but is provided as a convenience to users wanting to read a
        coded element file, such as from another mesh generator or
        from a CAD/CAM program.  Data should be formatted as produced
        with the EWRITE command. If issuing EREAD to acquire element
        information generated from ANSYS EWRITE, you must also issue
        NREAD before the EREAD command. The element types [ET] must be
        defined before the file is read so that the file may be read
        properly. Only elements that are specified with the ERRANG
        command are read from the file. Also, only elements that are
        fully attached to the nodes specified on the NRRANG command
        are read from the file. Elements are assigned numbers
        consecutively as read from the file, beginning with the
        current highest database element number plus one. The file is
        rewound before and after reading. Reading continues until the
        end of the file.
        """
        command = f"EREAD,{fname},{ext}"
        return self.run(command, **kwargs)

    def ereinf(self, **kwargs) -> Optional[str]:
        """Generates reinforcing elements from selected existing (base) elements.

        APDL Command: EREINF

        Notes
        -----
        The EREINF command generates reinforcing elements (REINF264 and
        REINF265) directly from selected base elements (that is,
        existing standard elements in your model). The command scans all
        selected base elements and generates (if necessary) a compatible
        reinforcing element type for each base element. (ANSYS
        allows a combination of different base element types.)

        Although predefining the reinforcing element type (ET) is not
        required, you must define the reinforcing element section type
        (SECTYPE); otherwise, ANSYS cannot generate the
        reinforcing element.

        The EREINF command does not create new nodes. The reinforcing
        elements and the base elements share the common nodes.

        Elements generated by this command are not associated with
        the solid model.

        After the EREINF command executes, you can issue ETLIST, ELIST,
        and EPLOT commands to verify the newly created reinforcing
        element types and elements.

        Reinforcing elements do not account for any subsequent
        modifications made to the base elements. ANSYS,
        Inc. recommends issuing the EREINF command only after the
        base elements are finalized. If you delete or modify base
        elements (via EDELE, EMODIF, ETCHG, EMID, EORIENT, NUMMRG,
        or NUMCMP commands, for example), remove all affected
        reinforcing elements and reissue the EREINF command to avoid
        inconsistencies.
        """
        command = f"EREINF,"
        return self.run(command, **kwargs)

    def errang(
        self,
        emin: MapdlInt = "",
        emax: MapdlInt = "",
        einc: MapdlInt = "",
        **kwargs,
    ) -> Optional[str]:
        """Specifies the element range to be read from a file.

        APDL Command: ERRANG

        Parameters
        ----------
        emin, emax, einc
            Elements with numbers from EMIN (defaults to 1) to EMAX
            (defaults to 99999999) in steps of EINC (defaults to 1)
            will be read.

        Notes
        -----
        Defines the element number range to be read [EREAD] from the
        element file. If a range is also implied from the NRRANG
        command, only those elements satisfying both ranges will be
        read.
        """
        command = f"ERRANG,{emin},{emax},{einc}"
        return self.run(command, **kwargs)

    def esurf(
        self, xnode: MapdlInt = "", tlab: str = "", shape: str = "", **kwargs
    ) -> Optional[str]:
        """Generates elements overlaid on the free faces of selected nodes.

        APDL Command: ESURF

        Parameters
        ----------
        xnode
            Node number that is used only in the following two cases:

        tlab
            Generates target, contact, and hydrostatic fluid elements
            with correct direction of normals.

            TOP - Generates target and contact elements over beam and
                  shell elements, or hydrostatic fluid elements over
                  shell elements, with the normals the same as the
                  underlying beam and shell elements (default).

            BOTTOM - Generates target and contact elements over beam
                     and shell elements, or hydrostatic fluid
                     elements over shell elements, with the
                     normals opposite to the underlying beam and shell
                     elements.

            If target or contact elements and hydrostatic fluid
            elements are defined on the same underlying shell
            elements, you only need to use this option once to orient
            the normals opposite to the
            underlying shell elements.

            REVERSE - Reverses the direction of the normals on
                      existing selected target elements, contact
                      elements, and hydrostatic fluid elements. - If
                      target or contact elements and hydrostatic
                      fluid elements are defined on the same
                      underlying shell elements, you only need to use
                      this option once to reverse the normals for all
                      selected elements.

        shape
            Used to specify the element shape for target element
            TARGE170 (Shape = LINE or POINT) or TARGE169 elements
            (Shape = POINT).

            (blank) - The target element takes the same shape as the
                      external surface of the underlying element
                      (default).

            LINE - Generates LINE or PARA (parabolic) segments on
                   exterior of selected 3-D elements.

            POINT - Generates POINT segments on selected nodes.

        Notes
        -----
        The ESURF command generates elements of the currently active
        element type overlaid on the free faces of existing elements.
        For example, surface elements (such as SURF151, SURF152,
        SURF153, SURF154, or SURF159) can be generated over solid
        elements (such as PLANE55, SOLID70, PLANE182, SOLID185,
        or SOLID272, respectively).

        Element faces are determined from the selected node set
        (NSEL) and the load faces for that element type. The
        operation is similar to that used for generating element
        loads from selected nodes via the SF,ALL command, except that
        elements (instead of loads) are generated. All nodes on the
        face must be selected for the face to be used. For shell
        elements, only face one of the element is available. If nodes
        are shared by adjacent selected element faces, the faces are not
        free and no element is generated.

        Elements created by ESURF are oriented such that their
        surface load directions are consistent with those of the
        underlying elements. Carefully check generated elements and
        their orientations.

        Generated elements use the existing nodes and the active MAT,
        TYPE, REAL, and ESYS attributes. The exception is when Tlab =
        REVERSE. The reversed target and contact elements have the
        same attributes as the original elements. If the underlying
        elements are solid elements, Tlab = TOP or BOTTOM has no effect.

        When the command generates a target element, the shape is by
        default the same as that of the underlying element. Issue
        ESURF,,, LINE or ESURF,,,POINT to generate LINE, PARA,
        and POINT segments.

        The ESURF command can also generate the 2-D or 3-D
        node-to-surface element CONTA175, based on the selected node
        components of the underlying solid elements. When used to
        generate CONTA175 elements, all ESURF arguments are ignored.
        (If CONTA175 is the active element type, the path Main Menu>
        Preprocessor> Modeling> Create> Elements> Node-to-Surf uses
        ESURF to generate elements.)

        To generate SURF151 or SURF152 elements that have two extra
        nodes from FLUID116 elements, KEYOPT(5) for SURF151 or
        SURF152 is first set to 0 and ESURF is issued. Then KEYOPT(5)
        for SURF151 or SURF152 is set to 2 and MSTOLE is issued. For
        more information, see Using the Surface Effect Elements in
        the Thermal Analysis Guide.

        For hydrostatic fluid elements HSFLD241 and HSFLD242,
        the ESURF command generates triangular (2-D) or
        pyramid-shaped (3-D) elements with bases that are overlaid on
        the faces of selected 2-D or 3-D solid or shell elements.
        The single vertex for all generated elements is at the
        pressure node specified as XNODE. The generated elements fill
        the volume enclosed by the solid or shell elements. The nodes
        on the overlaid faces have translational degrees of freedom,
        while the pressure node shared by all generated elements has
        a single hydrostatic pressure degree of freedom, HDSP (see
        HSFLD241 and HSFLD242 for more information about the pressure
        node).
        """
        command = f"ESURF,{xnode},{tlab},{shape}"
        return self.run(command, **kwargs)

    def esym(
        self,
        ninc: MapdlInt = "",
        iel1: MapdlInt = "",
        iel2: MapdlInt = "",
        ieinc: MapdlInt = "",
        **kwargs,
    ) -> Optional[str]:
        """Generates elements from a pattern by a symmetry reflection.

        APDL Command: ESYM

        Parameters
        ----------
        ninc
            Increment nodes in the given pattern by NINC.

        iel1, iel2, ieinc
            Reflect elements from pattern beginning with IEL1 to IEL2
            (defaults to IEL1) in steps of IEINC (defaults to 1). If
            IEL1 = ALL, IEL2 and IEINC are ignored and pattern is all
            selected elements [ESEL]. A component name may
            also be substituted for IEL1 (IEL2 and IEINC are ignored).

        Notes
        -----
        Generates additional elements from a given pattern (similar
        to EGEN) except with a "symmetry" reflection. The operation
        generates a new element by incrementing the nodes on the
        original element, and reversing and shifting  the node
        connectivity pattern. For example, for a 4-node 2-D element,
        the nodes in positions I, J, K, and L of the original element
        are placed in positions J, I, L, and K of the reflected element.

        Similar permutations occur for all other element types. For line
        elements, the nodes in positions I and J of the original
        element are placed in positions J and I of the reflected
        element. In releases prior
        to ANSYS 5.5, no node pattern reversing and shifting occurred
        for line elements generated by ESYM. To achieve the same
        results with ANSYS 5.5 as you did in prior releases, use the
        EGEN command instead.

        It is recommended that symmetry elements be displayed and
        graphically reviewed.

        If the nodes are also reflected (as with the NSYM command)
        this pattern is such that the orientation of the symmetry
        element remains similar to the original element (i.e.,
        clockwise elements are generated from
        clockwise elements).

        For a non-reflected node pattern, the reversed orientation
        has the effect of reversing the outward normal direction (
        clockwise elements are generated from counterclockwise
        elements).

        Note:: : Since nodes may be defined anywhere in the model
        independently of this command, any orientation of the
        "symmetry" elements is possible. See also the ENSYM command
        for modifying existing elements.
        """
        return self.run(f"ESYM,,{ninc},{iel1},{iel2},{ieinc}", **kwargs)

    def ewrite(
        self,
        fname: str = "",
        ext: str = "",
        kappnd: MapdlInt = "",
        format_: str = "",
        **kwargs,
    ) -> Optional[str]:
        """Writes elements to a file.

        APDL Command: EWRITE

        Writes the selected elements to a file. The write operation is not
        necessary in a standard ANSYS run but is provided as convenience
        to users wanting a coded element file. If issuing :meth:`ewrite`
        from ANSYS to be used in ANSYS, you must also issue NWRITE to
        store nodal information for later use. Only elements having all of
        their nodes defined (and selected) are written. Data are written
        in a coded format. The data description of each record is: I, J,
        K, L, M, N, O, P, MAT, TYPE, REAL, SECNUM, ESYS, IEL, where MAT,
        TYPE, REAL, and ESYS are attribute numbers, SECNUM is the beam
        section number, and IEL is the element number.

        The format is (14I6) if Format is set to SHORT and (14I8) if the
        Format is set to LONG, with one element description per record for
        elements having eight nodes of less. For elements having more than
        eight nodes, nodes nine and above are written on a second record
        with the same format.

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

        format_
            Format key:

            SHORT - I6 format (the default).

            LONG - I8 format.

        Examples
        --------
        >>> mapdl.ewrite('etable.txt', format_='LONG')

        """
        return self.run(f"EWRITE,{fname},{ext},,{kappnd},{format_}", **kwargs)

    def gcdef(self, option="", sect1="", sect2="", matid="", realid="", **kwargs):
        """Defines interface interactions between general contact surfaces.

        APDL Command: GCDEF

        GCDEF defines the interface interaction between general contact
        surfaces identified by SECT1 and SECT2. GCDEF commands are order
        independent in most cases.

        GCDEF definitions should be issued after GCGEN. They are saved in the
        database and are written to and read from .CDB files.

        See General Contact in the Contact Technology Guide for more
        information on the overall procedure to create general contact.

        SECT1/SECT2 Interactions

        The most specific types of general contact definitions are those
        described below:

        The remaining general contact definition types can be overridden by the
        above two general contact definition types:

        Parameters
        ----------
        option
            Option to be performed.

            (blank) - Retain the previous Option setting between SECT1 and SECT2.

            AUTO - Define auto asymmetric contact between surfaces SECT1 and SECT2.

            SYMM - Define symmetric contact between surfaces SECT1 and SECT2.

            ASYM - Define asymmetric contact with SECT1 as the source
                   (contact) surface and SECT2 as the target surface.

            EXCL - Exclude contact between surfaces SECT1 and
            SECT2. MATID and REALID are ignored.

            DELETE - Remove the given definition from the GCDEF
            table. MATID and REALID are ignored.

            Note that GCDEF,DELETE,ALL,ALL does not remove the entire
            GCDEF table; it merely removes any existing GCDEF,,ALL,ALL
            definitions, while leaving intact any existing GCDEF
            definitions that are more specific.  - To remove the
            entire GCDEF table, issue GCDEF,DELETE,TOTAL.

            It is good practice to list all definitions using
            GCDEF,LIST,ALL,ALL before and after a GCDEF,DELETE
            command.

            LIST - List stored GCDEF data entries. MATID and REALID are
            ignored. GCDEF,LIST,ALL,ALL lists the entire GCDEF table,
            including more specific GCDEF definitions. - TABLE

        sect1, sect2
            Section numbers representing general contact surfaces (no
            defaults). Labels ALL and SELF are also valid input. See
            SECT1/SECT2 Interactions for a description of how the various
            inputs for SECT1 and SECT2 are interpreted.

        matid
            Material ID number for general contact interaction properties at
            the SECT1/SECT2 interface. If zero or blank, the previous setting
            of MATID for SECT1/SECT2 (if any) is retained.

        realid
            Real constant ID number for general contact interaction properties
            at the SECT1/SECT2 interface.  If zero or blank, the previous
            setting of REALID for SECT1/SECT2 (if any) is retained.

        """
        command = f"GCDEF,{option},{sect1},{sect2},{matid},{realid}"
        return self.run(command, **kwargs)

    def gcgen(
        self,
        option="",
        featureangle="",
        edgekey="",
        splitkey="",
        selopt="",
        **kwargs,
    ):
        """Creates contact elements for general contact.

        APDL Command: GCGEN

        Parameters
        ----------
        option
            Option to be performed.

            NEW - Create a new general contact definition. This option removes all existing
                  general contact elements and generates new elements with new
                  section IDs. Any existing GCDEF specifications, general
                  contact SECTYPE/SECDATA data, and general contact element
                  types are also removed. If no general contact elements or
                  data exist, this option behaves the same as Option = UPDATE.

            UPDATE - Generate general contact elements on newly added (or selected) base elements.
                     Newly generated contact elements are assigned new Section
                     IDs. Existing general contact elements remain with their
                     previously assigned section IDs and element attributes.
                     Existing GCDEF and SECTYPE/SECDATA general contact data
                     are respected. (This is the default option.)

            DELETE - Remove all existing general contact elements. Existing GCDEF specifications,
                     general contact SECTYPE/SECDATA data, and general contact
                     element types are also removed.

            SELECT - Select all existing general contact elements.

        featureangle
            Angle tolerance for determining feature edges (EdgeKEY) and general
            surfaces (SplitKey). Default = 42 degrees.

        edgekey
            Key that controls creation of general contact line elements
            (CONTA177) on base shell element perimeter edges and/or base solid
            element feature edges. See Understanding FeatureANGLE for an
            explanation of the feature edge criteria.

            0 - Exclude feature edges and shell perimeter edges (default).

            1 - Include feature edges only.

            2 - Include shell perimeter edges only.

            3 - Include both feature edges and shell perimeter edges.

        splitkey
            Key that controls how section IDs and contact element type IDs are
            assigned to surfaces.

            SPLIT - Assign a different section ID and contact element type ID for every general
                    surface of the selected base elements (default). See
                    Understanding FeatureANGLE for an explanation of the split
                    criteria. Different section IDs are assigned to top and
                    bottom surfaces of 2-D beam and 3-D shell bodies. This
                    allows different GCDEF specifications for different
                    portions of the assembly.

            PART - Assign a different section ID and contact element type ID for every general
                   surface which covers a physical part. Compared to the SPLIT
                   option, this option produces fewer unique section IDs, which
                   can make it easier to specify interactions via GCDEF.
                   However, it may also result in a less accurate and/or less
                   efficient solution.

        selopt
            Key that controls which base elements are considered for general
            contact.

            ATTACH - Use a recursive adjacency selection to obtain complete physical parts, starting
                     from the selected base elements, before generating general
                     contact elements (default).

            SELECT - Use only the initially selected base elements to generate general contact
                     elements.

        Notes
        -----
        GCGEN creates general contact elements on the exterior faces of
        selected base elements. The base elements can be 2-D or 3-D solids, 2-D
        beams (top and bottom), or 3-D shells (top and bottom). The contact
        element types can be CONTA172, CONTA174, and/or CONTA177, depending
        upon the types of base elements in the model and the specified GCGEN
        options. General contact elements are identified by a real constant ID
        equal to zero.

        You can control contact interactions between specific general contact
        surfaces that could potentially be in contact by using the GCDEF
        command. See General Contact in the Contact Technology Guide for more
        information on the overall procedure to create general contact.

        Understanding FeatureANGLE

        The exterior facets of the selected base solid and shell elements are
        divided into subsets based on the angle between the normals of
        neighboring faces. On a flat or smooth surface, adjacent exterior
        element faces have normals that are parallel or nearly parallel; that
        is, the angle between the adjacent normals is near zero degrees.

        When the angle between the normals of two adjacent faces is greater
        than FeatureANGLE, the two faces are considered to be on two separate
        surfaces (SplitKey = SPLIT). The edge between the faces may be convex
        or concave. A convex (or outside) edge is considered to be a feature
        edge and may be affected by the EdgeKEY setting. For more information,
        see Feature Angle (FeatureANGLE) in the Contact Technology Guide.
        """
        command = f"GCGEN,{option},{featureangle},{edgekey},{splitkey},{selopt}"
        return self.run(command, **kwargs)

    def inistate(
        self,
        action="",
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
        """Defines initial state data and parameters.

        APDL Command: INISTATE

        Parameters
        ----------
        action
            Specifies action for defining or manipulating initial state data:

            SET - Use Action = SET to designate initial state coordinate system, data type, and
                  material type parameters. See "Command Specification for
                  Action = SET".

            DEFINE - Use Action = DEFINE to specify the actual state values, and the corresponding
                     element, integration point, or layer information. See
                     "Command Specifications for Action = DEFINE".

            WRITE - Use Action = WRITE to write the initial state values to a file when the SOLVE
                    command is issued. See "Command Specifications for Action =
                    WRITE".

            READ - Use Action = READ to read the initial state values from a file. See "Command
                   Specifications for Action = READ".

            LIST - Use Action = LIST  to read out the initial state data. See "Command
                   Specifications for Action = LIST".

            DELETE - Use Action = DELE to delete initial state data from a selected set of elements.
                     See "Command Specifications for Action = DELETE"

        val1, val2, ..., val9
            Input values based on the Action type.

        Notes
        -----
        The INISTATE command is available for current-technology elements.
        Initial state supported for a given element is indicated in the
        documentation for the element under "Special Features."

        The command is not for use with kinematic hardening material properties
        (TB,BKIN, TB,KINH, TB,PLAS,,,,KINH) or the shape memory alloy material
        model (TB,SMA).

        INISTATE with elastic strain alone is not supported for gasket
        materials (TB,GASK) and hyperelastic materials (TB,HYPER, TB,BB,
        TB,AHYPER, TB,CDM, TB,EXPE).

        INISTATE with initial stress alone is not supported for gasket
        materials (TB,GASK).

        INISTATE with plastic strain (which must include initial strain or
        stress, plastic strain, and accumulated plastic strain) does not
        support gasket materials (TB,GASK), porous media (TB,PM), rate-
        dependent plasticity (TB,RATE), and viscoplasticity (TB,PRONY,
        TB,SHIFT).

        For detailed information about using the initial state capability, see
        Initial State in the Basic Analysis Guide.
        """
        command = f"INISTATE,{action},{val1},{val2},{val3},{val4},{val5},{val6},{val7},{val8},{val9}"
        return self.run(command, **kwargs)

    def laylist(self, iel="", layr1="", layr2="", mplab1="", mplab2="", **kwargs):
        """Lists real constants material properties for layered elements.

        APDL Command: LAYLIST

        Parameters
        ----------
        iel
            Element number to be listed.  If ALL, list all selected elements
            [ESEL] of the appropriate type.  If blank and the current element
            type is a layered element type, list data from the current real
            constant table in the layered format.

        layr1, layr2
            Range of layer numbers to be listed.  If LAYR1 is greater than
            LAYR2, a reverse order list is produced.  LAYR1 defaults to 1.
            LAYR2 defaults to LAYR1 if LAYR1 is input or to the number of
            layers if LAYR1 is not input.

        mplab1, mplab2
            Material property labels (e.g., EX) to be listed along with the
            layer real constants.

        Notes
        -----
        Lists real constants and any two material properties for layered shell
        and solid elements.

        If matrix input is selected (KEYOPT(2) = 2 or 3), LAYR1, LAYR2, Mplab1,
        and Mplab2 are not used.

        This command is valid in any processor.
        """
        command = f"LAYLIST,{iel},{layr1},{layr2},{mplab1},{mplab2}"
        return self.run(command, **kwargs)

    def layplot(self, iel="", layr1="", layr2="", **kwargs):
        """Displays the layer stacking sequence for layered elements.

        APDL Command: LAYPLOT

        Parameters
        ----------
        iel
            Element number for the display.  If blank and the current element
            type is a layered element type, display data from the current real
            constant table.

        layr1, layr2
            Range of layer numbers to be displayed.  If LAYR1 is greater than
            LAYR2, a reversed order display is produced.  Up to 20 layers may
            be displayed at a time.  LAYR1 defaults to 1. LAYR2 defaults to
            LAYR1 if LAYR1 is input or to the number of layers (or to 19+LAYR1,
            if smaller) if LAYR1 is not input.

        Notes
        -----
        Displays the layer-stacking sequence as defined in the real constant
        table for layered shell and solid elements in a form where the layers
        are visible (like a sheared deck of cards).

        The element x-axis is shown as 0.0 degrees.

        Layers are cross-hatched and color-coded for clarity. The hatch lines
        indicate the layer angle (real constant THETA) and the color coding is
        for material identification (real constant MAT).

        The actual orientation of a specific layer in three-dimensional space
        can be seen using /PSYMB,LAYR. To use /PSYMB,LAYR with smeared
        reinforcing elements (REINF265), first set the vector-mode graphics
        option (/DEVICE,VECTOR,1).

        Layer thickness can be displayed using the /ESHAPE and EPLOT commands.

        This command is valid in any processor.
        """
        command = f"LAYPLOT,{iel},{layr1},{layr2}"
        return self.run(command, **kwargs)

    def lfsurf(self, sline="", tline="", **kwargs):
        """Generates surface elements overlaid on the edge of existing solid

        APDL Command: LFSURF
        elements and assigns the extra node as the closest fluid element node.

        Parameters
        ----------
        sline
            Component name for the surface lines of the meshed solid areas.

        tline
            Component name for the target lines meshed with fluid elements.

        Notes
        -----
        This command macro is used to generate surface effect elements overlaid
        on the surface of existing plane elements and, based on proximity, to
        determine and assign the extra node for each surface element.  The
        underlying areas of the solid region and the fluid lines must be meshed
        prior to calling this command macro. The active element type must be
        SURF151 with appropriate settings for KEYOPT(4), KEYOPT(5), KEYOPT(6),
        and KEYOPT(8).

        The surface lines of the solid and the target lines of the fluid are
        grouped into components and named using the CM command.  The names must
        be enclosed in single quotes (e.g., 'SLINE') when the LFSURF command is
        manually typed in.

        When using the GUI method, node and element components are created
        through the picking dialog boxes associated with this command.

        The macro is applicable for the SURF151 and FLUID116 element types.
        """
        command = f"LFSURF,{sline},{tline}"
        return self.run(command, **kwargs)

    def ndsurf(self, snode="", telem="", dimn="", **kwargs):
        """Generates surface elements overlaid on the edge of existing elements

        APDL Command: NDSURF
        and assigns the extra node as the closest fluid element node.

        Parameters
        ----------
        snode
            Component name for the surface nodes of the solid elements.

        telem
            Component name for the target fluid elements.

        dimn
            Model dimensionality:

            2 - 2-D model.

            3 - 3-D model.

        Notes
        -----
        This command macro is used to generate surface effect elements (SURF151
        or SURF152) overlaid on the surface of existing plane or solid elements
        and, based on proximity, to determine and assign the extra node
        (FLUID116) for each surface element. The active element type must be
        SURF151 or SURF152 with appropriate settings for KEYOPT(4), KEYOPT(5),
        KEYOPT(6), and KEYOPT(8).

        The surface nodes of the plane or solid elements must be grouped into a
        node component and the fluid elements must be grouped into an element
        component and named using the CM command.  The names must be enclosed
        in single quotes (e.g., 'NOD') when the NDSURF command is manually
        typed in.

        When using the GUI method, node and element components are created
        through the picking dialog boxes associated with this command.

        The macro is applicable for the SURF151, SURF152, and FLUID116 element
        types.
        """
        command = f"NDSURF,{snode},{telem},{dimn}"
        return self.run(command, **kwargs)

    def shsd(self, rid="", action="", **kwargs):
        """Creates or deletes a shell-solid interface to be used in shell-to-solid assemblies.

        APDL Command: SHSD

        Parameters
        ----------
        rid
            The real constant set ID that identifies the contact pair on
            which a shell-to-solid assembly is defined. If ALL, all
            selected contact pairs will be considered for assembly.

        Action
            * ``"CREATE"`` : Builds new shell and contact elements to be
              used in shell-to-solid assemblies (default). New elements
              are stored as internally-created components.

            * ``"DELETE"`` : Deletes the nodes and elements created during
              a previous execution of SHSD,RID,CREATE for the real
              constant set identified by RID.

        Notes
        -----
        The SHSD command creates a shell-solid interface to be used in
        shell-to-solid assemblies, or deletes a previously-created
        shell-solid interface. “Virtual” shell elements and additional
        CONTA175 elements are created at the contact pair identified by
        RID when Action = CREATE. Set Action = DELETE to remove the
        generated nodes and elements at the contact pair identified by
        RID.

        For further details, see:
        https://www.mm.bme.hu/~gyebro/files/ans_help_v182/ans_cmd/Hlp_C_SHSD.html

        """
        return self.run(f"SHSD,{rid},{action}", **kwargs)

    def swadd(
        self,
        ecomp="",
        shrd="",
        ncm1="",
        ncm2="",
        ncm3="",
        ncm4="",
        ncm5="",
        ncm6="",
        ncm7="",
        ncm8="",
        ncm9="",
        **kwargs,
    ):
        """Adds more surfaces to an existing spot weld set.

        APDL Command: SWADD

        Parameters
        ----------
        ecomp
            Name of an existing spot weld set that was previously defined using
            SWGEN.

        shrd
            Search radius. Defaults to 4 times the spot weld radius defined for
            the spot weld set (SWRD on SWGEN).

        ncm1, ncm2, ncm3, . . . , ncm9
            Surfaces to be added to the spot weld set. Each surface can be
            input as a predefined node component or a meshed area number.

        Notes
        -----
        This command adds surfaces to an existing spot weld set defined by the
        SWGEN command. You can add additional surfaces by repeating the SWADD
        command. However, the maximum number of allowable surfaces (including
        the 2 surfaces used for the original set defined by SWGEN) for each
        spot weld set is 11. See Adding Surfaces to a Basic Set for more
        information.
        """
        command = f"SWADD,{ecomp},{shrd},{ncm1},{ncm2},{ncm3},{ncm4},{ncm5},{ncm6},{ncm7},{ncm8},{ncm9}"
        return self.run(command, **kwargs)

    def swdel(self, ecomp="", **kwargs):
        """Deletes spot weld sets.

        APDL Command: SWDEL

        Parameters
        ----------
        ecomp
            Name of an existing spot weld set that was previously defined using
            SWGEN. If Ecomp = ALL (default) all spot welds are deleted.

        Notes
        -----
        This command deletes spot weld sets previously defined by the SWGEN
        command.
        """
        command = f"SWDEL,{ecomp}"
        return self.run(command, **kwargs)

    def swgen(
        self,
        ecomp="",
        swrd="",
        ncm1="",
        ncm2="",
        snd1="",
        snd2="",
        shrd="",
        dirx="",
        diry="",
        dirz="",
        itty="",
        icty="",
        **kwargs,
    ):
        """Creates a new spot weld set.

        APDL Command: SWGEN

        Parameters
        ----------
        ecomp
            Name to identify the new spot weld. This name will be used for the
            element component containing the new contact, target, and beam
            elements generated for the spot weld set.

        swrd
            Spot weld radius.

        ncm1
            Name of a component containing nodes on the first spot weld
            surface, or a meshed area number for the surface.

        ncm2
            Name of a component containing nodes on the second spot weld
            surface, or a meshed area number for the surface.

        snd1
            Node number of the first spot weld node corresponding to the first
            surface (NCM1). This node can be on or close to the first surface.

        snd2
            Node number of the second spot weld node corresponding to the
            second surface (NCM2).  This node can be on or close to the second
            surface. ANSYS will create the node if it is not specified.

        shrd
            Search radius. Defaults to 4 times the spot weld radius SWRD.

        dirx, diry, dirz
            Spot weld projection direction in terms of normal X, Y, and Z
            components.

        itty
            Target element type ID.

        icty
            Contact element type ID.

        Notes
        -----
        This command creates a new spot weld set. You can add more surfaces to
        the set using SWADD after the initial SWGEN command. However, the
        maximum number of allowable surfaces (including the 2 surfaces used for
        the original set) for each spot weld set is 11.

        Ecomp, SWRD, NCM1, NCM2, and SND1 must be specified. SND2, SHRD, DIRX,
        DIRY, DIRZ, ITTY, ICTY are optional inputs. If the second spot weld
        node (SND2) is specified, that node is used to determine the spot weld
        projection direction, andDIRX, DIRY and DIRZ are ignored.

        If ITTY is specified, the following corresponding target element key
        option must be set: KEYOPT(5) = 4. If ICTY is specified, the following
        corresponding contact element key options must be set: KEYOPT(2) = 2,
        KEYOPT(12) = 5.

        Use the SWLIST and SWDEL commands to list or delete spot welds. See
        Creating a Basic Spot Weld Set with SWGEN for detailed information on
        defining spot welds.
        """
        command = f"SWGEN,{ecomp},{swrd},{ncm1},{ncm2},{snd1},{snd2},{shrd},{dirx},{diry},{dirz},{itty},{icty}"
        return self.run(command, **kwargs)

    def swlist(self, ecomp="", **kwargs):
        """Lists spot weld sets.

        APDL Command: SWLIST

        Parameters
        ----------
        ecomp
            Name of an existing spot weld set that was previously defined using
            SWGEN. If Ecomp = ALL (default), all spot weld sets are listed.

        Notes
        -----
        This command lists spot weld node, beam, and contact pair information
        for all defined spot weld sets, or for the specified set. To ensure
        that all defined spotwelds are listed, issue CMSEL,ALL (to select all
        components) before issuing the SWLIST command.

        When SWLIST is issued in POST1, the beam forces and moments are output.
        For the case of a deformable spot weld, the stresses are also output in
        the beam local coordinate system.
        """
        command = f"SWLIST,{ecomp}"
        return self.run(command, **kwargs)

    def tshap(self, shape="", **kwargs):
        """Defines simple 2-D and 3-D geometric surfaces for target segment

        APDL Command: TSHAP
        elements.

        Parameters
        ----------
        shape
            Specifies the geometric shapes for target segment elements TARGE169
            and TARGE170.

            LINE - Straight line (2-D, 3-D) (Default for 2-D)

            PARA - Parabola (2-D, 3-D)

            ARC - Clockwise arc (2-D)

            CARC - Counterclockwise arc (2-D)

            CIRC - Complete circle (2-D)

            TRIA - Three-node triangle (3-D) (Default for 3-D)

            TRI6 - Six-node triangle (3-D)

            QUAD - Four-node quadrilateral (3-D)

            QUA8 - Eight-node quadrilateral (3-D)

            CYLI - Cylinder (3-D)

            CONE - Cone (3-D)

            SPHE - Sphere (3-D)

            PILO - Pilot node (2-D, 3-D)

            POINT - Point (rigid surface node) (2-D, 3-D)

        Notes
        -----
        Use this command to specify the target segment shapes for the rigid
        target surface associated with surface-to-surface contact (TARGE169,
        CONTA171, CONTA172 (2-D) and TARGE170, CONTA173, CONTA174 (3-D)), 3-D
        beam-to-beam contact (TARGE170 and CONTA176), and 3-D line-to-surface
        contact (TARGE170 and CONTA177).  Once you issue TSHAP, all subsequent
        target elements generated via the direct element generation technique
        will have the same shape, until you issue TSHAP again with a different
        Shape value.
        """
        command = f"TSHAP,{shape}"
        return self.run(command, **kwargs)

    def upgeom(self, factor="", lstep="", sbstep="", fname="", ext="", **kwargs):
        """Adds displacements from a previous analysis and updates the geometry of

        APDL Command: UPGEOM
        the finite element model to the deformed configuration.

        Parameters
        ----------
        factor
            Multiplier for displacements being added to coordinates.  The value
            1.0 will add the full value of the displacements to the geometry of
            the finite element model.  Defaults to 1.0.

        lstep
            Load step number of data to be imported.  Defaults to the last load
            step.

        sbstep
            Substep number of data to be imported.  Defaults to the last
            substep.

        fname
            File name and directory path (248 characters maximum, including the
            characters needed for the directory path).  An unspecified
            directory path defaults to the working directory; in this case, you
            can use all 248 characters for the file name.

        ext
            Filename extension (eight-character maximum).

        Notes
        -----
        This command updates the geometry of the finite element model according
        to the displacement results of the previous analysis and creates a
        revised geometry at the deformed configuration.  This command works on
        all nodes (default) or on a selected set of nodes.  If this command is
        issued repeatedly, it creates a revised geometry of the finite element
        model in a cumulative fashion, i.e., it adds displacement results on
        the previously generated deformed geometry. The solid model geometry is
        not updated by this command.

        When UPGEOM is issued, the current finite element model is overwritten
        by finite element information from the results file. For this reason,
        it is important that the finite element information in the results file
        matches the finite element model in which the nodal coordinates are
        being updated. No changes should be made to the model before the UPGEOM
        command is issued.
        """
        command = f"UPGEOM,{factor},{lstep},{sbstep},{fname},{ext}"
        return self.run(command, **kwargs)

    def usrdof(
        self,
        action="",
        dof1="",
        dof2="",
        dof3="",
        dof4="",
        dof5="",
        dof6="",
        dof7="",
        dof8="",
        dof9="",
        dof10="",
        **kwargs,
    ):
        """Specifies the degrees of freedom for the user-defined element USER300.

        APDL Command: USRDOF

        Parameters
        ----------
        action
            One of the following command operations:

            DEFINE - Specify the degrees of freedom (DOFs). This value is the default.

            LIST - List all previously specified DOFs.

            DELETE -  Delete all previously specified DOFs.

        dof1, dof2, dof3, . . . , dof10
            The list of DOFs.

        Notes
        -----
        The USRDOF command specifies the degrees of freedom for the user-
        defined element USER300.

        Although you can intersperse other commands as necessary for your
        analysis, issue the USRDOF command as part of the following general
        sequence of commands:

        Issue the ET command for element USER300, followed by the related TYPE
        command.

        Issue both the USRELEM and USRDOF commands (in either order).

        Define your element using USER300.

        The DOF list (DOF1 through DOF10) can consist of up to 10 DOFs. Use any
        valid and appropriate DOF (such as UX, UY, UZ, ROTX, ROTY, ROTZ, AX,
        AY, AZ, VX, VY, VZ, PRES, WARP, TEMP, VOLT, MAG, EMF, and CURR).

        You can specify a maximum of 10 DOFs per USRDOF command. To define
        additional DOFs, issue the command again.

        The maximum number of DOFs for a user-defined element--the number of
        nodes times the number of DOFs per node--cannot exceed 480.

        To learn more about user-defined elements, see Creating a New Element
        in the Programmer's Reference.
        """
        command = f"USRDOF,{action},{dof1},{dof2},{dof3},{dof4},{dof5},{dof6},{dof7},{dof8},{dof9},{dof10}"
        return self.run(command, **kwargs)

    def usrelem(
        self,
        nnodes="",
        ndim="",
        keyshape="",
        nreal="",
        nsavevars="",
        nrsltvar="",
        keyansmat="",
        nintpnts="",
        kestress="",
        keysym="",
        **kwargs,
    ):
        """Specifies the characteristics of the user-defined element USER300.

        APDL Command: USRELEM

        Parameters
        ----------
        nnodes
            The number of nodes.

        ndim
            The number of dimensions (of nodal coordinates). Valid values are 2
            or 3.

        keyshape
            One of the following element shape options:

            ANYSHAPE - Any shape (that is, no specified shape). This value is the default. (The ANSYS
                       MeshTool is unavailable.)

            POINT - Point.

            LINE - Straight line.

            TRIAN - Triangle.

            QUAD - Quadrilateral. This shape can be degenerated to a triangle.

            TET - Tetrahedron.

            BRICK - Brick. This shape can be degenerated to a wedge, pyramid, or tetrahedron.

        nreal
            The number of real constants.

        nsavevars
            The number of saved variables.

        nrsltvar
            The number of variables saved in results files.

        keyansmat
            Key for element formulation control:

            0 - Create your own material codes within the element formulation. In this case,
                the real constants are available to input material properties.
                You can also input linear material properties via MP and MPDATA
                commands .

            1 - Use ANSYS standard material routines or the USERMAT subroutine to form
                structural material data. ANSYS material properties must be
                input in the standard way (as you would for non-user-defined
                elements). This value is invalid when KeyShape = ANYSHAPE.

        nintpnts
            The maximum number of integration points (used when KEYANSMAT = 1).

        kestress
            Key for the element stress state (used when KEYANSMAT = 1):

            0 - Plane stress elements.

            1 - Axisymmetric elements.

            2 - Plane strain elements.

            3 - 3-D solid elements.

            4 - 3-D solid-shell elements.

            5 - Generalized plane strain elements.

            6 - Beam elements.

            7 - Link/truss elements.

            8 - 3-D shell elements.

            9 - Axisymmetric shell elements.

        keysym
            Key for specifying whether element stiffness matrices are symmetric
            or unsymmetric:

            0 - Symmetric.

            1 - Unsymmetric.

        Notes
        -----
        The USRELEM command specifies the characteristics of the user-defined
        element USER300.

        Although you can intersperse other commands as necessary for your
        analysis, issue the USRELEM command as part of the following general
        sequence of commands:

        Issue the ET command for element USER300, followed by the related TYPE
        command.

        Issue both the USRELEM and USRDOF commands (in either order).

        Define your element using USER300.

        The number of real constants (NREAL) can refer to geometry quantities,
        material quantities, or any parameters for element formulation.

        ANSYS saves variables in the .esav file to preserve element data when
        you specify a positive NSAVEVARS value. When KEYANSMAT = 0, all
        variables of both material and kinematic formulation are saved. When
        KEYANSMAT = 1, only the variables for kinematic formulation (such as
        deformation gradient tensor) are saved; in this case, the material
        routine saves all necessary material data automatically.

        Element data saved in results files (NRSLTVAR) are accessible only as
        nonsummable miscellaneous data.  ANSYS saves stress and total strain
        data for structural elements in the .rst file automatically (as it does
        for equivalent variables such as thermal gradient and thermal flux in
        thermal elements); therefore, NRSLTVAR does not need to include stress
        and total strain data.

        To learn more about creating user-defined elements, see Creating a New
        Element in the Programmer's Reference.
        """
        command = f"USRELEM,{nnodes},{ndim},{keyshape},{nreal},{nsavevars},{nrsltvar},{keyansmat},{nintpnts},{kestress},{keysym}"
        return self.run(command, **kwargs)

    def wtbcreate(self, iel="", node="", damp="", **kwargs):
        """Creates a USER300 element to model the turbine for full aeroelastic

        APDL Command: WTBCREATE
        coupling analysis and specifies relevant settings for the analysis.

        Parameters
        ----------
        iel
            Element number (next available number by default).

        node
            Node number connecting support structure and turbine.

        damp
            Damping option for the turbine:

            0 - Damping matrix obtained from the aeroelastic code plus Rayleigh damping
                (default).

            1 - Rayleigh damping only.

            2 - Damping from the aeroelastic code only.

        Notes
        -----
        WTBCREATE invokes a predefined ANSYS macro that will automatically
        generate a turbine element and issue relevant data commands that are
        necessary to run a full aeroelastic coupling analysis. For detailed
        information on how to perform a fully coupled aeroelastic analysis, see
        Fully Coupled Wind Turbine Example in Mechanical APDL in the Mechanical
        APDL Programmer's Reference.

        The generated USER300 turbine element will have 9 nodes with node
        numbers NODE, NMAX+1, NMAX+2, ..., NMAX+8, where NMAX is the maximum
        node number currently in the model.

        There are 6 freedoms on the first node of the element: UX, UY, UZ,
        ROTX, ROTY, ROTZ, and these are true structural freedoms. For all the
        other nodes (i.e., nodes 2 to 9), only the translational freedoms (UX,
        UY, UZ) are used. These are generalized freedoms that are internal to
        the turbine element and are used by the aeroelastic code only.

        The element type integer of the USER300 element is the current maximum
        element type integer plus one.

        The command will also set up the analysis settings appropriate for a
        full aeroelastic coupling analysis. These include full Newton-Raphson
        solution (NROPT,FULL) and a USRCAL command to activate the relevant
        user routines.
        """
        command = f"WTBCREATE,{iel},{node},{damp}"
        return self.run(command, **kwargs)
