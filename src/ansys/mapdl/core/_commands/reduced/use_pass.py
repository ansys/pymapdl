class UsePass:
    def dcvswp(
        self,
        option="",
        elem="",
        cnum="",
        vmax="",
        vinc1="",
        vinc2="",
        gap="",
        **kwargs,
    ):
        """Performs a DC voltage sweep on a ROM element.

        APDL Command: DCVSWP

        Parameters
        ----------
        option
            Sweep option:

            GV - Perform voltage sweep up to given voltage Vmax.

        elem
            Element number of the ROM element for the ROM use pass analysis.

        cnum
            Number of sweep conductor.

        vmax
            Maximum voltage. For the PI option, this voltage should be below
            the pull-in voltage value.

        vinc1
            Voltage increment for Vmax (default = Vmax/20).

        vinc2
            Voltage increment for pull-in voltage (default = 1).

        gap
            Gap elements option:

            0 - Create gap elements (COMBIN40) (default).

        Notes
        -----
        Vinc1 is used to ramp the sweep conductor voltage from 0 to Vmax. Vinc2
        is used to increase the sweep conductor voltage from Vmax to the pull-
        in value if the PI sweep option is used.

        Because ramping the voltage may lead to the unstable region of an
        electromechanical system, DCVSWP might not converge when the sweep
        conductor voltage approaches the pull-in value. To avoid non-converged
        solutions, you should use the gap option to create a set of spring-gap
        elements (COMBIN40). By default, DCVSWP creates two spring-gap elements
        with opposite orientations for each active modal displacement DOF of
        the ROM element. The gap size is set to the maximum absolute values of
        the deflection range for the corresponding mode, as calculated by
        RMMSELECT or modified  using the RMMRANGE command. The spring constants
        are set to 1.E5 for all the COMBIN40 elements. Along with the spring-
        gap elements, DCVSWP creates a set of constraint equations relating the
        ROM element modal displacements DOF (EMF) and the displacement DOF (UX)
        of the gap elements. Constraining the modal displacements using the
        spring-gap elements allows DCVSWP to converge in the pull-in range. The
        DCVSWP macro has a limit of 900 equilibrium iterations. If this limit
        is not sufficient to reach convergence, try the advanced techniques
        given in Overcoming Convergence Problems in the Structural Analysis
        Guide. For more information on gap elements, see Using Gap Elements
        with ROM144 in the Coupled-Field Analysis Guide.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"DCVSWP,{option},{elem},{cnum},{vmax},{vinc1},{vinc2},{gap}"
        return self.run(command, **kwargs)

    def rmlvscale(
        self,
        nload="",
        fact1="",
        fact2="",
        fact3="",
        fact4="",
        fact5="",
        **kwargs,
    ):
        """Defines element load vector scaling for a ROM use pass.

        APDL Command: RMLVSCALE

        Parameters
        ----------
        nload
            Total number of load cases to be considered within a ROM use pass.
            If Nload = "DELETE", all defined load vectors are deleted.

        fact1, fact2, fact3, . . . , fact5
            Scale factors applied to load vectors (maximum 5). Defaults to 0.

        Notes
        -----
        Specifies the element load scale factor applied to a ROM analysis use
        pass.  Element load vectors are extracted from a Static Analysis using
        the RMNDISP command. Up to 5 element load vectors may be scaled and
        applied to a ROM use pass.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"RMLVSCALE,{nload},{fact1},{fact2},{fact3},{fact4},{fact5}"
        return self.run(command, **kwargs)

    def rmuse(self, option="", usefil="", **kwargs):
        """Activates ROM use pass for ROM elements.

        APDL Command: RMUSE

        Parameters
        ----------
        option
            Type of data to be plotted. Valid types are:

            1 or "ON" - Activates ROM use pass.

        usefil
            Name of the reduced displacement file (.rdsp) created by the ROM
            Use Pass (required field only for the Expansion Pass).

        Notes
        -----
        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"RMUSE,{option},{usefil}"
        return self.run(command, **kwargs)
