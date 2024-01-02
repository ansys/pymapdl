class BinDump:
    def dump(self, nstrt="", nstop="", **kwargs):
        """Dumps the contents of a binary file.

        APDL Command: DUMP

        Parameters
        ----------
        nstrt, nstop
            Dump file from record NSTRT (defaults to 1) to NSTOP (defaults to
            NSTRT).  If NSTRT = HEAD, dump only record 1 of the file (NSTOP and
            the format specification are ignored).  If NSTRT = ALL, dump the
            entire file.

        Notes
        -----
        Dumps the file named on the AUX2 FILEAUX2 command according the format
        specified on the FORM command.
        """
        command = f"DUMP,{nstrt},{nstop}"
        return self.run(command, **kwargs)

    def fileaux2(self, fname="", ident="", **kwargs):
        """Specifies the binary file to be dumped.

        APDL Command: FILEAUX2

        Parameters
        ----------
        fname
            File name and directory path (248 characters maximum,
            including the characters needed for the directory path).
            An unspecified directory path defaults to the working
            directory; in this case, you can use all 248 characters
            for the file name.

        ident
            ANSYS filename identifier.  See the Basic Analysis Guide
            for file descriptions and identifiers.  If not an ANSYS
            identifier, Ident will be used as the filename extension.

        Notes
        -----
        Specifies the binary file to be dumped with the DUMP command.
        """
        command = f"FILEAUX2,{fname},{ident}"
        return self.run(command, **kwargs)

    def form(self, lab="", **kwargs):
        """Specifies the format of the file dump.

        APDL Command: FORM

        Parameters
        ----------
        lab
            Format:

            RECO - Basic record description only (minimum output) (default).

            TEN - Same as RECO plus the first ten words of each record.

            LONG - Same as RECO plus all words of each record.

        Notes
        -----
        Specifies the format of the file dump (from the DUMP command).
        """
        command = f"FORM,{lab}"
        return self.run(command, **kwargs)

    def ptr(self, loc="", base="", **kwargs):
        """Dumps the record of a binary file.

        APDL Command: PTR

        Parameters
        ----------
        loc, base
            Dump the file record starting at pointer LOC. BASE is the base
            pointer, and would be used if LOC is a relative pointer.

        Notes
        -----
        Dumps the record of the file named on the AUX2 FILEAUX2 command
        according the format specified on the FORM command.
        """
        command = f"PTR,{loc},{base}"
        return self.run(command, **kwargs)
