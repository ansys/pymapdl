"""
These DATABASE commands can be used to initialize the database, save
it to a file, or annotate it with titles and systems of units.
"""


class Setup:
    def resume(self, fname="", ext="", nopar="", knoplot="", **kwargs):
        """Resumes the database from the database file.

        APDL Command: RESUME

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

        nopar
            Parameter resume key:

            0 - All data in the database, including the scalar
                parameters, are replaced with the data saved on
                File.DB (default).

            1 - All data in the database, except the scalar
                parameters, are replaced with the data saved on
                File.DB.

        knoplot
            If equal to 1, will suppress automatic plot. Otherwise, if
            the GUI is on and this RESUME command was not read from a
            file, the selected elements from Fname are plotted. (If
            there are no selected elements, selected nodes are
            plotted. If no nodes, volumes; if no volumes, areas; if no
            areas, lines; if no lines, keypoints. If there are no
            selected keypoints, the screen is erased.)

        Notes
        -----
        The RESUME command resumes a database file into the ANSYS program. The
        command causes the database file (File.DB) to be read, thereby
        resetting the database (including any geometry settings) either a) as
        it was at the last SAVE command, or b) as it was saved with the last
        /EXIT command, whichever was last.

        For multiple load step analyses (because only the data for one load
        step at a time may reside in the database), the load step data restored
        to the database will correspond to the load step data written when the
        save occurred.

        If the database file was saved in another ANSYS, Inc. product, it may
        contain element type and KEYOPT specifications which are invalid in the
        resuming product. Immediately after the database resume is completed,
        you should redefine these invalid element types and KEYOPT settings to
        valid ones (ET, KEYOPT).

        The NOPAR = 1 option should not be used if array parameters are
        defined, as existing array parameters might be redefined with arbitrary
        values. For a more general method of preventing the replacement of both
        scalar and array parameters, see PARSAV and PARRES.)

        This command is valid in any processor.  If used in the solution
        processor, this command is valid only within the first load step.
        """
        return self.run(f"RESUME,{fname},{ext},,{nopar},{knoplot}", **kwargs)

    def save(self, fname="", ext="", slab="", **kwargs):
        """Saves all current database information.

        APDL Command: SAVE

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

        slab
            Mode for saving the database:

            ALL
              Save the model data, solution data and post data
              (element tables, etc.). This value is the default.

            MODEL
              Save the model data (solid model, finite element
              model, loadings, etc.) only.

            SOLU
              Save the model data and the solution data (nodal
              and element results).

        Notes
        -----
        Saves all current database information to a file (File.DB).
        In interactive mode, an existing File.DB is first written to a
        backup file (File.DBB).  In batch mode, an existing File.DB is
        replaced by the current database information with no backup.
        The command should be issued periodically to ensure a current
        file backup in case of a system "crash" or a "line drop."  It
        may also be issued before a "doubtful" command so that if the
        result is not what was intended the database may be easily
        restored to the previous state.  A save may be time consuming
        for large models.  Repeated use of this command overwrites the
        previous data on the file (but a backup file is first written
        during an interactive run).  When issued from within POST1,
        the nodal boundary conditions in the database (which were read
        from the results file) will overwrite the nodal boundary
        conditions existing on the database file.

        Internal nodes may be created during solution (for example,
        via the mixed u-P formulation or generalized plane strain
        option for current- technology elements, the Lagrangian
        multiplier method for contact elements or the MPC184 elements,
        or the quadratic or cubic option of the BEAM188 and PIPE288
        elements). It is sometimes necessary to save the internal
        nodes in the database for later operations, such as cutting
        boundary interpolations (CBDOF) for submodeling. To do so,
        issue the SAVE command after the first SOLVE command.

        In general, saving after solving is always a good practice.

        This command is valid in any processor.
        """
        return self.run(f"SAVE,{fname},{ext},,{slab}", **kwargs)

    def smbc(self, mode="", **kwargs):
        """Controls the display of solid model boundary condition symbols and

        APDL Command: /SMBC
        labels.

        Parameters
        ----------
        mode
            CENT
              Solid model boundary condition symbols and labels appear at the centroid of the
              solid model entity (default).

            TESS
              Solid model boundary condition symbols and labels appear inside each
              constituent element of the tessellation.

        Notes
        -----
        Mode = CENT is designed to reduce the clutter of boundary condition
        symbols in solid model plots. For example, if you have assigned normal
        pressure loads to an area, you may choose to display the pressures as
        arrows with the /PSF command using /PSF,PRES,NORM,2. When Mode = CENT,
        the pressure arrow is displayed at the centroid of the area. When Mode
        = TESS, a pressure arrow is displayed at the centroid of each polygon
        of the area's tessellation.

        This command is valid in any processor.
        """
        command = "/SMBC,%s" % (str(mode))
        return self.run(command, **kwargs)

    def stat(self, **kwargs):
        """Displays the status of database settings.

        APDL Command: STAT

        Notes
        -----
        In the DISPLAY program, STAT will show the current status of the
        program settings.

        In the ANSYS program, STAT is a command generated by the GUI and will
        appear in the log file (Jobname.LOG) if status is requested for some
        items under Utility Menu> List> Status.  Generally, STAT will be
        preceded by one of the commands listed below, which specifies the
        particular topic that status was requested for.

        If entered directly into the program, the STAT command should be
        immediately preceded by the desired topic command listed below.  In
        processors other than those listed below (e.g., AUX12), no topic
        command should proceed STAT.

        This command is valid in any processor.

        PREP7 topic commands (and their corresponding topics) are:

        SOLUTION topic commands (and their corresponding topics) are:

        POST1 topic commands (and their corresponding topics) are:

        POST26 topic commands (and their corresponding topics) are:
        """
        command = "STAT,"
        return self.run(command, **kwargs)

    def stitle(self, nline="", title="", **kwargs):
        """Defines subtitles.

        APDL Command: /STITLE

        Parameters
        ----------
        nline
            Subtitle line number (1 to 4).  Defaults to 1.

        title
            Input up to 70 alphanumeric characters.  Parameter substitution may
            be forced within the title by enclosing the parameter name or
            parametric expression within percent (%) signs.  If Title is blank,
            this subtitle is deleted.

        Notes
        -----
        Subtitles (4 maximum) are displayed in the output along with the main
        title [/TITLE].  Subtitles do not appear in GUI windows or in ANSYS
        plot displays.  The first subtitle is also written to various ANSYS
        files along with the main title.  Previous subtitles may be overwritten
        or deleted.  Issue /STATUS to display titles.

        This command is valid in any processor.
        """
        command = "/STITLE,%s,%s" % (str(nline), str(title))
        return self.run(command, **kwargs)

    def title(self, title="", **kwargs):
        """Defines a main title.

        APDL Command: /TITLE

        Parameters
        ----------
        title str
            Input up to 72 alphanumeric characters.  Parameter substitution may
            be forced within the title by enclosing the parameter name or
            parametric expression within percent (%) signs.

        Notes
        -----
        The title is carried through the printout and written on various files.
        The title written to a file is the title defined at that time.  Special
        characters may be used within the title text.  Subtitles may also be
        defined [/STITLE].

        This command is valid in any processor.
        """
        return self.run(f"/TITLE,{title}", **kwargs)

    def units(
        self,
        label="",
        lenfact="",
        massfact="",
        timefact="",
        tempfact="",
        toffset="",
        chargefact="",
        forcefact="",
        heatfact="",
        **kwargs,
    ):
        """Annotates the database with the system of units used.

        APDL Command: /UNITS

        Parameters
        ----------
        label
            Label to denote the system of units used in this job:

            USER - User-defined system (default).

            SI - International system (m, kg, s, K).

            MKS - MKS system (m, kg, s, °C).

            uMKS - μMKS system (μm, kg, s, °C).

            CGS - CGS system (cm, g, s, °C).

            MPA - MPA system (mm, Mg, s, °C).

            BFT - U. S. Customary system using feet (ft, slug, s, °F).

            BIN - U. S. Customary system using inches (in, lbf*s2/in, s, °F).

        Notes
        -----
        Allows the user to set a marker in the database indicating the system
        of units used.  The setting may be reviewed with the /STATUS command at
        the Begin level.  The units label and conversion factors on this
        command are for user convenience only and have no effect on the
        analysis or data.  That is, /UNITS will not convert database items from
        one system to another (e.g., from U. S. Customary to SI, etc.).  The
        units setting will be written to the file of IGES data [IGESOUT or
        CDWRITE], which can then be read by many programs that read IGES files.
        The user must still use consistent units for the results to be valid.

        If you choose the MKS system of units, the EPZRO option for the EMUNIT
        command is set to 8.85 e-12 F/m.  (EPZRO specifies alternate free-space
        permittivity.)

        For micro-electromechanical systems (MEMS), where dimensions are on the
        order of microns, see the conversion factors in System of Units in the
        Coupled-Field Analysis Guide.

        If you use the ANSYS ADAMS Interface to export model information to the
        ADAMS program, the /UNITS command is required to ensure the correct
        transfer of data between ANSYS and ADAMS. You may choose a predefined
        unit system label (Label = SI, CGS, etc.) or you can select the user-
        defined system option (Label = USER) and input the appropriate
        conversion factors (LENFACT, MASSFACT, TIMEFACT, and FORCEFACT). The
        conversion factors will be written to the ADAMS input file Jobname.MNF
        in order to correctly generate the load. For more information, see
        Export to ADAMS in the Substructuring Analysis Guide.

        All differences between the base solution units used by the ANSYS and
        CFX solvers will be noted in the ANSYS output file.   Unit conversions
        are automatically applied to all loads transferred unless Label = USER.
        Unit conversions are not applied to any of the loads transferred
        between the ANSYS and CFX solvers if they use a user-defined unit
        system.

        This command is valid in any processor.
        """
        command = "/UNITS,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (
            str(label),
            str(lenfact),
            str(massfact),
            str(timefact),
            str(tempfact),
            str(toffset),
            str(chargefact),
            str(forcefact),
            str(heatfact),
        )
        return self.run(command, **kwargs)
