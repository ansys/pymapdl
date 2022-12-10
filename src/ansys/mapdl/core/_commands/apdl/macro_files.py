class MacroFiles:
    def cfclos(self, **kwargs):
        """Closes the "command" file.

        APDL Command: ``*CFCLOS``

        Notes
        -----
        This command is valid in any processor.
        """
        command = f"*CFCLOS,"
        return self.run(command, **kwargs)

    def cfopen(self, fname="", ext="", loc="", **kwargs):
        """Opens a "command" file.

        APDL Command: ``*CFOPEN``

        .. warning::
           This command must be run using :func:`non_interactive
           <ansys.mapdl.core.Mapdl.non_interactive>`

        Parameters
        ----------
        fname
            File name and directory path (248 characters maximum,
            including the characters needed for the directory path).
            An unspecified directory path defaults to the working
            directory; in this case, you can use all 248 characters
            for the file name.

        ext
            Filename extension (eight-character maximum).

        loc
            Determines whether existing file will be overwritten or appended:

            (blank) : The existing file will be overwritten.
            APPEND :  The file will be appended to the existing file.

        Notes
        -----
        Data processed with the ``*VWRITE`` command will also be written to this
        file if the file is open when the ``*VWRITE`` command is issued.

        This command is valid in any processor.
        """
        return self.run(f"*CFOPEN,{fname},{ext},,{loc}", **kwargs)

    def cfwrite(self, command="", **kwargs):
        """Writes an ANSYS command (or similar string) to a "command" file.

        APDL Command: ``*CFWRITE``

        Parameters
        ----------
        command
            Command or string to be written.  The standard command form of a
            label followed by arguments separated by commas is assumed.
            Command may be a parameter assignment (e.g.,  ``*CFWRITE, A = 5``).

        Notes
        -----
        Writes an ANSYS command (or similar string) to the file opened
        with ``*CFOPEN``.  The Command string is not executed (except
        that numeric and character parameter substitution and
        operations (with embedded ``*``, /, >,$ etc. characters) are
        performed before writing).  When used with ``*GET`` results
        and parameter substitution, an ANSYS command can be created
        from results and then read back into the ANSYS program (or
        used elsewhere).  For example, if the command
        ``*CFWRITE,BF,NNUM,TEMP,TVAL`` is used in a do-loop, where
        TVAL is a parameter value returned from the ``*GET`` operation
        and NNUM is a specified or returned parameter value, a series
        of BF commands, with numerical values substituted for the two
        parameters, will be written.  To create a file without
        parameter substitution, use ``*CREATE``.

        This command is valid in any processor.
        """
        command = f"*CFWRITE,{command}"
        return self.run(command, **kwargs)

    def create(self, fname="", ext="", **kwargs):
        """Opens (creates) a macro file.

        APDL Command: ``*CREATE``

        .. warning::
           This command must be run using :func:`non_interactive
           <ansys.mapdl.core.Mapdl.non_interactive>`

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
        See the ``*USE`` command for a discussion of macros.  All
        commands following the ``*CREATE`` command, up to the ``*END``
        command, are written to the specified file without being
        executed.  An existing file of the same name, if any, will be
        overwritten.  Parameter values are not substituted for
        parameter names in the commands when the commands are written
        to the file.  Use ``*CFWRITE`` to create a file if this is
        desired.  The resulting macro may be executed with a ``*USE``
        command (which also allows parameters to be passed into the
        macro) or a /INPUT command (which does not allow parameters to
        be passed in).  Several macros may be stacked into a library
        file ``[*ULIB]``. You cannot use ``*CREATE`` within a DO loop.

        This command is valid in any processor.
        """
        return self.run(f"*CREATE,{fname},{ext}", **kwargs)

    def dflab(self, dof="", displab="", forcelab="", **kwargs):
        """Changes degree-of-freedom labels for user custom elements.

        APDL Command: /DFLAB

        Parameters
        ----------
        dof
            Number between 1 and 32 indicating which degree of freedom is to
            have its labels changed. For a list of these quantities, see the
            degree-of-freedom table in the echprm.inc file. The first few
            quantities follow:

        displab
            New label (four-character maximum) for the displacement label. The
            prior label is no longer valid.

        forcelab
            New label (four-character maximum) for the force label for this
            degree of freedom. The prior label is no longer valid.

        Notes
        -----
        The /DFLAB command is rarely used. Use it if you are writing a custom
        element and want to use degrees of freedom that are not part of the
        standard element set.
        """
        command = f"/DFLAB,{dof},{displab},{forcelab}"
        return self.run(command, **kwargs)

    def end(self, **kwargs):
        """Closes a macro file.

        APDL Command: ``*END``

        Notes
        -----
        Closes a file opened with ``*CREATE``. The ``*END`` command is an 8-character
        command (to differentiate it from ``*ENDIF``).   If you add commented text
        on that same line but do not allow enough spaces between ``*END`` and the
        "!" that indicates the comment text, the ``*END`` will attempt to interpret
        the "!" as the 8th character and will fail.

        This command is valid in any processor.
        """
        command = f"*END,"
        return self.run(command, **kwargs)

    def mkdir(self, dir_="", **kwargs):
        """Creates a directory.

        APDL Command: /MKDIR

        Parameters
        ----------
        dir_
            The directory to create (248 characters maximum on Linux;
            233 on Windows). If no path is provided, it will be
            created in the current working directory. Must be a valid
            name (and path) for the system you are working on.

        Notes
        -----
        It is recommended to just use ``os.mkdir``

        Creates a directory on the computer ANSYS is currently running on.
        """
        command = f"/MKDIR,{dir_}"
        return self.run(command, **kwargs)

    def msg(
        self,
        lab="",
        val1="",
        val2="",
        val3="",
        val4="",
        val5="",
        val6="",
        val7="",
        val8="",
        **kwargs,
    ):
        """Writes an output message via the ANSYS message subroutine.

        APDL Command: ``*MSG``

        Parameters
        ----------
        lab
            Label for output and termination control:

            Writes the message with no heading (default). - Writes the
            message with a "NOTE" heading.

            Writes the message with a "WARNING" heading.  Also writes
            the message to the errors file, Jobname.ERR. - Writes the
            message with a "ERROR" heading and causes run termination
            (if batch) at earliest "clean exit" point.  Also writes
            the message to the errors file, Jobname.ERR.

            Writes the message with a "FATAL ERROR" heading and causes
            run termination immediately.  Also writes the message to
            the errors file, Jobname.ERR. - Writes the message with a
            "NOTE" heading and displays it in the message dialog box.
            This option is most useful in GUI mode.

        val1, val2, val3, . . . , val8
            Numeric or alphanumeric character values to be included in message.
            Values may be the results of parameter evaluations.  All numeric
            values are assumed to be double precision. The FORTRAN nearest
            integer (NINT) function is used to form integers for the %I
            specifier.

        Notes
        -----
        Allows writing an output message via the ANSYS message subroutine.
        Also allows run termination control.  This command is used only when
        contained in a prepared file read into the ANSYS program (i.e.,
        ``*USE,/INPUT``, etc.).  A message format must immediately follow the ``*MSG``
        command (on a separate line, without parentheses, as described below).

        The message format may be up to 80 characters long, consisting of text
        strings and predefined "data descriptors" between the strings where
        numeric or alphanumeric character data are to be inserted.  The normal
        descriptors are %I for integer data, %G for double precision data, %C
        for alphanumeric character data, and %/ for a line break.  The
        corresponding FORTRAN data descriptors are I9, 1PG16.9 and A8,
        respectively.  Each descriptor must be preceded by a blank.  There must
        be one data descriptor for each specified value (8 maximum) in the
        order of the specified values.

        Enhanced descriptions may also be used:

        Do not begin ``*MSG`` format lines with ``*IF``, ``*ELSE`` ,
        ``*ELSEIF``, or ``*ENDIF`` .  If the last nonblank character
        of the message format is an ampersand (&), a second line will
        also be read as a continuation of the format.  Up to nine
        continuations (ten total lines) may be read.  If normal
        descriptions are used, then consecutive blanks are condensed
        into one blank upon output, and a period is appended.  Up to
        ten lines of output of 72 characters each may be produced
        (using the %/ descriptor).  Two examples follow.

        Here is an example of the ``*MSG`` command and a format to print a message
        with two integer values and one real value:

        The output line is:

        Here is an example illustrating multiline displays in GUI message
        windows:

        Note:: : The /UIS,MSGPOP command controls which messages are displayed
        in the message dialog box when the GUI is active.  All messages
        produced by the ``*MSG`` command are subject to the /UIS specification,
        with one exception,  If Lab = UI, the message will be displayed in the
        dialog box regardless of the /UIS specification.

        This command is valid in any processor.

        """
        command = f"*MSG,{lab},{val1},{val2},{val3},{val4},{val5},{val6},{val7},{val8}"
        return self.run(command, **kwargs)

    def pmacro(self, **kwargs):
        """Specifies that macro contents be written to the session log file.

        APDL Command: /PMACRO

        Notes
        -----
        This command forces the contents of a macro or other input file to be
        written to Jobname.LOG.  It is valid only within a macro or input file,
        and should be placed at the top of the file.  /PMACRO should be
        included in any macro or input file that calls GUI functions.
        """
        command = f"/PMACRO,"
        return self.run(command, **kwargs)

    def psearch(self, pname="", **kwargs):
        """Specifies a directory to be searched for "unknown command" macro files.

        APDL Command: /PSEARCH

        Parameters
        ----------
        pname
            Path name (64 characters maximum, and must include the final
            delimiter) of the middle directory to be searched.  Defaults to the
            user home directory.  If Pname = OFF, search only the ANSYS and
            current working directories.  If Pname = STAT, list the current
            middle directory and show the ANSYS_MACROLIB setting.

        Notes
        -----
        Specifies the pathname of a directory for file searches when reading
        "unknown command" macro files.  The search for the files is typically
        from the ANSYS directory, then from the user home directory, and then
        from the current working directory.  This command allows the middle
        directory searched to be other than the user home directory.

        This command is valid only at the Begin Level.
        """
        command = f"/PSEARCH,{pname}"
        return self.run(command, **kwargs)

    def rmdir(self, dir_="", **kwargs):
        """Removes (deletes) a directory.

        APDL Command: /RMDIR

        Parameters
        ----------
        dir\_
            The directory to remove. If no path is provided, it will be assumed
            to be in the current working directory. All files in the directory
            are also removed.

        Notes
        -----
        Removes a directory on the computer ANSYS is currently running on. No
        warning or prompt is given, so use with extreme caution.
        """
        command = f"/RMDIR,{dir_}"
        return self.run(command, **kwargs)

    def tee(self, label="", fname="", ext="", **kwargs):
        """Writes a list of commands to a specified file at the same time that the

        APDL Command: /TEE
        commands are being executed.

        Parameters
        ----------
        label
            Indicates how ANSYS is to interpret this /TEE command:

            Signals the beginning of the command text that is to be
            written to Fname. If Fname already exists, specifying NEW
            causes the contents of Fname to be overwritten. -
            Indicates that you want to append to Fname the command
            text that follows.

        fname
            File name and directory path (248 characters maximum, including the
            characters needed for the directory path).  An unspecified
            directory path defaults to the working directory; in this case, you
            can use all 248 characters for the file name.

        ext
            Filename extension (eight-character maximum).

        Notes
        -----
        You can use the /TEE command to record a macro to a specified file at
        the same time that the macro is being executed. It is similar to the
        Linux tee command.

        For more information about the /TEE command, see the Introducing APDL
        of the ANSYS Parametric Design Language Guide.

        The following example illustrates the use of the /TEE command. If you
        issue these commands:

        the content of myfile.mac is:

        This command is valid in any processor, but only during an interactive
        run.
        """
        command = f"/TEE,{label},{fname},{ext}"
        return self.run(command, **kwargs)

    def ulib(self, fname="", ext="", **kwargs):
        """Identifies a macro library file.

        APDL Command: ``*ULIB``

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
        Identifies a macro library file for the ``*USE`` command.  A
        library of macros allows blocks of often used ANSYS commands
        to be stacked and executed from a single file.  The macro
        blocks must be enclosed within block identifier and terminator
        lines as shown in the example below.  If you want to add
        comment lines to a macro block, you may place them anywhere
        within the macro block.  (This includes placing them directly
        on the lines where the macro block identifier and the macro
        block terminator appear, as shown in the example.)  Do not
        place comment lines (or any other lines) outside of a macro
        block.

        The name of the macro library file is identified for reading
        on the ``*ULIB`` command.  The name of the macro block is
        identified on the ``*USE`` command.  The commands within the macro
        block are copied to a temporary file (of the macro block name)
        during the ``*USE`` operation and executed as if a macro file of
        that name had been created by the user.  The temporary file is
        deleted after it has been used.  Macro block names should be
        acceptable filenames (system dependent) and should not match
        user created macro file names, since the user macro file will
        be used first (if it exists) before the library file is
        searched.  Macro blocks may be stacked in any order.
        Branching [``*GO`` or ``*IF``] external to the macro block is not
        allowed.

        This command is valid in any processor.
        """
        command = f"*ULIB,{fname},{ext}"
        return self.run(command, **kwargs)

    def use(
        self,
        name="",
        arg1="",
        arg2="",
        arg3="",
        arg4="",
        arg5="",
        arg6="",
        arg7="",
        arg8="",
        arg9="",
        ar10="",
        ar11="",
        ar12="",
        ar13="",
        ar14="",
        ag15="",
        ar16="",
        ar17="",
        ar18="",
        **kwargs,
    ):
        """Executes a macro file.

        APDL Command: ``*USE``

        Parameters
        ----------
        name
            Name (32 characters maximum, beginning with a letter) identifying
            the macro file or a macro block on a macro library file.

        arg1, arg2, arg3, . . . , ar18
            Values passed into the file or block where the parameters ARG1
            through ARG9 and AR10 through AR18 are referenced.  Values may be
            numbers, alphanumeric character strings (up to 32 characters
            enclosed in single quotes), parameters (numeric or character) or
            parametric expressions.  See below for additional details.

        Notes
        -----
        Causes execution of a macro file called Name, or, if not found, a macro
        block "Name" on the macro library file [``*ULIB``].  Argument values
        (numeric or character) are passed into the file or block and
        substituted for local parameters ARG1, ARG2, ..., AR18.  The file Name
        may also be executed as an "unknown command" (i.e., without the ``*USE``
        command name) as described below.

        A macro is a sequence of ANSYS commands (as many as needed) recorded in
        a file or in a macro block in a library file (specified with the ``*ULIB``
        command).  The file or block is typically executed with the ``*USE``
        command.  In addition to command, numerical and alphanumeric data, the
        macro may include parameters which will be assigned numerical or
        alphanumerical character values when the macro is used.  Use of the
        macro may be repeated (within a do-loop, for example) with the
        parameters incremented.  A macro is defined within a run by "enclosing"
        a sequence of data input commands between a ``*CREATE`` and a ``*END``
        command.  The data input commands are passive (not executed) while
        being written to the macro file.  The macro file (without ``*CREATE`` and
        ``*END`` ) can also be created external to ANSYS.

        Up to 99 specially named scalar parameters called ARG1 to AR99 are
        locally available to each macro.  Note that the prefix for the first 9
        parameters is "ARG," while the prefix for the last 90 is "AR."  A local
        parameter is one which is not affected by, nor does it affect, other
        parameters, even those of the same name, which are used outside of the
        macro.  The only way a local parameter can affect, or be affected by,
        parameters outside the macro is if values are passed out of, or into,
        the macro by an argument list.  Parameters ARG1 through AR18 can have
        their values (numeric or character) passed via the argument list on the
        ``*USE`` command (ARG1 through AR19 can be passed as arguments on the
        "unknown command" macro).  Parameters AR19 through AR99 (AR20 through
        AR99 in the "unknown command" macro) are available solely for use
        within the macro; they cannot be passed via an argument list.  Local
        parameters are available to do-loops and to /INPUT files processed
        within the macro.  In addition to an ARG1--AR99 set for each macro,
        another ARG1--AR99 set is available external to all macros, local to
        "non-macro" space.

        A macro is exited after its last line is executed.  Macros may be
        nested (such as a ``*USE`` or an "unknown command" within a macro).  Each
        nested macro has its own set of 99 local parameters.  Only one set of
        local parameters can be active at a time and that is the set
        corresponding to the macro currently being executed or to the set
        external to all macros (if any).  When a nested macro completes
        execution, the previous set of local parameters once again becomes
        available.  Use ``*STATUS,ARGX`` to view current macro parameter values.

        An alternate way of executing a macro file is via the "unknown command"
        route.  If a command unknown to the ANSYS program is entered, a search
        for a file of that name (plus a .MAC suffix) is made.  If the file
        exists, it is executed, if not, the "unknown command" message is
        output.  Thus, users can write their own commands in terms of other
        ANSYS commands.  The procedure is similar to issuing the ``*USE`` command
        with the unknown command in the Name field.  For example, the command
        CMD,10,20,30 is internally similar to ``*USE,CMD,10,20,30``.  The macro
        file named CMD.MAC will be executed with the three parameters.  The
        ``*USE`` macro description also applies to the "unknown command" macro,
        except that various directories are searched and a suffix (.MAC) is
        assumed.  Also, a macro library file is not searched.

        A three-level directory search for the "unknown command" macro file may
        be available (see the Operations Guide).  The search order may be: 1) a
        high-level system directory, 2) the login directory, and 3) the local
        (working) directory.  Use the /PSEARCH command to change the directory
        search path.  For an "unknown command" CMD, the first file named
        CMD.MAC found to exist in the search order will be executed.  The
        command may be input as upper or lower case, however, it is converted
        to upper case before the file name search occurs.  On systems that
        uniquely support both upper and lower case file names, the file with
        the matching lower case name will be used if it exists, otherwise, the
        file with the matching upper case name will be used. All macro files
        placed in the apdl directory must be upper case.

        Note, since undocumented commands exist in the ANSYS program, the user
        should issue the command intended for the macro file name to be sure
        the "unknown command" message is output in the processor where it's to
        be used.  If the macro is to be used in other processors, the other
        processors must also be checked.

        This command is valid in any processor.
        """
        command = f"*USE,{name},{arg1},{arg2},{arg3},{arg4},{arg5},{arg6},{arg7},{arg8},{arg9},{ar10},{ar11},{ar12},{ar13},{ar14},{ag15},{ar16},{ar17},{ar18}"
        with self.non_interactive:
            self.run(command, **kwargs)

        return self._response  # returning last response
