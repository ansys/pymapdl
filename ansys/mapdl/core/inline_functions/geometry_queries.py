from .core import _QueryExecution


class _AngleQueries(_QueryExecution):
    _mapdl = None

    def anglen(self, n1, n2, n3) -> float:
        """Return the angle between 3 nodes where ``n1`` is the vertex.

        Subtended angle between two lines (defined by three
        nodes where ``n1`` is the vertex node).
        Default is in radians.

        Parameters
        ----------
        n1 : int
            The vertex node
        n2 : int
            Node
        n3 : int
            Node

        Returns
        -------
        float
            The angle in radians (default)

        Examples
        --------
        Here we construct a simple right angle of 3 nodes
        and query the angle. Finish by converting it to degrees.

        >>> from ansys.mapdl.core import launch_mapdl
        >>> from math import pi
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> mapdl.et(1, 'SOLID5')
        >>> n1 = mapdl.n(1, 0, 0, 0)
        >>> n2 = mapdl.n(2, 1, 0, 0)
        >>> n3 = mapdl.n(3, 0, 1, 0)
        >>> angle = mapdl.queries.anglen(n1, n2, n3)
        >>> angle*180./pi
        90.0
        """
        return self._run_query(f"ANGLEN({n1},{n2},{n3})", integer=False)

    def anglek(self, k1, k2, k3) -> float:
        """Return the angle between 3 keypoints where ``k1`` is the vertex.

        Subtended angle between two lines (defined by three
        keypoints where ``k1`` is the vertex node).
        Default is in radians.

        Parameters
        ----------
        k1 : int
            The vertex node
        k2 : int
            Node
        k3 : int
            Node

        Returns
        -------
        float
            The angle in radians (default)

        Examples
        --------
        Here we construct a simple 45 degree angle of 3
        keypoints and query the angle. Finish by converting it
        to degrees.

        >>> from ansys.mapdl.core import launch_mapdl
        >>> from math import pi
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> mapdl.et(1, 'SOLID5')
        >>> k1 = mapdl.k(1, 0, 0, 0)
        >>> k2 = mapdl.k(2, 1, 0, 0)
        >>> k3 = mapdl.k(3, 1, 1, 0)
        >>> angle = mapdl.queries.anglek(k1, k2, k3)
        >>> angle*180./pi
        45.0
        """
        return self._run_query(f"ANGLEK({k1},{k2},{k3})", integer=False)


class _AreaQueries(_QueryExecution):
    _mapdl = None

    def areand(self, n1, n2, n3) -> float:
        """Area of the triangle with vertices at nodes ``n1``, ``n2``, and ``n3``.

        Parameters
        ----------
        n1 : int
            First node
        n2 : int
            Second node
        n3 : int
            Third node

        Returns
        -------
        float
            The area of the triangle.

        Examples
        --------
        Here we construct a simple right-angle triangle and query the area.

        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> n1 = mapdl.n(1, 0, 0, 0)
        >>> n2 = mapdl.n(2, 1, 0, 0)
        >>> n3 = mapdl.n(3, 0, 1, 0)
        >>> area = mapdl.queries.areand(n1, n2, n3)
        0.5
        """
        return self._run_query(f"AREAND({n1},{n2},{n3})", integer=False)

    def areakp(self, k1, k2, k3) -> float:
        """Area of the triangle with vertices at keypoints ``k1``, ``k2``, and ``k3``.

        Parameters
        ----------
        k1 : int
            First keypoint
        k2 : int
            Second keypoint
        k3 : int
            Third keypoint

        Returns
        -------
        float
            The area of the triangle.

        Examples
        --------
        Here we construct a simple triangle in 3D and query the area.

        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> k1 = mapdl.k(1, 0, 0, 0)
        >>> k2 = mapdl.k(2, 0.6, 0, 0.6)
        >>> k3 = mapdl.k(3, 0, 0.6, 0)
        >>> mapdl.queries.areakp(k1, k2, k3)
        0.2545584412
        """
        return self._run_query(f"AREAKP({k1},{k2},{k3})", integer=False)


class _DistanceQueries(_QueryExecution):
    _mapdl = None

    def distnd(self, n1, n2) -> float:
        """Compute the distance between nodes ``n1`` and ``n2``.

        Parameters
        ----------
        n1 : int
            First node.
        n2 : int
            Second node.

        Returns
        -------
        float
            Distance between the nodes.

        Examples
        --------
        Here we construct two nodes and return the distance between them.

        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> n1 = mapdl.n(1, 1, 0, 0)
        >>> n2 = mapdl.n(2, 0, 0, 0)
        >>> mapdl.queries.distnd(n1, n2)
        1.0
        """
        return self._run_query(f"DISTND({n1},{n2})", integer=False)

    def distkp(self, k1, k2) -> float:
        """Compute the distance between keypoints ``k1`` and ``k2``.

        Parameters
        ----------
        k1 : int
            First keypoint.
        k2 : int
            Second keypoint.

        Returns
        -------
        float
            Distance between the keypoints.

        Examples
        --------
        Here we construct two keypoints and query for the distance between them.
        It should be equal to the square root of 2.

        >>> from ansys.mapdl.core import launch_mapdl
        >>> from math import sqrt
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> n1 = mapdl.n(1, 1, 0, 0)
        >>> n2 = mapdl.n(2, 0, 1, 0)
        >>> mapdl.queries.distnd(n1, n2)
        1.414213562
        >>> sqrt(2)
        1.4142135623730951
        """
        return self._run_query(f"DISTKP({k1},{k2})", integer=False)
