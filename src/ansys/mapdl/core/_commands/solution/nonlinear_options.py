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


class NonlinearOptions:

    def arclen(self, key: str = "", maxarc: str = "", minarc: str = "", **kwargs):
        r"""Activates the arc-length method.

        Mechanical APDL Command: `ARCLEN <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ARCLEN.html>`_

        Parameters
        ----------
        key : str
            Arc-length key:

            * ``OFF`` - Do not use the arc-length method (default).

            * ``ON`` - Use the arc-length method.

        maxarc : str
            Maximum multiplier of the reference arc-length radius (default = 25).

        minarc : str
            Minimum multiplier of the reference arc-length radius (default = 1/1000).

        Notes
        -----

        .. _ARCLEN_notes:

        Activates the arc-length method and sets the minimum and maximum multipliers for controlling the
        arc-length radius based on the initial arc-length radius.

        The initial arc-length radius, t:sub:`0`, is proportional (in absolute value) to the initial load
        factor. The initial load factor is given by:

        Initial Load Factor = ``TIME`` / ``NSBSTP``

        where ``TIME`` is the time specified by the :ref:`time` command for the arc-length load step, and
        ``NSBSTP`` is the number of substeps specified by the :ref:`nsubst` command.

        The factors ``MAXARC`` and ``MINARC`` are used to define the range for the arc-length radius to
        expand and shrink during the substep solution:

        * t :sub:`MAX` = ``MAXARC`` \* t :sub:`0`
        * t :sub:`MIN` = ``MINARC`` \* t :sub:`0`

        In each substep, the arc-length radius is kept constant throughout the equilibrium iterations. After
        each converged substep, the arc-length radius for the next substep is modified depending on the
        convergence behavior. If the substep converges and the program heuristic predicts an easy
        convergence, the arc-length radius is enlarged. If the enlarged value is greater than t:sub:`MAX`,
        the arc-length radius is reset to t:sub:`MAX`. If the substep does not converge, bisection will
        take place until the arc-length radius is reduced to t:sub:`MIN`. If further nonconvergence is
        encountered, the solution terminates.

        The arc-length method predicts the next time increment (that is, load factor increment). Therefore,
        the :ref:`autots` and :ref:`pred` commands are ignored when the arc-length method is used.

        The :ref:`stabilize` and :ref:`lnsrch` commands are also ignored.

        The arc-length method cannot be used in a multiframe restart.

        For difficult problems, one suggestion is to increase the initial number of substeps ( :ref:`nsubst`
        ), and to prevent the arc-length radius from increasing too rapidly ( ``MAXARC`` = 1).

        :ref:`arclen` cannot be used for any load step that has no applied load or displacement.

        The arc-length method does not support tabular loads. In order to use the arc-length method, you
        must replace tabular loads by other load types and then run the analysis again.

        The arc-length method can only be used with the sparse solver ( :ref:`eqslv`,SPARSE). If any other
        solver is specified, the solver method is automatically changed to sparse, and a warning message is
        issued to notify you.
        """
        command = f"ARCLEN,{key},{maxarc},{minarc}"
        return self.run(command, **kwargs)

    def arctrm(
        self, lab: str = "", val: str = "", node: str = "", dof: str = "", **kwargs
    ):
        r"""Controls termination of the solution when the arc-length method is used.

        Mechanical APDL Command: `ARCTRM <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ARCTRM.html>`_

        Parameters
        ----------
        lab : str
            Specifies the basis of solution termination:

            * ``OFF`` - Does not use :ref:`arctrm` to terminate analysis (default).

            * ``L`` - Terminates the analysis if the first limit point has been reached. The first limit point
              is that point in the response history when the tangent stiffness matrix becomes singular (that is,
              the point at which the structure becomes unstable). If ``Lab`` = L, arguments ``VAL``, ``NODE``,
              ``DOF`` are ignored.

            * ``U`` - Terminates the analysis when the displacement first equals or exceeds the maximum desired
              value.

        val : str
            Maximum desired displacement (absolute value). Valid only if ``Lab`` = U. The analysis
            terminates whenever the calculated displacement first equals or exceeds this value. For
            rotational degrees of freedom, ``VAL`` must be in radians (not degrees).

        node : str
            Node number corresponding to displacement used to compare with displacement specified by
            ``VAL``. If blank, the maximum displacement will be used. Valid only if ``Lab`` = U.

        dof : str
            Valid degree of freedom label for nodal displacement specified by ``NODE``. Valid labels are UX,
            UY, UZ, ROTX, ROTY, ROTZ. Valid only if ``NODE`` >0 and ``Lab`` = U.

        Notes
        -----

        .. _ARCTRM_notes:

        The :ref:`arctrm` command is valid only when the arc-length method ( :ref:`arclen`,ON) is used.

        It can be convenient to use this command to terminate the analysis when the first limit point is
        reached. In addition, the :ref:`ncnv` command should be used to limit the maximum number of
        iterations. If the :ref:`arctrm` command is not used, and the applied load is so large that the
        solution path can never reach that load, the arc-length solution will continue to run until a CPU
        time limit or a "maximum number of iterations" is reached.
        """
        command = f"ARCTRM,{lab},{val},{node},{dof}"
        return self.run(command, **kwargs)

    def bucopt(
        self,
        method: str = "",
        nmode: str = "",
        shift: str = "",
        ldmulte: str = "",
        rangekey: str = "",
        **kwargs,
    ):
        r"""Specifies buckling analysis options.

        Mechanical APDL Command: `BUCOPT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_BUCOPT.html>`_

        Parameters
        ----------
        method : str
            Mode extraction method to be used for the buckling analysis:

            * ``LANB`` - Block Lanczos

            * ``SUBSP`` - Subspace iteration

            See `Eigenvalue and Eigenvector Extraction
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_tool13.html#eltcomplexeigens>`_

        nmode : str
            Number of buckling modes (that is, eigenvalues or load multipliers) to extract (defaults to 1).

        shift : str
            By default, this value acts as the initial shift point about which the buckling modes are
            calculated (defaults to 0.0).

            When ``RangeKey`` = RANGE, this value acts as the lower bound of the load multiplier range of
            interest ( ``LDMULTE`` is the upper bound).

        ldmulte : str
            Boundary for the load multiplier range of interest (defaults to :math:`equation not available`
            ).

            When ``RangeKey`` = CENTER, the ``LDMULTE`` value determines the lower and upper bounds of the
            load multiplier range of interest (- ``LDMULTE``, + ``LDMULTE`` ).

            When ``RangeKey`` = RANGE, the ``LDMULTE`` value is the upper bound for the load multiplier
            range of interest ( ``SHIFT`` is the lower bound).

        rangekey : str
            Key used to control the behavior of the eigenvalue extraction method (defaults to CENTER):

            * ``CENTER`` - Use the CENTER option control (default); the program computes ``NMODE`` buckling
              modes centered around ``SHIFT`` in the range of (- ``LDMULTE``, + ``LDMULTE`` ).

            * ``RANGE`` - Use the RANGE option control; the program computes ``NMODE`` buckling modes in the
              range of ( ``SHIFT``, ``LDMULTE`` ).

        Notes
        -----

        .. _BUCOPT_notes:

        Specifies buckling analysis ( :ref:`antype`,BUCKLE) options. Additional options used only for the
        Block Lanczos (LANB) eigensolver are specified by the :ref:`lanboption` command. For more difficult
        buckling problems, you can specify an alternative version of the Block Lanczos eigensolver (
        :ref:`lanboption`,,,ALT1).

        Eigenvalues from a buckling analysis can be negative and/or positive. The program sorts the
        eigenvalues from the most negative to the most positive values. The minimum buckling load factor may
        correspond to the smallest eigenvalue in absolute value, or to an eigenvalue within the range,
        depending on your application (that is, linear perturbation buckling analysis or purely linear
        buckling analysis).

        It is recommended that you request an additional few buckling modes beyond what is needed in order
        to enhance the accuracy of the final solution. It is also recommended that you input a non zero
        ``SHIFT`` value and a reasonable ``LDMULTE`` value (that is, a smaller ``LDMULTE`` that is closer to
        the last buckling mode of interest) when numerical problems are encountered.

        When using the RANGE option, defining a range that spans zero is not recommended. If you are seeking
        both negative and positive eigenvalues, it is recommended that you use the CENTER option.

        This command is also valid in PREP7. If used in SOLUTION, this command is valid only within the
        first load step.
        """
        command = f"BUCOPT,{method},{nmode},{shift},{ldmulte},{rangekey}"
        return self.run(command, **kwargs)

    def cnvtol(
        self,
        lab: str = "",
        value: str = "",
        toler: str = "",
        norm: int | str = "",
        minref: str = "",
        **kwargs,
    ):
        r"""Sets convergence values for nonlinear analyses.

        Mechanical APDL Command: `CNVTOL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CNVTOL.html>`_

        **Command default:**

        .. _CNVTOL_default:

        For static or transient analysis, check the out-of-balance load for any active degree of freedom
        using the default ``VALUE``, ``TOLER``, ``NORM``, and ``MINREF``. Also check the translational
        displacement convergence in most cases. For harmonic magnetic analysis, check the out-of-balance of
        the degrees of freedom. The energy criterion convergence check is off by default.

        Parameters
        ----------
        lab : str
            Valid convergence labels.

            This command contains some tables and extra information which can be inspected in the original
            documentation pointed above.

        value : str
            Typical reference value for the specified convergence label ( ``Lab`` ).

            ``VALUE`` defaults to the maximum of a program calculated reference or ``MINREF``. For degrees
            of freedom, the reference is based upon the selected ``NORM`` and the current total degree-of-
            freedom value. For forcing quantities, the reference is based upon the selected ``NORM`` and the
            applied loads.

            If ``VALUE`` is negative, the convergence criterion based on the specified label is removed,
            including the default convergence criterion value. The convergence criterion for all other
            labels remain as they were (either a default value or a previously specified value).

        toler : str
            Tolerance value used for the specified ``Lab`` convergence label. Default values are described below.

            * If :ref:`cnvtol` is issued with a ``Lab`` value specified but no ``TOLER`` value, the default
              tolerance values are:

            * 0.05 (5%) for displacement (U).

            * 1.0E-7 for the joint element constraint check (JOINT). This value rarely needs to be changed. A
              loose tolerance value may lead to inaccurate or incorrect solutions. When ``Lab`` = JOINT,
              ``VALUE``, ``NORM``, and ``MINREF`` are ignored.

            * 1.0E-3 for the volumetric compatibility check (COMP). When ``Lab`` = COMP, ``VALUE``, ``NORM``,
              and ``MINREF`` are ignored.

            * 0.05 for energy error (ENGY).

            * For all other ``Lab`` labels, the default tolerance value is 0.005 (0.5%).

            * If :ref:`cnvtol` is not issued, the ``TOLER`` defaults are as follows:

            * 0.005 (0.5%) for force (F) and moment (M)

            * 1.0E-4 (0.01%) for volume (DVOL)

            * 0.05 (5%) for displacement (U)

            * 0.05 (5%) for hydrostatic pressure (HDSP)

            * 1.0 for temperature (TEMP) when the iterative QUASI solver is used ( :ref:`thopt`,QUASI,,,,,,1)

            If you choose to specify a ``TOLER`` value, it must be greater than zero and less than 1. This is
            true for all ``Lab`` labels.

            The program may adjust the force convergence tolerance if you do not explicitly set a value via
            :ref:`cnvtol`. See :ref:`Notes for details. <CNVTOL_notes>`

        norm : int or str
            Specifies norm selection:

            * ``0`` - Infinite norm (check each degree of freedom separately) (default for ``Lab`` = U and for
              ``Lab`` = TEMP when the iterative QUASI solver is used ( :ref:`thopt`,QUASI,,,,,,,1).

              The infinite norm is also used for the energy error criterion (ENGY) and is the only option
              available for ENGY.

            * ``1`` - L1 norm (check absolute value sum).

            * ``2`` - L2 norm (check SRSS value) (default, except for ``Lab`` = U).

            * ``3`` - Infinite norm (check each degree of freedom separately). The reference is calculated using
              the infinite norm of the displacement increment of the substep. Valid only for ``Lab`` = U.

        minref : str
            The minimum value allowed for the program-calculated reference value. If negative, no minimum is
            enforced. Used only if ``VALUE`` is blank. Default values are as follows:

            * maximum of 0.01 or internally calculated minimum reference value for force (F), moment (M)

            * a small factor times the average element length of the model for displacement (U) convergence

            * 0.01 for volume (DVOL) convergence

            * 1.0E-4 for gradient field residual (GFRS)

            * 1.0E-6 for heat flow (HEAT)

            * 1.0E-6 for diffusion flow (RATE)

            * 1.0E-12 for charge (CHRG)

            * 1.0E-6 for hydrostatic pressure (HDSP)

            * 1.0 for temperature (TEMP) when the iterative QUASI solver is used ( :ref:`thopt`,QUASI,,,,,,,1)

            * 1.0 for energy error convergence (ENGY)

            * 0.0 otherwise

        Notes
        -----

        .. _CNVTOL_notes:

        This command is usually not needed because the default convergence criteria are sufficient for most
        nonlinear analyses. In rare cases, you may need to use this command to diagnose convergence
        difficulties.

        Values may be set for the degrees of freedom and/or the out-of-balance load for the corresponding
        forcing quantities.

        Issuing :ref:`cnvtol` to set a convergence criterion for a specific convergence label ( ``Lab`` )
        does not affect the convergence criterion for any other label. All other convergence criteria will
        remain at their default setting or at the value set by a previous :ref:`cnvtol` command.

        If :ref:`cnvtol` is not issued for any force convergence label (F, M, DVOL, and so on as listed
        under the ``Lab`` argument), the default convergence tolerance for a particular force label is
        increased dynamically during the Newton-Raphson iterations in the range of 1 to 1.66 times the
        default value. For example, the F label default tolerance is 0.005. Therefore, the maximum
        convergence tolerance with the adjustment is 0.0083. This adjustment is not activated until the 8th
        or higher Newton-Raphson iteration. If you do not want the program to adjust the tolerance, issue
        :ref:`cnvtol` to specify the convergence tolerance for the appropriate force label.

        When using the Mechanical APDL graphical user interface (GUI), if a "Delete" operation in a
        Nonlinear
        Convergence Criteria dialog box writes this command to a log file ( :file:`Jobname.LOG` or
        :file:`Jobname.LGW` ), you will observe that ``Lab`` is blank, ``VALUE`` = -1, and ``TOLER`` is an
        integer number. In this case, the GUI has assigned a value of ``TOLER`` that corresponds to the
        location of a chosen convergence label in the dialog box's list. It is not intended that you type in
        such a location value for ``TOLER`` in an interactive session. However, a file that contains a GUI-
        generated :ref:`cnvtol` command of this form can be used for batch input or with the :ref:`input`
        command.

        Convergence norms specified with :ref:`cnvtol` may be graphically tracked while the solution is in
        process using the Graphical Solution Tracking (GST) feature. Issue :ref:`gst` to enable or disable
        GST. By default, GST is ON for interactive sessions and OFF for batch runs.

        The energy convergence check (ENGY) is not available when the arc-length method ( :ref:`arclen`,ON)
        is used.

        For more information on convergence calculations in a nonlinear analysis, see `Convergence
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_tool10.html#eq17e730e1-975b-4fe6-a06d-86bc08aa77ad>`_

        This command is also valid in PREP7.
        """
        command = f"CNVTOL,{lab},{value},{toler},{norm},{minref}"
        return self.run(command, **kwargs)

    def gst(self, lab: str = "", runtrack: str = "", **kwargs):
        r"""Enables the Graphical Solution Tracking (GST) feature.

        Mechanical APDL Command: `/GST <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_GST.html>`_

        Parameters
        ----------
        lab : str
            Enables or disables the GST feature:

            * ON - Enable
            * OFF - Disable

        runtrack : str
            Enables or disables :file:`.GST` file viewing in the Results Tracker utility:

            * ON - Enable
            * OFF - Disable (default)

        Notes
        -----

        .. _s-GST_notes:

        For interactive sessions using the GUI ( :ref:`menu`,ON), GST directs solution graphics to the
        screen.

        For interactive sessions not using the GUI ( :ref:`menu`,OFF), or for batch sessions, GST saves
        solution graphics to the :file:`Jobname.GST` file. To create a :file:`Jobname.GST` file that is
        compatible with the Results Tracker utility (available via the Mechanical APDL Product Launcher ),
        issue :ref:`gst`,ON,ON.

        You can use the GST feature for these nonlinear analysis types: structural, thermal, electric,
        magnetic, fluid, and diffusion.

        For more information about GST and illustrations of the GST graphics for each analysis type, see the
        analysis guide for the appropriate discipline.
        """
        command = f"/GST,{lab},{runtrack}"
        return self.run(command, **kwargs)

    def lnsrch(self, key: str = "", lstol: str = "", lstrun: str = "", **kwargs):
        r"""Activates a line search to be used with Newton-Raphson.

        Mechanical APDL Command: `LNSRCH <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_LNSRCH.html>`_

        Parameters
        ----------
        key : str
            Line search key:

            * ``OFF`` - Do not use a line search.

            * ``ON`` - Use a line search. Note, adaptive descent is suppressed when :ref:`lnsrch` is on unless
              explicitly requested on the :ref:`nropt` command. Having line search on and adaptive descent on at
              the same time is not recommended.

            * ``AUTO`` - The program automatically switches line searching ON and OFF between substeps of a load
              step as needed. This option is recommended.

        lstol : str
            Line search convergence tolerance (default = 0.5).

        lstrun : str
            Truncation key for the line search parameter. Default = OFF, meaning no truncation. To
            activation truncation, input the number of digits to use after the decimal point for the line
            search parameter. (See `Line Search
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_tool10.html#eq7ef4bddb-f782-469d-ad98-a2e8f4a9309c>`_

        Notes
        -----

        .. _LNSRCH_notes:

        Activates a line search to be used with the Newton-Raphson method ( :ref:`nropt` ). Line search is
        an alternative to adaptive descent (see `Line Search
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_tool10.html#eq7ef4bddb-f782-469d-ad98-a2e8f4a9309c>`_

        :ref:`lnsrch`,AUTO can be very efficient for problems in which :ref:`lnsrch` is needed at only
        certain substeps.

        You cannot use line search ( :ref:`lnsrch` ), automatic time stepping ( :ref:`autots` ), or the DOF
        solution predictor ( :ref:`pred` ) with the arc-length method ( :ref:`arclen`, :ref:`arctrm` ). If
        you activate the arc-length method after you set :ref:`lnsrch`, :ref:`autots`, or :ref:`pred`, a
        warning message appears. If you choose to proceed with the arc-length method, the program disables
        your line search, automatic time stepping, and DOF predictor settings, and the time step size is
        controlled by the arc-length method internally.

        This command is also valid in PREP7.
        """
        command = f"LNSRCH,{key},{lstol},{lstrun}"
        return self.run(command, **kwargs)

    def ncnv(
        self,
        kstop: int | str = "",
        dlim: str = "",
        itlim: str = "",
        etlim: str = "",
        cplim: str = "",
        **kwargs,
    ):
        r"""Sets the key to terminate an analysis.

        Mechanical APDL Command: `NCNV <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_NCNV.html>`_

        Parameters
        ----------
        kstop : int or str
            Program behavior upon nonconvergence:

            * ``0`` - Do not terminate the analysis if the solution fails to converge.

            * ``1`` - Terminate the analysis and the program execution if the solution fails to converge
              (default).

            * ``2`` - Terminate the analysis, but not the program execution, if the solution fails to converge.

        dlim : str
            Terminates program execution if the largest nodal DOF solution value (displacement, temperature,
            etc.) exceeds this limit. Defaults to 1.0E6 for all DOF except MAG and A. Defaults to 1.0E10 for
            MAG and A.

        itlim : str
            Terminates program execution if the cumulative iteration number exceeds this limit (defaults to
            infinity).

        etlim : str
            Terminates program execution if the elapsed time (seconds) exceeds this limit (defaults to
            infinity).

        cplim : str
            Terminates program execution if the CPU time (seconds) exceeds this limit (defaults to
            infinity).

        Notes
        -----

        .. _NCNV_notes:

        Sets the key to terminate an analysis if not converged, or if any of the following limits are
        exceeded for nonlinear and full transient analyses: DOF (displacement), cumulative iteration,
        elapsed time, or CPU time limit. Applies only to static and transient analyses ( :ref:`antype`
        ,STATIC and :ref:`antype`,TRANS). Time limit checks are made at the end of each equilibrium
        iteration.

        This command is also valid in PREP7.
        """
        command = f"NCNV,{kstop},{dlim},{itlim},{etlim},{cplim}"
        return self.run(command, **kwargs)

    def neqit(self, neqit: str = "", forcekey: str = "", **kwargs):
        r"""Specifies the maximum number of equilibrium iterations for nonlinear analyses.

        Mechanical APDL Command: `NEQIT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_NEQIT.html>`_

        Parameters
        ----------
        neqit : str
            Maximum number of equilibrium iterations allowed each substep.

        forcekey : str
            One iteration forcing key:

            * ``FORCE`` - Forces one iteration per substep. Leave this field blank otherwise.

            Using one iteration per substep may result in unconverged solutions for nonlinear analysis, and the
            program may not indicate divergence in this case. This option is intended primarily for use by the
            Ansys Workbench interface. Keep in mind that forcing one iteration per substep is only recommended under
            very specific conditions; for example, nonlinearity in bonded penalty type contact. Under these
            conditions the solution typically converges in one iteration.

        Notes
        -----

        .. _NEQIT_notes:

        This command is also valid in PREP7.
        """
        command = f"NEQIT,{neqit},{forcekey}"
        return self.run(command, **kwargs)

    def nladaptive(
        self,
        component: str = "",
        action: str = "",
        criterion: str = "",
        option: str = "",
        val1: str = "",
        val2: str = "",
        val3: str = "",
        val4: str = "",
        **kwargs,
    ):
        r"""Defines the criteria under which the mesh is refined or modified during a nonlinear solution.

        Mechanical APDL Command: `NLADAPTIVE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_NLADAPTIVE.html>`_

        Parameters
        ----------
        component : str
            Specifies the element component upon which this command should act:

            * ``ALL`` - All selected components, or all selected elements if no component is selected (default).

            * ``Name`` - Component name.

        action : str
            Action to perform on the selected component(s):

            * ``ADD`` - Add a criterion to the database.

            * ``LIST`` - List the criteria defined for the specified component(s).

            * ``OCTREE`` - Enable adaptive mesh coarsening for additive manufacturing process simulation using
              the AM octree method.

            * ``DELETE`` - Delete the criteria defined for the specified component(s).

            * ``ON`` - Enable the defined criteria for the specified component(s) and specify how frequently and
              when to check them (via ON, ``VAL1``, ``VAL2``, ``VAL3`` ):

              ``VAL1`` -- Checking frequency. If > 0, check criteria at every ``VAL1`` substeps. If < 0, check
              criteria at each of the ``VAL1`` points (approximately equally spaced) between ``VAL2`` and
              ``VAL3``. (Default = -1.)

              ``VAL2`` -- Checking start time, where ``VAL2`` < ``VAL3``. (Default = Start time of load step.)

              ``VAL3`` -- Checking end time, where ``VAL3`` > ``VAL2``. (Default = End time of load step.)

              ``VAL4`` -- ``SOLID187`` element type ID (defined prior to issuing this command). Valid only for
              ``SOLID185`` or ``SOLID186`` components in a `NLAD-ETCHG analysis
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_nlad/nladetchgexample.html>`_.

            * ``OFF`` - Disable the defined criteria for the specified component(s).

        criterion : str
            Type of criterion to apply to the selected component(s):

            * ``CONTACT`` - Contact-based. Valid only for ``Action`` = ADD, ``Action`` = LIST, or ``Action`` =
              DELETE.

            * ``ENERGY`` - Energy-based. Valid only for ``Action`` = ADD, ``Action`` = LIST, or ``Action`` =
              DELETE.

            * ``BOX`` - A position-based criterion, defined by a box. Valid only for ``Action`` = ADD,
              ``Action`` = LIST, or ``Action`` = DELETE.

            * ``MESH`` - A mesh-quality-based criterion. Valid only for ``Action`` = ADD, ``Action`` = LIST, or
              ``Action`` = DELETE.

            * ``ALL`` - All criteria and options. Valid only for ``Action`` = LIST or ``Action`` = DELETE.
              ``Option`` and all subsequent arguments are ignored.

        option : str
            Criterion option to apply to the selected component(s):

            * ``NUMELEM`` - For target elements only, defines the minimum number of contact elements to contact
              with each target element. If this criterion is not satisfied, the program refines the contact
              elements and the associated solid elements. For this option, ``VAL1`` must be a positive integer.

              Valid only for ``Criterion`` = CONTACT and ``Action`` = ADD, LIST, or DELETE.

            * ``MEAN`` - Checks the strain energy of any element that is part of the defined component for the condition E:sub:`e` ≥ c:sub:`1` * E:sub:`total` / ``NUME`` (where c:sub:`1` = ``VAL1``, E:sub:`total` is the total strain energy of the component, and ``NUME`` is the number of elements of the component). If this criterion is satisfied at an element, the program refines the element. ``VAL1`` must be non-negative. Default = 1.

              Valid only for ``Criterion`` = ENERGY and ``Action`` = ADD, LIST, or DELETE.

            * ``XYZRANGE`` - Defines the location box in which all elements within are to be split or refined.
              Up to six values following the ``Option`` argument (representing the x1, x2, y1, y2, z1, and z2
              coordinates) are allowed. An unspecified coordinate is not checked.

              Valid only for ``Criterion`` = BOX and ``Action`` = ADD, LIST, or DELETE.

            * ``LAYER`` - Sets layer options for AM octree adaptive meshing for additive simulations.

              * ``VAL1`` - Number of layers to keep at fine mesh resolution between the current, top layer and the
                layers to be remeshed. Default = 2.
              * ``VAL2`` - Number of buffer elements to keep at fine mesh resolution between the part edges and
                the remeshed elements. Default = 2.

              Valid only for ``Action`` = OCTREE.

            * ``SKEWNESS`` - Mesh-quality-control threshold for elements ``SOLID187``, ``SOLID285``, and ``SOLID227`` :

              * ``VAL1`` - Defines skewness. Valid values: 0.0 through 1.0. Default = 0.9.
              * ``VAL2`` - Maximum Jacobian ratio at element integration points ( ``SOLID187`` and ``SOLID227``
                only). Valid values: 0.0 to 1.0. Default = 0.1.

              Valid only for ``Criterion`` = MESH and ``Action`` = ADD, LIST, or DELETE.

            * ``SHAPE`` - Mesh-quality control threshold for elements ``PLANE182`` and ``PLANE222``. Also
              applies to ``SOLID185`` and ``SOLID186`` in a `NLAD-ETCHG analysis
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_nlad/nladetchgexample.html>`_.

              ``VAL1`` -- Maximum corner angle of an element in degrees. Valid values are 0 through 180. Default =
              160 (2D analysis) or 155 (3D analysis). An element is remeshed when any of its corner angles reach
              the specified value.

              Valid only for ``Criterion`` = MESH and ``Action`` = ADD, LIST, or DELETE.

            * ``WEAR`` - For contact elements having surface wear specified ( :ref:`tb`,WEAR) only, defines
              ``VAL1`` as a critical ratio of magnitude of wear to the average depth of the solid element
              underlying the contact element. Once this critical ratio is reached for any element, the program
              morphs the mesh to improve the quality of the elements. ``VAL1`` must be a positive integer.

              Valid only for ``Criterion`` = CONTACT and ``Action`` = ADD, ``Action`` = LIST, or ``Action`` =
              DELETE. Cannot be combined with any other option during solution.

            * ``CZM`` - For contact elements with `cohesive zone material
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_nlad/advmnacriteria.html#nladrefsubstep>`_
              ( :ref:`tb`,CZM) only, defines ``VAL1`` as a critical value of change in released energy due to
              debonding between reference and current substep, and ``VAL2`` as the critical value for the change
              in the damage parameter between neighboring elements. Both values can be applied separately or
              together.

              When the critical value is reached (for either of the defined options) for one contact element, the
              solid elements underlying that contact element and the corresponding deformable target element are
              selected as candidates for remeshing.

              ``VAL1`` must be > 0. ``VAL2`` must be > 0 and < 1. No default.

              Valid only for ``Criterion`` = CONTACT and ``Action`` = ADD, LIST, or DELETE. Combing the CZM
              criterion with `mesh-quality-based
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_nlad/advmnacriteria.html#advmnlaskewnessopt>`_
              criteria may be necessary to improve distorted elements.

            * ``ALL`` - All options. Valid only for ``Action`` = LIST or ``Action`` = DELETE. All subsequent
              arguments are ignored.

        val1 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_NLADAPTIVE.html>`_ for
            further information.

        val2 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_NLADAPTIVE.html>`_ for
            further information.

        val3 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_NLADAPTIVE.html>`_ for
            further information.

        val4 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_NLADAPTIVE.html>`_ for
            further information.

        Notes
        -----

        .. _NLADAPTIVE_notes:

        If a specified component ( ``Component`` ) is an assembly, the defined criterion applies to all
        element components included in the assembly.

        All components must be defined and selected before the first solve ( :ref:`solve` ), although their
        nonlinear adaptivity criteria can be modified from load step to load step, and upon restart. For
        nonlinear adaptivity to work properly, ensure that all components are selected before each solve.

        After issuing this command to define a new criterion, the new criterion becomes active. The program
        checks the new criterion once per load step, roughly in mid-loading (unless this behavior is changed
        via ``Action`` = ON).

        When a criterion is defined, it overwrites a previously defined criterion (if one exists) through
        the same component, or through the component assembly that includes the specified component.

        During solution, the same criteria defined for an element through different components are combined,
        and the tightest criteria and action control ( ``Action``,ON, ``VAL1`` ) are used. If an ON action
        is defined by a positive ``VAL1`` value through one component and a negative ``VAL1`` value through
        another, the program uses the positive value.

        When the AM octree option is specified ( ``Action`` = OCTREE), the checking frequency ( Action,ON,,
        VAL1 ), checking start time ( Action,ON, VAL2 ), and checking end time ( Action,ON, VAL3 )
        control the checking layer frequency, start layer, and end layer respectively. If start and end
        layers are not specified, the start layer will default to the checking frequency, and the end layer
        will default to the final layer of the AM simulation.

        If ``VAL1`` < 0, the program checks ``VAL1`` points between ``VAL2`` and ``VAL3``. The time interval
        between each check points is determined by ( ``VAL3`` - ``VAL2`` ) / ( ``VAL1`` + 1), with the first
        check point as close to ``VAL2`` + ( ``VAL3`` - ``VAL2`` ) / ( ``VAL1`` + 1) as possible. Fewer
        check points can be used if the number of substeps during solution is insufficient (as the program
        can only check at the end of a substep).

        If ``VAL2`` (start time) and/or ``VAL3`` (end time) are unspecified or invalid, the program uses the
        start and/or end time (respectively) of the load step.

        ``VAL1`` applies to tetrahedral elements ``SOLID187``, ``SOLID227``, and ``SOLID285``. When the
        skewness of an element is >= ``VAL1``, the element is used as the core (seed) element of the
        remeshed region(s). The most desirable skewness value is 0, applicable when the element is a
        standard tetrahedral element; the highest value is 1, applicable when the element becomes flat with
        zero volume. To bypass skewness checking (not recommended), set ``VAL1`` = 0.

        ``VAL2`` represents the Jacobian ratio and is required for tetrahedral elements ``SOLID187`` and
        ``SOLID227``. When the maximum Jacobian ratio of an element is <= ``VAL2``, the element is used as
        the core (seed) element of the remeshed region(s). The most desirable maximum Jacobian ratio is 1,
        when the element is a standard tetrahedral element; the lowest reported value is -1, when the
        element is turned inside out. To bypass maximum Jacobian ratio checking (not recommended), set
        ``VAL2`` = 0.

        If this criterion is used with any other criteria defined for the same component, and a mesh change
        is requested at the same substep, all criteria defined are considered together. For more information
        about this special case, see `Simultaneous Quality- and Refinement-Based Remeshing
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_nlad/advmnanewmesh.html#>`_

        For more information about skewness, maximum Jacobian ratio, and remeshing, see `Nonlinear Mesh
        Adaptivity <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_nlad/advmnaexample.html>`_

        For more granular control of the source mesh geometry, see :ref:`nlmesh`.
        """
        command = f"NLADAPTIVE,{component},{action},{criterion},{option},{val1},{val2},{val3},{val4}"
        return self.run(command, **kwargs)

    def nldiag(self, label: str = "", key: str = "", maxfile: str = "", **kwargs):
        r"""Sets nonlinear diagnostics functionality.

        Mechanical APDL Command: `NLDIAG <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_NLDIAG.html>`_

        Parameters
        ----------
        label : str
            Diagnostic function:

            * ``NRRE`` - Store the Newton-Raphson residuals information.

            * ``EFLG`` - Identify or display elements or nodes that violate the criteria.

            * ``CONT`` - Write contact information to a single :file:`Jobname.cnd` diagnostic text file during
              solution.

        key : str
            Diagnostic function characteristics:

            * ``OFF or 0`` - Suppresses writing of diagnostic information (default).

            * ``ON or 1`` - Writes diagnostic information to the :file:`Jobname.ndxxx`, :file:`Jobname.nrxxx`,
              or :file:`Jobname.cnd` file. (If ``Label`` = CONT, this option is the same as the SUBS option
              described below.)

            * ``ITER`` - Writes contact diagnostic information at each iteration. Valid only when ``Label`` =
              CONT.

            * ``SUBS`` - Writes contact diagnostic information at each substep. Valid only when ``Label`` =
              CONT.

            * ``LSTP`` - Writes contact diagnostic information at each load step. Valid only when ``Label`` =
              CONT.

            * ``STAT`` - Lists information about the diagnostic files in the current working directory.

            * ``DEL`` - Deletes all diagnostic files in the current working directory.

        maxfile : str
            Maximum number of diagnostic files to create. Valid values are 1 through 999. Default = 4. Valid
            only when ``Label`` = NRRE or EFLG.

            Information is written to :file:`Jobname.ndxxx` or :file:`Jobname.nrxxx`, where ``xxx`` iterates
            from 001 through ``MAXFILE``. When the specified maximum number of diagnostic files is reached,
            the counter resets to 001 and earlier files are overwritten. The ``MAXFILE`` value specified for
            this ``Label`` function applies until a new value is specified.

        Notes
        -----

        .. _NLDIAG_notes:

        The :ref:`nldiag` command is a nonlinear diagnostics tool valid for nonlinear analyses that include
        structural degrees of freedom. It is a debugging tool for use when you must restart after an
        unconverged solution. The command creates :file:`Jobname.ndxxx`, :file:`Jobname.nrxxx`, or
        :file:`Jobname.cnd` files in the working directory to store the information you specify.

        For more information, see.

        Issue the :ref:`nldiag`,NRRE,ON command to create :file:`Jobname.nrxxx` diagnostic files (for each
        equilibrium iteration after the first) in which to store the relevant Newton-Raphson residual
        information of FX, FY, FZ (forces), MX, MY, MZ (moments), HEAT (heat flow), AMPS (current flow),
        CHRG (electric charge), or RATE (diffusion flow rate) for the last ``MAXFILE`` equilibrium
        iterations.

        Issue a :ref:`nldpost`,NRRE,STAT command to list the load step, substep, time, and equilibrium
        iteration corresponding to each of the :file:`Jobname.nrxxx` diagnostic files in the working
        directory, then issue a :ref:`plnsol`,NRRES,, ``FileID`` command to point to the file from which
        you want to create a contour plot of your Newton-Raphson residuals.

        If you restart or issue a new :ref:`solve` command, any :file:`Jobname.nrxxx` diagnostic files in
        the current (working) directory are overwritten.

        Issue a :ref:`nldiag`,EFLG,ON command to create :file:`Jobname.ndxxx` diagnostic files which store
        IDs for elements violating the following criteria:

        * Too large a distortion (HDST)

        * Elements contain nodes that have near zero pivots (PIVT) for nonlinear analyses

        * Too large a plastic/creep (EPPL/EPCR) strain increment ( :ref:`cutcontrol` )

        * Elements for which mixed u-P constraints are not satisfied (mixed U-P option of 18 ``x`` solid
          elements only) (MXUP)

        * Hyperelastic element (EPHY), cohesive zone material (EPCZ), or damage strain (EPDM) not converged

        * Radial displacement (RDSP) not converged

        * ``MPC184`` multipoint constraint elements using KEYOPT(1) = 6 through 16 with the Lagrange
          multiplier option fail to satisfy constraint conditions (184J)

        For :ref:`nldiag`,EFLG,ON, all :file:`Jobname.ndxxx` diagnostic files (for each equilibrium
        iteration after the first) in the current (working) directory are deleted when you issue a new
        :ref:`solve` command (or restart).

        In the solution processor ( :ref:`slashsolu` ), use the STAT option to list the active status of
        this command. In the postprocessor ( :ref:`post1` ), issue a :ref:`nldpost`,EFLG,STAT command to
        list the load step, substep, time, and equilibrium iteration corresponding to each of the
        :file:`Jobname.ndxxx` diagnostic files in the working directory, then issue a
        :ref:`nldpost`,EFLG,CM, ``FileID`` command to create element components that violate the criteria.

        Issue the :ref:`nldiag`,CONT,ON command to create a :file:`Jobname.cnd` diagnostic file which stores
        contact information for all defined contact pairs at all substeps. Alternatively, you may issue one
        of the following commands to store contact information at a specific frequency:

        * :ref:`nldiag`,CONT,ITER to write at each iteration

        * :ref:`nldiag`,CONT,SUBS to write at each substep (default)

        * :ref:`nldiag`,CONT,LSTP to write at each load step

        Contact diagnostic information is available for elements ``CONTA172``, ``CONTA174``, ``CONTA175``,
        and ``CONTA177`` ; it is not available for ``CONTA178``.

        Diagnostic file :file:`Jobname.cnd` is written during solution and lists, on a pair-base, the
        following contact information:

        * Contact pair ID :ref:`NLDIAGfootnt1` :sup:`[1]`

        * Number of contact elements in contact :ref:`NLDIAGfootnt2` :sup:`[2]`

        * Number of contact elements in sticking contact status

        * Maximum chattering level

        * Maximum contact penetration/Minimum gap :ref:`NLDIAGfootnt3` :sup:`[3]`

        * Maximum geometric gap

        * Maximum normal contact stiffness

        * Minimum normal contact stiffness

        * Maximum resulting pinball

        * Maximum elastic slip distance

        * Maximum tangential contact stiffness

        * Minimum tangential contact stiffness

        * Maximum sliding distance (algebraic sum)

        * Maximum contact pressure

        * Maximum friction stress

        * Average contact depth

        * Maximum geometric penetration

        * Number of contact points having too much penetration

        * Contacting area

        * Maximum contact damping pressure

        * Maximum tangential contact damping stress

        * Maximum total sliding distance ( GSLID ), including near-field

        * Minimum total sliding distance ( GSLID ), including near-field

        * Maximum normal fluid penetration pressure on contact surface

        * Maximum normal fluid penetration pressure on target surface

        * Total volume lost due to wear for the contact pair

        * Total strain energy due to contact constraint :ref:`NLDIAGfootnt6` :sup:`[6]`

        * Total frictional dissipation energy :ref:`NLDIAGfootnt6` :sup:`[6]`

        * Total contact stabilization energy :ref:`NLDIAGfootnt6` :sup:`[6]`

        * Ansys Workbench contact pair ID :ref:`NLDIAGfootnt4` :sup:`[4]`

        * Total force due to contact pressure - X component

        * Total force due to contact pressure - Y component

        * Total force due to contact pressure - Z component :ref:`NLDIAGfootnt5` :sup:`[5]`

        * Total force due to tangential stress - X component

        * Total force due to tangential stress - Y component

        * Total force due to tangential stress - Z component :ref:`NLDIAGfootnt5` :sup:`[5]`

        * Number of contact points having too much sliding for small sliding contact

        * Pair-based force convergence norm :ref:`NLDIAGfootnt7` :sup:`[7]`

        * Pair-based force convergence criterion :ref:`NLDIAGfootnt7` :sup:`[7]`

        * Maximum tangential fluid penetration pressure on contact surface

        * Maximum tangential fluid penetration pressure on target surface

        * Maximum sliding distance for closed contact in the current substep

        .. _NLDIAGfootnt1:

        Contact pair ID. A positive number refers to a real constant ID for a pair-based contact definition.
        A negative number refers to a section ID of a surface in a general contact definition. (See
        `Comparison of Pair-Based Contact and General Contact
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_ctec/ctec_comppairgen.html#gcfeatnotsup>`_

        .. _NLDIAGfootnt2:

        Number of contact elements in contact. Other values are interpreted as follows:

        * 0 indicates that the contact pair is in near-field contact status. * -1 indicates that the contact
        pair is in far-field contact status. * -2 indicates that the contact pair is inactive ( symmetric to
        asymmetric contact ).

        .. _NLDIAGfootnt3:

        A positive value indicates penetration and a negative value indicates a gap. If the contact pair has
        a far-field contact status, penetration and gap are not available and the value stored is the
        current pinball radius.

        .. _NLDIAGfootnt4:

        Intended primarily for internal use in the contact tracking of Ansys Workbench.

        .. _NLDIAGfootnt5:

        In a 3D model, the reported item is total force along the Z-axis. In a 2D axisymmetric model (with
        or without ROTY), the reported item is maximum torque that can potentially act on the Y-axis.

        .. _NLDIAGfootnt6:

        The pair-based dissipation energy and stabilization energy do not include contributions from contact
        elements that are in far-field. The pair-based strain energy does not include the frictional
        dissipation energy and stabilization energy; it only contains an elastic recovery energy when the
        contact status changes from closed to open.

        .. _NLDIAGfootnt7:

        The program uses a default tolerance value of 0.1 to calculate the pair-based force convergence norm
        and pair-based force convergence criterion. This is not a check for local convergence. It is for
        monitoring purposes only and is useful for nonlinear contact diagnostics.

        In the solution processor ( :ref:`slashsolu` ), use the :ref:`nldiag`,CONT,STAT command to list the
        active status of the contact information. If you subsequently issue a new :ref:`solve` command (or
        restart), the :file:`Jobname.cnd` diagnostic file in the current (working) directory is not deleted;
        information is appended to it. Delete the existing diagnostic file ( :ref:`nldiag`,CONT,DEL command)
        if you do not want to retain diagnostic information from previous solutions.
        """
        command = f"NLDIAG,{label},{key},{maxfile}"
        return self.run(command, **kwargs)

    def nlgeom(self, key: str = "", **kwargs):
        r"""Includes large-deflection effects in a static or full transient analysis.

        Mechanical APDL Command: `NLGEOM <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_NLGEOM.html>`_

        Parameters
        ----------
        key : str
            Large-deflection key:

            * ``OFF`` - Ignores large-deflection effects (that is, a small-deflection analysis is specified).
              This option is the default.

            * ``ON`` - Includes large-deflection (large rotation) effects or large strain effects, according to
              the element type.

        Notes
        -----

        .. _NLGEOM_notes:

        Large-deflection effects are categorized as either large deflection (or large rotation) or large
        strain, depending on the element type. These are listed (if available) under Special Features in the
        input data table for each element in the `Element Reference
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_BIBLIO.html>`_. When large
        deflection effects are included (
        :ref:`nlgeom`,ON), stress stiffening effects are also included automatically.

        If used during the solution ( :ref:`slashsolu` ), this command is valid only within the first load
        step.

        In a large-deflection analysis, pressure loads behave differently than other load types. For more
        information, see `Load Direction in a Large-Deflection Analysis
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STRnlbasin.html#aQAlprb2tlm>`_.

        The gyroscopic matrix (that occurs due to rotational angular velocity) does not support large-
        deflection effects. The theoretical formulations for the gyroscopic matrix support small deflection
        (linear formulation) only.

        When large-deflection effects are included in a substructure or CMS transient analysis use pass, the
        :ref:`outres` command ignores ``DSUBres`` = ALL.

        This command is also valid in PREP7.
        """
        command = f"NLGEOM,{key}"
        return self.run(command, **kwargs)

    def nlhist(
        self,
        key: str = "",
        name: str = "",
        item: str = "",
        comp: str = "",
        node: str = "",
        elem: str = "",
        shell: str = "",
        layer: str = "",
        stop_value: str = "",
        stop_cond: int | str = "",
        **kwargs,
    ):
        r"""Specify results items to track during solution.

        Mechanical APDL Command: `NLHIST <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_NLHIST.html>`_

        Parameters
        ----------
        key : str
            Specifies the command operation:

            * ``NSOL`` - Nodal solution data.

            * ``ESOL`` - Element nodal data.

            * ``PAIR`` - Contact data (for pair-based contact).

            * ``GCN`` - Contact data (for general contact).

            * ``RSEC`` - `Result section
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/str_resultsec.html#>`_ data.

            * ``STAT`` - Displays a list of items to track.

            * ``OFF or 0`` - Deactivates tracking of all variables. This value is the default.

            * ``ON or 1`` - Activates tracking of all variables. Tracking also activates whenever any
              specification changes.

            * ``DEL`` - Removes the specified variable from the set of result items to track. If ``Name`` = ALL
              (default), all specifications are removed.

        name : str
            The 32-character user-specified name.

        item : str
            Predetermined output item and component label for valid elements. See the `Element Reference
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_BIBLIO.html>`_ for more
            information.

        comp : str
            Predetermined output item and component label for valid elements. See the `Element Reference
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_BIBLIO.html>`_ for more
            information.

        node : str
            Number identifying one of the following:

            * Valid node number (if ``Key`` = NSOL or ESOL).
            * Valid real constant set number identifying a contact pair (if ``Key`` = PAIR).
            * Valid section ID number identifying a surface of a general contact definition (if ``Key`` = GCN).
            * Valid real constant set number identifying a result section (if ``Key`` = RSEC).
             ``NODE`` is required input when ``Key`` = NSOL, ESOL, PAIR, GCN, or RSEC.

        elem : str
            Valid element number for element results. Used for ESOL items. If ``ELEM`` is specified, then a
            node number that belongs to the element must also be specified in the ``NODE`` field.

        shell : str
            Valid labels are TOP, MID or BOT. This field can specify the location on shell elements for
            which to retrieve data. Used only for element nodal data (ESOL).

        layer : str
            Layer number (for layered elements only). Used only for element nodal data (ESOL).

        stop_value : str
            Critical value of the tracked variable. This value is used to determine if the analysis should
            be terminated.

        stop_cond : int or str
            Specifies the conditional relationship between the variable being tracked and the ``STOP_VALUE`` upon which the analysis will be terminated:

            * ``-1`` - Terminate the analysis when the tracked variable is less than or equal to ``STOP_VALUE``.

            * ``0`` - Terminate the analysis when the tracked variable equals ``STOP_VALUE``.

            * ``1`` - Terminate the analysis when the tracked variable is greater than or equal to
              ``STOP_VALUE``.

        Notes
        -----

        .. _NLHIST_notes:

        The :ref:`nlhist` command is a nonlinear diagnostics tool that enables you to monitor diagnostics
        results of interest in real time during a solution.

        You can track a maximum of 50 variables during solution. The specified result quantities are written
        to the file :file:`Jobname.nlh`. Nodal results and contact results are written for every converged
        substep (irrespective of the :ref:`outres` command setting), while element results are written only
        at time points specified via the :ref:`outres` command. Result section data is written only at time
        points specified via the :ref:`outpr`,RSO, ``Freq`` command.

        For time points where element results data is not available, a very small number is written instead.
        If the conditions for contact to be established are not satisfied, 0.0 will be written for contact
        results.

        Results tracking is available for:

        * nonlinear structural analyses (static or transient)

        * nonlinear steady-state thermal analyses

        * transient thermal analyses (linear or nonlinear)

        * nonlinear coupled structural-thermal analyses (static or transient)

        All results are tracked in the Solution Coordinate System (that is, nodal results are in the nodal
        coordinate system and element results are in the element coordinate system).

        Contact results can be tracked for elements ``CONTA172``, ``CONTA174``, ``CONTA175``, and
        ``CONTA177`` ; they cannot be tracked for ``CONTA178``.

        `Result section
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/str_resultsec.html#>`_ data can be
        tracked for elements ``CONTA172`` and ``CONTA174``.

        When contact results ( ``Key`` = PAIR or GCN) or result section data ( ``Key`` = RSEC) are tracked,
        the user-specified name ( ``Name`` argument) is used to create a user-defined parameter. This
        enables you to monitor the parameter during solution. As an example, you can use a named parameter
        to easily convert the contact stiffness units from FORCE/LENGTH :sup:`3` to FORCE/LENGTH based on
        the initial contact area CAREA. Be sure to specify ``Name`` using the `APDL parameter naming
        convention
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_apdl/Hlp_P_APDL3_2.html#apdlhidparmtlm8599>`_.

        The ``STOP_VALUE`` and ``STOP_COND`` arguments enable you to automatically terminate the analysis
        when a desired value for a tracked contact result or section result has been reached. This
        capability is only available for contact variables ( ``Key`` = PAIR or GCN) and result section
        variables ( ``Key`` = RSEC ).

        The :file:`Jobname.nlh` file is an ASCII file that lists each time point at which a converged
        solution occurs along with the values of the relevant result quantities.

        The GUI option Solution> Results tracking provides an interface to define the result items to be
        tracked. The GUI also allows you to graph one or more variables against time or against other
        variables during solution. You can use the interface to graph or list variables from any
        :file:`.nlh` file generated by Mechanical APDL.

        You can also track results during batch runs. Either access the `launcher
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/install_misc/launcherhelp.html#laumenuopts>`_
        and select ``Run Results Tracker Utility`` from the Tools menu, or type
        :file:`nlhist232` at the command line. Use the supplied file browser to
        navigate to your :file:`Jobname.nlh` file, and click on it to invoke the tracking utility. You can
        use this utility to read the file at any time, even after the solution is complete (the data in the
        file must be formatted correctly).

        .. _nlhist_nsol_tab:

        NLHIST - Valid NSOL Item and Component Labels
        *********************************************

        .. flat-table::
           :header-rows: 1

           * - Item
             - Comp
             - Description
           * - U
             - X, Y, Z
             - X, Y, or Z structural displacement.
           * - ROT
             - X, Y, Z
             - X, Y, or Z structural rotation.
           * - F
             - X, Y, Z
             - X, Y, or Z structural reaction force.
           * - M
             - X, Y, Z
             - X, Y, or Z structural reaction moment.
           * - TEMP [ :ref:`nlhist_nsol_tabnote1` ]
             - -
             - Temperature.
           * - TEMP
             - MAX, MIN
             - Maximum or minimum temperature in the model.
           * - HEAT [ :ref:`nlhist_nsol_tabnote2` ]
             - -
             - Reaction heat flow.

        .. _nlhist_nsol_tabnote1:

        For ``SHELL131`` and ``SHELL132`` elements with KEYOPT(3) = 0 or 1, use the labels TBOT, TE2, TE3,.
        .., TTOP instead of TEMP.

        .. _nlhist_nsol_tabnote2:

        For ``SHELL131`` and ``SHELL132`` elements with KEYOPT(3) = 0 or 1, use the labels HBOT, HE2, HE3,.
        .., HTOP instead of HEAT.

        .. _nlhist_tab_1:

        NLHIST - Valid ESOL Item and Component Labels
        *********************************************

        .. flat-table::
           :header-rows: 1

           * - Item
             - Comp
             - Description
           * - S
             - X, Y, Z, XY, YZ, XZ
             - Component stress.
           * - "
             - 1, 2, 3
             - Principal stress.
           * - "
             - INT
             - Stress intensity.
           * - "
             - EQV
             - Equivalent stress.
           * - EPEL
             - X, Y, Z, XY, YZ, XZ
             - Component elastic strain.
           * - "
             - 1, 2, 3
             - Principal elastic strain.
           * - "
             - INT
             - Elastic strain intensity.
           * - "
             - EQV
             - Elastic equivalent strain.
           * - EPPL
             - X, Y, Z, XY, YZ, XZ
             - Component plastic strain.
           * - "
             - 1, 2, 3
             - Principal plastic strain.
           * - "
             - INT
             - Plastic strain intensity.
           * - "
             - EQV
             - Plastic equivalent strain.
           * - EPCR
             - X, Y, Z, XY, YZ, XZ
             - Component creep strain.
           * - "
             - 1, 2, 3
             - Principal creep strain.
           * - "
             - INT
             - Creep strain intensity.
           * - "
             - EQV
             - Creep equivalent strain.
           * - EPTH
             - X, Y, Z, XY, YZ, XZ
             - Component thermal strain.
           * - "
             - 1, 2, 3
             - Principal thermal strain.
           * - "
             - INT
             - Thermal strain intensity.
           * - "
             - EQV
             - Thermal equivalent strain.
           * - EPDI
             - X, Y, Z, XY, YZ, XZ
             - Component diffusion strain.
           * - "
             - 1, 2, 3
             - Principal diffusion strain.
           * - "
             - INT
             - Diffusion strain intensity.
           * - "
             - EQV
             - Diffusion equivalent strain.
           * - NL
             - SEPL
             - Equivalent stress (from stress-strain curve).
           * - "
             - SRAT
             - Stress state ratio.
           * - "
             - HPRES
             - Hydrostatic pressure.
           * - "
             - EPEQ
             - Accumulated equivalent plastic strain.
           * - "
             - CREQ
             - Accumulated equivalent creep strain.
           * - "
             - PSV
             - Plastic state variable.
           * - "
             - PLWK
             - Plastic work/volume.
           * - TG
             - X, Y, Z, SUM
             - Component thermal gradient or vector sum.
           * - TF
             - X, Y, Z, SUM
             - Component thermal flux or vector sum.

        ETABLE items are not supported for :ref:`esol` items.

        PAIR solution quantities are output on a per contact pair basis. GCN solution quantities are output
        on a “per general contact section” basis. (See `Comparison of Pair-Based Contact and General Contact
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_ctec/ctec_comppairgen.html#gcfeatnotsup>`_
        :file:`Jobname.nlh` file represent a minimum or a maximum over the associated contact pair or
        general contact surface, as detailed in the table below.

        .. _nlhist_tab_2:

        NLHIST - Valid Contact (PAIR or GCN) Item and Component Labels
        **************************************************************

        .. flat-table::
           :header-rows: 1

           * - Item
             - Comp
             - Description
           * - CONT
             - ELCN
             - If >0, number of contact elements in contact. Other values are interpreted as follows:   * 0 indicates the contact pair (or GCN surface) is in near-field contact status. * -1 indicates the contact pair (or GCN surface) is in far-field contact status. * -2 indicates that the contact pair (or GCN surface) is inactive ( symmetric to asymmetric contact   ).
           * - "
             - ELST
             - Number of contact elements in sticking contact status
           * - "
             - CNOS
             - Maximum chattering level
           * - "
             - PENE
             - Maximum penetration (or minimum gap) [ :ref:`nlhist_tab2note1` ]
           * - "
             - CLGP
             - Maximum geometric gap
           * - "
             - SLID
             - Maximum total sliding distance (algebraic sum)
           * - "
             - SLMX
             - Maximum total sliding distance for closed contact in the current substep
           * - "
             - ESLI
             - Maximum elastic slip distance
           * - "
             - KNMX
             - Maximum normal contact stiffness
           * - "
             - KTMX
             - Maximum tangential contact stiffness
           * - "
             - KNMN
             - Minimum normal contact stiffness
           * - "
             - KTMN
             - Minimum tangential contact stiffness
           * - "
             - PINB
             - Maximum pinball radius
           * - "
             - PRES
             - Maximum contact pressure
           * - "
             - SFRI
             - Maximum frictional stress
           * - "
             - CNDP
             - Average contact depth
           * - "
             - CLPE
             - Maximum geometric penetration
           * - "
             - LGPE
             - Number of contact points having too much penetration
           * - "
             - CAREA
             - Contacting area
           * - "
             - NDMP
             - Maximum contact damping pressure
           * - "
             - TDMP
             - Maximum tangential contact damping stress
           * - "
             - GSMX
             - Maximum total sliding distance ( GSLID ), including near-field
           * - "
             - GSMN
             - Minimum total sliding distance ( GSLID ), including near-field
           * - "
             - FPSC
             - Maximum normal fluid penetration pressure on contact surface
           * - "
             - FPST
             - Maximum normal fluid penetration pressure on target surface
           * - "
             - WEAR
             - Total volume lost due to wear for the contact pair (not available for general contact, ``Key`` = GCN )
           * - "
             - CTEN
             - Total strain energy due to contact constraint [ :ref:`nlhist_tab2note2` ]
           * - "
             - CFEN
             - Total frictional dissipation energy [ :ref:`nlhist_tab2note2` ]
           * - "
             - CDEN
             - Total contact stabilization energy [ :ref:`nlhist_tab2note2` ]
           * - "
             - CFNX
             - Total force due to contact pressure - X component [ :ref:`nlhist_tab2note4` ]
           * - "
             - CFNY
             - Total force due to contact pressure - Y component [ :ref:`nlhist_tab2note4` ]
           * - "
             - CFNZ
             - Total force due to contact pressure - Z component [ :ref:`nlhist_tab2note4` ] [ :ref:`nlhist_tab2note5` ]
           * - "
             - CFSX
             - Total force due to tangential stress - X component [ :ref:`nlhist_tab2note4` ]
           * - "
             - CFSY
             - Total force due to tangential stress - Y component [ :ref:`nlhist_tab2note4` ]
           * - "
             - CFSZ
             - Total force due to tangential stress - Z component [ :ref:`nlhist_tab2note4` ] [ :ref:`nlhist_tab2note5` ]
           * - "
             - CTRQ
             - Maximum torque in an axisymmetric analysis with MU = 1.0
           * - "
             - LGSL
             - Number of contact points having too much sliding for small sliding contact
           * - "
             - NORM
             - Pair-based force convergence norm [ :ref:`nlhist_tab2note3` ]
           * - "
             - CRIT
             - Pair-based force convergence criterion [ :ref:`nlhist_tab2note3` ]
           * - "
             - FPTC
             - Maximum tangential fluid penetration pressure on contact surface
           * - "
             - FPTT
             - Maximum tangential fluid penetration pressure on target surface

        .. _nlhist_tab2note1:

        For PENE, a positive value indicates a penetration, and a negative value indicates a gap. If the
        contact pair (or GCN surface) has a far-field contact status, penetration and gap are not available,
        and the value stored for PENE is the current pinball radius.

        .. _nlhist_tab2note2:

        The pair-based dissipation energy (CFEN) and stabilization energy (CDEN) do not include
        contributions from contact elements that are in far-field. The pair-based strain energy (CTEN) does
        not include the frictional dissipation energy and stabilization energy; it only contains an elastic
        recovery energy when the contact status changes from closed to open.

        .. _nlhist_tab2note3:

        The program uses a default tolerance value of 0.1 to calculate the pair-based force convergence norm
        and pair-based force convergence criterion. This is not a check for local convergence. It is for
        monitoring purposes only and is useful for nonlinear contact diagnostics.

        .. _nlhist_tab2note4:

        If the specified contact pair is a `rigid surface or force-distributed constraint
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_ctec/Hlp_ctec_surfcon.html#strbeamso1703>`_
        that includes stress stiffening effects, this quantity represents a total constraint force or moment
        at the pilot node as shown below:

        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.

        .. _nlhist_tab2note5:

        For the case of 2D axisymmetric with torsion ( ``CONTA172`` with a ROTY DOF), CFNZ and CFSZ
        represent moments along the Y direction.

        NLHIST - Valid Result Section (RSEC) Item and Component Labels
        **************************************************************

        .. flat-table::
           :header-rows: 1

           * - Item
             - Comp
             - Description
           * - REST
             - SECF
             - Total section force
           * - "
             - SECM
             - Total section moment
           * - "
             - AXST
             - Section axial stress
           * - "
             - BDST
             - Section bending stress
           * - "
             - SPTX
             - Section center X coordinate
           * - "
             - SPTY
             - Section center Y coordinate
           * - "
             - SPTZ
             - Section center Z coordinate
           * - "
             - THXY
             - Rotation about local z
           * - "
             - THYZ
             - Rotation about local x
           * - "
             - THZX
             - Rotation about local y

        """
        command = f"NLHIST,{key},{name},{item},{comp},{node},{elem},{shell},{layer},{stop_value},{stop_cond}"
        return self.run(command, **kwargs)

    def nlmesh(self, control: str = "", val1: str = "", val2: str = "", **kwargs):
        r"""Controls remeshing in `nonlinear adaptivity
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_nlad/Hlp_G_ADVREZ.html>`_.

        Mechanical APDL Command: `NLMESH <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_NLMESH.html>`_

        Parameters
        ----------
        control : str
            The mesh-quality control to adjust:

            * ``NLAY`` - The sculpting layer adjustment:

              ``VAL1`` - The number of sculpting layers, beginning with detected seed elements. Valid for 2D and
              3D analysis.

              * Default: ``VAL1`` = 10 for 2D analysis, ``VAL1`` = 2 for 3D analysis.
              * For local (partial) remeshing, this option helps the remesher to detect remeshing regions from the
                whole deformed model.
              * Generally, a larger ``VAL1`` leads to larger remeshing regions and tends to unite isolated
                multiple regions. A larger value also tends to result in better remeshing quality (and increases
                mapping and solution overhead accordingly).
              * Only elements with the same element and material properties as seed elements are included into the
                remeshing regions.
              * ``VAL1`` = 0 is not valid, as the remeshing regions would contain only the detected seed elements,
                resulting in many small cavities within remeshing regions (especially if the specified mesh-
                quality metric threshold ( :ref:`nladaptive` ) is relatively large).

              ``VAL2`` - Same as ``VAL1``, except that ``VAL1`` controls remeshing to remove distortion and
              ``VAL2`` controls element refinement. Default: ``VAL2`` = 1 for 2D analysis, ``VAL2`` = 2 for 3D
              analysis.

              Not used in a `NLAD-ETCHG analysis
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_nlad/nladetchgexample.html>`_.

              For more information about this control, see `Sculpting Layers Control
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_nlad/advmnanewmesh.html#>`_

            * ``BDRA`` - The boundary angle threshold in degrees. Use this adjustment to retain geometry
              features of the original (source) mesh. Valid for both 2D and 3D analysis.

              In a 3D analysis, this value is the dihedral angle (the angle between the normal vectors from two
              neighboring surface facets). In a 2D analysis, this value is the 2D patch boundary edge normal
              angle. If the edge angle or dihedral angle is larger than the specified threshold, the node shared
              by 2D edges or edges shared by 3D facets are retained during remeshing.

              Valid values: 0 < ``VAL1`` < 80.

              Default for 2D analysis: ``VAL1`` = 10. Default for 3D analysis: ``VAL1`` = 15.

              Generally, a larger ``VAL1`` improves the quality of the new mesh (and may even repair local tiny
              edges or facets of poor quality). Too large a value, however, may also smooth out some geometric
              features, leading to slightly different results and possibly causing convergence issues in the
              substeps immediately following remeshing.

              For more information about this control, see `Boundary-Angle and Edge-Angle Control
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_nlad/advmnanewmesh.html#>`_

            * ``AEDG`` - The edge angle threshold in degrees. Valid for 3D analysis only.

              Use this control to split 3D patch segments. The edge angle is the angle between adjacent surface
              segment edges sharing a node. If the edge angle is larger than the specified threshold (VAL1), the
              segment splits and the node is automatically treated as a node to be retained.

              Default: ``VAL1`` = 10.

              Generally, a larger ``VAL1`` improves the quality of the new mesh, but may result in loss of feature
              nodes. The effect is similar to that of boundary angles ( ``Control`` = BDRA).

              For more information about this control, see `Boundary-Angle and Edge-Angle Control
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_nlad/advmnanewmesh.html#>`_

            * ``SRAT`` - The global sizing ratio. Valid for 2D and 3D analysis.

              ``VAL1`` - The global sizing ratio for remeshing.

              * Default: ``VAL1`` = 1.0. The default value results in the new mesh having a size similar to that
                of the original mesh.
              * Generally, set the value ( ``VAL1`` ) to >= 0.7. The model can be refined (< 1.0) or coarsened (>
                1.0) up to 3x depending on the mesh-sizing gradient and number of 3D elements, and approximately
                2x for 2D elements.

              ``VAL2`` - Same as ``VAL1``, except that ``VAL1`` controls remeshing to remove distortion and
              ``VAL2`` controls element refinement. Default: ``VAL2`` = 0.75.

              Not used in a `NLAD-ETCHG analysis
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_nlad/nladetchgexample.html>`_.

              For more information about this control, see `Global Sizing Control
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_nlad/advmnanewmesh.html#>`_

            * ``GRAD`` - Adjusts the new mesh-sizing gradient during remeshing. Valid for 2D and 3D analysis.

              Valid values: ``VAL1`` = 0, 1, 2, or 3. Default: ``VAL1`` = 2 for 2D analysis, ``VAL1`` = 3 for 3D
              analysis.

              * ``VAL1`` = 0 -- The mesh-sizing gradient is not retained. The new mesh is uniform and has an
                approximate average size on the entire remeshed domain(s), even if the original mesh has sizing
                gradients.
              * ``VAL1`` = 1 -- The new mesh follows the original mesh-sizing gradient to retain the element
                averaged-edge length. This value tends to coarsen the mesh in the location of the distorted
                elements during remeshing.
              * ``VAL1`` = 2 -- The new mesh follows the sizing gradient of the original mesh, with additional
                sizing compensation based on the element size change due to deformation during solution. This
                value tends to refine the mesh at the location of the distorted elements, where the distortion may
                have originated from deformation during solution.
              * ``VAL1`` = 3 -- Similar to ``VAL1`` = 2, but assumes that perfect mesh quality is not required,
                thus avoiding over-refinement of minor distorted regions. Valid for 3D analysis only.

              For more information about this control, see.

            * ``QTOL`` - The new mesh-acceptance tolerance ( ``PLANE182``, ``PLANE222``, ``SOLID187``,
              ``SOLID227``, and ``SOLID285`` ).

              ``VAL1`` - Controls remeshing to remove distortion. Default: 0.05.

              ``VAL2`` - Controls element refinement. Default: 0.5.

              For ``PLANE182`` and ``PLANE222``, ``VAL2`` is the only valid option (for mesh refinement), and the
              new mesh is accepted when ( MaxCornerAngleNew - MaxCornerAngleOld ) / MaxCornerAngleOld <= ``QTOL``.

              For ``SOLID285``, the new mesh is accepted when ( SkewnessNew - SkewnessOld ) / SkewnessOld <=
              ``QTOL``.

              For ``SOLID187`` and ``SOLID227``, the new mesh is accepted when, in addition to skewness, (
              JacobianOld - JacobianNew ) / JacobianOld <= ``QTOL``.

              The program uses both tolerance and mesh-quality parameters to determine whether or not a new mesh
              is accepted.

              Not used in a `NLAD-ETCHG analysis
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_nlad/nladetchgexample.html>`_.

            * ``REFA`` - The refinement algorithm adjustment ( ``PLANE182``, ``PLANE222``, and ``SOLID285`` ). Valid for 2D
              and 3D analysis.

              ``VAL1`` -

              * SPLIT - Use mesh `splitting
                <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_nlad/advmnanewmesh.html#>`_ instead of
                general remeshing. This is the only valid value.

              If not specified, mesh refinement occurs via general remeshing (except for ``PLANE183`` ).

              Not used in a `NLAD-ETCHG analysis
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_nlad/nladetchgexample.html>`_.

            * ``TCOR`` - Coordinate truncation adjustments for nodal locations of the meshes during remeshing. Valid for 2D
              and 3D analysis.

              ``VAL1`` -

              * ON - Truncates the decimal value after the seventh position. Default behavior for ``PLANE182``,
                ``PLANE222``, and ``SOLID285`` (augmented Lagrange and penalty contact formulations only).
              * OFF - No truncation occurs on the decimal value. Default behavior for ``SOLID187`` and
                ``SOLID227`` (all contact formulations), and ``PLANE182`` and ``PLANE222`` (Lagrange multiplier
                contact formulation only).
            * ``AGGR`` - Aggressive remeshing. Creates meshes with improved shape metrics. May change some global remeshing
              control parameters applied by other :ref:`nlmesh` commands, and may increase remeshing time. Valid
              for both 2D and 3D nonlinear adaptivity analysis.

              ``VAL1`` -

              * ON - Enable aggressive remeshing.
              * OFF - Disable aggressive remeshing (default).
            * ``ELSZ`` - Reduces the set of remeshable (seed) elements used for remeshing by filtering out
              elements based on their size, preventing over- or under-refinement in the remeshing regions. Valid
              only in `general remeshing
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_nlad/advmnanewmesh.html#nladsimultaneous>`_
              using an energy -, position-, or `contact
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_nlad/advmnacriteria.html#advczmcriterion>`_
              -based refinement criterion.

              ``Val1`` is a user-defined lower bound of the element size, and ``Val2`` is a user-defined upper
              bound of the element size. If both are specified, seed elements selected via the specified criterion
              are filtered out if their size is < ``Val1`` or > ``Val2``. If ``Val1`` is unspecified, only the
              size check with ``Val2`` occurs. If ``Val2`` is unspecified, only the size check with ``Val1``
              occurs.

            * ``NSTR`` - Reduces the set of remeshable (seed) elements used for remeshing by filtering out elements based on
              their (maximum) equivalent stress level, preventing over- or under-refinement in the remeshing
              regions based on the stress state. Valid only in `general remeshing
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_nlad/advmnanewmesh.html#nladsimultaneous>`_
              using an energy -, position-, or `contact
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_nlad/advmnacriteria.html#advczmcriterion>`_
              -based refinement criterion.

              ``Val1`` is a user-defined lower bound of element equivalent stress, and ``Val2`` is a user-defined
              upper bound of the element equivalent stress. If both are specified, seed elements selected by the
              specified criterion are filtered out if their (maximum) equivalent stress is < ``Val1`` or >
              ``Val2``. If ``Val1`` is unspecified, only the equivalent stress check with ``Val2`` occurs. If
              ``Val2`` is unspecified, only the equivalent stress check with ``Val1`` occurs.

              **Important:** Before specifying this option, copy the integration-point results to the nodes ( :ref:`eresx`,NO).

            * ``NSTN`` - Reduces the set of remeshable (seed) elements used for remeshing by filtering out elements based on
              their (maximum) equivalent strain level, preventing over- or under-refinement in the remeshing
              regions based on the strain state. Valid only in `general remeshing
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_nlad/advmnanewmesh.html#nladsimultaneous>`_
              using an energy -, position-, or `contact
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_nlad/advmnacriteria.html#advczmcriterion>`_
              -based refinement criterion.

              ``Val1`` is a user-defined lower bound of the element equivalent strain, and ``Val2`` is a user-
              defined upper bound of the element equivalent strain. If both are specified, seed elements selected
              by the specified criterion are filtered out if their (maximum) equivalent strain is < ``Val1`` or >
              ``Val2``. If ``Val1`` is unspecified, only the equivalent strain check with ``Val2`` occurs. If
              ``Val2`` is unspecified then only the equivalent strain check with ``Val1`` occurs.

              **Important:** Before specifying this option, copy the integration-point results to the nodes ( :ref:`eresx`,NO).

            * ``LIST`` - Lists all mesh-quality control parameters.

              If ``VAL1`` has been specified for a given mesh control, the most recently specified value is
              listed. If a value was not explicitly specified, the default value is listed (assuming that the
              problem has been solved at least once).

        val1 : str
            Numerical input value that varies according to the specified ``Control`` option.

            Valid for all ``Control`` options. Can be used when controlling remeshing for both distortion
            removal and for element refinement.

        val2 : str
            Numerical input value that varies according to the specified ``Control`` option.

            Valid only for these ``Control`` options: NLAY, SRAT, and QTOL. Also used for controlling
            remeshing for element refinement.

        Notes
        -----

        .. _NLMESH_notes:

        :ref:`nlmesh` is a global control command enabling mesh-quality adjustments for remeshing in
        `nonlinear adaptivity
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_nlad/advmnaexample.html>`_. The command
        can be used when components are associated with mesh-quality criteria ( :ref:`nladaptive` with
        ``Criterion`` = MESH, or another criterion with mesh change through general refinement).

        Issue the :ref:`nlmesh` command only in cases where advanced mesh-quality control is desirable for
        remeshing in nonlinear adaptivity. The control values specified apply to all components having mesh-
        quality-based criteria defined, or components having mesh change through general refinement, and can
        be modified at every load step during the nonlinear adaptive solution or when performing a restart
        analysis.
        """
        command = f"NLMESH,{control},{val1},{val2}"
        return self.run(command, **kwargs)

    def nropt(self, option1: str = "", option2: str = "", optval: str = "", **kwargs):
        r"""Specifies the Newton-Raphson options in a static or full transient analysis.

        Mechanical APDL Command: `NROPT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_NROPT.html>`_

        Parameters
        ----------
        option1 : str
            Option key:

            * ``AUTO`` - Let the program choose the option (default).

            * ``FULL`` - Use full Newton-Raphson.

            * ``MODI`` - Use modified Newton-Raphson.

            * ``INIT`` - Use the previously computed matrix (initial-stiffness).

            * ``UNSYM`` - Use full Newton-Raphson with unsymmetric matrices of elements where the unsymmetric
              option exists.

        option2 : str
            Option key:

            * ``CRPL`` - When applicable in a static creep analysis, activates modified Newton-Raphson with a
              creep-ratio limit. Valid only when ``Option1`` = AUTO.

        optval : str
            If ``Option2`` is blank, ``Optval`` is the Adaptive Descent Key ( ``Adptky`` ):

            * ``ON`` - Use adaptive descent (default if frictional contact exists). Explicit ON is valid only if
              ``Option`` = FULL.

            * ``OFF`` - Do not use adaptive descent (default in all other cases).

            If ``Option2`` = CRPL, ``Optval`` is the creep ratio limit:

            * ``CRLIMIT`` - The creep ratio limit for use with the modified Newton-Raphson procedure. Valid only
              when ``Option1`` = AUTO (default) and ``Option2`` = CRPL. Typically, this value should not exceed
              0.15 in order to make the modified Newton-Raphson solution converge efficiently. For more
              information about the creep ratio limit, see the :ref:`cutcontrol` command.

        Notes
        -----

        .. _NROPT_notes:

        The :ref:`nropt` command specifies the Newton-Raphson option used to solve the nonlinear equations
        in a static or full transient analysis.

        The automatic modified Newton-Raphson procedure with creep-ratio limit control (
        :ref:`nropt`,AUTO,CRPL, ``CRLIMIT`` ) applies to static creep analysis only. When the creep ratio is
        smaller than the value of the creep ratio limit specified, the modified Newton-Raphson procedure is
        used. If convergence difficulty occurs during solution, use the full Newton-Raphson procedure.

        The command :ref:`nropt`,UNSYM is also valid in a linear non-prestressed modal analysis that is used
        to perform a brake squeal analysis. In this special case, the command is used only to generate the
        unsymmetric stiffness matrix; no Newton-Raphson iterations are performed.

        :ref:`nropt`,MODI and :ref:`nropt`,INIT are only applicable with the sparse solver (
        :ref:`eqslv`,SPARSE). Thermal analyses will always use full Newton-Raphson irrespective of the
        ``Option1`` value selected.

        See Newton-Raphson Option in the `Structural Analysis Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/str_enercalc_app.html>`_ for more
        information.

        This command is also valid in PREP7.

        **Switching Between the Symmetric and Unsymmetric Option**

        Normally, switching from the symmetric Newton-Raphson option ( :ref:`nropt`,FULL) to the
        unsymmetric option ( :ref:`nropt`,UNSYM) or from the unsymmetric option to the symmetric option is
        allowed between load steps within the same analysis type. This is applicable to linear and
        nonlinear, static and full transient analyses.

        Under the following circumstances, the solution could be slightly different or inaccurate if you
        switch from symmetric to unsymmetric or vice versa:

        * The underlying elements or materials are unsymmetric by their mathematical definition, and you
          switch from unsymmetric to symmetric.

        * You change analysis types and also switch from symmetric to unsymmetric (or vise versa) at the
          same time. This situation could result in failures such as data corruption or a core dump and
          should therefore be avoided.

        * In some rare cases, switching between the symmetric and unsymmetric options can cause a system
          core dump when reading/writing the :file:`.ESAV` or :file:`.OSAV` file, and the analysis
          terminates. Typically, this happens when the record length of the element nonlinear saved
          variables cannot be altered between load steps by their mathematical definition.

        If all the elements and the material are symmetric by their mathematical definition and you use the
        unsymmetric option, the solution accuracy is the same as the symmetric option. However, the analysis
        will run twice as slow as the symmetric case.

        In a static or full transient linear perturbation base analysis, be aware that if the unsymmetric
        Newton-Raphson procedure is used, you must specify the UNSYM or DAMP eigensolver option in the
        downstream modal analysis, which may be more expensive than symmetric modal analysis.
        """
        command = f"NROPT,{option1},{option2},{optval}"
        return self.run(command, **kwargs)

    def pred(self, sskey: str = "", lskey: str = "", **kwargs):
        r"""Activates a predictor in a nonlinear analysis.

        Mechanical APDL Command: `PRED <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PRED.html>`_

        **Command default:**

        .. _PRED_default:

        The default command behavior is to use prediction ( ``Sskey`` = AUTO). The AUTO option chooses to
        either use the linear predictor or to turn the predictor OFF. However, prediction does not occur if
        one or more of these conditions exist:

        * Over prediction occurs due to a large residual force or excessive element distortion.

        * You are mapping ( :ref:`mapsolve` ) variables to a new mesh during `rezoning
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_nlad/Hlp_G_ADVRZSMP.html>`_.
          (Prediction does not occur for any :ref:`mapsolve` substeps, nor for the first substep
          afterwards.)

        * You have steady-state analysis defined ( :ref:`sstate` ), and contact elements exist in the model.

        Parameters
        ----------
        sskey : str
            Substep predictor key:

            * ``AUTO`` - The program uses a predictor but, within certain exceptions, automatically switches
              prediction off. This behavior is the default; see :ref:`PRED_default` for details.

            * ``OFF`` - No prediction occurs.

            * ``LINEAR (or ON)`` - Use the linear predictor on all substeps after the first.

            * ``QUADRATIC`` - Use the quadratic predictor on all substeps after the second.

        lskey : str
            Load step predictor:

            * ``OFF`` - No prediction across load steps occurs. This is the default behavior.

            * ``ON`` - Use a predictor also on the first substep of the load step. ( ``Sskey`` = ON is
              required.)

        Notes
        -----

        .. _PRED_notes:

        Activates a predictor in a nonlinear analysis on the degree-of-freedom solution for the first
        equilibrium iteration of each substep.

        When using the arc-length method ( :ref:`arclen`, :ref:`arctrm` ), you cannot issue the DOF solution
        predictor command ( :ref:`pred` ), the automatic time stepping command ( :ref:`autots` ), or the
        line search command ( :ref:`lnsrch` ). If you activate the arc-length method after you set
        :ref:`pred`, :ref:`autots`, or :ref:`lnsrch`, a warning message appears. If you elect to proceed
        with the arc-length method, the program disables your DOF predictor, automatic time stepping, and
        line search settings, and the time step size is controlled by the arc-length method internally.

        When using step-applied loads, such as :ref:`tunif`, :ref:`bfunif`, etc., or other types of non-
        monotonic loads, the predictor may adversely affect the convergence. If the solution is
        discontinuous, the predictor may need to be turned off.

        When performing a nonlinear analysis involving large rotations, the predictor may require using
        smaller substeps. If the model has rotational degrees-of-freedom, the quadratic predictor could work
        more efficiently than the linear predictor.

        This command is also valid in PREP7.
        """
        command = f"PRED,{sskey},,{lskey}"
        return self.run(command, **kwargs)

    def pstres(self, key: str = "", **kwargs):
        r"""Specifies whether prestress effects are calculated or included.

        Mechanical APDL Command: `PSTRES <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PSTRES.html>`_

        Parameters
        ----------
        key : str
            Prestress key:

            * ``OFF`` - Do not calculate (or include) prestress effects (default).

            * ``ON`` - Calculate (or include) prestress effects.

        Notes
        -----

        .. _PSTRES_notes:

        The :ref:`pstres` command specifies whether or not prestress effects are to be calculated or
        included. The command should be issued after the :ref:`antype` command.

        Prestress effects are calculated in a static or transient analysis for inclusion in a buckling,
        modal, harmonic (Method = FULL), or substructure generation analysis. If used in the solution
        processor ( :ref:`slashsolu` ), this command is valid only within the first load step.

        If you apply thermal body forces during a static analysis to calculate prestress effects, do not
        delete the forces during any subsequent full harmonic analyses. If you delete the thermal body
        forces, the thermal prestress effects will not be included in the harmonic analysis. Temperature
        loads used to define the thermal prestress will also be used in the full harmonic analysis as
        sinusoidally time-varying temperature loads.

        A prestress effect applied with non-follower loads resists rigid body rotation of the model. For
        example, an unsupported beam with axial tensile forces applied to both ends will have two nonzero
        rotational rigid body modes.

        If tabular loading ( :ref:`dim`, TABLE ) was used in the prestress static analysis step, the
        corresponding value of :ref:`time` will be used for tabular evaluations in the modal analysis.

        This command is also valid in PREP7.
        """
        command = f"PSTRES,{key}"
        return self.run(command, **kwargs)

    def semiimplicit(
        self, option: str = "", type_: str = "", value: str = "", **kwargs
    ):
        r"""Specifies parameters for a semi-implicit solution.

        Mechanical APDL Command: `SEMIIMPLICIT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SEMI.html>`_

        Parameters
        ----------
        option : str
            Option to be performed:

            * ``ETOI`` - Criterion for transitioning from the semi-implicit solution phase to the implicit
              solution phase.

            * ``MSCA`` - Selective mass scaling factor used during the semi-implicit solution phase.

            * ``SFAC`` - Safety factor for time incrementation used during the semi-implicit solution phase.

            * ``AUTS`` - Automatic time stepping and bisection controls used during the semi-implicit solution
              phase.

            * ``BVIS`` - Bulk viscosity controls used during the semi-implicit solution phase.

            * ``EFRQ`` - Output and restart file frequency used during the semi-implicit solution phase.

        type_ : str
            Additional input; varies depending on the ``Option`` value. See table below.

        value : str
            Additional input; varies depending on the ``Option`` and ``Type`` values. See table below.

        Notes
        -----

        .. _SEMIIMPLICIT_notes:

        This command triggers a `semi-implicit solution scheme
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_adv/semi_limitations.html>`_ in which
        the analysis transitions to a semi-implicit solution method when the implicit solution method fails
        to converge. The command is valid only in the solution processor ( :ref:`slashsolu` ) and must be
        defined before the first :ref:`solve` command.

        The :ref:`semiimplicit` command can be used in a restart, even if the base analysis did not include
        the command. Therefore, a problem that failed in the implicit analysis can be restarted with this
        command so that it can transition to the semi-implicit method and solve further.

        The :ref:`semiimplicit` command can overwrite the values on some commands, as described in the
        following table.

        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.
        """
        command = f"SEMIIMPLICIT,{option},{type_},{value}"
        return self.run(command, **kwargs)

    def soloption(self, option: str = "", type_: str = "", value: str = "", **kwargs):
        r"""Specifies solution transition options.

        Mechanical APDL Command: `SOLOPTION <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SOLO.html>`_

        Parameters
        ----------
        option : str
            Transition option:

            * ``STOT`` - Use criterion for transitioning from a static solution to a transient dynamic solution.

            * ``TTOS`` - Use criterion for transitioning from a transient dynamic solution to a static solution.

        type_ : str
            Additional input; varies depending on the ``Option`` value. See table below.

        value : str
            Additional input; varies depending on the ``Option`` and ``Type`` values. See table below.

        Notes
        -----

        .. _SOLOPTION_notes:

        This command triggers an automatic transition from a static solution to a transient solution based
        on the specified criterion. The command is valid only in the solution processor ( :ref:`slashsolu` )
        and must be defined either before the first :ref:`solve` command or during a restart analysis.

        If :ref:`soloption` is issued with no arguments specified, the static solution will transition to a
        quasi-static transient solution if the static solution fails to converge (that is,
        :ref:`soloption`,STOT,CONV,QUASI).

        :ref:`soloption` can be used in a restart even if the base analysis did not include the command.
        Therefore, a problem that failed in the static analysis can be restarted using this command so that
        it transitions to a transient solution and solves further. Material densities are required for the
        transient solution, but they must be defined during the static solution since the restart framework
        does not permit material density to be defined in the restart analysis.

        For more information on using :ref:`soloption`, see `Automatic Transition Between Static and
        Transient Solutions
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_adv/solutran_limitations.html>`_
        """
        command = f"SOLOPTION,{option},{type_},{value}"
        return self.run(command, **kwargs)

    def ssopt(
        self,
        option: str = "",
        par1: str = "",
        par2: str = "",
        par3: str = "",
        par4: str = "",
        par5: str = "",
        **kwargs,
    ):
        r"""Defines a solution option for soil analysis.

        Mechanical APDL Command: `SSOPT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SSOPT.html>`_

        Parameters
        ----------
        option : str
            Solution option to define:

            * ``GEOSTATIC`` - Geostatic equilibrium step for soil analysis.

            * ``CONSOLIDATION`` - Consolidation step for soil analysis.

            * ``STOP`` - Stop condition for soil consolidation analysis.

            * ``SFSW`` - Specific weight load.

        par1 : str
            Parameters for the specified ``Option``.

        par2 : str
            Parameters for the specified ``Option``.

        par3 : str
            Parameters for the specified ``Option``.

        par4 : str
            Parameters for the specified ``Option``.

        par5 : str
            Parameters for the specified ``Option``.

        Notes
        -----
        **Valid ParValues for Each Option**
        * ``Option = GEOSTATIC`` - No parameter values required.

        * ``Option = CONSOLIDATION`` - No parameter values required.

        * ``Option = STOP`` - ``Par1`` :

          * SSTATE -- The steady-state solution threshold of incremental pore pressure in a step.
          * OFF -- Deactivate steady-state solution check.

          ``Par2`` :

          * Valid only when ``Par1`` = SSTATE.
          * A positive value to define the maximum pore pressure increment in a step, or a negative value to
            define the percentage of incremental pore pressure in a step to maximum pore pressure in the
            solution.

        * ``Option = SFSW`` - ``Par1, Par2, Par3`` :

          * The specific weight load direction. ( Default : The -Y axis in the global coordinate system.)

          ``Par4`` :

          * OFF -- Ignore the specific bulk weight (default).
          * ON -- Account for the specific bulk weight load.

          ``Par5`` :

          * OFF -- Ignores the fluid specific weight (default).
          * ON -- Account for the fluid specific weight.

        .. _SSOPT_notes:

        The :ref:`ssopt` command defines solution options for soil analysis ( :ref:`antype`,SOIL) only.
        """
        command = f"SSOPT,{option},{par1},{par2},{par3},{par4},{par5}"
        return self.run(command, **kwargs)

    def sstif(self, key: str = "", **kwargs):
        r"""Activates stress stiffness effects in a nonlinear analysis.

        Mechanical APDL Command: `SSTIF <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SSTIF.html>`_

        Parameters
        ----------
        key : str
            Stress stiffening key:

            * ``OFF`` - No stress stiffening is included (default unless :ref:`nlgeom`,ON).

            * ``ON`` - Stress stiffening is included (default if :ref:`nlgeom`,ON).

        Notes
        -----

        .. _SSTIF_notes:

        Activates stress stiffness effects in a nonlinear analysis ( :ref:`antype`,STATIC or TRANS). (The
        :ref:`pstres` command also controls the generation of the stress stiffness matrix and therefore
        should not be used in conjunction with :ref:`sstif`.) If used within the solution processor, this
        command is valid only within the first load step.

        When :ref:`nlgeom` is ON, :ref:`sstif` defaults to ON. This normally forms all of the consistent
        tangent matrix. However, for some special nonlinear cases, this can lead to divergence caused by
        some elements which do not provide a complete consistent tangent (notably, elements outside the 18
        ``x`` family). In such a case, Ansys, Inc. recommends issuing an :ref:`sstif`,OFF command
        to achieve convergence. For `current-technology elements
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/EL2oldnewtable.html#EL2curtechelembenefits>`_,
        setting :ref:`sstif`,OFF when :ref:`nlgeom` is ON has no effect (because stress stiffness effects
        are always included).

        This command is also valid in PREP7.

        .. warning::

            This command is archived in the latest version of the software.

        """
        command = f"SSTIF,{key}"
        return self.run(command, **kwargs)
