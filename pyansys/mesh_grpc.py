"""Module to manage downloading and parsing geometry from the MAPDL grpc server"""
import numpy as np

from pyansys.misc import threaded
from pyansys.geometry import Geometry
from pyansys.mapdl_grpc import MapdlGrpc
from pyansys.common_grpc import (parse_chunks,
                                 ANSYS_VALUE_TYPE,
                                 DEFAULT_CHUNKSIZE,
                                 DEFAULT_FILE_CHUNK_SIZE)

from ansys.grpc.mapdl import mapdl_pb2 as pb_types
from ansys.grpc.mapdl import mapdl_pb2_grpc as mapdl_grpc
from ansys.grpc.mapdl import ansys_kernel_pb2 as anskernel


class MeshGrpc(Geometry):

    def __init__(self, mapdl):
        """Initialize grpc geometry data"""
        super().__init__()
        if not isinstance(mapdl, MapdlGrpc):
            raise TypeError('Must be initialized using MapdlGrpc class')
        self._mapdl = mapdl

        # allow default chunk_size to be overridden
        self._chunk_size = None

        # local cache
        self._cache_nnum = None
        self._cache_elem = None
        self._cache_elem_off = None
        self._cache_element_desc = None
        self._grid_cache = None

    def _reset_cache(self):
        """Reset any geometry cache"""
        self._node_coord = None
        self._nnum = None
        self._elem = None
        self._elem_off = None
        self._ekey = None
        self._grid = None
        self._node_angles = None
        self._enum = None

    def _update_cache(self):
        """Threaded local cache update.

        Used when needing all the geometry entries from MAPDL
        """
        threads = [self._update_cache_elem(),
                   self._update_cache_element_desc(),
                   self._update_cache_nnum(),
                   self._update_node_coord()]

        for thread in threads:
            thread.join()

    @property
    def n_node(self):
        """Number of currently selected nodes in MAPDL"""
        return int(self._mapdl._get('NODE, , COUNT'))

    @property
    def n_elem(self):
        """Number of currently selected nodes in MAPDL"""
        return int(self._mapdl._get('ELEM, , COUNT'))

    @property
    def node_angles(self):
        """Not yet implemented"""
        return

    @threaded
    def _update_cache_nnum(self):
        if self._cache_nnum is None:
            self._cache_nnum = self._mapdl.vget('NODE', 'NLIST').astype(np.int32)

    @property
    def _nnum(self):
        self._update_cache_nnum().join()
        return self._cache_nnum

    @_nnum.setter
    def _nnum(self, value):
        self._cache_nnum = value

    @threaded
    def _update_cache_element_desc(self):
        if self._cache_element_desc is None:
            self._cache_element_desc = self._load_element_types()

    @property
    def _ekey(self):
        """Element key description"""
        self._update_cache_element_desc().join()

        # convert to ekey format
        ekey = [einfo[:2] for einfo in self._cache_element_desc]
        return np.vstack(ekey).astype(np.int32)

    @_ekey.setter
    def _ekey(self, value):
        self._cache_element_desc = value

    @threaded
    def _update_node_coord(self):
        if self._node_coord is None:
            self._node_coord = self._load_nodes()

    @property
    def nodes(self):
        """Array of nodes.

        Examples
        --------
        >>> mapdl.mesh.nodes
        [[0.   0.   0.  ]
         [1.   0.   0.  ]
         [0.25 0.   0.  ]
         ...,
         [0.75 0.5  3.5 ]
         [0.75 0.5  4.  ]
         [0.75 0.5  4.5 ]]
        """
        self._update_node_coord().join()
        return self._node_coord

    def _load_nodes(self, chunk_size=DEFAULT_CHUNKSIZE):
        """Loads nodes from server.

        Parameters
        ----------
        chunk_size : int
            Size of the chunks to request from the server.  Default
            256 kB

        Returns
        -------
        nodes : np.ndarray
            Numpy array of nodes
        """
        if self._chunk_size:
            chunk_size = self._chunk_size

        request = anskernel.StreamRequest(chunk_size=chunk_size)
        chunks = self._mapdl._stub.Nodes(request)
        nodes = parse_chunks(chunks, np.double).reshape(-1, 3)
        return nodes

    @threaded
    def _update_cache_elem(self):
        """Update the element and element offset cache"""
        if self._cache_elem is None:
            self._cache_elem, self._cache_elem_off = self._load_elements_offset()

    @property
    def _elem(self):
        """Contingious array of elements.

        Array of elements, with each element starting at the indices
        in offset.  Each element contains 10 items plus the nodes
        belonging to the element.
        """
        self._update_cache_elem().join()
        return self._cache_elem

    @_elem.setter
    def _elem(self, value):
        self._cache_elem = value

    @property
    def _elem_off(self):
        """Element offset array"""
        self._update_cache_elem().join()
        return self._cache_elem_off

    @_elem_off.setter
    def _elem_off(self, value):
        self._cache_elem_off = value

    def _load_elements_offset(self, chunk_size=DEFAULT_CHUNKSIZE):
        """Loads elements from server

        Parameters
        ----------
        chunk_size : int, optional
            Size of the chunks to request from the server.

        Returns
        -------
        elements : np.ndarray
            Array of elements, with each element starting at the
            indices in offset.  Each element contains 10 items plus
            the nodes belonging to the element.  The first 10 items
            are:

            mat    - material reference number
            type   - element type number
            real   - real constant reference number
            secnum - section number
            esys   - element coordinate system
            death  - death flag (0 - alive, 1 - dead)
            solidm - solid model reference
            shape  - coded shape key
            elnum  - element number
            baseeid- base element number (applicable to reinforcing
                     elements only)
            nodes  - The nodes belonging to the elementoffset

        offset : np.ndarray
            Array of indices indicating the start of each element.

        """
        if self._chunk_size:
            chunk_size = self._chunk_size

        request = anskernel.StreamRequest(chunk_size=chunk_size)
        chunks = self._mapdl._stub.LoadElements(request)
        elem_raw = parse_chunks(chunks, np.int32)
        n_elem = elem_raw[0]

        # TODO: arrays from gRPC interface should include size of the elem array
        lst_value = np.array(elem_raw.size - n_elem, np.int32)
        offset = np.hstack((elem_raw[:n_elem] - n_elem, lst_value))
        return elem_raw[n_elem:], offset

    def _load_element_types(self, chunk_size=DEFAULT_CHUNKSIZE):
        """Loads element types from the MAPDL server.

        Returns
        -------
        element_types : np.ndarray
            Array of numpy element types.

        Parameters
        ----------
        chunk_size : int
            Size of the chunks to request from the server.
        """
        request = anskernel.StreamRequest(chunk_size=chunk_size)
        chunks = self._mapdl._stub.LoadElementTypeDescription(request)
        data = parse_chunks(chunks, np.int32)
        n_items = data[0]
        split_ind = data[1:1 + n_items]
        return np.split(data, split_ind)[1:]

    @property
    def _grid(self):
        if self._grid_cache is None:
            self._update_cache()
            self._grid_cache = self._parse_vtk()
        return self._grid_cache

    @_grid.setter
    def _grid(self, value):
        self._grid_cache = value

    def __repr__(self):  # TODO
        return ""

    def __str__(self):  # TODO
        return ""
