from .core import SelectionStatus, _QueryExecution


class _SelectionStatusQueries(_QueryExecution):
    _mapdl = None

    def nsel(self, n: int) -> SelectionStatus:
        """Returns selection status of a node.

        Returns a ``SelectionStatus`` object with values:

        1  - SELECTED
        0  - UNDEFINED
        -1 - UNSELECTED

        Parameters
        ----------
        n : int
            Node number

        Returns
        -------
        mapdl.ansys.core.inline_functions.SelectionStatus
            Status of node

        Examples
        --------
        Here we create a single node and interrogate its selection
        status.

        >>> from ansys.mapdl.core import launch_mapdl
        >>> from ansys.mapdl.core.inline_functions import Query
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> n1 = mapdl.n(1, 0, 0, 0)
        >>> n1
        1

        We can use ``Query.nsel`` to interrogate the selection status
        of the node. The response is an ``enum.IntEnum`` object. If
        you query a node that does not exist, it will return a status
        ``SelectionStatus.UNDEFINED``.

        >>> q = Query(mapdl)
        >>> q.nsel(n1)
        <SelectionStatus.SELECTED: 1>
        >>> mapdl.nsel('NONE')
        >>> q.nsel(n1)
        <SelectionStatus.UNSELECTED: -1>
        >>> q.nsel(0)
        <SelectionStatus.UNDEFINED: 0>
        """
        return SelectionStatus(self._run_query(f"NSEL({n})", integer=True))

    def ksel(self, k: int) -> SelectionStatus:
        """Returns selection status of a keypoint.

        Returns a ``SelectionStatus`` object with values:

        1  - SELECTED
        0  - UNDEFINED
        -1 - UNSELECTED

        Parameters
        ----------
        k : int
            Keypoint number

        Returns
        -------
        mapdl.ansys.core.inline_functions.SelectionStatus
            Status of keypoint

        Examples
        --------
        Here we create a single keypoint and interrogate its selection
        status.

        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> k1 = mapdl.k(1, 0, 0, 0)
        >>> k1
        1

        We can use ``Query.ksel`` to interrogate the selection status
        of the node. The response is an ``enum.IntEnum`` object. If
        you query a node that does not exist, it will return a status
        ``SelectionStatus.UNDEFINED``.

        >>> q = mapdl.queries
        >>> q.ksel(k1)
        <SelectionStatus.SELECTED: 1>
        >>> mapdl.ksel('NONE')
        >>> q.ksel(k1)
        <SelectionStatus.UNSELECTED: -1>
        >>> q.ksel(0)
        <SelectionStatus.UNDEFINED: 0>
        """
        return SelectionStatus(self._run_query(f"KSEL({k})", integer=True))

    def lsel(self, n: int) -> SelectionStatus:
        """Returns selection status of a line.

        Returns a ``SelectionStatus`` object with values:

        1  - SELECTED
        0  - UNDEFINED
        -1 - UNSELECTED

        Parameters
        ----------
        n : int
            Line number

        Returns
        -------
        mapdl.ansys.core.inline_functions.SelectionStatus
            Status of line

        Examples
        --------
        Here we create a single line and interrogate its selection
        status.

        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> k1 = mapdl.k(1, 0, 0, 0)
        >>> k2 = mapdl.k(2, 1, 1, 1)
        >>> L1 = mapdl.l(k1, k2)
        >>> L1
        1

        We can use ``Query.lsel`` to interrogate the selection status
        of the line. The response is an ``enum.IntEnum`` object. If
        you query a line that does not exist, it will return a status
        ``SelectionStatus.UNDEFINED``.

        >>> q = mapdl.queries
        >>> q.lsel(L1)
        <SelectionStatus.SELECTED: 1>
        >>> mapdl.lsel('NONE')
        >>> q.lsel(L1)
        <SelectionStatus.UNSELECTED: -1>
        >>> q.lsel(0)
        <SelectionStatus.UNDEFINED: 0>
        """
        return SelectionStatus(self._run_query(f"LSEL({n})", integer=True))

    def asel(self, a: int) -> SelectionStatus:
        """Returns selection status of an area.

        Returns a ``SelectionStatus`` object with values:

        1  - SELECTED
        0  - UNDEFINED
        -1 - UNSELECTED

        Parameters
        ----------
        a : int
            Area number

        Returns
        -------
        mapdl.ansys.core.inline_functions.SelectionStatus
            Selection status of the area.

        Examples
        --------
        Here we create a single area and interrogate its selection
        status.

        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> k1 = mapdl.k(1, 0, 0, 0)
        >>> k2 = mapdl.k(2, 1, 0, 0)
        >>> k3 = mapdl.k(3, 1, 1, 1)
        >>> a1 = mapdl.a(k1, k2, k3)
        >>> a1
        1

        We can use ``Query.asel`` to interrogate the selection status
        of the line. The response is an ``enum.IntEnum`` object. If
        you query a line that does not exist, it will return a status
        ``SelectionStatus.UNDEFINED``.

        >>> q = mapdl.queries
        >>> q.asel(a1)
        <SelectionStatus.SELECTED: 1>
        >>> mapdl.asel('NONE')
        >>> q.asel(a1)
        <SelectionStatus.UNSELECTED: -1>
        >>> q.asel(0)
        <SelectionStatus.UNDEFINED: 0>
        """
        return SelectionStatus(self._run_query(f"ASEL({a})", integer=True))

    def esel(self, e: int) -> SelectionStatus:
        """Returns selection status of an element.

        Returns a ``SelectionStatus`` object with values:

        1  - SELECTED
        0  - UNDEFINED
        -1 - UNSELECTED

        Parameters
        ----------
        e : int
            Element number

        Returns
        -------
        mapdl.ansys.core.inline_functions.SelectionStatus
            Status of element

        Examples
        --------
        Here we create a single element and interrogate its selection
        status.

        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> mapdl.et(1, 'SHELL181')
        >>> n1 = mapdl.n(1, 0, 0, 0)
        >>> n2 = mapdl.n(2, 1, 0, 0)
        >>> n3 = mapdl.n(3, 1, 1, 1)
        >>> e1 = mapdl.e(n1, n2, n3)
        >>> e1
        1

        We can use ``Query.esel`` to interrogate the selection status
        of the element. The response is an ``enum.IntEnum`` object. If
        you query an element that does not exist, it will return a
        status ``SelectionStatus.UNDEFINED``.

        >>> q = mapdl.queries
        >>> q.esel(e1)
        <SelectionStatus.SELECTED: 1>
        >>> mapdl.esel('NONE')
        >>> q.esel(e1)
        <SelectionStatus.UNSELECTED: -1>
        >>> q.esel(0)
        <SelectionStatus.UNDEFINED: 0>
        """
        return SelectionStatus(self._run_query(f"ESEL({e})", integer=True))

    def vsel(self, v: int) -> SelectionStatus:
        """Returns selection status of a volume.

        Returns a :class:`SelectionStatus
        <mapdl.ansys.core.inline_functions.SelectionStatus>` with values:

        * 1 - SELECTED
        * 0 - UNDEFINED
        * -1 - UNSELECTED

        Parameters
        ----------
        v : int
            Volume number

        Returns
        -------
        mapdl.ansys.core.inline_functions.SelectionStatus
            Status of element

        Examples
        --------
        Here we create a single volume and interrogate its selection
        status.

        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> mapdl.et(1, 'SHELL181')
        >>> k1 = mapdl.k(1, 0, 0, 0)
        >>> k2 = mapdl.k(2, 1, 0, 0)
        >>> k3 = mapdl.k(3, 0, 1, 0)
        >>> k4 = mapdl.k(4, 0, 0, 1)
        >>> v1 = mapdl.v(k1, k2, k3, k4)
        >>> v1
        1

        We can use ``Query.vsel`` to interrogate the selection status
        of the element. The response is an ``enum.IntEnum`` object. If
        you query a volume that does not exist, it will return a
        status ``SelectionStatus.UNDEFINED``.

        >>> q = mapdl.queries
        >>> q.vsel(v1)
        <SelectionStatus.SELECTED: 1>
        >>> mapdl.vsel('NONE')
        >>> q.vsel(v1)
        <SelectionStatus.UNSELECTED: -1>
        >>> q.vsel(0)
        <SelectionStatus.UNDEFINED: 0>
        """
        return SelectionStatus(self._run_query(f"VSEL({v})", integer=True))


class _NextSelectedEntityQueries(_QueryExecution):
    _mapdl = None

    def ndnext(self, n: int) -> int:
        """Returns next selected node with a number greater than `n`.

        Returns the next highest node number after the supplied node
        number `n`, from the current selection.

        If no 'next selected' node exists (or if the supplied node
        number does not exist in the selection) `0` is returned.

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
        Here we create 10 nodes, select them all, and find the next
        selected node for each. For the last node there are no other
        nodes with a higher number, so 0 is returned.

        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> q = mapdl.queries
        >>> nodes = [mapdl.n(i+1, i, 0, 0) for i in range(10)]
        >>> next_selected_nodes = [q.ndnext(j) for j in nodes]
        >>> next_selected_nodes
        [2, 3, 4, 5, 6, 7, 8, 9, 10, 0]
        """
        return self._run_query(f"NDNEXT({n})", integer=True)

    def kpnext(self, k: int) -> int:
        """Returns next selected keypoint with a number greater than `k`.

        Returns the next highest keypoint number after the supplied
        keypoint number `k`, from the current selection.

        If no 'next selected' keypoint exists (or if the supplied
        keypoint number does not exist in the selection) `0` is
        returned.

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
        Here we create 10 keypoints and find the next selected keypoint
        for each. For the last node there are no other keypoints with a
        higher number, so 0 is returned.

        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> q = mapdl.queries
        >>> kps = [mapdl.k(i+1, i, 0, 0) for i in range(10)]
        >>> next_selected_kps = [q.kpnext(j) for j in kps]
        >>> next_selected_kps
        [2, 3, 4, 5, 6, 7, 8, 9, 10, 0]
        """
        return self._run_query(f"KPNEXT({k})", integer=True)

    def elnext(self, e: int) -> int:
        """Returns next selected element with a number greater than `e`.

        Returns the next highest element number after the supplied
        element number `e`, from the current selection.

        If no 'next selected' element exists (or if the supplied
        element number does not exist in the selection) `0` is
        returned.

        Parameters
        ----------
        e : int
            Element number

        Returns
        -------
        int
            Element number

        Examples
        --------
        Here we create 9 elements from 10 nodes and find the next
        selected element for each. For the last element there are no
        other elements with a higher number, so 0 is returned.

        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> mapdl.et(1, 'LINK11')
        >>> q = mapdl.queries
        >>> nodes = [mapdl.n(i+1, i, 0, 0) for i in range(10)]
        >>> els = [mapdl.e(i, i+1) for i in nodes[:-1]]
        >>> next_selected_els = [q.elnext(j) for j in els]
        >>> next_selected_els
        [2, 3, 4, 5, 6, 7, 8, 9, 0]
        """
        return self._run_query(f"ELNEXT({e})", integer=True)

    def lsnext(self, n: int) -> int:
        """Returns next selected line with a number greater than `n`.

        Returns the next highest line number after the supplied
        line number `n`, from the current selection.

        If no 'next selected' line exists (or if the supplied
        line number does not exist in the selection) `0` is
        returned.

        Parameters
        ----------
        n : int
            Line number

        Returns
        -------
        int
            Line number

        Examples
        --------
        Here we create 9 lines from 10 nodes and find the next
        selected line for each. For the last line there are no
        other lines with a higher number, so 0 is returned.

        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> mapdl.et(1, 'LINK11')
        >>> q = mapdl.queries
        >>> kps = [mapdl.k(i+1, i, 0, 0) for i in range(10)]
        >>> lines = [mapdl.l(i, i+1) for i in kps[:-1]]
        >>> next_selected_lines = [q.lsnext(j) for j in lines]
        >>> next_selected_lines
        [2, 3, 4, 5, 6, 7, 8, 9, 0]
        """
        return self._run_query(f"LSNEXT({n})", integer=True)

    def arnext(self, a: int) -> int:
        """Returns next selected area with a number greater than `a`.

        Returns the next highest area number after the supplied
        area number `a`, from the current selection.

        If no 'next selected' area exists (or if the supplied
        area number does not exist in the selection) `0` is
        returned.

        Parameters
        ----------
        a : int
            Area number

        Returns
        -------
        int
            Area number

        Examples
        --------
        Here we create 9 areas from 11 nodes and find the next
        selected area for each. For the last area there are no
        other areas with a higher number, so 0 is returned.

        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> q = mapdl.queries
        >>> farpoint = mapdl.k(999, 0, 10, 0)
        >>> kps = [mapdl.k(i+1, i, 0, 0) for i in range(10)]
        >>> areas = [mapdl.a(i, i+1, farpoint) for i in kps[:-1]]
        >>> next_selected_areas = [q.arnext(j) for j in areas]
        >>> next_selected_areas
        [2, 3, 4, 5, 6, 7, 8, 9, 0]
        """
        return self._run_query(f"ARNEXT({a})", integer=True)

    def vlnext(self, v: int) -> int:
        """Returns next selected volume with a number greater than `v`.

        Returns the next highest volume number after the supplied
        volume number `v`, from the current selection.

        If no 'next selected' volume exists (or if the supplied
        volume number does not exist in the selection) `0` is
        returned.

        Parameters
        ----------
        v : int
            Volume number

        Returns
        -------
        int
            Volume number

        Examples
        --------
        Here we create 9 volumes from 12 nodes and find the next
        selected volume for each. For the last volume there are no
        other volumes with a higher number, so 0 is returned.

        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> q = mapdl.queries
        >>> point1 = mapdl.k(999, 0, 10, 0)
        >>> point2 = mapdl.k(99, 0, 0, 10)
        >>> kps = [mapdl.k(i+1, i, 0, 0) for i in range(10)]
        >>> vols = [mapdl.v(i, i+1, point1, point2) for i in kps[:-1]]
        >>> next_selected_vols = [q.vlnext(j) for j in vols]
        >>> next_selected_vols
        [2, 3, 4, 5, 6, 7, 8, 9, 0]
        """
        return self._run_query(f"VLNEXT({v})", integer=True)
