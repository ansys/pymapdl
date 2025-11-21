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


class Keypoints:

    def gsum(self, **kwargs):
        r"""Calculates and prints geometry items.

        Mechanical APDL Command: `GSUM <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_GSUM.html>`_

        Notes
        -----

        .. _GSUM_notes:

        Calculates and prints geometry items (centroid location, moments of inertia, length, area, volume
        etc.) associated with the selected keypoints, lines, areas, and volumes. Geometry items are reported
        in the global Cartesian coordinate system. For volumes, a unit density is assumed unless the volumes
        have a material association via the :ref:`vatt` command. For areas, a unit density (and thickness)
        is assumed unless the areas have a material (and real constant) association via the :ref:`aatt`
        command. For lines and keypoints, a unit density is assumed, irrespective of any material
        associations ( :ref:`latt`, :ref:`katt`, :ref:`mat` ). Items calculated by :ref:`gsum` and later
        retrieved by a :ref:`get` or :ref:`starvget` commands are valid only if the model is not
        modified after the :ref:`gsum` command is issued. This command combines the functions of the
        :ref:`ksum`, :ref:`lsum`, :ref:`asum`, and :ref:`vsum` commands.
        """
        command = "GSUM"
        return self.run(command, **kwargs)

    def k(self, npt: str = "", x: str = "", y: str = "", z: str = "", **kwargs):
        r"""Defines a keypoint.

        Mechanical APDL Command: `K <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_K.html>`_

        Parameters
        ----------
        npt : str
            Reference number for keypoint. If zero, the lowest available number is assigned ( :ref:`numstr`
            ).

        x : str
            Keypoint location in the active coordinate system (may be R, θ, Z or R, θ, Φ). If ``X`` = P,
            graphical picking is enabled and all other fields (including ``NPT`` ) are ignored (valid only
            in the GUI).

        y : str
            Keypoint location in the active coordinate system (may be R, θ, Z or R, θ, Φ). If ``X`` = P,
            graphical picking is enabled and all other fields (including ``NPT`` ) are ignored (valid only
            in the GUI).

        z : str
            Keypoint location in the active coordinate system (may be R, θ, Z or R, θ, Φ). If ``X`` = P,
            graphical picking is enabled and all other fields (including ``NPT`` ) are ignored (valid only
            in the GUI).

        Returns
        -------
        int
            The keypoint number of the generated keypoint.

        Notes
        -----

        .. _K_notes:

        Defines a keypoint in the active coordinate system ( :ref:`csys` ) for line, area, and volume
        descriptions. A previously defined keypoint of the same number will be redefined. Keypoints may be
        redefined only if it is not yet attached to a line or is not yet meshed. Solid modeling in a
        toroidal system is not recommended.

        Examples
        --------
        Create keypoint at ``(0, 1, 2)``

        >>> knum = mapdl.k('', 0, 1, 2)
        >>> knum
        1

        Create keypoint at ``(10, 11, 12)`` while specifying the
        keypoint number.

        >>> knum = mapdl.k(5, 10, 11, 12)
        >>> knum
        5
        """
        command = f"K,{npt},{x},{y},{z}"
        return parse.parse_k(self.run(command, **kwargs))

    def kbetw(
        self,
        kp1: str = "",
        kp2: str = "",
        kpnew: str = "",
        type_: str = "",
        value: str = "",
        **kwargs,
    ):
        r"""Creates a keypoint between two existing keypoints.

        Mechanical APDL Command: `KBETW <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_KBETW.html>`_

        Parameters
        ----------
        kp1 : str
            First keypoint. If ``KP1`` = P, graphical picking is enabled and all remaining command fields
            are ignored (valid only in the GUI).

        kp2 : str
            Second keypoint.

        kpnew : str
            Number assigned to the new keypoint. Defaults to the lowest available keypoint number.

        type_ : str
            Type of input for ``VALUE``.

            * ``RATIO`` - Value is the ratio of the distances between keypoints as follows: ( ``KP1`` -
              ``KPNEW`` )/( ``KP1`` - ``KP2`` ).

            * ``DIST`` - Value is the absolute distance between ``KP1`` and ``KPNEW`` (valid only if current
              coordinate system is Cartesian).

        value : str
            Location of new keypoint, as defined by ``Type`` (defaults to 0.5). If ``VALUE`` is a ratio (
            ``Type`` = RATIO) and is less than 0 or greater than 1, the keypoint is created on the extended
            line. Similarly, if ``VALUE`` is a distance ( ``Type`` = DIST) and is less than 0 or greater
            than the distance between ``KP1`` and ``KP2``, the keypoint is created on the extended line.

        Returns
        -------
        int
            Keypoint number of the generated keypoint.

        Notes
        -----

        .. _KBETW_notes:

        Placement of the new keypoint depends on the currently active coordinate system ( :ref:`csys` ). If
        the coordinate system is Cartesian, the keypoint will lie on a straight line between ``KP1`` and
        ``KP2``. If the system is not Cartesian (for example, cylindrical, spherical, etc.), the keypoint
        will be located as if on a line (which may not be straight) created in the current coordinate system
        between ``KP1`` and ``KP2``. Note that solid modeling in a toroidal coordinate system is not
        recommended.

        Examples
        --------
        Create a keypoint exactly centered between two keypoints.

        >>> k0 = mapdl.k("", 0, 0, 0)
        >>> k1 = mapdl.k("", 1, 0, 0)
        >>> k2 = mapdl.kbetw(k0, k1)
        >>> k2
        3
        """
        command = f"KBETW,{kp1},{kp2},{kpnew},{type_},{value}"
        return parse.parse_kpoint(self.run(command, **kwargs))

    def kcenter(
        self,
        type_: str = "",
        val1: str = "",
        val2: str = "",
        val3: str = "",
        val4: str = "",
        kpnew: str = "",
        **kwargs,
    ):
        r"""Creates a keypoint at the center of a circular arc defined by three locations.

        Mechanical APDL Command: `KCENTER <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_KCENTER.html>`_

        Parameters
        ----------
        type_ : str
            Type of entity used to define the circular arc. The meaning of ``VAL1`` through ``VAL4`` will vary depending on ``Type``. If ``Type`` = P, graphical picking is enabled and all remaining command fields are ignored (valid only in the GUI).

            * ``KP`` - Arc is defined by keypoints.

            * ``LINE`` - Arc is defined by locations on a line.

        val1 : str
            Values used to specify three locations on the arc (see table below).

        val2 : str
            Values used to specify three locations on the arc (see table below).

        val3 : str
            Values used to specify three locations on the arc (see table below).

        val4 : str
            Values used to specify three locations on the arc (see table below).

        kpnew : str
            Number assigned to new keypoint. Defaults to the lowest available keypoint number.

        Returns
        -------
        int
            Keypoint number of the generated keypoint.

        Notes
        -----

        .. warning::

           This function contains specificities regarding the argument definitions.
           Please refer to the `command documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_KCENTER.html>`_
           for further explanations.

        .. _KCENTER_notes:

        :ref:`kcenter` should be used in the Cartesian coordinate system ( :ref:`csys`,0) only. This command
        provides three methods to define a keypoint at the center of three locations. As shown below, the
        center point can be calculated based on a) three keypoints, b) three keypoints and a radius, or c)
        three locations on a line. Note that for method c, if a circular line is specified by ``VAL1``,
        ``VAL2`` through ``VAL4`` are not needed.

        .. only:: html

            .. figure:: ../../../images/_commands/gKCEN1.svg


        Examples
        --------
        Create a keypoint at the center of a circle centered at (0, 0, 0)

        >>> k0 = mapdl.k("", 0, 1, 0)
        >>> k1 = mapdl.k("", 1, 0, 0)
        >>> k2 = mapdl.k("", 0, -1, 0)
        >>> k3 = mapdl.kcenter('KP', k0, k1, k2)
        >>> k3
        4
        """
        command = f"KCENTER,{type_},{val1},{val2},{val3},{val4},{kpnew}"
        return parse.parse_kpoint(self.run(command, **kwargs))

    def kdele(self, np1: str = "", np2: str = "", ninc: str = "", **kwargs):
        r"""Deletes unmeshed keypoints.

        Mechanical APDL Command: `KDELE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_KDELE.html>`_

        Parameters
        ----------
        np1 : str
            Delete keypoints from ``NP1`` to ``NP2`` (defaults to ``NP1`` ) in steps of ``NINC`` (defaults
            to 1). If ``NP1`` = ALL, ``NP2`` and ``NINC`` are ignored and all selected keypoints (
            :ref:`ksel` ) are deleted. If ``NP1`` = P, graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI). A component name may also be substituted for
            ``NP1`` ( ``NP2`` and ``NINC`` are ignored).

        np2 : str
            Delete keypoints from ``NP1`` to ``NP2`` (defaults to ``NP1`` ) in steps of ``NINC`` (defaults
            to 1). If ``NP1`` = ALL, ``NP2`` and ``NINC`` are ignored and all selected keypoints (
            :ref:`ksel` ) are deleted. If ``NP1`` = P, graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI). A component name may also be substituted for
            ``NP1`` ( ``NP2`` and ``NINC`` are ignored).

        ninc : str
            Delete keypoints from ``NP1`` to ``NP2`` (defaults to ``NP1`` ) in steps of ``NINC`` (defaults
            to 1). If ``NP1`` = ALL, ``NP2`` and ``NINC`` are ignored and all selected keypoints (
            :ref:`ksel` ) are deleted. If ``NP1`` = P, graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI). A component name may also be substituted for
            ``NP1`` ( ``NP2`` and ``NINC`` are ignored).

        Notes
        -----

        .. _KDELE_notes:

        Deletes selected keypoints. A keypoint attached to a line cannot be deleted unless the line is first
        deleted.
        """
        command = f"KDELE,{np1},{np2},{ninc}"
        return self.run(command, **kwargs)

    def kdist(self, kp1: str = "", kp2: str = "", **kwargs):
        r"""Calculates and lists the distance between two keypoints.

        Mechanical APDL Command: `KDIST <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_KDIST.html>`_

        Parameters
        ----------
        kp1 : str
            First keypoint in distance calculation. If ``KP1`` = P, graphical picking is enabled and all
            remaining command fields are ignored (valid only in the GUI).

        kp2 : str
            Second keypoint in distance calculation.

        Returns
        -------
            list
            ``[DIST, X, Y, Z]`` distance between two keypoints.

        Notes
        -----

        .. _KDIST_notes:

        :ref:`kdist` lists the distance between keypoints ``KP1`` and ``KP2``, as well as the current
        coordinate system offsets from ``KP1`` to ``KP2``, where the X, Y, and Z locations of ``KP1`` are
        subtracted from the X, Y, and Z locations of ``KP2`` (respectively) to determine the offsets.
        :ref:`kdist` is valid in any coordinate system except toroidal ( :ref:`csys`,3).

        :ref:`kdist` returns a variable, called ``_RETURN``, which contains the distance value. You can use
        this value for various purposes; for example, to set the default number of line divisions to be
        generated along region boundary lines ( :ref:`esize`, ``_RETURN`` ). In interactive mode, you can
        access this command by using the Model Query Picker ( Utility Menu> List> Picked Entities ), where
        you can also access automatic annotation functions, and display the value on your model.

        This command is valid in any processor.

        Examples
        --------
        Compute the distance between two keypoints.

        >>> kp0 = (0, 10, -3)
        >>> kp1 = (1, 5, 10)
        >>> knum0 = mapdl.k("", *kp0)
        >>> knum1 = mapdl.k("", *kp1)
        >>> dist = mapdl.kdist(knum0, knum1)
        >>> dist
        [13.96424004376894, 1.0, -5.0, 13.0]
        """
        return parse.parse_kdist(self.run(f"KDIST,{kp1},{kp2}", **kwargs))

    def kfill(
        self,
        np1: str = "",
        np2: str = "",
        nfill: str = "",
        nstrt: str = "",
        ninc: str = "",
        space: str = "",
        **kwargs,
    ):
        r"""Generates keypoints between two keypoints.

        Mechanical APDL Command: `KFILL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_KFILL.html>`_

        Parameters
        ----------
        np1 : str
            Beginning and ending keypoints for fill-in. ``NP1`` defaults to next to last keypoint specified,
            ``NP2`` defaults to last keypoint specified. If ``NP1`` = P, graphical picking is enabled and
            all remaining command fields are ignored (valid only in the GUI).

        np2 : str
            Beginning and ending keypoints for fill-in. ``NP1`` defaults to next to last keypoint specified,
            ``NP2`` defaults to last keypoint specified. If ``NP1`` = P, graphical picking is enabled and
            all remaining command fields are ignored (valid only in the GUI).

        nfill : str
            Fill ``NFILL`` keypoints between ``NP1`` and ``NP2`` (defaults to \| ``NP2`` - ``NP1`` \|-1).
            ``NFILL`` must be positive.

        nstrt : str
            Keypoint number assigned to first filled-in keypoint (defaults to ``NP1`` + ``NINC`` ).

        ninc : str
            Add this increment to each of the remaining filled-in keypoint numbers (may be positive or
            negative). Defaults to ( ``NP2`` - ``NP1`` )/( ``NFILL`` + 1), that is, linear interpolation.

        space : str
            Spacing ratio. Ratio of last division size to first division size. If > 1.0, divisions increase.
            If < 1.0, divisions decrease. Ratio defaults to 1.0 (uniform spacing).

        Notes
        -----

        .. _KFILL_notes:

        Generates keypoints (in the active coordinate system) between two existing keypoints. The two
        keypoints may have been defined in any coordinate system. However, solid modeling in a toroidal
        coordinate system is not recommended. Any number of keypoints may be filled in and any keypoint
        numbering sequence may be assigned.
        """
        command = f"KFILL,{np1},{np2},{nfill},{nstrt},{ninc},{space}"
        return self.run(command, **kwargs)

    def kgen(
        self,
        itime: str = "",
        np1: str = "",
        np2: str = "",
        ninc: str = "",
        dx: str = "",
        dy: str = "",
        dz: str = "",
        kinc: str = "",
        noelem: int | str = "",
        imove: int | str = "",
        **kwargs,
    ):
        r"""Generates additional keypoints from a pattern of keypoints.

        Mechanical APDL Command: `KGEN <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_KGEN.html>`_

        Parameters
        ----------
        itime : str
            Do this generation operation a total of ``ITIME`` times, incrementing all keypoints in the given
            pattern automatically (or by ``KINC`` ) each time after the first. ``ITIME`` must be more than 1
            for generation to occur.

        np1 : str
            Generate keypoints from the pattern of keypoints beginning with ``NP1`` to ``NP2`` (defaults to
            ``NP1`` ) in steps of ``NINC`` (defaults to 1). If ``NP1`` = ALL, ``NP2`` and ``NINC`` are
            ignored and the pattern is all selected keypoints ( :ref:`ksel` ). If ``NP1`` is negative,
            ``NP2`` and ``NINC`` are ignored and the last \| ``NP1`` \| keypoints (in sequence from the
            highest keypoint number) are used as the pattern to be repeated. If ``NP1`` = P, graphical
            picking is enabled and all remaining command fields are ignored (valid only in the GUI). A
            component name may also be substituted for ``NP1`` ( ``NP2`` and ``NINC`` are ignored).

        np2 : str
            Generate keypoints from the pattern of keypoints beginning with ``NP1`` to ``NP2`` (defaults to
            ``NP1`` ) in steps of ``NINC`` (defaults to 1). If ``NP1`` = ALL, ``NP2`` and ``NINC`` are
            ignored and the pattern is all selected keypoints ( :ref:`ksel` ). If ``NP1`` is negative,
            ``NP2`` and ``NINC`` are ignored and the last \| ``NP1`` \| keypoints (in sequence from the
            highest keypoint number) are used as the pattern to be repeated. If ``NP1`` = P, graphical
            picking is enabled and all remaining command fields are ignored (valid only in the GUI). A
            component name may also be substituted for ``NP1`` ( ``NP2`` and ``NINC`` are ignored).

        ninc : str
            Generate keypoints from the pattern of keypoints beginning with ``NP1`` to ``NP2`` (defaults to
            ``NP1`` ) in steps of ``NINC`` (defaults to 1). If ``NP1`` = ALL, ``NP2`` and ``NINC`` are
            ignored and the pattern is all selected keypoints ( :ref:`ksel` ). If ``NP1`` is negative,
            ``NP2`` and ``NINC`` are ignored and the last \| ``NP1`` \| keypoints (in sequence from the
            highest keypoint number) are used as the pattern to be repeated. If ``NP1`` = P, graphical
            picking is enabled and all remaining command fields are ignored (valid only in the GUI). A
            component name may also be substituted for ``NP1`` ( ``NP2`` and ``NINC`` are ignored).

        dx : str
            Keypoint location increments in the active coordinate system (DR, Dθ, DZ for cylindrical, DR,
            Dθ, DΦ for spherical).

        dy : str
            Keypoint location increments in the active coordinate system (DR, Dθ, DZ for cylindrical, DR,
            Dθ, DΦ for spherical).

        dz : str
            Keypoint location increments in the active coordinate system (DR, Dθ, DZ for cylindrical, DR,
            Dθ, DΦ for spherical).

        kinc : str
            Keypoint increment between generated sets. If zero, the lowest available keypoint numbers are
            assigned ( :ref:`numstr` ).

        noelem : int or str
            Specifies if elements and nodes are also to be generated:

            * ``0`` - Generate nodes and point elements associated with the original keypoints, if they exist.

            * ``1`` - Do not generate nodes and elements.

        imove : int or str
            Specifies whether keypoints will be moved or newly defined:

            * ``0`` - Generate additional keypoints as requested with the ``ITIME`` argument.

            * ``1`` - Move original keypoints to new position retaining the same keypoint numbers ( ``ITIME``,
              ``KINC``, and ``NOELEM`` are ignored). Valid only if the old keypoints are no longer needed at their
              original positions. Corresponding meshed items are also moved if not needed at their original
              position.

        Notes
        -----

        .. _KGEN_notes:

        Generates additional keypoints (and corresponding mesh) from a given keypoint pattern. The MAT,
        TYPE, REAL, and ESYS attributes are based upon the keypoints in the pattern and not upon the current
        settings. Generation is done in the active coordinate system. Keypoints in the pattern may have been
        defined in any coordinate system. However, solid modeling in a toroidal coordinate system is not
        recommended.
        """
        command = (
            f"KGEN,{itime},{np1},{np2},{ninc},{dx},{dy},{dz},{kinc},{noelem},{imove}"
        )
        return self.run(command, **kwargs)

    def kl(self, nl1: str = "", ratio: str = "", nk1: str = "", **kwargs):
        r"""Generates a keypoint at a specified location on an existing line.

        Mechanical APDL Command: `KL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_KL.html>`_

        Parameters
        ----------
        nl1 : str
            Number of the line. If negative, the direction of line (as interpreted for ``RATIO`` ) is
            reversed. If ``NL1`` = P, graphical picking is enabled and all remaining command fields are
            ignored (valid only in the GUI).

        ratio : str
            Ratio of line length to locate keypoint. Must be between 0.0 and 1.0. Defaults to 0.5 (divide
            the line in half).

        nk1 : str
            Number to be assigned to keypoint generated at division location (defaults to lowest available
            keypoint number ( :ref:`numstr` )).

        Returns
        -------
        int
            Keypoint number of the generated keypoint.

        Examples
        --------
        Create a keypoint on a line from (0, 0, 0) and (10, 0, 0)

        >>> kp0 = (0, 0, 0)
        >>> kp1 = (10, 0, 0)
        >>> knum0 = mapdl.k("", *kp0)
        >>> knum1 = mapdl.k("", *kp1)
        >>> lnum = mapdl.l(knum0, knum1)
        >>> lnum
        1
        """
        cmd = f"KL,{nl1},{ratio},{nk1}"
        return parse.parse_kl(self.run(cmd, **kwargs))

    def klist(
        self, np1: str = "", np2: str = "", ninc: str = "", lab: str = "", **kwargs
    ):
        r"""Lists the defined keypoints or hard points.

        Mechanical APDL Command: `KLIST <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_KLIST.html>`_

        Parameters
        ----------
        np1 : str
            List keypoints from ``NP1`` to ``NP2`` (defaults to ``NP1`` ) in steps of ``NINC`` (defaults to
            1). If ``NP1`` = ALL (default), ``NP2`` and ``NINC`` are ignored and all selected keypoints (
            :ref:`ksel` ) are listed. If ``NP1`` = P, graphical picking is enabled and all remaining command
            fields are ignored (valid only in the GUI). A component name may also be substituted for ``NP1``
            ( ``NP2`` and ``NINC`` are ignored).

        np2 : str
            List keypoints from ``NP1`` to ``NP2`` (defaults to ``NP1`` ) in steps of ``NINC`` (defaults to
            1). If ``NP1`` = ALL (default), ``NP2`` and ``NINC`` are ignored and all selected keypoints (
            :ref:`ksel` ) are listed. If ``NP1`` = P, graphical picking is enabled and all remaining command
            fields are ignored (valid only in the GUI). A component name may also be substituted for ``NP1``
            ( ``NP2`` and ``NINC`` are ignored).

        ninc : str
            List keypoints from ``NP1`` to ``NP2`` (defaults to ``NP1`` ) in steps of ``NINC`` (defaults to
            1). If ``NP1`` = ALL (default), ``NP2`` and ``NINC`` are ignored and all selected keypoints (
            :ref:`ksel` ) are listed. If ``NP1`` = P, graphical picking is enabled and all remaining command
            fields are ignored (valid only in the GUI). A component name may also be substituted for ``NP1``
            ( ``NP2`` and ``NINC`` are ignored).

        lab : str
            Coordinate listing key:

            * ``(blank)`` - List all keypoint information.

            * ``COORD`` - Suppress all but the keypoint coordinates (shown to a higher degree of accuracy than
              when displayed with all information).

            * ``HPT`` - List only hard point information.

        Notes
        -----

        .. _KLIST_notes:

        Lists keypoints in the active display coordinate system ( :ref:`dsys` ). An attribute (TYPE, MAT,
        REAL, or ESYS) listed as a zero is unassigned; one listed as a positive value indicates that the
        attribute was assigned with the :ref:`katt` command (and will not be reset to zero if the mesh is
        cleared); one listed as a negative value indicates that the attribute was assigned using the
        attribute pointer ( :ref:`type`, :ref:`mat`, :ref:`real`, or :ref:`esys` ) that was active during
        meshing (and will be reset to zero if the mesh is cleared).

        This command is valid in any processor.
        """
        command = f"KLIST,{np1},{np2},{ninc},{lab}"
        return self.run(command, **kwargs)

    def kmodif(self, npt: str = "", x: str = "", y: str = "", z: str = "", **kwargs):
        r"""Modifies an existing keypoint.

        Mechanical APDL Command: `KMODIF <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_KMODIF.html>`_

        Parameters
        ----------
        npt : str
            Modify coordinates of this keypoint. If ``NPT`` = ALL, modify coordinates of all selected
            keypoints ( :ref:`ksel` ). If ``NPT`` = P, graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI). A component name may also be substituted for
            ``NPT``.

        x : str
            Replace the previous coordinate values assigned to this keypoint with these corresponding
            coordinate values. Values are interpreted according to the active coordinate system (R, θ, Z for
            cylindrical, R, θ,Φ for spherical). If ``X`` = P, graphical picking is used to locate keypoint
            and ``Y`` and ``Z`` are ignored. A blank retains the previous value. You cannot specify ``Y`` =
            P.

        y : str
            Replace the previous coordinate values assigned to this keypoint with these corresponding
            coordinate values. Values are interpreted according to the active coordinate system (R, θ, Z for
            cylindrical, R, θ,Φ for spherical). If ``X`` = P, graphical picking is used to locate keypoint
            and ``Y`` and ``Z`` are ignored. A blank retains the previous value. You cannot specify ``Y`` =
            P.

        z : str
            Replace the previous coordinate values assigned to this keypoint with these corresponding
            coordinate values. Values are interpreted according to the active coordinate system (R, θ, Z for
            cylindrical, R, θ,Φ for spherical). If ``X`` = P, graphical picking is used to locate keypoint
            and ``Y`` and ``Z`` are ignored. A blank retains the previous value. You cannot specify ``Y`` =
            P.

        Notes
        -----

        .. _KMODIF_notes:

        Lines, areas, and volumes attached to the modified keypoint (if any) must all be selected and will
        be redefined using the active coordinate system. However, solid modeling in a toroidal coordinate
        system is not recommended.

        .. warning::

            Redefined entities may be removed from any defined components and assemblies. Nodes and elements
            will be automatically cleared from any redefined keypoints, lines, areas, or volumes.

        The :ref:`kmodif` command moves keypoints for geometry modification without validating underlying
        entities. To merge keypoints and update higher order entities, issue the :ref:`nummrg` command
        instead.
        """
        command = f"KMODIF,{npt},{x},{y},{z}"
        return self.run(command, **kwargs)

    def kmove(
        self,
        npt: str = "",
        kc1: str = "",
        x1: str = "",
        y1: str = "",
        z1: str = "",
        kc2: str = "",
        x2: str = "",
        y2: str = "",
        z2: str = "",
        **kwargs,
    ):
        r"""Calculates and moves a keypoint to an intersection.

        Mechanical APDL Command: `KMOVE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_KMOVE.html>`_

        Parameters
        ----------
        npt : str
            Move this keypoint. If ``NPT`` = P, graphical picking is enabled and all remaining command
            fields are ignored (valid only in the GUI). A component name may also be substituted for
            ``NPT``.

        kc1 : str
            First coordinate system number. Defaults to 0 (global Cartesian).

        x1 : str
            Input one or two values defining the location of the keypoint in this coordinate system. Input
            "U" for unknown value(s) to be calculated and input "E" to use an existing coordinate value.
            Fields are R1, θ1, Z1 for cylindrical, or R1, θ1, ϕ1 for spherical.

        y1 : str
            Input one or two values defining the location of the keypoint in this coordinate system. Input
            "U" for unknown value(s) to be calculated and input "E" to use an existing coordinate value.
            Fields are R1, θ1, Z1 for cylindrical, or R1, θ1, ϕ1 for spherical.

        z1 : str
            Input one or two values defining the location of the keypoint in this coordinate system. Input
            "U" for unknown value(s) to be calculated and input "E" to use an existing coordinate value.
            Fields are R1, θ1, Z1 for cylindrical, or R1, θ1, ϕ1 for spherical.

        kc2 : str
            Second coordinate system number.

        x2 : str
            Input two or one value(s) defining the location of the keypoint in this coordinate system. Input
            U for unknown value(s) to be calculated and input E to use an existing coordinate value.
            Arguments are R2, θ2, Z2 for cylindrical, or R2, θ2, ϕ2 for spherical.

        y2 : str
            Input two or one value(s) defining the location of the keypoint in this coordinate system. Input
            U for unknown value(s) to be calculated and input E to use an existing coordinate value.
            Arguments are R2, θ2, Z2 for cylindrical, or R2, θ2, ϕ2 for spherical.

        z2 : str
            Input two or one value(s) defining the location of the keypoint in this coordinate system. Input
            U for unknown value(s) to be calculated and input E to use an existing coordinate value.
            Arguments are R2, θ2, Z2 for cylindrical, or R2, θ2, ϕ2 for spherical.

        Notes
        -----

        .. _KMOVE_notes:

        Calculates and moves a keypoint to an intersection location. The keypoint must have been previously
        defined (at an approximate location) or left undefined (in which case it is internally defined at
        the :ref:`source` location). The actual location is calculated from the intersection of three
        surfaces (implied from three coordinate constants in two different coordinate systems). Note that
        solid modeling in a toroidal coordinate system is not recommended. See the :ref:`move` command for
        surface and intersection details. The three (of six) constants easiest to define should be used. The
        program will calculate the remaining three coordinate constants. All arguments, except ``KC1``, must
        be input. Use the repeat command ( ``*REPEAT`` ) after the :ref:`kmove` command to move a series of
        keypoints, if desired.
        """
        command = f"KMOVE,{npt},{kc1},{x1},{y1},{z1},{kc2},{x2},{y2},{z2}"
        return self.run(command, **kwargs)

    def knode(self, npt: str = "", node: str = "", **kwargs):
        r"""Defines a keypoint at an existing node location.

        Mechanical APDL Command: `KNODE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_KNODE.html>`_

        Parameters
        ----------
        npt : str
            Arbitrary reference number for keypoint. If zero, the lowest available number is assigned (
            :ref:`numstr` ).

        node : str
            Node number defining global X, Y, Z keypoint location. If ``NODE`` = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in the GUI). A component name
            may also be substituted for ``NODE``.

        Returns
        -------
        int
            Keypoint number of the generated keypoint.

        Examples
        --------
        Create a keypoint at a node at (1, 2, 3)

        >>> nnum = mapdl.n('', 1, 2, 3)
        >>> knum1 = mapdl.knode('', nnum)
        >>> knum1
        1
        """
        cmd = f"KNODE,{npt},{node}"
        return parse.parse_knode(self.run(cmd, **kwargs))

    def kplot(
        self, np1: str = "", np2: str = "", ninc: str = "", lab: str = "", **kwargs
    ):
        r"""Displays the selected keypoints.

        Mechanical APDL Command: `KPLOT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_KPLOT.html>`_

        Parameters
        ----------
        np1 : str
            Display keypoints from ``NP1`` to ``NP2`` (defaults to ``NP1`` ) in steps of ``NINC`` (defaults
            to 1). If ``NP1`` = ALL (default), ``NP2`` and ``NINC`` are ignored and all selected keypoints (
            :ref:`ksel` ) are displayed.

        np2 : str
            Display keypoints from ``NP1`` to ``NP2`` (defaults to ``NP1`` ) in steps of ``NINC`` (defaults
            to 1). If ``NP1`` = ALL (default), ``NP2`` and ``NINC`` are ignored and all selected keypoints (
            :ref:`ksel` ) are displayed.

        ninc : str
            Display keypoints from ``NP1`` to ``NP2`` (defaults to ``NP1`` ) in steps of ``NINC`` (defaults
            to 1). If ``NP1`` = ALL (default), ``NP2`` and ``NINC`` are ignored and all selected keypoints (
            :ref:`ksel` ) are displayed.

        lab : str
            Determines what keypoints are plotted (one of the following):

            * ``(blank)`` - Plots all keypoints.

            * ``HPT`` - Plots only those keypoints that are hard points.

        Notes
        -----

        .. _KPLOT_notes:

        This command is valid in any processor.
        """
        command = f"KPLOT,{np1},{np2},{ninc},{lab}"
        return self.run(command, **kwargs)

    def kpscale(
        self,
        np1: str = "",
        np2: str = "",
        ninc: str = "",
        rx: str = "",
        ry: str = "",
        rz: str = "",
        kinc: str = "",
        noelem: int | str = "",
        imove: int | str = "",
        **kwargs,
    ):
        r"""Generates a scaled set of (meshed) keypoints from a pattern of keypoints.

        Mechanical APDL Command: `KPSCALE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_KPSCALE.html>`_

        Parameters
        ----------
        np1 : str
            Set of keypoints ( ``NP1`` to ``NP2`` in steps of ``NINC`` ) that defines the pattern to be
            scaled. ``NP2`` defaults to ``NP1``, ``NINC`` defaults to 1. If ``NP1`` = ALL, ``NP2`` and
            ``NINC`` are ignored and the pattern is defined by all selected keypoints. If ``NP1`` = P,
            graphical picking is enabled and all remaining command fields are ignored (valid only in the
            GUI). A component name may also be substituted for ``NP1`` ( ``NP2`` and ``NINC`` are ignored).

        np2 : str
            Set of keypoints ( ``NP1`` to ``NP2`` in steps of ``NINC`` ) that defines the pattern to be
            scaled. ``NP2`` defaults to ``NP1``, ``NINC`` defaults to 1. If ``NP1`` = ALL, ``NP2`` and
            ``NINC`` are ignored and the pattern is defined by all selected keypoints. If ``NP1`` = P,
            graphical picking is enabled and all remaining command fields are ignored (valid only in the
            GUI). A component name may also be substituted for ``NP1`` ( ``NP2`` and ``NINC`` are ignored).

        ninc : str
            Set of keypoints ( ``NP1`` to ``NP2`` in steps of ``NINC`` ) that defines the pattern to be
            scaled. ``NP2`` defaults to ``NP1``, ``NINC`` defaults to 1. If ``NP1`` = ALL, ``NP2`` and
            ``NINC`` are ignored and the pattern is defined by all selected keypoints. If ``NP1`` = P,
            graphical picking is enabled and all remaining command fields are ignored (valid only in the
            GUI). A component name may also be substituted for ``NP1`` ( ``NP2`` and ``NINC`` are ignored).

        rx : str
            Scale factors to be applied to the X, Y, Z keypoint coordinates in the active coordinate system
            (RR, Rθ, RZ for cylindrical; RR, Rθ, RΦ for spherical). The Rθ and RΦ scale factors are
            interpreted as angular offsets. For example, if CSYS = 1, an ``RX``, ``RY``, ``RZ`` input of
            (1.5,10,3) would scale the specified keypoints 1.5 times in the radial and 3 times in the Z
            direction, while adding an offset of 10 degrees to the keypoints.) Zero, blank, or negative
            scale factor values are assumed to be 1.0. Zero or blank angular offsets have no effect.

        ry : str
            Scale factors to be applied to the X, Y, Z keypoint coordinates in the active coordinate system
            (RR, Rθ, RZ for cylindrical; RR, Rθ, RΦ for spherical). The Rθ and RΦ scale factors are
            interpreted as angular offsets. For example, if CSYS = 1, an ``RX``, ``RY``, ``RZ`` input of
            (1.5,10,3) would scale the specified keypoints 1.5 times in the radial and 3 times in the Z
            direction, while adding an offset of 10 degrees to the keypoints.) Zero, blank, or negative
            scale factor values are assumed to be 1.0. Zero or blank angular offsets have no effect.

        rz : str
            Scale factors to be applied to the X, Y, Z keypoint coordinates in the active coordinate system
            (RR, Rθ, RZ for cylindrical; RR, Rθ, RΦ for spherical). The Rθ and RΦ scale factors are
            interpreted as angular offsets. For example, if CSYS = 1, an ``RX``, ``RY``, ``RZ`` input of
            (1.5,10,3) would scale the specified keypoints 1.5 times in the radial and 3 times in the Z
            direction, while adding an offset of 10 degrees to the keypoints.) Zero, blank, or negative
            scale factor values are assumed to be 1.0. Zero or blank angular offsets have no effect.

        kinc : str
            Increment to be applied to the keypoint numbers for generated set. If zero, the lowest available
            keypoint numbers will be assigned ( :ref:`numstr` ).

        noelem : int or str
            Specifies whether nodes and elements are also to be generated:

            * ``0`` - Nodes and point elements associated with the original keypoints will be generated (scaled)
              if they exist.

            * ``1`` - Nodes and point elements will not be generated.

        imove : int or str
            Specifies whether keypoints will be moved or newly defined:

            * ``0`` - Additional keypoints will be generated.

            * ``1`` - Original keypoints will be moved to new position ( ``KINC`` and ``NOELEM`` are ignored).
              Use only if the old keypoints are no longer needed at their original positions. Corresponding meshed
              items are also moved if not needed at their original position.

        Notes
        -----

        .. _KPSCALE_notes:

        Generates a scaled set of keypoints (and corresponding mesh) from a pattern of keypoints. The MAT,
        TYPE, REAL, and ESYS attributes are based on the keypoints in the pattern and not the current
        settings. Scaling is done in the active coordinate system. Keypoints in the pattern could have been
        generated in any coordinate system. However, solid modeling in a toroidal coordinate system is not
        recommended.
        """
        command = f"KPSCALE,{np1},{np2},{ninc},{rx},{ry},{rz},{kinc},{noelem},{imove}"
        return self.run(command, **kwargs)

    def kscale(
        self,
        kinc: str = "",
        np1: str = "",
        np2: str = "",
        ninc: str = "",
        rx: str = "",
        ry: str = "",
        rz: str = "",
        **kwargs,
    ):
        r"""Generates a scaled pattern of keypoints from a given keypoint pattern.

        Mechanical APDL Command: `KSCALE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_KSCALE.html>`_

        Parameters
        ----------
        kinc : str
            Do this scaling operation one time, incrementing all keypoints in the given pattern by ``KINC``.
            If ``KINC`` = 0, keypoints will be redefined at the scaled locations.

        np1 : str
            Scale keypoints from pattern beginning with ``NP1`` to ``NP2`` (defaults to ``NP1`` ) in steps
            of ``NINC`` (defaults to 1). If ``NP1`` = ALL, ``NP2`` and ``NINC`` are ignored and pattern is
            all selected keypoints ( :ref:`ksel` ). If ``NP1`` = P, graphical picking is enabled and all
            remaining command fields are ignored (valid only in the GUI). A component name may also be
            substituted for ``NP1`` ( ``NP2`` and ``NINC`` are ignored).

        np2 : str
            Scale keypoints from pattern beginning with ``NP1`` to ``NP2`` (defaults to ``NP1`` ) in steps
            of ``NINC`` (defaults to 1). If ``NP1`` = ALL, ``NP2`` and ``NINC`` are ignored and pattern is
            all selected keypoints ( :ref:`ksel` ). If ``NP1`` = P, graphical picking is enabled and all
            remaining command fields are ignored (valid only in the GUI). A component name may also be
            substituted for ``NP1`` ( ``NP2`` and ``NINC`` are ignored).

        ninc : str
            Scale keypoints from pattern beginning with ``NP1`` to ``NP2`` (defaults to ``NP1`` ) in steps
            of ``NINC`` (defaults to 1). If ``NP1`` = ALL, ``NP2`` and ``NINC`` are ignored and pattern is
            all selected keypoints ( :ref:`ksel` ). If ``NP1`` = P, graphical picking is enabled and all
            remaining command fields are ignored (valid only in the GUI). A component name may also be
            substituted for ``NP1`` ( ``NP2`` and ``NINC`` are ignored).

        rx : str
            Scale factor ratios. Scaling is relative to the origin of the active coordinate system (RR, Rθ,
            RZ for cylindrical, RR, Rθ, RΦ for spherical). If > 1.0, pattern is enlarged. If < 1.0, pattern
            is reduced. Ratios each default to 1.0.

        ry : str
            Scale factor ratios. Scaling is relative to the origin of the active coordinate system (RR, Rθ,
            RZ for cylindrical, RR, Rθ, RΦ for spherical). If > 1.0, pattern is enlarged. If < 1.0, pattern
            is reduced. Ratios each default to 1.0.

        rz : str
            Scale factor ratios. Scaling is relative to the origin of the active coordinate system (RR, Rθ,
            RZ for cylindrical, RR, Rθ, RΦ for spherical). If > 1.0, pattern is enlarged. If < 1.0, pattern
            is reduced. Ratios each default to 1.0.

        Notes
        -----

        .. _KSCALE_notes:

        Generates a scaled pattern of keypoints from a given keypoint pattern. Scaling is done in the active
        coordinate system (see analogous node scaling ( :ref:`nscale` )). Solid modeling in a toroidal
        coordinate system is not recommended.
        """
        command = f"KSCALE,{kinc},{np1},{np2},{ninc},{rx},{ry},{rz}"
        return self.run(command, **kwargs)

    def ksum(self, **kwargs):
        r"""Calculates and prints geometry statistics of the selected keypoints.

        Mechanical APDL Command: `KSUM <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_KSUM.html>`_

        Notes
        -----

        .. _KSUM_notes:

        Calculates and prints geometry statistics (centroid location, moments of inertia, etc.) associated
        with the selected keypoints. Geometry items are reported in the global Cartesian coordinate system.
        A unit density is assumed, irrespective of any material associations ( :ref:`katt`, :ref:`mat` ).
        Items calculated by :ref:`ksum` and later retrieved by a :ref:`get` or :ref:`starvget` command are
        valid only if the model is not modified after the :ref:`ksum` command is issued.
        """
        command = "KSUM"
        return self.run(command, **kwargs)

    def ksymm(
        self,
        ncomp: str = "",
        np1: str = "",
        np2: str = "",
        ninc: str = "",
        kinc: str = "",
        noelem: int | str = "",
        imove: int | str = "",
        **kwargs,
    ):
        r"""Generates a reflected set of keypoints.

        Mechanical APDL Command: `KSYMM <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_KSYMM.html>`_

        Parameters
        ----------
        ncomp : str
            Symmetry key:

            * ``X`` - X (or R) symmetry (default).

            * ``Y`` - Y (or θ) symmetry.

            * ``Z`` - Z (or Φ) symmetry.

        np1 : str
            Reflect keypoints from pattern beginning with ``NP1`` to ``NP2`` (defaults to ``NP1`` ) in steps
            of ``NINC`` (defaults to 1). If ``NP1`` = ALL, ``NP2`` and ``NINC`` are ignored and pattern is
            all selected keypoints ( :ref:`ksel` ). If ``Ncomp`` = P, graphical picking is enabled and all
            remaining command fields are ignored (valid only in the GUI). A component name may also be
            substituted for ``NP1`` ( ``NP2`` and ``NINC`` are ignored).

        np2 : str
            Reflect keypoints from pattern beginning with ``NP1`` to ``NP2`` (defaults to ``NP1`` ) in steps
            of ``NINC`` (defaults to 1). If ``NP1`` = ALL, ``NP2`` and ``NINC`` are ignored and pattern is
            all selected keypoints ( :ref:`ksel` ). If ``Ncomp`` = P, graphical picking is enabled and all
            remaining command fields are ignored (valid only in the GUI). A component name may also be
            substituted for ``NP1`` ( ``NP2`` and ``NINC`` are ignored).

        ninc : str
            Reflect keypoints from pattern beginning with ``NP1`` to ``NP2`` (defaults to ``NP1`` ) in steps
            of ``NINC`` (defaults to 1). If ``NP1`` = ALL, ``NP2`` and ``NINC`` are ignored and pattern is
            all selected keypoints ( :ref:`ksel` ). If ``Ncomp`` = P, graphical picking is enabled and all
            remaining command fields are ignored (valid only in the GUI). A component name may also be
            substituted for ``NP1`` ( ``NP2`` and ``NINC`` are ignored).

        kinc : str
            Keypoint increment between sets. If zero, the lowest available keypoint numbers are assigned (
            :ref:`numstr` ).

        noelem : int or str
            Specifies whether nodes and elements are also to be generated:

            * ``0`` - Generate nodes and point elements associated with the original keypoints, if they exist.

            * ``1`` - Do not generate nodes and elements.

        imove : int or str
            Specifies whether keypoints will be moved or newly defined:

            * ``0`` - Generate additional keypoints.

            * ``1`` - Move original keypoints to new position retaining the same keypoint numbers ( ``KINC`` and
              ``NOELEM`` are ignored). Valid only if the old keypoints are no longer needed at their original
              positions. Corresponding meshed items are also moved if not needed at their original position.

        Notes
        -----

        .. _KSYMM_notes:

        Generates a reflected set of keypoints (and corresponding mesh) from a given keypoint pattern by a
        symmetry reflection (see analogous node symmetry command, :ref:`nsym` ). The MAT, TYPE, REAL, and
        ESYS attributes are based upon the keypoints in the pattern and not upon the current settings.
        Reflection is done in the active coordinate system by changing a particular coordinate sign.
        Keypoints in the pattern may have been generated in any coordinate system. However, solid modeling
        in a toroidal coordinate system is not recommended.
        """
        command = f"KSYMM,{ncomp},{np1},{np2},{ninc},{kinc},{noelem},{imove}"
        return self.run(command, **kwargs)

    def ktran(
        self,
        kcnto: str = "",
        np1: str = "",
        np2: str = "",
        ninc: str = "",
        kinc: str = "",
        noelem: int | str = "",
        imove: int | str = "",
        **kwargs,
    ):
        r"""Transfers a pattern of keypoints to another coordinate system.

        Mechanical APDL Command: `KTRAN <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_KTRAN.html>`_

        Parameters
        ----------
        kcnto : str
            Reference number of coordinate system where the pattern is to be transferred. Transfer occurs
            from the active coordinate system.

        np1 : str
            Transfer keypoints from pattern beginning with ``NP1`` to ``NP2`` (defaults to ``NP1`` ) in
            steps of ``NINC`` (defaults to 1). If ``NP1`` = ALL, ``NP2`` and ``NINC`` are ignored and
            pattern is all selected keypoints ( :ref:`ksel` ). If ``NP1`` = P, graphical picking is enabled
            and all remaining command fields are ignored (valid only in the GUI). A component name may also
            be substituted for ``NP1`` ( ``NP2`` and ``NINC`` are ignored).

        np2 : str
            Transfer keypoints from pattern beginning with ``NP1`` to ``NP2`` (defaults to ``NP1`` ) in
            steps of ``NINC`` (defaults to 1). If ``NP1`` = ALL, ``NP2`` and ``NINC`` are ignored and
            pattern is all selected keypoints ( :ref:`ksel` ). If ``NP1`` = P, graphical picking is enabled
            and all remaining command fields are ignored (valid only in the GUI). A component name may also
            be substituted for ``NP1`` ( ``NP2`` and ``NINC`` are ignored).

        ninc : str
            Transfer keypoints from pattern beginning with ``NP1`` to ``NP2`` (defaults to ``NP1`` ) in
            steps of ``NINC`` (defaults to 1). If ``NP1`` = ALL, ``NP2`` and ``NINC`` are ignored and
            pattern is all selected keypoints ( :ref:`ksel` ). If ``NP1`` = P, graphical picking is enabled
            and all remaining command fields are ignored (valid only in the GUI). A component name may also
            be substituted for ``NP1`` ( ``NP2`` and ``NINC`` are ignored).

        kinc : str
            Keypoint increment between sets. If zero, the lowest available keypoint numbers are assigned (
            :ref:`numstr` ).

        noelem : int or str
            Specifies whether nodes and elements are also to be generated:

            * ``0`` - Generate nodes and point elements associated with the original keypoints, if they exist.

            * ``1`` - Do not generate nodes and elements.

        imove : int or str
            Specifies whether keypoints will be moved or newly defined:

            * ``0`` - Generate additional keypoints.

            * ``1`` - Move original keypoints to new position retaining the same keypoint numbers ( ``KINC`` and
              ``NOELEM`` are ignored). Valid only if the old keypoints are no longer needed at their original
              positions. Corresponding meshed items are also moved if not needed at their original position.

        Notes
        -----

        .. _KTRAN_notes:

        Transfers a pattern of keypoints (and corresponding mesh) from one coordinate system to another (see
        analogous node transfer command, :ref:`transfer` ). The MAT, TYPE, REAL, and ESYS attributes are
        based upon the keypoints in the pattern and not upon the current settings. Coordinate systems may be
        translated and rotated relative to each other. Initial pattern may be generated in any coordinate
        system. Coordinate values are interpreted in the active coordinate system and are transferred
        directly. Solid modeling in a toroidal coordinate system is not recommended.
        """
        command = f"KTRAN,{kcnto},{np1},{np2},{ninc},{kinc},{noelem},{imove}"
        return self.run(command, **kwargs)

    def source(self, x: str = "", y: str = "", z: str = "", **kwargs):
        r"""Defines a default location for undefined nodes or keypoints.

        Mechanical APDL Command: `SOURCE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SOURCE.html>`_

        Parameters
        ----------
        x : str
            Global Cartesian coordinates for source nodes or keypoints (defaults to the origin).

        y : str
            Global Cartesian coordinates for source nodes or keypoints (defaults to the origin).

        z : str
            Global Cartesian coordinates for source nodes or keypoints (defaults to the origin).

        Notes
        -----

        .. _SOURCE_notes:

        Defines a global Cartesian location for undefined nodes or keypoints moved during intersection
        calculations ( :ref:`move` or :ref:`kmove` ).
        """
        command = f"SOURCE,{x},{y},{z}"
        return self.run(command, **kwargs)
