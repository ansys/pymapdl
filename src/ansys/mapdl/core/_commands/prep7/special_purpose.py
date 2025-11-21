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


class SpecialPurpose:

    def adpci(
        self,
        action: str = "",
        par1: str = "",
        par2: str = "",
        par3: str = "",
        par4: str = "",
        par5: str = "",
        par6: str = "",
        par7: str = "",
        par8: str = "",
        **kwargs,
    ):
        r"""Defines parameters associated with adaptive crack initiation.

        Mechanical APDL Command: `ADPCI <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ADPCI.html>`_

        Parameters
        ----------
        action : str
            Specifies action for defining or manipulating initial crack data:

            * ``DEFINE`` - `Command Specification for Action= DEFINE
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cmd/Hlp_C_ADPCI.html#>`_ Initiate a new
              adaptive-crack calculation and assign an ID.

            * ``GEOM`` - `Command Specifications for Action= GEOM
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cmd/Hlp_C_ADPCI.html#>`_ Define the
              geometry data for initializing a crack.

            * ``DELE`` - `Command Specifications for Action= DELE
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cmd/Hlp_C_ADPCI.html#>`_ Delete the
              :ref:`adpci` data set associated with the specified ID.

            * ``LIST`` - `Command Specifications for Action= LIST
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cmd/Hlp_C_ADPCI.html#>`_ List the
              :ref:`adpci` data set associated with the specified ID.

        par1 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ADPCI.html>`_ for further
            information.

        par2 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ADPCI.html>`_ for further
            information.

        par3 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ADPCI.html>`_ for further
            information.

        par4 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ADPCI.html>`_ for further
            information.

        par5 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ADPCI.html>`_ for further
            information.

        par6 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ADPCI.html>`_ for further
            information.

        par7 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ADPCI.html>`_ for further
            information.

        par8 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ADPCI.html>`_ for further
            information.

        Other Parameters
        ----------------
        **Command Specification for Action= DEFINE**

        .. _adpci_define:

        * ``Par1`` - :ref:`adpci` ID number.

        * ``Par2`` - Surface-node component name for defining the crack-initiation zone (must be 32
          characters or less).

        * ``Par3`` - Material ID for defining the crack-initiation criterion.

        * ``Par4`` - Shape of the initialized crack:

          * ELLIPSE - Elliptical crack shape (default, and the only valid value).

        **Command Specifications for Action= GEOM**

        .. _adpci_geom:

        * ``Par1`` - :ref:`adpci` ID number.

        * ``Par2`` - Crack geometry characteristic to define:

          * CENTER - Specify the ellipse center location.
          * AXES - Specify the directions of the two ellipse axes.
          * ALEN - Specify the lengths of two ellipse axes. This value is required when AXES or LCS is
            specified.
          * LCS - Local coordinate system number for defining the ellipse center location and axes directions.
            See :ref:`adpci_notes` below.

        * ``Par3`` - The first value to assign to the geometry characteristic specified via ``Par2`` :

          * If ``Par2`` = CENTER, the X coordinate of the ellipse center.
          * If ``Par2`` = AXES, the X component of the first ellipse axis direction.
          * If ``Par2`` = ALEN, the length of the first ellipse axis.
          * If ``Par2`` = LCS, the local coordinate system number.

        * ``Par4`` - The second value to assign to the geometry characteristic specified via ``Par2`` :

          * If ``Par2`` = CENTER, the Y coordinate of the ellipse center.
          * If ``Par2`` = AXES, the Y component of the first ellipse axis direction.
          * If ``Par2`` = ALEN, the length of the second ellipse axis.

        * ``Par5`` - The third value to assign to the geometry characteristic specified via ``Par2`` :

          * If ``Par2`` = CENTER, the Z coordinate of the ellipse center.
          * If ``Par2`` = AXES, the Z component of the first ellipse axis direction.

        * ``Par6`` - The fourth value to assign to the geometry characteristic specified via ``Par2`` :

          * If ``Par2`` = AXES, the X component of the second ellipse axis direction.

        * ``Par7`` - The fifth value to assign to the geometry characteristic specified via ``Par2`` :

          * If ``Par2`` = AXES, the Y component of the second ellipse axis direction.

        * ``Par8`` - The sixth value to assign to the geometry characteristic specified via ``Par2`` :

          * If ``Par2`` = AXES, the Z component of the second ellipse axis direction.

        **Command Specifications for Action= DELE**

        .. _adpci_dele:

        * ``Par1`` - :ref:`adpci` ID (default = ALL).

        **Command Specifications for Action= LIST**

        .. _adpci_ncontour:

        * ``Par1`` - :ref:`adpci` ID number (default = ALL).

        Notes
        -----

        .. _adpci_notes:

        For :ref:`adpci`,GEOM,LCS, the ellipse center locates at the origin of the local coordinate system.
        The local coordinate system Y axis defines the plane normal of the ellipse, and X and Z axes define
        two orientations of the ellipse. (The LCS argument is equivalent to combining the CENTER and AXES
        arguments. Separate :ref:`adpci`,GEOM commands to specify those arguments are therefore not issued.)

        For more information about using :ref:`adpci` in a crack-initiation analysis, see `SMART Method for
        Crack-Initiation Simulation
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/fractSMARTinit.html#SMARTcrackinitexamp>`_
        """
        command = (
            f"ADPCI,{action},{par1},{par2},{par3},{par4},{par5},{par6},{par7},{par8}"
        )
        return self.run(command, **kwargs)

    def aerocoeff(
        self,
        aeromodetype: str = "",
        aeromappedfilenames: str = "",
        aerospecs: str = "",
        aeroscalar: str = "",
        nblades: str = "",
        autofileread: str = "",
        **kwargs,
    ):
        r"""Computes the aero-damping and stiffness coefficients and writes them to an APDL array.

        Mechanical APDL Command: `AEROCOEFF <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_AEROCOEFF.html>`_

        **Command default:**

        .. _AEROCOEFF_default:

        No defaults are available for the :ref:`aerocoeff` command.

        Parameters
        ----------
        aeromodetype : str
            Mode type to be used.

            * ``BLADE`` - Non-cyclic cantilevered blade mode (default)

        aeromappedfilenames : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_AEROCOEFF.html>`_ for
            further information.

        aerospecs : str
            Name of numerical array containing data organized to correspond to the ``AeroMappedFiles``
            array. See the :ref:`AEROCOEFF_notes` section for specific information that must be in the
            array.

        aeroscalar : str
            Scaling value(s) to handle any modal scaling difference between structural and CFD modes. The
            values can be entered as a scalar or 1-dimensional array. (each scaling value defaults to 1)

        nblades : str
            Number of blades.

        autofileread : str
            Key to automatically read and use values from CFD file header.

            * ``0 (OFF or NO)`` - Do not read scaling values or nodal diameter from the CFD file header.
              (default)

            * ``1 (ON or YES)`` - Read scaling values (labeled ``Mode Multiplier`` in CFD file) from CFD file
              header. The scaling values read will be used in calculations and the ``AeroScalar`` input will be
              ignored. The nodal diameter values will be used to cross check the value of i (input through
              ``AeroSpecs`` array).

        Notes
        -----

        .. _AEROCOEFF_notes:

        The :ref:`aerocoeff` command is designed to `generate an array of aerodynamic coefficients
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cycsym/cycsym_aero_coupling.html#>`_
        that can be used in a cyclic mode-superposition harmonic response analysis using the :ref:`cycfreq`
        ,AERO command to represent aerodynamic stiffness and damping. These aerodynamic coefficients can
        also be used in a damped modal analysis phase ( :ref:`cycfreq`,MODAL) of a cyclic mode-
        superposition harmonic solve. An APDL array called ``Jobname`` AeroArray is generated using the
        :ref:`aerocoeff` command. This array is compatible with the array needed for the :ref:`cycfreq`,AERO
        command.

        The format of the written array follows that of the :ref:`cycfreq`,AERO command. The array is
        formatted as follows:

        .. math::

            equation not available

        where

        * :math:`equation not available`  = the i :sup:`th` interblade phase angle (IBPA)
        * :math:`equation not available`  = the m :sup:`th` vibrating blade mode
        * :math:`equation not available`  = the n :sup:`th` blade mode generating the pressure oscillations
        * :math:`equation not available`  and  :math:`equation not available`  = the real and imaginary
          coefficients.

        Prior to issuing the :ref:`aerocoeff` command, a non-cyclic cantilevered blade modal analysis must
        be run, either stress-free or prestressed using linear perturbation. For more information, see
        `Modal Analysis
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STR_SMSUP.html>`_
        :ref:`aerocoeff` command are the same as those needed for modal restart as described in `Modal
        Analysis Restart
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/Hlp_G_BAS3_12.html#modalrestex>`_

        The ``AeroSpecs`` values are specified in a 3×r array ( :ref:`dim` ), wherer is a positive integer
        equal to the number of interblade phase angles and the pressure modes solved for in the CFD
        analysis. Each row has the structure:

        .. math::

            equation not available

        where

        * :math:`equation not available`  = the i :sup:`th` interblade phase angle (IBPA)
        * :math:`equation not available`  = the m :sup:`th` vibrating blade mode
        * :math:`equation not available`  = the n :sup:`th` blade mode generating the pressure oscillations
        At least one aerodynamic damping coefficient must be specified for each IBPA (equal to the number of
        blades) while keeping
         :math:`equation not available`  and  :math:`equation not available`  constant. If a value is not specified, the program writes an array value of      zero for both  :math:`equation not available`  and  :math:`equation not available`. The values of  :math:`equation not available`  and  :math:`equation not available`  are relative to the modes computed in the required modal analysis.

        The number of ``AeroScalar`` values must be equal to the number of pressure modes ( :math:`equation
        not available`  from  ``AeroSpecs`` ). If the number of ``AeroScalar`` values is greater than 1, the
        values must be entered by defining an :math:`equation not available`  array ( :ref:`dim` ) and
        entering the array name in the ``AeroScalar`` field. For a discussion of how ``AeroScalar`` values
        are computed, see `Scaling Aerodynamic Coupling Coefficients
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cycsym/cycsym_aero_coupling.html#>`_

        The value for ``nBlades`` should be equal to the number of sectors of the system. If there are
        multiple blades per cyclic sector, then the combination of blades on the single sector will have an
        aero coefficient value. In this case, each blade will not have a distinct aero coefficient.
        """
        command = f"AEROCOEFF,{aeromodetype},{aeromappedfilenames},{aerospecs},{aeroscalar},{nblades},{autofileread}"
        return self.run(command, **kwargs)

    def cint(
        self,
        action: str = "",
        par1: str = "",
        par2: str = "",
        par3: str = "",
        par4: str = "",
        par5: str = "",
        par6: str = "",
        par7: str = "",
        **kwargs,
    ):
        r"""Defines parameters associated with fracture-parameter calculations.

        Mechanical APDL Command: `CINT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CINT.html>`_

        Parameters
        ----------
        action : str
            Specifies action for defining or manipulating initial crack data:

            * ``NEW`` - `Command Specification for Action= NEW
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cmd/Hlp_C_CINT.html#>`_ Initiate a new
              calculation and assign an ID.

            * ``CTNC`` - `Command Specifications for Action= CTNC
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cmd/Hlp_C_CINT.html#>`_ Define the
              crack-tip node component.

            * ``SURF`` - `Command Specifications for Action= SURF
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cmd/Hlp_C_CINT.html#>`_ Define the
              crack-surface node components.

            * ``CENC`` - `Command Specifications for Action= CENC
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cmd/Hlp_C_CINT.html#>`_ Define the
              crack-extension node component, the crack-tip node, and the crack-extension direction.

            * ``TYPE`` - `Command Specifications for Action= TYPE
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cmd/Hlp_C_CINT.html#>`_ Define the type
              of calculation to perform.

            * ``DELE`` - `Command Specifications for Action= DELE
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cmd/Hlp_C_CINT.html#>`_ Delete the
              :ref:`cint` object associated with the specified ID.

            * ``NCON`` - `Command Specifications for Action= NCON
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cmd/Hlp_C_CINT.html#>`_ Specify the
              number of contours to calculate in the contour-integral calculation.

            * ``SYMM`` - `Command Specifications for Action= SYMM
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cmd/Hlp_C_CINT.html#>`_ Indicate whether
              the crack is on a symmetrical line or plane.

            * ``NORM`` - `Command Specifications for Action= NORM
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cmd/Hlp_C_CINT.html#>`_ Define the
              crack-plane normal.

            * ``UMM`` - `Command Specifications for Action= UMM
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cmd/Hlp_C_CINT.html#>`_ Enable or
              disable the unstructured-mesh method (UMM).

            * ``EDIR`` - `Command Specifications for Action= EDIR
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cmd/Hlp_C_CINT.html#>`_ Crack-assist
              extension direction.

            * ``PLOT`` - `Command Specifications for Action= PLOT
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cmd/Hlp_C_CINT.html#>`_ Plots the crack-
              front and crack-tip coordinate system.

            * ``LIST`` - `Command Specifications for Action= LIST <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cmd/Hlp_C_CINT.html#>`_ List the **CINT** commands issued, or the elements used, in fracture-parameter calculations.

            * ``CXFE`` - `Command Specifications for Action= CXFE
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cmd/Hlp_C_CINT.html#>`_ Define the
              crack-tip element or crack-front element set. Valid for `XFEM-based crack-growth
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/Hlp_G_FRACXFEM.html#fracxfemreferences>`_
              analysis only.

            * ``RADIUS`` - `Command Specifications for Action= RADIUS
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cmd/Hlp_C_CINT.html#>`_ Define the
              radius at which the given value is to be evaluated. Valid for XFEM-based crack-growth analysis only.

            * ``RSWEEP`` - `Command Specifications for Action= RSWEEP
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cmd/Hlp_C_CINT.html#>`_ Define the
              minimum and maximum sweep angle from existing crack direction. Valid for XFEM-based crack-growth
              analysis only.

            * ``INIT`` - `Command Specifications for Action= INIT
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cmd/Hlp_C_CINT.html#>`_ SMART crack-
              initiation ID.

            * ``CSFL`` - `Command Specifications for Action= CSFL
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cmd/Hlp_C_CINT.html#>`_ Convert initial-
              stress data to crack-surface traction loading.

        par1 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CINT.html>`_ for further
            information.

        par2 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CINT.html>`_ for further
            information.

        par3 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CINT.html>`_ for further
            information.

        par4 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CINT.html>`_ for further
            information.

        par5 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CINT.html>`_ for further
            information.

        par6 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CINT.html>`_ for further
            information.

        par7 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CINT.html>`_ for further
            information.

        Other Parameters
        ----------------
        **Command Specification for Action= NEW**

        .. _cint_new:

        * ``Par1`` - :ref:`cint` ID number.

        **Command Specifications for Action= CTNC**

        .. _cint_ctncomp:

        * ``Par1`` - Crack-tip node component name (must be 32 characters or less).

        * ``Par2`` - Crack-extension direction calculation-assist node. Any node on the open side of the
          crack.

        * ``Par3`` - Crack front``s end-node crack-extension direction override flag:

          * ``0`` - Align the extension direction with the edges attached at the two end nodes of the crack
            front (default).

          * ``1`` - Align the extension direction to be perpendicular to the crack front.

        **Command Specifications for Action= SURF**

        .. _cint_ctnsurf:

        * ``Par1`` - Crack-surface node component 1 (top or bottom crack face). (Component name must be 32
          characters or less.)

        * ``Par2`` - Crack-surface node component 2 (top or bottom crack face, but the opposite of ``Par1``
          ). (Component name must be 32 characters or less.)

        **Command Specifications for Action= CENC**

        .. _cint_cencomp:

        * ``Par1`` - Crack-extension node component name ( :ref:`cm` ). (Must be 32 characters or less.)

        * ``Par2`` - Crack-tip node. The crack-tip node defaults to the first node of the crack-extension
          node component.

        * ``Par3, Par4`` - Coordinate system number ( ``Par3`` ) and the number of the axis that is
          coincident with the crack direction ( ``Par4`` ). When these parameters are defined, ``Par5``,
          ``Par6`` and ``Par7`` are ignored.

        * ``Par5, Par6, Par7`` - Global x, y, and z components of the crack-extension direction vector. (
          ``Par3`` and ``Par4`` must be blank.)

        **Command Specifications for Action= TYPE**

        .. _cint_type:

        * ``Par1`` - Type of calculation to perform:

          * ``JINT`` - Calculate `J-integral
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/frac_parmcalctypes.html#strjintcalcmethod>`_
            (default).

          * ``SIFS`` - Calculate `stress-intensity factors
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/frac_parmcalctypes.html#strcalcSIFs>`_.

          * ``TSTRESS`` - Calculate `T-stress
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/frac_parmcalctypes.html#strtstrcalculating>`_.

          * ``MFOR`` - Calculate `material forces
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/frac_parmcalctypes.html#strcalcmatforce>`_.

          * ``CSTAR`` - Calculate `C\2-integral
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/frac_parmcalctypes.html#>`_.

          * ``VCCT`` - Calculate `energy-release rate
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/frac_parmcalctypes.html#strcalcERRproc>`_
            using the VCCT method.

          * ``PSMAX`` - Calculate circumferential stress at the location where :math:`equation not available`
            when sweeping around the crack tip at the                                        given radius. Valid
            in an  `XFEM- based crack-growth
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/Hlp_G_FRACXFEM.html#fracxfemreferences>`_
            analysis only.

          * ``STTMAX`` - Calculate maximum circumferential stress when sweeping around the crack tip at the
            given radius. Valid in an XFEM-based crack-growth analysis only.

        * ``Par2`` - Auxiliary stress fields and strategy for **3D**  `stress-intensity factors
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/frac_parmcalctypes.html#strcalcSIFs>`_
        ( ``Par1`` = SIFS) calculations:

          * ``0`` - The plane-strain auxiliary fields are used at the interior nodes along the crack front.
            The stress- intensity factors at the end nodes of the crack front are set to copy the stress-
            intensity factors at the adjacent nodes. (Default.)

          * ``1`` - The plane-stress auxiliary fields are used over the entire crack front.

          * ``2`` - The plane-strain auxiliary fields are used over the entire crack front.

        **Command Specifications for Action= DELE**

        .. _cint_dele:

        * ``Par1`` - :ref:`cint` ID (default = ALL).

        **Command Specifications for Action= NCON**

        .. _cint_ncontour:

        * ``Par1`` - Number of contours to be calculated.

        **Command Specifications for Action= SYMM**

        .. _cint_symmetric:

        * ``Par1`` - * ``OFF, 0, or NO`` - No symmetry (default).

          * ``ON, 1, or YES`` - Symmetric about the crack line/plane.

        **Command Specifications for Action= UMM**

        .. _cint_umm:

        * ``Par1`` - * ``OFF, 0, or NO`` - Disable the `unstructured-mesh method (UMM)
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/fracumm.html#fracummassump>`_
            (default).

          * ``ON, 1, or YES`` - Enable the UMM.

        **Command Specifications for Action= NORM**

        .. _cint_normal:

        * ``Par1`` - Coordinate system number (default = 0, global Cartesian).

        * ``Par2`` - Axis of coordinate system (default = 2, global Cartesian Y-axis).

        **Command Specifications for Action= EDIR**

        .. _cint_caextdir:

        * ``ITYPE`` - Input type for the crack-assist extension direction. Valid values are CS (coordinate
          system number) or COMP (component x or y extension direction).

        * ``Par2`` - If ``ITYPE`` = CS, the coordinate system number.

          If ``ITYPE`` = COMP, the x component of the crack-assist extension direction.

        * ``Par3`` - If ``ITYPE`` is CS, the axis representing the crack-assist extension direction.

          If ``ITYPE`` = COMP, the y component of the crack-assist extension direction.

        * ``Par4`` - For ``ITYPE`` = CS, this value is not specified.

          For ``ITYPE`` = COMP, the z component of the crack-assist extension direction.

        * ``Par5`` - A reference node on the crack front attached to the crack-assist extension direction.
          To accurately calculate and flip the crack-extension directions, the crack-assist extension
          direction defined at this node is rotated as the tangent along the crack front rotates. This
          capability is useful when the crack-extension directions vary by more than 180 degrees along the
          crack front.

        **Command Specifications for Action= PLOT**

        .. _cint_plot:

        * ``Par1`` - Crack ID.

        * ``Par2`` - 0 -- Disable plotting of crack-tip coordinate system.

          1 -- Enable plotting of crack-tip coordinate system (default).

          Color codes are white for the crack-extension direction, green for the crack normal, and red for the
          direction tangential to the crack front. To clear or delete the plots, issue :ref:`annot`.

        **Command Specifications for Action= LIST**

        .. _cint_list:

        * ``CrackID`` - Crack ID. Default = ALL.

        * ``Par2`` - No value -- Lists the :ref:`cint` commands issued for the crack. ``Par3`` and ``Par4``
          are ignored.

          ELEM -- Lists the elements used in the fracture-parameter calculation.

        * ``Par3`` - Node number on the crack front/tip. Default = ALL. Valid only when ``Par2`` =ELEM.

        * ``Par4`` - Contour number around the crack front/tip. Default = ALL. Valid only when ``Par2``
          =ELEM.

        **Command Specifications for Action= CXFE**

        .. _cint_cxfe:

        * ``Par1`` - Crack-tip element number or crack-front component name. (Component name must be 32
          characters or less.)

        **Command Specifications for Action= RADIUS**

        .. _cint_radius:

        * ``Par1`` - Radius at which a value is evaluated (used with :ref:`cint`,TYPE,PSMAX or
          :ref:`cint`,TYPE,STTMAX only).

        **Command Specifications for Action= RSWEEP**

        .. _cint_rsweep:

        * ``Par1`` - Number of intervals for the sweep.

        * ``Par2`` - Minimum angle of the sweep.

        * ``Par3`` - Maximum angle of the sweep

        **Command Specifications for Action= INIT**

        .. _cint_init:

        * ``Par1`` - :ref:`adpci` ID number. The data associated with the :ref:`adpci` ID is connected to
          the :ref:`cint` data set to define `crack-initiation analysis
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/fractSMARTinit.html#SMARTcrackinitexamp>`_
          details (such as crack location and shape, initiation criteria, etc.).

        **Command Specifications for Action= CSFL**

        .. _cint_csfl:

        `Initial-stress
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_adv/Hlp_G_INSTWRITVAL.html>`_ data (
        mesh-independent ) are converted to a traction load acting on the crack-surfaces (specified via
        :ref:`cint`,SURF). The traction is applied as a step load for all substeps.

        The initial-stress data points are specified at various spatial locations in the global Cartesian
        coordinate system ( :ref:`csys` ). The data is required in the vicinity of the crack surfaces only.
        The program interpolates the initial stress at the centroid of each element face of the crack
        surfaces, then determines the equivalent traction at the element face based on its orientation.

        For more information, see and

        Notes
        -----

        .. _cint_notes:

        Initiate a new calculation via the ``Action`` = NEW parameter. Subsequent :ref:`cint` commands (with
        parameters other than NEW) define the input required for the fracture-parameter calculations.

        The simplest method is to define crack information via ``Action`` = CTNC; however, this method
        limits you to only one node for a given location along the crack front. Use the CTNC option only
        when all nodes that define the crack front lie in a single plane.

        For ``Action`` = SURF, ``Par1`` and ``Par2`` can be the top or bottom crack-face node component. No
        order is required, provided that if one value the top crach-face node component, the other must be
        the bottom, and vice-versa. This option is valid only with :ref:`cgrow` for crack-growth simulation.

        To define crack information at multiple locations along the crack front, use ``Action`` = CENC. You
        can issue :ref:`cint`,CENC, ``Par1``, etc. multiple times to define the crack-extension node
        component, the crack tip, and the crack-extension directions at multiple locations along the crack
        front.

        Although you can vary the sequence of your definitions, all specified crack-tip nodes must be at the
        crack front, and no crack-tip node can be omitted.

        You can define the crack-extension direction directly by specifying either ``Action`` = CENC or
        ``Action`` = NORM.

        The crack-assist extension direction ( ``Action`` = EDIR) provides a generic extension direction
        when ``Action`` = CTNC. It helps to define crack-extension directions based on the connectivity of
        the crack-front elements. For a 2D case when the crack tangent cannot be calculated, the program
        uses the provided crack-assist extension direction directly.

        For an `XFEM-based crack-growth
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/Hlp_G_FRACXFEM.html#fracxfemreferences>`_
        analysis:

        * ``Action`` = CTNC, CENC, NCON, SYMM, UMM, or EDIR have no effect.

        * ``Action`` = CXFE, RADIUS, or RSWEEP are XFEM-specific and invalid for any other type of crack-
          growth analysis.

        * For :ref:`cint`,TYPE, only ``Par1`` = PSMAX or STTMAX are valid. Other ``Par1`` values have no
          effect.

        The stress-intensity factors calculation ( :ref:`cint`,TYPE,SIFS) applies only to isotropic linear
        elasticity. Use only one material type for the crack-tip elements that are used for the
        calculations.

        When calculating energy release rates ( :ref:`cint`,TYPE,VCCT), do not restrict the results from
        being written to the database ( :ref:`config`,NOELDB,1) after solution processing; otherwise,
        incorrect and potentially random results are possible.

        Fracture-parameter calculations based on domain integrations such as stress-intensity factors,
        J-integral, or material force are not supported when contact elements exist inside the domain. The
        calculations may become path-dependent unless the contact pressure is negligible.

        For ``Action`` = UMM, the default value can be OFF or ON `depending on the element type
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/fracumm.html#cintondefaulttab>`_.
        The :ref:`cint` command overrides the default setting for the given element.

        The :ref:`cint` command supports only strain data for initial state (
        :ref:`inistate`,SET,DTYP,EPEL). Other initial-state capabilities are not supported.

        For more information about using the :ref:`cint` command, including supported element types and
        material behavior, see `Calculating Fracture Parameters
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/fracumm.html>`_
        """
        command = f"CINT,{action},{par1},{par2},{par3},{par4},{par5},{par6},{par7}"
        return self.run(command, **kwargs)

    def cycexpand(
        self,
        wn: str = "",
        option: str = "",
        value1: str = "",
        value2: str = "",
        **kwargs,
    ):
        r"""Graphically expands displacements, stresses and strains of a cyclically symmetric model.

        Mechanical APDL Command: `/CYCEXPAND <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CYCEXPAND_sl.html>`_

        Parameters
        ----------
        wn : str
            The window number to which the expansion applies. Valid values are 1 through 5. The default
            value is 1. The window number applies only to the AMOUNT argument.

        option : str
            One of the following options:

            * ``ON`` - Activates cyclic expansion using the previous settings (if any). If no previous settings
              exist, this option activates the default settings. This option is default.

            * ``DEFAULT`` - Resets cyclic expansion to the default settings.

            * ``OFF`` - Deactivates cyclic expansion.

            * ``STATUS`` - Lists the current cyclic expansion settings.

            * ``AMOUNT`` - The number of repetitions or the total angle.

              * ``Value1`` - NREPEAT

              * ``Value2`` - The number of repetitions. The default is the total number of sectors in 360 degrees.

              or

              * ``Value1`` - ANGLE

              * ``Value2`` - The total angle in degrees. The default is 360.

            * ``WHAT`` - A specified portion or subset of the model to expand:

              * ``Value1`` - The component name of the elements to expand. The default is all selected components.

            * ``EDGE`` - Sector edge display key. Possible ``Value1`` settings are:

              * ``-1`` - Suppresses display of edges between sectors even if the cyclic count varies between active windows.
                This setting is not valid for cyclic mode-superposition (MSUP) harmonic analyses.

                .. warning::

                    Plots with fewer than the maximum number of repetitions may have missing element faces at the
                    sector boundaries.
              * ``0 or OFF`` - Averages stresses or strains across sector boundaries. This value is the default
                (although the default reverts to 1 or ON if the cyclic count varies between active windows).

              * ``1 or ON`` - No averaging of stresses or strains occurs, and sector boundaries are shown on the
                plot. This setting is not valid for cyclic MSUP harmonic analyses.

            * ``PHASEANG`` - Possible ``Value1`` settings are:

              * ``n`` - The phase angle shift in degrees. The valid range for ``n``  is 0 through 360. The default
                is 0. For a modal solution, this value is typically the phase angle obtained via the :ref:`cycphase`
                command. The expanded modal results are printed or displayed for the specified phase angle shift.

              * ``AMPLITUDE (or, n ≥ 360)`` - The amplitude is reported, except for the following circumstances where the amplitude solution is
                not valid:

                * non-component results (such as equivalent stress)

                * modal analyses (no amplitude is calculated, and the expanded modal results are printed or
                  displayed at a phase angle of 360º).

              * ``SWEEP`` - For a mode-superposition harmonic solution, the maximum values across a phase angle
                sweep are reported.

        value1 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CYCEXPAND_sl.html>`_ for
            further information.

        value2 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CYCEXPAND_sl.html>`_ for
            further information.

        Notes
        -----

        .. _s-CYCEXPAND_notes:

        In preprocessing, the :ref:`cycexpand` command verifies a cyclically symmetric model by graphically
        expanding it partially or through the full 360 degrees.

        For the postprocessing plot nodal solution ( :ref:`plnsol` ) operation, the command graphically
        expands displacements, stresses and strains of a cyclically symmetric model partially or though the
        full 360 degrees by combining the real (original nodes and elements) and imaginary (duplicate nodes
        and elements) parts of the solution.

        For the print nodal solution ( :ref:`prnsol` ) operation, the command expands the printed output of
        displacements or stresses on a sector-by-sector basis. To learn more about specific :ref:`prnsol`
        behaviors in cyclic analyses, see `Using the /CYCEXPAND Command
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cycsym/advcycpost.html#>`_

        Use of the :ref:`cycexpand` command does not change the database. The command does not modify the
        geometry, nodal displacements or element stresses.

        The command affects element and result plots only. It has no effect on operations other than plot
        element solution ( :ref:`plesol` ), plot nodal solution ( :ref:`plnsol` ), print nodal solution (
        :ref:`prnsol` ), and calculate harmonic solution ( :ref:`cyccalc` ). Operations other than
        :ref:`plesol`, :ref:`plnsol`, :ref:`prnsol`, or :ref:`cyccalc` work on the unprocessed real and
        imaginary parts of a cyclic symmetry solution

        If you issue a :ref:`cycexpand`, OFF command, you cannot then expand the model by simply issuing
        another :ref:`cycexpand` command (for example, to specify an NREPEAT value for the number of
        repetitions). In such a case, you must specify :ref:`cycexpand`, ON, which activates expansion using
        the previous settings (if any) or the default settings.

        The command requires PowerGraphics and will turn PowerGraphics on ( :ref:`graphics`, POWER ) if not
        already active. Any setting which bypasses PowerGraphics (for example, :ref:`pbf` ) also bypasses
        cyclic expansion; in such cases, the :ref:`cycexpand` command displays unprocessed real and
        imaginary results.

        The :ref:`cycphase` command uses full model graphics ( :ref:`graphics`, FULL ) to compute peak
        values. Because of this, there may be slight differences between max/min values obtained with
        :ref:`cycphase`, and those obtained via :ref:`cycexpand`, which uses power graphics (
        :ref:`graphics`, POWER ).

        For PHASEANG = AMPLITUDE (or 360) with a cyclic full harmonic solution, the only appropriate
        coordinate system is the solution coordinate system ( :ref:`rsys`,SOLU).

        Load case operations ( :ref:`lcoper` ) are not valid during a cyclic expansion using
        :ref:`cycexpand`.

        To learn more about analyzing a cyclically symmetric structure, see the `Cyclic Symmetry Analysis
        Guide <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cycsym/cycsym_example.html>`_.
        """
        command = f"/CYCEXPAND,{wn},{option},{value1},{value2}"
        return self.run(command, **kwargs)

    def cycfreq(
        self,
        option: str = "",
        value1: str = "",
        value2: str = "",
        value3: str = "",
        value4: str = "",
        value5: str = "",
        **kwargs,
    ):
        r"""Specifies solution options for a cyclic symmetry mode-superposition harmonic analysis.

        Mechanical APDL Command: `CYCFREQ <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CYCFREQ.html>`_

        **Command default:**

        .. _CYCFREQ_default:

        No defaults are available for the :ref:`cycfreq` command. You must specify an ``Option`` label when
        issuing this command. Other values which may be necessary depend upon which ``Option`` label you
        specify.

        Parameters
        ----------
        option : str
            One of the following options:

            * ``AERO`` - Specify the array containing the aerodynamic damping coefficients.

              * ``Value1`` - The name of the array containing the aerodynamic stiffness damping coefficients.

            * ``BLADE`` - Blade information required for a mistuning or aerodamping analysis.

              * ``Value1`` - The name of the nodal component containing the blade boundary nodes at the blade-to-
                disk interface. Also include boundary nodes at any shroud interfaces.

              * ``Value2`` - The name of the element component containing the blade elements.

              * ``Value3`` - The number of blade modes to include in the CMS reduction.

              * ``Value4`` - The lower bound of the frequency range of interest. This value is optional.

              * ``Value5`` - The upper bound of the frequency range of interest. This value is optional.

            * ``DEFAULT`` - Set the default cyclic harmonic solution settings.

            * ``EO`` - Excitation engine order.

              * ``Value1`` - An integer value indicating the the excitation order. The loadings on the other
                sectors will be related to the loading on the base sector based on the engine order phase shift.

              * ``Value2`` - The name of the Mechanical APDL array containing the modal forces corresponding to the modes
                kept in the mode-superpostion analysis.

            * ``MIST`` - Mistuning parameters.

              * ``Value1`` - The type of mistuning:

                * ``K`` - Stiffness (frequency) mistuning

              * ``Value2`` - The name of the array containing the stiffness mistuning parameters.

            * ``MODAL`` - Specifies if a damped modal analysis should be performed on the reduced system.

              * ``Value1`` - On/Off key.

                * ``0 (OFF or NO)`` - No modal solution. Perform the harmonic solution.

                * ``1 (ON or YES)`` - Perform a damped modal analysis of the reduced system in order to obtain the
                  complex frequencies. The harmonic solution is not performed.

              * ``Value2`` - Number of modes for the damped modal analysis.

              * ``Value3`` - The beginning, or lower end, of the frequency range of interest (in Hz).

              * ``Value4`` - The ending, or upper end, of the frequency range of interest (in Hz).

            * ``RESTART`` - Defines the point at which to restart the harmonic analysis.

              * ``Value1`` - The restart point:

                * ``OFF`` - No restart (default)

                * ``SWEEP`` - Restart for a new frequency sweep range ( :ref:`harfrq` )

                * ``MIST`` - Restart for new mistuning parameters (new mistuning arrays)

            * ``USER`` - Causes the program to call for a user-defined solution.

              * ``Value1-5`` - Values passed down to the user-defined solution.

            * ``STATUS`` - List the harmonic solution option settings active for the cyclic model.

        value1 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CYCFREQ.html>`_ for
            further information.

        value2 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CYCFREQ.html>`_ for
            further information.

        value3 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CYCFREQ.html>`_ for
            further information.

        value4 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CYCFREQ.html>`_ for
            further information.

        value5 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CYCFREQ.html>`_ for
            further information.

        Notes
        -----

        .. _CYCFREQ_notes:

        The program solves a cyclically symmetric model (set up via the :ref:`cyclic` command during
        preprocessing) at the harmonic indices specified via the :ref:`cycopt` command.

        When ``Option`` = AERO, the aerodynamic coefficients are specified in a 5×(N×r) array ( :ref:`dim`
        ), where N is the number of blades and r can be any positive integer. Each column has the structure:

        .. math::

            equation not available

        where:

        * :math:`equation not available`  = the i :sup:`th` interblade phase angle (IBPA)
        * :math:`equation not available`  = the m :sup:`th` vibrating blade mode
        * :math:`equation not available`  = the n :sup:`th` blade mode generating the pressure oscillations
        * :math:`equation not available`  and  :math:`equation not available`  = the real and imaginary
          coefficients.
        One aerodynamic damping coefficient must be specified for each IBPA (equal to the number of blades)
        while keeping m and n constant.

        The following table shows how the IBPA index ( :math:`equation not available` ) relates to other
        quantities for a system with 22 blades:

        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.

        The :ref:`cycfreq`,AERO command is only valid if :ref:`cycfreq`,BLADE is also specified. The blade
        mode numbers, m and n, are relative to the values kept in the :ref:`cycfreq`,BLADE command.

        For constant (frequency-independent) mistuning, the stiffness parameters are specified in an N×1
        array ( :ref:`dim` ) where N is the number of blades.

        For stiffness mistuning, each row entry represents the deviation of Young``s modulus from nominal,
        :math:`equation not available`  (or equivalently, the ratio of the frequency deviationsquared). Each
        frequency can also be independently mistuned, in whichcase the array is NtimesM, where M is the
        number of blade frequencies( ``Value3`` of :ref:`cycfreq`,BLADE). The entries in each row therefore
        correspond to the ratio of the mistuned frequency to the tuned frequency squared minus one:

        .. math::

            equation not available

        The USER option activates the solution macro :file:`CYCMSUPUSERSOLVE.MAC`. The normal solution is
        skipped. You may implement your own mistuning solution using APDL and APDL Math operations, or call
        your own program for the solution.

        The :ref:`cycfreq` command is valid in the preprocessing and solution stages of an analysis.

        The :ref:`cycfreq`,MODAL,ON command writes modal frequencies to the output file. No other
        postprocessing is available for this modal solve.

        When using :ref:`cycfreq`,RESTART, only mistuning parameters or frequency range may be changed. All
        other changes in parameters are ignored. This type of restart can only be performed by exiting the
        current mistuning solution using :ref:`finish` and re-entering the solution phase using
        :ref:`slashsolu` and then calling the desired :ref:`cycfreq`,RESTART command.

        To learn more about analyzing a cyclically symmetric structure, see the `Cyclic Symmetry Analysis
        Guide <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cycsym/cycsym_example.html>`_.

        **Example Usage**

        .. _CYCFREQ_ExUsage:

        `Analysis and Solution Controls section of the Technology Showcase Example Problem: Forced-response
        analysis of a mistuned bladed disk with aerodamping
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_tec/tecmistuninganalysis.html#tecmistuning_nonlinmsup_mistuned>`_.

        For an example demonstrating how to apply modal loads directly in the cyclic harmonic analysis step
        of a mode-superposition harmonic cyclic symmetry analysis, see.
        """
        command = f"CYCFREQ,{option},{value1},{value2},{value3},{value4},{value5}"
        return self.run(command, **kwargs)

    def cyclic(
        self,
        nsector: str = "",
        angle: str = "",
        kcn: str = "",
        name: str = "",
        usrcomp: str = "",
        usrnmap: str = "",
        **kwargs,
    ):
        r"""Specifies a cyclic symmetry analysis.

        Mechanical APDL Command: `CYCLIC <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CYCLIC.html>`_

        **Command default:**

        .. _CYCLIC_default:

        The default :ref:`cyclic` command (issuing the command with no arguments) detects the number of
        sectors ( ``NSECTOR`` ), the sector angle ( ``ANGLE`` ), and the coordinate system ( ``KCN`` ) based
        upon the existing solid or finite-element model. The command also detects sector low- and high-edge
        components in most cases and assigns the default root name CYCLIC to the components.

        Parameters
        ----------
        nsector : str
            The number of sectors in the full 360 degrees, or one of the following options:

            * ``STATUS`` - Indicates the current cyclic status.

            * ``OFF`` - Resets model to normal (non-cyclic) status and removes the duplicate sector if it
              exists. This option also deletes automatically detected edge components (generated when ``USRCOMP``
              = 0).

            * ``UNDOUBLE`` - Removes the duplicate sector if it exists. The duplicate sector is created during
              the solution ( :ref:`solve` ) stage of a modal cyclic symmetry analysis.

              The duplicate sector is necessary for displaying cyclic symmetry analysis results during
              postprocessing ( :ref:`post1` ).

            If you specify a value of STATUS, OFF or UNDOUBLE, the command ignores all remaining arguments.

        angle : str
            The sector angle in degrees.

        kcn : str
            An arbitrary reference number assigned to the cyclic coordinate system. The default value of 0
            specifies automatic detection.

        name : str
            The root name of sector low- and high-edge components (line, area, or node components). The default
            root name (when ``USRCOMP`` = 0) is CYCLIC. A root name that you specify can contain up to 11
            characters.

            The naming convention for each low- and high-edge component pair is either of the following:

            * ``Name`` _m ``xx`` l, ``Name`` _m ``xx`` h (potentially matched node patterns)
            * ``Name`` _u ``xx`` l, ``Name`` _u ``xx`` h (potentially unmatched node patterns)

            The ``Name`` value is the default ( CYCLIC ) or specified root name and ``xx`` is the component pair
            ID number (sequential, starting at 01).

        usrcomp : str
            The number of pairs of user-defined low- and high-edge components on the cyclic sector (if any).
            The default value of 0 specifies automatic detection of sector edges; however, the automatic
            setting is not valid in all cases. (For more information, see the Notes section below.) If the
            value is greater than 0, no verification of user-defined components occurs.

        usrnmap : str
            The name of a user-defined array specifying the matching node pairs between the sector low and high
            edges. Valid only when ``USRCOMP`` = 0. Skips the automatic detection of sector edges. Node pairs
            may be input in any order, but the low edge node must be the first entry in each pair.

            .. code:: apdl

               *DIM,MYMAP,ARRAY,2,14	! specifying 14 low-high edge node pairs
               *set,mymap(1, 1), 107, 108	! low node 107 <> high node 108
               *set,mymap(1, 2), 147, 211	! low node 147 <> high node 211
               *set,mymap(1, 3), 110, 109	! low node 110 <> high node 109
                       ! etc for node pairs 4 through 14
               cyclic,12,,1,,,MYMAP		! use array MYMAP to generate cyclic CEs

        Notes
        -----

        .. _CYCLIC_notes:

        You can input your own value for ``NSECTOR``, ``ANGLE`` or ``KCN`` ; if you do so, the command
        verifies argument values before executing.

        When ``USRCOMP`` = 0 and ``UsrNMap`` = blank (default), the :ref:`cyclic` command automatically
        detects `low- and high-edge components
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cycsym/advcycedgecomp.html#>`_ for
        models that consist of any combination of line, area, or volume elements. If a solid model exists,
        however, the command uses only the lines, areas, and/or volumes to determine the low- and high-edge
        components; the elements, if any, are ignored.

        Nodes will be automatically rotated unless :ref:`cycopt`,USRROT,YES has been specified.

        If you issue a :ref:`cycopt`,TOLER command to set a tolerance for edge-component pairing before
        issuing the :ref:`cyclic` command, the :ref:`cyclic` command uses the specified tolerance when
        performing automatic edge-component detection.

        For 2D models, autodetection does not consider the :ref:`csys`,5 or :ref:`csys`,6 coordinate system
        specification. Autodetection for 180 degree (two-sector) models is not possible unless a central
        hole exists.

        The :ref:`cyclic` command sets values and keys so that, if possible, the area-mesh ( :ref:`amesh` )
        or volume-mesh ( :ref:`vmesh` ) command meshes the sector with matching node and element face
        patterns on the low and high edges. (The command has no effect on any other element-creation
        command.)

        Issue the :ref:`cyclic` command prior to the meshing command to, if possible, produce a mesh with
        identical node and element patterns on the low and high sector edges. Only the :ref:`amesh` or
        :ref:`vmesh` commands can perform automated matching. (Other meshing operation commands such as
        :ref:`vsweep` cannot.) If you employ a meshing operation other than :ref:`amesh` or :ref:`vmesh`,
        you should ensure that node and element face patterns match, if desired. The :ref:`cyclic` command
        output indicates whether each edge-component pair has or can produce a matching node pair.

        A cyclic solution (via the :ref:`solve` command) allows dissimilar mesh patterns on the extreme
        boundaries of a cyclically symmetric model. The allowance for dissimilar patterns is useful when you
        have only finite-element meshes for your model but not the geometry data necessary to remesh it to
        obtain identical node patterns. In such cases, it is possible to obtain solution results, although
        perhaps at the expense of accuracy. A warning message appears because results may be degraded near
        the sector edges.

        The constraint equations (CEs) that tie together the low and high edges of your model are generated
        at the solution stage of the analysis from the low- and high-edge components (and nowhere else). You
        should verify that automatically detected components are in the correct locations and that you can
        account for all components; to do so, you can list ( :ref:`cmlist` ) or plot ( :ref:`cmplot` ) the
        components.

        If you issue the :ref:`cyclic` command after meshing and have defined element types with rotational
        degrees of freedom (DOFs), Mechanical APDL generates cyclic CEs for rotational DOFs that may not
        exist on
        the sector boundaries. Issue :ref:`cycopt`,DOF to prevent unused rotational terms from being
        generated.

        Modal cyclic symmetry analysis is supported by the following eigensolvers:

        * Block Lanczos ( :ref:`modopt`,LANB)

        * PCG Lanczos ( :ref:`modopt`,LANPCG)

        * Super Node ( :ref:`modopt`,SNODE)

        * Subspace ( :ref:`modopt`,SUBSP)

        To learn more about analyzing a cyclically symmetric structure, see the `Cyclic Symmetry Analysis
        Guide <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cycsym/cycsym_example.html>`_.

        When using the :ref:`cyclic` command to automatically detect the sector, if an area is defined with
        the :ref:`al` command, the lines need to be oriented to form the closed curve.
        """
        command = f"CYCLIC,{nsector},{angle},{kcn},{name},{usrcomp},{usrnmap}"
        return self.run(command, **kwargs)

    def cycopt(
        self,
        option: str = "",
        value1: str = "",
        value2: str = "",
        value3: str = "",
        value4: str = "",
        value5: str = "",
        value6: str = "",
        value7: str = "",
        **kwargs,
    ):
        r"""Specifies solution options for a cyclic symmetry analysis.

        Mechanical APDL Command: `CYCOPT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CYCOPT.html>`_

        Parameters
        ----------
        option : str
            Cyclic symmetry analysis option. There is no default. You must choose o ne of the following options:

            * ``BCMULT`` - Controls whether cyclic sector array parameter names are reused or created new for multiple
              entities.

              * ``Value1`` - The flag value.

                * ``0 (OFF or NO)`` - Create new array parameter names (default)

                * ``1(ON or YES)`` - Reuse array parameter names

            * ``COMBINE`` - For linear `static cyclic symmetry analysis
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cycsym/advcycstaticans.html#cycsym_postproc_stat>`_
              with `non-cyclically symmetric loading
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cycsym/advcycsolarch.html#>`_ only,
              expands and combines all harmonic index solutions and writes them to the results file during the
              solution phase of the analysis.

              * ``Value1`` - The flag value.

                * ``0 (OFF or NO)`` - Disable combining of harmonic index solutions (default)

                * ``1 (ON or YES)`` - Enable combining of harmonic index solutions

            * ``DEFAULT`` - Set the default cyclic solution settings.

            * ``DOF`` - The degrees of freedom to couple from the nodes on the low sector boundary to nodes on the high
              boundary:

              * ``Value1`` - The component pair ID number.

              * ``Value2, Value3, Value4, ..., Value7`` - The constraint-equation/-coupling degree of
                freedom (DOF) for this pair. Repeat the command to add other DOFs. The default is constraint-
                equation/-coupling all applicable DOFs.

            * ``FACETOL`` - Tolerance for inclusion of surface nodes into your base sector. Autodetect defaults to 15°,
              accommodating most sections. Specify a new ``Value1`` only when extreme cut angles or complex model
              geometry cause surface nodes to be excluded. See Notes (below) for more information.

              Ansys, Inc. recommends that successful auto-detection depends more on the value of ANGTOL
              than the value of FACETOL. Please refer to `CYCOPTAuto Detection Tolerance Adjustments for Difficult
              Cases
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cycsym/advcycedgecomp.html#gadvcycopttol7>`_
              :ref:`cycopt` command.

              * ``Value1`` - The face tolerance applies only to auto detection from node/element models (already
                meshed and no solid model), and it defaults to 15°.

            * ``HINDEX`` - The `harmonic index
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cycsym/advcycmodalans.html#harmindex>`_
              ranges to be solved. Applies to static and harmonic analyses only if :ref:`CYCOPT_HINDEXValue5`
              ``Value5`` = STATIC.

              By default, the :ref:`solve` command loops through all available harmonic indices. `Static
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cycsym/advcycstaticans.html#cycsym_postproc_stat>`_
              and `harmonic
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cycsym/advcycmodalans.html#harmindex>`_
              analyses only solve harmonic indices required for the applied loads. All other analyses solve them
              all.

              * ``EVEN / ODD`` - For low-frequency electromagnetic analysis only, EVEN specifies a symmetric
                solution and ODD specifies an antisymmetric solution.

                The value you specify is based on the `harmonic index
                <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cycsym/advcycmodalans.html#harmindex>`_
                : EVEN (default) indicates harmonic index = 0, and ODD indicates harmonic index = ``N`` / 2 (where
                ``N`` is an integer representing the number of sectors in 360°). A value of ODD applies only when
                ``N`` is an even number.

                The :ref:`cycopt` command with this HINDEX option is cumulative. To remove an option (for example,
                EVEN), issue this command: :ref:`cycopt`,HINDEX,EVEN,,,-1

              * ``ALL`` - Solve all applicable harmonic indices. ``Value2`` must be blank.

              * ``Value1, Value2, Value3`` - Solve harmonic indices in range ``Value1`` through ``Value2`` in
                steps of ``Value3``. Repeat the command to add other ranges. The default solves all applicable
                harmonic indices.

              * ``Value4`` - The only valid value is -1. If specified, it removes ``Value1`` through ``Value2`` in
                steps of ``Value3`` from the set to solve. By default, if ``Value4`` = -1 then ``Value1`` = 0,
                ``Value2`` = 0, and ``Value3`` = 1.

              * ``Value5`` - For `static
                <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cycsym/advcycstaticans.html#cycsym_postproc_stat>`_
                and `harmonic
                <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cycsym/advcycmodalans.html#harmindex>`_
                analyses, enter either a number or STATIC:

                If ``Value5`` = <number>  the number entered sets the tolerance for determining if the Fourier
                contribution of a load is significant (default = 1.0E-5). In this case, the harmonic index selection
                is disabled.

                If ``Value5`` = STATIC the harmonic index selection is enabled, and no verification is done on the
                significance of unselected harmonic indicies. Improper selection of the harmonic index range may
                produce incomplete (incorrect) results.

            * ``LDSECT`` - Restricts subsequently defined force loads and surface loads to a specified sector. The restriction
              remains in effect until you change or reset it. This option is not available for harmonic analyses
              based on mode-superposition ( :ref:`cycopt`,MSUP,1)

              * ``Value1`` - The sector number. A value other than 0 (default) is valid for a cyclic symmetry
                analysis with `non- cyclically symmetric loading
                <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cycsym/advcycsolarch.html#>`_ only. A
                value of 0 (or ALL) resets the default behavior for cyclic loading (where the loads are identical on
                all sectors).

            * ``MOVE`` - Specifies if the program should move high- or low-edge component nodes paired within the specified
              tolerance (TOLER) to create precisely matching pairs.

              * ``Value1`` - The flag value.

                * ``0`` - Do not move edge component nodes (default)

                * ``1 or HIGH`` - Move the high-edge component nodes to precisely match the low-edge component nodes

                * ``-1 or LOW`` - Move the low-edge component nodes to precisely match the high-edge component nodes

            * ``MSUP`` - This flag is used to limit the results written to the :file:`Jobname.MODE` and :file:`Jobname.RST`
              files in a modal cyclic symmetry analysis. In a linear perturbation analysis, the modal analysis and
              the first load step of the preceding base analysis must be set to the same value.

              * ``Value1`` - The flag value.

                * ``0 (OFF or NO)`` - Write results for the base and duplicate sectors to the :file:`Jobname.MODE`
                  and :file:`Jobname.RST` files.

                * ``1 (ON or YES)`` - Write only the base sector results to the :file:`Jobname.MODE` and
                  :file:`Jobname.RST` files for use in a subsequent mode-superposition-based analysis. Default, except
                  for cyclic unsymmetric modal, LANPCG, and SNODE solutions, which use ``Value1`` = 0 as the default.
                  This option is not valid for cyclic unsymmetric modal, LANPCG, and SNODE solutions.

            * ``STATUS`` - List the solution option settings active for the cyclic model.

            * ``TOLER`` - The tolerance used to determine whether a node on the low edge is paired with a node on the high
              edge.

              * ``Value1`` - The tolerance value.

                * ``Greater than 0`` - The absolute distance tolerance for automatic sector-boundary detection and
                  low-/high-edge component node pairing

                * ``Less than 0`` - The relative tolerance for automatic sector-boundary detection and low-/high-edge component node
                  pairing. In this case, the tolerance is ``Value1`` \* ``Length``, where ``Length`` is the length of the diagonal of an imaginary box enclosing the model

                * ``0`` - Tolerance is set to -1.0 x 10 :sup:`-4` (default)

              * ``Value2`` - ``ANGTOL`` = Maximum allowable angle tolerance. (default = 0.01°)

                The valid range for ``ANGTOL`` is model dependent.

                If you input both the number of sectors and a sector angle, the angle must match 360/(number of
                sectors) within ``ANGTOL``.

                If you input only a sector angle, it must divide evenly into 360° within ``ANGTOL``.

                If you input a sector angle, the final cyclic sector must span that angle within ``ANGTOL``.

                For auto detected sector angle, the final cyclic sector must span 360/(number of sectors) within
                ``ANGTOL``, everywhere along the LOW/HIGH boundaries.

                If ``ANGTOL`` is too small, your CAD or FEA model may not be accurate enough to allow auto detection
                or verification.

                If ``ANGTOL`` is too large, you may get an unexpected or incorrect boundary definition, or in other
                cases fail to detect the boundaries.

                For some difficult cases from FEA models (not solid models), you may need to change the value of
                ``FACETOL`` to achieve auto detection. Please refer to `CYCOPTAuto Detection Tolerance Adjustments
                for Difficult Cases
                <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cycsym/advcycedgecomp.html#gadvcycopttol7>`_
                :ref:`cycopt` command.

            * ``USRROT`` - Flag specifying whether the program should override automatic nodal rotations to edge components and
              allow you to apply nodal rotations manually.

              * ``Value1`` - The flag value.

                * ``0 (OFF or NO)`` - Allow automatic node rotation (default)

                * ``1 (ON or YES)`` - Suppress automatic node rotation. If you select this option, you must apply
                  appropriate nodal rotations to all edge component nodes; otherwise, your analysis will yield
                  incorrect solution results.

                * ``LOW`` - Suppresses automatic rotation of low-edge component nodes only, allowing you to apply
                  them manually. Automatic rotation of high-edge component nodes occurs to produce the matching edge
                  nodes required for a valid cyclic solution.

                * ``HIGH`` - Suppresses automatic rotation of high-edge component nodes only, allowing you to apply
                  them manually. Automatic rotation of low-edge component nodes occurs to produce the matching edge
                  nodes required for a valid cyclic solution.

        value1 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CYCOPT.html>`_ for
            further information.

        value2 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CYCOPT.html>`_ for
            further information.

        value3 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CYCOPT.html>`_ for
            further information.

        value4 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CYCOPT.html>`_ for
            further information.

        value5 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CYCOPT.html>`_ for
            further information.

        value6 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CYCOPT.html>`_ for
            further information.

        value7 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CYCOPT.html>`_ for
            further information.

        Notes
        -----

        .. _CYCOPT_notes:

        The program solves a cyclically symmetric model (set up via the :ref:`cyclic` command during
        preprocessing) at the harmonic indices specified via the :ref:`cycopt` command.

        The :ref:`cycopt`,COMBINE option is an alternative to the :ref:`cycexpand` command and is especially
        useful for testing purposes. However, Ansys, Inc. recommends specifying COMBINE only when
        the number of sectors is relatively small. (The option expands nodes and elements into the full 360°
        and can slow postprocessing significantly.

        If you issue a :ref:`cycopt`,TOLER command to set a tolerance for `edge-component
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cycsym/advcycedgecomp.html#>`_ pairing
        before issuing the :ref:`cyclic` command, the :ref:`cyclic` command uses the specified tolerance
        when performing automatic edge-component detection.

        In cases involving `non-cyclically symmetric loading
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cycsym/advcycsolarch.html#>`_ (that is,
        when LDSECT > 0), the underlying command operations create or modify the required SECTOR tabular
        boundary condition (BC) data to apply on the appropriate sector. Therefore, it is not necessary to
        manipulate tables for situations where the applied BC is not a function of other tabular BC
        variables such as TIME, X, Y, Z, and so on.

        To delete a previously applied load on a specified sector, issue an :ref:`fdele` command.

        Because edge nodes are rotated into the cyclic coordinate system during solution, any applied
        displacements or forces on sector edges will be in the cyclic coordinate system.

        The :ref:`cycopt` command is valid in the preprocessing and solution stages of an analysis.

        To learn more about analyzing a cyclically symmetric structure, see the `Cyclic Symmetry Analysis
        Guide <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cycsym/cycsym_example.html>`_.

        Distributed-Memory Parallel (DMP) Restriction The COMBINE option is not supported in a DMP solution.
        """
        command = f"CYCOPT,{option},{value1},{value2},{value3},{value4},{value5},{value6},{value7}"
        return self.run(command, **kwargs)

    def emsym(self, nsect: str = "", **kwargs):
        r"""Specifies circular symmetry for electromagnetic sources.

        Mechanical APDL Command: `EMSYM <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_EMSYM.html>`_

        Parameters
        ----------
        nsect : str
            The number of circular symmetry sections (defaults to 1).

        Notes
        -----

        .. _EMSYM_notes:

        Specifies the number of times to repeat electromagnetic sources for circular symmetry. Applies to
        ``SOURC36`` elements and to coupled-field elements with electric current conduction results in the
        database. Sources are assumed to be equally spaced over 360° about the global Cartesian Z axis.

        This command is also valid in SOLUTION.
        """
        command = f"EMSYM,{nsect}"
        return self.run(command, **kwargs)

    def msopt(
        self,
        option: str = "",
        sname: str = "",
        value1: str = "",
        value2: str = "",
        value3: str = "",
        value4: str = "",
        value5: str = "",
        value6: str = "",
        value7: str = "",
        **kwargs,
    ):
        r"""Specifies solution options for a `multistage cyclic symmetry analysis
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mstag/ans_mstag_introTheory.html>`_.

        Mechanical APDL Command: `MSOPT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MSOPT.html>`_

        Parameters
        ----------
        option : str
            Multistage cyclic symmetry analysis option. There is no default. You must choose one of the
            following options:

            * ``CSYS`` - Activates a previously defined cyclic coordinate system by the reference number specified in
              ``Value1``. ``Sname`` is ignored. This option is only valid in the /PREP7 processor.

              * ``Value1`` - Cylindrical coordinate system reference number. You must have already created the
                coordinate system by issuing prior commands like :ref:`cs` or :ref:`local` to define it. Defaults to
                1 where the global Cartesian Z axis is the cyclic symmetry axis.

              You must define the coordinate system before defining the stages.

            * ``NEW`` - Creates a new stage with the name entered in ``Sname`` and the ``Value1`` - ``Value6``
              specifications listed in the table below. This option is only valid in the /PREP7 processor.

              * ``Sname`` - An alphanumeric name used to identify the stage. ``Sname`` may be up to 32 characters,
                beginning with a letter and containing only letters, numbers, and underscores. Names beginning with
                an underscore (for example, _LOOP) are reserved for use by Mechanical APDL and should be avoided. The
                component name ALL is not permitted.

              This command contains some tables and extra information which can be inspected in the original
              documentation pointed above.

              When creating a new stage, the base and duplicate sector meshes should be coincident. The offset
              between the number of base and duplicate coincident nodes is constant throughout the whole model.
              The same is true for the element numbers.

            * ``DELETE`` - Deletes the stage identified by ``Sname``.

              * ``Sname`` - The name of the stage to be deleted. Entities such as nodes and elements contained in
                the stage are unaffected. Only the grouping and the related constraint equations are concerned.

            * ``EXPAND`` - Specifies stages (identified by ``Sname`` ) and sectors (sector number specified in ``Value1`` ) for
              subsequent expansion. This option is only valid in the /POST1 processor.

              * ``Sname`` - The name of the stage to be expanded. A value of 0 resets all expansion settings. A
                value of ALL means all existing stages will be expanded (default).

              * ``Value1`` - The sector number. A value of 0 resets all sector settings. A value of ALL means all
                sectors will be expanded (default).

            * ``LIST`` - Lists the stage identified by ``Sname`` with the level of detail specified in ``Value1``.

              * ``Sname`` - The name of the stage to be listed. If blank, list all stages (default).

              * ``Value1`` - Key for specifying the level of detail.

                * ``0 (, or OFF)`` - Basic listing (default).

                * ``1 (, or ON)`` - Detailed listing, including constraint equations information. Note that the
                  interstage constraint equations number information is only listed for the stage with the smallest
                  number of sectors.

            * ``MODIFY`` - Sets the `harmonic index
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cycsym/advcycmodalans.html#harmindex>`_
              of a stage identified by ``Sname`` to the integer specified in ``Value1``.

              * ``Sname`` - The name of the stage to be modified.

              * ``Value1`` - The new `harmonic index
                <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cycsym/advcycmodalans.html#harmindex>`_.
                Existing cyclic and multistage interface constraint equations will be deleted.

            * ``RESET`` - Deletes all stages and resets all multistage analysis settings.

        sname : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MSOPT.html>`_ for further
            information.

        value1 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MSOPT.html>`_ for further
            information.

        value2 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MSOPT.html>`_ for further
            information.

        value3 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MSOPT.html>`_ for further
            information.

        value4 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MSOPT.html>`_ for further
            information.

        value5 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MSOPT.html>`_ for further
            information.

        value6 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MSOPT.html>`_ for further
            information.

        value7 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MSOPT.html>`_ for further
            information.

        Notes
        -----

        .. _MSOPT_notes:

        The :ref:`msopt` command is used to specify solution options for a `multistage cyclic symmetry
        analysis
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mstag/ans_mstag_introTheory.html>`_. It
        is not part of the :ref:`cyclic` procedure for a cyclic symmetry analysis.

        When you issue :ref:`msopt`,EXPAND, subsequent :ref:`set` commands read the data set from the
        specified :file:`.rst` file and expand the nodes and elements to the stages and sectors specified
        via :ref:`msopt`,EXPAND.

        **Example Usage**
        `Example: Static Analysis of a Compressor Model with 4 Axial Stages Without a Duplicate Sector
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mstag/multistage_ex_compressor.html#>`_

        `Example: Linear Perturbation Modal Analysis of a Simplified Model with 2 Axial Stages and a Non-
        planar Interstage Boundary
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mstag/multistag_ex_linearPert.html#>`_

        `Example: Modal Analysis of Turbomachinery Stage Modeled as 2 Radial Stages with Offset Cyclic Edge
        Starting Points
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mstag/multistag_ex_modal_turboOffset.html#>`_

        `Example: Mutistage Multiharmonic Modal Analysis of a Hollow Cylinder Modeled Using 2 Stages
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mstag/mstag_hollowCyl2stages.html#>`_

        `Example: Multiharmonic Linear Perturbation Modal Analysis of a Simplified Model with 3 Axial Stages
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mstag/ans_mstagExMultiHarmLP.html#>`_
        """
        command = f"MSOPT,{option},{sname},{value1},{value2},{value3},{value4},{value5},{value6},{value7}"
        return self.run(command, **kwargs)

    def mstole(
        self, method: int | str = "", namesurf: str = "", namefluid: str = "", **kwargs
    ):
        r"""Adds two extra nodes from ``FLUID116`` elements to ``SURF151`` or ``SURF152`` elements for
        convection analyses.

        Mechanical APDL Command: `MSTOLE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MSTOLE.html>`_

        Parameters
        ----------
        method : int or str
            Mapping method:

            * ``0`` - Hybrid method (default).

            * ``1`` - Projection method.

            * ``2`` - Minimum centroid distance method.

        namesurf : str
            Component name for a group of ``SURF151`` or ``SURF152`` elements. The component name must be 32
            characters or less, and it must be enclosed in single quotes (for example, 'COM152') when the
            :ref:`mstole` command is manually typed in.

        namefluid : str
            Component name for a group of ``FLUID116`` elements. The component name must be 32 characters or
            less, and it must be enclosed in single quotes (for example, 'COM116') when the :ref:`mstole`
            command is manually typed in.

        Notes
        -----

        .. _MSTOLE_notes:

        For convection analyses, the :ref:`mstole` command adds two extra nodes from ``FLUID116`` elements
        to ``SURF151`` or ``SURF152`` elements by employing the specified mapping method. In the hybrid
        method, the projection method is tried first and if it fails the centroid distance method is used.
        The ``SURF151`` or ``SURF152`` elements and the ``FLUID116`` elements must be grouped into
        components and named using the :ref:`cm` command.

        The ``SURF151`` or ``SURF152`` extra node option must be set for two extra nodes (KEYOPT(5) = 2).

        For more information, see `Using the Surface Effect Elements
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_the/Hlp_G_THE2_5.html#>`_ in the
        `Thermal Analysis Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_the/Hlp_G_THE4.html>`_.
        """
        command = f"MSTOLE,{method},{namesurf},{namefluid}"
        return self.run(command, **kwargs)

    def perbc2d(
        self,
        loc1: str = "",
        loc2: str = "",
        loctol: str = "",
        r1: str = "",
        r2: str = "",
        tolr: str = "",
        opt: int | str = "",
        plnopt: int | str = "",
        **kwargs,
    ):
        r"""Generates periodic constraints for 2D planar magnetic field analyses.

        Mechanical APDL Command: `PERBC2D <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PERBC2D.html>`_

        Parameters
        ----------
        loc1 : str
            Constant coordinate location of the first plane of nodes. For ``PLNOPT`` = 1 or 2, the constant
            coordinate location is the global Cartesian coordinate system ( :ref:`csys`,0) location in the X
            or Y direction respectively. For ``PLNOPT`` = 0, the location is the angle in the global
            cylindrical coordinate system ( :ref:`csys`,1).

        loc2 : str
            Constant coordinate location of the second plane of nodes. For ``PLNOPT`` = 1 or 2, the constant
            coordinate location is the global Cartesian coordinate system ( :ref:`csys`,0) location in the X
            or Y direction respectively. For ``PLNOPT`` = 0, the location is the angle (in degrees) in the
            global cylindrical coordinate system ( :ref:`csys`,1).

        loctol : str
            Tolerance on the constant coordinate location for node selection. Defaults to.00001 for
            ``PLNOPT`` = 1 or 2 and.001 degrees for ``PLNOPT`` = 0.

        r1 : str
            Minimum coordinate location along the second plane of nodes. For ``PLNOPT`` = 1 or 2, the
            coordinate location is the global Cartesian coordinate system location in the Y or X direction
            respectively. For ``PLNOPT`` = 0, the coordinate location is the radial coordinate value in the
            global cylindrical coordinate system. Periodic conditions are not applied to nodes at this
            location.

        r2 : str
            Maximum coordinate location along the second plane of nodes. For ``PLNOPT`` = 1 or 2, the
            coordinate location is the global Cartesian coordinate system location in the Y or X direction
            respectively. For ``PLNOPT`` = 0, the coordinate location is the radial coordinate value in the
            global cylindrical coordinate system. Periodic conditions are not applied to nodes at this
            location.

        tolr : str
            Tolerance dimension on node selection along the plane of nodes. Defaults to.00001.

        opt : int or str
            Periodic option:

            * ``0`` - Odd symmetry (default). Apply constraint equations such that AZ(i) = -AZ(j).

            * ``1`` - Even symmetry. Apply node coupling such that AZ(i) = AZ(j).

        plnopt : int or str
            Symmetry plane option:

            * ``0`` - Planes of constant angle in the global cylindrical coordinate system ( :ref:`csys`,1).

            * ``1`` - Planes parallel to the global Cartesian X axis ( :ref:`csys`,0).

            * ``2`` - Planes parallel to the global Cartesian Y axis ( :ref:`csys`,0).

        Notes
        -----

        .. _PERBC2D_notes:

        :ref:`perbc2d` invokes a Mechanical APDL macro which generates periodic boundary condition
        constraints for
        2D planar magnetic field analysis.

        The macro is restricted to node pairs sharing common coordinate values along symmetry planes
        separated by a constant coordinate value. Planes (or lines) must lie at either constant angles (
        ``PLNOPT`` = 0), constant X values ( ``PLNOPT`` = 1), or constant Y values ( ``PLNOPT`` = 2).

        The macro applies constraint equations ( ``OPT`` = 0, odd symmetry) or node coupling ( ``OPT`` = 1,
        even symmetry) to each node pair sharing a common coordinate value along the symmetry planes. By
        default, periodic conditions are not applied at the first and last node pairs on the symmetry planes
        unless the input location values, R1 and R2, are adjusted to be less than or greater than the actual
        node coordinate values.

        Nodes are selected for application of constraints via :ref:`nsel`, with tolerances on the constant
        coordinate location ( ``LOCTOL`` ) and the coordinate location along the plane (RTOL).
        """
        command = f"PERBC2D,{loc1},{loc2},{loctol},{r1},{r2},{tolr},{opt},{plnopt}"
        return self.run(command, **kwargs)

    def race(
        self,
        xc: str = "",
        yc: str = "",
        rad: str = "",
        tcur: str = "",
        dy: str = "",
        dz: str = "",
        cname: str = "",
        **kwargs,
    ):
        r"""Defines a "racetrack" current source.

        Mechanical APDL Command: `RACE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_RACE.html>`_

        Parameters
        ----------
        xc : str
            Location of the mid-thickness of the vertical leg along the working plane X-axis.

        yc : str
            Location of the mid-thickness of the horizontal leg along the working plane Y-axis.

        rad : str
            Radius of curvature of the mid-thickness of the curves in the racetrack source. Defaults to.501 * DY

        tcur : str
            Total current, amp-turns (MKS), flowing in the source.

        dy : str
            In-plane thickness of the racetrack source.

        dz : str
            Out-of-plane thickness (depth) of the racetrack source.

        cname : str

        Notes
        -----

        .. _RACE_notes:

        :ref:`race` invokes a Mechanical APDL macro which defines a racetrack current source in the working
        plane
        coordinate system.

        .. figure:: ../../../images/_commands/gRACE1.svg

        The current source is generated from bar and arc source primitives using ``SOURC36`` (which is
        assigned the next available element type number).

        The macro is valid for use in 3D magnetic field analysis using a scalar potential formulation.

        Current flows in a counterclockwise direction with respect to the working plane.
        """
        command = f"RACE,{xc},{yc},{rad},{tcur},{dy},{dz},,,{cname}"
        return self.run(command, **kwargs)

    def sstate(
        self,
        action: str = "",
        cm_name: str = "",
        val1: str = "",
        val2: str = "",
        val3: str = "",
        val4: str = "",
        val5: str = "",
        val6: str = "",
        val7: str = "",
        val8: str = "",
        val9: str = "",
        **kwargs,
    ):
        r"""Defines a steady-state rolling analysis.

        Mechanical APDL Command: `SSTATE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SSTATE.html>`_

        Parameters
        ----------
        action : str
            Action to perform for defining or manipulating steady-state rolling analysis data:

            * ``DEFINE`` - Define steady-state rolling analysis data

            * ``LIST`` - List current steady-state rolling analysis data

            * ``DELETE`` - Delete steady-state rolling analysis data

        cm_name : str
            Element component name

        val1 : str
            Input values (based on the ``Action`` type)

        val2 : str
            Input values (based on the ``Action`` type)

        val3 : str
            Input values (based on the ``Action`` type)

        val4 : str
            Input values (based on the ``Action`` type)

        val5 : str
            Input values (based on the ``Action`` type)

        val6 : str
            Input values (based on the ``Action`` type)

        val7 : str
            Input values (based on the ``Action`` type)

        val8 : str
            Input values (based on the ``Action`` type)

        val9 : str
            Input values (based on the ``Action`` type)

        Notes
        -----

        .. _SSTATE_notes:

        The :ref:`sstate` command specifies steady-state rolling analysis parameters for the given element
        component. The program runs the steady-state rolling analysis if the corresponding element key
        option is enabled for that element component.

        The command supports the following elements:

        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.

        For information about steady-state rolling for rebar and solid elements, see `Steady-State Rolling
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_geosteadystroll.html#>`_

        .. _sstate_define_spec:

        The following data types can be defined:

        * SPIN -- Spinning motion

        * TRANSLATE -- Rigid body motion (velocity) that the spinning component is undergoing

        **Define the steady-state spinning motion:**

        :ref:`sstate`, DEFINE, ``CM_Name``, SPIN, ``OMEGA``, ``Method``, ``Val4``, ``Val5``, ``Val6``,
        ``Val7``, ``Val8``, ``Val9``

        * ``OMEGA`` - Spin velocity

        * ``Method`` - Method to use for defining the spin axis:

          * ``POINTS`` - Define the spin axis using two points:

            ``Val4``, ``Val5``, ``Val6`` -- Coordinates of the first point

            ``Val7``, ``Val8``, ``Val9`` -- Coordinates of the second point

            This definition method is currently the only option.

              **Example: Defining Steady-State Spinning Motion**

              This command defines a steady-state spinning motion of 120 rad/s around the spin axis:

              .. code:: apdl

                 SSTATE,DEFINE, CM_Name,SPIN,120,POINTS,0,0,0,0,1,0

              In this case, two points with coordinates (0,0,0) and (0,1,0) define the spin axis in the global Y
              direction.

        **Define the rigid body motion (velocity):**

        :ref:`sstate`, DEFINE, ``CM_Name``, TRANSLATE, ``Val2``, ``Val3``, ``Val4``

        * ``Val2``, ``Val3``, ``Val4`` -- Rigid body velocity components

        .. _sstate_list_spec:

        :ref:`sstate`, LIST, ``CM_Name``

        Lists all steady-state rolling analysis data defined on the specified element component. All data is
        listed if no component ( ``CM_Name`` ) is specified.

        .. _sstate_delete_spec:

        :ref:`sstate`, DELETE, ``CM_Name``

        Deletes all steady-state rolling analysis data defined on the specified element component. All data
        is deleted if no component ( ``CM_Name`` ) is specified.
        """
        command = f"SSTATE,{action},{cm_name},{val1},{val2},{val3},{val4},{val5},{val6},{val7},{val8},{val9}"
        return self.run(command, **kwargs)

    def xfcrkmesh(
        self, enrichmentid: str = "", elemcomp: str = "", nodecomp: str = "", **kwargs
    ):
        r"""Defines a crack in the model when the crack surface is discretized by ``MESH200`` elements

        Mechanical APDL Command: `XFCRKMESH <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_XFCRKMESH.html>`_

        Parameters
        ----------
        enrichmentid : str
            Name of the enrichment specified via the associated :ref:`xfenrich` command.

        elemcomp : str
            Name of the element component consisting of ``MESH200`` elements that form the crack surface.

        nodecomp : str
            Name of the node component consisting of the crack front nodes of the crack surface.

        Notes
        -----

        .. _XFCRKMESH_notes:

        Used in an `XFEM-based crack analysis
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/Hlp_G_FRACXFEM.html#fracxfemreferences>`_,
        this command defines a crack in the model when the crack surface is discretized by ``MESH200``
        elements. For more informatiom, see `MESH200 Element Method
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/Hlp_G_FRACXFEM.html#>`_

        Issue the :ref:`xfcrkmesh` command multiple times as needed to define multiple crack surfaces in the
        model.

        This command is valid in PREP7 ( :ref:`prep7` ) only.
        """
        command = f"XFCRKMESH,{enrichmentid},{elemcomp},{nodecomp}"
        return self.run(command, **kwargs)

    def xfdata(
        self,
        enrichmentid: str = "",
        lsm: str = "",
        elemnum: str = "",
        nodenum: str = "",
        phi: str = "",
        psi: str = "",
        **kwargs,
    ):
        r"""Defines a crack in the model by specifying nodal level set values

        Mechanical APDL Command: `XFDATA <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_XFDATA.html>`_

        Parameters
        ----------
        enrichmentid : str
            Name of the enrichment specified via the associated :ref:`xfenrich` command.

        lsm : str
            Indicates that level set values are being specified (default).

        elemnum : str
            Element number.

        nodenum : str
            Node number associated with the specified element ``ELNUM``.

        phi : str
            Signed normal distance of the node from the crack.

        psi : str
            Signed normal distance of the node from the crack tip (or crack front). Used only in the
            `singularity-based
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/Hlp_G_FRACXFEM.html#fracxfemfig1>`_
            XFEM method.

        Notes
        -----

        .. _XFDATA_notes:

        Issue the :ref:`xfdata` command multiple times as needed to specify nodal level set values for all
        nodes of an element.

        This command is valid in PREP7 ( :ref:`prep7` ) only.
        """
        command = f"XFDATA,{enrichmentid},{lsm},{elemnum},{nodenum},{phi},{psi}"
        return self.run(command, **kwargs)

    def xfenrich(
        self,
        enrichmentid: str = "",
        compname: str = "",
        mat_id: str = "",
        method: str = "",
        radius: str = "",
        snaptoler: str = "",
        **kwargs,
    ):
        r"""Defines parameters associated with crack propagation using XFEM

        Mechanical APDL Command: `XFENRICH <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_XFENRICH.html>`_

        Parameters
        ----------
        enrichmentid : str
            An alphanumeric name assigned to identify the enrichment. The name can contain up to 32
            characters and must begin with an alphabetic character. Alphabetic characters, numbers, and
            underscores are valid.

        compname : str
            Name of the element set component for which initial cracks are defined and possibly propagated.

        mat_id : str
            Material ID number referring to cohesive zone material behavior on the initial crack. If 0 or
            not specified, the initial crack is assumed to be free of cohesive zone behavior. Used only with
            the phantom-node XFEM method ( ``Method`` ).

        method : str
            PHAN -- Use `phantom-node-based
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/Hlp_G_FRACXFEM.html#fracxfemfig2>`_
            XFEM (default).

            SING -- Use `singularity-based
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/Hlp_G_FRACXFEM.html#fracxfemfig1>`_
            XFEM.

        radius : str
            Radius defining the region around the crack tip encompassing the set of elements to be
            influenced by the crack-tip singularity effects. Default = 0.0. Used only in singularity-based
            XFEM.

        snaptoler : str
            Snap tolerance to snap the crack tip to the closest crack face along the extension direction.
            Default = 1.0E-6. Used only in singularity-based XFEM.

        Notes
        -----

        .. _XFENRICH_notes:

        If ``MAT_ID`` is specified, the cohesive zone behavior is described by the `bilinear cohesive law
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/cozonemats.html#eq882acced-35ea-449a-9f59-1a8f1175f44c>`_.

        If issuing multiple :ref:`xfenrich` commands, the element components ( ``CompName`` ) should not
        intersect (that is, the element components should not have any common elements between them).

        When multiple :ref:`xfenrich` commands are issued in an analysis, combining the phantom-node-based
        method ( ``Method`` = PHAN) and the singularity-based method ( ``Method`` = SING) is not valid. Only
        one XFEM method per analysis is allowed.

        This command is valid in PREP7 ( :ref:`prep7` ) only.
        """
        command = (
            f"XFENRICH,{enrichmentid},{compname},{mat_id},{method},{radius},{snaptoler}"
        )
        return self.run(command, **kwargs)

    def xflist(self, enrichmentid: str = "", **kwargs):
        r"""Lists enrichment details and associated crack information

        Mechanical APDL Command: `XFLIST <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_XFLIST.html>`_

        Parameters
        ----------
        enrichmentid : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_XFLIST.html>`_ for
            further information.

        Notes
        -----

        .. _XFLIST_notes:

        This command is valid in PREP7 ( :ref:`prep7` ) and SOLUTION ( :ref:`slashsolu` ).
        """
        command = f"XFLIST,{enrichmentid}"
        return self.run(command, **kwargs)
