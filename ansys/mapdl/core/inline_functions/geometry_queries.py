from .core import _ParameterParsing


class _AngleQueries(_ParameterParsing):
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
        Here we consrtruct a simple right angle of 3 nodes
        and query the angle. Converting it to degrees after
        the fact.

        >>> from ansys.mapdl.core import launch_mapdl
        >>> from ansys.mapdl.core.inline_functions import Query
        >>> from math import pi
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> mapdl.et(1, 'SOLID5')
        >>> n1 = mapdl.n(1, 0, 0, 0)
        >>> n2 = mapdl.n(2, 1, 0, 0)
        >>> n3 = mapdl.n(3, 0, 1, 0)
        >>> q = Query(mapdl)
        >>> angle = q.anglen(n1, n2, n3)
        >>> angle*180./pi
        90.00000001175157
        """
        response = self._mapdl.run(f'_=ANGLEN({n1},{n2},{n3})')
        return self._parse_parameter_float_response(response)

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
        Here we consrtruct a simple 45 degree angle of 3
        keypoints and query the angle. Converting it
        to degrees after the fact.

        >>> from ansys.mapdl.core import launch_mapdl
        >>> from ansys.mapdl.core.inline_functions import Query
        >>> from math import pi
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> mapdl.et(1, 'SOLID5')
        >>> k1 = mapdl.k(1, 0, 0, 0)
        >>> k2 = mapdl.k(2, 1, 0, 0)
        >>> k3 = mapdl.k(3, 1, 1, 0)
        >>> q = Query(mapdl)
        >>> angle = q.anglek(k1, k2, k3)
        >>> angle*180./pi
        45.00000000014621
        """
        response = self._mapdl.run(f'_=ANGLEK({k1},{k2},{k3})')
        return self._parse_parameter_float_response(response)


class _AreaQueries(_ParameterParsing):
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
            The area of the triangle

        Examples
        --------
        Here we consrtruct a simple right-angled triangle and query the area.

        >>> from ansys.mapdl.core import launch_mapdl
        >>> from ansys.mapdl.core.inline_functions import Query
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> n1 = mapdl.n(1, 0, 0, 0)
        >>> n2 = mapdl.n(2, 1, 0, 0)
        >>> n3 = mapdl.n(3, 0, 1, 0)
        >>> q = Query(mapdl)
        >>> area = q.areand(n1, n2, n3)
        0.5
        """
        response = self._mapdl.run(f'_=AREAND({n1},{n2},{n3})')
        return self._parse_parameter_float_response(response)

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
            The area of the triangle

        Examples
        --------
        Here we consrtruct a simple triangle in 3D and query the area.

        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> k1 = mapdl.k(1, 0, 0, 0)
        >>> k2 = mapdl.k(2, .6, 0, 0.6)
        >>> k3 = mapdl.k(3, 0, 0.6, 0)
        >>> mapdl.queries.areakp(k1, k2, k3)
        0.2545584412
        """
        response = self._mapdl.run(f'_=AREAKP({k1},{k2},{k3})')
        return self._parse_parameter_float_response(response)
