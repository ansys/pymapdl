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

from ansys.mapdl.core._commands import parse


class Booleans:

    def aadd(
        self,
        na1: str = "",
        na2: str = "",
        na3: str = "",
        na4: str = "",
        na5: str = "",
        na6: str = "",
        na7: str = "",
        na8: str = "",
        na9: str = "",
        **kwargs,
    ):
        r"""Adds separate areas to create a single area.

        Mechanical APDL Command: `AADD <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_AADD.html>`_

        Parameters
        ----------
        na1 : str
            Numbers of areas to be added. If ``NA1`` = ALL, add all selected areas and ignore ``NA2`` to
            ``NA9``. If ``NA1`` = P, graphical picking is enabled and all remaining arguments are ignored
            (valid only in the GUI). A component name may also be substituted for ``NA1``.

        na2 : str
            Numbers of areas to be added. If ``NA1`` = ALL, add all selected areas and ignore ``NA2`` to
            ``NA9``. If ``NA1`` = P, graphical picking is enabled and all remaining arguments are ignored
            (valid only in the GUI). A component name may also be substituted for ``NA1``.

        na3 : str
            Numbers of areas to be added. If ``NA1`` = ALL, add all selected areas and ignore ``NA2`` to
            ``NA9``. If ``NA1`` = P, graphical picking is enabled and all remaining arguments are ignored
            (valid only in the GUI). A component name may also be substituted for ``NA1``.

        na4 : str
            Numbers of areas to be added. If ``NA1`` = ALL, add all selected areas and ignore ``NA2`` to
            ``NA9``. If ``NA1`` = P, graphical picking is enabled and all remaining arguments are ignored
            (valid only in the GUI). A component name may also be substituted for ``NA1``.

        na5 : str
            Numbers of areas to be added. If ``NA1`` = ALL, add all selected areas and ignore ``NA2`` to
            ``NA9``. If ``NA1`` = P, graphical picking is enabled and all remaining arguments are ignored
            (valid only in the GUI). A component name may also be substituted for ``NA1``.

        na6 : str
            Numbers of areas to be added. If ``NA1`` = ALL, add all selected areas and ignore ``NA2`` to
            ``NA9``. If ``NA1`` = P, graphical picking is enabled and all remaining arguments are ignored
            (valid only in the GUI). A component name may also be substituted for ``NA1``.

        na7 : str
            Numbers of areas to be added. If ``NA1`` = ALL, add all selected areas and ignore ``NA2`` to
            ``NA9``. If ``NA1`` = P, graphical picking is enabled and all remaining arguments are ignored
            (valid only in the GUI). A component name may also be substituted for ``NA1``.

        na8 : str
            Numbers of areas to be added. If ``NA1`` = ALL, add all selected areas and ignore ``NA2`` to
            ``NA9``. If ``NA1`` = P, graphical picking is enabled and all remaining arguments are ignored
            (valid only in the GUI). A component name may also be substituted for ``NA1``.

        na9 : str
            Numbers of areas to be added. If ``NA1`` = ALL, add all selected areas and ignore ``NA2`` to
            ``NA9``. If ``NA1`` = P, graphical picking is enabled and all remaining arguments are ignored
            (valid only in the GUI). A component name may also be substituted for ``NA1``.

        Notes
        -----

        .. _AADD_notes:

        The areas must be coplanar. The original areas (and their corresponding lines and keypoints) will be
        deleted by default. See the :ref:`boptn` command for the options available to Boolean operations.
        Element attributes and solid model boundary conditions assigned to the original entities will not be
        transferred to the new entities generated. Concatenated entities are not valid with this command.

        Examples
        --------
        Generate two areas and combine them.

        >>> a1 = mapdl.rectng(2.5, 3.5, 0, 10)
        >>> a2 = mapdl.cyl4(0, 10, 2.5, 0, 3.5, 90)
        >>> a_comb = mapdl.aadd(a1, a2)
        >>> a_comb
        3
        """
        command = f"AADD,{na1},{na2},{na3},{na4},{na5},{na6},{na7},{na8},{na9}"
        return parse.parse_output_areas(self.run(command, **kwargs))

    def aglue(
        self,
        na1: str = "",
        na2: str = "",
        na3: str = "",
        na4: str = "",
        na5: str = "",
        na6: str = "",
        na7: str = "",
        na8: str = "",
        na9: str = "",
        **kwargs,
    ):
        r"""Generates new areas by "gluing" areas.

        Mechanical APDL Command: `AGLUE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_AGLUE.html>`_

        Parameters
        ----------
        na1 : str
            Numbers of the areas to be glued. If ``NA1`` = ALL, all selected areas will be glued ( ``NA2``
            to ``NA9`` will be ignored). If ``NA1`` = P, graphical picking is enabled and all remaining
            arguments are ignored (valid only in the GUI). A component name may also be substituted for
            ``NA1``.

        na2 : str
            Numbers of the areas to be glued. If ``NA1`` = ALL, all selected areas will be glued ( ``NA2``
            to ``NA9`` will be ignored). If ``NA1`` = P, graphical picking is enabled and all remaining
            arguments are ignored (valid only in the GUI). A component name may also be substituted for
            ``NA1``.

        na3 : str
            Numbers of the areas to be glued. If ``NA1`` = ALL, all selected areas will be glued ( ``NA2``
            to ``NA9`` will be ignored). If ``NA1`` = P, graphical picking is enabled and all remaining
            arguments are ignored (valid only in the GUI). A component name may also be substituted for
            ``NA1``.

        na4 : str
            Numbers of the areas to be glued. If ``NA1`` = ALL, all selected areas will be glued ( ``NA2``
            to ``NA9`` will be ignored). If ``NA1`` = P, graphical picking is enabled and all remaining
            arguments are ignored (valid only in the GUI). A component name may also be substituted for
            ``NA1``.

        na5 : str
            Numbers of the areas to be glued. If ``NA1`` = ALL, all selected areas will be glued ( ``NA2``
            to ``NA9`` will be ignored). If ``NA1`` = P, graphical picking is enabled and all remaining
            arguments are ignored (valid only in the GUI). A component name may also be substituted for
            ``NA1``.

        na6 : str
            Numbers of the areas to be glued. If ``NA1`` = ALL, all selected areas will be glued ( ``NA2``
            to ``NA9`` will be ignored). If ``NA1`` = P, graphical picking is enabled and all remaining
            arguments are ignored (valid only in the GUI). A component name may also be substituted for
            ``NA1``.

        na7 : str
            Numbers of the areas to be glued. If ``NA1`` = ALL, all selected areas will be glued ( ``NA2``
            to ``NA9`` will be ignored). If ``NA1`` = P, graphical picking is enabled and all remaining
            arguments are ignored (valid only in the GUI). A component name may also be substituted for
            ``NA1``.

        na8 : str
            Numbers of the areas to be glued. If ``NA1`` = ALL, all selected areas will be glued ( ``NA2``
            to ``NA9`` will be ignored). If ``NA1`` = P, graphical picking is enabled and all remaining
            arguments are ignored (valid only in the GUI). A component name may also be substituted for
            ``NA1``.

        na9 : str
            Numbers of the areas to be glued. If ``NA1`` = ALL, all selected areas will be glued ( ``NA2``
            to ``NA9`` will be ignored). If ``NA1`` = P, graphical picking is enabled and all remaining
            arguments are ignored (valid only in the GUI). A component name may also be substituted for
            ``NA1``.

        Notes
        -----

        .. _AGLUE_notes:

        Use of the :ref:`aglue` command generates new areas by "gluing" input areas. The glue operation
        redefines the input areas so that they share lines along their common boundaries. The new areas
        encompass the same geometry as the original areas. This operation is only valid if the intersection
        of the input areas are lines along the boundaries of those areas. See the `Modeling and Meshing
        Guide <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD14.html>`_ for an
        illustration. See the :ref:`boptn` command for an explanation of the options available to Boolean
        operations. Element attributes and solid model boundary conditions assigned to the original entities
        will not be transferred to new entities generated.

        The :ref:`aglue` command results in the merging of lines and keypoints at the common area
        boundaries. The lines and keypoints of the lower numbered area will be kept. This means one must be
        aware of area numbering when multiple :ref:`aglue` commands are applied to avoid any "ungluing" of
        geometry.
        """
        command = f"AGLUE,{na1},{na2},{na3},{na4},{na5},{na6},{na7},{na8},{na9}"
        return self.run(command, **kwargs)

    def aina(
        self,
        na1: str = "",
        na2: str = "",
        na3: str = "",
        na4: str = "",
        na5: str = "",
        na6: str = "",
        na7: str = "",
        na8: str = "",
        na9: str = "",
        **kwargs,
    ):
        r"""Finds the intersection of areas.

        Mechanical APDL Command: `AINA <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_AINA.html>`_

        Parameters
        ----------
        na1 : str
            Numbers of areas to be intersected. If ``NA1`` = ALL, ``NA2`` to ``NA9`` are ignored and the
            intersection of all selected areas is found. If ``NA1`` = P, graphical picking is enabled and
            all remaining arguments are ignored (valid only in the GUI). A component name may also be
            substituted for ``NA1``.

        na2 : str
            Numbers of areas to be intersected. If ``NA1`` = ALL, ``NA2`` to ``NA9`` are ignored and the
            intersection of all selected areas is found. If ``NA1`` = P, graphical picking is enabled and
            all remaining arguments are ignored (valid only in the GUI). A component name may also be
            substituted for ``NA1``.

        na3 : str
            Numbers of areas to be intersected. If ``NA1`` = ALL, ``NA2`` to ``NA9`` are ignored and the
            intersection of all selected areas is found. If ``NA1`` = P, graphical picking is enabled and
            all remaining arguments are ignored (valid only in the GUI). A component name may also be
            substituted for ``NA1``.

        na4 : str
            Numbers of areas to be intersected. If ``NA1`` = ALL, ``NA2`` to ``NA9`` are ignored and the
            intersection of all selected areas is found. If ``NA1`` = P, graphical picking is enabled and
            all remaining arguments are ignored (valid only in the GUI). A component name may also be
            substituted for ``NA1``.

        na5 : str
            Numbers of areas to be intersected. If ``NA1`` = ALL, ``NA2`` to ``NA9`` are ignored and the
            intersection of all selected areas is found. If ``NA1`` = P, graphical picking is enabled and
            all remaining arguments are ignored (valid only in the GUI). A component name may also be
            substituted for ``NA1``.

        na6 : str
            Numbers of areas to be intersected. If ``NA1`` = ALL, ``NA2`` to ``NA9`` are ignored and the
            intersection of all selected areas is found. If ``NA1`` = P, graphical picking is enabled and
            all remaining arguments are ignored (valid only in the GUI). A component name may also be
            substituted for ``NA1``.

        na7 : str
            Numbers of areas to be intersected. If ``NA1`` = ALL, ``NA2`` to ``NA9`` are ignored and the
            intersection of all selected areas is found. If ``NA1`` = P, graphical picking is enabled and
            all remaining arguments are ignored (valid only in the GUI). A component name may also be
            substituted for ``NA1``.

        na8 : str
            Numbers of areas to be intersected. If ``NA1`` = ALL, ``NA2`` to ``NA9`` are ignored and the
            intersection of all selected areas is found. If ``NA1`` = P, graphical picking is enabled and
            all remaining arguments are ignored (valid only in the GUI). A component name may also be
            substituted for ``NA1``.

        na9 : str
            Numbers of areas to be intersected. If ``NA1`` = ALL, ``NA2`` to ``NA9`` are ignored and the
            intersection of all selected areas is found. If ``NA1`` = P, graphical picking is enabled and
            all remaining arguments are ignored (valid only in the GUI). A component name may also be
            substituted for ``NA1``.

        Notes
        -----

        .. _AINA_notes:

        Finds the common (not pairwise) intersection of areas. The common intersection is defined as the
        regions shared (in common) by **all** areas listed on this command. New areas will be generated
        where the original areas intersect. If the
        regions of intersection are only lines, new lines will be generated instead. See the `Modeling and
        Meshing Guide <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD14.html>`_
        for an
        illustration. See the :ref:`boptn` command for the options available to Boolean operations. Element
        attributes and solid model boundary conditions assigned to the original entities will not be
        transferred to the new entities generated.
        """
        command = f"AINA,{na1},{na2},{na3},{na4},{na5},{na6},{na7},{na8},{na9}"
        return self.run(command, **kwargs)

    def ainp(
        self,
        na1: str = "",
        na2: str = "",
        na3: str = "",
        na4: str = "",
        na5: str = "",
        na6: str = "",
        na7: str = "",
        na8: str = "",
        na9: str = "",
        **kwargs,
    ):
        r"""Finds the pairwise intersection of areas.

        Mechanical APDL Command: `AINP <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_AINP.html>`_

        Parameters
        ----------
        na1 : str
            Numbers of areas to be intersected pairwise. If ``NA1`` = ALL, ``NA2`` to ``NA9`` are ignored
            and the pairwise intersection of all selected areas is found. If ``NA1`` = P, graphical picking
            is enabled and all remaining arguments are ignored (valid only in the GUI). A component name may
            be substituted for ``NA1``.

        na2 : str
            Numbers of areas to be intersected pairwise. If ``NA1`` = ALL, ``NA2`` to ``NA9`` are ignored
            and the pairwise intersection of all selected areas is found. If ``NA1`` = P, graphical picking
            is enabled and all remaining arguments are ignored (valid only in the GUI). A component name may
            be substituted for ``NA1``.

        na3 : str
            Numbers of areas to be intersected pairwise. If ``NA1`` = ALL, ``NA2`` to ``NA9`` are ignored
            and the pairwise intersection of all selected areas is found. If ``NA1`` = P, graphical picking
            is enabled and all remaining arguments are ignored (valid only in the GUI). A component name may
            be substituted for ``NA1``.

        na4 : str
            Numbers of areas to be intersected pairwise. If ``NA1`` = ALL, ``NA2`` to ``NA9`` are ignored
            and the pairwise intersection of all selected areas is found. If ``NA1`` = P, graphical picking
            is enabled and all remaining arguments are ignored (valid only in the GUI). A component name may
            be substituted for ``NA1``.

        na5 : str
            Numbers of areas to be intersected pairwise. If ``NA1`` = ALL, ``NA2`` to ``NA9`` are ignored
            and the pairwise intersection of all selected areas is found. If ``NA1`` = P, graphical picking
            is enabled and all remaining arguments are ignored (valid only in the GUI). A component name may
            be substituted for ``NA1``.

        na6 : str
            Numbers of areas to be intersected pairwise. If ``NA1`` = ALL, ``NA2`` to ``NA9`` are ignored
            and the pairwise intersection of all selected areas is found. If ``NA1`` = P, graphical picking
            is enabled and all remaining arguments are ignored (valid only in the GUI). A component name may
            be substituted for ``NA1``.

        na7 : str
            Numbers of areas to be intersected pairwise. If ``NA1`` = ALL, ``NA2`` to ``NA9`` are ignored
            and the pairwise intersection of all selected areas is found. If ``NA1`` = P, graphical picking
            is enabled and all remaining arguments are ignored (valid only in the GUI). A component name may
            be substituted for ``NA1``.

        na8 : str
            Numbers of areas to be intersected pairwise. If ``NA1`` = ALL, ``NA2`` to ``NA9`` are ignored
            and the pairwise intersection of all selected areas is found. If ``NA1`` = P, graphical picking
            is enabled and all remaining arguments are ignored (valid only in the GUI). A component name may
            be substituted for ``NA1``.

        na9 : str
            Numbers of areas to be intersected pairwise. If ``NA1`` = ALL, ``NA2`` to ``NA9`` are ignored
            and the pairwise intersection of all selected areas is found. If ``NA1`` = P, graphical picking
            is enabled and all remaining arguments are ignored (valid only in the GUI). A component name may
            be substituted for ``NA1``.

        Notes
        -----

        .. _AINP_notes:

        Finds the pairwise intersection of areas. The pairwise intersection is defined as all regions shared
        by any two or more areas listed on this command. New areas will be generated where the original
        areas intersect pairwise. If the regions of pairwise intersection are only lines, new lines will be
        generated. See the `Modeling and Meshing Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD14.html>`_ for an
        illustration. See the :ref:`boptn` command for the options
        available to Boolean operations. Element attributes and solid model boundary conditions assigned to
        the original entities will not be transferred to the new entities generated.
        """
        command = f"AINP,{na1},{na2},{na3},{na4},{na5},{na6},{na7},{na8},{na9}"
        return self.run(command, **kwargs)

    def ainv(self, na: str = "", nv: str = "", **kwargs):
        r"""Finds the intersection of an area with a volume.

        Mechanical APDL Command: `AINV <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_AINV.html>`_

        Parameters
        ----------
        na : str
            Number of area to be intersected. If P, graphical picking is enabled and all remaining arguments
            are ignored (valid only in the GUI).

        nv : str
            Number of volume to be intersected.

        Notes
        -----

        .. _AINV_notes:

        New areas will be generated where the areas intersect the volumes. If the regions of intersection
        are only lines, new lines will be generated instead. See the `Modeling and Meshing Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD14.html>`_ for an
        illustration. See the
        :ref:`boptn` command for the options available to Boolean operations. Element attributes and solid
        model boundary conditions assigned to the original entities will not be transferred to the new
        entities generated.
        """
        command = f"AINV,{na},{nv}"
        return self.run(command, **kwargs)

    def aovlap(
        self,
        na1: str = "",
        na2: str = "",
        na3: str = "",
        na4: str = "",
        na5: str = "",
        na6: str = "",
        na7: str = "",
        na8: str = "",
        na9: str = "",
        **kwargs,
    ):
        r"""Overlaps areas.

        Mechanical APDL Command: `AOVLAP <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_AOVLAP.html>`_

        Parameters
        ----------
        na1 : str
            Numbers of areas to be operated on. If ``NA1`` = ALL, use all selected areas and ignore ``NA2``
            to ``NA9``. If ``NA1`` = P, graphical picking is enabled and all remaining arguments are ignored
            (valid only in the GUI). A component name may also be substituted for ``NA1``.

        na2 : str
            Numbers of areas to be operated on. If ``NA1`` = ALL, use all selected areas and ignore ``NA2``
            to ``NA9``. If ``NA1`` = P, graphical picking is enabled and all remaining arguments are ignored
            (valid only in the GUI). A component name may also be substituted for ``NA1``.

        na3 : str
            Numbers of areas to be operated on. If ``NA1`` = ALL, use all selected areas and ignore ``NA2``
            to ``NA9``. If ``NA1`` = P, graphical picking is enabled and all remaining arguments are ignored
            (valid only in the GUI). A component name may also be substituted for ``NA1``.

        na4 : str
            Numbers of areas to be operated on. If ``NA1`` = ALL, use all selected areas and ignore ``NA2``
            to ``NA9``. If ``NA1`` = P, graphical picking is enabled and all remaining arguments are ignored
            (valid only in the GUI). A component name may also be substituted for ``NA1``.

        na5 : str
            Numbers of areas to be operated on. If ``NA1`` = ALL, use all selected areas and ignore ``NA2``
            to ``NA9``. If ``NA1`` = P, graphical picking is enabled and all remaining arguments are ignored
            (valid only in the GUI). A component name may also be substituted for ``NA1``.

        na6 : str
            Numbers of areas to be operated on. If ``NA1`` = ALL, use all selected areas and ignore ``NA2``
            to ``NA9``. If ``NA1`` = P, graphical picking is enabled and all remaining arguments are ignored
            (valid only in the GUI). A component name may also be substituted for ``NA1``.

        na7 : str
            Numbers of areas to be operated on. If ``NA1`` = ALL, use all selected areas and ignore ``NA2``
            to ``NA9``. If ``NA1`` = P, graphical picking is enabled and all remaining arguments are ignored
            (valid only in the GUI). A component name may also be substituted for ``NA1``.

        na8 : str
            Numbers of areas to be operated on. If ``NA1`` = ALL, use all selected areas and ignore ``NA2``
            to ``NA9``. If ``NA1`` = P, graphical picking is enabled and all remaining arguments are ignored
            (valid only in the GUI). A component name may also be substituted for ``NA1``.

        na9 : str
            Numbers of areas to be operated on. If ``NA1`` = ALL, use all selected areas and ignore ``NA2``
            to ``NA9``. If ``NA1`` = P, graphical picking is enabled and all remaining arguments are ignored
            (valid only in the GUI). A component name may also be substituted for ``NA1``.

        Notes
        -----

        .. _AOVLAP_notes:

        Generates new areas which encompass the geometry of all the input areas. The new areas are defined
        by the regions of intersection of the input areas, and by the complementary (non-intersecting)
        regions. See `Solid Modeling
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD5_10.html>`_   in
        the `Modeling and Meshing Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD14.html>`_ for an
        illustration. This operation is only valid when the region of intersection is an
        area. See the :ref:`boptn` command for an explanation of the options available to Boolean
        operations. Element attributes and solid model boundary conditions assigned to the original entities
        will not be transferred to the new entities generated.
        """
        command = f"AOVLAP,{na1},{na2},{na3},{na4},{na5},{na6},{na7},{na8},{na9}"
        return self.run(command, **kwargs)

    def aptn(
        self,
        na1: str = "",
        na2: str = "",
        na3: str = "",
        na4: str = "",
        na5: str = "",
        na6: str = "",
        na7: str = "",
        na8: str = "",
        na9: str = "",
        **kwargs,
    ):
        r"""Partitions areas.

        Mechanical APDL Command: `APTN <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_APTN.html>`_

        Parameters
        ----------
        na1 : str
            Numbers of areas to be operated on. If ``NA1`` = ALL, ``NA2`` to ``NA9`` are ignored and all
            selected areas are used. If ``NA1`` = P, graphical picking is enabled and all remaining
            arguments are ignored (valid only in the GUI). A component name may be substituted for ``NA1``.

        na2 : str
            Numbers of areas to be operated on. If ``NA1`` = ALL, ``NA2`` to ``NA9`` are ignored and all
            selected areas are used. If ``NA1`` = P, graphical picking is enabled and all remaining
            arguments are ignored (valid only in the GUI). A component name may be substituted for ``NA1``.

        na3 : str
            Numbers of areas to be operated on. If ``NA1`` = ALL, ``NA2`` to ``NA9`` are ignored and all
            selected areas are used. If ``NA1`` = P, graphical picking is enabled and all remaining
            arguments are ignored (valid only in the GUI). A component name may be substituted for ``NA1``.

        na4 : str
            Numbers of areas to be operated on. If ``NA1`` = ALL, ``NA2`` to ``NA9`` are ignored and all
            selected areas are used. If ``NA1`` = P, graphical picking is enabled and all remaining
            arguments are ignored (valid only in the GUI). A component name may be substituted for ``NA1``.

        na5 : str
            Numbers of areas to be operated on. If ``NA1`` = ALL, ``NA2`` to ``NA9`` are ignored and all
            selected areas are used. If ``NA1`` = P, graphical picking is enabled and all remaining
            arguments are ignored (valid only in the GUI). A component name may be substituted for ``NA1``.

        na6 : str
            Numbers of areas to be operated on. If ``NA1`` = ALL, ``NA2`` to ``NA9`` are ignored and all
            selected areas are used. If ``NA1`` = P, graphical picking is enabled and all remaining
            arguments are ignored (valid only in the GUI). A component name may be substituted for ``NA1``.

        na7 : str
            Numbers of areas to be operated on. If ``NA1`` = ALL, ``NA2`` to ``NA9`` are ignored and all
            selected areas are used. If ``NA1`` = P, graphical picking is enabled and all remaining
            arguments are ignored (valid only in the GUI). A component name may be substituted for ``NA1``.

        na8 : str
            Numbers of areas to be operated on. If ``NA1`` = ALL, ``NA2`` to ``NA9`` are ignored and all
            selected areas are used. If ``NA1`` = P, graphical picking is enabled and all remaining
            arguments are ignored (valid only in the GUI). A component name may be substituted for ``NA1``.

        na9 : str
            Numbers of areas to be operated on. If ``NA1`` = ALL, ``NA2`` to ``NA9`` are ignored and all
            selected areas are used. If ``NA1`` = P, graphical picking is enabled and all remaining
            arguments are ignored (valid only in the GUI). A component name may be substituted for ``NA1``.

        Notes
        -----

        .. _APTN_notes:

        Partitions areas that intersect. This command is similar to the combined functionality of the
        :ref:`asba` and :ref:`aovlap` commands. If the intersection of two or more areas is an area (that
        is, planar), new areas will be created with boundaries that conform to the area of intersection and
        to the boundaries of the non-intersecting portions of the input areas ( :ref:`aovlap` ). If the
        intersection is a line (that is, not planar), the areas will be subtracted, or divided, along the
        line(s) of intersection ( :ref:`asba` ). Both types of intersection can occur during a single
        :ref:`aptn` operation. Areas that do not intersect will not be modified. See the `Modeling and
        Meshing Guide <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD14.html>`_
        for an
        illustration. See the :ref:`boptn` command for an explanation of the options available to Boolean
        operations. Element attributes and solid model boundary conditions assigned to the original entities
        will not be transferred to the new entities generated.
        """
        command = f"APTN,{na1},{na2},{na3},{na4},{na5},{na6},{na7},{na8},{na9}"
        return self.run(command, **kwargs)

    def asba(
        self,
        na1: str = "",
        na2: str = "",
        sepo: str = "",
        keep1: str = "",
        keep2: str = "",
        **kwargs,
    ):
        r"""Subtracts areas from areas.

        Mechanical APDL Command: `ASBA <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ASBA.html>`_

        Parameters
        ----------
        na1 : str
            Area (or areas, if picking is used) to be subtracted from. If ALL, use all selected areas. Areas
            specified in this argument are not available for use in the ``NA2`` argument. If P, graphical
            picking is enabled (valid only in the GUI) and remaining fields are ignored. A component name
            may also be substituted for ``NA1``.

        na2 : str
            Area (or areas, if picking is used) to subtract. If ALL, use all selected areas (except those
            included in the ``NA1`` argument). A component name may also be substituted for ``NA2``.

        sepo : str
            Behavior if the intersection of the ``NA1`` areas and the ``NA2`` areas is a line or lines:

            * ``(blank)`` - The resulting areas will share line(s) where they touch.

            * ``SEPO`` - The resulting areas will have separate, but coincident line(s) where they touch.

        keep1 : str
            Specifies whether ``NA1`` areas are to be deleted:

            * ``(blank)`` - Use the setting of KEEP on the :ref:`boptn` command.

            * ``DELETE`` - Delete ``NA1`` areas after :ref:`asba` operation (override :ref:`boptn` command
              settings).

            * ``KEEP`` - Keep ``NA1`` areas after :ref:`asba` operation (override :ref:`boptn` command
              settings).

        keep2 : str
            Specifies whether ``NA2`` areas are to be deleted:

            * ``(blank)`` - Use the setting of KEEP on the :ref:`boptn` command.

            * ``DELETE`` - Delete ``NA2`` areas after :ref:`asba` operation (override :ref:`boptn` command
              settings).

            * ``KEEP`` - Keep ``NA2`` areas after :ref:`asba` operation (override :ref:`boptn` command
              settings).

        Returns
        -------
        int
            Area number of the new area (if applicable)

        Notes
        -----

        .. _ASBA_notes:

        Generates new areas by subtracting the regions common to both ``NA1`` and ``NA2`` areas (the
        intersection) from the ``NA1`` areas. The intersection can be an area(s) or line(s). If the
        intersection is a line and ``SEPO`` is blank, the ``NA1`` area is divided at the line and the
        resulting areas will be connected, sharing a common line where they touch. If ``SEPO`` is set to
        SEPO, ``NA1`` is divided into two unconnected areas with separate lines where they touch. See `Solid
        Modeling <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD5_10.html>`_
         in the `Modeling and Meshing Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD14.html>`_ for an
        illustration. See the :ref:`boptn` command for an explanation of the
        options available to Boolean operations. Element attributes and solid model boundary conditions
        assigned to the original entities will not be transferred to the new entities generated.
        :ref:`asba`,ALL,ALL will have no effect since all the areas (in ``NA1`` ) will be unavailable as
        ``NA2`` areas.

        Examples
        --------
        Subtract a 0.5 x 0.5 rectangle from a 1 x 1 rectangle.

        >>> anum0 = mapdl.blc4(0, 0, 1, 1)
        >>> anum1 = mapdl.blc4(0.25, 0.25, 0.5, 0.5)
        >>> aout = mapdl.asba(anum0, anum1)
        >>> aout
        3
        """
        command = f"ASBA,{na1},{na2},{sepo},{keep1},{keep2}"
        return parse.parse_output_volume_area(self.run(command, **kwargs))

    def asbl(
        self, na: str = "", nl: str = "", keepa: str = "", keepl: str = "", **kwargs
    ):
        r"""Subtracts lines from areas.

        Mechanical APDL Command: `ASBL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ASBL.html>`_

        Parameters
        ----------
        na : str
            Area (or areas, if picking is used) to be subtracted from. If ALL, use all selected areas. If P,
            graphical picking is enabled (valid only in the GUI) and remaining fields are ignored. A
            component name may also be substituted for ``NA``.

        nl : str
            Line (or lines, if picking is used) to subtract. If ALL, use all selected lines. A component
            name may also be substituted for ``NL``.

        keepa : str
            Specifies whether ``NA`` areas are to be deleted:

            * ``(blank)`` - Use the setting of KEEP on the :ref:`boptn` command.

            * ``DELETE`` - Delete ``NA`` areas after :ref:`asbl` operation (override :ref:`boptn` command
              settings).

            * ``KEEP`` - Keep ``NA`` areas after :ref:`asbl` operation (override :ref:`boptn` command settings).

        keepl : str
            Specifies whether ``NL`` lines are to be deleted:

            * ``(blank)`` - Use the setting of KEEP on the :ref:`boptn` command.

            * ``DELETE`` - Delete ``NL`` lines after :ref:`asbl` operation (override :ref:`boptn` command
              settings).

            * ``KEEP`` - Keep ``NL`` lines after :ref:`asbl` operation (override :ref:`boptn` command settings).

        Notes
        -----

        .. _ASBL_notes:

        Generates new areas by subtracting the regions common to both the areas and lines (the intersection)
        from the ``NA`` areas. The intersection will be a line(s). See `Solid Modeling
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD5_10.html>`_   in the
        `Modeling and Meshing Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD14.html>`_ for an
        illustration. See the :ref:`boptn` command for an explanation of the options
        available to Boolean operations. Element attributes and solid model boundary conditions assigned to
        the original entities will not be transferred to the new entities generated.
        """
        command = f"ASBL,{na},{nl},,{keepa},{keepl}"
        return self.run(command, **kwargs)

    def asbv(
        self,
        na: str = "",
        nv: str = "",
        sepo: str = "",
        keepa: str = "",
        keepv: str = "",
        **kwargs,
    ):
        r"""Subtracts volumes from areas.

        Mechanical APDL Command: `ASBV <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ASBV.html>`_

        Parameters
        ----------
        na : str
            Area (or areas, if picking is used) to be subtracted from. If ALL, use all selected areas. If P,
            graphical picking is enabled (valid only in the GUI) and remaining fields are ignored. A
            component name may also be substituted for ``NA``.

        nv : str
            Volume (or volumes, if picking is used) to subtract. If ALL, use all selected volumes. A
            component name may also be substituted for ``NV``.

        sepo : str
            Behavior if the intersection of the areas and the volumes is a line or lines:

            * ``(blank)`` - The resulting areas will share line(s) where they touch.

            * ``SEPO`` - The resulting areas will have separate, but coincident line(s) where they touch.

        keepa : str
            Specifies whether ``NA`` areas are to be deleted:

            * ``(blank)`` - Use the setting of KEEP on the :ref:`boptn` command.

            * ``DELETE`` - Delete ``NA`` areas after :ref:`asbv` operation (override :ref:`boptn` command
              settings).

            * ``KEEP`` - Keep ``NA`` areas after :ref:`asbv` operation (override :ref:`boptn` command settings).

        keepv : str
            Specifies whether ``NV`` volumes are to be deleted:

            * ``(blank)`` - Use the setting of KEEP on the :ref:`boptn` command.

            * ``DELETE`` - Delete volumes after :ref:`asbv` operation (override :ref:`boptn` command settings).

            * ``KEEP`` - Keep volumes after :ref:`asbv` operation (override :ref:`boptn` command settings).

        Notes
        -----

        .. _ASBV_notes:

        Generates new areas by subtracting the regions common to both ``NA`` areas and ``NV`` volumes (the
        intersection) from the ``NA`` areas. The intersection can be an area(s) or line(s). If the
        intersection is a line and ``SEPO`` is blank, the ``NA`` area is divided at the line and the
        resulting areas will be connected, sharing a common line where they touch. If ``SEPO`` is set to
        SEPO, ``NA`` is divided into two unconnected areas with separate lines where they touch. See `Solid
        Modeling <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD5_10.html>`_
         in the `Modeling and Meshing Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD14.html>`_ for an
        illustration. See the :ref:`boptn` command for an explanation of the
        options available to Boolean operations. Element attributes and solid model boundary conditions
        assigned to the original entities will not be transferred to the new entities generated.
        """
        command = f"ASBV,{na},{nv},{sepo},{keepa},{keepv}"
        return self.run(command, **kwargs)

    def asbw(self, na: str = "", sepo: str = "", keep: str = "", **kwargs):
        r"""Subtracts the intersection of the working plane from areas (divides areas).

        Mechanical APDL Command: `ASBW <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ASBW.html>`_

        Parameters
        ----------
        na : str
            Area (or areas, if picking is used) to be subtracted from. If ``NA`` = ALL, use all selected
            areas. If ``NA`` = P, graphical picking is enabled (valid only in the GUI). A component name may
            also be input for ``NA``.

        sepo : str
            Behavior of the created boundary.

            * ``(blank)`` - The resulting areas will share line(s) where they touch.

            * ``SEPO`` - The resulting areas will have separate, but coincident line(s).

        keep : str
            Specifies whether ``NA`` areas are to be deleted.

            * ``(blank)`` - Use the setting of KEEP on the :ref:`boptn` command.

            * ``DELETE`` - Delete ``NA`` areas after :ref:`asbw` operation (override :ref:`boptn` command
              settings).

            * ``KEEP`` - Keep ``NA`` areas after :ref:`asbw` operation (override :ref:`boptn` command settings).

        Notes
        -----

        .. _ASBW_notes:

        Generates new areas by subtracting the intersection of the working plane from the ``NA`` areas. The
        intersection will be a line(s). The working plane must not be in the same plane as the ``NA``
        area(s). If ``SEPO`` is blank, the ``NA`` area is divided at the line and the resulting areas will
        be connected, sharing a common line where they touch. If ``SEPO`` is set to SEPO, ``NA`` is divided
        into two unconnected areas with separate lines. The SEPO option may cause unintended consequences if
        any keypoints exist along the cut plane. See `Solid Modeling
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD5_10.html>`_   in the
        `Modeling and Meshing Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD14.html>`_ for an
        illustration. See the :ref:`boptn` command for an explanation of the options
        available to Boolean operations. Element attributes and solid model boundary conditions assigned to
        the original entities will not be transferred to the new entities generated.

        Issuing the :ref:`asbw` command under certain conditions may generate a topological degeneracy
        error. Do not issue the command if:

        * A sphere or cylinder has been scaled. (A cylinder must be scaled unevenly in the XY plane.)

        * A sphere or cylinder has not been scaled but the work plane has been rotated.
        """
        command = f"ASBW,{na},{sepo},{keep}"
        return self.run(command, **kwargs)

    def boptn(self, lab: str = "", value: str = "", **kwargs):
        r"""Specifies Boolean operation options.

        Mechanical APDL Command: `BOPTN <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_BOPTN.html>`_

        **Command default:**

        .. _BOPTN_default:

        Input entities will be deleted, and operations with no effect (that is, operations which are valid
        but which do not cause a change in the input entities, such as adding two non-touching areas) will
        produce a warning message. The Revision 5.2 Boolean compatibility option will be used.

        Parameters
        ----------
        lab : str
            Default/status key:

            * ``DEFA`` - Resets settings to default values.

            * ``STAT`` - Lists status of present settings.

            Option to be controlled:

            * ``KEEP`` - Delete or keep input entity option.

            * ``NUMB`` - Output numbering warning message option.

            * ``NWARN`` - No effect warning message option.

            * ``VERSION`` - Boolean compatibility option.

        value : str
            Option settings if ``Lab`` = KEEP:

            * ``NO`` - Delete entities used as input with a Boolean operation (default). Entities will not be
              deleted if meshed or if attached to a higher entity.

            * ``YES`` - Keep input solid modeling entities.

            Option settings if ``Lab`` = NUMB:

            * ``0`` - No warning message will be produced if the output entities of a Boolean operation are
              numbered based on geometry (default).

            * ``1`` - A warning message will be produced if the output entities of a Boolean operation are
              numbered based on geometry. (With geometric numbering, re-use of the input with altered dimensions
              may not produce the same numbering, and later operations in the input may fail or produce unexpected
              results.)

            Option settings if ``Lab`` = NWARN:

            * ``0`` - A warning message will be produced if a Boolean operation has no effect (default).

            * ``1`` - No warning or error messages will be generated if a Boolean operation has no effect.

            * ``-1`` - An error message will be produced if a Boolean operation has no effect.

            Option settings if ``Lab`` = VERSION:

            * ``RV52`` - Activate the Revision 5.2 compatibility option (default). The 5.2 option can produce
              different numbering of the entities produced by Boolean operations than the 5.1 option. See Notes
              below.

            * ``RV51`` - Activate the Revision 5.1 compatibility option. The 5.1 option can produce different
              numbering of the entities produced by Boolean operations than the 5.2 option. See :ref:`BOPTN_notes`
              below.

        Notes
        -----

        .. _BOPTN_notes:

        Boolean operations at Revision 5.2 may produce a different number of entities than previous
        revisions of Mechanical APDL. When running input files created in earlier versions of Mechanical
        APDL, match the
        Boolean compatibility option (VERSION) to the revision originally used. For instance, if you are
        running Revision 5.2 and are reading an input file ( :ref:`input` ) created at Revision 5.1, it is
        recommended that you set VERSION to RV51 before reading the input.

        See the `Modeling and Meshing Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD14.html>`_ for further
        details on the functions of the RV51 and RV52 labels.

        This command is valid in any processor.
        """
        command = f"BOPTN,{lab},{value}"
        return self.run(command, **kwargs)

    def btol(self, ptol: str = "", **kwargs):
        r"""Specifies the Boolean operation tolerances.

        Mechanical APDL Command: `BTOL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_BTOL.html>`_

        **Command default:**

        .. _BTOL_default:

        ``PTOL`` = 0.10E-4.

        Parameters
        ----------
        ptol : str
            Point coincidence tolerance. Points within this distance to each other will be assumed to be
            coincident during Boolean operations. Loosening the tolerance will increase the run time and
            storage requirements, but will allow more Boolean intersections to succeed. Defaults to 0.10E-4.

        Notes
        -----

        .. _BTOL_notes:

        Use :ref:`btol`,DEFA to reset the setting to its default value. Use :ref:`btol`,STAT to list the
        status of the present setting.
        """
        command = f"BTOL,{ptol}"
        return self.run(command, **kwargs)

    def lcsl(
        self,
        nl1: str = "",
        nl2: str = "",
        nl3: str = "",
        nl4: str = "",
        nl5: str = "",
        nl6: str = "",
        nl7: str = "",
        nl8: str = "",
        nl9: str = "",
        **kwargs,
    ):
        r"""Divides intersecting lines at their point(s) of intersection.

        Mechanical APDL Command: `LCSL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_LCSL.html>`_

        Parameters
        ----------
        nl1 : str
            Numbers of lines to be intersected. If ``NL1`` = ALL, ``NL2`` to ``NL9`` are ignored and the
            intersection of all selected lines is found. If ``NL1`` = P, use graphical picking to specify
            lines ( ``NL2`` to ``NL9`` are ignored).

        nl2 : str
            Numbers of lines to be intersected. If ``NL1`` = ALL, ``NL2`` to ``NL9`` are ignored and the
            intersection of all selected lines is found. If ``NL1`` = P, use graphical picking to specify
            lines ( ``NL2`` to ``NL9`` are ignored).

        nl3 : str
            Numbers of lines to be intersected. If ``NL1`` = ALL, ``NL2`` to ``NL9`` are ignored and the
            intersection of all selected lines is found. If ``NL1`` = P, use graphical picking to specify
            lines ( ``NL2`` to ``NL9`` are ignored).

        nl4 : str
            Numbers of lines to be intersected. If ``NL1`` = ALL, ``NL2`` to ``NL9`` are ignored and the
            intersection of all selected lines is found. If ``NL1`` = P, use graphical picking to specify
            lines ( ``NL2`` to ``NL9`` are ignored).

        nl5 : str
            Numbers of lines to be intersected. If ``NL1`` = ALL, ``NL2`` to ``NL9`` are ignored and the
            intersection of all selected lines is found. If ``NL1`` = P, use graphical picking to specify
            lines ( ``NL2`` to ``NL9`` are ignored).

        nl6 : str
            Numbers of lines to be intersected. If ``NL1`` = ALL, ``NL2`` to ``NL9`` are ignored and the
            intersection of all selected lines is found. If ``NL1`` = P, use graphical picking to specify
            lines ( ``NL2`` to ``NL9`` are ignored).

        nl7 : str
            Numbers of lines to be intersected. If ``NL1`` = ALL, ``NL2`` to ``NL9`` are ignored and the
            intersection of all selected lines is found. If ``NL1`` = P, use graphical picking to specify
            lines ( ``NL2`` to ``NL9`` are ignored).

        nl8 : str
            Numbers of lines to be intersected. If ``NL1`` = ALL, ``NL2`` to ``NL9`` are ignored and the
            intersection of all selected lines is found. If ``NL1`` = P, use graphical picking to specify
            lines ( ``NL2`` to ``NL9`` are ignored).

        nl9 : str
            Numbers of lines to be intersected. If ``NL1`` = ALL, ``NL2`` to ``NL9`` are ignored and the
            intersection of all selected lines is found. If ``NL1`` = P, use graphical picking to specify
            lines ( ``NL2`` to ``NL9`` are ignored).

        Notes
        -----

        .. _LCSL_notes:

        Divides intersecting (classifies) lines at their point(s) of intersection. The original lines (and
        their corresponding keypoint(s)) will be deleted by default. See the :ref:`boptn` command for the
        options available to Boolean operations. Element attributes and solid model boundary conditions
        assigned to the original entities will not be transferred to the new entities generated.
        """
        command = f"LCSL,{nl1},{nl2},{nl3},{nl4},{nl5},{nl6},{nl7},{nl8},{nl9}"
        return self.run(command, **kwargs)

    def lglue(
        self,
        nl1: str = "",
        nl2: str = "",
        nl3: str = "",
        nl4: str = "",
        nl5: str = "",
        nl6: str = "",
        nl7: str = "",
        nl8: str = "",
        nl9: str = "",
        **kwargs,
    ):
        r"""Generates new lines by "gluing" lines.

        Mechanical APDL Command: `LGLUE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_LGLUE.html>`_

        Parameters
        ----------
        nl1 : str
            Numbers of the lines to be glued. If ``NL1`` = ALL, all selected lines will be glued ( ``NL2``
            to ``NL9`` will be ignored). If ``NL1`` = P, graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI). A component name may also be substituted for
            ``NL1``.

        nl2 : str
            Numbers of the lines to be glued. If ``NL1`` = ALL, all selected lines will be glued ( ``NL2``
            to ``NL9`` will be ignored). If ``NL1`` = P, graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI). A component name may also be substituted for
            ``NL1``.

        nl3 : str
            Numbers of the lines to be glued. If ``NL1`` = ALL, all selected lines will be glued ( ``NL2``
            to ``NL9`` will be ignored). If ``NL1`` = P, graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI). A component name may also be substituted for
            ``NL1``.

        nl4 : str
            Numbers of the lines to be glued. If ``NL1`` = ALL, all selected lines will be glued ( ``NL2``
            to ``NL9`` will be ignored). If ``NL1`` = P, graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI). A component name may also be substituted for
            ``NL1``.

        nl5 : str
            Numbers of the lines to be glued. If ``NL1`` = ALL, all selected lines will be glued ( ``NL2``
            to ``NL9`` will be ignored). If ``NL1`` = P, graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI). A component name may also be substituted for
            ``NL1``.

        nl6 : str
            Numbers of the lines to be glued. If ``NL1`` = ALL, all selected lines will be glued ( ``NL2``
            to ``NL9`` will be ignored). If ``NL1`` = P, graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI). A component name may also be substituted for
            ``NL1``.

        nl7 : str
            Numbers of the lines to be glued. If ``NL1`` = ALL, all selected lines will be glued ( ``NL2``
            to ``NL9`` will be ignored). If ``NL1`` = P, graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI). A component name may also be substituted for
            ``NL1``.

        nl8 : str
            Numbers of the lines to be glued. If ``NL1`` = ALL, all selected lines will be glued ( ``NL2``
            to ``NL9`` will be ignored). If ``NL1`` = P, graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI). A component name may also be substituted for
            ``NL1``.

        nl9 : str
            Numbers of the lines to be glued. If ``NL1`` = ALL, all selected lines will be glued ( ``NL2``
            to ``NL9`` will be ignored). If ``NL1`` = P, graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI). A component name may also be substituted for
            ``NL1``.

        Notes
        -----

        .. _LGLUE_notes:

        Use of the :ref:`lglue` command generates new lines by "gluing" input lines. The glue operation
        redefines the input lines so that they share keypoints at their common ends. The new lines encompass
        the same geometry as the original lines. This operation is only valid if the intersections of the
        input lines are keypoints at the ends of those lines. See the `Modeling and Meshing Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD14.html>`_ for an
        illustration. See the
        :ref:`boptn` command for an explanation of the options available to Boolean operations. Element
        attributes and solid model boundary conditions assigned to the original entities will not be
        transferred to the new entities generated.

        The :ref:`lglue` command results in the merging of keypoints at the common end of the lines. The
        keypoints of the lower numbered line will be kept. This means one must be aware of line numbering
        when multiple :ref:`lglue` commands are applied to avoid any "ungluing" of geometry.
        """
        command = f"LGLUE,{nl1},{nl2},{nl3},{nl4},{nl5},{nl6},{nl7},{nl8},{nl9}"
        return self.run(command, **kwargs)

    def lina(self, nl: str = "", na: str = "", **kwargs):
        r"""Finds the intersection of a line with an area.

        Mechanical APDL Command: `LINA <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_LINA.html>`_

        Parameters
        ----------
        nl : str
            Number of line to be intersected. If ``NL`` = P, graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI).

        na : str
            Number of area to be intersected.

        Notes
        -----

        .. _LINA_notes:

        Finds the intersection of a line with an area. New lines will be generated where the lines intersect
        the areas. If the regions of intersection are only points, new keypoints will be generated instead.
        See the `Modeling and Meshing Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD14.html>`_ for an
        illustration. See the :ref:`boptn` command for the options available to
        Boolean operations. Element attributes and solid model boundary conditions assigned to the original
        entities will not be transferred to the new entities generated.
        """
        command = f"LINA,{nl},{na}"
        return self.run(command, **kwargs)

    def linl(
        self,
        nl1: str = "",
        nl2: str = "",
        nl3: str = "",
        nl4: str = "",
        nl5: str = "",
        nl6: str = "",
        nl7: str = "",
        nl8: str = "",
        nl9: str = "",
        **kwargs,
    ):
        r"""Finds the common intersection of lines.

        Mechanical APDL Command: `LINL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_LINL.html>`_

        Parameters
        ----------
        nl1 : str
            Numbers of lines to be intersected. If ``NL1`` = ALL, find the intersection of all selected
            lines and ``NL2`` to ``NL9`` are ignored. If ``NL1`` = P, graphical picking is enabled and all
            remaining command fields are ignored (valid only in the GUI). A component name may also be
            substituted for ``NL1``.

        nl2 : str
            Numbers of lines to be intersected. If ``NL1`` = ALL, find the intersection of all selected
            lines and ``NL2`` to ``NL9`` are ignored. If ``NL1`` = P, graphical picking is enabled and all
            remaining command fields are ignored (valid only in the GUI). A component name may also be
            substituted for ``NL1``.

        nl3 : str
            Numbers of lines to be intersected. If ``NL1`` = ALL, find the intersection of all selected
            lines and ``NL2`` to ``NL9`` are ignored. If ``NL1`` = P, graphical picking is enabled and all
            remaining command fields are ignored (valid only in the GUI). A component name may also be
            substituted for ``NL1``.

        nl4 : str
            Numbers of lines to be intersected. If ``NL1`` = ALL, find the intersection of all selected
            lines and ``NL2`` to ``NL9`` are ignored. If ``NL1`` = P, graphical picking is enabled and all
            remaining command fields are ignored (valid only in the GUI). A component name may also be
            substituted for ``NL1``.

        nl5 : str
            Numbers of lines to be intersected. If ``NL1`` = ALL, find the intersection of all selected
            lines and ``NL2`` to ``NL9`` are ignored. If ``NL1`` = P, graphical picking is enabled and all
            remaining command fields are ignored (valid only in the GUI). A component name may also be
            substituted for ``NL1``.

        nl6 : str
            Numbers of lines to be intersected. If ``NL1`` = ALL, find the intersection of all selected
            lines and ``NL2`` to ``NL9`` are ignored. If ``NL1`` = P, graphical picking is enabled and all
            remaining command fields are ignored (valid only in the GUI). A component name may also be
            substituted for ``NL1``.

        nl7 : str
            Numbers of lines to be intersected. If ``NL1`` = ALL, find the intersection of all selected
            lines and ``NL2`` to ``NL9`` are ignored. If ``NL1`` = P, graphical picking is enabled and all
            remaining command fields are ignored (valid only in the GUI). A component name may also be
            substituted for ``NL1``.

        nl8 : str
            Numbers of lines to be intersected. If ``NL1`` = ALL, find the intersection of all selected
            lines and ``NL2`` to ``NL9`` are ignored. If ``NL1`` = P, graphical picking is enabled and all
            remaining command fields are ignored (valid only in the GUI). A component name may also be
            substituted for ``NL1``.

        nl9 : str
            Numbers of lines to be intersected. If ``NL1`` = ALL, find the intersection of all selected
            lines and ``NL2`` to ``NL9`` are ignored. If ``NL1`` = P, graphical picking is enabled and all
            remaining command fields are ignored (valid only in the GUI). A component name may also be
            substituted for ``NL1``.

        Notes
        -----

        .. _LINL_notes:

        Finds the common (not pairwise) intersection of lines. The common intersection is defined as the
        regions shared (in common) by all lines listed on this command. New lines will be generated where
        the original lines intersect. If the regions of intersection are only points, new keypoints will be
        generated instead. See the `Modeling and Meshing Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD14.html>`_ for an
        illustration. See the :ref:`boptn` command for the
        options available to Boolean operations. Element attributes and solid model boundary conditions
        assigned to the original entities will not be transferred to the new entities generated.
        """
        command = f"LINL,{nl1},{nl2},{nl3},{nl4},{nl5},{nl6},{nl7},{nl8},{nl9}"
        return self.run(command, **kwargs)

    def linp(
        self,
        nl1: str = "",
        nl2: str = "",
        nl3: str = "",
        nl4: str = "",
        nl5: str = "",
        nl6: str = "",
        nl7: str = "",
        nl8: str = "",
        nl9: str = "",
        **kwargs,
    ):
        r"""Finds the pairwise intersection of lines.

        Mechanical APDL Command: `LINP <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_LINP.html>`_

        Parameters
        ----------
        nl1 : str
            Numbers of lines to be intersected pairwise. If ``NL1`` = ALL, find the pairwise intersection of
            all selected lines and ``NL2`` to ``NL9`` are ignored. If ``NL1`` = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in the GUI). A component name
            may be substituted for ``NL1``.

        nl2 : str
            Numbers of lines to be intersected pairwise. If ``NL1`` = ALL, find the pairwise intersection of
            all selected lines and ``NL2`` to ``NL9`` are ignored. If ``NL1`` = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in the GUI). A component name
            may be substituted for ``NL1``.

        nl3 : str
            Numbers of lines to be intersected pairwise. If ``NL1`` = ALL, find the pairwise intersection of
            all selected lines and ``NL2`` to ``NL9`` are ignored. If ``NL1`` = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in the GUI). A component name
            may be substituted for ``NL1``.

        nl4 : str
            Numbers of lines to be intersected pairwise. If ``NL1`` = ALL, find the pairwise intersection of
            all selected lines and ``NL2`` to ``NL9`` are ignored. If ``NL1`` = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in the GUI). A component name
            may be substituted for ``NL1``.

        nl5 : str
            Numbers of lines to be intersected pairwise. If ``NL1`` = ALL, find the pairwise intersection of
            all selected lines and ``NL2`` to ``NL9`` are ignored. If ``NL1`` = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in the GUI). A component name
            may be substituted for ``NL1``.

        nl6 : str
            Numbers of lines to be intersected pairwise. If ``NL1`` = ALL, find the pairwise intersection of
            all selected lines and ``NL2`` to ``NL9`` are ignored. If ``NL1`` = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in the GUI). A component name
            may be substituted for ``NL1``.

        nl7 : str
            Numbers of lines to be intersected pairwise. If ``NL1`` = ALL, find the pairwise intersection of
            all selected lines and ``NL2`` to ``NL9`` are ignored. If ``NL1`` = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in the GUI). A component name
            may be substituted for ``NL1``.

        nl8 : str
            Numbers of lines to be intersected pairwise. If ``NL1`` = ALL, find the pairwise intersection of
            all selected lines and ``NL2`` to ``NL9`` are ignored. If ``NL1`` = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in the GUI). A component name
            may be substituted for ``NL1``.

        nl9 : str
            Numbers of lines to be intersected pairwise. If ``NL1`` = ALL, find the pairwise intersection of
            all selected lines and ``NL2`` to ``NL9`` are ignored. If ``NL1`` = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in the GUI). A component name
            may be substituted for ``NL1``.

        Notes
        -----

        .. _LINP_notes:

        Finds the pairwise intersection of lines. The pairwise intersection is defined as any and all
        regions shared by at least two lines listed on this command. New lines will be generated where the
        original lines intersect pairwise. If the regions of pairwise intersection are only points, new
        keypoints will be generated. See the `Modeling and Meshing Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD14.html>`_ for an
        illustration. See the :ref:`boptn` command for
        the options available to Boolean operations. Element attributes and solid model boundary conditions
        assigned to the original entities will not be transferred to the new entities generated.
        """
        command = f"LINP,{nl1},{nl2},{nl3},{nl4},{nl5},{nl6},{nl7},{nl8},{nl9}"
        return self.run(command, **kwargs)

    def linv(self, nl: str = "", nv: str = "", **kwargs):
        r"""Finds the intersection of a line with a volume.

        Mechanical APDL Command: `LINV <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_LINV.html>`_

        Parameters
        ----------
        nl : str
            Number of line to be intersected. If ``NL`` = P, graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI).

        nv : str
            Number of volume to be intersected.

        Notes
        -----

        .. _LINV_notes:

        Finds the intersection of a line with a volume. New lines will be generated where the lines
        intersect the volumes. If the regions of intersection are only points, new keypoints will be
        generated instead. See the `Modeling and Meshing Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD14.html>`_ for an
        illustration. See the :ref:`boptn` command for the
        options available to Boolean operations. Element attributes and solid model boundary conditions
        assigned to the original entities will not be transferred to the new entities generated.
        """
        command = f"LINV,{nl},{nv}"
        return self.run(command, **kwargs)

    def lovlap(
        self,
        nl1: str = "",
        nl2: str = "",
        nl3: str = "",
        nl4: str = "",
        nl5: str = "",
        nl6: str = "",
        nl7: str = "",
        nl8: str = "",
        nl9: str = "",
        **kwargs,
    ):
        r"""Overlaps lines.

        Mechanical APDL Command: `LOVLAP <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_LOVLAP.html>`_

        Parameters
        ----------
        nl1 : str
            Numbers of lines to be overlapped. If ``NL1`` = ALL, ``NL2`` to ``NL9`` are ignored and all
            selected lines are overlapped. If ``NL1`` = P, graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI). A component name may also be substituted for
            ``NL1``.

        nl2 : str
            Numbers of lines to be overlapped. If ``NL1`` = ALL, ``NL2`` to ``NL9`` are ignored and all
            selected lines are overlapped. If ``NL1`` = P, graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI). A component name may also be substituted for
            ``NL1``.

        nl3 : str
            Numbers of lines to be overlapped. If ``NL1`` = ALL, ``NL2`` to ``NL9`` are ignored and all
            selected lines are overlapped. If ``NL1`` = P, graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI). A component name may also be substituted for
            ``NL1``.

        nl4 : str
            Numbers of lines to be overlapped. If ``NL1`` = ALL, ``NL2`` to ``NL9`` are ignored and all
            selected lines are overlapped. If ``NL1`` = P, graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI). A component name may also be substituted for
            ``NL1``.

        nl5 : str
            Numbers of lines to be overlapped. If ``NL1`` = ALL, ``NL2`` to ``NL9`` are ignored and all
            selected lines are overlapped. If ``NL1`` = P, graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI). A component name may also be substituted for
            ``NL1``.

        nl6 : str
            Numbers of lines to be overlapped. If ``NL1`` = ALL, ``NL2`` to ``NL9`` are ignored and all
            selected lines are overlapped. If ``NL1`` = P, graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI). A component name may also be substituted for
            ``NL1``.

        nl7 : str
            Numbers of lines to be overlapped. If ``NL1`` = ALL, ``NL2`` to ``NL9`` are ignored and all
            selected lines are overlapped. If ``NL1`` = P, graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI). A component name may also be substituted for
            ``NL1``.

        nl8 : str
            Numbers of lines to be overlapped. If ``NL1`` = ALL, ``NL2`` to ``NL9`` are ignored and all
            selected lines are overlapped. If ``NL1`` = P, graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI). A component name may also be substituted for
            ``NL1``.

        nl9 : str
            Numbers of lines to be overlapped. If ``NL1`` = ALL, ``NL2`` to ``NL9`` are ignored and all
            selected lines are overlapped. If ``NL1`` = P, graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI). A component name may also be substituted for
            ``NL1``.

        Notes
        -----

        .. _LOVLAP_notes:

        Overlaps lines. Generates new lines which encompass the geometry of all the input lines. The new
        lines are defined by the regions of intersection of the input lines, and by the complementary (non-
        intersecting) regions. See the `Modeling and Meshing Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD14.html>`_ for an
        illustration. This operation is only valid when the
        region of intersection is a line. See the :ref:`boptn` command for an explanation of the options
        available to Boolean operations. Element attributes and solid model boundary conditions assigned to
        the original entities will not be transferred to the new entities generated.
        """
        command = f"LOVLAP,{nl1},{nl2},{nl3},{nl4},{nl5},{nl6},{nl7},{nl8},{nl9}"
        return self.run(command, **kwargs)

    def lptn(
        self,
        nl1: str = "",
        nl2: str = "",
        nl3: str = "",
        nl4: str = "",
        nl5: str = "",
        nl6: str = "",
        nl7: str = "",
        nl8: str = "",
        nl9: str = "",
        **kwargs,
    ):
        r"""Partitions lines.

        Mechanical APDL Command: `LPTN <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_LPTN.html>`_

        Parameters
        ----------
        nl1 : str
            Numbers of lines to be operated on. If ``NL1`` = ALL, ``NL2`` to ``NL9`` are ignored all
            selected lines are used. If ``NL1`` = P, graphical picking is enabled and all remaining command
            fields are ignored (valid only in the GUI). A component name may be substituted for ``NL1``.

        nl2 : str
            Numbers of lines to be operated on. If ``NL1`` = ALL, ``NL2`` to ``NL9`` are ignored all
            selected lines are used. If ``NL1`` = P, graphical picking is enabled and all remaining command
            fields are ignored (valid only in the GUI). A component name may be substituted for ``NL1``.

        nl3 : str
            Numbers of lines to be operated on. If ``NL1`` = ALL, ``NL2`` to ``NL9`` are ignored all
            selected lines are used. If ``NL1`` = P, graphical picking is enabled and all remaining command
            fields are ignored (valid only in the GUI). A component name may be substituted for ``NL1``.

        nl4 : str
            Numbers of lines to be operated on. If ``NL1`` = ALL, ``NL2`` to ``NL9`` are ignored all
            selected lines are used. If ``NL1`` = P, graphical picking is enabled and all remaining command
            fields are ignored (valid only in the GUI). A component name may be substituted for ``NL1``.

        nl5 : str
            Numbers of lines to be operated on. If ``NL1`` = ALL, ``NL2`` to ``NL9`` are ignored all
            selected lines are used. If ``NL1`` = P, graphical picking is enabled and all remaining command
            fields are ignored (valid only in the GUI). A component name may be substituted for ``NL1``.

        nl6 : str
            Numbers of lines to be operated on. If ``NL1`` = ALL, ``NL2`` to ``NL9`` are ignored all
            selected lines are used. If ``NL1`` = P, graphical picking is enabled and all remaining command
            fields are ignored (valid only in the GUI). A component name may be substituted for ``NL1``.

        nl7 : str
            Numbers of lines to be operated on. If ``NL1`` = ALL, ``NL2`` to ``NL9`` are ignored all
            selected lines are used. If ``NL1`` = P, graphical picking is enabled and all remaining command
            fields are ignored (valid only in the GUI). A component name may be substituted for ``NL1``.

        nl8 : str
            Numbers of lines to be operated on. If ``NL1`` = ALL, ``NL2`` to ``NL9`` are ignored all
            selected lines are used. If ``NL1`` = P, graphical picking is enabled and all remaining command
            fields are ignored (valid only in the GUI). A component name may be substituted for ``NL1``.

        nl9 : str
            Numbers of lines to be operated on. If ``NL1`` = ALL, ``NL2`` to ``NL9`` are ignored all
            selected lines are used. If ``NL1`` = P, graphical picking is enabled and all remaining command
            fields are ignored (valid only in the GUI). A component name may be substituted for ``NL1``.

        Notes
        -----

        .. _LPTN_notes:

        Partitions lines. Generates new lines which encompass the geometry of all the input lines. The new
        lines are defined by both the regions of intersection of the input lines and the complementary (non-
        intersecting) regions. See the `Modeling and Meshing Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD14.html>`_ for an
        illustration. See the :ref:`boptn` command for an
        explanation of the options available to Boolean operations. Element attributes and solid model
        boundary conditions assigned to the original entities will not be transferred to the new entities
        generated.
        """
        command = f"LPTN,{nl1},{nl2},{nl3},{nl4},{nl5},{nl6},{nl7},{nl8},{nl9}"
        return self.run(command, **kwargs)

    def lsba(
        self,
        nl: str = "",
        na: str = "",
        sepo: str = "",
        keepl: str = "",
        keepa: str = "",
        **kwargs,
    ):
        r"""Subtracts areas from lines.

        Mechanical APDL Command: `LSBA <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_LSBA.html>`_

        Parameters
        ----------
        nl : str
            Line (or lines, if picking is used) to be subtracted from. If ALL, use all selected lines. If
            ``NL`` = P, graphical picking is enabled and all remaining command fields are ignored (valid
            only in the GUI). A component name may also be substituted for ``NL``.

        na : str
            Area (or areas, if picking is used) to be subtracted. If ALL, use all selected areas. A
            component name may also be substituted for ``NA``.

        sepo : str
            Behavior if the intersection of the lines and the areas is a keypoint or keypoints:

            * ``(blank)`` - The resulting lines will share keypoint(s) where they touch.

            * ``SEPO`` - The resulting lines will have separate, but coincident keypoint(s) where they touch.

        keepl : str
            Specifies whether ``NL`` lines are to be deleted:

            * ``(blank)`` - Use the setting of KEEP on the :ref:`boptn` command.

            * ``DELETE`` - Delete ``NL`` lines after :ref:`lsba` operation (override :ref:`boptn` command
              settings).

            * ``KEEP`` - Keep ``NL`` lines after :ref:`lsba` operation (override :ref:`boptn` command settings).

        keepa : str
            Specifies whether ``NA`` areas are to be deleted:

            * ``(blank)`` - Use the setting of KEEP on the :ref:`boptn` command.

            * ``DELETE`` - Delete areas after :ref:`lsba` operation (override :ref:`boptn` command settings).

            * ``KEEP`` - Keep areas after :ref:`lsba` operation (override :ref:`boptn` command settings).

        Notes
        -----

        .. _LSBA_notes:

        Generates new lines by subtracting the regions common to both ``NL`` lines and ``NA`` areas (the
        intersection) from the ``NL`` lines. The intersection can be a line(s) or keypoint(s). If the
        intersection is a keypoint and ``SEPO`` is blank, the ``NL`` line is divided at the keypoint and the
        resulting lines will be connected, sharing a common keypoint where they touch. If ``SEPO`` is set to
        SEPO, ``NL`` is divided into two unconnected lines with separate keypoints where they touch. See the
        `Modeling and Meshing Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD14.html>`_ for an
        illustration. See the :ref:`boptn` command for an explanation of the options
        available to Boolean operations. Element attributes and solid model boundary conditions assigned to
        the original entities will not be transferred to the new entities generated.
        """
        command = f"LSBA,{nl},{na},{sepo},{keepl},{keepa}"
        return self.run(command, **kwargs)

    def lsbl(
        self,
        nl1: str = "",
        nl2: str = "",
        sepo: str = "",
        keep1: str = "",
        keep2: str = "",
        **kwargs,
    ):
        r"""Subtracts lines from lines.

        Mechanical APDL Command: `LSBL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_LSBL.html>`_

        Parameters
        ----------
        nl1 : str
            Line (or lines, if picking is used) to be subtracted from. If ALL, use all selected lines. Lines
            specified in this argument are not available for use in the ``NL2`` argument. If P, graphical
            picking is enabled (valid only in the GUI) and all remaining fields are ignored. A component
            name may also be substituted for ``NL1``.

        nl2 : str
            Line (or lines, if picking is used) to subtract. If ALL, use all selected lines (except those
            included in the ``NL1`` argument). A component name may also be substituted for ``NL2``.

        sepo : str
            Behavior if the intersection of the ``NL1`` lines and the ``NL2`` lines is a keypoint or keypoints:

            * ``(blank)`` - The resulting lines will share keypoint(s) where they touch.

            * ``SEPO`` - The resulting lines will have separate, but coincident keypoint(s) where they touch.

        keep1 : str
            Specifies whether ``NL1`` lines are to be deleted:

            * ``(blank)`` - Use the setting of KEEP on the :ref:`boptn` command.

            * ``DELETE`` - Delete ``NL1`` lines after :ref:`lsbl` operation (override :ref:`boptn` command
              settings).

            * ``KEEP`` - Keep ``NL1`` lines after :ref:`lsbl` operation (override :ref:`boptn` command
              settings).

        keep2 : str
            Specifies whether ``NL2`` lines are to be deleted:

            * ``(blank)`` - Use the setting of KEEP on the :ref:`boptn` command.

            * ``DELETE`` - Delete ``NL2`` lines after :ref:`lsbl` operation (override :ref:`boptn` command
              settings).

            * ``KEEP`` - Keep ``NL2`` lines after :ref:`lsbl` operation (override :ref:`boptn` command
              settings).

        Notes
        -----

        .. _LSBL_notes:

        Generates new lines by subtracting the regions common to both ``NL1`` and ``NL2`` lines (the
        intersection) from the ``NL1`` lines. The intersection can be a line(s) or point(s). If the
        intersection is a point and ``SEPO`` is blank, the ``NL1`` line is divided at the point and the
        resulting lines will be connected, sharing a common keypoint where they touch. If ``SEPO`` is set to
        SEPO, ``NL1`` is divided into two unconnected lines with separate keypoints where they touch. See
        the `Modeling and Meshing Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD14.html>`_ for an
        illustration. See the :ref:`boptn` command for an explanation of the options
        available to Boolean operations. Element attributes and solid model boundary conditions assigned to
        the original entities will not be transferred to the new entities generated. :ref:`lsbl`,ALL,ALL
        will have no effect since all the lines (in ``NL1`` ) will be unavailable as ``NL2`` lines.
        """
        command = f"LSBL,{nl1},{nl2},{sepo},{keep1},{keep2}"
        return self.run(command, **kwargs)

    def lsbv(
        self,
        nl: str = "",
        nv: str = "",
        sepo: str = "",
        keepl: str = "",
        keepv: str = "",
        **kwargs,
    ):
        r"""Subtracts volumes from lines.

        Mechanical APDL Command: `LSBV <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_LSBV.html>`_

        Parameters
        ----------
        nl : str
            Line (or lines, if picking is used) to be subtracted from. If ALL, use all selected lines. If
            ``NL`` = P, graphical picking is enabled and all remaining command fields are ignored (valid
            only in the GUI). A component name may also be substituted for ``NL``.

        nv : str
            Volume (or volumes, if picking is used) to be subtracted. If ALL, use all selected volumes. A
            component name may also be substituted for ``NV``.

        sepo : str
            Behavior if the intersection of the ``NL`` lines and the ``NV`` volumes is a keypoint or keypoints:

            * ``(blank)`` - The resulting lines will share keypoint(s) where they touch.

            * ``SEPO`` - The resulting lines will have separate, but coincident keypoint(s) where they touch.

        keepl : str
            Specifies whether ``NL`` lines are to be deleted:

            * ``(blank)`` - Use the setting of KEEP on the :ref:`boptn` command.

            * ``DELETE`` - Delete ``NL`` lines after :ref:`lsbv` operation (override :ref:`boptn` command
              settings).

            * ``KEEP`` - Keep ``NL`` lines after :ref:`lsbv` operation (override :ref:`boptn` command settings).

        keepv : str
            Specifies whether ``NV`` volumes are to be deleted:

            * ``(blank)`` - Use the setting of KEEP on the :ref:`boptn` command.

            * ``DELETE`` - Delete ``NV`` volumes after :ref:`lsbv` operation (override :ref:`boptn` command
              settings).

            * ``KEEP`` - Keep ``NV`` volumes after :ref:`lsbv` operation (override :ref:`boptn` command
              settings).

        Notes
        -----

        .. _LSBV_notes:

        Generates new lines by subtracting the regions common to both ``NL`` lines and ``NV`` volumes (the
        intersection) from the ``NL`` lines. The intersection can be a line(s) or point(s). If the
        intersection is a point and ``SEPO`` is blank, the ``NL1`` line is divided at the point and the
        resulting lines will be connected, sharing a common keypoint where they touch. If ``SEPO`` is set to
        SEPO, ``NL1`` is divided into two unconnected lines with separate keypoints where they touch. See
        the `Modeling and Meshing Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD14.html>`_ for an
        illustration. See the :ref:`boptn` command for an explanation of the options
        available to Boolean operations. Element attributes and solid model boundary conditions assigned to
        the original entities will not be transferred to the new entities generated. :ref:`lsbl`,ALL,ALL
        will have no effect since all the lines (in ``NL1`` ) will be unavailable as ``NL2`` lines.
        """
        command = f"LSBV,{nl},{nv},{sepo},{keepl},{keepv}"
        return self.run(command, **kwargs)

    def lsbw(self, nl: str = "", sepo: str = "", keep: str = "", **kwargs):
        r"""Subtracts the intersection of the working plane from lines (divides lines).

        Mechanical APDL Command: `LSBW <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_LSBW.html>`_

        Parameters
        ----------
        nl : str
            Line (or lines, if picking is used) to be subtracted from. If ``NL`` = ALL, use all selected
            lines. If ``NL`` = P, graphical picking is enabled and all remaining command fields are ignored
            (valid only in the GUI). A component name may also be input for ``NL``.

        sepo : str
            Behavior of the created boundary.

            * ``(blank)`` - The resulting lines will share keypoint(s) where they touch.

            * ``SEPO`` - The resulting lines will have separate, but coincident keypoint(s).

        keep : str
            Specifies whether ``NL`` lines are to be deleted:

            * ``(blank)`` - Use the setting of KEEP on the :ref:`boptn` command.

            * ``DELETE`` - Delete ``NL`` lines after :ref:`lsbw` operation (override :ref:`boptn` command
              settings).

            * ``KEEP`` - Keep ``NL`` lines after :ref:`lsbw` operation (override :ref:`boptn` command settings).

        Notes
        -----

        .. _LSBW_notes:

        Generates new lines by subtracting the intersection of the working plane from the ``NL`` lines. The
        intersection will be a keypoint(s). The working plane must not be in the same plane as the ``NL``
        line(s). If ``SEPO`` is blank, the ``NL`` line is divided and the resulting lines will be connected,
        sharing a common keypoint where they touch. If ``SEPO`` is set to SEPO, ``NL`` is divided into two
        unconnected lines with separate keypoints. See the `Modeling and Meshing Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD14.html>`_ for an
        illustration. See the
        :ref:`boptn` command for an explanation of the options available to Boolean operations. Element
        attributes and solid model boundary conditions assigned to the original entities will not be
        transferred to the new entities generated. Areas that completely contain the input lines will be
        updated if the lines are divided by this operation.
        """
        command = f"LSBW,{nl},{sepo},{keep}"
        return self.run(command, **kwargs)

    def vadd(
        self,
        nv1: str = "",
        nv2: str = "",
        nv3: str = "",
        nv4: str = "",
        nv5: str = "",
        nv6: str = "",
        nv7: str = "",
        nv8: str = "",
        nv9: str = "",
        **kwargs,
    ):
        r"""Adds separate volumes to create a single volume.

        Mechanical APDL Command: `VADD <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_VADD.html>`_

        Parameters
        ----------
        nv1 : str
            Numbers of volumes to be added. If ``NV1`` = ALL, add all selected volumes and ignore ``NV2`` to
            ``NV9``. If ``NV1`` = P, graphical picking is enabled and all remaining command fields are
            ignored (valid only in the GUI). A component name may also be substituted for ``NV1``.

        nv2 : str
            Numbers of volumes to be added. If ``NV1`` = ALL, add all selected volumes and ignore ``NV2`` to
            ``NV9``. If ``NV1`` = P, graphical picking is enabled and all remaining command fields are
            ignored (valid only in the GUI). A component name may also be substituted for ``NV1``.

        nv3 : str
            Numbers of volumes to be added. If ``NV1`` = ALL, add all selected volumes and ignore ``NV2`` to
            ``NV9``. If ``NV1`` = P, graphical picking is enabled and all remaining command fields are
            ignored (valid only in the GUI). A component name may also be substituted for ``NV1``.

        nv4 : str
            Numbers of volumes to be added. If ``NV1`` = ALL, add all selected volumes and ignore ``NV2`` to
            ``NV9``. If ``NV1`` = P, graphical picking is enabled and all remaining command fields are
            ignored (valid only in the GUI). A component name may also be substituted for ``NV1``.

        nv5 : str
            Numbers of volumes to be added. If ``NV1`` = ALL, add all selected volumes and ignore ``NV2`` to
            ``NV9``. If ``NV1`` = P, graphical picking is enabled and all remaining command fields are
            ignored (valid only in the GUI). A component name may also be substituted for ``NV1``.

        nv6 : str
            Numbers of volumes to be added. If ``NV1`` = ALL, add all selected volumes and ignore ``NV2`` to
            ``NV9``. If ``NV1`` = P, graphical picking is enabled and all remaining command fields are
            ignored (valid only in the GUI). A component name may also be substituted for ``NV1``.

        nv7 : str
            Numbers of volumes to be added. If ``NV1`` = ALL, add all selected volumes and ignore ``NV2`` to
            ``NV9``. If ``NV1`` = P, graphical picking is enabled and all remaining command fields are
            ignored (valid only in the GUI). A component name may also be substituted for ``NV1``.

        nv8 : str
            Numbers of volumes to be added. If ``NV1`` = ALL, add all selected volumes and ignore ``NV2`` to
            ``NV9``. If ``NV1`` = P, graphical picking is enabled and all remaining command fields are
            ignored (valid only in the GUI). A component name may also be substituted for ``NV1``.

        nv9 : str
            Numbers of volumes to be added. If ``NV1`` = ALL, add all selected volumes and ignore ``NV2`` to
            ``NV9``. If ``NV1`` = P, graphical picking is enabled and all remaining command fields are
            ignored (valid only in the GUI). A component name may also be substituted for ``NV1``.

        Notes
        -----

        .. _VADD_notes:

        Adds separate volumes to create a single volume. The original volumes (and their corresponding
        areas, lines and keypoints) will be deleted by default ( :ref:`boptn` ). See the :ref:`boptn`
        command for the options available to Boolean operations. Element attributes and solid model boundary
        conditions assigned to the original entities will not be transferred to the new entities generated.
        Concatenated entities are not valid with this command.
        """
        command = f"VADD,{nv1},{nv2},{nv3},{nv4},{nv5},{nv6},{nv7},{nv8},{nv9}"
        return self.run(command, **kwargs)

    def vglue(
        self,
        nv1: str = "",
        nv2: str = "",
        nv3: str = "",
        nv4: str = "",
        nv5: str = "",
        nv6: str = "",
        nv7: str = "",
        nv8: str = "",
        nv9: str = "",
        **kwargs,
    ):
        r"""Generates new volumes by "gluing" volumes.

        Mechanical APDL Command: `VGLUE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_VGLUE.html>`_

        Parameters
        ----------
        nv1 : str
            Numbers of the volumes to be glued. If ``NV1`` = ALL, all selected volumes will be glued (
            ``NV2`` to ``NV9`` will be ignored). If ``NV1`` = P, graphical picking is enabled and all
            remaining command fields are ignored (valid only in the GUI). A component name may also be
            substituted for ``NV1``.

        nv2 : str
            Numbers of the volumes to be glued. If ``NV1`` = ALL, all selected volumes will be glued (
            ``NV2`` to ``NV9`` will be ignored). If ``NV1`` = P, graphical picking is enabled and all
            remaining command fields are ignored (valid only in the GUI). A component name may also be
            substituted for ``NV1``.

        nv3 : str
            Numbers of the volumes to be glued. If ``NV1`` = ALL, all selected volumes will be glued (
            ``NV2`` to ``NV9`` will be ignored). If ``NV1`` = P, graphical picking is enabled and all
            remaining command fields are ignored (valid only in the GUI). A component name may also be
            substituted for ``NV1``.

        nv4 : str
            Numbers of the volumes to be glued. If ``NV1`` = ALL, all selected volumes will be glued (
            ``NV2`` to ``NV9`` will be ignored). If ``NV1`` = P, graphical picking is enabled and all
            remaining command fields are ignored (valid only in the GUI). A component name may also be
            substituted for ``NV1``.

        nv5 : str
            Numbers of the volumes to be glued. If ``NV1`` = ALL, all selected volumes will be glued (
            ``NV2`` to ``NV9`` will be ignored). If ``NV1`` = P, graphical picking is enabled and all
            remaining command fields are ignored (valid only in the GUI). A component name may also be
            substituted for ``NV1``.

        nv6 : str
            Numbers of the volumes to be glued. If ``NV1`` = ALL, all selected volumes will be glued (
            ``NV2`` to ``NV9`` will be ignored). If ``NV1`` = P, graphical picking is enabled and all
            remaining command fields are ignored (valid only in the GUI). A component name may also be
            substituted for ``NV1``.

        nv7 : str
            Numbers of the volumes to be glued. If ``NV1`` = ALL, all selected volumes will be glued (
            ``NV2`` to ``NV9`` will be ignored). If ``NV1`` = P, graphical picking is enabled and all
            remaining command fields are ignored (valid only in the GUI). A component name may also be
            substituted for ``NV1``.

        nv8 : str
            Numbers of the volumes to be glued. If ``NV1`` = ALL, all selected volumes will be glued (
            ``NV2`` to ``NV9`` will be ignored). If ``NV1`` = P, graphical picking is enabled and all
            remaining command fields are ignored (valid only in the GUI). A component name may also be
            substituted for ``NV1``.

        nv9 : str
            Numbers of the volumes to be glued. If ``NV1`` = ALL, all selected volumes will be glued (
            ``NV2`` to ``NV9`` will be ignored). If ``NV1`` = P, graphical picking is enabled and all
            remaining command fields are ignored (valid only in the GUI). A component name may also be
            substituted for ``NV1``.

        Notes
        -----

        .. _VGLUE_notes:

        Use of the :ref:`vglue` command generates new volumes by gluing input volumes. The glue operation
        redefines the input volumes so that they share areas along their common boundaries. The new volumes
        encompass the same geometry as the original volumes. This operation is only valid if the
        intersections of the input volumes are areas along the boundaries of those volumes. See the
        `Modeling and Meshing Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD14.html>`_
        for an illustration. See the :ref:`boptn` command for an explanation of the options available to
        Boolean operations. Element attributes and solid model boundary conditions assigned to the original
        entities will not be transferred to the new entities generated.

        The :ref:`vglue` command results in the merging of areas, lines, and keypoints at the common volume
        boundaries. The areas, lines, and keypoints of the lower numbered volume will be kept. This means
        one must be aware of volume numbering when multiple :ref:`vglue` commands are applied to avoid any
        ungluing of geometry.
        """
        command = f"VGLUE,{nv1},{nv2},{nv3},{nv4},{nv5},{nv6},{nv7},{nv8},{nv9}"
        return self.run(command, **kwargs)

    def vinp(
        self,
        nv1: str = "",
        nv2: str = "",
        nv3: str = "",
        nv4: str = "",
        nv5: str = "",
        nv6: str = "",
        nv7: str = "",
        nv8: str = "",
        nv9: str = "",
        **kwargs,
    ):
        r"""Finds the pairwise intersection of volumes.

        Mechanical APDL Command: `VINP <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_VINP.html>`_

        Parameters
        ----------
        nv1 : str
            Numbers of volumes to be intersected pairwise. If ``NV1`` = ALL, ``NV2`` to ``NV9`` are ignored
            and the pairwise intersection of all selected volumes is found. If ``NV1`` = P, graphical
            picking is enabled and all remaining command fields are ignored (valid only in the GUI). A
            component name may also be substituted for ``NV1``.

        nv2 : str
            Numbers of volumes to be intersected pairwise. If ``NV1`` = ALL, ``NV2`` to ``NV9`` are ignored
            and the pairwise intersection of all selected volumes is found. If ``NV1`` = P, graphical
            picking is enabled and all remaining command fields are ignored (valid only in the GUI). A
            component name may also be substituted for ``NV1``.

        nv3 : str
            Numbers of volumes to be intersected pairwise. If ``NV1`` = ALL, ``NV2`` to ``NV9`` are ignored
            and the pairwise intersection of all selected volumes is found. If ``NV1`` = P, graphical
            picking is enabled and all remaining command fields are ignored (valid only in the GUI). A
            component name may also be substituted for ``NV1``.

        nv4 : str
            Numbers of volumes to be intersected pairwise. If ``NV1`` = ALL, ``NV2`` to ``NV9`` are ignored
            and the pairwise intersection of all selected volumes is found. If ``NV1`` = P, graphical
            picking is enabled and all remaining command fields are ignored (valid only in the GUI). A
            component name may also be substituted for ``NV1``.

        nv5 : str
            Numbers of volumes to be intersected pairwise. If ``NV1`` = ALL, ``NV2`` to ``NV9`` are ignored
            and the pairwise intersection of all selected volumes is found. If ``NV1`` = P, graphical
            picking is enabled and all remaining command fields are ignored (valid only in the GUI). A
            component name may also be substituted for ``NV1``.

        nv6 : str
            Numbers of volumes to be intersected pairwise. If ``NV1`` = ALL, ``NV2`` to ``NV9`` are ignored
            and the pairwise intersection of all selected volumes is found. If ``NV1`` = P, graphical
            picking is enabled and all remaining command fields are ignored (valid only in the GUI). A
            component name may also be substituted for ``NV1``.

        nv7 : str
            Numbers of volumes to be intersected pairwise. If ``NV1`` = ALL, ``NV2`` to ``NV9`` are ignored
            and the pairwise intersection of all selected volumes is found. If ``NV1`` = P, graphical
            picking is enabled and all remaining command fields are ignored (valid only in the GUI). A
            component name may also be substituted for ``NV1``.

        nv8 : str
            Numbers of volumes to be intersected pairwise. If ``NV1`` = ALL, ``NV2`` to ``NV9`` are ignored
            and the pairwise intersection of all selected volumes is found. If ``NV1`` = P, graphical
            picking is enabled and all remaining command fields are ignored (valid only in the GUI). A
            component name may also be substituted for ``NV1``.

        nv9 : str
            Numbers of volumes to be intersected pairwise. If ``NV1`` = ALL, ``NV2`` to ``NV9`` are ignored
            and the pairwise intersection of all selected volumes is found. If ``NV1`` = P, graphical
            picking is enabled and all remaining command fields are ignored (valid only in the GUI). A
            component name may also be substituted for ``NV1``.

        Notes
        -----

        .. _VINP_notes:

        Finds the pairwise intersection of volumes. The pairwise intersection is defined as all regions
        shared by any two or more volumes listed on this command. New volumes will be generated where the
        original volumes intersect pairwise. If the regions of pairwise intersection are only areas, new
        areas will be generated. See the `Modeling and Meshing Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD14.html>`_ for an
        illustration. See the :ref:`boptn` command for an
        explanation of the options available to Boolean operations. Element attributes and solid model
        boundary conditions assigned to the original entities will not be transferred to the new entities
        generated.
        """
        command = f"VINP,{nv1},{nv2},{nv3},{nv4},{nv5},{nv6},{nv7},{nv8},{nv9}"
        return self.run(command, **kwargs)

    def vinv(
        self,
        nv1: str = "",
        nv2: str = "",
        nv3: str = "",
        nv4: str = "",
        nv5: str = "",
        nv6: str = "",
        nv7: str = "",
        nv8: str = "",
        nv9: str = "",
        **kwargs,
    ):
        r"""Finds the intersection of volumes.

        Mechanical APDL Command: `VINV <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_VINV.html>`_

        Parameters
        ----------
        nv1 : str
            Numbers of volumes to be intersected. If ``NV1`` = ALL, ``NV2`` to ``NV9`` are ignored, and the
            intersection of all selected volumes is found. If ``NV1`` = P, graphical picking is enabled and
            all remaining command fields are ignored (valid only in the GUI). A component name may also be
            substituted for ``NV1``.

        nv2 : str
            Numbers of volumes to be intersected. If ``NV1`` = ALL, ``NV2`` to ``NV9`` are ignored, and the
            intersection of all selected volumes is found. If ``NV1`` = P, graphical picking is enabled and
            all remaining command fields are ignored (valid only in the GUI). A component name may also be
            substituted for ``NV1``.

        nv3 : str
            Numbers of volumes to be intersected. If ``NV1`` = ALL, ``NV2`` to ``NV9`` are ignored, and the
            intersection of all selected volumes is found. If ``NV1`` = P, graphical picking is enabled and
            all remaining command fields are ignored (valid only in the GUI). A component name may also be
            substituted for ``NV1``.

        nv4 : str
            Numbers of volumes to be intersected. If ``NV1`` = ALL, ``NV2`` to ``NV9`` are ignored, and the
            intersection of all selected volumes is found. If ``NV1`` = P, graphical picking is enabled and
            all remaining command fields are ignored (valid only in the GUI). A component name may also be
            substituted for ``NV1``.

        nv5 : str
            Numbers of volumes to be intersected. If ``NV1`` = ALL, ``NV2`` to ``NV9`` are ignored, and the
            intersection of all selected volumes is found. If ``NV1`` = P, graphical picking is enabled and
            all remaining command fields are ignored (valid only in the GUI). A component name may also be
            substituted for ``NV1``.

        nv6 : str
            Numbers of volumes to be intersected. If ``NV1`` = ALL, ``NV2`` to ``NV9`` are ignored, and the
            intersection of all selected volumes is found. If ``NV1`` = P, graphical picking is enabled and
            all remaining command fields are ignored (valid only in the GUI). A component name may also be
            substituted for ``NV1``.

        nv7 : str
            Numbers of volumes to be intersected. If ``NV1`` = ALL, ``NV2`` to ``NV9`` are ignored, and the
            intersection of all selected volumes is found. If ``NV1`` = P, graphical picking is enabled and
            all remaining command fields are ignored (valid only in the GUI). A component name may also be
            substituted for ``NV1``.

        nv8 : str
            Numbers of volumes to be intersected. If ``NV1`` = ALL, ``NV2`` to ``NV9`` are ignored, and the
            intersection of all selected volumes is found. If ``NV1`` = P, graphical picking is enabled and
            all remaining command fields are ignored (valid only in the GUI). A component name may also be
            substituted for ``NV1``.

        nv9 : str
            Numbers of volumes to be intersected. If ``NV1`` = ALL, ``NV2`` to ``NV9`` are ignored, and the
            intersection of all selected volumes is found. If ``NV1`` = P, graphical picking is enabled and
            all remaining command fields are ignored (valid only in the GUI). A component name may also be
            substituted for ``NV1``.

        Notes
        -----

        .. _VINV_notes:

        Finds the common (not pairwise) intersection of volumes. The common intersection is defined as the
        regions shared (in common) by **all** volumes listed on this command. New volumes will be generated
        where the original volumes intersect.
        If the regions of intersection are only areas, new areas will be generated instead. See the
        `Modeling and Meshing Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD14.html>`_
        for an illustration. See the :ref:`boptn` command for an explanation of the options available to
        Boolean operations. Element attributes and solid model boundary conditions assigned to the original
        entities will not be transferred to the new entities generated.
        """
        command = f"VINV,{nv1},{nv2},{nv3},{nv4},{nv5},{nv6},{nv7},{nv8},{nv9}"
        return self.run(command, **kwargs)

    def vovlap(
        self,
        nv1: str = "",
        nv2: str = "",
        nv3: str = "",
        nv4: str = "",
        nv5: str = "",
        nv6: str = "",
        nv7: str = "",
        nv8: str = "",
        nv9: str = "",
        **kwargs,
    ):
        r"""Overlaps volumes.

        Mechanical APDL Command: `VOVLAP <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_VOVLAP.html>`_

        Parameters
        ----------
        nv1 : str
            Numbers of volumes to be operated on. If ``NV1`` = ALL, ``NV2`` to ``NV9`` are ignored and all
            selected volumes are used. If ``NV1`` = P, graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI). A component name may also be substituted for
            ``NV1``.

        nv2 : str
            Numbers of volumes to be operated on. If ``NV1`` = ALL, ``NV2`` to ``NV9`` are ignored and all
            selected volumes are used. If ``NV1`` = P, graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI). A component name may also be substituted for
            ``NV1``.

        nv3 : str
            Numbers of volumes to be operated on. If ``NV1`` = ALL, ``NV2`` to ``NV9`` are ignored and all
            selected volumes are used. If ``NV1`` = P, graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI). A component name may also be substituted for
            ``NV1``.

        nv4 : str
            Numbers of volumes to be operated on. If ``NV1`` = ALL, ``NV2`` to ``NV9`` are ignored and all
            selected volumes are used. If ``NV1`` = P, graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI). A component name may also be substituted for
            ``NV1``.

        nv5 : str
            Numbers of volumes to be operated on. If ``NV1`` = ALL, ``NV2`` to ``NV9`` are ignored and all
            selected volumes are used. If ``NV1`` = P, graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI). A component name may also be substituted for
            ``NV1``.

        nv6 : str
            Numbers of volumes to be operated on. If ``NV1`` = ALL, ``NV2`` to ``NV9`` are ignored and all
            selected volumes are used. If ``NV1`` = P, graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI). A component name may also be substituted for
            ``NV1``.

        nv7 : str
            Numbers of volumes to be operated on. If ``NV1`` = ALL, ``NV2`` to ``NV9`` are ignored and all
            selected volumes are used. If ``NV1`` = P, graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI). A component name may also be substituted for
            ``NV1``.

        nv8 : str
            Numbers of volumes to be operated on. If ``NV1`` = ALL, ``NV2`` to ``NV9`` are ignored and all
            selected volumes are used. If ``NV1`` = P, graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI). A component name may also be substituted for
            ``NV1``.

        nv9 : str
            Numbers of volumes to be operated on. If ``NV1`` = ALL, ``NV2`` to ``NV9`` are ignored and all
            selected volumes are used. If ``NV1`` = P, graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI). A component name may also be substituted for
            ``NV1``.

        Notes
        -----

        .. _VOVLAP_notes:

        Overlaps volumes. Generates new volumes which encompass the geometry of all the input volumes. The
        new volumes are defined by the regions of intersection of the input volumes, and by the
        complementary (non-intersecting) regions. See the `Modeling and Meshing Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD14.html>`_ for an
        illustration. This operation is
        only valid when the region of intersection is a volume. See the :ref:`boptn` command for an
        explanation of the options available to Boolean operations. Element attributes and solid model
        boundary conditions assigned to the original entities will not be transferred to the new entities
        generated.
        """
        command = f"VOVLAP,{nv1},{nv2},{nv3},{nv4},{nv5},{nv6},{nv7},{nv8},{nv9}"
        return self.run(command, **kwargs)

    def vptn(
        self,
        nv1: str = "",
        nv2: str = "",
        nv3: str = "",
        nv4: str = "",
        nv5: str = "",
        nv6: str = "",
        nv7: str = "",
        nv8: str = "",
        nv9: str = "",
        **kwargs,
    ):
        r"""Partitions volumes.

        Mechanical APDL Command: `VPTN <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_VPTN.html>`_

        Parameters
        ----------
        nv1 : str
            Numbers of volumes to be operated on. If ``NV1`` = ALL, ``NV2`` to ``NV9`` are ignored and all
            selected volumes are used. If ``NV1`` = P, graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI). A component name may also be substituted for
            ``NV1``.

        nv2 : str
            Numbers of volumes to be operated on. If ``NV1`` = ALL, ``NV2`` to ``NV9`` are ignored and all
            selected volumes are used. If ``NV1`` = P, graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI). A component name may also be substituted for
            ``NV1``.

        nv3 : str
            Numbers of volumes to be operated on. If ``NV1`` = ALL, ``NV2`` to ``NV9`` are ignored and all
            selected volumes are used. If ``NV1`` = P, graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI). A component name may also be substituted for
            ``NV1``.

        nv4 : str
            Numbers of volumes to be operated on. If ``NV1`` = ALL, ``NV2`` to ``NV9`` are ignored and all
            selected volumes are used. If ``NV1`` = P, graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI). A component name may also be substituted for
            ``NV1``.

        nv5 : str
            Numbers of volumes to be operated on. If ``NV1`` = ALL, ``NV2`` to ``NV9`` are ignored and all
            selected volumes are used. If ``NV1`` = P, graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI). A component name may also be substituted for
            ``NV1``.

        nv6 : str
            Numbers of volumes to be operated on. If ``NV1`` = ALL, ``NV2`` to ``NV9`` are ignored and all
            selected volumes are used. If ``NV1`` = P, graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI). A component name may also be substituted for
            ``NV1``.

        nv7 : str
            Numbers of volumes to be operated on. If ``NV1`` = ALL, ``NV2`` to ``NV9`` are ignored and all
            selected volumes are used. If ``NV1`` = P, graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI). A component name may also be substituted for
            ``NV1``.

        nv8 : str
            Numbers of volumes to be operated on. If ``NV1`` = ALL, ``NV2`` to ``NV9`` are ignored and all
            selected volumes are used. If ``NV1`` = P, graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI). A component name may also be substituted for
            ``NV1``.

        nv9 : str
            Numbers of volumes to be operated on. If ``NV1`` = ALL, ``NV2`` to ``NV9`` are ignored and all
            selected volumes are used. If ``NV1`` = P, graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI). A component name may also be substituted for
            ``NV1``.

        Notes
        -----

        .. _VPTN_notes:

        Partitions volumes. Generates new volumes which encompass the geometry of all the input volumes. The
        new volumes are defined by the regions of intersection of the input volumes, and by the
        complementary (non-intersecting) regions. See the `Modeling and Meshing Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD14.html>`_ for an
        illustration. See the :ref:`boptn`
        command for an explanation of the options available to Boolean operations. Element attributes and
        solid model boundary conditions assigned to the original entities will not be transferred to the new
        entities generated.
        """
        command = f"VPTN,{nv1},{nv2},{nv3},{nv4},{nv5},{nv6},{nv7},{nv8},{nv9}"
        return self.run(command, **kwargs)

    def vsba(
        self,
        nv: str = "",
        na: str = "",
        sepo: str = "",
        keepv: str = "",
        keepa: str = "",
        **kwargs,
    ):
        r"""Subtracts areas from volumes.

        Mechanical APDL Command: `VSBA <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_VSBA.html>`_

        Parameters
        ----------
        nv : str
            Volume (or volumes, if picking is used) to be subtracted from. If ALL, use all selected volumes.
            If P, graphical picking is enabled (valid only in the GUI) and remaining fields are ignored. A
            component name may also be substituted for ``NV``.

        na : str
            Area (or areas, if picking is used) to subtract. If ALL, use all selected areas. A component
            name may also be substituted for ``NA``.

        sepo : str
            Behavior of the touching boundary:

            * ``(blank)`` - The resulting volumes will share area(s) where they touch.

            * ``SEPO`` - The resulting volumes will have separate, but coincident area(s) where they touch.

        keepv : str
            Specifies whether ``NV`` volumes are to be deleted:

            * ``(blank)`` - Use the setting of KEEP on the :ref:`boptn` command.

            * ``DELETE`` - Delete ``NV`` volumes after :ref:`vsba` operation (override :ref:`boptn` command
              settings).

            * ``KEEP`` - Keep ``NV`` volumes after :ref:`vsba` operation (override :ref:`boptn` command
              settings).

        keepa : str
            Specifies whether ``NA`` areas are to be deleted:

            * ``(blank)`` - Use the setting of KEEP on the :ref:`boptn` command.

            * ``DELETE`` - Delete ``NA`` areas after :ref:`vsba` operation (override :ref:`boptn` command
              settings).

            * ``KEEP`` - Keep ``NA`` areas after :ref:`vsba` operation (override :ref:`boptn` command settings).

        Notes
        -----

        .. _VSBA_notes:

        Generates new volumes by subtracting the regions common to both the volumes and areas (the
        intersection) from the ``NV`` volumes. The intersection will be an area(s). If ``SEPO`` is blank,
        the volume is divided at the area and the resulting volumes will be connected, sharing a common area
        where they touch. If ``SEPO`` is set to SEPO, the volume is divided into two unconnected volumes
        with separate areas where they touch. See the `Modeling and Meshing Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD14.html>`_ for an
        illustration. See the :ref:`boptn`
        command for an explanation of the options available to Boolean operations. Element attributes and
        solid model boundary conditions assigned to the original entities will not be transferred to the new
        entities generated.
        """
        command = f"VSBA,{nv},{na},{sepo},{keepv},{keepa}"
        return self.run(command, **kwargs)

    def vsbv(
        self,
        nv1: str = "",
        nv2: str = "",
        sepo: str = "",
        keep1: str = "",
        keep2: str = "",
        **kwargs,
    ):
        r"""Subtracts volumes from volumes.

        Mechanical APDL Command: `VSBV <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_VSBV.html>`_

        Parameters
        ----------
        nv1 : str
            Volume (or volumes, if picking is used) to be subtracted from. If ALL, use all selected volumes.
            Volumes specified in set ``NV2`` are removed from set ``NV1``. If P, graphical picking is
            enabled (valid only in the GUI) and remaining fields are ignored. A component name may also be
            substituted for ``NV1``.

        nv2 : str
            Volume (or volumes, if picking is used) to subtract. If ALL, use all selected volumes (except
            those included in the ``NV1`` argument). A component name may also be substituted for ``NV2``.

        sepo : str
            Behavior if the intersection of the ``NV1`` volumes and the ``NV2`` volumes is an area or areas:

            * ``(blank)`` - The resulting volumes will share area(s) where they touch.

            * ``SEPO`` - The resulting volumes will have separate, but coincident area(s) where they touch.

        keep1 : str
            Specifies whether ``NV1`` volumes are to be deleted:

            * ``(blank)`` - Use the setting of ``KEEP`` on the :ref:`boptn` command.

            * ``DELETE`` - Delete ``NV1`` volumes after :ref:`vsbv` operation (override :ref:`boptn` command
              settings).

            * ``KEEP`` - Keep ``NV1`` volumes after :ref:`vsbv` operation (override :ref:`boptn` command
              settings).

        keep2 : str
            Specifies whether ``NV2`` volumes are to be deleted:

            * ``(blank)`` - Use the setting of ``KEEP`` on the :ref:`boptn` command.

            * ``DELETE`` - Delete ``NV2`` volumes after :ref:`vsbv` operation (override :ref:`boptn` command
              settings).

            * ``KEEP`` - Keep ``NV2`` volumes after :ref:`vsbv` operation (override :ref:`boptn` command
              settings).

        Notes
        -----

        .. _VSBV_notes:

        Generates new volumes by subtracting the regions common to both ``NV1`` and ``NV2`` volumes (the
        intersection) from the ``NV1`` volumes. The intersection can be a volume(s) or area(s). If the
        intersection is an area and ``SEPO`` is blank, the ``NV1`` volume is divided at the area and the
        resulting volumes will be connected, sharing a common area where they touch. If ``SEPO`` is set to
        SEPO, ``NV1`` is divided into two unconnected volumes with separate areas where they touch. See the
        `Modeling and Meshing Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD14.html>`_ for an
        illustration. See the :ref:`boptn` command for an explanation of the options
        available to Boolean operations. Element attributes and solid model boundary conditions assigned to
        the original entities will not be transferred to the new entities generated. :ref:`vsbv`,ALL,ALL
        will have no effect because all the volumes in set ``NV1`` will have been moved to set ``NV2``.
        """
        command = f"VSBV,{nv1},{nv2},{sepo},{keep1},{keep2}"
        return self.run(command, **kwargs)

    def vsbw(self, nv: str = "", sepo: str = "", keep: str = "", **kwargs):
        r"""Subtracts intersection of the working plane from volumes (divides volumes).

        Mechanical APDL Command: `VSBW <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_VSBW.html>`_

        Parameters
        ----------
        nv : str
            Volume (or volumes, if picking is used) to be subtracted from. If ``NV`` = ALL, use all selected
            volumes. If ``NV`` = P, graphical picking is enabled (valid only in the GUI). A component name
            may also be input for ``NV``.

        sepo : str
            Behavior of the created boundary.

            * ``(blank)`` - The resulting volumes will share area(s) where they touch.

            * ``SEPO`` - The resulting volumes will have separate, but coincident area(s).

        keep : str
            Specifies whether ``NV`` volumes are to be deleted.

            * ``(blank)`` - Use the setting of ``KEEP`` on the :ref:`boptn` command.

            * ``DELETE`` - Delete ``NV`` volumes after :ref:`vsbw` operation (override :ref:`boptn` command
              settings).

            * ``KEEP`` - Keep ``NV`` volumes after :ref:`vsbw` operation (override :ref:`boptn` command
              settings).

        Notes
        -----

        .. _VSBW_notes:

        Generates new volumes by subtracting the intersection of the working plane from the ``NV`` volumes.
        The intersection will be an area(s). If ``SEPO`` is blank, the volume is divided at the area and the
        resulting volumes will be connected, sharing a common area where they touch. If ``SEPO`` is set to
        SEPO, the volume is divided into two unconnected volumes with separate areas. The SEPO option may
        cause unintended consequences if any keypoints exist along the cut plane. See the `Modeling and
        Meshing Guide <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD14.html>`_
        for an
        illustration. See the :ref:`boptn` command for an explanation of the options available to Boolean
        operations. Element attributes and solid model boundary conditions assigned to the original entities
        will not be transferred to the new entities generated.

        Issuing the :ref:`vsbw` command under certain conditions may generate a topological degeneracy
        error. Do not issue the command if:

        * A sphere or cylinder has been scaled. (A cylinder must be scaled unevenly in the XY plane.)

        * A sphere or cylinder has not been scaled but the work plane has been rotated.
        """
        command = f"VSBW,{nv},{sepo},{keep}"
        return self.run(command, **kwargs)
