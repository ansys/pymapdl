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

from ansys.mapdl.core._commands import CommandsBase


class Morphing(CommandsBase):

    def damorph(
        self, area: str = "", xline: str = "", rmshky: int | str = "", **kwargs
    ):
        r"""Move nodes in selected areas to conform to structural displacements.

        Mechanical APDL Command: `DAMORPH <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_DAMORPH.html>`_

        Parameters
        ----------
        area : str
            Non-structural area to which mesh movement (morph) applies. If ALL, apply morphing to all
            selected areas [ASEL]. If ``AREA`` = P, graphical picking is enabled. A component may be
            substituted for ``AREA``.

        xline : str
            Lines to be excluded from morphing. If ALL, exclude all selected lines [LSEL] from morphing. If
            ``XLINE`` = P, graphical picking is enabled. A component may be substituted for ``XLINE``. If
            ``XLINE`` is blank (default), allow morphing of nodes attached to lines of the selected areas (
            ``AREA`` ) which are not shared by unselected areas. See Notes for clarification.

        rmshky : int or str
            Remesh flag option:

            * ``0`` - Remesh the selected non-structural areas only if mesh morphing fails.

            * ``1`` - Remesh the selected non-structural areas and bypass mesh morphing.

            * ``2`` - Perform mesh morphing only and do not remesh.

        Notes
        -----

        .. _DAMORPH_notes:

        The selected areas should include only non-structural regions adjacent to structural regions.
        :ref:`damorph` will morph the non-structural areas to coincide with the deflections of the
        structural regions.

        Nodes in the structural regions move in accordance with computed displacements. Displacements from a
        structural analysis must be in the database prior to issuing :ref:`damorph`.

        By default, nodes attached to lines can move along the lines, or off the lines (if a line is
        interior to the selected areas). You can use ``XLINE`` to restrain nodes on certain lines.

        By default ( ``RMSHKEY`` = 0), :ref:`damorph` will remesh the selected non-structural areas entirely
        if a satisfactory morphed mesh cannot be provided.

        If boundary conditions and loads are applied directly to nodes and elements, the :ref:`damorph`
        command requires that these be removed before remeshing can take place.

        Exercise care with initial conditions defined by the :ref:`ic` command. Before a structural analysis
        is performed for a sequentially coupled analysis, the :ref:`damorph` command requires that initial
        conditions be removed from all null element type nodes in the non-structural regions. Use
        :ref:`icdele` to delete the initial conditions.
        """
        command = f"DAMORPH,{area},{xline},{rmshky}"
        return self.run(command, **kwargs)

    def demorph(self, elem: str = "", dimn: str = "", rmshky: int | str = "", **kwargs):
        r"""Move nodes in selected elements to conform to structural displacements.

        Mechanical APDL Command: `DEMORPH <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_DEMORPH.html>`_

        Parameters
        ----------
        elem : str
            Non-structural elements to which mesh movement (morph) applies. If ALL, apply morphing to all
            selected elements ( :ref:`esel`  ). If ELEM = P, graphical picking is enabled. A
            component may be substituted for ELEM.

        dimn : str
            Problem dimensionality. Use "2" for a 2D problem and "3" for a 3D problem (no default).

        rmshky : int or str
            Remesh flag option:

            * ``0`` - Remesh the selected non-structural regions only if mesh morphing fails.

            * ``1`` - Remesh the selected non-structural regions and bypass mesh morphing.

            * ``2`` - Perform mesh morphing only and do not remesh.

        Notes
        -----

        .. _DEMORPH_notes:

        The selected elements should include only non-structural regions adjacent to structural regions. The
        exterior nodes of the selected elements will usually be on the boundary of the region which will
        have node positions displaced. For ``DIMN`` = 2, elements must lie on a flat plane. The
        :ref:`demorph` command requires a single domain grouping of elements be provided (multiple domains
        of elements are not permitted). Exterior nodes will be assumed fixed (no nodes will be morphed)
        unless they coincide with structural nodes having nonzero displacements.

        Nodes in the structural regions move in accordance with computed displacements. Displacements from a
        structural analysis must be in the database prior to issuing :ref:`demorph`.

        By default ( ``RMSHKY`` = 0), :ref:`demorph` will remesh the selected non-structural regions
        entirely if a satisfactory morphed mesh cannot be provided.

        If boundary conditions and loads are applied directly to nodes and elements, the :ref:`demorph`
        command requires that these be removed before remeshing can take place.

        Exercise care with initial conditions defined by the :ref:`ic` command. Before a structural analysis
        is performed for a sequentially coupled analysis, the :ref:`demorph` command requires that initial
        conditions be removed from all null element type nodes in the non-structural regions. Use
        :ref:`icdele` to delete the initial conditions.
        """
        command = f"DEMORPH,{elem},{dimn},{rmshky}"
        return self.run(command, **kwargs)

    def dvmorph(
        self, volu: str = "", xarea: str = "", rmshky: int | str = "", **kwargs
    ):
        r"""Move nodes in selected volumes to conform to structural displacements.

        Mechanical APDL Command: `DVMORPH <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_DVMORPH.html>`_

        Parameters
        ----------
        volu : str
            Non-structural volume to which mesh movement (morph) applies. If ALL, apply morphing to all
            selected volumes ( :ref:`vsel` ). If ``VOLU`` = P, graphical picking is enabled. A component may
            be substituted for ``VOLU``.

        xarea : str
            Areas to be excluded from morphing. If ALL, exclude all selected areas ( :ref:`asel` ). If
            ``XAREA`` = P, graphical picking is enabled. A component may be substituted for ``XAREA``. If
            ``XAREA`` is blank (default), allow morphing of nodes attached to areas of the selected volumes
            ( ``VOLU`` ) which are not shared by unselected volumes. (See Notes for clarification).

        rmshky : int or str
            Remesh flag option:

            * ``0`` - Remesh the selected non-structural volumes only if mesh morphing fails.

            * ``1`` - Remesh the selected non-structural volumes and bypass mesh morphing.

            * ``2`` - Perform mesh morphing only and do not remesh.

        Notes
        -----

        .. _DVMORPH_notes:

        The selected volumes should include only non-structural regions adjacent to structural regions.
        DVMORPH will morph the non-structural volumes to coincide with the deflections of the structural
        regions.

        Nodes in the structural regions move in accordance with computed displacements. Displacements from a
        structural analysis must be in the database prior to issuing DVMORPH.

        By default, nodes attached to areas can move along the areas. You can use ``XAREA`` to restrain
        nodes on certain areas.

        By default ( ``RMSHKY`` = 0), DVMORPH will remesh the selected non-structural volumes entirely if a
        satisfactory morphed mesh cannot be provided.

        If boundary conditions and loads are applied directly to nodes and elements, the DVMORPH command
        requires that these be removed before remeshing can take place.

        Exercise care with initial conditions defined by the :ref:`ic` command. Before a structural analysis
        is performed for a sequentially coupled analysis, the DVMORPH command requires that initial
        conditions be removed from all null element type nodes in the non-structural regions. Use
        :ref:`icdele` to delete the initial conditions.
        """
        command = f"DVMORPH,{volu},{xarea},{rmshky}"
        return self.run(command, **kwargs)

    def morph(
        self,
        option: str = "",
        remeshopt: str = "",
        elemset: str = "",
        armax: str = "",
        voch: str = "",
        arch: str = "",
        step: str = "",
        time: str = "",
        stropt: str = "",
        **kwargs,
    ):
        r"""Specifies morphing and remeshing controls.

        Mechanical APDL Command: `MORPH <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MORPH.html>`_

        Parameters
        ----------
        option : str

            * ``OFF`` - Turns off morphing for field elements (default).

            * ``ON`` - Turns on morphing for field elements.

        remeshopt : str

            * ``OFF`` - Do not remesh (default).

            * ``ON`` - Remesh when element qualities fall below values specified by ``ARMAX``, ``VOCH``, or
              ``ARCH`` as explained below. Valid only when ``Option`` is ON.

        elemset : str

            * ``ALL`` - Remesh all selected elements if the quality of the worst defined element falls below any
              quality requirement (default when ``Remeshopt`` = ON).

            * ``CompName`` - Specify a component name, up to 256 characters. All elements included in this
              component name are remeshed if the quality of the worst element falls below any quality requirement.

        armax : str
            The maximum allowable element generalized aspect ratio. Defaults to 5.

        voch : str
            The maximum allowable change of element size (area or volume). Defaults to 3.

        arch : str
            The maximum allowable element aspect ratio change. Defaults to 3.

        step : str
            The frequency of element quality checking, based on time steps. A quality check takes place at
            the intervals defined by ``STEP``. Defaults to 1 (quality check at every step).

        time : str
            A quality check takes place at the time point specified. Defaults to -1 (a quality check at
            every time point).

        stropt : str
            * ``NO`` - There are no structural elements in the model (default).

            * ``YES`` - There are structural elements in the model and the morphing happens after the structural
              solution.

        Notes
        -----

        .. _MORPH_notes:

        :ref:`morph` is applicable to any non-structural field analysis. It activates displacement degrees
        of freedom for non-structural elements so that boundary conditions may be placed on the field mesh
        to constrain the movement of the non-structural mesh during morphing. It morphs the non-structural
        mesh using displacements transferred at the surface interface between the structural field and the
        non-structural field. The displacements of non-structural elements are mesh displacements to avoid
        mesh distortion, but have no physical meaning except at the interface. :ref:`morph` does not support
        surface, link, or shell elements, or any element shape other than triangles, quads, tets, and
        bricks. Morphed fields must be in the global Cartesian system ( :ref:`csys` = 0).

        If ``StrOpt`` = YES, the following non-structural element types will be morphed:

        * Acoustic: ``FLUID30``, ``FLUID220``, ``FLUID221``, ``FLUID243``, ``FLUID244``,

        * Electrostatic ``PLANE121``, ``SOLID122``, and ``SOLID123``,

        * Electric ``PLANE230``, ``SOLID231``, and ``SOLID232``,

        * Electromagnetic ``PLANE233``, ``SOLID236``, and ``SOLID237``,

        * Thermal ``PLANE35``, ``PLANE55``, ``PLANE77``, ``PLANE292``, ``PLANE293``, ``SOLID70``,
          ``SOLID87``, ``SOLID90``, ``SOLID278``, ``SOLID279``, and ``SOLID291``,

        * Diffusion ``PLANE238``, ``SOLID239``, and ``SOLID240``,

        * Coupled-field ``PLANE222``, ``PLANE223``, ``SOLID225``, ``SOLID226``, and ``SOLID227`` with no
          structural degrees of freedom.

        The following structural elements types are supported by ``StrOpt`` = YES:

        * ``PLANE182``, ``PLANE183``, ``SOLID185``, ``SOLID186``, ``SOLID187``, ``SOLSH190``,

        * Coupled-field ``PLANE222``, ``PLANE223``, ``SOLID225``, ``SOLID226``, and ``SOLID227`` with
          structural degrees of freedom.

        After each remesh, new databases and results files are written with the extensions :file:`.rth0n`
        and :file:`.db0n`, where ``n`` is the remesh file number ( :file:`FieldName.rth01`,
        :file:`FieldName.rth02`,... and :file:`FieldName.db01`, :file:`FieldName.db02`, etc.). The original
        database file is :file:`FieldName.dbo`. The :file:`FieldName.db01`, :file:`FieldName.db02`, etc.
        files have elements that are detached from the solid model.

        Remeshing has the following restrictions:

        * Valid only for the electrostatic elements ( ``PLANE121``, ``SOLID122``, and ``SOLID123`` )

        * Limited to triangle (2D) and tetrahedral (3D) options of these elements

        * No body loads allowed in the interior nodes of the remeshing domain

        * Nodes on the boundary cannot be remeshed; remeshing will not work if morphing failed on the
          surface nodes

        * Not suitable for extreme area or volume changes

        This command is also valid in SOLUTION.
        """
        command = f"MORPH,{option},,{remeshopt},{elemset},{armax},{voch},{arch},{step},{time},{stropt}"
        return self.run(command, **kwargs)
