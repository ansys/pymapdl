class Generation:
    def rmalist(self, **kwargs):
        """Lists all defined master nodes for a ROM method.

        APDL Command: RMALIST

        Notes
        -----
        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"RMALIST,"
        return self.run(command, **kwargs)

    def rmanl(self, fname="", ext="", dimn="", oper="", **kwargs):
        """Assigns model database, dimensionality, and operating

        APDL Command: RMANL
        direction for the ROM method.

        Parameters
        ----------
        fname
            Database file name and directory path  (248 characters maximum,
            including directory). The file name defaults to Jobname.

        ext
            File extension (8 character maximum). The extension defaults to db.

        dimn
            Model dimensionality:

            2 - 2-D models

            3 - 3-D Models

        oper
            Primary operating direction:

            X - direction

            Y - direction

            Z - direction

        Notes
        -----
        Required Inputs:

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        return self.run(f"RMANL,{fname},{ext},,{dimn},{oper}", **kwargs)

    def rmaster(self, node="", lab="", **kwargs):
        """Defines master nodes for the ROM method.

        APDL Command: RMASTER

        Parameters
        ----------
        node
            Node number at which master degree of freedom is defined  If Node =
            P, graphical picking is enabled and all remaining command fields
            are ignored (valid only in the GUI).

        lab
            Valid labels are "ADD" (default) and "DEL".

        Notes
        -----
        Defines master nodes for the ROM.  Master nodes are used to track the
        total displacement of a structure in the operating direction [RMANL].
        They may be used as attachment points for 1-D structural elements
        during a ROM use pass via the UX degree of freedom.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"RMASTER,{node},{lab}"
        return self.run(command, **kwargs)

    def rmcap(self, refname="", c1="", c2="", **kwargs):
        """Defines lumped capacitance pairs between conductors C1 and C2 for a ROM

        APDL Command: RMCAP
        method.

        Parameters
        ----------
        refname
            Reference name for capacitance pair definition.

        c1
            First conductor (between 1 and 5).

        c2
            Second conductor (between 1 and 5).

        Notes
        -----
        For a capacitance definition between conductor C1 and C2, node
        components COND%C1% and COND%C2% (see CM command) must be present
        containing the conductor nodes. If C1 and C2 are blank, the capacitance
        definition with RefName will be deleted.  (For example, if C1 = 1, and
        C2 = 2, then node components COND1 and COND2 must be defined).

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"RMCAP,{refname},{c1},{c2}"
        return self.run(command, **kwargs)

    def rmclist(self, **kwargs):
        """Lists all lumped capacitance pairs defined.

        APDL Command: RMCLIST

        Notes
        -----
        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"RMCLIST,"
        return self.run(command, **kwargs)

    def rmmlist(self, **kwargs):
        """Lists all mode specifications for the ROM method.

        APDL Command: RMMLIST

        Notes
        -----
        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"RMMLIST,"
        return self.run(command, **kwargs)

    def rmmrange(
        self,
        mode="",
        key="",
        min_="",
        max_="",
        nstep="",
        damp="",
        scale="",
        **kwargs,
    ):
        """Defines and edits various modal parameters for the ROM method.

        APDL Command: RMMRANGE

        Parameters
        ----------
        mode
            Mode number. Must be lower or equal to the number of modes
            extracted via the RMNEVEC command.

        key
            Mode classification key. Valid keys are:

            DOMINANT - Dominant mode

        min\_
            Lower bound for fit range of mode.

        max\_
            Upper bound for fit range of mode.

        nstep
            Number of equidistant steps in fit range of mode.

        damp
            Modal damping factor. Defaults to 0.0.

        scale
            Modal scaling factor.

        Notes
        -----
        When selected manually (RMMSELECT), modes must be classified as
        dominant, relevant, or unused. Dominant modes (Key = DOMINANT) are
        basis functions with large amplitudes. Relevant modes (Key = RELEVANT)
        are influenced by the dominant modes but do not cause interactions
        among themselves due to the small amplitude. This assumption leads to
        essential speed up of the sample point generator (see RMSMPLE).

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"RMMRANGE,{mode},{key},{min_},{max_},{nstep},{damp},{scale}"
        return self.run(command, **kwargs)

    def rmmselect(self, nmode="", method="", dmin="", dmax="", **kwargs):
        """Selects modes for the ROM method.

        APDL Command: RMMSELECT

        Parameters
        ----------
        nmode
            Total number of modes to be selected

        method
            Method for mode selection. Valid methods are:

            TMOD - Automated selection using a test load. TMOD must be enclosed in single quotes.

        dmin
            Lower bound for total deflection range.

        dmax
            Upper bound for total deflection range.

        Notes
        -----
        Select pertinent modes for use in a ROM. Pertinent mode selection may
        be enhanced by using the deflection state of the structure
        representative of the operating nature of the device (Method = TMOD). A
        static analysis with an applied Test Load may be used.  The test load
        displacements must be extracted at the neutral plane of the device (if
        the device is stress-stiffened), or at any plane of the device (non-
        stress-stiffened). A node component "NEUN" must be defined for the
        plane of nodes, and the displacements extracted using the RMNDISP
        command prior to issuing this command. If Method = NMOD, use the first
        Nmode eigenmodes to select the pertinent modes for the ROM tool. Only
        those modes are selected that act in the operating direction of the
        structure [RMANL].

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.

        jobname.evx, jobname.evy, jobname.evz, jobname.evn, jobname.evl

        Test load and element load neutral plane displacement files:
        jobname.tld, jobname.eld
        """
        command = f"RMMSELECT,{nmode},{method},{dmin},{dmax}"
        return self.run(command, **kwargs)

    def rmporder(
        self,
        ord1="",
        ord2="",
        ord3="",
        ord4="",
        ord5="",
        ord6="",
        ord7="",
        ord8="",
        ord9="",
        **kwargs,
    ):
        """Defines polynomial orders for ROM functions.

        APDL Command: RMPORDER

        Parameters
        ----------
        ord1, ord2, ord3, . . . , ord9
            Polynomial orders for modes. Ordi specifies the polynomial order
            for modei. Modes are ordered as extracted from a modal analysis
            using the RMNEVEC command.  Defaults to 0 if mode i is unused;
            default to nstep(i) -1 for dominant or relevant modes, where
            nstep(i) is the number of equidistant steps in fit range of mode i.
            nstep(i) is automatically set by RMMSELECT or modified by the
            RMMRANGE command.

        Notes
        -----
        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = (
            f"RMPORDER,{ord1},{ord2},{ord3},{ord4},{ord5},{ord6},{ord7},{ord8},{ord9}"
        )
        return self.run(command, **kwargs)

    def rmrgenerate(self, **kwargs):
        """Performs fitting procedure for all ROM functions to generate response

        APDL Command: RMRGENERATE
        surfaces.

        Notes
        -----
        The fitting procedure uses modal analysis data and function data
        generated using the RMSMPLE command and specifications set forth in the
        RMROPTIONS command. The files jobname_ijk.pcs (modes i, j, k) will be
        generated containing the coefficients of the response surfaces. These
        files are needed for the ROM Use Pass along with a ROM data base file
        [RMSAVE].

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.

        Strain energy and capacitance data file jobname_ijk.dec

        Response surface coefficients jobname_ijk.pcs (modes i, j, k)
        """
        command = f"RMRGENERATE,"
        return self.run(command, **kwargs)

    def rmroptions(self, refname="", type_="", invert="", **kwargs):
        """Defines options for ROM response surface fitting.

        APDL Command: RMROPTIONS

        Parameters
        ----------
        refname
            Reference name of ROM function to be fitted. Valid reference names
            are "SENE" for the strain energy of the structural domain and any
            capacitance reference name previously defined by means of RMCAP
            command for the electrostatic domain.

        type\_
            Type of fitting function to be applied for regression analysis.
            Valid types are:

            LAGRANGE - Lagrange type (default)

        invert
            Flag to specify whether data should be inverted prior to fitting.

            0 - Do not invert data (default for SENE)

        Notes
        -----
        The objective of response surface fit is to compute an analytical
        expression for the strain energy and the capacitance as functions of
        modal amplitudes.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"RMROPTIONS,{refname},{type_},{invert}"
        return self.run(command, **kwargs)

    def rmrplot(self, refname="", type_="", mode1="", mode2="", **kwargs):
        """Plots response surface of ROM function or its derivatives with respect

        APDL Command: RMRPLOT
        to the dominant mode(s).

        Parameters
        ----------
        refname
            Reference name of ROM function. Valid reference names are "SENE"
            for the strain energy of the mechanical domain and any capacitance
            definition, previously defined by means of the RMCAP command, for
            the electrostatic domain.

        type\_
            Type of data to be plotted. Valid types are:

            FUNC - Response surface (default)

        mode1
            First mode number (used for Type = "FIRST" and Type = "SECOND"
            only).

        mode2
            Second mode number (used for Type = "SECOND" only).

        Notes
        -----
        The objective of response surface fit is to compute an analytical
        expression for the strain energy and the capacitance as functions of
        modal amplitudes. This command assumes that the coefficient files
        jobnam_ijk.pcs are available [RMRGENERATE]. Visualization of the
        response surface will help to evaluate the validity of the function
        fit.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"RMRPLOT,{refname},{type_},{mode1},{mode2}"
        return self.run(command, **kwargs)

    def rmrstatus(self, refname="", **kwargs):
        """Prints status of response surface for ROM function.

        APDL Command: RMRSTATUS

        Parameters
        ----------
        refname
            Reference name of ROM function. Valid reference names are "SENE"
            for the strain energy of the mechanical domain and any capacitance
            reference names [RMCAP], for the electrostatic domain.

        Notes
        -----
        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"RMRSTATUS,{refname}"
        return self.run(command, **kwargs)

    def rmsmple(self, nlgeom="", cap="", seqslv="", eeqslv="", **kwargs):
        """Runs finite element solutions and obtains sample points for the ROM

        APDL Command: RMSMPLE
        method.

        Parameters
        ----------
        nlgeom
            Specify whether a large or small deflection analysis is to be
            performed for the  mechanical domain:

            OFF (or 0) - Perform small deflection analysis (default).

        cap
            Capacitance calculation method.

            CHARGE - Compute capacitance based on the charge voltage relationship (default).

        seqslv
            Solver for structural analysis:

            SPARSE - Sparse direct equation solver (default).

        eeqslv
            Solver for electrostatic analysis:

            SPARSE - Sparse direct equation solver (default).

        Notes
        -----
        This command prepares and runs multiple finite element solutions on the
        Structural domain and the Electrostatic domain of a model to collect
        sample points of data for ROM response curve fitting. The command
        requires a model database [RMANL] and two Physics Files (Structural
        domain, titled "STRU" and an Electrostatic domain, titled "ELEC"; see
        PHYSICS command). Also required is a complete ROM database generated
        from the ROM Tools.  The Cap = CHARGE method is preferred when
        capacitance to "infinity" is not required. Capacitance conductor pairs
        are defined by the RMCAP command.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.

        Strain energy and capacitance data files  jobname_ijk.dec (mode i, j,
        k).
        """
        command = f"RMSMPLE,{nlgeom},{cap},{seqslv},{eeqslv}"
        return self.run(command, **kwargs)

    def rmxport(self, **kwargs):
        """Exports ROM model to external VHDL-AMS simulator.

        APDL Command: RMXPORT

        Notes
        -----
        Use this command to generate all files necessary to run the ROM
        analysis in an external VHDL-AMS Simulator.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.

        VHDL files: Initial.vhd, S_ams_ijk.vhd, Cxxx_ams_ijk.vhd,
        transducer.vhd.
        """
        command = f"RMXPORT,"
        return self.run(command, **kwargs)
