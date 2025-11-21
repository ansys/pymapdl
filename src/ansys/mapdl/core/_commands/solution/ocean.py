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


class Ocean:

    def ocdata(
        self,
        val1: str = "",
        val2: str = "",
        val3: str = "",
        val4: str = "",
        val5: str = "",
        val6: str = "",
        val7: str = "",
        val8: str = "",
        val9: str = "",
        val10: str = "",
        val11: str = "",
        val12: str = "",
        val13: str = "",
        val14: str = "",
        **kwargs,
    ):
        r"""Defines an ocean load using non-table data.

        Mechanical APDL Command: `OCDATA <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_OCDATA.html>`_

        Parameters
        ----------
        val1 : str
            Values describing the basic ocean load or a wave condition.

        val2 : str
            Values describing the basic ocean load or a wave condition.

        val3 : str
            Values describing the basic ocean load or a wave condition.

        val4 : str
            Values describing the basic ocean load or a wave condition.

        val5 : str
            Values describing the basic ocean load or a wave condition.

        val6 : str
            Values describing the basic ocean load or a wave condition.

        val7 : str
            Values describing the basic ocean load or a wave condition.

        val8 : str
            Values describing the basic ocean load or a wave condition.

        val9 : str
            Values describing the basic ocean load or a wave condition.

        val10 : str
            Values describing the basic ocean load or a wave condition.

        val11 : str
            Values describing the basic ocean load or a wave condition.

        val12 : str
            Values describing the basic ocean load or a wave condition.

        val13 : str
            Values describing the basic ocean load or a wave condition.

        val14 : str
            Values describing the basic ocean load or a wave condition.

        Notes
        -----

        .. _OCDATA_notes:

        The :ref:`ocdata` command specifies non-table data that defines the ocean load, such as the depth of
        the ocean to the mud line, the ratio of added mass over added mass for a circular cross section, or
        the wave type to apply. The terms ``VAL1``, ``VAL2``, etc. are specialized according to the input
        set required for the given ocean load.

        The program interprets the data input via the :ref:`ocdata` command within the context of the most
        recently issued :ref:`octype` command.

        Input values in the order indicated.

        This command is also valid in PREP7.

        You can define the following ocean data types:

        .. _ocdataBASIC:

        For a better understanding of how to set up a basic ocean type, see :ref:`ocdatafigbasic`.

        * ``VAL1`` - ``DEPTH`` -- The depth of the ocean (that is, the distance between the mean sea level
          and the mud line). The water surface is assumed to be level in the XY plane, with Z being positive
          upwards. This value is required and must be positive.

        * ``VAL2`` - ``MATOC`` -- The material number of the ocean. This value is required and is used to
          input the required density. It is also used to input the viscosity if the Reynolds number is used (
          :ref:`octable` ).

        * ``VAL3`` - ``KFLOOD`` -- The inside-outside fluid-interaction key:

          * 0 -- The density and pressure of fluid inside and outside of the pipe element ( ``PIPE288`` or
            ``PIPE289`` ) are independent of each other. This behavior is the default.
          * 1 -- The density and pressure of fluid inside of the pipe element ( ``PIPE288`` or ``PIPE289`` )
            are set to equal the values outside of the pipe element.

          For beam subtype CTUBE and HREC used with ``BEAM188`` or ``BEAM189`` and ocean loading, ``KFLOOD``
          is always set to 1.

        * ``VAL4`` - ``Cay`` -- The ratio of added mass of the external fluid over the mass of the fluid
          displaced by the element cross section in the y direction (normal). The added mass represents the
          mass of the external fluid (ocean water) that moves with the pipe, beam, or link element when the
          element moves in the element y direction during a dynamic analysis.

          If no value is specified, and the coefficient of inertia ``CMy`` is not specified ( :ref:`octable`
          ), both values default to 0.0.

          If no value is specified, but ``CMy``  is specified, this value defaults to ``Cay`` = ``CMy`` - 1.0.

          If this value should be 0.0, enter 0.0.

        * ``VAL5`` - ``Caz`` -- The ratio of added mass of the external fluid over the mass of a cross
          section in the element z direction (normal). The added mass represents the mass of the external
          fluid (ocean water) that moves with the pipe, beam, or link element when the element moves in the
          element z direction during a dynamic analysis.

          If no value is specified, and Cay is specified, this value defaults to Cay.

          If no value is specified, and the coefficient of inertia ``CMz`` is not specified ( :ref:`octable`
          ), both values default to 0.0.

          If no value is specified, but ``CMz``  is specified, this value defaults to ``Cay`` = ``CMz`` - 1.0.

          If this value should be 0.0, enter 0.0.

        * ``VAL6`` - ``Cb`` -- The ratio of buoyancy force used over buoyancy force based on the outside
          diameter and water density. Accept the default value in most cases. Adjust this option only when you
          must account for additional hardware (such as a control valve) attached to the pipe exterior. A non-
          default value may lead to small non-physical inconsistencies; testing is therefore recommended for
          non-default values.

          If no value is specified, this value defaults to 1.0.

          If this value should be 0.0 (useful when troubleshooting your input), enter 0.0.

        * ``VAL7`` - ``Zmsl`` -- A vertical offset from the global origin to the mean sea level. The default
        value is
          zero (meaning that the origin is located at the mean sea level).

          Two example cases for ``Zmsl`` are:

          * A structure with its origin on the sea floor ( ``Zmsl`` = ``DEPTH`` ).

          * A tidal change ( ``tc`` ) above the mean sea level ( ``Zmsl`` = ``tc``, and ``DEPTH`` becomes
            ``DEPTH`` + ``tc`` )

        * ``VAL8`` - ``Ktable`` -- The dependency of ``VAL1`` on the :ref:`octable` command:

          * Z (or 1) -- Values on the :ref:`octable` command depend on the Z levels (default).
          * RE (or 2) -- Values on the :ref:`octable` command depend on the Reynolds number.

        .. figure:: ../../../images/_commands/gOCDATA1.png

           Basic Ocean Data Type Components

        .. _ocdataWAVE:

        * ``VAL1`` - ``KWAVE`` -- The incident wave type:

          * 0 or AIRY -- Small amplitude Airy wave without modifications (default).
          * 1 or WHEELER -- Small amplitude wave with Wheeler empirical modification of depth decay function.
          * 2 or STOKES-- Stokes fifth-order wave.
          * 3 or STREAMFUNCTION -- Stream function wave.
          * 5 or RANDOM -- Random (but repeatable) combination of linear Airy wave components.
          * 6 or SHELLNEWWAVE -- Shell new wave.
          * 7 or CONSTRAINED -- Constrained new wave.
          * 8 or DIFFRACTED -- Diffracted wave (using `imported hydrodynamic data
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_adv/advOLexample.html>`_ )
          * 101+ -- API for computing particle velocities and accelerations due to waves and current:

          * 101 through 200 -- Data preprocessed (via ``KWAVE`` = 0 logic).
          * 201+ -- Data not preprocessed.
          * For more information, see the description of the `userPartVelAcc subroutine
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_prog/Hlp_P_UPFCUSTLOAD.html#upf_wvargu>`_
            in the `Programmer&#39;s Reference <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_prog/Hlp_P_UPFTOC.html>`_.

        * ``VAL2`` - ``THETA`` -- Angle of the wave direction θ from the global Cartesian X axis
          toward the global Cartesian Y axis (in degrees).

        * ``VAL3`` - ``WAVELOC`` (valid when ``KWAVE`` = 0 through 3, and 101+) -- The wave location type:

          * 0 -- Waves act on elements at their actual locations (default).
          * 1 -- Elements are assumed to be at wave peak.
          * 2 -- Upward vertical wave velocity acts on elements.
          * 3 -- Downward vertical wave velocity acts on elements.
          * 4 -- Elements are assumed to be at wave trough.

          ``SPECTRUM`` (valid when ``KWAVE`` = 5 through 7) -- The wave spectrum type:

          * 0 -- Pierson-Moskowitz (default).
          * 1 -- JONSWAP.
          * 2 -- User-defined spectrum.

        * ``VAL4`` - ``KCRC`` -- The wave-current interaction key.

          Adjustments to the current profile are available via the ``KCRC`` constant of the water motion
          table. Typically, these options are used only when the wave amplitude is large relative to the water
          depth, such that significant wave-current interaction exists.

          * 0 -- Use the current profile (as input) for wave locations below the mean water level, and the top
            current profile value for wave locations above the mean water level (default).
          * 1 -- Linearly stretch or compress the current profile from the mud line to the top of the wave.
          * 2 -- Similar to ``KCRC`` = 1, but also adjusts the current profile horizontally such that total
            flow continuity is maintained with the input profile. All current directions ``Th`` (j) must be
            identical.
          * The following option is valid only when KWAVE = 5 through 7:
          * 3 -- Nonlinear stretch or compress the current profile, as recommended in API RP 2A Codes of
            Practice for Designing and Constructing Fixed Offshore Platforms.

        * ``VAL5`` - ``KMF`` -- The MacCamy-Fuchs adjustment key, typically used only for larger-diameter
        pipes in relatively shallow water:

          * 0 -- Do not apply the adjustment (default).
          * 1 -- Apply the adjustment (valid only when ``KWAVE`` = 0 or 1).

        * ``VAL6`` - ``PRKEY`` -- The wavelength wave-printout key:

          * 0 -- No extra printout (default).
          * 1 -- Include the extra printout.
          * 2 -- Print wave component details (valid only when ``KWAVE`` = 5 through 7).

        **The following input values are valid only when** ``KWAVE`` = 5 through 7:

        * ``VAL7`` - ``APC`` -- Activate apparent period calculation when a wave is superimposed upon a
        current:

          * 0 -- Not activated (default).
          * 1 -- Activated.

        * ``VAL8`` - ``DSA`` -- Stretching depth factor:

          * Stretching is performed between a distance of ``DSA`` \* ``Hs`` below the mean water level (MWL)
            and the water surface, where ``Hs`` is the significant wave height measured from the MWL. No
            stretching occurs outside this range, or if the wave surface is below the MWL. If ``DSA`` \*
            ``Hs`` is negative, stretching is performed between that level above the MWL and the water
            surface. The default ``DSA`` value is 0.5.

        * ``VAL9`` - ``DELTA`` -- Delta stretching parameter (0.0 :math:`equation not available`   ``DELTA``
        :math:`equation not available`  1.0):

          * A value of 0.0 corresponds to Wheeler stretching under wave crests, 1.0 corresponds to linear
            extrapolation of kinematics at mean water level to crest. (Default = 0.3.) If zero is required,
            specify a small positive number (0.01 or less) instead.

        * ``VAL10`` - Wave kinematics factor or wave spreading angle:

          * ``KINE`` ( ``KWAVE`` = 5 or 7) -- Wave kinematics factor (0.0 < ``KINE``  :math:`equation not
            available`  1.0). The factor is used to account forwave spreading by modifying the horizontal wave
            velocities and accelerations.A value of 1.0 corresponds to uni-directional wave with no
            spreading.(Default = 1.0, no spreading.)
          * ``SPANGLE`` ( ``KWAVE`` = 6) -- Wave spreading angle in degrees (0.0 :math:`equation not
            available`           ``SPANGLE`` ≤ 40.0). The angle is used to compute a wave spreading factor to
            modify the horizontal wave kinematics for nearly unidirectional seas. ``SPANGLE`` = 0.0
            corresponds to no spreading. (Default = 0.0, no spreading.)

        * ``VAL11`` - Random seed value for phase angle generation, or wave crest amplitude value:

          * ``SEED`` ( ``KWAVE`` = 5) -- Initial seed for random phase angle generation. (Default = 1.)
          * ``AMPMAX`` ( ``KWAVE`` = 6) -- Maximum wave crest amplitude (distance between the mean water level
            and maximum wave crest).
          * ``AMPCONST`` ( ``KWAVE`` = 7) -- Constrained wave crest amplitude (distance between the mean water
            level and wave crest).

        **The following input values are valid only when** ``KWAVE`` = 6 or 7:

        * ``VAL12`` - ``TOFF`` -- Time offset at which the maximum wave crest will occur. (Default = 0.0.)

        * ``VAL13`` - ``ROFF`` -- Position offset along the wave direction where the maximum wave crest will
          occur. (Default = 0.0.)

        * ``VAL14`` - ``EVOLVING`` ( ``KWAVE`` = 6) -- Activate evolving wave:

          * 0 -- Not activated (default).
          * 1 -- Activated.

          ``SEED`` ( ``KWAVE`` = 7) -- Initial seed for random phase angle generation. (Default = 1.)

        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.

        When using waves in a `superelement generation run
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_substr/aKa7uq1a9ldm.html#advsupmtr2jla062999>`_
        ( :ref:`antype`,SUBSTR), consider whether you should take the ocean level into account ( ``SeOcLvL``
        on the :ref:`seopt` command).

        .. _ocdataZONE:

        An ocean zone is a local space where you can override global ocean-loading parameters. The following
        arguments specifying the ocean zone values are described in more detail under :ref:`ocdataBASIC`.

        * ``VAL1`` - ``KFLOOD`` -- The inside-outside fluid-interaction key.

        * ``VAL2`` - ``Cay`` -- The ratio of added mass of the external fluid over the mass of a cross
          section in the element y direction (normal).

        * ``VAL3`` - ``Caz`` -- The ratio of added mass of the external fluid over the mass of a cross
          section in the element z direction (normal).

        * ``VAL4`` - ``Cb`` -- The ratio of buoyancy force used over buoyancy force based on the outside
          diameter and water density.

        Ocean zone values specified via the :ref:`ocdata` command override global ocean-loading parameters.

        Arguments not specified default to the global values specified for the basic ocean type. Therefore,
        the relationship between ``Ca`` and ``CM`` values ( ``Ca`` = ``CM`` - 1.0) is not applied to ocean
        zones.

        For a pipe-type ocean zone ( :ref:`oczone`,PIP), ``KFLOOD`` is the only valid option.
        """
        command = f"OCDATA,{val1},{val2},{val3},{val4},{val5},{val6},{val7},{val8},{val9},{val10},{val11},{val12},{val13},{val14}"
        return self.run(command, **kwargs)

    def ocdelete(self, datatype: str = "", zonename: str = "", **kwargs):
        r"""Deletes a previously defined ocean load.

        Mechanical APDL Command: `OCDELETE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_OCDELETE.html>`_

        Parameters
        ----------
        datatype : str
            Ocean data type to delete. Valid values are BASIC, CURRENT, WAVE, ZONE, and ALL.

            For ``DataType`` = ALL, all defined ocean loads are deleted.

        zonename : str
            The name of the ocean zone to delete. If no name is specified, all defined ocean zones are
            deleted. Valid only when DataType = ZONE.

        Notes
        -----

        .. _OCDELETE_notes:

        The :ref:`ocdelete` command deletes previously specified ocean data from the database.

        This command is also valid in PREP7.
        """
        command = f"OCDELETE,{datatype},{zonename}"
        return self.run(command, **kwargs)

    def oclist(self, datatype: str = "", zonename: str = "", **kwargs):
        r"""Summarizes all currently defined ocean loads.

        Mechanical APDL Command: `OCLIST <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_OCLIST.html>`_

        Parameters
        ----------
        datatype : str
            Ocean data type to list. Valid values are BASIC, CURRENT, WAVE, ZONE, and ALL.

            For ``DataType`` = ALL, all defined ocean loads are listed.

        zonename : str
            The name of an ocean zone to list. If no name is specified, all defined ocean zones are listed.
            Valid only when DataType = ZONE.

        Notes
        -----

        .. _OCLIST_notes:

        The :ref:`oclist` command summarizes the ocean properties for all defined ocean loads in the current
        session.

        When this command follows the :ref:`solve` command, certain waves types also list the calculated
        wave length.

        This command is also valid in PREP7.
        """
        command = f"OCLIST,{datatype},{zonename}"
        return self.run(command, **kwargs)

    def ocread(self, fname: str = "", ext: str = "", option: str = "", **kwargs):
        r"""Reads externally defined ocean data.

        Mechanical APDL Command: `OCREAD <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_OCREAD.html>`_

        Parameters
        ----------
        fname : str
            External ocean data file name (excluding the filename extension) and directory path containing
            the file. For more information, see the :ref:`Notes section. <OCREAD_notes>`

        ext : str
            Filename extension (limited to eight characters).

        option : str
            Integer value passed to the userOceanRead subroutine (as ``iOption`` ) for user-defined waves.
            This value does not apply to the diffracted wave type.

        Notes
        -----

        .. _OCREAD_notes:

        The :ref:`ocread` command imports ocean data that has been defined externally (for example, via the
        `Hydrodynamic Diffraction System (AQWA)
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/wb_aqwa/aqwa_appendix.html>`_ ).

        The command operates on the ocean load ID specified via the most recently issued :ref:`octype`
        command. Issue a separate :ref:`ocread` command for each ocean load that you want to read into the
        program.

        ``Fname`` is limited to 248 characters, including the directory path. If ``Fname`` does not include
        a directory path, the program searches for the specified file in the current working directory. An
        unspecified ``Fname`` defaults to :file:`Jobname`.

        For the diffracted wave type ( ``KWAVE`` = 8 on the :ref:`ocdata` command), you must issue an
        :ref:`ocread` command for the ocean wave ID in order to `import the hydrodynamic data from the
        hydrodynamic analysis
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_adv/advOLexample.html>`_.

        For more information, see `Applying Ocean Loading from a Hydrodynamic Analysis
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_adv/advOLexample.html>`_

        To learn more about creating user-defined waves, see `Subroutine userPanelHydFor (Calculating Panel
        Loads Caused by Ocean Loading)
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_prog/Hlp_P_UPFCUSTLOAD.html#upf_userOceanRead>`_

        This command is also valid in PREP7.
        """
        command = f"OCREAD,{fname},{ext},,{option}"
        return self.run(command, **kwargs)

    def octable(
        self,
        val1: str = "",
        val2: str = "",
        val3: str = "",
        val4: str = "",
        val5: str = "",
        val6: str = "",
        val7: str = "",
        **kwargs,
    ):
        r"""Defines an ocean load using table data.

        Mechanical APDL Command: `OCTABLE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_OCTABLE.html>`_

        Parameters
        ----------
        val1 : str
            Values describing the basic ocean load, a current condition, or a wave condition.

        val2 : str
            Values describing the basic ocean load, a current condition, or a wave condition.

        val3 : str
            Values describing the basic ocean load, a current condition, or a wave condition.

        val4 : str
            Values describing the basic ocean load, a current condition, or a wave condition.

        val5 : str
            Values describing the basic ocean load, a current condition, or a wave condition.

        val6 : str
            Values describing the basic ocean load, a current condition, or a wave condition.

        val7 : str
            Values describing the basic ocean load, a current condition, or a wave condition.

        Notes
        -----

        .. _OCTABLE_notes:

        The :ref:`octable` specifies table data that defines the ocean load. The terms ``VAL1``, ``VAL2``,
        etc. are specialized according to the input set required for the given ocean load.

        The program interprets the data input via the :ref:`octable` command within the context of the most
        recently issued :ref:`octype` command.

        There is no limit to the number of data input.

        Input values in the order indicated.

        This command is also valid in PREP7.

        You can define the following ocean data types:

        .. _octabletypebasic:

        * Basic ocean data to provide in the value fields:
        * ``IndVar``, ``--``, ``CDy``, ``CDz``, ``CT``, ``CMy``, ``CMz``
        * where
        * ``IndVar`` = Independent variable for the table inputs. This value is dependent on the ``Ktable``
          value specified via the :ref:`ocdata` command. If ``Ktable`` = Z, enter this value in descending
          order on each :ref:`octable` command. If ``Ktable`` = RE, enter this value field in ascending
          order.
        .. flat-table ::

        * -- = Reserved.

        * ``CDy`` = Drag coefficient in the element y direction (normal).
        * ``CDz`` = Drag coefficient in the element z direction (normal). This value defaults to ``CDy``.
        * ``CT`` = Drag coefficient in the element x direction (tangential).
        * ``CMy`` = Coefficient of inertia in the element y direction. If no value is specified, and ``Cay``
          is specified, this value defaults to ``Cay`` + 1.0. If neither this value nor ``Cay`` is
          specified, both values default to 0.0.
        * ``CMz`` = Coefficent of inertia in the element z direction. If no value is specified, and ``CMy``
          is specified on the same :ref:`octable` command, this value defaults to ``CMy``. If neither this
          value nor ``CMy`` is specified, and ``Caz`` is specified, this value defaults to ``Caz`` + 1.0. If
          neither this value nor ``Caz`` is specified, both values default to 0.0.

        * Current data to provide in the value fields:
        * ``Dep``, ``W``, ``Th``, ``Te``
        * where
        * ``Dep`` = Depth of the drift current being input. Input these values in ascending order from one
          command to the next.

        * If the current is constant, only one :ref:`octable` command is necessary and ``Dep`` is not
          required.

        * For `Ocean Data Type: Wave ( OCTYPE,WAVE)
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cmd/Hlp_C_OCTABLE.html#octablewavespectinput>`_
          waves, the current profile is stretched or compressed linearly up to 10 percent.

        * The first ``Dep`` value (representing the mean sea level) must be zero. The last ``Dep`` value
          (representing the mud line) must be equal to the ``DEPTH`` value input on the :ref:`ocdata`
          command.

        * The Cartesian Z values used to locate nodes, etc. decrease as one moves from the ocean surface to
          the sea floor, but the ``Dep`` values increase. See :ref:`ocdatafigbasic`.

        * ``Dep`` is not affected by changes to ``Zmsl`` on the :ref:`ocdata` command, as that value simply
          relocates the origin.

        * ``W`` = Velocity of the drift current at this location.
        * ``Th`` = Angle of the drift current from the global Cartesian X axis toward the global Cartesian Y
          axis (in degrees) at this location.
        * ``Te`` = Temperature at this location.

        .. _OCTYPEWAVE-6E898667:

        When specifying an ocean wave type, issue the :ref:`octable` command to input either :ref:`wave
        location data or <octablewavelocinput>` `Wave Spectrum Input Data
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cmd/Hlp_C_OCTABLE.html#eq74124840-ae99-4778-8938-c48ecc8cdee7>`_
        wave spectrum data.

        .. _octablewavelocinput:

        * Wave location data to provide in the value fields (valid only when ``KWAVE`` = 0 through 3, or 8,
          on the :ref:`ocdata` command):
        * ``H``, ``T``, ``Ps``, ``L``, ``NORDER``, ``KPRCO``
        * where
        * ``H`` = Wave height (peak-to-trough).
        * ``T`` = Wave period.
        * ``Ps`` = Phase shift (in degrees)
        * ``L`` = Wavelength. An optional value used only when ``KWAVE`` = 0 or 1 (and ignored for all other
          ``KWAVE`` types).
        * ``NORDER`` = Order used by stream function wave theory ( ``KWAVE`` = 3). This value is optional.
        * ``KPRCO`` = Key for printing (1) or not printing (0 and default) the calculated dimensionless
          coefficients of the stream function wave theory ( ``KWAVE`` = 3). This value is optional.

        **Hints for Wave Location Input:**

        * The :ref:`time` command is not used, except perhaps to identify the load case.

        * The phase shift ( ``Ps`` ) determines the wave position (that is, the point at which the load is
          to be applied).

        * When using the Stokes fifth-order ( ``KWAVE`` = 2) or stream function ( ``KWAVE`` = 3) wave type,
          issue only one :ref:`octable` command.

        * The valid range of the order of the stream function ( ``NORDER`` ) is 3 through 50. If no value is
          specified, the program determines a value automatically.

        * When using the diffracted wave type ( ``KWAVE`` = 8), an :ref:`ocread` command is also required to
          read in the hydrodynamic data from the `hydrodynamic analysis
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_adv/advOLexample.html>`_.

        .. _octablewavespectinput:

        * Wave spectrum data to provide in the value fields (valid only when ``KWAVE`` = 5 through 7 on the
          :ref:`ocdata` command):
        * **SPECTRUM= 0** (Pierson-Moskowitz spectrum)
        * ``HS``, ``TP``, ``NWC``
        * where
        * ``HS`` = Significant wave height of the spectrum.
        * ``TP`` = Peak period for the spectrum.
        * ``NWC`` = Number of wave components (1 :math:`equation not available`   ``NWC``  :math:`equation
          not available`  1000) to model the spectrum. (Default= 50.)
        * **SPECTRUM= 1** (JONSWAP spectrum)
        * ``HS``, ``TP``, ``GAMMA``, ``NWC``
        * where
        * ``HS`` = Significant wave height of the spectrum.
        * ``TP`` = Peak period for the spectrum.
        * ``GAMMA`` = Peak enhancement factor for the spectrum. (Default = 3.3.)
        * ``NWC`` = Number of wave components (1 :math:`equation not available`   ``NWC``  :math:`equation
          not available`  1000) to model the spectrum. (Default= 50.)
        * **SPECTRUM= 2** (User-defined spectrum)
        * ``w``, ``s``, ``NWC``
        * ``w`` = Angular frequency (rad/s).
        * ``s`` = Spectral energy density (Length :sup:`2` / (rad/s))
        * ``NWC`` = Number of wave components (1 :math:`equation not available`   ``NWC``  :math:`equation
          not available`  1000) to model the spectrum. (Default= 50.)

        **Hints for Wave Spectrum Input:**

        * When defining a Pierson-Moskowitz or JONSWAP spectrum ( ``SPECTRUM`` = 0 or 1, respectively, on
          the :ref:`ocdata` command), issue only one :ref:`octable` command.

        * When defining a Pierson-Moskowitz or JONSWAP spectrum for Shell new wave ( ``KWAVE`` = 6 on the
          :ref:`ocdata` command), ``HS`` is calculated from the maximum wave crest amplitude ( ``AMPMAX`` on
          the :ref:`ocdata` command) if no value is specified. For further information, see `Hydrodynamic
          Loads
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_et8.html#thy_dynpresshead>`_

        * For a user-defined spectrum ( ``SPECTRUM`` = 2 on the :ref:`ocdata` command), issue an
          :ref:`octable` command for each frequency data point defining the spectrum. Specify the frequency
          data in ascending order. The number of wave components ( ``NWC`` ) is required on the first
          :ref:`octable` command only.

        An ocean zone is a local space where you can override global ocean-loading parameters.

        Ocean zone data to provide in the value fields:

        * ``Z``, --, ``CDy``, ``CDz``, ``CT``, ``CMy``, ``CMz``, ``Mbio``, ``Tbio``

        where

        * ``Z`` = Z level for the coefficients specified on this command.
        * ``--`` = Reserved.
        * ``CDy`` = Drag coefficient in the element y direction (normal).
        * ``CDz`` = Drag coefficient in the element z direction (normal). This value defaults to ``CDy``.
        * ``CT`` = Drag coefficient in the element x direction (tangential).
        * ``CMy`` = Coefficient of inertia in the element y direction.
        * ``CMz`` = Coefficient of inertia in the element z direction. This value defaults to ``CMy``.
        * ``Mbio`` = Material ID of biofouling.
        * ``Tbio`` = Thickness of biofouling.

        Ocean zone values specified via the :ref:`octable` command override global ocean-loading parameters.

        Arguments not specified default to the global values specified for the basic ocean type (
        :ref:`octype`,BASIC). Therefore, the relationship between ``Ca`` and ``CM`` values ( ``Ca`` = ``CM``
        - 1.0) is not applied to ocean zones.

        The :ref:`octable` command is not valid for a pipe-type ocean zone ( :ref:`oczone`,PIP).
        """
        command = f"OCTABLE,{val1},{val2},{val3},{val4},{val5},{val6},{val7}"
        return self.run(command, **kwargs)

    def octype(self, datatype: str = "", name: str = "", **kwargs):
        r"""Specifies the type of ocean load data to follow.

        Mechanical APDL Command: `OCTYPE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_OCTYPE.html>`_

        Parameters
        ----------
        datatype : str
            The type of ocean data to be input following this command:

            * ``BASIC`` - The basic ocean load, required for any ocean loading.

            * ``CURR`` - An optional drift current.

            * ``WAVE`` - An optional ocean wave state.

            Specify basic, current, or wave input data via the :ref:`ocdata` and :ref:`octable` commands. The
            example input fragment listed in the `Notes
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cmd/Hlp_C_SECTYPE.html#SECTYPE.prodres>`_
            Notes section shows how to use the ocean load data types.

        name : str
            An eight-character name for the ocean load. An ocean name can consist of letters and numbers,
            but cannot contain punctuation, special characters, or spaces.

        Notes
        -----

        .. _OCTYPE_notes:

        The :ref:`octype` command specifies the type of ocean load data to follow (basic, current, or wave).
        Issue this command before defining your ocean load data ( :ref:`ocdata` and :ref:`octable` ).

        Ocean loading applies only to current-technology pipe ( ``PIPE288`` and ``PIPE289`` ), surface (
        ``SURF154`` ), link ( ``LINK180`` ) and beam ( ``BEAM188`` and ``BEAM189`` ) elements.

        An ocean current or wave is accessible repeatedly. For example, it is not necessary to input an
        identical current table again just because the drag coefficients of the basic input table have
        changed.

        The following example shows how you can use the basic ( ``DataType`` = BASIC), current (
        ``DataType`` = CURR), and wave ( ``DataType`` = WAVE) ocean data types within the context of a
        simple input file fragment:

        .. code:: apdl

           Do=1.5                        ! outside diameter
           th=0.1                        ! wall thickness
           height=10                     ! wave height
           CS=2                          ! surface current speed
           Depth=100                     ! water depth
           matwat=2                      ! material number id of the ocean
           secpipe= 1                    ! section number of the pipe
           !
           sectype,secpipe,pipe,,pipetest
           secdata,Do,th,16              ! 16 cells around circumference
           !
           octype,basic
           ocdata,Depth,matwat,0,0,0,0   ! suppress added mass and buoyancy
           octable,,,.5,.5,,2            ! CD =.5, CM = 2

           octype,curr
           octable,0.0,CS                ! input free surface current speed
           octable,Depth,0.00            ! input ocean floor current speed of 0.0
           !
           octype,wave
           ocdata,2                      ! request Stokes wave type
           octable,height,8              ! wave period of 8 seconds

           slist,all                     ! lists pipe section AND
           !                                 mentions ocean loading
           oclist,all                    ! lists details of ocean loading
        """
        command = f"OCTYPE,{datatype},{name}"
        return self.run(command, **kwargs)

    def oczone(
        self,
        zonetype: str = "",
        zonename: str = "",
        compnameint: str = "",
        compnameext: str = "",
        **kwargs,
    ):
        r"""Specifies the type of ocean zone data to follow.

        Mechanical APDL Command: `OCZONE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_OCZONE.html>`_

        Parameters
        ----------
        zonetype : str
            The type of ocean zone data to be input following this command:

            * ``COMP`` - Define by a component.

            * ``ZLOC`` - Define by Z levels.

            * ``PIP`` - Associate an internal pipe or pipes with an external pipe.

        zonename : str
            The ocean zone name. If no name is specified, the program assigns one.

        compnameint : str
            For ``Zonetype`` = COMP, the required name of a component.

            For ``Zonetype`` = PIP, the required name of an internal pipe component.

        compnameext : str
            For ``Zonetype`` = PIP, the required name of an external pipe component.

        Notes
        -----

        .. _OCZONE_notes:

        The :ref:`oczone` command specifies the type of ocean zone data to follow (component, Z-level, or
        internal pipes associated with an external pipe). An ocean zone is a local space where you can
        override global ocean-loading parameters.

        Names specified for ``ZoneName``, ``CompNameInt``, and ``CompNameExt`` can consist of up to 32
        alphanumeric characters. The name cannot contain punctuation, special characters, or spaces.

        For ``Zonetype`` = COMP, the zone is defined by a component. Only the elements in the component are
        affected by the local parameters. A partial component can be defined as the zone via the Z input on
        the :ref:`octable` command.

        For ``Zonetype`` = ZLOC, the zone is defined by Z levels. Structural elements (such as ``BEAM188``,
        ``BEAM189``, ``PIPE288``, ``PIPE289``, and ``LINK180`` ) in the Z levels are included in the zone.

        For ``Zonetype`` = PIP, the zone is prepared for a special configuration of pipes. It associates an
        internal pipe or pipes with an external pipe to remove the hydrodynamic effect on the internal pipe.
        Only hydrostatic pressure is applied on the internal pipe.

        This command is also valid in PREP7.

        .. figure:: ../../../images/_commands/gcmd_oczone_comp.png

           Ocean Zone Types (Specified via ZoneType)

        Issue this command before defining your ocean load data ( :ref:`ocdata` or :ref:`octable` ). Define
        components before defining a component-type or a pipe-type zone ( :ref:`oczone`,COMP or
        :ref:`oczone`,PIP, respectively).
        """
        command = f"OCZONE,{zonetype},{zonename},{compnameint},{compnameext}"
        return self.run(command, **kwargs)
