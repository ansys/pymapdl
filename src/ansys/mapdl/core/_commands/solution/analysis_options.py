from typing import Optional

from ansys.mapdl.core.mapdl_types import MapdlInt


class AnalysisOptions:
    def abextract(self, mode1="", mode2="", **kwargs):
        """Extracts the alpha-beta damping multipliers for Rayleigh damping.

        APDL Command: ABEXTRACT

        Parameters
        ----------
        mode1
            First mode number.

        mode2
            Second mode number.

        Notes
        -----
        ABEXTRACT calls the command macro DMPEXT to extract the damping ratio
        of MODE1 and MODE2 and then computes the Alpha and Beta damping
        multipliers for use in a subsequent structural harmonic or transient
        analysis. See Damping in the Structural Analysis Guide for more
        information on the alpha and beta damping multipliers. The damping
        multipliers are stored in parameters ALPHADMP and BETADMP and can be
        applied using the ALPHAD and BETAD commands. Before calling ABEXTRACT,
        you must issue RMFLVEC to extract the modal displacements. In addition,
        a node component FLUN must exist from all FLUID136 nodes. See
        Introduction for more information on thin film analyses.

        This command is also valid in PREP7.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"ABEXTRACT,{mode1},{mode2}"
        return self.run(command, **kwargs)

    def accoption(self, activate="", **kwargs):
        """Specifies GPU accelerator capability options.

        APDL Command: ACCOPTION

        Parameters
        ----------
        activate
            Activates the GPU accelerator capability within the equation
            solvers.

            Do not use GPU accelerator. - Use GPU accelerator.

        Notes
        -----
        The GPU accelerator capability requires specific hardware to be
        installed on the machine. See the appropriate ANSYS, Inc. Installation
        Guide (Windows or Linux) for a list of supported GPU hardware. Use of
        this capability also requires HPC licensing. For more information, see
        GPU Accelerator Capability in the Parallel Processing Guide.

        The GPU accelerator capability is available for the sparse direct
        solver and the PCG and JCG iterative solvers. Static, buckling, modal,
        full harmonic, and full transient analyses are supported. For buckling
        analyses, the Block Lanczos and Subspace eigensolvers are supported.
        For modal analyses, only the Block Lanczos, PCG Lanczos, Subspace,
        Unsymmetric, and Damped eigensolvers are supported. Activating this
        capability when using other equation solvers or other analysis types
        has no effect.

        The GPU accelerator capability is supported only on the Windows 64-bit
        and Linux 64-bit platforms.
        """
        command = f"ACCOPTION,{activate}"
        return self.run(command, **kwargs)

    def adams(self, nmodes="", kstress="", kshell="", **kwargs):
        """Performs solutions and writes flexible body information to a modal

        APDL Command: ADAMS
        neutral file (Jobname.MNF) for use in an ADAMS analysis.

        Parameters
        ----------
        nmodes
            Number of normal modes to be written to Jobname.MNF file (no
            default).

        kstress
            Specifies whether to write stress or strain results:

            0 - Do not write stress or strain results (default).

            1 - Write stress results.

            2 - Write strain results.

            3 - Write both stress and strain results.

        kshell
            Shell element output location. This option is valid only for shell
            elements.

            0, 1 - Shell top surface (default).

            2 - Shell middle surface.

            3 - Shell bottom surface.

        Notes
        -----
        ADAMS invokes a predefined ANSYS macro that solves a series of analyses
        and then writes the modal neutral file, Jobname.MNF. This file can be
        imported into the ADAMS program in order to perform a rigid body
        dynamics simulation. For detailed information on how to use the ADAMS
        command macro to create a modal neutral file, see Rigid Body Dynamics
        and the ANSYS-ADAMS Interface in the Substructuring Analysis Guide.

        Before running the ADAMS command macro, you must specify the units with
        the /UNITS command. The interface points should be the only selected
        nodes when the command macro is initiated. (Interface points are nodes
        where constraints may be applied in ADAMS.) Only selected elements will
        be considered in the calculations.

        By default, stress and strain data is transferred to the ADAMS program
        for all nodes, as specified by the KSTRESS value.  If you want to
        transfer stress/strain data for only a subset of nodes, select the
        desired subset and create a node component named "STRESS" before
        running the ADAMS command macro.  For example, you may want to select
        exterior nodes for the purpose of visualization in the ADAMS program.

        The default filename for the modal neutral file is Jobname.MNF. In
        interactive (GUI) mode, you can specify a filename other than
        Jobname.MNF. In batch mode, there is no option to change the filename,
        and the modal neutral file is always written to Jobname.MNF.
        """
        command = f"ADAMS,{nmodes},{kstress},{kshell}"
        return self.run(command, **kwargs)

    def antype(self, antype="", status="", ldstep="", substep="", action="", **kwargs):
        """Specifies the analysis type and restart status.

        APDL Command: ANTYPE

        Parameters
        ----------
        antype
            Analysis type (defaults to the previously specified analysis type,
            or to ``STATIC`` if none specified):

            STATIC or 0
                Perform a **static analysis**.
                Valid for all degrees of freedom.

            BUCKLE or 1
                Perform a buckling analysis.
                Implies that a previous static solution was performed with
                prestress effects calculated
                (:meth:`Mapdl.pstres('ON') <ansys.mapdl.core.Mapdl.pstres>`).
                Valid for structural degrees of freedom only.

            MODAL or 2
                Perform a modal analysis.
                Valid for structural and fluid degrees of freedom.

            HARMIC or 3
                Perform a harmonic analysis.
                Valid for structural, fluid, magnetic, and electrical degrees
                of freedom.

            TRANS or 4
                Perform a transient analysis.
                Valid for all degrees of freedom.

            SUBSTR or 7
                Perform a substructure analysis.
                Valid for all degrees of freedom.

            SPECTR or 8
                Perform a spectrum analysis.
                Implies that a previous modal analysis was
                performed.  Valid for structural degrees of freedom
                only.

        status
            Specifies the status of the analysis (new or restart):

            NEW
                Specifies a new analysis (default). If ``NEW``, the remaining fields on this
                command are ignored.

            RESTART
                Specifies a restart of a previous analysis. Valid for static, modal, and
                transient (full or mode-superposition method) analyses.
                For more information about restarting static and
                transient analyses, see Multiframe Restart in the Basic
                Analysis Guide. For more information on restarting a
                modal analysis, see Modal Analysis Restart in the Basic
                Analysis Guide.

                Multiframe restart is also valid for harmonic analysis, but is limited
                to 2-D magnetic analysis only.

                A substructure analysis (`backsubstitution` method only) can be restarted for the
                purpose of generating additional load vectors. For more information, see the
                :meth:`Mapdl.seopt() <ansys.mapdl.core.Mapdl.seopt>` command and
                Applying Loads and Creating the Superelement
                Matrices in the Substructuring Analysis Guide.

            VTREST
                Specifies the restart of a previous VT Accelerator analysis. Valid only with
                ``Antype = STATIC``, ``HARMIC``, or ``TRANS``. For more information,
                see VT Accelerator Re-run in the Basic Analysis Guide.

        ldstep
            Specifies the load step at which a multiframe restart begins.

        substep
            Specifies the substep at which a multiframe restart begins.

        action
            Specifies the manner of a multiframe restart.

            CONTINUE
                The program continues the analysis based on the specified
                ``LDSTEP`` and ``SUBSTEP`` (default). The current load step is continued.
                If the end of the load step is encountered in the ``.Rnnn`` file, a
                new load step is started. The program deletes all ``.Rnnn``
                files, or ``.Mnnn`` files for mode-superposition transient
                analyses, beyond the point of restart and updates the
                ``.LDHI`` file if a new load step is encountered.

            ENDSTEP
                At restart, force the specified load step (``LDSTEP``) to end at the specified
                substep (``SUBSTEP``), even though the end of the current
                load step has not been reached. At the end of the
                specified substep, all loadings are scaled to the level
                of the current ending and stored in the ``.LDHI`` file. A run
                following this ``ENDSTEP`` starts a new load step. This
                capability allows you to change the load level in the
                middle of a load step. The program updates the ``.LDHI`` file
                and deletes all .Rnnn files, or ``.Mnnn`` files for mode-
                superposition transient analyses, beyond the point of
                ``ENDSTEP``. The ``.Rnnn`` or ``.Mnnn`` file at the point of ``ENDSTEP``
                are rewritten to record the rescaled load level.

            RSTCREATE
                At restart, retrieve information to be written to the results file for the
                specified load step (``LDSTEP``) and substep (``SUBSTEP``). Be
                sure to use :meth:`Mapdl.outres() <ansys.mapdl.core.Mapdl.outres>`
                to write the results to the
                results file. This action does not affect the ``.LDHI`` or
                ``.Rnnn`` files. Previous items stored in the results file
                at and beyond the point of ``RSTCREATE`` are deleted. This
                option cannot be used to restart a mode-superposition
                transient analysis.

            PERTURB
                At restart, a linear perturbation analysis (static, modal, buckling, or full
                harmonic) is performed for the specified load step
                (``LDSTEP``) and substep (``SUBSTEP``). This action does not
                affect the ``.LDHI``, ``.Rnnn``, or ``.RST`` files.

        Notes
        -----
        If using the :meth:`Mapdl.antype() <ansys.mapdl.core.Mapdl.antype>`
        command to change the analysis type in the same
        :meth:`Mapdl.solve() <ansys.mapdl.core.Mapdl.solve>` session,
        the program issues the following message: `"Some analysis
        options have been reset to their defaults. Please verify current
        settings or respecify as required."` Typically, the program resets
        commands such as :meth:`Mapdl.nlgeom() <ansys.mapdl.core.Mapdl.nlgeom>` and
        :meth:`Mapdl.eqslv() <ansys.mapdl.core.Mapdl.eqslv>` to their default values.

        The analysis type (:meth:`Mapdl.antype() <ansys.mapdl.core.Mapdl.antype>`)
        cannot be changed if a restart is specified.
        Always save parameters before doing a restart. For more information on
        the different types of restart, see Restarting an Analysis in the Basic
        Analysis Guide.

        This command is also valid in :meth:`Mapdl.prep7() <ansys.mapdl.core.Mapdl.prep7>`.

        The ANSYS Professional - Nonlinear Structural (PRN) product supports
        the ``Antype = TRANS`` option for mode-superposition (
        :meth:`Mapdl.trnopt("MSUP") <ansys.mapdl.core.Mapdl.trnopt>`) analyses
        only.
        """
        command = f"ANTYPE,{antype},{status},{ldstep},{substep},{action}"
        return self.run(command, **kwargs)

    def ascres(self, opt="", **kwargs):
        """Specifies the output type for an acoustic scattering analysis.

        APDL Command: ASCRES

        Parameters
        ----------
        opt
            Output option:

            TOTAL - Output the total pressure field (default).

            SCAT - Output the scattered pressure field.

        Notes
        -----
        Use the ASCRES command to specify the output type for an acoustic
        scattering analysis.

        The scattered option (Opt = SCAT) provides a scattered pressure output,
        psc, required for calculating target strength (TS).

        The default behavior (Opt = TOTAL) provides a sum of the incident and
        scattering fields, ptotal = pinc + psc.

        Issue the AWAVE command to define the incident pressure pinc. If the
        AWAVE command is defined with Opt2 = INT, only the total pressure field
        is output regardless of the ASCRES,Opt command.
        """
        command = f"ASCRES,{opt}"
        return self.run(command, **kwargs)

    def asol(self, lab="", opt="", **kwargs):
        """Specifies the output type of an acoustic scattering analysis.

        APDL Command: ASOL

        Parameters
        ----------
        lab
            Acoustic solver specification (no default):

            SCAT - Set acoustic solver to the scattered field formulation.

        opt
            Option identifying an acoustic solver status:

            OFF - Deactivate the specified acoustic solver (default).

            ON - Activate the specified acoustic solver.

        Notes
        -----
        Use the ASOL command to activate the specified acoustic solution
        process.

        The scattered option (Lab = SCAT) sets the acoustic solver to the
        scattered-pressure field formulation.

        Issue the AWAVE command to define the incident pressure pinc. If the
        AWAVE command is defined with Opt2 = INT, the acoustic solver is set to
        the scattered field formulation regardless of the ASOL command issued.
        """
        command = f"ASOL,{lab},{opt}"
        return self.run(command, **kwargs)

    def bcsoption(self, memory_option="", memory_size="", solve_info="", **kwargs):
        """Sets memory option for the sparse solver.

        APDL Command: BCSOPTION

        Parameters
        ----------
        memory_option
            Memory allocation option:

            DEFAULT
                Use the default memory allocation strategy for
                the sparse solver. The default strategy attempts
                to run in the ``INCORE`` memory mode. If there is
                not enough available physical memory when the
                solver starts to run in the ``INCORE`` memory mode,
                the solver will then attempt to run in the
                ``OUTOFCORE`` memory mode.

            INCORE
                Use a memory allocation strategy in the sparse
                solver that will attempt to obtain enough memory
                to run with the entire factorized matrix in
                memory. This option uses the most amount of
                memory and should avoid doing any I/O. By
                avoiding I/O, this option achieves optimal solver
                performance. However, a significant amount of
                memory is required to run in this mode, and it is
                only recommended on machines with a large amount
                of memory. If the allocation for in-core memory
                fails, the solver will automatically revert to
                out-of-core memory mode.

            OUTOFCORE
                Use a memory allocation strategy in the sparse
                solver that will attempt to allocate only
                enough work space to factor each individual
                frontal matrix in memory, but will store the
                entire factorized matrix on disk. Typically,
                this memory mode results in poor performance
                due to the potential bottleneck caused by the
                I/O to the various files written by the
                solver.

            FORCE
                This option, when used in conjunction with the
                ``Memory_Size`` option, allows you to force the sparse
                solver to run with a specific amount of
                memory. This option is only recommended for the
                advanced user who understands sparse solver memory
                requirements for the problem being solved,
                understands the physical memory on the system, and
                wants to control the sparse solver memory usage.

        memory_size
            Initial memory size allocation for the sparse solver in
            MB. This argument allows you to tune the sparse solver
            memory and is not generally required. Although there is no
            upper limit for ``Memory_Size``, the ``Memory_Size`` setting
            should always be well within the physical memory
            available, but not so small as to cause the sparse solver
            to run out of memory. Warnings and/or errors from the
            sparse solver will appear if this value is set too low. If
            the FORCE memory option is used, this value is the amount
            of memory allocated for the entire duration of the sparse
            solver solution.

        solve_info
            Solver output option:

            OFF
                Turns off additional output printing from the sparse
                solver (default).

            PERFORMANCE
                Turns on additional output printing from the
                sparse solver, including a performance
                summary and a summary of file I/O for the
                sparse solver. Information on memory usage
                during assembly of the global matrix (that
                is, creation of the Jobname.FULL file) is
                also printed with this option.

        Notes
        -----
        This command controls options related to the sparse solver in
        all analysis types where the sparse solver can be used. It
        also controls the Block Lanczos eigensolver in a modal or
        buckling analysis.

        The sparse solver runs from one large work space (that is, one
        large memory allocation). The amount of memory required for
        the sparse solver is unknown until the matrix structure is
        preprocessed, including equation reordering. The amount of
        memory allocated for the sparse solver is then dynamically
        adjusted to supply the solver what it needs to compute the
        solution.

        If you have a very large memory system, you may want to try
        selecting the ``INCORE`` memory mode for larger jobs to improve
        performance. When running the sparse solver on a machine with
        very slow I/O performance (for example, slow hard drive
        speed), you may want to try using the ``INCORE`` memory mode to
        achieve better performance. However, doing so may require much
        more memory compared to running in the ``OUTOFCORE`` memory mode.

        Running with the ``INCORE`` memory mode is best for jobs which
        comfortably fit within the limits of the physical memory on a
        given system. If the sparse solver work space exceeds physical
        memory size, the system will be forced to use virtual memory
        (or the system page/swap file). In this case, it is typically
        more efficient to run with the ``OUTOFCORE`` memory mode. Assuming
        the job fits comfortably within the limits of the machine,
        running with the ``INCORE`` memory mode is often ideal for jobs
        where repeated solves are performed for a single matrix
        factorization.  This occurs in a modal or buckling analysis or
        when doing multiple load steps in a linear, static analysis.

        For repeated runs with the sparse solver, you may set the
        initial sparse solver memory allocation to the amount required
        for factorization. This strategy reduces the frequency of
        allocation and reallocation in the run to make the ``INCORE``
        option fully effective. If you have a very large memory
        system, you may use the Memory_Size argument to increase the
        maximum size attempted for in-core runs.
        """
        command = f"BCSOPTION,,{memory_option},{memory_size},,,{solve_info}"
        return self.run(command, **kwargs)

    def cgrow(self, action="", par1="", par2="", **kwargs):
        """Defines crack-growth information

        APDL Command: CGROW

        Parameters
        ----------
        action
            Specifies the action for defining or manipulating crack-growth
            data:

            NEW
                Initiate a new set of crack-growth simulation data (default).

            CID
                Specify the crack-calculation (CINT) ID for energy-release rates to be used in
                the fracture criterion calculation.

            FCOPTION
                Specify the fracture criterion for crack-growth/delamination.

            CPATH
                Specify the element component for crack growth.

            DTIME
                Specify the initial time step for crack growth.

            DTMIN
                Specify the minimum time step for crack growth.

            DTMAX
                Specify the maximum time step for crack growth.

            FCRAT
                Fracture criterion ratio (fc).

            STOP
                Stops the analysis when the specified maximum crack extension is reached.

            METHOD
                Define the method of crack propagation.

        Notes
        -----
        When ``Action = NEW``, the :meth:`Mapdl.cgrow() <ansys.mapdl.core.Mapdl.cgrow>` command initializes a crack-growth
        simulation set. Subsequent :meth:`Mapdl.cgrow() <ansys.mapdl.core.Mapdl.cgrow>` commands define the parameters
        necessary for the simulation.

        For multiple cracks, issue multiple :meth:`Mapdl.cgrow("NEW") <ansys.mapdl.core.Mapdl.cgrow>` commands (and any
        subsequent :meth:`Mapdl.cgrow() <ansys.mapdl.core.Mapdl.cgrow>` commands necessary to define the parameters) for each
        crack.

        If the analysis is restarted (:meth:`Mapdl.antype("","RESTART") <ansys.mapdl.core.Mapdl.antype>`), the :meth:`Mapdl.cgrow() <ansys.mapdl.core.Mapdl.cgrow>` command must
        be re-issued.

        For additional details on this command, see
        https://www.mm.bme.hu/~gyebro/files/ans_help_v182/ans_cmd/Hlp_C_CGROW.html

        """
        command = f"CGROW,{action},{par1},{par2}"
        return self.run(command, **kwargs)

    def cmatrix(
        self,
        symfac="",
        condname="",
        numcond="",
        grndkey="",
        capname="",
        **kwargs,
    ):
        """Performs electrostatic field solutions and calculates the
        self and mutual capacitances between multiple conductors.x

        APDL Command: CMATRIX

        Parameters
        ----------
        symfac
            Geometric symmetry factor.  Capacitance values are scaled by this
            factor which represents the fraction of the total device modeled.
            Defaults to 1.

        condname
            Alphanumeric prefix identifier used in defining named conductor
            components.

        numcond
            Total Number of Components.  If a ground is modeled, it is to be
            included as a component.  If a ground is not modeled, but infinite
            elements are used to model the far-field ground, a named component
            for the far-field ground is not required.

        grndkey
            Ground key:

            0 - Ground is one of the components, which is not at infinity.

            1 - Ground is at infinity (modeled by infinite elements).

        capname
            Array name for computed capacitance matrix.  Defaults to CMATRIX.

        Notes
        -----
        To invoke the CMATRIX macro, the exterior nodes of each conductor must
        be grouped into individual components using the CM command.  Each set
        of  independent components is assigned a component name with a common
        prefix followed by the conductor number.  A conductor system with a
        ground must also include the ground nodes as a component.  The ground
        component is numbered last in the component name sequence.

        A ground capacitance matrix relates charge to a voltage vector.  A
        ground matrix cannot be applied to a circuit modeler. The lumped
        capacitance matrix is a combination of  lumped "arrangements" of
        voltage differences between conductors.  Use the lumped capacitance
        terms in a circuit modeler to represent capacitances between
        conductors.

        Enclose all name-strings in single quotes in the CMATRIX command line.

        See the Mechanical APDL Theory Reference and HMAGSOLV in the Low-
        Frequency Electromagnetic Analysis Guide for details.

        This command does not support multiframe restarts.
        """
        command = f"CMATRIX,{symfac},'{condname}',{numcond},{grndkey},'{capname}'"
        return self.run(command, **kwargs)

    def cmsopt(
        self,
        cmsmeth="",
        nmode="",
        freqb="",
        freqe="",
        fbddef="",
        fbdval="",
        iokey="",
        **kwargs,
    ):
        """Specifies component mode synthesis (CMS) analysis options.

        APDL Command: CMSOPT

        Parameters
        ----------
        cmsmeth
            The component mode synthesis method to use. This value is required.

            FIX
                Fixed-interface method.

            FREE
                Free-interface method.

            RFFB
                Residual-flexible free-interface method.

        nmode
            The number of normal modes extracted and used in the superelement
            generation. This value is required; the minimum is 1.

        freqb
            Beginning, or lower end, of frequency range of interest. This value
            is optional.

        freqe
            Ending, or upper end, of frequency range of interest. This value is
            optional.

        fbddef
            In a free-interface (CMSMETH = FREE) or residual-flexible free-
            interface (CMSMETH = RFFB) CMS analysis, the method to use for
            defining free body modes:

            FNUM
                The number (FDBVAL) of rigid body modes in the calculation.

            FTOL
                Employ a specified tolerance (FDBVAL) to determine rigid body modes in the
                calculation.

            FAUTO
                Automatically determine rigid body modes in the calculation. This method is the
                default.

            RIGID
                If no rigid body modes exist, define your own via the RIGID command.

        fbdval
            In a free-interface CMS analysis (CMSMETH = FREE), the number of
            rigid body modes if FBDDEF = fnum (where the value is an integer
            from 0 through 6), or the tolerance to employ if FBDDEF = ftol
            (where the value is a positive real number representing rad/sec).
            This value is required only when FBDDEF = fnum or FBDDEF = ftol;
            otherwise, any specified value is ignored.

        iokey
            Output key to control writing of the transformation matrix to the
            .TCMS file (FIX or FREE methods) or body properties to the .EXB
            file (FIX method).

            TCMS
                Write the transformation matrix of the nodal component defined by the OUTPR
                command to a .TCMS file. Refer to TCMS File Format in the
                Programmer's Reference for more information on the this
                file.

            EXB
                Write a body property input file (.EXB file) containing the condensed
                substructure matrices and other body properties for use with
                AVL EXCITE. Refer to ANSYS Interface to AVL EXCITE in the
                Substructuring Analysis Guide for more information.

        Notes
        -----
        CMS employs the Block Lanczos eigensolution method in the generation
        pass.

        CMS supports damping matrix reduction when a damping matrix exists. Set
        the matrix generation key to 3 (SEOPT,Sename,SEMATR) to generate and
        then reduce stiffness, mass, and damping matrices.

        CMS does not support the SEOPT,,,,,RESOLVE command. Instead, ANSYS sets
        the expansion method for the expansion pass (EXPMTH) to BACKSUB.

        For more information about performing a CMS analysis, see Component
        Mode Synthesis in the Substructuring Analysis Guide.

        If IOKEY = TCMS is used to output the transformation matrix, then only
        ITEM = NSOL is valid in the OUTPR command.  In the interactive
        sessions, the transformation matrix will not be output if the model has
        more than 10 elements.

        This command is also valid in /PREP7.
        """
        command = f"CMSOPT,{cmsmeth},{nmode},{freqb},{freqe},{fbddef},{fbdval},{iokey}"
        return self.run(command, **kwargs)

    def cncheck(
        self,
        option="",
        rid1="",
        rid2="",
        rinc="",
        intertype="",
        trlevel="",
        cgap="",
        cpen="",
        ioff="",
        **kwargs,
    ):
        """Provides and/or adjusts the initial status of contact pairs.

        APDL Command: CNCHECK

        Parameters
        ----------
        option
            Option to be performed:

            * ``"DETAIL"`` : List all contact pair properties (default).

            * ``"SUMMARY"`` : List only the open/closed status for each
              contact pair.

            * ``"POST"`` : Execute a partial solution to write the initial
              contact configuration to the Jobname.RCN file.

            * ``"ADJUST"`` : Physically move contact nodes to the target
              in order to close a gap or reduce penetration. The initial
              adjustment is converted to structural displacement values
              (UX, UY, UZ) and stored in the Jobname.RCN file.

            * ``"MORPH"`` : Physically move contact nodes to the target in
              order to close a gap or reduce penetration, and also morph
              the underlying solid mesh. The initial adjustment of contact
              nodes and repositioning of solid element nodes due to mesh
              morphing are converted to structural displacement values
              (UX, UY, UZ) and stored in the Jobname.RCN file.

            * ``"RESET"`` : Reset target element and contact element key
              options and real constants to their default values. This
              option is not valid for general contact.

            * ``"AUTO"`` : Automatically sets certain real constants and
              key options to recommended values or settings in order to
              achieve better convergence based on overall contact pair
              behaviors. This option is not valid for general contact.

            * ``"TRIM"`` : Trim contact pair (remove certain contact and
              target elements).

            * ``"UNSE"`` : Unselect certain contact and target elements.

        rid1, rid2, rinc
            For pair-based contact, the range of real constant pair IDs
            for which Option will be performed. If RID2 is not specified,
            it defaults to RID1. If no value is specified, all contact
            pairs in the selected set of elements are considered.

            For general contact (InterType = GCN), RID1 and RID2 are
            section IDs associated with general contact surfaces instead
            of real constant IDs. If RINC = 0, the Option is performed
            between the two sections, RID1 and RID2. If RINC > 0, the
            Option is performed among all specified sections (RID1 to RID2
            with increment of RINC).

        intertype
            The type of contact interface (pair-based versus general
            contact) to be considered; or the type of contact pair to be
            trimmed/unselected/auto-set.

            The following labels specify the type of contact interface:

            * ``""`` : (blank) Include all contact definitions (pair-based
              and general contact).

            * ``"GCN"`` : Include general contact definitions only (not valid when Option = RESET or AUTO).

            The following labels specify the type of contact pairs to be
            trimmed/unselected/auto-set (used only when Option = TRIM,
            UNSE, or AUTO, and only for pair-based contact definitions):

            * ``"ANY"`` : All types (default).

            * ``"MPC"`` : MPC-based contact pairs (KEYOPT(2) = 2).

            * ``"BOND"`` : Bonded contact pairs (KEYOPT(12) = 3, 5, 6).

            * ``"NOSP"`` : No separation contact pairs (KEYOPT(12) = 2, 4).

            * ``"INAC"`` : Inactive contact pairs (symmetric contact pairs for MPC contact or KEYOPT(8) = 2).

            * ``"TRlevel"`` : mming level (used only when Option = TRIM, UNSE, or MORPH):

            * ``"(blank)"`` : Normal trimming (default): remove/unselect contact and target elements which are in far-field.

            * ``"AGGRE"`` : Aggressive trimming: remove/unselect contact and target elements which are in far-field, and certain elements in near-field.

        cgap
            They are only valid when Option = ADJUST or MORPH.  Control
            parameter for opening gap. Close the opening gap if the
            absolute value of the gap is smaller than the CGAP value. CGAP
            defaults to ``0.25*PINB`` (where PINB is the pinball radius) for
            bonded and no-separation contact; otherwise it defaults to the
            value of real constant ICONT.

        CPEN
            They are only valid when Option = ADJUST or MORPH.  Control
            parameter for initial penetration. Close the initial
            penetration if the absolute value of the penetration is
            smaller than the CPEN value. CPEN defaults to ``0.25*PINB`` (where
            PINB is the pinball radius) for any type of interface behavior
            (either bonded or standard contact).

        IOFF
            They are only valid when Option = ADJUST or MORPH.  Control
            parameter for initial adjustment. Input a positive value to
            adjust the contact nodes towards the target surface with a
            constant interference distance equal to IOFF. Input a negative
            value to adjust the contact node towards the target surface
            with a uniform gap distance equal to the absolute value of
            IOFF.

        Notes
        -----
        The CNCHECK command provides information for surface-to-surface,
        node-to-surface, and line-to-line contact pairs (element types
        TARGE169, TARGE170, CONTA171, CONTA172, CONTA173, CONTA174,
        CONTA175, CONTA176, CONTA177). All contact and target elements of
        interest, along with the solid elements and nodes attached to
        them, must be selected for the command to function properly. For
        performance reasons, the program uses a subset of nodes and
        elements based on the specified contact regions (RID1, RID2, RINC)
        when executing the CNCHECK command.

        For additional details, see the notes section at:
        https://www.mm.bme.hu/~gyebro/files/ans_help_v182/ans_cmd/Hlp_C_CNCHECK.html

        """
        command = f"CNCHECK,{option},{rid1},{rid2},{rinc},{intertype},{trlevel},{cgap},{cpen},{ioff}"
        return self.run(command, **kwargs)

    def cnkmod(self, itype="", knum="", value="", **kwargs):
        """Modifies contact element key options.

        APDL Command: CNKMOD

        Parameters
        ----------
        itype
            Contact element type number as defined on the ET command.

        knum
            Number of the KEYOPT to be modified (KEYOPT(KNUM)).

        value
            Value to be assigned to the KEYOPT.

        Notes
        -----
        The CNKMOD command has the same syntax as the KEYOPT command. However,
        it is valid only in the SOLUTION processor. This command is intended
        only for use in a linear perturbation analysis, and can only be used to
        modify certain contact element KEYOPT values as described below.

        Modifying KEYOPT(12)

        One use for this command is to modify contact interface behavior
        between load steps in a linear perturbation analysis; it allows the
        user to control the contact status locally per contact pair. For this
        application, this command is limited to changing the contact interface
        behavior key option: KEYOPT(12) of CONTA171, CONTA172, CONTA173,
        CONTA174, CONTA175, CONTA176, and CONTA177; and KEYOPT(10) of CONTA178.

        When used for this purpose, the command adjusts the contact status from
        the linear perturbation base analysis (at the point of restart) as
        described in the table below. Note that CNKMOD allows you to take
        points in the base analysis that are near contact (within the pinball
        region) and modify them to be treated as "in contact" in the
        perturbation analysis; see the "1 - near-field" row with KEYOPT(12)
        values set to 4 or 5. CNKMOD also allows you to take points that are
        sliding in the base analysis and treat them as sticking in the
        perturbation analysis, irrespective of the MU value; see the "2 -
        sliding" row with KEYOPT(12) values set to 1,3, 5, or 6.

        Table: 128:: : Adjusted Contact Status with CNKMOD is Issued

        (if outside of the adjusted pinball region)

        (if inside of the adjusted pinball region)

        (if outside of the adjusted pinball region)

        (if inside of the adjusted pinball region)

        If an open gap exists at the end of the previous load step and the
        contact status is adjusted as sliding or sticking due to a "bonded" or
        "no separation" contact behavior definition, then the program will
        treat it as near-field contact when executing CNKMOD in the subsequent
        load steps.

        In the linear perturbation analysis procedure, contact status can also
        be controlled or modified by the PERTURB command. The contact status
        always follows local controls defined by the CNKMOD command first, and
        is then adjusted by the global sticking or bonded setting (ContKey =
        STICKING or BONDED) on the PERTURB command (see the PERTURB command for
        details).

        Modifying KEYOPT(3)

        Another use for this command is to change the units of normal contact
        stiffness (contact element real constant FKN) in a linear perturbation
        modal analysis that is used to model brake squeal. For contact elements
        CONTA171, CONTA172, CONTA173, and CONTA174, KEYOPT(3) controls the
        units of normal contact stiffness. You can issue the command
        CNKMOD,ITYPE,3,1 during the first phase of the linear perturbation
        analysis in order to change the units of normal contact stiffness from
        FORCE/LENGTH3 (in the base analysis) to FORCE/LENGTH. Note that
        KEYOPT(3) = 1 is valid only when a penalty-based algorithm is used
        (KEYOPT(2) = 0 or 1) and the absolute normal contact stiffness value is
        explicitly specified (that is, a negative value input for real constant
        FKN).
        """
        command = f"CNKMOD,{itype},{knum},{value}"
        return self.run(command, **kwargs)

    def cntr(self, option="", key="", **kwargs):
        """Redirects contact pair output quantities to a text file.

        APDL Command: CNTR

        Parameters
        ----------
        option
            Output option:

            OUT - Contact output control.

        key
            Control key:

            NO - Write contact information to the output file or to the screen (default).

            YES - Write contact information to the Jobname.CNM file.

        Notes
        -----
        Issue the command CNTR,OUT,YES to redirect contact pair output
        quantities to the Jobname.CNM file.

        To ensure that the contact information is written to Jobname.CNM,
        reissue CNTR,OUT,YES each time you reenter the solution processor
        (/SOLU).
        """
        command = f"CNTR,{option},{key}"
        return self.run(command, **kwargs)

    def cutcontrol(self, lab="", value="", option="", **kwargs):
        """Controls time-step cutback during a nonlinear solution.

        APDL Command: CUTCONTROL

        Parameters
        ----------
        lab
            Specifies the criteria for causing a cutback.  Valid labels are:

            PLSLIMIT
                Maximum equivalent plastic strain allowed within a time-step (substep).  If the
                calculated value exceeds the VALUE, the program
                performs a cutback (bisection).  VALUE defaults to 0.15
                (15%).

            CRPLIMIT
                Set values for calculating the maximum equivalent creep ratio allowed within a
                time step. If the calculated maximum creep ratio
                exceeds the defined creep ratio limit, the program
                performs a cutback.

            DSPLIMIT
                Maximum incremental displacement within the solution field in a time step
                (substep).  If the maximum calculated value exceeds
                VALUE, the program performs a cutback (bisection).
                VALUE defaults to 1.0 x 107.

            NPOINT
                Number of points in a cycle for a second order dynamic equation, used to
                control automatic time stepping.  If the number of
                solution points per cycle is less than VALUE, the program
                performs a cutback in time step size. VALUE defaults to
                13 for linear analysis, 5 for nonlinear analysis. A
                larger number of points yields a more accurate solution
                but also increases the solution run time.

                This option works well for linear problems. For nonlinear analyses, other
                factors such as contact status changes and solution convergence rate can
                overwrite NPOINT. See Automatic Time Stepping in the Mechanical APDL
                Theory Reference for more information on automatic time stepping.

            NOITERPREDICT

                If VALUE is 0 (default), an internal auto time step scheme will predict
                the number of iterations for nonlinear convergence and perform a cutback
                earlier than the number of iterations specified by the NEQIT command.
                This is the recommended option.

                If VALUE is 1, the solution will iterate (if nonconvergent) to NEQIT
                number of iterations before a cutback is invoked.
                It is sometimes useful for poorly-convergent problems, but rarely needed in general.

                Bisection is also controlled by contact status change, plasticity or creep
                strain limit, and other factors. If any of these
                factors occur, bisection will still take place,
                regardless of the NOITERPREDICT setting.

            CUTBACKFACTOR
                Changes the cutback value for bisection. Default is 0.5. VALUE must be greater
                than 0.0 and less than 1.0. This option is active
                only if AUTOTS,ON is set.

        value
            Numeric value for the specified cutback criterion. For Lab =
            CRPLIMIT, VALUE is the creep criteria for the creep ratio limit.

        option
            Type of creep analysis. Valid for Lab = CRPLIMIT only.

            IMPRATIO
                Set the maximum creep ratio value for implicit creep. The default is 0.0 (i.e.,
                no creep limit control) and any positive value is
                valid. (See Implicit Creep Procedure in the Structural
                Analysis Guide for information on how to define
                implicit creep.)

            EXPRATIO
                Set the maximum creep ratio value for explicit creep. The default value is 0.1
                and any positive value up to 0.25 is allowed. (See
                Explicit Creep Procedure in the Structural Analysis
                Guide for information on how to define explicit
                creep.)

            STSLIMIT
                Stress threshold for calculating the creep ratio. For integration points with
                effective stress below this threshold, the creep ratio
                does not cause cutback. The default value is 0.0 and
                any positive value is valid.

            STNLIMIT
                Elastic strain threshold for calculating the creep ratio. For integration
                points with effective elastic strain below this
                threshold, the creep ratio does not cause cutback. The
                default value is 0.0 and any positive value is valid.

        Notes
        -----
        A cutback is a method for automatically reducing the step size when
        either the solution error is too large or the solution encounters
        convergence difficulties during a nonlinear analysis.

        Should a convergence failure occur, the program reduces the time step
        interval to a fraction of its previous size and automatically continues
        the solution from the last successfully converged time step. If the
        reduced time step again fails to converge, the program again reduces
        the time step size and proceeds with the solution. This process
        continues until convergence is achieved or the minimum specified time
        step value is reached.

        For creep analysis, the cutback procedure is similar; the process
        continues until the minimum specified time step size is reached.
        However, if the creep ratio limit is exceeded, the program issues a
        warning but continues the substep until the analysis is complete. In
        this case, convergence is achieved but the creep ratio criteria is not
        satisfied.

        The CRPLIM command is functionally equivalent to Lab = CRPLIMIT with
        options IMPRATIO and EXPRATIO
        """
        command = f"CUTCONTROL,{lab},{value},{option}"
        return self.run(command, **kwargs)

    def ddoption(self, decomp="", **kwargs):
        """Sets domain decomposer option for Distributed ANSYS.

        APDL Command: DDOPTION

        Parameters
        ----------
        decomp
            Controls which domain decomposition algorithm to use.

            AUTO
                Use the default domain decomposition algorithm when splitting the model into
                domains for Distributed ANSYS (default).

            GREEDY
                Use the "greedy" domain decomposition algorithm.

            METIS
                Use the METIS graph partitioning domain decomposition algorithm.

        Notes
        -----
        This command controls options relating to the domain decomposition
        algorithm used by Distributed ANSYS to split the model into pieces (or
        domains), with each piece being solved on a different processor.

        The greedy domain decomposition algorithm starts from a single element
        at a corner of the model. The domain grows by taking the properly
        connected neighboring elements and stops after reaching the optimal
        size.

        The METIS domain decomposition algorithm starts by creating a graph
        from the finite element mesh. It then uses a multilevel graph
        partitioning scheme which reduces the size of the original graph,
        creates domains using the reduced graph, and then creates the final CPU
        domains by expanding the smaller domains from the reduced graph back to
        the original mesh.
        """
        command = f"DDOPTION,{decomp}"
        return self.run(command, **kwargs)

    def dmpext(
        self,
        smode="",
        tmode="",
        dmpname="",
        freqb="",
        freqe="",
        nsteps="",
        **kwargs,
    ):
        """Extracts modal damping coefficients in a specified frequency range.

        APDL Command: DMPEXT

        Parameters
        ----------
        smode
            Source mode number. There is no default for this field; you must
            enter an integer greater than zero.

        tmode
            Target mode. Defaults to SMODE.

        dmpname
            Array parameter name containing the damping results. Defaults to
            d_damp.

        freqb
            Beginning frequency range (real number greater than zero) or 'EIG'
            at eigenfrequency of source mode. 'EIG' is valid only if SMODE =
            TMODE. Note that EIG must be enclosed in single quotes when this
            command is used on the command line or in an input file. There is
            no default for this field; you must enter a value.

        freqe
            End of frequency range. Must be blank for Freqb = EIG. Default is
            Freqb.

        nsteps
            Number of substeps. Defaults to 1.

        Notes
        -----
        DMPEXT invokes an ANSYS macro that uses modal projection techniques to
        compute the damping force by the modal velocity of the source mode onto
        the target mode. From the damping force, damping parameters are
        extracted. DMPEXT creates an array parameter Dmpname, with the
        following entries in each row:

        response frequency

        modal damping coefficient

        modal squeeze stiffness coefficient

        damping ratio

        squeeze-to-structural stiffness ratio

        The macro requires the modal displacements from the file Jobname.EFL
        obtained from the RMFLVEC command. In addition, a node component FLUN
        must exist from all FLUID136 nodes. The computed damping ratio may be
        used to specify constant or modal damping by means of the DMPRAT or
        MDAMP commands. For Rayleigh damping, use the ABEXTRACT command to
        compute ALPHAD and BETAD damping parameters. See Thin Film Analysis for
        more information on thin film analyses.

        The macro uses the LSSOLVE command to perform two load steps for each
        frequency.  The first load case contains the solution of the source
        mode excitation and can be used for further postprocessing. Solid model
        boundary conditions are deleted from the model.  In addition,
        prescribed nodal boundary conditions are applied to the model.  You
        should carefully check the boundary conditions of your model prior to
        executing a subsequent analysis.

        This command is also valid in PREP7.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"DMPEXT,{smode},{tmode},{dmpname},{freqb},{freqe},{nsteps}"
        return self.run(command, **kwargs)

    def dmpoption(self, filetype="", combine="", **kwargs):
        """Specifies distributed memory parallel (Distributed ANSYS) file

        APDL Command: DMPOPTION
        combination options.

        Parameters
        ----------
        filetype
            Type of solution file to combine after a distributed memory
            parallel solution. There is no default; if (blank), the command is
            ignored.

            RST - Results files (.RST, .RTH, .RMG, .RSTP)

            EMAT - Element matrix files (.EMAT).

            ESAV - Element saved data files (.ESAVE)

            MODE - Modal results files (.MODE)

            MLV - Modal load vector file (.MLV)

            IST - Initial state file (.IST)

            FULL - Full matrix file (.FULL)

            RFRQ - Reduced complex displacement file (.RFRQ)

            RDSP - Reduced displacement file (.RDSP)

        combine
            Option to combine solution files.

            Yes - Combine solution files (default).

            No - Do not combine solution files.

        Notes
        -----
        The DMPOPTION command controls how solution files are written during a
        distributed memory parallel (Distributed ANSYS) solution. This command
        is most useful for controlling how results files (.RST,.RTH, etc.) are
        written.

        In a distributed memory parallel solution, a local results file is
        written by each process (JobnameN.ext, where N is the process number).
        By default, the program automatically combines the local results files
        (for example, JobnameN.RST) upon leaving the SOLUTION processor (for
        example, upon the FINISH command) into a single global results file
        (Jobname.RST) which can be used in ANSYS postprocessing. To reduce the
        amount of communication and I/O performed by this operation, you can
        issue the command DMPOPTION,RST,NO to bypass this step of combining the
        local results files; the local files will remain on the local disks in
        the current working directory. You can then use the RESCOMBINE command
        macro in the POST1 general postprocessor (/POST1) to read all results
        into the database for postprocessing.

        The RESCOMBINE command macro is intended for use with POST1. If you
        want to postprocess distributed parallel solution results using the
        POST26 time-history postprocessor (/POST26), it is recommended that you
        combine your local results files into one global results file
        (DMPOPTION,RST,YES or COMBINE).

        Local .EMAT, .ESAV, .MODE, .MLV, .IST, .RFRQ, .RDSP, and .FULL files
        are also written (when applicable) by each process in a distributed
        memory parallel solution. If these files are not needed for a
        downstream solution or operation, you can issue the command
        DMPOPTION,FileType,NO for each file type to bypass the file combination
        step and thereby improve performance. You should not bypass the file
        combination step if a downstream PSD analysis or modal expansion pass
        will be performed.

        If DMPOPTION,MODE,NO or DMPOPTION,RST,NO is specified in a modal
        analysis, element results cannot be written to the combined mode file
        (Jobname.MODE). In this case, if Distributed ANSYS is used in a
        downstream harmonic or transient analysis that uses the mode-
        superposition method, the MSUPkey on the MXPAND command can retain its
        value. However, if shared memory parallel processing is used in the
        downstream harmonic or transient analysis, the MSUPkey is effectively
        set to NO.

        The DMPOPTION command can be changed between load steps; however, doing
        so will not affect which set of solution files are combined. Only the
        last values of FileType and Combine upon leaving the solution processor
        will be used to determine whether the solution files are combined. For
        example, given a two load step solution and FileType = RST, setting
        Combine = NO for the first load step and YES for the second load step
        will cause all sets on the local results files to be combined. If the
        opposite is true (Combine = YES for the first load step and NO for the
        second load step), no results will be combined.

        After using DMPOPTION to suppress file combination, you may find it
        necessary to combine the local files for a specific FileType for use in
        a subsequent analysis. In this case, use the COMBINE command to combine
        local solution files into a single, global file.
        """
        command = f"DMPOPTION,{filetype},{combine}"
        return self.run(command, **kwargs)

    def dspoption(
        self,
        reord_option="",
        memory_option="",
        memory_size="",
        solve_info="",
        **kwargs,
    ):
        """Sets memory option for the distributed sparse solver.

        APDL Command: DSPOPTION

        Parameters
        ----------
        reord_option
            Reordering option:

            DEFAULT - Use the default reordering scheme.

            SEQORDER - Use a sequential equation reordering scheme
                       within the distributed sparse solver. Relative
                       to PARORDER, this option typically results in
                       longer equation ordering times and therefore
                       longer overall solver times. Occasionally,
                       however, this option will produce better
                       quality orderings which decrease the matrix
                       factorization times and improve overall solver
                       performance.

            PARORDER - Use a parallel equation reordering scheme
                       within the distributed sparse solver.  Relative
                       to SEQORDER, this option typically results in
                       shorter equation ordering times and therefore
                       shorter overall solver times. Occasionally,
                       however, this option will produce lower quality
                       orderings which increase the matrix
                       factorization times and degrade overall solver
                       performance.

        memory_option
            Memory allocation option:

            DEFAULT - Use the default memory allocation strategy for
                      the distributed sparse solver.  The default
                      strategy attempts to run in the INCORE memory
                      mode. If there is not enough physical memory
                      available when the solver starts to run in the
                      INCORE memory mode, the solver will then attempt
                      to run in the OUTOFCORE memory mode.

            INCORE - Use a memory allocation strategy in the
                     distributed sparse solver that will attempt to
                     obtain enough memory to run with the entire
                     factorized matrix in memory. This option uses the
                     most amount of memory and should avoid doing any
                     I/O. By avoiding I/O, this option achieves
                     optimal solver performance. However, a
                     significant amount of memory is required to run
                     in this mode, and it is only recommended on
                     machines with a large amount of memory. If the
                     allocation for in-core memory fails, the solver
                     will automatically revert to out-of-core memory
                     mode.

            OUTOFCORE - Use a memory allocation strategy in the
                        distributed sparse solver that will attempt to
                        allocate only enough work space to factor each
                        individual frontal matrix in memory, but will
                        share the entire factorized matrix on
                        disk. Typically, this memory mode results in
                        poor performance due to the potential
                        bottleneck caused by the I/O to the various
                        files written by the solver.

            FORCE - This option, when used in conjunction with the
                    Memory_Size option, allows you to force the
                    distributed sparse solver to run with a specific
                    amount of memory. This option is only recommended
                    for the advanced user who understands distributed
                    sparse solver memory requirements for the problem
                    being solved, understands the physical memory on
                    the system, and wants to control the distributed
                    sparse solver memory usage.

        memory_size
            Initial memory size allocation for the sparse solver in
            MB. The Memory_Size setting should always be well within
            the physical memory available, but not so small as to
            cause the distributed sparse solver to run out of
            memory. Warnings and/or errors from the distributed sparse
            solver will appear if this value is set too low.  If the
            FORCE memory option is used, this value is the amount of
            memory allocated for the entire duration of the
            distributed sparse solver solution.

        solve_info
            Solver output option:

            OFF - Turns off additional output printing from the
                  distributed sparse solver (default).

            PERFORMANCE - Turns on additional output printing from the
                          distributed sparse solver, including a
                          performance summary and a summary of file
                          I/O for the distributed sparse
                          solver. Information on memory usage during
                          assembly of the global matrix (that is,
                          creation of the Jobname.FULL file) is also
                          printed with this option.

        Notes
        -----
        This command controls options related to the distributed sparse solver
        in all analysis types where the distributed sparse solver can be used.

        The amount of memory required for the distributed sparse solver is
        unknown until the matrix structure is preprocessed, including equation
        reordering. The amount of memory allocated for the distributed sparse
        solver is then dynamically adjusted to supply the solver what it needs
        to compute the solution.

        If you have a large memory system, you may want to try selecting the
        INCORE memory mode for larger jobs to improve performance. Also, when
        running the distributed sparse solver with many processors on the same
        machine or on a machine with very slow I/O performance (e.g., slow hard
        drive speed), you may want to try using the INCORE memory mode to
        achieve better performance. However, doing so may require much more
        memory compared to running in the OUTOFCORE memory mode.

        Running with the INCORE memory mode is best for jobs which comfortably
        fit within the limits of the physical memory on a given system. If the
        distributed sparse solver workspace exceeds physical memory size, the
        system will be forced to use virtual memory (or the system page/swap
        file). In this case, it is typically more efficient to run with the
        OUTOFCORE memory mode.
        """
        command = (
            f"DSPOPTION,{reord_option},{memory_option},{memory_size},,,{solve_info}"
        )
        return self.run(command, **kwargs)

    def exbopt(
        self,
        outinv2="",
        outtcms="",
        outsub="",
        outcms="",
        outcomp="",
        outrm="",
        noinv="",
        outele="",
        **kwargs,
    ):
        """Specifies .EXB file output options in a CMS generation pass.

        APDL Command: EXBOPT

        Parameters
        ----------
        outinv2
            Output control for 2nd order invariant:

            * ``"0"`` : Do not output (default).
            * ``"1"`` : Output the second order invariant.

        outtcms
            Output control for .TCMS file:

            * ``"0"`` : Do not output (default).
            * ``"1"`` : Output the .TCMS file.

        outsub
            Output control for .SUB file:

            * ``"0"`` : Do not output (default).
            * ``"1"`` : Output the .SUB file.

        OUTCMS
            Output control for .CMS file:

            * ``"0"`` : Do not output (default).
            * ``"1"`` : Output the .CMS file.

        outcomp
            Output control for node and element component information:

            * ``"0"`` : Do not output any component information.
            * ``"1"`` : Output node component information only.
            * ``"2"`` : Output element component information only.
            * ``"3"`` : Output both node and element component information (default).

        outrm
            Output control for the recovery matrix:

            * ``"0"`` : Do not output (default).
            * ``"1"`` : Output the recovery matrix to file.EXB.
            * ``"2"`` : Output the recovery matrix to a separate file, file_RECOVER.EXB.

        noinv
            Invariant calculation:

            * ``"0"`` : Calculate all invariants (default).
            * ``"1"`` : Suppress calculation of the 1st and 2nd order
              invariants. NOINV = 1 suppresses OUTINV2 = 1.

        OUTELE
        Output control for the element data:

            * ``"0"`` : Do not output (default).
            * ``"1"`` : Output the element data.

        Notes
        -----
        When the body property file (file.EXB) is requested in a CMS
        generation pass (CMSOPT,,,,,,,EXB command), the .TCMS, .SUB, and
        .CMS files are not output by default. Use the EXBOPT command to
        request these files, as needed.

        EXBOPT can also be used to manage some content in the .EXB file
        for improving performance and storage (see the OUTINV2, OUTCOMP,
        OUTRM, NOINV, and OUTELE arguments described above).

        If both recovery matrix output (OUTRM = 1 or 2) and the .TCMS file
        (OUTTCMS = 1) are requested, the .TCMS file writing is turned off
        due to potentially large in-core memory use.

        For more information on how to generate file.EXB, see ANSYS
        Interface to AVL EXCITE in the Mechanical APDL Substructuring
        Analysis Guide
        """
        command = f"EXBOPT,{outinv2},{outtcms},{outsub},{outcms},{outcomp},{outrm},{noinv},{outele}"
        return self.run(command, **kwargs)

    def ematwrite(self, key: str = "", **kwargs) -> Optional[str]:
        """Forces the writing of all the element matrices to File.EMAT.

        APDL Command: EMATWRITE

        Parameters
        ----------
        key
            Write key:

            YES - Forces the writing of the element matrices to
                  File.EMAT even if not normally
                  done.

            NO - Element matrices are written only if required. This
                 value is the default.

        Notes
        -----
        The EMATWRITE command forces ANSYS to write the File.EMAT
        file. The file is necessary if you intend to follow the
        initial load step with a subsequent inertia relief
        calculation (IRLF). If used in the solution
        processor (/SOLU), this command is only valid within the
        first load step.

        This command is also valid in PREP7.
        """
        command = f"EMATWRITE,{key}"
        return self.run(command, **kwargs)

    def eqslv(self, lab="", toler="", mult="", keepfile="", **kwargs):
        """Specifies the type of equation solver.

        APDL Command: EQSLV

        Parameters
        ----------
        lab
            Equation solver type:

            SPARSE - Sparse direct equation solver.  Applicable to
                     real-value or complex-value symmetric and
                     unsymmetric matrices. Available only for STATIC,
                     HARMIC (full method only), TRANS (full method
                     only), SUBSTR, and PSD spectrum analysis types
                     [ANTYPE].  Can be used for nonlinear and linear
                     analyses, especially nonlinear analysis where
                     indefinite matrices are frequently
                     encountered. Well suited for contact analysis
                     where contact status alters the mesh
                     topology. Other typical well-suited applications
                     are: (a) models consisting of shell/beam or
                     shell/beam and solid elements (b) models with a
                     multi-branch structure, such as an automobile
                     exhaust or a turbine fan. This is an alternative
                     to iterative solvers since it combines both speed
                     and robustness. Generally, it requires
                     considerably more memory (~10x) than the PCG
                     solver to obtain optimal performance (running
                     totally in-core). When memory is limited, the
                     solver works partly in-core and out-of-core,
                     which can noticeably slow down the performance of
                     the solver. See the BCSOPTION command for more
                     details on the various modes of operation for
                     this solver.

            This solver can be run in shared memory parallel or
            distributed memory parallel (Distributed ANSYS) mode. When
            used in Distributed ANSYS, this solver preserves all of
            the merits of the classic or shared memory sparse
            solver. The total sum of memory (summed for all processes)
            is usually higher than the shared memory sparse
            solver. System configuration also affects the performance
            of the distributed memory parallel solver. If enough
            physical memory is available, running this solver in the
            in-core memory mode achieves optimal performance. The
            ideal configuration when using the out-of-core memory mode
            is to use one processor per machine on multiple machines
            (a cluster), spreading the I/O across the hard drives of
            each machine, assuming that you are using a high-speed
            network such as Infiniband to efficiently support all
            communication across the multiple machines.  - This solver
            supports use of the GPU accelerator capability.

            JCG - Jacobi Conjugate Gradient iterative equation
                  solver. Available only for STATIC, HARMIC (full
                  method only), and TRANS (full method only) analysis
                  types [ANTYPE]. Can be used for structural, thermal,
                  and multiphysics applications. Applicable for
                  symmetric, unsymmetric, complex, definite, and
                  indefinite matrices.  Recommended for 3-D harmonic
                  analyses in structural and multiphysics
                  applications. Efficient for heat transfer,
                  electromagnetics, piezoelectrics, and acoustic field
                  problems.

            This solver can be run in shared memory parallel or
            distributed memory parallel (Distributed ANSYS) mode. When
            used in Distributed ANSYS, in addition to the limitations
            listed above, this solver only runs in a distributed
            parallel fashion for STATIC and TRANS (full method)
            analyses in which the stiffness is symmetric and only when
            not using the fast thermal option (THOPT). Otherwise, this
            solver runs in shared memory parallel mode inside
            Distributed ANSYS. - This solver supports use of the GPU
            accelerator capability. When using the GPU accelerator
            capability, in addition to the limitations listed above,
            this solver is available only for STATIC and TRANS (full
            method) analyses where the stiffness is symmetric and does
            not support the fast thermal option (THOPT).

            ICCG - Incomplete Cholesky Conjugate Gradient iterative
                   equation solver. Available for STATIC, HARMIC (full
                   method only), and TRANS (full method only) analysis
                   types [ANTYPE].  Can be used for structural,
                   thermal, and multiphysics applications, and for
                   symmetric, unsymmetric, complex, definite, and
                   indefinite matrices. The ICCG solver requires more
                   memory than the JCG solver, but is more robust than
                   the JCG solver for ill-conditioned matrices.

            This solver can only be run in shared memory parallel
            mode. This is also true when the solver is used inside
            Distributed ANSYS. - This solver does not support use of
            the GPU accelerator capability.

            QMR - Quasi-Minimal Residual iterative equation
                  solver. Available for the HARMIC (full method only)
                  analysis type [ANTYPE]. Can be used for
                  high-frequency electromagnetic applications, and for
                  symmetric, complex, definite, and indefinite
                  matrices. The QMR solver is more stable than the
                  ICCG solver.

            This solver can only be run in shared memory parallel
            mode. This is also true when the solver is used inside
            Distributed ANSYS. - This solver does not support use of
            the GPU accelerator capability.

            PCG - Preconditioned Conjugate Gradient iterative equation
                  solver (licensed from Computational Applications and
                  Systems Integration, Inc.).  Requires less disk file
                  space than SPARSE and is faster for large
                  models. Useful for plates, shells, 3-D models, large
                  2-D models, and other problems having symmetric,
                  sparse, definite or indefinite matrices for
                  nonlinear analysis.  Requires twice as much memory
                  as JCG. Available only for analysis types [ANTYPE]
                  STATIC, TRANS (full method only), or MODAL (with PCG
                  Lanczos option only). Also available for the use
                  pass of substructure analyses (MATRIX50). The PCG
                  solver can robustly solve equations with constraint
                  equations (CE, CEINTF, CPINTF, and CERIG).  With
                  this solver, you can use the MSAVE command to obtain
                  a considerable memory savings.

            The PCG solver can handle ill-conditioned problems by
            using a higher level of difficulty (see
            PCGOPT). Ill-conditioning arises from elements with high
            aspect ratios, contact, and plasticity. - This solver can
            be run in shared memory parallel or distributed memory
            parallel (Distributed ANSYS) mode. When used in
            Distributed ANSYS, this solver preserves all of the merits
            of the classic or shared memory PCG solver. The total sum
            of memory (summed for all processes) is about 30% more
            than the shared memory PCG solver.

        toler
            Iterative solver tolerance value. Used only with the
            Jacobi Conjugate Gradient, Incomplete Cholesky Conjugate
            Gradient, Pre- conditioned Conjugate Gradient, and
            Quasi-Minimal Residual equation solvers. For the PCG
            solver, the default is 1.0E-8. The value 1.0E-5 may be
            acceptable in many situations. When using the PCG Lanczos
            mode extraction method, the default solver tolerance value
            is 1.0E-4. For the JCG and ICCG solvers with symmetric
            matrices, the default is 1.0E-8. For the JCG and ICCG
            solvers with unsymmetric matrices, and for the QMR solver,
            the default is 1.0E-6. Iterations continue until the SRSS
            norm of the residual is less than TOLER times the norm of
            the applied load vector. For the PCG solver in the linear
            static analysis case, 3 error norms are used. If one of
            the error norms is smaller than TOLER, and the SRSS norm
            of the residual is smaller than 1.0E-2, convergence is
            assumed to have been reached. See Iterative Solver in the
            Mechanical APDL Theory Reference for details.

        mult
            Multiplier (defaults to 2.5 for nonlinear analyses; 1.0
            for linear analyses) used to control the maximum number of
            iterations performed during convergence calculations. Used
            only with the Pre- conditioned Conjugate Gradient equation
            solver (PCG). The maximum number of iterations is equal to
            the multiplier (MULT) times the number of degrees of
            freedom (DOF). If MULT is input as a negative value, then
            the maximum number of iterations is equal to abs(MULT).
            Iterations continue until either the maximum number of
            iterations or solution convergence has been reached. In
            general, the default value for MULT is adequate for
            reaching convergence.  However, for ill-conditioned
            matrices (that is, models containing elements with high
            aspect ratios or material type discontinuities) the
            multiplier may be used to increase the maximum number of
            iterations used to achieve convergence.  The recommended
            range for the multiplier is 1.0 MULT 3.0.  Normally, a
            value greater than 3.0 adds no further benefit toward
            convergence, and merely increases time requirements.  If
            the solution does not converge with 1.0 MULT 3.0, or in
            less than 10,000 iterations, then convergence is highly
            unlikely and further examination of the model is
            recommended. Rather than increasing the default value of
            MULT, consider increasing the level of difficulty
            (Lev_Diff) on the PCGOPT command.

        keepfile
            Determines whether files from a SPARSE solver run should be deleted
            or retained. Applies only to Lab = SPARSE for static and full
            transient analyses.
        """
        return self.run(f"EQSLV,{lab},{toler},{mult},,{keepfile}", **kwargs)

    def eresx(self, key="", **kwargs):
        """Specifies extrapolation of integration point results.

        APDL Command: ERESX

        Parameters
        ----------
        key
            Extrapolation key:

            DEFA - If element is fully elastic (no active plasticity, creep, or swelling
                   nonlinearities), extrapolate the integration point results
                   to the nodes.  If any portion of the element is plastic (or
                   other active material nonlinearity), copy the integration
                   point results to the nodes (default).

            YES - Extrapolate the linear portion of the integration point results to the nodes
                  and copy the nonlinear portion (for example, plastic
                  strains).

            NO - Copy the integration point results to the nodes.

        Notes
        -----
        Specifies whether the solution results at the element integration
        points are extrapolated or copied to the nodes for element and nodal
        postprocessing. The structural stresses, elastic and thermal strains,
        field gradients, and fluxes are affected.  Nonlinear data (plastic,
        creep, and swelling strains) are always copied to the nodes, never
        extrapolated. For shell elements, ERESX applies only to integration
        point results in the in-plane directions.

        This command is also valid in PREP7.
        """
        command = f"ERESX,{key}"
        return self.run(command, **kwargs)

    def escheck(
        self, sele: str = "", levl: str = "", defkey: MapdlInt = "", **kwargs
    ) -> Optional[str]:
        """Perform element shape checking for a selected element set.

        APDL Command: ESCHECK

        Parameters
        ----------
        sele
            Specifies whether to select elements for checking:

            (blank) - List all warnings/errors from element shape
            checking.

            ESEL - Select the elements based on the .Levl criteria
            specified below.

        levl
            WARN - Select elements producing warning and error messages.

            ERR - Select only elements producing error messages (
            default).

        defkey
            Specifies whether check should be performed on deformed
            element
            shapes. .

            0 - Do not update node coordinates before performing
            shape checks (default).

            1 - Update node coordinates using the current set of
            deformations in the database.

        Notes
        -----
        Shape checking will occur according to the current SHPP
        settings. Although ESCHECK is valid in all processors,
        Defkey  uses the current results in the database. If no
        results are available a warning will be issued.

        This command is also valid in PREP7, SOLUTION and POST1.
        """
        command = f"ESCHECK,{sele},{levl},{defkey}"
        return self.run(command, **kwargs)

    def essolv(
        self,
        electit="",
        strutit="",
        dimn="",
        morphopt="",
        mcomp="",
        xcomp="",
        electol="",
        strutol="",
        mxloop="",
        ruseky="",
        restky="",
        eiscomp="",
        **kwargs,
    ):
        """Performs a coupled electrostatic-structural analysis.

        APDL Command: ESSOLV

        Parameters
        ----------
        electit
            Title of the electrostatics physics file as assigned by the PHYSICS
            command.

        strutit
            Title of the structural physics file as assigned by the PHYSICS
            command.

        dimn
            Model dimensionality (a default is not allowed):

            2 - 2-D model.

            3 - 3-D model.

        morphopt
            Morphing option:

            <0 - Do not perform any mesh morphing or remeshing.

            0 - Remesh the non-structural regions for each recursive loop only if mesh morphing
                fails (default).

            1 - Remesh the non-structural regions each recursive loop and bypass mesh morphing.

            2 - Perform mesh morphing only, do not remesh any non-structural regions.

        mcomp
            Component name of the region to be morphed.  For 2-D models, the
            component may be elements or areas.  For 3-D models, the component
            may be elements or volumes.  A component must be specified. You
            must enclose name-strings in single quotes in the ESSOLV command
            line.

        xcomp
            Component name of entities excluded from morphing.  In the 2-D
            case, it is the component name for the lines excluded from
            morphing.  In the 3-D case, it is component name for the areas
            excluded from morphing.  Defaults to exterior non-shared entities
            (see the DAMORPH, DVMORPH, and DEMORPH commands). You must enclose
            name-strings in single quotes in the ESSOLV command line.

        electol
            Electrostatic energy convergence tolerance.  Defaults to .005 (.5%)
            of the value computed from the previous iteration.  If less than
            zero, the convergence criteria based on electrostatics results is
            turned off.

        strutol
            Structural maximum displacement convergence tolerance.  Defaults to
            .005 (.5%) of the value computed from the previous iteration.  If
            less than zero, the convergence criteria base on structural results
            is turned off.

        mxloop
            Maximum number of allowable solution recursive loops.  A single
            pass through both an electrostatics and structural analysis
            constitutes one loop.  Defaults to 100.

        ruseky
            Reuse flag option:

            1 - Assumes initial run of ESSOLV using base geometry for
                the first electrostatics solution.

            >1 - Assumes ESSOLV run is a continuation of a previous
                 ESSOLV run, whereby the morphed geometry is used for
                 the initial electrostatic simulation.

        restky
            Structural restart key.

            0 - Use static solution option for structural solution.

            1 - Use static restart solution option for structural solution.

        eiscomp
            Element component name for elements containing initial stress data
            residing in file jobname.ist. The initial stress data must be
            defined prior to issuing ESSOLV (see INISTATE command).

        Notes
        -----
        ESSOLV invokes an ANSYS macro which automatically performs a coupled
        electrostatic-structural analysis.

        The macro displays periodic updates of the convergence.

        If non-structural regions are remeshed during the analysis, boundary
        conditions and loads applied to nodes and elements will be lost.
        Accordingly, it is better to assign boundary conditions and loads to
        the solid model.

        Use RUSEKY > 1 for solving multiple ESSOLV simulations for different
        excitation levels (i.e., for running a voltage sweep). Do not issue the
        SAVE command to save the database between ESSOLV calls.

        For nonlinear structural solutions, the structural restart option
        (RESTKY = 1) may improve solution time by starting from the previous
        converged structural solution.

        For solid elements, ESSOLV automatically detects the air-structure
        interface and applies a Maxwell surface flag on the electrostatic
        elements. This flag is used to initiate the transfer for forces from
        the electrostatic region to the structure. When using the ESSOLV
        command with structural shell elements (for example, SHELL181), you
        must manually apply the Maxwell surface flag on all air elements
        surrounding the shells before writing the final electrostatic physics
        file. Use the SFA command to apply the Maxwell surface flag to the
        areas representing the shell elements; doing so ensures that the air
        elements next to both sides of the shells receive the Maxwell surface
        flag.

        If lower-order structural solids or shells are used, set KEYOPT(7) = 1
        for the electrostatic element types to ensure the correct transfer of
        forces.

        Information on creating the initial stress file is documented in the
        Loading chapter in the Basic Analysis Guide.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"ESSOLV,{electit},{strutit},{dimn},{morphopt},{mcomp},{xcomp},{electol},{strutol},{mxloop},,{ruseky},{restky},{eiscomp}"
        return self.run(command, **kwargs)

    def expass(self, key="", **kwargs):
        """Specifies an expansion pass of an analysis.

        APDL Command: EXPASS

        Parameters
        ----------
        key
            Expansion pass key:

            OFF - No expansion pass will be performed (default).

            ON - An expansion pass will be performed.

        Notes
        -----
        Specifies that an expansion pass of a modal, substructure, buckling,
        transient, or harmonic analysis is to be performed.

        Note:: : This separate solution pass requires an explicit FINISH to
        preceding analysis and reentry into SOLUTION.

        This command is also valid in PREP7.
        """
        command = f"EXPASS,{key}"
        return self.run(command, **kwargs)

    def gauge(self, opt="", freq="", **kwargs):
        """Gauges the problem domain for a magnetic edge-element formulation.

        APDL Command: GAUGE

        Parameters
        ----------
        opt
            Type of gauging to be performed:

            ON - Perform tree gauging of the edge values (default).

            OFF - Gauging is off. (You must specify custom gauging via APDL specifications.)

            STAT - Gauging status (returns the current Opt and FREQ values)

        freq
            The following options are valid when Opt = ON:

            0 - Generate tree-gauging information once, at the first load step. Gauging data is
                retained for subsequent load steps. (This behavior is the
                default.)

            1 - Repeat gauging for each load step. Rewrites the gauging information at each
                load step to accommodate changing boundary conditions on the AZ
                degree of freedom (for example, adding or deleting AZ
                constraints via the D or CE commands).

        Notes
        -----
        The GAUGE command controls the tree-gauging procedure required for
        electromagnetic analyses using an edge-based magnetic formulation
        (elements SOLID236 and SOLID237).

        Gauging occurs at the solver level for each solution (SOLVE). It sets
        additional zero constraints on the edge-flux degrees of freedom AZ to
        produce a unique solution; the additional constraints are removed after
        solution.

        Use the FREQ option to specify how the command generates gauging
        information for multiple load steps.

        Access the gauging information via the _TGAUGE component of gauged
        nodes. The program creates and uses this component internally to remove
        and reapply the AZ constraints required by gauging. If FREQ = 0, the
        _TGAUGE component is created at the first load step and is used to
        reapply the tree gauge constraints at subsequent load steps. If FREQ =
        1, the tree-gauging information and the _TGAUGE component are generated
        at every load step

        If gauging is turned off (GAUGE,OFF), you must specify your own gauging
        at the APDL level.

        This command is also valid in PREP7.
        """
        command = f"GAUGE,{opt},{freq}"
        return self.run(command, **kwargs)

    def gmatrix(self, symfac="", condname="", numcond="", matrixname="", **kwargs):
        """Performs electric field solutions and calculates the self and mutual

        APDL Command: GMATRIX
        conductance between multiple conductors.

        Parameters
        ----------
        symfac
            Geometric symmetry factor.  Conductance values are scaled by this
            factor which represents the fraction of the total device modeled.
            Defaults to 1.

        condname
            Alphanumeric prefix identifier used in defining named conductor
            components.

        numcond
            Total number of components.  If a ground is modeled, it is to be
            included as a component.

        matrixname
            Array name for computed conductance matrix.  Defaults to GMATRIX.

        Notes
        -----
        To invoke the GMATRIX macro, the exterior nodes of each conductor must
        be grouped into individual components using the CM command.  Each set
        of  independent components is assigned a component name with a common
        prefix followed by the conductor number.  A conductor system with a
        ground must also include the ground nodes as a component.  The ground
        component is numbered last in the component name sequence.

        A ground conductance matrix relates current to a voltage vector.  A
        ground matrix cannot be applied to a circuit modeler.  The lumped
        conductance matrix is a combination of  lumped "arrangements" of
        voltage differences between conductors.  Use the lumped conductance
        terms in a circuit modeler to represent conductances between
        conductors.

        Enclose all name-strings in single quotes in the GMATRIX command line.

        GMATRIX works with the following elements:

        SOLID5 (KEYOPT(1) = 9)

        SOLID98 (KEYOPT(1) = 9)

        LINK68

        PLANE230

        SOLID231

        SOLID232

        This command is available from the menu path shown below only if
        existing results are available.

        This command does not support multiframe restarts

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"GMATRIX,{symfac},{condname},{numcond},,{matrixname}"
        return self.run(command, **kwargs)

    def lanboption(self, strmck="", **kwargs):
        """Specifies Block Lanczos eigensolver options.

        APDL Command: LANBOPTION

        strmck
            Controls whether the Block Lanczos eigensolver will perform a
            Sturm sequence check:

            * ``"OFF"`` : Do not perform the Sturm sequence check
              (default).

            * ``"ON"`` : Perform a Sturm sequence check. This requires
              additional matrix factorization (which can be expensive),
              but does help ensure that no modes are missed in the
              specified range.

        Notes
        -----
        LANBOPTION specifies options to be used with the Block Lanczos
        eigensolver during an eigenvalue buckling analysis (BUCOPT,LANB)
        or a modal analysis (MODOPT,LANB).

        By default the sturm sequence check is off for the Block Lanczos
        eigensolver when it is used in a modal analysis, and on when it is
        used in a buckling analysis.

        """
        return self.run(f"LANBOPTION,{strmck}", **kwargs)

    def lumpm(self, key="", **kwargs):
        """Specifies a lumped mass matrix formulation.

        APDL Command: LUMPM

        Parameters
        ----------
        key
            Formulation key:

            OFF - Use the element-dependent default mass matrix formulation (default).

            ON - Use a lumped mass approximation.

        Notes
        -----
        This command is also valid in PREP7.  If used in SOLUTION, this command
        is valid only within the first load step.
        """
        command = f"LUMPM,{key}"
        return self.run(command, **kwargs)

    def moddir(self, key="", directory="", fname="", **kwargs):
        """Activates the remote read-only modal files usage.

        APDL Command: MODDIR

        Parameters
        ----------
        key
            Key to activate the remote modal files usage

            * ``"1 (ON or YES)"`` : The program performs the analysis
              using remote modal files. The files are read-only.

            * ``"0 (OFF or NO)"`` : The program performs the analysis
              using modal files located in the working directory
              (default).

        directory
            Directory path (248 characters maximum). The directory
            contains the modal analysis files.  The directory path
            defaults to the current working directory.

        fname
            File name (no extension or directory path) for the modal
            analysis files.  The file name defaults to the current
            Jobname.

        Notes
        -----
        Only applies to spectrum analyses (ANTYPE,SPECTR).

        Using the default for both the directory path (Directory) and the
        file name (Fname) is not valid. At least one of these values must
        be specified.

        The MODDIR command must be issued during the first solution and at
        the beginning of the solution phase (before LVSCALE in
        particular).

        Remote modal files usage is not supported when mode file reuse is
        activated (modeReuseKey = YES on SPOPT).
        """
        return self.run(f"MODDIR,{key},{directory},{fname}", **kwargs)

    def monitor(self, var="", node="", lab="", **kwargs):
        """Controls contents of three variable fields in nonlinear solution

        APDL Command: MONITOR
        monitor file.

        Parameters
        ----------
        var
            One of three variable field numbers in the monitor file whose
            contents can be specified by the Lab field.  Valid arguments are
            integers 1, 2, or 3. See Notes section for default values.

        node
            The node number for which information is monitored in the specified
            VAR field.  In the GUI, if Node = P, graphical picking is enabled.
            If blank, the monitor file lists the maximum value of the specified
            quantity (Lab field) for the entire structure.

        lab
            The solution quantity to be monitored in the specified VAR field.
            Valid labels for solution quantities are UX, UY, and UZ
            (displacements); ROTX, ROTY, and ROTZ (rotations); and TEMP
            (temperature).  Valid labels for reaction force are FX, FY, and FZ
            (structural force) and MX, MY, and MZ (structural moment).  Valid
            label for heat flow rate is HEAT. For defaults see the Notes
            section.

        Notes
        -----
        The monitor file always has an extension of .mntr, and takes its file
        name from the specified Jobname.  If no Jobname is specified, the file
        name defaults to file.

        You must issue this command once for each solution quantity you want to
        monitor at a specified node at each load step. You cannot monitor a
        reaction force during a linear analysis. The variable field contents
        can be redefined at each load step by reissuing the command. The
        monitored quantities are appended to the file for each load step.

        Reaction forces reported in the monitor file may be incorrect if the
        degree of freedom of the specified node is involved in externally
        defined coupling (CP command) or constraint equations (CE command), or
        if the program has applied constraint equations internally to the node.

        The following example shows the format of a monitor file.  Note that
        the file only records the solution substep history when a substep is
        convergent.

        The following details the contents of the various fields in the monitor
        file:

        The current load step number.

        The current substep (time step) number.

        The number of attempts made in solving the current substep.  This
        number is equal to the number of failed attempts (bisections) plus one
        (the successful attempt).

        The number of iterations used by the last successful attempt.

        Total cumulative number of iterations (including each iteration used by
        a bisection).

        :

        Time or load factor increments for the current substep.

        Total time (or load factor) for the last successful attempt in the
        current substep.

        Variable field 1.  In this example, the field is reporting the UZ
        value.  By default, this field lists the CPU time used up to (but not
        including) the current substep.

        Variable field 2.  In this example, the field is reporting the MZ
        value.  By default, this field lists the maximum displacement in the
        entire structure.

        Variable field 3.  By default (and in the example), this field reports
        the maximum equivalent plastic strain increment in the entire
        structure.
        """
        command = f"MONITOR,{var},{node},{lab}"
        return self.run(command, **kwargs)

    def msave(self, key="", **kwargs):
        """Sets the solver memory saving option. This option only applies to the

        APDL Command: MSAVE
        PCG solver (including PCG Lanczos).

        Parameters
        ----------
        key
            Activation key:

            0 or OFF - Use global assembly for the stiffness matrix (and mass matrix, when using PCG
                       Lanczos) of the entire model.

            1 or ON - Use an element-by-element approach when possible to save memory during the
                      solution. In this case, the global stiffness (and mass)
                      matrix is not assembled; element stiffness (and mass) is
                      regenerated during PCG or PCG Lanczos iterations.

        Notes
        -----
        MSAVE,ON only applies to and is the default for parts of the model
        using the following element types with linear material properties that
        meet the conditions listed below.

        SOLID186 (Structural Solid only)

        SOLID187

        The following conditions must also be true:

        The PCG solver has been specified.

        Small strains are assumed (NLGEOM,OFF).

        No prestress effects (PSTRES) are included.

        All nodes on the supported element types must be defined (i.e., the
        midside nodes cannot be removed using the EMID command).

        For elements with thermally dependent material properties, MSAVE,ON
        applies only to elements with uniform temperatures prescribed.

        The default element coordinate system must be used.

        If you manually force MSAVE,ON by including it in the input file, the
        model can include the following additional conditions:

        The analysis can be a modal analysis using the PCG Lanczos method
        (MODOPT,LANPCG).

        Large deflection effects (NLGEOM,ON) are included.

        SOLID185 (brick shapes and KEYOPT(2) = 3 only) elements can be
        included.

        All other element types or other parts of the model that don't meet the
        above criteria will be solved using global assembly (MSAVE,OFF). This
        command can result in memory savings of up to 70 percent over the
        global assembly approach for the part of the model that meets the
        criteria. Depending on the hardware (e.g., processor speed, memory
        bandwidth, etc.), the solution time may increase or decrease when this
        feature is used.

        This memory-saving feature runs in parallel when multiple processors
        are used with the /CONFIG command or with Distributed ANSYS. The gain
        in performance with using multiple processors with this feature turned
        on should be similar to the default case when this feature is turned
        off. Performance also improves when using the uniform reduced
        integration option for SOLID186 elements.

        This command does not support the layered option of the SOLID185 and
        SOLID186 elements.

        When using MSAVE,ON with the PCGOPT command, note the following
        restrictions:

        For static and modal analyses, MSAVE,ON is not valid when using a
        Lev_Diff value of 5 on the PCGOPT command; Lev_Diff will automatically
        be reset to 2.

        For modal analyses, MSAVE,ON is not valid with the StrmCk option of the
        PCGOPT command; Strmck will be set to OFF.

        For all analysis types, MSAVE,ON is not valid when the Lagrange
        multiplier option (LM_Key) of the PCGOPT command is set to ON; the
        MSAVE activation key will be set to OFF.

        For linear perturbation static and modal analyses, MSAVE,ON is not
        valid; the MSAVE activation key will be set to OFF.

        When using MSAVE,ON for modal analyses, no .FULL file will be created.
        The .FULL file may be necessary for subsequent analyses (e.g.,
        harmonic, transient mode-superposition, or spectrum analyses). To
        generate the .FULL file, rerun the modal analysis using the WRFULL
        command.
        """
        command = f"MSAVE,{key}"
        return self.run(command, **kwargs)

    def msolve(self, numslv="", nrmtol="", nrmchkinc="", **kwargs):
        """Starts multiple solutions for random acoustics analysis with diffuse

        APDL Command: MSOLVE
        sound field.

        Parameters
        ----------
        numslv
            Number of multiple solutions (load steps) corresponding to the
            number of samplings. Default = 1.

        Notes
        -----
        The MSOLVE command starts multiple solutions (load steps) for random
        acoustics analysis with multiple samplings.

        The process is controlled by the norm convergence tolerance NRMTOL or
        the number of multiple solutions NUMSLV (if the solution steps reach
        the defined number).

        The program checks the norm convergence by comparing two averaged sets
        of radiated sound powers with the interval NRMCHKINC over the frequency
        range. For example, if NRMCHKINC = 5, the averaged values from 5
        solutions are compared with the averaged values from 10 solutions, then
        the averaged values from 10 solutions are compared with the averaged
        values from 15 solutions, and so on.

        The incident diffuse sound field is defined via the DFSWAVE command.

        The average result of multiple solutions with different samplings is
        calculated via the PLST command.
        """
        command = f"MSOLVE,{numslv},{nrmtol},{nrmchkinc}"
        return self.run(command, **kwargs)

    def opncontrol(self, lab="", value="", numstep="", **kwargs):
        """Sets decision parameter for automatically increasing the time step

        APDL Command: OPNCONTROL
        interval.

        Parameters
        ----------
        lab
            DOF

            DOF  - Degree-of-freedom label used to base a decision for increasing the time step
                   (substep) interval in a nonlinear or transient analysis.
                   The only DOF label currently supported is TEMP.

            OPENUPFACTOR  - Factor for increasing the time step interval. Specify when AUTOTS,ON is issued
                            and specify a VALUE > 1.0 (up to 10.0). The default
                            VALUE = 1.5 (except for thermal analysis, where it
                            is 3.0). Generally, VALUE > 3.0 is not recommended.

        value, numstep
            Two values used in the algorithm for determining if the time step
            interval can be increased. Valid only when Lab = DOF.

        Notes
        -----
        This command is available only for nonlinear or full transient
        analysis.
        """
        command = f"OPNCONTROL,{lab},{value},{numstep}"
        return self.run(command, **kwargs)

    def outaero(self, sename="", timeb="", dtime="", **kwargs):
        """Outputs the superelement matrices and load vectors to formatted files

        APDL Command: OUTAERO
        for aeroelastic analysis.

        Parameters
        ----------
        sename
            Name of the superelement that models the wind turbine supporting
            structure. Defaults to the current Jobname.

        timeb
            First time at which the load vector is formed (defaults to be read
            from SENAME.sub).

        dtime
            Time step size of the load vectors (defaults to be read from
            SENAME.sub).

        Notes
        -----
        Both TIMEB and DTIME must be blank if the time data is to be read from
        the SENAME.sub file.

        The matrix file (SENAME.SUB) must be available from the substructure
        generation run before issuing this command. This superelement that
        models the wind turbine supporting structure must contain only one
        master node with six freedoms per node: UX, UY, UZ, ROTX, ROTY, ROTZ.
        The master node represents the connection point between the turbine and
        the supporting structure.

        This command will generate four files that are exported to the
        aeroelastic code for integrated wind turbine analysis. The four files
        are Jobname.GNK for the generalized stiffness matrix, Jobname.GNC for
        the generalized damping matrix, Jobname.GNM for the generalized mass
        matrix and Jobname.GNF for the generalized load vectors.

        For detailed information on how to perform a wind coupling analysis,
        see Coupling to External Aeroelastic Analysis of Wind Turbines in the
        Mechanical APDL Advanced Analysis Guide.
        """
        command = f"OUTAERO,{sename},{timeb},{dtime}"
        return self.run(command, **kwargs)

    def ovcheck(self, method="", frequency="", set_="", **kwargs):
        """Checks for overconstraint among constraint equations and Lagrange

        APDL Command: OVCHECK
        multipliers.

        Parameters
        ----------
        method
            Method used to determine which slave DOFs will be eliminated:

            TOPO - Topological approach (default). This method only works with constraint
                   equations; it does not work with Lagrange multipliers.

            ALGE - Algebraic approach.

            NONE - Do not use overconstraint detection logic.

        frequency
            Frequency of overconstraint detection for static or full transient
            analyses:

            ITERATION - For all equilibrium iterations (default).

            SUBSTEP - At the beginning of each substep.

            LOADSTEP - At the beginning of each load step.

        set\_
            Set of equations:

            All - Check for overconstraint between all constraint equations (default).

            LAG - Check for overconstraint only on the set of equations that involves Lagrange
                  multipliers. This is faster than checking all sets,
                  especially when the model contains large MPC bonded contact
                  pairs.

        Notes
        -----
        The OVCHECK command checks for overconstraint among the constraint
        equations (CE/CP) and the Lagrange multipliers for the globally
        assembled stiffness matrix. If overconstrained constraint equations or
        Lagrange multipliers are detected, they are automatically removed from
        the system of equations.

        The constraint equations that are identified as redundant are removed
        from the system and printed to the output file. It is very important
        that you check the removed equations—they may lead to convergence
        issues, especially for nonlinear analyses.

        The Frequency  and Set arguments are active only for the topological
        method (Method = TOPO). If you do not issue the OVCHECK command,
        overconstraint detection is performed topologically, and the slave DOFs
        are also determined topologically.

        Overconstraint detection slows down the run. We recommend using it to
        validate that your model does not contain any overconstraints. Then,
        you can switch back to the default method (no OVCHECK command is
        needed).

        As an example, consider the redundant set of constraint equations
        defined below:

        Equation number 2 will be removed by the overconstraint detection
        logic. However, this is an arbitrary decision since equation number 1
        could be removed instead. This is an important choice as the constant
        term is not the same in these two constraint equations. Therefore, you
        must check the removed constraint equations carefully.

        For detailed information on the topological and algebraic methods of
        overconstraint detection, see Constraints: Automatic Selection of Slave
        DOFs  in the Mechanical APDL Theory Reference
        """
        command = f"OVCHECK,{method},{frequency},{set_}"
        return self.run(command, **kwargs)

    def pcgopt(
        self,
        lev_diff="",
        reduceio="",
        strmck="",
        wrtfull="",
        memory="",
        lm_key="",
        **kwargs,
    ):
        """Controls PCG solver options.

        APDL Command: PCGOPT

        Parameters
        ----------
        lev_diff
            Indicates the level of difficulty of the analysis. Valid
            settings are AUTO or 0 (default), 1, 2, 3, 4, or 5. This
            option applies to both the PCG solver when used in static
            and full transient analyses and to the PCG Lanczos method
            in modal analyses. Use AUTO to let ANSYS automatically
            choose the proper level of difficulty for the model. Lower
            values (1 or 2) generally provide the best performance for
            well-conditioned problems. Values of 3 or 4 generally
            provide the best performance for ill-conditioned problems;
            however, higher values may increase the solution time for
            well-conditioned problems. Higher level-of-difficulty
            values typically require more memory. Using the highest
            value of 5 essentially performs a factorization of the
            global matrix (similar to the sparse solver) and may
            require a very large amount of memory. If necessary, use
            Memory to reduce the memory usage when using Lev_Diff = 5.
            Lev_Diff = 5 is generally recommended for small- to
            medium-sized problems when using the PCG Lanczos mode
            extraction method.

        reduceio
            Controls whether the PCG solver will attempt to reduce I/O
            performed during equation solution:

            AUTO - Automatically chooses whether to reduce I/O or not
            (default).

            YES - Reduces I/O performed during equation solution in
            order to reduce total solver time.

            NO  - Does NOT reduce I/O performed during equation solution.

        strmck
            Controls whether or not a Sturm sequence check is performed:

            OFF - Does NOT perform Sturm sequence check (default).

            ON - Performs Sturm sequence check

        wrtfull
            Controls whether or not the .FULL file is written.

            ON - Write .FULL file (default)

            OFF - Do not write .FULL file.

        memory
            Controls whether to run using in-core or out-of-core mode
            when using Lev_Diff = 5.

            AUTO - Automatically chooses which mode to use (default).

            INCORE - Run using in-core mode.

            OOC - Run using out-of-core mode.

        lm_key
            Controls use of the PCG solver for MPC184 Lagrange
            multiplier method elements. This option applies only to
            the PCG solver when used in static and full transient
            analyses.

            OFF - Do not use the PCG solver for the MPC184 Lagrange
            multiplier method (default).

            ON - Allow use of the PCG solver for the MPC184 Lagrange
            multiplier method.

        Notes
        -----
        ReduceIO works independently of the MSAVE command in the PCG
        solver.  Setting ReduceIO to YES can significantly increase
        the memory usage in the PCG solver.

        To minimize the memory used by the PCG solver with respect to
        the Lev_Diff option only, set Lev_Diff = 1 if you do not have
        sufficient memory to run the PCG solver with Lev_Diff = AUTO.

        The MSAVE,ON command is not valid when using Lev_Diff = 5. In
        this case, the Lev_Diff value will automatically be reset to
        2. The MSAVE,ON command is also not valid with the StrmCk
        option. In this case, StrmCk will be set to OFF.

        Distributed ANSYS Restriction: The Memory option and the
        LM_Key option are not supported in Distributed ANSYS.
        """
        command = f"PCGOPT,{lev_diff},,{reduceio},{strmck},{wrtfull},{memory},{lm_key}"
        return self.run(command, **kwargs)

    def perturb(self, type_="", matkey="", contkey="", loadcontrol="", **kwargs):
        """Sets linear perturbation analysis options.

        APDL Command: PERTURB

        Parameters
        ----------
        type\_
            Type of linear perturbation analysis to be performed:

            STATIC - Perform a linear perturbation static analysis.

            MODAL - Perform a linear perturbation modal analysis.

            BUCKLE - Perform a linear perturbation eigenvalue buckling analysis.

            HARMONIC - Perform a linear perturbation full harmonic analysis.

            SUBSTR - Perform a linear perturbation substructure generation pass.

            OFF - Do not perform a linear perturbation analysis (default).

        matkey
            Key for specifying how the linear perturbation analysis uses
            material properties, valid for all structural elements except
            contact elements. For more information, see Linear Perturbation
            Analysis in the Mechanical APDL Theory Reference.

            AUTO - The program selects the material properties for the linear perturbation
                   analysis automatically (default). The materials are handled
                   in the following way:

            For pure linear elastic materials used in the base analysis, the same properties are used in the linear perturbation analysis. - For hyperelastic materials used in the base analysis, the material properties
                              are assumed to be linear elastic in the linear
                              perturbation analysis. The material property data
                              (or material Jacobian) is obtained based on the
                              tangent of the hyperelastic material's
                              constitutive law at the point where restart
                              occurs.

            For any nonlinear materials other than hyperelastic materials used in the base analysis, the material properties are assumed to be linear elastic in the linear perturbation analysis. The material data is the same as the linear portion of the nonlinear materials (that is, the parts defined by MP commands). - For COMBIN39, the stiffness is that of the first segment of the force-
                              deflection curve.

            TANGENT - Use the tangent (material Jacobian) on the material constitutive curve as the
                      material property. The material property remains linear
                      in the linear perturbation analysis and is obtained at
                      the point of the base analysis where restart occurs. The
                      materials are handled in the following way:

            For pure linear elastic materials used in the base analysis, the same properties are used in the linear perturbation analysis. Because the material constitutive curve is linear, the tangent is the same as the base analysis.  - For hyperelastic materials used in the base analysis, the program uses the same
                              tangent as that used for MatKey = AUTO, and the
                              results are therefore identical.

            For any nonlinear materials other than hyperelastic materials used in the base analysis, the material properties are obtained via the material tangent on the material constitutive curve at the restart point of the base analysis.  - The materials and properties typically differ from Matkey = AUTO, but it is
                              possible the results could be identical or very
                              similar if a.) the material is elasto-plastic
                              rate-independent and is unloading (or has neutral
                              loading) at the restart point, or b.) the
                              material is rate-dependent, depending on the
                              material properties and loading conditions.

            For COMBIN39, the stiffness is equal to the tangent of the current segment of the force-deflection curve. - In a modal restart solution that follows a linear perturbation modal analysis,
                              the TANGENT option is overridden by the AUTO
                              option and linear material properties are used
                              for stress calculations in the modal restart. See
                              the discussion in the Notes for more information.

        contkey
            Key that controls contact status for the linear perturbation
            analysis. This key controls all contact elements (TARGE169,
            TARGE170, and CONTA171 through CONTA178) globally for all contact
            pairs. Alternatively, contact status can be controlled locally per
            contact pair by using the CNKMOD command. Note that the contact
            status from the base analysis solution is always adjusted by the
            local contact controls specified by CNKMOD first and then modified
            by the global sticking or bonded control (ContKey = STICKING or
            BONDED). The tables in the Notes section show how the contact
            status is adjusted by CNKMOD and/or the ContKey setting.

            CURRENT - Use the current contact status from the restart
                      snapshot (default). If the previous run is
                      nonlinear, then the nonlinear contact status at
                      the point of restart is frozen and used
                      throughout the linear perturbation analysis.

            STICKING - For frictional contact pairs (MU > 0), use
                       sticking contact (e.g., ``MU*KN`` for tangential
                       contact stiffness) everywhere the contact state
                       is closed (i.e., status is sticking or
                       sliding).  This option only applies to contact
                       pairs that are in contact and have a frictional
                       coefficient MU greater than zero. Contact pairs
                       without friction (MU = 0) and in a sliding
                       state remain free to slide in the linear
                       perturbation analysis.

            BONDED - Any contact pairs that are in the closed
                     (sticking or sliding) state are moved to bonded
                     (for example, KN for both normal and tangential
                     contact stiffness). Contact pairs that have a
                     status of far-field or near-field remain open.

        loadcontrol
            Key that controls how the load vector of {Fperturbed} is
            calculated. This control is provided for convenience of load
            generation for linear perturbation analysis. In general, a new set
            of loads is required for a linear perturbation analysis. This key
            controls all mechanical loads; it does not affect non-mechanical
            loads. Non-mechanical loads (including thermal loads) are always
            kept (i.e., not deleted).

            ALLKEEP - Keep all the boundary conditions (loads and
                      constraints) from the end of the load step of
                      the current restart point. This option is
                      convenient for further load application and is
                      useful for a linear perturbation analysis
                      restarted from a previous linear analysis. For
                      this option, {Fend} is the total load vector at
                      the end of the load step at the restart point.

            INERKEEP - Delete all loads and constraints from the
                       restart step, except for displacement
                       constraints and inertia loads (default). All
                       displacement constraints and inertia loads are
                       kept for convenience when performing the linear
                       perturbation analysis. Note that nonzero and
                       tabular displacement constraints can be
                       considered as external loads; however, they are
                       not deleted when using this option.

            PARKEEP - Delete all loads and constraints from the
                      restart step, except for displacement
                      constraints. All displacement constraints are
                      kept for convenience when performing the linear
                      perturbation analysis. Note that nonzero and
                      tabular displacement constraints can be
                      considered as external loads; however, they are
                      not deleted when using this option.

            DZEROKEEP - Behaves the same as the PARKEEP option, except
                        that all nonzero displacement constraints are
                        set to zero upon the onset of linear
                        perturbation.

            NOKEEP - Delete all the loads and constraints, including
                     all displacement constraints.  For this option,
                     {Fend} is zero unless non-mechanical loads (e.g.,
                     thermal loads) are present.

        Notes
        -----
        This command controls options relating to linear perturbation analyses.
        It must be issued in the first phase of a linear perturbation analysis.

        This command is also valid in PREP7.
        """
        command = f"PERTURB,{type_},{matkey},{contkey},{loadcontrol}"
        return self.run(command, **kwargs)

    def prscontrol(self, key="", **kwargs):
        """Specifies whether to include pressure load stiffness in the element

        APDL Command: PRSCONTROL
        stiffness formation.

        Parameters
        ----------
        key
            Pressure load stiffness key. In general, use the default setting.
            Use a non-default setting only if you encounter convergence
            difficulties. Pressure load stiffness is automatically included
            when using eigenvalue buckling analyses (ANTYPE,BUCKLE), equivalent
            to Key = INCP. For all other types of analyses, valid arguments for
            Key are:

            NOPL - Pressure load stiffness not included for any elements.

            (blank) (default) - Include pressure load stiffness for elements SURF153, SURF154, SURF156,
                              SURF159, SHELL181, PLANE182, PLANE183, SOLID185,
                              SOLID186, SOLID187, SOLSH190, BEAM188, BEAM189,
                              FOLLW201, SHELL208, SHELL209, SOLID272, SOLID273,
                              SHELL281, SOLID285, PIPE288, PIPE289, and
                              ELBOW290. Do not include pressure load stiffness
                              for elements SOLID65.

            INCP - Pressure load stiffness included for all of the default elements listed above
                   and SOLID65.

        Notes
        -----
        This command is rarely needed. The default settings are recommended for
        most analyses.
        """
        command = f"PRSCONTROL,{key}"
        return self.run(command, **kwargs)

    def pscontrol(self, option="", key="", **kwargs):
        """Enables or disables shared-memory parallel operations.

        APDL Command: PSCONTROL

        Parameters
        ----------
        option
            Specify the operations for which you intend to enable/disable
            parallel behavior:

            ALL  - Enable/disable parallel for all areas (default).

            PREP  - Enable/disable parallel during preprocessing (/PREP7).

            SOLU  - Enable/disable parallel during solution (/SOLU).

            FORM  - Enable/disable parallel during element matrix generation.

            SOLV  - Enable/disable parallel during equation solver.

            RESU - Enable/disable parallel during element results calculation.

            POST  - Enable/disable parallel during postprocessing (/POST1 and /POST26).

            STAT - List parallel operations that are enabled/disabled.

        key
             Option control key. Used for all Option values except STAT.

            ON  - Enable parallel operation.

            OFF  - Disable parallel operation.

        Notes
        -----
        Use this command in shared-memory parallel operations.

        This command is useful when you encounter minor discrepancies in a
        nonlinear solution when using different numbers of processors. A
        parallel operation applied to the element matrix generation can produce
        a different nonlinear solution with a different number of processors.
        Although the nonlinear solution converges to the same nonlinear
        tolerance, the minor discrepancy created may not be desirable for
        consistency.

        Enabling/disabling parallel behavior for the solution (Option = SOLU)
        supersedes the activation/deactivation of parallel behavior for element
        matrix generation (FORM), equation solver (SOLV), and element results
        calculation (RESU).

        The SOLV option supports only the sparse direct and PCG solvers
        (EQSLV,SPARSE or PCG). No other solvers are supported.

        This command applies only to shared-memory architecture. It does not
        apply to the Distributed ANSYS product.
        """
        command = f"PSCONTROL,{option},{key}"
        return self.run(command, **kwargs)

    def rate(self, option="", **kwargs):
        """Specifies whether the effect of creep strain rate will be used in the

        APDL Command: RATE
        solution of a load step.

        Parameters
        ----------
        option
            Activates implicit creep analysis.

            0 or OFF  - No implicit creep analysis. This option is the default.

            1 or ON  - Perform implicit creep analysis.

        Notes
        -----
        Set Option = 1 (or ON) to perform an implicit creep analysis (TB,CREEP
        with TBOPT :  1). For viscoplasticity/creep analysis, Option specifies
        whether or not to include the creep calculation in the solution of a
        load step. If Option = 1 (or ON), ANSYS performs the creep calculation.
        Set an appropriate time for solving the load step via a TIME,TIME
        command.
        """
        command = f"RATE,{option}"
        return self.run(command, **kwargs)

    def resvec(self, key="", **kwargs):
        """Calculates or includes residual vectors.

        APDL Command: RESVEC

        Parameters
        ----------
        key
            Residual vector key:

            OFF - Do not calculate or include residual vectors. This option is the default.

            ON  - Calculate or include residual vectors.

        Notes
        -----
        In a modal analysis, the RESVEC command calculates residual vectors. In
        a mode-superposition transient dynamic, mode-superposition harmonic,
        PSD or spectrum analysis, the command includes residual vectors.

        In a component mode synthesis (CMS) generation pass, the RESVEC command
        calculates one residual vector which is included in the normal modes
        basis used in the transformation matrix. It is supported for the three
        available CMS methods. RESVEC,ON can only be specified in the first
        load step of a generation pass and is ignored if issued at another load
        step.

        If rigid-body modes exist, pseudo-constraints are required for the
        calculation. Issue the D,,,SUPPORT command to specify only the minimum
        number of pseudo-constraints necessary to prevent rigid-body motion.

        For more information about residual vector formulation, see Residual
        Vector Method in the Mechanical APDL Theory Reference.
        """
        command = f"RESVEC,{key}"
        return self.run(command, **kwargs)

    def rstoff(self, lab="", offset="", **kwargs):
        """Offsets node or element IDs in the FE geometry record.

        APDL Command: RSTOFF

        Parameters
        ----------
        lab
            The offset type:

            NODE  - Offset the node IDs.

            ELEM  - Offset the element IDs.

        offset
            A positive integer value specifying the offset value to apply. The
            value must be greater than the number of nodes or elements in the
            existing superelement results file.

        Notes
        -----
        The RSTOFF command offsets node or element IDs in the FE geometry
        record saved in the .rst results file. Use the command when expanding
        superelements in a bottom-up substructuring analysis (where each
        superelement is generated individually in a generation pass, and all
        superelements are assembled together in the use pass).

        With appropriate offsets, you can write results files with unique node
        or element IDs and thus display the entire model even if the original
        superelements have overlapping element or node ID sets. (Such results
        files are incompatible with the .db database file saved at the
        generation pass.)

        The offset that you specify is based on the original superelement node
        or element numbering, rather than on any offset specified via a SESYMM
        or SETRAN command. When issuing an RSTOFF command, avoid specifying an
        offset that creates conflicting node or element numbers for a
        superelement generated via a SESYMM or SETRAN command.

        If you issue the command to set non-zero offsets for node or element
        IDs, you must bring the geometry into the database via the SET command
        so that ANSYS can display the results. You must specify appropriate
        offsets to avoid overlapping node or element IDs with other
        superelement results files.

        The command is valid only in the first load step of a superelement
        expansion pass.
        """
        command = f"RSTOFF,{lab},{offset}"
        return self.run(command, **kwargs)

    def scopt(self, tempdepkey="", **kwargs):
        """Specifies System Coupling options.

        APDL Command: SCOPT

        Parameters
        ----------
        tempdepkey
            Temperature-dependent behavior key based on the convection
            coefficient:

            * ``"YES"`` : A negative convection coefficient, -N, is
              assumed to be a function of temperature and is determined
              from the HF property table for material N (MP command). This
              is the default.

            * ``"NO"`` : A negative convection coefficient, -N, is used as
              is in the convection calculation.

        Notes
        -----
        By default in the Mechanical APDL program, a negative convection
        coefficient value triggers temperature-dependent behavior. In
        System Coupling, and in some one-way CFD to Mechanical APDL
        thermal simulations, it is desirable to allow convection
        coefficients to be used as negative values. To do so, issue the
        command ``scopt("NO")``.
        """
        return self.run(f"SCOPT,{tempdepkey}", **kwargs)

    def seexp(self, sename="", usefil="", imagky="", expopt="", **kwargs):
        """Specifies options for the substructure expansion pass.

        APDL Command: SEEXP

        Parameters
        ----------
        sename
            The name (case-sensitive) of the superelement matrix file created
            by the substructure generation pass (Sename.SUB).  Defaults to the
            initial jobname File.  If a number, it is the element number of the
            superelement as used in the use pass.

        usefil
            The name of the file containing the superelement degree-of-freedom
            (DOF) solution created by the substructure use pass (Usefil.DSUB).

        imagky
            Key to specify use of the imaginary component of the DOF solution.
            Applicable only if the use pass is a harmonic (ANTYPE,HARMIC)
            analysis:

            OFF - Use real component of DOF solution (default).

            ON - Use imaginary component of DOF solution.

        expopt
            Key to specify whether the superelement (ANTYPE,SUBSTR) expansion
            pass (EXPASS,ON) should transform the geometry:

            OFF - Do not transform node or element locations (default).

            ON - Transform node or element locations in the FE geometry record of the .rst
                 results file.

        Notes
        -----
        Specifies options for the expansion pass of the substructure analysis
        (ANTYPE,SUBSTR).  If used in SOLUTION, this command is valid only
        within the first load step.

        If you specify geometry transformation (Expopt = ON), you must retrieve
        the transformation matrix (if it exists) from the specified .SUB file.
        The command updates the nodal X, Y, and Z coordinates to represent the
        transformed node locations. The Expopt option is useful when you want
        to expand superelements created from other superelements (via SETRAN or
        SESYMM commands). For more information, see Superelement Expansion in
        Transformed Locations and Plotting or Printing Mode Shapes.

        This command is also valid in /PREP7.
        """
        command = f"SEEXP,{sename},{usefil},{imagky},{expopt}"
        return self.run(command, **kwargs)

    def seopt(
        self,
        sename="",
        sematr="",
        sepr="",
        sesst="",
        expmth="",
        seoclvl="",
        **kwargs,
    ):
        """Specifies substructure analysis options.

        APDL Command: SEOPT

        Parameters
        ----------
        sename
            The name (case-sensitive, thirty-two character maximum) assigned to
            the superelement matrix file. The matrix file will be named
            Sename.SUB. This field defaults to Fname on the /FILNAME command.

        sematr
            Matrix generation key:

            1 - Generate stiffness (or conductivity) matrix (default).

            2 - Generate stiffness and mass (or conductivity and specific heat) matrices.

            3 - Generate stiffness, mass and damping matrices.

        sepr
            Print key:

            0 - Do not print superelement matrices or load vectors.

            1 - Print both load vectors and superelement matrices.

            2 - Print load vectors but not matrices.

        sesst
            Stress stiffening key:

            0 - Do not save space for stress stiffening in a later run.

            1 - Save space for the stress stiffening matrix (calculated in a subsequent
                generation run after the expansion pass).

        expmth
            Expansion method for expansion pass:

            BACKSUB - Save necessary factorized matrix files for backsubstitution during subsequent
                      expansion passes (default). This normally results in a
                      large usage of disk space

            RESOLVE - Do not save factorized matrix files. Global stiffness matrix will be reformed
                      during expansion pass. This option provides an effective
                      way to save disk space usage. This option cannot be used
                      if the use pass uses large deflections (NLGEOM,ON).

        seoclvl
            For the added-mass calculation, the ocean level to use when ocean
            waves (OCTYPE,,WAVE) are present:

            ATP - The ocean level at this point in time (default).

            MSL - The mean ocean level.

        Notes
        -----
        The SEOPT command specifies substructure analysis options
        (ANTYPE,SUBSTR).  If used during solution, the command is valid only
        within the first load step.

        When ocean waves (OCTYPE,,WAVE) are present, the SeOcLvL argument
        specifies the ocean height or level to use for the added-mass
        calculation, as the use-run analysis type is unknown during the
        generation run.

        The expansion pass method RESOLVE is not supported with component mode
        synthesis analysis (CMSOPT). ExpMth is automatically set to BACKSUB for
        CMS analysis. The RESOLVE method invalidates the use of the NUMEXP
        command. The RESOLVE method does not allow the computation of results
        based on nodal velocity and nodal acceleration (damping force, inertial
        force, kinetic energy, etc.) in the substructure expansion pass.

        This command is also valid in PREP7.
        """
        command = f"SEOPT,{sename},{sematr},{sepr},{sesst},{expmth},{seoclvl}"
        return self.run(command, **kwargs)

    def snoption(
        self,
        rangefact="",
        blocksize="",
        robustlev="",
        compute="",
        solve_info="",
        **kwargs,
    ):
        """Specifies Supernode (SNODE) eigensolver options.

        APDL Command: SNOPTION

        Parameters
        ----------
        rangefact
            Factor used to control the range of eigenvalues computed for each
            supernode. The value of RangeFact must be a number between 1.0 and
            5.0. By default the RangeFact value is set to 2.0, which means that
            all eigenvalues between 0 and ``2*FREQE`` are computed for each
            supernode (where FREQE is the upper end of the frequency range of
            interest as specified on the MODOPT command). As the RangeFact
            value increases, the eigensolution for the SNODE solver becomes
            more accurate and the computational time increases.

        blocksize
            BlockSize to be used when computing the final eigenvectors. The
            value of Blocksize must be either MAX or a number between 1 and
            NMODE, where NMODE is the number of modes to be computed as set on
            the MODOPT command. Input a value of MAX to force the algorithm to
            allocate enough memory to hold all of the final eigenvectors in
            memory and, therefore, only read through the file containing the
            supernode eigenvectors once. Note that this setting is ONLY
            recommended when there is sufficient physical memory on the machine
            to safely hold all of the final eigenvectors in memory.

        robustlev
            Parameter used to control the robustness of the SNODE eigensolver.
            The value of RobustLev must be a number between 0 and 10.  Lower
            values of RobustLev allow the eigensolver to run in the most
            efficient manner for optimal performance.  Higher values of
            RobustLev often slow down the performance of the eigensolver, but
            can increase the robustness; this may be desirable if a problem is
            detected with the eigensolver or its eigensolution.

        compute
            Key to control which computations are performed by the Supernode
            eigensolver:

            EVALUE - The eigensolver computes only the eigenvalues.

            EVECTOR - The eigensolver computes only the eigenvectors
                      (must be preceded by a modal analysis where the
                      eigenvalues were computed using the Supernode
                      eigensolver).

            BOTH - The eigensolver computes both the eigenvalues and
                   eigenvectors in the same pass (default).

        solve_info
            Solver output option:

            OFF - Turns off additional output printing from the
            Supernode eigensolver (default).

            PERFORMANCE - Turns on additional output printing from the
                          Supernode eigensolver, including a
                          performance summary and a summary of file
                          I/O for the Supernode
                          eigensolver. Information on memory usage
                          during assembly of the global matrices (that
                          is, creation of the Jobname.FULL file) is
                          also printed with this option.

        Notes
        -----
        This command specifies options for the Supernode (SNODE)
        eigensolver.

        Setting RangeFact to a value greater than 2.0 will improve the
        accuracy of the computed eigenvalues and eigenvectors, but
        will often increase the computing time of the SNODE
        eigensolver. Conversely, setting RangeFact to a value less
        than 2.0 will deteriorate the accuracy of the computed
        eigenvalues and eigenvectors, but will often speedup the
        computing time of the SNODE eigensolver.  The default value of
        2.0 has been set as a good blend of accuracy and performance.

        The SNODE eigensolver reads the eigenvectors and related
        information for each supernode from a file and uses that
        information to compute the final eigenvectors.  For each
        eigenvalue/eigenvector requested by the user, the program must
        do one pass through the entire file that contains the
        supernode eigenvectors.  By choosing a BlockSize value greater
        than 1, the program can compute BlockSize number of final
        eigenvectors for each pass through the file.  Therefore,
        smaller values of BlockSize result in more I/O, and larger
        values of BlockSize result in less I/O.  Larger values of
        BlockSize also result in significant additional memory usage,
        as BlockSize number of final eigenvectors must be stored in
        memory. The default Blocksize of min(NMODE,40) is normally a
        good choice to balance memory and I/O usage.

        The RobustLev field should only be used when a problem is
        detected with the accuracy of the final solution or if the
        Supernode eigensolver fails while computing the
        eigenvalues/eigenvectors. Setting RobustLev to a value greater
        than 0 will cause the performance of the eigensolver to
        deteriorate. If the performance deteriorates too much or if
        the eigensolver continues to fail when setting the RobustLev
        field to higher values, then switching to another eigensolver
        such as Block Lanczos or PCG Lanczos is recommended.

        Setting Compute = EVALUE causes the Supernode eigensolver to
        compute only the requested eigenvalues.  During this process a
        Jobname.SNODE file is written; however, a Jobname.MODE file is
        not written. Thus, errors will likely occur in any downstream
        computations that require the Jobname.MODE file (for example,
        participation factor computations, mode superpostion
        transient/harmonic analysis, PSD analysis). Setting Compute =
        EVECTOR causes the Supernode eigensolver to compute only the
        corresponding eigenvectors. The Jobname.SNODE file and the
        associated Jobname.FULL file are required when requesting
        these eigenvectors. In other words, the eigenvalues must have
        already been computed for this model before computing the
        eigenvectors. This field can be useful in order to separate
        the two steps (computing eigenvalues and computing
        eigenvectors).
        """
        command = (
            f"SNOPTION,{rangefact},{blocksize},{robustlev},{compute},,{solve_info}"
        )
        return self.run(command, **kwargs)

    def solve(self, action="", **kwargs):
        """Starts a solution.

        APDL Command: SOLVE

        Parameters
        ----------
        action
            Action to be performed on solve (used only for linear perturbation
            analyses).

            ELFORM  - Reform all appropriate element matrices in the first phase of a linear
                      perturbation analysis.

        Notes
        -----
        Starts the solution of one load step of a solution sequence based on
        the current analysis type and option settings. Use Action = ELFORM only
        in the first phase of a linear perturbation analysis.
        """
        command = f"SOLVE,{action}"
        return self.run(command, **kwargs)

    def stabilize(
        self, key="", method="", value="", substpopt="", forcelimit="", **kwargs
    ):
        """Activates stabilization for all elements that support nonlinear

        APDL Command: STABILIZE
        stabilization.

        Parameters
        ----------
        key
            Key for controlling nonlinear stabilization:

            OFF  -  Deactivate stabilization. This value is the default.

            CONSTANT  -  Activate stabilization. The energy-dissipation ratio or damping factor remains
                        constant during the load step.

            REDUCE  -  Activate stabilization. The energy-dissipation ratio or damping factor is
                      reduced linearly to zero at the end of the load step from
                      the specified or calculated value.

        method
            The stabilization-control method:

            ENERGY  -  Use the energy-dissipation ratio as the control. This value is the default
                      when Key ≠ OFF.

            DAMPING  -  Use the damping factor as the control.

        value
            The energy-dissipation ratio (Method = ENERGY) or damping factor
            (Method = DAMPING). This value must be greater than 0 when Method =
            ENERGY or Method = DAMPING. When Method = ENERGY, this value is
            usually a number between 0 and 1.

        substpopt
            Option for the first substep of the load step:

            NO  -  Stabilization is not activated for the first substep even when it does not
                  converge after the minimal allowed time increment is reached.
                  This value is the default when Key ≠ OFF.

            MINTIME  -  Stabilization is activated for the first substep if it still does not converge
                       after the minimal allowed time increment is reached.

            ANYTIME  -  Stabilization is activated for the first substep. Use this option if
                       stabilization was active for the previous load step via
                       Key = CONSTANT.

        forcelimit
            The stabilization force limit coefficient, such that 0 < FORCELIMIT
            < 1. The default value is 0.2. To omit a stabilization force check,
            set this value to 0.

        Notes
        -----
        Once issued, a STABILIZE command remains in effect until you reissue
        the command.

        For the energy dissipation ratio, specify VALUE = 1.0e-4 if you have no
        prior experience with the current model; if convergence problems are
        still an issue, increase the value gradually. The damping factor is
        mesh-, material-, and time-step-dependent; an initial reference value
        from the previous run (such as a run with the energy-dissipation ratio
        as input) should suggest itself.

        Exercise caution when specifying SubStpOpt = MINTIME or ANYTIME for the
        first load step; ANSYS, Inc. recommends this option only for
        experienced users. If stabilization was active for the previous load
        step via Key = CONSTANT and convergence is an issue for the first
        substep, specify SubStpOpt = ANYTIME.

        When the L2-norm of the stabilization force (CSRSS value) exceeds the
        L2-norm of the internal force multiplied by the stabilization force
        coefficient, ANSYS issues a message displaying both the stabilization
        force norm and the internal force norm. The FORCELIMIT argument allows
        you to change the default stabilization force coefficient (normally 20
        percent).

        This command stabilizes the degrees of freedom for current-technology
        elements only. Other elements can be included in the FE model, but
        their degrees of freedom are not stabilized.

        For more information about nonlinear stabilization, see Unstable
        Structures in the Structural Analysis Guide. For additional tips that
        can help you to achieve a stable final model, see Simplify Your Model
        in the Structural Analysis Guide.
        """
        command = f"STABILIZE,{key},{method},{value},{substpopt},{forcelimit}"
        return self.run(command, **kwargs)

    def thexpand(self, key="", **kwargs):
        """Enables or disables thermal loading

        APDL Command: THEXPAND

        Parameters
        ----------
        key
            Activation key:

            ON  - Thermal loading is included in the load vector (default).

            OFF - Thermal loading is not included in the load vector.

        Notes
        -----
        Temperatures applied in the analysis are used by default to evaluate
        material properties and contribute to the load vector if the
        temperature does not equal the reference temperature and a coefficient
        of thermal expansion is specified.

        Use THEXPAND,OFF to evaluate the material properties but not contribute
        to the load vector. This capability is particularly useful when
        performing a harmonic analysis where you do not want to include
        harmonically varying thermal loads. It is also useful in a modal
        analysis when computing a modal load vector but excluding the thermal
        load.

        This command is valid for all analysis types except linear perturbation
        modal and linear perturbation harmonic analyses. For these two linear
        perturbation analysis types, the program internally sets THEXPAND,OFF,
        and it cannot be set to ON by using this command (THEXPAND,ON is
        ignored).
        """
        command = f"THEXPAND,{key}"
        return self.run(command, **kwargs)

    def thopt(
        self,
        refopt="",
        reformtol="",
        ntabpoints="",
        tempmin="",
        tempmax="",
        algo="",
        **kwargs,
    ):
        """Specifies nonlinear transient thermal solution options.

        APDL Command: THOPT

        Parameters
        ----------
        refopt
            Matrix reform option.

            FULL - Use the full Newton-Raphson solution option (default). All subsequent input
                   values are ignored.

            QUASI - Use a selective reform solution option based on REFORMTOL.

        reformtol
            Property change tolerance for Matrix Reformation (.05 default). The
            thermal matrices are reformed if the maximum material property
            change in an element (from the previous reform time) is greater
            than the reform tolerance. Valid only when Refopt = QUASI.

        ntabpoints
            Number of points in Fast Material Table (64 default). Valid only
            when Refopt = QUASI.

        tempmin
            Minimum temperature for Fast Material Table. Defaults to the
            minimum temperature defined by the MPTEMP command for any material
            property defined. Valid only when Refopt = QUASI.

        tempmax
            Maximum temperature for Fast Material Table. Defaults to the
            maximum temperature defined by the MPTEMP command for any material
            property defined. Valid only when Refopt = QUASI.

        --
            Reserved field.

        algo
            Specifies which solution algorithm to apply:

            0 - Multipass (default).

            1 - Iterative.

        Notes
        -----
        The QUASI matrix reform option is supported by the ICCG, JCG, and
        sparse solvers only (EQSLV).

        For Refopt = QUASI:

        Results from a restart may be different than results from a single run
        because the stiffness matrices are always recreated in a restart run,
        but may or may not be in a single run (depending on the behavior
        resulting from the REFORMTOL setting). Additionally, results may differ
        between two single runs as well, if the matrices are reformed as a
        result of the REFORMTOL setting.

        Midside node temperatures are not calculated if 20-node thermal solid
        elements (SOLID90 or SOLID279) are used.

        For more information, see Solution Algorithms Used in Transient Thermal
        Analysis in the Thermal Analysis Guide.
        """
        command = f"THOPT,{refopt},{reformtol},{ntabpoints},{tempmin},{tempmax},{algo}"
        return self.run(command, **kwargs)
