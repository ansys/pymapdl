class Listing:
    def format(
        self,
        ndigit="",
        ftype="",
        nwidth="",
        dsignf="",
        line="",
        char="",
        **kwargs,
    ):
        """Specifies format controls for tables.

        APDL Command: /FORMAT

        Parameters
        ----------
        ndigit
            Number of digits (3 to 32) in first table column (usually the node
            or element number).  Initially defaults to 7.

        ftype
            FORTRAN format types (initially defaults to G):

            G - Gxx.yy.  xx and yy are described below.

            F - Fxx.yy

            E - Exx.yy

        nwidth
            Total width (9 to 32) of the field (the xx in Ftype).  Initially
            defaults to 12.

        dsignf
            Number of digits after the decimal point (yy in F or E format) or
            number of significant digits in G format.  Range is 2 to xx-7 for
            Ftype = G or E; and 0 to xx-4 for Ftype = F.  Initially defaults to
            5.

        line
            Number of lines (11 minimum) per page.  Defaults to ILINE or BLINE
            from the /PAGE command.

        char
            Number of characters (41 to 240, system-dependent) per line before
            wraparound.  Defaults to ICHAR or BCHAR from the /PAGE command.

        Notes
        -----
        Specifies various format controls for tables printed with the POST1
        PRNSOL, PRESOL, PRETAB, PRRSOL, PRPATH, and CYCCALC commands.  A blank
        (or out-of-range) field on the command retains the current setting.
        Issue /FORMAT,STAT to display the current settings.  Issue /FORMAT,DEFA
        to reestablish the initial default specifications.

        For the POST26 PRVAR command, the Ftype, NWIDTH, and DSIGNF fields
        control the time output format.

        This command is valid in any processor.
        """
        command = f"/FORMAT,{ndigit},{ftype},{nwidth},{dsignf},{line},{char}"
        return self.run(command, **kwargs)

    def header(
        self,
        header="",
        stitle="",
        idstmp="",
        notes="",
        colhed="",
        minmax="",
        **kwargs,
    ):
        """Sets page and table heading print controls.

        APDL Command: /HEADER

        Parameters
        ----------
        header
            ANSYS page header (system, date, time, version, copyright, title,
            etc.):

            ON - Turns this item on (default for batch mode; not available for interactive
                 mode).

            OFF - Turns this item off.

            (blank) - Retains the previous setting.

        stitle
            Subtitles (see /STITLE command):   ON, OFF, or (blank) (see above).

        idstmp
            Load step information (step number, substep number, time value):
            ON, OFF, or (blank) (see above).

        notes
            Information relative to particular table listings:   ON, OFF, or
            (blank) (see above).

        colhed
            Column header labels of table listings (currently only for single
            column tables):   ON, OFF, or (blank) (see above).

        minmax
            Minimum/maximum information or totals after table listings:   ON,
            OFF, or (blank) (see above).

        Notes
        -----
        Sets specifications on or off for page and table heading print controls
        associated with the POST1 PRNSOL, PRESOL, PRETAB, PRRSOL, and PRPATH
        commands.

        Note:: : If the printout caused a  top-of-form (page eject to top of
        next page), the top-of-form is also suppressed with the printout.
        Issue /HEADER,STAT to display the current settings.  Issue /HEADER,DEFA
        to reset the default specifications.

        This command is valid in any processor.
        """
        command = f"/HEADER,{header},{stitle},{idstmp},{notes},{colhed},{minmax}"
        return self.run(command, **kwargs)

    def irlist(self, **kwargs):
        """Prints inertia relief summary table.

        APDL Command: IRLIST

        Notes
        -----
        Prints the inertia relief summary data, including the mass summary
        table, the total load summary table, and the inertia relief summary
        table resulting from the inertia relief calculations. These
        calculations are performed in the solution phase [SOLVE] as specified
        by the IRLF command.

        Inertia relief output is stored in the database rather than in the
        results file (Jobname.RST). When you issue IRLIST, ANSYS pulls the
        information from the database, which contains the inertia relief output
        from the most recent solution [SOLVE].

        This command is valid in any processor.
        """
        command = f"IRLIST,"
        return self.run(command, **kwargs)

    def page(self, iline="", ichar="", bline="", bchar="", comma="", **kwargs):
        """Defines the printout and screen page size.

        APDL Command: /PAGE

        Parameters
        ----------
        iline
            Number of lines (11 minimum) per "page" or screen.  Defaults to 24.
            Applies to interactive non-GUI to the screen output only.

        ichar
            Number of characters (41 to 132) per line before wraparound.
            Defaults to 80.  Applies to interactive non-GUI to the screen
            output only.

        bline
            Number of lines (11 minimum) per page.  Defaults to 56.  Applies to
            batch mode [/BATCH], diverted [/OUTPUT], or interactive GUI [/MENU]
            output. If negative, no page headers are output.

        bchar
            Number of characters (41 to 240 (system dependent)) per line before
            wraparound.  Defaults to 132.  Applies to batch mode [/BATCH],
            diverted [/OUTPUT], or interactive GUI [/MENU] output.

        comma
            Input 1 to specify comma-separated output for node [NLIST] and
            element [ELIST] output.

        Notes
        -----
        Defines the printout page size for batch runs and the screen page size
        for interactive runs.  Applies to the POST1 PRNSOL, PRESOL, PRETAB,
        PRRSOL, and PRPATH commands.  See the /HEADER command for additional
        controls (page ejects, headers, etc.) that affect the amount of
        printout.  A blank (or out-of-range) value retains the previous
        setting.  Issue /PAGE,STAT to display the current settings.  Issue
        /PAGE,DEFA to reset the default specifications.

        This command is valid in any processor.
        """
        command = f"/PAGE,{iline},{ichar},{bline},{bchar},{comma}"
        return self.run(command, **kwargs)

    def prerr(self, **kwargs):
        """Prints SEPC and TEPC.

        APDL Command: PRERR

        Notes
        -----
        Prints the percent error in structural energy norm (SEPC) and the
        thermal energy norm percent error (TEPC).  Approximations of mesh
        discretization error associated with a solution are calculated for
        analyses having structural or thermal degrees of freedom.

        The structural approximation is based on the energy error (which is
        similar in concept to the strain energy) and represents the error
        associated with the discrepancy between the calculated stress field and
        the globally continuous stress field (see POST1 - Error Approximation
        Technique in the Mechanical APDL Theory Reference).  This discrepancy
        is due to the assumption in the elements that only the displacements
        are continuous at the nodes.  The stress field is calculated from the
        displacements and should also be continuous, but generally is not.

        Thermal analyses may use any solid and shell thermal element having
        only temperature degrees of freedom.  The thermal approximation is
        based on the total heat flow dissipation and represents the error
        associated with the discrepancy between the calculated nodal thermal
        flux within an element and a continuous global thermal flux.  This
        continuous thermal flux is calculated with the normal nodal averaging
        procedure.

        The volume (result label VOLU) is used to calculate the energy error
        per element (result label SERR for the structural energy error and TERR
        for the thermal energy error).  These energy errors, along with the
        appropriate energy, are then used to calculate the percent error in
        energy norm (SEPC for structural and TEPC for thermal). These
        percentages can be listed by the PRERR command, retrieved by the ``*GET``
        command (with labels SEPC and TEPC) for further calculations, and shown
        on the displacement display (PLDISP), as applicable.

        For structural analyses, the maximum absolute value of nodal stress
        variation of any stress component for any node of an element (result
        item SDSG) is also calculated.  Similarly, for thermal gradient
        components, TDSG is calculated.  Minimum and maximum result bounds
        considering the possible effect of discretization error will be shown
        on contour displays (PLNSOL).  For shell elements, the top surface
        location is used to produce a meaningful percentage value.  SERR, TERR,
        SEPC, TEPC, SDSG, and TDSG will be updated whenever the nodal stresses
        or fluxes are recalculated.

        If the energy error is a significant portion of the total energy, then
        the analysis should be repeated using a finer mesh to obtain a more
        accurate solution.  The energy error is relative from problem to
        problem but will converge to a zero energy error as the mesh is
        refined.  An automated adaptive meshing procedure using this energy
        error is described with the ADAPT macro.

        The following element- and material-type limitations apply:

        Valid with most 2-D solid, 3-D solid, axisymmetric solid, or 3-D shell
        elements.

        The following element types are not valid: SHELL28, SHELL41, and
        SOLID65.

        The model should have only structural or thermal degrees of freedom.

        The analysis must be linear (for both material and geometry).

        Multi-material (for example, composite) elements are not valid.

        Transition regions from one material to another are not valid (that is,
        the entire model should consist of one material).

        Anisotropic materials (TB,ANEL) are not considered.
        """
        command = f"PRERR,"
        return self.run(command, **kwargs)

    def priter(self, **kwargs):
        """Prints solution summary data.

        APDL Command: PRITER

        Notes
        -----
        Prints solution summary data (such as time step size, number of
        equilibrium iterations, convergence values, etc.) from a static or full
        transient analysis. All other analyses print zeros for the data.
        """
        command = f"PRITER,"
        return self.run(command, **kwargs)
