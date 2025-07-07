# Copyright (C) 2016 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


class Animation:

    def ancntr(self, nfram: str = "", delay: str = "", ncycl: str = "", **kwargs):
        r"""Produces an animated sequence of a contoured deformed shape.

        Mechanical APDL Command: `ANCNTR <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ANCNTR.html>`_

        Parameters
        ----------
        nfram : str
            Number of frames captures (defaults to 5).

        delay : str
            Time delay during animation (defaults to 0.1 seconds).

        ncycl : str
            Number of animation cycles (defaults to 5). Available in non-UI mode only.

        Notes
        -----

        .. _ANCNTR_notes:

        :ref:`ancntr` involves a Mechanical APDL macro which produces an animation of a contoured deformed
        shape of
        the last plot action command. This command operates only on graphic display platforms supporting the
        :ref:`seg` command. After executing :ref:`ancntr`, you can replay the animated sequence by issuing
        the :ref:`anim` command.

        The command functions only in the postprocessor.
        """
        command = f"ANCNTR,{nfram},{delay},{ncycl}"
        return self.run(command, **kwargs)

    def ancut(
        self,
        nfram: str = "",
        delay: str = "",
        ncycl: str = "",
        qoff: str = "",
        ktop: str = "",
        topoff: str = "",
        node1: str = "",
        node2: str = "",
        node3: str = "",
        **kwargs,
    ):
        r"""Produces an animated sequence of Q-slices.

        Mechanical APDL Command: `ANCUT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ANCUT.html>`_

        Parameters
        ----------
        nfram : str
            Number of frames captures (defaults to 5).

        delay : str
            Time delay during animation (defaults to 0.1 seconds).

        ncycl : str
            Number of animation cycles (defaults to 5). Available in non-UI mode only.

        qoff : str
            Q-slice working plane increment (defaults to.1 half screens).

        ktop : str
            Topological effect on or off (YES or NO; default is NO).

        topoff : str
            Topological offset (default is.1 half screens).

        node1 : str
            Node 1 for start of the Q-slice.

        node2 : str
            Node 2 for direction of the Q-slice.

        node3 : str
            Node 3 for plane of the Q-slice.

        Notes
        -----

        .. _ANCUT_notes:

        :ref:`ancut` involves a Mechanical APDL macro which produces an animation of Q-slices of the last
        plot
        action command. This command operates only on graphic display platforms supporting the :ref:`seg`
        command. After executing :ref:`ancut`, you can replay the animated sequence by issuing the
        :ref:`anim` command.

        The command functions only in the postprocessor.
        """
        command = f"ANCUT,{nfram},{delay},{ncycl},{qoff},{ktop},{topoff},{node1},{node2},{node3}"
        return self.run(command, **kwargs)

    def ancyc(
        self, numframes: str = "", kcycl: int | str = "", delay: str = "", **kwargs
    ):
        r"""Applies a traveling wave animation to graphics data in a modal cyclic symmetry analysis.

        Mechanical APDL Command: `ANCYC <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ANCYC.html>`_

        **Command default:**

        .. _ANCYC_default:

        The default :ref:`ancyc` command (issuing the command with no arguments) specifies these implicit
        argument values: :ref:`ancyc`, 18, 0, 0.1

        Parameters
        ----------
        numframes : str
            The number of plot frames for the animation. Valid values range from 5 through 36. The default
            is 18. A low value (because it specifies fewer graphical frames) produces a rougher animation
            but loads faster. A high value produces a smoother animation but requires more time to load.

        kcycl : int or str
            The animation mode:

            * ``0`` - Continuous animation cycle (forward-reverse-forward).

            * ``1`` - Discontinuous animation cycle (forward-reset-forward). This option is the default.



        delay : str
            The time delay (in seconds) between animation frames. Valid values range from 0.1 through 1.0.
            The default is 0.1 seconds, which produces a seemingly real-time animation. A higher value
            produces a slower animation.

        Notes
        -----

        .. _ANCYC_notes:

        The :ref:`ancyc` command is valid in a `modal cyclic symmetry analysis
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cycsym/advcycmodalans.html#cycsym_postproc_modal>`_
        only.

        The command animates the cyclic symmetry mode shape plot in the General Post Processor (
        :ref:`post1` ). When you issue a nodal- or element-results plot command (for example, :ref:`plnsol`,
        :ref:`plesol`, or :ref:`pldisp` ) and then issue the :ref:`ancyc` command, Mechanical APDL applies a
        traveling wave animation to the mode shape plot.

        Each frame of the animation is created by expanding the cyclic symmetry mode shape at increasing
        phase angles (via the :ref:`cycexpand` command) starting at zero in equal increments over 360°. The
        phase-angle increment is 360 / ``NUMFRAMES``.

        The animation display shows the traveling wave of the result quantity being plotted. The traveling
        wave animation is applicable only to nodal diameters (harmonic indices) greater than 0 and less than
        ``N`` / 2 (where ``N`` is the number of cyclic sectors in the model).

        For more information, see `Applying a Traveling Wave Animation to the Cyclic Model
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cycsym/advcycmodalans.html#gadvcyctwave>`_
        in the `Cyclic Symmetry Analysis Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cycsym/cycsym_example.html>`_.
        """
        command = f"ANCYC,{numframes},{kcycl},{delay}"
        return self.run(command, **kwargs)

    def andata(
        self,
        delay: str = "",
        ncycl: str = "",
        rsltdat: int | str = "",
        min_: str = "",
        max_: str = "",
        incr: str = "",
        frclst: str = "",
        autocont: str = "",
        autocntr: str = "",
        **kwargs,
    ):
        r"""Displays animated graphics data for nonlinear problems.

        Mechanical APDL Command: `ANDATA <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ANDATA.html>`_

        Parameters
        ----------
        delay : str
            Time delay during animation (defaults to 0.5 seconds).

        ncycl : str
            Number of animation cycles (defaults to 5). Available in non-UI mode only.

        rsltdat : int or str
            The type of results data to be used for the animation sequence. This can be:

            * ``0`` - Current load step data (default).

            * ``1`` - Range of load step data.

            * ``2`` - Range of results data.

        min_ : str
            The range minimum value. If left blank or 0, defaults to the first data point.

        max_ : str
            The range maximum value. If left blank or 0, defaults to the last data point.

        incr : str
            The increment between result data (defaults to 1).

        frclst : str
            Key to force the last sub step in a selected load step to be included in the animation (defaults
            to 0).

        autocont : str
            A value of 1 enables automatic scaling of contour values based on the overall subset range of
            values. The default value is 0 (no automatic scaling).

        autocntr : str
            A value of 1 disables automatic centering of displaced plots. The default value is 0 (allow
            automatic centering).

        Notes
        -----

        .. _ANDATA_notes:

        Use the :ref:`andata` command to create animations for nonlinear problems. The command works by
        displaying an individual graphical image for each result data set from the results file. For
        information about creating animations for linear problems, see the :ref:`anim` command.

        The command operates only on graphic display platforms supporting the :ref:`seg` command. It uses a
        macro to produce an animation based on the last plot action command (for example, :ref:`pldisp` ).

        The results file must have more than one set of results.

        The command implicitly issues :ref:`slashdscale`, 1 for default displacement scaling. Large
        displacements may not give good results.


        This command functions only in the postprocessor.
        """
        command = f"ANDATA,{delay},{ncycl},{rsltdat},{min_},{max_},{incr},{frclst},{autocont},,{autocntr}"
        return self.run(command, **kwargs)

    def andscl(self, nfram: str = "", delay: str = "", ncycl: str = "", **kwargs):
        r"""Produces an animated sequence of a deformed shape.

        Mechanical APDL Command: `ANDSCL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ANDSCL.html>`_

        Parameters
        ----------
        nfram : str
            Number of frames captured (defaults to 5).

        delay : str
            Time delay during animation (defaults to 0.1 seconds).

        ncycl : str
            Number of animation cycles (defaults to 5). Available in non-UI mode only.

        Notes
        -----

        .. _ANDSCL_notes:

        :ref:`andscl` involves a Mechanical APDL macro which produces an animation of displacement of the
        last plot
        action command (for example, :ref:`pldisp` ). This command operates only on graphic display
        platforms supporting the :ref:`seg` command. After executing :ref:`andscl`, you can replay the
        animated sequence by issuing the :ref:`anim` command.

        The command functions only in the postprocessor.
        """
        command = f"ANDSCL,{nfram},{delay},{ncycl}"
        return self.run(command, **kwargs)

    def andyna(
        self,
        delay: str = "",
        ncycl: str = "",
        start: str = "",
        end: str = "",
        inc: str = "",
        autocontourkey: str = "",
        **kwargs,
    ):
        r"""Produces an animated sequence of contour values through substeps.

        Mechanical APDL Command: `ANDYNA <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ANDYNA.html>`_

        Parameters
        ----------
        delay : str
            Time delay during animation (defaults to 0.1 seconds).

        ncycl : str
            Number of animation cycles (defaults to 5). Available in non-UI mode only.

        start : str
            Number of the starting substep (defaults to 1).

        end : str
            Number of the ending substep (defaults to the maximum substep).

        inc : str
            Increment between substeps (defaults to 1).

        autocontourkey : str
            Auto-scales contour values, based on the overall subset range of values (defaults to 0, no auto-
            scaling).

        Notes
        -----

        .. _ANDYNA_notes:

        :ref:`andyna` involves a Mechanical APDL macro which produces an animation of contour values through
        all
        the substeps of the last plot action command. This command operates only on graphic display
        platforms supporting the :ref:`seg` command. After executing :ref:`andyna`, you can replay the
        animated sequence by issuing :ref:`anim`.

        The command functions only in the postprocessor.
        """
        command = f"ANDYNA,{delay},{ncycl},{start},{end},{inc},{autocontourkey}"
        return self.run(command, **kwargs)

    def anfile(self, lab: str = "", fname: str = "", ext: str = "", **kwargs):
        r"""Saves or resumes an animation sequence to or from a file.

        Mechanical APDL Command: `/ANFILE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ANFILE.html>`_

        Parameters
        ----------
        lab : str
            Label type.

            * ``SAVE`` - Save the current animation to a file.

            * ``RESUME`` - Resume an animation from a file.

        fname : str
            File name and directory path (248 characters maximum, including the characters needed for the
            directory path). An unspecified directory path defaults to the working directory; in this case,
            you can use all 248 characters for the file name. The file name defaults to :file:`Jobname`.

        ext : str
            Filename extension (eight-character maximum). The extension defaults to ANIM if ``Fname`` is
            blank.

        Notes
        -----

        .. _s-ANFILE_notes:

        This command saves an animation to a file from local terminal segments or resumes an animation from
        a file to local terminal segments. See the :ref:`seg` command for details on segment storage. See
        the :ref:`ancntr` macro for a convenient method of storing graphics frames in terminal memory
        segments. This command is device dependent and is valid in any processor.
        """
        command = f"/ANFILE,{lab},{fname},{ext}"
        return self.run(command, **kwargs)

    def anflow(
        self,
        nfram: str = "",
        delay: str = "",
        ncycl: str = "",
        time: str = "",
        spacing: str = "",
        size: str = "",
        length: str = "",
        **kwargs,
    ):
        r"""Produces an animated sequence of a charged particle traveling in an electric or magnetic field.

        Mechanical APDL Command: `ANFLOW <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ANFLOW.html>`_

        Parameters
        ----------
        nfram : str
            Number of frames captured (defaults to 5).

        delay : str
            Time delay during animation (defaults to 0.1 seconds).

        ncycl : str
            Number of animation cycles (defaults to 5). Non-UI mode only.

        time : str
            Total Trace Time (seconds) (defaults to 0, which is the full flow trace).

        spacing : str
            Particle spacing in seconds (defaults to 0).

        size : str
            Particle size (defaults to 0, which is a line).

        length : str
            Particle length fraction (defaults to.1).

        Notes
        -----

        .. _ANFLOW_notes:

        :ref:`anflow` invokes a Mechanical APDL macro which produces an animation of charged particle motion
        in an
        electric or magnetic field by the last plot action command (that is, :ref:`pltrac` ). This command
        is only operational on graphic display platforms supporting the :ref:`seg` command. After executing
        :ref:`anflow`, you can replay the animated sequence by issuing the :ref:`anim` command. This command
        is functional only in the Postprocessor.

        The ``TIME`` option lets you set the time interval of forward travel for the trace. The ``SPACING``
        option is used to define the particle spacing in seconds from adjacent particles in the stream line.
        The ``SIZE`` variable sets the radius of the particle. The ``LENGTH`` variable is used to define the
        particle length fraction. By default, the ``LENGTH`` is set to.1, which means the particle occupies
        10% of the trace region and the other 90% is a color-code line. The ``SPACING`` and ``LENGTH``
        variables only make sense when the ``SIZE`` variable is nonzero (that is, the particle is bigger
        than the line).
        """
        command = f"ANFLOW,{nfram},{delay},{ncycl},{time},{spacing},{size},{length}"
        return self.run(command, **kwargs)

    def anharm(
        self,
        nfram: str = "",
        delay: str = "",
        ncycl: str = "",
        nperiod: str = "",
        cms_antype: str = "",
        cms_modopt: str = "",
        **kwargs,
    ):
        r"""Produces an animated sequence of time-harmonic results or complex mode shapes.

        Mechanical APDL Command: `ANHARM <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ANHARM.html>`_

        Parameters
        ----------
        nfram : str
            Number of frame captures per cycle. Defaults to 12.

        delay : str
            Time delay (seconds) during animation. Defaults to 0.1 seconds.

        ncycl : str
            Number of animation cycles. Defaults to 5. Not available in the GUI.

        nperiod : str
            Period number for the second set of frames showing the decay or growth of a mode shape. Only
            applies to complex mode shape animation. Defaults to 1, animating the decay or growth on the
            first period. Issue -1 to animate without decay or growth.

        cms_antype : str
            Analysis type performed in the CMS use pass. No default.

            * ``MODAL`` - Modal analysis

            * ``HARMIC`` - Harmonic analysis

        cms_modopt : str
            Mode extraction method selected in the CMS use pass. No default.

            * ``UNSYM`` - Unsymmetric matrix

            * ``DAMP`` - Damped system

            * ``QRDAMP`` - Damped system using QR algorithm

        Notes
        -----

        .. _ANHARM_notes:

        :ref:`anharm` invokes a Mechanical APDL macro which produces an animated sequence of:

        * Time-harmonic results in the case of a harmonic analysis ( :ref:`antype`,HARMIC)

        * Complex mode shapes in the case of a modal analysis ( :ref:`antype`,MODAL).

        In both cases, the results are those of the last plot action (for example, :ref:`plnsol`,B,SUM).

        The animation converts the complex solution variables (real and imaginary sets) into time varying
        results over one period. For example, if ``NFRAM`` = 12, then the frame captures are in increments
        of 30 degree phase angles.

        A second set of ``NFRAM`` frames will be generated for damped eigenmodes from complex eigensolvers
        to visualize any exponential decay or growth of the oscillations. The second set generated will
        display frames from the period number specified by ``NPERIOD``.

        In a CMS analysis, the :ref:`anharm` command can be used after the CMS expansion pass or the use
        pass. To use :ref:`anharm` after the expansion pass, you must indicate whether a modal analysis or a
        harmonic analysis was performed in the CMS use pass by setting ``CMS_ANTYPE`` to either MODAL or
        HARMIC. If the use pass was a modal analysis, you must also set the ``CMS_MODOPT`` field to indicate
        the mode extraction method that was used (UNSYM, DAMP, or QRDAMP). If ``CMS_MODOPT`` = QRDAMP, it is
        assumed that ``CPXMOD`` was set to ON in the :ref:`modopt` command to request complex eigenmodes. If
        the :ref:`anharm` command is used after the use pass, it is not necessary to set the ``CMS_ANTYPE``
        or ``CMS_MODOPT`` arguments.

        For more information about complex results postprocessing, see `POST1 and POST26 - Complex Results
        Postprocessing
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_post15.html#thyeq1cdmplxres6a>`_
        """
        command = f"ANHARM,{nfram},{delay},{ncycl},{nperiod},{cms_antype},{cms_modopt}"
        return self.run(command, **kwargs)

    def anim(self, ncycl: str = "", kcycl: int | str = "", delay: str = "", **kwargs):
        r"""Displays animated graphics data for linear problems.

        Mechanical APDL Command: `ANIM <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ANIM.html>`_

        Parameters
        ----------
        ncycl : str
            Number of cycles associated with the animation (defaults to 5 in non-GUI mode only)

        kcycl : int or str
            Animation mode:

            * ``0`` - Continuous animation cycle (forward-reverse-forward-etc.) (default).

            * ``1`` - Discontinuous animation cycle (forward-reset-forward-etc.).

        delay : str
            Time delay (seconds) between animation frames (defaults to 0.1 seconds).

        Notes
        -----

        .. _ANIM_notes:

        Use the :ref:`anim` command to create animations for linear problems only. The command uses the
        currently displayed picture based on one particular data set from the results file, and linearly
        interpolates that data into different sets, displaying pictures of each interpolated data set in
        sequence to create animation. For information about creating animations for nonlinear problems, see
        the :ref:`andata` command.

        This command is device-dependent.


        Do not resize the graphic while animation is in progress; doing so can result in distorted plots.

        For more information, see the :ref:`seg` command for details about segment storage, and the
        :ref:`ancntr` macro for a convenient method of storing graphics frames in terminal memory segments.

        This command is valid in any processor.
        """
        command = f"ANIM,{ncycl},{kcycl},{delay}"
        return self.run(command, **kwargs)

    def anisos(self, nfram: str = "", delay: str = "", ncycl: str = "", **kwargs):
        r"""Produces an animated sequence of an isosurface.

        Mechanical APDL Command: `ANISOS <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ANISOS.html>`_

        Parameters
        ----------
        nfram : str
            Number of frames captures (defaults to 9).

        delay : str
            Time delay during animation (defaults to 0.1 seconds).

        ncycl : str
            Number of animation cycles (defaults to 5). Available in non-UI mode only.

        Notes
        -----

        .. _ANISOS_notes:

        :ref:`anisos` invokes a Mechanical APDL macro which produces an animation of an isosurface of the
        last plot
        action command (for example, :ref:`plnsol`,S,EQV). The :ref:`anisos` command operates only on
        graphic display platforms supporting the :ref:`seg` command. After executing :ref:`anisos`, you can
        replay the animated sequence by issuing the :ref:`anim` command.

        This command functions only in the postprocessor.
        """
        command = f"ANISOS,{nfram},{delay},{ncycl}"
        return self.run(command, **kwargs)

    def anmode(
        self,
        nfram: str = "",
        delay: str = "",
        ncycl: str = "",
        kaccel: int | str = "",
        **kwargs,
    ):
        r"""Produces an animated sequence of a mode shape.

        Mechanical APDL Command: `ANMODE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ANMODE.html>`_

        Parameters
        ----------
        nfram : str
            Number of frames captures (defaults to 5).

        delay : str
            Time delay during animation (defaults to 0.1 seconds).

        ncycl : str
            Number of animation cycles (defaults to 5). Available in non-UI mode only.

        kaccel : int or str
            Acceleration type:

            * ``0`` - Linear acceleration.

            * ``1`` - Sinusoidal acceleration.

        Notes
        -----

        .. _ANMODE_notes:

        :ref:`anmode` invokes a Mechanical APDL macro which produces an animation of mode shape of the last
        plot
        action command (for example, :ref:`pldisp` ). The :ref:`anmode` command operates only on graphic
        display platforms supporting the :ref:`seg` command. After executing :ref:`anmode`, you can replay
        the animated sequence by issuing the :ref:`anim` command.

        This command functions only in the postprocessor.
        """
        command = f"ANMODE,{nfram},{delay},{ncycl},{kaccel}"
        return self.run(command, **kwargs)

    def antime(
        self,
        nfram: str = "",
        delay: str = "",
        ncycl: str = "",
        autocntrky: str = "",
        rsltdat: int | str = "",
        min_: str = "",
        max_: str = "",
        **kwargs,
    ):
        r"""Generates a sequential contour animation over a range of time.

        Mechanical APDL Command: `ANTIME <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ANTIME.html>`_

        Parameters
        ----------
        nfram : str
            Number of frame captures (defaults to 5).

        delay : str
            Time delay during animation (defaults to 0.1 seconds).

        ncycl : str
            Number of animation cycles (defaults to 5). Available in non-UI mode only.

        autocntrky : str
            Auto-scales contour values, based on the overall subset range of values. The auto-scaling option
            defaults to 0, no auto-scaling.

        rsltdat : int or str
            The results data to be used for the animation sequence. This can be:

            * ``0`` - Current load step data (default).

            * ``1`` - Range of load step data.

            * ``2`` - Range of time data.

        min_ : str
            The range minimum value. If left blank defaults to the first data point.

        max_ : str
            The range maximum value. If left blank defaults to the last data point.

        Notes
        -----

        .. _ANTIME_notes:

        The :ref:`antime` command operates only on graphic display platforms supporting the :ref:`seg`
        command. It uses a Mechanical APDL macro to produce an animation of contour values for the last plot
        action
        command (for example, :ref:`pldisp` ). After executing :ref:`antime`, the :ref:`anim` command
        replays the animated sequence.

        This command functions only in the postprocessor.
        """
        command = f"ANTIME,{nfram},{delay},{ncycl},{autocntrky},{rsltdat},{min_},{max_}"
        return self.run(command, **kwargs)

    def trtime(
        self,
        time: str = "",
        spacing: str = "",
        offset: str = "",
        size: str = "",
        length: str = "",
        **kwargs,
    ):
        r"""Defines the options used for the :ref:`pltrac` (charged particle trace) command.

        Mechanical APDL Command: `TRTIME <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_TRTIME.html>`_

        Parameters
        ----------
        time : str
            Total Trace Time (seconds) (defaults to 0, which is the full particle trace).

        spacing : str
            Particle spacing in seconds (defaults to 0).

        offset : str
            Particle offset in seconds (defaults to 0). It is used internally in the :ref:`anflow` macro to
            produce an animation of charged particle motion in an electric or magnetic field.

        size : str
            Particle size (defaults to 0, which is a line).

        length : str
            Particle length fraction (defaults to.1).

        Notes
        -----

        .. _TRTIME_notes:

        The :ref:`trtime` command varies the type of :ref:`pltrac` display produced. Charged particle traces
        follow a particle's path in the forward and backward direction of travel. The DOF selected
        determines the color of the particle trace. ``SPACING`` defines the particle spacing in seconds from
        adjacent particles in the stream line. ``OFFSET`` defines the offset in seconds from the spacing set
        by the ``SPACING`` argument.

        ``LENGTH`` defines the particle length fraction. The default value (.1), means the particle occupies
        10% of the trace region, and the other 90% is a color-coded line.

        ``SIZE`` sets the radius of the particle. Use ``SPACING``, ``OFFSET`` and ``LENGTH`` only when
        ``SIZE`` is nonzero (that is, the particle is bigger than the line).
        """
        command = f"TRTIME,{time},{spacing},{offset},{size},{length}"
        return self.run(command, **kwargs)
