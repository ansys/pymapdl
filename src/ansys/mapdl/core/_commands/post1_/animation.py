class Animation:
    def ancntr(self, nfram="", delay="", ncycl="", **kwargs):
        """Produces an animated sequence of a contoured deformed shape.

        APDL Command: ANCNTR

        Parameters
        ----------
        nfram
            Number of frames captures (defaults to 5).

        delay
            Time delay during animation (defaults to 0.1 seconds).

        ncycl
            Number of animation cycles (defaults to 5).  Available in non-UI
            mode only.

        Notes
        -----
        ANCNTR involves an ANSYS macro which produces an animation of a
        contoured deformed shape of the last plot action command.  This command
        operates only on graphic display platforms supporting the /SEG command.
        After executing ANCNTR, you can replay the animated sequence by issuing
        the ANIM command.

        The command functions only in the postprocessor.
        """
        command = f"ANCNTR,{nfram},{delay},{ncycl}"
        return self.run(command, **kwargs)

    def ancut(
        self,
        nfram="",
        delay="",
        ncycl="",
        qoff="",
        ktop="",
        topoff="",
        node1="",
        node2="",
        node3="",
        **kwargs,
    ):
        """Produces an animated sequence of Q-slices.

        APDL Command: ANCUT

        Parameters
        ----------
        nfram
            Number of frames captures (defaults to 5).

        delay
            Time delay during animation (defaults to 0.1 seconds).

        ncycl
            Number of animation cycles (defaults to 5).  Available in non-UI
            mode only.

        qoff
            Q-slice working plane increment (defaults to .1 half screens).

        ktop
            Topological effect on or off (YES or NO; default is NO).

        topoff
            Topological offset (default is .1 half screens).

        node1
            Node 1 for start of the Q-slice.

        node2
            Node 2 for direction of the Q-slice.

        node3
            Node 3 for plane of the Q-slice.

        Notes
        -----
        ANCUT involves an ANSYS macro which produces an animation of Q-slices
        of the last plot action command.  This command operates only on graphic
        display platforms supporting the /SEG command.  After executing ANCUT,
        you can replay the animated sequence by issuing the ANIM command.

        The command functions only in the postprocessor.
        """
        command = f"ANCUT,{nfram},{delay},{ncycl},{qoff},{ktop},{topoff},{node1},{node2},{node3}"
        return self.run(command, **kwargs)

    def andata(
        self,
        delay="",
        ncycl="",
        rsltdat="",
        min_="",
        max_="",
        incr="",
        frclst="",
        autocont="",
        autocntr="",
        **kwargs,
    ):
        """Displays animated graphics data for nonlinear problems.

        APDL Command: ANDATA

        Parameters
        ----------
        delay
            Time delay during animation (defaults to 0.5 seconds).

        ncycl
            Number of animation cycles (defaults to 5).  Available in non-UI
            mode only.

        rsltdat
            The type of results data to be used for the animation sequence.
            This can be:

            0 - Current load step data (default).

            1 - Range of load step data.

            2 - Range of results data.

        min\_
            The range minimum value.  If left blank or 0, defaults to the first
            data point.

        max\_
            The range maximum value.  If left blank or 0, defaults to the last
            data point.

        incr
            The increment between result data (defaults to 1).

        frclst
            Key to force the last sub step in a selected load step to be
            included in the animation (defaults to 0).

        autocont
            A value of 1 enables automatic scaling of contour values based on
            the overall subset range of values. The default value is 0 (no
            automatic scaling).

        autocntr
            A value of 1 disables automatic centering of displaced plots. The
            default value is 0 (allow automatic centering).

        Notes
        -----
        Use the ANDATA command to create animations for nonlinear problems. The
        command works by displaying an individual graphical image for each
        result data set from the results file. For information about creating
        animations for linear problems, see the ANIM command.

        The command operates only on graphic display platforms supporting the
        /SEG command. It uses a macro to produce an animation based on the last
        plot action command (for example, PLDISP).

        The results file must have more than one set of results.

        The command implicitly issues /DSCALE, 1 for default displacement
        scaling. Large displacements may not give good results.

        This command functions only in the postprocessor.
        """
        command = f"ANDATA,{delay},{ncycl},{rsltdat},{min_},{max_},{incr},{frclst},{autocont},,{autocntr}"
        return self.run(command, **kwargs)

    def andscl(self, nfram="", delay="", ncycl="", **kwargs):
        """Produces an animated sequence of a deformed shape.

        APDL Command: ANDSCL

        Parameters
        ----------
        nfram
            Number of frames captured (defaults to 5).

        delay
            Time delay during animation (defaults to 0.1 seconds).

        ncycl
            Number of animation cycles (defaults to 5).  Available in non-UI
            mode only.

        Notes
        -----
        ANDSCL involves an ANSYS macro which produces an animation of
        displacement of the last plot action command (for example, PLDISP).
        This command operates only on graphic display platforms supporting the
        /SEG command.  After executing ANDSCL, you can replay the animated
        sequence by issuing the ANIM command.

        The command functions only in the postprocessor.
        """
        command = f"ANDSCL,{nfram},{delay},{ncycl}"
        return self.run(command, **kwargs)

    def ancyc(self, numframes="", kcycl="", delay="", **kwargs):
        """Applies a traveling wave animation to graphics data in a modal cyclic

        APDL Command: ANCYC
        symmetry analysis.

        Parameters
        ----------
        numframes
            The number of plot frames for the animation. Valid values range
            from 5 through 36. The default is 18. A low value (because it
            specifies fewer graphical frames) produces a rougher animation but
            loads faster. A high value produces a smoother animation but
            requires more time to load.

        kcycl
            The animation mode:

            0 - Continuous animation cycle (forward-reverse-forward).

            1 - Discontinuous animation cycle (forward-reset-forward). This option is the
                default.

        delay
            The time delay (in seconds) between animation frames. Valid values
            range from 0.1 through 1.0. The default is 0.1 seconds, which
            produces a seemingly real-time animation. A higher value produces a
            slower animation.

        Notes
        -----
        The ANCYC command is valid in a modal cyclic symmetry analysis only.

        The command animates the cyclic symmetry mode shape plot in the General
        Post Processor (/POST1). When you issue a nodal- or element-results
        plot command (for example, PLNSOL, PLESOL, or PLDISP) and then issue
        the ANCYC command, ANSYS applies a traveling wave animation to the mode
        shape plot.

        Each frame of the animation is created by expanding the cyclic symmetry
        mode shape at increasing phase angles (via the /CYCEXPAND command)
        starting at zero in equal increments over 360°. The phase-angle
        increment is 360 / NUMFRAMES.

        The animation display shows the traveling wave of the result quantity
        being plotted. The traveling wave animation is applicable only to nodal
        diameters (harmonic indices) greater than 0 and less than N / 2 (where
        N is the number of cyclic sectors in the model).

        For more information, see Applying a Traveling Wave Animation to the
        Cyclic Model in the Cyclic Symmetry Analysis Guide.
        """
        command = f"ANCYC,{numframes},{kcycl},{delay}"
        return self.run(command, **kwargs)

    def andyna(
        self,
        delay="",
        ncycl="",
        start="",
        end="",
        inc="",
        autocontourkey="",
        **kwargs,
    ):
        """Produces an animated sequence of contour values through substeps.

        APDL Command: ANDYNA

        Parameters
        ----------
        delay
            Time delay during animation (defaults to 0.1 seconds).

        ncycl
            Number of animation cycles (defaults to 5).  Available in non-UI
            mode only.

        start
            Number of the starting substep (defaults to 1).

        end
            Number of the ending substep (defaults to the maximum substep).

        inc
            Increment between substeps (defaults to 1).

        autocontourkey
            Auto-scales contour values, based on the overall subset range of
            values  (defaults to 0, no auto-scaling).

        Notes
        -----
        ANDYNA involves an ANSYS macro which produces an animation of contour
        values through all the substeps of the last plot action command.  This
        command operates only on graphic display platforms supporting the /SEG
        command.  After executing ANDYNA, you can replay the animated sequence
        by issuing the ANIM command.

        The command functions only in the postprocessor.
        """
        command = f"ANDYNA,{delay},{ncycl},{start},{end},{inc},{autocontourkey}"
        return self.run(command, **kwargs)

    def anfile(self, lab="", fname="", ext="", **kwargs):
        """Saves or resumes an animation sequence to or from a file.

        APDL Command: /ANFILE

        Parameters
        ----------
        lab
            Label type.

            SAVE - Save the current animation to a file.

            RESUME - Resume an animation from a file.

        fname
            File name and directory path (248 characters maximum, including the
            characters needed for the directory path).  An unspecified
            directory path defaults to the working directory; in this case, you
            can use all 248 characters for the file name.

        ext
            Filename extension (eight-character maximum).

        Notes
        -----
        This command saves an animation to a file from local terminal segments
        or resumes an animation from a file to local terminal segments.  See
        the /SEG command for details on segment storage.  See the ANCNTR macro
        for a convenient method of storing graphics frames in terminal memory
        segments.  This command is device dependent and is valid in any
        processor.
        """
        command = f"/ANFILE,{lab},{fname},{ext}"
        return self.run(command, **kwargs)

    def anflow(
        self,
        nfram="",
        delay="",
        ncycl="",
        time="",
        spacing="",
        size="",
        length="",
        **kwargs,
    ):
        """Produces an animated sequence of particle flow in a flowing fluid or a charged particle traveling in an electric or magnetic field.

        APDL Command: ANFLOW

        Parameters
        ----------
        nfram
            Number of frames captured (defaults to 5).

        delay
            Time delay during animation (defaults to 0.1 seconds).

        ncycl
            Number of animation cycles (defaults to 5).  Non-UI mode only.

        time
            Total Trace Time (seconds) (defaults to 0, which is the full flow
            trace).

        spacing
            Particle spacing in seconds (defaults to 0).

        size
            Particle size (defaults to 0, which is a line).

        length
            Particle length fraction (defaults to .1).

        Notes
        -----
        ANFLOW invokes an ANSYS macro which produces an animation of particle
        flow in a flowing fluid or charged particle motion in an electric or
        magnetic field by the last plot action command (i.e., PLTRAC).  This
        command is only operational on graphic display platforms supporting the
        /SEG command.  After executing ANFLOW, you can replay the animated
        sequence by issuing the ANIM command.  This command is functional only
        in the Postprocessor.

        The TIME option lets you set the time interval of forward travel for
        the trace.  The SPACING option is used to define the particle spacing
        in seconds from adjacent particles in the stream line.  The SIZE
        variable sets the radius of the particle.  The LENGTH variable is used
        to define the particle length fraction.  By default, the LENGTH is set
        to .1, which means the particle occupies 10% of the flow region and the
        other 90% is a color-code line.  The SPACING and LENGTH variables only
        make sense when the SIZE variable is nonzero (i.e., the particle is
        bigger than the line).
        """
        command = f"ANFLOW,{nfram},{delay},{ncycl},{time},{spacing},{size},{length}"
        return self.run(command, **kwargs)

    def anharm(
        self,
        nfram="",
        delay="",
        ncycl="",
        nperiod="",
        cms_antype="",
        cms_modopt="",
        **kwargs,
    ):
        """Produces an animated sequence of time-harmonic results or complex mode

        APDL Command: ANHARM
        shapes.

        Parameters
        ----------
        nfram
            Number of frame captures per cycle.  Defaults to 12.

        delay
            Time delay (seconds) during animation.  Defaults to 0.1 seconds.

        ncycl
            Number of animation cycles.  Defaults to 5.  Not available in the
            GUI.

        nperiod
            Period number for the second set of frames showing the decay or
            growth of a mode shape. Only applies to complex mode shape
            animation. Defaults to 1, animating the decay or growth on the
            first period. Issue -1 to animate without decay or growth.

        cms_antype
            Analysis type performed in the CMS use pass. No default.

            MODAL - Modal analysis

            HARMIC - Harmonic analysis

        cms_modopt
            Mode extraction method selected in the CMS use pass. No default.

            UNSYM - Unsymmetric matrix

            DAMP - Damped system

            QRDAMP - Damped system using QR algorithm

        Notes
        -----
        ANHARM invokes an ANSYS macro which produces an animated sequence of:

        Time-harmonic results in the case of a harmonic analysis
        (ANTYPE,HARMIC)

        Complex mode shapes in the case of a modal analysis (ANTYPE,MODAL).

        In both cases, the results are those of the last plot action (for
        example, PLNSOL,B,SUM).

        The animation converts the complex solution variables (real and
        imaginary sets) into time varying results over one period. For example,
        if NFRAM = 12, then the frame captures are in increments of 30 degree
        phase angles.

        A second set of NFRAM frames will be generated for damped eigenmodes
        from complex eigensolvers to visualize any exponential decay or growth
        of the oscillations. The second set generated will display frames from
        the period number specified by NPERIOD.

        In a CMS analysis, the ANHARM command can be used after the CMS
        expansion pass or the use pass. To use ANHARM after the expansion pass,
        you must indicate whether a modal analysis or a harmonic analysis was
        performed in the CMS use pass by setting CMS_ANTYPE to either MODAL or
        HARMIC. If the use pass was a modal analysis, you must also set the
        CMS_MODOPT field to indicate the mode extraction method that was used
        (UNSYM, DAMP, or QRDAMP). If CMS_MODOPT = QRDAMP, it is assumed that
        CPXMOD was set to ON in the MODOPT command to request complex
        eigenmodes. If the ANHARM command is used after the use pass, it is not
        necessary to set the CMS_ANTYPE or CMS_MODOPT arguments.

        For more information about complex results postprocessing, see POST1
        and POST26 – Complex Results Postprocessing in the Mechanical APDL
        Theory Reference
        """
        command = f"ANHARM,{nfram},{delay},{ncycl},{nperiod},{cms_antype},{cms_modopt}"
        return self.run(command, **kwargs)

    def anim(self, ncycl="", kcycl="", delay="", **kwargs):
        """Displays animated graphics data for linear problems.

        APDL Command: ANIM

        Parameters
        ----------
        ncycl
            Number of cycles associated with the animation (defaults to 5 in
            non-GUI mode only)

        kcycl
            Animation mode:

            0 - Continuous animation cycle (forward-reverse-forward-etc.) (default).

            1 - Discontinuous animation cycle (forward-reset-forward-etc.).

        delay
            Time delay (seconds) between animation frames (defaults to 0.1
            seconds).

        Notes
        -----
        Use the ANIM command to create animations for linear problems only. The
        command uses the currently displayed picture based on one particular
        data set from the results file, and linearly interpolates that data
        into different sets, displaying pictures of each interpolated data set
        in sequence to create animation.  For information about creating
        animations for nonlinear problems, see the ANDATA command.

        This command is device-dependent.

        Do not resize the graphic while animation is in progress; doing so can
        result in distorted plots.

        For more information, see the /SEG command for details about segment
        storage, and the ANCNTR macro for a convenient method of storing
        graphics frames in terminal memory segments.

        This command is valid in any processor.
        """
        command = f"ANIM,{ncycl},{kcycl},{delay}"
        return self.run(command, **kwargs)

    def anisos(self, nfram="", delay="", ncycl="", **kwargs):
        """Produces an animated sequence of an isosurface.

        APDL Command: ANISOS

        Parameters
        ----------
        nfram
            Number of frames captures (defaults to 9).

        delay
            Time delay during animation (defaults to 0.1 seconds).

        ncycl
            Number of animation cycles (defaults to 5).  Available in non-UI
            mode only.

        Notes
        -----
        ANISOS involves an ANSYS macro which produces an animation of an
        isosurface  of the last plot action command (for example,
        PLNSOL,S,EQV).  The ANISOS command operates only on graphic display
        platforms supporting the /SEG command.  After executing ANISOS, you can
        replay the animated sequence by issuing the ANIM command.

        This command functions only in the postprocessor.
        """
        command = f"ANISOS,{nfram},{delay},{ncycl}"
        return self.run(command, **kwargs)

    def anmode(self, nfram="", delay="", ncycl="", kaccel="", **kwargs):
        """Produces an animated sequence of a mode shape.

        APDL Command: ANMODE

        Parameters
        ----------
        nfram
            Number of frames captures (defaults to 5).

        delay
            Time delay during animation (defaults to 0.1 seconds).

        ncycl
            Number of animation cycles (defaults to 5).  Available in non-UI
            mode only.

        kaccel
            Acceleration type:

            0 - Linear acceleration.

            1 - Sinusoidal acceleration.

        Notes
        -----
        ANMODE involves an ANSYS macro which produces an animation of mode
        shape of the last plot action command (for example, PLDISP).  The
        ANMODE command operates only on graphic display platforms supporting
        the /SEG command.  After executing ANMODE, you can replay the animated
        sequence by issuing the ANIM command.

        This command functions only in the postprocessor.
        """
        command = f"ANMODE,{nfram},{delay},{ncycl},{kaccel}"
        return self.run(command, **kwargs)

    def anmres(
        self,
        delay="",
        min_="",
        max_="",
        inc="",
        autocntrky="",
        freq="",
        ext="",
        **kwargs,
    ):
        """Performs animation of results over multiple results files in an

        APDL Command: ANMRES
        explicit dynamic structural analysis or fluid flow analysis with
        remeshing.

        Parameters
        ----------
        delay
            Time delay during animation (default = 0.5 seconds).

        min\_
            Minimum results file number to animate. Default = 1 (for
            Jobname.RS01).

        max\_
            Maximum results file number to animate. Defaults to the highest
            numbered results file, Jobname.RSnn.

        inc
            Increment between results file numbers. Default = 1.

        autocntrky
            Automatic contour scaling option.

            0 - No auto-scaling (default).

            1 - Auto-scaling on.

        freq
             Results frequency key.

            0 or 1 - Animate every results set in each Jobname.EXT file (default).

            2 - Animate every other results set in each Jobname.EXT file.

            n - Animate every nth results set in each Jobname.EXT file.

        ext
            Extension of result files

            'rfl' - Animate Jobname.rflnn

            'rs' - Animate Jobname.rsnn. Default = 'rs'.

        Notes
        -----
        ANMRES invokes an ANSYS macro that performs animation across multiple
        results files (Jobname.EXT, Jobname.EXT, etc.) produced by an explicit
        dynamic structural analysis or fluid flow analysis with remeshing.
        Multiple results files typically occur when adaptive meshing is used in
        an explicit dynamic structural analysis or fluid flow analysis with
        remeshing. Each results file must have more than one set of results.
        ANMRES cannot be used for multiple results files that are caused by
        file splitting.

        ANMRES animates results from files having the currently specified
        jobname (Jobname.EXT - Jobname.EXT).  To change the current jobname,
        use  the /FILNAME command. The animation is based on the last plot
        command (e.g., PLDISP).

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"ANMRES,{delay},{min_},{max_},{inc},{autocntrky},{freq},{ext}"
        return self.run(command, **kwargs)

    def antime(
        self,
        nfram="",
        delay="",
        ncycl="",
        autocntrky="",
        rsltdat="",
        min_="",
        max_="",
        **kwargs,
    ):
        """Produces a  sequential contour animation over a range of time.

        APDL Command: ANTIME

        Parameters
        ----------
        nfram
            Number of frame captures (defaults to 5).

        delay
            Time delay during animation (defaults to 0.1 seconds).

        ncycl
            Number of animation cycles (defaults to 5).  Available in non-UI
            mode only.

        autocntrky
            Auto-scales contour values, based on the overall subset range of
            values.  The auto-scaling option defaults to 0, no auto-scaling.

        rsltdat
            The results data to be used for the animation sequence.  This can
            be:

            0 - Current load step data (default).

            1 - Range of load step data.

            2 - Range of time data.

        min\_
            The range minimum value.  If left blank defaults to the first data
            point.

        max\_
            The range maximum value.  If left blank defaults to the last data
            point.

        Notes
        -----
        The ANTIME command operates only on graphic display platforms
        supporting the /SEG command. It uses an ANSYS macro to produce an
        animation of contour values for the last plot action command (for
        example, PLDISP).  After executing ANTIME, the ANIM command will replay
        the animated sequence.

        This command functions only in the postprocessor.
        """
        command = f"ANTIME,{nfram},{delay},{ncycl},{autocntrky},{rsltdat},{min_},{max_}"
        return self.run(command, **kwargs)

    def trtime(self, time="", spacing="", offset="", size="", length="", **kwargs):
        """Defines the options used for the PLTRAC (particle flow or charged

        APDL Command: TRTIME
        particle trace) command.

        Parameters
        ----------
        time
            Total Trace Time (seconds) (defaults to 0, which is the full flow
            trace).

        spacing
            Particle spacing in seconds (defaults to 0).

        offset
            Particle offset in seconds (defaults to 0).  It is used internally
            in the ANFLOW macro to produce an animation of particle flow in a
            flowing fluid or charged particle motion in an electric or magnetic
            field.

        size
            Particle size (defaults to 0, which is a line).

        length
            Particle length fraction (defaults to .1).

        Notes
        -----
        The TRTIME command varies the type of   PLTRAC display produced.
        Particle flow or charged particle traces follow a particle's path in
        the forward and backward direction of travel. The DOF selected
        determines the color of the particle trace.  SPACING defines the
        particle spacing in seconds from adjacent particles in the stream line.
        OFFSET defines the offset in seconds from the spacing set by the
        SPACING argument.

        LENGTH defines the particle length fraction.  The default value (.1),
        means the particle occupies 10% of the flow region, and the other 90%
        is a color-coded line.

        SIZE sets the radius of the particle. Use SPACING, OFFSET and LENGTH
        only when SIZE is nonzero (i.e., the particle is bigger than the line).

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"TRTIME,{time},{spacing},{offset},{size},{length}"
        return self.run(command, **kwargs)
