class MasterDOF:
    def m(
        self,
        node="",
        lab1="",
        nend="",
        ninc="",
        lab2="",
        lab3="",
        lab4="",
        lab5="",
        lab6="",
        **kwargs,
    ):
        """Defines master degrees of freedom for superelement generation analyses.

        APDL Command: M

        Parameters
        ----------
        node
            Node number at which master degree of freedom is defined.  If ALL,
            define master degrees of freedom at all selected nodes (NSEL).  If
            NODE = P, graphical picking is enabled and all remaining command
            fields are ignored (valid only in the GUI).  A component name may
            also be substituted for NODE.

        lab1
            Valid degree of freedom label. If ALL, use all appropriate labels.
            Structural labels:  UX, UY, or UZ (displacements); ROTX, ROTY, or
            ROTZ (rotations). Thermal labels: TEMP, TBOT, TE2, TE3, . . ., TTOP
            (temperature).  Electric labels:  VOLT (voltage).

        nend, ninc
            Define all nodes from NODE to NEND (defaults to NODE) in steps of
            NINC (defaults to 1) as master degrees of freedom in the specified
            direction.

        lab2, lab3, lab4, . . . , lab6
            Additional master degree of freedom labels.  The nodes defined are
            associated with each label specified.

        Notes
        -----
        Defines master degrees of freedom (MDOF) for superelement generation.
        If defined for other analyses, MDOF are ignored.  If used in SOLUTION,
        this command is valid only within the first load step.

        Repeat M command for additional master degrees of freedom.  The limit
        for the number of master nodes used is determined by the maximum system
        memory available.

        The substructure (ANTYPE,SUBSTR) analysis utilizes the matrix
        condensation technique to reduce the structure matrices to those
        characterized by a set of master degrees of freedom.

        Master degrees of freedom are identified by a list of nodes and their
        nodal directions.  The actual degree of freedom directions available
        for a particular node depends upon the degrees of freedom associated
        with element types (ET) at that node.  There must be some mass (or
        stress stiffening in the case of the buckling analysis) associated with
        each master degree of freedom (except for the VOLT label).  The mass
        may be due either to the distributed mass of the element or due to
        discrete lumped masses at the node.  If a master degree of freedom is
        specified at a constrained point, it is ignored.  If a master degree of
        freedom is specified at a coupled node, it should be specified at the
        prime node of the coupled set.

        Substructure analysis connection points must be defined as master
        degrees of freedom.

        This command is also valid in PREP7.
        """
        command = f"M,{node},{lab1},{nend},{ninc},{lab2},{lab3},{lab4},{lab5},{lab6}"
        return self.run(command, **kwargs)

    def mdele(
        self,
        node="",
        lab1="",
        nend="",
        ninc="",
        lab2="",
        lab3="",
        lab4="",
        lab5="",
        lab6="",
        **kwargs,
    ):
        """Deletes master degrees of freedom.

        APDL Command: MDELE

        Parameters
        ----------
        node, lab1, nend, ninc
            Delete master degrees of freedom in the Lab1 direction [M] from
            NODE to NEND (defaults to NODE) in steps of NINC (defaults to 1).
            If NODE = ALL, NEND and NINC are ignored and masters for all
            selected nodes [NSEL] are deleted.  If Lab1 = ALL, all label
            directions will be deleted.  If NODE = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in
            the GUI).  A component name may also be substituted for NODE.

        lab2, lab3, lab4, . . . , lab6
            Delete masters in these additional directions.

        Notes
        -----
        Deletes master degrees of freedom.  If used in SOLUTION, this command
        is valid only within the first load step.

        This command is also valid in PREP7.
        """
        command = (
            f"MDELE,{node},{lab1},{nend},{ninc},{lab2},{lab3},{lab4},{lab5},{lab6}"
        )
        return self.run(command, **kwargs)

    def mgen(self, itime="", inc="", node1="", node2="", ninc="", **kwargs):
        """Generates additional MDOF from a previously defined set.

        APDL Command: MGEN

        Parameters
        ----------
        itime, inc
            Do this generation operation a total of ITIMEs, incrementing all
            nodes in the set by INC each time after the first.  ITIME must be >
            1 for generation to occur.  All previously defined master degree of
            freedom directions are included in the set.  A component name may
            also be substituted for ITIME.

        node1, node2, ninc
            Generate master degrees of freedom from set beginning with NODE1 to
            NODE2 (defaults to NODE1) in steps of NINC (defaults to 1).  If
            NODE1 = ALL, NODE2 and NINC are ignored and set is all selected
            nodes [NSEL].  If NODE1 = P, graphical picking is enabled and all
            remaining command fields are ignored (valid only in the GUI).

        Notes
        -----
        Generates additional master degrees of freedom from a previously
        defined set.  If used in SOLUTION, this command is valid only within
        the first load step.

        This command is also valid in PREP7.
        """
        command = f"MGEN,{itime},{inc},{node1},{node2},{ninc}"
        return self.run(command, **kwargs)

    def mlist(self, node1="", node2="", ninc="", **kwargs):
        """Lists the MDOF of freedom.

        APDL Command: MLIST

        Parameters
        ----------
        node1, node2, ninc
            List master degrees of freedom from NODE1 to NODE2 (defaults
            toNODE1) in steps of NINC (defaults to 1).  If NODE1 = ALL
            (default), NODE2 and NINC are ignored and masters for all selected
            nodes [NSEL] are listed.  If NODE1 = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in
            the GUI).  A component name may also be substituted for NODE1
            (NODE2 and NINC are ignored).

        Notes
        -----
        Lists the master degrees of freedom.
        """
        command = f"MLIST,{node1},{node2},{ninc}"
        return self.run(command, **kwargs)
