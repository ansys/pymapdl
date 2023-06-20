"""Contains the MapdlDb classes, allowing the access to MAPDL DB from Python."""
from enum import Enum
from functools import wraps
import os
import time
from warnings import warn
import weakref

from ansys.api.mapdl.v0 import mapdl_db_pb2_grpc
from ansys.tools.versioning import server_meets_version
import grpc

from ansys.mapdl.core.errors import MapdlConnectionError

from ..mapdl_grpc import MapdlGrpc

MINIMUM_MAPDL_VERSION = "21.1"


class WithinBeginLevel:

    """Context manager to run MAPDL within the being level."""

    def __init__(self, mapdl):
        """Initialize this context manager."""
        self._mapdl = mapdl

    def __enter__(self):
        """Enter the begin level and cache the current routine."""
        self._mapdl._cache_routine()
        if "BEGIN" not in self._mapdl._cached_routine.upper():
            self._mapdl.finish()

    def __exit__(self, *args, **kwargs):
        """Exit the begin level and reload the previous routine."""
        if "BEGIN" not in self._mapdl._cached_routine.upper():
            self._mapdl._resume_routine()


def check_mapdl_db_is_alive(function):
    """
    Decorator to check that the MAPDL.DB has started.

    It works for the DB object (DBDef) and for the derived object which has "_db" attribute.
    """

    @wraps(function)
    def wrapper(self, *args, **kwargs):
        if hasattr(self, "active"):
            active = self.active
        elif hasattr(self, "_db"):
            active = self._db.active
        else:  # pragma: no cover
            raise Exception("The DB object could not be found.")

        if not active:
            self._mapdl._log.error(
                f"Please start the MAPDL DB Server to access '{function.__name__}'."
            )
            return None
        return function(self, *args, **kwargs)

    return wrapper


class DBDef(Enum):  # From MAPDL ansysdef.inc include file

    """Database type definitions."""

    DB_SELECTED = 1
    DB_NUMDEFINED = 12
    DB_NUMSELECTED = 13
    DB_MAXDEFINED = 14
    DB_MAXRECLENG = 15
    DB_GETNEXTRECD = 16
    DB_MAXALLOC = 17
    DB_OBJFLAG = -777
    DB_NEXT = -888
    DB_NEXT_ALLOC = -889
    DB_MODIFIED = -999
    DB_INTERNAL = -9999


class MapdlDb:

    """
    Abstract mapdl database class.  Created from a ``Mapdl`` instance.

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

    """

    def __init__(self, mapdl):
        """Initialize this class."""
        if not isinstance(mapdl, MapdlGrpc):  # pragma: no cover
            raise TypeError("``mapdl`` must be a MapdlGrpc instance")
        self._mapdl_weakref = weakref.ref(mapdl)
        self._stub = None
        self._channel = None
        self._ip = None
        self._server = {}
        self._channel_str = None
        self._state = None
        self._nodes = None
        self._elems = None

    def __str__(self):
        """Return the string representation of this class."""
        if self.active:
            return f"MAPDL database server active at {self._channel_str}"
        return f"MAPDL database server not active"

    @property
    def _mapdl(self):
        """Return the weakly referenced instance of mapdl."""
        return self._mapdl_weakref()

    def _start(self) -> int:
        """
        Lower level start of the database server.

        Returns
        -------
        int
            Port of the database server.

        """
        self._mapdl._log.debug("Starting MAPDL server")

        # database server must be run from the "BEGIN" level
        self._mapdl._cache_routine()
        with WithinBeginLevel(self._mapdl):
            self._mapdl.run("/DBS,SERVER,START")

        # Scan the DBServer.info file to get the Port Number

        # Default is 50055
        # wait for start
        tstart = time.time()
        timeout = 1
        status = self._mapdl._download_as_raw("DBServer.info").decode()
        while status == "":  # pragma: no cover
            status = self._mapdl._download_as_raw("DBServer.info").decode()
            time.sleep(0.05)
            if time.time() - tstart > timeout:
                raise TimeoutError(
                    f"Unable to start database server in {timeout} second(s)"
                )

        try:
            # expected of the form 'Port : 50055'
            port = int(status.split(":")[1])
        except Exception as e:  # pragma: no cover
            self._mapdl._log.error(
                "Unable to read port number from '%s' due to\n%s",
                status,
                str(e),
            )
            port = 50055

        self._mapdl._log.debug("MAPDL database server started on port %d", port)
        return port

    @property
    def active(self) -> bool:
        """Return if the database server is active."""
        return "NOT" not in self._status()

    def start(self, timeout=10):
        """
        Start the gRPC MAPDL database server.

        Parameters
        ----------
        timeout : float, optional
            Timeout to start the service.

        Examples
        --------
        >>> mapdl.db.start()
        """
        # checking MAPDL API
        from ansys.api.mapdl import __version__ as api_version

        api_version = tuple(int(each) for each in api_version.split("."))

        if api_version < (0, 5, 1):  # pragma: no cover
            raise ImportError(
                "Please upgrade the 'ansys.api.mapdl' package to at least v0.5.1."
                "You can use 'pip install ansys-api-mapdl --upgrade"
            )

        ## Checking MAPDL versions
        mapdl_version = self._mapdl.version
        if not server_meets_version(
            str(mapdl_version), MINIMUM_MAPDL_VERSION
        ):  # pragma: no cover
            from ansys.mapdl.core.errors import MapdlVersionError

            raise MapdlVersionError(
                f"This MAPDL version ({mapdl_version}) is not compatible with the Database module."
                "Please check the online documentation regarding Database Module at 'mapdl.docs.pyansys.com'."
            )

        if self._mapdl._server_version < (0, 4, 1):
            from ansys.mapdl.core.errors import MapdlVersionError

            ver_ = ".".join([str(each) for each in self._mapdl._server_version])
            raise MapdlVersionError(
                f"This version of MAPDL gRPC API version ('ansys.api.mapdl' == {ver_}) is not compatible with 'database' module.\n"
                "Please check the online documentation at 'mapdl.docs.pyansys.com' "
            )

        # only start if not already running
        is_running = self.active
        self._mapdl._log.debug("MAPDL DB server running: %s", str(is_running))
        if is_running:
            return
        db_port = self._start()

        self._ip = self._mapdl._ip

        # permit overriding db_port via env var for CI
        if "PYMAPDL_DB_PORT" in os.environ:
            db_port_str = os.environ.get("PYMAPDL_DB_PORT")
            try:
                db_port = int(db_port_str)
            except ValueError:  # pragma: no cover
                raise ValueError(
                    f"Invalid port '{db_port_str}' specified in the env var PYMAPDL_DB_PORT"
                )

        self._server = {"ip": self._ip, "port": db_port}
        self._channel_str = f"{self._ip}:{db_port}"

        self._channel = grpc.insecure_channel(self._channel_str)
        self._state = grpc.channel_ready_future(self._channel)
        self._stub = mapdl_db_pb2_grpc.MapdlDbServiceStub(self._channel)

        # wait until the channel matures
        tstart = time.time()
        while ((time.time() - tstart) < timeout) and not self._state._matured:
            time.sleep(0.01)

        if not self._state._matured:  # pragma: no cover
            raise MapdlConnectionError(
                "Unable to establish connection to MAPDL database server"
            )
        self._mapdl._log.debug("Established connection to MAPDL database server")

    def _stop(self):
        """Stop the MAPDL database service."""
        with WithinBeginLevel(self._mapdl):
            return self._mapdl.run("/DBS,SERVER,STOP")

    def stop(self):
        """
        Shutdown the MAPDL database service and close the connection.

        Examples
        --------
        Stop the database service.

        >>> mapdl.db.stop()
        """
        if not self.active:
            warn("Server is already shutdown")
            return

        self._mapdl._log.debug("Closing the connection with the MAPDL DB Server")
        self._stop()
        self._channel.close()
        self._channel = None
        self._stub = None
        self._state = None

    def _status(self):
        """
        Return the status of the MADPL DB Server.

        Examples
        --------
        >>> output = mapdl.db._status()
        >>> print(output)
        >ENTERING THE SERVER MODE: STATUS

         DB Server is NOT currently running ..
        """
        # Need to use the health check here
        with WithinBeginLevel(self._mapdl):
            return self._mapdl.run("/DBS,SERVER,STATUS")

    def load(self, fname, progress_bar=False):
        """
        Load a MAPDL database file in memory.

        Parameters
        ----------
        fname : str
            The file name of the database to load.

        Examples
        --------
        >>> mapdl.db.load('file.db')
        """
        self._mapdl._get_file_path(fname, progress_bar=progress_bar)
        return self._mapdl.resume(fname)

    def save(self, fname, option="ALL"):
        """
        Save the MAPDL database to disk.

        Parameters
        ----------
        fname : str
            Filename to save the database to.

        option : str
            The mode for saving the database, either:

            * "ALL" - Both the model and the solution
            * "MODEL" - Just the model
            * "SOLU" - Just the solution

        Examples
        --------
        >>> mapdl.db.save('model.db', option=)
        """
        allowed = ["ALL", "MODEL", "SOLU"]
        if option.upper() not in allowed:
            raise ValueError(f"Option must be one of the following: {allowed}")

        return self._mapdl.run(f"SAVE,{fname},,,{option}")

    def clear(self, **kwargs):
        """
        Delete everything in the MAPDL database.

        Examples
        --------
        >>> mapdl.db.clear()
        """
        return self._mapdl.run("/CLEAR,ALL")

    @property
    @check_mapdl_db_is_alive
    def nodes(self):
        """
        MAPDL database nodes interface.

        Returns
        -------
        :class:`DbNodes <ansys.mapdl.core.database.nodes.DbNodes>`

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
        if self._nodes is None:
            from .nodes import DbNodes  # here to avoid circular import

            self._nodes = DbNodes(self)
        return self._nodes

    @property
    @check_mapdl_db_is_alive
    def elems(self):
        """
        MAPDL database element interface.

        Returns
        -------
        :class:`DbElems <ansys.mapdl.core.database.elems.DbElems>`

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
        if self._elems is None:
            from .elems import DbElems  # here to avoid circular import

            self._elems = DbElems(self)
        return self._elems
