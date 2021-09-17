class FeForces:
    def f(self, node="", lab="", value="", value2="", nend="", ninc="", **kwargs):
        """Specifies force loads at nodes.

        APDL Command: F

        Parameters
        ----------
        node
            Node at which force is to be specified.  If ALL, NEND and NINC are
            ignored and forces are applied to all selected nodes [NSEL]. If
            NODE = P, graphical picking is enabled and all remaining command
            fields are ignored (valid only in the GUI).  A component name may
            also be substituted for NODE.

        lab
            Valid force label.  Structural labels:  FX, FY, or FZ (forces); MX,
            MY, or MZ (moments).  Thermal labels:  HEAT, HBOT, HE2, HE3, . . .,
            HTOP (heat flow).  Fluid labels:  FLOW (fluid flow).   Electric
            labels:  AMPS (current flow), CHRG (electric charge).  Magnetic
            labels:  FLUX (magnetic flux);  CSGX, CSGY, or CSGZ (magnetic
            current segments).  Diffusion labels: RATE (diffusion flow rate).

        value
            Force value or table name reference for specifying tabular boundary
            conditions.  To specify a table, enclose the table name in percent
            signs (%), e.g., F, NODE,HEAT,%tabname%).  Use the ``*DIM`` command to
            define a table.

        value2
            Second force value (if any).  If the analysis type and the force
            allow a complex input, VALUE (above) is the real component and
            VALUE2 is the imaginary component.

        nend, ninc
            Specifies the same values of force at the nodes ranging from NODE
            to NEND (defaults to NODE), in steps of NINC (defaults to 1).

        Notes
        -----
        The available force loads per node correspond to the degrees of freedom
        listed under "Degrees of Freedom" in the input table for each element
        type in the Element Reference.  If both a force and a constrained
        degree of freedom [D] are specified at the same node, the constraint
        takes precedence.  Forces are defined in the nodal coordinate system.
        The positive directions of structural forces and moments are along and
        about the positive nodal axis directions.  The node and the degree of
        freedom label corresponding to the force must be selected [NSEL,
        DOFSEL].

        For hydrostatic fluid elements (HSFLD241 and HSFLD242), DVOL is used to
        specify fluid mass flow rate (with units of mass/time) at the pressure
        node. This allows fluid to be added or taken out of the fluid elements
        sharing the pressure node. A fluid density must also be specified (via
        the MP command or TB command) to apply a volume change corresponding to
        the prescribed fluid mass flow rate.

        Tabular boundary conditions (VALUE = %tabname%) are available only for
        the following labels: Fluid (FLOW), Electric (AMPS), Structural force
        (FX, FY, FZ, MX, MY, MZ), and Thermal (HEAT, HBOT, HE2, HE3, . . .,
        HTOP). Tabular boundary conditions are valid only in static
        (ANTYPE,STATIC), full transient (ANTYPE,TRANS), full harmonic (ANTYPE,
        HARMIC), modal superposition harmonic and modal superposition transient
        analyses.

        This command is also valid in PREP7.
        """
        command = f"F,{node},{lab},{value},{value2},{nend},{ninc}"
        return self.run(command, **kwargs)

    def fcum(self, oper="", rfact="", ifact="", **kwargs):
        """Specifies that force loads are to be accumulated.

        APDL Command: FCUM

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

        Notes
        -----
        Allows repeated force load (force, heat flow, etc.) values to be
        replaced, added, or ignored.  Operations apply to the selected nodes
        [NSEL]. and the force labels corresponding to the selected force labels
        [DOFSEL].  The operations occur when the next force specifications are
        defined.  For example, issuing the command F,1,FX,250 after a previous
        F,1,FX,200 causes the current value of the force on node 1 in the
        x-direction to be 450 with the add operation, 250 with the replace
        operation, or 200 with the ignore operation.  Scale factors are also
        available to multiply the next value before the add or replace
        operation.  A scale factor of 2.0 with the previous "add" example
        results in a force of 700.  Scale factors are applied even if no
        previous values exist.  Issue FCUM,STAT to show the current label,
        operation, and scale factors.  Solid model boundary conditions are not
        affected by this command, but boundary conditions on the FE model are
        affected.

        Note:: : FE boundary conditions may still be overwritten by existing
        solid model boundary conditions if a subsequent boundary condition
        transfer occurs.

        FCUM does not work for tabular boundary conditions.

        This command is also valid in PREP7.
        """
        command = f"FCUM,{oper},{rfact},{ifact}"
        return self.run(command, **kwargs)

    def fdele(self, node="", lab="", nend="", ninc="", lkey="", **kwargs):
        """Deletes force loads on nodes.

        APDL Command: FDELE

        Parameters
        ----------
        node
            Node for which force is to be deleted.  If ALL, NEND and NINC are
            ignored and forces are deleted on all selected nodes [NSEL].  If
            NODE = P, graphical picking is enabled and all remaining command
            fields are ignored (valid only in the GUI).  A component name may
            also be substituted for NODE.

        lab
            Valid force label.  If ALL, use all appropriate labels.  Structural
            labels:  FX, FY, or FZ (forces); MX, MY, or MZ (moments).  Thermal
            labels:  HEAT, HBOT, HE2, HE3, . . ., HTOP (heat flow).  Fluid
            labels:  FLOW (fluid flow).  Electric labels:  AMPS (current flow),
            CHRG (electric charge).  Magnetic labels:  FLUX (magnetic flux);
            CSGX, CSGY, or CSGZ (magnetic current segments).  Diffusion labels:
            RATE (diffusion flow rate).

        nend, ninc
            Delete forces from NODE to NEND (defaults to NODE) in steps of NINC
            (defaults to 1).

        lkey
            Lock key:

            (blank) - The DOF is not locked (default).

            FIXED - Displacement on the specified degrees of freedom (Lab) is locked. The program
                    prescribes the degree of freedom to the "current" relative
                    displacement value in addition to deleting the force. If a
                    displacement constraint (for example, D command) is applied
                    in conjunction with this option, the actual applied
                    displacement will be ramped during the next load step. The
                    displacement is ramped from the current value to the newly
                    defined value. This option is only valid for the following
                    labels: FX, FY, FZ, MX, MY, MZ. This option is intended
                    primarily for use in the ANSYS Workbench interface to apply
                    an increment length adjustment (bolt pretension loading).

        Notes
        -----
        The node and the degree of freedom label corresponding to the force
        must be selected [NSEL, DOFSEL].

        This command is also valid in PREP7.
        """
        command = f"FDELE,{node},{lab},{nend},{ninc},{lkey}"
        return self.run(command, **kwargs)

    def fj(self, elem="", label="", value="", **kwargs):
        """Specify forces or moments on the components of the relative motion of a

        APDL Command: FJ
        joint element.

        Parameters
        ----------
        elem
            Element number or ALL to specify all joint elements.

        label
            Valid labels:

            FX - Force in local x direction.

            FY - Force in local y direction.

            FZ - Force in local z direction.

            MX - Moment about local x axis.

            MY - Moment about local y axis.

            MZ - Moment about local z axis.

        value
            Value of the label.

        Notes
        -----
        Valid for MPC184 (joint options in KEYOPT(1)).

        See FJDELE for information on deleting forces and moments.
        """
        command = f"FJ,{elem},{label},{value}"
        return self.run(command, **kwargs)

    def fjdele(self, elem="", lab="", **kwargs):
        """Deletes forces (or moments) on the components of the relative motion of

        APDL Command: FJDELE
        a joint element.

        Parameters
        ----------
        elem
            Element number, or ALL. (leaving this blank defaults to ALL)

        lab
            Valid labels are:

            FX - Force in local x direction.

            FY - Force in local y direction.

            FZ - Force in local z direction.

            MX - Moment about local x axis.

            MY - Moment about local y axis.

            MZ - Moment about local z axis.

            ALL, or (blank) - Delete all valid forces or moments.

        Notes
        -----
        Valid for MPC184 (joint options in KEYOPT(1)).

        See FJ for information on specifying forces (or moments).
        """
        command = f"FJDELE,{elem},{lab}"
        return self.run(command, **kwargs)

    def fjlist(self, elem="", **kwargs):
        """Lists forces and moments applied on joint elements.

        APDL Command: FJLIST

        Parameters
        ----------
        elem
            Element number or ALL (or blank). Lists joint element forces and
            moments on the specified element(s).

        Notes
        -----
        Valid for MPC184 joint elements. See FJ for information on specifying
        forces and moments.
        """
        command = f"FJLIST,{elem}"
        return self.run(command, **kwargs)

    def flist(self, node1="", node2="", ninc="", **kwargs):
        """Lists force loads on the nodes.

        APDL Command: FLIST

        Parameters
        ----------
        node1, node2, ninc
            List forces for nodes NODE1 to NODE2 (defaults to NODE1) in steps
            of NINC (defaults to 1).  If ALL, list for all selected nodes
            [NSEL] and NODE2 and NINC  are ignored (default).  If NODE1 = P,
            graphical picking is enabled and all remaining command fields are
            ignored (valid only in the GUI).  A component name may also be
            substituted for NODE1.

        Notes
        -----
        Listing applies to the selected nodes [NSEL] and the selected force
        labels [DOFSEL].

        Caution:: : A list containing a node number that is larger than the
        maximum defined node (NODE2), could deplete the system memory and
        produce unpredictable results.

        This command is valid in any processor.
        """
        command = f"FLIST,{node1},{node2},{ninc}"
        return self.run(command, **kwargs)

    def fssect(self, rho="", nev="", nlod="", kbr="", **kwargs):
        """Calculates and stores total linearized stress components.

        APDL Command: FSSECT

        Parameters
        ----------
        rho
            In-plane (X-Y) average radius of curvature of the inside and
            outside surfaces of an axisymmetric section.  If zero (or blank), a
            plane or 3-D structure is assumed.  If nonzero, an axisymmetric
            structure is assumed.  Use a suitably large number (see the
            Mechanical APDL Theory Reference) or use -1 for an axisymmetric
            straight section.

        nev
            Event number to be associated with these stresses (defaults to 1).

        nlod
            Loading number to be associated with these stresses (defaults to
            1).

        kbr
            For an axisymmetric analysis (RHO ≠ 0):

            0 - Include the thickness-direction bending stresses

            1 - Ignore the thickness-direction bending stresses

            2 - Include the thickness-direction bending stress using the same formula as the Y
                (axial direction ) bending stress. Also use the same formula
                for the shear stress.

        Notes
        -----
        Calculates and stores the total linearized stress components at the
        ends of a section path [PATH] (as defined by the first two nodes with
        the PPATH command). The path must be entirely within the selected
        elements (that is, there must not be any element gaps along the path).
        Stresses are stored according to the fatigue event number and loading
        number specified.  Locations (one for each node) are associated with
        those previously defined for these nodes [FL] or else they are
        automatically defined.  Stresses are separated into six total
        components (SX through SXZ) and six membrane-plus-bending (SX through
        SXZ) components.  The temperature at each end point and the current
        time are also stored along with the total stress components.
        Calculations are made from the stresses currently in the database (last
        SET or LCASE command).  Stresses are stored as section coordinate
        components if axisymmetric or as global Cartesian coordinate components
        otherwise, regardless of the active results coordinate system [RSYS].
        The FSLIST command may be used to list stresses.  The FS command can be
        used to modify stored stresses.  See also the PRSECT and PLSECT
        commands for similar calculations.
        """
        command = f"FSSECT,{rho},{nev},{nlod},{kbr}"
        return self.run(command, **kwargs)

    def fscale(self, rfact="", ifact="", **kwargs):
        """Scales force load values in the database.

        APDL Command: FSCALE

        Parameters
        ----------
        rfact
            Scale factor for the real component.  Zero (or blank) defaults to
            1.0.  Use a small number for a zero scale factor.

        ifact
            Scale factor for the imaginary component.  Zero (or blank) defaults
            to 1.0.  Use a small number for a zero scale factor.

        Notes
        -----
        Scales force load (force, heat flow, etc.) values in the database.
        Scaling applies to the previously defined values for the selected nodes
        [NSEL] and the selected force labels [DOFSEL].  Issue FLIST command to
        review results.  Solid model boundary conditions are not scaled by this
        command, but boundary conditions on the FE model are scaled.

        Note:: : Such scaled FE boundary conditions may still be overwritten by
        unscaled solid model boundary conditions if a subsequent boundary
        condition transfer occurs.

        FSCALE does not work for tabular boundary conditions.

        This command is also valid in PREP7.
        """
        command = f"FSCALE,{rfact},{ifact}"
        return self.run(command, **kwargs)
