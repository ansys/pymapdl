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


class Piping:

    def bellow(
        self,
        nloc: str = "",
        leng: str = "",
        stiff: str = "",
        flex: str = "",
        elem: str = "",
        **kwargs,
    ):
        r"""Defines a bellows in a piping run.

        Mechanical APDL Command: `BELLOW <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_BELLOW.html>`_

        Parameters
        ----------
        nloc : str
            Node where bellows is to be placed. Defaults to current run starting point (RUN).

        leng : str
            Length of bellows (defaults to average pipe OD).

        stiff : str
            Axial stiffness value (defaults to that of equivalent straight pipe).

        flex : str
            Bending flexibility factor (defaults to 1.0).

        elem : str
            Element number to be assigned to bellows (defaults to the previous maximum element number
            (MAXEL) + 1).

        Notes
        -----

        .. _BELLOW_notes:

        Defines a bellows (straight-pipe element PIPE16 with adjusted specifications and loadings) at a
        given location in a piping run.

        .. warning::

            This command is archived in the latest version of the software.

        """
        command = f"BELLOW,{nloc},{leng},{stiff},{flex},{elem}"
        return self.run(command, **kwargs)

    def bend(
        self,
        nel1: str = "",
        nel2: str = "",
        rad: str = "",
        ndiv: str = "",
        estrt: str = "",
        einc: str = "",
        **kwargs,
    ):
        r"""Defines a bend in a piping run.

        Mechanical APDL Command: `BEND <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_BEND.html>`_

        Parameters
        ----------
        nel1 : str
            Element numbers of the two intersecting straight pipes. Defaults to the last two straight pipe
            elements nearest the intersection of the last two runs.

        nel2 : str
            Element numbers of the two intersecting straight pipes. Defaults to the last two straight pipe
            elements nearest the intersection of the last two runs.

        rad : str
            Bend radius. If LR, use long radius standard (1.5 x nominal diameter) (default). If SR, use
            short radius standard (1.0 x nominal diameter).

        ndiv : str
            Number of divisions (elements) along bend (defaults to 2). A node is generated at the end of
            each division.

        estrt : str
            Number to be assigned to first element of bend (defaults to MAXEL + 1).

        einc : str
            Element number increment (defaults to 1).

        Notes
        -----

        .. _BEND_notes:

        Defines a bend of curved (elbow) pipe elements (PIPE18) in place of the intersection of two
        previously defined straight pipe elements (RUN). Two new nodes are generated at the ends of the bend
        (at the tangency points). A node is also generated at the center of curvature point. The two
        straight pipes are automatically "shortened" to meet the ends of the bend. The bend specifications
        and loadings are taken from the corresponding two straight pipes. The flexibility factors are
        calculated from the internal pressure and EX (evaluated at TAVE) based on the current PPRES and
        PTEMP command specifications when the element is generated.

        .. warning::

            This command is archived in the latest version of the software.

        """
        command = f"BEND,{nel1},{nel2},{rad},{ndiv},{estrt},{einc}"
        return self.run(command, **kwargs)

    def branch(self, node: str = "", x: str = "", y: str = "", z: str = "", **kwargs):
        r"""Defines the starting point for a piping branch.

        Mechanical APDL Command: `BRANCH <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_BRANCH.html>`_

        Parameters
        ----------
        node : str
            Start branch at this node.

        x : str
            Start branch at this location (in the active coordinate system). Used only if ``Node`` is not
            input or input but the node itself is not previously defined. In either case a node is generated
            at this location and assigned the number ``Node`` (or 1 + previous maximum node number if
            ``Node`` is not input).

        y : str
            Start branch at this location (in the active coordinate system). Used only if ``Node`` is not
            input or input but the node itself is not previously defined. In either case a node is generated
            at this location and assigned the number ``Node`` (or 1 + previous maximum node number if
            ``Node`` is not input).

        z : str
            Start branch at this location (in the active coordinate system). Used only if ``Node`` is not
            input or input but the node itself is not previously defined. In either case a node is generated
            at this location and assigned the number ``Node`` (or 1 + previous maximum node number if
            ``Node`` is not input).

        Notes
        -----

        .. _BRANCH_notes:

        Notes
        See the RUN command in :ref:`archlegacycommands` for information about piping models.

        .. warning::

            This command is archived in the latest version of the software.

        """
        command = f"BRANCH,{node},{x},{y},{z}"
        return self.run(command, **kwargs)

    def flange(
        self,
        nloc: str = "",
        leng: str = "",
        mass: str = "",
        sif: str = "",
        flex: str = "",
        arins: str = "",
        elem: str = "",
        **kwargs,
    ):
        r"""Defines a flange in a piping run.

        Mechanical APDL Command: `FLANGE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_FLANGE.html>`_

        Parameters
        ----------
        nloc : str
            Node where flange is to be placed (as described below). Defaults to current piping run starting
            point.

        leng : str
            Length of flange (defaults to larger pipe OD).

        mass : str
            Dry mass (weight/gravity) of flange without insulation (defaults to equivalent straight pipe
            mass). Note that acceleration ( :ref:`acel` ) must be nonzero for weight to be calculated.

        sif : str
            Stress intensification factor (defaults to 1.0).

        flex : str
            Bending flexibility factor (defaults to 1.0).

        arins : str
            Insulation surface area (defaults to equivalent straight pipe insulation area). Units (length
            :sup:`2` ) must be consistent with the smallest unit of the system used (not mixed) regardless
            of the PUNIT option.

        elem : str
            Element number to be assigned to flange (defaults to the previous maximum element number (MAXEL)
            + 1).

        Notes
        -----

        .. _FLANGE_notes:

        Defines a flange (straight-pipe element PIPE16 with adjusted specifications and loadings) at a given
        location in a piping run. (See the RUN command, and other commands described here, in
        :ref:`archlegacycommands`.)

        The FLANGE command is similar to the VALVE command except for a different flexibility factor
        default. The location may be 1) between two adjacent colinear straight pipes, 2) between an adjacent
        straight pipe and a different piping component, or 3) at the end of a straight pipe.

        For Case 1, two new nodes are generated at the ends of the flange. The two straight pipes are
        automatically "shortened" to meet the ends of the flange. The flange specifications and loadings are
        taken from the corresponding two straight pipes.

        For Case 2, one new node is generated at one end of the flange. The straight pipe is automatically
        "shortened" to meet this end of the flange. The other end of the flange meets the other piping
        component. The flange specifications and loadings are taken from the straight pipe.

        For Case 3, one new node is generated at the free end of the flange. The other end of the flange
        meets the straight pipe. The flange specifications and loadings are taken from the straight pipe.

        .. warning::

            This command is archived in the latest version of the software.

        """
        command = f"FLANGE,{nloc},{leng},{mass},{sif},{flex},{arins},{elem}"
        return self.run(command, **kwargs)

    def miter(
        self,
        nel1: str = "",
        nel2: str = "",
        rad: str = "",
        ndiv: str = "",
        estrt: str = "",
        einc: str = "",
        **kwargs,
    ):
        r"""Defines a mitered bend in a piping run.

        Mechanical APDL Command: `MITER <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MITER.html>`_

        Parameters
        ----------
        nel1 : str
            Element numbers of the two intersecting straight pipes. Defaults to the last two straight pipe
            elements nearest the intersection of the last two runs.

        nel2 : str
            Element numbers of the two intersecting straight pipes. Defaults to the last two straight pipe
            elements nearest the intersection of the last two runs.

        rad : str
            Bend radius. If LR, use long radius standard (1.5 x OD) (default). If SR, use short radius
            standard (1.0 x OD).

        ndiv : str
            Number of divisions (elements) along bend (defaults to 2). A node is generated at the end of
            each division.

        estrt : str
            Number to be assigned to first element of bend (defaults to MAXEL + 1).

        einc : str
            Element number increment (defaults to 1).

        Notes
        -----

        .. _MITER_notes:

        Defines a mitered bend of piecewise straight-pipe PIPE16 elements in place of the intersection of
        two previously defined straight pipe elements (RUN). This command is similar to the BEND command
        except that straight pipe elements are used to form the bend instead of curved (elbow) elements.
        (See the RUN and BEND command descriptions in :ref:`archlegacycommands`.)

        .. warning::

            This command is archived in the latest version of the software.

        """
        command = f"MITER,{nel1},{nel2},{rad},{ndiv},{estrt},{einc}"
        return self.run(command, **kwargs)

    def pcorro(self, ctk: str = "", **kwargs):
        r"""Specifies the allowable exterior corrosion thickness for a piping run.

        Mechanical APDL Command: `PCORRO <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PCORRO.html>`_

        Parameters
        ----------
        ctk : str
            Allowable corrosion thickness.

        Notes
        -----

        .. _PCORRO_notes:

        Specifies the allowable exterior corrosion thickness for a piping run. (See the RUN command
        description in :ref:`archlegacycommands`.)

        .. warning::

            This command is archived in the latest version of the software.

        """
        command = f"PCORRO,{ctk}"
        return self.run(command, **kwargs)

    def pdrag(
        self,
        px1: str = "",
        py1: str = "",
        pz1: str = "",
        h1: str = "",
        px2: str = "",
        py2: str = "",
        pz2: str = "",
        h2: str = "",
        kcord: str = "",
        **kwargs,
    ):
        r"""Defines the external fluid drag loading for a piping run.

        Mechanical APDL Command: `PDRAG <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PDRAG.html>`_

        Parameters
        ----------
        px1 : str
            External fluid drag pressure (global Cartesian components) at height ``H1``.

        py1 : str
            External fluid drag pressure (global Cartesian components) at height ``H1``.

        pz1 : str
            External fluid drag pressure (global Cartesian components) at height ``H1``.

        h1 : str
            Height (along ``Kcord`` coordinate) for first drag pressure.

        px2 : str
            External fluid drag pressure (global Cartesian components) at height ``H2``.

        py2 : str
            External fluid drag pressure (global Cartesian components) at height ``H2``.

        pz2 : str
            External fluid drag pressure (global Cartesian components) at height ``H2``.

        h2 : str
            Height (along ``Kcord`` coordinate) for second drag pressure.

        kcord : str
            Coordinate direction for height value (in the global Cartesian coordinate system):

            * ``X`` - X coordinate.

            * ``Y`` - Y coordinate (default).

            * ``Z`` - Z coordinate.

        Notes
        -----

        .. _PDRAG_notes:

        Defines the external fluid drag loading (pressure) as a function of height for a piping run. (See
        the RUN command description in :ref:`archlegacycommands`.) The element drag pressure is determined
        from the centroid height and linear interpolation. Pressures are assigned to the elements as they
        are generated.

        .. warning::

            This command is archived in the latest version of the software.

        """
        command = f"PDRAG,{px1},{py1},{pz1},{h1},{px2},{py2},{pz2},{h2},{kcord}"
        return self.run(command, **kwargs)

    def pfluid(self, dens: str = "", **kwargs):
        r"""Defines the contained fluid density for a piping run.

        Mechanical APDL Command: `PFLUID <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PFLUID.html>`_

        Parameters
        ----------
        dens : str
            Density of the contained fluid.

        Notes
        -----

        .. _PFLUID_notes:

        See the RUN command description in :ref:`archlegacycommands`.

        .. warning::

            This command is archived in the latest version of the software.

        """
        command = f"PFLUID,{dens}"
        return self.run(command, **kwargs)

    def pgap(
        self,
        nloc: str = "",
        k: str = "",
        dx: str = "",
        dy: str = "",
        dz: str = "",
        gap: str = "",
        elem: str = "",
        **kwargs,
    ):
        r"""Defines a spring-gap constraint in a piping run.

        Mechanical APDL Command: `PGAP <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PGAP.html>`_

        Parameters
        ----------
        nloc : str
            Node where gap is to be placed. Defaults to current run starting point.

        k : str
            Spring constant value (must be positive).

        dx : str
            Increment (in terms of the active coordinate system components) to determine gap ground point.
            Element length must not be zero. Constraints are automatically generated at the ground point.

        dy : str
            Increment (in terms of the active coordinate system components) to determine gap ground point.
            Element length must not be zero. Constraints are automatically generated at the ground point.

        dz : str
            Increment (in terms of the active coordinate system components) to determine gap ground point.
            Element length must not be zero. Constraints are automatically generated at the ground point.

        gap : str
            Gap size (defaults to the element length).

        elem : str
            Element number to be assigned to gap (defaults to MAXEL + 1).

        Notes
        -----

        .. _PGAP_notes:

        Defines a spring-gap constraint (gap element CONTAC52) at a given location in a piping run. Gives
        spring constraint resistance after a specified gap is closed. (See the RUN command description in
        :ref:`archlegacycommands`.)

        .. warning::

            This command is archived in the latest version of the software.

        """
        command = f"PGAP,{nloc},{k},{dx},{dy},{dz},{gap},{elem}"
        return self.run(command, **kwargs)

    def pinsul(self, dens: str = "", itk: str = "", **kwargs):
        r"""Defines the external insulation constants in a piping run.

        Mechanical APDL Command: `PINSUL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PINSUL.html>`_

        **Command default:**

        .. _PINSUL_default:

        No insulation.

        Parameters
        ----------
        dens : str
            Insulation density.

        itk : str
            Insulation thickness.

        Notes
        -----

        .. _PINSUL_notes:

        Defines the external insulation constants in a piping run. (See the RUN command description in
        :ref:`archlegacycommands`.)

        .. warning::

            This command is archived in the latest version of the software.

        """
        command = f"PINSUL,{dens},{itk}"
        return self.run(command, **kwargs)

    def popt(self, lop1: str = "", **kwargs):
        r"""Selects the piping analysis standard for a piping run.

        Mechanical APDL Command: `POPT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_POPT.html>`_

        **Command default:**

        .. _POPT_default:

        ANSI B31.1.

        Parameters
        ----------
        lop1 : str
            Option label:

            * ``B31.1`` - for ANSI B31.1.

            * ``NC`` - for ASME Section III NC, Class 2.

        Notes
        -----

        .. _POPT_notes:

        Selects the piping analysis standard for a piping run (RUN). Affects only the flexibility and stress
        intensification factors applied to the curved pipe elements. (See the RUN command description in
        :ref:`archlegacycommands`.)

        .. warning::

            This command is archived in the latest version of the software.

        """
        command = f"POPT,{lop1}"
        return self.run(command, **kwargs)

    def ppres(self, press: str = "", **kwargs):
        r"""Defines the internal pressure for a piping run.

        Mechanical APDL Command: `PPRES <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PPRES.html>`_

        Parameters
        ----------
        press : str
            Pipe internal pressure.

        Notes
        -----

        .. _PPRES_notes:

        Defines the pipe internal pressure for a piping run (RUN). These pressures are assigned to the
        elements as they are generated. (See the RUN command description in :ref:`archlegacycommands`.)

        .. warning::

            This command is archived in the latest version of the software.

        """
        command = f"PPRES,{press}"
        return self.run(command, **kwargs)

    def pspec(
        self,
        mat: str = "",
        dnom: str = "",
        sched: str = "",
        od: str = "",
        tk: str = "",
        **kwargs,
    ):
        r"""Defines pipe material and dimensions.

        Mechanical APDL Command: `PSPEC <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PSPEC.html>`_

        Parameters
        ----------
        mat : str
            Material number referring to a material property [ :ref:`mp` ]. Material number must be between
            1 and 40.

        dnom : str
            Nominal diameter of pipe and schedule rating. Only valid ratings accepted. If these are
            specified, the ``OD`` and ``TK`` values are found from an internal table.

            Valid values for ``DNOM`` are: 1, 1.5, 2, 2.5, 3, 3.5, 4, 5, 6, 8, 10, 12, 14, 16, 18, 20, 22,
            24, 26, 28, 30, 32, 34, and 36.

            Valid ratings for ``SCHED`` are: 5, 5S, 10, 10S, 20, 30, 40, 40S, 60, 80 80S, 100, 120, 140,
            160, XS, XXS, and STD.

        sched : str
            Nominal diameter of pipe and schedule rating. Only valid ratings accepted. If these are
            specified, the ``OD`` and ``TK`` values are found from an internal table.

            Valid values for ``DNOM`` are: 1, 1.5, 2, 2.5, 3, 3.5, 4, 5, 6, 8, 10, 12, 14, 16, 18, 20, 22,
            24, 26, 28, 30, 32, 34, and 36.

            Valid ratings for ``SCHED`` are: 5, 5S, 10, 10S, 20, 30, 40, 40S, 60, 80 80S, 100, 120, 140,
            160, XS, XXS, and STD.

        od : str
            Outer diameter of pipe (if ``DNOM`` not specified). If both ``DNOM`` and ``OD`` are not
            specified, ``OD`` and ``TK`` retain their previous values.

        tk : str
            Wall thickness of pipe (if ``OD`` specified).

        Notes
        -----

        .. _PSPEC_notes:

        Defines pipe material and dimensions. (See the RUN command description in
        :ref:`archlegacycommands`.)

        .. warning::

            This command is archived in the latest version of the software.

        """
        command = f"PSPEC,{mat},{dnom},{sched},{od},{tk}"
        return self.run(command, **kwargs)

    def psprng(
        self,
        nloc: str = "",
        type_: str = "",
        k: str = "",
        dx: str = "",
        dy: str = "",
        dz: str = "",
        elem: str = "",
        **kwargs,
    ):
        r"""Defines a spring constraint in a piping run.

        Mechanical APDL Command: `PSPRNG <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PSPRNG.html>`_

        Parameters
        ----------
        nloc : str
            Node where spring is to be placed. Defaults to current run starting point.

        type_ : str
            Type of spring:

            * ``TRAN`` - Translational (default).

            * ``ROT`` - Rotational.

        k : str
            Spring constant value (must be positive).

        dx : str
            Increment (in terms of the active coordinate system components) to determine spring ground
            point. Spring length must not be zero. Constraints are automatically generated at the ground
            point.

        dy : str
            Increment (in terms of the active coordinate system components) to determine spring ground
            point. Spring length must not be zero. Constraints are automatically generated at the ground
            point.

        dz : str
            Increment (in terms of the active coordinate system components) to determine spring ground
            point. Spring length must not be zero. Constraints are automatically generated at the ground
            point.

        elem : str
            Element number to be assigned to spring (defaults to the previous maximum element number (MAXEL
            + 1)).

        Notes
        -----

        .. _PSPRNG_notes:

        Defines a spring constraint (spring element ``COMBIN14`` ) at a given location in a piping run. (See
        the RUN command description in :ref:`archlegacycommands`.)

        .. warning::

            This command is archived in the latest version of the software.

        """
        command = f"PSPRNG,{nloc},{type_},{k},{dx},{dy},{dz},{elem}"
        return self.run(command, **kwargs)

    def ptemp(self, tout: str = "", tin: str = "", **kwargs):
        r"""Defines the pipe wall temperatures in a piping run.

        Mechanical APDL Command: `PTEMP <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PTEMP.html>`_

        **Command default:**

        .. _PTEMP_default:

        Assign uniform temperature :ref:`bfunif` to elements.

        Parameters
        ----------
        tout : str
            Outer pipe wall temperature. If NONE, reset temperature specification to none ( :ref:`bfunif`
            will be assigned).

        tin : str
            Inner pipe wall temperature (defaults to ``TOUT`` ).

        Notes
        -----

        .. _PTEMP_notes:

        Defines the pipe wall temperatures in a piping run. These temperatures are assigned to the elements
        as they are generated. (See the RUN command description in :ref:`archlegacycommands`.)

        .. warning::

            This command is archived in the latest version of the software.

        """
        command = f"PTEMP,{tout},{tin}"
        return self.run(command, **kwargs)

    def punit(self, kopt: int | str = "", **kwargs):
        r"""Selects the system of length units to be used in a piping run.

        Mechanical APDL Command: `PUNIT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PUNIT.html>`_

        **Command default:**

        .. _PUNIT_default:

        Input units are consistent (no conversions are done).

        Parameters
        ----------
        kopt : int or str
            Units key:

            * ``0`` - Input units are consistent (no conversions are done) (default).

            * ``FTIN or 1`` - English units (feet A, inch B, fraction of inch C/D). Use A+B+C/D format for
              PDRAG, BRANCH, RUN, BEND, MITER, REDUCE, VALVE, BELLOW, FLANGE, PSPRNG, and PGAP commands. Precede
              by "-'' sign for negative coordinates. (Example: 5+6+7/16 for 5 ft. 6-7/16 in., +3 for 3 in., -0+3
              for -3 in., +0+9/16 for 9/16 in.).

              The two signs should not be consecutive. A, B, C, and D must be integers. Use B+C/D format for
              PSPEC, PINSUL, and PCORRO commands. (Example: 2 for 2 in., 3+1/2 for 3-1/2 in., +3/8 for 3/8 in.)

            * ``METRIC or 2`` - Metric units (meter A, centimeter B, fraction of cm C/D). Use as explained for
              English units. (Example: 5+6+7/10 for 5 m 6-7/10 cm with PDRAG command.)

        Notes
        -----

        .. _PUNIT_notes:

        Selects the system of length units to be used for the piping commands. Mixed length units require a
        + sign to delimit (or position) the units in the system and are converted to the smallest unit of
        the system (inches or centimeters) upon input.

        This conversion is local only to pure length units of the piping commands listed. Other units and
        units for other commands must be input to be consistent with the smallest length unit of the system
        used.

        .. warning::

            This command is archived in the latest version of the software.

        """
        command = f"PUNIT,{kopt}"
        return self.run(command, **kwargs)

    def reduce(self, nloc: str = "", leng: str = "", elem: str = "", **kwargs):
        r"""Defines a reducer in a piping run.

        Mechanical APDL Command: `REDUCE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_REDUCE.html>`_

        Parameters
        ----------
        nloc : str
            Node where two straight pipes intersect at center of reducer. Defaults to previous run starting
            point.

        leng : str
            Length of reducer (defaults to average pipe OD).

        elem : str
            Element number to be assigned to reducer (defaults to MAXEL + 1).

        Notes
        -----

        .. _REDUCE_notes:

        Defines a reducer (straight-pipe element PIPE16 with averaged specifications) in place of the
        intersection of two previously defined straight pipe elements in a piping run. (See the RUN command
        description in :ref:`archlegacycommands`.) Two new nodes are generated at the ends of the reducer.
        The two straight pipes are automatically "shortened" to meet the ends of the reducer. The reducer
        specifications and loadings are taken from the corresponding two straight pipes.

        .. warning::

            This command is archived in the latest version of the software.

        """
        command = f"REDUCE,{nloc},{leng},{elem}"
        return self.run(command, **kwargs)

    def run(
        self,
        dx: str = "",
        dy: str = "",
        dz: str = "",
        ndiv: str = "",
        nend: str = "",
        estrt: str = "",
        einc: str = "",
        **kwargs,
    ):
        r"""Defines a pipe run.

        Mechanical APDL Command: `RUN <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_RUN.html>`_

        Parameters
        ----------
        dx : str
            Increment (in terms of the active coordinate system components) to determine run end point.
            Increment is applied to branch starting point (BRANCH) or end point of previous run (whichever
            was later).

        dy : str
            Increment (in terms of the active coordinate system components) to determine run end point.
            Increment is applied to branch starting point (BRANCH) or end point of previous run (whichever
            was later).

        dz : str
            Increment (in terms of the active coordinate system components) to determine run end point.
            Increment is applied to branch starting point (BRANCH) or end point of previous run (whichever
            was later).

        ndiv : str
            Number of divisions (elements) along branch (defaults to 1). A node is generated at the end of
            each division.

        nend : str
            Number to be assigned to end node of branch (defaults to MAXNP + ``NDIV`` ).

        estrt : str
            Number to be assigned to first element of branch (defaults to the previous maximum element
            number (MAXEL) + 1).

        einc : str
            Element number increment (defaults to 1).

        Notes
        -----

        .. _RUN_notes:

        Defines a pipe run from a previous point to an incremental point. Nodes (and elements) are generated
        straight (in the active coordinate system). Elements are of type PIPE16 straight pipes. Material
        properties, real constants, and loads are derived from the previously defined piping specifications.
        Piping loads and specifications are defined via PCORRO, PDRAG, PFLUID, PINSUL, POPT, PPRES, PSPEC,
        PTEMP, and PUNIT commands.

        Generated items may be listed (or displayed) with the standard commands ( :ref:`nlist`,
        :ref:`elist`, :ref:`nplot`, :ref:`eplot`, :ref:`etlist`, :ref:`rlist`, etc.).

        Items may also be modified ( :ref:`nmodif`, :ref:`emodif`, :ref:`rmodif`, etc.) or redefined as
        desired.

        See :ref:`aCcQxq3dbmcm` for more information.

        .. warning::

            This command is archived in the latest version of the software.

        """
        command = f"RUN,{dx},{dy},{dz},{ndiv},{nend},{estrt},{einc}"
        return self.run(command, **kwargs)

    def tee(
        self,
        ncent: str = "",
        type_: str = "",
        elem: str = "",
        einc: str = "",
        l1: str = "",
        l2: str = "",
        l3: str = "",
        **kwargs,
    ):
        r"""Defines a tee in a piping run.

        Mechanical APDL Command: `TEE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/None>`_

        Parameters
        ----------
        ncent : str
            Node where three straight pipes intersect forming a tee (or "Y"). Defaults to last starting
            branch node (BRANCH).

        type_ : str
            Type of tee:

            * ``WT`` - Welding tee (default).

              r = (D:sub:`0` - t:sub:`w` ) / 2

              h = 4.4 t:sub:`w` / r

              SIF = 0.9 / (h :sup:`2/3` )

              If (SIF < 1) SIF = 1

            * ``UFT`` - Unreinforced fabricated tee.

              r = (D:sub:`0` - t:sub:`w` ) / 2

              h = t:sub:`w` / r

              SIF = 0.9 / (h :sup:`2/3` )

              If (SIF < 1) SIF = 1

        elem : str
            Element number to be assigned to first tee leg (defaults to the previous maximum element number
            (MAXEL) + 1).

        einc : str
            Element number increment (defaults to 1).

        l1 : str
            Tee leg lengths (corresponding in order of increasing straight pipe element numbers). Must be
            less than the straight pipe length. Defaults to 2 x OD of straight pipe (for each leg).

        l2 : str
            Tee leg lengths (corresponding in order of increasing straight pipe element numbers). Must be
            less than the straight pipe length. Defaults to 2 x OD of straight pipe (for each leg).

        l3 : str
            Tee leg lengths (corresponding in order of increasing straight pipe element numbers). Must be
            less than the straight pipe length. Defaults to 2 x OD of straight pipe (for each leg).

        Notes
        -----

        .. _TEE_notes:

        Defines a tee in place of the tee intersection of three previously defined straight pipe elements.
        (See the RUN command description in :ref:`archlegacycommands`.)

        The new tee is also composed of three PIPE16 straight pipe elements, but of the leg lengths
        specified and with the appropriate tee factors calculated.

        Three new nodes are generated at the ends of the tee.

        The original three straight pipes are automatically "shortened" to meet the ends of the tee. The tee
        specifications and loadings are taken from the corresponding three straight pipes.

        .. warning::

            This command is archived in the latest version of the software.

        """
        command = f"TEE,{ncent},{type_},{elem},{einc},{l1},{l2},{l3}"
        return self.run(command, **kwargs)

    def valve(
        self,
        nloc: str = "",
        leng: str = "",
        mass: str = "",
        sif: str = "",
        flex: str = "",
        arins: str = "",
        elem: str = "",
        **kwargs,
    ):
        r"""Defines a valve in a piping run.

        Mechanical APDL Command: `VALVE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_VALVE.html>`_

        Parameters
        ----------
        nloc : str
            Node where valve is to be placed (as described below). Defaults to current run starting point.

        leng : str
            Length of valve (defaults to larger pipe OD).

        mass : str
            Dry mass (weight/gravity) of valve without insulation (defaults to equivalent straight pipe
            mass). Note, acceleration ( :ref:`acel` ) must be nonzero for weight to be calculated.

        sif : str
            Stress intensification factor (defaults to 1.0).

        flex : str
            Bending flexibility factor (defaults to 0.5).

        arins : str
            Insulation surface area (defaults to equivalent straight pipe insulation area). Units (length
            :sup:`2` ) must be consistent with the smallest unit of the system used (not mixed) regardless
            of the PUNIT option.

        elem : str
            Element number to be assigned to valve (defaults to the previous maximum element number (MAXEL)
            + 1).

        Notes
        -----

        .. _VALVE_notes:

        Defines a valve (straight-pipe element PIPE16 with adjusted specifications and loadings) at a given
        location in a piping run. (See the RUN command description in :ref:`archlegacycommands`.) The
        location may be 1) between two adjacent colinear straight pipes, 2) between an adjacent straight
        pipe and a different piping component, or 3) at the end of a straight pipe.

        For Case 1, two new nodes are generated at the ends of the valve. The two straight pipes are
        automatically "shortened" to meet the ends of the valve. The valve specifications and loadings are
        taken from the corresponding two straight pipes.

        For Case 2, one new node is generated at one end of the valve. The straight pipe is automatically
        "shortened" to meet this end of the valve. The other end of the valve meets the other piping
        component. The valve specifications and loadings are taken from the straight pipe.

        For Case 3, one new node is generated at the free end of the valve. The other end of the valve meets
        the straight pipe. The valve specifications and loadings are taken from the straight pipe.

        .. warning::

            This command is archived in the latest version of the software.

        """
        command = f"VALVE,{nloc},{leng},{mass},{sif},{flex},{arins},{elem}"
        return self.run(command, **kwargs)
