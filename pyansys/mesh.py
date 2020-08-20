"""Module for common class between gRPC, Archive, and Result mesh"""
import pyvista as pv
import vtk
import numpy as np

from pyansys import _relaxmidside, _reader
from pyansys.misc import unique_rows
from pyansys.elements import ETYPE_MAP


VTK9 = vtk.vtkVersion().GetVTKMajorVersion() >= 9
INVALID_ALLOWABLE_TYPES = TypeError('`allowable_types` must be an array '
                                    'of ANSYS element types from 1 and 300')

# map MESH200 elements to a pyansys/VTK element type (see elements.py)
MESH200_MAP = {0: 2,  # line
               1: 2,  # line
               2: 2,  # line
               3: 2,  # line
               4: 3,  # triangle
               5: 3,  # triangle
               6: 3,  # quadrilateral
               7: 3,  # quadrilateral
               8: 5,  # tetrahedron with 4 nodes
               9: 5,  # tetrahedron with 10 nodes
               10: 4,  # hex with 8 nodes
               11: 4}  # hex with 8 nodes


class Mesh():

    def __init__(self, nnum=None, nodes=None, elem=None,
                 elem_off=None, ekey=None, node_comps={},
                 elem_comps={}, rdat=[], rnum=[], keyopt={}):
        self._etype = None  # internal element type reference
        self._grid = None  # VTK grid
        self._enum = None  # cached element numbering
        self._etype_cache = None  # cached ansys element type numbering
        self._rcon = None  # cached ansys element real constant
        self._mtype = None  # cached ansys material type
        self._node_angles = None  # cached node angles
        self._node_coord = None  # cached node coordinates
        self._cached_elements = None  # cached list of elements
        self._secnum = None  # cached section number
        self._esys = None  # cached element coordinate system

        # Always set on init
        self._nnum = nnum
        self._nodes = nodes
        self._elem = elem
        self._elem_off = elem_off
        self._ekey = ekey

        # optional
        self._node_comps = node_comps
        self._elem_comps = elem_comps
        self._rdat = rdat
        self._rnum = rnum
        self._keyopt = keyopt

    @property
    def _has_nodes(self):
        """Returns True when has nodes"""
        # if isinstance(self._nodes, np.ndarray):
            # return bool(self._nodes.size)
        return len(self.nodes)

    @property
    def _has_elements(self):
        """Returns True when geometry has elements"""
        if self._elem is None:
            return False

        if isinstance(self._elem, np.ndarray):
            return self._elem.size

        return len(self._elem)

    def _parse_vtk(self, allowable_types=None, force_linear=False,
                   null_unallowed=False, fix_midside=True, additional_checking=False):
        """Convert raw ANSYS nodes and elements to a VTK UnstructuredGrid

        Parameters
        ----------
        fix_midside : bool, optional
            Adds additional midside nodes when ``True``.  When
            ``False``, missing ANSYS cells will simply point to the
            first node.

        """
        if not self._has_nodes or not self._has_elements:
            # warnings.warn('Missing nodes or elements.  Unable to parse to vtk')
            return

        etype_map = ETYPE_MAP
        if allowable_types is not None:
            try:
                allowable_types = np.asarray(allowable_types)
            except:
                raise INVALID_ALLOWABLE_TYPES

            if not issubclass(allowable_types.dtype.type, np.integer):
                raise TypeError('Element types must be an integer array-like')

            if allowable_types.min() < 1 or allowable_types.max() > 300:
                raise INVALID_ALLOWABLE_TYPES

            etype_map = np.zeros_like(ETYPE_MAP)
            etype_map[allowable_types] = ETYPE_MAP[allowable_types]

        # ANSYS element type to VTK map
        type_ref = np.empty(2 << 15, np.int32)  # 65536
        type_ref[self._ekey[:, 0]] = etype_map[self._ekey[:, 1]]        

        # special treatment for MESH200
        if allowable_types is None or 200 in allowable_types:
            for etype_ind, etype in self._ekey:
                if etype == 200 and etype_ind in self.key_option:
                    # keyoption 1 contains various cell types
                    # map them to the corresponding type (see elements.py)
                    mapped = MESH200_MAP[self.key_option[etype_ind][0][1]]
                    type_ref[etype_ind] = mapped

        offset, celltypes, cells = _reader.ans_vtk_convert(self._elem,
                                                           self._elem_off,
                                                           type_ref,
                                                           self.nnum,
                                                           True)  # for reset_midside

        nodes, angles, nnum = self.nodes, self.node_angles, self.nnum

        # fix missing midside
        if np.any(cells == -1):
            if fix_midside:
                nodes, angles, nnum = fix_missing_midside(cells, nodes, celltypes,
                                                          offset, angles, nnum)
            else:
                cells[cells == -1] = 0

        if additional_checking:
            cells[cells < 0] = 0
            cells[cells >= nodes.shape[0]] = 0

        if VTK9:
            grid = pv.UnstructuredGrid(cells, celltypes, nodes, deep=False)
        else:
            grid = pv.UnstructuredGrid(offset, cells, celltypes, nodes,
                                       deep=False)

        # Store original ANSYS element and node information
        grid.point_arrays['ansys_node_num'] = nnum
        grid.cell_arrays['ansys_elem_num'] = self.enum
        grid.cell_arrays['ansys_real_constant'] = self.elem_real_constant
        grid.cell_arrays['ansys_material_type'] = self.material_type
        grid.cell_arrays['ansys_etype'] = self._ans_etype
        grid.cell_arrays['ansys_elem_type_num'] = self.etype

        # add components
        # Add element components to unstructured grid
        for key, item in self.element_components.items():
            mask = np.in1d(self.enum, item, assume_unique=True)
            grid.cell_arrays[key] = mask

        # Add node components to unstructured grid
        for key, item in self.node_components.items():
            mask = np.in1d(nnum, item, assume_unique=True)
            grid.point_arrays[key] = mask

        # store node angles
        if angles is not None:
            grid.point_arrays['angles'] = angles

        if not null_unallowed:
            grid = grid.extract_cells(grid.celltypes != 0)

        if force_linear:
            grid = grid.linear_copy()

        # map over element types
        # Add tracker for original node numbering
        ind = np.arange(grid.number_of_points)
        grid.point_arrays['origid'] = ind
        grid.point_arrays['VTKorigID'] = ind
        return grid

    @property
    def key_option(self):
        """Additional key options for element types

        Examples
        --------
        >>> import pyansys
        >>> archive = pyansys.Archive(pyansys.examples.hexarchivefile)
        >>> archive.key_option
        {1: [[1, 11]]}
        """
        return self._keyopt

    @property
    def material_type(self):
        """Material type index of each element in the archive.

        Examples
        --------
        >>> import pyansys
        >>> archive = pyansys.Archive(pyansys.examples.hexarchivefile)
        >>> archive.material_type
        array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
               1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
               1, 1, 1, 1], dtype=int32)
        """
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

        Examples
        --------
        >>> import pyansys
        >>> archive = pyansys.Archive(pyansys.examples.hexarchivefile)
        >>> archive.element_components
        {'ECOMP1 ': array([17, 18, 21, 22, 23, 24, 25, 26, 27, 28, 29,
                           30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40],
                           dtype=int32),
        'ECOMP2 ': array([ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13,
                          14, 15, 16, 17, 18, 19, 20, 23, 24], dtype=int32)}
        """
        return self._elem_comps

    @property
    def node_components(self):
        """Node components for the archive.

        Output is a dictionary of node components.  Each entry is an
        array of MAPDL node numbers corresponding to the node
        component.  The keys are node component names.

        Examples
        --------
        >>> import pyansys
        >>> archive = pyansys.Archive(pyansys.examples.hexarchivefile)
        >>> archive.node_components
        {'NCOMP2  ': array([  1,   2,   3,   4,   5,   6,   7,   8,
                             14, 15, 16, 17, 18, 19, 20, 21, 43, 44,
                             62, 63, 64, 81, 82, 90, 91, 92, 93, 94,
                             118, 119, 120, 121, 122, 123, 124, 125,
                             126, 137, 147, 148, 149, 150, 151, 152,
                             153, 165, 166, 167, 193, 194, 195, 202,
                             203, 204, 205, 206, 207, 221, 240, 258,
                             267, 268, 276, 277, 278, 285, 286, 287,
                             304, 305, 306, 313, 314, 315, 316
                             ], dtype=int32),
        ...,
        }
        """
        return self._node_comps

    @property
    def elem_real_constant(self):
        """Real constant reference for each element.

        Use the data within ``rlblock`` and ``rlblock_num`` to get the
        real constant datat for each element.

        Examples
        --------
        >>> import pyansys
        >>> archive = pyansys.Archive(pyansys.examples.hexarchivefile)
        >>> archive.elem_real_constant
        array([ 1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,
                1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,
                1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,
                ...,
                1,  1,  1,  1,  1,  1,  1,  1,  1,  1, 61, 61, 61, 61,
               61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61,
               61], dtype=int32)

        """
        # FIELD 2 : real constant reference number
        if self._rcon is None:
            self._rcon = self._elem[self._elem_off[:-1] + 2]
        return self._rcon

    @property
    def etype(self):
        """Element type of each element.

        This is the ansys element type for each element.

        Examples
        --------
        >>> import pyansys
        >>> archive = pyansys.Archive(pyansys.examples.hexarchivefile)
        >>> archive.etype
        array([ 45,  45,  45,  45,  45,  45,  45,  45,  45,  45,  45,
                45,  45,  45,  45,  45,  45,  45,  45,  92,  92,  92,
                92,  92,  92,  92,  92,  92,  92,  92,  92,  92,  92,
                ...,
                92,  92,  92,  92,  92, 154, 154, 154, 154, 154, 154,
               154, 154, 154, 154, 154, 154, 154, 154, 154, 154, 154,
               154], dtype=int32)

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
        """Section number

        Examples
        --------
        >>> import pyansys
        >>> archive = pyansys.Archive(pyansys.examples.hexarchivefile)
        >>> archive.section
        array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
               1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
               1, 1], dtype=int32)
        """
        if self._secnum is None:
            self._secnum = self._elem[self._elem_off[:-1] + 3]  # FIELD 3
        return self._secnum

    def element_coord_system(self):
        """Element coordinate system number

        Examples
        --------
        >>> import pyansys
        >>> archive = pyansys.Archive(pyansys.examples.hexarchivefile)
        >>> archive.element_coord_system
        array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0], dtype=int32)
        """
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

        Examples
        --------
        >>> import pyansys
        >>> archive = pyansys.Archive(pyansys.examples.hexarchivefile)
        >>> archive.elem
        [array([  1,   4,  19,  15,  63,  91, 286, 240,   3,  18,  17,
                 16,  81, 276, 267, 258,  62,  90, 285, 239],
         array([  4,   2,   8,  19,  91,  44, 147, 286,   5,   7,  21,
                 18, 109, 137, 313, 276,  90,  43, 146, 285],
         array([ 15,  19,  12,  10, 240, 286, 203, 175,  17,  20,  13,
                 14, 267, 304, 221, 230, 239, 285, 202, 174],
        ...
        """
        if self._cached_elements is None:
            self._cached_elements = np.split(self._elem, self._elem_off[1:-1])
        return self._cached_elements

    @property
    def enum(self):
        """ANSYS element numbers.

        Examples
        --------
        >>> import pyansys
        >>> archive = pyansys.Archive(pyansys.examples.hexarchivefile)
        >>> archive.enum
        array([    1,     2,     3, ...,  9998,  9999, 10000])
        """
        if self._enum is None:
            self._enum = self._elem[self._elem_off[:-1] + 8]
        return self._enum

    @property
    def nnum(self):
        """Array of node numbers.

        Examples
        --------
        >>> import pyansys
        >>> archive = pyansys.Archive(pyansys.examples.hexarchivefile)
        >>> archive.nnum
        array([    1,     2,     3, ..., 19998, 19999, 20000])
        """
        return self._nnum

    @property
    def ekey(self):
        """Element type key

        Array containing element type numbers in the first column and
        the element types (like SURF154) in the second column.

        Examples
        --------
        >>> import pyansys
        >>> archive = pyansys.Archive(pyansys.examples.hexarchivefile)
        >>> archive.ekey
        array([[  1,  45],
               [  2,  95],
               [  3,  92],
               [ 60, 154]], dtype=int32)
        """
        return self._ekey

    @property
    def rlblock(self):
        """Real constant data from the RLBLOCK.

        Examples
        --------
        >>> import pyansys
        >>> archive = pyansys.Archive(pyansys.examples.hexarchivefile)
        >>> archive.rlblock
        [[0.   , 0.   , 0.   , 0.   , 0.   , 0.   , 0.02 ],
         [0.   , 0.   , 0.   , 0.   , 0.   , 0.   , 0.01 ],
         [0.   , 0.   , 0.   , 0.   , 0.   , 0.   , 0.005],
         [0.   , 0.   , 0.   , 0.   , 0.   , 0.   , 0.005]]
        """
        return self._rdat

    @property
    def rlblock_num(self):
        """Indices from the real constant data

        Examples
        --------
        >>> import pyansys
        >>> archive = pyansys.Archive(pyansys.examples.hexarchivefile)
        >>> archive.rnum
        array([60, 61, 62, 63])
        """
        return self._rnum

    @property
    def nodes(self):
        """Array of nodes.

        Examples
        --------
        >>> import pyansys
        >>> archive = pyansys.Archive(pyansys.examples.hexarchivefile)
        >>> archive.nodes
        [[0.   0.   0.  ]
         [1.   0.   0.  ]
         [0.25 0.   0.  ]
         ...,
         [0.75 0.5  3.5 ]
         [0.75 0.5  4.  ]
         [0.75 0.5  4.5 ]]
        """
        if self._node_coord is None:
            self._node_coord = np.ascontiguousarray(self._nodes[:, :3])
        return self._node_coord

    @property
    def node_angles(self):
        """Node angles from the archive file.

        Examples
        --------
        >>> import pyansys
        >>> archive = pyansys.Archive(pyansys.examples.hexarchivefile)
        >>> archive.nodes
        [[0.   0.   0.  ]
         [0.   0.   0.  ]
         [0.   0.   0.  ]
         ...,
         [0.   0.   0.  ]
         [0.   0.   0.  ]
         [0.   0.   0.  ]]
        """
        if self._node_angles is None:
            self._node_angles = np.ascontiguousarray(self._nodes[:, 3:])
        return self._node_angles

    def __repr__(self):
        txt = 'ANSYS Mesh\n'
        txt += '  Number of Nodes:              %d\n' % len(self.nnum)
        txt += '  Number of Elements:           %d\n' % len(self.enum)
        txt += '  Number of Element Types:      %d\n' % len(self.ekey)
        txt += '  Number of Node Components:    %d\n' % len(self.node_components)
        txt += '  Number of Element Components: %d\n' % len(self.element_components)
        return txt

    def save(self, filename, binary=True, force_linear=False, allowable_types=[],
             null_unallowed=False):
        """Save the geometry as a vtk file

        Parameters
        ----------
        filename : str
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
            types in ``pyansys.elements.valid_types``

            See ``help(pyansys.elements)`` for available element types.

        null_unallowed : bool, optional
            Elements types not matching element types will be stored
            as empty (null) elements.  Useful for debug or tracking
            element numbers.  Default False.

        Examples
        --------
        >>> geom.save('mesh.vtk')

        Notes
        -----
        Binary files write much faster than ASCII and have a smaller
        file size.
        """
        grid = self._parse_vtk(allowable_types=allowable_types,
                               force_linear=force_linear,
                               null_unallowed=null_unallowed)
        return grid.save(filename, binary=binary)

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


def fix_missing_midside(cells, nodes, celltypes, offset, angles, nnum):
    """Adds missing midside nodes to cells.

    ANSYS sometimes does not add midside nodes, and this is denoted in
    the element array with a ``0``.  When translated to VTK, this is
    saved as a ``-1``.  If this is not corrected, VTK will segfault.

    This function creates missing midside nodes for the quadratic
    elements.
    """
    # Check for missing midside nodes
    mask = cells == -1
    nnodes = nodes.shape[0]

    nextra = mask.sum()
    cells[mask] = np.arange(nnodes, nnodes + nextra)

    nodes_new = np.empty((nnodes + nextra, 3))
    nodes_new[:nnodes] = nodes

    # Set new midside nodes directly between their edge nodes
    temp_nodes = nodes_new.copy()
    _relaxmidside.reset_midside(cells, celltypes, offset, temp_nodes)

    # merge midside nodes
    unique_nodes, idx_a, idx_b = unique_rows(temp_nodes[nnodes:])

    # rewrite node numbers
    cells[mask] = idx_b + nnodes
    nextra = idx_a.shape[0]  # extra unique nodes
    nodes_new = nodes_new[:nnodes + nextra]
    nodes_new[nnodes:] = unique_nodes

    if angles is not None:
        new_angles = np.empty((nnodes + nextra, 3))
        new_angles[:nnodes] = angles
        new_angles[nnodes:] = 0
    else:
        new_angles = None

    # Add extra node numbers
    nnum_new = np.empty(nnodes + nextra)
    nnum_new[:nnodes] = nnum
    nnum_new[nnodes:] = -1
    return nodes_new, new_angles, nnum_new
