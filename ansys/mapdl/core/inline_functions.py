import warnings
from enum import IntEnum


class SelectionStatus(IntEnum):
    """Enumeration class for selection status information.

    This class is used with methods on the ``Query`` class and has the
    following options.

    UNSELECTED = -1
    UNDEFINED = 0
    SELECTED = 1

    Examples
    --------
    The following example is taken from ``Query.nsel`` and demonstrates
    how `SelectionSatus` appears in PyMAPDL.

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
    UNSELECTED = -1
    UNDEFINED = 0
    SELECTED = 1


class _ParameterParsing:
    def _parse_parameter_integer_response(self, response) -> int:
        return int(self._parse_parameter_float_response(response))

    @staticmethod
    def _parse_parameter_float_response(response) -> float:
        if 'PARAMETER' not in response or '=' not in response:
            raise TypeError(f'Parameter response not recognised: '
                            f'"{response}"')
        parts = response.rsplit('=', 1)
        if 'WARNING' in parts[0]:
            warnings.warn(parts[0])

        number = parts[1].strip()
        return float(number)


class _ComponentQueries(_ParameterParsing):
    _mapdl = None

    def centrx(self, e: int) -> float:
        """Return the x coordinate of the element centroid.

        Fetches centroid X-coordinate of element ``e`` in global
        Cartesian coordinate system. Centroid is determined from the
        selected nodes on the element.

        Parameters
        ----------
        e : int
            The element number of the element to be considered.

        Returns
        -------
        float
            The centroid coordinate.

        Examples
        --------
        Here we construct a line between the coordinates ``(0, 0, 0)``
        and ``(1, 2, 3)`` then find the centroid x-coordinate of this
        element.

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
        """Return the y coordinate of the element centroid.

        Fetches centroid Y-coordinate of element ``e`` in global
        Cartesian coordinate system. Centroid is determined from the
        selected nodes on the element.

        Parameters
        ----------
        e : int
            The element number of the element to be considered.

        Returns
        -------
        float
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
        """Return the z coordinate of the element centroid.

        Fetches centroid Z-coordinate of element ``e`` in global
        Cartesian coordinate system. Centroid is determined from the
        selected nodes on the element.

        Parameters
        ----------
        e : int
            The element number of the element to be considered.

        Returns
        -------
        float
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
        """Return the x coordinate of a node.

        Fetches X-coordinate of node ``n`` in the active coordinate
        system.

        Parameters
        ----------
        n : int
            Node number

        Returns
        -------
        float
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
        """Return the y coordinate of a node.

        Fetches Y-coordinate of node ``n`` in the active coordinate
        system.

        Parameters
        ----------
        n : int
            Node number

        Returns
        -------
        float
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
        """Return the z coordinate of a node.

        Fetches Z-coordinate of node ``n`` in the active coordinate
        system.

        Parameters
        ----------
        n : int
            Node number

        Returns
        -------
        float
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
        """Return the x coordinate of a keypont.

        X-coordinate of keypoint ``k`` in the active coordinate system.

        Parameters
        ----------
        k : int
            Keypoint number to be considered.

        Returns
        -------
        float
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
        """Return the y coordinate of a keypont.

        Y-coordinate of keypoint ``k`` in the active coordinate system.

        Parameters
        ----------
        k : int
            Keypoint number to be considered.

        Returns
        -------
        float
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
        """Return the z coordinate of a keypont.

        Z-coordinate of keypoint ``k`` in the active coordinate system.

        Parameters
        ----------
        k : int
            Keypoint number to be considered.

        Returns
        -------
        float
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


class _DisplacementComponentQueries(_ParameterParsing):
    _mapdl = None

    def rotx(self, n: int) -> float:
        """Returns x-component of rotational displacement at a node.

        X-component of rotational displacement at node ``n``.

        Parameters
        ----------
        n : int
            Node number

        Returns
        -------
        float
            Rotational displacement of the node.

        Examples
        --------
        This example has been adapted from the example script
        :ref:`ref_rotational_displacement_example`. We create a square
        of shell material, apply a displacement perpendicular to the
        plane of the material, and then solve.

        Then we can use ``Query.rotx`` to get the x-component rotational
        displacement at the middle node on the deformed edge.

        >>> from ansys.mapdl.core import launch_mapdl
        >>> from ansys.mapdl.core.inline_functions import Query
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> mapdl.et(1, 'SHELL181')
        >>> mapdl.mp("EX", 1, 2e5)
        >>> mapdl.rectng(0, 1, 0, 1)
        >>> mapdl.sectype(1, "SHELL")
        >>> mapdl.secdata(0.1)
        >>> mapdl.esize(0.2)
        >>> mapdl.amesh("all")
        >>> mapdl.run('/SOLU')
        >>> mapdl.antype('STATIC')
        >>> mapdl.nsel("s", "loc", "x", 0)
        >>> mapdl.d("all", "all")
        >>> mapdl.nsel("s", "loc", "x", 1)
        >>> mapdl.d("all", "uz", -0.1)
        >>> mapdl.allsel("all")
        >>> mapdl.solve()
        >>> q = Query(mapdl)
        >>> node = q.node(1, 0.5, 0)
        >>> q.rotx(node)
        -0.0002149851187
        """
        response = self._mapdl.run(f'_=ROTX({n})')
        return self._parse_parameter_float_response(response)

    def roty(self, n: int) -> float:
        """Returns y-component of rotational displacement at a node.

        Y-component of rotational displacement at node ``n``.

        Parameters
        ----------
        n : int
            Node number

        Returns
        -------
        float
            Rotational displacement of the node.

        Examples
        --------
        This example has been adapted from the example script
        :ref:`ref_rotational_displacement_example`. We create a square
        of shell material, apply a displacement perpendicular to the
        plane of the material, and then solve.

        Then we can use ``Query.roty`` to get the y-component rotational
        displacement at the middle node on the deformed edge.

        >>> from ansys.mapdl.core import launch_mapdl
        >>> from ansys.mapdl.core.inline_functions import Query
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> mapdl.et(1, 'SHELL181')
        >>> mapdl.mp("EX", 1, 2e5)
        >>> mapdl.rectng(0, 1, 0, 1)
        >>> mapdl.sectype(1, "SHELL")
        >>> mapdl.secdata(0.1)
        >>> mapdl.esize(0.2)
        >>> mapdl.amesh("all")
        >>> mapdl.run('/SOLU')
        >>> mapdl.antype('STATIC')
        >>> mapdl.nsel("s", "loc", "x", 0)
        >>> mapdl.d("all", "all")
        >>> mapdl.nsel("s", "loc", "x", 1)
        >>> mapdl.d("all", "uz", -0.1)
        >>> mapdl.allsel("all")
        >>> mapdl.solve()
        >>> q = Query(mapdl)
        >>> node = q.node(1, 0.5, 0)
        >>> q.roty(node)
        0.1489593933
        """
        response = self._mapdl.run(f'_=ROTY({n})')
        return self._parse_parameter_float_response(response)

    def rotz(self, n: int) -> float:
        """Returns z-component of rotational displacement at a node.

        Z-component of rotational displacement at node ``n``.

        Parameters
        ----------
        n : int
            Node number

        Returns
        -------
        float
            Rotational displacement of the node.

        Examples
        --------
        This example has been adapted from the example script
        :ref:`ref_rotational_displacement_example`. We create a square
        of shell material, apply a displacement perpendicular to the
        plane of the material, and then solve.

        Then we can use ``Query.rotz`` to get the z-component rotational
        displacement at the middle node on the deformed edge.

        >>> from ansys.mapdl.core import launch_mapdl
        >>> from ansys.mapdl.core.inline_functions import Query
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> mapdl.et(1, 'SHELL181')
        >>> mapdl.mp("EX", 1, 2e5)
        >>> mapdl.rectng(0, 1, 0, 1)
        >>> mapdl.sectype(1, "SHELL")
        >>> mapdl.secdata(0.1)
        >>> mapdl.esize(0.2)
        >>> mapdl.amesh("all")
        >>> mapdl.run('/SOLU')
        >>> mapdl.antype('STATIC')
        >>> mapdl.nsel("s", "loc", "x", 0)
        >>> mapdl.d("all", "all")
        >>> mapdl.nsel("s", "loc", "x", 1)
        >>> mapdl.d("all", "uz", -0.1)
        >>> mapdl.allsel("all")
        >>> mapdl.solve()
        >>> q = Query(mapdl)
        >>> node = q.node(1, 0.5, 0)
        >>> q.rotz(node)
        0.0
        """
        response = self._mapdl.run(f'_=ROTZ({n})')
        return self._parse_parameter_float_response(response)

    def ux(self, n: int) -> float:
        """Returns x-component of structural displacement at a node.

        X-component of structural displacement at node ``n``.

        Parameters
        ----------
        n : int
            Node number

        Returns
        -------
        float
            Displacement of node

        Examples
        --------
        In this example we create a simple block of 6 cubic elements,
        fix one end in place, and then bend the other perpendicular to
        it. We can then examine the displacement of one of the nodes
        in the x-direction at the deformed end (node number 7).

        >>> from ansys.mapdl.core import launch_mapdl
        >>> from ansys.mapdl.core.inline_functions import Query
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> mapdl.et(1, 'SOLID5')
        >>> mapdl.block(0, 10, 0, 20, 0, 30)
        >>> mapdl.esize(10)
        >>> mapdl.vmesh('ALL')
        >>> mapdl.mp('EX', 1, 210E9)
        >>> mapdl.nsel('S', 'LOC', 'Z', 0)
        >>> mapdl.d('ALL', 'UX')
        >>> mapdl.d('ALL', 'UY')
        >>> mapdl.d('ALL', 'UZ')
        >>> mapdl.nsel('S', 'LOC', 'Z', 30)
        >>> mapdl.f('ALL', 'FY', 1000)
        >>> mapdl.run('/SOLU')
        >>> mapdl.antype('STATIC')
        >>> mapdl.solve()
        >>> mapdl.finish()
        >>> q = Query(mapdl)
        >>> q.ux(7)
        1.549155634e-07

        """
        response = self._mapdl.run(f'_=UX({n})')
        return self._parse_parameter_float_response(response)

    def uy(self, n: int) -> float:
        """Returns y-component of structural displacement at a node.

        Y-component of structural displacement at node ``n``.

        Parameters
        ----------
        n : int
            Node number

        Returns
        -------
        float
            Displacement of node

        Examples
        --------
        In this example we create a simple block of 6 cubic elements,
        fix one end in place, and then bend the other perpendicular to
        it. We can then examine the displacement of one of the nodes
        in the y-direction at the deformed end (node number 7).

        >>> from ansys.mapdl.core import launch_mapdl
        >>> from ansys.mapdl.core.inline_functions import Query
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> mapdl.et(1, 'SOLID5')
        >>> mapdl.block(0, 10, 0, 20, 0, 30)
        >>> mapdl.esize(10)
        >>> mapdl.vmesh('ALL')
        >>> mapdl.mp('EX', 1, 210E9)
        >>> mapdl.nsel('S', 'LOC', 'Z', 0)
        >>> mapdl.d('ALL', 'UX')
        >>> mapdl.d('ALL', 'UY')
        >>> mapdl.d('ALL', 'UZ')
        >>> mapdl.nsel('S', 'LOC', 'Z', 30)
        >>> mapdl.f('ALL', 'FY', 1000)
        >>> mapdl.run('/SOLU')
        >>> mapdl.antype('STATIC')
        >>> mapdl.solve()
        >>> mapdl.finish()
        >>> q = Query(mapdl)
        >>> q.uy(7)
        5.803680779e-10

        """
        response = self._mapdl.run(f'_=UY({n})')
        return self._parse_parameter_float_response(response)

    def uz(self, n: int) -> float:
        """Returns z-component of structural displacement at a node.

        Z-component of structural displacement at node ``n``.

        Parameters
        ----------
        n : int
            Node number

        Returns
        -------
        float
            Displacement of node

        Examples
        --------
        In this example we create a simple block of 6 cubic elements,
        fix one end in place, and then bend the other perpendicular to
        it. We can then examine the displacement of one of the nodes
        in the z-direction at the deformed end (node number 7).

        >>> from ansys.mapdl.core import launch_mapdl
        >>> from ansys.mapdl.core.inline_functions import Query
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> mapdl.et(1, 'SOLID5')
        >>> mapdl.block(0, 10, 0, 20, 0, 30)
        >>> mapdl.esize(10)
        >>> mapdl.vmesh('ALL')
        >>> mapdl.mp('EX', 1, 210E9)
        >>> mapdl.nsel('S', 'LOC', 'Z', 0)
        >>> mapdl.d('ALL', 'UX')
        >>> mapdl.d('ALL', 'UY')
        >>> mapdl.d('ALL', 'UZ')
        >>> mapdl.nsel('S', 'LOC', 'Z', 30)
        >>> mapdl.f('ALL', 'FY', 1000)
        >>> mapdl.run('/SOLU')
        >>> mapdl.antype('STATIC')
        >>> mapdl.solve()
        >>> mapdl.finish()
        >>> q = Query(mapdl)
        >>> q.uz(7)
        3.74530389e-08

        """
        response = self._mapdl.run(f'_=UZ({n})')
        return self._parse_parameter_float_response(response)


class _SelectionStatusQueries(_ParameterParsing):
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
        response = self._mapdl.run(f'_=NSEL({n})')
        integer = self._parse_parameter_integer_response(response)
        return SelectionStatus(integer)

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
        >>> from ansys.mapdl.core.inline_functions import Query
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> k1 = mapdl.k(1, 0, 0, 0)
        >>> k1
        1

        We can use ``Query.ksel`` to interrogate the selection status
        of the node. The response is an ``enum.IntEnum`` object. If
        you query a node that does not exist, it will return a status
        ``SelectionStatus.UNDEFINED``.

        >>> q = Query(mapdl)
        >>> q.ksel(k1)
        <SelectionStatus.SELECTED: 1>
        >>> mapdl.ksel('NONE')
        >>> q.ksel(k1)
        <SelectionStatus.UNSELECTED: -1>
        >>> q.ksel(0)
        <SelectionStatus.UNDEFINED: 0>
        """
        response = self._mapdl.run(f'_=KSEL({k})')
        integer = self._parse_parameter_integer_response(response)
        return SelectionStatus(integer)

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
        >>> from ansys.mapdl.core.inline_functions import Query
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

        >>> q = Query(mapdl)
        >>> q.lsel(L1)
        <SelectionStatus.SELECTED: 1>
        >>> mapdl.lsel('NONE')
        >>> q.lsel(L1)
        <SelectionStatus.UNSELECTED: -1>
        >>> q.lsel(0)
        <SelectionStatus.UNDEFINED: 0>
        """
        response = self._mapdl.run(f'_=LSEL({n})')
        integer = self._parse_parameter_integer_response(response)
        return SelectionStatus(integer)

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
        >>> from ansys.mapdl.core.inline_functions import Query
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

        >>> q = Query(mapdl)
        >>> q.asel(a1)
        <SelectionStatus.SELECTED: 1>
        >>> mapdl.asel('NONE')
        >>> q.asel(a1)
        <SelectionStatus.UNSELECTED: -1>
        >>> q.asel(0)
        <SelectionStatus.UNDEFINED: 0>
        """
        response = self._mapdl.run(f'_=ASEL({a})')
        integer = self._parse_parameter_integer_response(response)
        return SelectionStatus(integer)

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
        >>> from ansys.mapdl.core.inline_functions import Query
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

        >>> q = Query(mapdl)
        >>> q.esel(e1)
        <SelectionStatus.SELECTED: 1>
        >>> mapdl.esel('NONE')
        >>> q.esel(e1)
        <SelectionStatus.UNSELECTED: -1>
        >>> q.esel(0)
        <SelectionStatus.UNDEFINED: 0>
        """
        response = self._mapdl.run(f'_=ESEL({e})')
        integer = self._parse_parameter_integer_response(response)
        return SelectionStatus(integer)


class Query(_ComponentQueries,
            _InverseGetComponentQueries,
            _DisplacementComponentQueries,
            _SelectionStatusQueries):
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
    - `ux(n)` - get the structural displacement at node `n` in x
    - `uy(n)` - get the structural displacement at node `n` in y
    - `uz(n)` - get the structural displacement at node `n` in z
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
