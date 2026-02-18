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


class AdditiveManufacturing:

    def ambeam(self, numbeams: str = "", **kwargs):
        r"""For multiple-beam printers, specifies the number of beams in an `additive manufacturing
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/add_ag/add_ag_cal.html>`_ analysis.

        Mechanical APDL Command: `AMBEAM <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_AMBEAM.html>`_

        Parameters
        ----------
        numbeams : str
            Number of beams used in the build process. Default = 1.

        Notes
        -----

        .. _AMBEAM_notes:

        This command is also valid in PREP7.

        For more information, including a list of the elements and commands used in an additive
        manufacturing analysis, see `AM Process Simulation in Workbench Additive
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/add_ag/add_ag_AM_in_WB.html#add_ag_load_addon>`_
        """
        command = f"AMBEAM,{numbeams}"
        return self.run(command, **kwargs)

    def ambuild(
        self,
        option: str = "",
        val1: str = "",
        val2: str = "",
        val3: str = "",
        val4: str = "",
        **kwargs,
    ):
        r"""Specifies printer parameters for the build and other options in an `additive manufacturing
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/add_ag/add_ag_cal.html>`_ analysis.

        Mechanical APDL Command: `AMBUILD <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_AMBUILD.html>`_

        Parameters
        ----------
        option : str
            Option:

            * ``LAYERT`` - ``VAL1`` - Deposition-layer thickness.

              ``VAL2`` - Mesh height.

              ``VAL3`` - Error-checking flag. Set to 0 (default) or 1. Setting to 1 causes the application to omit
              error checks for consistent element size and elements spanning across layers.

            * ``SCAN`` - ``VAL1`` - Hatch spacing.

              ``VAL2`` - Beam-travel speed.

            * ``TIME`` - ``VAL1`` - Inter-layer dwell time. Default = 0.0.

              ``VAL2`` - Dwell-time multiplier for multiple parts on the build plate or number of repeated
              symmetry sectors in simulations with symmetry. Default = 1.0.

              ``VAL3`` - Unused field.

              ``VAL4`` - Scan time table.

            * ``PLATE`` - ``VAL1`` - Z-coordinate of the top of the build plate. Default = 0.0.

            * ``CHECK`` - ``VAL1`` - If YES, create the build-summary file but do not solve. Default = NO.

            * ``RTHFILE`` - ``VAL1`` - Name of the thermal-results file (including its path). Default =
              :file:`file.rth` in the current working directory.

            * ``SSF`` - ``VAL1`` - Strain Scaling Factor. Default = 1.0.

        val1 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_AMBUILD.html>`_ for
            further information.

        val2 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_AMBUILD.html>`_ for
            further information.

        val3 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_AMBUILD.html>`_ for
            further information.

        val4 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_AMBUILD.html>`_ for
            further information.

        Notes
        -----

        .. _AMBUILD_notes:

        If using a layered tetrahedral mesh, specify the mesh height (LAYERT, ``VAL2`` ). For Cartesian
        meshes, the mesh height is determined automatically.

        When setting the error-checking flag (LAYERT,,,1), verify your model and results carefully. Using
        the flag may lead to improper setup of layers or boundary conditions.

        The hatch spacing and beam travel speed are the average values used during the build.

        The inter-layer dwell time (TIME, ``VAL1`` ) is the span of time from the end of the deposition of a
        layer to the start of the deposition of the next layer. It includes the time required for recoater-
        blade repositioning and powder-layer spreading.

        The dwell-time multiplier (TIME, ``VAL2`` ) accounts for more than one part being printed on the
        build plate, or it is used to reconcile build time in simulations using symmetry. For multiple parts
        on a build plate, if the additional parts are the same part as the one being simulated and are
        arranged in the same orientation on the build plate, the multiplier is the total number of parts. If
        different parts exist on the plate, the multiplier is an estimate of the time required to build the
        other parts relative to the part being simulated. In simulations with symmetry, the dwell-time
        multiplier is the total number of repeated symmetry sectors: 2 for half symmetry, 4 for ¼ symmetry,
        and so on.

        The scan time (TIME, ``VAL4`` ) represents the amount of time it takes to scan a real layer. By
        default, the scan time will be determined from each layer``s cross-sectional area and other process
        parameters. When specified, it must be defined as a table with times specified on the Z primary
        variable. Times that are averaged or interpolated from the table should not include recoating time
        and will be adjusted to account for superlayer size compared to the deposition thickness.

        When specifying the name of the thermal-results file (RTHFILE, ``VAL1`` ), omit the :file:`.rth`
        extension. The program also looks for the :file:`thermal.build` file in the same path.

        The strain scaling factor (SSF, ``VAL1`` ) scales the thermal strains in the structural portion of
        thermal-structural simulations by the specified value.

        This command is also valid in PREP7.

        For more information, including a list of the elements and commands used in an additive
        manufacturing analysis, see `AM Process Simulation in Workbench Additive
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/add_ag/add_ag_AM_in_WB.html#add_ag_load_addon>`_
        """
        command = f"AMBUILD,{option},{val1},{val2},{val3},{val4}"
        return self.run(command, **kwargs)

    def amenv(self, tgas: str = "", hgas: str = "", **kwargs):
        r"""Specifies the build-environment thermal boundary conditions in an `additive manufacturing
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/add_ag/add_ag_cal.html>`_ analysis.

        Mechanical APDL Command: `AMENV <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_AMENV.html>`_

        Parameters
        ----------
        tgas : str
            Temperature of the gas in the build enclosure.

        hgas : str
            Convection coefficient from the part to the enclosure gas.

        Notes
        -----

        .. _AMENV_notes:

        If using the power-bed fusion process ( :ref:`amtype`,PBF), the convection is applied only to the
        top of a newly laid layer.

        If using the directed-energy deposition process ( :ref:`amtype`,DED), the convection is applied to
        the top of a newly laid layer and to the sides of the part already built.

        No convection boundary conditions are applied to the plate, although you can define them manually (
        :ref:`sf` and related commands).

        This command is also valid in PREP7.

        For more information, including a list of the elements and commands used in an additive
        manufacturing analysis, see `AM Process Simulation in Workbench Additive
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/add_ag/add_ag_AM_in_WB.html#add_ag_load_addon>`_
        """
        command = f"AMENV,{tgas},{hgas}"
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
