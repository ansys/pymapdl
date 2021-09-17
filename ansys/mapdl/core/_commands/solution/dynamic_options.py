class DynamicOptions:
    def alphad(self, value="", **kwargs):
        """Defines the mass matrix multiplier for damping.

        APDL Command: ALPHAD

        Parameters
        ----------
        value
            Mass matrix multiplier for damping.

        Notes
        -----
        This command defines the mass matrix multiplier α used to form the
        viscous damping matrix [C] = α[M] where [M] is the mass matrix.

        Values of  α may also be input as a material property (use the ALPD
        label on the MP command). If ALPD is included, the ALPD value is added
        to the ALPHAD value as appropriate (see Damping Matrices in the
        Mechanical APDL Theory Reference). Damping is not used in the static
        (ANTYPE,STATIC) or buckling (ANTYPE,BUCKLE) analyses.

        This command is also valid in PREP7.
        """
        command = f"ALPHAD,{value}"
        return self.run(command, **kwargs)

    def betad(self, value="", **kwargs):
        """Defines the stiffness matrix multiplier for damping.

        APDL Command: BETAD

        Parameters
        ----------
        value
            Stiffness matrix multiplier for damping.

        Notes
        -----
        This command defines the stiffness matrix multiplier β used to form the
        viscous damping matrix [C] = β [K] where [K] is the stiffness matrix.

        Values of : β may also be input as a material property (use the BETD
        label on the MP command).  If BETD is included, the BETD value is added
        to the BETAD value as appropriate (see Damping Matrices in the
        Mechanical APDL Theory Reference).  Damping is not used in the static
        (ANTYPE,STATIC) or buckling (ANTYPE,BUCKLE) analyses.

        This command is also valid in PREP7.
        """
        command = f"BETAD,{value}"
        return self.run(command, **kwargs)

    def dmprat(self, ratio="", **kwargs):
        """Sets a constant modal damping ratio.

        APDL Command: DMPRAT

        Parameters
        ----------
        ratio
            Modal damping ratio (for example, 2% is input as 0.02).

        Notes
        -----
        Sets a constant damping ratio for use in the mode-superposition
        transient (ANTYPE,TRANS) or harmonic (ANTYPE,HARMIC) analysis and the
        spectrum (ANTYPE,SPECTR) analysis.

        This command is also valid in PREP7.
        """
        command = f"DMPRAT,{ratio}"
        return self.run(command, **kwargs)

    def dmpstr(self, coeff="", **kwargs):
        """Sets a constant structural damping coefficient.

        APDL Command: DMPSTR

        Parameters
        ----------
        coeff
            Structural damping coefficient.

        Notes
        -----
        Sets a constant structural (or hysteretic) damping coefficient for use
        in harmonic (ANTYPE,HARMIC) analyses (FULL, MSUP, and VT) and modal
        analyses (ANTYPE,MODAL with MODOPT,UNSYM, DAMP or QRDAMP).

        Note that for structures with multiple materials, MP,DMPR can also be
        used to specify constant structural material damping on a per material
        basis. Note that if both DMPSTR and MP,DMPR are specified, the damping
        effects are additive.

        Caution:: : DMPSTR adds the damping contribution as gK, whereas MP,DMPR
        adds the contribution on a per-material basis as 2gK. For more
        information, see Damping Matrices in the Mechanical APDL Theory
        Reference.

        This command is also valid in PREP7.
        """
        command = f"DMPSTR,{coeff}"
        return self.run(command, **kwargs)

    def frqscl(self, scaling="", **kwargs):
        """Turns on automatic scaling of the entire mass matrix and frequency

        APDL Command: FRQSCL
        range for modal analyses using the Block Lanczos, PCG Lanczos, or
        Supernode mode extraction method.

        Parameters
        ----------
        scaling


            Off  - Do not use automatic scaling of the mass matrix and frequency range.

            On  - Use automatic scaling of the mass matrix and frequency range.

        Notes
        -----
        Use this command to deactivate or force activation of automatic scaling
        of the entire mass matrix and frequency range for modal analyses where
        the entire mass matrix is significantly different (i.e., orders of
        magnitude difference) than the entire stiffness matrix (for example,
        due to the particular unit system being used).  Where the mass matrix
        is significantly smaller compared to the stiffness matrix, the
        eigenvalues will tend to approach very large numbers (>10e12), making
        the Block Lanczos, PCG Lanczos, or Supernode mode extraction method
        less efficient and more likely to miss modes.

        ANSYS uses scaling (if appropriate) by default. However, you can issue
        FRQSCL,ON to force the entire mass matrix and frequency range to be
        scaled to bring the stiffness and mass matrices closer together in
        terms of orders of magnitude, improving efficiency and reducing the
        likelihood of missed modes.  The resulting eigenvalues are then
        automatically scaled back to the original system. If you are using
        micro MKS units, where the density is typically very small compared to
        the stiffness, you may want to issue FRQSCL,ON to force scaling on.

        If the stiffness and mass are on the same scale, FRQSCL,ON has no
        effect.

        This command is available only for modal analyses using the Block
        Lanczos, PCG Lanczos, or Supernode mode extraction method (MODOPT,LANB,
        LANPCG, or SNODE).

        This command is not valid and has no effect when used in conjunction
        with the MSAVE,ON command in a modal analysis with the PCG Lanczos mode
        extraction method.
        """
        command = f"FRQSCL,{scaling}"
        return self.run(command, **kwargs)

    def harfrq(self, freqb="", freqe="", logopt="", freqarr="", toler="", **kwargs):
        """Defines the frequency range in a harmonic analysis.

        APDL Command: HARFRQ

        Parameters
        ----------
        freqb
            Frequency (Hz) at the beginning of the FREQB to FREQE range (if
            FREQE > FREQB).  If FREQE is blank, the solution is done only at
            frequency FREQB (the central frequency of octave bands, when LogOpt
            = OB1, OB2, OB3, OB6, OB12 or OB24).

        freqe
            Frequency at end of this range.  Solutions are done at an interval
            of (FREQE-FREQB) / NSBSTP, ending at FREQE.  No solution is done at
            the beginning of the frequency range.  NSBSTP is input via the
            NSUBST command.  See the EXPSOL command documentation for expansion
            pass solutions.

        --
            Reserved.

        logopt
            Logarithm frequency span. Solutions are done at an interval of
            (log(FREQE) - log(FREQB)) / (NSBSTP-1), (NSBSTP>1). The central
            frequency or beginning frequency is used for NSBSTP = 1. Valid
            values are:

            OB1 - Octave band.

            OB2 - 1/2 octave band.

            OB3 - 1/3 octave band.

            OB6 - 1/6 octave band.

            OB12 - 1/12 octave band.

            OB24 - 1/24 octave band.

            LOG - General logarithm frequency span.

        freqarr
            An array containing frequency values (Hz). Combined with the
            tolerance argument, Toler, these values are merged with values
            calculated based on the specifications from FREQB, FREQE, and
            LogOpt, as well NSBSTP on the NSUBST command and Clust on the HROUT
            command. Enclose the array name in percent (%) signs (for example,
            HARFRQ,,,,,%arrname%). Use ``*DIM`` to define the array.

        toler
            Tolerance to determine if a user input frequency value in FREQARR
            is a duplicate and can be ignored. Two frequency values are
            considered duplicates if their difference is less than the
            frequency range multiplied by the tolerance. The default value is 1
            x 10-5.

        Notes
        -----
        Defines the frequency range for loads in the harmonic analysis
        (ANTYPE,HARMIC).

        Do not use this command for a harmonic ocean wave analysis (HROCEAN).

        When frequencies are user-defined, the array FREQARR must be one-
        dimensional and contain positive values. User-defined frequency input
        is not supported in the following cases:

        in a cyclic symmetry harmonic analysis

        when the Variational Technology method is used (Method = VT on the
        HROPT command)

        This command is also valid in PREP7.
        """
        command = f"HARFRQ,{freqb},{freqe},{logopt},{freqarr},{toler}"
        return self.run(command, **kwargs)

    def hrexp(self, angle="", **kwargs):
        """Specifies the phase angle for the harmonic analysis expansion pass.

        APDL Command: HREXP

        Parameters
        ----------
        angle
            Phase angle (degrees) for expansion pass.  If ALL (default), use
            both 0.0° (real) and 90.0° (imaginary) phase angles.

        Notes
        -----
        Specifies the phase angle where the expansion pass will be done for a
        harmonic mode-superposition expansion pass.

        For a specific angle, the following real solution is stored in the
        results (``*.rst``) file:

        If ANGLE is ALL, both the real and imaginary parts of the solution are
        stored in the results file.

        For more details about the solution equations, see Harmonic Analyses in
        the Mechanical APDL Theory Reference.

        This command is ignored if the HROPT command has been issued with
        Method = VT or Method = VTRU.

        This command is also valid in PREP7.
        """
        command = f"HREXP,{angle}"
        return self.run(command, **kwargs)

    def hrocean(self, type_="", nphase="", **kwargs):
        """Perform the harmonic ocean wave procedure (HOWP).

        APDL Command: HROCEAN

        Parameters
        ----------
        type\_
            Specifies how to include ocean wave information in a harmonic
            analysis:

            HARMONIC - Performs a harmonic analysis using both real and imaginary load vectors
                       calculated via the harmonic ocean wave procedure (HOWP).
                       This behavior is the default. This option performs a
                       harmonic analysis running at a frequency determined by
                       the wave period (specified via OCTABLE command input).

            STATIC - Performs a static analysis using both real and imaginary load vectors
                     (calculated via HOWP). This option works by performing a
                     harmonic analysis running at a frequency of 0.0.

            OFF - Deactivates a previously activated HOWP and performs a standard harmonic
                  analysis.

        nphase
            Positive number specifying the number of phases to calculate
            forces. This value must be at least 8. The default value is 20.

        Notes
        -----
        The HROCEAN command applies ocean wave information (obtained via the
        OCDATA and OCTABLE commands) in a harmonic analysis (ANTYPE,HARMIC) as
        real and imaginary forces.

        You can apply only one ocean load at a time.

        The applied frequency in the harmonic (Type = HARMONIC) analysis is
        based on the wave period input on the OCTABLE command (and not on
        HARFRQ command input, which cannot be used). Phase-shift input on the
        OCTABLE command is ignored.

        HOWP does not generate a damping matrix. If you require a damping
        matrix, you must add it separately.

        The command applies to regular wave types only (Airy with one wave
        component, Wheeler with one wave component, Stokes, and stream
        function). Irregular wave types are not supported. For information
        about wave types, see Hydrodynamic Loads in the Mechanical APDL Theory
        Reference.

        The program calculates the forces on each load component of each
        element at NPHASE solutions, spread evenly over one wave cycle. Then,
        the minimum and maximum, and the phase between them, are calculated.
        The command uses the resulting information to generate the real and
        imaginary loads.

        HOWP cannot be used with stress stiffening.

        HOWP works with the full harmonic analysis method (HROPT,FULL) only.

        For more information, see Harmonic Ocean Wave Procedure (HOWP) in the
        Mechanical APDL Theory Reference.

        This command is also valid in PREP7.
        """
        command = f"HROCEAN,{type_},{nphase}"
        return self.run(command, **kwargs)

    def hropt(self, method="", maxmode="", minmode="", mcout="", damp="", **kwargs):
        """Specifies harmonic analysis options.

        APDL Command: HROPT

        Parameters
        ----------
        method
            Solution method for the harmonic analysis:

            AUTO - Automatically select the most efficient method. Either the FULL method or the
                   Variational Technology method is selected depending on the
                   model. (default method).

            FULL - Full method.

            MSUP - Mode-superposition method.

            VT - Variational Technology method (based on FULL harmonic algorithm).

            VTPA - Variational Technology perfect absorber method (based on FULL harmonic
                   algorithm).

            VTRU - Variational Technology reuse method (based on FULL harmonic algorithm).

        maxmode
            Largest mode number to be used to calculate the response (for
            Method = MSUP only).  Defaults to the highest mode calculated in
            the preceding modal analysis.

        minmode
            Smallest mode number to be used (for Method = MSUP only).  Defaults
            to 1.

        mcout
            Modal coordinates output key (valid only for the mode superposition
            method MSUP):

            NO - No output of modal coordinates (default).

            YES - Output modal coordinates to the text file jobname.MCF.

        damp
            Damping mode for frequency-dependent material properties (valid
            only for the Variational Technology Method VT).

            Hysteretic - Not proportional to the frequency.

            Viscous - Proportional to the frequency (default).

        Notes
        -----
        Specifies the method of solution for a harmonic analysis
        (ANTYPE,HARMIC).  If used in SOLUTION, this command is valid only
        within the first load step. See the product restrictions indicated
        below.

        For cyclic symmetry mode-superposition harmonic solutions, MAXMODE and
        MINMODE are ignored.

        To include residual vectors in your mode-superposition harmonic
        analysis, specify RESVEC,ON.

        This command is also valid in PREP7.

        Distributed ANSYS Restriction: The VTRU method is not supported.
        """
        command = f"HROPT,{method},{maxmode},{minmode},{mcout},{damp}"
        return self.run(command, **kwargs)

    def hrout(self, reimky="", clust="", mcont="", **kwargs):
        """Specifies the harmonic analysis output options.

        APDL Command: HROUT

        Parameters
        ----------
        reimky
            Real/Imaginary print key:

            ON - Print complex displacements as real and imaginary components (default).

            OFF - Print complex displacements as amplitude and phase angle (degrees).

        clust
            Cluster option (for HROPT,MSUP):

            OFF - Uniform spacing of frequency solutions (default).

            ON - Cluster frequency solutions about natural frequencies.

        mcont
            Mode contributions key (for HROPT,MSUP):

            OFF - No print of mode contributions at each frequency (default).

            ON - Print mode contributions at each frequency.

        Notes
        -----
        Specifies the harmonic analysis (ANTYPE,HARMIC) output options.  If
        used in SOLUTION, this command is valid only within the first load
        step. OUTPR,NSOL must be specified to print mode contributions at each
        frequency.

        This command is ignored if the HROPT command has been issued with
        Method = VT, VTPA, or VTRU. Displacements are not available at expanded
        frequencies with these solution methods.

        For cyclic symmetry mode-superposition harmonic solutions, the cluster
        option is not available.

        This command is also valid in PREP7.
        """
        command = f"HROUT,{reimky},{clust},{mcont}"
        return self.run(command, **kwargs)

    def lvscale(self, fact="", ldstep="", **kwargs):
        """Scales the load vector for mode-superposition analyses.

        APDL Command: LVSCALE

        Parameters
        ----------
        fact
            Scale factor applied to both the real and imaginary (if they exist)
            components of the load vector. Defaults to 0.0.

        ldstep
            Specifies the load step number from the modal analysis
            (MODCONT,ON). It corresponds to the load vector number. Defaults to
            1. The maximum value is 240.

        Notes
        -----
        Specifies the scale factor for the load vector that was created in a
        modal (ANTYPE,MODAL) analysis.  Applies only to the mode-superposition
        transient analysis (ANTYPE,TRANS), mode-superposition harmonic analysis
        (ANTYPE,HARMIC), random vibration analysis (ANTYPE,SPECTR with
        SPOPT,PSD), and multiple point response spectrum analysis
        (ANTYPE,SPECTR with SPOPT,MPRS).  For PSD and MPRS analyses, LVSCALE is
        only applicable for pressure loading.

        The LVSCALE command supports tabular boundary conditions (%TABNAME_X%)
        for FACT input values only as a function of time in the mode-
        superposition transient (ANTYPE,TRANS) or as a function of frequency in
        mode-superposition harmonic (ANTYPE,HARMIC).

        MPC contact generates constraint equations that can include constant
        terms (included on the right-hand side of the system equation). The
        LVSCALE command scales the constant terms.

        In mode-superposition transient and harmonic analyses, all of the load
        vectors need to be scaled in the first load step. Use a zero scale
        factor if they are not actually used in this first load step. :
        Similarly, in random vibration and multipoint response spectrum
        analyses, all of the load vectors need to be scaled in the first
        participation factor calculation (PFACT). : Use a zero scale factor if
        they are not actually used for the first input table.

        This command is also valid in PREP7.
        """
        command = f"LVSCALE,{fact},{ldstep}"
        return self.run(command, **kwargs)

    def mascale(self, massfact="", **kwargs):
        """Activates scaling of the entire system matrix.

        APDL Command: MASCALE

        Parameters
        ----------
        massfact
           Scaling factor (> 0) for the mass matrix. Default = 1.0.

        Notes
        -----
        This command is supported in the first load step of the analysis only.
        The following features are not affected by the scaling:

        * Ocean loading
        * Steady-state rolling SSTATE

        The mass-related information (mass, center of mass, and mass
        moments of inertia) printed in the mass summary is based on
        unscaled mass properties.
        """
        return self.run(f"MASCALE,{massfact}", **kwargs)

    def mdamp(self, stloc="", v1="", v2="", v3="", v4="", v5="", v6="", **kwargs):
        """Defines the damping ratios as a function of mode.

        APDL Command: MDAMP

        Parameters
        ----------
        stloc
            Starting location in table for entering data.  For example, if
            STLOC = 1, data input in the V1 field applies to the first constant
            in the table.  If STLOC = 7, data input in the V1 field applies to
            the seventh constant in the table, etc.  Defaults to the last
            location filled + 1.

        v1, v2, v3, . . . , v6
            Data assigned to six locations starting with STLOC.  If a value is
            already in this location, it will be redefined.  Blank values for
            V2 to V6 leave the corresponding previous value unchanged.

        Notes
        -----
        Defines the damping ratios as a function of mode.  Table position
        corresponds to mode number.  These ratios are added to the DMPRAT
        value, if defined.  Use STAT command to list current values.  Applies
        to the mode-superposition harmonic (ANTYPE,HARMIC), the mode-
        superposition linear transient dynamic (ANTYPE,TRANS), and the spectrum
        (ANTYPE,SPECTR) analyses.  Repeat MDAMP command for additional
        constants (10000 maximum).

        MDAMP can also be defined in a substructure analysis using component
        mode synthesis with fixed-interface method (ANTYPE,SUBSTR with
        CMSOPT,FIX and SEOPT,,,3). The damping ratios are added to the diagonal
        of the reduced damping matrix as explained in Component Mode Synthesis
        (CMS).

        This command is also valid in PREP7.
        """
        command = f"MDAMP,{stloc},{v1},{v2},{v3},{v4},{v5},{v6}"
        return self.run(command, **kwargs)

    def mdplot(self, function="", dmpname="", scale="", **kwargs):
        """Plots frequency-dependent modal damping coefficients calculated by

        APDL Command: MDPLOT
        DMPEXT.

        Parameters
        ----------
        function
            Function to display.

            d_coeff - Damping coefficient

            s_coeff - Squeeze coefficient

            d_ratio - Damping ratio

            s_ratio - Squeeze stiffness ratio

        dmpname
            Array parameter name where damping information is stored. Defaults
            to d_damp.

        scale
            Indicates whether to perform a linear or a double logarithmic plot.

            LIN - Perform a linear plot. Default

            LOG - Perform a double logarithmic plot.

        Notes
        -----
        See Thin Film Analysis for more information on thin film analyses.
        """
        command = f"MDPLOT,{function},{dmpname},{scale}"
        return self.run(command, **kwargs)

    def midtol(self, key="", tolerb="", resfq="", **kwargs):
        """Sets midstep residual criterion values for structural transient

        APDL Command: MIDTOL
        analyses.

        Parameters
        ----------
        key
            Midstep residual criterion activation key.

            ON or 1 - Activate midstep residual criterion in a structural transient analysis
                      (default).

            OFF or 0 - Deactivate midstep residual criterion in a structural transient analysis.

            STAT  - List the current midstep residual criterion setting.

        tolerb
            Midstep residual tolerance or reference value for bisection.
            Defaults to 100 times the TOLER setting of the CNVTOL command.

        resfq
            Key to use response frequency computation along with midstep
            residual criterion for automatic time stepping (AUTOTS,ON).

            OFF or 0 - Do not calculate response frequency and do not consider it in the automatic
                       time stepping (default).

            ON or 1 - Calculate response frequency and consider it in the automatic time stepping.

        Notes
        -----
        When TOLERB is input as a tolerance value (TOLERB > 0), the typical
        force and/or moment from the regular time step is used in the midstep
        residual force and/or moment comparison.

        In a structural transient analysis, the suggested tolerance range of
        TOLERB (TOLERB > 0) is as follows:

        If the structural transient analysis is elastic and linear, and the
        load is constant or changes slowly, use a smaller value of TOLERB to
        achieve an accurate solution. If the analysis involves large amounts of
        energy dissipation, such as elastic-plastic material, TOLERB can be
        larger. If the analysis includes contact or rapidly varying loads, a
        smaller value of TOLERB should be used if high frequency response is
        important; otherwise, a larger value of TOLERB may be used to enable
        faster convergence with larger time step sizes.

        For more information on how the midstep criterion is used by the
        program, see Midstep Residual for Structural Dynamic Analysis in the
        Mechanical APDL Theory Reference.

        This command is also valid in PREP7.
        """
        command = f"MIDTOL,{key},{tolerb},{resfq}"
        return self.run(command, **kwargs)

    def modcont(self, mlskey="", enforcedkey="", **kwargs):
        """Specify additional modal analysis options.

        APDL Command: MODCONT

        Parameters
        ----------
        mlskey
            Multiple load step key:

            OFF - Perform the modal analysis (compute the eigenvalues and the load vector) for
                  each load step. (default)

            ON - Perform the modal analysis (compute the eigenvalues and the load vector) only
                 for the first load step; form the load vector for each
                 subsequent load step (without repeating the eigenvalue
                 calculations) and write all load vectors to the Jobname.MODE
                 file for downstream mode-superposition analyses.

        enforcedkey
            Enforced motion key:

            OFF - Do not calculate enforced static modes. (default)

            ON - Calculate enforced static modes and write them to the Jobname.MODE file.

        Notes
        -----
        Specifies additional modal analysis (ANTYPE,MODAL) options.

        Use the LVSCALE command to apply the desired load in a mode-
        superposition transient or harmonic analysis.

        The maximum number of load vectors that can be used in the downstream
        mode-superposition transient or harmonic analysis is: 240.

        Generation of multiple loads (MLSkey = ON) is supported by the Block
        Lanczos, PCG Lanczos, Supernode, Subspace, Unsymmetric, and QR damped
        modal methods.

        The enforced motion calculation (EnforcedKey = ON) is supported by the
        Block Lanczos and Supernode mode extraction methods.
        """
        command = f"MODCONT,{mlskey},{enforcedkey}"
        return self.run(command, **kwargs)

    def modseloption(
        self, dir1="", dir2="", dir3="", dir4="", dir5="", dir6="", **kwargs
    ):
        """APDL Command: MODSELOPTION

        Parameters
        ----------
        dir1, dir2, dir3, dir4, dir5, dir6
            Selection of the direction to be expanded.

            For ``modeselmethod=effm`` on the MXPAND command, the
            directions correspond to the global Cartesian directions,
            i.e. 1=X, 2=Y, 3=Z, 4=ROTX, 5=ROTY, and 6=ROTZ. If dir1 = YES,
            then any mode in this direction is expanded if its modal
            effective mass divided by the total mass (modal effective mass
            ratio) is greater than SIGNIF on the MXPAND command. If
            dir1=NO, then the specified direction is not considered as a
            criterion for expansion. If dir1 is given a numerical decimal
            value, modes in that direction are selected (starting from the
            ones with the largest modal effective mass ratios to the
            smallest) until the sum of their modal effective mass ratio
            equals this requested threshold.

            For ModeSelMethod = MODC on the MXPAND command, dir1
            corresponds to the first input spectrum, dir2 to the second,
            etc. (i.e. for multiple spectrum inputs; the actual directions
            correspond to their respective SED directions). If dir1=YES,
            then any mode in this spectrum is ex- panded if its mode
            coefficient divided by the largest mode coefficient is greater
            than SIGNIF on the MXPAND command. If dir1=NO, then the
            specified direction is not considered as a criterion for
            expansion.

        Notes
        -----
        This command is only applicable when a mode selection method is defined
        (ModeSelMethod on the MXPAND command). See Using Mode Selection in the
        Mechanical APDL Structural Analysis Guide for more details.

        If a numerical value is specified for a direction, the significance
        threshold (SIGNIF on the MXPAND command) is ignored for the selection
        of the modes in this direction.

        If a mode is determined to be expanded in any of the 6 directions, it
        will be expanded in the .MODE file. : Otherwise, the mode will not be
        expanded.

        The default behavior is to consider all directions for expansion.
        """
        command = f"MODSELOPTION,{dir1},{dir2},{dir3},{dir4},{dir5},{dir6}"
        return self.run(command, **kwargs)

    def modopt(
        self,
        method="",
        nmode="",
        freqb="",
        freqe="",
        cpxmod="",
        nrmkey="",
        modtype="",
        blocksize="",
        freqmod="",
        **kwargs,
    ):
        """Specifies modal analysis options.

        APDL Command: MODOPT

        Parameters
        ----------
        method
            Mode-extraction method to be used for the modal analysis.

            LANB - Block Lanczos

            LANPCG - PCG Lanczos

            SNODE - Supernode modal solver

            SUBSP - Subspace algorithm

            UNSYM - Unsymmetric matrix

            DAMP - Damped system

            QRDAMP - Damped system using QR algorithm

            VT - Variational Technology

        nmode
            The number of modes to extract. The value can depend on the value
            supplied for Method. NMODE has no default and must be specified. If
            Method = LANB, LANPCG, or SNODE, the number of modes that can be
            extracted can equal the DOFs in the model after the application of
            all boundary conditions.

        freqb
            The beginning, or lower end, of the frequency range of interest.

        freqe
            The ending, or upper end, of the frequency range of interest (in
            Hz). The default for Method = SNODE is described below. The default
            for all other methods is to calculate all modes, regardless of
            their maximum frequency.

        cpxmod
            Complex eigenmode key. (Valid only when Method = QRDAMP or Method =
            UNSYM).

            AUTO - Determine automatically if the eigensolutions are real or complex and output
                   them accordingly. This is the default for Method = UNSYM.
                   Not supported for Method = QRDAMP.

            ON or CPLX - Calculate and output complex eigenmode shapes.

            OFF or REAL - Do not calculate complex eigenmode shapes. This is required if a mode-
                          superposition analysis is intended after the modal
                          analysis for Method = QRDAMP. This is the default for
                          this method.

        nrmkey
            Mode shape normalization key:

            OFF - Normalize the mode shapes to the mass matrix (default).

            ON - Normalize the mode shapes to unity instead of to the mass matrix.  If a
                 subsequent spectrum or mode-superposition analysis is planned,
                 the mode shapes should be normalized to the mass matrix
                 (Nrmkey = OFF).

        modtype
            Type of modes calculated by the eigensolver. Only applicable to the
            unsymmetric eigensolver.

            Blank - Right eigenmodes. This value is the default.

            BOTH - Right and left eigenmodes. The left eigenmodes are written to Jobname.LMODE.
                   This option must be activated if a mode-superposition
                   analysis is intended.

        blocksize
            The block vector size to be used with the Block Lanczos or
            Subspace eigensolver (used only when Method = LANB or
            SUBSP). BlockSize must be an integer value between 0 and
            16. When BlockSize = zero or blank, the code decides the
            block size internally (normally, a value of 8 is used for
            LANB and a value of 6 is used for SUBSP).  Typically,
            higher BlockSize values are more efficient under each of
            the following conditions:

            - When running in out-of-core mode and there is not enough
              physical memory to buffer all of the files written by
              the Block Lanczos or Subspace eigensolver (and thus, the
              time spent doing I/O is considerable).
            - Many modes are requested (>100).
            - Higher-order solid elements dominate the model.

            The memory usage only slightly increases as BlockSize is
            increased. It is recommended that you use a value
            divisible by 4 (4, 8, 12, or 16).

        freqmod
            The specified frequency when the solved eigenvalues are no
            longer frequencies (for example, the model has the Floquet
            periodic boundary condition). In a modal analysis, the
            Floquet periodic boundary condition (body load FPBC) is
            only valid for the acoustic elements FLUID30, FLUID220,
            and FLUID221.

        Notes
        -----
        Specifies modal analysis (ANTYPE,MODAL) options. Additional options
        used only for the Supernode (SNODE) eigensolver are specified by the
        SNOPTION command. Additional options used only for the Subspace (SUBSP)
        eigensolver are specified by the SUBOPT command. If Method = LANPCG,
        ANSYS automatically switches to the PCG solver internally for this
        modal analysis. You can further control the efficiency of the PCG
        solver with the PCGOPT and EQSLV commands.

        For models that involve a non-symmetric element stiffness matrix, as in
        the case of a contact element with frictional contact, the QRDAMP
        eigensolver (MODOPT, QRDAMP) extracts modes in the modal subspace
        formed by the eigenmodes from the symmetrized eigenproblem. The QRDAMP
        eigensolver symmetrizes the element stiffness matrix on the first pass
        of the eigensolution, and in the second pass, eigenmodes are extracted
        in the modal subspace of the first eigensolution pass. For such non-
        symmetric eigenproblems, you should verify the eigenvalue and eigenmode
        results using the non-symmetric matrix eigensolver  (MODOPT,UNSYM).

        The DAMP and QRDAMP options cannot be followed by a subsequent spectrum
        analysis. The UNSYM method supports spectrum analysis when
        eigensolutions are real.

        This command is also valid in PREP7.

        Distributed ANSYS Restriction: The VT extraction method is not
        supported in Distributed ANSYS. All other extraction methods are
        supported. However, PCG Lanczos, SUBSP, UNSYM, DAMP, and QRDAMP are the
        only distributed eigensolvers that will run a fully distributed
        solution. The Block Lanczos and Supernode eigensolvers are not
        distributed eigensolvers; therefore, you will not see the full
        performance improvements with these methods that you would with a fully
        distributed solution.
        """
        command = f"MODOPT,{method},{nmode},{freqb},{freqe},{cpxmod},{nrmkey},{modtype},{blocksize},,,,{freqmod}"
        return self.run(command, **kwargs)

    def mxpand(
        self,
        nmode="",
        freqb="",
        freqe="",
        elcalc="",
        signif="",
        msupkey="",
        modeselmethod="",
        **kwargs,
    ):
        """Specifies the number of modes to expand and write for a modal or

        APDL Command: MXPAND
        buckling analysis.

        Parameters
        ----------
        nmode
            Number of modes or array name (enclosed in percent signs) to expand
            and write. If blank or ALL, expand and write all modes within the
            frequency range specified. If -1, do not expand and do not write
            modes to the results file during the analysis. If an array name is
            input, the array must contain 1 for the expanded modes and zero
            otherwise, where the array index corresponds to the mode number. To
            specify an array containing the individual modes to expand, enclose
            the array name in percent (%) signs (for example,
            MXPAND,%arrname%). Use the ``*DIM`` command to define the array.

        freqb
            Beginning, or lower end, of frequency range of interest. If FREQB
            and FREQE are both blank, expand and write the number of modes
            specified without regard to the frequency range. Defaults to the
            entire range.

        freqe
            Ending, or upper end, of frequency range of interest.

        elcalc
            Element calculation key:

            NO - Do not calculate element results, reaction forces, and energies (default).

            YES - Calculate element results, reaction forces, energies, and the nodal degree of
                  freedom solution.

        signif
            Expand only those modes whose significance level exceeds the SIGNIF
            threshold (only applicable when ModeSelMethod is defined).

        msupkey
            Element result superposition key:

            NO - Do not write element results to the mode file Jobname.MODE.

            YES - Write element result to the mode file for use in the expansion pass of a
                  subsequent mode-superposition PSD, transient, or harmonic
                  analysis (default if Elcalc = YES and the mode shapes are
                  normalized to the mass matrix).

        modeselmethod
            Methods for mode selection (not supported for complex
            eigensolvers):

            blank - No mode selection is performed (default).

            MODM - The mode selection is based on the modal effective masses.

            MODC - The mode selection is based on the mode coefficients.

            DDAM - The mode selection is based on DDAM procedure (see Mode Selection Based on DDAM
                   Procedure in the Mechanical APDL Structural Analysis Guide
                   for more information). This option is applicable only to
                   DDAM spectrum analysis.

        Notes
        -----
        Specifies the number of modes to expand and write over a frequency
        range for a modal (ANTYPE,MODAL) or buckling (ANTYPE,BUCKLE) analysis.
        If used in SOLUTION, this command is valid only within the first load
        step.

        There is no limit on the number of expanded modes (NMODE). However,
        there is a limit on the maximum number of modes used via the ``*GET,,MODE``
        command, mode combinations, and the MDAMP command.

        With MSUPkey = YES, the computed element results (Elcalc = YES) are
        written to Jobname.MODE for use in subsequent downstream mode-
        superposition analyses, including harmonic, transient, and PSD
        analyses. This significantly reduces computation time for the
        combination or expansion passes. For limitations, see Option: Number of
        Modes to Expand (MXPAND) in the Mechanical APDL Structural Analysis
        Guide.

        If a mode selection method (ModeSelMethod) is defined, only the
        selected modes will be expanded. See Using Mode Selection in the
        Mechanical APDL Structural Analysis Guide for more details about the
        procedure.

        For array input (NMODE), the array must be dimensioned to be the size
        of the number of modes extracted (NMODE on the MODOPT command). A value
        of 1 in the array indicates the mode is to be expanded, and a value of
        0 indicates not to expand the mode. For the DAMP modal solution, the
        modes are in pairs, so be sure to verify that both modes of a pair have
        the same value. (For example, if modes #3 and #4 are a pair, indices 3
        and 4 in the array should have the same value, 0 or 1.)

        For linear perturbation modal analyses, you must set both Elcalc and
        MSUPkey to YES so that the downstream stress expansion pass can produce
        a solution consistent with the linear or nonlinear base (static or full
        transient) analysis. The prestressed nonlinear element history (saved
        variables) is accessible only in the first and second phases of the
        linear perturbation. The downstream MSUP or PSD analysis can only reuse
        the nonlinear information contained in the Jobname.MODE file that is
        generated in the linear perturbation.

        In a Distributed ANSYS analysis, you must issue MXPAND to specify the
        number of modes to expand when computing the modes and mode shapes. In
        a Distributed ANSYS run, MXPAND cannot be issued in an expansion pass
        (EXPASS).

        This command is also valid in PREP7.
        """
        command = f"MXPAND,{nmode},{freqb},{freqe},{elcalc},{signif},{msupkey},{modeselmethod}"
        return self.run(command, **kwargs)

    def qrdopt(self, reusekey="", symmeth="", cmccoutkey="", **kwargs):
        """Specifies additional QRDAMP modal analysis options.

        APDL Command: QRDOPT

        Parameters
        ----------
        reusekey
            Reuse key for method=QRDAMP specified in MODOPT command.

            ON - Reuse the symmetric eigensolution from the previous
                 load steps or from the previous solution.

            OFF - Do not reuse (calculates symmetric eigensolution at
                  current load step). This is the default.

        symmeth
            Mode-extraction method to be used for the symmetric eigenvalue
            problem.

            LANB - Block Lanczos (default for shared-memory parallel processing).

            SUBSP - Subspace algorithm (default for distributed-memory
                    parallel processing).

        cmccoutkey
            Complex Modal Contribution Coefficients (CMCC) output
            key. See Calculate the Complex Mode Contribution
            Coefficients (CMCC) in the Structural Analysis Guide for
            details and usage.

            ON - Output the CMCC to the text file Jobname.CMCC.

            OFF - Do not output the CMCC. This is the default.

        Notes
        -----
        If the filename.modesym file exists in the working directory
        and ReuseKey = ON, filename.modesym will be reused. If
        filename.modesym does not exist in the working directory, the
        symmetric eigensolution will be calculated.

        When ReuseKey=ON, both the new modal analysis
        (filename.modesym usage) and the preceding modal analysis
        (filename.modesym generation) must be performed using the same
        product version number.

        The mode-extraction method changes depending on the type of
        parallelism involved. For performance reasons, the subspace
        method is used with distributed-memory parallel processing
        (Distributed ANSYS) runs, while the Block Lanczos method is
        used with shared-memory parallel processing runs.
        """
        return self.run(f"QRDOPT,{reusekey},,,{symmeth},{cmccoutkey}", **kwargs)

    def rigid(self, dof1="", dof2="", dof3="", dof4="", dof5="", dof6="", **kwargs):
        """Specifies known rigid body modes (if any) of the model.

        APDL Command: RIGID

        Parameters
        ----------
        dof1, dof2, dof3, . . . , dof6
            Up to six global Cartesian directions of the rigid modes.
            For a completely free 2-D model, use ALL or UX, UY, ROTZ.
            For a completely free 3-D model, use ALL or UX, UY, UZ,
            ROTX, ROTY, ROTZ.  For a constrained model, use UX, UY,
            UZ, ROTX, ROTY, or ROTZ, as appropriate, to specify each
            and every unconstrained direction which exists in the
            model (not specifying every direction may cause
            difficulties in extracting the modes).

        Notes
        -----
        Specifies known rigid body modes (if any) of the model.  This
        command applies only to a component mode synthesis (CMS)
        analysis (see the CMSOPT command).  Any rigid body modes
        specified must be permitted by the applied displacement
        constraints (i.e., do not specify a rigid body mode in a
        constrained direction).  Reissue the command to redefine the
        specification.  If used in SOLUTION, this command is valid
        only within the first load step.

        This command is also valid in PREP7.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"RIGID,{dof1},{dof2},{dof3},{dof4},{dof5},{dof6}"
        return self.run(command, **kwargs)

    def subopt(self, option="", value1="", **kwargs):
        """Specifies Subspace (SUBSP) eigensolver options.

        APDL Command: SUBOPT

        Parameters
        ----------
        option
            One of the following options:

            STRMCK - Controls whether a Sturm sequence check is performed.

            Value1: - OFF

            Do not perform Sturm sequence check (default). - ON

            Perform Sturm sequence check. - MEMORY

            Controls the memory allocation strategy for the Subspace eigensolver. - Value1:

            AUTO - Use the default memory allocation strategy (default).

            INCORE - Force the Subspace eigensolver to allocate in-core memory.

            OUTOFCORE - Force the Subspace eigensolver to use scratch files.

        Notes
        -----
        SUBOPT specifies options to be used with the Subspace eigensolver
        (MODOPT,SUBSP) during a modal analysis.
        """
        command = f"SUBOPT,{option},{value1}"
        return self.run(command, **kwargs)

    def timint(self, key="", lab="", **kwargs):
        """Turns on transient effects.

        APDL Command: TIMINT

        Parameters
        ----------
        key
            Transient effects key:

            OFF - No transient effects (static or steady-state).

            ON - Include transient (mass or inertia) effects.

        lab
            Degree of freedom label:

            ALL - Apply this key to all appropriate labels (default).

            STRUC - Apply this key to structural DOFs.

            THERM - Apply this key to thermal DOFs.

            ELECT - Apply this key to electric DOFs.

            MAG - Apply this key to magnetic DOFs.

            FLUID - Apply this key to fluid DOFs.

            DIFFU - Apply this key to concentration of DOFs.

        Notes
        -----
        Indicates whether this load step in a full transient analysis should
        use time integration, that is, whether it includes transient effects
        (e.g. structural inertia, thermal capacitance) or whether it is a
        static (steady-state) load step for the indicated DOFs.  Transient
        initial conditions are introduced at the load step having Key = ON.
        Initial conditions are then determined from the previous two substeps.
        Zero initial velocity and acceleration are assumed if no previous
        substeps exist.  See the Structural Analysis Guide, the Thermal
        Analysis Guide, and the Low-Frequency Electromagnetic Analysis Guide
        for details.

        This command is also valid in PREP7.
        """
        command = f"TIMINT,{key},{lab}"
        return self.run(command, **kwargs)

    def tintp(
        self,
        gamma="",
        alpha="",
        delta="",
        theta="",
        oslm="",
        tol="",
        avsmooth="",
        alphaf="",
        alpham="",
        **kwargs,
    ):
        """Defines transient integration parameters.

        APDL Command: TINTP

        Parameters
        ----------
        gamma
            Amplitude decay factor for 2nd order transient integration, e.g.,
            structural dynamics (used only if ALPHA, DELTA, ALPHAF, and ALPHAM
            are blank).  Defaults to 0.005.

        alpha
            2nd order transient integration parameter (used only if GAMMA is
            blank).  Defaults to 0.2525.

        delta
            2nd order transient integration parameter (used only if GAMMA is
            blank).  Defaults to 0.5050.

        theta
            1st order transient (e.g., thermal transient) integration
            parameter.  Defaults to 1.0.

        oslm
            Specifies the oscillation limit criterion for automatic time
            stepping of 1st order transients (e.g., thermal transients).
            Defaults to 0.5 with a tolerance of TOL.

        tol
            Tolerance applied to OSLM.  Defaults to 0.0.

        avsmooth
            Smoothing flag option:

            0 - Include smoothing of the velocity (1st order system)
                or the acceleration (2nd order system) (default).

            1 - Do not include smoothing.

        alphaf
            Interpolation factor in HHT algorithm for force and damping terms
            (used only if GAMMA is blank). Defaults to 0.005.

        alpham
            Interpolation factor in HHT algorithm for inertial term (used only
            if GAMMA is blank). Defaults to 0.0.

        Notes
        -----
        Used to define the transient integration parameters.  For more
        information on transient integration parameters, refer to the
        Mechanical APDL Theory Reference.

        For structural transient analyses, you may choose between the
        Newmark and HHT time integration methods (see the TRNOPT
        command). In this case, if GAMMA is input and the integration
        parameters ALPHA, DELTA, ALPHAF, and ALPHAM are left blank,
        the program will calculate the integration
        parameters. Alternatively, you can input these integration
        parameters directly on this command. However, for the
        unconditional stability and second order accuracy of the time
        integration, these parameters should satisfy a specific
        relationship, as described in Description of Structural and
        Other Second Order Systems of the Mechanical APDL Theory
        Reference.

        In a transient piezoelectric analysis, required input for this
        command is ALPHA = 0.25, DELTA = 0.5, and THETA = 0.5.  For a
        coupled electromagnetic-circuit transient analysis, use THETA
        = 1.0, the default value, to specify the backward Euler
        method.

        This command is also valid in PREP7.
        """
        command = f"TINTP,{gamma},{alpha},{delta},{theta},{oslm},{tol},,,{avsmooth},{alphaf},{alpham}"
        return self.run(command, **kwargs)

    def trnopt(
        self,
        method="",
        maxmode="",
        minmode="",
        mcfwrite="",
        tintopt="",
        vaout="",
        dmpsfreq="",
        engcalc="",
        mckey="",
        **kwargs,
    ):
        """Specifies transient analysis options.

        APDL Command: TRNOPT

        Parameters
        ----------
        method
            Solution method for the transient analysis:

            FULL - Full method (default).

            MSUP - Mode-superposition method.

            VT - Variational Technology method.  (Removed by V18.2)

        maxmode
            Largest mode number to be used to calculate the response
            (for Method = MSUP).  Defaults to the highest mode
            calculated in the preceding modal analysis.

        minmode
            Smallest mode number to be used (for Method = MSUP).
            Defaults to 1.

        mcfwrite
            Modal coordinates output key to the .mcf file (valid only
            for the mode-superposition method):

            NO - No output of modal coordinates (default).

            YES - Output modal coordinates to the text file Jobname.MCF.

        tintopt
            Time integration method for the transient analysis:

            NMK or 0 - Newmark algorithm (default).

            HHT or 1 - HHT algorithm (valid only for the full transient method).

        vaout
            Velocities and accelerations output key (valid only for
            mode- superposition transient analysis):

            NO - No output of velocities and accelerations (default).

            YES - Write velocities and accelerations on the reduced displacement file
                  Jobname.RDSP.

        dmpsfreq
            Average excitation frequency (Hz) for the calculation of
            equivalent viscous damping from structural damping input
            (DMPSTR and MP,DMPS). See Damping for more
            details. Defaults to zero. If an excitation frequency is
            not specified, structural damping is ignored. If tabular
            excitation frequency data is provided in a full transient
            analysis (DMPSFreqTab on DMPSTR), it supersedes this
            value.

        engcalc
            Additional element energies calculation key:

            NO - Do not calculate additional element energies
            (default).

            YES - Calculate damping energy and work done by external
            loads.

        mckey
            Modal coordinates output key to the .rdsp file (valid only
            for the mode-superposition method):

            AUTO - Writing depends on the modal analysis settings of
            the MXPAND command (default).

            YES - Always write the modal coordinates to the file
            Jobname.rdsp. A subsequent expansion pass (EXPASS) is not
            supported.

        Notes
        -----
        Specifies transient analysis (ANTYPE,TRANS) options. If used
        in SOLUTION, this command is valid only within the first load
        step. Use the TINTP command to set transient integration
        parameters.

        To include residual vectors in your mode-superposition
        transient analysis (Method = MSUP), specify RESVEC,ON.

        Method = MSUP is not available for ocean loading.

        By default in a mode-superposition transient analysis,
        reaction force and other force output contains only static
        contributions. If you want to postprocess the velocities,
        accelerations, and derived results (Lab = TOTAL, DAMP, or
        INERT on the FORCE command), set VAout = YES to activate
        velocity and acceleration output.

        The calculation of additional energies (EngCalc = YES) is
        valid only for the full solution method (Method = FULL). The
        Jobname.ESAV file is always saved in this case. The numerical
        integration for damping energy and work are consistent only if
        solution data are written to the database for every substep
        (OUTRES,ALL,ALL, OUTRES,ESOL,ALL, or OUTRES,VENG, ALL). For
        more information, see Damping Energy and Work Done by External
        Loads in the Mechanical APDL Theory Reference.

        This command is also valid in PREP7.
        """
        command = f"TRNOPT,{method},{maxmode},,{minmode},{mcfwrite},{tintopt},{vaout},{dmpsfreq},{engcalc},{mckey}"
        return self.run(command, **kwargs)
