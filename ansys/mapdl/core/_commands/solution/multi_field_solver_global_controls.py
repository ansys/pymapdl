class MultiFieldSolverGlobalControls:
    def mfanalysis(self, key="", **kwargs):
        """Activates or deactivates an ANSYS Multi-field solver analysis.

        APDL Command: MFANALYSIS

        Parameters
        ----------
        key
            Multifield analysis key:

            ON - Activates an ANSYS Multi-field solver analysis.

            OFF - Deactivates an ANSYS Multi-field solver analysis (default).

        Notes
        -----
        This command is also valid in PREP7.

        See Multi-field Commands in the Coupled-Field Analysis Guide for a list
        of all ANSYS Multi-field solver commands and their availability for MFS
        and MFX analyses.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"MFANALYSIS,{key}"
        return self.run(command, **kwargs)

    def mfclear(self, option="", value="", **kwargs):
        """Deletes ANSYS Multi-field solver analysis settings.

        APDL Command: MFCLEAR

        Parameters
        ----------
        option
            SOLU

            SOLU - Resets all ANSYS solution commands except KBC to their default states. This
                   option clears analysis options when setting up different
                   fields for an ANSYS Multi-field solver analysis.

            FIELD - Deletes all ANSYS Multi-field solver specifications for the specified field
                    number.

            SINT - Deletes all ANSYS Multi-field solver specifications for the specified surface
                   interface number.

            VINT - Deletes all ANSYS Multi-field solver specifications for the volumetric
                   interface number.

            ORD - Deletes the analysis order specified by the MFORDER command.

            EXT - Deletes external fields specified by the MFEXTER command

            MFLC - Deletes load transfers specified by the MFLCOMM command

        value
            Use only for Option = FIELD, SINT, or VINT.

        Notes
        -----
        See Multi-field Commands in the Coupled-Field Analysis Guide for a list
        of all ANSYS Multi-field solver commands and their availability for MFS
        and MFX analyses.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"MFCLEAR,{option},{value}"
        return self.run(command, **kwargs)

    def mffr(self, fname="", lab="", rfini="", rfmin="", rfmax="", **kwargs):
        """Setup Multi-Field relaxation factors for field solutions.

        APDL Command: MFFR

        Parameters
        ----------
        fname
            Field name (MFX) or number (MFS). Must be the ANSYS field (cannot
            be a CFX field).

        lab
            Label name. Valid values are DISP and TEMP.

        rfini
            Initial relaxation factor. Defaults to 0.75.

        rfmin
            Minimum relaxation factor. Defaults to RFINI.

        rfmax
            Maximum relaxation factor. Defaults to RFINI.

        Notes
        -----
        Use this command to relax the field solutions in fluid-solid
        interaction analyses and thermal-thermal analyses for a better
        convergence rate in coupled problems, especially cases that need
        dynamic relaxation. The ANSYS field that has the MFFR command applied
        will do only one nonlinear stagger iteration within each multi-field
        stagger; the convergence of the ANSYS field solver will be satisfied
        through multiple multi-field staggers. Note that the CFX field solver
        can have multiple iterations within the field solver; see the CFX
        documentation for more details. ANSYS will not terminate the nonlinear
        field solution until the ANSYS field solver converges or reaches the
        maximum number of multi-field staggers as specified on MFITER.

        The interface load relaxation (MFRELAX) will be automatically turned
        off for the corresponding surface loads that have MFFR applied. The
        automatic change of the relaxation factor for accelerating the
        nonlinear convergence of the coupled field solution is based on
        Aitken's acceleration scheme.

        This command is valid only with coupled problems involving surface load
        transfer only. No subcycling is allowed for the field solver if using
        this command.
        """
        command = f"MFFR,{fname},{lab},{rfini},{rfmin},{rfmax}"
        return self.run(command, **kwargs)

    def mfinter(self, option="", **kwargs):
        """Specifies the interface load transfer interpolation option for an ANSYS

        APDL Command: MFINTER
        Multi-field solver analysis.

        Parameters
        ----------
        option
            Interface load transfer option:

            CONS - Conservative formulation for load transfer.

            NONC - Nonconservative formulation for load transfer (default).

        Notes
        -----
        This command only applies to the interpolation method for forces, heat
        flux, and heat generation. Displacement and temperature transfers are
        always nonconservative.

        For more information on conservative and nonconservative load transfer,
        see Load Transfer in the Coupled-Field Analysis Guide.

        This command is also valid in PREP7.

        See Multi-field Commands in the Coupled-Field Analysis Guide for a list
        of all ANSYS Multi-field solver commands and their availability for MFS
        and MFX analyses.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"MFINTER,{option}"
        return self.run(command, **kwargs)

    def mflist(self, option="", value="", **kwargs):
        """Lists the settings for an ANSYS Multi-field solver analysis.

        APDL Command: MFLIST

        Parameters
        ----------
        option
            ALL

            ALL - Lists all ANSYS Multi-field solver analysis options.

            SOLU - Lists all solution-related ANSYS Multi-field solver options.

            FIELD - Lists all ANSYS Multi-field solver options related to the specified field
                    number.

            SINT - Lists all surface interface information for the specified surface interface
                   number.

            VINT - Lists all volumetric interface information for the specified volumetric
                   interface number.

        value
            Use only for Option = FIELD, SINT, or VINT.

        Notes
        -----
        This command is also valid in PREP7.

        See Multi-field Commands in the Coupled-Field Analysis Guide for a list
        of all ANSYS Multi-field solver commands and their availability for MFS
        and MFX analyses.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"MFLIST,{option},{value}"
        return self.run(command, **kwargs)

    def mforder(
        self,
        fnumb1="",
        fnumb2="",
        fnumb3="",
        fnumb4="",
        fnumb5="",
        fnumb6="",
        fnumb7="",
        fnumb8="",
        fnumb9="",
        fnumb10="",
        fnumb11="",
        fnumb12="",
        fnumb13="",
        fnumb14="",
        fnumb15="",
        fnumb16="",
        fnumb17="",
        fnumb18="",
        fnumb19="",
        fnumb20="",
        **kwargs,
    ):
        """Specifies field solution order for an ANSYS Multi-field solver

        APDL Command: MFORDER
        analysis.

        Parameters
        ----------
        fnumb1, fnumb2, fnumb3, . . . , fnumb20
            Field numbers defined by the MFELEM command.

        Notes
        -----
        You can define up to twenty fields in an ANSYS Multi-field solver
        analysis.

        This command is also valid in PREP7.

        See Multi-field Commands in the Coupled-Field Analysis Guide for a list
        of all ANSYS Multi-field solver commands and their availability for MFS
        and MFX analyses.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"MFORDER,{fnumb1},{fnumb2},{fnumb3},{fnumb4},{fnumb5},{fnumb6},{fnumb7},{fnumb8},{fnumb9},{fnumb10},{fnumb11},{fnumb12},{fnumb13},{fnumb14},{fnumb15},{fnumb16},{fnumb17},{fnumb18},{fnumb19},{fnumb20}"
        return self.run(command, **kwargs)

    def mfpsimul(self, gname="", fname1="", fname2="", **kwargs):
        """Sets up a field solver group to simultaneously process with code

        APDL Command: MFPSIMUL
        coupling analyses.

        Parameters
        ----------
        gname
            Sets the group name with a character string of up to 80 characters.

        fname1, fname2
            Sets the field solver 1 and field solver 2 names, which are
            processed simultaneously, with a character string of up to 80
            characters.

        Notes
        -----
        This command is used to define a group of simultaneously-processed
        field solvers in an MFX analysis. For example, to define group g1 with
        field solvers ansys-code and cfx-code, enter MFPS,g1,ansys-code,cfx-
        code.

        To indicate groups of sequentially-processed field solvers for your MFX
        analysis, create two groups (g1 and g2).

        A field solver refers to a specific instance of an ANSYS or CFX solver
        execution that is defined by the respective input file(s) referenced
        when starting the solver (through the launcher or from the command
        line). The field solver names that are referenced in several MFX
        commands must be consistent with the names that will be used when
        starting the coupled simulation.

        Note:: : When running MFX from the launcher, you must use ANSYS and CFX
        (uppercase) as the field solver names (MFPSIMUL) in your input file.

        See Multi-field Commands in the Coupled-Field Analysis Guide for a list
        of all ANSYS Multi-field solver commands and their availability for MFS
        and MFX analyses.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"MFPSIMUL,{gname},{fname1},{fname2}"
        return self.run(command, **kwargs)

    def mfsorder(self, gname1="", gname2="", **kwargs):
        """Sets up the solution sequence of simultaneous field solver groups for

        APDL Command: MFSORDER
        code coupling analyses.

        Parameters
        ----------
        gname1, gname2
            Specifies the group name for groups defined by the MFPSIMUL command
            with a character string of up to 80 characters.

        Notes
        -----
        See Multi-field Commands in the Coupled-Field Analysis Guide for a list
        of all ANSYS Multi-field solver commands and their availability for MFS
        and MFX analyses.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"MFSORDER,{gname1},{gname2}"
        return self.run(command, **kwargs)

    def mfwrite(self, fname="", ext="", **kwargs):
        """Writes an ANSYS master input file for MFX multiple code coupling.

        APDL Command: MFWRITE

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
        When working interactively, you need to issue this command as the last
        step in your setup process. This command will write out the input file
        that you will then use to submit the MFX analysis. This file will
        include the /SOLU, SOLVE, and FINISH commands.

        See Multi-field Commands in the Coupled-Field Analysis Guide for a list
        of all ANSYS Multi-field solver commands and their availability for MFS
        and MFX analyses.
        """
        command = f"MFWRITE,{fname},{ext}"
        return self.run(command, **kwargs)
