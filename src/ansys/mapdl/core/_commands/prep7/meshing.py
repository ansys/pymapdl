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

class Meshing:

    def aatt(self, mat: str = "", real: str = "", type_: str = "", esys: str = "", secn: str = "", **kwargs):
        r"""Associates element attributes with the selected, unmeshed areas.

        Mechanical APDL Command: `AATT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_AATT.html>`_

        Parameters
        ----------
        mat : str
            The material number to be associated with selected, unmeshed areas.

        real : str
            The real constant set number to be associated with selected, unmeshed areas.

        type_ : str
            The type number to be associated with selected, unmeshed areas.

        esys : str
            The coordinate system number to be associated with selected, unmeshed areas.

        secn : str
            The section number to be associated with selected unmeshed areas.

        Notes
        -----

        .. _AATT_notes:

        Areas subsequently generated from the areas will also have these attributes. These element
        attributes will be used when the areas are meshed. If an area does not have attributes associated
        with it (by this command) at the time it is meshed, the attributes are obtained from the then
        current :ref:`mat`, :ref:`real`, :ref:`type`, :ref:`esys`, and :ref:`secnum` command settings.
        Reissue the :ref:`aatt` command (before areas are meshed) to change the attributes. A zero (or
        blank) argument removes the corresponding association. If any of the arguments ``MAT``, ``REAL``,
        ``TYPE``, ``ESYS``, or ``SECN`` are defined as -1, then that value will be left unchanged in the
        selected set.

        In some cases, Mechanical APDL can proceed with an area meshing operation even when no logical
        element type
        has been assigned via :ref:`aatt`, ``TYPE`` or :ref:`type`. For more information, see the
        discussion on setting element attributes in `Meshing Your Solid Model
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD7_5.html#modmeshvaidck31400>`_
        in the `Modeling and Meshing Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD14.html>`_.
        """
        command = f"AATT,{mat},{real},{type_},{esys},{secn}"
        return self.run(command, **kwargs)



    def accat(self, na1: str = "", na2: str = "", **kwargs):
        r"""Concatenates multiple areas in preparation for mapped meshing.

        Mechanical APDL Command: `ACCAT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ACCAT.html>`_

        Parameters
        ----------
        na1 : str
            Areas to be concatenated. If ``NA1`` = ALL, ``NA2`` will be ignored and all selected areas (
            :ref:`asel` ) will be concatenated. If ``NA1`` = P, graphical picking is enabled and all
            remaining arguments are ignored (valid only in the GUI). A component name may also be
            substituted for ``NA1`` ( ``NA2`` is ignored).

        na2 : str
            Areas to be concatenated. If ``NA1`` = ALL, ``NA2`` will be ignored and all selected areas (
            :ref:`asel` ) will be concatenated. If ``NA1`` = P, graphical picking is enabled and all
            remaining arguments are ignored (valid only in the GUI). A component name may also be
            substituted for ``NA1`` ( ``NA2`` is ignored).

        Notes
        -----

        .. _ACCAT_notes:

        Concatenates multiple, adjacent areas (the input areas) into one area (the output area) in
        preparation for mapped meshing. A volume that contains too many areas for mapped meshing can still
        be mapped meshed if some of the areas in that volume are first concatenated (see `Meshing Your Solid
        Model
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD7_5.html#modmeshvaidck31400>`_
        in the `Modeling and Meshing Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD14.html>`_ for details on
        mapped meshing restrictions).

        Because of modeling restrictions that result from its use, :ref:`accat` is meant to be used solely
        for meshing. Specifically, (a) the output area and any volumes that have the output area on their
        area list ( :ref:`vlist` ) cannot be used as input to any other solid modeling operation (not even
        another :ref:`accat` command); and (b) the output area cannot accept solid model boundary conditions
        ( :ref:`da`, :ref:`sfa` ).

        The output area (or volumes which contain it) will be meshed ( :ref:`amesh`, :ref:`vmesh` ) by
        meshing the input areas, which themselves must be meshable. The output area from the :ref:`accat`
        operation will be coincident with the input areas and the input areas will be retained. Consider the
        :ref:`aadd` command instead of :ref:`accat` if you wish to delete the input areas. When an
        :ref:`accat` command is issued, volume area lists ( :ref:`vlist` ) that contain all of the input
        areas will be updated so that the volume area lists refer to the output area instead of the input
        area. Deletion of the output area ( :ref:`adele` ) effectively reverses the :ref:`accat` operation
        and restores volume area lists to their original condition. :ref:`accat` operations on pairs of
        adjacent four-sided areas automatically concatenate appropriate lines ( :ref:`lccat` ); in all other
        situations, line concatenations must be addressed by the user.

        You can use the :ref:`asel` command to select areas that were created by concatenation, and then
        follow it with an :ref:`adele`,ALL command to delete them. See `Meshing Your Solid Model
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD7_5.html#modmeshvaidck31400>`_
         in the `Modeling and Meshing Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD14.html>`_ for a discussion
        on how to easily select and delete concatenated areas in
        one step.
        """
        command = f"ACCAT,{na1},{na2}"
        return self.run(command, **kwargs)



    def aclear(self, na1: str = "", na2: str = "", ninc: str = "", **kwargs):
        r"""Deletes nodes and area elements associated with selected areas.

        Mechanical APDL Command: `ACLEAR <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ACLEAR.html>`_

        Parameters
        ----------
        na1 : str
            Delete mesh for areas ``NA1`` to ``NA2`` (defaults to ``NA1`` ) in steps of ``NINC`` (defaults
            to 1). If ``NA1`` = ALL, ``NA2`` and ``NINC`` are ignored and the mesh for all selected areas (
            :ref:`asel` ) is deleted. If ``NA1`` = P, graphical picking is enabled and all remaining
            arguments are ignored (valid only in the GUI). A component name may also be substituted for
            ``NA1`` ( ``NA2`` and ``NINC`` are ignored).

        na2 : str
            Delete mesh for areas ``NA1`` to ``NA2`` (defaults to ``NA1`` ) in steps of ``NINC`` (defaults
            to 1). If ``NA1`` = ALL, ``NA2`` and ``NINC`` are ignored and the mesh for all selected areas (
            :ref:`asel` ) is deleted. If ``NA1`` = P, graphical picking is enabled and all remaining
            arguments are ignored (valid only in the GUI). A component name may also be substituted for
            ``NA1`` ( ``NA2`` and ``NINC`` are ignored).

        ninc : str
            Delete mesh for areas ``NA1`` to ``NA2`` (defaults to ``NA1`` ) in steps of ``NINC`` (defaults
            to 1). If ``NA1`` = ALL, ``NA2`` and ``NINC`` are ignored and the mesh for all selected areas (
            :ref:`asel` ) is deleted. If ``NA1`` = P, graphical picking is enabled and all remaining
            arguments are ignored (valid only in the GUI). A component name may also be substituted for
            ``NA1`` ( ``NA2`` and ``NINC`` are ignored).

        Notes
        -----

        .. _ACLEAR_notes:

        Deletes all nodes and area elements associated with selected areas (regardless of whether the nodes
        or elements are selected). Nodes shared by adjacent meshed areas and nodes associated with non-area
        elements will not be deleted. Attributes assigned as a result of :ref:`aatt` are maintained. In the
        program's response to the command, if an area, line, or keypoint is tallied as "cleared," it means
        either its node or element reference was deleted.

        This command is also valid for `rezoning
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_nlad/Hlp_G_ADVRZSMP.html>`_.
        When issued during rezoning (after the :ref:`remesh`,START command and before the
        :ref:`remesh`,FINISH command), :ref:`aclear` clears only the area generated by the :ref:`aremesh`
        command.
        """
        command = f"ACLEAR,{na1},{na2},{ninc}"
        return self.run(command, **kwargs)



    def aesize(self, anum: str = "", size: str = "", **kwargs):
        r"""Specifies the element size to be meshed onto areas.

        Mechanical APDL Command: `AESIZE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_AESIZE.html>`_

        Parameters
        ----------
        anum : str
            Area number of the area to which this element size specification applies. If ``ANUM`` = ALL,
            size applies to all selected areas. If ``ANUM`` = P, graphical picking is enabled. A component
            name may also be substituted for ``ANUM``.

        size : str
            Desired element size.

        Notes
        -----

        .. _AESIZE_notes:

        :ref:`aesize` allows control over the element sizing inside any area or on the face(s) of a volume.

        ``SIZE`` controls element size on the interior of the area. For any line on the area not having its
        own size assignment and not controlled by keypoint size assignments, it specifies the element size
        along the line as well, so long as no adjacent area has a smaller size, which would take precedence.
        If the :ref:`aesize` governs the boundary and SmartSizing is on, the boundary size can be refined
        for curvature or proximity.

        This command is also valid for `rezoning
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_nlad/Hlp_G_ADVRZSMP.html>`_.
        """
        command = f"AESIZE,{anum},{size}"
        return self.run(command, **kwargs)



    def amap(self, area: str = "", kp1: str = "", kp2: str = "", kp3: str = "", kp4: str = "", **kwargs):
        r"""Generates a 2D mapped mesh based on specified area corners.

        Mechanical APDL Command: `AMAP <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_AMAP.html>`_

        Parameters
        ----------
        area : str
            Area number of area to be meshed. If ``AREA`` = P, graphical picking is enabled and all
            remaining arguments are ignored (valid only in the GUI).

        kp1 : str
            Keypoints defining corners of the mapped mesh. Three or four corners may be specified, and may
            be input in any order.

        kp2 : str
            Keypoints defining corners of the mapped mesh. Three or four corners may be specified, and may
            be input in any order.

        kp3 : str
            Keypoints defining corners of the mapped mesh. Three or four corners may be specified, and may
            be input in any order.

        kp4 : str
            Keypoints defining corners of the mapped mesh. Three or four corners may be specified, and may
            be input in any order.

        Notes
        -----

        .. _AMAP_notes:

        Only one area at a time can be meshed with this command. The program internally concatenates all
        lines between the specified keypoints, then meshes the area with all quadrilateral elements. If line
        divisions are set, the mesh will follow the rules for mapped meshing (see  `Meshing Your Solid
        Model
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD7_5.html#modmeshvaidck31400>`_
        in the `Modeling and Meshing Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD14.html>`_).

        If the area being meshed has concatenated lines, the program will ask if those concatenations should
        be removed (in batch, the concatenations will automatically be removed). Nodes required for the
        generated elements are created and assigned the lowest available node numbers. If a mapped mesh is
        not possible due to mismatched line divisions or poor element shapes, the meshing operation is
        aborted.
        """
        command = f"AMAP,{area},{kp1},{kp2},{kp3},{kp4}"
        return self.run(command, **kwargs)



    def amesh(self, na1: str = "", na2: str = "", ninc: str = "", **kwargs):
        r"""Generates nodes and area elements within areas.

        Mechanical APDL Command: `AMESH <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_AMESH.html>`_

        Parameters
        ----------
        na1 : str
            Mesh areas from ``NA1`` to ``NA2`` (defaults to ``NA1`` ) in steps of ``NINC`` (defaults to 1).
            If ``NA1`` = ALL, ``NA2`` and ``NINC`` are ignored and all selected areas ( :ref:`asel` ) are
            meshed. If ``NA1`` = P, graphical picking is enabled and all remaining arguments are ignored
            (valid only in the GUI). A component name may also be substituted for ``NA1`` ( ``NA2`` and
            ``NINC`` are ignored).

        na2 : str
            Mesh areas from ``NA1`` to ``NA2`` (defaults to ``NA1`` ) in steps of ``NINC`` (defaults to 1).
            If ``NA1`` = ALL, ``NA2`` and ``NINC`` are ignored and all selected areas ( :ref:`asel` ) are
            meshed. If ``NA1`` = P, graphical picking is enabled and all remaining arguments are ignored
            (valid only in the GUI). A component name may also be substituted for ``NA1`` ( ``NA2`` and
            ``NINC`` are ignored).

        ninc : str
            Mesh areas from ``NA1`` to ``NA2`` (defaults to ``NA1`` ) in steps of ``NINC`` (defaults to 1).
            If ``NA1`` = ALL, ``NA2`` and ``NINC`` are ignored and all selected areas ( :ref:`asel` ) are
            meshed. If ``NA1`` = P, graphical picking is enabled and all remaining arguments are ignored
            (valid only in the GUI). A component name may also be substituted for ``NA1`` ( ``NA2`` and
            ``NINC`` are ignored).

        Notes
        -----

        .. _AMESH_notes:

        Any undefined nodes required for the generated elements are created and assigned the lowest
        available numbers.

        This command is also valid fo  r `rezoning
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_nlad/Hlp_G_ADVRZSMP.html>`_.
        """
        command = f"AMESH,{na1},{na2},{ninc}"
        return self.run(command, **kwargs)



    def arefine(self, na1: str = "", na2: str = "", ninc: str = "", level: str = "", depth: str = "", post: str = "", retain: str = "", **kwargs):
        r"""Refines the mesh around specified areas.

        Mechanical APDL Command: `AREFINE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_AREFINE.html>`_

        Parameters
        ----------
        na1 : str
            Areas ( ``NA1`` to ``NA2`` in increments of ``NINC`` ) around which the mesh is to be refined.
            ``NA2`` defaults to ``NA1``, and ``NINC`` defaults to 1. If ``NA1`` = ALL, ``NA2`` and ``NINC``
            are ignored and all selected areas are used for refinement. If ``NA1`` = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in the GUI). A component name
            may also be substituted for ``NA1`` ( ``NA2`` and ``NINC`` are ignored).

        na2 : str
            Areas ( ``NA1`` to ``NA2`` in increments of ``NINC`` ) around which the mesh is to be refined.
            ``NA2`` defaults to ``NA1``, and ``NINC`` defaults to 1. If ``NA1`` = ALL, ``NA2`` and ``NINC``
            are ignored and all selected areas are used for refinement. If ``NA1`` = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in the GUI). A component name
            may also be substituted for ``NA1`` ( ``NA2`` and ``NINC`` are ignored).

        ninc : str
            Areas ( ``NA1`` to ``NA2`` in increments of ``NINC`` ) around which the mesh is to be refined.
            ``NA2`` defaults to ``NA1``, and ``NINC`` defaults to 1. If ``NA1`` = ALL, ``NA2`` and ``NINC``
            are ignored and all selected areas are used for refinement. If ``NA1`` = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in the GUI). A component name
            may also be substituted for ``NA1`` ( ``NA2`` and ``NINC`` are ignored).

        level : str
            Amount of refinement to be done. Specify the value of ``LEVEL`` as an integer from 1 to 5, where
            a value of 1 provides minimal refinement, and a value of 5 provides maximum refinement (defaults
            to 1).

        depth : str
            Depth of mesh refinement in terms of the number of elements outward from the indicated areas
            (defaults to 1).

        post : str
            Type of postprocessing to be done after element splitting, in order to improve element quality:

            * ``OFF`` - No postprocessing will be done.

            * ``SMOOTH`` - Smoothing will be done. Node locations may change.

            * ``CLEAN`` - Smoothing and cleanup will be done. Existing elements may be deleted, and node
              locations may change (default).

        retain : str
            Flag indicating whether quadrilateral elements must be retained in the refinement of an all-
            quadrilateral mesh. (The Mechanical APDL program ignores the ``RETAIN`` argument when you are refining anything other than a quadrilateral mesh.)

            * ``ON`` - The final mesh will be composed entirely of quadrilateral elements, regardless of the
              element quality (default).

            * ``OFF`` - The final mesh may include some triangular elements in order to maintain element quality
              and provide transitioning.

        Notes
        -----

        .. _AREFINE_notes:

        :ref:`arefine` performs local mesh refinement around the specified areas. By default, the indi
         cated elements are split to create new elements with 1/2 the edge length of the original
        elements ( ``LEVEL`` = 1).

        :ref:`arefine` refines all area elements and tetrahedral volume elements that are adjacent to the
        specified areas. Any volume elements that are adjacent to the specified areas, but are not
        tetrahedra (for example, hexahedra, wedges, and pyramids), are not refined.

        You cannot use mesh refinement on a solid model that contains initial conditions at nodes (
        :ref:`ic` ), coupled nodes ( :ref:`cp` family of commands), constraint equations ( :ref:`ce` family
        of commands), or boundary conditions or loads applied directly to any of its nodes or elements. This
        applies to nodes and elements anywhere in the model, not just in the region where you want to
        request mesh refinement. See `Revising Your Model
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD8_6.html>`_ in the
        `Modeling and Meshing Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD14.html>`_
        for additional restrictions on mesh refinement.

        This command is also valid for `rezoning
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_nlad/Hlp_G_ADVRZSMP.html>`_.
        """
        command = f"AREFINE,{na1},{na2},{ninc},{level},{depth},{post},{retain}"
        return self.run(command, **kwargs)



    def chkmsh(self, comp: str = "", **kwargs):
        r"""Checks area and volume entities for previous meshes.

        Mechanical APDL Command: `CHKMSH <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CHKMSH.html>`_

        Parameters
        ----------
        comp : str
            Name of component containing areas or volumes.

        Notes
        -----

        .. _CHKMSH_notes:

        :ref:`chkmsh` invokes a predefined Mechanical APDL macro that checks areas and volumes to find out
        if they
        were previously meshed. This macro name will appear in the log file ( :file:`Jobname.LOG` ) prior to
        area and volume meshing operations initiated through the GUI. This command is not intended to be
        typed in directly in a Mechanical APDL session (although it can be included in an input file for use
        via
        :ref:`input` ).
        """
        command = f"CHKMSH,{comp}"
        return self.run(command, **kwargs)



    def clrmshln(self, **kwargs):
        r"""Clears meshed entities.

        Mechanical APDL Command: `CLRMSHLN <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CLRMSHLN.html>`_

        Notes
        -----

        .. _CLRMSHLN_notes:

        When you use the GUI method to set the number of elements on specified lines, and any of those lines
        is connected to one or more meshed lines, areas, or volumes, the program gives you the option to
        clear the meshed entities. This occurs only when you perform this operation via the GUI; the program
        does not provide such an option when you use the command method ( :ref:`lesize` ).

        If you activate the mesh clearing option, the program invokes a Mechanical APDL macro,
        :ref:`clrmshln`,
        that clears the meshed entities. This macro name will appear in the log file ( :file:`Jobname.LOG`
        ). This macro is for the Mechanical APDL program's internal use only. This command is not intended
        to be
        typed in directly in a Mechanical APDL session, although it can be included in an input file for
        batch
        input or for use via :ref:`input`.
        """
        command = "CLRMSHLN"
        return self.run(command, **kwargs)



    def cpcyc(self, lab: str = "", toler: str = "", kcn: str = "", dx: str = "", dy: str = "", dz: str = "", knonrot: str = "", kmid: str = "", ceopt: str = "", **kwargs):
        r"""Couples the two side faces of a cyclically symmetric model for loadings that are the same on every
        segment.

        Mechanical APDL Command: `CPCYC <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CPCYC.html>`_

        Parameters
        ----------
        lab : str
            Degree of freedom label for coupled nodes (in the nodal coordinate system). If ALL, use all
            appropriate labels. Valid labels are: Structural labels: UX, UY, or UZ (displacements); ROTX,
            ROTY, or ROTZ (rotations, in radians). Thermal label: TEMP (temperature). Fluid label: PRES
            (pressure). Electric label: VOLT (voltage).

        toler : str
            Tolerance for coincidence (based on maximum coordinate difference in each global Cartesian
            direction for node locations and on angle differences for node orientations). Defaults to
            0.0001. Only nodes within the tolerance are considered to be coincident for coupling.

        kcn : str
            In coordinate system ``KCN``, two nodes are coupled when the coordinates of the first node (on
            the low boundary) plus the increments DX, DY, and DZ match the coordinates of the second node
            (on the high boundary).

        dx : str
            Node location increments in the active coordinate system (DR, Dθ, DZ for cylindrical, DR, D θ,
            DΦ for spherical or toroidal).

        dy : str
            Node location increments in the active coordinate system (DR, Dθ, DZ for cylindrical, DR, D θ,
            DΦ for spherical or toroidal).

        dz : str
            Node location increments in the active coordinate system (DR, Dθ, DZ for cylindrical, DR, D θ,
            DΦ for spherical or toroidal).

        knonrot : str
            When ``KNONROT`` = 0, the nodes on coupled sets are rotated into coordinate system ``KCN`` (see
            :ref:`nrotat` command description). When ``KNONROT`` = 1, the nodes are not rotated, and you
            should make sure that coupled nodal DOF directions are correct.

        kmid : str
            When ``KMID`` = 1, the midside nodes of the element edges are added to the coupled sets of the
            end nodes of edges with specified nodal DOFs, if the end nodes of an edge are coupled. By
            default ( ``KMID`` = 0), the midside nodes are not included in the coupled sets.

        ceopt : str
            When ``CEOPT`` = 1, the coupled sets are converted to constraint equations. Use this option to
            improve performance in a distributed-memory parallel ( DMP ) solution. By default ( ``CEOPT`` =
            0), the coupled sets are not converted to constraint equations.

        Notes
        -----

        .. _CPCYC_notes:

        Cyclic coupling requires identical node and element patterns on the low and high sector boundaries.
        The :ref:`mshcopy` operation allows convenient generation of identical node and element patterns.
        See `Using CPCYC and MSHCOPY Commands
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD7_8.html#>`_ in the
        `Modeling and Meshing Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD14.html>`_ for more
        information.

        Although developed initially for use with cyclically symmetric models, use of the :ref:`cpcyc`
        command is not limited to cyclic symmetry analyses.

        **Example Usage**
        `Using CPCYC and MSHCOPY Commands
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD7_8.html#>`_
        """
        command = f"CPCYC,{lab},{toler},{kcn},{dx},{dy},{dz},{knonrot},{kmid},{ceopt}"
        return self.run(command, **kwargs)



    def czdel(self, grp1: str = "", grp2: str = "", grp3: str = "", **kwargs):
        r"""Edits or clears cohesive zone sections.

        Mechanical APDL Command: `CZDEL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CZDEL.html>`_

        Parameters
        ----------
        grp1 : str
            Initial group of cohesive zone elements to be deleted.

        grp2 : str
            Final group of cohesive zone elements to be deleted.

        grp3 : str
            Increment for selected groups.

        Notes
        -----
        The :ref:`czdel` command edits or deletes the interface elements and nodes, along with the
        associated changes made to the underlying plane or solid elements created during a previous
        :ref:`czmesh` operation.

        Each :ref:`czmesh` operation will create groups of elements and nodes with component names in the
        format CZME_EL01 (elements) and CZME_ND01 (nodes). The final number of this format will be the
        number used for ``grp1`` and ``grp2``. If ``grp1`` = ALL, all nodes and elements created by the
        :ref:`czmesh` command will be deleted. After using :ref:`czdel`, all the user-defined components
        will be unselected.

        The :ref:`czdel` command is valid for structural analyses only.
        """
        command = f"CZDEL,{grp1},{grp2},{grp3}"
        return self.run(command, **kwargs)



    def czmesh(self, ecomps1: str = "", ecomps2: str = "", kcn: str = "", kdir: str = "", value: str = "", cztol: str = "", **kwargs):
        r"""Create and mesh an interface area composed of cohesive zone elements.

        Mechanical APDL Command: `CZMESH <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CZMESH.html>`_

        Parameters
        ----------
        ecomps1 : str
            Component name or number for the group of plane or solid structural elements adjacent to the
            interface being meshed.

        ecomps2 : str
            Component name or number for the opposing (from ``ecomps1`` ) group of plane or solid structural
            elements adjacent to the interface being meshed.

        kcn : str
            Coordinate system number for the separation surface and normal direction. (if ``ecomps1`` and
            ``ecomps2`` not specified)

        kdir : str
            Direction (x, y, or z) normal to separation surface in the ``KCN`` coordinate system (if
            ``ecomps1`` and ``ecomps2`` not specified).

        value : str
            Coordinate value along the ``KDIR`` axis at which to locate the interface (if ``ecomps1`` and
            ``ecomps2`` not specified).

        cztol : str
            Optional absolute tolerance about ``VALUE`` (if ``ecomps1`` and ``ecomps2`` not specified).
            Allows nodes occurring slightly above or below the separation to be grouped properly. The
            following expression represents the default value:

            .. math::

                equation not available  ``max`` - X ``min`` ).

        Notes
        -----

        .. _CZMESH_notes:

        :ref:`czmesh` is used on a mesh with shared nodes at the interface.

        If ``ecomps1`` and ``ecomps2`` are specified, the :ref:`czmesh` command creates/meshes interface
        elements ( ``INTER202``, ``INTER203``, ``INTER204``, ``INTER205`` ) along the boundary between the
        two components or groups of elements.

        The elements in each of the components or groups of elements share nodes with each other and also
        with the interface elements. This one-element thick boundary of interface elements splits the body
        between the two components or groups of elements.

        Subsequent separation (delamination and failure) of the interface zone results in an increasing
        displacement between the nodes (within the interface element) along the cohesive zone elements.
        Unless otherwise specified, the :ref:`czmesh` command analyzes the configuration and geometry of the
        adjacent structural elements and provides the appropriate interface element.

        The :ref:`czmesh` operation copies any nodal temperatures that you have defined on the split surface
        of the original mesh from the original nodes to the newly created coincident duplicate nodes.
        Displacements, forces, and other boundary conditions, however, are not copied; therefore, apply
        boundary conditions and loadings after issuing :ref:`czmesh`.

        If using :ref:`czmesh` to generate interface elements ( ``INTER202`` and ``INTER205`` ) in a `VCCT-
        based crack-growth simulation
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/Hlp_G_STR_VCCT.html#vcctsimassum>`_,
        be aware that those elements do not support degenerate shapes. Examine the resulting mesh,
        therefore, to verify correct element connectivity around the crack tip.

        This command does not support mesh regions with non-solid elements (such as surface-effect and shell
        elements).

        This command is valid for structural analyses only.
        """
        command = f"CZMESH,{ecomps1},{ecomps2},{kcn},{kdir},{value},{cztol}"
        return self.run(command, **kwargs)



    def desize(self, minl: str = "", minh: str = "", mxel: str = "", angl: str = "", angh: str = "", edgmn: str = "", edgmx: str = "", adjf: str = "", adjm: str = "", **kwargs):
        r"""Controls default element sizes.

        Mechanical APDL Command: `DESIZE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_DESIZE.html>`_

        **Command default:**

        .. _DESIZE_default:

        Default settings as described for each argument are used.

        Parameters
        ----------
        minl : str
            Minimum number of elements that will be attached to a line when using lower-order elements
            (defaults to 3 elements per line). If ``MINL`` = DEFA, all arguments will be set back to default
            values. If ``MINL`` = ``STAT``, list status of command (Including on/off status). If ``MINL`` =
            OFF, deactivate default element sizing. If ``MINL`` = ON, reactivate default element sizing.

        minh : str
            Minimum number of elements that will be attached to a line when using higher-order elements.
            Defaults to 2 elements per line.

        mxel : str
            Maximum number of elements that will be attached to a single line (lower or higher-order
            elements). Defaults to 15 elements per line for h-elements. To deactivate this limit, specify a
            large number (such as 9999).

        angl : str
            Maximum spanned angle per lower-order element for curved lines. Defaults to 15 degrees per
            element.

        angh : str
            Maximum spanned angle per higher-order element for curved lines. Defaults to 28 degrees per
            element.

        edgmn : str
            Minimum element edge length. Defaults to no minimum edge length. The ``MINL`` or ``MINH``
            argument can override this value.

        edgmx : str
            Maximum element edge length. Defaults to no maximum edge length. The ``MXEL`` argument can
            override this value.

        adjf : str
            Target aspect ratio for adjacent line. Used only when free meshing. Defaults to 1.0, which
            attempts to create equal-sided h-elements.

        adjm : str
            Target aspect ratio for adjacent line. Used only when map meshing. Defaults to 4.0, which
            attempts to create rectangular h-elements.

        Notes
        -----

        .. _DESIZE_notes:

        :ref:`desize` settings are usually used for mapped meshing. They are also used for free meshing if
        SmartSizing is turned off ( :ref:`smrtsize`,OFF), which is the default. Even when SmartSizing is on,
        some :ref:`desize` settings (such as maximum and minimum element edge length) can affect free mesh
        density. The default settings of the :ref:`desize` command are used only when no other element size
        specifications ( :ref:`kesize`, :ref:`lesize`, :ref:`esize` ) exist for a certain line.

        This command is also valid for `rezoning
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_nlad/Hlp_G_ADVRZSMP.html>`_.
        """
        command = f"DESIZE,{minl},{minh},{mxel},{angl},{angh},{edgmn},{edgmx},{adjf},{adjm}"
        return self.run(command, **kwargs)



    def eorient(self, etype: str = "", dir_: str = "", toler: str = "", **kwargs):
        r"""Reorients solid element normals.

        Mechanical APDL Command: `EORIENT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_EORIENT.html>`_

        Parameters
        ----------
        etype : str
            Specifies which elements to orient.

            * ``LYSL`` - Specifies that layered solid elements will be oriented. This value is the default.
              Layered element types affected by this option include ``SOLID185`` with KEYOPT(3) = 1, ``SOLID186``
              with KEYOPT(3) = 1, ``SOLSH190``, ``SOLID278`` with KEYOPT(3) = 1 or 2, and ``SOLID279`` with
              KEYOPT(3) = 1 or 2.

        dir_ : str
            The axis and direction for orientation, or an element number. If ``Dir`` is set to a positive number ( ``n`` ), then all eligible elements are oriented as similarly as possible to element ``n``.

            * ``NEGX`` - The element face with the outward normal most nearly parallel to the element coordinate
              system``s negative x-axis is designated (reoriented) as face 1.

            * ``POSX`` - The element face with the outward normal most nearly parallel to the element coordinate
              system``s positive x-axis is designated (reoriented) as face 1.

            * ``NEGY`` - The element face with the outward normal most nearly parallel to the element coordinate
              system``s negative y-axis is designated (reoriented) as face 1..

            * ``POSY`` - The element face with the outward normal most nearly parallel to the element coordinate
              system``s positive y-axis is designated (reoriented) as face 1.

            * ``NEGZ`` - (Default) The element face with the outward normal most nearly parallel to the element
              coordinate system``s negative z-axis is designated (reoriented) as face 1.

            * ``POSZ`` - The element face with the outward normal most nearly parallel to the element coordinate
              system``s positive z-axis is designated (reoriented) as face 1.

        toler : str
            The maximum angle (in degrees) between the outward normal face and the target axis. Default is
            90.0. Lower ``TOLER`` values will reduce the number of faces that are considered as the basis of
            element reorientation.

        Notes
        -----

        .. _EORIENT_notes:

        :ref:`eorient` renumbers the element faces, designating the face most parallel to the XY plane of
        the element coordinate system (set with :ref:`esys` ) as face 1 (nodes I-J-K-L, parallel to the
        layers in layered elements). It calculates the outward normal of each face and changes the node
        designation of the elements so the face with a normal most nearly parallel with and in the same
        general direction as the target axis becomes face 1.

        The target axis, defined by ``Dir``, is either the negative or positive indicated axis or the
        outward normal of face 1 of that element.

        All layered solid elements in the selected set are considered for reorientation. The elements
        affected are layered structural solids ( ``SOLID185``, ``SOLID186`` ), solid shell elements (
        ``SOLSH190`` ), and layered thermal elements ( ``SOLID278``, ``SOLID279`` ).

        After reorienting elements, you should always display and graphically review results using the
        :ref:`eshape` command. When plotting models with many or symmetric layers, it may be useful to
        temporarily reduce the number of layers to two, with one layer being much thicker than the other.

        You cannot use :ref:`eorient` to change the normal direction of any element that has a body or
        surface load. We recommend that you apply all of your loads only after ensuring that the element
        normal directions are acceptable.

        Prisms and tetrahedrals are also supported for non-layered solid elements. Prisms are supported for
        layered solid elements, including layered ``SOLID185``, layered ``SOLID186``, layered ``SOLID278``,
        layered ``SOLID279``, and ``SOLSH190``. However, layers parallel to the four-node face of the prism
        are not supported.
        """
        command = f"EORIENT,{etype},{dir_},{toler}"
        return self.run(command, **kwargs)



    def erefine(self, ne1: str = "", ne2: str = "", ninc: str = "", level: str = "", depth: str = "", post: str = "", retain: str = "", **kwargs):
        r"""Refines the mesh around specified elements.

        Mechanical APDL Command: `EREFINE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_EREFINE.html>`_

        Parameters
        ----------
        ne1 : str
            Elements ( ``NE1`` to ``NE2`` in increments of ``NINC`` ) around which the mesh is to be
            refined. ``NE2`` defaults to ``NE1``, and ``NINC`` defaults to 1. If ``NE1`` = ALL, ``NE2`` and
            ``NINC`` are ignored and all selected elements are used for refinement. If ``NE1`` = P,
            graphical picking is enabled and all remaining command fields are ignored (valid only in the
            GUI). A component name may also be substituted for ``NE1`` ( ``NE2`` and ``NINC`` are ignored).

        ne2 : str
            Elements ( ``NE1`` to ``NE2`` in increments of ``NINC`` ) around which the mesh is to be
            refined. ``NE2`` defaults to ``NE1``, and ``NINC`` defaults to 1. If ``NE1`` = ALL, ``NE2`` and
            ``NINC`` are ignored and all selected elements are used for refinement. If ``NE1`` = P,
            graphical picking is enabled and all remaining command fields are ignored (valid only in the
            GUI). A component name may also be substituted for ``NE1`` ( ``NE2`` and ``NINC`` are ignored).

        ninc : str
            Elements ( ``NE1`` to ``NE2`` in increments of ``NINC`` ) around which the mesh is to be
            refined. ``NE2`` defaults to ``NE1``, and ``NINC`` defaults to 1. If ``NE1`` = ALL, ``NE2`` and
            ``NINC`` are ignored and all selected elements are used for refinement. If ``NE1`` = P,
            graphical picking is enabled and all remaining command fields are ignored (valid only in the
            GUI). A component name may also be substituted for ``NE1`` ( ``NE2`` and ``NINC`` are ignored).

        level : str
            Amount of refinement to be done. Specify the value of ``LEVEL`` as an integer from 1 to 5, where
            a value of 1 provides minimal refinement, and a value of 5 provides maximum refinement (defaults
            to 1).

        depth : str
            Depth of mesh refinement in terms of number of elements outward from the indicated elements,
            ``NE1`` to ``NE2`` (defaults to 0).

        post : str
            Type of postprocessing to be done after element splitting, in order to improve element quality:

            * ``OFF`` - No postprocessing will be done.

            * ``SMOOTH`` - Smoothing will be done. Node locations may change.

            * ``CLEAN`` - Smoothing and cleanup will be done. Existing elements may be deleted, and node
              locations may change (default).

        retain : str
            Flag indicating whether quadrilateral elements must be retained in the refinement of an all-
            quadrilateral mesh. (The program ignores the ``RETAIN`` argument when you are refining anything other than a quadrilateral mesh.)

            * ``ON`` - The final mesh will be composed entirely of quadrilateral elements, regardless of the
              element quality (default).

            * ``OFF`` - The final mesh may include some triangular elements in order to maintain element quality
              and provide transitioning.

        Notes
        -----

        .. _EREFINE_notes:

        :ref:`erefine` refines all area elements and tetrahedral volume elements adjacent to the specified
        elements.

        Mesh refinement is not available on a solid model containing initial conditions at nodes ( :ref:`ic`
        ), coupled nodes ( :ref:`cp` family of commands), constraint equations ( :ref:`ce` family of
        commands), or boundary conditions or loads applied directly to any of its nodes or elements. This
        restriction applies to nodes and elements anywhere in the model, not just in the region where you
        want to request mesh refinement. If you have detached the mesh from the solid model, disable
        postprocessing cleanup or smoothing ( ``POST`` = OFF) after refinement to preserve the element
        attributes.

        For more information about mesh refinement, see `Revising Your Model
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD8_6.html>`_.

        This command is also valid for `rezoning
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_nlad/Hlp_G_ADVRZSMP.html>`_.
        """
        command = f"EREFINE,{ne1},{ne2},{ninc},{level},{depth},{post},{retain}"
        return self.run(command, **kwargs)



    def esize(self, size: str = "", ndiv: str = "", **kwargs):
        r"""Specifies the default number of line divisions.

        Mechanical APDL Command: `ESIZE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ESIZE.html>`_

        Parameters
        ----------
        size : str
            Default element edge length on surface boundaries (that is, lines). Divisions are automatically
            calculated (rounded upward to next integer) from line lengths. If ``SIZE`` is zero (or blank),
            use ``NDIV``.

        ndiv : str
            Default number of element divisions along region boundary lines. Not used if ``SIZE`` is input.

        Notes
        -----

        .. _ESIZE_notes:

        Specifies the default number of line divisions (elements) to be generated along the region boundary
        lines. The number of divisions may be defined directly or automatically calculated. Divisions
        defined directly for any line ( :ref:`lesize`, :ref:`kesize`, etc.) are retained. For adjacent
        regions, the divisions assigned to the common line for one region are also used for the adjacent
        region. See the :ref:`mopt` command for additional meshing options.

        For free meshing operations, if smart element sizing is being used ( :ref:`smrtsize` ) and
        :ref:`esize`, ``SIZE`` has been specified, ``SIZE`` will be used as a starting element size, but
        will be overridden (that is, a smaller size may be used) to accommodate curvature and small
        features.

        This command is also valid for `rezoning
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_nlad/Hlp_G_ADVRZSMP.html>`_.
        """
        command = f"ESIZE,{size},{ndiv}"
        return self.run(command, **kwargs)



    def esys(self, kcn: int | str = "", **kwargs):
        r"""Sets the element coordinate system attribute pointer.

        Mechanical APDL Command: `ESYS <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ESYS.html>`_

        **Command default:**

        .. _ESYS_default:

        Use element coordinate system orientation as defined (either by default or by KEYOPT setting) for
        the element (default).

        Parameters
        ----------
        kcn : int or str
            Coordinate system number:

            * ``0`` - Use element coordinate system orientation as defined (either by default or by KEYOPT
              setting) for the element (default).

            * ``N`` - Use element coordinate system orientation based on local coordinate system N (where N must
              be greater than 10). For global system 0, 1, or 2, define a local system N parallel to appropriate
              system with the :ref:`local` or :ref:`cs` command (for example: :ref:`local`,11,1).

        Notes
        -----

        .. _ESYS_notes:

        Identifies the local coordinate system to be used to define the element coordinate system of
        subsequently defined elements. Used only with area and volume elements. For non-layered volume
        elements, the local coordinate system N is simply assigned to be the element coordinate system. For
        shell and layered volume elements, the x and y axes of the local coordinate system N are projected
        onto the shell or layer plane to determine the element coordinate system. See `Understanding the
        Element Coordinate System
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_CH2_3.html#elemESYSchange>`_
         for more details. N refers to the coordinate system reference number ( ``KCN`` ) defined
        using the :ref:`local` (or similar) command. Element coordinate system numbers may be displayed(
        :ref:`pnum` ).
        """
        command = f"ESYS,{kcn}"
        return self.run(command, **kwargs)



    def fvmesh(self, keep: int | str = "", **kwargs):
        r"""Generates nodes and tetrahedral volume elements from detached exterior area elements (facets).

        Mechanical APDL Command: `FVMESH <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_FVMESH.html>`_

        Parameters
        ----------
        keep : int or str
            Specifies whether to keep the area elements after the tetrahedral meshing operation is complete.

            * ``0`` - Delete area elements (default).

            * ``1`` - Keep area elements.

        Notes
        -----

        .. _FVMESH_notes:

        The :ref:`fvmesh` command generates a tetrahedral volume mesh from a selected set of detached
        exterior area elements (facets). (Detached elements have no solid model associativity.) The area
        elements can be triangular-shaped, quadrilateral-shaped, or a mixture of the two.

        The :ref:`fvmesh` command is in contrast to the :ref:`vmesh` command, which requires a volume to be
        input.

        The main tetrahedra mesher ( :ref:`mopt`,VMESH,MAIN) is the only tetrahedra mesher that supports
        the :ref:`fvmesh` command. The alternate tetrahedra mesher ( :ref:`mopt`,VMESH,ALTERNATE) does not
        support :ref:`fvmesh`. ``MESH200`` elements do not support :ref:`fvmesh`.

        Tetrahedral mesh expansion ( :ref:`mopt`,TETEXPND, ``Value`` ) is supported for both the
        :ref:`fvmesh` and :ref:`vmesh` commands. Tet-mesh expansion is the only mesh control supported by
        :ref:`fvmesh`.

        Triangle- or quadrilateral-shaped elements may be used as input to the :ref:`fvmesh` command. Where
        quadrilaterals are used, the default behavior is for the pyramid-shaped elements to be formed at the
        boundary when the appropriate element type is specified. See the :ref:`mopt`,PYRA command for
        details.

        The :ref:`fvmesh` command does not support multiple "volumes." If you have multiple volumes in your
        model, select the surface elements for one "volume," while making sure that the surface elements for
        the other volumes are deselected. Then use :ref:`fvmesh` to generate a mesh for the first volume.
        Continue this procedure by selecting one volume at a time and meshing it, until all of the volumes
        in the model have been meshed.

        If an error occurs during the meshing operation, the area elements are kept even if ``KEEP`` = 0.
        """
        command = f"FVMESH,{keep}"
        return self.run(command, **kwargs)



    def gsgdata(self, lfiber: str = "", xref: str = "", yref: str = "", rotx0: str = "", roty0: str = "", **kwargs):
        r"""Specifies the reference point and defines the geometry in the fiber direction for the generalized
        plane strain element option.

        Mechanical APDL Command: `GSGDATA <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_GSGDATA.html>`_

        Parameters
        ----------
        lfiber : str
            Fiber length from the reference point. Defaults to 1.

        xref : str
            X coordinate of the reference point. Defaults to zero.

        yref : str
            Y coordinate of the reference point. Defaults to zero.

        rotx0 : str
            Rotation of the ending plane about X in radians Defaults to zero.

        roty0 : str
            Rotation of the ending plane about Y in radians Defaults to zero.

        Notes
        -----

        .. _GSGDATA_notes:

        The ending point is automatically determined from the starting (reference) point and the geometry
        inputs. All inputs are in the global Cartesian coordinate system. For more information about the
        generalized plane strain feature, see Generalized Plane Strain Option of Current-Technology Solid
        Elements in the  `Element Reference
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_BIBLIO.html>`_.
        """
        command = f"GSGDATA,{lfiber},{xref},{yref},{rotx0},{roty0}"
        return self.run(command, **kwargs)



    def imesh(self, laky: str = "", nsla: str = "", ntla: str = "", kcn: str = "", dx: str = "", dy: str = "", dz: str = "", tol: str = "", **kwargs):
        r"""Generates nodes and interface elements along lines or areas.

        Mechanical APDL Command: `IMESH <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_IMESH.html>`_

        Parameters
        ----------
        laky : str
            Copies mesh according to the following:

            * ``LINE or 1`` - Copies line mesh (default).

            * ``AREA or 2`` - Copies area mesh.

        nsla : str
            Number that identifies the source line or area. This is the line or area whose mesh will provide
            the pattern for the interface elements. Mechanical APDL copies the pattern of the line or area
            elements through the area or volume to create the mesh of area or volume interface elements.

        ntla : str
            Number that identifies the target line or area. This is the line or area that is opposite the
            source line or area specified by ``NSLA``. Add ``NTLA`` to obtain the copied mesh from the
            source line or area.

        kcn : str
            Number that identifies the particular Mechanical APDL coordinate system.

        dx : str
            Incremental translation of node coordinates in the active coordinate system ( ``DR``, ``Dθ``,
            ``DZ`` for cylindrical, and ``DR``, ``Dθ``, ``DΦ`` for spherical or toroidal). The source line
            or area coordinates + ``DX``, ``DY``, ``DZ`` = the target line or area coordinates. If left
            blank, Mechanical APDL automatically estimates the incremental translation.

        dy : str
            Incremental translation of node coordinates in the active coordinate system ( ``DR``, ``Dθ``,
            ``DZ`` for cylindrical, and ``DR``, ``Dθ``, ``DΦ`` for spherical or toroidal). The source line
            or area coordinates + ``DX``, ``DY``, ``DZ`` = the target line or area coordinates. If left
            blank, Mechanical APDL automatically estimates the incremental translation.

        dz : str
            Incremental translation of node coordinates in the active coordinate system ( ``DR``, ``Dθ``,
            ``DZ`` for cylindrical, and ``DR``, ``Dθ``, ``DΦ`` for spherical or toroidal). The source line
            or area coordinates + ``DX``, ``DY``, ``DZ`` = the target line or area coordinates. If left
            blank, Mechanical APDL automatically estimates the incremental translation.

        tol : str
            Tolerance for verifying topology and geometry. By default, Mechanical APDL automatically
            calculates the tolerance based on associated geometries.

        Notes
        -----

        .. _IMESH_notes:

        Generates nodes and interface elements along lines or areas. The :ref:`imesh` command requires that
        the target line or area exactly match the source line or area. Also, both target and source lines or
        areas must be in the same area or volume. The area or volume containing the source line or area must
        be meshed before executing :ref:`imesh`, while the area or volume containing the target line or area
        must be meshed after executing :ref:`imesh`.

        For three dimensional problems where ``LAKY`` = AREA, Mechanical APDL fills the interface layer as
        follows:
        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.
        """
        command = f"IMESH,{laky},{nsla},{ntla},{kcn},{dx},{dy},{dz},{tol}"
        return self.run(command, **kwargs)



    def katt(self, mat: str = "", real: str = "", type_: str = "", esys: str = "", **kwargs):
        r"""Associates attributes with the selected, unmeshed keypoints.

        Mechanical APDL Command: `KATT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_KATT.html>`_

        Parameters
        ----------
        mat : str
            Material number, real constant set number, type number, and coordinate system number to be
            associated with selected, unmeshed keypoints.

        real : str
            Material number, real constant set number, type number, and coordinate system number to be
            associated with selected, unmeshed keypoints.

        type_ : str
            Material number, real constant set number, type number, and coordinate system number to be
            associated with selected, unmeshed keypoints.

        esys : str
            Material number, real constant set number, type number, and coordinate system number to be
            associated with selected, unmeshed keypoints.

        Notes
        -----

        .. _KATT_notes:

        Keypoints subsequently generated from the keypoints will also have these attributes. These element
        attributes will be used when the keypoints are meshed. If a keypoint does not have attributes
        associated with it (by this command) at the time it is meshed, the attributes are obtained from the
        then current :ref:`mat`, :ref:`real`, :ref:`type`, and :ref:`esys` command settings. Reissue the
        :ref:`katt` command (before keypoints are meshed) to change the attributes. A zero (or blank)
        argument removes the corresponding association.

        If any of the arguments ``MAT``, ``REAL``, ``TYPE``, or ``ESYS`` are defined as -1, then that value
        will be left unchanged in the selected set.

        In some cases, Mechanical APDL can proceed with a keypoint meshing operation even when no logical
        element
        type has been assigned via :ref:`katt`, ``TYPE`` or :ref:`type`. For more information, see the
        discussion on setting element attributes in `Meshing Your Solid Model
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD7_8.html>`_ eshing Your
        Solid Model in the `Modeling and Meshing Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD14.html>`_.
        """
        command = f"KATT,{mat},{real},{type_},{esys}"
        return self.run(command, **kwargs)



    def kclear(self, np1: str = "", np2: str = "", ninc: str = "", **kwargs):
        r"""Deletes nodes and point elements associated with selected keypoints.

        Mechanical APDL Command: `KCLEAR <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_KCLEAR.html>`_

        Parameters
        ----------
        np1 : str
            Delete mesh for keypoints ``NP1`` to ``NP2`` (defaults to ``NP1`` ) in steps of ``NINC``
            (defaults to 1). If ``NP1`` = ALL, ``NP2`` and ``NINC`` are ignored and the mesh for all
            selected keypoints ( :ref:`ksel` ) is deleted. If ``NP1`` = P, graphical picking is enabled and
            all remaining command fields are ignored (valid only in the GUI). A component name may also be
            substituted for ``NP1``.

        np2 : str
            Delete mesh for keypoints ``NP1`` to ``NP2`` (defaults to ``NP1`` ) in steps of ``NINC``
            (defaults to 1). If ``NP1`` = ALL, ``NP2`` and ``NINC`` are ignored and the mesh for all
            selected keypoints ( :ref:`ksel` ) is deleted. If ``NP1`` = P, graphical picking is enabled and
            all remaining command fields are ignored (valid only in the GUI). A component name may also be
            substituted for ``NP1``.

        ninc : str
            Delete mesh for keypoints ``NP1`` to ``NP2`` (defaults to ``NP1`` ) in steps of ``NINC``
            (defaults to 1). If ``NP1`` = ALL, ``NP2`` and ``NINC`` are ignored and the mesh for all
            selected keypoints ( :ref:`ksel` ) is deleted. If ``NP1`` = P, graphical picking is enabled and
            all remaining command fields are ignored (valid only in the GUI). A component name may also be
            substituted for ``NP1``.

        Notes
        -----

        .. _KCLEAR_notes:

        Deletes all nodes and point elements associated with selected keypoints (regardless of whether the
        nodes or elements are selected). Nodes associated with non-point elements will not be deleted.
        Attributes assigned as a result of :ref:`katt` are maintained. In the program's response to the
        command, if a keypoint is tallied as cleared, it means either its node or element reference was
        deleted.
        """
        command = f"KCLEAR,{np1},{np2},{ninc}"
        return self.run(command, **kwargs)



    def kesize(self, npt: str = "", size: str = "", fact1: str = "", fact2: str = "", **kwargs):
        r"""Specifies the edge lengths of the elements nearest a keypoint.

        Mechanical APDL Command: `KESIZE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_KESIZE.html>`_

        Parameters
        ----------
        npt : str
            Number of the keypoint whose lines will be adjusted. If ALL, use all selected keypoints (
            :ref:`ksel` ). If ``NPT`` = P, graphical picking is enabled and all remaining command fields are
            ignored (valid only in the GUI).

        size : str
            Size of elements along lines nearest keypoint ``NPT`` (overrides any other specified size). If
            ``SIZE`` is zero (or blank), use ``FACT1`` or ``FACT2``.

        fact1 : str
            Scale factor applied to a previously defined ``SIZE``. Not used if ``SIZE`` is input.

        fact2 : str
            Scale factor applied to the minimum element division at keypoint ``NPT`` for any attached line.
            This feature is useful with adaptive mesh refinement. Not used if ``SIZE`` or ``FACT1`` is
            input.

        Notes
        -----

        .. _KESIZE_notes:

        Affects only the line divisions adjacent to the keypoint on lines not previously assigned divisions
        by other line commands ( :ref:`lesize`, etc.). The remaining line divisions are determined from the
        division nearest the keypoint at the other end of the line (specified by another :ref:`kesize`
        command or the :ref:`esize` command). Divisions are transferred to the lines during the mesh
        operation. If smart element sizing is being used ( :ref:`smrtsize` ), :ref:`kesize` specifications
        may be overridden (that is, a smaller element size may be used) to accommodate curvature and small
        features.

        This command is valid in any processor. The command is also valid for `rezoning
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_nlad/Hlp_G_ADVRZSMP.html>`_.
        """
        command = f"KESIZE,{npt},{size},{fact1},{fact2}"
        return self.run(command, **kwargs)



    def kmesh(self, np1: str = "", np2: str = "", ninc: str = "", **kwargs):
        r"""Generates nodes and point elements at keypoints.

        Mechanical APDL Command: `KMESH <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_KMESH.html>`_

        Parameters
        ----------
        np1 : str
            Mesh keypoints from ``NP1`` to ``NP2`` (defaults to ``NP1`` ) in steps of ``NINC`` (defaults to
            1). If ``NP1`` = ALL, ``NP2`` and ``NINC`` are ignored and all selected keypoints ( :ref:`ksel`
            ) are meshed. If ``NP1`` = P, graphical picking is enabled and all remaining command fields are
            ignored (valid only in the GUI). A component name may also be substituted for ``NP1``.

        np2 : str
            Mesh keypoints from ``NP1`` to ``NP2`` (defaults to ``NP1`` ) in steps of ``NINC`` (defaults to
            1). If ``NP1`` = ALL, ``NP2`` and ``NINC`` are ignored and all selected keypoints ( :ref:`ksel`
            ) are meshed. If ``NP1`` = P, graphical picking is enabled and all remaining command fields are
            ignored (valid only in the GUI). A component name may also be substituted for ``NP1``.

        ninc : str
            Mesh keypoints from ``NP1`` to ``NP2`` (defaults to ``NP1`` ) in steps of ``NINC`` (defaults to
            1). If ``NP1`` = ALL, ``NP2`` and ``NINC`` are ignored and all selected keypoints ( :ref:`ksel`
            ) are meshed. If ``NP1`` = P, graphical picking is enabled and all remaining command fields are
            ignored (valid only in the GUI). A component name may also be substituted for ``NP1``.

        Notes
        -----

        .. _KMESH_notes:

        Missing nodes required for the generated elements are created and assigned the lowest available
        numbers.
        """
        command = f"KMESH,{np1},{np2},{ninc}"
        return self.run(command, **kwargs)



    def krefine(self, np1: str = "", np2: str = "", ninc: str = "", level: str = "", depth: str = "", post: str = "", retain: str = "", **kwargs):
        r"""Refines the mesh around specified keypoints.

        Mechanical APDL Command: `KREFINE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_KREFINE.html>`_

        Parameters
        ----------
        np1 : str
            Keypoints ( ``NP1`` to ``NP2`` in increments of ``NINC`` ) around which the mesh is to be
            refined. ``NP2`` defaults to ``NP1``, and ``NINC`` defaults to 1. If ``NP1`` = ALL, ``NP2`` and
            ``NINC`` are ignored and all selected keypoints are used for refinement. If ``NP1`` = P,
            graphical picking is enabled and all remaining command fields are ignored (valid only in the
            GUI). A component name may also be substituted for ``NP1`` ( ``NP2`` and ``NINC`` are ignored).

        np2 : str
            Keypoints ( ``NP1`` to ``NP2`` in increments of ``NINC`` ) around which the mesh is to be
            refined. ``NP2`` defaults to ``NP1``, and ``NINC`` defaults to 1. If ``NP1`` = ALL, ``NP2`` and
            ``NINC`` are ignored and all selected keypoints are used for refinement. If ``NP1`` = P,
            graphical picking is enabled and all remaining command fields are ignored (valid only in the
            GUI). A component name may also be substituted for ``NP1`` ( ``NP2`` and ``NINC`` are ignored).

        ninc : str
            Keypoints ( ``NP1`` to ``NP2`` in increments of ``NINC`` ) around which the mesh is to be
            refined. ``NP2`` defaults to ``NP1``, and ``NINC`` defaults to 1. If ``NP1`` = ALL, ``NP2`` and
            ``NINC`` are ignored and all selected keypoints are used for refinement. If ``NP1`` = P,
            graphical picking is enabled and all remaining command fields are ignored (valid only in the
            GUI). A component name may also be substituted for ``NP1`` ( ``NP2`` and ``NINC`` are ignored).

        level : str
            Amount of refinement to be done. Specify the value of ``LEVEL`` as an integer from 1 to 5, where
            a value of 1 provides minimal refinement, and a value of 5 provides maximum refinement (defaults
            to 1).

        depth : str
            Depth of mesh refinement in terms of the number of elements outward from the indicated keypoints
            (defaults to 1).

        post : str
            Type of postprocessing to be done after element splitting, in order to improve element quality:

            * ``OFF`` - No postprocessing will be done.

            * ``SMOOTH`` - Smoothing will be done. Node locations may change.

            * ``CLEAN`` - Smoothing and cleanup will be done. Existing elements may be deleted, and node
              locations may change (default).

        retain : str
            Flag indicating whether quadrilateral elements must be retained in the refinement of an all-
            quadrilateral mesh. (Mechanical APDL ignores the ``RETAIN`` argument when you are refining anything other than a quadrilateral mesh.)

            * ``ON`` - The final mesh will be composed entirely of quadrilateral elements, regardless of the
              element quality (default).

            * ``OFF`` - The final mesh may include some triangular elements in order to maintain element quality
              and provide transitioning.

        Notes
        -----

        .. _KREFINE_notes:

        :ref:`krefine` performs local mesh refinement around the specified keypoints. By default, the
        indicated elements are split to create new elements with 1/2 the edge length of the original
        elements ( ``LEVEL`` = 1).

        :ref:`krefine` refines all area elements and tetrahedral volume elements that are adjacent to the
        specified keypoints. Any volume elements that are adjacent to the specified keypoints, but are not
        tetrahedra (for example, hexahedra, wedges, and pyramids), are not refined.

        You cannot use mesh refinement on a solid model that contains initial conditions at nodes (
        :ref:`ic` ), coupled nodes ( :ref:`cp` family of commands), constraint equations ( :ref:`ce` family
        of commands), or boundary conditions or loads applied directly to any of its nodes or elements. This
        applies to nodes and elements anywhere in the model, not just in the region where you want to
        request mesh refinement. See `Revising Your Model
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD8_6.html>`_   in the
        `Modeling and Meshing Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD14.html>`_ for additional
        restrictions on mesh refinement.

        This command is also valid for `rezoning
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_nlad/Hlp_G_ADVRZSMP.html>`_.
        """
        command = f"KREFINE,{np1},{np2},{ninc},{level},{depth},{post},{retain}"
        return self.run(command, **kwargs)



    def kscon(self, npt: str = "", delr: str = "", kctip: int | str = "", nthet: str = "", rrat: str = "", **kwargs):
        r"""Specifies a keypoint about which an area mesh will be skewed.

        Mechanical APDL Command: `KSCON <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_KSCON.html>`_

        Parameters
        ----------
        npt : str
            Keypoint number at concentration. If ``NPT`` = ALL, use all selected keypoints. If remaining
            fields are blank, remove concentration from this keypoint (if unmeshed). If ``NPT`` = P,
            graphical picking is enabled and all remaining command fields are ignored (valid only in the
            GUI). A component name may also be substituted for ``NPT``.

        delr : str
            Radius of first row of elements about keypoint.

        kctip : int or str
            Crack tip singularity key:

            * ``0`` - Do not skew midside nodes, if any, within the element.

            * ``1`` - Skew midside nodes of the first row of elements to the 1/4 point for crack tip
              singularity.

        nthet : str
            Number of elements in circumferential direction (defaults to approximately one per 45° (or one
            per 30°, if ``KCTIP`` = 1)).

        rrat : str
            Ratio of 2nd row element size to ``DELR`` (defaults to 0.75, or 0.5 if ``KCTIP`` = 1).

        Notes
        -----

        .. _KSCON_notes:

        Defines a concentration keypoint about which an area mesh will be skewed. Useful for modeling stress
        concentrations and crack tips. During meshing, elements are initially generated circumferentially
        about, and radially away, from the keypoint. Lines attached to the keypoint are given appropriate
        divisions and spacing ratios. Only one concentration keypoint per unmeshed area is allowed. Use
        :ref:`kscon`,STAT to list current status of concentration keypoints. The :ref:`kscon` command does
        not support 3D modeling.

        This command is also valid for `rezoning
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_nlad/Hlp_G_ADVRZSMP.html>`_.
        """
        command = f"KSCON,{npt},{delr},{kctip},{nthet},{rrat}"
        return self.run(command, **kwargs)



    def latt(self, mat: str = "", real: str = "", type_: str = "", kb: str = "", ke: str = "", secnum: str = "", **kwargs):
        r"""Associates element attributes with the selected, unmeshed lines.

        Mechanical APDL Command: `LATT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_LATT.html>`_

        Parameters
        ----------
        mat : str
            Material number, real constant set number, and type number to be associated with selected,
            unmeshed lines.

        real : str
            Material number, real constant set number, and type number to be associated with selected,
            unmeshed lines.

        type_ : str
            Material number, real constant set number, and type number to be associated with selected,
            unmeshed lines.

        kb : str
            Beginning and ending orientation keypoints to be associated with selected, unmeshed lines.
            Mechanical APDL uses the location of these keypoints to determine how to orient beam cross
            sections during beam meshing. Beam elements may be created along a line with a constant
            orientation by specifying only one orientation keypoint ( ``KB`` ), or a pre-twisted beam may be
            created by selecting different orientation keypoints at each end of the line ( ``KB`` and ``KE``
            ). (For a line bounded by two keypoints ( ``KP1`` and ``KP2`` ), the orientation vector at the
            beginning of the line extends from ``KP1`` to ``KB``, and the orientation vector at the end of
            the line extends from ``KP2`` to ``KE``. The orientation vectors are used to compute the
            orientation nodes of the elements.)

        ke : str
            Beginning and ending orientation keypoints to be associated with selected, unmeshed lines.
            Mechanical APDL uses the location of these keypoints to determine how to orient beam cross
            sections during beam meshing. Beam elements may be created along a line with a constant
            orientation by specifying only one orientation keypoint ( ``KB`` ), or a pre-twisted beam may be
            created by selecting different orientation keypoints at each end of the line ( ``KB`` and ``KE``
            ). (For a line bounded by two keypoints ( ``KP1`` and ``KP2`` ), the orientation vector at the
            beginning of the line extends from ``KP1`` to ``KB``, and the orientation vector at the end of
            the line extends from ``KP2`` to ``KE``. The orientation vectors are used to compute the
            orientation nodes of the elements.)

        secnum : str
            Section identifier to be associated with selected, unmeshed lines. For details, see the
            description of the :ref:`sectype` and :ref:`secnum` commands.

        Notes
        -----

        .. _LATT_notes:

        The element attributes specified by the :ref:`latt` command will be used when the lines are meshed.

        Lines subsequently generated from the lines will also have the attributes specified by ``MAT``,
        ``REAL``, ``TYPE``, and ``SECNUM``. If a line does not have these attributes associated with it (by
        this command) at the time it is meshed, the attributes are obtained from the then current
        :ref:`mat`, :ref:`real`, :ref:`type`, and :ref:`secnum` command settings.

        In contrast, the values specified by ``KB`` and ``KE`` apply only to the selected lines; t
        hat is, lines subsequently generated from these lines will not share these attributes. Similarly, if
        a line does not have ``KB`` and ``KE`` attributes associated with it via the :ref:`latt` command at
        the time it is meshed, Mechanical APDL cannot obtain the attributes from elsewhere. See the
        discussion on
        beam meshing in `Meshing Your Solid Model
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD7_8.html>`_ in the
        `Modeling and Meshing Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD14.html>`_
        for more information.

        Reissue the :ref:`latt` command (before lines are meshed) to change the attributes. A zero (or
        blank) argument removes the corresponding association. If any of the arguments are defined as -1,
        then that value will be left unchanged in the selected set.

        In some cases, Mechanical APDL can proceed with a line meshing operation even when no logical
        element type
        has been assigned via :ref:`latt`, ``TYPE`` or :ref:`type`. See `Meshing Your Solid Model
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD7_8.html>`_ in the
        `Modeling and Meshing Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD14.html>`_
        for more information about setting element attributes.
        """
        command = f"LATT,{mat},{real},{type_},,{kb},{ke},{secnum}"
        return self.run(command, **kwargs)



    def lccat(self, nl1: str = "", nl2: str = "", **kwargs):
        r"""Concatenates multiple lines into one line for mapped meshing.

        Mechanical APDL Command: `LCCAT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_LCCAT.html>`_

        Parameters
        ----------
        nl1 : str
            Lines to be concatenated. If ``NL1`` = ALL, ``NL2`` is ignored and all selected lines (
            :ref:`lsel` ) are concatenated. If ``NL1`` = P, graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI). A component name may also be substituted for
            ``NL1`` ( ``NL2`` is ignored).

        nl2 : str
            Lines to be concatenated. If ``NL1`` = ALL, ``NL2`` is ignored and all selected lines (
            :ref:`lsel` ) are concatenated. If ``NL1`` = P, graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI). A component name may also be substituted for
            ``NL1`` ( ``NL2`` is ignored).

        Notes
        -----

        .. _LCCAT_notes:

        Concatenates multiple, adjacent lines (the input lines) into one line (the output line) in
        preparation for mapped meshing. An area that contains too many lines for mapped meshing can still be
        mapped meshed if some of the lines in that area are first concatenated (see `Meshing Your Solid
        Model <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD7_8.html>`_ in the
        `Modeling and Meshing Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD14.html>`_ for details on
        mapped meshing restrictions).

        :ref:`lccat` is meant to be used solely for meshing and cannot be used for any other purposes.
        Specifically, (a) the output line and any areas that have the output line on their line list (
        :ref:`alist` ) cannot be used as input to any other solid modeling operation (not even another
        :ref:`lccat` command); and (b) the output line cannot accept solid model boundary conditions (
        :ref:`dl`, :ref:`sfl` ).

        The output line will take on the element divisions of the input lines and will not accept element
        divisions that are directly assigned ( :ref:`lesize` ). The output line from the :ref:`lccat`
        operation will be coincident with the input lines and the input lines will be retained. Consider the
        :ref:`lcomb` command instead of :ref:`lccat` if you wish to delete the input lines and if the lines
        to be combined have similar slopes at the common keypoint(s). When an :ref:`lccat` command is
        issued, area line lists ( :ref:`alist` ) that contain all of the input lines will be updated so that
        the area line lists refer to the output line instead of the input lines. Deletion of the output line
        ( :ref:`ldele` ) effectively reverses the :ref:`lccat` operation and restores area line lists to
        their original condition.

        You can use the :ref:`lsel` command to select lines that were created by concatenation, and then
        follow it with an :ref:`ldele`,ALL command to delete them. Also see `Meshing Your Solid Model
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD7_8.html>`_   in the
        `Modeling and Meshing Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD14.html>`_ for a discussion
        on how to easily select and delete concatenated lines in one step.
        """
        command = f"LCCAT,{nl1},{nl2}"
        return self.run(command, **kwargs)



    def lclear(self, nl1: str = "", nl2: str = "", ninc: str = "", **kwargs):
        r"""Deletes nodes and line elements associated with selected lines.

        Mechanical APDL Command: `LCLEAR <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_LCLEAR.html>`_

        Parameters
        ----------
        nl1 : str
            Delete mesh for lines ``NL1`` to ``NL2`` (defaults to ``NL1`` ) in steps of ``NINC`` (defaults
            to 1). If ``NL1`` = ALL, ``NL2`` and ``NINC`` are ignored and the mesh for all selected lines (
            :ref:`lsel` ) is deleted. If ``NL1`` = P, graphical picking is enabled and all remaining command
            fields are ignored (valid only in the GUI). A component name may also be substituted for ``NL1``
            ( ``NL2`` and ``NINC`` are ignored).

        nl2 : str
            Delete mesh for lines ``NL1`` to ``NL2`` (defaults to ``NL1`` ) in steps of ``NINC`` (defaults
            to 1). If ``NL1`` = ALL, ``NL2`` and ``NINC`` are ignored and the mesh for all selected lines (
            :ref:`lsel` ) is deleted. If ``NL1`` = P, graphical picking is enabled and all remaining command
            fields are ignored (valid only in the GUI). A component name may also be substituted for ``NL1``
            ( ``NL2`` and ``NINC`` are ignored).

        ninc : str
            Delete mesh for lines ``NL1`` to ``NL2`` (defaults to ``NL1`` ) in steps of ``NINC`` (defaults
            to 1). If ``NL1`` = ALL, ``NL2`` and ``NINC`` are ignored and the mesh for all selected lines (
            :ref:`lsel` ) is deleted. If ``NL1`` = P, graphical picking is enabled and all remaining command
            fields are ignored (valid only in the GUI). A component name may also be substituted for ``NL1``
            ( ``NL2`` and ``NINC`` are ignored).

        Notes
        -----

        .. _LCLEAR_notes:

        Deletes all nodes and line elements associated with selected lines (regardless of whether the nodes
        or elements are selected). Nodes shared by adjacent meshed lines and nodes associated with non-line
        elements will not be deleted. Attributes assigned as a result of :ref:`latt` are maintained. In the
        program's response to the command, if a line or keypoint is tallied as "cleared," it means either
        its node or element reference was deleted.
        """
        command = f"LCLEAR,{nl1},{nl2},{ninc}"
        return self.run(command, **kwargs)



    def lesize(self, nl1: str = "", size: str = "", angsiz: str = "", ndiv: str = "", space: str = "", kforc: int | str = "", layer1: str = "", layer2: str = "", kyndiv: str = "", **kwargs):
        r"""Specifies the divisions and spacing ratio on unmeshed lines.

        Mechanical APDL Command: `LESIZE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_LESIZE.html>`_

        Parameters
        ----------
        nl1 : str
            Number of the line to be modified. If ALL, modify all selected lines ( :ref:`lsel` ). If ``NL1``
            = P, graphical picking is enabled and all remaining command fields are ignored (valid only in
            the GUI). A component name may also be substituted for ``NL1``.

        size : str
            If ``NDIV`` is blank, ``SIZE`` is the division (element edge) length. The number of divisions is
            automatically calculated from the line length (rounded upward to next integer). If ``SIZE`` is
            zero (or blank), use ``ANGSIZ`` or ``NDIV``.

        angsiz : str
            The division arc (in degrees) spanned by the element edge (except for straight lines, which
            always result in one division). The number of divisions is automatically calculated from the
            line length (rounded upward to next integer).

        ndiv : str
            If positive, ``NDIV`` is the number of element divisions per line. If -1 (and ``KFORC`` = 1),
            ``NDIV`` is assumed to be zero element divisions per line. TARGE169 with a rigid specification
            ignores ``NDIV`` and will always mesh with one element division.

        space : str
            Spacing ratio. If positive, nominal ratio of last division size to first division size (if >
            1.0, sizes increase, if < 1.0, sizes decrease). If negative, \| ``SPACE`` \| is nominal ratio of
            center division(s) size to end divisions size. Ratio defaults to 1.0 (uniform spacing). For
            layer-meshing, a value of 1.0 normally is used. If ``SPACE`` = FREE, ratio is determined by
            other considerations

        kforc : int or str
            ``KFORC`` 0-3 are used only with ``NL1`` = ALL. Specifies which selected lines are to be modified.

            * ``0`` - Modify only selected lines having undefined (zero) divisions.

            * ``1`` - Modify all selected lines.

            * ``2`` - Modify only selected lines having fewer divisions (including zero) than specified with
              this command.

            * ``3`` - Modify only selected lines having more divisions than specified with this command.

            * ``4`` - Modify only nonzero settings for ``SIZE``, ``ANGSIZ``, ``NDIV``, ``SPACE``, ``LAYER1``,
              and ``LAYER2``. If ``KFORC`` = 4, blank or 0 settings remain unchanged.

        layer1 : str
            Layer-meshing control parameter. Distance which defines the thickness of the inner mesh layer,
            ``LAYER1``. Elements in this layer are uniformly-sized with edge lengths equal to the specified
            element size for the line (either through ``SIZE`` or line-length/ ``NDIV`` ). A positive value
            for ``LAYER1`` is interpreted as an absolute length, while a negative value in interpreted as a
            multiplier on the specified element size for the line. As a general rule, the resulting
            thickness of the inner mesh layer should be greater than or equal to the specified element size
            for the line. If ``LAYER1`` = OFF, layer-meshing control settings are cleared for the selected
            lines. The default value is 0.0

        layer2 : str
            Layer-meshing control parameter. Distance which defines the thickness of the outer mesh layer,
            ``LAYER2``. Elements in this layer transition in size from those in ``LAYER1`` to the global
            element size. A positive value of ``LAYER2`` is interpreted as an absolute length, while a
            negative value is interpreted as a mesh transition factor. A value of ``LAYER2`` = -2 would
            indicate that elements should approximately double in size as the mesh progresses normal to
            ``LAYER1``. The default value is 0.0.

        kyndiv : str
            0, No, and Off means that SmartSizing cannot override specified divisions and spacing ratios.
            Mapped mesh fails if divisions do not match. This defines the specification as hard.

            1, Yes, and On means that SmartSizing can override specified divisions and spacing ratios for
            curvature or proximity. Mapped meshing can override divisions to obtain required matching
            divisions. This defines the specification as soft.

        Notes
        -----

        .. _LESIZE_notes:

        Defines the number of divisions and the spacing ratio on selected lines. Lines with previously
        specified divisions may also be changed.

        This command is also valid for `rezoning
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_nlad/Hlp_G_ADVRZSMP.html>`_.
        """
        command = f"LESIZE,{nl1},{size},{angsiz},{ndiv},{space},{kforc},{layer1},{layer2},{kyndiv}"
        return self.run(command, **kwargs)



    def lmesh(self, nl1: str = "", nl2: str = "", ninc: str = "", **kwargs):
        r"""Generates nodes and line elements along lines.

        Mechanical APDL Command: `LMESH <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_LMESH.html>`_

        Parameters
        ----------
        nl1 : str
            Mesh lines from ``NL1`` to ``NL2`` (defaults to ``NL1`` ) in steps of ``NINC`` (defaults to 1).
            If ``NL1`` = ALL, ``NL2`` and ``NINC`` are ignored and all selected lines ( :ref:`lsel` ) are
            meshed. If ``NL1`` = P, graphical picking is enabled and all remaining command fields are
            ignored (valid only in the GUI). A component name may also be substituted for ``NL1`` ( ``NL2``
            and ``NINC`` are ignored).

        nl2 : str
            Mesh lines from ``NL1`` to ``NL2`` (defaults to ``NL1`` ) in steps of ``NINC`` (defaults to 1).
            If ``NL1`` = ALL, ``NL2`` and ``NINC`` are ignored and all selected lines ( :ref:`lsel` ) are
            meshed. If ``NL1`` = P, graphical picking is enabled and all remaining command fields are
            ignored (valid only in the GUI). A component name may also be substituted for ``NL1`` ( ``NL2``
            and ``NINC`` are ignored).

        ninc : str
            Mesh lines from ``NL1`` to ``NL2`` (defaults to ``NL1`` ) in steps of ``NINC`` (defaults to 1).
            If ``NL1`` = ALL, ``NL2`` and ``NINC`` are ignored and all selected lines ( :ref:`lsel` ) are
            meshed. If ``NL1`` = P, graphical picking is enabled and all remaining command fields are
            ignored (valid only in the GUI). A component name may also be substituted for ``NL1`` ( ``NL2``
            and ``NINC`` are ignored).

        Notes
        -----

        .. _LMESH_notes:

        Generates nodes and line elements along lines. Missing nodes required for the generated elements are
        created and assigned the lowest available numbers.
        """
        command = f"LMESH,{nl1},{nl2},{ninc}"
        return self.run(command, **kwargs)



    def lrefine(self, nl1: str = "", nl2: str = "", ninc: str = "", level: str = "", depth: str = "", post: str = "", retain: str = "", **kwargs):
        r"""Refines the mesh around specified lines.

        Mechanical APDL Command: `LREFINE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_LREFINE.html>`_

        Parameters
        ----------
        nl1 : str
            Lines ( ``NL1`` to ``NL2`` in increments of ``NINC`` ) around which the mesh is to be refined.
            ``NL2`` defaults to ``NL1``, and ``NINC`` defaults to 1. If ``NL1`` = ALL, ``NL2`` and ``NINC``
            are ignored and all selected lines are used for refinement. If ``NL1`` = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in the GUI). A component name
            may also be substituted for ``NL1`` ( ``NL2`` and ``NINC`` are ignored).

        nl2 : str
            Lines ( ``NL1`` to ``NL2`` in increments of ``NINC`` ) around which the mesh is to be refined.
            ``NL2`` defaults to ``NL1``, and ``NINC`` defaults to 1. If ``NL1`` = ALL, ``NL2`` and ``NINC``
            are ignored and all selected lines are used for refinement. If ``NL1`` = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in the GUI). A component name
            may also be substituted for ``NL1`` ( ``NL2`` and ``NINC`` are ignored).

        ninc : str
            Lines ( ``NL1`` to ``NL2`` in increments of ``NINC`` ) around which the mesh is to be refined.
            ``NL2`` defaults to ``NL1``, and ``NINC`` defaults to 1. If ``NL1`` = ALL, ``NL2`` and ``NINC``
            are ignored and all selected lines are used for refinement. If ``NL1`` = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in the GUI). A component name
            may also be substituted for ``NL1`` ( ``NL2`` and ``NINC`` are ignored).

        level : str
            Amount of refinement to be done. Specify the value of ``LEVEL`` as an integer from 1 to 5, where
            a value of 1 provides minimal refinement, and a value of 5 provides maximum refinement (defaults
            to 1).

        depth : str
            Depth of mesh refinement in terms of the number of elements outward from the indicated lines
            (defaults to 1).

        post : str
            Type of postprocessing to be done after element splitting, in order to improve element quality:

            * ``OFF`` - No postprocessing will be done.

            * ``SMOOTH`` - Smoothing will be done. Node locations may change.

            * ``CLEAN`` - Smoothing and cleanup will be done. Existing elements may be deleted, and node
              locations may change (default).

        retain : str
            Flag indicating whether quadrilateral elements must be retained in the refinement of an all-
            quadrilateral mesh. (Mechanical APDL ignores the ``RETAIN`` argument when you are refining anything other than a quadrilateral mesh.)

            * ``ON`` - The final mesh will be composed entirely of quadrilateral elements, regardless of the
              element quality (default).

            * ``OFF`` - The final mesh may include some triangular elements in order to maintain element quality
              and provide transitioning.

        Notes
        -----

        .. _LREFINE_notes:

        :ref:`lrefine` performs local mesh refinement around the specified lines. By default, the indicated
        elements are split to create new elements with 1/2 the edge length of the original elements (
        ``LEVEL`` = 1).

        :ref:`lrefine` refines all area elements and tetrahedral volume elements that are adjacent to the
        specified lines. Any volume elements that are adjacent to the specified lines, but are not
        tetrahedra (for example, hexahedra, wedges, and pyramids), are not refined.

        You cannot use mesh refinement on a solid model that contains initial conditions at nodes (
        :ref:`ic` ), coupled nodes ( :ref:`cp` family of commands), constraint equations ( :ref:`ce` family
        of commands), or boundary conditions or loads applied directly to any of its nodes or elements. This
        applies to nodes and elements anywhere in the model, not just in the region where you want to
        request mesh refinement. For additional restrictions on mesh refinement, see `Revising Your Model
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD8_6.html>`_ in the
        `Modeling and Meshing Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD14.html>`_.

        This command is also valid for `rezoning
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_nlad/Hlp_G_ADVRZSMP.html>`_.
        """
        command = f"LREFINE,{nl1},{nl2},{ninc},{level},{depth},{post},{retain}"
        return self.run(command, **kwargs)



    def mat(self, mat: str = "", **kwargs):
        r"""Sets the element material attribute pointer.

        Mechanical APDL Command: `MAT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MAT.html>`_

        Parameters
        ----------
        mat : str
            Assign this material number to subsequently defined elements (defaults to 1).

        Notes
        -----

        .. _MAT_notes:

        Identifies the material number to be assigned to subsequently defined elements. This number refers
        to the material number ( ``MAT`` ) defined with the material properties ( :ref:`mp` ). Material
        numbers may be displayed ( :ref:`pnum` ).
        """
        command = f"MAT,{mat}"
        return self.run(command, **kwargs)



    def mcheck(self, lab: str = "", **kwargs):
        r"""Checks mesh connectivity.

        Mechanical APDL Command: `MCHECK <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MCHECK.html>`_

        Parameters
        ----------
        lab : str
            Operation:

            * ``ESEL`` - Unselects the valid elements.

        Notes
        -----

        .. _MCHECK_notes:

        Wherever two area or volume elements share a common face, :ref:`mcheck` verifies that the way the
        elements are connected to the face is consistent with their relative normals or integrated volumes.
        (This may detect folds or otherwise overlapping elements.)

        :ref:`mcheck` verifies that the element exterior faces form simply-connected closed surfaces. (This
        may detect unintended cracks in a mesh.)

        :ref:`mcheck` warns if the number of element facets in a 2D loop or 3D shell is not greater than a
        computed limit. This limit is the smaller of either three times the number of faces on one element,
        or one-tenth the total number of element faces in the model. (This may detect holes in the middle of
        a mesh.)

        The :ref:`mcheck` command will perform a number of validity checks on the selected elements,
        including: **Normal check:** Wherever two area elements share a common edge, :ref:`mcheck` verifies
        that the
        ordering of the nodes on each element is consistent with their relative normals.

        **Volume check:** Wherever two volume elements share a common face, :ref:`mcheck` verifies that the
        sign of the integrated volume of each element is consistent.

        **Closed surface check:**  :ref:`mcheck` verifies that the element exterior faces form simply-
        connected closed surfaces (this may detect unintended cracks in a mesh).

        **Check for holes in the mesh:**  :ref:`mcheck` warns if the number of element faces surrounding an
        interior void in the mesh is small enough to suggest one or more accidentally omitted elements,
        rather than a deliberately formed hole. For this test, the number of faces around the void is
        compared to the smaller of a) three times the number of faces on one element, or b) one-tenth the
        total number of element faces in the model.

        """
        command = f"MCHECK,{lab}"
        return self.run(command, **kwargs)



    def modmsh(self, lab: str = "", **kwargs):
        r"""Controls the relationship of the solid model and the FE model.

        Mechanical APDL Command: `MODMSH <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MODMSH.html>`_

        Parameters
        ----------
        lab : str
            Relationship key:

            * ``STAT`` - Gives status of command (default). This applies only to the CHECK option (no status is
              provided for the DETACH option).

            * ``NOCHECK`` - Deactivates the checking of the solid model and the finite element model. Allows
              elements and nodes generated with the mesh commands to be modified directly ( :ref:`emodif`,
              :ref:`nmodif`, :ref:`edele`, :ref:`ndele`, etc.). Also deactivates solid model hierarchical checking
              so that areas attached to volumes may be deleted etc.

            * ``CHECK`` - Reactivates future checking of the solid model.

            * ``DETACH`` - Releases all associativity between the current solid model and finite element model.
              Mechanical APDL deletes any element attributes that were assigned to the affected solid model entities
              through default attributes (that is, through the :ref:`type`, :ref:`real`, :ref:`mat`,
              :ref:`secnum`, and :ref:`esys` command settings and a subsequent meshing operation). However,
              attributes that were assigned directly to the solid model entities (via the :ref:`katt`,
              :ref:`latt`, :ref:`aatt`, and :ref:`vatt` commands) are not deleted.

        Notes
        -----

        .. _MODMSH_notes:

        Affects the relationship of the solid model (keypoints, lines, areas, volumes) and the finite
        element model (nodes, elements, and boundary conditions).

        Specify ``Lab`` = NOCHECK carefully. By deactivating checking, the solid model database can be
        corrupted by subsequent operations.

        After specifying ``Lab`` = DETACH, it is no longer possible to select or define finite element model
        items in terms of the detached solid model or to clear the mesh.
        """
        command = f"MODMSH,{lab}"
        return self.run(command, **kwargs)



    def mopt(self, lab: str = "", value: str = "", **kwargs):
        r"""Specifies meshing options.

        Mechanical APDL Command: `MOPT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MOPT.html>`_

        Parameters
        ----------
        lab : str
            Meshing option to be specified (determines the meaning of ``Value`` ):

            * ``AORDER`` - Mesh by ascending area size order. Set ``Value`` to ON to mesh smaller areas first.
              Using this results in finer meshes in critical areas for volume meshes; this can be used for cases
              where :ref:`smrtsize` does not mesh as needed. Default is OFF.

            * ``EXPND`` - Area mesh expansion (or contraction) option. (This option is the same as
              :ref:`smrtsize`,,,EXPND.) This option is used to size internal elements in an area based on the size
              of the elements on the area's boundaries.

              ``Value`` is the expansion (or contraction) factor. For example, issuing :ref:`mopt`,EXPND,2 before
              meshing an area will allow a mesh with elements that are approximately twice as large in the
              interior of an area as they are on the boundary. If ``Value`` is less than 1, a mesh with smaller
              elements on the interior of the area will be allowed. ``Value`` for this option should be greater
              than 0.5 but less than 4.

              ``Value`` defaults to 1, which does not allow expansion or contraction of internal element sizes
              (except when using :ref:`aesize` sizing). If ``Value`` = 0, the default value of 1 will be used. The
              actual size of the internal elements will also depend on the TRANS option (or upon :ref:`aesize` or
              :ref:`esize` sizing, if used).

            * ``TETEXPND`` - Tet-mesh expansion (or contraction) option. This option is used to size internal
              elements in a volume based on the size of the elements on the volume's boundaries.

              ``Value`` is the expansion (or contraction) factor. For example, issuing :ref:`mopt`,TETEXPND,2
              before meshing a volume will allow a mesh with elements that are approximately twice as large in the
              interior of the volume as they are on the boundary. If ``Value`` is less than 1, a mesh with smaller
              elements on the interior of the volume will be allowed. ``Value`` for this option should be greater
              than 0.1 but less than 3.

              ``Value`` defaults to 1, which does not allow expansion or contraction of internal element sizes. If
              ``Value`` = 0, the default value of 1 will be used. If ``Value`` is greater than 2, mesher
              robustness may be affected.

              The TETEXPND option is supported for both the :ref:`vmesh` and :ref:`fvmesh` commands. Tet-mesh
              expansion is the only mesh control supported by :ref:`fvmesh`.

            * ``TRANS`` - Mesh-transition option. Controls how rapidly elements are permitted to change in size
              from the boundary to the interior of an area. (This option performs the same operation as
              :ref:`smrtsize`,,,,TRANS.)

              ``Value`` is the transitioning factor. ``Value`` defaults to 2.0, which permits elements to
              approximately double in size as they approach the interior of the area. (If ``Value`` = 0, the
              default value of 2 will be used.) ``Value`` must be greater than 1 and, for best results, should be
              less than 4. The actual size of the internal elements will also depend on the EXPND option (or upon
              :ref:`aesize` or :ref:`esize` sizing, if used).

              For a quad mesh with any element size, this option has no effect, as the program strictly respects
              any face size to ensure the most uniform quad mesh possible. To obtain a graded mesh using this
              option, apply :ref:`lesize` to the lines of the desired face.

            * ``AMESH`` - Triangle surface-meshing option. Valid inputs for ``Value`` are:

              * ``DEFAULT`` - Allows the program to choose which triangle mesher to use. In most cases, the
                program chooses the main triangle mesher, which is the Riemann space mesher. If the chosen mesher
                fails for any reason, the program invokes the alternate mesher and retries the meshing operation.

              * ``MAIN`` - The program uses the main triangle mesher (Riemann space mesher), and it does not
                invoke an alternate mesher if the main mesher fails. The Riemann space mesher is well suited for
                most surfaces.

              * ``ALTERNATE`` - The program uses the first alternate triangle mesher (3D tri-mesher), and it does
                not invoke another mesher if this mesher fails. This option is not recommended due to speed
                considerations. However, for surfaces with degeneracies in parametric space, this mesher often
                provides the best results.

              * ``ALT2`` - The program uses the second alternate triangle mesher (2D parametric space mesher), and
                it does not invoke another mesher if this mesher fails. This option is not recommended for use on
                surfaces with degeneracies (spheres, cones, etc.) or poorly parameterized surfaces because poor
                meshes may result.

            * ``QMESH`` - Quadrilateral surface meshing option. (Quadrilateral surface meshes will differ based on which
              triangle surface mesher is selected. This is true because all free quadrilateral meshing algorithms
              use a triangle mesh as a starting point.) Valid inputs for ``Value`` are:

              * ``DEFAULT`` - Let the program choose which quadrilateral mesher to use. In most cases, the program
                will choose the main quadrilateral mesher, which is the Q-Morph (quad-morphing) mesher. For very
                coarse meshes, the program may choose the alternate quadrilateral mesher instead. In most cases, the
                Q-Morph mesher results in higher quality elements. If either mesher fails for any reason, the
                program invokes the other mesher and retries the meshing operation. (Default.)

              * ``MAIN`` - The program uses the main quadrilateral mesher (Q-Morph mesher), and it does not invoke
                the alternate mesher if the main mesher fails.

              * ``ALTERNATE`` - The program uses the alternate quadrilateral mesher, and it does not invoke the
                Q-Morph mesher if the alternate mesher fails. To use the alternate quadrilateral mesher, you must
                also select :ref:`mopt`,AMESH,ALTERNATE or :ref:`mopt`,AMESH,ALT2.

            * ``VMESH`` - Tetrahedral element meshing option. Valid inputs for ``Value`` are:

              * ``DEFAULT`` - Let the program choose which tetrahedra mesher to use.

              * ``MAIN`` - Use the main tetrahedra mesher (Delaunay technique mesher). (GHS3D meshing technology
                by P. L. George, INRIA, France.) For most models, this mesher is significantly faster than the
                alternate mesher.

              * ``ALTERNATE`` - Use the alternate tetrahedra mesher (advancing front mesher). This mesher does not
                support the generation of a tetrahedral volume mesh from facets ( :ref:`fvmesh` ). If this mesher is
                selected and you issue the :ref:`fvmesh` command, the program uses the main tetrahedra mesher to
                create the mesh from facets and issues a warning message to notify you.

            * ``SPLIT`` - Quad splitting option for non-mapped meshing. If ``Value`` = 1, ON, or ERR,
              quadrilateral elements in violation of shape error limits are split into triangles (default). If
              ``Value`` = 2 or WARN, quadrilateral elements in violation of either shape error or warning limits
              are split into triangles. If ``Value`` = OFF, splitting does not occur, regardless of element
              quality.

            * ``LSMO`` - Line smoothing option. ``Value`` can be ON or OFF. If ``Value`` = ON, smoothing of
              nodes on area boundaries is performed during smoothing step of meshing. During smoothing, node
              locations are adjusted to achieve a better mesh. If ``Value`` = OFF (default), no smoothing takes
              place at area boundaries.

            * ``CLEAR`` - This option affects the element and node numbering after clearing a mesh. If ``Value``
              = ON (default), the starting node and element numbers will be the lowest available number after the
              nodes and elements are cleared. If ``Value`` = OFF, the starting node and element numbers are not
              reset after the clear operation.

            * ``PYRA`` - Transitional pyramid elements option. ``Value`` can be ON or OFF. If ``Value`` = ON
              (default), the program automatically creates transitional pyramid elements, when possible. Pyramids
              may be created at the interface of tetrahedral and hexahedral elements, or directly from
              quadrilateral elements. For pyramids to be created, you must also issue the command
              :ref:`mshape`,1,3D (degenerate 3D elements). If ``Value`` = OFF, the program does not create
              transitional pyramid elements.

            * ``TIMP`` - Identifies the level of tetrahedra improvement to be performed when the next free volume meshing
              operation is initiated ( :ref:`vmesh`, :ref:`fvmesh` ). (For levels 2-5, improvement occurs primarily through the use of face swapping and node smoothing techniques.) Valid inputs for ``Value`` are:

              * ``0`` - Turn off tetrahedra improvement. Although this value can lead to faster tetrahedral mesh
                creation, it is not recommended because it often leads to poorly shaped elements and mesh failures.

              * ``1`` - Do the minimal amount of tetrahedra improvement. (Default.) This option is supported by
                the main tetrahedra mesher only ( :ref:`mopt`,VMESH,MAIN). If the alternate tetrahedra mesher (
                :ref:`mopt`,VMESH,ALTERNATE) is invoked with this setting, the program automatically performs
                tetrahedra improvement at level 3 instead ( :ref:`mopt`,TIMP,3).

              * ``2`` - Perform the least amount of swapping/smoothing. No improvement occurs if all tetrahedral
                elements are within acceptable limits.

              * ``3`` - Perform an intermediate amount of swapping/smoothing. Some improvement is always done.

              * ``4`` - Perform the greatest amount of swapping/smoothing. Meshing takes longer with this level of
                improvement, but usually results in a better mesh.

              * ``5`` - Perform the greatest amount of swapping/smoothing, plus additional improvement techniques.
                This level of improvement usually produces results that are similar to those at level 4, except for
                very poor meshes.

              * ``6`` - For linear tetrahedral meshes, this value provides the same level of improvement as
                :ref:`mopt`,TIMP,5. For quadratic tetrahedral meshes, this value provides an additional pass of
                cleanup. This value is supported for both the main ( :ref:`mopt`,VMESH,MAIN) and alternate (
                :ref:`mopt`,VMESH,ALTERNATE) tetrahedra meshers.

            * ``STAT`` - Display status of :ref:`mopt` settings. ``Value`` is ignored.

            * ``DEFA`` - Set all :ref:`mopt` options to default values. ``Value`` is ignored.

        value : str
            Value, as described for each different ``Lab`` above.

        Notes
        -----

        .. _MOPT_notes:

        See the `Modeling and Meshing Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD14.html>`_ for more
        information on the :ref:`mopt` command and its options.

        This command is also valid for `rezoning
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_nlad/Hlp_G_ADVRZSMP.html>`_.
        """
        command = f"MOPT,{lab},{value}"
        return self.run(command, **kwargs)



    def mshape(self, key: int | str = "", dimension: str = "", **kwargs):
        r"""For elements that support multiple shapes, specifies the element shape to be used for meshing.

        Mechanical APDL Command: `MSHAPE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MSHAPE.html>`_

        Parameters
        ----------
        key : int or str
            Key indicating the element shape to be used:

            * ``0`` - Mesh with quadrilateral-shaped elements when ``Dimension`` = 2D mesh with hexahedral-
              shaped elements when ``Dimension`` = 3D.

            * ``1`` - Mesh with triangle-shaped elements when ``Dimension`` = 2D mesh with tetrahedral-shaped
              elements when ``Dimension`` = 3D.

        dimension : str
            Specifies the dimension of the model to be meshed:

            * ``2D`` - 2D model (area mesh).

            * ``3D`` - 3D model (volume mesh).

        Notes
        -----

        .. _MSHAPE_notes:

        If no value is specified for ``Dimension`` the value of ``KEY`` determines the element shape that
        will be used for both 2D and 3D meshing. In other words, if you specify :ref:`mshape`,0,
        quadrilateral-shaped and hexahedral-shaped elements will be used. If you specify :ref:`mshape`,1,
        triangle-shaped and tetrahedral-shaped elements will be used.

        This command is also valid for `rezoning
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_nlad/Hlp_G_ADVRZSMP.html>`_.
        """
        command = f"MSHAPE,{key},{dimension}"
        return self.run(command, **kwargs)



    def mshcopy(self, keyla: str = "", laptrn: str = "", lacopy: str = "", kcn: str = "", dx: str = "", dy: str = "", dz: str = "", tol: str = "", low: str = "", high: str = "", **kwargs):
        r"""Simplifies the generation of meshes that have matching node element patterns on two different line
        groups (in 2D) or area groups (3D).

        Mechanical APDL Command: `MSHCOPY <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MSHCOPY.html>`_

        Parameters
        ----------
        keyla : str
            Copy line mesh (default) if LINE, 0 or 1. Copy area mesh if AREA, or 2.

        laptrn : str
            Meshed line/area to be copied, or a component name containing a list. If ``LAPTRN`` = P,
            graphical picking is enabled (valid only in the GUI).

        lacopy : str
            Unmeshed line/area to get copied mesh, or a component name containing a list. If ``LACOPY`` = P,
            graphical picking is enabled (valid only in the GUI).

        kcn : str
            In coordinate system ``KCN``, ``LAPTRN`` + ``DX``  ``DY``  ``DZ`` = ``LACOPY``.

        dx : str
            Node location increments in the active coordinate system (DR, Dθ, DZ for cylindrical, DR, Dθ, DΦ
            for spherical or toroidal).

        dy : str
            Node location increments in the active coordinate system (DR, Dθ, DZ for cylindrical, DR, Dθ, DΦ
            for spherical or toroidal).

        dz : str
            Node location increments in the active coordinate system (DR, Dθ, DZ for cylindrical, DR, Dθ, DΦ
            for spherical or toroidal).

        tol : str
            Tolerance. Defaults to 1.e--4.

        low : str
            Name of low node component to be defined (optional).

        high : str
            Name of high node component to be defined (optional).

        Notes
        -----

        .. _MSHCOPY_notes:

        Matching meshes are used for rotational (cyclic) symmetry, or for contact analysis using coupling or
        node-to-node gap elements. See `Using CPCYC and MSHCOPY Commands
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD7_8.html#>`_   in
        the `Modeling and Meshing Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD14.html>`_ for more
        information.
        """
        command = f"MSHCOPY,{keyla},{laptrn},{lacopy},{kcn},{dx},{dy},{dz},{tol},{low},{high}"
        return self.run(command, **kwargs)



    def mshkey(self, key: int | str = "", **kwargs):
        r"""Specifies whether free meshing or mapped meshing should be used to mesh a model.

        Mechanical APDL Command: `MSHKEY <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MSHKEY.html>`_

        Parameters
        ----------
        key : int or str
            Key indicating the type of meshing to be used:

            * ``0`` - Use free meshing (the default).

            * ``1`` - Use mapped meshing.

            * ``2`` - Use mapped meshing if possible; otherwise, use free meshing. If you specify
              :ref:`mshkey`,2, SmartSizing will be inactive even while free meshing non-map-meshable areas.

        Notes
        -----

        .. _MSHKEY_notes:

        This command is also valid for `rezoning
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_nlad/Hlp_G_ADVRZSMP.html>`_.
        """
        command = f"MSHKEY,{key}"
        return self.run(command, **kwargs)



    def mshmid(self, key: int | str = "", **kwargs):
        r"""Specifies placement of midside nodes.

        Mechanical APDL Command: `MSHMID <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MSHMID.html>`_

        Parameters
        ----------
        key : int or str
            Key indicating placement of midside nodes:

            * ``0`` - Midside nodes (if any) of elements on a region boundary follow the curvature of the
              boundary line or area (the default).

            * ``1`` - Place midside nodes of all elements so that element edges are straight. Allows coarse mesh
              along curves.

            * ``2`` - Do not create midside nodes (elements will have removed midside nodes).

        Notes
        -----

        .. _MSHMID_notes:

        This command is also valid for `rezoning
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_nlad/Hlp_G_ADVRZSMP.html>`_.
        """
        command = f"MSHMID,{key}"
        return self.run(command, **kwargs)



    def mshpattern(self, key: int | str = "", **kwargs):
        r"""Specifies pattern to be used for mapped triangle meshing.

        Mechanical APDL Command: `MSHPATTERN <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MSHPATTERN.html>`_

        Parameters
        ----------
        key : int or str
            Key indicating triangle pattern to be used (the figures below illustrate the pattern that will be
            used for each value of ``KEY`` ):

            * ``0`` - Allow Mechanical APDL choose the pattern (default). The program maximizes the minimum angle of
              the triangular-shaped elements that are created.

            * ``1`` - Unidirectional split at node I.

            * ``2`` - Unidirectional split at node J.

        Notes
        -----

        .. _MSHPATTERN_notes:

        "Mapped triangle meshing" refers to the Mechanical APDL program's ability to take a map-meshable
        area and
        mesh it with triangular elements, based on the value of :ref:`mshpattern`, ``KEY``. This type of
        meshing is particularly useful for analyses that involve the meshing of rigid contact elements.

        This command is valid only when you have specified that Mechanical APDL use triangle-shaped elements
        (
        :ref:`mshape`,1,2D)--or you are meshing with an element that supports only triangles-- and you have
        specified mapped meshing ( :ref:`mshkey`,1) to mesh an area.

        For details about mapped meshing with triangles, see the `Modeling and Meshing Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD14.html>`_.
        """
        command = f"MSHPATTERN,{key}"
        return self.run(command, **kwargs)



    def nrefine(self, nn1: str = "", nn2: str = "", ninc: str = "", level: str = "", depth: str = "", post: str = "", retain: str = "", **kwargs):
        r"""Refines the mesh around specified nodes.

        Mechanical APDL Command: `NREFINE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_NREFINE.html>`_

        Parameters
        ----------
        nn1 : str
            Nodes ( ``NN1`` to ``NN2`` in increments of ``NINC`` ) around which the mesh is to be refined.
            ``NN2`` defaults to ``NN1``, and ``NINC`` defaults to 1. If ``NN1`` = ALL, ``NN2`` and ``NINC``
            are ignored and all selected nodes are used for refinement. If ``NN1`` = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in the GUI). A component name
            may also be substituted for ``NN1`` ( ``NN2`` and ``NINC`` are ignored).

        nn2 : str
            Nodes ( ``NN1`` to ``NN2`` in increments of ``NINC`` ) around which the mesh is to be refined.
            ``NN2`` defaults to ``NN1``, and ``NINC`` defaults to 1. If ``NN1`` = ALL, ``NN2`` and ``NINC``
            are ignored and all selected nodes are used for refinement. If ``NN1`` = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in the GUI). A component name
            may also be substituted for ``NN1`` ( ``NN2`` and ``NINC`` are ignored).

        ninc : str
            Nodes ( ``NN1`` to ``NN2`` in increments of ``NINC`` ) around which the mesh is to be refined.
            ``NN2`` defaults to ``NN1``, and ``NINC`` defaults to 1. If ``NN1`` = ALL, ``NN2`` and ``NINC``
            are ignored and all selected nodes are used for refinement. If ``NN1`` = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in the GUI). A component name
            may also be substituted for ``NN1`` ( ``NN2`` and ``NINC`` are ignored).

        level : str
            Amount of refinement to be done. Specify the value of ``LEVEL`` as an integer from 1 to 5, where
            a value of 1 provides minimal refinement, and a value of 5 provides maximum refinement (defaults
            to 1).

        depth : str
            Depth of mesh refinement in terms of number of elements outward from the indicated nodes
            (defaults to 1).

        post : str
            Type of postprocessing to be done after element splitting, in order to improve element quality:

            * ``OFF`` - No postprocessing will be done.

            * ``SMOOTH`` - Smoothing will be done. Node locations may change.

            * ``CLEAN`` - Smoothing and cleanup will be done. Existing elements may be deleted, and node
              locations may change (default).

        retain : str
            Flag indicating whether quadrilateral elements must be retained in the refinement of an all-
            quadrilateral mesh. (Mechanical APDL ignores this argument if you are refining anything other than a
            quadrilateral mesh.)

            * ``ON`` - The final mesh will be composed entirely of quadrilateral elements, regardless of the
              element quality (default).

            * ``OFF`` - The final mesh may include some triangular elements to maintain element quality and
              provide transitioning.

        Notes
        -----

        .. _NREFINE_notes:

        This command refines all area elements and tetrahedral volume elements adjacent to the specified
        nodes.

        Mesh refinement is not available on a solid model containing initial conditions at nodes ( :ref:`ic`
        ), coupled nodes ( :ref:`cp` family of commands), constraint equations ( :ref:`ce` family of
        commands), or boundary conditions or loads applied directly to any of its nodes or elements. This
        restriction applies to nodes and elements anywhere in the model, not just in the region where you
        want to request mesh refinement. For more information about mesh refinement, see `Revising Your
        Model <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD8_6.html>`_.

        This command is also valid for `rezoning
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_nlad/Hlp_G_ADVRZSMP.html>`_.
        """
        command = f"NREFINE,{nn1},{nn2},{ninc},{level},{depth},{post},{retain}"
        return self.run(command, **kwargs)



    def psmesh(self, secid: str = "", name: str = "", p0: str = "", egroup: str = "", num: str = "", kcn: str = "", kdir: str = "", value: str = "", ndplane: str = "", pstol: str = "", pstype: str = "", ecomp: str = "", ncomp: str = "", **kwargs):
        r"""Creates and meshes a pretension section ( ``PRETS179`` ) or a preload section ( ``MPC184`` ).

        Mechanical APDL Command: `PSMESH <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PSMESH.html>`_

        Parameters
        ----------
        secid : str
            Unique section number. This number must not already be assigned to a section.

        name : str
            Unique eight character descriptive name, if desired.

        p0 : str
            Pretension node number (for a pretension section using ``PRETS179`` ) or joint element number
            (for a preload section using ``MPC184`` ).

            For a pretension element, the node is defined if it doesn't exist, and the number defaults to
            the highest node number plus one.

            For a joint element, a unique element number is assigned by default.

        egroup : str
            Element group on which :ref:`psmesh` will operate. If ``Egroup`` = P, graphical picking is enabled
            and ``NUM`` is ignored (valid only in the GUI).

            * ``L (or LINE)`` - :ref:`psmesh` operates on all elements in the line specified by ``NUM``. New
              pretension nodes are associated with ``NUM`` or entities below it. Any subsequent :ref:`lclear`
              operation of ``NUM`` deletes the pretension elements and nodes created by :ref:`psmesh`. (
              ``MPC184`` joint elements and associated contact pairs of a preload section are not deleted by
              :ref:`lclear`.)

            * ``A (or AREA)`` - :ref:`psmesh` operates on all elements in the area specified by ``NUM``. New
              pretension nodes are associated with ``NUM`` or entities below it. Any subsequent :ref:`aclear` of
              ``NUM`` deletes the pretension elements and nodes created by :ref:`psmesh`. ( ``MPC184`` joint
              elements and associated contact pairs of a preload section are not deleted by :ref:`aclear`.)

            * ``V (or VOLU)`` - :ref:`psmesh` operates on all elements in the volume specified by ``NUM``. New
              pretension nodes are associated with ``NUM`` or entities below it. Any subsequent :ref:`vclear` of
              ``NUM`` deletes the pretension elements and nodes created by :ref:`psmesh`. ( ``MPC184`` joint
              elements and associated contact pairs of a preload section are not deleted by :ref:`vclear`.)

            * ``P`` - :ref:`psmesh` operates on elements selected through the subsequent picking operations, and
              ``NUM`` is ignored

            * ``ALL`` - The command operates on all selected elements, and ``NUM`` is ignored.

        num : str
            Element group on which :ref:`psmesh` will operate. If ``Egroup`` = P, graphical picking is enabled
            and ``NUM`` is ignored (valid only in the GUI).

            * ``L (or LINE)`` - :ref:`psmesh` operates on all elements in the line specified by ``NUM``. New
              pretension nodes are associated with ``NUM`` or entities below it. Any subsequent :ref:`lclear`
              operation of ``NUM`` deletes the pretension elements and nodes created by :ref:`psmesh`. (
              ``MPC184`` joint elements and associated contact pairs of a preload section are not deleted by
              :ref:`lclear`.)

            * ``A (or AREA)`` - :ref:`psmesh` operates on all elements in the area specified by ``NUM``. New
              pretension nodes are associated with ``NUM`` or entities below it. Any subsequent :ref:`aclear` of
              ``NUM`` deletes the pretension elements and nodes created by :ref:`psmesh`. ( ``MPC184`` joint
              elements and associated contact pairs of a preload section are not deleted by :ref:`aclear`.)

            * ``V (or VOLU)`` - :ref:`psmesh` operates on all elements in the volume specified by ``NUM``. New
              pretension nodes are associated with ``NUM`` or entities below it. Any subsequent :ref:`vclear` of
              ``NUM`` deletes the pretension elements and nodes created by :ref:`psmesh`. ( ``MPC184`` joint
              elements and associated contact pairs of a preload section are not deleted by :ref:`vclear`.)

            * ``P`` - :ref:`psmesh` operates on elements selected through the subsequent picking operations, and
              ``NUM`` is ignored

            * ``ALL`` - The command operates on all selected elements, and ``NUM`` is ignored.

        kcn : str
            Coordinate system number for the separation surface and normal direction.

        kdir : str
            Direction (x, y, or z) normal to separation surface in the ``KCN`` coordinate system.

            If ``KCN`` is Cartesian, the pretension section normal will be parallel to the ``KDIR`` axis
            regardless of the position of the pretension node.

            If ``KCN`` is non-Cartesian, the pretension section normal will be aligned with the ``KDIR``
            direction of system ``KCN`` at the position of the pretension node.

            For an ``MPC184`` joint element defined as part of a preload section, ``KDIR`` is used to define
            the normal of the separation surface and does not affect the axis direction of the joint
            element.

        value : str
            Point along the ``KDIR`` axis at which to locate the separation surface. Ignored if ``NDPLANE``
            is supplied.

        ndplane : str
            Existing node that :ref:`psmesh` will use to locate the separation surface. If ``NDPLANE`` is
            supplied, the location of the separation surface is defined by the ``KDIR`` coordinate of
            ``NDPLANE``.

        pstol : str
            Optional tolerance below ``VALUE``. Allows nodes occurring precisely at or slightly below the
            separation to be identified properly as above the plane. Has the effect of shifting the plane
            down by ``PSTOL``. The following expression represents the default value:

            .. math::

                equation not available  of the locally selected region of the model based on nodal locations
            (that is, ΔX = X ``max`` - X ``min`` ).

        pstype : str
            Type of pretension or preload section to be generated.

            If a positive value is specified (or if this argument is left blank), a pretension section that
            includes ``PRETS179`` elements is generated. The value entered is the element type number for
            ``PRETS179``. If no number is specified, the program defines the element type number.

            If TORQUE is specified, a preload section that includes a `cylindrical joint element <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_MPC184cyl.html#mpc184cylinprores>`_ ( ``MPC184`` ) is generated as follows:

            * **For a 2D model** : An x-axis cylindrical joint element is generated along with two force-
              distributed surface-based constraints. A local Cartesian coordinate system is created at the first
              node of the joint element such that the local x- axis is the axis of that element (KEYOPT(4) = 0
              for the ``MPC184`` element).

            * **For a 3D model** : A z-axis cylindrical joint element is generated along with two force-
              distributed surface-based constraints. A local Cartesian coordinate system is created at the first
              node of the joint element such that the local z- axis is the axis of that element (KEYOPT(4) = 1
              for the ``MPC184`` element).

            * **For a 3D model that contains beam elements** : A z-axis cylindrical joint element is generated
              between the endpoints of two beam elements. (No force-distributed surface-based constraints are
              needed.) A local Cartesian coordinate system is created at the first node of the joint element
              such that the local z- axis is the axis of that element (KEYOPT(4) = 1 for the ``MPC184``
              element).

            If a negative value is specified, a preload section that includes a `screw joint element
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_MPC184scr.html#mpc184screwprores>`_
            ( ``MPC184`` ) is created with the absolute value of ``PSTYPE`` used as the pitch value for the
            joint. This option is only valid for 3D models. Two force-distributed surface-based constraints are
            generated at the cutting surfaces, except for the case of a beam model which does not need the
            force-distributed constraints. A local Cartesian coordinate system is created at the first node of
            the joint element such that the local z- axis is the axis of that element.

        ecomp : str
            If specified, the name of a component to be composed of new pretension elements and existing
            elements modified by the :ref:`psmesh` command. This argument is not used with the ``MPC184``
            joint element.

        ncomp : str
            Name of a component to be composed of nodes on new pretension elements. This argument is not
            used with the ``MPC184`` joint element.

        Notes
        -----

        .. _PSMESH_notes:

        :ref:`psmesh` generates a pretension section ( ``PRETS179`` ) or a preload section ( ``MPC184`` )
        for modeling bolt fastener preloads. The type of section is specified by the ``PSTYPE`` argument.

        The :ref:`psmesh` command is valid for structural analyses only.

        Pretension Section ( ``PRETS179`` )
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        When ``PSTYPE`` is a positive value or blank, the :ref:`psmesh` command creates a pretension section
        normal to the pretension load direction by cutting the mesh along existing element boundaries at the
        point defined by ``VALUE`` or ``NDPLANE`` and inserting ``PRETS179`` elements. The :ref:`psmesh`
        command verifies that ``PSTYPE`` is a ``PRETS179`` element type; if it is not, the command finds the
        lowest available ``ITYPE`` ( :ref:`et` ) that is ``PRETS179``, or it creates a new one if necessary.

        When it is necessary to define the pretension node, the program uses node ``NDPLANE``. If the
        ``NDPLANE`` value is not specified, the program defines the pretension node at:

        * The centroid of geometric entity ``NUM``, if ``Egroup`` = LINE, AREA, or VOLU; or

        * The centroid location of all selected elements, if ``Egroup`` = ALL or if graphical picking is
          used.

        If the elements to which the pretension load is to be applied have already been meshed in two
        groups, :ref:`psmesh` cannot be used to insert the pretension elements. The :ref:`eintf` command
        must be used to insert the ``PRETS179`` elements between the two meshed groups.

        The :ref:`psmesh` operation copies any nodal temperatures you have defined on the split surface of
        the original mesh from the original nodes to the newly created coincident duplicate nodes. However,
        displacements, forces, and other boundary conditions are not copied.

        By mathematical definition, the pretension surface must always be a flat plane. In a non-Cartesian
        coordinate system, the :ref:`psmesh` command creates that plane at the indicated position, oriented
        with respect to the specified direction of the active system (in the same manner that the
        :ref:`nrotat` command orients a nodal system with respect to a curved system). For example, assuming
        X = 1 and Y = 45 in a cylindrical coordinate system with Z as the axis of rotation ( ``KCN`` = 1), a
        pretension surface normal to X tilts 45 degrees away from the global X axis.

        A pretension section can be defined for fastener models made up of any 2D or 3D structural solid,
        beam, shell, pipe, or link element type. The elements can be low- or high-order.

        The pretension section is also supported for general axisymmetric elements ( ``SOLID272`` and
        ``SOLID273`` ). :ref:`psmesh` cuts the model and generates ``PRETS179`` elements between all Fourier
        nodes in the circumferential direction.

        For more information, see `Defining Pretension in a Joint Fastener
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/Hlp_G_BAS2_9.html#>`_

        Preload Section ( ``MPC184`` )
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        When ``PSTYPE`` is a negative value or set to TORQUE, the :ref:`psmesh` command defines an
        ``MPC184`` joint element for applying a preload to a bolt undergoing large rotation or large
        deformation. :ref:`psmesh` cuts the mesh in two parts along existing element boundaries at the point
        defined by ``VALUE`` or ``NDPLANE``. It generates `force-distributed surface-based constraints
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_ctec/Hlp_ctec_surfcon.html#strbeamso1703>`_
        (remote points) on the cutting surfaces, inserts an ``MPC184`` joint element that connects the two
        pilot nodes, and creates a local Cartesian coordinate system at the first node of the joint element
        to define the normal direction. If the joint is between beam elements, no force-distributed
        constraints are generated. For more information, see `Defining Preload in a Joint Fastener
        Undergoing Large Rotation
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/bas_preload_joint.html#>`_

        The preload section based on ``MPC184`` is not supported for general axisymmetric elements (
        ``SOLID272`` and ``SOLID273`` ).
        """
        command = f"PSMESH,{secid},{name},{p0},{egroup},{num},{kcn},{kdir},{value},{ndplane},{pstol},{pstype},{ecomp},{ncomp}"
        return self.run(command, **kwargs)



    def real(self, nset: str = "", **kwargs):
        r"""Sets the element real constant set attribute pointer.

        Mechanical APDL Command: `REAL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_REAL.html>`_

        Parameters
        ----------
        nset : str
            Assign this real constant set number to subsequently defined elements (defaults to 1).

        Notes
        -----

        .. _REAL_notes:

        Identifies the real constant set number to be assigned to subsequently defined elements. This number
        refers to the real constant set number ( ``NSET`` ) defined with the real constant sets ( :ref:`r`
        ). Real constant set numbers may be displayed ( :ref:`pnum` ). If the element type requires no real
        constants, this entry is ignored. Elements of different type should not refer to the same real
        constant set.
        """
        command = f"REAL,{nset}"
        return self.run(command, **kwargs)



    def rsmesh(self, p0: str = "", rid: str = "", kcn: str = "", kdir: str = "", value: str = "", ndplane: str = "", pstol: str = "", ecomp: str = "", **kwargs):
        r"""Generates a result section.

        Mechanical APDL Command: `RSMESH <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_RSMESH.html>`_

        Parameters
        ----------
        p0 : str
            User-defined anchor point node number. This must be a previously defined target element pilot
            node (see :ref:`RSMESH_notes` for more information). If ``P0`` is specified, ``RID``, ``KCN``,
            ``Kdir``, ``VALUE``, and ``NDPLANE`` are ignored. The result section is defined in the
            x-direction of the nodal coordinate system of the pilot node.

            If ``P0`` is not specified, the program computes the geometry center point as the anchor point
            location by default.

        rid : str
            Unique real constant ID number that has not been previously assigned to any other elements. If
            ``RID`` is not specified, the program selects the next available real constant ID number.

        kcn : str
            Coordinate system number used to define the result surface and normal direction.

        kdir : str
            Direction (x, y, or z) normal to the result surface in the ``KCN`` coordinate system.

        value : str
            Point along the ``Kdir`` axis at which to locate the result surface. Ignored if ``NDPLANE`` is
            specified.

        ndplane : str
            Node number of existing node used to locate the result surface. If ``NDPLANE`` is specified, the
            location of the result surface is defined by the ``Kdir`` coordinate of ``NDPLANE`` in the
            ``KCN`` coordinate system.

        pstol : str
            Optional tolerance below ``VALUE``. Allows nodes occurring precisely at or slightly below the
            result surface to be identified properly as above the plane. Has the effect of shifting the
            plane down by ``PSTOL``. The following expression represents the default value:

            .. math::

                equation not available  of the locally selected region of the model based on nodal locations
            (that is, ΔX = X ``max`` - X ``min`` ).

        ecomp : str
            If specified, the name of a component to be composed of elements underneath the result section
            generated by the :ref:`rsmesh` command.

        Notes
        -----

        .. _RSMESH_notes:

        This command defines a result section and automatically imbeds contact elements ( ``CONTA172`` or
        ``CONTA174`` ) on the surface of the selected base elements. See `Monitoring Result Section Data
        During Solution
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/str_resultsec.html#>`_

        A user-specified anchor point and local coordinate system can be specified by defining a pilot node
        (a target element defined using :ref:`tshap`,PILO) before issuing the :ref:`rsmesh` command. Input
        the pilot node number for ``P0``. Only one pilot node should be associated with a result section;
        the pilot node should not be used for any other purpose (such as remote loading). The contact
        elements generated for the result section will have the same real constant ID as the pilot node
        target element.
        """
        command = f"RSMESH,{p0},{rid},{kcn},{kdir},{value},{ndplane},{pstol},{ecomp}"
        return self.run(command, **kwargs)



    def shpp(self, lab: str = "", value1: str = "", value2: str = "", **kwargs):
        r"""Controls element shape checking.

        Mechanical APDL Command: `SHPP <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SHPP.html>`_

        Parameters
        ----------
        lab : str
            Shape-checking option. (When ``Lab`` = WARN, STATUS, SUMMARY, or DEFAULT, the remaining arguments are ignored.)

            * ``ON`` - Activates element shape-checking. New elements, regardless of how they are created, are
              tested against existing warning and error limits. (The existing limits may be the default limits, or
              previously modified limits.) Elements that violate error limits produce error messages and either
              (a) cause a meshing failure, or (b) for element creation or storage other than :ref:`amesh` or
              :ref:`vmesh`, are not stored. Elements that violate warning limits produce warning messages. If
              shape-checking was previously turned off ( :ref:`shpp`,OFF) and you turn it on, existing elements
              are marked as untested; use the :ref:`check` command to retest them. With this option, you may also
              specify a value for ``VALUE1`` to turn individual shape tests on. If you do not specify a value for
              ``VALUE1``, all shape tests are turned on.

            * ``WARN`` - Activates element shape-checking; however, in contrast to :ref:`shpp`,ON, elements that
              violate error limits do not cause either a meshing or element storage failure. Instead, they produce
              warning messages to notify you that error limits have been violated. This option does not alter
              current shape parameter limits. Since the default shape parameter error limits are set to allow
              almost any usable element, the elements this option allows, which would otherwise be forbidden, are
              likely to be very poorly shaped.

            * ``OFF`` - Deactivates element shape-checking. This setting does not alter current shape parameter
              limits. Use of this option is risky, since poorly shaped elements can lead to analysis results that
              are less accurate than would otherwise be expected for a given mesh density. With this option, you
              may also specify a value for ``VALUE1`` to turn individual shape tests off. If you do not specify a
              value for ``VALUE1``, all element shape tests are turned off.

            * ``SILENT`` - Determines whether element shape-checking runs in silent mode. In silent mode,
              Mechanical APDL checks elements without issuing warnings, with the exception of the generic warnings that
              it issues at solution. With this option, you must also specify a value for ``VALUE1`` (During the
              execution of certain commands, Mechanical APDL automatically runs element shape-checking in silent mode,
              then internally summarizes the shape test results for all of the new or modified elements. Mechanical APDL
              does this when it executes any of the following commands: :ref:`agen`, :ref:`amesh`, :ref:`arefine`,
              :ref:`arsym`, :ref:`atran`, :ref:`cdread`, :ref:`egen`, :ref:`engen`, :ref:`ensym`, :ref:`eread`,
              :ref:`erefine`, :ref:`esym`, :ref:`et`, :ref:`fvmesh`, :ref:`krefine`, :ref:`lrefine`,
              :ref:`nrefine`, :ref:`timp`, :ref:`vext`, :ref:`vgen`, :ref:`vimp`, :ref:`vmesh`, :ref:`voffst`,
              :ref:`vrotat`, :ref:`vsweep`, :ref:`vsymm`, and :ref:`vtran`.)

            * ``STATUS`` - Lists the shape parameter limits currently in effect, along with status information
              about element shape-checking (for example, whether any individual shape tests are off, whether any
              of the shape parameter limits have been modified, and so on).

            * ``SUMMARY`` - Lists a summary of element shape test results for all selected elements.

            * ``DEFAULT`` - Resets element shape parameter limits to their default values. Also, if any
              individual tests were turned off, turns them back on. (The :ref:`shpp`,DEFAULT command may be useful
              if any parameter limits were previously altered by using the MODIFY option.)

            * ``OBJECT`` - Determines whether element shape test results data is stored in memory. When this
              option is turned on, an "object" is created for storing test results in memory. When this option is
              turned off, no object is created and no data is stored; thus, any operation that requires shape
              parameters for an existing element (such as use of the :ref:`check` command) causes the shape
              parameters to be recomputed. (Note the distinction between storing the data in memory and storing it
              in the database; regardless of whether this option is turned on or off, no element shape test
              results data will be stored in the database. The element shape parameter object is deleted
              automatically before any solution.) This setting is independent of shape-checking status, with one
              exception--if shape- checking is turned off ( :ref:`shpp`,OFF), the object is not created. Keep in
              mind that recomputing shape parameters is more computationally expensive than retrieving them from
              the object. With this option, you must also specify a value for the ``VALUE1`` argument; the
              ``VALUE2`` argument is ignored.

            * ``LSTET`` - Determines, for Jacobian ratio tests, whether sampling is done at integration points
              or at corner nodes. When this option is turned on, sampling is done at integration points, and the
              default limits for h-element Jacobian ratios are a warning tolerance of 10 and an error tolerance of
              40. When this option is turned off, sampling is done at corner nodes, and the corresponding default
              limits are a warning tolerance of 30 and an error tolerance of 1000. Sampling at the integration
              points (option on) results in a lower Jacobian ratio, but that ratio is also subjected to a more
              restrictive error limit. Some elements that have passed the integration point sampling criterion,
              have failed the corner mode sampling criterion. Because of this, use integration point sampling only
              for simple linear analyses. For other types of analyses (e.g., nonlinear, electromagnetic), use
              sampling at corner nodes, which is the more conservative approach. With this option, you must also
              specify a value for the ``VALUE1`` argument; the ``VALUE2`` argument is ignored.

            * ``MODIFY`` - Indicates that you want to respecify a shape parameter limit. With this option, you
              must also specify values for the ``VALUE1`` and ``VALUE2`` arguments.

            * ``FLAT`` - Determines the warning and error limits used to test elements that may exhibit
              nonzero/nonconstant Z coordinates. With this option, you must also specify values for the ``VALUE1``
              and/or ``VALUE2`` arguments.

        value1 : str
            Valid for the ON, OFF, SILENT, OBJECT, LSTET, MODIFY, and FLAT options only. When ``Lab`` = ON or OFF, use ``VALUE1`` to individually control (that is, turn off or turn on) specific element shape tests. Thus, ``VALUE1`` can be ASPECT (aspect ratio tests), PARAL (deviation from parallelism of opposite edges tests), MAXANG (maximum corner angle tests), JACRAT (Jacobian ratio tests), WARP (warping factor tests), or ALL (all tests). When ``Lab`` = SILENT, ``VALUE1`` can be ON (to turn silent mode on) or OFF (to turn silent mode off). When ``Lab`` = OBJECT, ``VALUE1`` can be either 1, YES, or ON to turn on storage of element shape test data (the default); or it can be 0, NO, or OFF to turn off storage of element shape test data (delete the data and recompute as necessary). When ``Lab`` = LSTET, ``VALUE1`` can be either 1, YES, or ON to choose Jacobian sampling at integration points; or it can be 0, NO, or OFF to choose Jacobian sampling at nodes (the default). When ``Lab`` = MODIFY, ``VALUE1`` is the numeric location (within the shape parameter limit array) of the shape parameter limit to be modified. Locations are identified in the element shape-checking status listing ( :ref:`shpp`,STATUS). For more information, see the examples in the **Notes** section. When ``Lab`` = FLAT, ``VALUE1`` is the warning limit for XY element constant Z sets performed at :ref:`check` or :ref:`solve`. The default is 1.0e-8.

        value2 : str
            Valid for the MODIFY and FLAT options only. When ``Lab`` = MODIFY, specifies the new limit for the shape parameter that is in the location indicated by the ``VALUE1`` argument. See the examples in the **Notes** section. When ``Lab`` = FLAT, ``VALUE2`` is the error limit. The default is 1.0e-2.

        Notes
        -----

        .. _SHPP_notes:

        The following examples illustrate how to use the :ref:`shpp`,MODIFY, ``VALUE1``, ``VALUE2`` command
        to respecify shape parameter limits. Assume that you issued the :ref:`shpp`,STATUS command, and you
        received the output below:

        .. code:: apdl

            ASPECT RATIO (EXCEPT EMAG)

               QUAD OR TRIANGLE ELEMENT OR FACE
                    WARNING TOLERANCE ( 1) =   20.00000
                    ERROR TOLERANCE   ( 2) =  1000000.
                               .
                               .
                               .
            MAXIMUM CORNER ANGLE IN DEGREES (EXCEPT OR EMAG)
               TRIANGLE ELEMENT OR FACE
                    WARNING TOLERANCE (15) =   165.0000
                    ERROR TOLERANCE   (16) =   179.9000

 

        Notice that in the sample output, the warning tolerance for aspect ratios is set to 20. Now assume
        that you want to "loosen" this shape parameter limit so that it is less restrictive. To allow
        elements with aspect ratios of up to 500 without causing warning messages, you would issue this
        command:

        :ref:`shpp`,MODIFY,1,500

        Also notice that each shape parameter's numeric location within the shape parameter limit array
        appears in the sample output within parentheses. For example, the numeric location of the aspect
        ratio shape parameter (for warning tolerance) is 1, which is why "1" is specified for the ``VALUE1``
        argument in the example command above.

        Now notice that the sample output indicates that any triangle element with an internal angle that is
        greater than 179.9 degrees will produce an error message. Suppose that you want to "tighten" this
        shape parameter limit, so that it is more restrictive. To cause any triangle or tetrahedron with an
        internal angle greater than 170 degrees to produce an error message, you would issue this command:

        :ref:`shpp`,MODIFY,16,170

        The existence of badly shaped elements in a model may lead to certain computational errors that can
        cause your system to terminate during solution. Therefore, you run the risk of a system abort during
        solution any time that you disable element shape-checking entirely, run shape-checking in warning-
        only mode, disable individual shape-checks, or loosen shape-parameter limits.

        Changing any shape parameter limit marks all existing elements as untested; use the :ref:`check`
        command to retest them.

        For more information about element shape-checking, see `Meshing Your Solid Model
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD7_8.html>`_.

        This command is also valid for `rezoning
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_nlad/Hlp_G_ADVRZSMP.html>`_.
        """
        command = f"SHPP,{lab},{value1},{value2}"
        return self.run(command, **kwargs)



    def smrtsize(self, sizlvl: str = "", fac: str = "", expnd: str = "", trans: str = "", angl: str = "", angh: str = "", gratio: str = "", smhlc: str = "", smanc: str = "", mxitr: str = "", sprx: str = "", **kwargs):
        r"""Specifies meshing parameters for automatic (smart) element sizing.

        Mechanical APDL Command: `SMRTSIZE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SMRTSIZE.html>`_

        Parameters
        ----------
        sizlvl : str
            Overall element size level for meshing. The level value controls the fineness of the mesh. (Any
            input in this field causes remaining arguments to be ignored.) Valid inputs are:

            * ``n`` - Activate SmartSizing and set the size level to ``n``. Must be an integer value from 1
              (fine mesh) to 10 (coarse mesh). Remaining arguments are ignored, and argument values are set as
              shown in :ref:`SMRTSIZE_tab_1`.

            * ``STAT`` - List current :ref:`smrtsize` settings.

            * ``DEFA`` - Set all :ref:`smrtsize` settings to default values (as shown in :ref:`SMRTSIZE_tab_1`
              for size level 6).

            * ``OFF`` - Deactivate SmartSizing. Current settings of :ref:`desize` will be used. To reactivate
              SmartSizing, issue :ref:`smrtsize`, ``n``.

        fac : str
            Scaling factor applied to the computed default mesh sizing. Defaults to 1 for h-elements (size
            level 6), which is medium. Values from 0.2 to 5.0 are allowed.

        expnd : str
            Mesh expansion (or contraction) factor. (This factor is the same as :ref:`mopt`,EXPND,
            ``Value``.) ``EXPND`` is used to size internal elements in an area based on the size of the
            elements on the area's boundaries. For example, issuing :ref:`smrtsize`,,,2 before meshing an
            area will allow a mesh with elements that are approximately twice as large in the interior of an
            area as they are on the boundary. If ``EXPND`` is less than 1, a mesh with smaller elements on
            the interior of the area will be allowed. ``EXPND`` should be greater than 0.5 but less than 4.
            ``EXPND`` defaults to 1 for h-elements (size level 6), which does not allow expansion or
            contraction of internal element sizes (except when using :ref:`aesize` element sizing). (If
            ``EXPND`` is set to zero, the default value of 1 will be used.) The actual size of the internal
            elements will also depend on the ``TRANS`` option or upon :ref:`aesize` or :ref:`esize` sizing,
            if used.

        trans : str
            Mesh transition factor. (This factor is the same as :ref:`mopt`,TRANS, ``Value``.) ``TRANS`` is
            used to control how rapidly elements are permitted to change in size from the boundary to the
            interior of an area. ``TRANS`` defaults to 2.0 for h-elements (size level 6), which permits
            elements to approximately double in size from one element to the next as they approach the
            interior of the area. (If ``TRANS`` is set to zero, the default value will be used.) ``TRANS``
            must be greater than 1 and, for best results, should be less than 4. The actual size of the
            internal elements will also depend on the ``EXPND`` option or upon :ref:`aesize` or :ref:`esize`
            sizing, if used.

        angl : str
            Maximum spanned angle per lower-order element for curved lines. Defaults to 22.5 degrees per
            element (size level 6). This angle limit may be exceeded if the mesher encounters a small
            feature (hole, fillet, etc.). (This value is not the same as that set by :ref:`desize`,,,
            ``ANGL``.)

        angh : str
            Maximum spanned angle per higher-order element for curved lines. Defaults to 30 degrees per
            element (size level 6). This angle limit may be exceeded if the mesher encounters a small
            feature (hole, fillet, etc.). (This value is NOT the same as that set by :ref:`desize`,,,,
            ``ANGH``.)

        gratio : str
            Allowable growth ratio used for proximity checking. Defaults to 1.5 for h-elements (size level
            6). Values from 1.2 to 5.0 are allowed; however, values from 1.5 to 2.0 are recommended.

        smhlc : str
            Small hole coarsening key, can be ON (default for size level 6) or OFF. If ON, this feature
            suppresses curvature refinement that would result in very small element edges (that is,
            refinement around small features).

        smanc : str
            Small angle coarsening key, can be ON (default for all levels) or OFF. If ON, this feature
            restricts proximity refinement in areas where it is ill-advised (that is, in tight corners on
            areas, especially those that approach 0 degrees).

        mxitr : str
            Maximum number of sizing iterations (defaults to 4 for all levels).

        sprx : str
            Surface proximity refinement key, can be off ( ``SPRX`` = 0, which is the default for all levels
            ) or on via two different values ( ``SPRX`` = 1 or ``SPRX`` = 2). If ``SPRX`` = 1, surface
            proximity refinement is performed and any shell elements that need to be modified are modified.
            If ``SPRX`` =2, surface proximity refinement is performed but no shell elements are altered.

        Notes
        -----

        .. _SMRTSIZE_notes:

        If a valid level number (1 (fine) to 10 (coarse)) is input on ``SIZLVL``, inputs for remaining
        arguments are ignored, and the argument values are set as shown in :ref:`SMRTSIZE_tab_1`.

        The settings shown are for h-elements. The first column contains ``SIZLV`` data, ranging from 10
        (coarse) to 1 (fine). The default is 6 (indicated by the shaded row).

        .. _SMRTSIZE_tab_1:

        SMRTSIZE - Argument Values for h-elements
        *****************************************

        .. flat-table::
           :header-rows: 1

           * - 
             -  FAC
             -  EXPND
             -  TRANS
             -  ANGL
             -  ANGH
             -  GRATIO
             -  SMHLC
             -  SMANC
             -  MXITR
             -  SPRX
           * - 10
             - 5.0
             - 2.0
             - 2.0*
             - 45.0
             - 45.0*
             - 2.0
             - on
             - on
             - 4*
             - off
           * - 9
             - 3.0
             - 1.75
             - 2.0*
             - 36.0
             - 45.0*
             - 1.9
             - on
             - on
             - 4*
             - off
           * - 8
             - 1.875
             - 1.5
             - 2.0*
             - 30.0
             - 45.0*
             - 1.8
             - on
             - on
             - 4*
             - off
           * - 7
             - 1.5
             - 1.0
             - 2.0*
             - 26.0
             - 36.0*
             - 1.7
             - on
             - on
             - 4*
             - off
           * -  6
             -  1.0*
             - _cellfont Shading="gray1" ? 1.0*
             -  2.0*
             -  22.5
             -  30.0*
             - _cellfont Shading="gray1" ? 1.5*
             -  on
             -  on
             -  4*
             - _cellfont Shading="gray1" ? off
           * - 5
             - 0.65
             - 1.0*
             - 2.0*
             - 18.0
             - 27.0
             - 1.5
             - on
             - on
             - 4*
             - off
           * - 4
             - 0.4
             - 1.0*
             - 2.0*
             - 15.0
             - 22.0
             - 1.5
             - off
             - on
             - 4*
             - off
           * - 3
             - 0.3
             - 1.0*
             - 2.0*
             - 12.0
             - 18.0
             - 1.5
             - off
             - on
             - 4*
             - off
           * - 2
             - 0.25
             - 1.0*
             - 2.0*
             - 10.0
             - 15.0
             - 1.5
             - off
             - on
             - 4*
             - off
           * - 1
             - 0.2
             - 1.0*
             - 2.0*
             - 7.5
             - 15.0
             - 1.4
             - off
             - on
             - 4*
             - off

        Where appropriate, SmartSizing will start with :ref:`aesize` settings. Elsewhere, it will start with
        any defined :ref:`esize`,SIZE setting. It will locally override :ref:`aesize` or :ref:`esize` for
        proximity and curvature. SmartSizing ignores any :ref:`esize`,,NDIV setting.

        :ref:`lesize` line division and spacing specifications will be honored by SmartSizing, unless you
        give permission for SmartSizing to override them (for proximity or curvature) by setting KYNDIV to
        1. Lines not having an :ref:`lesize` specification are meshed as well as they can be.

        This command is also valid for `rezoning
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_nlad/Hlp_G_ADVRZSMP.html>`_.
        """
        command = f"SMRTSIZE,{sizlvl},{fac},{expnd},{trans},{angl},{angh},{gratio},{smhlc},{smanc},{mxitr},{sprx}"
        return self.run(command, **kwargs)



    def tchg(self, ename1: str = "", ename2: str = "", etype2: str = "", **kwargs):
        r"""Converts 20-node degenerate tetrahedral elements to their 10-node non-degenerate counterparts.

        Mechanical APDL Command: `TCHG <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_TCHG.html>`_

        Parameters
        ----------
        ename1 : str
            Name (or the number) of the 20-node tetrahedron element that you want to convert. This argument
            is required.

        ename2 : str
            Name (or the number) of the 10-node tetrahedron element to which you want to convert the
            ``ENAME`` elements. This argument is required.

        etype2 : str
            Element TYPE reference number for ``ENAME2``. If ``ETYPE2`` is 0 or is not specified, the
            program selects the element TYPE reference number for ``ENAME2``. See the :ref:`TCHG_notes`
            section for details. This argument is optional.

        Notes
        -----

        .. _TCHG_notes:

        The :ref:`tchg` command allows you to specify conversion of any selected 20-node brick that is
        degenerated into a tetrahedron to a 10-node tetrahedron.

        The :ref:`tchg` command is useful when used in with the :ref:`mopt`,PYRA command. Twenty-node
        pyramid shaped elements may be used in the same volume with 10-node tetrahedra.

        Performing a conversion is likely to create circumstances in which more than one element type is
        defined for a single volume.

        If specified, ``ETYPE2`` will usually be the same as the local element TYPE number ( :ref:`et`,
        ``ITYPE`` ) that was assigned to ``ENAME2`` with the :ref:`et` command. You can specify a unique
        number for ``ETYPE2`` if you prefer. Although ``ETYPE2`` is optional, it may be useful when two or
        more ``ITYPE`` s have been assigned to the same element (for example, if two ``SOLID187`` elements
        have been established in the element attribute tables for the current model, use the ``ETYPE2``
        argument to distinguish between them). If ``ETYPE2`` is nonzero and it has not already been assigned
        to an element via :ref:`et`, the program assigns the ``ETYPE2`` value to ``ENAME2`` as its element
        TYPE reference number.

        If ``ETYPE2`` is 0 or is not specified, the program determines the element TYPE reference number for
        ``ENAME2`` in one of these ways:

        * If ``ETYPE2`` is 0 or is not specified, and ``ENAME2``  does not appear in the element attribute
          tables, the program uses the next available (unused) location in the element attribute tables to
          determine the element TYPE reference number for ``ENAME2``.

        * If ``ETYPE2`` is 0 or is not specified, and ``ENAME2``  appears in the element attribute tables,
          the program uses ``ENAME2`` 's existing element TYPE reference number for ``ETYPE2``. (If there is
          more than one occurrence of ``ENAME2`` in the element attribute tables (each with its own TYPE
          reference number), the program uses the first ``ENAME2`` reference number for ``ETYPE2``.)

        You cannot use element conversion if boundary conditions or loads are applied directly to any
        selected elements.

        For more information about converting degenerate tetrahedral elements, see `Meshing Your Solid Model
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD7_8.html>`_ in the
        `Modeling and Meshing Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD14.html>`_
        """
        command = f"TCHG,{ename1},{ename2},{etype2}"
        return self.run(command, **kwargs)



    def timp(self, elem: str = "", chgbnd: int | str = "", implevel: int | str = "", **kwargs):
        r"""Improves the quality of tetrahedral elements that are not associated with a volume.

        Mechanical APDL Command: `TIMP <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_TIMP.html>`_

        Parameters
        ----------
        elem : str
            Identifies the tetrahedral elements to be improved. Valid values are ALL and P. If ``ELEM`` =
            ALL (default), improve all selected tetrahedral elements. If ``ELEM`` = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in the GUI).

        chgbnd : int or str
            Specifies whether to allow boundary modification. Boundary modification includes such things as
            changes in the connectivity of the element faces on the boundary and the addition of boundary nodes.
            (Also see the Notes section below for important usage information for ``CHGBND``.)

            * ``0`` - Do not allow boundary modification.

            * ``1`` - Allow boundary modification (default).

        implevel : int or str
            Identifies the level of improvement to be performed on the elements. (Improvement occurs primarily
            through the use of face swapping and node smoothing techniques.)

            * ``0`` - Perform the least amount of swapping/smoothing.

            * ``1`` - Perform an intermediate amount of swapping/smoothing.

            * ``2`` - Perform the greatest amount of swapping/smoothing.

            * ``3`` - Perform the greatest amount of swapping/smoothing, plus additional improvement techniques
              (default).

        Notes
        -----

        .. _TIMP_notes:

        The :ref:`timp` command enables you to improve a given tetrahedral mesh by reducing the number of
        poorly-shaped tetrahedral elements (in particular, the number of sliver tetrahedral elements)--as
        well as the overall number of elements--in the mesh. It also improves the overall quality of the
        mesh.

        :ref:`timp` is particularly useful for an imported tetrahedral mesh for which no geometry
        information is attached.

        Regardless of the value of the ``CHGBND`` argument, boundary mid-nodes can be moved.


        When loads or constraints have been placed on boundary nodes or mid-nodes, and boundary mid-nodes
        are later moved, the program issues a warning message to let you know that it will not update the
        loads or constraints.

        No boundary modification is performed if shell or beam elements are present in the mesh, even when
        ``CHGBND`` = 1.
        """
        command = f"TIMP,{elem},{chgbnd},{implevel}"
        return self.run(command, **kwargs)



    def type(self, itype: str = "", **kwargs):
        r"""Sets the element type attribute pointer.

        Mechanical APDL Command: `TYPE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_TYPE.html>`_

        Parameters
        ----------
        itype : str
            Assign a type number to the elements (defaults to 1).

        Notes
        -----

        .. _TYPE_notes:

        Assigns an element-type number to subsequently defined elements. The number refers to the element-
        type number ( ``ITYPE`` ) defined with via :ref:`et`. You can display type numbers ( :ref:`pnum` ).

        In some cases, the program can proceed with a meshing operation even when no logical element type
        has been assigned via :ref:`type` or **XATT**, ``TYPE``. For more information, see the discussion
        for setting element attributes in `Meshing Your Solid Model
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD7_8.html>`_.
        """
        command = f"TYPE,{itype}"
        return self.run(command, **kwargs)



    def vatt(self, mat: str = "", real: str = "", type_: str = "", esys: str = "", secnum: str = "", **kwargs):
        r"""Associates element attributes with the selected, unmeshed volumes.

        Mechanical APDL Command: `VATT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_VATT.html>`_

        Parameters
        ----------
        mat : str
            Material number, real constant set number, type number, coordinate system number, and section
            number to be associated with selected, unmeshed volumes.

        real : str
            Material number, real constant set number, type number, coordinate system number, and section
            number to be associated with selected, unmeshed volumes.

        type_ : str
            Material number, real constant set number, type number, coordinate system number, and section
            number to be associated with selected, unmeshed volumes.

        esys : str
            Material number, real constant set number, type number, coordinate system number, and section
            number to be associated with selected, unmeshed volumes.

        secnum : str
            Material number, real constant set number, type number, coordinate system number, and section
            number to be associated with selected, unmeshed volumes.

        Notes
        -----

        .. _VATT_notes:

        These element attributes will be used when the volumes are meshed. If a volume does not have
        attributes associated with it (by this command) at the time it is meshed, the attributes are
        obtained from the then current :ref:`mat`, :ref:`real`, :ref:`type`, :ref:`esys`, and :ref:`secnum`
        command settings. Reissue the :ref:`vatt` command (before volumes are meshed) to change the
        attributes. A zero (or blank) argument removes the corresponding association.

        If any of the arguments ``MAT``, ``REAL``, ``TYPE``, ``ESYS`` or ``SECNUM`` are defined as -1, then
        that value will be left unchanged in the selected set.

        In some cases, the program can proceed with a volume meshing operation even when no logical element
        type has been assigned via :ref:`vatt`, ``TYPE`` or :ref:`type`. For more information, see the
        discussion on setting element attributes in `Meshing Your Solid Model
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD7_8.html>`_   of the
        `Modeling and Meshing Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD14.html>`_.
        """
        command = f"VATT,{mat},{real},{type_},{esys},{secnum}"
        return self.run(command, **kwargs)



    def vclear(self, nv1: str = "", nv2: str = "", ninc: str = "", **kwargs):
        r"""Deletes nodes and volume elements associated with selected volumes.

        Mechanical APDL Command: `VCLEAR <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_VCLEAR.html>`_

        Parameters
        ----------
        nv1 : str
            Delete mesh for volumes ``NV1`` to ``NV2`` (defaults to ``NV1`` ) in steps of ``NINC`` (defaults
            to 1). If ``NV1`` = ALL, ``NV2`` and ``NINC`` are ignored and mesh for all selected volumes (
            :ref:`vsel` ) is deleted. If ``NV1`` = P, graphical picking is enabled and all remaining command
            fields are ignored (valid only in the GUI). A component name may also be substituted for ``NV1``
            ( ``NV2`` and ``NINC`` are ignored).

        nv2 : str
            Delete mesh for volumes ``NV1`` to ``NV2`` (defaults to ``NV1`` ) in steps of ``NINC`` (defaults
            to 1). If ``NV1`` = ALL, ``NV2`` and ``NINC`` are ignored and mesh for all selected volumes (
            :ref:`vsel` ) is deleted. If ``NV1`` = P, graphical picking is enabled and all remaining command
            fields are ignored (valid only in the GUI). A component name may also be substituted for ``NV1``
            ( ``NV2`` and ``NINC`` are ignored).

        ninc : str
            Delete mesh for volumes ``NV1`` to ``NV2`` (defaults to ``NV1`` ) in steps of ``NINC`` (defaults
            to 1). If ``NV1`` = ALL, ``NV2`` and ``NINC`` are ignored and mesh for all selected volumes (
            :ref:`vsel` ) is deleted. If ``NV1`` = P, graphical picking is enabled and all remaining command
            fields are ignored (valid only in the GUI). A component name may also be substituted for ``NV1``
            ( ``NV2`` and ``NINC`` are ignored).

        Notes
        -----

        .. _VCLEAR_notes:

        Deletes all nodes and volume elements associated with selected volumes (regardless of whether the
        nodes or elements are selected). Nodes shared by adjacent meshed volumes and nodes associated with
        non-volume elements will not be deleted. Attributes assigned as a result of :ref:`vatt` are
        maintained. In the program's response to the command, if a volume, area, line, or keypoint is
        tallied as "cleared," it means either its node or element reference was deleted.
        """
        command = f"VCLEAR,{nv1},{nv2},{ninc}"
        return self.run(command, **kwargs)



    def veorient(self, vnum: str = "", option: str = "", value1: str = "", value2: str = "", **kwargs):
        r"""Specifies brick element orientation for volume mapped (hexahedron) meshing.

        Mechanical APDL Command: `VEORIENT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_VEORIENT.html>`_

        **Command default:**
        Elements are not oriented in any specific manner.

        Parameters
        ----------
        vnum : str
            Number identifying volume for which elements are to be oriented (no default).

        option : str
            Option for defining element orientation:

            * ``KP`` - Orientation is determined by two keypoints on the volume. Input the keypoint numbers (KZ1
              and KZ2) in fields ``VALUE1`` and ``VALUE2``, respectively. The element z-axis points from KZ1
              toward KZ2. Element x and y directions point away from KZ1 along edges of the volume to make a
              right-hand triad. (The element x- and y-axes are uniquely determined by this specification.)

            * ``LINE`` - Orientation is determined by one of the lines defining the volume. Input the line
              number in field ``VALUE1``. The element z direction follows the direction of the line. Input a
              negative value if the desired z direction is opposite to the direction of the specified line. (The
              element x- and y-axes are uniquely determined by this specification.) ( ``VALUE2`` is not used.)

            * ``AREA`` - Orientation is determined by one of the areas defining the volume. The area represents
              the desired element top surface. Input the area number as ``VALUE1``. The shortest line in the
              volume connected to the area will be used to specify the element z direction. (If more than one
              shortest line exists, the lowest numbered of those is used.) Element x and y directions are not
              uniquely specified by this option. ( ``VALUE2`` is not used.)

            * ``THIN`` - Align the element z normal to the thinnest dimension of the volume. The shortest line
              in the volume is used to specify the element z direction. (If more than one shortest line exists,
              the lowest numbered of those is used.) Element x and y directions are not uniquely specified by this
              option. ( ``VALUE1`` and ``VALUE2`` are not used.)

            * ``DELE`` - Delete the previously defined volume orientation for the specified volume ( ``VNUM`` ).
              ( ``VALUE1`` and ``VALUE2`` are not used.)

        value1 : str
            Parameters required for the element z-axis direction specification. The meaning of ``VALUE1``
            and ``VALUE2`` will depend on the chosen ``Option``. See the description of ``Option`` above for
            details.

        value2 : str
            Parameters required for the element z-axis direction specification. The meaning of ``VALUE1``
            and ``VALUE2`` will depend on the chosen ``Option``. See the description of ``Option`` above for
            details.

        Notes
        -----
        Use :ref:`veorient` before the :ref:`vmesh` command to specify the desired orientation of brick
        elements in a mapped mesh. :ref:`veorient` has no effect on tetrahedron meshes, extruded meshes (
        :ref:`vrotat`, :ref:`vdrag`, :ref:`vext`, etc.), or swept meshes ( :ref:`vsweep` ).

        Proper brick orientation is essential for certain element types such as  ``SOLID185`` Layered
        Solid, ``SOLID186`` Layered Solid, and ``SOLSH190``. In such cases, use :ref:`veorient` or
        :ref:`eorient` to achieve the desired orientation. For other brick element types, you may need to
        specify element orientation to control orthotropic material property directions without concern for
        the element connectivity. For those cases, the :ref:`esys` command is the preferred method of
        specifying the material property directions.

        For ``Option`` = LINE, AREA, and THIN, the orientation will be internally converted to an equivalent
        ``Option`` = KP specification (KP,KZ1,KZ2). Use the :ref:`vlist` command to view the element
        orientations (in terms of KZ1 and KZ2) associated with each volume.
        """
        command = f"VEORIENT,{vnum},{option},{value1},{value2}"
        return self.run(command, **kwargs)



    def vimp(self, vol: str = "", chgbnd: int | str = "", implevel: int | str = "", **kwargs):
        r"""Improves the quality of the tetrahedral elements in the selected volume(s).

        Mechanical APDL Command: `VIMP <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_VIMP.html>`_

        Parameters
        ----------
        vol : str
            Number of the volume containing the tetrahedral elements to be improved. If ``VOL`` = ALL
            (default), improve the tetrahedral elements in all selected volumes. If ``VOL`` = P, graphical
            picking is enabled and all remaining command fields are ignored (valid only in the GUI). A
            component name may also be substituted for ``VOL``.

        chgbnd : int or str
            Specifies whether to allow boundary modification. Boundary modification includes such things as
            changes in the connectivity of the element faces on the boundary and the addition of boundary nodes.
            (Also see :ref:`VIMP_notes` below for important usage information for ``CHGBND``.)

            * ``0`` - Do not allow boundary modification.

            * ``1`` - Allow boundary modification (default).

        implevel : int or str
            Identifies the level of improvement to be performed on the elements. (Improvement occurs primarily
            through the use of face swapping and node smoothing techniques.)

            * ``0`` - Perform the least amount of swapping/smoothing.

            * ``1`` - Perform an intermediate amount of swapping/smoothing.

            * ``2`` - Perform the greatest amount of swapping/smoothing.

            * ``3`` - Perform the greatest amount of swapping/smoothing, plus additional improvement techniques
              (default).

        Notes
        -----

        .. _VIMP_notes:

        :ref:`vimp` is useful for further improving a volume mesh created in Mechanical APDL ( :ref:`vmesh`
        ),
        especially quadratic tetrahedral element meshes.

        The command enables you to improve a given tetrahedral mesh by reducing the number of poorly-shaped
        tetrahedral elements (in particular, the number of sliver tetrahedral elements)--as well as the
        overall number of elements--in the mesh. It also improves the overall quality of the mesh.

        Regardless of the value of the ``CHGBND`` argument, boundary mid-nodes can be moved.


        When loads or constraints have been placed on boundary nodes or mid-nodes, and boundary mid-nodes
        are later moved, the program issues a warning message indicating that it will not update the loads
        or constraints.

        Even when ``CHGBND`` = 1, no boundary modification is performed on areas and lines that are not
        modifiable. For example, areas that are adjacent to other volumes or that contain shell elements, or
        lines that are not incident on modifiable areas, contain beam elements, or have line divisions
        specified for them ( :ref:`lesize` ).
        """
        command = f"VIMP,{vol},{chgbnd},{implevel}"
        return self.run(command, **kwargs)



    def vmesh(self, nv1: str = "", nv2: str = "", ninc: str = "", **kwargs):
        r"""Generates nodes and volume elements within volumes.

        Mechanical APDL Command: `VMESH <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_VMESH.html>`_

        Parameters
        ----------
        nv1 : str
            Mesh volumes from ``NV1`` to ``NV2`` (defaults to ``NV1`` ) in steps of ``NINC`` (defaults to
            1). If ``NV1`` = ALL, ``NV2`` and ``NINC`` are ignored and all selected volumes ( :ref:`vsel` )
            are meshed. If ``NV1`` = P, graphical picking is enabled and all remaining command fields are
            ignored (valid only in the GUI). A component name may also be substituted for ``NV1`` ( ``NV2``
            and ``NINC`` are ignored).

        nv2 : str
            Mesh volumes from ``NV1`` to ``NV2`` (defaults to ``NV1`` ) in steps of ``NINC`` (defaults to
            1). If ``NV1`` = ALL, ``NV2`` and ``NINC`` are ignored and all selected volumes ( :ref:`vsel` )
            are meshed. If ``NV1`` = P, graphical picking is enabled and all remaining command fields are
            ignored (valid only in the GUI). A component name may also be substituted for ``NV1`` ( ``NV2``
            and ``NINC`` are ignored).

        ninc : str
            Mesh volumes from ``NV1`` to ``NV2`` (defaults to ``NV1`` ) in steps of ``NINC`` (defaults to
            1). If ``NV1`` = ALL, ``NV2`` and ``NINC`` are ignored and all selected volumes ( :ref:`vsel` )
            are meshed. If ``NV1`` = P, graphical picking is enabled and all remaining command fields are
            ignored (valid only in the GUI). A component name may also be substituted for ``NV1`` ( ``NV2``
            and ``NINC`` are ignored).

        Notes
        -----

        .. _VMESH_notes:

        Missing nodes required for the generated elements are created and assigned the lowest available
        numbers ( :ref:`numstr` ). During a batch run and if elements already exist, a mesh abort will write
        an alternative database file ( :file:`File.DBE` ) for possible recovery.

        Tetrahedral mesh expansion ( :ref:`mopt`,TETEXPND, ``Value`` ) is supported for both the
        :ref:`vmesh` and :ref:`fvmesh` commands.
        """
        command = f"VMESH,{nv1},{nv2},{ninc}"
        return self.run(command, **kwargs)



    def vsweep(self, vnum: str = "", srca: str = "", trga: str = "", lsmo: int | str = "", **kwargs):
        r"""Fills an existing unmeshed volume with elements by sweeping the mesh from an adjacent area through
        the volume.

        Mechanical APDL Command: `VSWEEP <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_VSWEEP.html>`_

        Parameters
        ----------
        vnum : str
            Number identifying the volume that is to be meshed by :ref:`vsweep`. If ``VNUM`` = P, graphical
            picking is enabled, you will be prompted to choose the volume or volumes based on the setting of
            :ref:`extopt`,VSWE,AUTO. This argument is required.

            "ALL" is a valid input value that when selected sends all the selected volumes to the sweeper.
            If ``VNUM`` = ALL, each volume that can be swept will be and those not able to be swept will be
            unmeshed or meshed with tets depending upon the setting of :ref:`extopt`,VSWE,TETS.

            A component name is a valid input value. All volumes that are part of the specified component
            will be sent to the sweeper.

        srca : str
            Number identifying the source area. This is the area whose mesh will provide the pattern for the
            volume elements. (If you do not mesh the source area prior to volume sweeping, the program
            meshes it internally when you initiate volume sweeping.) The program sweeps the pattern of the
            area elements through the volume to create the mesh of volume elements. You cannot substitute a
            component name for ``SRCA``.

            This argument is optional. If ``VNUM`` = ALL or is a component containing more than one volume,
            ``SRCA`` is ignored. If ``SRCA`` is not provided or if it is ignored, :ref:`vsweep` attempts to
            automatically determine which area should be the target area.

        trga : str
            Number identifying the target area. This is the area that is opposite the source area specified
            by ``SRCA``. You cannot substitute a component name for ``TRGA``.

            This argument is optional. If ``VNUM`` = ALL or component containing more than one volume,
            ``TRGA`` is ignored. If ``TRGA`` is not provided or if it is ignored, :ref:`vsweep` attempts to
            automatically determine which area should be the target area.

        lsmo : int or str
            Value specifying whether the program should perform line smoothing during volume sweeping. (The
            value of this argument controls line smoothing for the :ref:`vsweep` command only; it has no effect on the setting of the :ref:`mopt` command's LSMO option.) This argument is optional.

            * ``0`` - Do not perform line smoothing. This is the default.

            * ``1`` - Always perform line smoothing. This setting is not recommended for large models due to
              speed considerations.

        Notes
        -----

        .. _VSWEEP_notes:

        If the source mesh consists of quadrilateral elements, the program fills the volume with hexahedral
        elements. If the source mesh consists of triangles, the program fills the volume with wedges. If the
        source mesh consists of a combination of quadrilaterals and triangles, the program fills the volume
        with a combination of hexahedral and wedge elements.

        In the past, you may have used the :ref:`vrotat`, :ref:`vext`, :ref:`voffst`, and/or :ref:`vdrag`
        commands to extrude a meshed area into a meshed volume. However, those commands create the volume
        and the volume mesh simultaneously. In contrast, the :ref:`vsweep` command is intended for use in an
        existing unmeshed volume. This makes :ref:`vsweep` particularly useful when you have imported a
        solid model that was created in another program, and you want to mesh it in Mechanical APDL.

        For related information, see the description of the :ref:`extopt` command (although :ref:`extopt`
        sets volume sweeping options, it does not affect element spacing). Also see the detailed discussion
        of volume sweeping in `Meshing Your Solid Model
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD7_5.html#modmeshvaidck31400>`_
         of the `Modeling and Meshing Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD14.html>`_.
        """
        command = f"VSWEEP,{vnum},{srca},{trga},{lsmo}"
        return self.run(command, **kwargs)


