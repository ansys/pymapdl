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
        
        # check is DB Server is running

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
        
        #IpPortString = '0.0.0.0:' + str(iPort)  # need to change to use the real IP Server Adr
        iPort = int(iPort)

        self._ip = '0.0.0.0'
        self._server = {'ip': self._ip, 'port': iPort}
        self._channel_str = '%s:%d' % (self._ip, iPort)
        #self._log.debug('Opening insecure channel at %s', self._channel_str)

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

    def node_next(self, inod=0):
        """get the number of the next selected node
        
        Parameters
        ----------
        inod : int, optional
                the last node number used
                = 0 - use for initial value

        Returns
        -------
        ndnext : int
        The next selected node number
        = 0 - no more nodes
        """

        request = mapdl_db_pb2.NodRequest( next=inod)
        result = self._stub.NodNext( request)
        inum = result.inum
        return inum

    def node_iqr(self, ind, ikey):
        """get information about a node

        Parameters
        ind     int       - node number
                Should be 0 for key=11, DB_NUMDEFINED,
                DB_NUMSELECTED, DB_MAXDEFINED, and
                DB_MAXRECLENG

        ikey    int       - key as to information needed about the node.
                 = DB_SELECTED    - return select status:
                     ndinqr  =  0 - node is undefined.
                             = -1 - node is unselected.
                             =  1 - node is selected.
                 = DB_NUMDEFINED  - return number of defined nodes
                 = DB_NUMSELECTED - return number of selected nodes
                 = DB_MAXDEFINED  - return highest node number defined
                 = DB_MAXRECLENG  - return maximum record length (dp words)
                 =   2, return length (dp words)
                 =   3,
                 =   4, pointer to first data word
                 =  11, return void percent (integer)
                 =  17, pointer to start of index
                 = 117, return the maximum number of DP contact data stored for any node
                 =  -1,
                 =  -2, superelement flag
                 =  -3, master dof bit pattern
                 =  -4, active dof bit pattern
                 =  -5, solid model attachment
                 =  -6, pack nodal line parametric value
                 =  -7, constraint bit pattern
                 =  -8, force bit pattern
                 =  -9, body force bit pattern
                 = -10, internal node flag
                 = -11, orientation node flag =1 is =0 isnot
                 = -11, contact node flag <0
                 = -12, constraint bit pattern (for DSYM)
                 = -13, if dof constraint written to file.k (for LSDYNA only)
                 = -14, nodal coordinate system number (set by NROTATE)
                 =-101, pointer to node data record
                 =-102, pointer to angle record
                 =-103, 
                 =-104, pointer to attached couplings
                 =-105, pointer to attacted constraint equations
                 =-106, pointer to nodal stresses
                 =-107, pointer to specified disp'S
                 =-108, pointer to specified forces
                 =-109, pointer to x/y/z record
                 =-110,
                 =-111,
                 =-112, pointer to nodal temperatures
                 =-113, pointer to nodal heat generations
                 =-114,
                 =-115, pointer to calculated displacements
                 =-116,

        Returns
        -------
        ndinqr : int
        the returned value of ndinqr is based on setting of key
        """
        
        request = mapdl_db_pb2.NodInqrRequest( node=ind, key=ikey)
        result = self._stub.NodInqr( request)
        inqr = result.ret
        return inqr

    def getnod( inod):
        """get a nodal point
        
        Parameters
        inod    (int)       - node number
        
        Returns
        -------
        result      (getnodResponse)
                This structure has two members:
                  - kerr (int) select status
                      = 0 - node is selected
                      = 1 - node is not defined
                      =-1 - node is unselected
                  - v (double[]) Coordinates ( first 3 values) and rotation angles ( last 3 values)
        """
        
        request = mapdl_db_pb2.getnodRequest( node=inod)
        result = self._stub.getNod( request)
        return result
    
    def putnod( inod, x, y, z):
        """Store a node
        
        Parameters
        node    (int)           - node number
        x,y,z   (double)        - nodal coordinates
        
        Returns
        -------
        none
        """
        
        request = mapdl_db_pb2.putnodRequest()
        request.node = inod
        request.vctn.extend( [x])
        request.vctn.extend( [y])
        request.vctn.extend( [z])
        result = self._stub.putNod( request)
        print(".")
        return
    
