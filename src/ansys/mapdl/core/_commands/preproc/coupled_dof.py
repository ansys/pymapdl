class CoupledDOF:
    def cp(
        self,
        nset="",
        lab="",
        node1="",
        node2="",
        node3="",
        node4="",
        node5="",
        node6="",
        node7="",
        node8="",
        node9="",
        node10="",
        node11="",
        node12="",
        node13="",
        node14="",
        node15="",
        node16="",
        node17="",
        **kwargs,
    ):
        """Defines (or modifies) a set of coupled degrees of freedom.

        APDL Command: CP

        Parameters
        ----------
        nset
            Set reference number:

            n - Arbitrary set number.

            HIGH - The highest defined coupled set number will be used (default, unless Lab =
                   ALL).  This option is useful when adding nodes to an
                   existing set.

            NEXT - The highest defined coupled set number plus one will be used (default if Lab =
                   ALL).  This option automatically numbers coupled sets so
                   that existing sets are not modified.

        lab
            Degree of freedom label for coupled nodes (in the nodal coordinate
            system).  Defaults to label previously defined with NSET if set
            NSET already exists. A different label redefines the previous label
            associated with NSET.  Valid labels are: Structural labels:  UX,
            UY, or UZ (displacements); ROTX, ROTY, or ROTZ (rotations) (in
            radians); HDSP (hydrostatic pressure). Thermal labels: TEMP, TBOT,
            TE2, TE3, . . ., TTOP (temperature).  Fluid labels:  PRES
            (pressure);  VX, VY, or VZ (velocities).  Electric labels:  VOLT
            (voltage);  EMF (electromotive force drop);  CURR (current).
            Magnetic labels:  MAG (scalar magnetic potential); AX, AY, or AZ
            (vector magnetic potentials);  CURR (current). Diffusion label:
            CONC (concentration). Explicit analysis labels:  UX, UY, or UZ
            (displacements).

        node1, node2, node3, . . . , node17
            List of nodes to be included in set. Duplicate nodes are ignored.
            If a node number is input as negative, the node is deleted from the
            coupled set. The first node in the list is the primary (retained)
            node, and the remaining nodes represent the removed degrees of
            freedom. If NODE1 = ALL, NODE2 through NODE17 are ignored and all
            selected nodes (NSEL) are included in the set.  If NODE1 = P,
            graphical picking is enabled and all remaining command fields are
            ignored (valid only in the GUI).  A component name may also be
            substituted for NODE1.

        Notes
        -----
        Do not include the same degree of freedom in more than one coupled set.
        Repeat CP command for additional nodes.

        Coupling degrees of freedom into a set causes the results calculated
        for one member of the set to be the same for all members of the set.
        Coupling can be used to model various joint and hinge effects.  A more
        general form of coupling can be done with constraint equations (CE).
        For structural analyses, a list of nodes is defined along with the
        nodal directions in which these nodes are to be coupled.  As a result
        of this coupling, these nodes are forced to take the same displacement
        in the specified nodal coordinate direction.  The amount of the
        displacement is unknown until the analysis is completed.  A set of
        coupled nodes which are not coincident, or which are not along the line
        of the coupled displacement direction, may produce an applied moment
        which will not appear in the reaction forces.  The actual degrees of
        freedom available for a particular node depends upon the degrees of
        freedom associated with element types (ET) at that node. For scalar
        field analysis, this command is used to couple nodal temperatures,
        pressures, voltages, etc.

        For an explicit dynamic analysis, the only valid DOF labels for
        coupling are UX, UY, and UZ. Since the rotational DOF (ROTX, ROTY,
        ROTZ) are not allowed. The CP family of commands should not be used in
        an explicit analysis to model rigid body behavior that involves
        rotations. If CP is used in this manner, it could lead to nonphysical
        responses.

        A set of coupled nodes which are not coincident, or which are not along
        the line of the coupled displacement direction, produce an artificial
        moment constraint.  If the structure rotates, a moment may be produced
        in the coupled set in the form of a force couple.  This moment is in
        addition to the real reaction forces and may make it appear that moment
        equilibrium is not satisfied by just the applied forces and the
        reaction forces. Note, however, that in an explicit dynamic analysis,
        this artificial moment will not be produced. Rather, just the applied
        forces and the reaction forces will satisfy the moment equilibrium in
        the model. Thus, in an explicit analysis, the magnitude of nodal
        displacements for this set of nodes will depend on the distance from
        each node to the center of the coupled set, and the direction of
        displacement will depend on the resulting moment. This may lead to a
        nonphysical response in some cases.

        Additional sets of coupled nodes may be generated from a specified set.
        Degrees of freedom are coupled within a set but are not coupled between
        sets.  No degree of freedom should appear in more than one coupled set.
        Such an appearance would indicate that at least two sets were in fact
        part of a single larger set.  The first degree of freedom of the
        coupled set is the "prime" degree of freedom.  All other degrees of
        freedom in the coupled sets are eliminated from the solution matrices
        by their relationship to the prime degree of freedom.  Forces applied
        to coupled nodes (in the coupled degree of freedom direction) will be
        summed and applied to the prime degree of freedom.  Output forces are
        also summed at the prime degree of freedom.  Degrees of freedom with
        specified constraints (D) should not be included in a coupled set
        (unless the degree of freedom is prime).

        If master degrees of freedom are defined for coupled nodes, only the
        prime degree of freedom should be so defined. The use of coupled nodes
        reduces the set of coupled degrees of freedom to only one degree of
        freedom.

        The removed degrees of freedom defined by the CP command cannot be
        included in any CE or CERIG command.
        """
        command = f"CP,{nset},{lab},{node1},{node2},{node3},{node4},{node5},{node6},{node7},{node8},{node9},{node10},{node11},{node12},{node13},{node14},{node15},{node16},{node17}"
        return self.run(command, **kwargs)

    def cpdele(self, nset1="", nset2="", ninc="", nsel="", **kwargs):
        """Deletes coupled degree of freedom sets.

        APDL Command: CPDELE

        Parameters
        ----------
        nset1, nset2, ninc
            Delete coupled sets from NSET1 to NSET2 (defaults to NSET1) in
            steps of NINC (defaults to 1).  If NSET1 = ALL, NSET2 and NINC are
            ignored and all coupled sets are deleted.

        nsel
            Additional node selection control:

            ANY - Delete coupled set if any of the selected nodes are in the set (default).

            ALL - Delete coupled set only if all of the selected nodes are in the set.

        Notes
        -----
        See the CP command for a method to delete individual nodes from a set.
        """
        command = f"CPDELE,{nset1},{nset2},{ninc},{nsel}"
        return self.run(command, **kwargs)

    def cpintf(self, lab="", toler="", **kwargs):
        """Defines coupled degrees of freedom at an interface.

        APDL Command: CPINTF

        Parameters
        ----------
        lab
            Degree of freedom label for coupled nodes (in the nodal coordinate
            system). If ALL, use all appropriate labels except HDSP.  Valid
            labels are: Structural labels:  UX, UY, or UZ (displacements);
            ROTX, ROTY, or ROTZ (rotations, in radians), HDSP (hydrostatic
            pressure).  Thermal labels: TEMP, TBOT, TE2, TE3, . . ., TTOP
            (temperature).  Fluid labels:  PRES (pressure);  VX, VY, or VZ
            (velocities).  Electric labels:  VOLT (voltage);  EMF
            (electromotive force drop);  CURR (current).  Magnetic labels:  MAG
            (scalar magnetic potential); AX, AY, or AZ (vector magnetic
            potentials);  CURR (current). Diffusion label: CONC
            (concentration).

        toler
            Tolerance for coincidence (based on maximum coordinate difference
            in each global Cartesian direction for node locations and on angle
            differences for node orientations).  Defaults to 0.0001.   Only
            nodes within the tolerance are considered to be coincident for
            coupling.

        Notes
        -----
        Defines coupled degrees of freedom between coincident nodes (within a
        tolerance).  May be used, for example, to "button" together elements
        interfacing at a seam, where the seam consists of a series of node
        pairs.  One coupled set is generated for each selected degree of
        freedom for each pair of coincident nodes.  For more than two
        coincident nodes in a cluster, a coupled set is generated from the
        lowest numbered node to each of the other nodes in the cluster.
        Coupled sets are generated only within (and not between) clusters.  If
        fewer than all nodes are to be checked for coincidence, use the NSEL
        command to select nodes.  Coupled set reference numbers are incremented
        by one from the highest previous set number.  Use CPLIST to display the
        generated sets.  Only nodes having the same nodal coordinate system
        orientations ("coincident" within a tolerance) are included.  Use the
        CEINTF command to connect nodes by constraint equations instead of by
        coupling.  Use the EINTF command to connect nodes by line elements
        instead of by coupling.
        """
        command = f"CPINTF,{lab},{toler}"
        return self.run(command, **kwargs)

    def cplgen(self, nsetf="", lab1="", lab2="", lab3="", lab4="", lab5="", **kwargs):
        """Generates sets of coupled nodes from an existing set.

        APDL Command: CPLGEN

        Parameters
        ----------
        nsetf
            Generate sets from existing set NSETF.

        lab1, lab2, lab3, . . . , lab5
            Generate sets with these labels (see CP command for valid labels).
            Sets are numbered as the highest existing set number + 1.

        Notes
        -----
        Generates additional sets of coupled nodes (with different labels) from
        an existing set [CP, CPNGEN].  The same node numbers are included in
        the generated sets.  If all labels of nodes are to be coupled and the
        nodes are coincident, the NUMMRG command should be used to
        automatically redefine the node number (for efficiency).
        """
        command = f"CPLGEN,{nsetf},{lab1},{lab2},{lab3},{lab4},{lab5}"
        return self.run(command, **kwargs)

    def cplist(self, nset1="", nset2="", ninc="", nsel="", **kwargs):
        """Lists the coupled degree of freedom sets.

        APDL Command: CPLIST

        Parameters
        ----------
        nset1, nset2, ninc
            List coupled sets from NSET1 to NSET2 (defaults to NSET1) in steps
            of NINC (defaults to 1).  If NSET1 = ALL (default), NSET2 and NINC
            are ignored and all coupled sets are listed.

        nsel
            Node selection control:

            ANY - List coupled set if any of the selected nodes are in the set (default).

            ALL - List coupled set only if all of the selected nodes are in the set.

        Notes
        -----
        This command is valid in any processor.
        """
        command = f"CPLIST,{nset1},{nset2},{ninc},{nsel}"
        return self.run(command, **kwargs)

    def cpmerge(self, lab="", **kwargs):
        """Merges different couple sets with duplicate degrees of freedom into one

        APDL Command: CPMERGE
        couple set.

        Parameters
        ----------
        lab
            Degree of freedom label for coupled nodes (in the nodal coordinate
            system).  Valid labels are: Structural labels:  UX, UY, or UZ
            (displacements); ROTX, ROTY, or ROTZ (rotations) (in radians).
            Thermal labels: TEMP, TBOT, TE2, TE3, . . ., TTOP (temperature).
            Fluid labels:  PRES (pressure);  VX, VY, or VZ (velocities).
            Electric labels:  VOLT (voltage);  EMF (electromotive force drop);
            CURR (current).  Magnetic labels:  MAG (scalar magnetic potential);
            AX, AY, or AZ (vector magnetic potentials);  CURR (current).
            Diffusion label: CONC (concentration). Explicit analysis labels:
            UX, UY, or UZ (displacements).  The degree of freedom set is
            determined from all element types defined and the DOF command, if
            used.
        """
        command = f"CPMERGE,{lab}"
        return self.run(command, **kwargs)

    def cpngen(self, nset="", lab="", node1="", node2="", ninc="", **kwargs):
        """Defines, modifies, or adds to a set of coupled degrees of freedom.

        APDL Command: CPNGEN

        Parameters
        ----------
        nset
            Set reference number [CP].

        lab
            Degree of freedom label [CP].

        node1, node2, ninc
            Include in coupled set nodes NODE1 to NODE2 in steps of NINC
            (defaults to 1).  If NODE1 = P, graphical picking is enabled and
            all remaining command fields are ignored (valid only in the GUI).
            If -NODE1, delete range of nodes from set instead of including.  A
            component name may also be substituted for NODE1 (NODE2 and NINC
            are ignored).

        Notes
        -----
        Defines, modifies, or adds to a set of coupled degrees of freedom.  May
        be used in combination with (or in place of) the CP command.  Repeat
        CPNGEN command for additional nodes.
        """
        command = f"CPNGEN,{nset},{lab},{node1},{node2},{ninc}"
        return self.run(command, **kwargs)

    def cpsgen(self, itime="", inc="", nset1="", nset2="", ninc="", **kwargs):
        """Generates sets of coupled nodes from existing sets.

        APDL Command: CPSGEN

        Parameters
        ----------
        itime, inc
            Do this generation operation a total of ITIMEs, incrementing all
            nodes in the existing sets by INC each time after the first.  ITIME
            must be > 1 for generation to occur.

        nset1, nset2, ninc
            Generate sets from sets beginning with NSET1 to NSET2 (defaults to
            NSET1) in steps of NINC (defaults to 1).  If NSET1 is negative,
            NSET2 and NINC are ignored and the last ``|NSET1|`` sets (in sequence
            from the maximum set number) are used as the sets to be repeated.

        Notes
        -----
        Generates additional sets of coupled nodes (with the same labels) from
        existing sets.  Node numbers between sets may be uniformly incremented.
        """
        command = f"CPSGEN,{itime},{inc},{nset1},{nset2},{ninc}"
        return self.run(command, **kwargs)
