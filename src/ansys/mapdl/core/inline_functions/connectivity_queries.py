# Copyright (C) 2016 - 2024 ANSYS, Inc. and/or its affiliates.
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


class _ConnectivityQueries(_QueryExecution):
    _mapdl = None

    def nelem(self, e, npos) -> int:
        """Return the number of the node at position ``npos`` in element ``e``.

        Returns the node number in position `npos` for element number ``e``.
        ``npos`` can be 1, 2, 3, ..., 20.

        Parameters
        ----------
        e : int
            The element number of the element to be considered.
        npos : int
            The node position within the element. Can be 1-20.

        Returns
        -------
        int
            The node number.

        Examples
        --------
        Here we construct a simple block 10 x 10 x 10, mesh it and
        use `nelem` to query the nodes in each position (1-20) within
        element 1.

        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> mapdl.et(1, 'SOLID5')
        >>> mapdl.block(0, 10, 0, 10, 0, 10)
        >>> mapdl.esize(3)
        >>> mapdl.vmesh('ALL')
        >>> q = mapdl.queries
        >>> positions = [q.nelem(1, i) for i in range(1, 21)]
        >>> positions
        [2, 14, 17, 5, 53, 63, 99, 83, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        """
        return self._run_query(f"NELEM({e},{npos})", integer=True)

    def enextn(self, n, loc) -> int:
        """Returns the ``loc`` element connected to node ``n``.

        Returns the element connected to node ``n``. ``loc`` is the position
        in the resulting list when many elements share the node.
        A zero is returned at the end of the list.

        Parameters
        ----------
        n : int
            Node number.
        loc : int
             The position in the resulting list when many elements share the node.

        Returns
        -------
        int
            The element number

        Examples
        --------
        Here we construct a simple block 10 x 10 x 10, mesh it and
        use `enextn` to find the first and second elements
        connected to node 5.

        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> mapdl.et(1, 'SOLID5')
        >>> mapdl.block(0, 10, 0, 10, 0, 10)
        >>> mapdl.esize(1)
        >>> mapdl.vmesh('ALL')
        >>> q = mapdl.queries
        >>> elements = [q.enextn(5, 1), q.enextn(5, 2)]
        >>> elements
        [61, 71]
        """
        return self._run_query(f"ENEXTN({n},{loc})", integer=True)
