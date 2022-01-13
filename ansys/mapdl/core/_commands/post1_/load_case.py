class LoadCase:
    def lcabs(self, lcno="", kabs="", **kwargs):
        """Specifies absolute values for load case operations.

        APDL Command: LCABS

        Parameters
        ----------
        lcno
            Load case pointer number.  If ALL, apply to all selected load cases
            [LCSEL].

        kabs
            Absolute value key:

            0 - Use algebraic values of load case LCNO in operations.

            1 - Use absolute values of load case LCNO in operations.

        Notes
        -----
        Causes absolute values to be used in the load case operations [LCASE or
        LCOPER].  Absolute values are taken prior to assigning a load case
        factor [LCFACT] and are applied only to defined load cases [LCDEF].
        """
        command = f"LCABS,{lcno},{kabs}"
        return self.run(command, **kwargs)

    def lcase(self, lcno="", **kwargs):
        """Reads a load case into the database.

        APDL Command: LCASE

        Parameters
        ----------
        lcno
            Load case pointer number [LCDEF,STAT].  Defaults to 1.

        Notes
        -----
        Reads a load case into the database.  Load cases are created as
        described on the LCDEF or LCWRITE commands.  The results portion of the
        database and the applied forces and displacements are cleared before
        reading the data in.  Absolute values [LCABS] and scale factors
        [LCFACT] can be applied during the read operation.
        """
        command = f"LCASE,{lcno}"
        return self.run(command, **kwargs)

    def lcdef(self, lcno="", lstep="", sbstep="", kimg="", **kwargs):
        """Creates a load case from a set of results on a results file.

        APDL Command: LCDEF

        Parameters
        ----------
        lcno
            Arbitrary pointer number (1-99) to be assigned to the load case
            specified by LSTEP, SBSTEP and by the FILE command.  Defaults to 1
            + previous value.

        lstep
            Load step number to be defined as the load case.  Defaults to one.

        sbstep
            Substep number.  Defaults to the last substep of the load step.

        kimg
            Used only with results from complex analyses:

            0 - Use real part of complex solution

            1 - Use imaginary part.

        Notes
        -----
        Creates a load case by establishing a pointer to a set of results on a
        results file (written during the ANSYS solution phase).  This pointer
        (LCNO) can then be used on the LCASE or LCOPER commands to read the
        load case data into the database.

        Issue LCDEF,ERASE to delete all load case pointers (and all load case
        files, if any).  Issue LCDEF,LCNO,ERASE to delete only the specific
        load case pointer LCNO (and its file, if any).  With the ERASE options,
        all pointers are deleted; however only files with the default extension
        [LCWRITE] are deleted.  Issue LCDEF,STAT for status of all selected
        load cases [LCSEL], or LCDEF,STAT,ALL for status of all load cases.
        The STAT command may be used to list all load cases.  See also LCFILE
        to establish a pointer to a set of results on a load case file (written
        by LCWRITE). Harmonic element data read from a result file load case is
        stored at the zero-degree position.
        """
        command = f"LCDEF,{lcno},{lstep},{sbstep},{kimg}"
        return self.run(command, **kwargs)

    def lcfact(self, lcno="", fact="", **kwargs):
        """Defines scale factors for load case operations.

        APDL Command: LCFACT

        Parameters
        ----------
        lcno
            Load case pointer number.  If ALL, apply to all selected load cases
            [LCSEL].

        fact
            Scale factor applied to load case LCNO.  Blank defaults to 1.0.

        Notes
        -----
        Defines scale factors to be used in the load case operations [LCASE or
        LCOPER].  Scale factors are applied after an absolute value operation
        [LCABS] and are applied only to defined load cases [LCDEF].
        """
        command = f"LCFACT,{lcno},{fact}"
        return self.run(command, **kwargs)

    def lcfile(self, lcno="", fname="", ext="", **kwargs):
        """Creates a load case from an existing load case file.

        APDL Command: LCFILE

        Parameters
        ----------
        lcno
            Arbitrary (1-99) pointer number assigned to this load case.

        fname
            File name and directory path (248 characters maximum, including the
            characters needed for the directory path).  An unspecified
            directory path defaults to the working directory; in this case, you
            can use all 248 characters for the file name.

        ext
            Filename extension (eight-character maximum).

        Notes
        -----
        Creates a load case by establishing a pointer to an existing load case
        file [LCWRITE].  This pointer (LCNO) can then be used on the LCASE or
        LCOPER commands to read the load case data into the database.  This
        command is typically used to reestablish load case pointers in a new
        ANSYS session (pointers are not saved on the database file), or when
        more than one pointer to a single load case is desired.  See the LCDEF
        command for status and erase operations.  See also LCDEF to establish a
        pointer to a set of results on a results file (written during the ANSYS
        solution phase).
        """
        command = f"LCFILE,{lcno},{fname},{ext}"
        return self.run(command, **kwargs)

    def lcoper(self, oper="", lcase1="", oper2="", lcase2="", **kwargs):
        """Performs load case operations.

        APDL Command: LCOPER

        Parameters
        ----------
        oper
            Valid operations are:

            ZERO - Zero results portion of database (LCASE1 ignored).

            SQUA - Square database values (LCASE1 ignored).

            SQRT - Square root of database (absolute) values (LCASE1 ignored).

            LPRIN - Recalculate line element principal stresses (LCASE1 ignored).  Stresses are as
                    shown for the NMISC items of the ETABLE command for the
                    specific line element type.

            ADD - Add LCASE1 to database values.

            SUB - Subtract LCASE1 from database values.

            SRSS - Square root of the sum of the squares of database and LCASE1.

            MIN - Compare and save in database the algebraic minimum of database and LCASE1.

            MAX - Compare and save in database the algebraic maximum of database and LCASE1.

            ABMN - Compare and save in database the absolute minimum of database and LCASE1 (based
                   on magnitudes, then apply the corresponding sign).

            ABMX - Compare and save in database the absolute maximum of database and LCASE1 (based
                   on magnitudes, then apply the corresponding sign).

        lcase1
            First load case in the operation (if any).  See LCNO of the LCDEF
            command. If ALL, repeat operations using all selected load cases
            [LCSEL].

        oper2
            Valid operations are:

            MULT - Multiplication: ``LCASE1*LCASE2``

            CPXMAX - This option does a phase angle sweep to calculate the maximum of derived
                     stresses and equivalent strain for a complex solution
                     where LCASE1 is the real part and LCASE2 is the imaginary
                     part. The Oper field is not applicable with  this option.
                     Also, the LCABS and SUMTYPE commands have no effect on
                     this option. The value of S3 will be a minimum.   This
                     option does not apply to derived displacement amplitude
                     (USUM). Load case writing (LCWRITE) is not supported. See
                     POST1 and POST26 – Complex Results Postprocessing in the
                     Mechanical APDL Theory Reference for more information.

        lcase2
            Second load case.  Used only with Oper2 operations.

        Notes
        -----
        LCOPER operates on the database and one or two load cases according to:

        Database = Database Oper (LCASE1 Oper2 LCASE2)

        where operations Oper and Oper2 are as described above.  Absolute
        values and scale factors may be applied to the load cases before the
        operations [LCABS, LCFACT].  If LCASE1 is not specified, only operation
        Oper is performed on the current database.  If LCASE2 is specified,
        operation Oper2 will be performed before operation Oper.  If LCASE2 is
        not specified, operation Oper2 is ignored.  Solution items not
        contained [OUTRES] in either the database or the applicable load cases
        will result in a null item during a load case operation.  Harmonic
        element data read from a result file load case are processed at zero
        degrees.  All load case combinations are performed in the solution
        coordinate system, and the data resulting from load case combinations
        are stored in the solution coordinate system.  The resultant data are
        then transformed to the active results coordinate system [RSYS] when
        listed or displayed. Except in the cases of Oper = LPRIN, ADD, or SUB,
        you must use RSYS,SOLU to list or display, and in the case of layered
        elements, the layer (LAYER) must also be specified.

        Use the FORCE command prior to any combination operation to correctly
        combine the requested force type.

        If Oper2=CPXMAX, the derived stresses and strain calculation do not
        apply to line elements.
        """
        command = f"LCOPER,{oper},{lcase1},{oper2},{lcase2}"
        return self.run(command, **kwargs)

    def lcsel(self, type_="", lcmin="", lcmax="", lcinc="", **kwargs):
        """Selects a subset of load cases.

        APDL Command: LCSEL

        Parameters
        ----------
        type\_
            Label identifying the type of select:

            S - Select a new set.

            R - Reselect a set from the current set.

            A - Additionally select a set and extend the current set.

            U - Unselect a set from the current set.

            ALL - Restore the full set.

            NONE - Unselect the full set.

            INVE - Invert the current set (selected becomes unselected and vice versa).

            STAT - Display the current select status.

        lcmin
            Minimum value of load case pointer range.

        lcmax
            Maximum value of load case pointer range.  LCMAX defaults to LCMIN.

        lcinc
            Value increment within range.  Defaults to 1.  LCINC cannot be
            negative.

        Notes
        -----
        Selects a subset of load cases for other operations.  For example, to
        select a new set of load cases based on load cases 1 through 7, use
        LCSEL,S,1,7.  The subset is used when the ALL label is entered (or
        implied) on other commands, such as LCFACT, LCABS, LCOPER, etc.  Load
        cases are flagged as selected and unselected; no load case pointers
        [LCDEF, LCWRITE, LCFILE] are actually deleted from the database.
        """
        command = f"LCSEL,{type_},{lcmin},{lcmax},{lcinc}"
        return self.run(command, **kwargs)

    def lcsum(self, lab="", **kwargs):
        """Specifies whether to process non-summable items in load case

        APDL Command: LCSUM
        operations.

        Parameters
        ----------
        lab
            Combination option

            (blank) - Only combine summable items [default].

            ALL - Combine all items including non summable items.

        Notes
        -----
        Allows non-summable items (e.g. plastic strains) to be included in load
        combinations.  Issue LCSUM,ALL before the first load case operation
        (LCXX command).  May also be used to include nonsummable items in the
        appending of a results file (RAPPND command).
        """
        command = f"LCSUM,{lab}"
        return self.run(command, **kwargs)

    def lcwrite(self, lcno="", fname="", ext="", **kwargs):
        """Creates a load case by writing results to a load case file.

        APDL Command: LCWRITE

        Parameters
        ----------
        lcno
            Arbitrary pointer number (1-99) to be assigned to this load case.

        fname
            File name and directory path (248 characters maximum, including the
            characters needed for the directory path).  An unspecified
            directory path defaults to the working directory; in this case, you
            can use all 248 characters for the file name.

        ext
            Filename extension (eight-character maximum).

        Notes
        -----
        Creates a load case by writing the results data in the database to a
        load case file.  The database remains unchanged by this operation.  A
        pointer is also established to the written set of results on the load
        case file.  This pointer (LCNO) can then be used on the LCASE or LCOPER
        commands to read the load case data into the database.  By default,
        only summable results data (such as displacements, stresses, elastic
        strains) and constant results data (such as volume) are written to the
        load case file unless requested (LCSUM command).  Non-summable results
        data (such as plastic strains, strain energy), boundary conditions, and
        nodal loads are not written to the load case file.  The load case file
        may be named by default or by a user name.  Rewriting to the same file
        overwrites the previous data.  See the LCDEF command for status and
        erase operations.
        """
        command = f"LCWRITE,{lcno},{fname},{ext}"
        return self.run(command, **kwargs)

    def lczero(self, **kwargs):
        """Zeroes the results portion of the database.

        APDL Command: LCZERO

        Notes
        -----
        Often used before the LCOPER command.  Same as LCOPER,ZERO.
        """
        command = f"LCZERO,"
        return self.run(command, **kwargs)

    def rappnd(self, lstep="", time="", **kwargs):
        """Appends results data from the database to the results file.

        APDL Command: RAPPND

        Parameters
        ----------
        lstep
            Load step number to be assigned to the results data set.  If it is
            the same as an existing load step number on the results file, the
            appended load step will be inaccessible.  Defaults to 1.

        time
            Time value to be assigned to the results data set.  Defaults to
            0.0.  A time value greater than the last load step should be used.

        Notes
        -----
        This command is typically used to append the results from a load case
        combination to the results file.  See the LCWRITE command to create a
        separate load case file.  Only summable and constant data are written
        to the results file by default; non-summable data are not written
        unless requested (LCSUM command). RAPPND should not be used to append
        results from a harmonic analysis.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"RAPPND,{lstep},{time}"
        return self.run(command, **kwargs)
