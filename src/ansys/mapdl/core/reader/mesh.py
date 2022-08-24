"""
Module to replace mapdl reader mesh.

List of methods to replace
[
 '_ans_etype',
 '_has_elements',
 '_has_nodes',
 '_parse_vtk',
 '_surf',
 'ekey',
 'elem',
 'elem_real_constant',
 'element_components',
 'element_coord_system',
 'enum',
 'et_id',
 'etype',
 'key_option',
 'material_type',
 'n_elem',
 'n_node',
 'nnum',
 'node_angles',
 'node_components',
 'nodes',
 'rlblock',
 'rlblock_num',
 'save',
 'section',
 'tshape',
 'tshape_key']
"""
import weakref

import numpy as np

from ansys.mapdl.core.mapdl_grpc import MapdlGrpc


class MapdlMesh:
    """
    This class assumes that is going to be used together with MapdlGrpc class
    """

    def __init__(self, mapdl) -> None:
        if not isinstance(mapdl, MapdlGrpc):  # pragma: no cover
            raise TypeError("Must be initialized using MapdlGrpc class")
        self._mapdl_weakref = weakref.ref(mapdl)
        mapdl._log.debug("Attached MAPDL object to MapdlMesh.")
        self.logger = mapdl._log

        self._elem = None
        self._elem_off = None

        # For compatibility with child class
        # Most of them are used for cache flags
        self._enum = None  # cached element numbering
        self._etype_cache = None  # cached ansys element type numbering
        self._rcon = None  # cached ansys element real constant
        self._mtype = None  # cached ansys material type
        self._node_angles = None  # cached node angles
        self._node_coord = None  # cached node coordinates
        self._cached_elements = None  # cached list of elements
        self._secnum = None  # cached section number
        self._esys = None  # cached element coordinate system
        self._etype_id = None  # cached element type id
        self._tshape = None
        self._tshape_key = None
        self._keyopt = {}
        self._rdat = None
        self._rnum = None

        # optionals from Reader Mesh
        self._node_comps = {}
        self._elem_comps = {}

        # For compatibility but not used.
        self._surf_cache = None

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
    def local(self):
        return self._mapdl._local

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
        return len(self.nodes) != 0

    @property
    def _has_elements(self):
        """Returns True when geometry has elements"""
        if self._elem is None:
            return False

        if isinstance(self._elem, np.ndarray):
            return self._elem.size

        return len(self._elem)  # pragma: no cover

    @property
    def n_node(self):
        """Number of nodes"""
        if not self._has_nodes:
            return 0
        return self.nodes.shape[0]

    @property
    def n_elem(self):
        """Number of nodes"""
        if not self._has_elements:
            return 0
        return len(self.enum)

    @property
    def et_id(self):
        """Element type id (ET) for each element."""
        if self._etype_id is None:
            etype_elem_id = self._elem_off[:-1] + 1
            self._etype_id = self._elem[etype_elem_id]
        return self._etype_id

    @property
    def tshape(self):
        """Tshape of contact elements."""
        if self._tshape is None:
            shape_elem_id = self._elem_off[:-1] + 7
            self._tshape = self._elem[shape_elem_id]
        return self._tshape

    @property
    def tshape_key(self):
        """Dict with the mapping between element type and element shape.

        TShape is only applicable to contact elements.
        """
        if self._tshape_key is None:
            self._tshape_key = np.unique(np.vstack((self.et_id, self.tshape)), axis=1).T

        return {elem_id: tshape for elem_id, tshape in self._tshape_key}

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
        return grid.save(str(filename), binary=binary)

    @property
    def key_option(self):
        """Additional key options for element types"""
        return self._keyopt

    @property
    def material_type(self):
        """Material type index of each element in the archive."""
        # FIELD 0 : material reference number
        if self._mtype is None:
            self._mtype = self._elem[self._elem_off[:-1]]
        return self._mtype

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
    def _ans_etype(self):
        """FIELD 1 : element type number"""
        if self._etype_cache is None:
            self._etype_cache = self._elem[self._elem_off[:-1] + 1]
        return self._etype_cache

    @property
    def section(self):
        """Section number"""
        if self._secnum is None:
            self._secnum = self._elem[self._elem_off[:-1] + 3]  # FIELD 3
        return self._secnum

    @property
    def element_coord_system(self):
        """Element coordinate system number"""
        if self._esys is None:
            self._esys = self._elem[self._elem_off[:-1] + 4]  # FIELD 4
        return self._esys

    @property
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
    def enum(self):
        """ANSYS element numbers."""
        if self._enum is None:
            self._enum = self._elem[self._elem_off[:-1] + 8]
        return self._enum

    @property
    def nnum(self):
        """Array of node numbers."""
        return self._nnum

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
        # if not self._rdat:
        #     pass # todo: fix this
        # return self._rdat
        raise NotImplementedError()

    @property
    def rlblock_num(self):
        """Indices from the real constant data"""
        # if not self._rnum:
        #     pass # todo: to fix
        # return self._rnum
        raise NotImplementedError()

    @property
    def nodes(self):
        """Array of nodes."""
        if self._node_coord is None:
            self._node_coord = np.ascontiguousarray(self._nodes[:, :3])
        return self._node_coord

    @property
    def node_angles(self):
        """Node angles from the archive file."""
        # if self._node_angles is None:
        #     self._node_angles = np.ascontiguousarray(self._nodes[:, 3:])
        # return self._node_angles
        raise NotImplementedError()

    def _parse_vtk(
        self,
        allowable_types=None,
        force_linear=False,
        null_unallowed=False,
        fix_midside=True,
        additional_checking=False,
    ):
        from ansys.mapdl.reader.mesh import Mesh

        return Mesh._parse_vtk(
            self,
            allowable_types,
            force_linear,
            null_unallowed,
            fix_midside,
            additional_checking,
        )
