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


class ElementTable:

    def esort(
        self,
        item: str = "",
        lab: str = "",
        order: int | str = "",
        kabs: int | str = "",
        numb: str = "",
        **kwargs,
    ):
        r"""Sorts the element table.

        Mechanical APDL Command: `ESORT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ESORT.html>`_

        **Command default:**

        .. _ESORT_default:

        Use ascending element number order.

        Parameters
        ----------
        item : str
            Label identifying the item:

            * ``ETAB`` - (currently the only ``Item`` available)

        lab : str
            element table label:

            * ``Lab`` - Any user-defined label from the :ref:`etable` command (input in the ``Lab`` field of the
              :ref:`etable` command).

        order : int or str
            Order of sort operation:

            * ``0`` - Sort into descending order.

            * ``1`` - Sort into ascending order.

        kabs : int or str
            Absolute value key:

            * ``0`` - Sort according to real value.

            * ``1`` - Sort according to absolute value.

        numb : str
            Number of elements (element table rows) to be sorted in ascending or descending order (
            ``ORDER`` ) before sort is stopped (remainder will be in unsorted sequence) (defaults to all
            elements).

        Notes
        -----

        .. _ESORT_notes:

        The element table rows are sorted based on the column containing the ``Lab`` values. Use
        :ref:`eusort` to restore the original order. If :ref:`esort` is specified with PowerGraphics on (
        :ref:`graphics`,POWER), then the nodal solution results listing ( :ref:`prnsol` ) will be the same
        as with the full graphics mode ( :ref:`graphics`,FULL).
        """
        command = f"ESORT,{item},{lab},{order},{kabs},{numb}"
        return self.run(command, **kwargs)

    def etable(
        self, lab: str = "", item: str = "", comp: str = "", option: str = "", **kwargs
    ):
        r"""Fills a table of element values for further processing.

        Mechanical APDL Command: `ETABLE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ETABLE.html>`_

        Parameters
        ----------
        lab : str
            Any unique user-defined label for use in subsequent commands and output headings. A valid label has
            a maximum of eight characters and is not a general predefined ``Item`` label. Default: An eight-
            character label formed by concatenating the first four characters of the ``Item`` and ``Comp``
            labels.

            If the same as a previous user label, the result item is included under the same label. Up to 200
            different labels can be defined.

            The following predefined labels are reserved:

            * ``REFL`` - Refills all tables previously defined with the :ref:`etable` commands (not the
              :ref:`calc` module commands) according to the latest :ref:`etable` specifications. It is convenient
              for refilling tables after the load step ( :ref:`set` ) has changed. Remaining fields are ignored.

            * ``STAT`` - Displays stored table values.

            * ``ERAS`` - Erases the entire table.

        item : str
            Label identifying the item. General item labels are shown in the tables below. Some items also
            require a component label. Character parameters are valid. ``Item`` = ERAS erases a ``Lab``
            column.

        comp : str
            Component of the item (if required). General component labels are shown in the tables below.
            Character parameters can be used.

        option : str
            Option for storing element table data:

            * ``MIN`` - Store minimum element nodal value of the specified item component.

            * ``MAX`` - Store maximum element nodal value of the specified item component.

            * ``AVG`` - Store averaged element centroid value of the specified item component (default).

        Notes
        -----

        .. _ETABLE_notes:

        :ref:`etable` defines a table of values per element (the element table) for use in further
        processing. The element table is organized similar to a spreadsheet, with rows representing all
        selected elements and columns consisting of result items which have been moved into the table (
        ``Item``, ``Comp`` ) via :ref:`etable`. Each column of data is identified by a user-defined label (
        ``Lab`` ) for listings and displays.

        After entering the data into the element table, you are not limited to listing or displaying your
        data ( :ref:`plesol`, :ref:`presol`, etc.). You can also perform many types of operations on your
        data, such as adding or multiplying columns ( :ref:`sadd`, :ref:`smult` ), defining allowable
        stresses for safety calculations ( :ref:`sallow` ), or multiplying one column by another (
        :ref:`smult` ). For more information, see `Getting Started
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/afbRsqe0ldm.html>`_

        For `reinforcing
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/str_compreinfdirectemb.html>`_
        elements, this command displays the results of reinforcing member (individual reinforcing) selected
        via the :ref:`layer`, ``N`` command (where ``N`` is a given reinforcing member). :ref:`layer`,0
        (default) or :ref:`layer`,1 selects the first reinforcing member.

        Various results data can be stored in the element table. For example, many items for an element are
        inherently single-valued (one value per element). The single-valued items include: SERR, SDSG, TERR,
        TDSG, SENE, TENE, KENE, ASENE, PSENE, AKENE, PKENE, DENE, WEXT, AENE, JHEAT, JS, VOLU, and CENT. All
        other items are multivalued (varying over the element, such that there is a different value at each
        node). Because only one value is stored in the element table per element, an average value (based on
        the number of contributing nodes) is calculated for multivalued items. Exceptions to this averaging
        procedure are FMAG and all element force items, which represent the sum only of the contributing
        nodal values.

        Two methods of data access can be used with the :ref:`etable` command. The method you select depends
        upon the type of data that you want to store. Some results can be accessed via a generic label
        (Component Name method), while others require a label and number (Sequence Number method).

        The component name method is used to access the general element data (that is, element data which is
        generally available to most element types or groups of element types). All of the single-valued
        items and some of the more general multivalued items are accessible with the Component Name method.
        Various element results depend on the calculation method and the selected results location (
        :ref:`avprin`, :ref:`rsys`, :ref:`layer`, :ref:`shell`, and :ref:`esel` ).

        Although nodal data is readily available for listing and display ( :ref:`prnsol`, :ref:`plnsol` )
        without using the element table, you can also use the Component Name method to enter these results
        into the element table for further "worksheet" manipulation. (See `Getting Started
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/afbRsqe0ldm.html>`_  ``Item`` and
        ``Comp`` labels for the component name method is shown in :ref:`ETABLE_tab_1`. See
        :ref:`ETABLE_tab_2` for a list of selected result ( ``Item`` = SRES) ``Comp`` labels.

        The sequence number method enables you to view results for data that is not averaged (such as
        pressures at nodes, temperatures at integration points, etc.), or data that is not easily described
        in a generic fashion (such as all derived data for structural line elements and contact elements,
        all derived data for thermal line elements, layer data for layered elements, etc.). A table
        illustrating the ``Items`` (such as LS, LEPEL, LEPTH, SMISC, NMISC, SURF, etc.) and corresponding
        sequence numbers for each element is shown in the Output Data section of each element description.

        Some element table data are reported in the results coordinate system. These include all component
        results (for example, UX, UY, etc.; SX, SY, etc.). The solution writes component results in the
        database and on the results file in the solution coordinate system. When you issue the :ref:`etable`
        command, these results are then transformed into the results coordinate system ( :ref:`rsys` )
        before being stored in the element table. The default results coordinate system is global Cartesian
        ( :ref:`rsys`,0). All other data are retrieved from the database and stored in the element table
        with no coordinate transformation.

        To display the stored table values, issue the :ref:`pretab`, :ref:`pletab`, or :ref:`etable`,STAT
        command. To erase the entire table, issue :ref:`etable`,ERAS. To erase a ``Lab`` column, issue
        :ref:`etable`, ``Lab``,ERAS.

        When the GUI is enabled, if a **Delete** operation in a Define Element Table Data dialog box writes
        this command to a log file ( :file:`Jobname.LOG` or :file:`Jobname.LGW` ), the program sets ``Lab``
        = blank, ``Item`` = ERASE, and ``Comp`` = an integer number. In this case, the program has assigned
        a value of ``Comp`` that corresponds to the location of a chosen variable name in the dialog list.
        It is not intended that you type in such a location value for ``Comp`` in a session; however, a file
        that contains a GUI-generated :ref:`etable` command of this form can be used for batch input or the
        :ref:`input` command.

        The MIN and MAX options are not available for thermal elements.

        The element table data option ( ``Option`` ) is not available for all output items. See the table
        below for supported items.

        .. _ETABLE_tab_1:

        ETABLE - General Result Item and Component Labels
        *************************************************

        .. flat-table:: General Item and Component Labels :ref:`etable`, ``Lab, Item, Comp``
           :header-rows: 1

           * - Item
             - Comp
             - Description
           * - Valid Item Labels for Degree of Freedom Results
           * - U
             - X, Y, Z
             - X, Y, or Z structural displacement.
           * - ROT
             - X, Y, Z
             - X, Y, or Z structural rotation.
           * - TEMP For ``SHELL131`` and ``SHELL132`` elements with KEYOPT(3) = 0 or 1, use labels TBOT, TE2, TE3, ..., TTOP instead of TEMP.
             -
             - Temperature.
           * - PRES
             -
             - Pressure.
           * - VOLT
             -
             - Electric potential.
           * - GFV1, GFV2, GFV3
             -
             - Nonlocal field values 1, 2, and 3.
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
           * - CURR
             -
             - Current.
           * - EMF
             -
             - Electromotive force drop.
           * - Valid Item and Component Labels for Element Results
           * - :rspan:`3` S Element table option ( ``Option`` ) is available for this element output data item.
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
           * - :rspan:`3` EPDI
             - X, Y, Z, XY, YZ, XZ
             - Component diffusion strain.
           * - 1, 2, 3
             - Principal diffusion strain.
           * - EQV
             - Diffusion equivalent strain.
           * - INT
             - Diffusion strain intensity.
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
           * - 1, 2, 3
             - Principal creep strain.
           * - INT
             - Creep strain intensity.
           * - EQV
             - Creep equivalent strain.
           * - EPSW
             -
             - Swelling strain.
           * - :rspan:`3` EPTO
             - X, Y, Z, XY, YZ, XZ
             - Component total mechanical strain ( excluding thermal) (EPEL + EPPL + EPCR).
           * - 1, 2, 3
             - Principal total mechanical strain.
           * - INT
             - Total mechanical strain intensity.
           * - EQV
             - Total equivalent mechanical strain.
           * - :rspan:`3` EPTT
             - X, Y, Z, XY, YZ, XZ
             - Component total strain including thermal, diffusion, and swelling (EPEL + EPTH + EPPL + EPDI + EPCR + EPSW).
           * - 1, 2, 3
             - Principal total strain.
           * - INT
             - Total strain intensity.
           * - EQV
             - Total equivalent strain.
           * - :rspan:`3` NL
             - SEPL
             - Equivalent stress (from stress-strain curve).
           * - SRAT
             - Stress state ratio.
           * - HPRES
             - Hydrostatic pressure.
           * - EPEQ
             - Accumulated equivalent plastic strain.
           * - :rspan:`7` SEND
             - ELASTIC The results for this postprocessing SEND component are invalid for ``ELBOW290`` when that element is used with viscoelastic or viscohyperelastic materials.
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
           * - SVAR
             - 1 to MAX
             - State variable.
           * - :rspan:`1` CDM
             - DMG
             - Damage variable.
           * - LM
             - Maximum previous strain energy for virgin material.
           * - :rspan:`13` FAIL
             - MAX  For MPC-based contact definitions, the value of STAT can be negative. This indicates that one or more contact constraints were intentionally removed to prevent overconstraint. STAT = -3 is used for MPC bonded contact; STAT = -2 is used for MPC no-separation contact.
             - Maximum of all active failure criteria defined at the current location ( :ref:`fctyp` ).
           * - EMAX
             - Maximum Strain Failure Criterion.
           * - SMAX
             - Maximum Stress Failure Criterion.
           * - TWSI
             - Tsai-Wu Strength Index Failure Criterion.
           * - TWSR
             - Inverse of Tsai-Wu Strength Ratio Index Failure Criterion.
           * - HFIB   Some element- and material-type limitations apply. For more information, see :ref:`prerr`.
             - Hashin Fiber Failure Criterion.
           * - HMAT
             - Hashin Matrix Failure Criterion.
           * - PFIB
             - Puck Fiber Failure Criterion.
           * - PMAT
             - Puck Matrix Failure Criterion.
           * - L3FB
             - LaRc03 Fiber Failure Criterion.
           * - L3MT
             - LaRc03 Matrix Failure Criterion.
           * - L4FB
             - LaRc04 Fiber Failure Criterion.
           * - L4MT
             - LaRc04 Matrix Failure Criterion.
           * - USR1, USR2,..., USR9    When using the :ref:`emft` procedure to calculate electromagnetic force ( ``PLANE121``, ``SOLID122``, ``SOLID123``, ``PLANE233``, ``SOLID236`` or ``SOLID237`` elements only), the FMAG sum will be zero or near zero.
             - User-defined failure criteria.
           * - :rspan:`4` PFC
             - MAX Failure criteria are based on the effective stresses in the damaged material.
             - Maximum of all failure criteria defined at current location.
           * - FT
             - Fiber tensile failure criteria.
           * - FC
             - Fiber compressive failure criteria.
           * - MT
             - Matrix tensile failure criteria.
           * - MC
             - Matrix compressive failure criteria.
           * - :rspan:`7` PDMG
             - STAT
             - Damage status (0 = undamaged, 1 = damaged, 2 = completely damaged).
           * - FT
             - Fiber tensile damage variable.
           * - FC
             - Fiber compressive damage variable.
           * - MT
             - Matrix tensile damage variable.
           * - MC
             - Matrix compressive damage variable.
           * - S
             - Shear damage variable (S).
           * - SED
             - Energy dissipated per unit volume.
           * - SEDV
             - Energy per unit volume due to viscous damping.
           * - :rspan:`2` FCMX
             - LAY
             - Layer number where the maximum of all active failure criteria over the entire element occurs.
           * - FC
             - Number of the maximum-failure criterion over the entire element:   * 1 - EMAX * 2 - SMAX * 3 - TWSI * 4 - TWSR * 5 - PFIB * 6 - PMAT * 7 - HFIB * 8 - HMAT * 9 - L3FB * 10 - L3MT * 11 - L4FB * 12 - L4MT * 13~21 - USR1~USR9
           * - VAL
             - Value of the maximum failure criterion over the entire element.
           * - TG ``Comp`` = SUM is not supported for coupled pore-pressure-thermal (CPT ``nnn`` ) elements.
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
           * - SERR
             -
             - Structural error energy.
           * - SDSG
             -
             - Absolute value of maximum variation of any nodal stress component.
           * - TERR
             -
             - Thermal error energy.
           * - TDSG
             -
             - Absolute value of the maximum variation of any nodal thermal gradient component.
           * - F
             - X, Y, Z
             - Component structural force. Sum of element nodal values.
           * - M
             - X, Y, Z
             - Component structural moment. Sum of element nodal values.
           * - HEAT
             -
             - Heat flow. Sum of element nodal values.
           * - FLOW
             -
             - Fluid flow. Sum of element nodal values.
           * - AMPS
             -
             - Current flow. Sum of element nodal values.
           * - FLUX
             -
             - Magnetic flux. Sum of element nodal values.
           * - CSG
             - X, Y, Z
             - Component magnetic current segment.
           * - RATE
             -
             - Diffusion flow rate. Sum of element nodal values.
           * - SENE
             -
             - "Stiffness" energy or thermal heat dissipation (applies to all elements where meaningful). Same as TENE.
           * - AENE
             -
             - Artificial energy of the element. This includes the sum of hourglass control energy and energy generated by in-plane drilling stiffness from shell elements (applies to all elements where meaningful). It also includes artificial energy due to contact stabilization. The energy is used for comparisons to SENE energy to predict the solution error due to artificial stiffness.
           * - TENE
             -
             - Thermal heat dissipation or "stiffness" energy (applies to all elements where meaningful). Same as SENE.
           * - KENE
             -
             - Kinetic energy (applies to all elements where meaningful).
           * - ASENE
             -
             - Amplitude "stiffness" energy.
           * - PSENE
             -
             - Peak "stiffness" energy.
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
           * - STEN
             -
             - Elemental energy dissipation due to `stabilization <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STRUNST.html#>`_.
           * - JHEAT
             -
             - Element Joule heat generation.
           * - JS
             - X, Y, Z, SUM
             - Source current density for low-frequency magnetic analyses. Total current density (sum of conduction and displacement current densities) in low frequency electric analyses. Components (X, Y, Z) and vector sum (SUM).
           * - JT
             - X, Y, Z, SUM
             - Total measurable current density in low-frequency electromagnetic analyses. (Conduction current density in a low-frequency electric analysis.) Components (X, Y, Z) and vector sum (SUM).
           * - JC
             - X, Y, Z, SUM
             - Conduction current density for elements that support conduction current calculation. Components (X, Y, Z) and vector sum (SUM).
           * - MRE
             -
             - Magnetics Reynolds number.
           * - VOLU
             -
             - Element volume. Based on unit thickness for 2D plane elements (unless the thickness option is used) and on the full 360 degrees for 2D axisymmetric elements.
           * - CENT
             - X, Y, Z
             - Undeformed X, Y, or Z location (based on shape function) of the element centroid in the active coordinate system.
           * - BFE
             - TEMP
             - Body temperatures (calculated from applied temperatures) as used in solution (area and volume elements only).
           * - SMISC
             - snum
             - Element summable miscellaneous data value at sequence number snum (shown in the Output Data section of each applicable element description).
           * - NMISC
             - snum
             - Element non-summable miscellaneous data value at sequence number snum (shown in the Output Data section of each applicable element description).
           * - SURF
             - snum
             - Element surface data value at sequence number snum.
           * - :rspan:`9` CONT
             - STAT
             - Contact status:   * 3 = closed and sticking * 2 = closed and sliding * 1 = open but near contact * 0 = open and not near contact
           * - PENE
             - Contact penetration (zero or positive).
           * - PRES
             - Contact pressure.
           * - SFRIC
             - Contact friction stress.
           * - STOT
             - Contact total stress (pressure plus friction).
           * - SLIDE
             - Contact sliding distance.
           * - GAP
             - Contact gap distance (0 or negative).
           * - FLUX
             - Total heat flux at contact surface.
           * - CNOS
             - Total number of contact status changes during substep.
           * - FPRS
             - Fluid penetration pressure.
           * - TOPO
             -
             - Densities used for topological optimization.
           * - CAP
             - C0,X0,K0,ZONE, DPLS,VPLS
             - Material cap plasticity model only: Cohesion; hydrostatic compaction yielding stress; I1 at the transition point at which the shear and compaction envelopes intersect; zone = 0: elastic state, zone = 1: compaction zone, zone = 2: shear zone, zone = 3: expansion zone; effective deviatoric plastic strain; volume plastic strain.
           * - EDPC
             - CSIG,CSTR
             - Material EDP creep model only (not including the cap model): Equivalent creep stress; equivalent creep strain.
           * - :rspan:`3` ESIG
             - X,Y,Z,XY,YZ,ZX
             - Components of Biot``s effective stress.
           * - 1, 2, 3
             - Principal stresses of Biot``s effective stress.
           * - INT
             - Stress intensity of Biot``s effective stress.
           * - EQV
             - Equivalent stress of Biot``s effective stress.
           * - :rspan:`2` DPAR
             - TPOR
             - Total porosity (Gurson material model).
           * - GPOR
             - Porosity due to void growth.
           * - NPOR
             - Porosity due to void nucleation.
           * - FFLX
             - X,Y,Z
             - Fluid flow flux in poromechanics.
           * - FGRA
             - X,Y,Z
             - Fluid pore pressure gradient in poromechanics.
           * - FICT
             - TEMP
             - Fictive temperature.
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
           * - BKS1,..., BKS5
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


        .. _ETABLE_tab_2:

        ETABLE - Selected Result Component Labels
        *****************************************

        Selected Result Component Labels :ref:`etable`, ``Lab``,SRES, ``Comp``

        .. flat-table::

           * - **Comp**
             - **Description**
           * - SVAR ``n``
             - The ``n`` th state variable.
           * - FLDUF0 ``n``
             - The ``n`` th user-defined field variable.
        """
        command = f"ETABLE,{lab},{item},{comp},{option}"
        return self.run(command, **kwargs)

    def eusort(self, **kwargs):
        r"""Restores original order of the element table.

        Mechanical APDL Command: `EUSORT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_EUSORT.html>`_

        Notes
        -----

        .. _EUSORT_notes:

        Changing the selected element set ( :ref:`esel` ) also restores the original element order.
        """
        command = "EUSORT"
        return self.run(command, **kwargs)

    def pletab(self, itlab: str = "", avglab: str = "", **kwargs):
        r"""Displays element table items.

        Mechanical APDL Command: `PLETAB <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PLETAB.html>`_

        Parameters
        ----------
        itlab : str
            User-defined label, as specified with the :ref:`etable` command, of item to be displayed.

        avglab : str
            Averaging operation:

            * ``NOAV`` - Do not average element items at common nodes (default).

            * ``AVG`` - Average the element items at common nodes.

        Notes
        -----

        .. _PLETAB_notes:

        Displays items stored in the table defined with the :ref:`etable` command for the selected elements.
        For display purposes, items are assumed to be constant over the element and assigned to each of its
        nodes. Contour display lines (lines of constant value) are determined by linear interpolation within
        each element from the nodal values. These nodal values have the option of being averaged (values are
        averaged at a node whenever two or more elements connect to the same node) or not averaged
        (discontinuous). The discontinuity between contour lines of adjacent elements is an indication of
        the gradient across elements.

        For `reinforcing
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/str_compreinfdirectemb.html>`_
        elements, this command displays the results of reinforcing member (individual reinforcing) selected
        via the :ref:`layer`, ``N`` command (where ``N`` is a given reinforcing member). :ref:`layer`,0
        (default) or :ref:`layer`,1 selects the first reinforcing member.

        Portions of this command are not supported by PowerGraphics ( :ref:`graphics`,POWER).
        """
        command = f"PLETAB,{itlab},{avglab}"
        return self.run(command, **kwargs)

    def plls(
        self,
        labi: str = "",
        labj: str = "",
        fact: str = "",
        kund: int | str = "",
        viewup: int | str = "",
        **kwargs,
    ):
        r"""Displays element table items as contoured areas along elements.

        Mechanical APDL Command: `PLLS <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PLLS.html>`_

        Parameters
        ----------
        labi : str
            Label of element table item ( :ref:`etable` ) for node I magnitude.

        labj : str
            Label of element table item for node J magnitude.

        fact : str
            Scale factor for display (defaults to 1). A negative scaling factor may be used to invert the
            display.

        kund : int or str
            Undisplaced shape key:

            * ``0`` - Display selected items on undeformed shape.

            * ``1`` - Display selected items on deformed shape.

        viewup : int or str
            View Up key:

            * ``0`` - Ignore the view-up ( :ref:`vup` ) vector when calculating trapezoid orientation (default).

            * ``1`` - Use the view-up ( :ref:`vup` ) vector to calculate trapezoid orientation.

        Notes
        -----

        .. _PLLS_notes:

        Displays selected items (such as shears and moments) as a contoured area (trapezoid) display along
        line elements and 2D axisymmetric shell elements (such as shear and moment diagrams). Three sides of
        the trapezoid are formed by the element (one side) and lines at nodes I and J of length proportional
        to the item magnitude and displayed normal to the element and the viewing direction (the two
        parallel sides).

        When ``ViewUP`` = 1, the trapezoid is oriented within the plane created by the element and the
        global Cartesian coordinate system reference orientation (/VUP or view up) vector. In this case, the
        program does not perform the calculation involving the element and view direction.

        Portions of this command are not supported by PowerGraphics ( :ref:`graphics`,POWER).
        """
        command = f"PLLS,{labi},{labj},{fact},{kund},{viewup}"
        return self.run(command, **kwargs)

    def pretab(
        self,
        lab1: str = "",
        lab2: str = "",
        lab3: str = "",
        lab4: str = "",
        lab5: str = "",
        lab6: str = "",
        lab7: str = "",
        lab8: str = "",
        lab9: str = "",
        **kwargs,
    ):
        r"""Prints the element table items.

        Mechanical APDL Command: `PRETAB <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PRETAB.html>`_

        Parameters
        ----------
        lab1 : str
            Print selected items. Valid labels are (blank) or any label as specified with the :ref:`etable`
            command. Convenience labels may be used for ``Lab1`` to select groups of labels (10 labels
            maximum): GRP1 for first 10 stored items; GRP2 for items 11 to 20; GRP3 for items 21 to 30; GRP4
            for items 31 to 40; GRP5 for items 41 to 50. Enter :ref:`etable`,STAT command to list stored
            item order. If all labels are blank, print first 10 stored items (GRP1).

        lab2 : str
            Print selected items. Valid labels are (blank) or any label as specified with the :ref:`etable`
            command. Convenience labels may be used for ``Lab1`` to select groups of labels (10 labels
            maximum): GRP1 for first 10 stored items; GRP2 for items 11 to 20; GRP3 for items 21 to 30; GRP4
            for items 31 to 40; GRP5 for items 41 to 50. Enter :ref:`etable`,STAT command to list stored
            item order. If all labels are blank, print first 10 stored items (GRP1).

        lab3 : str
            Print selected items. Valid labels are (blank) or any label as specified with the :ref:`etable`
            command. Convenience labels may be used for ``Lab1`` to select groups of labels (10 labels
            maximum): GRP1 for first 10 stored items; GRP2 for items 11 to 20; GRP3 for items 21 to 30; GRP4
            for items 31 to 40; GRP5 for items 41 to 50. Enter :ref:`etable`,STAT command to list stored
            item order. If all labels are blank, print first 10 stored items (GRP1).

        lab4 : str
            Print selected items. Valid labels are (blank) or any label as specified with the :ref:`etable`
            command. Convenience labels may be used for ``Lab1`` to select groups of labels (10 labels
            maximum): GRP1 for first 10 stored items; GRP2 for items 11 to 20; GRP3 for items 21 to 30; GRP4
            for items 31 to 40; GRP5 for items 41 to 50. Enter :ref:`etable`,STAT command to list stored
            item order. If all labels are blank, print first 10 stored items (GRP1).

        lab5 : str
            Print selected items. Valid labels are (blank) or any label as specified with the :ref:`etable`
            command. Convenience labels may be used for ``Lab1`` to select groups of labels (10 labels
            maximum): GRP1 for first 10 stored items; GRP2 for items 11 to 20; GRP3 for items 21 to 30; GRP4
            for items 31 to 40; GRP5 for items 41 to 50. Enter :ref:`etable`,STAT command to list stored
            item order. If all labels are blank, print first 10 stored items (GRP1).

        lab6 : str
            Print selected items. Valid labels are (blank) or any label as specified with the :ref:`etable`
            command. Convenience labels may be used for ``Lab1`` to select groups of labels (10 labels
            maximum): GRP1 for first 10 stored items; GRP2 for items 11 to 20; GRP3 for items 21 to 30; GRP4
            for items 31 to 40; GRP5 for items 41 to 50. Enter :ref:`etable`,STAT command to list stored
            item order. If all labels are blank, print first 10 stored items (GRP1).

        lab7 : str
            Print selected items. Valid labels are (blank) or any label as specified with the :ref:`etable`
            command. Convenience labels may be used for ``Lab1`` to select groups of labels (10 labels
            maximum): GRP1 for first 10 stored items; GRP2 for items 11 to 20; GRP3 for items 21 to 30; GRP4
            for items 31 to 40; GRP5 for items 41 to 50. Enter :ref:`etable`,STAT command to list stored
            item order. If all labels are blank, print first 10 stored items (GRP1).

        lab8 : str
            Print selected items. Valid labels are (blank) or any label as specified with the :ref:`etable`
            command. Convenience labels may be used for ``Lab1`` to select groups of labels (10 labels
            maximum): GRP1 for first 10 stored items; GRP2 for items 11 to 20; GRP3 for items 21 to 30; GRP4
            for items 31 to 40; GRP5 for items 41 to 50. Enter :ref:`etable`,STAT command to list stored
            item order. If all labels are blank, print first 10 stored items (GRP1).

        lab9 : str
            Print selected items. Valid labels are (blank) or any label as specified with the :ref:`etable`
            command. Convenience labels may be used for ``Lab1`` to select groups of labels (10 labels
            maximum): GRP1 for first 10 stored items; GRP2 for items 11 to 20; GRP3 for items 21 to 30; GRP4
            for items 31 to 40; GRP5 for items 41 to 50. Enter :ref:`etable`,STAT command to list stored
            item order. If all labels are blank, print first 10 stored items (GRP1).

        Notes
        -----

        .. _PRETAB_notes:

        Prints the items stored in the table defined with the :ref:`etable` command. Item values will be
        listed for the selected elements in the sorted sequence ( :ref:`esort` ). The :ref:`force` command
        can be used to define which component of the nodal load is to be used (static, damping, inertia, or
        total).

        Portions of this command are not supported by PowerGraphics ( :ref:`graphics`,POWER).
        """
        command = (
            f"PRETAB,{lab1},{lab2},{lab3},{lab4},{lab5},{lab6},{lab7},{lab8},{lab9}"
        )
        return self.run(command, **kwargs)

    def sabs(self, key: int | str = "", **kwargs):
        r"""Specifies absolute values for element table operations.

        Mechanical APDL Command: `SABS <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SABS.html>`_

        Parameters
        ----------
        key : int or str
            Absolute value key:

            * ``0`` - Use algebraic values in operations.

            * ``1`` - Use absolute values in operations.

        Notes
        -----

        .. _SABS_notes:

        Causes absolute values to be used in the :ref:`sadd`, :ref:`smult`, :ref:`smax`, :ref:`smin`, and
        :ref:`ssum` operations.
        """
        command = f"SABS,{key}"
        return self.run(command, **kwargs)

    def sadd(
        self,
        labr: str = "",
        lab1: str = "",
        lab2: str = "",
        fact1: str = "",
        fact2: str = "",
        const: str = "",
        **kwargs,
    ):
        r"""Forms an element table item by adding two existing items.

        Mechanical APDL Command: `SADD <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SADD.html>`_

        Parameters
        ----------
        labr : str
            Label assigned to results. If same as existing label, the existing values will be overwritten by
            these results.

        lab1 : str
            First labeled result item in operation.

        lab2 : str
            Second labeled result item in operation (may be blank).

        fact1 : str
            Scale factor applied to ``Lab1``. A (blank) or '0' entry defaults to 1.0.

        fact2 : str
            Scale factor applied to ``Lab2``. A (blank) or '0' entry defaults to 1.0.

        const : str
            Constant value.

        Notes
        -----

        .. _SADD_notes:

        Forms a labeled result (see :ref:`etable` command) for the selected elements by adding two existing
        labeled result items according to the operation:

        ``LabR`` = ( ``FACT1`` x ``Lab1`` ) + ( ``FACT2`` x ``Lab2`` ) + ``CONST``

        May also be used to scale results for a single labeled result item. If absolute values are requested
        ( :ref:`sabs`,1), absolute values of ``Lab1`` and ``Lab2`` are used.
        """
        command = f"SADD,{labr},{lab1},{lab2},{fact1},{fact2},{const}"
        return self.run(command, **kwargs)

    def sallow(
        self,
        strs1: str = "",
        strs2: str = "",
        strs3: str = "",
        strs4: str = "",
        strs5: str = "",
        strs6: str = "",
        **kwargs,
    ):
        r"""Defines the allowable stress table for safety factor calculations.

        Mechanical APDL Command: `SALLOW <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SALLOW.html>`_

        Parameters
        ----------
        strs1 : str
            Input up to six allowable stresses corresponding to the temperature points ( :ref:`tallow` ).

        strs2 : str
            Input up to six allowable stresses corresponding to the temperature points ( :ref:`tallow` ).

        strs3 : str
            Input up to six allowable stresses corresponding to the temperature points ( :ref:`tallow` ).

        strs4 : str
            Input up to six allowable stresses corresponding to the temperature points ( :ref:`tallow` ).

        strs5 : str
            Input up to six allowable stresses corresponding to the temperature points ( :ref:`tallow` ).

        strs6 : str
            Input up to six allowable stresses corresponding to the temperature points ( :ref:`tallow` ).

        Notes
        -----

        .. _SALLOW_notes:

        Defines the allowable stress table for safety factor calculations ( :ref:`sfact`, :ref:`sfcalc` ).
        Use the :ref:`stat` command to list current allowable stress table. Repeat :ref:`sallow` to zero
        table and redefine points (6 maximum).

        Safety factor calculations are not supported by PowerGraphics. Both the :ref:`sallow` and
        :ref:`tallow` commands must be used with the Full Model Graphics display method active.
        """
        command = f"SALLOW,{strs1},{strs2},{strs3},{strs4},{strs5},{strs6}"
        return self.run(command, **kwargs)

    def sexp(
        self,
        labr: str = "",
        lab1: str = "",
        lab2: str = "",
        exp1: str = "",
        exp2: str = "",
        **kwargs,
    ):
        r"""Forms an element table item by exponentiating and multiplying.

        Mechanical APDL Command: `SEXP <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SEXP.html>`_

        Parameters
        ----------
        labr : str
            Label assigned to results. If same as existing label, the existing values will be overwritten by
            these results.

        lab1 : str
            First labeled result item in operation.

        lab2 : str
            Second labeled result item in operation (may be blank).

        exp1 : str
            Exponent applied to ``Lab1``.

        exp2 : str
            Exponent applied to ``Lab2``.

        Notes
        -----

        .. _SEXP_notes:

        Forms a labeled result item (see :ref:`etable` command) for the selected elements by exponentiating
        and multiplying two existing labeled result items according to the operation:

        ``LabR`` = (\| ``Lab1`` \| :sup:`EXP1` ) x (\| ``Lab2`` \| :sup:`EXP2` )

        Roots, reciprocals, and divides may also be done with this command.
        """
        command = f"SEXP,{labr},{lab1},{lab2},{exp1},{exp2}"
        return self.run(command, **kwargs)

    def sfact(self, type_: int | str = "", **kwargs):
        r"""Allows safety factor or margin of safety calculations to be made.

        Mechanical APDL Command: `SFACT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SFACT.html>`_

        Parameters
        ----------
        type_ : int or str
            Type of calculation:

            * ``0`` - No nodal safety factor or margin of safety calculations.

            * ``1`` - Calculate and store safety factors in place of nodal stresses.

            * ``2`` - Calculate and store margins of safety in place of nodal stresses.

        Notes
        -----

        .. _SFACT_notes:

        Allows safety factor (SF) or margin of safety (MS) calculations to be made for the average nodal
        stresses according to:

        SF = SALLOW/\|Stress\|

        MS = (SALLOW/\|Stress\|) -- 1.0

        Calculations are done during the display, select, or sort operation in the active coordinate system
        ( :ref:`rsys` ) with results stored in place of the nodal stresses. Use the :ref:`prnsol` or
        :ref:`plnsol` command to display the results.

        The results are meaningful only for the stress (SIG1, SIGE, etc.) upon which :ref:`sallow` is based.
        Nodal temperatures used are those automatically stored for the node. Related commands are
        :ref:`sfcalc`, :ref:`sallow`, :ref:`tallow`.
        """
        command = f"SFACT,{type_}"
        return self.run(command, **kwargs)

    def sfcalc(
        self,
        labr: str = "",
        labs: str = "",
        labt: str = "",
        type_: int | str = "",
        **kwargs,
    ):
        r"""Calculates the safety factor or margin of safety.

        Mechanical APDL Command: `SFCALC <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SFCALC.html>`_

        Parameters
        ----------
        labr : str
            Label assigned to results. If same as existing label, the existing values will be overwritten by
            these results.

        labs : str
            Labeled result item corresponding to the element stress.

        labt : str
            Labeled result item corresponding to the element temperature.

        type_ : int or str
            Type of calculation:

            * ``0 or 1`` - Use safety factor (SF) calculation.

            * ``2`` - Use margin of safety (MS) calculation.

            * ``3`` - Use 1/SF calculation.

        Notes
        -----

        .. _SFCALC_notes:

        Calculates safety factor (SF) or margin of safety (MS) as described for the :ref:`sfact` command for
        any labeled result item (see :ref:`etable` command) for the selected elements. Use the :ref:`pretab`
        or :ref:`pletab` command to display results. Allowable element stress is determined from the SALLOW-
        TALLOW table ( :ref:`sallow`, :ref:`tallow` ).
        """
        command = f"SFCALC,{labr},{labs},{labt},{type_}"
        return self.run(command, **kwargs)

    def smax(
        self,
        labr: str = "",
        lab1: str = "",
        lab2: str = "",
        fact1: str = "",
        fact2: str = "",
        **kwargs,
    ):
        r"""Forms an element table item from the maximum of two other items.

        Mechanical APDL Command: `SMAX <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SMAX.html>`_

        Parameters
        ----------
        labr : str
            Label assigned to results. If same as existing label, the existing values will be overwritten by
            these results.

        lab1 : str
            First labeled result item in operation.

        lab2 : str
            Second labeled result item in operation (may be blank).

        fact1 : str
            Scale factor applied to ``Lab1``. A (blank) or '0' entry defaults to 1.0.

        fact2 : str
            Scale factor applied to ``Lab2``. A (blank) or '0' entry defaults to 1.0.

        Notes
        -----

        .. _SMAX_notes:

        Forms a labeled result item (see :ref:`etable` command) for the selected elements by comparing two
        existing labeled result items according to the operation:

        ``LabR`` = ( ``FACT1`` x ``Lab1`` ) cmx ( ``FACT2`` x ``Lab2`` )

        where "cmx" means "compare and save maximum." If absolute values are requested ( :ref:`sabs`,1), the
        absolute values of ``Lab1`` and ``Lab2`` are used.
        """
        command = f"SMAX,{labr},{lab1},{lab2},{fact1},{fact2}"
        return self.run(command, **kwargs)

    def smin(
        self,
        labr: str = "",
        lab1: str = "",
        lab2: str = "",
        fact1: str = "",
        fact2: str = "",
        **kwargs,
    ):
        r"""Forms an element table item from the minimum of two other items.

        Mechanical APDL Command: `SMIN <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SMIN.html>`_

        Parameters
        ----------
        labr : str
            Label assigned to results. If same as existing label, the existing values will be overwritten by
            these results.

        lab1 : str
            First labeled result item in operation.

        lab2 : str
            Second labeled result item in operation (may be blank).

        fact1 : str
            Scale factor applied to ``Lab1``. A (blank) or '0' entry defaults to 1.0.

        fact2 : str
            Scale factor applied to ``Lab2``. A (blank) or '0' entry defaults to 1.0.

        Notes
        -----

        .. _SMIN_notes:

        Forms a labeled result item (see :ref:`etable` command) for the selected elements by comparing two
        existing labeled result items according to the operation:

        ``LabR`` = ( ``FACT1`` x ``Lab1`` ) cmn ( ``FACT2`` x ``Lab2`` )

        where "cmn" means "compare and save minimum." If absolute values are requested ( :ref:`sabs`,1), the
        absolute values of ``Lab1`` and ``Lab2`` are used.
        """
        command = f"SMIN,{labr},{lab1},{lab2},{fact1},{fact2}"
        return self.run(command, **kwargs)

    def smult(
        self,
        labr: str = "",
        lab1: str = "",
        lab2: str = "",
        fact1: str = "",
        fact2: str = "",
        **kwargs,
    ):
        r"""Forms an element table item by multiplying two other items.

        Mechanical APDL Command: `SMULT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SMULT.html>`_

        Parameters
        ----------
        labr : str
            Label assigned to results. If same as existing label, the existing values will be overwritten by
            these results.

        lab1 : str
            First labeled result item in operation.

        lab2 : str
            Second labeled result item in operation (may be blank).

        fact1 : str
            Scale factor applied to ``Lab1``. A (blank) or '0' entry defaults to 1.0.

        fact2 : str
            Scale factor applied to ``Lab2``. A (blank) or '0' entry defaults to 1.0.

        Notes
        -----

        .. _SMULT_notes:

        Forms a labeled result item (see :ref:`etable` command) for the selected elements by multiplying two
        existing labeled result items according to the operation:

        ``LabR`` = ( ``FACT1`` x ``Lab1`` ) x ( ``FACT2`` x ``Lab2`` )

        May also be used to scale results for a single labeled result item. If absolute values are requested
        ( :ref:`sabs`,1), the absolute values of ``Lab1`` and ``Lab2`` are used.
        """
        command = f"SMULT,{labr},{lab1},{lab2},{fact1},{fact2}"
        return self.run(command, **kwargs)

    def ssum(self, **kwargs):
        r"""Calculates and prints the sum of element table items.

        Mechanical APDL Command: `SSUM <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SSUM.html>`_

        Notes
        -----

        .. _SSUM_notes:

        Calculates and prints the tabular sum of each existing labeled result item ( :ref:`etable` ) for the
        selected elements. If absolute values are requested ( :ref:`sabs`,1), absolute values are used.
        """
        command = "SSUM"
        return self.run(command, **kwargs)

    def tallow(
        self,
        temp1: str = "",
        temp2: str = "",
        temp3: str = "",
        temp4: str = "",
        temp5: str = "",
        temp6: str = "",
        **kwargs,
    ):
        r"""Defines the temperature table for safety factor calculations.

        Mechanical APDL Command: `TALLOW <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_TALLOW.html>`_

        Parameters
        ----------
        temp1 : str
            Input up to six temperatures covering the range of nodal temperatures. Temperatures must be
            input in ascending order.

        temp2 : str
            Input up to six temperatures covering the range of nodal temperatures. Temperatures must be
            input in ascending order.

        temp3 : str
            Input up to six temperatures covering the range of nodal temperatures. Temperatures must be
            input in ascending order.

        temp4 : str
            Input up to six temperatures covering the range of nodal temperatures. Temperatures must be
            input in ascending order.

        temp5 : str
            Input up to six temperatures covering the range of nodal temperatures. Temperatures must be
            input in ascending order.

        temp6 : str
            Input up to six temperatures covering the range of nodal temperatures. Temperatures must be
            input in ascending order.

        Notes
        -----

        .. _TALLOW_notes:

        Defines the temperature table for safety factor calculations ( :ref:`sfact`, :ref:`sallow` ). Use
        :ref:`stat` command to list current temperature table. Repeat :ref:`tallow` command to zero table
        and redefine points (6 maximum).

        Safety factor calculations are not supported by PowerGraphics. Both the :ref:`sallow` and
        :ref:`tallow` commands must be used with the Full Model Graphics display method active.
        """
        command = f"TALLOW,{temp1},{temp2},{temp3},{temp4},{temp5},{temp6}"
        return self.run(command, **kwargs)

    def vcross(
        self,
        labxr: str = "",
        labyr: str = "",
        labzr: str = "",
        labx1: str = "",
        laby1: str = "",
        labz1: str = "",
        labx2: str = "",
        laby2: str = "",
        labz2: str = "",
        **kwargs,
    ):
        r"""Forms element table items from the cross product of two vectors.

        Mechanical APDL Command: `VCROSS <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_VCROSS.html>`_

        Parameters
        ----------
        labxr : str
            Label assigned to X, Y, and Z-component of resultant vector.

        labyr : str
            Label assigned to X, Y, and Z-component of resultant vector.

        labzr : str
            Label assigned to X, Y, and Z-component of resultant vector.

        labx1 : str
            X, Y, and Z-component of first vector label.

        laby1 : str
            X, Y, and Z-component of first vector label.

        labz1 : str
            X, Y, and Z-component of first vector label.

        labx2 : str
            X, Y, and Z-component of second vector label.

        laby2 : str
            X, Y, and Z-component of second vector label.

        labz2 : str
            X, Y, and Z-component of second vector label.

        Notes
        -----

        .. _VCROSS_notes:

        Forms labeled result items for the selected element from the cross product of two vectors:

        { ``LabXR``, ``LabYR``, ``LabZR`` } = { ``LabX1``, ``LabY1``, ``LabZ1`` } X { ``LabX2``, ``LabY2``,
        ``LabZ2`` }

        Data must be in a consistent coordinate system. Labels are those associated with the :ref:`etable`
        command.
        """
        command = f"VCROSS,{labxr},{labyr},{labzr},{labx1},{laby1},{labz1},{labx2},{laby2},{labz2}"
        return self.run(command, **kwargs)

    def vdot(
        self,
        labr: str = "",
        labx1: str = "",
        laby1: str = "",
        labz1: str = "",
        labx2: str = "",
        laby2: str = "",
        labz2: str = "",
        **kwargs,
    ):
        r"""Forms an element table item from the dot product of two vectors.

        Mechanical APDL Command: `VDOT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_VDOT.html>`_

        Parameters
        ----------
        labr : str
            Label assigned to dot product result.

        labx1 : str
            X, Y, and Z-component of first vector label.

        laby1 : str
            X, Y, and Z-component of first vector label.

        labz1 : str
            X, Y, and Z-component of first vector label.

        labx2 : str
            X, Y, and Z-component of second vector label.

        laby2 : str
            X, Y, and Z-component of second vector label.

        labz2 : str
            X, Y, and Z-component of second vector label.

        Notes
        -----

        .. _VDOT_notes:

        Forms labeled result items for the selected element from the dot product of two vectors:

        ``LabR`` = { ``LabX1``, ``LabY1``, ``LabZ1`` } { ``LabX2``, ``LabY2``, ``LabZ2`` }

        Data must be in a consistent coordinate system. Labels are those associated with the :ref:`etable`
        command.
        """
        command = f"VDOT,{labr},{labx1},{laby1},{labz1},{labx2},{laby2},{labz2}"
        return self.run(command, **kwargs)
