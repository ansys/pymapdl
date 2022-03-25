class Display:
    def keep(self, key="", **kwargs):
        """Stores POST26 definitions and data during active session.

        APDL Command: KEEP

        Parameters
        ----------
        key
            State or value

            On or 1  - Allows you to exit and reenter /POST26 without losing your current time history
                       variable information. Keeps a cache of the /POST26
                       variable information including the active file name
                       (FILE),  variable definitions (NSOL, ESOL, GAPF, RFORCE,
                       SOLU, and EDREAD) and stored variable data in memory for
                       the current ANSYS session.

            Off or 0  - /POST26 variable information is deleted when you exit /POST26.

        Notes
        -----
        Your variable information is saved in memory only for the current
        active ANSYS session. It is deleted when you exit ANSYS. This
        information is also deleted when you issue /CLEAR, RESUME, SOLVE, or
        RESET.

        When you reenter /POST26 all time history variable data is available
        for use. When you issue STORE,NEW, variable definitions created by math
        operations such as ADD or PROD will not be restored. However, variables
        defined with NSOL, ESOL, GAPF, RFORCE, SOLU, and EDREAD will be
        restored. Only the last active results file name is kept in memory
        (FILE).

        Commands such as LAYERP26, SHELL, and FORCE that specify the location
        or a component of data to be stored will retain the setting at the time
        of exiting /POST26 .
        """
        command = f"KEEP,{key}"
        return self.run(command, **kwargs)

    def plcplx(self, key="", **kwargs):
        """Specifies the part of a complex variable to display.

        APDL Command: PLCPLX

        Parameters
        ----------
        key
            Complex variable part:

            0 - Amplitude.

            1 - Phase angle.

            2 - Real part.

            3 - Imaginary part.

        Notes
        -----
        Used only with harmonic analyses (ANTYPE,HARMIC).

        All results data are stored in the form of real and imaginary
        components and converted to amplitude and/or phase angle as specified
        via the PLCPLX command. The conversion is not  valid for derived
        results (such as principal stress/strain, equivalent stress/strain and
        USUM).
        """
        command = f"PLCPLX,{key}"
        return self.run(command, **kwargs)

    def pltime(self, tmin="", tmax="", **kwargs):
        """Defines the time range for which data are to be displayed.

        APDL Command: PLTIME

        Parameters
        ----------
        tmin
            Minimum time (defaults to the first point stored).

        tmax
            Maximum time (defaults to the last point stored).

        Notes
        -----
        Defines the time (or frequency) range (within the range stored) for
        which data are to be displayed.  Time is always displayed in the Z-axis
        direction for 3-D graph displays.  If XVAR = 1, time is also displayed
        in the X-axis direction and this control also sets the abscissa scale
        range.
        """
        command = f"PLTIME,{tmin},{tmax}"
        return self.run(command, **kwargs)

    def plvar(
        self,
        nvar1="",
        nvar2="",
        nvar3="",
        nvar4="",
        nvar5="",
        nvar6="",
        nvar7="",
        nvar8="",
        nvar9="",
        nvar10="",
        **kwargs,
    ):
        """Displays up to ten variables in the form of a graph.

        APDL Command: PLVAR

        Parameters
        ----------
        nvar1, nvar2, nvar3, . . . , nvar10
            Variables to be displayed, defined either by the reference number
            or a unique thirty-two character name. If duplicate names are used
            the command will plot the data for the lowest-numbered variable
            with that name.

        Notes
        -----
        Variables are displayed vs. variable N on the XVAR command. The string
        value will be a predefined, unique name. For complex variables, the
        amplitude is displayed by default [PLCPLX].  Each PLVAR command
        produces a new frame.  See the /GRTYP command for displaying multiple
        variables in a single frame with separate Y-axes.
        """
        command = f"PLVAR,{nvar1},{nvar2},{nvar3},{nvar4},{nvar5},{nvar6},{nvar7},{nvar8},{nvar9},{nvar10}"
        return self.run(command, **kwargs)

    def spread(self, value="", **kwargs):
        """Turns on a dashed tolerance curve for the subsequent curve plots.

        APDL Command: SPREAD

        Parameters
        ----------
        value
            Amount of tolerance.  For example, 0.1 is ± 10%.
        """
        return self.run("SPREAD,%s" % (str(value)), **kwargs)

    def xvar(self, n="", **kwargs):
        """Specifies the X variable to be displayed.

        APDL Command: XVAR

        Parameters
        ----------
        n
            X variable number:

            0 or 1 - Display PLVAR values vs. time (or frequency).

            n - Display PLVAR values vs. variable n (2 to NV [NUMVAR]).

            1 - Interchange time and PLVAR variable numbers with time as the curve parameter.
                PLVAR variable numbers are displayed uniformly spaced along
                X-axis from position 1 to 10.

        Notes
        -----
        Defines the X variable (displayed along the abscissa) against which the
        Y variable(s) [PLVAR] are to be displayed.
        """
        command = f"XVAR,{n}"
        return self.run(command, **kwargs)
