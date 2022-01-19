"""Contains the MapdlDb classes, allowing the access to MAPDL DB
from Python.  """
import grpc
import os
import weakref
import string
import random
from enum import Enum

import numpy as np
from ansys.grpc.mapdl import ansys_kernel_pb2 as anskernel
from ansys.grpc.mapdl import mapdl_pb2 as pb_types

from ansys.mapdl.core import mapdl_db_pb2_grpc
from ansys.mapdl.core import mapdl_db_pb2

from .errors import ANSYSDataTypeError, protect_grpc
from .mapdl_grpc import MapdlGrpc
from .common_grpc import (ANSYS_VALUE_TYPE, DEFAULT_CHUNKSIZE,
                          DEFAULT_FILE_CHUNK_SIZE)
from .check_version import version_requires, meets_version, VersionError

class DBDef(Enum):             # From MAPDL ansysdef.inc include file
    DB_SELECTED    =  1
    DB_NUMDEFINED  =  12
    DB_NUMSELECTED =  13
    DB_MAXDEFINED  =  14
    DB_MAXRECLENG  =  15
    DB_GETNEXTRECD =  16
    DB_MAXALLOC    =  17
    DB_OBJFLAG     = -777
    DB_NEXT        = -888
    DB_NEXT_ALLOC  = -889
    DB_MODIFIED    = -999
    DB_INTERNAL    = -9999

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
            raise TypeError('``mapdl`` must be a MapdlGrpc instance')
        self._mapdl_weakref = weakref.ref(mapdl)
        self._stub = None
        self._channel = None
        self._itele = -1

    @property
    def _mapdl(self):
        """Return the weakly referenced instance of mapdl"""
        return self._mapdl_weakref()
    
    @property
    def _server_version(self):
        """Return the version of MAPDL"""
        return self._mapdl._server_version

    def start(self):
        """Start the gRPC MAPDL DB Server

        Examples
        --------
        >>> db.start()
        """

        # check if DB Server is running

        IsRunning = self._mapdl.run("/DBS,SERVER,STATUS")
        if (IsRunning.find('NOT') != -1):
            print(self._mapdl.run("/DBS,SERVER,START"))
        else:
            print(">> MAPDL DB Server is already running.")
        
        # Scan the DBServer.info file to get the Port Number
        # Default is 50055

        self._mapdl.download( 'DBServer.info', progress_bar=False)

        iPort = '50055'         # Default Port Number Value

        try:
            with open( 'DBServer.info', 'rt') as f:
                for line in f:
                    if line.startswith('Port'):
                        iPort = line[-5:]
                        break
        except IOError:
            iPort = '50055'         # useless, but for clarity
        
        iPort = int(iPort)

        self._ip = self._mapdl._ip
        self._server = {'ip': self._ip, 'port': iPort}
        self._channel_str = '%s:%d' % (self._ip, iPort)

        self._channel = grpc.insecure_channel(self._channel_str)
        self._state = grpc.channel_ready_future(self._channel)
        self._stub = mapdl_db_pb2_grpc.MapdlDbServiceStub(self._channel)
                
        print('>> MAPDL DB Server started on Port : ' + str(iPort))
        return

    def stop( self, server=False):
        """Shutdown the MAPDL DB Client

        Parameters
        ----------

        server: bool, optional
            Shutdown the MAPDL DB Server. Default is ``False``

        Examples
        --------
        >>> db.stop()
        """

        if server:
            # Shutdown the MAPDL DB Server            
            print(self._mapdl.run("/DBS,SERVER,STOP"))
            
        if self._channel != 0:
            print( ">> Shutdown the connection with the MAPDL DB Server")
            self._channel.close()
            self._channel = 0
            self._stub = 0            
        else:
            print( ">> MAPDL DB Client is not active. Command is ignored.")
            
        return

    def status(self):
        """Print out the status of the MADPL DB Server

        Examples
        --------
        >>> db.status()
        >>> Bla Bla Bla
        >>> Bla Bla Bla
        >>> ....
        """
        # Need to use the health check here
        
        return self._mapdl.run("/DBS,SERVER,STATUS")
                
    def load(self, fname):
        """Load a DB File in memory

        Parameters

        fname : str
                The file name we want to create

        Example
        --------
        >>> db.load('file.db')
        """

        self._mapdl.upload( fname, progress_bar=False)
        print(self._mapdl.run("resume," + fname, mute=False))
        return

    def save(self, fname, option='ALL'):
        """Save DB to a File

        Parameters

        fname : str
                The file name we want to create

        option : str
                The mode for saving the database (ALL,MODEL,SOLU)

        Example
        --------
        >>> db.save('model.db')
        """

        print(self._mapdl.run("save," + fname + ",,," + option, mute=False))
        return
    
    def clear(self):
        """Delete everything in the MAPDL DB

        Examples
        --------
        >>> db.clear()
        """
        print(self._mapdl.run("/CLEAR,ALL", mute=False))
        return

    @property
    def nodes(self):
        """DB Nodes interface

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
        
        from ansys.mapdl.core.mapdl_db_nodes import DbNodes
        return DbNodes(self)

    @property
    def elems(self):
        """DB Elems interface

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
        
        from ansys.mapdl.core.mapdl_db_elems import DbElems
        return DbElems(self)
    
