class Special:
    def cvar(self, ir="", ia="", ib="", itype="", datum="", name="", **kwargs):
        """Computes covariance between two quantities.

        APDL Command: CVAR

        Parameters
        ----------
        ir
            Arbitrary reference number assigned to the resulting variable (2 to
            NV [NUMVAR]).  If this number is the same as for a previous
            variable, the previous variable will be overwritten with this
            result.

        ia, ib
            Reference numbers of the two variables to be operated on.  If only
            one, leave ``IB`` blank.

        itype
            Defines the type of response PSD to be calculated:

            * ``0,1`` - Displacement (default).

            * ``2`` - Velocity.

            * ``3`` - Acceleration.

        datum
            Defines the reference with respect to which covariance is to be
            calculated:

            * ``1`` - Absolute value.

            * ``2`` - Relative to base (default).

        name
            Thirty-two character name for identifying the variable on listings
            and displays.  Embedded blanks are compressed upon output.

        Notes
        -----
        This command computes the covariance value for the variables referenced
        by the reference numbers IA and IB.  If DATUM = 2, the variable
        referenced by IR will contain the individual modal contributions (i.e.,
        the dynamic or relative values).  If DATUM = 1, the variable referenced
        by IR will contain the modal contributions followed by the
        contributions of pseudo-static and covariance between dynamic and
        pseudo-static responses. File.PSD must be available for the
        calculations to occur.
        """
        command = f"CVAR,{ir},{ia},{ib},{itype},{datum},{name}"
        return self.run(command, **kwargs)

    def pmgtran(
        self,
        fname="",
        freq="",
        fcnam1="",
        fcnam2="",
        pcnam1="",
        pcnam2="",
        ecnam1="",
        ccnam1="",
        **kwargs,
    ):
        """Summarizes electromagnetic results from a transient analysis.

        APDL Command: PMGTRAN

        Parameters
        ----------
        fname
            File name (8 characters maximum) to which tabular data and plot
            files will be written.  Must be enclosed in single quotes when the
            command is manually typed in.  Defaults to ``MG_TRNS``.  The data file
            extension is ``.OUT`` and the plot file extension is ``.PLT``.

        freq
            Frequency of solution output.  Defaults to 1.  Every FREQth
            solution on the results file is output.

        fcnam1, fcnam2
            Names of element components for force calculation.  Must be
            enclosed in single quotes when the command is manually typed in.

        pcnam1, pcnam2
            Names of element components for power loss calculation.  Must be
            enclosed in single quotes when the command is manually typed in.

        ecnam1, ccnam1
            Names of element components for energy and total current
            calculations, respectively.  Must be enclosed in single quotes when
            the command is manually typed in.

        Notes
        -----
        ``PMGTRAN`` invokes an ANSYS macro which calculates and summarizes
        electromagnetic results from a transient analysis.  The results are
        summarized by element components and listed on the screen as well as
        written to a file (``Fname.OUT``).  Also, graph plots of results as a
        function of time are created and written to a file (``Fname.PLT``) for use
        in the ``DISPLAY`` program.

        Two components may be selected for the summary of electromagnetic
        forces (see ``FMAGSUM``), two for power loss, and one each for stored
        energy (see ``SENERGY``) and total current (see ``CURR2D``).  See the
        referenced commands for other restrictions.

        PMGTRAN is restricted to MKSA units.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"PMGTRAN,{fname},{freq},{fcnam1},{fcnam2},{pcnam1},{pcnam2},{ecnam1},{ccnam1}"
        return self.run(command, **kwargs)

    def rcyc(self, ir="", ia="", sector="", name="", **kwargs):
        """Calculates cyclic results for a mode-superposition harmonic solution.

        APDL Command: RCYC

        Parameters
        ----------
        ir
            Arbitrary reference number assigned to the resulting variable (2 to
            NV [NUMVAR]). If this number is the same as for a previous
            variable, the previous variable will be overwritten with this
            result.

        ia
            Reference number of the variable to be operated on.

        sector
            Sector number to calculate the results for.

        name
            Thirty-two character name identifying the variable on listings and
            displays. Embedded blanks are compressed for output.

        Notes
        -----
        This command calculates the harmonic response in the sector specified
        by SECTOR for the variable referenced by the reference number IA. Only
        component values for IA are valid (no principles or sums). The variable
        specified by IR will contain the harmonic solution. Jobname.RFRQ from
        the cyclic mode-superposition harmonic solve and Jobname.RST or
        Jobname.RSTP from the cyclic modal solve must be available for the
        calculations to occur. The Jobname must be the same for the cyclic
        modal solve and the cyclic mode-superposition harmonic solve.

        For SECTOR > 1, the result is in the nodal coordinate system of the
        base sector, and it is rotated to the expanded sector’s location. Refer
        to Using the /CYCEXPAND Command in the Cyclic Symmetry Analysis Guide
        for more information.

        See also Mode-Superposition Harmonic Cyclic Symmetry Analysis in the
        Cyclic Symmetry Analysis Guide.
        """
        command = f"RCYC,{ir},{ia},{sector},{name}"
        return self.run(command, **kwargs)

    def resp(
        self,
        ir="",
        lftab="",
        ldtab="",
        spectype="",
        dampratio="",
        dtime="",
        tmin="",
        tmax="",
        inputtype="",
        **kwargs,
    ):
        """Generates a response spectrum.

        APDL Command: RESP

        Parameters
        ----------
        ir
            Arbitrary reference number assigned to the response spectrum
            results (2 to NV [NUMVAR]).  If this number is the same as for a
            previously defined variable, the previously defined variable will
            be overwritten with these results.

        lftab
            Reference number of variable containing frequency table (created
            with FILLDATA or DATA command).  The frequency table defines the
            number and frequency of oscillating systems used to determine the
            response spectrum. The frequency interval need not be constant over
            the entire range. Frequencies must be input in ascending order.

        ldtab
            Reference number of variable containing the input time-history.

        spectype
            Defines the type of response spectrum to be calculated:

            * ``0`` or ``1`` - Displacement (relative to base excitation)

            * ``2`` - Velocity (relative to base excitation)

            * ``3`` - Acceleration response spectrum (absolute)

            * ``4`` - Pseudo-velocity

            * ``5`` - Pseudo-acceleration

        dampratio
            Ratio of viscous damping to critical damping (input as a decimal
            number).

        dtime
            Integration time step. This value should be equal to or greater
            than the integration time step used in the initial transient
            analysis performed to generate the input time-history (LDTAB).

        tmin, tmax
            Specifies a subset of the displacement-time history to be used in
            the response spectrum calculation.  Defaults to the full time
            range.

        inputtype
            Defines the type of the input time-history:

            * ``0`` - Displacement (default)

            * ``1`` - Acceleration

        Notes
        -----
        This command generates a response spectrum from a displacement or
        acceleration time-history and frequency data. The response spectrum is
        defined as the maximum response of single degree of freedom systems of
        varying frequency (or period) to a given input support excitation.

        A response spectrum analysis (``ANTYPE, SPECTR`` with ``SPOPT``, ``SPRS`` or ``MPRS``)
        requires a response spectrum input. This input can be determined from
        the response spectrum printout or display of this command.

        If a response spectrum is to be calculated from a given displacement
        (or acceleration) time-history, the displacement time-history may be
        input to a single one-element reduced linear transient dynamic
        (``ANTYPE,TRANS``) analysis, so that the calculated output (which should be
        the same as the input) will be properly located on the file.

        The integration time step (argument ``DTIME`` on the RESP command) and the
        damping coefficient (argument dampRatio) are constant over the
        frequency range. The number of calculations done per response spectrum
        curve is the product of the number of input solution points ``(TMAX-
        TMIN)/DTIME`` and the number of frequency points (frequencies located in
        variable LFTAB).

        Input solution points requested (using ``DTIME`` and the frequency range)
        at a time not corresponding to an actual displacement solution time on
        the file are linearly interpolated with respect to the existing points.

        For the details of the response spectrum calculation, see POST26 -
        Response Spectrum Generator (RESP).
        """
        command = f"RESP,{ir},{lftab},{ldtab},{spectype},{dampratio},{dtime},{tmin},{tmax},{inputtype}"
        return self.run(command, **kwargs)

    def rpsd(
        self,
        ir="",
        ia="",
        ib="",
        itype="",
        datum="",
        name="",
        signif="",
        **kwargs,
    ):
        """Calculates response power spectral density (PSD).

        APDL Command: RPSD

        Parameters
        ----------
        ir
            Arbitrary reference number assigned to the resulting variable (2 to
            NV [NUMVAR]).  If this number is the same as for a previous
            variable, the previous variable will be overwritten with this
            result.

        ia, ib
            Reference numbers of the two variables to be operated on.  If only
            one, leave ``IB`` blank.

        itype
            Defines the type of response PSD to be calculated:

            * ``0,1`` - Displacement (default).

            * ``2`` - Velocity.

            * ``3`` - Acceleration.

        datum
            Defines the reference with respect to which response PSD is to be
            calculated:

            * ``1`` - Absolute value.

            * ``2`` - Relative to base (default).

        name
            Thirty-two character name identifying variable on listings and
            displays.  Embedded blanks are compressed for output.

        signif
            Combine only those modes whose significance level exceeds the
            ``SIGNIF`` threshold. The significance level is defined as the modal
            covariance matrix term divided by the maximum of all the modal
            covariance matrix terms. Any term whose significance level is less
            than ``SIGNIF`` is considered insignificant and does not contribute to
            the response. All modes are taken into account by default (``SIGNIF =
            0.0``).

        Notes
        -----
        This command calculates response power spectral density (PSD) for the
        variables referenced by the reference numbers IA and IB.  The variable
        referred by IR will contain the response PSD.  You must issue the
        STORE,PSD command first; File.PSD must be available for the
        calculations to occur.

        See POST26 - Response Power Spectral Density in the Mechanical APDL
        Theory Reference for more information on these equations.
        """
        command = f"RPSD,{ir},{ia},{ib},{itype},{datum},{name},{signif}"
        return self.run(command, **kwargs)

    def smooth(
        self,
        vect1="",
        vect2="",
        datap="",
        fitpt="",
        vect3="",
        vect4="",
        disp="",
        **kwargs,
    ):
        """Allows smoothing of noisy data and provides a graphical representation

        APDL Command: SMOOTH
        of the data.

        Parameters
        ----------
        vect1
            Name of the first vector that contains the noisy data set (i.e.,
            independent variable). You must create and fill this vector before
            issuing ``SMOOTH``.

        vect2
            Name of the second vector that contains the dependent set of data.
            Must be the same length as the first vector. You must create and
            fill this vector before issuing ``SMOOTH``.

        datap
            Number of data points to be fitted, starting from the beginning of
            the vector. If left blank, the entire vector will be fitted. The
            maximum number of data points is 100,000 (or greater, depending on
            the memory of the computer).

        fitpt
            Order of the fitting curve that will be used as a smooth
            representation of the data. This number should be less than or
            equal to the number of the data points. Default (blank) is one-half
            the number of data points. Maximum number of smoothed data fitting
            order is the number of data points up to 50.  Depending on this
            number, the smoothed curve will be one of the following:

            * ``1`` - Curve is the absolute average of all of the data points.

            * ``2`` - Curve is the least square average of all of the data points.

            * ``3`` or more - Curve is a polynomial of the order (n-1), where n is the number of data fitting
                        order points.

        vect3
            Name of the vector that contains the smoothed data of the
            independent variable. This vector should have a length equal to or
            greater than the number of smoothed data points. In batch (command)
            mode, you must create this vector before issuing the ``SMOOTH``
            command. In interactive mode, the GUI automatically creates this
            vector (if it does not exist). If you do not specify a vector name,
            the GUI will name the vector smth_ind.

        vect4
            Name of the vector that contains the smoothed data of the dependent
            variable.  This vector must be the same length as Vect3.  In batch
            (command) mode, you must create this vector before issuing the
            ``SMOOTH`` command. In interactive mode, the GUI automatically creates
            this vector (if it does not exist). If you do not specify a vector
            name, the GUI will name the vector smth_dep.

        disp
            Specifies how you want to display data. No default; you must
            specify an option.

            * ``1`` - Unsmoothed data only

            * ``2`` - Smoothed data only

            * ``3`` - Both smoothed and unsmoothed data

        Notes
        -----
        You can control the attributes of the graph using standard ANSYS
        controls (``/GRID``, ``/GTHK``, ``/COLOR``, etc.). If working interactively, these
        controls appear in this dialog box for convenience, as well as in their
        standard dialog boxes. You must always create Vect1 and Vect2 (using
        ``*DIM``) and fill these vectors before smoothing the data. If you're
        working interactively, ANSYS automatically creates Vect3 and Vect4, but
        if you're working in batch (command) mode, you must create Vect3 and
        Vect4 (using ``*DIM``) before issuing SMOOTH.  Vect3 and Vect4 are then
        filled automatically by ANSYS.  In addition, ANSYS creates an
        additional TABLE type array that contains the smoothed array and the
        unsmoothed data to allow for plotting later with ``*VPLOT``.  Column 1 in
        this table corresponds to Vect1, column 2 to Vect2, and column 3 to
        Vect4.  This array is named Vect3_SMOOTH, up to a limit of 32
        characters. For example, if the array name is X1, the table name is
        X1_SMOOTH.

        This command is also valid in PREP7 and SOLUTION.
        """
        command = f"SMOOTH,{vect1},{vect2},{datap},{fitpt},{vect3},{vect4},{disp}"
        return self.run(command, **kwargs)

    def vget(self, par="", ir="", tstrt="", kcplx="", **kwargs):
        """Moves a variable into an array parameter vector.

        APDL Command: VGET

        Parameters
        ----------
        par
            Array parameter vector in the operation.

        ir
            Reference number of the variable (1 to NV [NUMVAR]).

        tstrt
            Time (or frequency) corresponding to start of IR data.  If between
            values, the nearer value is used.

        kcplx
            Complex number key:

            * ``0`` - Use the real part of the IR data.

            * ``1`` - Use the imaginary part of the IR data.

        Notes
        -----
        Moves a variable into an array parameter vector.  The starting array
        element number must be defined.  For example, ``VGET,A(1),2`` moves
        variable 2 (starting at time 0.0) to array parameter A.  Looping
        continues from array element ``A(1)`` with the index number incremented by
        one until the variable is filled.  The number of loops may be
        controlled with the ``*VLEN`` command (except that loop skipping (``NINC``) is
        not allowed).  For multi-dimensioned array parameters, only the first
        (row) subscript is incremented.
        """
        command = f"VGET,{par},{ir},{tstrt},{kcplx}"
        return self.run(command, **kwargs)

    def vput(self, par="", ir="", tstrt="", kcplx="", name="", **kwargs):
        """Moves an array parameter vector into a variable.

        APDL Command: VPUT

        Parameters
        ----------
        par
            Array parameter vector in the operation.

        ir
            Arbitrary reference number assigned to this variable (1 to NV
            [NUMVAR]).  Overwrites any existing results for this variable.

        tstrt
            Time (or frequency) corresponding to start of IR data.  If between
            values, the nearer value is used.

        kcplx
            Complex number key:

            * ``0`` - Use the real part of the IR data.

            * ``1`` - Use the imaginary part of the IR data.

        name
            Thirty-two character name identifying the item on printouts and
            displays. Defaults to the label formed by concatenating VPUT with
            the reference number IR.

        Notes
        -----
        At least one variable should be defined (``NSOL``, ``ESOL``, ``RFORCE``, etc.)
        before using this command.  The starting array element number must be
        defined.  For example,`` VPUT,A(1),2`` moves array parameter A to variable
        2 starting at time 0.0.  Looping continues from array element ``A(1)`` with
        the index number incremented by one until the variable is filled.
        Unfilled variable locations are assigned a zero value.  The number of
        loops may be controlled with the ``*VLEN`` command (except that loop
        skipping (``NINC``) is not allowed).  For multi-dimensioned array
        parameters, only the first (row) subscript is incremented.
        """
        command = f"VPUT,{par},{ir},{tstrt},{kcplx},{name}"
        return self.run(command, **kwargs)
