"""
Contains the element implement of the MAPDL database service.

This allows lower level the access to the elements in the MAPDL database.

"""
import weakref

from ansys.api.mapdl.v0 import mapdl_db_pb2

from ansys.mapdl.core.errors import MapdlRuntimeError

from . import DBDef, MapdlDb, check_mapdl_db_is_alive


class DbElems:

    """
    Abstract mapdl database element class.

    Examples
    --------
    Create a MAPDL database element instance.

    >>> from ansys.mapdl.core import launch_mapdl
    >>> mapdl = launch_mapdl()
    >>> elems = mapdl.db.elems
    >>> print(elems)
    MAPDL Database Elements
        Number of elements:          64
        Number of selected elements: 64
        Maximum element number:      64

    Return the element information of element 1.

    >>> elems = mapdl.db.elems
    >>> elem_info = elems.get(1)

    Return the nodes belonging to the element.

    >>> elem_info.nodes
    [2, 27, 37, 8]

    Return the element data.

    >>> elem_info.elmdat
    [1, 1, 1, 1, 0, 0, 14, 0, 0, 0]

    """

    def __init__(self, db):
        """Initialize this class."""
        if not isinstance(db, MapdlDb):  # pragma: no cover
            raise TypeError("``db`` must be a MapdlDb instance")
        self._db_weakref = weakref.ref(db)
        self._itelm = -1

    @property
    def _db(self):
        """Return the weakly referenced instance of the database."""
        return self._db_weakref()

    def __str__(self):
        """Return the string representation of this class."""
        lines = ["MAPDL Database Elements"]
        lines.append(f"    Number of elements:          {self.num()}")
        lines.append(f"    Number of selected elements: {self.num(selected=True)}")
        lines.append(f"    Maximum element number:      {self.max_num}")
        return "\n".join(lines)

    def __repr__(self) -> str:
        return self.__str__()

    @check_mapdl_db_is_alive
    def first(self, ielm=0):
        """
        Get the number of the first element.

        This starts at ``inod``, defaults to the first element in the model.

        Parameters
        ----------
        ielm : int, optional
            The first element number to consider as the "first element".

        Returns
        -------
        int
            The first element number after ``ielm``.

        Examples
        --------
        Return the first selected element.

        >>> elems = mapdl.db.elems
        >>> elems.first()
        1

        Return the first element after element 10.

        >>> elems.first(ielm=10)
        11

        """
        self._itelm = ielm
        return self.next()

    @check_mapdl_db_is_alive
    def next(self):
        """
        Return the number of the next selected element.

        You must first call :func:`DbElems.first`.

        Returns
        -------
        int
            The next selected element number. Returns 0 if there are no more nodes.

        Examples
        --------
        Call :func:`DbElems.first` first.

        >>> elems = mapdl.db.elems
        >>> elems.first()
        1

        Then get the next node.

        >>> elems.next()
        2

        """
        if self._itelm == -1:
            raise MapdlRuntimeError(
                "You first have to call the `DbElems.first` method."
            )

        request = mapdl_db_pb2.ElmRequest(next=self._itelm)
        result = self._db._stub.ElmNext(request)
        self._itelm = result.inum
        return self._itelm

    ###########################################################################
    # broken on server-side as of 2022R2 (server v0.5.1)
    # def next_defined(self):
    #     """get the number of the next defined elem
    #     You first have to call first)_

    #     Returns
    #     -------
    #     next_defined : int
    #     The next defined elem number
    #     = 0 - no more elems
    #     """

    #     if self._itelm == -1:
    #         raise TypeError("``elems.next`` you first have to call first function")

    #     request = mapdl_db_pb2.ElmRequest(next=self._itelm)
    #     result = self._db._stub.ElmNextDefined(request)
    #     self._itelm = result.inum
    #     return self._itelm
    ###########################################################################

    @check_mapdl_db_is_alive
    def info(self, ielm, ikey):
        """
        Get information about a element

        Parameters
        ----------
        ielm : int
            Element number. Should be 0 for key=11 for the following:

            * ``DB_NUMDEFINED``
            * ``DB_NUMSELECTED``
            * ``DB_MAXDEFINED``
            * ``DB_MAXRECLENG``

        ikey : int
            Key of the information needed about the node. One of the following:

            * DB_SELECTED : return select status

                * 0 - element is undefined.
                * -1 - element is unselected.
                *  1 - element is selected.

            * DB_NUMDEFINED - return number of defined elements
            * DB_NUMSELECTED - return number of selected elements
            * DB_MAXDEFINED - return highest element number defined
            * DB_MAXRECLENG - return maximum record length (dp words)
            * 2 - length (dp words)
            * 3 -
            * 4 - pointer to first data word
            * 11 - return void percent (integer)
            * 17 - pointer to start of index
            * 117 - return the maximum number of DP contact data stored for any element
            * -1 -
            * -2 - superelement flag
            * -3 - master dof bit pattern
            * -4 - active dof bit pattern
            * -5 - solid model attachment
            * -6 - pack nodal line parametric value
            * -7 - constraint bit pattern
            * -8 - force bit pattern
            * -9 - body force bit pattern
            * -10 - internal element flag
            * -11 - orientation element flag =1 is =0 isnot
            * -11 - contact element flag <0
            * -12 - constraint bit pattern (for DSYM)
            * -13 - if dof constraint written to file. (for LSDYNA only)
            * -14 - nodal coordinate system number (set by NROTATE)
            * -101 - pointer to element data record
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
            The returned value of is based on the value of ``ikey``.

        Examples
        --------
        Query if an element is selected.

        >>> from ansys.mapdl.core.database import DBDef
        >>> elems = mapdl.db.elems
        >>> elems.info(1, DBDef.DB_SELECTED)
        1
        """
        if isinstance(ikey, DBDef):
            ikey = ikey.value

        request = mapdl_db_pb2.ElmIqrRequest(ielem=ielm, key=ikey)
        result = self._db._stub.ElmIqr(request)
        return result.elmiqr

    def num(self, selected=False):
        """
        Number of elements.

        Parameters
        ----------
        selected : bool, optional
            Return either the number of selected elements of the total number of
            elements.

        Returns
        -------
        int
            Number of elements. Set ``selected`` to ``True`` to include
            selection status.

        Examples
        --------
        Get the number of selected elements.

        >>> elems = mapdl.db.elems
        >>> elems.num(selected=True)
        425

        """
        if selected:
            return self.info(0, DBDef.DB_NUMSELECTED)
        return self.info(0, DBDef.DB_NUMDEFINED)

    @property
    def max_num(self) -> int:
        """
        Maximum element number.

        Examples
        --------
        Return the maximum element number.

        >>> elems = mapdl.db.elems
        >>> elems.max_num
        64

        """
        return self.info(0, DBDef.DB_MAXDEFINED.value)

    def get(self, ielm):
        """
        Get element attributes and nodes.

        Parameters
        ----------
        ielm : int
            Element number. Should be 0 for key=11 for the following:

        Returns
        -------
        ansys.api.mapdl.v0.mapdl_db_pb2.getelmResponse
            Element information containing the following attributes.

            * ``ielem`` : Element number
            * ``elmdat`` - Element data. Contains:

                * FIELD 0 : material reference number
                * FIELD 1 : element type number
                * FIELD 2 : real constant reference number
                * FIELD 3 : section number
                * FIELD 4 : element coordinate system
                * FIELD 5 : death flag (0 - alive, 1 - dead)
                * FIELD 6 : solid model reference
                * FIELD 7 : coded shape key
                * FIELD 8 : element number
                * FIELD 9 : base element number (applicable to reinforcing elements only)

            * ``nnod`` : Number of nodes
            * ``nodes`` : Node numbers belonging to the element

        Examples
        --------
        Return the element information of element 1.

        >>> elems = mapdl.db.elems
        >>> elem_info = elems.info(1)

        Return the nodes belonging to the element.

        >>> elem_info.nodes
        [2, 27, 37, 8]

        Return the element data.

        >>> elem_info.elmdat
        [1, 1, 1, 1, 0, 0, 14, 0, 0, 0]

        """
        request = mapdl_db_pb2.getelmRequest(ielem=ielm)
        return self._db._stub.getElm(request)

    def push(self, ielm, elmdat, nodes):
        """
        Push an element into the database.

        Examples
        --------
        Push a new linear hexahedron to MAPDL. This assumes that element type 1
        has been set to SOLID185 with ``mapdl.etype(1, "SOLID185")``.

        >>> elems = mapdl.db.elems
        >>> elems.push(
        ...     1,
        ...     [1, 1, 1, 1, 0, 0, 1, 0, 0, 0],
        ...     [1, 2, 3, 4, 5, 6, 7, 8],
        ... )

        """
        if len(elmdat) != 10:
            raise ValueError("`elmdat` must be length 10")
        request = mapdl_db_pb2.putelmRequest(
            ielem=ielm,  # int32
            elmdat=elmdat,  # repeated int32
            nnod=len(nodes),  # int32
            nodes=nodes,  # repeated int32
        )
        self._db._stub.putElm(request)
