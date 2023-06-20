"""Module to manage downloading and parsing the FEM from the MAPDL gRPC server."""
from functools import wraps
import os
import time
import weakref

from ansys.api.mapdl.v0 import ansys_kernel_pb2 as anskernel
import numpy as np

from ansys.mapdl.core.common_grpc import DEFAULT_CHUNKSIZE, parse_chunks
from ansys.mapdl.core.mapdl_grpc import MapdlGrpc
from ansys.mapdl.core.misc import supress_logging, threaded

TMP_NODE_CM = "__NODE__"


def requires_model(output=None):
    def decorator(method):
        """
        This function wrap some methods to check if the model contains elements or nodes.
        """

        @wraps(method)
        def wrapper(self, *args, **kwargs):
            if self._has_nodes and self._has_elements:
                return method(self, *args, **kwargs)
            else:
                if not output or output == "array":
                    return np.array([])
                elif output == "list":
                    return []
                elif output == "dict":
                    return {}
                else:  # pragma: no cover
                    raise ValueError("Output type not allowed.")

        return wrapper

    return decorator


class MeshGrpc:
    """Provides an interface to the gRPC mesh from MAPDL."""

    def __init__(self, mapdl):
        """Initialize grpc geometry data"""
        if not isinstance(mapdl, MapdlGrpc):  # pragma: no cover
            raise TypeError("Must be initialized using MapdlGrpc class")
        self._mapdl_weakref = weakref.ref(mapdl)
        mapdl._log.debug("Attached MAPDL object to MapdlMesh.")

        self.logger = mapdl._log
        self._log = mapdl._log

        self._ignore_cache_reset = False
        self._reset_cache()

    def __repr__(self):
        txt = "ANSYS Mesh\n"
        txt += f"  Number of Nodes:              {len(self.nnum)}\n"
        txt += f"  Number of Elements:           {len(self.enum)}\n"
        txt += f"  Number of Element Types:      {len(self.ekey)}\n"
        txt += f"  Number of Node Components:    {len(self.node_components)}\n"
        txt += f"  Number of Element Components: {len(self.element_components)}\n"
        return txt

    @property
    def _mapdl(self):
        """Return the weakly referenced instance of mapdl"""
        return self._mapdl_weakref()

    @property
    def _surf(self):
        """External surface"""
        if self._surf_cache is None:
            self._surf_cache = self._grid.extract_surface()
        return self._surf_cache

    @property
    def _has_nodes(self):
        """Returns True when has nodes"""
        # if isinstance(self._nodes, np.ndarray):
        # return bool(self._nodes.size)
        return self.nodes.size != 0

    @property
    def _has_elements(self):
        """Returns True when geometry has elements"""
        return self._elem.size != 0

    def _set_log_level(self, level):
        """Wraps set_log_level"""
        self._mapdl._set_log_level(level)

    def _reset_cache(self):
        """Reset entire mesh cache"""
        if not self._ignore_cache_reset:
            self.logger.debug("Resetting cache")

            self._cache_elem = None
            self._cache_elem_off = None
            self._cache_element_desc = None
            self._cache_nnum = None
            self._cached_elements = None  # cached list of elements
            self._chunk_size = None
            self._elem = None
            self._elem_comps = {}
            self._elem_off = None
            self._enum = None  # cached element numbering
            self._esys = None  # cached element coordinate system
            self._etype = None
            self._etype_cache = None  # cached ansys element type numbering
            self._etype_id = None  # cached element type id
            self._grid = None
            self._grid_cache = None
            self._keyopt = {}
            self._mtype = None  # cached ansys material type
            self._nnum = None
            self._node_angles = None  # cached node angles
            self._node_comps = {}
            self._node_coord = None  # cached node coordinates
            self._rcon = None  # cached ansys element real constant
            self._rdat = None
            self._rnum = None
            self._secnum = None  # cached section number
            self._surf_cache = None
            self._tshape = None
            self._tshape_key = None

    def _update_cache(self):
        """Threaded local cache update.

        Used when needing all the geometry entries from MAPDL.
        """
        self.logger.debug("Updating cache")
        # elements must have their underlying nodes selected to avoid
        # VTK segfault
        self._mapdl.cm(TMP_NODE_CM, "NODE", mute=True)
        self._mapdl.nsle("S", mute=True)

        # not thread safe
        self._update_cache_elem()

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

    @threaded
    def _update_cache_nnum(self):
        if self._cache_nnum is None:
            self.logger.debug("Updating nodes cache")
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
            self.logger.debug("Updating elements (desc) cache")
            self._cache_element_desc = self._load_element_types()

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
        return np.array([])

    @threaded
    def _update_node_coord(self):
        if self._node_coord is None:
            self._node_coord = self._load_nodes()

    @property
    def _ans_etype(self):
        """FIELD 1 : element type number"""
        if self._etype_cache is None:
            self._etype_cache = self._elem[self._elem_off[:-1] + 1]
        return self._etype_cache

    @property
    def local(self):
        return self._mapdl._local

    @property
    @requires_model()
    def et_id(self):
        """Element type id (ET) for each element."""
        if self._etype_id is None:
            etype_elem_id = self._elem_off[:-1] + 1
            self._etype_id = self._elem[etype_elem_id]
        return self._etype_id

    @property
    @requires_model()
    def tshape(self):
        """Tshape of contact elements."""
        if self._tshape is None:
            shape_elem_id = self._elem_off[:-1] + 7
            self._tshape = self._elem[shape_elem_id]
        return self._tshape

    @property
    @requires_model("dict")
    def tshape_key(self):
        """Dict with the mapping between element type and element shape.

        TShape is only applicable to contact elements.
        """
        if self._tshape_key is None:
            self._tshape_key = np.unique(np.vstack((self.et_id, self.tshape)), axis=1).T
        return {elem_id: tshape for elem_id, tshape in self._tshape_key}

    @property
    @requires_model()
    def material_type(self):
        """Material type index of each element in the archive."""
        # FIELD 0 : material reference number
        if self._mtype is None:
            self._mtype = self._elem[self._elem_off[:-1]]
        return self._mtype

    @property
    @requires_model()
    def etype(self):
        """Element type of each element.

        This is the ansys element type for each element.

        Notes
        -----
        Element types are listed below.  Please see the APDL Element
        Reference for more details:

        https://www.mm.bme.hu/~gyebro/files/vem/ansys_14_element_reference.pdf
        """
        if self._etype is None:
            arr = np.empty(self._ekey[:, 0].max() + 1, np.int32)
            arr[self._ekey[:, 0]] = self._ekey[:, 1]
            self._etype = arr[self._ans_etype]
        return self._etype

    @property
    @requires_model()
    def section(self):
        """Section number"""
        if self._secnum is None:
            self._secnum = self._elem[self._elem_off[:-1] + 3]  # FIELD 3
        return self._secnum

    @property
    @requires_model()
    def element_coord_system(self):
        """Element coordinate system number"""
        if self._esys is None:
            self._esys = self._elem[self._elem_off[:-1] + 4]  # FIELD 4
        return self._esys

    @property
    @requires_model("list")
    def elem(self):
        """List of elements containing raw ansys information.

        Each element contains 10 items plus the nodes belonging to the
        element.  The first 10 items are:

        - FIELD 0 : material reference number
        - FIELD 1 : element type number
        - FIELD 2 : real constant reference number
        - FIELD 3 : section number
        - FIELD 4 : element coordinate system
        - FIELD 5 : death flag (0 - alive, 1 - dead)
        - FIELD 6 : solid model reference
        - FIELD 7 : coded shape key
        - FIELD 8 : element number
        - FIELD 9 : base element number (applicable to reinforcing elements only)
        - FIELDS 10 - 30 : The nodes belonging to the element in ANSYS numbering.

        """
        if self._cached_elements is None:
            self._cached_elements = np.split(self._elem, self._elem_off[1:-1])
        return self._cached_elements

    @property
    def element_components(self):
        """Element components for the archive.

        Output is a dictionary of element components.  Each entry is an
        array of MAPDL element numbers corresponding to the element
        component.  The keys are element component names.
        """
        return self._elem_comps

    @property
    def node_components(self):
        """Node components for the archive.

        Output is a dictionary of node components.  Each entry is an
        array of MAPDL node numbers corresponding to the node
        component.  The keys are node component names.
        """
        return self._node_comps

    @property
    @requires_model()
    def elem_real_constant(self):
        """Real constant reference for each element.

        Use the data within ``rlblock`` and ``rlblock_num`` to get the
        real constant datat for each element.
        """
        # FIELD 2 : real constant reference number
        if self._rcon is None:
            self._rcon = self._elem[self._elem_off[:-1] + 2]
        return self._rcon

    @property
    def ekey(self):
        """Element type key

        Array containing element type numbers in the first column and
        the element types (like SURF154) in the second column.

        """
        return self._ekey

    @property
    def rlblock(self):
        """Real constant data from the RLBLOCK."""
        return self._mapdl._parse_rlist()

    @property
    def rlblock_num(self):
        """Indices from the real constant data"""
        return list(self._mapdl._parse_rlist().keys())

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

    @property
    def key_option(self):
        """Key options of selected element types."""
        self._update_cache_element_desc().join()

        key_opt = {}
        for einfo in self._cache_element_desc:
            keyopt = einfo[2:20]
            if keyopt.any():
                # convert to fortran/ANSYS format
                valid_keyopt = keyopt[keyopt.astype(np.bool_)]
                ans_keyopt = np.vstack((np.nonzero(keyopt)[0] + 1, valid_keyopt))
                key_opt[einfo[0]] = ans_keyopt.T.tolist()

        return key_opt

    @property
    def nodes(self) -> np.ndarray:
        """Array of nodes in Global Cartesian coordinate system.

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

    @property
    def nodes_in_current_CS(self) -> np.ndarray:
        """Returns the nodes array in the current coordinate system."""
        CS_id = self._mapdl.get_value("active", 0, "CSYS")
        return self.nodes_in_coordinate_system(CS_id=CS_id)

    def nodes_in_coordinate_system(self, CS_id):
        """Return nodes in the desired coordinate system."""
        if CS_id == 0:
            return self.nodes
        else:
            self._mapdl.parameters["__node_loc__"] = self.nodes
            self._mapdl.vfun("__node_loc_cs__", "local", "__node_loc__", CS_id)
            return self._mapdl.parameters["__node_loc_cs__"]

    @property
    def nodes_rotation(self):
        """Returns an array of node rotations"""
        return self._mapdl.nlist(kinternal="").to_array()[:, 4:]

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

    def _update_cache_elem(self):
        """Update the element and element offset cache"""
        if self._cache_elem is None:
            (
                self._cache_elem,
                self._cache_elem_off,
            ) = self._load_elements_offset()

    @property
    def _elem(self):
        """Contingious array of elements.

        Array of elements, with each element starting at the indices
        in offset.  Each element contains 10 items plus the nodes
        belonging to the element.
        """
        self._update_cache_elem()
        return self._cache_elem

    @_elem.setter
    def _elem(self, value):
        self._cache_elem = value

    @property
    def _elem_off(self):
        """Element offset array"""
        self._update_cache_elem()
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

        if len(elem_raw) == 0:  # for empty mesh.
            return np.array([]), np.array([])
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
        indx_elem = offset[:-1] + 8
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

    def save(
        self,
        filename,
        binary=True,
        force_linear=False,
        allowable_types=None,
        null_unallowed=False,
    ):
        """Save the geometry as a vtk file

        Parameters
        ----------
        filename : str, pathlib.Path
            Filename of output file. Writer type is inferred from
            the extension of the filename.

        binary : bool, optional
            If ``True``, write as binary, else ASCII.

        force_linear : bool, optional
            This parser creates quadratic elements if available.  Set
            this to True to always create linear elements.  Defaults
            to False.

        allowable_types : list, optional
            Allowable element types.  Defaults to all valid element
            types in ``ansys.mapdl.reader.elements.valid_types``

            See ``help(ansys.mapdl.reader.elements)`` for available element types.

        null_unallowed : bool, optional
            Elements types not matching element types will be stored
            as empty (null) elements.  Useful for debug or tracking
            element numbers.  Default False.

        Notes
        -----
        Binary files write much faster than ASCII and have a smaller
        file size.
        """
        grid = self._parse_vtk(
            allowable_types=allowable_types,
            force_linear=force_linear,
            null_unallowed=null_unallowed,
        )
        if grid:
            return grid.save(str(filename), binary=binary)
        else:
            raise ValueError("The mesh is empty, hence no file has been written.")

    def _parse_vtk(
        self,
        allowable_types=None,
        force_linear=False,
        null_unallowed=False,
        fix_midside=True,
        additional_checking=False,
    ):
        from ansys.mapdl.core.mesh.mesh import _parse_vtk

        return _parse_vtk(
            self,
            allowable_types,
            force_linear,
            null_unallowed,
            fix_midside,
            additional_checking,
        )
