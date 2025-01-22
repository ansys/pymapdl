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


class Abbreviations:

    def ucmd(self, cmd: str = "", srnum: str = "", **kwargs):
        r"""Assigns a user-defined command name.

        Mechanical APDL Command: `/UCMD <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_UCMD.html>`_

        Parameters
        ----------
        cmd : str
            User-defined command name. Only the first four characters are significant. Must not conflict
            with any Mechanical APDL command name or any user unknown-command macro name.

        srnum : str
            User subroutine number (1 to 10) programmed for this command. For example, the command :ref:`ucmd`,MYCMD,3 will execute subroutine USER03 whenever the command **MYCMD** is entered. Use a blank command name to disassociate ``SRNUM`` from its command. For example, :ref:`ucmd`,,3 removes **MYCMD** as a command.

        Notes
        -----
        Assigns a user-defined command name to a user-programmable (system-dependent) subroutine. This
        feature allows user-defined commands to be programmed into Mechanical APDL. Once programmed, this
        command
        can be input to the program like other commands, and can also be included in the Mechanical APDL
        start-up
        file.

        Up to 10 subroutines are available for user-defined commands (USER01 to USER10). You must have
        system permission, system access, and knowledge to write, compile, and link the appropriate
        subprocessors into Mechanical APDL at your site.

        All routines should be written in FORTRAN. For more information about FORTRAN compilers, refer to
        either the `Ansys, Inc. Windows Installation Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/installation/win_product_table.html>`_ or
        the Ansys, Inc. Linux Installation Guide  for details specific to your platform or operating
        system.

        The USER01 routine is commented and should be listed from the distribution media (system dependent)
        for more details.

        Issue :ref:`ucmd`,STAT to list all user-defined command names.

        Because a user-programmed command is a nonstandard use of the program, the verification of any
        Mechanical APDL run incorporating these commands is your responsibility. In any contact with
        Mechanical APDL
        customer support regarding the performance of a custom version of Mechanical APDL, explicitly state
        that a
        user-programmable feature has been used.

        See `User-Programmable Features (UPFs)
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_adv/Hlp_G_ADV7_1.html#aRzouq21ldm>`_
        `Guide to User-Programmable Features
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_prog/ansysprog_aero_fullycoupled.html>`_

        See :ref:`ulib` for another way of defining user commands.

        This command is valid only at the Begin Level.
        """
        command = f"/UCMD,{cmd},{srnum}"
        return self.run(command, **kwargs)

    def abbres(self, lab: str = "", fname: str = "", ext: str = "", **kwargs):
        r"""Reads abbreviations from a coded file.

        Mechanical APDL Command: `ABBRES <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ABBRES.html>`_

        Parameters
        ----------
        lab : str
            Label that specifies the read operation:

            * ``NEW`` - Replace current abbreviation set with these abbreviations (default).

            * ``CHANGE`` - Extend current abbreviation set with these abbreviations, replacing any of the same name that
              already exist.

        fname : str
            File name and directory path (248 characters maximum, including the characters needed for the
            directory path). An unspecified directory path defaults to the working directory; in this case,
            you can use all 248 characters for the file name. The file name defaults to :file:`Jobname`.

        ext : str
            Filename extension (eight-character maximum). The extension defaults to ABBR if ``Fname`` is
            blank.

        Notes
        -----
        The abbreviation file may have been written with the :ref:`abbsav` command. Do not issue
        :ref:`abbres`,NEW while inside an executing abbreviation. Doing so will cause all data for the
        executing abbreviation to be deleted.

        This command is valid in any processor.
        """
        command = f"ABBRES,{lab},{fname},{ext}"
        return self.run(command, **kwargs)

    def abbsav(self, lab: str = "", fname: str = "", ext: str = "", **kwargs):
        r"""Writes the current abbreviation set to a coded file.

        Mechanical APDL Command: `ABBSAV <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ABBSAV.html>`_

        Parameters
        ----------
        lab : str
            Label that specifies the write operation:

            * ``ALL`` - Write all abbreviations (default).

        fname : str
            File name and directory path (248 characters maximum, including the characters needed for the
            directory path). An unspecified directory path defaults to the working directory; in this case,
            you can use all 248 characters for the file name. The file name defaults to :file:`Jobname`.

        ext : str
            Filename extension (eight-character maximum). The extension defaults to ABBR if ``Fname`` is
            blank.

        Notes
        -----
        Existing abbreviations on this file, if any, will be overwritten. The abbreviation file may be read
        with the :ref:`abbres` command.

        This command is valid in any processor.
        """
        command = f"ABBSAV,{lab},{fname},{ext}"
        return self.run(command, **kwargs)

    def abbr(self, abbr: str = "", string: str = "", **kwargs):
        r"""Defines an abbreviation.

        Mechanical APDL Command: `\*ABBR <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ABBR.html>`_

        Parameters
        ----------
        abbr : str
            The abbreviation (up to 8 alphanumeric characters) used to represent the string ``String``. If
            ``Abbr`` is the same as an existing Mechanical APDL command, the abbreviation overrides. Avoid
            using an ``Abbr`` which is the same as an Mechanical APDL command.

        string : str
            String of characters (60 maximum) represented by ``Abbr``. Cannot include a $ or any of the
            commands ``C***``, :ref:`com`, :ref:`gopr`, :ref:`nopr`, :ref:`quit`, :ref:`ui`, or :ref:`end`.
            Parameter names and commands of the ``\*DO`` and Use the ``\*IF`` groups may not be abbreviated.
            If ``String`` is blank, the abbreviation is deleted. To abbreviate multiple commands, create an
            "unknown command" macro or define ``String`` to execute a macro file ( :ref:`use` ) containing
            the desired commands.

        Notes
        -----
        Once the abbreviation ``Abbr`` is defined, you can issue it at the beginning of a command line and
        follow it with a blank (or with a comma and appended data), and the program will substitute the
        string ``String`` for ``Abbr`` as the line is executed. Up to 100 abbreviations may exist at any
        time and are available throughout the program. Abbreviations may be redefined or deleted at any
        time.

        Use :ref:`starstatus` to display the current list of abbreviations. For abbreviations repeated with
        ``\*REPEAT``, substitution occurs before the repeat increments are applied. There are a number of
        abbreviations that are predefined by the program (these can be deleted by using the blank ``String``
        option described above). Note that ``String`` will be written to the :file:`File.LOG`.

        This command is valid in any processor.
        """
        command = f"*ABBR,{abbr},{string}"
        return self.run(command, **kwargs)
