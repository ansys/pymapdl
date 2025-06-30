# Copyright (C) 2016 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


class MacroFiles:

    def cfclos(self, **kwargs):
        r"""Closes the "command" file.

        Mechanical APDL Command: `\*CFCLOS <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CFCLOS.html>`_

        Notes
        -----

        .. _a-CFCLOS_notes:

        This command is valid in any processor.
        """
        command = "*CFCLOS"
        return self.run(command, **kwargs)

    def cfopen(self, fname: str = "", ext: str = "", loc: str = "", **kwargs):
        r"""Opens a "command" file.

        Mechanical APDL Command: `\*CFOPEN <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CFOPEN.html>`_

        Parameters
        ----------
        fname : str
            File name and directory path (248 characters maximum, including the characters needed for the
            directory path). An unspecified directory path defaults to the working directory; in this case,
            you can use all 248 characters for the file name. The file name defaults to :file:`Jobname`.

        ext : str
            Filename extension (eight-character maximum). The extension defaults to CMD if ``Fname`` is
            blank.

        loc : str
            Determines whether existing file will be overwritten or appended:

            * ``(blank)`` - The existing file will be overwritten.

            * ``APPEND`` - The file will be appended to the existing file.

        Notes
        -----

        .. warning::

           This function contains specificities regarding the argument definitions.
           Please refer to the `command documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CFOPEN.html>`_
           for further explanations.

        **Argument Descriptions**

        .. _a-CFOPEN_argdescript:

        * ``fname : str`` - File name and directory path (248 characters maximum, including the characters
        needed for the
        directory path). An unspecified directory path defaults to the working directory; in this case, you
        can use all 248 characters for the file name. The file name defaults to :file:`Jobname`.

        * ``ext : str`` - Filename extension (eight-character maximum). The extension defaults to CMD if
        ``Fname`` is blank.

        * ``loc : str`` - Determines whether existing file will be overwritten or appended:

          * ``(blank)`` - The existing file will be overwritten.

          * ``APPEND`` - The file will be appended to the existing file.

        .. _a-CFOPEN_notes:

        Mechanical APDL commands specified by the :ref:`cfwrite` command are written to the file opened by
        :ref:`cfopen`. Data processed with the :ref:`vwrite` command are also written to this file if the
        file is open when the :ref:`vwrite` command is issued.

        Issue the :ref:`cfclos` command to close the command file.

        This command is valid in any processor.
        """
        command = f"*CFOPEN,{fname},{ext},,{loc}"
        return self.run(command, **kwargs)

    def cfwrite(self, command: str = "", **kwargs):
        r"""Writes a Mechanical APDL command (or similar string) to a "command" file.

        Mechanical APDL Command: `\*CFWRITE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CFWRITE.html>`_

        Parameters
        ----------
        command : str
            Command or string to be written. The standard command form of a label followed by arguments
            separated by commas is assumed. ``Command`` may be a parameter assignment (for example,
            :ref:`cfwrite`, A = 5).

        Notes
        -----

        .. warning::

           This function contains specificities regarding the argument definitions.
           Please refer to the `command documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CFWRITE.html>`_
           for further explanations.

        **Argument Descriptions**

        .. _a-CFWRITE_argdescript:

        * ``command : str`` - Command or string to be written. The standard command form of a label followed
          by arguments separated by commas is assumed. ``Command`` may be a parameter assignment (for example,
          :ref:`cfwrite`, A = 5).

        .. _a-CFWRITE_notes:

        Writes a Mechanical APDL command (or similar string) to the file opened via :ref:`cfopen`. The
        ``Command``
        string is not executed (except that numeric and character parameter substitution and operations
        (with imbedded \*, /, >, etc. characters) are performed before writing).

        When used with :ref:`get` results and parameter substitution, a command can be created from results
        and then read back into the Mechanical APDL program (or used elsewhere). For example, if the command
        :ref:`cfwrite`,BF,NNUM,TEMP,TVAL is used in a do-loop, where TVAL is a parameter value returned from
        the :ref:`get` operation and NNUM is a specified or returned parameter value, a series of :ref:`bf`
        commands, with numerical values substituted for the two parameters, will be written.

        To create a file without parameter substitution, issue :ref:`create`.

        This command is valid in any processor.
        """
        command = f"*CFWRITE,{command}"
        return self.run(command, **kwargs)

    def create(self, fname: str = "", ext: str = "", **kwargs):
        r"""Opens (creates) a macro file.

        Mechanical APDL Command: `\*CREATE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CREATE.html>`_

        .. warning::

            This command must be run using :func:`non_interactive <ansys.mapdl.core.Mapdl.non_interactive>`.
            Please visit `Unsupported Interactive Commands <https://mapdl.docs.pyansys.com/version/stable/user_guide/mapdl.html#unsupported-interactive-commands>`_
            for further information.

        Parameters
        ----------
        fname : str
            File name and directory path (248 characters maximum, including the characters needed for the
            directory path). An unspecified directory path defaults to the working directory; in this case,
            you can use all 248 characters for the file name. Do not use a directory path if file is to be
            read with the macro ``Name`` option of the :ref:`use` command.

        ext : str
            Filename extension (eight-character maximum). ``Ext`` should not be used if file is to be read
            with the macro ``Name`` option of the :ref:`use` command.

        Notes
        -----

        .. warning::

           This function contains specificities regarding the argument definitions.
           Please refer to the `command documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CREATE.html>`_
           for further explanations.

        **Argument Descriptions**

        .. _a-CREATE_argdescript:

        * ``fname : str`` - File name and directory path (248 characters maximum, including the characters
        needed for the
        directory path). An unspecified directory path defaults to the working directory; in this case, you
        can use all 248 characters for the file name. Do not use a directory path if file is to be read with
        the macro
          ``Name`` option of the :ref:`use` command.

        * ``ext : str`` - Filename extension (eight-character maximum). ``Ext`` should not be used if file
        is to be read with the macro
          ``Name`` option of the :ref:`use` command.

        .. _a-CREATE_notes:

        See the :ref:`use` command for a discussion of macros. All commands following the :ref:`create`
        command, up to the :ref:`end` command, are written to the specified file without being executed. An
        existing file of the same name, if any, will be overwritten. Parameter values are not substituted
        for parameter names in the commands when the commands are written to the file. Use :ref:`cfwrite` to
        create a file if this is desired. The resulting macro may be executed with a :ref:`use` command
        (which also allows parameters to be passed into the macro) or a :ref:`input` command (which does not
        allow parameters to be passed in). Several macros may be stacked into a library file ( :ref:`ulib`
        ). You cannot use :ref:`create` within a DO loop.

        This command is valid in any processor.
        """
        command = f"*CREATE,{fname},{ext}"
        return self.run(command, **kwargs)

    def end(self, **kwargs):
        r"""Closes a macro file.

        Mechanical APDL Command: `\*END <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_END.html>`_

        Notes
        -----

        .. _a-END_notes:

        Closes a file opened with :ref:`create`. The :ref:`end` command is an 8-character command (to
        differentiate it from ``*ENDIF`` ). If you add commented text on that same line but do not allow
        enough spaces between :ref:`end` and the "!" that indicates the comment text, the :ref:`end` will
        attempt to interpret the "!" as the 8th character and will fail.

        This command is valid in any processor.
        """
        command = "*END"
        return self.run(command, **kwargs)

    def mkdir(self, dir_: str = "", **kwargs):
        r"""Creates a directory.

        Mechanical APDL Command: `/MKDIR <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MKDIR.html>`_

        Parameters
        ----------
        dir_ : str
            The directory to create (248 characters maximum on Linux; 233 on Windows). If no path is
            provided, it will be created in the current working directory. Must be a valid name (and path)
            for the system you are working on.

        Notes
        -----

        .. warning::

           This function contains specificities regarding the argument definitions.
           Please refer to the `command documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MKDIR.html>`_
           for further explanations.

        **Argument Descriptions**
        * ``Dir`` - The directory to create (248 characters maximum on Linux; 233 on Windows). If no path is
          provided, it will be created in the current working directory. Must be a valid name (and path) for
          the system you are working on.

        Creates a directory on the computer Mechanical APDL is currently running on.
        """
        command = f"/MKDIR,{dir_}"
        return self.run(command, **kwargs)

    def msg(
        self,
        lab: str = "",
        val1: str = "",
        val2: str = "",
        val3: str = "",
        val4: str = "",
        val5: str = "",
        val6: str = "",
        val7: str = "",
        val8: str = "",
        **kwargs,
    ):
        r"""Writes an output message via the Mechanical APDL message subroutine.

        Mechanical APDL Command: `\*MSG <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MSG.html>`_

        Parameters
        ----------
        lab : str
            Label for output and termination control:

            * ``INFO`` - Writes the message with no heading (default).

            * ``NOTE`` - Writes the message with a "NOTE" heading.

            * ``WARN`` - Writes the message with a "WARNING" heading. Also writes the message to the errors
              file, :file:`JobnameERR`.

            * ``ERROR`` - Writes the message with a "ERROR" heading and causes run termination (if batch) at
              earliest "clean exit" point. Also writes the message to the errors file, :file:`JobnameERR`.

            * ``FATAL`` - Writes the message with a "FATAL ERROR" heading and causes run termination
              immediately. Also writes the message to the errors file, :file:`JobnameERR`.

            * ``UI`` - Writes the message with a "NOTE" heading and displays it in the message dialog box. This
              option is most useful in GUI mode.

        val1 : str
            Numeric or alphanumeric character values to be included in message. Values may be the results of
            parameter evaluations. All numeric values are assumed to be double precision. The FORTRAN
            nearest integer (NINT) function is used to form integers for the %I specifier.

        val2 : str
            Numeric or alphanumeric character values to be included in message. Values may be the results of
            parameter evaluations. All numeric values are assumed to be double precision. The FORTRAN
            nearest integer (NINT) function is used to form integers for the %I specifier.

        val3 : str
            Numeric or alphanumeric character values to be included in message. Values may be the results of
            parameter evaluations. All numeric values are assumed to be double precision. The FORTRAN
            nearest integer (NINT) function is used to form integers for the %I specifier.

        val4 : str
            Numeric or alphanumeric character values to be included in message. Values may be the results of
            parameter evaluations. All numeric values are assumed to be double precision. The FORTRAN
            nearest integer (NINT) function is used to form integers for the %I specifier.

        val5 : str
            Numeric or alphanumeric character values to be included in message. Values may be the results of
            parameter evaluations. All numeric values are assumed to be double precision. The FORTRAN
            nearest integer (NINT) function is used to form integers for the %I specifier.

        val6 : str
            Numeric or alphanumeric character values to be included in message. Values may be the results of
            parameter evaluations. All numeric values are assumed to be double precision. The FORTRAN
            nearest integer (NINT) function is used to form integers for the %I specifier.

        val7 : str
            Numeric or alphanumeric character values to be included in message. Values may be the results of
            parameter evaluations. All numeric values are assumed to be double precision. The FORTRAN
            nearest integer (NINT) function is used to form integers for the %I specifier.

        val8 : str
            Numeric or alphanumeric character values to be included in message. Values may be the results of
            parameter evaluations. All numeric values are assumed to be double precision. The FORTRAN
            nearest integer (NINT) function is used to form integers for the %I specifier.

        Notes
        -----

        .. warning::

           This function contains specificities regarding the argument definitions.
           Please refer to the `command documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MSG.html>`_
           for further explanations.

        **Argument Descriptions**

        .. _a-MSG_argdescript:

        * ``lab : str`` - Label for output and termination control:

          * ``INFO`` - Writes the message with no heading (default).

          * ``NOTE`` - Writes the message with a "NOTE" heading.

          * ``WARN`` - Writes the message with a "WARNING" heading. Also writes the message to the errors
            file, :file:`JobnameERR`.

          * ``ERROR`` - Writes the message with a "ERROR" heading and causes run termination (if batch) at
            earliest "clean exit" point. Also writes the message to the errors file, :file:`JobnameERR`.

          * ``FATAL`` - Writes the message with a "FATAL ERROR" heading and causes run termination
            immediately. Also writes the message to the errors file, :file:`JobnameERR`.

          * ``UI`` - Writes the message with a "NOTE" heading and displays it in the message dialog box. This
            option is most useful in GUI mode.

        * ``val1, val2, val3,..., val8 : str`` - Numeric or alphanumeric character values to be included
          in message. Values may be the results of parameter evaluations. All numeric values are assumed to be
          double precision. The FORTRAN nearest integer (NINT) function is used to form integers for the %I
          specifier.

        .. _a-MSG_notes:

        Allows writing an output message via the Mechanical APDL message subroutine. Also allows run
        termination
        control. This command is used only when contained in a prepared file read into the Mechanical APDL
        program
        (that is, :ref:`use`, :ref:`input`, etc.). A message format must immediately follow the :ref:`msg`
        command (on a separate line, without parentheses, as described below).

        The message format may be up to 80 characters long, consisting of text strings and predefined "data
        descriptors" between the strings where numeric or alphanumeric character data are to be inserted.
        The normal descriptors are %I for integer data, %G for double precision data, %C for alphanumeric
        character data, and %/ for a line break. The corresponding FORTRAN data descriptors are I9, 1PG16.9
        and A8, respectively. Each descriptor must be preceded by a blank. There must be one data descriptor
        for each specified value (8 maximum) in the order of the specified values.

        Enhanced descriptions may also be used:  This command contains some tables and extra information
        which can be inspected in the original documentation pointed above.

        Do not begin :ref:`msg` format lines with ``*IF``, ``*ELSE``, ``*ELSEIF``, or ``*ENDIF``. If the
        last nonblank character of the message format is an ampersand (&), a second line will also be read
        as a continuation of the format. Up to nine continuations (ten total lines) may be read. If normal
        descriptions are used, then consecutive blanks are condensed into one blank upon output, and a
        period is appended. Up to ten lines of output of 72 characters each may be produced (using the %/
        descriptor). Two examples follow.

        Here is an example of the :ref:`msg` command and a format to print a message with two integer values
        and one real value:

        .. code:: apdl

           *MSG, INFO, 'Inner',25,1.2,148
           Radius ( %C) = %I, Thick = %G, Length = %I

        The output line is:

        .. code:: apdl

           Radius (Inner) = 25, Thick = 1.2, Length = 148.

        Here is an example illustrating multiline displays in GUI message windows:

        .. code:: apdl

           *MSG,UI,Vcoilrms,THTAv,Icoilrms,THTAi,Papprnt,Pelec,PF,indctnc
           Coil RMS voltage, RMS current, apparent pwr, actual pwr, pwr factor: %/&
           Vcoil = %G V (electrical angle = %G DEG) %/&
           Icoil = %G A (electrical angle = %G DEG) %/&
           APPARENT POWER = %G W %/&
           ACTUAL POWER = %G W %/&
           Power factor: %G %/&
           Inductance = %G %/&
           VALUES ARE FOR ENTIRE COIL (NOT JUST THE MODELED SECTOR)

        The :ref:`uis`,MSGPOP command controls which messages are displayed in the message dialog box when
        the GUI is active. All messages produced by the :ref:`msg` command are subject to the :ref:`uis`
        specification, with one exception, If ``Lab`` = UI, the message will be displayed in the dialog box
        regardless of the :ref:`uis` specification.

        This command is valid in any processor.
        """
        command = f"*MSG,{lab},{val1},{val2},{val3},{val4},{val5},{val6},{val7},{val8}"
        return self.run(command, **kwargs)

    def pmacro(self, **kwargs):
        r"""Specifies that macro contents be written to the session log file.

        Mechanical APDL Command: `/PMACRO <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PMACRO.html>`_

        Notes
        -----

        .. _s-PMACRO_notes:

        This command forces the contents of a macro or other input file to be written to
        :file:`Jobname.LOG`. It is valid only within a macro or input file, and should be placed at the top
        of the file. :ref:`pmacro`   should be included in any macro or input file that calls GUI
        functions.
        """
        command = "/PMACRO"
        return self.run(command, **kwargs)

    def psearch(self, pname: str = "", **kwargs):
        r"""Specifies a directory to be searched for "unknown command" macro files.

        Mechanical APDL Command: `/PSEARCH <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PSEARCH.html>`_

        Parameters
        ----------
        pname : str
            Path name (64 characters maximum, and must include the final delimiter) of the middle directory
            to be searched. Defaults to the user home directory. If ``Pname`` = OFF, search only the program
            and current working directories. If ``Pname`` = STAT, list the current middle directory and show
            the ANSYS_MACROLIB setting.

        Notes
        -----

        .. _s-PSEARCH_notes:

        Specifies the pathname of a directory for file searches when reading unknown-command macro files.

        The search for the files is typically from the program directory, then from the user home directory,
        and then from the current working directory. The command allows the middle directory searched to be
        other than the user home directory.

        This command is valid only at the Begin level.
        """
        command = f"/PSEARCH,{pname}"
        return self.run(command, **kwargs)

    def rmdir(self, dir_: str = "", **kwargs):
        r"""Removes (deletes) a directory.

        Mechanical APDL Command: `/RMDIR <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_RMDIR.html>`_

        Parameters
        ----------
        dir_ : str
            The directory to remove. If no path is provided, it will be assumed to be in the current working
            directory. All files in the directory are also removed.

        Notes
        -----

        .. warning::

           This function contains specificities regarding the argument definitions.
           Please refer to the `command documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_RMDIR.html>`_
           for further explanations.

        **Argument Descriptions**
        * ``Dir`` - The directory to remove. If no path is provided, it will be assumed to be in the current
          working directory. All files in the directory are also removed.

        Removes a directory on the computer on which Mechanical APDL is currently running. No warning or
        prompt is
        given, so use with extreme caution.
        """
        command = f"/RMDIR,{dir_}"
        return self.run(command, **kwargs)

    def slashtee(self, label: str = "", fname: str = "", ext: str = "", **kwargs):
        r"""Writes a list of commands to a specified file at the same time that the commands are being executed.

        Mechanical APDL Command: `/TEE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_TEE_sl.html>`_

        Parameters
        ----------
        label : str
            Specifies how Mechanical APDL is to interpret this :ref:`slashtee` command:

            * ``NEW`` - Signals the beginning of the command text that is to be written to ``Fname``. If
              ``Fname`` already exists, specifying NEW causes the contents of ``Fname`` to be overwritten.

            * ``APPEND`` - Indicates that you want to append to ``Fname`` the command text that follows.

            * ``END`` - Signals the end of the command text that is to be written to or appended to ``Fname``.

        fname : str
            File name and directory path (248 characters maximum, including the characters needed for the
            directory path). An unspecified directory path defaults to the working directory; in this case,
            you can use all 248 characters for the file name.

        ext : str
            Filename extension (eight-character maximum). If you plan to execute the file as if it were a
            Mechanical APDL command, use the extension ``.mac``.

        Notes
        -----

        .. warning::

           This function contains specificities regarding the argument definitions.
           Please refer to the `command documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_TEE_sl.html>`_
           for further explanations.

        **Argument Descriptions**

        .. _pmTEEsargdescript:

        * ``label : str`` - Specifies how Mechanical APDL is to interpret this :ref:`slashtee` command:

          * ``NEW`` - Signals the beginning of the command text that is to be written to ``Fname``. If
            ``Fname`` already exists, specifying NEW causes the contents of ``Fname`` to be overwritten.

          * ``APPEND`` - Indicates that you want to append to ``Fname`` the command text that follows.

          * ``END`` - Signals the end of the command text that is to be written to or appended to ``Fname``.

        * ``fname : str`` - File name and directory path (248 characters maximum, including the characters
        needed for the
        directory path). An unspecified directory path defaults to the working directory; in this case, you
        can use all 248 characters for the file name.
        * ``ext : str`` - Filename extension (eight-character maximum). If you plan to execute the file as
        if it were a Mechanical APDL command, use
          the extension ``.mac``.

        .. _s-TEE_notes:

        You can use the :ref:`slashtee` command to record a macro to a specified file at the same time that
        the macro is being executed. It is similar to the Linux **tee** command.

        For more information about the :ref:`slashtee` command, see the of the `Ansys Parametric Design
        Language Guide <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_apdl/apdlxpl.html>`_.

        The following example illustrates the use of the :ref:`slashtee` command. If you issue these
        commands:

        .. code:: apdl

           /tee,new,myfile,mac
           et,1,42,0,0,1
           ex,1,3e7
           /tee,end
           /tee,append,myfile,mac
           n,1,8
           n,5,11
           fill
           ngen,5,5,1,5,1,0,1
           /tee,end

        the content of **myfile.mac** is:

        .. code:: apdl

           et,1,42,0,0,1
           ex,1,3e7
           n,1,8
           n,5,11
           fill
           ngen,5,5,1,5,1,0,1

        This command is valid in any processor, but only during an interactive run.
        """
        command = f"/TEE,{label},{fname},{ext}"
        return self.run(command, **kwargs)

    def ulib(self, fname: str = "", ext: str = "", **kwargs):
        r"""Identifies a macro library file.

        Mechanical APDL Command: `\*ULIB <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ULIB.html>`_

        Parameters
        ----------
        fname : str
            File name and directory path (248 characters maximum, including the characters needed for the
            directory path). An unspecified directory path defaults to the working directory; in this case,
            you can use all 248 characters for the file name.

        ext : str
            Filename extension (eight-character maximum).

        Notes
        -----

        .. warning::

           This function contains specificities regarding the argument definitions.
           Please refer to the `command documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ULIB.html>`_
           for further explanations.

        **Argument Descriptions**

        .. _a-ULIB_argdescript:

        * ``fname : str`` - File name and directory path (248 characters maximum, including the characters
          needed for the directory path). An unspecified directory path defaults to the working directory; in
          this case, you can use all 248 characters for the file name.

        * ``ext : str`` - Filename extension (eight-character maximum).

        .. _a-ULIB_notes:

        Identifies a macro library file for the :ref:`use` command.

        A library of macros allows blocks of often-used commands to be stacked and executed from a single
        file. The macro blocks must be enclosed within block identifier and terminator lines as shown in
        this example:   **Example: Macro Blocks**

          .. code:: apdl

             ABC! Any valid alphanumeric name (32 characters maximum)
             !  identifying this data block
             ---! Mechanical APDL data-input commands
             ---
             ---
             /EOF! Terminator for this data block
             XYZ! Identify another data block (if desired)
             ---! Mechanical APDL data-input commands
             ---
             ---
             /EOF! Terminator for this data block
             (etc.)

        To add comment lines to a macro block, place them anywhere within the macro block, including
        directly on the lines where the macro block identifier and the macro block terminator appear as
        shown in the example. Do not place comment lines (or any other lines) outside of a macro block.

        The name of the macro library file is identified for reading via :ref:`ulib`. The name of the macro
        block is identified via :ref:`use`.

        Commands within the macro block are copied to a temporary file (of the macro block name) during the
        :ref:`use` operation and executed as if a macro file of that name had been created. The temporary
        file is deleted after it has been used.

        Macro block names should be acceptable file names (system-dependent) and should not match user-
        created macro file names, as the user-created macro file is used first (if it exists) before the
        library file is searched.

        Macro blocks may be stacked in any order. Branching ( ``*GO`` or ``*IF`` ) external to the macro
        block is not allowed.

        This command is valid in any processor.
        """
        command = f"*ULIB,{fname},{ext}"
        return self.run(command, **kwargs)

    def use(
        self,
        name: str = "",
        arg1: str = "",
        arg2: str = "",
        arg3: str = "",
        arg4: str = "",
        arg5: str = "",
        arg6: str = "",
        arg7: str = "",
        arg8: str = "",
        arg9: str = "",
        ar10: str = "",
        ar11: str = "",
        ar12: str = "",
        ar13: str = "",
        ar14: str = "",
        ag15: str = "",
        ar16: str = "",
        ar17: str = "",
        ar18: str = "",
        **kwargs,
    ):
        r"""Executes a macro file.

        Mechanical APDL Command: `\*USE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_USE.html>`_

        Parameters
        ----------
        name : str
            Name (32 characters maximum, beginning with a letter) identifying the macro file or a macro
            block on a macro library file.

        arg1 : str
            Values passed into the file or block where the parameters ARG1 through ARG9 and AR10 through
            AR18 are referenced. Values may be numbers, alphanumeric character strings (up to 32 characters
            enclosed in single quotes), parameters (numeric or character) or parametric expressions. See
            below for additional details.

        arg2 : str
            Values passed into the file or block where the parameters ARG1 through ARG9 and AR10 through
            AR18 are referenced. Values may be numbers, alphanumeric character strings (up to 32 characters
            enclosed in single quotes), parameters (numeric or character) or parametric expressions. See
            below for additional details.

        arg3 : str
            Values passed into the file or block where the parameters ARG1 through ARG9 and AR10 through
            AR18 are referenced. Values may be numbers, alphanumeric character strings (up to 32 characters
            enclosed in single quotes), parameters (numeric or character) or parametric expressions. See
            below for additional details.

        arg4 : str
            Values passed into the file or block where the parameters ARG1 through ARG9 and AR10 through
            AR18 are referenced. Values may be numbers, alphanumeric character strings (up to 32 characters
            enclosed in single quotes), parameters (numeric or character) or parametric expressions. See
            below for additional details.

        arg5 : str
            Values passed into the file or block where the parameters ARG1 through ARG9 and AR10 through
            AR18 are referenced. Values may be numbers, alphanumeric character strings (up to 32 characters
            enclosed in single quotes), parameters (numeric or character) or parametric expressions. See
            below for additional details.

        arg6 : str
            Values passed into the file or block where the parameters ARG1 through ARG9 and AR10 through
            AR18 are referenced. Values may be numbers, alphanumeric character strings (up to 32 characters
            enclosed in single quotes), parameters (numeric or character) or parametric expressions. See
            below for additional details.

        arg7 : str
            Values passed into the file or block where the parameters ARG1 through ARG9 and AR10 through
            AR18 are referenced. Values may be numbers, alphanumeric character strings (up to 32 characters
            enclosed in single quotes), parameters (numeric or character) or parametric expressions. See
            below for additional details.

        arg8 : str
            Values passed into the file or block where the parameters ARG1 through ARG9 and AR10 through
            AR18 are referenced. Values may be numbers, alphanumeric character strings (up to 32 characters
            enclosed in single quotes), parameters (numeric or character) or parametric expressions. See
            below for additional details.

        arg9 : str
            Values passed into the file or block where the parameters ARG1 through ARG9 and AR10 through
            AR18 are referenced. Values may be numbers, alphanumeric character strings (up to 32 characters
            enclosed in single quotes), parameters (numeric or character) or parametric expressions. See
            below for additional details.

        ar10 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_USE.html>`_
            for further information.

        ar11 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_USE.html>`_
            for further information.

        ar12 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_USE.html>`_
            for further information.

        ar13 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_USE.html>`_
            for further information.

        ar14 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_USE.html>`_
            for further information.

        ag15 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_USE.html>`_
            for further information.

        ar16 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_USE.html>`_
            for further information.

        ar17 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_USE.html>`_
            for further information.

        ar18 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_USE.html>`_
            for further information.

        Notes
        -----

        .. warning::

           This function contains specificities regarding the argument definitions.
           Please refer to the `command documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_USE.html>`_
           for further explanations.

        **Argument Descriptions**

        .. _a-USE_argdescript:

        * ``name : str`` - Name (32 characters maximum, beginning with a letter) identifying the macro file
          or a macro block on a macro library file.

        * ``arg1, arg2, arg3,..., ar18 : str`` - Values passed into the file or block where the
          parameters ARG1 through ARG9 and AR10 through AR18 are referenced. Values may be numbers,
          alphanumeric character strings (up to 32 characters enclosed in single quotes), parameters (numeric
          or character) or parametric expressions. See below for additional details.

        .. _a-USE_notes:

        Causes execution of a macro file called ``Name``, or, if not found, a macro block " ``Name`` " on
        the macro library file ( :ref:`ulib` ). Argument values (numeric or character) are passed into the
        file or block and substituted for local parameters ARG1, ARG2,..., AR18. The file ``Name`` may also
        be executed as an "unknown command" (that is, without the :ref:`use` command name) as described
        below.

        A macro is a sequence of Mechanical APDL commands (as many as needed) recorded in a file or in a
        macro
        block in a library file (specified with the :ref:`ulib` command). The file or block is typically
        executed via :ref:`use`. In addition to command, numerical and alphanumeric data, the macro can
        include parameters which will be assigned numerical or alphanumerical character values when the
        macro is used. Use of the macro can be repeated (within a do-loop, for example) with the parameters
        incremented.

        A macro is defined within a run by enclosing a sequence of data input commands between :ref:`create`
        and :ref:`end` commands. The data input commands are passive (not executed) while being written to
        the macro file. The macro file (without :ref:`create` and :ref:`end` ) can also be created external
        to Mechanical APDL.

        Up to 99 specially named scalar parameters, ARG1 to AR99, are locally available to each macro:

        * The prefix for the first nine parameters is ARG, and the prefix for the remaining 90 parameters is
          AR.

        * A local parameter is not affected by, nor does it affect, other parameters, even those of the same
          name, which are used outside of the macro. The only way a local parameter can affect, or be
          affected by, parameters outside the macro is if values are passed out of, or into, the macro by an
          argument list.

        * Parameters ARG1 through AR18 can have their values (numeric or character) passed via the argument
          list on :ref:`use`. (ARG1 through AR19 can be passed as arguments on the unknown-command macro.)
          Parameters AR19 through AR99 (AR20 through AR99 in the unknown-command macro) are available solely
          for use within the macro; they cannot be passed via an argument list.

        * Local parameters are available to do-loops and to :ref:`input` files processed within the macro.
          In addition to an ARG1--AR99 set for each macro, another ARG1--AR99 set is available external to
          all macros, local to "non-macro" space.

        A macro is exited after its last line is executed. Macros may be nested (such as a :ref:`use` or an
        unknown command within a macro). Each nested macro has its own set of 99 local parameters. Only one
        set of local parameters can be active at a time and that is the set corresponding to the macro
        currently being executed or to the set external to all macros (if any). When a nested macro
        completes execution, the previous set of local parameters once again becomes available. Issue
        :ref:`starstatus`,ARGX to view current macro parameter values.

        An alternate way of executing a macro file is via the unknown-command route. If a command unknown to
        Mechanical APDL is entered, a search for a file of that name (plus a :file:`.MAC` suffix) is made.
        If the file exists, it is executed, if not, the "unknown command" message is output. Thus, you can
        write your own commands in terms of other Mechanical APDL commands. The procedure is similar to
        issuing :ref:`use` with the unknown command in the ``Name`` field. For example, the command **CMD**
        ,10,20,30 is internally similar to :ref:`use`,CMD,10,20,30. The macro file named :file:`CMD.MAC` is
        executed with the three parameters. The :ref:`use` macro description also applies to the unknown-
        command macro, except that various directories are searched and a suffix ( :file:`.MAC` ) is
        assumed. Also, a macro library file is not searched.

        A three-level directory search for the unknown-command macro file may be available. The search order
        may be: 1) a high-level system directory, 2) the log-in directory, and 3) the local (working)
        directory. Issue :ref:`psearch` to change the directory search path. For an unknown command **CMD**,
        the first file named :file:`CMD.MAC` found to exist in the search order is executed. The command can
        be input in lower-, upper-, or mixed-case; however, it converts to uppercase automatically before
        the file name search occurs. On systems that preserve the case as it was input, a file matching the
        upper-case name is used first, followed by a file with the matching the lower-case name, and finally
        a file matching the mixed-case name. All macro files placed in the :file:`apdl` directory must be
        upper-case.

        Because undocumented commands exist in Mechanical APDL, you should issue the command intended for
        the macro
        file name to ensure that the unknown-command message is output in the processor where it is to be
        used. If the macro is to be used in other processors, the other processors must also be checked.

        This command is valid in any processor.
        """
        command = f"*USE,{name},{arg1},{arg2},{arg3},{arg4},{arg5},{arg6},{arg7},{arg8},{arg9},{ar10},{ar11},{ar12},{ar13},{ar14},{ag15},{ar16},{ar17},{ar18}"
        return self.run(command, **kwargs)
