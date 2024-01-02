"""
Contains the Node implementation of the MapdlDb class.

This allows access to the Nodes in the MAPDL DB from Python.

"""
import weakref

from ansys.api.mapdl.v0 import ansys_kernel_pb2 as anskernel
from ansys.api.mapdl.v0 import mapdl_db_pb2
import numpy as np
from numpy.lib import recfunctions

from ansys.mapdl.core.errors import MapdlRuntimeError

from ..common_grpc import DEFAULT_CHUNKSIZE
from .database import DBDef, MapdlDb, check_mapdl_db_is_alive


class DbNodes:

    """
    Abstract mapdl db nodes class.

    Examples
    --------
    Create a nodes instance.

    >>> from ansys.mapdl.core import launch_mapdl
    >>> mapdl = launch_mapdl()
    >>> # create nodes...
    >>> nodes = mapdl.db.nodes
    >>> print(nodes)
    MAPDL Database Nodes
        Number of nodes:          270641
        Number of selected nodes: 270641
        Maximum node number:      270641

    >>> mapdl.nsel("NONE")
    >>> print(nodes)
    MAPDL Database Nodes
        Number of nodes:          270641
        Number of selected nodes: 0
        Maximum node number:      270641

    Return the selection status and the coordinates of node 22.

    >>> nodes = mapdl.db.nodes
    >>> sel, coord = nodes.coord(22)
    >>> coord
    (1.0, 0.5, 0.0, 0.0, 0.0, 0.0)

    Return all the node indices, coordinates, and angles of all the nodes.

    >>> nodes = mapdl.db.nodes
    >>> ind, coords, angles = nodes.all_asarray()
    >>> ind
    array([     1,      2,      3, ..., 270639, 270640, 270641], dtype=int32)

    >>> coords
    array([[0.    , 1.    , 0.    ],
           [0.    , 0.    , 0.    ],
           [0.    , 0.9875, 0.    ],
           ...,
           [0.9875, 0.975 , 0.925 ],
           [0.9875, 0.975 , 0.95  ],
           [0.9875, 0.975 , 0.975 ]])

    >>> angles
    array([[0., 0., 0.],
           [0., 0., 0.],
           [0., 0., 0.],
           ...,
           [0., 0., 0.],
           [0., 0., 0.],
           [0., 0., 0.]])

    """

    def __init__(self, db):
        """Initialize this class."""
        if not isinstance(db, MapdlDb):  # pragma: no cover
            raise TypeError("``db`` must be a MapdlDb instance")
        self._db_weakref = weakref.ref(db)
        self._itnod = -1

    def __str__(self):
        """Return the string representation of this class."""
        lines = ["MAPDL Database Nodes"]
        lines.append(f"    Number of nodes:          {self.num()}")
        lines.append(f"    Number of selected nodes: {self.num(selected=True)}")
        lines.append(f"    Maximum node number:      {self.max_num}")
        return "\n".join(lines)

    def __repr__(self) -> str:
        return self.__str__()

    @property
    def _db(self):
        """Return the weakly referenced instance of db."""
        return self._db_weakref()

    @check_mapdl_db_is_alive
    def first(self, inod=0):
        """
        Return the number of the first node.

        This starts at ``inod``, defaults to the first node in the model.

        Parameters
        ----------
        inod : int, optional
            The first node number to consider as the "first node".

        Returns
        -------
        int
            The first node number within either selected or all nodes.

        Examples
        --------
        Return the first selected node.

        >>> nodes.first()
        1

        Return the first node after node 10.

        >>> nodes.first(inod=10)
        11

        """
        self._itnod = inod
        return self.next()

    @check_mapdl_db_is_alive
    def next(self):
        """
        Return the number of the next selected node.

        You must first call :func:`DbNodes.first`.

        Returns
        -------
        int
            The next selected node number. Returns 0 if there are no more nodes.

        Examples
        --------
        Call :func:`DbNodes.first` first.

        >>> nodes.first()
        1

        Then get the next node.

        >>> nodes.next()
        2

        """
        if self._itnod == -1:
            raise MapdlRuntimeError(
                "You first have to call the `DbNodes.first` method."
            )

        request = mapdl_db_pb2.NodRequest(next=self._itnod)
        result = self._db._stub.NodNext(request)
        self._itnod = result.inum
        return self._itnod

    # def next_defined(self):
    #     """get the number of the next defined node
    #     You first have to call first)_

    #     Returns
    #     -------
    #     next_defined : int
    #     The next defined node number
    #     = 0 - no more nodes
    #     """

    #     if self._itnod == -1:
    #         raise TypeError(
    #             "``db.next_node`` you first have to call first_node function"
    #         )
    #     breakpoint()
    #     request = mapdl_db_pb2.NodRequest(next=self._itnod)
    #     result = self._db._stub.NodNextDefined(request)
    #     self._itnod = result.inum
    #     return self._itnod

    @check_mapdl_db_is_alive
    def info(self, inod, ikey):
        """
        Return information about a node.

        Parameters
        ----------
        inod : int
            Node number. Should be 0 for key=11 for the following:

            * ``DB_NUMDEFINED``
            * ``DB_NUMSELECTED``
            * ``DB_MAXDEFINED``
            * ``DB_MAXRECLENG``

        ikey : int
            Key of the information needed about the node. One of the following:

            * DB_SELECTED : return select status

                * 0 - node is undefined.
                * -1 - node is unselected.
                *  1 - node is selected.

            * DB_NUMDEFINED - return number of defined nodes
            * DB_NUMSELECTED - return number of selected nodes
            * DB_MAXDEFINED - return highest node number defined
            * DB_MAXRECLENG - return maximum record length (dp words)
            * 2 - length (dp words)
            * 3 -
            * 4 - pointer to first data word
            * 11 - return void percent (integer)
            * 17 - pointer to start of index
            * 117 - return the maximum number of DP contact data stored for any node
            * -1 -
            * -2 - superelement flag
            * -3 - master dof bit pattern
            * -4 - active dof bit pattern
            * -5 - solid model attachment
            * -6 - pack nodal line parametric value
            * -7 - constraint bit pattern
            * -8 - force bit pattern
            * -9 - body force bit pattern
            * -10 - internal node flag
            * -11 - orientation node flag =1 is =0 isnot
            * -11 - contact node flag <0
            * -12 - constraint bit pattern (for DSYM)
            * -13 - if dof constraint written to file. (for LSDYNA only)
            * -14 - nodal coordinate system number (set by NROTATE)
            * -101 - pointer to node data record
            * -102 - pointer to angle record
            * -103 -
            * -104 - pointer to attached couplings
            * -105 - pointer to attacted constraint equations
            * -106 - pointer to nodal stresses
            * -107 - pointer to specified disp'S
            * -108 - pointer to specified forces
            * -109 - pointer to x/y/z record
            * -110 -
            * -111 -
            * -112 - pointer to nodal temperatures
            * -113 - pointer to nodal heat generations
            * -114 -
            * -115 - pointer to calculated displacements
            * -116 -

        Returns
        -------
        int
            Information from the query based on ``ikey``.

        Examples
        --------
        Query if a node is selected.

        >>> from ansys.mapdl.core.database import DBDef
        >>> nodes = mapdl.db.nodes
        >>> nodes.info(1, DBDef.DB_SELECTED)
        1

        """
        if isinstance(ikey, DBDef):
            ikey = ikey.value
        request = mapdl_db_pb2.NodInqrRequest(node=inod, key=ikey)
        result = self._db._stub.NodInqr(request)
        return result.ret

    @check_mapdl_db_is_alive
    def num(self, selected=False) -> int:
        """
        Return the number of nodes, either selected or all.

        Parameters
        ----------
        selected : bool, optional
            Return either the number of selected nodes of the total number of
            nodes.

        Returns
        -------
        int
            Number of nodes.

        Examples
        --------
        Get the number of selected nodes.

        >>> nodes = mapdl.db.nodes
        >>> nodes.num(selected=True)
        425

        """
        if selected:
            return self.info(0, DBDef.DB_NUMSELECTED.value)
        return self.info(0, DBDef.DB_NUMDEFINED.value)

    @property
    @check_mapdl_db_is_alive
    def max_num(self) -> int:
        """
        Return the maximum node number.

        Examples
        --------
        Return the maximum node number.

        >>> nodes = mapdl.db.nodes
        >>> nodes.max_num
        425

        """
        return self.info(0, DBDef.DB_MAXDEFINED.value)

    @check_mapdl_db_is_alive
    def coord(self, inod):
        """
        Return the location of a node.

        Parameters
        ----------
        inod : int
            Node number.

        Returns
        -------
        int
            Selection status:

            * 0 - node is selected
            * 1 - node is not defined
            * -1 - node is unselected

        tuple
            Coordinates (first 3 values) and rotation angles (last 3 values).

        Examples
        --------
        Return the selection status and the coordinates of node 22.

        >>> nodes = mapdl.db.nodes
        >>> sel, coord = nodes.coord(22)
        >>> coord
        (1.0, 0.5, 0.0, 0.0, 0.0, 0.0)

        """
        request = mapdl_db_pb2.getnodRequest(node=inod)
        node = self._db._stub.getNod(request)
        return node.kerr, tuple(node.v)

    @check_mapdl_db_is_alive
    def all_asarray(self):
        """
        Return all node indices, coordinates, and angles as arrays.

        .. note::
           This only returns data of the selected nodes.

        Returns
        -------
        np.ndarray
            Numpy.int32 array of node numbers with shape ``(n_node,)``.
        np.ndarray
            Numpy.double array of node coordinates with shape ``(n_node, 3)``.
        np.ndarray
            Numpy.double array of node angles with shape ``(n_node, 3)``.

        Examples
        --------
        Return all the node indices, coordinates, and angles of all the nodes.

        >>> nodes = mapdl.db.nodes
        >>> ind, coords, angles = nodes.all_asarray()
        >>> ind
        array([     1,      2,      3, ..., 270639, 270640, 270641], dtype=int32)

        >>> coords
        array([[0.    , 1.    , 0.    ],
               [0.    , 0.    , 0.    ],
               [0.    , 0.9875, 0.    ],
               ...,
               [0.9875, 0.975 , 0.925 ],
               [0.9875, 0.975 , 0.95  ],
               [0.9875, 0.975 , 0.975 ]])

        >>> angles
        array([[0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               ...,
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.]])

        """
        chunk_size = DEFAULT_CHUNKSIZE
        metadata = [("chunk_size", str(chunk_size))]
        request = anskernel.EmptyRequest()
        chunks = self._db._stub.getAllNodC(request, metadata=metadata)

        n_nodes = int(chunks.initial_metadata()[0][1])

        ind = np.empty(n_nodes, np.int32)
        coord = np.empty((n_nodes, 3), np.double)
        angle = np.empty((n_nodes, 3), np.double)

        # each "chunk" from MAPDL is organized as:
        # n_nodes, node, node ... last_node
        #
        # where each node is
        # INT32, DOUBLE, DOUBLE, DOUBLE, DOUBLE, DOUBLE, DOUBLE

        # first, just interpret as int32 and extract node numbering
        # ignore the first int as this is n_nodes
        # data = parse_chunks(chunks, np.int32)
        c = 0
        for chunk in chunks:
            parsed_chunk = np.frombuffer(chunk.payload, np.int32)
            n_node = parsed_chunk[0]
            data = parsed_chunk[1:].view(
                [
                    ("ind", np.int32),
                    ("x", np.double),
                    ("y", np.double),
                    ("z", np.double),
                    ("xang", np.double),
                    ("yang", np.double),
                    ("zang", np.double),
                ]
            )

            ind_chunk = recfunctions.structured_to_unstructured(data[["ind"]]).ravel()

            coord_chunk = recfunctions.structured_to_unstructured(
                data[["x", "y", "z"]]
            ).reshape((-1, 3))

            angle_chunk = recfunctions.structured_to_unstructured(
                data[["xang", "yang", "zang"]]
            ).reshape((-1, 3))

            ind[c : c + n_node] = ind_chunk
            coord[c : c + n_node] = coord_chunk
            angle[c : c + n_node] = angle_chunk
            c += n_node

        return ind, coord, angle

    @check_mapdl_db_is_alive
    def push(self, inod, x, y, z, xang=None, yang=None, zang=None):
        """
        Push a single node into the DB.

        Parameters
        ----------
        inod : int
            Node number.
        x : float
            X coordinate.
        y : float
            X coordinate.
        z : float
            Z coordinate.
        xang : float, optional
            X angle.
        yang : float, optional
            X angle.
        zang : float, optional
            Z angle.

        Examples
        --------
        Update node 1 to have coordinates ``(10.0, 20.0, 30.0)``.

        >>> nodes = mapdl.db.nodes
        >>> nodes.push(1, 10, 20, 30)
        >>> sel, coord = nodes.coord(1)
        >>> coord
        (10.0, 20.0, 30.0, 0.0, 0.0, 0.0)

        """
        request = mapdl_db_pb2.putnodRequest()
        request.node = inod
        request.vctn.extend([x, y, z])
        if xang:
            request.vctn.extend([xang])
        if yang:
            if xang is None:
                raise ValueError("X angle must be input as well when inputing Y angle")
            request.vctn.extend([yang])
        if zang:
            if xang is None or yang is None:
                raise ValueError(
                    "X and Y angles must be input as well when inputing Z angle"
                )
            request.vctn.extend([zang])

        self._db._stub.putNod(request)

    ###############################################################################
    # unimplemented

    # def _select(self, inod, sel=1):
    #     """Select, unselect, or delete a node in the database.

    #     Parameters
    #     ----------
    #     inod : int
    #         Node number.
    #     sel : int
    #         Action to take. One of the following:

    #         * ``0`` - Delete the node.
    #         * ``1`` - Select a node.
    #         * ``-1`` - Unselect a node.
    #         * ``2`` - Switch the exist select status.

    #     """
    #     request = mapdl_db_pb2.NodSelRequest(inum=inod, ksel=sel)
    #     self._db._stub.NodSel(request)

    # def delete(self, inod):
    #     """Delete a node from the database.

    #     Parameters
    #     ----------
    #     inod : int
    #         Node number.

    #     Examples
    #     --------
    #     Push and then delete a node.

    #     >>> nodes = mapdl.db.nodes
    #     >>> nodes.push(1, 10, 20, 30)
    #     >>> sel, coord = nodes.coord(1)
    #     >>> nodes.delete(1)

    #     """
    #     return self._select(inod, 0)

    # def select(self, inod):
    #     """select a node in the database.

    #     Parameters
    #     ----------
    #     inod : int
    #         Node number.

    #     Examples
    #     --------

    #     """
    #     self._select(inod, 1)

    # def unselect(self, inod):
    #     """Unselect a node in the database.

    #     Parameters
    #     ----------
    #     inod : int
    #         Node number.

    #     Examples
    #     --------

    #     """
    #     self._select(inod, -1)

    # def invselect(self, inod):
    #     """Inverse the select status of a node in the database.

    #     Parameters
    #     ----------
    #     inod : int
    #         Node number.

    #     Examples
    #     --------

    #     """
    #     self._select(inod, 2)

    ###############################################################################
