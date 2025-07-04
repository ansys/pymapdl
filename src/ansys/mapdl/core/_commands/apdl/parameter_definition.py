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

        .. warning::

           This function contains specificities regarding the argument definitions.
           Please refer to the `command documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_AFUN.html>`_
           for further explanations.

        **Argument Descriptions**

        .. _a-AFUN_argdescript:

        * ``lab : str`` - Specifies the units to be used:

          * ``RAD`` - Use radians for input and output of parameter angular functions (default).

          * ``DEG`` - Use degrees for input and output of parameter angular functions.

          * ``STAT`` - Show current setting (DEG or RAD) for this command.

        .. _a-AFUN_default:

        Use radians for input or output of parameter angular functions.

        .. _a-AFUN_notes:

        Only the SIN, COS, TAN, ASIN, ACOS, ATAN, ATAN2, ANGLEK, and ANGLEN functions ( :ref:`starset`,
        :ref:`vfun` ) are affected by this command.
        """
        command = f"*AFUN,{lab}"
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

            * ``ARRAY`` - Arrays are similar to standard FORTRAN arrays (indices are integers) (default). Index
              numbers for the rows, columns, and planes are sequential values beginning with one. Used for 1-, 2-,
              or 3D arrays.

            * ``ARR4`` - Same as ARRAY, but used to specify 4-D arrays.

            * ``ARR5`` - Same as ARRAY, but used to specify 5-D arrays.

            * ``CHAR`` - Array entries are character strings (up to 8 characters each). Index numbers for rows,
              columns, and planes are sequential values beginning with one.

            * ``TABLE`` - Array indices are real (non-integer) numbers which must be defined when filling the
              table. Index numbers for the rows and columns are stored in the zero column and row "array elements"
              and are initially assigned a near-zero value. Index numbers must be in ascending order and are used
              only for retrieving an array element. When retrieving an array element with a real index that does
              not match a specified index, linear interpolation is done among the nearest indices and the
              corresponding array element values ( :ref:`starset` ). Used for 1-, 2-, or 3D tables.

            * ``TAB4`` - Same as TABLE, but used to specify 4-D tables.

            * ``TAB5`` - Same as TABLE, but used to specify 5-D tables.

            * ``STRING`` - Array entries are character strings (up to IMAX each). Index numbers for columns and
              planes are sequential values beginning with 1. Row index is character position in string.

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

        .. warning::

           This function contains specificities regarding the argument definitions.
           Please refer to the `command documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_DIM.html>`_
           for further explanations.

        **Argument Descriptions**

        .. _a-DIM_argdescript:

        * ``par : str`` - Name of parameter to be dimensioned. See :ref:`starset` for name restrictions.

        * ``type_ : str`` - Array type:

          * ``ARRAY`` - Arrays are similar to standard FORTRAN arrays (indices are integers) (default). Index
            numbers for the rows, columns, and planes are sequential values beginning with one. Used for 1-, 2-,
            or 3D arrays.

          * ``ARR4`` - Same as ARRAY, but used to specify 4-D arrays.

          * ``ARR5`` - Same as ARRAY, but used to specify 5-D arrays.

          * ``CHAR`` - Array entries are character strings (up to 8 characters each). Index numbers for rows,
            columns, and planes are sequential values beginning with one.

          * ``TABLE`` - Array indices are real (non-integer) numbers which must be defined when filling the
            table. Index numbers for the rows and columns are stored in the zero column and row "array elements"
            and are initially assigned a near-zero value. Index numbers must be in ascending order and are used
            only for retrieving an array element. When retrieving an array element with a real index that does
            not match a specified index, linear interpolation is done among the nearest indices and the
            corresponding array element values ( :ref:`starset` ). Used for 1-, 2-, or 3D tables.

          * ``TAB4`` - Same as TABLE, but used to specify 4-D tables.

          * ``TAB5`` - Same as TABLE, but used to specify 5-D tables.

          * ``STRING`` - Array entries are character strings (up to IMAX each). Index numbers for columns and
            planes are sequential values beginning with 1. Row index is character position in string.

        * ``imax : str`` - Extent of first dimension (row). (For ``Type`` = STRING, ``IMAX`` is rounded up
          to the next multiple of eight and has a limit of 248). Default = 1.

        * ``jmax : str`` - Extent of second dimension (column). Default = 1.

        * ``kmax : str`` - Extent of third dimension (plane). Default = 1.

        * ``var1 : str`` - Variable name corresponding to the first dimension (row) for ``Type`` = TABLE,
          TAB4, or TAB5. Default = Row.

        * ``var2 : str`` - Variable name corresponding to the second dimension (column) for ``Type`` =
          TABLE, TAB4, or TAB5. Default = Column.

        * ``var3 : str`` - Variable name corresponding to the third dimension (plane) for ``Type`` = TABLE,
          TAB4, TAB5. Default = Plane.

        * ``csysid : str`` - An integer corresponding to the coordinate system ID number. Default = 0
          (global Cartesian).

        .. _a-DIM_notes:

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
        can either specify a primary variable (listed in :ref:`a-DIM_tab_1` ) or can be an independent
        parameter. If specifying an independent parameter, then you must define an additional table for the
        independent parameter. The additional table must have the same name as the independent parameter and
        may be a function of one or more primary variables or another independent parameter. All independent
        parameters must relate to a primary variable.

        Tabular load arrays can be defined in both global Cartesian (default), cylindrical, spherical, or
        local (see below) coordinate systems by specifying ``CSYSID``, as defined in :ref:`local`.
        Coordinate system ``CSYSID`` must exist prior to issuing the :ref:`dim` command.

        **The following constraints apply when specifying a local coordinate system for your tabular
        loads:**

        * Only Cartesian, cylindrical and spherical coordinate systems are supported

        * Angle values for Y in cylindrical or spherical coordinate systems must be input in degrees and
          must be positive values between 0 and 360 degrees (0 :math:`equation not available`  Y
          :math:`equation not available`  360)

        * Angle values for Z in spherical coordinate system must be input in degrees and must be positive
          values between -90 and +90 ( -90 :math:`equation not available`  Z  :math:`equation not available`
          90)

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

        .. _a-DIM_tab_1:

        \*DIM - Primary Variables
        *************************

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
             - PRESSURE [ :ref:`cmddimvarnote1` ]
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


        .. _cmddimvarnote1:

        Specify PRESSURE as the independent variable (not PRES).

        The X, Y, and Z coordinate locations listed above are valid in global Cartesian, or local
        (Cartesian, cylindrical and spherical) coordinate systems. The VELOCITY label is applicable only to
        the calculated fluid velocity in element ``FLUID116``.

        When using PRESSURE as a primary variable, the underlying element must have the pressure DOF
        associated with it, or it must be a supported contact element.

        The gap/penetration label (GAP) is only used for defining certain contact element real constants.

        The frequency label (FREQ) is valid for harmonic analyses only.

        The node and element labels (NODE and ELEM) allow you to use node and element numbers as primary
        variables, and their axis values should be integers.

        The OMEGS, ECCENT, and THETA primary variables only apply to the ``COMBI214`` element. The amplitude
        of the rotational velocity (OMEGS) is an absolute value, so only positive values of OMEGS are valid.
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

        .. _GET_notes:

        :ref:`get` retrieves a value for a specified item and stores the value as a scalar parameter, or as
        a value in a user-named array parameter. An item is identified by various keyword, label, and number
        combinations. Usage is similar to the :ref:`starset` command except that the parameter values are
        retrieved from previously input or calculated results.

          Example: :ref:`get` Usage

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

        * :ref:`gettabgen`

        * :ref:`gettabprep`

        * :ref:`gettabsol`

        * :ref:`gettabpost`

        The :ref:`get` command is valid in any processor.

        **General Items**

        .. _gettabgen:

        \*GET General Entity Items
        ^^^^^^^^^^^^^^^^^^^^^^^^^^

        * :ref:`get_gen_act`

        * :ref:`get_gen_cmd`

        * :ref:`get_gen_comp`

        * :ref:`get_gen_graph`

        * :ref:`get_gen_parm`

        * :ref:`get_gen_tbtype`

        .. _get_gen_act:

        \*GET General Items, Entity = ACTIVE
        ************************************

        .. flat-table:: ``Entity`` = ACTIVE, ``ENTNUM`` = 0 (or blank)
           :header-rows: 2

           * - :ref:`get`, Par, ACTIVE, 0, ``Item1``, ``IT1NUM``, ``Item2``, ``IT2NUM``
           * - Item1
             - IT1NUM
             - Description
           * - INT
             -
             - Current interactive key: 0=off, 2=on.
           * - IMME
             -
             - Current immediate key: 0=off, 1=on.
           * - MENU
             -
             - Current menu key: 0=off, 1=on.
           * - PRKEY
             -
             - Printout suppression status: 0= :ref:`nopr`, 1= :ref:`gopr` or :ref:`slashgo`
           * - UNITS
             -
             - Units specified by :ref:`units` command: 0 = USER, 1 = SI, 2 = CGS, 3 = BFT, 4 = BIN, 5 = MKS, 6 = MPA, 7 = uMKS.
           * - ROUT
             -
             - Current routine: 0 = Begin level, 17 = PREP7, 21 = SOLUTION, 31 = POST1, 36 = POST26, 52 = AUX2, 53 = AUX3, 62 = AUX12, 65 = AUX15.
           * - TIME
             - WALL,CPU
             - Current wall clock or CPU time. Current wall clock will continue to accumulate during a run and is not reset to zero at midnight.
           * - DBASE
             - LDATE
             - Date of first modification of any database quantity required for POST1 operation. The parameter returned is ``Par`` = YEAR\*10000 + MONTH\*100 + DAY.
           * - DBASE
             - LTIME
             - Time of last modification of any database quantity required for POST1 operation. The parameter returned is ``Par`` = HOURS\*10000 + MINUTES\*100 + SECONDS.
           * - REV
             -
             - Minor release revision number (5.6, 5.7, 6.0 etc.). Letter notation (for example, 5.0A) is not included.
           * - TITLE
             - 0,1,2,3,4
             - **Item2:** START **IT2NUM:**  ``N`` Current title string of the main title ( ``IT1NUM`` =0 or blank) or subtitle 1, 2, 3, or 4 ( ``IT1NUM`` =1,2,3, or 4). A character parameter of up to 8 characters, starting at position ``N``, is returned.
           * - JOBNAM
             -
             - **Item2:** START **IT2NUM:**  ``N`` Current Jobname. A character parameter of up to 8 characters, starting at position ``N``, is returned. Use :ref:`dim` and ``*DO`` to get all 32 characters.
           * - PLATFORM
             -
             - The current platform.
           * - NPROC
             - CURR, MAX, MAXP
             - The number of processors being used for the current session, or the maximum total number of processors (physical and virtual) available on the machine, or the maximum number of physical processors available on the machine. This only applies to shared-memory parallelism.
           * - NUMCPU
             -
             - Number of distributed processes being used (distributed-memory parallel solution).


        .. _get_gen_cmd:

        \*GET General Items, Entity = CMD
        *********************************

        .. flat-table:: ``Entity`` = CMD, ``ENTNUM`` = 0 (or blank) The following items are valid for all commands except star (\2) commands and non-graphics slash (/) commands.
           :header-rows: 2

           * - :ref:`get`, ``Par``, CMD, 0, ``Item1``, ``IT1NUM``, ``Item2``, ``IT2NUM``
           * - Item1
             - IT1NUM
             - Description
           * - STAT
             -
             - Status of previous command: 0=found, 1=not found (unknown).
           * - NARGS
             -
             - Field number of last nonblank field on the previous command.
           * - FIELD
             - 2,3... ``N``
             - Numerical value of the ``N`` th field on the previous command. Field 1 is the command name (not available)


        .. _get_gen_comp:

        \*GET General Items, Entity = COMP
        **********************************

        .. flat-table:: ``Entity`` = COMP, ``ENTNUM`` = 0 (or blank)
           :header-rows: 2

           * - :ref:`get`, ``Par``, COMP, 0, ``Item1``, ``IT1NUM``, ``Item2``, ``IT2NUM``
           * - Item1
             - IT1NUM
             - Description
           * - NCOMP
             -
             - Total number of components and assemblies currently defined.


        .. _get_gen_graph:

        \*GET General Items, Entity = GRAPH
        ***********************************

        .. flat-table:: ``Entity`` =GRAPH, ``ENTNUM`` = N (window number)
           :header-rows: 2

           * - :ref:`get`, ``Par``, GRAPH, N, ``Item1``, ``IT1NUM``, ``Item2``, ``IT2NUM``
           * - Item1
             - IT1NUM
             - Description
           * - ACTIVE
             -
             - :ref:`window` status: 0=off, 1=on.
           * - ANGLE
             -
             - :ref:`angle`  ``THETA`` angle.
           * - CONTOUR
             - ``Name``
             - :ref:`contour` value for ``Name``, where ``Name`` = VMIN, VINC, or NCONT.
           * - DIST
             -
             - :ref:`dist`  ``DVAL`` value.
           * - DSCALE
             - DMULT
             - :ref:`slashdscale`  ``DMULT`` value.
           * - EDGE
             -
             - :ref:`edge`  ``KEY`` value.
           * - FOCUS
             - X, Y, Z
             - :ref:`focus`  ``CIN``, ``YF``, or ``ZF`` value.
           * - GLINE
             -
             - :ref:`gline`  ``STYLE`` value.
           * - MODE
             -
             - :ref:`user` or :ref:`auto` setting: 0=user, 1=auto.
           * - NORMAL
             -
             - :ref:`normal`  ``KEY`` value.
           * - RANGE
             - XMIN, XMAX, YMIN, YMAX
             - :ref:`window`  ``XMIN``, ``XMAX``, ``YMIN``, or ``YMAX`` screen coordinates.
           * - RATIO
             - X, Y
             - :ref:`ratio`  ``RATOX`` or ``RATOY`` value.
           * - SSCALE
             - SMULT
             - :ref:`sscale`  ``SMULT`` value.
           * - TYPE
             -
             - :ref:`slashtype`  ``Type`` value.
           * - VCONE
             - ANGLE
             - :ref:`vcone`  ``PHI`` angle.
           * - VIEW
             - X, Y, Z
             - :ref:`view`  ``XV``, ``YV``, or ``ZV`` value.
           * - VSCALE
             - VRATIO
             - :ref:`vscale`  ``VRATIO`` value.


        .. _get_gen_parm:

        \*GET General Items, Entity = PARM
        **********************************

        .. flat-table:: ``Entity`` = PARM, ``ENTNUM`` = 0 (or blank)
           :header-rows: 2

           * - :ref:`get`, ``Par``, PARM, 0, ``Item1``, ``IT1NUM``, ``Item2``, ``IT2NUM``
           * - Item1
             - IT1NUM
             - Description
           * - MAX
             -
             - Total number of parameters currently defined.
           * - BASIC
             -
             - Number of scalar parameters (excluding parameters beginning with an underscore _, array parameters, and character parameters).
           * - LOC
             - ``Num``
             - Name of the parameter at the ``Num`` location in the parameter table. A character parameter is returned.


        .. _get_gen_tbtype:

        \*GET General Items, Entity = TBTYPE
        ************************************

        .. flat-table:: ``Entity`` = ``TBTYPE``, ``ENTNUM`` = ``MatID``  (where TBTYPE is the material table type as defined via the :ref:`tb` command, such (ELASTIC, CTE, etc.), and ``MatID`` is the material ID)   **Evaluates a material property coefficient for a given set of input field variables.**
           :header-rows: 2

           * - :ref:`get`, ``Par``, **TBTYPE**, ``MatID``, ``Item1``, ``IT1NUM``, ``Item2``, ``IT2NUM``, ``Fld1``, ``Fld2``,...
           * - Item1
             - IT1NUM
             - Description
           * - :rspan:`2` TBEV: Material table evaluation for query at a given field variable
             - :rspan:`2` ``SINDEX`` = Subtable index (1 - max number of subtables)
             - **Item2** : ``CINDEX`` = Coefficient index
           * - **IT2NUM** : ``N`` = Number of field variables input
           * - ``Fld1``, ``Fld2``, ..., : ``Val`` = Value of the field variable(s), entered in the same order specified via the :ref:`tbfield` command(s)

        **Preprocessing Items**

        .. _gettabprep:

        \*GET Preprocessing Entity Items
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        * :ref:`get_prep_act`

        * :ref:`get_prep_area`

        * :ref:`get_prep_axis`

        * :ref:`get_prep_cdsy`

        * :ref:`get_prep_ce`

        * :ref:`get_prep_cmpb`

        * :ref:`get_prep_cp`

        * :ref:`get_prep_csec`

        * :ref:`get_prep_elem`

        * :ref:`get_prep_etyp`

        * :ref:`get_prep_gcn`

        * :ref:`get_prep_genb`

        * :ref:`get_prep_gens`

        * :ref:`get_prep_kp`

        * :ref:`get_prep_line`

        * :ref:`get_prep_link`

        * :ref:`get_prep_mat`

        * :ref:`get_prep_mplab`

        * :ref:`get_prep_node`

        * :ref:`get_prep_ocean`

        * :ref:`get_prep_oczone`

        * :ref:`get_prep_part`

        * :ref:`get_prep_pipe`

        * :ref:`get_prep_rcon`

        * :ref:`get_prep_rein`

        * :ref:`get_prep_sctn`

        * :ref:`get_prep_secp`

        * :ref:`get_prep_shel`

        * :ref:`get_prep_tbft1`

        * :ref:`get_prep_tblab`

        * :ref:`get_prep_volu`

        .. _get_prep_act:

        \*GET Preprocessing Items, Entity = ACTIVE
        ******************************************

        .. flat-table:: ``Entity`` = ACTIVE, ``ENTNUM`` = 0 (or blank)
           :header-rows: 2

           * - :ref:`get`, ``Par``, ACTIVE, 0, ``Item1``, ``IT1NUM``, ``Item2``, ``IT2NUM``
           * - Item1
             - IT1NUM
             - Description
           * - SEG
             -
             - Segment capability of graphics driver: 0=no segments available, 1=erasable segments available, 2=non-erasable segments available.
           * - CSYS
             -
             - Active coordinate system.
           * - DSYS
             -
             - Active display coordinate system.
           * - MAT
             -
             - Active material.
           * - TYPE
             -
             - Active element type.
           * - REAL
             -
             - Active real constant set.
           * - ESYS
             -
             - Active element coordinate system.
           * - SECT
             -
             - Active section.
           * - CP
             -
             - Maximum coupled node set number in the model (includes merged and deleted sets until compressed out).
           * - CE
             -
             - Maximum constraint equation set number in the model (includes merged and deleted sets until compressed out).


        .. _get_prep_area:

        \*GET Preprocessing items, Entity = AREA
        ****************************************

        .. flat-table:: ``Entity`` = AREA, ``ENTNUM`` = ``N`` (area number)
           :header-rows: 2

           * - :ref:`get`, ``Par``, AREA, ``N``, ``Item1``, ``IT1NUM``, ``Item2``, ``IT2NUM``
           * - Item1
             - IT1NUM
             - Description
           * - ATTR
             - ``Name``
             - Number assigned to the attribute, ``Name``, where ``Name`` =MAT, TYPE, REAL, ESYS, KB,KE,SECN, NNOD, NELM, or ESIZ. (NNOD=number of nodes, NELM=number of elements, ESIZ=element size.)
           * - ASEL
             -
             - Select status of area ``N`` : -1=unselected, 0=undefined, 1=selected. Alternative get function: ASEL( ``N`` ).
           * - NXTH
             -
             - Next higher area number above ``N`` in selected set (or zero if none found).
           * - NXTL
             -
             - Next lower area number below ``N`` in selected set (or zero if none found).
           * - AREA
             -
             - Area of area ``N``. ( :ref:`asum` or :ref:`gsum` must have been performed sometime previously with at least this area ``N`` selected).
           * - LOOP
             - 1,2,..., ``I``
             - ``Item2`` : LINE, ``IT2NUM`` : 1,2,..., ``p`` Line number of position ``p`` of loop ``I``


        .. _get_prep_axis:

        \*GET Preprocessing Items, Entity = AXIS
        ****************************************

        .. flat-table:: ``Entity`` = AXIS, ``ENTNUM`` = 0 (or blank)
           :header-rows: 2

           * - :ref:`get`, ``Par``, AXIS, 0, ``Item1``, ``IT1NUM``, ``Item2``, ``IT2NUM``
           * - Item1
             - IT1NUM
             - Description
           * - COUNT
             - --
             - Number of defined sections.
           * - NUM
             - MAX
             - Largest section number defined.


        .. _get_prep_cdsy:

        \*GET Preprocessing Items, Entity = CDSY
        ****************************************

        .. flat-table:: ``Entity`` = CDSY, ``ENTNUM`` = ``N`` (coordinate system number)
           :header-rows: 2

           * - :ref:`get`, ``Par``, CDSY, ``N``, ``Item1``, ``IT1NUM``, ``Item2``, ``IT2NUM``
           * - Item1
             - IT1NUM
             - Description
           * - LOC
             - X, Y, Z
             - X, Y, or Z origin location in global Cartesian system.
           * - ANG
             - XY, YZ, ZX
             - THXY, THYZ, or THZX rotation angle (in degrees) relative to the global Cartesian coordinate system.
           * - ATTR
             - ``Name``
             - Number assigned to ``Name``, where ``Name`` =KCS, KTHET, KPHI, PAR1, or PAR2. The value -1.0 is returned for KCS if the coordinate system is undefined.
           * - NUM
             - MAX
             - The maximum coordinate system number


        .. _get_prep_ce:

        \*GET Preprocessing Items, Entity = CE
        **************************************

        .. flat-table:: ``Entity`` = CE, ``ENTNUM`` = ``N`` (constraint equation set)
           :header-rows: 2

           * - :ref:`get`, ``Par``, CE, ``N``, ``Item1``, ``IT1NUM``, ``Item2``, ``IT2NUM``
           * - Item1
             - IT1NUM
             - Description
           * - If N = 0, then
           * - MAX
             -
             - Maximum constraint equation number
           * - NUM
             -
             - Number of constraint equations
           * - If N > 0, then
           * - NTERM
             -
             - Number of terms in this constraint equation
           * - CONST
             -
             - Constant term for this constraint equation
           * - TERM
             - number
             - Item2 = NODE: Gives the node for this position in the constraint equation.   Item2 = DOF: Gives the DOF number for this position in the constraint equation. (1-UX, 2-UY, 3-UZ, 4-ROTX, etc.)   Item2 = COEF: Gives the coefficient for this position in the constraint equation.


        .. _get_prep_cmpb:

        \*GET Preprocessing Items, Entity = CMPB
        ****************************************

        .. flat-table:: ``Entity`` = CMPB, ``ENTNUM`` = ``N`` (composite beam section identification number)
           :header-rows: 2

           * - :ref:`get`, ``Par``, CMPB, ``N``, ``Item1``, ``IT1NUM``, ``Item2``, ``IT2NUM``
           * - Item1
             - IT1NUM
             - Description
           * - COUNT
             -
             - Number of defined sections. If Item1 = COUNT, then N is blank.
           * - NUM
             - MAX
             - Largest section number defined. If IT1NUM = MAX, then N is blank.
           * - EXIS
             -
             - Returns a 1 if the section exists and if it is a CMPB section.
           * - NAME
             -
             - The 8-character section name defined via the :ref:`sectype` command.
           * - One of the following:     * CBMX * CBTE * CBMD
             -
             - Item2 = NTEM (the number of temperatures for :ref:`cbmx`, :ref:`cbte`, or :ref:`cbmd` data).
           * - One of the following:     * CBMX * CBTE * CBMD
             -
             - Item2 = TVAL; IT2NUM = ``nnn``  where ``nnn`` is the temperature value (< = NTEM).
           * - One of the following:     * CBMX * CBTE * CBMD
             - ``nnn``
             - Item2 = TEMP; IT2NUM = ``tval``  Where ``nnn`` is the location in the :ref:`cbmx`, :ref:`cbte`, or :ref:`cbmd` command for the given coefficient number, and ``tval`` is the temperature value.


        .. _get_prep_cp:

        \*GET Preprocessing Items, Entity = CP
        **************************************

        .. flat-table:: ``Entity`` = CP, ``ENTNUM`` = ``N`` (coupled node set)
           :header-rows: 2

           * - :ref:`get`, ``Par``, CP, ``N``, ``Item1``, ``IT1NUM``, ``Item2``, ``IT2NUM``
           * - Item1
             - IT1NUM
             - Description
           * - If N = 0, then
           * - MAX
             -
             - Maximum coupled set number
           * - NUM
             -
             - Number of coupled sets
           * - If N > 0, then
           * - DOF
             -
             - The degree of freedom for this set (1-UX, 2-UY, 3-UZ, 4-ROTX, etc.)
           * - NTERM
             -
             - Number of nodes in this set.
           * - TERM
             - number
             - Item2 = NODE: Gives the node for this position number in the coupled set.


        .. _get_prep_csec:

        \*GET Preprocessing Items, Entity = CSEC
        ****************************************

        .. flat-table:: ``Entity`` = CSEC, ``ENTNUM`` = 0 (or blank)
           :header-rows: 2

           * - :ref:`get`, ``Par``, CSEC, 0, ``Item1``, ``IT1NUM``, ``Item2``, ``IT2NUM``
           * - Item1
             - IT1NUM
             - Description
           * - COUNT
             - --
             - Number of defined sections.
           * - NUM
             - MAX
             - Largest section number defined.


        .. _get_prep_elem:

        \*GET Preprocessing Items, Entity = ELEM
        ****************************************

        .. flat-table:: ``Entity`` = ELEM, ``ENTNUM`` = ``N`` (element number)
           :header-rows: 2

           * - :ref:`get`, ``Par``, ELEM, ``N``, ``Item1``, ``IT1NUM``, ``Item2``, ``IT2NUM``
           * - Item1
             - IT1NUM
             - Description
           * - NODE
             - 1, 2,... 20
             - Node number at position 1,2,... or 20 of element ``N``. Alternative get function: NELEM( ``n,npos`` ), where ``npos`` is 1,2,...20.
           * - CENT
             - X, Y, Z
             - Centroid X, Y, or Z location (based on shape function) in the active coordinate system. The original locations is used even if large deflections are active. Alternative get functions: CENTRX( ``N`` ), CENTRY( ``N`` ), and CENTRZ( ``N`` ) always retrieve the element centroid in global Cartesian coordinates, and are determined from the selected nodes on the elements.
           * - ADJ
             - 1, 2,... 6
             - Element number adjacent to face 1,2,...6. Alternative get function: ELADJ( ``N``, ``face`` ). Only elements (of the same dimensionality) adjacent to lateral faces are considered.
           * - ATTR
             - ``Name``
             - Number assigned to the attribute ``Name``, where ``Name`` = MAT, TYPE, REAL, ESYS, PSTAT, LIVE, or SECN. Returns a zero if the element is unselected. If ``Name`` = LIVE, returns a 1 if the element is selected and active, and a -1 if it is selected and inactive. ``Name`` = SECN returns the section number of the selected beam element.
           * - LENG
             -
             - Length of line element (straight line between ends).
           * - LPROJ
             - X, Y, Z
             - Projected line element length (in the active coordinate system). X is x-projection onto y-z plane, Y is y projection onto z-x plane, and Z is z-projection onto x-y plane.
           * - AREA
             -
             - Area of area element.
           * - APROJ
             - X, Y, Z
             - Projected area of area element area (in the active coordinate system). X is x-projection onto y-z plane, Y is y projection onto z-x plane, and Z is z-projection onto x-y plane.
           * - VOLU
             -
             - Element volume. Based on unit thickness for 2D plane elements (unless the thickness option is used) and on the full 360 degrees for 2D axisymmetric elements. For general axisymmetric elements ``SOLID272`` and ``SOLID273``, only the area of the element on the master plane is reported before solving, not the volume. After solving, the volume is reported.   If results data are in the database, the volume returned is the volume calculated during solution.
           * - ESEL
             -
             - Select status of element ``N`` : -1 = unselected, 0 = undefined, 1 = selected. Alternative get function: ESEL( ``N`` ).
           * - NXTH
             -
             - Next higher element number above ``N`` in selected set (or zero if none found). Alternative get function: ELNEXT( ``N`` )
           * - NXTL
             -
             - Next lower element number below ``N`` in selected set (or zero if none found).
           * - HGEN
             -
             - Heat generation on selected element ``N``.
           * - DGEN
             -
             - Diffusing substance generation on selected node N (returns 0.0 if node is unselected, or if the DOF is inactive).
           * - HCOE
             - face
             - Heat coefficient for selected element ``N`` on specified face. Returns the value at the first node that forms the face.
           * - TBULK
             - face
             - Bulk temperature for selected element ``N`` on specified face. Returns the value at the first node that forms the face.
           * - PRES
             - face
             - Pressure on selected element, ``N`` on specified face. Returns the value at the first node that forms the face.
           * - SHPAR
             - ``Test``
             - Element shape test result for selected element ``N``, where ``Test`` = ANGD, ASPE (aspect ratio), JACR (Jacobian ratio), MAXA (maximum corner angle), PARA (deviation from parallelism of opposite edges), or WARP (warping factor).
           * - MEMBER
             - COUNT
             - Number of reinforcing members (individual reinforcings) in the element ``N``.
           * - :rspan:`1` EGID
             - COUNT
             - Number of non-duplicate global identifiers in the element ``N``.
           * - MIN, MAX
             - Lowest or highest global identifier in the element ``N``.


        .. _get_prep_etyp:

        \*GET Preprocessing Items, Entity = ETYP
        ****************************************

        .. flat-table:: ``Entity`` = ETYP, ``ENTNUM`` = ``N`` (element type number)
           :header-rows: 2

           * - :ref:`get`, ``Par``, ETYP, ``N``, ``Item1``, ``IT1NUM``, ``Item2``, ``IT2NUM``
           * - Item1
             - IT1NUM
             - Description
           * - ATTR
             - ``Name``
             - Number assigned to the attribute ``Name``, where ``Name`` =ENAM, KOP1, KOP2,..., KOP9, KO10, KO11, etc.


        .. _get_prep_gcn:

        \*GET Preprocessing Items, Entity = GCN
        ***************************************

        .. flat-table:: ``Entity`` = GCN, ``ENTNUM`` = 0 (or blank)
           :header-rows: 2

           * - :ref:`get`, ``Par``, GCN, 0, ``Item1``, ``IT1NUM``, ``Item2``, ``IT2NUM``
           * - Item1
             - IT1NUM
             - Description
           * - MAT
             - ``Sect1``
             - ``Item2`` = 0 or blank; ``IT2NUM`` = ``Sect2``. Material ID to be used for general contact between ``Sect1`` and ``Sect2``. Alternative get function: SECTOMAT( ``Sect1``, ``Sect2`` ).
           * - REAL
             - ``Sect1``
             - ``Item2`` = 0 or blank; ``IT2NUM`` = ``Sect2``. Real constant ID to be used for general contact between ``Sect1`` and ``Sect2`` . Alternative get function: SECTOREAL( ``Sect1``, ``Sect2`` ).
           * - DEF
             - ``Sect1``
             - ``Item2`` = 0 or blank; ``IT2NUM`` = ``Sect2``. Number indicating the type of contact for the general contact definition between ``Sect1`` and ``Sect2`` :   * = 0 - Excluded general contact between ``Sect1`` / ``Sect2`` * = 1 - Asymmetric general contact between ``Sect1`` (contact) / ``Sect2`` (target) * = 2 - Asymmetric general contact between ``Sect1`` (target) / ``Sect2`` (contact) * = 3 - Symmetric general contact between ``Sect1`` / ``Sect2``
           * - ``Sect1`` and ``Sect2`` are section numbers associated with general contact surfaces.


        .. _get_prep_genb:

        \*GET Preprocessing Items, Entity = GENB
        ****************************************

        .. flat-table:: ``Entity`` = GENB, ``ENTNUM`` = ``N`` (nonlinear beam general section identification number)
           :header-rows: 2

           * - :ref:`get`, ``Par``, GENB, ``N``, ``Item1``, ``IT1NUM``, ``Item2``, ``IT2NUM``
           * - Item1
             - IT1NUM
             - Description
           * - COUNT
             - (Blank)
             - Number of defined sections. If ``Item1`` = COUNT, then ``N`` is blank.
           * - NUM
             - MAX
             - Largest section number defined. If ``IT1NUM`` = MAX, then ``N`` is blank.
           * - EXIS
             - (Blank)
             - Returns a 1 if the section exists and if it is a GENB section.
           * - SUBTYPE
             - (Blank)
             - Section subtype for the section ID specified via the :ref:`sectype` command.
           * - NAME
             - (Blank)
             - The 8-character section name defined via the :ref:`sectype` command.
           * - One of the following:    * BSAX * BSM1 * BSM2 * BSTQ * BSS1 * BSS2 * BSMD * BSTE
             - (Blank)
             - ``Item2`` = NTEM, the number of temperatures for :ref:`bsax`, :ref:`bsm1`, :ref:`bsm2`, :ref:`bstq`, :ref:`bss1`, :ref:`bss2`, :ref:`bsmd`, or :ref:`bste` data.
           * - One of the following:    * BSAX * BSM1 * BSM2 * BSTQ * BSS1 * BSS2 * BSMD * BSTE
             - (Blank)
             - ``Item2`` = TVAL; ``IT2NUM`` = ``nnn``  Where ``nnn`` is the temperature value (<= NTEM).
           * - One of the following:    * BSAX * BSM1 * BSM2 * BSTQ * BSS1 * BSS2 * BSMD * BSTE
             - ``nnn``
             - ``Item2`` = TEMP; ``IT2NUM`` = ``tval``  Where ``nnn`` is the location in the :ref:`bsax`, :ref:`bsm1`, :ref:`bsm2`, :ref:`bstq`, :ref:`bss1`, :ref:`bss2`, :ref:`bsmd`, or :ref:`bste` command for the given coefficient number, and ``tval`` is the temperature value.   Examples for ``nnn`` :     * ``nnn`` = 1 for STRAIN(1) * ``nnn`` = 2 for STRESS(1) * ``nnn`` = 3 for STRAIN(2) * ``nnn`` = 4 for STRESS(2) * ``nnn`` = 5 for STRAIN(3) *...
           * - One of the following:    * BSAX * BSM1 * BSM2 * BSTQ * BSS1 * BSS2 * BSMD * BSTE
             - (Blank)
             - ``Item2`` = TEMP; ``IT2NUM`` = ``tval`` ; ``Item3`` = NCONST The number of constants at ``tval``.


        .. _get_prep_gens:

        \*GET Preprocessing Items, Entity = GENS
        ****************************************

        .. flat-table:: ``Entity`` = GENS, ``ENTNUM`` = ``N`` (preintegrated shell general section identification number)
           :header-rows: 2

           * - :ref:`get`, ``Par``, GENS, ``N``, ``Item1``, ``IT1NUM``, ``Item2``, ``IT2NUM``
           * - Item1
             - IT1NUM
             - Description
           * - COUNT
             - (Blank)
             - Number of defined sections. If ``Item1`` = COUNT, then ``N`` is blank.
           * - NUM
             - MAX
             - Largest section number defined. If ``IT1NUM`` = MAX, then ``N`` is blank.
           * - EXIS
             - (Blank)
             - Returns a 1 if the section exists and if it is a GENS section.
           * - NAME
             - (Blank)
             - The 8-character section name defined via the :ref:`sectype` command.
           * - One of the following:    * SSPA * SSPB * SSPD * SSPE * SSMT * SSBT * SSPM
             - (Blank)
             - ``Item2`` = NTEM, the number of temperatures for :ref:`sspa`, :ref:`sspb`, :ref:`sspd`, :ref:`sspe`, :ref:`ssmt`, :ref:`ssbt`, or :ref:`sspm` data.
           * - One of the following:    * SSPA * SSPB * SSPD * SSPE * SSMT * SSBT * SSPM
             - (Blank)
             - ``Item2`` = TVAL; ``IT2NUM`` = ``nnn``  Where ``nnn`` is the temperature value (<= NTEM).
           * - One of the following:    * SSPA * SSPB * SSPD * SSPE * SSMT * SSBT * SSPM
             - ``nnn``
             - ``Item2`` = TEMP; ``IT2NUM`` = ``tval``  Where ``nnn`` is the location in the :ref:`sspa`, :ref:`sspb`, :ref:`sspd`, :ref:`sspe`, :ref:`ssmt`, :ref:`ssbt`, or :ref:`sspm` command for the given coefficient number, and ``tval`` is the temperature value.


        .. _get_prep_kp:

        \*GET Preprocessing Items, Entity = KP
        **************************************

        .. flat-table:: ``Entity`` = KP, ``ENTNUM`` = ``N`` (keypoint number)
           :header-rows: 2

           * - :ref:`get`, ``Par``, KP, ``N``, ``Item1``, ``IT1NUM``, ``Item2``, ``IT2NUM``
           * - Item1
             - IT1NUM
             - Description
           * - LOC
             - X, Y, Z
             - X, Y, or Z location in the active coordinate system. Alternative get functions: KX( ``N`` ), KY( ``N`` ), KZ( ``N`` ). Inverse get function: KP( ``x,y,z`` ) returns the number of the selected keypoint nearest the ``x,y,z`` location (in the active coordinate system, lowest number for coincident keypoints).
           * - ATTR
             - ``Name``
             - Number assigned to the attribute ``Name``, where ``Name`` = MAT, TYPE, REAL, ESYS, NODE, or ELEM.
           * - KSEL
             -
             - Select status of keypoint ``N`` : -1 = unselected, 0 = undefined, 1 = selected. Alternative get function: KSEL( ``N`` ).
           * - NXTH
             -
             - Next higher keypoint number above ``N`` in selected set (or zero if none found). Alternative get function: KPNEXT( ``N`` ).
           * - NXTL
             -
             - Next lower keypoint number below ``N`` in selected set (or zero if none found).
           * - DIV
             -
             - Divisions (element size setting) from :ref:`kesize` command.


        .. _get_prep_line:

        \*GET Preprocessing Items, Entity = LINE
        ****************************************

        .. flat-table:: ``Entity`` = LINE, ``ENTNUM`` = ``N`` (line number)
           :header-rows: 2

           * - :ref:`get`, ``Par``, LINE, ``N``, ``Item1``, ``IT1NUM``, ``Item2``, ``IT2NUM``
           * - Item1
             - IT1NUM
             - Description
           * - KP
             - 1,2
             - Keypoint number at position 1 or 2.
           * - ATTR
             - ``Name``
             - Number assigned to the attribute, ``Name``, where ``Name`` =MAT, TYPE, REAL, ESYS, NNOD, NELM, NDIV, NDNX, SPAC, SPNX, KYND, KYSP, LAY1, or LAY2. (NNOD=number of nodes, returns --1 for meshed line with no internal nodes, NELM=number of elements, NDIV=number of divisions in an existing mesh, NDNX=number of divisions assigned for next mesh, SPAC=spacing ratio in an existing mesh, SPNX=spacing ratio for next mesh, KYND=soft key for NDNX, KYSP=soft key for SPNX, LAY1=LAYER1 setting, LAY2=LAYER2 setting.)
           * - LSEL
             -
             - Select status of line ``N`` : -1=unselected, 0=undefined, 1=selected. Alternative get function: LSEL( ``N`` ).
           * - NXTH
             -
             - Next higher line number above ``N`` in the selected set (or zero if none found). Alternative get function: LSNEXT( ``N`` )
           * - NXTL
             -
             - Next lower line number below ``N`` in selected set (or zero if none found).
           * - LENG
             -
             - Length. A get function LX( ``n,lfrac`` ) also exists to return the X coordinate location of line ``N`` at the length fraction ``lfrac`` (0.0 to 1.0). Similar LY and LZ functions exist.


        .. _get_prep_link:

        \*GET Preprocessing Items, Entity = LINK
        ****************************************

        .. flat-table:: ``Entity`` = LINK, ``ENTNUM`` = 0 (or blank)
           :header-rows: 2

           * - :ref:`get`, ``Par``, LINK, ``NUM``, ``Item1``, ``IT1NUM``, ``Item2``, ``IT2NUM``
           * - Item1
             - IT1NUM
             - Description
           * - COUNT
             -
             - Number of defined sections.
           * - NUM
             - MAX
             - Largest section number defined.


        .. _get_prep_mat:

        \*GET Preprocessing Items, Entity = MAT
        ***************************************

        .. flat-table:: ``Entity`` = MAT, ``ENTNUM`` = 0 (or blank)
           :header-rows: 2

           * - :ref:`get`, ``Par``, MAT, 0, ``Item1``, ``IT1NUM``, ``Item2``, ``IT2NUM``
           * - Item1
             - IT1NUM
             - Description
           * - COUNT
             -
             - Number of materials.
           * - NUM
             - MAX
             - Largest material number for which at least one property is defined.


        .. _get_prep_mplab:

        \*GET Preprocessing Items, Entity = MPLAB
        *****************************************

        .. flat-table:: ``Entity`` = MPlab, ``ENTNUM`` = ``N`` ( ``MPlab`` = material property label from :ref:`mp` command; ``N`` = material number.)
           :header-rows: 2

           * - :ref:`get`, ``Par``, MPlab, ``N``, ``Item1``, ``IT1NUM``, ``Item2``, ``IT2NUM``
           * - Item1
             - IT1NUM
             - Description
           * - TEMP
             - val
             - Material property value at temperature of ``val`` . For temperature dependent materials, the program interpolates the property at temperature input for ``val``.


        .. _get_prep_node:

        \*GET Preprocessing Items, Entity = NODE
        ****************************************

        .. flat-table:: ``Entity`` = NODE, ``ENTNUM`` = ``N`` (node number)
           :header-rows: 2

           * - :ref:`get`, ``Par``, NODE, ``N``, ``Item1``, ``IT1NUM``, ``Item2``, ``IT2NUM``
           * - Item1
             - IT1NUM
             - Description
           * - LOC
             - X, Y, Z
             - X, Y, Z location in the active coordinate system. Alternative get functions: NX( ``N`` ), NY( ``N`` ), NZ( ``N`` ). Inverse get function. NODE( ``x,y,z`` ) returns the number of the selected node nearest the ``x,y,z`` location (in the active coordinate system, lowest number for coincident nodes).
           * - ANG
             - XY, YZ, ZX
             - THXY, THYZ, THZX rotation angle.
           * - NSEL
             -
             - Select status of node ``N`` : -1=unselected, 0=undefined, 1=selected. Alternative get function: NSEL( ``N`` ).
           * - NXTH
             -
             - Next higher node number above ``N`` in selected set (or zero if none found). Alternative get function: NDNEXT( ``N`` ).
           * - NXTL
             -
             - Next lower node number below ``N`` in selected set (or zero if none found).
           * - F
             - FX, MX,...
             - Applied force at selected node ``N`` in direction ``IT1NUM`` (returns 0.0 if no force is defined, if node is unselected, or if the DOF is inactive). If ``ITEM2`` is IMAG, return the imaginary part.
           * - D
             - UX, ROTX,...
             - Applied constraint force at selected node ``N`` in direction ``IT1NUM`` (returns a large number, such as 2e100, if no constraint is specified, if the node is unselected, or if the DOF is inactive). If ``ITEM2`` is IMAG, return the imaginary part.
           * - HGEN
             -
             - Heat generation on selected node ``N`` (returns 0.0 if node is unselected, or if the DOF is inactive).
           * - NTEMP
             -
             - Temperature on selected node N (returns 0.0 if node is unselected)
           * - CPS
             - Lab
             - Couple set number with direction Lab = any active DOF, which contains the node ``N``.
           * - DGEN
             -
             - Diffusing substance generation on selected node N (returns 0.0 if node is unselected, or if the DOF is inactive).


        .. _get_prep_ocean:

        \*GET Preprocessing Items, Entity = OCEAN
        *****************************************

        .. flat-table:: ``Entity`` = OCEAN, ``ENTNUM`` = ``Type`` (where ``Type`` is a valid label on the ``DataType`` field of the :ref:`octype` command)
           :header-rows: 2

           * - :ref:`get`, ``Par``, OCEAN, ``Type``, ``Item1``, ``IT1NUM``, ``Item2``, ``IT2NUM``
           * - Item1
             - IT1NUM
             - Description
           * - NAME
             -
             - Name defined for a given ``Type``
           * - :rspan:`13` DATA
             - 1
             - Depth when ``Type`` = BASI
           * - 2
             - Material ID when ``Type`` = BASI
           * - 8
             - ``KFLOOD`` when ``Type`` = BASI
           * - 9
             - ``Cay`` when ``Type`` = BASI
           * - 10
             - ``Cb`` when ``Type`` = BASI
           * - 11
             - ``Zmsl`` when ``Type`` = BASI
           * - 13
             - ``Caz`` when ``Type`` = BASI
           * - 14
             - ``Ktable`` when ``Type`` = BASI
           * - 1
             - ``KWAVE`` when ``Type`` = WAVE
           * - 2
             - ``THETA`` when ``Type`` = WAVE
           * - 3
             - ``WAVELOC`` when ``Type`` = WAVE
           * - 4
             - ``KCRC`` when ``Type`` = WAVE
           * - 5
             - ``KMF`` when ``Type`` = WAVE
           * - 6
             - ``PRKEY`` when ``Type`` = WAVE
           * - PROP
             - NROW
             - Number of rows defined by :ref:`octable` command
           * - TABL
             - ``i``
             - Data in table defined by :ref:`octable` command ``i`` = row number; Item2 = column number


        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.

        .. _get_prep_oczone:

        \*GET Preprocessing Items, Entity = OCZONE
        ******************************************

        .. flat-table:: ``Entity`` = OCZONE, ``ENTNUM`` = ``Name`` (where ``Name`` is a valid label on the ``ZoneName`` field of the :ref:`oczone` command)
           :header-rows: 2

           * - :ref:`get`, ``Par``, OCZONE, ``Name``, ``Item1``, ``IT1NUM``, ``Item2``, ``IT2NUM``
           * - Item1
             - IT1NUM
             - Description
           * - :rspan:`3` DATA
             - 8
             - ``KFLOOD`` for a given ``ENTNUM`` = ``Name``
           * - 9
             - ``Cay`` for a given ``ENTNUM`` = ``Name``
           * - 10
             - ``Cb`` for a given ``ENTNUM`` = ``Name``
           * - 13
             - ``Caz`` for a given ``ENTNUM`` = ``Name``
           * - PROP
             - NROW
             - Number of rows defined by :ref:`octable` command
           * - TABL
             - ``i``
             - Data in table defined by :ref:`octable` command ``i`` = row number; Item2 = column number
           * - TYPE
             -
             - Ocean zone type (returns 1, 2 or 3 for ZLOC-, COMP-, or PIP-type zones, respectively)
           * - COMP
             -
             - Component name when the given ocean zone type is COMP, or internal component name when the given ocean zone type is PIP
           * - COMP2
             -
             - External component name when the type of given ocean zone is PIP


        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.

        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.

        .. _get_prep_pipe:

        \*GET Preprocessing Items, Entity = PIPE
        ****************************************

        .. flat-table:: ``Entity`` = PIPE, ``ENTNUM`` = 0 (or blank)
           :header-rows: 2

           * - :ref:`get`, ``Par``, PIPE, ``NUM``, ``Item1``, ``IT1NUM``, ``Item2``, ``IT2NUM``
           * - Item1
             - IT1NUM
             - Description
           * - COUNT
             -
             - Number of defined sections
           * - NUM
             - MAX
             - Largest section number defined


        .. _get_prep_part:

        \*GET Preprocessing Items, Entity = PART
        ****************************************

        .. flat-table:: ``Entity`` = PART, ``ENTNUM`` = ``N`` (PART number)
           :header-rows: 2

           * - :ref:`get`, ``Par``, PART, ``N``, ``Item1``, ``IT1NUM``, ``Item2``, ``IT2NUM``
           * - Item1
             - IT1NUM
             - Description
           * - TYPE
             -
             - Element type number assigned to PART ``N``.
           * - MAT
             -
             - Material number assigned to PART ``N``.
           * - REAL
             -
             - Real constant number assigned to PART ``N``.


        .. _get_prep_rcon:

        \*GET Preprocessing Items, Entity = RCON
        ****************************************

        .. flat-table:: ``Entity`` = :ref:`rcon`, ``ENTNUM`` = ``N`` (real constant set number)
           :header-rows: 1

           * - :ref:`get`, ``Par``, RCON, ``N``, ``Item1``, ``IT1NUM``, ``Item2``, ``IT2NUM``
           * - CONST
             - 1, 2,..., ``m``
             - Value of real constant number ``m`` in set ``N``.
           * - :ref:`get`
             - [\*GET ,Par, RCON,0, Item1, IT1NUM, Item2, IT2NUM]
           * - NUM
             - MAX
             - The maximum real constant set number defined


        .. _get_prep_rein:

        \*GET Preprocessing Items, Entity = REIN
        ****************************************

        .. flat-table:: ``Entity`` = REIN, ``ENTNUM`` = ``N`` (reinforcing section identification number)
           :header-rows: 2

           * - :ref:`get`, ``Par``, REIN, ``N``, ``Item1``, ``IT1NUM``, ``Item2``, ``IT2NUM``
           * - Item1
             - IT1NUM
             - Description
           * - TYPE
             -
             - Section type, for ID -- :ref:`sectype` command (always REIN for reinforcing sections).
           * - SUBTYPE
             -
             - Section subtype for ID -- :ref:`sectype` command.
           * - NAME
             -
             - Name defined for a given ID number.
           * - NREIN
             -
             - Number of reinforcing fibers. For reinforcing sections generated ( :ref:`ereinf` ) via the standard method, the number of fibers defined via :ref:`secdata`. For reinforcing sections generated ( :ref:`ereinf` ) via the mesh-independent method, the total number of fibers in the section.
           * - TABL
             - ``ReinfNum,I``
             - Reinforcing fiber data, as defined via :ref:`secdata`. This item is not allowed for reinforcing sections generated ( :ref:`ereinf` ) via the mesh-independent method.


        .. _get_prep_sctn:

        \*GET Preprocessing Items, Entity = SCTN
        ****************************************

        .. flat-table:: ``Entity`` = SCTN, ``ENTNUM`` = ``N`` (pretension section ID number)
           :header-rows: 2

           * - :ref:`get`, ``Par``, SCTN, ``N``, ``Item1``, ``IT1NUM``, ``Item2``, ``IT2NUM``
           * - Item1
             - IT1NUM
             - Description
           * - 1
             -
             - Section ID number.
           * - 2
             -
             - Section type (always 5 for pretension section).
           * - 3
             -
             - Pretension node number.
           * - 4
             - Coordinate system number.
             - Section normal NX.
           * - 5
             - Coordinate system number.
             - Section normal NY.
           * - 6
             - Coordinate system number.
             - Section normal NZ.
           * - 7 or 8
             -
             - Eight character section name.
           * - 9
             -
             - Initial action key. Returns 0 or 1 for lock, 2 for "free-to-slide," or 3 for tiny.
           * - 10
             -
             - Force displacement key. Returns 0 or 1 for force, or 2 for displacement.
           * - 11
             -
             - First preload value.
           * - 12
             -
             - Load step in which first preload value is to be applied.
           * - 13
             -
             - Load step in which first preload value is to be locked.
           * - 14...
             -
             - 14 through 17 is a repeat of 10 through 13, but for the second preload value; 18 through 21 is for the third preload value; and so forth.


        .. _get_prep_secp:

        \*GET Preprocessing Items, Entity = SECP
        ****************************************

        .. flat-table:: ``Entity`` = SECP, ``ENTNUM`` = 0 (or blank)
           :header-rows: 2

           * - :ref:`get`, ``Par``, SECP, ``NUM``, ``Item1``, ``IT1NUM``, ``Item2``, ``IT2NUM``
           * - Item1
             - IT1NUM
             - Description
           * - COUNT
             -
             - Number of defined sections
           * - NUM
             - MAX
             - Largest section number defined


        .. _get_prep_shel:

        \*GET Preprocessing Items, Entity = SHEL
        ****************************************

        .. flat-table:: ``Entity`` = SHEL, ENTNUM = ``N`` (shell section identification number)
           :header-rows: 2

           * - :ref:`get`, ``Par``, SHEL, ``N``, ``Item1``, ``IT1NUM``, ``Item2``, ``IT2NUM``
           * - Item1
             - IT1NUM
             - Description
           * - TYPE
             -
             - Section type, for id -- :ref:`sectype` command. (always SHEL for shell sections)
           * - NAME
             -
             - Name defined for a given id number.
           * - :rspan:`26` PROP
             - TTHK
             - Total thickness.
           * - NLAY
             - Number of layers.
           * - NSP
             - Number of section integration points.
           * - :rspan:`4` POS
             - Node position (as defined by :ref:`secoffset` ).
           * - 0 = User Defined.
           * - 1 = Middle.
           * - 2 = Top.
           * - 3 = Bottom.
           * - OFFZ
             - User-defined section offset (POS = 0).
           * - TS11
             - Transverse shear stiffness factors.
           * - TS22
             - Transverse shear stiffness factors.
           * - TS12
             - Transverse shear stiffness factors.
           * - :rspan:`2` HORC
             - Homogeneous or complete section flag.
           * - 0 = Homogeneous.
           * - 1 = Composite.
           * - FUNC
             - Tabular function name for total thickness.
           * - UT11
             - User transverse shear stiffness 11.
           * - UT22
             - User transverse shear stiffness 22.
           * - UT12
             - User transverse shear stiffness 12.
           * - AMAS
             - Added mass.
           * - MSCF
             - Hourglass control membrane scale factor.
           * - BSCF
             - Hourglass control bending scale factor.
           * - DSTF
             - Drill stiffness scale factor.
           * - LDEN
             - Laminate density.
           * - FKCN
             - ``KCN`` field value from the :ref:`secfunction` command, in which the array or table is interpreted.
           * - ABD
             - Section membrane and bending stiffness matrix. Valid ITEM2 = 1,6 and IT2NUM = 1,6.
           * - E
             - Section transverse shear stiffness matrix. Valid ITEM2 = 1,2 and IT2NUM = 1,2.
           * - :rspan:`3` LAYD
             - LayerNumber,THIC
             - Layer thickness.
           * - LayerNumber,MAT
             - Layer material.
           * - LayerNumber,ANGL
             - Layer orientation angle.
           * - LayerNumber,NINT
             - Number of layer integration points.


        .. _get_prep_tbft1:

        \*GET Preprocessing Items, Entity = TBFT
        ****************************************

        .. flat-table:: ``Entity`` = TBFT, ``ENTNUM`` = ``blank``
           :header-rows: 2

           * - :ref:`get`, ``Par``, TBFT, ``Item1``, ``IT1NUM``, ``Item2``, ``IT2NUM``
           * - Item1
             - IT1NUM
             - Description
           * - nmat
             -
             - Number of defined material models.
           * - matnum
             - ``index``
             - Material number in array (index varies for 1 to num materials).
           * - ``Entity`` = TBFT, ``ENTNUM`` = ``matid`` (For getting names of constitutive function, matid = the material ID number)
           * - :ref:`get`
             - [\*GET ,Par, TBFT,matid,nfun,IT1NUM,Item2,IT2NUM]
           * - Item1
             - IT1NUM
             - Description
           * - nfun
             -
             - Number of constitutive functions for this material.
           * - ``Entity`` = TBFT, ``ENTNUM`` = ``matid`` (To query constitutive function data, matid = the material ID number)
           * - :ref:`get`
             - [\*GET ,Par, TBFT,matid,func,fname,Item2,IT2NUM]
           * - Item1
             - IT1NUM
             - Description
           * - func
             - index
             - If Item2 = fname, the name of the constitutive function is returned.
           * - func
             - function name
             - If Item2 = ncon, the number of constants is returned for the function specified in IT1NUM by the constitutive function name.
           * - "
             - "
             - If Item2 = cons, set Item2num to index to return the value of the constant.
           * - "
             - "
             - If Item2 = fixe, set Item2num to index to return the fix flag status.
           * - "
             - "
             - If Item2 = RESI, returns the residual error while fitting the data.
           * - "
             - "
             - If Item2 = type, returns the category of the constitutive model (moon, poly, etc.)
           * - "
             - "
             - If Item2 = sord, returns the shear order of the prony visco model.
           * - "
             - "
             - If Item2 = bord, returns the bulk order of the prony visco model.
           * - "
             - "
             - If Item2 = shif, returns the shift function name of the prony visco model.
           * - ``Entity`` = TBFT, ``ENTNUM`` = ``matid`` (For getting names of experimental data, matid = the material ID number)
           * - :ref:`get`
             - [\*GET ,Par, TBFT,matid,nexp,IT1NUM,Item2,IT2NUM]
           * - Item1
             - IT1NUM
             - Description
           * - nexp
             -
             - Number of experiments for this material.
           * - ``Entity`` = TBFT, ``ENTNUM`` = ``matid`` (To query experimental data, ``matid`` = the material ID number))
           * - :ref:`get`
             - [\*GET ,Par, TBFT,matid,func,fname,Item2,IT2NUM]
           * - Item1
             - IT1NUM
             - Description
           * - "
             - expindex
             - If Item2 = type, returns experiments type string.
           * - "
             - "
             - If Item2 = numrow, returns number of rows in the data.
           * - "
             - "
             - If Item2 = numcol, returns the number of cols in a row (set Intem2num = Row index)
           * - "
             - "
             - If Item2 = data, returns the value of the data in row, col of exp expindex (set item2Num = row index and item3 = column index. All indices vary from 1 to the maximum value.
           * - "
             - "
             - If Item2 = natt, returns the number of attributes.
           * - "
             - "
             - If Item2 = attname, returns the attribute name (set Item2Num = Attr index).
           * - "
             - "
             - If Item2 = attvald, returns double value of attribute (set Item2Num = Attr index).
           * - "
             - "
             - If Item2 = attvali, returns integer valud of attribute (set Item2Num = Attr index).
           * - "
             - "
             - If Item2 = attvals, returns the string value of the attribute (set Item2Num = Attr index).


        .. _get_prep_tblab:

        \*GET Preprocessing Items, Entity = TBLAB
        *****************************************

        .. flat-table:: ``Entity`` = TBLAB, ``ENTNUM`` = ``N``..( ``TBlab`` = data table label from the :ref:`tb` command; ``N`` = material number.)
           :header-rows: 2

           * - :ref:`get`, ``Par``, ``TBlab``, ``N``, ``Item1``, ``IT1NUM``, ``Item2``, ``IT2NUM``, ``TBOPT``
           * - Item1
             - IT1NUM
             - Description
           * - TEMP
             - ``T``
             - **Item2** : CONST **IT2NUM** : ``Num`` Value of constant number Num in the data table at temperature ``T``. For constants, input an X,Y point; the constant numbers are consecutive with the X constants being the odd numbers, beginning with one.
           * - To get all necessary output for materials defined via the :ref:`tb` command, you must specify the final argument ``TBOPT`` as indicated in the syntax description above.


        .. _get_prep_volu:

        \*GET Preprocessing Items, Entity = VOLU
        ****************************************

        .. flat-table:: ``Entity`` = VOLU, ``ENTNUM`` = ``N`` (volume number)
           :header-rows: 2

           * - :ref:`get`, ``Par``, VOLU, ``N``, ``Item1``, ``IT1NUM``, ``Item2``, ``IT2NUM``
           * - Item1
             - IT1NUM
             - Description
           * - ATTR
             - ``Name``
             - Number assigned to the attribute ``Name``, where ``Name`` =MAT, TYPE, REAL, ESYS, NNOD, or NELM. (NNOD=number of nodes, NELM=number of elements.)
           * - VSEL
             -
             - Select status of volume ``N`` : -1=unselected, 0=undefined, 1=selected. Alternative get function: VSEL( ``N`` ).
           * - NXTH
             -
             - Next higher volume number above ``N`` in selected set (or zero if none found). Alternative get function: VLNEXT( ``N`` ).
           * - NXTL
             -
             - Next lower volume number below ``N`` in selected set (or zero if none found).
           * - VOLU
             -
             - Volume of volume ``N``. ( :ref:`vsum` or :ref:`gsum` must have been performed sometime previously with at least this volume ``N`` selected).
           * - SHELL
             - 1, 2,..., ``m``
             - **Item2** : AREA **IT2NUM** : 1,2,..., ``p`` Line number of position ``p`` of shell ``m``

        **Solution Items**

        .. _gettabsol:

        \*GET Solution Entity Items
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^

        * :ref:`get_sol_active`

        * :ref:`get_sol_elem`

        * :ref:`get_sol_mode`

        * :ref:`get_sol_ddam`

        .. _get_sol_active:

        \*GET Solution Items, Entity = ACTIVE
        *************************************

        .. flat-table:: ``Entity`` = ACTIVE, ``ENTNUM`` = 0 (or blank)
           :header-rows: 2

           * - :ref:`get`, ``Par``, ACTIVE, 0, ``Item1``, ``IT1NUM``, ``Item2``, ``IT2NUM``
           * - Item1
             - IT1NUM
             - Description
           * - ANTY
             -
             - Current analysis type.
           * - :rspan:`27` SOLU
             - DTIME
             - Time step size.
           * - NCMLS
             - Cumulative number of load steps.
           * - NCMSS
             - Number of substeps. NOTE: Used only for static and transient analyses.
           * - EQIT
             - Number of equilibrium iterations.
           * - NCMIT
             - Cumulative number of iterations.
           * - CNVG
             - Convergence indicator: 0=not converged, 1=converged.
           * - MXDVL
             - Maximum degree of freedom value.
           * - RESFRQ
             - Response frequency for 2nd order systems.
           * - RESEIG
             - Response eigenvalue for 1st order systems.
           * - DSPRM
             - Descent parameter.
           * - FOCV
             - Force convergence value.
           * - MOCV
             - Moment convergence value.
           * - HFCV
             - Heat flow convergence value.
           * - MFCV
             - Magnetic flux convergence value.
           * - CSCV
             - Current segment convergence value.
           * - CUCV
             - Current convergence value.
           * - FFCV
             - Fluid flow convergence value.
           * - DICV
             - Displacement convergence value.
           * - ROCV
             - Rotation convergence value.
           * - TECV
             - Temperature convergence value.
           * - VMCV
             - Vector magnetic potential convergence value.
           * - SMCV
             - Scalar magnetic potential convergence value.
           * - VOCV
             - Voltage convergence value.
           * - PRCV
             - Pressure convergence value.
           * - VECV
             - Velocity convergence value.
           * - CRPRAT
             - Maximum creep ratio.
           * - PSINC
             - Maximum plastic strain increment.
           * - CGITER
             - Number of iterations in the PCG and symmetric JCG (non-complex version) solvers.


        .. _get_sol_elem:

        \*GET Solution Items, Entity = ELEM
        ***********************************

        .. flat-table:: ``Entity`` = ELEM, ``ENTNUM`` = 0 (or blank)
           :header-rows: 2

           * - :ref:`get`, ``Par``, ELEM, 0, ``Item1``, ``IT1NUM``, ``Item2``, ``IT2NUM``
           * - Item1
             - IT1NUM
             - Description
           * - MTOT
             - X, Y, Z
             - Total mass components.
           * - MC
             - X, Y, Z
             - Center of mass components.
           * - IOR
             - X, Y, Z, XY, YZ, ZX
             - Moment of inertia about origin.
           * - IMC
             - X, Y, Z, XY, YZ, ZX
             - Moment of inertia about the center of mass.
           * - IPRIN
             - X, Y, Z
             - Principal moments of inertia.
           * - IANG
             - XY, YZ, ZX
             - Angles of the moments of inertia principal axes.
           * - FMC
             - X, Y, Z
             - Force components at mass centroid ( :ref:`1). <getentelem1>`
           * - MMOR
             - X, Y, Z
             - Moment components at origin ( :ref:`1).`
           * - MMMC
             - X, Y, Z
             - Moment components at mass centroid ( :ref:`1).`

        Items ( :ref:`1) are available only after inertia relief solution ( <getentelem1>` :ref:`irlf`,1)
        or pre-calculation of masses ( :ref:`irlf`,-1).

         Item values are consistent with the mass summary printed in the output file. They are based on
        unscaled mass properties (see :ref:`mascale` command).

        .. _get_sol_mode:

        \*GET Solution Items, Entity = MODE
        ***********************************

        .. flat-table:: ``Entity`` = MODE, ``ENTNUM`` = ``N`` (mode number)
           :header-rows: 2

           * - :ref:`get`, ``Par``, MODE, ``N``, ``Item1``, ``IT1NUM``, ``Item2``, ``IT2NUM``
           * - Item1
             - IT1NUM
             - Description
           * - FREQ
             -
             - Frequency of mode ``N``. Returned values are valid for modal analyses which calculate real eigensolutions.
           * - STAB
             -
             - Stability value of mode ``N``. Returned values are valid for modal analyses which calculate complex eigensolutions. The stability value is the real part of the complex eigenvalue. It contains information on the mode damping in a damped modal analysis.
           * - DFRQ
             -
             - Damped frequency of mode ``N``. Returned values are valid for modal analyses which calculate complex eigensolutions. The damped frequency is the imaginary part of the complex eigenvalue.
           * - PFACT
             -
             - Participation factor of mode ``N``.   * If retrieved after a modal analysis, the real part of the participation factor is returned unless   ``IT1NUM`` = IMAG. The direction is specified using ``Item2`` = DIREC and ``IT2NUM`` = X, Y, Z,   ROTX, ROTY, or ROTZ   * If retrieved after a spectrum analysis, the spectrum number M is specified using ``Item2`` = SPECT   and ``IT2NUM`` = M.    For a PSD analysis with spatial correlation or wave excitation, the retrieved participation factors will correspond to the first degree of freedom that is excited.
           * - EFFM
             -
             - Effective mass of mode ``N``. Returned values are valid only after a modal analysis with effective mass calculation has been solved. The direction is specified using ``Item2`` = DIREC and ``IT2NUM`` = X, Y, Z, ROTX, ROTY, or ROTZ.
           * - GENM
             -
             - Generalized mass (also called modal mass) of mode ``N``. Returned values are valid only after a modal analysis with generalized mass calculation has been solved.
           * - MCOEF
             -
             - Mode coefficient of mode ``N``. Returned values are valid only after a spectrum analysis has been solved. The spectrum number M is specified using ``Item2`` = SPECT and ``IT2NUM`` = M. In a SPRS analysis, the values returned are based on the curve with the lowest damping.   After a PSD analysis, the diagonal of the dynamic modal covariance matrix is retrieved for the displacement solution.
           * - DAMP
             -
             - Damping ratio of mode ``N``. If retrieved after a modal analysis that creates complex solutions (DAMP, QRDAMP, or UNSYM eigensolvers) returned value is calculated from the complex frequencies. If retrieved after a spectrum analysis, returned value is the effective damping ratio. Not a function of direction. Also retrievable following a harmonic analysis or transient analysis with mode-superposition.

        For all items except PFACT and MCOEF (as noted above), only the first 10000 values corresponding to
        significant modes will be returned.

        The MODE file must be available to retrieve items PFACT and MCOEF with specified ``Item2``. If
        ``Item2`` is not specified, the last calculated value will be returned.

        All values retrieved correspond to the first load step values. For a Campbell diagram analysis
        (multistep modal), :ref:`get` with ``Entity`` = CAMP must be used.

        .. _get_sol_ddam:

        \*GET Solution Items, Entity = DDAM
        ***********************************

        .. flat-table:: ``Entity`` = DDAM, ``ENTNUM`` = ``N`` (mode number)
           :header-rows: 2

           * - :ref:`get`, ``Par``,DDAM, ``N``, ``Item1``, ``IT1NUM``
           * - Item1
             - IT1NUM
             - Description
           * - DSHOCK
             -
             - Shock design value of mode ``N``.

        If multiple DDAM analyses are performed, the last calculated value will be returned.

        **Postprocessing Items**

        .. _gettabpost:

        \*GET Postprocessing Entity Items
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        * :ref:`get_post_act`

        * :ref:`get_post_acus`

        * :ref:`get_post_camp`

        * :ref:`get_post_cint`

        * :ref:`get_post_cyccalc`

        * :ref:`get_post_elem`

        * :ref:`get_post_etab`

        * :ref:`get_post_fsum`

        * :ref:`get_post_gsresult`

        * :ref:`get_post_member`

        * :ref:`get_post_node`

        * :ref:`get_post_path`

        * :ref:`get_post_plnsol`

        * :ref:`get_post_prenergy`

        * :ref:`get_post_prerr`

        * :ref:`get_post_rad`

        * :ref:`get_post_rstmac`

        * :ref:`get_post_secr`

        * :ref:`get_post_section`

        * :ref:`get_post_sort`

        * :ref:`get_post_ssum`

        * :ref:`get_post_vari`

        * :ref:`get_prep_xfem`

        .. _get_post_act:

        \*GET Postprocessing Items, Entity = ACTIVE
        *******************************************

        .. flat-table:: ``Entity`` = ACTIVE, ``ENTNUM`` = 0 (or blank)
           :header-rows: 2

           * - :ref:`get`, ``Par``, ACTIVE, 0, ``Item1``, ``IT1NUM``, ``Item2``, ``IT2NUM``
           * - Item1
             - IT1NUM
             - Description
           * - :rspan:`4` SET
             - LSTP
             - Current load step number.
           * - SBST
             - Current substep number.
           * - TIME
             - Time associated with current results in the database.
           * - FREQ
             - Frequency (for ANTYPE=MODAL, HARMIC, SPECTR; load factor for ANTYPE=BUCKLE).
           * - NSET
             - If Item2 is blank, number of data sets on result file.   * If Item2 = FIRST, IT2NUM = Loadstep, get set number of first substep of loadstep * If Item2 = LAST, IT2NUM = Loadstep, get set number of last substep of loadstep
           * - RSYS
             -
             - Active results coordinate system.


        .. _get_post_acus:

        \*GET Postprocessing Items, Entity = ACUS
        *****************************************

        .. flat-table:: ``Entity`` = ACUS, ``ENTNUM`` = 0 (or blank)
           :header-rows: 2

           * - :ref:`get`, ``Par``, ACUS, 0, ``Item1``, ``IT1NUM``, ``Item2``, ``IT2NUM``
           * - Item1
             - IT1NUM
             - Description
           * - PWL
             -
             - Radiated sound power level
           * - PRES
             -
             - Far-field pressure at a given point
           * - PHASE
             -
             - Far-field pressure phase at a given point
           * - SPL
             -
             - Far-field sound pressure level at a given point
           * - SPLA
             -
             - Far-field a-weighted sound pressure level at a given point
           * - DG
             -
             - Far-field directivity at a given point
           * - PS
             -
             - Far-field scattered pressure at a given point
           * - TS
             -
             - Far-field target strength at a given point
           * - DFIN
             -
             - Diffuse sound field incident power
           * - SIMP
             -
             - Magnitude of specific acoustic impedance on the selected surface
           * - AIMP
             -
             - Magnitude of acoustic impedance on the selected surface
           * - MIMP
             -
             - Magnitude of mechanical impedance on the selected surface
           * - APRES
             -
             - Magnitude of average pressure on the selected surface
           * - FORC
             -
             - Magnitude of average force on the selected surface
           * - POWER
             -
             - Acoustic power through the selected surface
           * - BSPL
             -
             - SPL over frequency band
           * - BSPA
             -
             - A-weighted SPL over frequency band
           * - PWRF
             -
             - Reference sound power
           * - TL
             -
             - Transmission loss
           * - RL
             -
             - Return loss
           * - Item1 = PWL, PRES, SPL, SPLA, PHASE, DG, PS, and TS are available after issuing the :ref:`prfar` or :ref:`plfar` command. The maximum values are obtained from the current command.   Item1 = SIMP, AIMP, MIMP, APRES, FORC, POWER, TL, and RL are available after issuing the corresponding :ref:`pras` command at the current frequency. The values are obtained at the current frequency, or at the last frequency for multiple load step and substep cases.   Item1 = DFIN is available after the diffuse sound field solution.


        .. _get_post_camp:

        \*GET Postprocessing Items, Entity = CAMP
        *****************************************

        .. flat-table:: Available after :ref:`plcamp` or :ref:`prcamp` command is issued.   ``Entity`` = CAMP, ``ENTNUM`` = ``N`` (mode number)
           :header-rows: 2

           * - :ref:`get`, ``Par``, CAMP, ``N``, ``Item1``, ``IT1NUM``, ``Item2``, ``IT2NUM``
           * - Item1
             - IT1NUM
             - Description
           * - NBMO
             -
             - Number of modes in the Campbell diagram ( ``ENTNUM`` not required). This value is the maximum value for ``N``.
           * - NBST
             -
             - Number of steps in the Campbell diagram: modal load steps with rotational velocity ( ``ENTNUM`` not required). This value is the maximum value for ``M`` (see Item1 = FREQ).
           * - WHRL
             - ``M``
             - Whirl of mode ``N``  at step ``M``  : -1 is backward whirl, 1 is forward whirl, and 0 is undetermined. For default ``IT1NUM``, it corresponds to the whirl at the maximum rotational velocity.
           * - VCRI
             -
             - Critical speed for mode ``N``. This value is available if an excitation is defined via the :ref:`plcamp` or :ref:`prcamp` command's ``SLOPE`` argument. (The unit of speed depends upon the ``UNIT`` value specified in those commands.)   N does not correspond to the mode number if ``FREQB`` ( :ref:`prcamp` or :ref:`plcamp` command) is used. Instead, it represents the Nth mode number listed in the output of :ref:`prcamp` or :ref:`plcamp`.
           * - FREQ
             - ``M``
             - Natural frequency of mode (Hz) ``N`` at step ``M``. It represents the complex part of the eigenvalue.
           * - STAB
             - ``M``
             - Stability value (Hz) of mode ``N`` at step ``M``. It represents the real part of the eigenvalue.
           * - UKEY
             - ``M``
             - Instability key for mode ``N``  at step ``M``  : 0 is stable and 1 is unstable. For default ``IT1NUM``, it corresponds to the stability over the whole rotational velocity range.
           * - VSTA
             -
             - Stability limit for mode N. This value is available when ``SLOPE`` is zero on the :ref:`plcamp` or :ref:`prcamp` command. (The unit of speed depends upon the ``UNIT`` value specified in those commands.)   N does not correspond to the mode number if ``FREQB`` ( :ref:`prcamp` or :ref:`plcamp` command) is used. Instead, it represents the Nth mode number listed in the output of :ref:`prcamp` or :ref:`plcamp`.

        If the sorting is activated (Option= ``ON`` on the :ref:`prcamp` and :ref:`plcamp` commands), all
        the parameters retrieved are in the sorted order.

        .. _get_post_cint:

        \*GET Postprocessing Items, Entity = CINT
        *****************************************

        .. flat-table:: ``Entity`` = CINT, ``ENTNUM`` = ``CrackId`` (required Crack ID number)
           :header-rows: 2

           * - :ref:`get`, ``Par``, CINT, ``CrackId``, ``Item1``, ``IT1NUM``, ``Item2``, ``IT2NUM``
           * - Item1
             - IT1NUM
             - Description
           * - CTIP
             - ctnum
             - ``IT1NUM`` = Crack tip node number (required)   ``Item2`` = CONTOUR   ``IT2NUM`` = Contour number (default 1)   Returns JINT value if crack ID is JINT type; otherwise, returns 0.   ``Item1`` defaults to CTIP, ``Item2`` defaults to CONTOUR.
           * - **Entity= CINT,** ``ENTNUM`` = CrackID (required Crack ID number)
           * - **\*GET ,** ``Par``, CINT, ``CrackId``, ``Item1``, ``IT1NUM``, ``Item2``, ``IT2NUM``, ``Item3``, ``IT3NUM``, ``Item4``, ``IT4NUM``
           * - **Item1**
             - **IT1NUM**
             - **Description**
           * - CTIP
             - ctnum
             - ``IT1NUM`` = Crack tip node number (required)   ``Item2`` = CONTOUR   ``IT2NUM`` = Contour number (default 1)   ``Item3`` = DTYPE   ``IT3NUM`` = Data type (JINT, IIN1, IIN2, IIN3, K1, K2, K3, G1, G2, G3, GT, MFTX, MFTY, MFTZ, TSTRESS, CEXT, STTMAX, PSMAX, CSTAR, DLTA, DLTN, DLTK, R, UFAC, CRDX, CRDY, CRDZ, and APOS)     FOR ``IT3NUM`` = STTMAX or PSMAX:    * Item4 = AINDEX (angle index)   * IT4NUM = Index value (1 to N+1; N = Maximum number of intervals for the sweep (   :ref:`cint`,RSWEEP).   Returns specified data type value.         FOR ``IT3NUM`` = DLTA, DLTN, DLTK, R, UFAC, CRDX, CRDY, CRDZ, APOS:    * Set ``IT2NUM`` = 1   Returns specified data type value.       ``Item1`` defaults to CTIP, ``Item2`` defaults to CONTOUR, ``Item3`` defaults to DTYPE.   DLTK in a 3D XFEM-based fatigue crack-growth analysis is evaluated based on the smoothed SIFS values. The actual DLTK value can be easily calculated by issuing :ref:`get` for SIFS values and the stress (load) ratio.
           * - **Entity= CINT,** ``ENTNUM`` = CrackID (required Crack ID number)
           * - **\*GET ,** ``Par``, CINT, ``CrackId``, ``Item1``, ``IT1NUM``, ``Item2``, ``IT2NUM`` ,
           * - **Item1**
             - **IT1NUM**
             - **Description**
           * - NNOD
             -
             - Maximum number of nodes along the crack front.
           * - **Entity= CINT,** ``ENTNUM`` = CrackID (required Crack ID number)
           * - **\*GET ,** ``Par``, CINT, ``CrackId``, ``Item1``, ``IT1NUM``, ``Item2``, ``IT2NUM``
           * - **Item1**
             - **IT1NUM**
             - **Description**
           * - NODE
             - ipos
             - IT1NUM = Position along the crack front (from 1 to NNOD). Default = 1. Returns node number at the given position along the crack front. (For XFEM, an internal node number is returned.)


        .. _get_post_cyccalc:

        \*GET Postprocessing Items, Entity = CYCCALC
        ********************************************

        .. flat-table:: ``Entity`` = CYCCALC, ``ENTNUM`` = :ref:`cycspec` specification number Generate date for cyclic results using :ref:`cyccalc` before retrieving those items.
           :header-rows: 2

           * - :ref:`get`, ``Par``,CYCCALC, ``spec``, ``Item1``, ``IT1NUM``, ``Item2``, ``IT2NUM``
           * - Item1
             - IT1NUM
             - Item2
             - IT2NUM
             - Description
           * - :rspan:`3` FREQ
             - :rspan:`3` frequency point
             - SECTOR
             - sector
             - :ref:`cycspec` result at the IT1NUM frequency and IT2NUM sector
           * - SECMAX
             - -
             - :ref:`cycspec` maximum result at the IT1NUM frequency
           * - SECNUM
             - -
             - :ref:`cycspec` sector with the maximum result at the IT1NUM frequency
           * - SECNODE
             - -
             - :ref:`cycspec` node in the sector with the maximum result at the IT1NUM frequency
           * - The frequency point refers to the harmonic solution data set number (NSET on the :ref:`set` command)


        .. _get_post_elem:

        \*GET Postprocessing Items, Entity = ELEM
        *****************************************

        .. flat-table:: ``Entity`` = :ref:`elem`, ``ENTNUM`` = ``N`` (element number)
           :header-rows: 2

           * - :ref:`get`, ``Par``, ELEM, ``N``, ``Item1``, ``IT1NUM``, ``Item2``, ``IT2NUM``
           * - Item1
             - IT1NUM
             - Description
           * - SERR Some element- and material-type limitations apply. For more information, see the documentation for the :ref:`prerr` command.
             -
             - Structural error energy.
           * - SDSG
             -
             - Absolute value of the maximum variation of any nodal stress component.
           * - TERR
             -
             - Thermal error energy.
           * - TDSG
             -
             - Absolute value of the maximum variation of any nodal thermal gradient component.
           * - SENE
             -
             - "Stiffness" energy or thermal heat dissipation. Same as TENE.
           * - TENE
             -
             - Thermal heat dissipation or "stiffness" energy. Same as SENE.
           * - KENE
             -
             - Kinetic energy.
           * - ASENE
             -
             - Amplitude “stiffness” energy.
           * - PSENE
             -
             - Peak “stiffness” energy.
           * - AKENE
             -
             - Amplitude kinetic energy.
           * - PKENE
             -
             - Peak kinetic energy.
           * - DENE
             -
             - Damping energy.
           * - WEXT WEXT is calculated for element-based loading only (and not for nodal-force loading). WEXT is stored on elements to which loading has been applied; if surface elements are added on top of other elements, for example, and pressure loading is applied to the surface elements, WEXT is available for the surface elements only.
             -
             - Work due to external load.
           * - JHEAT
             -
             - Element Joule heat generation (coupled-field calculation).
           * - JS
             - X, Y, Z
             - Source current density (coupled-field calculation) in the global Cartesian coordinate system.
           * - HS
             - X, Y, Z
             - Average element magnetic field intensity from current sources.
           * - VOLU
             -
             - Element volume, as calculated during solution.
           * - ETAB
             - ``Lab``
             - Value of element table item ``Lab`` for element ``N`` (see :ref:`etable` command).
           * - EFOR
             - ``Nnum``
             - Element force at node ``Nnum``. The force label is specified using Item2 = FX, FY, FZ, MX, MY, MZ, or HEAT.   In a dynamics analysis, the element forces returned are based on the type of force requested. It is specified using the :ref:`force` command for all dynamics analyses, except for spectrum analyses where ``ForceType`` is used on the combination commands ( :ref:`srss`, :ref:`psdcom`, etc.).
           * - SMISC
             - ``Snum``
             - Value of element summable miscellaneous data at sequence number ``Snum`` (as used on :ref:`etable` command).
           * - NMISC
             - ``Snum``
             - Value of element non-summable miscellaneous data at sequence number ``Snum`` (as used on :ref:`etable` command).
           * - FSOU
             -
             - Element fluid flow source loading (poromechanics).


        .. _get_post_etab:

        \*GET Postprocessing Items, Entity = ETAB
        *****************************************

        .. flat-table:: ``Entity`` = ETAB, ``ENTNUM = N`` (column number)
           :header-rows: 2

           * - :ref:`get`, ``Par``, ETAB, ``N``, ``Item1``, ``IT1NUM``, ``Item2``, ``IT2NUM``
           * - Item1
             - IT1NUM
             - Description
           * - LAB
             -
             - Label for column ``N`` of the element table ( :ref:`etable` ). Returns a character parameter.
           * - ELEM
             - ``E``
             - Value in :ref:`etable` column ``N`` for element number ``E``.


        .. _get_post_fsum:

        \*GET Postprocessing Items, Entity = FSUM
        *****************************************

        .. flat-table:: ``Entity`` = :ref:`fsum`, ``ENTNUM`` = 0 (or blank)
           :header-rows: 2

           * - :ref:`get`, ``Par``, FSUM, 0, ``Item1``, ``IT1NUM``, ``Item2``, ``IT2NUM``
           * - Item1
             - IT1NUM
             - Description
           * - ITEM
             - ``Lab``
             - Value of item ``Lab`` from last :ref:`fsum` command. Valid labels are FX, FY, FZ, MX, MY, MZ, FLOW, HEAT, FLUX, etc.


        .. _get_post_gsresult:

        \*GET Postprocessing Items, Entity = GSRESULT
        *********************************************

        .. flat-table:: ``Entity`` = GSRESULT, ``ENTNUM`` = 0 (or blank) for generalized plane strain results in fiber direction
           :header-rows: 2

           * - :ref:`get`, ``Par``, GSRESULT, 0, ``Item1``, ``IT1NUM``
           * - Item1
             - IT1NUM
             - Description
           * - LFIBER
             -
             - Fiber length change at ending point.
           * - ROT
             - X,Y
             - Rotation angle of end plane about X or Y axis.
           * - F
             -
             - Reaction force at ending point.
           * - M
             - X,Y
             - Reaction moment on ending plane.


        .. _get_post_member:

        \*GET Postprocessing Items, Entity = MEMBER
        *******************************************

        .. flat-table:: ``Entity`` = MEMBER, ``ENTNUM`` = ``N`` (GroupID)
           :header-rows: 2

           * - :ref:`get`, ``Par``,MEMBER, ``N``, ``Item1``, ``IT1NUM``
           * - Item1
             - IT1NUM
             - Description
           * - TEMP
             - MIN, MAX
             - Minimum or maximum temperature of members (individual reinforcings) with GroupID = ``N`` in the selected set of reinforcing elements.


        .. _get_post_node:

        \*GET Postprocessing Items, Entity = NODE
        *****************************************

        .. flat-table:: ``Entity`` = ``NODE``, ``ENTNUM`` = ``N`` (node number) for nodal degree-of-freedom results:
           :header-rows: 2

           * - :ref:`get`, ``Par``, NODE, ``N``, ``Item1``, ``IT1NUM``, ``Item2``, ``IT2NUM``
           * - Item1
             - IT1NUM
             - Description
           * - U
             - X, Y, Z, SUM
             - X, Y, or Z structural displacement or vector sum. Alternative get functions: UX( ``N`` ), UY( ``N`` ), UZ( ``N`` ).
           * - ROT
             - X, Y, Z, SUM
             - X, Y, or Z structural rotation or vector sum. Alternative get functions: ROTX( ``N`` ), ROTY( ``N`` ), ROTZ( ``N`` ).
           * - TEMP
             -
             - Temperature. For ``SHELL131`` and ``SHELL132`` elements with KEYOPT(3) = 0 or 1, use TBOT, TE2, TE3,..., TTOP instead of TEMP. Alternative get functions: TEMP( ``N`` ), TBOT( ``N`` ), TE2( ``N`` ), etc.
           * - PRES
             -
             - Pressure. Alternative get function: PRES( ``N`` ).
           * - GFV1, GFV2, GFV3
             -
             - Nonlocal field values 1, 2, and 3.
           * - VOLT
             -
             - Electric potential. Alternative get function: VOLT( ``N`` ).
           * - CONC
             -
             - Concentration.
           * - MAG
             -
             - Magnetic scalar potential. Alternative get function: MAG( ``N`` ).
           * - V
             - X, Y, Z, SUM
             - X, Y, or Z fluid velocity or vector sum in a fluid analysis. X, Y, or Z nodal velocity or vector sum in a structural transient analysis (analysis with :ref:`antype`,TRANS). Alternative get functions: VX( ``N`` ), VY( ``N`` ), VZ( ``N`` ).
           * - A
             - X, Y, Z, SUM
             - X, Y, or Z magnetic vector potential or vector sum in an electromagnetic analysis. X, Y, or Z nodal acceleration or vector sum in a structural transient analysis (analysis with :ref:`antype`,TRANS). Alternative get functions: AX( ``N`` ), AY( ``N`` ), AZ( ``N`` ).
           * - CURR
             -
             - Current.
           * - EMF
             -
             - Electromotive force drop.
           * - RF
             - FX, FY, FZ, MX, MY, MZ, CSGZ, BMOM, RATE, DVOL, FLOW, HEAT, AMPS or CHRG, FLUX, CURT, VLTG
             - Nodal reaction forces in the nodal coordinate system. The reaction forces returned are the total forces: static, plus damping, plus inertial, as appropriate based on analysis type (see :ref:`prrsol` command). The first exception is modal analyses and mode-superposition transient analyses where static forces are returned. The second exception is spectrum analyses where the :ref:`prrfor` logic is used internally. In this case, the reaction forces are based on the type of force requested (using ``ForceType`` with combination commands, such as :ref:`srss`, :ref:`psdcom`, etc.).
           * - ORBT
             - A, B, PSI, PHI, YMAX, ZMAX, Whirl
             - Whirl orbit characteristics:     * A is the semi-major axis. * B is the semi-minor axis. * PSI is the angle between the local axis y and the major axis Y. * PHI is the angle between initial position (t = 0) and major axis. * YMAX is the maximum displacement along local y axis. * ZMAX is the maximum displacement along local z axis. * Whirl is the direction of an orbital motion (-1 is backward whirl, 1 is forward whirl, and 0 is   undetermined).  Angles PSI and PHI are in degrees and within the range of -180 through +180.   Orbits are available only after issuing a :ref:`prorb` command.
           * - Use this command carefully when N represents an internal node, as the nodal degrees of freedom may have different physical meanings.


        .. _get_post_path:

        \*GET Postprocessing Items, Entity = PATH
        *****************************************

        .. flat-table:: Entity = PATH, ``ENTNUM`` = 0 (or blank)
           :header-rows: 2

           * - :ref:`get`, ``Par``, PATH, 0, ``Item1``, ``IT1NUM``, ``Item2``, ``IT2NUM``
           * - Item1
             - IT1NUM
             - Description
           * - MAX
             - ``Lab``
             - Maximum value of path item ``Lab`` from last path operation. Valid labels are the user-defined labels on the :ref:`pdef` or :ref:`pcalc` command.
           * - MAXPATH
             -
             - Returns the maximum path number defined.
           * - MIN
             - ``Lab``
             - Minimum value of path item ``Lab`` from last path operation. Valid labels are the user-defined labels on the :ref:`pdef` or :ref:`pcalc` command.
           * - LAST
             - ``Lab``
             - Last value of path item ``Lab`` from last path operation. Valid labels are the user-defined labels on the :ref:`pdef` or :ref:`pcalc` command.
           * - NODE
             -
             - Value providing the number of nodes defining the path referenced in the last path operation.
           * - ITEM
             - ``Lab``
             - **Item2** = PATHPT, **IT2NUM** = n The value of ``Lab`` at the ``n`` th data point from the last path operation.
           * - POINT
             - ``n``
             - **Item2** = X,Y,Z, or CSYS. Returns information about the nth point on the current path.
           * - NVAL
             -
             - The number of path data points (the length of the data table) from the last path operation.
           * - SET
             - ``n``
             - **Item2** = NAME. Returns the name of the n th data set on the current path.
           * - NUMPATH
             -
             - Returns the number of paths defined.


        .. _get_post_plnsol:

        \*GET Postprocessing Items, Entity = PLNSOL
        *******************************************

        .. flat-table:: ``Entity`` = :ref:`plnsol`  You must issue the :ref:`show` command before commands that produce a graphical output when running in batch mode to produce/export graphic files. For more details, see `External Graphics Options <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/Hlp_G_BAS16_1.html#basexunijla61499>`_, ``ENTNUM`` = 0 (or blank)
           :header-rows: 2

           * - :ref:`get`, ``Par``, PLNSOL, 0, ``Item1``, ``IT1NUM``, ``Item2``, ``IT2NUM``
           * - Item1
             - IT1NUM
             - Description
           * - MAX
             -
             - Maximum value of item in last contour display ( :ref:`plnsol`, :ref:`plesol` ).
           * - MIN
             -
             - Minimum value of item in last contour display ( :ref:`plnsol`, :ref:`plesol` ).
           * - BMAX
             -
             - Maximum bound value of item in last contour display ( :ref:`plnsol`, :ref:`plesol` ).
           * - BMIN
             -
             - Minimum bound value of item in last contour display ( :ref:`plnsol`, :ref:`plesol` ).


        .. _get_post_prenergy:

        \*GET Postprocessing Items, Entity = PRENERGY
        *********************************************

        .. flat-table:: Available after the :ref:`prenergy` command is issued.   ``Entity`` = PRENERGY, ``ENTNUM`` = ``N`` (component number)
           :header-rows: 2

           * - :ref:`get`, ``Par``, PRENERGY, ``N``, ``Item1``, ``IT1NUM``
           * - Item1
             - IT1NUM
             - Description
           * - NCMP
             -
             - Number of components ( ``ENTNUM`` not required). This value is the maximum value for ``N``.
           * - NENE
             -
             - Number of energy types ( ``ENTNUM`` not required). This value is the maximum value for ``M``.
           * - TOTE
             - ``M``
             - Total energy of type ``M`` of the model ( ``ENTNUM`` not required). Energy value is non-zero when ``Cname1`` is blank on prior :ref:`prenergy` command.
           * - ENG
             - ``M``
             - Energy of type ``M`` of component ``N``. Energy value is non-zero when ``Cname1`` is specified on prior :ref:`prenergy` command.
           * - PENG
             - ``M``
             - Percentage of energy of type ``M`` of component ``N``. Percentage of energy value is non-zero when ``Cname1`` is specified on prior :ref:`prenergy` command.
           * - Ordering of ``N`` and ``M`` corresponds to :ref:`prenergy` output.


        .. _get_post_prerr:

        \*GET Postprocessing Items, Entity = PRERR
        ******************************************

        .. flat-table:: ``Entity`` = PRERR, ``ENTNUM`` = 0 (or blank)
           :header-rows: 2

           * - :ref:`get`, ``Par``, PRERR, 0, ``Item1``, ``IT1NUM``, ``Item2``, ``IT2NUM``
           * - Item1
             - IT1NUM
             - Description
           * - SEPC[ :ref:`starget_prerr_limits` ]
             -
             - Structural percent error in energy norm ( :ref:`prerr` ).
           * - TEPC[ :ref:`starget_prerr_limits` ]
             -
             - Thermal percent error in energy norm ( :ref:`prerr` ).
           * - SERSM[ :ref:`starget_prerr_limits` ]
             -
             - Structural error energy summation ( :ref:`prerr` ).
           * - TERSM[ :ref:`starget_prerr_limits` ]
             -
             - Thermal error energy summation ( :ref:`prerr` ).
           * - SENSM[ :ref:`starget_prerr_limits` ]
             -
             - Structural energy summation ( :ref:`prerr` ).
           * - TENSM[ :ref:`starget_prerr_limits` ]
             -
             - Thermal energy summation ( :ref:`prerr` ).

        .. _starget_prerr_limits:

        Some element- and material-type limitations apply. For more information, see the documentation for
        the :ref:`prerr` command.

        .. _get_post_rad:

        \*GET Postprocessing Items, Entity = RAD
        ****************************************

        .. flat-table:: ``Entity`` = RAD, ENTNUM = 0 (or blank)
           :header-rows: 2

           * - :ref:`get`, ``Par``, RAD, 0, ``Item1``, ``IT1NUM``, ``Item2``, ``IT2NUM``
           * - Item1
             - IT1NUM
             - Description
           * - VFAVG
             -
             - Value of the average view factor computed from the previous VFQUERY command.


        .. _get_post_rstmac:

        \*GET Postprocessing Items, Entity = RSTMAC
        *******************************************

        .. flat-table:: Available after :ref:`rstmac` command is issued.   ``Entity`` = :ref:`rstmac`, ``ENTNUM`` = ``N`` (solution number on ``File1`` )
           :header-rows: 2

           * - :ref:`get`, ``Par``, RSTMAC, 0 or ``N``, ``Item1``, ``IT1NUM``, ``Item2``, ``IT2NUM``
           * - Item1
             - IT1NUM
             - Description
           * - NS1
             -
             - Total number of solutions (modes for example) read on ``File1``. See ``Sbstep1`` on the :ref:`rstmac` command. This value is the maximum value for ``N``.
           * - NS2
             -
             - Total number of solutions (modes for example) read on ``File2``. See ``Sbstep2`` on the :ref:`rstmac` command. This value is the maximum value for ``M``
           * - MAC
             - M
             - Modal assurance criterion value (MAC) between the solution ``N`` read on ``File1`` and the solution ``M`` read on ``File2``.   ``N`` and ``M`` do not correspond to the substep (or mode) numbers if NS1 and NS2 are different from the total number of substeps (or modes).
           * - MACCYC
             - M
             - Modal assurance criterion value (MAC) from compressed table for :ref:`cyclic` between the solution ``N`` read on ``File1`` and the solution ``M`` read on ``File2``. ``N`` and ``M`` do not correspond to the substep (or mode) numbers if NS1 and NS2 are different from the total number of substeps (or modes).


        .. _get_post_secr:

        \*GET Postprocessing Items, Entity = SECR
        *****************************************

        .. flat-table:: ``Entity`` = SECR, ``ENTNUM`` = ``n`` (element number) For beam and pipe (including elbow) section results, return values for all elements   if the element number ( ``n`` ) is blank or ALL.
           :header-rows: 2

           * - :ref:`get`, ``Par``, SECR, n, ``Item1``, ``IT1NUM``, ``Item2``, ``IT2NUM``
           * - Item1
             - IT1NUM
             - Description
             - Item2
             - IT2NUM
           * - :rspan:`3` S
             - X, Y, Z, XY, YZ, XZ
             - Component total stress
             - :rspan:`39` MAX - Returns maximum   MIN - Returns minimum   MAXY - Returns section Y location of maximum   MAXZ - Returns section Z location of maximum   MINY - Returns section Y location of minimum   MINZ - Returns section Z location of minimum   IVAL - Returns value at node or integration point at element I node   JVAL - Returns value at node or integration point at element J node   KVAL - Returns value at node or integration point at element K node ( ``ELBOW290`` )   ---   **For IVAL, JVAL, and KVAL:** The ALL (or blank) option for the element number is not valid. You must specify an element ( **n** ).
             - :rspan:`39` These values are applicable only when Item2 = IVAL, JVAL, or KVAL:   When KEYOPT(15) = 0, this value is the section node number (which can be visualized via :ref:`secplot`,,2).   When KEYOPT(15) = 1 (or when using elbow elements), this value is the integration point number.
           * - 1, 2, 3
             - Principal stress value
           * - INT
             - Stress intensity value
           * - EQV
             - Equivalent stress value
           * - :rspan:`3` EPTO
             - X, Y, Z, XY, YZ, XZ
             - Component total strain
           * - 1, 2, 3
             - Principal total strain value
           * - INT
             - Total strain intensity value
           * - EQV
             - Equivalent total strain value
           * - :rspan:`3` EPEL
             - X, Y, Z, XY, YZ, XZ
             - Component elastic strain
           * - 1, 2, 3
             - Principal elastic strain value
           * - INT
             - Elastic strain intensity value
           * - EQV
             - Equivalent elastic strain value
           * - :rspan:`3` EPTH
             - X, Y, Z, XY, YZ, XZ
             - Component thermal strain
           * - 1, 2, 3
             - Principal thermal strain value
           * - INT
             - Thermal strain intensity value
           * - EQV
             - Equivalent thermal strain value
           * - :rspan:`3` EPPL
             - X, Y, Z, XY, YZ, XZ
             - Component plastic strain
           * - 1, 2, 3
             - Principal plastic strain value
           * - INT
             - Plastic strain intensity value
           * - EQV
             - Equivalent plastic strain value
           * - :rspan:`3` EPCR
             - X, Y, Z, XY, YZ, XZ
             - Component creep strain
           * - 1, 2, 3
             - Principal component creep strain value
           * - INT
             - Component creep strain intensity value
           * - EQV
             - Equivalent component creep strain value
           * - :rspan:`3` EPTT
             - X, Y, Z, XY, YZ, XZ
             - Component total mechanical and thermal and swelling strain
           * - 1, 2, 3
             - Principal total mechanical and thermal and swelling strain value
           * - INT
             - Total mechanical and thermal and swelling strain intensity value
           * - EQV
             - Equivalent total mechanical and thermal and swelling strain value
           * - :rspan:`3` EPDI
             - X, Y, Z, XY, YZ, XZ
             - Component diffusion strain
           * - 1, 2, 3
             - Principal diffusion strain value
           * - INT
             - Diffusion strain intensity value
           * - EQV
             - Equivalent diffusion strain value
           * - :rspan:`5` NL
             - SEPL
             - Plastic yield stress
           * - SRAT
             - Plastic yielding (1 = actively yielding, 0 = not yielding)
           * - HPRES
             - Hydrostatic pressure
           * - EPEQ
             - Accumulated equivalent plastic strain
           * - CREQ
             - Accumulated equivalent creep strain
           * - PLWK
             - Plastic work/volume
           * - YSIDX
             - TENS,SHEA
             - Yield surface activity status: 1 for yielded and 0 for not yielded.
           * - FPIDX
             - TF01,SF01, TF02,SF02, TF03,SF03, TF04,SF04
             - Failure plane surface activity status: 1 for yielded and 0 for not yielded. Tension and Shear failure status are available for all four sets of failure planes.


        .. _get_post_section:

        \*GET Postprocessing Items, Entity = SECTION
        ********************************************

        .. flat-table:: ``Entity`` = SECTION, ``ENTNUM`` = ``component`` (listed below). Generate data for section stress results, using :ref:`prsect` before retrieving these items. Valid labels for ``ENTNUM`` are MEMBRANE, BENDING, SUM (Membrane+Bending), PEAK, and TOTAL. (The following items are not stored in the database and the values returned reflect the last quantities generated by :ref:`prsect` or :ref:`plsect`.) Only MEMBRANE, BENDING, and SUM data are available after a :ref:`plsect` command. The MEMBRANE label is only valid with ``Item1`` = INSIDE.
           :header-rows: 2

           * - :ref:`get`, ``Par``, SECTION, ``component``, ``Item1``, ``IT1NUM``, ``Item2``, ``IT2NUM``
           * - Item1
             - IT1NUM
             - Item2
             - Description
           * - :rspan:`2` INSIDE
             - :rspan:`2` S
             - X, Y, Z, XY, YZ, XZ
             - Stress component at beginning of path.
           * - 1, 2, 3
             - Principal stress at beginning of path.
           * - INT, EQV
             - Stress intensity or equivalent stress at beginning of path.
           * - :rspan:`2` CENTER
             - :rspan:`2` S
             - X, Y, Z, XY, YZ, XZ
             - Stress component at midpoint of path.
           * - 1, 2, 3
             - Principal stress at midpoint of path.
           * - INT, EQV
             - Stress intensity or equivalent stress at midpoint of path.
           * - :rspan:`2` OUTSIDE
             - :rspan:`2` S
             - X, Y, Z, XY, YZ, XZ
             - Stress component at end of path.
           * - 1, 2, 3
             - Principal stress at end of path.
           * - INT, EQV
             - Stress intensity or equivalent stress at end of path.


        .. _get_post_sort:

        \*GET Postprocessing Items, Entity = SORT
        *****************************************

        .. flat-table:: ``Entity`` = SORT, ``ENTNUM`` = 0 (or blank)
           :header-rows: 2

           * - :ref:`get`, ``Par``, SORT, 0, ``Item1``, ``IT1NUM``, ``Item2``, ``IT2NUM``
           * - Item1
             - IT1NUM
             - Description
           * - MAX
             -
             - Maximum value of last sorted item ( :ref:`nsort` or :ref:`esort` command).
           * - MIN
             -
             - Minimum value of last sorted item ( :ref:`nsort` or :ref:`esort` command).
           * - IMAX
             -
             - Node/Element number where maximum value occurs.
           * - IMIN
             -
             - Node/Element number where minimum value occurs.


        .. _get_post_ssum:

        \*GET Postprocessing Items, Entity = SSUM
        *****************************************

        .. flat-table:: ``Entity`` = SSUM, ``ENTNUM`` = 0 (or blank)
           :header-rows: 2

           * - :ref:`get`, ``Par``, SSUM, 0, ``Item1``, ``IT1NUM``, ``Item2``, ``IT2NUM``
           * - Item1
             - IT1NUM
             - Description
           * - ITEM
             - ``Lab``
             - Value of item ``Lab`` from last :ref:`ssum` command. Valid labels are the user-defined labels on the :ref:`etable` command.


        .. _get_post_vari:

        \*GET Postprocessing Items, Entity = VARI
        *****************************************

        .. flat-table:: ``Entity`` = VARI, ``ENTNUM`` = ``N`` (variable number after POST26 data storage) (for complex values, only the real part is returned with Item1 = EXTREM)
           :header-rows: 2

           * - :ref:`get`, ``Par,VARI,N``, ``Item1``, ``IT1NUM``, ``Item2``, ``IT2NUM``
           * - Item1
             - IT1NUM
             - Description
           * - :rspan:`6` EXTREM
             - VMAX
             - Maximum extreme value.
           * - TMAX
             - Time or frequency corresponding to VMAX.
           * - VMIN
             - Minimum extreme value.
           * - TMIN
             - Time or frequency corresponding to VMIN.
           * - VLAST
             - Last value.
           * - TLAST
             - Time or frequency corresponding to VLAST.
           * - CVAR
             - Covariance
           * - REAL
             - f
             - Real part of variable ``N`` at time or frequency f.
           * - IMAG
             - f
             - Imaginary part of variable ``N`` at frequency f.
           * - AMPL
             - f
             - Amplitude value of variable ``N`` at frequency f
           * - PHASE
             - f
             - Phase angle value of variable ``N`` at frequency f
           * - RSET
             - ``Snum``
             - Real part of variable ``N`` at location ``Snum``.
           * - ISET
             - ``Snum``
             - Imaginary part of variable ``N`` at location ``Snum``.


        .. _get_prep_xfem:

        \*GET Postprocessing Items, Entity = XFEM
        *****************************************

        .. flat-table:: ``Entity`` = XFEM, ``ENTNUM`` = 0 (or blank)
           :header-rows: 2

           * - :ref:`get`, ``Par``, XFEM, 0, ``Item1``, ``IT1NUM``
           * - Item1
             - IT1NUM
             - Description
           * - STAT
             - ``Element Number``
             - Status of the element: 0 = uncracked, 1 = cracked

        """
        command = f"*GET,{par},{entity},{entnum},{item1},{it1num},{item2},{it2num}"
        return self.run(command, **kwargs)

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
            Specifies the type of file information returned:

            * ``EXIST`` - Returns a 1 if the specified file exists, and 0 if it does not.

            * ``DATE`` - Returns the date stamp of the specified file in the format ``yyyymmdd.hhmmss``.

            * ``SIZE`` - Returns the size of the specified file in MB.

            * ``WRITE`` - Returns the status of the write attribute. A 0 denotes no write permission while a 1
              denotes write permission.

            * ``READ`` - Returns the status of the read attribute. A 0 denotes no read permission while a 1
              denotes read permission.

            * ``EXEC`` - Returns the status of the execute attribute (this has meaning only on Linux). A 0
              denotes no execute permission while a 1 denotes execute permission.

            * ``LINES`` - Returns the number of lines in an ASCII file.

        Notes
        -----

        .. warning::

           This function contains specificities regarding the argument definitions.
           Please refer to the `command documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_INQUIRE.html>`_
           for further explanations.

        **Argument Descriptions**

        .. _s-INQUIRE_argdescript:

        * ``strarray : str`` - Name of the "string array" parameter that will hold the returned values.
          String array parameters are similar to character arrays, but each array element can be as long as
          248 characters. If the string parameter does not exist, it will be created.

        * ``func : str`` - Specifies the type of system information returned:

          * ``LOGIN`` - Returns the pathname of the login directory on Linux systems or the pathname of the
            default directory (including drive letter) on Windows systems.

          * ``DOCU`` - Returns the pathname of the Mechanical APDL docu directory.

          * ``APDL`` - Returns the pathname of the Mechanical APDL APDL directory.

          * ``PROG`` - Returns the pathname of the Mechanical APDL executable directory.

          * ``AUTH`` - Returns the pathname of the directory in which the license file resides.

          * ``USER`` - Returns the name of the user currently logged-in.

          * ``DIRECTORY`` - Returns the pathname of the current directory.

          * ``JOBNAME`` - Returns the current ``Jobname``.

          * ``RSTDIR`` - Returns rst directory ( ``FILE`` command).

          * ``RSTFILE`` - Returns rst file name ( ``FILE`` command).

          * ``RSTEXT`` - Returns rst file extension ( ``FILE`` command).

          * ``PSEARCH`` - Returns path used for "unknown command" macro ( :ref:`psearch` command).

          * ``OUTPUT`` - Returns the current output file name ( :ref:`output` command).

        Returning the Value of an Environment Variable to a Parameter
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        If ``FUNC`` =ENV, the command format is :ref:`inquire`, ``StrArray``,ENV, ``ENVNAME``,
        ``Substring``. In this instance, ENV specifies that the command should return the value of an
        environment variable. The following defines the remaining fields:

        * ``envname : str`` - Specifies the name of the environment variable.

        * ``substring : str`` - If ``Substring`` = 1, the first substring (up to the first colon (:)) is
          returned. If ``Substring`` = 2, the second substring is returned, etc. For Windows platforms, the
          separating character is semicolon (;). If this argument is either blank or 0, the entire value of
          the environment variable is returned.

        Returning the Value of a Title to a Parameter
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        If ``FUNC`` = TITLE, the command format is :ref:`inquire`, ``StrArray``,TITLE, ``Title_num``. In
        this context, the value of ``Title_num`` can be blank or 1 through 5. If the value is 1 or blank,
        the title is returned. If the value is 2 through 5, a corresponding subtitle is returned (2 denoting
        the first subtitle, and so on).

        Returning Information About a File to a Parameter
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        The :ref:`inquire` command can also return information about specified files within the file system.
        For these capabilities, the format is :ref:`inquire`, ``Parameter``, ``FUNC``,``Fname``, ``Ext``,
        ``--``. The
        following defines the fields:

        * ``parameter : str`` - Name of the parameter that will hold the returned values.

        * ``func : str`` - Specifies the type of file information returned:

          * ``EXIST`` - Returns a 1 if the specified file exists, and 0 if it does not.

          * ``DATE`` - Returns the date stamp of the specified file in the format ``yyyymmdd.hhmmss``.

          * ``SIZE`` - Returns the size of the specified file in MB.

          * ``WRITE`` - Returns the status of the write attribute. A 0 denotes no write permission while a 1
            denotes write permission.

          * ``READ`` - Returns the status of the read attribute. A 0 denotes no read permission while a 1
            denotes read permission.

          * ``EXEC`` - Returns the status of the execute attribute (this has meaning only on Linux). A 0
            denotes no execute permission while a 1 denotes execute permission.

          * ``LINES`` - Returns the number of lines in an ASCII file.

        * ``fname : str`` - File name and directory path (248 characters maximum, including the characters
        needed for the
        directory path). An unspecified directory path defaults to the working directory; in this case, you
        can use all 248 characters for the file name.
        * ``ext : str`` - Filename extension (eight-character maximum).

        .. _s-INQUIRE_notes:

        The :ref:`inquire` command is valid in any processor.
        """
        command = f"/INQUIRE,{strarray},{func}"
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

        .. warning::

           This function contains specificities regarding the argument definitions.
           Please refer to the `command documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PARRES.html>`_
           for further explanations.

        **Argument Descriptions**

        .. _PARRES_argdescript:

        * ``lab : str`` - Read operation:

          * ``NEW`` - Replace current parameter set with these parameters (default).

          * ``CHANGE`` - Extend current parameter set with these parameters, replacing any that already exist.

        * ``fname : str`` - File name and directory path (248 characters maximum, including the characters
        needed for the
        directory path). An unspecified directory path defaults to the working directory; in this case, you
        can use all 248 characters for the file name. The file name defaults to :file:`Jobname`.

        * ``ext : str`` - Filename extension (eight-character maximum). The extension defaults to PARM if
        ``Fname`` is blank.

        .. _PARRES_notes:

        Reads parameters from a coded file. The parameter file may have been written with the :ref:`parsav`
        command. The parameters read may replace or change the current parameter set.

        This command is valid in any processor.
        """
        command = f"PARRES,{lab},{fname},{ext}"
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

        .. warning::

           This function contains specificities regarding the argument definitions.
           Please refer to the `command documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PARSAV.html>`_
           for further explanations.

        **Argument Descriptions**

        .. _PARSAV_argdescript:

        * ``lab : str`` - Write operation:

          * ``SCALAR`` - Write only scalar parameters (default).

          * ``ALL`` - Write scalar and array parameters. Parameters may be numeric or alphanumeric.

        * ``fname : str`` - File name and directory path (248 characters maximum, including the characters
        needed for the
        directory path). An unspecified directory path defaults to the working directory; in this case, you
        can use all 248 characters for the file name. The file name defaults to :file:`Jobname`.

        * ``ext : str`` - Filename extension (eight-character maximum). The extension defaults to PARM if
        ``Fname`` is blank.

        .. _PARSAV_notes:

        Writes the current parameters to a coded file. Previous parameters on this file, if any, will be
        overwritten. The parameter file may be read with the :ref:`parres` command.

        :ref:`parsav` / :ref:`parres` operations truncate some long decimal strings, and can cause differing
        values in your solution data when other operations are performed. A good practice is to limit the
        number of decimal places you will use before and after these operations.

        This command is valid in any processor.
        """
        command = f"PARSAV,{lab},{fname},{ext}"
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

        .. warning::

           This function contains specificities regarding the argument definitions.
           Please refer to the `command documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SET_st.html>`_
           for further explanations.

        **Argument Descriptions**

        .. _a-SET_argdescript:

        * ``par : str`` - An alphanumeric name used to identify this parameter. ``Par`` can contain up to 32
          characters, beginning with a letter and containing only letters, numbers, and underscores. Examples:

          .. code:: apdl

             ABC A3X TOP_END

          Command names, function names, label names, component and assembly names, etc., are invalid, as are
          parameter names beginning with an underscore (for example,

          .. code:: apdl

             _LOOP

          ).

          Parameter names ending in an underscore are not listed by the :ref:`starstatus` command. Array
          parameter names must be followed by a subscript, and the entire expression must be 32 characters or
          less. Examples:

          .. code:: apdl

             A(1,1) NEW_VAL(3,2,5) RESULT(1000)

          There is no character parameter substitution for the ``Par`` field. Table parameters used in command
          fields (where constant values are normally given) are limited to 32 characters.

        * ``value : str`` - Numerical value or alphanumeric character string (up to 32 characters enclosed
          in single quotes) to be assigned to this parameter. Examples:

          .. code:: apdl

             A(1,3)=7.4 B='ABC3'

          Can also be a parameter or a parametric expression. Examples:

          .. code:: apdl

             C=A(1,3) A(2,2)=(C+4)/2

          .. code:: apdl

             C=A(1,3) A(2,2)=(C+4)/2

           If ``VALUE`` is the table array name, the subscripts are the values of the primary variables and
          the table is evaluated at these specified index values.

          If blank, delete this parameter. Example:

          .. code:: apdl

             A=

          deletes parameter

          .. code:: apdl

             A

          .. code:: apdl

             A

        * ``val2, val3, val4, val5, val6, val7, val8, val9, val10 : str`` - If ``Par`` is an array
          parameter, values ``VAL2`` through ``VAL10`` (up to the last nonblank value) are sequentially
          assigned to the succeeding array elements of the column. Examples:

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

        .. _a-SET_notes:

        Assigns values to user-named parameters that can be substituted later in the run. The equivalent
        (and recommended) format is ``Par`` = ``VALUE``, ``VAL2``, ``VAL3``,..., ``VAL10``

        which can be used in place of :ref:`starset`, ``Par``,... for convenience.

        This command is valid in any processor.

        .. _a-SET_extranote1:

        Parameters (numeric or character) can be scalars (single valued) or arrays (multiple valued in one,
        two, or three dimensions). An unlimited number of parameter names can be defined in any run. For
        very large numbers of parameters, it is most efficient to define them in alphabetical order.

        Parameter values can be redefined at any time. Array parameters can also be assigned values within a
        do-loop ( ``*DO`` ) for convenience. Internally programmed do-loop commands are also available with
        the **\*V** ``XX``  commands ( :ref:`vfill` ). Parameter values (except for parameters ending in an
        underscore) can be listed with the :ref:`starstatus` command, displayed via :ref:`starvplot`
        (numeric parameters only), and modified via ``*VEDIT`` (numeric parameters only).

        Older program-provided macro files can use parameter names that do not begin with an underscore.
        Using these macros embedded in your own macros may cause conflicts if the same parameter names are
        used.

        Parameters can also be resolved in comments created via :ref:`com`. A parameter can be deleted by
        redefining it with a blank ``VALUE``. If the parameter is an array, the entire array is deleted.
        Parameters can also be defined by a response to a query via ``*ASK`` or from a Mechanical APDL-
        provided
        value via :ref:`get`.

        .. _a-SET_extranote2:

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

        .. _a-SET_extranote3:

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

        .. _a-SET_extranote4:

        Most alphanumeric arguments permit the use of character parameter substitution. When the parameter
        name ``Par`` input, the alphanumeric value of the parameter is substituted into the command at that
        point. Substitution can be suppressed by enclosing the parameter name within single quotes ( ' ).
        Forced substitution is available in some fields by enclosing the parameter name within percent (%)
        signs. Valid forced substitution fields include command name fields, ``Fname`` (filename) or ``Ext``
        (extension) arguments, :ref:`abbr` command ( ``Abbr`` arguments), :ref:`title` and :ref:`stitle`
        commands ( ``Title`` argument) and :ref:`tlabel` command ( ``Text`` argument). Character parameter
        substitution is also available in the ``*ASK``, :ref:`an3d`, :ref:`cfwrite`, ``*IF``, ``*ELSEIF``,
        :ref:`msg`, :ref:`starset`, :ref:`use`, :ref:`vread`, and :ref:`vwrite` commands. Character array
        parameters must include a subscript (within parentheses) to identify the array element whose value
        is to be substituted.

        .. _a-SET_extranote5:

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

        * operations in parentheses (innermost first)

        * then exponentiation (right to left)

        * then multiplication or division (left to right)

        * then unary association (such as +A or -A)

        * then addition or subtraction (left to right)

        * then logical evaluations (left to right).

        Expressions (E) can be a constant, a parameter, a function, or another operation expression (of the
        form E1oE2oE3...oE10). Functions are of the form FTN(A) where the argument (A) can itself be of the
        form E1oE2oE3...oE10. Operations are recursive to a level of four deep (three levels of internally
        nested parentheses). Iterative floating point parameter arithmetic should not be used for high
        precision input because of the accumulated numerical round off-error. Up to 10 expressions are
        accepted within a set of parenthesis.

        Valid functions (which are based on standard FORTRAN functions where possible) are:

        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.

        Function arguments ( X, Y, etc.) must be enclosed within parentheses and can be numeric values,
        parameters, or expressions. Input arguments for angular functions must evaluate to radians by
        default. Output from angular functions are also in radians by default. See :ref:`afun` to use
        degrees instead of radians for the angular functions. See :ref:`vfun` for applying these parameter
        functions to a sequence of array elements. Additional functions, called get functions, are described
        via :ref:`get`.
        """
        command = f"*SET,{par},{value},{val2},{val3},{val4},{val5},{val6},{val7},{val8},{val9},{val10}"
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
            etc. to specify ranges. Use :ref:`dim` to define array parameters. Use ``*VEDIT`` to review array
            parameters interactively. Use :ref:`vwrite` to print array values in a formatted output. If ``Par``
            is blank, list all scalar parameter values, array parameter dimensions, and abbreviations. If ARGX,
            list the active set of local macro parameters (ARG1 to ARG9 and AR10 to AR99) ( :ref:`use` ).

            The following are possible values for ``Par``

            * ``ALL or blank`` - Lists all parameters (except local macro parameters and those with names
              beginning or ending with an underbar) and toolbar abbreviations.

            * ``_PRM`` - Lists only parameters with names beginning with an underbar (_). These are Mechanical APDL
              internal parameters.

            * ``PRM_`` - Lists only parameters with names ending with an underbar (_). A good APDL programming
              convention is to ensure that all parameters created by your system programmer are named with a
              trailing underbar.

            * ``ABBR`` - Lists all toolbar abbreviations.

            * ``PARM`` - Lists all parameters (except local macro parameters and those with names beginning or
              ending with an underbar).

            * ``MATH`` - Lists all APDL Math parameters, including vectors, matrices, and linear solvers.

            * ``PARNAME`` - Lists only the parameter specified. ``PARNAME`` cannot be a local macro parameter
              name.

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

        .. warning::

           This function contains specificities regarding the argument definitions.
           Please refer to the `command documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_STATUS_st.html>`_
           for further explanations.

        **Argument Descriptions**

        .. _a-STATUS_argdescript:

        * ``par : str`` - Specifies the parameter or sets of parameters listed. For array parameters, use
        ``IMIN``, ``IMAX``,
          etc. to specify ranges. Use :ref:`dim` to define array parameters. Use ``*VEDIT`` to review array
          parameters interactively. Use :ref:`vwrite` to print array values in a formatted output. If ``Par``
          is blank, list all scalar parameter values, array parameter dimensions, and abbreviations. If ARGX,
          list the active set of local macro parameters (ARG1 to ARG9 and AR10 to AR99) ( :ref:`use` ).

          The following are possible values for ``Par``

          * ``ALL or blank`` - Lists all parameters (except local macro parameters and those with names
            beginning or ending with an underbar) and toolbar abbreviations.

          * ``_PRM`` - Lists only parameters with names beginning with an underbar (_). These are Mechanical APDL
            internal parameters.

          * ``PRM_`` - Lists only parameters with names ending with an underbar (_). A good APDL programming
            convention is to ensure that all parameters created by your system programmer are named with a
            trailing underbar.

          * ``ABBR`` - Lists all toolbar abbreviations.

          * ``PARM`` - Lists all parameters (except local macro parameters and those with names beginning or
            ending with an underbar).

          * ``MATH`` - Lists all APDL Math parameters, including vectors, matrices, and linear solvers.

          * ``PARNAME`` - Lists only the parameter specified. ``PARNAME`` cannot be a local macro parameter
            name.

          * ``ARGX`` - Lists all local macro parameter values (ARG1- AR99) that are non-zero or non-blank.

        * ``imin, imax, jmin, jmax, kmin, kmax, lmin, lmax, mmin, mmax : str`` - Range of array elements to
          display (in terms of the dimensions (row, column, plane, book, and shelf). Minimum values default to
          1. Maximum values default to the maximum dimension values. Zero may be input for ``IMIN``, ``JMIN``,
          and ``KMIN`` to display the index numbers. See :ref:`taxis` command to list index numbers of 4- and
          5-D tables.

        * ``kpri : int`` - Use this field to list your primary variable labels (X, Y, Z, TIME, etc.).

          * ``1`` - List the labels (default). YES, Y, or ON are also valid entries.

          * ``0`` - Do not list the labels. NO, N, or OFF are also valid entries.

        .. _a-STATUS_notes:

        You cannot obtain the value for a single local parameter (for example, :ref:`starstatus`,ARG2). You
        can only request all local parameters simultaneously using :ref:`starstatus`,ARGX.

        This command is valid in any processor.
        """
        command = f"*STATUS,{par},{imin},{imax},{jmin},{jmax},{kmin},{kmax},{lmin},{lmax},{mmin},{mmax},{kpri}"
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

        .. warning::

           This function contains specificities regarding the argument definitions.
           Please refer to the `command documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_VGET_st.html>`_
           for further explanations.

        **Argument Descriptions**

        .. _a-VGET_argdescript:

        * ``parr : str`` - The name of the resulting vector array parameter. See :ref:`starset` for name
          restrictions. The program creates the array parameter if it does not exist.

        * ``entity : str`` - Entity keyword. Valid keywords are NODE, ELEM, KP, LINE, AREA, VOLU, etc. as
          shown for ``Entity`` = in the tables below.

        * ``entnum : str`` - The number of the entity (as shown for ``ENTNUM`` = in the tables below).

        * ``item1 : str`` - The name of a particular item for the given entity. Valid items are as shown in
          the ``Item1`` columns of the tables below.

        * ``it1num : str`` - The number (or label) for the specified ``Item1`` (if any). Valid ``IT1NUM``
          values are as shown in the ``IT1NUM`` columns of the tables below. Some ``Item1`` labels do not
          require an ``IT1NUM`` value.

        * ``item2, it2num : str`` - A second set of item labels and numbers to further qualify the item for
          which data is to be retrieved. Most items do not require this level of information.

        * ``kloop : str`` - Field to be looped on:

          * ``0 or 2`` - Loop on the ``ENTNUM`` field (default).

          * ``3`` - Loop on the ``Item1`` field.

          * ``4`` - Loop on the ``IT1NUM`` field. Successive items are as shown with ``IT1NUM``.

          * ``5`` - Loop on the ``Item2`` field.

          * ``6`` - Loop on the ``IT2NUM`` field. Successive items are as shown with ``IT2NUM``.

        .. _a-VGET_notes:

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

        * `\*VGET PREP7 Items
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cmd/Hlp_C_VGET_st.html#vget.prep7.tlab>`_
          \*VGET PREP7 Items

        * `\*VGET POST1 Items
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cmd/Hlp_C_VGET_st.html#vget.post1.node.ndof>`_
          \*VGET POST1 Items

        This command is valid in any processor.

        **\*VGET PREP7 Items**

        .. _vget_prep7:

        * :ref:`vget_prep7_node`

        * :ref:`vget_prep7_elem`

        * :ref:`vget_prep7_kp`

        * :ref:`vget_prep7_line`

        * :ref:`vget_prep7_area`

        * :ref:`vget_prep7_volu`

        * :ref:`vget_prep7_cdsy`

        * :ref:`vget_prep7_rcon`

        * :ref:`vget_prep7_tlab`

        .. _vget_prep7_node:

        \*VGET PREP7 Items, Entity = NODE
        *********************************

        .. flat-table:: ``Entity`` = NODE, ``ENTNUM`` = ``n`` (node number)
           :header-rows: 2

           * - :ref:`starvget`, ``ParR``, NODE, ``n``, ``Item1``, ``IT1NUM``,, ``KLOOP``
           * - Item1
             - IT1NUM
             - Description
           * - LOC
             - X, Y, Z
             - X, Y, or Z location in the active coordinate system
           * - ANG
             - XY, YZ, ZX
             - THXY, THYZ, THZX rotation angle
           * - NSEL
             -
             - Select status of node ``n`` : -1 = unselected, 0 = undefined, 1 = selected
           * - NLIST
             -
             - Returns the list of selected nodes ( ``ENTNUM`` is ignored)


        .. _vget_prep7_elem:

        \*VGET PREP7 Items, Entity = ELEM
        *********************************

        .. flat-table:: ``Entity`` = ELEM, ``ENTNUM`` = ``n`` (element number)
           :header-rows: 2

           * - :ref:`starvget`, ``ParR``, ELEM, ``n``, ``Item1``, ``IT1NUM``,, ``KLOOP``
           * - Item1
             - IT1NUM
             - Description
           * - NODE
             - 1, 2,... 20
             - Node number at position 1, 2,... 20 of element ``n``
           * - CENT
             - X, Y, Z
             - Centroid X, Y, or Z location (based on shape function) in the active coordinate system
           * - ADJ
             - 1, 2,... 6
             - Number of elements adjacent to face 1, 2,... 6
           * - ATTR
             - ``name``
             - Number assigned to specified attribute; ``name`` = MAT, TYPE, REAL, ESYS, ENAM, or SECN
           * - GEOM
             -
             - Characteristic element geometry. Length of line element (straight line between ends), area of area element, or volume of volume element. Issuing :ref:`starvget` for an element returns a signed value. To always get a positive value, issue :ref:`vabs`,1 prior to issuing the :ref:`starvget` command.
           * - ESEL
             -
             - Select status of element ``n`` : -1 = unselected, 0 = undefined, 1 = selected
           * - SHPAR
             - ``Test``
             - Element shape test result for selected element ``n``, where ``Test`` = ASPE (aspect ratio), JACR (Jacobian ratio), MAXA (maximum corner angle), PARA (deviation from parallelism of opposite edges), or WARP (warping factor)
           * - ELIST
             -
             - Returns the list of selected elements ( ``ENTNUM`` is ignored)


        .. _vget_prep7_kp:

        \*VGET PREP7 Items, Entity = KP
        *******************************

        .. flat-table:: ``Entity`` = KP, ``ENTNUM`` = ``n`` (keypoint number)
           :header-rows: 2

           * - :ref:`starvget`, ``ParR``, KP, ``n``, ``Item1``, ``IT1NUM``,, ``KLOOP``
           * - Item1
             - IT1NUM
             - Description
           * - LOC
             - X, Y, Z
             - X, Y, or Z location in the active coordinate system
           * - ATTR
             - ``name``
             - Number assigned to specified attribute; ``name`` = MAT, TYPE, REAL, ESYS, NODE, or ELEM
           * - DIV
             -
             - Divisions (element size setting) from :ref:`kesize`
           * - KSEL
             -
             - Select status of keypoint ``n`` : -1 = unselected, 0 = undefined, 1 = selected
           * - KLIST
             -
             - Returns the list of selected keypoints ( ``ENTNUM`` is ignored)


        .. _vget_prep7_line:

        \*VGET PREP7 Items, Entity = LINE
        *********************************

        .. flat-table:: ``Entity`` = LINE, ``ENTNUM`` = ``n`` (line number)
           :header-rows: 2

           * - :ref:`starvget`, ``ParR``, LINE, ``n``, ``Item1``, ``IT1NUM``,, ``KLOOP``
           * - Item1
             - IT1NUM
             - Description
           * - KP
             - 1, 2
             - Keypoint number at position 1 or 2
           * - ATTR
             - ``name``
             - Number assigned to specified attribute; ``name`` = MAT, TYPE, REAL, ESYS, NNOD, NELM, or NDIV (NNOD = number of nodes, NELM = number of elements, NDIV = number of divisions)
           * - LENG
             -
             - Length
           * - LSEL
             -
             - Select status of line ``n`` : -1 = unselected, 0 = undefined, 1 = selected
           * - LLIST
             -
             - Returns the list of selected lines ( ``ENTNUM`` is ignored)


        .. _vget_prep7_area:

        \*VGET PREP7 Items, Entity = AREA
        *********************************

        .. flat-table:: ``Entity`` = AREA, ``ENTNUM`` = ``n`` (area number)
           :header-rows: 2

           * - :ref:`starvget`, ``ParR``, AREA, ``n``, ``Item1``, ``IT1NUM``, ``Item2``, ``IT2NUM``, ``KLOOP``
           * - Item1
             - IT1NUM
             - Item2
             - IT2NUM
             - Description
           * - LOOP
             - 1,2,...
             - LINE
             - 1, 2,... ``p``
             - IT1NUM is the loop number, and must be input if LINE is to be retrieved. IT2NUM is line number at position 1, 2,... ``p``
           * - ATTR
             - ``name``
             - :rspan:`3`
             - :rspan:`3`
             - Number assigned to specified attribute; ``name`` = MAT, TYPE, REAL, ESYS, SECN, NNOD, or NELM (NNOD = number of nodes, NELM = number of elements)
           * - AREA
             - -
             - Area (after last :ref:`asum` )
           * - ASEL
             - -
             - Select status of area ``n`` : -1 = unselected, 0 = undefined, 1 = selected
           * - ALIST
             - -
             - Returns the list of selected areas ( ``ENTNUM`` is ignored)


        .. _vget_prep7_volu:

        \*VGET PREP7 Items, Entity = VOLU
        *********************************

        .. flat-table:: ``Entity`` = VOLU, ``ENTNUM`` = ``n`` (volume number)
           :header-rows: 2

           * - :ref:`starvget`, ``ParR``, VOLU, ``n``, ``Item1``, ``IT1NUM``, ``Item2``, ``IT2NUM``, ``KLOOP``
           * - Item1
             - IT1NUM
             - Item2
             - IT2NUM
             - Description
           * - SHELL
             - 1, 2,...
             - AREA
             - 1, 2,... ``p``
             - IT1NUM is the shell number, and must be input if AREA is to be retrieved. IT2NUM is area number at position 1, 2... ``p``
           * - ATTR
             - ``name``
             - :rspan:`3`
             - :rspan:`3`
             - Number assigned to specified attribute; ``name`` = MAT, TYPE, REAL, ESYS, NNOD, or NELM (NNOD = number of nodes, NELM = number of elements)
           * - VOLU
             - -
             - Volume (after last :ref:`vsum` )
           * - VSEL
             - -
             - Select status of volume ``n`` : -1 = unselected, 0 = undefined, 1 = selected
           * - VLIST
             - -
             - Returns the list of selected volumes ( ``ENTNUM`` is ignored)


        .. _vget_prep7_cdsy:

        \*VGET PREP7 Items, Entity = CDSY
        *********************************

        .. flat-table:: ``Entity`` = CDSY, ``ENTNUM`` = ``n`` (coordinate system number)
           :header-rows: 2

           * - :ref:`starvget`, ``ParR``, CDSY, ``n``, ``Item1``, ``IT1NUM``,, ``KLOOP``
           * - Item1
             - IT1NUM
             - Description
           * - LOC
             - X, Y, Z
             - X, Y, or Z origin location (global Cartesian coordinate)
           * - ANG
             - XY, YZ, ZX
             - THXY, THYZ, or THZX rotation angle (°) relative to the global Cartesian coordinate system
           * - ATTR
             - ``name``
             - Number assigned to specified attribute; ``name`` = KCS, KTHET, KPHI, PAR1, or PAR2. If the coordinate system is undefined, KCS returns as -1.0


        .. _vget_prep7_rcon:

        \*VGET PREP7 Items, Entity = RCON
        *********************************

        .. flat-table:: ``Entity`` = RCON, ``ENTNUM`` = ``n`` (real constant set number)
           :header-rows: 2

           * - :ref:`starvget`, ``ParR``, RCON, ``n``, ``Item1``, ``IT1NUM``,, ``KLOOP``
           * - Item1
             - IT1NUM
             - Description
           * - CONST
             - 1, 2,... ``m``
             - Real constant value for constant 1, 2,... ``m``


        .. _vget_prep7_tlab:

        \*VGET PREP7 Items, Entity = TLAB
        *********************************

        .. flat-table:: ``Entity`` = ``TLAB``, ``ENTNUM`` = ``n`` ( ``TLAB`` is the ``Lab`` data table label on the :ref:`tb` command. ``n`` is the material number.)
           :header-rows: 2

           * - :ref:`starvget`, ``ParR``, ``TLAB``, ``n``, ``Item1``, ``IT1NUM``,, ``KLOOP``
           * - Item1
             - IT1NUM
             - Item2
             - IT2NUM
             - Description
           * - TEMP
             - ``val``
             - CONST
             - ``num``
             - IT1NUM ``value`` is the temperature value at which to retrieve table data. ``num`` is the constant number whose value is to be retrieved. For constants input as X, Y points, the constant numbers are consecutive with the X constants being the odd numbers, beginning with one.

        **\*VGET POST1 Items**

        .. _vget_post1:

        * :ref:`vget_post1_cyccalc`

        * :ref:`vget_post1_elem`

        * :ref:`vget_post1_member`

        * :ref:`vget_post1_node_enode`

        * :ref:`vget_post1_node_ndof`

        Vector items are in the active results coordinate system unless otherwise specified.

        .. _vget_post1_cyccalc:

        \*VGET POST1 Items, Entity = CYCCALC
        ************************************

        .. flat-table:: ``Entity`` = CYCCALC, ``ENTNUM`` = ``n`` ( :ref:`cycspec` specification number)
           :header-rows: 2

           * - :ref:`starvget`, ``ParR``, CYCCALC, ``n``, ``Item1``, ``IT1NUM``, ``Item2``, ``IT2NUM``, ``KLOOP``
           * - Item1
             - IT1NUM
             - Item2
             - IT2NUm
             - Description
           * - :rspan:`1` FREQ
             - :rspan:`1` ``Frequency point``
             - SECTOR
             - ``sector``
             - :ref:`cycspec` results at the IT1NUM frequency or sector (depending on ``KLOOP`` )
           * - SECMAX
             -
             - :ref:`cycspec` maximum results
           * - The frequency point refers to the harmonic solution data set number ( ``NSET`` on the :ref:`set` command).   For ``KLOOP`` = 4 or SECMAX, returns the requested sector results for all frequencies and ``IT1NUM`` is ignored.   For ``KLOOP`` = 6, returns the requested frequency results for all sectors and ``IT2NUM`` is ignored.   All other ``KLOOP`` options are invalid.


        .. _vget_post1_elem:

        \*VGET POST1 Items, Entity = ELEM
        *********************************

        .. flat-table:: ``Entity`` = ELEM, ``ENTNUM`` = ``n`` (element number)
           :header-rows: 2

           * - :ref:`starvget`, ``ParR``, ELEM, ``n``, ``Item1``, ``IT1NUM``,, ``KLOOP``
           * - Item1
             - IT1NUM
             - Description
           * - ETAB
             - ``Label``
             - Any user-defined element table label (see :ref:`etable` command)


        .. _vget_post1_member:

        \*VGET POST1 Items, Entity = MEMBER
        ***********************************

        .. flat-table:: ``Entity`` = MEMBER, ``ENTNUM`` = ``N`` (GroupID)
           :header-rows: 2

           * - :ref:`starvget`, ``Par`` ,MEMBER, ``N``, ``Item1``, ``IT1NUM``,, ``KLOOP``
           * - Item1
             - IT1NUM
             - Description
           * - TEMP
             - MIN, MAX
             - Minimum or maximum temperature of members (individual reinforcings) with GroupID = ``N`` in the selected set of reinforcing elements


        .. _vget_post1_node_enode:

        \*VGET POST1 Items, Entity = NODE, Element Nodal Results
        ********************************************************

        .. flat-table:: ``Entity`` = NODE, ``ENTNUM`` = ``n`` (node number)
           :header-rows: 2

           * - :ref:`starvget`, ``ParR``, NODE, ``n``, ``Item1``, ``IT1NUM``,, ``KLOOP``
           * - Item1
             - IT1NUM
             - Description
             - Item2
           * - :rspan:`2` S
             - X, Y, Z, XY, YZ, XZ
             - Component stress
             - :rspan:`2` ``Item2`` controls whether `nodal-averaged results <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_CH2_2.html#nodeavepost>`_ are used. Valid labels are: AUTO - Use nodal-averaged results, if available. Otherwise use element-based results.   ESOL- Use element-based results only.   NAR - Use nodal-averaged results only.
           * - 1, 2, 3
             - Principal stress
           * - INT, EQV
             - Stress intensity or equivalent stress
           * - :rspan:`2` EPTO
             - X, Y, Z, XY, YZ, XZ
             - Component total strain (EPEL + EPPL + EPCR)
             -
           * - 1, 2, 3
             - Principal total strain
             -
           * - INT, EQV
             - Total strain intensity or total equivalent strain
             -
           * - :rspan:`2` EPEL
             - X, Y, Z, XY, YZ, XZ
             - Component elastic strain
             - :rspan:`2` ``Item2`` controls whether `nodal-averaged results`_ are used. Valid labels are: AUTO - Use nodal-averaged results, if available. Otherwise use element-based results.   ESOL- Use element-based results only.   NAR - Use nodal-averaged results only.
           * - 1, 2, 3
             - Principal elastic strain
           * - INT, EQV
             - Elastic strain intensity or elastic equivalent strain
           * - :rspan:`2` EPPL
             - X, Y, Z, XY, YZ, XZ
             - Component plastic strain
             - :rspan:`2` ``Item2`` controls whether `nodal-averaged results`_ are used. Valid labels are: AUTO - Use nodal-averaged results, if available. Otherwise use element-based results.   ESOL- Use element-based results only.   NAR - Use nodal-averaged results only.
           * - 1, 2, 3
             - Principal plastic strain
           * - INT, EQV
             - Plastic strain intensity or plastic equivalent strain
           * - :rspan:`2` EPCR
             - X, Y, Z, XY, YZ, XZ
             - Component creep strain
             - :rspan:`2` ``Item2`` controls whether `nodal-averaged results`_ are used. Valid labels are: AUTO - Use nodal-averaged results, if available. Otherwise use element-based results.   ESOL- Use element-based results only.   NAR - Use nodal-averaged results only.
           * - 1, 2, 3
             - Principal creep strain
           * - INT, EQV
             - Creep strain intensity or creep equivalent strain
           * - :rspan:`2` EPTH
             - X, Y, Z, XY, YZ, XZ
             - Component thermal strain
             - :rspan:`2` ``Item2`` controls whether `nodal-averaged results`_ are used. Valid labels are: AUTO - Use nodal-averaged results, if available. Otherwise use element-based results.   ESOL- Use element-based results only.   NAR - Use nodal-averaged results only.
           * - 1, 2, 3
             - Principal thermal strain
           * - INT, EQV
             - Thermal strain intensity or thermal equivalent strain
           * - EPSW
             -
             - Swelling strain
             - ``Item2`` controls whether `nodal-averaged results`_ are used. Valid labels are: AUTO - Use nodal-averaged results, if available. Otherwise use element-based results.   ESOL- Use element-based results only.   NAR - Use nodal-averaged results only.
           * - :rspan:`2` EPDI
             - X, Y, Z, XY, YZ, XZ
             - Component diffusion strain
             -
           * - 1, 2, 3
             - Principal diffusion strain
             -
           * - INT, EQV
             - Diffusion strain intensity or diffusion equivalent strain
             -
           * - :rspan:`5` NL
             - SEPL
             - Equivalent stress (from stress-strain curve)
             -
           * - SRAT
             - Stress state ratio
             -
           * - HPRES
             - Hydrostatic pressure
             -
           * - EPEQ
             - Accumulated equivalent plastic strain
             -
           * - PSV
             - Plastic state variable
             -
           * - PLWK
             - Plastic work/volume
             -
           * - HS
             - X, Y, Z
             - Component magnetic field intensity from current sources (in the global Cartesian coordinate system)
             -
           * - BFE
             - TEMP
             - Body temperatures (calculated from applied temperatures) as used in solution
             -
           * - TG
             - X, Y, Z, SUM
             - Component thermal gradient and sum
             -
           * - TF
             - X, Y, Z, SUM
             - Component thermal flux and sum
             -
           * - PG
             - X, Y, Z, SUM
             - Component pressure gradient and sum
             -
           * - EF
             - X, Y, Z, SUM
             - Component electric field and sum
             -
           * - D
             - X, Y, Z, SUM
             - Component electric flux density and sum
             -
           * - H
             - X, Y, Z, SUM
             - Component magnetic field intensity and sum
             -
           * - B
             - X, Y, Z, SUM
             - Component magnetic flux density and sum
             -
           * - FMAG
             - X, Y, Z, SUM
             - Component electromagnetic force and sum
             -
           * - :rspan:`9` CONT
             - STAT
             - Contact status
             -
           * - PENE
             - Contact penetration
             -
           * - PRES
             - Contact pressure
             -
           * - SFRIC
             - Contact friction stress
             -
           * - STOT
             - Contact total stress (pressure plus friction)
             -
           * - SLIDE
             - Contact sliding distance
             -
           * - GAP
             - Contact gap distance
             -
           * - FLUX
             - Total heat flux at contact surface
             -
           * - CNOS
             - Total number of contact status changes during substep
             -
           * - FPRS
             - Actual applied fluid penetration pressure
             -
           * - Element nodal results are the average nodal value of the selected elements


        .. _vget_post1_node_ndof:

        \*VGET POST1 Items, Entity = NODE, Nodal Degree of Freedom Results
        ******************************************************************

        .. flat-table:: ``Entity`` = NODE, ``ENTNUM`` = ``n`` (node number)
           :header-rows: 2

           * - :ref:`starvget`, ``ParR``, NODE, ``n``, ``Item1``, ``IT1NUM``,, ``KLOOP``
           * - Item1
             - IT1NUM
             - Description
           * - U
             - X, Y, Z
             - X, Y, or Z structural displacement
           * - ROT
             - X, Y, Z
             - X, Y, or Z structural rotation
           * - TEMP
             -
             - Temperature. For ``SHELL131`` and ``SHELL132`` elements with KEYOPT(3) = 0 or 1, use TBOT, TE2, TE3,..., TTOP instead of TEMP. Alternative get functions: TEMP(N), TBOT(N), TE2(N), etc.
           * - PRES
             -
             - Pressure
           * - VOLT
             -
             - Electric potential
           * - MAG
             -
             - Magnetic scalar potential
           * - V
             - X, Y, Z
             - X, Y, or Z fluid velocity; X, Y, or Z nodal velocity in a transient structural analysis (analysis with :ref:`antype`,TRANS)
           * - A
             - X, Y, Z
             - X, Y, or Z magnetic vector potential; X, Y or Z nodal acceleration in a transient structural analysis (analysis with :ref:`antype`,TRANS)
           * - CURR
             -
             - Current
           * - EMF
             -
             - Electromotive force drop

        """
        command = (
            f"*VGET,{parr},{entity},{entnum},{item1},{it1num},{item2},{it2num},{kloop}"
        )
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

        .. warning::

           This function contains specificities regarding the argument definitions.
           Please refer to the `command documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_TAXIS.html>`_
           for further explanations.

        **Argument Descriptions**

        .. _a-TAXIS_argdescript:

        * ``parmloc : str`` - Name and starting location in the table array parameter for indexing. Indexing
          occurs along the axis defined with ``nAxis``.

        * ``naxis : str`` - Axis along which indexing occurs. Valid labels are:

          * ``1`` - Corresponds to Row. Default.

          * ``2`` - Corresponds to Column.

          * ``3`` - Corresponds to Plane.

          * ``4`` - Corresponds to Book.

          * ``5`` - Corresponds to Shelf.

          * ``ALL`` - Lists all index numbers. Valid only if ``Val1`` = LIST.

        * ``val1, val2, val3,..., val10 : str`` - Values of the index numbers for the axis ``nAxis``,
          starting from the table array parameter location ``ParmLoc``. You can define up to ten values.

          To list the index values specified with ``nAxis``, issue ``Val1`` = LIST. If ``Val1`` = LIST,
          ``Val2`` - ``Val10`` are ignored.

        .. _a-TAXIS_notes:

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

        .. warning::

           This function contains specificities regarding the argument definitions.
           Please refer to the `command documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_TREAD.html>`_
           for further explanations.

        **Argument Descriptions**

        .. _a-TREAD_argdescript:

        * ``par : str`` - Table array parameter name as defined by the :ref:`dim` command.

        * ``fname : str`` - File name and directory path (248 characters maximum, including the characters
        needed for the
        directory path). An unspecified directory path defaults to the working directory; in this case, you
        can use all 248 characters for the file name. File name has no default.

        * ``ext : str`` - Filename extension (eight-character maximum). Extension has no default.

        * ``nskip : str`` - Number of comment lines at the beginning of the file being read that will be
          skipped during the reading. Default = 0.

        .. _a-TREAD_notes:

        Use this command to read in a table of data from an external file into a table array parameter. The
        external file may be created using a text editor or by an external application or program. To be
        used by :ref:`tread`, the external file's encoding format must be UTF-8, and the file must be in
        tab-delimited, blank-delimited, or comma-delimited format. The TABLE type array parameter must be
        defined before you can read in an external file. See :ref:`dim` for more information.

        This command is not applicable to 4- or 5-D tables.
        """
        command = f"*TREAD,{par},{fname},{ext},,{nskip}"
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

            * ``DATA`` - Assign specified values ``CON1``, ``CON2``, etc. to successive array elements. Up to 10
              assignments may be made at a time. Any CON values after a blank CON value are ignored.

            * ``RAMP`` - Assign ramp function values: ``CON1`` +((n-1)\* ``CON2`` ), where n is the loop number ( :ref:`vlen` ). To specify a constant function (no ramp), set ``CON2`` to zero.

            * ``RAND`` - Assign random number values based on a uniform distribution RAND( ``CON1``, ``CON2`` ), where:

              * ``CON1`` is the lower bound (defaults to 0.0)
              * ``CON2`` is the upper bound (defaults to 1.0)

            * ``GDIS`` - Assign random sample of Gaussian distributions GDIS( ``CON1``, ``CON2`` ) where:

              * ``CON1`` is the mean (defaults to 0.0)
              * ``CON2`` is the standard deviation (defaults to 1.0)

            * ``TRIA`` - Assigns random number values based on a triangular distribution TRIA( ``CON1``, ``CON2``, ``CON3`` ) where:

              * ``CON1`` is the lower bound (defaults to 0.0)
              * ``CON2`` is the location of the peak value ( ``CON1`` ≤ ``CON2`` ≤ ``CON3`` ; ``CON2`` defaults to
                0 if ``CON1`` ≤ 0 ≤ ``CON3``, ``CON1`` if 0 ≤ ``CON1``, or ``CON3`` if ``CON3`` ≤ 0)
              * ``CON3`` is the upper bound (defaults to 1.0 + ``CON1`` if ``CON1`` ≥ 0 or 0.0 if ``CON1`` ≤ 0)

            * ``BETA`` - Assigns random number values based on a beta distribution BETA( ``CON1``, ``CON2``, ``CON3``, ``CON4`` ) where:

              * ``CON1`` is the lower bound (defaults to 0.0)
              * ``CON2`` is the upper bound (defaults to 1.0 + ``CON1`` if ``CON1`` ≥ 0 or 0.0 if ``CON1`` ≤ 0)
              * ``CON3`` and ``CON4`` are the alpha and beta parameters, respectively, of the beta function. Alpha
                and beta must both be positive; they default to 1.0.

            * ``GAMM`` - Assigns random number values based on a gamma distribution: GAMM( ``CON1``, ``CON2``, ``CON3`` ) where:

              * ``CON1`` is the lower bound (defaults to 0.0)
              * ``CON2`` and ``CON3`` are the alpha and beta parameters, respectively, of the gamma function.
                Alpha and beta must both be positive; they default to 1.0.

            * ``RIGID`` - Generates the rigid body modes with respect to the reference point coordinates (
              ``CON1``, ``CON2``, ``CON3`` ). The dimensions of the array parameter ``ParR`` are
              (dim:sub:`1`,dim:sub:`2` ) where dim:sub:`1` is the maximum node number (including internal nodes
              but excluding orientation nodes ) multiplied by the number of degrees of freedom, and dim:sub:`2` is
              the number of rigid body modes (which corresponds to the number of structural degrees of freedom).

            * ``CLUSTER`` - Generates excitation frequencies with clustering option CLUSTER( ``CON1``, ``CON2``, ``CON3``, ``CON4``, ``%CON5%`` ) where:

              * ``CON1`` is the lower end of the frequency range in Hz (0 < ``CON1`` )
              * ``CON2`` is the upper end of the frequency range in Hz ( ``CON1`` < ``CON2`` )
              * ``CON3`` is the number of points on each side of the natural frequency (4 ≤ ``CON3`` ≤ 20,
                defaults to 4)
              * ``CON4`` is the constant damping ratio value or an array parameter (size NFR) specifying the
                damping ratios (if zero or blank, defaults to constant damping ratio of 0.005)
              * ``CON5`` is an array parameter (size NFR) specifying the natural frequencies in Hz
              The dimension of the resulting array parameter ParR is less than 2+NFR\2(2*
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

        .. warning::

           This function contains specificities regarding the argument definitions.
           Please refer to the `command documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_VFILL.html>`_
           for further explanations.

        **Argument Descriptions**

        .. _a-VFILL_argdescript:

        * ``parr : str`` - The name of the resulting numeric array parameter vector. See :ref:`starset` for
          name restrictions.

        * ``func : str`` - Fill function:

          * ``DATA`` - Assign specified values ``CON1``, ``CON2``, etc. to successive array elements. Up to 10
            assignments may be made at a time. Any CON values after a blank CON value are ignored.

          * ``RAMP`` - Assign ramp function values: ``CON1`` +((n-1)\* ``CON2`` ), where n is the loop number ( :ref:`vlen` ). To specify a constant function (no ramp), set ``CON2`` to zero.

          * ``RAND`` - Assign random number values based on a uniform distribution RAND( ``CON1``, ``CON2`` ), where:

            * ``CON1`` is the lower bound (defaults to 0.0)
            * ``CON2`` is the upper bound (defaults to 1.0)

          * ``GDIS`` - Assign random sample of Gaussian distributions GDIS( ``CON1``, ``CON2`` ) where:

            * ``CON1`` is the mean (defaults to 0.0)
            * ``CON2`` is the standard deviation (defaults to 1.0)

          * ``TRIA`` - Assigns random number values based on a triangular distribution TRIA( ``CON1``, ``CON2``, ``CON3`` ) where:

            * ``CON1`` is the lower bound (defaults to 0.0)
            * ``CON2`` is the location of the peak value ( ``CON1`` ≤ ``CON2`` ≤ ``CON3`` ; ``CON2`` defaults to
              0 if ``CON1`` ≤ 0 ≤ ``CON3``, ``CON1`` if 0 ≤ ``CON1``, or ``CON3`` if ``CON3`` ≤ 0)
            * ``CON3`` is the upper bound (defaults to 1.0 + ``CON1`` if ``CON1`` ≥ 0 or 0.0 if ``CON1`` ≤ 0)

          * ``BETA`` - Assigns random number values based on a beta distribution BETA( ``CON1``, ``CON2``, ``CON3``, ``CON4`` ) where:

            * ``CON1`` is the lower bound (defaults to 0.0)
            * ``CON2`` is the upper bound (defaults to 1.0 + ``CON1`` if ``CON1`` ≥ 0 or 0.0 if ``CON1`` ≤ 0)
            * ``CON3`` and ``CON4`` are the alpha and beta parameters, respectively, of the beta function. Alpha
              and beta must both be positive; they default to 1.0.

          * ``GAMM`` - Assigns random number values based on a gamma distribution: GAMM( ``CON1``, ``CON2``, ``CON3`` ) where:

            * ``CON1`` is the lower bound (defaults to 0.0)
            * ``CON2`` and ``CON3`` are the alpha and beta parameters, respectively, of the gamma function.
              Alpha and beta must both be positive; they default to 1.0.

          * ``RIGID`` - Generates the rigid body modes with respect to the reference point coordinates (
            ``CON1``, ``CON2``, ``CON3`` ). The dimensions of the array parameter ``ParR`` are
            (dim:sub:`1`,dim:sub:`2` ) where dim:sub:`1` is the maximum node number (including internal nodes
            but excluding orientation nodes ) multiplied by the number of degrees of freedom, and dim:sub:`2` is
            the number of rigid body modes (which corresponds to the number of structural degrees of freedom).

          * ``CLUSTER`` - Generates excitation frequencies with clustering option CLUSTER( ``CON1``, ``CON2``, ``CON3``, ``CON4``, ``%CON5%`` ) where:

            * ``CON1`` is the lower end of the frequency range in Hz (0 < ``CON1`` )
            * ``CON2`` is the upper end of the frequency range in Hz ( ``CON1`` < ``CON2`` )
            * ``CON3`` is the number of points on each side of the natural frequency (4 ≤ ``CON3`` ≤ 20,
              defaults to 4)
            * ``CON4`` is the constant damping ratio value or an array parameter (size NFR) specifying the
              damping ratios (if zero or blank, defaults to constant damping ratio of 0.005)
            * ``CON5`` is an array parameter (size NFR) specifying the natural frequencies in Hz
            The dimension of the resulting array parameter ParR is less than 2+NFR\2(2*
             ``CON3`` +1) where NFR is the number of natural frequencies defined in ``CON5``.

        * ``con1, con2, con3,..., con10 : str`` - Constants used with above functions.

        .. _a-VFILL_notes:

        Operates on input data and produces one output array parameter vector according to: ``ParR`` = f(
        ``CON1``, ``CON2``,...)

        where the functions (f) are described above. Operations use successive array elements ( :ref:`vlen`,
        :ref:`vmask` ) with the default being all successive elements. For example, :ref:`vfill`
        ,A,RAMP,1,10 assigns A(1) = 1.0, A(2) = 11.0, A(3) = 21.0, etc. :ref:`vfill`,B(5,1),DATA,1.5,3.0
        assigns B(5,1) = 1.5 and B(6,1) = 3.0. Absolute values and scale factors may be applied to the
        result parameter ( :ref:`vabs`, :ref:`vfact` ). Results may be cumulative ( :ref:`vcum` ). See the
        :ref:`voper` command for details.

        This command is valid in any processor.
        """
        command = f"*VFILL,{parr},{func},{con1},{con2},{con3},{con4},{con5},{con6},{con7},{con8},{con9},{con10}"
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

        .. warning::

           This function contains specificities regarding the argument definitions.
           Please refer to the `command documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_VREAD.html>`_
           for further explanations.

        **Argument Descriptions**

        .. _a-VREAD_argdescript:

        * ``parr : str`` - The name of the resulting array parameter vector. See :ref:`starset` for name
          restrictions. The parameter must exist as a dimensioned array ( :ref:`dim` ). String arrays are
          limited to a maximum of 8 characters.

        * ``fname : str`` - File name and directory path (248 characters maximum, including the characters
        needed for the
        directory path). An unspecified directory path defaults to the working directory; in this case, you
        can use all 248 characters for the file name. If the ``Fname`` field is left blank, reading
        continues from the
          current input device, such as the terminal.

        * ``ext : str`` - Filename extension (eight-character maximum).
        * ``label : str`` - Can take a value of IJK, IKJ, JIK, JKI, KIJ, KJI, or blank (IJK).

        * ``n1, n2, n3 : str`` - Read as ((( ``ParR`` (i,j,k), k = 1,n1), i = 1, n2), j = 1, n3) for
          ``Label`` = KIJ. ``n2`` and ``n3`` default to 1.

        * ``nskip : str`` - Number of lines at the beginning of the file being read that will be skipped
          during the reading. Default = 0.

        .. _a-VREAD_notes:

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
