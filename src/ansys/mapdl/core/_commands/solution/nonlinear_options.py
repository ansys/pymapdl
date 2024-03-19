class NonLinearOptions:
    def arclen(self, key="", maxarc="", minarc="", **kwargs):
        """Activates the arc-length method.

        APDL Command: ARCLEN

        Parameters
        ----------
        key
            Arc-length key:

            OFF - Do not use the arc-length method (default).

            ON - Use the arc-length method.

        maxarc
            Maximum multiplier of the reference arc-length radius (default =
            25).

        minarc
            Minimum multiplier of the reference arc-length radius (default =
            1/1000).

        Notes
        -----
        Activates the arc-length method and sets the minimum and maximum
        multipliers for controlling the arc-length radius based on the initial
        arc-length radius.

        The initial arc-length radius, t0, is proportional (in absolute value)
        to the initial load factor. The initial load factor is given by:

        Initial Load Factor = TIME / NSBSTP

        where TIME is the time specified by the TIME command for the arc-length
        load step, and NSBSTP is the number of substeps specified by the NSUBST
        command.

        The factors MAXARC and MINARC are used to define the range for the arc-
        length radius to expand and shrink during the substep solution:

        In each substep, the arc-length radius is kept constant throughout the
        equilibrium iterations. After each converged substep, the arc-length
        radius for the next substep is modified depending on the convergence
        behavior. If the substep converges and the program heuristic predicts
        an easy convergence, the arc-length radius is enlarged. If the enlarged
        value is greater than tMAX, the arc-length radius is reset to tMAX. If
        the substep does not converge, bisection will take place until the arc-
        length radius is reduced to tMIN. If further nonconvergence is
        encountered, the solution terminates.

        The arc-length method predicts the next time increment (that is, load
        factor increment). Therefore, the AUTOTS and PRED commands are ignored
        when the arc-length method is used.

        The STABILIZE and LNSRCH commands are also ignored.

        The arc-length method cannot be used in a multiframe restart.

        For difficult problems, one suggestion is to increase the initial
        number of substeps (NSUBST), and to prevent the arc-length radius from
        increasing too rapidly (MAXARC = 1).

        ARCLEN cannot be used for any load step that has no applied load or
        displacement.

        The arc-length method does not support tabular loads. In order to use
        the arc-length method, you must replace tabular loads by other load
        types and then run the analysis again.
        """
        command = f"ARCLEN,{key},{maxarc},{minarc}"
        return self.run(command, **kwargs)

    def arctrm(self, lab="", val="", node="", dof="", **kwargs):
        """Controls termination of the solution when the arc-length method is

        APDL Command: ARCTRM
        used.

        Parameters
        ----------
        lab
            Specifies the basis of solution termination:

            OFF - Does not use ARCTRM to terminate analysis (default).

            L - Terminates the analysis if the first limit point has been reached.  The first
                limit point is that point in the response history when the
                tangent stiffness matrix becomes singular (i.e., the point at
                which the structure becomes unstable).  If Lab = L, arguments
                VAL, NODE, DOF are ignored.

            U - Terminates the analysis when the displacement first equals or exceeds the
                maximum desired value.

        val
            Maximum desired displacement (absolute value).  Valid only if Lab =
            U.  The analysis terminates whenever the calculated displacement
            first equals or exceeds this value.  For rotational degrees of
            freedom, VAL must be in radians (not degrees).

        node
            Node number corresponding to displacement used to compare with
            displacement specified by VAL.  If blank, the maximum displacement
            will be used.  Valid only if Lab = U.

        dof
            Valid degree of freedom label for nodal displacement specified by
            NODE.  Valid labels are UX, UY, UZ, ROTX, ROTY, ROTZ.  Valid only
            if NODE>0 and Lab = U.

        Notes
        -----
        The ARCTRM command is valid only when the arc-length method (ARCLEN,ON)
        is used.

        It can be convenient to use this command to terminate the analysis when
        the first limit point is reached. In addition, the NCNV command should
        be used to limit the maximum number of iterations. If the ARCTRM
        command is not used, and the applied load is so large that the solution
        path can never reach that load, the arc-length solution will continue
        to run until a CPU time limit or a "maximum number of iterations" is
        reached.
        """
        command = f"ARCTRM,{lab},{val},{node},{dof}"
        return self.run(command, **kwargs)

    def bucopt(self, method="", nmode="", shift="", ldmulte="", rangekey="", **kwargs):
        """Specifies buckling analysis options.

        APDL Command: BUCOPT

        Parameters
        ----------
        method
            Mode extraction method to be used for the buckling analysis:

            LANB - Block Lanczos

            SUBSP - Subspace iteration

        nmode
            Number of buckling modes (i.e., eigenvalues or load multipliers) to
            extract (defaults to 1).

        shift
            By default, this value acts as the initial shift point about which
            the buckling modes are calculated (defaults to 0.0).

        ldmulte
            Boundary for the load multiplier range of interest (defaults to ).

        rangekey
            Key used to control the behavior of the eigenvalue extraction
            method (defaults to CENTER):

            CENTER - Use the CENTER option control (default); the program computes NMODE buckling
                     modes centered around SHIFT in the range of (-LDMULTE,
                     +LDMULTE).

            RANGE - Use the RANGE option control; the program computes NMODE buckling modes in the
                    range of (SHIFT, LDMULTE).

        Notes
        -----
        Eigenvalues from a buckling analysis can be negative and/or positive.
        The program sorts the eigenvalues from the most negative to the most
        positive values. The minimum buckling load factor may correspond to the
        smallest eigenvalue in absolute value, or to an eigenvalue within the
        range, depending on your application (i.e., linear perturbation
        buckling analysis or purely linear buckling analysis).

        It is recommended that you request an additional few buckling modes
        beyond what is needed in order to enhance the accuracy of the final
        solution. It is also recommended that you input a non zero SHIFT value
        and a reasonable LDMULTE value (i.e., a smaller LDMULTE that is closer
        to the last buckling mode of interest) when numerical problems are
        encountered.

        When using the RANGE option, defining a range that spans zero is not
        recommended. If you are seeking both negative and positive eigenvalues,
        it is recommended that you use the CENTER option.

        This command is also valid in PREP7.  If used in SOLUTION, this command
        is valid only within the first load step.

        Distributed ANSYS Restriction: Both extraction methods (LANB and SUBSP)
        are supported within Distributed ANSYS. However, the subspace iteration
        eigensolver (SUBSP) is the only distributed eigensolver that will run a
        fully distributed solution. The Block Lanczos eigensolver (LANB) is not
        a distributed eigensolver; therefore, you will not see the full
        performance improvements with this method that you would with a fully
        distributed solution.
        """
        command = f"BUCOPT,{method},{nmode},{shift},{ldmulte},{rangekey}"
        return self.run(command, **kwargs)

    def cnvtol(self, lab="", value="", toler="", norm="", minref="", **kwargs):
        """Sets convergence values for nonlinear analyses.

        APDL Command: CNVTOL

        Parameters
        ----------
        lab
            Valid convergence labels. If STAT, list the status of the currently
            specified criteria.

        value
            Typical reference value for the specified convergence label (Lab).

        toler
            Tolerance; defaults to 0.005 (0.5%) for force and moment, 1.0E-4
            (0.01%) for DVOL, 0.05 (5%) for displacement when rotational DOFs
            are not present, and 0.05 (5%) for HDSP.

        norm
            Specifies norm selection:

            2 - L2 norm (check SRSS value). Default, except for Lab = U.

            1 - L1 norm (check absolute value sum).

            0 - Infinite norm (check each DOF separately). Default for Lab = U.

        minref
            The minimum value allowed for the program calculated reference
            value. If negative, no minimum is enforced. Used only if VALUE is
            blank. Defaults to 0.01 for force, moment, and volume convergence,
            1.0E-6 for heat flow, 1.0E-12 for VLTG and CHRG, 1.0E-6 for HDSP,
            and 0.0 otherwise.

        Notes
        -----
        This command is usually not needed because the default convergence
        criteria are sufficient for most nonlinear analyses. In rare cases, you
        may need to use this command to diagnose convergence difficulties.

        Values may be set for the degrees of freedom (DOF) and/or the out-of-
        balance load for the corresponding forcing quantities.

        Issuing CNVTOL to set a convergence criterion for a specific
        convergence label (Lab) does not affect the convergence criterion for
        any other label. All other convergence criteria will remain at their
        default setting or at the value set by a previous CNVTOL command.

        When the GUI is on, if a "Delete" operation in a Nonlinear Convergence
        Criteria dialog box writes this command to a log file (Jobname.LOG or
        Jobname.LGW), you will observe that Lab is blank, VALUE = -1, and TOLER
        is an integer number.  In this case, the GUI has assigned a value of
        TOLER that corresponds to the location of a chosen convergence label in
        the dialog box's list.  It is not intended that you type in such a
        location value for TOLER in an ANSYS session.  However, a file that
        contains a GUI-generated CNVTOL command of this form can be used for
        batch input or with the /INPUT command.

        Convergence norms specified with CNVTOL may be graphically tracked
        while the solution is in process using the ANSYS program's Graphical
        Solution Tracking (GST) feature.  Use the /GST command to turn GST on
        or off.  By default, GST is ON for interactive sessions and OFF for
        batch runs.

        This command is also valid in PREP7.
        """
        command = f"CNVTOL,{lab},{value},{toler},{norm},{minref}"
        return self.run(command, **kwargs)

    def crplim(self, crcr="", option="", **kwargs):
        """Specifies the creep criterion for automatic time stepping.

        APDL Command: CRPLIM

        Parameters
        ----------
        crcr
            Value of creep criteria for the creep limit ratio control.

        option
            Type of creep analysis for which the creep limit ratio is
            specified:

            1 (or ON) - Implicit creep analysis.

            0 (or OFF) - Explicit creep analysis.

        Notes
        -----
        The CUTCONTROL command can also be used to set the creep criterion and
        is preferred over this command for setting automatic time step
        controls.

        The creep ratio control can be used at the same time for implicit creep
        and explicit creep analyses. For implicit creep (Option = 1), the
        default value of CRCR is zero (i.e., no creep limit control), and you
        can specify any value. For explicit creep (Option = 0), the default
        value of CRCR is 0.1, and the maximum value allowed is 0.25.

        This command is also valid in PREP7.
        """
        command = f"CRPLIM,{crcr},{option}"
        return self.run(command, **kwargs)

    def gst(self, lab="", lab2="", **kwargs):
        """Turns Graphical Solution Tracking (GST) on or off.

        APDL Command: /GST

        Parameters
        ----------
        lab
            Determines whether the Graphical Solution Tracking feature is
            active.  Specify ON to activate GST, or OFF to deactivate the
            feature.

        lab2
            Activates generation of interface and field convergence files
            (ANSYS MFX analyses only).

        Notes
        -----
        For interactive runs using GUI [/MENU,ON] or graphics [/MENU,GRPH]
        mode, ANSYS directs GST graphics to the screen.  For interactive
        sessions not using GUI or graphics mode, or for batch sessions, GST
        graphics are saved in the ANSYS graphics file Jobname.GST when Lab2 is
        unspecified. The file Jobname.GST can be viewed with the DISPLAY
        program in this case. You must select All File Types to access it. For
        more information on the DISPLAY program see Getting Started with the
        DISPLAY Program in the Basic Analysis Guide. For MFX runs (when
        Lab2=ON), the Jobname.GST file is in XML format, and it can be viewed
        with the Results Tracker Utility, accessed from within the Tools menu
        of the Mechanical APDL Product Launcher.

        The GST feature is available only for nonlinear structural, thermal,
        electric, magnetic, fluid, or CFD simulations. For more information
        about this feature and illustrations of the GST graphics for each
        analysis type, see the ANSYS Analysis Guide for the appropriate
        discipline.  See also the CNVTOL command description.

        When running an ANSYS MFX analysis, specify /GST,ON,ON to generate both
        the interface (Jobname.NLH) and field convergence (Fieldname.GST) files
        for monitoring the analysis. This field is not available on the GUI.
        """
        command = f"/GST,{lab},{lab2}"
        return self.run(command, **kwargs)

    def lnsrch(self, key="", **kwargs):
        """Activates a line search to be used with Newton-Raphson.

        APDL Command: LNSRCH

        Parameters
        ----------
        key
            Line search key:

            OFF - Do not use a line search.

            ON - Use a line search.  Note, adaptive descent is suppressed when LNSRCH is on
                 unless explicitly requested on the NROPT command.   Having
                 line search on and adaptive descent on at the same time is not
                 recommended.

            AUTO - The program automatically switches line searching ON and OFF between substeps
                   of a load step as needed.  This option is recommended.

        Notes
        -----
        Activates a line search to be used with the Newton-Raphson method
        [NROPT].  Line search is an alternative to adaptive descent (see Line
        Search in the Mechanical APDL Theory Reference).

        LNSRCH,AUTO can be very efficient for problems in which LNSRCH is
        needed at only certain substeps.

        You cannot use line search [LNSRCH], automatic time stepping [AUTOTS],
        or the DOF solution predictor [PRED] with the arc-length method
        [ARCLEN, ARCTRM]. If you activate the arc-length method after you set
        LNSRCH, AUTOTS, or PRED, a warning message appears. If you choose to
        proceed with the arc-length method, the program disables your line
        search, automatic time stepping, and DOF predictor settings, and the
        time step size is controlled by the arc-length method internally.

        This command is also valid in PREP7.
        """
        command = f"LNSRCH,{key}"
        return self.run(command, **kwargs)

    def ncnv(self, kstop="", dlim="", itlim="", etlim="", cplim="", **kwargs):
        """Sets the key to terminate an analysis.

        APDL Command: NCNV

        Parameters
        ----------
        kstop
            Program behavior upon nonconvergence:

            0 - Do not terminate the analysis if the solution fails to converge.

            1 - Terminate the analysis and the program execution if the solution fails to
                converge (default).

            2 - Terminate the analysis, but not the program execution, if the solution fails to
                converge.

        dlim
            Terminates program execution if the largest nodal DOF solution
            value (displacement, temperature, etc.) exceeds this limit.
            Defaults to 1.0E6 for all DOF except MAG and A. Defaults to 1.0E10
            for MAG and A.

        itlim
            Terminates program execution if the cumulative iteration number
            exceeds this limit (defaults to infinity).

        etlim
            Terminates program execution if the elapsed time (seconds) exceeds
            this limit (defaults to infinity).

        cplim
            Terminates program execution if the CPU time (seconds) exceeds this
            limit (defaults to infinity).

        Notes
        -----
        Sets the key to terminate an analysis if not converged, or if any of
        the following limits are exceeded for nonlinear and full transient
        analyses: DOF (displacement), cumulative iteration, elapsed time, or
        CPU time limit.  Applies only to static and transient analyses
        (ANTYPE,STATIC and ANTYPE,TRANS). Time limit checks are made at the end
        of each equilibrium iteration.

        This command is also valid in PREP7.
        """
        command = f"NCNV,{kstop},{dlim},{itlim},{etlim},{cplim}"
        return self.run(command, **kwargs)

    def neqit(self, neqit="", forcekey="", **kwargs):
        """Specifies the maximum number of equilibrium iterations for nonlinear

        APDL Command: NEQIT
        analyses.

        Parameters
        ----------
        neqit
            Maximum number of equilibrium iterations allowed each substep.

        forcekey
            One iteration forcing key:

            FORCE - Forces one iteration per substep. Leave this field blank otherwise.

        Notes
        -----
        This command is also valid in PREP7.
        """
        command = f"NEQIT,{neqit},{forcekey}"
        return self.run(command, **kwargs)

    def nladaptive(
        self,
        component="",
        action="",
        criterion="",
        option="",
        val1="",
        val2="",
        val3="",
        val4="",
        **kwargs,
    ):
        """Defines the criteria under which the mesh is refined or
        modified during a nonlinear solution.

        APDL Command: NLADAPTIVE

        Parameters
        ----------
        component : str
            Specifies the element component upon which this command should
            act.  One of the following:

            - ``"ALL"`` : All selected components, or all selected
                   elements if no component is selected (default).
            - ``"Name"`` : Component name.

        action : str
            The action to perform on the selected component(s).  One of
            the following:

            - ``"ADD"`` : Add a criterion to the database.
            - ``"LIST"`` : List the criteria defined for the specified
              component(s).
            - ``"DELETE"`` : Delete the criteria defined for the specified
              component(s).
            - ``"ON"`` : Enable the defined criteria for the specified
              component(s) and specify how frequently and when to check
              them (via ON,,,VAL1,VAL2,VAL3):

                - ``"VAL1"`` : Checking frequency. If > 0, check criteria
                  at every VAL1 substeps. If < 0, check criteria at each
                  of the VAL1 points (approximately equally spaced)
                  between VAL2 and VAL3. (Default = -1.)
                - ``"VAL2"`` : Checking start time, where VAL2 <
                  VAL3. (Default is the start time of the load step.)
                - ``"VAL3"`` : Checking end time, where VAL3 >
                  VAL2. (Default is the end time of the load step.)
                - ``"VAL4"`` : SOLID187 element type ID (defined prior to
                  issuing this command). Valid only for SOLID185 or
                  SOLID186 components in a NLAD-ETCHG analysis.

            - ``"OFF"`` : Disable the defined criteria for the specified
              component(s).

        criterion
            The type of criterion to apply to the selected component(s):

            - ``"CONTACT"`` : Contact-based. (Valid only for Action = ADD,
              Action = LIST, or Action = DELETE.)

            - ``"ENERGY"`` : Energy-based. (Valid only for Action = ADD,
              Action = LIST, or Action = DELETE.)

            - ``"BOX"`` : A position-based criterion, defined by a
              box. (Valid only for Action = ADD, Action = LIST, or Action
              = DELETE.)

            - ``"MESH"`` : A mesh-quality-based criterion. (Valid only for
              Action = LIST, or Action = DELETE.)

            - ``"ALL"`` : All criteria and options. (Valid only for Action
              = LIST or Action = DELETE. Option and all subsequent
              arguments are ignored.)

        option : str
            Criterion option to apply to the selected component(s):

            - ``"NUMELEM"`` : For target elements only, define the minimum
              number of contact elements to contact with each target
              element. If this criterion is not satisfied, the program
              refines the contact elements and the associated solid
              elements. For this option, VAL1 must be a positive
              integer. (Valid only for Action = ADD, Action = LIST, or
              Action = DELETE. )

            - ``"MEAN"`` : Check the strain energy of any element that is
              part of the defined component for the condition Ee ≥ c1 *
              Etotal / NUME (where c1 = VAL1, Etotal is the total strain
              energy of the component, and NUME is the number of elements
              of the component). If this criterion is satisfied at an
              element, the program refines the element. For this option,
              VAL1 must be non-negative and defaults to 1. (Valid only for
              Action = ADD, Action = LIST, or Action = DELETE.)

            - ``"XYZRANGE"`` : Define the location box in which all
              elements within are to be split or refined. Up to six values
              following the Option argument (representing the x1, x2, y1,
              y2, z1, and z2 coordinates) are allowed. An unspecified
              coordinate is not checked. (Valid only for Action = ADD,
              Action = LIST, or Action = DELETE.)

            - ``"SKEWNESS"`` : Mesh-quality control threshold for element
              SOLID285. Valid values (VAL1) are 0.0 through 1.0. Default =
              0.9. (Valid only for Action = ADD, Action = LIST, or Action
              = DELETE.)

            - ``"WEAR"`` : This option is valid only for contact elements
              having surface wear specified (TB,WEAR). Define VAL1 as a
              critical ratio of magnitude of wear to the average depth of
              the solid element underlying the contact element. Once this
              critical ratio is reached for any element, the program
              morphs the mesh to improve the quality of the elements. VAL1
              must be a positive integer.  (Valid only for Action = ADD,
              Action = LIST, or Action = DELETE.) The WEAR criterion
              cannot be combined with any other criterion.

            - ``"ALL"`` : All options. (Valid only for Action = LIST or
              Action = DELETE. All subsequent arguments are ignored.)

        Notes
        -----
        If a specified component (Component) is an assembly, the defined
        criterion applies to all element components included in the
        assembly.

        All components must be defined and selected before the first solve
        (SOLVE), although their nonlinear adaptivity criteria can be
        modified from load step to load step, and upon restart. For
        nonlinear adaptivity to work properly, ensure that all components
        are selected before each solve.

        After using this command to define a new criterion, the new
        criterion becomes active and is checked one time during each load
        step, roughly in mid-loading (unless this behavior is changed via
        Action = ON).

        When a criterion is defined, it overwrites a previously defined
        criterion (if one exists) through the same component, or through
        the component assembly that includes the specified component.

        During solution, the same criteria defined for an element through
        different components are combined, and the tightest criteria and
        action control (Action,ON,,,VAL1) are used. If an ON action is
        defined by a positive VAL1 value through one component and a
        negative VAL1 value through another, the program uses the positive
        value.

        For ``action="ON"``, if VAL2 (start time) and/or VAL3 (end time)
        are unspecified or invalid, the program uses the start and/or end
        time (respectively) of the load step. If VAL1 < 0, the program
        checks VAL1 points between VAL2 and VAL3. The time interval
        between each check points is determined by (VAL3 - VAL2) / (VAL1 +
        1), with the first check point as close to VAL2 + (VAL3 - VAL2) /
        (VAL1 + 1) as possible.  Fewer check points can be used if the
        number of substeps during solution is insufficient (as the program
        can only check at the end of a substep).

        Option = SKEWNESS applies to linear tetrahedral element SOLID285
        only.  When the skewness of a SOLID285 element is >= the defined
        value, the element is used as the core (seed) element of the
        remeshed region(s).  If this criterion is used together with any
        other criteria for the same component, the other criteria defined
        for the component are ignored.  The most desirable skewness value
        is 0, applicable when the element is a standard tetrahedral
        element; the highest value is 1, applicable when the element
        becomes flat with zero volume. For more information about skewness
        and remeshing, see Mesh Nonlinear Adaptivity in the Advanced
        Analysis Guide.

        For more granular control of the source mesh geometry, see NLMESH.
        """
        command = f"NLADAPTIVE,{component},{action},{criterion},{option},{val1},{val2},{val3},{val4}"
        return self.run(command, **kwargs)

    def nldiag(self, label="", key="", maxfile="", **kwargs):
        """Sets nonlinear diagnostics functionality.

        APDL Command: NLDIAG

        Parameters
        ----------
        label
            Diagnostic function:

            NRRE - Store the Newton-Raphson residuals information.

            EFLG - Identify or display elements or nodes that violate the criteria.

            CONT - Write contact information to a single Jobname.cnd diagnostic text file during
                   solution.

        key
            Diagnostic function characteristics:

            OFF or 0 - Suppresses writing of diagnostic information (default).

            ON or 1 - Writes diagnostic information to the Jobname.ndxxx, Jobname.nrxxx, or
                      Jobname.cnd file. (If Label = CONT, this option is the
                      same as the SUBS option described below.)

            ITER  - Writes contact diagnostic information at each iteration. Valid only when Label
                    = CONT.

            SUBS  - Writes contact diagnostic information at each substep. Valid only when Label =
                    CONT.

            LSTP  - Writes contact diagnostic information at each load step. Valid only when Label
                    = CONT.

            STAT - Lists information about the diagnostic files in the current working directory.

            DEL - Deletes all diagnostic files in the current working directory.

        maxfile
            Maximum number of diagnostic files to create. Valid values are 1
            through 999. Default = 4. Valid only when Label = NRRE or EFLG.

        Notes
        -----
        The NLDIAG command is a nonlinear diagnostics tool valid for nonlinear
        structural analyses. It is a debugging tool for use when you must
        restart after an unconverged solution. The command creates
        Jobname.ndxxx, Jobname.nrxxx, or Jobname.cnd files in the working
        directory to store the information you specify.

        For more information, see Performing Nonlinear Diagnostics.

        Issue the NLDIAG,NRRE,ON command to create Jobname.nrxxx diagnostic
        files (for each equilibrium iteration after the first) in which to
        store the relevant Newton-Raphson residual information of
        forces/moments Fx, Fy, Fz, Mx, My and Mz for the last MAXFILE
        equilibrium iterations.

        Issue a NLDPOST,NRRE,STAT command to list the load step, substep, time,
        and equilibrium iteration corresponding to each of the Jobname.nrxxx
        diagnostic files in the working directory, then issue a
        PLNSOL,NRRES,,,,FileID command to point to the file from which you want
        to create a contour plot of your Newton-Raphson residuals.

        If you restart or issue a new SOLVE command, any Jobname.nrxxx
        diagnostic files in the current (working) directory are overwritten.

        Issue a NLDIAG,EFLG,ON command to create Jobname.ndxxx  diagnostic
        files which store IDs for elements violating the following criteria:

        Too large a distortion (HDST)

        Elements contain nodes that have near zero pivots (PIVT) for nonlinear
        analyses

        Too large a plastic/creep (EPPL/EPCR) strain increment (CUTCONTROL)

        Elements for which mixed u-P constraints are not satisfied (mixed U-P
        option of 18x solid elements only) (MXUP)

        Hyperelastic element (EPHY), cohesive zone material (EPCZ), or damage
        strain (EPDM) not converged

        Radial displacement (RDSP) not converged

        MPC184 multipoint constraint elements using KEYOPT(1) = 6 through 16
        with the Lagrange multiplier option fail to satisfy constraint
        conditions (184J)

        For NLDIAG,EFLG,ON, all Jobname.ndxxx diagnostic files (for each
        equilibrium iteration after the first) in the current (working)
        directory are deleted when you issue a new SOLVE command (or restart).

        In the solution processor (/SOLU), use the STAT option to list the
        active status of this command. In the postprocessor (/POST1), issue a
        NLDPOST,EFLG,STAT command to list the load step, substep, time, and
        equilibrium iteration corresponding to each of the Jobname.ndxxx
        diagnostic files in the working directory, then issue a
        NLDPOST,EFLG,CM,FileID command to create element components that
        violate the criteria.

        Issue the NLDIAG,CONT,ON command to create a Jobname.cnd diagnostic
        file which stores contact information for all defined contact pairs at
        all substeps. Alternatively, you may issue one of the following
        commands to store contact information at a specific frequency:

        NLDIAG,CONT,ITER to write at each iteration

        NLDIAG,CONT,SUBS to write at each substep (default)

        NLDIAG,CONT,LSTP to write at each load step

        Contact diagnostic information is available for elements CONTA171
        through CONTA177; it is not available for CONTA178.

        Diagnostic file Jobname.cnd is written during solution and lists, on a
        pair-base, the following contact information:

        Contact pair ID[1]

        Number of contact elements in contact[2]

        Number of contact elements in "sticking" contact status

        Maximum chattering level

        Maximum contact penetration/Minimum gap[3]

        Maximum closed gap

        Maximum normal contact stiffness

        Minimum normal contact stiffness

        Maximum resulting pinball

        Maximum elastic slip distance

        Maximum tangential contact stiffness

        Minimum tangential contact stiffness

        Maximum sliding distance

        Maximum contact pressure

        Maximum friction stress

        Average contact depth

        Maximum closed penetration

        Number of contact points having too much penetration

        Contacting area

        Maximum contact damping pressure

        Maximum tangential contact damping stress

        Maximum total sliding distance (GSLID), including near-field

        Minimum total sliding distance (GSLID), including near-field

        Maximum fluid penetration pressure on contact surface

        Maximum fluid penetration pressure on target surface

        Total volume lost due to wear for the contact pair

        Total strain energy due to contact constraint

        Total frictional dissipation energy

        Total contact stabilization energy

        ANSYS Workbench contact pair ID[4]
        """
        command = f"NLDIAG,{label},{key},{maxfile}"
        return self.run(command, **kwargs)

    def nlgeom(self, key="", **kwargs):
        """Includes large-deflection effects in a static or full transient

        APDL Command: NLGEOM
        analysis.

        Parameters
        ----------
        key
            Large-deflection key:

            OFF - Ignores large-deflection effects (that is, a small-deflection analysis is
                  specified). This option is the default.

            ON - Includes large-deflection (large rotation) effects or large strain effects,
                 according to the element type.

        Notes
        -----
        Large-deflection effects are categorized as either large deflection (or
        large rotation) or large strain, depending on the element type. These
        are listed (if available) under Special Features in the input data
        table for each element in the Element Reference. When large deflection
        effects are included (NLGEOM,ON), stress stiffening effects are also
        included automatically.

        If used during the solution (/SOLU), this command is valid only within
        the first load step.

        In a large-deflection analysis, pressure loads behave differently than
        other load types. For more information, see Load Direction in a Large-
        Deflection Analysis.

        The gyroscopic matrix (that occurs due to rotational angular velocity)
        does not support large-deflection effects. The theoretical formulations
        for the gyroscopic matrix support small deflection (linear formulation)
        only.

        When large-deflection effects are included in a substructure or CMS
        transient analysis use pass, the OUTRES command ignores DSUBres = ALL.

        This command is also valid in PREP7.

        In ANSYS Professional NLT, large deflection effects should not be
        turned on if 2-D solid (PLANEn) or 3-D solid (SOLIDn) elements are
        defined. ANSYS Professional NLS supports NLGEOM,ON for plane and solid
        elements.
        """
        command = f"NLGEOM,{key}"
        return self.run(command, **kwargs)

    def nlhist(
        self,
        key="",
        name="",
        item="",
        comp="",
        node="",
        elem="",
        shell="",
        layer="",
        stop_value="",
        stop_cond="",
        **kwargs,
    ):
        """Specify result items to track during solution.

        APDL Command: NLHIST

        Parameters
        ----------
        key
            Specifies the command operation:

            NSOL - Nodal solution data.

            ESOL - Element nodal data.

            PAIR  - Contact data (for pair-based contact).

            GCN - Contact data (for general contact).

            STAT - Displays a list of items to track.

            OFF or 0 - Deactivates tracking of all variables. This value is the default.

            ON or 1 - Activates tracking of all variables.  Tracking also activates whenever any
                      specification changes.

            DEL - Removes the specified variable from the set of result items to track. If Name =
                  ALL (default), all specifications are removed.

        name
            The 32-character user-specified name.

        item, comp
            Predetermined output item and component label for valid elements.
            See the Element Reference for more information.

        node
            Number identifying one of the following:

        elem
            Valid element number for element results. Used for ESOL items. If
            ELEM is specified, then a node number that belongs to the element
            must also be specified in the NODE field.

        shell
            Valid labels are TOP, MID or BOT. This field can specify the
            location on shell elements for which to retrieve data. Used only
            for element nodal data (ESOL).

        layer
            Layer number (for layered elements only). Used only for element
            nodal data (ESOL).

        stop_value
            Critical value of the tracked variable. This value is used to
            determine if the analysis should be terminated. This field is only
            valid for contact data (Key = PAIR or GCN).

        stop_cond
            Specifies the conditional relationship between the variable being
            tracked and the STOP_VALUE upon which the analysis will be
            terminated:

            -1 - Terminate the analysis when the tracked variable is less than or equal to
                 STOP_VALUE.

            0 - Terminate the analysis when the tracked variable equals STOP_VALUE.

            1 - Terminate the analysis when the tracked variable is greater than or equal to
                STOP_VALUE.

        Notes
        -----
        The NLHIST command is a nonlinear diagnostics tool that enables you to
        monitor diagnostics results of interest in real time during a solution.

        You can track a maximum of 50 variables during solution. The specified
        result quantities are written to the file Jobname.nlh. Nodal results
        and contact results are written for every converged substep
        (irrespective of the OUTRES command setting) while element results are
        written only at time points specified via the OUTRES command. For time
        points where element results data is not available, a very small number
        is written instead. If the conditions for contact to be established are
        not satisfied, 0.0 will be written for contact results.

        Results tracking is available only for a nonlinear structural analysis
        (static or transient), a nonlinear steady-state thermal analysis, or a
        transient thermal analysis (linear or nonlinear). All results are
        tracked in the Solution Coordinate System (that is, nodal results are
        in the nodal coordinate system and element results are in the element
        coordinate system).

        Contact results can be tracked for elements CONTA171 through CONTA177;
        they cannot be tracked for CONTA178.

        When contact results are tracked (Key = PAIR or GCN), the user-
        specified name (Name argument) is used to create a user-defined
        parameter. This enables you to monitor the parameter during solution.
        As an example, you can use a named parameter to easily convert the
        contact stiffness units from FORCE/LENGTH3 to FORCE/LENGTH based on the
        initial contact area CAREA. Be sure to specify Name using the APDL
        parameter naming convention.

        The STOP_VALUE and STOP_COND arguments enable you to automatically
        terminate the analysis when a desired value for a tracked contact
        result has been reached. This capability is only available for contact
        variables (Key = PAIR or GCN).

        The Jobname.nlh file is an ASCII file that lists each time point at
        which a converged solution occurs along with the values of the relevant
        result quantities.

        The GUI option Solution> Results tracking provides an interface to
        define the result items to be tracked. The GUI also allows you to graph
        one or more variables against time or against other variables during
        solution. You can use the interface to graph or list variables from any
        .nlh file generated by the ANSYS program.

        You can also track results during batch runs. Either access the ANSYS
        Launcher and select File Tracking from the Tools menu, or type
        nlhist162 at the command line. Use the supplied file browser to
        navigate to your Jobname.nlh file, and click on it to invoke the
        tracking utility. You can use this utility to read the file at any
        time, even after the solution is complete (the data in the file must be
        formatted correctly).

        Table: 205:: : NLHIST - Valid NSOL Item and Component Labels

        For SHELL131 and SHELL132 elements with KEYOPT(3) = 0 or 1, use the
        labels TBOT, TE2, TE3, . . ., TTOP instead of TEMP.

        For SHELL131 and SHELL132 elements with KEYOPT(3) = 0 or 1, use the
        labels HBOT, HE2, HE3, . . ., HTOP instead of HEAT.

        Table: 206:: : NLHIST - Valid ESOL Item and Component Labels
        """
        command = f"NLHIST,{key},{name},{item},{comp},{node},{elem},{shell},{layer},{stop_value},{stop_cond}"
        return self.run(command, **kwargs)

    def nlmesh(self, control="", val1="", val2="", val3="", val4="", **kwargs):
        """Controls remeshing in nonlinear adaptivity.

        APDL Command: NLMESH

        Parameters
        ----------
        control
            The mesh-quality control to adjust:

            NANG  - Specifies the surface facet dihedral angle threshold. Use this option to retain
                    source mesh geometry features. The dihedral angle is
                    defined by the angle between the normal vectors from two
                    neighboring surface facet sharing an edge. If the dihedral
                    angle is larger than the specified threshold, the edge is
                    treated as soft edge so that the new nodes are forced to
                    the edge.

            VAL1 is the dihedral angle threshold (in degrees) on concave surfaces. VAL2 is the dihedral angle threshold (in degrees) on convex surfaces.  - Default: VAL1 = 15 and VAL2 = 15.

            When NLMESH,EXPL is issued, the VAL1 and VAL2 become the lower bounds of dihedral angles for mesh exploration. Use VAL3 and VAL4 to define the upper bounds of dihedral angles on concave and convex surfaces (respectively) for mesh exploration. - Generally, larger VAL1 and VAL2 values lead to better quality new meshes (and
                              may even repair local tiny facets of poor
                              quality); however, larger values may also smooth
                              out some geometric features, leading to slightly
                              different results and causing possible
                              convergence difficulty in the substeps
                              immediately following remeshing.

            AEDG  - Specifies the edge angle threshold (in degrees). Use this option to split patch
                    segments. The edge angle is the angle between adjacent
                    surface segment edges sharing a node. If the edge angle is
                    larger than the specified threshold (VAL1), the segment
                    splits and the node is automatically treated as a hard node
                    to be retained.

            Default: VAL1 = 10. - Generally, larger VAL1 values improve the quality of the new mesh, but may
                              result in fewer feature nodes. The effect is
                              similar to that of dihedral angles.

            SRAT  - Specifies the global sizing ratio for remeshing.

            Generally, set the lower value (VAL1) to >= 0.7 and the upper value (VAL2) to <= 1.5. Within this range, the model can be refined (< 1.0) or coarsened (> 1.0) up to 3x depending on the number of elements (if performing a remesh of the entire model). - Default: VAL1 = 1.0. The default value results in the new mesh having a similar
                              size as that of the source mesh.

            NLAY - Specifies the number of sculpting layers beginning with detected seed elements.
                   This option helps to detect remeshing regions from whole
                   model.

            Default: VAL1 = 2. - Generally, a larger VAL1 value leads to larger remeshing regions and tends to
                              unite isolated multiple regions. A larger value
                              also tends to result in better remeshing quality
                              (and increases mapping and solution overhead
                              accordingly).

            VAL1 = 0 is not valid, as the remeshing regions would contain only detected seed elements, resulting in many small cavities within remeshing regions (especially if the specified skewness threshold (NLADAPTIVE) is relatively large). - When NLMESH,EXPL is issued, VAL1 becomes the lower bound of mesh exploration.
                              Use VAL2 to define the upper bound for mesh
                              exploration.

            LSRT  - Specifies the local sizing ratio threshold (VAL1). If the length of adjacent
                    segments over that of surface short segments exceeds the
                    specified threshold ratio, the neighboring segments are
                    candidates for local sizing to improve target mesh quality.

            Use local sizing in cases where any of the following conditions exist: - Short edges significantly smaller than average

            Poor surface mesh (triangles) on top edges - Small surface patches composed of few triangles caused by small user-specified
                              dihedral angles.

            Valid values are VAL1 >= 1.0. Default: VAL1 = 1.0. - When NLMESH, EXPL is issued, VAL1 becomes the lower bound of mesh exploration.
                              Use VAL2 to define the upper bound for mesh
                              exploration.

            For more information about this control, see "Notes". - EXPL

            Specifies the nonlinear mesh-exploration behavior. Mesh exploration consists of trying various mesh controls to obtain the best quality mesh during remeshing process. - For more information about this control, see "Notes".

            LIST  - Lists all defined advanced control parameters.

        val1, val2, val3, val4
            Numerical input values that vary according to the specified Control
            option.

        Notes
        -----
        NLMESH is a global control command enabling mesh-quality adjustments
        for remeshing in nonlinear adaptivity. The command can be used when
        components are associated with mesh-quality criteria (NLADAPTIVE with
        Criterion = MESH).

        Issue the NLMESH command only in cases where advanced mesh-quality
        control is desirable for remeshing in nonlinear adaptivity. The
        settings specified by this command apply to all components having mesh-
        quality-based criteria defined.

        Following are LSRT usage examples to help you determine a suitable
        threshold value for the local sizing ratio:

        If the value is only slightly greater than the minimum (and default)
        value of 1.0, local sizing is imposed on all segments. Recommended:
        VAL1 > 1.1.

        If the value is large enough such that no neighboring segments have
        lengths that would cause the threshold ratio to be exceeded, all
        segments are treated as though local sizing is disabled.

        For mesh exploration (NLMESH,EXPL,VAL1):

        VAL1 = 0 -- The exception to the default behavior (no mesh exploration)
        occurs when remeshing fails to create a mesh for the user-specified
        NLMESH input parameters. In this case, mesh exploration is performed as
        though VAL1 = 1, with default NANG upper bounds of 60,60 in order to
        continue the solution, and the lower bounds being user-specified.

        VAL1 = 1 -- The NANG lower and upper bounds must be input; otherwise,
        the command is ignored. The upper bound can be input for NLAY also, but
        the exploration still triggers remeshings with the whole model as seed
        elements.

        VAL1 = 2 -- The NANG lower and upper bounds must be input; otherwise,
        the command is ignored.

        VAL1 = 3 -- An optional upper bound can be specified via LSRT. By
        default, the upper bound is set to be 30 percent more than the (user-
        specified) lower bound.

        Mesh exploration is needed only when it is difficult to obtain a good
        quality mesh via standard remeshing. It is good practice to first try
        less aggressive exploration with VAL1 = 1.
        """
        command = f"NLMESH,{control},{val1},{val2},{val3},{val4}"
        return self.run(command, **kwargs)

    def nropt(self, option1="", option2="", optval="", **kwargs):
        """Specifies the Newton-Raphson options in a static or full transient

        APDL Command: NROPT
        analysis.

        Parameters
        ----------
        option1
            Option key:

            AUTO - Let the program choose the option (default).

            FULL - Use full Newton-Raphson.

            MODI - Use modified Newton-Raphson.

            INIT - Use the previously computed matrix (initial-stiffness).

            UNSYM - Use full Newton-Raphson with unsymmetric matrices of elements where the
                    unsymmetric option exists.

        option2
            Option key:

            CRPL  - When applicable in a static creep analysis, activates modified Newton-Raphson
                    with a creep-ratio limit. Valid only when Option1 = AUTO.

        optval
            If Option2 is blank, Optval is the Adaptive Descent Key (Adptky):

            ON - Use adaptive descent (default if frictional contact exists). Explicit ON is
                 valid only if Option = FULL.

            OFF - Do not use adaptive descent (default in all other cases).

        Notes
        -----
        The NROPT command specifies the Newton-Raphson option used to solve the
        nonlinear equations in a static or full transient analysis.

        The automatic modified Newton-Raphson procedure with creep-ratio limit
        control (NROPT,AUTO,CRPL,CRLIMIT) applies to static creep analysis
        only. When the creep ratio is smaller than the value of the creep ratio
        limit specified, the modified Newton-Raphson procedure is used. If
        convergence difficulty occurs during solution, use the full Newton-
        Raphson procedure.

        The command NROPT,UNSYM is also valid in a linear non-prestressed modal
        analysis that is used to perform a brake squeal analysis. In this
        special case, the command is used only to generate the unsymmetric
        stiffness matrix; no Newton-Raphson iterations are performed.

        NROPT,MODI and NROPT,INIT are only applicable with the sparse solver
        (EQSLV,SPARSE). Thermal analyses will always use full Newton-Raphson
        irrespective of the Option1 value selected.

        See Newton-Raphson Option in the Structural Analysis Guide for more
        information.

        This command is also valid in PREP7.

        Switching Between the Symmetric and Unsymmetric Option

        Normally, switching from the symmetric Newton-Raphson option
        (NROPT,FULL) to the unsymmetric option (NROPT,UNSYM) or from the
        unsymmetric option to the symmetric option is allowed between load
        steps within the same analysis type. This is applicable to linear and
        nonlinear, static and full transient analyses.

        Under the following circumstances, the solution could be slightly
        different or inaccurate if you switch from symmetric to unsymmetric or
        vice versa:

        The underlying elements or materials are unsymmetric by their
        mathematical definition, and you switch from unsymmetric to symmetric.

        You change analysis types and also switch from symmetric to unsymmetric
        (or vice versa) at the same time. This situation could result in
        failures such as data corruption or a core dump and should therefore be
        avoided.

        In some rare cases, switching between the symmetric and unsymmetric
        options can cause a system core dump when reading/writing the .ESAV or
        .OSAV file, and the analysis terminates. Typically, this happens when
        the record length of the element nonlinear saved variables cannot be
        altered between load steps by their mathematical definition.

        If all the elements and the material are symmetric by their
        mathematical definition and you use the unsymmetric option, the
        solution accuracy is the same as the symmetric option. However, the
        analysis will run twice as slow as the symmetric case.

        If the static or full transient solution is used as the base analysis
        for a linear perturbation, be aware that switching to the unsymmetric
        Newton-Raphson option forces the program to use the UNSYM or DAMP
        eigensolver in a downstream modal analysis, which may be more expensive
        than symmetric modal analysis.
        """
        command = f"NROPT,{option1},{option2},{optval}"
        return self.run(command, **kwargs)

    def pred(self, sskey="", lskey="", **kwargs):
        """Activates a predictor in a nonlinear analysis.

        APDL Command: PRED

        Parameters
        ----------
        sskey
            Substep predictor key:

            OFF - No prediction occurs.

            ON - Use a predictor on all substeps after the first.

            AUTO - The program uses a predictor but, within certain
                   exceptions, automatically switches prediction
                   off. This behavior is the default; see "Command
                   Default" for details.

        lskey
            Load step predictor:

            OFF - No prediction across load steps occurs. This is the
                  default behavior.

            ON - Use a predictor also on the first substep of the load
                 step. (Sskey = ON is required.)

        Notes
        -----
        Activates a predictor in a nonlinear analysis on the
        degree-of-freedom solution for the first equilibrium iteration
        of each substep.

        When using the arc-length method (ARCLEN, ARCTRM), you cannot
        issue the DOF solution predictor command (PRED), the automatic
        time stepping command (AUTOTS), or the line search command
        (LNSRCH). If you activate the arc-length method after you set
        PRED, AUTOTS, or LNSRCH, a warning message appears. If you
        elect to proceed with the arc-length method, the program
        disables your DOF predictor, automatic time stepping, and line
        search settings, and the time step size is controlled by the
        arc- length method internally.

        When using step-applied loads, such as TUNIF, BFUNIF, etc., or
        other types of non-monotonic loads, the predictor may
        adversely affect the convergence. If the solution is
        discontinuous, the predictor may need to be turned off.

        When performing a nonlinear analysis involving large
        rotations, the predictor may require using smaller substeps.

        This command is also valid in PREP7.
        """
        command = f"PRED,{sskey},,{lskey}"
        return self.run(command, **kwargs)

    def pstres(self, key="", **kwargs):
        """Specifies whether prestress effects are calculated or included.

        APDL Command: PSTRES

        Parameters
        ----------
        key
            Prestress key:

            OFF - Do not calculate (or include) prestress effects (default).

            ON - Calculate (or include) prestress effects.

        Notes
        -----
        The PSTRES command specifies whether or not prestress effects are to be
        calculated or included. The command should be issued after the ANTYPE
        command.

        Prestress effects are calculated in a static or transient analysis for
        inclusion in a buckling, modal, harmonic (Method = FULL), or
        substructure generation analysis. If used in the solution processor
        (/SOLU), this command is valid only within the first load step.

        If you apply thermal body forces during a static analysis to calculate
        prestress effects, do not delete the forces during any subsequent full
        harmonic analyses. If you delete the thermal body forces, the thermal
        prestress effects will not be included in the harmonic analysis.
        Temperature loads used to define the thermal prestress will also be
        used in the full harmonic analysis as sinusoidally time-varying
        temperature loads.

        A prestress effect applied with non-follower loads resists rigid body
        rotation of the model. For example, an unsupported beam with axial
        tensile forces applied to both ends will have two nonzero rotational
        rigid body modes.

        If tabular loading (``*DIM,,TABLE``) was used in the prestress static
        analysis step, the corresponding value of TIME will be used for tabular
        evaluations in the modal analysis.

        This command is also valid in PREP7.
        """
        command = f"PSTRES,{key}"
        return self.run(command, **kwargs)
