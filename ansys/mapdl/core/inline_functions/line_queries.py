from .core import _ParameterParsing


class _LineFractionCoordinateQueries(_ParameterParsing):
    _mapdl = None

    def lx(self, n: int, lfrac: float) -> float:
        """X-coordinate of line ``n`` at length fraction ``lfrac``.

        Fetches X-coordinate of line ``n`` at ``lfrac`` times the line
        length along the line. ``0. <= lfrac <= 1.``.

        Parameters
        ----------
        n : int
            The line number of the line to be considered.

        lfrac: float
            The fraction of the length of the line along which to
            enquire. ``0. <= lfrac <= 1.``

        Returns
        -------
        float
            The X-coordinate.

        Examples
        --------
        Here we construct a line between the coordinates ``(0, 0, 0)``
        and ``(1, 2, 3)`` then find the X-coordinate halfway along the line.

        >>> from ansys.mapdl.core.inline_functions import Query
        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> k0 = mapdl.k(1, 0, 0, 0)
        >>> k1 = mapdl.k(2, 1, 2, 3)
        >>> l0 = mapdl.l(k0, k1)
        >>> q = Query(mapdl)
        >>> q.lx(l0, 0.5)
        0.5
        """
        response = self._mapdl.run(f'_=LX({n},{lfrac})')
        return self._parse_parameter_float_response(response)

    def ly(self, n: int, lfrac: float) -> float:
        """Y-coordinate of line ``n`` at length fraction ``lfrac``.

        Fetches Y-coordinate of line ``n`` at ``lfrac`` times the line
        length along the line. ``0. <= lfrac <= 1.``.

        Parameters
        ----------
        n : int
            The line number of the line to be considered.

        lfrac: float
            The fraction of the length of the line along which to
            enquire. ``0. <= lfrac <= 1.``

        Returns
        -------
        float
            The Y-coordinate.

        Examples
        --------
        Here we construct a line between the coordinates ``(0, 0, 0)``
        and ``(1, 2, 3)`` then find the Y-coordinate halfway along the line.

        >>> from ansys.mapdl.core.inline_functions import Query
        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> k0 = mapdl.k(1, 0, 0, 0)
        >>> k1 = mapdl.k(2, 1, 2, 3)
        >>> l0 = mapdl.l(k0, k1)
        >>> q = Query(mapdl)
        >>> q.ly(l0, 0.5)
        1.0
        """
        response = self._mapdl.run(f'_=LY({n},{lfrac})')
        return self._parse_parameter_float_response(response)

    def lz(self, n: int, lfrac: float) -> float:
        """Z-coordinate of line ``n`` at length fraction ``lfrac``.

        Fetches Z-coordinate of line ``n`` at ``lfrac`` times the line
        length along the line. ``0. <= lfrac <= 1.``.

        Parameters
        ----------
        n : int
            The line number of the line to be considered.

        lfrac: float
            The fraction of the length of the line along which to
            enquire. ``0. <= lfrac <= 1.``

        Returns
        -------
        float
            The Z-coordinate.

        Examples
        --------
        Here we construct a line between the coordinates ``(0, 0, 0)``
        and ``(1, 2, 3)`` then find the Z-coordinate halfway along the line.

        >>> from ansys.mapdl.core.inline_functions import Query
        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> k0 = mapdl.k(1, 0, 0, 0)
        >>> k1 = mapdl.k(2, 1, 2, 3)
        >>> l0 = mapdl.l(k0, k1)
        >>> q = Query(mapdl)
        >>> q.lz(l0, 0.5)
        1.5
        """
        response = self._mapdl.run(f'_=LZ({n},{lfrac})')
        return self._parse_parameter_float_response(response)


class _LineFractionSlopeQueries(_ParameterParsing):
    _mapdl = None

    def lsx(self, n: int, lfrac: float) -> float:
        """X-slope of line ``n`` at length fraction ``lfrac``.

        Fetches X-slope of line ``n`` at ``lfrac`` times the line
        length along the line. ``0. <= lfrac <= 1.``.
        This is equivalent to the rate of change of the x-coordinate
        with respect to the change of line length.

        Parameters
        ----------
        n : int
            The line number of the line to be considered.
        lfrac: float
            The fraction of the length of the line along which to
            enquire. ``0. <= lfrac <= 1.``

        Returns
        -------
        float
            The X-slope.

        Examples
        --------
        Here we construct a line between the coordinates ``(0, 0, 0)``
        and ``(1, 2, 2)`` then find the X-slope halfway along the line.

        >>> from ansys.mapdl.core.inline_functions import Query
        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> k0 = mapdl.k(1, 0, 0, 0)
        >>> k1 = mapdl.k(2, 1, 2, 2)
        >>> l0 = mapdl.l(k0, k1)
        >>> q = Query(mapdl)
        >>> q.lsx(l0, 0.5)
        0.3333333333
        """
        response = self._mapdl.run(f'_=LSX({n},{lfrac})')
        return self._parse_parameter_float_response(response)

    def lsy(self, n: int, lfrac: float) -> float:
        """Y-slope of line ``n`` at length fraction ``lfrac``.

        Fetches Y-slope of line ``n`` at ``lfrac`` times the line
        length along the line. ``0. <= lfrac <= 1.``.
        This is equivalent to the rate of change of the y-coordinate
        with respect to the change of line length.

        Parameters
        ----------
        n : int
            The line number of the line to be considered.
        lfrac: float
            The fraction of the length of the line along which to
            enquire. ``0. <= lfrac <= 1.``

        Returns
        -------
        float
            The Y-slope.

        Examples
        --------
        Here we construct a line between the coordinates ``(0, 0, 0)``
        and ``(1, 2, 2)`` then find the Y-slope halfway along the line.

        >>> from ansys.mapdl.core.inline_functions import Query
        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> k0 = mapdl.k(1, 0, 0, 0)
        >>> k1 = mapdl.k(2, 1, 2, 2)
        >>> l0 = mapdl.l(k0, k1)
        >>> q = Query(mapdl)
        >>> q.lsy(l0, 0.5)
        0.6666666667
        """
        response = self._mapdl.run(f'_=LSY({n},{lfrac})')
        return self._parse_parameter_float_response(response)

    def lsz(self, n: int, lfrac: float) -> float:
        """Z-slope of line ``n`` at length fraction ``lfrac``.

        Fetches Z-slope of line ``n`` at ``lfrac`` times the line
        length along the line. ``0. <= lfrac <= 1.``.
        This is equivalent to the rate of change of the z-coordinate
        with respect to the change of line length.

        Parameters
        ----------
        n : int
            The line number of the line to be considered.
        lfrac: float
            The fraction of the length of the line along which to
            enquire. ``0. <= lfrac <= 1.``

        Returns
        -------
        float
            The Z-slope.

        Examples
        --------
        Here we construct a line between the coordinates ``(0, 0, 0)``
        and ``(1, 2, 2)`` then find the Z-slope halfway along the line.

        >>> from ansys.mapdl.core.inline_functions import Query
        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> k0 = mapdl.k(1, 0, 0, 0)
        >>> k1 = mapdl.k(2, 1, 2, 2)
        >>> l0 = mapdl.l(k0, k1)
        >>> q = Query(mapdl)
        >>> q.lsz(l0, 0.5)
        0.6666666667
        """
        response = self._mapdl.run(f'_=LSZ({n},{lfrac})')
        return self._parse_parameter_float_response(response)