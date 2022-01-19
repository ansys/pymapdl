"""Contains the Node section of the  MapdlDb class, allowing the access 
to the Nodes in the MAPDL DB from Python.  """
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
from .mapdl_db import MapdlDb, DBDef
from .common_grpc import (ANSYS_VALUE_TYPE, DEFAULT_CHUNKSIZE,
                          DEFAULT_FILE_CHUNK_SIZE)
from .common_grpc import parse_chunks
from .check_version import version_requires, meets_version, VersionError

class DbNodes:
    """Abstract mapdl db nodes class.  Created from a ``MapdlDb`` instance.

    Examples
    --------
    Create an instance.

    >>> from ansys.mapdl.core import launch_mapdl
    >>> mapdl = launch_mapdl()
    >>> db = mapdl.db
    >>> nodes = db.nodes


    """

    def __init__(self, db):
        if not isinstance(db, MapdlDb):
            raise TypeError('``db`` must be a MapdlDb instance')
        self._db_weakref = weakref.ref(db)
        self._itnod = -1

    @property
    def _db(self):
        """Return the weakly referenced instance of db"""
        return self._db_weakref()

    def first(self, inod=0, defined=False):
        """get the number of the first node, 
           starting at inod ( default = first  node in the model)
        By default, we loop over the selected nodes. If you wish
        to loop over all defined nodes, you need to set defined=True
        
        Parameters
        ----------
        inod : int, optional
                the last node number used
                = 0 - use for initial value
        defined : bool, optional
                Set of nodes to loop over
                False: loop over selected nodes
                True: loop over all defined nodes
        Returns
        -------
        first : int
        The first node number
        = 0 - no nodes
        """

        self._itnod = inod
        if defined:
            return self.next_defined()
        else:
            return self.next()
                
    def next(self):
        """get the number of the next selected node        
        You first have to call first()
        
        Returns
        -------
        next : int
        The next selected node number
        = 0 - no more nodes
        """

        if self._itnod == -1:
            raise TypeError('``db.next_node`` you first have to call first_node function')

        request = mapdl_db_pb2.NodRequest( next=self._itnod)
        result = self._db._stub.NodNext( request)
        self._itnod = result.inum
        return self._itnod

    def next_defined(self):
        """get the number of the next defined node
        You first have to call first)_

        Returns
        -------
        next_defined : int
        The next defined node number
        = 0 - no more nodes
        """

        if self._itnod == -1:
            raise TypeError('``db.next_node`` you first have to call first_node function')

        request = mapdl_db_pb2.NodRequest( next=self._itnod)
        result = self._db._stub.NodNextDefined( request)
        self._itnod = result.inum
        return self._itnod

    def info(self, ind, ikey):
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
        info : int
        the returned value of info_node is based on setting of key
        """        
        request = mapdl_db_pb2.NodInqrRequest( node=ind, key=ikey)
        result = self._db._stub.NodInqr( request)
        inqr = result.ret
        return inqr

    def howmany(self, defined=False):
        if defined:
            return self.info( 0, DBDef.DB_NUMSELECTED.value)
        else:
            return self.info( 0, DBDef.DB_NUMDEFINED.value)

    def maxnumber(self):
        return self.info( 0, DBDef.DB_MAXDEFINED.value)
    
    def get( self, inod):
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
        result = self._db._stub.getNod( request)
        return result

    def get_all( self):
        request = anskernel.EmptyRequest()
        stream = self._db._stub.getAllNod( request)
        nodes = []
        for nod in stream:
            nodes.append(nod.v)
        return nodes

    def get_all_asarray( self):
        chunk_size = DEFAULT_CHUNKSIZE
        metadata = [('chunk_size', str(chunk_size))]
        request = anskernel.EmptyRequest()
        chunks = self._db._stub.getAllNodC( request, metadata=metadata)
        nodes = parse_chunks(chunks, np.int32).reshape(-1, 7)
        nodes_nb = nodes[:, 0]
        nodes = np.delete( nodes, 0, 1)
        coords = np.frombuffer(nodes,np.double).reshape(-1,3)
        return coords, nodes_nb;
        
    def put( self, inod, x, y, z):
        """push a node into the DB
        
        Parameters
        inod    (int)           - node number
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
        result = self._db._stub.putNod( request)
        return
    
    def _select( self, inod, sel=1):
        """select/unselect/delete a node in the DB
        
        Parameters
        inod    (int) - node number
        sel     (int) - action to take:
                        0: delete the node
                        1: select a node
                       -1: unselect a node
                        2: switch the exist select status        
        Returns
        -------
        none
        """
        
        request = mapdl_db_pb2.NodSelRequest( inum=inod, ksel=sel)
        self._db._stub.NodSel( request)
        return

    def delete( self, inod):
        """delete a node from the DB
        
        Parameters
        inod    (int)           - node number
        
        Returns
        -------
        none
        """
        return self._select( inod, 0)

    def select( self, inod):
        """select a node in the DB
        
        Parameters
        inod    (int)           - node number
        
        Returns
        -------
        none
        """
        return self._select( inod, 1)

    def unselect( self, inod):
        """unselect a node in the DB
        
        Parameters
        inod    (int)           - node number
        
        Returns
        -------
        none
        """
        return self._select( inod, -1)

    def invselect( self, inod):
        """inverse the select status of a node in the DB
        
        Parameters
        inod    (int)           - node number
        
        Returns
        -------
        none
        """
        return self._select( inod, 2)
