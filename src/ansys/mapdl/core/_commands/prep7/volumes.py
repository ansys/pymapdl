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


class Volumes:

    def extopt(
        self,
        lab: str = "",
        val1: str = "",
        val2: str = "",
        val3: str = "",
        val4: str = "",
        **kwargs,
    ):
        r"""Controls options relating to the generation of volume elements from area elements.

        Mechanical APDL Command: `EXTOPT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_EXTOPT.html>`_

        Parameters
        ----------
        lab : str
            Label identifying the control option. The meanings of ``Val1``, ``Val2``, and ``Val3`` will vary depending on ``Lab``.

            * ``ON`` - Sets carryover of the material attributes, real constant attributes, and element
              coordinate system attributes of the pattern area elements to the generated volume elements. Sets the
              pattern area mesh to clear when volume generations are done. ``Val1``, ``Val2``, and ``Val3`` are
              ignored.

            * ``OFF`` - Removes all settings associated with this command. ``Val1``, ``Val2``, and ``Val3`` are
              ignored.

            * ``STAT`` - Shows all settings associated with this command. ``Val1``, ``Val2``, ``Val3``, and
              ``Val4`` are ignored.

            * ``ATTR`` - Sets carryover of particular pattern area attributes (materials, real constants, and element
              coordinate systems) of the pattern area elements to the generated volume elements. (See :ref:`EXTOPT_notes_2`.) ``Val1`` can be:

              * ``0`` - Sets volume elements to use current :ref:`mat` command settings.

              * ``1`` - Sets volume elements to use material attributes of the pattern area elements.

               ``Val2`` can be:

              * ``0`` - Sets volume elements to use current :ref:`real` command settings.

              * ``1`` - Sets volume elements to use real constant attributes of the pattern area elements.

               ``Val3`` can be:

              * ``0`` - Sets volume elements to use current :ref:`esys` command settings.

              * ``1`` - Sets volume elements to use element coordinate system attributes of the pattern area
                elements.

               ``Val4`` can be:

              * ``0`` - Sets volume elements to use current :ref:`secnum` command settings.

              * ``1`` - Sets volume elements to use section attributes of the pattern area elements.

            * ``ESIZE`` - Val1 sets the number of element divisions in the direction of volume generation or
              volume sweep. For :ref:`vdrag` and :ref:`vsweep`, ``Val1`` is overridden by the :ref:`lesize`
              command ``NDIV`` setting. ``Val2`` sets the spacing ratio (bias) in the direction of volume
              generation or volume sweep. If positive, ``Val2`` is the nominal ratio of last division size to
              first division size (if > 1.0, sizes increase, if < 1.0, sizes decrease). If negative, ``Val2`` is
              the nominal ratio of center division(s) size to end divisions size. Ratio defaults to 1.0 (uniform
              spacing). ``Val3`` and ``Val4`` are ignored.

            * ``ACLEAR`` - Sets clearing of pattern area mesh. (See :ref:`EXTOPT_notes_3`.) ``Val1`` can be:

              * ``0`` - Sets pattern area to remain meshed when volume generation is done.

              * ``1`` - Sets pattern area mesh to clear when volume generation is done. ``Val2``, ``Val3``, and
                ``Val4`` are ignored.

            * ``VSWE`` - Indicates that volume sweeping options will be set using ``Val1`` and ``Val2``. Settings specified with :ref:`extopt`, ``VSWE`` will be used the next time the :ref:`vsweep` command is invoked. If ``Lab`` = VSWE, ``Val1`` becomes a label. ``Val1`` can be:

              * ``AUTO`` - Indicates whether you will be prompted for the source and target used by :ref:`vsweep`
                or if VSWE should automatically determine the source and target. If ``Val1`` = AUTO, ``Val2`` is ON
                by default. VSWE will automatically determine the source and target for :ref:`vsweep`. You will be
                allowed to pick more than one volume for sweeping. When ``Val2`` = OFF, the application prompts you
                for the source and target for :ref:`vsweep`. You will only be allowed to pick one volume for
                sweeping.

              * ``TETS`` - Indicates whether :ref:`vsweep` will tet mesh non-sweepable volumes or leave them
                unmeshed. If ``Val1`` = TETS, ``Val2`` is OFF by default. Non-sweepable volumes will be left
                unmeshed. When ``Val2`` = ON, the non-sweepable volumes will be tet meshed if the assigned element
                type supports tet shaped elements.

                ``Val3`` is ignored for Lab = VSWE.

        val1 : str
            Additional input values as described under each option for ``Lab``.

        val2 : str
            Additional input values as described under each option for ``Lab``.

        val3 : str
            Additional input values as described under each option for ``Lab``.

        val4 : str
            Additional input values as described under each option for ``Lab``.

        Notes
        -----

        .. _EXTOPT_notes:

        .. _EXTOPT_notes_1:

        :ref:`extopt` controls options relating to the generation of volume elements from pattern area
        elements using the :ref:`vext`, :ref:`vrotat`, :ref:`voffst`, :ref:`vdrag`, and :ref:`vsweep`
        commands. (When using :ref:`vsweep`, the pattern area is referred to as the source area.)

        .. _EXTOPT_notes_2:

        Enables carryover of the attributes of the pattern area elements to the generated volume elements
        when you are using :ref:`vext`, :ref:`vrotat`, :ref:`voffst`, or :ref:`vdrag`. (When using
        :ref:`vsweep`, since the volume already exists, use the :ref:`vatt` command to assign attributes
        before sweeping.)

        .. _EXTOPT_notes_3:

        When you are using :ref:`vext`, :ref:`vrotat`, :ref:`voffst`, or :ref:`vdrag`, enables clearing of
        the pattern area mesh when volume generations are done. (When you are using :ref:`vsweep`, if
        selected, the area meshes on the pattern (source), target, and/or side areas clear when volume
        sweeping is done.)

        .. _EXTOPT_notes_4:

        Neither :ref:`extopt`,VSWE,AUTO nor :ref:`extopt`,VSWE,TETS will be affected by :ref:`extopt`,ON or
        :ref:`extopt`, OFF.
        """
        command = f"EXTOPT,{lab},{val1},{val2},{val3},{val4}"
        return self.run(command, **kwargs)

    def v(
        self,
        p1: str = "",
        p2: str = "",
        p3: str = "",
        p4: str = "",
        p5: str = "",
        p6: str = "",
        p7: str = "",
        p8: str = "",
        **kwargs,
    ):
        r"""Defines a volume through keypoints.

        Mechanical APDL Command: `V <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_V.html>`_

        Parameters
        ----------
        p1 : str
            Keypoint defining starting corner of volume. If ``P1`` = P, graphical picking is enabled and all
            remaining command fields are ignored (valid only in the GUI).

        p2 : str
            Keypoint defining second corner of volume.

        p3 : str
            Keypoint defining third corner of volume.

        p4 : str
            Keypoint defining fourth corner of volume.

        p5 : str
            Keypoint defining fifth corner of volume.

        p6 : str
            Keypoint defining sixth corner of volume.

        p7 : str
            Keypoint defining seventh corner of volume.

        p8 : str
            Keypoint defining eighth corner of volume.

        Returns
        -------
        int
            Volume number of the generated volume.

        Notes
        -----
        **Notes**

        .. _V_notes:

        Defines a volume (and its corresponding lines and areas) through eight (or fewer) existing
        keypoints. Keypoints must be input in a continuous order. The order of the keypoints should be
        around the bottom and then the top. Missing lines are generated "straight" in the active coordinate
        system and assigned the lowest available numbers ( :ref:`numstr` ). Missing areas are generated and
        assigned the lowest available numbers.

        Solid modeling in a toroidal coordinate system is not recommended.

        Certain faces may be condensed to a line or point by repeating keypoints. For example, use
        :ref:`v`, ``P1``, ``P2``, ``P3``, ``P3``, ``P5``, ``P6``, ``P7``, ``P7`` for a triangular prism or
        :ref:`v`, ``P1``, ``P2``, ``P3``, ``P3``, ``P5``, ``P5``, ``P5``, ``P5`` for a tetrahedron.

        Using keypoints to produce partial sections in :ref:`csys` = 2 can generate anomalies; check the
        resulting volumes carefully.

        Examples
        --------
        Create a simple cube volume.

        >>> k0 = mapdl.k("", 0, 0, 0)
        >>> k1 = mapdl.k("", 1, 0, 0)
        >>> k2 = mapdl.k("", 1, 1, 0)
        >>> k3 = mapdl.k("", 0, 1, 0)
        >>> k4 = mapdl.k("", 0, 0, 1)
        >>> k5 = mapdl.k("", 1, 0, 1)
        >>> k6 = mapdl.k("", 1, 1, 1)
        >>> k7 = mapdl.k("", 0, 1, 1)
        >>> v0 = mapdl.v(k0, k1, k2, k3, k4, k5, k6, k7)
        >>> v0
        1

        Create a triangular prism

        >>> k0 = mapdl.k("", 0, 0, 0)
        >>> k1 = mapdl.k("", 1, 0, 0)
        >>> k2 = mapdl.k("", 1, 1, 0)
        >>> k3 = mapdl.k("", 0, 1, 0)
        >>> k4 = mapdl.k("", 0, 0, 1)
        >>> k5 = mapdl.k("", 1, 0, 1)
        >>> k6 = mapdl.k("", 1, 1, 1)
        >>> k7 = mapdl.k("", 0, 1, 1)
        >>> v1 = mapdl.v(k0, k1, k2, k2, k4, k5, k6, k6)
        >>> v1
        2

        Create a tetrahedron

        >>> k0 = mapdl.k("", 0, 0, 0)
        >>> k1 = mapdl.k("", 1, 0, 0)
        >>> k2 = mapdl.k("", 1, 1, 0)
        >>> k3 = mapdl.k("", 0, 0, 1)
        >>> v2 = mapdl.v(k0, k1, k2, k2, k3, k3, k3, k3)
        >>> v2
        3
        """
        command = f"V,{p1},{p2},{p3},{p4},{p5},{p6},{p7},{p8}"
        return parse.parse_v(self.run(command, **kwargs))

    def va(
        self,
        a1: str = "",
        a2: str = "",
        a3: str = "",
        a4: str = "",
        a5: str = "",
        a6: str = "",
        a7: str = "",
        a8: str = "",
        a9: str = "",
        a10: str = "",
        **kwargs,
    ):
        r"""Generates a volume bounded by existing areas.

        Mechanical APDL Command: `VA <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_VA.html>`_

        Parameters
        ----------
        a1 : str
            List of areas defining volume. The minimum number of areas is 4. If ``A1`` = ALL, use all
            selected ( :ref:`asel` ) areas and ignore ``A2`` to ``A10``. If ``A1`` = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in the GUI). A component name
            may also be substituted for ``A1``.

        a2 : str
            List of areas defining volume. The minimum number of areas is 4. If ``A1`` = ALL, use all
            selected ( :ref:`asel` ) areas and ignore ``A2`` to ``A10``. If ``A1`` = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in the GUI). A component name
            may also be substituted for ``A1``.

        a3 : str
            List of areas defining volume. The minimum number of areas is 4. If ``A1`` = ALL, use all
            selected ( :ref:`asel` ) areas and ignore ``A2`` to ``A10``. If ``A1`` = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in the GUI). A component name
            may also be substituted for ``A1``.

        a4 : str
            List of areas defining volume. The minimum number of areas is 4. If ``A1`` = ALL, use all
            selected ( :ref:`asel` ) areas and ignore ``A2`` to ``A10``. If ``A1`` = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in the GUI). A component name
            may also be substituted for ``A1``.

        a5 : str
            List of areas defining volume. The minimum number of areas is 4. If ``A1`` = ALL, use all
            selected ( :ref:`asel` ) areas and ignore ``A2`` to ``A10``. If ``A1`` = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in the GUI). A component name
            may also be substituted for ``A1``.

        a6 : str
            List of areas defining volume. The minimum number of areas is 4. If ``A1`` = ALL, use all
            selected ( :ref:`asel` ) areas and ignore ``A2`` to ``A10``. If ``A1`` = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in the GUI). A component name
            may also be substituted for ``A1``.

        a7 : str
            List of areas defining volume. The minimum number of areas is 4. If ``A1`` = ALL, use all
            selected ( :ref:`asel` ) areas and ignore ``A2`` to ``A10``. If ``A1`` = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in the GUI). A component name
            may also be substituted for ``A1``.

        a8 : str
            List of areas defining volume. The minimum number of areas is 4. If ``A1`` = ALL, use all
            selected ( :ref:`asel` ) areas and ignore ``A2`` to ``A10``. If ``A1`` = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in the GUI). A component name
            may also be substituted for ``A1``.

        a9 : str
            List of areas defining volume. The minimum number of areas is 4. If ``A1`` = ALL, use all
            selected ( :ref:`asel` ) areas and ignore ``A2`` to ``A10``. If ``A1`` = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in the GUI). A component name
            may also be substituted for ``A1``.

        a10 : str
            List of areas defining volume. The minimum number of areas is 4. If ``A1`` = ALL, use all
            selected ( :ref:`asel` ) areas and ignore ``A2`` to ``A10``. If ``A1`` = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in the GUI). A component name
            may also be substituted for ``A1``.

        Returns
        -------
        int
            Volume number of the volume.

        Notes
        -----

        .. _VA_notes:

        This command conveniently allows generating volumes from regions having more than eight keypoints
        (which is not allowed with the :ref:`v` command). Areas may be input in any order. The exterior
        surface of a :ref:`va` volume must be continuous, but holes may pass completely through it.

        Examples
        --------
        Create a simple tetrahedral bounded by 4 areas.

        >>> k0 = mapdl.k('', -1, 0, 0)
        >>> k1 = mapdl.k('', 1, 0,  0)
        >>> k2 = mapdl.k('', 1, 1, 0)
        >>> k3 = mapdl.k('', 1, 0.5, 1)
        >>> a0 = mapdl.a(k0, k1, k2)
        >>> a1 = mapdl.a(k0, k1, k3)
        >>> a2 = mapdl.a(k1, k2, k3)
        >>> a3 = mapdl.a(k0, k2, k3)
        >>> vnum = mapdl.va(a0, a1, a2, a3)
        >>> vnum
        1
        """
        command = f"VA,{a1},{a2},{a3},{a4},{a5},{a6},{a7},{a8},{a9},{a10}"
        return parse.parse_v(self.run(command, **kwargs))

    def vdele(
        self,
        nv1: str = "",
        nv2: str = "",
        ninc: str = "",
        kswp: int | str = "",
        **kwargs,
    ):
        r"""Deletes unmeshed volumes.

        Mechanical APDL Command: `VDELE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_VDELE.html>`_

        Parameters
        ----------
        nv1 : str
            Delete volumes from ``NV1`` to ``NV2`` (defaults to ``NV1`` ) in steps of ``NINC`` (defaults to
            1). If ``NV1`` = ALL, ``NV2`` and ``NINC`` are ignored and all selected volumes ( :ref:`vsel` )
            are deleted. If ``NV1`` = P, graphical picking is enabled and all remaining command fields are
            ignored (valid only in the GUI). A component name may also be substituted for ``NV1`` ( ``NV2``
            and ``NINC`` are ignored).

        nv2 : str
            Delete volumes from ``NV1`` to ``NV2`` (defaults to ``NV1`` ) in steps of ``NINC`` (defaults to
            1). If ``NV1`` = ALL, ``NV2`` and ``NINC`` are ignored and all selected volumes ( :ref:`vsel` )
            are deleted. If ``NV1`` = P, graphical picking is enabled and all remaining command fields are
            ignored (valid only in the GUI). A component name may also be substituted for ``NV1`` ( ``NV2``
            and ``NINC`` are ignored).

        ninc : str
            Delete volumes from ``NV1`` to ``NV2`` (defaults to ``NV1`` ) in steps of ``NINC`` (defaults to
            1). If ``NV1`` = ALL, ``NV2`` and ``NINC`` are ignored and all selected volumes ( :ref:`vsel` )
            are deleted. If ``NV1`` = P, graphical picking is enabled and all remaining command fields are
            ignored (valid only in the GUI). A component name may also be substituted for ``NV1`` ( ``NV2``
            and ``NINC`` are ignored).

        kswp : int or str
            Specifies whether keypoints, lines, and areas are also deleted:

            * ``0`` - Delete volumes only (default).

            * ``1`` - Delete volumes, as well as keypoints, lines, and areas attached to the specified volumes
              but not shared by other volumes.

        """
        command = f"VDELE,{nv1},{nv2},{ninc},{kswp}"
        return self.run(command, **kwargs)

    def vdgl(self, nv1: str = "", nv2: str = "", ninc: str = "", **kwargs):
        r"""Lists keypoints of a volume that lie on a parametric degeneracy.

        Mechanical APDL Command: `VDGL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_VDGL.html>`_

        Parameters
        ----------
        nv1 : str
            List keypoints that lie on a parametric degeneracy on volumes from ``NV1`` to ``NV2`` (defaults
            to ``NV1`` ) in steps of ``NINC`` (defaults to 1). If ``NV1`` = ALL (default), ``NV2`` and
            ``NINC`` will be ignored and keypoints on all selected volumes ( :ref:`vsel` ) will be listed.
            If ``NV1`` = P, graphical picking is enabled and all remaining command fields are ignored (valid
            only in the GUI). You may also substitute a component name for ``NV1`` (ignore ``NV2`` and
            ``NINC`` ).

        nv2 : str
            List keypoints that lie on a parametric degeneracy on volumes from ``NV1`` to ``NV2`` (defaults
            to ``NV1`` ) in steps of ``NINC`` (defaults to 1). If ``NV1`` = ALL (default), ``NV2`` and
            ``NINC`` will be ignored and keypoints on all selected volumes ( :ref:`vsel` ) will be listed.
            If ``NV1`` = P, graphical picking is enabled and all remaining command fields are ignored (valid
            only in the GUI). You may also substitute a component name for ``NV1`` (ignore ``NV2`` and
            ``NINC`` ).

        ninc : str
            List keypoints that lie on a parametric degeneracy on volumes from ``NV1`` to ``NV2`` (defaults
            to ``NV1`` ) in steps of ``NINC`` (defaults to 1). If ``NV1`` = ALL (default), ``NV2`` and
            ``NINC`` will be ignored and keypoints on all selected volumes ( :ref:`vsel` ) will be listed.
            If ``NV1`` = P, graphical picking is enabled and all remaining command fields are ignored (valid
            only in the GUI). You may also substitute a component name for ``NV1`` (ignore ``NV2`` and
            ``NINC`` ).

        Notes
        -----

        .. _VDGL_notes:

        See the `Modeling and Meshing Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD14.html>`_ for details
        about parametric degeneracies.

        This command is valid in any processor.
        """
        command = f"VDGL,{nv1},{nv2},{ninc}"
        return self.run(command, **kwargs)

    def vdrag(
        self,
        na1: str = "",
        na2: str = "",
        na3: str = "",
        na4: str = "",
        na5: str = "",
        na6: str = "",
        nlp1: str = "",
        nlp2: str = "",
        nlp3: str = "",
        nlp4: str = "",
        nlp5: str = "",
        nlp6: str = "",
        **kwargs,
    ):
        r"""Generates volumes by dragging an area pattern along a path.

        Mechanical APDL Command: `VDRAG <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_VDRAG.html>`_

        Parameters
        ----------
        na1 : str
            List of areas in the pattern to be dragged (6 maximum if using keyboard entry). If ``NA1`` = P,
            graphical picking is enabled and all remaining command fields are ignored (valid only in the
            GUI). If ``NA1`` = ALL, all selected areas will be swept along the path. A component name may
            also be substituted for ``NA1``.

        na2 : str
            List of areas in the pattern to be dragged (6 maximum if using keyboard entry). If ``NA1`` = P,
            graphical picking is enabled and all remaining command fields are ignored (valid only in the
            GUI). If ``NA1`` = ALL, all selected areas will be swept along the path. A component name may
            also be substituted for ``NA1``.

        na3 : str
            List of areas in the pattern to be dragged (6 maximum if using keyboard entry). If ``NA1`` = P,
            graphical picking is enabled and all remaining command fields are ignored (valid only in the
            GUI). If ``NA1`` = ALL, all selected areas will be swept along the path. A component name may
            also be substituted for ``NA1``.

        na4 : str
            List of areas in the pattern to be dragged (6 maximum if using keyboard entry). If ``NA1`` = P,
            graphical picking is enabled and all remaining command fields are ignored (valid only in the
            GUI). If ``NA1`` = ALL, all selected areas will be swept along the path. A component name may
            also be substituted for ``NA1``.

        na5 : str
            List of areas in the pattern to be dragged (6 maximum if using keyboard entry). If ``NA1`` = P,
            graphical picking is enabled and all remaining command fields are ignored (valid only in the
            GUI). If ``NA1`` = ALL, all selected areas will be swept along the path. A component name may
            also be substituted for ``NA1``.

        na6 : str
            List of areas in the pattern to be dragged (6 maximum if using keyboard entry). If ``NA1`` = P,
            graphical picking is enabled and all remaining command fields are ignored (valid only in the
            GUI). If ``NA1`` = ALL, all selected areas will be swept along the path. A component name may
            also be substituted for ``NA1``.

        nlp1 : str
            List of lines defining the path along which the pattern is to be dragged (6 maximum if using
            keyboard entry). Must be a continuous set of lines. To be continuous, adjacent lines must share
            the connecting keypoint (the end keypoint of one line must also be first keypoint of the next
            line).

        nlp2 : str
            List of lines defining the path along which the pattern is to be dragged (6 maximum if using
            keyboard entry). Must be a continuous set of lines. To be continuous, adjacent lines must share
            the connecting keypoint (the end keypoint of one line must also be first keypoint of the next
            line).

        nlp3 : str
            List of lines defining the path along which the pattern is to be dragged (6 maximum if using
            keyboard entry). Must be a continuous set of lines. To be continuous, adjacent lines must share
            the connecting keypoint (the end keypoint of one line must also be first keypoint of the next
            line).

        nlp4 : str
            List of lines defining the path along which the pattern is to be dragged (6 maximum if using
            keyboard entry). Must be a continuous set of lines. To be continuous, adjacent lines must share
            the connecting keypoint (the end keypoint of one line must also be first keypoint of the next
            line).

        nlp5 : str
            List of lines defining the path along which the pattern is to be dragged (6 maximum if using
            keyboard entry). Must be a continuous set of lines. To be continuous, adjacent lines must share
            the connecting keypoint (the end keypoint of one line must also be first keypoint of the next
            line).

        nlp6 : str
            List of lines defining the path along which the pattern is to be dragged (6 maximum if using
            keyboard entry). Must be a continuous set of lines. To be continuous, adjacent lines must share
            the connecting keypoint (the end keypoint of one line must also be first keypoint of the next
            line).

        Notes
        -----

        .. _VDRAG_notes:

        Generates volumes (and their corresponding keypoints, lines, and areas) by sweeping a given area
        pattern along a characteristic drag path. If the drag path consists of multiple lines, the drag
        direction is determined by the sequence in which the path lines are input ( ``NLP1``, ``NLP2``,
        etc.). If the drag path is a single line ( ``NLP1`` ), the drag direction is from the keypoint on
        the drag line that is closest to the first keypoint of the given area pattern to the other end of
        the drag line.

        The magnitude of the vector between the keypoints of the given pattern and the first path keypoint
        remains constant for all generated keypoint patterns and the path keypoints. The direction of the
        vector relative to the path slope also remains constant so that patterns may be swept around curves.
        Lines are generated with the same shapes as the given pattern and the path lines.

        Keypoint, line, area, and volume numbers are automatically assigned (beginning with the lowest
        available values ( :ref:`numstr` )). Adjacent lines use a common keypoint, adjacent areas use a
        common line, and adjacent volumes use a common area. For best results, the entities to be dragged
        should be orthogonal to the start of the drag path. Drag operations that produce an error message
        may create some of the desired entities prior to terminating.

        If element attributes have been associated with the input area via the :ref:`aatt` command, the
        opposite area generated by the :ref:`vdrag` operation will also have those attributes (that is, the
        element attributes from the input area are copied to the opposite area). Note that only the area
        opposite the input area will have the same attributes as the input area; the areas adjacent to the
        input area will not.

        If the input areas are meshed or belong to a meshed volume, the area(s) can be extruded to a 3D
        mesh. Note that the ``NDIV`` argument of the :ref:`esize` command should be set before extruding the
        meshed areas. Alternatively, mesh divisions can be specified directly on the drag line(s) (
        :ref:`lesize` ). See the `Modeling and Meshing Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD14.html>`_ for more
        information.

        You can use the :ref:`vdrag` command to generate 3D interface element meshes for elements
        ``INTER194`` and ``INTER195``. When generating interface element meshes using :ref:`vdrag`, you must
        specify the line divisions to generate one interface element directly on the drag line using the
        :ref:`lesize` command. The source area to be extruded becomes the bottom surface of the interface
        element. Interface elements must be extruded in what will become the element's local x direction,
        that is, bottom to top.
        """
        command = f"VDRAG,{na1},{na2},{na3},{na4},{na5},{na6},{nlp1},{nlp2},{nlp3},{nlp4},{nlp5},{nlp6}"
        return self.run(command, **kwargs)

    def vext(
        self,
        na1: str = "",
        na2: str = "",
        ninc: str = "",
        dx: str = "",
        dy: str = "",
        dz: str = "",
        rx: str = "",
        ry: str = "",
        rz: str = "",
        **kwargs,
    ):
        r"""Generates additional volumes by extruding areas.

        Mechanical APDL Command: `VEXT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_VEXT.html>`_

        Parameters
        ----------
        na1 : str
            Set of areas ( ``NA1`` to ``NA2`` in steps of ``NINC`` ) that defines the pattern to be
            extruded. ``NA2`` defaults to ``NA1``, ``NINC`` defaults to 1. If ``NA1`` = ALL, ``NA2`` and
            ``NINC`` are ignored and the pattern is defined by all selected areas. If ``NA1`` = P, graphical
            picking is enabled and all remaining command fields are ignored (valid only in the GUI). A
            component name may also be substituted for ``NA1`` ( ``NA2`` and ``NINC`` are ignored).

        na2 : str
            Set of areas ( ``NA1`` to ``NA2`` in steps of ``NINC`` ) that defines the pattern to be
            extruded. ``NA2`` defaults to ``NA1``, ``NINC`` defaults to 1. If ``NA1`` = ALL, ``NA2`` and
            ``NINC`` are ignored and the pattern is defined by all selected areas. If ``NA1`` = P, graphical
            picking is enabled and all remaining command fields are ignored (valid only in the GUI). A
            component name may also be substituted for ``NA1`` ( ``NA2`` and ``NINC`` are ignored).

        ninc : str
            Set of areas ( ``NA1`` to ``NA2`` in steps of ``NINC`` ) that defines the pattern to be
            extruded. ``NA2`` defaults to ``NA1``, ``NINC`` defaults to 1. If ``NA1`` = ALL, ``NA2`` and
            ``NINC`` are ignored and the pattern is defined by all selected areas. If ``NA1`` = P, graphical
            picking is enabled and all remaining command fields are ignored (valid only in the GUI). A
            component name may also be substituted for ``NA1`` ( ``NA2`` and ``NINC`` are ignored).

        dx : str
            Increments to be applied to the X, Y, and Z keypoint coordinates in the active coordinate system
            ( DR, Dθ, DZ for cylindrical; DR, Dθ, DΦ for spherical).

        dy : str
            Increments to be applied to the X, Y, and Z keypoint coordinates in the active coordinate system
            ( DR, Dθ, DZ for cylindrical; DR, Dθ, DΦ for spherical).

        dz : str
            Increments to be applied to the X, Y, and Z keypoint coordinates in the active coordinate system
            ( DR, Dθ, DZ for cylindrical; DR, Dθ, DΦ for spherical).

        rx : str
            Scale factors to be applied to the X, Y, and Z keypoint coordinates in the active coordinate
            system ( RR, Rθ, RZ for cylindrical; RR, Rθ, RΦ for spherical). Note that the Rθ and RΦ scale
            factors are interpreted as angular offsets. For example, if CSYS = 1, ``RX``, ``RY``, ``RZ``
            input of (1.5,10,3) would scale the specified keypoints 1.5 times in the radial and 3 times in
            the Z direction, while adding an offset of 10 degrees to the keypoints. Zero, blank, or negative
            scale factor values are assumed to be 1.0. Zero or blank angular offsets have no effect.

        ry : str
            Scale factors to be applied to the X, Y, and Z keypoint coordinates in the active coordinate
            system ( RR, Rθ, RZ for cylindrical; RR, Rθ, RΦ for spherical). Note that the Rθ and RΦ scale
            factors are interpreted as angular offsets. For example, if CSYS = 1, ``RX``, ``RY``, ``RZ``
            input of (1.5,10,3) would scale the specified keypoints 1.5 times in the radial and 3 times in
            the Z direction, while adding an offset of 10 degrees to the keypoints. Zero, blank, or negative
            scale factor values are assumed to be 1.0. Zero or blank angular offsets have no effect.

        rz : str
            Scale factors to be applied to the X, Y, and Z keypoint coordinates in the active coordinate
            system ( RR, Rθ, RZ for cylindrical; RR, Rθ, RΦ for spherical). Note that the Rθ and RΦ scale
            factors are interpreted as angular offsets. For example, if CSYS = 1, ``RX``, ``RY``, ``RZ``
            input of (1.5,10,3) would scale the specified keypoints 1.5 times in the radial and 3 times in
            the Z direction, while adding an offset of 10 degrees to the keypoints. Zero, blank, or negative
            scale factor values are assumed to be 1.0. Zero or blank angular offsets have no effect.

        Notes
        -----

        .. _VEXT_notes:

        Generates additional volumes (and their corresponding keypoints, lines, and areas) by extruding and
        scaling a pattern of areas in the active coordinate system.

        If element attributes have been associated with the input area via the :ref:`aatt` command, the
        opposite area generated by the :ref:`vext` operation will also have those attributes (that is, the
        element attributes from the input area are copied to the opposite area). Note that only the area
        opposite the input area will have the same attributes as the input area; the areas adjacent to the
        input area will not.

        If the areas are meshed or belong to meshed volumes, a 3D mesh can be extruded with this command.
        Note that the ``NDIV`` argument on the :ref:`esize` command should be set before extruding the
        meshed areas.

        Scaling of the input areas, if specified, is performed first, followed by the extrusion.

        In a non-Cartesian coordinate system, the :ref:`vext` command locates the end face of the volume
        based on the active coordinate system. However, the extrusion is made along a straight line between
        the end faces. Note that solid modeling in a toroidal coordinate system is not recommended.

        .. warning::

            Use of the VEXT command can produce unexpected results when operating in a non-Cartesian
            coordinate system. For a detailed description of the possible problems that may occur, see
            Solid Modelingin the `Modeling and Meshing Guide <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD14.html>`_.
        """
        command = f"VEXT,{na1},{na2},{ninc},{dx},{dy},{dz},{rx},{ry},{rz}"
        return self.run(command, **kwargs)

    def vgen(
        self,
        itime: str = "",
        nv1: str = "",
        nv2: str = "",
        ninc: str = "",
        dx: str = "",
        dy: str = "",
        dz: str = "",
        kinc: str = "",
        noelem: int | str = "",
        imove: int | str = "",
        **kwargs,
    ):
        r"""Generates additional volumes from a pattern of volumes.

        Mechanical APDL Command: `VGEN <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_VGEN.html>`_

        Parameters
        ----------
        itime : str
            Do this generation operation a total of ``ITIME`` s, incrementing all keypoints in the given
            pattern automatically (or by ``KINC`` ) each time after the first. ``ITIME`` must be > 1 for
            generation to occur.

        nv1 : str
            Generate volumes from pattern beginning with ``NV1`` to ``NV2`` (defaults to ``NV1`` ) in steps
            of ``NINC`` (defaults to 1). If ``NV1`` = ALL, ``NV2`` and ``NINC`` are ignored and the pattern
            is all selected volumes ( :ref:`vsel` ). If ``NV1`` = P, graphical picking is enabled and all
            remaining command fields are ignored (valid only in the GUI). A component name may also be
            substituted for ``NV1`` ( ``NV2`` and ``NINC`` are ignored).

        nv2 : str
            Generate volumes from pattern beginning with ``NV1`` to ``NV2`` (defaults to ``NV1`` ) in steps
            of ``NINC`` (defaults to 1). If ``NV1`` = ALL, ``NV2`` and ``NINC`` are ignored and the pattern
            is all selected volumes ( :ref:`vsel` ). If ``NV1`` = P, graphical picking is enabled and all
            remaining command fields are ignored (valid only in the GUI). A component name may also be
            substituted for ``NV1`` ( ``NV2`` and ``NINC`` are ignored).

        ninc : str
            Generate volumes from pattern beginning with ``NV1`` to ``NV2`` (defaults to ``NV1`` ) in steps
            of ``NINC`` (defaults to 1). If ``NV1`` = ALL, ``NV2`` and ``NINC`` are ignored and the pattern
            is all selected volumes ( :ref:`vsel` ). If ``NV1`` = P, graphical picking is enabled and all
            remaining command fields are ignored (valid only in the GUI). A component name may also be
            substituted for ``NV1`` ( ``NV2`` and ``NINC`` are ignored).

        dx : str
            Keypoint location increments in the active coordinate system (--, Dθ, DZ for cylindrical, --,
            Dθ, -- for spherical).

        dy : str
            Keypoint location increments in the active coordinate system (--, Dθ, DZ for cylindrical, --,
            Dθ, -- for spherical).

        dz : str
            Keypoint location increments in the active coordinate system (--, Dθ, DZ for cylindrical, --,
            Dθ, -- for spherical).

        kinc : str
            Keypoint increment between generated sets. If zero, the lowest available keypoint numbers are
            assigned ( :ref:`numstr` ).

        noelem : int or str
            Specifies if elements and nodes are also to be generated:

            * ``0`` - Generate nodes and elements associated with the original volumes, if they exist.

            * ``1`` - Do not generate nodes and elements.

        imove : int or str
            Specifies whether to redefine the existing volumes:

            * ``0`` - Generate additional volumes as requested with the ``ITIME`` argument.

            * ``1`` - Move original volumes to new position retaining the same keypoint line, and area numbers (
              ``ITIME``, ``KINC``, and ``NOELEM`` are ignored). Corresponding meshed items are also moved if not
              needed at their original position.

        Notes
        -----

        .. _VGEN_notes:

        Generates additional volumes (and their corresponding keypoints, lines, areas and mesh) from a given
        volume pattern. The MAT, TYPE, REAL, and ESYS attributes are based upon the volumes in the pattern
        and not upon the current settings of the pointers. End slopes of the generated lines remain the same
        (in the active coordinate system) as those of the given pattern. For example, radial slopes remain
        radial, etc. Generations which produce volumes of a size or shape different from the pattern (that
        is, radial generations in cylindrical systems, radial and phi generations in spherical systems, and
        theta generations in elliptical systems) are not allowed. Note that solid modeling in a toroidal
        coordinate system is not recommended. Volume, area, and line numbers are automatically assigned
        (beginning with the lowest available values ( :ref:`numstr` )).
        """
        command = (
            f"VGEN,{itime},{nv1},{nv2},{ninc},{dx},{dy},{dz},{kinc},{noelem},{imove}"
        )
        return self.run(command, **kwargs)

    def vlist(self, nv1: str = "", nv2: str = "", ninc: str = "", **kwargs):
        r"""Lists the defined volumes.

        Mechanical APDL Command: `VLIST <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_VLIST.html>`_

        Parameters
        ----------
        nv1 : str
            List volumes from ``NV1`` to ``NV2`` (defaults to ``NV1`` ) in steps of ``NINC`` (defaults to
            1). If ``NV1`` = ALL (default), ``NV2`` and ``NINC`` are ignored and all selected volumes (
            :ref:`vsel` ) are listed. If ``NV1`` = P, graphical picking is enabled and all remaining command
            fields are ignored (valid only in the GUI). A component name may also be substituted for ``NV1``
            ( ``NV2`` and ``NINC`` are ignored).

        nv2 : str
            List volumes from ``NV1`` to ``NV2`` (defaults to ``NV1`` ) in steps of ``NINC`` (defaults to
            1). If ``NV1`` = ALL (default), ``NV2`` and ``NINC`` are ignored and all selected volumes (
            :ref:`vsel` ) are listed. If ``NV1`` = P, graphical picking is enabled and all remaining command
            fields are ignored (valid only in the GUI). A component name may also be substituted for ``NV1``
            ( ``NV2`` and ``NINC`` are ignored).

        ninc : str
            List volumes from ``NV1`` to ``NV2`` (defaults to ``NV1`` ) in steps of ``NINC`` (defaults to
            1). If ``NV1`` = ALL (default), ``NV2`` and ``NINC`` are ignored and all selected volumes (
            :ref:`vsel` ) are listed. If ``NV1`` = P, graphical picking is enabled and all remaining command
            fields are ignored (valid only in the GUI). A component name may also be substituted for ``NV1``
            ( ``NV2`` and ``NINC`` are ignored).

        Notes
        -----

        .. _VLIST_notes:

        An attribute (TYPE, MAT, REAL, or ESYS) listed as a zero is unassigned; one listed as a positive
        value indicates that the attribute was assigned with the :ref:`vatt` command (and will not be reset
        to zero if the mesh is cleared); one listed as a negative value indicates that the attribute was
        assigned using the attribute pointer [TYPE, MAT, REAL, or ESYS] that was active during meshing (and
        will be reset to zero if the mesh is cleared). A "-1" in the "nodes" column indicates that the
        volume has been meshed but there are no interior nodes. The volume size is listed only if a
        :ref:`vsum` command has been performed on the volume. Volume orientation attributes (KZ1 and KZ2)
        are listed only if a :ref:`veorient` command was previously used to define an orientation for the
        volume.

        This command is valid in any processor.
        """
        command = f"VLIST,{nv1},{nv2},{ninc}"
        return self.run(command, **kwargs)

    def vlscale(
        self,
        nv1: str = "",
        nv2: str = "",
        ninc: str = "",
        rx: str = "",
        ry: str = "",
        rz: str = "",
        kinc: str = "",
        noelem: int | str = "",
        imove: int | str = "",
        **kwargs,
    ):
        r"""Generates a scaled set of volumes from a pattern of volumes.

        Mechanical APDL Command: `VLSCALE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_VLSCALE.html>`_

        Parameters
        ----------
        nv1 : str
            Set of volumes ( ``NV1`` to ``NV2`` in steps of ``NINC`` ) that defines the pattern to be
            scaled. ``NV2`` defaults to ``NV1``, ``NINC`` defaults to 1. If ``NV1`` = ALL, ``NV2`` and
            ``NINC`` are ignored and the pattern is defined by all selected volumes. If ``NV1`` = P,
            graphical picking is enabled and all remaining command fields are ignored (valid only in the
            GUI). A component name may also be substituted for ``NV1`` ( ``NV2`` and ``NINC`` are ignored).

        nv2 : str
            Set of volumes ( ``NV1`` to ``NV2`` in steps of ``NINC`` ) that defines the pattern to be
            scaled. ``NV2`` defaults to ``NV1``, ``NINC`` defaults to 1. If ``NV1`` = ALL, ``NV2`` and
            ``NINC`` are ignored and the pattern is defined by all selected volumes. If ``NV1`` = P,
            graphical picking is enabled and all remaining command fields are ignored (valid only in the
            GUI). A component name may also be substituted for ``NV1`` ( ``NV2`` and ``NINC`` are ignored).

        ninc : str
            Set of volumes ( ``NV1`` to ``NV2`` in steps of ``NINC`` ) that defines the pattern to be
            scaled. ``NV2`` defaults to ``NV1``, ``NINC`` defaults to 1. If ``NV1`` = ALL, ``NV2`` and
            ``NINC`` are ignored and the pattern is defined by all selected volumes. If ``NV1`` = P,
            graphical picking is enabled and all remaining command fields are ignored (valid only in the
            GUI). A component name may also be substituted for ``NV1`` ( ``NV2`` and ``NINC`` are ignored).

        rx : str
            Scale factors to be applied to the X, Y, and Z keypoint coordinates in active coordinate system
            ( RR, R θ, RZ for cylindrical; RR, R θ, R Φ for spherical). Note that the R θ and R Φ scale
            factors are interpreted as angular offsets. For example, if CSYS = 1, ``RX``, ``RY``, ``RZ``
            input of (1.5,10,3) would scale the specified keypoints 1.5 times in the radial and 3 times in
            the Z direction, while adding an offset of 10 degrees to the keypoints. Zero, blank, or negative
            scale factor values are assumed to be 1.0. Zero or blank angular offsets have no effect.

        ry : str
            Scale factors to be applied to the X, Y, and Z keypoint coordinates in active coordinate system
            ( RR, R θ, RZ for cylindrical; RR, R θ, R Φ for spherical). Note that the R θ and R Φ scale
            factors are interpreted as angular offsets. For example, if CSYS = 1, ``RX``, ``RY``, ``RZ``
            input of (1.5,10,3) would scale the specified keypoints 1.5 times in the radial and 3 times in
            the Z direction, while adding an offset of 10 degrees to the keypoints. Zero, blank, or negative
            scale factor values are assumed to be 1.0. Zero or blank angular offsets have no effect.

        rz : str
            Scale factors to be applied to the X, Y, and Z keypoint coordinates in active coordinate system
            ( RR, R θ, RZ for cylindrical; RR, R θ, R Φ for spherical). Note that the R θ and R Φ scale
            factors are interpreted as angular offsets. For example, if CSYS = 1, ``RX``, ``RY``, ``RZ``
            input of (1.5,10,3) would scale the specified keypoints 1.5 times in the radial and 3 times in
            the Z direction, while adding an offset of 10 degrees to the keypoints. Zero, blank, or negative
            scale factor values are assumed to be 1.0. Zero or blank angular offsets have no effect.

        kinc : str
            Increment to be applied to keypoint numbers for generated set. If zero, the lowest available
            keypoint numbers will be assigned ( :ref:`numstr` ).

        noelem : int or str
            Specifies whether nodes and elements are also to be generated:

            * ``0`` - Nodes and elements associated with the original volumes will be generated (scaled) if they
              exist.

            * ``1`` - Nodes and elements will not be generated.

        imove : int or str
            Specifies whether volumes will be moved or newly defined:

            * ``0`` - Additional volumes will be generated.

            * ``1`` - Original volumes will be moved to new position ( ``KINC`` and ``NOELEM`` are ignored). Use
              only if the old volumes are no longer needed at their original positions. Corresponding meshed items
              are also moved if not needed at their original position.

        Notes
        -----

        .. _VLSCALE_notes:

        Generates a scaled set of volumes (and their corresponding keypoints, lines, areas, and mesh) from a
        pattern of volumes. The MAT, TYPE, REAL, and ESYS attributes are based on the volumes in the pattern
        and not the current settings. Scaling is done in the active coordinate system. Volumes in the
        pattern could have been generated in any coordinate system. However, solid modeling in a toroidal
        coordinate system is not recommended.
        """
        command = f"VLSCALE,{nv1},{nv2},{ninc},{rx},{ry},{rz},{kinc},{noelem},{imove}"
        return self.run(command, **kwargs)

    def voffst(self, narea: str = "", dist: str = "", kinc: str = "", **kwargs):
        r"""Generates a volume, offset from a given area.

        Mechanical APDL Command: `VOFFST <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_VOFFST.html>`_

        Parameters
        ----------
        narea : str
            Area from which generated volume is to be offset. If ``NAREA`` = P, graphical picking is enabled
            and all remaining command fields are ignored (valid only in the GUI).

        dist : str
            Distance normal to given area at which keypoints for generated volume are to be located.
            Positive normal is determined from the right-hand rule keypoint order.

        kinc : str
            Increment to be applied to the keypoint numbers between sets. If zero, keypoint numbers will be
            automatically assigned beginning with the lowest available value ( :ref:`numstr` ).

        Notes
        -----

        .. _VOFFST_notes:

        Generates a volume (and its corresponding keypoints, lines, and areas) by offsetting from an area.
        The direction of the offset varies with the given area normal. End slopes of the generated lines
        remain the same as those of the given pattern.

        If element attributes have been associated with the input area via the :ref:`aatt` command, the
        opposite area generated by the :ref:`voffst` operation will also have those attributes (that is, the
        element attributes from the input area are copied to the opposite area). Note that only the area
        opposite the input area will have the same attributes as the input area; the areas adjacent to the
        input area will not.

        If the areas are meshed or belong to meshed volumes, a 3D mesh can be extruded with this command.
        Note that the ``NDIV`` argument on the :ref:`esize` command should be set before extruding the
        meshed areas.
        """
        command = f"VOFFST,{narea},{dist},{kinc}"
        return self.run(command, **kwargs)

    def vplot(
        self,
        nv1: str = "",
        nv2: str = "",
        ninc: str = "",
        degen: str = "",
        scale: str = "",
        **kwargs,
    ):
        r"""Displays the selected volumes.

        Mechanical APDL Command: `VPLOT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_VPLOT.html>`_

        Parameters
        ----------
        nv1 : str
            Display volumes from ``NV1`` to ``NV2`` (defaults to ``NV1`` ) in steps of ``NINC`` (defaults to
            1). If ``NV1`` = ALL (default), ``NV2`` and ``NINC`` are ignored and all selected volumes (
            :ref:`vsel` ) are displayed.

        nv2 : str
            Display volumes from ``NV1`` to ``NV2`` (defaults to ``NV1`` ) in steps of ``NINC`` (defaults to
            1). If ``NV1`` = ALL (default), ``NV2`` and ``NINC`` are ignored and all selected volumes (
            :ref:`vsel` ) are displayed.

        ninc : str
            Display volumes from ``NV1`` to ``NV2`` (defaults to ``NV1`` ) in steps of ``NINC`` (defaults to
            1). If ``NV1`` = ALL (default), ``NV2`` and ``NINC`` are ignored and all selected volumes (
            :ref:`vsel` ) are displayed.

        degen : str
            Degeneracy marker:

            * ``(blank)`` - No degeneracy marker is used (default).

            * ``DEGE`` - A red star is placed on keypoints at degeneracies (see the `Modeling and Meshing Guide <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD14.html>`_). Not available if
              :ref:`facet`,WIRE is set.

        scale : str
            Scale factor for the size of the degeneracy-marker star. The scale is the size in window space
            (-1 to 1 in both directions) (defaults to.075).

        Notes
        -----

        .. _VPLOT_notes:

        Displays selected volumes. (Only volumes having areas within the selected area set ( :ref:`asel` )
        will be plotted.) With PowerGraphics on ( :ref:`graphics`,POWER), :ref:`vplot` will display only the
        currently selected areas. This command is also a utility command, valid anywhere. The degree of
        tessellation used to plot the volumes is set through the :ref:`facet` command.
        """
        command = f"VPLOT,{nv1},{nv2},{ninc},{degen},{scale}"
        return self.run(command, **kwargs)

    def vrotat(
        self,
        na1: str = "",
        na2: str = "",
        na3: str = "",
        na4: str = "",
        na5: str = "",
        na6: str = "",
        pax1: str = "",
        pax2: str = "",
        arc: str = "",
        nseg: str = "",
        **kwargs,
    ):
        r"""Generates cylindrical volumes by rotating an area pattern about an axis.

        Mechanical APDL Command: `VROTAT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_VROTAT.html>`_

        Parameters
        ----------
        na1 : str
            List of areas in the pattern to be rotated (6 maximum if using keyboard entry). Areas must lie
            to one side of, and in the plane of, the axis of rotation. If ``NA1`` = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in the GUI). If ``NA1`` = ALL,
            all selected areas will define the pattern to be rotated. A component name may also be
            substituted for ``NA1``.

        na2 : str
            List of areas in the pattern to be rotated (6 maximum if using keyboard entry). Areas must lie
            to one side of, and in the plane of, the axis of rotation. If ``NA1`` = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in the GUI). If ``NA1`` = ALL,
            all selected areas will define the pattern to be rotated. A component name may also be
            substituted for ``NA1``.

        na3 : str
            List of areas in the pattern to be rotated (6 maximum if using keyboard entry). Areas must lie
            to one side of, and in the plane of, the axis of rotation. If ``NA1`` = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in the GUI). If ``NA1`` = ALL,
            all selected areas will define the pattern to be rotated. A component name may also be
            substituted for ``NA1``.

        na4 : str
            List of areas in the pattern to be rotated (6 maximum if using keyboard entry). Areas must lie
            to one side of, and in the plane of, the axis of rotation. If ``NA1`` = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in the GUI). If ``NA1`` = ALL,
            all selected areas will define the pattern to be rotated. A component name may also be
            substituted for ``NA1``.

        na5 : str
            List of areas in the pattern to be rotated (6 maximum if using keyboard entry). Areas must lie
            to one side of, and in the plane of, the axis of rotation. If ``NA1`` = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in the GUI). If ``NA1`` = ALL,
            all selected areas will define the pattern to be rotated. A component name may also be
            substituted for ``NA1``.

        na6 : str
            List of areas in the pattern to be rotated (6 maximum if using keyboard entry). Areas must lie
            to one side of, and in the plane of, the axis of rotation. If ``NA1`` = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in the GUI). If ``NA1`` = ALL,
            all selected areas will define the pattern to be rotated. A component name may also be
            substituted for ``NA1``.

        pax1 : str
            Keypoints defining the axis about which the area pattern is to be rotated.

        pax2 : str
            Keypoints defining the axis about which the area pattern is to be rotated.

        arc : str
            Arc length (in degrees). Positive follows right-hand rule about ``PAX1`` - ``PAX2`` vector.
            Defaults to 360.

        nseg : str
            Number of volumes (8 maximum) around circumference. Defaults to minimum required for 90°
            (maximum) arcs, that is, 4 for 360°, 3 for 270°, etc.

        Notes
        -----

        .. _VROTAT_notes:

        Generates cylindrical volumes (and their corresponding keypoints, lines, and areas) by rotating an
        area pattern (and its associated line and keypoint patterns) about an axis. Keypoint patterns are
        generated at regular angular locations (based on a maximum spacing of 90°). Line patterns are
        generated at the keypoint patterns. Arc lines are also generated to connect the keypoints
        circumferentially. Keypoint, line, area, and volume numbers are automatically assigned (beginning
        with the lowest available values). Adjacent lines use a common keypoint, adjacent areas use a common
        line, and adjacent volumes use a common area.

        To generate a single volume with an arc greater than 180°, ``NSEG`` must be greater than or equal to
        2.

        If element attributes have been associated with the input area via the :ref:`aatt` command, the
        opposite area generated by the :ref:`vrotat` operation will also have those attributes (that is, the
        element attributes from the input area are copied to the opposite area). Note that only the area
        opposite the input area will have the same attributes as the input area; the areas adjacent to the
        input area will not.

        If the given areas are meshed or belong to meshed volumes, the 2D mesh can be rotated (extruded) to
        a 3D mesh. See the `Modeling and Meshing Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD14.html>`_ for more
        information. Note that the ``NDIV`` argument on the
        :ref:`esize` command should be set before extruding the meshed areas.
        """
        command = (
            f"VROTAT,{na1},{na2},{na3},{na4},{na5},{na6},{pax1},{pax2},{arc},{nseg}"
        )
        return self.run(command, **kwargs)

    def vsum(self, lab: str = "", **kwargs):
        r"""Calculates and prints geometry statistics of the selected volumes.

        Mechanical APDL Command: `VSUM <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_VSUM.html>`_

        Parameters
        ----------
        lab : str
            Controls the degree of tessellation used in the calculation of area properties. If ``LAB`` =
            DEFAULT, area calculations will use the degree of tessellation set through the :ref:`facet`
            command. If ``LAB`` = FINE, area calculations are based on a finer tessellation.

        Notes
        -----

        .. _VSUM_notes:

        Calculates and prints geometry statistics (volume, centroid location, moments of inertia, etc.)
        associated with the selected volumes. Geometry items are reported in the global Cartesian coordinate
        system. A unit density is assumed unless the volumes have a material association via the :ref:`vatt`
        command. Items calculated by :ref:`vsum` and later retrieved by a :ref:`get` or :ref:`starvget`
        command are valid only if the model is not modified after the :ref:`vsum` command is issued.

        Setting a finer degree of tessellation will provide area calculations with greater accuracy,
        especially for thin, hollow models. However, using a finer degree of tessellation requires longer
        processing.

        For very thin volumes, such that the ratio of the minimum to the maximum dimension is less than
        0.01, the :ref:`vsum` command can provide erroneous volume information. To ensure that such
        calculations are accurate, make certain that you subdivide such volumes so that the ratio of the
        minimum to the maximum is at least 0.05.
        """
        command = f"VSUM,{lab}"
        return self.run(command, **kwargs)

    def vsymm(
        self,
        ncomp: str = "",
        nv1: str = "",
        nv2: str = "",
        ninc: str = "",
        kinc: str = "",
        noelem: int | str = "",
        imove: int | str = "",
        **kwargs,
    ):
        r"""Generates volumes from a volume pattern by symmetry reflection.

        Mechanical APDL Command: `VSYMM <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_VSYMM.html>`_

        Parameters
        ----------
        ncomp : str
            Symmetry key:

            * ``X`` - X symmetry (default).

            * ``Y`` - Y symmetry.

            * ``Z`` - Z symmetry.

        nv1 : str
            Reflect volumes from pattern beginning with ``NV1`` to ``NV2`` (defaults to ``NV1`` ) in steps
            of ``NINC`` (defaults to 1). If ``NV1`` = ALL, ``NV2`` and ``NINC`` are ignored and the pattern
            is all selected volumes ( :ref:`vsel` ). If ``NV1`` = P, graphical picking is enabled and all
            remaining command fields are ignored (valid only in the GUI). A component name may also be
            substituted for ``NV1`` ( ``NV2`` and ``NINC`` are ignored).

        nv2 : str
            Reflect volumes from pattern beginning with ``NV1`` to ``NV2`` (defaults to ``NV1`` ) in steps
            of ``NINC`` (defaults to 1). If ``NV1`` = ALL, ``NV2`` and ``NINC`` are ignored and the pattern
            is all selected volumes ( :ref:`vsel` ). If ``NV1`` = P, graphical picking is enabled and all
            remaining command fields are ignored (valid only in the GUI). A component name may also be
            substituted for ``NV1`` ( ``NV2`` and ``NINC`` are ignored).

        ninc : str
            Reflect volumes from pattern beginning with ``NV1`` to ``NV2`` (defaults to ``NV1`` ) in steps
            of ``NINC`` (defaults to 1). If ``NV1`` = ALL, ``NV2`` and ``NINC`` are ignored and the pattern
            is all selected volumes ( :ref:`vsel` ). If ``NV1`` = P, graphical picking is enabled and all
            remaining command fields are ignored (valid only in the GUI). A component name may also be
            substituted for ``NV1`` ( ``NV2`` and ``NINC`` are ignored).

        kinc : str
            Keypoint increment between sets. If zero, the lowest available keypoint numbers are assigned (
            :ref:`numstr` ).

        noelem : int or str
            Specifies whether nodes and elements are also to be generated:

            * ``0`` - Generate nodes and elements associated with the original volumes, if they exist.

            * ``1`` - Do not generate nodes and elements.

        imove : int or str
            Specifies whether volumes will be moved or newly defined:

            * ``0`` - Generate additional volumes.

            * ``1`` - Move original volumes to new position retaining the same keypoint numbers ( ``KINC`` and
              ``NOELEM`` are ignored). Corresponding meshed items are also moved if not needed at their original
              position.

        Notes
        -----

        .. _VSYMM_notes:

        Generates a reflected set of volumes (and their corresponding keypoints, lines, areas and mesh) from
        a given volume pattern by a symmetry reflection (see analogous node symmetry command, :ref:`nsym` ).
        The MAT, TYPE, REAL, and ESYS attributes are based upon the volumes in the pattern and not upon the
        current settings. Reflection is done in the active coordinate system by changing a particular
        coordinate sign. The active coordinate system must be a Cartesian system. Volumes in the pattern may
        have been generated in any coordinate system. However, solid modeling in a toroidal coordinate
        system is not recommended. Volumes are generated as described in the :ref:`vgen` command.

        See the :ref:`esym` command for additional information about symmetry elements.
        """
        command = f"VSYMM,{ncomp},{nv1},{nv2},{ninc},{kinc},{noelem},{imove}"
        return self.run(command, **kwargs)

    def vtran(
        self,
        kcnto: str = "",
        nv1: str = "",
        nv2: str = "",
        ninc: str = "",
        kinc: str = "",
        noelem: int | str = "",
        imove: int | str = "",
        **kwargs,
    ):
        r"""Transfers a pattern of volumes to another coordinate system.

        Mechanical APDL Command: `VTRAN <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_VTRAN.html>`_

        Parameters
        ----------
        kcnto : str
            Reference number of coordinate system where the pattern is to be transferred. Transfer occurs
            from the active coordinate system. The coordinate system type and parameters of ``KCNTO`` must
            be the same as the active system.

        nv1 : str
            Transfer volumes from pattern beginning with ``NV1`` to ``NV2`` (defaults to ``NV1`` ) in steps
            of ``NINC`` (defaults to 1). If ``NV1`` = ALL, ``NV2`` and ``NINC`` are ignored and the pattern
            is all selected volumes ( :ref:`vsel` ). If ``NV1`` = P, graphical picking is enabled and all
            remaining command fields are ignored (valid only in the GUI). A component name may also be
            substituted for ``NV1`` ( ``NV2`` and ``NINC`` are ignored).

        nv2 : str
            Transfer volumes from pattern beginning with ``NV1`` to ``NV2`` (defaults to ``NV1`` ) in steps
            of ``NINC`` (defaults to 1). If ``NV1`` = ALL, ``NV2`` and ``NINC`` are ignored and the pattern
            is all selected volumes ( :ref:`vsel` ). If ``NV1`` = P, graphical picking is enabled and all
            remaining command fields are ignored (valid only in the GUI). A component name may also be
            substituted for ``NV1`` ( ``NV2`` and ``NINC`` are ignored).

        ninc : str
            Transfer volumes from pattern beginning with ``NV1`` to ``NV2`` (defaults to ``NV1`` ) in steps
            of ``NINC`` (defaults to 1). If ``NV1`` = ALL, ``NV2`` and ``NINC`` are ignored and the pattern
            is all selected volumes ( :ref:`vsel` ). If ``NV1`` = P, graphical picking is enabled and all
            remaining command fields are ignored (valid only in the GUI). A component name may also be
            substituted for ``NV1`` ( ``NV2`` and ``NINC`` are ignored).

        kinc : str
            Keypoint increment between sets. If zero, the lowest available keypoint numbers are assigned (
            :ref:`numstr` ).

        noelem : int or str
            Specifies whether elements and nodes are also to be generated:

            * ``0`` - Generate nodes and elements associated with the original volumes, if they exist.

            * ``1`` - Do not generate nodes and elements.

        imove : int or str
            Specifies whether to redefine the existing volumes:

            * ``0`` - Generate additional volumes.

            * ``1`` - Move original volumes to new position retaining the same keypoint numbers ( ``KINC`` and
              ``NOELEM`` are ignored). Corresponding meshed items are also moved if not needed at their original
              position.

        Notes
        -----

        .. _VTRAN_notes:

        Transfers a pattern of volumes (and their corresponding keypoints, lines, areas and mesh) from one
        coordinate system to another (see analogous node transfer command, :ref:`transfer` ). The MAT, TYPE,
        REAL, and ESYS attributes are based upon the volumes in the pattern and not upon the current
        settings. Coordinate systems may be translated and rotated relative to each other. Initial pattern
        may be generated in any coordinate system. However, solid modeling in a toroidal coordinate system
        is not recommended. Coordinate and slope values are interpreted in the active coordinate system and
        are transferred directly. Volumes are generated as described in the :ref:`vgen` command.
        """
        command = f"VTRAN,{kcnto},{nv1},{nv2},{ninc},{kinc},{noelem},{imove}"
        return self.run(command, **kwargs)
