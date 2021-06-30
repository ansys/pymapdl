from typing import Optional


class _ParameterParsing:
    def _parse_parameter_integer_response(self, response) -> Optional[int]:
        return int(self._parse_parameter_float_response(response))

    @staticmethod
    def _parse_parameter_float_response(response) -> Optional[int]:
        parts = response.split('=')
        if len(parts) != 2:
            raise TypeError('Expression not provided; parameter response not recognised.')
        number = parts[1].strip()
        return float(number)


class ComponentQueries(_ParameterParsing):
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
        >>> from ansys.mapdl.core.inline_functions import Query
        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> n0 = mapdl.n(1, 0, 0, 0)
        >>> n1 = mapdl.n(2, 1, 2, 3)
        >>> mapdl.et(1, 'LINK11')
        >>> e0 = mapdl.e(n0, n1)
        >>> q = Query(mapdl)
        >>> print(q.centrx(e0))
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
        >>> from ansys.mapdl.core.inline_functions import Query
        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> n0 = mapdl.n(1, 0, 0, 0)
        >>> n1 = mapdl.n(2, 1, 2, 3)
        >>> mapdl.et(1, 'LINK11')
        >>> e0 = mapdl.e(n0, n1)
        >>> q = Query(mapdl)
        >>> print(q.centry(e0))
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
        >>> from ansys.mapdl.core.inline_functions import Query
        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> n0 = mapdl.n(1, 0, 0, 0)
        >>> n1 = mapdl.n(2, 1, 2, 3)
        >>> mapdl.et(1, 'LINK11')
        >>> e0 = mapdl.e(n0, n1)
        >>> q = Query(mapdl)
        >>> print(q.centrz(e0))
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


class Query(ComponentQueries):
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

    Examples
    --------
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
