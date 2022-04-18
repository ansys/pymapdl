class MultiFieldSolverTimeControls:
    def mfcalc(self, fnumb="", freq="", **kwargs):
        """Specifies a calculation frequency for a field in an ANSYS Multi-field

        APDL Command: MFCALC
        solver analysis.

        Parameters
        ----------
        fnumb
            Field number set by the MFELEM command.

        freq
            Perform calculation every Nth ANSYS Multi-field solver time step.
            Defaults to 1 for every time step.

        Notes
        -----
        This command only applies to a harmonic analysis of the specified
        field. It is useful when a field contributes negligible field
        interaction within a single ANSYS Multi-field solver time step.

        This command is also valid in PREP7.

        See Multi-field Commands in the Coupled-Field Analysis Guide for a list
        of all ANSYS Multi-field solver commands and their availability for MFS
        and MFX analyses.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"MFCALC,{fnumb},{freq}"
        return self.run(command, **kwargs)

    def mfdtime(self, dtime="", dtmin="", dtmax="", carry="", **kwargs):
        """Sets time step sizes for an ANSYS Multi-field solver analysis.

        APDL Command: MFDTIME

        Parameters
        ----------
        dtime
            Multi-field time step size.  If automatic time stepping is being
            used [see Notes below], DTIME is the starting time step.

        dtmin
            Minimum time step. Defaults to DTIME.

        dtmax
            Maximum time step. Defaults to DTIME.

        carry
            Time step carryover key.

            OFF  - Use DTIME as the starting time step for the next restart run (default).

            ON  - Use the final time step from the previous run as the starting time step for the
                  next restart run.

        Notes
        -----
        This command specifies time step sizes for an ANSYS Multi-field solver
        analysis. If either DTMIN or DTMAX is not equal to DTIME, auto time-
        stepping is turned on for the multi-field loop. ANSYS will
        automatically adjust the time step size for the next multi-field step
        between DTMIN and DTMAX, based on the status of the current
        convergence, the number of target stagger iterations (specified by
        MFITER), and the actual number of iterations needed to reach
        convergence at the current time step.

        If auto time-stepping is turned off, the time step size must be evenly
        divisible into the end time (specified by MFTIME) minus the start time
        (0 for a new analysis or a restart time specified by MFRSTART).

        You can use a smaller time step within each ANSYS field analysis. This
        is called subcycling. Use the DELTIM and AUTOTS commands to subcycle a
        structural, thermal, or electromagnetic analysis.

        This command is also valid in PREP7.

        See Multi-field Commands in the Coupled-Field Analysis Guide for a list
        of all ANSYS Multi-field solver commands and their availability for MFS
        and MFX analyses.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"MFDTIME,{dtime},{dtmin},{dtmax},{carry}"
        return self.run(command, **kwargs)

    def mfoutput(self, freq="", **kwargs):
        """Specifies results file output frequency for an ANSYS

        APDL Command: MFOUTPUT
        Multi-field solver analysis.

        Parameters
        ----------
        freq
            N

            N - Write solution every Nth (and the last) time
                 step. Defaults to 1, for every time step.

            -N - Writes up to -N equally spaced results (for multifield auto time stepping).

            NONE - Suppresses writing of results for all multifield time steps.

            ALL - Writes results for every multifield time step (default).

            LAST - Writes results for only the last multifield time step.

            %array% - Where %array% is the name of an n X 1 X 1
                      dimensional array parameter defining n key
                      times, the data for the specified solution
                      results item is written at those key times. Key
                      times in the array parameter must appear in
                      ascending order. Value must be greater than or
                      equal to the ending time values for the load
                      step.

            For restart runs (see MFRSTART command), either change the
            parameter values to fall between the beginning and ending
            time values of the load step, or erase the current
            settings and reissue the command with a new array
            parameter.  - For more information about defining array
            parameters, see the ``*DIM`` command documentation.

        Notes
        -----
        A MFOUTPUT setting overrides any other output frequency setting
        (OUTRES). To select the solution items, use the OUTRES command.

        For the case of Freq = -n and Freq = %array%, the results at the time
        points which first time reaches or exceeds the targeting ouptupt time
        points will be written.

        This command is also valid in PREP7.

        See Multi-field Commands in the Coupled-Field Analysis Guide for a list
        of all ANSYS Multi-field solver commands and their availability for MFS
        and MFX analyses.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"MFOUTPUT,{freq}"
        return self.run(command, **kwargs)

    def mfrstart(self, time="", **kwargs):
        """Specifies restart status for an ANSYS Multi-field solver analysis.

        APDL Command: MFRSTART

        Parameters
        ----------
        time
            Restart time

            0  -  New analysis (Default)

            -1  - Restart from the last result set from a previous run.

            n  - Specify any positive number for the actual time point from which the ANSYS
                 Multi-field solver will restart. ANSYS checks the availability
                 of the result set and database file.

        Notes
        -----
        For MFX analyses, ANSYS always passes an actual time value to CFX (zero
        for a new analysis or a positive value for a restart run) and CFX
        verifies the consistency with the initial results file. For more
        details about ANSYS restart capabilities, please see Restarting an
        Analysis in the Basic Analysis Guide.

        See Multi-field Commands in the Coupled-Field Analysis Guide for a list
        of all ANSYS Multi-field solver commands and their availability for MFS
        and MFX analyses.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"MFRSTART,{time}"
        return self.run(command, **kwargs)

    def mftime(self, time="", **kwargs):
        """Sets end time for an ANSYS Multi-field solver analysis.

        APDL Command: MFTIME

        Parameters
        ----------
        time
            End time of an ANSYS Multi-field solver analysis. Defaults to 1.

        Notes
        -----
        A MFTIME setting overrides any other end time setting (TIME).

        This command is also valid in PREP7.

        See Multi-field Commands in the Coupled-Field Analysis Guide for a list
        of all ANSYS Multi-field solver commands and their availability for MFS
        and MFX analyses.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"MFTIME,{time}"
        return self.run(command, **kwargs)
