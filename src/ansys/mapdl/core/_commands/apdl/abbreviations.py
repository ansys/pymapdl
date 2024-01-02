class Abbreviations:
    def abbr(self, abbr="", string="", **kwargs):
        """Defines an abbreviation.

        APDL Command: ``*ABBR``

        Parameters
        ----------
        abbr
            The abbreviation (up to 8 alphanumeric characters) used to
            represent the string String.  If Abbr is the same as an existing
            ANSYS command, the abbreviation overrides.  Avoid using an Abbr
            which is the same as an ANSYS command.

        string
            String of characters (60 maximum) represented by Abbr.
            Cannot include a $ or any of the commands ``C***``, /COM,
            /GOPR, /NOPR, /QUIT, /UI, or ``*END``.

            Use the ``*IF`` groups may not be abbreviated. If String
            is blank, the abbreviation is deleted. To abbreviate
            multiple commands, create an "unknown command" macro or
            define String to execute a macro file [``*USE``]
            containing the desired commands.

        Notes
        -----
        Once the abbreviation Abbr is defined, you can issue it at the
        beginning of a command line and follow it with a blank (or with a comma
        and appended data), and the program will substitute the string  String
        for Abbr as the line is executed. Up to 100 abbreviations may exist at
        any time and are available throughout the program. Abbreviations may be
        redefined or deleted at any time.

        Use ``*STATUS`` to display the current list of abbreviations. For
        abbreviations repeated with ``*REPEAT``, substitution occurs before the
        repeat increments are applied. There are a number of abbreviations that
        are predefined by the program (these can be deleted by using the blank
        String option described above). Note that String will be written to the
        File.LOG.

        This command is valid in any processor.
        """
        command = f"*ABBR,{abbr},{string}"
        return self.run(command, **kwargs)

    def abbres(self, lab="", fname="", ext="", **kwargs):
        """Reads abbreviations from a coded file.

        APDL Command: ABBRES

        Parameters
        ----------
        lab
            Label that specifies the read operation:

            Replace current abbreviation set with these abbreviations (default). - Extend current abbreviation set with these abbreviations, replacing any of the
                              same name that already exist.

        fname
            File name and directory path (248 characters maximum, including the
            characters needed for the directory path).  An unspecified
            directory path defaults to the working directory; in this case, you
            can use all 248 characters for the file name.

        ext
            Filename extension (eight-character maximum).

        Notes
        -----
        The abbreviation file may have been written with the ABBSAV command. Do
        not issue ABBRES,NEW while inside an executing abbreviation. Doing so
        will cause all data for the executing abbreviation to be deleted.

        This command is valid in any processor.
        """
        command = f"ABBRES,{lab},{fname},{ext}"
        return self.run(command, **kwargs)

    def abbsav(self, lab="", fname="", ext="", **kwargs):
        """Writes the current abbreviation set to a coded file.

        APDL Command: ABBSAV

        Parameters
        ----------
        lab
            Label that specifies the write operation.

            ALL - Write all abbreviations (default).

        fname
            File name and directory path (248 characters maximum,
            including the characters needed for the directory path).
            An unspecified directory path defaults to the working
            directory; in this case, you can use all 248 characters
            for the file name.

            The file name defaults to Jobname.

        ext
            Filename extension (eight-character maximum).  The
            extension defaults to ABBR if Fname is blank.

        Notes
        -----
        Existing abbreviations on this file, if any, will be overwritten.  The
        abbreviation file may be read with the ABBRES command.

        This command is valid in any processor.
        """
        command = f"ABBSAV,{lab},{fname},{ext}"
        return self.run(command, **kwargs)

    def ucmd(self, cmd="", srnum="", **kwargs):
        """Assigns a user-defined command name.

        APDL Command: /UCMD

        Parameters
        ----------
        cmd
            User-defined command name.  Only the first four characters are
            significant.  Must not conflict with any ANSYS command name or any
            user "unknown command" macro name.

        srnum
            User subroutine number (1 to 10) programmed for this command.  For
            example, the command /UCMD,MYCMD,3 will execute subroutine USER03
            whenever the command MYCMD is entered.  Use a blank command name to
            disassociate SRNUM from its command.  For example, /UCMD,,3 removes
            MYCMD as a command.

        Notes
        -----
        Assigns a user-defined command name to a user-programmable (system-
        dependent) subroutine.  This feature allows user-defined commands to be
        programmed into the ANSYS program.  Once programmed, this command can
        be input to the program like other commands, and can also be included
        in the ANSYS start-up file.  See ``*ULIB`` for another way of defining user
        commands.

        Up to 10 subroutines are available for user-defined commands (USER01 to
        USER10).  Users must have system permission, system access, and
        knowledge to write, compile, and link the appropriate subprocessors
        into the ANSYS program at the site where it is to be run.  All routines
        should be written in FORTRAN. For more information on FORTRAN compilers
        please refer to either the ANSYS, Inc. Windows Installation Guide or
        the ANSYS, Inc. Linux Installation Guide for details specific to your
        platform or operating system. The USER01 routine is commented and
        should be listed from the distribution media (system dependent) for
        more details.  Issue /UCMD,STAT to list all user-defined command names.
        Since a user-programmed command is a nonstandard use of the program,
        the verification of any ANSYS run incorporating these commands is
        entirely up to the user.  In any contact with ANSYS customer support
        regarding the performance of a custom version of the ANSYS program, you
        should explicitly state that a user programmable feature has been used.
        See the Advanced Analysis Guide for a general description of user-
        programmable features and Guide to User-Programmable Features for a
        detailed description of these features.

        This command is valid only at the Begin Level.
        """
        command = f"/UCMD,{cmd},{srnum}"
        return self.run(command, **kwargs)
