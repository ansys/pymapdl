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

class Materials:

    def emunit(self, lab: str = "", value: str = "", **kwargs):
        r"""Specifies the system of units for magnetic field problems.

        Mechanical APDL Command: `EMUNIT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_EMUNIT.html>`_

        **Command default:**

        .. _EMUNIT_default:

        Rationalized MKS system of units (meters, amperes, henries, webers, etc.). Free-space permeability
        is set to 4 πe-7 Henries/meter, free-space permittivity is set to 8.85e-12 Farads/meter.

        Parameters
        ----------
        lab : str
            Label specifying the type of units:

            * ``MKS`` - Rationalized MKS system of units (meters, amperes, henries, webers, etc.). Free-space
              permeability is set to 4 πe-7 henries/meter. Free-space permittivity is set to 8.85 e-12 F/m.

            * ``MUZRO`` - User defined system of units. Free-space permeability is set to the value input for
              ``VALUE``. Other units must correspond to the permeability units. Relative permeability may be
              altered to absolute values.

            * ``EPZRO`` - User defined system of units. Free-space permittivity is set to the value input for
              VALUE. Other units must correspond to the permittivity units.

        value : str
            User value of free-space permeability (defaults to 1) if ``Lab`` = MUZRO, or free-space
            permittivity (defaults to 1) if ``Lab`` = EPZRO.

        Notes
        -----

        .. _EMUNIT_notes:

        Specifies the system of units to be used for electric and magnetic field problems. The free-space
        permeability and permittivity values may be set as desired. These values are used with the relative
        property values ( :ref:`mp` ) to establish absolute property values. If the magnetic source field
        strength (H:sub:`s` ) has already been calculated ( :ref:`biot` ), switching :ref:`emunit` will not
        change the values.

        For micro-electromechanical systems (MEMS), where dimensions are on the order of microns, see the
        conversion factors in `System of Units
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cou/Hlp_G_COU1_3.html#couthermelesmksvfa>`_
        in the `Coupled-Field Analysis Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cou/Hlp_G_COU_N4.html>`_.

        This command is also valid in SOLUTION.
        """
        command = f"EMUNIT,{lab},{value}"
        return self.run(command, **kwargs)



    def fc(self, mat: str = "", lab1: str = "", lab2: str = "", data1: str = "", data2: str = "", data3: str = "", data4: str = "", data5: str = "", data6: str = "", **kwargs):
        r"""Provides failure criteria information and activates a data table to input temperature-dependent
        stress and strain limits.

        Mechanical APDL Command: `FC <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_FC.html>`_

        Parameters
        ----------
        mat : str
            Material reference number. You can define failure criteria for up to 250 different materials.

        lab1 : str
            Type of data.

            * ``TEMP`` - Temperatures. Each of the materials you define can have a different set of temperatures
              to define the failure criteria.

            * ``EPEL`` - Strains.

            * ``S`` - Stresses.

        lab2 : str
            Specific criteria. Not used if ``Lab1`` = TEMP.

            * ``XTEN`` - Allowable tensile stress or strain in the x-direction. (Must be positive.)

            * ``XCMP`` - Allowable compressive stress or strain in the x-direction. (Defaults to negative of
              XTEN.)

            * ``YTEN`` - Allowable tensile stress or strain in the y-direction. (Must be positive.)

            * ``YCMP`` - Allowable compressive stress or strain in the y-direction. (Defaults to negative of
              YTEN.)

            * ``ZTEN`` - Allowable tensile stress or strain in the z-direction. (Must be positive.)

            * ``ZCMP`` - Allowable compressive stress or strain in the z-direction. (Defaults to negative of
              ZTEN.)

            * ``XY`` - Allowable XY stress or shear strain. (Must be positive.)

            * ``YZ`` - Allowable YZ stress or shear strain. (Must be positive.)

            * ``XZ`` - Allowable XZ stress or shear strain. (Must be positive.)

            * ``XYCP`` - XY coupling coefficient (Used only if ``Lab1`` = S). Defaults to -1.0. [
              :ref:`FC_arg_note` ]

            * ``YZCP`` - YZ coupling coefficient (Used only if ``Lab1`` = S). Defaults to -1.0. [
              :ref:`FC_arg_note` ]

            * ``XZCP`` - XZ coupling coefficient (Used only if ``Lab1`` = S). Defaults to -1.0. [
              :ref:`FC_arg_note` ]

            * ``XZIT`` - XZ tensile inclination parameter for Puck failure index (default = 0.0)

            * ``XZIC`` - XZ compressive inclination parameter for Puck failure index (default = 0.0)

            * ``YZIT`` - YZ tensile inclination parameter for Puck failure index (default = 0.0)

            * ``YZIC`` - YZ compressive inclination parameter for Puck failure index (default = 0.0)

            * ``G1G2`` - Fracture toughness ratio between GI (mode I) and GII (mode II)

            * ``ETAL`` - Longitudinal friction coefficient

            * ``ETAT`` - Transverse friction coefficient

            * ``APL0`` - Fracture angle under pure transverse compression (default to 53) [ :ref:`FC_arg_note2`
              ]

            .. _FC_arg_note:

            Entering a blank or a zero for XYCP, YZCP, or XZCP triggers the default value of -1.0. To specify an
            effective zero, use a small, nonzero value (such as 1E-14) instead. For more information, see
            :ref:`aPG6vq1bamcm`.

            .. _FC_arg_note2:

            Entering a blank or a zero ALP0 triggers the default value of 53. To specify an effective zero, use
            a small, nonzero value (such as 1E-14) instead. For more information, see :ref:`aPG6vq1bamcm`.

        data1 : str
            Description of ``DATA1`` through ``DATA6``.

            * ``T1, T2, T3, T4, T5, T6`` - Temperature at which limit data is input. Used only when ``Lab1`` =
              TEMP.

            * ``V1, V2, V3, V4, V5, V6`` - Value of limit stress or strain at temperature T1 through T6. Used
              only when ``Lab1`` = S or EPEL.

        data2 : str
            Description of ``DATA1`` through ``DATA6``.

            * ``T1, T2, T3, T4, T5, T6`` - Temperature at which limit data is input. Used only when ``Lab1`` =
              TEMP.

            * ``V1, V2, V3, V4, V5, V6`` - Value of limit stress or strain at temperature T1 through T6. Used
              only when ``Lab1`` = S or EPEL.

        data3 : str
            Description of ``DATA1`` through ``DATA6``.

            * ``T1, T2, T3, T4, T5, T6`` - Temperature at which limit data is input. Used only when ``Lab1`` =
              TEMP.

            * ``V1, V2, V3, V4, V5, V6`` - Value of limit stress or strain at temperature T1 through T6. Used
              only when ``Lab1`` = S or EPEL.

        data4 : str
            Description of ``DATA1`` through ``DATA6``.

            * ``T1, T2, T3, T4, T5, T6`` - Temperature at which limit data is input. Used only when ``Lab1`` =
              TEMP.

            * ``V1, V2, V3, V4, V5, V6`` - Value of limit stress or strain at temperature T1 through T6. Used
              only when ``Lab1`` = S or EPEL.

        data5 : str
            Description of ``DATA1`` through ``DATA6``.

            * ``T1, T2, T3, T4, T5, T6`` - Temperature at which limit data is input. Used only when ``Lab1`` =
              TEMP.

            * ``V1, V2, V3, V4, V5, V6`` - Value of limit stress or strain at temperature T1 through T6. Used
              only when ``Lab1`` = S or EPEL.

        data6 : str
            Description of ``DATA1`` through ``DATA6``.

            * ``T1, T2, T3, T4, T5, T6`` - Temperature at which limit data is input. Used only when ``Lab1`` =
              TEMP.

            * ``V1, V2, V3, V4, V5, V6`` - Value of limit stress or strain at temperature T1 through T6. Used
              only when ``Lab1`` = S or EPEL.

        Notes
        -----

        .. _FC_notes:

        The data table can be input in either PREP7 or POST1. This table is used only in POST1. When you
        postprocess failure criteria results defined via the :ref:`fc` command ( :ref:`plesol`,
        :ref:`presol`, :ref:`plnsol`, :ref:`prnsol`, :ref:`prrsol`, etc.), the active coordinate system must
        be the coordinate system of the material being analyzed. You do this using :ref:`rsys`, SOLU. For
        layered applications, you also use the :ref:`layer` command. See the specific element documentation
        in the `Element Reference
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_BIBLIO.html>`_ for
        information about defining your coordinate system for layers.

        Some plotting and printing functions will not support Failure Criteria for your PowerGraphics
        displays. This could result in minor changes to other data when Failure Criteria are applied. See
        the appropriate plot or print command documentation for more information.
        """
        command = f"FC,{mat},{lab1},{lab2},{data1},{data2},{data3},{data4},{data5},{data6}"
        return self.run(command, **kwargs)



    def fccheck(self, **kwargs):
        r"""Checks both the strain and stress input criteria for all materials.

        Mechanical APDL Command: `FCCHECK <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_FCCHECK.html>`_

        Notes
        -----

        .. _FCCHECK_notes:

        Issue the :ref:`fccheck` command to check the completeness of the input during the input phase.
        """
        command = "FCCHECK"
        return self.run(command, **kwargs)



    def fcdele(self, mat: str = "", **kwargs):
        r"""Deletes previously defined failure criterion data for the given material.

        Mechanical APDL Command: `FCDELE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_FCDELE.html>`_

        Parameters
        ----------
        mat : str
            Material number. Deletes all :ref:`fc` command input for this material.

            A value of ALL deletes all :ref:`fc` command input for all materials.

        Notes
        -----

        .. _FCDELE_notes:

        This command is also valid in POST1.
        """
        command = f"FCDELE,{mat}"
        return self.run(command, **kwargs)



    def fclist(self, mat: str = "", temp: str = "", **kwargs):
        r"""To list what the failure criteria is that you have input.

        Mechanical APDL Command: `FCLIST <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_FCLIST.html>`_

        Parameters
        ----------
        mat : str
            Material number (defaults to ALL for all materials).

        temp : str
            Temperature to be evaluated at (defaults to TUNIF).

        Notes
        -----

        .. _FCLIST_notes:

        This command allows you to see what you have already input for failure criteria using the FC
        commands.
        """
        command = f"FCLIST,{mat},,{temp}"
        return self.run(command, **kwargs)



    def mp(self, lab: str = "", mat: str = "", c0: str = "", c1: str = "", c2: str = "", c3: str = "", c4: str = "", **kwargs):
        r"""Defines a linear material property as a constant or a function of temperature.

        Mechanical APDL Command: `MP <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MP.html>`_

        Parameters
        ----------
        lab : str
            Valid material property label. Applicable labels are listed under "Material Properties" in the input
            table for each element type in the `Element Reference <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_BIBLIO.html>`_.

            * ``ALPD`` - Mass matrix multiplier for damping.

            * ``ALPX`` - Secant coefficients of thermal expansion (also ALPY, ALPZ).

            * ``BETD`` - Stiffness matrix multiplier for damping.

            * ``BETX`` - Coefficient of diffusion expansion (also BETY, BETZ)

            * ``BVIS`` - Bulk viscosity

            * ``C`` - Specific heat

            * ``CREF`` - Reference concentration (may not be temperature dependent)

            * ``CSAT`` - Saturated concentration

            * ``CTEX`` - Instantaneous coefficients of thermal expansion (also CTEY, CTEZ)

            * ``CVH`` - Heat coefficient at constant volume per unit of mass

            * ``DENS`` - Mass density.

            * ``DMPR`` - Damping ratio.

            * ``DMPS`` - Constant structural damping coefficient.

            * ``DXX`` - Diffusivity coefficients (also DYY, DZZ)

            * ``EMIS`` - Emissivity. For default behavior, see :ref:`Notes. <MP_EMIS_notes>`

            * ``ENTH`` - Enthalpy. See :ref:`Considerations for Enthalpy. <MP_enthalpy_notes>`

            * ``EX`` - Elastic moduli (also EY, EZ)

            * ``GXY`` - Shear moduli (also GYZ, GXZ)

            * ``HF`` - Convection or film coefficient

            * ``KXX`` - Thermal conductivities (also KYY, KZZ)

            * ``LSST`` - Electric loss tangent

            * ``LSSM`` - Magnetic loss tangent

            * ``MGXX`` - Magnetic coercive forces (also MGYY, MGZZ)

            * ``MURX`` - Magnetic relative permeabilities (also MURY, MURZ)

            * ``MU`` - Coefficient of friction

            * ``NUXY`` - Minor Poisson's ratios (also NUYZ, NUXZ) (NUXY = ν:sub:`yx`, as described in
              `Stress-Strain Relationships
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_str1.html#eq84e81ad6-8b11-4580-8034-9e5f20df8c23>`_

            * ``PERX`` - Electric relative permittivities (also PERY, PERZ)

              If you enter permittivity values less than 1 for ``SOLID5``, ``PLANE13``, or ``SOLID98``, the
              program interprets the values as absolute permittivity. Values input for ``PLANE222``, ``PLANE223``,
              ``SOLID225``, ``SOLID226``, or ``SOLID227`` are always interpreted as relative permittivity.

            * ``PRXY`` - Major Poisson's ratios (also PRYZ, PRXZ) (PRXY = ν:sub:`xy`, as described in
              `Stress-Strain Relationships
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_str1.html#eq84e81ad6-8b11-4580-8034-9e5f20df8c23>`_

            * ``QRATE`` - Heat generation rate for thermal mass element ``MASS71``. Fraction of plastic work
              converted to heat (Taylor-Quinney coefficient) or fraction of viscoelastic loss converted to heat
              for coupled- field elements ``PLANE222``, ``PLANE223``, ``SOLID225``, ``SOLID226``, and
              ``SOLID227``.

            * ``REFT`` - Reference temperature. Must be defined as a constant; C1 through C4 are ignored.

            * ``RH`` - Hall Coefficient.

            * ``RSVX`` - Electrical resistivities (also RSVY, RSVZ).

            * ``SBKX`` - Seebeck coefficients (also SBKY, SBKZ).

            * ``SONC`` - Sonic velocity.

            * ``THSX`` - Thermal strain (also THSY, THSZ).

            * ``VISC`` - Viscosity.

        mat : str
            Material reference number to be associated with the elements (defaults to the current MAT
            setting ( :ref:`mat` )).

        c0 : str
            Material property value, or if a property-versus-temperature polynomial is being defined, the
            constant term in the polynomial. ``C0`` can also be a table name (``tabname``); if ``C0`` is a
            table name, ``C1`` through ``C4`` are ignored.

        c1 : str
            Coefficients of the linear, quadratic, cubic, and quartic terms, respectively, in the property-
            versus-temperature polynomial. Leave blank (or set to zero) for a constant material property.

        c2 : str
            Coefficients of the linear, quadratic, cubic, and quartic terms, respectively, in the property-
            versus-temperature polynomial. Leave blank (or set to zero) for a constant material property.

        c3 : str
            Coefficients of the linear, quadratic, cubic, and quartic terms, respectively, in the property-
            versus-temperature polynomial. Leave blank (or set to zero) for a constant material property.

        c4 : str
            Coefficients of the linear, quadratic, cubic, and quartic terms, respectively, in the property-
            versus-temperature polynomial. Leave blank (or set to zero) for a constant material property.

        Notes
        -----

        .. _MP_notes:

        :ref:`mp` defines a linear material property as a constant or in terms of a fourth order polynomial
        as a function of temperature. (See the :ref:`tb` command for nonlinear material property input.)
        Linear material properties typically require a single substep for solution, whereas nonlinear
        material properties require multiple substeps.

        If the constants C1 - C4 are input, the polynomial

        Property = ``C0`` + ``C1`` (T) + ``C2`` (T) :sup:`2` + ``C3`` (T) :sup:`3` + ``C4`` (T) :sup:`4`

        is evaluated at discrete temperature points with linear interpolation between points (that is, a
        piecewise linear representation) and a constant-valued extrapolation beyond the extreme points.
        First-order properties use two discrete points (±9999°). The :ref:`mptemp` or :ref:`mptgen` commands
        must be used for second and higher order properties to define appropriate temperature steps. To
        ensure that the number of temperatures defined via the :ref:`mptemp` and :ref:`mptgen` commands is
        minimally sufficient for a reasonable representation of the curve, Mechanical APDL generates an
        error
        message if the number is less than N, and a warning message if the number is less than 2N. The value
        N represents the highest coefficient used; for example, if C3 is nonzero and C4 is zero, a cubic
        curve is being used which is defined using 4 coefficients so that N = 4.

        Some elements (for example, ``FLUID116`` ) support tabular input for material properties. Use the
        :ref:`dim` command to create the table of property values as a function of the independent
        variables. Then input this table name ( ``C0`` = ``tabname``) when defining the property via the
        :ref:`mp` command. Tabular material properties are calculated before the first iteration (that is,
        using initial values ( :ref:`ic` )). For a list of elements that support tabular material properties
        and associated primary variables, see `Defining Linear Material Properties Using Tabular Input
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/ansmatdeflin.html#fntbdatareqd>`_

        When defining a reference temperature ( :ref:`mp`,REFT), you can convert temperature-dependent
        secant coefficients of thermal expansion (SCTE) data from the definition temperature to the
        reference temperature. To do so, issue the :ref:`mpamod` command.

        This command is also valid in SOLUTION.

        .. _MP_enthalpy_notes:

        Considerations for Enthalpy ( ``Lab`` = ENTH)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        * To ensure correct results, you must define enthalpy over a large enough temperature range to span
          all computed temperatures during the solution. The :ref:`tb` command does not extrapolate enthalpy
          values beyond the specified temp range like the :ref:`mp` command does.

        * If both the :ref:`tb` and :ref:`mp` commands are used to specify enthalpy values, enthalpy values
          defined via the :ref:`tb` command are used and those defined via the :ref:`mp` command are
          ignored.

        .. _MP_EMIS_notes:

        Default behavior for Emissivity ( ``Lab`` = EMIS)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        There is no :ref:`command default value for emissivity, and you must specify it by issuing
        <ans_cmd_cmdDef>` :ref:`mp`,EMIS. Otherwise, an error message appears. If you issue :ref:`mp`,EMIS
        without specifying ``C0``, ``C1``, ``C2``, ``C3``, ``C4`` values, emissivity defaults to 0.

        .. _MPprodRest:

        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.
        """
        command = f"MP,{lab},{mat},{c0},{c1},{c2},{c3},{c4}"
        return self.run(command, **kwargs)



    def mpamod(self, mat: str = "", deftemp: str = "", **kwargs):
        r"""Modifies temperature-dependent secant coefficients of thermal expansion.

        Mechanical APDL Command: `MPAMOD <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MPAMOD.html>`_

        Parameters
        ----------
        mat : str
            Material number for which the secant coefficients of thermal expansion (SCTE's) are to be
            modified. Defaults to 1.

        deftemp : str
            Definition temperature at which the existing SCTE-versus-temperature tables were defined.
            Defaults to zero.

        Notes
        -----

        .. _MPAMOD_notes:

        This command converts temperature-dependent SCTE data (properties ALPX, ALPY, ALPZ) from the
        definition temperature ( ``DEFTEMP`` ) to the reference temperature defined by :ref:`mp`,REFT or
        :ref:`tref`. If both the :ref:`mp`,REFT and :ref:`tref` commands have been issued, the reference
        temperature defined by the :ref:`mp`,REFT command will be used.

        This command does not apply to the instantaneous coefficients of thermal expansion (properties CTEX,
        CTEY, CTEZ) or to the thermal strains (properties THSX, THSY, THSZ).

        This command is also valid in SOLUTION.
        """
        command = f"MPAMOD,{mat},{deftemp}"
        return self.run(command, **kwargs)



    def mpchg(self, mat: str = "", elem: str = "", **kwargs):
        r"""Changes the material number attribute of an element.

        Mechanical APDL Command: `MPCHG <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MPCHG.html>`_

        Parameters
        ----------
        mat : str
            Assign this material number to the element. Material numbers are defined with the material
            property commands ( :ref:`mp` ).

        elem : str
            Element for material change. If ALL, change materials for all selected elements ( :ref:`esel` ).

        Notes
        -----

        .. _MPCHG_notes:

        Changes the material number of the specified element. Between load steps in SOLUTION, material
        properties cannot be changed from linear to nonlinear, nonlinear to linear, or from one nonlinear
        option to another.

        If you change from one CHABOCHE model to another CHABOCHE model, the different models need to have
        the same number of data points.
        """
        command = f"MPCHG,{mat},{elem}"
        return self.run(command, **kwargs)



    def mpcopy(self, matf: str = "", matt: str = "", **kwargs):
        r"""Copies linear material model data from one material reference number to another.

        Mechanical APDL Command: `MPCOPY <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MPCOPY.html>`_

        Parameters
        ----------

        matf : str
            Material reference number from where material property data will be copied.

        matt : str
            Material reference number to where material property data will be copied.

        Notes
        -----

        .. _MPCOPY_notes:

        The :ref:`mpcopy` command copies linear material properties only, which are all properties defined
        through the :ref:`mp` command. If you copy a model that includes both linear and yield behavior
        constants (for example, a BKIN model), the :ref:`mpcopy` and :ref:`tbcopy`, ALL commands are used
        together to copy the entire model. All input data associated with the model is copied, that is, all
        data defined through the :ref:`mp` and :ref:`tb` commands.

        Also, if you copy a material model using the `Material Model Interface
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/BAS1matmodifjwf0413001150.html#BAS1mamoimisjwf0414000942>`_
         ( Edit> Copy ), both the commands :ref:`mpcopy` and :ref:`tbcopy`, ALL are issued,
        regardless of whether the model includes linear constants only, or if it includes a combination of
        linear and yield behavior constants.

        This command is also valid in SOLUTION.
        """
        command = f"MPCOPY,,{matf},{matt}"
        return self.run(command, **kwargs)



    def mpdata(self, lab: str = "", mat: str = "", sloc: str = "", c1: str = "", c2: str = "", c3: str = "", c4: str = "", c5: str = "", c6: str = "", **kwargs):
        r"""Defines property data to be associated with the temperature table.

        Mechanical APDL Command: `MPDATA <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MPDATA.html>`_

        Parameters
        ----------
        lab : str
            Valid property label. Applicable labels are listed under "Material Properties" in the input table
            for each element type in the `Element Reference <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_BIBLIO.html>`_.

            * ``ALPD`` - Mass matrix multiplier for damping.

            * ``ALPX`` - Secant coefficients of thermal expansion (also ALPY, ALPZ). (See also :ref:`mpamod`
              command for adjustment to reference temperature).

            * ``BETD`` - Stiffness matrix multiplier for damping.

            * ``BETX`` - Coefficient of diffusion expansion (also BETY, BETZ)

            * ``C`` - Specific heat.

            * ``CREF`` - Reference concentration (may not be temperature dependent)

            * ``CSAT`` - Saturated concentration

            * ``CTEX`` - Instantaneous coefficients of thermal expansion (also CTEY, CTEZ).

            * ``DENS`` - Mass density.

            * ``DMPS`` - Constant material damping coefficient.

            * ``DXX`` - Diffusivity coefficients (also DYY, DZZ)

            * ``EMIS`` - Emissivity.

            * ``ENTH`` - Enthalpy.

            * ``EX`` - Elastic moduli (also EY, EZ).

            * ``GXY`` - Shear moduli (also GYZ, GXZ).

            * ``HF`` - Convection or film coefficient.

            * ``KXX`` - Thermal conductivities (also KYY, KZZ).

            * ``LSST`` - Dielectric loss tangent.

            * ``MGXX`` - Magnetic coercive forces (also MGYY, MGZZ).

            * ``MU`` - Coefficient of friction.

            * ``MURX`` - Magnetic relative permeabilities (also MURY, MURZ).

            * ``NUXY`` - Minor Poisson's ratios (also NUYZ, NUXZ).

            * ``PERX`` - Electric relative permittivities (also PERY, PERZ).

            * ``PRXY`` - Major Poisson's ratios (also PRYZ, PRXZ).

            * ``QRATE`` - Heat generation rate.

            * ``REFT`` - Reference temperature (may not be temperature dependent).

            * ``RH`` - Hall Coefficient.

            * ``RSVX`` - Electrical resistivities (also RSVY, RSVZ).

            * ``SBKX`` - Seebeck coefficients (also SBKY, SBKZ).

            * ``SONC`` - Sonic velocity.

            * ``THSX`` - Thermal strain (also THSY, THSZ).

            * ``VISC`` - Viscosity.

        mat : str
            Material reference number to be associated with the elements (defaults to 1 if you specify zero
            or no material number).

        sloc : str
            Property data values assigned to six locations starting with ``SLOC``. If a value is already in
            this location, it is redefined. A blank (or zero) value for ``C1`` resets the previous value in
            ``SLOC`` to zero. A value of zero can only be assigned by ``C1``. Blank (or zero) values for
            ``C2`` to ``C6`` leave the corresponding previous values unchanged.

        c1 : str
            Property data values assigned to six locations starting with ``SLOC``. If a value is already in
            this location, it is redefined. A blank (or zero) value for ``C1`` resets the previous value in
            ``SLOC`` to zero. A value of zero can only be assigned by ``C1``. Blank (or zero) values for
            ``C2`` to ``C6`` leave the corresponding previous values unchanged.

        c2 : str
            Property data values assigned to six locations starting with ``SLOC``. If a value is already in
            this location, it is redefined. A blank (or zero) value for ``C1`` resets the previous value in
            ``SLOC`` to zero. A value of zero can only be assigned by ``C1``. Blank (or zero) values for
            ``C2`` to ``C6`` leave the corresponding previous values unchanged.

        c3 : str
            Property data values assigned to six locations starting with ``SLOC``. If a value is already in
            this location, it is redefined. A blank (or zero) value for ``C1`` resets the previous value in
            ``SLOC`` to zero. A value of zero can only be assigned by ``C1``. Blank (or zero) values for
            ``C2`` to ``C6`` leave the corresponding previous values unchanged.

        c4 : str
            Property data values assigned to six locations starting with ``SLOC``. If a value is already in
            this location, it is redefined. A blank (or zero) value for ``C1`` resets the previous value in
            ``SLOC`` to zero. A value of zero can only be assigned by ``C1``. Blank (or zero) values for
            ``C2`` to ``C6`` leave the corresponding previous values unchanged.

        c5 : str
            Property data values assigned to six locations starting with ``SLOC``. If a value is already in
            this location, it is redefined. A blank (or zero) value for ``C1`` resets the previous value in
            ``SLOC`` to zero. A value of zero can only be assigned by ``C1``. Blank (or zero) values for
            ``C2`` to ``C6`` leave the corresponding previous values unchanged.

        c6 : str
            Property data values assigned to six locations starting with ``SLOC``. If a value is already in
            this location, it is redefined. A blank (or zero) value for ``C1`` resets the previous value in
            ``SLOC`` to zero. A value of zero can only be assigned by ``C1``. Blank (or zero) values for
            ``C2`` to ``C6`` leave the corresponding previous values unchanged.

        Notes
        -----

        .. _MPDATA_notes:

        Defines a table of property data to be associated with the temperature table. Repeat :ref:`mpdata`
        command for additional values (100 maximum). Temperatures must be defined first ( :ref:`mptemp` ).
        Also stores assembled property function table (temperature and data) in virtual space.

        This command is also valid in SOLUTION.

        .. _MPDATA_extranote1:

        Ansys Mechanical Enterprise The command :ref:`mpdata`,LSST is only available to the Ansys Mechanical
        Enterprise product family (Ansys Mechanical Enterprise, Ansys Mechanical Enterprise PrepPost,
        and Ansys Mechanical Enterprise Solver).
        """
        command = f"MPDATA,{lab},{mat},{sloc},{c1},{c2},{c3},{c4},{c5},{c6}"
        return self.run(command, **kwargs)



    def mpdele(self, lab: str = "", mat1: str = "", mat2: str = "", inc: str = "", lchk: str = "", **kwargs):
        r"""Deletes linear material properties.

        Mechanical APDL Command: `MPDELE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MPDELE.html>`_

        Parameters
        ----------
        lab : str
            Material property label (see :ref:`mp` command for valid labels). If ALL, delete properties for
            all applicable labels.

        mat1 : str
            Delete materials from ``MAT1`` to ``MAT2`` (defaults to ``MAT1`` ) in steps of ``INC`` (defaults
            to 1). If ``MAT1`` = ALL, ``MAT2`` and ``INC`` are ignored and the properties for all materials
            are deleted.

        mat2 : str
            Delete materials from ``MAT1`` to ``MAT2`` (defaults to ``MAT1`` ) in steps of ``INC`` (defaults
            to 1). If ``MAT1`` = ALL, ``MAT2`` and ``INC`` are ignored and the properties for all materials
            are deleted.

        inc : str
            Delete materials from ``MAT1`` to ``MAT2`` (defaults to ``MAT1`` ) in steps of ``INC`` (defaults
            to 1). If ``MAT1`` = ALL, ``MAT2`` and ``INC`` are ignored and the properties for all materials
            are deleted.

        lchk : str
            Specifies the level of element-associativity checking:

            * ``NOCHECK`` - No element-associativity check occurs. This option is the default.

            * ``WARN`` - When a section, material, or real constant is associated with an element, Mechanical APDL
              issues a message warning that the necessary entity has been deleted.

            * ``CHECK`` - The command terminates, and no section, material, or real constant is deleted if it is
              associated with an element.

        Notes
        -----

        .. _MPDELE_notes:

        This command is also valid in SOLUTION.

        The ``LCHK`` argument is valid only when ``Lab`` = ALL.
        """
        command = f"MPDELE,{lab},{mat1},{mat2},{inc},{lchk}"
        return self.run(command, **kwargs)



    def mpdres(self, labf: str = "", matf: str = "", labt: str = "", matt: str = "", **kwargs):
        r"""Reassembles existing material data with the temperature table.

        Mechanical APDL Command: `MPDRES <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MPDRES.html>`_

        Parameters
        ----------
        labf : str
            Material property label associated with ``MATF``.

        matf : str
            Material reference number of property to restore from virtual space.

        labt : str
            Material property label associated with ``MATT`` (defaults to label associated with ``MATF`` ).

        matt : str
            Material reference number assigned to generated property (defaults to ``MATF`` ).

        Notes
        -----

        .. _MPDRES_notes:

        Restores into the database (from virtual space) a data table previously defined ( :ref:`mp` ) for a
        particular property, assembles data with current database temperature table, and stores back in
        virtual space as a new property.

        This command is also valid in SOLUTION.
        """
        command = f"MPDRES,{labf},{matf},{labt},{matt}"
        return self.run(command, **kwargs)



    def mplib(self, r_w_opt: str = "", path: str = "", **kwargs):
        r"""Sets the default material library read and write paths.

        Mechanical APDL Command: `/MPLIB <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MPLIB.html>`_

        Parameters
        ----------
        r_w_opt : str
            Determines what path is being set. Possible values are:

            * ``READ`` - Set the read path.

            * ``WRITE`` - Set the write path.

            * ``STAT`` - Report what read and write paths are currently in use.

        path : str
            The directory path to be used for material library files.

        Notes
        -----

        .. _s-MPLIB_notes:

        The :ref:`mplib` command sets two path strings used in conjunction with the material library feature
        and the :ref:`mpread` and :ref:`mpwrite` commands.

        For :ref:`mpread`, when you use the ``LIB`` option and no directory path is given in the file name,
        the command searches for the file in these locations: the current working directory, the user's home
        directory, the user-specified material library directory (as defined by the :ref:`mplib`,READ,
        ``PATH`` command), and :file:`/ansys_dir/matlib`.

        For :ref:`mpwrite`, when you use the ``LIB`` option and the directory portion of the specification
        for the material library file is blank, the command writes the material library file to the
        directory specified by the :ref:`mplib`,WRITE, ``PATH`` command (if that path has been set). If the
        path has not been set, the default is to write the file to the current working directory.

        The Material Library files supplied with the distribution media are meant for demonstration purposes
        only. These files are not intended for use in customer applications.
        """
        command = f"/MPLIB,{r_w_opt},{path}"
        return self.run(command, **kwargs)



    def mplist(self, mat1: str = "", mat2: str = "", inc: str = "", lab: str = "", tevl: str = "", **kwargs):
        r"""Lists linear material properties.

        Mechanical APDL Command: `MPLIST <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MPLIST.html>`_

        Parameters
        ----------
        mat1 : str
            List materials from ``MAT1`` to ``MAT2`` (defaults to ``MAT1`` ) in steps of ``INC`` (defaults
            to 1). If ``MAT1`` = ALL (default), ``MAT2`` and ``INC`` are ignored and properties for all
            material numbers are listed.

        mat2 : str
            List materials from ``MAT1`` to ``MAT2`` (defaults to ``MAT1`` ) in steps of ``INC`` (defaults
            to 1). If ``MAT1`` = ALL (default), ``MAT2`` and ``INC`` are ignored and properties for all
            material numbers are listed.

        inc : str
            List materials from ``MAT1`` to ``MAT2`` (defaults to ``MAT1`` ) in steps of ``INC`` (defaults
            to 1). If ``MAT1`` = ALL (default), ``MAT2`` and ``INC`` are ignored and properties for all
            material numbers are listed.

        lab : str
            Material property label (see the :ref:`mp` command for labels). If ALL (or blank), list
            properties for all labels. If EVLT, list properties for all labels evaluated at TEVL.

        tevl : str
            Evaluation temperature for ``Lab`` = EVLT listing (defaults to :ref:`bfunif` ).

        Notes
        -----

        .. _MPLIST_notes:

        For ``Lab``   = EVLT, when the property is from tables, the :ref:`mpplot` command will not be
        valid because the property could be a function of more than temperature.

        This command is valid in any processor.
        """
        command = f"MPLIST,{mat1},{mat2},{inc},{lab},{tevl}"
        return self.run(command, **kwargs)



    def mpplot(self, lab: str = "", mat: str = "", tmin: str = "", tmax: str = "", pmin: str = "", pmax: str = "", **kwargs):
        r"""Plots linear material properties as a function of temperature.

        Mechanical APDL Command: `MPPLOT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MPPLOT.html>`_

        Parameters
        ----------
        lab : str
            Linear material property label (EX, EY, etc.) ( :ref:`mp` ).

        mat : str
            Material reference number. Defaults to 1.

        tmin : str
            Minimum abscissa value to be displayed.

        tmax : str
            Maximum abscissa value.

        pmin : str
            Minimum property (ordinate) value to be displayed.

        pmax : str
            Maximum property value.

        Notes
        -----

        .. _MPPLOT_notes:

        When the property is from tables, the :ref:`mpplot` command will not be valid because the property
        could be a f  unction of more than temperature.

        This command is valid in any processor.
        """
        command = f"MPPLOT,{lab},{mat},{tmin},{tmax},{pmin},{pmax}"
        return self.run(command, **kwargs)



    def mpread(self, fname: str = "", ext: str = "", lib: str = "", **kwargs):
        r"""Reads a file containing material properties.

        Mechanical APDL Command: `MPREAD <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MPREAD.html>`_

        Parameters
        ----------
        fname : str
            File name and directory path (248 characters maximum, including directory). If you do not
            specify the ``LIB`` option, the default directory is the current working directory. If you
            specify the ``LIB`` option, the default is the following search path: the current working
            directory, the user's home directory, MPLIB_DIR (as specified by the :ref:`mplib`,READ, ``PATH``
            command) and :file:`/ansys_dir/matlib` (as defined by installation). If you use the default for
            your directory, you can use all 248 characters for the file name.

            The file name defaults to :file:`Jobname`.

        ext : str
            Filename extension (eight-character maximum). If you omit the default extension is MP. extension
            is units_MPL, where units is the system of units currently in use. (See the description of the
            :ref:`units` command.) For example, if :ref:`units` is set to SI, the extension defaults to
            SI_MPL.

        lib : str
            Reads material library files previously written with the :ref:`mpwrite` command. (See the
            description of the LIB option for the :ref:`mpwrite` command.) The only allowed value for LIB is
            LIB.

            The LIB field indicates that the specified file was written by :ref:`mpwrite` using the LIB
            option, and that the file is consistent with the material library file format. When the
            :ref:`mpread` command executes, Mechanical APDL reads material properties defined in the
            specified file into the current Mechanical APDL working database. The currently selected
            material, as defined by the :ref:`mat` command ( :ref:`mat`,MAT), determines the material number
            used when reading the material properties. The LIB option for :ref:`mpread` and :ref:`mpwrite`
            supports storing and retrieving both linear and nonlinear properties.

        Notes
        -----

        .. _MPREAD_notes:

        Material properties written to a file without the LIB option do not support nonlinear properties.
        Also, properties written to a file without the LIB option are restored in the same material number
        as originally defined. To avoid errors, use :ref:`mpread` with the LIB option only when reading
        files written using :ref:`mpwrite` with the LIB option.

        If you omit the LIB option for :ref:`mpread`, this command supports only linear properties.

        Material numbers are hardcoded. If you write a material file without specifying the LIB option, then
        read that file in via the :ref:`mpread` command with the LIB option, Mechanical APDL does not write
        the
        file to a new material number; instead, it writes the file to the old material number (the number
        specified on the :ref:`mpwrite` command that created the file.)

        This command is also valid in SOLUTION.
        """
        command = f"MPREAD,{fname},{ext},,{lib}"
        return self.run(command, **kwargs)



    def mptemp(self, sloc: str = "", t1: str = "", t2: str = "", t3: str = "", t4: str = "", t5: str = "", t6: str = "", **kwargs):
        r"""Defines a temperature table for material properties.

        Mechanical APDL Command: `MPTEMP <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MPTEMP.html>`_

        Parameters
        ----------
        sloc : str
            Starting location in table for entering temperatures. For example, if ``SLOC`` = 1, data input
            in the ``T1`` field applies to the first constant in the table. If ``SLOC`` = 7, data input in
            the ``T1`` field applies to the seventh constant in the table, etc. Defaults to the last
            location filled + 1.

        t1 : str
            Temperatures assigned to six locations starting with ``SLOC``. If a value is already in this
            location, it will be redefined. A blank (or zero) value for ``T1`` resets the previous value in
            ``SLOC`` to zero. A value of zero can only be assigned by ``T1``. Blank (or zero) values for
            ``T2`` to ``T6`` leave the corresponding previous values unchanged.

        t2 : str
            Temperatures assigned to six locations starting with ``SLOC``. If a value is already in this
            location, it will be redefined. A blank (or zero) value for ``T1`` resets the previous value in
            ``SLOC`` to zero. A value of zero can only be assigned by ``T1``. Blank (or zero) values for
            ``T2`` to ``T6`` leave the corresponding previous values unchanged.

        t3 : str
            Temperatures assigned to six locations starting with ``SLOC``. If a value is already in this
            location, it will be redefined. A blank (or zero) value for ``T1`` resets the previous value in
            ``SLOC`` to zero. A value of zero can only be assigned by ``T1``. Blank (or zero) values for
            ``T2`` to ``T6`` leave the corresponding previous values unchanged.

        t4 : str
            Temperatures assigned to six locations starting with ``SLOC``. If a value is already in this
            location, it will be redefined. A blank (or zero) value for ``T1`` resets the previous value in
            ``SLOC`` to zero. A value of zero can only be assigned by ``T1``. Blank (or zero) values for
            ``T2`` to ``T6`` leave the corresponding previous values unchanged.

        t5 : str
            Temperatures assigned to six locations starting with ``SLOC``. If a value is already in this
            location, it will be redefined. A blank (or zero) value for ``T1`` resets the previous value in
            ``SLOC`` to zero. A value of zero can only be assigned by ``T1``. Blank (or zero) values for
            ``T2`` to ``T6`` leave the corresponding previous values unchanged.

        t6 : str
            Temperatures assigned to six locations starting with ``SLOC``. If a value is already in this
            location, it will be redefined. A blank (or zero) value for ``T1`` resets the previous value in
            ``SLOC`` to zero. A value of zero can only be assigned by ``T1``. Blank (or zero) values for
            ``T2`` to ``T6`` leave the corresponding previous values unchanged.

        Notes
        -----

        .. _MPTEMP_notes:

        Defines a temperature table to be associated with the property data table ( :ref:`mpdata` ). These
        temperatures are also used for polynomial property evaluation, if defined ( :ref:`mp` ).
        Temperatures must be defined in non-descending order. Issue :ref:`mater` $ :ref:`stat` to list the
        current temperature table. Repeat :ref:`mptemp` command for additional temperatures (100 maximum).
        If all arguments are blank, the temperature table is erased.

        For clear definition, the temperature range you define with the :ref:`mptemp` command should include
        the entire range you'll use in subsequently defined materials. To assist the user in this, the first
        (and only the first) excursion out of the temperature range defined by the :ref:`mptemp` commands is
        flagged with a warning message. Similarly, the reference temperature ( :ref:`tref` or :ref:`mp`
        ,REFT commands) should also fall in this same temperature range. If not and :ref:`mp`,ALPX was
        used, a note will be output. If not, and :ref:`mp`,CTEX or :ref:`mp`,THSX was used, an error
        message will be output.

        This command is also valid in SOLUTION.
        """
        command = f"MPTEMP,{sloc},{t1},{t2},{t3},{t4},{t5},{t6}"
        return self.run(command, **kwargs)



    def mptgen(self, stloc: str = "", num: str = "", tstrt: str = "", tinc: str = "", **kwargs):
        r"""Adds temperatures to the temperature table by generation.

        Mechanical APDL Command: `MPTGEN <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MPTGEN.html>`_

        Parameters
        ----------
        stloc : str
            Starting location in table for generating temperatures. Defaults to last location filled + 1.

        num : str
            Number of temperatures to be generated (1-100).

        tstrt : str
            Temperature assigned to ``STLOC`` location.

        tinc : str
            Increment previous temperature by ``TINC`` and assign to next location until all ``NUM``
            locations are filled.

        Notes
        -----

        .. _MPTGEN_notes:

        Adds temperatures to the temperature table by generation. May be used in combination (or in place
        of) the :ref:`mptemp` command.

        This command is also valid in SOLUTION.
        """
        command = f"MPTGEN,{stloc},{num},{tstrt},{tinc}"
        return self.run(command, **kwargs)



    def mptres(self, lab: str = "", mat: str = "", **kwargs):
        r"""Restores a temperature table previously defined.

        Mechanical APDL Command: `MPTRES <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MPTRES.html>`_

        Parameters
        ----------
        lab : str
            Material property label ( :ref:`mp` ).

        mat : str
            Material reference number.

        Notes
        -----

        .. _MPTRES_notes:

        Restores into the database (from virtual space) a temperature table previously defined ( :ref:`mp` )
        for a particular property. The existing temperature table in the database is erased before this
        operation.

        This command is also valid in SOLUTION.
        """
        command = f"MPTRES,{lab},{mat}"
        return self.run(command, **kwargs)



    def mpwrite(self, fname: str = "", ext: str = "", lib: str = "", mat: str = "", **kwargs):
        r"""Writes linear material properties in the database to a file (if the LIB option is not specified) or
        writes both linear and nonlinear material properties (if LIB is specified) from the database to a
        file.

        Mechanical APDL Command: `MPWRITE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MPWRITE.html>`_

        Parameters
        ----------
        fname : str
            File name and directory path (248 characters maximum, including directory). If you do not
            specify the ``LIB`` option, the default directory is the current working directory. If you
            specify ``LIB`` and you have specified a material library directory (via the :ref:`mplib`
            command), that directory is the default. Otherwise, the default is the current working
            directory. If you use the default for your directory, you can use all 248 characters for the
            file name.

            The file name defaults to :file:`Jobname`.

        ext : str
            Filename extension (eight-character maximum). If you omit the ``LIB`` option, the default
            extension is MP. If you specify the ``LIB`` option, the default extension is units_MPL, where
            units is the system of units currently in use. (See the description of the :ref:`units`
            command.) For example, if :ref:`units` is set to BIN, the extension defaults to BIN_MPL.

        lib : str
            The only value allowed for this field is the string "LIB."

            The LIB option indicates that you wish to have properties associated with the material (MAT)
            written to the specified material library file using the material library file format. The
            material library file format is ASCII-text-based Mechanical APDL command input. Certain commands
            associated with this format have been modified to interpret the string "_MATL" to mean the
            currently selected material. This feature makes the material library file independent of the
            material number in effect when the file was written; this enables you to restore the properties
            into the Mechanical APDL database using the material number of your choice. The LIB option also
            enables you to save both linear and nonlinear properties. If you omit the LIB option, you can
            save linear properties only.

        mat : str
            Specifies the material to be written to the named material library file. There is no default;
            you must either specify a material or omit the ``MAT`` argument. Even if you specify a ``MAT``
            value, Mechanical APDL ignores it if the LIB argument is not specified.

        Notes
        -----

        .. _MPWRITE_notes:

        Writes linear material properties currently in the database to a file. The file is rewound before
        and after writing.

        This command is also valid in SOLUTION.
        """
        command = f"MPWRITE,{fname},{ext},,{lib},{mat}"
        return self.run(command, **kwargs)



    def tbfplot(self, matid: str = "", curvefitname: str = "", expdatid: str = "", colx: str = "", coly1: str = "", coly2: str = "", **kwargs):
        r"""Plots `material curve-fitting
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/Hlp_AM_GMCF.html>`_ data.

        Mechanical APDL Command: `TBFPLOT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_TBFPLOT.html>`_

        Parameters
        ----------
        matid : str
            Material reference identification number.

        curvefitname : str
            Material curve-fitting model name (obtainable via :ref:`tbft`,LIST). Enclose the name within
            single quotes.

        expdatid : str
            Experimental data ID.

        colx : str
            Experimental data column to use in the X axis.

        coly1 : str
            Experimental data column to use in the Y axis.

        coly2 : str
            Fitted-data column to use in the Y axis.

        Notes
        -----

        .. _TBFPLOT_notes:

        This command plots the fitted data specified via ``ColY2`` (the number of experimental data columns
        + 1) and the data specified via ``ColY1`` as a function of the X-axis data specified via ``ColX``.

        Issue this command after curve-fitting has been completed ( :ref:`tbft`,SOLVE).

        Material curve-fitting does not support saving to ( :ref:`save` ) and resuming from ( :ref:`resume`
        ) the database file. You must therefore rerun the curve-fitting analysis, then issue :ref:`tbfplot`
        again to replot.
        """
        command = f"TBFPLOT,{matid},{curvefitname},{expdatid},{colx},{coly1},{coly2}"
        return self.run(command, **kwargs)



    def tbft(self, **kwargs):
        r"""Performs `material curve-fitting
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/Hlp_AM_GMCF.html>`_ operations.

        Mechanical APDL Command: `TBFT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_TBFT.html>`_

        Notes
        -----

        .. warning::

           This function contains specificities regarding the argument definitions.
           Please refer to the `command documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_TBFT.html>`_
           for further explanations.

        *\*TBFT Specifications for Hyperelastic Models**

        .. _TBFThypspec:

        :ref:`tbft`, ``Oper``, ``MATID``, ``Option1``, ``Option2``, ``Option3``, ``Option4``, ``Option5``,
        ``Option6``, ``Option7``

        * ``Oper`` - The operation to perform:

          * ``Operation Set 1 (Curve-Fitting)`` - - - - - - - - - - - - - - - - - - - - -

          * ``FADD`` - Define a constitutive model for parameter fitting and import all parameters (defined
            previously via :ref:`tb` and :ref:`tbdata` ).

          * ``FDEL`` - Delete a constitutive model.

          * ``FSET`` - Write data related to a constitutive model to the database (same as :ref:`tb` command).

          * ``SET`` - Initialize coefficients of a constitutive model for nonlinear curve-fitting procedure.

          * ``CDEL`` - Deletes coefficients at current reference temperature. Applicable only for temperature
            dependent coefficients.

          * ``SOLVE`` - Solve for coefficients.

          * ``FIX`` - Fix (hold constant) the coefficient you specify in ``Option4``.

          * ``Operation Set 2 (Experimental Data)`` - - - - - - - - - - - - - - - - - - - - -

          * ``EADD`` - Add experimental data.

          * ``EDEL`` - Delete experimental data.

          * ``Other Operations`` - - - - - - - - - - - - - - - - - - - - -

          * ``LIST`` - List all data associated with the material model represented by the material ID number
            ( ``MATID`` )

        * ``MATID`` - Material reference identification number (same as ``MAT`` argument used in the
          :ref:`tb` command). Valid value is any number ``n``, where 0 < ``n`` < 100,000. Default = 1.

        * ``Option1`` - For curve-fit function operations ( ``Oper`` = FADD, FDEL, FSET, SET, CDEL, SOLVE or
        FIX) this value
          specifies the category (AML).

          For adding or deleting your experiment ( ``Oper`` = EADD or EDEL), this value specifies the experimental data type. **Valid options:** UNIA (default), BIAX, SHEA, SSHE,and VOLU.

        * ``Option2`` - For curve-fit function operations ( ``Oper`` = FADD, FDEL, FSET, SET, CDEL, SOLVE,
          or FIX), set this value to GENR.

          When you need to specify a file name from which to get experimental data ( ``Oper`` = EADD), place
          that string here. Valid value is any file name string. You can enter the entire
          :file:`path\filename.extension` string and leave the next two values ( ``Option3`` and ``Option4`` )
          blank, or you can specify the name here, the extension in the next value, and the path following.

        * ``Option3`` - For ``Oper`` = FADD, FDEL, FSET, CDEL, SET, SOLVE or FIX, set this value to a user-
          defined name (to be used consistently in the curve-fitting process).

          If a file name for experimental data is being specified in ``Option2`` ( ``Oper`` = EADD), this
          value will contain the file extension.

        * ``Option4`` - When you are working on a specific coefficient ( ``Oper`` = FIX), this value
          specifies the index of that coefficient. Valid values vary from 1 to ``n``, where ``n`` is the total
          number of coefficients. Default = 1.

          For ``Oper`` = SET, see :ref:`tbfthypsetvals`, below.

          If a file name for experimental data is being specified in ``Option2`` ( ``Oper`` = EADD), this
          value will contain the directory/path specification.

          If ``Oper`` = SOLVE, this value specifies the curve-fitting procedure. Valid values are 0 for non-
          normalized least squares curve-fitting procedure, and 1 for normalized least squares curve-fitting
          procedure.

        * ``Option5`` - When you are working on a specific coefficient ( ``Oper`` = FIX), this value
        specifies the index of
          that coefficient. Valid values vary from 1 to N, where N is the total number of coefficients.
          Default = 1.

          For ``Oper`` = SET, see :ref:`tbfthypsetvals`, below.

          .. _tbfthypsetvals:

          Set Operations
          **************

          .. flat-table::
             :header-rows: 1

             * - Purpose
               - Option4
               - Option5
             * - Set the value of the coefficient.
               - Index of coefficient
               - Value of that coefficient
             * - Set temperature dependency ON/OFF Specify temperature data in the same specified via :ref:`tref`.
               - TDEP
               - 1 -- ON   0 -- OFF
             * - Set reference temperature
               - TREF
               - Temperature value

          If ``Oper`` = SOLVE, use this value to specify the number of iterations to be used in the
          calculation of the coefficients. Valid value is any positive integer. Default = 1000.

        * ``Option6`` - If ``Oper`` = SOLVE, specifies the allowed tolerance in residual change to stop an
          iteration. Valid value is 0.0 to 1.0. Default = 0.0.

        * ``Option7`` - If ``Oper`` = SOLVE, specifies the allowed tolerance in coefficient change to stop
          an iteration. Valid value is 0 to 1. Default = 0.

        For the supported list of material models, see.

        This table summarizes the format for hyperelastic curve-fitting operations via :ref:`tbft` :

        Hyperelastic Model Command Summary
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.

        *\*TBFT Specifications for Viscoelastic Models**

        .. _TBFTviscspec:

        :ref:`tbft`, ``Oper``, ``MATID``, ``Option1``, ``Option2``, ``Option3``, ``Option4``, ``Option5``,
        ``Option6``, ``Option7``

        * ``Oper`` - The operation to perform:

          * ``Operation Set 1 (Curve-Fitting)`` - - - - - - - - - - - - - - - - - - - - -

          * ``FADD`` - Define a constitutive model.

          * ``FDEL`` - Delete a constitutive model.

          * ``FSET`` - Write data related to a constitutive model to the database (same as :ref:`tb` command).

          * ``SET`` - Initialize coefficients of a constitutive model for nonlinear curve-fitting procedure.

          * ``CDEL`` - Deletes coefficients at current reference temperature. Applicable only for temperature
            dependent coefficients.

          * ``SOLVE`` - Solve for coefficients.

          * ``FIX`` - Fix (hold constant) the coefficient you specify in ``Option4``.

          * ``Operation Set 2 (Experimental Data)`` - - - - - - - - - - - - - - - - - - - - -

          * ``EADD`` - Add experimental data.

          * ``EDEL`` - Delete experimental data.

          * ``Other Operations`` - - - - - - - - - - - - - - - - - - - - -

          * ``LIST`` - List all data associated with the material model represented by the material ID number
            ( ``MATID`` )

        * ``MATID`` - Material reference identification number (same as ``MAT`` argument used in the
          :ref:`tb` command). Valid value is any number ``n``, where 0 < ``n`` < 100,000. Default = 1.

        * ``Option1`` - For curve-fitting function operations ( ``Oper`` = FADD, FDEL, FSET, SET, CDEL,
        SOLVE, or FIX), this
          value is set to AML.

          For adding or deleting your experiment ( ``Oper`` = EADD or EDEL), this value specifies the experiment type. **Valid options:** SDEC (Shear Modulus vs. Time/Freq) or BDEC (Bulk Modulus vs. Time/Freq).

        * ``Option2`` - For curve-fitting function operations ( ``Oper`` = FADD, FDEL, FSET, SET, CDEL,
          SOLVE, or FIX), this value is set to GENR.

          When you need to specify a file name from which to get experimental data ( ``Oper`` = EADD), place
          that string here. Valid value is any file name string. You can enter the entire
          :file:`path\filename.extension` string and leave the next two values ( ``Option3`` and ``Option4`` )
          blank, or you can specify the name here, the extension in the next value, and the path following.

        * ``Option3`` - For ``Oper`` = FADD, FDEL, FSET, CDEL, SET, SOLVE, or FIX, set this value to any
          user-defined name (to be used consistently during the curve-fitting process).

          If a file name for experimental data is being specified in ``Option2`` ( ``Oper`` = EADD), this
          value will contain the file extension.

        * ``Option4`` - When you are working on a specific coefficient ( ``Oper`` = FIX), this value
          specifies the index of that coefficient. Valid values vary from 1 to ``n``, where ``n`` is the total
          number of coefficients. Default = 1.

          For ``Oper`` = SET, see :ref:`tbftvscsetvals` below.

          You can also specify ``TREF`` to indicate the reference temperature.

          If a file name for experimental data is being specified in ``Option2`` ( ``Oper`` = EADD), this
          value will contain the directory/path specification.

          If ``Oper`` = SOLVE, this value specifies the curve-fitting procedure. Valid values are 0 for non-
          normalized least squares curve-fitting procedure, and 1 for normalized least squares curve-fitting
          procedure.

        * ``Option5`` - For ``Oper`` = SET, see :ref:`tbftvscsetvals` below.

          .. _tbftvscsetvals:

          Set Operations
          **************

          .. flat-table::
             :header-rows: 1

             * - Purpose
               - Option4
               - Option5
             * - Set the value of the coefficient
               - Index of coefficient
               - Value of coefficient
             * - Set temperature dependency ON/OFF
               - TDEP
               - 1 for ON and 0 for OFF
             * - Set reference temperature
               - TREF
               - Temperature value

          If ``Oper`` = SOLVE, use this value to specify the number of iterations to be used in the
          calculation of the coefficients. Valid value is any positive integer. Default = 1000.

          If you are specifying a coefficient to be held constant ( ``Oper`` = FIX):

          * 1 - Fix the specified coefficient.
          * 0 - Allow the specified coefficient to vary (disable fixing).

        * ``Option6`` - If ``Oper`` = SOLVE, specifies the allowed tolerance in residual change to stop an
          iteration. Valid value is 0.0 to 1.0. Default = 0.0.

        * ``Option7`` - If ``Oper`` = SOLVE, specifies the allowed tolerance in coefficient change to stop
          an iteration. Valid value is 0 to 1. Default = 0.

        This table summarizes the format for viscoelastic curve-fitting operations via :ref:`tbft` :

        Viscoelastic Model Command Summary
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.

        *\*TBFT Specifications for Chaboche Kinematic Hardening Plasticity Models**

        .. _TBFTchabspec:

        :ref:`tbft`, ``Oper``, ``MATID``, ``Option1``, ``Option2``, ``Option3``, ``Option4``, ``Option5``,
        ``Option6``, ``Option7``, -, -, ``Option10``

        * ``Oper`` - The operation to perform:

          * ``Operation Set 1 (Curve-Fitting)`` - - - - - - - - - - - - - - - - - - - - -

          * ``FCASE`` - Define a case/constitutive model for plasticity.

          * ``FADD`` - Define a constitutive model.

          * ``FDEL`` - Delete a constitutive model.

          * ``FSET`` - Write data related to a constitutive model to the database (same as :ref:`tb` command).

          * ``SET`` - Initialize coefficients of a constitutive model for nonlinear curve-fitting procedure.

          * ``CDEL`` - Deletes coefficients at current reference temperature. Applicable only for temperature-
            dependent coefficients.

          * ``SOLVE`` - Solve for coefficients.

          * ``FIX`` - Fix (hold constant) the coefficient you specify in ``Option4``.

          * ``Operation Set 2 (Experimental Data)`` - - - - - - - - - - - - - - - - - - - - -

          * ``EADD`` - Add experimental data.

          * ``EDEL`` - Delete experimental data.

          * ``Other Operations`` - - - - - - - - - - - - - - - - - - - - -

          * ``LIST`` - List all data associated with the material model represented by the material ID number
            ( ``MATID`` ).

        * ``MATID`` - Material reference identification number (same as ``MAT`` argument used in the
          :ref:`tb` command). Valid value is any number greater than zero (default = 1) but less than 100,000.

        * ``Option1`` - For ``Oper`` = FCASE, set to either NEW or FINI. The command :ref:`tbft`,FCASE,
          ``MATID``,NEW initializes a new curve-fitting case. (The :ref:`tbft`,FADD commands described next
          are always issued between :ref:`tbft`,FCASE, ``MATID``,NEW and :ref:`tbft`,FCASE, ``MATID``,FINI
          commands.) After issuing :ref:`tbft`,FCASE, ``MATID``,FINI, the Chaboche model is created and is
          ready to be used to perform other curve-fitting operations. For more information, see `Material
          Curve-Fitting <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/Hlp_AM_GMCF.html>`_

          For ``Oper`` = FADD, set to PLAS to add options/parameters for the new case being created (via
          :ref:`tbft`,FCASE, ``MATID``,NEW, which must be issued before the :ref:`tbft`,FADD command). This
          operation specifies the order of the Chaboche kinematic model.

          For other curve-fitting function operations ( ``Oper`` = FDEL, FSET, SET, CDEL, SOLVE or FIX), set
          to CASE.

          For adding or deleting your experiment ( ``Oper`` = EADD or EDEL), this option specifies the
          experiment type. The only valid option is UNIA (plastic strain vs. true stress).

        * ``Option2`` - For ``Oper`` = FCASE (defining your Chaboche case), set to CPLA.

          For ``Oper`` = FDEL, FSET, SET, CDEL, SOLVE, or FIX (curve-fitting function operations), this value
          specifies the case name being operated on.

          For ``Oper`` = FADD (specifying options for the plasticity model), valid options are:

          * CHAB -- Chaboche kinematic hardening (required for any defined curve-fitting case)
          * BISO -- Bilinear isotropic hardening (optional)
          * MISO -- Multilinear isotropic hardening (optional)
          * VOCE -- Nonlinear isotropic hardening, Voce model (optional)
          * The :ref:`tbft`,FADD command can be issued twice, once to specify the order of the Chaboche model,
            and again to specify the isotropic hardening option. (Only one of the options BISO, MISO or VOCE
            can be used in a single curve-fitting case, and none of those options are required.)

          For ``Oper`` = EADD (specifying a file name from which to get experimental data), place that string
          here. A valid entry is any file name string. You can either:

          * Enter the entire :file:`path\filename.extension` string and leave the next two values (
            ``Option3`` and ``Option4`` ) blank, or

          * Specify the name here, the extension in the next value, and the path in the following value.

        * ``Option3`` - For ``Oper`` = FCASE, this value specifies the case name.

          For ``Oper`` = FADD, this value specifies either:

          * The order of the Chaboche kinematic hardening model ( ``Option2`` = CHAB), or

          * The number of terms in the MISO model ( ``Option2`` = MISO).

          If a file name for experimental data is being specified in ``Option2`` ( ``Oper`` = EADD), this
          value contains the file extension.

        * ``Option4`` - When fixing a specific coefficient to a desired value ( ``Oper`` = FIX), this value
          specifies the index of that coefficient. Valid values vary from 1 to ``n``, where ``n`` is the total
          number of coefficients. Default = 1.

          For ``Oper`` = SET, see :ref:`tbftvscsetvals`.

          You can also specify ``TREF`` to indicate the reference temperature, or ``COMP`` for a
          partial/complete solution (only for bulk, only for shear, or all coefficients).

          If a file name for experimental data is being specified in ``Option2`` ( ``Oper`` = EADD), this
          value contains the directory/path specification.

          If ``Oper`` = SOLVE, this value specifies the normalized/non-normalized option. This option is not
          available for Chaboche curve-fitting.

        * ``Option5`` - For ``Oper`` = SET, refer to the following table.

          .. _tbftchabsetvals:

          Set Operations
          **************

          .. flat-table::
             :header-rows: 1

             * - Purpose
               - Option4
               - Option5
             * - Set the value of the coefficient
               - Index of coefficient
               - Value of coefficient
             * - Set temperature dependency ON/OFF
               - TDEP
               - 1 for ON and 0 for OFF
             * - Set reference temperature
               - TREF
               - Temperature value

          If ``Oper`` = SOLVE, use this value to specify the number of iterations to be used in the
          calculation of the coefficients. Valid value is any positive integer. Default = 1000.

          If you are specifying a coefficient to be held constant ( ``Oper`` = FIX):

          * 1 - Fix the specified coefficient.
          * 0 - Allow the specified coefficient to vary (disable fixing).

        * ``Option6`` - If ``Oper`` = SOLVE, specifies the allowed tolerance in residual change to stop an
          iteration. Valid value is 0.0 to 1.0. Default = 0.0.

        * ``Option7`` - If ``Oper`` = SOLVE, specifies the allowed tolerance in coefficient change to stop
          an iteration. Valid value is 0 to 1. Default = 0.

        * ``-`` - Reserved for future use.

        * ``-`` - Reserved for future use.

        * ``Option10`` - If ``Oper`` = SOLVE, enables parameter scaling when set to 1. Default = 0. Used for
          Chaboche material curve-fitting.

        This table summarizes the format for Chaboche curve-fitting operations via :ref:`tbft` :

        Chaboche Model Command Summary
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.

        *\*TBFT Specifications for Creep Models**

        .. _TBFTcreepspec:

        :ref:`tbft`, ``Oper``, ``MATID``, ``Option1``, ``Option2``, ``Option3``, ``Option4``, ``Option5``,
        ``Option6``, ``Option7``, -, -, ``Option10``

        * ``Oper`` - The operation to perform:

          * ``Operation Set 1 (Curve-Fitting)`` - - - - - - - - - - - - - - - - - - - - -

          * ``FADD`` - Define a constitutive model.

          * ``FDEL`` - Delete a constitutive model.

          * ``FSET`` - Write data related to a constitutive model to the database (same as :ref:`tb` command).

          * ``SET`` - Initialize coefficients of a constitutive model for nonlinear curve-fitting procedure.

          * ``CDEL`` - Deletes coefficients at current reference temperature. Applicable only for temperature
            dependent coefficients.

          * ``SOLVE`` - Solve for coefficients.

          * ``FIX`` - Fix (hold constant) the coefficient you specify in ``Option4``.

          * ``Operation Set 2 (Experimental Data)`` - - - - - - - - - - - - - - - - - - - - -

          * ``EADD`` - Add experimental data.

          * ``EDEL`` - Delete experimental data.

          * ``Other Operations`` - - - - - - - - - - - - - - - - - - - - -

          * ``LIST`` - List all data associated with the material model represented by the material ID number
            ( ``MATID`` )

        * ``MATID`` - Material reference identification number (same as ``MAT`` argument used in the
          :ref:`tb` command). Valid value is any number ``n``, where 0 < ``n`` < 100,000. Default = 1.

        * ``Option1`` - For curve-fit function operations ( ``Oper`` = FADD, FDEL, FSET, SET, CDEL, SOLVE or
          FIX) this value specifies the category (CREEP).

          For adding or deleting your experiment ( ``Oper`` = EADD or EDEL), this value specifies the
          experimental data type (CREEP).

        * ``Option2`` - For curve-fit function operations ( ``Oper`` = FADD, FDEL, FSET, SET, CDEL, SOLVE,
          or FIX), this value specifies constitutive model type. The valid values are listed in
          :ref:`tbftcreepoption` below.

          When you need to specify a file name from which to get experimental data ( ``Oper`` = EADD), place
          that string here. Valid value is any file name string. You can enter the entire
          :file:`path\filename.extension` string and leave the next two values ( ``Option3`` and ``Option4`` )
          blank, or you can specify the name here, the extension in the next value, and the path following.

        * ``Option3`` - If a file name for experimental data is being specified in ``Option2`` ( ``Oper`` =
          EADD), this value will contain the file extension.

        * ``Option4`` - When you are working on a specific coefficient ( ``Oper`` = FIX), this value,
          specifies the index of that coefficient. Valid values vary from 1 to ``n``, where ``n`` is the total
          number of coefficients. Default = 1.

          For ``Oper`` = SET, see :ref:`tbftcrpsetvals`, below.

          If a file name for experimental data is being specified in ``Option2`` ( ``Oper`` = EADD), this
          value will contain the directory/path specification.

          If ``Oper`` = SOLVE, this value specifies the curve-fitting procedure. Valid values are 0 for non-
          normalized least squares curve-fitting procedure, and 1 for normalized least squares curve-fitting
          procedure.

        * ``Option5`` - If ``Oper`` = SOLVE, use this value to specify the number of iterations to be used
        in the
          calculation of the coefficients. Valid value is any positive integer. Default = 1000.

          If you are specifying a coefficient to be held constant ( ``Oper`` = FIX):

          * 1 - Fix the specified coefficient.
          * 0 - Allow the specified coefficient to vary (disable fixing).

          For ``Oper`` = SET, see :ref:`tbftcrpsetvals`, below.

          .. _tbftcrpsetvals:

          Set Operations
          **************

          .. flat-table::
             :header-rows: 1

             * - Purpose
               - Option4
               - Option5
             * - Set the value of the coefficient
               - Index of coefficient
               - Value of coefficient
             * - Set temperature dependency ON When TDEP is OFF, the Arrhenius term (C4) in the strain-hardening creep equation is calculated. Because :ref:`tbtemp` is not included in the curve-fitting, the experimental data (in absolute temperature) must be provided via ``/TEMP``.   /OFF When TDEP is ON, the Arrhenius term is set to 0 and the constants are calculated separately for each temperature. The curve-fitting process uses :ref:`tbtemp`. You must provide the experimental data using the same units as specified via :ref:`tref`.
               - TDEP
               - 1 -- ON   0 -- OFF
             * - Set reference temperature
               - TREF
               - Temperature value

        * ``Option6`` - If ``Oper`` = SOLVE, specifies the allowed tolerance in residual change to stop an
          iteration. Valid value is 0.0 to 1.0. Default = 0.0.

        * ``Option7`` - If ``Oper`` = SOLVE, specifies the allowed tolerance in coefficient change to stop
          an iteration. Valid value is 0 to 1. Default = 0.

        * ``-`` - Reserved for future use.

        * ``-`` - Reserved for future use.

        * ``Option10`` - If ``Oper`` = SOLVE, enables parameter scaling when set to 1. Default = 0. Used for
          creep material curve-fitting.

        .. _tbftcreepoption:

        Creep Options
        *************

        .. flat-table::
           :header-rows: 1

           * - Category
             - Name
             - Option
           * - CREEP
             - SHAR
             - NA
           * - CREEP
             - THAR
             - NA
           * - CREEP
             - GEXP
             - NA
           * - CREEP
             - GGRA
             - NA
           * - CREEP
             - GBLA
             - NA
           * - CREEP
             - MTHA
             - NA
           * - CREEP
             - MSHA
             - NA
           * - CREEP
             - GGAR
             - NA
           * - CREEP
             - EXPO
             - NA
           * - CREEP
             - NORT
             - NA
           * - CREEP
             - PSTH
             - NA
           * - CREEP
             - PSRP
             - NA
           * - CREEP
             - GTHA
             - NA

        This table summarizes the format for creep curve-fitting operations via :ref:`tbft` :

        Creep Model Command Summary
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^

        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.

        *\*TBFT Specifications for Thermomechanical Fatigue (TMF)and Plasticity Model Combinations**

        .. _TBFTtmfspec:

        :ref:`tbft`, ``Oper``, ``MATID``, ``Option1``, ``Option2``, ``Option3``, ``Option4``, ``Option5``,
        ``Option6``, ``Option7``

        * ``Oper`` - The operation to perform:

          * ``Operation Set 1 (Curve-Fitting)`` - - - - - - - - - - - - - - - - - - - - -

          * ``FADD`` - Define a constitutive model.

          * ``FDEL`` - Delete a constitutive model.

          * ``FSET`` - Write data related to a constitutive model to the database (same as :ref:`tb` command).

          * ``SET`` - Initialize coefficients of a constitutive model for nonlinear curve-fitting procedure.

          * ``CDEL`` - Deletes coefficients at current reference temperature. Applicable only for temperature-
            dependent coefficients.

          * ``AINI`` - Automatically initialize coefficients based on elastic properties and experimental
            data.

          * ``SOLVE`` - Solve for coefficients.

          * ``PSOLVE`` - Custom multistep solve for coefficients.

          * ``FIX`` - Fix (hold constant) the coefficient you specify in ``Option4``.

          * ``Operation Set 2 (Experimental Data)`` - - - - - - - - - - - - - - - - - - - - -

          * ``EADD`` - Add experimental data.

          * ``EDEL`` - Delete experimental data.

          * ``Other Operations`` - - - - - - - - - - - - - - - - - - - - -

          * ``LIST`` - List all data associated with the material model represented by the material ID number
            ( ``MATID`` ).

        * ``MATID`` - Material reference identification number. (Same as :ref:`tb`, ``MATID``.) Valid value
          is any number ``n``, where 0 < ``n`` < 100,000. Default = 1.

        * ``Option1`` - AML - For curve-fitting function operations ( ``Oper`` = Operation Set 1), this
          value specifies the category.

          UNIA - For adding or deleting your experiment (Operation Set 2), this value specifies the
          experimental data type.

        * ``Option2`` - For curve-fitting function operations ( ``Oper`` = Operation Set 1), this value
          specifies the constitutive model type. The only valid value is GENR (generic).

          To obtain experimental data ( ``Oper`` = EADD in Operation Set 2) from a file, specify any valid
          file name. (You can either specify the entire ``path`` \ ``filename`` . ``extension`` string here
          and leave ``Option3`` and ``Option4`` blank, or specify ``filename`` here, ``extension`` in
          ``Option3``, and ``path`` in ``Option4``.)

        * ``Option3`` - For curve-fitting function operations ( ``Oper`` = Operation Set 1), specify a
          unique name for your curve-fitting model.

          For obtaining experimental data ( Oper = EADD in Operation Set 2) from a file specified in Option2,
          specify the file extension.

        * ``Option4`` - When fixing a specific coefficient to a desired value ( ``Oper`` = FIX), this value
          specifies the index of that coefficient. Valid values vary from 1 to ``n``, where ``n`` is the total
          number of coefficients. Default = 1.

          For ``Oper`` = SET, see :ref:`tmftableoperset`.

          You can also specify ``TREF`` to indicate the reference temperature, or ``COMP`` for a
          partial/complete solution (only for bulk, only for shear, or all coefficients).

          If ``Oper`` = SOLVE, this value specifies the curve-fitting procedure. Valid values are 0 for non-
          normalized least squares curve-fitting procedure, and 1 for normalized least squares curve-fitting
          procedure.

          For obtaining experimental data ( Oper = EADD) from a file specified in Option2, specify the path in
          which the file resides.

        * ``Option5`` - For ``Oper`` = SET, refer to the following table:

          .. _tmftableoperset:

          Set Operations
          **************

          .. flat-table::
             :header-rows: 1

             * - Purpose
               - Option4
               - Option5
             * - Set the value of the coefficient
               - Index of coefficient
               - Value of coefficient
             * - Set temperature dependency ON/OFF
               - TDEP
               - 1 -- ON   0 -- OFF
             * - Set reference temperature
               - TREF
               - Temperature value

          If ``Oper`` = SOLVE, use this value to specify the number of iterations to be used in the
          calculation of the coefficients. Valid value is any positive integer. Default = 1000.

          If you are specifying a coefficient to be held constant ( ``Oper`` = FIX):

          * 1 - Fix the specified coefficient.
          * 0 - Allow the specified coefficient to vary (disable fixing).

        * ``Option6`` - If ``Oper`` = SOLVE, specify the allowed tolerance in residual change to stop an
          iteration. Valid value is 0.0 to 1.0. Default = 0.0.

        * ``Option7`` - If ``Oper`` = SOLVE, specify the allowed tolerance in coefficient change to stop an
          iteration. Valid value is 0 to 1. Default = 0.

        Supported Material Models
        ^^^^^^^^^^^^^^^^^^^^^^^^^

        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.

        .. _TBFT_notes:

        The :ref:`tbft` command provides tools for comparing experimental material data to the program-
        provided calculated data for various nonlinear material options. Based on curve-fitting comparisons
        and error norms, choose the model to use during the solution phase of the analysis according to the
        best fit. All of the capabilities of the :ref:`tbft` command are accessible interactively via the
        standard material GUI. For more information, see `Material Curve-Fitting
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/Hlp_AM_GMCF.html>`_

        Display material model data associated with both the :ref:`tb` command and the :ref:`tbft`,FSET
        command via :ref:`tblist`,ALL,ALL.

        Material model data associated with the most recent  :ref:`tb` or :ref:`tbft`,FSET command
        overwrites previous data.

        Display material model data associated with both the :ref:`tb` command and the :ref:`tbft`,FSET
        command via :ref:`tblist`,ALL,ALL.

        The capability to fix coefficients ( ``Option4`` = FIX) applies only to nonlinear curve fitting (as
        listed in.

        The uniaxial, biaxial, and shear experimental data use engineering stress. The volumetric data uses
        true stress. See the `Material Reference
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/nonguimatprops.html>`_ for details
        about experimental data for creep and viscoelasticity.

        The hyperelastic option AML,GENR is a generalized framework where the parameters (defined prior to
        issuing :ref:`tbft` ) are imported directly from :ref:`tb` and :ref:`tbdata`. Parameter-fitting uses
        this framework for the `thermomechanical fatigue
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/Hlp_AM_TMFMCF.html#advtmvcfexamples>`_,
        `geomechanical
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/Hlp_AM_GMCF.html#gmcfexamps>`_, and
        `TNM
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/aQw8sq22dldm.html#mathypertnmrefs>`_
        material models.

        :ref:`tbft` does not support saving to ( :ref:`save` ) and resuming from ( :ref:`resume` ) the
        database file. You must therefore rerun the curve-fitting analysis and then replot ( :ref:`tbfplot`
        ).
        """
        command = "TBFT"
        return self.run(command, **kwargs)



    def uimp(self, mat: str = "", lab1: str = "", lab2: str = "", lab3: str = "", val1: str = "", val2: str = "", val3: str = "", **kwargs):
        r"""Defines constant material properties (GUI).

        Mechanical APDL Command: `UIMP <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_UIMP.html>`_

        Parameters
        ----------
        mat : str
            Material number.

        lab1 : str
            Material property labels (see :ref:`mp` for valid labels).

        lab2 : str
            Material property labels (see :ref:`mp` for valid labels).

        lab3 : str
            Material property labels (see :ref:`mp` for valid labels).

        val1 : str
            Values corresponding to three labels.

        val2 : str
            Values corresponding to three labels.

        val3 : str
            Values corresponding to three labels.

        Notes
        -----

        .. _UIMP_notes:

        :ref:`uimp` is generated by the Graphical User Interface (GUI) and appears in the log file (
        :file:`Jobname.LOG` ) if material properties are specified via the Material Properties dialog. The
        command is not intended to be typed in directly during an analysis (although it can be included in
        an input file for batch input or for use with :ref:`input` ).
        """
        command = f"UIMP,{mat},{lab1},{lab2},{lab3},{val1},{val2},{val3}"
        return self.run(command, **kwargs)


