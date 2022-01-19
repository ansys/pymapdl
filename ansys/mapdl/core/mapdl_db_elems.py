"""Contains the Elems section of the  MapdlDb class, allowing the access 
to the Elems in the MAPDL DB from Python.  """
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
from ansys.mapdl.core.common_grpc import parse_chunks
from .check_version import version_requires, meets_version, VersionError

class DbElems:
    """Abstract mapdl db elems class.  Created from a ``MapdlDb`` instance.

    Examples
    --------
    Create an instance.

    >>> from ansys.mapdl.core import launch_mapdl
    >>> mapdl = launch_mapdl()
    >>> db = mapdl.db
    >>> elems = db.elems


    """

    def __init__(self, db):
        if not isinstance(db, MapdlDb):
            raise TypeError('``db`` must be a MapdlDb instance')
        self._db_weakref = weakref.ref(db)
        self._itelm = -1

    @property
    def _db(self):
        """Return the weakly referenced instance of db"""
        return self._db_weakref()

    def first(self, ielm=0, defined=False):
        """get the number of the first elem, 
           starting at ielm ( default = first elem in the model)
        By default, we loop over the selected elems. If you wish
        to loop over all defined elems, you need to set defined=True
        
        Parameters
        ----------
        ielm : int, optional
                the last elem number used
                = 0 - use for initial value
        defined : bool, optional
                Set of elems to loop over
                False: loop over selected elems
                True: loop over all defined elems
        Returns
        -------
        first : int
        The first elem number
        = 0 - no elems
        """

        self._itelm = ielm
        if defined:
            return self.next_defined()
        else:
            return self.next()
                
    def next(self):
        """get the number of the next selected elem        
        You first have to call first()
        
        Returns
        -------
        next : int
        The next selected elem number
        = 0 - no more elems
        """

        if self._itelm == -1:
            raise TypeError('``elems.next`` you first have to call first function')

        request = mapdl_db_pb2.ElmRequest( next=self._itelm)
        result = self._db._stub.ElmNext( request)
        self._itelm = result.inum
        return self._itelm

    def next_defined(self):
        """get the number of the next defined elem
        You first have to call first)_

        Returns
        -------
        next_defined : int
        The next defined elem number
        = 0 - no more elems
        """

        if self._itelm == -1:
            raise TypeError('``elems.next`` you first have to call first function')

        request = mapdl_db_pb2.ElmRequest( next=self._itelm)
        result = self._db._stub.ElmNextDefined( request)
        self._itelm = result.inum
        return self._itelm

    def info(self, ind, ikey):
        """get information about a elem

        Parameters
        ind     int       - elem number
                Should be 0 for key=11, DB_NUMDEFINED,
                DB_NUMSELECTED, DB_MAXDEFINED, and
                DB_MAXRECLENG

        ikey    int       - key as to information needed about the node.
                 = DB_SELECTED    - return select status:
                     ndinqr  =  0 - node is undefined.
                             = -1 - node is unselected.
                             =  1 - node is selected.
                 = DB_NUMDEFINED  - return number of defined elems
                 = DB_NUMSELECTED - return number of selected elems
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
        request = mapdl_db_pb2.ElmInqrRequest( node=ind, key=ikey)
        result = self._db._stub.ElmInqr( request)
        inqr = result.ret
        return inqr

    def howmany(self, defined=False):
        if defined:
            return self.info( 0, DBDef.DB_NUMSELECTED);
        else:
            return self.info( 0, DBDef.DB_NUMDEFINED);
    
    def maxnumber(self):
        return self.info( 0, DBDef.DB_MAXDEFINED.value)

    def get( self, iel):
        """get element attributes and nodes 
        
        Parameters
        iel    (int)       - element number
        
        Returns
        -------
        result      (getelmResponse)
                This structure has 4 members:
                  - iel (int) element number
                  - kerr (int) select status
                      = 0 - node is selected
                      = 1 - node is not defined
                      =-1 - node is unselected
                  - v (double[]) Coordinates ( first 3 values) and rotation angles ( last 3 values)
        """
        
        request = mapdl_db_pb2.getelmRequest( ielem=iel)
        result = self._db._stub.getElm( request)
        return result

    def put( self, ielm, x, y, z):
        """push an element into the DB
        
        Parameters
        
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
    
    
