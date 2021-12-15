from .core import _QueryExecution


class _ScalarQueries(_QueryExecution):
    _mapdl = None

    def temp(self, n: int) -> float:
        """Returns temperature at node ``n``.

        Temperature at node ``n``.

        Parameters
        ----------
        n : int
            Node number

        Returns
        -------
        float
            Temperature

        Examples
        --------
        This example has been adapted from the example script
        :ref:`_ref_3d_plate_thermal`. We create a block
        of solid material, and apply a temperature to one end
        of the block, and then solve.

        Then we can use ``queries.temp`` to get the temperature
        at the first node on the deformed.

        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> mapdl.clear()
        >>> mapdl.prep7()
        >>> mapdl.mp("kxx", 1, 45)
        >>> mapdl.et(1, 'SOLID70')
        >>> mapdl.block(0, 1, 0, 1, 0, 1)
        >>> mapdl.esize(0.5)
        >>> mapdl.vmesh(1)
        >>> mapdl.d("all", "temp", 5)
        >>> mapdl.slashsolu()
        >>> mapdl.solve()
        >>> mapdl.queries.temp(1)
        5.0
        """
        return self._run_query(f"TEMP({n})", integer=False)

    def pres(self, n: int) -> float:
        """Returns pressure at node ``n``.

        Pressure at node ``n``.

        Parameters
        ----------
        n : int
            Node number

        Returns
        -------
        float
            Pressure
        """
        return self._run_query(f"PRES({n})", integer=False)

    def volt(self, n: int) -> float:
        """Returns electric potential at node ``n``.

        Electric potential at node ``n``.

        Parameters
        ----------
        n : int
            Node number

        Returns
        -------
        float
            Electric potential
        """
        return self._run_query(f"VOLT({n})", integer=False)

    def mag(self, n: int) -> float:
        """Returns magnetic scalar potential at node ``n``.

        Magnetic scalar potential at node ``n``.

        Parameters
        ----------
        n : int
            Node number

        Returns
        -------
        float
            Magnetic scalar potential
        """
        return self._run_query(f"VOLT({n})", integer=False)
