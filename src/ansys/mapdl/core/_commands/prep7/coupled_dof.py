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


class CoupledDof:

    def cpsel(
        self, type_: str = "", vmin: str = "", vmax: str = "", vinc: str = "", **kwargs
    ):
        r"""Selects coupled degree-of-freedom sets via predefined reference numbers.

        Mechanical APDL Command: `CPSEL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CPSEL.html>`_

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
            Minimum value of coupled DOF reference number range.

        vmax : str
            Maximum value of coupled DOF reference number range. ``VMAX`` defaults to ``VMIN``.

        vinc : str
            Value increment within the specified range. Defaults to 1.

        Notes
        -----

        .. warning::

           This function contains specificities regarding the argument definitions.
           Please refer to the `command documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CPSEL.html>`_
           for further explanations.

        .. _CPSEL_notes:

        The :ref:`cpsel` command selects coupled degree-of-freedom sets ( :ref:`cp` ) via specified
        reference numbers. ``VMIN``, ``VMAX``, and ``VINC`` must be positive integer values.

        For example, the following command selects a new set of coupled degree-of-freedom sets based on
        reference numbers 1 through 7:

        .. code:: apdl

           CPSEL,S,,,1,7,1

        Data are flagged as selected and unselected; no data are actually deleted from the database.

        Use :ref:`cplist` to list coupled degree-of-freedom sets and their reference numbers. If a coupled
        degree-of-freedom set is selected but involves unselected nodes, that coupled degree-of-freedom set
        will not be listed by the :ref:`cplist` command, and the solver ignores it.

        Internally coupled degrees of freedom are not affected by this command.

        This command is also valid in POST1.
        """
        command = f"CPSEL,{type_},,,{vmin},{vmax},{vinc}"
        return self.run(command, **kwargs)

    def cpsgen(
        self,
        itime: str = "",
        inc: str = "",
        nset1: str = "",
        nset2: str = "",
        ninc: str = "",
        **kwargs,
    ):
        r"""Generates sets of coupled nodes from existing sets.

        Mechanical APDL Command: `CPSGEN <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CPSGEN.html>`_

        Parameters
        ----------
        itime : str
            Do this generation operation a total of ``ITIME`` s, incrementing all nodes in the existing sets
            by ``INC`` each time after the first. ``ITIME`` must be > 1 for generation to occur.

        inc : str
            Do this generation operation a total of ``ITIME`` s, incrementing all nodes in the existing sets
            by ``INC`` each time after the first. ``ITIME`` must be > 1 for generation to occur.

        nset1 : str
            Generate sets from sets beginning with ``NSET1`` to ``NSET2`` (defaults to ``NSET1`` ) in steps
            of ``NINC`` (defaults to 1). If ``NSET1`` is negative, ``NSET2`` and ``NINC`` are ignored and
            the last \| ``NSET1`` \| sets (in sequence from the maximum set number) are used as the sets to be
            repeated.

        nset2 : str
            Generate sets from sets beginning with ``NSET1`` to ``NSET2`` (defaults to ``NSET1`` ) in steps
            of ``NINC`` (defaults to 1). If ``NSET1`` is negative, ``NSET2`` and ``NINC`` are ignored and
            the last \| ``NSET1`` \| sets (in sequence from the maximum set number) are used as the sets to be
            repeated.

        ninc : str
            Generate sets from sets beginning with ``NSET1`` to ``NSET2`` (defaults to ``NSET1`` ) in steps
            of ``NINC`` (defaults to 1). If ``NSET1`` is negative, ``NSET2`` and ``NINC`` are ignored and
            the last \| ``NSET1`` \| sets (in sequence from the maximum set number) are used as the sets to be
            repeated.

        Notes
        -----

        .. _CPSGEN_notes:

        Generates additional sets of coupled nodes (with the same labels) from existing sets. Node numbers
        between sets may be uniformly incremented.
        """
        command = f"CPSGEN,{itime},{inc},{nset1},{nset2},{ninc}"
        return self.run(command, **kwargs)

    def cpngen(
        self,
        nset: str = "",
        lab: str = "",
        node1: str = "",
        node2: str = "",
        ninc: str = "",
        **kwargs,
    ):
        r"""Defines, modifies, or adds to a set of coupled degrees of freedom.

        Mechanical APDL Command: `CPNGEN <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CPNGEN.html>`_

        Parameters
        ----------
        nset : str
            Set reference number ( :ref:`cp` ).

        lab : str
            Degree of freedom label ( :ref:`cp` ).

        node1 : str
            Include in coupled set nodes ``NODE1`` to ``NODE2`` in steps of ``NINC`` (defaults to 1). If
            ``NODE1`` = P, graphical picking is enabled and all remaining command fields are ignored (valid
            only in the GUI). If - ``NODE1``, delete range of nodes from set instead of including. A
            component name may also be substituted for ``NODE1`` ( ``NODE2`` and ``NINC`` are ignored).

        node2 : str
            Include in coupled set nodes ``NODE1`` to ``NODE2`` in steps of ``NINC`` (defaults to 1). If
            ``NODE1`` = P, graphical picking is enabled and all remaining command fields are ignored (valid
            only in the GUI). If - ``NODE1``, delete range of nodes from set instead of including. A
            component name may also be substituted for ``NODE1`` ( ``NODE2`` and ``NINC`` are ignored).

        ninc : str
            Include in coupled set nodes ``NODE1`` to ``NODE2`` in steps of ``NINC`` (defaults to 1). If
            ``NODE1`` = P, graphical picking is enabled and all remaining command fields are ignored (valid
            only in the GUI). If - ``NODE1``, delete range of nodes from set instead of including. A
            component name may also be substituted for ``NODE1`` ( ``NODE2`` and ``NINC`` are ignored).

        Notes
        -----

        .. _CPNGEN_notes:

        Defines, modifies, or adds to a set of coupled degrees of freedom. May be used in combination with
        (or in place of) the :ref:`cp` command. Repeat :ref:`cpngen` command for additional nodes.
        """
        command = f"CPNGEN,{nset},{lab},{node1},{node2},{ninc}"
        return self.run(command, **kwargs)

    def cp(
        self,
        nset: str = "",
        lab: str = "",
        node1: str = "",
        node2: str = "",
        node3: str = "",
        node4: str = "",
        node5: str = "",
        node6: str = "",
        node7: str = "",
        node8: str = "",
        node9: str = "",
        node10: str = "",
        node11: str = "",
        node12: str = "",
        node13: str = "",
        node14: str = "",
        node15: str = "",
        node16: str = "",
        node17: str = "",
        **kwargs,
    ):
        r"""Defines (or modifies) a set of coupled degrees of freedom.

        Mechanical APDL Command: `CP <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CP.html>`_

        Parameters
        ----------
        nset : str
            Set reference number:

            * ``n`` - Arbitrary set number.

            * ``HIGH`` - The highest defined coupled set number will be used (default, unless ``Lab`` = ALL).
              This option is useful when adding nodes to an existing set.

            * ``NEXT`` - The highest defined coupled set number plus one will be used (default if ``Lab`` =
              ALL). This option automatically numbers coupled sets so that existing sets are not modified.

        lab : str
            Degree of freedom label for coupled nodes (in the nodal coordinate system). Defaults to label
            previously defined with ``NSET`` if set ``NSET`` already exists. A different label redefines the
            previous label associated with ``NSET``. Valid labels are: Structural labels: UX, UY, or UZ
            (displacements); ROTX, ROTY, or ROTZ (rotations) (in radians); HDSP (hydrostatic pressure). Thermal
            labels: TEMP, TBOT, TE2, TE3...., TTOP (temperature). Fluid labels: PRES (pressure); VX, VY, or VZ
            (velocities). Electric labels: VOLT (voltage); EMF (electromotive force drop); CURR (current).
            Magnetic labels: MAG (scalar magnetic potential); AZ (vector magnetic potential); CURR (current).
            Diffusion label: CONC (concentration).

            When ``Lab`` = ALL:

            * Sets are generated for each active degree of freedom (that is, one set for the UX degree of
              freedom, another set for UY, etc.), and ``NSET`` is incremented automatically to prevent
              overwriting existing sets.

            * Existing sets are not modified. ``NSET`` must be a new set number ``n`` or NEXT.

            * The degree of freedom set is determined according to all element types defined and the :ref:`dof`
              command, if used.

            * Hydrostatic pressure (HDSP) is not included.

        node1 : str
            List of nodes to be included in set. Duplicate nodes are ignored. If a node number is input as
            negative, the node is deleted from the coupled set. The first node in the list is the primary
            (retained) node, and the remaining nodes represent the removed degrees of freedom.

            If ``NODE1`` = ALL, ``NODE2`` through ``NODE17`` are ignored and all selected nodes (
            :ref:`nsel` ) are included in the set, and the node with the lowest node number becomes the
            primary node.

            If ``NODE1`` = P, graphical picking is enabled and all remaining command fields are ignored
            (valid only in the GUI).

            A component name can be substituted for ``NODE1``. The component consists of the node group to
            be coupled. The node with the lowest node number becomes the primary node among the node group.
            To display the generated and coupled node sets, issue the :ref:`cplist` command.

        node2 : str
            List of nodes to be included in set. Duplicate nodes are ignored. If a node number is input as
            negative, the node is deleted from the coupled set. The first node in the list is the primary
            (retained) node, and the remaining nodes represent the removed degrees of freedom.

            If ``NODE1`` = ALL, ``NODE2`` through ``NODE17`` are ignored and all selected nodes (
            :ref:`nsel` ) are included in the set, and the node with the lowest node number becomes the
            primary node.

            If ``NODE1`` = P, graphical picking is enabled and all remaining command fields are ignored
            (valid only in the GUI).

            A component name can be substituted for ``NODE1``. The component consists of the node group to
            be coupled. The node with the lowest node number becomes the primary node among the node group.
            To display the generated and coupled node sets, issue the :ref:`cplist` command.

        node3 : str
            List of nodes to be included in set. Duplicate nodes are ignored. If a node number is input as
            negative, the node is deleted from the coupled set. The first node in the list is the primary
            (retained) node, and the remaining nodes represent the removed degrees of freedom.

            If ``NODE1`` = ALL, ``NODE2`` through ``NODE17`` are ignored and all selected nodes (
            :ref:`nsel` ) are included in the set, and the node with the lowest node number becomes the
            primary node.

            If ``NODE1`` = P, graphical picking is enabled and all remaining command fields are ignored
            (valid only in the GUI).

            A component name can be substituted for ``NODE1``. The component consists of the node group to
            be coupled. The node with the lowest node number becomes the primary node among the node group.
            To display the generated and coupled node sets, issue the :ref:`cplist` command.

        node4 : str
            List of nodes to be included in set. Duplicate nodes are ignored. If a node number is input as
            negative, the node is deleted from the coupled set. The first node in the list is the primary
            (retained) node, and the remaining nodes represent the removed degrees of freedom.

            If ``NODE1`` = ALL, ``NODE2`` through ``NODE17`` are ignored and all selected nodes (
            :ref:`nsel` ) are included in the set, and the node with the lowest node number becomes the
            primary node.

            If ``NODE1`` = P, graphical picking is enabled and all remaining command fields are ignored
            (valid only in the GUI).

            A component name can be substituted for ``NODE1``. The component consists of the node group to
            be coupled. The node with the lowest node number becomes the primary node among the node group.
            To display the generated and coupled node sets, issue the :ref:`cplist` command.

        node5 : str
            List of nodes to be included in set. Duplicate nodes are ignored. If a node number is input as
            negative, the node is deleted from the coupled set. The first node in the list is the primary
            (retained) node, and the remaining nodes represent the removed degrees of freedom.

            If ``NODE1`` = ALL, ``NODE2`` through ``NODE17`` are ignored and all selected nodes (
            :ref:`nsel` ) are included in the set, and the node with the lowest node number becomes the
            primary node.

            If ``NODE1`` = P, graphical picking is enabled and all remaining command fields are ignored
            (valid only in the GUI).

            A component name can be substituted for ``NODE1``. The component consists of the node group to
            be coupled. The node with the lowest node number becomes the primary node among the node group.
            To display the generated and coupled node sets, issue the :ref:`cplist` command.

        node6 : str
            List of nodes to be included in set. Duplicate nodes are ignored. If a node number is input as
            negative, the node is deleted from the coupled set. The first node in the list is the primary
            (retained) node, and the remaining nodes represent the removed degrees of freedom.

            If ``NODE1`` = ALL, ``NODE2`` through ``NODE17`` are ignored and all selected nodes (
            :ref:`nsel` ) are included in the set, and the node with the lowest node number becomes the
            primary node.

            If ``NODE1`` = P, graphical picking is enabled and all remaining command fields are ignored
            (valid only in the GUI).

            A component name can be substituted for ``NODE1``. The component consists of the node group to
            be coupled. The node with the lowest node number becomes the primary node among the node group.
            To display the generated and coupled node sets, issue the :ref:`cplist` command.

        node7 : str
            List of nodes to be included in set. Duplicate nodes are ignored. If a node number is input as
            negative, the node is deleted from the coupled set. The first node in the list is the primary
            (retained) node, and the remaining nodes represent the removed degrees of freedom.

            If ``NODE1`` = ALL, ``NODE2`` through ``NODE17`` are ignored and all selected nodes (
            :ref:`nsel` ) are included in the set, and the node with the lowest node number becomes the
            primary node.

            If ``NODE1`` = P, graphical picking is enabled and all remaining command fields are ignored
            (valid only in the GUI).

            A component name can be substituted for ``NODE1``. The component consists of the node group to
            be coupled. The node with the lowest node number becomes the primary node among the node group.
            To display the generated and coupled node sets, issue the :ref:`cplist` command.

        node8 : str
            List of nodes to be included in set. Duplicate nodes are ignored. If a node number is input as
            negative, the node is deleted from the coupled set. The first node in the list is the primary
            (retained) node, and the remaining nodes represent the removed degrees of freedom.

            If ``NODE1`` = ALL, ``NODE2`` through ``NODE17`` are ignored and all selected nodes (
            :ref:`nsel` ) are included in the set, and the node with the lowest node number becomes the
            primary node.

            If ``NODE1`` = P, graphical picking is enabled and all remaining command fields are ignored
            (valid only in the GUI).

            A component name can be substituted for ``NODE1``. The component consists of the node group to
            be coupled. The node with the lowest node number becomes the primary node among the node group.
            To display the generated and coupled node sets, issue the :ref:`cplist` command.

        node9 : str
            List of nodes to be included in set. Duplicate nodes are ignored. If a node number is input as
            negative, the node is deleted from the coupled set. The first node in the list is the primary
            (retained) node, and the remaining nodes represent the removed degrees of freedom.

            If ``NODE1`` = ALL, ``NODE2`` through ``NODE17`` are ignored and all selected nodes (
            :ref:`nsel` ) are included in the set, and the node with the lowest node number becomes the
            primary node.

            If ``NODE1`` = P, graphical picking is enabled and all remaining command fields are ignored
            (valid only in the GUI).

            A component name can be substituted for ``NODE1``. The component consists of the node group to
            be coupled. The node with the lowest node number becomes the primary node among the node group.
            To display the generated and coupled node sets, issue the :ref:`cplist` command.

        node10 : str
            List of nodes to be included in set. Duplicate nodes are ignored. If a node number is input as
            negative, the node is deleted from the coupled set. The first node in the list is the primary
            (retained) node, and the remaining nodes represent the removed degrees of freedom.

            If ``NODE1`` = ALL, ``NODE2`` through ``NODE17`` are ignored and all selected nodes (
            :ref:`nsel` ) are included in the set, and the node with the lowest node number becomes the
            primary node.

            If ``NODE1`` = P, graphical picking is enabled and all remaining command fields are ignored
            (valid only in the GUI).

            A component name can be substituted for ``NODE1``. The component consists of the node group to
            be coupled. The node with the lowest node number becomes the primary node among the node group.
            To display the generated and coupled node sets, issue the :ref:`cplist` command.

        node11 : str
            List of nodes to be included in set. Duplicate nodes are ignored. If a node number is input as
            negative, the node is deleted from the coupled set. The first node in the list is the primary
            (retained) node, and the remaining nodes represent the removed degrees of freedom.

            If ``NODE1`` = ALL, ``NODE2`` through ``NODE17`` are ignored and all selected nodes (
            :ref:`nsel` ) are included in the set, and the node with the lowest node number becomes the
            primary node.

            If ``NODE1`` = P, graphical picking is enabled and all remaining command fields are ignored
            (valid only in the GUI).

            A component name can be substituted for ``NODE1``. The component consists of the node group to
            be coupled. The node with the lowest node number becomes the primary node among the node group.
            To display the generated and coupled node sets, issue the :ref:`cplist` command.

        node12 : str
            List of nodes to be included in set. Duplicate nodes are ignored. If a node number is input as
            negative, the node is deleted from the coupled set. The first node in the list is the primary
            (retained) node, and the remaining nodes represent the removed degrees of freedom.

            If ``NODE1`` = ALL, ``NODE2`` through ``NODE17`` are ignored and all selected nodes (
            :ref:`nsel` ) are included in the set, and the node with the lowest node number becomes the
            primary node.

            If ``NODE1`` = P, graphical picking is enabled and all remaining command fields are ignored
            (valid only in the GUI).

            A component name can be substituted for ``NODE1``. The component consists of the node group to
            be coupled. The node with the lowest node number becomes the primary node among the node group.
            To display the generated and coupled node sets, issue the :ref:`cplist` command.

        node13 : str
            List of nodes to be included in set. Duplicate nodes are ignored. If a node number is input as
            negative, the node is deleted from the coupled set. The first node in the list is the primary
            (retained) node, and the remaining nodes represent the removed degrees of freedom.

            If ``NODE1`` = ALL, ``NODE2`` through ``NODE17`` are ignored and all selected nodes (
            :ref:`nsel` ) are included in the set, and the node with the lowest node number becomes the
            primary node.

            If ``NODE1`` = P, graphical picking is enabled and all remaining command fields are ignored
            (valid only in the GUI).

            A component name can be substituted for ``NODE1``. The component consists of the node group to
            be coupled. The node with the lowest node number becomes the primary node among the node group.
            To display the generated and coupled node sets, issue the :ref:`cplist` command.

        node14 : str
            List of nodes to be included in set. Duplicate nodes are ignored. If a node number is input as
            negative, the node is deleted from the coupled set. The first node in the list is the primary
            (retained) node, and the remaining nodes represent the removed degrees of freedom.

            If ``NODE1`` = ALL, ``NODE2`` through ``NODE17`` are ignored and all selected nodes (
            :ref:`nsel` ) are included in the set, and the node with the lowest node number becomes the
            primary node.

            If ``NODE1`` = P, graphical picking is enabled and all remaining command fields are ignored
            (valid only in the GUI).

            A component name can be substituted for ``NODE1``. The component consists of the node group to
            be coupled. The node with the lowest node number becomes the primary node among the node group.
            To display the generated and coupled node sets, issue the :ref:`cplist` command.

        node15 : str
            List of nodes to be included in set. Duplicate nodes are ignored. If a node number is input as
            negative, the node is deleted from the coupled set. The first node in the list is the primary
            (retained) node, and the remaining nodes represent the removed degrees of freedom.

            If ``NODE1`` = ALL, ``NODE2`` through ``NODE17`` are ignored and all selected nodes (
            :ref:`nsel` ) are included in the set, and the node with the lowest node number becomes the
            primary node.

            If ``NODE1`` = P, graphical picking is enabled and all remaining command fields are ignored
            (valid only in the GUI).

            A component name can be substituted for ``NODE1``. The component consists of the node group to
            be coupled. The node with the lowest node number becomes the primary node among the node group.
            To display the generated and coupled node sets, issue the :ref:`cplist` command.

        node16 : str
            List of nodes to be included in set. Duplicate nodes are ignored. If a node number is input as
            negative, the node is deleted from the coupled set. The first node in the list is the primary
            (retained) node, and the remaining nodes represent the removed degrees of freedom.

            If ``NODE1`` = ALL, ``NODE2`` through ``NODE17`` are ignored and all selected nodes (
            :ref:`nsel` ) are included in the set, and the node with the lowest node number becomes the
            primary node.

            If ``NODE1`` = P, graphical picking is enabled and all remaining command fields are ignored
            (valid only in the GUI).

            A component name can be substituted for ``NODE1``. The component consists of the node group to
            be coupled. The node with the lowest node number becomes the primary node among the node group.
            To display the generated and coupled node sets, issue the :ref:`cplist` command.

        node17 : str
            List of nodes to be included in set. Duplicate nodes are ignored. If a node number is input as
            negative, the node is deleted from the coupled set. The first node in the list is the primary
            (retained) node, and the remaining nodes represent the removed degrees of freedom.

            If ``NODE1`` = ALL, ``NODE2`` through ``NODE17`` are ignored and all selected nodes (
            :ref:`nsel` ) are included in the set, and the node with the lowest node number becomes the
            primary node.

            If ``NODE1`` = P, graphical picking is enabled and all remaining command fields are ignored
            (valid only in the GUI).

            A component name can be substituted for ``NODE1``. The component consists of the node group to
            be coupled. The node with the lowest node number becomes the primary node among the node group.
            To display the generated and coupled node sets, issue the :ref:`cplist` command.

        Notes
        -----

        .. _CP_notes:

        Do not include the same degree of freedom in more than one coupled set. Repeat :ref:`cp` command for
        additional nodes.

        Coupling degrees of freedom into a set causes the results calculated for one member of the set to be
        the same for all members of the set. Coupling can be used to model various joint and hinge effects.
        A more general form of coupling can be done with constraint equations ( :ref:`ce` ). For structural
        analyses, a list of nodes is defined along with the nodal directions in which these nodes are to be
        coupled. As a result of this coupling, these nodes are forced to take the same displacement in the
        specified nodal coordinate direction. The amount of the displacement is unknown until the analysis
        is completed. A set of coupled nodes which are not coincident, or which are not along the line of
        the coupled displacement direction, may produce an applied moment which will not appear in the
        reaction forces. The actual degrees of freedom available for a particular node depends upon the
        degrees of freedom associated with element types ( :ref:`et` ) at that node. For scalar field
        analysis, this command is used to couple nodal temperatures, pressures, voltages, etc.

        A set of coupled nodes which are not coincident, or which are not along the line of the coupled
        displacement direction, produce an artificial moment constraint. If the structure rotates, a moment
        may be produced in the coupled set in the form of a force couple. This moment is in addition to the
        real reaction forces and may make it appear that moment equilibrium is not satisfied by just the
        applied forces and the reaction forces.

        Additional sets of coupled nodes may be generated from a specified set. Degrees of freedom are
        coupled within a set but are not coupled between sets. No degree of freedom should appear in more
        than one coupled set. Such an appearance would indicate that at least two sets were in fact part of
        a single larger set. The first degree of freedom of the coupled set is the "prime" degree of
        freedom. All other degrees of freedom in the coupled sets are eliminated from the solution matrices
        by their relationship to the prime degree of freedom. Forces applied to coupled nodes (in the
        coupled degree of freedom direction) will be summed and applied to the prime degree of freedom.
        Output forces are also summed at the prime degree of freedom. Degrees of freedom with specified
        constraints ( :ref:`d` ) should not be included in a coupled set (unless the degree of freedom is
        prime).

        If master degrees of freedom are defined for coupled nodes, only the prime degree of freedom should
        be so defined. The use of coupled nodes reduces the set of coupled degrees of freedom to only one
        degree of freedom.

        The removed degrees of freedom defined by the :ref:`cp` command cannot be included in any :ref:`ce`
        or :ref:`cerig` command.
        """
        command = f"CP,{nset},{lab},{node1},{node2},{node3},{node4},{node5},{node6},{node7},{node8},{node9},{node10},{node11},{node12},{node13},{node14},{node15},{node16},{node17}"
        return self.run(command, **kwargs)

    def cplgen(
        self,
        nsetf: str = "",
        lab1: str = "",
        lab2: str = "",
        lab3: str = "",
        lab4: str = "",
        lab5: str = "",
        **kwargs,
    ):
        r"""Generates sets of coupled nodes from an existing set.

        Mechanical APDL Command: `CPLGEN <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CPLGEN.html>`_

        Parameters
        ----------
        nsetf : str
            Generate sets from existing set ``NSETF``.

        lab1 : str
            Generate sets with these labels (see :ref:`cp` command for valid labels). Sets are numbered as
            the highest existing set number + 1.

        lab2 : str
            Generate sets with these labels (see :ref:`cp` command for valid labels). Sets are numbered as
            the highest existing set number + 1.

        lab3 : str
            Generate sets with these labels (see :ref:`cp` command for valid labels). Sets are numbered as
            the highest existing set number + 1.

        lab4 : str
            Generate sets with these labels (see :ref:`cp` command for valid labels). Sets are numbered as
            the highest existing set number + 1.

        lab5 : str
            Generate sets with these labels (see :ref:`cp` command for valid labels). Sets are numbered as
            the highest existing set number + 1.

        Notes
        -----

        .. _CPLGEN_notes:

        Generates additional sets of coupled nodes (with different labels) from an existing set ( :ref:`cp`,
        :ref:`cpngen` ). The same node numbers are included in the generated sets. If all labels of nodes
        are to be coupled and the nodes are coincident, the :ref:`nummrg` command should be used to
        automatically redefine the node number (for efficiency).
        """
        command = f"CPLGEN,{nsetf},{lab1},{lab2},{lab3},{lab4},{lab5}"
        return self.run(command, **kwargs)

    def cpmerge(self, lab: str = "", **kwargs):
        r"""Merges different couple sets with duplicate degrees of freedom into one couple set.

        Mechanical APDL Command: `CPMERGE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CPMERGE.html>`_

        Parameters
        ----------
        lab : str
            Degree of freedom label for coupled nodes (in the nodal coordinate system). Valid labels are:
            Structural labels: UX, UY, or UZ (displacements); ROTX, ROTY, or ROTZ (rotations) (in radians).
            Thermal labels: TEMP, TBOT, TE2, TE3...., TTOP (temperature). Fluid labels: PRES (pressure); VX,
            VY, or VZ (velocities). Electric labels: VOLT (voltage); EMF (electromotive force drop); CURR
            (current). Magnetic labels: MAG (scalar magnetic potential); AZ (vector magnetic potential);
            CURR (current). Diffusion label: CONC (concentration). The degree of freedom set is determined
            from all element types defined and the :ref:`dof` command, if used.
        """
        command = f"CPMERGE,{lab}"
        return self.run(command, **kwargs)

    def cpintf(self, lab: str = "", toler: str = "", **kwargs):
        r"""Defines coupled degrees of freedom at an interface.

        Mechanical APDL Command: `CPINTF <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CPINTF.html>`_

        Parameters
        ----------
        lab : str
            Degree of freedom label for coupled nodes (in the nodal coordinate system). If ALL, use all
            appropriate labels except HDSP. Valid labels are: Structural labels: UX, UY, or UZ
            (displacements); ROTX, ROTY, or ROTZ (rotations, in radians), HDSP (hydrostatic pressure).
            Thermal labels: TEMP, TBOT, TE2, TE3...., TTOP (temperature). Fluid labels: PRES (pressure); VX,
            VY, or VZ (velocities). Electric labels: VOLT (voltage); EMF (electromotive force drop); CURR
            (current). Magnetic labels: MAG (scalar magnetic potential); AZ (vector magnetic potential);
            CURR (current). Diffusion label: CONC (concentration).

        toler : str
            Tolerance for coincidence (based on maximum coordinate difference in each global Cartesian
            direction for node locations and on angle differences for node orientations). Defaults to
            0.0001. Only nodes within the tolerance are considered to be coincident for coupling.

        Notes
        -----

        .. _CPINTF_notes:

        Defines coupled degrees of freedom between coincident nodes (within a tolerance). May be used, for
        example, to "button" together elements interfacing at a seam, where the seam consists of a series of
        node pairs. One coupled set is generated for each selected degree of freedom for each pair of
        coincident nodes. For more than two coincident nodes in a cluster, a coupled set is generated from
        the lowest numbered node to each of the other nodes in the cluster. Coupled sets are generated only
        within (and not between) clusters. If fewer than all nodes are to be checked for coincidence, use
        the :ref:`nsel` command to select nodes. Coupled set reference numbers are incremented by one from
        the highest previous set number. Use :ref:`cplist` to display the generated sets. Only nodes having
        the same nodal coordinate system orientations ("coincident" within a tolerance) are included. Use
        the :ref:`ceintf` command to connect nodes by constraint equations instead of by coupling. Use the
        :ref:`eintf` command to connect nodes by line elements instead of by coupling.
        """
        command = f"CPINTF,{lab},{toler}"
        return self.run(command, **kwargs)

    def cpdele(
        self, nset1: str = "", nset2: str = "", ninc: str = "", nsel: str = "", **kwargs
    ):
        r"""Deletes coupled degree of freedom sets.

        Mechanical APDL Command: `CPDELE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CPDELE.html>`_

        Parameters
        ----------
        nset1 : str
            Delete coupled sets from ``NSET1`` to ``NSET2`` (defaults to ``NSET1`` ) in steps of ``NINC``
            (defaults to 1). If ``NSET1`` = ALL, ``NSET2`` and ``NINC`` are ignored and all coupled sets are
            deleted.

        nset2 : str
            Delete coupled sets from ``NSET1`` to ``NSET2`` (defaults to ``NSET1`` ) in steps of ``NINC``
            (defaults to 1). If ``NSET1`` = ALL, ``NSET2`` and ``NINC`` are ignored and all coupled sets are
            deleted.

        ninc : str
            Delete coupled sets from ``NSET1`` to ``NSET2`` (defaults to ``NSET1`` ) in steps of ``NINC``
            (defaults to 1). If ``NSET1`` = ALL, ``NSET2`` and ``NINC`` are ignored and all coupled sets are
            deleted.

        nsel : str
            Additional node selection control:

            * ``ANY`` - Delete coupled set if any of the selected nodes are in the set (default).

            * ``ALL`` - Delete coupled set only if all of the selected nodes are in the set.

        Notes
        -----

        .. _CPDELE_notes:

        See the :ref:`cp` command for a method to delete individual nodes from a set.
        """
        command = f"CPDELE,{nset1},{nset2},{ninc},{nsel}"
        return self.run(command, **kwargs)

    def cplist(
        self, nset1: str = "", nset2: str = "", ninc: str = "", nsel: str = "", **kwargs
    ):
        r"""Lists the coupled degree of freedom sets.

        Mechanical APDL Command: `CPLIST <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CPLIST.html>`_

        Parameters
        ----------
        nset1 : str
            List coupled sets from ``NSET1`` to ``NSET2`` (defaults to ``NSET1`` ) in steps of ``NINC``
            (defaults to 1). If ``NSET1`` = ALL (default), ``NSET2`` and ``NINC`` are ignored and all
            coupled sets are listed.

        nset2 : str
            List coupled sets from ``NSET1`` to ``NSET2`` (defaults to ``NSET1`` ) in steps of ``NINC``
            (defaults to 1). If ``NSET1`` = ALL (default), ``NSET2`` and ``NINC`` are ignored and all
            coupled sets are listed.

        ninc : str
            List coupled sets from ``NSET1`` to ``NSET2`` (defaults to ``NSET1`` ) in steps of ``NINC``
            (defaults to 1). If ``NSET1`` = ALL (default), ``NSET2`` and ``NINC`` are ignored and all
            coupled sets are listed.

        nsel : str
            Node selection control:

            * ``ANY`` - List coupled set if any of the selected nodes are in the set (default).

            * ``ALL`` - List coupled set only if all of the selected nodes are in the set.

        Notes
        -----

        .. _CPLIST_notes:

        This command is valid in any processor.
        """
        command = f"CPLIST,{nset1},{nset2},{ninc},{nsel}"
        return self.run(command, **kwargs)
