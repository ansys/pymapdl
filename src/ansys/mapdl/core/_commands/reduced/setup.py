class Setup:
    def rmresume(self, fname="", ext="", **kwargs):
        """Resumes ROM data from a file.

        APDL Command: RMRESUME

        Parameters
        ----------
        fname
            Name and directory path of the ROM database file (248 character
            maximum). Default to Jobname.

        ext
            Extension of the ROM database file. Default to .rom.

        Notes
        -----
        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"RMRESUME,{fname},{ext}"
        return self.run(command, **kwargs)

    def rmsave(self, fname="", ext="", **kwargs):
        """Saves ROM data to file.

        APDL Command: RMSAVE

        Parameters
        ----------
        fname
            Name and directory path of the ROM database file. Default to
            Jobname.

        ext
            Extension of the ROM database file. Default to .rom.

        Notes
        -----
        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        return self.run(f"RMSAVE,{fname},{ext}", **kwargs)
