class Ocean:
    def ocdata(self, val1="", val2="", val3="", val14="", **kwargs):
        """Defines an ocean load using non-table data.

        APDL Command: OCDATA

        Parameters
        ----------
        val1, val2, val3, . . . , val14
            Values describing the basic ocean load or a wave condition.

        Notes
        -----
        The OCDATA command specifies non-table data that defines the ocean
        load, such as the depth of the ocean to the mud line, the ratio of
        added mass over added mass for a circular cross section, or the wave
        type to apply. The terms VAL1, VAL2, etc. are specialized according to
        the input set required for the given ocean load.

        The program interprets the data input via the OCDATA command within the
        context of the most recently issued OCTYPE command.

        Input values in the order indicated.

        This command is also valid in PREP7.

        You can define the following ocean data types:

        For a better understanding of how to set up a basic ocean type, see
        Figure: 5:: Basic Ocean Data Type Components .

        DEPTH -- The depth of the ocean (that is, the distance between the mean
        sea level and the mud line). The water surface is assumed to be level
        in the XY plane, with Z being positive upwards. This value is required
        and must be positive.

        MATOC -- The material number of the ocean. This value is required and
        is used to input the required density. It is also used to input the
        viscosity if the Reynolds number is used (OCTABLE).

        KFLOOD -- The inside-outside fluid-interaction key:

        For beam subtype CTUBE and HREC used with BEAM188 or BEAM189 and ocean
        loading, KFLOOD is always set to 1.

        Cay -- The ratio of added mass of the external fluid over the mass of
        the fluid displaced by the element cross section in the y direction
        (normal). The added mass represents the mass of the external fluid
        (ocean water) that moves with the pipe, beam, or link element when the
        element moves in the element y direction during a dynamic analysis.

        If no value is specified, and the coefficient of inertia CMy is not
        specified (OCTABLE), both values default to 0.0.

        If no value is specified, but CMy is specified, this value defaults to
        Cay = CMy - 1.0.

        If this value should be 0.0, enter 0.0.

        Caz -- The ratio of added mass of the external fluid over the mass of a
        cross section in the element z direction (normal). The added mass
        represents the mass of the external fluid (ocean water) that moves with
        the pipe, beam, or link element when the element moves in the element z
        direction during a dynamic analysis.

        If no value is specified, and Cay is specified, this value defaults to
        Cay.

        If no value is specified, and the coefficient of inertia CMz is not
        specified (OCTABLE), both values default to 0.0.

        If no value is specified, but CMz is specified, this value defaults to
        Cay = CMz - 1.0.

        If this value should be 0.0, enter 0.0.

        Cb -- The ratio of buoyancy force used over buoyancy force based on the
        outside diameter and water density. Accept the default value in most
        cases. Adjust this option only when you must account for additional
        hardware (such as a control valve) attached to the pipe exterior. A
        non-default value may lead to small non-physical inconsistencies;
        testing is therefore recommended for non-default values.

        If no value is specified, this value defaults to 1.0.

        If this value should be 0.0 (useful when troubleshooting your input),
        enter 0.0.

        Zmsl -- A vertical offset from the global origin to the mean sea level.
        The default value is zero (meaning that the origin is located at the
        mean sea level).

        Two example cases for Zmsl are:

        A structure with its origin on the sea floor (Zmsl = DEPTH).

        A tidal change (tc) above the mean sea level (Zmsl = tc, and DEPTH
        becomes DEPTH + tc)

        Ktable -- The dependency of VAL1 on the OCTABLE command:

        KWAVE -- The incident wave type:

        THETA -- Angle of the wave direction θ from the global Cartesian X axis
        toward the global Cartesian Y axis (in degrees).

        WAVELOC (valid when KWAVE = 0 through 3, and 101+) -- The wave location
        type:

        SPECTRUM (valid when KWAVE = 5 through 7) -- The wave spectrum type:

        KCRC -- The wave-current interaction key.

        Adjustments to the current profile are available via the KCRC constant
        of the water motion table. Typically, these options are used only when
        the wave amplitude is large relative to the water depth, such that
        significant wave-current interaction exists.
        """
        command = f"OCDATA,{val1},{val2},{val3},{val14}"
        return self.run(command, **kwargs)

    def ocdelete(self, datatype="", zonename="", **kwargs):
        """Deletes a previously defined ocean load.

        APDL Command: OCDELETE

        Parameters
        ----------
        datatype
            Ocean data type to delete. Valid values are BASIC, CURRENT, WAVE,
            ZONE, and ALL.

        zonename
            The name of the ocean zone to delete. If no name is specified, all
            defined ocean zones are deleted. Valid only when DataType = ZONE.

        Notes
        -----
        The OCDELETE command deletes previously specified ocean data from the
        database.

        This command is also valid in PREP7.
        """
        command = f"OCDELETE,{datatype},{zonename}"
        return self.run(command, **kwargs)

    def oclist(self, datatype="", zonename="", **kwargs):
        """Summarizes all currently defined ocean loads.

        APDL Command: OCLIST

        Parameters
        ----------
        datatype
            Ocean data type to list. Valid values are BASIC, CURRENT, WAVE,
            ZONE, and ALL.

        zonename
            The name of an ocean zone to list. If no name is specified, all
            defined ocean zones are listed. Valid only when DataType = ZONE.

        Notes
        -----
        The OCLIST command summarizes the ocean properties for all defined
        ocean loads in the current session.

        When this command follows the SOLVE command, certain waves types also
        list the calculated wave length.

        This command is also valid in PREP7.
        """
        command = f"OCLIST,{datatype},{zonename}"
        return self.run(command, **kwargs)

    def ocread(self, fname="", ext="", option="", **kwargs):
        """Reads externally defined ocean data.

        APDL Command: OCREAD

        Parameters
        ----------
        fname
            External ocean data file name (excluding the filename extension)
            and directory path containing the file. For more information, see
            the Notes section.

        ext
            Filename extension (limited to eight characters).

        --
            Reserved field.

        option
            Integer value passed to the userOceanRead subroutine (as iOption)
            for user-defined waves. This value does not apply to the diffracted
            wave type.

        Notes
        -----
        The OCREAD command imports ocean data that has been defined externally
        (for example, via the Hydrodynamic Diffraction System (AQWA)).

        The command operates on the ocean load ID specified via the most
        recently issued OCTYPE command. Issue a separate OCREAD command for
        each ocean load that you want to read into the program.

        Fname is limited to 248 characters, including the directory path. If
        Fname does not include a directory path, the program searches for the
        specified file in the current working directory. An unspecified Fname
        defaults to Jobname.

        For the diffracted wave type (KWAVE = 8 on the OCDATA command), you
        must issue an OCREAD command for the ocean wave ID in order to import
        the hydrodynamic data from the hydrodynamic analysis.

        For more information, see Applying Ocean Loading from a Hydrodynamic
        Analysis in the Advanced Analysis Guide.

        To learn more about creating user-defined waves, see Subroutine
        userPanelHydFor (Calculating Panel Loads Caused by Ocean Loading) in
        the Programmer's Reference.

        This command is also valid in PREP7.
        """
        command = f"OCREAD,{fname},{ext},{option}"
        return self.run(command, **kwargs)

    def octable(
        self,
        val1="",
        val2="",
        val3="",
        val4="",
        val5="",
        val6="",
        val7="",
        **kwargs,
    ):
        """Defines an ocean load using table data.

        APDL Command: OCTABLE

        Parameters
        ----------
        val1, val2, val3, . . . , val6
            Values describing the basic ocean load, a current condition, or a
            wave condition.

        Notes
        -----
        The OCTABLE specifies table data that defines the ocean load. The terms
        VAL1, VAL2, etc. are specialized according to the input set required
        for the given ocean load.

        The program interprets the data input via the OCTABLE command within
        the context of the most recently issued OCTYPE command.

        There is no limit to the number of data input.

        Input values in the order indicated.

        This command is also valid in PREP7.

        You can define the following ocean data types:

        If the current is constant, only one OCTABLE command is necessary and
        Dep  is not required.

        For waves, the current profile is stretched or compressed linearly up
        to 10 percent.

        The first Dep value (representing the mean sea level) must be zero. The
        last Dep value (representing the mud line) must be equal to the DEPTH
        value input on the OCDATA command.

        The Cartesian Z values used to locate nodes, etc. decrease as one moves
        from the ocean surface to the sea floor, but the Dep values increase.
        See Figure: 5:: Basic Ocean Data Type Components .

        Dep is not affected by changes to Zmsl on the OCDATA command, as that
        value simply relocates the origin.

        When specifying an ocean wave type, issue the OCTABLE command to input
        either wave location data or wave spectrum data.

        Hints for Wave Location Input:

        The TIME command is not used, except perhaps to identify the load case.

        The phase shift (Ps) determines the wave position (that is, the
        point at which the load is to be applied).

        When using the Stokes fifth-order (KWAVE = 2) or stream function (KWAVE
        = 3) wave type, issue only one OCTABLE command.

        The valid range of the order of the stream function (NORDER) is 3
        through 50. If no value is specified, the program determines a value
        automatically.

        When using the diffracted wave type (KWAVE = 8), an OCREAD command is
        also required to read in the hydrodynamic data from the hydrodynamic
        analysis.
        """
        command = f"OCTABLE,{val1},{val2},{val3},{val4},{val5},{val6},{val7}"
        return self.run(command, **kwargs)

    def octype(self, datatype="", name="", **kwargs):
        """Specifies the type of ocean load data to follow.

        APDL Command: OCTYPE

        Parameters
        ----------
        datatype
            The type of ocean data to be input following this command:

            BASIC - The basic ocean load, required for any ocean loading.

            CURR - An optional drift current.

            WAVE - An optional ocean wave state.

        name
            An eight-character name for the ocean load. An ocean name can
            consist of letters and numbers, but cannot contain punctuation,
            special characters, or spaces.

        Notes
        -----
        The OCTYPE command specifies the type of ocean load data to follow
        (basic, current, or wave). Issue this command before defining your
        ocean load data (OCDATA and OCTABLE).

        Ocean loading applies only to current-technology pipe (PIPE288 and
        PIPE289), surface (SURF154), link (LINK180) and beam (BEAM188 and
        BEAM189) elements.

        An ocean current or wave is accessible repeatedly. For example, it is
        not necessary to input an identical current table again just because
        the drag coefficients of the basic input table have changed.

        The following example shows how you can use the basic (DataType =
        BASIC), current (DataType = CURR), and wave (DataType = WAVE) ocean
        data types within the context of a simple input file fragment:
        """
        command = f"OCTYPE,{datatype},{name}"
        return self.run(command, **kwargs)

    def oczone(
        self, zonetype="", zonename="", compnameint="", compnameext="", **kwargs
    ):
        """Specifies the type of ocean zone data to follow.

        APDL Command: OCZONE

        Parameters
        ----------
        zonetype
            The type of ocean zone data to be input following this command:

            COMP - Define by a component.

            ZLOC - Define by Z levels.

            PIP - Associate an internal pipe or pipes with an external pipe.

        zonename
            The ocean zone name. If no name is specified, the program assigns
            one.

        compnameint
            For Zonetype = COMP, the required name of a component.

        compnameext
            For Zonetype = PIP, the required name of an external pipe
            component.

        Notes
        -----
        The OCZONE command specifies the type of ocean zone data to follow
        (component, Z-level, or internal pipes associated with an external
        pipe). An ocean zone is a local space where you can override global
        ocean-loading parameters.

        Names specified for ZoneName, CompNameInt, and CompNameExt can consist
        of up to 32 alphanumeric characters. The name cannot contain
        punctuation, special characters, or spaces.

        For Zonetype = COMP, the zone is defined by a component. Only the
        elements in the component are affected by the local parameters. A
        partial component can be defined as the zone via the Z input on the
        OCTABLE command.

        For Zonetype = ZLOC, the zone is defined by Z levels. Structural
        elements (such as BEAM188, BEAM189, PIPE288, PIPE289, and LINK180) in
        the Z levels are included in the zone.

        For Zonetype = PIP, the zone is prepared for a special configuration of
        pipes. It associates an internal pipe or pipes with an external pipe to
        remove the hydrodynamic effect on the internal pipe. Only hydrostatic
        pressure is applied on the internal pipe.

        This command is also valid in PREP7.

        Figure: 6:: : Ocean Zone Types (Specified via ZoneType)

        Issue this command before defining your ocean load data (OCDATA or
        OCTABLE). Define components before defining a component-type or a pipe-
        type zone (OCZONE,COMP or OCZONE,PIP, respectively).
        """
        command = f"OCZONE,{zonetype},{zonename},{compnameint},{compnameext}"
        return self.run(command, **kwargs)
