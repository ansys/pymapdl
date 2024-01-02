class MultiFieldConvergenceControls:
    def mfconv(self, lab="", toler="", minref="", **kwargs):
        """Sets convergence values for an ANSYS Multi-field solver analysis.

        APDL Command: MFCONV

        Parameters
        ----------
        lab
            Valid labels:

        toler
            Convergence tolerance about program calculated reference value (the
            L2 norm of the new load in a multi-field analysis). Defaults to
            0.01 (1%) for all labels. Must be less than 1.0.

        minref
            The minimum value allowed for the program calculated reference
            value. If negative, no minimum is enforced. Defaults to 1.0e-6 for
            all labels. Not available in the GUI. MINREF corresponds to
            ||ϕnew|| as defined in Set up Stagger Solution in the Coupled-Field
            Analysis Guide.

        Notes
        -----
        MFCONV sets convergence values for variables at the ANSYS
        Multi-field solver interface.

        This command is also valid in PREP7.

        See Multi-field Commands in the Coupled-Field Analysis Guide
        for a list of all ANSYS Multi-field solver commands and their
        availability for MFS and MFX analyses.

        Distributed ANSYS Restriction: This command is not supported
        in Distributed ANSYS.
        """
        return self.run(f"MFCONV,{lab},{toler},,{minref}", **kwargs)

    def mfiter(self, maxiter="", miniter="", target="", **kwargs):
        """Sets the number of stagger iterations for an ANSYS Multi-field solver

        APDL Command: MFITER
        analysis.

        Parameters
        ----------
        maxiter
            Maximum number of iterations. Defaults to 10.

        miniter
            Minimum number of iterations. Defaults to 1.

        target
            Target number of iterations. Defaults to 5.

        Notes
        -----
        The number of stagger iterations applies to each time step in an ANSYS
        Multi-field solver analysis. MINITER and TARGET are valid only when
        multi-field auto time stepping is on (MFDTIME).

        This command is also valid in PREP7.

        See Multi-field Commands in the Coupled-Field Analysis Guide for a list
        of all ANSYS Multi-field solver commands and their availability for MFS
        and MFX analyses.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"MFITER,{maxiter},{miniter},{target}"
        return self.run(command, **kwargs)

    def mfrelax(self, lab="", value="", option="", **kwargs):
        """Sets relaxation values for an ANSYS Multi-field solver analysis.

        APDL Command: MFRELAX

        Parameters
        ----------
        lab
            Valid labels:

        value
            Relaxation value. Defaults to 0.75 for all labels.

        option
            Valid options are:

            RELX  - Uses relaxation method for load transfer (default).

            LINT  - Uses a linear interpolation for loaf transfer.

        Notes
        -----
        MFRELAX sets relaxation values for the load transfer variables at a
        surface or volume interface. Option = RELX will usually give you a more
        stable and smooth load transfer and is suitable for strongly coupled
        problems (such as FSI problems). Option = LINT is suitable for weakly
        coupled problems because it will transfer the full load in fewer
        stagger iterations.

        See the MFFR and MFITER commands for more information on relaxation in
        the ANSYS Multi-field solver.

        This command is also valid in PREP7.

        See Multi-field Commands in the Coupled-Field Analysis Guide for a list
        of all ANSYS Multi-field solver commands and their availability for MFS
        and MFX analyses.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"MFRELAX,{lab},{value},{option}"
        return self.run(command, **kwargs)
