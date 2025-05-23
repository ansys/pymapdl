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


class RunControls:

    def config(self, lab: str = "", val: str = "", **kwargs):
        r"""Assigns values to Mechanical APDL configuration parameters.

        Mechanical APDL Command: `/CONFIG <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CONFIG.html>`_

        Parameters
        ----------
        lab : str
            Configuration parameter to be changed:

            * ``NORSTGM`` - Option to write or not write geometry data to the results file:

              * When ``VAL`` = 0, write geometry data (default).
              * When ``VAL`` = 1, does not write geometry data.

              Useful when complex analyses are likely to create abnormally large files.

            * ``NBUF`` - The number of buffers ( ``VAL`` = 1 to 32) per file in the solver. Default: ``VAL`` =
              4.

            * ``LOCFL`` - File open and close actions:

              * When ``VAL`` = 0, global (default).
              * When ``VAL`` = 1, local.

              Applies to :file:`File.EROT`, :file:`File.ESAV`, and :file:`FileEMAT`.

              Typically used for large problems where locally closed files may be deleted earlier in the run via
              :ref:`slashfdele`.

            * ``SZBIO`` - Record size ( ``VAL`` = 1024 to 4194304) of binary files (in integer words).

              Default: ``VAL`` = 16384 (system-dependent).

            * ``FSPLIT`` - Defines split points for binary files. ``VAL`` is the file split point in megawords.

              Default: ``VAL`` = Maximum file size for the system.

            * ``MXND`` - Maximum number of nodes.

              Default: ``VAL`` = 100 at first encounter.

              Dynamically expanded by doubling, even at first encounter, when the maximum is exceeded.

            * ``MXEL`` - Maximum number of elements. Default and expansion as for MXND.

            * ``MXKP`` - Maximum number of keypoints. Default and expansion as for MXND.

            * ``MXLS`` - Maximum number of lines. Default and expansion as for MXND.

            * ``MXAR`` - Maximum number of areas. Default and expansion as for MXND.

            * ``MXVL`` - Maximum number of volumes. Default and expansion as for MXND.

            * ``MXRL`` - Maximum number of sets of real constants (element attributes). Default and expansion as
              for MXND.

            * ``MXCP`` - Maximum number of sets of coupled degrees of freedom. Default and expansion as for
              MXND.

            * ``MXCE`` - Maximum number of constraint equations. Default and expansion as for MXND.

            * ``NOELDB`` - Option to write or not write results into the database after a solution.

              * When ``VAL`` = 0 (default), writes results into the database.
              * When ``VAL`` = 1, does not write results into the database.
            * ``NUMLV`` - Maximum number of load vectors written on :file:`Jobname.MODE` file when ``MSUPkey`` =
              YES on the :ref:`mxpand` command.

              Default: ``VAL`` = 1000 at first encounter.

              When the maximum is exceeded, the value is not expanded.

              The NUMLV option is not supported for fast load vector generation ( ``FastLV`` = ON on the
              :ref:`modcont` command).

            * ``NUMSUBLV`` - Maximum number of load vectors written on :file:`Jobname.SUB` file in
              substructure/CMS generation pass.

              Default: ``VAL`` = 31 at first encounter.

              When the maximum is exceeded, the value is not expanded.

            * ``GRW_NBUF`` - Option to automatically grow the number of file buffers for most binary files ( :file:`.ESAV`,
              :file:`.EMAT`, :file:`.FULL`, and so on), with the exception of the results file and files written
              by the sparse and PCG equation solvers (for example, :file:`.DSPxxxx` and :file:`.PCn` ).

              * When ``VAL`` = -1, the number of file buffers does not grow automatically for any file.
              * When ``VAL`` = 0 (default), the number of file buffers may or may not grow automatically. The
                logic is program-controlled.
              * When ``VAL`` = 1, the number of file buffers automatically grows for most binary files to reduce
                the amount of I/O. This option may require a significantly greater amount of memory than the
                default behavior ( ``VAL`` = 0).
            * ``MEBA_LIC`` - Option to control automatic checkout of a Mechanical batch license during solution when the
              capability is not enabled, useful for PrepPost sessions:

              * When ``VAL`` = 0 (default), check out a license automatically when needed.
              * When ``VAL`` = 1, bypass automatic license checkout.
            * ``STAT`` - Displays current values set by the :ref:`config` command.

        val : str
            Value (an integer number) assigned to the specified configuration parameter.

        Notes
        -----

        .. _s-CONFIG_notes:

        All configuration parameters have initial defaults, which in most cases do not need to be changed.
        Where a specially configured version of the Mechanical APDL program is desired, the parameters can
        be
        changed with this command.

        Issue :ref:`config`,STAT to display current values.

        Define changes before the parameter is required.

        These changes (and others) may also be incorporated into the :file:`config.ans` file, read in upon
        execution of the program. (See `The Configuration File
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/Hlp_G_BAS19_4.html#a6c2Kn1b3ctg>`_
        in the `Basic Analysis Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/Hlp_G_BAS19.html>`_.) If the same
        configuration parameter appears in both the configuration file and
        this command, this command overrides.

        Distributed-memory parallel DMP solutions use the default FSPLIT value and force NOELDB = 1 for all
        results files. You cannot change the FSPLIT and NOELDB options for a DMP solution.
        """
        command = f"/CONFIG,{lab},{val}"
        return self.run(command, **kwargs)

    def cwd(self, dirpath: str = "", **kwargs):
        r"""Changes the current working directory.

        Mechanical APDL Command: `/CWD <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CWD_sl.html>`_

        Parameters
        ----------
        dirpath : str
            The full path name of the new working directory.

        Notes
        -----

        .. _s-CWD_notes:

        After issuing the /CWD command, all new files opened with no default directory specified (via the
        :ref:`file`, :ref:`copy`, or :ref:`resume` commands, for example) default to the new ``DIRPATH``
        directory.

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
                'The CWD command does not accept paths that contain singular quotes "\'".'
            )
        return self.run(f"/CWD,'{dirpath}'", **kwargs)

    def filname(self, fname: str = "", key: str = "", **kwargs):
        r"""Changes the Jobname for the analysis.

        Mechanical APDL Command: `/FILNAME <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_FILNAME.html>`_

        Parameters
        ----------
        fname : str
            Name (32 characters maximum) to be used as the :file:`Jobname`. Defaults to the initial
            :file:`Jobname` as specified on the Mechanical APDL execution command, or to :file:`file` if
            none specified.

        key : str
            Specify whether to use the existing log, error, lock, page, and output files ( :file:`.LOG`, :file:`.ERR`, :file:`.LOCK`, :file:`.PAGE` and :file:`.OUT` ) or
            start new files.

            * ``0, OFF`` - Continue using current log, error, lock, page, and output files.

            * ``1, ON`` - Start new log, error, lock, page, and output files (old log and error files are closed
              and saved, but old lock, page, and output files are deleted). Existing log and error files are
              appended.

        Notes
        -----

        .. _s-FILNAME_notes:

        All subsequently created files will be named with this :file:`Jobname` if ``Key`` = 0. Use ``Key`` =
        1 to start new log, error, lock, page, and output files. The previous :file:`Jobname` is typically
        defined on the Mechanical APDL program execution line. (See the `Operations Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_ope/Hlp_G_OPE8.html>`_.

        This command is useful when different groups of files created throughout the run are to have
        different names. For example, the command may be used before each substructure pass to avoid
        overwriting files or having to rename each file individually.

        This command is valid only at the Begin level.
        """
        command = f"/FILNAME,{fname},{key}"
        return self.run(command, **kwargs)

    def input(
        self,
        fname: str = "",
        ext: str = "",
        dir_: str = "",
        line: str = "",
        log: int | str = "",
        **kwargs,
    ):
        r"""Switches the input file for the commands that follow.

        Mechanical APDL Command: `/INPUT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_INPUT.html>`_

        Parameters
        ----------
        fname : str
            File name and directory path (248 characters maximum, including the characters needed for the
            directory path). An unspecified directory path defaults to the working directory; in this case,
            you can use all 248 characters for the file name. The file name defaults to the current
            :file:`Jobname` if ``Ext`` is specified.

        ext : str
            Filename extension (eight-character maximum).

        dir_ : str
            Directory path (64 characters maximum). Defaults to current directory.

        line : str
            A value indicating either a line number in the file or a user-defined label in the file from which
            to begin reading the input file.

            * ``(blank), 0, or 1`` - Begins reading from the top of the file (default).

            * ``LINE_NUMBER`` - Begins reading from the specified line number in the file.

            * ``:, label`` - Begins reading from the first line beginning with the matching user-defined label :
              ``label`` (beginning with a colon (:), 8 characters maximum).

        log : int or str
            Indicates whether secondary input from this command should be recorded in the command log ( :file:`File.LOG` ) and the database log:

            * ``0`` - Record only the :ref:`input` command on the log (default).

            * ``1`` - Record commands in the specified secondary file as they are executed.

        Notes
        -----

        .. _s-INPUT_notes:

        Switches the input file for the next commands. Commands are read from this file until an end-of-file
        or another file switching directive is read. An end-of-file occurs after the last record of the file
        or when a ``/EOF`` command is read. An automatic switch back one level (to the previous file) occurs
        when an end-of-file is encountered. Twenty levels of nested file switching are allowed. Note that
        files including ``\*DO``, :ref:`use`, :ref:`ulib`, and the "Unknown Command" Macro have less nesting
        available because each of these operations also uses a level of file switching. For an interactive
        run, a :ref:`input`,TERM switches to the terminal for the next input. A ``/EOF`` read from the
        terminal then switches back to the previous file. A :ref:`input` (with a blank second field)
        switches back to the primary input file.

        Setting ``LOG`` = 1 on :ref:`input` causes all commands read from the specified file to be recorded
        in the command log ( :file:`File.LOG` ) and the internal database command log ( :ref:`lgwrite` ).
        This option is recommended if the log file will be used later. The ``LOG`` = 1 option is only valid
        when the :ref:`input` occurs in the primary input file. Using ``LOG`` = 1 on a nested :ref:`input`
        or on a :ref:`input` within a do-loop will have no effect (that is, commands in the secondary input
        file are not written to the command log).

        The ``Dir`` option is optional as the directory path can be included directly in ``Fname``.

        This command is valid in any processor.
        """
        command = f"/INPUT,{fname},{ext},{dir_},{line},{log}"
        return self.run(command, **kwargs)

    def keyw(self, **kwargs):
        r"""Sets a keyword used by the GUI for context filtering (GUI).

        Mechanical APDL Command: `KEYW <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_KEYW.html>`_

        Notes
        -----

        .. _KEYW_notes:

        This is a program-generated command and is not intended for your use. It is included here in the
        documentation because it might appear in the log file ( :file:`Jobname.log` ). When using log files,
        or portions of log files, as input, any included :ref:`keyw` commands may be left as is, or removed,
        without consequence.
        """
        command = "KEYW"
        return self.run(command, **kwargs)

    def memm(self, lab: str = "", kywrd: str = "", **kwargs):
        r"""Allows the current session to keep allocated memory

        Mechanical APDL Command: `MEMM <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MEMM.html>`_

        Parameters
        ----------
        lab : str
            When ``Lab`` = KEEP, the memory manager's ability to acquire and keep memory is controlled by
            ``Kywrd``

        kywrd : str
            Turns the memory "keep" mode on or off

            * ``ON`` - Keep any memory allocated during the analysis.

            * ``OFF`` - Use memory dynamically and free it up to other users after use (default).

        Notes
        -----

        .. _MEMM_notes:

        You can use the :ref:`memm` command to ensure that memory intensive operations will always have the
        same memory available when the operations occur intermittently. Normally, if a large amount of
        memory is allocated for a specific operation, it will be returned to the system once the operation
        is finished. This option always maintains the highest level used during the analysis until the
        analysis is finished.

        The :ref:`memm` command does not affect the value you specify with the -m switch. When you allocate
        memory with the -m switch, that amount will always be available. However, if dynamic memory
        allocation in excess of the -m value occurs, you can use the :ref:`memm` command to ensure that
        amount is retained until the end of your analysis.
        """
        command = f"MEMM,{lab},{kywrd}"
        return self.run(command, **kwargs)

    def menu(self, key: str = "", **kwargs):
        r"""Activates the Graphical User Interface (GUI).

        Mechanical APDL Command: `/MENU <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MENU.html>`_

        Parameters
        ----------
        key : str
            Activation key:

            * ``ON`` - Activates the menu system (device dependent).

        Notes
        -----

        .. _s-MENU_notes:

        Activates the Graphical User Interface (GUI).

        .. warning::

            if you include the /MENU,ON command in your start.ans, it should be the lastcommand in the file.
            Any commands after /MENU,ON may be ignored. (It is not necessary to include the /SHOW and
            /MENU,ON commands in start.ansif you will be using the launcher to enter the Mechanical APDL program.)

        This command is valid in any processor.
        """
        command = f"/MENU,{key}"
        return self.run(command, **kwargs)

    def mstart(self, label: str = "", key: str = "", **kwargs):
        r"""Controls the initial GUI components.

        Mechanical APDL Command: `/MSTART <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MSTART.html>`_

        Parameters
        ----------
        label : str
            Label identifying the GUI component:

            * ``ZOOM`` - `Pan,Zoom, Rotate
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_wid/Hlp_UI_PanZoom.html#wpanzoomk>`_
              dialog box, off by default.

            * ``WORK`` - `OffsetWorking Plane
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_wid/Hlp_UI_WP_Offset.html#wwpoffsetdynamic>`_
              dialog box, off by default.

            * ``WPSET`` - `WorkingPlane Settings
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_wid/Hlp_UI_WP_Set.html#wwpsetgrid>`_
              dialog box, off by default.

            * ``ABBR`` - `EditToolbar/Abbreviations
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_wid/Hlp_UI_Toolbar.html#edittoolbarselect>`_
              dialog box, off by default.

            * ``PARM`` - `ScalarParameters
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_wid/Hlp_UI_Scal_Parm.html#wscalparmselect>`_
              dialog box, off by default.

            * ``SELE`` - Select Entities dialog box, off by default.

            * ``ANNO`` - Annotation dialog box, off by default.

            * ``HARD`` - Hard Copy dialog box, off by default.

            * ``UTIL`` - Activates the pre-6.1 (UIDL) GUI (off by default).

        key : str
            Switch value:

            * ``OFF or 0`` - Component does not appear when GUI is initialized.

            * ``ON or 1`` - Component appears when GUI is initialized.

        Notes
        -----

        .. _s-MSTART_notes:

        Controls which components appear when the Graphical User Interface (GUI) is initially brought up.
        This command is valid only before the GUI is brought up ( :ref:`menu`,ON) and is intended to be used
        in the :file:`start.ans` file. It only affects how the GUI is initialized ; you can always bring up
        or close any component once you are in the GUI.

        This command is valid only at the Begin Level.
        """
        command = f"/MSTART,{label},{key}"
        return self.run(command, **kwargs)

    def nerr(
        self,
        nmerr: str = "",
        nmabt: str = "",
        ifkey: str = "",
        num: int | str = "",
        **kwargs,
    ):
        r"""Limits the number of warning and error messages displayed.

        Mechanical APDL Command: `/NERR <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_NERR.html>`_

        Parameters
        ----------
        nmerr : str
            Maximum number of warning and error messages displayed per command. Defaults to 5 for
            interactive runs with the GUI turned on, 20 for interactive runs with the GUI turned off, 200
            for batch runs. If ``NMERR`` is negative, the absolute value of ``NMERR`` is used as the maximum
            number of warning and error messages written to the error file ( :file:`Jobname.ERR` ) per
            command, as well as the maximum number of messages displayed per command.

        nmabt : str
            Maximum number of warning and error messages allowed per command before run aborts (must be
            greater than zero). Maximum value is 99,999,999. Defaults to 10,000.

        ifkey : str
            Specifies whether or not to abort if an error occurs during a :ref:`input` operation:

            * ``0, or OFF`` - Do not abort. This option is the default.

            * ``1, or ON`` - Abort.

        num : int or str
            The number of invalid command warnings before a stop warning will be issued:

            * ``0`` - Disables the stop warning/error function.

            * ``n`` - An integer value representing the number of warnings that will be encountered before
              prompting the user to stop (default = 5). The first error encountered will ALWAYS result in a
              prompt.

              Invalid command warnings and error tracking are mutually exclusive.

        Notes
        -----

        .. _s-NERR_notes:

        Limits the number of warning and error messages displayed for any one command in an interactive run.

        Warning and error messages continue to be written to :file:`Jobname.ERR` regardless of these limits,
        unless ``NMERR`` is negative. There is no way to totally suppress writing of warning and error
        messages to the error file.

        Issue this command with ``NUM`` = ``n`` to specify the number of invalid command warnings to be
        encountered before the user is prompted to stop. You can then continue or abort the run. If you
        choose to abort the run, the log file can be saved so that any of the processing up to that point
        can be appended to an input that rectifies the condition. A batch run always aborts on the first
        error. Issue :ref:`nerr`,STAT to list current settings.

        Issue :ref:`nerr`,DEFA to reset values to initial defaults.

        An ``IFKEY`` value of 1 or ON causes Mechanical APDL to terminate immediately upon encountering an
        error during a file :ref:`input` operation. However, use of this option may cause the following
        conditions to occur:

        * The :ref:`input` command may abort if issued for a log file ( :file:`jobname.log` ).

        * Some macros may terminate.

        * A CAD connection may fail after reading only a small portion of a CAD model.

        The command is valid in any processor.
        """
        command = f"/NERR,{nmerr},{nmabt},,{ifkey},{num}"
        return self.run(command, **kwargs)

    def output(self, fname: str = "", ext: str = "", loc: str = "", **kwargs):
        r"""Redirects text output to a file or to the screen.

        Mechanical APDL Command: `/OUTPUT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_OUTPUT.html>`_

        Parameters
        ----------
        fname : str
            Filename and directory path (248 character maximum, including directory) to which text output
            will be redirected (defaults to :file:`Jobname` if ``Ext`` is specified). For interactive runs,
            ``Fname`` = TERM (or blank) redirects output to the screen. For batch runs, ``Fname`` = blank
            (with all remaining command arguments blank) redirects output to the default system output file.

        ext : str
            Filename extension (eight-character maximum).

        loc : str
            Location within a file to which output will be written:

            * ``(blank)`` - Output is written starting at the top of the file (default).

            * ``APPEND`` - Output is appended to the existing file.

        Notes
        -----

        .. _s-OUTPUT_notes:

        Text output includes responses to every command and GUI function, notes, warnings, errors, and other
        informational messages. Upon execution of :ref:`output`, ``Fname``, ``Ext``, ``...``, all subsequent
        text output is redirected to the file :file:`Fname.Ext`. To redirect output back to the default
        location, issue :ref:`output` (no arguments).

        When using the GUI, output from list operations ( :ref:`nlist`, :ref:`dlist`, etc.) is always sent
        to a list window regardless of the :ref:`output` setting. The output can then be saved on a file or
        copied to the :ref:`output` location using the File menu in the list window.

        This command is valid in any processor.
        """
        command = f"/OUTPUT,{fname},{ext},,{loc}"
        return self.run(command, **kwargs)

    def pause(self, **kwargs):
        r"""Temporarily releases the current product license.

        Mechanical APDL Command: `PAUSE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PAUSE.html>`_

        Notes
        -----

        .. _PAUSE_notes:

        The :ref:`pause` command temporarily releases (or pauses) the current product license so that
        another application can use it.

        This application consumes a license as soon as you launch it, and retains that license until it is
        finished. If you launch the product interactively, the license is retained until you either close
        the application or issue a :ref:`pause` command via the command line.

        No other operation (other than :ref:`save` or :ref:`slashexit` ) is possible in the current
        application  while use of the product license is paused.

        When the second application has finished and releases the license, issue an :ref:`unpause` command
        via the command line to restore use of the license to the current application.

        For more information, see the `Ansys Licensing Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/licensing/Hlp_IN_TBSHOOT.html>`_.
        """
        command = "PAUSE"
        return self.run(command, **kwargs)

    def slashexit(self, slab: str = "", fname: str = "", ext: str = "", **kwargs):
        r"""Stops the run and returns control to the system.

        Mechanical APDL Command: `/EXIT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_EXIT.html>`_

        Parameters
        ----------
        slab : str
            Mode for saving the database:

            * ``MODEL`` - Save the model data (solid model, finite element model, loadings, etc.) only
              (default).

            * ``SOLU`` - Save the model data and the solution data (nodal and element results).

            * ``ALL`` - Save the model data, solution data and post data (element tables, path results, etc.)

            * ``NOSAVE`` - Do not save any data on :file:`File.DB` (an existing DB file will not be
              overwritten).

        fname : str
            File name and directory path (248 characters maximum, including the characters needed for the
            directory path). An unspecified directory path defaults to the working directory; in this case,
            you can use all 248 characters for the file name. The file name, defaults to :file:`Jobname`.

        ext : str
            Filename extension (eight-character maximum). The extension defaults to DB if ``Fname`` is
            blank.

        Notes
        -----

        .. _s-EXIT_notes:

        The current database information may be written on :file:`File.DB` or a named file. If
        :file:`File.DB` already exists, a backup file ( :file:`File.DBB` ) will also be written whenever a
        new :file:`File.DB` is written.

        This command is valid in any processor. Issuing this command at any point will exit the program.
        """
        command = f"/EXIT,{slab},{fname},{ext}"
        return self.run(command, **kwargs)

    def slashstatus(self, lab: str = "", **kwargs):
        r"""Lists the status of items for the run.

        Mechanical APDL Command: `/STATUS <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_STATUS.html>`_

        Parameters
        ----------
        lab : str
            Items to list status for:

            * ``ALL`` - List all below (default).

            * ``TITLE`` - List only titles, :file:`Jobname`, and revision number.

            * ``UNITS`` - List only units.

            * ``MEM`` - List only memory data statistics.

            * ``DB`` - List only database statistics

            * ``CONFIG`` - List only configuration parameters.

            * ``GLOBAL`` - Provides a global status summary.

            * ``SOLU`` - Provides a solution status summary.

            * ``PROD`` - Provides a product summary.

        Notes
        -----

        .. _s-STATUS_notes:

        Displays various items active for the run (such as the Mechanical APDL revision number,
        :file:`Jobname`,
        titles, units, configuration parameters, database statistics, etc.).

        This command is valid in any processor.
        """
        command = f"/STATUS,{lab}"
        return self.run(command, **kwargs)

    def syp(
        self,
        string: str = "",
        arg1: str = "",
        arg2: str = "",
        arg3: str = "",
        arg4: str = "",
        arg5: str = "",
        arg6: str = "",
        arg7: str = "",
        arg8: str = "",
        **kwargs,
    ):
        r"""Passes a command string and arguments to the operating system.

        Mechanical APDL Command: `/SYP <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SYP.html>`_

        Parameters
        ----------
        string : str
            Command string (cannot include commas). See also the :ref:`sys` command.

        arg1 : str
            Arguments to be appended to the command string, separated by blanks, commas, or other delimiter
            characters (see the `Operations Guide
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_ope/Hlp_G_OPE8.html>`_). The
            arguments may be numbers, parameters, or parametric expressions.

        arg2 : str
            Arguments to be appended to the command string, separated by blanks, commas, or other delimiter
            characters (see the `Operations Guide
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_ope/Hlp_G_OPE8.html>`_). The
            arguments may be numbers, parameters, or parametric expressions.

        arg3 : str
            Arguments to be appended to the command string, separated by blanks, commas, or other delimiter
            characters (see the `Operations Guide
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_ope/Hlp_G_OPE8.html>`_). The
            arguments may be numbers, parameters, or parametric expressions.

        arg4 : str
            Arguments to be appended to the command string, separated by blanks, commas, or other delimiter
            characters (see the `Operations Guide
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_ope/Hlp_G_OPE8.html>`_). The
            arguments may be numbers, parameters, or parametric expressions.

        arg5 : str
            Arguments to be appended to the command string, separated by blanks, commas, or other delimiter
            characters (see the `Operations Guide
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_ope/Hlp_G_OPE8.html>`_). The
            arguments may be numbers, parameters, or parametric expressions.

        arg6 : str
            Arguments to be appended to the command string, separated by blanks, commas, or other delimiter
            characters (see the `Operations Guide
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_ope/Hlp_G_OPE8.html>`_). The
            arguments may be numbers, parameters, or parametric expressions.

        arg7 : str
            Arguments to be appended to the command string, separated by blanks, commas, or other delimiter
            characters (see the `Operations Guide
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_ope/Hlp_G_OPE8.html>`_). The
            arguments may be numbers, parameters, or parametric expressions.

        arg8 : str
            Arguments to be appended to the command string, separated by blanks, commas, or other delimiter
            characters (see the `Operations Guide
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_ope/Hlp_G_OPE8.html>`_). The
            arguments may be numbers, parameters, or parametric expressions.

        Notes
        -----

        .. _s-SYP_notes:

        Passes a command string to the operating system for execution, along with arguments to be appended
        to the command string. See the `Operations Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_ope/Hlp_G_OPE8.html>`_ for details.
        Mechanical APDL may not be aware of your specific user
        environment. For example, on Linux this command may not recognize aliases, depending on the hardware
        platform and user environment.

        This command is valid in any processor.
        """
        command = (
            f"/SYP,{string},{arg1},{arg2},{arg3},{arg4},{arg5},{arg6},{arg7},{arg8}"
        )
        return self.run(command, **kwargs)

    def sys(self, string: str = "", **kwargs):
        r"""Passes a command string to the operating system.

        Mechanical APDL Command: `/SYS <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SYS.html>`_

        Parameters
        ----------
        string : str
            Command string, up to 639 characters (including blanks, commas, etc.). The specified string is
            passed verbatim to the operating system, that is, no parameter substitution is performed.

        Notes
        -----

        .. _s-SYS_notes:

        Passes a command string to the operating system for execution (see the `Operations Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_ope/Hlp_G_OPE8.html>`_). Typical strings
        are system commands such as list, copy, rename, etc. Control returns to Mechanical APDL after the
        system
        procedure is completed. Mechanical APDL may not be aware of your specific user environment. For
        example, on
        Linux this command may not recognize aliases, depending on the hardware platform and user
        environment.

        This command is valid in any processor.
        """
        command = f"/SYS,{string}"
        return self.run(command, **kwargs)

    def ui(
        self,
        func: str = "",
        type_: str = "",
        format_: str = "",
        screen: str = "",
        color: str = "",
        krev: str = "",
        orient: str = "",
        compress: str = "",
        quality: str = "",
        **kwargs,
    ):
        r"""Activates specified GUI dialog boxes.

        Mechanical APDL Command: `/UI <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_UI.html>`_

        Parameters
        ----------
        func : str
            Label identifying the dialog box to be activated:

            * ``HELP`` - Activates the online help system.

            * ``VIEW`` - Activates the Pan, Zoom, Rotate dialog box

            * ``WPSE`` - Activates the Working Plane Settings dialog box.

            * ``WPVI`` - Activates the Offset Working Plane dialog box.

            * ``RESULT`` - Activates the Query Picking Menu for reviewing results.

            * ``QUERY`` - Activates the Query Picked Entities (preprocess) dialog box.

            * ``COPY`` - Activates the Hard Copy dialog box.

            * ``ANNO`` - Activates the 2D Annotation dialog box.

            * ``AN3D`` - Activates the 3D Annotation dialog box.

            * ``SELECT`` - Activates the Select Entities dialog box.

            * ``NSEL`` - Activates a picking menu to select nodes.

            * ``ESEL`` - Activates a picking menu to select elements.

            * ``KSEL`` - Activates a picking menu to select keypoints.

            * ``LSEL`` - Activates a picking menu to select lines.

            * ``ASEL`` - Activates a picking menu to select areas.

            * ``VSEL`` - Activates a picking menu to select volumes.

            * ``REFRESH`` - Refreshes the graphics window (non-UI mode only).

            * ``COLL`` - Controls the collapse of the Mechanical APDL main menu when a :ref:`finish` command is issued.
              See Type below for a discussion of the arguments.

        type_ : str
            Label identifying the type of select operation. Valid only for the following ``Func`` labels; NSEL, ESEL, KSEL, LSEL, ASEL, and VSEL:

            * ``S`` - Select a new set.

            * ``R`` - Reselect a set from the current set.

            * ``A`` - Additionally select a set and extend the current set.

            * ``U`` - Unselect a set from the current set.

            Label identifying the type of results data to be queried. Valid only for ``Func`` = RESULT:

            * ``NODE`` - Nodal solution data (h-elements only).

            * ``ELEMENT`` - Element solution data.

            .. _ui_coll_label:

             Label specifying the behavior of the Mechanical APDL main menu after a :ref:`finish` command is issued. User interaction with the main menu is unaffected. Valid only for ``Func`` = COLL:

            * ``YES, 1 or blank`` - Allows the Main Menu to collapse after :ref:`finish` command.

            * ``NO or 0`` - Prevents Main Menu collapse after :ref:`finish` command.

        format_ : str

            * ``TIFF`` - Tagged Image File Format.

            * ``BMP`` - (PC only) Bitmap (Windows) file format.

            * ``WMF`` - (PC only) Windows Metafile format.

            * ``EMF`` - (PC only) Enhanced Metafile format.

            * ``JPEG`` - JPEG (Joint Photographic Experts Group) file format.

        screen : str

            * ``FULL`` - Saves the entire screen in the specified format.

            * ``GRAPH`` - Saves only the Mechanical APDL graphic window.

        color : str

            * ``MONO`` - A two color (black and white) file is saved.

            * ``GRAY`` - The specified file format is saved in gray scale.

            * ``COLOR`` - The file is saved at the specified color depth.

        krev : str

            * ``NORM`` - Saves file as shown on the screen.

            * ``REVERSE`` - Saves file with the background color reversed.

        orient : str

            * ``LANDSCAPE`` - Saves file in landscape mode.

            * ``PORTRAIT`` - Saves file in portrait mode.

        compress : str

            * ``YES`` - Compresses TIFF files and EPS files with TIFF preview (default).

            * ``NO`` - Saves files with no compression.

        quality : str

            * ``1,2,,,100`` - JPEG quality index, with 100 being the maximum quality level.

        Notes
        -----

        .. warning::

           This function contains specificities regarding the argument definitions.
           Please refer to the `command documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_UI.html>`_
           for further explanations.

        .. _s-UI_notes:

        Allows you to activate specified GUI dialog boxes directly in either GUI or non-GUI mode.

        The :ref:`ui` command itself is valid in any processor, however certain dialog boxes are accessible
        only in a particular processor (for example, :ref:`ui`,RESULT,... is valid only in the General
        Postprocessor).

        Mechanical APDL JPEG software is based in part on the work of the Independent JPEG Group, Copyright
        1998,
        Thomas G. Lane.
        """
        command = f"/UI,{func},{type_},{format_},{screen},{color},{krev},{orient},{compress},{quality}"
        return self.run(command, **kwargs)

    def uis(self, label: str = "", value: int | str = "", **kwargs):
        r"""Controls the GUI behavior.

        Mechanical APDL Command: `/UIS <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_UIS.html>`_

        Parameters
        ----------
        label : str
            Behavior control key:

            * ``BORD`` - Controls the functionality of the mouse buttons for dynamic viewing mode only. When
              ``Label`` = BORD, the three values that follow control the functionality of the LEFT, MIDDLE and
              RIGHT buttons, respectively (see below).

            * ``MSGPOP`` - Controls which messages from the Mechanical APDL error-message subroutine are displayed in a
              message dialog box.

            * ``REPLOT`` - Controls whether or not an automatic replot occurs after functions affecting the
              model are executed.

            * ``ABORT`` - Controls whether or not the program displays dialog boxes to show the status of an
              operation in progress and to cancel that operation.

            * ``DYNA`` - Controls whether the dynamic mode preview is a bounding box or the edge outline of the
              model. This label only applies to 2D display devices (that is, :ref:`show`,XII or
              :ref:`show`,WIN32). This "model edge outline" mode is only supported in PowerGraphics (
              :ref:`graphics`,POWER) and is intended for element, line, results, area, or volume displays.

            * ``PICK`` - Controls how graphical entities are highlighted from within the the Select menu.

            * ``POWER`` - Controls whether or not PowerGraphics is active when the GUI is initiated. Mechanical APDL
              default status is PowerGraphics "ON"; this command is used (placed in the :file:`start.ans` file)
              when full graphics is desired on start up.

            * ``DPRO`` - Controls whether or not the input window displays a dynamic prompt. The dynamic prompt
              shows the correct command syntax for the command, as you are entering it.

            * ``UNDO`` - Controls whether or not the session editor includes nonessential commands or comments
              in the file it creates. You can use this option to include comments and other materials in the
              session editor file.

            * ``LEGE`` - Controls whether or not the multi-legend is activated when you start the GUI. The
              multi-legend enables you to specify the location of your legend items in each of the five graphics
              windows. You can place this option in your :file:`start.ans` file and have the GUI start with the
              legend items in a pre-specified location.

            * ``PBAK`` - Controls whether or not the background shading is activated when you start the GUI. You
              can place this option in your :file:`start.ans` file.

            * ``ZPIC`` - Controls the sorting order for entities that are coincident (directly in front of or
              behind each other) to a picked spot on your model. When you pick a spot on your model that could
              indicate two or more entities, a message warns you of this condition, and a list of the coincident
              entities can be generated. The ``VALUE`` term (below) will determine the sort order.

            * ``HPOP`` - Controls the prioritization of your GUI windows when the contents are ported to a plot
              or print file ( :ref:`ui`,COPY,SAVE). OpenGL (3D) graphics devices require that the Mechanical APDL
              graphics window contents be set in front of all overlying windows in order to port them to a printer
              or a file. This operation can sometimes conflict with :ref:`noerase` settings. See the ``VALUE``
              term (below) to determine the available control options.

        value : int or str
            Values controlling behavior if ``Label`` = BORD:

            (These values control the operation according to syntax : :ref:`uis`,BORD, LEFT, MIDDLE, RIGHT )

            * ``1`` - PAN, controls dynamic translations.

            * ``2`` - ZOOM, controls zoom, and dynamic rotation about the view vector.

            * ``3`` - ROTATE, controls dynamic rotation about the screen X and Y axes.

              You can designate any value for any button, or designate the same value for all three buttons. If no
              value is specified, default is LEFT = PAN, MIDDLE = ZOOM and RIGHT = ROTATE.

            Values controlling behavior if ``Label`` = MSGPOP:

            * ``0`` - All messages displayed.

            * ``1`` - Only notes, warnings, and errors displayed.

            * ``2`` - Only warnings and errors displayed (default).

            * ``3`` - Only errors displayed.

            Values controlling behavior if ``Label`` = REPLOT:

            * ``0`` - No automatic replot.

            * ``1`` - Automatic replot (default).

            Values controlling behavior if ``Label`` = ABORT:

            * ``ON`` - Display status and cancellation dialog boxes (default).

            * ``OFF`` - Do not display status and cancellation dialog boxes.

            * ``1`` - Same as ON.

            * ``0`` - Same as OFF.

            Values controlling behavior if ``Label`` = DYNA:

            * ``0`` - Use model edge outline when possible (default).

            * ``1`` - Use bounding box preview.

            Values controlling behavior if ``Label`` = PICK:

            * ``0`` - Picked keypoints and nodes are enclosed by a square. Picked lines are overlaid by a
              thicker line. Picked areas, volumes, and elements (non-point/non-line) are redrawn with highlighting
              colors. However, if the pick is a box, circle, or polygon pick, the highlighting for all entitles
              consists only of a square placed around the entity's centroid.

            * ``1`` - Picked entities are not highlighted.

            * ``2`` - 5.1 highlighting (that is, no XOR).

            * ``3`` - Picked entities are highlighted as in ``VALUE`` = 0, except that, for a box, circle, or
              polygon pick, the picked areas, volumes, and elements (non-point/non-line) are redrawn with
              highlighting colors. This technique is slower than the ``VALUE`` = 0 technique.

            Values controlling behavior if ``Label`` = POWER:

            * ``0`` - Start GUI in Full Graphics mode.

            * ``1`` - Start GUI in PowerGraphics mode (default).

            Values controlling behavior if ``Label`` = DPRO:

            * ``0 or OFF`` - Do not display the dynamic prompt.

            * ``1 or ON`` - Display the dynamic prompt (default).

            Values controlling behavior if ``Label`` = UNDO:

            * ``0 or None`` - Do not suppress any commands (default).

            * ``1 or Comment`` - Write the nonessential commands to the session editor file as comments (with a
              ! at the beginning).

            * ``2 or Remove`` - Do not write nonessential commands or comments.

            Values controlling behavior if ``Label`` = LEGE:

            * ``0 or OFF`` - Start GUI with the enhanced legend off (default).

            * ``1 or ON`` - Start GUI with the enhanced legend capability activated.

            Values controlling behavior if ``Label`` = PBAK:

            * ``0 or OFF`` - Start the GUI with the no background shading (default).

            * ``1 or ON`` - Start the GUI with background shading activated.

            Values controlling behavior if ``Label`` = HPOP:

            * ``0 or OFF`` - No rewrite operations are performed to compensate for items that obscure or overlay
              the graphics window (default).

            * ``1 or ON`` - The Graphics screen contents are replotted to ensure that they are situated in front
              of all other windows. If :ref:`noerase` is detected, this operation is suppressed.

        Notes
        -----

        .. _s-UIS_notes:

        Controls certain features of the Graphical User Interface (GUI), including whether Mechanical APDL
        displays
        dialog boxes to show you the status of an operation (such as meshing or solution) in progress and to
        enable you to cancel that operation. Issue :ref:`uis`,STAT for current status. Issue :ref:`uis`,DEFA
        to reset default values for all labels. Issue :ref:`uis`, ``Label``,STAT and :ref:`uis`,
        ``Label``,DEFA for status and to reset a specific ``Label`` item.

        A :ref:`uis`,HPOP,1 command employs a fast redraw method which does not allow entering the legend
        logic for a :ref:`plopts`,INFO,1 or :ref:`plopts`,INFO,2 command. However, the legend is redrawn for
        :ref:`plopts`,INFO,3 because that command also allows a fast redraw.

        This command is valid in any processor.
        """
        command = f"/UIS,{label},{value}"
        return self.run(command, **kwargs)

    def unpause(self, **kwargs):
        r"""Restores use of a temporarily released product license.

        Mechanical APDL Command: `UNPAUSE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_UNPAUSE.html>`_

        Notes
        -----

        .. _UNPAUSE_notes:

        The :ref:`unpause` command restores use of a temporarily released (paused) product license. The
        command is valid only after a previously issued :ref:`pause` command.

        When use of the product license is paused via the :ref:`pause` command, no other operation (other
        than :ref:`save` or :ref:`slashexit` ) is possible until you issue the :ref:`unpause` command.

        For more information, see the documentation for the :ref:`pause` command and the `Ansys Licensing
        Guide <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/licensing/Hlp_IN_TBSHOOT.html>`_.
        """
        command = "UNPAUSE"
        return self.run(command, **kwargs)
