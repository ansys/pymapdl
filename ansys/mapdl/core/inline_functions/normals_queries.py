from .core import _ParameterParsing


class _NodeNormalQueries(_ParameterParsing):
    _mapdl = None

    def normnx(self, n1: int, n2: int, n3: int) -> float:
        """X-direction cosine of the normal to the plane containing the given nodes.

        X-direction cosine of the normal to the plane containing nodes
        `n1`, `n2`, and `n3`, reported in the global Cartesian
        coordinate system.

        Parameters
        ----------
        n1 : int
            Node number

        n2 : int
            Node number

        n3 : int
            Node number

        Returns
        -------
        float
            X-direction cosine of the normal

        Examples
        --------
        Here we create three nodes in the y-z plane and interrogate the
        x-component of the normal to that plane, which is trivially 1.0.

        >>> from ansys.mapdl.core import launch_mapdl
        >>> from ansys.mapdl.core.inline_functions import Query
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> n1 = mapdl.n(1, 0, 0, 0)
        >>> n2 = mapdl.n(2, 0, 1, 0)
        >>> n3 = mapdl.n(3, 0, 1, 1)
        >>> q = Query(mapdl)
        >>> q.normnx(n1, n2, n3)
        1.0
        """
        response = self._mapdl.run(f'_=NORMNX({n1}, {n2}, {n3})')
        float_ = self._parse_parameter_float_response(response)
        return float_

    def normny(self, n1: int, n2: int, n3: int) -> float:
        """Y-direction cosine of the normal to the plane containing the given nodes.

        Y-direction cosine of the normal to the plane containing nodes
        `n1`, `n2`, and `n3`, reported in the global Cartesian
        coordinate system.

        Parameters
        ----------
        n1 : int
            Node number

        n2 : int
            Node number

        n3 : int
            Node number

        Returns
        -------
        float
            Y-direction cosine of the normal

        Examples
        --------
        Here we create three nodes in the x-z plane and interrogate the
        y-component of the normal to that plane, which is trivially 1.0.

        >>> from ansys.mapdl.core import launch_mapdl
        >>> from ansys.mapdl.core.inline_functions import Query
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> n1 = mapdl.n(1, 0, 0, 0)
        >>> n2 = mapdl.n(2, 1, 0, 0)
        >>> n3 = mapdl.n(3, 1, 0, 1)
        >>> q = Query(mapdl)
        >>> q.normny(n1, n2, n3)
        1.0
        """
        response = self._mapdl.run(f'_=NORMNY({n1}, {n2}, {n3})')
        float_ = self._parse_parameter_float_response(response)
        return float_

    def normnz(self, n1: int, n2: int, n3: int) -> float:
        """Z-direction cosine of the normal to the plane containing the given nodes.

        Z-direction cosine of the normal to the plane containing nodes
        `n1`, `n2`, and `n3`, reported in the global Cartesian
        coordinate system.

        Parameters
        ----------
        n1 : int
            Node number

        n2 : int
            Node number

        n3 : int
            Node number

        Returns
        -------
        float
            Z-direction cosine of the normal

        Examples
        --------
        Here we create three nodes in the x-y plane and interrogate the
        z-component of the normal to that plane, which is trivially 1.0.

        >>> from ansys.mapdl.core import launch_mapdl
        >>> from ansys.mapdl.core.inline_functions import Query
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> n1 = mapdl.n(1, 0, 0, 0)
        >>> n2 = mapdl.n(2, 0, 1, 0)
        >>> n3 = mapdl.n(3, 1, 1, 0)
        >>> q = Query(mapdl)
        >>> q.normnz(n1, n2, n3)
        1.0
        """
        response = self._mapdl.run(f'_=NORMNZ({n1}, {n2}, {n3})')
        float_ = self._parse_parameter_float_response(response)
        return float_


class _KeypointNormalQueries(_ParameterParsing):
    _mapdl = None

    def normkx(self, k1: int, k2: int, k3: int) -> float:
        """X-direction cosine of the normal to the plane containing the given keypoints.

        X-direction cosine of the normal to the plane containing
        keypoints `k1`, `k2`, and `k3`, reported in the global Cartesian
        coordinate system.

        Parameters
        ----------
        k1 : int
            Node number

        k2 : int
            Node number

        k3 : int
            Node number

        Returns
        -------
        float
            X-direction cosine of the normal

        Examples
        --------
        Here we create three keypoints in the y-z plane and interrogate
        the x-component of the normal to that plane, which is trivially
        1.0.

        >>> from ansys.mapdl.core import launch_mapdl
        >>> from ansys.mapdl.core.inline_functions import Query
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> k1 = mapdl.k(1, 0, 0, 0)
        >>> k2 = mapdl.k(2, 0, 1, 0)
        >>> k3 = mapdl.k(3, 0, 1, 1)
        >>> q = Query(mapdl)
        >>> q.normnx(k1, k2, k3)
        1.0
        """
        response = self._mapdl.run(f'_=NORMKX({k1}, {k2}, {k3})')
        float_ = self._parse_parameter_float_response(response)
        return float_

    def normky(self, k1: int, k2: int, k3: int) -> float:
        """Y-direction cosine of the normal to the plane containing the given keypoints.

        Y-direction cosine of the normal to the plane containing
        keypoints `k1`, `k2`, and `k3`, reported in the global Cartesian
        coordinate system.

        Parameters
        ----------
        k1 : int
            Node number

        k2 : int
            Node number

        k3 : int
            Node number

        Returns
        -------
        float
            Y-direction cosine of the normal

        Examples
        --------
        Here we create three keypoints in the x-z plane and interrogate
        the y-component of the normal to that plane, which is trivially
        1.0.

        >>> from ansys.mapdl.core import launch_mapdl
        >>> from ansys.mapdl.core.inline_functions import Query
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> k1 = mapdl.k(1, 0, 0, 0)
        >>> k2 = mapdl.k(2, 1, 0, 0)
        >>> k3 = mapdl.k(3, 1, 0, 1)
        >>> q = Query(mapdl)
        >>> q.normny(k1, k2, k3)
        1.0
        """
        response = self._mapdl.run(f'_=NORMKY({k1}, {k2}, {k3})')
        float_ = self._parse_parameter_float_response(response)
        return float_

    def normkz(self, k1: int, k2: int, k3: int) -> float:
        """Z-direction cosine of the normal to the plane containing the given keypoints.

        Z-direction cosine of the normal to the plane containing
        keypoints `k1`, `k2`, and `k3`, reported in the global Cartesian
        coordinate system.

        Parameters
        ----------
        k1 : int
            Node number

        k2 : int
            Node number

        k3 : int
            Node number

        Returns
        -------
        float
            Z-direction cosine of the normal

        Examples
        --------
        Here we create three keypoints in the x-y plane and interrogate
        the z-component of the normal to that plane, which is trivially
        1.0.

        >>> from ansys.mapdl.core import launch_mapdl
        >>> from ansys.mapdl.core.inline_functions import Query
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> k1 = mapdl.k(1, 0, 0, 0)
        >>> k2 = mapdl.k(2, 0, 1, 0)
        >>> k3 = mapdl.k(3, 1, 1, 0)
        >>> q = Query(mapdl)
        >>> q.normnz(k1, k2, k3)
        1.0
        """
        response = self._mapdl.run(f'_=NORMKZ({k1}, {k2}, {k3})')
        float_ = self._parse_parameter_float_response(response)
        return float_

