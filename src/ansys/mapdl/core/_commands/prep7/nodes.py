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


class Nodes:

    def eextrude(
        self,
        action: str = "",
        nelem: str = "",
        space: str = "",
        dist: str = "",
        theta: str = "",
        tfact: str = "",
        bckey: str = "",
        **kwargs,
    ):
        r"""Extrudes 2D plane elements into 3D solids during a 2D to 3D analysis.

        Mechanical APDL Command: `EEXTRUDE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_EEXTRUDE.html>`_

        Parameters
        ----------
        action : str
            Specifies one of the following command behaviors:

            * ``AUTO`` - Extrudes plane elements ( ``PLANE182``and ``PLANE183``) `Notes
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cmd/Hlp_C_EEXTRUDE.html#>`_ based on the
              KEYOPT(3) setting. Complementary elements are also extruded. (See `Notes
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cmd/Hlp_C_EEXTRUDE.html#>`_ Notes for
              more information.) This behavior is the default.

            * ``PLANE`` - Extrudes elements in the global Z direction. KEYOPT(3) of the parent plane elements is
              ignored.

            * ``AXIS`` - Extrudes elements about the global Y axis. KEYOPT(3) of the parent plane elements is
              ignored.

            * ``TANGENT`` - Extrudes plane and contact elements about the global Y axis. Target elements are
              extruded in the global Z direction.

            * ``TIRE`` - Extrudes plane and contact elements about the global Y axis in a 360-degree span.
              Target elements are extruded in the global Z direction if outside the plane elements. Mesh
              refinement is adapted specifically for tire analysis.

            See :ref:`actionbehavior`.

        nelem : str
            Number of elements to generate in the extruded direction. If you do not specify a number, the
            program calculates a number automatically based on the average element size and extrusion
            distance.

        space : str
            Spacing ratio. If positive, this value is the nominal ratio of the last division size to the
            first division size (if > 1.0, sizes increase, if < 1.0, sizes decrease). If negative, \|SPACE\|
            is the nominal ratio of the center division size to the end division size. Default = 1.0
            (uniform spacing).

        dist : str
            Distance to extrude in the global Z direction for the plane strain case ( ``Action`` = PLANE).
            The default is 1.

        theta : str
            Angle (in degrees) depending on ``Action`` :

            * ``Action`` = AXIS - Ending angle to extrude about the global Y axis for the axisymmetric case.
              Default = 360. (The beginning angle is always 0 degrees.)
            * ``Action`` = TIRE - Span of the contact patch for mesh refinement. The program generates an abrupt
              mesh transition from fine to coarse. Default = 0.

        tfact : str
            Factor for increasing the rigid target size. The size of the extruded rigid target elements is
            determined automatically based on the size of the contact elements. Default = 0.2.

        bckey : str
            Controls the nodal orientation in the third direction and boundary-condition mapping ( ``Action`` = AXIS or TIRE only):

            * ``0`` - All nodes are rotated to a local Cartesian coordinate system where X is the radial, Y
              axial and Z circumferential direction. All loads and displacements are mapped from the 2D model to
              the 3D model in the local coordinate system.

              If applying rotation ROTY in axisymmetric cases with torsion on the 2D model, this value sets UZ = 0
              at all corresponding 3D nodes.

              This value is the default.

            * ``1`` - Only nodes with applied loads and/or displacements are rotated to a local Cartesian
              coordinate system where X is the radial, Y axial and Z circumferential direction. All loads are
              mapped to the 3D model and all applied displacements are reset to zero.

            See :ref:`bckeybehavior`.

        Notes
        -----

        .. _EEXTRUDE_notes:

        The :ref:`eextrude` command extrudes elements ``PLANE182``and ``PLANE183``. Complementary elements
        ``TARGE169``, ``CONTA172``, and ``REINF263`` also extrude. Extrusion operates automatically on
        elements in the selected element set.

        ``Action`` = TIRE determines if target elements are in the middle (rim) part of the model or on the
        outside (road) part. The middle elements extrude axisymmetrically about the Y axis, and the outside
        elements extrude in the Z direction.

        Example Command Actions
        If interference exists between road and tire, the command extrudes outside elements within the
        specified tolerance ( :ref:`seltol` ) in the global Z direction. For more information, see `2D to 3D
        analysis
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_adv/Hlp_G_ADV2DTO3DREST.html>`_.

        The ``BCKEY`` value is valid only within the 2D to 3D analysis environment (that is, after issuing
        :ref:`map2dto3d`,START and before issuing :ref:`map2dto3d`,FINISH).

        Use the default ``BCKEY`` = 0 setting if you intend to apply minimal new loads or constraints during
        the 3D analysis phase; otherwise, set ``BCKEY`` = 1.

        For more information, including how boundary conditions and loads are mapped from the 2D model to
        the 3D model, see `2D to 3D Analysis
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_adv/Hlp_G_ADV2DTO3DREST.html>`_

        Boundary Condition Key Behavior
        This command is valid in the PREP7 ( :ref:`prep7` ) and SOLUTION ( :ref:`slashsolu` ) processors.
        Some options are valid within the 2D to 3D analysis environment only (between :ref:`map2dto3d`,START
        and :ref:`map2dto3d`,FINISH).

        For automatic ``PLANE182``and ``PLANE183``extrusion ( ``Action`` = AUTO), based on the element
        behavior of the plane elements, the command performs as follows:

        * ``KEYOPT(3) = 0`` - Plane stress; the element is ignored.

        * ``KEYOPT(3) = 1`` - Axisymmetric; the element is extruded 360 degrees about the Y-axis. ``THETA``
          is ignored.

        * ``KEYOPT(3) = 2`` - Plane strain (Z strain = 0.0); the element is extruded a unit distance in the
          global Z direction.

        * ``KEYOPT(3) = 3`` - Plane stress with thickness input; the element is extruded in the Z-direction
          as specified by the thickness input via a real constant.

        * ``KEYOPT(3) = 5`` - Generalized plane strain; the element is ignored.

        * ``KEYOPT(3) = 6`` - Axisymmetric with torsion; the element is extruded 360 degrees about the
          Y-axis. ``THETA`` is ignored.

        For an axisymmetric extrusion ( ``Action`` = AUTO with KEYOPT(3) = 1, ``Action`` = AXIS, or
        ``Action`` = TANGENT), the command merges any nodes within the specified tolerance ( :ref:`seltol`,
        ``TOLER`` ) of the axis into a single node, then forms degenerate tetrahedrons, pyramids, or wedges.
        The default tolerance value is 1.0E-6.

        For an axisymmetric extrusion, ``SHELL208``and ``SHELL209``will extrude.

        You can control shape-checking options via the :ref:`shpp` command.

        The extrusion behavior of accompanying contact ( ``CONTA172``) is determined by the plane element
        settings. Rigid target ( ``TARGE169``) elements are extruded in the global Z direction unless
        axisymmetric extrusion ( ``Action`` = AXIS or ``Action`` = TIRE) is in effect.

        Within the 2D to 3D analysis environment (between :ref:`map2dto3d`,START and
        :ref:`map2dto3d`,FINISH), ``PLANE182``, ``PLANE183``, and associated contact/target/reinforcing
        elements are supported for the axisymmetric (with or without torsion) and plane-strain options only.
        For ``REINF263``reinforcing elements, if the fibers have an orientation angle that causes torsion in
        an axisymmetric analysis, use the axsiymmetrixc-with-torsion option (KEYOPT(3) = 6) for the base
        elements. For more information, see `2D to 3D Analysis Requirements and Limitations
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_adv/Hlp_G_ADV2DTO3DREQ.html#fnconta172173>`_

        The following table shows each 2D element capable of extrusion and its corresponding post-extrusion
        3D element:

        InformalTables need to be added.
        All element properties are also transferred consistently during extrusion. For example, a :math:````
        2D element is extruded to a  :math:````  3D element, and a mixed u-P 2D element is extruded to a
        mixed u-P 3D    element. Element and node components are passed over the 3D elements and extruded
        nodes.
        """
        command = f"EEXTRUDE,{action},{nelem},{space},{dist},{theta},{tfact},,{bckey}"
        return self.run(command, **kwargs)

    def move(
        self,
        node: str = "",
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
        r"""Calculates and moves a node to an intersection.

        Mechanical APDL Command: `MOVE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MOVE.html>`_

        Parameters
        ----------
        node : str
            Move this node. If ``NODE`` = P, graphical picking is enabled and all remaining command fields
            are ignored (valid only in the GUI). A component name may also be substituted for ``NODE``.

        kc1 : str
            First coordinate system number. Defaults to 0 (global Cartesian).

        x1 : str
            Input one or two values defining the location of the node in this coordinate system. Input "U"
            for unknown value(s) to be calculated and input "E" to use an existing coordinate value. Fields
            are R1, θ1, Z1 for cylindrical, or R1, θ1, Φ1 for spherical or toroidal.

        y1 : str
            Input one or two values defining the location of the node in this coordinate system. Input "U"
            for unknown value(s) to be calculated and input "E" to use an existing coordinate value. Fields
            are R1, θ1, Z1 for cylindrical, or R1, θ1, Φ1 for spherical or toroidal.

        z1 : str
            Input one or two values defining the location of the node in this coordinate system. Input "U"
            for unknown value(s) to be calculated and input "E" to use an existing coordinate value. Fields
            are R1, θ1, Z1 for cylindrical, or R1, θ1, Φ1 for spherical or toroidal.

        kc2 : str
            Second coordinate system number.

        x2 : str
            Input two or one value(s) defining the location of the node in this coordinate system. Input "U"
            for unknown value(s) to be calculated and input "E" to use an existing coordinate value. Fields
            are R2, θ2, Z2 for cylindrical, or R2, θ2, Φ2 for spherical or toroidal.

        y2 : str
            Input two or one value(s) defining the location of the node in this coordinate system. Input "U"
            for unknown value(s) to be calculated and input "E" to use an existing coordinate value. Fields
            are R2, θ2, Z2 for cylindrical, or R2, θ2, Φ2 for spherical or toroidal.

        z2 : str
            Input two or one value(s) defining the location of the node in this coordinate system. Input "U"
            for unknown value(s) to be calculated and input "E" to use an existing coordinate value. Fields
            are R2, θ2, Z2 for cylindrical, or R2, θ2, Φ2 for spherical or toroidal.

        Notes
        -----

        .. _MOVE_notes:

        Calculates and moves a node to an intersection location. The node may have been previously defined
        (at an approximate location) or left undefined (in which case it is internally defined at the
        :ref:`source` location). The actual location is calculated from the intersection of three surfaces
        (implied from three coordinate constants in two different coordinate systems). The three (of six)
        constants easiest to define should be used. The program will calculate the remaining three
        coordinate constants. All arguments, except ``KC1``, must be input. Use the repeat command (
        ``\*REPEAT`` ) after the :ref:`move` command to define a line of intersection by repeating the move
        operation on all nodes of the line.

        Surfaces of constant value are implied by some commands by specifying a single coordinate value.
        Implied surfaces are used with various commands ( :ref:`move`, :ref:`kmove`, :ref:`nsel`, etc.).
        Three surfaces are available with each of the four coordinate system types. Values or X, Y, or Z may
        be constant for the Cartesian coordinate system; values of R, θ, or Z for the cylindrical
        system; and values of R, θ, Φ for the spherical and toroidal systems. For example, an X value
        of 3 represents the Y-Z plane (or surface) at X=3. In addition, the parameters for the cylindrical
        and spherical coordinate systems may be adjusted ( :ref:`cs`, :ref:`local` ) to form elliptical
        surfaces. For surfaces in elliptical coordinate systems, a surface of "constant" radius is defined
        by the radius value at the X-axis. Surfaces of constant value may be located in local coordinate
        systems ( :ref:`local`, :ref:`clocal`, :ref:`cs`, or :ref:`cskp` ) to allow for any orientation.

        The intersection calculation is based on an iterative procedure (250 iterations maximum) and a
        tolerance of 1.0E-4. The approximate location of a node should be sufficient to determine a unique
        intersection if more than one intersection point is possible. Tangent "intersections" should be
        avoided. If an intersection is not found, the node is placed at the last iteration location.

        This command is also valid in the :ref:`slashmap` processor.
        """
        command = f"MOVE,{node},{kc1},{x1},{y1},{z1},{kc2},{x2},{y2},{z2}"
        return self.run(command, **kwargs)

    def transfer(
        self,
        kcnto: str = "",
        inc: str = "",
        node1: str = "",
        node2: str = "",
        ninc: str = "",
        **kwargs,
    ):
        r"""Transfers a pattern of nodes to another coordinate system.

        Mechanical APDL Command: `TRANSFER <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_TRANSFER.html>`_

        Parameters
        ----------
        kcnto : str
            Reference number of coordinate system where the pattern is to be transferred. Transfer occurs
            from the active coordinate system.

        inc : str
            Increment all nodes in the given pattern by ``INC`` to form the transferred node pattern.

        node1 : str
            Transfer nodes from pattern beginning with ``NODE1`` to ``NODE2`` (defaults to ``NODE1`` ) in
            steps of ``NINC`` (defaults to 1). If ``NODE1`` = ALL, ``NODE2`` and ``NINC`` are ignored and
            the pattern is all selected nodes ( :ref:`nsel` ). If ``NODE1`` = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in the GUI). A component may be
            substituted for ``NODE1`` ( ``NODE2`` and ``NINC`` are ignored).

        node2 : str
            Transfer nodes from pattern beginning with ``NODE1`` to ``NODE2`` (defaults to ``NODE1`` ) in
            steps of ``NINC`` (defaults to 1). If ``NODE1`` = ALL, ``NODE2`` and ``NINC`` are ignored and
            the pattern is all selected nodes ( :ref:`nsel` ). If ``NODE1`` = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in the GUI). A component may be
            substituted for ``NODE1`` ( ``NODE2`` and ``NINC`` are ignored).

        ninc : str
            Transfer nodes from pattern beginning with ``NODE1`` to ``NODE2`` (defaults to ``NODE1`` ) in
            steps of ``NINC`` (defaults to 1). If ``NODE1`` = ALL, ``NODE2`` and ``NINC`` are ignored and
            the pattern is all selected nodes ( :ref:`nsel` ). If ``NODE1`` = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in the GUI). A component may be
            substituted for ``NODE1`` ( ``NODE2`` and ``NINC`` are ignored).

        Notes
        -----

        .. _TRANSFER_notes:

        Transfers a pattern of nodes from one coordinate system to another. Coordinate systems may be
        translated and rotated relative to each other. Initial pattern may be generated in any coordinate
        system. Coordinate values are interpreted in the active coordinate system and are transferred
        directly.

        A model generated in one coordinate system may be transferred to another coordinate system. The user
        may define several coordinate systems (translated and rotated from each other), generate a model in
        one coordinate system, and then repeatedly transfer the model to other coordinate systems. The model
        may be generated in any type of coordinate system (Cartesian, cylindrical, etc.) and transferred to
        any other type of coordinate system. Coordinate values (X, Y, Z, or R, θ, Z, or etc.) of the
        model being transferred are interpreted in the active coordinate system type, regardless of how they
        were generated. Values are transferred directly and are interpreted according to the type of
        coordinate system being transferred to. For example, transferring from a Cartesian coordinate system
        to a cylindrical coordinate system (not recommended) would cause X = 2.0 and Y = 3.0 values to be
        directly interpreted as R = 2.0 and θ = 3.0 values, respectively.

        This command is also valid in the :ref:`slashmap` processor.
        """
        command = f"TRANSFER,{kcnto},{inc},{node1},{node2},{ninc}"
        return self.run(command, **kwargs)

    def nsym(
        self,
        ncomp: str = "",
        inc: str = "",
        node1: str = "",
        node2: str = "",
        ninc: str = "",
        **kwargs,
    ):
        r"""Generates a reflected set of nodes.

        Mechanical APDL Command: `NSYM <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_NSYM.html>`_

        Parameters
        ----------
        ncomp : str
            Symmetry key:

            * ``X`` - X (or R) symmetry (default).

            * ``Y`` - Y (or θ) symmetry.

            * ``Z`` - Z (or Φ) symmetry.

        inc : str
            Increment all nodes in the given pattern by ``INC`` to form the reflected node pattern.

        node1 : str
            Reflect nodes from pattern beginning with ``NODE1`` to ``NODE2`` (defaults to ``NODE1`` ) in
            steps of ``NINC`` (defaults to 1). If ``NODE1`` = ALL, ``NODE2`` and ``NINC`` are ignored and
            pattern is all selected nodes ( :ref:`nsel` ). If ``NODE1`` = P, graphical picking is enabled
            and all remaining command fields are ignored (valid only in the GUI). A component name may also
            be substituted for ``NODE1`` ( ``NODE2`` and ``NINC`` are ignored).

        node2 : str
            Reflect nodes from pattern beginning with ``NODE1`` to ``NODE2`` (defaults to ``NODE1`` ) in
            steps of ``NINC`` (defaults to 1). If ``NODE1`` = ALL, ``NODE2`` and ``NINC`` are ignored and
            pattern is all selected nodes ( :ref:`nsel` ). If ``NODE1`` = P, graphical picking is enabled
            and all remaining command fields are ignored (valid only in the GUI). A component name may also
            be substituted for ``NODE1`` ( ``NODE2`` and ``NINC`` are ignored).

        ninc : str
            Reflect nodes from pattern beginning with ``NODE1`` to ``NODE2`` (defaults to ``NODE1`` ) in
            steps of ``NINC`` (defaults to 1). If ``NODE1`` = ALL, ``NODE2`` and ``NINC`` are ignored and
            pattern is all selected nodes ( :ref:`nsel` ). If ``NODE1`` = P, graphical picking is enabled
            and all remaining command fields are ignored (valid only in the GUI). A component name may also
            be substituted for ``NODE1`` ( ``NODE2`` and ``NINC`` are ignored).

        Notes
        -----

        .. _NSYM_notes:

        Generates nodes from a given node pattern by a symmetry reflection. Reflection is done in the active
        coordinate system by changing a particular coordinate sign. Nodes in the pattern may have been
        generated in any coordinate system. Nodal rotation angles are not reflected.

        Symmetry reflection may be used with any node pattern, in any coordinate system, as many times as
        desired. Reflection is accomplished by a coordinate sign change (in the active coordinate system).
        For example, an X-reflection in a Cartesian coordinate system generates additional nodes from a
        given pattern, with a node increment added to each node number, and an X coordinate sign change. An
        R-reflection in a cylindrical coordinate system gives a reflected "radial" location by changing the
        "equivalent" Cartesian (that is, the Cartesian system with the same origin as the active cylindrical
        system) X and Y coordinate signs. An R-reflection in a spherical coordinate system gives a reflected
        "radial" location by changing the equivalent Cartesian X, Y, and Z coordinate location signs. Nodal
        coordinate system rotation angles are not reflected.
        """
        command = f"NSYM,{ncomp},{inc},{node1},{node2},{ninc}"
        return self.run(command, **kwargs)

    def nread(self, fname: str = "", ext: str = "", **kwargs):
        r"""Reads nodes from a file.

        Mechanical APDL Command: `NREAD <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_NREAD.html>`_

        Parameters
        ----------
        fname : str
            File name and directory path (248 characters maximum, including the characters needed for the
            directory path). An unspecified directory path defaults to the working directory; in this case,
            you can use all 248 characters for the file name. The file name defaults to :file:`Jobname`.

        ext : str
            Filename extension (eight-character maximum). The extension defaults to NODE if ``Fname`` is
            blank.

        Notes
        -----

        .. _NREAD_notes:

        The read operation is not necessary in a standard Mechanical APDL run but is provided as a
        convenience for
        those who want to read a coded node file (such as from another mesh generator or from a CAD/CAM
        program).

        Data should be formatted as produced via :ref:`nwrite`.

        Only nodes within the node range specified via :ref:`nrrang` are read from the file. Duplicate nodes
        already in the database are overwritten.

        The file is rewound before and after reading. Reading continues until the end of the file.
        """
        command = f"NREAD,{fname},{ext}"
        return self.run(command, **kwargs)

    def naxis(self, action: str = "", val: str = "", **kwargs):
        r"""Generates nodes for general axisymmetric element sections.

        Mechanical APDL Command: `NAXIS <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_NAXIS.html>`_

        Parameters
        ----------
        action : str
            Specifies one of the following command behaviors:

            * ``GEN`` - Generates nodes around the axis of an axisymmetric section (default).

            * ``CLEAR`` - Clears all nodes around the axis of an axisymmetric section.

            * ``EFACET`` - Specifies the number of facets per edge between nodal planes and integration planes
              in the circumferential direction to display using PowerGraphics. This option is only valid with
              :ref:`eshape`,1 and :ref:`rsys`,SOLU commands.

        val : str
            Tolerance value or number of facets per edge:

            * ``TOLER`` - When ``Action`` = GEN, the tolerance to use for merging the generated nodes around the
              axis.

            * ``NUM`` - When ``Action`` = EFACET, the number of facets per element edge for element plots:

              * ``AUTO`` - Use program-chosen facets per edge (default).

              * ``1`` - Use 1 facet per edge (default for elements with 9, 10, 11, or 12 nodal planes). Shows
                nodal and integration planes only.

              * ``2`` - Use 2 facets per edge (default for elements with 5, 6, 7, or 8 nodal planes, and maximum
                for elements with 9, 10, 11, or 12 nodal planes).

              * ``3`` - Use 3 facets per edge (default for elements with 3 or 4 nodal planes, and maximum for
                elements with 6, 7, or 8 nodal planes).

              * ``4`` - Use 4 facets per edge (maximum for elements with 5 nodal planes).

              * ``5`` - Use 5 facets per edge (maximum for elements with 4 nodal planes).

              * ``6`` - Use 6 facets per edge (maximum for elements with 3 nodal planes).

        Notes
        -----

        .. _NAXIS_notes:

        The :ref:`naxis` command generates or clears the nodes for general axisymmetric element sections.
        The command applies to elements ``SURF159``, ``SOLID272``, and ``SOLID273``.

        The generate option ( ``Action`` = GEN) operates automatically on any current-technology
        axisymmetric element. Any nodes within the tolerance value ( ``TOLER`` ) of the axis are merged into
        a single node. The default tolerance is 1.0e-4.

        If you want to change the number of nodes, use the clear option ( ``Action`` = CLEAR) before
        regenerating the nodes.

        To cause the 3D element plot to appear more like the actual 3D model, use :ref:`naxis`,EFACET,
        ``NUM``, where ``NUM`` > 1. In this case, the coordinate system specified for displaying element and
        nodal results (RSYS) must be solution ( :ref:`rsys`,SOLU); otherwise, Ansys  resets
        ``NUM`` to 1.
        """
        command = f"NAXIS,{action},{val}"
        return self.run(command, **kwargs)

    def nrotat(self, node1: str = "", node2: str = "", ninc: str = "", **kwargs):
        r"""Rotates nodal coordinate systems into the active system.

        Mechanical APDL Command: `NROTAT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_NROTAT.html>`_

        Parameters
        ----------
        node1 : str
            Rotate nodes from ``NODE1`` to ``NODE2`` (defaults to ``NODE1`` ) in steps of ``NINC`` (defaults
            to 1). If ``NODE1`` = ALL, ``NODE2`` and ``NINC`` are ignored and all selected nodes (
            :ref:`nsel` ) are rotated. If ``NODE1`` = P, graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI). A component name may also be substituted for
            ``NODE1`` ( ``NODE2`` and ``NINC`` are ignored).

        node2 : str
            Rotate nodes from ``NODE1`` to ``NODE2`` (defaults to ``NODE1`` ) in steps of ``NINC`` (defaults
            to 1). If ``NODE1`` = ALL, ``NODE2`` and ``NINC`` are ignored and all selected nodes (
            :ref:`nsel` ) are rotated. If ``NODE1`` = P, graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI). A component name may also be substituted for
            ``NODE1`` ( ``NODE2`` and ``NINC`` are ignored).

        ninc : str
            Rotate nodes from ``NODE1`` to ``NODE2`` (defaults to ``NODE1`` ) in steps of ``NINC`` (defaults
            to 1). If ``NODE1`` = ALL, ``NODE2`` and ``NINC`` are ignored and all selected nodes (
            :ref:`nsel` ) are rotated. If ``NODE1`` = P, graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI). A component name may also be substituted for
            ``NODE1`` ( ``NODE2`` and ``NINC`` are ignored).

        Notes
        -----

        .. _NROTAT_notes:

        Rotates nodal coordinate systems into the active coordinate system. Nodal coordinate systems may be
        automatically rotated into the active (global or local) coordinate system as follows: Rotations in
        Cartesian systems will have nodal x directions rotated parallel to the Cartesian X direction.
        Rotations in cylindrical, spherical or toroidal systems will have the nodal x directions rotated
        parallel to the R direction. Nodes at (or near) a zero radius location should not be rotated. Nodal
        coordinate directions may be displayed ( :ref:`psymb` ). Nodal forces and constraints will also
        appear rotated when displayed if the nodal coordinate system is rotated.

        When the nodal coordinate systems are defined, they remain parallel to the global Cartesian system
        unless subsequently rotated.

        Previously specified rotations on the specified nodes are overridden.

        See the :ref:`nmodif`, :ref:`nang`, and :ref:`nora` commands for other rotation options.
        """
        command = f"NROTAT,{node1},{node2},{ninc}"
        return self.run(command, **kwargs)

    def nkpt(self, node: str = "", npt: str = "", **kwargs):
        r"""Defines a node at an existing keypoint location.

        Mechanical APDL Command: `NKPT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_NKPT.html>`_

        Parameters
        ----------
        node : str
            Arbitrary reference number for node. If zero or blank, defaults to the highest node number +1 (
            :ref:`numstr` ).

        npt : str
            Keypoint number defining global X, Y, Z location. If ``NPT`` = All, then a node will be placed
            at each selected keypoint. If ``NPT`` = P, graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI). A component name may also be substituted for
            ``NPT``.
        """
        command = f"NKPT,{node},{npt}"
        return self.run(command, **kwargs)

    def norl(self, line: str = "", area: str = "", ndir: str = "", **kwargs):
        r"""Rotates nodal coordinate systems perpendicular to line normal

        Mechanical APDL Command: `NORL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_NORL.html>`_

        Parameters
        ----------
        line : str
            Line number containing the nodes to be rotated. If ALL, applies to all selected lines (see the
            :ref:`lsel` command). If ``LINE`` = P, graphical picking is enabled.

        area : str
            The area number containing the selected lines. The normal of the line(s) selected is supposed to
            lie on this area. Defaults to the lowest numbered selected area containing the line number.

        ndir : str
            Direction of the normal. If ``NDIR`` = -1, the nodal coordinate system is rotated in the
            opposite direction of the line normal. The default is the same direction as the surface normal.

        Notes
        -----

        .. _NORL_notes:

        The NORL command rotates the X-axis of the nodal coordinate perpendicular to the line normal. The
        rotated nodal coordinate systems may be displayed through the :ref:`psymb` command. In case multiple
        lines are selected, there could be conflicts at the boundaries. If a node belongs to two lines that
        have a different normal, its nodal coordinate system will be rotated to the line normal with the
        lowest number. Keep the following in mind when using the NORL command:

        * If the nodal coordinate system is parallel to the global Cartesian system, it is not displayed
          through the :ref:`psymb` command.

        * Previously specified rotation on the selected nodes are overridden.
        """
        command = f"NORL,{line},{area},{ndir}"
        return self.run(command, **kwargs)

    def nrrang(self, nmin: str = "", nmax: str = "", ninc: str = "", **kwargs):
        r"""Specifies the range of nodes to be read from the node file.

        Mechanical APDL Command: `NRRANG <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_NRRANG.html>`_

        Parameters
        ----------
        nmin : str
            Node range is defined from ``NMIN`` (defaults to 1) to ``NMAX`` (defaults to 999999999) in steps
            of ``NINC`` (defaults to 1).

        nmax : str
            Node range is defined from ``NMIN`` (defaults to 1) to ``NMAX`` (defaults to 999999999) in steps
            of ``NINC`` (defaults to 1).

        ninc : str
            Node range is defined from ``NMIN`` (defaults to 1) to ``NMAX`` (defaults to 999999999) in steps
            of ``NINC`` (defaults to 1).

        Notes
        -----

        .. _NRRANG_notes:

        Defines the range of nodes to be read ( :ref:`nread` ) from the node file. Also implies an element
        range since only elements fully attached to these nodes will be read from the element file.
        """
        command = f"NRRANG,{nmin},{nmax},{ninc}"
        return self.run(command, **kwargs)

    def nang(
        self,
        node: str = "",
        x1: str = "",
        x2: str = "",
        x3: str = "",
        y1: str = "",
        y2: str = "",
        y3: str = "",
        z1: str = "",
        z2: str = "",
        z3: str = "",
        **kwargs,
    ):
        r"""Rotates a nodal coordinate system by direction cosines.

        Mechanical APDL Command: `NANG <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_NANG.html>`_

        Parameters
        ----------
        node : str
            Rotate coordinate system of this node.

        x1 : str
            Global X, Y, Z components of a unit vector in new nodal X direction.

        x2 : str
            Global X, Y, Z components of a unit vector in new nodal X direction.

        x3 : str
            Global X, Y, Z components of a unit vector in new nodal X direction.

        y1 : str
            Global X, Y, Z components of a unit vector in new nodal Y direction.

        y2 : str
            Global X, Y, Z components of a unit vector in new nodal Y direction.

        y3 : str
            Global X, Y, Z components of a unit vector in new nodal Y direction.

        z1 : str
            Global X, Y, Z components of a unit vector in new nodal Z direction.

        z2 : str
            Global X, Y, Z components of a unit vector in new nodal Z direction.

        z3 : str
            Global X, Y, Z components of a unit vector in new nodal Z direction.

        Notes
        -----

        .. _NANG_notes:

        Rotates a nodal coordinate system to the orientation specified by the X, Y and Z direction cosines.
        Existing rotation specifications on the node are redefined. If only two of the three unit vectors
        are specified, the third is defined according to the right hand rule. It is the responsibility of
        the user to ensure that input direction cosines are orthogonal in a right-handed system.

        See the :ref:`nmodif`, :ref:`nrotat`,  and :ref:`nora` commands for other rotation options.
        """
        command = f"NANG,{node},{x1},{x2},{x3},{y1},{y2},{y3},{z1},{z2},{z3}"
        return self.run(command, **kwargs)

    def n(
        self,
        node: str = "",
        x: str = "",
        y: str = "",
        z: str = "",
        thxy: str = "",
        thyz: str = "",
        thzx: str = "",
        **kwargs,
    ):
        r"""Defines a node.

        Mechanical APDL Command: `N <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_N.html>`_

        Parameters
        ----------
        node : str
            Node number to be assigned. A previously defined node of the same number will be redefined.
            Defaults to the maximum node number used +1.

        x : str
            Node location in the active coordinate system (R, θ, Z for cylindrical, R, θ, Φ for spherical or
            toroidal). If ``X`` = P, graphical picking is enabled and all remaining command fields are
            ignored (valid only in the GUI).

        y : str
            Node location in the active coordinate system (R, θ, Z for cylindrical, R, θ, Φ for spherical or
            toroidal). If ``X`` = P, graphical picking is enabled and all remaining command fields are
            ignored (valid only in the GUI).

        z : str
            Node location in the active coordinate system (R, θ, Z for cylindrical, R, θ, Φ for spherical or
            toroidal). If ``X`` = P, graphical picking is enabled and all remaining command fields are
            ignored (valid only in the GUI).

        thxy : str
            First rotation about nodal Z (positive X toward Y).

        thyz : str
            Second rotation about nodal X (positive Y toward Z).

        thzx : str
            Third rotation about nodal Y (positive Z toward X).

        Returns
        -------
        int
            Node number of the generated node.

        Notes
        -----

        .. _N_notes:

        Defines a node in the active coordinate system ( :ref:`csys` ). The nodal coordinate system is
        parallel to the global Cartesian system unless rotated. Rotation angles are in degrees and redefine
        any previous rotation angles. See the :ref:`nmodif`, :ref:`nang`, :ref:`nrotat`, and :ref:`nora`
        commands for other rotation options.

        Examples
        --------
        Create a node at ``(0, 1, 1)``

        >>> nnum = mapdl.n("", 0, 1, 1)
        >>> nnum
        1

        Create a node at ``(4, 5, 1)`` with a node ID of 10

        >>> nnum = mapdl.n(10, 4, 5, 1)
        >>> nnum
        10
        """
        command = f"N,{node},{x},{y},{z},{thxy},{thyz},{thzx}"
        return parse.parse_n(self.run(command, **kwargs))

    def nlist(
        self,
        node1: str = "",
        node2: str = "",
        ninc: str = "",
        lcoord: str = "",
        sort1: str = "",
        sort2: str = "",
        sort3: str = "",
        kinternal: str = "",
        **kwargs,
    ):
        r"""Lists nodes.

        Mechanical APDL Command: `NLIST <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_NLIST.html>`_

        Parameters
        ----------
        node1 : str
            List nodes from ``NODE1`` to ``NODE2`` (defaults to ``NODE1`` ) in steps of ``NINC`` (defaults
            to 1). If ``NODE1`` = ALL (default), ``NODE2`` and ``NINC`` are ignored and all selected nodes (
            :ref:`nsel` ) are listed. If ``NODE1`` = P, graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI). A component name may also be substituted for
            ``NODE1`` ( ``NODE2`` and ``NINC`` are ignored).

        node2 : str
            List nodes from ``NODE1`` to ``NODE2`` (defaults to ``NODE1`` ) in steps of ``NINC`` (defaults
            to 1). If ``NODE1`` = ALL (default), ``NODE2`` and ``NINC`` are ignored and all selected nodes (
            :ref:`nsel` ) are listed. If ``NODE1`` = P, graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI). A component name may also be substituted for
            ``NODE1`` ( ``NODE2`` and ``NINC`` are ignored).

        ninc : str
            List nodes from ``NODE1`` to ``NODE2`` (defaults to ``NODE1`` ) in steps of ``NINC`` (defaults
            to 1). If ``NODE1`` = ALL (default), ``NODE2`` and ``NINC`` are ignored and all selected nodes (
            :ref:`nsel` ) are listed. If ``NODE1`` = P, graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI). A component name may also be substituted for
            ``NODE1`` ( ``NODE2`` and ``NINC`` are ignored).

        lcoord : str
            Coordinate listing key:

            * ``(blank)`` - List all nodal information

            * ``COORD`` - Suppress all but the XYZ coordinates (shown to a higher degree of accuracy than when
              displayed with all information).

        sort1 : str
            First item on which to sort. Valid item names are NODE, X, Y, Z, THXY, THYZ, THXZ

        sort2 : str
            Second and third items on which to sort. Valid item names are the same as for ``SORT1``.

        sort3 : str
            Second and third items on which to sort. Valid item names are the same as for ``SORT1``.

        kinternal : str
            Internal nodes listing key:

            * ``(blank)`` - List only external nodes.

            * ``INTERNAL`` - List all nodes, including internal nodes.

        Notes
        -----

        .. _NLIST_notes:

        Lists nodes in the active display coordinate system ( :ref:`dsys` ). Nodal coordinate rotation
        angles are also listed (relative to the global Cartesian coordinate system).

        Node listing can be in a sorted order (ascending). ``SORT2``, for example, will be carried out on
        nodes having equal values of ``SORT1``.

        This command is valid in any processor.
        """
        command = (
            f"NLIST,{node1},{node2},{ninc},{lcoord},{sort1},{sort2},{sort3},{kinternal}"
        )
        return self.run(command, **kwargs)

    def nscale(
        self,
        inc: str = "",
        node1: str = "",
        node2: str = "",
        ninc: str = "",
        rx: str = "",
        ry: str = "",
        rz: str = "",
        **kwargs,
    ):
        r"""Generates a scaled set of nodes from a pattern of nodes.

        Mechanical APDL Command: `NSCALE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_NSCALE.html>`_

        Parameters
        ----------
        inc : str
            Do this scaling operation one time, incrementing all nodes in the given pattern by ``INC``. If
            ``INC`` = 0, nodes will be redefined at the scaled locations.

        node1 : str
            Scale nodes from pattern of nodes beginning with ``NODE1`` to ``NODE2`` (defaults to ``NODE1`` )
            in steps of ``NINC`` (defaults to 1). If ``NODE1`` = ALL, ``NODE2`` and ``NINC`` are ignored and
            pattern is all selected nodes ( :ref:`nsel` ). If ``NODE1`` = P, graphical picking is enabled
            and all remaining command fields are ignored (valid only in the GUI). A component name may also
            be substituted for ``NODE1`` ( ``NODE2`` and ``NINC`` are ignored).

        node2 : str
            Scale nodes from pattern of nodes beginning with ``NODE1`` to ``NODE2`` (defaults to ``NODE1`` )
            in steps of ``NINC`` (defaults to 1). If ``NODE1`` = ALL, ``NODE2`` and ``NINC`` are ignored and
            pattern is all selected nodes ( :ref:`nsel` ). If ``NODE1`` = P, graphical picking is enabled
            and all remaining command fields are ignored (valid only in the GUI). A component name may also
            be substituted for ``NODE1`` ( ``NODE2`` and ``NINC`` are ignored).

        ninc : str
            Scale nodes from pattern of nodes beginning with ``NODE1`` to ``NODE2`` (defaults to ``NODE1`` )
            in steps of ``NINC`` (defaults to 1). If ``NODE1`` = ALL, ``NODE2`` and ``NINC`` are ignored and
            pattern is all selected nodes ( :ref:`nsel` ). If ``NODE1`` = P, graphical picking is enabled
            and all remaining command fields are ignored (valid only in the GUI). A component name may also
            be substituted for ``NODE1`` ( ``NODE2`` and ``NINC`` are ignored).

        rx : str
            Scale factor ratios. Scaling is relative to the origin of the active coordinate system (RR, Rθ,
            RZ for cylindrical, RR, Rθ, RΦ for spherical or toroidal). If absolute value of ratio > 1.0,
            pattern is enlarged. If < 1.0, pattern is reduced. Ratios default to 1.0 (each).

        ry : str
            Scale factor ratios. Scaling is relative to the origin of the active coordinate system (RR, Rθ,
            RZ for cylindrical, RR, Rθ, RΦ for spherical or toroidal). If absolute value of ratio > 1.0,
            pattern is enlarged. If < 1.0, pattern is reduced. Ratios default to 1.0 (each).

        rz : str
            Scale factor ratios. Scaling is relative to the origin of the active coordinate system (RR, Rθ,
            RZ for cylindrical, RR, Rθ, RΦ for spherical or toroidal). If absolute value of ratio > 1.0,
            pattern is enlarged. If < 1.0, pattern is reduced. Ratios default to 1.0 (each).

        Notes
        -----

        .. _NSCALE_notes:

        Generates a scaled pattern of nodes from a given node pattern. Scaling is done in the active
        coordinate system. Nodes in the pattern may have been generated in any coordinate system.

        This command is also valid in the :ref:`slashmap` processor.
        """
        command = f"NSCALE,{inc},{node1},{node2},{ninc},{rx},{ry},{rz}"
        return self.run(command, **kwargs)

    def nmodif(
        self,
        node: str = "",
        x: str = "",
        y: str = "",
        z: str = "",
        thxy: str = "",
        thyz: str = "",
        thzx: str = "",
        **kwargs,
    ):
        r"""Modifies an existing node.

        Mechanical APDL Command: `NMODIF <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_NMODIF.html>`_

        Parameters
        ----------
        node : str
            Modify coordinates of this node. If ALL, modify coordinates of all selected nodes ( :ref:`nsel`
            ). If ``NODE`` = P, graphical picking is enabled and all remaining command fields are ignored
            (valid only in the GUI). A component name may also be substituted for ``NODE``.

        x : str
            Replace the previous coordinate values assigned to this node with these corresponding coordinate
            values. Values are interpreted in the active coordinate system (R, θ, Z for cylindrical; R, θ, Φ
            for spherical or toroidal). Leaving any of these fields blank retains the previous value(s).

        y : str
            Replace the previous coordinate values assigned to this node with these corresponding coordinate
            values. Values are interpreted in the active coordinate system (R, θ, Z for cylindrical; R, θ, Φ
            for spherical or toroidal). Leaving any of these fields blank retains the previous value(s).

        z : str
            Replace the previous coordinate values assigned to this node with these corresponding coordinate
            values. Values are interpreted in the active coordinate system (R, θ, Z for cylindrical; R, θ, Φ
            for spherical or toroidal). Leaving any of these fields blank retains the previous value(s).

        thxy : str
            First rotation of nodal coordinate system about nodal Z (positive X toward Y). Leaving this
            field blank retains the previous value.

        thyz : str
            Second rotation of nodal coordinate system about nodal X (positive Y toward Z). Leaving this
            field blank retains the previous value.

        thzx : str
            Third rotation of nodal coordinate system about nodal Y (positive Z toward X). Leaving this
            field blank retains the previous value.

        Notes
        -----

        .. _NMODIF_notes:

        Modifies an existing node. Nodal coordinate system rotation angles are in degrees and redefine any
        existing rotation angles. Nodes can also be redefined with the :ref:`n` command.

        See the :ref:`nrotat`, :ref:`nang`, and :ref:`nora` commands for other rotation options.

        This command is also valid in the :ref:`slashmap` processor.
        """
        command = f"NMODIF,{node},{x},{y},{z},{thxy},{thyz},{thzx}"
        return self.run(command, **kwargs)

    def nwrite(self, fname: str = "", ext: str = "", kappnd: int | str = "", **kwargs):
        r"""Writes nodes to a file.

        Mechanical APDL Command: `NWRITE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_NWRITE.html>`_

        Parameters
        ----------
        fname : str
            File name and directory path (248 characters maximum, including the characters needed for the
            directory path). An unspecified directory path defaults to the working directory; in this case,
            you can use all 248 characters for the file name. The file name defaults to :file:`Jobname`.

        ext : str
            Filename extension (eight-character maximum). The extension defaults to NODE if ``Fname`` is
            blank.

        kappnd : int or str
            Append key:

            * ``0`` - Rewind file before the write operation.

            * ``1`` - Append data to the end of the existing file.

        Notes
        -----

        .. _NWRITE_notes:

        Writes selected nodes ( :ref:`nsel` ]) to a file. The write operation is not necessary in a standard
        Mechanical APDL run but is provided as a convenience to those who want coded node file.

        Data are written in a coded format. The format used is (I9, 6G21.13E3) to write out ``NODE``, ``X``,
        ``Y``, ``Z``, ``THXY``, ``THYZ``, ``THZX``. If the last number is zero ( ``THZX`` = 0), or the last
        set of numbers are zero, they are not written but are left blank. Therefore, use a formatted read to
        process this file.

        Coordinate values are in the global Cartesian system.
        """
        command = f"NWRITE,{fname},{ext},,{kappnd}"
        return self.run(command, **kwargs)

    def nplot(self, knum: int | str = "", **kwargs):
        r"""Displays nodes.

        Mechanical APDL Command: `NPLOT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_NPLOT.html>`_

        Parameters
        ----------
        knum : int or str
            Node number key:

            * ``0`` - No node numbers on display.

            * ``1`` - Include node numbers on display. See also :ref:`pnum` command.

        Notes
        -----

        .. _NPLOT_notes:

        Produces a node display. Only selected nodes ( :ref:`nsel` ) are displayed. Elements need not be
        defined. See the :ref:`dsys` command for display coordinate system.

        This command is valid in any processor.
        """
        command = f"NPLOT,{knum}"
        return self.run(command, **kwargs)

    def ndele(self, node1: str = "", node2: str = "", ninc: str = "", **kwargs):
        r"""Deletes nodes.

        Mechanical APDL Command: `NDELE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_NDELE.html>`_

        Parameters
        ----------
        node1 : str
            Delete nodes from ``NODE1`` to ``NODE2`` (defaults to ``NODE1`` ) in steps of ``NINC`` (defaults
            to 1). If ``NODE1`` = ALL, ``NODE2`` and ``NINC`` are ignored and all selected nodes (
            :ref:`nsel` ) are deleted. If ``NODE1`` = P, graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI). A component name may also be substituted for
            ``NODE1``.

        node2 : str
            Delete nodes from ``NODE1`` to ``NODE2`` (defaults to ``NODE1`` ) in steps of ``NINC`` (defaults
            to 1). If ``NODE1`` = ALL, ``NODE2`` and ``NINC`` are ignored and all selected nodes (
            :ref:`nsel` ) are deleted. If ``NODE1`` = P, graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI). A component name may also be substituted for
            ``NODE1``.

        ninc : str
            Delete nodes from ``NODE1`` to ``NODE2`` (defaults to ``NODE1`` ) in steps of ``NINC`` (defaults
            to 1). If ``NODE1`` = ALL, ``NODE2`` and ``NINC`` are ignored and all selected nodes (
            :ref:`nsel` ) are deleted. If ``NODE1`` = P, graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI). A component name may also be substituted for
            ``NODE1``.

        Notes
        -----

        .. _NDELE_notes:

        Deletes selected nodes that are not connected to elements. Nodes may also be redefined instead of
        deleted, if desired. Boundary conditions (displacements, forces, etc.) as well as any coupling or
        constraint equations containing the deleted nodes are also deleted.

        This command is also valid in the :ref:`slashmap` processor.
        """
        command = f"NDELE,{node1},{node2},{ninc}"
        return self.run(command, **kwargs)

    def ndist(self, nd1: str = "", nd2: str = "", **kwargs):
        r"""Calculates and lists the distance between two nodes.

        Mechanical APDL Command: `NDIST <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_NDIST.html>`_

        Parameters
        ----------
        nd1 : str
            First node in distance calculation. If ``ND1`` = P, graphical picking is enabled and all
            remaining command fields are ignored (valid only in the GUI).

        nd2 : str
            Second node in distance calculation.

        Returns
        -------
            list
            ``[DIST, X, Y, Z]`` distance between two nodes.

        Notes
        -----

        .. _NDIST_notes:

        :ref:`ndist` lists the distance between nodes ``ND1`` and ``ND2``, as well as the current coordinate
        system offsets from ``ND1`` to ``ND2``, where the X, Y, and Z locations of ``ND1`` are subtracted
        from the X, Y, and Z locations of ``ND2`` (respectively) to determine the offsets. :ref:`ndist` is
        valid in any coordinate system except toroidal ( :ref:`csys`,3).

        :ref:`ndist` returns a variable, called " ``_RETURN``," which contains the distance value. You can
        use this value for various purposes, such as the calculation of distributed loads. In interactive
        mode, you can access this command by using the Model Query Picker ( Utility Menu> List> Picked
        Entities ), where you can also access automatic annotation functions and display the value on your
        model.

        This command is valid in any processor.

        Examples
        --------
        Compute the distance between two nodes.

        >>> node1 = (0, 8, -3)
        >>> node2 = (13, 5, 7)
        >>> node_num1 = mapdl.n("", *node1)
        >>> node_num2 = mapdl.n("", *node2)
        >>> node_dist = mapdl.ndist(node_num1, node_num2)
        >>> node_dist
        [16.673332000533065, 13.0, -3.0, 10.0]
        """
        return parse.parse_ndist(self.run(f"NDIST,{nd1},{nd2}", **kwargs))

    def nora(self, area: str = "", ndir: str = "", **kwargs):
        r"""Rotates nodal coordinate systems to surface normal

        Mechanical APDL Command: `NORA <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_NORA.html>`_

        Parameters
        ----------
        area : str
            The area number containing the nodes to be rotated to their normals. If ALL, applies to all
            selected areas (see the :ref:`asel` command). If AREA = P, graphical picking is enabled.

        ndir : str
            Direction of the normal. If NDIR = -1, the nodal coordinate system is rotated in the opposite
            direction of the surface normal. The default is the same direction as the surface normal.

        Notes
        -----

        .. _NORA_notes:

        The NORA command rotates the X-axis of the nodal coordinate system to the surface normal. The
        rotated nodal coordinate systems may be displayed through the :ref:`psymb` command. In case multiple
        areas are selected, there could be conflicts at the boundaries. If a node belongs to two areas that
        have a different normal, its nodal coordinate system will be rotated to the area normal with the
        lowest number. You can use the :ref:`areverse` and :ref:`anorm` commands to rotate the surface
        normals in the appropriate direction. Keep the following in mind when using the NORA command:

        * If the nodal coordinate system is parallel to the global Cartesian system, it is not displayed
          through the :ref:`psymb` command.

        * Previously specified rotation on the selected nodes are overridden.
        """
        command = f"NORA,{area},{ndir}"
        return self.run(command, **kwargs)

    def ngen(
        self,
        itime: str = "",
        inc: str = "",
        node1: str = "",
        node2: str = "",
        ninc: str = "",
        dx: str = "",
        dy: str = "",
        dz: str = "",
        space: str = "",
        **kwargs,
    ):
        r"""Generates additional nodes from a pattern of nodes.

        Mechanical APDL Command: `NGEN <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_NGEN.html>`_

        Parameters
        ----------
        itime : str
            Do this generation operation a total of ``ITIME`` times, incrementing all nodes in the given
            pattern by ``INC`` each time after the first. ``ITIME`` must be > 1 for generation to occur.

        inc : str
            Do this generation operation a total of ``ITIME`` times, incrementing all nodes in the given
            pattern by ``INC`` each time after the first. ``ITIME`` must be > 1 for generation to occur.

        node1 : str
            Generate nodes from the pattern of nodes beginning with ``NODE1`` to ``NODE2`` (defaults to
            ``NODE1`` ) in steps of ``NINC`` (defaults to 1). If ``NODE1`` = ALL, ``NODE2`` and ``NINC`` are
            ignored and the pattern is all selected nodes ( :ref:`nsel` ). If ``NODE1`` = P, graphical
            picking is enabled and all remaining command fields are ignored (valid only in the GUI). A
            component name may also be substituted for ``NODE1`` ( ``NODE2`` and ``NINC`` are ignored).

        node2 : str
            Generate nodes from the pattern of nodes beginning with ``NODE1`` to ``NODE2`` (defaults to
            ``NODE1`` ) in steps of ``NINC`` (defaults to 1). If ``NODE1`` = ALL, ``NODE2`` and ``NINC`` are
            ignored and the pattern is all selected nodes ( :ref:`nsel` ). If ``NODE1`` = P, graphical
            picking is enabled and all remaining command fields are ignored (valid only in the GUI). A
            component name may also be substituted for ``NODE1`` ( ``NODE2`` and ``NINC`` are ignored).

        ninc : str
            Generate nodes from the pattern of nodes beginning with ``NODE1`` to ``NODE2`` (defaults to
            ``NODE1`` ) in steps of ``NINC`` (defaults to 1). If ``NODE1`` = ALL, ``NODE2`` and ``NINC`` are
            ignored and the pattern is all selected nodes ( :ref:`nsel` ). If ``NODE1`` = P, graphical
            picking is enabled and all remaining command fields are ignored (valid only in the GUI). A
            component name may also be substituted for ``NODE1`` ( ``NODE2`` and ``NINC`` are ignored).

        dx : str
            Node location increments in the active coordinate system (DR, Dθ, DZ for cylindrical, DR, Dθ, DΦ
            for spherical or toroidal).

        dy : str
            Node location increments in the active coordinate system (DR, Dθ, DZ for cylindrical, DR, Dθ, DΦ
            for spherical or toroidal).

        dz : str
            Node location increments in the active coordinate system (DR, Dθ, DZ for cylindrical, DR, Dθ, DΦ
            for spherical or toroidal).

        space : str
            Spacing ratio. Ratio of last division size to first division size. If > 1.0, divisions increase.
            If < 1.0, divisions decrease. Ratio defaults to 1.0 (uniform spacing).

            The average spacing ratio remains 1.0, such that the location of the last generated set will be
            the same regardless of ``SPACE``. ``SPACE`` only serves to skew the position of the nodes
            between the pattern set and the last set.

        Notes
        -----

        .. _NGEN_notes:

        Generates additional nodes from a given node pattern. Generation is done in the active coordinate
        system. Nodes in the pattern may have been generated in any coordinate system.

        This command is also valid in the :ref:`slashmap` processor.
        """
        command = f"NGEN,{itime},{inc},{node1},{node2},{ninc},{dx},{dy},{dz},{space}"
        return self.run(command, **kwargs)

    def nsmooth(self, npass: str = "", **kwargs):
        r"""Smooths selected nodes among selected elements.

        Mechanical APDL Command: `NSMOOTH <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_NSMOOTH.html>`_

        Parameters
        ----------
        npass : str
            Number of smoothing passes. Defaults to 3.

        Notes
        -----

        .. _NSMOOTH_notes:

        Repositions each selected node at the average position of its immediate neighbors on the selected
        elements. The node positions converge after some number of smoothing passes. For some initial
        conditions, ``NPASS`` may need to be much larger than 3. If the boundary of a mesh is to be
        undisturbed (usually desirable), the boundary nodes should be unselected before issuing
        :ref:`nsmooth`.
        """
        command = f"NSMOOTH,{npass}"
        return self.run(command, **kwargs)

    def center(
        self,
        node: str = "",
        node1: str = "",
        node2: str = "",
        node3: str = "",
        radius: int | str = "",
        **kwargs,
    ):
        r"""Defines a node at the center of curvature of 2 or 3 nodes.

        Mechanical APDL Command: `CENTER <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CENTER.html>`_

        Parameters
        ----------
        node : str
            Number to be assigned to the node generated at the center of curvature.

        node1 : str
            Three nodes used to calculated the center of curvature, as described under ``RADIUS``.

        node2 : str
            Three nodes used to calculated the center of curvature, as described under ``RADIUS``.

        node3 : str
            Three nodes used to calculated the center of curvature, as described under ``RADIUS``.

        radius : int or str
            Used to control the interpretation of ``NODE1``, ``NODE2`` and ``NODE3`` :

            * ``0`` - ``NODE1``, ``NODE2`` and ``NODE3`` lie on a circular arc. The program will calculate the
              center of curvature (and radius) (default).

            * ``≠,  0`` - ``NODE1`` and ``NODE2`` are the endpoints of an arc, and ``RADIUS`` is the
              radius of curvature. The program will locate the center of curvature on the ``NODE3`` side of the
              ``NODE1`` - ``NODE2`` line if ``RADIUS`` > 0, and opposite to ``NODE3`` if ``RADIUS`` < 0.

        """
        command = f"CENTER,{node},{node1},{node2},{node3},{radius}"
        return self.run(command, **kwargs)

    def quad(
        self,
        node1: str = "",
        nintr: str = "",
        node2: str = "",
        nfill: str = "",
        nstrt: str = "",
        ninc: str = "",
        pkfac: str = "",
        **kwargs,
    ):
        r"""Generates a quadratic line of nodes from three nodes.

        Mechanical APDL Command: `QUAD <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_QUAD.html>`_

        Parameters
        ----------
        node1 : str
            Begin fill-in from this node location. If ``NODE1`` = P, graphical picking is enabled and all
            remaining command fields are ignored (valid only in the GUI).

        nintr : str
            Intermediate or guiding node. Quadratic curve will pass through this location. ``NINTR`` may
            have any node number and any location. If the quadratic line also generates a node with number
            ``NINTR``, the generated location overrides the previous ``NINTR`` location.

        node2 : str
            End quadratic fill-in at this node location.

        nfill : str
            Fill-in ``NFILL`` nodes between ``NODE1`` and ``NODE2`` (defaults to | ``NODE2`` - ``NODE1``
            |-1). ``NFILL`` must be positive.

        nstrt : str
            Node number assigned to first filled-in node (defaults to ``NODE1`` + ``NINC`` ).

        ninc : str
            Add this increment to each of the remaining filled-in node numbers (may be positive or
            negative). Defaults to ( ``NODE2`` - ``NODE1`` )/( ``NFILL`` + 1), that is, linear
            interpolation.

        pkfac : str
            Peak location factor. If ``PKFAC`` =0.5, the peak of the quadratic shape occurs at the ``NINTR``
            location. If 0.0 < ``PKFAC`` < 0.5, the peak occurs to the ``NODE2`` side of the ``NINTR``
            location. If 0.5 < ``PKFAC`` < 1.0, the peak occurs to the ``NODE1`` side of the ``NINTR``
            location. Defaults to 0.5.

        Notes
        -----

        .. _QUAD_notes:

        Generates a quadratic line of nodes (in the active coordinate system) from three nodes. The three
        nodes determine the plane of the curve and may have been defined in any coordinate system. Any
        number of nodes may be filled-in and any node number sequence may be assigned.

        The quadratic line feature uses three nodes ( ``NODE1``, ``NINTR``, ``NODE2`` ) to determine the
        plane of the curve. The curve passes through the three points, beginning from ``NODE1``, through the
        intermediate (or guiding) point ``NINTR``, and toward ``NODE2``.

        Generated nodes are also quadratically spaced. If the guiding node number is within the set being
        generated, it will be relocated according to the quadratic spacing.

        The peak location factor is used to determine how the quadratic fits through the three points.
        Various nodal progressions can be obtained by different combinations of ``PKFAC`` and the guiding
        node location. If the guiding node is at mid-length between ``NODE1`` and ``NODE2``, 0.293
        :math:````   ``PKFAC`` < 0.707 will ensure that all generated nodes fall within the ``NODE1``,
        ``NODE2`` bounds. In the limit, as ``PKFAC`` approaches 0.0, the peak approaches the line through
        ``NODE1`` and ``NINTR`` at an infinite distance from ``NODE1``. The :ref:`quad` command generates
        quadratic lines of nodes, which in turn may be used as a base line for generating irregular surfaces
        of nodes (by repeating ( ``\*REPEAT`` ), generating ( :ref:`ngen`, :ref:`nscale` ), etc.). Irregular
        surfaces may also be generated with the meshing commands.
        """
        command = f"QUAD,{node1},{nintr},{node2},{nfill},{nstrt},{ninc},{pkfac}"
        return self.run(command, **kwargs)

    def fill(
        self,
        node1: str = "",
        node2: str = "",
        nfill: str = "",
        nstrt: str = "",
        ninc: str = "",
        itime: str = "",
        inc: str = "",
        space: str = "",
        **kwargs,
    ):
        r"""Generates a line of nodes between two existing nodes.

        Mechanical APDL Command: `FILL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_FILL.html>`_

        Parameters
        ----------
        node1 : str
            Beginning and ending nodes for fill-in. ``NODE1`` defaults to next to last node specified,
            ``NODE2`` defaults to last node specified. If ``NODE1`` = P, graphical picking is enabled and
            all remaining command fields are ignored (valid only in the GUI).

        node2 : str
            Beginning and ending nodes for fill-in. ``NODE1`` defaults to next to last node specified,
            ``NODE2`` defaults to last node specified. If ``NODE1`` = P, graphical picking is enabled and
            all remaining command fields are ignored (valid only in the GUI).

        nfill : str
            Fill ``NFILL`` nodes between ``NODE1`` and ``NODE2`` (defaults to \| ``NODE2`` - ``NODE1`` \|-1).
            ``NFILL`` must be positive.

        nstrt : str
            Node number assigned to first filled-in node (defaults to ``NODE1`` + ``NINC`` ).

        ninc : str
            Add this increment to each of the remaining filled-in node numbers (may be positive or
            negative). Defaults to the integer result of ( ``NODE2`` - ``NODE1`` )/( ``NFILL`` + 1), that
            is, linear interpolation. If the default evaluates to zero, or if zero is input, ``NINC`` is set
            to 1.

        itime : str
            Do fill-in operation a total of ``ITIMEs``, incrementing ``NODE1``, ``NODE2`` and ``NSTRT`` by
            ``INC`` each time after the first. ``ITIME`` and ``INC`` both default to 1.

        inc : str
            Do fill-in operation a total of ``ITIMEs``, incrementing ``NODE1``, ``NODE2`` and ``NSTRT`` by
            ``INC`` each time after the first. ``ITIME`` and ``INC`` both default to 1.

        space : str
            Spacing ratio. Ratio of last division size to first division size. If > 1.0, divisions increase.
            If < 1.0, divisions decrease. Ratio defaults to 1.0 (uniform spacing).

        Notes
        -----

        .. _FILL_notes:

        Generates a line of nodes (in the active coordinate system) between two existing nodes. The two
        nodes may have been defined in any coordinate system. Nodal locations and rotation angles are
        determined by interpolation. Any number of nodes may be filled-in and any node number sequence may
        be assigned. See the :ref:`cscir` command when filling across the 180° singularity line in a non-
        Cartesian system.
        """
        command = f"FILL,{node1},{node2},{nfill},{nstrt},{ninc},{itime},{inc},{space}"
        return self.run(command, **kwargs)
