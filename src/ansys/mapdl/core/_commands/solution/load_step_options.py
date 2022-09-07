class LoadStepOptions:
    def autots(self, key="", **kwargs):
        """Specifies whether to use automatic time stepping or load stepping.

        APDL Command: AUTOTS

        Parameters
        ----------
        key
            Automatic time stepping key:

            OFF
                Do not use automatic time stepping.

            ON
                Use automatic time stepping (default).

            AUTO
                The program determines whether to use automatic time stepping (used by
                Workbench).

        Notes
        -----
        Specifies whether to use automatic time stepping (or load stepping)
        over this load step. If Key = ON, both time step prediction and time
        step bisection will be used.

        You cannot use automatic time stepping ``AUTOTS``, line search ``LNSRCH``,
        or the DOF solution predictor [PRED] with the arc-length method
        ``ARCLEN, ARCTRM``. If you activate the arc-length method after you set
        ``AUTOTS, LNSRCH``, or ``PRED``, a warning message appears. If you choose to
        proceed with the arc-length method, the program disables your automatic
        time stepping, line search, and DOF predictor settings, and the time
        step size is controlled by the arc-length method internally.

        This command is also valid in PREP7.
        """
        command = f"AUTOTS,{key}"
        return self.run(command, **kwargs)

    def campbell(self, action="", **kwargs):
        """Prepares the result file for a subsequent Campbell diagram of a

        APDL Command: CAMPBELL
        prestressed structure.

        Parameters
        ----------
        action
            Campbell action:

            NONE - Do not prepare the result file. This option is the default behavior.

            RSTP - Prepare the result file (Jobname.RSTP) for a subsequent Campbell diagram of a
                   prestressed structure.

        Notes
        -----
        For an analysis involving a prestressed structure, the ``CAMPBELL`` command
        specifies whether or not to prepare the result file to support  a
        Campbell diagram analysis (``PRCAMP`` or ``PLCAMP``).

        To prestress a structure, the program performs a static solution before
        the linear perturbation modal solution.

        The CAMPBELL command requires that modal and static analyses be
        performed alternately. It works only when the number of static analyses
        is the same as the number of modal analyses. Any number of analyses can
        be performed, but the same number of each (static and modal) is
        expected. The modal solutions are appended in the results file
        (Jobname.RSTP).

        For an example of PLCAMP command usage, see Example Campbell Diagram
        Analysis in the Advanced Analysis Guide.
        """
        command = f"CAMPBELL,{action}"
        return self.run(command, **kwargs)

    def cecmod(self, neqn="", const="", **kwargs):
        """Modifies the constant term of a constraint equation during solution.

        APDL Command: CECMOD

        Parameters
        ----------
        neqn
            Reference number of constraint equation.

        const
            New value of the constant term of equation.

        Notes
        -----
        Other terms of the constraint equation cannot be changed during the
        solution phase, but must be defined or changed within PREP7 prior to
        the solution.  See the CE command for details.

        This command is also valid in PREP7.
        """
        command = f"CECMOD,{neqn},{const}"
        return self.run(command, **kwargs)

    def deltim(self, dtime="", dtmin="", dtmax="", carry="", **kwargs):
        """Specifies the time step sizes to be used for the current load step.

        APDL Command: DELTIM

        Parameters
        ----------
        dtime
            Time step size for this step. If automatic time stepping is used
            (AUTOTS), DTIME is the starting time substep.

        dtmin
            Minimum time step (if automatic time stepping is used). The program
            automatically determines the default based on the physics of the
            model.

        dtmax
            Maximum time step (if automatic time stepping is used). The program
            automatically determines the default based on the physics of the
            model.

        carry
            Time step carry over key:

            OFF - Use DTIME as time step at start of each load step.

            ON - Use final time step from previous load step as the starting time step (if
                 automatic time stepping is used).

        Notes
        -----
        See NSUBST for an alternative input.

        Use consistent values for DTIME and TIME (TIME). For example, using 0.9
        for DTIME and 1.0 for TIME results in one time step because 1.0 (TIME)
        is divisible by .9 (DTIME) at most once. If you intend to load in 10
        increments over a time span of 1.0, use 0.1 for DTIME and 1.0 for TIME.

        The program calculates the initial incremental time so that (EndingTime
        - StartingTime)/DTIME is an integer, which may affect the initial
        incremental time that you specify. For example, if the starting time is
        0, the ending time is 1, and the initial incremental time is 0.4, the
        program rounds to the nearest integer and adjusts the time to 0.33333.

        For solution efficiency, specify values for all fields of this command.

        This command is also valid in PREP7.
        """
        command = f"DELTIM,{dtime},{dtmin},{dtmax},{carry}"
        return self.run(command, **kwargs)

    def expsol(self, lstep="", sbstep="", timfrq="", elcalc="", **kwargs):
        """Specifies the solution to be expanded for mode-superposition analyses

        APDL Command: EXPSOL
        or substructure analyses.

        Parameters
        ----------
        lstep, sbstep
            Expand the solution identified as load step LSTEP and substep
            SBSTEP.

        timfrq
            As an alternative to LSTEP and SBSTEP, expand the solution at, or
            nearest to, the time value TIMFRQ (for ANTYPE,TRANS or
            ANTYPE,SUBSTR) or frequency value TIMFRQ (for ANTYPE,HARMIC).
            LSTEP and SBSTEP should be blank.

        elcalc
            Element calculation key:

            YES - Calculate element results, nodal loads, and reaction loads.

            NO - Do not calculate these items.

        Notes
        -----
        Specifies the solution to be expanded from analyses that use the mode-
        superposition method (ANTYPE,HARMIC or TRANS) or substructuring
        (ANTYPE,SUBSTR). Use the NUMEXP command to expand a group of solutions.

        The resulting results file will maintain the same load step, substep,
        and time (or frequency) values as the requested solution to be
        expanded.

        This command is also valid in PREP7.
        """
        command = f"EXPSOL,{lstep},{sbstep},{timfrq},{elcalc}"
        return self.run(command, **kwargs)

    def kbc(self, key="", **kwargs):
        """Specifies ramped or stepped loading within a load step.

        APDL Command: KBC

        Parameters
        ----------
        key
            Ramping key:

            0 - Loads are linearly interpolated (ramped) for each substep from the values of
                the previous load step to the values of this load step. This is
                the default value.

            1 - Loads are step changed (stepped) at the first substep of this load step to the
                values of this load step (i.e., the same values are used for
                all substeps).  Useful for rate-dependent behavior (e.g.,
                creep, viscoplasticity, etc.) or transient load steps only.

        Notes
        -----
        Specifies whether loads applied to intermediate substeps within the
        load step are to be stepped or ramped. Used only if DTIME on the DELTIM
        command is less than the time span or, conversely, if NSBSTP on the
        NSUBST command is greater than one. Flags (FSI, MXWF, MVDI, etc.) are
        always stepped.

        Changing the ramping KEY (i.e., switching between ramped and stepped
        boundary conditions) between load steps is not recommended.

        For ramped loading (KBC,0), when a load is applied for the first time,
        it is interpolated from zero to the value of the current load step, and
        not from the initial condition or value of the degree of freedom from
        the previous load step.

        Spatially varying tabular loads or boundary conditions do not support
        direct ramping or stepping options and, instead, apply their full
        values according to the supplied tabular functions regardless of the
        KBC setting.

        For a static or harmonic cyclic symmetry analysis, any load that varies
        by sector (CYCOPT,LDSECT) is tabular and is applied as a step change,
        regardless of the KBC setting; however, any non-tabular loads in the
        same analysis are ramped or stepped according to the KBC setting.

        Irrespective of the KBC setting, loads are usually step-removed. See
        Stepping or Ramping Loads in the Basic Analysis Guide for more
        information.

        It is sometimes difficult to obtain successful convergence with stepped
        loading in a nonlinear transient problem. If divergence is encountered,
        determine if stepped loading was used by default, then determine if it
        is appropriate for the analysis.

        This command is also valid in PREP7.
        """
        command = f"KBC,{key}"
        return self.run(command, **kwargs)

    def kuse(self, key="", **kwargs):
        """Specifies whether or not to reuse the factorized matrix.

        APDL Command: KUSE

        Parameters
        ----------
        key
            Reuse key:

            - 0 : Program decides whether or not to reuse the previous
              factorized stiffness matrix.
            - 1 : Force the previous factorized stiffness matrix to be
              reused.  Used mainly in a restart.  Forcing reuse of the
              matrix is a nonstandard use of the program, and
              should be done with caution.  For instance, using
              this option and changing the number of elements, or
              the number or type of degrees of freedom, may cause
              an abort.
            - -1 : All element matrices are reformed and are used to
              reform a new factorized stiffness matrix.

        Notes
        -----
        Overrides the program logic to determine whether or not to reuse the
        previous factorized stiffness matrix for each substep of this load
        step.  Applies only to static or full transient analyses and to full
        harmonic analyses if the frequency is not changed for continuing
        loadsteps. For full harmonic analyses, only KEY = 1 or KEY = 0 is
        valid.

        This command is also valid in PREP7.
        """
        command = f"KUSE,{key}"
        return self.run(command, **kwargs)

    def magopt(self, value="", **kwargs):
        """Specifies options for a 3-D magnetostatic field analysis.

        APDL Command: MAGOPT

        Parameters
        ----------
        value
            Option key:

            0 - Calculate a complete H field solution in the entire domain using a single
                (reduced) potential.

            Caution:When used in problems with both current sources and iron regions, errors may result due to numerical cancellation. - 1

            Calculate and store a preliminary H field in "iron" regions (μr ≠ 1).  Requires flux-parallel boundary conditions to be specified on exterior iron boundaries.  Used in conjunction with subsequent solutions with VALUE = 2 followed by VALUE = 3.  Applicable to multiply-connected iron domain problems. - 2

            Calculate and store a preliminary H field in "air" regions (μr = 1).  The air-iron interface is appropriately treated internally by the program.  Used in conjunction with a subsequent solution with VALUE = 3.  Applicable to singly-connected iron domain problems (with subsequent solution with VALUE = 3) or to multiply-connected iron domain problems (when preceded by a solution with VALUE = 1 and followed by a solution with VALUE = 3). - 3

        Notes
        -----
        Specifies the solution sequence options for a 3-D magnetostatic field
        analysis using a scalar potential (MAG).  The solution sequence is
        determined by the nature of the problem.

        You cannot use constraint equations with Value = 1.

        This command is also valid in PREP7.

        Distributed ANSYS Restriction: The MAGOPT,3 option is not supported in
        Distributed ANSYS when the following contact elements are present in
        the model: CONTA173, CONTA174, CONTA175, CONTA176, or CONTA177.
        """
        command = f"MAGOPT,{value}"
        return self.run(command, **kwargs)

    def magsolv(
        self,
        opt="",
        nramp="",
        cnvcsg="",
        cnvflux="",
        neqit="",
        biot="",
        cnvtol="",
        **kwargs,
    ):
        """Specifies magnetic solution options and initiates the solution.

        APDL Command: MAGSOLV

        Parameters
        ----------
        opt
            Static magnetic solution option:

            0 - Vector potential (MVP) or edge formulation  (default).

            1 - Combined vector potential and reduced scalar potential (MVP-RSP).

            2 - Reduced scalar potential (RSP).

            3 - Difference scalar potential (DSP).

            4 - General scalar potential (GSP).

        nramp
            Number of ramped substeps for the first load step of a nonlinear
            MVP or MVP-RSP solution.  Defaults to 3.  If NRAMP = -1, ignore the
            ramped load step entirely.NRAMP is ignored for linear
            magnetostatics.

        cnvcsg
            Tolerance value on the program-calculated reference value for the
            magnetic current-segment convergence.  Used for the MVP, the MVP-
            RSP, and the edge formulation solution options (OPT = 0 and 1).
            Defaults to 0.001.

        cnvflux
            Tolerance value on the program-calculated reference value for the
            magnetic flux convergence.  Used for all scalar potential solution
            options (OPT = 2, 3, 4).  Defaults to 0.001.

        neqit
            Maximum number of equilibrium iterations per load step.  Defaults
            to 25.

        biot
            Option to force execution of a Biot-Savart integral solution
            [BIOT,NEW] for the scalar potential options.  Required if multiple
            load steps are being performed with different current source
            primitives (SOURC36 elements).

            0 - Do not force execution of Biot-Savart calculation (default); Biot-Savart is
                automatically calculated only for the first solution.

            1 - Force execution of Biot-Savart calculation.

        cnvtol
            Sets the convergence tolerance for AMPS reaction. Defaults to 1e-3.

        Notes
        -----
        MAGSOLV invokes an ANSYS macro which specifies magnetic solution
        options and initiates the solution.  The macro is applicable to any
        ANSYS magnetostatic analysis using the magnetic vector potential (MVP),
        reduced scalar potential (RSP), difference scalar potential (DSP),
        general scalar potential (GSP), or combined MVP-RSP formulation
        options.  Results are only stored for the final converged solution.
        (In POST1, issue ``*SET,LIST`` to identify the load step of solution
        results.)  The macro internally determines if a nonlinear analysis is
        required based on magnetic material properties.

        If you use the BIOT option and issue SAVE after solution or
        postprocessing, the Biot-Savart calculations are saved to the database,
        but will be overwritten upon normal exit from the program.  To save
        this data after issuing SAVE, use the /EXIT,NOSAVE command.  You can
        also issue the /EXIT,SOLU command to exit ANSYS and save all solution
        data, including the Biot-Savart calculations, in the database.
        Otherwise, when you issue RESUME, the Biot-Savart calculation will be
        lost (resulting in a zero solution).

        The MVP, MVP-RSP, and edge formulation options perform a two-load-step
        solution sequence.  The first load step ramps the applied loads over a
        prescribed number of substeps (NRAMP), and the second load step
        calculates the converged solution.  For linear problems, only a single
        load step solution is performed.  The ramped load step can be bypassed
        by setting NRAMP to -1.

        The RSP option solves in a single load step using the adaptive descent
        procedure.  The DSP option uses two load steps, and the GSP solution
        uses three load steps.

        The following analysis options and nonlinear options are controlled by
        this macro:  KBC, NEQIT, NSUBST, CNVTOL, NROPT, MAGOPT, and OUTRES.

        You cannot use constraint equations with OPT = 4.
        """
        command = f"MAGSOLV,{opt},{nramp},{cnvcsg},{cnvflux},{neqit},{biot},{cnvtol}"
        return self.run(command, **kwargs)

    def mode(self, mode="", isym="", **kwargs):
        """Specifies the harmonic loading term for this load step.

        APDL Command: MODE

        Parameters
        ----------
        mode
            Number of harmonic waves around circumference for this harmonic
            loading term (defaults to 0).

        isym
            Symmetry condition for this harmonic loading term (not used when
            MODE = 0):

            1 - Symmetric (UX, UY, ROTZ, TEMP use cosine terms; UZ uses sine term) (default).

            -1 - Antisymmetric (UX, UY, ROTZ, TEMP use sine terms; UZ uses cosine term).

        Notes
        -----
        Used with axisymmetric elements having nonaxisymmetric loading
        capability (for example, PLANE25, SHELL61, etc.).  For analysis types
        ANTYPE,MODAL, HARMIC, TRANS, and SUBSTR, the term must be defined in
        the first load step and may not be changed in succeeding load steps.

        This command is also valid in PREP7.
        """
        command = f"MODE,{mode},{isym}"
        return self.run(command, **kwargs)

    def nsubst(self, nsbstp="", nsbmx="", nsbmn="", carry="", **kwargs):
        """Specifies the number of substeps to be taken this load step.

        APDL Command: NSUBST

        Parameters
        ----------
        nsbstp
            Number of substeps to be used for this load step (i.e., the time
            step size or frequency increment). If automatic time stepping is
            used (``AUTOTS``), ``NSBSTP`` defines the size of the first substep.

        nsbmx
            Maximum number of substeps to be taken (i.e., the minimum time step
            size) if automatic time stepping is used. The program automatically
            determines the default based on the physics of the model.

        nsbmn
            Minimum number of substeps to be taken (i.e., the maximum time step
            size) if automatic time stepping is used. The program automatically
            determines the default based on the physics of the model.

        carry
            Time step carryover key (program-determined default depending on
            the problem physics):

            OFF
                Use NSBSTP to define time step at start of each load step.

            ON
                Use final time step from previous load step as the starting time step (if
                automatic time stepping is used).

        Notes
        -----
        See ``DELTIM`` for an alternative input.  It is recommended that all fields
        of this command be specified for solution efficiency and robustness.

        When the arc-length method is active (``ARCLEN`` command), the ``NSBMX`` and
        ``NSBMN`` arguments are ignored.

        This command is also valid in PREP7.
        """
        command = f"NSUBST,{nsbstp},{nsbmx},{nsbmn},{carry}"
        return self.run(command, **kwargs)

    def numexp(self, num="", begrng="", endrng="", elcalc="", **kwargs):
        """Specifies solutions to be expanded from mode-superposition analyses or

        APDL Command: NUMEXP
        substructure analyses.

        Parameters
        ----------
        num
            The number of solutions to expand. This value is required.

            Num
                Number of solutions to expand.

            ALL
                Expand all substeps between ``BEGRNG`` and ``ENDRNG`` (provided that ENDRNG > 0). If
                ``BEGRNG`` and ``ENDRNG`` have no specified values, this option
                expands all substeps of all load steps.

        begrng, endrng
            Beginning and ending time (or frequency) range for expanded
            solutions. The default is 0 for both values.

        elcalc
            The element-calculation key:

            YES
                Calculate element results, nodal loads, and reaction loads. This value is the
                default.

            NO
                Do not calculate these items.

        Notes
        -----
        Specifies a range of solutions to be expanded from analyses that use
        mode-superposition methods (``ANTYPE,HARMIC`` or ``TRANS``) or substructuring
        (``ANTYPE,SUBSTR``).

        For ANTYPE,TRANS, NUM, evenly spaced solutions are expanded between
        time BEGRNG and time ``ENDRNG``.

        For ANTYPE,HARMIC, NUM, evenly spaced solutions are expanded between
        frequency BEGRNG and frequency ``ENDRNG``.

        The first expansion in all cases is done at the first point beyond
        BEGRNG (that is, at ``BEGRNG + (ENDRNG - BEGRNG) / NUM``)).

        The resulting results file will maintain the same load step, substep,
        and time (or frequency) values as the use pass.

        For a single expansion of a solution, or for multiple expansions when
        the solutions are not evenly spaced (such as in a mode-superposition
        harmonic analysis with the cluster option), ANSYS, Inc. recommends
        issuing one or more ``EXPSOL`` commands.

        The NUMEXP command is invalid in these cases:

        In a substructing analysis (``ANTYPE,SUBST``) when a factorized matrix file
        (the ``.LN22`` file generated by the sparse solver) does not exist, causing
        ANSYS to employ the full-resolve method.

        If the full-resolve option is selected using the ``SEOPT`` command.

        In both situations, use the ``EXPSOL`` command to perform a single
        expansion for each solution desired.

        This command is also valid in PREP7.
        """
        command = f"NUMEXP,{num},{begrng},{endrng},{elcalc}"
        return self.run(command, **kwargs)

    def time(self, time="", **kwargs):
        """Sets the time for a load step.

        APDL Command: TIME

        Parameters
        ----------
        time
            Time at the end of the load step.

        Notes
        -----
        Associates the boundary conditions at the end of the load step with a
        particular TIME value.

        TIME must be a positive, nonzero, monotonically increasing quantity
        that "tracks" the input history.  Units of time should be consistent
        with those used elsewhere (for properties, creep equations, etc.).

        Typically, for the first load step TIME defaults to 1. However, for the
        first load step of a mode-superposition transient analysis
        (ANTYPE,TRANS and TRNOPT,MSUP), the TIME command is ignored and a
        static solution is performed at TIME = 0.

        For a full transient analyses, the command's default behavior does not
        apply. You must specify a time for each load step and it must be
        greater than the time at the end of the prior load step.

        TIME does not apply to modal (ANTYPE,MODAL), harmonic (ANTYPE,HARMIC),
        or substructure (ANTYPE,SUBSTR) analyses.

        This command is also valid in PREP7.
        """
        command = f"TIME,{time}"
        return self.run(command, **kwargs)

    def tref(self, tref="", **kwargs):
        """Defines the reference temperature for the thermal strain calculations.

        APDL Command: TREF

        Parameters
        ----------
        tref
            Reference temperature for thermal expansion.

        Notes
        -----
        Defines the reference temperature for the thermal strain calculations
        in structural analyses and explicit dynamic analyses.  Thermal strains
        are given by : ``α * (T-TREF)``, where α is the coefficient of thermal
        expansion (for more on this see the Mechanical APDL Theory Reference).
        Input the strain via ALPX, ALPY, ALPZ (the secant or mean coefficient
        value), or CTEX, CTEY, CTEZ (the instantaneous coefficient value), or
        the thermal strain value (THSX, THSY, THSZ). T is the element
        temperature. If α is temperature-dependent, TREF should be in the range
        of temperatures you define using the MPTEMP command.

        Reference temperatures may also be input per material by specifying a
        value on the MP material property command:

        MP,REFT,MAT,C0.

        Only a constant (non-temperature-dependent) value is valid. The value
        input on the TREF command applies to all materials not having a
        specified material property definition.

        To convert temperature-dependent secant coefficients of thermal
        expansion (SCTE) data (properties ALPX, ALPY, ALPZ) from the definition
        temperature to the reference temperature defined via a TREF (or
        MP,REFT) command, issue the MPAMOD command.

        This command is also valid in PREP7.
        """
        command = f"TREF,{tref}"
        return self.run(command, **kwargs)

    def tsres(self, array="", **kwargs):
        """Defines an array of key times at which the time-stepping strategy

        APDL Command: TSRES
        changes.

        Parameters
        ----------
        array
            Identifies an Nx1x1 array parameter containing the key times at
            which the heat transfer time-stepping strategy changes (the time
            step is reset to the initial time step based on DELTIM or NSUBST
            settings).  The array name must be enclosed by % signs (e.g.,
            %array%).  See ``*DIM`` for more information on array parameters.

        Notes
        -----
        Time values in the array parameter must be in ascending order and must
        not exceed the time at the end of the load step as defined on the TIME
        command. The time increment between time points in the array list must
        be larger than the initial time step defined on the DELTIM or NSUBST
        command.  Time values must also fall between the beginning and ending
        time values of the load step.  For multiple load step problems, you
        must either change the parameter values to fall between the beginning
        and ending time values of the load step or reissue the command with a
        new array parameter.  To clear the array parameter specification, issue
        TSRES,ERASE.  Results can be output at the requested time points if the
        array or time values in the array are also specified in the OUTRES
        command using FREQ=%array%.  Use this command to reset the time-
        stepping strategy within a load step. You may need to reset the time-
        stepping strategy when using tabular time-varying boundary conditions.

        See Steady-State Thermal Analysis of the Thermal Analysis Guide  for
        more information on applying boundary conditions via tabular input.
        See Transient Thermal Analysis of the Thermal Analysis Guide for more
        information on defining the key time array.
        """
        command = f"TSRES,{array}"
        return self.run(command, **kwargs)

    def upcoord(self, factor="", key="", **kwargs):
        """Modifies the coordinates of the active set of nodes, based on the

        APDL Command: UPCOORD
        current displacements.

        Parameters
        ----------
        factor
            Scale factor for displacements being added to nodal coordinates.
            If FACTOR = 1.0, the full displacement value will be added to each
            node, 0.5, half the displacement value will be added, etc.  If
            FACTOR = -1, the full displacement value will be subtracted from
            each node, etc.

        key
            Key for zeroing displacements in the database:

            OFF - Do not zero the displacements (default).

            ON - Zero the displacements.

        Notes
        -----
        The UPCOORD command uses displacements stored in the ANSYS database,
        and not those contained within the results file, Jobname.RST.  Nodal
        coordinates are updated each time the command is issued.  After
        updating, both the nodal displacements and rotations are set to zero if
        Key = ON.

        For structural solutions with an updated mesh, unless the coefficient
        matrix is otherwise reformed (e.g., a new analysis or NLGEOM,ON) it
        should first be reformed by issuing a KUSE,-1 command.

        UPCOORD should not be issued between load steps in structural analysis.

        For a multiphysics simulation where a CFD or electromagnetic field is
        being coupled to a structure undergoing large displacements, all (or a
        portion) of the surrounding field mesh may take part in the structural
        solution to "move" with the displacing structure.  You can use the
        UPCOORD command with a suitable FACTOR to update the coordinates of the
        nodes using the newly computed displacements.  The mesh will now
        conform with the displaced structure for subsequent field solutions.
        However, the mesh should always be restored to its original location by
        using an UPCOORD,FACTOR command before performing any subsequent
        structural solutions.  This is true for both repeated linear solutions,
        and for nonlinear restarts. (All saved displacements are relative to
        the original mesh location.)

        This command is not intended to replace either the large displacement
        or birth and death logic.

        This command is also valid in PREP7.
        """
        command = f"UPCOORD,{factor},{key}"
        return self.run(command, **kwargs)

    def usrcal(
        self,
        rnam1="",
        rnam2="",
        rnam3="",
        rnam4="",
        rnam5="",
        rnam6="",
        rnam7="",
        rnam8="",
        rnam9="",
        **kwargs,
    ):
        """Allows user-solution subroutines to be activated or deactivated.

        APDL Command: USRCAL

        Parameters
        ----------
        rnam1, rnam2, rnam3, . . . , rnam9
            User-defined solution subroutine names to be activated.  Up to nine
            may be defined on one command or multiple commands may be used.  If
            Rnam1 = ALL, activate all valid user subroutines.   If Rnam1 =
            NONE, deactivate all valid user subroutines.  All characters are
            required:

            USREFL - Allows user defined scalar field (body force) loads.

            USERCV - Allows user defined convection (surface) loads.

            USERPR - Allows user defined pressure (surface) loads.

            USERFX - Allows user-defined heat flux (surface) loads.

            USERCH - Allows user-defined charge density (surface) loads.

            USERFD - Computes the complex load vector for the frequency domain logic.

            USEROU - Allows user supplied element output.

            USERMC - Allows user control of the hygrothermal growth).

            USOLBEG - Allows user access before each solution.

            ULDBEG - Allows user access before each load step.

            USSBEG - Allows user access before each substep.

            UITBEG - Allows user access before each equilibrium iteration.

            UITFIN - Allows user access after each equilibrium iteration.

            USSFIN - Allows user access after each substep.

            ULDFIN - Allows user access after each load step.

            USOLFIN - Allows user access after each solution.

            UANBEG - Allows user access at start of run.

            UANFIN - Allows user access at end of run.

            UELMATX - Allows user access to element matrices and load vectors.

            UTIMEINC - Allows a user-defined time step, overriding the program-determined time step.

            UCNVRG - Allows user-defined convergence checking, overriding the program-determined
                     convergence.

        Notes
        -----
        Allows certain user-solution subroutines to be activated or deactivated
        (system-dependent).  This command only affects the subroutines named.
        Other user subroutines (such as user elements, user creep, etc.) have
        their own activation controls described with the feature.

        The routines are commented and should be listed after performing a
        custom installation from the distribution media for more details.  See
        also the Advanced Analysis Guide for a general description of user-
        programmable features.

        Users must have system permission, system access, and knowledge to
        write, compile, and link the appropriate subroutines into the program
        at the site where it is to be run.  All routines should be written in
        FORTRAN. (For more information on FORTRAN compilers please refer to
        either the ANSYS, Inc. Windows Installation Guide or the ANSYS, Inc.
        Linux Installation Guide for details specific to your platform or
        operating system.) Issue USRCAL,STAT to list the status of these user
        subroutines.  Since a user-programmed subroutine is a nonstandard use
        of the program, the verification of any ANSYS run incorporating these
        commands is entirely up to the user.  In any contact with ANSYS
        customer support regarding the performance of a custom version of the
        ANSYS program, you should explicitly state that a user programmable
        feature has been used.

        This command is also valid in PREP7.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"USRCAL,{rnam1},{rnam2},{rnam3},{rnam4},{rnam5},{rnam6},{rnam7},{rnam8},{rnam9}"
        return self.run(command, **kwargs)

    def wrfull(self, ldstep="", **kwargs):
        """Stops solution after assembling global matrices.

        APDL Command: WRFULL

        Parameters
        ----------
        ldstep
            Specify action to take:

            OFF or 0 - Turn off feature (default)

            N - Turn on feature and set it to stop after assembling the global matrices and
                writing the .FULL file for load step N.

        Notes
        -----
        This command is used in conjunction with the SOLVE command to generate
        the assembled matrix file (.FULL file) only.  The element matrices are
        assembled into the relevant global matrices for the particular analysis
        being performed and the .FULL file is written.  Equation solution and
        the output of data to the results file are skipped.  To dump the
        matrices written on the .FULL file into Harwell-Boeing format, use the
        HBMAT command in /AUX2. To copy the matrices to a postscript format
        that can be viewed graphically, use the PSMAT command.

        To use the LSSOLVE macro with this command, you may need to modify the
        LSSOLVE macro to properly stop at the load step of interest.

        This command only valid for linear static, full harmonic, and full
        transient analyses when the sparse direct solver is selected.  This
        command is also valid for buckling or modal analyses with any mode
        extraction method.  This command is not valid for nonlinear analyses.
        It is not supported in a linear perturbation analysis.

        In general, the assembled matrix file .FULL contains stiffness, mass,
        and damping matrices. However, the availability of the matrices depends
        on the analysis type chosen when the file is written.
        """
        command = f"WRFULL,{ldstep}"
        return self.run(command, **kwargs)
