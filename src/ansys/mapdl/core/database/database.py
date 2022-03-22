"""Contains the MapdlDb classes, allowing the access to MAPDL DB from Python."""
from enum import Enum
import os
import time
from warnings import warn
import weakref

from ansys.api.mapdl.v0 import mapdl_db_pb2_grpc
import grpc

from ..mapdl_grpc import MapdlGrpc


class WithinBeginLevel:
    """Context manager to run MAPDL within the being level."""

    def __init__(self, mapdl):
        self._mapdl = mapdl

    def __enter__(self):
        self._mapdl._cache_routine()
        if "BEGIN" not in self._mapdl._cached_routine.upper():
            self._mapdl.finish()

    def __exit__(self, type, value, traceback):
        if "BEGIN" not in self._mapdl._cached_routine.upper():
            self._mapdl._resume_routine


class DBDef(Enum):  # From MAPDL ansysdef.inc include file
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
    """Abstract mapdl db class.  Created from a ``Mapdl`` instance.

    Examples
    --------
    Create an instance.

    >>> from ansys.mapdl.core import launch_mapdl
    >>> mapdl = launch_mapdl()
    >>> db = mapdl.db

    Get the number of nodes

    Get a given node

    Set a new node into MAPDL DB

    """

    def __init__(self, mapdl):
        if not isinstance(mapdl, MapdlGrpc):
            raise TypeError("``mapdl`` must be a MapdlGrpc instance")
        self._mapdl_weakref = weakref.ref(mapdl)
        self._stub = None
        self._channel = None
        # self._itele = -1
        self._ip = None
        self._server = {}
        self._channel_str = None
        self._state = None
        self._nodes = None
        self._elems = None

    def __str__(self):
        if self.active:
            return f"MAPDL database server active at {self._channel_str}"
        else:
            return f"MAPDL database server not active"

    @property
    def _mapdl(self):
        """Return the weakly referenced instance of mapdl"""
        return self._mapdl_weakref()

    @property
    def _server_version(self):
        """Return the version of MAPDL"""
        return self._mapdl._server_version

    def _start(self) -> int:
        """Start the database server.

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
        status = self._mapdl._download_as_raw("DBServer.info").decode()

        try:
            # expected of the form 'Port : 50055'
            port = int(status.split(":")[1])
        except Exception as e:  # pragma: no cover
            self._mapdl._log.error(
                "Unable to read port number from '%s' due to\n%s", status, str(e)
            )
            port = 50055

        self._mapdl._log.debug("MAPDL database server started on port %d", port)
        return port

    @property
    def active(self) -> bool:
        """Return if the database server is active."""
        return "NOT" not in self._status()

    def start(self, timeout=10):
        """Start the gRPC MAPDL database server.

        Parameters
        ----------
        timeout : float, optional
            Timeout to start the service.

        Examples
        --------
        >>> db.start()
        """

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
            except ValueError:
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
            raise RuntimeError(
                "Unable to establish connection to MAPDL database server"
            )
        self._mapdl._log.debug("Established connection to MAPDL database server")

    def _stop(self):
        """Stop the MAPDL database service."""
        with WithinBeginLevel(self._mapdl):
            return self._mapdl.run("/DBS,SERVER,STOP")

    def stop(self):
        """Shutdown the MAPDL database service and close the connection.

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
        """Return the status of the MADPL DB Server.

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
        """Load a MAPDL database file in memory.

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
        """Save a MAPDL database to disk.

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
        """Delete everything in the MAPDL DB.

        Examples
        --------
        >>> mapdl.db.clear()
        """
        return self._mapdl.run("/CLEAR,ALL")

    @property
    def nodes(self):
        """MAPDL database nodes interface.

        Returns
        -------
        :class:`DbNodes <ansys.mapdl.core.DbNodes>`

        Examples
        --------
        Get the number of nodes in the MAPDL DB

        >>> db = mapdl.db
        >>> nodes = db.nodes
        >>> nodes.num()

        Push a new node into MAPDL

        >>> nodes.set(...)
        >>>
        """
        if self._nodes is None:
            from .nodes import DbNodes  # here to avoid circular import

            self._nodes = DbNodes(self)
        return self._nodes

    @property
    def elems(self):
        """MAPDL database element interface.

        Returns
        -------
        :class:`DbElems <ansys.mapdl.core.DbElems>`

        Examples
        --------
        Get the number of elems in the MAPDL DB

        >>> db = mapdl.db
        >>> elems = db.elems
        >>> elems.num()

        Push a new elem into MAPDL

        >>> elems.set(...)
        >>>
        """
        if self._elems is None:
            from .elems import DbElems  # here to avoid circular import

            self._elems = DbElems(self)
        return self._elems
