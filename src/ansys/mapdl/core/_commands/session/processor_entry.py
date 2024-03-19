"""These SESSION commands are used to enter and exit the various
processors in the program.
"""


class ProcessorEntry:
    def aux2(self, **kwargs):
        """Enters the binary file dumping processor.

        APDL Command: /AUX2

        Notes
        -----
        Enters the binary file dumping processor (ANSYS auxiliary processor
        AUX2).  This processor is used to dump the contents of certain ANSYS
        binary files for visual examination.

        This command is valid only at the Begin Level.
        """
        command = "/AUX2,"
        return self.run(command, **kwargs)

    def aux3(self, **kwargs):
        """Enters the results file editing processor.

        APDL Command: /AUX3

        Notes
        -----
        Enters the results file editing processor (ANSYS auxiliary processor
        AUX3).  This processor is used to edit ANSYS results files.

        This command is valid only at the Begin Level.
        """
        command = "/AUX3,"
        return self.run(command, **kwargs)

    def aux12(self, **kwargs):
        """Enters the radiation processor.

        APDL Command: /AUX12

        Notes
        -----
        Enters the radiation processor (ANSYS auxiliary processor AUX12).  This
        processor supports the Radiation Matrix and the Radiosity Solver
        methods.

        This command is valid only at the Begin Level.
        """
        command = "/AUX12,"
        return self.run(command, **kwargs)

    def aux15(self, **kwargs):
        """Enters the IGES file transfer processor.

        APDL Command: /AUX15

        Notes
        -----
        Enters the IGES file transfer processor (ANSYS auxiliary processor
        AUX15), used to read an IGES data file into the ANSYS program.

        This command is valid only at the Begin Level.
        """
        command = "/AUX15,"
        return self.run(command, **kwargs)

    def finish(self, **kwargs):
        """Exits normally from a processor.

        APDL Command: FINISH

        Notes
        -----
        Exits any of the ANSYS processors or the DISPLAY program.  For the
        ANSYS processors, data will remain intact in the database but the
        database is not automatically written to a file (use the SAVE command
        to write the database to a file).  See also the /QUIT command for an
        alternate processor exit command.  If exiting POST1, POST26, or OPT,
        see additional notes below.

        POST1:  Data in the database will remain intact, including the POST1
        element table data, the path table data, the fatigue table data, and
        the load case pointers.

        POST26:  Data in the database will remain intact, except that POST26
        variables are erased and specification commands (such as FILE, PRTIME,
        NPRINT, etc.) are reset.  Use the /QUIT command to exit the processor
        and bypass these exceptions.

        This command is valid in any processor.  This command is not valid at
        the Begin level.
        """
        command = "FINISH,"
        return self.run(command, **kwargs)

    def post1(self, **kwargs):
        """Enters the database results postprocessor.

        APDL Command: /POST1

        Notes
        -----
        Enters the general database results postprocessor (POST1).  All load
        symbols (/PBC, /PSF, or /PBF) are automatically turned off with this
        command.

        This command is valid only at the Begin Level.
        """
        command = "/POST1,"
        return self.run(command, **kwargs)

    def post26(self, **kwargs):
        """Enters the time-history results postprocessor.

        APDL Command: /POST26

        Notes
        -----
        Enters the time-history results postprocessor (POST26).

        This command is valid only at the Begin Level.
        """
        command = "/POST26,"
        return self.run(command, **kwargs)

    def prep7(self, **kwargs):
        """Enters the model creation preprocessor.

        APDL Command: /PREP7

        Notes
        -----
        Enters the general input data preprocessor (PREP7).

        This command is valid only at the Begin Level.
        """
        command = "/PREP7,"
        return self.run(command, **kwargs)

    def quit(self, **kwargs):
        """Exits a processor.

        APDL Command: /QUIT

        Notes
        -----
        This is an alternative to the FINISH command.  If any cleanup or file
        writing is normally done by the FINISH command, it is bypassed if the
        /QUIT command is used instead.  A new processor may be entered after
        this command.  See the /EXIT command to terminate the run.

        This command is valid in any processor.  This command is not valid at
        the Begin level.
        """
        command = "/QUIT,"
        return self.run(command, **kwargs)

    def slashsolu(self, **kwargs):
        """Enters the solution processor.

        APDL Command: /SOLU

        Notes
        -----
        This command is valid only at the Begin Level.
        """
        command = "/SOLU,"
        return self.run(command, **kwargs)
