class LoadStepOperations:
    def lsclear(self, lab="", **kwargs):
        """Clears loads and load step options from the database.

        APDL Command: LSCLEAR

        Parameters
        ----------
        lab
            Label identifying the data to be cleared:

            SOLID - Delete only solid model loads.

            FE - Delete only finite element loads.

            INER - Delete only inertia loads (ACEL, etc.).

            LFACT - Initialize only load factors (on DCUM, FCUM, SFCUM, etc.).

            LSOPT - Initialize only load step options.

            ALL - Delete all loads and initialize all load step options and load factors.

        Notes
        -----
        Loads are deleted, and load step options are initialized to their
        default values.

        This command is also valid in PREP7.
        """
        command = f"LSCLEAR,{lab}"
        return self.run(command, **kwargs)

    def lsdele(self, lsmin="", lsmax="", lsinc="", **kwargs):
        """Deletes load step files.

        APDL Command: LSDELE

        Parameters
        ----------
        lsmin, lsmax, lsinc
            Range of load step files to be deleted, from LSMIN to LSMAX in
            steps of LSINC.  LSMAX defaults to LSMIN, and LSINC defaults to 1.
            If LSMIN = ALL, all load step files are deleted (and LSMAX and
            LSINC are ignored).  The load step files are assumed to be named
            Jobname.Sn, where n is a number assigned by the LSWRITE command (01
            --09,10,11, etc.).  On systems with a 3-character limit on the
            extension, the "S" is dropped for numbers > 99.

        Notes
        -----
        Deletes load step files in the current directory (written by the
        LSWRITE command).

        This command is also valid in PREP7.
        """
        command = f"LSDELE,{lsmin},{lsmax},{lsinc}"
        return self.run(command, **kwargs)

    def lsread(self, lsnum="", **kwargs):
        """Reads load and load step option data into the database.

        APDL Command: LSREAD

        Parameters
        ----------
        lsnum
            Identification number of the load step file to be read.  Defaults
            to 1 + highest number read in the current session.  Issue
            LSREAD,STAT to list the current value of LSNUM.  Issue LSREAD,INIT
            to reset LSNUM to 1.  The load step files are assumed to be named
            Jobname.Sn, where n is a number assigned by the LSWRITE command (01
            --09,10,11, etc.).  On systems with a 3-character limit on the
            extension, the "S" is dropped for LSNUM > 99.

        Notes
        -----
        Reads load and load step option data from the load step file into the
        database.  LSREAD will not clear the database of all current loads.
        However, if a load is respecified with LSREAD, then it will overwrite
        the existing load. See the LSWRITE command to write load step files,
        and the LSDELE command to delete load step files.  LSREAD removes any
        existing SFGRAD specification.

        This command is also valid in PREP7.
        """
        command = f"LSREAD,{lsnum}"
        return self.run(command, **kwargs)

    def lssolve(self, lsmin="", lsmax="", lsinc="", **kwargs):
        """Reads and solves multiple load steps.

        APDL Command: LSSOLVE

        Parameters
        ----------
        lsmin, lsmax, lsinc
            Range of load step files to be read and solved, from
            ``lsmin`` to ``lsmax`` in steps of ``lsinc``.  ``lsmax``
            defaults to ``lsmin``, and ``lsinc`` defaults to 1. If
            ``lsmin`` is blank, a brief command description is
            displayed.  The load step files are assumed to be named
            Jobname.Sn, where n is a number assigned by the
            ``lswrite`` command (01--09, 10, 11, etc.).  On systems
            with a 3-character limit on the extension, the "S" is
            dropped for numbers > 99.

        Notes
        -----
        ``lssolve`` invokes an ANSYS macro to read and solve multiple
        load steps.  The macro loops through a series of load step
        files written by the LSWRITE command.  The macro file called
        by ``lssolve`` is called LSSOLVE.MAC.

        ``lssolve`` cannot be used with the birth-death option.

        ``lssolve`` is not supported for cyclic symmetry analyses.

        ``lssolve`` does not support restarts.

        Examples
        --------
        Write the load and load step option data to a file and solve
        it.  In this case, write the second load step.

        >>> mapdl.lswrite(2)
        >>> mapdl.lssolve(1, 2)

        """
        with self.non_interactive:
            self.run(f"LSSOLVE,{lsmin},{lsmax},{lsinc}", **kwargs)
        return self.last_response

    def lswrite(self, lsnum="", **kwargs):
        """Writes load and load step option data to a file.

        APDL Command: LSWRITE

        Parameters
        ----------
        lsnum
            Number to be assigned to the load step file name for identification
            purposes.  Defaults to 1 + highest LSNUM used in the current
            session.  Issue LSWRITE,STAT to list the current value of LSNUM.
            Issue LSWRITE,INIT to reset to 1.  The load step file will be named
            Jobname.Sn, where n is the specified LSNUM value (preceded by "0"
            for values 1-9).  On systems with a 3-character limit on the file
            name extension, the "S" is dropped for LSNUM > 99.

        Notes
        -----
        Writes all load and load step option data for the selected model to a
        load step file for later use.  LSWRITE does not capture changes made to
        real constants (R), material properties (MP), couplings (CP), or
        constraint equations (CE).

        Solid model loads will not be saved if the model is not meshed. Solid
        model loads, if any, are transferred to the finite element model. Issue
        LSCLEAR,FE to delete finite element loads.

        One file is written for each load step. Use the LSREAD command to read
        a single load step file, and the LSDELE command to delete load step
        files.  Use the LSSOLVE command to read and solve the load steps
        sequentially.

        Solution control commands are typically not written to the file unless
        you specifically change a default solution setting.

        LSWRITE does not support the following commands: DJ, FJ, GSBDATA,
        GSGDATA, ESTIF, EKILL, EALIVE, MPCHG, and OUTRES. These commands will
        not be written to the load step file.

        LSWRITE cannot be used with the birth-death option.

        This command is also valid in PREP7.
        """
        command = f"LSWRITE,{lsnum}"
        return self.run(command, **kwargs)
