"""These SESSION commands control the overall characteristics of the
session, including the jobname, Graphical User Interface behavior, and
file switching.
"""
from ansys.mapdl.core.errors import MapdlRuntimeError


class RunControls:
    def config(self, lab="", value="", **kwargs):
        """Assigns values to ANSYS configuration parameters.

        APDL Command: /CONFIG

        Parameters
        ----------
        lab
            Configuration parameter to be changed:

            NORSTGM - Option to write or not write geometry data to
                      the results file. VALUE is either 0 (write
                      geometry data) or 1 (do not write geometry
                      data). Useful when complex analyses will create
                      abnormally large files. Default is 0.

            NBUF - VALUE is the number of buffers (1 to 32) per file
                   in the solver.  Defaults to 4.

            LOCFL - File open and close actions.  For VALUE use: 0 for
                    global (default); 1 for local.  Applicable to
                    File.EROT, File.ESAV, and File.EMAT.  Typically
                    used for large problems where locally closed files
                    may be deleted earlier in the run with the /FDELE
                    command.

            SZBIO - VALUE is the record size (1024 to 4194304) of
                    binary files (in integer words).  Defaults to
                    16384 (system dependent).

            ORDER - Automatic reordering scheme.  For VALUE use: 0 for
                    WSORT,ALL; 1 for WAVES; 2 for both WSORT,ALL and
                    WAVES (default).

            FSPLIT - Defines split points for binary files.  VALUE is
                     the file split point in megawords and defaults to
                     the maximum file size for the system.

            MXND - Maximum number of nodes. If not specified, defaults
                   to 100 at first encounter.  Dynamically expanded by
                   doubling, even at first encounter, when maximum is
                   exceeded.

            MXEL - Maximum number of elements.  Default and expansion as for MXND.

            MXKP - Maximum number of keypoints.  Default and expansion as for MXND.

            MXLS - Maximum number of lines.  Default and expansion as for MXND.

            MXAR - Maximum number of areas.  Default and expansion as for MXND.

            MXVL - Maximum number of volumes.  Default and expansion as for MXND.

            MXRL - Maximum number of sets of real constants (element
                   attributes).  Default and expansion as for MXND.

            MXCP - Maximum number of sets of coupled degrees of
                   freedom.  Default and expansion as for MXND.

            MXCE - Maximum number of constraint equations.  Default
            and expansion as for MXND.

            NOELDB - Option to write or not write results into the
                     database after a solution.  When VALUE = 0
                     (default), write results into the database.  When
                     VALUE = 1, do not write results into the
                     database.

            DYNA_DBL - Option to invoke the double precision version
                       of the explicit dynamics solver LS-DYNA. When
                       VALUE = 0 (default), the single precision
                       version is used. When VALUE = 1, the double
                       precision version is used.

            STAT - Displays current values set by the /CONFIG command.

        value
            Value (an integer number) assigned to the configuration parameter.

        Notes
        -----
        All configuration parameters have initial defaults, which in most cases
        do not need to be changed.  Where a specially configured version of the
        ANSYS program is desired, the parameters may be changed with this
        command.  Issue /CONFIG,STAT to display current values.  Changes must
        be defined before the parameter is required.  These changes (and
        others) may also be incorporated into the config162.ans file which is
        read upon execution of the program (see The Configuration File in the
        Basic Analysis Guide).  If the same configuration parameter appears in
        both the  configuration file and this command, this command overrides.

        Distributed ANSYS uses the default FSPLIT value, and forces NOELDB = 1
        and NORSTGM = 0 for all results files. The FSPLIT, NOELDB, and NORSTGM
        options cannot be changed when using Distributed ANSYS.

        The /CONFIG command is not valid for the ANSYS Multiphysics 1, 2, or 3
        products.

        The ANSYS Multi-field solver (MFS and MFX) does not support
        /CONFIG,NOELDB,1. The ANSYS Multi-field solver needs the updated ANSYS
        database.
        """
        command = "/CONFIG,%s,%s" % (str(lab), str(value))
        return self.run(command, **kwargs)

    def cwd(self, dirpath="", **kwargs):
        """Changes the current working directory.

        ``dirpath`` must not contain any singular quotations/apostrophes.
        These are not supported in APDL.

        APDL Command: /CWD

        Parameters
        ----------
        dirpath
            The full path name of the new working directory.

        Notes
        -----
        After issuing the /CWD command, all new files opened with no default
        directory specified (via the FILE, /COPY, or RESUME commands, for
        example) default to the new ``dirpath`` directory.

        Examples
        --------
        Change MAPDL's working directory to ``"C:/temp"``.  This
        assumes that MAPDL running on Windows.

        >>> mapdl.cwd("C:/temp")

        MAPDL on Linux example:

        >>> mapdl.cwd("/tmp/")

        """
        dirpath = str(dirpath)
        if not (dirpath.startswith("'") and dirpath.endswith("'")) and "'" in dirpath:
            raise MapdlRuntimeError(
                'The CWD command does not accept paths that contain singular quotes "'
            )
        return self.run(f"/CWD,'{dirpath}'", **kwargs)

    def filname(self, fname="", key="", **kwargs):
        """Changes the Jobname for the analysis.

        APDL Command: /FILNAME

        Parameters
        ----------
        fname
            Name (32 characters maximum) to be used as the Jobname.  Defaults
            to the initial Jobname as specified on the ANSYS execution command,
            or to file if none specified.

        key
            Specify whether to use the existing log, error, lock, page, and
            output files (.LOG, .ERR, .LOCK, .PAGE and .OUT) or start new
            files.

            0, OFF - Continue using current log, error, lock, page, and output files.

            1, ON - Start new log, error, lock, page, and output files
                    (old log and error files are closed and saved, but
                    old lock, page, and output files are
                    deleted). Existing log and error files are
                    appended.

        Notes
        -----
        All subsequently created files will be named with this Jobname if Key =
        0.  Use Key = 1 to start new log, error, lock, page, and output files.
        The previous Jobname is typically defined on the ANSYS program
        execution line (see the Operations Guide).  This command is useful when
        different groups of files created throughout the run are to have
        different names.  For example, the command may be used before each
        substructure pass to avoid overwriting files or having to rename each
        file individually.

        This command is valid only at the Begin level.
        """
        command = "/FILNAME,%s,%s" % (str(fname), str(key))
        return self.run(command, **kwargs)

    def input(self, fname="", ext="", dir="", line="", log="", **kwargs):
        """Switches the input file for the commands that follow.

        APDL Command: /INPUT

        Parameters
        ----------
        fname
            File name and directory path (248 characters maximum,
            including the characters needed for the directory path).  An
            unspecified directory path defaults to the working directory;
            in this case, you can use all 248 characters for the file
            name.

        ext
            Filename extension (eight-character maximum).

        dir
            Directory path (64 characters maximum). Defaults to current
            directory.

        line
            A value indicating either a line number in the file or a user-
            defined label in the file from which to begin reading the
            input file.

            (blank), 0, or 1 - Begins reading from the top of the file (default).

            LINE_NUMBER - Begins reading from the specified line number in the file.

            :label - Begins reading from the first line beginning with the
                     matching user-defined label :label (beginning with a
                     colon (:), 8 characters maximum).

        log
            Indicates whether secondary input from this command should be
            recorded in the command log (File.LOG) and the database log:

            0 - Record only the /INPUT command on the log (default).

            1 - Record commands in the specified secondary file as they are executed.

        Notes
        -----
        Switches the input file for the next commands.  Commands are read
        from this file until an end-of-file or another file switching
        directive is read.  An end-of-file occurs after the last record of
        the file or when a /EOF command is read.  An automatic switch back
        one level (to the previous file) occurs when an end-of-file is
        encountered.  Twenty levels of nested file switching are allowed.
        Note that files including ``*DO``, ``*USE``, ``*ULIB``, and the "Unknown
        Command" Macro have less nesting available because each of these
        operations also uses a level of file switching.  For an
        interactive run, a /INPUT,TERM switches to the terminal for the
        next input.  A /EOF read from the terminal then switches back to
        the previous file.  A /INPUT (with a blank second field) switches
        back to the primary input file.

        Setting LOG = 1 on /INPUT causes all commands read from the
        specified file to be recorded in the command log (File.LOG) and
        the internal database command log [LGWRITE].  This option is
        recommended if the log file will be used later .  The LOG = 1
        option is only valid when the /INPUT occurs in the primary input
        file.  Using LOG = 1 on a nested /INPUT or on a /INPUT within a
        do-loop will have no effect (i.e., commands in the secondary input
        file are not written to the command log).

        The Dir option is optional as the directory path can be included
        directly in Fname.

        Examples
        --------
        Run an input file relative to the location of MAPDL.

        >>> mapdl.input('my_input_file.inp')

        """
        return self.run(f"/INPUT,{fname},{ext},{dir},{line},{log}", **kwargs)

    def keyw(self, keyword="", key="", **kwargs):
        """Sets a keyword used by the GUI for context filtering (GUI).

        APDL Command: KEYW

        Parameters
        ----------
        keyword
            A keyword which, when set to either true or false, changes the
            behavior of the GUI.

        key
            Keyword switch:

            0 - Sets the keyword to "false."

            1 - Sets the keyword to "true."

        Notes
        -----
        Defines a keyword used by the GUI for context filtering.  This is a
        command generated by the GUI and may appear in the log file
        (Jobname.LOG) if the GUI is used.  This command is usually not typed in
        directly in an ANSYS session.

        This command is valid in any processor.
        """
        command = "KEYW,%s,%s" % (str(keyword), str(key))
        return self.run(command, **kwargs)

    def memm(self, lab="", kywrd="", **kwargs):
        """Allows the current session to keep allocated memory.

        APDL Command: MEMM

        Parameters
        ----------
        lab
            When Lab = KEEP, the memory manager's ability to acquire and keep
            memory is controlled by Kywrd

        kywrd
            Turns the memory "keep" mode on or off

            ON - Keep any memory allocated during the analysis.

            OFF - Use memory dynamically and free it up to other users after use (default).

        Notes
        -----
        You can use the MEMM command to ensure that memory intensive operations
        will always have the same memory available when the operations occur
        intermittently. Normally, if a large amount of memory is allocated for
        a specific operation, it will be returned to the system once the
        operation is finished. This option always maintains the highest level
        used during the analysis until the analysis is finished.

        The MEMM command does not affect the value you specify with the -m
        switch. When you allocate memory with the -m switch, that amount will
        always be available. However, if dynamic memory allocation in excess of
        the-m value occurs, you can use the MEMM command to ensure that amount
        is retained until the end of your analysis.
        """
        command = "MEMM,%s,%s" % (str(lab), str(kywrd))
        return self.run(command, **kwargs)

    def nerr(self, nmerr="", nmabt="", abort="", ifkey="", num="", **kwargs):
        """Limits the number of warning and error messages displayed.

        APDL Command: /NERR

        Parameters
        ----------
        nmerr
            Maximum number of warning and error messages displayed per
            command.  Defaults to 5 for interactive runs with the GUI
            turned on, 20 for interactive runs with the GUI turned
            off, 200 for batch runs.  If NMERR is negative, the
            absolute value of NMERR is used as the maximum number of
            warning and error messages written to the error file
            (file.ERR) per command, as well as the maximum number of
            messages displayed per command.

        nmabt
            Maximum number of warning and error messages allowed per
            command before run aborts (must be greater than zero).
            Maximum value is 99,999,999. Defaults to 10,000.

        abort
            Abort level key.  Set to 0 for default abort behavior, -1
            to never abort, and -2 to abort after ``nmabt`` errors.
            Altering the abort level key is not recommended, but can
            be helpful for avoiding an abort within /BATCH mode but
            using ``pyansys`` interactively.

        ifkey
            Specifies whether or not to abort if an error occurs during a
            /INPUT operation:

            0 or OFF - Do not abort. This option is the default.

            1 or ON - Abort.

        num
            The number of invalid command warnings before a stop warning will
            be issued:

            0 - Disables the stop warning/error function.

            n - An integer value representing the number of warnings that will be encountered
                before prompting the user to stop (default = 5). The first
                error encountered will ALWAYS result in a prompt.

        Notes
        -----
        Limits the number of warning and error messages displayed for any one
        command in an interactive run.

        Warning and error messages continue to be written to Jobname.ERR
        regardless of these limits (unless NMERR is negative).

        Issue this command with NUM = n to specify the number of "invalid
        command" warnings to be encountered before the user is prompted to
        stop. You can then continue or abort the run. If you choose to abort
        the run, the log file can be saved so that any of the processing up to
        that point can be appended to an input that rectifies the condition. A
        batch run always aborts on the first error.  Issue /NERR,STAT to list
        current settings.

        Issue /NERR,DEFA to reset values to initial defaults.

        An IFKEY value of 1 or ON causes the ANSYS program to abort immediately
        upon encountering an error during a file /INPUT operation. However, use
        of this option may cause the following conditions to occur:

        The /INPUT command may abort if issued for a log file (jobname.log).

        Some macros may abort.

        A CAD connection may fail after reading only a small portion of a CAD
        model.

        The command is valid in any processor.
        """
        command = "/NERR,%s,%s,%s,%s,%s" % (
            str(nmerr),
            str(nmabt),
            str(abort),
            str(ifkey),
            str(num),
        )
        return self.run(command, **kwargs)

    def pause(self, **kwargs):
        """Temporarily releases the current product license.

        APDL Command: PAUSE

        Notes
        -----
        The PAUSE command temporarily releases (or pauses) the current product
        license so that another application can use it.

        This application consumes a license as soon as you launch it, and
        retains that license until it is finished. If you launch the product
        interactively, the license is retained until you either close the
        application or issue a PAUSE command via the command line.

        No other operation (other than SAVE or /EXIT) is possible in the
        current application while use of the product license is paused.

        When the second application has finished and releases the license,
        issue an UNPAUSE command via the command line to restore use of the
        license to the current application.

        For more information, see the ANSYS, Inc. Licensing Guide.
        """
        command = "PAUSE,"
        return self.run(command, **kwargs)

    def slashstatus(self, lab="", **kwargs):
        """Lists the status of items for the run.

        APDL Command: /STATUS

        Parameters
        ----------
        lab
            Items to list status for:

            ALL - List all below (default).

            TITLE - List only titles, Jobname, and revision number.

            UNITS - List only units.

            MEM - List only memory data statistics.

            DB - List only database statistics

            CONFIG - List only configuration parameters.

            GLOBAL - Provides a global status summary.

            SOLU - Provides a solution status summary.

            PROD - Provides a product summary.

        Notes
        -----
        Displays various items active for the run (such as the ANSYS revision
        number, Jobname, titles, units, configuration parameters, database
        statistics, etc.).

        This command is valid in any processor.
        """
        return self.run(f"/STATUS,{lab}", **kwargs)

    def starstatus(
        self,
        par="",
        imin="",
        imax="",
        jmin="",
        jmax="",
        kmin="",
        kmax="",
        lmin="",
        lmax="",
        mmin="",
        mmax="",
        kpri="",
        **kwargs,
    ):
        """Lists the current parameters and abbreviations.

        APDL Command: ``*STATUS``

        Parameters
        ----------
        par
            Specifies the parameter or sets of parameters listed. For array
            parameters, use IMIN, IMAX, etc. to specify ranges.  Use ``*DIM`` to
            define array parameters. Use ``*VEDIT`` to review array parameters
            interactively. Use ``*VWRITE`` to print array values in a formatted
            output. If Par is blank, list all scalar parameter values, array
            parameter dimensions, and abbreviations.  If ARGX, list the active
            set of local macro parameters (ARG1 to ARG9 and AR10 to AR99)
            [``*USE``].

            Lists all parameters (except local macro parameters and those with names beginning or ending with an underbar) and toolbar abbreviations. - Lists only parameters with names beginning with an underbar (_). These are
                              ANSYS internal parameters.

            Lists only parameters with names ending with an underbar (_). A good APDL programming convention is to ensure that all parameters created by your system programmer are named with a trailing underbar. - Lists all toolbar abbreviations.

            Lists all parameters (except local macro parameters and those with names beginning or ending with an underbar). - Lists all APDL Math parameters, including vectors, matrices, and linear
                              solvers.

            Lists only the parameter specified. PARNAME cannot be a local macro parameter name. - Lists all local macro parameter values (ARG1- AR99) that are non-zero or non-
                              blank.

        imin, imax, jmin, jmax, kmin, kmax, lmin, lmax, mmin, mmax
            Range of array elements to display (in terms of the dimensions
            (row, column, plane, book, and shelf).   Minimum values default to
            1.  Maximum values default to the maximum dimension values.  Zero
            may be input for IMIN, JMIN, and KMIN to display the index numbers.
            See ``*TAXIS``  command to list index numbers of 4- and 5-D tables.

        kpri
            Use this field to list your primary variable labels (X, Y, Z, TIME,
            etc.).

            List the labels (default). YES, Y, or ON are also valid entries.  - Do not list the labels. NO, N, or OFF are also valid entries.

        Notes
        -----
        You cannot obtain the value for a single local parameter (e.g.,
        ``*STATUS,ARG2``). You can only request all local parameters simultaneously
        using ``*STATUS,ARGX``.

        This command is valid in any processor.
        """
        command = "*STATUS,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (
            str(par),
            str(imin),
            str(imax),
            str(jmin),
            str(jmax),
            str(kmin),
            str(kmax),
            str(lmin),
            str(lmax),
            str(mmin),
            str(mmax),
            str(kpri),
        )
        return self.run(command, **kwargs)

    def syp(
        self,
        string="",
        arg1="",
        arg2="",
        arg3="",
        arg4="",
        arg5="",
        arg6="",
        arg7="",
        arg8="",
        **kwargs,
    ):
        """Passes a command string and arguments to the operating system.

        APDL Command: /SYP

        Parameters
        ----------
        string
            Command string (cannot include commas).  See also the /SYS command.

        arg1, arg2, arg3, . . . , arg8
            Arguments to be appended to the command string, separated by
            blanks, commas, or other delimiter characters (see the Operations
            Guide).  The arguments may be numbers, parameters, or parametric
            expressions.

        Notes
        -----
        Passes a command string to the operating system for execution, along
        with arguments to be appended to the command string.  See the
        Operations Guide for details.  ANSYS may not be aware of your specific
        user environment. For example, on Linux this command may not recognize
        aliases, depending on the hardware platform and user environment.

        This command is valid in any processor.
        """
        command = "/SYP,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (
            str(string),
            str(arg1),
            str(arg2),
            str(arg3),
            str(arg4),
            str(arg5),
            str(arg6),
            str(arg7),
            str(arg8),
        )
        return self.run(command, **kwargs)

    def sys(self, string="", **kwargs):
        """Passes a command string to the operating system.

        APDL Command: /SYS

        Parameters
        ----------
        string
            Command string, up to 639 characters (including blanks, commas,
            etc.). The specified string is passed verbatim to the operating
            system, i.e., no parameter substitution is performed.

        Notes
        -----
        Passes a command string to the operating system for execution (see the
        Operations Guide).  Typical strings are system commands such as list,
        copy, rename, etc.  Control returns to the ANSYS program after the
        system procedure is completed.   ANSYS may not be aware of your
        specific user environment. For example, on Linux this command may not
        recognize aliases, depending on the hardware platform and user
        environment.

        This command is valid in any processor.
        """
        command = "/SYS,%s" % (str(string))
        return self.run(command, **kwargs)

    def unpause(self, **kwargs):
        """Restores use of a temporarily released product license.

        APDL Command: UNPAUSE

        Notes
        -----
        The UNPAUSE command restores use of a temporarily released (paused)
        product license. The command is valid only after a previously issued
        PAUSE command.

        When use of the product license is paused via the PAUSE command, no
        other operation (other than SAVE or /EXIT) is possible until you issue
        the UNPAUSE command.

        For more information, see the documentation for the PAUSE command and
        the ANSYS, Inc. Licensing Guide.
        """
        command = "UNPAUSE,"
        return self.run(command, **kwargs)
