# Copyright (C) 2016 - 2026 ANSYS, Inc. and/or its affiliates.
# Copyright (C) 2016 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
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


class AdditiveManufacturing(CommandsBase):

    def ambeam(
        self, numbeams: str = "", power: str = "", absorptivity: str = "", **kwargs
    ):
        r"""Specifies energy source parameters in an `additive manufacturing
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/add_ag/add_ag.html>`_
        analysis.

        Mechanical APDL Command: `AMBEAM <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_AMBEAM.html>`_

        **Command default:**

        One beam is used in the build process.

        If ``POWER``\ is not specified, the melting temperature will be used for
        heating steps.

        ``ABSORPTIVITY``\ is only used if ``POWER``\ is also specified.

        Parameters
        ----------
        numbeams : str
            Number of beams used in the build process. Default = 1.

        power : str
            Command argument ``POWER``. Refer to the `AMBEAM command
            documentation
            <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_AMBEAM.html>`_
            for option-specific definitions.

        absorptivity : str
            Command argument ``ABSORPTIVITY``. Refer to the `AMBEAM command
            documentation
            <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_AMBEAM.html>`_
            for option-specific definitions.

        Notes
        -----

        .. _AMBEAM_notes:

        * ``POWER`` - (Optional) Beam power for the build process.

        * ``ABSORPTIVITY`` - (Optional) Beam absorptivity value. Must be between
          0 and 1. Default = 1.

        This command is also valid in PREP7.

        For the ``POWER``\ option, if a value is specified, then ``POWER``\ \*
        ``ABSORPTIVITY``\ will be used with other process and geometric
        parameters (scan speed, hatch spacing, deposition thickness, heating
        time, superlayer volume) to define the heat generation to heat new
        element layers. The heating time for this option is specified with the
        `AMBUILD
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_AMBUILD.html>`_,TIME
        command. If a ``POWER``\ is not specified, new layers will be set to the
        melting temperature (`AMMAT
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_AMMAT.html>`_).

        For more information, including a list of the elements and commands used
        in an additive manufacturing analysis, see `Additive Simulation in the
        Mechanical Application in the Powder Bed Fusion Simulation Guide
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/add_ag/add_ag_AM_in_WB.html>`_.
        """
        command = f"AMBEAM,{numbeams},{power},{absorptivity}"
        return self.run(command, **kwargs)

    def ambuild(
        self,
        option: str = "",
        val1: str = "",
        val2: str = "",
        val3: str = "",
        val4: str = "",
        val5: str = "",
        val6: str = "",
        **kwargs,
    ):
        r"""Specifies printer parameters for the build and other options in an `additive
        manufacturing (AM)
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/add_ag/add_ag.html>`_
        analysis.

        Mechanical APDL Command: `AMBUILD <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_AMBUILD.html>`_

        **Command default:**

        None. An ``Option``\ label is required.

        Parameters
        ----------
        option : str
            Option:

            * ``LAYERT`` - ``Value1``\ - Deposition-layer thickness.

              ``Value2``\ - Mesh height.

              ``Value3``\ - Error-checking flag. Set to 0 (default) or 1.
              Setting to 1 causes the application to omit error checks for
              consistent element size and elements spanning across layers.

            * ``SCAN`` - ``Value1``\ - Hatch spacing.

              ``Value2``\ - Beam-travel speed.

            * ``TIME`` - ``Value1``\ - Inter-layer dwell time. Default =
              0.0.

              ``Value2``\ - Dwell-time multiplier for multiple parts on
              the build plate or number of repeated symmetry sectors in
              simulations with symmetry. Default = 1.0.

              ``Value3``\ - Heating step time for use with beam power
              option (`AMBEAM
              <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_AMBEAM.html>`_,,``POWER``).

              ``Value4``\ - Scan time table.

            * ``PLATE`` - ``Value1``\ - Z-coordinate of the top of the build
              plate. Default = 0.0.

            * ``CHECK`` - ``Value1``\ - If YES, create the build-summary
              file but do not solve. Default = NO.

            * ``RTHFILE`` - ``Value1``\ - Name of the thermal-results file
              (including its path). Default = ``file.rth``\ in the current
              working directory.

            * ``SSF`` - ``Value1``\ - Strain Scaling Factor. Default = 1.0.

            * ``SEQUENCE`` - Use ``Option``\ = SEQUENCE to build up a
              sequence of heating and cooling options for each layer of the
              build. When specifying multiple steps, the sequence must end
              in a dwell step scoped to ALL.

              If no sequence steps are specified, a default build sequence
              of 1 heating step and 1 cooling step per layer is assumed
              and the AMBUILD,SEQUENCE command does not need to be
              specified directly. See `"Command Specification for Option\
              = SEQUENCE"
              <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_AMBUILD.html#ambuild_sequence>`_.

        val1 : str
            Command argument ``VAL1``. Refer to the `AMBUILD command
            documentation
            <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_AMBUILD.html>`_
            for option-specific definitions.

        val2 : str
            Command argument ``VAL2``. Refer to the `AMBUILD command
            documentation
            <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_AMBUILD.html>`_
            for option-specific definitions.

        val3 : str
            Command argument ``VAL3``. Refer to the `AMBUILD command
            documentation
            <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_AMBUILD.html>`_
            for option-specific definitions.

        val4 : str
            Command argument ``VAL4``. Refer to the `AMBUILD command
            documentation
            <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_AMBUILD.html>`_
            for option-specific definitions.

        val5 : str
            Command argument ``VAL5``. Refer to the `AMBUILD command
            documentation
            <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_AMBUILD.html>`_
            for option-specific definitions.

        val6 : str
            Command argument ``VAL6``. Refer to the `AMBUILD command
            documentation
            <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_AMBUILD.html>`_
            for option-specific definitions.

        Notes
        -----

        .. _AMBUILD_notes:

        **Command Specification for Option = SEQUENCE**

        **AMBUILD, SEQUENCE, Action,Position,Item,Value4,Value5,Vlaue6**

        * ``Action`` - Action for the sequence.

          * ``ADD`` - Adds a new sequence step at the specified position.

          * ``DELETE`` - Deletes a sequence step at the specified position.

          * ``EDIT`` - Edits a sequence step item.

          * ``LIST`` - Lists current sequence.

          * ``CLEAR`` - Deletes all sequence steps.

          * ``OPTION`` - Sets sequence related options.

        * ``Position`` - Step position in the sequence.

          * ``n`` - *n*\ -th position in the sequence.

          * ``FIRST`` - First position in the sequence.

          * ``LAST`` - Last position in the sequence.

        * ``Item (with ADD/DELETE Action)`` - Item to be added or deleted in the
          sequence.

          * ``HEAT,cmName`` - Adds or deletes a heating step in the sequence.
            Can be preheating or melting, it doesn't matter.

            ``cmName``\ = component or named selection to be heated by this
            step. If blank or ALL, heat is applied to all elements in each
            layer.

          * ``DWELL,cmName`` - Adds or deletes a dwell or cooling step in the
            sequence. Used for timing calculations. A dwell step must be
            specified as the final step in the sequence.

            ``cmName``\ = component or named selection to be cooled by this
            step. If blank or ALL, cooling applies to all elements in each
            layer.

        * ``Item (with EDIT Action)`` - Item to be edited in the sequence.

          * ``TIME,Value,typeOpt,volOpt`` - Time-related options.

            * ``Value`` - Time value for the step.

            * ``typeOpt`` - Defines what the time value represents for this
              step.

              * ``TIME`` - Units in seconds. This is a basic time value
                for the step (default).

              * ``LAYER`` - Units in seconds per layer. The layer here is
                the physical layer height (not the mesh). LAYERTHICKNESS
                must be defined for this sequence step.

              * ``AREA`` - Units in seconds/(length:sup:`2`) per layer.
                This represents the time it takes per unit area on a
                physical layer. LAYERTHICKNESS must be defined for this
                sequence step.

              * ``VOLUME`` - Units in seconds/length:sup:`3`. Represents
                the time to melt a volume of material.

              * ``PARAMETERS`` - ``Value4``\ is not needed, time will be
                determined based on the specified component’s layer volume
                and the parameters defined for this step. SCANSPEED,
                LAYERTHICKNESS, and HATCHSPACING must be defined for this
                step.

            * ``volOpt`` - Sets flag identifying how time is adjusted to
              account for the difference between layer thickness and mesh
              height.

              * ``0`` - When possible, adjust to use a time based on how
                long it would take to heat the entire volume. Affects AREA
                and PARAMETERS options where the time to scan the area
                will be identified then multiplied by the number of layers
                in a superlayer (default).

              * ``1`` - Adjust time values based on the difference between
                the layer thickness and mesh height derived from an
                instantaneous heat source on semi-infinite domain (affects
                all ``typeOpt``\ options). Useful on dwell steps after
                temperature loading.

              * ``2`` - Do not adjust time based on how many layers are
                present in the element layer (affects AREA and PARAMETERS
                options only).

              Example:

              .. code-block:: text

                 AMBUILD, SEQUENCE, EDIT, 7, TIME, 0.2, AREA,1

          * ``POWER,Value`` - Power value to use with power heating option.

          * ``AREA,Value`` - Area over which the heat or timing calculations
            are applied. This allows for the representation of the total
            affected area, irrespective of whether the area is represented by
            elements or not. If unspecified, uses the active layer. This field
            only affects steps with either POWER heating or TIME options of
            AREA, VOLUME, or PARAMETERS.

          * ``TEMP,Value`` - Heating temperature for heating.

            .. note::

               **Note:**\ Only one of TEMP and POWER is required.
               Defaults to power if both are provided.

          * ``SCANSPEED,Value`` - Scan speed for the sequence step.

          * ``LAYERTHICKNESS,Value`` - Layer thickness for the sequence step.

          * ``HATCHSPACING,Value`` - Hatch spacing for the sequence step.

          * ``ABSORPTIVITY,Value`` - Power absorptivity for the sequence step.
            Default = 1.

        * ``Item (with OPTION Action)`` - Specifies options for the entire
          sequence rather than for individual positions within the sequence.
          (``Position``\ field not relevant.) Example: AMBUILD, SEQUENCE,
          OPTION,``Opt1,Opt2,Opt3``.

          * ``HEAT`` - Options for heating.

            * ``SINGLE`` - Combines the sequence workflow into one heating
              and one cooling step.

              * ``FLASH`` - Heat in a very short period of time and cool
                for a majority of the layer time. (This will get higher
                peak temperatures when using power heating.) Max applied
                temperature at a specific location will be applied when
                using temperature heating.

              * ``SCAN`` - Heat for the amount of time that it takes to go
                through all defined sequence steps except for the final
                dwell step.

                With the SINGLE,SCAN option, the cooling step will be
                the length of the final dwell step in the sequence and
                the other steps will be used to define the length of the
                heating.

            * ``STEP`` - Goes through each sequence step one by one
              (default).

        This command specifies printer parameters for the build and other
        options in an `additive manufacturing (AM)
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/add_ag/add_ag.html>`_
        analysis. When specifying printer parameters, the command is usually
        used in one of two ways: to set parameters for a single, non-sequence
        solve, or to set up a solver sequence (``Option``\ = SEQUENCE) on each
        step between adding a new layer and cooling at the end of the layer. A
        solver sequence provides flexibility for the following:

        * Specifying different preheats for different steps of the electron beam
          melting (EBM) process simulation.

        * Enabling location specific process parameters for both laser powder
          bed fusion (LPBF) and EBM process simulations.

        * Modeling multi-material builds for both LPBF and EBM process
          simulations.

        **Non-sequence options:**\

        If using a layered tetrahedral mesh, specify the mesh height (`AMBUILD
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_AMBUILD.html>`_,LAYERT,``MESHHEIGHT``).
        For Cartesian meshes, the mesh height is determined automatically.

        When setting the error-checking flag (`AMBUILD
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_AMBUILD.html>`_,LAYERT,,,1),
        verify your model and results carefully. Using the flag may lead to
        improper setup of layers or boundary conditions.

        The hatch spacing and beam travel speed are the average values used
        during the build.

        The inter-layer dwell time (`AMBUILD
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_AMBUILD.html>`_,TIME,``DWELLTIME``)
        is the span of time from the end of the deposition of a layer to the
        start of the deposition of the next layer. It includes the time required
        for recoater-blade repositioning and powder-layer spreading.

        The dwell-time multiplier (`AMBUILD
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_AMBUILD.html>`_,TIME,,``MULTIPLIER``)
        accounts for more than one part being printed on the build plate, or it
        is used to reconcile build time in simulations using symmetry. For
        multiple parts on a build plate, if the additional parts are the same
        part as the one being simulated and are arranged in the same orientation
        on the build plate, the multiplier is the total number of parts. If
        different parts exist on the plate, the multiplier is an estimate of the
        time required to build the other parts relative to the part being
        simulated. In simulations with symmetry, the dwell-time multiplier is
        the total number of repeated symmetry sectors: 2 for half symmetry, 4
        for ¼ symmetry, and so on.

        The heating step time (`AMBUILD
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_AMBUILD.html>`_,TIME,,,``HEATTIME``)
        is used along with other defined process and geometric parameters
        (power, scan speed, hatch spacing, deposition thickness, superlayer
        volume) to set the time duration and magnitude of heat generation on new
        element layers. A value of 0 (default) sets the heating time to the
        minimum time step constraint. See `General Options in the Thermal
        Analysis Guide
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_the/Hlp_G_THE3_5.html#thegenopttlm51799>`_.
        When power has been specified, you can alternatively enter SCAN in this
        field to set the heating time to the amount of time it would take to
        scan the volume of material in each element layer. With the SCAN option,
        the cooling between layers will still be the recoater time. Setting
        ``Value3``\ = SCAN may give better temperature results at the end of the
        layer and is more stable across different mesh sizes. Note that the SCAN
        option will have a different end time of the simulation because the
        layer thickness adjustment for cooling will not be used.

        The scan time (`AMBUILD
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_AMBUILD.html>`_,TIME,,,,``SCANTIME``)
        represents the amount of time it takes to scan a real layer. By default,
        the scan time will be determined from each layer’s cross-sectional area
        and other process parameters. When specified, it must be defined as a
        table with times specified on the Z primary variable. Times that are
        averaged or interpolated from the table should not include recoating
        time and will be adjusted to account for superlayer size compared to the
        deposition thickness.

        The strain scaling factor (`AMBUILD
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_AMBUILD.html>`_,SSF,``SSF``)
        scales the thermal strains in the structural portion of
        thermal-structural simulations by the specified value.

        **Sequence options:**\

        When using a stepwise build sequence (`AMBUILD
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_AMBUILD.html>`_,SEQUENCE,OPTION,HEAT,STEP,
        which is the default setting when using a sequence), the top layer of
        the build is never set to powder properties in thermal analyses as it is
        with other non-sequence AM workflows and is therefore not affected by
        the powder factor (``MATFACTOR``\ from `AMPOWDER
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_AMPOWDER.html>`_\
        command).

        If process parameters (layer thickness, hatch spacing, scan speed) are
        needed in certain build steps but were not explicitly provided in the
        sequence step, values from the `AMBUILD
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_AMBUILD.html>`_,LAYERT
        and `AMBUILD
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_AMBUILD.html>`_,SCAN
        commands are used.

        One of either TEMP or POWER is required for heating sequence steps. If
        both are provided, the power option will be used for heating.

        TIME is required for all steps. Other inputs are optional based on time
        and heating settings.

        A dwell step scoped to ALL elements must be defined as the last step in
        the sequence, for example: `AMBUILD
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_AMBUILD.html>`_,
        SEQUENCE, ADD, LAST, DWELL.

        The `AMBUILD
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_AMBUILD.html>`_,SEQUENCE
        options can be used for thermal-structural analyses in addition to just
        thermal.

        **Other general options:**\

        When specifying the name of the thermal-results file (`AMBUILD
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_AMBUILD.html>`_,RTHFILE,``RthPath``),
        omit the ``.rth``\ extension. The program also looks for the
        ``thermal.build``\ file in the same path.

        This command is also valid in PREP7.

        For more information, including a list of the elements and commands used
        in an additive manufacturing analysis, see `Additive Simulation in the
        Mechanical Application in the Powder Bed Fusion Simulation Guide
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/add_ag/add_ag_AM_in_WB.html>`_.

        **Example Usage**

        As an example, assume that typical Mechanical APDL commands, including
        normal AM commands, are used to set up the melting step. Then an 8-part
        sequence is defined for each step between adding a new layer and cooling
        at the end of the layer. The input below shows the ``Option``\ =
        SEQUENCE commands:

        .. code-block:: text

           !Sequence step 1 - heat
           AMBUILD, SEQUENCE, ADD, 1, HEAT,ALL              !Add heating step to all build elements
           AMBUILD, SEQUENCE, EDIT, 1, POWER, 450000        !Specify power value
           AMBUILD, SEQUENCE, EDIT, 1, AREA, 10000          !Specify area value that is being heated instead of calculating it from the elements
           AMBUILD, SEQUENCE, EDIT, 1, TIME, 10,            !Specify sequence time, defaults to using TIME option - value is in seconds
           AMBUILD, SEQUENCE, EDIT, 1, ABSORPTIVITY, 0.5    !Specify power absorptivity

           !Sequence step 2 - heat
           AMBUILD, SEQUENCE, ADD, 2, HEAT,SEL1             !Add heating step to component SEL1
           AMBUILD, SEQUENCE, EDIT, 2, POWER, 650000        !Specify power value
           AMBUILD, SEQUENCE, EDIT, 2, TIME, 1.5, TIME      !Specify sequence time with TIME option - value is in seconds
           AMBUILD, SEQUENCE, EDIT, 2, ABSORPTIVITY, 0.2    !Specify power absorptivity

           !Sequence step 3 - heat
           AMBUILD, SEQUENCE, ADD, 3, HEAT,SEL3             !Add heating step for component SEL3
           AMBUILD, SEQUENCE, EDIT, 3, POWER, 100000        !Specify power value
           AMBUILD, SEQUENCE, EDIT, 3, TIME, 0.5, LAYER,1   !Specify time with LAYER option - value is in seconds per deposition layer
           AMBUILD, SEQUENCE, EDIT, 3, LAYER, 0.05          !Specify layer thickness, required due to use of LAYER option
           AMBUILD, SEQUENCE, EDIT, 3, ABSORPTIVITY, 0.5    !Specify power absorptivity

           !Sequence step 4 - heat
           AMBUILD, SEQUENCE, ADD, 4, HEAT,SEL4             !Add heating step for component SEL4
           AMBUILD, SEQUENCE, EDIT, 4, POWER, 5000          !Specify power value
           AMBUILD, SEQUENCE, EDIT, 4, TIME, 0.4, AREA      !Specify time with AREA option - value is in seconds/length^2 per deposition layer
           AMBUILD, SEQUENCE, EDIT, 4, LAYER, 0.05          !Specify layer thickness, required due to use of AREA option
           AMBUILD, SEQUENCE, EDIT, 4, ABSORPTIVITY, 0.4    !Specify power absorptivity

           !Sequence step 5 - dwell/cool
           AMBUILD, SEQUENCE, ADD, 5, DWELL, ALL            !Add a dwell step for cooling (no heating BCs applied)
           AMBUILD, SEQUENCE, EDIT, 5, TIME, 1.5, VOLUME,1  !Specify time with VOLUME option - value is in seconds/length^3

           !Sequence step 6 - heat
           AMBUILD, SEQUENCE, ADD, 6, HEAT, ALL             !Add heating step for all build elements
           AMBUILD, SEQUENCE, EDIT, 6, POWER, 800000        !Specify power value
           AMBUILD, SEQUENCE, EDIT, 6, TIME, , PARAMETERS,2 !Specify time with PARAMETERS option - value not needed as it will be determined by parameters
           AMBUILD, SEQUENCE, EDIT, 6, SCAN, 1000           !Specify scan speed
           AMBUILD, SEQUENCE, EDIT, 6, LAYER, 0.05          !Specify layer thickness
           AMBUILD, SEQUENCE, EDIT, 6, HATCH, 0.1           !Specify hatch spacing
           AMBUILD, SEQUENCE, EDIT, 6, ABSORPTIVITY, 0.5    !Specify power absorptivity

           !Sequence step 7 - heat
           AMBUILD, SEQUENCE, ADD, 7, HEAT,SEL24            !Add heating step for component SEL24
           AMBUILD, SEQUENCE, EDIT, 7, POWER, 200000        !Specify power value
           AMBUILD, SEQUENCE, EDIT, 7, TIME, 2, VOLUME,1    !Specify time with VOLUME option - value is in seconds/length^3
           AMBUILD, SEQUENCE, EDIT, 7, ABSORPTIVITY, 0.5    !Specify power absorptivity

           !Sequence step 8 - dwell/cool
           AMBUILD, SEQUENCE, ADD, 8, DWELL, ALL            !Add a dwell step for cooling (no heating BCs applied)
           AMBUILD, SEQUENCE, EDIT, 8, TIME, 10             !Specify time with VOLUME option - value is in seconds/length^3

           !Specify that we want to heat in a single step for the length of the defined sequence
           AMBUILD, SEQUENCE, OPTION, HEAT, SINGLE, SCAN
        """
        command = f"AMBUILD,{option},{val1},{val2},{val3},{val4},{val5},{val6}"
        return self.run(command, **kwargs)

    def amenv(
        self,
        tgas: str = "",
        hgas: str = "",
        radopt: str = "",
        emis: str = "",
        sbc: str = "",
        **kwargs,
    ):
        r"""Specifies the build-environment thermal boundary conditions in an `additive
        manufacturing
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/add_ag/add_ag.html>`_
        analysis.

        Mechanical APDL Command: `AMENV <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_AMENV.html>`_

        **Command default:**

        No convection or radiation is included in the analysis.

        Parameters
        ----------
        tgas : str
            Temperature of the gas in the build enclosure.

        hgas : str
            Convection coefficient from the part to the enclosure gas.

        radopt : str
            Flag to enable radiation losses from the part to the enclosure.
            Allowed values: 0 (No radiation, default), 1 (Enabled).

        emis : str
            Surface emissivity value for radiation losses. This value must
            be between 0 (no radiation) and 1 (perfect blackbody emitter). A
            value is required if radiation is enabled.

        sbc : str
            Stefan-Boltzmann constant in consistent unit system. If the
            value is not provided, the solver unit system (defined with
            `/UNITS
            <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_UNITS.html>`_)
            is used to define the constant in consistent units. The value
            defaults to a number in the following table, depending on your
            unit system. The value must be supplied if using a custom
            `/UNITS
            <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_UNITS.html>`_,USER
            unit system.

            .. list-table::
               :header-rows: 2

               * - Stefan-Boltzmann constant default values
                 - -
               * - Unit system
                 - Default value
               * - MKS or SI units
                 - (see command documentation for equation)
               * - CGS units
                 - (see command documentation for equation)
               * - MPA units
                 - (see command documentation for equation)
               * - µMKS units
                 - (see command documentation for equation)
               * - BFT units
                 - (see command documentation for equation)
               * - BIN units
                 - (see command documentation for equation)

        Notes
        -----

        .. _AMENV_notes:

        If using the power-bed fusion process (`AMTYPE
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_AMTYPE.html>`_,PBF),
        the convection and radiation (if enabled) are applied only to the top of
        a newly laid layer.

        If using the directed-energy deposition process (`AMTYPE
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_AMTYPE.html>`_,DED),
        the convection and radiation (if enabled) are applied to the top of a
        newly laid layer *and*\ to the sides of the part already built.

        No convection or radiation boundary conditions are applied to the plate,
        although you can define them manually (`SF
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_SF.html>`_\
        and related commands).

        When radiation is enabled (`AMENV
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_AMENV.html>`_,
        ``TGAS``,,``RADOPT``,,), heat losses from radiation are applied only
        during the build and cooldown process steps (`AMSTEP
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_AMSTEP.html>`_,``Sequence``\
        = BUILD and COOLDOWN). Radiation heat losses are calculated with gray
        body assumptions, and the surrounding gas is assumed to be equal to
        ``TGAS``. Ansys recommends increasing the number of steps between layers
        (`AMSTEP
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_AMSTEP.html>`_\
        command) for increased accuracy of the radiation effects.

        This command is also valid in PREP7.

        For more information, including a list of the elements and commands used
        in an additive manufacturing analysis, see `Additive Simulation in the
        Mechanical Application in the Powder Bed Fusion Simulation Guide
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/add_ag/add_ag_AM_in_WB.html>`_.
        """
        command = f"AMENV,{tgas},{hgas},{radopt},{emis},{sbc}"
        return self.run(command, **kwargs)

    def ammat(self, matpart: str = "", tmelt: str = "", trelax: str = "", **kwargs):
        r"""Specifies the melting and relaxation temperatures of the build material in an `additive
        manufacturing <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/add_ag/add_ag_cal.html>`_
        analysis.

        Mechanical APDL Command: `AMMAT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_AMMAT.html>`_

        Parameters
        ----------
        matpart : str
            The material ID of the build part. Default = 1.

        tmelt : str
            Melting temperature of the build part (required).

        trelax : str
            Relaxation temperature of the build part (optional).

        Notes
        -----

        .. _AMMAT_notes:

        This command is required in an additive manufacturing analysis.

        If the part consists of multiple material IDs, you can specify any of the material IDs ( ``MATPART``
        ), as all are of the same material.

        The melting temperature ( ``TMELT`` ) is the temperature at which thermal strains begin to
        accumulate. This value is typically the liquidus-to-solidus temperature, but may be less for some
        phase-transition material (such as Ti64).

        The relaxation temperature ( ``TRELAX`` ) is the temperature at which the strains are zeroed out
        (annealed). You can use ``TRELAX`` during the build process ( :ref:`amstep`,BUILD) to account for
        stress relaxation, but it serves primarily as a simplified stress-relaxation method during the heat-
        treat step ( :ref:`amstep`,HEATTREAT). (A creep model offers a more stringent stress-relaxation
        approach if needed.)

        This command is also valid in PREP7.

        For more information, including a list of the elements and commands used in an additive
        manufacturing analysis, see `AM Process Simulation in Workbench Additive
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/add_ag/add_ag_AM_in_WB.html#add_ag_load_addon>`_
        """
        command = f"AMMAT,{matpart},{tmelt},{trelax}"
        return self.run(command, **kwargs)

    def ampowder(
        self, tpowder: str = "", hpowder: str = "", matfactor: str = "", **kwargs
    ):
        r"""Specifies the thermal conditions of the powder in an `additive manufacturing
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/add_ag/add_ag_cal.html>`_ analysis.

        Mechanical APDL Command: `AMPOWDER <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_AMPOWDER.html>`_

        Parameters
        ----------
        tpowder : str
            Temperature of the newly added powder.

        hpowder : str
            Effective convection coefficient from the part to the powder bed.

        matfactor : str
            Knockdown factor applied to the solid material properties (to obtain the powder material
            properties). Default = 0.01.

        Notes
        -----

        .. _AMPOWDER_notes:

        This command applies only to the powder-bed fusion ( :ref:`amtype`,PBF) process.

        To estimate the convection coefficient ( ``HPOWDER`` ), divide the conduction property of the powder
        (its KXX) by a characteristic conduction length into the powder (for example, ¼ of the distance from
        the part boundary to the build-chamber wall).

        The program uses the knockdown factor ( ``MATFACTOR`` ) to estimate the powder properties. The
        program applies the factor (typically 0.01) to the solid material properties to estimate the
        properties of the material in its powder state. The powder-state properties are used during the
        heating of the new layer (before its subsequent solidification and cooldown) prior to the next layer
        being applied.

        This command is also valid in PREP7.

        For more information, including a list of the elements and commands used in an additive
        manufacturing analysis, see `AM Process Simulation in Workbench Additive
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/add_ag/add_ag_AM_in_WB.html#add_ag_load_addon>`_
        """
        command = f"AMPOWDER,{tpowder},{hpowder},{matfactor}"
        return self.run(command, **kwargs)

    def amresult(self, item: str = "", key: str = "", **kwargs):
        r"""Specifies `additive manufacturing
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/add_ag/add_ag_cal.html>`_ result data
        written to a :file:`.txt` None file.

        Mechanical APDL Command: `AMRESULT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_AMRESULT.html>`_

        Parameters
        ----------
        item : str
            Result item to output to a tab-delimited :file:`.txt` file:

            * ``RINT`` - Recoater interference. Available in a structural additive manufacturing analysis only.

            * ``DTEMP`` - Layer end temperature. Available in a thermal additive manufacturing analysis only.

            * ``HSTN`` - High Strain. Available in a structural additive manufacturing analysis only.

        key : str
            Write-control key:

            * ``OFF`` - Does not write the specified result item (default).

            * ``ON`` - Writes the specified result item.

        Notes
        -----

        .. _AMRESULT_notes:

        This command controls `additive manufacturing
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/add_ag/add_ag_cal.html>`_ result data
        written to a :file:`.txt` file. Specifically, :file:`AMResults.txt` is written for recoater
        interference and layer end temperature, and :file:`AMHighStrain.txt` is written for high strains.
        The specified results are not written to the database results ( :file:`.RST` ) file.

        Result items written to the :file:`.txt` file also include node numbers and x, y, z locations.

        RINT gives the z-deformation of a layer just before a new layer is applied. This result value can
        help to determine whether an issue may occur when spreading a new layer.

        DTEMP gives the temperature of a layer just before a new layer is applied. This result value can
        help to identify regions where the build may be overheating that may result in problematic thermal
        conditions.

        HSTN gives the maximum equivalent strain experienced during the build process. This result value can
        help to identify regions at risk of cracking.
        """
        command = f"AMRESULT,{item},{key}"
        return self.run(command, **kwargs)

    def amstep(
        self,
        sequence: str = "",
        val1: str = "",
        val2: str = "",
        val3: str = "",
        val4: str = "",
        val5: str = "",
        val6: str = "",
        **kwargs,
    ):
        r"""Specifies the process-sequence steps in an additive manufacturing analysis.

        Mechanical APDL Command: `AMSTEP <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_AMSTEP.html>`_

        Parameters
        ----------
        sequence : str
            One of the following sequence options:

            * ``PREHEAT`` - ``VAL1`` - Preheat temperature of the build plate. Default = :ref:`tunif`.

            * ``BUILD`` - ``VAL1`` - Unused.

              ``VAL2`` - Ending-layer number (for performing the simulation from the first layer to the specified
              layer only). Default = last layer necessary to build the part.

              ``VAL3`` - Number of time steps taken to apply heating. Default = 2.

              ``VAL4`` - Number of time steps taken between layer additions. Default = 2.

              ``VAL5`` - Unused.

              ``VAL6`` - Bias growth factor for time steps between layer additions. Default = 1.

            * ``COOLDOWN`` - ``VAL1`` - Ambient (room) temperature (to serve as the target cooldown
              temperature).

              ``VAL2`` - Cooldown time. If 0 or unspecified, the program calculates the time based on the volume
              of the part and the convection coefficient ( :ref:`amenv` and :ref:`ampowder` ).

              ``VAL3`` - Number of time steps taken to cool down. Default = 20.

            * ``HEATTREAT`` - Perform a heat-treat (stress-relief) step.

            * ``REMOVE`` - ``VAL1`` - The number of a support to remove. Specify 0 for plate.

              ``VAL2`` - Directional cutoff step size. Only valid if ``VAL1`` = 0.

              ``VAL3`` - Directional cutoff angle specified on the X-Y plane from the +X axis. Only valid if
              ``VAL1`` = 0. Default = 0 radians.

            * ``USER`` - Perform a user-defined step.

        val1 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_AMSTEP.html>`_ for
            further information.

        val2 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_AMSTEP.html>`_ for
            further information.

        val3 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_AMSTEP.html>`_ for
            further information.

        val4 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_AMSTEP.html>`_ for
            further information.

        val5 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_AMSTEP.html>`_ for
            further information.

        val6 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_AMSTEP.html>`_ for
            further information.

        Notes
        -----

        .. _AMSTEP_notes:

        :ref:`amstep` executes a process-sequence step:

        * In a thermal analysis, ``Sequence`` = PREHEAT sets the value of the starting temperature of the
          build plate. It is ignored in a structural analysis.

        * ``Sequence`` = BUILD executes the layer-by-layer build sequence.

        * ``Sequence`` = COOLDOWN executes the cooldown step and must occur after the BUILD step.

        * ``Sequence`` = HEATTREAT performs a heat-treatment step to stress-relieve the part. Issue
          :ref:`ambuild`,RTHFILE to point to the heat-treat thermal-cycle results and specify either a
          relaxation temperature ( :ref:`ammat` ) or creep properties ( :ref:`tb` ).

        * In a structural analysis, ``Sequence`` = REMOVE removes the requested support or build plate. It
          is ignored in a thermal analysis.

        * In a structural analysis, ``Sequence`` = USER can specify an initial step (such as bolt-pretension
          the build plate) or a final step (such as a manufacturing postprocessing step).

        For ``Sequence`` = BUILD and ``Sequence`` = COOLDOWN, the number of time steps specified determines
        the accuracy of the captured temperature profile. For distortion and global residual stresses, the
        default is usually sufficient. With some materials (Al alloys in particular), the default of evenly
        spaced time steps during the build ( ``Sequence`` = BUILD) may not adequately capture the cooldown.
        The bias growth factor ( ``VAL6`` ) adjusts the time spacing to better resolve temperatures as they
        cool between layers.

        For ``Sequence`` = REMOVE, directional cutoff is activated when ``VAL1`` is set to 0 (plate), and a
        value is given for ``VAL2`` (cut step size). This option will sequentially remove the first layer of
        elements in a series of steps with each step moving the specified distance ( ``VAL2`` ). The cutoff
        steps will continue across the entire part in the direction of the specified angle ( ``VAL3`` ). If
        neither ``VAL1`` nor ``VAL2`` are specified, the entire base is removed in a single instantaneous
        step.

        When ``Sequence`` = USER, the process-sequence steps are bypassed, and the usual nonlinear solution
        is performed during this step. All applicable load and load step options are accessible. If USER is
        the initial step, all times are offset by the TIME associated with the USER step.

        This command starts a solution. You must remain in SOLUTION between sequence steps.

        This command is valid in the SOLUTION processor only.

        For more information, including a list of the elements and commands used in an additive
        manufacturing analysis, see `AM Process Simulation in Workbench Additive
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/add_ag/add_ag_AM_in_WB.html#add_ag_load_addon>`_

        **Product Restrictions**

        .. _AMSTEPprodrest:

        Ansys Mechanical Enterprise PrepPost This command is not valid.
        """
        command = f"AMSTEP,{sequence},{val1},{val2},{val3},{val4},{val5},{val6}"
        return self.run(command, **kwargs)

    def amsupports(
        self, nsupports: str = "", compname: str = "", sectarray: str = "", **kwargs
    ):
        r"""Specifies information about the supports in an `additive manufacturing
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/add_ag/add_ag_cal.html>`_ analysis.

        Mechanical APDL Command: `AMSUPPORTS <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_AMSUPPORTS.html>`_

        Parameters
        ----------
        nsupports : str
            Number of supports.

        compname : str
            Root name of the components containing the elements comprising each support. (For example, if
            ``CompName`` = "MySupport," MySupport1 represents support 1, MySupport2 represents support 2,
            etc.)

        sectarray : str
            Name of the array ( :ref:`dim` ) containing the section-reference ID for each support.

        Notes
        -----

        .. _AMSUPPORTS_notes:

        The section-reference ID array ( ``SectArray`` ) is ``NSUPPORTS`` long, with each array member
        representing a section-reference ID of a corresponding support.

        :ref:`sectype` specifies the type of support, and :ref:`secdata` specifies the geometry of the
        support.

          **Example: Specifying Support Information in an Additive Manufacturing Analysis**

          .. code:: apdl

             ! specify supports
             *dim,suppsect,,2               ! two supports
             suppsect(1)=101                ! support 1 sectID=101
             suppsect(2)=101                ! support 2 sectID=101
             !
             sectype,101,support,block      ! sectype is a block support
             secdata,.07,1                  ! wall thickness and spacing
             amsupport,2,support,suppsect   ! root name is "support" and suppsect is the
                                            !   array name containing the section IDs

        This command is also valid in PREP7.

        For more information, including a list of the elements and commands used in an additive
        manufacturing analysis, see `AM Process Simulation in Workbench Additive
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/add_ag/add_ag_AM_in_WB.html#add_ag_load_addon>`_
        """
        command = f"AMSUPPORTS,{nsupports},{compname},{sectarray}"
        return self.run(command, **kwargs)

    def amtype(self, process: str = "", **kwargs):
        r"""Specifies the printing process in an `additive manufacturing
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/add_ag/add_ag_cal.html>`_ analysis.

        Mechanical APDL Command: `AMTYPE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_AMTYPE.html>`_

        Parameters
        ----------
        process : str
            Process option:

            * ``PBF`` - Powder-bed fusion process.

            * ``DED`` - Directed-energy deposition process.

        Notes
        -----

        .. _AMTYPE_notes:

        The powder-bed fusion (PBF) process uses thermal energy from a laser or electron beam to selectively
        fuse powder in a powder bed.

        The directed-energy deposition (DED) process uses thermal energy, typically from a laser, to fuse
        materials by melting them as they are deposited.

        This command is also valid in PREP7.

        For more information, including a list of the elements and commands used in an additive
        manufacturing analysis, see `AM Process Simulation in Workbench Additive
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/add_ag/add_ag_AM_in_WB.html#add_ag_load_addon>`_
        """
        command = f"AMTYPE,{process}"
        return self.run(command, **kwargs)
