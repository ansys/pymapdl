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

from ansys.mapdl.core._commands import CommandsBase, parse


class Areas(CommandsBase):

    def a(
        self,
        p1: str = "",
        p2: str = "",
        p3: str = "",
        p4: str = "",
        p5: str = "",
        p6: str = "",
        p7: str = "",
        p8: str = "",
        p9: str = "",
        p10: str = "",
        p11: str = "",
        p12: str = "",
        p13: str = "",
        p14: str = "",
        p15: str = "",
        p16: str = "",
        p17: str = "",
        p18: str = "",
        **kwargs,
    ):
        r"""Defines an area by connecting keypoints.

        Mechanical APDL Command: `A <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_A.html>`_

        Parameters
        ----------
        p1 : str
            List of keypoints defining the area (18 maximum if using keyboard entry). At least 3 keypoints
            must be entered. If ``P1`` = P, graphical picking is enabled and all remaining arguments are
            ignored (valid only in the GUI).

        p2 : str
            List of keypoints defining the area (18 maximum if using keyboard entry). At least 3 keypoints
            must be entered. If ``P1`` = P, graphical picking is enabled and all remaining arguments are
            ignored (valid only in the GUI).

        p3 : str
            List of keypoints defining the area (18 maximum if using keyboard entry). At least 3 keypoints
            must be entered. If ``P1`` = P, graphical picking is enabled and all remaining arguments are
            ignored (valid only in the GUI).

        p4 : str
            List of keypoints defining the area (18 maximum if using keyboard entry). At least 3 keypoints
            must be entered. If ``P1`` = P, graphical picking is enabled and all remaining arguments are
            ignored (valid only in the GUI).

        p5 : str
            List of keypoints defining the area (18 maximum if using keyboard entry). At least 3 keypoints
            must be entered. If ``P1`` = P, graphical picking is enabled and all remaining arguments are
            ignored (valid only in the GUI).

        p6 : str
            List of keypoints defining the area (18 maximum if using keyboard entry). At least 3 keypoints
            must be entered. If ``P1`` = P, graphical picking is enabled and all remaining arguments are
            ignored (valid only in the GUI).

        p7 : str
            List of keypoints defining the area (18 maximum if using keyboard entry). At least 3 keypoints
            must be entered. If ``P1`` = P, graphical picking is enabled and all remaining arguments are
            ignored (valid only in the GUI).

        p8 : str
            List of keypoints defining the area (18 maximum if using keyboard entry). At least 3 keypoints
            must be entered. If ``P1`` = P, graphical picking is enabled and all remaining arguments are
            ignored (valid only in the GUI).

        p9 : str
            List of keypoints defining the area (18 maximum if using keyboard entry). At least 3 keypoints
            must be entered. If ``P1`` = P, graphical picking is enabled and all remaining arguments are
            ignored (valid only in the GUI).

        p10 : str
            List of keypoints defining the area (18 maximum if using keyboard entry). At least 3 keypoints
            must be entered. If ``P1`` = P, graphical picking is enabled and all remaining arguments are
            ignored (valid only in the GUI).

        p11 : str
            List of keypoints defining the area (18 maximum if using keyboard entry). At least 3 keypoints
            must be entered. If ``P1`` = P, graphical picking is enabled and all remaining arguments are
            ignored (valid only in the GUI).

        p12 : str
            List of keypoints defining the area (18 maximum if using keyboard entry). At least 3 keypoints
            must be entered. If ``P1`` = P, graphical picking is enabled and all remaining arguments are
            ignored (valid only in the GUI).

        p13 : str
            List of keypoints defining the area (18 maximum if using keyboard entry). At least 3 keypoints
            must be entered. If ``P1`` = P, graphical picking is enabled and all remaining arguments are
            ignored (valid only in the GUI).

        p14 : str
            List of keypoints defining the area (18 maximum if using keyboard entry). At least 3 keypoints
            must be entered. If ``P1`` = P, graphical picking is enabled and all remaining arguments are
            ignored (valid only in the GUI).

        p15 : str
            List of keypoints defining the area (18 maximum if using keyboard entry). At least 3 keypoints
            must be entered. If ``P1`` = P, graphical picking is enabled and all remaining arguments are
            ignored (valid only in the GUI).

        p16 : str
            List of keypoints defining the area (18 maximum if using keyboard entry). At least 3 keypoints
            must be entered. If ``P1`` = P, graphical picking is enabled and all remaining arguments are
            ignored (valid only in the GUI).

        p17 : str
            List of keypoints defining the area (18 maximum if using keyboard entry). At least 3 keypoints
            must be entered. If ``P1`` = P, graphical picking is enabled and all remaining arguments are
            ignored (valid only in the GUI).

        p18 : str
            List of keypoints defining the area (18 maximum if using keyboard entry). At least 3 keypoints
            must be entered. If ``P1`` = P, graphical picking is enabled and all remaining arguments are
            ignored (valid only in the GUI).

        Returns
        -------
        int
            The area number of the generated area.

        Notes
        -----

        .. _A_notes:

        Keypoints ( ``P1`` through ``P18`` ) must be input in a clockwise or counterclockwise order around
        the area. This order also determines the positive normal direction of the area according to the
        right-hand rule. Existing lines between adjacent keypoints will be used; missing lines are generated
        "straight" in the active coordinate system and assigned the lowest available numbers ( :ref:`numstr`
        ). If more than one line exists between two keypoints, the shorter one will be chosen. If the area
        is to be defined with more than four keypoints, the required keypoints and lines must lie on a
        constant coordinate value in the active coordinate system (such as a plane or a cylinder). Areas may
        be redefined only if not yet attached to a volume. Solid modeling in a toroidal coordinate system is
        not recommended.

        Examples
        --------
        Create a simple triangle in the XY plane using three keypoints.

        >>> k0 = mapdl.k("", 0, 0, 0)
        >>> k1 = mapdl.k("", 1, 0, 0)
        >>> k2 = mapdl.k("", 0, 1, 0)
        >>> a0 = mapdl.a(k0, k1, k2)
        >>> a0
        1
        """
        command = f"A,{p1},{p2},{p3},{p4},{p5},{p6},{p7},{p8},{p9},{p10},{p11},{p12},{p13},{p14},{p15},{p16},{p17},{p18}"
        return parse.parse_a(self.run(command, **kwargs))

    def adele(
        self,
        na1: str = "",
        na2: str = "",
        ninc: str = "",
        kswp: int | str = "",
        **kwargs,
    ):
        r"""Deletes unmeshed areas.

        Mechanical APDL Command: `ADELE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ADELE.html>`_

        Parameters
        ----------
        na1 : str
            Delete areas from ``NA1`` to ``NA2`` (defaults to ``NA1`` ) in steps of ``NINC`` (defaults to
            1). If ``NA1`` = ALL, ``NA2`` and ``NINC`` are ignored and all selected areas ( :ref:`asel` )
            are deleted. If ``NA1`` = P, graphical picking is enabled and all remaining arguments are
            ignored (valid only in the GUI). A component name may also be substituted for ``NA1`` ( ``NA2``
            and ``NINC`` are ignored).

        na2 : str
            Delete areas from ``NA1`` to ``NA2`` (defaults to ``NA1`` ) in steps of ``NINC`` (defaults to
            1). If ``NA1`` = ALL, ``NA2`` and ``NINC`` are ignored and all selected areas ( :ref:`asel` )
            are deleted. If ``NA1`` = P, graphical picking is enabled and all remaining arguments are
            ignored (valid only in the GUI). A component name may also be substituted for ``NA1`` ( ``NA2``
            and ``NINC`` are ignored).

        ninc : str
            Delete areas from ``NA1`` to ``NA2`` (defaults to ``NA1`` ) in steps of ``NINC`` (defaults to
            1). If ``NA1`` = ALL, ``NA2`` and ``NINC`` are ignored and all selected areas ( :ref:`asel` )
            are deleted. If ``NA1`` = P, graphical picking is enabled and all remaining arguments are
            ignored (valid only in the GUI). A component name may also be substituted for ``NA1`` ( ``NA2``
            and ``NINC`` are ignored).

        kswp : int or str
            Specifies whether keypoints and lines are also to be deleted:

            * ``0`` - Delete areas only (default).

            * ``1`` - Delete areas, as well as keypoints and lines attached to specified areas but not shared by
              other areas.

        Notes
        -----

        .. _ADELE_notes:

        An area attached to a volume cannot be deleted unless the volume is first deleted.
        """
        command = f"ADELE,{na1},{na2},{ninc},{kswp}"
        return self.run(command, **kwargs)

    def adgl(self, na1: str = "", na2: str = "", ninc: str = "", **kwargs):
        r"""Lists keypoints of an area that lie on a parametric degeneracy.

        Mechanical APDL Command: `ADGL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ADGL.html>`_

        Parameters
        ----------
        na1 : str
            List keypoints that lie on a parametric degeneracy on areas from ``NA1`` to ``NA2`` (defaults to
            ``NA1`` ) in steps of ``NINC`` (defaults to 1). If ``NA1`` = ALL (default), ``NA2`` and ``NINC``
            will be ignored and keypoints on all selected areas ( :ref:`asel` ) will be listed. If ``NA1`` =
            P, graphical picking is enabled and all remaining arguments are ignored (valid only in the GUI).
            A component name may be substituted in ``NA1`` ( ``NA2`` and ``NINC`` will be ignored).

        na2 : str
            List keypoints that lie on a parametric degeneracy on areas from ``NA1`` to ``NA2`` (defaults to
            ``NA1`` ) in steps of ``NINC`` (defaults to 1). If ``NA1`` = ALL (default), ``NA2`` and ``NINC``
            will be ignored and keypoints on all selected areas ( :ref:`asel` ) will be listed. If ``NA1`` =
            P, graphical picking is enabled and all remaining arguments are ignored (valid only in the GUI).
            A component name may be substituted in ``NA1`` ( ``NA2`` and ``NINC`` will be ignored).

        ninc : str
            List keypoints that lie on a parametric degeneracy on areas from ``NA1`` to ``NA2`` (defaults to
            ``NA1`` ) in steps of ``NINC`` (defaults to 1). If ``NA1`` = ALL (default), ``NA2`` and ``NINC``
            will be ignored and keypoints on all selected areas ( :ref:`asel` ) will be listed. If ``NA1`` =
            P, graphical picking is enabled and all remaining arguments are ignored (valid only in the GUI).
            A component name may be substituted in ``NA1`` ( ``NA2`` and ``NINC`` will be ignored).

        Notes
        -----

        .. _ADGL_notes:

        See the `Modeling and Meshing Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD14.html>`_ for details on
        parametric degeneracies.

        This command is valid in any processor.
        """
        command = f"ADGL,{na1},{na2},{ninc}"
        return self.run(command, **kwargs)

    def adrag(
        self,
        nl1: str = "",
        nl2: str = "",
        nl3: str = "",
        nl4: str = "",
        nl5: str = "",
        nl6: str = "",
        nlp1: str = "",
        nlp2: str = "",
        nlp3: str = "",
        nlp4: str = "",
        nlp5: str = "",
        nlp6: str = "",
        **kwargs,
    ):
        r"""Generates areas by dragging a line pattern along a path.

        Mechanical APDL Command: `ADRAG <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ADRAG.html>`_

        Parameters
        ----------
        nl1 : str
            List of lines in the pattern to be dragged (6 maximum if using keyboard entry). Lines should
            form a continuous pattern (no more than two lines connected to any one keypoint. If ``NL1`` = P,
            graphical picking is enabled and all remaining arguments are ignored (valid only in the GUI). If
            ``NL1`` = ALL, all selected lines (except those that define the drag path) will be swept along
            the path. A component name may also be substituted for ``NL1``.

        nl2 : str
            List of lines in the pattern to be dragged (6 maximum if using keyboard entry). Lines should
            form a continuous pattern (no more than two lines connected to any one keypoint. If ``NL1`` = P,
            graphical picking is enabled and all remaining arguments are ignored (valid only in the GUI). If
            ``NL1`` = ALL, all selected lines (except those that define the drag path) will be swept along
            the path. A component name may also be substituted for ``NL1``.

        nl3 : str
            List of lines in the pattern to be dragged (6 maximum if using keyboard entry). Lines should
            form a continuous pattern (no more than two lines connected to any one keypoint. If ``NL1`` = P,
            graphical picking is enabled and all remaining arguments are ignored (valid only in the GUI). If
            ``NL1`` = ALL, all selected lines (except those that define the drag path) will be swept along
            the path. A component name may also be substituted for ``NL1``.

        nl4 : str
            List of lines in the pattern to be dragged (6 maximum if using keyboard entry). Lines should
            form a continuous pattern (no more than two lines connected to any one keypoint. If ``NL1`` = P,
            graphical picking is enabled and all remaining arguments are ignored (valid only in the GUI). If
            ``NL1`` = ALL, all selected lines (except those that define the drag path) will be swept along
            the path. A component name may also be substituted for ``NL1``.

        nl5 : str
            List of lines in the pattern to be dragged (6 maximum if using keyboard entry). Lines should
            form a continuous pattern (no more than two lines connected to any one keypoint. If ``NL1`` = P,
            graphical picking is enabled and all remaining arguments are ignored (valid only in the GUI). If
            ``NL1`` = ALL, all selected lines (except those that define the drag path) will be swept along
            the path. A component name may also be substituted for ``NL1``.

        nl6 : str
            List of lines in the pattern to be dragged (6 maximum if using keyboard entry). Lines should
            form a continuous pattern (no more than two lines connected to any one keypoint. If ``NL1`` = P,
            graphical picking is enabled and all remaining arguments are ignored (valid only in the GUI). If
            ``NL1`` = ALL, all selected lines (except those that define the drag path) will be swept along
            the path. A component name may also be substituted for ``NL1``.

        nlp1 : str
            List of lines defining the path along which the pattern is to be dragged (6 maximum if using
            keyboard entry). Must be a continuous set of lines.

        nlp2 : str
            List of lines defining the path along which the pattern is to be dragged (6 maximum if using
            keyboard entry). Must be a continuous set of lines.

        nlp3 : str
            List of lines defining the path along which the pattern is to be dragged (6 maximum if using
            keyboard entry). Must be a continuous set of lines.

        nlp4 : str
            List of lines defining the path along which the pattern is to be dragged (6 maximum if using
            keyboard entry). Must be a continuous set of lines.

        nlp5 : str
            List of lines defining the path along which the pattern is to be dragged (6 maximum if using
            keyboard entry). Must be a continuous set of lines.

        nlp6 : str
            List of lines defining the path along which the pattern is to be dragged (6 maximum if using
            keyboard entry). Must be a continuous set of lines.

        Notes
        -----

        .. _ADRAG_notes:

        Generates areas (and their corresponding keypoints and lines) by sweeping a given line pattern along
        a characteristic drag path. If the drag path consists of multiple lines, the drag direction is
        determined by the sequence in which the path lines are input ( ``NLP1``, ``NLP2``, etc.). If the
        drag path is a single line ( ``NLP1`` ), the drag direction is from the keypoint on the drag line
        that is closest to the first keypoint of the given line pattern to the other end of the drag line.

        The magnitude of the vector between the keypoints of the given pattern and the first path keypoint
        remains constant for all generated keypoint patterns and the path keypoints. The direction of the
        vector relative to the path slope also remains constant so that patterns may be swept around curves.

        Keypoint, line, and area numbers are automatically assigned, beginning with the lowest available
        values ( :ref:`numstr` ). Adjacent lines use a common keypoint. Adjacent areas use a common line.
        For best results, the entities to be dragged should be orthogonal to the start of the drag path.
        Drag operations that produce an error message may create some of the desired entities prior to
        terminating.
        """
        command = f"ADRAG,{nl1},{nl2},{nl3},{nl4},{nl5},{nl6},{nlp1},{nlp2},{nlp3},{nlp4},{nlp5},{nlp6}"
        return self.run(command, **kwargs)

    def afillt(self, na1: str = "", na2: str = "", rad: str = "", **kwargs):
        r"""Generates a fillet at the intersection of two areas.

        Mechanical APDL Command: `AFILLT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_AFILLT.html>`_

        Parameters
        ----------
        na1 : str
            Number of the first intersecting area. If ``NA1`` = P, graphical picking is enabled and all
            remaining arguments are ignored (valid only in the GUI).

        na2 : str
            Number of the second intersecting area.

        rad : str
            Radius of fillet to be generated.

        Notes
        -----

        .. _AFILLT_notes:

        Generates an area of constant fillet radius at the intersection of two areas using a series of
        Boolean operations. Corresponding lines and keypoints are also generated. See :ref:`boptn` command
        for an explanation of the options available to Boolean operations. If areas do not initially
        intersect at a common line, use the :ref:`aina` command.
        """
        command = f"AFILLT,{na1},{na2},{rad}"
        return self.run(command, **kwargs)

    def agen(
        self,
        itime: str = "",
        na1: str = "",
        na2: str = "",
        ninc: str = "",
        dx: str = "",
        dy: str = "",
        dz: str = "",
        kinc: str = "",
        noelem: int | str = "",
        imove: int | str = "",
        **kwargs,
    ):
        r"""Generates additional areas from a pattern of areas.

        Mechanical APDL Command: `AGEN <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_AGEN.html>`_

        Parameters
        ----------
        itime : str
            Do this generation operation a total of ``ITIME`` s, incrementing all keypoints in the given
            pattern automatically (or by ``KINC`` ) each time after the first. ``ITIME`` must be more than 1
            for generation to occur.

        na1 : str
            Generate areas from the pattern of areas ``NA1`` to ``NA2`` (defaults to ``NA1`` ) in steps of
            ``NINC`` (defaults to 1). If ``NA1`` = ALL, ``NA2`` and ``NINC`` are ignored and the pattern is
            all selected areas ( :ref:`asel` ). If ``NA1`` = P, graphical picking is enabled and all
            remaining arguments are ignored (valid only in the GUI). A component name may also be
            substituted for ``NA1`` ( ``NA2`` and ``NINC`` are ignored).

        na2 : str
            Generate areas from the pattern of areas ``NA1`` to ``NA2`` (defaults to ``NA1`` ) in steps of
            ``NINC`` (defaults to 1). If ``NA1`` = ALL, ``NA2`` and ``NINC`` are ignored and the pattern is
            all selected areas ( :ref:`asel` ). If ``NA1`` = P, graphical picking is enabled and all
            remaining arguments are ignored (valid only in the GUI). A component name may also be
            substituted for ``NA1`` ( ``NA2`` and ``NINC`` are ignored).

        ninc : str
            Generate areas from the pattern of areas ``NA1`` to ``NA2`` (defaults to ``NA1`` ) in steps of
            ``NINC`` (defaults to 1). If ``NA1`` = ALL, ``NA2`` and ``NINC`` are ignored and the pattern is
            all selected areas ( :ref:`asel` ). If ``NA1`` = P, graphical picking is enabled and all
            remaining arguments are ignored (valid only in the GUI). A component name may also be
            substituted for ``NA1`` ( ``NA2`` and ``NINC`` are ignored).

        dx : str
            Keypoint location increments in the active coordinate system (--, D θ, DZ for cylindrical; --, D
            θ, -- for spherical).

        dy : str
            Keypoint location increments in the active coordinate system (--, D θ, DZ for cylindrical; --, D
            θ, -- for spherical).

        dz : str
            Keypoint location increments in the active coordinate system (--, D θ, DZ for cylindrical; --, D
            θ, -- for spherical).

        kinc : str
            Keypoint number increment between generated sets. If zero, the lowest available keypoint numbers
            are assigned ( :ref:`numstr` }.

        noelem : int or str
            Specifies if elements and nodes are also to be generated:

            * ``0`` - Generate nodes and elements associated with the original areas, if they exist.

            * ``1`` - Do not generate nodes and elements.

        imove : int or str
            Specifies whether to redefine the existing areas:

            * ``0`` - Generate new areas as requested with the ``ITIME`` argument.

            * ``1`` - Move original areas to new position, retaining the same keypoint numbers ( ``ITIME``,
              ``KINC``, and ``NOELEM`` are ignored). If the original areas are needed in the original position
              (for example, they may be attached to a volume), they are not moved, and new areas are generated
              instead. Meshed items corresponding to moved areas are also moved if not needed at their original
              position.

        Notes
        -----

        .. _AGEN_notes:

        Generates additional areas (and their corresponding keypoints, lines and mesh) from a given area
        pattern. The MAT, TYPE, REAL, ESYS, and SECNUM attributes of the new areas are based upon the areas
        in the pattern and not upon the current settings of the pointers. End slopes of the generated lines
        remain the same (in the active coordinate system) as those of the given pattern. For example, radial
        slopes remain radial. Generations which produce areas of a size or shape different from the pattern
        (that is, radial generations in cylindrical systems, radial and phi generations in spherical
        systems, and theta generations in elliptical systems) are not allowed. Solid modeling in a toroidal
        coordinate system is not recommended. Area and line numbers are automatically assigned, beginning
        with the lowest available values ( :ref:`numstr` ).
        """
        command = (
            f"AGEN,{itime},{na1},{na2},{ninc},{dx},{dy},{dz},{kinc},{noelem},{imove}"
        )
        return self.run(command, **kwargs)

    def al(
        self,
        l1: str = "",
        l2: str = "",
        l3: str = "",
        l4: str = "",
        l5: str = "",
        l6: str = "",
        l7: str = "",
        l8: str = "",
        l9: str = "",
        l10: str = "",
        **kwargs,
    ):
        r"""Generates an area bounded by previously defined lines.

        Mechanical APDL Command: `AL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_AL.html>`_

        Parameters
        ----------
        l1 : str
            List of lines defining area. The minimum number of lines is 3. The positive normal of the area
            is controlled by the direction of ``L1`` using the right-hand rule. A negative value of ``L1``
            reverses the normal direction. If ``L1`` = ALL, use all selected lines with ``L2`` defining the
            normal ( ``L3`` to ``L10`` are ignored and ``L2`` defaults to the lowest numbered selected
            line). If ``L1`` = P, graphical picking is enabled and all remaining arguments are ignored
            (valid only in the GUI). A component name may also be substituted for ``L1``.

        l2 : str
            List of lines defining area. The minimum number of lines is 3. The positive normal of the area
            is controlled by the direction of ``L1`` using the right-hand rule. A negative value of ``L1``
            reverses the normal direction. If ``L1`` = ALL, use all selected lines with ``L2`` defining the
            normal ( ``L3`` to ``L10`` are ignored and ``L2`` defaults to the lowest numbered selected
            line). If ``L1`` = P, graphical picking is enabled and all remaining arguments are ignored
            (valid only in the GUI). A component name may also be substituted for ``L1``.

        l3 : str
            List of lines defining area. The minimum number of lines is 3. The positive normal of the area
            is controlled by the direction of ``L1`` using the right-hand rule. A negative value of ``L1``
            reverses the normal direction. If ``L1`` = ALL, use all selected lines with ``L2`` defining the
            normal ( ``L3`` to ``L10`` are ignored and ``L2`` defaults to the lowest numbered selected
            line). If ``L1`` = P, graphical picking is enabled and all remaining arguments are ignored
            (valid only in the GUI). A component name may also be substituted for ``L1``.

        l4 : str
            List of lines defining area. The minimum number of lines is 3. The positive normal of the area
            is controlled by the direction of ``L1`` using the right-hand rule. A negative value of ``L1``
            reverses the normal direction. If ``L1`` = ALL, use all selected lines with ``L2`` defining the
            normal ( ``L3`` to ``L10`` are ignored and ``L2`` defaults to the lowest numbered selected
            line). If ``L1`` = P, graphical picking is enabled and all remaining arguments are ignored
            (valid only in the GUI). A component name may also be substituted for ``L1``.

        l5 : str
            List of lines defining area. The minimum number of lines is 3. The positive normal of the area
            is controlled by the direction of ``L1`` using the right-hand rule. A negative value of ``L1``
            reverses the normal direction. If ``L1`` = ALL, use all selected lines with ``L2`` defining the
            normal ( ``L3`` to ``L10`` are ignored and ``L2`` defaults to the lowest numbered selected
            line). If ``L1`` = P, graphical picking is enabled and all remaining arguments are ignored
            (valid only in the GUI). A component name may also be substituted for ``L1``.

        l6 : str
            List of lines defining area. The minimum number of lines is 3. The positive normal of the area
            is controlled by the direction of ``L1`` using the right-hand rule. A negative value of ``L1``
            reverses the normal direction. If ``L1`` = ALL, use all selected lines with ``L2`` defining the
            normal ( ``L3`` to ``L10`` are ignored and ``L2`` defaults to the lowest numbered selected
            line). If ``L1`` = P, graphical picking is enabled and all remaining arguments are ignored
            (valid only in the GUI). A component name may also be substituted for ``L1``.

        l7 : str
            List of lines defining area. The minimum number of lines is 3. The positive normal of the area
            is controlled by the direction of ``L1`` using the right-hand rule. A negative value of ``L1``
            reverses the normal direction. If ``L1`` = ALL, use all selected lines with ``L2`` defining the
            normal ( ``L3`` to ``L10`` are ignored and ``L2`` defaults to the lowest numbered selected
            line). If ``L1`` = P, graphical picking is enabled and all remaining arguments are ignored
            (valid only in the GUI). A component name may also be substituted for ``L1``.

        l8 : str
            List of lines defining area. The minimum number of lines is 3. The positive normal of the area
            is controlled by the direction of ``L1`` using the right-hand rule. A negative value of ``L1``
            reverses the normal direction. If ``L1`` = ALL, use all selected lines with ``L2`` defining the
            normal ( ``L3`` to ``L10`` are ignored and ``L2`` defaults to the lowest numbered selected
            line). If ``L1`` = P, graphical picking is enabled and all remaining arguments are ignored
            (valid only in the GUI). A component name may also be substituted for ``L1``.

        l9 : str
            List of lines defining area. The minimum number of lines is 3. The positive normal of the area
            is controlled by the direction of ``L1`` using the right-hand rule. A negative value of ``L1``
            reverses the normal direction. If ``L1`` = ALL, use all selected lines with ``L2`` defining the
            normal ( ``L3`` to ``L10`` are ignored and ``L2`` defaults to the lowest numbered selected
            line). If ``L1`` = P, graphical picking is enabled and all remaining arguments are ignored
            (valid only in the GUI). A component name may also be substituted for ``L1``.

        l10 : str
            List of lines defining area. The minimum number of lines is 3. The positive normal of the area
            is controlled by the direction of ``L1`` using the right-hand rule. A negative value of ``L1``
            reverses the normal direction. If ``L1`` = ALL, use all selected lines with ``L2`` defining the
            normal ( ``L3`` to ``L10`` are ignored and ``L2`` defaults to the lowest numbered selected
            line). If ``L1`` = P, graphical picking is enabled and all remaining arguments are ignored
            (valid only in the GUI). A component name may also be substituted for ``L1``.

        Returns
        -------
        int
            Area number of the generated area.

        Notes
        -----

        .. _AL_notes:

        Lines may be input (once each) in any order and must form a simply connected closed curve. If the
        area is defined with more than four lines, the lines must also lie in the same plane or on a
        constant coordinate value in the active coordinate system (such as a plane or a cylinder). Solid
        modeling in a toroidal coordinate system is not recommended. Areas may be redefined only if not yet
        attached to a volume.

        This command is valid in any processor.

        Examples
        --------
        Create an area from four lines

        >>> k0 = mapdl.k("", 0, 0, 0)
        >>> k1 = mapdl.k("", 1, 0, 0)
        >>> k2 = mapdl.k("", 1, 1, 0)
        >>> k3 = mapdl.k("", 0, 1, 0)
        >>> l0 = mapdl.l(k0, k1)
        >>> l1 = mapdl.l(k1, k2)
        >>> l2 = mapdl.l(k2, k3)
        >>> l3 = mapdl.l(k3, k0)
        >>> anum = mapdl.al(l0, l1, l2, l3)
        >>> anum
        1
        """
        command = f"AL,{l1},{l2},{l3},{l4},{l5},{l6},{l7},{l8},{l9},{l10}"
        return parse.parse_a(self.run(command, **kwargs))

    def alist(
        self, na1: str = "", na2: str = "", ninc: str = "", lab: str = "", **kwargs
    ):
        r"""Lists the defined areas.

        Mechanical APDL Command: `ALIST <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ALIST.html>`_

        Parameters
        ----------
        na1 : str
            List areas from ``NA1`` to ``NA2`` (defaults to ``NA1`` ) in steps of ``NINC`` (defaults to 1).
            If ``NA1`` = ALL (default), ``NA2`` and ``NINC`` are ignored and all selected areas (
            :ref:`asel` ) are listed. If ``NA1`` = P, graphical picking is enabled and all remaining
            arguments are ignored (valid only in the GUI). A component name may also be substituted for
            ``NA1`` ( ``NA2`` and ``NINC`` are ignored).

        na2 : str
            List areas from ``NA1`` to ``NA2`` (defaults to ``NA1`` ) in steps of ``NINC`` (defaults to 1).
            If ``NA1`` = ALL (default), ``NA2`` and ``NINC`` are ignored and all selected areas (
            :ref:`asel` ) are listed. If ``NA1`` = P, graphical picking is enabled and all remaining
            arguments are ignored (valid only in the GUI). A component name may also be substituted for
            ``NA1`` ( ``NA2`` and ``NINC`` are ignored).

        ninc : str
            List areas from ``NA1`` to ``NA2`` (defaults to ``NA1`` ) in steps of ``NINC`` (defaults to 1).
            If ``NA1`` = ALL (default), ``NA2`` and ``NINC`` are ignored and all selected areas (
            :ref:`asel` ) are listed. If ``NA1`` = P, graphical picking is enabled and all remaining
            arguments are ignored (valid only in the GUI). A component name may also be substituted for
            ``NA1`` ( ``NA2`` and ``NINC`` are ignored).

        lab : str
            Determines what type of listing is used (one of the following):

            * ``(blank)`` - Prints information about all areas in the specified range.

            * ``HPT`` - Prints information about only those areas that contain hard points.

        Notes
        -----

        .. _ALIST_notes:

        An attribute (TYPE, MAT, REAL, or ESYS) listed as a zero is unassigned; one listed as a positive
        value indicates that the attribute was assigned with the :ref:`aatt` command (and will not be reset
        to zero if the mesh is cleared); one listed as a negative value indicates that the attribute was
        assigned using the attribute pointer ( :ref:`type`, :ref:`mat`, :ref:`real`, or :ref:`esys` ) that
        was active during meshing (and will be reset to zero if the mesh is cleared). A "-1" in the "nodes"
        column indicates that the area has been meshed but there are no interior nodes. The area size is
        listed only if an :ref:`asum` command has been performed on the area.
        """
        command = f"ALIST,{na1},{na2},{ninc},{lab}"
        return self.run(command, **kwargs)

    def anorm(self, anum: str = "", noeflip: int | str = "", **kwargs):
        r"""Reorients area normals.

        Mechanical APDL Command: `ANORM <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ANORM.html>`_

        Parameters
        ----------
        anum : str
            Area number having the normal direction that the reoriented areas are to match.

        noeflip : int or str
            Indicates whether you want to change the normal direction of the existing elements on the reoriented
            area(s) so that they are consistent with each area's new normal direction.

            * ``0`` - Make the normal direction of existing elements on the reoriented area(s) consistent with
              each area's new normal direction (default).

            * ``1`` - Do not change the normal direction of existing elements on the reoriented area(s).

        Notes
        -----

        .. _ANORM_notes:

        Reorients areas so that their normals are consistent with that of a specified area.

        If any of the areas have inner loops, the :ref:`anorm` command will consider the inner loops when it
        reorients the area normals.

        You cannot use the :ref:`anorm` command to change the normal direction of any element that has a
        body or surface load. We recommend that you apply all of your loads only after ensuring that the
        element normal directions are acceptable.

        Real constants (such as nonuniform shell thickness and tapered beam constants) may be invalidated by
        an element reversal.

        See `Revising Your Model
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD8_6.html>`_  of the
        `Modeling and Meshing Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD14.html>`_ for more
        information.
        """
        command = f"ANORM,{anum},{noeflip}"
        return self.run(command, **kwargs)

    def aoffst(self, narea: str = "", dist: str = "", kinc: str = "", **kwargs):
        r"""Generates an area, offset from a given area.

        Mechanical APDL Command: `AOFFST <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_AOFFST.html>`_

        Parameters
        ----------
        narea : str
            Area from which generated area is to be offset. If ``NAREA`` = ALL, offset from all selected
            areas ( :ref:`asel` ). If ``NAREA`` = P, graphical picking is enabled and all remaining
            arguments are ignored (valid only in the GUI).

        dist : str
            Distance normal to given area at which keypoints for generated area are to be located. Positive
            normal is determined from the right-hand-rule keypoint order.

        kinc : str
            Keypoint increment between areas. If zero, the lowest available keypoint numbers are assigned (
            :ref:`numstr` ).

        Notes
        -----

        .. _AOFFST_notes:

        Generates an area (and its corresponding keypoints and lines) offset from a given area. The
        direction of the offset varies with the given area normal. End slopes of the generated lines remain
        the same as those of the given pattern. Area and line numbers are automatically assigned, beginning
        with the lowest available values ( :ref:`numstr` ).
        """
        command = f"AOFFST,{narea},{dist},{kinc}"
        return self.run(command, **kwargs)

    def aplot(
        self,
        na1: str = "",
        na2: str = "",
        ninc: str = "",
        degen: str = "",
        scale: str = "",
        **kwargs,
    ):
        r"""Displays the selected areas.

        Mechanical APDL Command: `APLOT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_APLOT.html>`_

        Parameters
        ----------
        na1 : str
            Displays areas from ``NA1`` to ``NA2`` (defaults to ``NA1`` ) in steps of ``NINC`` (defaults to
            1). If ``NA1`` = ALL (default), ``NA2`` and ``NINC`` are ignored and all selected areas (
            :ref:`asel` ) are displayed.

        na2 : str
            Displays areas from ``NA1`` to ``NA2`` (defaults to ``NA1`` ) in steps of ``NINC`` (defaults to
            1). If ``NA1`` = ALL (default), ``NA2`` and ``NINC`` are ignored and all selected areas (
            :ref:`asel` ) are displayed.

        ninc : str
            Displays areas from ``NA1`` to ``NA2`` (defaults to ``NA1`` ) in steps of ``NINC`` (defaults to
            1). If ``NA1`` = ALL (default), ``NA2`` and ``NINC`` are ignored and all selected areas (
            :ref:`asel` ) are displayed.

        degen : str
            Degeneracy marker:

            * ``(blank)`` - No degeneracy marker is used (default).

            * ``DEGE`` - A red star is placed on keypoints at degeneracies (see the `Modeling and Meshing Guide <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD14.html>`_ ). Not available if
              :ref:`facet`,WIRE is set.

        scale : str
            Scale factor for the size of the degeneracy-marker star. The scale is the size in window space
            (-1 to 1 in both directions) (defaults to.075).

        Notes
        -----

        .. _APLOT_notes:

        This command is valid in any processor. The degree of tessellation used to plot the selected areas
        is set through the :ref:`facet` command.
        """
        command = f"APLOT,{na1},{na2},{ninc},{degen},{scale}"
        return self.run(command, **kwargs)

    def areverse(self, anum: str = "", noeflip: int | str = "", **kwargs):
        r"""Reverses the normal of an area, regardless of its connectivity or mesh status.

        Mechanical APDL Command: `AREVERSE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_AREVERSE.html>`_

        Parameters
        ----------
        anum : str
            Area number of the area whose normal is to be reversed. If ``ANUM`` = ALL, the normals of all
            selected areas will be reversed. If ``ANUM`` = P, graphical picking is enabled. A component name
            may also be substituted for ``ANUM``.

        noeflip : int or str
            Indicates whether you want to change the normal direction of the existing elements on the reversed
            area(s) so that they are consistent with each area's new normal direction.

            * ``0`` - Make the normal direction of existing elements on the reversed area(s) consistent with
              each area's new normal direction (default).

            * ``1`` - Do not change the normal direction of existing elements on the reversed area(s).

        Notes
        -----

        .. _AREVERSE_notes:

        You cannot use the :ref:`areverse` command to change the normal direction of any element that has a
        body or surface load. We recommend that you apply all of your loads only after ensuring that the
        element normal directions are acceptable. Also, you cannot use this command to change the normal
        direction for areas attached to volumes because IGES and ANF data is unchanged by reversal. Reversed
        areas that are attached to volumes need to be reversed again when imported.

        Real constants (such as nonuniform shell thickness and tapered beam constants) may be invalidated by
        an element reversal.

        See `Revising Your Model
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD8_6.html>`_ in the
        `Modeling and Meshing Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD14.html>`_
        for more information.
        """
        command = f"AREVERSE,{anum},{noeflip}"
        return self.run(command, **kwargs)

    def arotat(
        self,
        nl1: str = "",
        nl2: str = "",
        nl3: str = "",
        nl4: str = "",
        nl5: str = "",
        nl6: str = "",
        pax1: str = "",
        pax2: str = "",
        arc: str = "",
        nseg: str = "",
        **kwargs,
    ):
        r"""Generates cylindrical areas by rotating a line pattern about an axis.

        Mechanical APDL Command: `AROTAT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_AROTAT.html>`_

        Parameters
        ----------
        nl1 : str
            List of lines in the pattern to be rotated (6 maximum if using keyboard entry of ``NL1`` to
            ``NL6`` ). The lines must lie in the plane of the axis of rotation. If ``NL1`` = P, graphical
            picking is enabled and all remaining arguments are ignored (valid only in the GUI). If ``NL1`` =
            ALL, all selected lines will define the pattern to be rotated. A component name may also be
            substituted for ``NL1``.

        nl2 : str
            List of lines in the pattern to be rotated (6 maximum if using keyboard entry of ``NL1`` to
            ``NL6`` ). The lines must lie in the plane of the axis of rotation. If ``NL1`` = P, graphical
            picking is enabled and all remaining arguments are ignored (valid only in the GUI). If ``NL1`` =
            ALL, all selected lines will define the pattern to be rotated. A component name may also be
            substituted for ``NL1``.

        nl3 : str
            List of lines in the pattern to be rotated (6 maximum if using keyboard entry of ``NL1`` to
            ``NL6`` ). The lines must lie in the plane of the axis of rotation. If ``NL1`` = P, graphical
            picking is enabled and all remaining arguments are ignored (valid only in the GUI). If ``NL1`` =
            ALL, all selected lines will define the pattern to be rotated. A component name may also be
            substituted for ``NL1``.

        nl4 : str
            List of lines in the pattern to be rotated (6 maximum if using keyboard entry of ``NL1`` to
            ``NL6`` ). The lines must lie in the plane of the axis of rotation. If ``NL1`` = P, graphical
            picking is enabled and all remaining arguments are ignored (valid only in the GUI). If ``NL1`` =
            ALL, all selected lines will define the pattern to be rotated. A component name may also be
            substituted for ``NL1``.

        nl5 : str
            List of lines in the pattern to be rotated (6 maximum if using keyboard entry of ``NL1`` to
            ``NL6`` ). The lines must lie in the plane of the axis of rotation. If ``NL1`` = P, graphical
            picking is enabled and all remaining arguments are ignored (valid only in the GUI). If ``NL1`` =
            ALL, all selected lines will define the pattern to be rotated. A component name may also be
            substituted for ``NL1``.

        nl6 : str
            List of lines in the pattern to be rotated (6 maximum if using keyboard entry of ``NL1`` to
            ``NL6`` ). The lines must lie in the plane of the axis of rotation. If ``NL1`` = P, graphical
            picking is enabled and all remaining arguments are ignored (valid only in the GUI). If ``NL1`` =
            ALL, all selected lines will define the pattern to be rotated. A component name may also be
            substituted for ``NL1``.

        pax1 : str
            Keypoints defining the axis about which the line pattern is to be rotated.

        pax2 : str
            Keypoints defining the axis about which the line pattern is to be rotated.

        arc : str
            Arc length (in degrees). Positive follows right-hand rule about ``PAX1`` - ``PAX2`` vector.
            Defaults to 360°.

        nseg : str
            Number of areas (8 maximum) around circumference. Defaults to minimum number required for 90°
            -maximum arcs, that is, 4 for 360°, 3 for 270°, etc.

        Notes
        -----

        .. _AROTAT_notes:

        Generates cylindrical areas (and their corresponding keypoints and lines) by rotating a line pattern
        (and its associated keypoint pattern) about an axis. Keypoint patterns are generated at regular
        angular locations, based on a maximum spacing of 90°. Line patterns are generated at the keypoint
        patterns. Arc lines are also generated to connect the keypoints circumferentially. Keypoint, line,
        and area numbers are automatically assigned, beginning with the lowest available values (
        :ref:`numstr` ). Adjacent lines use a common keypoint. Adjacent areas use a common line.
        """
        command = (
            f"AROTAT,{nl1},{nl2},{nl3},{nl4},{nl5},{nl6},{pax1},{pax2},{arc},{nseg}"
        )
        return self.run(command, **kwargs)

    def arscale(
        self,
        na1: str = "",
        na2: str = "",
        ninc: str = "",
        rx: str = "",
        ry: str = "",
        rz: str = "",
        kinc: str = "",
        noelem: int | str = "",
        imove: int | str = "",
        **kwargs,
    ):
        r"""Generates a scaled set of areas from a pattern of areas.

        Mechanical APDL Command: `ARSCALE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ARSCALE.html>`_

        Parameters
        ----------
        na1 : str
            Set of areas, ``NA1`` to ``NA2`` in steps of ``NINC``, that defines the pattern to be scaled.
            ``NA2`` defaults to ``NA1``, ``NINC`` defaults to 1. If ``NA1`` = ALL, ``NA2`` and ``NINC`` are
            ignored and the pattern is defined by all selected areas. If ``NA1`` = P, graphical picking is
            enabled and all remaining arguments are ignored (valid only in the GUI). A component name may
            also be substituted for ``NA1`` ( ``NA2`` and ``NINC`` are ignored).

        na2 : str
            Set of areas, ``NA1`` to ``NA2`` in steps of ``NINC``, that defines the pattern to be scaled.
            ``NA2`` defaults to ``NA1``, ``NINC`` defaults to 1. If ``NA1`` = ALL, ``NA2`` and ``NINC`` are
            ignored and the pattern is defined by all selected areas. If ``NA1`` = P, graphical picking is
            enabled and all remaining arguments are ignored (valid only in the GUI). A component name may
            also be substituted for ``NA1`` ( ``NA2`` and ``NINC`` are ignored).

        ninc : str
            Set of areas, ``NA1`` to ``NA2`` in steps of ``NINC``, that defines the pattern to be scaled.
            ``NA2`` defaults to ``NA1``, ``NINC`` defaults to 1. If ``NA1`` = ALL, ``NA2`` and ``NINC`` are
            ignored and the pattern is defined by all selected areas. If ``NA1`` = P, graphical picking is
            enabled and all remaining arguments are ignored (valid only in the GUI). A component name may
            also be substituted for ``NA1`` ( ``NA2`` and ``NINC`` are ignored).

        rx : str
            Scale factors to be applied to the X, Y, and Z keypoint coordinates in the active coordinate
            system. ( RR, R θ, RZ for cylindrical; RR, R θ, R Φ for spherical). Note that the R θ and R Φ
            scale factors are interpreted as angular offsets. For example, if CSYS = 1, ``RX, RY, RZ`` input
            of (1.5,10,3) would scale the specified keypoints 1.5 times in the radial and 3 times in the Z
            direction, while adding an offset of 10 degrees to the keypoints. Zero, blank, or negative scale
            factor values are assumed to be 1.0. Zero or blank angular offsets have no effect.

        ry : str
            Scale factors to be applied to the X, Y, and Z keypoint coordinates in the active coordinate
            system. ( RR, R θ, RZ for cylindrical; RR, R θ, R Φ for spherical). Note that the R θ and R Φ
            scale factors are interpreted as angular offsets. For example, if CSYS = 1, ``RX, RY, RZ`` input
            of (1.5,10,3) would scale the specified keypoints 1.5 times in the radial and 3 times in the Z
            direction, while adding an offset of 10 degrees to the keypoints. Zero, blank, or negative scale
            factor values are assumed to be 1.0. Zero or blank angular offsets have no effect.

        rz : str
            Scale factors to be applied to the X, Y, and Z keypoint coordinates in the active coordinate
            system. ( RR, R θ, RZ for cylindrical; RR, R θ, R Φ for spherical). Note that the R θ and R Φ
            scale factors are interpreted as angular offsets. For example, if CSYS = 1, ``RX, RY, RZ`` input
            of (1.5,10,3) would scale the specified keypoints 1.5 times in the radial and 3 times in the Z
            direction, while adding an offset of 10 degrees to the keypoints. Zero, blank, or negative scale
            factor values are assumed to be 1.0. Zero or blank angular offsets have no effect.

        kinc : str
            Increment to be applied to keypoint numbers for generated set. If zero, the lowest available
            keypoint numbers will be assigned ( :ref:`numstr` ).

        noelem : int or str
            Specifies whether nodes and elements are also to be generated:

            * ``0`` - Nodes and elements associated with the original areas will be generated (scaled) if they
              exist.

            * ``1`` - Nodes and elements will not be generated.

        imove : int or str
            Specifies whether areas will be moved or newly defined:

            * ``0`` - Additional areas will be generated.

            * ``1`` - Original areas will be moved to new position ( ``KINC`` and ``NOELEM`` are ignored). Use
              only if the old areas are no longer needed at their original positions. Corresponding meshed items
              are also moved if not needed at their original position.

        Notes
        -----

        .. _ARSCALE_notes:

        Generates a scaled set of areas (and their corresponding keypoints, lines, and mesh) from a pattern
        of areas. The MAT, TYPE, REAL, and ESYS attributes are based on the areas in the pattern and not the
        current settings. Scaling is done in the active coordinate system. Areas in the pattern could have
        been generated in any coordinate system. However, solid modeling in a toroidal coordinate system is
        not recommended.
        """
        command = f"ARSCALE,{na1},{na2},{ninc},{rx},{ry},{rz},{kinc},{noelem},{imove}"
        return self.run(command, **kwargs)

    def arsym(
        self,
        ncomp: str = "",
        na1: str = "",
        na2: str = "",
        ninc: str = "",
        kinc: str = "",
        noelem: int | str = "",
        imove: int | str = "",
        **kwargs,
    ):
        r"""Generates areas from an area pattern by symmetry reflection.

        Mechanical APDL Command: `ARSYM <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ARSYM.html>`_

        Parameters
        ----------
        ncomp : str
            Symmetry key:

            * ``X`` - X symmetry (default).

            * ``Y`` - Y symmetry.

            * ``Z`` - Z symmetry.

        na1 : str
            Reflect areas from pattern beginning with ``NA1`` to ``NA2`` (defaults to ``NA1`` ) in steps of
            ``NINC`` (defaults to 1). If ``NA1`` = ALL, ``NA2`` and ``NINC`` are ignored and the pattern is
            all selected areas ( :ref:`asel` ). If ``Ncomp`` = P, use graphical picking to specify areas and
            ignore ``NL2`` and ``NINC``. A component name may also be substituted for ``NA1`` ( ``NA2`` and
            ``NINC`` are ignored).

        na2 : str
            Reflect areas from pattern beginning with ``NA1`` to ``NA2`` (defaults to ``NA1`` ) in steps of
            ``NINC`` (defaults to 1). If ``NA1`` = ALL, ``NA2`` and ``NINC`` are ignored and the pattern is
            all selected areas ( :ref:`asel` ). If ``Ncomp`` = P, use graphical picking to specify areas and
            ignore ``NL2`` and ``NINC``. A component name may also be substituted for ``NA1`` ( ``NA2`` and
            ``NINC`` are ignored).

        ninc : str
            Reflect areas from pattern beginning with ``NA1`` to ``NA2`` (defaults to ``NA1`` ) in steps of
            ``NINC`` (defaults to 1). If ``NA1`` = ALL, ``NA2`` and ``NINC`` are ignored and the pattern is
            all selected areas ( :ref:`asel` ). If ``Ncomp`` = P, use graphical picking to specify areas and
            ignore ``NL2`` and ``NINC``. A component name may also be substituted for ``NA1`` ( ``NA2`` and
            ``NINC`` are ignored).

        kinc : str
            Keypoint increment between sets. If zero, the lowest available keypoint numbers are assigned (
            :ref:`numstr` ).

        noelem : int or str
            Specifies whether nodes and elements are also to be generated:

            * ``0`` - Generate nodes and elements associated with the original areas, if they exist.

            * ``1`` - Do not generate nodes and elements.

        imove : int or str
            Specifies whether areas will be moved or newly defined:

            * ``0`` - Generate additional areas.

            * ``1`` - Move original areas to new position retaining the same keypoint numbers ( ``KINC`` and
              ``NOELEM`` are ignored). Valid only if the old areas are no longer needed at their original
              positions. Corresponding meshed items are also moved if not needed at their original position.

        Notes
        -----

        .. _ARSYM_notes:

        Generates a reflected set of areas (and their corresponding keypoints, lines and mesh) from a given
        area pattern by a symmetry reflection (see analogous node symmetry command, :ref:`nsym` ). The MAT,
        TYPE, REAL, ESYS, and SECNUM attributes are based upon the areas in the pattern and not upon the
        current settings. Reflection is done in the active coordinate system by changing a particular
        coordinate sign. The active coordinate system must be a Cartesian system. Areas in the pattern may
        have been generated in any coordinate system. However, solid modeling in a toroidal coordinate
        system is not recommended. Areas are generated as described in the :ref:`agen` command.

        See the :ref:`esym` command for additional information about symmetry elements.
        """
        command = f"ARSYM,{ncomp},{na1},{na2},{ninc},{kinc},{noelem},{imove}"
        return self.run(command, **kwargs)

    def askin(
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
        r"""Generates an area by "skinning" a surface through guiding lines.

        Mechanical APDL Command: `ASKIN <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ASKIN.html>`_

        Parameters
        ----------
        nl1 : str
            The additional guiding lines for the skinned area (up to 9 total lines, including ``NL1``, if
            using keyboard entry). If negative (and ``NL1`` is negative), the line beginning and end will be
            temporarily interchanged for the skinning operation (see :ref:`ASKIN_extranote1` below).

        nl2 : str
            The additional guiding lines for the skinned area (up to 9 total lines, including ``NL1``, if
            using keyboard entry). If negative (and ``NL1`` is negative), the line beginning and end will be
            temporarily interchanged for the skinning operation (see :ref:`ASKIN_extranote1` below).

        nl3 : str
            The additional guiding lines for the skinned area (up to 9 total lines, including ``NL1``, if
            using keyboard entry). If negative (and ``NL1`` is negative), the line beginning and end will be
            temporarily interchanged for the skinning operation (see :ref:`ASKIN_extranote1` below).

        nl4 : str
            The additional guiding lines for the skinned area (up to 9 total lines, including ``NL1``, if
            using keyboard entry). If negative (and ``NL1`` is negative), the line beginning and end will be
            temporarily interchanged for the skinning operation (see :ref:`ASKIN_extranote1` below).

        nl5 : str
            The additional guiding lines for the skinned area (up to 9 total lines, including ``NL1``, if
            using keyboard entry). If negative (and ``NL1`` is negative), the line beginning and end will be
            temporarily interchanged for the skinning operation (see :ref:`ASKIN_extranote1` below).

        nl6 : str
            The additional guiding lines for the skinned area (up to 9 total lines, including ``NL1``, if
            using keyboard entry). If negative (and ``NL1`` is negative), the line beginning and end will be
            temporarily interchanged for the skinning operation (see :ref:`ASKIN_extranote1` below).

        nl7 : str
            The additional guiding lines for the skinned area (up to 9 total lines, including ``NL1``, if
            using keyboard entry). If negative (and ``NL1`` is negative), the line beginning and end will be
            temporarily interchanged for the skinning operation (see :ref:`ASKIN_extranote1` below).

        nl8 : str
            The additional guiding lines for the skinned area (up to 9 total lines, including ``NL1``, if
            using keyboard entry). If negative (and ``NL1`` is negative), the line beginning and end will be
            temporarily interchanged for the skinning operation (see :ref:`ASKIN_extranote1` below).

        nl9 : str
            The additional guiding lines for the skinned area (up to 9 total lines, including ``NL1``, if
            using keyboard entry). If negative (and ``NL1`` is negative), the line beginning and end will be
            temporarily interchanged for the skinning operation (see :ref:`ASKIN_extranote1` below).

        Notes
        -----

        .. _ASKIN_notes:

        Generates an area by "skinning" a surface through specified guiding lines. The lines act as a set of
        "ribs" over which a surface is "stretched." Two opposite edges of the area are framed by the first (
        ``NL1`` ) and last ( NLn ) guiding lines specified. The other two edges of the area are framed by
        splines-fit lines which the program automatically generates through the ends of all guiding lines.
        The interior of the area is shaped by the interior guiding lines. Once the area has been created,
        only the four edge lines will be attached to it. In rare cases, it may be necessary to change the
        default algorithm used by the :ref:`askin` command (see :ref:`ASKIN_extranote1` below).

        .. _ASKIN_extranote1:

        When skinning from one guiding line to the next, the program can create the transition area in one
        of two ways: one more spiraled and one less spiraled ("flatter"). By default, the program attempts
        to produce the flatter transition, instead of the more spiraled transition. This algorithm can be
        changed by inputting ``NL1`` as a negative number, in which case the program connects all the
        keypoints at the line "beginnings" ( :ref:`psymb`,LDIR command) as one edge of the area, and all the
        line "ends" as the opposite edge, irrespective of the amount of spiraling produced in each
        transition area.

        To further control the geometry of the area (if ``NL1`` is negative), the beginning and end of any
        specified line (other than ``NL1`` ) can be temporarily interchanged (for the skinning operation
        only) by inputting that line number as negative. See `Solid Modeling
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD5_10.html>`_  in the
        `Modeling and Meshing Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD14.html>`_ for an
        illustration.
        """
        command = f"ASKIN,{nl1},{nl2},{nl3},{nl4},{nl5},{nl6},{nl7},{nl8},{nl9}"
        return self.run(command, **kwargs)

    def asub(
        self,
        na1: str = "",
        p1: str = "",
        p2: str = "",
        p3: str = "",
        p4: str = "",
        **kwargs,
    ):
        r"""Generates an area using the shape of an existing area.

        Mechanical APDL Command: `ASUB <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ASUB.html>`_

        Parameters
        ----------
        na1 : str
            Existing area number whose shape is to be used. If ``P1`` = P, graphical picking is enabled and
            all remaining arguments are ignored (valid only in the GUI).

        p1 : str
            Keypoint defining starting corner of area.

        p2 : str
            Keypoint defining second corner of area.

        p3 : str
            Keypoint defining third corner of area.

        p4 : str
            Keypoint defining fourth corner of area (defaults to ``P3`` ).

        Notes
        -----

        .. _ASUB_notes:

        The new area will overlay the old area. Often used when the area to be subdivided consists of a
        complex shape that was not generated in a single coordinate system. Keypoints and any corresponding
        lines must lie on the existing area. Missing lines are generated to lie on the given area. The
        active coordinate system is ignored.
        """
        command = f"ASUB,{na1},{p1},{p2},{p3},{p4}"
        return self.run(command, **kwargs)

    def asum(self, lab: str = "", **kwargs):
        r"""Calculates and prints geometry statistics of the selected areas.

        Mechanical APDL Command: `ASUM <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ASUM.html>`_

        Parameters
        ----------
        lab : str
            Controls the degree of tessellation used in the calculation of area properties. If ``LAB`` =
            DEFAULT, area calculations will use the degree of tessellation set through the :ref:`facet`
            command. If ``LAB`` = FINE, area calculations are based on a finer tessellation.

        Notes
        -----

        .. _ASUM_notes:

        Calculates and prints geometry statistics (area, centroid location, moments of inertia, volume,
        etc.) associated with the selected areas. :ref:`asum` should only be used on perfectly flat areas.

        Geometry items are reported in the global Cartesian coordinate system. A unit thickness is assumed
        unless the areas have a non-zero total thickness defined by real constant or section data.

        For layered areas, a unit density is always assumed. For single-layer areas, a unit density is
        assumed unless the areas have a valid material (density).

        The thickness and density are associated to the areas via the :ref:`aatt` command.

        Items calculated via :ref:`asum` and later retrieved via a :ref:`get` or :ref:`starvget` command are
        valid only if the model is not modified after issuing the :ref:`asum` command.

        Setting a finer degree of tessellation will provide area calculations with greater accuracy,
        especially for thin, hollow models. However, using a finer degree of tessellation requires longer
        processing.

        For very narrow (sliver) areas, such that the ratio of the minimum to the maximum dimension is less
        than 0.01, the :ref:`asum` command can provide erroneous area information. To ensure that the
        calculations are accurate, subdivide such areas so that the ratio of the minimum to the maximum is
        at least 0.05.
        """
        command = f"ASUM,{lab}"
        return self.run(command, **kwargs)

    def atran(
        self,
        kcnto: str = "",
        na1: str = "",
        na2: str = "",
        ninc: str = "",
        kinc: str = "",
        noelem: int | str = "",
        imove: int | str = "",
        **kwargs,
    ):
        r"""Transfers a pattern of areas to another coordinate system.

        Mechanical APDL Command: `ATRAN <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ATRAN.html>`_

        Parameters
        ----------
        kcnto : str
            Reference number of coordinate system where the pattern is to be transferred. Transfer occurs
            from the active coordinate system. The coordinate system type and parameters of ``KCNTO`` must
            be the same as the active system.

        na1 : str
            Transfer area pattern beginning with ``NA1`` to ``NA2`` (defaults to ``NA1`` ) in steps of
            ``NINC`` (defaults to 1). If ``NA1`` = ALL, ``NA2`` and ``NINC`` are ignored and the pattern is
            all selected areas ( :ref:`asel` ). If ``NA1`` = P, graphical picking is enabled and all
            remaining arguments are ignored (valid only in the GUI). A component name may also be
            substituted for ``NA1`` ( ``NA2`` and ``NINC`` are ignored).

        na2 : str
            Transfer area pattern beginning with ``NA1`` to ``NA2`` (defaults to ``NA1`` ) in steps of
            ``NINC`` (defaults to 1). If ``NA1`` = ALL, ``NA2`` and ``NINC`` are ignored and the pattern is
            all selected areas ( :ref:`asel` ). If ``NA1`` = P, graphical picking is enabled and all
            remaining arguments are ignored (valid only in the GUI). A component name may also be
            substituted for ``NA1`` ( ``NA2`` and ``NINC`` are ignored).

        ninc : str
            Transfer area pattern beginning with ``NA1`` to ``NA2`` (defaults to ``NA1`` ) in steps of
            ``NINC`` (defaults to 1). If ``NA1`` = ALL, ``NA2`` and ``NINC`` are ignored and the pattern is
            all selected areas ( :ref:`asel` ). If ``NA1`` = P, graphical picking is enabled and all
            remaining arguments are ignored (valid only in the GUI). A component name may also be
            substituted for ``NA1`` ( ``NA2`` and ``NINC`` are ignored).

        kinc : str
            Keypoint increment between sets. If zero, the lowest available keypoint numbers are assigned (
            :ref:`numstr` ).

        noelem : int or str
            Specifies whether elements and nodes are also to be generated:

            * ``0`` - Generate nodes and elements associated with the original areas, if they exist.

            * ``1`` - Do not generate nodes and elements.

        imove : int or str
            Specifies whether to redefine the existing areas:

            * ``0`` - Generate additional areas.

            * ``1`` - Move original areas to new position retaining the same keypoint numbers ( ``KINC`` and
              ``NOELEM`` are ignored). Valid only if the old areas are no longer needed at their original
              positions. Corresponding meshed items are also moved if not needed at their original position.

        Notes
        -----

        .. _ATRAN_notes:

        Transfers a pattern of areas (and their corresponding lines, keypoints and mesh) from one coordinate
        system to another (see analogous node :ref:`transfer` command). The MAT, TYPE, REAL, and ESYS
        attributes are based upon the areas in the pattern and not upon the current settings. Coordinate
        systems may be translated and rotated relative to each other. Initial pattern may be generated in
        any coordinate system. However, solid modeling in a toroidal coordinate system is not recommended.
        Coordinate and slope values are interpreted in the active coordinate system and are transferred
        directly. Areas are generated as described in the :ref:`agen` command.
        """
        command = f"ATRAN,{kcnto},{na1},{na2},{ninc},{kinc},{noelem},{imove}"
        return self.run(command, **kwargs)

    def splot(
        self, na1: str = "", na2: str = "", ninc: str = "", mesh: str = "", **kwargs
    ):
        r"""Displays the selected areas and a faceted view of their underlying surfaces

        Mechanical APDL Command: `SPLOT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SPLOT.html>`_

        Parameters
        ----------
        na1 : str
            Starting area for display of areas and underlying surfaces. If ``NA1`` = ALL (default), ``NA2``
            and ``NINC`` are ignored and all selected areas are displayed ( :ref:`asel` command).

        na2 : str
            Last area to be displayed.

        ninc : str
            Numeric value setting steps between NA1 and NA2 for display. Default value is (1).

        mesh : str
            Specifies a rectangular mesh density used to display the underlying surface (default 4, i.e. 4 x
            4).

        Notes
        -----

        .. _SPLOT_notes:

        This command is valid in any processor. The plot output displays the external and internal trim
        curves and underlying surface. You cannot obtain a faceted view of your surface areas when you are
        using the :ref:`slashexpand` command to create larger graphics displays.

        Use :ref:`aplot` for trimmed surface display.
        """
        command = f"SPLOT,{na1},{na2},{ninc},{mesh}"
        return self.run(command, **kwargs)
