class SpectrumOptions:
    def addam(self, af="", aa="", ab="", ac="", ad="", amin="", **kwargs):
        """Specifies the acceleration spectrum computation constants for the

        APDL Command: ADDAM
        analysis of shock resistance of shipboard structures.

        Parameters
        ----------
        af
            Direction-dependent acceleration coefficient for elastic or
            elastic-plastic analysis option (default = 0).

        aa, ab, ac, ad
            Coefficients for the DDAM acceleration spectrum equations. Default
            for these coefficients is zero.

        amin
            The minimum acceleration value in inch/sec2.  It defaults to 2316
            inch/sec2 which equals 6g, where g is acceleration due to gravity
            (g = 386 inch/sec2).

        Notes
        -----
        This command specifies acceleration coefficients to analyze shock
        resistance of shipboard equipment.  These coefficients are used to
        compute mode coefficients according to the equations given in Dynamic
        Design Analysis Method in the Mechanical APDL Theory Reference.  The
        form of these equations is based on the Naval NRL Dynamic Design
        Analysis Method.  This command, along with the VDDAM and SED commands,
        is used with the spectrum (ANTYPE,SPECTR) analysis as a special purpose
        alternative to the SV, FREQ, and SVTYP commands.  The mass and length
        units of the model must be in pounds and inches, respectively.

        DDASPEC may alternatively be used to calculate spectrum coefficients.

        This command is also valid in PREP7.
        """
        command = f"ADDAM,{af},{aa},{ab},{ac},{ad},{amin}"
        return self.run(command, **kwargs)

    def coval(
        self,
        tblno1="",
        tblno2="",
        sv1="",
        sv2="",
        sv3="",
        sv4="",
        sv5="",
        sv6="",
        sv7="",
        **kwargs,
    ):
        """Defines PSD cospectral values.

        APDL Command: COVAL

        Parameters
        ----------
        tblno1
            First input PSD table number associated with this spectrum.

        tblno2
            Second input PSD table number associated with this spectrum.

        sv1, sv2, sv3, . . . , sv7
            PSD cospectral values corresponding to the frequency points
            [PSDFRQ].

        Notes
        -----
        Defines PSD cospectral values to be associated with the previously
        defined frequency points.  Two table references are required since
        values are off-diagonal terms.  Unlike autospectra [PSDVAL], the
        cospectra can be positive or negative.  The cospectral curve segment
        where there is a sign change is interpolated linearly (the rest of the
        curve segments use log-log interpolation).  For better accuracy, choose
        as small a curve segment as possible wherever a sign change occurs.

        Repeat COVAL command using the same table numbers for additional
        points.  This command is valid for SPOPT,PSD only.

        This command is also valid in PREP7.
        """
        command = f"COVAL,{tblno1},{tblno2},{sv1},{sv2},{sv3},{sv4},{sv5},{sv6},{sv7}"
        return self.run(command, **kwargs)

    def cqc(self, signif="", label="", forcetype="", **kwargs):
        """Specifies the complete quadratic mode combination method.

        APDL Command: CQC

        Parameters
        ----------
        signif
            Combine only those modes whose significance level exceeds the
            SIGNIF threshold.  For single point, multipoint, or DDAM response
            (SPOPT,SPRS, MPRS or DDAM), the significance level of a mode is
            defined as the mode coefficient of the mode, divided by the maximum
            mode coefficient of all modes.  Any mode whose significance level
            is less than SIGNIF is considered insignificant and is not
            contributed to the mode combinations.  The higher the SIGNIF
            threshold, the fewer the number of modes combined.  SIGNIF defaults
            to 0.001.  If SIGNIF is specified as 0.0, it is taken as 0.0.
            (This mode combination method is not valid for SPOPT,PSD.)

        label
            Label identifying the combined mode solution output.

            DISP - Displacement solution (default).  Displacements, stresses, forces, etc., are
                   available.

            VELO - Velocity solution.  Velocities, "stress velocities," "force velocities," etc.,
                   are available.

            ACEL - Acceleration solution.  Accelerations, "stress accelerations," "force
                   accelerations," etc., are available.

        forcetype
            Label identifying the forces to be combined:

            STATIC - Combine the modal static forces (default).

            TOTAL - Combine the modal static plus inertial forces.

        Notes
        -----
        Damping is required for this mode combination method.  The CQC command
        is also valid for PREP7.
        """
        command = f"CQC,{signif},{label},{forcetype}"
        return self.run(command, **kwargs)

    def ddaspec(self, keyref="", shptyp="", mountloc="", deftyp="", amin="", **kwargs):
        """APDL Command: DDASPEC

        Specifies the shock spectrum computation constants for DDAM analysis.

        Parameters
        ----------
        keyref
            Key for reference catalog:

            1 - The spectrum computation constants are based on NRL-1396 (default). For more
                information, see Dynamic Design Analysis Method in the
                Mechanical APDL Theory Reference

        shptyp
            Select the ship type:

            SUBM - Submarine

            SURF - Surface ship

        mountloc
            Select the mounting location:

            HULL - Hull mounting location. These structures are mounted directly to basic hull
                   structures like frames, structural bulkheads below the water
                   line, and shell plating above the water line.

            DECK - Deck mounting location. These structures are mounted directly to decks, non-
                   structural bulkheads, or to structural bulkheads above the
                   water line.

            SHEL - Shell plating mounting location. These structures are mounted directly to shell
                   plating below the water line without intervening
                   foundations.

        deftyp
            Select the deformation type:

            ELAS - Elastic deformation (default)

            PLAS - Elastic-plastic deformation

        amin
            Minimum acceleration value in inch/sec2. It defaults to 2316
            inch/sec2 which equals 6g, where g is the acceleration due to
            gravity (g = 386 in/sec2).

        Notes
        -----
        The excitation direction is required to calculate the spectrum
        coefficients. Issue the SED command before issuing DDASPEC.

        ADDAM and VDDAM may alternatively be used to calculate spectrum
        coefficients.

        This command is also valid in PREP7.
        """
        command = f"DDASPEC,{keyref},{shptyp},{mountloc},{deftyp},{amin}"
        return self.run(command, **kwargs)

    def dsum(self, signif="", label="", td="", forcetype="", **kwargs):
        """Specifies the double sum mode combination method.

        APDL Command: DSUM

        Parameters
        ----------
        signif
            Combine only those modes whose significance level exceeds the
            SIGNIF threshold.  For single point, multipoint, or DDAM response
            (SPOPT, SPRS, MPRS, or DDAM), the significance level of a mode is
            defined as the mode coefficient of the mode, divided by the maximum
            mode coefficient of all modes.  Any mode whose significance level
            is less than SIGNIF is considered insignificant and is not
            contributed to the mode combinations.  The higher the SIGNIF
            threshold, the fewer the number of modes combined. SIGNIF defaults
            to 0.001.  If SIGNIF is specified as 0.0, it is taken as 0.0.
            (This mode combination method is not valid for SPOPT, PSD.)

        label
            Label identifying the combined mode solution output.

            DISP - Displacement solution (default).  Displacements, stresses, forces, etc., are
                   available.

            VELO - Velocity solution.  Velocities, "stress velocities," "force velocities," etc.,
                   are available.

            ACEL - Acceleration solution.  Accelerations, "stress accelerations," "force
                   accelerations," etc., are available.

        td
            Time duration for earthquake or shock spectrum.  TD defaults to 10.

        forcetype
            Label identifying the forces to be combined:

            STATIC - Combine the modal static forces (default).

            TOTAL - Combine the modal static plus inertial forces.

        Notes
        -----
        This command is also valid for PREP7.
        """
        command = f"DSUM,{signif},{label},{td},{forcetype}"
        return self.run(command, **kwargs)

    def freq(
        self,
        freq1="",
        freq2="",
        freq3="",
        freq4="",
        freq5="",
        freq6="",
        freq7="",
        freq8="",
        freq9="",
        **kwargs,
    ):
        """Defines the frequency points for the SV vs. FREQ tables.

        APDL Command: FREQ

        Parameters
        ----------
        freq1, freq2, freq3, . . . , freq9
            Frequency points for SV vs. FREQ tables.  Values must be in
            ascending order. FREQ1 should be greater than zero.  Units are
            cycles/time.

        Notes
        -----
        Repeat the FREQ command for additional frequency points (100 maximum).
        Values are added after the last nonzero frequency.  If all fields
        (FREQ1 -- FREQ9) are blank, erase SV vs. FREQ tables.

        Frequencies must be in ascending order.

        Spectral values are input with the SV command and interpreted according
        to the SVTYP command.  Applies only to the SPRS (single-point) option
        of the SPOPT command.  See the SPFREQ command for frequency input in
        MPRS (multi-point) analysis.

        Use the STAT command to list current frequency points.

        This command is also valid in PREP7.
        """
        command = f"FREQ,{freq1},{freq2},{freq3},{freq4},{freq5},{freq6},{freq7},{freq8},{freq9}"
        return self.run(command, **kwargs)

    def grp(self, signif="", label="", forcetype="", **kwargs):
        """Specifies the grouping mode combination method.

        APDL Command: GRP

        Parameters
        ----------
        signif
            Combine only those modes whose significance level exceeds the
            SIGNIF  threshold.  For single point, multipoint, or DDAM response
            (SPOPT,SPRS, MPRS or DDAM), the significance level of a mode is
            defined as the mode coefficient of the mode, divided by the maximum
            mode coefficient of all modes.  Any mode whose significance level
            is less than SIGNIF is considered insignificant and is not
            contributed to the mode combinations.  The higher the SIGNIF
            threshold, the fewer the number of modes combined.  SIGNIF defaults
            to 0.001.  If SIGNIF is specified as 0.0, it is taken as 0.0.
            (This mode combination method is not valid for SPOPT,PSD.)

        label
            Label identifying the combined mode solution output.

            DISP - Displacement solution (default).  Displacements, stresses, forces, etc., are
                   available.

            VELO - Velocity solution.  Velocities, "stress velocities," "force velocities," etc.,
                   are available.

            ACEL - Acceleration solution.  Accelerations, "stress accelerations," "force
                   accelerations," etc., are available.

        forcetype
            Label identifying the forces to be combined:

            STATIC - Combine the modal static forces (default).

            TOTAL - Combine the modal static plus inertial forces.

        Notes
        -----
        The SIGNIF value set with this command (including the default value of
        0.001) overrides the SIGNIF value set with the MXPAND command.

        This command is also valid for PREP7.
        """
        command = f"GRP,{signif},{label},{forcetype}"
        return self.run(command, **kwargs)

    def mmass(self, option="", zpa="", **kwargs):
        """Specifies the missing mass response calculation.

        APDL Command: MMASS

        Parameters
        ----------
        option
            Flag to activate or deactivate missing mass response calculation.

            0 (OFF or NO) - Deactivate (default).

            1 (ON or YES) - Activate.

        zpa
            Zero Period Acceleration Value. If a scale factor FACT is defined
            on the SVTYP command, it is applied to this value.

        Notes
        -----
        The missing mass calculation is valid only for single point excitation
        response spectrum analysis (SPOPT, SPRS) and for multiple point
        response spectrum analysis (SPOPT, MPRS) performed with base excitation
        using acceleration response spectrum loading. Missing mass is supported
        in a spectrum analysis only when the preceding modal analysis is
        performed with the Block Lanczos, PCG Lanczos, Supernode, or Subspace
        eigensolver (Method =LANB, LANPCG, SNODE, or SUBSP on the MODOPT
        command).

        The velocity solution is not available (Label = VELO on the combination
        command: SRSS, CQC...) when the missing mass calculation is activated.

        The missing mass calculation is not supported when the spectrum
        analysis is based on a linear perturbation modal analysis performed
        after a nonlinear base analysis.

        The missing mass is not supported when superelements are present.

        To take into account the contribution of the truncated modes, the
        residual vector (RESVEC) can be used in place of the missing mass
        response. This is of particular interest if the velocity solution is
        requested or if a nonlinear prestress is included in the analysis
        (linear perturbation), or if a superelement is present, since the
        missing mass cannot be used in these cases.

        In a multiple point response spectrum analysis (SPOPT,MPRS), the MMASS
        command must precede the participation factor calculation command
        (PFACT).

        This command is also valid in PREP7.
        """
        command = f"MMASS,{option},{zpa}"
        return self.run(command, **kwargs)

    def nrlsum(self, signif="", label="", labelcsm="", forcetype="", **kwargs):
        """Specifies the Naval Research Laboratory (NRL) sum mode combination

        APDL Command: NRLSUM
        method.

        Parameters
        ----------
        signif
            Combine only those modes whose significance level exceeds the
            SIGNIF threshold. For single point, multipoint, or DDAM response
            (SPOPT,SPRS, MPRS or DDAM), the significance level of a mode is
            defined as the mode coefficient of the mode, divided by the maximum
            mode coefficient of all modes. Any mode whose significance level is
            less than SIGNIF is considered insignificant and is not contributed
            to the mode combinations. The higher the SIGNIF threshold, the
            fewer the number of modes combined. SIGNIF defaults to 0.001. If
            SIGNIF is specified as 0.0, it is taken as 0.0. (This mode
            combination method is not valid for SPOPT,PSD.)

        label
            Label identifying the combined mode solution output.

            DISP - Displacement solution (default). Displacements, stresses, forces, etc., are
                   available.

            VELO - Velocity solution. Velocities, "stress velocities," "force velocities," etc.,
                   are available.

            ACEL - Acceleration solution. Accelerations, "stress accelerations," "force
                   accelerations," etc., are available.

        labelcsm
            Label identifying the CSM (Closely Spaced Modes) method.

            CSM - Use the CSM method.

            Blank  - Do not use the CSM method (default).

        forcetype
            Label identifying the forces to be combined:

            STATIC - Combine the modal static forces (default).

            TOTAL - Combine the modal static plus inertial forces.

        Notes
        -----
        This command is also valid in PREP7. This mode combination method is
        usually used for SPOPT,DDAM.

        This CSM method is only applicable in a DDAM analysis (SPOPT,DDAM). The
        CSM method combines two closely spaced modes into one mode when their
        frequencies are within 10 percent of the common mean frequency and
        their responses are opposite in sign. The contribution of these closely
        spaced modes is then included in the NRL sum as a single effective
        mode. Refer to Closely Spaced Modes (CSM) Method in the Mechanical APDL
        Theory Reference for more information.

        NRLSUM is not allowed in ANSYS Professional.
        """
        command = f"NRLSUM,{signif},{label},{labelcsm},{forcetype}"
        return self.run(command, **kwargs)

    def pfact(self, tblno="", excit="", parcor="", **kwargs):
        """Calculates participation factors for the PSD or multi-point response

        APDL Command: PFACT
        spectrum table.

        Parameters
        ----------
        tblno
            Input PSD (Power Spectral Density) table number for which
            participation factors are to be calculated.

        excit
            Label defining the location of excitation:

            BASE - Base excitation (default).

            NODE - Nodal excitation.

        parcor
            Label defining excitation type (applies only to SPOPT,PSD
            analysis).  Used only when partially correlated excitation is due
            to wave propagation or spatial correlation.  Defaults to partially
            correlated excitation as defined by COVAL and QDVAL commands.

            WAVE - Excitation defined by PSDWAV command.

            SPAT - Excitation defined by PSDSPL command.

        Notes
        -----
        Calculates the participation factors for a particular PSD or multi-
        point response spectrum table defined with the PSDVAL or SPVAL command.
        The Jobname.DB file must contain modal solution data in order for this
        command to calculate the participation factor.  There must be a PFACT
        command for each excitation spectrum. You are limited to 300
        excitations.

        This command is also valid in PREP7.
        """
        command = f"PFACT,{tblno},{excit},{parcor}"
        return self.run(command, **kwargs)

    def pivcheck(self, key="", prntcntrl="", **kwargs):
        """Controls the behavior of an analysis when a negative or zero equation solver pivot value is encountered.

        APDL Command: PIVCHECK

        Parameters
        ----------
        key
            Determines whether to stop or continue an analysis when a negative
            or zero equation solver pivot value is encountered:

            AUTO - Check for negative or zero pivot values for analyses
                   performed with the sparse and PCG solvers. When one is
                   encountered, an error or warning is issued, per various
                   criteria relating to the type of analysis being
                   solved. An error causes the analysis to stop; a warning
                   allows the analysis to continue. A negative pivot value
                   may be valid for some nonlinear and multiphysics
                   analyses (for example, electromagnetic and thermal
                   analyses); this key has no effect in these cases.

            ERROR - Check for negative or zero pivot values for analyses
                    performed with the sparse and PCG solvers. When one is
                    encountered, an error is issued, stopping the
                    analysis. A negative pivot value may be valid for some
                    nonlinear and multiphysics analyses (for example,
                    electromagnetic and thermal analyses); this key has no
                    effect in these cases.

            WARN - Check for negative or zero pivot values for analyses
                   performed with the sparse and PCG solvers. When one is
                   encountered, a warning is issued and the analysis
                   continues. A negative pivot value may be valid for some
                   nonlinear and multiphysics analyses (for example,
                   electromagnetic and thermal analyses); this key has no
                   effect in these cases.

            OFF - Pivot values are not checked. This key causes the
                  analysis to continue in spite of a negative or zero
                  pivot value.

        prntcntrl
            Provides print options. Print output with these options will be
            sent to the default output file, not to the files created by the
            nonlinear diagnostic tools (NLDIAG).

            ONCE - Print only the maximum and minimum pivot information on
                   the first call to the sparse solver (which is the
                   default solver). This is the default behavior.

            EVERY - Print the maximum and minimum pivot information at
                    every call to the sparse solver. This option is
                    provided for nonlinear analysis diagnostics.

        Notes
        -----
        This command is valid for all analyses. In a nonlinear analysis, a
        negative pivot may be valid. In some cases, rigid body motions in
        a nonlinear analysis will be trapped by error routines checking
        infinitely large displacements (DOF limit exceeded) or
        nonconvergence status. An under-constrained model may avoid the
        pivot check, but fail with a DOF limit exceeded error.

        Machine precision may affect whether a small pivot triggers an
        error or bypasses this checking logic. You may wish to review the
        ratio of the maximum to absolute minimum pivot values. For ratios
        exceeding 12 to 14 orders of magnitude, the accuracy of the
        computed solution may be degraded by the severe ill-conditioning
        of the assembled matrix.

        Note that negative pivots corresponding to Lagrange multiplier
        based mixed u-P elements are not checked or reported by this
        command.  Negative pivots arising from the u-P element formulation
        and related analyses can occur and lead to correct solutions.

        This command is also valid in PREP7.
        """
        command = f"PIVCHECK,{key},{prntcntrl}"
        return self.run(command, **kwargs)

    def psdcom(self, signif="", comode="", forcetype="", **kwargs):
        """Specifies the power spectral density mode combination method.

        APDL Command: PSDCOM

        Parameters
        ----------
        signif
            Combine only those modes whose significance level exceeds theSIGNIF
            threshold.  For PSD response (SPOPT,PSD), the significance level is
            defined as the modal covariance matrix term, divided by the maximum
            modal covariance matrix term.  Any term whose significance level is
            less than SIGNIF is considered insignificant and is not contributed
            to the mode combinations.  The higher the SIGNIF threshold, the
            fewer the number of terms used. SIGNIF defaults to 0.0001.  If
            SIGNIF is specified as 0.0, it is taken as 0.0.

        comode
            First COMODE number of modes to be actually combined.  COMODE must
            always be less than or equal to NMODE (input quantity NMODE on the
            SPOPT command).  COMODE defaults to NMODE.  COMODE performs a
            second level of control for the first sequential COMODE number of
            modes to be combined.  It uses the significance level threshold
            indicated by SIGNIF and operates only on the significant modes.

        forcetype
            Label identifying the forces to be combined:

            STATIC - Combine the modal static forces (default).

            TOTAL - Combine the modal static plus inertial forces.

        Notes
        -----
        This command is also valid for PREP7.   This command is valid only for
        SPOPT,PSD.

        PSDCOM is not allowed in ANSYS Professional.
        """
        command = f"PSDCOM,{signif},{comode},{forcetype}"
        return self.run(command, **kwargs)

    def psdfrq(
        self,
        tblno1="",
        tblno2="",
        freq1="",
        freq2="",
        freq3="",
        freq4="",
        freq5="",
        freq6="",
        freq7="",
        **kwargs,
    ):
        """Defines the frequency points for the input spectrum tables PSDVAL vs.

        APDL Command: PSDFRQ
        PSDFRQ for PSD analysis.

        Parameters
        ----------
        tblno1
            Input table number.  When used with the COVAL or the QDVAL command,
            TBLNO1 represents the row number of this table. Up to 200 tables
            may be defined.

        tblno2
            Input table number.  TBLNO2 is used only for the COVAL or the QDVAL
            commands and represents the column number of this table.

        freq1, freq2, freq3, . . . , freq7
            Frequency points (cycles/time) for spectrum vs. frequency tables.
            FREQ1 should be greater than zero, and values must be in ascending
            order.  Log-log interpolation will be used between frequency
            points.

        Notes
        -----
        The spectrum values may be input with the PSDVAL, COVAL , or QDVAL
        commands.  A separate PSDFRQ command must be used for each table and
        cross table defined.  Frequencies must be in ascending order.

        Repeat PSDFRQ command for additional frequency points.  Values are
        added after the last nonzero frequency.  If all fields after PSDFRQ are
        blank, all input vs. frequency tables are erased.  If TBLNO1 is
        nonblank, all corresponding PSDVAL tables are erased.  If both TBLNO1
        and TBLNO2 are nonblank,  all corresponding COVAL and QDVAL tables are
        erased.

        This command is also valid in PREP7.
        """
        command = f"PSDFRQ,{tblno1},{tblno2},{freq1},{freq2},{freq3},{freq4},{freq5},{freq6},{freq7}"
        return self.run(command, **kwargs)

    def psdgraph(self, tblno1="", tblno2="", **kwargs):
        """Displays input PSD curves

        APDL Command: PSDGRAPH

        Parameters
        ----------
        tblno1
            PSD table number to display.

        tblno2
            Second PSD table number to display. TBLNO2 is used only in
            conjunction with the COVAL or the QDVAL commands.

        Notes
        -----
        The input PSD tables are displayed in log-log format as dotted lines.
        The best-fit curves, used to perform the closed-form integration, are
        displayed as solid lines. If there is a significant discrepancy between
        the two, then you should add one or more intermediate points to the
        table to obtain a better fit.

        If TBLNO2 is zero, blank, or equal to TBLNO1, then the autospectra
        (PSDVAL) are displayed for TBLNO1. If TBLNO2 is also specified, then
        the autospectra for TBLNO1 and TBLNO2 are displayed, along with the
        corresponding cospectra (COVAL) and quadspectra (QDVAL), if they are
        defined.

        This command is valid in any processor.
        """
        command = f"PSDGRAPH,{tblno1},{tblno2}"
        return self.run(command, **kwargs)

    def psdres(self, lab="", relkey="", **kwargs):
        """Controls solution output written to the results file from a PSD

        APDL Command: PSDRES
        analysis.

        Parameters
        ----------
        lab
            Label identifying the solution output:

            DISP - Displacement solution (default).  One-sigma displacements, stresses, forces,
                   etc.  Written as load step 3 on File.RST.

            VELO - Velocity solution.  One-sigma velocities, "stress velocities," "force
                   velocities," etc.  Written as load step 4 of File.RST.

            ACEL - Acceleration solution.  One-sigma accelerations, "stress accelerations," "force
                   accelerations," etc.  Written as load step 5 on File.RST.

        relkey
            Key defining relative or absolute calculations:

            REL - Calculations are relative to the base excitation (default).

            ABS - Calculations are absolute.

            OFF - No calculation of solution output identified by Lab.

        Notes
        -----
        Controls the amount and form of solution output written to the results
        file from a PSD analysis.  One-sigma values of the relative or absolute
        displacement solution, relative or absolute velocity solution, relative
        or absolute acceleration solution, or any combination may be included
        on the results file.

        This command is also valid in PREP7.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"PSDRES,{lab},{relkey}"
        return self.run(command, **kwargs)

    def psdspl(self, tblno="", rmin="", rmax="", **kwargs):
        """Defines a partially correlated excitation in a PSD analysis.

        APDL Command: PSDSPL

        Parameters
        ----------
        tblno
            Input PSD table number defined with PSDVAL command.

        rmin
            Minimum distance between excitation points which are partially
            correlated. Excited nodes closer than RMIN will be fully
            correlated.

        rmax
            Maximum distance between excitation points which are partially
            correlated. Excited nodes farther apart than RMAX will be
            uncorrelated.

        Notes
        -----
        Defines a partially correlated excitation in terms of a sphere of
        influence relating excitation point geometry (in a PSD analysis).  If
        the distance between any two excitation points is less than RMIN, then
        the excitation is fully correlated.  If the distance is greater than
        RMAX, then the excitation is uncorrelated.  If the distance lies
        between RMIN and RMAX, then the excitation is partially correlated with
        the degree of correlation dependent on the separation distance between
        the points. This command is not available for a pressure PSD analysis.

        This command is also valid in PREP7.
        """
        command = f"PSDSPL,{tblno},{rmin},{rmax}"
        return self.run(command, **kwargs)

    def psdunit(self, tblno="", type_="", gvalue="", **kwargs):
        """Defines the type of input PSD.

        APDL Command: PSDUNIT

        Parameters
        ----------
        tblno
            Input table number.

        type\_
            Label identifying the type of spectrum:

            DISP - Displacement spectrum (in terms of displacement2/Hz ).

            VELO - Velocity spectrum (in terms of velocity2/Hz ).

            ACEL - Acceleration spectrum (in terms of acceleration2/Hz ).

            ACCG - Acceleration spectrum (in terms of g2/Hz ).

            FORC - Force spectrum (in terms of force2/Hz ).

            PRES - Pressure spectrum (in terms of pressure2/Hz ).

        gvalue
            Value of acceleration due to gravity in any arbitrary units for
            Type=ACCG.  Default is 386.4 in/sec2.

        Notes
        -----
        Defines the type of PSD defined by the PSDVAL, COVAL, and QDVAL
        commands.

        Force (FORC) and pressure (PRES) type spectra can be used only as a
        nodal excitation.

        GVALUE is valid only when type ACCG is specified.  A zero or negative
        value cannot be used.  A parameter substitution can also be performed.

        This command is also valid in PREP7.
        """
        command = f"PSDUNIT,{tblno},{type_},{gvalue}"
        return self.run(command, **kwargs)

    def psdval(
        self,
        tblno="",
        sv1="",
        sv2="",
        sv3="",
        sv4="",
        sv5="",
        sv6="",
        sv7="",
        **kwargs,
    ):
        """Defines PSD values.

        APDL Command: PSDVAL

        Parameters
        ----------
        tblno
            Input table number being defined.

        sv1, sv2, sv3, . . . , sv7
            Spectral values corresponding to the frequency points [PSDFRQ].
            Values are interpreted as defined with the PSDUNIT command.

        Notes
        -----
        Defines PSD values to be associated with the previously defined
        frequency points.

        Repeat PSDVAL command for additional values, up to the number of
        frequency points [PSDFRQ].  Values are added after the last nonzero
        value.

        This command is also valid in PREP7.
        """
        command = f"PSDVAL,{tblno},{sv1},{sv2},{sv3},{sv4},{sv5},{sv6},{sv7}"
        return self.run(command, **kwargs)

    def psdwav(self, tblno="", vx="", vy="", vz="", **kwargs):
        """Defines a wave propagation excitation in a PSD analysis.

        APDL Command: PSDWAV

        Parameters
        ----------
        tblno
            Input PSD table number defined with PSDVAL command.

        vx
            Global Cartesian X-velocity of traveling wave.

        vy
            Global Cartesian Y-velocity of traveling wave.

        vz
            Global Cartesian Z-velocity of traveling wave.

        Notes
        -----
        Defines a traveling wave in a PSD analysis. This command is not
        available for a pressure PSD analysis.

        This command is also valid in PREP7.
        """
        command = f"PSDWAV,{tblno},{vx},{vy},{vz}"
        return self.run(command, **kwargs)

    def qdval(
        self,
        tblno1="",
        tblno2="",
        sv1="",
        sv2="",
        sv3="",
        sv4="",
        sv5="",
        sv6="",
        sv7="",
        **kwargs,
    ):
        """Defines PSD quadspectral values.

        APDL Command: QDVAL

        Parameters
        ----------
        tblno1
            First input PSD table number associated with this spectrum.

        tblno2
            Second input PSD table number associated with this spectrum.

        sv1, sv2, sv3, . . . , sv7
            PSD quadspectral values corresponding to the frequency points
            [PSDFRQ].

        Notes
        -----
        Defines PSD quadspectral values to be associated with the previously
        defined frequency points.  Repeat QDVAL command with the same table
        number for additional points.  Unlike autospectra [PSDVAL], the
        quadspectra can be positive or negative.  The quadspectral curve
        segment where there is a sign change is interpolated linearly (the rest
        of the curve segments use log-log interpolation).  For better accuracy,
        choose as small a curve segment as possible wherever a sign change
        occurs.

        Two table numbers are required since values are off-diagonal terms.
        This command is valid for SPOPT,PSD only.

        This command is also valid in PREP7.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"QDVAL,{tblno1},{tblno2},{sv1},{sv2},{sv3},{sv4},{sv5},{sv6},{sv7}"
        return self.run(command, **kwargs)

    def rock(self, cgx="", cgy="", cgz="", omx="", omy="", omz="", **kwargs):
        """Specifies a rocking response spectrum.

        APDL Command: ROCK

        Parameters
        ----------
        cgx, cgy, cgz
            Global Cartesian X, Y, and Z location of center of rotation about
            which rocking occurs.

        omx, omy, omz
            Global Cartesian angular velocity components associated with the
            rocking.

        Notes
        -----
        Specifies a rocking response spectrum effect in the spectrum
        (ANTYPE,SPECTR) analysis.

        The excitation direction with rocking included is not normalized to
        one; rather, it scales the spectrum. For more information, see
        Participation Factors and Mode Coefficients.

        This command is also valid in PREP7.
        """
        command = f"ROCK,{cgx},{cgy},{cgz},{omx},{omy},{omz}"
        return self.run(command, **kwargs)

    def rose(self, signif="", label="", td="", forcetype="", **kwargs):
        """Specifies the Rosenblueth mode combination method.

        APDL Command: ROSE

        Parameters
        ----------
        signif
            Combine only those modes whose significance level exceeds the
            SIGNIF threshold. For single point, multipoint, or DDAM response
            (SPOPT, SPRS, MPRS, or DDAM), the significance level of a mode is
            defined as the mode coefficient of the mode, divided by the maximum
            mode coefficient of all modes. Any mode whose significance level is
            less than SIGNIF is considered insignificant and does not
            contribute to the mode combinations. The higher the SIGNIF
            threshold, the fewer the number of modes combined. SIGNIF defaults
            to 0.001. If SIGNIF is specified as 0.0, it is taken as 0.0.

        label
            Label identifying the combined mode solution output.

            DISP - Displacement solution (default). Displacements, stresses, forces, etc., are
                   available.

            VELO - Velocity solution. Velocities, "stress velocities," "force velocities," etc.,
                   are available.

            ACEL - Acceleration solution. Accelerations, "stress accelerations," "force
                   accelerations," etc. are available.

        td
            Time duration for earthquake or shock spectrum. TD defaults to 10.

        forcetype
            Label identifying the forces to be combined:

            STATIC - Combine the modal static forces (default).

            TOTAL - Combine the modal static plus inertial forces.

        Notes
        -----
        For more information on spectrum analysis combination methods, see
        Combination of Modes

        This command is also valid in PREP7.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"ROSE,{signif},{label},{td},{forcetype}"
        return self.run(command, **kwargs)

    def rigresp(self, option="", method="", val1="", val2="", **kwargs):
        """Specifies the rigid response calculation.

        APDL Command: RIGRESP

        Parameters
        ----------
        option
            Flag to activate or deactivate the rigid response calculation:

            1 (ON or YES) - Activate.

            2 (OFF or NO) - Deactivate. This value is the default.

        method
            Method used to calculate the rigid response:

            GUPTA - Gupta method.

            LINDLEY - Lindley-Yow method.

        val1
            If Method = GUPTA, Val1 represents the frequency F1 in Hertz.

        val2
            If Method = GUPTA, Val2 represents the frequency F2 in Hertz.

        Notes
        -----
        This rigid response calculation is only valid for single point response
        spectrum analysis (SPOPT, SPRS) and multiple point response spectrum
        analysis (SPOPT, MPRS) with combination methods (SRSS), complete
        quadratic (CQC) or Rosenblueth (ROSE)

        This command is also valid in PREP7.

        Only Sptype = SPRS is allowed in ANSYS Professional.
        """
        command = f"RIGRESP,{option},{method},{val1},{val2}"
        return self.run(command, **kwargs)

    def sed(self, sedx="", sedy="", sedz="", cname="", **kwargs):
        """Defines the excitation direction for response spectrum and PSD

        APDL Command: SED
        analyses.

        Parameters
        ----------
        sedx, sedy, sedz
            Global Cartesian coordinates of a point that defines a line
            (through the origin) corresponding to the excitation direction.
            For example: 0.0, 1.0, 0.0 defines global Y as the spectrum
            direction.

        cname
            The component name corresponding to the group of excited nodes.
            Only applies to base excitation multi-point response spectrum
            analysis (SPOPT, MPRS) and power spectral density analysis (SPOPT,
            PSD). Defaults to no component.

        Notes
        -----
        In single-point response spectrum analysis (SPOPT,SPRS), the excitation
        direction without rocking (ROCK) is normalized to one so that the SEDX,
        SEDY, and SEDZ values do not scale the spectrum.  The excitation
        direction with rocking is not normalized. The SEDX, SEDY, and SEDZ
        values must be consistent with the OMX, OMY, and OMZ values on the ROCK
        command. The calculated direction then scales the spectrum. For more
        information, see Participation Factors and Mode Coefficients.

        In multi-point response spectrum analysis (SPOPT,MPRS) and power
        spectral density analysis (SPOPT,PSD), the excitation direction is
        normalized to one so that the SEDX, SEDY, and SEDZ values do not scale
        the spectrum.  The component name (Cname) is required. The constraints
        corresponding to the excitation direction are applied to the component
        nodes.

        This command is also valid in PREP7.
        """
        command = f"SED,{sedx},{sedy},{sedz},{cname}"
        return self.run(command, **kwargs)

    def spdamp(self, tblno="", curvno="", dampratio="", **kwargs):
        """Defines input spectrum damping in a multi-point response spectrum

        APDL Command: SPDAMP
        analysis.

        Parameters
        ----------
        tblno
            Input table number. Corresponds to the frequency table number
            (TBLNO on the SPFREQ command).

        curvno
            Input curve number. Corresponds to the spectrum values curve number
            (CURVNO on the SPVAL command).

        dampratio
            Damping ratio for the response spectrum curve. Up to 20 different
            curves may be defined, each with a different damping ratio. Damping
            values must be input in ascending order.

        Notes
        -----
        Defines multi-point response spectrum damping value to be associated
        with:

        Previously defined frequency points (SPFREQ).

        Subsequently defined spectrum points (SPVAL).

        Damping values are used only to identify input spectrum values for the
        mode coefficients calculation.

        The curve number must be input in ascending order starting with 1.

        This command is also valid in PREP7.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"SPDAMP,{tblno},{curvno},{dampratio}"
        return self.run(command, **kwargs)

    def spfreq(
        self,
        tblno="",
        freq1="",
        freq2="",
        freq3="",
        freq4="",
        freq5="",
        freq6="",
        freq7="",
        **kwargs,
    ):
        """Defines the frequency points for the input spectrum tables SPVAL vs.

        APDL Command: SPFREQ
        SPFREQ for multi-point spectrum analysis.

        Parameters
        ----------
        tblno
            Input table number. Up to 200 tables may be defined.

        freq1, freq2, freq3,..., freq7
            Frequency points (Hz) for spectrum vs. frequency tables. FREQ1
            should be greater than zero, and values must be in ascending order.

        Notes
        -----
        The spectrum values are input with the SPVAL command. A separate SPFREQ
        command must be used for each table defined. Frequencies must be in
        ascending order.

        Repeat SPFREQ command for additional frequency points. Values are added
        after the last nonzero frequency.

        If all fields after SPFREQ are blank, all input vs. frequency tables
        are erased. If TBLNO is the only non-blank field, all corresponding
        SPVAL curves are erased.

        Use the SPTOPT and STAT commands to list current frequency points.

        This command is also valid in PREP7.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = (
            f"SPFREQ,{tblno},{freq1},{freq2},{freq3},{freq4},{freq5},{freq6},{freq7}"
        )
        return self.run(command, **kwargs)

    def spgraph(self, tblno="", curvno="", curvnobeg="", **kwargs):
        """Displays input spectrum curves for MPRS analysis.

        APDL Command: SPGRAPH

        Parameters
        ----------
        tblno
            Table number to display.  Defaults to 1.

        curvno
            Curve number to display. Defaults to none.

        curvnobeg
            Beginning of the curve number range to display. Defaults to 1.

        Notes
        -----
        You can display up to 10 input spectrum curves (SPVAL and SPFREQ
        commands) with log X scale.

        If the input spectrum curves are not associated with a damping value
        (SPDAMP command), CURVNO and CURVNOBeg are not applicable and table
        TBLNO is displayed. Otherwise, specify CURVNO or CURVNOBeg:

        if CURVNO is used, one curve is displayed.

        if CURVNOBeg is used, up to 10 curves are displayed. CURVNOBeg is the
        beginning of the curve number range of interest.
        """
        command = f"SPGRAPH,{tblno},{curvno},{curvnobeg}"
        return self.run(command, **kwargs)

    def spopt(self, sptype="", nmode="", elcalc="", modereusekey="", **kwargs):
        """Selects the spectrum type and other spectrum options.

        APDL Command: SPOPT

        Parameters
        ----------
        sptype
            Spectrum type:

            SPRS - Single point excitation response spectrum (default).  See also the SVTYP
                   command.

            MPRS - Multiple point excitation response spectrum.

            DDAM - Dynamic design analysis method.

            PSD - Power spectral density.

        nmode
            Use the first NMODE modes from the modal analysis.  Defaults to all
            extracted modes, as specified by the MODOPT and BUCOPT commands.
            NMODE cannot be larger than 10000.

        elcalc
            Element results calculation key (for Sptype = PSD only):

            NO - Do not calculate element results and reaction forces (default).

            YES - Calculate element results and reaction forces, as well as the nodal degree of
                  freedom solution.

        modereusekey
            Key for existing MODE file reuse when running multiple spectrum
            analyses:

            NO - No spectrum analysis has been performed yet (default).

            YES - This is not the first spectrum analysis.  The MODE file will be reused and the
                  necessary files will be cleaned up for the new spectrum
                  analysis.

        Notes
        -----
        Valid only for a spectrum analysis (ANTYPE,SPECTR).  This operation
        must be preceded by a modal solution (ANTYPE,MODAL) with the
        appropriate files available.  Both the spectrum analysis and the
        preceding modal analysis must be performed under the same ANSYS version
        number.

        If used in SOLUTION, this command is valid only within the first load
        step.

        This command is also valid in PREP7.

        Only Sptype = SPRS is allowed in ANSYS Professional.
        """
        command = f"SPOPT,{sptype},{nmode},{elcalc},{modereusekey}"
        return self.run(command, **kwargs)

    def spunit(self, tblno="", type_="", gvalue="", keyinterp="", **kwargs):
        """Defines the type of multi-point response spectrum.

        APDL Command: SPUNIT

        Parameters
        ----------
        tblno
            Input table number.

        type\_
            Label identifying the type of spectrum:

            DISP   - Displacement spectrum (SPVAL values interpreted as displacements with units of
                     length).

            VELO   - Velocity spectrum (SPVAL values interpreted as velocities with units of
                     length/time).

            ACEL   - Acceleration spectrum (SPVAL values interpreted as accelerations with units of
                     length/time2).

            ACCG   - Acceleration spectrum (SPVAL values interpreted as accelerations with units of
                     g/time2).

            FORC   - Force spectrum.

            PRES   - Pressure spectrum.

        gvalue
            Value of acceleration due to gravity in any arbitrary units for
            Type=ACCG table. Default is 386.4 in/sec2.

        keyinterp
            Key to activate or deactivate the linear interpolation between
            input response spectrum points and input response spectrum curves:

            0 (OFF or NO) - Deactivate linear and use logarithmic interpolation. This value is the default.

            1 (ON or YES) - Activate linear interpolation.

        Notes
        -----
        Defines the type of multi-point response spectrum defined by the SPFREQ
        and  SPVAL commands.

        Force (FORC) and pressure (PRES) type spectra can be used only as a
        nodal excitation.

        GVALUE is valid only when type=ACCG is specified. A zero or negative
        value cannot be used. A parameter substitution can also be performed.

        This command is also valid in PREP7.
        """
        command = f"SPUNIT,{tblno},{type_},{gvalue},{keyinterp}"
        return self.run(command, **kwargs)

    def spval(
        self,
        tblno="",
        curvno="",
        sv1="",
        sv2="",
        sv3="",
        sv4="",
        sv5="",
        sv6="",
        sv7="",
        **kwargs,
    ):
        """Defines multi-point response spectrum values.

        APDL Command: SPVAL

        Parameters
        ----------
        tblno
            Input table number. It corresponds to TBLNO on the SPFREQ command.

        curvno
            Input curve number. It corresponds to CURVNO on the SPDAMP command
            (optional).

        sv1, sv2, sv3, , , . . . , sv7
            Spectral values corresponding to the frequency points (SPFREQ) and
            damping ratio (SPDAMP). Values are interpreted as defined with the
            SPUNIT command.

        Notes
        -----
        Defines multi-point response spectrum values to be associated with the
        previously defined frequency points (SPFREQ). It can also be associated
        with the previously defined damping value (SPDAMP). If CURVNO is not
        specified, the input spectrum is not associated with a damping value.

        Repeat SPVAL command for additional values, up to the number of
        frequency points (SPFREQ). Values are added after the last nonzero
        value.

        The interpolation method between response spectrum points and curves is
        specified using KeyInterp on the SPUNIT command. It is logarithmic by
        default.

        Use the SPTOPT and STAT commands to list current spectrum curve values.

        This command is also valid in PREP7.
        """
        command = f"SPVAL,{tblno},{curvno},{sv1},{sv2},{sv3},{sv4},{sv5},{sv6},{sv7}"
        return self.run(command, **kwargs)

    def srss(self, signif="", label="", abssumkey="", forcetype="", **kwargs):
        """Specifies the square root of sum of squares mode combination method.

        APDL Command: SRSS

        Parameters
        ----------
        signif
            Combine only those modes whose significance level exceeds the
            SIGNIF threshold.  For single point, multipoint, or DDAM response
            (SPOPT,SPRS, MPRS or DDAM), the significance level of a mode is
            defined as the mode coefficient of the mode, divided by the maximum
            mode coefficient of all modes.  Any mode whose significance level
            is less than SIGNIF is considered insignificant and is not
            contributed to the mode combinations.  The higher the SIGNIF
            threshold, the fewer the number of modes combined. SIGNIF defaults
            to 0.001.  If SIGNIF is specified as 0.0, it is taken as 0.0.
            (This mode combination method is not valid for SPOPT,PSD.)

        label
            Label identifying the combined mode solution output.

            DISP - Displacement solution (default).  Displacements, stresses, forces, etc., are
                   available.

            VELO - Velocity solution.  Velocities, "stress velocities," "force velocities," etc.,
                   are available.

            ACEL - Acceleration solution.  Accelerations, "stress accelerations," "force
                   accelerations," etc., are available.

        abssumkey
            Absolute Sum combination key (for SPOPT,MPRS only):

            NO - Do not use the Absolute Sum method (default).

            YES - Combine the modes per excitation direction using the Absolute Sum method, then
                  combine the resulting quantities using the square root of sum
                  of squares method.

        forcetype
            Label identifying the forces to be combined:

            STATIC - Combine the modal static forces (default).

            TOTAL - Combine the modal static plus inertial forces.

        Notes
        -----
        This command is also valid for PREP7.
        """
        command = f"SRSS,{signif},{label},{abssumkey},{forcetype}"
        return self.run(command, **kwargs)

    def sv(
        self,
        damp="",
        sv1="",
        sv2="",
        sv3="",
        sv4="",
        sv5="",
        sv6="",
        sv7="",
        sv8="",
        sv9="",
        **kwargs,
    ):
        """Defines spectrum values to be associated with frequency points.

        APDL Command: SV

        Parameters
        ----------
        damp
            Damping ratio for this response spectrum curve.  If the same as a
            previously defined curve, the SV values are added to the previous
            curve.  Up to four different curves may be defined, each with a
            different damping ratio.  Damping values must be input in ascending
            order.

        sv1, sv2, sv3, . . . , sv9
            Spectrum values corresponding to the frequency points [FREQ].
            Values are interpreted as defined with the SVTYP command.   SV
            values should not be zero.  Values required outside the frequency
            range use the extreme input values.

        Notes
        -----
        Defines the spectrum values to be associated with the previously
        defined frequency points [FREQ].  Applies only to the single-point
        response spectrum.  Damping has no effect on the frequency solution.
        Damping values are used only to identify SV curves for the mode
        combinations calculation.  Only the curve with the lowest damping value
        is used in the initial mode coefficient calculation.  Use STAT command
        to list current spectrum curve values.

        Repeat SV command for additional SV points (100 maximum per DAMP
        curve).  SV values are added to the DAMP curve after the last nonzero
        SV value.

        The interpolation method between response spectrum points and curves is
        specified using KeyInterp in the SVTYP command. It is logarithmic by
        default.

        This command is also valid in PREP7.
        """
        command = f"SV,{damp},{sv1},{sv2},{sv3},{sv4},{sv5},{sv6},{sv7},{sv8},{sv9}"
        return self.run(command, **kwargs)

    def svplot(self, optionscale="", damp1="", damp2="", damp3="", damp4="", **kwargs):
        """Displays input spectrum curves.

        APDL Command: SVPLOT

        Parameters
        ----------
        optionscale
            Flag to activate or deactivate input spectrum value scaling:

            OFF  - Do not scale the input spectrum values with scale factor FACT (SVTYP command).
                   This is the default value.

            ON  - Scale the input spectrum values with scale factor FACT (SVTYP command)

        damp1
            Damping ratio corresponding to DAMP (SV command) defining the first
            spectrum curve.

        damp2
            Damping ratio corresponding to DAMP (SV command) defining the
            second spectrum curve.

        damp3
            Damping ratio corresponding to DAMP (SV command) defining the third
            spectrum curve.

        damp4
            Damping ratio corresponding to DAMP (SV command) defining the
            fourth spectrum curve.

        Notes
        -----
        You can display up to four input spectrum tables (SV and FREQ commands)
        with log X scale. If no damping ratio is specified, all spectrum tables
        are displayed.

        This command is valid in any processor.
        """
        command = f"SVPLOT,{optionscale},{damp1},{damp2},{damp3},{damp4}"
        return self.run(command, **kwargs)

    def svtyp(self, ksv="", fact="", keyinterp="", **kwargs):
        """Defines the type of single-point response spectrum.

        APDL Command: SVTYP

        Parameters
        ----------
        ksv
            Response spectrum type:

            0 - Seismic velocity response spectrum loading (SV values interpreted as velocities
                with units of length/time).

            1 - Force response spectrum loading (SV values interpreted as force amplitude
                multipliers).

            2 - Seismic acceleration response spectrum loading (SV values interpreted as
                accelerations with units of length/time2).

            3 - Seismic displacement response spectrum loading (SV values interpreted as
                displacements with units of length).

            4 - PSD loading (SV values interpreted as acceleration2/(cycles/time), such as
                (in/sec2)2/Hz (not g2/Hz)).  (Not recommended)

        fact
            Scale factor applied to spectrum values (defaults to 1.0).  Values
            are scaled when the solution is initiated [SOLVE].  Database values
            remain the same.

        keyinterp
            Key to activate or deactivate the linear interpolation between
            input response spectrum points and input response spectrum curves:

            0 (OFF or NO) - Deactivate linear and use logarithmic interpolation. This value is the default.

            1 (ON or YES) - Activate linear interpolation.

        Notes
        -----
        Defines the type of single-point response spectrum [SPOPT].  The
        seismic excitation direction is defined with the SED command.

        This command is also valid in PREP7.
        """
        command = f"SVTYP,{ksv},{fact},{keyinterp}"
        return self.run(command, **kwargs)

    def vddam(self, vf="", va="", vb="", vc="", **kwargs):
        """Specifies the velocity spectrum computation constants for the analysis

        APDL Command: VDDAM
        of shock resistance of shipboard structures.

        Parameters
        ----------
        vf
            Direction-dependent velocity coefficient for elastic or elastic-
            plastic analysis option (Default = 0).

        va, vb, vc
            Coefficients for the DDAM velocity spectrum equations.  See Dynamic
            Design Analysis Method in the Mechanical APDL Theory Reference.
            Default for these coefficients is zero.

        Notes
        -----
        This command specifies velocity coefficients to analyze shock
        resistance of shipboard equipment.  These coefficients are used to
        compute mode coefficients according to the equations given in Dynamic
        Design Analysis Method in the Mechanical APDL Theory Reference.  The
        form of these equations is based on the Naval NRL Dynamic Design
        Analysis Method.  This command, along with the ADDAM and SED commands,
        is used with the spectrum (ANTYPE,SPECTR) analysis as a special purpose
        alternative to the SV, FREQ, and SVTYP commands.  The mass and length
        units of the model must be in pounds and inches, respectively.

        DDASPEC may alternatively be used to calculate spectrum coefficients.

        This command is also valid in PREP7.
        """
        command = f"VDDAM,{vf},{va},{vb},{vc}"
        return self.run(command, **kwargs)
