class ConstraintEquations:
    def ce(
        self,
        neqn="",
        const="",
        node1="",
        lab1="",
        c1="",
        node2="",
        lab2="",
        c2="",
        node3="",
        lab3="",
        c3="",
        **kwargs,
    ):
        """Defines a constraint equation relating degrees of freedom.

        APDL Command: CE

        Parameters
        ----------
        neqn
            Set equation reference number:

            n - Arbitrary set number.

            HIGH - The highest defined constraint equation number. This option is especially
                   useful when adding nodes to an existing set.

            NEXT - The highest defined constraint equation number plus one. This option
                   automatically numbers coupled sets so that existing sets are
                   not modified.

        const
            Constant term of equation.

        node1
            Node for first term of equation.  If -NODE1, this term is deleted
            from the equation.

        lab1
            Degree of freedom label for first term of equation.  Structural
            labels:  UX, UY, or UZ (displacements); ROTX, ROTY, or ROTZ
            (rotations, in radians).  Thermal labels: TEMP, TBOT, TE2, TE3, . .
            ., TTOP (temperature).  Electric labels:  VOLT (voltage).  Magnetic
            labels:  MAG (scalar magnetic potential); AX, AY, or AZ (vector
            magnetic potentials). Diffusion label: CONC (concentration).

        c1
            Coefficient for first node term of equation.  If zero, this term is
            ignored.

        node2, lab2, c2
            Node, label, and coefficient for second term.

        node3, lab3, c3
            Node, label, and coefficient for third term.

        Notes
        -----
        Repeat the CE command to add additional terms to the same equation.  To
        change only the constant term, repeat the command with no node terms
        specified.  Only the constant term can be changed during solution, and
        only with the CECMOD command.

        Linear constraint equations may be used to relate the degrees of
        freedom of selected nodes in a more general manner than described for
        nodal coupling [CP].  The constraint equation is of the form:

        where U(I) is the degree of freedom (displacement, temperature, etc.)
        of term (I).  The following example is a set of two constraint
        equations, each containing three terms:

        0.0 = 3.0* (1 UX) + 3.0* (4 UX) + (-2.0)* (4 ROTY)

        2.0 = 6.0* (2 UX) + 10.0* (4 UY) + 1.0* (3 UZ)

        The first unique degree of freedom in the equation is eliminated in
        terms of all other degrees of freedom in the equation.  A unique degree
        of freedom is one which is not specified in any other constraint
        equation, coupled node set, specified displacement set, or master
        degree of freedom set.  It is recommended that the first term of the
        equation be the degree of freedom to be eliminated.  The first term of
        the equation cannot contain a master degree of freedom, and no term can
        contain coupled degrees of freedom.  The same degree of freedom may be
        specified in more than one equation but care must be taken to avoid
        over-specification (over-constraint).

        The degrees of freedom specified in the equation (i.e., UX, UY, ROTZ,
        etc.) must also be included in the model (as determined from the
        element types [ET]).  Also, each node in the equation must be defined
        on an element (any element type containing that degree of freedom will
        do).

        For buckling and modal analyses, the constant term of the equation will
        not be taken into account (that is, CONST is always zero).

        Note that under certain circumstances a constraint equation generated
        by CE may be modified during the solution. See Program Modification of
        Constraint Equations for more information.
        """
        command = f"CE,{neqn},{const},{node1},{lab1},{c1},{node2},{lab2},{c2},{node3},{lab3},{c3}"
        return self.run(command, **kwargs)

    def cecyc(
        self,
        lowname="",
        highname="",
        nsector="",
        hindex="",
        tolerance="",
        kmove="",
        kpairs="",
        **kwargs,
    ):
        """Generates the constraint equations for a cyclic symmetry analysis

        APDL Command: CECYC

        Parameters
        ----------
        lowname
            Name of a component for the nodes on the low angle edge of the
            sector.  Enclosed in single quotes.

        highname
            Name of a component for the nodes on the high angle edge of the
            sector.  Enclosed in single quotes.

        nsector
            Number of sectors in the complete 360 degrees.

        hindex
            Harmonic index to be represented by this set of constraint
            equations.  If Hindex is -1, generate constraint equations for
            static cyclic symmetry.  If HIndex is -2, generate constraint
            equations for static cyclic asymmetry.

        tolerance
            A positive tolerance is an absolute tolerance (length units), and a
            negative tolerance is a tolerance relative to the local element
            size.

        kmove
            0

            0 - Nodes are not moved.

            1 - HIGHNAME component nodes are moved to match LOWNAME component nodes exactly.

        kpairs
            0

            0 - Do not print paired nodes

            1 - Print table of paired nodes

        Notes
        -----
        The analysis can be either modal cyclic symmetry or static cyclic
        symmetry.

        The pair of nodes for which constraint equations are written are
        rotated into CSYS,1.
        """
        command = f"CECYC,{lowname},{highname},{nsector},{hindex},{tolerance},{kmove},{kpairs}"
        return self.run(command, **kwargs)

    def cedele(self, neqn1="", neqn2="", ninc="", nsel="", **kwargs):
        """Deletes constraint equations.

        APDL Command: CEDELE

        Parameters
        ----------
        neqn1, neqn2, ninc
            Delete constraint equations from NEQN1 to NEQN2 (defaults to NEQN1)
            in steps of NINC (defaults to 1).  If NEQN1 = ALL, NEQN2  and NINC
            will be ignored all constraint equations will be deleted.

        nsel
            Additional node selection control:

            ANY  - Delete equation set if any of the selected nodes are in the set (default).

            ALL  - Delete equation set only if all of the selected nodes are in the set.
        """
        command = f"CEDELE,{neqn1},{neqn2},{ninc},{nsel}"
        return self.run(command, **kwargs)

    def ceintf(
        self,
        toler="",
        dof1="",
        dof2="",
        dof3="",
        dof4="",
        dof5="",
        dof6="",
        movetol="",
        **kwargs,
    ):
        """Generates constraint equations at an interface.

        APDL Command: CEINTF

        Parameters
        ----------
        toler
            Tolerance about selected elements, based on a fraction of the
            element dimension (defaults to 0.25 (25%)).  Nodes outside the
            element by more than the tolerance are not accepted as being on the
            interface.

        dof1, dof2, dof3, . . . , dof6
            Degrees of freedom for which constraint equations are written.
            Defaults to all applicable DOFs.  DOF1 accepts ALL as a valid
            label, in which case the rest are ignored (all DOFs are applied).

        movetol
            The allowed "motion" of a node (see Note below).  This distance is
            in terms of the element coordinates (-1.0 to 1.0).  A typical value
            is 0.05.  Defaults to 0 (do not move).  MoveTol must be less than
            or equal to TOLER.

        Notes
        -----
        This command can be used to "tie" together two regions with dissimilar
        mesh patterns by generating constraint equations that connect the
        selected nodes of one region to the selected elements of the other
        region.  At the interface between regions, nodes should be selected
        from the more dense mesh region, A, and the elements selected from the
        less dense mesh region, B.  The degrees of freedom of region A nodes
        are interpolated with the corresponding degrees of freedom of the nodes
        on the region B elements, using the shape functions of the region B
        elements.  Constraint equations are then written that relate region A
        and B nodes at the interface.

        The MoveTol field lets the nodes in the previously mentioned region A
        change coordinates when slightly inside or outside the elements of
        region B.  The change in coordinates causes the nodes of region A to
        assume the same surface as the nodes associated with the elements of
        region B.   The constraint equations that relate the nodes at both
        regions of the interface are then written.

        Solid elements with six degrees of freedom should only be interfaced
        with other six degree-of-freedom elements.  The region A nodes should
        be near the region B elements.   A location tolerance based on the
        smallest region B element length may be input.  Stresses across the
        interface are not necessarily continuous.  Nodes in the interface
        region should not have specified constraints.

        Use the CPINTF command to connect nodes by coupling instead of
        constraint equations.  Use the EINTF command to connect nodes by line
        elements.  See also the NSEL and ESEL commands for selecting nodes and
        elements.  See the Mechanical APDL Theory Reference for a description
        of 3-D space used to determine if a node will be considered by this
        command.

        As an alternative to the CEINTF command, you can use contact elements
        and the internal multipoint constraint (MPC) algorithm to tie together
        two regions having dissimilar meshes. See Solid-Solid and Shell-Shell
        Assemblies for more information.
        """
        command = f"CEINTF,{toler},{dof1},{dof2},{dof3},{dof4},{dof5},{dof6},{movetol}"
        return self.run(command, **kwargs)

    def celist(self, neqn1="", neqn2="", ninc="", option="", **kwargs):
        """Lists the constraint equations.

        APDL Command: CELIST

        Parameters
        ----------
        neqn1, neqn2, ninc
            List constraint equations from NEQN1 to NEQN2 (defaults to NEQN1)
            in steps of NINC (defaults to 1).  If NEQN1 = ALL (default), NEQN2
            and NINC are ignored and all constraint equations are listed.

        option
            Options for listing constraint equations:

            ANY - List equation set if any of the selected nodes are in the set (default). Only
                  externally-generated constraint equations are listed.

            ALL - List equation set only if all of the selected nodes are in the set. Only
                  externally-generated constraint equations are listed.

            INTE - List internally-generated constraint equations that are associated with MPC-
                   based contact. Constraint equations are listed only if all
                   the nodes in the set are selected.

            CONV - Convert internal constraint equations to external constraint equations.
                   Internal constraint equations are converted only if all of
                   the nodes in the set are selected.

        Notes
        -----
        This command is valid in any processor. However, the INTE and CONV
        options are only valid in the Solution processor after a SOLVE command
        has been issued.
        """
        command = f"CELIST,{neqn1},{neqn2},{ninc},{option}"
        return self.run(command, **kwargs)

    def cerig(
        self,
        maste="",
        slave="",
        ldof="",
        ldof2="",
        ldof3="",
        ldof4="",
        ldof5="",
        **kwargs,
    ):
        """Defines a rigid region.

        APDL Command: CERIG

        Parameters
        ----------
        maste
            Retained (or master) node for this rigid region.  If MASTE = P,
            then graphical picking of the master and slave nodes is enabled
            (first node picked will be the master node, and subsequent nodes
            picked will be slave  nodes), and subsequent fields are ignored
            (valid only in GUI).

        slave
            Removed (or slave) node for this rigid region.  If ALL, slave nodes
            are all selected nodes.

        ldof
            Degrees of freedom associated with equations:

            ALL - All applicable degrees of freedom (default).  If 3-D, generate 6 equations
                  based on UX, UY, UZ, ROTX, ROTY, ROTZ;  if 2-D, generate 3
                  equations based on UX, UY, ROTZ.

            UXYZ - Translational degrees of freedom.  If 3-D, generate 3 equations based on the
                   slave nodes' UX, UY, and UZ DOFs and the master node's UX,
                   UY, UZ, ROTX, ROTY, and ROTZ DOFs;  if 2-D, generate 2
                   equations based on the slave nodes UX and UY DOFs and the
                   master nodes UX, UY, and ROTZ DOFs.  No equations are
                   generated for the rotational coupling.

            RXYZ - Rotational degrees of freedom.  If 3-D, generate 3 equations based on ROTX,
                   ROTY, ROTZ;  if 2-D, generate 1 equation based on ROTZ.  No
                   equations are generated for the translational coupling.

            UX - Slave translational UX degree of freedom only.

            UY - Slave translational UY degree of freedom only.

            UZ - Slave translational UZ degree of freedom only.

            ROTX - Slave rotational ROTX degree of freedom only.

            ROTY - Slave rotational ROTY degree of freedom only.

            ROTZ - Slave rotational ROTZ degree of freedom only.

        ldof2, ldof3, ldof4, ldof5
            Additional degrees of freedom.  Used only if more than one degree
            of freedom required and Ldof is not ALL, UXYZ, or RXYZ.

        Notes
        -----
        Defines a rigid region (link, area or volume) by automatically
        generating constraint equations to relate nodes in the region.  Nodes
        in the rigid region must be assigned a geometric location before this
        command is used.  Also, nodes must be connected to elements having the
        required degree of freedom set (see Ldof above).  Generated constraint
        equations are based on small deflection theory.  Generated constraint
        equations are numbered beginning from the highest previously defined
        equation number (NEQN) plus 1.  Equations, once generated, may be
        listed [CELIST] or modified [CE] as desired.  Repeat CERIG command for
        additional rigid region equations.

        This command will generate the constraint equations needed for defining
        rigid lines in 2-D or 3-D space.  Multiple rigid lines relative to a
        common point are used to define a rigid area or a rigid volume.  In 2-D
        space, with Ldof = ALL, three equations are generated for each pair of
        constrained nodes.  These equations define the three rigid body motions
        in global Cartesian space, i.e., two in-plane translations and one in-
        plane rotation.  These equations assume the X-Y plane to be the active
        plane with UX, UY, and ROTZ degrees of freedom available at each node.
        Other types of equations can be generated with the appropriate Ldof
        labels.

        Six equations are generated for each pair of constrained nodes in 3-D
        space (with Ldof = ALL).  These equations define the six rigid body
        motions in global Cartesian space.  These equations assume that UX, UY,
        UZ, ROTX, ROTY, and ROTZ degrees of freedom are available at each node.

        The UXYZ label allows generating a partial set of rigid region
        equations.  This option is useful for transmitting the bending moment
        between elements having different degrees of freedom at a node.  With
        this option only two of the three equations are generated for each pair
        of constrained nodes in 2-D space.  In 3-D space, only three of the six
        equations are generated.  In each case the rotational coupling
        equations are not generated.  Similarly, the RXYZ label allows
        generating a partial set of equations with the translational coupling
        equations omitted.

        Applying this command to a large number of slave nodes may result in
        constraint equations with a large number of coefficients. This may
        significantly increase the peak memory required during the process of
        element assembly. If real memory or virtual memory is not available,
        consider reducing the number of slave nodes.

        Note that under certain circumstances the constraint equations
        generated by CERIG may be modified during the solution. See Program
        Modification of Constraint Equations for more information.

        As an alternative to the CERIG command, you can define a similar type
        of rigid region using contact elements and the internal multipoint
        constraint (MPC) algorithm. See Surface-Based Constraints for more
        information.

        CERIG cannot be deleted using CEDELE,ALL and then regenerated in the
        second or higher load steps if the LSWRITE  and LSSOLVE procedure is
        used. CERIG writes constraint equations directly into load step files.
        Deleting constraint equations (CEDELE,ALL) cannot always maintain the
        consistency among load steps.
        """
        command = f"CERIG,{maste},{slave},{ldof},{ldof2},{ldof3},{ldof4},{ldof5}"
        return self.run(command, **kwargs)

    def cesgen(self, itime="", inc="", nset1="", nset2="", ninc="", **kwargs):
        """Generates a set of constraint equations from existing sets.

        APDL Command: CESGEN

        Parameters
        ----------
        itime, inc
            Do this generation operation a total of ITIMEs, incrementing all
            nodes in the existing sets by INC each time after the first.  ITIME
            must be >1 for generation to occur.

        nset1, nset2, ninc
            Generate sets from sets beginning with NSET1 to NSET2 (defaults to
            NSET1) in steps of NINC (defaults to 1).  If NSET1 is negative,
            NSET2 and NINC are ignored and the last ``|NSET1|`` sets (in sequence
            from maximum set number) are used as the sets to be repeated.

        Notes
        -----
        Generates additional sets of constraint equations (with same labels)
        from existing sets.  Node numbers between sets may be uniformly
        incremented.
        """
        command = f"CESGEN,{itime},{inc},{nset1},{nset2},{ninc}"
        return self.run(command, **kwargs)

    def rbe3(self, master="", dof="", slaves="", wtfact="", **kwargs):
        """Distributes the force/moment applied at the master node to a set  of

        APDL Command: RBE3
        slave nodes, taking into account the geometry of the slave nodes as
        well as weighting factors.

        Parameters
        ----------
        master
            Node at which the force/moment to be distributed will be applied.
            This node must be associated with an element for the master node to
            be included in the DOF solution.

        dof
            Refers to the master node degrees of freedom to be used in
            constraint equations. Valid labels are: UX, UY, UZ, ROTX, ROTY,
            ROTZ, UXYZ, RXYZ, ALL

        slaves
            The name of an array parameter that contains a list of slave nodes.
            Must specify the starting index number. ALL can be used for
            currently selected set of nodes. The slave nodes may not be
            colinear, that is, not be all located on the same straight line
            (see Notes below).

        wtfact
            The name of an array parameter that contains a list of weighting
            factors corresponding to each slave node above. Must have the
            starting index number. If not specified, the weighting factor for
            each slave node defaults to 1.

        Notes
        -----
        The force is distributed to the slave nodes proportional to the
        weighting factors. The moment is distributed as forces to the slaves;
        these forces are proportional to the distance from the center of
        gravity of the slave nodes times the weighting factors.  Only the
        translational degrees of freedom of the slave nodes are used for
        constructing the constraint equations. Constraint equations are
        converted to distributed forces/moments on the slave nodes during
        solution.

        RBE3 creates constraint equations such that the motion of the master is
        the average of the slaves. For the rotations, a least-squares approach
        is used to define the "average rotation" at the master from the
        translations of the slaves. If the slave nodes are colinear, then one
        of the master rotations that is parallel to the colinear direction can
        not be determined in terms of the translations of the slave nodes.
        Therefore, the associated moment component on the master node in that
        direction can not be transmitted. When this case occurs, a warning
        message is issued and the constraint equations created by RBE3 are
        ignored.

        Applying this command to a large number of slave nodes may result in
        constraint equations with a large number of coefficients. This may
        significantly increase the peak memory required during the process of
        element assembly. If real memory or virtual memory is not available,
        consider reducing the number of slave nodes.

        As an alternative to the RBE3 command, you can apply a similar type of
        constraint using contact elements and the internal multipoint
        constraint (MPC) algorithm. See Surface-based Constraints for more
        information.

        This command is also valid in SOLUTION.
        """
        command = f"RBE3,{master},{dof},{slaves},{wtfact}"
        return self.run(command, **kwargs)
