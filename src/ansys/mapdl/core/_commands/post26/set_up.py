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

from ansys.mapdl.core._commands import CommandsBase


class SetUp(CommandsBase):

    def ansol(
        self,
        nvar: str = "",
        node: str = "",
        item: str = "",
        comp: str = "",
        name: str = "",
        mat: str = "",
        real: str = "",
        ename: str = "",
        datakey: str = "",
        **kwargs,
    ):
        r"""Specifies averaged element nodal data to be stored from the results file.

        Mechanical APDL Command: `ANSOL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ANSOL.html>`_

        Parameters
        ----------
        nvar : str
            Arbitrary reference number assigned to this variable (2 to ``NV`` ( :ref:`numvar` )). Overwrites
            any existing results for this variable.

        node : str
            Node number for which data are to be stored.

        item : str
            Label identifying the item. General item labels are shown in :ref:`ANSOL_tab_1` below. Some
            items also require a component label.

        comp : str
            Component of the item (if required). General component labels are shown in :ref:`ANSOL_tab_1`.
            Selected result components ( ``Item`` = SRES) are shown in :ref:`ANSOL_tab_2`.

        name : str
            32-character name to identify the item on the printout and displays. Default: An eight-character
            label formed by concatenating the first four characters of the ``Item`` and ``Comp`` labels.

        mat : str
            Material number. Average is calculated based on the subset of elements with the specified
            material number. Default: Use all elements in the active set unless ``Real`` and/or ``Ename`` is
            specified.

        real : str
            Real number. Average is calculated based on the subset of elements with the specified real
            number. Default: Use all elements in the active set unless ``Mat`` and/or ``Ename`` is
            specified.

        ename : str
            Element type name. Average is calculated based on the subset of elements with the specified
            element type name. Default: Use all elements in the active set unless ``Mat`` and/or ``Real`` is
            specified.

        datakey : str
            Key to specify which data is stored:

            * ``AUTO`` - `Nodal-averaged results
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_CH2_2.html#nodeavepost>`_ are
              used if they are available for the first applicable time step; otherwise, the element-based data is
              used, if available. (Default.)

            * ``ESOL`` - Only element-based results are used. If they are not available, the command is ignored.

            * ``NAR`` - Only nodal-averaged results are used. If they are not available, the command is ignored.

            ``Mat``, ``Real``, and ``Ename`` are ignored when nodal-averaged results are used.

        Notes
        -----

        .. _ANSOL_notes:

        Valid item and component labels for element nodal results are listed in :ref:`ANSOL_tab_1`.

        :ref:`ansol` defines element nodal results data to be stored from a results file ( :ref:`file` ).
        Not all items are valid for all nodes. See the input and output summary tables of each element
        attached to the node for the available items.

        If `nodal-averaged results
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_CH2_2.html#nodeavepost>`_ (
        :ref:`outres`,NAR or another nodal-averaged label) are available, then :ref:`ansol` uses the nodal-
        averaged data for the applicable items (S, EPEL, EPPL, EPCR, EPTH) as dictated by the by ``DataKey``
        argument. By default, ( ``DataKey`` = AUTO), the availability of nodal-averaged results or element-
        based data is determined at the first load step that has results for the associated item. For more
        information, see `Postprocessing Nodal-Averaged Results
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_CH2_2.html#>`_

        **Coordinate systems:** Generally, element nodal quantities stored by :ref:`ansol` are obtained in
        the solution coordinate system ( :ref:`rsys`, SOLU) and then averaged. There are some exceptions as
        listed below. :ref:`ansol` does not transform results from :ref:`rsys`,SOLU (or from the coordinate
        systems described for the exceptions below) to other coordinate systems. Verify that all elements
        attached to the subject node have the same coordinate system before using :ref:`ansol`.

        * Layered element results are in the layer coordinate system ( :ref:`rsys`,LSYS). You can further
          specify the element nodal results, for some elements, with the :ref:`shell`, :ref:`layerp26`, and
          :ref:`force` commands.

        * When :ref:`ansol` is used to store nodal-averaged result data (based on the ``DataType`` setting),
          the global Cartesian coordinate system ( :ref:`rsys`,0) is used.

        **Shell elements:** The default shell element coordinate system is based on node ordering. For shell
        elements the
        adjacent elements could have a different :ref:`rsys`,SOLU, making the resultant averaged data
        inconsistent. A message to this effect is issued when :ref:`ansol` is used in models containing
        shell elements. Ensure that consistent coordinate systems are active for all associated elements
        used by the :ref:`ansol` command.

        **Derived quantities:** Some of the result items supported by :ref:`ansol` ( :ref:`ANSOL_tab_1` )
        are derived from the component quantities. Issue :ref:`avprin` to specify the principal and vector
        sum quantity averaging methods.

        **Default:** If ``Mat``, ``Real``, and ``Ename`` are not specified, all elements attached to the
        node are considered. When a material ID, real constant ID, or element-type discontinuity is detected
        at a node, a message is issued. For example, in a FSI analysis, a ``FLUID30`` element at the
        structure interface would be considered; however, because it contains no SX result, it is not used
        during :ref:`store` operations.

        .. _ANSOL_tab_1:

        ANSOL - General Result Item and Component Labels
        ************************************************

        .. flat-table:: General Item and Component Labels :ref:`ansol`, ``NVAR,NODE,Item,Comp,Name,Mat,Real,Ename,DataType``
           :header-rows: 1

           * - Item
             - Comp
             - Description
           * - :rspan:`3` S
             - X, Y, Z, XY, YZ, XZ
             - Component stress. This item stores `nodal-averaged results <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_CH2_2.html#nodeavepost>`_ if they are available on the results file.
           * - 1, 2, 3
             - Principal stress.
           * - INT
             - Stress intensity.
           * - EQV
             - Equivalent stress.
           * - :rspan:`3` EPEL
             - X, Y, Z, XY, YZ, XZ
             - Component elastic strain.
           * - 1, 2, 3
             - Principal elastic strain.
           * - INT
             - Elastic strain intensity.
           * - EQV
             - Elastic equivalent strain.
           * - :rspan:`3` EPPL
             - X, Y, Z, XY, YZ, XZ
             - Component plastic strain.
           * - 1, 2, 3
             - Principal plastic strain.
           * - INT
             - Plastic strain intensity.
           * - EQV
             - Plastic equivalent strain.
           * - :rspan:`3` EPCR
             - X, Y, Z, XY, YZ, XZ
             - Component creep strain.
           * - 1,2,3
             - Principal creep strain.
           * - INT
             - Creep strain intensity.
           * - EQV
             - Creep equivalent strain.
           * - :rspan:`3` EPTH
             - X, Y, Z, XY, YZ, XZ
             - Component thermal strain.
           * - 1, 2, 3
             - Principal thermal strain.
           * - INT
             - Thermal strain intensity.
           * - EQV
             - Thermal equivalent strain.
           * - :rspan:`3` ESIG
             - X, Y, Z, XY, YZ, XZ
             - Components of Biot``s effective stress.
           * - 1, 2, 3
             - Principal stresses of Biot's effective stress.
           * - INT
             - Stress intensity of Biot's effective stress.
           * - EQV
             - Equivalent stress of Biot's effective stress.
           * - :rspan:`6` NL
             - SEPL
             - Equivalent stress (from stress-strain curve).
           * - SRAT
             - Stress state ratio.
           * - HPRES
             - Hydrostatic pressure.
           * - EPEQ
             - Accumulated equivalent plastic strain.
           * - CREQ
             - Accumulated equivalent creep strain.
           * - PSV
             - Plastic state variable.
           * - PLWK
             - Plastic work/volume.
           * - :rspan:`9` CONT
             - STAT For more information about the meaning of contact status and its possible values, see `Reviewing Results in POST1 <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_ctec/Hlp_ctec_revresu.html#ctecpostslide>`_
             - Contact status.
           * - PENE
             - Contact penetration.
           * - PRES
             - Contact pressure.
           * - SFRIC
             - Contact friction stress.
           * - STOT
             - Contact total stress (pressure plus friction).
           * - SLIDE
             - Contact sliding distance.
           * - GAP
             - Contact gap distance.
           * - FLUX
             - Total heat flux at contact surface.
           * - CNOS
             - Total number of contact status changes during substep.
           * - FPRS
             - Fluid penetration pressure.
           * - TG
             - X, Y, Z, SUM ``Comp`` = SUM is not supported for coupled pore-pressure-thermal (CPT ``nnn`` ) elements.
             - Component thermal gradient or vector sum.
           * - TF
             - X, Y, Z, SUM
             - Component thermal flux or vector sum.
           * - PG
             - X, Y, Z, SUM
             - Component pressure gradient or vector sum.
           * - EF
             - X, Y, Z, SUM
             - Component electric field or vector sum.
           * - D
             - X, Y, Z, SUM
             - Component electric flux density or vector sum.
           * - H
             - X, Y, Z, SUM
             - Component magnetic field intensity or vector sum.
           * - B
             - X, Y, Z, SUM
             - Component magnetic flux density or vector sum.
           * - CG
             - X, Y, Z, SUM
             - Component concentration gradient or vector sum.
           * - DF
             - X, Y, Z, SUM
             - Component diffusion flux density or vector sum.
           * - JC
             - X, Y, Z, SUM
             - Conduction current density for elements that support conduction current calculation. Components (X, Y, Z) and vector sum (SUM).
           * - FFLX
             - X, Y, Z
             - Fluid-flow flux in poromechanics.
           * - FGRA
             - X, Y, Z
             - Fluid pore-pressure gradient in poromechanics.
           * - PMSV
             - VRAT, PPRE, DSAT, RPER
             - Void volume ratio, pore pressure, degree of saturation, and relative permeability for coupled pore-pressure-thermal elements.
           * - NS
             - X, Y, Z, XY, YZ, XZ
             - `Nominal strain <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_mat5.html#eq4dc2eb28-41da-4d81-b0d0-8716ce41a6e1>`_ for hyperelastic material, reported in the current configuration (unaffected by :ref:`rsys` ).
           * - MPLA
             - DMAC, DMAX
             - Microplane damage, macroscopic and maximum values.
           * - MPDP
             - TOTA, TENS, COMP, RW
             - Microplane homogenized total, tension, and compression damages (TOTA, TENS, COMP), and split weight factor (RW).
           * - EPFR
             -
             - Free strain in porous media
           * - DAMAGE
             - 1,2,3,MAX
             - Damage in directions 1, 2, 3 (1, 2, 3) and the maximum damage (MAX).
           * - GDMG
             -
             - Damage
           * - IDIS
             -
             - Structural-thermal dissipation rate


        .. _ANSOL_tab_2:

        ANSOL - Selected Result Component Labels
        ****************************************

        .. flat-table:: Selected Result Component Labels :ref:`ansol`, ``NVAR``, ``NODE``,SRES, ``Comp``, ``Name``, ``Mat``, ``Real``, ``Ename``
           :header-rows: 1

           * - Comp
             - Description
           * - SVAR ``n``
             - The ``n`` th state variable.
           * - FLDUF0 ``n``
             - The ``n`` th user-defined field variable.
        """
        command = (
            f"ANSOL,{nvar},{node},{item},{comp},{name},{mat},{real},{ename},{datakey}"
        )
        return self.run(command, **kwargs)

    def cisol(
        self,
        n: str = "",
        id_: str = "",
        node: str = "",
        cont: str = "",
        dtype: str = "",
        **kwargs,
    ):
        r"""Stores fracture parameter information in a variable.

        Mechanical APDL Command: `CISOL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CISOL.html>`_

        Parameters
        ----------
        n : str
            Arbitrary reference number or name assigned to this variable. Number must be >1 but </= NUMVAR.

        id_ : str
            Crack ID number.

        node : str
            Crack tip node number.

        cont : str
            Contour number.

        dtype : str
            Data type to output:

            * ``JINT`` - J-integral

            * ``IIN1`` - Interaction integral 1

            * ``IIN2`` - Interaction integral 2

            * ``IIN3`` - Interaction integral 3

            * ``K1`` - Mode 1 stress-intensity factor

            * ``K2`` - Mode 2 stress-intensity factor

            * ``K3`` - Mode 3 stress-intensity factor

            * ``G1`` - Mode 1 energy release rate

            * ``G2`` - Mode 2 energy release rate

            * ``G3`` - Mode 3 energy release rate

            * ``GT`` - Total energy release rate

            * ``MFTX`` - Total material force X

            * ``MFTY`` - Total material force Y

            * ``MFTZ`` - Total material force Z

            * ``CEXT`` - Crack extension
        """
        command = f"CISOL,{n},{id_},{node},{cont},{dtype}"
        return self.run(command, **kwargs)

    def data(
        self,
        ir: str = "",
        lstrt: str = "",
        lstop: str = "",
        linc: str = "",
        name: str = "",
        kcplx: int | str = "",
        **kwargs,
    ):
        r"""Reads data records from a file into a variable.

        Mechanical APDL Command: `DATA <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_DATA.html>`_

        Parameters
        ----------
        ir : str
            Arbitrary reference number assigned to the resulting variable (2 to NV ( :ref:`numvar` )). If
            this number is the same as for a previously defined variable, the previously defined variable
            will be overwritten with this result.

        lstrt : str
            Start at location ``LSTRT`` (defaults to 1).

        lstop : str
            Stop at location ``LSTOP`` (defaults to ``LSTRT`` ). Maximum location available is determined
            from data previously stored.

        linc : str
            Fill every ``LINC`` location between ``LSTRT`` and ``LSTOP`` (defaults to 1).

        name : str
            Eight character name for identifying the variable on the printout and displays. Embedded blanks
            are compressed upon output.

        kcplx : int or str
            Complex number key:

            * ``0`` - Data stored as the real part of the complex number.

            * ``1`` - Data stored as the imaginary part of the complex number.

        Notes
        -----

        .. _DATA_notes:

        This command must be followed by a format statement (on the next line) and the subsequent data
        records, and all must be on the same file (that may then be read with the :ref:`input` command). The
        format specifies the number of fields to be read per record, the field width, and the placement of
        the decimal point (if one is not included in the data value). The read operation follows the
        available FORTRAN FORMAT conventions of the system. See the system FORTRAN manual for details. Any
        standard FORTRAN real format (such as (4F6.0), (F2.0,2X,F12.0), etc.) may be used. Integer (I),
        character (A), and list-directed (\2) descriptors may not be used. The parentheses must be included
        in the format. Up to 80 columns per record may be read. Locations may be filled within a range.
        Previous data in the range will be overwritten.
        """
        command = f"DATA,{ir},{lstrt},{lstop},{linc},{name},{kcplx}"
        return self.run(command, **kwargs)

    def enersol(self, nvar: str = "", item: str = "", name: str = "", **kwargs):
        r"""Specifies the total energies to be stored.

        Mechanical APDL Command: `ENERSOL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ENERSOL.html>`_

        Parameters
        ----------
        nvar : str
            Arbitrary reference number assigned to this variable (2 to NV).

        item : str

            * ``SENE`` - Potential energy (stiffness energy)

            * ``KENE`` - Kinetic energy

            * ``DENE`` - Damping energy

            * ``WEXT`` - Work done by external load

            * ``AENE`` - Artificial energy due to hourglass control/drill stiffness or due to contact
              stabilization damping

            * ``STEN`` - Artificial energy due to nonlinear stabilization

        name : str
            A 32-character name identifying the item on printouts and displays. Defaults to a 4-character
            label formed by the four characters of the ``Item`` value.

        Notes
        -----

        .. _ENERSOL_Notes:

        Damping energy (DENE) and work done by external loads (WEXT) are available only if the following
        were set prior to the analysis solution: ``EngCalc`` = YES on the :ref:`trnopt`, :ref:`hrout` or
        :ref:`mxpand` command; and ``Item`` = VENG, ESOL, or ALL on the :ref:`outres` command.

        If ``EngCalc`` = YES on the :ref:`hrout` or :ref:`mxpand` command, ``Item`` = SENE and KENE are the
        average potential and kinetic energies, respectively.
        """
        command = f"ENERSOL,{nvar},{item},,{name}"
        return self.run(command, **kwargs)

    def esol(
        self,
        nvar: str = "",
        elem: str = "",
        node: str = "",
        item: str = "",
        comp: str = "",
        name: str = "",
        **kwargs,
    ):
        r"""Specifies element data to be stored from the results file.

        Mechanical APDL Command: `ESOL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ESOL.html>`_

        Parameters
        ----------
        nvar : str
            Arbitrary reference number assigned to this variable (2 to ``NV`` ( :ref:`numvar` )). Overwrites
            any existing results for this variable.

        elem : str
            Element for which data are to be stored. If ``ELEM`` = P, graphical picking is enabled (valid
            only in the GUI).

        node : str
            Node number on this element for which data are to be stored. If blank, store the average element
            value (except for ``FMAG`` values, which are summed instead of averaged). If ``NODE`` = P,
            graphical picking is enabled (valid only in the GUI).

        item : str
            Label identifying the item. General item labels are shown in :ref:`ESOL_tab_1`. Some items also
            require a component label.

        comp : str
            Component of the item (if required). General component labels are shown in :ref:`ESOL_tab_1`
            below. If ``Comp`` is a sequence number ( ``n`` ), the ``NODE`` field is ignored.

        name : str
            32-character name for identifying the item on the printout and displays. Defaults to a label
            formed by concatenating the first four characters of the ``Item`` and ``Comp`` labels.

        Notes
        -----

        .. _ESOL_notes:

        See :ref:`ESOL_tab_1` for a list of item and component labels for element (excluding line element)
        results. See :ref:`ESOL_tab_2` for a list of valid selected result ( ``Item`` = SRES) components.

        :ref:`esol` defines element results data to be stored from a results file ( :ref:`file` ). Not all
        items are valid for all elements. To see the available items for a given element, refer to the input
        and output summary tables in the documentation for that element.

        Two methods of data access are available via the :ref:`esol` command. You can access some data by
        using a generic label ( component name method ), while others require a label and number ( sequence
        number method ).

        Use the component name method to access general element data (that is, element data generally
        available to most element types or groups of element types). Element results are in the element
        coordinate system, except for layered elements where results are in the layer coordinate system.
        Element forces and moments are in the nodal coordinate system. Results are obtainable for an element
        at a specified node. Further location specifications can be made for some elements via :ref:`shell`,
        :ref:`layerp26`, and :ref:`force`.

        The sequence number method is required for data that is not averaged (such as pressures at nodes and
        temperatures at integration points), or data that is not easily described generically (such as all
        derived data for structural line elements and contact elements, all derived data for thermal line
        elements, and layer data for layered elements).

        In a `2D to 3D analysis
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_adv/Hlp_G_ADV2DTO3DREST.html>`_, this
        command not supported in the POST26 postprocessor and is ignored.

        .. _ESOL_tab_1:

        ESOL - General Result Item and Component Labels
        ***********************************************

        .. flat-table:: Component Name Method
           :header-rows: 1

           * - Item
             - Comp
             - Description
           * - :rspan:`3` S
             - X, Y, Z, XY, YZ, XZ
             - Component stress.
           * - 1, 2, 3
             - Principal stress.
           * - INT
             - Stress intensity.
           * - EQV
             - Equivalent stress.
           * - :rspan:`3` EPEL
             - X, Y, Z, XY, YZ, XZ
             - Component elastic strain.
           * - 1, 2, 3
             - Principal elastic strain.
           * - INT
             - Elastic strain intensity.
           * - EQV
             - Elastic equivalent strain.
           * - :rspan:`3` EPTH
             - X, Y, Z, XY, YZ, XZ
             - Component thermal strain.
           * - 1, 2, 3
             - Principal thermal strain.
           * - INT
             - Thermal strain intensity.
           * - EQV
             - Thermal equivalent strain.
           * - :rspan:`3` EPPL
             - X, Y, Z, XY, YZ, XZ
             - Component plastic strain.
           * - 1, 2, 3
             - Principal plastic strain.
           * - INT
             - Plastic strain intensity.
           * - EQV
             - Plastic equivalent strain.
           * - :rspan:`3` EPCR
             - X, Y, Z, XY, YZ, XZ
             - Component creep strain.
           * - 1,2,3
             - Principal creep strain.
           * - INT
             - Creep strain intensity.
           * - EQV
             - Creep equivalent strain.
           * - :rspan:`3` EPDI
             - X, Y, Z, XY, YZ, XZ
             - Component diffusion strain.
           * - 1, 2, 3
             - Principal diffusion strain.
           * - INT
             - Diffusion strain intensity.
           * - EQV
             - Diffusion equivalent strain.
           * - :rspan:`6` NL
             - SEPL
             - Equivalent stress (from stress-strain curve).
           * - SRAT
             - Stress state ratio.
           * - HPRES
             - Hydrostatic pressure.
           * - EPEQ
             - Accumulated equivalent plastic strain.
           * - CREQ
             - Accumulated equivalent creep strain.
           * - PSV
             - Plastic state variable.
           * - PLWK
             - Plastic work/volume.
           * - :rspan:`7` SEND
             - ELASTIC The results for this postprocessing SEND component are invalid for ``ELBOW290`` if that element is used with viscoelastic or viscohyperelastic materials.
             - Elastic strain energy density. (For `viscoelastic <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/evis.html#mat_harmvisco>`_ and `sintering <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/amp8sq21dldm.html#>`_ materials, the `stored energy <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/evis.html#eq92b60ee3-7e22-457b-9543-53f86d16432a>`_.)
           * - PLASTIC
             - Plastic strain energy density.
           * - CREEP
             - Creep strain energy density.
           * - DAMAGE
             - Damage strain energy density.
           * - VDAM
             - Viscoelastic dissipation energy density.
           * - VREG
             - Visco-regularization strain energy density.
           * - DISS
             - Structural-thermal dissipation.
           * - ENTO
             - Total strain energy density (sum of ELASTIC, PLASTIC, and CREEP strain energy densities).
           * - :rspan:`1` CDM
             - DMG
             - Damage variable.
           * - LM
             - Maximum previous strain energy for virgin material.
           * - GKS
             - X
             - Gasket component stress (also gasket pressure).
           * - GKD
             - X
             - Gasket component total closure.
           * - GKDI
             - X
             - Gasket component total inelastic closure.
           * - GKTH
             - X
             - Gasket component thermal closure.
           * - SS
             - X, XY, XZ
             - Interface traction (stress).
           * - SD
             - X,XY,XZ
             - Interface separation.
           * - :rspan:`9` CONT
             - STAT For more information about the meaning of contact status and its possible values, see `Reviewing Results in POST1 <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_ctec/Hlp_ctec_revresu.html#ctecpostslide>`_
             - Contact status.
           * - PENE
             - Contact penetration.
           * - PRES
             - Contact pressure.
           * - SFRIC
             - Contact friction stress.
           * - STOT
             - Contact total stress (pressure plus friction).
           * - SLIDE
             - Contact sliding distance.
           * - GAP
             - Contact gap distance.
           * - FLUX
             - Total heat flux at contact surface.
           * - CNOS
             - Total number of contact status changes during substep.
           * - FPRS
             - Fluid penetration pressure.
           * - TG For ``SHELL131`` and ``SHELL132`` elements with KEYOPT(3) = 0 or 1, use the labels HBOT, HE2, HE3, ..., HTOP instead of HEAT.
             - X, Y, Z, SUM
             - Component thermal gradient or vector sum.
           * - TF
             - X, Y, Z, SUM
             - Component thermal flux or vector sum.
           * - PG
             - X, Y, Z, SUM
             - Component pressure gradient or vector sum.
           * - EF
             - X, Y, Z, SUM
             - Component electric field or vector sum.
           * - D
             - X, Y, Z, SUM
             - Component electric flux density or vector sum.
           * - H
             - X, Y, Z, SUM
             - Component magnetic field intensity or vector sum.
           * - B
             - X, Y, Z, SUM
             - Component magnetic flux density or vector sum.
           * - CG
             - X, Y, Z, SUM
             - Component concentration gradient or vector sum.
           * - DF
             - X, Y, Z, SUM
             - Component diffusion flux density or vector sum.
           * - FMAG
             - X, Y, Z, SUM
             - Component electromagnetic forces or vector sum.
           * - P
             - X, Y, Z, SUM
             - Poynting vector components or vector sum
           * - F
             - X, Y, Z
             - Component structural force.
           * - M
             - X, Y, Z
             - Component structural moment.
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
             - Component magnetic current segment.
           * - RATE
             -
             - Diffusion flow rate.
           * - SENE
             -
             - "Stiffness" energy.
           * - STEN
             -
             - Elemental energy dissipation due to `stabilization <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STRUNST.html#>`_.
           * - KENE
             -
             - Kinetic energy.
           * - ASENE
             -
             - Amplitude stiffness energy.
           * - PSENE
             -
             - Peak stiffness energy.
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
           * - AENE
             -
             - Artificial energy due to hourglass control/drill stiffness or due to contact stabilization.
           * - JHEAT
             -
             - Element Joule heat generation.
           * - JC
             - X, Y, Z, SUM
             - Conduction current density for elements that support conduction current calculation. Components (X, Y, Z) and vector sum (SUM).
           * - JS
             - X, Y, Z
             - Source current density for low-frequency magnetic analyses. Total current density (sum of conduction and displacement current densities) in low-frequency electric analyses. Components (X, Y, Z).
           * - JT
             - X, Y, Z, SUM
             - Total measurable current density in low-frequency electromagnetic analyses. (Conduction current density in a low-frequency electric analysis.) Components (X, Y, Z) and vector sum (SUM).
           * - MRE
             -
             - Magnetics Reynolds number.
           * - VOLU
             -
             - Volume of volume element.
           * - BFE
             - TEMP
             - Body temperatures (calculated from applied temperatures) as used in solution (area and volume elements only).
           * - FICT
             - TEMP
             - Fictive temperature.
           * - CAP
             - C0,X0,K0,ZONE, DPLS,VPLS
             - Material cap plasticity model only: Cohesion; hydrostatic compaction yielding stress; I1 at the transition point at which the shear and compaction envelopes intersect; zone = 0: elastic state, zone = 1: compaction zone, zone = 2: shear zone, zone = 3: expansion zone; effective deviatoric plastic strain; volume plastic strain.
           * - EDPC
             - CSIG,CSTR
             - Material EDP creep model only (not including the cap model): Equivalent creep stress; equivalent creep strain.
           * - FFLX
             - X, Y, Z
             - Fluid flux flow in poromechanics.
           * - FGRA
             - X, Y, Z
             - Fluid pore pressure gradient in poromechanics.
           * - PMSV
             - VRAT, PPRE, DSAT, RPER
             - Void volume ratio, pore pressure, degree of saturation, and relative permeability for coupled pore-pressure-thermal elements.
           * - YSIDX
             - TENS,SHEA
             - Yield surface activity status for Mohr-Coulomb, soil, concrete, and joint rock material models: 1 = yielded, 0 = not yielded.
           * - FPIDX
             - TF01,SF01, TF02,SF02, TF03,SF03, TF04,SF04
             - Failure plane surface activity status for concrete and joint rock material models: 1 = yielded, 0 = not yielded. Tension and shear failure status are available for all four sets of failure planes.
           * - NS
             - X, Y, Z, XY, YZ, XZ
             - `Nominal strain <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_mat5.html#eq4dc2eb28-41da-4d81-b0d0-8716ce41a6e1>`_ for hyperelastic material, reported in the current configuration (unaffected by :ref:`rsys` ).
           * - MPLA
             - DMAC, DMAX
             - Microplane damage, macroscopic and maximum values.
           * - MPDP
             - TOTA, TENS, COMP, RW
             - Microplane homogenized total, tension, and compression damages (TOTA, TENS, COMP), and split weight factor (RW).
           * - DAMAGE
             - 1,2,3,MAX
             - Damage in directions 1, 2, 3 (1, 2, 3) and the maximum damage (MAX).
           * - GDMG
             -
             - Damage
           * - IDIS
             -
             - Structural-thermal dissipation rate
           * - BKS
             - X, Y, Z, XY, YZ, XZ
             - Total `nonlinear kinematic backstress <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/amp8sq21dldm.html#>`_ reported in the current configuration (unaffected by :ref:`rsys` ). Available for 3D, plane strain, and axisymmetric elements.
           * - BKS1,...,BKS5
             - X, Y, Z, XY, YZ, XZ
             - Superimposed components of the total `nonlinear kinematic backstress`_ reported in the current configuration (unaffected by :ref:`rsys` ). Available for 3D, plane strain, and axisymmetric elements when more than one superimposed back-stress component is defined.
           * - EPFR
             -
             - Free strain in porous media
           * - FC1S
             - 1,2,3,4,5,6
             - First set of six components of FCC crystal slip. Available for 3D elements only.
           * - FC2S
             - 1,2,3,4,5,6
             - Second set of six components of FCC crystal slip. Available for 3D elements only.
           * - HC1S
             - 1,2,3,4,5,6
             - Six components of HCP crystal slip on basal and prismatic systems. Available for 3D elements only.
           * - HC2S
             - 1,2,3,4,5,6
             - Six components of HCP crystal slip on pyramidal system. Available for 3D elements only.
           * - HC3S
             - 1,2,3,4,5,6
             - First set of six components of HCP crystal slip on the first-order pyramidal system. Available for 3D elements only.
           * - HC4S
             - 1,2,3,4,5,6
             - Second set of six components of HCP crystal slip on the first-order pyramidal system. Available for 3D elements only.
           * - HC5S
             - 1,2,3,4,5,6
             - Six components of HCP crystal slip on the second-order pyramidal system. Available for 3D elements only.
           * - BC1S
             - 1,2,3,4,5,6
             - First set of six components of BCC slip on 111 plane. Available for 3D elements only.
           * - BC2S
             - 1,2,3,4,5,6
             - Second set of six components of BCC slip on 111 plane. Available for 3D elements only.
           * - BC3S
             - 1,2,3,4,5,6
             - First set of six components of BCC slip on 112 plane. Available for 3D elements only.
           * - BC4S
             - 1,2,3,4,5,6
             - Second set of six components of BCC slip on 112 plane. Available for 3D elements only.
           * - BC5S
             - 1,2,3,4,5,6
             - First set of six components of BCC slip on 123 plane. Available for 3D elements only.
           * - BC6S
             - 1,2,3,4,5,6
             - Second set of six components of BCC slip on 123 plane. Available for 3D elements only.
           * - BC7S
             - 1,2,3,4,5,6
             - Third set of six components of BCC slip on 123 plane. Available for 3D elements only.
           * - BC8S
             - 1,2,3,4,5,6
             - Fourth set of six components of BCC slip on 123 plane. Available for 3D elements only.
           * - FC1H
             - 1,2,3,4,5,6
             - First set of six components of FCC crystal hardness. Available for 3D elements only.
           * - FC2H
             - 1,2,3,4,5,6
             - Second set of six components of FCC crystal hardness. Available for 3D elements only.
           * - HC1H
             - 1,2,3,4,5,6
             - Sixcomponents of HCP crystal hardness on basal and prismatic systems. Available for 3D elements.
           * - HC2H
             - 1,2,3,4,5,6
             - Six components of HCP crystal hardness on pyramidal system. Available for 3D elements only.
           * - HC3H
             - 1,2,3,4,5,6
             - First set of six components of HCP crystal hardness on the first-order pyramidal system. Available for 3D elements only.
           * - HC4H
             - 1,2,3,4,5,6
             - Second set of six components of HCP crystal hardness on the first-order pyramidal system. Available for 3D elements only.
           * - HC5H
             - 1,2,3,4,5,6
             - Six components of HCP crystal hardness on the second-order pyramidal system. Available for 3D elements only.
           * - BC1H
             - 1,2,3,4,5,6
             - First set of six components of BCC hardness on 111 plane. Available for 3D elements only.
           * - BC2H
             - 1,2,3,4,5,6
             - Second set of six components of BCC hardness on 111 plane. Available for 3D elements only.
           * - BC3H
             - 1,2,3,4,5,6
             - First set of six components of BCC hardness on 112 plane. Available for 3D elements only.
           * - BC4H
             - 1,2,3,4,5,6
             - Second set of six components of BCC hardness on 112 plane. Available for 3D elements only.
           * - BC5H
             - 1,2,3,4,5,6
             - First set of six components of BCC hardness on 123 plane. Available for 3D elements only.
           * - BC6H
             - 1,2,3,4,5,6
             - Second set of six components of BCC hardness on 123 plane. Available for 3D elements only.
           * - BC7H
             - 1,2,3,4,5,6
             - Third set of six components of BCC hardness on 123 plane. Available for 3D elements only.
           * - BC8H
             - 1,2,3,4,5,6
             - Fourth set of six components of BCC hardness on 123 plane. Available for 3D elements only.
           * - XELG
             - 1,2,3,45,6,EQV
             - Crystal Lagrangian strain in 11, 22, 33, 12, 23,13 directions and its equivalent. Available for 3D elements only.
           * - SINT
             - RHO, ETA, SSTR, GRAIN
             - Sintering relative density, viscosity, sintering stress, and average grain size values.
           * - **Sequence Number Method**
           * - **Item**
             - **Comp**
             - **Description**
           * - SMISC
             - ``snum``
             - Summable items.
           * - NMISC
             - ``snum``
             - Nonsummable items.
           * - LS
             - ``snum``
             - Line element elastic stresses.
           * - LEPEL
             - ``snum``
             - Line element strains.
           * - LEPTH
             - ``snum``
             - Line element thermal strains.
           * - LEPPL
             - ``snum``
             - Line element plastic strains.
           * - LEPCR
             - ``snum``
             - Line element creep strains.
           * - LBFE
             - ``snum``
             - Line element temperatures.


        .. _ESOL_tab_2:

        ESOL - Selected Result Component Labels
        ***************************************

        .. flat-table::
           :header-rows: 1

           * - Comp
             - Description
           * - SVAR ``n``
             - The ``n`` th state variable.
           * - FLDUF0 ``n``
             - The ``n`` th user-defined field variable.
        """
        command = f"ESOL,{nvar},{elem},{node},{item},{comp},{name}"
        return self.run(command, **kwargs)

    def gssol(
        self, nvar: str = "", item: str = "", comp: str = "", name: str = "", **kwargs
    ):
        r"""Specifies which results to store from the results file when using generalized plane strain.

        Mechanical APDL Command: `GSSOL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_GSSOL.html>`_

        Parameters
        ----------
        nvar : str
            Arbitrary reference number or name assigned to this variable. Variable numbers can be 2 to
            ``NV`` ( :ref:`numvar` ) while the name can be an eight byte character string. Overwrites any
            existing results for this variable.

        item : str
            Label identifying item to be stored.

            * ``LENGTH`` - Change of fiber length at the ending point.

            * ``ROT`` - Rotation of the ending plane during deformation.

            * ``F`` - Reaction force at the ending point in the fiber direction.

            * ``M`` - Reaction moment applied on the ending plane.

        comp : str
            Component of the item, if Item = ROT or M.

            * ``X`` - The rotation angle or reaction moment of the ending plane about X.

            * ``Y`` - The rotation angle or reaction moment of the ending plane about Y.

        name : str
            Thirty-two character name identifying the item on the printout and display. Defaults to the
            label formed by concatenating the first four characters of the ``Item`` and ``Comp`` labels.

        Notes
        -----

        .. _GSSOL_notes:

        This command stores the results (new position of the ending plane after deformation) for generalized
        plane strain. All outputs are in the global Cartesian coordinate system. For more information about
        the generalized plane strain feature, see Generalized Plane Strain Option of Current-Technology
        Solid Elements in the  `Element Reference
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_BIBLIO.html>`_.
        """
        command = f"GSSOL,{nvar},{item},{comp},{name}"
        return self.run(command, **kwargs)

    def jsol(
        self,
        nvar: str = "",
        elem: str = "",
        item: str = "",
        comp: str = "",
        name: str = "",
        **kwargs,
    ):
        r"""Specifies result items to be stored for the joint element.

        Mechanical APDL Command: `JSOL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_JSOL.html>`_

        Parameters
        ----------
        nvar : str
            Arbitrary reference number or name assigned to this variable. Variable numbers can be 2 to
            ``NV`` ( :ref:`numvar` ) while the name can be an eight-byte character string. Overwrites any
            existing results for this variable.

        elem : str
            Element number for which to store results.

        item : str
            Label identifying the item. Valid item labels are shown in :ref:`jsol_tab_1` below.

        comp : str
            Component of the ``Item`` (if required). Valid component labels are shown in :ref:`jsol_tab_1`
            below.

        name : str
            Thirty-two character name identifying the item on printouts and displays. Defaults to a label
            formed by concatenating the first four characters of the ``Item`` and ``Comp`` labels.

        Notes
        -----

        .. _JSOL_notes:

        This command is valid for the ``MPC184`` joint elements. The values stored are for the free or
        unconstrained degrees of freedom of a joint element. Relative reaction forces and moments are
        available only if stiffness, damping, or friction is associated with the joint element.
        .. _jsol_tab_1:

        JSOL - Valid Item and Component Labels
        **************************************

        .. flat-table::
           :header-rows: 1

           * - Item
             - Comp
             - Description
           * - U
             - X, Y, Z
             - x, y, or z relative displacement.
           * - ROT
             - X, Y, Z
             - x, y, or z relative rotation.
           * - VEL
             - X, Y, Z
             - x, y, or z relative linear velocity.
           * - OMG
             - X, Y, Z
             - x, y, or z relative angular velocity.
           * - ACC
             - X, Y, Z
             - x, y, or z relative linear acceleration.
           * - DMG
             - X, Y, Z
             - x, y, or z relative angular acceleration.
           * - RF
             - X, Y, Z
             - Relative reaction forces in the local x, y, or z direction.
           * - RM
             - X, Y, Z
             - Relative reaction moments in the local x, y, or z direction.
        """
        command = f"JSOL,{nvar},{elem},{item},{comp},{name}"
        return self.run(command, **kwargs)

    def nsol(
        self,
        nvar: str = "",
        node: str = "",
        item: str = "",
        comp: str = "",
        name: str = "",
        sector: str = "",
        **kwargs,
    ):
        r"""Specifies nodal data to be stored from the results file.

        Mechanical APDL Command: `NSOL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_NSOL.html>`_

        Parameters
        ----------
        nvar : str
            Arbitrary reference number assigned to this variable. Variable numbers can be 2 to ``NV`` (
            :ref:`numvar` ). Overwrites any existing results for this variable.

        node : str
            Node for which data are to be stored.

        item : str
            Label identifying the item. Valid item labels are shown in the table below. Some items also
            require a component label.

        comp : str
            Component of the item (if required). Valid component labels are shown in the table below.

        name : str
            Thirty-two character name identifying the item on printouts and displays. Defaults to a label
            formed by concatenating the first four characters of the ``Item`` and ``Comp`` labels.

        sector : str
            For a full harmonic cyclic symmetry solution, the sector number for which the results from NODE
            are to be stored.

        Notes
        -----

        .. _NSOL_notes:

        Stores nodal degree of freedom and solution results in a variable. For more information, see Data
        Interpreted in the Nodal Coordinate System in the `Modeling and Meshing Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD14.html>`_.

        For ``SECTOR`` >1, the result is in the nodal coordinate system of the base sector, and it is
        rotated to the expanded sector``s location. Refer to `Using the /CYCEXPAND Command
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cycsym/advcycpost.html#>`_

        .. _nsol_tab_1:

        NSOL - Valid Item and Component Labels
        **************************************

        .. flat-table:: Valid Item and Component Labels :ref:`nsol`, ``NVAR,NODE,Item,Comp,Name``
           :header-rows: 2

           * - Valid item and component labels for nodal degree of freedom results are:
           * - Item
             - Comp
             - Description
           * - U
             - X, Y, Z
             - X, Y, or Z structural displacement.
           * - ROT
             - X, Y, Z
             - X, Y, or Z structural rotation.
           * - TEMP[ :ref:`NSOL_temp` ]
             -
             - Temperature.
           * - PRES
             -
             - Pressure.
           * - GFV1, GFV2, GFV3
             -
             - Nonlocal field values 1, 2, and 3.
           * - VOLT
             -
             - Electric potential.
           * - MAG
             -
             - Magnetic scalar potential.
           * - V
             - X, Y, Z
             - X, Y, or Z fluid velocity in a fluid analysis.
           * - A
             - X, Y, Z
             - X, Y, or Z magnetic vector potential in an electromagnetic analysis.
           * - CONC
             -
             - Concentration.
           * - VEL
             - X, Y, Z
             - X, Y, or Z velocity in a structural transient dynamic analysis ( :ref:`antype`,TRANS).
           * - ACC
             - X, Y, Z
             - X, Y, or Z acceleration in a structural transient dynamic analysis ( :ref:`antype`,TRANS).
           * - OMG
             - X, Y, Z
             - X, Y, or Z rotational velocity in a structural transient dynamic analysis ( :ref:`antype`,TRANS).
           * - DMG
             - X, Y, Z
             - X, Y, or Z rotational acceleration in a structural transient dynamic analysis ( :ref:`antype`,TRANS).
           * - CURR
             -
             - Current.
           * - EMF
             -
             - Electromotive force drop.
           * - SPL
             -
             - Sound pressure level.
           * - SPLA
             -
             - A-weighted sound pressure level (dBA).
           * - ENKE
             -
             - Acoustic energy density

        .. _NSOL_temp:

        For ``SHELL131`` and ``SHELL132`` elements with KEYOPT(3) = 0 or 1, use the labels TBOT, TE2, TE3,.
        .., TTOP instead of TEMP.
        """
        command = f"NSOL,{nvar},{node},{item},{comp},{name},{sector}"
        return self.run(command, **kwargs)

    def nstore(self, tinc: str = "", **kwargs):
        r"""Defines which time points are to be stored.

        Mechanical APDL Command: `NSTORE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_NSTORE.html>`_

        Parameters
        ----------
        tinc : str
            Store data associated with every ``TINC`` time (or frequency) point(s), within the previously
            defined range of ``TMIN`` to ``TMAX`` ( :ref:`timerange` ). (Defaults to 1)

        Notes
        -----

        .. _NSTORE_notes:

        Defines which time (or frequency) points within the range are to be stored.
        """
        command = f"NSTORE,{tinc}"
        return self.run(command, **kwargs)

    def numvar(self, nv: str = "", **kwargs):
        r"""Specifies the number of variables allowed in POST26.

        Mechanical APDL Command: `NUMVAR <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_NUMVAR.html>`_

        Parameters
        ----------
        nv : str
            Allow storage for ``NV`` variables. 200 maximum are allowed. Defaults to 10. TIME (variable 1)
            should also be included in this number.

        Notes
        -----

        .. _NUMVAR_notes:

        Specifies the number of variables allowed for data read from the results file and for data resulting
        from an operation (if any). For efficiency, ``NV`` should not be larger than necessary. ``NV``
        cannot be changed after data storage begins.
        """
        command = f"NUMVAR,{nv}"
        return self.run(command, **kwargs)

    def rforce(
        self,
        nvar: str = "",
        node: str = "",
        item: str = "",
        comp: str = "",
        name: str = "",
        **kwargs,
    ):
        r"""Specifies the total reaction force data to be stored.

        Mechanical APDL Command: `RFORCE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_RFORCE.html>`_

        Parameters
        ----------
        nvar : str
            Arbitrary reference number assigned to this variable (2 to NV ( :ref:`numvar` )). Overwrites any
            existing results for this variable.

        node : str
            Node for which data are to be stored. If ``NODE`` = P, graphical picking is enabled (valid only
            in the GUI).

        item : str
            Label identifying the item. Valid item labels are shown in the table below. Some items also
            require a component label.

        comp : str
            Component of the item (if required). Valid component labels are shown in the table below.

        name : str
            Thirty-two character name identifying the item on printouts and displays. Defaults to an eight
            character label formed by concatenating the first four characters of the ``Item`` and ``Comp``
            labels.

        Notes
        -----

        .. _RFORCE_notes:

        Defines the total reaction force data (static, damping, and inertial components) to be stored from
        single pass ( :ref:`antype`,STATIC or TRANS) solutions or from the expansion pass of mode-
        superposition ( :ref:`antype`,HARMIC or TRANS) solutions.

        .. _rforce_tab_1:

        RFORCE - Valid Item and Component Labels
        ****************************************

        .. flat-table:: Valid item and component labels for node results are:
           :header-rows: 1

           * - Item
             - Comp
             - Description
           * - F
             - X,Y,Z
             - X, Y, or Z structural force
           * - M
             - X,Y,Z
             - X, Y, or Z structural moment
           * - HEAT[ :ref:`rforce_table1_note1` ]
             -
             - Heat flow
           * - FLOW
             -
             - Fluid flow
           * - AMPS
             -
             - Current flow
           * - FLUX
             -
             - Magnetic flux
           * - CSG
             - X,Y,Z
             - X, Y, or Z magnetic current segment component
           * - RATE
             -
             - Diffusion flow rate
           * - VLTG
             -
             - Voltage drop
           * - CURT
             -
             - Current
           * - CHRG
             -
             - Charge

        .. _rforce_table1_note1:

        For ``SHELL131`` and ``SHELL132`` elements with KEYOPT(3) = 0 or 1, use the labels HBOT, HE2, HE3,.
        .., HTOP instead of HEAT.
        """
        command = f"RFORCE,{nvar},{node},{item},{comp},{name}"
        return self.run(command, **kwargs)

    def rgb(
        self,
        kywrd: str = "",
        pred: str = "",
        pgrn: str = "",
        pblu: str = "",
        n1: str = "",
        n2: str = "",
        ninc: str = "",
        ncntr: str = "",
        **kwargs,
    ):
        r"""Specifies the RGB color values for indices and contours.

        Mechanical APDL Command: `/RGB <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_RGB.html>`_

        Parameters
        ----------
        kywrd : str
            Determines how RGB modifications will be applied.

            * ``INDEX`` - Specifies that subsequent color values apply to Mechanical APDL color indices (0-15).

            * ``CNTR`` - Specifies that subsequent color values apply to contours (1-128). Applies to C-option
              devices only (i.e. X11C or Win32C).

        pred : str
            Intensity of the color red, expressed as a percentage.

        pgrn : str
            Intensity of the color green, expressed as a percentage.

        pblu : str
            Intensity of the color blue, expressed as a percentage.

        n1 : str
            First index (0-15), or contour (1-128) to which the designated RGB values apply.

        n2 : str
            Final index (0-15), or contour (1-128) to which the designated RGB values apply.

        ninc : str
            The step increment between the values ``N1`` and ``N2`` determining which contours or indices
            will be controlled by the specified RGB values.

        ncntr : str
            The new maximum number of contours (1-128).

        Notes
        -----

        .. _s-RGB_notes:

        Issuing the :ref:`cmap` command (with no filename) will restore the default color settings.
        """
        command = f"/RGB,{kywrd},{pred},{pgrn},{pblu},{n1},{n2},{ninc},{ncntr}"
        return self.run(command, **kwargs)

    def solu(
        self, nvar: str = "", item: str = "", comp: str = "", name: str = "", **kwargs
    ):
        r"""Specifies solution summary data per substep to be stored.

        Mechanical APDL Command: `SOLU <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SOLU.html>`_

        Parameters
        ----------
        nvar : str
            Arbitrary reference number assigned to this variable (2 to ``NV`` ( :ref:`numvar` )).

        item : str
            Label identifying the item. Valid item labels are shown in the table below. Some items may also
            require a component label.

        comp : str
            Component of the item (if required). Valid component labels are shown in the table below. None
            are currently required.

        name : str
            Thirty-two character name identifying the item on printouts and displays. Defaults to an eight
            character label formed by concatenating the first four characters of the ``Item`` and ``Comp``
            labels.

        Notes
        -----

        .. _SOLU_notes:

        See also the :ref:`priter` command of POST1 to display some of these items directly. Valid for a
        static or full transient analysis. All other analyses have zeros for the data. Valid item and
        component labels for solution summary values are:

        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.
        """
        command = f"SOLU,{nvar},{item},{comp},{name}"
        return self.run(command, **kwargs)

    def store(
        self,
        lab: str = "",
        npts: str = "",
        freq: str = "",
        toler: str = "",
        cluster: str = "",
        **kwargs,
    ):
        r"""Stores data in the database for the defined variables.

        Mechanical APDL Command: `STORE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_STORE.html>`_

        Parameters
        ----------
        lab : str
            Valid labels:

            * ``MERGE`` - Merge data from results file for the time points in memory with the existing data
              using current specifications (default).

            * ``NEW`` - Store a new set of data, replacing any previously stored data with current result file
              specifications and deleting any previously-calculated variables (see ).

              Variables defined using the :ref:`ansol` command are also deleted if they represent element-based
              results. Variables created using `nodal-averaged results
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_CH2_2.html#nodeavepost>`_ are
              not deleted.

            * ``APPEN`` - Append data from results file to the existing data.

            * ``ALLOC`` - Allocate (and zero) space for ``NPTS`` data points.

            * ``PSD`` - Create a new set of frequency points for PSD calculations (replacing any previously
              stored data and erasing any previously calculated data).

        npts : str
            The number of time points (or frequency points) for storage (used only with ``Lab`` = ALLOC or
            PSD). The value may be input when using POST26 with data supplied from other than a results
            file. This value is automatically determined from the results file data with the NEW, APPEN, and
            MERGE options. For the PSD option, ``NPTS`` determines the resolution of the frequency vector
            (valid numbers are between 1 and 10, defaults to 5).

        freq : str
            A frequency value, or an array containing frequency values (Hz). Use :ref:`dim` to define the
            array and enclose the array name in percent signs (for example, :ref:`store`,,,,``arrayname``).
            A default value of 1% of damping is considered for clustering around the user-input frequency
            values. Supported for ``Lab`` = PSD only.

        toler : str
            Tolerance to determine if a user-input frequency value ( ``FREQ`` ) is a duplicate and can be
            ignored. Two frequency values are considered duplicates if their difference is smaller than the
            frequency range multiplied by the tolerance. The default value is 10 :sup:`-5`. Supported for
            ``Lab`` = PSD and ``Cluster`` = YES only.

        cluster : str
            Key to control whether or not to consider the clustering frequencies around each of the user-input
            array values. Available only when a user-defined frequency array is used ( ``FREQ`` ).

            * ``YES`` - Merge the clustering frequencies around both the natural frequencies and the frequency
              values entered in the user-defined array ( ``FREQ`` ) (default).

            * ``NO`` - Do not include clustering frequencies, and use only natural frequencies and the
              frequencies in the user-defined array ( ``FREQ`` ).

        Notes
        -----

        .. _STORE_notes:

        This command stores data from the results file in the database for the defined variables (
        :ref:`ansol`, :ref:`nsol`, :ref:`esol`, :ref:`solu`, :ref:`jsol` ) per specification (
        :ref:`avprin`, :ref:`force`, :ref:`layerp26`, :ref:`shell` ). See `Storing the Variable
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/Hlp_G_BASP26define.html#>`_

        The :ref:`store`,PSD command creates a new frequency vector (variable 1) for response PSD
        calculations ( :ref:`rpsd` ). This command should first be issued before defining variables (
        :ref:`nsol`, :ref:`esol`, :ref:`rforce` ) for which response PSD's are to be calculated.

        If the frequencies in the user-defined array are relevant, turning off clustering ( ``Cluster`` =
        NO) reduces calculation costs without significant loss of accuracy. You can check the frequencies by
        initially issuing a default :ref:`rpsd` (with clustering) to obtain a reference plot of the
        response.
        """
        command = f"STORE,{lab},{npts},,{freq},{toler},{cluster}"
        return self.run(command, **kwargs)

    def timerange(self, tmin: str = "", tmax: str = "", **kwargs):
        r"""Specifies the time range for which data are to be stored.

        Mechanical APDL Command: `TIMERANGE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_TIMERANGE.html>`_

        Parameters
        ----------
        tmin : str
            Minimum time (defaults to first time (or frequency) point on the file).

        tmax : str
            Maximum time (defaults to last time (or frequency) point on the file).

        Notes
        -----

        .. _TIMERANGE_notes:

        Defines the time (or frequency) range for which data are to be read from the file and stored in
        memory. Use the :ref:`nstore` command to define the time increment.

        Use :ref:`prtime` or :ref:`pltime` to specify the time (frequency) range for cyclic mode-
        superposition harmonic analyses.
        """
        command = f"TIMERANGE,{tmin},{tmax}"
        return self.run(command, **kwargs)

    def vardel(self, nvar: str = "", **kwargs):
        r"""Deletes a variable (GUI).

        Mechanical APDL Command: `VARDEL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_VARDEL.html>`_

        Parameters
        ----------
        nvar : str
            The reference number of the variable to be deleted. ``NVAR`` is as defined by :ref:`nsol`,
            :ref:`esol`, etc.

        Notes
        -----

        .. _VARDEL_notes:

        Deletes a POST26 solution results variable. This command is generated by the Graphical User
        Interface (GUI). It appears in the log file ( :file:`Jobname.LOG` ) if a POST26 variable is deleted
        from the Defined Time-History Variables dialog box.

        The command is not intended to be typed in directly in a Mechanical APDL session (although it can be
        included in an input file for batch input or for use with :ref:`input` ).
        """
        command = f"VARDEL,{nvar}"
        return self.run(command, **kwargs)

    def varnam(self, ir: str = "", name: str = "", **kwargs):
        r"""Names (or renames) a variable.

        Mechanical APDL Command: `VARNAM <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_VARNAM.html>`_

        Parameters
        ----------
        ir : str
            Reference number of the variable (2 to NV ( :ref:`numvar` )).

        name : str
            Thirty-two character name for identifying variable on printouts and displays. Embedded blanks
            are compressed for output.
        """
        command = f"VARNAM,{ir},{name}"
        return self.run(command, **kwargs)
