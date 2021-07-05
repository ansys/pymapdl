

class _ParameterParsing:
    def _parse_parameter_integer_response(self, response) -> int:
        return int(self._parse_parameter_float_response(response))

    @staticmethod
    def _parse_parameter_float_response(response) -> float:
        parts = response.split('=')
        if len(parts) != 2:
            raise TypeError('Expression not provided; parameter response not recognised.')
        number = parts[1].strip()
        return float(number)


class _ComponentQueries(_ParameterParsing):
    _mapdl = None

    def centrx(self, e: int) -> float:
        """
        Fetches centroid X-coordinate of element ``e`` in global
        Cartesian coordinate system. Centroid is determined from the
        selected nodes on the element.

        Parameters
        ----------
        e : int
            The element number of the element to be considered.

        Returns
        -------
        number : float
            The centroid coordinate.

        Examples
        --------
        Here we construct a line between the coordinates (0, 0, 0) and
        (1, 2, 3) then find the centroid x-coordinate of this element.

        >>> from ansys.mapdl.core.inline_functions import Query
        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> n0 = mapdl.n(1, 0, 0, 0)
        >>> n1 = mapdl.n(2, 1, 2, 3)
        >>> mapdl.et(1, 'LINK11')
        >>> e0 = mapdl.e(n0, n1)
        >>> q = Query(mapdl)
        >>> q.centrx(e0)
        0.5
        """
        response = self._mapdl.run(f'_=CENTRX({e})')
        return self._parse_parameter_float_response(response)

    def centry(self, e: int) -> float:
        """
        Fetches centroid Y-coordinate of element ``e`` in global
        Cartesian coordinate system. Centroid is determined from the
        selected nodes on the element.

        Parameters
        ----------
        e : int
            The element number of the element to be considered.

        Returns
        -------
        number : float
            The centroid coordinate.

        Examples
        --------
        Here we construct a line between the coordinates (0, 0, 0) and
        (1, 2, 3) then find the centroid y-coordinate of this element.

        >>> from ansys.mapdl.core.inline_functions import Query
        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> n0 = mapdl.n(1, 0, 0, 0)
        >>> n1 = mapdl.n(2, 1, 2, 3)
        >>> mapdl.et(1, 'LINK11')
        >>> e0 = mapdl.e(n0, n1)
        >>> q = Query(mapdl)
        >>> q.centry(e0)
        1.0
        """
        response = self._mapdl.run(f'_=CENTRY({e})')
        return self._parse_parameter_float_response(response)

    def centrz(self, e: int) -> float:
        """
        Fetches centroid Z-coordinate of element ``e`` in global
        Cartesian coordinate system. Centroid is determined from the
        selected nodes on the element.

        Parameters
        ----------
        e : int
            The element number of the element to be considered.

        Returns
        -------
        number : float
            The centroid coordinate.

        Examples
        --------
        Here we construct a line between the coordinates (0, 0, 0) and
        (1, 2, 3) then find the centroid z-coordinate of this element.

        >>> from ansys.mapdl.core.inline_functions import Query
        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> n0 = mapdl.n(1, 0, 0, 0)
        >>> n1 = mapdl.n(2, 1, 2, 3)
        >>> mapdl.et(1, 'LINK11')
        >>> e0 = mapdl.e(n0, n1)
        >>> q = Query(mapdl)
        >>> q.centrz(e0)
        1.5
        """
        response = self._mapdl.run(f'_=CENTRZ({e})')
        return self._parse_parameter_float_response(response)

    def nx(self, n: int) -> float:
        """
        Fetches X-coordinate of node ``n`` in the active coordinate
        system.

        Parameters
        ----------
        n : int
            Node number

        Returns
        -------
        number: float
             Coordinate of node

        Examples
        --------
        Here we construct a simple box and mesh it with elements. Then
        we use the ``Query`` class, and the ``nx`` method to find the
        x-coordinate of the 10th node.

        >>> from ansys.mapdl.core import launch_mapdl
        >>> from ansys.mapdl.core.inline_functions import Query
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> mapdl.et(1, 'SOLID5')
        >>> mapdl.block(0, 10, 0, 20, 0, 30)
        >>> mapdl.esize(2)
        >>> mapdl.vmesh('ALL')
        >>> q = Query(mapdl)
        >>> q.nx(10)
        0.0
        """
        response = self._mapdl.run(f'_=NX({n})')
        return self._parse_parameter_float_response(response)

    def ny(self, n: int) -> float:
        """
        Fetches Y-coordinate of node ``n`` in the active coordinate
        system.

        Parameters
        ----------
        n : int
            Node number

        Returns
        -------
        number: float
             Coordinate of node

        Examples
        --------
        Here we construct a simple box and mesh it with elements. Then
        we use the ``Query`` class, and the ``ny`` method to find the
        y-coordinate of the 10th node.

        >>> from ansys.mapdl.core import launch_mapdl
        >>> from ansys.mapdl.core.inline_functions import Query
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> mapdl.et(1, 'SOLID5')
        >>> mapdl.block(0, 10, 0, 20, 0, 30)
        >>> mapdl.esize(2)
        >>> mapdl.vmesh('ALL')
        >>> q = Query(mapdl)
        >>> q.ny(10)
        4.0
        """
        response = self._mapdl.run(f'_=NY({n})')
        return self._parse_parameter_float_response(response)

    def nz(self, n: int) -> float:
        """
        Fetches Z-coordinate of node ``n`` in the active coordinate
        system.

        Parameters
        ----------
        n : int
            Node number

        Returns
        -------
        number: float
             Coordinate of node

        Examples
        --------
        Here we construct a simple box and mesh it with elements. Then
        we use the ``Query`` class, and the ``nz`` method to find the
        z-coordinate of the 10th node.

        >>> from ansys.mapdl.core import launch_mapdl
        >>> from ansys.mapdl.core.inline_functions import Query
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> mapdl.et(1, 'SOLID5')
        >>> mapdl.block(0, 10, 0, 20, 0, 30)
        >>> mapdl.esize(2)
        >>> mapdl.vmesh('ALL')
        >>> q = Query(mapdl)
        >>> q.nz(10)
        0.0
        """
        response = self._mapdl.run(f'_=NZ({n})')
        return self._parse_parameter_float_response(response)

    def kx(self, k: int) -> float:
        """
        X-coordinate of keypoint ``k`` in the active coordinate system.

        Parameters
        ----------
        k : int
            Keypoint number to be considered.

        Returns
        -------
        number : float
            Coordinate of the keypoint.

        Examples
        --------
        Here we add a single keypoint, then use ``kx`` to extract the
        x-coordinate of it.

        >>> from ansys.mapdl.core import launch_mapdl
        >>> from ansys.mapdl.core.inline_functions import Query
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> mapdl.k(1, 0, 1, 2)
        >>> q = Query(mapdl)
        >>> q.kx(1)
        0.0
        """
        response = self._mapdl.run(f'_=KX({k})')
        return self._parse_parameter_float_response(response)

    def ky(self, k: int) -> float:
        """
        Y-coordinate of keypoint ``k`` in the active coordinate system.

        Parameters
        ----------
        k : int
            Keypoint number to be considered.

        Returns
        -------
        number : float
            Coordinate of the keypoint.

        Examples
        --------
        Here we add a single keypoint, then use ``ky`` to extract the
        y-coordinate of it.

        >>> from ansys.mapdl.core import launch_mapdl
        >>> from ansys.mapdl.core.inline_functions import Query
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> mapdl.k(1, 0, 1, 2)
        >>> q = Query(mapdl)
        >>> q.ky(1)
        1.0
        """
        response = self._mapdl.run(f'_=KY({k})')
        return self._parse_parameter_float_response(response)

    def kz(self, k: int) -> float:
        """
        Z-coordinate of keypoint ``k`` in the active coordinate system.

        Parameters
        ----------
        k : int
            Keypoint number to be considered.

        Returns
        -------
        number : float
            Coordinate of the keypoint.

        Examples
        --------
        Here we add a single keypoint, then use ``kz`` to extract the
        z-coordinate of it.

        >>> from ansys.mapdl.core import launch_mapdl
        >>> from ansys.mapdl.core.inline_functions import Query
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> mapdl.k(1, 0, 1, 2)
        >>> q = Query(mapdl)
        >>> q.kz(1)
        2.0
        """
        response = self._mapdl.run(f'_=KZ({k})')
        return self._parse_parameter_float_response(response)


class _InverseGetComponentQueries(_ParameterParsing):
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
        use ``Query.node`` to find the node closest to the centre of the
        cube. Using this we can extract the coordinates of this node and
        see how close to the centre the node is.

        >>> from ansys.mapdl.core import launch_mapdl
        >>> from ansys.mapdl.core.inline_functions import Query
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> mapdl.et(1, 'SOLID5')
        >>> mapdl.block(0, 10, 0, 10, 0, 10)
        >>> mapdl.esize(3)
        >>> mapdl.vmesh('ALL')
        >>> q = Query(mapdl)
        >>> node_number = q.node(5., 5., 5.)
        >>> node_number
        112
        >>> q.nx(node_number), q.ny(node_number), q.nz(node_number)
        5.0, 5.0, 5.0
        """
        response = self._mapdl.run(f'_=NODE({x},{y},{z})')
        return self._parse_parameter_integer_response(response)

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
        >>> from ansys.mapdl.core.inline_functions import Query
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> mapdl.k(1, 0, 1, 2)
        >>> mapdl.k(2, 1, 2, 0)
        >>> mapdl.k(3, 2, 0, 1)
        >>> q = Query(mapdl)
        >>> q.kp(1., 1., 1.)
        1
        """
        response = self._mapdl.run(f'_=KP({x},{y},{z})')
        return self._parse_parameter_integer_response(response)


class Query(_ComponentQueries, _InverseGetComponentQueries):
    """Class containing all the inline functions of APDL.

    Most of the results of these methods are shortcuts for specific
    combinations of arguments supplied to `mapdl.get(...)` and the
    same results can be achieved just using `mapdl.get()`.

    Currently implemented functions:

    - `centrx(e)` - get the centroid x-coordinate of element `e`
    - `centry(e)` - get the centroid y-coordinate of element `e`
    - `centrz(e)` - get the centroid z-coordinate of element `e`
    - `nx(n)` - get the x-coordinate of node `n`
    - `ny(n)` - get the y-coordinate of node `n`
    - `nz(n)` - get the z-coordinate of node `n`
    - `kx(k)` - get the x-coordinate of keypoint `k`
    - `ky(k)` - get the y-coordinate of keypoint `k`
    - `kz(k)` - get the z-coordinate of keypoint `k`
    - `node(x, y, z)` - get the node closest to coordinate (x, y, z)
    - `kp(x, y, z)` - get the keypoint closest to coordinate (x, y, z)

    Examples
    --------
    In this example we construct a solid box and mesh it. Then we use
    the ``Query`` methods ``nx``, ``ny``, and ``nz`` to find the
    cartesian coordinates of the first node.

    >>> from ansys.mapdl.core import launch_mapdl
    >>> from ansys.mapdl.core.inline_functions import Query
    >>> mapdl = launch_mapdl()
    >>> mapdl.prep7()
    >>> mapdl.et(1, 'SOLID5')
    >>> mapdl.block(0, 10, 0, 20, 0, 30)
    >>> mapdl.esize(2)
    >>> mapdl.vmesh('ALL')
    >>> q = Query(mapdl)
    >>> q.nx(1), q.ny(1), q.nz(1)
    0.0 20.0 0.0
    """
    def __init__(self, mapdl):
        self._mapdl = mapdl
