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


class Results(CommandsBase):

    def lcsum(self, lab: str = "", **kwargs):
        r"""Specifies whether to process non-summable items in load case operations.

        Mechanical APDL Command: `LCSUM <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_LCSUM.html>`_

        Parameters
        ----------
        lab : str
            Combination option

            * ``(blank)`` - Only combine summable items [default].

            * ``ALL`` - Combine all items including non summable items.

        Notes
        -----

        .. _LCSUM_notes:

        Allows non-summable items (e.g. plastic strains) to be included in load combinations. Issue
        :ref:`lcsum`,ALL before the first load case operation ( **LC** ``XX``  command). May also be used to
        include nonsummable items in the appending of a results file ( :ref:`rappnd` command).

        For details on using load case combination, see `Creating and Combining Load Cases
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/Hlp_G_BAS5_4.html#bassummtlm51499325>`_
        """
        command = f"LCSUM,{lab}"
        return self.run(command, **kwargs)

    def nsort(
        self,
        item: str = "",
        comp: str = "",
        order: int | str = "",
        kabs: int | str = "",
        numb: str = "",
        sel: str = "",
        **kwargs,
    ):
        r"""Sorts nodal data.

        Mechanical APDL Command: `NSORT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_NSORT.html>`_

        Parameters
        ----------
        item : str
            Label identifying the item to be sorted on. Valid item labels are shown in the table below. Some
            items also require a component label.

        comp : str
            Component of the item (if required). Valid component labels are shown in the table below.

        order : int or str
            Order of sort operation:

            * ``0`` - Sort into descending order.

            * ``1`` - Sort into ascending order.

        kabs : int or str
            Absolute value key:

            * ``0`` - Sort according to real value.

            * ``1`` - Sort according to absolute value.

        numb : str
            Number of nodal data records to be sorted in ascending or descending order ( ``ORDER`` ) before
            sort is stopped (remainder will be in unsorted sequence) (defaults to all nodes).

        sel : str
            Allows selection of nodes in the sorted field.

            * ``(blank)`` - No selection (default).

            * ``SELECT`` - Select the nodes in the sorted list.

        Notes
        -----

        .. _NSORT_notes:

        Values are in the active coordinate system ( :ref:`csys` for input data or :ref:`rsys` for results
        data). Various element results also depend upon the recalculation method and the selected results
        location ( :ref:`avprin`, :ref:`rsys`, :ref:`shell`, :ref:`esel`, and :ref:`nsel` ). If simultaneous
        load cases are stored, the last sorted sequence formed from any load case applies to all load cases.
        Use :ref:`nusort` to restore the original order. This command is not valid with PowerGraphics.

        .. _nsort_tab_1:

        NSORT - Valid Item and Component Labels
        ***************************************

        .. flat-table:: Valid Item and Component Labels :ref:`nsort`, ``Item,Comp,ORDER,KABS,NUMB,SEL``
           :header-rows: 2

           * - Valid item and component labels for input values are:
           * - Item
             - Comp
             - Description
           * - LOC
             - X, Y, Z
             - X, Y, or Z location.
           * - ANG
             - XY, YZ, ZX
             - THXY, THYZ, or THZX rotation angle.


        .. _nsort_tab_2:

        NSORT - Valid Item and Component Labels for Nodal DOF Result Values
        *******************************************************************

        .. flat-table::
           :header-rows: 1

           * - Item
             - Comp
             - Description
           * - U
             - X, Y, Z, SUM
             - X, Y, or Z structural displacement or vector sum.
           * - ROT
             - X, Y, Z, SUM
             - X, Y, or Z structural rotation or vector sum.
           * - TEMP
             -
             - Temperature (includes TEMP, TBOT, TE2, TE3,..., TTOP values).
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
             - X, Y, Z, SUM
             - X, Y, or Z fluid velocity or vector sum.
           * - A
             - X, Y, Z, SUM
             - X, Y, or Z magnetic vector potential or vector sum.
           * - CONC
             -
             - Concentration
           * - CURR
             -
             - Current.
           * - EMF
             -
             - Electromotive force drop.


        .. _nsort_tab_3:

        NSORT - Valid Item and Component Labels for Element Result Values
        *****************************************************************

        .. flat-table::
           :header-rows: 1

           * - Item
             - Comp
             - Description
           * - S
             - X, Y, Z, XY, YZ, XZ
             - Component stress.
           * - "
             - 1, 2,3
             - Principal stress.
           * - "
             - INT, EQV
             - Stress intensity or equivalent stress.
           * - EPTO
             - X, Y, Z, XY, YZ, XZ
             - Component total strain (EPEL + EPPL + EPCR).
           * - "
             - 1, 2, 3
             - Principal total strain.
           * - "
             - INT, EQV
             - Total strain intensity or total equivalent strain.
           * - EPEL
             - X, Y, Z, XY, YZ, XZ
             - Component elastic strain.
           * - "
             - 1, 2, 3
             - Principal elastic strain.
           * - "
             - INT, EQV
             - Elastic strain intensity or elastic equivalent strain.
           * - EPPL
             - X, Y, Z, XY, YZ, XZ
             - Component plastic strain.
           * - "
             - 1, 2, 3
             - Principal plastic strain.
           * - "
             - INT, EQV
             - Plastic strain intensity or plastic equivalent strain.
           * - EPCR
             - X, Y, Z, XY, YZ, XZ
             - Component creep strain.
           * - "
             - 1, 2, 3
             - Principal creep strain.
           * - "
             - INT, EQV
             - Creep strain intensity or creep equivalent strain.
           * - EPTH
             - X, Y, Z, XY, YZ, XZ
             - Component thermal strain.
           * - "
             - 1, 2, 3
             - Principal thermal strain.
           * - "
             - INT, EQV
             - Thermal strain intensity or thermal equivalent strain.
           * - EPSW
             -
             - Swelling strain.
           * - EPDI
             - X, Y, Z, XY, YZ, XZ
             - Component diffusion strain.
           * - "
             - 1, 2, 3
             - Principal diffusion strain.
           * - "
             - INT, EQV
             - Diffusion strain intensity or diffusion equivalent strain.
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
           * - FAIL
             - MAX
             - Maximum of all active failure criteria defined at the current location. (See the :ref:`fctyp` command for details.) [ :ref:`NSORTinputneed` ]
           * - "
             - EMAX
             - Maximum Strain Failure Criterion [ :ref:`NSORTinputneed` ]
           * - "
             - SMAX
             - Maximum Stress Failure Criterion [ :ref:`NSORTinputneed` ]
           * - "
             - TWSI
             - Tsai-Wu Strength Index Failure Criterion [ :ref:`NSORTinputneed` ]
           * - "
             - TWSR
             - Inverse of Tsai-Wu Strength Ratio Index Failure Criterion [ :ref:`NSORTinputneed` ]
           * - "
             - HFIB
             - Hashin Fiber Failure Criterion. [ :ref:`NSORTinputneed` ][ :ref:`nsort_tab_elemlim` ]
           * - "
             - HMAT
             - Hashin Matrix Failure Criterion. [ :ref:`NSORTinputneed` ][ :ref:`nsort_tab_elemlim` ]
           * - "
             - PFIB
             - Puck Fiber Failure Criterion. [ :ref:`NSORTinputneed` ][ :ref:`nsort_tab_elemlim` ]
           * - "
             - PMAT
             - Puck Matrix Failure Criterion. [ :ref:`NSORTinputneed` ][ :ref:`nsort_tab_elemlim` ]
           * - "
             - USR1, USR2,..., USR9
             - User-defined failure criteria [ :ref:`NSORTinputneed` ][ :ref:`nsort_tab_elemlim` ][ :ref:`NSORT_ftnote_failcritroutine` ]
           * - CONT
             - STAT [ :ref:`NSORTcontstat` ]
             - Contact status.
           * - "
             - PENE
             - Contact penetration.
           * - "
             - PRES
             - Contact pressure.
           * - "
             - SFRIC
             - Contact friction stress.
           * - "
             - STOT
             - Contact total stress (pressure plus friction).
           * - "
             - SLIDE
             - Contact sliding distance.
           * - TG
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
             - Component concentration gradient or vector sum
           * - DF
             - X, Y, Z, SUM
             - Component diffusion flux density or vector sum
           * - FMAG
             - X, Y, Z, SUM
             - Component electromagnetic forces or vector sum.

        .. _NSORTinputneed:

        Works only if failure criteria information is provided. (For more information, see the documentation
        for the :ref:`fc` and :ref:`tb` commands.)

        .. _nsort_tab_elemlim:

        Must be added via the :ref:`fctyp` command first.

        .. _NSORT_ftnote_failcritroutine:

        Works only if user failure criteria routine is provided.

        .. _NSORTcontstat:

        For more information about contact status and its possible values, see `Reviewing Results in POST1
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_ctec/Hlp_ctec_revresu.html#ctecpostslide>`_
        """
        command = f"NSORT,{item},{comp},{order},{kabs},{numb},{sel}"
        return self.run(command, **kwargs)

    def nusort(self, **kwargs):
        r"""Restores original order for nodal data.

        Mechanical APDL Command: `NUSORT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_NUSORT.html>`_

        Notes
        -----

        .. _NUSORT_notes:

        This command restores the nodal data to its original order (sorted in ascending node number
        sequence) after an :ref:`nsort` command. Changing the selected nodal set ( :ref:`nsel` ) also
        restores the original nodal order.
        """
        command = "NUSORT"
        return self.run(command, **kwargs)

    def plcint(
        self,
        action: str = "",
        id_: str = "",
        node: str = "",
        cont: str = "",
        dtype: str = "",
        **kwargs,
    ):
        r"""Plots the fracture parameter ( :ref:`cint` ) result data.

        Mechanical APDL Command: `PLCINT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PLCINT.html>`_

        Parameters
        ----------
        action : str
            * ``PATH`` - Plots :ref:`cint` quantities according to path number (default).

            * ``FRONT`` - Plots :ref:`cint` quantities distribution along the crack front.

        id_ : str
            Crack ID number.

        node : str
            Crack tip node number (default = ALL).

            Use only for ``ACTION`` = PATH. Plots :ref:`cint` contour for an individual crack tip node.

        cont : str
            Contour number (Default = ALL).

            Use only for ``ACTION`` = FRONT. Plots :ref:`cint` distribution along the crack for a given
            path.

        dtype : str
            Data type to output:

            * ``JINT`` - J-integral (default)

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

            * ``TSTRESS`` - T-stress

            * ``CEXT`` - Crack extension

            * ``CSTAR`` - C\2-integral

        Notes
        -----

        .. _PLCINT_notes:

        The :ref:`plcint` command is not available for `XFEM-based crack-growth
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/Hlp_G_FRACXFEM.html#fracxfemreferences>`_
        analyses results processing.
        """
        command = f"PLCINT,{action},{id_},{node},{cont},{dtype}"
        return self.run(command, **kwargs)

    def plcksurf(self, modeldisplay: int | str = "", **kwargs):
        r"""Plots the Φ = 0 level set surface in an `XFEM-based crack analysis
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/Hlp_G_FRACXFEM.html#fracxfemreferences>`_

        Mechanical APDL Command: `PLCKSURF <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PLCKSURF.html>`_

        Parameters
        ----------
        modeldisplay : int or str
            Solid model display behavior:

            * ``0`` - No display of the solid model (default).

            * ``1`` - Solid model displayed with translucency and edges disabled.

        Notes
        -----

        .. _PLCKSURF_notes:

        The :ref:`plcksurf` command is available only for `XFEM-based crack analysis
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/Hlp_G_FRACXFEM.html#fracxfemreferences>`_
        during results processing.
        """
        command = f"PLCKSURF,{modeldisplay}"
        return self.run(command, **kwargs)

    def pldisp(self, kund: int | str = "", **kwargs):
        r"""Displays the displaced structure.

        Mechanical APDL Command: `PLDISP <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PLDISP.html>`_

        Parameters
        ----------
        kund : int or str
            Undisplaced shape key:

            * ``0`` - Display only displaced structure.

            * ``1`` - Overlay displaced display with similar undisplaced display (appearance is system-
              dependent).

            * ``2`` - Same as 1 except overlay with undisplaced edge display (appearance is system-dependent).

        Notes
        -----

        .. _PLDISP_notes:

        Displays the displaced structure for the selected elements.

        For information on true scale plots, refer to the description of the :ref:`slashdscale` command (
        :ref:`slashdscale`,,1.0).
        """
        command = f"PLDISP,{kund}"
        return self.run(command, **kwargs)

    def plesol(
        self,
        item: str = "",
        comp: str = "",
        kund: int | str = "",
        fact: str = "",
        avg: int | str = "",
        **kwargs,
    ):
        r"""Displays solution results as discontinuous element contours.

        Mechanical APDL Command: `PLESOL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PLESOL.html>`_

        Parameters
        ----------
        item : str
            Label identifying the item. Valid item labels are shown in the table below. Some items also
            require a component label.

        comp : str
            Component of the item (if required). Valid component labels are shown in the table below.

        kund : int or str
            Undisplaced shape key:

            * ``0`` - Do not overlay undeformed structure display.

            * ``1`` - Overlay displaced contour plot with undeformed display (appearance is system-dependent).

            * ``2`` - Overlay displaced contour plot with undeformed edge display (appearance is system-
              dependent).

        fact : str
            Scale factor for 2D display of contact items. Default = 1. To invert the display, specify a
            negative scaling factor.

        avg : int or str
            Specifies whether results of reinforcing members within the same reinforcing element are smoothed:

            * ``0`` - Disable smoothing.

            * ``1`` - Enable smoothing (default), displaying constant results of reinforcing members if the base
              elements are low-order, and linear results when the base elements are high-order.

        Notes
        -----

        .. _PLESOL_notes:

        :ref:`plesol` displays the solution results as element contours discontinuous across element
        boundaries for the selected elements.

        For example, :ref:`plesol`,S,X displays the X component of stress S (that is, the SX stress
        component). Various element results depend on the calculation method and the selected results
        location ( :ref:`avprin`, :ref:`rsys`, and :ref:`esel` ).

        Contours are determined by linear interpolation within each element, unaffected by the surrounding
        elements; that is, no nodal averaging occurs. The discontinuity between contours of adjacent
        elements is an indication of the gradient across elements. Component results are displayed in the
        active results coordinate system ( :ref:`rsys` [default is global Cartesian]).

        To display items not available via :ref:`plesol` (such as line element results), see :ref:`etable`
        and :ref:`pletab`.

        For PowerGraphics displays ( :ref:`graphics`,POWER), results are plotted only for the model exterior
        surface. Items not supported by PowerGraphics are noted in :ref:`plesol_tab_1`.

        The results displayed by :ref:`plesol` are unaffected by any requested nodal-averaged results (
        :ref:`outres`,NAR). For more information, see `Nodal-Averaged Results
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_CH2_2.html#nodeavepost>`_

        For ``Item`` = SRES, selected result ( :ref:`osresult` ) values are output. See :ref:`PLESOL_tab_2`.

        .. _plesol_tab_1:

        PLESOL - General Result Item and Component Labels
        *************************************************

        .. flat-table:: General Item and Component Labels :ref:`plesol`, ``Item, Comp``
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
           * - :rspan:`3` EPDI
             - X, Y, Z, XY, YZ, XZ
             - Component diffusion strain. Not supported by PowerGraphics.
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
           * - :rspan:`3` EPTH
             - X, Y, Z, XY, YZ, XZ
             - Component thermal strain.
           * - 1, 2, 3
             - Principal thermal strain.
           * - INT
             - Thermal strain intensity.
           * - EQV
             - Thermal equivalent strain.
           * - EPSW
             -
             - Swelling strain.
           * - :rspan:`3` EPTO
             - X, Y, Z, XY, YZ, XZ
             - Component total mechanical strain (EPEL + EPPL + EPCR).
           * - 1, 2, 3
             - Principal total mechanical strain.
           * - INT
             - Total mechanical strain intensity.
           * - EQV
             - Total mechanical equivalent strain.
           * - :rspan:`3` EPTT
             - X, Y, Z, XY, YZ, XZ
             - Total mechanical, thermal, diffusion, and swelling strain (EPEL + EPPL + EPCR + EPTH + EPDI + EPSW).
           * - 1, 2, 3
             - Principal total mechanical, thermal, diffusion, and swelling strain.
           * - INT
             - Total mechanical, thermal, diffusion, and swelling strain intensity.
           * - EQV
             - Total mechanical, thermal, diffusion, and swelling equivalent strain.
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
           * - :rspan:`13` FAIL
             - MAX
             - Maximum of all active failure criteria defined at the current location.  Works only if failure criteria are provided ( :ref:`fc` and :ref:`tb` ).
           * - EMAX
             - Maximum Strain Failure Criterion.
           * - SMAX
             - Maximum Stress Failure Criterion.
           * - TWSI
             - Tsai-Wu Strength Index Failure Criterion.
           * - TWSR
             - Inverse of Tsai-Wu Strength Ratio Index Failure Criterion
           * - HFIB
             - Hashin Fiber Failure Criterion.   Must first be added ( :ref:`fctyp`.
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
           * - USR1, USR2,..., USR9
             - User-defined failure criteria.    USR1 through USR9 require a failure-criteria routine.
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
             - Number of the maximum-failure criterion over the entire element:     * 1 = EMAX * 2 = SMAX * 3 = TWSI * 4 = TWSR * 5 = PFIB * 6 = PMAT * 7 = HFIB * 8 = HMAT * 9 = L3FB * 10 = L3MT * 11 = L4FB * 12 = L4MT * 13~21 = USR1~USR9
           * - VAL
             - Value of the maximum failure criterion over the entire element:
           * - SVAR
             - 1, 2, 3,... N
             - State variable.
           * - GKS
             - X, XY, XZ
             - Gasket component stress.
           * - GKD
             - X, XY, XZ
             - Gasket component total closure.
           * - GKDI
             - X, XY, XZ
             - Gasket component total inelastic closure.
           * - GKTH
             - X, XY, XZ
             - Gasket component thermal closure.
           * - SS
             - X, XY, XZ
             - Interface traction (stress).
           * - SD
             - X, XY, XZ
             - Interface separation.
           * - :rspan:`9` CONT
             - STAT
             - Contact status: For MPC-based contact definitions, the value of STAT can be negative, indicating that one or more contact constraints were intentionally removed to prevent overconstraint. STAT = -3 is used for MPC bonded contact; STAT = -2 is used for MPC no-separation contact.     * 3 = closed and sticking * 2 = closed and sliding * 1 = open but near contact * 0 = open and not near contact
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
           * - TG ``Comp`` = SUM is not supported for coupled pore-pressure-thermal (CPT ``nnn`` ) elements.
             - X, Y, Z, SUM
             - Component thermal gradient or vector sum.
           * - TF
             - X, Y, Z, SUM
             - Component thermal flux or vector sum.
           * - PG
             - X, Y, Z, SUM
             - Component or vector sum of velocity or energy density flux (room acoustics).
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
             - Component electromagnetic force or vector sum.
           * - P
             - X, Y, Z, SUM
             - Poynting vector component or sum.
           * - SERR Some element- and material-type limitations apply. (See :ref:`prerr`.)
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
           * - F
             - X, Y, Z
             - X, Y, or Z structural force.  Do not use :ref:`plesol` to obtain contact force values for contact elements. (The force values reported may not be accurate for these elements.) Use :ref:`etable` instead.
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
             - Current flow. Use :ref:`force` for type.
           * - CHRG
             -
             - Charge. Use :ref:`force` for type.
           * - FLUX
             -
             - Magnetic flux.
           * - CSG
             - X, Y, Z
             - X, Y, or Z magnetic current segment component.
           * - RATE
             -
             - Diffusion flow rate.
           * - SENE
             -
             - "Stiffness" energy or thermal heat dissipation. Same as TENE.
           * - STEN
             -
             - Elemental energy dissipation due to `stabilization <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STRUNST.html#>`_.
           * - TENE
             -
             - Thermal heat dissipation or "stiffness" energy. Same as SENE.
           * - KENE
             -
             - Kinetic energy.
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
           * - AENE
             -
             - Artificial energy due to hourglass control/drill stiffness or due to contact stabilization.
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
             - Magnetic Reynolds number.
           * - VOLU
             -
             - Volume of volume element.
           * - CENT
             - X, Y, Z
             - Centroid X, Y, or Z location (based on shape function) in the active coordinate system.
           * - BFE
             - TEMP For `reinforcing <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/str_compreinfdirectemb.html>`_ elements ``REINF264`` and ``REINF265``, issue :ref:`plesol` ,BFE,TEMP to plot the corner-point temperature of each member. You can also plot intersection-point temperature gradients ( :ref:`plesol`,TG) and intersection-point heat flux ( :ref:`plesol`,TF). For higher-order reinforcing members (generated when using higher-order base elements), the midpoint values are not available for the reinforcing members.
             - Body temperatures (calculated from applied temperatures) as used in solution (area and volume elements only). For ``SOLID278`` and ``SOLID279`` with KEYOPT(3) = 2, use :ref:`plesol`,BFE,TEMP to plot the temperature distribution through the thickness of the element. When other thermal elements are included in the model, they should be unselected to avoid plotting undefined information.
           * - SMISC
             - ``snum``
             - Element summable miscellaneous data value at sequence number ``snum`` (shown in the Output Data section of each element description.
           * - NMISC
             - ``snum``
             - Element non-summable miscellaneous data value at sequence number ``snum`` (shown in the Output Data section of each element description.
           * - CAP
             - C0,X0,K0,ZONE, DPLS,VPLS
             - Material cap plasticity model only: Cohesion; hydrostatic compaction yielding stress; I1 at the transition point at which the shear and compaction envelopes intersect; zone = 0: elastic state, zone = 1: compaction zone, zone = 2: shear zone, zone = 3: expansion zone; effective deviatoric plastic strain; volume plastic strain.
           * - EDPC
             - CSIG,CSTR
             - Material EDP creep model only (not including the cap model): Equivalent creep stress; equivalent creep strain.
           * - FICT
             - TEMP
             - Fictive temperature.
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
             - Fluid pore-pressure gradient in poromechanics.
           * - MENE
             -
             - Acoustic potential energy.
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
           * - SNDI
             - X, Y, Z, SUM
             - Component sound intensity or vector sum.
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


        .. _PLESOL_tab_2:

        PLESOL - Selected Result Component Labels
        *****************************************

        .. flat-table:: Selected Result Component Labels :ref:`plesol`,SRES, ``Comp``
           :header-rows: 1

           * - Comp
             - Description
           * - SVAR ``n``
             - The ``n`` th state variable.
           * - FLDUF0 ``n``
             - The ``n`` th user-defined field variable.
        """
        command = f"PLESOL,{item},{comp},{kund},{fact},{avg}"
        return self.run(command, **kwargs)

    def plnsol(
        self,
        item: str = "",
        comp: str = "",
        kund: int | str = "",
        fact: str = "",
        fileid: str = "",
        avg: str = "",
        datakey: str = "",
        **kwargs,
    ):
        r"""Displays solution results as continuous element contours.

        Mechanical APDL Command: `PLNSOL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PLNSOL.html>`_

        Parameters
        ----------
        item : str
            Label identifying the item. Valid item labels are shown in the table below. Some items also
            require a component label.

        comp : str
            Component of the item (if required). Valid component labels are shown in the table below.

        kund : int or str
            Undisplaced shape key:

            * ``0`` - Do not overlay undeformed structure display.

            * ``1`` - Overlay displaced contour plot with undeformed display (appearance is system-dependent).

            * ``2`` - Overlay displaced contour plot with undeformed edge display (appearance is system-
              dependent).

        fact : str
            Scale factor for 2D display for contact items. Default value is 1. A negative scaling factor
            inverts the display.

        fileid : str
            The file index number (obtained via :ref:`nldiag`,NRRE,ON). Valid only for ``Item`` = NRRE.

        avg : str
            Specifies whether random acoustic results are averaged. Valid only for ``Item`` = U and PRES.

            * ``(blank)`` - No averaging (default).

            * ``AVG`` - Display averaged results for random acoustics.

        datakey : str
            Key to specify which data is plotted:

            * ``AUTO`` - `Nodal-averaged results
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_CH2_2.html#nodeavepost>`_ are
              used, if available; otherwise, the element-based data is used, if available. (Default.)

            * ``ESOL`` - Only element-based results are used. If they are not available, the command is ignored.

            * ``NAR`` - Only nodal-averaged results are used. If they are not available, the command is ignored.

        Notes
        -----

        .. _PLNSOL_notes:

        :ref:`plnsol` displays the solution results as continuous contours across element boundaries for the
        selected nodes and elements.

        For example, :ref:`plnsol`,S,X displays the X component of stress S (that is, the SX stress
        component). Various element results depend upon the recalculation method and the selected results
        location ( :ref:`avprin`, :ref:`rsys`, :ref:`layer`, :ref:`shell`, and :ref:`nsel` ).

        Contours are determined by linear interpolation within each element from the nodal values, averaged
        at a node whenever two or more elements connect to the same node. (The exception is FMAG, which is
        summed at the node.)

        For `reinforcing
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/str_compreinfdirectemb.html>`_
        elements (REINF ``nnn`` ), contours are determined by interpolation within each reinforcing member
        of reinforcing elements from the results of the base elements. Element results of members within the
        same reinforcing element are smoothed based on the order of its base element. :ref:`plnsol` displays
        constant results for a reinforcing element if the base elements are low-order, and linear results
        when the base elements are high-order.

        For PowerGraphics displays ( :ref:`graphics`,POWER), results are plotted for the model exterior
        surface only. Items not supported by PowerGraphics are noted in :ref:`plnsol_tab_1`.

        To plot midside nodes, first issue :ref:`efacet`,2.

        If `nodal-averaged results
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_CH2_2.html#nodeavepost>`_ (
        :ref:`outres`,NAR or another nodal-averaged label) are in the database, then :ref:`plnsol` uses the
        nodal-averaged data for the applicable items (S, EPEL, EPPL, EPCR, EPTH, EPSW) by default. You can
        change this behavior via the ``DataKey`` argument. Keep these points in mind when using nodal-
        averaged results:

        * The :ref:`layer` and :ref:`rsys`,SOLU commands are not valid with nodal-averaged results. If these
          commands are used, the element solution is plotted instead if applicable.

        * Issuing :ref:`esel` before plotting nodal-averaged results has no effect on the output.

        * PowerGraphics is supported. The output is equivalent to the full model graphics output, but only
          the appropriate surface nodes are plotted. See `Postprocessing Nodal-Averaged Results
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_CH2_2.html#>`_

        For ``Item`` = SRES, selected result ( :ref:`osresult` ) values are output. See :ref:`PLNSOL_tab_2`.

        .. _plnsol_tab_1:

        PLNSOL - Valid Item and Component Labels
        ****************************************

        .. flat-table:: General Item and Component Labels :ref:`plnsol`, ``Item, Comp``
           :header-rows: 1

           * - Item
             - Comp
             - Description
           * - **Valid item and component labels for nodal degree of freedom results are:**
           * - U
             - X, Y, Z, SUM
             - X, Y, or Z structural displacement or vector sum.
           * - ROT
             - X, Y, Z, SUM
             - X, Y, or Z structural rotation or vector sum.
           * - TEMP For ``SHELL131`` and ``SHELL132`` elements with KEYOPT(3) = 0 or 1, use the labels TBOT, TE2, TE3, ..., TTOP instead of TEMP to view the individual temperature degree of freedom. When other thermal elements are included in the model, deselect them to avoid plotting undefined information. To view all temperatures in the same plot, set :ref:`eshape` ,1 and :ref:`graphics`,POWER and issue :ref:`plnsol`,TEMP.
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
           * - CONC
             -
             - Concentration. Not supported by PowerGraphics.
           * - V
             - X, Y, Z, SUM
             - X, Y, or Z fluid velocity or vector sum in a fluid analysis.
           * - A
             - X, Y, Z, SUM
             - X, Y, or Z magnetic vector potential or vector sum in an electromagnetic analysis.
           * - VEL
             - X, Y, Z, SUM
             - X, Y, or Z velocity or vector sum in a structural transient dynamic analysis ( :ref:`antype`,TRANS).
           * - ACC
             - X, Y, Z, SUM
             - X, Y, or Z acceleration or vector sum in a structural transient dynamic analysis ( :ref:`antype`,TRANS).
           * - OMG
             - X, Y, Z, SUM
             - X, Y, or Z rotational velocity or vector sum in a structural transient dynamic analysis ( :ref:`antype`,TRANS).
           * - DMG
             - X, Y, Z, SUM
             - X, Y, or Z rotational acceleration or vector sum in a structural transient dynamic analysis ( :ref:`antype`,TRANS).
           * - WARP
             -
             - Warping.
           * - :rspan:`1` NRRE
             - FX, FY, FZ, FNRM, MX, MY, MZ, MNRM
             - Plot the Newton-Raphson residuals from the file you obtained via the :ref:`nldiag`,NRRE,ON command. The FNRM and MNRM labels are computed as the square root of the sum of the squares of the residual component forces or moments (FX,FY,FZ, MX, MY, MZ). When plotting Newton-Raphson residual items ( ``Item`` = NRRE) from a file on the deformed geometry, the displacements are based on the current set of results in the database. These displacements may not correspond to the loadstep and substep in the :file:`.nrxxxxx` file. (For more information about :file:`.nrxxxxx` files and nonlinear diagnostics postprocessing, see the description of the :ref:`nldpost` command and.)
           * - SPL
             -
             - Sound pressure level.
           * - SPLA
             -
             - A-weighted sound pressure level (dBA).
           * - VNS
             -
             - Normal velocity on the structural surface. Valid only for ``SHELL181``, ``SOLID185``, ``SOLID186``, ``SOLID187``, ``SOLSH190``, and ``SHELL281``.
           * - ENKE
             -
             - Acoustic diffusion energy density
           * - **Valid item and component labels for element results are:**
           * - :rspan:`3` S
             - X, Y, Z, XY, YZ, XZ
             - Component stress. This item plots the solution using `nodal-averaged results <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_CH2_2.html#nodeavepost>`_ if they are available on the results file.
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
           * - INT
             - Diffusion strain intensity.
           * - EQV
             - Diffusion equivalent strain.
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
             - Component total mechanical strain (EPEL + EPPL + EPCR).
           * - 1, 2, 3
             - Principal total mechanical strain.
           * - INT
             - Total mechanical strain intensity.
           * - EQV
             - Total mechanical equivalent strain.
           * - :rspan:`3` EPTT
             - X, Y, Z, XY, YZ, XZ
             - Component total mechanical, thermal, diffusion, and swelling strain (EPEL + EPPL + EPCR + EPTH + EPDI + EPSW).
           * - 1, 2, 3
             - Principal total, mechanical, thermal, diffusion, and swelling strain.
           * - INT
             - Total mechanical, thermal, diffusion, and swelling strain intensity.
           * - EQV
             - Total mechanical, thermal, diffusion, and swelling equivalent strain.
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
           * - :rspan:`13` FAIL
             - MAX
             - Maximum of all active failure criteria defined at the current location. (See :ref:`fctyp`.)  Works only if failure criteria are provided ( :ref:`fc` and :ref:`tb` ).
           * - EMAX
             - Maximum Strain Failure Criterion.
           * - SMAX
             - Maximum Stress Failure Criterion.
           * - TWSI
             - Tsai-Wu Strength Index Failure Criterion.
           * - TWSR
             - Inverse of Tsai-Wu Strength Ratio Index Failure Criterion.
           * - HFIB
             - Hashin Fiber Failure Criterion.   Must first be added ( :ref:`fctyp` ).
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
           * - USR1, USR2,..., USR9
             - User-defined failure criteria.    USR1 through USR9 require a failure-criteria routine.
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
           * - SVAR
             - 1, 2, 3,... N
             - State variable.
           * - GKS
             - X, XY, XZ
             - Gasket component stress.
           * - GKD
             - X, XY, XZ
             - Gasket component total closure.
           * - GKDI
             - X, XY, XZ
             - Gasket component total inelastic closure.
           * - GKTH
             - X, XY, XZ
             - Gasket component thermal closure.
           * - SS
             - X, XY, XZ
             - Interface traction (stress).
           * - SD
             - X, XY, XZ
             - Interface separation.
           * - FICT
             - TEMP
             - Fictive temperature.
           * - :rspan:`9` CONT For contact results, PowerGraphics is supported for 3D models only.   For the CONT items for elements ``CONTA172``, ``CONTA174``, ``CONTA175``, and ``CONTA177``, the reported data is averaged across the element. To obtain a more meaningful STAT value, use :ref:`plesol`.
             - STAT
             - Contact status For MPC-based contact definitions, the value of STAT can be negative, indicating that one or more contact constraints were intentionally removed to prevent overconstraint. STAT = -3 is used for MPC bonded contact; STAT = -2 is used for MPC no-separation contact.   :   * 3 = closed and sticking * 2 = closed and sliding * 1 = open but near contact * 0 = open and not near contact
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
           * - TG ``Comp`` = SUM is not supported for coupled pore-pressure-thermal (CPT ``nnn`` ) elements.
             - X, Y, Z, SUM
             - Component thermal gradient or vector sum.
           * - TF
             - X, Y, Z, SUM
             - Component thermal flux or vector sum.
           * - PG
             - X, Y, Z, SUM
             - Component or vector sum of velocity or energy density flux (room acoustics).
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
           * - CAP
             - C0,X0,K0,ZONE, DPLS,VPLS
             - Material cap plasticity model only: Cohesion; hydrostatic compaction yielding stress; I1 at the transition point at which the shear and compaction envelopes intersect; zone = 0: elastic state, zone = 1: compaction zone, zone = 2: shear zone, zone = 3: expansion zone; effective deviatoric plastic strain; volume plastic strain.
           * - EDPC
             - CSIG,CSTR
             - Material EDP creep model only (not including the cap model): Equivalent creep stress; equivalent creep strain.
           * - FFLX
             - X,Y,Z
             - Fluid flow flux in poromechanics.
           * - FGRA
             - X,Y,Z
             - Fluid pore-pressure gradient in poromechanics.
           * - FMAG
             - X, Y, Z, SUM
             - Component electromagnetic force or vector sum.
           * - JC
             - X, Y, Z, SUM
             - Conduction current density for elements that support conduction current calculation. Components (X, Y, Z) and vector sum (SUM).
           * - BFE
             - TEMP
             - Body temperatures (calculated from applied temperatures) as used in solution (area and volume elements only).
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
           * - SNDI
             - X, Y, Z, SUM
             - Component sound intensity or vector sum.
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


        .. _PLNSOL_tab_2:

        PLNSOL - Selected Result Component Labels
        *****************************************

        .. flat-table:: Selected Result Component Labels :ref:`plnsol`,SRES, ``Comp``
           :header-rows: 1

           * - Comp
             - Description
           * - SVAR ``n``
             - The ``n`` th state variable.
           * - FLDUF0 ``n``
             - The ``n`` th user-defined field variable.
        """
        command = f"PLNSOL,{item},{comp},{kund},{fact},{fileid},{avg},{datakey}"
        return self.run(command, **kwargs)

    def plorb(self, **kwargs):
        r"""Displays the orbital motion of a rotating structure

        Mechanical APDL Command: `PLORB <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PLORB.html>`_

        Notes
        -----
        When a structure is rotating and the Coriolis or gyroscopic effect is taken into account (
        :ref:`coriolis` ), nodes lying on the rotation axis generally exhibit an elliptical orbital motion.
        The :ref:`plorb` command displays the `orbit
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_rot/Hlp_G_ROTTERMINOLOGY.html#rotgloss1>`_
        of each rotating node as well as the deformed shape at time t = 0 (the real part of the solution).

        To print the characteristics of the orbital path traversed by each node, issue the :ref:`prorb`
        command.

        The :ref:`plorb` command is valid for line elements (such as ``BEAM188``, ``BEAM189``, ``PIPE288``,
        and ``PIPE289`` ). :ref:`plorb` is not supported for beam elements with the warping degree of
        freedom activated.

        Your model must also involve a rotational velocity ( :ref:`omega` or :ref:`cmomega` ) with Coriolis
        enabled ( :ref:`coriolis` ).

        Because orbit data is written in the database, a :ref:`set` command must be issued after the
        :ref:`plorb` command to ensure proper output for subsequent postprocessing commands.

        The coordinate system for displaying nodal results must be global Cartesian ( :ref:`rsys`, ``KCN`` =
        0). :ref:`plorb` is not supported if nodes are rotated in a cylindrical coordinate system.
        """
        command = "PLORB"
        return self.run(command, **kwargs)

    def plvect(
        self,
        item: str = "",
        lab2: str = "",
        lab3: str = "",
        labp: str = "",
        mode: str = "",
        loc: str = "",
        edge: str = "",
        kund: int | str = "",
        **kwargs,
    ):
        r"""Displays results as vectors.

        Mechanical APDL Command: `PLVECT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PLVECT.html>`_

        Parameters
        ----------
        item : str
            Predefined vector item (from :ref:`plvect_tab_1` below) or a label identifying the i-component
            of a user-defined vector.

        lab2 : str
            Label identifying the j-component of a user-defined vector. In most cases, this value must be
            blank if ``Item`` is selected from :ref:`plvect_tab_1`. Individual principal stresses ( ``Item``
            = S) or principal strains ( ``Item`` = EP ``xx`` ) may be plotted by specifying the value as 1,
            2, or 3.

        lab3 : str
            Label identifying the k-component of a user-defined vector. Must be blank if ``Item`` is
            selected from list below or for 2D user defined vector.

        labp : str
            Label assigned to resultant vector for display labeling (defaults to ``Item`` ).

        mode : str
            Vector or raster mode override key:

            * ``(blank)`` - Use the setting of ``KEY`` on the :ref:`device` command.

            * ``RAST`` - Use raster mode for :ref:`plvect` displays.

            * ``VECT`` - Use vector mode for :ref:`plvect` displays.

        loc : str
            Vector location for display of field element results:

            * ``ELEM`` - Display at element centroid (default).

            * ``NODE`` - Display at element nodes.

            Nodal results quantities will only be displayed at nodes, not at element centroids.

        edge : str
            Edge display override key:

            * ``(blank)`` - Use the setting of Key on the :ref:`edge` command.

            * ``OFF`` - Deactivate the edge display.

            * ``ON`` - Activate the edge display.

        kund : int or str
            Undisplaced shape key:

            * ``0`` - Display vectors on undeformed mesh or geometry.

            * ``1`` - Display vectors on deformed mesh or geometry.

        Notes
        -----

        .. _PLVECT_notes:

        Displays various solution results as vectors (arrows) for the selected nodes and/or elements
        (elements must contain at least three nodes that are not colinear). For example, :ref:`plvect`,U
        displays the displacement vector for all selected nodes. For section displays ( :ref:`slashtype` ),
        the vectors are shown only on the section face (that is, cutting plane). The :ref:`plvect` display
        of principal strains and stresses ( ``Item`` = S, EPTO, EPEL, EPPL, EPCR, or EPTH) on a "cut" of the
        model ( :ref:`slashtype`,,1,5,7,8, or 9) is not supported. The resulting plot displays the vectors
        on all selected elements, not on just the sliced surface. See the :ref:`vscale` command to scale
        vector lengths. Vector magnitudes may be shown as a contour display with the :ref:`plnsol` command.
        Various results also depend upon the recalculation method and the selected results location (
        :ref:`layer`, :ref:`shell`, and :ref:`nsel` ).

        Items may be selected from a set of recognized vector labels ( ``Item`` ) or a vector may be defined
        from up to three scalar labels ( ``Item``, ``Lab2``, ``Lab3`` ). Scalar labels may be user-defined
        with the :ref:`etable` command. The vectors appear on an element display as arrows showing the
        relative magnitude of the vector and its direction. The predefined items will be shown either at the
        node or at the element centroid, depending on what item is being displayed and depending on the
        ``Loc`` setting. User defined :ref:`etable` items will be shown at the element centroid, regardless
        of the ``Loc`` setting. Stress vectors appear as arrows at the element centroid, with the arrowheads
        pointing away from each other for tension and toward each other for compression.

        For PowerGraphics, vector arrow displays are generated in Global Cartesian ( :ref:`rsys` = 0). All
        subsequent displays will revert to your original coordinate system.

        When vector mode is active ( ``Mode`` = VECT), use the Z-buffered display type ( :ref:`slashtype`
        ,,6) to maximize speed of :ref:`plvect` plots (other hidden display types may make plotting slow).
        For PowerGraphics ( :ref:`graphics`,POWER), the items marked with [ :ref:`plvect_tab3-43note1` ] are
        not supported by PowerGraphics.

        It is possible to plot principal stresses ( ``Item`` = S) or principal strains ( ``Item`` = EP
        ``xx`` ) individually. To do so, specify a ``Lab2`` value of 1, 2, or 3. For example, the following
        are valid commands:

        * :ref:`plvect`,S,1,,,VECT,ELEM,ON,0
        * :ref:`plvect`,EPEL,3,,,VECT,NODE,ON,0

        .. _plvect_tab_1:

        PLVECT - Valid Item Labels
        **************************

        .. flat-table::
           :header-rows: 1

           * - Item
             - Description
           * - **Valid item labels for nodal degree of freedom vector results are:**
           * - U
             - Structural displacement vector.
           * - ROT
             - Structural rotation vector.
           * - V
             - Velocity vector.
           * - A
             - Magnetic vector potential vector.
           * - FFLX
             - Fluid flux in poromechanics.
           * - **Valid item labels for structural element results are:**
           * - S
             - Principal stresses [ :ref:`plvect_tab3-43note1` ].
           * - EPTO
             - Principal total strain (EPEL + EPPL + EPCR) [ :ref:`plvect_tab3-43note1` ].
           * - EPEL
             - Principal elastic strains [ :ref:`plvect_tab3-43note1` ].
           * - EPPL
             - Principal plastic strains [ :ref:`plvect_tab3-43note1` ].
           * - EPCR
             - Principal creep strains [ :ref:`plvect_tab3-43note1` ].
           * - EPTH
             - Principal thermal strains [ :ref:`plvect_tab3-43note1` ].
           * - EPDI
             - Principal diffusion strains [ :ref:`plvect_tab3-43note1` ].
           * - **Valid item labels for field element results are:**
           * - TG
             - Thermal gradient vector.
           * - TF
             - Thermal flux vector.
           * - PG
             - Velocity vector or energy density flux vector (room acoustics).
           * - EF
             - Electric field vector.
           * - D
             - Electric flux density vector.
           * - H
             - Magnetic field intensity vector. If Lab2 is blank, Item is interpreted as one of the predefined labels; otherwise, Item is interpreted as a user-defined :ref:`et` label and the program requests a nonblank Lab2 / Lab3 according to the dimension of the problem.
           * - B
             - Magnetic flux density vector.
           * - CG
             - Concentration gradient vector.
           * - DF
             - Diffusion flux density vector.
           * - FMAG
             - Electromagnetic force vector.
           * - P
             - Poynting vector.
           * - JS
             - Source current density vector for low-frequency magnetic analyses. Total current density vector (sum of conduction and displacement current densities) in low frequency electric analyses.
           * - JT
             - Total measurable current density vector in low-frequency electromagnetic analyses. (Conduction current density vector in a low-frequency electric analysis.)
           * - JC
             - Conduction current density vector for elements that support conduction current calculation.
           * - SNDI
             - Sound intensity vector [ :ref:`plvect_tab3-43note1` ].

        .. _plvect_tab3-43note1:

        Not supported by PowerGraphics
        """
        command = f"PLVECT,{item},{lab2},{lab3},{labp},{mode},{loc},{edge},{kund}"
        return self.run(command, **kwargs)

    def prcint(self, id_: str = "", node: str = "", dtype: str = "", **kwargs):
        r"""Lists fracture parameter ( :ref:`cint` ) results data.

        Mechanical APDL Command: `PRCINT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PRCINT.html>`_

        Parameters
        ----------
        id_ : str
            Crack ID number.

        node : str
            Crack tip node number. Default = ALL. Valid only for 3D analysis.

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

            * ``TSTRESS`` - T-stress

            * ``CEXT`` - Crack extension

            * ``CSTAR`` - C\2-integral

            * ``STTMAX`` - Maximum circumferential stress

            * ``PSMAX`` - Maximum circumferential stress when :math:`equation not available`

            * ``DLTA`` - Incremental crack extension in a `fatigue crack-growth analysis
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/fracfcgxfem.html#fracfcgxfemexample>`_

            * ``DLTN`` - Number of incremental cycles in a fatigue crack-growth analysis

            * ``DLTK`` - Equivalent stress intensity factors in a fatigue crack-growth analysis

            * ``R`` - Stress (load) ratio in a fatigue crack-growth analysis

            * ``UFAC`` - U-factor (crack closure) in a fatigue crack-growth analysis

            * ``CRDX`` - X coordinate of the crack tip

            * ``CRDY`` - Y coordinate of the crack tip

            * ``CRDZ`` - Z coordinate of the crack tip

            * ``APOS`` - Position attribute of the crack-tip node:

              * ``Positive integer`` - The subcrack Subcracks typically appear in `SMART
                <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/fracSMART.html#fracsmartexample>`_
                crack-growth analyses and are uncommon in other types of fracture analyses.

                 ID number to which this tip belongs. For a crack with only a single subcrack, this value is 1.

              * ``Negative integer`` - The absolute value of the negative integer is the subcrack ID number to
                which this tip belongs.

                The negative sign indicates that this crack tip is the end of this subcrack, and that this subcrack
                is a closed polygon. It must be connected to the first tip of this subcrack when the crack front is
                plotted.

              For more information, see :ref:`aposexamples`.

        Notes
        -----
        **Examples: APOS Usage**

        .. _aposexamples:

        The following examples show how APOS values Issuing :ref:`get` is an effective way to obtain APOS
        values.

         are applied in several cases for fracture analysis.

        The most common situation is that an open crack exists in ``N`` crack tips, and all tips are
        connected into a single subcrack. The APOS values for each tip are:

        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.

        For a closed crack without extra subcracks, the APOS values are:

        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.

        The following crack has two subcracks, the first open and the second closed. Assuming ``M`` tips on
        the first subcrack and ``N`` tips on the second, the APOS values are:

        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.

        .. _PRCINT_notes:

        When a crack tip node is defined, the values associated with the specified node are listed.

        ``Dtype`` = STTMAX or PSMAX are valid for `phantom-node-based
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/Hlp_G_FRACXFEM.html#fracxfemfig2>`_
        XFEM analyses only.

        ``Dtype`` = CRDX, CRDY, CRDZ, and APOS are valid only in a fatigue/static crack-growth analysis
        using `SMART
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/fracSMART.html#fracsmartexample>`_
        or `singularity-based
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/Hlp_G_FRACXFEM.html#fracxfemfig1>`_
        XFEM.

        ``Dtype`` = DLTA, DLTN, DLTK, R are valid only in a `fatigue crack-growth analysis
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/fracSMART.html#>`_ using `SMART
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/fracSMART.html#fracsmartexample>`_
        or `singularity-based
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/Hlp_G_FRACXFEM.html#fracxfemfig1>`_
        XFEM.

        ``Dtype`` = UFAC is valid only in a fatigue crack-growth analysis using `SMART
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/fracSMART.html#fracsmartexample>`_.
        """
        command = f"PRCINT,{id_},{node},{dtype}"
        return self.run(command, **kwargs)

    def prenergy(
        self,
        energytype: str = "",
        cname1: str = "",
        cname2: str = "",
        cname3: str = "",
        cname4: str = "",
        cname5: str = "",
        cname6: str = "",
        **kwargs,
    ):
        r"""Prints the total energies of a model or the energies of the specified components.

        Mechanical APDL Command: `PRENERGY <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PRENERGY.html>`_

        Parameters
        ----------
        energytype : str
            Type of energies to be printed:

            * ``ALL`` - All energies are printed: potential, kinetic, artificial hourglass/drill stiffness,
              contact stabilization energy, and artificial stabilization energy when applicable. This is the
              default.

            * ``SENE`` - Potential energy (stiffness energy).

            * ``KENE`` - Kinetic energy.

            * ``DENE`` - Damping energy.

            * ``WEXT`` - Work done by external loads.

        cname1 : str
            Component names for energies of the components printout.

            If ``Cname1`` is blank, the total energies are listed.

            If ``Cname1`` = ALL, the energies are listed for all selected components.

            If ``Cname1`` is neither blank nor ALL, it is the name of an existing component. The energies
            are listed for up to 6 selected components named in ``Cname1`` to ``Cname6``.

        cname2 : str
            Component names for energies of the components printout.

            If ``Cname1`` is blank, the total energies are listed.

            If ``Cname1`` = ALL, the energies are listed for all selected components.

            If ``Cname1`` is neither blank nor ALL, it is the name of an existing component. The energies
            are listed for up to 6 selected components named in ``Cname1`` to ``Cname6``.

        cname3 : str
            Component names for energies of the components printout.

            If ``Cname1`` is blank, the total energies are listed.

            If ``Cname1`` = ALL, the energies are listed for all selected components.

            If ``Cname1`` is neither blank nor ALL, it is the name of an existing component. The energies
            are listed for up to 6 selected components named in ``Cname1`` to ``Cname6``.

        cname4 : str
            Component names for energies of the components printout.

            If ``Cname1`` is blank, the total energies are listed.

            If ``Cname1`` = ALL, the energies are listed for all selected components.

            If ``Cname1`` is neither blank nor ALL, it is the name of an existing component. The energies
            are listed for up to 6 selected components named in ``Cname1`` to ``Cname6``.

        cname5 : str
            Component names for energies of the components printout.

            If ``Cname1`` is blank, the total energies are listed.

            If ``Cname1`` = ALL, the energies are listed for all selected components.

            If ``Cname1`` is neither blank nor ALL, it is the name of an existing component. The energies
            are listed for up to 6 selected components named in ``Cname1`` to ``Cname6``.

        cname6 : str
            Component names for energies of the components printout.

            If ``Cname1`` is blank, the total energies are listed.

            If ``Cname1`` = ALL, the energies are listed for all selected components.

            If ``Cname1`` is neither blank nor ALL, it is the name of an existing component. The energies
            are listed for up to 6 selected components named in ``Cname1`` to ``Cname6``.

        Notes
        -----

        .. _PRENERGY_Notes:

        The :ref:`prenergy` command prints out either the total energies of the entire model or the energies
        of the components depending on the ``Cname1`` specification.

        Only existing components based on elements (defined with the :ref:`cm` command) are supported when
        component energies are listed.

        Damping energy (DENE) and work done by external loads (WEXT) are available only if the following
        were set prior to the analysis solution: ``EngCalc`` = YES on the :ref:`trnopt`, :ref:`hrout` or
        :ref:`mxpand` command; and ``Item`` = VENG, ESOL, or ALL on the :ref:`outres` command.

        If ``EngCalc`` = YES on the :ref:`hrout` or :ref:`mxpand` command, average, amplitude, and peak
        values are returned for potential (SENE) and kinetic (KENE) energies.

        The energy values can be retrieved using the :ref:`get` command with ``Entity`` = PRENERGY.

        This command applies to structural elements only.
        """
        command = f"PRENERGY,{energytype},{cname1},{cname2},{cname3},{cname4},{cname5},{cname6}"
        return self.run(command, **kwargs)

    def presol(self, item: str = "", comp: str = "", **kwargs):
        r"""Prints the solution results for elements.

        Mechanical APDL Command: `PRESOL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PRESOL.html>`_

        Parameters
        ----------
        item : str
            Label identifying the item. Valid item labels are shown in the table below. Some items also
            require a component label.

        comp : str
            Component of the item (if required). Valid component labels are shown in the table below.

        Notes
        -----

        .. _PRESOL_notes:

        :ref:`presol` prints the solution results for the selected elements in the sorted sequence.

        For example, :ref:`presol`,S prints the stress items SX, SY, SZ, SXY, SYZ, and SXZ for the node
        locations of the element. Various element results depend on the calculation method ( :ref:`avprin`
        ).

        Component results are in the global Cartesian coordinate directions unless transformed ( :ref:`rsys`
        ).

        Shell elements print values at the top, then bottom of the element (or layer). If KEYOPT(8) = 2 (for
        ``SHELL181``, ``SHELL208``, ``SHELL209``, ``SHELL281``, or ``ELBOW290`` ), the results are printed
        in the order TOP, BOT and then MID of each element, (or layer). The MID value is the actual value to
        the results file.

        Items are listed as columns of a table versus element number. An exception occurs for item ELEM,
        which uses an element format (where all applicable line element results are listed per element)
        instead of a tabular format.

        You can issue :ref:`force` to define which component of the nodal load is to be used (static,
        damping, inertia, or total).

        To print items not available via :ref:`presol` (such as line element results), see :ref:`etable` and
        :ref:`pretab`.

        For PowerGraphics ( :ref:`graphics`,POWER), results are listed only for the element surface. Items
        not supported by PowerGraphics are noted in :ref:`presol_tab_1`.

        The results printed by :ref:`presol` are unaffected by any requested nodal-averaged results (
        :ref:`outres`,NAR). For more information, see `Nodal-Averaged Results
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_CH2_2.html#nodeavepost>`_

        For ``Item`` = SRES, selected result components ( :ref:`osresult` ) are output. See
        :ref:`presol_tab_2`.

        .. _presol_tab_1:

        PRESOL - General Result Item and Component Labels
        *************************************************

        .. flat-table:: General Item and Component Labels :ref:`presol`, ``Item, Comp``
           :header-rows: 1

           * - Item
             - Comp
             - Description
           * - :rspan:`1` S
             - COMP or blank
             - Component (X, Y, Z, XY, YZ, XZ) stresses.
           * - PRIN
             - Principal stresses (1, 2, 3), stress intensity (INT), and equivalent stress (EQV).
           * - :rspan:`1` EPEL
             - COMP or blank
             - Component (X, Y, Z, XY, YZ, XZ) elastic strains.
           * - PRIN
             - Principal elastic strains (1, 2, 3), strain intensity (INT), and equivalent strain (EQV).
           * - :rspan:`1` EPTH
             - COMP or blank
             - Component (X, Y, Z, XY, YZ, XZ) thermal strains.
           * - PRIN
             - Principal thermal strains (1, 2, 3), strain intensity (INT), and equivalent strain (EQV).
           * - :rspan:`1` EPDI
             - COMP or blank
             - Component (X, Y, Z, XY, YZ, XZ) diffusion strains.
           * - PRIN
             - Principal diffusion strains (1, 2, 3), strain intensity (INT), and equivalent strain (EQV).
           * - :rspan:`1` EPPL
             - COMP or blank
             - Component (X, Y, Z, XY, YZ, XZ) plastic strains.
           * - PRIN
             - Principal plastic strains (1, 2, 3), strain intensity (INT), and equivalent strain (EQV).
           * - :rspan:`1` EPCR
             - COMP or blank
             - Component (X, Y, Z, XY, YZ, XZ) creep strains.
           * - PRIN
             - Principal creep strains (1, 2, 3), strain intensity (INT), and equivalent strain (EQV).
           * - EPSW
             -
             - Swelling strain.
           * - :rspan:`1` EPTO
             - COMP or blank
             - Component (X, Y, Z, XY, YZ, XZ) total mechanical strains (EPEL + EPPL + EPCR).
           * - PRIN
             - Principal total mechanical strains (1, 2, 3), strain intensity (INT), and equivalent strain (EQV).
           * - :rspan:`1` EPTT
             - COMP or blank
             - Component (X, Y, Z, XY, YZ, XZ) total mechanical, thermal, diffusion, and swelling strains (EPEL + EPPL + EPCR + EPTH + EPDI + EPSW).
           * - PRIN
             - Principal total mechanical, diffusion, thermal, and swelling strains (1, 2, 3), strain intensity (INT), and equivalent strain (EQV).
           * - NL
             -
             - Nonlinear items (SEPL, SRAT, HPRES, EPEQ, CREQ, PSV, PLWK).
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
           * - FAIL
             -
             - Failure criteria for virgin material. Not supported by PowerGraphics.   Works only if failure criteria are provided ( :ref:`fc` and :ref:`tb` ).   **Default components:** Maximum of all failure criteria defined at current location (MAX), maximum strain (EMAX), maximum stress (SMAX), Tsai-Wu Strength Index (TWSI), inverse of Tsai-Wu Strength Ratio Index (TWSR).   **Other available components:** Hashin Fiber Failure (HFIB), Hashin Matrix Failure (HMAT), Puck Fiber Failure (PFIB), Puck Matrix Failure (PMAT), LaRc03 Fiber Failure (L3FB), LaRc03 Matrix Failure (L3MT), LaRc04 Fiber Failure (L4FB), LaRc04 Matrix Failure (L4MT), and any user-defined failure criteria (USR1 through USR9). USR1 through USR9 require a failure-criteria routine.     Issue :ref:`fctyp` to activate or remove failure criteria.
           * - PFC
             -
             - Failure criteria based on the effective stresses in the damaged material.   **Components:** Maximum of all failure criteria defined at current location (MAX), fiber tensile failure (FT), fiber compressive failure (FC), matrix tensile failure (MT), and matrix compressive (MC).
           * - PDMG
             -
             - Progressive damage parameters.   **Components:** Damage status (STAT, 0 = undamaged, 1 = damaged, 2 = complete damage), fiber tensile damage variable (FT), fiber compressive damage variable (FC), matrix tensile damage variable (MT), matrix compressive damage variable (MC), shear damage variable (S), energy dissipated per unit volume (SED), energy per unit volume due to viscous damping (SEDV).
           * - FCMX
             -
             - Maximum failure criterion over the entire element.   **Components:** Layer number where the maximum occurs (LAY), name of the maximum failure criterion (FC), and value of the maximum failure criterion (VAL).
           * - SVAR
             - 1,2,3,... N
             - State variable.
           * - GKS
             -
             - Gasket component (X, XY, XZ) stress.
           * - GKD
             -
             - Gasket component (X, XY, XZ) total closure.
           * - GKDI
             -
             - Gasket component (X, XY, XZ) total inelastic closure.
           * - GKTH
             -
             - Gasket component (X, XY, XZ) thermal closure.
           * - CONT
             -
             - Contact items (STAT, PENE, PRES, SFRIC, STOT, SLIDE, GAP, FLUX, CNOS, FPRS). See component descriptions in :ref:`plesol`.
           * - TG
             -
             - Component (X, Y, Z) thermal gradients and vector sum (SUM). No vector sum is calculated for coupled pore-pressure-thermal (CPT ``nnn`` ) elements.
           * - TF
             -
             - Component (X, Y, Z) thermal fluxes and vector sum (SUM).
           * - PG
             -
             - Component (X, Y, Z) and vector sum (SUM) for velocity or energy density flux (room acoustics).
           * - EF
             -
             - Component (X, Y, Z) electric fields and vector sum (SUM).
           * - D
             -
             - Component (X, Y, Z) electric flux densities and vector sum (SUM).
           * - H
             -
             - Component (X, Y, Z) magnetic field intensities and vector sum (SUM).
           * - B
             -
             - Component (X, Y, Z) magnetic flux densities and vector sum (SUM).
           * - CG
             -
             - Component concentration gradient or vector sum.
           * - DF
             -
             - Component diffusion flux density or vector sum.
           * - FMAG
             -
             - Component (X, Y, Z) electromagnetic forces and vector sum (SUM).
           * - P
             -
             - Poynting vector components (X, Y, Z) and sum (SUM).
           * - CG
             -
             - Concentration gradient.
           * - F
             -
             - Component (X, Y, Z) structural forces.  Use :ref:`force` for type.   Do not use :ref:`presol` to obtain contact forces for contact elements, as the force values reported may not be accurate for these elements. Use :ref:`etable` instead.
           * - M
             -
             - Component (X, Y, Z) structural moments.
           * - HEAT
             -
             - Heat flow.
           * - FLOW
             -
             - Fluid flow.
           * - AMPS
             -
             - Current flow.
           * - CHRG
             -
             - Charge.
           * - FLUX
             -
             - Magnetic flux.
           * - CSG
             -
             - Component (X, Y, Z) magnetic current segments.
           * - FORC
             -
             - All available force items (F to CSG above). (10 maximum).
           * - RATE
             -
             - Diffusion flow rate.
           * - BFE
             - TEMP For reinforcing elements ``REINF264`` and ``REINF265``, issue :ref:`presol` ,BFE,TEMP to print the intersection-point temperature of each member. You can also print intersection-point temperature gradients ( :ref:`presol`,TG) and intersection-point heat flux ( :ref:`plesol`,TF). For higher- order reinforcing members (generated when using higher-order base elements), the midpoint values are not available for the reinforcing members.
             - Body temperatures (calculated from applied temperatures) as used in solution (area and volume elements only).
           * - ELEM
             -
             - All applicable element results (available only for ``LINK180`` and previous-generation structural line elements).
           * - SERR Some element- and material-type limitations apply. See :ref:`prerr`.
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
           * - STEN
             -
             - Elemental energy dissipation due to `stabilization <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STRUNST.html#>`_.
           * - TENE
             -
             - Thermal heat dissipation or "stiffness" energy. Same as SENE.
           * - KENE
             -
             - Kinetic energy.
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
           * - AENE
             -
             - Artificial energy due to hourglass control/drill stiffness or due to contact stabilization.
           * - JHEAT
             -
             - Element Joule heat generation (coupled-field calculation).
           * - JS
             -
             - Source current density for low-frequency magnetic analyses. Total current density (sum of conduction and displacement current densities) in low frequency electric analyses. Components (X, Y, Z) and vector sum (SUM).
           * - JT
             -
             - Total measurable current density in low-frequency electromagnetic analyses. (Conduction current density in a low-frequency electric analysis.) Components (X, Y, Z) and vector sum (SUM).
           * - JC
             -
             - Conduction current density for elements that support conduction current calculation. Components (X, Y, Z) and vector sum (SUM).
           * - MRE
             -
             - Magnetic Reynolds number.
           * - VOLU
             -
             - Volume of volume element.
           * - CENT
             -
             - Centroid X, Y, or Z location (based on shape function) in the active coordinate system.
           * - LOCI
             -
             - Integration point location.
           * - SMISC
             - ``snum``
             - Element summable miscellaneous data value at sequence number ``snum`` (shown in the Output Data section of each element description).
           * - NMISC
             - ``snum``
             - Element nonsummable miscellaneous data value at sequence number ``snum`` (shown in the Output Data section of each element description).
           * - CAP
             -
             - Material cap plasticity model only: Cohesion (C0); hydrostatic compaction yielding stress (X0); I1 at the transition point at which the shear and compaction envelopes intersect (K0); ZONE = 0: elastic state, ZONE = 1: compaction zone, ZONE = 2: shear zone, ZONE = 3: expansion zone; effective deviatoric plastic strain (DPLS); volume plastic strain (VPLS).
           * - EDPC
             -
             - Material EDP creep model only (not including the cap model): Equivalent creep stress (CSIG); equivalent creep strain (CSTR).
           * - FICT
             - TEMP
             - Fictive temperature.
           * - :rspan:`3` ESIG
             - COMP or blank
             - Components of Biot``s effective stress.
           * - PRIN
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
             - COMP
             - Fluid flow flux components in poromechanics.
           * - FGRA
             - COMP
             - Fluid pore-pressure gradient components in poromechanics.
           * - MENE
             -
             - Acoustic potential energy.
           * - PMSV
             - COMP
             - Void volume ratio, pore pressure, degree of saturation, and relative permeability for coupled pore-pressure CPT elements.
           * - FPIDX
             - TF01,SF01, TF02,SF02, TF03,SF03, TF04,SF04
             - Failure plane surface activity status for concrete and joint rock material models: 1 = yielded, 0 = not yielded. Tension and shear failure status are available for all four sets of failure planes.
           * - YSIDX
             - TENS,SHEA
             - Yield surface activity status for Mohr-Coulomb, soil, concrete, and joint rock material models: 1 = yielded, 0 = not yielded.
           * - NS
             - COMP
             - `Nominal strain <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_mat5.html#eq4dc2eb28-41da-4d81-b0d0-8716ce41a6e1>`_ for hyperelastic material, reported in the current configuration (unaffected by :ref:`rsys` ).
           * - MPLA
             - DMAC,DMAX
             - Microplane damage, macroscopic and maximum values.
           * - MPDP
             -
             - Microplane homogenized total, tension, and compression damages (TOTA, TENS, COMP), and split weight factor (RW).
           * - DAMAGE
             -
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
           * - SNDI
             -
             - Component (X, Y, Z) sound intensity and vector sum (SUM).
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


        .. _presol_tab_2:

        PRESOL - Selected Result Component Labels
        *****************************************

        .. flat-table:: Selected Result Component Labels :ref:`presol`,SRES, ``Comp``
           :header-rows: 1

           * - Comp
             - Description
           * - SVAR ``n``
             - The ``n`` th state variable.
           * - FLDUF0 ``n``
             - The ``n`` th user-defined field variable.
        """
        command = f"PRESOL,{item},{comp}"
        return self.run(command, **kwargs)

    def prjsol(self, item: str = "", comp: str = "", **kwargs):
        r"""Prints joint element output.

        Mechanical APDL Command: `PRJSOL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PRJSOL.html>`_

        Parameters
        ----------
        item : str
            Label identifying the item. Some items also require a component label.

            * ``DISP`` - Relative displacements.

            * ``ROT`` - Relative rotations.

            * ``VEL`` - Relative linear velocities.

            * ``OMG`` - Relative angular velocities.

            * ``ACC`` - Relative linear accelerations.

            * ``DMG`` - Relative angular accelerations.

            * ``SMISC`` - Summable miscellaneous quantities.

        comp : str
            Component of the item (if required). For ``Item`` = DISP, ROT, VEL, OMG, ACC, and DMG, enter the
            direction label, X, Y, or Z. For ``Item`` = SMISC, enter a valid number.

        Notes
        -----

        .. _PRJSOL_notes:

        Prints element output for the ``MPC184`` joint element. The joint element quantities printed are the
        values for the free or unconstrained relative degrees of freedom.

        Only :ref:`prjsol`,SMISC is available in linear, modal, and linear perturbation analyses.

        This command is valid in POST1 only.
        """
        command = f"PRJSOL,{item},{comp}"
        return self.run(command, **kwargs)

    def prnld(self, lab: str = "", tol: int | str = "", item: str = "", **kwargs):
        r"""Prints the summed element nodal loads.

        Mechanical APDL Command: `PRNLD <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PRNLD.html>`_

        Parameters
        ----------
        lab : str
            Nodal reaction load type. If blank, use the first ten of all available labels. Valid labels are:

            * **Structural force labels** : FX, FY or FZ (forces); F (FX, FY and FZ); MX, MY or MZ (moments); M
              (MX, MY and MZ).
            * **Thermal force labels** : HEAT, HBOT, HE2, HE3,..., HTOP (heat flow).
            * **Fluid force labels** : FLOW (fluid flow); VFX, VFY and VFZ (fluid "forces"); VF (VFX, VFY and
              VFZ).
            * **Electric force labels** : AMPS (current flow); CHRG (charge); CURT (current); VLTG (voltage
              drop).
            * **Magnetic force labels** : FLUX (magnetic flux); CSGZ (magnetic current segment).
            * **Diffusion label** : RATE (diffusion flow rate).

        tol : int or str
            Tolerance value about zero within which loads are not printed, as follows:

            * ``> 0`` - Relative tolerance about zero within which loads are not printed. In this case, the tolerance is ``TOL`` \* ``Load``, where ``Load`` is the absolute value of the maximum load on the selected nodes.

            * ``0`` - Print all nodal loads.

            * ``> 0`` - Absolute tolerance about zero within which loads are not printed.

            Defaults to 1.0E-9 times the absolute value of the maximum load on the selected nodes.

        item : str
            Selected set of nodes.

            * ``(blank)`` - Prints the summed element nodal loads for all selected nodes (default), excluding
              contact elements.

            * ``CONT`` - Prints the summed element nodal loads for contact nodes only.

            * ``BOTH`` - Prints the summed element nodal loads for all selected nodes, including contact nodes.

        Notes
        -----

        .. _PRNLD_notes:

        Prints the summed element nodal loads (forces, moments, heat flows, flux, etc.) for the selected
        nodes in the sorted sequence. Results are in the global Cartesian coordinate directions unless
        transformed ( :ref:`rsys` ). Zero values (within a tolerance range) are not printed. Loads applied
        to a constrained degree of freedom are not included. The :ref:`force` command can be used to define
        which component of the nodal load is to be used (static, damping, inertia, or total).

        By default, :ref:`prnld` excludes elements ``TARGE169`` - ``CONTA177``. Setting ``ITEM`` = CONT will
        only account for nodal forces on selected contact elements ( ``CONTA172``, ``CONTA174``,
        ``CONTA175``, and ``CONTA177`` ). Setting ``ITEM`` = BOTH will account for nodal forces on all
        selected nodes, including contact nodes.

        **Using PRNLD in a Spectrum or PSD Analysis ( ANTYPE, SPECTR)**
        When using :ref:`prnld` in a spectrum analysis (after the combination file has been input through
        :ref:`input`,,MCOM and when :ref:`spopt` has not been issued with ``Elcalc`` = YES during the
        spectrum analysis), or in a PSD analysis when postprocessing 1-sigma results (loadstep 3, 4, or 5),
        the following message will display in the printout header:

        (Spectrum analysis summation is used)

        This message means that the summation of the element nodal forces is performed prior to the
        combination of those forces. In this case, :ref:`rsys` does not apply. The forces are in the nodal
        coordinate systems, and the vector sum is always printed in the global coordinate system.

        The spectrum analysis summation is available when the element results are written to the mode file,
        :file:`Jobname.mode` ( ``MSUPkey`` = Yes on the :ref:`mxpand` command).

        Because modal displacements cannot be used to calculate contact element nodal forces, ``ITEM`` does
        not apply to spectrum and PSD analyses.
        """
        command = f"PRNLD,{lab},{tol},{item}"
        return self.run(command, **kwargs)

    def prnsol(
        self, item: str = "", comp: str = "", avg: str = "", datakey: str = "", **kwargs
    ):
        r"""Prints nodal solution results.

        Mechanical APDL Command: `PRNSOL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PRNSOL.html>`_

        Parameters
        ----------
        item : str
            Label identifying the item. Valid item labels are shown in the table below. Some items also
            require a component label.

        comp : str
            Component of the item (if required). Valid component labels are shown in the table below.
            Default = COMP.

        avg : str
            Specifies whether random acoustic results are averaged. Valid only for ``Item`` = U and PRES.

            * ``(blank)`` - No averaging (default).

            * ``AVG`` - Print averaged results for random acoustics.

        datakey : str
            Key to specify which data is printed:

            * ``AUTO`` - `Nodal-averaged results
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_CH2_2.html#nodeavepost>`_ are
              used if available; otherwise, the element-based data is used, if available. (Default.)

            * ``ESOL`` - Only element-based results are used. If they are not available, the command is ignored.

            * ``NAR`` - Only nodal-averaged results are used. If they are not available, the command is ignored.

        Notes
        -----

        .. _PRNSOL_notes:

        Prints the nodal solution results for the selected nodes in the sorted sequence. For `reinforcing
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/str_compreinfdirectemb.html>`_
        elements (REINF ``nnn`` ), results are printed at intersection points of reinforcing elements and
        base elements.

        For example, :ref:`prnsol`,U,X prints the X component of displacement vector U (that is, the UX
        degree of freedom).

        Component results are in the global Cartesian coordinate directions unless transformed ( :ref:`rsys`
        ).

        Various element results also depend upon the recalculation method and the selected results location
        ( :ref:`avprin`, :ref:`rsys`, :ref:`layer`, :ref:`shell`, and :ref:`nsel` ).

        If :ref:`layer` is issued, the resulting output is listed in full graphics mode (
        :ref:`graphics`,FULL).

        You can define which component of the nodal load (static, damping, inertia, or total) should be used
        ( :ref:`force` ).

        PowerGraphics can affect your nodal solution listings. For PowerGraphics ( :ref:`graphics`,POWER),
        results are listed for the model exterior surfaces only.

        When shell element types are present, results are output on a surface-by-surface basis. For shell
        elements (such as ``SHELL181`` or ``SHELL281`` ), and for ``ELBOW290``, printed output is for both
        the top and bottom surfaces. For solid elements such as ``SOLID185``, the output is averaged for
        each surface and printed as follows:

        * **Node at a vertex:** Three lines are output (one printed line for each surface).

        * **Node on an edge:** Two lines are output (one printed line for each surface).

        * **Nodes on a face:** One value is output.

        * **Nodes interior to the volume:** No printed values are output.

        If a node is common to more than one element, or if a geometric discontinuity exists, several
        conflicting listings may result. For example, a corner node incorporating results from solid
        elements and shell elements could yield as many as nine different results; the printed output would
        be averages at the top and bottom for the three shell surfaces plus averages at the three surfaces
        for the solid, for a total of nine lines of output. The program does not average result listings
        across geometric discontinuities when shell element types are present. It is important to analyze
        the listings at discontinuities to ascertain the significance of each set of data.

        When only `reinforcing
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/str_compreinfdirectemb.html>`_
        elements (REINF ``nnn`` ) are selected, results are listed for intersection points of reinforcing
        elements and base elements. Prints include coordinates of intersection points in global Cartesian
        coordinate system and results. Results are interpolated from the results of base elements. If a
        point is common to more than one reinforcing element, or reinforcing member within one reinforcing
        element, averaged results are printed. Prints also include minimum and maximum values.

        The printed output for full graphics ( :ref:`graphics`,FULL) averages results at the node. For shell
        elements, the default for display is TOP so that the results for the top of the shell are averaged
        with the other elements attached to that node.

        If :ref:`nsort`, :ref:`esort` or :ref:`eshape` is issued with PowerGraphics enabled (
        :ref:`graphics`,POWER), :ref:`prnsol` behaves as though full graphics mode is enabled (
        :ref:`graphics`,FULL).

        Items not supported by PowerGraphics are noted in :ref:`prnsol_tab_1`.

        For ``Item`` = SRES, selected result component ( :ref:`osresult` ) values are output. See
        :ref:`PRNSOL_tab_2`.

        To print midside nodes, first issue :ref:`efacet`,2.

        To learn more about the specific behaviors of :ref:`prnsol` in a cyclic symmetry analysis and
        printing results for nodes at cyclic edges, see `Using the /CYCEXPAND Command
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cycsym/advcycpost.html#>`_

        If `nodal-averaged results
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_CH2_2.html#nodeavepost>`_ (
        :ref:`outres`,NAR or another nodal-averaged label) are in the database, then :ref:`prnsol` uses the
        nodal-averaged data for the applicable items (S, EPEL, EPPL, EPCR, EPTH, EPSW) by default. You can
        change this behavior via the ``DataKey`` argument. Keep these points in mind when using nodal-
        averaged results:

        * The :ref:`layer` and :ref:`rsys`,SOLU commands are not valid with nodal-averaged results. If these
          commands are used, the element solution is printed instead if applicable.

        * Issuing :ref:`esel` before printing nodal-averaged results has no effect on the output.

        * PowerGraphics is supported. The output is equivalent to the full model graphics output, but only
          the appropriate surface nodes are printed. See `Postprocessing Nodal-Averaged Results
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_CH2_2.html#>`_

        .. _prnsol_tab_1:

        PRNSOL - General Result Item and Component Labels
        *************************************************

        .. flat-table:: General Item and Component Labels :ref:`prnsol`, ``Item,Comp``
           :header-rows: 1

           * - Item
             - Comp
             - Description
           * - **Valid item and component labels for nodal degree of freedom results are:**
           * - :rspan:`1` U
             - X, Y, Z
             - X, Y, or Z structural displacement.
           * - COMP
             - X, Y, and Z structural displacements and vector sum.
           * - :rspan:`1` ROT
             - X, Y, Z
             - X, Y, or Z structural rotation.
           * - COMP
             - X, Y, and Z structural rotations and vector sum.
           * - TEMP For ``SHELL131`` and ``SHELL132`` elements with KEYOPT(3) = 0 or 1, use the labels TBOT, TE2, TE3, ..., TTOP instead of TEMP.
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
           * - CONC
             -
             - Concentration. Not supported by PowerGraphics.
           * - :rspan:`1` V
             - X, Y, Z
             - X, Y, or Z fluid velocity in a fluid analysis.
           * - COMP
             - X, Y, and Z fluid velocity and vector sum in a fluid analysis.
           * - :rspan:`1` A
             - X, Y, Z
             - X, Y, or Z magnetic vector potential in an electromagnetic analysis.
           * - COMP
             - X, Y, and Z magnetic vector potential and vector sum in an electromagnetic analysis.
           * - :rspan:`1` VEL
             - X, Y, Z
             - X, Y, or Z velocity in a structural transient dynamic analysis ( :ref:`antype`,TRANS).
           * - COMP
             - X, Y, and Z velocity and vector sum in a structural transient dynamic analysis ( :ref:`antype`,TRANS).
           * - :rspan:`1` ACC
             - X, Y, Z
             - X, Y, or Z acceleration in a structural transient dynamic analysis ( :ref:`antype`,TRANS).
           * - COMP
             - X, Y, and Z acceleration and vector sum in a structural transient dynamic analysis ( :ref:`antype`,TRANS).
           * - :rspan:`1` OMG
             - X, Y, Z
             - X, Y, or Z rotational velocity in a structural transient dynamic analysis ( :ref:`antype`,TRANS).
           * - COMP
             - X, Y, and Z rotational velocity and vector sum in a structural transient dynamic analysis ( :ref:`antype`,TRANS).
           * - :rspan:`1` DMG
             - X, Y, Z
             - X, Y, or Z rotational acceleration in a structural transient dynamic analysis ( :ref:`antype`,TRANS).
           * - COMP
             - X, Y, and Z rotational acceleration and vector sum in a structural transient dynamic analysis ( :ref:`antype`,TRANS).
           * - CURR
             -
             - Current.
           * - EMF
             -
             - Electromotive force drop.
           * - DOF
             -
             - All available degree of freedom labels (10 maximum).
           * - FICT
             - TEMP
             - Fictive temperature.
           * - SPL
             -
             - Sound pressure level.
           * - SPLA
             -
             - A-weighted sound pressure level (dBA).
           * - VNS
             -
             - Normal velocity on the structural surface. Valid only for ``SHELL181``, ``SOLID185``, ``SOLID186``, ``SOLID187``, ``SOLSH190``, and ``SHELL281``.
           * - ENKE
             -
             - Acoustic diffusion energy density
           * - **Valid item and component labels for element results are:**
           * - :rspan:`1` S
             - COMP
             - X, Y, Z, XY, YZ, and XZ component stresses. This item outputs `nodal-averaged results <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_CH2_2.html#nodeavepost>`_ if they are available on the results file.
           * - PRIN
             - S1, S2, S3 principal stresses, SINT stress intensity, and SEQV equivalent stress.
           * - :rspan:`2` EPEL
             - COMP
             - Component elastic strains.
           * - PRIN
             - Principal elastic strains, strain intensity, and equivalent strain.
           * - FAIL
             - Maximum Strain Failure Criteria.  Works only if failure criteria are provided ( :ref:`fc` and :ref:`tb` ).
           * - :rspan:`1` EPTH
             - COMP
             - Component thermal strains.
           * - PRIN
             - Principal thermal strains, strain intensity, and equivalent strain.
           * - :rspan:`1` EPDI
             - COMP
             - Component diffusion strains.
           * - PRIN
             - Principal diffusion strains, strain intensity, and equivalent strain.
           * - :rspan:`1` EPPL
             - COMP
             - Component plastic strains.
           * - PRIN
             - Principal plastic strains, strain intensity, and equivalent strain.
           * - :rspan:`1` EPCR
             - COMP
             - Component creep strains.
           * - PRIN
             - Principal creep strains, strain intensity, and equivalent strain.
           * - EPSW
             -
             - Swelling strain.
           * - :rspan:`1` EPTO
             - COMP
             - Component total mechanical strains (EPEL + EPPL + EPCR).
           * - PRIN
             - Principal total mechanical strains, strain intensity, and equivalent strain.
           * - :rspan:`1` EPTT
             - COMP
             - Component total mechanical, thermal, diffusion, and swelling strains (EPEL + EPPL + EPCR + EPTH + EPDI + EPSW).
           * - PRIN
             - Principal total mechanical, thermal, diffusion, and swelling strains, strain intensity, and equivalent strain.
           * - NL
             -
             - Nonlinear items (SEPL, SRAT, HPRES, EPEQ, CREQ, PSV, PLWK).
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
           * - FAIL
             -
             - Failure criteria.   **Default components:** Maximum of all failure criteria defined at current location (MAX), maximum strain (EMAX), maximum stress (SMAX), Tsai-Wu Strength Index (TWSI), inverse of Tsai-Wu Strength Ratio Index (TWSR).   **Other available components:** Other available components: Hashin Fiber Failure (HFIB), Hashin Matrix Failure (HMAT), Puck Fiber Failure (PFIB), Puck Matrix Failure (PMAT), LaRc03 Fiber Failure (L3FB), LaRc03 Matrix Failure (L3MT), LaRc04 Fiber Failure (L4FB), LaRc04 Matrix Failure (L4MT), and any user-defined failure criteria (USR1 through USR9). USR1 through USR9 require a failure-criteria routine.     Issue :ref:`fctyp` to activate or remove failure criteria.
           * - PFC
             -
             - Failure criteria based on the effective stresses in the damaged material.   **Components:** Maximum of all failure criteria defined at current location (MAX), fiber tensile failure (FT), fiber compressive failure (FC), matrix tensile failure (MT), and matrix compressive (MC).
           * - PDMG
             -
             - Progressive damage parameters.   **Components:** Damage status (STAT, 0 = undamaged, 1 = damaged, 2 = complete damage), fiber tensile damage variable (FT), fiber compressive damage variable (FC), matrix tensile damage variable (MT), matrix compressive damage variable (MC), shear damage variable (S), energy dissipated per unit volume (SED), energy per unit volume due to viscous damping (SEDV).
           * - SVAR Not supported by PowerGraphics.
             - 1, 2, 3,... N
             - State variable.
           * - GKS
             - COMP
             - X, XY, XZ component gasket stress.
           * - GKD
             - COMP
             - X, XY, XZ component gasket total closure.
           * - GKDI
             - COMP
             - X, XY, XZ component gasket total inelastic closure.
           * - GKTH
             - COMP
             - X, XY, XZ component thermal closure.
           * - SS
             - X, XY, XZ
             - Interface traction (stress).
           * - SD
             - X, XY, XZ
             - Interface separation.
           * - CONT
             -
             - Contact items (STAT For contact elements ``CONTA172``, ``CONTA174``, ``CONTA175``, and ``CONTA177``, the reported data are averaged across the element. To obtain a more meaningful STAT value, use :ref:`presol`., PENE, PRES, SFRIC, STOT, SLIDE, GAP, FLUX, CNOS, FPRS). See component descriptions in :ref:`plnsol`.
           * - TG
             - COMP
             - Component thermal gradients and vector sum. No vector sum is calculated for coupled pore-pressure-thermal (CPT ``nnn`` ) elements.
           * - TF
             - COMP
             - Component thermal fluxes and vector sum.
           * - PG
             - COMP
             - Components and vector sum for velocity or energy density flux (room acoustics).
           * - EF
             - COMP
             - Component electric fields and vector sum.
           * - D
             - COMP
             - Component electric flux densities and vector sum.
           * - H
             - COMP
             - Component magnetic field intensities and vector sum.
           * - B
             - COMP
             - Component magnetic flux densities and vector sum.
           * - CG
             - COMP
             - Component concentration gradient or vector sum.
           * - DF
             - COMP
             - Component diffusion flux density or vector sum.
           * - FMAG
             - COMP
             - Component electromagnetic forces and vector sum.
           * - JC
             - COMP
             - Conduction current density for elements that support conduction current calculation. Components (X, Y, Z) and vector sum (SUM).
           * - BFE
             -
             - Body temperatures (calculated from applied temperatures) as used in solution (area and volume elements only).
           * - CAP
             -
             - Material cap plasticity model only: Cohesion (C0); hydrostatic compaction yielding stress (X0); I1 at the transition point at which the shear and compaction envelopes intersect (K0); ZONE = 0: elastic state, ZONE = 1: compaction zone, ZONE = 2: shear zone, ZONE = 3: expansion zone; effective deviatoric plastic strain (DPLS); volume plastic strain (VPLS).
           * - EDPC
             -
             - Material EDP creep model only (not including the cap model): Equivalent creep stress (CSIG); equivalent creep strain (CSTR).
           * - :rspan:`3` ESIG
             - COMP or blank
             - Components of Biot``s effective stress.
           * - PRIN
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
             - COMP
             - Fluid flow flux in poromechanics.
           * - FGRA
             - COMP
             - Fluid pore pressure gradient components in poromechanics.
           * - PMSV
             - COMP
             - Void volume ratio, pore pressure, degree of saturation, and relative permeability for coupled pore-pressure CPT elements.
           * - NS
             - COMP
             - `Nominal strain <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_mat5.html#eq4dc2eb28-41da-4d81-b0d0-8716ce41a6e1>`_ for hyperelastic material, reported in the current configuration (unaffected by :ref:`rsys` ).
           * - MPLA
             - DMAC, DMAX
             - Microplane damage, macroscopic and maximum values.
           * - MPDP
             -
             - Microplane homogenized total, tension, and compression damages (TOTA, TENS, COMP), and split weight factor (RW).
           * - DAMAGE
             -
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
           * - SNDI
             - COMP
             - Component sound intensity and vector sum.
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


        .. _PRNSOL_tab_2:

        PRNSOL - Selected Result Component Labels
        *****************************************

        .. flat-table:: Selected Result Component Labels :ref:`prnsol`,SRES, ``Comp``
           :header-rows: 1

           * - Comp
             - Description
           * - SVAR ``n``
             - The ``n`` th state variable.
           * - FLDUF0 ``n``
             - The ``n`` th user-defined field variable.
        """
        command = f"PRNSOL,{item},{comp},,,,{avg},{datakey}"
        return self.run(command, **kwargs)

    def prorb(self, whrlnodkey: str = "", **kwargs):
        r"""Prints the orbital motion characteristics of a rotating structure

        Mechanical APDL Command: `PRORB <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PRORB.html>`_

        Parameters
        ----------
        whrlnodkey : str
            Flag to print the whirl for each node:

            * ``1 (ON or YES)`` - Print the whirl for each node.

            * ``0 (OFF or NO)`` - No printout. This value is the default.

        Notes
        -----
        When a structure is rotating and the Coriolis or gyroscopic effect is taken into account (
        :ref:`coriolis` ), nodes lying on the rotation axis generally exhibit an elliptical orbital motion.
        The :ref:`prorb` command prints out the `orbit
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_rot/Hlp_G_ROTTERMINOLOGY.html#rotgloss1>`_
        characteristics A, B, PSI, PHI, YMAX, ZMAX, and Whirl of each rotating node, where

        * A is the semi-major axis.
        * B is the semi-minor axis.
        * PSI is the angle between local y axis and major axis.
        * PHI is the angle between initial position (t = 0) and major axis.
        * YMAX is the maximum displacement along local y axis.
        * ZMAX is the maximum displacement along local z axis.
        * Whirl is the direction of an orbital motion (BW for backward whirl and FW for forward whirl).

        Angles PSI and PHI are in degrees and within the range of -180 through +180.

        To display the characteristics of the orbital path traversed by each node, issue the :ref:`plorb`
        command.

        The :ref:`prorb` command is valid for line elements (such as ``BEAM188``, ``BEAM189``, ``PIPE288``,
        and ``PIPE289`` ). :ref:`prorb` is not supported for beam elements with the warping degree of
        freedom activated.

        Your model must also involve a rotational velocity ( :ref:`omega` or :ref:`cmomega` ) with Coriolis
        enabled ( :ref:`coriolis` ).

        Because orbit data is written in the database, a :ref:`set` command must be issued after the
        :ref:`prorb` command to ensure proper output for subsequent postprocessing commands.

        The coordinate system for displaying nodal results must be global Cartesian ( :ref:`rsys`, ``KCN`` =
        0). :ref:`prorb` is not supported if nodes are rotated in a cylindrical coordinate system.
        """
        command = f"PRORB,{whrlnodkey}"
        return self.run(command, **kwargs)

    def prrfor(self, lab: str = "", **kwargs):
        r"""Prints the constrained node reaction solution. Used with the :ref:`force` command.

        Mechanical APDL Command: `PRRFOR <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PRRFOR.html>`_

        Parameters
        ----------
        lab : str
            Nodal reaction load type. If blank, use the first ten of all available labels. Valid labels are:

            * **Structural force labels** : FX, FY or FZ (forces); F (FX, FY and FZ); MX, MY or MZ (moments); M
              (MX, MY and MZ).
            * **Thermal force labels** : HEAT, HBOT, HE2, HE3,..., HTOP (heat flow).
            * **Fluid force labels** : FLOW (fluid flow); VFX, VFY and VFZ (fluid forces); VF (VFX, VFY and
              VFZ).
            * **Electric force labels** : AMPS (current flow); CHRG (charge); CURT (current); VLTG (voltage
              drop).
            * **Magnetic force labels** : FLUX (magnetic flux); CSGZ (magnetic current segment); CURT (current),
              VLTG (voltage drop).
            * **Diffusion labels** : RATE (diffusion flow rate).

        Notes
        -----

        .. _PRRFOR_notes:

        :ref:`prrfor` has the same functionality as the :ref:`prrsol` command; use :ref:`prrfor` instead of
        :ref:`prrsol` when a :ref:`force` command has been issued.

        In a non-spectrum analysis, if either contact or pretension elements exist in the model,
        :ref:`prrfor` uses the :ref:`prrsol` command internally and the :ref:`force` setting is ignored.

        Because modal displacements cannot be used to calculate contact element nodal forces, those forces
        are not included in the spectrum and PSD analyses reaction solution. As a consequence, the
        :ref:`prrfor` command is not supported when constraints on contact element pilot nodes are present.

        :ref:`prrfor` is not valid when using the amplitude or phase results set ( ``KIMG`` = AMPL or PHAS
        on the :ref:`set` command). Use :ref:`prrsol` instead.

        **Using PRRFOR in a Spectrum or PSD Analysis ( ANTYPE,SPECTR)**
        When using :ref:`prrfor` in a spectrum analysis (after the combination file has been input through
        :ref:`input`,,MCOM and when :ref:`spopt` has not been issued with ``Elcalc`` = YES during the
        spectrum analysis), or in a PSD analysis when postprocessing 1-sigma results (loadstep 3, 4, or 5),
        the following message will display in the printout header:

        .. code:: apdl

           (Spectrum analysis summation is used)

        This message means that the summation of the element nodal forces is performed prior to the
        combination of those forces. In this case, :ref:`rsys` does not apply, and the reaction forces are
        in the nodal coordinate systems. Unlike :ref:`prrsol`, which retrieves the forces from the database,
        the :ref:`prrfor` command calculates the forces in the postprocessor.

        The spectrum analysis summation is available when the element results are written to the mode file,
        :file:`Jobname.mode` ( ``MSUPkey`` = Yes on :ref:`mxpand` ).

        The spectrum analysis summation is not available after reading a load case ( :ref:`lcwrite`,
        :ref:`lczero`, :ref:`lcase` ).
        """
        command = f"PRRFOR,{lab}"
        return self.run(command, **kwargs)

    def prrsol(self, lab: str = "", **kwargs):
        r"""Prints the constrained node reaction solution.

        Mechanical APDL Command: `PRRSOL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PRRSOL.html>`_

        Parameters
        ----------
        lab : str
            Nodal reaction load type. If blank, use the first ten of all available labels. Valid labels are:

            * **Structural force labels** : FX, FY or FZ (forces); F (FX, FY and FZ); MX, MY or MZ (moments); M
              (MX, MY and MZ); BMOM (bimoments).
            * **Thermal force labels** : HEAT, HBOT, HE2, HE3,..., HTOP (heat flow).
            * **Fluid force labels** : FLOW (fluid flow); VFX, VFY and VFZ (fluid forces); VF (VFX, VFY and
              VFZ).
            * **Electric force labels** : AMPS (current flow); CHRG (charge); CURT (current); VLTG (voltage
              drop).
            * **Magnetic force labels** : FLUX (magnetic flux); CSGZ (magnetic current segment); CURT (current),
              VLTG (voltage drop).
            * **Diffusion labels** : RATE (diffusion flow rate).

        Notes
        -----

        .. _PRRSOL_notes:

        Prints the constrained node reaction solution for the selected nodes in the sorted sequence. For
        coupled nodes and nodes in constraint equations, the sum of all reactions in the coupled or
        constraint equation set appears at the primary node of the set. Results are in the global Cartesian
        coordinate directions unless transformed ( :ref:`rsys` ).

        :ref:`prrsol` is not valid if any load is applied to a constrained node in the direction of the
        constraint and any of the following is true:

        * :ref:`lcoper` has been used.

        * :ref:`lcase` has been used to read from a load case file.

        * The applied loads and constraints in the database are not the ones used to create the results data
          being processed.

        :ref:`prrsol` provides the total reaction solution (static, plus damping, plus inertial, as
        appropriate based on the analysis type); however, modal reactions include only the static
        contribution.

        Use :ref:`prrfor` instead of :ref:`prrsol` with the :ref:`force` command to obtain only the static,
        damping, or inertial components.

        When using distributed-memory parallel processing, in a spectrum analysis or a PSD analysis
        performed with ``Elcalc`` = YES on the :ref:`spopt` command, use :ref:`prrfor` instead of
        :ref:`prrsol` to print the maximum reaction forces (spectrum analysis) or reaction forces variances
        of 1-σ solutions, as :ref:`prrsol` may lead to more conservative results.
        """
        command = f"PRRSOL,{lab}"
        return self.run(command, **kwargs)

    def prvect(
        self, item: str = "", lab2: str = "", lab3: str = "", labp: str = "", **kwargs
    ):
        r"""Prints results as vector magnitude and direction cosines.

        Mechanical APDL Command: `PRVECT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PRVECT.html>`_

        Parameters
        ----------
        item : str
            Predefined vector item (from :ref:`prvect_tab_1` below) or a label identifying the i-component
            of a user-defined vector.

        lab2 : str
            Label identifying the j-component of a user-defined vector. In most cases, this value must be
            blank if ``Item`` is selected from :ref:`prvect_tab_1`. Individual principal stresses ( ``Item``
            = S) or principal strains ( ``Item`` = EP ``xx`` ) may be printed by specifying the value as 1,
            2, or 3.

        lab3 : str
            Label identifying the k-component of a user-defined vector. Must be blank if ``Item`` is
            selected from list below or for 2D user defined vector.

        labp : str
            Label assigned to resultant vector for printout labeling (defaults to ``Item`` ).

        Notes
        -----

        .. _PRVECT_notes:

        Prints various solution results as vector magnitude and direction cosines for the selected nodes
        and/or elements. For example, :ref:`prvect`,U prints the displacement magnitude and its direction
        cosines for all selected nodes. For nodal degree of freedom vector results, direction cosines are
        with respect to the results coordinate system RSYS. For element results, direction cosines are with
        respect to the global Cartesian system. Item components may be printed with the :ref:`prnsol`
        command. Various results also depend upon the recalculation method and the selected results location
        ( :ref:`layer`, :ref:`shell`, :ref:`nsel`, and :ref:`esel` ). Items may be selected from a set of
        recognized vector labels ( ``Item`` ) or a vector may be defined from up to three scalar labels (
        ``Item``, ``Lab2``, ``Lab3`` ). Scalar labels may be user-defined with the :ref:`etable` command.

        Portions of this command are not supported by PowerGraphics ( :ref:`graphics`,POWER).

        .. _prvect_tab_1:

        PRVECT - Valid Item and Component Labels
        ****************************************

        .. flat-table::
           :header-rows: 1

           * - Item
             - Comp
             - Description
           * - Valid item labels for nodal degree of freedom vector results are:
           * - U
             -
             - Structural displacement vector magnitude and direction cosines.
           * - ROT
             -
             - Structural rotation vector magnitude and direction cosines.
           * - V
             -
             - Velocity vector magnitude and direction cosines.
           * - A
             -
             - Magnetic vector potential vector magnitude and direction cosines.
           * - Valid item labels for element results are:
           * - S
             -
             - Principal stresses and direction cosines.
           * - EPTO
             -
             - Principal total strains (EPEL + EPPL + EPCR) and direction cosines.
           * - EPEL
             -
             - Principal elastic strains and direction cosines.
           * - EPPL
             -
             - Principal plastic strains and direction cosines.
           * - EPCR
             -
             - Principal creep strains and direction cosines.
           * - EPTH
             -
             - Principal thermal strains and direction cosines.
           * - EPDI
             -
             - Principal diffusion strains and direction cosines.
           * - TG
             -
             - Thermal gradient vector sum and direction cosines.
           * - TF
             -
             - Thermal flux vector sum and direction cosines.
           * - PG
             -
             - Velocity or energy density flux (room acoustics) vector sum and direction cosines.
           * - EF
             -
             - Electric field vector sum and direction cosines.
           * - D
             -
             - Electric flux density vector sum and direction cosines.
           * - H
             -
             - Magnetic field intensity vector sum and direction cosines. If ``Lab2`` is blank, Item is interpreted as one of the predefined labels; otherwise, Item is interpreted as a user-defined :ref:`et` label and the program requests a non-blank ``Lab2`` / ``Lab3`` according to the dimension of the problem.
           * - B
             -
             - Magnetic flux density vector sum and direction cosines.
           * - CG
             -
             - Concentration gradient vector sum and direction cosines.
           * - DF
             -
             - Diffusion flux density vector sum and direction cosines.
           * - FMAG
             -
             - Electromagnetic force vector sum and direction cosines.
           * - P
             -
             - Poynting vector sum and direction cosines.
           * - JS
             -
             - Source current density vector sum and direction cosines for low-frequency magnetic analyses. Total current density vector sum and direction cosines (sum of conduction and displacement current densities) in low frequency electric analyses.
           * - JT
             -
             - Total measurable current density vector sum and direction cosines in low-frequency electromagnetic analyses. (Conduction current density vector sum and direction cosines in a low-frequency electric analysis.)
           * - JC
             -
             - Conduction current density vector sum and direction cosines for elements that support conduction current calculation.
           * - SNDI
             -
             - Sound intensity vector sum and direction cosines.
        """
        command = f"PRVECT,{item},{lab2},{lab3},{labp}"
        return self.run(command, **kwargs)

    def sumtype(self, label: str = "", **kwargs):
        r"""Sets the type of summation to be used in the following load case operations.

        Mechanical APDL Command: `SUMTYPE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SUMTYPE.html>`_

        Parameters
        ----------
        label : str
            Summation type

            * ``COMP`` - Combine element component stresses only. Stresses such as average nodal stresses,
              principal stresses, equivalent stresses, and stress intensities are derived from the combined
              element component stresses. Default.

            * ``PRIN`` - Combine principal stress, equivalent stress, and stress intensity directly as stored on
              the results file. Component stresses are not available with this option.

        Notes
        -----

        .. _SUMTYPE_notes:

        Issue :ref:`sumtype`,PRIN when you want to have a load case operation ( :ref:`lcoper` ) act on the
        principal / equivalent stresses instead of the component stresses. Also issue :ref:`sumtype`,PRIN
        when you want to read in load cases ( :ref:`lcase` ). Note that the :ref:`sumtype` setting is not
        maintained between /POS  T1 sessions.

        :ref:`sumtype`,PRIN also causes principal nodal values to be the average of the contributing
        principal element nodal values (see :ref:`avprin`,1).

        ``BEAM188`` and ``BEAM189`` elements compute principal stress, equivalent stress, and stress
        intensity values on request instead of storing them on the results file; :ref:`sumtype`,PRIN does
        not apply for these elements.
        """
        command = f"SUMTYPE,{label}"
        return self.run(command, **kwargs)
