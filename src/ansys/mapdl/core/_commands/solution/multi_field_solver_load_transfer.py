class MultiFieldSolverLoadTransfer:
    def mflcomm(
        self,
        type_="",
        fname1="",
        intname1="",
        label1="",
        fname2="",
        intname2="",
        label2="",
        option="",
        **kwargs,
    ):
        """Defines a load transfer for code coupling analyses.

        APDL Command: MFLCOMM

        Parameters
        ----------
        type\_
            Set to SURF for a surface load transfer. Only surface load
            transfers are available for MFX.

        fname1
            Sets the field solver name for the server (sending) code with a
            case-sensitive character string of up to 80 characters.

        intname1
            Sets the interface name or number for the field solver of the
            server code. ANSYS interfaces are numbered and are defined by the
            SF family of commands (SF, SFA, or SFE) with the FSIN surface load
            label. CFX interfaces use names, which are set in CFX-Pre.

        label1
            Sets the surface load label for the field solver of the server code
            with a character string of up to 80 characters. ANSYS uses a
            combination of the label and option to determine what data is
            transferred (e.g., heat flows and not fluxes are sent with the
            label/option pair HFLU/CPP). ANSYS cannot serve total force or
            total force density to CFX for either formulation. CFX will send
            the data requested by the label regardless of the option. CFX
            labels that have more than one word must be enclosed in single
            quotes. Note that this field is case-sensitive; i.e., FORC will
            work, but forc will not.

        fname2
            Sets the field solver name for the client (receiving) code with a
            character string of up to 80 characters.

        intname2
            Sets the interface name or number for the field solver of the
            client code with a character string of up to 80 characters. ANSYS
            interfaces are numbered and are defined by the SF family of
            commands (SF, SFA, or SFE) with the FSIN surface load label. CFX
            interfaces use names, which are set in CFX-Pre.

        label2
            Sets the surface load label for the field solver of the client code
            with a character string of up to 80 characters. ANSYS uses a
            combination of the label and option to determine what data is
            transferred (e.g., heat flows and not fluxes are sent with the
            label-option pair HFLU/CPP). CFX will send the data requested by
            the label regardless of the option. CFX labels that have more than
            one word must be enclosed in single quotes. Note that this field is
            case-sensitive; i.e., FORC will work, but forc will not.

        option
            NONC

            NONC - Profile preserving: Sets the interface load transfer to the nonconservative
                   formulation (default for displacement and temperature). In
                   the nonconservative formulation, the force density (or heat
                   flux) is transferred across the interface, preserving the
                   density profile between the two fields.

            CPP - Conservative: Uses a local conservative formulation while preserving the
                  density profile (default for total force and wall heat flow).
                  In the conservative formulation, total force (or heat flow)
                  must be transferred across the interface from the CFX field
                  solver to the ANSYS field solver.

        Notes
        -----
        ANSYS input should always be in consistent units for its model.

        ANSYS uses a combination of the label and option to determine what data
        to transfer. CFX will send exactly the data requested by the label,
        regardless of the option. However, for the NONC option, the CFX label
        must be Total Force Density or Wall Heat Flux and for the CPP option,
        the CFX label must be Total Force or Wall Heat Flow.

        For more information on profile preserving and conservative load
        transfer, see Load Interpolation in the Coupled-Field Analysis Guide.
        Mapping Diagnostics are also available; however, if the improperly-
        mapped nodes are based on the CFX mesh, you should ignore the ANSYS-
        generated components because the CFX nodes are not present in the ANSYS
        database.

        If you are working interactively, you can choose two pre-defined
        combinations, Mechanical or Thermal, or you can choose a Custom option.
        If you choose the Mechanical load type, then the Total Force Density
        and Total Mesh Displacement data (corresponding to the ANSYS FORC and
        DISP labels, respectively) is transferred. If you choose the Thermal
        load type, then the Temperature and Wall Heat Flux data (corresponding
        to the ANSYS TEMP and HFLU labels, respectively) is transferred. If you
        choose Custom, you can select any valid combination of label and option
        as described above.

        The ANSYS Multi-field solver solver does not allow you to switch the
        load transfer direction for the same load quantity across the same
        interfaces for a restart run. For example, if Field1 sends temperature
        to and receives heat flow from Field2 across Interface 1 in a previous
        solution, then you cannot make Field1 send heat flow to and receive
        temperatures from Field2 across the same interface in a restart run,
        even if you cleared the corresponding load transfer command.

        See Multi-field Commands in the Coupled-Field Analysis Guide for a list
        of all ANSYS Multi-field solver commands and their availability for MFS
        and MFX analyses.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"MFLCOMM,{type_},{fname1},{intname1},{label1},{fname2},{intname2},{label2},{option}"
        return self.run(command, **kwargs)

    def mfsurface(self, inumb="", fnumb1="", label="", fnumb2="", **kwargs):
        """Defines a surface load transfer for an ANSYS Multi-field solver

        APDL Command: MFSURFACE
        analysis.

        Parameters
        ----------
        inumb
            Interface number for load transfer. The interface number
            corresponds to the interface number specified by the surface flag
            FSIN (SFxxcommands).

        fnumb1
            Field number of sending field.

        label
            Valid surface load labels:

        fnumb2
            Field number for receiving field.

        Notes
        -----
        This command is also valid in PREP7.

        The ANSYS Multi-field solver solver does not allow you to switch the
        load transfer direction for the same load quantity across the same
        interfaces for a restart run. For example, if Field1 sends temperature
        to and receives heat flow from Field2 across Interface 1 in a previous
        solution, then you cannot make Field1 send heat flow to and receive
        temperatures from Field2 across the same interface in a restart run,
        even if you cleared the corresponding load transfer command.

        See Multi-field Commands in the Coupled-Field Analysis Guide for a list
        of all ANSYS Multi-field solver commands and their availability for MFS
        and MFX analyses.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"MFSURFACE,{inumb},{fnumb1},{label},{fnumb2}"
        return self.run(command, **kwargs)

    def mfvolume(self, inumb="", fnumb1="", label="", fnumb2="", **kwargs):
        """Defines a volume load transfer for an ANSYS Multi-field solver

        APDL Command: MFVOLUME
        analysis.

        Parameters
        ----------
        inumb
            Interface number for load transfer. The interface number
            corresponds to the interface number specified by the volume flag
            FVIN (BFE command).

        fnumb1
            Field number of sending field.

        label
            Valid volume load labels:

        fnumb2
            Field number for receiving field.

        Notes
        -----
        This command is also valid in PREP7.

        The ANSYS Multi-field solver solver does not allow you to switch the
        load transfer direction for the same load quantity across the same
        interfaces for a restart run. For example, if Field1 sends temperature
        to and receives heat flow from Field2 across Interface 1 in a previous
        solution, then you cannot make Field1 send heat flow to and receive
        temperatures from Field2 across the same interface in a restart run,
        even if you cleared the corresponding load transfer command.

        See Multi-field Commands in the Coupled-Field Analysis Guide for a list
        of all ANSYS Multi-field solver commands and their availability for MFS
        and MFX analyses.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"MFVOLUME,{inumb},{fnumb1},{label},{fnumb2}"
        return self.run(command, **kwargs)
