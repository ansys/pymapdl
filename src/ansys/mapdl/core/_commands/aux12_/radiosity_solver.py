class RadiositySolver:
    def hemiopt(self, hres="", **kwargs):
        """Specifies options for Hemicube view factor calculation.

        APDL Command: HEMIOPT

        Parameters
        ----------
        hres
            Hemicube resolution.  Increase value to increase the accuracy of
            the view factor calculation.  Defaults to 10.
        """
        command = f"HEMIOPT,{hres}"
        return self.run(command, **kwargs)

    def radopt(
        self,
        fluxtol="",
        solver="",
        maxiter="",
        toler="",
        overrlex="",
        maxfluxiter="",
        **kwargs,
    ):
        """Specifies Radiosity Solver options.

        APDL Command: RADOPT

        Parameters
        ----------
        fluxtol
            Convergence tolerance for radiation flux. Defaults to 0.0001. This
            value is a relative tolerance.

        solver
            Choice of solver for radiosity calculation:

            0 - Gauss-Seidel iterative solver (default).

            1 - Direct solver.

            2 - Jacobi solver.

        maxiter
            Maximum number of iterations for iterative solver (SOLVER = 0 or
            2). Defaults to 1000.

        toler
            Convergence tolerance for the iterative solver (SOLVER = 0 or 2).
            Defaults to 0.1.

        overrlex
            Over-relaxation factor applied to the iterative solver (SOLVER = 0
            or 2). Defaults to 0.1.

        maxfluxiter
            Maximum number of flux iterations to be performed according to the
            specified solver type:

            0 - If the FULL solver is specified (THOPT,FULL), convergence criteria are
                monitored and iterations are performed until convergence
                occurs. If the QUASI solver is specified (THOPT,QUASI),
                convergence criteria are ignored and one iteration is
                performed. This value is the default.

            1, 2, 3, ...N  - If the FULL solver is specified
                             (THOPT,FULL), convergence criteria are
                             monitored and iterations are performed
                             until convergence occurs, or until the
                             specified number of iterations has been
                             completed, whichever comes first. If the
                             QUASI solver is specified (THOPT,QUASI),
                             convergence criteria are ignored and the
                             specified number of iterations are
                             completed.

        Notes
        -----
        The radiation heat flux is linearized, resulting in robust convergence.

        The radiation flux norm for FLUXTOL is expressed as:

        where i is the pass or iteration number and j is the surface facet for
        radiation.

        For a sufficiently small absolute tolerance value, relative tolerance
        converges in fewer iterations than absolute tolerance. For a
        sufficiently large absolute tolerance value, relative tolerance may
        cause convergence difficulties.

        For more information about FLUXTOL and MAXFLUXITER usage, see Figure:
        3.5:: FULL Solution Method When Radiosity Is Present and Figure: 3.6::
        QUASI Solution Method When Radiosity Is Present in the Thermal Analysis
        Guide.

        In Figure: 3.5:: FULL Solution Method When Radiosity Is Present and
        Figure: 3.6:: QUASI Solution Method When Radiosity Is Present (under
        Solving for Temperature and Radiosity in the Thermal Analysis Guide),
        refer to the KQQ = FQ equation system via the iterative method:

        If TOLER ≥ 0, the iterative solver is converged for maximum value over
        a different j as shown:

        If TOLER < 0, the iterative solver is converged for maximum value over
        a different j as shown:

        where:

        The Jacobi solver (SOLVER = 2) is suitable when using Distributed
        ANSYS. This option is only available for 3-D models; if SOLVER is set
        to 2 for a 2-D analysis, the Gauss-Seidel iterative solver (SOLVER = 0)
        is used.
        """
        command = (
            f"RADOPT,,{fluxtol},{solver},{maxiter},{toler},{overrlex},,,,,{maxfluxiter}"
        )
        return self.run(command, **kwargs)

    def spcnod(self, encl="", node="", **kwargs):
        """Defines a space node for radiation using the Radiosity method.

        APDL Command: SPCNOD

        Parameters
        ----------
        encl
            Radiating surface enclosure number.  Defaults to 1. If ENCL = STAT,
            the command lists all enclosure space nodes. If  ENCL =  DELE, the
            command deletes all enclosure space nodes.

        node
            Node defined to be the space node.

        Notes
        -----
        For open systems, an enclosure may radiate to a space node (NODE).

        Open systems may be characterized by one or more enclosures (ENCL).
        Each enclosure may radiate to a different space node (NODE).

        For a space node that is not part of the finite element model, specify
        the temperature using the D command. For the first load step, the space
        node temperature ramps from the uniform temperature specified by the
        TUNIF command to the temperature specified by the D command. For
        subsequent load steps, it ramps from the previous value of the space
        node temperature. For intermediate load steps, use the SPCNOD,DELETE
        command and specify the space node temperature again to ramp from the
        uniform temperature.

        For a space node that is part of the finite element model, the
        temperature is that calculated during the finite element solution.
        """
        command = f"SPCNOD,{encl},{node}"
        return self.run(command, **kwargs)

    def spctemp(self, encl="", temp="", **kwargs):
        """Defines a free-space ambient temperature for radiation using the

        APDL Command: SPCTEMP
        Radiosity method.

        Parameters
        ----------
        encl
            Radiating surface enclosure number. Defaults to 1. If ENCL = STAT,
            the command lists all enclosure space temperatures.  If ENCL =
            DELE, the command deletes all enclosure space temperatures.

        temp
            Temperature of free-space in the reference temperature system.  The
            temperature will be offset by the value specified in the TOFFST
            command for internal calculations.

        Notes
        -----
        For open systems, an enclosure may radiate to the free-space ambient
        temperature (TEMP).

        Open systems may be characterized by one or more enclosures (ENCL).
        Each enclosure may radiate to a different free-space ambient
        temperature  (TEMP).

        For the first load step, the space temperature ramps from the uniform
        temperature specified by the TUNIF command to the temperature specified
        by the SPCTEMP command. For subsequent load steps, it ramps from the
        previous value of the space temperature. For intermediate load steps,
        use the SPCTEMP,DELETE command and specify the space temperature again
        to ramp from the uniform temperature.

        If using SPCTEMP with the ANSYS Multi-field solver (MFS),  you must
        capture this command in the command file using MFCMMAND. This step is
        necessary because at the end of each field computation, this command is
        unset.
        """
        command = f"SPCTEMP,{encl},{temp}"
        return self.run(command, **kwargs)

    def v2dopt(self, geom="", ndiv="", hidopt="", nzone="", **kwargs):
        """Specifies 2-D/axisymmetric view factor calculation options.

        APDL Command: V2DOPT

        Parameters
        ----------
        geom
            Choice of geometry:

            0 - Planar (default).

            1 - Axisymmetric

        ndiv
            Number of divisions for axisymmetric geometry (that is, the number
            of circumferential segments). Default is 20. Maximum is 90.

        hidopt
            Viewing option:

            0 - Hidden (default).

            1 - Non-hidden

        nzone
            Number of zones (that is, the number of rays emanating from a
            surface) for view factor calculation. Default is 200. Maximum is
            1000.
        """
        command = f"V2DOPT,{geom},{ndiv},{hidopt},{nzone}"
        return self.run(command, **kwargs)

    def vfsm(self, action="", encl="", opt="", maxiter="", conv="", **kwargs):
        """Adjusts view factor matrix to satisfy reciprocity and/or
        row sum properties.

        APDL Command: VFSM

        Parameters
        ----------
        action
            Action to be performed:

            Define - Define a view factor summation (default)

            Clear - Resets the scaling method to 0 for all
                    enclosures. All subsequent arguments are ignored.

            Status - Outputs the OPT value for each enclosure in the model.

        encl
            Previously defined enclosure number for the view factor adjustment.

        opt
            Option key:

            0 - The view factor matrix values are not adjusted (default).

            1 - The view factor matrix values are adjusted so that the
                row sum equals 1.0.

            2 - The view factor matrix values are adjusted so that the
                row sum equals 1.0 and the reciprocity relationship is
                satisfied.

            3 - The view factor matrix values are adjusted so that the
                original row sum is maintained.

            4 - The view factor matrix values are adjusted so that the
                original row sum is maintained and the reciprocity
                relationship is satisfied.

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
        command = f"VFSM,{action},{encl},{opt},{maxiter},{conv}"
        return self.run(command, **kwargs)

    def vfopt(
        self,
        opt="",
        filename="",
        ext="",
        dir_="",
        filetype="",
        fileformat="",
        **kwargs,
    ):
        """Specifies options for the view factor file and calculates view factors.

        APDL Command: VFOPT

        Parameters
        ----------
        opt
            View factor option:

            NEW - Calculate view factors and write them to a file.

            OFF - Do not recalculate view factors it they already exist in the database,
                  otherwise calculate compute them. This option is the default
                  behavior.

            READ - Read view factors from a binary file. For subsequent SOLVE commands, switch to
                   the default option (OFF).

            NONE - Do not write view factors to a file.

        fname
            File name for view factor matrix. Default = Jobname.

        ext
            Filename extension for view factor matrix. Default = .vf.

        dir\_
            Directory path for view factor matrix. If you do not specify a
            directory path, it will default to your working directory.

        filetype
            View factor file type:

            BINA - Binary (default).

            ASCI - ASCII.

        fileformat
            Format for the specified Filetype:

            Binary files (Filetype = BINA): - 0

            No compression. (View factor file size may be very large.) - 1

        Notes
        -----
        The VFOPT command allows you to deactivate the view factor computation
        (Opt = OFF) if the view factors already exist in the database. The
        default behavior is OFF upon encountering the second and subsequent
        SOLVE commands in the solution processor.

        When Opt = READ, only a previously calculated view factor binary file
        is valid.

        For 3-D analyses, two options are available for calculating view
        factors when running Distributed ANSYS:

        Issue a SOLVE command -- View factors are calculated in parallel mode
        if no view factors were previously calculated.

        Issue a VFOPT,NEW command -- View factors are calculated in serial
        mode.

        For 2-D analyses, view factors are calculated in serial mode.
        """
        command = f"VFOPT,{opt},{filename},{ext},{dir_},{filetype},{fileformat}"
        return self.run(command, **kwargs)

    def vfquery(self, srcelem="", tarelem="", **kwargs):
        """Queries and prints element Hemicube view factors and average view

        APDL Command: VFQUERY
        factor.

        Parameters
        ----------
        srcelem
            Elements representing the source radiating surfaces used to query
            the view factor at the target element(s). If SRCELEM = P, graphical
            picking is enabled (valid only in the GUI). If SRCELEM = ALL, all
            selected elements will have their view factors queried. A component
            name may also be substituted for SRCELEM. Selected elements must be
            flagged for surface to surface radiation in order to query view
            factors (SF, SFA, or SFE with Lab = RDSF). The view factors must
            have been previously computed.

        tarelem
            Element for view factor query. If TARELEM = P, graphical picking is
            enabled (valid only in the GUI). If TARELEM = ALL, all selected
            elements will have their view factors queried. A component name may
            also be substituted for TARELEM. Selected elements must be flagged
            for surface to surface radiation in order to query view factors
            (SF, SFA, or SFE with Lab = RDSF). The view factors must have been
            previously computed.

        Notes
        -----
        View factors for each target element will be printed.

        An average view factor for all target elements will be computed.  (Use
        ``*GET``  to retrieve the average value).

        When resuming a database, issue the command VFOPT,READ before issuing
        the VFQUERY command.
        """
        command = f"VFQUERY,{srcelem},{tarelem}"
        return self.run(command, **kwargs)
