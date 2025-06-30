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


class LoadCaseCalculations:

    def lcabs(self, lcno: str = "", kabs: int | str = "", **kwargs):
        r"""Specifies absolute values for load case operations.

        Mechanical APDL Command: `LCABS <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_LCABS.html>`_

        Parameters
        ----------
        lcno : str
            Load case pointer number. If ALL, apply to all selected load cases ( :ref:`lcsel` ).

        kabs : int or str
            Absolute value key:

            * ``0`` - Use algebraic values of load case ``LCNO`` in operations.

            * ``1`` - Use absolute values of load case ``LCNO`` in operations.

        Notes
        -----

        .. _LCABS_notes:

        Causes absolute values to be used in the load case operations ( :ref:`lcase` or :ref:`lcoper` ).
        Absolute values are taken prior to assigning a load case factor ( :ref:`lcfact` ) and are applied
        only to defined load cases ( :ref:`lcdef` ).

        When :ref:`lcabs` operates on nodal-averaged results, it may yield different numerical values
        compared to the same data stored as element results. For more information, see `Nodal-Averaged
        Results
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_CH2_2.html#nodeavepost>`_
        """
        command = f"LCABS,{lcno},{kabs}"
        return self.run(command, **kwargs)

    def lcase(self, lcno: str = "", **kwargs):
        r"""Reads a load case into the database.

        Mechanical APDL Command: `LCASE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_LCASE.html>`_

        Parameters
        ----------
        lcno : str
            Load case pointer number ( :ref:`lcdef`,STAT). Defaults to 1.

        Notes
        -----

        .. _LCASE_notes:

        Reads a load case into the database. Load cases are created as described on the :ref:`lcdef` or
        :ref:`lcwrite` commands. The results portion of the database and the applied forces and
        displacements are cleared before reading the data in. Absolute values ( :ref:`lcabs` ) and scale
        factors ( :ref:`lcfact` ) can be applied during the read operation.

        For details on using load case combination, see `Creating and Combining Load Cases
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/Hlp_G_BAS5_4.html#bassummtlm51499325>`_
        """
        command = f"LCASE,{lcno}"
        return self.run(command, **kwargs)

    def lcdef(
        self,
        lcno: str = "",
        lstep: str = "",
        sbstep: str = "",
        kimg: int | str = "",
        **kwargs,
    ):
        r"""Creates a load case from a set of results on a results file.

        Mechanical APDL Command: `LCDEF <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_LCDEF.html>`_

        Parameters
        ----------
        lcno : str
            Arbitrary pointer number (1-99) to be assigned to the load case specified by ``LSTEP``,
            ``SBSTEP`` and by the ``FILE`` command. Defaults to 1 + previous value.

        lstep : str
            Load step number to be defined as the load case. Defaults to one.

        sbstep : str
            Substep number. Defaults to the last substep of the load step.

        kimg : int or str
            Used only with results from complex analyses:

            * ``0`` - Use real part of complex solution

            * ``1`` - Use imaginary part.

        Notes
        -----

        .. _LCDEF_notes:

        Creates a load case by establishing a pointer to a set of results on a results file (written during
        the analysis solution phase). This pointer ( ``LCNO`` ) can then be used on the :ref:`lcase` or
        :ref:`lcoper` commands to read the load case data into the database.

        Issue :ref:`lcdef`,ERASE to delete all load case pointers (and all load case files, if any). Issue
        :ref:`lcdef`, ``LCNO``,ERASE to delete only the specific load case pointer ``LCNO`` (and its file,
        if any). With the ERASE options, all pointers are deleted; however only files with the default
        extension ( :ref:`lcwrite` ) are deleted. Issue :ref:`lcdef`,STAT for status of all selected load
        cases ( :ref:`lcsel` ), or :ref:`lcdef`,STAT,ALL for status of all load cases. The :ref:`stat`
        command may be used to list all load cases. See also :ref:`lcfile` to establish a pointer to a set
        of results on a load case file (written by :ref:`lcwrite` ). Harmonic element data read from a
        result file load case is stored at the zero-degree position.

        For details on using load case combination, see `Creating and Combining Load Cases
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/Hlp_G_BAS5_4.html#bassummtlm51499325>`_
        """
        command = f"LCDEF,{lcno},{lstep},{sbstep},{kimg}"
        return self.run(command, **kwargs)

    def lcfact(self, lcno: str = "", fact: str = "", **kwargs):
        r"""Defines scale factors for load case operations.

        Mechanical APDL Command: `LCFACT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_LCFACT.html>`_

        Parameters
        ----------
        lcno : str
            Load case pointer number. If ALL, apply to all selected load cases ( :ref:`lcsel` ).

        fact : str
            Scale factor applied to load case ``LCNO``. Blank defaults to 1.0.

        Notes
        -----

        .. _LCFACT_notes:

        Defines scale factors to be used in the load case operations ( :ref:`lcase` or :ref:`lcoper` ).
        Scale factors are applied after an absolute value operation ( :ref:`lcabs` ) and are applied only to
        defined load cases ( :ref:`lcdef` ).

        For details on using load case combination, see `Creating and Combining Load Cases
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/Hlp_G_BAS5_4.html#bassummtlm51499325>`_
        """
        command = f"LCFACT,{lcno},{fact}"
        return self.run(command, **kwargs)

    def lcfile(self, lcno: str = "", fname: str = "", ext: str = "", **kwargs):
        r"""Creates a load case from an existing load case file.

        Mechanical APDL Command: `LCFILE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_LCFILE.html>`_

        Parameters
        ----------
        lcno : str
            Arbitrary (1-99) pointer number assigned to this load case.

        fname : str
            File name and directory path (248 characters maximum, including the characters needed for the
            directory path). An unspecified directory path defaults to the working directory; in this case,
            you can use all 248 characters for the file name. The file name defaults to :file:`Jobname`.

        ext : str
            Filename extension (eight-character maximum). The extension defaults to the ``LCNO`` value
            preceded by an L (for values 10-99) or by an L0 (for values 1-9).

        Notes
        -----

        .. _LCFILE_notes:

        Creates a load case by establishing a pointer to an existing load case file ( :ref:`lcwrite` ). This
        pointer ( ``LCNO`` ) can then be used on the :ref:`lcase` or :ref:`lcoper` commands to read the load
        case data into the database. This command is typically used to reestablish load case pointers in a
        new Mechanical APDL session (pointers are not saved on the database file), or when more than one
        pointer to
        a single load case is desired. See the :ref:`lcdef` command for status and erase operations. See
        also :ref:`lcdef` to establish a pointer to a set of results on a results file (written during the
        analysis solution phase).

        For details on using load case combination, see `Creating and Combining Load Cases
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/Hlp_G_BAS5_4.html#bassummtlm51499325>`_
        """
        command = f"LCFILE,{lcno},{fname},{ext}"
        return self.run(command, **kwargs)

    def lcoper(
        self,
        oper: str = "",
        lcase1: str = "",
        oper2: str = "",
        lcase2: str = "",
        sweepang: str = "",
        **kwargs,
    ):
        r"""Performs load case operations.

        Mechanical APDL Command: `LCOPER <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_LCOPER.html>`_

        Parameters
        ----------
        oper : str
            Valid operations are:

            * ``ZERO`` - Zero results portion of database ( ``LCASE1`` ignored).

            * ``SQUA`` - Square database values ( ``LCASE1`` ignored).

            * ``SQRT`` - Square root of database (absolute) values ( ``LCASE1`` ignored).

            * ``LPRIN`` - Recalculate line element principal stresses ( ``LCASE1`` ignored). Stresses are as
              shown for the NMISC items of the :ref:`etable` command for the specific line element type.

            * ``ADD`` - Add ``LCASE1`` to database values.

            * ``SUB`` - Subtract ``LCASE1`` from database values.

            * ``SRSS`` - Square root of the sum of the squares of database and ``LCASE1``.

            * ``MIN`` - Compare and save in database the algebraic minimum of database and ``LCASE1``.

            * ``MAX`` - Compare and save in database the algebraic maximum of database and ``LCASE1``.

            * ``ABMN`` - Compare and save in database the absolute minimum of database and ``LCASE1`` (based on
              magnitudes, then apply the corresponding sign).

            * ``ABMX`` - Compare and save in database the absolute maximum of database and ``LCASE1`` (based on
              magnitudes, then apply the corresponding sign).

        lcase1 : str
            First load case in the operation (if any). See ``LCNO`` of the :ref:`lcdef` command. If ALL,
            repeat operations using all selected load cases ( :ref:`lcsel` ).

        oper2 : str
            Valid operations are:

            * ``MULT`` - Multiplication: ``LCASE1`` \* ``LCASE2``

            * ``CPXMAX`` - This option does a phase angle sweep to calculate the maximum of derived stresses,
              equivalent strain, and principal strains for a complex solution where ``LCASE1`` is the real part
              and ``LCASE2`` is the imaginary part. The ``Oper`` field is not applicable with this option. Also,
              the :ref:`lcabs` and :ref:`sumtype` commands have no effect on this option. The value of S3 will be
              a minimum. Absolute maximum is obtained for component quantity. This option does not apply to
              derived displacement amplitude (USUM). Load case writing ( :ref:`lcwrite` ) is not supported. See
              `POST1 and POST26 - Complex Results Postprocessing
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_post15.html#thyeq1cdmplxres6a>`_

        lcase2 : str
            Second load case. Used only with ``Oper2`` operations.

        sweepang : str
            Sweep angle increment in degrees for phase sweep. Used only with ``Oper2`` = CPXMAX. (Default =
            1°)

        Notes
        -----

        .. _LCOPER_notes:

        :ref:`lcoper` operates on the database and one or two load cases according to:

        * Database = Database ``Oper`` ( ``LCASE1``  ``Oper2``  ``LCASE2`` )

        where operations ``Oper`` and ``Oper2`` are as described above.

        Absolute values and scale factors may be applied to the load cases before the operations (
        :ref:`lcabs`, :ref:`lcfact` ). If ``LCASE1`` is not specified, only operation ``Oper`` is performed
        on the current database. If ``LCASE2`` is specified, operation ``Oper2`` is performed before
        operation ``Oper``. If ``LCASE2`` is not specified, operation ``Oper2`` is ignored.

        Solution items not contained ( :ref:`outres` ) in either the database or the applicable load cases
        will result in a null item during a load case operation. Harmonic element data read from a result
        file load case are processed at zero degrees.

        Load case combinations must be performed on load cases from the same results file. Combining load
        cases from different results files is not supported.

        Load case combinations of element-based solutions are performed in the solution coordinate system,
        and the data resulting from load case combinations are stored in the solution coordinate system. The
        resultant data are then transformed to the active results coordinate system ( :ref:`rsys` ) when
        listed or displayed. Except in the cases of ``Oper`` = LPRIN, ADD, or SUB, you must use
        :ref:`rsys`,SOLU to list or display results. In the case of layered elements, the layer (
        :ref:`layer` ) must also be specified.

        If `nodal-averaged results
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_CH2_2.html#nodeavepost>`_ are
        a part of the load case combination, the resulting nodal-averaged result data are in the global
        Cartesian coordinate system. Furthermore, the resulting numerical values may differ from the same
        :ref:`lcoper` operation performed on the same data stored as element results. The SQUA, SQRT, LPRIN,
        and SRSS operations are not valid when applied to nodal averaged results. For more information, see
        `Nodal-Averaged Results
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_CH2_2.html#nodeavepost>`_

        Use the :ref:`force` command prior to any combination operation to correctly combine the requested
        force type.

        If Oper2=CPXMAX, the derived stresses and strain calculation do not apply to line elements.

        For details on using load case combination, see `Creating and Combining Load Cases
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/Hlp_G_BAS5_4.html#bassummtlm51499325>`_

        For cyclic symmetry ( :ref:`cyclic` ), :ref:`lcoper` operates on the raw base and duplicate sector
        values. It cannot be used on the expanded values ( :ref:`cycexpand` ).
        """
        command = f"LCOPER,{oper},{lcase1},{oper2},{lcase2},{sweepang}"
        return self.run(command, **kwargs)

    def lcsel(
        self,
        type_: str = "",
        lcmin: str = "",
        lcmax: str = "",
        lcinc: str = "",
        **kwargs,
    ):
        r"""Selects a subset of load cases.

        Mechanical APDL Command: `LCSEL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_LCSEL.html>`_

        Parameters
        ----------
        type_ : str
            Label identifying the type of select:

            * ``S`` - Select a new set.

            * ``R`` - Reselect a set from the current set.

            * ``A`` - Additionally select a set and extend the current set.

            * ``U`` - Unselect a set from the current set.

            * ``ALL`` - Restore the full set.

            * ``NONE`` - Unselect the full set.

            * ``INVE`` - Invert the current set (selected becomes unselected and vice versa).

            * ``STAT`` - Display the current select status.

        lcmin : str
            Minimum value of load case pointer range.

        lcmax : str
            Maximum value of load case pointer range. ``LCMAX`` defaults to ``LCMIN``.

        lcinc : str
            Value increment within range. Defaults to 1. ``LCINC`` cannot be negative.

        Notes
        -----

        .. _LCSEL_notes:

        Selects a subset of load cases for other operations. For example, to select a new set of load cases
        based on load cases 1 through 7, use :ref:`lcsel`,S,1,7. The subset is used when the ALL label is
        entered (or implied) on other commands, such as :ref:`lcfact`, :ref:`lcabs`, :ref:`lcoper`, etc.
        Load cases are flagged as selected and unselected; no load case pointers ( :ref:`lcdef`,
        :ref:`lcwrite`, :ref:`lcfile` ) are actually deleted from the database.

        For details on using load case combination, see `Creating and Combining Load Cases
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/Hlp_G_BAS5_4.html#bassummtlm51499325>`_
        """
        command = f"LCSEL,{type_},{lcmin},{lcmax},{lcinc}"
        return self.run(command, **kwargs)

    def lcwrite(self, lcno: str = "", fname: str = "", ext: str = "", **kwargs):
        r"""Creates a load case by writing results to a load case file.

        Mechanical APDL Command: `LCWRITE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_LCWRITE.html>`_

        Parameters
        ----------
        lcno : str
            Arbitrary pointer number (1-99) to be assigned to this load case.

        fname : str
            File name and directory path (248 characters maximum, including the characters needed for the
            directory path). An unspecified directory path defaults to the working directory; in this case,
            you can use all 248 characters for the file name. The file name defaults to :file:`Jobname`.

        ext : str
            Filename extension (eight-character maximum). The extension defaults to the ``LCNO`` value
            preceded by an L (for values 10-99) or by an L0 (for values 1-9).

        Notes
        -----

        .. _LCWRITE_notes:

        Creates a load case by writing the results data in the database to a load case file. The database
        remains unchanged by this operation. A pointer is also established to the written set of results on
        the load case file. This pointer ( ``LCNO`` ) can then be used on the :ref:`lcase` or :ref:`lcoper`
        commands to read the load case data into the database. By default, only summable results data (such
        as displacements, stresses, elastic strains) and constant results data (such as volume) are written
        to the load case file unless requested ( :ref:`lcsum` command). Non-summable results data (such as
        plastic strains, strain energy), boundary conditions, and nodal loads are not written to the load
        case file. The load case file may be named by default or by a user name. Rewriting to the same file
        overwrites the previous data. See the :ref:`lcdef` command for status and erase operations.

        For details on using load case combination, see `Creating and Combining Load Cases
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/Hlp_G_BAS5_4.html#bassummtlm51499325>`_
        """
        command = f"LCWRITE,{lcno},{fname},{ext}"
        return self.run(command, **kwargs)

    def lczero(self, **kwargs):
        r"""Zeroes the results portion of the database.

        Mechanical APDL Command: `LCZERO <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_LCZERO.html>`_

        Notes
        -----

        .. _LCZERO_notes:

        Often used before the :ref:`lcoper` command. Same as :ref:`lcoper`,ZERO.
        """
        command = "LCZERO"
        return self.run(command, **kwargs)

    def rappnd(self, lstep: str = "", time: str = "", **kwargs):
        r"""Appends results data from the database to the results file.

        Mechanical APDL Command: `RAPPND <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_RAPPND.html>`_

        Parameters
        ----------
        lstep : str
            Load step number to be assigned to the results data set. If it is the same as an existing load
            step number on the results file, the appended load step will be inaccessible. Defaults to 1.

        time : str
            Time value to be assigned to the results data set. Defaults to 0.0. A time value greater than
            the last load step should be used.

        Notes
        -----

        .. _RAPPND_notes:

        This command is typically used to append the results from a load case combination to the results
        file. See the :ref:`lcwrite` command to create a separate load case file. Only summable and constant
        data are written to the results file by default; non-summable data are not written unless requested
        ( :ref:`lcsum` command). ``RAPPND`` should not be used to append results from a harmonic analysis.
        """
        command = f"RAPPND,{lstep},{time}"
        return self.run(command, **kwargs)
