class FeConstraints:
    def d(
        self,
        node="",
        lab="",
        value="",
        value2="",
        nend="",
        ninc="",
        lab2="",
        lab3="",
        lab4="",
        lab5="",
        lab6="",
        **kwargs,
    ):
        """Defines degree-of-freedom constraints at nodes.

        APDL Command: D

        Parameters
        ----------
        node
            Node at which constraint is to be specified. If ALL, NEND and NINC
            are ignored and constraints are applied to all selected nodes
            (NSEL). If Node = P, graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI).  A component
            name may also be substituted for Node.

        lab
            Valid degree-of-freedom label.  If ALL, use all appropriate labels.

        value
            Degree-of-freedom value or table name reference for tabular
            boundary conditions.  To specify a table, enclose the table name in
            percent (%) signs (for example, D,Node,TEMP,%tabname%). Use the
            ``*DIM`` command to define a table.

        value2
            Second degree-of-freedom value (if any).  If the analysis type and
            the degree of freedom allow a complex input, Value (above) is the
            real component and VALUE2 is the imaginary component.

        nend, ninc
            Specifies the same values of constraint at the range of nodes from
            Node to NEND (defaults to Node), in steps of NINC (defaults to 1).

        lab2, lab3, lab4, lab5, lab6
            Additional degree-of-freedom labels. The same values are applied to
            the nodes for these labels.

        Notes
        -----
        The available degrees of freedom per node are listed under "Degrees of
        Freedom" in the input table for each element type in the Element
        Reference.  Degrees of freedom are defined in the nodal coordinate
        system.  The positive directions of structural translations and
        rotations are along and about the positive nodal axes directions.
        Structural rotations should be input in radians.  The node and the
        degree-of-freedom label must be selected (NSEL, DOFSEL).

        In a structural analysis, you can apply only one displacement,
        velocity, or acceleration load at any degree of freedom. If multiple
        loads are specified, the last applied load overrides the previous ones.
        For example, the following commands apply loads to node 100:

        In this case, the velocity load (VELX) applied in the last command will
        override the displacement load (UX).

        For elements used in static and low frequency electromagnetic analysis
        (SOLID236 and SOLID237), the AZ degree of freedom is not a z-component
        of a vector potential, but rather the flux contribution on the element
        edge.  To specify a flux-parallel condition, set AZ = 0.  For more
        information, see 3-D Magnetostatics and Fundamentals of Edge-based
        Analysis in the Low-Frequency Electromagnetic Analysis Guide.

        In an explicit dynamic analysis, the D command can only be used to fix
        nodes in the model. The degree-of-freedom value must be zero; no other
        values are valid. Use the EDLOAD command to apply a nonzero
        displacement in an explicit dynamic analysis.

        For ELBOW290 cross-section degrees of freedom (Lab = SE, SO, SW, SRA,
        SRT, or SECT), the D command can only specify fixed constraints. The
        degree-of-freedom value must be zero; no other values are valid.

        For hydrostatic fluid elements (HSFLD241 and HSFLD242), the HDSP
        degree-of-freedom constraint at the pressure node prescribes the
        pressure value for all the fluid elements sharing the pressure node.

        Tabular boundary conditions (VALUE = %tabname%) are available only for
        the following degree-of-freedom labels: Electric (VOLT), structural
        (UX, UY, UZ, ROTX, ROTY, ROTZ, and velocity and acceleration loads
        VELX, VELY, VELZ, OMGX, OMGY, OMGZ, ACCX, ACCY, ACCZ, DMGX, DMGY,
        DMGZ), acoustic (PRES, UX, UY, UZ,), and temperature (TEMP, TBOT, TE2,
        TE3, . . ., TTOP). All labels are valid only in static (ANTYPE,STATIC)
        and full transient (ANTYPE,TRANS) analyses.

        %_FIX% is an ANSYS reserved table name. When VALUE is set to %_FIX%,
        ANSYS will prescribe the degree of freedom to the "current" relative
        displacement value. This option is only valid for the following labels:
        UX, UY, UZ, ROTX, ROTY, ROTZ. Alternatively, functions UX(), UY(), etc.
        may be used (see ``*GET`` for a complete list of available functions). In
        most cases, %_FIX% usage is efficient and recommended for all
        structural degrees of freedom.

        When Value = SUPPORT, specify only the minimum number of displacement
        constraints necessary to prevent rigid body motion: three constraints
        (or fewer, depending on the element type) for 2-D models and six (or
        fewer) for 3-D models.

        If constraints and initial conditions (IC) are applied at the same
        node, the constraint specification overrides. This combination is
        useful when a constraint degree-of-freedom value needs to start with a
        nonzero value at time = 0.0. For example, if the constraint degree-of-
        freedom value is prescribed to be a cosine function, then specifying an
        initial condition for the same node and degree of freedom ensures that
        the initial value for the constraint degree of freedom at time = 0.0 is
        same as the cosine function evaluated at time = 0.0. If initial
        conditions are not specified, the constraint degree-of-freedom value
        ramps from zero in the first substep of the first loadstep.

        If more than one rotational degrees of freedom are constrained with
        non-zero rotations (ROTX, ROTY, ROTZ), rotational velocities (OMGX,
        OMGY, OMGZ), or rotational accelerations (DMGX, DMGY, DMGZ), then the
        rotation of the constrained node from its initial configuration to its
        final configuration depends on the combination and the sequence in
        which the constraints are applied. See Rotations in a Large-Deflection
        Analysis in Structural Analysis Guide.

        This command is also valid in PREP7.
        """
        command = f"D,{node},{lab},{value},{value2},{nend},{ninc},{lab2},{lab3},{lab4},{lab5},{lab6}"
        return self.run(command, **kwargs)

    def dcum(self, oper="", rfact="", ifact="", tbase="", **kwargs):
        """Specifies that DOF constraint values are to be accumulated.

        APDL Command: DCUM

        Parameters
        ----------
        oper
            Accumulation key:

            REPL - Subsequent values replace the previous values (default).

            ADD - Subsequent values are added to the previous values.

            IGNO - Subsequent values are ignored.

        rfact
            Scale factor for the real component.  Zero (or blank) defaults to
            1.0.  Use a small number for a zero scale factor.

        ifact
            Scale factor for the imaginary component.  Zero (or blank) defaults
            to 1.0.  Use a small number for a zero scale factor.

        tbase
            Base temperature for temperature difference.  Used only with
            temperature degree of freedom.  Scale factor is applied to the
            temperature difference (T-TBASE) and then added to TBASE.  T is the
            current temperature.

        Notes
        -----
        Allows repeated degree of freedom constraint values (displacement,
        temperature, etc.)  to be replaced, added, or ignored.  Operations
        apply to the selected nodes [NSEL] and the selected degree of freedom
        labels [DOFSEL]. This command also operates on velocity and
        acceleration loads applied in a structural analysis.

        The operations occur when the next degree of freedom constraints are
        defined.  For example, issuing the command D,1,UX,.025 after a previous
        D,1,UX,.020 causes the new value of the displacement on node 1 in the
        x-direction to be 0.045 with the add operation, 0.025 with the replace
        operation, or 0.020 with the ignore operation.  Scale factors are also
        available to multiply the next value before the add or replace
        operation.  A scale factor of 2.0 with the previous "add" example
        results in a displacement of 0.070.  Scale factors are applied even if
        no previous values exist.  Issue DCUM,STAT to show the current label,
        operation, and scale factors.  Solid model boundary conditions are not
        affected by this command, but boundary conditions on the FE model are
        affected.

        Note:: : FE boundary conditions may still be overwritten by existing
        solid model boundary conditions if a subsequent boundary condition
        transfer occurs.

        DCUM does not work for tabular boundary conditions.

        This command is also valid in PREP7.
        """
        command = f"DCUM,{oper},{rfact},{ifact},{tbase}"
        return self.run(command, **kwargs)

    def ddele(self, node="", lab="", nend="", ninc="", rkey="", **kwargs):
        """Deletes degree-of-freedom constraints.

        APDL Command: DDELE

        Parameters
        ----------
        node
            Node for which constraint is to be deleted.  If ALL, NEND and NINC
            are ignored and constraints for all selected nodes [NSEL] are
            deleted.  If NODE = P, graphical picking is enabled and all
            remaining command fields are ignored (valid only in the GUI).  A
            component name may also be substituted for NODE.

        lab
            Valid degree of freedom label.  If ALL, use all selected labels
            [DOFSEL].  Structural labels:  UX, UY, or UZ (displacements); ROTX,
            ROTY, or ROTZ (rotations); WARP (warping).  Thermal labels: TEMP,
            TBOT, TE2, TE3, . . ., TTOP (temperature).  Acoustic labels:  PRES
            (pressure); UX, UY, or UZ (displacements for FSI coupled elements).
            Electric label:  VOLT (voltage).  Magnetic labels:  MAG (scalar
            magnetic potential); AX, AY, or AZ (vector magnetic potentials).
            Diffusion label: CONC (concentration).

        nend, ninc
            Delete constraints from NODE to NEND (defaults to NODE) in steps of
            NINC (defaults to 1).

        rkey
            Ramping key:

            OFF  - Loads are step-removed (default).

            ON or FORCE  - Forces on the specified degrees of freedom (Lab) are ramped during the next
                           load step. The forces are ramped from the reaction
                           forces of the previous load step, regardless of
                           whether or not a constraint was present. If the
                           specified node(s) and degree(s) of freedom has a
                           force value currently defined, the force is ramped
                           from the reaction force value to the currently
                           applied force value. If no force is currently
                           applied, the force is ramped from the reaction force
                           value to zero.

        Notes
        -----
        Deleting a constraint is not the same as setting it to zero (which
        "fixes" the degree of freedom to a zero value).  Deleting a constraint
        has the same effect as deactivating, releasing, or setting the
        constraint "free."  The node and the degree of freedom label must be
        selected [NSEL, DOFSEL].

        This command is also valid in PREP7.
        """
        command = f"DDELE,{node},{lab},{nend},{ninc},{rkey}"
        return self.run(command, **kwargs)

    def dflx(self, node="", bx="", by="", bz="", bx2="", by2="", bz2="", **kwargs):
        """Imposes a uniform magnetic flux B on an edge-element electromagnetic

        APDL Command: DFLX
        model.

        Parameters
        ----------
        node
            Nodes at which the edge-flux (AZ) constraints corresponding to the
            uniform magnetic flux are to be specified.  Valid options are ALL
            (default) or Component Name. If ALL, constraints are applied to all
            selected nodes (NSEL).

        bx, by, bz
            Real components of magnetic flux B.

        bx2, by2, bz2
            Imaginary components of magnetic flux B.

        Notes
        -----
        The DFLX command sets the constraints on the edge-flux (AZ) degrees of
        freedom to produce a uniform magnetic flux B in an edge-based
        electromagnetic analysis using elements SOLID236 and SOLID237. The
        command ignores the corner nodes of the elements (even if they were
        selected) and imposes the AZ-constraints on the mid-side nodes only.
        The AZ-constraints are imposed in the active Cartesian coordinate
        system. A non-Cartesian coordinate system will be ignored by the DFLX
        command.

        The edge-flux constraints at the mid-side nodes are derived from  the
        magnetic vector potential A, which is related to the imposed magnetic
        flux B as follows:

        where r is the position of the mid-side node.

        The DFLX command creates a component named _DFLX for the constrained
        midside nodes. You can use this component to delete the constraints
        imposed by the DFLX command.

        This command is also valid in PREP7.
        """
        command = f"DFLX,{node},{bx},{by},{bz},{bx2},{by2},{bz2}"
        return self.run(command, **kwargs)

    def dj(self, elem="", label="", value="", **kwargs):
        """Specifies boundary conditions on the components of relative motion of a

        APDL Command: DJ
        joint element.

        Parameters
        ----------
        elem
            Element number or ALL to be specified.

        label
            Valid labels are:

            UX - Displacement in local x direction.

            UY - Displacement in local y direction.

            UZ - Displacement in local z direction.

            ROTX - Rotation about local x axis.

            ROTY - Rotation about local y axis.

            ROTZ - Rotation about local y axis.

            VELX - Linear velocity in local x direction.

            VELY - Linear velocity in local y direction.

            VELZ - Linear velocity in local z direction.

            OMGX - Angular velocity in local x direction.

            OMGY - Angular velocity in local y direction.

            OMGZ - Angular velocity in local z direction.

            ACCX - Linear acceleration in local x direction.

            ACCY - Linear acceleration in local y direction.

            ACCZ - Linear acceleration in local z direction.

            DMGX - Angular acceleration in local x direction.

            DMGY - Angular acceleration in local y direction.

            DMGZ - Angular acceleration in local z direction.

        value
            Value of the label.

        Notes
        -----
        This command is valid for MPC184 joint elements. See DJDELE for
        information on deleting boundary conditions applied with the DJ
        command.

        You can apply only one displacement, velocity, or acceleration load at
        any relative degree of freedom. If multiple loads are specified, the
        last applied load overrides the previous ones. For example, the
        following commands apply loads to element 100:

        In this case, the velocity load (VELX) applied in the last command will
        override the displacement load (UX).

        Tabular boundary conditions (VALUE = %tabname%) can be used.

        %_FIX% is an ANSYS reserved table name. When VALUE is set to %_FIX%,
        ANSYS will prescribe the degree of freedom to the "current" relative
        displacement value. This option is only valid for the following labels:
        UX, UY, UZ, ROTX, ROTY, ROTZ. In most cases, %_FIX% usage is efficient
        and recommended for all structural degrees of freedom.
        """
        command = f"DJ,{elem},{label},{value}"
        return self.run(command, **kwargs)

    def djdele(self, elem="", lab="", **kwargs):
        """Deletes boundary conditions on the components of relative motion of a

        APDL Command: DJDELE
        joint element.

        Parameters
        ----------
        elem
            Element number or ALL. ALL (or leaving this field blank) will
            delete all joint element boundary conditions specified by LAB.

        lab
            Valid labels are:

            UX - Displacement in local x direction.

            UY - Displacement in local y direction.

            UZ - Displacement in local z direction.

            ROTX - Rotation about local x axis.

            ROTY - Rotation about local y axis.

            ROTZ - Rotation about local z axis.

            VELX - Linear velocity in local x direction.

            VELY - Linear velocity in local y direction.

            VELZ - Linear velocity in local z direction.

            OMGX - Angular velocity in local x direction.

            OMGY - Angular velocity in local y direction.

            OMGZ - Angular velocity in local z direction.

            ACCX - Linear acceleration in local x direction.

            ACCY - Linear acceleration in local y direction.

            ACCZ - Linear acceleration in local z direction.

            DMGX - Angular acceleration in local x direction.

            DMGY - Angular acceleration in local y direction.

            DMGZ - Angular acceleration in local z direction.

            ALL, or (blank) - Delete all applied boundary conditions.

        Notes
        -----
        This command is valid for MPC184 joint elements. See DJ for information
        on specifying boundary conditions on the components of relative motion
        of a joint element.
        """
        command = f"DJDELE,{elem},{lab}"
        return self.run(command, **kwargs)

    def djlist(self, elem="", **kwargs):
        """Lists boundary conditions applied to joint elements.

        APDL Command: DJLIST

        Parameters
        ----------
        elem
            Element number or ALL (or blank). Lists joint element boundary
            conditions on the specified element(s).

        Notes
        -----
        This command is valid for MPC184 joint elements. See DJ for information
        on specifying boundary conditions on joint elements.
        """
        command = f"DJLIST,{elem}"
        return self.run(command, **kwargs)

    def dlist(self, node1="", node2="", ninc="", **kwargs):
        """Lists DOF constraints.

        APDL Command: DLIST

        Parameters
        ----------
        node1, node2, ninc
            List constraints for nodes NODE1 to NODE2 (defaults to NODE1) in
            steps of NINC (defaults to 1).  If ALL (default), NODE2 and NINC
            are ignored and constraints for all selected nodes [NSEL] are
            listed.  If NODE1 = P, graphical picking is enabled and all
            remaining command fields are ignored (valid only in the GUI).  A
            component name may also be substituted for NODE1(NODE2 and NINC are
            ignored).

        Notes
        -----
        Listing applies to the selected nodes [NSEL] and the selected degree of
        freedom labels [DOFSEL].

        This command is valid in any processor.
        """
        command = f"DLIST,{node1},{node2},{ninc}"
        return self.run(command, **kwargs)

    def dscale(self, rfact="", ifact="", tbase="", **kwargs):
        """Scales DOF constraint values.

        APDL Command: DSCALE

        Parameters
        ----------
        rfact
            Scale factor for the real component.  Zero (or blank) defaults to
            1.0.  Use a small number for a zero scale factor.

        ifact
            Scale factor for the imaginary component.  Zero (or blank) defaults
            to 1.0.  Use a small number for a zero scale factor.

        tbase
            Base temperature for temperature difference.  For temperatures, the
            scale factor is applied to the temperature difference (T-TBASE) and
            then added to TBASE.  T is the current temperature.

        Notes
        -----
        Scales degree of freedom constraint values (displacement, temperature,
        etc.) in the database.  If velocity and acceleration boundary
        conditions are applied in a structural analysis, they are also scaled
        by this command. Solid model boundary conditions are not scaled by this
        command, but boundary conditions on the FE model are scaled.

        Note:: : Such scaled FE boundary conditions may still be overwritten by
        unscaled solid model boundary conditions if a subsequent boundary
        condition transfer occurs.

        Scaling applies to the previously defined values for the selected nodes
        [NSEL] and the selected degree of freedom labels [DOFSEL].  Issue DLIST
        command to review results.

        DSCALE does not work for tabular boundary conditions.

        This command is also valid in PREP7.
        """
        command = f"DSCALE,{rfact},{ifact},{tbase}"
        return self.run(command, **kwargs)

    def dsym(self, lab="", normal="", kcn="", **kwargs):
        """Specifies symmetry or antisymmetry degree-of-freedom constraints on

        APDL Command: DSYM
        nodes.

        Parameters
        ----------
        lab
            Symmetry label:

            SYMM - Generate symmetry constraints as described below (default).

            ASYM - Generate antisymmetry constraints as described below.

        normal
            Surface orientation label to determine the constraint set (surface
            is assumed to be perpendicular to this coordinate direction in
            coordinate system KCN):

            X - Surface is normal to coordinate X direction (default).  Interpreted as R
                direction for non-Cartesian coordinate systems.

            Y - Surface is normal to coordinate Y direction.   θ direction for non-Cartesian
                coordinate systems.

            Z - Surface is normal to coordinate Z direction.   Φ direction for spherical or
                toroidal coordinate systems.

        kcn
            Reference number of global or local coordinate system used to
            define surface orientation.

        Notes
        -----
        Specifies symmetry or antisymmetry degree-of-freedom constraints on the
        selected nodes. The nodes are first automatically rotated (any
        previously defined rotations on these nodes are redefined) into
        coordinate system KCN, then zero-valued constraints are generated, as
        described below, on the selected degree-of-freedom set (limited to
        displacement, velocity, and magnetic degrees of freedom) [DOFSEL].
        Constraints are defined in the (rotated) nodal coordinate system, as
        usual. See the D and NROTAT commands for additional details about
        constraints and nodal rotations.

        This command is also valid in PREP7.

        Symmetry or antisymmetry constraint generations are based upon the
        valid degrees of freedom in the model, i.e., the degrees of freedom
        associated with the elements attached to the nodes.  The labels for
        degrees of freedom used in the generation depend on the Normal label.

        For displacement degrees of freedom, the constraints generated are:

        For velocity degrees of freedom, the constraints generated are:

        For magnetic degrees of freedom, the SYMM label generates flux normal
        conditions (flux flows normal to the surface).  Where no constraints
        are generated, the flux normal condition is "naturally" satisfied.  The
        ASYM label generates flux parallel conditions (flux flows parallel to
        the surface).
        """
        command = f"DSYM,{lab},{normal},{kcn}"
        return self.run(command, **kwargs)

    def dval(self, baseid="", lab="", value="", value2="", keycal="", **kwargs):
        """Defines values at enforced motion base.

        APDL Command: DVAL

        Parameters
        ----------
        baseid
            The identification number of the enforced motion base (defined
            using the D command in the modal analysis).

        lab
            U

            U - Enforced displacement.

            ACC - Enforced acceleration.

        value
            The value or table name reference for tabular boundary conditions.
            To specify a table, enclose the table name in percent (%) signs
            (DVAL,BaseID,U,%tablename%). Use the ``*DIM`` command to define a
            table.

        value2
            The value of the second degree of freedom (if present). If the
            analysis type and the degree of freedom allow a complex input,
            VALUE is the real component and VALUE2 is the imaginary component.

        keycal
            Displacement result calculation key:

            ON - Calculate absolute displacement and acceleration results (default).

            OFF - Calculate relative displacement and acceleration results.

        Notes
        -----
        In a mode-superposition harmonic or transient analysis, you can apply
        enforced displacement or acceleration loads. If multiple loads are
        specified for the same base identification number (BaseID), the last
        load applied overrides the previous ones. For example, the following
        commands apply displacement to the base with identification number 1:

        In this case, the acceleration (ACC) applied in the last command will
        override the displacement (U).

        Issue LSCLEAR,LSOPT to delete DVAL command options from the database.

        For more information, see Enforced Motion Method for Mode-Superposition
        Transient and Harmonic Analyses in the Structural Analysis Guide and
        Enforced Motion Method for Transient and Harmonic Analyses in the
        Mechanical APDL Theory Reference.
        """
        command = f"DVAL,{baseid},{lab},{value},{value2},{keycal}"
        return self.run(command, **kwargs)

    def gsbdata(
        self,
        labz="",
        valuez="",
        labx="",
        valuex="",
        laby="",
        valuey="",
        **kwargs,
    ):
        """Specifies the constraints or applies the load at the ending point for

        APDL Command: GSBDATA
        generalized plane strain option.

        Parameters
        ----------
        labz
            Constraint or load at the ending point in the fiber Z direction.

            F - Apply a force in the fiber direction (default).

            LFIBER - Define a length change in the fiber direction.

        valuez
            Value for LabZ. The default is zero.

        labx
            Constraint or load on rotation about X.

            MX - Supply a moment to cause the rotation of the ending plane about X (default).

            ROTX - Define a rotation angle (in radians) of the ending plane about X.

        valuex
            Value for LabX. The default is zero.

        laby
            Constraint or load on rotation about Y

            MY - Supply a moment to cause the rotation of the ending plane about Y (default).

            ROTY - Define a rotation angle (in radians) of the ending plane about Y.

        valuey
            Value for LabY. The default is zero.

        Notes
        -----
        All inputs are in the global Cartesian coordinate system. For more
        information about the generalized plane strain feature, see Generalized
        Plane Strain Option of Current-Technology Solid Elements in the Element
        Reference.

        This command is also valid in PREP7.
        """
        command = f"GSBDATA,{labz},{valuez},{labx},{valuex},{laby},{valuey}"
        return self.run(command, **kwargs)

    def gslist(self, lab="", **kwargs):
        """When using generalized plane strain, lists the input data or solutions.

        APDL Command: GSLIST

        Parameters
        ----------
        lab
            Specify the content to be listed.

            GEOMETRY - List the data input using GSGDATA

            BC - List the data input using GSBDATA.

            REACTIONS - When the command is issued in POST1, list the reaction force at the ending
                        point,

             and the moment about X and Y if the corresponding constraints were applied. - RESULTS

            When the command is issued in POST1, list the change of fiber length at the ending point during deformation and the rotation of the ending plane about X and Y during deformation. - ALL

        Notes
        -----
        This command can be used to list the initial position of the ending
        plane, the applied load or displacements in the fiber direction, the
        resulting position of the ending plane after deformation, and the
        available reaction forces and moments at the ending point.

        All inputs and outputs are in the global Cartesian coordinate system.
        For more information about the generalized plane strain feature, see
        Generalized Plane Strain Option of Current-Technology Solid Elements in
        the Element Reference.

        This command is valid in any processor.
        """
        command = f"GSLIST,{lab}"
        return self.run(command, **kwargs)
