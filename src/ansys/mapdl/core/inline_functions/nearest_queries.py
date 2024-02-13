# Copyright (C) 2024 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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
