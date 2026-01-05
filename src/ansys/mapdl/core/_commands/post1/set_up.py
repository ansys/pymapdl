# Copyright (C) 2016 - 2026 ANSYS, Inc. and/or its affiliates.
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

from ansys.mapdl.core._commands import CommandsBase


class SetUp(CommandsBase):

    def append(
        self,
        lstep: str = "",
        sbstep: str = "",
        fact: str = "",
        kimg: int | str = "",
        time: str = "",
        angle: str = "",
        nset: str = "",
        **kwargs,
    ):
        r"""Reads data from the results file and appends it to the database.

        Mechanical APDL Command: `APPEND <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_APPEND.html>`_

        Parameters
        ----------
        lstep : str
            Load step number of the data set to be read. Defaults to 1. If FIRST, ignore ``SBSTEP`` and
            ``TIME`` and read the first data set. If LAST, ignore ``SBSTEP`` and ``TIME`` and read the last
            data set. If NEXT, ignore ``SBSTEP`` and ``TIME`` and read the next data set. If already at the
            last data set, the next set is the first data set. If NEAR, ignore ``SBSTEP`` and read the data
            set nearest to ``TIME``. If ``TIME`` is blank, read the first data set. If LIST, scan the
            results file to produce a summary of each load step ( ``FACT``, ``KIMG``, ``TIME`` and ``ANGLE``
            are ignored).

        sbstep : str
            Substep number (within ``LSTEP`` ) (defaults to last substep of load step). For the Buckling (
            :ref:`antype`,BUCKLE) or Modal ( :ref:`antype`,MODAL) analysis, the substep corresponds to the
            mode number (defaults to first mode). If ``LSTEP`` = LIST, ``SBSTEP`` = 0 or 1 will list the
            basic load step information; ``SBSTEP`` = 2 will also list the load step title, and label the
            imaginary data sets if they exist.

        fact : str
            Scale factor applied to data read from the file. If zero (or blank), a value of 1.0 is used.
            Harmonic velocities or accelerations may be calculated from the displacement results from a
            modal or harmonic ( :ref:`antype`,HARMIC) analyses. If ``FACT`` = VELO, the harmonic velocities
            (v) are calculated from the displacements (d) at a particular frequency (f) according to the
            relationship v = 2 πfd. Similarly, if ``FACT`` = ACEL, the harmonic accelerations (a) are
            calculated as a = (2 πf) :sup:`2` d.

        kimg : int or str
            Used only with results from complex analyses:

            * ``0`` - Store real part of complex solution.

            * ``1`` - Store imaginary part.

        time : str
            Time-point identifying the data set to be read. For harmonic analyses, time corresponds to the
            frequency. For the buckling analysis, time corresponds to the load factor. Used only in the
            following cases: If ``LSTEP`` is NEAR, read the data set nearest to ``TIME``. If both ``LSTEP``
            and ``SBSTEP`` are zero (or blank), read data set at time = ``TIME``. If ``TIME`` is between two
            solution time points on the results file, a linear interpolation is done between the two data
            sets. Solution items not written to the results file ( :ref:`outres` ) for either data set will
            result in a null item after data set interpolation. If ``TIME`` is beyond the last time point on
            the file, the last time point is used.

        angle : str
            Circumferential location (0° to 360°). Defines the circumferential location for the harmonic
            calculations used when reading from the results file. The harmonic factor (based on the
            circumferential angle) is applied to the harmonic elements ( ``PLANE25``, ``PLANE75``,
            ``PLANE78``, ``PLANE83``, and ``SHELL61`` ) of the load case. See the `Mechanical APDL Theory
            Reference <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_biblio.html>`_
            for details. Note that factored values of applied constraints and loads will overwrite any
            values existing in the database.

        nset : str
            Data set number of the data set to be read. If a positive value for ``NSET`` is entered,
            ``LSTEP``, ``SBSTEP``, ``KIMG``, and ``TIME`` are ignored. Available set numbers can be
            determined by :ref:`append`,LIST. To determine if data sets are real or imaginary, issue
            :ref:`append`,LIST,2 which labels imaginary data sets.

        Notes
        -----

        .. _APPEND_notes:

        Reads a data set from the results file and appends it to the existing data in the database for the
        selected model only. The existing database is not cleared (or overwritten in total), allowing the
        requested results data to be merged into the database. Various operations may also be performed
        during the read operation. The database must have the model geometry available (or used the
        :ref:`resume` command before the :ref:`append` command to restore the geometry from :file:`File.DB`
        ).
        """
        command = f"APPEND,{lstep},{sbstep},{fact},{kimg},{time},{angle},{nset}"
        return self.run(command, **kwargs)

    def desol(
        self,
        elem: str = "",
        node: str = "",
        item: str = "",
        comp: str = "",
        v1: str = "",
        v2: str = "",
        v3: str = "",
        v4: str = "",
        v5: str = "",
        v6: str = "",
        **kwargs,
    ):
        r"""Defines or modifies solution results at a node of an element.

        Mechanical APDL Command: `DESOL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_DESOL.html>`_

        Parameters
        ----------
        elem : str
            Element number for which results are defined or modified. If ALL, apply to all selected elements
            ( :ref:`esel` ).

        node : str
            Node of element (actual node number, not the position) to which results are specified. If ALL,
            specify results for all selected nodes ( :ref:`nsel` ) of element. If ``NODE`` = P, graphical
            picking is enabled and all remaining command fields are ignored (valid only in the GUI). A
            component name may also be substituted for ``NODE``.

        item : str
            Label identifying results. Valid item labels are shown in :ref:`DESOL_tab_1` below. Some items
            also require a component label ( ``Comp`` ).

        comp : str
            Component of the item (if required); see :ref:`DESOL_tab_1`.

        v1 : str
            Additional values (if any) assigned to the remaining components (in the order corresponding to
            the ``Comp`` list shown below) for the specified ``Item`` (starting from the specified ``Comp``
            label and proceeding to the right).

        v2 : str
            Additional values (if any) assigned to the remaining components (in the order corresponding to
            the ``Comp`` list shown below) for the specified ``Item`` (starting from the specified ``Comp``
            label and proceeding to the right).

        v3 : str
            Additional values (if any) assigned to the remaining components (in the order corresponding to
            the ``Comp`` list shown below) for the specified ``Item`` (starting from the specified ``Comp``
            label and proceeding to the right).

        v4 : str
            Additional values (if any) assigned to the remaining components (in the order corresponding to
            the ``Comp`` list shown below) for the specified ``Item`` (starting from the specified ``Comp``
            label and proceeding to the right).

        v5 : str
            Additional values (if any) assigned to the remaining components (in the order corresponding to
            the ``Comp`` list shown below) for the specified ``Item`` (starting from the specified ``Comp``
            label and proceeding to the right).

        v6 : str
            Additional values (if any) assigned to the remaining components (in the order corresponding to
            the ``Comp`` list shown below) for the specified ``Item`` (starting from the specified ``Comp``
            label and proceeding to the right).

        Notes
        -----

        .. _DESOL_notes:

        The :ref:`desol` command defines or modifies solution results in the database at a node of an area
        or volume element. For example, :ref:`desol`,35,50,S,X,1000,2000,1000 assigns values 1000, 2000, and
        1000 to SX, SY, and SZ (respectively) of node 50 of element 35.

        The settings of the POST1 :ref:`force`, :ref:`shell`, and :ref:`layer` commands, if applicable,
        further specify which database items are affected.

        For layered composite shells, specify the current element layer ( :ref:`layer` ) before issuing the
        :ref:`desol` command.

        All data is stored in the solution coordinate system but is displayed in the results coordinate
        system ( :ref:`rsys` ). To list the current results, use the :ref:`presol` command.

        Modified solution results are not saved automatically. To save separate records of modified results,
        use either the :ref:`rappnd` or :ref:`lcwrite` command.

        Result items are available depending on element type; check the individual element for availability.
        Valid item and component labels for element results are:

        .. _DESOL_tab_1:

        DESOL - Valid Item and Component Labels
        ***************************************

        .. flat-table::
           :header-rows: 1

           * - Item
             - Comp
             - Description
           * - ELEM
             -
             - Element number.
           * - S
             - X, Y, Z, XY, YZ, XZ
             - Component stress.
           * - EPEL
             - X, Y, Z, XY, YZ, XZ
             - Component elastic strain.
           * - EPTH
             - X, Y, Z, XY, YZ, XZ
             - Component thermal strain.
           * - EPPL
             - X, Y, Z, XY, YZ, XZ
             - Component plastic strain.
           * - EPCR
             - X, Y, Z, XY, YZ, XZ
             - Component creep strain.
           * - EPSW
             -
             - Swelling strain.
           * - NL
             - SEPL
             - Equivalent stress (from stress-strain curve).
           * - "
             - SRAT
             - Stress state ratio.
           * - "
             - HPRES
             - Hydrostatic pressure.
           * - "
             - EPEQ
             - Accumulated equivalent plastic strain.
           * - "
             - PSV
             - Plastic state variable.
           * - "
             - PLWK
             - Plastic work/volume.
           * - SEND
             - ELASTIC
             - Elastic strain energy density.
           * - "
             - PLASTIC
             - Plastic strain energy density.
           * - "
             - CREEP
             - Creep strain energy density.
           * - TG
             - X, Y, Z
             - Component thermal gradient.
           * - TF
             - X, Y, Z
             - Component thermal flux.
           * - PG
             - X, Y, Z
             - Component pressure gradient.
           * - EF
             - X, Y, Z
             - Component electric field.
           * - D
             - X, Y, Z
             - Component electric flux density.
           * - H
             - X, Y, Z
             - Component magnetic field intensity.
           * - B
             - X, Y, Z
             - Component magnetic flux density.
           * - CG
             - X, Y, Z
             - Concentration gradient
           * - DF
             - X, Y, Z
             - Diffusion flux density
           * - FMAG
             - X, Y, Z
             - Component electromagnetic force.
           * - F
             - X, Y, Z
             - X, Y, or Z structural force.
           * - M
             - X, Y, Z
             - X, Y, or Z structural moment.
           * - HEAT
             -
             - Heat flow.
           * - FLOW
             -
             - Fluid flow.
           * - AMPS
             -
             - Current flow.
           * - FLUX
             -
             - Magnetic flux.
           * - CSG
             - X, Y, Z
             - X, Y, or Z magnetic current segment component.
           * - RATE
             -
             - Diffusion flow rate
        """
        command = f"DESOL,{elem},{node},{item},{comp},{v1},{v2},{v3},{v4},{v5},{v6}"
        return self.run(command, **kwargs)

    def detab(
        self,
        elem: str = "",
        lab: str = "",
        v1: str = "",
        v2: str = "",
        v3: str = "",
        v4: str = "",
        v5: str = "",
        v6: str = "",
        **kwargs,
    ):
        r"""Modifies element table results in the database.

        Mechanical APDL Command: `DETAB <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_DETAB.html>`_

        Parameters
        ----------
        elem : str
            Element for which results are to be modified. If ALL, modify all selected elements ( :ref:`esel`
            ) results. If ``ELEM`` = P, graphical picking is enabled and all remaining command fields are
            ignored (valid only in the GUI). A component name may also be substituted for ``ELEM``.

        lab : str
            Label identifying results. Valid labels are as defined with the :ref:`etable` command. Issue
            :ref:`etable`, ``STAT`` to display labels and values.

        v1 : str
            Additional values (if any) assigned to consecutive element table columns.

        v2 : str
            Additional values (if any) assigned to consecutive element table columns.

        v3 : str
            Additional values (if any) assigned to consecutive element table columns.

        v4 : str
            Additional values (if any) assigned to consecutive element table columns.

        v5 : str
            Additional values (if any) assigned to consecutive element table columns.

        v6 : str
            Additional values (if any) assigned to consecutive element table columns.

        Notes
        -----

        .. _DETAB_notes:

        Modifies element table ( :ref:`etable` ) results in the database. For example, :ref:`detab`
        ,35,ABC,1000,2000,1000 assigns 1000, 2000, and 1000 to the first three table columns starting with
        label ABC for element 35. Use the :ref:`pretab` command to list the current results. After deleting
        a column of data using :ref:`etable`, ``Lab``,ERASE, the remaining columns of data are not shifted
        to compress the empty slot. Therefore, the user must allocate null (blank) values for ``V1``,
        ``V2``... ``V6`` for any ETABLE entries which have been deleted by issuing :ref:`etable`,
        ``Lab``,ERASE. All data are stored in the solution coordinate system but will be displayed in the
        results coordinate system ( :ref:`rsys` ).
        """
        command = f"DETAB,{elem},{lab},{v1},{v2},{v3},{v4},{v5},{v6}"
        return self.run(command, **kwargs)

    def dnsol(
        self,
        node: str = "",
        item: str = "",
        comp: str = "",
        v1: str = "",
        v2: str = "",
        v3: str = "",
        v4: str = "",
        v5: str = "",
        v6: str = "",
        datakey: str = "",
        **kwargs,
    ):
        r"""Defines or modifies solution results at a node.

        Mechanical APDL Command: `DNSOL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_DNSOL.html>`_

        Parameters
        ----------
        node : str
            Node for which results are specified. If ALL, apply to all selected nodes ( :ref:`nsel` ). If
            ``NODE`` = P, graphical picking is enabled and all remaining command fields are ignored (valid
            only in the GUI). A component name may also be substituted for ``NODE``.

        item : str
            Label identifying results, see :ref:`DNSOL_tab_1`. Some items also require a component label.

        comp : str
            Component of the item. Valid component labels are shown :ref:`DNSOL_tab_1` below.

        v1 : str
            Value assigned to result. If zero, a zero value will be assigned. If blank, the value remains
            unchanged. Additional values (if any) assigned to the remaining components (in the order
            corresponding to the ``Comp`` list shown below for the specified ``Item`` (starting from the
            specified ``Comp`` label and proceeding to the right).

        v2 : str
            Value assigned to result. If zero, a zero value will be assigned. If blank, the value remains
            unchanged. Additional values (if any) assigned to the remaining components (in the order
            corresponding to the ``Comp`` list shown below for the specified ``Item`` (starting from the
            specified ``Comp`` label and proceeding to the right).

        v3 : str
            Value assigned to result. If zero, a zero value will be assigned. If blank, the value remains
            unchanged. Additional values (if any) assigned to the remaining components (in the order
            corresponding to the ``Comp`` list shown below for the specified ``Item`` (starting from the
            specified ``Comp`` label and proceeding to the right).

        v4 : str
            Value assigned to result. If zero, a zero value will be assigned. If blank, the value remains
            unchanged. Additional values (if any) assigned to the remaining components (in the order
            corresponding to the ``Comp`` list shown below for the specified ``Item`` (starting from the
            specified ``Comp`` label and proceeding to the right).

        v5 : str
            Value assigned to result. If zero, a zero value will be assigned. If blank, the value remains
            unchanged. Additional values (if any) assigned to the remaining components (in the order
            corresponding to the ``Comp`` list shown below for the specified ``Item`` (starting from the
            specified ``Comp`` label and proceeding to the right).

        v6 : str
            Value assigned to result. If zero, a zero value will be assigned. If blank, the value remains
            unchanged. Additional values (if any) assigned to the remaining components (in the order
            corresponding to the ``Comp`` list shown below for the specified ``Item`` (starting from the
            specified ``Comp`` label and proceeding to the right).

        datakey : str
            Key to specify which data is modified:

            * ``AUTO`` - `Nodal-averaged results
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_CH2_2.html#nodeavepost>`_ are
              used if available. Otherwise, the element-based data is used if available. (Default)

            * ``ESOL`` - Only element-based results are used. If they are not available, the command is ignored.

            * ``NAR`` - Only nodal-averaged results are used. If they are not available, the command is ignored.

        Notes
        -----

        .. _DNSOL_notes:

        :ref:`dnsol` can be used only with FULL graphics activated ( :ref:`graphics`,FULL); it will not work
        correctly with PowerGraphics activated.

        :ref:`dnsol` defines or modifies solution results in the database at a node. For example,
        :ref:`dnsol`,35,U,X,.001,.002,.001 assigns values 0.001, 0.002, and 0.001 to UX, UY, and UZ
        (respectively) for node 35. All results that are changed in the database, including the nodal degree
        of freedom results, are available for all subsequent operations. All data is stored in the solution
        coordinate system but is displayed in the results coordinate system ( :ref:`rsys` ). Use
        :ref:`prnsol` to list the current results.

        Data input by :ref:`dnsol` is stored in temporary space and does not replace information in the
        database. Therefore, data input by this command may be overwritten if a change is made to the
        selected set of nodes or if an output operation acts on a new ``Item``.

        Issuing :ref:`dnsol` requires you to place the data type (stress/strain) in the element nodal
        records. To work around this requirement, use the :ref:`desol` command or equivalent path to add a
        dummy element stress/strain record.

        Result items are available depending on element type; check the individual element for availability.
        Valid item and component labels for element results are shown in :ref:`DNSOL_tab_1`.

        Using :ref:`dnsol` with Nodal-Averaged Results
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        If `nodal-averaged results
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_CH2_2.html#nodeavepost>`_ (
        :ref:`outres`,NAR or another nodal-averaged label) are in the database, then :ref:`dnsol` acts on
        the nodal-averaged data for the applicable items (S, EPEL, EPPL, EPCR, EPTH, EPSW) by default. You
        can change this behavior via the ``DataKey`` argument.

        :ref:`dnsol` behavior differs when the command acts on `nodal-averaged results
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_CH2_2.html#nodeavepost>`_.
        The nodal-averaged results that are defined or modified will be apparent in subsequent command
        operations (for example :ref:`prnsol`, :ref:`plnsol` ) in both full model graphics mode (
        :ref:`graphics`,FULL) and PowerGraphics mode ( :ref:`graphics`,POWER). The resultant data is stored
        in the global Cartesian coordinate system but is displayed in the results coordinate system (
        :ref:`rsys` ). :ref:`dnsol` can only be applied to nodal-averaged results if they are already in the
        database; otherwise, the modifications are applied to the element-based solution in temporary
        memory. The modified nodal-averaged results are not saved to the results file automatically. To save
        separate records of modified nodal-averaged results, use :ref:`lcwrite`, :ref:`rappnd`, or
        :ref:`reswrite`.

        :ref:`dnsol` can only modify component values ( ``Comp`` = X, Y, Z, XY, YZ, or XZ) for nodal-
        averaged results. If you attempt to modify principal values using :ref:`dnsol` with ``DataKey`` =
        AUTO, then the modification is applied to element-based results if they are available.

        .. _DNSOL_tab_1:

        DNSOL - Valid Item and Component Labels
        ***************************************

        .. flat-table:: Valid Item and Component Labels for Nodal DOF Results
           :header-rows: 1

           * - Item
             - Comp
             - Description
           * - U
             - X, Y, Z
             - X, Y, or Z structural displacement.
           * - ROT
             - X, Y, Z
             - X, Y, or Z structural rotation.
           * - TEMP[ :ref:`DNSOL_temp` ]
             -
             - Temperature.
           * - PRES
             -
             - Pressure.
           * - VOLT
             -
             - Electric potential.
           * - MAG
             -
             - Magnetic scalar potential.
           * - V
             - X, Y, Z
             - X, Y, or Z fluid velocity.
           * - A
             - X, Y, Z
             - X, Y, or Z magnetic vector potential.
           * - CONC
             -
             - Concentration.


        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.

        .. _DNSOL_temp:

        For ``SHELL131`` and ``SHELL132`` elements with KEYOPT(3) = 0 or 1, use the labels TBOT, TE2,
        TE3,..., TTOP instead of TEMP.

        .. _DNSOL_NAR:

        For these component values, `nodal-averaged results
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_CH2_2.html#nodeavepost>`_ are
        modified if they are available in the results file and ``DataKey`` = AUTO or NAR.

        .. _DNSOL_NAR_2:

        Modifying principal values of nodal-averaged results is not supported.
        """
        command = f"DNSOL,{node},{item},{comp},{v1},{v2},{v3},{v4},{v5},{v6},{datakey}"
        return self.run(command, **kwargs)

    def file(self, fname: str = "", ext: str = "", **kwargs):
        r"""Specifies the data file where results are to be found.

        Mechanical APDL Command: `FILE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_FILE.html>`_

        Parameters
        ----------
        fname : str
            File name and directory path (248 characters maximum, including the characters needed for the
            directory path). An unspecified directory path defaults to the working directory; in this case,
            you can use all 248 characters for the file name. The file name defaults to :file:`Jobname`.

        ext : str
            Filename extension (eight-character maximum). If ``Fname`` is blank, the extension defaults to
            RST (for structural, fluid, or coupled-field analyses), to RTH (for thermal or electrical
            analyses), or to RMG (for magnetic analyses). For postprocessing contact results corresponding
            to the initial contact state in POST1, use the RCN extension. For postprocessing modal
            coordinates results in POST1, use the RDSP or RFRQ extension.

        Notes
        -----

        .. _FILE_notes:

        Specifies the Mechanical APDL data file where the results are to be found for postprocessing.

        Issuing the :ref:`file` command with ``Ext`` = RSDP or RFRQ in POST1 specifies the :file:`.rsdp` or
        :file:`.rfrq` file used by the :ref:`prmc` and :ref:`plmc` commands. (See :ref:`POST1 example
        below.) <FILE_POST1example>`

        **Example Usage**

        .. _FILE_examples:

        .. _FILE_POST1example:

        POST1
        ^^^^^

        .. code:: apdl

           /POST1
           FILE,,rdsp   !Choose file Jobname.rdsp from a previous MSUP transient solution
           PRMC,2,1     !Plot Modal coordinates from rdsp file (loadstep and substep specified as arguments)
           FILE,,rst    !Choose file Jobname.rst
           SET,1,1      !Load results from chosen.rst file into database
           PRNSOL,u,x   !Plot Nodal displacements (loadstep and substep specified using the SET command)
           FINISH       !Exit POST1

        .. _FILE_POST26example:

        POST26
        ^^^^^^
        """
        command = f"FILE,{fname},{ext}"
        return self.run(command, **kwargs)

    def hrcplx(
        self,
        loadstep: str = "",
        substep: str = "",
        omegat: str = "",
        firstlcase: str = "",
        secondlcase: str = "",
        **kwargs,
    ):
        r"""Computes and stores in the database the time-harmonic solution at a prescribed phase angle.

        Mechanical APDL Command: `HRCPLX <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_HRCPLX.html>`_

        Parameters
        ----------
        loadstep : str
            Load step number of the data set to be read (defaults to 1).

        substep : str
            Substep number within ``LOADSTEP``.

        omegat : str
            Angle in degrees (Ω (angle) times T (time)).

            * If ≥ 360°, the amplitude is supplied.

            * All others supply results at that angle. For example, if the angle is set to 0.0°, the real part
              of the solution is supplied. If the angle is set to -90° the imaginary part of the solution is
              supplied.

        firstlcase : str
            First load case number (defaults to 1).

        secondlcase : str
            Second load case number (defaults to 2).

        Notes
        -----

        .. _HRCPLX_notes:

        :ref:`hrcplx` invokes a macro that combines the real and imaginary parts of the solution. If the
        angle is specified, it produces the following:

        .. math::

            equation not available

        R:sub:`R` and R:sub:`I` are, respectively, the real and imaginary parts of the results quantity
        (e.g. the nodal displacements, the reaction forces,...).

        α is the angle (OMEGAT).

        ``1STLCASE`` and ``2NDLCASE`` are internally generated load cases. You may want to specify these to
        avoid overwriting an existing load case number 1 or 2.

        Not all results computed by this command are valid. See `Summable, Non-Summable and Constant Data
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/Hlp_G_BAS5_4.html#apQ8Hn357ctg>`_ in
        the `Basic Analysis Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/Hlp_G_BAS19.html>`_ for more
        information. When the amplitude of the solution is requested ( ``OMEGAT`` >=
        360°), averaged values (such as the nodal component stresses, which are an average of element nodal
        component stresses) are calculated by averaging the amplitudes. Because the degrees of freedom
        results have different phases, derived results (such as the equivalent stress SEQV) are not valid.
        See `POST1 and POST26 - Complex Results Postprocessing
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_post15.html#thyeq1cdmplxres6a>`_

        For postprocessing amplitudes, the only appropriate coordinate system is the solution coordinate
        system ( :ref:`rsys`,SOLU). When displaying the displacement amplitudes, use a contour display (
        :ref:`plnsol` command). Because a deformed shape display ( :ref:`pldisp` command) could lead to a
        non-physical shape, the displacement scaling is off by default ( :ref:`slashdscale`,,OFF).

        For postprocessing cylindrical geometry, it is suggested that you rotate the element coordinate
        systems into the appropriate cylindrical system ( ``EMODIF,,ESYS`` ) before running the solution and
        then view the results in this system ( ``RSYS,SOLU`` ) in POST1.

        Since :ref:`hrcplx` performs load case combinations, it alters most of the data in the database. In
        particular, it alters applied loads such as forces and imposed displacements. To restore the
        original loads in the database for a subsequent analysis, reissue the :ref:`set` command in POST1 to
        retrieve the real and imaginary set data.

        To animate the solution over one period, use the :ref:`anharm` command.

        ``OMEGAT`` is not equal to the phase shift.

        This command is not supported after a cyclic symmetry analysis; use :ref:`cycexpand`,,PHASEANG
        instead.
        """
        command = f"HRCPLX,{loadstep},{substep},{omegat},{firstlcase},{secondlcase}"
        return self.run(command, **kwargs)

    def rescombine(
        self,
        numfiles: str = "",
        fname: str = "",
        ext: str = "",
        lstep: str = "",
        sbstep: str = "",
        fact: str = "",
        kimg: str = "",
        time: str = "",
        angle: str = "",
        nset: str = "",
        order: str = "",
        **kwargs,
    ):
        r"""Reads results from local results files into the database after a distributed-memory parallel
        solution.

        Mechanical APDL Command: `RESCOMBINE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_RESCOMBINE.html>`_

        Parameters
        ----------
        numfiles : str
            Number of local results files that are to be read into the database from the distributed-memory
            parallel solution. This number should be equal to the number of processes used in the parallel
            solution.

        fname : str
            File name (jobname) used during the distributed parallel solution. The file name must be an
            alphanumeric string (up to 32 characters) enclosed in single quotes.

        ext : str
            File extension for the results files (for example, RST, RTH, RMG, etc.). The file extension must
            be an alphanumeric string (up to 8 characters) enclosed in single quotes.

        lstep : str
            Load step number of the data set to be read (defaults to 1):

            * ``N`` - Read load step ``N``.

            * ``FIRST`` - Read the first data set ( ``Sbstep`` and ``TIME`` are ignored).

            * ``LAST`` - Read the last data set ( ``Sbstep`` and ``TIME`` are ignored).

            * ``NEXT`` - Read the next data set ( ``Sbstep`` and ``TIME`` are ignored). If at the last data set,
              the first data set will be read as the next.

            * ``PREVIOUS`` - Read the previous data set ( ``Sbstep`` and ``TIME`` are ignored). If at the first
              data set, the last data set will be read as the previous.

            * ``NEAR`` - Read the data set nearest to ``TIME`` ( ``Sbstep`` is ignored). If ``TIME`` is blank,
              read the first data set.

            * ``LIST`` - Scan the results files and list a summary of each load step ( ``KIMG``, ``TIME``,
              ``ANGLE``, ``NSET``, and ``ORDER`` are ignored.)

        sbstep : str
            Substep number within ``Lstep`` (defaults to the last substep of the load step). For a buckling
            ( :ref:`antype`,BUCKLE) or modal ( :ref:`antype`,MODAL) analysis, ``Sbstep`` corresponds to the
            mode number (defaults to the first mode). Specify ``Sbstep`` = LAST to store the last substep
            for the specified load step.

            If ``Lstep`` = LIST, ``Sbstep`` = 0 or 1 lists the basic step information; ``Sbstep`` = 2 also
            lists the basic step information, but includes the load step title, and labels imaginary data
            sets if they exist.

        fact : str
            Scale factor applied to data read from the files. If zero (or blank), a value of 1.0 is used. A
            nonzero factor excludes non-summable items. Harmonic velocities or accelerations may be
            calculated from the displacement results from a modal ( :ref:`antype`,MODAL) or harmonic (
            :ref:`antype`,HARMIC) analysis. If ``Fact`` = VELO, the harmonic velocities (v) are calculated
            from the displacements (d) at a particular frequency (f) according to the relationship v = 2πfd.
            Similarly, if ``Fact`` = ACEL, the harmonic accelerations (a) are calculated as a = (2πf)
            :sup:`2` d.

        kimg : str
            Used only with complex results (harmonic and complex modal analyses).

            * ``0 or REAL`` - Store the real part of a complex solution (default).

            * ``1, 2 or IMAG`` - Store the imaginary part of a complex solution.

        time : str
            Time-point identifying the data set to be read. For a harmonic analysis, time corresponds to the
            frequency. For a buckling analysis, time corresponds to the load factor. Used only in the
            following cases: If ``Lstep`` = NEAR, read the data set nearest to ``TIME``. If both ``Lstep``
            and ``Sbstep`` are zero (or blank), read data set at time = ``TIME``. If ``TIME`` is between two
            solution time points on the results file, a linear interpolation is done between the two data
            sets. Solution items not written to the results file ( :ref:`outres` ) for either data set will
            result in a null item after data set interpolation. If ``TIME`` is beyond the last time point on
            the file, the last time point will be used.

        angle : str
            Circumferential location (0.0 to 360°). Defines the circumferential location for the harmonic
            calculations used when reading from the results file. The harmonic factor (based on the
            circumferential angle) is applied to the harmonic elements ( ``PLANE25``, ``PLANE75``,
            ``PLANE78``, ``PLANE83``, and ``SHELL61`` ) of the load case. See the `Mechanical APDL Theory
            Reference <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_biblio.html>`_
            for details. Note that factored values of applied constraints and loads will overwrite any
            values existing in the database.

        nset : str
            Data set number of the data set to be read. If a positive value for ``NSET`` is entered,
            ``Lstep``, ``Sbstep``, ``KIMG``, and ``TIME`` are ignored. Available set numbers can be
            determined by :ref:`rescombine`,,,,LIST.

        order : str
            Key to sort the harmonic index results. This option applies to `cyclic symmetry <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cycsym/cycsym_example.html>`_ buckling and modal analyses only, and is valid only when ``Lstep`` = FIRST, LAST, NEXT, PREVIOUS, NEAR or LIST.

            * ``ORDER`` - Sort the harmonic index results in ascending order of eigenfrequencies or buckling
              load multipliers.

            * ``(blank)`` - No sorting takes place.

        Notes
        -----

        .. _RESCOMBINE_notes:

        :ref:`rescombine` is a Mechanical APDL command macro enabling you to combine results from a
        distributed-
        memory parallel ( DMP ) solution. A character string input for any argument must be enclosed in
        single quotes (for example, 'FIRST' input for ``Lstep`` ).

        In a distributed memory parallel solution, a global results file is saved by default. However, if
        you issued :ref:`dmpoption`,RST,NO in the parallel solution, no global results file is written and
        all local results files will be kept. In this case, you can use :ref:`rescombine` in the general
        postprocessor ( :ref:`post1` ) to read results into the database for postprocessing.

        :ref:`rescombine` cannot be used to combine results from local files generated during a distributed-
        memory parallel solution that used the frequency or cyclic harmonic index domain decomposition
        method ( :ref:`ddoption`,FREQ or :ref:`ddoption`,CYCHI).

        To use :ref:`rescombine`, all local results files from the distributed-memory parallel solution must
        be in the current working directory. If running on a single machine, the local results files are
        saved in the working directory by default. If running on a cluster, the local results files are kept
        in the working directory on each compute node. For the latter case, copy the local results files to
        the working directory on the primary compute node.

        Similar to :ref:`set`, :ref:`rescombine` defines the data set to be read from the results files into
        the database. Various operations can also be performed during the read operation. (See :ref:`set`
        for more information.) The database must have the model data available (or issue :ref:`resume`
        before :ref:`rescombine` to restore the geometry from :file:`Jobname.DB` ).

        After issuing :ref:`rescombine` to combine a set of data into the database, you can issue
        :ref:`reswrite` to write the data set into a new results file. The new results file will essentially
        contain the current set of results data for the entire (that is, global) model.

        Upon completion of a :ref:`rescombine` operation, the current file for postprocessing ( :ref:`file`
        ) is set to the last local results file specified via :ref:`rescombine`. For example, if reading in
        four local results files, the results file for POST1 is specified as :file:`Jobname3.RST` when
        :ref:`rescombine` is complete. Therefore, be aware that some downstream postprocessing actions (such
        as :ref:`set` ) may be operating on only this one local results file.

        :ref:`rescombine` is intended for use in POST1. If you want to postprocess DMP solution results
        using the POST26 time-history postprocessor, combine your local results files into one global
        results file ( :ref:`dmpoption`,RST,YES).

        The load case commands in the general postprocessor (such as :ref:`lcdef`, :ref:`lcfile`,
        :ref:`lcoper`, etc.) are not supported when using :ref:`rescombine`. Those commands set up pointers
        in the results file used for postprocessing; they cannot be used with the local results files used
        by :ref:`rescombine`.

        :ref:`cycexpand`, which performs a cyclic expansion, cannot be used with :ref:`rescombine`.
        """
        command = f"RESCOMBINE,{numfiles},{fname},{ext},{lstep},{sbstep},{fact},{kimg},{time},{angle},{nset},{order}"
        return self.run(command, **kwargs)

    def reset(self, **kwargs):
        r"""Resets all POST1 or POST26 specifications to initial defaults.

        Mechanical APDL Command: `RESET <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_RESET.html>`_

        Notes
        -----

        .. _RESET_notes:

        Has the same effect as entering the processor the first time within the run. In POST1, resets all
        specifications to initial defaults, erases all element table items, path table data, and load case
        pointers. In POST26, resets all specifications to initial defaults, erases all variables defined,
        and zeroes the data storage space.
        """
        command = "RESET"
        return self.run(command, **kwargs)

    def set(
        self,
        lstep: str = "",
        sbstep: str = "",
        fact: str = "",
        kimg: str = "",
        time: str = "",
        angle: str = "",
        nset: str = "",
        order: str = "",
        **kwargs,
    ):
        r"""Defines the data set to be read from the results file.

        Mechanical APDL Command: `SET <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SET.html>`_

        .. note::

            From version 0.64 you can use the methods ``to_list`` and ``to_array`` on the object
            returning from ``mapdl.set("list")``.

        Parameters
        ----------
        lstep : str
            Load step number of the data set to be read (defaults to 1):

            * ``N`` - Read load step ``N``.

            * ``FIRST`` - Read the first data set ( ``Sbstep`` and ``TIME`` are ignored).

            * ``LAST`` - Read the last data set ( ``Sbstep`` and ``TIME`` are ignored).

            * ``NEXT`` - Read the next data set ( ``Sbstep`` and ``TIME`` are ignored). If at the last data set,
              the first data set will be read as the next.

            * ``PREVIOUS`` - Read the previous data set ( ``Sbstep`` and ``TIME`` are ignored). If at the first
              data set, the last data set will be read as the previous.

            * ``NEAR`` - Read the data set nearest to ``TIME`` ( ``Sbstep`` is ignored). If ``TIME`` is blank,
              read the first data set.

            * ``LIST`` - Scan the results file and list a summary of each load step. ( ``KIMG``, ``TIME``,
              ``ANGLE``, and ``NSET`` are ignored.)

        sbstep : str
            Substep number (within ``Lstep`` ). Defaults to the last substep of the load step (except in a
            buckling or modal analysis). For a buckling ( :ref:`antype`,BUCKLE) or modal ( :ref:`antype`
            ,MODAL) analysis, ``Sbstep`` corresponds to the mode number. Specify ``Sbstep`` = LAST to store
            the last substep for the specified load step (that is, issue a :ref:`set`, ``Lstep``,LAST
            command).

            If ``Lstep`` = LIST, ``Sbstep`` = 0 or 1 lists the basic step information. ``Sbstep`` = 2 also
            lists the basic step information, but includes the load step title, and labels imaginary data
            sets if they exist.

        fact : str
            Scale factor applied to data read from the file. If zero (or blank), a value of 1.0 is used. A
            nonzero factor excludes non-summable items.

            Harmonic velocities or accelerations can be calculated from the displacement results from a
            modal ( :ref:`antype`,MODAL) or harmonic ( :ref:`antype`,HARMIC) analysis. If ``Fact`` = VELO,
            the harmonic velocities (v) are calculated from the displacements (d) at a particular frequency
            (f) according to the relationship v = 2 πfd. Similarly, if ``Fact`` = ACEL, the harmonic
            accelerations (a) are calculated as a = (2 πf) :sup:`2` d.

            If ``Lstep`` = LIST in an analysis using rezoning, ``Fact`` across all rezoning data sets is
            listed.

        kimg : str
            Used only with complex results (harmonic and complex modal analyses).

            * ``0 or REAL`` - Store the real part of complex solution (default).

            * ``1, 2 or IMAG`` - Store the imaginary part of a complex solution.

            * ``3 or AMPL`` - Store the amplitude

            * ``4 or PHAS`` - Store the phase angle. The angle value, expressed in degrees, will be between
              -180° and +180°.

        time : str
            Time-point identifying the data set to be read. For a harmonic analyses, time corresponds to the
            frequency.

            For a buckling analysis, time corresponds to the load factor.

            Used only in the following cases: If ``Lstep`` = NEAR, read the data set nearest to ``TIME``. If
            both ``Lstep`` and ``Sbstep`` are zero (or blank), read data set at time = ``TIME``.

            Do not use ``TIME`` to identify the data set to be read if you used the arc-length method (
            :ref:`arclen` ) in your solution.

            If ``TIME`` is between two solution time points in the results file, a linear interpolation
            occurs between the two data sets (except in cases where `rezoning
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_nlad/Hlp_G_ADVRZSMP.html>`_ or
            selected results output ( :ref:`osresult` ) is used).

            Solution items not written to the results file ( :ref:`outres` ) for either data set will result
            in a null item after data set interpolation.

            If ``TIME`` is beyond the last time point on the file, the last time point will be used.

            If ``TIME`` is between two solution time points and both ``Lstep`` and ``Sbstep`` are zero (or
            blank), no interpolation is performed for the :ref:`prcint` / :ref:`plcint` commands. (That is,
            for results generated by the :ref:`cint` command, only the data set associated with the lower of
            the solution time points is used.)

        angle : str
            For harmonic elements ( ``PLANE25``, ``PLANE75``, ``PLANE78``, ``PLANE83``, and ``SHELL61`` ),
            ``ANGLE`` specifies the circumferential location (0.0 to 360°) used when reading from the
            results file. The harmonic factor (based on the circumferential angle) is applied to the
            displacements and element results, and to the applied constraints and loads which overwrites any
            values existing in the database. If ``ANGLE`` = NONE, all harmonic factors are set to 1 and
            postprocessing yields the solution output.

            When using ``ANGLE`` = NONE with ``MODE`` > 0, the combined stresses and strains are not valid.

            The default value of ``ANGLE`` is 0.0; however if the :ref:`set` command is not used, the
            effective default is NONE.

            For full harmonic analyses with the amplitude option ( ``KIMG`` = 3 or AMPL), ``ANGLE`` is the
            prescribed phase angle at which the amplitude is computed.

        nset : str
            Data set number of the data set to be read. If a positive value for ``NSET`` is entered,
            ``Lstep``, ``Sbstep``, ``KIMG``, and ``TIME`` are ignored. Available set numbers can be
            determined by :ref:`set`,LIST.

        order : str
            Key to sort the harmonic index results. This option applies to `cyclic symmetry <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cycsym/cycsym_example.html>`_ buckling and modal analyses only, and is valid only when ``Lstep`` = FIRST, LAST, NEXT, PREVIOUS, NEAR or LIST.

            * ``ORDER`` - Sort the harmonic index results in ascending order of eigenfrequencies or buckling
              load multipliers.

            * ``(blank)`` - No sorting takes place.

        Notes
        -----

        .. _SET_notes:

        Defines the data set to be read from the results file into the database. Various operations may also
        be performed during the read operation. The database must have the model geometry available (or use
        the :ref:`resume` command before the :ref:`set` command to restore the geometry from
        :file:`Jobname.DB` ). Values for applied constraints ( :ref:`d` ) and loads ( :ref:`f` ) in the
        database will be replaced by their corresponding values on the results file, if available. (See the
        description of the :ref:`outres` command.) In a single load step analysis, these values are usually
        the same, except for results from harmonic elements. (See the description of the ``ANGLE`` value
        above.)

        In an interactive run, the sorted list ( ``ORDER`` option) is also available for results-set reading
        via a GUI pick option.

        You can postprocess results without issuing a :ref:`set` command if the solution results were saved
        to the database file ( :file:`Jobname.db` ). A distributed-memory parallel simulation, however, can
        only postprocess using the results file (for example, :file:`Jobname.rst` ) and cannot use the
        :file:`Jobname.db` file since no solution results are written to the database. Therefore, you must
        issue a :ref:`set` command or a :ref:`rescombine` command before postprocessing in a distributed-
        memory parallel run.

        When postprocessing amplitudes or phases ( ``KIMG`` = AMPL or PHAS):

        * The only appropriate coordinate system is the solution coordinate system ( :ref:`rsys`,SOLU). For
          layered elements, a layer ( :ref:`layer` ) must also be specified. When displaying the
          displacement amplitudes, use a contour display ( :ref:`plnsol` command). Because a deformed shape
          display ( :ref:`pldisp` command) could lead to a non-physical shape, the displacement scaling is
          off by default ( :ref:`slashdscale`,,OFF).

        * The conversion is not valid for averaged results, derived results (such as principal
          stress/strain, equivalent stress/strain, and USUM), or summed results obtained using :ref:`fsum`,
          :ref:`nforce`, :ref:`prnld`, and :ref:`prrfor`.

        * Cyclic symmetry and multistage cyclic symmetry analysis results are not supported.

        * Coupled-field analysis results are supported when ``KIMG`` = AMPL, but they are not supported when
          ``KIMG`` = PHAS.

        Issuing :ref:`expand` in a Cyclic Symmetry Modal Analysis
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        After issuing :ref:`expand`, ``Nrepeat`` in a cyclic symmetry modal analysis, subsequent :ref:`set`
        commands read data from the results file and expand them to ``Nrepeat`` sectors.

        Issuing :ref:`msopt`,EXPAND in a Multistage Cyclic Symmetry Analysis
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        When issuing :ref:`msopt`,EXPAND in a multistage cyclic symmetry analysis, subsequent :ref:`set`
        commands read the data set from the specified results file and expand the nodes and elements to the
        stages and sectors specified via :ref:`msopt`,EXPAND.
        """
        command = f"SET,{lstep},{sbstep},{fact},{kimg},{time},{angle},{nset},{order}"
        return self.run(command, **kwargs)

    def subset(
        self,
        lstep: str = "",
        sbstep: str = "",
        fact: str = "",
        kimg: int | str = "",
        time: str = "",
        angle: str = "",
        nset: str = "",
        **kwargs,
    ):
        r"""Reads results for the selected portions of the model.

        Mechanical APDL Command: `SUBSET <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SUBSET.html>`_

        Parameters
        ----------
        lstep : str
            Load step number of the data set to be read (defaults to 1):

            * ``N`` - Read load step ``N``.

            * ``FIRST`` - Read the first data set ( ``SBSTEP`` and ``TIME`` are ignored).

            * ``LAST`` - Read the last data set ( ``SBSTEP`` and ``TIME`` are ignored).

            * ``NEXT`` - Read the next data set ( ``SBSTEP`` and ``TIME`` are ignored). If at the last data set,
              the first data set will be read as the next.

            * ``NEAR`` - Read the data set nearest to ``TIME`` ( ``SBSTEP`` is ignored). If ``TIME`` is blank,
              read the first data set.

            * ``LIST`` - Scan the results file and list a summary of each load step. ( ``FACT``, ``KIMG``,
              ``TIME`` and ``ANGLE`` are ignored.)

        sbstep : str
            Substep number (within ``Lstep`` ). For the buckling ( :ref:`antype`,BUCKLE) analysis or the
            modal ( :ref:`antype`,MODAL) analysis, the substep corresponds to the mode number. Defaults to
            last substep of load step (except for :ref:`antype`,BUCKLE or MODAL). If ``Lstep`` = LIST,
            ``SBSTEP`` = 0 or 1 lists the basic step information, whereas ``SBSTEP`` = 2 also lists the load
            step title, and labels imaginary data sets if they exist.

        fact : str
            Scale factor applied to data read from the file. If zero (or blank), a value of 1.0 is used.
            Harmonic velocities or accelerations may be calculated from the displacement results from a
            modal ( :ref:`antype`,MODAL) or harmonic ( :ref:`antype`,HARMIC) analyses. If ``FACT`` = VELO,
            the harmonic velocities (v) are calculated from the displacements (d) at a particular frequency
            (f) according to the relationship v = 2 πfd. Similarly, if ``FACT`` = ACEL, the harmonic
            accelerations (a) are calculated as a = (2 πf) :sup:`2` d.

        kimg : int or str
            Used only with results from complex analyses:

            * ``0`` - Store real part of complex solution

            * ``1`` - Store imaginary part.

        time : str
            Time-point identifying the data set to be read. For harmonic analyses, time corresponds to the
            frequency. For the buckling analysis, time corresponds to the load factor. Used only in the
            following cases: If ``Lstep`` is NEAR, read the data set nearest to ``TIME``. If both ``Lstep``
            and ``SBSTEP`` are zero (or blank), read data set at time = ``TIME``. If ``TIME`` is between two
            solution time points on the results file, a linear interpolation is done between the two data
            sets. Solution items not written to the results file ( :ref:`outres` ) for either data set will
            result in a null item after data set interpolation. If ``TIME`` is beyond the last time point on
            the file, use the last time point.

        angle : str
            Circumferential location (0.0 to 360°). Defines the circumferential location for the harmonic
            calculations used when reading from the results file. The harmonic factor (based on the
            circumferential angle) is applied to the harmonic elements ( ``PLANE25``, ``PLANE75``,
            ``PLANE78``, ``PLANE83``, and ``SHELL61`` ) of the load case. See the `Mechanical APDL Theory
            Reference <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_biblio.html>`_
            for details. Note that factored values of applied constraints and loads will overwrite any
            values existing in the database.

        nset : str
            Data set number of the data set to be read. If a positive value for ``NSET`` is entered,
            ``Lstep``, ``SBSTEP``, ``KIMG``, and ``TIME`` are ignored. Available set numbers can be
            determined by :ref:`set`,LIST.

        Notes
        -----

        .. _SUBSET_notes:

        Reads a data set from the results file into the database for the selected portions of the model
        only. Data that has not been specified for retrieval from the results file by the :ref:`inres`
        command will be listed as having a zero value. Each time that the :ref:`subset` command is issued,
        the data currently in the database will be overwritten with a new set of data. Various operations
        may also be performed during the read operation. The database must have the model geometry available
        (or used the :ref:`resume` command before the :ref:`subset` command to restore the geometry from
        :file:`File.DB` ).
        """
        command = f"SUBSET,{lstep},{sbstep},{fact},{kimg},{time},{angle},{nset}"
        return self.run(command, **kwargs)
