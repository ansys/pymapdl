class MultiFieldSolverDefinitionCommands:
    def mfcmmand(self, fnumb="", fname="", ext="", **kwargs):
        """Captures field solution options in a command file.

        APDL Command: MFCMMAND

        Parameters
        ----------
        fnumb
            Field number specified by the MFELEM command.

        fname
            Command file name specified for the field number. Defaults to field
            "FNUMB".

        ext
            Extension for Fname. Defaults to .cmd.

        Notes
        -----
        All relevant solution option commands for the specified field are
        written to a file with the extension .cmd. Refer to the commands in the
        following tables in the Command Reference: Analysis Options, Nonlinear
        Options, Dynamic Options, and Load Step Options.

        This command is also valid in PREP7.

        See Multi-field Commands in the Coupled-Field Analysis Guide for a list
        of all ANSYS Multi-field solver commands and their availability for MFS
        and MFX analyses.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"MFCMMAND,{fnumb},{fname},{ext}"
        return self.run(command, **kwargs)

    def mfelem(
        self,
        fnumb="",
        itype1="",
        itype2="",
        itype3="",
        itype4="",
        itype5="",
        itype6="",
        itype7="",
        itype8="",
        itype9="",
        itype10="",
        **kwargs,
    ):
        """Defines a field by grouping element types.

        APDL Command: MFELEM

        Parameters
        ----------
        fnumb
            Field number for a group of element types.

        itype1, itype2, itype3, . . . , itype10
            Element types defined by the ET command.

        Notes
        -----
        You can define up to ten element types per field.

        Define only element types that contain elements in the field. Do not
        include MESH200 because it is a "mesh-only" element that does not
        contribute to the solution.

        This command is also valid in PREP7.

        See Multi-field Commands in the Coupled-Field Analysis Guide for a list
        of all ANSYS Multi-field solver commands and their availability for MFS
        and MFX analyses.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"MFELEM,{fnumb},{itype1},{itype2},{itype3},{itype4},{itype5},{itype6},{itype7},{itype8},{itype9},{itype10}"
        return self.run(command, **kwargs)

    def mfem(
        self,
        fnumb="",
        itype1="",
        itype2="",
        itype3="",
        itype4="",
        itype5="",
        itype6="",
        itype7="",
        itype8="",
        itype9="",
        itype10="",
        **kwargs,
    ):
        """Add more element types to a previously defined field number.

        APDL Command: MFEM

        Parameters
        ----------
        fnumb
            Existing field number defined by the MFELEM command.

        itype1, itype2, itype3, . . . , itype10
            Element types defined by the ET command.

        Notes
        -----
        You can add up to ten element types per MFEM command. This command
        should not be used after an initial solution.

        This command is also valid in PREP7.

        See Multi-field Commands in the Coupled-Field Analysis Guide for a list
        of all ANSYS Multi-field solver commands and their availability for MFS
        and MFX analyses.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"MFEM,{fnumb},{itype1},{itype2},{itype3},{itype4},{itype5},{itype6},{itype7},{itype8},{itype9},{itype10}"
        return self.run(command, **kwargs)

    def mfexter(
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
        """Defines external fields for an ANSYS Multi-field solver analysis.

        APDL Command: MFEXTER

        Parameters
        ----------
        fnumb1, fnumb2, fnumb3, . . . , fnumb20
            External field numbers defined by the MFELEM command.

        Notes
        -----
        This command specifies external field numbers to be used for load
        transfer in an ANSYS Multi-field solver analysis. Use the MFIMPORT
        command to import the external fields.

        Use the MFELEM command to specify external field numbers. Use the
        MFORDER command to specify the solution order for the external fields.

        You can define a maximum of 20 fields.

        This command is also valid in PREP7.

        See Multi-field Commands in the Coupled-Field Analysis Guide for a list
        of all ANSYS Multi-field solver commands and their availability for MFS
        and MFX analyses.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"MFEXTER,{fnumb1},{fnumb2},{fnumb3},{fnumb4},{fnumb5},{fnumb6},{fnumb7},{fnumb8},{fnumb9},{fnumb10},{fnumb11},{fnumb12},{fnumb13},{fnumb14},{fnumb15},{fnumb16},{fnumb17},{fnumb18},{fnumb19},{fnumb20}"
        return self.run(command, **kwargs)

    def mffname(self, fnumb="", fname="", **kwargs):
        """Specifies a file name for a field in an ANSYS Multi-field solver

        APDL Command: MFFNAME
        analysis.

        Parameters
        ----------
        fnumb
            Field number specified by the MFELEM command.

        fname
            File name. Defaults to field "FNUMB".

        Notes
        -----
        All files created for the field will have this file name with the
        appropriate extensions.

        This command is also valid in PREP7.

        See Multi-field Commands in the Coupled-Field Analysis Guide for a list
        of all ANSYS Multi-field solver commands and their availability for MFS
        and MFX analyses.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"MFFNAME,{fnumb},{fname}"
        return self.run(command, **kwargs)
