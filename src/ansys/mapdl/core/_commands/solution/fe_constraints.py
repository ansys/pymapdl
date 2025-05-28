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


class FeConstraints:

    def ldread(
        self,
        lab: str = "",
        lstep: str = "",
        sbstep: str = "",
        time: str = "",
        kimg: int | str = "",
        fname: str = "",
        ext: str = "",
        **kwargs,
    ):
        r"""Reads results from the results file and applies them as loads.

        Mechanical APDL Command: `LDREAD <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_LDREAD.html>`_

        Parameters
        ----------
        lab : str
            Valid load label:

            * ``TEMP`` - Temperatures from a thermal analysis are applied as body force nodal loads ( :ref:`bf`
              ) in a structural analysis or other type of analysis.

              When used in conjunction with ``KIMG`` = 1 or ``KIMG`` = 2, temperatures can be applied to a
              subsequent thermal analysis as nodal loads ( :ref:`d` ) or initial conditions ( :ref:`ic` ),
              respectively.

              See the :ref:`LDREAD_notes`section for details on transferring temperatures from layered thermal
              shell elements ( ``SHELL131``, ``SHELL132``) and layered thermal solid elements ( ``SOLID278``,
              ``SOLID279``).

            * ``FORC`` - Forces from an electromagnetic analysis are applied as force loads ( :ref:`f` ) in a
              structural analysis. :ref:`ldread`,FORC reads coupling forces. See the discussion on `force
              computation
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_lof/Hlp_G_ELE6_5.html#emagreluctfig>`_
              in the `Low-Frequency Electromagnetic Analysis Guide <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_lof/Hlp_G_ELE16.html>`_.

              For a full harmonic magnetic analysis, FORC represents the time-averaged force (use in conjunction
              with ``KIMG`` = 2). Values are in the nodal coordinate system for the force loads ( :ref:`f` ).

            * ``HGEN`` - Heat generations from an electromagnetic analysis are applied as body-force loads (
              :ref:`bfe` ) in a thermal analysis. For a full harmonic analysis, HGEN represents the time-averaged
              heat generation load (use in conjunction with ``KIMG`` = 2).

            * ``JS`` - Source current density from a current-conduction analysis are applied as body-force loads
              ( :ref:`bfe` ). Values are in the global Cartesian coordinate system.

            * ``EF`` - Electric field element centroid values from an electrostatic analysis are applied as
              body-force loads ( :ref:`bfe` ) in a magnetic analysis. Values are in the global Cartesian
              coordinate system.

            * ``REAC`` - Reaction loads from any analysis are applied as force loads ( :ref:`f` ) in any
              analysis. Values are in the nodal coordinate system.

            * ``CONC`` - Concentrations from a diffusion analysis are applied to a subsequent diffusion analysis
              as nodal loads ( :ref:`d` ) or initial conditions ( :ref:`ic` ) when used in conjunction with
              ``KIMG`` =1 or ``KIMG`` =2, respectively.

            * ``VMEN`` - Mean flow velocities from a static mean flow analysis are applied to a subsequent
              harmonic or modal solution of the convective wave equation as body-force loads ( :ref:`bf` ).

            * ``VOLT`` - Voltages from an electric, electrostatic, or electromagnetic analysis are applied to a
              subsequent electric, electrostatic, or electromagnetic analysis as nodal loads ( :ref:`d` ) when
              ``KIMG`` = 1 or as initial conditions ( :ref:`ic` ) when ``KIMG`` = 2.

        lstep : str
            Load step number of the data set to be read. Defaults to 1. If LAST, ignore ``SBSTEP`` and
            ``TIME`` and read the last data set.

        sbstep : str
            Substep number (within ``LSTEP`` ). If zero (or blank), ``LSTEP`` represents the last substep of
            the load step.

        time : str
            Time-point identifying the data set to be read. Used only if both ``LSTEP`` and ``SBSTEP`` are
            zero (or blank). If ``TIME`` is between two solution time points on the results file, a linear
            interpolation is done between the two data sets. If ``TIME`` is beyond the last time point on
            the file, use the last time point.

        kimg : int or str
            When used with results from harmonic analyses ( :ref:`antype`,HARMIC) ``KIMG`` establishes which set of data to read:

            * ``0`` - Read the real part of the solution. Valid also for ``Lab`` = EHFLU to read in time-average
              heat flux.

            * ``1`` - Read the imaginary part of the solution.

            * ``2`` - Calculate and read the time-average part. Meaningful for ``Lab`` = HGEN or FORC.

            When used with the PRES label, ``KIMG`` represents the shell element face on which to apply the pressure:

            * ``1`` - Apply pressure to face 1

            * ``2`` - Apply pressure to face 2

            When used with the TEMP label, ``KIMG`` indicates how temperatures are to be applied.

            * ``0`` - Apply temperatures as body loads ( :ref:`bf` )

            * ``1`` - Apply temperatures as nodal loads ( :ref:`d` )

            * ``2`` - Apply temperatures as initial conditions ( :ref:`ic` )

            When used with the CONC label, ``KIMG`` indicates how concentrations are to be applied.

            * ``1`` - Apply concentrations as nodal loads ( :ref:`d` )

            * ``2`` - Apply concentrations as initial conditions ( :ref:`ic` )

            When used with the VOLT label, ``KIMG`` indicates how voltages are to be applied.

            * ``1`` - Apply voltages as nodal loads ( :ref:`d` )

            * ``2`` - Apply voltages as initial conditions ( :ref:`ic` )

        fname : str
            File name and directory path (248 characters maximum, including the characters needed for the
            directory path). An unspecified directory path defaults to the working directory; in this case,
            you can use all 248 characters for the file name. The file name defaults to :file:`Jobname`.

        ext : str
            Filename extension (eight-character maximum). The extension defaults to RST (or RMF for a static
            mean flow analysis) if ``Fname`` is blank.

        Notes
        -----

        .. _LDREAD_notes:

        The :ref:`ldread` command reads results data from the results file and applies them as loads.

        The command can also apply results from an analysis defined with one physics environment as loads on
        a second analysis using a different physics environment. Results values are applied as loads for
        field-coupling effects (for example, output temperatures from a thermal analysis as input to a
        structural analysis).

        The command works based on the assumption that the meshes have not changed.

        Nodal loads are applied only to selected nodes. Element loads are applied only to selected elements.
        Element surface loads are applied only to selected elements where all face nodes for that surface
        are selected.

        To assure proper distribution of the surface loads, select only the nodes on the element face where
        the surface load is to be applied.

        Scaling and accumulation specifications are applied as the loads are read via the following
        commands:

        * :ref:`bfcum` for body-force loads. (Heat-generation loads are not accumulated.)

        * :ref:`sfcum` for surface loads.

        * :ref:`fcum` for force loads.

        List the results via the appropriate list command:

        * :ref:`bflist` or :ref:`bfelist` for body-force loads.

        * :ref:`sfelist` for surface loads.

        * :ref:`flist` for force loads.

        Values may be redefined after being read by issuing :ref:`ldread` again with a different load step
        and substep, or time value.

        This command is also valid in PREP7.

        **Transferring Temperature Output from SHELL131 and SHELL132**

        If a thermal analysis uses ``SHELL131``or ``SHELL132``thermal shell elements, temperatures can be
        transferred as body force element loads ( :ref:`bfe` ). In most cases, only the top and bottom
        temperatures from ``SHELL131``and ``SHELL132``are used by the structural shell elements; any
        interior temperatures are ignored. However, all temperatures are used by ``SHELL181``having section
        input, and ``SHELL281``having section input; for these elements, therefore, the number of
        temperature points at a node generated in the thermal model must match the number of temperature
        points at a node needed by the structural model.

        When using ``SHELL131``or ``SHELL132``information for the :ref:`ldread` operation, all element types
        should specify the same set of thermal degrees of freedom.

        **Transferring Temperature Output from SOLID278 and SOLID279**

        If a thermal analysis uses ``SOLID278``or ``SOLID279``thermal solid elements, the temperatures are
        available either at the nodes (KEYOPT(3) = 0) or at the nodes and layers (KEYOPT(3) = 1 or 2). Under
        normal circumstances, only the nodal temperatures are transferred to the structural elements.

        However, if the structural elements are layered solids (KEYOPT(3) = 1 for ``SOLSH190``,
        ``SOLID185``, ``SOLID186``) and the thermal elements have KEYOPT(3) = 1 or 2 (layered solid) and
        KEYOPT(8) = 1 (store data for all layers), then the layer temperatures are transferred to the
        structural elements. If the number of layers do not match, the algorithm reverts back to nodal
        temperature transfer.

        ``KIMG`` = 0 (body loads) is the only valid mode for layered temperature transfer.

        **Examples**
        Thermal-Stress Example: Load Transfer Coupled-Field Analysis with One-way Coupling

        Induction Heating Example: Load Transfer Coupled-Field Analysis with Two-way Coupling
        """
        command = f"LDREAD,{lab},{lstep},{sbstep},{time},{kimg},{fname},{ext}"
        return self.run(command, **kwargs)

    def gslist(self, lab: str = "", **kwargs):
        r"""When using generalized plane strain, lists the input data or solutions.

        Mechanical APDL Command: `GSLIST <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_GSLIST.html>`_

        Parameters
        ----------
        lab : str
            Specify the content to be listed.

            * ``GEOMETRY`` - List the data input using GSGDATA

            * ``BC`` - List the data input using GSBDATA.

            * ``REACTIONS`` - When the command is issued in POST1, list the reaction force at the ending point,

              and the moment about X and Y if the corresponding constraints were applied.

            * ``RESULTS`` - When the command is issued in POST1, list the change of fiber length at the ending
              point during deformation and the rotation of the ending plane about X and Y during deformation.

            * ``ALL`` - List all of the above (default).

        Notes
        -----

        .. _GSLIST_notes:

        This command can be used to list the initial position of the ending plane, the applied load or
        displacements in the fiber direction, the resulting position of the ending plane after deformation,
        and the available reaction forces and moments at the ending point.

        All inputs and outputs are in the global Cartesian coordinate system. For more information about the
        generalized plane strain feature, see Generalized Plane Strain Option of Current-Technology Solid
        Elements in the  `Element Reference
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_BIBLIO.html>`_.

        This command is valid in any processor.
        """
        command = f"GSLIST,{lab}"
        return self.run(command, **kwargs)

    def gsbdata(
        self,
        labz: str = "",
        valuez: str = "",
        labx: str = "",
        valuex: str = "",
        laby: str = "",
        valuey: str = "",
        **kwargs,
    ):
        r"""Specifies the constraints or applies the load at the ending point for generalized plane strain
        option.

        Mechanical APDL Command: `GSBDATA <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_GSBDATA.html>`_

        Parameters
        ----------
        labz : str
            Constraint or load at the ending point in the fiber Z direction.

            * ``F`` - Apply a force in the fiber direction (default).

            * ``LFIBER`` - Define a length change in the fiber direction.

        valuez : str
            Value for ``LabZ``. The default is zero.

        labx : str
            Constraint or load on rotation about X.

            * ``MX`` - Supply a moment to cause the rotation of the ending plane about X (default).

            * ``ROTX`` - Define a rotation angle (in radians) of the ending plane about X.

        valuex : str
            Value for ``LabX``. The default is zero.

        laby : str
            Constraint or load on rotation about Y

            * ``MY`` - Supply a moment to cause the rotation of the ending plane about Y (default).

            * ``ROTY`` - Define a rotation angle (in radians) of the ending plane about Y.

        valuey : str
            Value for ``LabY``. The default is zero.

        Notes
        -----

        .. _GSBDATA_notes:

        All inputs are in the global Cartesian coordinate system. For more information about the generalized
        plane strain feature, see Generalized Plane Strain Option of Current-Technology Solid Elements in
        the `Element Reference
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_BIBLIO.html>`_.

        This command is also valid in PREP7.
        """
        command = f"GSBDATA,{labz},{valuez},{labx},{valuex},{laby},{valuey}"
        return self.run(command, **kwargs)

    def dval(
        self,
        baseid: str = "",
        lab: str = "",
        value: str = "",
        value2: str = "",
        keycal: str = "",
        **kwargs,
    ):
        r"""Defines values at enforced motion base.

        Mechanical APDL Command: `DVAL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_DVAL.html>`_

        Parameters
        ----------
        baseid : str
            The identification number of the enforced motion base (defined using the :ref:`d` command in the
            modal analysis).

        lab : str
            * ``U`` - Enforced displacement.

            * ``ACC`` - Enforced acceleration.

        value : str
            The value or table name reference for tabular boundary conditions. To specify a table, enclose
            the table name in percent (%) signs ( :ref:`dval`, ``BaseID``,U,``%tablename%``). Use the
            :ref:`dim` command to define a table.

        value2 : str
            The value of the second degree of freedom (if present). If the analysis type and the degree of
            freedom allow a complex input, ``VALUE`` is the real component and ``VALUE2`` is the imaginary
            component.

        keycal : str
            Displacement result calculation key:

            * ``ON`` - Calculate absolute displacement and acceleration results (default).

            * ``OFF`` - Calculate relative displacement and acceleration results.

        Notes
        -----

        .. _DVAL_notes:

        In a mode-superposition harmonic or transient analysis, you can apply enforced displacement or
        acceleration loads. If multiple loads are specified for the same base identification number
        (BaseID), the last load applied overrides the previous ones. For example, the following commands
        apply displacement to the base with identification number 1:

        .. code:: apdl

           DVAL,1,U,VALUE
           DVAL,1,ACC,VALUE

        In this case, the acceleration (ACC) applied in the last command will override the displacement (U).

        Issue :ref:`lsclear`,LSOPT to delete :ref:`dval` command options from the database.

        For more information, see `Enforced Motion Method for Mode-Superposition Transient and Harmonic
        Analyses <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STR_SMSUP.html#>`_
        `Enforced Motion Method for Transient and Harmonic Analyses
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/str_EnMoinStAn.html#>`_
        """
        command = f"DVAL,{baseid},{lab},{value},{value2},{keycal}"
        return self.run(command, **kwargs)

    def djdele(self, elem: str = "", lab: str = "", **kwargs):
        r"""Deletes boundary conditions on the components of relative motion of a joint element.

        Mechanical APDL Command: `DJDELE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_DJDELE.html>`_

        Parameters
        ----------
        elem : str
            Element number or ALL. ALL (or leaving this field blank) will delete all joint element boundary
            conditions specified by ``LAB``.

        lab : str
            Valid labels are:

            * ``UX`` - Displacement in local x direction.

            * ``UY`` - Displacement in local y direction.

            * ``UZ`` - Displacement in local z direction.

            * ``ROTX`` - Rotation about local x axis.

            * ``ROTY`` - Rotation about local y axis.

            * ``ROTZ`` - Rotation about local z axis.

            * ``VELX`` - Linear velocity in local x direction.

            * ``VELY`` - Linear velocity in local y direction.

            * ``VELZ`` - Linear velocity in local z direction.

            * ``OMGX`` - Angular velocity in local x direction.

            * ``OMGY`` - Angular velocity in local y direction.

            * ``OMGZ`` - Angular velocity in local z direction.

            * ``ACCX`` - Linear acceleration in local x direction.

            * ``ACCY`` - Linear acceleration in local y direction.

            * ``ACCZ`` - Linear acceleration in local z direction.

            * ``DMGX`` - Angular acceleration in local x direction.

            * ``DMGY`` - Angular acceleration in local y direction.

            * ``DMGZ`` - Angular acceleration in local z direction.

            * ``ALL, or (blank)`` - Delete all applied boundary conditions.

        Notes
        -----

        .. _DJDELE_notes:

        This command is valid for ``MPC184``joint elements.  See :ref:`dj` for information on
        specifying boundary conditions on the components of relative motion of a joint element.
        """
        command = f"DJDELE,{elem},{lab}"
        return self.run(command, **kwargs)

    def dsym(self, lab: str = "", normal: str = "", kcn: str = "", **kwargs):
        r"""Specifies symmetry or antisymmetry degree-of-freedom constraints on nodes.

        Mechanical APDL Command: `DSYM <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_DSYM.html>`_

        Parameters
        ----------
        lab : str
            Symmetry label:

            * ``SYMM`` - Generate symmetry constraints as described below (default).

            * ``ASYM`` - Generate antisymmetry constraints as described below.

        normal : str
            Surface orientation label to determine the constraint set (surface is assumed to be perpendicular to
            this coordinate direction in coordinate system ``KCN`` ):

            * ``X`` - Surface is normal to coordinate X direction (default). Interpreted as R direction for non-
              Cartesian coordinate systems.

            * ``Y`` - Surface is normal to coordinate Y direction. θ direction for non-Cartesian
              coordinate systems.

            * ``Z`` - Surface is normal to coordinate Z direction. Φ direction for spherical or toroidal
              coordinate systems.

        kcn : str
            Reference number of global or local coordinate system used to define surface orientation.

        Notes
        -----

        .. _DSYM_notes:

        Specifies symmetry or antisymmetry degree-of-freedom constraints on the selected nodes. The nodes
        are first automatically rotated (any previously defined rotations on these nodes are redefined) into
        coordinate system ``KCN``, then zero-valued constraints are generated, as described below, on the
        selected degree-of-freedom set (limited to displacement, velocity, and magnetic degrees of freedom)
        ( :ref:`dofsel` ). Constraints are defined in the (rotated) nodal coordinate system, as usual. See
        the :ref:`d` and :ref:`nrotat` commands for additional details about constraints and nodal
        rotations.

        This command is also valid in PREP7.

        .. _DSYM_extranote1:

        Symmetry or antisymmetry constraint generations are based upon the valid degrees of freedom in the
        model, that is, the de  grees of freedom associated with the elements attached to the nodes.
        The labels for degrees of freedom used in the generation depend on the ``Normal`` label.

        For displacement degrees of freedom, the constraints generated are:

        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.

        For velocity degrees of freedom, the constraints generated are:

        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.

        For the 2D vector magnetic degree of freedom, AZ, symmetry is naturally satisfied and the SYMM label
        generates no constraints. The ASYM label generates flux parallel conditions (flux flows parallel to
        the surface).

        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.
        """
        command = f"DSYM,{lab},{normal},{kcn}"
        return self.run(command, **kwargs)

    def dlist(self, node1: str = "", node2: str = "", ninc: str = "", **kwargs):
        r"""Lists DOF constraints.

        Mechanical APDL Command: `DLIST <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_DLIST.html>`_

        Parameters
        ----------
        node1 : str
            List constraints for nodes ``NODE1`` to ``NODE2`` (defaults to ``NODE1`` ) in steps of ``NINC``
            (defaults to 1). If ALL (default), ``NODE2`` and ``NINC`` are ignored and constraints for all
            selected nodes ( :ref:`nsel` ) are listed. If ``NODE1`` = P, graphical picking is enabled and
            all remaining command fields are ignored (valid only in the GUI). A component name may also be
            substituted for ``NODE1`` ( ``NODE2`` and ``NINC`` are ignored).

        node2 : str
            List constraints for nodes ``NODE1`` to ``NODE2`` (defaults to ``NODE1`` ) in steps of ``NINC``
            (defaults to 1). If ALL (default), ``NODE2`` and ``NINC`` are ignored and constraints for all
            selected nodes ( :ref:`nsel` ) are listed. If ``NODE1`` = P, graphical picking is enabled and
            all remaining command fields are ignored (valid only in the GUI). A component name may also be
            substituted for ``NODE1`` ( ``NODE2`` and ``NINC`` are ignored).

        ninc : str
            List constraints for nodes ``NODE1`` to ``NODE2`` (defaults to ``NODE1`` ) in steps of ``NINC``
            (defaults to 1). If ALL (default), ``NODE2`` and ``NINC`` are ignored and constraints for all
            selected nodes ( :ref:`nsel` ) are listed. If ``NODE1`` = P, graphical picking is enabled and
            all remaining command fields are ignored (valid only in the GUI). A component name may also be
            substituted for ``NODE1`` ( ``NODE2`` and ``NINC`` are ignored).

        Notes
        -----

        .. _DLIST_notes:

        Listing applies to the selected nodes ( :ref:`nsel` ) and the selected degree of freedom labels (
        :ref:`dofsel` ).

        This command is valid in any processor.
        """
        command = f"DLIST,{node1},{node2},{ninc}"
        return self.run(command, **kwargs)

    def dcum(
        self,
        oper: str = "",
        rfact: str = "",
        ifact: str = "",
        tbase: str = "",
        **kwargs,
    ):
        r"""Specifies that DOF constraint values are to be accumulated.

        Mechanical APDL Command: `DCUM <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_DCUM.html>`_

        **Command default:**

        .. _DCUM_default:

        Replace previous values.

        Parameters
        ----------
        oper : str
            Accumulation key:

            * ``REPL`` - Subsequent values replace the previous values (default).

            * ``ADD`` - Subsequent values are added to the previous values.

            * ``IGNO`` - Subsequent values are ignored.

        rfact : str
            Scale factor for the real component. Zero (or blank) defaults to 1.0. Use a small number for a
            zero scale factor.

        ifact : str
            Scale factor for the imaginary component. Zero (or blank) defaults to 1.0. Use a small number
            for a zero scale factor.

        tbase : str
            Base temperature for temperature difference. Used only with temperature degree of freedom. Scale
            factor is applied to the temperature difference ( ``T`` - ``TBASE`` ) and then added to
            ``TBASE``. ``T`` is the current temperature.

        Notes
        -----

        .. _DCUM_notes:

        Allows repeated degree of freedom constraint values (displacement, temperature, etc.) to be
        replaced, added, or ignored. Operations apply to the selected nodes ( :ref:`nsel` ) and the selected
        degree of freedom labels ( :ref:`dofsel` ). This command also operates on velocity and acceleration
        loads applied in a structural analysis.

        The operations occur when the next degree of freedom constraints are defined. For example, issuing
        the command :ref:`d`,1,UX,.025 after a previous :ref:`d`,1,UX,.020 causes the new value of the
        displacement on node 1 in the x-direction to be 0.045 with the add operation, 0.025 with the replace
        operation, or 0.020 with the ignore operation. Scale factors are also available to multiply the next
        value before the add or replace operation. A scale factor of 2.0 with the previous "add" example
        results in a displacement of 0.070. Scale factors are applied even if no previous values exist.
        Issue :ref:`dcum`,STAT to show the current label, operation, and scale factors. Solid model boundary
        conditions are not affected by this command, but boundary conditions on the FE model are affected.
        FE boundary conditions may still be overwritten by existing solid model boundary conditions if a
        subsequent boundary condition transfer occurs.

        :ref:`dcum` does not work for tabular boundary conditions.

        This command is also valid in PREP7.
        """
        command = f"DCUM,{oper},{rfact},{ifact},{tbase}"
        return self.run(command, **kwargs)

    def djlist(self, elem: str = "", **kwargs):
        r"""Lists boundary conditions applied to joint elements.

        Mechanical APDL Command: `DJLIST <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_DJLIST.html>`_

        Parameters
        ----------
        elem : str
            Element number or ALL (or blank). Lists joint element boundary conditions on the specified
            element(s).

        Notes
        -----

        .. _DJLIST_notes:

        This command is valid for ``MPC184``joint elements. See :ref:`dj` for information on specifying
        boundary  conditions on joint elements.
        """
        command = f"DJLIST,{elem}"
        return self.run(command, **kwargs)

    def dflx(
        self,
        node: str = "",
        bx: str = "",
        by: str = "",
        bz: str = "",
        bx2: str = "",
        by2: str = "",
        bz2: str = "",
        **kwargs,
    ):
        r"""Imposes a uniform magnetic flux B on an edge-element electromagnetic model.

        Mechanical APDL Command: `DFLX <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_DFLX.html>`_

        Parameters
        ----------
        node : str
            Nodes at which the edge-flux (AZ) constraints corresponding to the uniform magnetic flux are to
            be specified. Valid options are ALL (default) or Component Name. If ALL, constraints are applied
            to all selected nodes ( :ref:`nsel` ).

        bx : str
            Real components of magnetic flux B.

        by : str
            Real components of magnetic flux B.

        bz : str
            Real components of magnetic flux B.

        bx2 : str
            Imaginary components of magnetic flux B.

        by2 : str
            Imaginary components of magnetic flux B.

        bz2 : str
            Imaginary components of magnetic flux B.

        Notes
        -----

        .. _DFLX_notes:

        The :ref:`dflx` command sets the constraints on the edge-flux (AZ) degrees of freedom to produce a
        uniform magnetic flux B in an edge-based electromagnetic analysis using one of these element types:
        ``SOLID226``, ``SOLID227``, ``SOLID236``, or ``SOLID237``. The command ignores the corner nodes of
        the elements (even if they were selected) and imposes the AZ-constraints on the mid-side nodes only.
        The AZ-constraints are imposed in the active Cartesian coordinate system. A non-Cartesian coordinate
        system will be ignored by the :ref:`dflx` command.

        The edge-flux constraints at the mid-side nodes are derived from the magnetic vector potential
        **A**, which is related to the imposed magnetic flux **B** as follows:

        A = 1 2 [ B × r ]
        where **r** is the position of the mid-side node.

        The :ref:`dflx` command creates a component named _DFLX for the constrained midside nodes. You can
        use this component to delete the constraints imposed by the :ref:`dflx` command.

        This command is also valid in PREP7.
        """
        command = f"DFLX,{node},{bx},{by},{bz},{bx2},{by2},{bz2}"
        return self.run(command, **kwargs)

    def ddele(
        self,
        node: str = "",
        lab: str = "",
        nend: str = "",
        ninc: str = "",
        rkey: str = "",
        **kwargs,
    ):
        r"""Deletes degree-of-freedom constraints.

        Mechanical APDL Command: `DDELE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_DDELE.html>`_

        Parameters
        ----------
        node : str
            Node for which constraint is to be deleted. If ALL, ``NEND`` and ``NINC`` are ignored and
            constraints for all selected nodes ( :ref:`nsel` ) are deleted. If ``NODE`` = P, graphical
            picking is enabled and all remaining command fields are ignored (valid only in the GUI). A
            component name may also be substituted for ``NODE``.

        lab : str
            Valid degree of freedom label. If ALL, use all selected labels ( :ref:`dofsel` ). Structural
            labels: UX, UY, or UZ (displacements); ROTX, ROTY, or ROTZ (rotations); WARP (warping). Thermal
            labels: TEMP, TBOT, TE2, TE3...., TTOP (temperature). Acoustic labels: PRES (pressure); UX, UY,
            or UZ (displacements for FSI coupled elements). Electric label: VOLT (voltage). Magnetic labels:
            MAG (scalar magnetic potential); AZ (vector magnetic potential). Diffusion label: CONC
            (concentration).

            In structural analyses, the following velocity and acceleration load labels are also valid:
            VELX, VELY, VELZ (translational velocities); OMGX, OMGY, OMGZ (rotational velocities); ACCX,
            ACCY, ACCZ (translational accelerations); DMGX, DMGY, DMGZ (rotational accelerations).

            In structural analyses, HDSP (hydrostatic pressure) is also valid.

            If the node is connected to an ``ELBOW290``element, the following pipe cross-section degree of
            freedom labels are also valid: SE, SO, SW, SRA, and SRT. (For details, see the
            ``ELBOW290``documentation.) The degrees of freedom are not included when ``Lab`` = ALL. To
            constrain all cross-section degrees of freedom, specify ``Lab`` = SECT.

        nend : str
            Delete constraints from ``NODE`` to ``NEND`` (defaults to ``NODE`` ) in steps of ``NINC``
            (defaults to 1).

        ninc : str
            Delete constraints from ``NODE`` to ``NEND`` (defaults to ``NODE`` ) in steps of ``NINC``
            (defaults to 1).

        rkey : str
            Ramping option:

            * ``OFF`` - Loads are step-removed (default).

            * ``ON or FORCE`` - Forces on the specified degrees of freedom ( ``Lab`` ) are ramped during the
              next load step. The forces are ramped from the reaction forces of the previous load step, regardless
              of whether or not a constraint was present. If the specified node(s) and degree(s) of freedom has a
              force value currently defined, the force is ramped from the reaction force value to the currently
              applied force value. If no force is currently applied, the force is ramped from the reaction force
              value to zero. The ramping behavior is not in effect if the subsequent force is applied in tabular
              format.

              For degrees of freedom other than structural and TEMP, UX, UY, YZ, ROTX, ROTY, and ROTZ

               when performing a restart at an intermediate point during a load step, Not at the beginning or end
              of a load step.

               the reaction-force data is not available. Therefore, the force is ramped from zero to the currently
              applied force value (if it exists) for the specified node(s) and degree(s) of freedom.

              For structural and TEMP degrees of freedom, during a restart from an intermediate point during a
              load step, the reaction-force data is available. Therefore, it is ramped down during this restart
              step if no other loads are applied. See :ref:`DDELE_notes`for more information about the behavior of
              this option.

        Notes
        -----

        .. _DDELE_notes:

        Deleting a constraint is not the same as setting it to zero (which fixes the degree of freedom to a
        zero value). Deleting a constraint has the same effect as deactivating, releasing, or setting the
        constraint free. The node and the degree of freedom label must be selected ( :ref:`nsel`,
        :ref:`dofsel` ).

        For structural degrees of freedom, the following limitation exists when the analysis is restarted:

        * If a new force is applied ( :ref:`f` ) upon restart of the load step during which :ref:`ddele`,
          ``NODE``, ``DofLabel``,,,RFORCE (or ON) was issued, the force will show a jump to the current
          value at the time of restart before being ramped to its final value.

        Upon restart, it is good practice is to allow the reaction force to ramp down to zero in a load
        step, then to apply new loads in the next load step.

        This command is also valid in PREP7.
        """
        command = f"DDELE,{node},{lab},{nend},{ninc},{rkey}"
        return self.run(command, **kwargs)

    def dscale(self, rfact: str = "", ifact: str = "", tbase: str = "", **kwargs):
        r"""Scales DOF constraint values.

        Mechanical APDL Command: `DSCALE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_DSCALE.html>`_

        Parameters
        ----------
        rfact : str
            Scale factor for the real component. Zero (or blank) defaults to 1.0. Use a sma  ll number
            for a zero scale factor.

        ifact : str
            Scale factor for the imaginary component. Zero (or blank) defaults to 1.0. Use a small number
            for a zero scale factor.

        tbase : str
            Base temperature for temperature difference. For temperatures, the scale factor is applied to
            the temperature difference ( ``T`` - ``TBASE`` ) and then added to ``TBASE``. ``T`` is the
            current temperature.

        Notes
        -----

        .. _DSCALE_notes:

        Scales degree of freedom constraint values (displacement, temperature, etc.) in the database. If
        velocity and acceleration boundary conditions are applied in a structural analysis, they are also
        scaled by this command. Solid model boundary conditions are not scaled by this command, but boundary
        conditions on the FE model are scaled. Such scaled FE boundary conditions may still be overwritten
        by unscaled solid model boundary conditions if a subsequent boundary condition transfer occurs.

        Scaling applies to the previously defined values for the selected nodes ( :ref:`nsel` ) and the
        selected degree of freedom labels ( :ref:`dofsel` ). Issue :ref:`dlist` command to review results.

        :ref:`dscale` does not work for tabular boundary conditions.

        This command is also valid in PREP7.
        """
        command = f"DSCALE,{rfact},{ifact},{tbase}"
        return self.run(command, **kwargs)

    def dj(self, elem: str = "", label: str = "", value: str = "", **kwargs):
        r"""Specifies boundary conditions on the components of relative motion of a joint element.

        Mechanical APDL Command: `DJ <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_DJ.html>`_

        Parameters
        ----------
        elem : str
            Element number or ALL to be specified.

        label : str
            Valid labels are:

            * ``UX`` - Displacement in local x direction.

            * ``UY`` - Displacement in local y direction.

            * ``UZ`` - Displacement in local z direction.

            * ``ROTX`` - Rotation about local x axis.

            * ``ROTY`` - Rotation about local y axis.

            * ``ROTZ`` - Rotation about local y axis.

            * ``VELX`` - Linear velocity in local x direction.

            * ``VELY`` - Linear velocity in local y direction.

            * ``VELZ`` - Linear velocity in local z direction.

            * ``OMGX`` - Angular velocity in local x direction.

            * ``OMGY`` - Angular velocity in local y direction.

            * ``OMGZ`` - Angular velocity in local z direction.

            * ``ACCX`` - Linear acceleration in local x direction.

            * ``ACCY`` - Linear acceleration in local y direction.

            * ``ACCZ`` - Linear acceleration in local z direction.

            * ``DMGX`` - Angular acceleration in local x direction.

            * ``DMGY`` - Angular acceleration in local y direction.

            * ``DMGZ`` - Angular acceleration in local z direction.

        value : str
            Value of the label.

        Notes
        -----

        .. _DJ_notes:

        This command is valid for ``MPC184``joint elements. See :ref:`djdele` for information about deleting
        boundary conditions applied via this command.

        You can apply only one displacement, velocity, or acceleration load at any relative degree of
        freedom. If multiple loads are specified, the last applied load overrides the previous ones. For
        example, the following commands apply loads to element 100:

        * D,100,UX, ``Value``
        * D,100,VELX, ``Value``

        In this case, the velocity load (VELX) applied in the last command will override the displacement
        load (UX).

        Tabular boundary conditions ( ``VALUE`` = ``%tabname%``) can be used.

        %_FIX% is a Mechanical APDL reserved table name. When ``VALUE`` is set to %_FIX%, the program
        sprescribe
        the degree of freedom to the current relative displacement value. This option is only valid for the
        following labels: UX, UY, UZ, ROTX, ROTY, ROTZ. In most cases, %_FIX% usage is efficient and
        recommended for all structural degrees of freedom.

        In a modal analysis, the values of the eigenvectors at the degree of freedom connected via :ref:`dj`
        may be insufficiently accurate to satisfy the :ref:`dj` constraint conditions.
        """
        command = f"DJ,{elem},{label},{value}"
        return self.run(command, **kwargs)

    def d(
        self,
        node: str = "",
        lab: str = "",
        value: str = "",
        value2: str = "",
        nend: str = "",
        ninc: str = "",
        lab2: str = "",
        lab3: str = "",
        lab4: str = "",
        lab5: str = "",
        lab6: str = "",
        meshflag: str = "",
        **kwargs,
    ):
        r"""Defines degree-of-freedom constraints at nodes.

        Mechanical APDL Command: `D <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_D.html>`_

        Parameters
        ----------
        node : str
            Node at which constraint is to be specified. If ALL, ``NEND`` and ``NINC`` are ignored and
            constraints are applied to all selected nodes ( :ref:`nsel` ). If ``Node`` = P, graphical
            picking is enabled and all remaining command fields are ignored (valid only in the GUI). A
            component name may also be substituted for ``Node``.

        lab : str
            Valid degree-of-freedom label. If ALL, use all appropriate labels.

            * **Structural labels** : UX, UY, or UZ (displacements); ROTX, ROTY, or ROTZ (rotations); WARP
              (warping).
            * **Thermal labels** : TEMP, TBOT, TE2, TE3...., TTOP (temperature).
            * **Electric labels** : VOLT (voltage); EMF (electromotive force).
            * **Magnetic labels** : MAG (scalar magnetic potential); AZ (vector magnetic potential).
            * **Acoustic labels** : PRES (pressure); UX, UY, or UZ (displacements for FSI coupled elements);
              ENKE (acoustic energy density).
            * **Pore fluid labels** : PRES (pore pressure); UX, UY, or UZ (displacements); TEMP (temperature).
            * **Diffusion labels** : CONC (concentration).

            For structural static and transient analyses, translational and rotational velocities are also valid
            loads. Use these labels: VELX, VELY, VELZ (translational velocities); OMGX, OMGY, OMGZ (rotational
            velocities).

            For structural analyses, HDSP (hydrostatic pressure) is also valid. However, HDSP is not included
            when ``Lab`` = ALL.

            For structural transient analyses, the following acceleration loads are also valid: ACCX, ACCY, ACCZ
            (translational accelerations); DMGX, DMGY, DMGZ (rotational accelerations). The velocity and
            acceleration loads are not included when ``Lab`` = ALL.

            If the node is connected to an ``ELBOW290``element, the following pipe cross-section degree-of-
            freedom labels are also valid: SE, SO, SW, SRA, and SRT. (For details, see the
            ``ELBOW290``documentation.) The degrees of freedom are not included when ``Lab`` = ALL. To constrain
            all cross-section degrees of freedom, specify ``Lab`` = SECT.

            The PRES degree of freedom is also available for `porous media
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/elemdatatblpor.html#pormedflowdamp>`_
            problems.

        value : str
            Degree-of-freedom value or table name reference for tabular boundary conditions. To specify a
            table, enclose the table name in percent (%) signs (for example, :ref:`d`, ``Node``,TEMP,%
            ``tabname%``). To define a table, issue :ref:`dim`.

            If ``Value`` = SUPPORT, you can specify pseudo-constraints when `using residual vectors
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STR_SMSUP.html#ans_str_moda_resresp>`_
            in a modal analysis ( :ref:`resvec`,ON) or `CMS
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_substr/advcms.html#advcmsunderstand>`_
            analysis ( :ref:`cmsopt`,RFFB).

            If the enforced motion is active in the modal analysis ( :ref:`modcont`,,on), ``Value`` is the
            base identification number. It should be an integer greater than or equal to 1 and less than
            10000.

        value2 : str
            Second degree-of-freedom value (if any). If the analysis type and the degree of freedom allow a
            complex input, ``Value`` (above) is the real component and ``VALUE2`` is the imaginary
            component.

        nend : str
            Specifies the same values of constraint at the range of nodes from ``Node`` to ``NEND``
            (defaults to ``Node`` ), in steps of ``NINC`` (defaults to 1).

        ninc : str
            Specifies the same values of constraint at the range of nodes from ``Node`` to ``NEND``
            (defaults to ``Node`` ), in steps of ``NINC`` (defaults to 1).

        lab2 : str
            Additional degree-of-freedom labels. The same values are applied to the nodes for these labels.

        lab3 : str
            Additional degree-of-freedom labels. The same values are applied to the nodes for these labels.

        lab4 : str
            Additional degree-of-freedom labels. The same values are applied to the nodes for these labels.

        lab5 : str
            Additional degree-of-freedom labels. The same values are applied to the nodes for these labels.

        lab6 : str
            Additional degree-of-freedom labels. The same values are applied to the nodes for these labels.

        meshflag : str
            Specifies how to apply constraint on the mesh. Valid in a `nonlinear adaptivity analysis
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_nlad/Hlp_G_ADVREZ.html>`_ when ``Lab`` =
            UX / UY / UZ and ``Node`` is not a component name.

            * 0 - Constraint applied on the current mesh (default).
            * 1 - Constraint applied on the initial mesh for nonlinear adaptivity. ( ``NEND`` and ``NINC`` are
              not valid.)

        Notes
        -----

        .. _D_notes:

        The available degrees of freedom per node are listed under **Degrees of Freedom** in the input table
        for each element type in the `Element Reference
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_BIBLIO.html>`_. Degrees of
        freedom are defined in the
        nodal coordinate system. The positive directions of structural translations and rotations are along
        and about the positive nodal axes directions. Structural rotations should be input in radians. The
        node and the degree-of-freedom label must be selected ( :ref:`nsel`, :ref:`dofsel` ).

        In a structural analysis, you can apply only one displacement, velocity, or acceleration load at any
        degree of freedom. If multiple loads are specified, the last applied load overrides the previous
        ones. For example, the following commands apply loads to node 100:

        * D,100,UX, ``Value``
        * D,100,VELX, ``Value``

        In this case, the velocity load (VELX) applied in the last command will override the displacement
        load (UX).

        For elements used in static and low frequency electromagnetic analysis ( ``SOLID236``and
        ``SOLID237``), the AZ degree of freedom is not a z-component of a vector potential, but rather the
        flux contribution on the element edge. To specify a flux-parallel condition, set AZ = 0. For more
        information, see `3D Magnetostatics andFundamentals of Edge-based Analysis
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_lof/lof3Dmagfunedgeanalxmps.html>`_ in
        the `Low-Frequency Electromagnetic Analysis Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_lof/Hlp_G_ELE16.html>`_.

        For ``ELBOW290``cross-section degrees of freedom ( ``Lab`` = SE, SO, SW, SRA, SRT, or SECT), the
        :ref:`d` command can only specify fixed constraints. The degree-of-freedom value must be zero; no
        other values are valid.

        For hydrostatic fluid elements ( ``HSFLD241``and ``HSFLD242``), the HDSP degree-of-freedom
        constraint at the pressure node prescribes the pressure value for all the fluid elements sharing the
        pressure node.

        Tabular boundary conditions ( ``VALUE`` = ``%tabname%``) are available only for the following
        degree-of-freedom labels: Electric (VOLT), structural (UX, UY, UZ, ROTX, ROTY, ROTZ, and velocity
        and acceleration loads VELX, VELY, VELZ, OMGX, OMGY, OMGZ, ACCX, ACCY, ACCZ, DMGX, DMGY, DMGZ),
        acoustic (PRES, UX, UY, UZ, ENKE ), temperature (TEMP, TBOT, TE2, TE3...., TTOP), diffusion (CONC).
        All labels are valid only in static ( :ref:`antype`,STATIC) and full transient (
        :ref:`antype`,TRANS) analyses.

        In a mode-superposition harmonic or transient analysis, you must apply the constraints in the modal
        portion of the analysis for residual vector ( `Using the Residual Vector or the Residual Response
        Method to Improve Accuracy
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STR_SMSUP.html#ans_str_moda_resresp>`_
        `Enforced Motion Method for Mode-Superposition Transient and Harmonic Analyses
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STR_SMSUP.html#>`_

        %_FIX% is a Mechanical APDL reserved table name. When ``VALUE`` is set to %_FIX%, the program
        prescribes
        the degree of freedom to the current relative displacement value. This option is valid for the
        following labels: UX, UY, UZ, ROTX, ROTY, ROTZ. Alternatively, functions UX(), UY(), etc. can be
        used. (See :ref:`get` for a list of available functions.) In most cases, %_FIX% usage is efficient
        and recommended for all structural degrees of freedom.

        When ``Value`` = SUPPORT, specify only the minimum number of displacement constraints necessary to
        prevent rigid body motion: three constraints (or fewer, depending on the element type) for 2D models
        and six (or fewer) for 3D models.

        If constraints and initial conditions ( :ref:`ic` ) are applied at the same node, the constraint
        specification overrides. This combination is useful when a constraint degree-of-freedom value needs
        to start with a nonzero value at time = 0.0. For example, if the constraint degree-of-freedom value
        is prescribed to be a cosine function, then specifying an initial condition for the same node and
        degree of freedom ensures that the initial value for the constraint degree of freedom at time = 0.0
        is same as the cosine function evaluated at time = 0.0. If initial conditions are not specified, the
        constraint degree-of-freedom value ramps from zero in the first substep of the first load step.

        If more than one rotational degrees of freedom are constrained with non-zero rotations (ROTX, ROTY,
        ROTZ), rotational velocities (OMGX, OMGY, OMGZ), or rotational accelerations (DMGX, DMGY, DMGZ),
        then the rotation of the constrained node from its initial configuration to its final configuration
        depends on the combination and the sequence in which the constraints are applied. See Rotations in a
        Large-Deflection Analysis in `Structural Analysis Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/str_enercalc_app.html>`_.

        This command is also valid in PREP7.
        """
        command = f"D,{node},{lab},{value},{value2},{nend},{ninc},{lab2},{lab3},{lab4},{lab5},{lab6},{meshflag}"
        return self.run(command, **kwargs)
