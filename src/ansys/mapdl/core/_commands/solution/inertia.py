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


class Inertia:

    def acel(self, acel_x: str = "", acel_y: str = "", acel_z: str = "", **kwargs):
        r"""Specifies the linear acceleration of the global Cartesian reference frame for the analysis.

        Mechanical APDL Command: `ACEL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ACEL.html>`_

        Parameters
        ----------
        acel_x : str
            Linear acceleration of the reference frame along global Cartesian X, Y, and Z axes,
            respectively.

        acel_y : str
            Linear acceleration of the reference frame along global Cartesian X, Y, and Z axes,
            respectively.

        acel_z : str
            Linear acceleration of the reference frame along global Cartesian X, Y, and Z axes,
            respectively.

        Notes
        -----

        .. _ACEL_notes:

        In the absence of any other loads or supports, the acceleration of the structure in each of the
        global Cartesian (X, Y, and Z) axes would be equal in magnitude but opposite in sign to that applied
        in the :ref:`acel` command. Thus, to simulate gravity (by using inertial effects), accelerate the
        reference frame with an :ref:`acel` command in the direction opposite to gravity.

        You can define the acceleration for the following analyses types:

        * Static ( :ref:`antype`,STATIC)

        * Harmonic ( :ref:`antype`,HARMIC), full, `VT
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/str_harmsweep.html#>`_ [
          :ref:`ACEL_FN_VT_KRY` ], `Krylov
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/str_Krysweep.html#str_Krylov_macros>`_
          [ :ref:`ACEL_FN_VT_KRY` ], or mode-superposition [ :ref:`ACEL_mode-sup_LoadSupport` ]

        * Transient ( :ref:`antype`,TRANS), `full
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STR5_4.html#strnote11tlm71999>`_
          or mode-superposition [ :ref:`ACEL_mode-sup_LoadSupport` ]

        * Substructure ( :ref:`antype`,SUBSTR).

        .. _ACEL_FN_VT_KRY:

        Loads for VT and Krylov methods are supported as long as they are not:

        * complex tabulated loads (constant or trapezoidal loads in tabulated form are supported)

        * used in conjunction with Rotordynamics ( :ref:`coriolis`,on).

        .. _ACEL_mode-sup_LoadSupport:

        In a mode-superposition harmonic or transient analysis, you must apply the load in the modal portion
        of the analysis. Mechanical APDL calculates a load vector and writes it to the :file:`MODE` file,
        which you
        can apply via the :ref:`lvscale` command.

        For all transient dynamic ( :ref:`antype`,TRANS) analyses, accelerations are combined with the
        element mass matrices to form a body-force load vector term. The element mass matrix may be formed
        from a mass input constant or from a nonzero density (DENS) property, depending upon the element
        type.

        For analysis type :ref:`antype`,HARMIC, the acceleration is assumed to be the real component with a
        zero imaginary component.

        Units of acceleration and mass must be consistent to give a product of force units.

        The :ref:`acel` command supports tabular boundary conditions (``TABNAME_X``, ``TABNAME_Y``, and
        ``TABNAME_Z``) for ``ACEL_X``, ``ACEL_Y``, and ``ACEL_Z`` input values ( :ref:`dim` ) as a function
        of both time and frequency for full transient and harmonic analyses.

        Related commands for rotational effects are :ref:`cmacel`, :ref:`cgloc`, :ref:`cgomga`,
        :ref:`dcgomg`, :ref:`domega`, :ref:`omega`, :ref:`cmomega`, and :ref:`cmdomega`.

        See `Analysis Tools
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/str_EnMoinStAn.html>`_

        This command is also valid in :ref:`prep7`.
        """
        command = f"ACEL,{acel_x},{acel_y},{acel_z}"
        return self.run(command, **kwargs)

    def airl(self, nrb: int | str = "", rigid_calc: int | str = "", **kwargs):
        r"""Specifies that automatic inertia relief calculations are to be performed.

        Mechanical APDL Command: `AIRL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_AIRL.html>`_

        Parameters
        ----------
        nrb : int or str
            Number of rigid body modes in the model:

            * ``AUTO`` - Activate automatic inertia relief (default). The program automatically determines the
              number of rigid body modes.

            * ``n`` - Activate automatic inertia relief with the assumption of ``n`` rigid body modes (1≤ ``n``
              ≤ 6).

            * ``0`` - Deactivate automatic inertia relief.

        rigid_calc : int or str
            Method for computing the rigid body modes:

            * ``0`` - Use an eigensolver to compute rigid body modes (default).

            * ``1`` - Use the geometry to compute rigid body modes (valid only when ``NRB`` = AUTO). The
              geometric rigid body vectors are calculated according to in `Participation Factors and Mode
              Coefficients
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_anproc7.html#eqe483f2f2-aaa1-4080-a835-10c0e1e18f57>`_

        Notes
        -----

        .. _AIRL_notes:

        The :ref:`airl` command activates automatic inertia relief for models having up to six rigid body
        modes. This method is only valid for linear static analyses ( :ref:`antype`,STATIC).

        By default ( ``NRB`` = AUTO), the number of rigid body modes in the structure is automatically
        determined. The static solution is altered so that the inertial effects factor into counterbalancing
        the external loads. This method relies on calculation of the rigid body modes using either an
        eigensolver ( ``RIGID_CALC`` = 0, which is the default) or the model geometry ( ``RIGID_CALC`` = 1).

        For the ``NRB`` = AUTO option, no supports should be defined.

        For a model that is partially constrained by design, you must set ``NRB`` to the number of rigid
        body modes present in the structure and set ``RIGID_CALC`` = 0. The use of geometry ( ``RIGID_CALC``
        = 1) to compute the rigid-body modes of a partially constrained model is not supported.

        Loads may be input as usual. Displacements and stresses are calculated as usual.

        Use :ref:`irlist` to print inertia relief calculation results. The mass and moment of inertia
        summary printed before the solution is accurate (because of the additional pre-calculations required
        for inertia relief). See `Inertia Relief
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_tool2.html#thy_InertiaRelAnalysisTypes>`_
        `Including Inertia Relief Calculations
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/Hlp_G_BAS2_6.html#>`_

        This command is also valid in PREP7.

        **Example Usage**
        Example command input for including automatic inertia relief calculations in a linear static
        analysis is found in `Including Inertia Relief Calculations
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/Hlp_G_BAS2_6.html#>`_
        """
        command = f"AIRL,{nrb},{rigid_calc}"
        return self.run(command, **kwargs)

    def cgloc(self, xloc: str = "", yloc: str = "", zloc: str = "", **kwargs):
        r"""Specifies the origin location of the acceleration coordinate system.

        Mechanical APDL Command: `CGLOC <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CGLOC.html>`_

        Parameters
        ----------
        xloc : str
            Global Cartesian X, Y, and Z coordinates of the acceleration coordinate system origin.

        yloc : str
            Global Cartesian X, Y, and Z coordinates of the acceleration coordinate system origin.

        zloc : str
            Global Cartesian X, Y, and Z coordinates of the acceleration coordinate system origin.

        Notes
        -----

        .. _CGLOC_notes:

        Specifies the origin location of the acceleration coordinate system with respect to the global
        Cartesian system. The axes of this acceleration coordinate system are parallel to the global
        Cartesian axes.

        A structure may be rotating about the global Cartesian origin ( :ref:`omega`, :ref:`domega` ), which
        may in turn be rotating about another point (the origin of the acceleration coordinate system),
        introducing Coriolis effects. The location of this point (relative to the global Cartesian origin)
        is specified with this :ref:`cgloc` command. For example, if Y is vertical and the global system
        origin is at the surface of the earth while the acceleration system origin is at the center of the
        earth, ``YLOC`` should be -4000 miles (or equivalent) if the rotational effects of the earth are to
        be included. The rotational velocity of the global Cartesian system about this point is specified
        with the :ref:`cgomga` command, and the rotational acceleration is specified with the :ref:`dcgomg`
        command.

        The rotational velocities and accelerations are mainly intended to include mass effects in a static
        ( :ref:`antype`,STATIC) analysis. If used in dynamic analyses, no coupling exists between the user
        input terms and the time history response of the structure. See `Acceleration Effect
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_tool1.html#>`_  :ref:`acel`,
        :ref:`cgomga`, :ref:`dcgomg`, :ref:`domega`, and :ref:`omega`.

        See `Analysis Tools
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/str_EnMoinStAn.html>`_

        This command is also valid in PREP7.


        """
        command = f"CGLOC,{xloc},{yloc},{zloc}"
        return self.run(command, **kwargs)

    def cgomga(self, cgomx: str = "", cgomy: str = "", cgomz: str = "", **kwargs):
        r"""Specifies the rotational velocity of the global origin.

        Mechanical APDL Command: `CGOMGA <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CGOMGA.html>`_

        Parameters
        ----------
        cgomx : str
            Rotational velocity of the global origin about the acceleration system X, Y, and Z axes.

        cgomy : str
            Rotational velocity of the global origin about the acceleration system X, Y, and Z axes.

        cgomz : str
            Rotational velocity of the global origin about the acceleration system X, Y, and Z axes.

        Notes
        -----

        .. _CGOMGA_notes:

        Specifies the rotational velocity of the global origin about each of the acceleration coordinate
        system axes. The location of the acceleration coordinate system is defined with the :ref:`cgloc`
        command. Rotational velocities may be defined in these analysis types:

        * Static ( :ref:`antype`,STATIC)

        * Harmonic ( :ref:`antype`,HARMIC) -- full, `VT
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/str_harmsweep.html#>`_ [
          :ref:`CGOMGA_FN_VT_KRY` ], `Krylov
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/str_Krysweep.html#str_Krylov_macros>`_
          [ :ref:`CGOMGA_FN_VT_KRY` ], or mode-superposition [ :ref:`CGOMGA_mode-sup_LoadSupport` ]

        * Transient ( :ref:`antype`,TRANS) -- `full
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STR5_4.html#strnote11tlm71999>`_
          or mode-superposition [ :ref:`CGOMGA_mode-sup_LoadSupport` ]

        * Substructuring ( :ref:`antype`,SUBSTR)

        * Modal ( :ref:`antype`,MODAL)

         .. _CGOMGA_FN_VT_KRY:

        Loads for VT and Krylov methods are supported as long as they are not:

        * complex tabulated loads (constant or trapezoidal loads in tabulated form are supported)

        * used in conjunction with Rotordynamics ( :ref:`coriolis`,on).

        .. _CGOMGA_mode-sup_LoadSupport:

        In a mode-superposition harmonic or transient analysis, you must apply the load in the modal portion
        of the analysis. Mechanical APDL calculates a load vector and writes it to the :file:`MODE` file,
        which you
        can apply via the :ref:`lvscale` command.

        See `Acceleration Effect
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_tool1.html#>`_  :ref:`acel`,
        :ref:`cgloc`, :ref:`dcgomg`, :ref:`domega`, and :ref:`omega`.

        See `Analysis Tools
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/str_EnMoinStAn.html>`_

        The :ref:`cgomga` command supports tabular boundary conditions (``TABNAME_X``, ``TABNAME_Y``, and
        ``TABNAME_Z``) for ``CGOMGA_X``, ``CGOMGA_Y``, and ``CGOMGA_Z`` input values ( :ref:`dim` ) for full
        transient and harmonic analyses.

        This command is also valid in PREP7.
        """
        command = f"CGOMGA,{cgomx},{cgomy},{cgomz}"
        return self.run(command, **kwargs)

    def cmacel(
        self,
        cm_name: str = "",
        cmacel_x: str = "",
        cmacel_y: str = "",
        cmacel_z: str = "",
        **kwargs,
    ):
        r"""Specifies the translational acceleration of an element component

        Mechanical APDL Command: `CMACEL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CMACEL.html>`_

        Parameters
        ----------
        cm_name : str
            The name of the element component.

        cmacel_x : str
            Acceleration of the element component ``CM_NAME`` in the global Cartesian X, Y, and Z axis
            directions, respectively.

        cmacel_y : str
            Acceleration of the element component ``CM_NAME`` in the global Cartesian X, Y, and Z axis
            directions, respectively.

        cmacel_z : str
            Acceleration of the element component ``CM_NAME`` in the global Cartesian X, Y, and Z axis
            directions, respectively.

        Notes
        -----

        .. _CMACEL_notes:

        The :ref:`cmacel` command specifies the translational acceleration of the element component in each
        of the global Cartesian (X, Y, and Z) axis directions.

        Components for which you want to specify acceleration loading must consist of elements only. The
        elements you use cannot be part of more than one component, and elements that share nodes cannot
        exist in different element components. You cannot apply the loading to an assembly of element
        components.

        To simulate gravity (by using inertial effects), accelerate the structure in the direction opposite
        to gravity. For example, apply a positive ``CMACELY`` to simulate gravity acting in the negative Y
        direction. Units are length/time :sup:`2`.

        You can define the acceleration for the following analyses types:

        * Static ( :ref:`antype`,STATIC)

        * Harmonic ( :ref:`antype`,HARMIC), full, `VT
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/str_harmsweep.html#>`_ [
          :ref:`CMACEL_FN_VT_KRY` ], `Krylov
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/str_Krysweep.html#str_Krylov_macros>`_
          [ :ref:`CMACEL_FN_VT_KRY` ], or mode-superposition [ :ref:`CMACEL_mode-sup_LVSCALE` ] method

        * Transient ( :ref:`antype`,TRANS), `full
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STR5_4.html#strnote11tlm71999>`_
          or mode-superposition [ :ref:`CMACEL_mode-sup_LVSCALE` ] method

        * Substructure ( :ref:`antype`,SUBSTR)

         .. _CMACEL_FN_VT_KRY:

        Loads for VT and Krylov methods are supported as long as they are not:

        * complex tabulated loads (constant or trapezoidal loads in tabulated form are supported)

        * used in conjunction with Rotordynamics ( :ref:`coriolis`,on).

        .. _CMACEL_mode-sup_LVSCALE:

        In a mode-superposition harmonic or transient analysis, you must apply the load in the modal portion
        of the analysis. Mechanical APDL calculates a load vector and writes it to the :file:`MODE` file,
        which you
        can apply via the :ref:`lvscale` command.

        Accelerations are combined with the element mass matrices to form a body-force load vector term.
        Units of acceleration and mass must be consistent to give a product of force units.

        The :ref:`cmacel` command supports tabular boundary conditions (``TABNAME_X``, ``TABNAME_Y``, and
        ``TABNAME_Z``) for ``CMACEL_X``, ``CMACEL_Y``, and ``CMACEL_Z`` input values ( :ref:`dim` ) as a
        function of both time and frequency for full transient and harmonic analyses.

        Related commands for inertia loads are :ref:`acel`, :ref:`cgloc`, :ref:`cgomga`, :ref:`dcgomg`,
        :ref:`domega`, :ref:`omega`, :ref:`cmomega`, and :ref:`cmdomega`.

        See `Analysis Tools
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/str_EnMoinStAn.html>`_

        This command is also valid in :ref:`prep7`.
        """
        command = f"CMACEL,{cm_name},{cmacel_x},{cmacel_y},{cmacel_z}"
        return self.run(command, **kwargs)

    def cmdomega(
        self,
        cm_name: str = "",
        domegax: str = "",
        domegay: str = "",
        domegaz: str = "",
        x1: str = "",
        y1: str = "",
        z1: str = "",
        x2: str = "",
        y2: str = "",
        z2: str = "",
        **kwargs,
    ):
        r"""Specifies the rotational acceleration of an element component about a user-defined rotational axis.

        Mechanical APDL Command: `CMDOMEGA <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CMDOMEGA.html>`_

        Parameters
        ----------
        cm_name : str
            The name of the element component.

        domegax : str
            If the ``X2``, ``Y2``, ``Z2`` fields are not defined, ``DOMEGAX``, ``DOMEGAY``, and ``DOMEGAZ``
            specify the components of the rotational acceleration vector in the global Cartesian X, Y, Z
            directions.

            If the ``X2``, ``Y2``, ``Z2`` fields are defined, only ``DOMEGAX`` is required. ``DOMEGAX``
            specifies the scalar rotational acceleration about the rotational axis. The rotational direction
            of ``DOMEGAX`` is designated either positive or negative, and is determined by the "right hand
            rule."

        domegay : str
            If the ``X2``, ``Y2``, ``Z2`` fields are not defined, ``DOMEGAX``, ``DOMEGAY``, and ``DOMEGAZ``
            specify the components of the rotational acceleration vector in the global Cartesian X, Y, Z
            directions.

            If the ``X2``, ``Y2``, ``Z2`` fields are defined, only ``DOMEGAX`` is required. ``DOMEGAX``
            specifies the scalar rotational acceleration about the rotational axis. The rotational direction
            of ``DOMEGAX`` is designated either positive or negative, and is determined by the "right hand
            rule."

        domegaz : str
            If the ``X2``, ``Y2``, ``Z2`` fields are not defined, ``DOMEGAX``, ``DOMEGAY``, and ``DOMEGAZ``
            specify the components of the rotational acceleration vector in the global Cartesian X, Y, Z
            directions.

            If the ``X2``, ``Y2``, ``Z2`` fields are defined, only ``DOMEGAX`` is required. ``DOMEGAX``
            specifies the scalar rotational acceleration about the rotational axis. The rotational direction
            of ``DOMEGAX`` is designated either positive or negative, and is determined by the "right hand
            rule."

        x1 : str
            If the ``X2``, ``Y2``, ``Z2`` fields are defined, ``X1``, ``Y1``, and ``Z1`` define the
            coordinates of the beginning point of the rotational axis vector. Otherwise, ``X1``, ``Y1``, and
            ``Z1`` are the coordinates of a point through which the rotational axis passes.

        y1 : str
            If the ``X2``, ``Y2``, ``Z2`` fields are defined, ``X1``, ``Y1``, and ``Z1`` define the
            coordinates of the beginning point of the rotational axis vector. Otherwise, ``X1``, ``Y1``, and
            ``Z1`` are the coordinates of a point through which the rotational axis passes.

        z1 : str
            If the ``X2``, ``Y2``, ``Z2`` fields are defined, ``X1``, ``Y1``, and ``Z1`` define the
            coordinates of the beginning point of the rotational axis vector. Otherwise, ``X1``, ``Y1``, and
            ``Z1`` are the coordinates of a point through which the rotational axis passes.

        x2 : str
            The coordinates of the end point of the rotational axis vector.

        y2 : str
            The coordinates of the end point of the rotational axis vector.

        z2 : str
            The coordinates of the end point of the rotational axis vector.

        Notes
        -----

        .. _CMDOMEGA_notes:

        Specifies the rotational acceleration components ``DOMEGAX``, ``DOMEGAY``, and ``DOMEGAZ`` of an
        element component ``CM_NAME`` about a user-defined rotational axis. The rotational axis can be
        defined either as a vector passing through a single point, or a vector connecting two points.

        You can define the rotational acceleration and rotational axis with the :ref:`cmdomega` command for
        these analyses:

        * Static ( :ref:`antype`,STATIC)

        * Harmonic ( :ref:`antype`,HARMIC) -- full, `VT
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/str_harmsweep.html#>`_ [
          :ref:`CMDOMEGA_FN_VT_KRY` ], `Krylov
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/str_Krysweep.html#str_Krylov_macros>`_
          [ :ref:`CMDOMEGA_FN_VT_KRY` ], or mode-superposition [ :ref:`CMDOMEGA_mode-sup_LVSCALE` ]

        * Transient ( :ref:`antype`,TRANS) -- `full
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STR5_4.html#strnote11tlm71999>`_
          or mode-superposition [ :ref:`CMDOMEGA_mode-sup_LVSCALE` ]

        * Substructuring ( :ref:`antype`,SUBSTR)

        * Modal ( :ref:`antype`,MODAL)

         .. _CMDOMEGA_FN_VT_KRY:

        Loads for VT and Krylov methods are supported as long as they are not:

        * complex tabulated loads (constant or trapezoidal loads in tabulated form are supported)

        * used in conjunction with Rotordynamics ( :ref:`coriolis`,on).

        .. _CMDOMEGA_mode-sup_LVSCALE:

        In a mode-superposition harmonic or transient analysis, you must apply the load in the modal portion
        of the analysis. Mechanical APDL calculates a load vector and writes it to the :file:`MODE` file,
        which you
        can apply via the :ref:`lvscale` command.

        Rotational velocities are combined with the element mass matrices to form a body force load vector
        term. Units are radians/time :sup:`2`.

        The :ref:`cmdomega` command supports tabular boundary conditions (``TABNAME_X``, ``TABNAME_Y``, and
        ``TABNAME_Z``) for ``DOMEGAX``, ``DOMEGAY``, and ``DOMEGAZ``  input values ( :ref:`dim` ) for full
        transient and harmonic analyses. In this case, if the end point is specified ( ``X2``, ``Y2``,
        ``Z2`` ), the rotational velocity axis must be along the global X-, Y-, or Z-axis.

        Related commands are :ref:`acel`, :ref:`cgloc`, :ref:`cgloc`, :ref:`omega`, :ref:`cmomega`,
        :ref:`dcgomg`, :ref:`domega`.

        See `Analysis Tools
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/str_EnMoinStAn.html>`_

        You can use the :ref:`cmdomega` command in conjunction with any one of the following two groups of
        commands, but not with both groups simultaneously:

        * GROUP ONE: :ref:`omega`, :ref:`domega`.
        * GROUP TWO: :ref:`cgomga`, :ref:`dcgomg`, :ref:`cgloc`.

        Components for which you want to specify rotational loading must consist of elements only. The
        elements you use cannot be part of more than one component, and elements that share nodes cannot
        exist in different element components. You cannot apply the loading to an assembly of element
        components.

        See `Acceleration Effect
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_tool1.html#>`_

        This command is also valid in PREP7.
        """
        command = f"CMDOMEGA,{cm_name},{domegax},{domegay},{domegaz},{x1},{y1},{z1},{x2},{y2},{z2}"
        return self.run(command, **kwargs)

    def cmomega(
        self,
        cm_name: str = "",
        omegax: str = "",
        omegay: str = "",
        omegaz: str = "",
        x1: str = "",
        y1: str = "",
        z1: str = "",
        x2: str = "",
        y2: str = "",
        z2: str = "",
        **kwargs,
    ):
        r"""Specifies the rotational velocity of an element component about a user-defined rotational axis.

        Mechanical APDL Command: `CMOMEGA <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CMOMEGA.html>`_

        Parameters
        ----------
        cm_name : str
            The name of the element component.

        omegax : str
            If the ``X2``, ``Y2``, ``Z2`` fields are not defined, ``OMEGAX``, ``OMEGAY``, and ``OMEGAZ``
            specify the components of the rotational velocity vector in the global Cartesian X, Y, Z
            directions.

            If the ``X2``, ``Y2``, ``Z2`` fields are defined, only ``OMEGAX`` is required. ``OMEGAX``
            specifies the scalar rotational velocity about the rotational axis. The rotational direction of
            ``OMEGAX`` is designated either positive or negative, and is determined by the "right hand
            rule."

        omegay : str
            If the ``X2``, ``Y2``, ``Z2`` fields are not defined, ``OMEGAX``, ``OMEGAY``, and ``OMEGAZ``
            specify the components of the rotational velocity vector in the global Cartesian X, Y, Z
            directions.

            If the ``X2``, ``Y2``, ``Z2`` fields are defined, only ``OMEGAX`` is required. ``OMEGAX``
            specifies the scalar rotational velocity about the rotational axis. The rotational direction of
            ``OMEGAX`` is designated either positive or negative, and is determined by the "right hand
            rule."

        omegaz : str
            If the ``X2``, ``Y2``, ``Z2`` fields are not defined, ``OMEGAX``, ``OMEGAY``, and ``OMEGAZ``
            specify the components of the rotational velocity vector in the global Cartesian X, Y, Z
            directions.

            If the ``X2``, ``Y2``, ``Z2`` fields are defined, only ``OMEGAX`` is required. ``OMEGAX``
            specifies the scalar rotational velocity about the rotational axis. The rotational direction of
            ``OMEGAX`` is designated either positive or negative, and is determined by the "right hand
            rule."

        x1 : str
            If the ``X2``, ``Y2``, ``Z2`` fields are defined, ``X1``, ``Y1``, and ``Z1`` define the
            coordinates of the beginning point of the rotational axis vector. Otherwise, ``X1``, ``Y1``, and
            ``Z1`` are the coordinates of a point through which the rotational axis passes.

        y1 : str
            If the ``X2``, ``Y2``, ``Z2`` fields are defined, ``X1``, ``Y1``, and ``Z1`` define the
            coordinates of the beginning point of the rotational axis vector. Otherwise, ``X1``, ``Y1``, and
            ``Z1`` are the coordinates of a point through which the rotational axis passes.

        z1 : str
            If the ``X2``, ``Y2``, ``Z2`` fields are defined, ``X1``, ``Y1``, and ``Z1`` define the
            coordinates of the beginning point of the rotational axis vector. Otherwise, ``X1``, ``Y1``, and
            ``Z1`` are the coordinates of a point through which the rotational axis passes.

        x2 : str
            The coordinates of the end point of the rotational axis vector.

        y2 : str
            The coordinates of the end point of the rotational axis vector.

        z2 : str
            The coordinates of the end point of the rotational axis vector.

        Notes
        -----

        .. _CMOMEGA_notes:

        Specifies the rotational velocity components ``OMEGAX``, ``OMEGAY``, and ``OMEGAZ`` of an element
        component ``CM_NAME`` about a user-defined rotational axis. The rotational axis can be defined
        either as a vector passing through a single point or a vector connecting two points.

        You can define the rotational velocity and rotational axis for these analysis types:

        * Static ( :ref:`antype`,STATIC)

        * Harmonic ( :ref:`antype`,HARMIC) -- full, `VT
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/str_harmsweep.html#>`_ [
          :ref:`CMOMEGA_FN_VT_KRY` ], `Krylov
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/str_Krysweep.html#str_Krylov_macros>`_
          [ :ref:`CMOMEGA_FN_VT_KRY` ], or mode-superposition [ :ref:`CMOMEGA_mode-sup_LVSCALE` ]

        * Transient ( :ref:`antype`,TRANS) -- `full
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STR5_4.html#strnote11tlm71999>`_
          or mode-superposition [ :ref:`CMOMEGA_mode-sup_LVSCALE` ]

        * Substructuring ( :ref:`antype`,SUBSTR)

        * Modal ( :ref:`antype`,MODAL)

         .. _CMOMEGA_FN_VT_KRY:

        Loads for VT and Krylov methods are supported as long as they are not:

        * complex tabulated loads (constant or trapezoidal loads in tabulated form are supported)

        * used in conjunction with Rotordynamics ( :ref:`coriolis`,on).

        .. _CMOMEGA_mode-sup_LVSCALE:

        In a mode-superposition harmonic or transient analysis, you must apply the load in the modal portion
        of the analysis. Mechanical APDL calculates a load vector and writes it to the :file:`MODE` file,
        which you
        can apply via the :ref:`lvscale` command.

        Rotational velocities are combined with the element mass matrices to form a body-force load vector
        term. Units are radians/time. Related commands are :ref:`acel`, :ref:`cgloc`, :ref:`cgloc`,
        :ref:`cgomga`, :ref:`cmdomega`, :ref:`dcgomg`, :ref:`domega`.

        See `Analysis Tools
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/str_EnMoinStAn.html>`_

        You can use the :ref:`cmomega` command in conjunction with either one of the following two groups of
        commands, but not with both groups simultaneously:

        * GROUP ONE: :ref:`omega`, :ref:`domega`.
        * GROUP TWO: :ref:`cgomga`, :ref:`dcgomg`, :ref:`cgloc`.

        Components for which you want to specify rotational loading must consist of elements only. The
        elements you use cannot be part of more than one component, and elements that share nodes cannot
        exist in different element components. You cannot apply the loading to an assembly of element
        components.

        If you have applied the Coriolis effect ( :ref:`coriolis` ) using a `stationary
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_rot/Hlp_G_ROTGENDYNEQ.html#rotintrogendyneq2>`_
        reference frame, the :ref:`cmomega` command takes the gyroscopic damping matrix into account for the
        elements listed under "Stationary Reference Frame" in the notes section of the :ref:`coriolis`
        command. Mechanical APDL verifies that the rotation vector axis is parallel to the axis of the
        element; if
        not, the gyroscopic effect is not applied. If you issue a :ref:`cmomega` command when the Coriolis
        or gyroscopic effect is present, a subsequently issued :ref:`omega` command has no effect.

        The :ref:`cmomega` command supports tabular boundary conditions (``TABNAME_X``, ``TABNAME_Y``, and
        ``TABNAME_Z``) for ``OMEGAX``, ``OMEGAY``, and ``OMEGAZ``  input values ( :ref:`dim` ) for modal,
        full transient, and full harmonic analyses. In this case, if the end point is specified ( ``X2``,
        ``Y2``, ``Z2`` ), the rotational velocity axis must be along the global X-, Y-, or Z-axis.

        The load interpolation setting ( :ref:`kbc` ) applies to the rotational velocity, in particular the
        ``OMGSQRDKEY`` option for quadratic interpolation.
        """
        command = f"CMOMEGA,{cm_name},{omegax},{omegay},{omegaz},{x1},{y1},{z1},{x2},{y2},{z2}"
        return self.run(command, **kwargs)

    def cmrotate(
        self,
        cm_name: str = "",
        rotatx: str = "",
        rotaty: str = "",
        rotatz: str = "",
        x1: str = "",
        y1: str = "",
        z1: str = "",
        x2: str = "",
        y2: str = "",
        z2: str = "",
        **kwargs,
    ):
        r"""Specifies the rotational velocity of an element component in a brake-squeal analysis.

        Mechanical APDL Command: `CMROTATE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CMROTATE.html>`_

        Parameters
        ----------
        cm_name : str
            The name of the element component.

        rotatx : str
            If the ``X2``, ``Y2``, ``Z2`` fields are not defined, ``ROTATX``, ``ROTATY``, and ``ROTATZ``
            specify the components of the rotational angle vector in the global Cartesian X, Y, Z
            directions.

            If the ``X2``, ``Y2``, ``Z2`` fields are defined, only ``ROTATX`` is required. ``ROTATX``
            specifies the scalar rotational velocity about the rotational axis. The rotational direction of
            ``ROTATX`` is designated either positive or negative, and is determined by the "right hand
            rule."

        rotaty : str
            If the ``X2``, ``Y2``, ``Z2`` fields are not defined, ``ROTATX``, ``ROTATY``, and ``ROTATZ``
            specify the components of the rotational angle vector in the global Cartesian X, Y, Z
            directions.

            If the ``X2``, ``Y2``, ``Z2`` fields are defined, only ``ROTATX`` is required. ``ROTATX``
            specifies the scalar rotational velocity about the rotational axis. The rotational direction of
            ``ROTATX`` is designated either positive or negative, and is determined by the "right hand
            rule."

        rotatz : str
            If the ``X2``, ``Y2``, ``Z2`` fields are not defined, ``ROTATX``, ``ROTATY``, and ``ROTATZ``
            specify the components of the rotational angle vector in the global Cartesian X, Y, Z
            directions.

            If the ``X2``, ``Y2``, ``Z2`` fields are defined, only ``ROTATX`` is required. ``ROTATX``
            specifies the scalar rotational velocity about the rotational axis. The rotational direction of
            ``ROTATX`` is designated either positive or negative, and is determined by the "right hand
            rule."

        x1 : str
            If the ``X2``, ``Y2``, ``Z2`` fields are defined, ``X1``, ``Y1``, and ``Z1`` define the
            coordinates of the beginning point of the rotational axis vector. Otherwise, ``X1``, ``Y1``, and
            ``Z1`` are the coordinates of a point through which the rotational axis passes.

        y1 : str
            If the ``X2``, ``Y2``, ``Z2`` fields are defined, ``X1``, ``Y1``, and ``Z1`` define the
            coordinates of the beginning point of the rotational axis vector. Otherwise, ``X1``, ``Y1``, and
            ``Z1`` are the coordinates of a point through which the rotational axis passes.

        z1 : str
            If the ``X2``, ``Y2``, ``Z2`` fields are defined, ``X1``, ``Y1``, and ``Z1`` define the
            coordinates of the beginning point of the rotational axis vector. Otherwise, ``X1``, ``Y1``, and
            ``Z1`` are the coordinates of a point through which the rotational axis passes.

        x2 : str
            The coordinates of the end point of the rotational axis vector.

        y2 : str
            The coordinates of the end point of the rotational axis vector.

        z2 : str
            The coordinates of the end point of the rotational axis vector.

        Notes
        -----
        The :ref:`cmrotate` command specifies the rotational motion velocity components ``ROTATX``,
        ``ROTATY``, and ``ROTATZ`` of an element component ``CM_Name`` about a user-defined rotational axis.
        The rotational axis can be defined either as a vector passing through a single point or a vector
        connecting two points. :ref:`cmrotate` can be used in static analyses ( :ref:`antype`,STATIC) and
        modal analyses ( :ref:`antype`,MODAL).

        This command sets the constant rotational velocity on the nodes of the specified element component,
        despite any deformation at the nodes. This feature is primarily used for generating sliding contact
        at frictional contact interfaces in a `brake-squeal analysis
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STRmodanexamp.html#strlinearnonpresmodan>`_.
        This type of analysis typically involves surface-to-surface contact between the brake pad and the
        rotating disk. The applicable contact elements, therefore, are ``CONTA174`` and ``CONTA175``.

        A `brake-squeal analysis
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STRmodanexamp.html#strlinearnonpresmodan>`_
        generally involves a linear perturbation modal analysis subsequent to a large-deformation static
        analysis with the Newton-Raphson option set as :ref:`nropt`,UNSYM. Therefore, :ref:`cmrotate` is not
        applicable for multiple load step solves using the :ref:`lssolve` command.

        The load interpolation setting ( :ref:`kbc` ) applies to the rotational velocity, in particular the
        ``OMGSQRDKEY`` option for quadratic interpolation.

        This command is also valid in PREP7.
        """
        command = f"CMROTATE,{cm_name},{rotatx},{rotaty},{rotatz},{x1},{y1},{z1},{x2},{y2},{z2}"
        return self.run(command, **kwargs)

    def coriolis(
        self,
        option: str = "",
        refframe: str = "",
        rotdamp: str = "",
        rotmass: str = "",
        **kwargs,
    ):
        r"""Applies the Coriolis effect to a rotating structure.

        Mechanical APDL Command: `CORIOLIS <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CORIOLIS.html>`_

        Parameters
        ----------
        option : str, bool, optional
            Flag to activate or deactivate the Coriolis effect:

            ``"ON"``, ``"YES"``, or ``True`` - Activate. This value is the default.

            ``"OFF"``, ``"NO"``, or ``False`` - Deactivate.

        refframe : str, bool, optional
            Flag to activate or deactivate a stationary reference frame.

            ``"ON"``, ``"YES"``, or ``True`` - Activate.

            ``"OFF"``, ``"NO"``, or ``False`` - Deactivate. This value is the default.

        rotdamp : str, bool, optional
            Flag to activate or deactivate rotating damping effect.

            ``"ON"``, ``"YES"``, or ``True`` - Activate.

            ``"OFF"``, ``"NO"``, or ``False`` - Deactivate. This value is the default.

        rotmass : str, bool, optional
            Flag to activate or deactivate rotor mass summary printout
            (only supported for ``refframe='on'``).

            ``"ON"``, ``"YES"``, or ``True`` - Activate.

            ``"OFF"``, ``"NO"``, or ``False`` - Deactivate. This value is the default.

        Notes
        -----
        The :ref:`coriolis` command is used for linear analyses in either a rotating or a stationary
        reference frame, and performs differently according to the designated ``RefFrame`` value. The
        :ref:`coriolis` command must be specified during the first step of the analysis. The rotational
        velocity must be defined using :ref:`omega` (when the whole model is rotating) or :ref:`cmomega`
        (component based rotation). Specific restrictions and elements apply to each case, as follows:

        * `Rotating Reference Frame
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_adv/Hlp_G_ADVROTFR.html#>`_ (, RefFrame
          = OFF) - The command applies the Coriolis effect in the following structural element types:
          ``MASS21``, ``SHELL181``, ``PLANE182``, ``PLANE183``, ``SOLID185``, ``SOLID186``, ``SOLID187``,
          ``BEAM188``, ``BEAM189``, ``SOLSH190``, ``SHELL281``, ``PIPE288`` and ``PIPE289``. It also applies
          this effect in the following coupled-field elements when structural degrees of freedom are present:
          ``PLANE222``, ``PLANE223``, ``SOLID225``, ``SOLID226``, and ``SOLID227``.

          The rotating damping effect ( ``RotDamp`` = ON) is only supported by the ``COMBI214`` element when
          stationary.

          In a rotating reference frame, the Coriolis and `spin-softening
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_adv/Hlp_G_ADVROTFR.html#>`_ effects, as
          well as the centrifugal forces, contribute to the dynamics and are applied by default.

        * `Stationary Reference Frame
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_rot/Hlp_G_ROTGENDYNEQ.html#rotintrogendyneq2>`_
          (, RefFrame = ON) - The command activates the gyroscopic damping matrix in the following structural
          elements: ``MASS21``, ``BEAM188``, ``SHELL181``, ``BEAM189``, ``SOLID185``, ``SOLID186``,
          ``SOLID187``, ``SOLSH190``, ``SOLID272``, ``SOLID273``, ``SHELL281``, ``PIPE288``, ``PIPE289``, and
          ``MATRIX50``.

          The rotating structure is assumed to be axisymmetric about the axis of rotation.

          The rotating damping effect ( ``RotDamp`` = ON) is supported by the elements listed above that
          generate a gyroscopic damping matrix. It is also supported by some specific elements (see for a
          complete list).

          The rotor mass summary printout ( ``RotMass`` = ON) is only supported for some of the elements that
          generate a gyroscopic damping matrix: ``MASS21``, ``BEAM188``, ``BEAM189``, ``PIPE288``, and
          ``PIPE289``. The EMAT file is required ( :ref:`ematwrite`,YES).

        To include Coriolis effects in a linear perturbation (prestressed) analysis, follow the procedure
        detailed in `Considerations for Rotating Structures
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/strllinpertrotmach.html#str_rot_rotating>`_

        In a nonlinear transient analysis in which the model is actually spinning ( :ref:`antype`,TRANS and
        :ref:`nlgeom`,ON) the :ref:`coriolis` command must not be used as any spinning motion applied
        through either the :ref:`ic` or :ref:`d` commands automatically includes nonlinear inertia terms
        such as the Coriolis effect.

        To take into account variable bearings ( ``COMBI214`` elements with tabular user-defined
        characteristics), you must activate the Coriolis effect in a stationary reference frame. The
        gyroscopic effect coming from ``COMBI214`` mass characteristics is not supported.

        For more information about using the :ref:`coriolis` command, see `Rotating Structure Analysis
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_adv/advrrfexamples.html>`_ in the
        `Advanced Analysis Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_adv/advoceanloading.html>`_ and also in
        the `Rotordynamic Analysis Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_rot/rotdynappenda.html>`_. For details
        about the Coriolis and gyroscopic effect element
        formulations, see the `Mechanical APDL Theory Reference
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_biblio.html>`_.

        Elements with `layered section properties
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STR11_2.html#atlQxq2f1mcm>`_
        do not support Coriolis effects (rotating and stationary reference frames).

        This command is also valid in PREP7.

        Examples
        --------
        Enable the coriolis effect with a stationary reference frame.

        >>> mapdl.coriolis('ON', refframe='ON')

        Alternatively, ``coriolis`` supports bool parameters.

        >>> mapdl.coriolis(True, refframe=True)
        """
        if isinstance(option, bool):
            option = int(option)
        if isinstance(refframe, bool):
            refframe = int(refframe)
        if isinstance(rotdamp, bool):
            rotdamp = int(rotdamp)
        if isinstance(rotmass, bool):
            rotmass = int(rotdamp)
        command = f"CORIOLIS,{option},,,{refframe},{rotdamp},{rotmass}"
        return self.run(command, **kwargs)

    def dcgomg(self, dcgox: str = "", dcgoy: str = "", dcgoz: str = "", **kwargs):
        r"""Specifies the rotational acceleration of the global origin.

        Mechanical APDL Command: `DCGOMG <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_DCGOMG.html>`_

        Parameters
        ----------
        dcgox : str
            Rotational acceleration of the global origin about the acceleration system X, Y, and Z axes.

        dcgoy : str
            Rotational acceleration of the global origin about the acceleration system X, Y, and Z axes.

        dcgoz : str
            Rotational acceleration of the global origin about the acceleration system X, Y, and Z axes.

        Notes
        -----

        .. _DCGOMG_notes:

        Specifies the rotational acceleration of the global origin about each of the acceleration coordinate
        system axes ( :ref:`cgloc` ). Rotational accelerations may be defined in these analysis types:

        * Static ( :ref:`antype`,STATIC)

        * Harmonic ( :ref:`antype`,HARMIC) -- full, `VT
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/str_harmsweep.html#>`_ [
          :ref:`DCGOMG_FN_VT_KRY` ], `Krylov
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/str_Krysweep.html#str_Krylov_macros>`_
          [ :ref:`DCGOMG_FN_VT_KRY` ], or mode-superposition [ :ref:`DCGOMG_mode-sup_LoadSupport` ]

        * Transient ( :ref:`antype`,TRANS) -- `full
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STR5_4.html#strnote11tlm71999>`_
          or mode-superposition [ :ref:`DCGOMG_mode-sup_LoadSupport` ]

        * Substructuring ( :ref:`antype`,SUBSTR)

        * Modal ( :ref:`antype`,MODAL)

         .. _DCGOMG_FN_VT_KRY:

        Loads for VT and Krylov methods are supported as long as they are not:

        * complex tabulated loads (constant or trapezoidal loads in tabulated form are supported)

        * used in conjunction with Rotordynamics ( :ref:`coriolis`,on).

        .. _DCGOMG_mode-sup_LoadSupport:

        In a mode-superposition harmonic or transient analysis, you must apply the load in the modal portion
        of the analysis. Mechanical APDL calculates a load vector and writes it to the :file:`MODE` file,
        which you
        can apply via the :ref:`lvscale` command.

        See `Acceleration Effect
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_tool1.html#>`_  :sup:`2`.

        The :ref:`dcgomg` command supports tabular boundary conditions (``TABNAME_X``, ``TABNAME_Y``, and
        ``TABNAME_Z``) for ``DCGOMG_X``, ``DCGOMG_Y``, and ``DCGOMG_Z`` input values ( :ref:`dim` ) for full
        transient and harmonic analyses.

        Related commands are :ref:`acel`, :ref:`cgloc`, :ref:`cgomga`, :ref:`domega`, and :ref:`omega`.

        See `Analysis Tools
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/str_EnMoinStAn.html>`_

        This command is also valid in PREP7.
        """
        command = f"DCGOMG,{dcgox},{dcgoy},{dcgoz}"
        return self.run(command, **kwargs)

    def domega(self, domgx: str = "", domgy: str = "", domgz: str = "", **kwargs):
        r"""Specifies the rotational acceleration of the structure.

        Mechanical APDL Command: `DOMEGA <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_DOMEGA.html>`_

        Parameters
        ----------
        domgx : str
            Rotational acceleration of the structure about the global Cartesian X, Y, and Z axes.

        domgy : str
            Rotational acceleration of the structure about the global Cartesian X, Y, and Z axes.

        domgz : str
            Rotational acceleration of the structure about the global Cartesian X, Y, and Z axes.

        Notes
        -----

        .. _DOMEGA_notes:

        Specifies the rotational acceleration of the structure about each of the global Cartesian axes.
        Rotational accelerations may be defined in these analysis types:

        * Static ( :ref:`antype`,STATIC)

        * Harmonic ( :ref:`antype`,HARMIC) -- full, `VT
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/str_harmsweep.html#>`_ [
          :ref:`DOMEGA_FN_VT_KRY` ], `Krylov
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/str_Krysweep.html#str_Krylov_macros>`_
          [ :ref:`DOMEGA_FN_VT_KRY` ], or mode-superposition [ :ref:`DOMEGA_mode-sup_LoadSupport` ]

        * Transient ( :ref:`antype`,TRANS) -- `full
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STR5_4.html#strnote11tlm71999>`_
          or mode-superposition [ :ref:`DOMEGA_mode-sup_LoadSupport` ]

        * Substructuring ( :ref:`antype`,SUBSTR)

        * Modal ( :ref:`antype`,MODAL)

         .. _DOMEGA_FN_VT_KRY:

        Loads for VT and Krylov methods are supported as long as they are not:

        * complex tabulated loads (constant or trapezoidal loads in tabulated form are supported)

        * used in conjunction with Rotordynamics ( :ref:`coriolis`,on).

        .. _DOMEGA_mode-sup_LoadSupport:

        In a mode-superposition harmonic or transient analysis, you must apply the load in the modal portion
        of the analysis. Mechanical APDL calculates a load vector and writes it to the :file:`MODE` file,
        which you
        can apply via the :ref:`lvscale` command.

        See `Acceleration Effect
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_tool1.html#>`_  :sup:`2`.

        The :ref:`domega` command supports tabular boundary conditions (``TABNAME_X``, ``TABNAME_Y``, and
        ``TABNAME_Z``) for ``DOMEGA_X``, ``DOMEGA_Y``, and ``DOMEGA_Z`` input values ( :ref:`dim` ) for full
        transient and harmonic analyses.

        Related commands are :ref:`acel`, :ref:`cgloc`, :ref:`cgomga`, :ref:`dcgomg`, and :ref:`omega`.

        See `Analysis Tools
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/str_EnMoinStAn.html>`_

        This command is also valid in PREP7.
        """
        command = f"DOMEGA,{domgx},{domgy},{domgz}"
        return self.run(command, **kwargs)

    def irlf(
        self,
        key: int | str = "",
        printfreq: int | str = "",
        rampkey: int | str = "",
        **kwargs,
    ):
        r"""Specifies that inertia relief calculations are to be performed.

        Mechanical APDL Command: `IRLF <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_IRLF.html>`_

        Parameters
        ----------
        key : int or str
            Calculation key:

            * ``0`` - No inertia relief calculations.

            * ``1`` - Counterbalance loads with inertia relief forces.

            * ``-1`` - Precalculate masses for summary printout only (no inertia relief).

        printfreq : int or str
            Frequency at which inertia relief information is printed during substeps in a nonlinear static or
            eigenvalue buckling analysis. This value must be a positive integer, 0, or ALL, as described below.

            * ``0`` - No inertia relief information is printed during the Newton Raphson substeps (default).

            * ``n`` - Prints inertia relief information every ``n`` th substep of each load step.

            * ``ALL`` - Prints inertia relief information every substep.

        rampkey : int or str
            Key to control ramping of rigid body accelerations. See notes for steps to achieve convergence when :ref:`turning on the inertia relief option in the second or later load step of a nonlinear analysis. <IRLF_Note_LateLoadStep>`

            * ``0`` - (Default) Rigid body acceleration is stepped and ramped together with total external loads
              following specifications set using the :ref:`kbc` command. Normally, the inertia relief option is
              turned on at the first load step.

            * ``1`` - Ramp the rigid body accelerations alone following specifications set by the :ref:`kbc`
              command. This option is only used for better convergence when the inertia relief load step is
              nonlinear and the inertia relief option is turned on from a later load step (other than the first).
              It works with :ref:`kbc`,0 specified and no new loads added to the current load step. After the
              current load step, ``RampKey`` is automatically set to 0. See :ref:`IRLF_Note_LateLoadStep`.

        Notes
        -----

        .. _IRLF_notes:

        The :ref:`irlf` command specifies that the program is to calculate accelerations to counterbalance
        the applied loads (inertia relief). Displacement constraints on the structure should be only those
        necessary to prevent rigid-body motions (3 are needed for a 2D structure and 6 for a 3D structure).
        If the minimum number of displacement constraints are applied and it is a linear static analysis,
        the sum of the reaction forces at the constrained points will be zero. However, if it is a nonlinear
        static analysis ( :ref:`nlgeom`,ON), the sum of reaction forces at the constrained points will be
        approximately zero due to the error introduced by nonlinear iterations. Accelerations are calculated
        from the element mass matrices and the applied forces. Data needed to calculate the mass (such as
        density) must be input. Both translational and rotational accelerations may be calculated.

        This option applies to the following analyses: static (linear or nonlinear), linear perturbation
        static, and buckling (see `Including Inertia Relief Calculations
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/Hlp_G_BAS2_6.html#>`_  `Supported
        Analysis Types for Inertia Relief
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_tool2.html#>`_  Elements that
        operate in the nodal coordinate system and axisymmetric or generalized plane strain elements are not
        allowed. Symmetry models are not valid for inertia relief analysis. Models with both 2D and 3D
        element types are not recommended.

        Loads may be input as usual. Displacements and stresses are calculated as usual.

        An automatic inertia relief capability is available for linear static analysis only. See the
        :ref:`airl` command for details.

        Use :ref:`irlist` to print inertia relief calculation results. Note that :ref:`irlist` can only be
        issued at the end of the analysis, right after the :ref:`solve` command in the nonlinear case. To
        print information during substeps in a nonlinear static or eigenvalue buckling analysis, set
        ``PrintFreq`` as described above. The mass and moment of inertia summary printed before the solution
        is accurate (because of the additional pre-calculations required for inertia relief). See `Inertia
        Relief
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_tool2.html#thy_InertiaRelAnalysisTypes>`_

        Turning On the Inertia Relief Option in the Second or Later Load Step If the inertia relief option
        is turned on in the second or later load step in a nonlinear static
        analysis, follow these precautionary steps for easy nonlinear convergence:

        At the second or higher load step, where :ref:`irlf`,1 is issued the first time, do not apply new
        external loads.

        Set ``Rampkey`` = 1 at this load step and :ref:`kbc`,0 so that the rigid body accelerations are
        ramped.

        Use the :ref:`nsubst` or :ref:`deltim` command to allow more substeps in this load step.

        When a superelement ( ``MATRIX50`` ) is present in the model, any DOF constraints that you need to
        apply ( :ref:`d` ) on a degree of freedom (DOF) belonging to the superelement must be applied in the
        `use pass
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_substr/an9Auq1d6ldm.html#advobsl5jla062999>`_
        of the ``MATRIX50`` element ( not in the `generation pass
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_substr/advcmssuperelem.html#usingcms_elemcalc>`_
        ). The command has no effect in the `generation pass
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_substr/aKa7uq1a9ldm.html#advsupmtr2jla062999>`_
        of a substructure. In the `expansion pass
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_substr/axcAuq367ldm.html#adv5note4jla062999>`_,
        precalculation of masses for summary printout ( :ref:`irlf`,-1) occurs only on elements that are
        part of the substructure.

        This command is also valid in PREP7.

        **Example Usage**
        Example command inputs for including inertia relief calculations in a static analysis with geometric
        nonlinearity, a linear perturbation static analysis, and a linear perturbation buckling analysis are
        found in `Including Inertia Relief Calculations
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/Hlp_G_BAS2_6.html#>`_
        """
        command = f"IRLF,{key},{printfreq},{rampkey}"
        return self.run(command, **kwargs)

    def omega(self, omegx: str = "", omegy: str = "", omegz: str = "", **kwargs):
        r"""Specifies the rotational velocity of the structure.

        Mechanical APDL Command: `OMEGA <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_OMEGA.html>`_

        Parameters
        ----------
        omegx : str
            Rotational velocity of the structure about the global Cartesian X, Y, and Z axes.

        omegy : str
            Rotational velocity of the structure about the global Cartesian X, Y, and Z axes.

        omegz : str
            Rotational velocity of the structure about the global Cartesian X, Y, and Z axes.

        Notes
        -----

        .. _OMEGA_notes:

        This command specifies the rotational velocity of the structure about each of the global Cartesian
        axes (right-hand rule). Rotational velocities may be defined in these analysis types:

        * Static ( :ref:`antype`,STATIC)

        * Harmonic ( :ref:`antype`,HARMIC) -- full, `VT
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/str_harmsweep.html#>`_ [
          :ref:`OMEGA_FN_VT_KRY` ], `Krylov
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/str_Krysweep.html#str_Krylov_macros>`_
          [ :ref:`OMEGA_FN_VT_KRY` ], or mode-superposition [ :ref:`OMEGA_mode-sup_LoadSupport` ]

        * Transient ( :ref:`antype`,TRANS) -- `full
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STR5_4.html#strnote11tlm71999>`_
          or mode-superposition [ :ref:`OMEGA_mode-sup_LoadSupport` ]

        * Substructuring ( :ref:`antype`,SUBSTR)

        * Modal ( :ref:`antype`,MODAL)

         .. _OMEGA_FN_VT_KRY:

        Loads for VT and Krylov methods are supported as long as they are not:

        * complex tabulated loads (constant or trapezoidal loads in tabulated form are supported)

        * used in conjunction with Rotordynamics ( :ref:`coriolis`,on).

        .. _OMEGA_mode-sup_LoadSupport:

        In a mode-superposition harmonic or transient analysis, you must apply the load in the modal portion
        of the analysis. Mechanical APDL calculates a load vector and writes it to the :file:`MODE` file,
        which you
        can apply via the :ref:`lvscale` command.

        The command supports tabular boundary conditions (``TABNAME_X``, ``TABNAME_Y``, and ``TABNAME_Z``)
        for ``OMEGA_X``, ``OMEGA_Y``, and ``OMEGA_Z`` input values ( :ref:`dim` ) for full transient and
        harmonic analyses.

        Rotational velocities are combined with the element mass matrices to form a body-force load vector
        term. Units are radians/time. Related commands are :ref:`acel`, :ref:`cgloc`, :ref:`cgomga`,
        :ref:`dcgomg`, and :ref:`domega`.

        See `Analysis Tools
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/str_EnMoinStAn.html>`_

        If you have applied the Coriolis effect ( :ref:`coriolis` ) using a `stationary reference frame
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_rot/Hlp_G_ROTGENDYNEQ.html#rotintrogendyneq2>`_,
        this command takes the gyroscopic damping matrix into account for the elements listed in the
        **Stationary Reference Frame** heading in the notes section of the :ref:`coriolis` command. The
        element axis must pass through the global Cartesian origin. The program verifies that the rotation
        vector axis is parallel to the axis of the element; if not, the gyroscopic effect is not applied.
        After issuing :ref:`omega` when the Coriolis or gyroscopic effect is present, a subsequently issued
        :ref:`cmomega` command has no effect.

        The load interpolation setting ( :ref:`kbc` ) applies to the rotational velocity, in particular the
        ``OMGSQRDKEY`` option for quadratic interpolation.

        This command is also valid in PREP7.
        """
        command = f"OMEGA,{omegx},{omegy},{omegz}"
        return self.run(command, **kwargs)

    def synchro(self, ratio: str = "", cname: str = "", **kwargs):
        r"""Specifies whether the excitation frequency is synchronous or asynchronous with the rotational
        velocity of a structure.

        Mechanical APDL Command: `SYNCHRO <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SYNCHRO.html>`_

        Parameters
        ----------
        ratio : str
            In a stationary reference frame ( :ref:`coriolis` with ``RefFrame`` = ON), ``RATIO`` is the
            ratio between the frequency of excitation and the frequency of the rotational velocity of the
            structure. This value must be greater than 0. The default is an unbalance excitation.

            In a rotating reference frame ( :ref:`coriolis` with ``RefFrame`` = OFF), ``RATIO`` is the ratio
            between the frequency of excitation and the frequency of the rotational velocity of the
            structure minus 1. This value must be greater than 0. There is no default.

        cname : str
            The name of the rotating component on which to apply the harmonic excitation.

        Notes
        -----
        The :ref:`synchro` command specifies whether the excitation frequency is synchronous or asynchronous
        with the rotational velocity of a structure in a harmonic analysis. Use the command to take into
        account rotating harmonic forces on rotating structures.

        Mechanical APDL calculates the rotational velocity Ω of the structure from the excitation frequency
        f,
        defined (via the :ref:`harfrq` command) as Ω = 2π f / ``RATIO``. The rotational velocity is applied
        along the direction cosines of the rotation axis (specified via an :ref:`omega` or :ref:`cmomega`
        command).

        In a stationary reference frame, specifying any value for ``RATIO`` causes a general rotational
        force excitation and not an unbalance force. To define an unbalance excitation force (F = Ω :sup:`2`
        * Unb), ``RATIO`` should be left blank (the nodal unbalance Unb is specified via the :ref:`f`
        command).

        In a rotating reference frame ( :ref:`coriolis` with ``RefFrame`` = OFF), an unbalance excitation is
        a static load; therefore, a value must be supplied for ``RATIO``.

        The :ref:`synchro` command is valid only for the full harmonic analysis method ( :ref:`hropt`,FULL)
        and the frequency-sweep harmonic analysis method ( :ref:`hropt`,VT) involving a rotating structure (
        :ref:`omega` or :ref:`cmomega` ) with Coriolis enabled ( :ref:`coriolis` ).
        """
        command = f"SYNCHRO,{ratio},{cname}"
        return self.run(command, **kwargs)
