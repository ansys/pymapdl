from .core import _QueryExecution


class _EntityNearestEntityQueries(_QueryExecution):
    _mapdl = None

    def nnear(self, n: int) -> int:
        """Returns the selected node nearest node `n`.

        Parameters
        ----------
        n : int
            Node number

        Returns
        -------
        int
            Node number

        Examples
        --------
        In this example we construct a solid box and mesh it. Then we
        use the ``Query`` method ``node`` to find the node closest to
        the centre of the block and finally use ``nnear`` to find the
        node nearest to that.

        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> mapdl.et(1, 'SOLID5')
        >>> mapdl.block(0, 10, 0, 10, 0, 10)
        >>> mapdl.esize(3)
        >>> mapdl.vmesh('ALL')
        >>> q = mapdl.queries
        >>> node_number = q.node(5., 5., 5.)
        >>> nearest_node = q.nnear(node_number)
        >>> node_number, nearest_node
        (112, 103)
        """
        return self._run_query(f"NNEAR({n})", integer=True)

    def knear(self, k: int) -> int:
        """Returns the selected keypoint nearest keypoint `k`.

        Parameters
        ----------
        k : int
            Keypoint number

        Returns
        -------
        int
            Keypoint number

        Examples
        --------
        In this example we construct two keypoints and then verify that
        the nearest keypoint to one is the other.

        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> k1 = mapdl.k(1, 0, 0, 0)
        >>> k2 = mapdl.k(2, 1, 1, 1)
        >>> q = mapdl.queries
        >>> q.knear(k1)
        1

        >>> q.knear(k1) == k2
        True
        """
        return self._run_query(f"KNEAR({k})", integer=True)

    def enearn(self, n: int) -> int:
        """Returns the selected element nearest node `n`.

        The element position is calculated from the selected nodes.

        Parameters
        ----------
        n : int
            Node number

        Returns
        -------
        int
            Element number

        Examples
        --------
        In this example we construct a solid box and mesh it. Then we
        use the ``Query`` method ``node`` to find the node closest to
        the centre of the block and finally use ``enearn`` to find the
        element nearest to that node.

        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> mapdl.et(1, 'SOLID5')
        >>> mapdl.block(0, 10, 0, 10, 0, 10)
        >>> mapdl.esize(3)
        >>> mapdl.vmesh('ALL')
        >>> q = mapdl.queries
        >>> node_number = q.node(5., 5., 5.)
        >>> nearest_element = q.enearn(node_number)
        >>> node_number, nearest_element
        (112, 22)
        """
        return self._run_query(f"ENEARN({n})", integer=True)
