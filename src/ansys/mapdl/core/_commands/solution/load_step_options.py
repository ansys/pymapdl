# Copyright (C) 2016 - 2026 ANSYS, Inc. and/or its affiliates.
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


class LoadStepOptions:

    def autots(self, key: str = "", **kwargs):
        r"""Specifies whether to use automatic time stepping or load stepping.

        Mechanical APDL Command: `AUTOTS <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_AUTOTS.html>`_

        Parameters
        ----------
        key : str
            Automatic time stepping key:

            * ``OFF`` - Do not use automatic time stepping.

            * ``ON`` - Use automatic time stepping (default).

            * ``AUTO`` - The program determines whether to use automatic time stepping (used by Workbench).

        Notes
        -----

        .. _AUTOTS_notes:

        Specifies whether to use automatic time stepping (or load stepping) over this load step. If ``Key``
        = ON, both time step prediction and time step bisection will be used.

        Bisection does not occur with :ref:`thopt`,QUASI since it uses only one equilibrium iteration per
        substep. To ensure bisection, use the iterative QUASI method ( :ref:`thopt`,QUASI,,,,,,1).

        You cannot use automatic time stepping ( :ref:`autots` ), line search ( :ref:`lnsrch` ), or the DOF
        solution predictor ( :ref:`pred` ) with the arc-length method ( :ref:`arclen`, :ref:`arctrm` ). If
        you activate the arc-length method after you set :ref:`autots`, :ref:`lnsrch`, or :ref:`pred`, a
        warning message appears. If you choose to proceed with the arc-length method, the program disables
        your automatic time stepping, line search, and DOF predictor settings, and the time step size is
        controlled by the arc-length method internally.

        This command is also valid in PREP7.
        """
        command = f"AUTOTS,{key}"
        return self.run(command, **kwargs)

    def campbell(self, action: str = "", **kwargs):
        r"""Prepares the result file for a subsequent Campbell diagram of a prestressed structure.

        Mechanical APDL Command: `CAMPBELL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CAMPBELL.html>`_

        Parameters
        ----------
        action : str
            Campbell action:

            * ``NONE`` - Do not prepare the result file. This option is the default behavior.

            * ``RSTP`` - Prepare the result file ( :file:`Jobname.RSTP` ) for a subsequent `Campbell diagram
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_rot/Hlp_G_ROTCAMPDIAGS.html#rotgencamp2a>`_
              of a prestressed structure.

        Notes
        -----
        For an analysis involving a prestressed structure, the :ref:`campbell` command specifies whether or
        not to prepare the result file to support a `Campbell diagram
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_rot/Hlp_G_ROTCAMPDIAGS.html#rotgencamp2a>`_
        analysis ( :ref:`prcamp` or :ref:`plcamp` ).

        To prestress a structure, the program performs a static solution before the `linear perturbation
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/strlinpertother.html>`_ modal
        solution. For specific information about rotating structures, see `Considerations for Rotating
        Structures
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/strllinpertrotmach.html#str_rot_rotating>`_

        The :ref:`campbell` command requires that modal and static analyses be performed alternately. It
        works only when the number of static analyses is the same as the number of modal analyses. Any
        number of analyses can be performed, but the same number of each (static and modal) is expected. The
        modal solutions are appended in the results file ( :file:`Jobname.RSTP` ).

        For an example of :ref:`campbell` command usage, see in the `Rotordynamic Analysis Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_rot/rotdynappenda.html>`_.
        """
        command = f"CAMPBELL,{action}"
        return self.run(command, **kwargs)

    def cecmod(self, neqn: str = "", const: str = "", **kwargs):
        r"""Modifies the constant term of a constraint equation during solution.

        Mechanical APDL Command: `CECMOD <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CECMOD.html>`_

        Parameters
        ----------
        neqn : str
            Reference number of constraint equation.

        const : str
            New value of the constant term of equation.

        Notes
        -----

        .. _CECMOD_notes:

        Other terms of the constraint equation cannot be changed during the solution phase, but must be
        defined or changed within PREP7 prior to the solution. See the :ref:`ce` command for details.

        This command is also valid in PREP7.
        """
        command = f"CECMOD,{neqn},{const}"
        return self.run(command, **kwargs)

    def deltim(
        self,
        dtime: str = "",
        dtmin: str = "",
        dtmax: str = "",
        carry: str = "",
        **kwargs,
    ):
        r"""Specifies the time step sizes to be used for the current load step.

        Mechanical APDL Command: `DELTIM <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_DELTIM.html>`_

        Parameters
        ----------
        dtime : str
            Time step size for this step. If automatic time stepping is used ( :ref:`autots` ), ``DTIME`` is
            the starting time substep.

            If contact elements ( ``TARGE169``, ``TARGE170``, ``CONTA172``, ``CONTA174``, ``CONTA175``, or
            ``CONTA177`` ) are used, defaults to ``TIME`` or ``TIME`` /20 (where ``TIME`` is the time at the
            end of the load step as set on the :ref:`time` command), depending on the physics of the model.
            If none of these contact elements are used, defaults to ``TIME``.

        dtmin : str
            Minimum time step (if automatic time stepping is used). The program automatically determines the
            default based on the physics of the model.

        dtmax : str
            Maximum time step (if automatic time stepping is used). The program automatically determines the
            default based on the physics of the model.

        carry : str
            Time step carry over key:

            * ``OFF`` - Use ``DTIME`` as time step at start of each load step.

            * ``ON`` - Use final time step from previous load step as the starting time step (if automatic time
              stepping is used).

            The program automatically determines the default based on the physics of the model.

        Notes
        -----

        .. _DELTIM_notes:

        See :ref:`nsubst` for an alternative input.

        Use consistent values for ``DTIME`` and ``TIME`` ( :ref:`time` ). For example, using 0.9 for
        ``DTIME`` and 1.0 for ``TIME`` results in one time step because 1.0 ( ``TIME`` ) is divisible by.9
        ( ``DTIME`` ) at most once. If you intend to load in 10 increments over a time span of 1.0, use 0.1
        for ``DTIME`` and 1.0 for ``TIME``.

        The program calculates the initial incremental time so that ( ``EndingTime`` - ``StartingTime`` )/
        ``DTIME`` is an integer, which may affect the initial incremental time that you specify. For
        example, if the starting time is 0, the ending time is 1, and the initial incremental time is 0.4,
        the program rounds to the nearest integer and adjusts the time to 0.33333.

        For solution efficiency, specify values for all fields of this command.

        Changing the time step size upon restarting an analysis during a load step is not recommended. You
        should only change the time step size between load steps.

        This command is also valid in PREP7.
        """
        command = f"DELTIM,{dtime},{dtmin},{dtmax},{carry}"
        return self.run(command, **kwargs)

    def expsol(
        self,
        lstep: str = "",
        sbstep: str = "",
        timfrq: str = "",
        elcalc: str = "",
        **kwargs,
    ):
        r"""Specifies the solution to be expanded for mode-superposition analyses or substructure analyses.

        Mechanical APDL Command: `EXPSOL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_EXPSOL.html>`_

        Parameters
        ----------
        lstep : str
            Expand the solution identified as load step ``LSTEP`` and substep ``SBSTEP``.

        sbstep : str
            Expand the solution identified as load step ``LSTEP`` and substep ``SBSTEP``.

        timfrq : str
            As an alternative to ``LSTEP`` and ``SBSTEP``, expand the solution at, or nearest to, the time
            value TIMFRQ (for :ref:`antype`,TRANS or :ref:`antype`,SUBSTR) or frequency value ``TIMFRQ``
            (for :ref:`antype`,HARMIC). ``LSTEP`` and ``SBSTEP`` should be blank.

        elcalc : str
            Element calculation key:

            * ``YES`` - Calculate element results, nodal loads, and reaction loads.

            * ``NO`` - Do not calculate these items.

        Notes
        -----

        .. _EXPSOL_notes:

        Specifies the solution to be expanded from analyses that use the mode-superposition method (
        :ref:`antype`,HARMIC or TRANS) or substructuring ( :ref:`antype`,SUBSTR). Use the :ref:`numexp`
        command to expand a group of solutions.

        The resulting results file will maintain the same load step, substep, and time (or frequency) values
        as the requested solution to be expanded.

        This command is also valid in PREP7.
        """
        command = f"EXPSOL,{lstep},{sbstep},{timfrq},{elcalc}"
        return self.run(command, **kwargs)

    def kbc(self, key: int | str = "", omgsqrdkey: int | str = "", **kwargs):
        r"""Specifies ramped or stepped loading within a load step.

        Mechanical APDL Command: `KBC <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_KBC.html>`_

        Parameters
        ----------
        key : int or str
            Ramping key:

            * ``0`` - Loads are linearly interpolated (ramped) for each substep from the values of the previous
              load step to the values of this load step. This is the default value.

            * ``1`` - Loads are step changed (stepped) at the first substep of this load step to the values of
              this load step (that is, the same values are used for all substeps). Useful for rate-dependent
              behavior (for example, creep, viscoplasticity, etc.) or transient load steps only.

        omgsqrdkey : int or str
            Key for the interpolation of the rotational velocity loading (only supported when ``KEY`` = 0):

            * ``0`` - Rotational velocities are linearly interpolated. This is the default.

            * ``1`` - A quadratic interpolation is used for the rotational velocities ( :ref:`omega`,
              :ref:`cmomega`, and :ref:`cmrotate` ). All other loads are interpolated linearly.

        Notes
        -----

        .. _KBC_notes:

        Specifies whether loads applied to intermediate substeps within the load step are to be stepped or
        ramped. Used only if ``DTIME`` on the :ref:`deltim` command is less than the time span or,
        conversely, if ``NSBSTP`` on the :ref:`nsubst` command is greater than one. Flags (FSI, MXWF, MVDI,
        etc.) are always stepped.

        Changing the ramping ``KEY`` (that is, switching between ramped and stepped boundary conditions)
        between load steps is not recommended.

        For ramped loading ( :ref:`kbc`,0), when a load is applied for the first time, it is interpolated
        from zero to the value of the current load step, and not from the initial condition or value of the
        degree of freedom from the previous load step.

        Spatially varying tabular loads or boundary conditions do not support direct ramping or stepping
        options and, instead, apply their full values according to the supplied tabular functions regardless
        of the :ref:`kbc` setting.

        Regardless of the :ref:`kbc` setting, any tabular load is applied as step change. This is the case,
        for example, for a static or harmonic cyclic symmetry analysis with a load that varies by sector (
        :ref:`cycopt`, LDSECT). Note that when tabular and non-tabular loads are present in the same
        analysis, the non-tabular loads are ramped or stepped according to the :ref:`kbc` setting.

        Irrespective of the :ref:`kbc` setting, loads are usually step-removed. See `Stepping or Ramping
        Loads
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/Hlp_G_BAS2_7.html#bas.ch.2.tab.11.ft.5>`_
        in the `Basic Analysis Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/Hlp_G_BAS19.html>`_ for more
        information.

        It is sometimes difficult to obtain successful convergence with stepped loading in a nonlinear
        transient problem. If divergence is encountered, determine if stepped loading was used by default,
        then determine if it is appropriate for the analysis.

        This command is also valid in PREP7.
        """
        command = f"KBC,{key},{omgsqrdkey}"
        return self.run(command, **kwargs)

    def kuse(self, key: int | str = "", **kwargs):
        r"""Specifies whether or not to reuse factorized matrices.

        Mechanical APDL Command: `KUSE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_KUSE.html>`_

        Parameters
        ----------
        key : int or str
            Reuse key:

            * ``0`` - Program decides whether or not to reuse the previous factorized matrices.

            * ``1`` - Force the previous factorized matrices to be reused. Used mainly in a restart. Forcing
              reuse of the matrices is a nonstandard use of the program and should be done with caution. For
              instance, using this option and changing the number of elements, or the number or type of degrees of
              freedom, may cause an abort.

            * ``-1`` - All element matrices are reformed and are used to reform new factorized matrices.

        Notes
        -----

        .. _KUSE_notes:

        Overrides the program logic to determine whether or not to reuse the previous factorized matrices
        for each substep of this load step. Applies only to static or full transient analyses. For more
        details see.

        This command is also valid in PREP7.
        """
        command = f"KUSE,{key}"
        return self.run(command, **kwargs)

    def magopt(self, value: int | str = "", **kwargs):
        r"""Specifies options for a 3D magnetostatic field analysis.

        Mechanical APDL Command: `MAGOPT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MAGOPT.html>`_

        Parameters
        ----------
        value : int or str
            Option key:

            * ``0`` - Calculate a complete H field solution in the entire domain using a single (reduced) potential.

              .. warning::

                  When used in problems with both current sources and iron regions, errors may result due to
                  numerical cancellation.

            * ``1`` - Calculate and store a preliminary H field in "iron" regions (μ:sub:`r` ≠ 1). Requires
              flux-parallel boundary conditions to be specified on exterior iron boundaries. Used in conjunction
              with subsequent solutions with ``VALUE`` = 2 followed by ``VALUE`` = 3. Applicable to multiply-
              connected iron domain problems.

            * ``2`` - Calculate and store a preliminary H field in "air" regions (μ:sub:`r` = 1). The air-iron
              interface is appropriately treated internally by the program. Used in conjunction with a subsequent
              solution with ``VALUE`` = 3. Applicable to singly-connected iron domain problems (with subsequent
              solution with ``VALUE`` = 3) or to multiply-connected iron domain problems (when preceded by a
              solution with ``VALUE`` = 1 and followed by a solution with ``VALUE`` = 3).

            * ``3`` - Use the previously stored H field solution(s) and calculate the complete H field.

        Notes
        -----

        .. _MAGOPT_notes:

        Specifies the solution sequence options for a 3D magnetostatic field analysis using a scalar
        potential (MAG). The solution sequence is determined by the nature of the problem.

        You cannot use constraint equations with ``Value`` = 1.

        This command is also valid in PREP7.

        Distributed-Memory Parallel (DMP) Restriction :ref:`magopt`,3 is not supported in a DMP solution
        when the following contact elements are present
        in the model: ``CONTA174``, ``CONTA175``, or ``CONTA177``.
        """
        command = f"MAGOPT,{value}"
        return self.run(command, **kwargs)

    def magsolv(
        self,
        opt: int | str = "",
        nramp: str = "",
        cnvcsg: str = "",
        cnvflux: str = "",
        neqit: str = "",
        biot: int | str = "",
        cnvtol: str = "",
        **kwargs,
    ):
        r"""Specifies magnetic solution options and initiates the solution.

        Mechanical APDL Command: `MAGSOLV <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MAGSOLV.html>`_

        Parameters
        ----------
        opt : int or str
            Static magnetic solution option:

            * ``0`` - Vector potential (MVP) or edge formulation (default).

            * ``1`` - Combined vector potential and reduced scalar potential (MVP-RSP).

            * ``2`` - Reduced scalar potential (RSP).

            * ``3`` - Difference scalar potential (DSP).

            * ``4`` - General scalar potential (GSP).

        nramp : str
            Number of ramped substeps for the first load step of a nonlinear MVP or MVP-RSP solution.
            Defaults to 3. If ``NRAMP`` = -1, ignore the ramped load step entirely. ``NRAMP`` is ignored for
            linear magnetostatics.

        cnvcsg : str
            Tolerance value on the program-calculated reference value for the magnetic current-segment
            convergence. Used for the MVP, the MVP-RSP, and the edge formulation solution options ( ``OPT``
            = 0 and 1). Defaults to 0.001.

        cnvflux : str
            Tolerance value on the program-calculated reference value for the magnetic flux convergence.
            Used for all scalar potential solution options ( ``OPT`` = 2, 3, 4). Defaults to 0.001.

        neqit : str
            Maximum number of equilibrium iterations per load step. Defaults to 25.

        biot : int or str
            Option to force execution of a Biot-Savart integral solution ( :ref:`biot`,NEW) for the scalar potential options. Required if multiple load steps are being performed with different current source primitives ( ``SOURC36`` elements).

            * ``0`` - Do not force execution of Biot-Savart calculation (default); Biot-Savart is automatically
              calculated only for the first solution.

            * ``1`` - Force execution of Biot-Savart calculation.

        cnvtol : str
            Sets the convergence tolerance for AMPS reaction. Defaults to 1e-3.

        Notes
        -----

        .. _MAGSOLV_notes:

        :ref:`magsolv` invokes a Mechanical APDL macro which specifies magnetic solution options and
        initiates the
        solution. The macro is applicable to any Mechanical APDL magnetostatic analysis using the magnetic
        vector
        potential (MVP), reduced scalar potential (RSP), difference scalar potential (DSP), general scalar
        potential (GSP), or combined MVP-RSP formulation options. Results are only stored for the final
        converged solution. (In POST1, issue :ref:`starset`,LIST to identify the load step of solution
        results.) The macro internally determines if a nonlinear analysis is required based on magnetic
        material properties.

        If you use the ``BIOT`` option and issue :ref:`save` after solution or postprocessing, the Biot-
        Savart calculations are saved to the database, but will be overwritten upon normal exit from the
        program. To save this data after issuing :ref:`save`, use the ``/EXIT``,NOSAVE command. You can
        also issue the ``/EXIT``,SOLU command to exit Mechanical APDL and save all solution data, including
        the
        Biot-Savart calculations, in the database. Otherwise, when you issue :ref:`resume`, the Biot-Savart
        calculation will be lost (resulting in a zero solution).

        The MVP, MVP-RSP, and edge formulation options perform a two-load-step solution sequence. The first
        load step ramps the applied loads over a prescribed number of substeps ( ``NRAMP`` ), and the second
        load step calculates the converged solution. For linear problems, only a single load step solution
        is performed. The ramped load step can be bypassed by setting ``NRAMP`` to -1.

        The RSP option solves in a single load step using the adaptive descent procedure. The DSP option
        uses two load steps, and the GSP solution uses three load steps.

        The following analysis options and nonlinear options are controlled by this macro: :ref:`kbc`,
        :ref:`neqit`, :ref:`nsubst`, :ref:`cnvtol`, :ref:`nropt`, :ref:`magopt`, and :ref:`outres`.

        You cannot use constraint equations with ``OPT`` = 4.

        When the ``BIOT`` option is on ( ``BIOT`` = 1), Distributed-Memory Parallel (DMP) restrictions may
        apply. For more information, see the :ref:`biot` command.
        """
        command = f"MAGSOLV,{opt},{nramp},{cnvcsg},{cnvflux},{neqit},{biot},{cnvtol}"
        return self.run(command, **kwargs)

    def mode(self, mode: str = "", isym: int | str = "", **kwargs):
        r"""Specifies the harmonic loading term for this load step.

        Mechanical APDL Command: `MODE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MODE.html>`_

        Parameters
        ----------
        mode : str
            Number of harmonic waves around circumference for this harmonic loading term (defaults to 0).

        isym : int or str
            Symmetry condition for this harmonic loading term (not used when ``MODE`` = 0):

            * ``1`` - Symmetric (UX, UY, ROTZ, TEMP use cosine terms; UZ uses sine term) (default).

            * ``-1`` - Antisymmetric (UX, UY, ROTZ, TEMP use sine terms; UZ uses cosine term).

        Notes
        -----

        .. _MODE_notes:

        Used with axisymmetric elements having nonaxisymmetric loading capability (for example, ``PLANE25``,
        ``SHELL61``, etc.). For analysis types :ref:`antype`,MODAL, HARMIC, TRANS, and SUBSTR, the term must
        be defined in the first load step and may not be changed in succeeding load steps.

        This command is also valid in PREP7.
        """
        command = f"MODE,{mode},{isym}"
        return self.run(command, **kwargs)

    def nsubst(
        self,
        nsbstp: str = "",
        nsbmx: str = "",
        nsbmn: str = "",
        carry: str = "",
        **kwargs,
    ):
        r"""Specifies the number of substeps to be taken this load step.

        Mechanical APDL Command: `NSUBST <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_NSUBST.html>`_

        Parameters
        ----------
        nsbstp : str
            Number of substeps to be used for this load step (that is, the time step size or frequency
            increment). If automatic time stepping is used ( :ref:`autots` ), ``NSBSTP`` defines the size of
            the first substep.

            If contact elements ( ``TARGE169``, ``TARGE170``, ``CONTA172``, ``CONTA174``, ``CONTA175``, or
            ``CONTA177`` ) are used, defaults to 1 or 20 substeps, depending on the physics of the model. If
            none of these contact elements are used, defaults to 1 substep.

        nsbmx : str
            Maximum number of substeps to be taken (that is, the minimum time step size) if automatic time
            stepping is used. The program automatically determines the default based on the physics of the
            model.

        nsbmn : str
            Minimum number of substeps to be taken (that is, the maximum time step size) if automatic time
            stepping is used. The program automatically determines the default based on the physics of the
            model.

        carry : str
            Time step carryover key (program-determined default depending on the problem physics):

            * ``OFF`` - Use ``NSBSTP`` to define time step at start of each load step.

            * ``ON`` - Use final time step from previous load step as the starting time step (if automatic time
              stepping is used).

            The program automatically determines the default based on the physics of the model.

        Notes
        -----

        .. _NSUBST_notes:

        See :ref:`deltim` for an alternative input. It is recommended that all fields of this command be
        specified for solution efficiency and robustness.

        When the arc-length method is active ( :ref:`arclen` command), the ``NSBMX`` and ``NSBMN`` arguments
        are ignored.

        Changing the number of substeps upon restarting an analysis during a load step is not recommended.
        You should only change the number of substeps between load steps.

        This command is also valid in PREP7.
        """
        command = f"NSUBST,{nsbstp},{nsbmx},{nsbmn},{carry}"
        return self.run(command, **kwargs)

    def numexp(
        self,
        num: str = "",
        begrng: str = "",
        endrng: str = "",
        elcalc: str = "",
        **kwargs,
    ):
        r"""Specifies solutions to be expanded from mode-superposition analyses or substructure analyses.

        Mechanical APDL Command: `NUMEXP <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_NUMEXP.html>`_

        Parameters
        ----------
        num : str
            The number of solutions to expand. This value is required.

            * ``Num`` - Number of solutions to expand.

            * ``ALL`` - Expand all substeps between ``BEGRNG`` and ``ENDRNG`` (provided that ``ENDRNG`` > 0). If
              ``BEGRNG`` and ``ENDRNG`` have no specified values, this option expands all substeps of all load
              steps.

        begrng : str
            Beginning and ending time (or frequency) range for expanded solutions. The default is 0 for both
            values.

        endrng : str
            Beginning and ending time (or frequency) range for expanded solutions. The default is 0 for both
            values.

        elcalc : str
            The element-calculation key:

            * ``YES`` - Calculate element results, nodal loads, and reaction loads. This value is the default.

            * ``NO`` - Do not calculate these items.

        Notes
        -----
        **Command Defaults**

        .. _NUMEXP_defaults:

        Issuing this command with no arguments is invalid. You must specify the number of solutions, or all
        solutions, to expand ( ``NUM`` ). The default value for both the beginning ( ``BEGRNG`` ) and ending
        ( ``ENDRNG`` ) time or frequency is 0. The default behavior of the command is to calculate element
        results, nodal loads, and reaction loads ( ``Elcalc`` = YES).

        .. _NUMEXP_notes:

        Specifies a range of solutions to be expanded from analyses that use mode-superposition methods (
        :ref:`antype`,HARMIC or TRANS) or substructuring ( :ref:`antype`,SUBSTR).

        For :ref:`antype`,TRANS, ``NUM``, evenly spaced solutions are expanded between time ``BEGRNG`` and
        time ``ENDRNG``.

        For :ref:`antype`,HARMIC, ``NUM``, evenly spaced solutions are expanded between frequency ``BEGRNG``
        and frequency ``ENDRNG``.

        The first expansion in all cases is done at the first point beyond ``BEGRNG`` (that is, at
        ``BEGRNG`` + ( ``ENDRNG`` - ``BEGRNG`` ) / ``NUM`` )).

        The resulting results file will maintain the same load step, substep, and time (or frequency) values
        as the use pass.

        For a single expansion of a solution, or for multiple expansions when the solutions are not evenly
        spaced (such as in a mode-superposition harmonic analysis with the cluster option),
        Ansys, Inc. recommends issuing one or more :ref:`expsol` commands.

        :ref:`numexp` is invalid in these cases:

        * In a substructing analysis ( :ref:`antype`, ``SUBST`` ) when a factorized matrix file (the
          :file:`.LN22` file generated by the sparse solver) does not exist, causing Mechanical APDL to use the
          full- resolve method.

        * If the full-resolve option is selected ( :ref:`seopt` ).

        In both situations, issue :ref:`expsol` to perform a single expansion for each solution desired.

        This command is also valid in PREP7.
        """
        command = f"NUMEXP,{num},{begrng},{endrng},{elcalc}"
        return self.run(command, **kwargs)

    def time(self, time: str = "", **kwargs):
        r"""Sets the time for a load step.

        Mechanical APDL Command: `TIME <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_TIME.html>`_

        Parameters
        ----------
        time : str
            Time at the end of the load step.

        Notes
        -----

        .. _TIME_notes:

        Associates the boundary conditions at the end of the load step with a particular ``TIME`` value.

        ``TIME`` must be a positive, nonzero, monotonically increasing quantity that "tracks" the input
        history. Units of time should be consistent with those used elsewhere (for properties, creep
        equations, etc.).

        Typically, for the first load step ``TIME`` defaults to 1. However, for the first load step of a
        mode-superposition transient analysis ( :ref:`antype`,TRANS and  :ref:`trnopt`,MSUP), the
        :ref:`time` command is ignored and a static solution is performed at ``TIME`` = 0.

        For a full transient analyses, the command's default behavior does not apply. You must specify a
        time for each load step and it must be greater than the time at the end of the prior load step.

        ``TIME`` does not apply to modal ( :ref:`antype`,MODAL), harmonic ( :ref:`antype`,HARMIC), or
        substructure ( :ref:`antype`,SUBSTR) analyses.

        This command is also valid in PREP7.
        """
        command = f"TIME,{time}"
        return self.run(command, **kwargs)

    def tref(self, tref: str = "", **kwargs):
        r"""Defines the reference temperature for thermal strain calculations.

        Mechanical APDL Command: `TREF <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_TREF.html>`_

        Parameters
        ----------
        tref : str
            Reference temperature for thermal expansion.

            If the uniform temperature ( :ref:`tunif` ) is not specified, it is also set to this value.

        Notes
        -----

        .. _TREF_notes:

        Defines the reference temperature for the thermal strain calculations in structural analyses.
        Thermal strains are given by α * (T - TREF), where α is the coefficient of thermal expansion. Input
        the strain via ALPX, ALPY, ALPZ (the secant or mean
        coefficient value), or CTEX, CTEY, CTEZ (the instantaneous coefficient value), or the thermal strain
        value (THSX, THSY, THSZ). T is the element temperature. If α is temperature-dependent, ``TREF``
        should be in the range of temperatures you define using the :ref:`mptemp` command.

        Reference temperatures may also be input per material by specifying a value on the :ref:`mp`
        material property command:

        :ref:`mp`,REFT, ``MAT``, ``C0``.

        Only a constant (non-temperature-dependent) value is valid. The value input on the :ref:`tref`
        command applies to all materials not having a specified material property definition.

        To convert temperature-dependent secant coefficients of thermal expansion (SCTE) data (properties
        ALPX, ALPY, ALPZ) from the definition temperature to the reference temperature defined via a
        :ref:`tref` (or :ref:`mp`,REFT) command, issue the :ref:`mpamod` command.

        This command is also valid in PREP7.
        """
        command = f"TREF,{tref}"
        return self.run(command, **kwargs)

    def tsres(self, array: str = "", **kwargs):
        r"""Defines an array of key times at which the time-stepping strategy changes.

        Mechanical APDL Command: `TSRES <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_TSRES.html>`_

        Parameters
        ----------
        array : str
            Identifies an ``N`` x1x1 array parameter containing the key times at which the heat transfer
            time- stepping strategy changes (the time step is reset to the initial time step based on
            :ref:`deltim` or :ref:`nsubst` settings). The array name must be enclosed by % signs (for
            example, ``array``). See :ref:`dim` for more information on array parameters.

        Notes
        -----

        .. _TSRES_notes:

        Time values in the array parameter must be in ascending order and must not exceed the time at the
        end of the load step as defined on the :ref:`time` command. The time increment between time points
        in the array list must be larger than the initial time step defined on the :ref:`deltim` or
        :ref:`nsubst` command. Time values must also fall between the beginning and ending time values of
        the load step. For multiple load step problems, you must either change the parameter values to fall
        between the beginning and ending time values of the load step or reissue the command with a new
        array parameter. To clear the array parameter specification, issue :ref:`tsres`,ERASE. Results can
        be output at the requested time points if the array or time values in the array are also specified
        in the :ref:`outres` command using ``FREQ`` =``array``. Use this command to reset the time-stepping
        strategy within a load step. You may need to reset the time-stepping strategy when using tabular
        time-varying boundary conditions.

        See `Steady-State Thermal Analysis
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_the/Hlp_G_THE2_10.html>`_ of the
        `Thermal Analysis Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_the/Hlp_G_THE4.html>`_ for more
        information on applying boundary conditions via tabular input. See `Transient
        Thermal Analysis
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_the/Hlp_G_THE3_12.html>`_  of
        the `Thermal Analysis Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_the/Hlp_G_THE4.html>`_ for more
        information on defining the key time array.
        """
        command = f"TSRES,{array}"
        return self.run(command, **kwargs)

    def upcoord(self, factor: str = "", key: str = "", **kwargs):
        r"""Modifies the coordinates of the active set of nodes, based on the current displacements.

        Mechanical APDL Command: `UPCOORD <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_UPCOORD.html>`_

        Parameters
        ----------
        factor : str
            Scale factor for displacements being added to nodal coordinates. If ``FACTOR`` = 1.0, the full
            displacement value will be added to each node, 0.5, half the displacement value will be added,
            etc. If ``FACTOR`` = -1, the full displacement value will be subtracted from each node, etc.

        key : str
            Key for zeroing displacements in the database:

            * ``OFF`` - Do not zero the displacements (default).

            * ``ON`` - Zero the displacements.

        Notes
        -----

        .. _UPCOORD_notes:

        The :ref:`upcoord` command uses displacements stored in the Mechanical APDL database, and not those
        contained within the results file, :file:`Jobname.RST`. Nodal coordinates are updated each time the
        command is issued. After updating, both the nodal displacements and rotations are set to zero if
        ``Key`` = ON.

        For structural solutions with an updated mesh, unless the coefficient matrix is otherwise reformed
        (for example, a new analysis or :ref:`nlgeom`,ON) it should first be reformed by issuing a
        :ref:`kuse`,-1 command.

        :ref:`upcoord` should not be issued between load steps in structural analysis.

        For a multiphysics simulation where a CFD or electromagnetic field is being coupled to a structure
        undergoing large displacements, all (or a portion) of the surrounding field mesh may take part in
        the structural solution to "move" with the displacing structure. You can use the :ref:`upcoord`
        command with a suitable ``FACTOR`` to update the coordinates of the nodes using the newly computed
        displacements. The mesh will now conform with the displaced structure for subsequent field
        solutions. However, the mesh should always be restored to its original location by using an
        :ref:`upcoord`, ``FACTOR`` command before performing any subsequent structural solutions. This is
        true for both repeated linear solutions, and for nonlinear restarts. (All saved displacements are
        relative to the original mesh location.)

        .. warning::

            Orientation nodes for beams and pipes always have zero displacements. Therefore, although this
            command may alter the locations of other beam and pipe nodes, it has no effect on orientation
            nodes. Carefully inspect the element coordinate systems on the updated model.

        This command is not intended to replace either the large-displacement or birth-and-death capability.

        This command is also valid in PREP7.
        """
        command = f"UPCOORD,{factor},{key}"
        return self.run(command, **kwargs)

    def usrcal(
        self,
        rnam1: str = "",
        rnam2: str = "",
        rnam3: str = "",
        rnam4: str = "",
        rnam5: str = "",
        rnam6: str = "",
        rnam7: str = "",
        rnam8: str = "",
        rnam9: str = "",
        **kwargs,
    ):
        r"""Allows user-solution subroutines to be activated or deactivated.

        Mechanical APDL Command: `USRCAL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_USRCAL.html>`_

        Parameters
        ----------
        rnam1 : str
            User-defined solution subroutine names to be activated. Up to nine may be defined on one command or
            multiple commands may be used. If ``Rnam1`` = ALL, activate all valid user subroutines. If ``Rnam1`` = NONE, deactivate all valid user subroutines. All characters are required:

            * ``USREFL`` - Allows user defined scalar field (body force) loads.

            * ``USERCV`` - Allows user defined convection (surface) loads.

            * ``USERPR`` - Allows user defined pressure (surface) loads.

            * ``USERFX`` - Allows user-defined heat flux (surface) loads.

            * ``USERCH`` - Allows user-defined charge density (surface) loads.

            * ``USERFD`` - Computes the complex load vector for the frequency domain logic.

            * ``USEROU`` - Allows user supplied element output.

            * ``USOLBEG`` - Allows user access before each solution.

            * ``ULDBEG`` - Allows user access before each load step.

            * ``USSBEG`` - Allows user access before each substep.

            * ``UITBEG`` - Allows user access before each equilibrium iteration.

            * ``UITFIN`` - Allows user access after each equilibrium iteration.

            * ``USSFIN`` - Allows user access after each substep.

            * ``ULDFIN`` - Allows user access after each load step.

            * ``USOLFIN`` - Allows user access after each solution.

            * ``UANFIN`` - Allows user access at end of run.

            * ``UELMATX`` - Allows user access to element matrices and load vectors.

            * ``UTIMEINC`` - Allows a user-defined time step, overriding the program-determined time step.

            * ``UCNVRG`` - Allows user-defined convergence checking, overriding the program-determined
              convergence.

        rnam2 : str
            User-defined solution subroutine names to be activated. Up to nine may be defined on one command or
            multiple commands may be used. If ``Rnam1`` = ALL, activate all valid user subroutines. If ``Rnam1`` = NONE, deactivate all valid user subroutines. All characters are required:

            * ``USREFL`` - Allows user defined scalar field (body force) loads.

            * ``USERCV`` - Allows user defined convection (surface) loads.

            * ``USERPR`` - Allows user defined pressure (surface) loads.

            * ``USERFX`` - Allows user-defined heat flux (surface) loads.

            * ``USERCH`` - Allows user-defined charge density (surface) loads.

            * ``USERFD`` - Computes the complex load vector for the frequency domain logic.

            * ``USEROU`` - Allows user supplied element output.

            * ``USOLBEG`` - Allows user access before each solution.

            * ``ULDBEG`` - Allows user access before each load step.

            * ``USSBEG`` - Allows user access before each substep.

            * ``UITBEG`` - Allows user access before each equilibrium iteration.

            * ``UITFIN`` - Allows user access after each equilibrium iteration.

            * ``USSFIN`` - Allows user access after each substep.

            * ``ULDFIN`` - Allows user access after each load step.

            * ``USOLFIN`` - Allows user access after each solution.

            * ``UANFIN`` - Allows user access at end of run.

            * ``UELMATX`` - Allows user access to element matrices and load vectors.

            * ``UTIMEINC`` - Allows a user-defined time step, overriding the program-determined time step.

            * ``UCNVRG`` - Allows user-defined convergence checking, overriding the program-determined
              convergence.

        rnam3 : str
            User-defined solution subroutine names to be activated. Up to nine may be defined on one command or
            multiple commands may be used. If ``Rnam1`` = ALL, activate all valid user subroutines. If ``Rnam1`` = NONE, deactivate all valid user subroutines. All characters are required:

            * ``USREFL`` - Allows user defined scalar field (body force) loads.

            * ``USERCV`` - Allows user defined convection (surface) loads.

            * ``USERPR`` - Allows user defined pressure (surface) loads.

            * ``USERFX`` - Allows user-defined heat flux (surface) loads.

            * ``USERCH`` - Allows user-defined charge density (surface) loads.

            * ``USERFD`` - Computes the complex load vector for the frequency domain logic.

            * ``USEROU`` - Allows user supplied element output.

            * ``USOLBEG`` - Allows user access before each solution.

            * ``ULDBEG`` - Allows user access before each load step.

            * ``USSBEG`` - Allows user access before each substep.

            * ``UITBEG`` - Allows user access before each equilibrium iteration.

            * ``UITFIN`` - Allows user access after each equilibrium iteration.

            * ``USSFIN`` - Allows user access after each substep.

            * ``ULDFIN`` - Allows user access after each load step.

            * ``USOLFIN`` - Allows user access after each solution.

            * ``UANFIN`` - Allows user access at end of run.

            * ``UELMATX`` - Allows user access to element matrices and load vectors.

            * ``UTIMEINC`` - Allows a user-defined time step, overriding the program-determined time step.

            * ``UCNVRG`` - Allows user-defined convergence checking, overriding the program-determined
              convergence.

        rnam4 : str
            User-defined solution subroutine names to be activated. Up to nine may be defined on one command or
            multiple commands may be used. If ``Rnam1`` = ALL, activate all valid user subroutines. If ``Rnam1`` = NONE, deactivate all valid user subroutines. All characters are required:

            * ``USREFL`` - Allows user defined scalar field (body force) loads.

            * ``USERCV`` - Allows user defined convection (surface) loads.

            * ``USERPR`` - Allows user defined pressure (surface) loads.

            * ``USERFX`` - Allows user-defined heat flux (surface) loads.

            * ``USERCH`` - Allows user-defined charge density (surface) loads.

            * ``USERFD`` - Computes the complex load vector for the frequency domain logic.

            * ``USEROU`` - Allows user supplied element output.

            * ``USOLBEG`` - Allows user access before each solution.

            * ``ULDBEG`` - Allows user access before each load step.

            * ``USSBEG`` - Allows user access before each substep.

            * ``UITBEG`` - Allows user access before each equilibrium iteration.

            * ``UITFIN`` - Allows user access after each equilibrium iteration.

            * ``USSFIN`` - Allows user access after each substep.

            * ``ULDFIN`` - Allows user access after each load step.

            * ``USOLFIN`` - Allows user access after each solution.

            * ``UANFIN`` - Allows user access at end of run.

            * ``UELMATX`` - Allows user access to element matrices and load vectors.

            * ``UTIMEINC`` - Allows a user-defined time step, overriding the program-determined time step.

            * ``UCNVRG`` - Allows user-defined convergence checking, overriding the program-determined
              convergence.

        rnam5 : str
            User-defined solution subroutine names to be activated. Up to nine may be defined on one command or
            multiple commands may be used. If ``Rnam1`` = ALL, activate all valid user subroutines. If ``Rnam1`` = NONE, deactivate all valid user subroutines. All characters are required:

            * ``USREFL`` - Allows user defined scalar field (body force) loads.

            * ``USERCV`` - Allows user defined convection (surface) loads.

            * ``USERPR`` - Allows user defined pressure (surface) loads.

            * ``USERFX`` - Allows user-defined heat flux (surface) loads.

            * ``USERCH`` - Allows user-defined charge density (surface) loads.

            * ``USERFD`` - Computes the complex load vector for the frequency domain logic.

            * ``USEROU`` - Allows user supplied element output.

            * ``USOLBEG`` - Allows user access before each solution.

            * ``ULDBEG`` - Allows user access before each load step.

            * ``USSBEG`` - Allows user access before each substep.

            * ``UITBEG`` - Allows user access before each equilibrium iteration.

            * ``UITFIN`` - Allows user access after each equilibrium iteration.

            * ``USSFIN`` - Allows user access after each substep.

            * ``ULDFIN`` - Allows user access after each load step.

            * ``USOLFIN`` - Allows user access after each solution.

            * ``UANFIN`` - Allows user access at end of run.

            * ``UELMATX`` - Allows user access to element matrices and load vectors.

            * ``UTIMEINC`` - Allows a user-defined time step, overriding the program-determined time step.

            * ``UCNVRG`` - Allows user-defined convergence checking, overriding the program-determined
              convergence.

        rnam6 : str
            User-defined solution subroutine names to be activated. Up to nine may be defined on one command or
            multiple commands may be used. If ``Rnam1`` = ALL, activate all valid user subroutines. If ``Rnam1`` = NONE, deactivate all valid user subroutines. All characters are required:

            * ``USREFL`` - Allows user defined scalar field (body force) loads.

            * ``USERCV`` - Allows user defined convection (surface) loads.

            * ``USERPR`` - Allows user defined pressure (surface) loads.

            * ``USERFX`` - Allows user-defined heat flux (surface) loads.

            * ``USERCH`` - Allows user-defined charge density (surface) loads.

            * ``USERFD`` - Computes the complex load vector for the frequency domain logic.

            * ``USEROU`` - Allows user supplied element output.

            * ``USOLBEG`` - Allows user access before each solution.

            * ``ULDBEG`` - Allows user access before each load step.

            * ``USSBEG`` - Allows user access before each substep.

            * ``UITBEG`` - Allows user access before each equilibrium iteration.

            * ``UITFIN`` - Allows user access after each equilibrium iteration.

            * ``USSFIN`` - Allows user access after each substep.

            * ``ULDFIN`` - Allows user access after each load step.

            * ``USOLFIN`` - Allows user access after each solution.

            * ``UANFIN`` - Allows user access at end of run.

            * ``UELMATX`` - Allows user access to element matrices and load vectors.

            * ``UTIMEINC`` - Allows a user-defined time step, overriding the program-determined time step.

            * ``UCNVRG`` - Allows user-defined convergence checking, overriding the program-determined
              convergence.

        rnam7 : str
            User-defined solution subroutine names to be activated. Up to nine may be defined on one command or
            multiple commands may be used. If ``Rnam1`` = ALL, activate all valid user subroutines. If ``Rnam1`` = NONE, deactivate all valid user subroutines. All characters are required:

            * ``USREFL`` - Allows user defined scalar field (body force) loads.

            * ``USERCV`` - Allows user defined convection (surface) loads.

            * ``USERPR`` - Allows user defined pressure (surface) loads.

            * ``USERFX`` - Allows user-defined heat flux (surface) loads.

            * ``USERCH`` - Allows user-defined charge density (surface) loads.

            * ``USERFD`` - Computes the complex load vector for the frequency domain logic.

            * ``USEROU`` - Allows user supplied element output.

            * ``USOLBEG`` - Allows user access before each solution.

            * ``ULDBEG`` - Allows user access before each load step.

            * ``USSBEG`` - Allows user access before each substep.

            * ``UITBEG`` - Allows user access before each equilibrium iteration.

            * ``UITFIN`` - Allows user access after each equilibrium iteration.

            * ``USSFIN`` - Allows user access after each substep.

            * ``ULDFIN`` - Allows user access after each load step.

            * ``USOLFIN`` - Allows user access after each solution.

            * ``UANFIN`` - Allows user access at end of run.

            * ``UELMATX`` - Allows user access to element matrices and load vectors.

            * ``UTIMEINC`` - Allows a user-defined time step, overriding the program-determined time step.

            * ``UCNVRG`` - Allows user-defined convergence checking, overriding the program-determined
              convergence.

        rnam8 : str
            User-defined solution subroutine names to be activated. Up to nine may be defined on one command or
            multiple commands may be used. If ``Rnam1`` = ALL, activate all valid user subroutines. If ``Rnam1`` = NONE, deactivate all valid user subroutines. All characters are required:

            * ``USREFL`` - Allows user defined scalar field (body force) loads.

            * ``USERCV`` - Allows user defined convection (surface) loads.

            * ``USERPR`` - Allows user defined pressure (surface) loads.

            * ``USERFX`` - Allows user-defined heat flux (surface) loads.

            * ``USERCH`` - Allows user-defined charge density (surface) loads.

            * ``USERFD`` - Computes the complex load vector for the frequency domain logic.

            * ``USEROU`` - Allows user supplied element output.

            * ``USOLBEG`` - Allows user access before each solution.

            * ``ULDBEG`` - Allows user access before each load step.

            * ``USSBEG`` - Allows user access before each substep.

            * ``UITBEG`` - Allows user access before each equilibrium iteration.

            * ``UITFIN`` - Allows user access after each equilibrium iteration.

            * ``USSFIN`` - Allows user access after each substep.

            * ``ULDFIN`` - Allows user access after each load step.

            * ``USOLFIN`` - Allows user access after each solution.

            * ``UANFIN`` - Allows user access at end of run.

            * ``UELMATX`` - Allows user access to element matrices and load vectors.

            * ``UTIMEINC`` - Allows a user-defined time step, overriding the program-determined time step.

            * ``UCNVRG`` - Allows user-defined convergence checking, overriding the program-determined
              convergence.

        rnam9 : str
            User-defined solution subroutine names to be activated. Up to nine may be defined on one command or
            multiple commands may be used. If ``Rnam1`` = ALL, activate all valid user subroutines. If ``Rnam1`` = NONE, deactivate all valid user subroutines. All characters are required:

            * ``USREFL`` - Allows user defined scalar field (body force) loads.

            * ``USERCV`` - Allows user defined convection (surface) loads.

            * ``USERPR`` - Allows user defined pressure (surface) loads.

            * ``USERFX`` - Allows user-defined heat flux (surface) loads.

            * ``USERCH`` - Allows user-defined charge density (surface) loads.

            * ``USERFD`` - Computes the complex load vector for the frequency domain logic.

            * ``USEROU`` - Allows user supplied element output.

            * ``USOLBEG`` - Allows user access before each solution.

            * ``ULDBEG`` - Allows user access before each load step.

            * ``USSBEG`` - Allows user access before each substep.

            * ``UITBEG`` - Allows user access before each equilibrium iteration.

            * ``UITFIN`` - Allows user access after each equilibrium iteration.

            * ``USSFIN`` - Allows user access after each substep.

            * ``ULDFIN`` - Allows user access after each load step.

            * ``USOLFIN`` - Allows user access after each solution.

            * ``UANFIN`` - Allows user access at end of run.

            * ``UELMATX`` - Allows user access to element matrices and load vectors.

            * ``UTIMEINC`` - Allows a user-defined time step, overriding the program-determined time step.

            * ``UCNVRG`` - Allows user-defined convergence checking, overriding the program-determined
              convergence.

        Notes
        -----

        .. _USRCAL_notes:

        Allows certain user-solution subroutines to be activated or deactivated (system-dependent). This
        command only affects the subroutines named. Other user subroutines (such as user elements, user
        creep, etc.) have their own activation controls described with the feature.

        The UAnBeg subroutine that allows user access at the start of a run does not require activation by
        this command; it is automatically activated when the program is started.

        The routines are commented and should be listed after performing a custom installation from the
        distribution media for more details. See also the `Advanced Analysis Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_adv/advoceanloading.html>`_ for a
        general description of user-
        programmable features.

        You must have system permission, system access, and knowledge to write, compile, and link the
        appropriate subroutines into the program at your site.

        All routines should be written in FORTRAN. (For more information about FORTRAN compilers, refer to
        either the `Ansys, Inc. Windows Installation Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/installation/win_product_table.html>`_ or
        the `Ansys, Inc. Linux Installation Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/installation/lin_product_table.html>`_ for
        details specific to your platform or operating system.)

        Issue :ref:`usrcal`,STAT to list the status of these user subroutines.

        Because a user-programmed subroutine is a nonstandard use of the program, the verification of any
        Mechanical APDL run incorporating these commands is entirely your responsibility. In any contact
        with
        customer support regarding the performance of a custom version of Mechanical APDL, explicitly state
        that a
        user-programmable feature has been used.

        This command is also valid in PREP7.
        """
        command = f"USRCAL,{rnam1},{rnam2},{rnam3},{rnam4},{rnam5},{rnam6},{rnam7},{rnam8},{rnam9}"
        return self.run(command, **kwargs)

    def wrfull(self, ldstep: str = "", **kwargs):
        r"""Stops solution after assembling global matrices.

        Mechanical APDL Command: `WRFULL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_WRFULL.html>`_

        Parameters
        ----------
        ldstep : str
            Specify action to take:

            * ``OFF or 0`` - Turn off feature (default)

            * ``N`` - Turn on feature and set it to stop after assembling the global matrices and writing the
              :file:`.FULL` file for load step N.

        Notes
        -----

        .. _WRFULL_notes:

        This command is used in conjunction with the :ref:`solve` command to generate the assembled matrix
        file ( :file:`.FULL` file) only. The element matrices are assembled into the relevant global
        matrices for the particular analysis being performed and the :file:`.FULL` file is written. Equation
        solution and the output of data to the results file are skipped. To dump the matrices written on the
        :file:`.FULL` file into Harwell-Boeing format, use the :ref:`hbmat` command in /AUX2. To copy the
        matrices to a postscript format that can be viewed graphically, use the :ref:`psmat` command.

        To use the :ref:`lssolve` macro with this command, you may need to modify the :ref:`lssolve` macro
        to properly stop at the load step of interest.

        This command only valid for linear static, full harmonic, and full transient analyses when the
        sparse direct solver is selected. This command is also valid for buckling or modal analyses with any
        mode extraction method. This command is not valid for nonlinear analyses. It is not supported in a
        linear perturbation analysis.

        In general, the assembled matrix file :file:`.FULL` contains stiffness, mass, and damping matrices.
        However, the availability of the matrices depends on the analysis type chosen when the file is
        written. Some analyses do not write the matrices individually but instead write combined matrices.
        For example, a full transient writes a combined stiffness/mass/damping matrix to the full file.
        """
        command = f"WRFULL,{ldstep}"
        return self.run(command, **kwargs)
