from .core import _QueryExecution


class _ComponentQueries(_QueryExecution):
    _mapdl = None

    def centrx(self, e: int) -> float:
        """Return the x coordinate of the element centroid.

        Fetches centroid X-coordinate of element ``e`` in global
        Cartesian coordinate system. Centroid is determined from the
        selected nodes on the element.

        Parameters
        ----------
        e : int
            The element number of the element to be considered.

        Returns
        -------
        float
            The centroid coordinate.

        Examples
        --------
        Here we construct a line between the coordinates ``(0, 0, 0)``
        and ``(1, 2, 3)`` then find the centroid x-coordinate of this
        element.

        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> n0 = mapdl.n(1, 0, 0, 0)
        >>> n1 = mapdl.n(2, 1, 2, 3)
        >>> mapdl.et(1, 'LINK11')
        >>> e0 = mapdl.e(n0, n1)
        >>> mapdl.queries.centrx(e0)
        0.5
        """
        return self._run_query(f"CENTRX({e})", integer=False)

    def centry(self, e: int) -> float:
        """Return the y coordinate of the element centroid.

        Fetches centroid Y-coordinate of element ``e`` in global
        Cartesian coordinate system. Centroid is determined from the
        selected nodes on the element.

        Parameters
        ----------
        e : int
            The element number of the element to be considered.

        Returns
        -------
        float
            The centroid coordinate.

        Examples
        --------
        Here we construct a line between the coordinates (0, 0, 0) and
        (1, 2, 3) then find the centroid y-coordinate of this element.

        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> n0 = mapdl.n(1, 0, 0, 0)
        >>> n1 = mapdl.n(2, 1, 2, 3)
        >>> mapdl.et(1, 'LINK11')
        >>> e0 = mapdl.e(n0, n1)
        >>> mapdl.queries.centry(e0)
        1.0
        """
        return self._run_query(f"CENTRY({e})", integer=False)

    def centrz(self, e: int) -> float:
        """Return the z coordinate of the element centroid.

        Fetches centroid Z-coordinate of element ``e`` in global
        Cartesian coordinate system. Centroid is determined from the
        selected nodes on the element.

        Parameters
        ----------
        e : int
            The element number of the element to be considered.

        Returns
        -------
        float
            The centroid coordinate.

        Examples
        --------
        Here we construct a line between the coordinates (0, 0, 0) and
        (1, 2, 3) then find the centroid z-coordinate of this element.

        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> n0 = mapdl.n(1, 0, 0, 0)
        >>> n1 = mapdl.n(2, 1, 2, 3)
        >>> mapdl.et(1, 'LINK11')
        >>> e0 = mapdl.e(n0, n1)
        >>> mapdl.queries.centrz(e0)
        1.5
        """
        return self._run_query(f"CENTRZ({e})", integer=False)

    def nx(self, n: int) -> float:
        """Return the x coordinate of a node.

        Fetches X-coordinate of node ``n`` in the active coordinate
        system.

        Parameters
        ----------
        n : int
            Node number

        Returns
        -------
        float
             Coordinate of node

        Examples
        --------
        Here we construct a simple box and mesh it with elements. Then
        we use the ``nx`` method from the ``queries`` attribute to
        find the x-coordinate of the 10th node.

        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> mapdl.et(1, 'SOLID5')
        >>> mapdl.block(0, 10, 0, 20, 0, 30)
        >>> mapdl.esize(2)
        >>> mapdl.vmesh('ALL')
        >>> mapdl.queries.nx(10)
        0.0
        """
        return self._run_query(f"NX({n})", integer=False)

    def ny(self, n: int) -> float:
        """Return the y coordinate of a node.

        Fetches Y-coordinate of node ``n`` in the active coordinate
        system.

        Parameters
        ----------
        n : int
            Node number

        Returns
        -------
        float
             Coordinate of node

        Examples
        --------
        Here we construct a simple box and mesh it with elements. Then
        we use the the ``ny`` method from the ``queries`` attribute to
        find the y-coordinate of the 10th node.

        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> mapdl.et(1, 'SOLID5')
        >>> mapdl.block(0, 10, 0, 20, 0, 30)
        >>> mapdl.esize(2)
        >>> mapdl.vmesh('ALL')
        >>> mapdl.queries.ny(10)
        4.0
        """
        return self._run_query(f"NY({n})", integer=False)

    def nz(self, n: int) -> float:
        """Return the z coordinate of a node.

        Fetches Z-coordinate of node ``n`` in the active coordinate
        system.

        Parameters
        ----------
        n : int
            Node number

        Returns
        -------
        float
             Coordinate of node

        Examples
        --------
        Here we construct a simple box and mesh it with elements. Then
        we use the ``nz`` attribute from the ``queries`` attribute to
        find the z-coordinate of the 10th node.

        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> mapdl.et(1, 'SOLID5')
        >>> mapdl.block(0, 10, 0, 20, 0, 30)
        >>> mapdl.esize(2)
        >>> mapdl.vmesh('ALL')
        >>> mapdl.queries.nz(10)
        0.0
        """
        return self._run_query(f"NZ({n})", integer=False)

    def kx(self, k: int) -> float:
        """Return the x coordinate of a keypont.

        X-coordinate of keypoint ``k`` in the active coordinate system.

        Parameters
        ----------
        k : int
            Keypoint number to be considered.

        Returns
        -------
        float
            Coordinate of the keypoint.

        Examples
        --------
        Here we add a single keypoint, then use ``kx`` to extract the
        x-coordinate of it.

        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> mapdl.k(1, 0, 1, 2)
        >>> mapdl.queries.kx(1)
        0.0
        """
        return self._run_query(f"KX({k})", integer=False)

    def ky(self, k: int) -> float:
        """Return the y coordinate of a keypont.

        Y-coordinate of keypoint ``k`` in the active coordinate system.

        Parameters
        ----------
        k : int
            Keypoint number to be considered.

        Returns
        -------
        float
            Coordinate of the keypoint.

        Examples
        --------
        Here we add a single keypoint, then use ``ky`` to extract the
        y-coordinate of it.

        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> mapdl.k(1, 0, 1, 2)
        >>> mapdl.queries.ky(1)
        1.0
        """
        return self._run_query(f"KY({k})", integer=False)

    def kz(self, k: int) -> float:
        """Return the z coordinate of a keypont.

        Z-coordinate of keypoint ``k`` in the active coordinate system.

        Parameters
        ----------
        k : int
            Keypoint number to be considered.

        Returns
        -------
        float
            Coordinate of the keypoint.

        Examples
        --------
        Here we add a single keypoint, then use ``kz`` to extract the
        z-coordinate of it.

        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> mapdl.k(1, 0, 1, 2)
        >>> mapdl.queries.kz(1)
        2.0
        """
        return self._run_query(f"KZ({k})", integer=False)


class _InverseGetComponentQueries(_QueryExecution):
    _mapdl = None

    def node(self, x: float, y: float, z: float) -> int:
        """Return node closest to coordinate ``(x, y, z)``.

        Number of the selected node nearest the `x`, `y`, `z` point.
        (In the active coordinate system, lowest number for coincident
        nodes.) A number higher than the highest node number indicates
        that the node is internal (generated by program).

        Parameters
        ----------
        x : float
            X-coordinate in the active coordinate system
        y : float
            Y-coordinate in the active coordinate system
        z : float
            Z-coordinate in the active coordinate system

        Returns
        -------
        int
            Node number

        Examples
        --------
        In this example we construct a solid cube and mesh it. Then we
        use ``queries.node`` to find the node closest to the centre of
        the cube. Using this we can extract the coordinates of this
        node and see how close to the centre the node is.

        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> mapdl.et(1, 'SOLID5')
        >>> mapdl.block(0, 10, 0, 10, 0, 10)
        >>> mapdl.esize(3)
        >>> mapdl.vmesh('ALL')
        >>> node_number = mapdl.queries.node(5., 5., 5.)
        >>> node_number
        112
        >>> x = mapdl.queries.nx(node_number)
        >>> y = mapdl.queries.ny(node_number)
        >>> z = mapdl.queries.nz(node_number)
        >>> (x, y, z)
        (5.0, 5.0, 5.0)
        """
        return self._run_query(f"NODE({x},{y},{z})", integer=True)

    def kp(self, x: float, y: float, z: float) -> int:
        """Return keypoint closest to coordinate ``(x, y, z)``.

        Number of the selected keypoint nearest the `x`, `y`, `z` point.

        In the active coordinate system, lowest number for coincident
        keypoints.

        Parameters
        ----------
        x : float
            X-coordinate in the active coordinate system
        y : float
            Y-coordinate in the active coordinate system
        z : float
            Z-coordinate in the active coordinate system

        Returns
        -------
        int
            Keypoint number

        Examples
        --------
        In this example we construct a simple triangle of keypoints in
        3D and then find the keypoint closest to the point (1, 1, 1).

        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> mapdl.k(1, 0, 1, 2)
        >>> mapdl.k(2, 1, 2, 0)
        >>> mapdl.k(3, 2, 0, 1)
        >>> mapdl.queries.kp(1., 1., 1.)
        1
        """
        return self._run_query(f"KP({x},{y},{z})", integer=True)


class _DisplacementComponentQueries(_QueryExecution):
    _mapdl = None

    def rotx(self, n: int) -> float:
        """Returns x-component of rotational displacement at a node.

        X-component of rotational displacement at node ``n``.

        Parameters
        ----------
        n : int
            Node number

        Returns
        -------
        float
            Rotational displacement of the node.

        Examples
        --------
        This example has been adapted from the example script
        :ref:`ref_rotational_displacement_example`. We create a square
        of shell material, apply a displacement perpendicular to the
        plane of the material, and then solve.

        Then we can use ``queries.rotx`` to get the x-component rotational
        displacement at the middle node on the deformed edge.

        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> mapdl.et(1, 'SHELL181')
        >>> mapdl.mp("EX", 1, 2e5)
        >>> mapdl.rectng(0, 1, 0, 1)
        >>> mapdl.sectype(1, "SHELL")
        >>> mapdl.secdata(0.1)
        >>> mapdl.esize(0.2)
        >>> mapdl.amesh("all")
        >>> mapdl.run('/SOLU')
        >>> mapdl.antype('STATIC')
        >>> mapdl.nsel("s", "loc", "x", 0)
        >>> mapdl.d("all", "all")
        >>> mapdl.nsel("s", "loc", "x", 1)
        >>> mapdl.d("all", "uz", -0.1)
        >>> mapdl.allsel("all")
        >>> mapdl.solve()
        >>> node = mapdl.queries.node(1, 0.5, 0)
        >>> mapdl.queries.rotx(node)
        -0.0002149851187
        """
        return self._run_query(f"ROTX({n})", integer=False)

    def roty(self, n: int) -> float:
        """Returns y-component of rotational displacement at a node.

        Y-component of rotational displacement at node ``n``.

        Parameters
        ----------
        n : int
            Node number

        Returns
        -------
        float
            Rotational displacement of the node.

        Examples
        --------
        This example has been adapted from the example script
        :ref:`ref_rotational_displacement_example`. We create a square
        of shell material, apply a displacement perpendicular to the
        plane of the material, and then solve.

        Then we can use ``queries.roty`` to get the y-component rotational
        displacement at the middle node on the deformed edge.

        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> mapdl.et(1, 'SHELL181')
        >>> mapdl.mp("EX", 1, 2e5)
        >>> mapdl.rectng(0, 1, 0, 1)
        >>> mapdl.sectype(1, "SHELL")
        >>> mapdl.secdata(0.1)
        >>> mapdl.esize(0.2)
        >>> mapdl.amesh("all")
        >>> mapdl.run('/SOLU')
        >>> mapdl.antype('STATIC')
        >>> mapdl.nsel("s", "loc", "x", 0)
        >>> mapdl.d("all", "all")
        >>> mapdl.nsel("s", "loc", "x", 1)
        >>> mapdl.d("all", "uz", -0.1)
        >>> mapdl.allsel("all")
        >>> mapdl.solve()
        >>> node = mapdl.queries.node(1, 0.5, 0)
        >>> mapdl.queries.roty(node)
        0.1489593933
        """
        return self._run_query(f"ROTY({n})", integer=False)

    def rotz(self, n: int) -> float:
        """Returns z-component of rotational displacement at a node.

        Z-component of rotational displacement at node ``n``.

        Parameters
        ----------
        n : int
            Node number

        Returns
        -------
        float
            Rotational displacement of the node.

        Examples
        --------
        This example has been adapted from the example script
        :ref:`ref_rotational_displacement_example`. We create a square
        of shell material, apply a displacement perpendicular to the
        plane of the material, and then solve.

        Then we can use ``queries.rotz`` to get the z-component rotational
        displacement at the middle node on the deformed edge.

        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> mapdl.et(1, 'SHELL181')
        >>> mapdl.mp("EX", 1, 2e5)
        >>> mapdl.rectng(0, 1, 0, 1)
        >>> mapdl.sectype(1, "SHELL")
        >>> mapdl.secdata(0.1)
        >>> mapdl.esize(0.2)
        >>> mapdl.amesh("all")
        >>> mapdl.run('/SOLU')
        >>> mapdl.antype('STATIC')
        >>> mapdl.nsel("s", "loc", "x", 0)
        >>> mapdl.d("all", "all")
        >>> mapdl.nsel("s", "loc", "x", 1)
        >>> mapdl.d("all", "uz", -0.1)
        >>> mapdl.allsel("all")
        >>> mapdl.solve()
        >>> node = mapdl.queries.node(1, 0.5, 0)
        >>> mapdl.queries.rotz(node)
        0.0
        """
        return self._run_query(f"ROTZ({n})", integer=False)

    def ux(self, n: int) -> float:
        """Returns x-component of structural displacement at a node.

        X-component of structural displacement at node ``n``.

        Parameters
        ----------
        n : int
            Node number

        Returns
        -------
        float
            Displacement of node

        Examples
        --------
        In this example we create a simple block of 6 cubic elements,
        fix one end in place, and then bend the other perpendicular to
        it. We can then examine the displacement of one of the nodes
        in the x-direction at the deformed end (node number 7).

        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> mapdl.et(1, 'SOLID5')
        >>> mapdl.block(0, 10, 0, 20, 0, 30)
        >>> mapdl.esize(10)
        >>> mapdl.vmesh('ALL')
        >>> mapdl.mp('EX', 1, 210E9)
        >>> mapdl.nsel('S', 'LOC', 'Z', 0)
        >>> mapdl.d('ALL', 'UX')
        >>> mapdl.d('ALL', 'UY')
        >>> mapdl.d('ALL', 'UZ')
        >>> mapdl.nsel('S', 'LOC', 'Z', 30)
        >>> mapdl.f('ALL', 'FY', 1000)
        >>> mapdl.run('/SOLU')
        >>> mapdl.antype('STATIC')
        >>> mapdl.solve()
        >>> mapdl.finish()
        >>> mapdl.queries.ux(7)
        1.549155634e-07

        """
        return self._run_query(f"UX({n})", integer=False)

    def uy(self, n: int) -> float:
        """Returns y-component of structural displacement at a node.

        Y-component of structural displacement at node ``n``.

        Parameters
        ----------
        n : int
            Node number

        Returns
        -------
        float
            Displacement of node

        Examples
        --------
        In this example we create a simple block of 6 cubic elements,
        fix one end in place, and then bend the other perpendicular to
        it. We can then examine the displacement of one of the nodes
        in the y-direction at the deformed end (node number 7).

        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> mapdl.et(1, 'SOLID5')
        >>> mapdl.block(0, 10, 0, 20, 0, 30)
        >>> mapdl.esize(10)
        >>> mapdl.vmesh('ALL')
        >>> mapdl.mp('EX', 1, 210E9)
        >>> mapdl.nsel('S', 'LOC', 'Z', 0)
        >>> mapdl.d('ALL', 'UX')
        >>> mapdl.d('ALL', 'UY')
        >>> mapdl.d('ALL', 'UZ')
        >>> mapdl.nsel('S', 'LOC', 'Z', 30)
        >>> mapdl.f('ALL', 'FY', 1000)
        >>> mapdl.run('/SOLU')
        >>> mapdl.antype('STATIC')
        >>> mapdl.solve()
        >>> mapdl.finish()
        >>> mapdl.queries.uy(7)
        5.803680779e-10

        """
        return self._run_query(f"UY({n})", integer=False)

    def uz(self, n: int) -> float:
        """Returns z-component of structural displacement at a node.

        Z-component of structural displacement at node ``n``.

        Parameters
        ----------
        n : int
            Node number

        Returns
        -------
        float
            Displacement of node

        Examples
        --------
        In this example we create a simple block of 6 cubic elements,
        fix one end in place, and then bend the other perpendicular to
        it. We can then examine the displacement of one of the nodes
        in the z-direction at the deformed end (node number 7).

        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> mapdl.et(1, 'SOLID5')
        >>> mapdl.block(0, 10, 0, 20, 0, 30)
        >>> mapdl.esize(10)
        >>> mapdl.vmesh('ALL')
        >>> mapdl.mp('EX', 1, 210E9)
        >>> mapdl.nsel('S', 'LOC', 'Z', 0)
        >>> mapdl.d('ALL', 'UX')
        >>> mapdl.d('ALL', 'UY')
        >>> mapdl.d('ALL', 'UZ')
        >>> mapdl.nsel('S', 'LOC', 'Z', 30)
        >>> mapdl.f('ALL', 'FY', 1000)
        >>> mapdl.run('/SOLU')
        >>> mapdl.antype('STATIC')
        >>> mapdl.solve()
        >>> mapdl.finish()
        >>> mapdl.queries.uz(7)
        3.74530389e-08

        """
        return self._run_query(f"UZ({n})", integer=False)
