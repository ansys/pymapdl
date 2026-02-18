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
class MasterDof:

    def m(
        self,
        node: str = "",
        lab1: str = "",
        nend: str = "",
        ninc: str = "",
        lab2: str = "",
        lab3: str = "",
        lab4: str = "",
        lab5: str = "",
        lab6: str = "",
        support: str = "",
        **kwargs,
    ):
        r"""Defines master degrees of freedom (MDOFs) for superelement generation analyses.

        Mechanical APDL Command: `M <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_M.html>`_

        Parameters
        ----------
        node : str
            Node number at which an MDOF is defined. If ALL, define MDOFs at all selected nodes (
            :ref:`nsel` ). If ``NODE`` = P, graphical picking is enabled and all remaining command fields
            are ignored (valid only in the GUI). A component name may also be substituted for ``NODE``.

        lab1 : str
            Additional MDOF labels. The nodes defined are associated with each label specified.

        nend : str
            Define all nodes from ``NODE`` to ``NEND`` (defaults to ``NODE`` ) in steps of ``NINC``
            (defaults to 1) as MDOFs in the specified direction.

        ninc : str
            Define all nodes from ``NODE`` to ``NEND`` (defaults to ``NODE`` ) in steps of ``NINC``
            (defaults to 1) as MDOFs in the specified direction.

        lab2 : str
            Additional MDOF labels. The nodes defined are associated with each label specified.

        lab3 : str
            Additional MDOF labels. The nodes defined are associated with each label specified.

        lab4 : str
            Additional MDOF labels. The nodes defined are associated with each label specified.

        lab5 : str
            Additional MDOF labels. The nodes defined are associated with each label specified.

        lab6 : str
            Additional MDOF labels. The nodes defined are associated with each label specified.

        support : str
            Pseudo-constraints key for the free-interface ( :ref:`cmsopt`,FREE) and residual-flexible free-
            interface ( :ref:`cmsopt`, RFFB) CMS method analyses:

            OFF - Defined MDOFs remain free during the mode-extraction analysis (default).

            ON - Defined MDOFs are constrained during the mode-extraction analysis.

        Notes
        -----

        .. _M_notes:

        Defines master degrees of freedom (MDOFs) for superelement generation. If defined for other
        analyses, MDOFs are ignored. If used in the SOLUTION processor, this command is valid only within
        the first load step.

        Reissue :ref:`m` for additional MDOFs. The number of master nodes allowed is limited only by the
        maximum system memory available.

        The substructure ( :ref:`antype`,SUBSTR) analysis uses the matrix condensation technique to reduce
        the structure matrices to those characterized by a set of MDOFs.

        MDOFs are identified by a list of nodes and their nodal directions. The actual degree-of-freedom
        directions available for a given node depends upon the degrees of freedom associated with element
        types ( :ref:`et` ) at that node.

        There must be some mass (or stress stiffening in the case of a buckling analysis) associated with
        each MDOF (except for the VOLT label). The mass may be due either to the distributed mass of the
        element or due to discrete lumped masses at the node.

        If an MDOF is specified at a constrained point, it is ignored.

        If an MDOF is specified at a coupled node, it should be specified at the prime node of the coupled
        set.

        For cyclic symmetry superelements, if MDOFs are defined at both low- and high-edge nodes, the cyclic
        constraint equations between those nodes are ignored.

        Substructure analysis connection points must be defined as MDOFs.

        The ``SUPPORT`` argument is ignored for the fixed-interface CMS method analysis (
        :ref:`cmsopt`,FIX).

        This command is also valid in PREP7.
        """
        command = f"M,{node},{lab1},{nend},{ninc},{lab2},{lab3},{lab4},{lab5},{lab6},{support}"
        return self.run(command, **kwargs)

    def mdele(
        self,
        node: str = "",
        lab1: str = "",
        nend: str = "",
        ninc: str = "",
        lab2: str = "",
        lab3: str = "",
        lab4: str = "",
        lab5: str = "",
        lab6: str = "",
        support: str = "",
        **kwargs,
    ):
        r"""Deletes master degrees of freedom.

        Mechanical APDL Command: `MDELE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MDELE.html>`_

        Parameters
        ----------
        node : str
            Delete master degrees of freedom in the ``Lab1`` direction ( :ref:`m` ) from ``NODE`` to
            ``NEND`` (defaults to ``NODE`` ) in steps of ``NINC`` (defaults to 1). If ``NODE`` = ALL,
            ``NEND`` and ``NINC`` are ignored and masters for all selected nodes ( :ref:`nsel` ) are
            deleted. If ``Lab1`` = ALL, all label directions will be deleted. If ``NODE`` = P, graphical
            picking is enabled and all remaining command fields are ignored (valid only in the GUI). A
            component name may also be substituted for ``NODE``.

        lab1 : str
            Delete masters in these additional directions.

        nend : str
            Delete master degrees of freedom in the ``Lab1`` direction ( :ref:`m` ) from ``NODE`` to
            ``NEND`` (defaults to ``NODE`` ) in steps of ``NINC`` (defaults to 1). If ``NODE`` = ALL,
            ``NEND`` and ``NINC`` are ignored and masters for all selected nodes ( :ref:`nsel` ) are
            deleted. If ``Lab1`` = ALL, all label directions will be deleted. If ``NODE`` = P, graphical
            picking is enabled and all remaining command fields are ignored (valid only in the GUI). A
            component name may also be substituted for ``NODE``.

        ninc : str
            Delete master degrees of freedom in the ``Lab1`` direction ( :ref:`m` ) from ``NODE`` to
            ``NEND`` (defaults to ``NODE`` ) in steps of ``NINC`` (defaults to 1). If ``NODE`` = ALL,
            ``NEND`` and ``NINC`` are ignored and masters for all selected nodes ( :ref:`nsel` ) are
            deleted. If ``Lab1`` = ALL, all label directions will be deleted. If ``NODE`` = P, graphical
            picking is enabled and all remaining command fields are ignored (valid only in the GUI). A
            component name may also be substituted for ``NODE``.

        lab2 : str
            Delete masters in these additional directions.

        lab3 : str
            Delete masters in these additional directions.

        lab4 : str
            Delete masters in these additional directions.

        lab5 : str
            Delete masters in these additional directions.

        lab6 : str
            Delete masters in these additional directions.

        support : str
            Pseudo-constraints key for the free-interface ( :ref:`cmsopt`,FREE) and residual-flexible free-
            interface ( :ref:`cmsopt`,RFFB) CMS method analyses:

            OFF - delete selected master degrees of freedom and any pseudo-constraints applied on them with
            SUPPORT = ON in the :ref:`m` command (default).

            ON - only delete any pseudo-constraints applied on selected master degrees of freedom.

        Notes
        -----

        .. _MDELE_notes:

        Deletes master degrees of freedom. If used in SOLUTION, this command is valid only within the first
        load step.

        The ``SUPPORT`` argument is ignored for the fixed-interface CMS method analysis (
        :ref:`cmsopt`,FIX).

        This command is also valid in PREP7.
        """
        command = f"MDELE,{node},{lab1},{nend},{ninc},{lab2},{lab3},{lab4},{lab5},{lab6},{support}"
        return self.run(command, **kwargs)

    def mgen(
        self,
        itime: str = "",
        inc: str = "",
        node1: str = "",
        node2: str = "",
        ninc: str = "",
        **kwargs,
    ):
        r"""Generates additional MDOF from a previously defined set.

        Mechanical APDL Command: `MGEN <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MGEN.html>`_

        Parameters
        ----------
        itime : str
            Do this generation operation a total of ``ITIME`` s, incrementing all nodes in the set by
            ``INC`` each time after the first. ``ITIME`` must be > 1 for generation to occur. All previously
            defined master degree of freedom directions are included in the set. A component name may also
            be substituted for ``ITIME``.

        inc : str
            Do this generation operation a total of ``ITIME`` s, incrementing all nodes in the set by
            ``INC`` each time after the first. ``ITIME`` must be > 1 for generation to occur. All previously
            defined master degree of freedom directions are included in the set. A component name may also
            be substituted for ``ITIME``.

        node1 : str
            Generate master degrees of freedom from set beginning with ``NODE1`` to ``NODE2`` (defaults to
            ``NODE1`` ) in steps of ``NINC`` (defaults to 1). If ``NODE1`` = ALL, ``NODE2`` and ``NINC`` are
            ignored and set is all selected nodes ( :ref:`nsel` ). If ``NODE1`` = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in the GUI).

        node2 : str
            Generate master degrees of freedom from set beginning with ``NODE1`` to ``NODE2`` (defaults to
            ``NODE1`` ) in steps of ``NINC`` (defaults to 1). If ``NODE1`` = ALL, ``NODE2`` and ``NINC`` are
            ignored and set is all selected nodes ( :ref:`nsel` ). If ``NODE1`` = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in the GUI).

        ninc : str
            Generate master degrees of freedom from set beginning with ``NODE1`` to ``NODE2`` (defaults to
            ``NODE1`` ) in steps of ``NINC`` (defaults to 1). If ``NODE1`` = ALL, ``NODE2`` and ``NINC`` are
            ignored and set is all selected nodes ( :ref:`nsel` ). If ``NODE1`` = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in the GUI).

        Notes
        -----

        .. _MGEN_notes:

        Generates additional master degrees of freedom from a previously defined set. If used in SOLUTION,
        this command is valid only within the first load step.

        For the free-interface ( :ref:`cmsopt`, FREE) and residual-flexible free-interface ( :ref:`cmsopt`,
        RFFB) CMS method analyses, pseudo-constraints could have been applied on some master degrees of
        freedom of the previously defined set (SUPPORT = ON in the :ref:`m` command). The master degrees of
        freedom generated from these with the :ref:`mgen` command are also defined with pseudo-constraints.

        This command is also valid in PREP7.
        """
        command = f"MGEN,{itime},{inc},{node1},{node2},{ninc}"
        return self.run(command, **kwargs)

    def mlist(self, node1: str = "", node2: str = "", ninc: str = "", **kwargs):
        r"""Lists the MDOF of freedom.

        Mechanical APDL Command: `MLIST <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MLIST.html>`_

        Parameters
        ----------
        node1 : str
            List master degrees of freedom from ``NODE1`` to ``NODE2`` (defaults to ``NODE1`` ) in steps of
            ``NINC`` (defaults to 1). If ``NODE1`` = ALL (default), ``NODE2`` and ``NINC`` are ignored and
            masters for all selected nodes ( :ref:`nsel` ) are listed. If ``NODE1`` = P, graphical picking
            is enabled and all remaining command fields are ignored (valid only in the GUI). A component
            name may also be substituted for ``NODE1`` ( ``NODE2`` and ``NINC`` are ignored).

        node2 : str
            List master degrees of freedom from ``NODE1`` to ``NODE2`` (defaults to ``NODE1`` ) in steps of
            ``NINC`` (defaults to 1). If ``NODE1`` = ALL (default), ``NODE2`` and ``NINC`` are ignored and
            masters for all selected nodes ( :ref:`nsel` ) are listed. If ``NODE1`` = P, graphical picking
            is enabled and all remaining command fields are ignored (valid only in the GUI). A component
            name may also be substituted for ``NODE1`` ( ``NODE2`` and ``NINC`` are ignored).

        ninc : str
            List master degrees of freedom from ``NODE1`` to ``NODE2`` (defaults to ``NODE1`` ) in steps of
            ``NINC`` (defaults to 1). If ``NODE1`` = ALL (default), ``NODE2`` and ``NINC`` are ignored and
            masters for all selected nodes ( :ref:`nsel` ) are listed. If ``NODE1`` = P, graphical picking
            is enabled and all remaining command fields are ignored (valid only in the GUI). A component
            name may also be substituted for ``NODE1`` ( ``NODE2`` and ``NINC`` are ignored).

        Notes
        -----

        .. _MLIST_notes:

        Lists the master degrees of freedom.

        For the free-interface CMS method analysis ( :ref:`cmsopt`,FREE),Â any pseudo-constraints applied on
        master degrees of freedom with ``SUPPORT`` = ON in the :ref:`m` command will be listedÂ when
        :ref:`mlist` is issued after :ref:`cmsopt` (see example printout below).

        .. code:: apdl

               NODE  LABEL     SUPPORT
                8529  UX
                8529  UY
                8529  UZ
                8545  UX         ON
                8545  UY         ON
                8545  UZ         ON
        """
        command = f"MLIST,{node1},{node2},{ninc}"
        return self.run(command, **kwargs)
