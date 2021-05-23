"""Pythonic MAPDL Commands"""

class _MapdlCommands():  # pragma: no cover
    """ANSYS class containing MAPDl functions."""    

    
    
    
    
    
    def wait(self, dtime="", **kwargs):
        """APDL Command: /WAIT

        Causes a delay before the reading of the next command.

        Parameters
        ----------
        dtime
            Time delay (in seconds). Maximum time delay is 59 seconds.

        Notes
        -----
        You should consider using ``time.sleep(dtime)``

        The command following the /WAIT will not be processed until the
        specified wait time increment has elapsed.  Useful when reading from a
        prepared input file to cause a pause, for example, after a display
        command so that the display can be reviewed for a period of time.
        Another "wait" feature is available via the *ASK command.

        This command is valid in any processor.
        """
        command = "/WAIT,%s" % (str(dtime))
        return self.run(command, **kwargs)

    
    def pdsave(self, fname="", ext="", **kwargs):
        """APDL Command: PDSAVE

        Writes the probabilistic model data to a file.

        Parameters
        ----------
        fname
            File name and directory path (248 characters maximum, including the
            characters needed for the directory path).  An unspecified
            directory path defaults to the working directory; in this case, you
            can use all 248 characters for the file name.

        ext
            Filename extension (eight-character maximum).

        Notes
        -----
        Writes the probabilistic model data to a file. Saved data include
        probabilistic data only; the results of the probabilistic analyses are
        not stored in the file (rather, these are stored in separate result
        files).
        """
        command = "PDSAVE,%s,%s" % (str(fname), str(ext))
        return self.run(command, **kwargs)

    
    
    def slashdscale(self, wn="", dmult="", **kwargs):
        """APDL Command: /DSCALE

        Sets the displacement multiplier for displacement displays.

        Parameters
        ----------
        wn
            Window number (or ALL) to which command applies (defaults to 1).

        dmult
            AUTO or 0

            AUTO or 0 - Scale displacements automatically so that maximum  displacement (vector
                        amplitude) displays as 5 percent of the maximum model
                        length, as measured in the global Cartesian X, Y, or Z
                        directions.

            1 - Do not scale displacements (i.e., scale displacements by 1.0, true to
                geometry).  Often used with large deflection results.

            FACTOR - Scale displacements by numerical value input for FACTOR.

            OFF - Remove displacement scaling (i.e., scale displacements by 0.0, no distortion).

            USER - Set DMULT to that used for last display (useful when last DMULT value was
                   automatically calculated).

        Notes
        -----
        If Multi-Plots are not being displayed, and the current device is a 3-D
        device [/SHOW,3D], then the displacement scale in all active windows
        will be the same, even if separate /DSCALE commands are issued for each
        active window. For efficiency, ANSYS 3-D graphics logic maintains a
        single data structure (segment), which contains only one displacement
        scale. The program displays the same segment (displacement scale) in
        all windows. Only the view settings will be different in each of the
        active windows.

        This command is valid in any processor.
        """
        command = "/DSCALE,%s,%s" % (str(wn), str(dmult))
        return self.run(command, **kwargs)

    
    
    
    
    def pdvar(self, name="", type_="", par1="", par2="", par3="", par4="",
              **kwargs):
        """APDL Command: PDVAR

        Specifies the parameters to be treated as probabilistic design
        variables.

        Parameters
        ----------
        name
            Parameter name (must be a scalar ANSYS parameter). The parameter
            must have been previously defined as a random input variable or a
            random output parameter with the PDVAR command. See the *SET
            command for restrictions about ANSYS parameters.

        type\_
            Probabilistic design variable type. This is the statistical
            distribution type. For more information on each of these types, see
            Probabilistic Design in the Advanced Analysis Guide.

            BETA - Beta distributed random variable.

            PAR1 = Shape parameter. Defaults to 2.0. - PAR2 = Shape parameter. Defaults to 2.0.

            PAR3 = Lower minimum value. Defaults to 0.0.  - PAR4 = Upper maximum value. Defaults to 1.0.

            EXPO - Exponential distributed random variable.

            PAR1 = Decay parameter λ. Must be larger then 0.0 and defaults to 1.0.  - PAR2 = Shift or minimum value. Defaults to 0.0.

            PAR3, PAR4 are ignored. - GAMA

            Gamma distributed random variable. - PAR1 = Decay parameter λ. Must be larger then 0.0 and defaults to 1.0.

            PAR2 = Exponential parameter k. Must be larger then 0.0 and defaults to 1.0.  - PAR3, PAR4 are ignored. Exponential distributed random variable.

            GAUS - Gaussian (Normal) distributed random variable.

            PAR1 = Mean value. Defaults to 0.0. - PAR2 = Standard deviation. Must be larger then 0.0 and defaults to 1.0.

            PAR3, PAR4 are ignored. - LOG1

            Lognormal distributed random variable specified directly with the statistical parameters mean value and standard deviation. - PAR1 = Mean value. Must be larger then 0.0 and defaults to 1.0.

            PAR2 = Standard deviation. Must be larger then 0.0 and defaults to 1.0. - PAR3, PAR4 are ignored.

            LOG2 - Lognormal distributed random variable specified with the statistical parameters
                   mean value and standard deviation of the logarithm of the
                   random values.

            PAR1 and PAR2 must also be defined. PAR1 = Mean value of the logarithm of the data. Defaults to 0.0.  - PAR2 = Standard deviation of the logarithm of the data. Must be larger then 0.0
                              and defaults to 1.0.

            PAR3, PAR4 are ignored. - UNIF

            Uniform distributed random variable. Note that PAR1 must be less than PAR2. - PAR1 = Minimum value. Defaults to 0.0.

            PAR2 = Maximum value. Defaults to 1.0. - PAR3, PAR4 are ignored.

            TGAU - Truncated Gaussian distributed random variable. Note that PAR3 must be less
                   than PAR4.

            PAR1 = Mean value of the untruncated Gaussian distribution. Defaults to 0.0. -  PAR2 = Standard deviation of the untruncated Gaussian distribution. Must be
                              larger then 0.0 and defaults to 1.0.

            PAR3 = Minimum value and lower truncation boundary. Defaults to -3.0. - PAR4 = Maximum value and upper truncation boundary. Defaults to +3.0.

            TRIA - Triangular distributed random variable. Note that PAR1 must be less than PAR2
                   which must be less than PAR3.

            PAR1 = Minimum value. Defaults to 0.0.  - PAR2 = Most Likely Value (MLV). Defaults to 0.5.

            PAR3 = Maximum value. Defaults to 1.0.  - PAR4 is ignored.

            WEIB - Weibull (Type III smallest) distributed random variable. Note that PAR2 must be
                   greater than PAR3. If PAR3 = 0.0, the random distribution is
                   equivalent to a two-parameter Weibull distribution.

            PAR1 = Weibull exponent. Must be larger then 0.0 and defaults to 1.0. - PAR2 = Characteristic value. Must be larger then 0.0 and defaults to 1.0.

            PAR3 = Shift or minimum value. Defaults to 0.0. - PAR4 is ignored.

            RESP - Random output or response parameter.PAR1 to PAR4 are not used.

            DEL - Deletes this probabilistic design variable (does not delete the ANSYS
                  parameter). This option is only valid if the parameter Name
                  was previously defined as a probabilistic design variable
                  (using Type = BETA, ..., WEIB or Type = RESP). The parameter
                  retains the value assigned during the last probabilistic
                  design loop.PAR1 to PAR4 are not used.

        par1, par2, par3, par4
            Parameters of the distribution function. The parameters must be
            specified according to the requirements of the individual
            distribution types described above.

        Notes
        -----
        Specifies the parameters to be treated as probabilistic design
        variables. A random input variable is specified by the name of the
        ANSYS parameter, the type of the distribution function (Type) and its
        distribution parameters (PAR1, ..., PAR4). A random output parameter is
        specified by the name of the ANSYS parameter and the type identifying
        it as a random output parameter (Type = RESP).
        """
        command = "PDVAR,%s,%s,%s,%s,%s,%s" % (str(name), str(type_), str(par1), str(par2), str(par3), str(par4))
        return self.run(command, **kwargs)

    
    
    
    def del_(self, val1="", val2="", **kwargs):
        """APDL Command: *DEL

        Deletes a parameter or parameters (GUI).

        Parameters
        ----------
        val1
            Command behavior key:

            Delete all user-defined parameters, or all user-defined parameters and all system parameters, as specified by Val2. - Delete the parameter(s) specified by Val2.

        val2
            The parameter or parameters to delete (used only when Val1 = ALL or
            (blank)):

            When Val1 is (blank), specifies the location of the parameter within the Array Parameters dialog box.  The location number is based on an alphabetically ordered list of all parameters in the database.   - When Val1 is ALL, deletes all parameters, including those named with a leading
                              underscore (_) (except _STATUS and _RETURN). When
                              Val1 is (blank), deletes only those parameters
                              named with a leading underscore (_) (except
                              _STATUS and _RETURN).

            When Val1 is (blank), deletes only those parameters named with a trailing underscore (_).  - When Val1 is ALL, a (blank) value for Val2 causes all user-defined parameters
                              to be deleted.

        Notes
        -----
        This is a command generally created by the graphical user interface
        (GUI).  It appears in the log file (Jobname.LOG) if an array parameter
        is deleted from within the Array Parameters dialog.

        Usage examples:

        Delete all user-defined parameters: *DEL,ALL

        Delete only those user-defined parameters named with a trailing
        underscore: *DEL,,PRM_

        Delete all user-defined and all system parameters (except for _STATUS
        and _RETURN): *DEL,ALL,_PRM

        Delete a parameter by specifying its location within the Array
        Parameters dialog: *DEL,,LOC

        Delete a single specified parameter by name: *DEL,ParmName (You cannot
        specify more than one named parameter at a time.)

        This command is valid in any processor.
        """
        command = "*DEL,%s,%s" % (str(val1), str(val2))
        return self.run(command, **kwargs)

    
    
    
    def starexit(self, **kwargs):
        """APDL Command: *EXIT

        Exits a do-loop.

        Notes
        -----
        The command following the *ENDDO is executed next. The exit option may
        also be conditional [Use the *IF].  The *EXIT command must appear on
        the same file as the  *DO command.

        This command is valid in any processor.
        """
        command = "*EXIT,"
        return self.run(command, **kwargs)

    
    def pivcheck(self, key="", prntcntrl="", **kwargs):
        """APDL Command: PIVCHECK

        Controls the behavior of an analysis when a negative or zero equation
        solver pivot value is encountered.

        Parameters
        ----------
        key
            Determines whether to stop or continue an analysis when a negative
            or zero equation solver pivot value is encountered:

            AUTO - Check for negative or zero pivot values for analyses performed with the sparse
                   and PCG solvers. When one is encountered, an error or
                   warning is issued, per various criteria relating to the type
                   of analysis being solved. An error causes the analysis to
                   stop; a warning allows the analysis to continue. A negative
                   pivot value may be valid for some nonlinear and multiphysics
                   analyses (for example, electromagnetic and thermal
                   analyses); this key has no effect in these cases.

            ERROR - Check for negative or zero pivot values for analyses performed with the sparse
                    and PCG solvers. When one is encountered, an error is
                    issued, stopping the analysis. A negative pivot value may
                    be valid for some nonlinear and multiphysics analyses (for
                    example, electromagnetic and thermal analyses); this key
                    has no effect in these cases.

            WARN - Check for negative or zero pivot values for analyses performed with the sparse
                   and PCG solvers. When one is encountered, a warning is
                   issued and the analysis continues. A negative pivot value
                   may be valid for some nonlinear and multiphysics analyses
                   (for example, electromagnetic and thermal analyses); this
                   key has no effect in these cases.

            OFF - Pivot values are not checked. This key causes the analysis to continue in spite
                  of a negative or zero pivot value.

        prntcntrl
            Provides print options. Print output with these options will be
            sent to the default output file, not to the files created by the
            nonlinear diagnostic tools (NLDIAG).

            ONCE - Print only the maximum and minimum pivot information on the first call to the
                   sparse solver (which is the default solver). This is the
                   default behavior.

            EVERY - Print the maximum and minimum pivot information at every call to the sparse
                    solver. This option is provided for nonlinear analysis
                    diagnostics.

        Notes
        -----
        This command is valid for all analyses. In a nonlinear analysis, a
        negative pivot may be valid. In some cases, rigid body motions in a
        nonlinear analysis will be trapped by error routines checking
        infinitely large displacements (DOF limit exceeded) or nonconvergence
        status. An under-constrained model may avoid the pivot check, but fail
        with a DOF limit exceeded error.

        Machine precision may affect whether a small pivot triggers an error or
        bypasses this checking logic. You may wish to review the ratio of the
        maximum to absolute minimum pivot values. For ratios exceeding 12 to 14
        orders of magnitude, the accuracy of the computed solution may be
        degraded by the severe ill-conditioning of the assembled matrix.

        Note that negative pivots corresponding to Lagrange multiplier based
        mixed u-P elements are not checked or reported by this command.
        Negative pivots arising from the u-P element formulation and related
        analyses can occur and lead to correct solutions.

        This command is also valid in PREP7.
        """
        command = "PIVCHECK,%s,%s" % (str(key), str(prntcntrl))
        return self.run(command, **kwargs)

    
    def pdcorr(self, name1="", name2="", corr="", **kwargs):
        """APDL Command: PDCORR

        Specifies the correlation between two random input variables.

        Parameters
        ----------
        name1
            Parameter name. The parameter must have been previously defined as
            a random input variable with the PDVAR command.

        name2
            Parameter name. The parameter must have been previously defined as
            a random input variable with the PDVAR command. Must be different
            from Name1.

        corr
            Specification of the correlation:

            Value - Sets the correlation coefficient between Name1 and Name2 to the specified
                    value. If this correlation coefficient was already defined
                    it will be changed to this new value. The correlation
                    coefficient must be between -1.0 and +1.0.

            DEL - Delete the previously defined correlation between Name1 and Name2.

        Notes
        -----
        Specifies the correlations between two random input variables. The PDS
        tool generates correlated samples if correlations exist. This applies
        to both probabilistic methods (Monte Carlo Simulation and Response
        Surface Methods).

        If there are correlated random input variables, the sampled locations
        of the random input variables reflect the correlation as illustrated
        below for the case of two standard normal distributed variables X1 and
        X2. The illustrations show no correlation (correlation coefficient
        0.0), a relatively moderate negative correlation (correlation
        coefficient -0.6), and a relative strong positive correlation
        (correlation coefficient 0.9).

        : : :
        """
        command = "PDCORR,%s,%s,%s" % (str(name1), str(name2), str(corr))
        return self.run(command, **kwargs)

    
    def pdclr(self, type_="", **kwargs):
        """APDL Command: PDCLR

        Clears the probabilistic design database.

        Parameters
        ----------
        type\_
            Specifies the part of the probabilistic database to be cleared.

            ALL - Clear the entire probabilistic database. Both the preprocessing and
                  postprocessing parts are cleared.

            POST - Clear only the postprocessing part of the probabilistic database. This is
                   necessary if you want to modify the deterministic model (the
                   analysis file) or probabilistic model (random variables,
                   correlations between random variables, or the random output
                   parameter) after a probabilistic analysis has already been
                   performed.

        Notes
        -----
        Clears the probabilistic design system (PDS) database. The settings are
        reset to their default values and the memory is cleared. Remember that
        the result files containing the results of the probabilistic loops are
        never deleted unless you intentionally delete them. We recommend that
        you use this command before switching to a new probabilistic analysis
        using a different probabilistic model (a different analysis loop file
        or deterministic model), or changing random input variables, their
        correlations, or random output parameters. Clearing the probabilistic
        database is not necessary if the probabilistic model remains the same
        and will be analyzed with a different probabilistic method or different
        method options. See the PDEXE command for restrictions. Before issuing
        the PDCLR command, you should save the probabilistic database using the
        PDSAVE command.
        """
        command = "PDCLR,%s" % (str(type_))
        return self.run(command, **kwargs)

    
    
    
    def staopt(self, method="", **kwargs):
        """APDL Command: STAOPT

        Specifies static analysis options.

        Parameters
        ----------
        method
            Solution method for the static analysis:

            DEFA - Standard ANSYS solve (default).

            VT - Solve with Variational Technology.

        Notes
        -----
        Specifies the method of solution for a static analysis (ANTYPE,STATIC).
        If used in SOLUTION, this command is valid only within the first load
        step.

        The VT option is valid for either thermal or structural nonlinear
        analyses, where it attempts to reduce the total number of iterations.

        This command is also valid in PREP7.

        Distributed ANSYS Restriction: The VT static solution method is not
        supported in Distributed ANSYS.
        """
        command = "STAOPT,%s" % (str(method))
        return self.run(command, **kwargs)

    
    
    def pdmeth(self, method="", samp="", **kwargs):
        """APDL Command: PDMETH

        Specifies the probabilistic analysis method.

        Parameters
        ----------
        method
            Label for the probabilistic analysis method.

            MCS - Monte Carlo Simulation

            RSM - Response Surface Method

        samp
            Label for the sampling techniques. The sampling technique
            determines the values of the random input variables during the
            simulation loops.

            DIR - Direct or Crude Monte Carlo Sampling. This technique randomly samples the
                  random input variables according to their distribution
                  functions without "memory" of previous simulations.

            The parameters for a Monte Carlo Simulation using direct sampling are specified with the PDDMCS command. - LHS

            Latin Hypercube Sampling (default). Valid only for Method = MCS. For this sampling technique the random input variables are sampled randomly according to their distribution functions, efficiently stratifying the samples into layers and avoiding the re-use of those layers. The sampling process has a "memory" of previous simulations, which prevents accumulation of clusters of samples. In addition, this sampling strategy forces the extreme ends of a distribution function to participate in the sampling. This generally leads to smoother distribution functions of the sampled set. - The parameters for a Monte Carlo Simulation using Latin-Hypercube sampling are
                              specified with the PDLHS command.

            USER - User specified sampling. Valid only for Method = MCS. In this case you provide
                   a file containing the sampling "points" (values) of all
                   random input variables for all simulation loops. These
                   samples are simply executed and it is your responsibility to
                   specify the samples correctly. The probabilistic design
                   system can perform only limited checks on the samples you
                   provide. ANSYS allows Monte Carlo specific postprocessing
                   operations on the results generated with user-specified
                   samples. The parameters for the user-supplied sampling
                   technique are specified with the PDUSER command.

            CCD - Central Composite Design. Valid only for Method = RSM. A central composite
                  design is composed of a center point, axis points, and corner
                  points, called factorial points. Using large numbers of
                  random input variables produces prohibitively large numbers
                  of factorial points; therefore, ANSYS automatically reduces
                  the number of factorial points by switching to a fractional
                  plan for the factorial part of the design. See the PDDOEL
                  command for more information.

            Note:This option is only valid for 2 to 20 random input variables. You will receive an error if you have specified fewer than 2 or more than 20 random input variables. - BBM

            Box-Behnken Matrix Design. Valid only for Method = RSM. A Box-Behnken Matrix design is composed of a center point plus the points at the middle of the edges of the hypercube in the space of random input variables. A Box-Behnken design might be advantageous if the corner points of the hypercube represent very extreme conditions that are undesirable and therefore should not be used for the sampling.  See the PDDOEL command for more information. - Note:  This option is only valid for 3 to 12 random input variables. You will
                              receive an error if you have specified fewer than
                              3 or more than 12 random input variables.

            USER - User specified sampling. In this case you provide a file containing the
                   sampling "points" (values) of all random input variables for
                   all simulation loops. These samples are simply executed and
                   it is your responsibility to specify the samples correctly.
                   The PDS can perform only limited checks on the samples you
                   provide, if user-supplied sampling technique are specified
                   with the PDUSER command.

        Notes
        -----
        Specifies the probabilistic analysis method and the sampling technique
        used for the individual probabilistic analysis method.
        """
        command = "PDMETH,%s,%s" % (str(method), str(samp))
        return self.run(command, **kwargs)

    
    def vfsm(self, action="", encl="", opt="", maxiter="", conv="", **kwargs):
        """APDL Command: VFSM

        Adjusts view factor matrix to satisfy reciprocity and/or row sum
        properties.

        Parameters
        ----------
        action
            Action to be performed:

            Define - Define a view factor summation (default)

            Clear - Resets the scaling method to 0 for all enclosures. All subsequent arguments are
                    ignored.

            Status - Outputs the OPT value for each enclosure in the model.

        encl
            Previously defined enclosure number for the view factor adjustment.

        opt
            Option key:

            0 - The view factor matrix values are not adjusted (default).

            1 - The view factor matrix values are adjusted so that the row sum equals 1.0.

            2 - The view factor matrix values are adjusted so that the row sum equals 1.0 and
                the reciprocity relationship is satisfied.

            3 - The view factor matrix values are adjusted so that the original row sum is
                maintained.

            4 - The view factor matrix values are adjusted so that the original row sum is
                maintained and the reciprocity relationship is satisfied.

        maxiter
            Maximum number of iterations to achieve convergence. Valid only
            when OPT = 2 or 4. Default is 100.

        conv
            Convergence value for row sum. Iterations will continue (up to
            MAXITER) until the maximum residual over all the rows is less than
            this value. Valid only when OPT = 2 or 4. Default is 1E-3.

        Notes
        -----
        To have a good energy balance, it is important to satisfy both the row
        sum and reciprocity relationships. For more information, see View
        Factors in the Mechanical APDL Theory Reference.

        OPT = 1 and 2 are suitable for perfect enclosures. OPT = 1 is less
        expensive than OPT = 2 because no iterations are involved. However,
        with OPT = 1, the reciprocity relationship is not satisfied.

        OPT = 3 and 4 are suitable for leaky enclosures. OPT = 3 is less
        expensive than OPT = 4 because no iterations are involved. However,
        with OPT = 3, the reciprocity relationship is not satisfied.

        The VFSM command must be used before VFOPT is issued, or Solve is
        initiated.
        """
        command = "VFSM,%s,%s,%s,%s,%s" % (str(action), str(encl), str(opt), str(maxiter), str(conv))
        return self.run(command, **kwargs)

    
    
    
    def fatigue(self, **kwargs):
        """APDL Command: FATIGUE

        Specifies "Fatigue data status" as the subsequent status topic.

        Notes
        -----
        This is a status [STAT] topic command.  Status topic commands are
        generated by the GUI and will appear in the log file (Jobname.LOG) if
        status is requested for some items under Utility Menu> List> Status.
        This command will be immediately followed by a STAT command, which will
        report the status for the specified topic.

        If entered directly into the program, the STAT command should
        immediately follow this command.
        """
        command = "FATIGUE,"
        return self.run(command, **kwargs)

    
    
    
    
    
    
    
    def pdpinv(self, rlab="", name="", prob="", conf="", **kwargs):
        """APDL Command: PDPINV

        Prints the result of the inversion of a probability.

        This command is no longer supported in V18.2 and newer

        Parameters
        ----------
        rlab
            Result set label. Identifies the result set to be used for
            postprocessing. A result set label can be the solution set label
            you defined in a PDEXE command (if you are directly postprocessing
            Monte Carlo Simulation results), or the response surface set label
            defined in an RSFIT command (for Response Surface Analyses).

        name
            Parameter name. The parameter must have been previously defined as
            a random input variable or a random output parameter with the PDVAR
            command.

        prob
            Target probability for which the random parameter value should be
            determined.

        conf
            Confidence level. The confidence level is used to print the
            confidence bounds on the random parameter value. The value for the
            confidence level must be between 0.0 and 1.0 and it defaults to
            0.95 (95%). Printing of confidence bound is suppressed for CONF
            0.5. This parameter is ignored for response surface methods results
            postprocessing.

        Notes
        -----
        Prints the value for the random parameter Name at which the probability
        that there are simulation values lower than that value is equal to
        PROB. This corresponds to an inversion of the cumulative distribution
        function (see PDCDF command) at a given probability. In this sense the
        PDPINV is doing the opposite of the PDPROB command. The PDPROB command
        evaluates a probability for a given random parameter value and the
        PDPINV command evaluates the random parameter value that corresponds to
        a given probability.

        If Rlab is left blank, then the result set label is inherited from the
        last PDEXE command (Slab), RSFIT command (RSlab), or the most recently
        used PDS postprocessing command where a result set label was explicitly
        specified.

        The confidence level is a probability expressing the confidence that
        the value for the requested result is in fact between the confidence
        bounds. The larger the confidence level, the wider the confidence
        bounds. Printing the confidence bounds only makes sense for
        postprocessing Monte Carlo simulation results, where the confidence
        bounds represent the accuracy of the results. With increasing sample
        sizes, the width of the confidence bounds gets smaller for the same
        confidence level. For response surface analysis methods, the number of
        simulations done on the response surface is usually very large;
        therefore, the accuracy of the results is determined by the response
        surface fit and not by the confidence level.

        The PDPINV command cannot be used to postprocess the results in a
        solution set that is based on Response Surface Methods, only Monte
        Carlo Simulations.
        """
        return self.run(f"PDPINV,{rlab},{name},{prob},,{conf}", **kwargs)

    
    
    
    def torq2d(self, **kwargs):
        """APDL Command: TORQ2D

        Calculates torque on a body in a magnetic field.

        Notes
        -----
        TORQ2D invokes an ANSYS macro which calculates mechanical torque on a
        body in a magnetic field.  The body must be completely surrounded by
        air (symmetry permitted), and a closed path [PATH] passing through the
        air elements surrounding the body must be available.  A
        counterclockwise ordering of nodes on the PPATH command will give the
        correct sign on the torque result.  The macro is valid for 2-D planar
        analysis.

        The calculated torque is stored in the parameter TORQUE.  A node plot
        showing the path is produced in interactive mode.  The torque is
        calculated using a Maxwell stress tensor approach.  Path operations are
        used for the calculation, and all path items are cleared upon
        completion.  See the TORQC2D command for torque calculation based on a
        circular path.
        """
        command = "TORQ2D,"
        return self.run(command, **kwargs)

    
    
    
    def ugin(self, name="", extension="", path="", entity="", layer="", fmt="",
             **kwargs):
        """APDL Command: ~UGIN

        Transfers an NX part into the ANSYS program.

        Parameters
        ----------
        name
            The file name of the NX part to be imported, which cannot exceed 64
            characters in length. The path name must begin with an alphanumeric
            character. Special characters such as &, -,  and * are not
            permitted in the part name.

        extension
            The NX part file extension. The default is .prt.

        path
            The full path name to the directory containing the part, enclosed
            in single quotes; for example, '/ug_parts'. The default is the
            current working directory.

        entity
            Entity to be imported.

            0 or Solid - Solids only, imported as ANSYS volumes (the default).

            1 or Surface - Surfaces only, imported as ANSYS areas.

            2 or Wireframe - Wireframe only, imported as ANSYS lines.

            3 or All - All entities. Use this option when the part contains entities that may not be
                       attached to each other, such as a solid in one location
                       and a surface in another.

        layer
            The number(s) assigned to the layer(s) to be imported. You can
            import one layer or a range of layers (designated by hyphens).
            Defaults to 1-256 (all layers).

        fmt
            The format in which ANSYS will store the model.

            0 - Neutral format (default). Defeaturing after import is restricted.

            1 - Solid format; this allows defeaturing after import.

        Notes
        -----
        More information on importing NX parts is available in UG/NX in the
        Connection User's Guide.
        """
        command = "~UGIN,%s,%s,%s,%s,%s,%s" % (str(name), str(extension), str(path), str(entity), str(layer), str(fmt))
        return self.run(command, **kwargs)

    
    
    
    def plst(self, fname="", ext="", parmplot="", mslvstep="", **kwargs):
        """APDL Command: PLST

        Plots sound power parameters vs. frequency, or postprocesses results
        for a random acoustics analysis with diffuse sound field.

        Parameters
        ----------
        fname
            File name and directory path of a sound power data file (248
            characters maximum, including the characters needed for the
            directory path). The sound power data file is created via the
            SPOWER command macro. An unspecified directory path defaults to the
            working directory; in this case, you can use all 248 characters for
            the file name. When postprocessing a random acoustics analysis, a
            file named Fname is generated if no file already exists.

        ext
            Extension of the sound power data file (.anp where n is the number
            of ports), or the random acoustics data file.  When postprocessing
            a random acoustics analysis, an extension named Ext is assigned if
            no extension already exists.

        parmplot
            Specified parameter to plot:

            LWIN  - Input sound power level (default)

            LWOUT  - Output sound power level at driven port

            RL - Return loss

            ALPHA - Absorption coefficient

            TL  - Transmission loss

            DFSTL   - Transmission loss of random acoustics analysis

            DFSPW - Radiated power in random acoustics analysis

        mslvstep
            Solution step (load step) of a random acoustics analysis (MSOLVE):

            0  - Average result of multiple samplings (default)

            > 0 - Result at the specified solution step (load step)

            ALL  - Average of all solution step (load step) results

        Notes
        -----
        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = "PLST,%s,%s,%s,%s" % (str(fname), str(ext), str(parmplot), str(mslvstep))
        return self.run(command, **kwargs)

    
    
    def fsdele(self, nloc="", nev="", nlod="", **kwargs):
        """APDL Command: FSDELE

        Deletes a stress condition for a fatigue location, event, and loading.

        Parameters
        ----------
        nloc
            Delete stresses associated with location NLOC.  Defaults to zero.

        nev
            Delete stresses associated with event NEV.  Defaults to zero.

        nlod
            Delete stresses associated with loading NLOD.  Defaults to zero.

        Notes
        -----
        Deletes a stress condition stored for a particular fatigue location,
        event, and loading.  Use FE command to delete all stresses for a
        particular event or FL command to delete all stresses for a particular
        location.
        """
        command = "FSDELE,%s,%s,%s" % (str(nloc), str(nev), str(nlod))
        return self.run(command, **kwargs)

    
    def pddoel(self, name="", method="", vtype="", lopt="", val1="", val2="",
               val3="", val4="", val5="", **kwargs):
        """APDL Command: PDDOEL

        Defines design of experiment levels for an individual random input
        variable.

        Parameters
        ----------
        name
            Parameter name. The parameter name must have been previously
            defined as a random input variable using the PDVAR command.

        method
            Specifies the response surface method for which the levels of the
            design of experiment are to be defined. This field must not be left
            blank.

            CCD - Use the Central Composite Design method. The design experiment levels of a
                  central composite design are defined in the fields VAL1 to
                  VAL5.

            BBM - Use the Box-Behnken Matrix method. The design experiment levels of a Box-
                  Behnken Matrix design are defined in the fields VAL1 to VAL3.
                  The fields VAL4 and VAL5 are ignored

        vtype
            Specifies the type of the values of the design of experiment
            levels.

            PROB - The design of experiment levels are specified in terms of probabilities. This
                   is the default.

            PHYS - The design of experiment levels are specified in terms of physical values.

        lopt
            Specifies the type of the design of experiment levels, indicating
            if they are defined by lower and upper bound only (default) or all
            specified by the user.

            BND - You specify the lower and upper bounds for the design of experiment levels. The
                  values for intermediate levels are calculated automatically
                  at run time (default). The lower and upper levels of the
                  design of experiment itself can be specified either in terms
                  of probabilities or in terms of physical values, depending on
                  the Vtype field.

            For Lopt = BND and Method = CCD only the entries VAL1 and VAL5 are processed and they represent the lower and upper bound values of a central composite design. The intermediate levels VAL2 to VAL4 are evaluated automatically. For Lopt = BND and Method = BBM only the entries VAL1 and VAL3 are processed and they represent the lower and upper bound values of a Box-Behnken Matrix design respectively. The intermediate level VAL2 is evaluated automatically. - NOTE: The intermediate levels between the lower and upper bounds are calculated
                              so they are at equal intervals along the curve
                              (interpolated linearly in the physical space
                              whether the curve is symmetrical or not)
                              regardless of whether the lower and upper bounds
                              are specified as probabilities (Vtype = PROB) or
                              as physical values (Vtype = PHYS).

            ALL - You explicitly specify all necessary design of experiment levels. The design of
                  experiment levels can be in terms of probabilities or in
                  terms of physical values, depending on the Vtype field.

        val1, val2, val3, . . . , val5
            Values for the levels of the design of experiment for the random
            input variable Name. Must be specified in ascending order. All
            probabilities must be between 0.0 and 1.0.

        Notes
        -----
        If Vtype = PHYS, you must enter values for VAL1 through VAL3 or VAL5
        (depending on the Method and Lopt option you choose). If Vtype = PROB
        and you do not enter values, they default to the values shown below.

        For Method = CCD:

        For Method = BBM:

        See Probabilistic Design in the Advanced Analysis Guide for more
        information on the PDS methods.
        """
        command = "PDDOEL,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (str(name), str(method), str(vtype), str(lopt), str(val1), str(val2), str(val3), str(val4), str(val5))
        return self.run(command, **kwargs)

    def ftcalc(self, nloc="", node="", **kwargs):
        """APDL Command: FTCALC

        Performs fatigue calculations for a particular node location.

        Parameters
        ----------
        nloc
            Location number of stress conditions to be used for fatigue
            calculation.

        node
            Node number (used only for convenience if NLOC is not input).
        """
        command = "FTCALC,%s,%s" % (str(nloc), str(node))
        return self.run(command, **kwargs)

    
    
    def wmore(self, node1="", node2="", ninc="", itime="", inc="", **kwargs):
        """APDL Command: WMORE

        Adds more nodes to the starting wave list.

        Parameters
        ----------
        node1, node2, ninc
            Add another node set to the previous starting wave list.  Set is
            NODE1 to NODE2 (defaults to NODE1) in steps of NINC (defaults to
            1).  If NODE1 is negative, delete (instead of add) this node set
            from previous starting wave list.

        itime, inc
            Add other node sets to the same starting wave list by repeating the
            previous node set with NODE1 and NODE2 incremented by INC (defaults
            to 1) each time after the first.  ITIME is the total number of sets
            (defaults to 1) defined with this command.

        Notes
        -----
        Adds more nodes to (or modifies) the previous starting wave list (if
        any) [WSTART].  Repeat WMORE command to add more nodes to the previous
        starting wave list.  Up to 10,000 nodes may be defined (total, for all
        starting waves).

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = "WMORE,%s,%s,%s,%s,%s" % (str(node1), str(node2), str(ninc), str(itime), str(inc))
        return self.run(command, **kwargs)

    
    
    def proein(self, name="", extension="", path="", proecomm="", **kwargs):
        """APDL Command: ~PROEIN

        Transfers a Creo Parametric part into the ANSYS program.

        Parameters
        ----------
        name
            The name of the Creo Parametric part to be imported, which cannot
            exceed 64 characters in length and must begin with an alphanumeric
            character. Special characters such as & - and * and spaces are not
            permitted in the part name.

        extension
            The general Creo Parametric extension format is prt for parts and
            asm for assemblies.

        path
            Full path name to the directory containing the part. The default is
            the current working directory.

        proecomm
            The start command for the version of Creo Parametric you are using.
            proe1 is the default command. Note that the full path name to the
            Creo Parametric command need not be used here if the path had been
            included in the PATH variable. The Creo Parametric command name is
            set by the PROE_START_CMD162 environment variable.

        Notes
        -----
        More information on importing Creo Parametric parts is available in
        Creo Parametric (formerly Pro/ENGINEER) in the Connection User's Guide.
        """
        command = "~PROEIN,%s,%s,%s,%s" % (str(name), str(extension), str(path), str(proecomm))
        return self.run(command, **kwargs)

    
    
    def satin(self, name="", extension="", path="", entity="", fmt="", nocl="",
              noan="", **kwargs):
        """APDL Command: ~SATIN

        Transfers a .SAT file into the ANSYS program.

        Parameters
        ----------
        name
            The name of a valid .SAT file, created with a supported version of
            ACIS. The first character of the file name must be an alphanumeric.
            Special characters such as & - and * and spaces are not permitted
            in the part name. See File Names in the Command Reference for more
            information about ANSYS file naming conventions.

        extension
            The extension for the file. The default extension is .sat.

        path
            The path name of the directory in which the file resides enclosed
            in single quotes. The default path name is the current working
            directory.

        entity
            Entity to be imported.

            SOLIDS - Solids only, imported as ANSYS volumes (Not implemented, imports All).

            SURFACES - Surfaces only, imported as ANSYS areas (Not implemented, imports All).

            WIREFRAME - Wireframe only, imported as ANSYS lines (Not implemented, imports All).

            ALL - All entities. Use this option when the file contains different types of
                  entities.

        fmt
            The format in which ANSYS will store the model.

            0 - Neutral format (default). Defeaturing after import is restricted.

            1 - Solid format; this allows defeaturing after import.

        nocl
            Remove tiny objects.

            0 - Remove tiny objects without checking model validity (default).

            1 - Do not remove tiny objects.

        noan
            Perform an ACIS analysis of the model.

            0 - Analyze the model (default).

            1 - Do not analyze the model.

        Notes
        -----
        More information on importing ACIS parts is available in ACIS in the
        Connection User's Guide.
        """
        command = "~SATIN,%s,%s,%s,%s,%s,%s,%s" % (str(name), str(extension), str(path), str(entity), str(fmt), str(nocl), str(noan))
        return self.run(command, **kwargs)

    def pdropt(self, rvar="", corr="", stat="", shis="", hist="", cdf="",
               sens="", cmat="", conf="", **kwargs):
        """APDL Command: PDROPT

        Specifies the options for an HTML report.

        Parameters
        ----------
        rvar
            Specifies in which form to show the definitions of random variables
            in the report.

            0 - Using tables (including name and distribution parameter) and figures (including
                a probability density function plot and a cumulative
                distribution plot) (default).

            1 - Using tables only.

            2 - Using figures only.

            3 - None.

        corr
            Specifies if a table describing the correlation between random
            variables should be included in the report.

            0 - Yes, include this table (default).

            1 - No, do not include this table.

        stat
            Specifies which statistics to include in the report. In general,
            statistics are provided in a tabular form.

            0 - Statistics of the random output parameters only (default).

            1 - Statistics of the random input variables only.

            2 - Statistics of both the random input variables and the random output parameters.

            3 - None.

        shis
            Specifies which sample history plots to include in the report. This
            option applies to the random output parameters only.

            0 - None (default).

            1 - Mean value and standard deviation as a sample plot.

            2 - Mean value, standard deviation and sample values as a sample plot.

            3 - All types of sample plots - mean value, standard deviation, minimum value,
                maximum values, and the sample values.

        hist
            Specifies which histogram plots to include in the report.

            0 - Histogram of the random output parameters only (default).

            1 - Histogram of the random input variables only.

            2 - Histogram of both the random input variables and the random output parameters.

            3 - None.

        cdf
            Specifies which cumulative distribution function (CDF) plots to
            include in the report.

            0 - CDF of the random output parameters only (default).

            1 - CDF of the random input variables only.

            2 - CDF of both the random input variables and the random output parameters.

            3 - None.

        sens
            Specifies which sensitivity plots to include in the report.

            0 - Plots the sensitivities for all random output parameters based on Spearman-
                rank-order correlation coefficient (default).

            1 - Plots the sensitivities for all random output parameters based on linear
                (Pearson) correlation coefficient.

            2 - Plots the sensitivities according to option SENS=1 and SENS=2.

            3 - None.

        cmat
            Specifies which correlation matrices to include in the report.

            0 - Correlation matrix between random output parameters and random output
                parameters only (default).

            1 - Correlation matrix between random input variables and random output parameters
                only.

            2 - Correlation matrix between random input variables and random input variables
                only.

            3 - Correlation matrices according to option CMAT=0 and CMAT=1.

            4 - Correlation matrices according to option CMAT=0 and CMAT=2.

            5 - Correlation matrices according to option CMAT=1 and CMAT=2.

            6 - Correlation matrices according to option CMAT=0, CMAT=1, and CMAT=2.

            7 - None.

        conf
            Confidence level. The confidence level is used to plot confidence
            bounds for the history value. The value for the confidence level
            must be between 0.0 and 1.0 and it defaults to 0.95 (95%).
            Confidence bound(s) plotting is suppressed for CONF  0.5. This
            option is ignored if the report does not include plots for which
            confidence bounds are applicable.

        Notes
        -----
        Specifies the options for an HTML report. An HTML report includes a
        description of the deterministic model, the probabilistic model, the
        probabilistic methods used for the analyses, and the results obtained
        from the analyses.  The deterministic model is documented in the report
        by including a link to the analysis file (see PDANL command). In
        addition, an element plot of the component is shown, if available,
        based on the current view settings. The command ALLSEL is issued
        automatically prior to the respective plot command.
        """
        command = "PDROPT,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (str(rvar), str(corr), str(stat), str(shis), str(hist), str(cdf), str(sens), str(cmat), str(conf))
        return self.run(command, **kwargs)

    
    def werase(self, **kwargs):
        """APDL Command: WERASE

        Erases all reordering wave lists.

        Notes
        -----
        The REORDER then STAT commands will display the current wave lists.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = "WERASE,"
        return self.run(command, **kwargs)

    
    
    
    
    def hmagsolv(self, freq="", nramp="", cnva="", cnvv="", cnvc="", cnve="",
                 neqit="", **kwargs):
        """APDL Command: HMAGSOLV

        Specifies 2-D or axisymmetric harmonic magnetic solution options and
        initiates the solution.

        Parameters
        ----------
        freq
            Analysis frequency (Hz).

        nramp
            Number of ramped substeps for the first load step of a nonlinear
            2-D harmonic electromagnetic solution.  Defaults to 3.  If NRAMP =
            -1, ignore the ramped load step entirely.

        cnva
            Convergence tolerance on the program calculated reference value for
            the magnetic vector potential degree of freedom.  Defaults to
            0.001.

        cnvv
            Convergence tolerance on the program calculated reference value for
            the time-integrated electric potential VOLT.    Defaults to 0.001.

        cnvc
            Convergence tolerance on the program calculated reference value for
            the current degree of freedom CURR.  Defaults to 0.001.

        cnve
            Convergence tolerance on the program calculated reference value for
            the voltage drop degree of freedom EMF.  Defaults to 0.001.

        neqit
            Maximum number of equilibrium iterations per load step.  Defaults
            to 50.

        Notes
        -----
        HMAGSOLV invokes an ANSYS macro which specifies harmonic
        electromagnetic solution options and initiates the solution.  The macro
        is applicable to any ANSYS 2-D or axisymmetric linear or nonlinear
        harmonic analysis.  Results are only stored for the final converged
        solution.  (In POST1, issue *SET,LIST to identify the load step of
        solution results.)  The macro internally determines if a nonlinear
        analysis is required based on magnetic material properties defined in
        the database.

        The macro performs a two-load-step solution sequence.  The first load
        step ramps the applied loads over a prescribed number of substeps
        (NRAMP), and the second load step calculates the converged solution.
        For linear problems, only a single load step solution is performed.
        The ramped load step can be bypassed by setting NRAMP to -1.

        A 3-D harmonic electromagnetic analysis is available for linear
        solutions only and does not require this solution macro.

        The following analysis options and nonlinear options are controlled by
        this macro:  KBC, NEQIT, NSUBST, CNVTOL, OUTRES.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = "HMAGSOLV,%s,%s,%s,%s,%s,%s,%s" % (str(freq), str(nramp), str(cnva), str(cnvv), str(cnvc), str(cnve), str(neqit))
        return self.run(command, **kwargs)

    def output(self, fname="", ext="", loc="", **kwargs):
        """APDL Command: /OUTPUT

        Redirects text output to a file or to the screen.

        Parameters
        ----------
        fname
            Filename and directory path (248 character maximum, including
            directory) to which text output will be redirected (defaults to
            Jobname if Ext is specified).  For interactive runs, Fname = TERM
            (or blank) redirects output to the screen.  For batch runs, Fname =
            blank (with all remaining command arguments blank) redirects output
            to the  default system output file.

        ext
            Filename extension (eight-character maximum).

        loc
            Location within a file to which output will be written:

            (blank) - Output is written starting at the top of the file (default).

            APPEND - Output is appended to the existing file.

        Notes
        -----
        Text output includes responses to every command and GUI
        function, notes, warnings, errors, and other informational
        messages.  Upon execution of /OUTPUT,Fname, Ext, ..., all
        subsequent text output is redirected to the file Fname.Ext.
        To redirect output back to the default location, issue /OUTPUT
        (no arguments).

        Note: When using the GUI, output from list operations [NLIST,
        DLIST, etc.] is always sent to a list window regardless of the
        /OUTPUT setting.  The output can then be saved on a file or
        copied to the /OUTPUT location using the File menu in the list
        window.

        This command is valid in any processor.
        """
        if loc:
            return self.run(f"/OUTPUT,{fname},{ext},,{loc}", **kwargs)
        else:
            return self.run(f"/OUTPUT,{fname},{ext}", **kwargs)

    
    def catiain(self, name="", extension="", path="", blank="", **kwargs):
        """APDL Command: ~CATIAIN

        Transfers a CATIA model into the ANSYS program.

        Parameters
        ----------
        name
            The name of a valid CATIA model, created with CATIA 4.x or
            lower.  The first character of the file name must be an
            alphanumeric.  Special characters such as & - and * and
            spaces are not permitted in the part name.

        extension
            The extension for the file. The default extension is .model.

        path
            The path name of the directory in which the file resides, enclosed
            in single quotes. The default path name is the current working
            directory.

        blank
            Sets whether to import "blanked" entities.

            0 - Does not import "blanked" (suppressed) CATIA entities (default).

            1 - Imports "blanked" entities. The portions of CATIA data
            that were suppressed will be included in the import.

        Notes
        -----
        More information on importing CATIA parts is available in CATIA V4 in
        the Connection User's Guide.
        """
        return self.run(f"~CATIAIN,{name},{extension},{path},,,{blank}", **kwargs)

    
    
    
    
    
    def fssect(self, rho="", nev="", nlod="", kbr="", **kwargs):
        """APDL Command: FSSECT

        Calculates and stores total linearized stress components.

        Parameters
        ----------
        rho
            In-plane (X-Y) average radius of curvature of the inside and
            outside surfaces of an axisymmetric section.  If zero (or blank), a
            plane or 3-D structure is assumed.  If nonzero, an axisymmetric
            structure is assumed.  Use a suitably large number (see the
            Mechanical APDL Theory Reference) or use -1 for an axisymmetric
            straight section.

        nev
            Event number to be associated with these stresses (defaults to 1).

        nlod
            Loading number to be associated with these stresses (defaults to
            1).

        kbr
            For an axisymmetric analysis (RHO ≠ 0):

            0 - Include the thickness-direction bending stresses

            1 - Ignore the thickness-direction bending stresses

            2 - Include the thickness-direction bending stress using the same formula as the Y
                (axial direction ) bending stress. Also use the same formula
                for the shear stress.

        Notes
        -----
        Calculates and stores the total linearized stress components at the
        ends of a section path [PATH] (as defined by the first two nodes with
        the PPATH command). The path must be entirely within the selected
        elements (that is, there must not be any element gaps along the path).
        Stresses are stored according to the fatigue event number and loading
        number specified.  Locations (one for each node) are associated with
        those previously defined for these nodes [FL] or else they are
        automatically defined.  Stresses are separated into six total
        components (SX through SXZ) and six membrane-plus-bending (SX through
        SXZ) components.  The temperature at each end point and the current
        time are also stored along with the total stress components.
        Calculations are made from the stresses currently in the database (last
        SET or LCASE command).  Stresses are stored as section coordinate
        components if axisymmetric or as global Cartesian coordinate components
        otherwise, regardless of the active results coordinate system [RSYS].
        The FSLIST command may be used to list stresses.  The FS command can be
        used to modify stored stresses.  See also the PRSECT and PLSECT
        commands for similar calculations.
        """
        command = "FSSECT,%s,%s,%s,%s" % (str(rho), str(nev), str(nlod), str(kbr))
        return self.run(command, **kwargs)

    
    
    def felist(self, nev1="", nev2="", ninc="", **kwargs):
        """APDL Command: FELIST

        Lists the fatigue event parameters.

        Parameters
        ----------
        nev1, nev2, ninc
            List event parameters from NEV1 (defaults to 1) to NEV2 (defaults
            to NEV1) in steps of NINC (defaults to 1).  If NEV1 = ALL, NEV2 and
            NINC are ignored and all events are listed.  Fatigue event
            parameters are defined with the FE command.
        """
        command = "FELIST,%s,%s,%s" % (str(nev1), str(nev2), str(ninc))
        return self.run(command, **kwargs)

    
    
    def pds(self, **kwargs):
        """APDL Command: /PDS

        Enters the probabilistic design system.

        Notes
        -----
        Enters the Probabilistic Design System (PDS). This command is valid
        only at the Begin Level.
        """
        command = "/PDS,"
        return self.run(command, **kwargs)

    
    
    def starset(self, par="", value="", val2="", val3="", val4="", val5="",
                val6="", val7="", val8="", val9="", val10="", **kwargs):
        """APDL Command: *SET

        Assigns values to user-named parameters.

        Parameters
        ----------
        par
            An alphanumeric name used to identify this parameter.  Par may be
            up to 32 characters, beginning with a letter and containing only
            letters, numbers, and underscores.  Examples:  ABC   A3X   TOP_END.
            ANSYS command names, function names, label names, component and
            assembly names, etc., should not be used.  Parameter names
            beginning with an underscore (e.g.,  _LOOP) are reserved for use by
            ANSYS and should be avoided.  Parameter names ending in an
            underscore are not listed by the *STATUS command.  Array parameter
            names must be followed by a subscript, and the entire expression
            must be 32 characters or less.  Examples:  A(1,1)   NEW_VAL(3,2,5)
            RESULT(1000).  There is no character parameter substitution for the
            Par field. Table parameters that are used in command fields (where
            constant values are normally given) are limited to 32 characters.

        value
            Numerical value or alphanumeric character string (up to 32
            characters enclosed in single quotes) to be assigned to this
            parameter.  Examples:  A(1,3)=7.4 B='ABC3'.  May also be a
            parameter or a parametric expression.  Examples:  C=A(1,3)
            A(2,2)=(C+4)/2.  If blank, delete this parameter.  Example:  A=
            deletes parameter A.

        val2, val3, val4, val5, val6, val7, val8, val9, val10
            If Par is an array parameter, values VAL2 through VAL10 (up to the
            last nonblank value) are sequentially assigned to the succeeding
            array elements of the column.  Example:  *SET,A(1,4),10,11 assigns
            A(1,4)=10, A(2,4)=11.  *SET,B(2,3),'file10','file11' assigns
            B(2,3)='file10', B(3,3)='file11'.

        Notes
        -----
        Assigns values to user-named parameters that may be substituted later
        in the run.  The equivalent (and recommended) format is

        Par = VALUE,VAL2,VAL3, . . . , VAL10

        which may be used in place of  *SET,Par, : ... for convenience.

        This command is valid in any processor.

        Parameters (numeric or character) may be scalars (single valued) or
        arrays (multiple valued in one, two, or three dimensions). An unlimited
        number of parameter names may be defined in any ANSYS run. For very
        large numbers of parameters, it is most efficient to define them in
        alphabetical order.

        Parameter values may be redefined at any time.  Array parameters may
        also be assigned values within a do-loop [*DO] for convenience.
        Internally programmed do-loop commands are also available with the *VXX
        commands (*VFILL).  Parameter values (except for parameters ending in
        an underscore) may be listed with the  *STATUS command, displayed with
        the *VPLOT   command (numeric parameters only), and modified with the
        *VEDIT command (numeric parameters only).

        Older ANSYS-supplied macro files may use parameter names that do not
        begin with an underscore. Using these macros embedded in your own
        macros may cause conflicts if the same parameter names are used.

        Parameters can also be resolved in comments created by the /COM command
        (see /COM for complete documentation). A parameter can be deleted by
        redefining it with a blank  VALUE.  If the parameter is an array, the
        entire array is deleted.  Parameters may also be defined by a response
        to a query with the  *ASK command or from an "ANSYS-supplied" value
        with the *GET command.

        Array parameters must be dimensioned  [*DIM] before being assigned
        values unless they are the result of an array operation or defined
        using the implied loop convention. Scalar parameters that are not
        defined are initialized to a "near" zero value.  Numeric array
        parameters are initialized to zero when dimensioned, and character
        array parameters are initialized to blank.  An existing array parameter
        must be deleted before it can be redimensioned.  Array parameter names
        must be followed by a subscript list (enclosed in parentheses)
        identifying the element of the array.  The subscript list may have one,
        two, or three values (separated by commas).  Typical array parameter
        elements are  A(1,1), NEW_VAL(3,2,5), RESULT(1000).  Subscripts for
        defining an array element must be integers (or parameter expressions
        that evaluate to integers).  Non-integer values are rounded to the
        nearest integer value.  All array parameters are stored as 3-D arrays
        with the unspecified dimensions set to 1.  For example, the 4th array
        element of a 1-dimensional array, A(4), is stored as array element
        A(4,1,1).  Arrays are patterned after standard FORTRAN conventions.

        If the parameter name Par is input in a numeric argument of a command,
        the numeric value of the parameter (as assigned with *SET, *GET, =,
        etc.) is substituted into the command at that point.  Substitution
        occurs only if the parameter name is used between blanks, commas,
        parentheses, or arithmetic operators (or any combination) in a numeric
        argument.  Substitution can be prevented by enclosing the parameter
        name Par within single quotes ( ' ), if the parameter is alone in the
        argument; if the parameter is part of an arithmetic expression, the
        entire expression must be enclosed within single quotes to prevent
        substitution.  In either case the character string will be used instead
        of the numeric value (and the string will be taken as 0.0 if it is in a
        numeric argument).

        A forced substitution is available in the text fields of the /TITLE,
        /STITLE,  /TLABEL, /AN3D, /SYP (ARG1--ARG8), and *ABBR  commands by
        enclosing the parameter within percent (%) signs.  Also, parameter
        substitution may be forced within the file name or extension fields of
        commands having these fields by enclosing the parameter within percent
        (%) signs.  Array parameters  [*DIM] must include a subscript (within
        parentheses) to identify the array element whose value is to be
        substituted, such as A(1,3).  Out-of-range subscripts result in an
        error message.  Non-integer subscripts are allowed when identifying a
        TABLE array element for substitution.  A proportional linear
        interpolation of values among the nearest array elements is performed
        before substitution.  Interpolation is done in all three dimensions.

        Note:: : Interpolation is based upon the assigned index numbers which
        must be defined when the table is filled [*DIM].

        Most alphanumeric arguments permit the use of character parameter
        substitution.  When the parameter name Par input, the alphanumeric
        value of the parameter is substituted into the command at that point.
        Substitution can be suppressed by enclosing the parameter name within
        single quotes ( ' ).  Forced substitution is available in some fields
        by enclosing the parameter name within percent (%) signs.  Valid forced
        substitution fields include command name fields, Fname (filename) or
        Ext (extension) arguments, *ABBR command (Abbr arguments), /TITLE and
        /STITLE commands (Title argument) and /TLABEL command (Text argument).
        Character parameter substitution is also available in the  *ASK, /AN3D,
        *CFWRITE,  *IF,  *ELSEIF,   *MSG,  *SET,  *USE,  *VREAD, and  *VWRITE
        commands.   Character array parameters must include a subscript (within
        parentheses) to identify the array element whose value is to be
        substituted.

        If a parameter operation expression is input in a numeric argument, the
        numeric value of the expression is substituted into the command at that
        point.  Allowable operation expressions are of the form

        E1oE2oE3: ...oE10

        where E1, E2, etc. are expressions connected by operators (o).  The
        allowable operations (o) are

        + - * / ** < >

        For example, A+B**C/D*E is a valid operation expression.  The *
        represents multiplication and the ** represents exponentiation.
        """
        command = "*SET,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (str(par), str(value), str(val2), str(val3), str(val4), str(val5), str(val6), str(val7), str(val8), str(val9), str(val10))
        return self.run(command, **kwargs)

    
    
    def parain(self, name="", extension="", path="", entity="", fmt="",
               scale="", **kwargs):
        """APDL Command: ~PARAIN

        Transfers a Parasolid file into the ANSYS program.

        Parameters
        ----------
        name
            The name of a valid Parasolid file. The first character of the file
            name must be an alphanumeric.

        extension
            The extension for the file. The default extension is .x_t on a PC
            or .xmt_txt on a Linux system. Parasolid files are compatible
            across systems, and do not need to be renamed to be used on another
            platform.

        path
            The path name of the directory in which the file resides, enclosed
            in single quotes. The default path name is the current working
            directory.

        entity
            Entity to be imported:

            SOLIDS - Solids only, imported as ANSYS volumes (default)

            SURFACES - Surfaces only, imported as ANSYS areas.

            WIREFRAME - Wireframe only, imported as ANSYS lines.

            ALL - All entities. Use this option when the file contains more than one type of
                  entity.

        fmt
            Sets the format in which ANSYS will store the model

            0 - Neutral format (default). Defeaturing after import is restricted. Use this
                option if you need to scale a model to a specific unit of
                measure (other than meters).

            1 - Solid format; this allows defeaturing after import.

        scale
            Allows scaling for the model

            0 - Do not rescale the model; retain the default Parasolid setting of meters
                (default).

            1 - Scale the model if warranted by the model size.

        Notes
        -----
        More information on importing Parasolid parts is available in Parasolid
        in the Connection User's Guide.
        """
        command = "~PARAIN,%s,%s,%s,%s,%s,%s" % (str(name), str(extension), str(path), str(entity), str(fmt), str(scale))
        return self.run(command, **kwargs)

    
    def wfront(self, kprnt="", kcalc="", **kwargs):
        """APDL Command: WFRONT

        Estimates wavefront statistics.

        Parameters
        ----------
        kprnt
            Wavefront history print key:

            0 - Print current wavefront statistics.

            1 - Print current wavefront statistics but also print wavefront history (wavefront
                at each element).  Elements are listed in the reordered
                sequence.

        kcalc
            Calculation options:

            0 - Wavefront estimate assumes maximum model DOF set at each node and does not
                include the effects of master degrees of freedom and specified
                displacement constraints.

            1 - Wavefront estimate uses the actual DOF set at each node and does not include
                the effects of master degrees of freedom and specified
                displacement constraints.  More time consuming than estimated
                wavefront.  KPRNT = 1 is not available with this option.

        Notes
        -----
        Estimates wavefront statistics of the model as currently ordered.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = "WFRONT,%s,%s" % (str(kprnt), str(kcalc))
        return self.run(command, **kwargs)

    
    
    
    
    def slashexpand(self, nrepeat1="", type1="", method1="", dx1="", dy1="",
                    dz1="", nrepeat2="", type2="", method2="", dx2="", dy2="",
                    dz2="", nrepeat3="", type3="", method3="", dx3="", dy3="",
                    dz3="", **kwargs):
        """APDL Command: /EXPAND

        Allows the creation of a larger graphic display than represented by the
        actual finite element analysis model.

        Parameters
        ----------
        nrepeat1, nrepeat2, nrepeat3
            The number of repetitions required for the element pattern. The
            default is 0 (no expansion).

        type1, type2, type3
            The type of expansion requested.

            RECT - Causes a Cartesian transformation of DX, DY, and DZ for each pattern (default).

            POLAR - Causes a polar transformation of DR, D-Theta and DZ for each pattern.

            AXIS - Causes 2-D axisymmetric expansion (that is, rotates a 2-D model created in the
                   X-Y plane about the Y axis to create a 3-D model).

            LRECT - Causes a Cartesian transformation of DX, DY, and DZ for each pattern about the
                    current local coordinate system (specified via the CSYS
                    command).

            LPOLAR - Causes a polar transformation of DR, D-Theta, and DZ for each pattern about the
                     local coordinate system (specified via the CSYS command).

        method1, method2, method3
            The method by which the pattern is repeated.

            FULL - Causes a normal repeat of the pattern (default).

            HALF - Uses a symmetry transformation for alternate repeats (to produce an image of a
                   complete circular gear from the image of half a tooth, for
                   example).

        dx1, dy1, dz1, dx2, dy2, dz2, dx3, dy3, dz3
            The Cartesian or polar increments between the repeated patterns.
            Also determines the reflection plane. Reflection is about the plane
            defined by the normal vector (DX, DY, DZ). If you want no
            translation, specify a small nonzero value.  For a half-image
            expansion, the increment DX, DY, or DZ is doubled so that
            POLAR,HALF, ,45 produces full images on 90° centers, and RECT,HALF,
            ,1 produces full images on 2-meter centers.

        Notes
        -----
        You can use the /EXPAND command to perform up to three symmetry
        expansions at once (that is, X, Y, and Z which is equal to going from a
        1/8 model to a full model). Polar expansions allow you to expand a
        wheel section into a half wheel, then into the half section, and then
        into the whole.

        The command displays elements/results when you issue the EPLOT command
        or postprocessing commands.

        The command works on all element and result displays, except as noted
        below. As the graphic display is created, the elements (and results)
        are repeated as many times as necessary, expanding the geometry and, if
        necessary, the displacements and stresses.

        Derived results are not supported.

        The /EXPAND command has the following limitations:

        It does not support solid model entities.

        POLAR, FULL or HALF operations are meaningful only in global
        cylindrical systems and are unaffected by the RSYS or DSYS commands.
        Cartesian symmetry or unsymmetric operations also occur about the
        global Cartesian system.

        It does not average nodal results across sector boundaries, even for
        averaged plots (such as those obtained via the PLNSOL command).

        Axisymmetric harmonic element results are not supported for Type =
        AXIS.

        The /EXPAND command differs significantly from the EXPAND command in
        several respects:

        The uses of /EXPAND are of a more general nature, whereas the EXPAND
        command is intended primarily to expand modal cyclic symmetry results.

        /EXPAND does not change the database as does the EXPAND command.

        You cannot print results displayed via /EXPAND.


        """
        command = "/EXPAND,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (str(nrepeat1), str(type1), str(method1), str(dx1), str(dy1), str(dz1), str(nrepeat2), str(type2), str(method2), str(dx2), str(dy2), str(dz2), str(nrepeat3), str(type3), str(method3), str(dx3), str(dy3), str(dz3))
        return self.run(command, **kwargs)

    
    
    def repeat(self, ntot="", vinc1="", vinc2="", vinc3="", vinc4="", vinc5="",
               vinc6="", vinc7="", vinc8="", vinc9="", vinc10="", vinc11="",
               **kwargs):
        """APDL Command: *REPEAT

        Repeats the previous command.

        Parameters
        ----------
        ntot
            Number of times the preceding command is executed (including the
            initial execution).  Must be 2 or greater.  NTOT of 2 causes one
            repeat (for a total of 2 executions).

        vinc1, vinc2,  vinc3, . . . , vinc11
            Value increments applied to first through eleventh data fields of
            the preceding command.

        Notes
        -----
        *REPEAT must immediately follow the command that is to be repeated.
        The numeric arguments of the initial command may be incremented in the
        generated commands.  The numeric increment values may be integer or
        real, positive or negative, zero or blank.  Alphanumeric arguments
        cannot be incremented.  For large values of NTOT, consider printout
        suppression (/NOPR command) first.

        Most commands beginning with slash (/), star (*), as well as "unknown
        command" macros, cannot be repeated.  For these commands, or if more
        than one command is to be repeated, include them within a do-loop. File
        switching commands (those reading additional commands) cannot be
        repeated.  If a *REPEAT command  immediately follows another *REPEAT
        command, the repeat action only applies to the last non-*REPEAT
        command.  Also, *REPEAT should not  be used in interactive mode
        immediately after a) a command (or its log file equivalent) that uses
        picking, or b) a command that requires a response from the user.

        This command is valid in any processor.
        """
        command = "*REPEAT,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (str(ntot), str(vinc1), str(vinc2), str(vinc3), str(vinc4), str(vinc5), str(vinc6), str(vinc7), str(vinc8), str(vinc9), str(vinc10), str(vinc11))
        return self.run(command, **kwargs)

    
    def cycexpand(self, wn="", option="", value1="", value2="", **kwargs):
        """APDL Command: /CYCEXPAND

        Graphically expands displacements, stresses and strains of a cyclically
        symmetric model.

        Parameters
        ----------
        wn
            The window number to which the expansion applies. Valid values are
            1 through 5. The default value is 1. The window number applies only
            to the AMOUNT argument.

        option
            One of the following options:

            ON - Activates cyclic expansion using the previous settings (if any). If no previous
                 settings exist, this option activates the default settings.

            DEFAULT - Resets cyclic expansion to the default settings.

            OFF - Deactivates cyclic expansion. This option is the default.

            STATUS - Lists the current cyclic expansion settings.

            AMOUNT - The number of repetitions or the total angle.

            Value1 - NREPEAT

            Value2 - The number of repetitions. The default is the total number of sectors in 360
                     degrees.

            or - Value1

            ANGLE - Value2

            The total angle in degrees. The default is 360. - WHAT

            A specified portion or subset of the model to expand: - Value1

            The component name of the elements to expand. The default is all selected components. - EDGE

            Sector edge display key. - -1

            Suppresses display of edges between sectors even if the cyclic count varies between active windows. - Caution:  Plots with fewer than the maximum number of repetitions may have
                              missing element faces at the sector boundaries.

            0 or OFF - Averages stresses or strains across sector boundaries. This value is the
                       default (although the default reverts to 1 or ON if the
                       cyclic count varies between active windows).

            1 or ON - No averaging of stresses or strains occurs and sector boundaries are shown on
                      the plot.

            PHASEANG - The phase angle shift:

            Value1 - The phase angle shift in degrees. The valid range is 0 through 360. The default
                     is 0. For a full harmonic solution, this value is
                     typically the phase angle obtained via the CYCPHASE
                     command. If Value1 = AMPLITUDE (or if Value1 ≥ 360), the
                     amplitude is supplied. The amplitude solution for non-
                     component results (such as equivalent stress) are not
                     valid. For a mode-superposition harmonic solution, if
                     Value1 = SWEEP, the maximum values across a phase angle
                     sweep are supplied.

        Notes
        -----
        In preprocessing, the /CYCEXPAND command verifies a cyclically
        symmetric model by graphically expanding it partially or through the
        full 360 degrees.

        For the postprocessing plot nodal solution (PLNSOL) operation, the
        command graphically expands displacements, stresses and strains of a
        cyclically symmetric model partially or though the full 360 degrees by
        combining the real (original nodes and elements) and imaginary
        (duplicate nodes and elements) parts of the solution.

        For the print nodal solution (PRNSOL) operation, the command expands
        the printed output of displacements or stresses on a sector-by-sector
        basis.

        Use of the /CYCEXPAND command does not change the database. The command
        does not modify the geometry, nodal displacements or element stresses.

        The command affects element and result plots only. It has no effect on
        operations other than plot element solution (PLESOL), plot nodal
        solution (PLNSOL), print nodal solution (PRNSOL), and calculate
        harmonic solution (CYCCALC). Operations other than PLESOL, PLNSOL,
        PRNSOL, or CYCCALC work on the unprocessed real and imaginary parts of
        a cyclic symmetry solution

        If you issue a /CYCEXPAND,,OFF command, you cannot then expand the
        model by simply issuing another  /CYCEXPAND command  (for example, to
        specify an NREPEAT value for the number of repetitions). In such a
        case, you must specify /CYCEXPAND,,ON, which activates expansion using
        the previous settings (if any) or the default settings.

        The command requires PowerGraphics and will turn PowerGraphics on
        (/GRAPHICS,POWER) if not already active. Any setting which bypasses
        PowerGraphics (for example, /PBF) also bypasses cyclic expansion; in
        such cases, the /CYCEXPAND command displays unprocessed real and
        imaginary results.

        The CYCPHASE command uses full model graphics (/GRAPHICS,FULL) to
        compute peak values. Because of this, there may be slight differences
        between max/min values obtained with CYCPHASE, and those obtained via
        /CYCEXPAND, which uses power graphics (/GRAPHICS,POWER).

        For PHASEANG = AMPLITUDE (or 360) with a cyclic full harmonic solution,
        the only appropriate coordinate system is the solution coordinate
        system (RSYS,SOLU)

        To learn more about analyzing a cyclically symmetric structure, see the
        Cyclic Symmetry Analysis Guide.
        """
        command = "/CYCEXPAND,%s,%s,%s,%s" % (str(wn), str(option), str(value1), str(value2))
        return self.run(command, **kwargs)

    
    
    def slashline(self, x1="", y1="", x2="", y2="", **kwargs):
        """APDL Command: /LINE

        Creates annotation lines (GUI).

        Parameters
        ----------
        x1
            Line X starting location (-1.0 < X < 2.0).

        y1
            Line Y starting location (-1.0 < Y < 1.0).

        x2
            Line X ending location (-1.0 < X < 2.0).

        y2
            Line Y ending location (-1.0 < Y < 1.0).

        Notes
        -----
        Defines annotation lines to be written directly onto the display at a
        specified location.  This is a command generated by the Graphical User
        Interface (GUI) and will appear in the log file (Jobname.LOG) if
        annotation is used.  This command is not intended to be typed in
        directly in an ANSYS session (although it can be included in an input
        file for batch input or for use with the /INPUT command).

        All lines are shown on subsequent displays unless the annotation is
        turned off or deleted.  Use the /LSPEC command to set the attributes of
        the line.

        This command is valid in any processor.
        """
        command = "/LINE,%s,%s,%s,%s" % (str(x1), str(y1), str(x2), str(y2))
        return self.run(command, **kwargs)

    
    def slashreset(self, **kwargs):
        """APDL Command: /RESET

        Resets display specifications to their initial defaults.

        Notes
        -----
        Resets slash display specifications (/WINDOW, /TYPE, /VIEW, etc.) back
        to their initial default settings (for convenience).  Also resets the
        focus location to the geometric center of the object.

        This command is valid in any processor.
        """
        command = "/RESET,"
        return self.run(command, **kwargs)

    
    def slashexit(self, slab="", fname="", ext="", **kwargs):
        """APDL Command: /EXIT

        Stops the run and returns control to the system.

        Parameters
        ----------
        slab
            Mode for saving the database:

            MODEL - Save the model data (solid model, finite element model, loadings, etc.) only
                    (default).

            SOLU - Save the model data and the solution data (nodal and element results).

            ALL - Save the model data, solution data and post data (element tables, path results,
                  etc.)

            NOSAVE - Do not save any data on File.DB (an existing DB file will not be overwritten).

        fname
            File name and directory path (248 characters maximum, including the
            characters needed for the directory path).  An unspecified
            directory path defaults to the working directory; in this case, you
            can use all 248 characters for the file name.

        ext
            Filename extension (eight-character maximum).

        Notes
        -----
        The current database information may be written on File.DB or a named
        file. If File.DB already exists, a backup file (File.DBB) will also be
        written whenever a new File.DB is written.

        This command is valid in any processor. Issuing this command at any
        point will exit the program.
        """
        command = "/EXIT,%s,%s,%s" % (str(slab), str(fname), str(ext))
        return self.run(command, **kwargs)

    
    
    
    
    def immed(self, key="", **kwargs):
        """APDL Command: IMMED

        Allows immediate display of a model as it is generated.

        Parameters
        ----------
        key
            Immediate mode key:

            0 - Display only upon request, i.e., no immediate display (default with the GUI
                off).

            1 - Display immediately as model is generated (default with the GUI on).

        Notes
        -----
        Allows immediate display of a model (as it is generated) without a
        screen erase or a display request.  Available only during an
        interactive session at a graphics display terminal.  A valid graphics
        device name must first be specified on the /SHOW command.

        The IMMED command allows you to control whether or not the model is
        displayed immediately as it is generated in an interactive session.  By
        default in the GUI, your model will immediately be displayed in the
        Graphics Window as you create new entities (such as areas, keypoints,
        nodes, elements, local coordinate systems, boundary conditions, etc.).
        This is called immediate mode graphics.  Also note that symbols (such
        as boundary conditions, local coordinate system triads, etc.) are shown
        immediately and will be present on subsequent displays unless you "turn
        off" the appropriate symbol using the GUI plot controls function or the
        appropriate graphics specification command.

        An immediate image will also be automatically scaled to fit nicely
        within the Graphics Window -- a feature called automatic scaling.  The
        new scaling is usually apparent on the automatic replot associated with
        immediate mode.  To suppress automatic replot, issue /UIS,REPLOT,0.
        (With automatic replot suppressed, the immediate image may not always
        be automatically scaled correctly.)

        Note:: : An immediate display in progress should not be aborted with
        the usual system "break" feature (or else the ANSYS session itself will
        be aborted).  When you run the ANSYS program interactively without
        using the GUI, immediate mode is off by default.

        This command is valid only in PREP7.
        """
        command = "IMMED,%s" % (str(key))
        return self.run(command, **kwargs)

    
    
    def lsdump(self, enginename="", filename="", **kwargs):
        """APDL Command: *LSDUMP

        Dumps a linear solver engine to a binary File.

        Parameters
        ----------
        enginename
            Name used to identify this engine. Must have been previously
            created using *LSENGINE and factorized using *LSFACTOR.

        filename
            Name of the file to create.

        Notes
        -----
        Dumps a previously factorized linear solver system to a binary file.
        Only LAPACK and BCS linear solvers can be used with this feature. The
        Linear Solver can later be restored with the *LSRESTORE command.

        A BCS Sparse Solver can be dumped only if uses the INCORE memory option
        (see BCSOPTION).
        """
        command = "*LSDUMP,%s,%s" % (str(enginename), str(filename))
        return self.run(command, **kwargs)

    
    
    
    def ddaspec(self, keyref="", shptyp="", mountloc="", deftyp="", amin="",
                **kwargs):
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
        command = "DDASPEC,%s,%s,%s,%s,%s" % (str(keyref), str(shptyp), str(mountloc), str(deftyp), str(amin))
        return self.run(command, **kwargs)

    
    
    
    def slashstatus(self, lab="", **kwargs):
        """APDL Command: /STATUS

        Lists the status of items for the run.

        Parameters
        ----------
        lab
            Items to list status for:

            ALL - List all below (default).

            TITLE - List only titles, Jobname, and revision number.

            UNITS - List only units.

            MEM - List only memory data statistics.

            DB - List only database statistics

            CONFIG - List only configuration parameters.

            GLOBAL - Provides a global status summary.

            SOLU - Provides a solution status summary.

            PROD - Provides a product summary.

        Notes
        -----
        Displays various items active for the run (such as the ANSYS revision
        number, Jobname, titles, units, configuration parameters, database
        statistics, etc.).

        This command is valid in any processor.
        """
        command = "/STATUS,%s" % (str(lab))
        return self.run(command, **kwargs)

    
    def starvput(self, parr="", entity="", entnum="", item1="", it1num="",
                 item2="", it2num="", kloop="", **kwargs):
        """APDL Command: *VPUT

         Restores array parameter values into the ANSYS database.

        Parameters
        ----------
        parr
            The name of the input vector array parameter.  See *SET for name
            restrictions.  The parameter must exist as a dimensioned array
            [*DIM] with data input.

        entity
            Entity keyword.  Valid keywords are shown for Entity = in the table
            below.

        entnum
            The number of the entity (as shown for ENTNUM= in the table below).

        item1
            The name of a particular item for the given entity.  Valid items
            are as shown in the Item1 columns of the table below.

        it1num
            The number (or label) for the specified Item1 (if any).  Valid
            IT1NUM values are as shown in the IT1NUM columns of the table
            below.  Some Item1 labels do not require an IT1NUM value.

        item2, it2num
            A second set of item labels and numbers to further qualify the item
            for which data is to be stored.  Most items do not require this
            level of information.

        kloop
            Field to be looped on:

            Loop on the ENTNUM field (default). - Loop on the Item1 field.

            Loop on the IT1NUM field.  Successive items are as shown with IT1NUM. - Loop on the Item2 field.

        Notes
        -----
        The *VPUT command is not supported for PowerGraphics displays.
        Inconsistent results may be obtained if this command is not used in
        /GRAPHICS, FULL.

        Plot and print operations entered via the GUI (Utility Menu> Pltcrtls,
        Utility Menu> Plot) incorporate the AVPRIN command. This means that the
        principal and equivalent values are recalculated. If you use *VPUT to
        put data back into the database, issue the plot commands from the
        command line to preserve your data.

        This operation is basically the inverse of the *VGET operation.  Vector
        items are put directly (without any coordinate system transformation)
        into the ANSYS database.  Items can only replace existing items of the
        database and not create new items.  Degree of freedom results that are
        replaced in the database are available for all subsequent
        postprocessing operations.  Other results are changed temporarily and
        are available mainly for the immediately following print and display
        operations.  The vector specification *VCUM does not apply to this
        command.  The valid labels for the location fields (Entity, ENTNUM,
        Item1, and IT1NUM) are listed below.  Item2 and IT2NUM are not
        currently used.  Not all items from the *VGET list are allowed on *VPUT
        since putting values into some locations could cause the database to be
        inconsistent.

        This command is valid in any processor.

        Table: 250:: : *VPUT - POST1 Items

        X, Y, or Z fluid velocity. X, Y, or Z nodal velocity in a transient
        structural analysis (LS-DYNA analysis or analysis with ANTYPE,TRANS).

        X, Y, or Z magnetic vector potential. X, Y, or Z nodal acceleration in
        a transient structural analysis (LS-DYNA analysis or analysis with
        ANTYPE,TRANS).
        """
        command = "*VPUT,%s,%s,%s,%s,%s,%s,%s,%s" % (str(parr), str(entity), str(entnum), str(item1), str(it1num), str(item2), str(it2num), str(kloop))
        return self.run(command, **kwargs)

    
    def fmagbc(self, cnam1="", cnam2="", cnam3="", cnam4="", cnam5="",
               cnam6="", cnam7="", cnam8="", cnam9="", **kwargs):
        """APDL Command: FMAGBC

        Applies force and torque boundary conditions to an element component.

        Parameters
        ----------
        cnam1, cnam2, cnam3, . . . , cnam9
            Names of existing element components (CM command).  Must be
            enclosed in single quotes (e.g., `Cnam1') when the command is
            manually typed in.

        Notes
        -----
        FMAGBC invokes a predefined ANSYS macro to apply Maxwell and virtual
        work force and torque boundary conditions to an element component.
        These boundary conditions are used for subsequent force and torque
        calculations during solution.  Magnetic virtual displacements (MVDI =
        1) are applied to nodes of elements in the components, and  Maxwell
        surface flags (MXWF) are applied to air elements adjoining the element
        components.  Incorrect force and torque calculations will occur for
        components sharing adjacent air elements.   Companion macros FMAGSUM
        and TORQSUM can be used in POST1 to summarize the force and torque
        calculations, respectively.  Torque calculations are valid for 2-D
        planar analysis only.  For 2-D harmonic analysis, force and torque
        represent time-average values.

         If using elements PLANE121, SOLID122, SOLID123, PLANE233, SOLID236 and
        SOLID237 (static analyses only), use EMFT to summarize electromagnetic
        force and torque. If you do use FMAGSUM, you do not need to first set
        either the Maxwell or the virtual work force flags via FMAGBC.
        """
        command = "FMAGBC,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (str(cnam1), str(cnam2), str(cnam3), str(cnam4), str(cnam5), str(cnam6), str(cnam7), str(cnam8), str(cnam9))
        return self.run(command, **kwargs)

    
    def torqc2d(self, rad="", numn="", lcsys="", **kwargs):
        """APDL Command: TORQC2D

        Calculates torque on a body in a magnetic field based on a circular
        path.

        Parameters
        ----------
        rad
            Radius of the circular path.  The nodes for the path are created at
            this radius.

        numn
            Number of nodes to be created for the circular path.  The greater
            the number of nodes, the higher the accuracy of the torque
            evaluation.  Defaults to 18.

        lcsys
            (Optional) Local coordinate system number to be used for defining
            the circular arc of nodes and the path.  Defaults to 99.  (If a
            local system numbered 99 already exists, it will be overwritten by
            this default.)

        Notes
        -----
        TORQC2D invokes an ANSYS macro which calculates the mechanical torque
        on a body using a circular path.  It is used for a circular or
        cylindrical body such as a rotor in an electric machine.  The body must
        be centered about the global origin and must be surrounded by air
        elements.  The air elements surrounding the path at radius RAD must be
        selected, and elements with a high-permeability material should be
        unselected prior to using the macro.  The macro is valid for 2-D planar
        analyses only.  For a harmonic analysis, the macro calculates the time-
        average torque.  Radial symmetry models are allowed, i.e., the model
        need not be a full 360° model.

        The calculated torque is stored in the parameter TORQUE.  If the model
        is not a full 360° model, TORQUE should be multiplied by the
        appropriate factor (such as 4.0 for a 90° sector) to obtain the total
        torque.  A node plot showing the path is produced in interactive mode.

        The torque is calculated via a circular path integral of the Maxwell
        stress tensor.  The circular path and the nodes for the path are
        created by the macro at the specified radius RAD.  Path operations are
        used for the calculation, and all path items are cleared upon
        completion.  See the TORQ2D command for torque calculation based on an
        arbitrary, non-circular path.
        """
        command = "TORQC2D,%s,%s,%s" % (str(rad), str(numn), str(lcsys))
        return self.run(command, **kwargs)

    
    
    def rsprnt(self, rslab="", yname="", xout="", **kwargs):
        """APDL Command: RSPRNT

        Print a response surface.

        Parameters
        ----------
        rslab
            Response Surface set label. Identifies the response surfaces
            generated by the RSFIT command.

        yname
            Parameter name. The parameter must have been previously defined as
            a random output parameter with the PDVAR command. Identifies the
            parameter for which a response surface has been generated by the
            RSFIT command.

        xout
            An option if an extended print-out of more feedback about goodness-
            of-fit and the details of the regression analysis of the response
            surface is requested.

            No - Use the standard print-out (default).

            Yes - Use the extended print-out.

        Notes
        -----
        Prints the results and details of a response surface analysis generated
        by the RSFIT command. For the specified output parameter Yname, the
        fitting details such as the individual terms of the response surface
        model and their corresponding coefficients are listed. The command also
        produces a comparison of the original values of Yname used for the
        fitting process and the approximate values derived from the fitting,
        and some goodness of fit measures.

        If Xout = Yes, then more information about the regression analysis of
        the response surface will be printed. For example, the confidence
        intervals on the regression coefficients and the correlation between
        the regression coefficients among others.
        """
        command = "RSPRNT,%s,%s,%s" % (str(rslab), str(yname), str(xout))
        return self.run(command, **kwargs)

    
    
    
    def reorder(self, **kwargs):
        """APDL Command: REORDER

        Specifies "Model reordering" as the subsequent status topic.

        Notes
        -----
        This is a status [STAT] topic command.  Status topic commands are
        generated by the GUI and will appear in the log file (Jobname.LOG) if
        status is requested for some items under Utility Menu> List> Status.
        This command will be immediately followed by a STAT command, which will
        report the status for the specified topic.

        If entered directly into the program, the STAT command should
        immediately follow this command.
        """
        command = "REORDER,"
        return self.run(command, **kwargs)

    
    
    
    def noorder(self, lab="", **kwargs):
        """APDL Command: NOORDER

        Re-establishes the original element ordering.

        Parameters
        ----------
        lab
            Turns element reordering on or off.

            ON (or blank) - Re-establishes original element ordering (default).

            OFF - Original ordering is not used and program establishes its own ordering at the
                  beginning of the solution phase.

        Notes
        -----
        If Lab = ON, the original element ordering is re-established and no
        automatic reordering occurs at the beginning of the solution phase.
        Use Lab = OFF only to remove the effect of a previous NOORDER command.
        This command affects only those elements that were defined up to the
        point that this command is issued. See the WSORT and WAVES commands for
        reordering.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = "NOORDER,%s" % (str(lab))
        return self.run(command, **kwargs)

    
    
    def pdprob(self, rlab="", name="", relation="", limit="", conf="",
               **kwargs):
        """APDL Command: PDPROB

        Prints a probability result.

        This command was removed prior to V18.2

        Parameters
        ----------
        rlab
            Result set label. Identifies the result set to be used for
            postprocessing. A result set label can be the solution set label
            you defined in a PDEXE command (if you are directly postprocessing
            Monte Carlo Simulation results), or the response surface set label
            defined in an RSFIT command (for Response Surface Analyses).

        name
            Parameter name. The parameter must have been previously defined as
            a random input variable or a random output parameter using the
            PDVAR command.

        relation
            Relation label for the relation between probabilistic design
            parameter Name and the limit value LIMIT:

            LT - Less than (default).

            GT - Greater than.

        limit
            Limit value.

        conf
            Confidence level. The confidence level is used to print the
            confidence bounds on the probability. The value for the confidence
            level must be between 0.0 and 1.0 and it defaults to 0.95 (95%).
            Printing of confidence bound is suppressed for CONF  0.5. This
            parameter is ignored for response surface methods results
            postprocessing.

        Notes
        -----
        Prints the probability that the probabilistic design input or output
        variable denoted with Name is smaller or larger than a certain limit
        value.

        If Rlab is left blank, then the result set label is inherited from the
        last PDEXE command (Slab), RSFIT command (RSlab), or the most recently
        used PDS postprocessing command where a result set label was explicitly
        specified.

        Use the relation label Relation to specify if you want to print a
        traditional probability value (LT) or the exceedence probability (GT).
        The LIMIT directly specifies at which value of Name (the design
        parameter) the probability should be evaluated. If LIMIT is between two
        sample values of Name the resulting probability is linearly
        interpolated between the sample values. If LIMIT is smaller than all
        sample values of Name the probability is 0.0 for Relation = LT and 1.0
        for Relation = GT. If LIMIT is greater than all sample values for Name
        the probability is 1.0 for Relation = LT and 0.0 for Relation = GT.

        The confidence level is a probability expressing the confidence that
        the value for the requested probability is in fact between the
        confidence bounds. The larger the confidence level, the wider the
        confidence bounds. Printing the confidence bounds only makes sense for
        postprocessing Monte Carlo simulation results, where the confidence
        bounds represent the accuracy of the results. With increasing sample
        sizes, the width of the confidence bounds gets smaller for the same
        confidence level. For response surface analysis methods, the number of
        simulations done on the response surface is usually very large;
        therefore, the accuracy of the results is determined by the response
        surface fit and not by the confidence level.

        The PDPROB command cannot be used to postprocess the results in a
        solution set that is based on Response Surface Methods, only Monte
        Carlo Simulations.
        """
        return self.run(f"PDPROB,{rlab},{name},{relation},{limit},,{conf}", **kwargs)

    
    def pdsens(self, rlab="", name="", chart="", type_="", slevel="", **kwargs):
        """APDL Command: PDSENS

        Plots the probabilistic sensitivities.

        Parameters
        ----------
        rlab
            Result set label. Identifies the result set to be used for
            postprocessing. A result set label can be the solution set label
            you defined in a PDEXE command (if you are directly postprocessing
            Monte Carlo Simulation results), or the response surface set label
            defined in an RSFIT command (for Response Surface Analyses). The
            PDSENS command cannot be used to postprocess the results in a
            solution set that is based on Response Surface Methods, only Monte
            Carlo Simulations.

        name
            Parameter name. The parameter must have been previously defined as
            a random output parameter using the PDVAR command.

        chart
            Keyword for the type of chart to be plotted.

            BAR - Bar chart of the absolute sensitivities.

            PIE - Pie chart of relative and normalized sensitivities.

            BOTH - Both pie and bar charts plotted side by side (default).

        type\_
            Keyword for the type of correlation coefficients used to evaluate
            the sensitivities.

            RANK - Spearman rank-order correlation coefficient (default).

            LIN - Pearson linear correlation coefficient.

        slevel
            Significance level. The value for the significance level must be
            between 0.0 and 1.0 and it defaults to 0.025 (2.5%).

        Notes
        -----
        Plots the probabilistic sensitivities.

        If Rlab is left blank, then the result set label is inherited from the
        last PDEXE command (Slab), RSFIT command (RSlab), or the most recently
        used PDS postprocessing command where a result set label was explicitly
        specified.

        Evaluation of the probabilistic sensitivities is based on the
        correlation coefficients between all random input variables and the
        random output parameter specified by Name. You can chose which
        correlation coefficient should be used for that evaluation using the
        Corr option. For all sensitivity values, the probabilistic design tool
        evaluates the probability that the sensitivity can be neglected, based
        on statistical test theory. If this probability exceeds the
        significance level as specified by the SLEVEL parameter, the
        sensitivity value should be regarded as negligible or insignificant.
        The higher the significance level (SLEVEL) the more sensitivities are
        considered as significant. The sensitivity plot includes the
        significant sensitivities only and lists the insignificant ones
        separately.
        """
        command = "PDSENS,%s,%s,%s,%s,%s" % (str(rlab), str(name), str(chart), str(type_), str(slevel))
        return self.run(command, **kwargs)

    
    
    
    def fctyp(self, oper="", lab="", **kwargs):
        """APDL Command: FCTYP

        Activates or removes failure-criteria types for postprocessing.

        Parameters
        ----------
        oper
            Operation key:

            ADD - Activate failure-criteria types. This option is the default behavior.

            DELE - Remove failure-criteria types.

        lab
            Valid failure-criteria labels. If ALL, select all available
            (including user-defined) failure criteria.

            EMAX - Maximum strain criterion (default)

            SMAX - Maximum stress criterion (default)

            TWSI  - Tsai-Wu strength index (default)

            TWSR  - Inverse of Tsai-Wu strength ratio index (default)

            HFIB  - Hashin fiber failure criterion

            HMAT  - Hashin matrix failure criterion

            PFIB  - Puck fiber failure criterion

            PMAT  - Puck inter-fiber (matrix) failure criterion

            L3FB - LaRc03 fiber failure criterion

            L3MT - LaRc03 matrix failure criterion

            L4FB - LaRc04 fiber failure criterion

            L4MT - LaRc04 matrix failure criterion

            USR1 through USR9  - User-defined failure criteria

        Notes
        -----
        The FCTYP command modifies the list of active failure criteria.

        By default, active failure criteria include EMAX, SMAX, TWSI, and TWSR.

        The command affects any subsequent postprocessing listing and plotting
        commands (such as PRESOL, PRNSOL, PLESOL, PLNSOL, and ETABLE).

        A single FCTYP command allows up to six failure-criteria labels. If
        needed, reissue the command to activate or remove additional failure-
        criteria types.
        """
        command = "FCTYP,%s,%s" % (str(oper), str(lab))
        return self.run(command, **kwargs)

    
    
    
    
    def pdscat(self, rlab="", name1="", name2="", type_="", order="", nmax="",
               **kwargs):
        """APDL Command: PDSCAT

        Plots a scatter graph.

        Parameters
        ----------
        rlab
            Result set label. Identifies the result set to be used for
            postprocessing. A result set label can be the solution set label
            you defined in a PDEXE command, or the response surface set label
            defined in an RSFIT command.

        name1, name2
            Parameter names. The parameters must have been previously defined
            as a random input variable or a random output parameter using the
            PDVAR command. The parameter data for Name1 is shown on the X-axis
            and the parameter data for Name2 is shown on the Y-axis in the
            plot.

        type\_
            Keyword for the type of trendline curve.

            POLY - Polynomial trendline (default).

            NONE - A trendline is not plotted.

        order
            Order of the polynomial trendline. This parameter is used only for
            Type = POLY. ORDER must be a positive number. There is no maximum
            for ORDER provided there are enough data points to evaluate a
            polynomial of the requested order. Default is 1.

        nmax
            Maximum number of points plotted in the scatter plot.  If there are
            more sample data, then only the first NMAX points are plotted. The
            default value is 10,000.

        Notes
        -----
        Plots a scatter graph with or without a trendline. The scatter plot
        shows the simulated points for two random parameters. Random input
        variables and random output parameters are valid for both X- and
        Y-axis. The mean value of both parameters are marked with separate
        green lines. The point where the green lines cross marks the
        statistical center of gravity of the cloud of all simulated data points
        of the two parameters.

        If Rlab is left blank, then the result set label is inherited from the
        last PDEXE command (Slab), RSFIT command (RSlab), or the most recently
        used PDS postprocessing command where a result set label was explicitly
        specified.

        If the parameter data for Name1 includes negative values, fitting a
        logarithmic trendline is not possible and the logarithmic trendline
        plot is suppressed if requested. The same applies for an exponential
        trendline if the data for the Name2 includes negative values.

        Because of the amount of data involved, the scatter plot is limited to
        NMAX points. If shown, the trendline is evaluated only on the NMAX
        points shown. However, the statistical information shown in the plot,
        such as the mean value lines for both parameters and the correlation
        coefficients listed in the legend are based on the full set of samples.
        If required, you can increase NMAX to plot more points, but this will
        affect the time needed to process the PDSCAT command. If NMAX is less
        than the total amount of simulated points, which is typically possible
        for Response Surface Methods, you will see an appropriate warning in
        the plot legend.
        """
        command = "PDSCAT,%s,%s,%s,%s,%s,%s" % (str(rlab), str(name1), str(name2), str(type_), str(order), str(nmax))
        return self.run(command, **kwargs)

    
    
    def c(self, comment="", **kwargs):
        """APDL Command: C***

        Places a comment in the output.

        Parameters
        ----------
        comment
            Comment string, up to 75 characters.

        Notes
        -----
        The output from this command consists of two lines -- a blank line
        followed by a line containing C*** and the comment.  This command is
        similar to /COM except that the comment produced by C*** is more easily
        identified in the output.

        Another way to include a comment is to precede it with a ! character
        (on the same line).  The ! may be placed anywhere on the line, and any
        input following it is ignored as a comment.  No output is produced by
        such a comment, but the comment line is included on the log file.  This
        is a convenient way to annotate the log file.

        This command is valid anywhere.
        """
        command = "C***,%s" % (str(comment))
        return self.run(command, **kwargs)

    def fe(self, nev="", cycle="", fact="", title="", **kwargs):
        """APDL Command: FE

        Defines a set of fatigue event parameters.

        Parameters
        ----------
        nev
            Reference number for this event (within MXEV).

        cycle
            Number of required cycles (defaults to 1).  If -1, erase all
            parameters and fatigue stresses for this event.

        fact
            Scale factor to be applied to all loadings in this event (defaults
            to 1.0).

        title
            User defined identification title for this event (up to 20
            characters).

        Notes
        -----
        Repeat FE command to define additional sets of event parameters (MXEV
        limit), to redefine event parameters, or to delete event stress
        conditions.

        The set of fatigue event parameters is associated with all loadings and
        all locations.  See the FTSIZE command for the maximum set of events
        (MXEV) allowed.
        """
        command = "FE,%s,%s,%s,%s" % (str(nev), str(cycle), str(fact), str(title))
        return self.run(command, **kwargs)

    
    
    def rssims(self, rslab="", nsim="", seed="", **kwargs):
        """APDL Command: RSSIMS

        Performs Monte Carlo simulations on response surface(s).

        Parameters
        ----------
        rslab
            Response Surface set label. Identifies the response surfaces
            generated by the RSFIT command.

        nsim
            Number of simulation loops on the response surfaces that will be
            generated for all random output parameters. If the RSSIMS command
            is issued multiple times using the same response surface set label
            the NSIM Monte Carlo simulations is appended to previous ones. The
            default value for NSIM is 10,000.

        seed
            Seed value label. Random number generators require a seed value
            that is used to calculate the next random number. After each random
            number generation finishes, the seed value is updated and is used
            again to calculate the next random number. By default ANSYS
            initializes the seed value with the system time (one time only)
            when the ANSYS session started.

            CONT - Continues updating using the derived seed value (default).

            TIME - Initializes the seed value with the system time. You can use this if you want
                   the seed value set to a specific value for one analysis and
                   then you want to continue with a "random" seed in the next
                   analysis. It is not recommended to "randomize" the seed
                   value with the Seed = TIME option for multiple analyses. If
                   the Monte Carlo simulations requested with this command will
                   be appended to previously existing simulations, then the
                   Seed option is ignored and Seed = CONT is used.

            INIT - Initializes the seed value using 123457. This value is a typical recommendation
                   used very often in literature. This option leads to
                   identical random numbers for all random input variables when
                   the exact analysis will be repeated, making it useful for
                   benchmarking and validation purposes (where identical random
                   numbers are desired). If the Monte Carlo simulations
                   requested with this command will be appended to previously
                   existing simulations, then the Seed option is ignored and
                   Seed = CONT is used.

            Value - Uses the specified (positive) value for the initialization of the seed value.
                    This option has the same effect as Seed = INIT, except you
                    can chose an arbitrary (positive) number for the
                    initialization. If the Monte Carlo simulations requested
                    with this command will be appended to previously existing
                    simulations, then the Seed option is ignored and Seed =
                    CONT is used.

        Notes
        -----
        Generate the Monte Carlo simulations on the response surfaces that are
        included in a response surface set. Simulations are evaluated only for
        the output parameters that have been fitted in a response surface set
        using the RSFIT command.

        If the RSSIMS command is issued multiple times using the same response
        surface label the probabilistic design system appends the samples
        generated here to the previous ones. This way you can start with a
        moderate NSIM number and add more samples if the probabilistic results
        are not accurate enough.
        """
        command = "RSSIMS,%s,%s,%s" % (str(rslab), str(nsim), str(seed))
        return self.run(command, **kwargs)

    
    
    def pdhist(self, rlab="", name="", ncl="", type_="", **kwargs):
        """APDL Command: PDHIST

        Plots the frequency histogram.

        Parameters
        ----------
        rlab
            Result set label. Identifies the result set to be used for
            postprocessing. A result set label can be the solution set label
            you defined in a PDEXE command (if you are directly postprocessing
            Monte Carlo Simulation results), or the response surface set label
            defined in an RSFIT command (for Response Surface Analyses).

        name
            Parameter name. The parameter must have been previously defined as
            a random input variable or a random output parameter with the PDVAR
            command.

        ncl
            Number of classes for the histogram plot. This is the number of
            bars shown in the histogram. NCL must be a positive number. If this
            field is left blank, Mechanical APDL calculates an appropriate
            number of classes based on the sample size. ANSYS divides the range
            between the smallest and largest sample value into NCL classes of
            equal width and determines the histogram frequencies by counting
            the number of hits that fall in the classes.

        type\_
            Type of histogram.

            ABS - Absolute frequency histogram. This is the actual number of hits in each class.

            REL - Relative frequency histogram (default). This is the number of hits in the
                  individual classes divided by the total number of samples.

            NORM - Normalized frequency histogram. This is the number of hits in the individual
                   classes divided by the total number of samples and divided
                   by the width of the class. This normalization makes the
                   histogram comparable to the probability density function.

        Notes
        -----
        Plots the frequency histogram.

        If Rlab is left blank, then the result set label is inherited from the
        last PDEXE command (Slab), RSFIT command (RSlab), or the most recently
        used PDS postprocessing command where a result set label was explicitly
        specified.

        The PDHIST command cannot be used to postprocess the results in a
        solution set that is based on Response Surface Methods, only Monte
        Carlo Simulations.
        """
        command = "PDHIST,%s,%s,%s,%s" % (str(rlab), str(name), str(ncl), str(type_))
        return self.run(command, **kwargs)

    
    
    
    def seltol(self, toler="", **kwargs):
        """APDL Command: SELTOL

        Sets the tolerance for subsequent select operations.

        Parameters
        ----------
        toler
            Tolerance value. If blank, restores the default tolerance logic.

        Notes
        -----
        For selects based on non-integer numbers (e.g. coordinates, results,
        etc.), items within the range VMIN - Toler and VMAX + Toler are
        selected, where VMIN and VMAX are the range values input on the xSEL
        commands (ASEL, ESEL, KSEL, LSEL, NSEL, and VSEL).

        The default tolerance logic is based on the relative values of VMIN and
        VMAX as follows:

        If VMIN = VMAX, Toler = 0.005 x VMIN.

        If VMIN = VMAX = 0.0, Toler = 1.0E-6.

        If VMAX ≠ VMIN, Toler = 1.0E-8 x (VMAX-VMIN).

        This command is typically used when VMAX-VMIN is very large so that the
        computed default tolerance is therefore large and the xSEL commands
        selects more than what is desired.

        Toler remains active until respecified by a subsequent SELTOL command.
        A SELTOL < blank > resets back to the default Toler logic.
        """
        command = "SELTOL,%s" % (str(toler))
        return self.run(command, **kwargs)

    
    def starlist(self, fname="", ext="", **kwargs):
        """APDL Command: *LIST

        Displays the contents of an external, coded file.

        Parameters
        ----------
        fname
            File name and directory path (248 characters maximum, including the
            characters needed for the directory path).  An unspecified
            directory path defaults to the working directory; in this case, you
            can use all 248 characters for the file name.

        ext
            Filename extension (eight-character maximum).

        Notes
        -----
        Displays the contents of an external, coded file.  The file to be
        listed cannot be in use (open) at the time (except for the error file,
        File.ERR, which may be displayed with *LIST,ERR).

        Use caution when you are listing active ANSYS files via the List>
        Files> Other and File> List> Other menu paths.  File I/O buffer and
        system configurations can result in incomplete listings unless the
        files are closed.

        This command is valid in any processor.
        """
        command = "*LIST,%s,%s" % (str(fname), str(ext))
        return self.run(command, **kwargs)

    
    
    def lmatrix(self, symfac="", coilname="", curname="", indname="",
                **kwargs):
        """APDL Command: LMATRIX

        Calculates an inductance matrix and the total flux linkage for an
        N-winding coil system.

        Parameters
        ----------
        symfac
            Geometric symmetry factor.  Inductance terms are scaled by this
            factor which represents the fraction of the total device modeled.
            Default is 1.

        coilname
            Alphanumeric prefix identifier for coil label used in defining
            named element coil components. Default is 'coil.'

        curname
            Name of a predefined parameter array containing the nominal coil
            currents of the system.  The array must be defined (see *DIM
            command) prior to calling the LMATRIX macro. Default is 'cur.'

        indname
            Name of the array parameter to be created by LMATRIX containing the
            calculated inductance matrix and the flux linkage in each coil.  A
            text file of the same name with an extension .TXT is created
            containing the matrix data. Default is 'lmatrix.'

        Notes
        -----
        LMATRIX calculates the differential inductance matrix for an N-winding
        system where N is the number of coils in the system, and calculates the
        total flux linkage in each coil. LMATRIX may only be executed after the
        solution of a problem with nominal currents applied to the coils at a
        desired "operating point." The array Indname has N rows and N+1
        columns. The N x N block is the differential inductance matrix; the
        N+1th column contains the total flux linkage, with the ith row
        corresponding to the ith coil. See the Mechanical APDL Theory Reference
        for more details.

        To invoke the LMATRIX macro, for the classical formulations, the
        elements for each coil must be grouped into a component using the CM
        command.  Each set of independent coil elements is assigned a component
        name with the prefix Coilname followed by the coil number. For the
        solenoidal formulations, you must make the exciting node with a F,AMPS
        load a node component using the CM command.  The classical and
        solenoidal formulations cannot be mixed.

        To invoke the LMATRIX macro, the vector array parameter Curname with
        dimension N must be defined and named using the *DIM command.  You must
        set each vector array entry equal to the nominal current per turn in
        the corresponding coil at the operating point.  Zero current values
        must be approximated by a negligibly small applied current.

        Do not apply (or remove) inhomogeneous loads before using the LMATRIX
        command. Inhomogeneous loads are those created by:

        Degree of freedom commands (D, DA, etc.) specifying nonzero degrees of
        freedom values on nodes or solid model entities

        Any CE command with a nonzero constant term

        Do not put any loads (for example, current) on elements not contained
        in the element component.

        Operating solutions must be obtained through static analysis before
        calling LMATRIX. All name-strings must be enclosed in single quotes in
        the LMATRIX command line. The geometric symmetry factor, Symfac,
        represents the fraction of the device modeled, disregarding any current
        source primitives.

        LMATRIX works only with magnetic field elements: PLANE53, SOLID96, and
        SOLID97, and with SOURC36 solenoidal formulations. For electromagnetic
        elements PLANE233, SOLID236 and SOLID237, static linear perturbation
        analysis can be used to calculate the differential inductance using the
        element incremental energy record (IENE).

        For more information, see LMATRIX in the Low-Frequency Electromagnetic
        Analysis Guide.

        See the Mechanical APDL Theory Reference and Electric and Magnetic
        Macros in the Low-Frequency Electromagnetic Analysis Guide for details.

        This command does not support multiframe restarts.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = "LMATRIX,%s,%s,%s,%s" % (str(symfac), str(coilname), str(curname), str(indname))
        return self.run(command, **kwargs)

    
    def for2d(self, **kwargs):
        """APDL Command: FOR2D

        Calculates magnetic forces on a body.

        Notes
        -----
        FOR2D invokes an ANSYS macro which calculates magnetic forces on a body
        that is completely surrounded by air (symmetry permitted).  The
        calculated forces are stored in the parameters FX and FY.  In
        interactive mode, a node plot is produced with the integration path
        highlighted.  A predefined closed path [PATH], passing through the air
        elements surrounding the body, must be available for this calculation.
        A counterclockwise ordering of nodes on the PPATH command will give the
        correct sign on the forces.  Forces are calculated using a Maxwell
        stress tensor approach.  The macro is valid for 2-D planar or
        axisymmetric analysis.  Path operations are used for the calculations,
        and all path items are cleared upon completion.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = "FOR2D,"
        return self.run(command, **kwargs)

    def rsplot(self, rslab="", yname="", x1name="", x2name="", type_="",
               npts="", plow="", pup="", **kwargs):
        """APDL Command: RSPLOT

        Plot a response surface.

        Parameters
        ----------
        rslab
            Response Surface set label. Identifies the response surfaces
            generated by the RSFIT command.

        yname
            Parameter name. The parameter must have been previously defined as
            a random output parameter with the PDVAR command.

        x1name
            Parameter name. The parameter must have been previously defined as
            a random input variable with the PDVAR command.

        x2name
            Parameter name. The parameter must have been previously defined as
            a random input variable with the PDVAR command. X2Name must be
            different than X1Name.

        type\_
            Type of the response surface visualization.

            2D - 2-D contour plot.

            3D - 3-D surface plot.

        npts
            Number of grid points for both the X1-axis and the X2-axis. The
            grid points are used for the evaluation of the response surface.
            The number must be between 1 and 500. Defaults to 20. If NPTS = 0
            or greater than 500, then a value of 20 is used.

        plow
            Lower probability level used to determine the lower boundary
            (plotting range) of the curve in case the random input variable
            does not have a minimum value (such as Gauss). This probability
            must be between 0.0 and 1.0. Defaults to 0.0025.

        pup
            Upper probability level used to determine the upper boundary of the
            curve. This probability must be between 0.0 and 1.0. Defaults to
            0.9975.

        Notes
        -----
         Plots the response surface of an output parameter YName as a function
        of two input parameters X1Name and X2Name.

        If PLOW is left blank, then a minimum value of the distribution is used
        for plotting, provided it exists (for example, uniform distribution).
        If the distribution type has no minimum value (for example, Gaussian
        distribution), then the default value is used to determine the lower
        plotting range value. The same is true for the maximum value if PUP is
        left blank.

        In addition to the response surface, the sampling points that are
        fitted by the response surface are also plotted by this command.
        However, sampling points falling outside of the plotting range defined
        by the PLOW and PUP fields will not be shown in the plot.
        """
        command = "RSPLOT,%s,%s,%s,%s,%s,%s,%s,%s" % (str(rslab), str(yname), str(x1name), str(x2name), str(type_), str(npts), str(plow), str(pup))
        return self.run(command, **kwargs)

    
    
    
    def wsort(self, lab="", kord="", wopt="", oldmax="", oldrms="", **kwargs):
        """APDL Command: WSORT

        Initiates element reordering based upon a geometric sort.

        This command was removed by V18.2

        Parameters
        ----------
        lab
            Coordinate (in the active system) along which element
            centroid locations are sorted.  Valid labels are: X, Y, Z,
            ALL.  If ALL (default), all three directions will be used,
            and the order corresponding to the lowest MAX or RMS
            wavefront value will be retained.

        kord
            Sort order:

            0 - Sort according to ascending coordinate values.

            1 - Sort according to descending coordinate values.

        wopt
            Option for comparison:

            MAX - Use maximum wavefront value for comparison (default).

            RMS - Use RMS wavefront value.

        oldmax, oldrms
            MAX and RMS wavefront values of model to be used in place of the
            old values.  OLDRMS defaults to OLDMAX (and vice versa).  If
            neither is  specified, each defaults to its calculated old value.

        Notes
        -----
        Initiates element reordering based upon a geometric sort of the element
        centroid locations.  Wave lists, if any [WSTART], are ignored.
        Reordering affects only the element order for the solution phase and
        not the element numbers (input referring to element numbers, such as
        element pressures, is unaffected by reordering).

        Note: The new order is retained only if new the new maximum or RMS
        wavefront values are lower than the old values, as described below.
        See the WAVES command for another reordering procedure and for more
        details on reordering.  The resulting element ordering can be shown by
        listing the wavefront history [WFRONT,1] or by displaying elements with
        their element location numbers [/PNUM].

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        return self.run(f"WSORT,{lab},{kord},,{wopt},{oldmax},{oldrms}", **kwargs)

    def pdcfld(self, parr="", entity="", ctype="", clength="", **kwargs):
        """APDL Command: PDCFLD

        Calculates a correlation field and stores it into an ANSYS array.

        Parameters
        ----------
        parr
            Parameter name. ParR is a one-dimensional array with the
            dimension N * (N - 1)/2, where N is either the number of
            the selected nodes or the number of the selected elements
            (depending on the Entity field). The PDCFLD command
            automatically sets ParR as a one- dimensional array, (so
            you do not have to use the *DIM command). If you use the
            PDCFLD command twice with the ANSYS parameter ParR, then
            the values stored in the array are automatically
            overwritten.  If the number of selected FE entities is
            different from the previous PDCFLD command, then the array
            ParR is re-dimensioned automatically.

        entity
            Specifies which FE entity the calculation of the correlation field
            is based on. This field must not be blank.

            NODE - Calculate the correlation coefficients based on the
                   distance between the selected nodes.

            ELEM - Calculate the correlation coefficients based on the
                   distance between the centroids of the selected
                   elements.

        ctype
            Specifies the equation used to calculate the correlation
            coefficients as a function of the nodal or element centroid
            distances. This field must not be blank.

            NONE - The random field is not correlated. This means the
                   correlation coefficients are determined according
                   to

            ρij = 1 for i = j - ρij = 0 for i ≠ j

            Here, ρij is the correlation coefficient between the i-th
            and j-th selected FE entity (node or element centroid). -
            LEXP.

            Calculate the correlation coefficient according to a
            linear-exponential decay function. - Here, D({xi} , {xj})
            is the "domain distance" between {xi}, {xj}, and {xi} and
            {xj} are the coordinate vectors of the i-th and j-th
            selected FE entity (node or element centroid), and CL is
            the correlation length of the random field as specified in
            the CLENGTH field.

        clength
            Correlation length of the correlation field. The correlation length
            is a characteristic length that influences how strongly two
            elements of a random field are correlated with each other. The
            larger the value of CLENGTH, the stronger the correlation between
            the random field elements. CLENGTH is required for Ctype = LEXP and
            Ctype = QEXP; it must be a nonzero, positive number.

        Notes
        -----
        Calculates a correlation field for a probabilistic analysis involving a
        random field. Random fields are random effects with a spatial
        distribution; the value of a random field not only varies from
        simulation to simulation at any given location, but also from location
        to location. The correlation field describes the correlation
        coefficient between two different spatial locations. Random fields can
        be either based on element properties (typically material) or nodal
        properties (typically surface shape defined by nodal coordinates).
        Hence, random fields are either associated with the selected nodes or
        the selected elements. If a random field is associated with elements,
        then the correlation coefficients of the random field are calculated
        based on the distance of the element centroids.

        For more information, see Probabilistic Design in the Advanced Analysis
        Guide.

        Note that for correlation fields, the "domain distance" D({xi} , {xj})
        is not the spatial distance |{xi} - {xj}|, but the length of a path
        between {xi} and {xj} that always remains inside the finite element
        domain. However, exceptions are possible in extreme meshing cases. For
        elements that share at least one node, the PDCFLD evaluates the
        distance by directly connecting the element centroids with a straight
        line. If these neighboring elements form a sharp inward corner then it
        is possible that the "domain distance" path lies partly outside the
        finite element domain, as illustrated below.

        After the correlation coefficients have been calculated and stored in
        the ANSYS parameter ParR, then use the PDCORR command to define the
        correlations between the elements of the random field.
        """
        command = "PDCFLD,%s,%s,%s,%s" % (str(parr), str(entity), str(ctype), str(clength))
        return self.run(command, **kwargs)

    
    
    
    
    def pdcdf(self, rlab="", name="", type_="", conf="", nmax="", **kwargs):
        """APDL Command: PDCDF

        Plots the cumulative distribution function.

        Parameters
        ----------
        rlab
            Result set label. Identifies the result set to be used for
            postprocessing. A result set label can be the solution set label
            you defined in a PDEXE command (if you are directly postprocessing
            Monte Carlo Simulation results), or the response surface set label
            defined in an RSFIT command (for Response Surface Analyses).

        name
            Parameter name. The parameter must have been previously defined as
            a random input variable or a random output parameter with the PDVAR
            command.

        type\_
            Type of cumulative distribution curve to be displayed.

            EMP - Show an empirical cumulative distribution curve.

            GAUS - Show a cumulative distribution curve in a normal distribution plot. A random
                   variable based on a normal or Gaussian distribution appears
                   as a straight line in this type of plot.

            LOGN - Show a cumulative distribution curve in a log-normal plot. A random variable
                   based on a log-normal distribution appears as a straight
                   line in this type of plot.

            WEIB - Show a cumulative distribution curve in a Weibull distribution plot. A random
                   variable based on a Weibull distribution appears as a
                   straight line in this type of plot.

        conf
            Confidence level. The confidence level is used to plot confidence
            bounds around the cumulative distribution function. The value for
            the confidence level must be between 0.0 and 1.0 and it defaults to
            0.95 (95%). Plotting of the confidence bound is suppressed for CONF
            0.5. This parameter is ignored for the postprocessing of response
            surface methods results.

        nmax
            Maximum number of points to be plotted for the distribution curve.
            This must be a positive number and it defaults to 100. If the
            sample size is less than NMAX, all sample data is represented in
            the plot. If the sample size is larger than NMAX, the probabilistic
            design system classifies the sample into NMAX classes of
            appropriate size.

        Notes
        -----
        Plots the cumulative distribution function.

        The PDCDF command cannot be used to postprocess the results in a
        solution set that is based on Response Surface Methods, only Monte
        Carlo Simulations.

        If Rlab is left blank, then the result set label is inherited from the
        last PDEXE command (Slab), RSFIT command (RSlab), or the most recently
        used PDS postprocessing command where a result set label was explicitly
        specified.
        """
        command = "PDCDF,%s,%s,%s,%s,%s" % (str(rlab), str(name), str(type_), str(conf), str(nmax))
        return self.run(command, **kwargs)

    def slashlarc(self, xcentr="", ycentr="", xlrad="", angle1="", angle2="",
                  **kwargs):
        """APDL Command: /LARC

        Creates annotation arcs (GUI).

        Parameters
        ----------
        xcentr
            Arc X center location (-1.0 < X < 1.0).

        ycentr
            Arc Y center location (-1.0 < Y < 1.0).

        xlrad
            Arc radius length.

        angle1
            Starting angle of arc.

        angle2
            Ending angle of arc.  The arc is drawn counterclockwise from the
            starting angle, ANGLE1, to the ending angle, ANGLE2.

        Notes
        -----
        Defines annotation arcs to be written directly onto the display at a
        specified location.  This is a command generated by the Graphical User
        Interface (GUI) and will appear in the log file (Jobname.LOG) if
        annotation is used.  This command is not intended to be typed in
        directly in an ANSYS session (although it can be included in an input
        file for batch input or for use with the /INPUT command).

        All arcs are shown on subsequent displays unless the annotation is
        turned off or deleted.  Use the /LSPEC command to set the attributes of
        the arc.

        This command is valid in any processor.
        """
        command = "/LARC,%s,%s,%s,%s,%s" % (str(xcentr), str(ycentr), str(xlrad), str(angle1), str(angle2))
        return self.run(command, **kwargs)

    
    
    def lsrestore(self, enginename="", filename="", **kwargs):
        """APDL Command: *LSRESTORE

        Restores a linear solver engine from a binary file.

        Parameters
        ----------
        enginename
            Name used to identify this engine.

        filename
            Name of the file to read from.

        Notes
        -----
        Restores a previously dumped Linear Solver (see the *LSDUMP command).
        This Linear Solver can be used to solve a linear system using the
        *LSBAC command.
        """
        command = "*LSRESTORE,%s,%s" % (str(enginename), str(filename))
        return self.run(command, **kwargs)

    
    
    def wstart(self, node1="", node2="", ninc="", itime="", inc="", **kwargs):
        """APDL Command: WSTART

        Defines a starting wave list.

        Parameters
        ----------
        node1, node2, ninc
            Define a set of nodes in the starting wave list from NODE1 to NODE2
            (defaults to NODE1) in steps of NINC (defaults to 1).  If NODE1 =
            ALL, ignore remaining fields and use all selected nodes [NSEL].

        itime, inc
            Add more node sets to the same starting wave list by repeating the
            previous node set with NODE1 and NODE2 incremented by INC (defaults
            to 1) each time after the first.  ITIME is the total number of sets
            (defaults to 1) defined with this command.

        Notes
        -----
        Defines a starting wave list (optional) for reordering with the WAVES
        command.  Repeat WSTART command to define other starting wave lists (20
        maximum).

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = "WSTART,%s,%s,%s,%s,%s" % (str(node1), str(node2), str(ninc), str(itime), str(inc))
        return self.run(command, **kwargs)

    
    
    def starvplot(self, parx="", pary="", y2="", y3="", y4="", y5="", y6="",
                  y7="", y8="", **kwargs):
        """APDL Command: *VPLOT

        Graphs columns (vectors) of array parameters.

        Parameters
        ----------
        parx
            Name of the array parameter whose column vector values will be the
            abscissa of the graph.  If blank, row subscript numbers are used
            instead.  ParX is not sorted by the program.

        pary
            Name of the array parameter whose column vector values will be
            graphed against the ParX values.

        y2, y3, y4, . . . , y8
            Additional column subscript of the ParY array parameter whose
            values are to be graphed against the ParX values.

        Notes
        -----
        The column to be graphed and the starting row for each array parameter
        must be specified as subscripts.  Additional columns of the ParY array
        parameter may be graphed by specifying column numbers for Y2,  Y3,
        ...,Y8.  For example, *VPLOT,TIME (4,6), DISP (8,1),2,3 specifies that
        the 1st, 2nd, and 3rd columns of array parameter DISP (all starting at
        row 8) are to be graphed against the 6th column of array parameter TIME
        (starting at row 4).  The columns are graphed from the starting row to
        their maximum extent.  See the *VLEN and  *VMASK commands to limit or
        skip data to be graphed.  The array parameters specified on the *VPLOT
        command must be of the same type (type ARRAY or TABLE; [*DIM].   Arrays
        of type TABLE are graphed as continuous curves.  Arrays of type ARRAY
        is displayed in bar chart fashion.

        The normal curve labeling scheme for *VPLOT is to label curve 1 "COL
        1", curve 2 "COL 2" and so on. You can use the /GCOLUMN command to
        apply user-specified labels (8 characters maximum) to your curves. See
        Modifying Curve Labels in the ANSYS Parametric Design Language Guide
        for more information on using /GCOLUMN.

        When a graph plot reaches minimum or maximum y-axis limits, the program
        indicates the condition by clipping the graph. The clip appears as a
        horizontal magenta line. Mechanical APDL calculates y-axis limits
        automatically; however, you can modify the (YMIN and YMAX) limits via
        the /YRANGE command.

        This command is valid in any processor.
        """
        command = "*VPLOT,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (str(parx), str(pary), str(y2), str(y3), str(y4), str(y5), str(y6), str(y7), str(y8))
        return self.run(command, **kwargs)

    
    
    
    def pdplot(self, name="", plow="", pup="", **kwargs):
        """APDL Command: PDPLOT

        Plots the distribution curves of a defined random input variable.

        Parameters
        ----------
        name
            Parameter name. The parameter name must have been previously
            defined as a random input variable using the PDVAR command.

        plow
            Lower probability level used to determine the lower boundary of the
            curve. This probability must be between 0.0 and 1.0 and it defaults
            to 0.0025. This parameter is used to determine the lower plotting
            range (boundary) in case the random input variable does not have a
            minimum value (such as Gauss).

        pup
            Upper probability level used to determine the upper boundary of the
            curve. This probability must be between 0.0 and 1.0 and it defaults
            to 0.9975.

        Notes
        -----
        Plots the distribution of a defined random input variable. The PDPLOT
        command generates a probability density function plot as well as a
        cumulative distribution function plot of the random variable. The
        probabilities PLOW and PUP are used to determine the plot range of the
        random input variable values. To do this, the probabilities are
        converted into random input variable values using the inverse
        cumulative distribution function of the random input variable as shown
        in the following illustration.

        Using the probabilities ensures that the boundaries are always feasible
        and meaningful for the random input variable regardless of its
        distribution type.

         If PLOW is left blank, then a minimum value of the distribution is
        used for plotting, provided it exists (for example, uniform
        distribution). If the distribution type has no minimum value (for
        example, a Gaussian distribution) then the default value is used to
        determine the lower plotting range value. The same applies for the
        maximum value, if  PUP is left blank.
        """
        command = "PDPLOT,%s,%s,%s" % (str(name), str(plow), str(pup))
        return self.run(command, **kwargs)

    
    
    def wrk(self, num="", **kwargs):
        """APDL Command: *WRK

        Sets the active workspace number.

        Parameters
        ----------
        num
            Number of the active memory workspace for APDLMath vector and
            matrices. All the following APDLMath vectors and matrices will
            belong to this memory workspace, until the next call to the *WRK
            command. By default, all the APDLMath objects belong to workspace
            number 1.

        Notes
        -----
        This feature enables you to associate a set of vector and matrices in a
        given memory workspace, so that you can easily manage the free step:

        This feature can be useful to free all the temporary APDLMath variables
        inside a MACRO in one call.
        """
        command = "*WRK,%s" % (str(num))
        return self.run(command, **kwargs)

    
    
    
    
    
    def stargo(self, base="", **kwargs):
        """APDL Command: *GO

        Causes a specified line on the input file to be read next.

        Parameters
        ----------
        base
            "Go to" action:

            A user-defined label (beginning with a colon (:), 8 characters maximum).  The command reader will skip (and wrap to the beginning of the file, if necessary) to the first line that begins with the matching :label.   - Caution:   This label option may not be mixed with do-loop or if-then-else
                              constructs.

        Notes
        -----
        Causes the next read to be from a specified line on the input file.
        Lines may be skipped or reread.  The *GO command will not be executed
        unless it is part of a macro, user file (processed by *USE),  an
        alternate input file (processed by /INPUT), or unless it is used in a
        batch-mode input stream.  Jumping into, out of, or within a do-loop or
        an if-then-else construct to a :label line is not allowed.

        This command is valid in any processor.
        """
        command = "*GO,%s" % (str(base))
        return self.run(command, **kwargs)

    
    def madapt(self, errtargt="", nadapt="", nmax="", kplt="", ksmooth="",
               klst="", kcd="", device="", **kwargs):
        """APDL Command: MADAPT

        Adaptively meshes and solves an edge-based model.

        Parameters
        ----------
        errtargt
            Target percentage for Zienkiewitz Zhu magnetic flux error (defaults
            to 5).

        nadapt
            Maximum number of adaptive steps (defaults to 5).

        nmax
            Maximum number of elements at which the iterations may continue
            (defaults to 50,000). Limits the number of elements that can be
            chosen for refinement.

        kplt
            Plotting options:

            0 - No plot (default)

            1 - Elements and H

            2 - BERR error estimates

            3 - BDSG, BEPC error estimates

            4 - Adaptive details

        ksmooth
            Smoothing options for refinement

            0 - No postprocessing will be done (default).

            1 - Smoothing will be done.  Node locations may change.

            2 - Smoothing and cleanup will be done.  Existing elements may be deleted, and node
                locations may change.

        klst
            Listing options

            0 - No printing (default)

            1 - Final report

            2 - Report at each iteration step

            3 - Report Zienkiewitz Zhu magnetic errors BERR and BSGD

            4 - Regular details

            5 - Full details

            6 - Refine details

            7 - Track

        kcd
            Allows you to issue a CDWRITE or CDREAD at every iteration.

            0 - Do not issue CDWRITE or CDREAD (default).

            1 - Issue CDWRITE at every iteration (to save every mesh variation). This option
                issues CDWRITE,geom, writing the information to jobnameN.cdb.

            2 - Issue CDREAD at every iteration (to read every mesh variation). Reads from an
                existing jobnameN.cdb.

        device
            Defines the output device for plotting.

            0 - Screen only (default)

            1 - JPEG frames. Each frame is written to a file (jobnameN.jpg by default). See
                /SHOW.

        Notes
        -----
        MADAPT invokes a predefined ANSYS macro for adaptive meshing and
        solution of edge-based magnetic analyses.  The macro causes repeated
        runs of the PREP7, SOLUTION, and POST1 phases of the ANSYS program with
        mesh density refinements based upon the percentage error in energy
        norm.

        The MADAPT command macro requires a second, user-defined macro, which
        must be named madaptld.mac and must reside in the same directory where
        ANSYS is being run. This madaptld macro must contain loads and boundary
        conditions, based on permanent geometry or solid model features (such
        as sides or vertices). Loads specified in the madaptld macro cannot be
        based on node numbers because the node numbers will change throughout
        the refinement process. This secondary macro is required because the
        MADAPT macro process must delete all loads and boundary conditions at
        every refinement step.

        MADAPT refines tetrahedral volume elements based on error. Hexahedra,
        wedges, and pyramids are not refined (see NREFINE).

        This command is also valid at the Begin level.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = "MADAPT,%s,%s,%s,%s,%s,%s,%s,%s" % (str(errtargt), str(nadapt), str(nmax), str(kplt), str(ksmooth), str(klst), str(kcd), str(device))
        return self.run(command, **kwargs)

    
    
    
    def pduser(self, fname="", ext="", **kwargs):
        """APDL Command: PDUSER

        Specifies options for user-specified sampling methods.

        Parameters
        ----------
        fname
            File name and directory path (248 characters maximum, including the
            characters needed for the directory path).  An unspecified
            directory path defaults to the working directory; in this case, you
            can use all 248 characters for the file name.

        ext
            Filename extension (eight-character maximum).

        Notes
        -----
        If user-specified sampling methods are requested with the PDMETH, MCS,
        USER command or the PDMETH, RSM, USER command, then you need to specify
        which file contains the sample data. For more information on the format
        of this file, see Probabilistic Design in the Advanced Analysis Guide.
        """
        command = "PDUSER,%s,%s" % (str(fname), str(ext))
        return self.run(command, **kwargs)

    
    
    
    def wmid(self, key="", **kwargs):
        """APDL Command: WMID

        Specifies reordering options for the WAVES command.

        Parameters
        ----------
        key
             Determines whether midside nodes are considered when reordering.

            NO - Do not consider midside nodes when reordering (default).

            YES - Consider midside nodes when reordering. This option
                  is useful for models where line elements are only
                  attached to midside nodes of solid elements.

        Notes
        -----
        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = "WMID,%s" % (str(key))
        return self.run(command, **kwargs)

    
    def pdresu(self, fname="", ext="", **kwargs):
        """APDL Command: PDRESU

        Reads the probabilistic model data and loads it into the database.

        Parameters
        ----------
        fname
            File name and directory path (248 characters maximum, including the
            characters needed for the directory path).  An unspecified
            directory path defaults to the working directory; in this case, you
            can use all 248 characters for the file name.

        ext
            Filename extension (eight-character maximum).

        Notes
        -----
        Reads the probabilistic model data from the specified file and loads it
        into the database. Probabilistic analyses results are not stored in the
        database with the PDRESU command, rather they reside in separate
        results files. Analyses results are loaded automatically (one-by-one
        and on demand) when a probabilistic postprocessing command is issued.
        """
        command = "PDRESU,%s,%s" % (str(fname), str(ext))
        return self.run(command, **kwargs)

    
    
    def mstart(self, label="", key="", **kwargs):
        """APDL Command: /MSTART

        Controls the initial GUI components.

        Parameters
        ----------
        label
            Label identifying the GUI component:

            ZOOM - Pan, Zoom, Rotate dialog box, off by default.

            WORK - Offset Working Plane dialog box, off by default.

            WPSET - Working Plane Settings dialog box, off by default.

            ABBR - Edit Toolbar/Abbreviations dialog box, off by default.

            PARM - Scalar Parameters dialog box, off by default.

            SELE - Select Entities dialog box, off by default.

            ANNO - Annotation dialog box, off by default.

            HARD - Hard Copy dialog box, off by default.

            UTIL - Turns on the pre-ANSYS 6.1 (UIDL) GUI, off by default.

        key
            Switch value:

            OFF or 0 - Component does not appear when GUI is initialized.

            ON or 1 - Component appears when GUI is initialized.

        Notes
        -----
        Controls which components appear when the Graphical User Interface
        (GUI) is initially brought up.  This command is valid only before the
        GUI is brought up [/MENU,ON] and is intended to be used in the
        start162.ans file.  It only affects how the GUI is initialized; you can
        always bring up or close any component once you are in the GUI.

        This command is valid only at the Begin Level.
        """
        command = "/MSTART,%s,%s" % (str(label), str(key))
        return self.run(command, **kwargs)

    
    def fs(self, node="", nev="", nlod="", stitm="", c1="", c2="", c3="",
           c4="", c5="", c6="", **kwargs):
        """APDL Command: FS

        Stores fatigue stress components at a node.

        Parameters
        ----------
        node
            Node number corresponding to this location.  Used only to associate
            a node with a new location or to find an existing location.

        nev
            Event number to be associated with these stresses (defaults to 1).

        nlod
            Loading number to be associated with these stresses (defaults to
            1).

        stitm
            Starting item number for entering stresses (defaults to 1).  If 1,
            data input in field C1 of this command is entered as the first item
            in the list; if 7, data input in field C1 of this command is
            entered as the seventh item in the list; etc.  Items are as
            follows:

            1-6 - SX, SY, SZ, SXY, SYZ, SXZ total stress components

            7 - Temperature

            8-13 - SX, SY, SZ, SXY, SYZ, SXZ membrane-plus-bending stress components.

            14 - Time

        c1, c2, c3, . . . , c6
            Stresses assigned to six locations starting with STITM.  If a value
            is already in one of these locations, it will be redefined.  A
            blank retains the previous value (except in the C1 field, which
            resets the STITM item to zero).

        Notes
        -----
        Stores fatigue stress components at a node as input on this command
        instead of from the current data in the database.  Stresses are stored
        according to the event number and loading number specified.  The
        location is associated with that previously defined for this node [FL]
        or else it is automatically defined.  May also be used to modify any
        previously stored stress components.  Stresses input with this command
        should be consistent with the global coordinate system for any FSNODE
        or FSSECT stresses used at the same location.
        """
        command = "FS,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (str(node), str(nev), str(nlod), str(stitm), str(c1), str(c2), str(c3), str(c4), str(c5), str(c6))
        return self.run(command, **kwargs)

    
    
    def ftwrite(self, fname="", ext="", **kwargs):
        """APDL Command: FTWRITE

        Writes all currently stored fatigue data on a file.

        Parameters
        ----------
        fname
            File name and directory path (248 characters maximum, including the
            characters needed for the directory path).  An unspecified
            directory path defaults to the working directory; in this case, you
            can use all 248 characters for the file name.

        ext
            Filename extension (eight-character maximum).

        Notes
        -----
        Data are written in terms of the equivalent POST1 fatigue commands
        [FTSIZE, FL, FS, etc.] which you can then edit and resubmit to POST1
        (with a /INPUT command).

        Once you have created a fatigue data file, each subsequent use of the
        FTWRITE command overwrites the contents of that file.
        """
        command = "FTWRITE,%s,%s" % (str(fname), str(ext))
        return self.run(command, **kwargs)

    def cat5in(self, name="", extension="", path="", entity="", fmt="",
               nocl="", noan="", **kwargs):
        """APDL Command: ~CAT5IN

        Transfers a .CATPart file into the ANSYS program.

        Parameters
        ----------
        name
            The name of a valid .CATPart file, created with CATIA Version 5.0.
            The first character of the file name must be an alphanumeric.

        extension
            The extension for the file. The default extension is .CATPart.

        path
            The path name of the directory in which the file resides enclosed
            in single quotes. The default path name is the current working
            directory.

        entity
            Entity to be imported.

            SOLIDS - Solids only, imported as ANSYS volumes (default).

            SURFACES - Surfaces only, imported as ANSYS areas.

            ALL - All entities. Use this option when the file contains different types of
                  entities.

        fmt
            The format in which ANSYS will store the model.

            0 - Neutral format (default). Defeaturing after import is restricted.

            1 - Solid format; this allows defeaturing after import.

        nocl
            Remove tiny objects.

            0 - Remove tiny objects without checking model validity (default).

            1 - Do not remove tiny objects.

        noan
            Perform an analysis of the model.

            0 - Analyze the model (default).

            1 - Do not analyze the model.

        Notes
        -----
        If defeaturing is specified (FMT = 1), this command must be the last
        line of any file, script, or other interactive input.

        More information on importing CATIA Version 5 parts is available in
        CATIA V5 in the Connection User's Guide.
        """
        command = "~CAT5IN,%s,%s,%s,%s,%s,%s,%s" % (str(name), str(extension), str(path), str(entity), str(fmt), str(nocl), str(noan))
        return self.run(command, **kwargs)

    # def if(self, val1="", oper1="", val2="", base1="", val3="", oper2="",
    #        val4="", base2="", **kwargs):
    #     """APDL Command: *IF

    #     Conditionally causes commands to be read.

    #     Parameters
    #     ----------
    #     val1
    #         First numerical value (or parameter which evaluates to a numerical
    #         value) in the conditional comparison operation.  VAL1, VAL2, VAL3,
    #         and VAL4 can also be character strings (enclosed in quotes) or
    #         parameters for Oper = EQ and NE only.

    #     oper1
    #         Operation label.  A tolerance of 1.0E-10 is used for comparisons
    #         between real numbers:

    #         Equal (for VAL1 = VAL2). - Not equal (for VAL1 ≠ VAL2).

    #         Less than (for VAL1 < VAL2). - Greater than (for VAL1 > VAL2).

    #         Less than or equal (for VAL1   VAL2). - Greater than or equal (for VAL1   VAL2).

    #         Absolute values of VAL1 and VAL2 before < operation. - Absolute values of VAL1 and VAL2 before > operation.

    #     val2
    #         Second numerical value (or parameter which evaluates to a numerical
    #         value) in the conditional comparison operation.

    #     base1
    #         Action based on the logical expression (Oper1) being true.  If
    #         false, continue reading at the next line. This is conditional,
    #         except for the IF-THEN-ELSE constructs described below; any of the
    #         following constructs (through Base1 = THEN) cause all subsequent
    #         fields to be ignored:

    #         A user-defined label (beginning with a colon (:), 8 characters maximum).  The command reader will skip (and wrap to the beginning of the file, if necessary) to the first line that begins with the matching :label. - Caution:   This label option may not be mixed with do-loop or if-then-else
    #                           constructs.

    #         This action will cause an exit from the ANSYS program at this line, unless running in interactive mode. In interactive mode, the program will not stop. - Exit the current do-loop [*EXIT].

    #         Skip to the end of the current do-loop [*CYCLE]. - Make this *IF an if-then-else construct (see below).

    #     val3
    #         Third numerical value (or parameter which evaluates to a numerical
    #         value).

    #     oper2
    #         Operation label. This will have the same labels as Oper1, except it
    #         uses Val3 and Val4. A tolerance of 1.0E-10 is used for comparisons
    #         between real numbers.

    #     val4
    #         Fourth numerical value (or parameter value which evaluates to a
    #         numerical value).

    #     base2
    #         Action based on the logical expression (Oper1 and Oper2) being
    #         true. They will be the same values as Base1, except as noted.

    #     Notes
    #     -----
    #     Conditionally causes commands to be read from a specific block or at a
    #     specific location.  Twenty levels of nested *IF blocks are allowed.
    #     Jumping to a :label line is not allowed with keyboard entry.  Jumping
    #     into, out of, or within a do-loop or an if-then-else construct to a
    #     :label line is not allowed. Using *IF interactively or from the command
    #     line prevents rereading the file to find a label. To do so, use batch
    #     mode or /INPUT.

    #     The following is an example of an if-then-else construct:

    #     *IF,VAL1,Oper,VAL2,THEN

    #     ----

    #     *ELSEIF,VAL1,Oper,VAL2

    #     ----

    #     *ELSEIF,VAL1,Oper,VAL2

    #     ----

    #     *ELSE

    #     ----

    #     *ENDIF

    #     where "----" represents a block of any number of commands.  Any number
    #     of *ELSEIF clauses (or none) may be included (in the location shown).
    #     One *ELSE clause (at most) may be included (in the location shown).
    #     The *IF command is executed by evaluating its logical expression.  If
    #     it is true, the block of commands following it is executed.  The
    #     construct is considered to be complete and the command following the
    #     *ENDIF is executed next.  If the logical expression is false, the next
    #     *ELSEIF command (if any) following the block is executed.  The
    #     execution logic is the same as for *IF.  The effect is that the logical
    #     expressions in the *IF and the *ELSEIF commands are sequentially tested
    #     until one is found to be true.  Then the block of commands immediately
    #     following the expression is executed, which completes the execution of
    #     the if-then-else construct.  If all *IF and *ELSEIF expressions are
    #     false, the block following the *ELSE command is executed, if there is
    #     one.  Only one block of commands (at most) is executed within the if-
    #     then-else construct.  If a batch input stream hits an end-of-file
    #     during a false *IF condition, the ANSYS run will not terminate
    #     normally. You will need to terminate it externally (use either the
    #     Linux "kill" function or the Windows task manager). The *IF, *ELSEIF,
    #     *ELSE, and *ENDIF commands for each if-then-else construct must all be
    #     read from the same file (or keyboard).

    #     This command is valid in any processor.
    #     """
    #     command = "*IF,%s,%s,%s,%s,%s,%s,%s,%s" % (str(val1), str(oper1), str(val2), str(b_ase1), str(val3), str(oper2), str(val4), str(b_ase2))
    #     return self.run(command, **kwargs)

    
    def fp(self, stitm="", c1="", c2="", c3="", c4="", c5="", c6="", **kwargs):
        """APDL Command: FP

        Defines the fatigue S vs. N and Sm vs. T tables.

        Parameters
        ----------
        stitm
            Starting item number for entering properties (defaults to 1).  If
            1, data input in field C1 of this command is entered as the first
            item in the list; if 7, data input in field C1 of this command is
            entered as the seventh item in the list; etc.  If the item number
            is negative, C1-C6 are ignored and the item is deleted.  If -ALL,
            the table is erased.  Items are as follows (items 41-62 are
            required only if simplified elastic-plastic code calculations are
            to be performed):

            1,2,...20 - N1, N2, ... N20

            21,22,...40 - S1, S2, ... S20

            41,42,...50 - T1, T2, ... T10

            51,52,...60 - Sm1, Sm2, ... Sm10

            61 - M (first elastic-plastic material parameter)

            62 - N (second elastic-plastic material parameter)

        c1, c2, c3, . . . , c6
            Data inserted into six locations starting with STITM.  If a value
            is already in one of these locations, it will be redefined.  A
            blank retains the previous value.

        Notes
        -----
        Defines the fatigue alternating stress (S) vs. cycles (N) table and the
        design stress-intensity value (Sm) vs. temperature (T) table.  May also
        be used to modify any previously stored property tables.  Log-log
        interpolation is used in the S vs. N table and linear interpolation is
        used in the Sm vs. T table.  Cycles and temperatures must be input in
        ascending order; S and Sm values in descending order.  Table values
        must be supplied in pairs, i.e., every N entry must have a
        corresponding S entry, etc.  Not all property pairs per curve need be
        used.  If no S vs. N table is defined, the fatigue evaluation will not
        produce usage factor results.  See the Structural Analysis Guide for
        details.
        """
        command = "FP,%s,%s,%s,%s,%s,%s,%s" % (str(stitm), str(c1), str(c2), str(c3), str(c4), str(c5), str(c6))
        return self.run(command, **kwargs)

    def term(self, kywrd="", opt1="", opt2="", opt3="", **kwargs):
        """APDL Command: TERM

        Specifies various terminal driver options.

        Parameters
        ----------
        ncopy
            Activate hard copy device for NCOPY (0,1,2, etc.) copies.

        Notes
        -----
        Used only with terminal driver names on /SHOWDISP command.

        This command is also valid in PREP7.
        """
        command = "TERM,%s,%s,%s,%s" % (str(kywrd), str(opt1), str(opt2), str(opt3))
        return self.run(command, **kwargs)

    
    
    def slashdelete(self, fname="", ext="", distkey="", **kwargs):
        """APDL Command: /DELETE

        Deletes a file.

        Parameters
        ----------
        fname
            File name and directory path (248 characters maximum,
            including the characters needed for the directory path).
            An unspecified directory path defaults to the working
            directory; in this case, you can use all 248 characters
            for the file name.

        ext
            Filename extension (eight-character maximum).

        distkey
            Key that specifies whether the file deletion is performed
            on all processes in distributed parallel mode (Distributed
            ANSYS):

            1 (ON or YES) - The program performs the file deletion
            locally on each process.

            0 (OFF or NO) - The program performs the file deletion
            only on the master process (default).

        Notes
        -----
        In distributed parallel mode (Distributed ANSYS), only the
        master process will delete Fname.Ext by default. However, when
        DistKey is set to 1 (or ON or YES), the command is executed by
        all processes. In this case, Fname will automatically have the
        process rank appended to it.  This means FnameN.Ext will be
        deleted by all processes, where N is the Distributed ANSYS
        process rank. For more information see Differences in General
        Behavior in the Parallel Processing Guide.
        """
        return self.run(f"/DELETE,{fname},{ext},,{distkey}", **kwargs)

    
    
    
    
    
    
    def fslist(self, nloc1="", nloc2="", ninc="", nev="", nlod="", **kwargs):
        """APDL Command: FSLIST

        Lists the stresses stored for fatigue evaluation.

        Parameters
        ----------
        nloc1, nloc2, ninc
            List stresses from NLOC1 (defaults to 1) to NLOC2 (defaults to
            NLOC1) in steps of NINC (defaults to 1).  If NLOC1 = ALL, NLOC2 and
            NINC are ignored and stresses for all locations are listed.

        nev
            Event number for stress listing (defaults to ALL).

        nlod
            Loading number for stress listing (defaults to ALL).

        Notes
        -----
        Stresses may be listed per location, per event, per loading, or per
        stress condition.  Use FELIST and FLLIST if only event and location
        parameters (no stresses) are to be listed.
        """
        command = "FSLIST,%s,%s,%s,%s,%s" % (str(nloc1), str(nloc2), str(ninc), str(nev), str(nlod))
        return self.run(command, **kwargs)

    
    
    
    def cgrow(self, action="", par1="", par2="", **kwargs):
        """APDL Command: CGROW

        Defines crack-growth information

        Parameters
        ----------
        action
            Specifies the action for defining or manipulating crack-growth
            data:

            NEW - Initiate a new set of crack-growth simulation data (default).

            CID - Specify the crack-calculation (CINT) ID for energy-release rates to be used in
                  the fracture criterion calculation.

            FCOPTION - Specify the fracture criterion for crack-growth/delamination.

            CPATH - Specify the element component for crack growth.

            DTIME - Specify the initial time step for crack growth.

            DTMIN - Specify the minimum time step for crack growth.

            DTMAX - Specify the maximum time step for crack growth.

            FCRAT - Fracture criterion ratio (fc).

            STOP - Stops the analysis when the specified maximum crack extension is reached.

            METHOD - Define the method of crack propagation.

        Notes
        -----
        When Action = NEW, the CGROW command initializes a crack-growth
        simulation set. Subsequent CGROW commands define the parameters
        necessary for the simulation.

        For multiple cracks, issue multiple CGROW,NEW commands (and any
        subsequent CGROW commands necessary to define the parameters) for each
        crack.

        If the analysis is restarted (ANTYPE,,RESTART), the CGROW command must
        be re-issued.

        For VCCT crack growth:

        Crack-growth element components must use the crack tip nodes as the
        starting nodes of the crack path.

        Fracture criteria (Action = FCOPTION) use energy-release rates
        calculated via VCCT technology (CINT,TYPE,VCCT). For information about
        the fracture criteria available, see Fracture Criteria in the Fracture
        Analysis Guide or the documentation for the TB,CGCR command.

        For XFEM-based crack growth:

        When using XFEM to grow the crack (CGROW,METHOD,XFEM), the crack
        specification originates via the XFENRICH and XFDATAa   >       c   o
        m   m   a   n   d   s   .       /   p   >   /   l   i   >   l   i
        c   l   a   s   s   =   "   l   i   s   t   i   t   e   m   "   >   p
        >   I   n       a   n       X   F   E   M   -   b   a   s   e   d
        c   r   a   c   k       g   r   o   w   t   h       a   n   a   l   y
        s   i   s   ,       e   m       c   l   a   s   s   =   "   r   e   p
        l   a   c   e   a   b   l   e   "   >   c   o   d   e   >   A   c   t
        i   o   n   /   c   o   d   e   >   /   e   m   >       =       C   P
        A   T   H   ,   D   T   M   I   N   ,   D   T   M   A   X       a   n
        d       S   T   O   P       h   a   v   e       n   o       e   f   f
        e   c   t   .   /   p   >   /   l   i   >   /   u   l   >   /   d   i
        v   >   /   d   i   v   >   d   i   v       c   l   a   s   s   =   "
        r   e   f   s   e   c   t   1   "       t   i   t   l   e   =   "   M
        e   n   u       P   a   t   h   s   "   >   a       n   a   m   e   =
        "   C   G   R   O   W   .   m   e   n   u   p   a   t   h   "   >   /
        a   >   h   2   >   M   e   n   u       P   a   t   h   s   /   h   2
        >   t   a   b   l   e       b   o   r   d   e   r   =   "   0   "
        s   u   m   m   a   r   y   =   "   S   i   m   p   l   e       l   i
        s   t   "       c   l   a   s   s   =   "   s   i   m   p   l   e   l
        i   s   t   "   >   t   r   >   t   d   >   s   p   a   n       c   l
        a   s   s   =   "   g   u   i   m   e   n   u   "   >   s   t   r   o
        n   g   >   T   h   i   s       c   o   m   m   a   n   d       c   a
        n   n   o   t       b   e       a   c   c   e   s   s   e   d       f
        r   o   m       a       m   e   n   u   .   /   s   t   r   o   n   g
        >   /   s   p   a   n   >   /   t   d   >   /   t   r   >   /   t   a
        b   l   e   >   /   d   i   v   >   /   d   i   v   >   h   r   >   p
        c   l   a   s   s   =   "   l   e   g   a   l   f   o   o   t   e   r
        "   >   s   m   a   l   l   >   i   >   R   e   l   e   a   s   e
        1   6   .   2       -       &c   o   p   y   ;       S   A   S       I
        P   ,       I   n   c   .       A   l   l       r   i   g   h   t   s
        r   e   s   e   r   v   e   d   .   /   i   >   /   s   m   a   l   l
        >   /   p   >   /   b   o   d   y   >   /   h   t   m   l   >
        """
        command = "CGROW,%s,%s,%s" % (str(action), str(par1), str(par2))
        return self.run(command, **kwargs)

    
    
    
    
    def secfunction(self, table="", kcn="", **kwargs):
        """APDL Command: SECFUNCTION

        Specifies shell section thickness as a tabular function.

        Parameters
        ----------
        table
            Table name or array parameter reference for specifying thickness.

        kcn
            Local coordinate system reference number or array interpretation
            pattern for this tabular function evaluation.

        Notes
        -----
         The SECFUNCTION command is associated with the section most recently
        defined via the SECTYPE command.

        A table (TABLE) can define tabular thickness as a function of
        coordinates. Alternatively, you can use an array parameter (indexed by
        node number) that expresses the function to be mapped. (For example,
        func (17) should be the desired shell thickness at node 17.)  To
        specify a table, enclose the table or array name in percent signs (%)
        (SECFUNCTION,%tablename%). Use the *DIM command to define a table.

        The table or array defines the total shell thickness at any point in
        space. In multilayered sections, the total thickness and each layer
        thickness are scaled accordingly.

        The Function Tool is a convenient way to define your thickness tables.
        For more information, see Using the Function Tool in the Basic Analysis
        Guide.

        If you do not specify a local coordinate system (KCN), the program
        interprets TABLE in global XYZ coordinates. (For information about
        local coordinate systems, see the LOCAL command documentation.)

        When KCN = NODE, the program interprets TABLE as an array parameter
        (indexed by node number) that expresses the function to be mapped.

        When KCN = NOD2, the program interprets TABLE as a 2-D array parameter
        (where columns contain node numbers and rows contain the corresponding
        thicknesses) that expresses the function to be mapped.
        """
        command = "SECFUNCTION,%s,%s" % (str(table), str(kcn))
        return self.run(command, **kwargs)

    
    
    def pdwrite(self, file="", fnam="", lnam="", **kwargs):
        """APDL Command: PDWRITE

        Generates an HTML report for the probabilistic analyses.

        Parameters
        ----------
        file
            File name and directory path (248 characters maximum, including
            directory) from which to read the report. If you do not specify a
            directory path, it will default to your working directory and you
            can use all 248 characters for the file name.

        fnam
            First name of the author of the report (32 characters maximum).
            This first name must not include blanks.

        lnam
            Last name of the author of the report (32 characters maximum). This
            last name must not include blanks.

        Notes
        -----
        Generates an HTML report for the probabilistic analysis. An HTML report
        includes a description of the deterministic model, the probabilistic
        model, the probabilistic methods used for the analyses and the results
        obtained from the analyses.
        """
        command = "PDWRITE,%s,%s,%s" % (str(file), str(fnam), str(lnam))
        return self.run(command, **kwargs)

    
    def fplist(self, **kwargs):
        """APDL Command: FPLIST

        Lists the property table stored for fatigue evaluation.
        """
        command = "FPLIST,"
        return self.run(command, **kwargs)

    
    
    def uis(self, label="", value="", **kwargs):
        """APDL Command: /UIS

        Controls the GUI behavior.

        Parameters
        ----------
        label
            Behavior control key:

            BORD - Controls the functionality of the mouse buttons for dynamic viewing mode only.
                   When Label = BORD, the three values that follow control the
                   functionality of the LEFT, MIDDLE and RIGHT buttons,
                   respectively (see below).

            MSGPOP - Controls which messages from the ANSYS error message subroutine are displayed
                     in a message dialog box.

            REPLOT - Controls whether or not an automatic replot occurs after functions affecting
                     the model are executed.

            ABORT - Controls whether or not ANSYS displays dialog boxes to show the status of an
                    operation in progress and to cancel that operation.

            DYNA - Controls whether the dynamic mode preview is a bounding box or the edge outline
                   of the model.  This label only applies to 2-D display
                   devices (i.e., /SHOW,XII or /SHOW,WIN32).  This "model edge
                   outline" mode is only supported in PowerGraphics
                   [/GRAPHICS,POWER] and is intended for element, line,
                   results, area, or volume displays.

            PICK - Controls how graphical entities are highlighted from within the ANSYS Select
                   menu.

            POWER - Controls whether or not PowerGraphics is active when the GUI is initiated. The
                    ANSYS program default status is PowerGraphics "ON";  this
                    command is used (placed in the start.ans file) when full
                    graphics is desired on start up.

            DPRO - Controls whether or not the ANSYS input window displays a dynamic prompt. The
                   dynamic prompt shows the correct command syntax for the
                   command, as you are entering it.

            UNDO - Controls whether or not the session editor includes nonessential commands or
                   comments in the file it creates. You can use this option to
                   include comments and other materials in the session editor
                   file.

            LEGE - Controls whether or not the multi-legend is activated when you start the GUI.
                   The multi-legend enables you to specify the location of your
                   legend items in each of the five graphics windows. You can
                   place this option in your start.ans file and have the GUI
                   start with the legend items in a pre-specified location.

            PBAK - Controls whether or not the background shading is activated when you start the
                   GUI. You can place this option in your start.ans file.

            ZPIC - Controls the sorting order for entities that are coincident (directly in front
                   of or behind each other) to a picked spot on your model.
                   When you pick a spot on your model that could indicate two
                   or more entities, a message warns you of this condition, and
                   a list of the coincident entities can be generated. The
                   VALUE term (below) will determine the sort order.

            HPOP - Controls the prioritization of your GUI windows when the contents are ported to
                   a plot or print file (/UI,COPY,SAVE). OpenGL (3D) graphics
                   devices require that the ANSYS Graphics Screen contents be
                   set in front of all overlying windows in order to port them
                   to a printer or a file. This operation can sometimes
                   conflict with /NOERASE settings. See the VALUE term (below)
                   to determine the available control options.

        value
            Values controlling behavior if Label = BORD:

            1 - PAN, controls dynamic translations.

            2 - ZOOM, controls zoom, and dynamic rotation about the view vector.

            3 - ROTATE, controls dynamic rotation about the screen X and Y axes.
        """
        command = "/UIS,%s,%s" % (str(label), str(value))
        return self.run(command, **kwargs)

    def spower(self, inletport="", outletport="", **kwargs):
        """APDL Command: SPOWER

        Calculates sound power parameters.

        Parameters
        ----------
        inletport
            Inlet source port number.

        outletport
            Outlet port number.

        Notes
        -----
        The SPOWER command calculates the input sound power level, reflected
        sound power level, return loss, and absorption coefficient for an inlet
        port.

        If a matched outlet port is defined, the command also calculates the
        transmission loss.

        The sound power parameters are output to the file
        jobname%ARG1%%ARG2%.anp (where n = 1 or 2).

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = "SPOWER,%s,%s" % (str(inletport), str(outletport))
        return self.run(command, **kwargs)

    
    
    
    
    def segen(self, mode="", nsuper="", mdof="", stopstage="", **kwargs):
        """APDL Command: SEGEN

        Automatically generate superelements.

        Parameters
        ----------
        mode
            Specify action to take (must be specified as one of the following):

            AUTO - Turn on feature.

            OFF - Turn off feature.

        nsuper
            Number of superelements to create. The minimum number of
            superelements is 2, and the maximum number of superelements is 999.
            Note that the number of requested superelements may not be the same
            as the number of defined superelements (see "Notes" for more
            details).

        mdof
            Specifies whether to use the master DOF defined by the user.

            YES - Use master DOF defined by the user with the M command.

            NO - Use the master DOF defined by the automatic generation process. Be aware that
                 this option can generate a large number of master DOFs (see
                 "Notes"  for more details).

        stopstage
            Specifies when to stop the automatic superelement generation
            process.

            PREVIEW - Preview the superelements only; stop after creating the domains which will
                      become the superelements, and after creating master DOF
                      on the interfaces between each domain.

            GEN - Create (generate) the superelements.

        Notes
        -----
        This command can be used to quickly generate a set of superelements.
        Each superelement is created in a separate file (jobnameXXX.sub, where
        XXX is a positive number from 1 to 999).

        Due to the heuristics in the automatic domain decomposer, which is used
        to define the domains that will become superelements, the number of
        defined superelements may exceed the number of requested superelements.
        Use the mDof and stopStage options to determine exactly how many
        superelements will be created, the interfaces between each
        superelement, and where master DOF will be defined. With the
        /PNUM,DOMAIN command, you can graphically (visually) preview the
        elements in each superelement.  Then, if required, you can add
        additional master DOF to (or remove from) the boundaries of the
        superelements. Use the SEGEN command again with stopStage = GEN to
        actually create the superelements.

        ANSYS automatically defines master DOF at each of the following: all
        interface DOF between superelements, all DOF attached to contact
        elements (TARGE169 to CONTA177), and all DOF associated with nodes
        having a point load defined.  Note that for regular superelements, all
        interface DOFs must be defined as master DOFs for the correct solution
        to be obtained. However, for CMS superelements, some of the interface
        DOFs can be removed without a significant loss of accuracy.

        For the case when mDof = YES, you should select the preview option
        first (stopStage = PREVIEW) to verify exactly how many superelements
        will be created and where the superelement boundaries are located.  If
        more superelements will be created than were requested, you should
        define master DOF on the interface(s) between all superelements.

        This command is valid only for substructuring analyses (ANTYPE,SUBSTR).
        Use SEOPT to specify any options for all of the superelements (e.g.,
        which matrices to reduce), and possibly CMSOPT for any CMS
        substructuring analysis.  Note that the created superelements will
        follow the current /FILNAME instead of SENAME from SEOPT.  Also, only
        one load vector will be written to each .SUB file.  Multiple load steps
        are not supported with the automatic superelement generation process.

        During the actual creation of the superelements, the output is
        redirected to jobname.autoTemp.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = "SEGEN,%s,%s,%s,%s" % (str(mode), str(nsuper), str(mdof), str(stopstage))
        return self.run(command, **kwargs)

    
    
    def pdcmat(self, rlab="", matrix="", name1="", name2="", corr="",
               slevel="", popt="", **kwargs):
        """APDL Command: PDCMAT

        Prints the correlation coefficient matrix.

        Parameters
        ----------
        rlab
            Result set label. Identifies the result set to be used for
            postprocessing. A result set label can be the solution set label
            you defined in a PDEXE command (if you are directly postprocessing
            Monte Carlo Simulation results), or the response surface set label
            defined in an RSFIT command (for Response Surface Analyses).

        matrix
            Keyword for the type of correlation coefficient matrix.

            IO - Matrix of correlation coefficients between random input variables and output
                 parameters.

            II - Matrix of correlation coefficients between random input variables and other
                 random input variables

            OO - Matrix of correlation coefficients between random output parameters and other
                 random output parameters.

            S - Correlation coefficient between a single random parameter (input or output) and
                another random parameter (input or output). The probabilistic
                design parameters must be specified in Name1 and Name2 for this
                option.

        name1, name2
            Parameter names. The parameters must have been previously defined
            as a random input variable or a random output parameter with the
            PDVAR command. These parameters are used for Matrix = S only and
            are ignored for the other Matrix keywords.

        corr
            Keyword for the type of correlation coefficients to be used for the
            output.

            RANK - Spearman rank-order correlation coefficient (default).

            LIN - Pearson linear correlation coefficient.

        slevel
            Significance level. The value for the significance level must be
            between 0.0 and 1.0. The default value is 0.025 (2.5%).

        popt
            Specifies whether the probabilities should be printed with the
            correlation coefficients.

            0 - Print only the correlation coefficients.

            1 - Print both the correlation coefficients and the probabilities (default).

        Notes
        -----
        Prints the correlation coefficient matrix.

        If Rlab is left blank, then the result set label is inherited from the
        last PDEXE command (Slab), RSFIT command (RSlab), or the most recently
        used PDS postprocessing command where a result set label was explicitly
        specified.

        For all correlation coefficients the probabilistic design tool
        evaluates the probability that the correlation coefficient can be
        neglected. The evaluation of this probability is based on statistical
        test theory. The larger this probability is the likelier it is that the
        correlation coefficient does not really reflect an observable
        statistical interdependence between the parameters involved. If this
        probability exceeds the significance level as specified by the SLEVEL
        parameter, the correlation coefficient should be regarded as negligible
        or insignificant. The higher the significance level SLEVEL, the more
        correlation coefficients are considered significant. Using the Popt
        parameter you can also get a list of the probabilities and review them
        as to how far they exceed the significance level or how far they stay
        below it.

        The PDCMAT command cannot be used to postprocess the results in a
        solution set that is based on Response Surface Methods, only Monte
        Carlo Simulations.
        """
        command = "PDCMAT,%s,%s,%s,%s,%s,%s,%s" % (str(rlab), str(matrix), str(name1), str(name2), str(corr), str(slevel), str(popt))
        return self.run(command, **kwargs)

    
    def starvget(self, parr="", entity="", entnum="", item1="", it1num="",
                 item2="", it2num="", kloop="", **kwargs):
        """APDL Command: *VGET

        Retrieves values and stores them into an array parameter.

        Parameters
        ----------
        parr
            The name of the resulting vector array parameter.  See *SET for
            name restrictions.

        entity
            Entity keyword.  Valid keywords are NODE, ELEM, KP, LINE, AREA,
            VOLU, etc. as shown for Entity = in the tables below.

        entnum
            The number of the entity (as shown for ENTNUM = in the tables
            below).

        item1
            The name of a particular item for the given entity.  Valid items
            are as shown in the Item1 columns of the tables below.

        it1num
            The number (or label) for the specified Item1 (if any).  Valid
            IT1NUM values are as shown in the IT1NUM columns of the tables
            below.  Some Item1 labels do not require an IT1NUM value.

        item2, it2num
            A second set of item labels and numbers to further qualify the item
            for which data is to be retrieved.  Most items do not require this
            level of information.

        kloop
            Field to be looped on:

            Loop on the ENTNUM  field (default). - Loop on the Item1 field.

            Loop on the IT1NUM field.  Successive items are as shown with IT1NUM. - Loop on the Item2 field.

        Notes
        -----
        Retrieves values for specified items and stores the values in an output
        vector of a user-named array parameter according to:

        ParR = f(Entity, ENTNUM, Item1, IT1NUM, Item2, IT2NUM)

        where (f) is the *GET function; Entity, Item1, and Item2 are keywords;
        and ENTNUM, IT1NUM, and IT2NUM are numbers or labels corresponding to
        the keywords. Looping continues over successive entity numbers (ENTNUM)
        for the KLOOP default.  For example, *VGET,A(1),ELEM,5,CENT,X returns
        the centroid x-location of element 5 and stores the result in the first
        location of A.  Retrieving continues with element 6, 7, 8, etc.,
        regardless of whether the element exists or is selected, until
        successive array locations are filled.  Use *VLEN or *VMASK to skip
        locations. Absolute values and scale factors may be applied to the
        result parameter [*VABS, *VFACT].  Results may be cumulative [*VCUM].
        See the *VOPER command for general details.  Results can be put back
        into an analysis by writing a file of the desired input commands with
        the *VWRITE command.  See also the *VPUT command.

        Both *GET and *VGET retrieve information from the active data stored in
        memory. The database is often the source, and sometimes the information
        is retrieved from common memory blocks that ANSYS uses to manipulate
        information. Although POST1 and POST26 operations use a *.rst file, GET
        data is accessed from the database or from the common blocks. Get
        operations do not access the *.rst file directly.

        The *VGET command retrieves both the unprocessed real and the imaginary
        parts (original and duplicate sector nodes and elements) of a cyclic
        symmetry solution.

        Each of the sections for accessing *VGET parameters are shown in the
        following order:

        *VGET PREP7 Items

        *VGET POST1 Items

        This command is valid in any processor.
        """
        command = "*VGET,%s,%s,%s,%s,%s,%s,%s,%s" % (str(parr), str(entity), str(entnum), str(item1), str(it1num), str(item2), str(it2num), str(kloop))
        return self.run(command, **kwargs)

    
    
    def secmodif(self, secid="", kywrd="", **kwargs):
        """APDL Command: SECMODIF

        Modifies a pretension section

        Parameters
        ----------
        secid
            Unique section number. This number must already be assigned to a
            section.

        norm
            Keyword specifying that the command will modify the pretension
            section normal direction.

        nx, ny, nz
            Specifies the individual normal components to modify.

        kcn
            Coordinate system number. This can be either 0 (Global Cartesian),
            1 (Global Cylindrical) 2 (Global Spherical), 4 (Working Plane), 5
            (Global Y Axis Cylindrical) or an arbitrary reference number
            assigned to a coordinate system.

        Notes
        -----
        The SECMODIF command either modifies the normal for a specified
        pretension section, or changes the name of the specified pretension
        surface.
        """
        command = "SECMODIF,%s,%s" % (str(secid), str(kywrd))
        return self.run(command, **kwargs)

    
    
    def ftsize(self, mxloc="", mxev="", mxlod="", **kwargs):
        """APDL Command: FTSIZE

        Defines the fatigue data storage array.

        Parameters
        ----------
        mxloc
            Maximum number of fatigue locations (defaults to 5).

        mxev
            Maximum number of fatigue events (defaults to 10).

        mxlod
            Maximum number of loadings in each event (defaults to 3).

        Notes
        -----
        Defines the size and erases the stress conditions for the fatigue data
        storage array.  A stress condition is a loading (stresses) at a
        particular location (node) for a particular event.  Size is defined in
        terms of the maximum number of locations, events, and loadings.  The
        array size cannot be changed once data storage has begun (without
        erasing all previously stored data).  If a size change is necessary,
        see the FTWRITE command.
        """
        command = "FTSIZE,%s,%s,%s" % (str(mxloc), str(mxev), str(mxlod))
        return self.run(command, **kwargs)

    
    def menu(self, key="", **kwargs):
        """APDL Command: /MENU

        Activates the Graphical User Interface (GUI).

        Parameters
        ----------
        key
            Activation key:

            ON - Activates the menu system (device dependent).

            GRPH - Enters non-GUI graphics mode.

        Notes
        -----
        Activates the Graphical User Interface (GUI).

        Caution:: : if you include the /MENU,ON command in your start162.ans,
        it should be the last command in the file.  Any commands after /MENU,ON
        may be ignored.  (It is not necessary to include the /SHOW and /MENU,ON
        commands in start162.ans if you will be using the launcher to enter the
        ANSYS program.)

        This command is valid in any processor.
        """
        command = "/MENU,%s" % (str(key))
        return self.run(command, **kwargs)

    
    
    def slashtype(self, wn="", type_="", **kwargs):
        """APDL Command: /TYPE

        Defines the type of display.

        Parameters
        ----------
        wn
            Window number (or ALL) to which command applies (defaults to 1).

        type\_
            Display type.  Defaults to ZBUF for raster mode displays or BASIC
            for vector mode displays:

            BASIC or 0 - Basic display (no hidden or section operations).

            SECT or 1 - Section display (plane view).  Use the /CPLANE command to define the cutting
                        plane.

            HIDC or 2 - Centroid hidden display (based on item centroid sort).

            HIDD or 3 - Face hidden display (based on face centroid sort).

            HIDP or 4 - Precise hidden display (like HIDD but with more precise checking). Because all
                        facets are sorted, this mode can be extremely slow,
                        especially for large models.

            CAP or 5 - Capped hidden display (same as combined SECT and HIDD with model in front of
                       section plane removed).

            ZBUF or 6 - Z-buffered display (like HIDD but using software Z-buffering).

            ZCAP or 7 - Capped Z-buffered display (same as combined SECT and ZBUF with model in front
                        of section plane removed).

            ZQSL or 8 - QSLICE Z-buffered display (same as SECT but the edge lines of the remaining 3-D
                        model are shown).

            HQSL or 9 - QSLICE precise hidden display (like ZQSL but using precise hidden).

        Notes
        -----
        Defines the type of display, such as section display or hidden-line
        display.  Use the /DEVICE command to specify either raster or vector
        mode.

        The SECT, CAP, ZCAP, ZQSL, and HQSL options produce section displays.
        The section or "cutting" plane is specified on the /CPLANE command as
        either normal to the viewing vector at the focus point (default), or as
        the working plane.

        When you use PowerGraphics, the section display options (Section,
        Slice, and Capped) use different averaging techniques for the interior
        and exterior results. Because of the different averaging schemes,
        anomalies may appear at the transition areas. In many cases, the
        automatically computed MIN and MAX values will differ from the full
        range of interior values. You can lessen the effect of these anomalies
        by issuing AVRES,,FULL (Main Menu> General Post Proc> Options for
        Outp). This command sets your legend's automatic contour interval range
        according to the minimum and maximum results found throughout the
        entire model.

        With PowerGraphics active (/GRAPHICS,POWER), the averaging scheme for
        surface data with interior element data included (AVRES,,FULL) and
        multiple facets per edge (/EFACET,2 or /EFACET,4) will yield differing
        minimum and maximum contour values depending on the  Z-Buffering
        options (/TYPE,,6 or /TYPE,,7).  When the Section data is not included
        in the averaging schemes (/TYPE,,7), the resulting absolute value for
        the midside node is significantly smaller.

        The HIDC, HIDD, HIDP, ZBUF, ZQSL, and HQSL options produce displays
        with "hidden" lines removed.  Hidden lines are lines obscured from view
        by another element, area, etc.  The choice of non-Z-buffered hidden-
        line procedure types is available only for raster mode [/DEVICE]
        displays.  For vector mode displays, all non-Z-buffered "hidden-line"
        options use the same procedure (which is slightly different from the
        raster procedures).  Both geometry and postprocessing displays may be
        of the hidden-line type.  Interior stress contour lines within solid
        elements can also be removed as hidden lines, leaving only the stress
        contour lines and element outlines on the visible surfaces.  Midside
        nodes of elements are ignored on postprocessing displays.  Overlapping
        elements will not be displayed.

        The ZBUF, ZCAP, and ZQSL options use a specific hidden-line technique
        called software Z-buffering.  This technique allows a more accurate
        display of overlapping surfaces (common when using Boolean operations
        or /ESHAPE on element displays), and allows smooth shaded displays on
        all interactive graphics displays.  Z-buffered displays can be
        performed faster than HIDP and CAP type displays for large models.  See
        also the /LIGHT, /SHADE, and /GFILE commands for additional options
        when Z-buffering is used.

        This command is valid in any processor.
        """
        command = "/TYPE,%s,%s" % (str(wn), str(type_))
        return self.run(command, **kwargs)

    
    def fl(self, nloc="", node="", scfx="", scfy="", scfz="", title="",
           **kwargs):
        """APDL Command: FL

        Defines a set of fatigue location parameters.

        Parameters
        ----------
        nloc
            Reference number for this location (within MXLOC).  When defining a
            new location, defaults to lowest unused location.  If the specified
            NODE is already associated with a location, NLOC defaults to that
            existing location.

        node
            Node number corresponding to this location (must be unique).  Used
            only to associate a node with a new location or to find an existing
            location (if NLOC is not input).  If NODE = -1 (or redefined),
            erase all parameters and fatigue stresses for this location.

        scfx, scfy, scfz
            Stress concentration factors applied to the total stresses.
            Factors are applied in the global X, Y, and Z directions unless the
            axisymmetric option of the FSSECT is used (i.e., RHO is nonzero),
            in which case the factors are applied in the section x, y, and z
            (radial, axial, and hoop) directions.

        title
            User-defined title for this location (up to 20 characters).

        Notes
        -----
        Repeat FL command to define additional sets of location parameters
        (MXLOC limit), to redefine location parameters, or to delete location
        stress conditions.

        One location must be defined for each node of interest and only one
        node can be associated with each location.  See the FTSIZE command for
        the maximum locations (MXLOC) allowed.  A location will be
        automatically defined for a node not having a location when the FSSECT,
        FSNODE, or FS command is issued.  Automatically defined locations are
        assigned the lowest available location number, unity stress
        concentration factors, and no title.
        """
        command = "FL,%s,%s,%s,%s,%s,%s" % (str(nloc), str(node), str(scfx), str(scfy), str(scfz), str(title))
        return self.run(command, **kwargs)

    
    
    
    def pdanl(self, fname="", ext="", **kwargs):
        """APDL Command: PDANL

        Defines the analysis file to be used for probabilistic looping.

        Parameters
        ----------
        fname
            File name and directory path (248 characters maximum, including the
            characters needed for the directory path).  An unspecified
            directory path defaults to the working directory; in this case, you
            can use all 248 characters for the file name.

        ext
            Filename extension (eight-character maximum).

        Notes
        -----
        The analysis file containing the deterministic, parameterized model
        must be specified if the probabilistic analysis is performed
        interactively. The file must exist at the time the PDANL command is
        issued. In this file, where /PREP7 and /PDS occur, they must be the
        first nonblank characters on the line (do not use the $ delimiter on
        any /PREP7 and /PDS command lines).

        By default the analysis files specified with PDANL are executed from
        the top. All definitions of random input variables (for example, APDL
        parameters defined as random input variables with the PDVAR command,
        using *SET or Pname = ... ) are ignored in the analysis file. The PDS
        takes control of setting the values of random input variable values for
        each loop.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = "PDANL,%s,%s" % (str(fname), str(ext))
        return self.run(command, **kwargs)

    
    
    
    def fllist(self, nloc1="", nloc2="", ninc="", **kwargs):
        """APDL Command: FLLIST

        Lists the fatigue location parameters.

        Parameters
        ----------
        nloc1, nloc2, ninc
            List location parameters from NLOC1 (defaults to 1) to NLOC2
            (defaults to NLOC1) in steps of NINC (defaults to 1).  If NLOC1 =
            ALL, NLOC2 and NINC are ignored and all locations are listed.
        """
        command = "FLLIST,%s,%s,%s" % (str(nloc1), str(nloc2), str(ninc))
        return self.run(command, **kwargs)

    
    
    
    
