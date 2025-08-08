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


class ConstraintEquations:

    def ce(
        self,
        neqn: str = "",
        const: str = "",
        node1: str = "",
        lab1: str = "",
        c1: str = "",
        node2: str = "",
        lab2: str = "",
        c2: str = "",
        node3: str = "",
        lab3: str = "",
        c3: str = "",
        **kwargs,
    ):
        r"""Defines a constraint equation relating degrees of freedom.

        Mechanical APDL Command: `CE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CE.html>`_

        Parameters
        ----------
        neqn : str
            Set equation reference number:

            * ``n`` - Arbitrary set number.

            * ``HIGH`` - The highest defined constraint equation number. This option is especially useful when
              adding nodes to an existing set.

            * ``NEXT`` - The highest defined constraint equation number plus one. This option automatically
              numbers coupled sets so that existing sets are not modified.

            The default value is HIGH.

        const : str
            Constant term of equation.

        node1 : str
            Node for first term of equation. If - ``NODE1``, this term is deleted from the equation.

        lab1 : str
            Degree of freedom label for first term of equation. Structural labels: UX, UY, or UZ
            (displacements); ROTX, ROTY, or ROTZ (rotations, in radians). Thermal labels: TEMP, TBOT, TE2,
            TE3, ..., TTOP (temperature). Electric labels: VOLT (voltage). Magnetic labels: MAG (scalar
            magnetic potential); AZ (vector magnetic potential). Diffusion label: CONC (concentration).

        c1 : str
            Coefficient for first node term of equation. If zero, this term is ignored.

        node2 : str
            Node, label, and coefficient for second term.

        lab2 : str
            Node, label, and coefficient for second term.

        c2 : str
            Node, label, and coefficient for second term.

        node3 : str
            Node, label, and coefficient for third term.

        lab3 : str
            Node, label, and coefficient for third term.

        c3 : str
            Node, label, and coefficient for third term.

        Notes
        -----

        .. _CE_notes:

        Repeat the :ref:`ce` command to add additional terms to the same equation. To change only the
        constant term, repeat the command with no node terms specified. Only the constant term can be
        changed during solution, and only with the :ref:`cecmod` command.

        Linear constraint equations may be used to relate the degrees of freedom of selected nodes in a more
        general manner than described for nodal coupling ( :ref:`cp` ). The constraint equation is of the
        form:

        .. math::

            equation not available

        where U(I) is the degree of freedom (displacement, temperature, etc.) of term (I). The following
        example is a set of two constraint equations, each containing three terms:

        0.0 = 3.0* (1 UX) + 3.0* (4 UX) + (-2.0)* (4 ROTY)

        2.0 = 6.0* (2 UX) + 10.0* (4 UY) + 1.0* (3 UZ)

        The first unique degree of freedom in the equation is eliminated in terms of all other degrees of
        freedom in the equation. A unique degree of freedom is one which is not specified in any other
        constraint equation, coupled node set, specified displacement set, or master degree of freedom set.
        It is recommended that the first term of the equation be the degree of freedom to be eliminated. The
        first term of the equation cannot contain a master degree of freedom, and no term can contain
        coupled degrees of freedom. The same degree of freedom may be specified in more than one equation
        but care must be taken to avoid over-specification (over-constraint).

        The degrees of freedom specified in the equation (that is, UX, UY, ROTZ, etc.) must also be included
        in the model (as determined from the element types ( :ref:`et` )). Also, each node in the equation
        must be defined on an element (any element type containing that degree of freedom will do).

        For buckling and modal analyses, the constant term of the equation will not be taken into account
        (that is, ``CONST`` is always zero).

        Note that under certain circumstances a constraint equation generated by :ref:`ce` may be modified
        during the solution. See for more information.
        """
        command = f"CE,{neqn},{const},{node1},{lab1},{c1},{node2},{lab2},{c2},{node3},{lab3},{c3}"
        return self.run(command, **kwargs)

    def cecycms(
        self,
        cyclownod: str = "",
        cychighnod: str = "",
        kmap: str = "",
        toler: str = "",
        kprint: int | str = "",
        usrnmap: str = "",
        **kwargs,
    ):
        r"""Generates the constraint equations for a `multistage cyclic symmetry analysis
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mstag/ans_mstag_introTheory.html>`_.

        Mechanical APDL Command: `CECYCMS <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CECYCMS.html>`_

        Parameters
        ----------
        cyclownod : str
            The name of a component for the nodes located on the low angle edge of the sector (up to 256
            characters enclosed in single quotes).

            The sector is that of the current stage ( ``Sname`` ) specified with :ref:`msopt`,NEW, ``Sname``
            or :ref:`msopt`,MODIFY, ``Sname``. If blank and if the array parameter of edge node pairs does
            not exist (no user-defined or default for ``UsrNMap`` ), the default component name is ‘
            ``Sname`` _CYCLOW_NOD``.

        cychighnod : str
            The name of a component for the nodes located on the high angle edge of the sector (up to 256
            characters enclosed in single quotes).

            The sector is that of the current stage ( ``Sname`` ) specified with :ref:`msopt`,NEW, ``Sname``
            or :ref:`msopt`,MODIFY, ``Sname``. If blank and if the array parameter of edge node pairs does
            not exist (no user-defined or default for ``UsrNMap`` ), the default component name is ‘
            ``Sname`` _CYCHIGH_NOD``.

        kmap : str
            Option to use mapping when creating cyclic symmetry constraint equations. This option is ignored if
            you specify ``UsrNMap``.

            * ``ON`` - Use mapping to relate low and high sector boundary DOFs when applying cyclic symmetry
              constraint equations.

            * ``OFF`` - Use matching node pairs from low and high sector boundaries to apply cyclic symmetry
              constraint equations (default).

        toler : str
            Tolerance for determining if one node on the low edge boundary matches the corresponding node on the
            high edge boundary after the nodes are rotated.

            * ``If positive`` - ``TOLER`` is absolute (length units, defaults to 1e-4 ). If the distance of the
              nodes is smaller than this absolute tolerance, the nodes are matched.

            * ``If negative`` - ``TOLER`` is relative. Considering the diagonal of an imaginary box enclosing
              the model, ``TOLER`` is a fraction of the length of that diagonal. Nodes within the relative
              tolerance are matched.

        kprint : int or str
            Option to print the table of matched nodes ( ``KMAP`` = OFF) or mapped nodes and elements ( ``KMAP``
            = ON).

            * ``0`` - Do not print the table (default).

            * ``1`` - Print the table. If edge nodes are mapped ( ``KMAP`` = ON) and a high edge node is
              matching a low edge node, the third column labeled MAPPED lists the node number. (See :ref:`Snippets
              of Table Printed with <CECYCMS_examples_PrintTable>` ``KPRINT`` = 1 on :ref:`cecycms` ).

        usrnmap : str
            Option for matching node pairs between low and high edges.

            Input the name of an existing array parameter or a numerical key:

            * ``<name>`` - Name of a user-defined array parameter that specifies the matching node pairs. The
              node pairs in the parameter may be input in any order, but the low edge node must be the first entry
              in each pair. (See :ref:`Example: <CECYCMS_us-def_array>` :ref:`cecycms` with a User-defined Array
              Parameter for ``UsrNMap``.)

            * ``0 ( or blank)`` - If the default array parameter named  ``Sname`` _CYCNODPAIR already exists,
              it is used to specify the matching node pairs (default).

              If this array parameter does not exist, nodes are paired automatically, and the array parameter
              named  ``Sname`` _CYCNODPAIR is created.

            * ``1`` - Nodes are paired automatically, and the array parameter named  ``Sname`` _CYCNODPAIR is
              created. If it exists, it is deleted and re-created.

            * ``-1`` - Nodes are paired automatically without creating or using an array parameter.

        Notes
        -----

        .. _CECYCMS_notes:

        :ref:`cecycms`, :ref:`ceims`, and :ref:`msopt` are commands used in a `multistage cyclic symmetry
        analysis
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mstag/ans_mstag_introTheory.html>`_.

        If edge node pairs are matched ( ``KMAP`` = OFF) and an array parameter is not specified for
        ``UsrNMap``, components are used for the cyclic edge nodes. You must specify those components using
        the :ref:`cm` command and ensure that they contain base sector nodes only. See `Building the Model
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mstag/multistage_building_model.html#>`_
        :ref:`Example Usage for examples demonstrating the use of <CECYCMS_ExampleUse>` :ref:`cecycms` in
        multistage cyclic symmetry analyses.

        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.

        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.

        **Example Usage**

        .. _CECYCMS_ExampleUse:

        `Example: Static Analysis of a Compressor Model with 4 Axial Stages Without a Duplicate Sector
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mstag/multistage_ex_compressor.html#>`_

        `Example: Linear Perturbation Modal Analysis of a Simplified Model with 2 Axial Stages and a Non-
        planar Interstage Boundary
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mstag/multistag_ex_linearPert.html#>`_

        `Example: Modal Analysis of Turbomachinery Stage Modeled as 2 Radial Stages with Offset Cyclic Edge
        Starting Points
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mstag/multistag_ex_modal_turboOffset.html#>`_

        `Example: Mutistage Multiharmonic Modal Analysis of a Hollow Cylinder Modeled Using 2 Stages
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mstag/mstag_hollowCyl2stages.html#>`_

        `Example: Multiharmonic Linear Perturbation Modal Analysis of a Simplified Model with 3 Axial Stages
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mstag/ans_mstagExMultiHarmLP.html#>`_
        """
        command = (
            f"CECYCMS,{cyclownod},{cychighnod},,{kmap},{toler},,{kprint},{usrnmap}"
        )
        return self.run(command, **kwargs)

    def cedele(
        self, neqn1: str = "", neqn2: str = "", ninc: str = "", nsel: str = "", **kwargs
    ):
        r"""Deletes constraint equations.

        Mechanical APDL Command: `CEDELE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CEDELE.html>`_

        Parameters
        ----------
        neqn1 : str
            Delete constraint equations from ``NEQN1`` to ``NEQN2`` (defaults to ``NEQN1`` ) in steps of
            ``NINC`` (defaults to 1). If ``NEQN1`` = ALL, ``NEQN2`` and ``NINC`` will be ignored all
            constraint equations will be deleted.

        neqn2 : str
            Delete constraint equations from ``NEQN1`` to ``NEQN2`` (defaults to ``NEQN1`` ) in steps of
            ``NINC`` (defaults to 1). If ``NEQN1`` = ALL, ``NEQN2`` and ``NINC`` will be ignored all
            constraint equations will be deleted.

        ninc : str
            Delete constraint equations from ``NEQN1`` to ``NEQN2`` (defaults to ``NEQN1`` ) in steps of
            ``NINC`` (defaults to 1). If ``NEQN1`` = ALL, ``NEQN2`` and ``NINC`` will be ignored all
            constraint equations will be deleted.

        nsel : str
            Additional node selection control:

            * ``ANY`` - Delete equation set if any of the selected nodes are in the set (default).

            * ``ALL`` - Delete equation set only if all of the selected nodes are in the set.

        """
        command = f"CEDELE,{neqn1},{neqn2},{ninc},{nsel}"
        return self.run(command, **kwargs)

    def ceims(
        self,
        toler: str = "",
        sname1: str = "",
        sname2: str = "",
        kprint: str = "",
        intf1nod: str = "",
        intf2nod: str = "",
        **kwargs,
    ):
        r"""Generates constraint equations at the interstage boundary in a `multistage cyclic symmetry analysis
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mstag/ans_mstag_introTheory.html>`_.

        Mechanical APDL Command: `CEIMS <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CEIMS.html>`_

        Parameters
        ----------
        toler : str
            Tolerance for determining if selected nodes are on the interface. ``TOLER`` is a fraction of the
            element dimension (defaults to 0.25 (25%)). Nodes outside the element by more than the tolerance
            are not accepted as being on the interface.

        sname1 : str
            The name of the first stage or part. For details on required node and element selections, see
            :ref:`CEIMS_NodeElemSelectReq`.

        sname2 : str
            The name of the second stage or part. For details on required node and element selections, see
            :ref:`CEIMS_NodeElemSelectReq`.

        kprint : str
            Option to print mapped nodes and elements.

            * ``0 (, or OFF)`` - Do not print mapped nodes and elements (default).

            * ``1 (, or ON)`` - Print mapped nodes and elements.

        intf1nod : str
            The name of the interstage nodal component of the first stage or sector part to be tied to the
            second stage or part named ``IntF2Nod``. It is optional to specify ``IntF1Nod`` (see
            :ref:`CEIMS_NodeElemSelectReq` ), but if used, ``IntF2Nod`` must also be specified.

        intf2nod : str
            The name of the interstage nodal component of the second stage or sector part to be tied to the
            first stage or part named ``IntF1Nod``. It is optional to specify ``IntF2Nod`` (see
            :ref:`CEIMS_NodeElemSelectReq` ), but it used, ``IntF1Nod`` must also be specified.

        Notes
        -----

        .. _CEIMS_notes:

        This command can be used to generate constraint equations to tie the interface nodes of two cyclic
        sector parts.

        Mapping is performed so mesh patterns at the interface of both parts can be different.

        This command is supported for the following degrees of freedom (DOFs) at the interstage boundary:
        UX, UY, UZ, ROTX, ROTY, ROTZ. Since only 3D elements are supported, UX, UY, and UZ are required.
        Note that if rotational DOFs are included, all three of them must be present.

        .. _CEIMS_NodeElemSelectReq:

        Node and Element Selection Requirements
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        You can specify the interface nodes in one of two ways: If you specify ``IntF1Nod`` and ``IntF2Nod``
        nodal components, there are no other node or element
        selection requirements.

        Otherwise, prior to issuing CEIMS:

        * the **nodes** at the interface of the first cyclic sector part ( ``Sname1``, part having the
        largest cyclic sector angle) must be selected, and

        * the **elements** at the interface of the second cyclic sector part ( ``Sname2``, part having the
        smallest cyclic sector angle) must be selected.

        For cyclic sector parts, select only base sector quantities (not duplicate sector ones). See also
        the :ref:`nsel` and :ref:`esel` commands for selecting nodes and elements.

        The degrees of freedom of the first part interface nodes are interpolated with the corresponding
        degrees of freedom of the nodes of the second part interface elements using the shape functions of
        those elements.

        Constraint equations are created between interface nodes. Those nodes should not have any other
        constraints defined, but if so they must be compatible.

        **Example Usage**
        `Example: Static Analysis of a Compressor Model with 4 Axial Stages Without a Duplicate Sector
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mstag/multistage_ex_compressor.html#>`_

        `Example: Linear Perturbation Modal Analysis of a Simplified Model with 2 Axial Stages and a Non-
        planar Interstage Boundary
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mstag/multistag_ex_linearPert.html#>`_

        `Example: Modal Analysis of Turbomachinery Stage Modeled as 2 Radial Stages with Offset Cyclic Edge
        Starting Points
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mstag/multistag_ex_modal_turboOffset.html#>`_

        `Example: Mutistage Multiharmonic Modal Analysis of a Hollow Cylinder Modeled Using 2 Stages
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mstag/mstag_hollowCyl2stages.html#>`_

        `Example: Multiharmonic Linear Perturbation Modal Analysis of a Simplified Model with 3 Axial Stages
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mstag/ans_mstagExMultiHarmLP.html#>`_
        """
        command = f"CEIMS,{toler},,{sname1},{sname2},{kprint},,,,,{intf1nod},{intf2nod}"
        return self.run(command, **kwargs)

    def ceintf(
        self,
        toler: str = "",
        dof1: str = "",
        dof2: str = "",
        dof3: str = "",
        dof4: str = "",
        dof5: str = "",
        dof6: str = "",
        movetol: str = "",
        **kwargs,
    ):
        r"""Generates constraint equations at an interface.

        Mechanical APDL Command: `CEINTF <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CEINTF.html>`_

        Parameters
        ----------
        toler : str
            Tolerance about selected elements, based on a fraction of the element dimension (defaults to
            0.25 (25%)). Nodes outside the element by more than the tolerance are not accepted as being on
            the interface.

        dof1 : str
            Degrees of freedom for which constraint equations are written. Defaults to all applicable DOFs.
            ``DOF1`` accepts ALL as a valid label, in which case the rest are ignored (all DOFs are
            applied).

        dof2 : str
            Degrees of freedom for which constraint equations are written. Defaults to all applicable DOFs.
            ``DOF1`` accepts ALL as a valid label, in which case the rest are ignored (all DOFs are
            applied).

        dof3 : str
            Degrees of freedom for which constraint equations are written. Defaults to all applicable DOFs.
            ``DOF1`` accepts ALL as a valid label, in which case the rest are ignored (all DOFs are
            applied).

        dof4 : str
            Degrees of freedom for which constraint equations are written. Defaults to all applicable DOFs.
            ``DOF1`` accepts ALL as a valid label, in which case the rest are ignored (all DOFs are
            applied).

        dof5 : str
            Degrees of freedom for which constraint equations are written. Defaults to all applicable DOFs.
            ``DOF1`` accepts ALL as a valid label, in which case the rest are ignored (all DOFs are
            applied).

        dof6 : str
            Degrees of freedom for which constraint equations are written. Defaults to all applicable DOFs.
            ``DOF1`` accepts ALL as a valid label, in which case the rest are ignored (all DOFs are
            applied).

        movetol : str
            The allowed "motion" of a node (see Note below). This distance is in terms of the element
            coordinates (-1.0 to 1.0). A typical value is 0.05. Defaults to 0 (do not move). ``MoveTol``
            must be less than or equal to ``TOLER``.

        Notes
        -----

        .. _CEINTF_notes:

        This command can be used to "tie" together two regions with dissimilar mesh patterns by generating
        constraint equations that connect the selected nodes of one region to the selected elements of the
        other region. At the interface between regions, nodes should be selected from the more dense mesh
        region, A, and the elements selected from the less dense mesh region, B. The degrees of freedom of
        region A nodes are interpolated with the corresponding degrees of freedom of the nodes on the region
        B elements, using the shape functions of the region B elements. Constraint equations are then
        written that relate region A and B nodes at the interface.

        The ``MoveTol`` field lets the nodes in the previously mentioned region A change coordinates when
        slightly inside or outside the elements of region B. The change in coordinates causes the nodes of
        region A to assume the same surface as the nodes associated with the elements of region B. The
        constraint equations that relate the nodes at both regions of the interface are then written.

        Solid elements with six degrees of freedom should only be interfaced with other six degree-of-
        freedom elements. The region A nodes should be near the region B elements. A location tolerance
        based on the smallest region B element length may be input. Stresses across the interface are not
        necessarily continuous. Nodes in the interface region should not have specified constraints.

        Use the :ref:`cpintf` command to connect nodes by coupling instead of constraint equations. Use the
        :ref:`eintf` command to connect nodes by line elements. See also the :ref:`nsel` and :ref:`esel`
        commands for selecting nodes and elements. See the `Mechanical APDL Theory Reference
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_biblio.html>`_ for a
        description of 3D space used to
        determine if a node will be considered by this command.

        As an alternative to the :ref:`ceintf` command, you can use contact elements and the internal
        multipoint constraint (MPC) algorithm to tie together two regions having dissimilar meshes. See
        `Solid-Solid and Shell-Shell Assemblies
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_ctec/Hlp_ctec_solsol.html#>`_
        for more information.
        """
        command = f"CEINTF,{toler},{dof1},{dof2},{dof3},{dof4},{dof5},{dof6},{movetol}"
        return self.run(command, **kwargs)

    def celist(
        self,
        neqn1: str = "",
        neqn2: str = "",
        ninc: str = "",
        option: str = "",
        **kwargs,
    ):
        r"""Lists the constraint equations.

        Mechanical APDL Command: `CELIST <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CELIST.html>`_

        Parameters
        ----------
        neqn1 : str
            List constraint equations from ``NEQN1`` to ``NEQN2`` (defaults to ``NEQN1`` ) in steps of
            ``NINC`` (defaults to 1). If ``NEQN1`` = ALL (default), ``NEQN2`` and ``NINC`` are ignored and
            all constraint equations are listed.

        neqn2 : str
            List constraint equations from ``NEQN1`` to ``NEQN2`` (defaults to ``NEQN1`` ) in steps of
            ``NINC`` (defaults to 1). If ``NEQN1`` = ALL (default), ``NEQN2`` and ``NINC`` are ignored and
            all constraint equations are listed.

        ninc : str
            List constraint equations from ``NEQN1`` to ``NEQN2`` (defaults to ``NEQN1`` ) in steps of
            ``NINC`` (defaults to 1). If ``NEQN1`` = ALL (default), ``NEQN2`` and ``NINC`` are ignored and
            all constraint equations are listed.

        option : str
            Options for listing constraint equations:

            * ``ANY`` - List equation set if any of the selected nodes are in the set (default). Only
              externally-generated constraint equations are listed.

            * ``ALL`` - List equation set only if all of the selected nodes are in the set. Only externally-
              generated constraint equations are listed.

            * ``INTE`` - List internally-generated constraint equations that are associated with MPC-based
              contact. Constraint equations are listed only if all the nodes in the set are selected.

            * ``CONV`` - Convert internal constraint equations to external constraint equations. Internal
              constraint equations are converted only if all of the nodes in the set are selected.

        Notes
        -----

        .. _CELIST_notes:

        This command is valid in any processor. However, the INTE and CONV options are only valid in the
        Solution processor after a :ref:`solve` command has been issued.
        """
        command = f"CELIST,{neqn1},{neqn2},{ninc},{option}"
        return self.run(command, **kwargs)

    def cerig(
        self,
        independ: str = "",
        depend: str = "",
        ldof: str = "",
        ldof2: str = "",
        ldof3: str = "",
        ldof4: str = "",
        ldof5: str = "",
        **kwargs,
    ):
        r"""Defines a rigid region.

        Mechanical APDL Command: `CERIG <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CERIG.html>`_

        Parameters
        ----------
        independ : str
            Retained (or independent) node for this rigid region. If ``INDEPEND`` = P, then graphical
            picking of the independent and dependent nodes is enabled (first node picked will be the
            independent node, and subsequent nodes picked will be dependent nodes), and subsequent fields
            are ignored (valid only in GUI).

        depend : str
            Removed (or dependent) node for this rigid region. If ALL, dependent nodes are all selected
            nodes.

        ldof : str
            Degrees of freedom associated with equations:

            * ``ALL`` - All applicable degrees of freedom (default). If 3D, generate 6 equations based on UX,
              UY, UZ, ROTX, ROTY, ROTZ; if 2D, generate 3 equations based on UX, UY, ROTZ.

            * ``UXYZ`` - Translational degrees of freedom. If 3D, generate 3 equations based on the dependent
              nodes' UX, UY, and UZ DOFs and the independent node's UX, UY, UZ, ROTX, ROTY, and ROTZ DOFs. If 2D,
              generate 2 equations based on the dependent nodes UX and UY DOFs and the independent nodes UX, UY,
              and ROTZ DOFs. No equations are generated for the rotational coupling.

            * ``RXYZ`` - Rotational degrees of freedom. If 3D, generate 3 equations based on ROTX, ROTY, ROTZ;
              if 2D, generate 1 equation based on ROTZ. No equations are generated for the translational coupling.

            * ``UX`` - Dependent translational UX degree of freedom only.

            * ``UY`` - Dependent translational UY degree of freedom only.

            * ``UZ`` - Dependent translational UZ degree of freedom only.

            * ``ROTX`` - Dependent rotational ROTX degree of freedom only.

            * ``ROTY`` - Dependent rotational ROTY degree of freedom only.

            * ``ROTZ`` - Dependent rotational ROTZ degree of freedom only.

        ldof2 : str
            Additional degrees of freedom. Used only if more than one degree of freedom are required and
            ``Ldof`` is not ALL, UXYZ, or RXYZ.

        ldof3 : str
            Additional degrees of freedom. Used only if more than one degree of freedom are required and
            ``Ldof`` is not ALL, UXYZ, or RXYZ.

        ldof4 : str
            Additional degrees of freedom. Used only if more than one degree of freedom are required and
            ``Ldof`` is not ALL, UXYZ, or RXYZ.

        ldof5 : str
            Additional degrees of freedom. Used only if more than one degree of freedom are required and
            ``Ldof`` is not ALL, UXYZ, or RXYZ.

        Notes
        -----

        .. _CERIG_notes:

        Defines a rigid region (link, area or volume) by automatically generating constraint equations to
        relate nodes in the region. Nodes in the rigid region must be assigned a geometric location before
        this command is used. Also, nodes must be connected to elements having the required degree of
        freedom set (see ``Ldof`` above). Generated constraint equations are based on small deflection
        theory. Generated constraint equations are numbered beginning from the highest previously defined
        equation number ( ``NEQN`` ) plus 1. Equations, once generated, may be listed ( :ref:`celist` ) or
        modified ( :ref:`ce` ) as desired. Repeat the :ref:`cerig` command for additional rigid region
        equations.

        This command generates the constraint equations needed for defining rigid lines in 2D or 3D space.
        Multiple rigid lines relative to a common point are used to define a rigid area or a rigid volume.
        In 2D space, with ``Ldof =`` ALL, three equations are generated for each pair of constrained nodes.
        These equations define the three rigid body motions in global Cartesian space, that is, two in-plane
        translations and one in-plane rotation. These equations assume the X-Y plane to be the active plane
        with UX, UY, and ROTZ degrees of freedom available at each node. Other types of equations can be
        generated with the appropriate ``Ldof`` labels.

        Six equations are generated for each pair of constrained nodes in 3D space (with ``Ldof =`` ALL).
        These equations define the six rigid body motions in global Cartesian space. These equations assume
        that UX, UY, UZ, ROTX, ROTY, and ROTZ degrees of freedom are available at each node.

        The UXYZ label allows generating a partial set of rigid region equations. This option is useful for
        transmitting the bending moment between elements having different degrees of freedom at a node. With
        this option only two of the three equations are generated for each pair of constrained nodes in 2D
        space. In 3D space, only three of the six equations are generated. In each case the rotational
        coupling equations are not generated. Similarly, the RXYZ label allows generating a partial set of
        equations with the translational coupling equations omitted.

        Applying this command to a large number of dependent nodes may result in constraint equations with a
        large number of coefficients. This may significantly increase the peak memory required during the
        process of element assembly. If real memory or virtual memory is not available, consider reducing
        the number of dependent nodes.

        Note that under certain circumstances the constraint equations generated by :ref:`cerig` may be
        modified during the solution. See for more information.

        :ref:`cerig` is restricted to small-deflection analysis (large-deflection is not supported). As an
        alternative to the :ref:`cerig` command, you can define a similar type of rigid region using contact
        elements and the internal multipoint constraint (MPC) algorithm. See `Surface-Based Constraints
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_ctec/Hlp_ctec_surfcon.html#strbeamso1703>`_
        for more information.

        :ref:`cerig` cannot be deleted using :ref:`cedele`,ALL and then regenerated in the second or higher
        load steps if the :ref:`lswrite` and :ref:`lssolve` procedure is used. :ref:`cerig` writes
        constraint equations directly into load step files. Deleting constraint equations (
        :ref:`cedele`,ALL) cannot always maintain the consistency among load steps.
        """
        command = f"CERIG,{independ},{depend},{ldof},{ldof2},{ldof3},{ldof4},{ldof5}"
        return self.run(command, **kwargs)

    def cesel(
        self, type_: str = "", vmin: str = "", vmax: str = "", vinc: str = "", **kwargs
    ):
        r"""Selects constraint equations via predefined reference numbers.

        Mechanical APDL Command: `CESEL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CESEL.html>`_

        Parameters
        ----------
        type_ : str
            Label identifying the type of select:

            * ``S`` - Select a new set (default).

            * ``A`` - Select an additional set and add it to the current set.

            * ``U`` - Unselect a set from the current set.

            * ``ALL`` - Restore the full set.

            * ``NONE`` - Unselect the full set.

            * ``INVE`` - Invert the current set (selected becomes unselected and vice versa).

            * ``STAT`` - Display the current select status.

        vmin : str
            Minimum value of constraint equation reference number range.

        vmax : str
            Maximum value of constraint equation reference number range. ``VMAX`` defaults to ``VMIN``.

        vinc : str
            Value increment within the specified range. Defaults to 1.

        Notes
        -----

        .. warning::

           This function contains specificities regarding the argument definitions.
           Please refer to the `command documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CESEL.html>`_
           for further explanations.

        .. _CESEL_notes:

        The :ref:`cesel` command selects sets of constraint equations ( :ref:`ce` ) via specified reference
        numbers. ``VMIN``, ``VMAX``, and ``VINC`` must be positive integer values.

        For example, the following command selects a new set of constraint equations based on reference
        numbers 1 through 7:

        .. code:: apdl

           CESEL,S,,,1,7,1

        Data are flagged as selected and unselected; no data are actually deleted from the database.

        Use :ref:`celist` to list constraint equations and their reference numbers. If a constraint equation
        is selected but involves unselected nodes, that constraint equation will not be listed by the
        :ref:`celist` command, and the solver ignores it.

        Internal constraint equations are not affected by this command.

        This command is also valid in POST1.
        """
        command = f"CESEL,{type_},,,{vmin},{vmax},{vinc}"
        return self.run(command, **kwargs)

    def cesgen(
        self,
        itime: str = "",
        inc: str = "",
        nset1: str = "",
        nset2: str = "",
        ninc: str = "",
        **kwargs,
    ):
        r"""Generates a set of constraint equations from existing sets.

        Mechanical APDL Command: `CESGEN <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CESGEN.html>`_

        Parameters
        ----------
        itime : str
            Do this generation operation a total of ``ITIME`` s, incrementing all nodes in the existing sets
            by ``INC`` each time after the first. ``ITIME`` must be >1 for generation to occur.

        inc : str
            Do this generation operation a total of ``ITIME`` s, incrementing all nodes in the existing sets
            by ``INC`` each time after the first. ``ITIME`` must be >1 for generation to occur.

        nset1 : str
            Generate sets from sets beginning with ``NSET1`` to ``NSET2`` (defaults to ``NSET1`` ) in steps
            of ``NINC`` (defaults to 1). If ``NSET1`` is negative, ``NSET2`` and ``NINC`` are ignored and
            the last \| ``NSET1`` \| sets (in sequence from maximum set number) are used as the sets to be
            repeated.

        nset2 : str
            Generate sets from sets beginning with ``NSET1`` to ``NSET2`` (defaults to ``NSET1`` ) in steps
            of ``NINC`` (defaults to 1). If ``NSET1`` is negative, ``NSET2`` and ``NINC`` are ignored and
            the last \| ``NSET1`` \| sets (in sequence from maximum set number) are used as the sets to be
            repeated.

        ninc : str
            Generate sets from sets beginning with ``NSET1`` to ``NSET2`` (defaults to ``NSET1`` ) in steps
            of ``NINC`` (defaults to 1). If ``NSET1`` is negative, ``NSET2`` and ``NINC`` are ignored and
            the last \| ``NSET1`` \| sets (in sequence from maximum set number) are used as the sets to be
            repeated.

        Notes
        -----

        .. _CESGEN_notes:

        Generates additional sets of constraint equations (with same labels) from existing sets. Node
        numbers between sets may be uniformly incremented.
        """
        command = f"CESGEN,{itime},{inc},{nset1},{nset2},{ninc}"
        return self.run(command, **kwargs)

    def rbe3(
        self,
        independ: str = "",
        dof: str = "",
        depend: str = "",
        wtfact: str = "",
        **kwargs,
    ):
        r"""Distributes the force/moment applied at an independent node to a set of dependent nodes.

        Mechanical APDL Command: `RBE3 <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_RBE3.html>`_

        Parameters
        ----------
        independ : str
            Node at which the force/moment to be distributed will be applied (the independent node). To be
            included in the degree-of-freedom (DOF) solution, this node must be associated with an element.

        dof : str
            Refers to the independent node DOFs to be used in the constraint equations. Valid labels are:
            UX, UY, UZ, ROTX, ROTY, ROTZ, UXYZ, RXYZ, ALL

        depend : str
            The name of an array parameter that contains a list of dependent nodes. Must specify the
            starting index number. ALL can be used for the currently selected set of nodes. The dependent
            nodes must not be colinear (that is, must not be located on the same straight line). See
            :ref:`RBE3_notes` for details.

        wtfact : str
            The name of an array parameter that contains a list of weighting factors corresponding to each
            dependent node defined by Depend. Must have the starting index number. If not specified, the
            weighting factor for each dependent node defaults to 1.

        Notes
        -----

        .. _RBE3_notes:

        :ref:`rbe3` distributes the force/moment applied at an independent node to a set of dependent nodes,
        taking into account the geometry of the dependent nodes as well as weighting factors. The force is
        distributed to the dependent nodes proportional to the weighting factors. The moment is distributed
        as forces to the dependent nodes; these forces are proportional to the distance from the center of
        gravity of the dependent nodes times the weighting factors. Only the translational degrees of
        freedom of the dependent nodes are used for constructing the constraint equations. Constraint
        equations are converted to distributed forces/moments on the dependent nodes during solution.

        :ref:`rbe3` creates constraint equations such that the motion of the independent node is the average
        of the dependent nodes. For the rotations, a least-squares approach is used to define the "average
        rotation" at the independent node from the translations of the dependent nodes. If the dependent
        nodes are colinear, then one of the independent node rotations that is parallel to the colinear
        direction cannot be determined in terms of the translations of the dependent nodes. Therefore, the
        associated moment component on the independent node in that direction cannot be transmitted. When
        this case occurs, a warning message is issued and the constraint equations created by :ref:`rbe3`
        are ignored.

        Applying this command to a large number of dependent nodes may result in constraint equations with a
        large number of coefficients. This may significantly increase the peak memory required during the
        process of element assembly. If real memory or virtual memory is not available, consider reducing
        the number of dependent nodes.

        You can use the :ref:`dofsel` command to select the degrees of freedom (DOFs) of the dependent nodes
        to be included in the resulting constraint equations. (Be sure to issue :ref:`dofsel`,ALL after
        issuing :ref:`rbe3`.) This capability is useful if, for example, you want to ignore radial
        constraints in cylindrical geometries. The selected DOFs must collectively generate forces and
        moments on the independent node in all six DOFs.

        :ref:`rbe3` is restricted to small-deflection analysis (large-deflection is not supported). As an
        alternative to :ref:`rbe3`, you can apply a similar type of constraint using contact elements and
        the internal multipoint constraint (MPC) algorithm. For more information, see `Surface-based
        Constraints
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_ctec/Hlp_ctec_surfcon.html#strbeamso1703>`_.

        This command is also valid in SOLUTION.
        """
        command = f"RBE3,{independ},{dof},{depend},{wtfact}"
        return self.run(command, **kwargs)
