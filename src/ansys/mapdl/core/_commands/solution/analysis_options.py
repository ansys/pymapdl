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


class AnalysisOptions:

    def abextract(self, mode1: str = "", mode2: str = "", **kwargs):
        r"""Extracts the alpha-beta damping multipliers for Rayleigh damping.

        Mechanical APDL Command: `ABEXTRACT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ABEXTRACT.html>`_

        Parameters
        ----------
        mode1 : str
            First mode number.

        mode2 : str
            Second mode number.

        Notes
        -----

        .. _ABEXTRACT_notes:

        :ref:`abextract` calls the command macro :ref:`dmpext` to extract the damping ratio of ``MODE1`` and
        ``MODE2`` and then computes the Alpha and Beta damping multipliers for use in a subsequent
        structural harmonic or transient analysis. See `Damping
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STR1D.html#strelemdamp>`_ in
        the `Structural Analysis Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/str_enercalc_app.html>`_ for more
        information on the alpha and beta damping multipliers. The damping multipliers
        are stored in parameters ALPHADMP and BETADMP and can be applied using the :ref:`alphad` and
        :ref:`betad` commands. Before calling :ref:`abextract`, you must issue :ref:`rmflvec` to extract the
        modal displacements. In addition, a node component FLUN must exist from all ``FLUID136`` nodes. See
         for more information on thin film analyses.

        This command is also valid in PREP7. Distributed-Memory Parallel (DMP) Restriction This command is
        not supported in a DMP solution.
        """
        command = f"ABEXTRACT,{mode1},{mode2}"
        return self.run(command, **kwargs)

    def accoption(self, activate: str = "", **kwargs):
        r"""Specifies GPU accelerator capability options.

        Mechanical APDL Command: `ACCOPTION <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ACCOPTION.html>`_

        Parameters
        ----------
        activate : str
            Activates the GPU accelerator capability within the equation solvers.

            * ``OFF`` - Do not use GPU accelerator.

            * ``ON`` - Use GPU accelerator.

        Notes
        -----

        .. warning::

           This function contains specificities regarding the argument definitions.
           Please refer to the `command documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ACCOPTION.html>`_
           for further explanations.

        **Argument Descriptions**

        .. _ACCOPTION_argdescript:

        * ``activate : str`` - Activates the GPU accelerator capability within the equation solvers.

          * ``OFF`` - Do not use GPU accelerator.

          * ``ON`` - Use GPU accelerator.

        .. _ACCOPTION_notes:

        The GPU accelerator capability requires specific hardware to be installed on the machine. See the
        appropriate Ansys, Inc. Installation Guide ( Windows or Linux ) for a list of supported GPU
        hardware. Use of this capability also requires HPC licensing. For more information, see `GPU
        Accelerator Capability
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_dan/gputrouble.html>`_

        The GPU accelerator capability is available for the sparse direct solver and the PCG and JCG
        iterative solvers. Static, buckling, modal, full harmonic, and full transient analyses are
        supported. For buckling analyses, the Block Lanczos and Subspace eigensolvers are supported. For
        modal analyses, only the Block Lanczos, PCG Lanczos, Subspace, Unsymmetric, and Damped eigensolvers
        are supported. Activating this capability when using other equation solvers or other analysis types
        has no effect.

        The GPU accelerator capability is supported only on the Windows 64-bit and Linux 64-bit platforms.
        """
        command = f"ACCOPTION,{activate}"
        return self.run(command, **kwargs)

    def adams(
        self,
        nmodes: str = "",
        kstress: int | str = "",
        kshell: int | str = "",
        **kwargs,
    ):
        r"""Performs solutions and writes flexible body information to a modal neutral file (
        :file:`Jobname.MNF` ) for use in an ADAMS analysis.

        Mechanical APDL Command: `ADAMS <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ADAMS.html>`_

        Parameters
        ----------
        nmodes : str
            Number of normal modes to be written to :file:`Jobname.MNF` file (no default).

        kstress : int or str
            Specifies whether to write stress or strain results:

            * ``0`` - Do not write stress or strain results (default).

            * ``1`` - Write stress results.

            * ``2`` - Write strain results.

            * ``3`` - Write both stress and strain results.

        kshell : int or str
            Shell element output location. This option is valid only for shell elements.

            * ``0, 1`` - Shell top surface (default).

            * ``2`` - Shell middle surface.

            * ``3`` - Shell bottom surface.

        Notes
        -----

        .. _ADAMS_notes:

        :ref:`adams` invokes a predefined Mechanical APDL macro that solves a series of analyses and then
        writes
        the modal neutral file, :file:`Jobname.MNF`. This file can be imported into the ADAMS program in
        order to perform a rigid body dynamics simulation. For detailed information about how to use the
        :ref:`adams` command macro to create a modal neutral file, see `Rigid Body Dynamics and the Ansys-
        Adams Interface
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_substr/advmeth2402.html>`_

        Before running the :ref:`adams` command macro, you must specify the units with the :ref:`units`
        command. The interface points should be the only selected nodes when the command macro is initiated.
        (Interface points are nodes where constraints may be applied in ADAMS.) Only selected elements will
        be considered in the calculations.

        By default, stress and strain data is transferred to the ADAMS program for all nodes, as specified
        by the ``KSTRESS`` value. If you want to transfer stress/strain data for only a subset of nodes,
        select the desired subset and create a node component named STRESS before running the :ref:`adams`
        command macro. For example, you may want to select exterior nodes for the purpose of visualization
        in the ADAMS program.

        The default filename for the modal neutral file is :file:`Jobname.MNF`. In interactive (GUI) mode,
        you can specify a filename other than :file:`Jobname.MNF`. In batch mode, there is no option to
        change the filename, and the modal neutral file is always written to :file:`JobnameMNF`.
        """
        command = f"ADAMS,{nmodes},{kstress},{kshell}"
        return self.run(command, **kwargs)

    def antype(
        self,
        antype: str = "",
        status: str = "",
        ldstep: str = "",
        substep: str = "",
        action: str = "",
        prelp: str = "",
        **kwargs,
    ):
        r"""Specifies the analysis type and restart status.

        Mechanical APDL Command: `ANTYPE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ANTYPE.html>`_

        **Command default:**

        .. _ANTYPE_default:

        New static analysis.

        Parameters
        ----------
        antype : str
            Analysis type (defaults to the previously specified analysis type, or to STATIC if none specified):

            * ``STATIC or 0`` - Perform a static analysis. Valid for all degrees of freedom.

            * ``BUCKLE or 1`` - Perform a buckling analysis. Implies that a previous static solution was
              performed with prestress effects calculated ( :ref:`pstres`,ON). Valid for structural degrees of
              freedom only.

            * ``MODAL or 2`` - Perform a modal analysis. Valid for structural and fluid degrees of freedom.

            * ``HARMIC or 3`` - Perform a harmonic analysis. Valid for structural, fluid, magnetic, and
              electrical degrees of freedom.

            * ``TRANS or 4`` - Perform a transient analysis. Valid for all degrees of freedom.

            * ``SUBSTR or 7`` - Perform a substructure analysis. Valid for all degrees of freedom.

            * ``SPECTR or 8`` - Perform a spectrum analysis. Implies that a previous modal analysis was
              performed. Valid for structural degrees of freedom only.

            * ``SOIL or 9`` - Perform a soil analysis including geostatic stress equilibrium or consolidation.
              Valid for structural and fluid-pore-pressure degrees of freedom.

        status : str
            Specifies the status of the analysis (new or restart):

            * ``NEW`` - Specifies a new analysis (default). If NEW, the remaining fields on this command are
              ignored.

            * ``RESTART`` - Specifies a restart of a previous analysis. Valid for static, modal, and transient
              (full or mode- superposition method) analyses. For more information about restarting static and
              transient analyses, see `Multiframe Restart
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/Hlp_G_BAS3_12.html#BASmultprocmap52199>`_
              `Modal Analysis Restart
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/Hlp_G_BAS3_12.html#modalrestex>`_

              Multiframe restart is also valid for harmonic analysis, but is limited to 2D magnetic analysis only.

              A substructure analysis (backsubstitution method only) can be restarted for the purpose of
              generating additional load vectors. For more information, see the :ref:`seopt` command and `Applying
              Loads and Creating the Superelement Matrices
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_substr/aKa7uq1a9ldm.html#substr_usingsubstr_appload>`_

        ldstep : str
            Specifies the load step at which a multiframe restart begins.

            For full transient and nonlinear static analyses, the default is the highest load step number
            found in the :file:`Jobname.Rnnn` files for the current jobname in the current directory.

            For mode-superposition transient analyses, the default is none.

        substep : str
            Specifies the substep at which a multiframe restart begins.

            For full transient and nonlinear static analyses, the default is the highest substep number
            found for the specified ``LDSTEP`` in the :file:`Jobname.Rnnn` files in the current directory.

            For mode-superposition transient analyses, the default is none.

        action : str
            Specifies the manner of a multiframe restart.

            * ``CONTINUE`` - The program continues the analysis based on the specified ``LDSTEP`` and
              ``SUBSTEP`` (default). The current load step is continued. If the end of the load step is
              encountered in the :file:`.Rnnn` file, a new load step is started. The program deletes all
              :file:`.Rnnn` files, or :file:`.Mnnn` files for mode-superposition transient analyses, beyond the
              point of restart and updates the :file:`.LDHI` file if a new load step is encountered.

            * ``ENDSTEP`` - At restart, force the specified load step ( ``LDSTEP`` ) to end at the specified
              substep ( ``SUBSTEP`` ), even though the end of the current load step has not been reached. At the
              end of the specified substep, all loadings are scaled to the level of the current ending and stored
              in the :file:`.LDHI` file. A run following this ENDSTEP starts a new load step. This capability
              allows you to change the load level in the middle of a load step. The program updates the
              :file:`.LDHI` file and deletes all :file:`.Rnnn` files, or :file:`.Mnnn` files for mode-
              superposition transient analyses, beyond the point of ENDSTEP. The :file:`.Rnnn` or :file:`.Mnnn`
              file at the point of ENDSTEP are rewritten to record the rescaled load level.

            * ``RSTCREATE`` - At restart, retrieve information to be written to the results file for the
              specified load step ( ``LDSTEP`` ) and substep ( ``SUBSTEP`` ). Be sure to use :ref:`outres` to
              write the results to the results file. This action does not affect the :file:`.LDHI` or
              :file:`.Rnnn` files. Previous items stored in the results file at and beyond the point of RSTCREATE
              are deleted. This option cannot be used to restart a mode-superposition transient analysis.

            * ``PERTURB`` - At restart, a linear perturbation analysis (static, modal, buckling, or full
              harmonic) is performed for the specified load step ( ``LDSTEP`` ) and substep ( ``SUBSTEP`` ). This
              action does not affect the :file:`.LDHI`, :file:`.Rnnn`, or :file:`.RST` files.

              For a `linear perturbation
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/strlinpertother.html>`_ analysis,
              set ``Action`` = PERTURB; otherwise, the existing restart files, such as the :file:`.LDHI`,
              :file:`.Rnnn`, or :file:`.RST` file, may be modified by the linear perturbation analysis. Issue the
              :ref:`perturb` command to indicate the desired analysis type (STATIC, MODAL, BUCKLE, HARMONIC, or
              SUBSTR ).

        prelp : str
            Flag indicating whether a subsequent linear perturbation will be performed:

            * ``YES`` - Specifies the first static analysis with a sequential linear perturbation analysis.
              Setting PRELP = YES is necessary for acoustics-structural interaction linear perturbation analysis,
              if the :ref:`morph` command with ``StrOpt`` = YES is not issued.

            * ``NO`` - No specification for a subsequent linear perturbation (default).

        Notes
        -----

        .. _ANTYPE_notes:

        If using the :ref:`antype` command to change the analysis type in the same SOLVE session, the
        program issues the following message: "Some analysis options have been reset to their defaults.
        Please verify current settings or respecify as required." Typically, the program resets commands
        such as :ref:`nlgeom` and :ref:`eqslv` to their default values.

        If you want to read in view factors after restarting a radiation analysis, issue VFOPT,READ after
        ANTYPE,,REST.

        The analysis type ( ``Antype`` ) cannot be changed if a restart is specified. Always save parameters
        before doing a restart. For more information on the different types of restart, see `Restarting an
        Analysis
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/Hlp_G_BAS3_12.html#bassolumodres>`_

        This command is also valid in PREP7.

        .. _ANTYPE_extranote1:

        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.
        """
        command = f"ANTYPE,{antype},{status},{ldstep},{substep},{action},,{prelp}"
        return self.run(command, **kwargs)

    def ascres(self, opt: str = "", **kwargs):
        r"""Specifies the output type for an acoustic scattering analysis.

        Mechanical APDL Command: `ASCRES <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ASCRES.html>`_

        Parameters
        ----------
        opt : str
            Output option:

            * ``TOTAL`` - Output the total pressure field (default).

            * ``SCAT`` - Output the scattered pressure field.

        Notes
        -----

        .. _ASCRES_notes:

        Use the :ref:`ascres` command to specify the output type for an acoustic scattering analysis.

        The scattered option ( ``Opt`` = SCAT) provides a scattered pressure output, p:sub:`sc`, required
        for calculating target strength (TS).

        The default behavior ( ``Opt`` = TOTAL) provides a sum of the incident and scattering fields, p
        :sup:`total` = p :sup:`inc` + p :sup:`sc`.

        Issue the :ref:`awave` command to define the incident pressure p :sup:`inc`. If the :ref:`awave`
        command is defined with ``Opt2`` = INT, only the total pressure field is output regardless of the
        :ref:`ascres`, ``Opt`` command.
        """
        command = f"ASCRES,{opt}"
        return self.run(command, **kwargs)

    def asol(self, lab: str = "", opt: str = "", **kwargs):
        r"""Specifies the acoustic solver with scattered field formulation.

        Mechanical APDL Command: `ASOL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ASOL.html>`_

        Parameters
        ----------
        lab : str
            Acoustic solver specification (no default):

            * ``SCAT`` - Set acoustic solver to the scattered field formulation.

        opt : str
            Option identifying an acoustic solver status:

            * ``OFF`` - Deactivate the specified acoustic solver (default).

            * ``ON`` - Activate the specified acoustic solver.

        Notes
        -----

        .. _ASOL_notes:

        Use the :ref:`asol` command to activate the specified acoustic solution process.

        The scattered option ( ``Lab`` = SCAT) sets the acoustic solver to the scattered-pressure field
        formulation.

        Issue the :ref:`awave` command to define the incident pressure p :sup:`inc`. If the :ref:`awave`
        command is defined with ``Opt2`` = INT, the acoustic solver is set to the scattered field
        formulation regardless of the :ref:`asol` command issued.
        """
        command = f"ASOL,{lab},{opt}"
        return self.run(command, **kwargs)

    def bcsoption(
        self,
        memory_option: str = "",
        memory_size: str = "",
        solve_info: str = "",
        **kwargs,
    ):
        r"""Sets memory option for the sparse solver.

        Mechanical APDL Command: `BCSOPTION <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_BCSOPTION.html>`_

        **Command default:**

        .. _BCSOPTION_default:

        Automatic memory allocation is used.

        Parameters
        ----------

        memory_option : str
            Memory allocation option:

            * ``DEFAULT`` - Use the default memory allocation strategy for the sparse solver. The default
              strategy attempts to run in the INCORE memory mode. If there is not enough available physical memory
              when the solver starts to run in the INCORE memory mode, the solver will then attempt to run in the
              OUTOFCORE memory mode.

            * ``INCORE`` - Use a memory allocation strategy in the sparse solver that will attempt to obtain
              enough memory to run with the entire factorized matrix in memory. This option uses the most amount
              of memory and should avoid doing any I/O. By avoiding I/O, this option achieves optimal solver
              performance. However, a significant amount of memory is required to run in this mode, and it is only
              recommended on machines with a large amount of memory. If the allocation for in-core memory fails,
              the solver will automatically revert to out-of-core memory mode.

            * ``OUTOFCORE`` - Use a memory allocation strategy in the sparse solver that will attempt to
              allocate only enough work space to factor each individual frontal matrix in memory, but will store
              the entire factorized matrix on disk. Typically, this memory mode results in poor performance due to
              the potential bottleneck caused by the I/O to the various files written by the solver.

            * ``FORCE`` - This option, when used in conjunction with the ``Memory_Size`` option, allows you to
              force the sparse solver to run with a specific amount of memory. This option is only recommended for
              the advanced user who understands sparse solver memory requirements for the problem being solved,
              understands the physical memory on the system, and wants to control the sparse solver memory usage.

        memory_size : str
            Initial memory size allocation for the sparse solver in GB. This argument allows you to tune the
            sparse solver memory and is not generally required. Although there is no upper limit for
            ``Memory_Size``, the ``Memory_Size`` setting should always be well within the physical memory
            available, but not so small as to cause the sparse solver to run out of memory. Warnings and/or
            errors from the sparse solver will appear if this value is set too low. If the FORCE memory
            option is used, this value is the amount of memory allocated for the entire duration of the
            sparse solver solution.

        solve_info : str
            Solver output option:

            * ``OFF`` - Turns off additional output printing from the sparse solver (default).

            * ``PERFORMANCE`` - Turns on additional output printing from the sparse solver, including a
              performance summary and a summary of file I/O for the sparse solver. Information on memory usage
              during assembly of the global matrix (that is, creation of the :file:`Jobname.FULL` file) is also
              printed with this option.

        Notes
        -----

        .. _BCSOPTION_notes:

        This command controls options related to the sparse solver in all analysis types where the sparse
        solver can be used. It also controls the Block Lanczos eigensolver in a modal or buckling analysis.

        The sparse solver runs from one large work space (that is, one large memory allocation). The amount
        of memory required for the sparse solver is unknown until the matrix structure is preprocessed,
        including equation reordering. The amount of memory allocated for the sparse solver is then
        dynamically adjusted to supply the solver what it needs to compute the solution.

        If you have a very large memory system, you may want to try selecting the INCORE memory mode for
        larger jobs to improve performance. When running the sparse solver on a machine with very slow I/O
        performance (for example, slow hard drive speed), you may want to try using the INCORE memory mode
        to achieve better performance. However, doing so may require much more memory compared to running in
        the OUTOFCORE memory mode.

        Running with the INCORE memory mode is best for jobs which comfortably fit within the limits of the
        physical memory on a given system. If the sparse solver work space exceeds physical memory size, the
        system will be forced to use virtual memory (or the system page/swap file). In this case, it is
        typically more efficient to run with the OUTOFCORE memory mode. Assuming the job fits comfortably
        within the limits of the machine, running with the INCORE memory mode is often ideal for jobs where
        repeated solves are performed for a single matrix factorization. This occurs in a modal or buckling
        analysis or when doing multiple load steps in a linear, static analysis.

        For repeated runs with the sparse solver, you may set the initial sparse solver memory allocation to
        the amount required for factorization. This strategy reduces the frequency of allocation and
        reallocation in the run to make the INCORE option fully effective. If you have a very large memory
        system, you may use the ``Memory_Size`` argument to increase the maximum size attempted for in-core
        runs.
        """
        command = f"BCSOPTION,,{memory_option},{memory_size},,,{solve_info}"
        return self.run(command, **kwargs)

    def cjump(
        self,
        option: str = "",
        input1: str = "",
        input2: str = "",
        input3: str = "",
        input4: str = "",
        input5: str = "",
        input6: str = "",
        input7: str = "",
        input8: str = "",
        **kwargs,
    ):
        r"""Initiates a `cycle-jump analysis
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_adv/advcycjumpmethod.html#>`_.

        Mechanical APDL Command: `CJUMP <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CJUMP.html>`_

        **Command default:**

        .. _CJUMP_default:

        Cycle jump analysis is disabled.

        Parameters
        ----------
        option : str
            Option to be applied:

            * ``CRIT`` - Jump criterion.

            * ``INTENT`` - Declaration of cycle jump analysis intent. For an analysis that begins with a
              standard solution, specify before the first :ref:`solve` command.

            * ``MINCYC`` - Minimum number of cycles before a jump is allowed (and, if desired, the `empirical
              adjustment of minimum intermediate cycles
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_adv/advcycjumpmethod.html#eq913e29a3-98a9-46aa-a8b0-e222d972a0cf>`_
              ).

            * ``INICYC`` - Minimum number of initial cycles before a jump is allowed.

            * ``MAXJUMP`` - Maximum allowable jump.

            * ``RELTIME`` - Relative time.

            * ``CONTROL`` - Control-variable selection.

            * ``CNMT`` - Material-ID-dependent jump control.

            * ``ADCR`` - Material-ID- and/or control-variable-dependent jump criteria.

            * ``CALC`` - Jump-calculation option.

            * ``PERC`` - Statistical-jump calculation.

            * ``OUTP`` - Diagnostic information output.

        input1 : str
            Additional input according to the specified Option :  This command contains some tables and
            extra information which can be inspected in the original documentation pointed above.

        input2 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CJUMP.html>`_ for further
            information.

        input3 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CJUMP.html>`_ for further
            information.

        input4 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CJUMP.html>`_ for further
            information.

        input5 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CJUMP.html>`_ for further
            information.

        input6 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CJUMP.html>`_ for further
            information.

        input7 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CJUMP.html>`_ for further
            information.

        input8 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CJUMP.html>`_ for further
            information.

        Notes
        -----

        .. _CJUMP_notes:

        When ``Option`` = CONTROL, any input of a control variable replaces the default (S). If stress is
        also needed in combination with another control variable (or variables), you must specify it
        explicitly.

        :ref:`cjump` requires a corresponding cyclic loading analysis ( :ref:`cload` ).

        For more information, see `Cycle-Jump Analysis
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_adv/advcycjumpmethod.html#>`_

        This command is also valid in PREP7 ( :ref:`prep7` ).
        """
        command = f"CJUMP,{option},{input1},{input2},{input3},{input4},{input5},{input6},{input7},{input8}"
        return self.run(command, **kwargs)

    def cload(self, option: str = "", input1: str = "", **kwargs):
        r"""Initiates a `cyclic-loading analysis
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_adv/advcycloadprocess.html#>`_.

        Mechanical APDL Command: `CLOAD <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CLOAD.html>`_

        **Command default:**

        .. _CLOAD_default:

        Cyclic load analysis is disabled.

        Parameters
        ----------
        option : str
            Option to be applied:

            * ``DEFINE`` - Mark tabular array as a cyclic load table.

            * ``CYCNUM`` - Total number of cycles.

            * ``CYCTIME`` - Cycle time.

            * ``TSTEP`` - Enable time-point-range time-stepping.

            * ``OUTR`` - Select time points for output.

        input1 : str
            Additional input according to the specified Option :  This command contains some tables and
            extra information which can be inspected in the original documentation pointed above.

        Notes
        -----

        .. _CLOAD_notes:

        For more information, see `Cyclic-Loading Analysis
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_adv/advcycloadprocess.html#>`_

        This command is also valid in PREP7 ( :ref:`prep7` ).
        """
        command = f"CLOAD,{option},{input1}"
        return self.run(command, **kwargs)

    def cmatrix(
        self,
        symfac: str = "",
        condname: str = "",
        numcond: str = "",
        grndkey: str = "",
        capname: str = "",
        **kwargs,
    ):
        r"""Performs electrostatic field solutions and calculates the self and mutual capacitances between
        multiple conductors.

        Mechanical APDL Command: `CMATRIX <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CMATRIX.html>`_

        Parameters
        ----------
        symfac : str
            Geometric symmetry factor. Capacitance values are scaled by this factor which represents the
            fraction of the total device modeled. Defaults to 1.

        condname : str
            Alpha-numeric prefix identifier used in defining named conductor components.

        numcond : str
            Total Number of Components. If a ground is modeled, it is to be included as a component. If a
            ground is not modeled, but infinite elements are used to model the far-field ground, a named
            component for the far-field ground is not required.

        grndkey : int or str
            Ground key:

            * ``0`` - Ground is one of the components, which is not at infinity.

            * ``1`` - Ground is at infinity (modeled by infinite elements).

        capname : str
            Array name for computed capacitance matrix. Defaults to :ref:`cmatrix`.

        Notes
        -----

        .. _CMATRIX_notes:

        To invoke the :ref:`cmatrix` macro, the exterior nodes of each conductor must be grouped into
        individual components using the :ref:`cm` command. Each set of independent components is assigned a
        component name with a common prefix followed by the conductor number. A conductor system with a
        ground must also include the ground nodes as a component. The ground component is numbered last in
        the component name sequence.

        A ground capacitance matrix relates charge to a voltage vector. A ground matrix cannot be applied to
        a circuit modeler. The lumped capacitance matrix is a combination of lumped "arrangements" of
        voltage differences between conductors. Use the lumped capacitance terms in a circuit modeler to
        represent capacitances between conductors.

        Enclose all name-strings in single quotes in the :ref:`cmatrix` command line.

        See the `Mechanical APDL Theory Reference
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_biblio.html>`_ for details.

        This command does not support multiframe restarts.
        """
        command = f"CMATRIX,{symfac},'{condname}',{numcond},{grndkey},'{capname}'"
        return self.run(command, **kwargs)

    def cmsopt(
        self,
        cmsmeth: str = "",
        nmode: str = "",
        freqb: str = "",
        freqe: str = "",
        fbddef: str = "",
        fbdval: str = "",
        iokey: str = "",
        elcalc: str = "",
        eigmeth: str = "",
        nstartvn: str = "",
        **kwargs,
    ):
        r"""Specifies component mode synthesis (CMS) analysis options.

        Mechanical APDL Command: `CMSOPT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CMSOPT.html>`_

        **Command default:**

        .. _CMSOPT_default:

        Issuing the :ref:`cmsopt` command with no arguments is invalid. You must specify at least the CMS
        method ( ``Cmsmeth`` ) and the number of modes ( ``NMODE`` ). In a free-interface ( ``Cmsmeth`` =
        FREE) or residual-flexible free-interface ( ``Cmsmeth`` = RFFB) CMS analysis, the default method for
        determining rigid body modes is FAUTO (automatic).

        Parameters
        ----------
        cmsmeth : str
            The component mode synthesis `method <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_substr/advcms.html#pseudo_constraints_FI_CMS>`_ to use. This value is required.

            * ``FIX`` - Fixed-interface method.

            * ``FREE`` - Free-interface method.

            * ``RFFB`` - Residual-flexible free-interface method.

        nmode : str
            The number of normal modes extracted and used in the superelement generation. This value is
            required; the minimum is 1.

        freqb : str
            Beginning, or lower end, of frequency range of interest. This value is optional.

            The program always sets this value to zero if the residual-flexible free-interface method (
            ``Cmsmeth`` = RFFB) or the free-interface method ( ``Cmsmeth`` = FREE) is specified via
            :ref:`resvec`.

        freqe : str
            Ending, or upper end, of frequency range of interest. This value is optional.

        fbddef : str
            In a free-interface ( ``Cmsmeth`` = FREE) or residual-flexible free-interface ( ``Cmsmeth`` = RFFB) CMS analysis, the method to use for defining free body modes:

            * ``FNUM`` - The number ( ``FDBVAL`` ) of rigid body modes in the calculation.

            * ``FTOL`` - Employ a specified tolerance ( ``FDBVAL`` ) to determine rigid body modes in the
              calculation.

            * ``FAUTO`` - Automatically determine rigid body modes in the calculation. This method is the
              default.

            * ``RIGID`` - If no rigid body modes exist, define your own via the :ref:`rigid` command.

        fbdval : str
            In a free-interface CMS analysis ( ``Cmsmeth`` = FREE), the number of rigid body modes if
            ``Fbddef`` = FNUM (where the value is an integer from 0 through 6), or the tolerance to employ
            if ``Fbddef`` = FTOL (where the value is a positive real number representing rad/sec). This
            value is required only when ``Fbddef`` = FNUM or ``Fbddef`` = FTOL; otherwise, any specified
            value is ignored.

        iokey : str
            Output key to control writing of the complete transformation matrix on the :file:`.cms` file to the
            :file:`.tcms` file (FIX or FREE methods) or body properties to the :file:`.EXB` file (FIX method).

            * ``CMS`` - Write the complete transformation matrix of the nodal component on the :file:`.cms`
              file. For more information, see.

            * ``TCMS`` - Write the transformation matrix of the nodal component defined via :ref:`outpr` to a
              :file:`.tcms` file. For more information, see.

            * ``EXB`` - Write a body property input file ( :file:`.EXB` file) containing the condensed
              substructure matrices and other body properties for use with AVL EXCITE. For more information, see
              `Ansys Interface to AVL EXCITE
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_substr/substrexbcms.html>`_

        elcalc : str
            Element calculation key:

            * ``NO`` - Do not calculate element results (default).

            * ``YES`` - Calculate element results and write them to the :file:`.cms` file for the expansion
              pass.

        eigmeth : str
            Mode extraction method to be used for the symmetric eigenvalue problem during the `generation pass
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_substr/advcmssuperelem.html#usingcms_elemcalc>`_
            :

            * ``LANB`` - Block Lanczos algorithm (default).

            * ``SUBS`` - Subspace algorithm.

            * ``SNODE`` - Supernode algorithm.

        nstartvn : str
            Node number to be assigned to the first virtual node created to store the generalized
            coordinates. See :ref:`CMSOPT_notes` for more information.

        Notes
        -----

        .. _CMSOPT_notes:

        CMS supports damping matrix reduction when a damping matrix exists. Set the matrix generation key to
        3 ( :ref:`seopt`, ``Sename``, ``SEMATR`` ) to generate and then reduce stiffness, mass, and damping
        matrices.

        CMS does not support the :ref:`seopt`,,,,,RESOLVE command. Instead, the program sets the expansion
        method for the expansion pass ( ``EXPMTH`` ) to BACKSUB.

        By default, the static constraint modes are not written to the :file:`.cms` file for the fixed-
        interface and free-interface methods. Issue ``IOkey`` = CMS to write them.

        If ``IOkey`` = TCMS, the transformation matrix is printed out and written to the :file:`.tcms` file
        when the :ref:`outpr` command is issued with ``ITEM`` = NSOL and ``FREQ`` not equal to NONE. In
        addition, the transformation matrix is printed out when ``SEPR`` is equal to 1 or 2 on :ref:`seopt`.
        In interactive sessions, the transformation matrix is not output if the model has more than 10
        elements.

        For information about the component modes stored in the :file:`.cms` or :file:`.tcms` file, refer to
        `Component Modes Storage
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_substr/advcmssuperelem.html#>`_

        If ``Elcalc`` = YES, the element results of the component modes included in the transformation
        matrix of the CMS method are calculated and written to the :file:`.cms` file. This can significantly
        reduce the computation time of the. For limitations and available element results, see.

        Select a ``nStartVN`` value to offset the virtual node numbers from the other node numbers used in
        the model; otherwise, the program selects ``nStartVN`` to fulfill that condition. In the case of
        multiple superelements, if ``nStartVN`` is defined during each generation pass, then in the use
        pass, the virtual nodes of all imported superelements are gathered and renumbered from the
        ``nStartVN`` value specified for the first encountered superelement (first :ref:`se` command).
        ``nStartVN`` can also be defined in the use pass via :ref:`se`. (If ``nStartVN`` is defined by both
        the :ref:`cmsopt` and :ref:`se` commands, the larger number prevails.)

        For more information, see `Component Mode Synthesis
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_substr/advcms.html#advcmsunderstand>`_

        This command is also valid in :ref:`prep7`.

        .. _CMSOPT_prodres:

        Ansys Mechanical Enterprise PrepPost Only :ref:`cmsopt`,FIX,,,,,,EXB is supported.
        """
        command = f"CMSOPT,{cmsmeth},{nmode},{freqb},{freqe},{fbddef},{fbdval},{iokey},,,{elcalc},,{eigmeth},{nstartvn}"
        return self.run(command, **kwargs)

    def cnkmod(self, itype: str = "", knum: str = "", value: str = "", **kwargs):
        r"""Modifies contact element key options.

        Mechanical APDL Command: `CNKMOD <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CNKMOD.html>`_

        Parameters
        ----------
        itype : str
            Contact element type number as defined on the :ref:`et` command.

        knum : str
            Number of the KEYOPT to be modified (KEYOPT( ``KNUM`` )).

        value : str
            Value to be assigned to the KEYOPT.

        Notes
        -----

        .. _CNKMOD_notes:

        The :ref:`cnkmod` command has the same syntax as the :ref:`keyopt` command. However, it is valid
        only in the SOLUTION processor. The command can be used to modify certain contact element KEYOPT
        values between load steps in any analysis, including restarts and `linear perturbation
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/strlinpertother.html>`_ analyses, as
        shown in the table below.

        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.

        In a `multiframe restart
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/Hlp_G_BAS3_12.html#BASmultprocmap52199>`_,
        :ref:`cnkmod` must be issued again during each subsequent restart run.

        **Modifying KEYOPT(12)**

        A common use for the :ref:`cnkmod` command is to modify contact interface behavior between load
        steps in a restart analysis, a linear perturbation analysis, or other types of analyses. This
        enables you to control the contact status locally per contact pair. The key options that control
        contact interface behavior are: KEYOPT(12) of ``CONTA172``, ``CONTA174``, ``CONTA175``, and
        ``CONTA177``  ; and KEYOPT(10) of ``CONTA178``.

        You can change KEYOPT(12) to any value. For example, you can change from standard contact to bonded
        contact or vice-versa. If an open gap exists at the end of the previous load step and the contact
        status is adjusted to sliding or sticking due to a bonded or no-separation contact behavior
        definition, the program considers it as near-field contact when executing :ref:`cnkmod` in the
        subsequent load steps.

        In a `linear perturbation analysis
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/strlinpertother.html>`_, the
        :ref:`cnkmod` command adjusts the contact status from the linear perturbation base analysis (at the
        point of restart) as described in the table below. It enables you to take points in the base
        analysis that are near contact (within the pinball region) and modify them to be treated as in-
        contact in the perturbation analysis (see the "1 - near-field" row with KEYOPT(12) values set to 4
        or 5). You can also take points that are sliding in the base analysis and treat them as sticking in
        the perturbation analysis, irrespective of the MU value (see the "2 - sliding" row with KEYOPT(12)
        values set to 1,3, 5, or 6).

        Contact Status Adjusted in Linear Perturbation Analysis via CNKMOD
        ******************************************************************

        .. flat-table::

           * - :rspan:`1` **Contact Status from the Base Analysis Solution at the Restart Point**
             - *\*CNKMOD,** ``ITYPE`` ,12, ``Value``
           * - KEYOPT(12) Value
             - Adjusted Contact Status
           * - 0 - far-field
             - any
             - 0 - far-field
           * - :rspan:`4` 1 - near-field
             - 0, 1, 2, 3, 6
             - 1 - near-field
           * - :rspan:`1` 4
             - 1 - near-field (if outside of the adjusted pinball region)
           * - 2 - sliding (if inside of the adjusted pinball region)
           * - :rspan:`1` 5
             - 1 - near-field (if outside of the adjusted pinball region)
           * - 3 - sticking (if inside of the adjusted pinball region)
           * - :rspan:`1` 2 - sliding
             - 0, 2, 4
             - 2 - sliding
           * - 1, 3, 5, 6
             - 3 - sticking
           * - 3 - sticking
             - any
             - 3 - sticking

        If an open gap exists at the end of the previous load step and the contact status is adjusted as
        sliding or sticking due to a bonded or no-separation contact behavior definition, the program
        considers it a near-field contact when executing :ref:`cnkmod` in the subsequent load steps.

        In the linear perturbation analysis procedure, contact status can also be controlled or modified via
        the :ref:`perturb` command. The contact status always follows local controls defined by the
        :ref:`cnkmod` command first, and is then adjusted by the global sticking or bonded setting (
        ``ContKey`` = STICKING or BONDED) on the :ref:`perturb` command.

        **Modifying KEYOPT(3)**

        Another use for the :ref:`cnkmod` command is to change the units of normal contact stiffness
        (contact element real constant FKN) in a `linear perturbation modal analysis
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/strlinpertother.html>`_ that is used
        to model `brake squeal
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STRmodanexamp.html#strlinearnonpresmodan>`_.
        For contact elements ``CONTA172`` and ``CONTA174``, KEYOPT(3) controls the units of normal contact
        stiffness. You can issue the command :ref:`cnkmod`, ``ITYPE``,3,1 during the first phase of the
        linear perturbation analysis in order to change the units of normal contact stiffness from
        FORCE/LENGTH :sup:`3` (in the base analysis) to FORCE/LENGTH. Note that KEYOPT(3) = 1 is valid only
        when a penalty-based algorithm is used (KEYOPT(2) = 0 or 1) and the absolute normal contact
        stiffness value is explicitly specified (that is, a negative value input for real constant FKN).

        **Modifying KEYOPT(15)**

        KEYOPT(15) controls the effect of contact stabilization damping for contact elements ``CONTA172``,
        ``CONTA174``, ``CONTA175``, and ``CONTA177``. You can use :ref:`cnkmod` to activate or deactivate
        the contact stabilization damping between load steps. For example, the command :ref:`cnkmod`,
        ``ITYPE``,15,1 deactivates the contact stabilization damping.
        """
        command = f"CNKMOD,{itype},{knum},{value}"
        return self.run(command, **kwargs)

    def cntr(self, option: str = "", key: str = "", **kwargs):
        r"""Redirects contact pair output quantities to a text file.

        Mechanical APDL Command: `CNTR <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CNTR.html>`_

        **Command default:**

        .. _CNTR_default:

        Contact pair output quantities are written to the output file ( :file:`Jobname.OUT` ) or to the
        screen, as specified by the :ref:`output` command.

        Parameters
        ----------
        option : str
            Output option:

            * ``OUT`` - Contact output control.

        key : str
            Control key:

            * ``NO`` - Write contact information to the output file or to the screen (default).

            * ``YES`` - Write contact information to the :file:`Jobname.CNM` file.

        Notes
        -----

        .. _CNTR_notes:

        Issue the command :ref:`cntr`,OUT,YES to redirect contact pair output quantities to the
        :file:`Jobname.CNM` file.

        To ensure that the contact information is written to :file:`Jobname.CNM`, reissue
        :ref:`cntr`,OUT,YES each time you reenter the solution processor ( :ref:`slashsolu` ).
        """
        command = f"CNTR,{option},{key}"
        return self.run(command, **kwargs)

    def cutcontrol(self, lab: str = "", value: str = "", option: str = "", **kwargs):
        r"""Controls time-step cutback during a nonlinear solution.

        Mechanical APDL Command: `CUTCONTROL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CUTCONTROL.html>`_

        Parameters
        ----------
        lab : str
            Specifies the criteria for causing a cutback. Valid labels are:

            * ``ALIMIT`` - Set the maximum edge-flux degree-of-freedom increment allowed within a time step. If
              the absolute value of the calculated increment within a time step exceeds ``VALUE``, the program
              performs a cutback. If not specified, default ``VALUE`` = 1.0 x 10 :sup:`25`. This cutback trigger
              criterion is part of the :ref:`physics limit set. <CUTCONTROL_physicsLimitSet>`

            * ``CONCLIMIT`` - Set the maximum concentration degree-of-freedom increment allowed within a time
              step. If the absolute value of the calculated increment within a time step exceeds ``VALUE``, the
              program performs a cutback. If not specified, default ``VALUE`` = 1.0 x 10 :sup:`25`. This cutback
              trigger criterion is part of the :ref:`physics limit set. <CUTCONTROL_physicsLimitSet>`

            * ``CRPLIMIT`` - Set values for calculating the maximum equivalent creep ratio allowed within a time
              step. If the calculated maximum creep ratio exceeds the defined creep-ratio limit, the program
              performs a cutback. For the first substep or the rebalance substeps after remeshing in `nonlinear
              mesh adaptivity
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_nlad/advmnaexample.html>`_ or `rezoning
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_nlad/Hlp_G_ADVRZSMP.html>`_, however,
              the user-defined maximum plastic-strain limit is ignored.

            * ``CUTBACKFACTOR`` - Key to set the cutback factor, a multiplier for reducing the time step
              interval to the fraction specified in ``VALUE``, where 0 < ``VALUE`` < 1 (default is 0.5 if
              ``VALUE`` is not specified.) The option to change the cutback factor is valid only when automatic
              time stepping is on ( :ref:`autots`,ON), which is the default.

            * ``DMGLIMIT`` - For damage models (such as `generalized damage and anisotropic damage
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/mat_damageall.html#mat_reganisodmgrefs>`_
              ), the maximum allowable damage increment in a time step. If the calculated value exceeds ``VALUE``,
              the program performs a cutback (bisection). If ``VALUE`` is unspecified, the program does not check
              the allowable damage increment.

            * ``DPPLMT`` - Set the maximum pore-pressure increment allowed within a time step. If the calculated
              maximum increment exceeds the specified limit, the program performs a cutback. This option has no
              default and is valid for coupled `structural-pore-fluid-diffusion
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cou/Hlp_G_COU_porefluiddiffstruct.html#coupfdsanalysis>`_
              analysis only.

            * ``DSPLIMIT`` - Set the maximum degree-of-freedom increment allowed within a time step. Considering
              all degrees of freedom at every node, if the absolute value of the maximum incremental degree-of-
              freedom solution within in a time step exceeds ``VALUE``, the program performs a cutback. If not
              specified, default ``VALUE`` = 1.0 x 10 :sup:`7`.This cutback trigger criterion is the sole member
              of the :ref:`DSPLIMIT set. <CUTCONTROL_DSPLIMITSet>`

            * ``EMFLIMIT`` - Set the maximum electromotive force degree-of-freedom increment allowed within a
              time step. If the absolute value of the calculated increment within a time step exceeds ``VALUE``,
              the program performs a cutback. If not specified, default ``VALUE`` = 1.0 x 10 :sup:`25`. This
              cutback trigger criterion is part of the :ref:`physics limit set. <CUTCONTROL_physicsLimitSet>`

            * ``MAGLIMIT`` - Set the maximum scalar magnetic potential degree-of-freedom increment allowed
              within a time step. If the absolute value of the calculated increment within a time step exceeds
              ``VALUE``, the program performs a cutback. If not specified, default ``VALUE`` = 1.0 x 10 :sup:`25`.
              This cutback trigger criterion is part of the :ref:`physics limit set. <CUTCONTROL_physicsLimitSet>`

            * ``MDMG`` - For regularized `microplane
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/microplane.html#matmicroplanereadlist>`_
              damage models, the maximum allowable microplane homogenized damage increment in a time step. If the
              calculated value exceeds ``VALUE``, the program performs a cutback (bisection). If ``VALUE`` is
              unspecified, the program does not check the allowable microplane homogenized damage increment.

            * ``PLSLIMIT`` - Maximum equivalent plastic strain allowed within a time-step (substep). If the
              calculated value exceeds ``VALUE``, the program performs a cutback (bisection). Default: ``VALUE`` =
              0.15 (15 percent)

              If :ref:`cutcontrol` with ``Lab`` = PLSLIMIT is not issued, the minimum time step specified is
              reached, and the maximum plastic limit calculated from the solution exceeds 15 percent, the program
              generates a warning and continues the Newton iterations.

              If :ref:`cutcontrol` with ``Lab`` = PLSLIMIT is issued, the minimum time step specified is reached,
              and the maximum plastic limit calculated exceeds the specified limit, the program generates an error
              and stops the Newton iterations. For the first substep or the rebalance substeps after remeshing in
              `nonlinear mesh adaptivity
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_nlad/advmnaexample.html>`_ or `rezoning
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_nlad/Hlp_G_ADVRZSMP.html>`_, however,
              the user-defined maximum plastic-strain limit is ignored.

            * ``PRESLIMIT`` - Set the maximum pressure degree-of-freedom increment allowed within a time step.
              If the absolute value of the calculated increment within a time step exceeds ``VALUE``, the program
              performs a cutback. If not specified, default ``VALUE`` = 1.0 x 10 :sup:`25`. This cutback trigger
              criterion is part of the :ref:`physics limit set. <CUTCONTROL_physicsLimitSet>`

            * ``ROTLIMIT`` - Set the maximum rotation degree-of-freedom increment allowed within a time step. If
              the absolute value of the calculated increment within a time step exceeds ``VALUE``, the program
              performs a cutback. If not specified, default ``VALUE`` = 1.0 x 10 :sup:`7`. This cutback trigger
              criterion is part of the :ref:`physics limit set. <CUTCONTROL_physicsLimitSet>`

            * ``TEMPLIMIT`` - Set the maximum temperature degree-of-freedom increment allowed within a time
              step. If the absolute value of the calculated increment within a time step exceeds ``VALUE``, the
              program performs a cutback. If not specified, default ``VALUE`` = 1.0 x 10 :sup:`25`. This cutback
              trigger criterion is part of the :ref:`physics limit set and is also valid for
              <CUTCONTROL_physicsLimitSet>` `coupled structural-pore-fluid-diffusion-thermal analysis
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cou/Hlp_G_COU_porefluiddiffstruct.html#coupfdsanalysis>`_.

            * ``ULIMIT`` - Set the maximum translation degree-of-freedom increment allowed within a time step.
              If the absolute value of the calculated increment within a time step exceeds ``VALUE``, the program
              performs a cutback. If not specified, default ``VALUE`` = 1.0 x 10 :sup:`7`. This cutback trigger
              criterion is part of the :ref:`physics limit set. <CUTCONTROL_physicsLimitSet>`

            * ``VOLTLIMIT`` - Set the maximum volt degree-of-freedom increment allowed within a time step. If
              the absolute value of the calculated increment within a time step exceeds ``VALUE``, the program
              performs a cutback. If not specified, default ``VALUE`` = 1.0 x 10 :sup:`25`. This cutback trigger
              criterion is part of the :ref:`physics limit set. <CUTCONTROL_physicsLimitSet>`

            * ``VSLIMIT`` - For `viscoelastic
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/evis.html#mat_harmvisco>`_
              materials, the `maximum equivalent viscous strain increment
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/evis.html#eq92b60ee3-7e22-457b-9543-53f86d16432a>`_
              allowed within a time step. If the calculated value exceeds ``VALUE`` (default = 0.01), the program
              performs a cutback (bisection). If ``VALUE`` = 0, the program does not check the equivalent viscous
              strain increment.

            * ``Other Valid Labels:`` -

            * ``NOITERPREDICT`` - If ``VALUE`` = 0 (default), the program predicts the number of iterations for
              nonlinear convergence and performs a cutback earlier than the number of iterations specified (
              :ref:`neqit` ). This is the recommended option.

              If ``VALUE`` = 1, the solution iterates (if nonconvergent) to :ref:`neqit` number of iterations
              before a cutback is invoked. It is sometimes useful for poorly-convergent problems, but rarely
              needed in general.

              Bisection is also controlled by contact status change, plasticity or creep strain limit, and other
              factors. If any of these factors occur, bisection still occurs, regardless of the NOITERPREDICT
              setting.

            * ``NPOINT`` - Number of points in a cycle for a second order dynamic equation, used to control
              automatic time- stepping. If the number of solution points per cycle is less than ``VALUE``, the
              program performs a cutback in time step size. Default: ``VALUE`` = 13 (linear analysis) or 5
              (nonlinear analysis). A larger number of points yields a more accurate solution but also increases
              the solution run time.

              This option works well for linear problems. For nonlinear analyses, other factors such as contact
              status changes and solution convergence rate can overwrite NPOINT. (See `Automatic Time-Stepping
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_tool6.html#autotime_midstep>`_

        value : str
            Numeric value for the specified cutback criterion. For ``Lab`` = CRPLIMIT only, ``VALUE`` is the
            creep criteria for the creep ratio limit.

        option : str
            Type of creep analysis. Valid for ``Lab`` = CRPLIMIT only.

            * ``IMPRATIO`` - Set the `maximum creep ratio
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STR8_3.html#STRTimeHCrAjwf0706991137>`_
              value for implicit creep. Default = 0.0 (no creep limit control). Any positive value is valid.

            * ``STSLIMIT`` - Stress threshold for calculating the creep ratio. For integration points with
              effective stress below this threshold, the creep ratio does not cause cutback. Default = 0.0. Any
              positive value is valid.

            * ``STNLIMIT`` - Elastic strain threshold for calculating the creep ratio. For integration points
              with effective elastic strain below this threshold, the creep ratio does not cause cutback. Default
              = 0.0. Any positive value is valid.

        Notes
        -----
        A cutback is a method for automatically reducing the step size when either the solution error is too
        large or the solution encounters convergence difficulties during a nonlinear analysis.

        If a convergence failure occurs, the program reduces the time step interval to a fraction of its
        previous size and automatically continues the solution from the last successfully converged time
        step. If the reduced time step again fails to converge, the program again reduces the time step size
        and proceeds with the solution. This process continues until convergence is achieved or the minimum
        specified time step value is reached.

        A cutback occurs when a trigger criteria is encountered. The magnitude of the time-step reduction is
        determined by the cutback factor. Both the trigger and the cutback factor can be specified via
        :ref:`cutcontrol` :

        * The trigger criteria can be specified for individual physics as detailed in :ref:`CUTCONTROL_Lab`
          ``Lab`` descriptions above.

        * The cutback factor is 0.5 by default, and can be specified via the :ref:`CUTBACKFACTOR label
          described above. <CUTCONTROL_CUTBACKFACTOR>`

        :ref:`cutcontrol` can be issued multiple times.

        .. _CUTCONTROL_DSPLIMITSet:

        DSPLIMIT Set
        ^^^^^^^^^^^^

        DSPLIMIT is the sole label in the DSPLIMIT Set. It can be used to specify the cutback trigger
        criterion as a limit on the maximum degree-of-freedom increment within a time step, considering all
        degrees of freedom in an analysis (see :ref:`DSPLIMIT label description above).
        <CUTCONTROL_DSPLIMIT>`

        .. _CUTCONTROL_physicsLimitSet:

        Physics Limit Set
        ^^^^^^^^^^^^^^^^^

        The physics limit set comprises the following labels: ULIMIT, ROTLIMIT, TEMPLIMIT, PRESLIMIT,
        VOLTLIMIT, EMFLIMIT, MAGLIMIT, ALIMIT, CONCLIMIT. They can be used to specify distinct degree-of-
        freedom limits as cutback triggers for individual physics in a multiphysics analysis. Whenever one
        of these distinct limits is encountered, a cutback is triggered.

        Degree-of-freedom limits as cutback trigger criteria are specified via :ref:`cutcontrol` with labels
        from either the DSPLIMIT set or the physics limit set. If multiple :ref:`cutcontrol` commands
        include labels from both of these sets, the last command issued determines whether the cutback
        trigger criteria is set by the DSPLIMIT or the physics limit set (see :ref:`example command listing
        snippets below). <CUTCONTROL_CMDlistingPysLimitDSPLimit>`

        .. _CUTCONTROL_PhysicsLimitSetDefault:

        .. rubric:: **Command Default: If no :ref:`cutcontrol` commands are issued with labels from the DSPLIMIT set or the physics limit set, the default cutback trigger criterion is DSPLIMIT with VALUE = 1.0 x 10 :sup:`7`.**

        Creep and Viscoelastic Analyses
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        For creep and viscoelastic analyses, the cutback procedure is similar; the process continues until
        the minimum specified time step size is reached. However, if the criterion is exceeded, the program
        issues a warning but continues the substep until the analysis is complete. In this case, convergence
        is achieved but the criterion is not satisfied.

        :ref:`cutcontrol` enables a step size reduction for analyses experiencing convergence difficulties;
        :ref:`opncontrol` is an analogous but opposite command that increases the step size to speed up
        converging analyses.

        **Example Usage**

        .. _CUTCONTROL_examples:

        * `Friction Stir Welding Simulation (specify PLSLIMIT on CUTCONTROL)
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_tec/tecfricstiranalysis.html#>`_
          CUTCONTROL )
        * Wire Crimping Simulation (specify PLSLIMIT on :ref:`cutcontrol` )
        * Control the maximum incremental pore pressure allowed in a time step via DPPLIMIT on
          :ref:`cutcontrol`
        * `Regularized Microplane Damage Models (specify MDMG on CUTCONTROL)
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/microplane.html#>`_ CUTCONTROL )

        .. _CUTCONTROL_CMDlistingPysLimitDSPLimit:

        Multiple :ref:`cutcontrol` Commands with labels from both the DSPLIMIT and the Physics Limit Sets
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        When multiple :ref:`cutcontrol` commands include labels from both the DSPLIMIT and the physics limit
        sets, DSPLIMIT is ignored unless ``Lab`` = DSPLIMIT on the last :ref:`cutcontrol` command issued as
        illustrated in the examples below.

        * **Label** **on the last** :ref:`cutcontrol` command issued is from the physics limit set : The
          cutback trigger criteria are those specified by the physics limit set, and the earlier
          :ref:`cutcontrol`,DSPLIMIT command is ignored.

        .. code:: apdl

           CUTCONTROL,TEMPLIMIT,10     CUTCONTROL,DSPLIMIT,0.7    CUTCONTROL,ULIMIT,0.2   !trigger criteria
          is specified by physics limit set (and DSPLIMIT is ignored)    !both ULIMIT and TEMPLIMIT
          contribute to the physics limit set of cutback trigger criteria

        * **Lab= DSPLIMIT on the last** :ref:`cutcontrol` command issued : DSPLIMIT sets the cutback trigger
          criterion and earlier :ref:`cutcontrol` command(s) issued with ``Lab`` = labels from the physics
          limit set are ignored.

        .. code:: apdl

           CUTCONTROL,TEMPLIMIT,10    CUTCONTROL,ULIMIT,0.2     CUTCONTROL,DSPLIMIT,0.7 !trigger criteria is
          specified by DSPLIMIT (and physics limit set labels are ignored)
        """
        command = f"CUTCONTROL,{lab},{value},{option}"
        return self.run(command, **kwargs)

    def ddoption(
        self, decomp: str = "", nprocpersol: str = "", numsolforlp: str = "", **kwargs
    ):
        r"""Sets domain decomposer option for a distributed-memory parallel (DMP) solution.

        Mechanical APDL Command: `DDOPTION <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_DDOPTION.html>`_

        **Command default:**

        .. _DDOPTION_default:

        The optimal algorithm for domain decomposition is automatically chosen.

        Parameters
        ----------
        decomp : str
            Controls which domain decomposition algorithm to use.

            * ``AUTO`` - Automatically selects the optimal domain decomposition method (default).

            * ``MESH`` - Decompose the FEA mesh.

            * ``FREQ`` - Decompose the frequency domain for harmonic analyses.

            * ``CYCHI`` - Decompose the harmonic indices for cyclic symmetry modal analyses.

        nprocpersol : str
            Number of processes to be used for mesh-based decomposition in conjunction with each frequency
            solution ( ``Decomp`` = FREQ) or harmonic index solution ( ``Decomp`` = CYCHI). Defaults to 1.
            This field is ignored when ``Decomp`` = MESH.

        numsolforlp : str
            Number of frequency or harmonic index solutions in a subsequent linear perturbation harmonic or
            linear perturbation cyclic modal analysis. This field is ignored when ``Decomp`` = MESH.

        Notes
        -----

        .. _DDOPTION_notes:

        This command controls options related to the domain decomposition algorithm used in a distributed-
        memory parallel (DMP) solution to split the analysis calculations into domains, with each domain
        being solved on a different process.

        By default, the optimal domain decomposition algorithm (MESH, FREQ, or CYCHI) is automatically
        chosen. When FREQ (for a harmonic analysis) or CYCHI (for a cyclic symmetry modal analysis) is
        automatically chosen, the ``NPROCPERSOL`` argument is also automatically set to a value ≥ 1.

        The "mesh" algorithm ( ``Decomp`` = MESH) divides the finite element mesh into domains. In this
        case, domains are effectively groups of elements, with one domain being solved on each process. This
        algorithm seeks to create evenly sized domains (that is, domains with equal numbers of elements) as
        well as to minimize the size of interfaces between the newly created domains. This algorithm can be
        used for all analysis types.

        The "frequency" algorithm ( ``Decomp`` = FREQ) divides the specified frequency range for a harmonic
        analysis into domains. In this case, domains are effectively groups of frequency solutions, with one
        domain being solved on ``NPROCPERSOL`` processes. If there are more processes than frequency points,
        some processes will remain idle during the harmonic analysis solution. This algorithm seeks to
        create evenly sized domains. However, if the number of processes does not divide evenly into the
        number of frequency solutions, the efficiency of the parallel solution will be reduced. This
        algorithm can only be used for harmonic analyses using the auto ( :ref:`hropt`,AUTO), full (
        :ref:`hropt`,FULL), or frequency-sweep ( :ref:`hropt`,VT) method.

        The "cyclic" algorithm ( ``Decomp`` = CYCHI) divides the specified list of harmonic indices for a
        cyclic symmetry modal analysis into domains. In this case, domains are effectively groups of cyclic
        harmonic indices, with one domain being solved on ``NPROCPERSOL`` processes. If there are more
        processes than harmonic indices, some processes will remain idle during the cyclic model solution.
        This algorithm seeks to create evenly sized domains. However, if the number of processes does not
        divide evenly into the number of harmonic indices, the efficiency of the parallel solution will be
        reduced.

        For the mesh algorithm (MESH), all available processes are used. This is not necessarily the case
        for the frequency and cyclic algorithms (FREQ and CYCHI).

        ``NPROCPERSOL`` is only used when ``Decomp`` = FREQ or CYCHI. It defaults to 1, which essentially
        means that no mesh-based domain decomposition occurs. When ``NPROCPERSOL`` is defined to be greater
        than 1, a combination of FREQ or CYCHI decomposition and MESH decomposition is employed. As an
        example, consider a harmonic analysis with 50 requested frequency points ( :ref:`nsubst`,50) that
        uses distributed processing with 100 CPU cores ( -dis -np 100). Specifying :ref:`ddoption`,FREQ,2
        would lead to 50 parallel sets of calculations, each working on a different frequency point and
        using 2 cores for mesh-based domain decomposition (that is, 2 groups of elements per frequency).

        :ref:`ddoption` must be issued prior to solving the first load step. Once the first load step is
        completed, this command cannot be used to change the domain decomposition method. The only exception
        is for analyses which use the linear perturbation procedure.

        In a linear perturbation analysis, :ref:`ddoption` must be entered prior to the :ref:`solve`,ELFORM
        command. In addition, the number of frequency solutions (in a subsequent harmonic analysis) or
        harmonic index solutions (in a subsequent cyclic modal analysis) must be input via the
        ``NUMSOLFORLP`` argument to enable proper domain decomposition to occur at the :ref:`solve`,ELFORM
        stage of the linear perturbation analysis. For more information, see `Linear Perturbation Analysis
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/strlinpertother.html>`_

        For more information and recommendations on how to choose the domain decomposition method, see.

        For the frequency and the cyclic algorithms, solution information for the harmonic frequencies (
        ``Decomp`` = FREQ) or cyclic harmonic indices ( ``Decomp`` = CYCHI) solved by the worker processes
        is only written to the output files for those processes ( :file:`Jobnamen.OUT` ). See for more
        information.
        """
        command = f"DDOPTION,{decomp},{nprocpersol},{numsolforlp}"
        return self.run(command, **kwargs)

    def dmpext(
        self,
        smode: str = "",
        tmode: str = "",
        dmpname: str = "",
        freqb: str = "",
        freqe: str = "",
        nsteps: str = "",
        **kwargs,
    ):
        r"""Extracts modal damping coefficients in a specified frequency range.

        Mechanical APDL Command: `DMPEXT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_DMPEXT.html>`_

        Parameters
        ----------
        smode : str
            Source mode number. There is no default for this field; you must enter an integer greater than
            zero.

        tmode : str
            Target mode. Defaults to ``SMODE``.

        dmpname : str
            Array parameter name containing the damping results. Defaults to :file:`d_damp`.

        freqb : str
            Beginning frequency range (real number greater than zero) or 'EIG' at eigenfrequency of source
            mode. 'EIG' is valid only if ``SMODE`` = ``TMODE``. Note that EIG must be enclosed in single
            quotes when this command is used on the command line or in an input file. There is no default
            for this field; you must enter a value.

        freqe : str
            End of frequency range. Must be blank for ``Freqb`` = EIG. Default is ``Freqb``.

        nsteps : str
            Number of substeps. Defaults to 1.

        Notes
        -----

        .. _DMPEXT_notes:

        DMPEXT invokes a Mechanical APDL macro that uses modal projection techniques to compute the damping
        force
        by the modal velocity of the source mode onto the target mode. From the damping force, damping
        parameters are extracted. DMPEXT creates an array parameter ``Dmpname``, with the following entries
        in each row:

        * response frequency

        * modal damping coefficient

        * modal squeeze stiffness coefficient

        * damping ratio

        * squeeze-to-structural stiffness ratio

        The macro requires the modal displacements from the file :file:`Jobname.EFL` obtained from the
        :ref:`rmflvec` command. In addition, a node component FLUN must exist from all ``FLUID136`` nodes.
        The computed damping ratio may be used to specify constant or modal damping by means of the
        :ref:`dmprat` or :ref:`mdamp` commands. For Rayleigh damping, use the :ref:`abextract` command to
        compute ALPHAD and BETAD damping parameters. See Thin Film Analysis  for more information on
        thin film analyses.

        The macro uses the :ref:`lssolve` command to perform two load steps for each frequency. The first
        load case contains the solution of the source mode excitation and can be used for further
        postprocessing. Solid model boundary conditions are deleted from the model. In addition, prescribed
        nodal boundary conditions are applied to the model. You should carefully check the boundary
        conditions of your model prior to executing a subsequent analysis.

        This command is also valid in PREP7. Distributed-Memory Parallel (DMP) Restriction This command is
        not supported in a DMP solution.
        """
        command = f"DMPEXT,{smode},{tmode},{dmpname},{freqb},{freqe},{nsteps}"
        return self.run(command, **kwargs)

    def dmpoption(
        self,
        filetype: str = "",
        combine: str = "",
        rescombfreq: str = "",
        deleopt: str = "",
        **kwargs,
    ):
        r"""Specifies distributed-memory parallel ( DMP ) file combination options.

        Mechanical APDL Command: `DMPOPTION <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_DMPOPTION.html>`_

        **Command default:**

        .. _DMPOPTION_default:

        Local solution files are automatically combined into a single global file upon leaving the solution
        processor (for example, :file:`JobnameN.RST` files are combined into one :file:`Jobname.RST` file).
        This is true for all files except the :file:`.Rnnn` files. Because they may be required in a
        subsequent analysis, local files are not automatically deleted after combination.

        Parameters
        ----------
        filetype : str
            Type of solution file to combine after a distributed memory parallel solution. There is no default;
            if (blank), the command is ignored.

            * ``RST`` - Results files ( :file:`.RST`, :file:`.RTH`, :file:`.RMG`, :file:`.RSTP` )

            * ``EMAT`` - Element matrix files ( :file:`.EMAT` ).

            * ``ESAV`` - Element saved data files ( :file:`.ESAV` )

            * ``MODE`` - Modal results files ( :file:`.MODE` )

            * ``MLV`` - Modal load vector file ( :file:`.MLV` )

            * ``IST`` - Initial state file ( :file:`.IST` )

            * ``FULL`` - Full matrix file ( :file:`.FULL` )

            * ``RFRQ`` - Reduced complex displacement file ( :file:`.RFRQ` )

            * ``RDSP`` - Reduced displacement file ( :file:`.RDSP` )

            * ``RNNN`` - Multiframe restart files ( :file:`.Rnnn` )

        combine : str
            Option to combine solution files.

            * ``Yes`` - Combine solution files (default for all files except the :file:`.Rnnn` files).

            * ``No`` - Do not combine solution files (default for the :file:`.Rnnn` files only).

        rescombfreq : str
            Frequency used to combine the local results files during a distributed memory parallel solution.
            This option applies only when ``FileType`` = RST and ``Combine`` = YES.

            * ``NONE`` - Do not combine the local results files during solution. The local results files is
              combined only upon leaving the solution processor (default).

            * ``ALL`` - Combines the local results files at every time point.

            * ``LAST`` - Combines the local results files at the last time point of every load step.

        deleopt : str
            Option to delete local solution files of the type specified by ``FileType`` option after they are combined. This option applies only when ``Combine`` = Yes.

            * ``Yes`` - Delete the local solution files after they are combined.

            * ``No`` - Do not delete the local solution files after they are combined (default).

        Notes
        -----

        .. _DMPOPTION_notes:

        The :ref:`dmpoption` command controls how solution files are written during a distributed-memory
        parallel ( DMP ) solution. This command is most useful for controlling how results files (
        :file:`.rst`, :file:`.rth`, etc.) are written.

        In a distributed memory parallel solution, a local results file is written by each process (
        :file:`JobnameN.ext`, where ``N`` is the process number). By default, the program automatically
        combines the local results files (for example, :file:`JobnameN.rst` ) upon leaving the solution
        processor (for example, upon the :ref:`finish` command) into a single global results file (
        :file:`Jobname.rst` ) which can be used in postprocessing.

        Alternatively, the ``ResCombFreq`` argument can be used to combine the local results files at
        certain time points during the distributed solution to create a single combined results file that
        can be used to postprocess the model while the solution progresses. Doing so increases data
        communication and I/O between processes, leading to slower performance.

        The ``ResCombFreq`` option only applies when solving static analyses, and harmonic or transient
        analyses that use the full method. It does not apply to mode superposition harmonic and mode
        superposition transient analyses. It does not apply when using the frequency domain decomposition
        option ( :ref:`ddoption`,FREQ) in a harmonic analysis.

        To reduce communication and I/O, issue :ref:`dmpoption`,RST,NO to bypass this step of combining the
        local results files; the local files remain on the local disks in the current working directory. You
        can then use :ref:`rescombine` in the POST1 general postprocessor ( :ref:`post1` ) to read all
        results into the database for postprocessing.

        The :ref:`rescombine` command macro is intended for use with POST1. If you want to postprocess
        distributed parallel solution results using the POST26 time-history postprocessor ( :ref:`post26` ),
        it is recommended that you combine your local results files into one global results file (
        :ref:`dmpoption`,RST,YES or :ref:`combine` ).

        Local :file:`.emat`, :file:`.esav`, :file:`.mode`, :file:`.mlv`, :file:`.ist`, :file:`.rfrq`,
        :file:`.rdsp`, and :file:`.full` files are also written (when applicable) by each process in a
        distributed memory parallel solution. If these files are not needed for a downstream solution or
        operation, you can issue the command :ref:`dmpoption`, ``FileType``,NO for each file type to bypass
        the file combination step and thereby improve performance.

        If :ref:`dmpoption`,MODE,NO or :ref:`dmpoption`,RST,NO is specified in a modal analysis, element
        results cannot be written to the combined mode file ( :file:`Jobname.MODE` ). In this case, if
        distributed-memory parallel processing is used in a downstream harmonic or transient analysis that
        uses the mode-superposition method, the ``MSUPkey`` on the :ref:`mxpand` command can retain its
        value. However, if shared-memory parallel processing is used in the downstream harmonic or transient
        analysis, the ``MSUPkey`` is effectively set to NO.

        If :ref:`dmpoption`,RNNN,YES is specified, all multiframe restart files named :file:`Jobname.R001`
        to :file:`Jobname.R999` are automatically combined upon leaving the solution processor (which can be
        slow and inefficient). To manually combine a single set of :file:`.Rnnn` restart files, use the
        :ref:`combine` command.

        Since local solution files may be required in a downstream analysis, the option to delete them after
        combination is disabled ( ``DeleOpt`` = No) by default. However, you can enable this option to
        reduce disk space usage by removing certain files if you know that they are not needed in any
        subsequent analysis.

        :ref:`dmpoption` can be changed between load steps; however, doing so does not affect which set of
        solution files are combined. The values of ``Combine`` and ``DeleOpt`` are overwritten if
        :ref:`dmpoption` is issued multiple times for the same ``FileType``. As a result, only the last
        values of ``Combine`` and ``DeleOpt`` for each ``FileType`` upon leaving the solution processor
        determine whether the local solution files are combined with or without deletion. For example, in a
        two-load-step solution, if :ref:`dmpoption`, RST, NO is issued in the first load step and
        :ref:`dmpoption`, RST, YES,,YES is issued in the second load step, all sets on the local results
        files will be combined, and then the local results files will be deleted. If the opposite is true (
        :ref:`dmpoption`, RST, YES,,YES is issued in the first load step, and :ref:`dmpoption`, RST, NO is
        issued in the second load step), no results files are combined, and thus no local results files are
        deleted.

        After using :ref:`dmpoption` to suppress file combination, you may find it necessary to combine the
        local files for a specific ``FileType`` for use in a subsequent analysis. In this case, use the
        :ref:`combine` command to combine local solution files into a single, global file.
        """
        command = f"DMPOPTION,{filetype},{combine},{rescombfreq},{deleopt}"
        return self.run(command, **kwargs)

    def dspoption(
        self,
        reord_option: str = "",
        memory_option: str = "",
        memory_size: str = "",
        solve_info: str = "",
        **kwargs,
    ):
        r"""Sets memory option for the sparse solver.

        Mechanical APDL Command: `DSPOPTION <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_DSPOPTION.html>`_

        **Command default:**

        .. _DSPOPTION_default:

        Automatic memory allocation is used.

        Parameters
        ----------
        reord_option : str
            Reordering option:

            * ``DEFAULT`` - Use the default reordering scheme.

            * ``SEQORDER`` - Use a sequential equation reordering scheme. Relative to PARORDER, this option
              typically results in longer equation ordering times and therefore longer overall solver times.
              Occasionally, however, this option will produce better quality orderings which decrease the matrix
              factorization times and improve overall solver performance.

            * ``PARORDER`` - Use a parallel equation reordering scheme. Relative to SEQORDER, this option
              typically results in shorter equation ordering times and therefore shorter overall solver times.
              Occasionally, however, this option will produce lower quality orderings which increase the matrix
              factorization times and degrade overall solver performance.

        memory_option : str
            Memory allocation option:

            * ``DEFAULT`` - Use the default memory allocation strategy for the sparse solver. The default
              strategy attempts to run in the INCORE memory mode. If there is not enough physical memory available
              when the solver starts to run in the INCORE memory mode, the solver will then attempt to run in the
              OUTOFCORE memory mode.

            * ``INCORE`` - Use a memory allocation strategy in the sparse solver that will attempt to obtain
              enough memory to run with the entire factorized matrix in memory. This option uses the most amount
              of memory and should avoid doing any I/O. By avoiding I/O, this option achieves optimal solver
              performance. However, a significant amount of memory is required to run in this mode, and it is only
              recommended on machines with a large amount of memory. If the allocation for in-core memory fails,
              the solver will automatically revert to out-of-core memory mode.

            * ``OUTOFCORE`` - Use a memory allocation strategy in the sparse solver that will attempt to
              allocate only enough work space to factor each individual frontal matrix in memory, but will share
              the entire factorized matrix on disk. Typically, this memory mode results in poor performance due to
              the potential bottleneck caused by the I/O to the various files written by the solver.

            * ``FORCE`` - This option, when used in conjunction with the ``Memory_Size`` option, allows you to
              force the sparse solver to run with a specific amount of memory. This option is only recommended for
              the advanced user who understands sparse solver memory requirements for the problem being solved,
              understands the physical memory on the system, and wants to control the sparse solver memory usage.

        memory_size : str
            Initial memory size allocation for the sparse solver for each process ( ``Memory_Size`` /process
            in GB ). The ``Memory_Size`` setting should always be well within the physical memory available,
            but not so small as to cause the sparse solver to run out of memory. Warnings and/or errors from
            the sparse solver will appear if this value is set too low. If the FORCE memory option is used,
            this value is the amount of memory allocated for the entire duration of the sparse solver
            solution.

        solve_info : str
            Solver output option:

            * ``OFF`` - Turns off additional output printing from the sparse solver (default).

            * ``PERFORMANCE`` - Turns on additional output printing from the sparse solver, including a
              performance summary and a summary of file I/O for the sparse solver. Information on memory usage
              during assembly of the global matrix (that is, creation of the :file:`Jobname.FULL` file) is also
              printed with this option.

        Notes
        -----

        .. _DSPOPTION_notes:

        This command controls options related to the sparse solver in all analysis types where this solver
        can be used.

        The amount of memory required for the sparse solver is unknown until the matrix structure is
        preprocessed, including equation reordering. The amount of memory allocated for the sparse solver is
        then dynamically adjusted to supply the solver what it needs to compute the solution.

        If you have a large memory system, you may want to try selecting the INCORE memory mode for larger
        jobs to improve performance. Also, when running the sparse solver with many processors on the same
        machine or on a machine with very slow I/O performance (for example, slow hard drive speed), you may
        want to try using the INCORE memory mode to achieve better performance. However, doing so may
        require much more memory compared to running in the OUTOFCORE memory mode.

        Running with the INCORE memory mode is best for jobs which comfortably fit within the limits of the
        physical memory on a given system. If the sparse solver workspace exceeds physical memory size, the
        system will be forced to use virtual memory (or the system page/swap file). In this case, it is
        typically more efficient to run with the OUTOFCORE memory mode.
        """
        command = (
            f"DSPOPTION,{reord_option},{memory_option},{memory_size},,,{solve_info}"
        )
        return self.run(command, **kwargs)

    def ematwrite(self, key: str = "", **kwargs):
        r"""Forces the writing of all the element matrices to :file:`Jobname.emat` None.

        Mechanical APDL Command: `EMATWRITE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_EMATWRITE.html>`_

        Parameters
        ----------
        key : str
            Write key:

            * ``YES`` - Forces the writing of the element matrices to :file:`Jobname.emat` None even if not
              normally done.

            * ``NO`` - Element matrices are written only if required. This value is the default.

        Notes
        -----

        .. _EMATWRITE_notes:

        The :ref:`ematwrite` command forces Mechanical APDL to write the :file:`Jobname.emat` file.

        If used in the solution processor ( :ref:`slashsolu` ), this command is valid within the first load
        step only.

        This command is also valid in PREP7.
        """
        command = f"EMATWRITE,{key}"
        return self.run(command, **kwargs)

    def eqslv(
        self,
        lab: str = "",
        toler: str = "",
        mult: str = "",
        keepfile: str = "",
        **kwargs,
    ):
        r"""Specifies the type of equation solver.

        Mechanical APDL Command: `EQSLV <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_EQSLV.html>`_

        **Command default:**

        .. _EQSLV_default:

        The sparse direct solver is the default solver for all analyses, with the exception of
        modal/buckling analyses.

        For modal/buckling analyses, there is no default solver. You must specify a solver with the
        :ref:`modopt` or :ref:`bucopt` command. The specified solver automatically chooses the required
        internal equation solver (for example, :ref:`modopt` ,LANPCG automatically uses :ref:`eqslv`,PCG
        internally, and :ref:`bucopt`,LANB automatically uses :ref:`eqslv`,SPARSE internally).

        Parameters
        ----------
        lab : str
            Equation solver type:

            * ``SPARSE`` - Sparse direct equation solver. Applicable to real-value or complex-value symmetric
              and unsymmetric matrices. Available only for STATIC, HARMIC (full method only), TRANS (full method
              only), SUBSTR, and PSD spectrum analysis types ( :ref:`antype` ). Can be used for nonlinear and
              linear analyses, especially nonlinear analysis where indefinite matrices are frequently encountered.
              Well suited for contact analysis where contact status alters the mesh topology. Other typical well-
              suited applications are: (a) models consisting of shell/beam or shell/beam and solid elements (b)
              models with a multi-branch structure, such as an automobile exhaust or a turbine fan. This is an
              alternative to iterative solvers since it combines both speed and robustness. Generally, it requires
              considerably more memory (~10x) than the PCG solver to obtain optimal performance (running totally
              in-core). When memory is limited, the solver works partly in-core and out-of-core, which can
              noticeably slow down the performance of the solver. See the :ref:`bcsoption` command for more
              details on the various modes of operation for this solver.

              This solver can be run using shared-memory parallel (SMP), distributed-memory parallel (DMP), or
              hybrid parallel processing. For DMP, this solver preserves all of the merits of the classic or
              shared memory sparse solver. The total sum of memory (summed for all processes) is usually higher
              than the shared memory sparse solver. System configuration also affects the performance of the
              distributed memory parallel solver. If enough physical memory is available, running this solver in
              the in-core memory mode achieves optimal performance. The ideal configuration when using the out-of-
              core memory mode is to use one processor per machine on multiple machines (a cluster), spreading the
              I/O across the hard drives of each machine, assuming that you are using a high-speed network such as
              Infiniband to efficiently support all communication across the multiple machines.

              This solver supports use of the `GPU accelerator capability
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_dan/gputrouble.html>`_.

            * ``JCG`` - Jacobi Conjugate Gradient iterative equation solver. Available only for STATIC, HARMIC
              (full method only), and TRANS (full method only) analysis types ( :ref:`antype` ). Can be used for
              structural, thermal, and multiphysics applications. Applicable for symmetric, unsymmetric, complex,
              definite, and indefinite matrices. Recommended for 3D harmonic analyses in structural and
              multiphysics applications. Efficient for heat transfer, electromagnetics, piezoelectrics, and
              acoustic field problems.

              This solver can be run using shared-memory parallel (SMP), distributed-memory parallel (DMP), or
              hybrid parallel processing. For DMP, in addition to the limitations listed above, this solver only
              runs in a distributed parallel fashion for STATIC and TRANS (full method) analyses in which the
              stiffness is symmetric and only when not using the fast thermal option ( :ref:`thopt` ). Otherwise,
              this solver disables distributed-memory parallelism at the onset of the solution, and shared-memory
              parallelism is used instead.

              This solver supports use of the `GPU accelerator capability
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_dan/gputrouble.html>`_. When using the
              GPU accelerator capability, in addition to the limitations listed above, this solver is available
              only for STATIC and TRANS (full method) analyses where the stiffness is symmetric and does not
              support the fast thermal option ( :ref:`thopt` ).

            * ``ICCG`` - Incomplete Cholesky Conjugate Gradient iterative equation solver. Available for STATIC,
              HARMIC (full method only), and TRANS (full method only) analysis types ( :ref:`antype` ). Can be
              used for structural, thermal, and multiphysics applications, and for symmetric, unsymmetric,
              complex, definite, and indefinite matrices. The ICCG solver requires more memory than the JCG
              solver, but is more robust than the JCG solver for ill-conditioned matrices.

              This solver can only be run in shared-memory parallel mode. If it is run in DMP mode, this solver
              disables distributed-memory parallelism at the onset of the solution, and shared-memory parallelism
              is used instead

              This solver does not support use of the `GPU accelerator capability
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_dan/gputrouble.html>`_.

            * ``QMR`` - Quasi-Minimal Residual iterative equation solver. Available for the HARMIC (full method
              only) analysis type ( :ref:`antype` ). Can be used for symmetric, complex, definite, and indefinite
              matrices. The QMR solver is more stable than the ICCG solver.

              This solver can only be run in shared memory parallel mode and only supports 1 core. If it is run in
              DMP mode, this solver disables distributed-memory parallelism at the onset of the solution, and
              shared-memory parallelism is used instead

              This solver does not support use of the `GPU accelerator capability
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_dan/gputrouble.html>`_.

            * ``PCG`` - Preconditioned Conjugate Gradient iterative equation solver (licensed from Computational
              Applications and Systems Integration, Inc.). Requires less disk file space than SPARSE and is faster
              for large models. Useful for plates, shells, 3D models, large 2D models, and other problems having
              symmetric, sparse matrices. Such matrices are typically positive definite, but could be indefinite
              for some nonlinear analyses. The PCG solver can also be used for single-field thermal analyses
              involving unsymmetric matrices. Requires twice as much memory as JCG. Available only for analysis
              types ( :ref:`antype` ) STATIC, TRANS (full method only), or MODAL (with PCG Lanczos option only).
              Also available for the use pass of substructure analyses ( ``MATRIX50`` ). The PCG solver can
              robustly handle models that involve the use of constraint and/or coupling equations ( :ref:`ce`,
              :ref:`ceintf`, :ref:`cp`, :ref:`cpintf`, and :ref:`cerig` ). With this solver, you can use the
              :ref:`msave` command to obtain a considerable memory savings.

              The PCG solver can handle ill-conditioned problems by using a higher level of difficulty (see
              :ref:`pcgopt` ). Ill-conditioning arises from elements with high aspect ratios, contact, and
              plasticity.

              This solver can be run in shared-memory parallel or distributed-memory parallel mode. In DMP mode,
              this solver preserves all of the merits of the classic or shared-memory PCG solver. The total sum of
              memory (summed for all processes) is about 30% more than the shared-memory PCG solver.

              This solver supports use of the `GPU accelerator capability
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_dan/gputrouble.html>`_.

        toler : str
            Iterative solver tolerance value. Used only with the Jacobi Conjugate Gradient, Incomplete
            Cholesky Conjugate Gradient, Pre-conditioned Conjugate Gradient, and Quasi-Minimal Residual
            equation solvers. For the PCG solver, the default is 1.0E-8. When using the PCG Lanczos mode
            extraction method, the default solver tolerance value is 1.0E-4. For the JCG and ICCG solvers
            with symmetric matrices, the default is 1.0E-8. For the JCG and ICCG solvers with unsymmetric
            matrices, and for the QMR solver, the default is 1.0E-6. Iterations continue until the SRSS norm
            of the residual is less than ``TOLER`` times the norm of the applied load vector. For the PCG
            solver in the linear static analysis case, 3 error norms are used. If one of the error norms is
            smaller than ``TOLER``, and the SRSS norm of the residual is smaller than 1.0E-2, convergence is
            assumed to have been reached. See `Iterative Solver
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_tool8.html#eq464eb6bb-
            fd2e-4e26-bc92-38d0e6628891>`_

            When used with the Pre-conditioned Conjugate Gradient equation solver, ``TOLER`` can be modified
            between load steps (this is typically useful for nonlinear analysis).

            If a ``Lev_Diff`` value of 5 is specified on the :ref:`pcgopt` command (either program- or user-
            specified), ``TOLER`` has no effect on the accuracy of the obtained solution from the PCG
            solver; a direct solver is used when ``Lev_Diff`` = 5.

        mult : str
            Multiplier (defaults to 2.5 for nonlinear analyses; 1.0 for linear analyses) used to control the
            maximum number of iterations performed during convergence calculations. Used only with the Pre-
            conditioned Conjugate Gradient equation solver (PCG). The maximum number of iterations is equal
            to the multiplier ( ``MULT`` ) times the number of degrees of freedom (DOF). If ``MULT`` is
            input as a negative value, then the maximum number of iterations is equal to abs( ``MULT`` ).
            Iterations continue until either the maximum number of iterations or solution convergence has
            been reached. In general, the default value for ``MULT`` is adequate for reaching convergence.
            However, for ill- conditioned matrices (that is, models containing elements with high aspect
            ratios or material type discontinuities) the multiplier may be used to increase the maximum
            number of iterations used to achieve convergence. The recommended range for the multiplier is
            1.0 :math:`equation not available` ``MULT``  :math:`equation not available` 3.0.  Normally, a
            value greater than 3.0adds no further benefit toward convergence, and merely increases
            timerequirements. If the solution does not converge with 1.0  :math:`equation not available`
            ``MULT``  :math:`equation not available` 3.0, or in less than 10,000 iterations,then convergence
            is highly unlikely and further examination of themodel is recommended. Rather than increasing
            the default value of  ``MULT``, consider increasing the level of difficulty ( ``Lev_Diff`` ) on
            the :ref:`pcgopt` command.

        keepfile : str
            Determines whether files from a SPARSE solver run should be deleted or retained. Applies only to
            ``Lab`` = SPARSE for static and full transient analyses.

            * ``DELE`` - Deletes all files from the SPARSE solver run, including the factorized file,
              :file:`.DSPsymb`, upon :ref:`finish` or ``/EXIT`` (default).

            * ``KEEP`` - Retains all necessary files from the SPARSE solver run, including the :file:`.DSPsymb`
              file, in the working directory.

        Notes
        -----

        .. _EQSLV_notes:

        The selection of a solver can affect the speed and accuracy of a solution. For a more detailed
        discussion of the merits of each solver, see `Solution
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/Hlp_G_BAS3_stopsolmatrix.html>`_ in
        the `Basic Analysis Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/afbRsqe0ldm.html>`_.

        This command is also valid in PREP7.

        Distributed-Memory Parallel (DMP) Restriction All equation solvers are supported in a DMP analysis.
        However, the SPARSE and PCG solvers are the
        only distributed solvers that always run a fully distributed solution. The JCG solver runs in a
        fully distributed mode in some cases; in other cases, it does not. The ICCG and QMR solvers are not
        distributed solvers; therefore, you will not see the full performance improvements with these
        solvers that you would with a fully distributed solution.
        """
        command = f"EQSLV,{lab},{toler},{mult},,{keepfile}"
        return self.run(command, **kwargs)

    def eresx(self, key: str = "", **kwargs):
        r"""Specifies extrapolation of integration-point results.

        Mechanical APDL Command: `ERESX <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ERESX.html>`_

        **Command default:**

        .. _ERESX_default:

        Extrapolate integration-point results to the nodes for all elements except those with active
        plasticity, creep, or swelling nonlinearities (default).

        For coupled pore-pressure-thermal elements ( ``CPT212``, ``CPT213``, ``CPT215``, ``CPT216``,
        ``CPT217`` ), the default behavior is to copy integration-point results to the nodes.

        Parameters
        ----------
        key : str
            Extrapolation key:

            * ``DEFA`` - If element is fully elastic (no active plasticity, creep, or swelling nonlinearities),
              extrapolate the integration-point results to the nodes. If any portion of the element is plastic (or
              other active material nonlinearity), copy the integration-point results to the nodes (default).

            * ``YES`` - Extrapolate the linear portion of the integration-point results to the nodes and copy
              the nonlinear portion (for example, plastic strains).

            * ``NO`` - Copy the integration-point results to the nodes.

        Notes
        -----

        .. _ERESX_notes:

        Specifies whether the solution results at the element-integration points are extrapolated or copied
        to the nodes for element and nodal postprocessing. Structural stresses, elastic and thermal strains,
        field gradients, and fluxes are affected. Nonlinear data (such as plastic, creep, and swelling
        strains) are always copied to the nodes, never extrapolated. For shell elements, :ref:`eresx`
        applies only to integration-point results in the in-plane directions.

        Extrapolation occurs in the element-solution coordinate system. For elements allowing different
        solution systems at integration points (such as ``SHELL281`` and ``SOLID186`` ), extrapolation can
        produce unreliable results when the solution coordinate systems in each element differ
        significantly. (Varying element-solution coordinate systems can be created via the :ref:`esys`
        command or from large deformation.) Examine results carefully in such cases, and disable
        extrapolation if necessary.

        This command is also valid in PREP7.
        """
        command = f"ERESX,{key}"
        return self.run(command, **kwargs)

    def exbopt(
        self,
        outinv2: int | str = "",
        outtcms: int | str = "",
        outsub: int | str = "",
        outcms: int | str = "",
        outcomp: int | str = "",
        outrm: int | str = "",
        noinv: int | str = "",
        outele: int | str = "",
        **kwargs,
    ):
        r"""Specifies ``.EXB`` file output options in a CMS generation pass.

        Mechanical APDL Command: `EXBOPT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_EXBOPT.html>`_

        **Command default:**

        .. _EXBOPT_default:

        Default settings as described for each argument are used.

        Parameters
        ----------
        outinv2 : int or str
            Output control for 2nd order invariant:

            * ``0`` - Do not output (default).

            * ``1`` - Output the second order invariant.

        outtcms : int or str
            Output control for :file:`.TCMS` file:

            * ``0`` - Do not output (default).

            * ``1`` - Output the :file:`.TCMS` file.

        outsub : int or str
            Output control for :file:`.SUB` file:

            * ``0`` - Do not output (default).

            * ``1`` - Output the :file:`.SUB` file.

        outcms : int or str
            Output control for :file:`.CMS` file:

            * ``0`` - Do not output (default).

            * ``1`` - Output the :file:`.CMS` file.

        outcomp : int or str
            Output control for node and element component information:

            * ``0`` - Do not output any component information.

            * ``1`` - Output node component information only.

            * ``2`` - Output element component information only.

            * ``3`` - Output both node and element component information (default).

        outrm : int or str
            Output control for the recovery matrix:

            * ``0`` - Do not output (default).

            * ``1`` - Output the recovery matrix to :file:`fileEXB`.

            * ``2`` - Output the recovery matrix to a separate file, :file:`file_RECOVEREXB`.

        noinv : int or str
            Invariant calculation:

            * ``0`` - Calculate all invariants (default).

            * ``1`` - Suppress calculation of the 1st and 2nd order invariants. NOINV = 1 suppresses OUTINV2 =
              1.

        outele : int or str
            Output control for the element data:

            * ``0`` - Do not output (default).

            * ``1`` - Output the element data.

        Notes
        -----

        .. _EXBOPT_notes:

        When the body property file ( :file:`file.EXB` ) is requested in a CMS generation pass (
        :ref:`cmsopt`,,,,,,,EXB command), the :file:`.TCMS`, :file:`.SUB`, and :file:`.CMS` files are not
        output by default. Use the :ref:`exbopt` command to request these files, as needed.

        :ref:`exbopt` can also be used to manage some content in the :file:`.EXB` file for improving
        performance and storage (see the ``OUTINV2``, ``OUTCOMP``, ``OUTRM``, ``NOINV``, and ``OUTELE``
        arguments described above).

        If both recovery matrix output ( ``OUTRM`` = 1 or 2) and the :file:`.TCMS` file ( ``OUTTCMS`` = 1)
        are requested, the :file:`.TCMS` file writing is turned off due to potentially large in-core memory
        use.

        For more information on how to generate :file:`file.EXB`, see `Ansys Interface to AVL EXCITE
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_substr/substrexbcms.html>`_
        """
        command = f"EXBOPT,{outinv2},{outtcms},{outsub},{outcms},{outcomp},{outrm},{noinv},{outele}"
        return self.run(command, **kwargs)

    def expass(self, key: str = "", keystat: str = "", **kwargs):
        r"""Specifies an expansion pass of an analysis.

        Mechanical APDL Command: `EXPASS <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_EXPASS.html>`_

        Parameters
        ----------
        key : str
            Expansion pass key:

            * ``OFF`` - No expansion pass will be performed (default).

            * ``ON`` - An expansion pass will be performed.

        keystat : str
            Static correction vectors key:

            * ``ON`` - Include static correction vectors in the expanded displacements (default).

            * ``OFF`` - Do not include static correction vectors in the expanded displacements.

        Notes
        -----

        .. _EXPASS_notes:

        Specifies that an expansion pass of a modal, substructure, buckling, transient, or harmonic analysis
        is to be performed.

        This separate solution pass requires an explicit :ref:`finish` from the preceding analysis and
        reentry into SOLUTION.

        The ``KeyStat`` argument is applicable to the expansion pass of a substructure analysis, and to the
        expansion pass of a component mode synthesis (CMS) analysis when the CMS method is fixed-interface
        or free-interface. For a substructure analysis, the static correction vectors are the first terms of
        in the `Mechanical APDL Theory Reference
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_biblio.html>`_. For a CMS
        analysis, the static correction vectors are the third terms of.

        This command is also valid in PREP7.
        """
        command = f"EXPASS,{key},,,{keystat}"
        return self.run(command, **kwargs)

    def gauge(self, opt: str = "", freq: int | str = "", **kwargs):
        r"""Gauges the problem domain for a magnetic edge-element formulation.

        Mechanical APDL Command: `GAUGE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_GAUGE.html>`_

        Parameters
        ----------
        opt : str
            Type of gauging to be performed:

            * ``ON`` - Perform tree gauging of the edge values (default).

            * ``OFF`` - Gauging is off. (You must specify custom gauging via APDL specifications.)

            * ``STAT`` - Gauging status (returns the current ``Opt`` and ``FREQ`` values)

        freq : int or str
            The following options are valid when ``Opt`` = ON:

            * ``0`` - Generate tree-gauging information once, at the first load step. Gauging data is retained
              for subsequent load steps. (This behavior is the default.)

            * ``1`` - Repeat gauging for each load step. Rewrites the gauging information at each load step to
              accommodate changing boundary conditions on the AZ degree of freedom (for example, adding or
              deleting AZ constraints via the :ref:`d` or :ref:`ce` commands).

        Notes
        -----

        .. _GAUGE_notes:

        The :ref:`gauge` command controls the tree-gauging procedure required for electromagnetic analyses
        using an edge-based magnetic formulation (elements ``SOLID226``, ``SOLID227``, ``SOLID236`` and
        ``SOLID237`` ).

        Gauging occurs at the solver level for each solution ( :ref:`solve` ). It sets additional zero
        constraints on the edge-flux degrees of freedom AZ to produce a unique solution; the additional
        constraints are removed after solution.

        Use the ``FREQ`` option to specify how the command generates gauging information for multiple load
        steps.

        Access the gauging information via the _TGAUGE component of gauged nodes. The program creates and
        uses this component internally to remove and reapply the AZ constraints required by gauging. If
        ``FREQ`` = 0, the _TGAUGE component is created at the first load step and is used to reapply the
        tree gauge constraints at subsequent load steps. If ``FREQ`` = 1, the tree-gauging information and
        the _TGAUGE component are generated at every load step

        If gauging is turned off ( :ref:`gauge`,OFF), you must specify your own gauging at the APDL level.

        This command is also valid in PREP7.
        """
        command = f"GAUGE,{opt},{freq}"
        return self.run(command, **kwargs)

    def gmatrix(
        self,
        symfac: str = "",
        condname: str = "",
        numcond: str = "",
        matrixname: str = "",
        **kwargs,
    ):
        r"""Performs electric field solutions and calculates the self and mutual conductance between multiple
        conductors.

        Mechanical APDL Command: `GMATRIX <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_GMATRIX.html>`_

        Parameters
        ----------
        symfac : str
            Geometric symmetry factor. Conductance values are scaled by this factor which represents the
            fraction of the total device modeled. Defaults to 1.

        condname : str
            Alphanumeric prefix identifier used in defining named conductor components.

        numcond : str
            Total number of components. If a ground is modeled, it is to be included as a component.

        matrixname : str
            Array name for computed conductance matrix. Defaults to GMATRIX.

        Notes
        -----
        To invoke the :ref:`gmatrix` macro, the exterior nodes of each conductor must be grouped into
        individual components using the :ref:`cm` command. Each set of independent components is assigned a
        component name with a common prefix followed by the conductor number. A conductor system with a
        ground must also include the ground nodes as a component. The ground component is numbered last in
        the component name sequence.

        A ground conductance matrix relates current to a voltage vector. A ground matrix cannot be applied
        to a circuit modeler. The lumped conductance matrix is a combination of lumped "arrangements" of
        voltage differences between conductors. Use the lumped conductance terms in a circuit modeler to
        represent conductances between conductors.

        Enclose all name-strings in single quotes in the :ref:`gmatrix` command line.

        :ref:`gmatrix` works with the following elements:

        * ``SOLID5`` (KEYOPT(1) = 9)

        * ``SOLID98`` (KEYOPT(1) = 9)

        * ``LINK68``

        * ``PLANE230``

        * ``SOLID231``

        * ``SOLID232``

        This command is available from the menu path shown below only if existing results are available.

        This command does not support multiframe restarts Distributed-Memory Parallel (DMP) Restriction This
        command is not supported in a DMP solution.
        """
        command = f"GMATRIX,{symfac},{condname},{numcond},,{matrixname}"
        return self.run(command, **kwargs)

    def invopt(self, option: str = "", **kwargs):
        r"""Enables or disables inverse solving for the current load step.

        Mechanical APDL Command: `INVOPT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_INVOPT.html>`_

        Parameters
        ----------
        option : str
            Enables or disables inverse solving for a load step:

            * ``ON`` - Enable.

            * ``OFF`` - Disable and revert to forward solving (default).

        Notes
        -----

        .. _INVOPT_notes:

        ``Option`` = ON is valid only at the first load step of a static analysis. Large-deflection effects
        must be enabled ( :ref:`nlgeom`,ON). The unsymmetric solver ( :ref:`nropt`,UNSYM) is required and
        the program selects it automatically.

        After issuing :ref:`invopt`,ON, inverse solving remains in effect until :ref:`invopt`,OFF is
        issued. The solution then reverts to traditional forward solving (default).

        This command cannot be issued during a restart. ``Option`` can only be changed between load steps.

        For more information, see `Nonlinear Static Analysis with Inverse Solving
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/strnonlininversesol.html#strinvsolvlimit>`_
        """
        command = f"INVOPT,{option}"
        return self.run(command, **kwargs)

    def lanboption(
        self, strmck: str = "", altmeth: str = "", memory_option: str = "", **kwargs
    ):
        r"""Specifies Block Lanczos eigensolver options.

        Mechanical APDL Command: `LANBOPTION <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_LANBOPTION.html>`_

        Parameters
        ----------
        strmck : str
            Controls whether the Block Lanczos eigensolver will perform a Sturm sequence check:

            * ``OFF`` - Do not perform the Sturm sequence check (default).

            * ``ON`` - Perform a Sturm sequence check. This requires additional matrix factorization (which can
              be expensive), but does help ensure that no modes are missed in the specified range.

        altmeth : str

            * ``ALT1`` - Alternative version of the Block Lanczos eigensolver for more difficult modal or
              buckling problems. This version of Block Lanczos only runs in shared-memory parallel (SMP) mode. If
              the analysis is run in distributed-memory parallel (DMP) mode, it will switch to SMP mode when this
              Alternative Block Lanczos solver is invoked, and resume in DMP mode after the eigensolution.

        memory_option : str
            Memory allocation option:

            * ``DEFAULT`` - Default memory configuration (default). Everything is determined dynamically with
              respect to current machine resources.

            * ``INCORE`` - Fully in-core memory configuration.

            * ``MIX1`` - First level of mixed in-core / out-of-core configuration.

            * ``MIX2`` - Second level of mixed in-core / out-of-core configuration.

            * ``OUTOFCORE`` - Fully out-of-core memory configuration.

        Notes
        -----

        .. _LANBOPTION_notes:

        :ref:`lanboption` specifies options to be used with the Block Lanczos eigensolver during an
        eigenvalue buckling analysis ( :ref:`bucopt`,LANB) or a modal analysis ( :ref:`modopt`,LANB).

        For more difficult eigenproblems, ``AltMeth`` = ALT1 could achieve better converged eigensolutions
        at the cost of more computing time. This ALT1 option is useful for double-checking solution
        accuracy. It should be used for difficult eigenproblems like those with many duplicated eigenmodes,
        or eigen-buckling problems with very thin beam/shell structures.

        **Memory Allocation Option**

        The Block Lanczos eigensolver algorithm allocates two main pools of memory:

        Memory for the internal sparse solver iterations.

        Memory for the specific Lanczos working arrays.

        The following table shows how memory is allocated for each option.

        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.

        The MIX1 configuration typically uses more memory than the MIX2 configuration, except when a large
        number of modes are requested for a small model.
        """
        command = f"LANBOPTION,{strmck},,{altmeth},{memory_option}"
        return self.run(command, **kwargs)

    def lumpm(self, key: str = "", keyelt: int | str = "", **kwargs):
        r"""Specifies a lumped mass matrix formulation.

        Mechanical APDL Command: `LUMPM <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_LUMPM.html>`_

        Parameters
        ----------
        key : str
            Formulation key:

            * ``OFF`` - Use the element-dependent default mass matrix formulation (default).

            * ``ON`` - Use a lumped mass approximation.

        keyelt : int or str
            Formulation key for elements with rotational degrees of freedom; applicable only when the lumped
            mass formulation key is turned on ( ``Key`` = ON):

            * ``0 (blank)`` - Use direct diagonalization of the element mass matrix (default).

            * ``1`` - Use translational mass only.

            * ``2`` - Use the frame invariant formulation.

        Notes
        -----

        .. _LUMPM_notes:

        In a modal analysis, the lumped mass matrix option ( :ref:`lumpm`,ON) is not allowed when using the
        Supernode mode-extraction method ( :ref:`modopt`,SNODE). The eigensolver will automatically be
        switched to Block Lanczos (LANB) in this case.

        In the use pass of a substructuring analysis, the lumped mass matrix formulation ( :ref:`lumpm`,ON)
        modifies the superelement mass matrix and may give unexpected results.

        The translational mass only option ( :ref:`lumpm`,ON,,1) applies to the following elements:
        ``SHELL181``, ``BEAM188``, ``BEAM189``, ``SHELL208``, ``SHELL209``, ``SHELL281``, ``PIPE288``,
        ``PIPE289``, and ``ELBOW290``. The frame invariant formulation ( :ref:`lumpm`,ON,,2) applies only to
        ``BEAM188``, ``BEAM189``, ``PIPE288``, and ``PIPE289`` elements.

        For more information, see `Lumped Matrices
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_et2.html#eltlimitlump>`_

        This command is also valid in PREP7. If used in SOLUTION, this command is valid only within the
        first load step.
        """
        command = f"LUMPM,{key},,{keyelt}"
        return self.run(command, **kwargs)

    def moddir(self, key: str = "", directory: str = "", fname: str = "", **kwargs):
        r"""Enables remote read-only usage of modal analysis files or substructuring analysis files.

        Mechanical APDL Command: `MODDIR <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MODDIR.html>`_

        Parameters
        ----------
        key : str
            Key for enabling remote read-only usage of modal analysis files or `substructuring
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_substr/advcms.html>`_ analysis files:

            * ``1 (ON or YES)`` - The program performs the analysis using remote files. The files are read-only.

            * ``0 (OFF or NO)`` - The program performs the analysis using files located in the working directory
              (default).

            * ``LIST`` - List remote modal files status, directory path, and file name.

        directory : str
            Directory path (248 characters maximum). The directory contains the modal analysis files or the
            substructuring generation pass files.

            The directory path defaults to the current working directory.

        fname : str
            File name (no extension or directory path) for the modal analysis files or the substructuring
            generation pass files.

            The file name defaults to the current :file:`Jobname`.

        Notes
        -----

        .. _MODDIR_notes:

        This commands is used when solving linked analyses in two different folders. It is mostly meant to
        be used to reduce solution time and disk space usage by specifying the path to required solution
        files rather than copying them in the Mechanical Application (see the file management sections of
        the following
        analyses: mode-superposition transient, mode-superposition harmonic, response spectrum, random
        vibration, and substructure generation in the Mechanical User's Guide ).

        This command applies to the following analysis types:

        * Spectrum ( :ref:`antype`,SPECTR)

        * Modal restart ( :ref:`antype`, MODAL, RESTART)

        * Mode-superposition transient ( :ref:`antype`,TRANS and :ref:`trnopt`, MSUP)

        * Mode-superposition harmonic ( :ref:`antype`,HARM and :ref:`hropt`, MSUP)

        * Substructuring ( :ref:`antype`,SUBSTR).

        Using the default for both the directory path ( ``Directory`` ) and the file name ( ``Fname`` ) is
        not valid. At least one of these values must be specified.

        In a spectrum analysis and in mode-superposition analyses, :ref:`moddir` must be issued during the
        first solution and at the beginning of the solution phase (before :ref:`lvscale` in particular). In
        a spectrum analysis, remote modal files usage is not supported when mode file reuse is activated (
        ``modeReuseKey`` = YES on :ref:`spopt` ).

        After a `PSD spectrum analysis
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STR6_8.html#aiiQxq1b2mcm>`_,
        :ref:`moddir` can be issued in POST26 prior to the :ref:`store` command.

        In a modal restart analysis, :ref:`moddir` must be issued during the first solution. Remote modal
        files usage cannot be activated in a modal restart analysis if during the first modal analysis:

        * Enforced static modes have been calculated ( ``EnforcedKey`` = ON on :ref:`modcont` ).

        * Element result superposition key ( ``MSUPkey`` on :ref:`mxpand` ) was set to NO, whereas it is set
          to YES in the modal restart.

        When using distributed-memory parallel processing, if element results calculation based on element
        modal results is activated for the spectrum analysis ( ``Elcalc`` = YES on :ref:`spopt` ),
        :ref:`moddir` usage can significantly reduce computation time as it decreases the size of the
        distributed :file:`.rst` files to be combined at the end of spectrum analysis solution.

        In a substructuring or CMS analysis, :ref:`moddir` can be issued during either of the following
        analysis phases:

        * The first solution of the first restart of a generation pass. ``ExpMth`` on :ref:`seopt` must be
          set to MODDIR during the first solve of the primary generation pass.

        * The first solution of the expansion pass.

        """
        command = f"MODDIR,{key},{directory},{fname}"
        return self.run(command, **kwargs)

    def monitor(self, var: str = "", node: str = "", lab: str = "", **kwargs):
        r"""Controls contents of variable fields in the nonlinear solution monitor file.

        Mechanical APDL Command: `MONITOR <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MONITOR.html>`_

        Parameters
        ----------
        var : str
            One of four variable field numbers in the monitor file whose contents can be specified by the
            Lab field. Valid arguments are integers 1, 2, 3, or 4. See Notes section for default values.

        node : str
            The node number for which information is monitored in the specified ``VAR`` field. In the GUI,
            if ``Node`` = P, graphical picking is enabled. If blank, the monitor file lists the maximum
            value of the specified quantity (Lab field) for the entire structure.

        lab : str
            The solution quantity to be monitored in the specified ``VAR`` field. Valid labels for solution
            quantities are UX, UY, and UZ (displacements); ROTX, ROTY, and ROTZ (rotations); and TEMP
            (temperature). Valid labels for reaction force are FX, FY, and FZ (structural force) and MX, MY,
            and MZ (structural moment). Valid label for heat flow rate is HEAT. For defaults see the Notes
            section.

        Notes
        -----

        .. _MONITOR_notes:

        The monitor file always has an extension of **.mntr**, and takes its file name from the specified
        :file:`Jobname`. If no :file:`Jobname` is specified, the file name defaults to :file:`file`.

        You must issue this command once for each solution quantity you want to monitor at a specified node
        at each load step. You cannot monitor a reaction force during a linear analysis. The variable field
        contents can be redefined at each load step by reissuing the command. The monitored quantities are
        appended to the file for each load step.

        Reaction forces reported in the monitor file may be incorrect if the degree of freedom of the
        specified node is involved in externally defined coupling ( :ref:`cp` command) or constraint
        equations ( :ref:`ce` command), or if the program has applied constraint equations internally to the
        node.

        The following example shows the format of a monitor file. Note that the file only records the
        solution substep history when a substep is convergent.

        _font TypeSize="8pt"? SOLUTION HISTORY INFORMATION FOR JOB: file.mntr LOAD SUB- NO. NO. TOTL
        INCREMENT TOTAL VARIAB 1
        VARIAB 2 VARIAB 3 VARIAB 4 STEP STEP ATTMP ITER ITER TIME/LFACT TIME/LFACT MONITOR MONITOR MONITOR
        MONITOR Wall MxDs FY MxRe 1 1 1 5 5 0.36000E-01 0.36000E-01 0.0000 -0.47242E-01 -0.13783E-01
        0.22670E-04 1 2 1 3 8 0.36000E-01 0.72000E-01 0.0000 -0.91552E-01 -0.27269E-01 0.38849E-03 1 3 1 4
        12 0.54000E-01 0.12600 0.0000 -0.15161 -0.43972E-01 0.25235E-03 1 4 1 3 15 0.81000E-01 0.20700
        0.0000 -0.22926 -0.65119E-01 0.11131E-03 1 5 1 5 20 0.12150 0.32850 0.0000 -0.34188 -0.93242E-01
        0.12267E-02 1 6 1 4 24 0.12150 0.45000 0.0000 -0.46860 -0.11992 0.22689E-02 1 7 1 5 29 0.18000
        0.63000 0.0000 -0.65720 -0.16217 0.12111E-03 1 8 2 7 38 0.63000E-01 0.69300 0.0000 -0.72594 -0.46582
        0.67121E-02 1 9 1 11 49 0.63000E-01 0.75600 0.0000 -0.79976 -1.1070 0.29302E-02 1 10 1 10 59
        0.63000E-01 0.81900 0.0000 -0.87073 -1.8708 0.95828E-02 1 11 1 18 77 0.81000E-01 0.90000 0.0000
        -0.90000 -269.31 0.73911/_font?
        The following details the contents of the various fields in the monitor file:

        * ``LOAD STEP`` - The current load step number.

        * ``SUBSTEP`` - The current substep (time step) number.

        * ``NO. ATTEMPT`` - The number of attempts made in solving the current substep. This number is equal
          to the number of failed attempts (bisections) plus one (the successful attempt).

        * ``NO. ITER`` - The number of iterations used by the last successful attempt.

        * ``TOTL. ITER`` - Total cumulative number of iterations (including each iteration used by a
          bisection).

        * ``INCREMENT`` -

        * ``TIME/LFACT`` - Time or load factor increments for the current substep.

        * ``TOTAL TIME/LFACT`` - Total time (or load factor) for the last successful attempt in the current
          substep.

        * ``VARIAB 1`` - Variable field 1. By default, this field lists the elapsed (or wall clock) times
          used up to (but not including) the current substep.

        * ``VARIAB 2`` - Variable field 2. In this example, the field is reporting the MZ value. By default,
          this field lists the maximum displacement in the entire structure.

        * ``VARIAB 3`` - Variable field 3. In this example, the field is reporting the FY value of a certain
          node. By default, this field reports the maximum equivalent plastic strain increment in the entire
          structure.

        * ``VARIAB 4`` - Variable field 4. By default, this field reports the maximum residual force in the
          entire structure.
        """
        command = f"MONITOR,{var},{node},{lab}"
        return self.run(command, **kwargs)

    def msave(self, key: str = "", **kwargs):
        r"""Sets the solver memory saving option. This option only applies to the PCG solver (including PCG
        Lanczos).

        Mechanical APDL Command: `MSAVE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MSAVE.html>`_

        Parameters
        ----------
        key : str
            Activation key:

            * ``0 or OFF`` - Use global assembly for the stiffness matrix (and mass matrix, when using PCG
              Lanczos) of the entire model.

            * ``1 or ON`` - Use an element-by-element approach when possible to save memory during the solution.
              In this case, the global stiffness (and mass) matrix is not assembled; element stiffness (and mass)
              is regenerated during PCG or PCG Lanczos iterations.

        Notes
        -----

        .. _MSAVE_notes:

        :ref:`msave`,ON only applies to and is the default for parts of the model using the following
        element types with linear material properties that meet the conditions listed below.

        * ``SOLID186`` (Structural Solid only)

        * ``SOLID187``

        The following conditions must also be true:

        * The PCG solver has been specified.

        * Small strains are assumed ( :ref:`nlgeom`,OFF).

        * No prestress effects ( :ref:`pstres` ) are included.

        * All nodes on the supported element types must be defined (that is, the midside nodes cannot be
          removed using the :ref:`emid` command).

        * For elements with thermally dependent material properties, :ref:`msave`,ON applies only to
          elements with uniform temperatures prescribed.

        * The default element coordinate system must be used.

        If you manually force :ref:`msave`,ON by including it in the input file, the model can include the
        following additional conditions:

        * The analysis can be a modal analysis using the PCG Lanczos method ( :ref:`modopt`,LANPCG).

        * Large deflection effects ( :ref:`nlgeom`,ON) can be included for ``SOLID186`` and/or ``SOLID187``
          elements.

        * ``SOLID185`` (brick shapes and KEYOPT(2) = 3 only) elements can be included for small strains (
          :ref:`nlgeom`,OFF).

        All other element types or other parts of the model that don't meet the above criteria will be
        solved using global assembly ( :ref:`msave`,OFF). This command can result in memory savings of up to
        70 percent over the global assembly approach for the part of the model that meets the criteria.
        Depending on the hardware (for example, processor speed, memory bandwidth, etc.), the solution time
        may increase or decrease when this feature is used.

        This memory-saving feature runs in parallel when multiple processors are used with the :ref:`config`
        command or in a distributed-memory parallel (DMP) solution. The gain in performance with using
        multiple processors with this feature turned on should be similar to the default case when this
        feature is turned off. Performance also improves when using the uniform reduced integration option
        for ``SOLID186`` elements.

        This command does not support the layered option of the SOLID185 and ``SOLID186`` elements.

        When using :ref:`msave`,ON with the :ref:`pcgopt` command, note the following restrictions:

        * For static and modal analyses, :ref:`msave`,ON is not valid when using a ``Lev_Diff`` value of 5
          on the :ref:`pcgopt` command; ``Lev_Diff``  is automatically reset to 2.

        * For modal analyses, :ref:`msave`,ON is not valid with the ``StrmCk`` option of the :ref:`pcgopt`
          command; ``Strmck``  is set to OFF.

        * For all analysis types, :ref:`msave`,ON is not valid when the Lagrange multiplier option (
          ``LM_Key`` ) of the :ref:`pcgopt` command is set to ON; the :ref:`msave` activation key is set to
          OFF.

        * For linear perturbation static and modal analyses, :ref:`msave`,ON is not valid; the :ref:`msave`
          activation key is set to OFF.

        * For static analyses, :ref:`msave`,ON is not valid when the ``Fallback`` option of the
          :ref:`pcgopt` command is enabled; ``Fallback`` is automatically reset to OFF.

        When using :ref:`msave`,ON for modal analyses, no :file:`.FULL` file will be created. The
        :file:`.FULL` file may be necessary for subsequent analyses (for example, harmonic, transient mode-
        superposition, or spectrum analyses). To generate the :file:`.FULL` file, rerun the modal analysis
        using the :ref:`wrfull` command.
        """
        command = f"MSAVE,{key}"
        return self.run(command, **kwargs)

    def msolve(
        self,
        numslv: str = "",
        val1: str = "",
        val2: str = "",
        lab: str = "",
        angfix: str = "",
        **kwargs,
    ):
        r"""Starts multiple solutions for an acoustic analysis.

        Mechanical APDL Command: `MSOLVE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MSOLVE.html>`_

        Parameters
        ----------
        numslv : str
            Number of multiple solutions (load steps). This number corresponds to the number of random
            samplings for the diffuse sound field in a random acoustic analysis, or the incident angles of
            the plane wave when the Floquet periodic boundary condition is present. Default = 1.

        val1 : str
            The meaning of ``VAL1`` depends on the ``Lab`` value.

            For ``Lab`` = DSF, ``VAL1`` is the norm convergence tolerance defined by comparing the averaged
            radiated diffuse sound power of two multiple sampling sets over the frequency range for the
            diffuse sound field (default = 0.05).

            For ``Lab`` = APHI or ATHETA, ``VAL1`` is the beginning angle for the incident angle sweep of
            the plane wave (default = 0).

        val2 : str
            The meaning of ``VAL2`` depends on the ``Lab`` value.

            For ``Lab`` = DSF, ``VAL2`` is the interval of the norm convergence check for the diffuse sound
            field (default = 5).

            For ``Lab`` = APHI or ATHETA, ``VAL2`` is the ending angle for the incident angle sweep of the
            plane wave (default = 0).

        lab : str
            Label indicating the type of acoustic analysis:

            * ``DSF`` - Diffuse sound field with multiple solutions (default).

            * ``APHI`` - Plane wave angle sweep with fixed :math:`equation not available`  angle and varied
              :math:`equation not available`  angle (see the  :ref:`aport` command).

            * ``ATHETA`` - Plane wave angle sweep with fixed :math:`equation not available`  angle and varied
              :math:`equation not available`  angle (see the  :ref:`aport` command).

        angfix : str
            The value of the fixed incident angle for the plane wave angle sweep (used only when ``Lab`` =
            APHI or ATHETA).

        Notes
        -----
        The :ref:`msolve` command starts multiple solutions (load steps) for a random acoustic analysis with
        multiple samplings or for the angle sweep of the incident plane wave with the Floquet periodic
        boundary condition, as described below.

        **Random Acoustic Analysis (** ``Lab`` = DSF)

        Use ``Lab`` = DSF for a random acoustic analysis. The process is controlled by the norm convergence
        tolerance ( ``VAL1`` ) or the number of multiple solutions ( ``NUMSLV`` ) if the solution steps
        reach the defined number.

        The program checks the norm convergence by comparing two averaged sets of radiated sound powers with
        the interval ``VAL2`` over the frequency range. For example, if ``VAL2`` = 5, the averaged values
        from 5 solutions are compared with the averaged values from 10 solutions, then the averaged values
        from 10 solutions are compared with the averaged values from 15 solutions, and so on.

        The incident diffuse sound field is defined via the :ref:`dfswave` command.

        The average result of multiple solutions with different samplings is calculated via the :ref:`pras`
        or :ref:`plas` command.

        **Plane Wave Incident Angle Sweep (** ``Lab`` = APHI or ATHETA)

        Use ``Lab`` = APHI or ATHETA to perform an angle sweep for the incident plane wave defined by the
        :ref:`aport` command. The process is controlled by the number of multiple solutions ( ``NUMSLV`` ).
        The plane wave port must be defined with the default values of incident angles prior to the
        :ref:`msolve` command.

        The sound power parameters are calculated over the sweeping angles during postprocessing by the
        :ref:`pras` or :ref:`plas` command.
        """
        command = f"MSOLVE,{numslv},{val1},{val2},{lab},{angfix}"
        return self.run(command, **kwargs)

    def opncontrol(self, lab: str = "", value: str = "", numstep: str = "", **kwargs):
        r"""Sets decision parameter for automatically increasing the time step interval in a pure thermal
        analysis.

        Mechanical APDL Command: `OPNCONTROL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_OPNCONTROL.html>`_

        Parameters
        ----------
        lab : str
            * ``TEMP`` - Degree-of-freedom label used to base a decision for increasing the time step (substep)
              interval in a nonlinear or transient analysis. The only DOF label currently supported is TEMP.

            * ``OPENUPFACTOR`` - Key to set a multiplier for increasing the time step interval as specified in ``VALUE`` > 1.0 (up to
              10.0). Valid only when :ref:`autots`,ON has been issued.

              The multiplier is set by issuing :ref:`opncontrol`,OPENUPFACTOR, ``VALUE`` as follows:

              * For a pure thermal analysis, if ``VALUE`` > 1.0, the OPENUPFACTOR is the minimum of 10.0,
                ``VALUE``.

              If the user does not specify the multiplier, the default is 3.0.

              Generally, ``VALUE`` > 3.0 is not recommended. Note that in some rare cases this specification can
              be overwritten by internal heuristics in determining the new time step interval.

        value : str
            A context sensitive value that depends on ``Lab`` :

            * If ``Lab`` = TEMP, ``VALUE`` is used together with ``NUMSTEP`` in the algorithm for determining if
              the time step interval can be increased. The time step interval is increased if the maximum
              absolute value of the incremental solution is less than ``VALUE`` for the number of contiguous
              time steps specified by ``NUMSTEP`` (default ``VALUE`` = 0.1).

            * If ``Lab`` = OPENUPFACTOR, ``VALUE`` is a multiplier (= 1.0 - 10.0) that can be specified for a
              pure thermal analysis as described above.

        numstep : str
            Valid only when ``Lab`` = TEMP. A value used together with ``VALUE`` in the algorithm for
            determining if the time step interval can be increased. The time step interval is increased if
            the maximum absolute value of the incremental solution at the specified TEMP label is less than
            ``VALUE`` for the number of contiguous time steps specified by ``NUMSTEP`` (default ``NUMSTEP``
            = 3).

        Notes
        -----

        .. _OPNCONTROL_notes:

        This command is available only for nonlinear static or full transient analyses. :ref:`opncontrol`
        enables an increase in the current time step size. It is analogous to the :ref:`cutcontrol` command,
        but with the opposite effect. :ref:`cutcontrol` reduces the step size for analyses experiencing
        convergence difficulties while :ref:`opncontrol` increases the step size to speed up converging
        analyses.

        The increase in the current time step size via :ref:`opncontrol` occurs when:

        * a trigger mechanism is encountered and

        * a multiplier (greater than 1.0) is set.

        Different internal heuristics are used to automatically trigger the increase of the time step for
        different physics. However, for a pure thermal analysis, an additional trigger to increase the step
        size can be implemented by issuing :ref:`opncontrol`,TEMP.

        The multiplier is set by issuing :ref:`opncontrol`,OPENUPFACTOR, ``VALUE`` (see details for
        different analysis types in the OPENUPFACTOR argument description above).

        For linear full transient analysis, where the time step interval can be predominantly determined by
        the estimated modal frequency (number of solution points in a cycle in the dynamic system), the
        multiplier set via the OPENUPFACTOR argument may show no effect.
        """
        command = f"OPNCONTROL,{lab},{value},{numstep}"
        return self.run(command, **kwargs)

    def outaero(self, sename: str = "", timeb: str = "", dtime: str = "", **kwargs):
        r"""Outputs the superelement matrices and load vectors to formatted files for aeroelastic analysis.

        Mechanical APDL Command: `OUTAERO <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/None>`_

        Parameters
        ----------
        sename : str
            Name of the superelement that models the wind turbine supporting structure. Defaults to the
            current Jobname.

        timeb : str
            First time at which the load vector is formed (defaults to be read from :file:`SENAME.sub` ).

        dtime : str
            Time step size of the load vectors (defaults to be read from :file:`SENAME.sub` ).

        Notes
        -----

        .. _OUTAERO_notes:

        Both TIMEB and DTIME must be blank if the time data is to be read from the :file:`SENAME.sub` file.

        The matrix file ( :file:`SENAME.SUB` ) must be available from the substructure generation run before
        issuing this command. This superelement that models the wind turbine supporting structure must
        contain only one master node with six freedoms per node: UX, UY, UZ, ROTX, ROTY, ROTZ. The master
        node represents the connection point between the turbine and the supporting structure.

        This command will generate four files that are exported to the aeroelastic code for integrated wind
        turbine analysis. The four files are :file:`Jobname.GNK` for the generalized stiffness matrix,
        :file:`Jobname.GNC` for the generalized damping matrix, :file:`Jobname.GNM` for the generalized mass
        matrix and :file:`Jobname.GNF` for the generalized load vectors.

        For detailed information on how to perform a wind coupling analysis, see `Coupling to External
        Aeroelastic Analysis of Wind Turbines
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_adv/advaerosequential.html>`_
        """
        command = f"OUTAERO,{sename},{timeb},{dtime}"
        return self.run(command, **kwargs)

    def pcgopt(
        self,
        lev_diff: str = "",
        fallback: str = "",
        reduceio: str = "",
        strmck: str = "",
        wrtfull: str = "",
        lm_key: str = "",
        **kwargs,
    ):
        r"""Controls PCG solver options.

        Mechanical APDL Command: `PCGOPT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PCGOPT.html>`_

        Parameters
        ----------
        lev_diff : str
            Indicates the level of difficulty of the analysis. Valid settings are AUTO or 0 (default), 1, 2, 3,
            4, or 5. This option applies to both the PCG solver when used in static and full transient analyses
            and to the PCG Lanczos method in modal analyses.

            * Specify AUTO to allow Mechanical APDL to select the proper level of difficulty for the model.
            * Lower values (1 or 2) generally provide the best performance for well-conditioned problems.
            * Values of 3 or 4 generally provide the best performance for ill-conditioned problems; however,
              higher values may increase the solution time for well-conditioned problems. Higher level-of-
              difficulty values typically require more memory.
            * The highest value of 5 essentially performs a factorization of the global matrix (similar to the
              sparse solver) and may require a very large amount of memory. This level is generally recommended
              for small- to medium-sized problems when using the PCG Lanczos mode-extraction method.

            For example, models containing elongated elements (that is, elements with high aspect ratios) and
            models containing contact elements can lead to ill-conditioned problems. To determine if your
            problem is ill-conditioned, view the :file:`Jobname.PCS` file to see the number of PCG iterations
            needed to reach a converged solution. Generally, static or full transient solutions that require
            more than 1500 iterations are considered to be ill-conditioned for the PCG solver.

        fallback : str
            Controls whether Mechanical APDL switches to the sparse direct solver automatically ( :ref:`eqslv`,SPARSE)
            under certain conditions. (The criteria are listed below.) When Mechanical APDL switched the equation
            solver, the simulation attempts to continue without interruption.

            * ``AUTO`` - Automatically switch to the sparse solver when one of the following conditions apply (default):

              * The assembled matrix is detected to be indefinite.

              * The PCG solver requires more than 2000 iterations to reach convergence.

              * The PCG solver fails to converge.

            * ``ON`` - More aggressive fallback criteria. Automatically switch to the sparse solver when one of the
              following conditions apply:

              * The assembled matrix is detected to be indefinite.

              * The PCG solver requires more than 1500 iterations to reach convergence.

              * The PCG solver fails to converge.

            * ``OFF`` - Disables the fallback logic so that there is no automatic switching, and only the PCG
              solver is used to solve the equations for this simulation.

            After switching to the sparse solver, the program reverts back to the PCG solver under certain
            conditions. See the :ref:`Notes section for details. <PCGOPT_Notes_revertAfterFallback>`

        reduceio : str
            Controls whether the PCG solver will attempt to reduce I/O performed during equation solution:

            * ``AUTO`` - Automatically chooses whether to reduce I/O or not (default).

            * ``YES`` - Reduces I/O performed during equation solution in order to reduce total solver time.

            * ``NO`` - Does NOT reduce I/O performed during equation solution.

            This option applies to both the PCG solver when used in static and full transient analyses and to
            the PCG Lanczos method in modal analyses.

        strmck : str
            Controls whether or not a Sturm sequence check is performed:

            * ``OFF`` - Does NOT perform Sturm sequence check (default).

            * ``ON`` - Performs Sturm sequence check

            This option applies only when using the PCG Lanczos method in modal analyses. When using this
            option, a factorization must be performed and will require a very large amount of memory for extra
            computations. This option is generally recommended for small- to medium-sized problems. If the Sturm
            sequence check takes a large amount of computing time, use the :file:`Jobname.ABT` file to abort the
            Sturm check, or press the STOP button if in interactive mode.

        wrtfull : str
            Controls whether or not the :file:`.FULL` file is written.

            * ``ON`` - Write :file:`.FULL` file (default)

            * ``OFF`` - Do not write :file:`.FULL` file.

            This option applies only when using the PCG Lanczos method in modal analyses because the
            :file:`.FULL` file is never written when using the PCG solver in static or full transient analyses.

            If using :ref:`msave`,ON and conditions for the :ref:`msave` command are met, a complete
            :file:`.FULL` file is never written regardless of this option.

            If constraint equations are present in the model, a :file:`.FULL` file is always written regardless
            of this option.

            This option is useful in a distributed-memory parallel processing analysis because assembling the
            global stiffness and mass matrices on the head compute node before writing the :file:`.FULL` file
            can take a considerable amount of memory. By setting ``Wrtfull`` = OFF, this assembly process is
            skipped on the head compute node, decreasing the amount of memory required to compute the modes and
            mode shapes. ``Wrtfull`` = OFF does not affect the results for the modes and mode shapes. However,
            without a :file:`.FULL` file, the participation factor table computations do not occur.

            To generate the :file:`.FULL` file, such as for a harmonic, transient mode-superposition, or
            spectrum analysis, rerun the modal analysis with ``Wrtfull`` = ON, or use the :ref:`wrfull` command.

        lm_key : str
            Controls use of the PCG solver for ``MPC184``  elements that involve the Lagrange multiplier method.
            This option applies only to the PCG solver when used in static analyses, full transient analyses,
            and modal analyses that use the PCG Lanczos mode-extraction method ( :ref:`modopt`,LANPCG).

            * ``ON`` - Allow use of the PCG solver with certain ``MPC184`` element types that use the Lagrange
              multiplier method. (default)

            * ``OFF`` - Do not use the PCG solver with any ``MPC184`` element types that use the Lagrange
              multiplier method.

            The Lagrange multiplier method used by ``MPC184`` elements transfers the Lagrange multipliers into
            multiple point constraints and, hence, can be solved by the PCG solver. The current ``MPC184``
            element types supported are: `rigid beam
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_MPC184link.html#mpc184linkprores>`_,
            `rigid link
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_MPC184link.html#mpc184linkprores>`_,
            `slider
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_MPC184slid.html#mpc184slidprores>`_,
            `revolute joint
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_MPC184revo.html#mpc184revoprores>`_,
            `universal joint
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_MPC184univ.html#mpc184univprores>`_,
            `translational joint
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_MPC184tran.html#mpc184transprores>`_,
            `cylindrical joint
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_MPC184cyl.html#mpc184cylinprores>`_,
            `weld joint
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_MPC184weld.html#mpc184weldprores>`_,
            `spherical joint
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_MPC184sphe.html#mpc184spherprores>`_,
            and `general joint
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_MPC184gen.html#mpc184generprores>`_
            . For all other ``MPC184`` element types, the PCG solver cannot be used, and the equation solver
            automatically switches to the sparse solver regardless of the ``LM_Key`` setting on :ref:`pcgopt`.
            The :ref:`msave` command does not support the ``LM_Key`` = ON option.

        Notes
        -----
        ``ReduceIO`` works independently of the :ref:`msave` command in the PCG solver. Setting ``ReduceIO``
        to YES can significantly increase the memory usage in the PCG solver.

        To minimize the memory used by the PCG solver with respect to the ``Lev_Diff`` option only, set
        ``Lev_Diff`` = 1 if you do not have sufficient memory to run the PCG solver with ``Lev_Diff`` =
        AUTO.

        The :ref:`msave`,ON command is not valid in these circumstances:

        * when ``Lev_Diff`` = 5; in this case, the ``Lev_Diff`` value will automatically be reset to 2.

        * with the ``StrmCk`` option; in this case, ``StrmCk`` will be set to OFF.

        * when the ``Fallback`` option is enabled (set to AUTO or ON); in this case, ``Fallback`` will
          automatically be reset to OFF.

        For Lagrange-formulation contact methods and mixed u-P formulations, the PCG solver cannot be used,
        and the sparse solver is required.

        ``Fallback`` logic is automatically disabled ( ``Fallback`` = OFF) in these circumstances:

        * for analyses that include ``MPC184`` elements using the Lagrange multiplier method to impose
          kinematic constraints

        * for thermal analyses that use the quasi-static ( :ref:`thopt`,QUASI) option.

        **Reverting to the PCG Solver After an Automatic Switch to the Sparse Solver**

        **Linear Analysis:** When fallback logic is enabled ( ``Fallback`` = AUTO or ON) and the program
        switches to the sparse direct solver during a linear analysis, the sparse solver is used for the
        remainder of the simulation unless the solver choice is changed by issuing the :ref:`eqslv` command
        between load steps.

        **Nonlinear Analysis:** If the program switches to the sparse direct solver during a nonlinear
        analysis, the sparse solver
        is used for the remaining equilibrium iterations of the current substep. The program reverts back to
        the PCG solver at the end of the current substep unless one of the following conditions apply:

        * The previous call to the sparse solver involved an indefinite or near-singular matrix.

        * The last equilibrium iteration of the current substep using the sparse solver was faster than the
          last successful equilibrium iteration using the PCG solver.

        * Three consecutive fallback switches between the sparse and the PCG solvers have occurred.

        For both linear and nonlinear analyses, the solver choice can be changed using the :ref:`eqslv`
        command between any subsequent load steps.
        """
        command = f"PCGOPT,{lev_diff},{fallback},{reduceio},{strmck},{wrtfull},{lm_key}"
        return self.run(command, **kwargs)

    def perturb(
        self,
        type_: str = "",
        matkey: str = "",
        contkey: str = "",
        loadcontrol: str = "",
        **kwargs,
    ):
        r"""Sets linear perturbation analysis options.

        Mechanical APDL Command: `PERTURB <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PERTURB.html>`_

        **Command default:**

        .. _PERTURB_default:

        Linear perturbation analysis is disabled ( ``Type`` = OFF) by default. When the linear perturbation
        analysis is enabled, linear material property behavior is assumed for stress calculations; contact
        status for all contact pairs from the point of restart is used by default; and all loads and
        constraints from the restart step are deleted, except for displacement constraints and inertia
        loads, by default.

        Parameters
        ----------
        type_ : str
            Type of linear perturbation analysis to be performed:

            * ``STATIC`` - Perform a linear perturbation static analysis.

            * ``MODAL`` - Perform a linear perturbation modal analysis.

            * ``BUCKLE`` - Perform a linear perturbation eigenvalue buckling analysis.

            * ``HARMONIC`` - Perform a linear perturbation full harmonic analysis.

            * ``SUBSTR`` - Perform a linear perturbation substructure generation pass.

            * ``OFF`` - Do not perform a linear perturbation analysis (default).

        matkey : str
            Key for specifying how the linear perturbation analysis uses material properties, valid for all
            structural elements except contact elements. For more information, see `Linear Perturbation Analysis <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thylinpert.html#anplpdown>`_

            * ``AUTO`` - The program selects the material properties for the linear perturbation analysis automatically
              (default). The materials are handled in the following way:

              * For pure linear elastic materials used in the base analysis, the same properties are used in the
                linear perturbation analysis.

              * For hyperelastic materials used in the base analysis, the material properties are assumed to be
                linear elastic in the linear perturbation analysis. The material property data (or material
                Jacobian) is obtained based on the tangent of the hyperelastic material's constitutive law at the
                point where restart occurs.

              * For hyperviscoelastic materials used in the base analysis, the program uses the harmonic material
                formulation in perturbed full harmonic solutions.

              * For other nonlinear materials used in the base analysis, the material properties are assumed to be
                linear elastic in the linear perturbation analysis. The material data is the same as the linear
                portion of the nonlinear materials (that is, the parts defined via :ref:`mp` commands).

              * For ``COMBIN39``, the stiffness is that of the first segment of the force-deflection curve.

            * ``TANGENT`` - Use the tangent (material Jacobian) on the material constitutive curve as the material property. The
              material property remains linear in the linear perturbation analysis and is obtained at the point of
              the base analysis where restart occurs. The materials are handled in the following way:

              * For pure linear elastic materials used in the base analysis, the same properties are used in the
                linear perturbation analysis. Because the material constitutive curve is linear, the tangent is
                the same as the base analysis.

              * For hyperelastic materials used in the base analysis, the program uses the same tangent as that
                used for ``MatKey`` = AUTO, and the results are therefore identical.

              * For hyperviscoelastic materials used in the base analysis, the program uses the harmonic material
                formulation in perturbed full harmonic solutions.

              * For other nonlinear materials used in the base analysis, the material properties are assumed to be
                linear elastic in the linear perturbation analysis. The material data is the same as the linear
                portion of the nonlinear materials (that is, the parts defined via :ref:`mp` commands).

              The materials and properties typically differ from ``Matkey`` = AUTO, but it is possible the results
                could be identical or very similar if a.) the material is elastoplastic rate-independent and is
                unloading (or has neutral loading) at the restart point, or b.) the material is rate-dependent,
                depending on the material properties and loading conditions.

              * For ``COMBIN39``, the stiffness is equal to the tangent of the current segment of the force-
                deflection curve.

              * In a modal restart solution that follows a linear perturbation modal analysis, the TANGENT option
                is overridden by the AUTO option and linear material properties are used for stress calculations
                in the modal restart. See the :ref:`discussion in the Notes for more information. <TANmodrest>`

            * ``SPOFF`` - Provide the same values as AUTO, but set the spin softening matrix to zero (ignoring
              the spin softening effect).

              The spin softening effect is excluded in all the linear perturbation analysis types except for
              linear perturbation buckling. Note that although the spin softening effect is excluded in linear
              perturbation analysis, it is still included in the base static or full transient analysis if
              :ref:`nlgeom`,ON is issued in the base analysis.

        contkey : str
            Key that controls contact status for the linear perturbation analysis. This key controls all contact
            elements ( ``TARGE169``, ``TARGE170``, ``CONTA172``, ``CONTA174``, ``CONTA175``, ``CONTA177``, and
            ``CONTA178`` ) globally for all contact pairs. Alternatively, contact status can be controlled
            locally per contact pair by using the :ref:`cnkmod` command. Note that the contact status from the base analysis solution is always adjusted by the local contact controls specified by :ref:`cnkmod` first and then modified by the global sticking or bonded control ( ``ContKey`` = STICKING or BONDED). The tables in the `Notes <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cmd/Hlp_C_PERTURB.html#>`_ Notes section show how the contact status is adjusted by :ref:`cnkmod` and/or the ``ContKey`` setting.

            * ``CURRENT`` - Use the current contact status from the restart snapshot (default). If the previous
              run is nonlinear, then the nonlinear contact status at the point of restart is frozen and used
              throughout the linear perturbation analysis.

            * ``STICKING`` - For frictional contact pairs (MU > 0), use sticking contact (for example, MU\*KN for
              tangential contact stiffness) everywhere the contact state is closed (that is, status is sticking or
              sliding). This option only applies to contact pairs that are in contact and have a frictional
              coefficient MU greater than zero. Contact pairs without friction (MU = 0) and in a sliding state
              remain free to slide in the linear perturbation analysis.

            * ``BONDED`` - Any contact pairs that are in the closed (sticking or sliding) state are moved to
              bonded (for example, KN for both normal and tangential contact stiffness). Contact pairs that have a
              status of far-field or near-field remain open.

        loadcontrol : str
            Key that controls how the load vector of {F:sub:`perturbed` } is calculated. This control is provided for convenience of load generation for linear perturbation analysis. In general, a new set of loads is required for a linear perturbation analysis. This key controls all mechanical loads; it does not affect non-mechanical loads. Non-mechanical loads (including thermal loads) are always kept (that is, not deleted).

            * ``ALLKEEP`` - Keep all the boundary conditions (loads and constraints) from the end of the load
              step of the current restart point. This option is convenient for further load application and is
              useful for a linear perturbation analysis restarted from a previous linear analysis. For this
              option, {F:sub:`end` } is the total load vector at the end of the load step at the restart point.

            * ``INERKEEP`` - Delete all loads and constraints from the restart step, except for displacement
              constraints and inertia loads (default). All displacement constraints and inertia loads are kept for
              convenience when performing the linear perturbation analysis. Note that nonzero and tabular
              displacement constraints can be considered as external loads; however, they are not deleted when
              using this option.

            * ``PARKEEP`` - Delete all loads and constraints from the restart step, except for displacement
              constraints. All displacement constraints are kept for convenience when performing the linear
              perturbation analysis. Note that nonzero and tabular displacement constraints can be considered as
              external loads; however, they are not deleted when using this option.

            * ``DZEROKEEP`` - Behaves the same as the PARKEEP option, except that all nonzero displacement
              constraints are set to zero upon the onset of linear perturbation.

            * ``NOKEEP`` - Delete all the loads and constraints, including all displacement constraints. For
              this option, {F:sub:`end` } is zero unless non-mechanical loads (for example, thermal loads) are
              present.

        Notes
        -----

        .. _PERTURB_notes:

        This command controls options relating to `linear perturbation analyses
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/strlinpertother.html>`_. It must be
        issued in the first phase of a linear perturbation analysis.

        This command is also valid in PREP7.

        A linear perturbation analysis consists of two phases (two :ref:`solve` commands). The first phase
        is a restart from a base analysis. This base analysis must be a linear or nonlinear static analysis
        or full transient analysis. The first phase starts with the :ref:`antype`,,RESTART,,,PERTURB
        command and ends with the :ref:`solve`,ELFORM command. The purpose of the first phase is to re-
        establish a snapshot of the stiffness matrices at the specified restart point. The second phase,
        ending with the second :ref:`solve` command, is for the actual linear perturbation analysis.

        The total perturbed loads are calculated as follows:

        {F:sub:`perturbed` } = {F:sub:`end` } + {F:sub:`add` }

        where:

        * {F :sub:`end` } = total loads at the end of the load step of the current restart point (load
          applications are read from the :file:`.LDHI` file). By default, all of the loads in {F :sub:`end`
          } are deleted except for displacement boundary conditions and inertia loads (see the description
          of ``LoadControl`` above).
        * {F :sub:`add` } = Additional (new) loads prescribed by the user in the second phase of the linear
          perturbation analysis (after the first :ref:`solve` command is invoked).

        In the first phase of a linear perturbation analysis, the :ref:`antype`,,RESTART command resumes the
        :file:`Jobname.RDB` database and reads in the :file:`.LDHI` file to establish the {F:sub:`end` }
        load. New load application (adding to {F:sub:`add` }) or load removal (changing {F:sub:`end` }) can
        be done only in the second phase of the linear perturbation analysis (after the first :ref:`solve`
        command), allowing flexibility in controlling the final {F:sub:`perturbed` } to be used.

        For ``Type`` = STATIC, {F:sub:`perturbed` } is the actual external load for the static analysis.

        For ``Type`` = MODAL, {F:sub:`perturbed` } is calculated and stored in the :file:`.FULL` and
        :file:`.MODE` files for a subsequent mode-superposition, PSD, or other type of modal-based linear
        dynamic analysis. Linear dynamic options such as multiple load generations ( :ref:`modcont`,ON),
        enforced motion ( :ref:`modcont`,,ON), and residual vector methods ( :ref:`resvec`,ON) can be used
        in a linear perturbation analysis. For these methods, the :ref:`modcont` or :ref:`resvec` command
        must be invoked in the second phase (after the first :ref:`solve` ) of the linear perturbation
        procedure. For the enforced motion method, the base identification number should be specified (
        :ref:`d` command) in the second phase of the linear perturbation analysis. This base identification
        number is used later in the downstream mode-superposition or other mode-superposition based
        analysis.

        For ``Type`` = BUCKLE, {F:sub:`perturbed` } is the actual linear buckling load which is used to
        generate the linear stress stiffening matrix for the buckling analysis.

        For ``Type`` = HARMONIC, {F:sub:`perturbed` } is the actual external load for the full harmonic
        analysis. In this case, {F:sub:`perturbed` } can be frequency dependent and can use complex input.

        For ``Type`` = SUBSTR, {F:sub:`perturbed` } is used to generate the first reduced external load
        vector of the substructure.

        In most cases involving linear perturbation analysis, ``Matkey`` = AUTO is the best option for
        controlling material behavior. ``Matkey`` = TANGENT is often the better option, however, in special
        cases such as the following:

        * A linear perturbation buckling analysis, to introduce preferred buckling modes into a subsequent
          post-buckling nonlinear analysis.

        * A linear perturbation modal analysis, to introduce preferred modes into a subsequent bifurcation
          analysis.

        If the TANGENT option is used in conjunction with a modal restart solution that follows a linear
        perturbation modal analysis, then the AUTO option is assumed and linear material properties are used
        for stress calculations in the modal restart solution. This occurs because the TANGENT material
        properties are not available during the modal restart phase due to a data architecture limitation.
        Furthermore, linear material properties are used for the stress calculation in any downstream
        analysis that uses the modal restart solution.

        For more information about the automatic and tangent options, see in the `Element Reference
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_BIBLIO.html>`_.

        You can control the contact status for the linear perturbation analysis by using the ``ContKey``
        field on this command and/or the :ref:`cnkmod` command. The first table shows the effects of using
        only the ``ContKey`` setting on the :ref:`perturb` command. The second table shows the effects of
        using both the :ref:`cnkmod` command and the ``ContKey`` setting on :ref:`perturb`.

        Adjusted Contact Status when PERTURB Command Is Issued
        ******************************************************

        .. flat-table::

           * - :rspan:`1` **Contact Status from the Base Analysis Solution at the Restart Point**
             - **ContKeySetting on PERTURB Command**
           * - ``ContKey`` Value
             - Adjusted Contact Status
           * - 0 - far-field
             - any
             - 0 - far-field
           * - 1 - near-field
             - any
             - 1 - near-field
           * - :rspan:`1` 2 - sliding
             - CURRENT or STICKING (mu=0)
             - 2 - sliding
           * - STICKING (mu>0) or BONDED
             - 3 - sticking
           * - 3 - sticking
             - any
             - 3 - sticking

        Adjusted Contact Status when Both CNKMOD and PERTURB Are Issued
        ***************************************************************

        .. flat-table::

           * - :rspan:`1` **Contact Status from the Base Analysis Solution at the Restart Point**
             - *\*CNKMOD,** ``ITYPE`` ,12, ``Value``
             - **ContKeySetting on PERTURB Command**
           * - KEYOPT(12) Value
             - Adjusted Contact Status
             - ``ContKey`` Value
             - Final Adjusted Contact Status
           * - 0 - far-field
             - any
             - 0 - far-field
             - any
             - 0 - far-field
           * - :rspan:`5` 1 - near-field
             - 0, 1, 2, 3, 6
             - 1 - near-field
             - any
             - 1 - near-field
           * - :rspan:`2` 4
             - 1 - near-field (if outside of the adjusted pinball region)
             - any
             - 1 - near-field
           * - :rspan:`1` 2 - sliding (if inside of the adjusted pinball region)
             - CURRENT or STICKING (mu=0)
             - 2 - sliding
           * - STICKING (mu>0) or BONDED
             - 3 - sticking
           * - :rspan:`1` 5
             - 1 - near-field (if outside of the adjusted pinball region)
             - any
             - 1 - near-field
           * - 3 - sticking (if inside of the adjusted pinball region)
             - any
             - 3 - sticking
           * - :rspan:`2` 2 - sliding
             - :rspan:`1` 0, 2, 4
             - :rspan:`1` 2 - sliding
             - CURRENT or STICKING (mu=0)
             - 2 - sliding
           * - STICKING (mu>0) or BONDED
             - 3 - sticking
           * - 1, 3, 5, 6
             - 3 - sticking
             - any
             - 3 - sticking
           * - 3 - sticking
             - any
             - 3 - sticking
             - any
             - 3 - sticking

        When ``ContKey`` is set to CURRENT, all contact related parameters (such as normal stiffness and
        tangential stiffness) will remain unchanged throughout the linear perturbation analysis. However
        when ``ContKey`` is set to STICKING or BONDED, the program will re-evaluate the contact normal and
        tangential stiffness in order to perform the linear perturbation analysis based on the actual
        sticking behavior regardless of the friction coefficient value.

        Note that the :ref:`cnkmod` command allows you to take points in the base analysis that are near
        contact (within the pinball region) and modify them to be treated as "in contact" in the linear
        perturbation analysis; see the "1 - near-field" row in the above table with KEYOPT(12) values set to
        4 or 5. :ref:`cnkmod` also allows you to take points that are sliding in the base analysis and treat
        them as sticking in the linear perturbation analysis, irrespective of the MU value; see the "2 -
        sliding" row in the above table with KEYOPT(12) values set to 1,5, or 6.

        If an open gap exists at the restart point of the base static/transient solution and the contact
        status is adjusted as sliding or sticking due to a “bonded” or “no separation” contact behavior
        definition, then the program will treat it as near-field contact when executing the :ref:`cnkmod`
        command in a downstream linear perturbation analysis.
        """
        command = f"PERTURB,{type_},{matkey},{contkey},{loadcontrol}"
        return self.run(command, **kwargs)

    def pivcheck(self, key: str = "", prntcntrl: str = "", **kwargs):
        r"""Controls the behavior of an analysis when a negative or zero equation solver pivot value is
        encountered.

        Mechanical APDL Command: `PIVCHECK <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PIVCHECK.html>`_

        **Command default:**

        .. _PIVCHECK_default:

        The program checks for negative or zero pivot values ( ``Key`` = AUTO). If any are found, the
        analysis may stop with an error or may proceed with only a warning, depending on various criteria
        pertaining to the type of analysis being solved.

        Parameters
        ----------
        key : str
            Determines whether to stop or continue an analysis when a negative or zero equation solver pivot
            value is encountered:

            * ``AUTO`` - Check for negative or zero pivot values for analyses performed with the sparse and PCG
              solvers. When one is encountered, an error or warning is issued, per various criteria relating to
              the type of analysis being solved. An error causes the analysis to stop; a warning allows the
              analysis to continue. A negative pivot value may be valid for some nonlinear and multiphysics
              analyses (for example, electromagnetic and thermal analyses); this key has no effect in these cases.

            * ``ERROR`` - Check for negative or zero pivot values for analyses performed with the sparse and PCG
              solvers. When one is encountered, an error is issued, stopping the analysis. A negative pivot value
              may be valid for some nonlinear and multiphysics analyses (for example, electromagnetic and thermal
              analyses); this key has no effect in these cases.

            * ``WARN`` - Check for negative or zero pivot values for analyses performed with the sparse and PCG
              solvers. When one is encountered, a warning is issued and the analysis continues. A negative pivot
              value may be valid for some nonlinear and multiphysics analyses (for example, electromagnetic and
              thermal analyses); this key has no effect in these cases.

            * ``OFF`` - Pivot values are not checked. This key causes the analysis to continue in spite of a
              negative or zero pivot value.

        prntcntrl : str
            Provides print options. Print output with these options will be sent to the default output file, not
            to the files created by the nonlinear diagnostic tools ( :ref:`nldiag` ).

            * ``ONCE`` - Print only the maximum and minimum pivot information on the first call to the sparse
              solver (which is the default solver). This is the default behavior.

            * ``EVERY`` - Print the maximum and minimum pivot information at every call to the sparse solver.
              This option is provided for nonlinear analysis diagnostics.

        Notes
        -----

        .. _PIVCHECK_notes:

        This command is valid for all analyses. In a nonlinear analysis, a negative pivot may be valid. In
        some cases, rigid body motions in a nonlinear analysis will be trapped by error routines checking
        infinitely large displacements (DOF limit exceeded) or nonconvergence status. An under-constrained
        model may avoid the pivot check, but fail with a DOF limit exceeded error.

        Machine precision may affect whether a small pivot triggers an error or bypasses this checking
        logic. You may wish to review the ratio of the maximum to absolute minimum pivot values. For ratios
        exceeding 12 to 14 orders of magnitude, the accuracy of the computed solution may be degraded by the
        severe ill-conditioning of the assembled matrix.

        Note that negative pivots corresponding to Lagrange multiplier based mixed u-P elements are not
        checked or reported by this command. Negative pivots arising from the u-P element formulation and
        related analyses can occur and lead to correct solutions.

        This command is also valid in PREP7.
        """
        command = f"PIVCHECK,{key},{prntcntrl}"
        return self.run(command, **kwargs)

    def prscontrol(self, key: str = "", **kwargs):
        r"""Specifies whether to include pressure load stiffness in the element stiffness formation.

        Mechanical APDL Command: `PRSCONTROL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PRSCONTROL.html>`_

        Parameters
        ----------
        key : str
            Pressure load stiffness key. In general, use the default setting. Use a non-default setting only if
            you encounter convergence difficulties. Pressure load stiffness is automatically included when using
            eigenvalue buckling analyses ( :ref:`antype`,BUCKLE), equivalent to ``Key`` = INCP. For all other types of analyses, valid arguments for ``Key`` are:

            * ``NOPL`` - Pressure load stiffness not included for any elements.

            * ``(blank) (default)`` - Include pressure load stiffness for elements ``SURF153``, ``SURF154``,
              ``SURF156``, ``SURF159``, ``SHELL181``, ``PLANE182``, ``PLANE183``, ``SOLID185``, ``SOLID186``,
              ``SOLID187``, ``SOLSH190``, ``BEAM188``, ``BEAM189``, ``FOLLW201``, ``SHELL208``, ``SHELL209``,
              ``SOLID272``, ``SOLID273``, ``SHELL281``, ``SOLID285``, ``PIPE288``, ``PIPE289``, and ``ELBOW290``.

        Notes
        -----

        .. _PRSCONTROL_notes:

        This command is rarely needed. The default settings are recommended for most analyses.
        """
        command = f"PRSCONTROL,{key}"
        return self.run(command, **kwargs)

    def pscontrol(self, option: str = "", key: str = "", **kwargs):
        r"""Enables or disables shared-memory parallel operations.

        Mechanical APDL Command: `PSCONTROL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PSCONTROL.html>`_

        **Command default:**
        None. The command is ignored if issued with no arguments.

        Parameters
        ----------
        option : str
            Specify the operations for which you intend to enable/disable parallel behavior:

            * ``ALL`` - Enable/disable parallel for all areas (default).

            * ``PREP`` - Enable/disable parallel during preprocessing ( :ref:`prep7` ).

            * ``SOLU`` - Enable/disable parallel during solution ( :ref:`slashsolu` ).

            * ``FORM`` - Enable/disable parallel during element matrix generation.

            * ``SOLV`` - Enable/disable parallel during equation solver.

            * ``RESU`` - Enable/disable parallel during element results calculation.

            * ``POST`` - Enable/disable parallel during postprocessing ( :ref:`post1` and :ref:`post26` ).

            * ``STAT`` - List parallel operations that are enabled/disabled.

        key : str
            Option control key. Used for all ``Option`` values except STAT.

            * ``ON`` - Enable parallel operation.

            * ``OFF`` - Disable parallel operation.

        Notes
        -----
        Use this command in shared-memory parallel operations.

        This command is useful when you encounter minor discrepancies in a nonlinear solution when using
        different numbers of processors. A parallel operation applied to the element matrix generation can
        produce a different nonlinear solution with a different number of processors. Although the nonlinear
        solution converges to the same nonlinear tolerance, the minor discrepancy created may not be
        desirable for consistency.

        Enabling/disabling parallel behavior for the solution ( ``Option`` = SOLU) supersedes the
        activation/deactivation of parallel behavior for element matrix generation (FORM), equation solver
        (SOLV), and element results calculation (RESU).

        The SOLV option supports only the sparse direct and PCG solvers ( :ref:`eqslv`,SPARSE or PCG). No
        other solvers are supported.

        This command applies only to shared-memory architecture. It does not apply to distributed-memory
        parallel processing.
        """
        command = f"PSCONTROL,{option},{key}"
        return self.run(command, **kwargs)

    def psolve(self, lab: str = "", **kwargs):
        r"""Directs the program to perform a partial solution.

        Mechanical APDL Command: `PSOLVE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PSOLVE.html>`_

        Parameters
        ----------
        lab : str
            Valid labels defining the solution step. All characters are required:

            * ``EIGDAMP`` - Calculates the eigenvalues and eigenvectors using the damped eigensolver. Requires
              :file:`Jobname.FULL` from :ref:`modopt`,UNSYM or :ref:`modopt`,DAMP options. Produces
              :file:`JobnameMODE`.

            * ``EIGQRDA`` - Calculates eigenvalues and eigenvectors using the QR damped eigensolver. Requires
              :file:`Jobname.EMAT` from :ref:`modopt`,QRDAMP option. Produces :file:`JobnameMODE`.

            * ``EIGEXP`` - Expands the eigenvector solution. Requires :file:`Jobname.ESAV` and
              :file:`Jobname.MODE`. Produces :file:`JobnameRST`.

            * ``EIGLANB`` - Calculates the eigenvalues and eigenvectors using Block Lanczos. Requires
              :file:`Jobname.EMAT` from :ref:`modopt`,LANB option. Produces :file:`JobnameMODE`.

            * ``EIGLANPCG`` - Calculates the eigenvalues and eigenvectors using PCG Lanczos. Requires
              :file:`Jobname.EMAT` from :ref:`modopt`,LANPCG option. Produces :file:`JobnameMODE`.

            * ``EIGSNODE`` - Calculates the eigenvalues and eigenvectors using the Supernode method. Requires
              :file:`Jobname.EMAT` from :ref:`modopt`,SNODE option. Produces :file:`Jobname.MODE`. (See the
              :ref:`modopt` command for more information on the SNODE modal solver.)

            * ``EIGUNSYM`` - Calculates the eigenvalues and eigenvectors using the unsymmetric eigensolver.
              Requires :file:`Jobname.EMAT` from :ref:`modopt`,UNSYM or :ref:`modopt`,DAMP options. Produces
              :file:`JobnameMODE`.

            * ``ELFORM`` - Creates the element matrices. Produces :file:`Jobname.EMAT` and :file:`JobnameESAV`.
              If you want to include prestress effects ( :ref:`pstres`,ON) from a previous prestress analysis, the
              ELFORM option requires the :file:`Jobname.EMAT` and :file:`Jobname.ESAV` files generated by that
              analysis.

        Notes
        -----

        .. _PSOLVE_notes:

        Directs the program to perform a partial solution (that is, one step of an analysis sequence).
        Predefined analysis types ( :ref:`antype` ) perform a defined subset of these solution steps in a
        predefined sequence. You can use the partial-solution procedure to repeat a certain step of an
        analysis or to restart an analysis.

        Not all steps are valid for all analysis types. The order of the steps may vary depending on the
        result you desire. See the `Basic Analysis Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/Hlp_G_BAS19.html>`_ for a
        description of how to perform partial and predefined
        solutions.

        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.

        In a cyclic symmetry analysis, :ref:`psolve`,EIGLANB or :ref:`psolve`,EIGLANPCG performs the modal
        analysis at multiple load steps, one for each nodal-diameter specified via the :ref:`cycopt`
        command. In addition, the eigenvector solution is expanded at each nodal-diameter solution,
        eliminating the need for a separate expansion pass ( :ref:`psolve`,EIGEXP).

        If :file:`Jobname.EMAT` is required, run the prior analysis with :ref:`ematwrite`,YES to ensure that
        a :file:`Jobname.EMAT` is generated.

        Distributed-Memory Parallel (DMP) Restriction Only the EIGLANB, and EIGLANPCG options on this
        command are supported in a DMP solution.

        .. warning::

            This command is archived in the latest version of the software.

        """
        command = f"PSOLVE,{lab}"
        return self.run(command, **kwargs)

    def rate(self, option: str = "", **kwargs):
        r"""Specifies whether the effect of creep strain rate will be used in the solution of a load step.

        Mechanical APDL Command: `RATE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_RATE.html>`_

        Parameters
        ----------
        option : str
            Activates implicit creep analysis.

            * ``0 or OFF`` - No implicit creep analysis. This option is the default.

            * ``1 or ON`` - Perform implicit creep analysis.

        Notes
        -----

        .. _RATE_notes:

        Set ``Option`` = 1 (or ON) to perform an implicit creep analysis ( :ref:`tb`,CREEP with ``TBOPT``
        :math:`equation not available`  1). For viscoplasticity/creep analysis,  ``Option`` specifies
        whether or not to include the creep calculation in the solution of a load step. If ``Option`` = 1
        (or ON), the program performs the creep calculation. Set an appropriate time for solving the load
        step via a :ref:`time`, ``TIME`` command.

        **Product Restrictions**

        .. _RATE_extranote1:

        This command works only when modeling implicit creep with either von Mises or Hill potentials.

        When modeling implicit creep with von Mises potential, you can use the following elements:
        ``LINK180``, ``SHELL181``, ``PLANE182``, ``PLANE183``, ``SOLID185``, ``SOLID186``, ``SOLID187``,
        ``SOLID272``, ``SOLID273``, ``SOLID285``, ``SOLSH190``, ``BEAM188``, ``BEAM189``, ``SHELL208``,
        ``SHELL209``, ``REINF264``, ``SHELL281``, and ``ELBOW290``.

        When modeling anisotropic creep ( :ref:`tb`,CREEP with :ref:`tb`,HILL), you can also use the
        following elements: ``LINK180``, ``SHELL181``, ``PLANE182``, ``PLANE183``, ``SOLID185``,
        ``SOLID186``, ``SOLID187``, ``BEAM188``, ``BEAM189``, ``SOLSH190``, ``SHELL208``, ``SHELL209``,
        ``REINF264``, ``REINF265``, ``SOLID272``, ``SOLID273``, ``SHELL281``, ``SOLID285``, ``PIPE288``,
        ``PIPE289``, and ``ELBOW290``.
        """
        command = f"RATE,{option}"
        return self.run(command, **kwargs)

    def resvec(self, keyvect: str = "", keyresp: str = "", **kwargs):
        r"""Calculates or includes residual vectors or residual responses

        Mechanical APDL Command: `RESVEC <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_RESVEC.html>`_

        **Command default:**
        No residual quantities are calculated or included in the analysis.

        Parameters
        ----------
        keyvect : str
            Residual vector key:

            * ``OFF`` - Do not calculate or include residual vectors (default).

            * ``ON`` - Calculate or include residual vectors.

        keyresp : str
            Residual response key:

            * ``OFF`` - Do not calculate or include residual responses (default).

            * ``ON`` - Calculate or include residual responses.

        Notes
        -----
        In a `modal analysis
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STR_SMSUP.html>`_, the
        :ref:`resvec` command calculates residual vectors (or responses). In a `mode-superposition transient
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STR5_10.html#a4iQxq2c8mcm>`_,
        `mode-superposition harmonic
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STR4_MODESUPER.html#aMhQxq6emcm>`_,
        PSD or `spectrum
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STR6_2.html#>`_ analysis, the
        command includes residual vectors. The command must be issued during the first modal solve.

        In the expansion pass of a mode-superposition transient or mode-superposition harmonic analysis, the
        command includes residual responses.

        In a component mode synthesis (CMS) `generation pass
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_substr/advcmssuperelem.html#usingcms_elemcalc>`_,
        the :ref:`resvec` command calculates one residual vector which is included in the normal modes basis
        used in the transformation matrix. It is supported for the three available `CMS methods
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_anproc6.html#eq39b62ffb-3890-471d-a79e-2d6096214d0b>`_.
        :ref:`resvec`,ON can only be specified in the first load step of a generation pass and is ignored if
        issued at another load step.

        If rigid-body modes exist, pseudo-constraints are required for the calculation. Issue the
        :ref:`d`,,,SUPPORT command to specify only the minimum number of pseudo-constraints necessary to
        prevent rigid-body motion.

        Both residual vector and residual response approaches cannot be used in the same analysis.

        For more information about residual vector or residual response formulation, see `Residual Vector
        Method <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_tool9.html#resvec_125>`_
        `Residual Response Method
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_tool9.html#thy_antools_resresp_eqn2>`_
        """
        command = f"RESVEC,{keyvect},,,,{keyresp}"
        return self.run(command, **kwargs)

    def rstoff(self, lab: str = "", offset: str = "", **kwargs):
        r"""Offsets node or element IDs in the FE geometry record.

        Mechanical APDL Command: `RSTOFF <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_RSTOFF.html>`_

        **Command default:**

        .. _RSTOFF_default:

        Issuing the :ref:`rstoff` command with no specified argument values applies no offsets.

        Parameters
        ----------
        lab : str
            The offset type:

            * ``NODE`` - Offset the node IDs.

            * ``ELEM`` - Offset the element IDs.

        offset : str
            A positive integer value specifying the offset value to apply. The value must be greater than
            the number of nodes or elements in the existing superelement results file.

        Notes
        -----
        The :ref:`rstoff` command offsets node or element IDs in the FE geometry record saved in the
        :file:`.rst` results file. Use the command when expanding superelements in a bottom-up
        substructuring analysis (where each superelement is generated individually in a `generation pass
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_substr/advcmssuperelem.html#usingcms_elemcalc>`_,
        and all superelements are assembled together in the `use pass
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_substr/an9Auq1d6ldm.html#advobsl5jla062999>`_
        ).

        With appropriate offsets, you can write results files with unique node or element IDs and thus
        display the entire model even if the original superelements have overlapping element or node ID
        sets. (Such results files are incompatible with the :file:`.db` database file saved at the
        generation pass.)

        The offset that you specify is based on the original superelement node or element numbering, rather
        than on any offset specified via a :ref:`sesymm` or :ref:`setran` command. When issuing an
        :ref:`rstoff` command, avoid specifying an offset that creates conflicting node or element numbers
        for a superelement generated via a :ref:`sesymm` or :ref:`setran` command.

        If you issue the command to set non-zero offsets for node or element IDs, you must bring the
        geometry into the database via the :ref:`set` command so that Mechanical APDL can display the
        results.
        Specify appropriate offsets to avoid overlapping node or element IDs with other superelement results
        files.

        The command is valid only in the first load step of a `superelement expansion pass
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_substr/axcAuq367ldm.html#adv5note4jla062999>`_.


        """
        command = f"RSTOFF,{lab},{offset}"
        return self.run(command, **kwargs)

    def scopt(self, tempdepkey: str = "", mappingkey: str = "", **kwargs):
        r"""Specifies System Coupling options.

        Mechanical APDL Command: `SCOPT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SCOPT.html>`_

        Parameters
        ----------
        tempdepkey : str
            Temperature-dependent behavior key based on the convection coefficient:

            * ``YES`` - A negative convection coefficient, - ``N``, is assumed to be a function of temperature
              and is determined from the HF property table for material ``N`` ( :ref:`mp` command). This is the
              default behavior.

            * ``NO`` - A negative convection coefficient, - ``N``, is used as is in the convection calculation.

        mappingkey : str
            Controls whether midside nodes of higher-order elements are used for mapping on System Coupling
            interfaces:

            * ``YES`` - Both corner and midside nodes are used (default).

            * ``NO`` - Only corner nodes are used.

        Notes
        -----

        .. _SCOPT_notes:

        By default in the Mechanical APDL program, a negative convection coefficient value triggers
        temperature-
        dependent behavior. In some one-way CFD to Mechanical APDL thermal simulations, it is desirable to
        allow
        convection coefficients to be used as negative values. To do so, issue the command :ref:`scopt`,NO.
        """
        command = f"SCOPT,{tempdepkey},{mappingkey}"
        return self.run(command, **kwargs)

    def seexp(
        self,
        sename: str = "",
        usefil: str = "",
        imagky: str = "",
        expopt: str = "",
        **kwargs,
    ):
        r"""Specifies options for the substructure expansion pass.

        Mechanical APDL Command: `SEEXP <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SEEXP.html>`_

        Parameters
        ----------
        sename : str
            The name (case-sensitive) of the superelement matrix file created by the substructure generation
            pass ( :file:`Sename.SUB` ). Defaults to the initial jobname :file:`File`. If a number, it is
            the element number of the superelement as used in the use pass.

        usefil : str
            The name of the file containing the superelement degree-of-freedom (DOF) solution created by the
            substructure use pass ( :file:`Usefil.DSUB` ).

        imagky : str
            Key to specify use of the imaginary component of the DOF solution. Applicable only if the use pass
            is a harmonic ( :ref:`antype`,HARMIC) analysis:

            * ``OFF`` - Use real component of DOF solution (default).

            * ``ON`` - Use imaginary component of DOF solution.

             If all solutions are to be expanded ( :ref:`numexp`,ALL), ``Imagky`` is ignored and both the real
            and imaginary solutions are expanded.

        expopt : str
            Key to specify whether the superelement ( :ref:`antype` ,SUBSTR) expansion pass ( :ref:`expass`,ON) should transform the geometry:

            * ``OFF`` - Do not transform node or element locations (default).

            * ``ON`` - Transform node or element locations in the FE geometry record of the :file:`.rst` results
              file.

        Notes
        -----

        .. _SEEXP_notes:

        Specifies options for the expansion pass of the substructure analysis ( :ref:`antype`,SUBSTR). If
        used in SOLUTION, this command is valid only within the first load step.

        If you specify geometry transformation ( ``Expopt`` = ON), you must retrieve the transformation
        matrix (if it exists) from the specified :file:`.SUB` file. The command updates the nodal X, Y, and
        Z coordinates to represent the transformed node locations. The ``Expopt`` option is useful when you
        want to expand superelements created from other superelements (via :ref:`setran` or :ref:`sesymm`
        commands). For more information, see and.


        This command is also valid in :ref:`prep7`.
        """
        command = f"SEEXP,{sename},{usefil},{imagky},{expopt}"
        return self.run(command, **kwargs)

    def seopt(
        self,
        sename: str = "",
        sematr: int | str = "",
        sepr: int | str = "",
        sesst: int | str = "",
        expmth: str = "",
        seoclvl: str = "",
        lpnamekey: str = "",
        **kwargs,
    ):
        r"""Specifies substructure analysis options.

        Mechanical APDL Command: `SEOPT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SEOPT.html>`_

        Parameters
        ----------
        sename : str
            The name (case-sensitive, 32-character maximum) assigned to the :file:`.sub` superelement matrix
            file. This field defaults to ``Fname`` on the :ref:`filname` command.

        sematr : int or str
            Matrix generation key:

            * ``1`` - Generate stiffness (or conductivity) matrix (default).

            * ``2`` - Generate stiffness and mass (or conductivity and specific heat) matrices.

            * ``3`` - Generate stiffness, mass and damping matrices.

        sepr : int or str
            Print key:

            * ``0`` - Do not print superelement matrices or load vectors.

            * ``1`` - Print both load vectors and superelement matrices.

            * ``2`` - Print load vectors but not matrices.

        sesst : int or str
            Stress-stiffening key:

            * ``0`` - Do not save space for stress stiffening in a later run.

            * ``1`` - Save space for the stress stiffening matrix (calculated in a subsequent generation run
              after the expansion pass).

        expmth : str
            Expansion method for expansion pass:

            * ``BACKSUB`` - Save necessary factorized matrix files (for example, the :file:`.LN22` file) for
              backsubstitution during the subsequent expansion passes (default). This normally results in a large
              usage of disk space.

            * ``MODDIR`` - This is the same expansion method as BACKSUB, except that the static correction
              vectors (see the first term of in the `Mechanical APDL Theory Reference <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_biblio.html>`_) are stored on the :file:`.bclv` file instead of
              the :file:`.LN22` file. This option is required when remote read-only file usage is used during the
              first solution of the first restart of a generation pass (see the :ref:`moddir` command).

            * ``RESOLVE`` - Do not save factorized matrix files. Global stiffness matrix will be reformed during
              expansion pass. This option provides an effective way to save disk space usage. This option cannot
              be used if the use pass uses large deflections ( :ref:`nlgeom`,ON).

            * ``NONE`` - Do not save factorized matrix files. With this option, the expansion pass is not
              possible when factorized matrix files are required.

            * ``BCLV`` - Do not save factorized matrix files. The static correction vectors (see the first term
              of ) are stored in the :file:`.bclv` file. With this option, the expansion pass is not possible when
              factorized matrix files are required.

        seoclvl : str
            For the added-mass calculation, the ocean level to use when ocean waves ( :ref:`octype`,,WAVE) are present:

            * ``ATP`` - The ocean level at this point in time (default).

            * ``MSL`` - The mean ocean level.

        lpnamekey : str

            * ``ON`` - All files created during the generation pass are named using ``Sename``.

            * ``OFF`` - All files created during the generation pass are named using the :file:`Jobname` defined
              for the analysis (see :ref:`filname` command) except for the :file:`.sub` file, which uses
              ``Sename`` if specified (default).

        Notes
        -----

        .. _SEOPT_notes:

        :ref:`seopt` specifies substructure analysis options ( :ref:`antype`,SUBSTR). If used during
        solution, the command is valid only within the first load step.

        When ocean waves ( :ref:`octype`,,WAVE) are present, the ``SeOcLvL`` argument specifies the ocean
        height or level to use for the added-mass calculation, as the use-run analysis type is unknown
        during the generation run.

        The expansion pass method RESOLVE is not supported with component mode synthesis analysis (
        :ref:`cmsopt` ). ``ExpMth`` is automatically set to BACKSUB for CMS analysis. The RESOLVE method
        invalidates the use of the :ref:`numexp` command. The RESOLVE method does not allow the restarting
        of the substructure generation pass and the computation of results based on nodal velocity and nodal
        acceleration (damping force, inertial force, kinetic energy, etc.) in the substructure expansion
        pass.

        If ``ExpMth`` = NONE or BCLV in a substructure analysis or component mode synthesis (CMS) analysis (
        :ref:`cmsopt` ) using the fixed-interface ( :ref:`cmsopt`,FIX) or free-interface ( :ref:`cmsopt`
        ,FREE) methods, you cannot restart the generation pass or perform the expansion pass. (In CMS
        analyses using those methods, however, the expansion pass is possible when element-results
        calculation is activated in the generation pass ( ``ELCALC`` = YES on :ref:`cmsopt` )). The
        ``ExpMth`` argument is not required for CMS analysis using the residual-flexible free-interface
        method ( :ref:`cmsopt`,RFFB).

        For linear perturbation substructure generation pass with multiple substructures, set ``LPnameKey``
        = ON to avoid copying files at the end of each generation pass with the :ref:`copy` command. For an
        example with CMS analysis using the fixed-interface method, see.

        This command is also valid in PREP7.
        """
        command = (
            f"SEOPT,{sename},{sematr},{sepr},{sesst},{expmth},{seoclvl},,{lpnamekey}"
        )
        return self.run(command, **kwargs)

    def snoption(
        self,
        rangefact: str = "",
        blocksize: str = "",
        robustlev: str = "",
        compute: str = "",
        solve_info: str = "",
        **kwargs,
    ):
        r"""Specifies Supernode (SNODE) eigensolver options.

        Mechanical APDL Command: `SNOPTION <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SNOPTION.html>`_

        **Command default:**

        .. _SNOPTION_default:

        ``RangeFact`` = 2.0. ``BlockSize`` is set to min( ``NMODE``,40), where ``NMODE`` is the number of
        modes to be computed as set on the :ref:`modopt` command. ``RobustLev`` = 0. ``Compute`` = BOTH.
        Additional output is not printed ( ``Solve_Info`` = OFF).

        Parameters
        ----------
        rangefact : str
            Factor used to control the range of eigenvalues computed for each supernode. The value of ``RangeFact`` must be a number between 1.0 and 10.0. By default the ``RangeFact`` value is set to 2.0, which means that all eigenvalues between 0 and 2\* ``FREQE`` are computed for each supernode (where ``FREQE`` is the upper end of the frequency range of interest as specified on the :ref:`modopt` command). As the ``RangeFact`` value increases, the eigensolution for the SNODE solver becomes more accurate and the computational time increases.

        blocksize : str
            ``BlockSize`` to be used when computing the final eigenvectors. The value of ``Blocksize`` must
            be either MAX or a number between 1 and ``NMODE``, where ``NMODE`` is the number of modes to be
            computed as set on the :ref:`modopt` command. Input a value of MAX to force the algorithm to
            allocate enough memory to hold all of the final eigenvectors in memory and, therefore, only read
            through the file containing the supernode eigenvectors once. Note that this setting is ONLY
            recommended when there is sufficient physical memory on the machine to safely hold all of the
            final eigenvectors in memory.

        robustlev : str
            Parameter used to control the robustness of the SNODE eigensolver. The value of ``RobustLev``
            must be a number between 0 and 10. Lower values of ``RobustLev`` allow the eigensolver to run in
            the most efficient manner for optimal performance. Higher values of ``RobustLev`` often slow
            down the performance of the eigensolver, but can increase the robustness; this may be desirable
            if a problem is detected with the eigensolver or its eigensolution.

        compute : str
            Key to control which computations are performed by the Supernode eigensolver:

            * ``EVALUE`` - The eigensolver computes only the eigenvalues.

            * ``EVECTOR`` - The eigensolver computes only the eigenvectors (must be preceded by a modal analysis
              where the eigenvalues were computed using the Supernode eigensolver).

            * ``BOTH`` - The eigensolver computes both the eigenvalues and eigenvectors in the same pass
              (default).

        solve_info : str
            Solver output option:

            * ``OFF`` - Turns off additional output printing from the Supernode eigensolver (default).

            * ``PERFORMANCE`` - Turns on additional output printing from the Supernode eigensolver, including a
              performance summary and a summary of file I/O for the Supernode eigensolver. Information on memory
              usage during assembly of the global matrices (that is, creation of the :file:`Jobname.FULL` file) is
              also printed with this option.

        Notes
        -----

        .. _SNOPTION_notes:

        This command specifies options for the Supernode (SNODE) eigensolver.

        Setting ``RangeFact`` to a value between 2.0 and 10.0 will improve the accuracy of the computed
        eigenvalues and eigenvectors, but will often increase the computing time of the SNODE eigensolver.
        Conversely, setting ``RangeFact`` to a value less than 2.0 will deteriorate the accuracy of the
        computed eigenvalues and eigenvectors, but will often speed up the computing time of the SNODE
        eigensolver. The default value of 2.0 has been set as a good blend of accuracy and performance. If
        the model has rigid body modes, setting ``RangeFact`` higher than 2 is recommended to achieve better
        solution accuracy for the lower flexible modes.

        The SNODE eigensolver reads the eigenvectors and related information for each supernode from a file
        and uses that information to compute the final eigenvectors. For each eigenvalue/eigenvector
        requested by the user, the program must do one pass through the entire file that contains the
        supernode eigenvectors. By choosing a ``BlockSize`` value greater than 1, the program can compute
        ``BlockSize`` number of final eigenvectors for each pass through the file. Therefore, smaller values
        of ``BlockSize`` result in more I/O, and larger values of ``BlockSize`` result in less I/O. Larger
        values of ``BlockSize`` also result in significant additional memory usage, as ``BlockSize`` number
        of final eigenvectors must be stored in memory. The default ``Blocksize`` of min( ``NMODE``,40) is
        normally a good choice to balance memory and I/O usage.

        The ``RobustLev`` field should only be used when a problem is detected with the accuracy of the
        final solution or if the Supernode eigensolver fails while computing the eigenvalues/eigenvectors.
        Setting ``RobustLev`` to a value greater than 0 will cause the performance of the eigensolver to
        deteriorate. If the performance deteriorates too much or if the eigensolver continues to fail when
        setting the ``RobustLev`` field to higher values, then switching to another eigensolver such as
        Block Lanczos or PCG Lanczos is recommended.

        Setting ``Compute`` = EVALUE causes the Supernode eigensolver to compute only the requested
        eigenvalues. During this process a :file:`Jobname.SNODE` file is written; however, a
        :file:`Jobname.MODE` file is not written. Thus, errors will likely occur in any downstream
        computations that require the :file:`Jobname.MODE` file (for example, participation factor
        computations, mode superpostion transient/harmonic analysis, PSD analysis). Setting ``Compute`` =
        EVECTOR causes the Supernode eigensolver to compute only the corresponding eigenvectors. The
        :file:`Jobname.SNODE` file and the associated :file:`Jobname.FULL` file are required when requesting
        these eigenvectors. In other words, the eigenvalues must have already been computed for this model
        before computing the eigenvectors. This field can be useful in order to separate the two steps
        (computing eigenvalues and computing eigenvectors).

        For more information on the eigensolver's accuracy and a discussion of its known limitations, see in
        the `Mechanical APDL Theory Reference
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_biblio.html>`_
        """
        command = (
            f"SNOPTION,{rangefact},{blocksize},{robustlev},{compute},,{solve_info}"
        )
        return self.run(command, **kwargs)

    def solve(self, action: str = "", **kwargs):
        r"""Starts a solution.

        Mechanical APDL Command: `SOLVE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SOLVE.html>`_

        Parameters
        ----------
        action : str
            Action to be performed on solve (used only for linear perturbation analyses).

            * ``ELFORM`` - Reform all appropriate element matrices in the first phase of a linear perturbation
              analysis.

        Notes
        -----

        .. _SOLVE_notes:

        Starts the solution of one load step of a solution sequence based on the current analysis type and
        option settings. Use ``Action`` = ELFORM only in the first phase of a `linear perturbation analysis
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/strlinpertother.html>`_.
        """
        command = f"SOLVE,{action}"
        return self.run(command, **kwargs)

    def stabilize(
        self,
        key: str = "",
        method: str = "",
        value: str = "",
        substpopt: str = "",
        forcelimit: str = "",
        recalcdamp: str = "",
        **kwargs,
    ):
        r"""Activates stabilization for all elements that support nonlinear stabilization.

        Mechanical APDL Command: `STABILIZE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_STABILIZE.html>`_

        Parameters
        ----------
        key : str
            Key for controlling nonlinear stabilization:

            * ``OFF`` - Deactivate stabilization (default).

            * ``CONSTANT`` - Activate stabilization. The energy-dissipation ratio or damping factor remains
              constant during the load step.

            * ``REDUCE`` - Activate stabilization. The energy-dissipation ratio or damping factor is reduced
              linearly to zero at the end of the load step from the specified or calculated value.

        method : str
            The stabilization-control method:

            * ``ENERGY`` - Use the energy-dissipation ratio as the control. This value is the default when
              ``Key`` ≠ OFF.

            * ``DAMPING`` - Use the damping factor as the control.

        value : str
            The energy-dissipation ratio ( ``Method`` = ENERGY) or damping factor ( ``Method`` = DAMPING).
            This value must be greater than 0 when ``Method`` = ENERGY or ``Method`` = DAMPING. When
            ``Method`` = ENERGY, this value is usually a number between 0 and 1.

        substpopt : str
            Option for the first substep of the load step:

            * ``NO`` - Stabilization is not activated for the first substep even when it does not converge after
              the minimal allowed time increment is reached. This value is the default when ``Key`` ≠ OFF.

            * ``MINTIME`` - Stabilization is activated for the first substep if it still does not converge after
              the minimal allowed time increment is reached.

            * ``ANYTIME`` - Stabilization is activated for the first substep. Use this option if stabilization
              was active for the previous load step via ``Key`` = CONSTANT.

        forcelimit : str
            The stabilization force limit coefficient, such that 0 < ``FORCELIMIT`` < 1. The default value
            is 0.2. To omit a stabilization force check, set this value to 0.

        recalcdamp : str
            Key for controlling damping recalculation:

            * 0 - No recalculation of the damping factor (default).
            * 1 - Recalculate the damping factor for the energy-based stabilization-control method.

        Notes
        -----

        .. _STABILIZE_notes:

        Once issued, a :ref:`stabilize` command remains in effect until you reissue the command.

        For the energy dissipation ratio, specify ``VALUE`` = 1.0e-4 if you have no prior experience with
        the current model; if convergence problems are still an issue, increase the value gradually. The
        damping factor is mesh-, material-, and time-step-dependent; an initial reference value from the
        previous run (such as a run with the energy-dissipation ratio as input) should suggest itself.

        Exercise caution when specifying ``SubStpOpt`` = MINTIME or ANYTIME for the first load step;
        Ansys, Inc. recommends this option only for experienced users. If stabilization was active
        for the previous load step via ``Key`` = CONSTANT and convergence is an issue for the first substep,
        specify ``SubStpOpt`` = ANYTIME.

        When the L2-norm of the stabilization force (CSRSS value) exceeds the L2-norm of the internal force
        multiplied by the stabilization force coefficient, the program issues a message displaying both the
        stabilization force norm and the internal force norm. The ``FORCELIMIT`` argument enables you to
        change the default stabilization force coefficient (normally 20 percent).

        When using the energy-based stabilization-control method and ``RECALCDAMP`` = 1, the damping factor
        is recalculated in the following cases:

        * In an analysis `restart
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/Hlp_G_BAS3_12.html#bassolumodres>`_.

        * In a nonlinear adaptivity analysis in the substep following the remeshing substep.

        This command stabilizes the degrees of freedom for `current-technology elements
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/EL2oldnewtable.html#EL2curtechelembenefits>`_
        only. Other elements can be included in the FE model, but their degrees of freedom are not
        stabilized.

        For more information about nonlinear stabilization, see `Unstable Structures
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STRUNST.html#strnonstabvsarclen>`_
        in the `Structural Analysis Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/str_enercalc_app.html>`_.
        """
        command = (
            f"STABILIZE,{key},{method},{value},{substpopt},{forcelimit},{recalcdamp}"
        )
        return self.run(command, **kwargs)

    def thexpand(self, key: str = "", **kwargs):
        r"""Enables or disables thermal loading

        Mechanical APDL Command: `THEXPAND <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_THEXPAND.html>`_

        Parameters
        ----------
        key : str
            Activation key:

            * ``ON`` - Thermal loading is included in the load vector (default).

            * ``OFF`` - Thermal loading is not included in the load vector.

        Notes
        -----

        .. _THEXPAND_notes:

        Temperatures applied in the analysis are used by default to evaluate material properties and
        contribute to the load vector if the temperature does not equal the reference temperature and a
        coefficient of thermal expansion is specified.

        Use :ref:`thexpand`,OFF to evaluate the material properties but not contribute to the load vector.
        This capability is particularly useful when performing a harmonic analysis where you do not want to
        include harmonically varying thermal loads. It is also useful in a modal analysis when computing a
        modal load vector but excluding the thermal load.

        This command is valid for all analysis types except linear perturbation modal and linear
        perturbation harmonic analyses. For these two linear perturbation analysis types, the program
        internally sets :ref:`thexpand`,OFF, and it cannot be set to ON by using this command (
        :ref:`thexpand`,ON is ignored).
        """
        command = f"THEXPAND,{key}"
        return self.run(command, **kwargs)

    def thopt(
        self,
        refopt: str = "",
        reformtol: str = "",
        ntabpoints: str = "",
        tempmin: str = "",
        tempmax: str = "",
        algo: int | str = "",
        **kwargs,
    ):
        r"""Specifies nonlinear transient thermal solution options.

        Mechanical APDL Command: `THOPT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_THOPT.html>`_

        Parameters
        ----------
        refopt : str
            Matrix reform option.

            * ``FULL`` - Use the full Newton-Raphson solution option (default). All subsequent input values are
              ignored.

            * ``QUASI`` - Use a selective reform solution option based on ``REFORMTOL``.

        reformtol : str
            Property change tolerance for Matrix Reformation (.05 default). The thermal matrices are
            reformed if the maximum material property change in an element (from the previous reform time)
            is greater than the reform tolerance. Valid only when ``Refopt`` = QUASI.

        ntabpoints : str
            Number of points in Fast Material Table (64 default). Valid only when ``Refopt`` = QUASI.

        tempmin : str
            Minimum temperature for Fast Material Table. Defaults to the minimum temperature defined by the
            :ref:`mptemp` command for any material property defined. Valid only when ``Refopt`` = QUASI.

        tempmax : str
            Maximum temperature for Fast Material Table. Defaults to the maximum temperature defined by the
            :ref:`mptemp` command for any material property defined. Valid only when ``Refopt`` = QUASI.

        algo : int or str
            Specifies which solution algorithm to apply:

            * ``0`` - Multipass (default).

            * ``1`` - Iterative.

            Valid only when ``Refopt`` = QUASI.

        Notes
        -----

        .. _THOPT_notes:

        The QUASI matrix reform option is supported by the ICCG, JCG, PCG, and sparse solvers only (
        :ref:`eqslv` ). The Quasi method is an approximation to the FULL method and will not be as accurate
        when the nonlinearity is strong. However, you can control the inaccuracy by using small time steps.

        For ``Refopt`` = QUASI:

        * Results from a restart may be different than results from a single run because the stiffness
          matrices are always recreated in a restart run, but may or may not be in a single run (depending
          on the behavior resulting from the ``REFORMTOL`` setting). Additionally, results may differ
          between two single runs as well, if the matrices are reformed as a result of the ``REFORMTOL``
          setting.

        For more information, see `Solution Algorithms Used in Transient Thermal Analysis
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_the/thermsolualgors.html#therm_fullquasirad>`_
        """
        command = f"THOPT,{refopt},{reformtol},{ntabpoints},{tempmin},{tempmax},,{algo}"
        return self.run(command, **kwargs)

    def toffst(self, value: str = "", **kwargs):
        r"""Specifies the temperature offset from absolute zero to zero.

        Mechanical APDL Command: `TOFFST <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_TOFFST.html>`_

        Parameters
        ----------
        value : str
            Degrees between absolute zero and zero of temperature system used (should be positive).

        Notes
        -----

        .. _TOFFST_notes:

        Specifies the difference (in degrees) between absolute zero and the zero of the temperature system
        used. Absolute temperature values are required in evaluating certain expressions, such as for creep,
        swelling, radiation heat transfer, ``MASS71``, etc. (The offset temperature is not used in
        evaluating emissivity.) Examples are 460° for the Fahrenheit system and 273° for the Celsius system.
        The offset temperature is internally included in the element calculations and does not affect the
        temperature input or output. If used in SOLUTION, this command is valid only within the first load
        step.

        This command is also valid in PREP7.
        """
        command = f"TOFFST,{value}"
        return self.run(command, **kwargs)
