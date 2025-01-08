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


class ProcessControls:

    def stargo(self, base: str = "", **kwargs):
        r"""Causes a specified line on the input file to be read next.

        Mechanical APDL Command: `\*GO <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_GO_st.html>`_

        Parameters
        ----------
        base : str
            "Go to" action:

              * ``:, label`` - A user-defined label (beginning with a colon (:), 8 characters maximum). The
              command reader will skip (and wrap to the beginning of the file, if necessary) to the first line
              that begins with the matching : ``label``.

              .. warning::     This label option may not be mixed with do-loop or if-then-else constructs.
              * ``STOP`` - This action will cause an exit from the Mechanical APDL program at this line.

        Notes
        -----
        Causes the next read to be from a specified line on the input file. Lines may be skipped or reread.
        The :ref:`stargo` command will not be executed unless it is part of a macro, user file (processed by
        :ref:`use` ), an alternate input file (processed by :ref:`input` ), or unless it is used in a batch-
        mode input stream. Jumping into, out of, or within a do-loop or an if-then-else construct to a :
        ``label`` line is not allowed.

        This command is valid in any processor.
        """
        command = f"*GO,{base}"
        return self.run(command, **kwargs)

    def wait(self, dtime: str = "", **kwargs):
        r"""Causes a delay before the reading of the next command.

        Mechanical APDL Command: `/WAIT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_WAIT.html>`_

        Parameters
        ----------
        dtime : str
            Time delay (in seconds). Maximum time delay is 59 seconds.

        Notes
        -----
        The command following the :ref:`wait` will not be processed until the specified wait time increment
        has elapsed. Useful when reading from a prepared input file to cause a pause, for example, after a
        display command so that the display can be reviewed for a period of time. Another "wait" feature is
        available via the ``\*ASK`` command.

        This command is valid in any processor.
        """
        command = f"/WAIT,{dtime}"
        return self.run(command, **kwargs)

    def cycle(self, **kwargs):
        r"""Bypasses commands within a do-loop.

        Mechanical APDL Command: `\*CYCLE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CYCLE.html>`_

        Notes
        -----
        Bypasses all commands between this command and the :ref:`enddo` command within a do-loop. The next
        loop (if applicable) is initiated. The cycle option may also be conditionally executed [Use the
        ``\*IF`` ]. The :ref:`cycle` command must appear on the same file as the :ref:`do` command.

        This command is valid in any processor.
        """
        command = f"*CYCLE"
        return self.run(command, **kwargs)

    def endif(self, **kwargs):
        r"""Ends an if-then-else.

        Mechanical APDL Command: `\*ENDIF <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ENDIF.html>`_

        Notes
        -----
        Required terminator for the if-then-else construct. See ``\*IF`` for details.

        If a batch input stream hits an end-of-file during a false ``\*IF`` condition, the analysis will not
        terminate normally. You will need to terminate it externally (use either the Linux "kill" function
        or the Windows task manager). The :ref:`endif` command must appear on the same file as the ``\*IF``
        command, and all six characters must be input.

        This command is valid in any processor.
        """
        command = f"*ENDIF"
        return self.run(command, **kwargs)

    def elseif(
        self,
        val1: str = "",
        oper1: str = "",
        val2: str = "",
        conj: str = "",
        val3: str = "",
        oper2: str = "",
        val4: str = "",
        **kwargs,
    ):
        r"""Separates an intermediate if-then-else block.

        Mechanical APDL Command: `\*ELSEIF <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ELSEIF.html>`_

        Parameters
        ----------
        val1 : str
            First numerical value (or parameter which evaluates to numerical value) in the conditional
            comparison operation. ``VAL1``, ``VAL2``, ``VAL3``, and ``VAL4`` can also be character
            strings (enclosed in quotes) or parameters for ``Oper`` = EQ and NE only.

        oper1 : str
            Operation label. A tolerance of 1.0E-10 is used for comparisons between real numbers:

              * ``EQ`` - Equal (for ``VAL1`` = ``VAL2`` ).

              * ``NE`` - Not equal (for ``VAL1`` ≠ ``VAL2`` ).

              * ``LT`` - Less than (for ``VAL1`` < ``VAL2`` ).

              * ``GT`` - Greater than (for ``VAL1`` > ``VAL2`` ).

              * ``LE`` - Less than or equal (for ``VAL1``  :math:``  ``VAL2`` ).

              * ``GE`` - Greater than or equal (for ``VAL1``  :math:``  ``VAL2`` ).

              * ``ABLT`` - Absolute values of ``VAL1`` and ``VAL2`` before < operation.

              * ``ABGT`` - Absolute values of ``VAL1`` and ``VAL2`` before > operation.

        val2 : str
            Second numerical value (or parameter which evaluates to numerical value) in the conditional
            comparison operation.

        conj : str
            (Optional) Connection between two logical clauses.

              * ``AND -`` - True if both clauses ( ``Oper1`` and ``Oper2`` ) are true.

              * ``OR -`` - True if either clause is true.

              * ``XOR -`` - True if either (but not both) clause is true.

        val3 : str
            (Optional) Third numerical value (or parameter which evaluates to numerical value).

        oper2 : str
            (Optional) Operation label. This will have the same labels as ``Oper1``, except it uses
            ``Val3`` and ``Val4``. A tolerance of 1.0E-10 is used for comparisons between real numbers.

        val4 : str
            (Optional) Fourth numerical value (or parameter value which evaluates to a numerical value).

        Notes
        -----
        Optional intermediate block separator within an if-then-else construct. All seven characters of the
        command name (\2ELSEIF) must be input. This command is similar to the ``\*IF`` command except that the
        ``Base`` field is not used. The ``\*IF``, :ref:`elseif`, ``\*ELSE``, and :ref:`endif` commands for
        each if-then-else construct must all be read from the same file (or keyboard).

        This command is valid in any processor.
        """
        command = f"*ELSEIF,{val1},{oper1},{val2},{conj},{val3},{oper2},{val4}"
        return self.run(command, **kwargs)

    def starexit(self, **kwargs):
        r"""Exits a do-loop.

        Mechanical APDL Command: `\*EXIT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_EXIT_st.html>`_

        Notes
        -----
        The command following the :ref:`enddo` is executed next. The exit option may also be conditional
        [Use the ``\*IF`` ]. The :ref:`starexit` command must appear on the same file as the :ref:`do`
        command.

        This command is valid in any processor.
        """
        command = f"*EXIT"
        return self.run(command, **kwargs)

    def enddo(self, **kwargs):
        r"""Ends a do-loop and starts the looping action.

        Mechanical APDL Command: `\*ENDDO <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ENDDO.html>`_

        Notes
        -----
        One :ref:`enddo` is required for each nested do-loop. The :ref:`enddo` command must appear on the
        same file as the :ref:`do` command, and all six characters must be input.

        This command is valid in any processor.
        """
        command = f"*ENDDO"
        return self.run(command, **kwargs)

    def repeat(
        self,
        ntot: str = "",
        vinc1: str = "",
        vinc2: str = "",
        vinc3: str = "",
        vinc4: str = "",
        vinc5: str = "",
        vinc6: str = "",
        vinc7: str = "",
        vinc8: str = "",
        vinc9: str = "",
        vinc10: str = "",
        vinc11: str = "",
        **kwargs,
    ):
        r"""Repeats the previous command.

        Mechanical APDL Command: `\*REPEAT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_REPEAT.html>`_

        Parameters
        ----------
        ntot : str
            Number of times the preceding command is executed (including the initial execution). Must be 2
            or greater. ``NTOT`` of 2 causes one repeat (for a total of 2 executions).

        vinc1 : str
            Value increments applied to first through eleventh data fields of the preceding command.

        vinc2 : str
            Value increments applied to first through eleventh data fields of the preceding command.

        vinc3 : str
            Value increments applied to first through eleventh data fields of the preceding command.

        vinc4 : str
            Value increments applied to first through eleventh data fields of the preceding command.

        vinc5 : str
            Value increments applied to first through eleventh data fields of the preceding command.

        vinc6 : str
            Value increments applied to first through eleventh data fields of the preceding command.

        vinc7 : str
            Value increments applied to first through eleventh data fields of the preceding command.

        vinc8 : str
            Value increments applied to first through eleventh data fields of the preceding command.

        vinc9 : str
            Value increments applied to first through eleventh data fields of the preceding command.

        vinc10 : str
            Value increments applied to first through eleventh data fields of the preceding command.

        vinc11 : str
            Value increments applied to first through eleventh data fields of the preceding command.

        Notes
        -----
        :ref:`repeat` must immediately follow the command that is to be repeated. The numeric arguments of
        the initial command may be incremented in the generated commands. The numeric increment values may
        be integer or real, positive or negative, zero or blank. Alphanumeric arguments cannot be
        incremented. For large values of ``NTOT``, consider printout suppression ( :ref:`nopr` command)
        first.

        Most commands beginning with slash (/), star (\2), as well as "unknown command" macros, cannot be
        repeated. For these commands, or if more than one command is to be repeated, include them within a
        do-loop. File switching commands (those reading additional commands) cannot be repeated. If a
        :ref:`repeat` command immediately follows another :ref:`repeat` command, the repeat action only
        applies to the last non- :ref:`repeat` command. Also, :ref:`repeat` should not be used in
        interactive mode immediately after a) a command (or its log file equivalent) that uses picking, or
        b) a command that requires a response from the user.

        This command is valid in any processor.
        """
        command = f"*REPEAT,{ntot},{vinc1},{vinc2},{vinc3},{vinc4},{vinc5},{vinc6},{vinc7},{vinc8},{vinc9},{vinc10},{vinc11}"
        return self.run(command, **kwargs)

    def dowhile(self, par: str = "", **kwargs):
        r"""Loops repeatedly through the next :ref:`enddo` command.

        Mechanical APDL Command: `\*DOWHILE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_DOWHILE.html>`_

        Parameters
        ----------
        par : str
            The name of the scalar parameter to be used as the loop index. There is no character parameter
            substitution for the ``Par`` field.

        Notes
        -----
        :ref:`dowhile` loops repeatedly through the next :ref:`enddo` command as long as ``Par`` is greater
        than zero. The block of commands following the :ref:`dowhile` command (up to the :ref:`enddo`
        command) is executed repeatedly until some loop control is satisfied. Printout is automatically
        suppressed on all loops after the first (include a :ref:`gopr` command to restore the printout). The
        command line loop control ( ``Par`` ) must be input; however, ``\*IF`` within the block can also be
        used to control looping ( :ref:`starexit`, :ref:`cycle` ). One level of internal file switching is
        used for each nested :ref:`dowhile` . Twenty levels of nested do-loops are allowed.

        This command is valid in any processor.
        """
        command = f"*DOWHILE,{par}"
        return self.run(command, **kwargs)

    def do(
        self, par: str = "", ival: str = "", fval: str = "", inc: str = "", **kwargs
    ):
        r"""Defines the beginning of a do-loop.

        Mechanical APDL Command: `\*DO <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_DO.html>`_

        Parameters
        ----------
        par : str
            The name of the scalar parameter to be used as the loop index. See :ref:`starset` for name
            restrictions. Any existing parameter of the same name will be redefined. There is no character
            parameter substitution for the ``Par`` field.

        ival : str
            Initially assign ``IVAL`` to ``Par``. Increment ``IVAL`` by ``INC`` for each successive loop.
            If ``IVAL`` exceeds ``FVAL`` and ``INC`` is positive, the loop is not executed. ``INC`` defaults
            to 1. Negative increments and non-integer numbers are allowed.

        fval : str
            Initially assign ``IVAL`` to ``Par``. Increment ``IVAL`` by ``INC`` for each successive loop.
            If ``IVAL`` exceeds ``FVAL`` and ``INC`` is positive, the loop is not executed. ``INC`` defaults
            to 1. Negative increments and non-integer numbers are allowed.

        inc : str
            Initially assign ``IVAL`` to ``Par``. Increment ``IVAL`` by ``INC`` for each successive loop.
            If ``IVAL`` exceeds ``FVAL`` and ``INC`` is positive, the loop is not executed. ``INC`` defaults
            to 1. Negative increments and non-integer numbers are allowed.

        Notes
        -----
        The block of commands following the :ref:`do` command (up to the :ref:`enddo` command) is executed
        repeatedly until some loop control is satisfied. Printout is automatically suppressed on all loops
        after the first (include a :ref:`gopr` command to restore the printout). The command line loop
        control ( ``Par``, ``IVAL``, ``FVAL``, ``INC`` ) must be input; however, a Use the ``\*IF`` within
        the block can also be used to control looping ( :ref:`starexit`, :ref:`cycle` ). One level of
        internal file switching is used for each nested :ref:`do`. Twenty levels of nested do-loops are
        allowed.

        Do-loops that include :ref:`input`, :ref:`use`, or an "Unknown Command" macro, have less nesting
        available because each of these operations also uses a level of file switching. The :ref:`do` ,
        :ref:`enddo`, and any :ref:`cycle` and :ref:`starexit` commands for a do-loop must all be read from
        the same file (or keyboard). You cannot use the `MULTIPRO
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_apdl/Hlp_P_APDL5_2.html#apdlch5fig2tlm>`_
        or :ref:`create` commands within a :ref:`do` -loop. Picking operations should also not be used
        within a :ref:`do` -loop.

        This command is valid in any processor.
        """
        command = f"*DO,{par},{ival},{fval},{inc}"
        return self.run(command, **kwargs)
