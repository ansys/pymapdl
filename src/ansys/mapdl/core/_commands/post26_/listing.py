class Listing:
    def extrem(self, nvar1="", nvar2="", ninc="", **kwargs):
        """Lists the extreme values for variables.

        APDL Command: EXTREM

        Parameters
        ----------
        nvar1, nvar2, ninc
            List extremes for variables NVAR1 through NVAR2 in steps of NINC.
            Variable range defaults to its maximum. NINC defaults to 1.

        Notes
        -----
        Lists the extreme values (and the corresponding times) for stored and
        calculated variables. Extremes for stored variables are automatically
        listed as they are stored. Only the real part of a complex number is
        used. Extreme values may also be assigned to parameters [``*GET``].
        """
        command = f"EXTREM,{nvar1},{nvar2},{ninc}"
        return self.run(command, **kwargs)

    def lines(self, n="", **kwargs):
        """Specifies the length of a printed page.

        APDL Command: LINES

        Parameters
        ----------
        n
            Number of lines per page (defaults to 20).  (Minimum allowed = 11).

        Notes
        -----
        Specifies the length of a printed page (for use in reports, etc.).
        """
        command = f"LINES,{n}"
        return self.run(command, **kwargs)

    def nprint(self, n="", **kwargs):
        """Defines which time points stored are to be listed.

        APDL Command: NPRINT

        Parameters
        ----------
        n
            List data associated with every N time (or frequency) point(s),
            beginning with the first point stored (defaults to 1).

        Notes
        -----
        Defines which time (or frequency) points within the range stored are to
        be listed.
        """
        command = f"NPRINT,{n}"
        return self.run(command, **kwargs)

    def prcplx(self, key="", **kwargs):
        """Defines the output form for complex variables.

        APDL Command: PRCPLX

        Parameters
        ----------
        key
            Output form key:

            0 - Real and imaginary parts.

            1 - Amplitude and phase angle.  Stored real and imaginary data are converted to
                amplitude and phase angle upon output.  Data remain stored as
                real and imaginary parts.

        Notes
        -----
        Defines the output form for complex variables.  Used only with harmonic
        analyses (ANTYPE,HARMIC).

        All results data are stored in the form of real and imaginary
        components and converted to amplitude and/or phase angle as specified
        via the PRCPLX command. The conversion is not  valid for derived
        results (such as principal stress/strain, equivalent stress/strain and
        USUM).
        """
        command = f"PRCPLX,{key}"
        return self.run(command, **kwargs)

    def prtime(self, tmin="", tmax="", **kwargs):
        """Defines the time range for which data are to be listed.

        APDL Command: PRTIME

        Parameters
        ----------
        tmin
            Minimum time (defaults to the first point stored).

        tmax
            Maximum time (defaults to the last point stored).

        Notes
        -----
        Defines the time (or frequency) range (within the range stored) for
        which data are to be listed.
        """
        command = f"PRTIME,{tmin},{tmax}"
        return self.run(command, **kwargs)

    def prvar(
        self,
        nvar1="",
        nvar2="",
        nvar3="",
        nvar4="",
        nvar5="",
        nvar6="",
        **kwargs,
    ):
        """Lists variables vs. time (or frequency).

        APDL Command: PRVAR

        Parameters
        ----------
        nvar1, nvar2, nvar3, . . . , nvar6
            Variables to be displayed, defined either by the reference number
            or a unique thirty-two character name. If duplicate names are used
            the command will print the data for the lowest-numbered variable
            with that name.

        Notes
        -----
        Lists variables vs. time (or frequency).  Up to six variables may be
        listed across the line. Time column output format can be changed using
        the /FORMAT command arguments Ftype, NWIDTH, and DSIGNF.
        """
        command = f"PRVAR,{nvar1},{nvar2},{nvar3},{nvar4},{nvar5},{nvar6}"
        return self.run(command, **kwargs)
