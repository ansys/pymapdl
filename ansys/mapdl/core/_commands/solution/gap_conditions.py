class GapConditions:
    def gp(self, node1="", node2="", lab="", stif="", gap="", damp="", **kwargs):
        """Defines a gap condition for transient analyses.

        APDL Command: GP

        Parameters
        ----------
        node1
            Node I of gap.  If NODE1 = P, graphical picking is enabled and all
            remaining command fields are ignored (valid only in the GUI).

        node2
            Node J of gap (must be different from NODE1).  Non-grounded gap
            nodes must be defined as master degrees of freedom or be
            unconstrained, active DOF in a full analysis type.  Grounded gap
            nodes (those not defined as MDOF) need not appear elsewhere in the
            model.

        lab
            Direction of gap action in the nodal coordinate system (implied
            from the following force labels): FX, FY, FZ, MX, MY, MZ.

        stif
            Stiffness (Force/Length) of closed gap (may be positive or
            negative).

        gap
            Initial size of gap.  A zero (or positive) value assumes an
            initially open gap.  A negative value defines an interference
            condition.  For a rotational gap, GAP should be in radians.

        damp
            Damping coefficient (``Force*Time/Length``) of closed gap using pseudo
            velocity (Newmark finite difference expansion scheme).

        Notes
        -----
        Defines a gap condition for the mode superposition transient analysis
        (ANTYPE,TRANS with TRNOPT,MSUP). If used in SOLUTION, this command is
        valid only within the first load step. Gap conditions specified in
        subsequent load steps are ignored.

        Repeat GP command for additional gap conditions. Gaps are numbered
        sequentially as input.

        Note:: : Gaps may be renumbered by the program during the solution (see
        output listing)

        The mode-superposition transient analysis does not allow gap action
        with the standard gap elements. However, you can define gap conditions
        which are similar to gap elements; gap conditions can be specified
        between surfaces that are expected to contact (impact) each other
        during the transient. The gap condition simulates the basic gap action
        of the COMBIN40 element.

        The gap condition is treated as an explicit force (equal to the
        interference times contact stiffness) and affects only the load vector
        calculation and not the stiffness matrix. The interference is
        calculated from the displacement extrapolated from the previous time
        points.

        Gap conditions can only be defined between two master degree of freedom
        (DOF) nodes or between master DOF nodes and ground, as shown in the
        following figure.

        Master degrees of freedom are the unconstrained and active degrees of
        freedom. Gap nodes not defined as active degrees of freedom or attached
        to an element are assumed to be grounded. Grounded gap nodes do not
        need a spatial location, nor do they need to be located on an element.

        Gap conditions may be defined in parallel (across the same nodes), with
        varying gap and stiffness values, to simulate a nonlinear (piecewise)
        force-deflection curve.

        The gap direction is determined from the force label input on the GP
        command; i.e., FX defines a translational gap acting in the UX nodal
        degree of freedom direction, and MZ defines a rotational gap acting in
        the nodal ROTZ degree of freedom direction. The actual degree of
        freedom directions available for a particular node depends upon the
        degrees of freedom associated with the element types [ET] at that node.

        If the coordinate systems of the nodes connecting the gap are rotated
        relative to each other, the same degree of freedom may be in different
        directions. The gap, however, assumes only a one-dimensional action.
        Nodes I and J may be anywhere in space (preferably coincident).  No
        moment effects are included due to noncoincident nodes. That is, if the
        nodes are offset from the line of action, moment equilibrium may not be
        satisfied.

        The contact stiffness value represents the stiffness of the closed gap.
        Stiffness values are related to the integration time step size and
        should be physically reasonable. High stiffness will require a small
        integration time step; otherwise, due to the displacement
        extrapolation, the solution may go unstable. Negative stiffness values
        may be used with gaps in parallel to produce a decreasing force-
        deflection curve.

        The order of specifying the gap nodes is important; i.e., a gap
        condition connecting two nodes will act differently depending upon
        which node is specified first on the GP command.  For example, for Node
        1 at X = 0.0, Node 2 at X = 0.1, and the gap defined from Node 1 to 2,
        a displacement of Node 1 greater than Node 2 will cause the gap to
        close.  For the gap defined from Node 2 to 1, a displacement of Node 2
        greater than Node 1 will cause the gap to close (like a hook action).
        In general, the gap closes whenever the separation (defined as UJ - UI
        + GAP) is negative.  UJ is the displacement of node J, UI is the
        displacement of node I, and GAP is the input gap value.  The gap force
        output appears in the printout only for the time steps for which the
        gap is closed.  A negative spring force is always associated with a
        closed gap (even with the hook option).

        Some guidelines to define gap conditions are presented below:

        Use enough gap conditions to obtain a smooth contact stress
        distribution between the contacting surfaces.

        Define a reasonable gap stiffness. If the stiffness is too low, the
        contacting surfaces may overlap too much. If the stiffness is too high,
        a very small time step will be required during impact. A general
        recommendation is to specify a gap stiffness that is one or two orders
        of magnitude higher than the adjacent element stiffness. You can
        estimate the adjacent element stiffness using AE/L, where A is the
        contributing area around the gap condition, E is the elastic modulus of
        the softer material at the interface, and L is the depth of the first
        layer of elements at the interface.

        A mode-superposition transient using the nonlinear gap damping provided
        through the DAMP field runs faster than a full transient analysis using
        a gap element (COMBIN40).

        Use the GPLIST command to list gap conditions and the GPDELE command to
        delete gap conditions.

        This command is also valid in PREP7.
        """
        command = f"GP,{node1},{node2},{lab},{stif},{gap},{damp}"
        return self.run(command, **kwargs)

    def gpdele(self, gap1="", gap2="", ginc="", **kwargs):
        """Deletes gap conditions.

        APDL Command: GPDELE

        Parameters
        ----------
        gap1, gap2, ginc
            Delete gap conditions from GAP1 to GAP2 (defaults to GAP1) in steps
            of GINC  (defaults to 1).

        Notes
        -----
        Deletes gap conditions defined with the GP command.  Gap conditions
        following those deleted are automatically compressed and renumbered.
        If used in SOLUTION, this command is valid only within the first load
        step.

        This command is also valid in PREP7.
        """
        command = f"GPDELE,{gap1},{gap2},{ginc}"
        return self.run(command, **kwargs)

    def gplist(self, gap1="", gap2="", ginc="", **kwargs):
        """Lists the gap conditions.

        APDL Command: GPLIST

        Parameters
        ----------
        gap1, gap2, ginc
            List gap conditions from GAP1 to GAP2 (GAP2 defaults to GAP1) in
            steps of GINC  (defaults to 1).  If GAP1 = ALL (default), GAP2 and
            GINC  are ignored and all gap conditions are listed.

        Notes
        -----
        This command is valid in any processor.
        """
        command = f"GPLIST,{gap1},{gap2},{ginc}"
        return self.run(command, **kwargs)
