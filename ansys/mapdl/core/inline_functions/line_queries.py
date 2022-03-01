from .core import _QueryExecution


class _LineFractionCoordinateQueries(_QueryExecution):
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

        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> k0 = mapdl.k(1, 0, 0, 0)
        >>> k1 = mapdl.k(2, 1, 2, 3)
        >>> l0 = mapdl.l(k0, k1)
        >>> q = mapdl.queries
        >>> q.lx(l0, 0.5)
        0.5
        """
        return self._run_query(f"LX({n}, {lfrac})", integer=False)

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

        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> k0 = mapdl.k(1, 0, 0, 0)
        >>> k1 = mapdl.k(2, 1, 2, 3)
        >>> l0 = mapdl.l(k0, k1)
        >>> q = mapdl.queries
        >>> q.ly(l0, 0.5)
        1.0
        """
        return self._run_query(f"LY({n}, {lfrac})", integer=False)

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

        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> k0 = mapdl.k(1, 0, 0, 0)
        >>> k1 = mapdl.k(2, 1, 2, 3)
        >>> l0 = mapdl.l(k0, k1)
        >>> q = mapdl.queries
        >>> q.lz(l0, 0.5)
        1.5
        """
        return self._run_query(f"LZ({n}, {lfrac})", integer=False)


class _LineFractionSlopeQueries(_QueryExecution):
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

        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> k0 = mapdl.k(1, 0, 0, 0)
        >>> k1 = mapdl.k(2, 1, 2, 2)
        >>> l0 = mapdl.l(k0, k1)
        >>> q = mapdl.queries
        >>> q.lsx(l0, 0.5)
        0.3333333333
        """
        return self._run_query(f"LSX({n}, {lfrac})", integer=False)

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

        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> k0 = mapdl.k(1, 0, 0, 0)
        >>> k1 = mapdl.k(2, 1, 2, 2)
        >>> l0 = mapdl.l(k0, k1)
        >>> q = mapdl.queries
        >>> q.lsy(l0, 0.5)
        0.6666666667
        """
        return self._run_query(f"LSY({n}, {lfrac})", integer=False)

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

        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> k0 = mapdl.k(1, 0, 0, 0)
        >>> k1 = mapdl.k(2, 1, 2, 2)
        >>> l0 = mapdl.l(k0, k1)
        >>> q = mapdl.queries
        >>> q.lsz(l0, 0.5)
        0.6666666667
        """
        return self._run_query(f"LSZ({n}, {lfrac})", integer=False)
