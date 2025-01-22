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


class ParameterDefinition:

    def inquire(self, strarray: str = "", func: str = "", **kwargs):
        r"""Returns system information to a parameter.

        Mechanical APDL Command: `/INQUIRE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_INQUIRE.html>`_

        Parameters
        ----------
        strarray : str
            Name of the "string array" parameter that will hold the returned values. String array parameters
            are similar to character arrays, but each array element can be as long as 248 characters. If the
            string parameter does not exist, it will be created.

        func : str
            Specifies the type of system information returned:

            * ``LOGIN`` - Returns the pathname of the login directory on Linux systems or the pathname of the default
              directory (including drive letter) on Windows systems.

            * ``DOCU`` - Returns the pathname of the Mechanical APDL docu directory.

            * ``APDL`` - Returns the pathname of the Mechanical APDL APDL directory.

            * ``PROG`` - Returns the pathname of the Mechanical APDL executable directory.

            * ``AUTH`` - Returns the pathname of the directory in which the license file resides.

            * ``USER`` - Returns the name of the user currently logged-in.

            * ``DIRECTORY`` - Returns the pathname of the current directory.

            * ``JOBNAME`` - Returns the current ``Jobname``.

            * ``RSTDIR`` - Returns rst directory ( :ref:`file` command).

            * ``RSTFILE`` - Returns rst file name ( :ref:`file` command).

            * ``RSTEXT`` - Returns rst file extension ( :ref:`file` command).

            * ``PSEARCH`` - Returns path used for "unknown command" macro ( :ref:`psearch` command).

            * ``OUTPUT`` - Returns the current output file name ( :ref:`output` command).

        Notes
        -----
        The :ref:`inquire` command is valid in any processor.
        """
        command = f"/INQUIRE,{strarray},{func}"
        return self.run(command, **kwargs)

    def afun(self, lab: str = "", **kwargs):
        r"""Specifies units for angular functions in parameter expressions.

        Mechanical APDL Command: `\*AFUN <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_AFUN.html>`_

        Parameters
        ----------
        lab : str
            Specifies the units to be used:

            * ``RAD`` - Use radians for input and output of parameter angular functions (default).

            * ``DEG`` - Use degrees for input and output of parameter angular functions.

            * ``STAT`` - Show current setting (DEG or RAD) for this command.

        Notes
        -----
        Only the SIN, COS, TAN, ASIN, ACOS, ATAN, ATAN2, ANGLEK, and ANGLEN functions ( :ref:`starset`,
        :ref:`vfun` ) are affected by this command.
        """
        command = f"*AFUN,{lab}"
        return self.run(command, **kwargs)

    def parsav(self, lab: str = "", fname: str = "", ext: str = "", **kwargs):
        r"""Writes parameters to a file.

        Mechanical APDL Command: `PARSAV <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PARSAV.html>`_

        Parameters
        ----------
        lab : str
            Write operation:

            * ``SCALAR`` - Write only scalar parameters (default).

            * ``ALL`` - Write scalar and array parameters. Parameters may be numeric or alphanumeric.

        fname : str
            File name and directory path (248 characters maximum, including the characters needed for the
            directory path). An unspecified directory path defaults to the working directory; in this case,
            you can use all 248 characters for the file name. The file name defaults to :file:`Jobname`.

        ext : str
            Filename extension (eight-character maximum). The extension defaults to PARM if ``Fname`` is
            blank.

        Notes
        -----
        Writes the current parameters to a coded file. Previous parameters on this file, if any, will be
        overwritten. The parameter file may be read with the :ref:`parres` command.

        :ref:`parsav` / :ref:`parres` operations truncate some long decimal strings, and can cause differing
        values in your solution data when other operations are performed. A good practice is to limit the
        number of decimal places you will use before and after these operations.

        This command is valid in any processor.
        """
        command = f"PARSAV,{lab},{fname},{ext}"
        return self.run(command, **kwargs)

    def parres(self, lab: str = "", fname: str = "", ext: str = "", **kwargs):
        r"""Reads parameters from a file.

        Mechanical APDL Command: `PARRES <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PARRES.html>`_

        Parameters
        ----------
        lab : str
            Read operation:

            * ``NEW`` - Replace current parameter set with these parameters (default).

            * ``CHANGE`` - Extend current parameter set with these parameters, replacing any that already exist.

        fname : str
            File name and directory path (248 characters maximum, including the characters needed for the
            directory path). An unspecified directory path defaults to the working directory; in this case,
            you can use all 248 characters for the file name. The file name defaults to :file:`Jobname`.

        ext : str
            Filename extension (eight-character maximum). The extension defaults to PARM if ``Fname`` is
            blank.

        Notes
        -----
        Reads parameters from a coded file. The parameter file may have been written with the :ref:`parsav`
        command. The parameters read may replace or change the current parameter set.

        This command is valid in any processor.
        """
        command = f"PARRES,{lab},{fname},{ext}"
        return self.run(command, **kwargs)

    def starstatus(
        self,
        par: str = "",
        imin: str = "",
        imax: str = "",
        jmin: str = "",
        jmax: str = "",
        kmin: str = "",
        kmax: str = "",
        lmin: str = "",
        lmax: str = "",
        mmin: str = "",
        mmax: str = "",
        kpri: int | str = "",
        **kwargs,
    ):
        r"""Lists the current parameters and abbreviations.

        Mechanical APDL Command: `\*STATUS <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_STATUS_st.html>`_

        Parameters
        ----------
        par : str
            Specifies the parameter or sets of parameters listed. For array parameters, use ``IMIN``, ``IMAX``,
            etc. to specify ranges. Use :ref:`dim` to define array parameters. Use ``\*VEDIT`` to review array
            parameters interactively. Use :ref:`vwrite` to print array values in a formatted output. If ``Par``
            is blank, list all scalar parameter values, array parameter dimensions, and abbreviations. If ARGX,
            list the active set of local macro parameters (ARG1 to ARG9 and AR10 to AR99) ( :ref:`use` ).

            The following are possible values for ``Par``

            * ``ALL or blank`` - Lists all parameters (except local macro parameters and those with names beginning or ending with an
              underbar) and toolbar abbreviations.

            * ``_PRM`` - Lists only parameters with names beginning with an underbar (_). These are Mechanical APDL internal
              parameters.

            * ``PRM_`` - Lists only parameters with names ending with an underbar (_). A good APDL programming convention is
              to ensure that all parameters created by your system programmer are named with a trailing underbar.

            * ``ABBR`` - Lists all toolbar abbreviations.

            * ``PARM`` - Lists all parameters (except local macro parameters and those with names beginning or ending with an
              underbar).

            * ``MATH`` - Lists all APDL Math parameters, including vectors, matrices, and linear solvers.

            * ``PARNAME`` - Lists only the parameter specified. ``PARNAME`` cannot be a local macro parameter name.

            * ``ARGX`` - Lists all local macro parameter values (ARG1- AR99) that are non-zero or non-blank.

        imin : str
            Range of array elements to display (in terms of the dimensions (row, column, plane, book, and
            shelf). Minimum values default to 1. Maximum values default to the maximum dimension values.
            Zero may be input for ``IMIN``, ``JMIN``, and ``KMIN`` to display the index numbers. See
            :ref:`taxis` command to list index numbers of 4- and 5-D tables.

        imax : str
            Range of array elements to display (in terms of the dimensions (row, column, plane, book, and
            shelf). Minimum values default to 1. Maximum values default to the maximum dimension values.
            Zero may be input for ``IMIN``, ``JMIN``, and ``KMIN`` to display the index numbers. See
            :ref:`taxis` command to list index numbers of 4- and 5-D tables.

        jmin : str
            Range of array elements to display (in terms of the dimensions (row, column, plane, book, and
            shelf). Minimum values default to 1. Maximum values default to the maximum dimension values.
            Zero may be input for ``IMIN``, ``JMIN``, and ``KMIN`` to display the index numbers. See
            :ref:`taxis` command to list index numbers of 4- and 5-D tables.

        jmax : str
            Range of array elements to display (in terms of the dimensions (row, column, plane, book, and
            shelf). Minimum values default to 1. Maximum values default to the maximum dimension values.
            Zero may be input for ``IMIN``, ``JMIN``, and ``KMIN`` to display the index numbers. See
            :ref:`taxis` command to list index numbers of 4- and 5-D tables.

        kmin : str
            Range of array elements to display (in terms of the dimensions (row, column, plane, book, and
            shelf). Minimum values default to 1. Maximum values default to the maximum dimension values.
            Zero may be input for ``IMIN``, ``JMIN``, and ``KMIN`` to display the index numbers. See
            :ref:`taxis` command to list index numbers of 4- and 5-D tables.

        kmax : str
            Range of array elements to display (in terms of the dimensions (row, column, plane, book, and
            shelf). Minimum values default to 1. Maximum values default to the maximum dimension values.
            Zero may be input for ``IMIN``, ``JMIN``, and ``KMIN`` to display the index numbers. See
            :ref:`taxis` command to list index numbers of 4- and 5-D tables.

        lmin : str
            Range of array elements to display (in terms of the dimensions (row, column, plane, book, and
            shelf). Minimum values default to 1. Maximum values default to the maximum dimension values.
            Zero may be input for ``IMIN``, ``JMIN``, and ``KMIN`` to display the index numbers. See
            :ref:`taxis` command to list index numbers of 4- and 5-D tables.

        lmax : str
            Range of array elements to display (in terms of the dimensions (row, column, plane, book, and
            shelf). Minimum values default to 1. Maximum values default to the maximum dimension values.
            Zero may be input for ``IMIN``, ``JMIN``, and ``KMIN`` to display the index numbers. See
            :ref:`taxis` command to list index numbers of 4- and 5-D tables.

        mmin : str
            Range of array elements to display (in terms of the dimensions (row, column, plane, book, and
            shelf). Minimum values default to 1. Maximum values default to the maximum dimension values.
            Zero may be input for ``IMIN``, ``JMIN``, and ``KMIN`` to display the index numbers. See
            :ref:`taxis` command to list index numbers of 4- and 5-D tables.

        mmax : str
            Range of array elements to display (in terms of the dimensions (row, column, plane, book, and
            shelf). Minimum values default to 1. Maximum values default to the maximum dimension values.
            Zero may be input for ``IMIN``, ``JMIN``, and ``KMIN`` to display the index numbers. See
            :ref:`taxis` command to list index numbers of 4- and 5-D tables.

        kpri : int or str
            Use this field to list your primary variable labels (X, Y, Z, TIME, etc.).

            * ``1`` - List the labels (default). YES, Y, or ON are also valid entries.

            * ``0`` - Do not list the labels. NO, N, or OFF are also valid entries.

        Notes
        -----
        You cannot obtain the value for a single local parameter (for example, :ref:`starstatus`,ARG2). You
        can only request all local parameters simultaneously using :ref:`starstatus`,ARGX.

        This command is valid in any processor.
        """
        command = f"*STATUS,{par},{imin},{imax},{jmin},{jmax},{kmin},{kmax},{lmin},{lmax},{mmin},{mmax},{kpri}"
        return self.run(command, **kwargs)

    def starset(
        self,
        par: str = "",
        value: str = "",
        val2: str = "",
        val3: str = "",
        val4: str = "",
        val5: str = "",
        val6: str = "",
        val7: str = "",
        val8: str = "",
        val9: str = "",
        val10: str = "",
        **kwargs,
    ):
        r"""Assigns values to user-named parameters.

        Mechanical APDL Command: `\*SET <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SET_st.html>`_

        Parameters
        ----------
        par : str
            An alphanumeric name used to identify this parameter. ``Par`` can contain up to 32 characters,
            beginning with a letter and containing only letters, numbers, and underscores. Examples:

            .. code:: apdl

               ABC A3X TOP_END

            Command names, function names, label names, component and assembly names, etc., are invalid, as
            are parameter names beginning with an underscore (for example,

            .. code:: apdl

               _LOOP

            ).

            Parameter names ending in an underscore are not listed by the :ref:`starstatus` command. Array
            parameter names must be followed by a subscript, and the entire expression must be 32 characters
            or less. Examples:

            .. code:: apdl

               A(1,1) NEW_VAL(3,2,5) RESULT(1000)

            There is no character parameter substitution for the ``Par`` field. Table parameters used in
            command fields (where constant values are normally given) are limited to 32 characters.

        value : str
            Numerical value or alphanumeric character string (up to 32 characters enclosed in single quotes)
            to be assigned to this parameter. Examples:

            .. code:: apdl

               A(1,3)=7.4 B='ABC3'

            Can also be a parameter or a parametric expression. Examples:

            .. code:: apdl

               C=A(1,3) A(2,2)=(C+4)/2

            .. code:: apdl

               C=A(1,3) A(2,2)=(C+4)/2

             If ``VALUE`` is the table array name, the subscripts are the values of the primary variables
            and the table is evaluated at these specified index values.

            If blank, delete this parameter. Example:

            .. code:: apdl

               A=

            deletes parameter

            .. code:: apdl

               A

            .. code:: apdl

               A

        val2 : str
            If ``Par`` is an array parameter, values ``VAL2`` through ``VAL10`` (up to the last nonblank
            value) are sequentially assigned to the succeeding array elements of the column. Examples:

            .. code:: apdl

               *SET,A(1,4),10,11

            assigns

            .. code:: apdl

               A(1,4)=10, A(2,4)=11

            .. code:: apdl

               A(1,4)=10, A(2,4)=11

            .. code:: apdl

               *SET,B(2,3),'file10','file11'

            assigns

            .. code:: apdl

               B(2,3)='file10',           B(3,3)='file11'

            .. code:: apdl

               B(2,3)='file10',           B(3,3)='file11'

        val3 : str
            If ``Par`` is an array parameter, values ``VAL2`` through ``VAL10`` (up to the last nonblank
            value) are sequentially assigned to the succeeding array elements of the column. Examples:

            .. code:: apdl

               *SET,A(1,4),10,11

            assigns

            .. code:: apdl

               A(1,4)=10, A(2,4)=11

            .. code:: apdl

               A(1,4)=10, A(2,4)=11

            .. code:: apdl

               *SET,B(2,3),'file10','file11'

            assigns

            .. code:: apdl

               B(2,3)='file10',           B(3,3)='file11'

            .. code:: apdl

               B(2,3)='file10',           B(3,3)='file11'

        val4 : str
            If ``Par`` is an array parameter, values ``VAL2`` through ``VAL10`` (up to the last nonblank
            value) are sequentially assigned to the succeeding array elements of the column. Examples:

            .. code:: apdl

               *SET,A(1,4),10,11

            assigns

            .. code:: apdl

               A(1,4)=10, A(2,4)=11

            .. code:: apdl

               A(1,4)=10, A(2,4)=11

            .. code:: apdl

               *SET,B(2,3),'file10','file11'

            assigns

            .. code:: apdl

               B(2,3)='file10',           B(3,3)='file11'

            .. code:: apdl

               B(2,3)='file10',           B(3,3)='file11'

        val5 : str
            If ``Par`` is an array parameter, values ``VAL2`` through ``VAL10`` (up to the last nonblank
            value) are sequentially assigned to the succeeding array elements of the column. Examples:

            .. code:: apdl

               *SET,A(1,4),10,11

            assigns

            .. code:: apdl

               A(1,4)=10, A(2,4)=11

            .. code:: apdl

               A(1,4)=10, A(2,4)=11

            .. code:: apdl

               *SET,B(2,3),'file10','file11'

            assigns

            .. code:: apdl

               B(2,3)='file10',           B(3,3)='file11'

            .. code:: apdl

               B(2,3)='file10',           B(3,3)='file11'

        val6 : str
            If ``Par`` is an array parameter, values ``VAL2`` through ``VAL10`` (up to the last nonblank
            value) are sequentially assigned to the succeeding array elements of the column. Examples:

            .. code:: apdl

               *SET,A(1,4),10,11

            assigns

            .. code:: apdl

               A(1,4)=10, A(2,4)=11

            .. code:: apdl

               A(1,4)=10, A(2,4)=11

            .. code:: apdl

               *SET,B(2,3),'file10','file11'

            assigns

            .. code:: apdl

               B(2,3)='file10',           B(3,3)='file11'

            .. code:: apdl

               B(2,3)='file10',           B(3,3)='file11'

        val7 : str
            If ``Par`` is an array parameter, values ``VAL2`` through ``VAL10`` (up to the last nonblank
            value) are sequentially assigned to the succeeding array elements of the column. Examples:

            .. code:: apdl

               *SET,A(1,4),10,11

            assigns

            .. code:: apdl

               A(1,4)=10, A(2,4)=11

            .. code:: apdl

               A(1,4)=10, A(2,4)=11

            .. code:: apdl

               *SET,B(2,3),'file10','file11'

            assigns

            .. code:: apdl

               B(2,3)='file10',           B(3,3)='file11'

            .. code:: apdl

               B(2,3)='file10',           B(3,3)='file11'

        val8 : str
            If ``Par`` is an array parameter, values ``VAL2`` through ``VAL10`` (up to the last nonblank
            value) are sequentially assigned to the succeeding array elements of the column. Examples:

            .. code:: apdl

               *SET,A(1,4),10,11

            assigns

            .. code:: apdl

               A(1,4)=10, A(2,4)=11

            .. code:: apdl

               A(1,4)=10, A(2,4)=11

            .. code:: apdl

               *SET,B(2,3),'file10','file11'

            assigns

            .. code:: apdl

               B(2,3)='file10',           B(3,3)='file11'

            .. code:: apdl

               B(2,3)='file10',           B(3,3)='file11'

        val9 : str
            If ``Par`` is an array parameter, values ``VAL2`` through ``VAL10`` (up to the last nonblank
            value) are sequentially assigned to the succeeding array elements of the column. Examples:

            .. code:: apdl

               *SET,A(1,4),10,11

            assigns

            .. code:: apdl

               A(1,4)=10, A(2,4)=11

            .. code:: apdl

               A(1,4)=10, A(2,4)=11

            .. code:: apdl

               *SET,B(2,3),'file10','file11'

            assigns

            .. code:: apdl

               B(2,3)='file10',           B(3,3)='file11'

            .. code:: apdl

               B(2,3)='file10',           B(3,3)='file11'

        val10 : str
            If ``Par`` is an array parameter, values ``VAL2`` through ``VAL10`` (up to the last nonblank
            value) are sequentially assigned to the succeeding array elements of the column. Examples:

            .. code:: apdl

               *SET,A(1,4),10,11

            assigns

            .. code:: apdl

               A(1,4)=10, A(2,4)=11

            .. code:: apdl

               A(1,4)=10, A(2,4)=11

            .. code:: apdl

               *SET,B(2,3),'file10','file11'

            assigns

            .. code:: apdl

               B(2,3)='file10',           B(3,3)='file11'

            .. code:: apdl

               B(2,3)='file10',           B(3,3)='file11'

        Notes
        -----
        Assigns values to user-named parameters that can be substituted later in the run. The equivalent
        (and recommended) format is ``Par`` = ``VALUE``, ``VAL2``, ``VAL3`....., ``VAL10``

        which can be used in place of :ref:`starset`, ``Par``,... for convenience.

        This command is valid in any processor.

        Parameters (numeric or character) can be scalars (single valued) or arrays (multiple valued in one,
        two, or three dimensions). An unlimited number of parameter names can be defined in any run. For
        very large numbers of parameters, it is most efficient to define them in alphabetical order.

        Parameter values can be redefined at any time. Array parameters can also be assigned values within a
        do-loop ( ``\*DO`` ) for convenience. Internally programmed do-loop commands are also available with
        the **\*V** ``XX``  commands ( :ref:`vfill` ). Parameter values (except for parameters ending in an
        underscore) can be listed with the :ref:`starstatus` command, displayed via :ref:`starvplot`
        (numeric parameters only), and modified via ``\*VEDIT`` (numeric parameters only).

        Older program-provided macro files can use parameter names that do not begin with an underscore.
        Using these macros embedded in your own macros may cause conflicts if the same parameter names are
        used.

        Parameters can also be resolved in comments created via :ref:`com`. A parameter can be deleted by
        redefining it with a blank ``VALUE``. If the parameter is an array, the entire array is deleted.
        Parameters can also be defined by a response to a query via ``\*ASK`` or from a Mechanical APDL-
        provided
        value via :ref:`get`.

        Array parameters must be dimensioned ( :ref:`dim` ) before being assigned values unless they are the
        result of an array operation or defined using the implied loop convention.

        Undefined scalar parameters are initialized to a near-zero value. Numeric array parameters are
        initialized to zero when dimensioned, and character array parameters are initialized to blank.

        An existing array parameter must be deleted before it can be redimensioned.

        Array parameter names must be followed by a subscript list (enclosed in parentheses) identifying the
        element of the array. The subscript list can have one, two, or three values (separated by commas).
        Typical array parameter elements are A(1,1), NEW_VAL(3,2,5), RESULT(1000). Subscripts for defining
        an array element must be integers (or parameter expressions that evaluate to integers). Non-integer
        values are rounded to the nearest integer value.

        All array parameters are stored as 3D arrays with the unspecified dimensions set to 1. For example,
        the 4th array element of a 1-dimensional array, A(4), is stored as array element A(4,1,1).

        Arrays adhere to standard FORTRAN conventions.

        If the parameter name ``Par`` is input in a numeric argument of a command, the numeric value of the
        parameter (as assigned with :ref:`starset`, :ref:`get`, =, etc.) is substituted into the command at
        that point. Substitution occurs only if the parameter name is used between blanks, commas,
        parentheses, or arithmetic operators (or any combination) in a numeric argument. Substitution can be
        prevented by enclosing the parameter name ``Par`` within single quotes ( ' ), if the parameter is
        alone in the argument; if the parameter is part of an arithmetic expression, the entire expression
        must be enclosed within single quotes to prevent substitution. In either case the character string
        will be used instead of the numeric value (and the string will be taken as 0.0 if it is in a numeric
        argument).

        A forced substitution is available in the text fields of :ref:`title`, :ref:`stitle`, :ref:`tlabel`,
        :ref:`an3d`, :ref:`syp` ( ``ARG1`` -- ``ARG8`` ), and :ref:`abbr` by enclosing the parameter within
        percent (%) signs. Also, parameter substitution can be forced within the file name or extension
        fields of commands having these fields by enclosing the parameter within percent (%) signs. Array
        parameters ( :ref:`dim` ) must include a subscript (within parentheses) to identify the array
        element whose value is to be substituted, such as A(1,3). Out-of-range subscripts result in an error
        message. Non-integer subscripts are allowed when identifying a TABLE array element for substitution.
        A proportional linear interpolation of values among the nearest array elements is performed before
        substitution. Interpolation is done in all three dimensions.

        Interpolation is based upon the assigned index numbers which must be defined when the table is
        filled ( :ref:`dim` ).

        Most alphanumeric arguments permit the use of character parameter substitution. When the parameter
        name ``Par`` input, the alphanumeric value of the parameter is substituted into the command at that
        point. Substitution can be suppressed by enclosing the parameter name within single quotes ( ' ).
        Forced substitution is available in some fields by enclosing the parameter name within percent (%)
        signs. Valid forced substitution fields include command name fields, ``Fname`` (filename) or ``Ext``
        (extension) arguments, :ref:`abbr` command ( ``Abbr`` arguments), :ref:`title` and :ref:`stitle`
        commands ( ``Title`` argument) and :ref:`tlabel` command ( ``Text`` argument). Character parameter
        substitution is also available in the ``\*ASK``, :ref:`an3d`, :ref:`cfwrite`, ``\*IF``, ``\*ELSEIF``,
        :ref:`msg`, :ref:`starset`, :ref:`use`, :ref:`vread`, and :ref:`vwrite` commands. Character array
        parameters must include a subscript (within parentheses) to identify the array element whose value
        is to be substituted.

        If a parameter operation expression is input in a numeric argument, the numeric value of the
        expression is substituted into the command at that point. Allowable operation expressions are of the
        form

        .. code:: apdl

           E1oE2oE3...oE10

        where E1, E2, etc. are expressions connected by operators (o). The allowable operations (o) are

        .. code:: apdl

           + - * / ** < >

        For example,

        .. code:: apdl

           A+B**C/D*E

        is a valid operation expression. The

        .. code:: apdl

           *

        represents multiplication and the

        .. code:: apdl

           **

        represents exponentiation.

        Exponentiation of a negative number (without parentheses) to an integer power follows standard
        FORTRAN hierarchy conventions; that is, the positive number is exponentiated and then the sign is
        attached. Thus, -4**2 is evaluated as -16. If parentheses are applied, such as (-4)**2, the result
        is 16.

        A parameter is evaluated as a number within parentheses before exponentiation. Exponentiation of a
        negative number to a non-integer power is performed by exponentiating the positive number and
        prepending the minus sign, for example, -4**2.3 is -(4**2.3). The < and > operators allow
        conditional substitution. For example, E1<E2 substitutes the value of E1 if the comparison is true
        or the value of E2 if the comparison is false.

        Do not use spaces around operation symbols, as " *" (a space and a star) makes the remainder of the
        line a comment. Operation symbols (or symbols and signs) cannot be immediately adjacent to each
        other. Parentheses can be used to separate symbols and signs, to determine a hierarchy of
        operations, or for clarity. For example, use A**(-B) instead of A**-B. Numbers ending with +0nn or
        -0nn are assumed to be of exponential form (as written on files by some computer systems) so that
        123-002 is 123E-2 while 123-2 is 121. Avoid inputting this form of exponential data directly. The
        default hierarchy follows the standard FORTRAN conventions, namely:

        operations in parentheses (innermost first) then exponentiation (right to left) then multiplication
        or division (left to right) then unary association (such as +A or -A) then addition or subtraction
        (left to right) then logical evaluations (left to right).

        Expressions (E) can be a constant, a parameter, a function, or another operation expression (of the
        form E1oE2oE3...oE10). Functions are of the form FTN(A) where the argument (A) can itself be of the
        form E1oE2oE3...oE10. Operations are recursive to a level of four deep (three levels of internally
        nested parentheses). Iterative floating point parameter arithmetic should not be used for high
        precision input because of the accumulated numerical round off-error. Up to 10 expressions are
        accepted within a set of parenthesis.

        Valid functions (which are based on standard FORTRAN functions where possible) are:

        InformalTables need to be added.
        Function arguments ( X, Y, etc.) must be enclosed within parentheses and can be numeric values,
        parameters, or expressions. Input arguments for angular functions must evaluate to radians by
        default. Output from angular functions are also in radians by default. See :ref:`afun` to use
        degrees instead of radians for the angular functions. See :ref:`vfun` for applying these parameter
        functions to a sequence of array elements. Additional functions, called get functions, are described
        via :ref:`get`.
        """
        command = f"*SET,{par},{value},{val2},{val3},{val4},{val5},{val6},{val7},{val8},{val9},{val10}"
        return self.run(command, **kwargs)

    def tread(
        self, par: str = "", fname: str = "", ext: str = "", nskip: str = "", **kwargs
    ):
        r"""Reads data from an external file into a table array parameter.

        Mechanical APDL Command: `\*TREAD <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_TREAD.html>`_

        Parameters
        ----------
        par : str
            Table array parameter name as defined by the :ref:`dim` command.

        fname : str
            File name and directory path (248 characters maximum, including the characters needed for the
            directory path). An unspecified directory path defaults to the working directory; in this case,
            you can use all 248 characters for the file name. File name has no default.

        ext : str
            Filename extension (eight-character maximum). Extension has no default.

        nskip : str
            Number of comment lines at the beginning of the file being read that will be skipped during the
            reading. Default = 0.

        Notes
        -----
        Use this command to read in a table of data from an external file into a table array parameter. The
        external file may be created using a text editor or by an external application or program. To be
        used by :ref:`tread`, the external file's encoding format must be UTF-8, and the file must be in
        tab-delimited, blank-delimited, or comma-delimited format. The TABLE type array parameter must be
        defined before you can read in an external file. See :ref:`dim` for more information.

        This command is not applicable to 4- or 5-D tables.
        """
        command = f"*TREAD,{par},{fname},{ext},,{nskip}"
        return self.run(command, **kwargs)

    def taxis(
        self,
        parmloc: str = "",
        naxis: str = "",
        val1: str = "",
        val2: str = "",
        val3: str = "",
        val4: str = "",
        val5: str = "",
        val6: str = "",
        val7: str = "",
        val8: str = "",
        val9: str = "",
        val10: str = "",
        **kwargs,
    ):
        r"""Defines table index numbers.

        Mechanical APDL Command: `\*TAXIS <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_TAXIS.html>`_

        Parameters
        ----------
        parmloc : str
            Name and starting location in the table array parameter for indexing. Indexing occurs along the
            axis defined with ``nAxis``.

        naxis : str
            Axis along which indexing occurs. Valid labels are:

            * ``1`` - Corresponds to Row. Default.

            * ``2`` - Corresponds to Column.

            * ``3`` - Corresponds to Plane.

            * ``4`` - Corresponds to Book.

            * ``5`` - Corresponds to Shelf.

            * ``ALL`` - Lists all index numbers. Valid only if ``Val1`` = LIST.

        val1 : str
            Values of the index numbers for the axis ``nAxis``, starting from the table array parameter
            location ``ParmLoc``. You can define up to ten values.

            To list the index values specified with ``nAxis``, issue ``Val1`` = LIST. If ``Val1`` = LIST,
            ``Val2`` - ``Val10`` are ignored.

        val2 : str
            Values of the index numbers for the axis ``nAxis``, starting from the table array parameter
            location ``ParmLoc``. You can define up to ten values.

            To list the index values specified with ``nAxis``, issue ``Val1`` = LIST. If ``Val1`` = LIST,
            ``Val2`` - ``Val10`` are ignored.

        val3 : str
            Values of the index numbers for the axis ``nAxis``, starting from the table array parameter
            location ``ParmLoc``. You can define up to ten values.

            To list the index values specified with ``nAxis``, issue ``Val1`` = LIST. If ``Val1`` = LIST,
            ``Val2`` - ``Val10`` are ignored.

        val4 : str
            Values of the index numbers for the axis ``nAxis``, starting from the table array parameter
            location ``ParmLoc``. You can define up to ten values.

            To list the index values specified with ``nAxis``, issue ``Val1`` = LIST. If ``Val1`` = LIST,
            ``Val2`` - ``Val10`` are ignored.

        val5 : str
            Values of the index numbers for the axis ``nAxis``, starting from the table array parameter
            location ``ParmLoc``. You can define up to ten values.

            To list the index values specified with ``nAxis``, issue ``Val1`` = LIST. If ``Val1`` = LIST,
            ``Val2`` - ``Val10`` are ignored.

        val6 : str
            Values of the index numbers for the axis ``nAxis``, starting from the table array parameter
            location ``ParmLoc``. You can define up to ten values.

            To list the index values specified with ``nAxis``, issue ``Val1`` = LIST. If ``Val1`` = LIST,
            ``Val2`` - ``Val10`` are ignored.

        val7 : str
            Values of the index numbers for the axis ``nAxis``, starting from the table array parameter
            location ``ParmLoc``. You can define up to ten values.

            To list the index values specified with ``nAxis``, issue ``Val1`` = LIST. If ``Val1`` = LIST,
            ``Val2`` - ``Val10`` are ignored.

        val8 : str
            Values of the index numbers for the axis ``nAxis``, starting from the table array parameter
            location ``ParmLoc``. You can define up to ten values.

            To list the index values specified with ``nAxis``, issue ``Val1`` = LIST. If ``Val1`` = LIST,
            ``Val2`` - ``Val10`` are ignored.

        val9 : str
            Values of the index numbers for the axis ``nAxis``, starting from the table array parameter
            location ``ParmLoc``. You can define up to ten values.

            To list the index values specified with ``nAxis``, issue ``Val1`` = LIST. If ``Val1`` = LIST,
            ``Val2`` - ``Val10`` are ignored.

        val10 : str
            Values of the index numbers for the axis ``nAxis``, starting from the table array parameter
            location ``ParmLoc``. You can define up to ten values.

            To list the index values specified with ``nAxis``, issue ``Val1`` = LIST. If ``Val1`` = LIST,
            ``Val2`` - ``Val10`` are ignored.

        Notes
        -----
        :ref:`taxis` is a convenient method to define table index values. These values reside in the zero
        column, row, etc. Instead of filling values in these zero location spots, use the :ref:`taxis`
        command. For example,

        .. code:: apdl

           *TAXIS,longtable(1,4,1,1),2,1.0,2.2,3.5,4.7,5.9

        would fill index values 1.0, 2.2, 3.5, 4.7, and 5.9 in ``nAxis`` 2 (column location), starting at
        location 4.

        To list index numbers, issue :ref:`taxis`, ``ParmLoc``, ``nAxis``, LIST, where ``nAxis`` = 1 through
        5 or ALL.
        """
        command = f"*TAXIS,{parmloc},{naxis},{val1},{val2},{val3},{val4},{val5},{val6},{val7},{val8},{val9},{val10}"
        return self.run(command, **kwargs)

    def dim(
        self,
        par: str = "",
        type_: str = "",
        imax: str = "",
        jmax: str = "",
        kmax: str = "",
        var1: str = "",
        var2: str = "",
        var3: str = "",
        csysid: str = "",
        **kwargs,
    ):
        r"""Defines an array parameter and its dimensions.

        Mechanical APDL Command: `\*DIM <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_DIM.html>`_

        Parameters
        ----------
        par : str
            Name of parameter to be dimensioned. See :ref:`starset` for name restrictions.

        type_ : str
            Array type:

            * ``ARRAY`` - Arrays are similar to standard FORTRAN arrays (indices are integers) (default). Index numbers for
              the rows, columns, and planes are sequential values beginning with one. Used for 1-, 2-, or 3D
              arrays.

            * ``ARR4`` - Same as ARRAY, but used to specify 4-D arrays.

            * ``ARR5`` - Same as ARRAY, but used to specify 5-D arrays.

            * ``CHAR`` - Array entries are character strings (up to 8 characters each). Index numbers for rows, columns, and
              planes are sequential values beginning with one.

            * ``TABLE`` - Array indices are real (non-integer) numbers which must be defined when filling the table. Index
              numbers for the rows and columns are stored in the zero column and row "array elements" and are
              initially assigned a near-zero value. Index numbers must be in ascending order and are used only for
              retrieving an array element. When retrieving an array element with a real index that does not match
              a specified index, linear interpolation is done among the nearest indices and the corresponding
              array element values ( :ref:`starset` ). Used for 1-, 2-, or 3D tables.

            * ``TAB4`` - Same as TABLE, but used to specify 4-D tables.

            * ``TAB5`` - Same as TABLE, but used to specify 5-D tables.

            * ``STRING`` - Array entries are character strings (up to IMAX each). Index numbers for columns and planes are
              sequential values beginning with 1. Row index is character position in string.

        imax : str
            Extent of first dimension (row). (For ``Type`` = STRING, ``IMAX`` is rounded up to the next
            multiple of eight and has a limit of 248). Default = 1.

        jmax : str
            Extent of second dimension (column). Default = 1.

        kmax : str
            Extent of third dimension (plane). Default = 1.

        var1 : str
            Variable name corresponding to the first dimension (row) for ``Type`` = TABLE, TAB4, or TAB5.
            Default = Row.

        var2 : str
            Variable name corresponding to the second dimension (column) for ``Type`` = TABLE, TAB4, or
            TAB5. Default = Column.

        var3 : str
            Variable name corresponding to the third dimension (plane) for ``Type`` = TABLE, TAB4, TAB5.
            Default = Plane.

        csysid : str
            An integer corresponding to the coordinate system ID number. Default = 0 (global Cartesian).

        Notes
        -----
        Up to three dimensions (row, column, and plane) may be defined using ARRAY and TABLE. Use ARR4,
        ARR5, TAB4, and TAB5 to define up to five dimensions (row, column, plane, book, and shelf). An index
        number is associated with each row, column, and plane. For array and table type parameters, element
        values are initialized to zero. For character and string parameters, element values are initialized
        to (blank). A defined parameter must be deleted ( :ref:`starset` ) before its dimensions can be
        changed. Scalar (single valued) parameters should not be dimensioned. :ref:`dim`,A,,3 defines a
        vector array with elements A(1), A(2), and A(3). :ref:`dim`,B,,2,3 defines a 2x3 array with elements
        B(1,1), B(2,1), B(1,2), B(2,2), B(1,3), and B(2,3). Use :ref:`starstatus`, ``Par`` to display
        elements of array ``Par``. You can write formatted data files (tabular formatting) from data held in
        arrays through the :ref:`vwrite` command.

        If you use table parameters to define boundary conditions, then ``Var1``, ``Var2``, and/or ``Var3``
        can either specify a primary variable (listed in ) or can be an independent parameter. If specifying
        an independent parameter, then you must define an additional table for the independent parameter.
        The additional table must have the same name as the independent parameter and may be a function of
        one or more primary variables or another independent parameter. All independent parameters must
        relate to a primary variable.

        Tabular load arrays can be defined in both global Cartesian (default), cylindrical, spherical, or
        local (see below) coordinate systems by specifying ``CSYSID``, as defined in :ref:`local`.
        Coordinate system ``CSYSID`` must exist prior to issuing the :ref:`dim` command.

        **The following constraints apply when specifying a local coordinate system for your tabular
        loads:**

        Only Cartesian, cylindrical and spherical coordinate systems are supported
        Angle values for Y in cylindrical or spherical coordinate systems must be input in degrees and must
        be positive values between 0 and 360 degrees (0 :math:``  Y  :math:``  360)
        Angle values for Z in spherical coordinate system must be input in degrees and must be positive
        values between -90 and +90 ( -90 :math:``  Z  :math:``  90)

        If specifying a 4- or 5-D array or table, four additional fields ( ``LMAX``, ``MMAX``, ``Var4``, and
        ``Var5`` ) are available. Thus, for a 4-D table, the command syntax would be:

        .. code:: apdl

           *DIM,Par,Type,IMAX,JMAX,KMAX,LMAX,Var1,Var2,Var3,Var4,CSYSID

        For a 5-D table, the command syntax is:

        .. code:: apdl

           *DIM,Par,Type,IMAX,JMAX,KMAX,LMAX,MMAX,Var1,Var2,Var3,Var4,Var5,CSYSID

        You cannot create or edit 4- or 5-D arrays or tables via the GUI.

        For more information, see `Array Parameters
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_apdl/Hlp_P_APDL3_11.html#ansys.guide.apdl.ch3.s11.9>`_

        **\*DIM - Primary Variables**

        .. flat-table::
           :header-rows: 1

           * - Primary Variable
             - Label for ``Var1, Var2, Var3, Var4, Var5``
           * - Time
             - TIME
           * - Frequency
             - FREQ
           * - X-coordinate location
             - X
           * - Y-coordinate location
             - Y
           * - Z-coordinate location
             - Z
           * - Temperature
             - TEMP
           * - Velocity
             - VELOCITY
           * - Pressure
             - PRESSURE [ ]
           * - Geometric gap/penetration
             - GAP
           * - Cyclic sector number
             - SECTOR
           * - Amplitude of the rotational velocity vector
             - OMEGS
           * - Eccentricity
             - ECCENT
           * - Phase shift
             - THETA
           * - Element number
             - ELEM
           * - Node number
             - NODE
           * - Concentration
             - CONC


        Specify PRESSURE as the independent variable (not PRES).

        The X, Y, and Z coordinate locations listed above are valid in global Cartesian, or local
        (Cartesian, cylindrical and spherical) coordinate systems. The VELOCITY label is applicable only to
        the calculated fluid velocity in element FLUID116.

        When using PRESSURE as a primary variable, the underlying element must have the pressure DOF
        associated with it, or it must be a supported contact element.

        The gap/penetration label (GAP) is only used for defining certain contact element real constants.

        The frequency label (FREQ) is valid for harmonic analyses only.

        The node and element labels (NODE and ELEM) allow you to use node and element numbers as primary
        variables, and their axis values should be integers.

        The OMEGS, ECCENT, and THETA primary variables only apply to the COMBI214 element. The amplitude of
        the rotational velocity (OMEGS) is an absolute value, so only positive values of OMEGS are valid.
        The eccentricity (ECCENT) and phase shift (THETA) labels are only valid for nonlinear analyses.

        If you use table parameters to define boundary conditions, the table names ( ``Par`` ) must not
        exceed 32 characters.

        In thermal analyses, if you apply tabular loads as a function of temperature but the rest of the
        model is linear (for example, includes no temperature-dependent material properties or radiation ),
        you should turn on Newton-Raphson iterations ( :ref:`nropt`,FULL) to evaluate the temperature-
        dependent tabular boundary conditions correctly.

        This command is valid in any processor.
        """
        command = (
            f"*DIM,{par},{type_},{imax},{jmax},{kmax},{var1},{var2},{var3},{csysid}"
        )
        return self.run(command, **kwargs)

    def starvget(
        self,
        parr: str = "",
        entity: str = "",
        entnum: str = "",
        item1: str = "",
        it1num: str = "",
        item2: str = "",
        it2num: str = "",
        kloop: str = "",
        **kwargs,
    ):
        r"""Retrieves values and stores them into an array parameter.

        Mechanical APDL Command: `\*VGET <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_VGET_st.html>`_

        Parameters
        ----------
        parr : str
            The name of the resulting vector array parameter. See :ref:`starset` for name restrictions. The
            program creates the array parameter if it does not exist.

        entity : str
            Entity keyword. Valid keywords are NODE, ELEM, KP, LINE, AREA, VOLU, etc. as shown for
            ``Entity`` = in the tables below.

        entnum : str
            The number of the entity (as shown for ``ENTNUM`` = in the tables below).

        item1 : str
            The name of a particular item for the given entity. Valid items are as shown in the ``Item1``
            columns of the tables below.

        it1num : str
            The number (or label) for the specified ``Item1`` (if any). Valid ``IT1NUM`` values are as shown
            in the ``IT1NUM`` columns of the tables below. Some ``Item1`` labels do not require an
            ``IT1NUM`` value.

        item2 : str
            A second set of item labels and numbers to further qualify the item for which data is to be
            retrieved. Most items do not require this level of information.

        it2num : str
            A second set of item labels and numbers to further qualify the item for which data is to be
            retrieved. Most items do not require this level of information.

        kloop : str
            Field to be looped on:

            * ``0 or 2`` - Loop on the ``ENTNUM`` field (default).

            * ``3`` - Loop on the ``Item1`` field.

            * ``4`` - Loop on the ``IT1NUM`` field. Successive items are as shown with ``IT1NUM``.

            * ``5`` - Loop on the ``Item2`` field.

            * ``6`` - Loop on the ``IT2NUM`` field. Successive items are as shown with ``IT2NUM``.

        Notes
        -----
        Retrieves values for specified items and stores the values in an output vector of a user-named array
        parameter according to: ``ParR`` = f( ``Entity``, ``ENTNUM``, ``Item1``, ``IT1NUM``, ``Item2``,
        ``IT2NUM`` )

        where (f) is the :ref:`get` function; ``Entity``, ``Item1``, and ``Item2`` are keywords; and
        ``ENTNUM``, ``IT1NUM``, and ``IT2NUM`` are numbers or labels corresponding to the keywords. Looping
        continues over successive entity numbers ( ``ENTNUM`` ) for the ``KLOOP`` default. For example,
        :ref:`starvget`,A(1),ELEM,5,CENT,X returns the centroid x-location of element 5 and stores the
        result in the first location of A. Retrieving continues with element 6, 7, 8, etc., regardless of
        whether the element exists or is selected, until successive array locations are filled. Use
        :ref:`vlen` or :ref:`vmask` to skip locations. Absolute values and scale factors may be applied to
        the result parameter ( :ref:`vabs`, :ref:`vfact` ). Results may be cumulative ( :ref:`vcum` ). See
        the :ref:`voper` command for general details. Results can be put back into an analysis by writing a
        file of the desired input commands with the :ref:`vwrite` command. See also the :ref:`starvput`
        command.

        Both :ref:`get` and :ref:`starvget` retrieve information from the active data stored in memory. The
        database is often the source, and sometimes the information is retrieved from common memory blocks
        that Mechanical APDL uses to manipulate information. Although POST1 and POST26 operations use a
        :file:`\*.rst` file, GET data is accessed from the database or from the common blocks. Get
        operations do not access the :file:`\*.rst` file directly.

        The :ref:`starvget` command retrieves both the unprocessed real and the imaginary parts (original
        and duplicate sector nodes and elements) of a `cyclic symmetry
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cycsym/cycsym_example.html>`_ solution.

        Each of the sections for accessing \*VGET parameters are shown in the following order:

        `\*VGET PREP7 Items
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cmd/Hlp_C_VGET_st.html#vget.prep7.tlab>`_
        `\*VGET POST1 Items
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cmd/Hlp_C_VGET_st.html#vget.post1.node.ndof>`_

        This command is valid in any processor.
        """
        command = (
            f"*VGET,{parr},{entity},{entnum},{item1},{it1num},{item2},{it2num},{kloop}"
        )
        return self.run(command, **kwargs)

    def vread(
        self,
        parr: str = "",
        fname: str = "",
        ext: str = "",
        label: str = "",
        n1: str = "",
        n2: str = "",
        n3: str = "",
        nskip: str = "",
        **kwargs,
    ):
        r"""Reads data and produces an array parameter vector or matrix.

        Mechanical APDL Command: `\*VREAD <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_VREAD.html>`_

        Parameters
        ----------
        parr : str
            The name of the resulting array parameter vector. See :ref:`starset` for name restrictions. The
            parameter must exist as a dimensioned array ( :ref:`dim` ). String arrays are limited to a
            maximum of 8 characters.

        fname : str
            File name and directory path (248 characters maximum, including the characters needed for the
            directory path). An unspecified directory path defaults to the working directory; in this case,
            you can use all 248 characters for the file name. If the ``Fname`` field is left blank, reading
            continues from the current input device, such as the terminal.

        ext : str
            Filename extension (eight-character maximum).

        label : str
            Can take a value of IJK, IKJ, JIK, JKI, KIJ, KJI, or blank (IJK).

        n1 : str
            Read as ((( ``ParR`` (i,j,k), k = 1,n1), i = 1, n2), j = 1, n3) for ``Label`` = KIJ. ``n2`` and
            ``n3`` default to 1.

        n2 : str
            Read as ((( ``ParR`` (i,j,k), k = 1,n1), i = 1, n2), j = 1, n3) for ``Label`` = KIJ. ``n2`` and
            ``n3`` default to 1.

        n3 : str
            Read as ((( ``ParR`` (i,j,k), k = 1,n1), i = 1, n2), j = 1, n3) for ``Label`` = KIJ. ``n2`` and
            ``n3`` default to 1.

        nskip : str
            Number of lines at the beginning of the file being read that will be skipped during the reading.
            Default = 0.

        Notes
        -----
        Reads data from a file and fills in an array parameter vector or matrix. Data are read from a
        formatted file or, if the menu is off ( :ref:`menu`,OFF) and ``Fname`` is blank, from the next input
        lines. The format of the data to be read must be input immediately following the :ref:`vread`
        command. The format specifies the number of fields to be read per record, the field width, and the
        placement of the decimal point (if none specified in the value). The read operation follows the
        available FORTRAN FORMAT conventions of the system (see your system FORTRAN manual). Any standard
        FORTRAN real format (such as (4F6.0), (E10.3,2X,D8.2), etc.) or alphanumeric format (A) may be used.
        Alphanumeric strings are limited to a maximum of 8 characters for any field (A8). For storage of
        string arrays greater than 8 characters, the \*SREAD command can be used. Integer (I) and list-
        directed (\2) descriptors may not be used. The parentheses must be included in the format and the
        format must not exceed 80 characters (including parentheses). The input line length is limited to
        128 characters.

        A starting array element number must be defined for the result array parameter vector (numeric or
        character). For example, entering these two lines:

        .. code:: apdl

           *VREAD,A(1),ARRAYVAL
           (2F6.0)

        will read two values from each line of file ARRAYVAL and assign the values to A(1), A(2), A(3), etc.
        Reading continues until successive row elements ( :ref:`vlen`, :ref:`vmask`, :ref:`dim` ) are
        filled.

        For an array parameter matrix, a starting array element row and column number must be defined. For
        example, entering these two lines:

        .. code:: apdl

           *VREAD,A(1,1),ARRAYVAL,,,IJK,10,2
           (2F6.0)

        will read two values from each line of file ARRAYVAL and assign the values to A(1,1), A(2,1),
        A(3,1), etc. Reading continues until ``n1`` (10) successive row elements are filled. Once the
        maximum row number is reached, subsequent data will be read into the next column (for example,
        A(1,2), A(2,2), A(3,2), etc.)

        For numerical parameters, absolute values and scale factors may be applied to the result parameter (
        :ref:`vabs`, :ref:`vfact` ). Results may be cumulative ( :ref:`vcum` ). See the :ref:`voper` command
        for details. If you are in the GUI the :ref:`vread` command must be contained in an externally
        prepared file read into Mechanical APDL (that is, :ref:`use`, :ref:`input`, etc.).

        This command is not applicable to 4- or 5-D arrays.

        This command is valid in any processor.
        """
        command = f"*VREAD,{parr},{fname},{ext},,{label},{n1},{n2},{n3},{nskip}"
        return self.run(command, **kwargs)

    def vfill(
        self,
        parr: str = "",
        func: str = "",
        con1: str = "",
        con2: str = "",
        con3: str = "",
        con4: str = "",
        con5: str = "",
        con6: str = "",
        con7: str = "",
        con8: str = "",
        con9: str = "",
        con10: str = "",
        **kwargs,
    ):
        r"""Fills an array parameter.

        Mechanical APDL Command: `\*VFILL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_VFILL.html>`_

        Parameters
        ----------
        parr : str
            The name of the resulting numeric array parameter vector. See :ref:`starset` for name
            restrictions.

        func : str
            Fill function:

            * ``DATA`` - Assign specified values ``CON1``, ``CON2``, etc. to successive array elements. Up to 10 assignments
              may be made at a time. Any CON values after a blank CON value are ignored.

            * ``RAMP`` - Assign ramp function values: ``CON1`` +((n-1)\* ``CON2`` ), where n is the loop number ( :ref:`vlen` ). To specify a constant function (no ramp), set ``CON2`` to zero.

            * ``RAND`` - Assign random number values based on a uniform distribution RAND( ``CON1``, ``CON2`` ), where:

              ``CON1`` is the lower bound (defaults to 0.0) ``CON2`` is the upper bound (defaults to 1.0)

            * ``GDIS`` - Assign random sample of Gaussian distributions GDIS( ``CON1``, ``CON2`` ) where:

              ``CON1`` is the mean (defaults to 0.0) ``CON2`` is the standard deviation (defaults to 1.0)

            * ``TRIA`` - Assigns random number values based on a triangular distribution TRIA( ``CON1``, ``CON2``, ``CON3`` )
              where:

              ``CON1`` is the lower bound (defaults to 0.0) ``CON2`` is the location of the peak value ( ``CON1``
              ≤ ``CON2`` ≤ ``CON3`` ; ``CON2`` defaults to 0 if ``CON1`` ≤ 0 ≤ ``CON3``, ``CON1`` if 0 ≤ ``CON1``,
              or ``CON3`` if ``CON3`` ≤ 0) ``CON3`` is the upper bound (defaults to 1.0 + ``CON1`` if ``CON1`` ≥ 0
              or 0.0 if ``CON1`` ≤ 0)

            * ``BETA`` - Assigns random number values based on a beta distribution BETA( ``CON1``, ``CON2``, ``CON3``,
              ``CON4`` ) where:

              ``CON1`` is the lower bound (defaults to 0.0) ``CON2`` is the upper bound (defaults to 1.0 +
              ``CON1`` if ``CON1`` ≥ 0 or 0.0 if ``CON1`` ≤ 0) ``CON3`` and ``CON4`` are the alpha and beta
              parameters, respectively, of the beta function. Alpha and beta must both be positive; they default
              to 1.0.

            * ``GAMM`` - Assigns random number values based on a gamma distribution: GAMM( ``CON1``, ``CON2``, ``CON3`` )
              where:

              ``CON1`` is the lower bound (defaults to 0.0) ``CON2`` and ``CON3`` are the alpha and beta
              parameters, respectively, of the gamma function. Alpha and beta must both be positive; they default
              to 1.0.

            * ``RIGID`` - Generates the rigid body modes with respect to the reference point coordinates ( ``CON1``, ``CON2``,
              ``CON3`` ). The dimensions of the array parameter ``ParR`` are (dim 1,dim 2 ) where dim 1 is the
              maximum node number (including internal nodes but excluding orientation nodes ) multiplied by the
              number of degrees of freedom, and dim

               2 is the number of rigid body modes (which corresponds to the number of structural degrees of
              freedom).

            * ``CLUSTER`` - Generates excitation frequencies with clustering option CLUSTER( ``CON1``, ``CON2``, ``CON3``,
              ``CON4``, ``%CON5%`` ) where:

              ``CON1`` is the lower end of the frequency range in Hz (0 < ``CON1`` ) ``CON2`` is the upper end of
              the frequency range in Hz ( ``CON1`` < ``CON2`` ) ``CON3`` is the number of points on each side of
              the natural frequency (4 ≤ ``CON3`` ≤ 20, defaults to 4) ``CON4`` is the constant damping ratio
              value or an array parameter (size NFR) specifying the damping ratios (if zero or blank, defaults to
              constant damping ratio of 0.005) ``CON5`` is an array parameter (size NFR) specifying the natural
              frequencies in Hz The dimension of the resulting array parameter ParR is less than 2+NFR\2(2*
              ``CON3`` +1) where NFR is the number of natural frequencies defined in ``CON5``.

        con1 : str
            Constants used with above functions.

        con2 : str
            Constants used with above functions.

        con3 : str
            Constants used with above functions.

        con4 : str
            Constants used with above functions.

        con5 : str
            Constants used with above functions.

        con6 : str
            Constants used with above functions.

        con7 : str
            Constants used with above functions.

        con8 : str
            Constants used with above functions.

        con9 : str
            Constants used with above functions.

        con10 : str
            Constants used with above functions.

        Notes
        -----
        Operates on input data and produces one output array parameter vector according to: ``ParR`` = f(
        ``CON1``, ``CON2``,...)

        where the functions (f) are described above. Operations use successive array elements ( :ref:`vlen`,
        :ref:`vmask` ) with the default being all successive elements. For example, :ref:`vfill`,A,RAMP,1,10
        assigns A(1) = 1.0, A(2) = 11.0, A(3) = 21.0, etc. :ref:`vfill`,B(5,1),DATA,1.5,3.0 assigns B(5,1) =
        1.5 and B(6,1) = 3.0. Absolute values and scale factors may be applied to the result parameter (
        :ref:`vabs`, :ref:`vfact` ). Results may be cumulative ( :ref:`vcum` ). See the :ref:`voper` command
        for details.

        This command is valid in any processor.
        """
        command = f"*VFILL,{parr},{func},{con1},{con2},{con3},{con4},{con5},{con6},{con7},{con8},{con9},{con10}"
        return self.run(command, **kwargs)

    def get(
        self,
        par: str = "",
        entity: str = "",
        entnum: str = "",
        item1: str = "",
        it1num: str = "",
        item2: str = "",
        it2num: str = "",
        **kwargs,
    ):
        r"""Retrieves a value and stores it as a scalar parameter or part of an array parameter.

        Mechanical APDL Command: `\*GET <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_GET.html>`_

        Parameters
        ----------
        par : str
            The name of the resulting parameter. See :ref:`starset` for name restrictions.

        entity : str
            Entity keyword. Valid keywords are NODE, ELEM, KP, LINE, AREA, VOLU, etc., as shown for
            ``Entity`` = in the tables below.

        entnum : str
            The number or label for the entity (as shown for ``ENTNUM`` = in the tables below). In some
            cases, a zero (or blank) ``ENTNUM`` represents all entities of the set.

        item1 : str
            The name of a particular item for the given entity. Valid items are as shown in the ``Item1``
            columns of the tables below.

        it1num : str
            The number (or label) for the specified ``Item1`` (if any). Valid ``IT1NUM`` values are as shown
            in the ``IT1NUM`` columns of the tables below. Some ``Item1`` labels do not require an
            ``IT1NUM`` value.

        item2 : str
            A second set of item labels and numbers to further qualify the item for which data are to be
            retrieved. Most items do not require this level of information.

        it2num : str
            A second set of item labels and numbers to further qualify the item for which data are to be
            retrieved. Most items do not require this level of information.

        Notes
        -----
        :ref:`get` retrieves a value for a specified item and stores the value as a scalar parameter, or as
        a value in a user-named array parameter. An item is identified by various keyword, label, and number
        combinations. Usage is similar to the :ref:`starset` command except that the parameter values are
        retrieved from previously input or calculated results.

        :ref:`get` Usage
        :ref:`get`,A,ELEM,5,CENT,X returns the centroid x location of element 5 and stores the result as
        parameter A.

        :ref:`get` command operations, and corresponding get functions, return values in the active
        coordinate system ( :ref:`csys` for input data or :ref:`rsys` for results data) unless stated
        otherwise.

        A get function is an alternative in-line function that can be used instead of the :ref:`get` command
        to retrieve a value. For more information, see.

        Both :ref:`get` and :ref:`starvget` retrieve information from the active data stored in memory. The
        database is often the source, and sometimes the information is retrieved from common memory blocks
        that the program uses to manipulate information. Although POST1 and POST26 operations use a
        :file:`\*.rst` file, :ref:`get` data is accessed from the database or from the common blocks. Get
        operations do not access the :file:`\*.rst` file directly. For repeated gets of sequential items,
        such as from a series of elements, see the :ref:`starvget` command.

        Most items are stored in the database after they are calculated and are available anytime
        thereafter. Items are grouped according to where they are usually first defined or calculated.
        Preprocessing data will often not reflect the calculated values generated from section data. Do not
        use :ref:`get` to obtain data from elements that use calculated section data, such as beams or
        shells.

        When the value retrieved by :ref:`get` is a component name, the resulting character parameter is
        limited to 32 characters. If the component name is longer than 32 characters, the remaining
        characters are ignored.

        Most of the general items listed below are available from all modules. Each of the sections for
        accessing :ref:`get` parameters are shown in the following order:

        The :ref:`get` command is valid in any processor.
        """
        command = f"*GET,{par},{entity},{entnum},{item1},{it1num},{item2},{it2num}"
        return self.run(command, **kwargs)
