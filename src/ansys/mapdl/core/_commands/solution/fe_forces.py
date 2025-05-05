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


class FeForces:

    def fj(self, elem: str = "", label: str = "", value: str = "", **kwargs):
        r"""Specify forces or moments on the components of the relative motion of a joint element.

        Mechanical APDL Command: `FJ <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_FJ.html>`_

        Parameters
        ----------
        elem : str
            Element number or ALL to specify all joint elements.

        label : str
            Valid labels:

            * ``FX`` - Force in local x direction.

            * ``FY`` - Force in local y direction.

            * ``FZ`` - Force in local z direction.

            * ``MX`` - Moment about local x axis.

            * ``MY`` - Moment about local y axis.

            * ``MZ`` - Moment about local z axis.

        value : str
            Value of the label.

        Notes
        -----

        .. _FJ_notes:

        Valid for ``MPC184``(joint options in KEYOPT(1)).

        In a mode-superposition harmonic or transient analysis, you must apply the load in the modal portion
        of the analysis. Mechanical APDL calculates a load vector and writes it to the :file:`MODE` file,
        which you
        can apply via the :ref:`lvscale` command.

        See :ref:`fjdele` for information on deleting forces and moments.
        """
        command = f"FJ,{elem},{label},{value}"
        return self.run(command, **kwargs)

    def fscale(self, rfact: str = "", ifact: str = "", **kwargs):
        r"""Scales force load values in the database.

        Mechanical APDL Command: `FSCALE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_FSCALE.html>`_

        Parameters
        ----------
        rfact : str
            Scale factor for the real component. Zero (or blank) defaults to 1.0. Use a small number for a
            zero scale factor.

        ifact : str
            Scale factor for the imaginary component. Zero (or blank) defaults to 1.0. Use a small number
            for a zero scale factor.

        Notes
        -----

        .. _FSCALE_notes:

        Scales force load (force, heat flow, etc.) values in the database. Scaling applies to the previously
        defined values for the selected nodes ( :ref:`nsel` ) and the selected force labels ( :ref:`dofsel`
        ). Issue :ref:`flist` command to review results. Solid model boundary conditions are not scaled by
        this command, but boundary conditions on the FE model are scaled. Such scaled FE boundary conditions
        may still be overwritten by unscaled solid model boundary conditions if a subsequent boundary
        condition transfer occurs.

        :ref:`fscale` does not work for tabular boundary conditions.

        This command is also valid in PREP7.
        """
        command = f"FSCALE,{rfact},{ifact}"
        return self.run(command, **kwargs)

    def fcum(self, oper: str = "", rfact: str = "", ifact: str = "", **kwargs):
        r"""Specifies that force loads are to be accumulated.

        Mechanical APDL Command: `FCUM <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_FCUM.html>`_

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

        Notes
        -----

        .. _FCUM_notes:

        Allows repeated force load (force, heat flow, etc.) values to be replaced, added, or ignored.
        Operations apply to the selected nodes [NSEL]. and the force labels corresponding to the selected
        force labels ( :ref:`dofsel` ). The operations occur when the next force specifications are defined.
        For example, issuing the command :ref:`f`,1,FX,250 after a previous :ref:`f`,1,FX,200 causes the
        current value of the force on node 1 in the x-direction to be 450 with the add operation, 250 with
        the replace operation, or 200 with the ignore operation. Scale factors are also available to
        multiply the next value before the add or replace operation. A scale factor of 2.0 with the previous
        "add" example results in a force of 700. Scale factors are applied even if no previous values exist.
        Issue :ref:`fcum`,STAT to show the current label, operation, and scale factors. Solid model boundary
        conditions are not affected by this command, but boundary conditions on the FE model are affected.
        FE boundary conditions may still be overwritten by existing solid model boundary conditions if a
        subsequent boundary condition transfer occurs.

        :ref:`fcum` does not work for tabular boundary conditions.

        This command is also valid in PREP7.
        """
        command = f"FCUM,{oper},{rfact},{ifact}"
        return self.run(command, **kwargs)

    def fjdele(self, elem: str = "", lab: str = "", **kwargs):
        r"""Deletes forces (or moments) on the components of the relative motion of a joint element.

        Mechanical APDL Command: `FJDELE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_FJDELE.html>`_

        Parameters
        ----------
        elem : str
            Element number, or ALL. (leaving this blank defaults to ALL)

        lab : str
            Valid labels are:

            * ``FX`` - Force in local x direction.

            * ``FY`` - Force in local y direction.

            * ``FZ`` - Force in local z direction.

            * ``MX`` - Moment about local x axis.

            * ``MY`` - Moment about local y axis.

            * ``MZ`` - Moment about local z axis.

            * ``ALL, or (blank)`` - Delete all valid forces or moments.

        Notes
        -----

        .. _FJDELE_notes:

        Valid for ``MPC184``(joint options in KEYOPT(1)).

        See :ref:`fj` for information on specifying forces (or moments).
        """
        command = f"FJDELE,{elem},{lab}"
        return self.run(command, **kwargs)

    def f(
        self,
        node: str = "",
        lab: str = "",
        value: str = "",
        value2: str = "",
        nend: str = "",
        ninc: str = "",
        meshflag: str = "",
        **kwargs,
    ):
        r"""Defines force loads at nodes.

        Mechanical APDL Command: `F <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_F.html>`_

        Parameters
        ----------
        node : str
            Node at which force is to be specified. If ALL, ``NEND`` and ``NINC`` are ignored and forces are
            applied to all selected nodes ( :ref:`nsel` ). If ``Node`` = P, graphical picking is enabled and
            all remaining command fields are ignored (valid only in the GUI). A component name may also be
            substituted for ``Node``.

        lab : str
            Valid force labels are:

            * **Structural labels** : FX, FY, or FZ (forces); MX, MY, or MZ (moments).
            * **Thermal labels** : HEAT, HBOT, HE2, HE3...., HTOP (heat flow).
            * **Fluid label** : FLOW (fluid flow).
            * **Electric labels** : AMPS (current flow), CHRG (electric charge).
            * **Magnetic labels** : FLUX (magnetic flux); CSGZ (magnetic current segment).
            * **Diffusion label** : RATE (diffusion flow rate).
            * **Viscous-thermal acoustics labels** : FX, FY, FZ ( `volumetric force density
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_acous/acous_excit_src.html#>`_ ).

            For structural analyses, DVOL (fluid mass flow rate) is also a valid label. See :ref:`Notes for more
            information. <F_notes>`

        value : str
            Force value or table name reference for specifying tabular boundary conditions. To specify a
            table, enclose the table name in percent signs (%), for example, :ref:`f`, ``Node``,HEAT,%
            ``tabname%``). To define a table, issue :ref:`dim`.

        value2 : str
            Second force value (if any). If the analysis type and the force allow a complex input, ``VALUE``
            (above) is the real component and ``VALUE2`` is the imaginary component.

        nend : str
            Specifies the same values of force at the nodes ranging from ``Node`` to ``NEND`` (defaults to
            ``Node`` ), in steps of ``NINC`` (defaults to 1).

        ninc : str
            Specifies the same values of force at the nodes ranging from ``Node`` to ``NEND`` (defaults to
            ``Node`` ), in steps of ``NINC`` (defaults to 1).

        meshflag : str
            Specifies how to apply nodal force on the mesh. Valid in a `nonlinear adaptivity analysis
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_nlad/Hlp_G_ADVREZ.html>`_ when ``Lab`` =
            FX / FY / FZ and ``Node`` is not a component name. Not valid when ``Lab`` = ALL.

            * 0 - Nodal-force loading occurs on the current mesh (default).
            * 1 - Nodal-force loading occurs on the initial mesh for nonlinear adaptivity. ( ``NEND`` and
              ``NINC`` are not valid.)

        Notes
        -----

        .. _F_notes:

        The available force loads per node correspond to the degrees of freedom listed under **Degrees of
        Freedom** in the input table for each element type in the `Element Reference
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_BIBLIO.html>`_. If both a
        force and a constrained degree
        of freedom ( :ref:`d` ) are specified at the same node, the constraint takes precedence. Forces are
        defined in the nodal coordinate system. The positive directions of structural forces and moments are
        along and about the positive nodal axis directions. The node and the degree-of-freedom label
        corresponding to the force must be selected ( :ref:`nsel`, :ref:`dofsel` ).

        Fluid flow (FLOW) is positive when flow is out of the nodes, and negative when flow is into the
        nodes.

        For hydrostatic fluid elements ( ``HSFLD241``and ``HSFLD242``), DVOL is used to specify fluid mass
        flow rate (with units of mass/time) at the pressure node. This allows fluid to be added or taken out
        of the fluid elements sharing the pressure node. A fluid density must also be specified ( :ref:`mp`
        or :ref:`tb` ) to apply a volume change corresponding to the prescribed fluid mass flow rate.

        Tabular boundary conditions ( ``VALUE`` = ``%tabname%``) are available only for the following
        labels: Fluid (FLOW), Electric (AMPS), Structural force (FX, FY, FZ, MX, MY, MZ), Thermal (HEAT,
        HBOT, HE2, HE3...., HTOP), Diffusion (RATE). Tabular boundary conditions are valid only in static (
        :ref:`antype`,STATIC), full transient ( :ref:`antype`,TRANS), full harmonic ( :ref:`antype`,
        HARMIC), modal superposition harmonic and modal superposition transient analyses.

        This command is also valid in PREP7.
        """
        command = f"F,{node},{lab},{value},{value2},{nend},{ninc},,,{meshflag}"
        return self.run(command, **kwargs)

    def fdele(
        self,
        node: str = "",
        lab: str = "",
        nend: str = "",
        ninc: str = "",
        lkey: str = "",
        **kwargs,
    ):
        r"""Deletes force loads on nodes.

        Mechanical APDL Command: `FDELE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_FDELE.html>`_

        Parameters
        ----------
        node : str
            Node for which force is to be deleted. If ALL, ``NEND`` and ``NINC`` are ignored and forces are
            deleted on all selected nodes ( :ref:`nsel` ). If ``NODE`` = P, graphical picking is enabled and
            all remaining command fields are ignored (valid only in the GUI). A component name may also be
            substituted for ``NODE``.

        lab : str
            If ALL, use all appropriate labels. Valid force labels are:

            * **Structural labels** : FX, FY, or FZ (forces); MX, MY, or MZ (moments).
            * **Thermal labels** : HEAT, HBOT, HE2, HE3...., HTOP (heat flow).
            * **Fluid label** : FLOW (fluid flow).
            * **Electric labels** : AMPS (current flow), CHRG (electric charge).
            * **Magnetic labels** : FLUX (magnetic flux); CSGZ (magnetic current segment).
            * **Diffusion label** : RATE (diffusion flow rate).

        nend : str
            Delete forces from ``NODE`` to ``NEND`` (defaults to ``NODE`` ) in steps of ``NINC`` (defaults
            to 1).

        ninc : str
            Delete forces from ``NODE`` to ``NEND`` (defaults to ``NODE`` ) in steps of ``NINC`` (defaults
            to 1).

        lkey : str
            Lock key:

            * ``(blank)`` - The DOF is not locked (default).

            * ``FIXED`` - Displacement on the specified degrees of freedom ( ``Lab`` ) is locked. The program
              prescribes the degree of freedom to the “current” relative displacement value in addition to
              deleting the force. If a displacement constraint (for example, :ref:`d` command) is applied in
              conjunction with this option, the actual applied displacement will be ramped during the next load
              step. The displacement is ramped from the current value to the newly defined value. This option is
              only valid for the following labels: FX, FY, FZ, MX, MY, MZ. This option is intended primarily for
              use in the Ansys Workbench interface to apply an increment length adjustment (bolt pretension loading).

        Notes
        -----

        .. _FDELE_notes:

        The node and the degree of freedom label corresponding to the force must be selected ( :ref:`nsel`,
        :ref:`dofsel` ).

        This command is also valid in PREP7.
        """
        command = f"FDELE,{node},{lab},{nend},{ninc},{lkey}"
        return self.run(command, **kwargs)

    def fjlist(self, elem: str = "", **kwargs):
        r"""Lists forces and moments applied on joint elements.

        Mechanical APDL Command: `FJLIST <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_FJLIST.html>`_

        Parameters
        ----------
        elem : str
            Element number or ALL (or blank). Lists joint element forces and moments on the specified
            element(s).

        Notes
        -----

        .. _FJLIST_notes:

        Notes
        Valid for ``MPC184``joint elements. See :ref:`fj` for information on specifying forces and moments.
        """
        command = f"FJLIST,{elem}"
        return self.run(command, **kwargs)

    def flist(self, node1: str = "", node2: str = "", ninc: str = "", **kwargs):
        r"""Lists force loads on the nodes.

        Mechanical APDL Command: `FLIST <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_FLIST.html>`_

        Parameters
        ----------
        node1 : str
            List forces for nodes ``NODE1`` to ``NODE2`` (defaults to ``NODE1`` ) in steps of ``NINC``
            (defaults to 1). If ALL, list for all selected nodes ( :ref:`nsel` ) and ``NODE2`` and ``NINC``
            are ignored (default). If ``NODE1`` = P, graphical picking is enabled and all remaining command
            fields are ignored (valid only in the GUI). A component name may also be substituted for
            ``NODE1``.

        node2 : str
            List forces for nodes ``NODE1`` to ``NODE2`` (defaults to ``NODE1`` ) in steps of ``NINC``
            (defaults to 1). If ALL, list for all selected nodes ( :ref:`nsel` ) and ``NODE2`` and ``NINC``
            are ignored (default). If ``NODE1`` = P, graphical picking is enabled and all remaining command
            fields are ignored (valid only in the GUI). A component name may also be substituted for
            ``NODE1``.

        ninc : str
            List forces for nodes ``NODE1`` to ``NODE2`` (defaults to ``NODE1`` ) in steps of ``NINC``
            (defaults to 1). If ALL, list for all selected nodes ( :ref:`nsel` ) and ``NODE2`` and ``NINC``
            are ignored (default). If ``NODE1`` = P, graphical picking is enabled and all remaining command
            fields are ignored (valid only in the GUI). A component name may also be substituted for
            ``NODE1``.

        Notes
        -----

        .. _FLIST_notes:

        Listing applies to the selected nodes ( :ref:`nsel` ) and the selected force labels ( :ref:`dofsel`
        ).

        .. warning::

            A list containing a node number that is larger than the maximum defined node ( NODE2), could
            deplete the system memory and produce unpredictable results.

        This command is valid in any processor.
        """
        command = f"FLIST,{node1},{node2},{ninc}"
        return self.run(command, **kwargs)
