class MagneticsCalc:
    def curr2d(self, **kwargs):
        """Calculates current flow in a 2-D conductor.

        APDL Command: CURR2D

        Notes
        -----
        CURR2D invokes an ANSYS macro which calculates the total current
        flowing in a conducting body for a 2-D planar or axisymmetric magnetic
        field analysis.  The currents may be applied source currents or induced
        currents (eddy currents).  The elements of the conducting region must
        be selected before this command is issued.  The total current
        calculated by the macro is stored in the parameter TCURR.  Also, the
        total current and total current density are stored on a per-element
        basis in the element table [ETABLE] with the labels TCURR and JT,
        respectively.  Use the PLETAB and PRETAB commands to plot and list the
        element table items.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"CURR2D,"
        return self.run(command, **kwargs)

    def emagerr(self, **kwargs):
        """Calculates the relative error in an electrostatic or electromagnetic

        APDL Command: EMAGERR
        field analysis.

        Notes
        -----
        The relative error is an approximation of the mesh discretization error
        associated with a solution. It is based on the discrepancy between the
        unaveraged, element-nodal field values and the averaged, nodal field
        values. The calculation is valid within a material boundary and does
        not consider the error in continuity of fields across dissimilar
        materials.

        For electrostatics, the field values evaluated are the electric field
        strength (EFSUM) and the electric flux density (DSUM). A relative error
        norm of each is calculated on a per-element basis and stored in the
        element table [ETABLE] with the labels EF_ERR and D_ERR. Normalized
        error values EFN_ERR and DN_ERR are also calculated and stored in the
        element table. Corresponding quantities for electromagnetics are H_ERR,
        B_ERR, HN_ERR, and BN_ERR, which are calculated from the magnetic field
        intensity (HSUM) and the magnetic flux density (BSUM).  The normalized
        error value is the relative error norm value divided by the peak
        element-nodal field value for the currently selected elements.

        Use the PLETAB and PRETAB commands to plot and list the error norms and
        normalized error values.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"EMAGERR,"
        return self.run(command, **kwargs)

    def emf(self, **kwargs):
        """Calculates the electromotive force (emf), or voltage drop along a

        APDL Command: EMF
        predefined path.

        Notes
        -----
        EMF invokes an ANSYS macro which calculates the electromotive force
        (emf), or voltage drop along a predefined path (specified with the PATH
        command). It is valid for both 2-D and 3-D electric field analysis or
        high-frequency electromagnetic field analysis. The calculated emf value
        is stored in the parameter EMF.

        You must define a line path (via the PATH command) before issuing the
        EMF command macro. The macro uses calculated values of the electric
        field (EF), and uses path operations for the calculations. All path
        items are cleared when the macro finishes executing.

        The EMF macro sets the "ACCURATE" mapping method and "MAT"
        discontinuity option on the PMAP command. The ANSYS program retains
        these settings after executing the macro.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"EMF,"
        return self.run(command, **kwargs)

    def emft(self, **kwargs):
        """Summarizes electromagnetic forces and torques.

        APDL Command: EMFT

        Notes
        -----
        Use this command to summarize electromagnetic force and torque in both
        static electric and magnetic problems. To use this command, select the
        nodes in the region of interest and make sure that all elements are
        selected. If RSYS = 0, the force is reported in the global Cartesian
        coordinate system. If RSYS ≠ 0, force is reported in the specified
        coordinate system. However, for torque, if RSYS ≠ 0, this command will
        account for the shift and rotation as specified by RSYS, but will
        report only the Cartesian components.

        Forces are stored as items _FXSUM, _FYSUM, _FZSUM, and _FSSUM. Torque
        is stored as items _TXSUM, _TYSUM, _TZSUM, and _TSSUM.

        This command is valid only with PLANE121, SOLID122, SOLID123, PLANE233,
        SOLID236 and SOLID237 elements. For any other elements, you must use
        FMAGSUM.
        """
        command = f"EMFT,"
        return self.run(command, **kwargs)

    def fluxv(self, **kwargs):
        """Calculates the flux passing through a closed contour.

        APDL Command: FLUXV

        Notes
        -----
        FLUXV invokes an ANSYS macro which calculates the flux passing through
        a closed contour (path) predefined by PATH.  The calculated flux is
        stored in the parameter FLUX.  In a 2-D analysis, at least two nodes
        must be defined on the path.  In 3-D, a path of nodes describing a
        closed contour must be specified (i.e., the first and last node in the
        path specification must be the same).  A counterclockwise ordering of
        nodes on the PPATH command will give the correct sign on flux.  Path
        operations are used for the calculations, and all path items are
        cleared upon completion.  This macro is only available for vector
        potential formulations.
        """
        command = f"FLUXV,"
        return self.run(command, **kwargs)

    def mmf(self, **kwargs):
        """Calculates the magnetomotive force along a path.

        APDL Command: MMF

        Notes
        -----
        MMF invokes an ANSYS macro which calculates the magnetomotive force
        (mmf) along a predefined path [PATH].  It  is valid for both 2-D and
        3-D magnetic field analyses.  The calculated mmf value is stored in the
        parameter MMF.

        A closed path [PATH], passing through the magnetic circuit for which
        mmf is to be calculated, must be defined before this command is issued.
        A counterclockwise ordering of points on the PPATH command will yield
        the correct sign on the mmf.  The mmf is based on Ampere's Law.  The
        macro makes use of calculated values of field intensity (H), and uses
        path operations for the calculations.  All path items are cleared upon
        completion.  The MMF macro sets the "ACCURATE" mapping method and "MAT"
        discontinuity option of the PMAP command.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"MMF,"
        return self.run(command, **kwargs)

    def plf2d(self, ncont="", olay="", anum="", win="", **kwargs):
        """Generates a contour line plot of equipotentials.

        APDL Command: PLF2D

        Parameters
        ----------
        ncont
            Number of contour lines to display.  Issue in multiples of 9 (i.e.,
            9, 18, 27, etc.).  Default is 27 contour lines.

        olay
            Overlay:

            0 - Overlay edge outlines by material number.

            1 - Overlay edge outlines by real constant number.

        anum
            Highest material or real constant attribute number.  Command will
            cycle through ANUM element display overlays.  Defaults to 10.

        win
            Window number to which command applies.  Defaults to 1.

        Notes
        -----
        PLF2D invokes an ANSYS macro which plots equipotentials of the degree
        of freedom AZ.  These equipotential lines are parallel to flux lines
        and thus give a good representation of flux patterns.  In the
        axisymmetric case, the display is actually ``r*AZ`` where "r" is the node
        radius.  The macro overlays (OLAY) edge outlines by material number or
        real constant number (ANUM) and allows user control over the number of
        contour lines to display (NCONT).

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"PLF2D,{ncont},{olay},{anum},{win}"
        return self.run(command, **kwargs)

    def powerh(self, **kwargs):
        """Calculates the rms power loss in a conductor or lossy dielectric.

        APDL Command: POWERH

        Notes
        -----
        POWERH invokes an ANSYS macro which calculates the time-averaged (rms)
        power loss in a conductor or lossy dielectric material from a harmonic
        analysis.  The power loss is stored in the parameter PAVG.  Conductor
        losses include solid conductors and surface conductors approximated by
        impedance or shielding boundary conditions. The power loss density for
        solid conductors or dielectrics is stored in the element table with the
        label PLOSSD and may be listed [PRETAB] or displayed [PLETAB].  PLOSSD
        does not include surface losses. The elements of the conducting region
        must be selected before this command is issued.  POWERH is valid for
        2-D and 3-D analyses.
        """
        command = f"POWERH,"
        return self.run(command, **kwargs)

    def senergy(self, opt="", antype="", **kwargs):
        """Determines the stored magnetic energy or co-energy.

        APDL Command: SENERGY

        Parameters
        ----------
        opt
            Item to be calculated:

            0 - Stored magnetic energy.

            1 - Stored magnetic co-energy.

        antype
            Analysis type:

            0 - Static or transient.

            1 - Harmonic.

        Notes
        -----
        SENERGY invokes an ANSYS macro which calculates the stored magnetic
        energy or co-energy for all selected elements.  (For a harmonic
        analysis, the macro calculates a time-averaged (rms) stored energy.)  A
        summary table listing the energy by material number is produced.  The
        energy density is also calculated and stored on a per-element basis in
        the element table [ETABLE] with the label MG_ENG (energy density) or
        MG_COENG (co-energy density).  The macro erases all other items in the
        element table [ETABLE] and only retains the energy density or co-energy
        density.  Use the PLETAB and PRETAB commands to plot and list the
        energy density.  The macro is valid for static and low-frequency
        magnetic field formulations.  The macro will not calculate stored
        energy and co-energy for the following cases:

        Orthotropic nonlinear permanent magnets.

        Orthotropic nonlinear permeable materials.

        Temperature dependent materials.

        SENERGY is restricted to MKSA units.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"SENERGY,{opt},{antype}"
        return self.run(command, **kwargs)
