class Aux15:
    def igesin(self, fname="", ext="", **kwargs):
        """Transfers IGES data from a file into MAPDL.

        APDL Command: IGESIN

        Parameters
        ----------
        fname : str
            File name and directory path (248 characters maximum,
            including the characters needed for the directory path).  An
            unspecified directory path defaults to the working directory;
            in this case, you can use all 248 characters for the file
            name.  The file name defaults to JOBNAME

        ext : str
            Filename extension (eight-character maximum).  This is
            optional and the extension can be included in the ``fname``
            parameter.  The extension defaults to CAD if ``fname`` is
            blank.

        Notes
        -----
        Reads a file containing IGES data and transfers it into the ANSYS
        database.  The file transferred is the IGES Version 5.1, ASCII
        format file.  IGES (Initial Graphics Exchange Specification) is a
        neutral format developed by the U.S. Dept. of Commerce, National
        Institute of Standards and Technology.  There is no output
        transfer file written since the transferred data is read directly
        into the MAPDL database.

        You can import multiple files into a single database, but you must
        use the same import option (set with the IOPTN command) for each
        file.

        The IOPTN command sets the parameters for reading the file.  Files
        read via the SMOOTH method (the only available method) use the
        standard database.

        Examples
        --------
        Read in an IGES file in the current MAPDL directory.

        >>> mapdl.igesin('bracket.iges')

        Read in an example IGES file

        >>> from ansys.mapdl.core import examples
        >>> bracket_file = examples.download_bracket()
        >>> mapdl.igesin(bracket_file)

        Read in a igesfile from a full path

        >>> mapdl.igesin('C:\\Users\\user\\bracket.iges)

        """
        return self.run(f"IGESIN,{fname},{ext}", **kwargs)

    def ioptn(self, lab="", val1="", **kwargs):
        """Controls options relating to importing a model.

        APDL Command: IOPTN

        Parameters
        ----------
        lab
            Label identifying the import option.  The meaning of VAL1 varies
            depending on Lab.

            STAT - List overall status of import facilities, including current option values.
                   VAL1 is ignored.

            DEFA - Set default values for all import options.  VAL1is ignored.

            MERG - Entity merge option.  VAL1 can be:

            YES - Automatic merging is performed (default).

            NO - No merging of entities.

            SOLID - Solid option.  VAL1 can be:

            YES - Solid is created automatically (default).

            NO - No solid created.

            GTOLER - Entity merging tolerance. If IGES = SMOOTH, the GTOLER,VAL1 can be:

            DEFA - Use system defaults (default).

            FILE - Use tolerance from the imported file.

            n - A user-specified tolerance value.

            IGES - IGES import option.  VAL1 can be:

            STAT - List status of IGES related options in the output window.

            SMOOTH (or RV52) - Use more robust IGES revision 5.2 import function (default).

            SMALL - Small areas option.   VAL1 can be:

            YES - Small areas are deleted (default).

            NO - Small areas are retained.

        val1
            Additional input value as described under each Lab option.

        Notes
        -----
        Controls various options during a model file transfer.  A global solid
        model tolerance (GTOLER) can be specified.

        The SMALL,YES option (default) delete small areas  and can cause
        geometrical inconsistencies that could cause the import process to
        abort.  Retaining the small areas increases processor time and memory
        usage.

        The data is stored in the standard ANSYS graphics database.

        The IGES,SMOOTH (default) option is capable of reading in any rational
        B-spline curve entity (type 126), or rational B-spline surface entity
        (type 128) with a degree less than or equal to 20.  Attempts to read in
        B-spline curve or surface entities of degree higher than 20 may result
        in error messages.

        If you issue the /CLEAR command, the IOPTN settings return to their
        defaults.

        For MERG,YES, merging of coincident geometry items is performed
        automatically when the IGESIN command is issued (that is, an internal
        NUMMRG,KP command is issued).  The model is merged with the
        consideration tolerance (TOLER on NUMMRG) set equal to 0.75 * the
        shortest distance between the endpoints of any active line. See the
        NUMMRG command for more information about the tolerances. In most
        cases, the default merging is appropriate.  Use the IOPTN command when
        you want to:

        Disable merging operations.

        Override the default merging and specify a global solid model tolerance
        value (GTOLER).

        Disable the automatic creation of solids (SOLID).

        The IOPTN command should be issued before the IGESIN command. You
        cannot change these options after your model has been imported or
        created. If you must change the options:

        Clear the database (/CLEAR) or exit and restart the program.

        Set the correct options.

        Reimport or recreate the model.

        This command is valid in any processor.
        """
        command = f"IOPTN,{lab},{val1}"
        return self.run(command, **kwargs)
