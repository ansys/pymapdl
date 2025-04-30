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


class DynamicOptions:

    def kryopt(self, maxdim: str = "", restol: str = "", **kwargs):
        r"""Specifies solution options for a Krylov method harmonic analysis.

        Mechanical APDL Command: `KRYOPT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_KRYOPT.html>`_

        Parameters
        ----------
        maxdim : str
            Maximum dimension of subspace. The default size is automatically determined by the program
            (ranges around 50).

        restol : str
            Tolerance used to verify the L-2 norm values of calculated residuals and issue a warning if
            ``RESTOL`` is exceeded throughout the entire frequency range. Default = 0.05.

        Notes
        -----

        .. _KRYOPT_notes:

        This command is used to specify solution options for a harmonic analysis solved with the Krylov
        method ( ``Method`` = KRYLOV on :ref:`hropt`, see also `Frequency-Sweep Harmonic Analysis via the
        Krylov Method
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/str_Krysweep.html#str_Krylov_macros>`_

        Increasing subspace size ( ``MAXDIM`` ) improves solution accuracy with the trade-off of increased
        computational cost and additional memory requirements.
        """
        command = f"KRYOPT,{maxdim},,,{restol}"
        return self.run(command, **kwargs)

    def lvscale(self, fact: str = "", ldstep: str = "", **kwargs):
        r"""Scales the load vector for mode-superposition analyses.

        Mechanical APDL Command: `LVSCALE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_LVSCALE.html>`_

        Parameters
        ----------
        fact : str
            Scale factor applied to both the real and imaginary (if they exist) components of the load
            vector. Defaults to 0.0.

        ldstep : str
            Specifies the load step number from the modal analysis ( :ref:`modcont`,ON). It corresponds to
            the load vector number. Defaults to 1. The maximum admissible value is the number of vectors
            written in the :file:`Jobname.MODE` file.

        Notes
        -----

        .. _LVSCALE_notes:

        Specifies the scale factor for the load vector that was created in a modal ( :ref:`antype`,MODAL)
        analysis. Applies only to the mode-superposition transient analysis ( :ref:`antype`,TRANS), mode-
        superposition harmonic analysis ( :ref:`antype`,HARMIC), random vibration analysis (
        :ref:`antype`,SPECTR with :ref:`spopt`,PSD), and multiple point response spectrum analysis (
        :ref:`antype`,SPECTR with :ref:`spopt`,MPRS). For PSD and MPRS analyses, :ref:`lvscale` is only
        applicable for pressure loading.

        The :ref:`lvscale` command supports tabular boundary conditions (%TABNAME_X%) for ``FACT`` input
        values only as a function of time in the mode-superposition transient ( :ref:`antype`,TRANS) or as a
        function of frequency in mode-superposition harmonic ( :ref:`antype`,HARMIC).

        `MPC contact
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_ctec/Hlp_ctec_restmpc.html>`_ generates
        constraint equations that can include constant terms (included on the right-hand side of the system
        equation). The :ref:`lvscale` command scales the constant terms.

        In mode-superposition transient and harmonic analyses, all of the load vectors need to be scaled in
        the first load step. Use a zero scale factor if they are not actually used in this first load step.
        Similarly, in random vibration and multipoint response spectrum analyses, all of the load vectors
        need to be scaled in the first participation factor calculation ( :ref:`pfact` ). Use a zero scale
        factor if they are not actually used for the first input table.

        This command is also valid in PREP7.
        """
        command = f"LVSCALE,{fact},{ldstep}"
        return self.run(command, **kwargs)

    def midtol(self, key: str = "", tolerb: str = "", resfq: str = "", **kwargs):
        r"""Sets midstep residual criterion values for structural transient analyses.

        Mechanical APDL Command: `MIDTOL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MIDTOL.html>`_

        **Command default:**
        For transient structural analysis, the out-of-balance residual is not checked at the midstep.

        Parameters
        ----------
        key : str
            Midstep residual criterion activation key.

            * ``ON or 1`` - Activate midstep residual criterion in a structural transient analysis (default).

            * ``OFF or 0`` - Deactivate midstep residual criterion in a structural transient analysis.

            * ``STAT`` - List the current midstep residual criterion setting.

        tolerb : str
            Midstep residual tolerance or reference value for bisection. Defaults to 100 times the ``TOLER``
            setting of the :ref:`cnvtol` command.

            If ``TOLERB`` > 0, it is used as a tolerance about the typical force and/or moment to compare
            midstep residual force and/or moment for convergence.

            If ``TOLERB`` < 0, it is used as a reference force value against which the midstep residual
            force is compared for convergence. The reference force value is used to compute a reference
            moment value for midstep residual moment comparison.

            If midstep residual force and/or moment has not converged and :ref:`autots`,ON is used, then
            ``TOLERB`` is also used to predict time step size for bisection.

        resfq : str
            Key to use response frequency computation along with midstep residual criterion for automatic time
            stepping ( :ref:`autots`,ON).

            * ``OFF or 0`` - Do not calculate response frequency and do not consider it in the automatic time
              stepping (default).

            * ``ON or 1`` - Calculate response frequency and consider it in the automatic time stepping.

        Notes
        -----
        When ``TOLERB`` is input as a tolerance value ( ``TOLERB`` > 0), the typical force and/or moment
        from the regular time step is used in the midstep residual force and/or moment comparison.

        In a structural transient analysis, the suggested tolerance range of ``TOLERB`` ( ``TOLERB`` > 0) is
        as follows:

        * ``TOLERB`` = 1 to 10 times the ``TOLER`` setting of the :ref:`cnvtol` command for high accuracy
          solution.
        * ``TOLERB`` = 10 to 100 times the ``TOLER`` setting of the :ref:`cnvtol` command for medium
          accuracy solution.
        * ``TOLERB`` = more than 100 times the ``TOLER`` setting of the :ref:`cnvtol` command for low
          accuracy solution.
        If the structural transient analysis is elastic and linear, and the load is constant or changes
        slowly, use a smaller value of
         ``TOLERB`` to achieve an accurate solution. If the analysis involves large amounts of energy dissipation, such as elastic-plastic material, ``TOLERB`` can be larger. If the analysis includes contact or rapidly varying loads, a smaller value of ``TOLERB`` should be used if high frequency response is important; otherwise, a larger value of ``TOLERB`` may be used to enable faster convergence with larger time step sizes.

        For more information on how the midstep criterion is used by the program, see `Midstep Residual for
        Structural Dynamic Analysis
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_tool6.html#eq3ee0a0c7-284e-4f2b-ad70-338834430235>`_
         in the `Mechanical APDL Theory Reference
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_biblio.html>`_.

        This command is also valid in PREP7.
        """
        command = f"MIDTOL,{key},{tolerb},{resfq}"
        return self.run(command, **kwargs)

    def mascale(self, massfact: str = "", **kwargs):
        r"""Activates scaling of the entire system matrix.

        Mechanical APDL Command: `MASCALE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MASCALE.html>`_

        Parameters
        ----------
        massfact : str
            Scaling factor (> 0) for the mass matrix. Default = 1.0.

        Notes
        -----

        .. _MASCALE_notes:

        This command is supported in the first load step of the analysis only.

        The following features are not affected by the scaling:

        * Ocean loading ( `Applying Ocean Loading from a Hydrodynamic Analysis
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_adv/advOLexample.html>`_

        * Steady-state rolling ( :ref:`sstate` )

        The mass-related information (mass, center of mass, and mass moments of inertia) printed in the mass
        summary is based on unscaled mass properties.
        """
        command = f"MASCALE,{massfact}"
        return self.run(command, **kwargs)

    def mdplot(self, function: str = "", dmpname: str = "", scale: str = "", **kwargs):
        r"""Plots frequency-dependent modal damping coefficients calculated by DMPEXT.

        Mechanical APDL Command: `MDPLOT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MDPLOT.html>`_

        Parameters
        ----------
        function : str
            Function to display.

            * ``d_coeff`` - Damping coefficient

            * ``s_coeff`` - Squeeze coefficient

            * ``d_ratio`` - Damping ratio

            * ``s_ratio`` - Squeeze stiffness ratio

        dmpname : str
            Array parameter name where damping information is stored. Defaults to :file:`d_damp`.

        scale : str
            Indicates whether to perform a linear or a double logarithmic plot.

            * ``LIN`` - Perform a linear plot. Default

            * ``LOG`` - Perform a double logarithmic plot.

        Notes
        -----

        .. _MDPLOT_notes:

        See Thin Film Analysis for more information on thin film analyses.
        """
        command = f"MDPLOT,{function},{dmpname},{scale}"
        return self.run(command, **kwargs)

    def mdamp(
        self,
        stloc: str = "",
        v1: str = "",
        v2: str = "",
        v3: str = "",
        v4: str = "",
        v5: str = "",
        v6: str = "",
        **kwargs,
    ):
        r"""Defines the damping ratios as a function of mode.

        Mechanical APDL Command: `MDAMP <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MDAMP.html>`_

        Parameters
        ----------
        stloc : str
            Starting location in table for entering data. For example, if ``STLOC`` = 1, data input in the
            ``V1`` field applies to the first constant in the table. If ``STLOC`` = 7, data input in the
            ``V1`` field applies to the seventh constant in the table, etc. Defaults to the last location
            filled + 1.

        v1 : str
            Data assigned to six locations starting with ``STLOC``. If a value is already in this location,
            it will be redefined. Blank values for ``V2`` to ``V6`` leave the corresponding previous value
            unchanged.

        v2 : str
            Data assigned to six locations starting with ``STLOC``. If a value is already in this location,
            it will be redefined. Blank values for ``V2`` to ``V6`` leave the corresponding previous value
            unchanged.

        v3 : str
            Data assigned to six locations starting with ``STLOC``. If a value is already in this location,
            it will be redefined. Blank values for ``V2`` to ``V6`` leave the corresponding previous value
            unchanged.

        v4 : str
            Data assigned to six locations starting with ``STLOC``. If a value is already in this location,
            it will be redefined. Blank values for ``V2`` to ``V6`` leave the corresponding previous value
            unchanged.

        v5 : str
            Data assigned to six locations starting with ``STLOC``. If a value is already in this location,
            it will be redefined. Blank values for ``V2`` to ``V6`` leave the corresponding previous value
            unchanged.

        v6 : str
            Data assigned to six locations starting with ``STLOC``. If a value is already in this location,
            it will be redefined. Blank values for ``V2`` to ``V6`` leave the corresponding previous value
            unchanged.

        Notes
        -----

        .. _MDAMP_notes:

        Defines the damping ratios as a function of mode. Table position corresponds to mode number. These
        ratios are added to the :ref:`dmprat` value, if defined. Use the :ref:`stat` command to list current
        values. This command applies to mode-superposition harmonic ( :ref:`antype`,HARMIC), mode-
        superposition linear transient dynamic ( :ref:`antype`,TRANS), and spectrum ( :ref:`antype`,SPECTR)
        analyses. Repeat the :ref:`mdamp` command for additional constants (10000 maximum).

        :ref:`mdamp` can also be defined in a substructure analysis that uses component mode synthesis. The
        damping ratios are added on the diagonal of the reduced damping matrix, as explained in `Component
        Mode Synthesis (CMS)
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_anproc6.html#eq39b62ffb-3890-471d-a79e-2d6096214d0b>`_

        This command is also valid in PREP7.
        """
        command = f"MDAMP,{stloc},{v1},{v2},{v3},{v4},{v5},{v6}"
        return self.run(command, **kwargs)

    def mxpand(
        self,
        nmode: str = "",
        freqb: str = "",
        freqe: str = "",
        elcalc: str = "",
        signif: str = "",
        msupkey: str = "",
        modeselmethod: str = "",
        engcalc: str = "",
        **kwargs,
    ):
        r"""Specifies modal or buckling analysis expansion options.

        Mechanical APDL Command: `MXPAND <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MXPAND.html>`_

        Parameters
        ----------
        nmode : str
            Number of modes or array name (enclosed in percent signs) to expand and write. If blank or ALL,
            expand and write all modes within the frequency range specified. If -1, do not expand and do not
            write modes to the results file during the analysis. If an array name is input, the array must
            contain 1 for the expanded modes and zero otherwise, where the array index corresponds to the
            mode number. To specify an array containing the individual modes to expand, enclose the array
            name in percent (%) signs (for example, :ref:`mxpand`,%arrname%). Use the :ref:`dim` command to
            define the array.

        freqb : str
            Beginning, or lower end, of frequency range of interest. If ``FREQB`` and ``FREQE`` are both
            blank, expand and write the number of modes specified without regard to the frequency range.
            Defaults to the entire range.

        freqe : str
            Ending, or upper end, of frequency range of interest.

        elcalc : str
            Element calculation key:

            * ``NO`` - Do not calculate element results, reaction forces, and energies (default).

            * ``YES`` - Calculate element results, reaction forces, energies, and the nodal degree of freedom
              solution.

        signif : str
            Expand only those modes whose significance level exceeds the ``SIGNIF`` threshold (only
            applicable when ``ModeSelMethod`` is defined).

            If ``ModeSelMethod`` = MODC, the significance level of a mode is defined as the mode coefficient
            divided by the maximum mode coefficient of all modes.

            If ``ModeSelMethod`` = EFFM, the significance level of a mode is defined as the modal effective
            mass, divided by the total mass.

            If ``ModeSelMethod`` = DDAM, the significance level of a mode is defined as the modal effective
            weight, divided by the total weight.

            Any mode whose significance level is less than ``SIGNIF`` is considered insignificant and is not
            expanded. The higher the ``SIGNIF`` threshold, the fewer the number of modes expanded.
            ``SIGNIF`` defaults to 0.001, except for the case of DDAM mode selection method where it
            defaults to 0.01. If ``SIGNIF`` is specified as 0.0, it is taken as 0.0.

        msupkey : str
            Element result superposition key:

            * ``NO`` - Do not write element results to the mode file :file:`Jobnamemode`.

            * ``YES`` - Write element result to the mode file for use in the expansion pass of a subsequent mode-
              superposition PSD, spectrum, transient, or harmonic analysis. This value is the default if all of
              the following conditions exist:

              * ``Elcalc`` = YES.

              * The mode shapes are normalized to the mass matrix.

              * ``FREQB`` and ``FREQE`` are blank or 0.0.

              * No superelement is defined.

        modeselmethod : str
            Methods for mode selection (not supported for complex eigensolvers):

            * ```` - No mode selection is performed (default).

            * ``EFFM`` - The mode selection is based on the modal effective masses.

            * ``MODC`` - The mode selection is based on the mode coefficients.

            * ``DDAM`` - The mode selection is based on DDAM procedure (see `Mode Selection Based on the DDAM
              Method <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STR_SMSUP.html#>`_

        engcalc : str
            Additional element energies calculation key:

            * ``NO`` - Do not calculate additional energies (default).

            * ``YES`` - Calculate average, amplitude, and peak values for the following: stiffness and kinetic
              energies, and damping energy.

        Notes
        -----

        .. _MXPAND_notes:

        Specifies the number of modes to expand and write over a frequency range for a modal (
        :ref:`antype`,MODAL) or buckling ( :ref:`antype`,BUCKLE) analysis. If used in SOLUTION, this command
        is valid only within the first load step.

        There is no limit on the number of expanded modes ( ``NMODE`` ). However, there is a limit on the
        maximum number of modes used via the :ref:`get`, MODE command, mode combinations, and the
        :ref:`mdamp` command.

        With ``MSUPkey`` = YES, the computed element results ( ``Elcalc`` = YES) are written to
        :file:`Jobname.mode` for use in subsequent downstream mode-superposition analyses, including
        harmonic, transient, and all spectrum analyses. This significantly reduces computation time for the
        combination or expansion passes. For limitations and available elemental results, see.

        The calculation of additional energies ( ``EngCalc`` = YES) is valid only for ``Method`` = DAMP on
        the :ref:`modopt` command and ``Method`` = QRDAMP with ``Cpxmod`` = CPLX on the :ref:`modopt`
        command.

        If a mode selection method ( ``ModeSelMethod`` ) is defined, only the selected modes will be
        expanded. See `Using Mode Selection
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STR_SMSUP.html#strModSelBasDD>`_

        For array input ( ``NMODE`` ), the array must be dimensioned to be the size of the number of modes
        extracted ( ``NMODE`` on the :ref:`modopt` command). A value of 1 in the array indicates the mode is
        to be expanded, and a value of 0 indicates not to expand the mode. For the DAMP modal solution, the
        modes are in pairs, so be sure to verify that both modes of a pair have the same value. (For
        example, if modes #3 and #4 are a pair, indices 3 and 4 in the array should have the same value, 0
        or 1.)

        For `linear perturbation
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/strlinpertother.html>`_ modal
        analyses, you must set both ``Elcalc`` and ``MSUPkey`` to YES so that the downstream stress
        expansion pass can produce a solution consistent with the linear or nonlinear base (static or full
        transient) analysis. The prestressed nonlinear element history (saved variables) is accessible only
        in the first and second phases of the linear perturbation. The downstream mode superposition
        analysis (such as MSUP or PSD) can only reuse the nonlinear information contained in the
        :file:`Jobname.mode` file that is generated in the linear perturbation.

        In a distributed-memory parallel (DMP) analysis, you must issue :ref:`mxpand` to specify the number
        of modes to expand when computing the modes and mode shapes. In a DMP run, :ref:`mxpand` cannot be
        issued in an expansion pass ( :ref:`expass` ).

        This command is also valid in PREP7.
        """
        command = f"MXPAND,{nmode},{freqb},{freqe},{elcalc},{signif},{msupkey},{modeselmethod},{engcalc}"
        return self.run(command, **kwargs)

    def modopt(
        self,
        method: str = "",
        nmode: str = "",
        freqb: str = "",
        freqe: str = "",
        cpxmod: str = "",
        nrmkey: str = "",
        modtype: str = "",
        blocksize: str = "",
        freqmod: str = "",
        **kwargs,
    ):
        r"""Specifies modal analysis options.

        Mechanical APDL Command: `MODOPT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MODOPT.html>`_

        Parameters
        ----------
        method : str
            Mode-extraction method to be used for the modal analysis.

            * ``LANB`` - Block Lanczos

            * ``LANPCG`` - PCG Lanczos

            * ``SNODE`` - Supernode modal solver

            * ``SUBSP`` - Subspace algorithm

            * ``UNSYM`` - Unsymmetric matrix

            * ``DAMP`` - Damped system

            * ``QRDAMP`` - Damped system using QR algorithm

        nmode : str
            The number of modes to extract. The value can depend on the value supplied for ``Method``. ``NMODE``
            has no default and must be specified. If ``Method`` = LANB, LANPCG, or SNODE, the number of modes
            that can be extracted can equal the DOFs in the model after the application of all boundary
            conditions.

            For ``Method`` = LANB, SUBSP and UNSYM, you can specify ``NMODE`` = ALL to extract all eigenvalues
            in a given frequency range. To use this option, you must also define the frequency range (that is, a
            ``FREQE`` value must be set).

            Recommendation:

            * When ``Method`` = LANPCG, ``NMODE`` should be less than 100 to be computationally efficient.
            * When ``Method`` = SNODE, ``NMODE`` should be greater than 100 for 2D plane or 3D shell/beam models
              and greater than 250 for 3D solid elements to be computationally efficient.

        freqb : str
            The beginning, or lower end, of the frequency range (or eigenvalue range if ``FREQMOD`` is
            specified) of interest.

            For ``Method`` = LANB, SUBSP, UNSYM, DAMP, and QRDAMP, ``FREQB`` also represents the first shift
            point for the eigenvalue iterations. For UNSYM and DAMP, the default = -1.0 For other methods,
            the default is calculated internally.

            Eigenvalue extraction is most accurate near the shift point. Multiple shift points are used
            internally in the LANB, SUBSP, UNSYM, and QRDAMP methods. For the LANB, LANPCG, SUBSP, UNSYM,
            DAMP, and QRDAMP methods with a positive ``FREQB`` value, eigenvalues are output beginning at
            the shift point and increase in magnitude. For the UNSYM and DAMP methods with a negative
            ``FREQB`` value, eigenvalues are output beginning at zero magnitude and increase.

            Choosing higher ``FREQB`` values with the LANPCG and SNODE methods may lead to inefficient
            solution times because these methods will find all eigenvalues between zero and ``FREQB`` before
            finding the requested modes between ``FREQB`` and ``FREQE``.

        freqe : str
            The ending, or upper end, of the frequency range (or eigenvalue range if ``FREQMOD`` is
            specified) of interest (in Hz). Default = 100 Hz when ``Method`` = SNODE. The default for all
            other methods is to calculate all modes, regardless of their maximum frequency.

            To maintain solution efficiency, do not set the ``FREQE`` value too high; for example, not
            higher than 5000 Hz for an industrial problem. The higher the ``FREQE`` value used for the SNODE
            method, the more accurate the solution and the more eigenvalues produced; however, the solution
            time also increases. For example, if ``FREQE`` is set to 1e8, it causes the underlying
            supernodal structures to find all possible eigenvalues of each group of supernodes, requiring
            excessive solution time. The accuracy of the SNODE solution is controlled by ``FREQE`` and by
            the ``RangeFact`` value on the :ref:`snoption` command.

        cpxmod : str
            Complex eigenmode key. (Valid only when ``Method`` = QRDAMP or ``Method`` = UNSYM).

            * ``AUTO`` - Determine automatically if the eigensolutions are real or complex and output them
              accordingly (default when ``Method`` = UNSYM). Not supported for ``Method`` = QRDAMP.

            * ``ON or CPLX`` - Calculate and output complex eigenmode shapes.

            * ``OFF or REAL`` - Do not calculate complex eigenmode shapes (default). This setting is required if
              a mode- superposition analysis is intended after the modal analysis for ``Method`` = QRDAMP.

        nrmkey : str
            Mode shape normalization key:

            * ``OFF`` - Normalize the mode shapes to the mass matrix (default). This option is invalid for
              damped modal cyclic symmetry ( ``Method`` = DAMP or QRDAMP with the :ref:`cyclic` command).

            * ``ON`` - Normalize the mode shapes to unity instead of to the mass matrix (default for damped
              modal cyclic symmetry [ ``Method`` = DAMP or QRDAMP with the :ref:`cyclic` command]).

              If a subsequent spectrum or mode-superposition analysis is planned, the mode shapes should be
              normalized to the mass matrix ( ``Nrmkey`` = OFF).

        modtype : str
            Type of modes calculated by the eigensolver. Only applicable to the unsymmetric eigensolver.

            * ```` - Right eigenmodes (default).

            * ``BOTH`` - Right and left eigenmodes. The left eigenmodes are written to :file:`Jobname.LMODE`.
              This option must be activated if a mode-superposition analysis is intended.

        blocksize : str
            The block vector size to be used with the Block Lanczos or Subspace eigensolver (used only when ``Method`` = LANB or SUBSP). ``BlockSize`` must be an integer value between 0 and 16. When BlockSize = zero or blank, the code decides the block size internally (normally, a value of 8 is used for LANB and a value of 6 is used for SUBSP). Typically, higher ``BlockSize`` values are more efficient under each of the following conditions:

            * When running in out-of-core mode and there is not enough physical memory to buffer all of the
              files written by the Block Lanczos or Subspace eigensolver (and thus, the time spent doing I/O is
              considerable).

            * Many modes are requested (>100).

            * Higher-order solid elements dominate the model.

            The memory usage only slightly increases as
             ``BlockSize`` is increased. It is recommended that you use a value divisible by 4 (4, 8, 12, or 16).

        freqmod : str
            The specified frequency when the solved eigenvalues are no longer frequencies (for example, the
            model has the Floquet periodic boundary condition). In a modal analysis, the Floquet periodic
            boundary condition (body load FPBC) is only valid for the acoustic elements ``FLUID30``,
            ``FLUID220``, and ``FLUID221``.

        Notes
        -----

        .. _MODOPT_notes:

        Specifies modal analysis ( :ref:`antype`,MODAL) options.

        Additional options for specific eigensolvers are controlled by these commands:

        * :ref:`snoption` specifies options for the Supernode (SNODE) eigensolver.

        * :ref:`subopt` specifies options for the Subspace (SUBSP) eigensolver.

        * :ref:`qrdopt` specifies options for the QRDAMP eigensolver.

        * :ref:`dampopt` specifies options for the damped (DAMP) eigensolver.

        * :ref:`lanboption` specifies options for the Block Lanczos (LANB) eigensolver. For more difficult
          modal problems, you can specify an alternative version of the Block Lanczos eigensolver (
          :ref:`lanboption`,, ALT1).

        If ``Method`` = LANPCG, Mechanical APDL automatically switches to the PCG solver internally for this
        modal
        analysis. You can further control the efficiency of the PCG solver with the :ref:`pcgopt` and
        :ref:`eqslv` commands.

        For models that involve a non-symmetric element stiffness matrix, as in the case of a contact
        element with frictional contact, the QRDAMP eigensolver ( :ref:`modopt`, QRDAMP) extracts modes in
        the modal subspace formed by the eigenmodes from the symmetrized eigenproblem. The QRDAMP
        eigensolver symmetrizes the element stiffness matrix on the first pass of the eigensolution, and in
        the second pass, eigenmodes are extracted in the modal subspace of the first eigensolution pass. For
        such non-symmetric eigenproblems, you should verify the eigenvalue and eigenmode results using the
        non-symmetric matrix eigensolver ( :ref:`modopt`,UNSYM).

        The DAMP and QRDAMP options cannot be followed by a subsequent spectrum analysis. The UNSYM method
        supports spectrum analysis when eigensolutions are real.

        In a modal analysis, the Floquet periodic boundary condition (body load FPBC) is only valid for the
        acoustic elements ``FLUID30``, ``FLUID220``, and ``FLUID221``.

        For more details about mode shape normalization, see `Description of Analysis for Symmetric Undamped
        Systems
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_anproc3.html#eq1a4e68e0-62f4-4fec-a234-4ec054188490>`_

        This command is also valid in PREP7.

        Distributed-Memory Parallel (DMP) Restriction All extraction methods are supported in a DMP
        solution. Block Lanczos, PCG Lanczos, SUBSP, UNSYM,
        DAMP, and QRDAMP are distributed eigensolvers that run a fully distributed solution. However, the
        Supernode eigensolver is not a distributed eigensolver; therefore, you will not see the full
        performance improvements with this method that you would with a fully distributed solution.

        .. _MODOPT_extranote1:

        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.
        """
        command = f"MODOPT,{method},{nmode},{freqb},{freqe},{cpxmod},{nrmkey},{modtype},{blocksize},,,,{freqmod}"
        return self.run(command, **kwargs)

    def mcfopt(
        self,
        format_: int | str = "",
        type_: int | str = "",
        norm: int | str = "",
        **kwargs,
    ):
        r"""Specifies options for the Modal Coordinates File ( :file:`Jobname.mcf` ).

        Mechanical APDL Command: `MCFOPT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MCFOPT.html>`_

        Parameters
        ----------
        format_ : int or str
            :file:`Jobname.mcf` file format:

            * ``0`` - ASCII with wrap for more than 25 values (harmonic analysis) or 50 values (transient
              analysis) (default).

            * ``1`` - ASCII.

        type_ : int or str
            Output form of the complex modal coordinates - Only supported for ``Format`` = 1:

            * ``0`` - Real and imaginary parts (default).

            * ``1`` - Amplitude and phase angle in degree.

        norm : int or str
            Mode shape normalization for the calculation of the modal coordinates - Only supported for ``Format`` = 1:

            * ``0`` - The modes are mass normalized (default).

            * ``1`` - The modes are normalized to unity.

        Notes
        -----

        .. _MCFOPT_notes:

        Options specified with :ref:`mcfopt` are processed when a request is made to write the
        ``Jobname.mcf`` file by issuing :ref:`trnopt` or :ref:`hropt` with ``MCFwrite`` = ON.

        If you specify normalized to unity for the modal coordinates ( ``Norm`` = 1), the generalized mass
        must be available (see ). Note that this option is independent from the normalization of the modes
        specified during the modal analysis ( ``NrmKey`` on :ref:`modopt` command).
        """
        command = f"MCFOPT,{format_},{type_},{norm}"
        return self.run(command, **kwargs)

    def modcont(
        self, mlskey: str = "", enforcedkey: str = "", fastlv: str = "", **kwargs
    ):
        r"""Specify additional modal analysis options.

        Mechanical APDL Command: `MODCONT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MODCONT.html>`_

        Parameters
        ----------
        mlskey : str
            Multiple load step key:

            * ``OFF`` - Perform the modal analysis (compute the eigenvalues and the load vector) for each load
              step. (default)

            * ``ON`` - Perform the modal analysis (compute the eigenvalues and the load vector) only for the
              first load step; form the load vector for each subsequent load step (without repeating the
              eigenvalue calculations) and write all load vectors to the :file:`Jobname.MODE` file for downstream
              mode- superposition analyses.

        enforcedkey : str
            Enforced motion key:

            * ``OFF`` - Do not calculate enforced static modes. (default)

            * ``ON`` - Calculate enforced static modes and write them to the :file:`Jobname.MODE` file.

        fastlv : str
            Fast load vector generation key; valid only when ``MLSkey`` = ON:

            * ``OFF`` - Do not activate fast load vector generation (default).

            * ``ON`` - Activate fast load vector generation. This option is only supported when each load vector
              is based on a unique element surface load ( :ref:`sfe` ) applied on one element, and the element
              result superposition key is activated ( ``MSUPkey`` = YES on :ref:`mxpand` ).

        Notes
        -----

        .. _MODCONT_notes:

        Specifies additional modal analysis ( :ref:`antype`,MODAL) options.

        Use the :ref:`lvscale` command to apply the desired load in a mode-superposition transient or
        harmonic analysis.

        When ``MSUPkey`` = YES on the :ref:`mxpand` command, the maximum number of load vectors allowed in
        the :file:`Jobname.MODE` file defaults to 1000. To increase this limit, use the command
        :ref:`config`,NUMLV. When ``FastLV`` = ON, the limit is automatically set to 1x10 :sup:`6` and
        cannot be changed.

        The maximum number of load vectors that can be used in the downstream mode-superposition transient
        or harmonic analysis is the number of load vectors written in the :file:`Jobname.MODE` file.

        `Generation of multiple loads
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STR_SMSUP.html#>`_ (
        ``MLSkey`` = ON) is supported by the Block Lanczos, PCG Lanczos, Supernode, Subspace, Unsymmetric,
        and QRDAMP mode extraction methods.

        The `enforced motion calculation
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STR_SMSUP.html#>`_ (
        ``EnforcedKey`` = ON) is supported by the Block Lanczos, Supernode, Subspace, and QRDAMP mode
        extraction methods.
        """
        command = f"MODCONT,{mlskey},{enforcedkey},,{fastlv}"
        return self.run(command, **kwargs)

    def modseloption(
        self,
        dir1: str = "",
        dir2: str = "",
        dir3: str = "",
        dir4: str = "",
        dir5: str = "",
        dir6: str = "",
        **kwargs,
    ):
        r"""Specifies the criteria for selecting the modes to be expanded.

        Mechanical APDL Command: `MODSELOPTION <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MODSELOPTION.html>`_

        Parameters
        ----------
        dir1 : str
            Selection of the direction to be expanded.

            For ``ModeSelMethod`` = EFFM on the :ref:`mxpand` command, the directions correspond to the
            global Cartesian directions, i.e. 1=X, 2=Y, 3=Z, 4=ROTX, 5=ROTY, and 6=ROTZ. If ``dir1`` = YES,
            then any mode in this direction is expanded if its modal effective mass divided by the total
            mass (modal effective mass ratio) is greater than ``SIGNIF`` on the :ref:`mxpand` command. If
            ``dir1`` =NO, then the specified direction is not considered as a criterion for expansion. If
            ``dir1`` is given a numerical decimal value, modes in that direction are selected (starting from
            the ones with the largest modal effective mass ratios to the smallest) until the sum of their
            modal effective mass ratio equals this requested threshold.

            For ``ModeSelMethod`` = MODC on the :ref:`mxpand` command, ``dir1`` corresponds to the first
            input spectrum, ``dir2`` to the second, etc. (i.e. for multiple spectrum inputs; the actual
            directions correspond to their respective SED directions). If ``dir1`` =YES, then any mode in
            this spectrum is expanded if its mode coefficient divided by the largest mode coefficient is
            greater than SIGNIF on the :ref:`mxpand` command. If ``dir1`` =NO, then the specified direction
            is not considered as a criterion for expansion.

        dir2 : str
            Selection of the direction to be expanded.

            For ``ModeSelMethod`` = EFFM on the :ref:`mxpand` command, the directions correspond to the
            global Cartesian directions, i.e. 1=X, 2=Y, 3=Z, 4=ROTX, 5=ROTY, and 6=ROTZ. If ``dir1`` = YES,
            then any mode in this direction is expanded if its modal effective mass divided by the total
            mass (modal effective mass ratio) is greater than ``SIGNIF`` on the :ref:`mxpand` command. If
            ``dir1`` =NO, then the specified direction is not considered as a criterion for expansion. If
            ``dir1`` is given a numerical decimal value, modes in that direction are selected (starting from
            the ones with the largest modal effective mass ratios to the smallest) until the sum of their
            modal effective mass ratio equals this requested threshold.

            For ``ModeSelMethod`` = MODC on the :ref:`mxpand` command, ``dir1`` corresponds to the first
            input spectrum, ``dir2`` to the second, etc. (i.e. for multiple spectrum inputs; the actual
            directions correspond to their respective SED directions). If ``dir1`` =YES, then any mode in
            this spectrum is expanded if its mode coefficient divided by the largest mode coefficient is
            greater than SIGNIF on the :ref:`mxpand` command. If ``dir1`` =NO, then the specified direction
            is not considered as a criterion for expansion.

        dir3 : str
            Selection of the direction to be expanded.

            For ``ModeSelMethod`` = EFFM on the :ref:`mxpand` command, the directions correspond to the
            global Cartesian directions, i.e. 1=X, 2=Y, 3=Z, 4=ROTX, 5=ROTY, and 6=ROTZ. If ``dir1`` = YES,
            then any mode in this direction is expanded if its modal effective mass divided by the total
            mass (modal effective mass ratio) is greater than ``SIGNIF`` on the :ref:`mxpand` command. If
            ``dir1`` =NO, then the specified direction is not considered as a criterion for expansion. If
            ``dir1`` is given a numerical decimal value, modes in that direction are selected (starting from
            the ones with the largest modal effective mass ratios to the smallest) until the sum of their
            modal effective mass ratio equals this requested threshold.

            For ``ModeSelMethod`` = MODC on the :ref:`mxpand` command, ``dir1`` corresponds to the first
            input spectrum, ``dir2`` to the second, etc. (i.e. for multiple spectrum inputs; the actual
            directions correspond to their respective SED directions). If ``dir1`` =YES, then any mode in
            this spectrum is expanded if its mode coefficient divided by the largest mode coefficient is
            greater than SIGNIF on the :ref:`mxpand` command. If ``dir1`` =NO, then the specified direction
            is not considered as a criterion for expansion.

        dir4 : str
            Selection of the direction to be expanded.

            For ``ModeSelMethod`` = EFFM on the :ref:`mxpand` command, the directions correspond to the
            global Cartesian directions, i.e. 1=X, 2=Y, 3=Z, 4=ROTX, 5=ROTY, and 6=ROTZ. If ``dir1`` = YES,
            then any mode in this direction is expanded if its modal effective mass divided by the total
            mass (modal effective mass ratio) is greater than ``SIGNIF`` on the :ref:`mxpand` command. If
            ``dir1`` =NO, then the specified direction is not considered as a criterion for expansion. If
            ``dir1`` is given a numerical decimal value, modes in that direction are selected (starting from
            the ones with the largest modal effective mass ratios to the smallest) until the sum of their
            modal effective mass ratio equals this requested threshold.

            For ``ModeSelMethod`` = MODC on the :ref:`mxpand` command, ``dir1`` corresponds to the first
            input spectrum, ``dir2`` to the second, etc. (i.e. for multiple spectrum inputs; the actual
            directions correspond to their respective SED directions). If ``dir1`` =YES, then any mode in
            this spectrum is expanded if its mode coefficient divided by the largest mode coefficient is
            greater than SIGNIF on the :ref:`mxpand` command. If ``dir1`` =NO, then the specified direction
            is not considered as a criterion for expansion.

        dir5 : str
            Selection of the direction to be expanded.

            For ``ModeSelMethod`` = EFFM on the :ref:`mxpand` command, the directions correspond to the
            global Cartesian directions, i.e. 1=X, 2=Y, 3=Z, 4=ROTX, 5=ROTY, and 6=ROTZ. If ``dir1`` = YES,
            then any mode in this direction is expanded if its modal effective mass divided by the total
            mass (modal effective mass ratio) is greater than ``SIGNIF`` on the :ref:`mxpand` command. If
            ``dir1`` =NO, then the specified direction is not considered as a criterion for expansion. If
            ``dir1`` is given a numerical decimal value, modes in that direction are selected (starting from
            the ones with the largest modal effective mass ratios to the smallest) until the sum of their
            modal effective mass ratio equals this requested threshold.

            For ``ModeSelMethod`` = MODC on the :ref:`mxpand` command, ``dir1`` corresponds to the first
            input spectrum, ``dir2`` to the second, etc. (i.e. for multiple spectrum inputs; the actual
            directions correspond to their respective SED directions). If ``dir1`` =YES, then any mode in
            this spectrum is expanded if its mode coefficient divided by the largest mode coefficient is
            greater than SIGNIF on the :ref:`mxpand` command. If ``dir1`` =NO, then the specified direction
            is not considered as a criterion for expansion.

        dir6 : str
            Selection of the direction to be expanded.

            For ``ModeSelMethod`` = EFFM on the :ref:`mxpand` command, the directions correspond to the
            global Cartesian directions, i.e. 1=X, 2=Y, 3=Z, 4=ROTX, 5=ROTY, and 6=ROTZ. If ``dir1`` = YES,
            then any mode in this direction is expanded if its modal effective mass divided by the total
            mass (modal effective mass ratio) is greater than ``SIGNIF`` on the :ref:`mxpand` command. If
            ``dir1`` =NO, then the specified direction is not considered as a criterion for expansion. If
            ``dir1`` is given a numerical decimal value, modes in that direction are selected (starting from
            the ones with the largest modal effective mass ratios to the smallest) until the sum of their
            modal effective mass ratio equals this requested threshold.

            For ``ModeSelMethod`` = MODC on the :ref:`mxpand` command, ``dir1`` corresponds to the first
            input spectrum, ``dir2`` to the second, etc. (i.e. for multiple spectrum inputs; the actual
            directions correspond to their respective SED directions). If ``dir1`` =YES, then any mode in
            this spectrum is expanded if its mode coefficient divided by the largest mode coefficient is
            greater than SIGNIF on the :ref:`mxpand` command. If ``dir1`` =NO, then the specified direction
            is not considered as a criterion for expansion.

        Notes
        -----

        .. _MODSELOPTION_notes:

        This command is only applicable when a mode selection method is defined ( ``ModeSelMethod`` on the
        :ref:`mxpand` command). See `Using Mode Selection
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STR_SMSUP.html#strModSelBasDD>`_

        If a numerical value is specified for a direction, the significance threshold (SIGNIF on the
        :ref:`mxpand` command) is ignored for the selection of the modes in this direction.

        If a mode is determined to be expanded in **any** of the 6 directions, it will be expanded in the
        :file:`.MODE` file. Otherwise, the mode will not be expanded.

        The default behavior is to consider all directions for expansion.

        For ``ModeSelMethod`` = EFFM on the :ref:`mxpand` command, ``dir4``, ``dir5``, and ``dir6`` are not
        considered if mass related information have been calculated using the lumped approximation instead
        of the precise calculation (See `Mass Related Information
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/ans_thry_MRI.html#bob121>`_
        """
        command = f"MODSELOPTION,{dir1},{dir2},{dir3},{dir4},{dir5},{dir6}"
        return self.run(command, **kwargs)

    def tintp(
        self,
        gamma: str = "",
        alpha: str = "",
        delta: str = "",
        theta: str = "",
        oslm: str = "",
        tol: str = "",
        avsmooth: int | str = "",
        alphaf: str = "",
        alpham: str = "",
        **kwargs,
    ):
        r"""Defines transient integration parameters.

        Mechanical APDL Command: `TINTP <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_TINTP.html>`_

        Parameters
        ----------
        gamma : str
            Amplitude decay factor for 2nd order transient integration, for example, structural dynamics (used
            only if ``ALPHA``, ``DELTA``, ``ALPHAF``, and ``ALPHAM`` are blank). Defaults to 0.005.

            Alternatively, you can input the application type for the analysis using one of the following
            labels. In this case, the program automatically sets the transient dynamic solver algorithm and
            settings based on the intended application. For more information, see.

            * ``IMPA`` - Impact application.

            * ``HISP`` - High speed dynamic application.

            * ``MOSP`` - Moderate speed dynamic application.

            * ``LOSP`` - Low speed dynamic application.

            * ``QUAS`` - Quasi-static application.

        alpha : str
            2nd order transient integration parameter (used only if ``GAMMA`` is blank). Defaults to 0.2525.

        delta : str
            2nd order transient integration parameter (used only if ``GAMMA`` is blank). Defaults to 0.5050.

        theta : str
            1st order transient (for example, thermal transient) integration parameter. Defaults to 1.0

        oslm : str
            Specifies the oscillation limit criterion for automatic time stepping of 1st order transients
            (for example, thermal transients). Defaults to 0.5 with a tolerance of ``TOL``.

        tol : str
            Tolerance applied to ``OSLM``. Defaults to 0.0.

        avsmooth : int or str
            Smoothing flag option:

            * ``0`` - Include smoothing of the velocity (1st order system) or the acceleration (2nd order
              system) (default).

            * ``1`` - Do not include smoothing.

        alphaf : str
            Interpolation factor in HHT algorithm for force and damping terms (used only if ``GAMMA`` is
            blank). Defaults to 0.005.

        alpham : str
            Interpolation factor in HHT algorithm for inertial term (used only if ``GAMMA`` is blank).
            Defaults to 0.0.

        Notes
        -----

        .. _TINTP_notes:

        Used to define the transient integration parameters. For more information on transient integration
        parameters, refer to `Transient Analysis
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_anproc2.html#anpdescp1order>`_

        For structural transient analyses, you may choose between the Newmark and HHT time integration
        methods (see the :ref:`trnopt` command). In this case, if ``GAMMA`` is input and the integration
        parameters ``ALPHA``, ``DELTA``, ``ALPHAF``, and ``ALPHAM`` are left blank, the program will
        calculate the integration parameters. Alternatively, you can input these integration parameters
        directly on this command. However, for the unconditional stability and second order accuracy of the
        time integration, these parameters should satisfy a specific relationship, as described in
        `Description of Structural and Other Second Order Systems
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_anproc2.html#anpsolu>`_

        This command is also valid in PREP7.
        """
        command = f"TINTP,{gamma},{alpha},{delta},{theta},{oslm},{tol},,,{avsmooth},{alphaf},{alpham}"
        return self.run(command, **kwargs)

    def trnopt(
        self,
        method: str = "",
        maxmode: str = "",
        initialacc: str = "",
        minmode: str = "",
        mcfwrite: str = "",
        tintopt: str = "",
        vaout: str = "",
        dmpsfreq: str = "",
        engcalc: str = "",
        mckey: str = "",
        **kwargs,
    ):
        r"""Specifies transient analysis options.

        Mechanical APDL Command: `TRNOPT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_TRNOPT.html>`_

        Parameters
        ----------
        method : str
            Solution method for the transient analysis:

            * ``FULL`` - Full method (default).

            * ``MSUP`` - Mode-superposition method.

        maxmode : str
            Largest mode number to be used to calculate the response (for ``Method`` = MSUP). Defaults to
            the highest mode calculated in the preceding modal analysis.

        initialacc : str
            Key to activate calculation of initial acceleration:

            * ``(blank)`` - Initial accelerations are not calculated (default).

            * ``INIL`` - Calculate initial acceleration for a full transient analysis using the lumped mass
              matrix.

        minmode : str
            Smallest mode number to be used (for ``Method`` = MSUP). Defaults to 1.

        mcfwrite : str
            Modal coordinates output key to the :file:`Jobname.mcf` file (valid only for the mode-superposition
            method). To control how :file:`Jobname.mcf` is written, specify options on the :ref:`mcfopt`
            command.

            * ``NO`` - Modal coordinates are not written to :file:`Jobnamemcf`.

            * ``YES`` - Modal coordinates are written to the text file :file:`Jobname.mcf` (default).

        tintopt : str
            `Time integration method
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_anproc2.html#anpsolu>`_ for the
            transient analysis:

            * ``NMK or 0`` - Newmark algorithm (default).

            * ``HHT or 1`` - HHT algorithm (valid only for the full transient method).

        vaout : str
            Velocities and accelerations output key (valid only for `mode-superpositiontransient analysis
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STR5_10.html#a4iQxq2c8mcm>`_
            ):

            * ``NO`` - No output of velocities and accelerations (default).

            * ``YES`` - Write velocities and accelerations to the reduced displacement file,
              :file:`Jobnamerdsp`.

        dmpsfreq : str
            Average excitation frequency (Hz) for the calculation of equivalent viscous damping from
            structural damping input ( :ref:`dmpstr` and :ref:`mp`,DMPS). See `Damping
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STR1D.html#strelemdamp>`_
            ``DMPSFreqTab`` on :ref:`dmpstr` ), it supersedes this value.

        engcalc : str
            Additional element energies calculation key:

            * ``NO`` - Do not calculate additional element energies (default).

            * ``YES`` - Calculate damping energy and work done by external loads.

        mckey : str
            Modal coordinates output key to the :file:`.rdsp` file (valid only for the mode-superposition
            method):

            * ``AUTO`` - Writing depends on the modal analysis settings of the :ref:`mxpand` command (default).

            * ``YES`` - Always write the modal coordinates to the file :file:`Jobname.rdsp`. A subsequent
              expansion pass ( :ref:`expass` ) is not supported.

        Notes
        -----

        .. _TRNOPT_notes:

        Specifies transient analysis ( :ref:`antype`,TRANS) options. If used in SOLUTION, this command is
        valid only within the first load step. Use the :ref:`tintp` command to set transient integration
        parameters.

        To include `residual vectors
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STR_SMSUP.html#ans_str_moda_resresp>`_
        in your `mode-superposition transient
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STR5_10.html#a4iQxq2c8mcm>`_
        analysis ( ``Method`` = MSUP), specify :ref:`resvec`,ON.

        For ``Method`` = MSUP, ``MAXMODE`` and ``MINMODE`` are ignored after a modal restart analysis where
        remote modal files usage ( :ref:`moddir` ) and residual vector calculation ( :ref:`resvec`,ON) have
        been activated.

        ``Method`` = MSUP is not available for ocean loading.

        By default in a mode-superposition transient analysis, reaction force and other force output
        contains only static contributions. If you want to postprocess the velocities, accelerations, and
        derived results ( ``Lab`` = TOTAL, DAMP, or INERT on the :ref:`force` command), set ``VAout`` = YES
        to activate velocity and acceleration output.

        The calculation of additional energies ( ``EngCalc`` = YES) is valid only for the full solution
        method ( ``Method`` = FULL). The :file:`Jobname.ESAV` file is always saved in this case. The
        numerical integration for damping energy and work are consistent only if solution data are written
        to the database for every substep ( :ref:`outres`,ALL,ALL, :ref:`outres`,ESOL,ALL, or
        :ref:`outres`,VENG, ALL). For more information, see `Damping Energy
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_tool16.html#>`_  `Work Done by
        External Loads <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_tool16.html#>`_

        This command is also valid in PREP7.

        .. _TRNOPT_extranote1:

        Additional product restrictions for the :ref:`trnopt` command are shown in the table below.

        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.
        """
        command = f"TRNOPT,{method},{maxmode},{initialacc},{minmode},{mcfwrite},{tintopt},{vaout},{dmpsfreq},{engcalc},{mckey}"
        return self.run(command, **kwargs)

    def timint(self, key: str = "", lab: str = "", **kwargs):
        r"""Turns on transient effects.

        Mechanical APDL Command: `TIMINT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_TIMINT.html>`_

        Parameters
        ----------
        key : str
            Transient effects key:

            * ``OFF`` - No transient effects (static or steady-state).

            * ``ON`` - Include transient (mass or inertia) effects.

        lab : str
            Degree of freedom label:

            * ``ALL`` - Apply this key to all appropriate labels (default).

            * ``STRUC`` - Apply this key to structural DOFs.

            * ``THERM`` - Apply this key to thermal DOFs.

            * ``ELECT`` - Apply this key to electric DOFs.

            * ``MAG`` - Apply this key to magnetic DOFs.

            * ``FLUID`` - Apply this key to fluid DOFs.

            * ``DIFFU`` - Apply this key to concentration of DOFs.

        Notes
        -----

        .. _TIMINT_notes:

        Indicates whether this load step in a full transient analysis should use time integration, that is,
        whether it includes transient effects (e.g. structural inertia, thermal capacitance) or whether it
        is a static (steady-state) load step for the indicated DOFs. Transient initial conditions are
        introduced at the load step having ``Key`` = ON. Initial conditions are then determined from the
        previous two substeps. Zero initial velocity and acceleration are assumed if no previous substeps
        exist. See the `Structural Analysis Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/str_enercalc_app.html>`_, the
        `Thermal Analysis Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_the/Hlp_G_THE4.html>`_, and the `Low-
        Frequency Electromagnetic Analysis Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_lof/Hlp_G_ELE16.html>`_ for details.

        This command is also valid in PREP7.
        """
        command = f"TIMINT,{key},{lab}"
        return self.run(command, **kwargs)

    def rigid(
        self,
        dof1: str = "",
        dof2: str = "",
        dof3: str = "",
        dof4: str = "",
        dof5: str = "",
        dof6: str = "",
        **kwargs,
    ):
        r"""Specifies known rigid body modes (if any) of the model.

        Mechanical APDL Command: `RIGID <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_RIGID.html>`_

        Parameters
        ----------
        dof1 : str
            Up to six global Cartesian directions of the rigid modes. For a completely free 2D model, use
            ALL or UX, UY, ROTZ. For a completely free 3D model, use ALL or UX, UY, UZ, ROTX, ROTY, ROTZ.
            For a constrained model, use UX, UY, UZ, ROTX, ROTY, or ROTZ, as appropriate, to specify each
            and every unconstrained direction which exists in the model (not specifying every direction may
            cause difficulties in extracting the modes).

        dof2 : str
            Up to six global Cartesian directions of the rigid modes. For a completely free 2D model, use
            ALL or UX, UY, ROTZ. For a completely free 3D model, use ALL or UX, UY, UZ, ROTX, ROTY, ROTZ.
            For a constrained model, use UX, UY, UZ, ROTX, ROTY, or ROTZ, as appropriate, to specify each
            and every unconstrained direction which exists in the model (not specifying every direction may
            cause difficulties in extracting the modes).

        dof3 : str
            Up to six global Cartesian directions of the rigid modes. For a completely free 2D model, use
            ALL or UX, UY, ROTZ. For a completely free 3D model, use ALL or UX, UY, UZ, ROTX, ROTY, ROTZ.
            For a constrained model, use UX, UY, UZ, ROTX, ROTY, or ROTZ, as appropriate, to specify each
            and every unconstrained direction which exists in the model (not specifying every direction may
            cause difficulties in extracting the modes).

        dof4 : str
            Up to six global Cartesian directions of the rigid modes. For a completely free 2D model, use
            ALL or UX, UY, ROTZ. For a completely free 3D model, use ALL or UX, UY, UZ, ROTX, ROTY, ROTZ.
            For a constrained model, use UX, UY, UZ, ROTX, ROTY, or ROTZ, as appropriate, to specify each
            and every unconstrained direction which exists in the model (not specifying every direction may
            cause difficulties in extracting the modes).

        dof5 : str
            Up to six global Cartesian directions of the rigid modes. For a completely free 2D model, use
            ALL or UX, UY, ROTZ. For a completely free 3D model, use ALL or UX, UY, UZ, ROTX, ROTY, ROTZ.
            For a constrained model, use UX, UY, UZ, ROTX, ROTY, or ROTZ, as appropriate, to specify each
            and every unconstrained direction which exists in the model (not specifying every direction may
            cause difficulties in extracting the modes).

        dof6 : str
            Up to six global Cartesian directions of the rigid modes. For a completely free 2D model, use
            ALL or UX, UY, ROTZ. For a completely free 3D model, use ALL or UX, UY, UZ, ROTX, ROTY, ROTZ.
            For a constrained model, use UX, UY, UZ, ROTX, ROTY, or ROTZ, as appropriate, to specify each
            and every unconstrained direction which exists in the model (not specifying every direction may
            cause difficulties in extracting the modes).

        Notes
        -----

        .. _RIGID_notes:

        Specifies known rigid body modes (if any) of the model. This command applies only to a component
        mode synthesis (CMS) analysis (see the :ref:`cmsopt` command). Any rigid body modes specified must
        be permitted by the applied displacement constraints (that is, do not specify a rigid body mode in a
        constrained direction). Reissue the command to redefine the specification. If used in SOLUTION, this
        command is valid only within the first load step.

        This command is also valid in PREP7. Distributed-Memory Parallel (DMP) Restriction This command is
        not supported in a DMP solution.
        """
        command = f"RIGID,{dof1},{dof2},{dof3},{dof4},{dof5},{dof6}"
        return self.run(command, **kwargs)

    def hropt(
        self,
        method: str = "",
        value1: str = "",
        value2: str = "",
        value3: str = "",
        value4: str = "",
        value5: str = "",
        **kwargs,
    ):
        r"""Specifies harmonic analysis options.

        Mechanical APDL Command: `HROPT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_HROPT.html>`_

        Parameters
        ----------
        method : str
            Solution method for the harmonic analysis:

            * ``AUTO`` - Automatically select the most efficient method (default). Either the full method (FULL)
              or the frequency-sweep method (VT) is selected, depending on the model. For ``Method`` = AUTO,
              ``Value1``.. ``Value5`` are unused fields.

            * ``FULL`` - Full method. For ``Method`` = AUTO, ``Value1``.. ``Value5`` are unused fields.

            * ``MSUP`` - Mode-superposition method. See :ref:`HROPT_MSUP`.

            * ``VT`` - Frequency-sweep (Variational Technology) method (based on the FULL harmonic algorithm). See
              :ref:`HROPT_VT_VTPA`.

            * ``VTPA`` - Frequency-sweep (Variational Technology) perfect absorber method (based on the FULL harmonic
              algorithm). See :ref:`HROPT_VT_VTPA`.

            * ``KRYLOV`` - Frequency-sweep Krylov method. See :ref:`HROPT_KRYLOV`.

              The Krylov approximation can be run using macros as customizable templates as described in.
              Alternatively, you can perform a Krylov solution without customization as described in `Krylov
              Method Implemented using Mechanical APDL Commands
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/str_Krysweep.html#str_kryClist>`_

            If the solution method is not specified, the program automatically selects either the Full method or
            the frequency-sweep method, depending on which method is most efficient for the model. The
            frequency-sweep method uses the underlying Variational Technology method.

        value1 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_HROPT.html>`_ for further
            information.

        value2 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_HROPT.html>`_ for further
            information.

        value3 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_HROPT.html>`_ for further
            information.

        value4 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_HROPT.html>`_ for further
            information.

        value5 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_HROPT.html>`_ for further
            information.

        Notes
        -----

        .. warning::

           This function contains specificities regarding the argument definitions.
           Please refer to the `command documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_HROPT.html>`_
           for further explanations.

        .. _HROPT_notes:

        Specifies the method of solution for a harmonic analysis ( :ref:`antype`,HARMIC).

        If used in SOLUTION, this command is valid only within the first load step.

        This command is also valid in PREP7.

        **For** ``Method`` = MSUP:

        * For cyclic symmetry mode-superposition harmonic solutions, ``MAXMODE`` and ``MINMODE`` are
          ignored.

        * To include `residual vectors
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STR_SMSUP.html#ans_str_moda_resresp>`_
          in your `mode-superposition harmonic analysis
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STR4_MODESUPER.html#aMhQxq6emcm>`_,
          specify :ref:`resvec`,ON.
        * ``MAXMODE`` and ``MINMODE`` are ignored after a modal restart analysis where remote modal files
          usage ( :ref:`moddir` ) and residual vector calculation ( :ref:`resvec`,ON) have been activated.
        """
        command = f"HROPT,{method},{value1},{value2},{value3},{value4},{value5}"
        return self.run(command, **kwargs)

    def hrocean(self, type_: str = "", nphase: str = "", **kwargs):
        r"""Perform the harmonic ocean wave procedure (HOWP).

        Mechanical APDL Command: `HROCEAN <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_HROCEAN.html>`_

        Parameters
        ----------
        type_ : str
            Specifies how to include ocean wave information in a harmonic analysis:

            * ``HARMONIC`` - Performs a harmonic analysis using both real and imaginary load vectors calculated
              via the `harmonic oceanwave procedure (HOWP)
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_anproc4.html#eq63629e12-76f7-4f52-97a7-ce8593b3f24e>`_.
              This behavior is the default. This option performs a harmonic analysis running at a frequency
              determined by the wave period (specified via :ref:`octable` command input).

            * ``STATIC`` - Performs a static analysis using both real and imaginary load vectors (calculated via
              HOWP). This option works by performing a harmonic analysis running at a frequency of 0.0.

            * ``OFF`` - Deactivates a previously activated HOWP and performs a standard harmonic analysis.

        nphase : str
            Positive number specifying the number of phases to calculate forces. This value must be at least
            8. The default value is 20.

        Notes
        -----

        .. _HROCEAN_notes:

        The :ref:`hrocean` command applies ocean wave information (obtained via the :ref:`ocdata` and
        :ref:`octable` commands) in a harmonic analysis ( :ref:`antype`,HARMIC) as real and imaginary
        forces.

        You can apply only one ocean load at a time.

        The applied frequency in the harmonic ( ``Type`` = HARMONIC) analysis is based on the wave period
        input on the :ref:`octable` command (and not on :ref:`harfrq` command input, which cannot be used).
        Phase-shift input on the :ref:`octable` command is ignored.

        HOWP does not generate a damping matrix. If you require a damping matrix, you must add it
        separately.

        The command applies to regular wave types only (Airy with one wave component, Wheeler with one wave
        component, Stokes, and stream function). Irregular wave types are not supported. For information
        about wave types, see `Hydrodynamic Loads
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_et8.html#thy_dynpresshead>`_

        The program calculates the forces on each load component of each element at ``NPHASE`` solutions,
        spread evenly over one wave cycle. Then, the minimum and maximum, and the phase between them, are
        calculated. The command uses the resulting information to generate the real and imaginary loads.

        HOWP cannot be used with stress stiffening.

        HOWP works with the full harmonic analysis method ( :ref:`hropt`,FULL) only.

        For more information, see `Harmonic Ocean Wave Procedure (HOWP)
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_anproc4.html#eq63629e12-76f7-4f52-97a7-ce8593b3f24e>`_

        This command is also valid in PREP7.
        """
        command = f"HROCEAN,{type_},{nphase}"
        return self.run(command, **kwargs)

    def harfrq(
        self,
        freqb: str = "",
        freqe: str = "",
        logopt: str = "",
        freqarr: str = "",
        toler: str = "",
        **kwargs,
    ):
        r"""Defines the frequency range in a harmonic analysis.

        Mechanical APDL Command: `HARFRQ <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_HARFRQ.html>`_

        Parameters
        ----------
        freqb : str
            Frequency (Hz) at the beginning of the ``FREQB`` to ``FREQE`` range (if ``FREQE`` > ``FREQB`` ).
            If ``FREQE`` is blank, the solution is done only at frequency ``FREQB`` (the central frequency
            of octave bands, when ``LogOpt`` = OB1, OB2, OB3, OB6, OB12 or OB24).

        freqe : str
            Frequency at end of this range. For non-logarithm spacing ( ``LogOpt`` is blank), solutions are
            done at an interval of ( ``FREQE`` - ``FREQB`` ) / ``NSBSTP``, ending at ``FREQE``, and no
            solution is done at the beginning of the frequency range, ``FREQB``. ``NSBSTP`` is input via the
            :ref:`nsubst` command. See the :ref:`expsol` command documentation for expansion pass solutions.

        logopt : str
            Logarithm frequency span. Solutions are done at an interval of (log( ``FREQE`` ) - log( ``FREQB`` ))
            / ( ``NSBSTP`` -1), ( ``NSBSTP`` >1). The central frequency or beginning frequency is used for
            ``NSBSTP`` = 1. Valid values are:

            * ``OB1`` - Octave band.

            * ``OB2`` - 1/2 octave band.

            * ``OB3`` - 1/3 octave band.

            * ``OB6`` - 1/6 octave band.

            * ``OB12`` - 1/12 octave band.

            * ``OB24`` - 1/24 octave band.

            * ``LOG`` - General logarithm frequency span.

        freqarr : str
            An array containing frequency values (Hz). Combined with the tolerance argument, ``Toler``,
            these values are merged with values calculated based on the specifications from ``FREQB``,
            ``FREQE``, and ``LogOpt``, as well ``NSBSTP`` on the :ref:`nsubst` command and ``Clust`` on the
            :ref:`hrout` command. Enclose the array name in percent (%) signs (for example,
            :ref:`harfrq`,,,,,%arrname%). Use :ref:`dim` to define the array.

        toler : str
            Tolerance to determine if a user input frequency value in ``FREQARR`` is a duplicate and can be
            ignored. Two frequency values are considered duplicates if their difference is less than the
            frequency range multiplied by the tolerance. The default value is 1 x 10 :sup:`-5`.

        Notes
        -----

        .. _HARFRQ_notes:

        Defines the frequency range for loads in the harmonic analysis ( :ref:`antype`,HARMIC).

        Do not use this command for a `harmonic ocean wave analysis
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_anproc4.html#eq63629e12-76f7-4f52-97a7-ce8593b3f24e>`_
        ( :ref:`hrocean` ).

        When frequencies are user-defined, the array ``FREQARR`` must be one-dimensional and contain
        positive values. User-defined frequency input is not supported when the `frequency-sweep
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/str_harmsweep.html#>`_ method is
        used ( :ref:`hropt`,VT ).

        This command is also valid in PREP7.
        """
        command = f"HARFRQ,{freqb},{freqe},,{logopt},{freqarr},{toler}"
        return self.run(command, **kwargs)

    def hrout(
        self,
        reimky: str = "",
        clust: str = "",
        mcont: str = "",
        engcalc: str = "",
        **kwargs,
    ):
        r"""Specifies the harmonic analysis output options.

        Mechanical APDL Command: `HROUT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_HROUT.html>`_

        Parameters
        ----------
        reimky : str
            Real/Imaginary print key:

            * ``ON`` - Print complex displacements as real and imaginary components (default).

            * ``OFF`` - Print complex displacements as amplitude and phase angle (degrees).

        clust : str
            Cluster option (for :ref:`hropt`,MSUP):

            * ``OFF`` - Uniform spacing of frequency solutions (default).

            * ``ON`` - Cluster frequency solutions about natural frequencies.

        mcont : str
            Mode contributions key (for :ref:`hropt`,MSUP):

            * ``OFF`` - No print of mode contributions at each frequency (default).

            * ``ON`` - Print mode contributions at each frequency.

        engcalc : str
            Additional element energies calculation key:

            * ``NO`` - Do not calculate additional energies (default).

            * ``YES`` - Calculate average, amplitude, and peak values for the following: stiffness and kinetic
              energies, damping energy, and work done by external loads.

        Notes
        -----

        .. _HROUT_notes:

        Specifies the harmonic analysis ( :ref:`antype`,HARMIC) output options. If used in SOLUTION, this
        command is valid only within the first load step. :ref:`outpr`,NSOL must be specified to print mode
        contributions at each frequency.

        If the calculation of additional energies is requested ( ``EngCalc`` = YES) in a mode-superposition
        harmonic analysis ( ``Method`` = MSUP on the :ref:`hropt` command), work done by external loads is
        not calculated if ``MSUPkey`` = YES on the :ref:`mxpand` command. If ``MSUPkey`` = NO, work due to
        element loads is calculated, but not work due to nodal loads.

        Only the ``Reimky`` argument is supported and applicable for frequency-sweep harmonic analyses using
        the `Krylov
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/str_Krysweep.html#str_Krylov_macros>`_
        or `Variational Technology
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/str_harmsweep.html#>`_ Methods. All
        other arguments are ignored if the :ref:`hropt` command has been issued with ``Method`` = KRYLOV,
        VT, or VTPA.

        This command is also valid in PREP7.
        """
        command = f"HROUT,{reimky},{clust},{mcont},{engcalc}"
        return self.run(command, **kwargs)

    def hrexp(self, angle: str = "", **kwargs):
        r"""Specifies the phase angle for the harmonic analysis expansion pass.

        Mechanical APDL Command: `HREXP <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_HREXP.html>`_

        Parameters
        ----------
        angle : str
            Phase angle (degrees) for expansion pass. If ALL (default), use both 0.0° (real) and 90.0°
            (imaginary) phase angles.

        Notes
        -----

        .. _HREXP_notes:

        Specifies the phase angle where the expansion pass will be done for a harmonic mode-superposition
        expansion pass.

        For a specific angle, the following real solution is stored in the results (\2.rst) file:

        { u } = { u max i cos ( ϕ i - φ ) }
        Where:

        i is the degree of freedom number.

        :math:``  is the amplitude of thei th degree of freedom solution

        Φ :sup:`i` is the phase shift angle of the i th degree of freedom solution

        ϕ is the supplied phase shift angle ( ``ANGLE`` )

        If ``ANGLE`` is ALL, both the real and imaginary parts of the solution are stored in the results
        file.

        For more details about the solution equations, see `Harmonic Analyses
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_anproc4.html#anwaveloadingharm>`_
        in the `Mechanical APDL Theory Reference
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_biblio.html>`_.

        This command is ignored if the :ref:`hropt` command has been issued with ``Method`` = KRYLOV, VT, or
        VTPA.

        This command is also valid in PREP7.
        """
        command = f"HREXP,{angle}"
        return self.run(command, **kwargs)

    def alphad(self, value: str = "", **kwargs):
        r"""Defines the mass matrix multiplier for damping.

        Mechanical APDL Command: `ALPHAD <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ALPHAD.html>`_

        Parameters
        ----------
        value : str
            Mass matrix multiplier for damping.

        Notes
        -----

        .. _ALPHAD_notes:

        This command defines the mass matrix multiplier :math:``  used to form the viscous damping matrix
        :math:``, where  :math:``  is the mass matrix.

        Values of :math:``  can also be input as a material property ( :ref:`mp`,ALPD or
        :ref:`tb`,SDAMP,,,,ALPD). If ALPD in either form is included, the ALPD value is added to the
        :ref:`alphad` value as appropriate. (See `Material Damping
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/mat_matdamping.html#>`_  `Damping
        Matrices <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_tool3.html#>`_
        :ref:`antype`,STATIC) or buckling ( :ref:`antype`,BUCKLE) analyses.

        This command is also valid in PREP7.
        """
        command = f"ALPHAD,{value}"
        return self.run(command, **kwargs)

    def dmprat(self, ratio: str = "", **kwargs):
        r"""Sets a modal damping ratio.

        Mechanical APDL Command: `DMPRAT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_DMPRAT.html>`_

        **Command default:**

        .. _DMPRAT_default:

        Use damping as defined by `Damping
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STR1D.html#strelemdamp>`_

        Parameters
        ----------
        ratio : str
            Modal damping ratio (for example, 2% is input as 0.02).

        Notes
        -----

        .. _DMPRAT_notes:

        Sets a damping ratio for use in a mode-superposition transient analysis ( :ref:`antype`,TRANS with
        :ref:`trnopt`,MSUP), a mode-superposition harmonic analysis ( :ref:`antype`,HARMIC with
        :ref:`hropt`,MSUP) analysis, or a spectrum ( :ref:`antype`,SPECTR) analysis.

        :ref:`dmprat` can also be defined in a substructure analysis that uses component mode synthesis. The
        damping ratio is added on the diagonal of the reduced damping matrix, as explained in `Component
        Mode Synthesis (CMS)
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_anproc6.html#eq39b62ffb-3890-471d-a79e-2d6096214d0b>`_

        This command is also valid in PREP7.

        **Additional Information**

        .. _DMPRAT_addlinfo:

        `Damping Matrices
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_tool3.html#>`_
        """
        command = f"DMPRAT,{ratio}"
        return self.run(command, **kwargs)

    def dampopt(self, option: str = "", value: str = "", **kwargs):
        r"""Sets damped eigensolver options.

        Mechanical APDL Command: `DAMPOPT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_DAMPOPT.html>`_

        **Command default:**

        .. _DAMPOPT_default:

        By default, the shift strategy is not activated for the damped eigensolver. This ensures a faster
        solve process but limits the number of eigenvalues that can be found.

        The default memory allocation strategy is used. Mechanical APDL evaluates the resources of the machine to
        choose the in-core or out-of-core mode.

        Parameters
        ----------
        option : str
            Damped eigensolver option:

            * ``SHIFT`` - Activate or deactivate the shift strategy of the damped eigensolver to move to a frequency range of
              interest. The ``FREQB`` value of the :ref:`modopt` command is used to choose the first frequency
              shift (see notes for details).

              Valid input for ``Value`` when ``Option`` = SHIFT:

              * ``OFF`` - Do not activate the shift strategy.

              * ``ON`` - Activate the shift strategy (default).

            * ``MEMORY`` - Controls the memory allocation strategy for the Damped eigensolver.

              Valid input for ``Value`` when ``Option`` = MEMORY:

              * ``DEFAULT`` - Default memory configuration (default). Everything is determined dynamically with
                respect to current machine resources.

              * ``INCORE`` - Fully in-core memory configuration.

              * ``MIX1`` - First level of mixed in-core / out-of-core configuration.

              * ``MIX2`` - Second level of mixed in-core / out-of-core configuration.

              * ``OUTOFCORE`` - Fully out-of-core memory configuration.

        value : str
            Assigned value for the specified ``Option`` (as described above).

        Notes
        -----

        .. _DAMPOPT_notes:

        :ref:`dampopt` specifies options to be used with the damped eigensolver ( :ref:`modopt`,DAMP) during
        a modal analysis ( :ref:`antype`,MODAL).

        Activating the shift strategy ( ``Option`` = SHIFT and ``Value`` = ON) enables the eigensolver to
        find higher frequency eigenvalues that might otherwise be missed. The SHIFT option has two
        objectives:

        * Extract high frequency eigenvalues according to the ``FREQB`` argument specified with
          :ref:`modopt`.

        * Unlock an auto-shift feature, so the algorithm will chain several analyses automatically then
          aggregate the solutions in one single results set.

        If ``FREQE`` is specified on :ref:`modopt`, the specified value is used to filter the complex
        eigenfrequencies based on magnitude.

        When the shift strategy is activated ( :ref:`dampopt`,SHIFT,ON)

        * and ``FREQB`` on :ref:`modopt` is specified, the damped eigensolver only produces eigenfrequencies
          with a real part greater than ``FREQB``

        * and ``FREQB`` on :ref:`modopt` is not specified, the damped eigensolver finds eigenvalues closest
          to the 0 Hz point.

        **Memory Allocation Option (** ``Option`` = MEMORY)

        The damped eigensolver algorithm allocates two main pools of memory:

        Memory for the internal damped eigensolver iterations.

        Memory for the specific damped eigensolver working arrays.

        The following table shows how memory is allocated for each option.

        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.

        The MIX1 configuration typically uses more memory than the MIX2 configuration, except when a large
        number of modes are requested for a small model.

        **Example Usage**

        .. _DAMPOPT_example:

        `Example: Shift Option Usage on DAMPOPT
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STR3_15.html#str_modal_dampExFig2>`_
        """
        command = f"DAMPOPT,{option},{value}"
        return self.run(command, **kwargs)

    def dmpstr(self, coeff: str = "", dmpsfreqtab: str = "", **kwargs):
        r"""Sets constant structural damping data.

        Mechanical APDL Command: `DMPSTR <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_DMPSTR.html>`_

        **Command default:**

        .. _DMPSTR_default:

        Use damping as defined by `Damping
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STR1D.html#strelemdamp>`_

        Parameters
        ----------
        coeff : str
            Constant structural damping coefficient.

        dmpsfreqtab : str
            Average excitation frequency table (Hz) for the calculation of equivalent viscous damping from
            structural damping input ( :ref:`dmpstr` and :ref:`mp`,DMPS) in a full transient analysis.
            Enclose the table name in percent signs (%) and use the :ref:`dim` command to define the table
            with primary variable TIME. To define a constant frequency instead of a table, see
            :ref:`trnopt`.

        Notes
        -----

        .. _DMPSTR_notes:

        Sets a constant structural (or hysteretic) damping coefficient for use in these analysis types:

        * Harmonic ( :ref:`antype`,HARMIC) -- full, `Krylov
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/str_Krysweep.html#str_Krylov_macros>`_,
          or mode-superposition [ :ref:`DMPSTR_mode-sup_LoadSupport`]

        * Modal ( :ref:`antype`,MODAL) with :ref:`modopt`,UNSYM, DAMP, or QRDAMP.

         .. _DMPSTR_mode-sup_LoadSupport:

        In a mode-superposition harmonic or transient analysis, you must apply the load in the modal portion
        of the analysis. Mechanical APDL calculates a load vector and writes it to the :file:`MODE` file,
        which you
        can apply via the :ref:`lvscale` command.

        :ref:`dmpstr` is also supported in transient ( :ref:`antype`,TRANS) analyses (full or QRDAMP mode-
        superposition) as an equivalent viscous damping when an average excitation frequency is specified.
        For a full or mode-superposition transient, specify a constant excitation frequency as ``DMPSFreq``
        on the :ref:`trnopt` command. For a full transient, you can alternatively specify a table of
        frequencies using ``DMPSFreqTab`` on this command. ``DMPSFreqTab`` overwrites ``DMPSFreq`` on
        :ref:`trnopt`.

        Note that for structures with multiple materials, :ref:`mp`,DMPS can also be used to specify
        constant structural material damping on a per material basis. If both :ref:`dmpstr` and
        :ref:`mp`,DMPS are specified, the damping effects are additive.

        This command is also valid in PREP7.
        """
        command = f"DMPSTR,{coeff},{dmpsfreqtab}"
        return self.run(command, **kwargs)

    def betad(self, value: str = "", **kwargs):
        r"""Defines the stiffness matrix multiplier for damping.

        Mechanical APDL Command: `BETAD <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_BETAD.html>`_

        Parameters
        ----------
        value : str
            Stiffness matrix multiplier for damping.

        Notes
        -----

        .. _BETAD_notes:

        This command defines the stiffness matrix multiplier :math:``  used to form the viscous damping
        matrix   :math:``, where  :math:``  is the stiffness matrix.

        Values of :math:``  can also be input as a material property ( :ref:`mp`,BETD or
        :ref:`tb`,SDAMP,,,,BETD). If BETD in either form is included, the BETD value is added to the
        :ref:`betad` value as appropriate. (See `Material Damping
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/mat_matdamping.html#>`_  `Damping
        Matrices <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_tool3.html#>`_
        :ref:`antype`,STATIC) or buckling ( :ref:`antype`,BUCKLE) analyses.

        This command is also valid in PREP7.
        """
        command = f"BETAD,{value}"
        return self.run(command, **kwargs)

    def qrdopt(
        self, reusekey: str = "", symmeth: str = "", cmccoutkey: str = "", **kwargs
    ):
        r"""Specifies additional QRDAMP modal analysis options.

        Mechanical APDL Command: `QRDOPT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_QRDOPT.html>`_

        Parameters
        ----------
        reusekey : str
            Reuse key for method= ``QRDAMP`` specified in :ref:`modopt` command.

            * ``ON`` - Reuse the symmetric eigensolution from the previous load steps or from the previous
              solution.

            * ``OFF`` - Do not reuse (calculates symmetric eigensolution at current load step). This is the
              default.

        symmeth : str
            Mode-extraction method to be used for the symmetric eigenvalue problem.

            * ``LANB`` - Block Lanczos algorithm (default).

            * ``SUBSP`` - Subspace algorithm.

            * ``SNODE`` - Supernode algorithm.

        cmccoutkey : str
            Complex Modal Contribution Coefficients (CMCC) output key. See `Calculate the Complex Mode Contribution Coefficients (CMCC) <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STRmodanexamp.html#streq375ccmcc>`_

            * ``ON`` - Output the CMCC to the text file :file:`JobnameCMCC`.

            * ``OFF`` - Do not output the CMCC. This is the default.

        Notes
        -----

        .. _QRDOPT_notes:

        If the :file:`filename.modesym` file exists in the working directory and ``ReuseKey`` = ON,
        :file:`filename.modesym` will be reused. If :file:`filename.modesym` does not exist in the working
        directory, the symmetric eigensolution will be calculated.

        When ``ReuseKey`` =ON, both the new modal analysis ( :file:`filename.modesym` usage) and the
        preceding modal analysis ( :file:`filename.modesym` generation) must be performed using the same
        product version number.
        """
        command = f"QRDOPT,{reusekey},,,{symmeth},{cmccoutkey}"
        return self.run(command, **kwargs)

    def subopt(self, option: str = "", value1: str = "", **kwargs):
        r"""Specifies Subspace (SUBSP) eigensolver options.

        Mechanical APDL Command: `SUBOPT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SUBOPT.html>`_

        Parameters
        ----------
        option : str
            One of the following options:

            * ``STRMCK`` - Controls whether a Sturm sequence check is performed.

              Valid input for ``Value1`` when ``Option`` = STRMCK:

              * ``OFF`` - Do not perform Sturm sequence check (default).

              * ``ON`` - Perform Sturm sequence check.

            * ``MEMORY`` - Controls the memory allocation strategy for the Subspace eigensolver.

              Valid input for ``Value1`` when ``Option`` = MEMORY:

              * ``DEFAULT`` - Default memory configuration (default). Everything is determined dynamically with
                respect to current machine resources.

              * ``INCORE`` - Fully in-core memory configuration.

              * ``MIX1`` - First level of mixed in-core / out-of-core configuration.

              * ``MIX2`` - Second level of mixed in-core / out-of-core configuration.

              * ``OUTOFCORE`` - Fully out-of-core memory configuration.

        value1 : str
            Assigned value for the specified ``Option`` (as described above).

        Notes
        -----

        .. _SUBOPT_notes:

        :ref:`subopt` specifies options to be used with the Subspace eigensolver ( :ref:`modopt`,SUBSP)
        during a modal analysis.

        **Memory Allocation Option (** ``Option`` = MEMORY)

        The Subspace eigensolver algorithm allocates two main pools of memory:

        Memory for the internal subspace eigensolver iterations.

        Memory for the specific subspace eigensolver working arrays.

        The following table shows how memory is allocated for each option.

        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.

        The MIX1 configuration typically uses more memory than the MIX2 configuration, except when a large
        number of modes are requested for a small model.
        """
        command = f"SUBOPT,{option},{value1}"
        return self.run(command, **kwargs)

    def frqscl(self, scaling: str = "", **kwargs):
        r"""Turns on automatic scaling of the entire mass matrix and frequency range for modal analyses.

        Mechanical APDL Command: `FRQSCL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_FRQSCL.html>`_

        **Command default:**
        Mechanical APDL uses automatic scaling if appropriate.

        Parameters
        ----------
        scaling : str

            * ``Off`` - Do not use automatic scaling of the mass matrix and frequency range.

            * ``On`` - Use automatic scaling of the mass matrix and frequency range.

        Notes
        -----
        This command is available only for modal analyses using the Block Lanczos, PCG Lanczos, Supernode,
        Subspace, or Unsymmetric mode extraction method ( :ref:`modopt`,LANB, LANPCG, SNODE, SUBPS, or
        UNSYM).

        Use this command to deactivate or force activation of automatic scaling of the entire mass matrix
        and frequency range for modal analyses where the entire mass matrix is significantly different (that
        is, orders of magnitude different) than the entire stiffness matrix (for example, due to the
        particular unit system being used). Where the mass matrix is significantly smaller compared to the
        stiffness matrix, the eigenvalues will tend to approach very large numbers (>10e12), making the
        selected mode-extraction method less efficient and more likely to miss modes.

        You can force the entire mass matrix and frequency range to be scaled via :ref:`frqscl`,ON. Doing so
        brings the stiffness and mass matrices closer together in terms of orders of magnitude, improving
        efficiency and reducing the likelihood of missed modes. The resulting eigenvalues are then
        automatically scaled back to the original system. If you are using micro MKS units, where the
        density is typically very small compared to the stiffness, you may want to force scaling on.

        If the stiffness and mass are on the same scale, :ref:`frqscl`,ON has no effect.

        This command is not valid and has no effect when used with :ref:`msave`,ON in a modal analysis with
        the PCG Lanczos mode extraction method.
        """
        command = f"FRQSCL,{scaling}"
        return self.run(command, **kwargs)
