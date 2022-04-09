"""Module to manage downloading and parsing the FEM from the MAPDL gRPC server."""
import os
import time
import weakref

from ansys.api.mapdl.v0 import ansys_kernel_pb2 as anskernel
from ansys.mapdl.reader.mesh import Mesh
import numpy as np

from ansys.mapdl.core.common_grpc import DEFAULT_CHUNKSIZE, parse_chunks
from ansys.mapdl.core.mapdl_grpc import MapdlGrpc
from ansys.mapdl.core.misc import supress_logging, threaded

TMP_NODE_CM = "__NODE__"


class MeshGrpc(Mesh):
    """Provides an interface to the gRPC mesh from MAPDL."""

    def __init__(self, mapdl):
        """Initialize grpc geometry data"""
        super().__init__()
        if not isinstance(mapdl, MapdlGrpc):  # pragma: no cover
            raise TypeError("Must be initialized using MapdlGrpc class")
        self._mapdl_weakref = weakref.ref(mapdl)

        # allow default chunk_size to be overridden
        self._chunk_size = None

        # local cache
        self._surf_cache = None
        self._cache_nnum = None
        self._cache_elem = None
        self._cache_elem_off = None
        self._cache_element_desc = None
        self._grid_cache = None
        self._log = self._mapdl._log
        self._ignore_cache_reset = False

    @property
    def _mapdl(self):
        """Return the weakly referenced instance of mapdl"""
        return self._mapdl_weakref()

    def _set_log_level(self, level):
        """Wraps set_log_level"""
        self._mapdl._set_log_level(level)

    def _reset_cache(self):
        """Reset entire mesh cache"""
        if not self._ignore_cache_reset:
            self._cache_nnum = None
            self._cache_elem = None
            self._cache_elem_off = None
            self._cache_element_desc = None
            self._grid_cache = None
            self._surf_cache = None
            self._cached_elements = None

            self._node_coord = None
            self._enum = None
            self._nnum = None
            self._elem = None
            self._elem_off = None
            self._grid = None
            self._node_angles = None
            self._enum = None
            self._rcon = None
            self._mtype = None
            self._etype_cache = None
            self._etype = None
            self._keyopt = None

    def _update_cache(self):
        """Threaded local cache update.

        Used when needing all the geometry entries from MAPDL.
        """
        # elements must have their underlying nodes selected to avoid
        # VTK segfault
        self._mapdl.cm(TMP_NODE_CM, "NODE", mute=True)
        self._mapdl.nsle("S", mute=True)

        # not thread safe
        self._update_cache_elem().join()

        threads = [
            self._update_cache_element_desc(),
            self._update_cache_nnum(),
            self._update_node_coord(),
        ]

        for thread in threads:
            thread.join()

        # must occur after read
        self._ignore_cache_reset = True

        # somehow requesting path seems to help windows avoid an
        # outright segfault prior to running CMSEL
        if os.name == "nt":
            _ = self._mapdl.path

        # TODO: flaky
        time.sleep(0.05)
        self._mapdl.cmsel("S", TMP_NODE_CM, "NODE", mute=True)
        self._ignore_cache_reset = False

    @property
    def nnum(self) -> np.ndarray:
        """Array of currently selected node numbers.

        Examples
        --------
        >>> mapdl.mesh.nnum
        array([    1,     2,     3, ..., 19998, 19999, 20000])
        """
        return self._nnum

    @property
    def nnum_all(self) -> np.ndarray:
        """Array of all node numbers, even those not selected.

        Examples
        --------
        >>> mapdl.mesh.nnum_all
        array([    1,     2,     3, ..., 19998, 19999, 20000])
        """
        self._ignore_cache_reset = True
        self._mapdl.cm(TMP_NODE_CM, "NODE", mute=True)
        self._mapdl.nsel("all", mute=True)

        nnum = self._mapdl.get_array("NODE", item1="NLIST")
        nnum = nnum.astype(np.int32)
        if nnum.size == 1:
            if nnum[0] == 0:
                nnum = np.empty(0, np.int32)

        self._mapdl.cmsel("S", TMP_NODE_CM, "NODE", mute=True)
        self._ignore_cache_reset = False

        return nnum

    @property
    def enum_all(self) -> np.ndarray:
        """Array of all element numbers, even those not selected.

        Examples
        --------
        >>> mapdl.mesh.enum_all
        array([    1,     2,     3, ..., 19998, 19999, 20000])
        """
        self._ignore_cache_reset = True
        self._mapdl.cm("__ELEM__", "ELEM", mute=True)
        self._mapdl.esel("all", mute=True)

        enum = self._mapdl.get_array("ELEM", item1="ELIST")
        enum = enum.astype(np.int32)
        if enum.size == 1:
            if enum[0] == 0:
                enum = np.empty(0, np.int32)

        self._mapdl.cmsel("S", "__ELEM__", "ELEM", mute=True)
        self._ignore_cache_reset = False

        return enum

    @property
    @supress_logging
    def n_node(self) -> int:
        """Number of currently selected nodes in MAPDL.

        Examples
        --------
        >>> mapdl.mesh.n_node
        7217
        """
        return int(self._mapdl.get(entity="NODE", item1="COUNT"))

    @property
    @supress_logging
    def n_elem(self) -> int:
        """Number of currently selected elements in MAPDL.

        Examples
        --------
        >>> mapdl.mesh.n_elem
        1520
        """
        return int(self._mapdl.get(entity="ELEM", item1="COUNT"))

    @property
    def node_angles(self):
        """Not yet implemented"""
        return

    @property
    def enum(self) -> np.ndarray:
        """Element numbers of currently selected elements

        Examples
        --------
        >>> mapdl.mesh.enum
        array([    1,     2,     3, ...,  9998,  9999, 10000])
        """
        if self._enum is None:
            if self._mapdl.mesh.n_elem == 0:
                return np.array([], dtype=np.int32)
            else:
                self._enum = self._mapdl.get_array("ELEM", item1="ELIST").astype(
                    np.int32
                )
        return self._enum

    @threaded
    def _update_cache_nnum(self):
        if self._cache_nnum is None:
            nnum = self._mapdl.get_array("NODE", item1="NLIST")
            self._cache_nnum = nnum.astype(np.int32)
        if self._cache_nnum.size == 1:
            if self._cache_nnum[0] == 0:
                self._cache_nnum = np.empty(0, np.int32)

    @property
    def _nnum(self):
        """Return node number cache"""
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
    def key_option(self):
        """Key options of selected element types."""
        self._update_cache_element_desc().join()

        key_opt = {}
        for einfo in self._cache_element_desc:
            keyopt = einfo[2:20]
            if keyopt.any():
                # convert to fortran/ANSYS format
                valid_keyopt = keyopt[keyopt.astype(np.bool)]
                ans_keyopt = np.vstack((np.nonzero(keyopt)[0] + 1, valid_keyopt))
                key_opt[einfo[0]] = ans_keyopt.T.tolist()

        return key_opt

    @property
    def _ekey(self):
        """Element key description"""
        self._update_cache_element_desc().join()

        # convert to ekey format
        if self._cache_element_desc:
            ekey = []
            for einfo in self._cache_element_desc:
                ekey.append(einfo[:2])
            return np.vstack(ekey).astype(np.int32)
        return []

    @_ekey.setter
    def _ekey(self, value):
        self._cache_element_desc = value

    @threaded
    def _update_node_coord(self):
        if self._node_coord is None:
            self._node_coord = self._load_nodes()

    @property
    def nodes(self) -> np.ndarray:
        """Array of nodes.

        Examples
        --------
        >>> mapdl.mesh.nodes
        array([[0.   0.   0.  ]
               [1.   0.   0.  ]
               [0.25 0.   0.  ]
               ...,
               [0.75 0.5  3.5 ]
               [0.75 0.5  4.  ]
               [0.75 0.5  4.5 ]]
        """
        self._update_node_coord().join()
        if self._node_coord is None:
            return np.empty(0)
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

        # ignore zeros
        elem_off_raw = elem_raw[:n_elem]
        elem_off_raw = elem_off_raw[elem_off_raw != 0]
        # TODO: arrays from gRPC interface should include size of the elem array
        lst_value = np.array(elem_raw.size - n_elem, np.int32)
        offset = np.hstack((elem_off_raw - n_elem, lst_value))

        # overwriting the last column to include element numbers
        elems_ = elem_raw.copy()  # elem_raw is only-read
        elems_ = elems_[n_elem:]
        indx_elem = offset[:-1] + 8  # Getting index of the second EL_SHAPE column
        elems_[indx_elem] = self.enum
        return elems_, offset

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
        split_ind = data[1 : 1 + n_items]
        # empty items sometimes...
        split_ind = split_ind[split_ind != 0]
        return np.split(data, split_ind)[1:]

    @property
    def grid(self):
        """VTK representation of the underlying finite element mesh.

        Examples
        --------
        Store the finite element mesh as a VTK UnstructuredGrid.

        >>> grid = mapdl.mesh.grid
        UnstructuredGrid (0x7f99b4135760)
          N Cells:	32198
          N Points:	50686
          X Bounds:	-1.181e+00, 1.181e+00
          Y Bounds:	-2.362e-01, 0.000e+00
          Z Bounds:	-2.394e+00, 2.509e+00
          N Arrays:	10

        Plot this grid.

        >>> grid.plot()

        Access the node numbers of grid.

        >>> grid.point_data
        Contains keys:
            ansys_node_num
            vtkOriginalPointIds
            origid
            VTKorigID

        >>> grid.point_data['ansys_node_num']
        pyvista_ndarray([    1,     2,     3, ..., 50684, 50685, 50686],
                        dtype=int32)

        Save this grid to disk

        >>> grid.save('grid.vtk')

        Load this grid externally with ParaView or with pyvista

        >>> import pyvista
        >>> pyvista.read('grid.vtk')

        """
        return self._grid

    @property
    def _grid(self):
        if self._grid_cache is None:
            self._update_cache()
            self._grid_cache = self._parse_vtk(force_linear=True)
        return self._grid_cache

    @_grid.setter
    def _grid(self, value):
        self._grid_cache = value
