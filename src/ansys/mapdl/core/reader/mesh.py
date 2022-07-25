"""
Module to replace mapdl reader mesh.
"""

"""
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

import os
import tempfile
import weakref

import numpy as np

from ansys.mapdl.core.mapdl_grpc import MapdlGrpc
from ansys.mapdl.core.misc import random_string


class DPFMapdlMesh:
    """

    This class assumes that is going to be used together with MapdlGrpc class
    """

    def __init__(self, mapdl) -> None:
        if not isinstance(mapdl, MapdlGrpc):  # pragma: no cover
            raise TypeError("Must be initialized using MapdlGrpc class")
        self._mapdl_weakref = weakref.ref(mapdl)
        mapdl._log.debug("Attached MAPDL object to DPFMapdlMesh.")
        self.logger = mapdl._log

        self.__rst_directory = None
        self.__tmp_rst_name = None
        self._update_required = False  # if true, it triggers a update on the RST file

        self._cached_dpf_model = None
        self._cached_dpf_mesh = None

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
    def _rst(self):
        return os.path.join(self._rst_directory, self._tmp_rst_name)

    @property
    def local(self):
        return self._mapdl._local

    @property
    def _rst_directory(self):
        if self.__rst_directory is None:
            if self.local:
                _rst_directory = self._mapdl.directory
            else:
                _rst_directory = os.path.join(tempfile.gettempdir(), random_string())
                if not os.path.exists(_rst_directory):
                    os.mkdir(_rst_directory)

            self.__rst_directory = _rst_directory

        return self.__rst_directory

    @property
    def _tmp_rst_name(self):
        if self.__tmp_rst_name is None:
            if self.local:
                self.__tmp_rst_name = self._mapdl.jobname
            else:
                self.__tmp_rst_name = f"model_{random_string()}.rst"
        return self.__tmp_rst_name

    def _update(self, progress_bar=None, chunk_size=None):
        # Saving model
        self._mapdl.save(self._tmp_rst_name[:-4], "rst", "model")

        if not self.local:
            self.logger.debug("Updating the local copy of remote RST file.")
            # download file
            self._mapdl.download(
                self._tmp_rst_name,
                self._rst_directory,
                chunk_size=chunk_size,
                progress_bar=progress_bar,
            )

        # Updating model
        self._build_dpf_object()

        # Resetting flag
        self._update_required = False

    def _build_dpf_object(self):
        self.logger.debug("Building DPF Model object.")
        self._cached_dpf_model = Model(self._rst)

    @property
    def dpf_mesh(self):
        if self._cached_dpf_model is None or self._update_required:
            self._update()
        return self._cached_dpf_model.metadata.meshed_region

    @property
    def dpf_model(self):
        if self._cached_dpf_model is None or self._update_required:
            self._update()
        return self._cached_dpf_model

    def update(self, progress_bar=None, chunk_size=None):
        self._update(progress_bar=progress_bar, chunk_size=chunk_size)

    @property
    def _grid(self):
        return self.dpf_mesh._grid

    @property
    def _surf(self):
        return self._grid.extract_surface()

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

        return len(self._elem)

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
    def tshape_key(self, as_array=False):
        """Dict with the mapping between element type and element shape.

        TShape is only applicable to contact elements.
        """
        if self._tshape_key is None:
            self._tshape_key = np.unique(np.vstack((self.et_id, self.tshape)), axis=1).T

        if as_array:
            return self._tshape_key
        return {elem_id: tshape for elem_id, tshape in self._tshape_key}

    def save(
        self,
        filename,
        binary=True,
        force_linear=False,
        allowable_types=[],
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
        return self._rdat

    @property
    def rlblock_num(self):
        """Indices from the real constant data"""
        return self._rnum

    @property
    def nodes(self):
        """Array of nodes."""
        if self._node_coord is None:
            self._node_coord = np.ascontiguousarray(self._nodes[:, :3])
        return self._node_coord

    @property
    def node_angles(self):
        """Node angles from the archive file."""
        if self._node_angles is None:
            self._node_angles = np.ascontiguousarray(self._nodes[:, 3:])
        return self._node_angles

    # def _parse_vtk(self,
    #     allowable_types=None,
    #     force_linear=False,
    #     null_unallowed=False,
    #     fix_midside=True,
    #     additional_checking=False):
    #     # The arguments here are kept for compatibility.
    #     return self.dpf_mesh.grid

    def _parse_vtk(
        self,
        allowable_types=None,
        force_linear=False,
        null_unallowed=False,
        fix_midside=True,
        additional_checking=False,
    ):
        """Convert raw ANSYS nodes and elements to a VTK UnstructuredGrid

        Parameters
        ----------
        fix_midside : bool, optional
            Adds additional midside nodes when ``True``.  When
            ``False``, missing ANSYS cells will simply point to the
            first node.

        """
        from ansys.mapdl.reader import _reader, _relaxmidside
        from ansys.mapdl.reader.elements import ETYPE_MAP
        from ansys.mapdl.reader.misc import unique_rows
        import pyvista as pv
        from pyvista._vtk import VTK9

        INVALID_ALLOWABLE_TYPES = TypeError(
            "`allowable_types` must be an array "
            "of ANSYS element types from 1 and 300"
        )

        # map MESH200 elements to a pymapdl_reader/VTK element type (see elements.py)
        MESH200_MAP = {
            0: 2,  # line
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
            11: 4,
        }  # hex with 8 nodes

        SHAPE_MAP = {  # from ELIST definition
            0: "",
            1: "LINE",
            2: "PARA",
            3: "ARC ",
            4: "CARC",
            5: "",
            6: "TRIA",
            7: "QUAD",
            8: "TRI6",
            9: "QUA8",
            10: "POIN",
            11: "CIRC",
            12: "",
            13: "",
            14: "CYLI",
            15: "CONE",
            16: "SPHE",
            17: "",
            18: "",
            19: "PILO",
        }
        # element type to VTK conversion function call map
        # 0: skip
        # 1: Point
        # 2: Line (linear or quadratic)
        # 3: Shell
        # 4: 3D Solid (Hexahedral, wedge, pyramid, tetrahedral)
        # 5: Tetrahedral
        # 6: Line (always linear)
        TARGE170_MAP = {
            "TRI": 3,  # 3-Node Triangle
            "QUAD": 3,  # 4-Node Quadrilateral
            "CYLI": 0,  # Not supported (NS)  # Cylinder
            "CONE": 0,  # NS  # Cone
            "TRI6": 3,  # 6-Node triangle
            "SPHE": 0,  # NS  # Sphere
            "PILO": 1,  # Pilot Node
            "QUAD8": 3,  # 8-Node Quadrilateral
            "LINE": 2,  # Line
            "PARA": 2,  # Parabola
            "POINT": 1,  # Point
        }

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
            nodes_new[nnodes:] = 0  # otherwise, segfault disaster

            # Set new midside nodes directly between their edge nodes
            temp_nodes = nodes_new.copy()
            _relaxmidside.reset_midside(cells, celltypes, offset, temp_nodes)

            # merge midside nodes
            unique_nodes, idx_a, idx_b = unique_rows(temp_nodes[nnodes:])

            # rewrite node numbers
            cells[mask] = idx_b + nnodes
            nextra = idx_a.shape[0]  # extra unique nodes
            nodes_new = nodes_new[: nnodes + nextra]
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
                raise TypeError("Element types must be an integer array-like")

            if allowable_types.min() < 1 or allowable_types.max() > 300:
                raise INVALID_ALLOWABLE_TYPES

            etype_map = np.zeros_like(ETYPE_MAP)
            etype_map[allowable_types] = ETYPE_MAP[allowable_types]

        # ANSYS element type to VTK map
        type_ref = np.empty(2 << 16, np.int32)  # 131072
        type_ref[self._ekey[:, 0]] = etype_map[self._ekey[:, 1]]

        if allowable_types is None or 200 in allowable_types:
            for etype_ind, etype in self._ekey:

                # MESH200
                if etype == 200 and etype_ind in self.key_option:
                    # keyoption 1 contains various cell types
                    # map them to the corresponding type (see elements.py)
                    mapped = MESH200_MAP[self.key_option[etype_ind][0][1]]
                    type_ref[etype_ind] = mapped

                # TARGE170 specifics
                if etype == 170:
                    # edge case where missing element within the tshape_key
                    if etype_ind not in self.tshape_key:  # pragma: no cover
                        continue
                    tshape_num = self.tshape_key[etype_ind]
                    if (
                        tshape_num >= 19
                    ):  # weird bug when 'PILO' can be 99 instead of 19.
                        tshape_num = 19
                    tshape_label = SHAPE_MAP[tshape_num]
                    type_ref[etype_ind] = TARGE170_MAP.get(tshape_label, 0)

        offset, celltypes, cells = _reader.ans_vtk_convert(
            self._elem, self._elem_off, type_ref, self.nnum, True
        )  # for reset_midside

        nodes, angles, nnum = self.nodes, self.node_angles, self.nnum

        # fix missing midside
        if np.any(cells == -1):
            if fix_midside:
                nodes, angles, nnum = fix_missing_midside(
                    cells, nodes, celltypes, offset, angles, nnum
                )
            else:
                cells[cells == -1] = 0

        if additional_checking:
            cells[cells < 0] = 0
            # cells[cells >= nodes.shape[0]] = 0  # fails when n_nodes < 20

        if VTK9:
            grid = pv.UnstructuredGrid(cells, celltypes, nodes, deep=True)
        else:
            grid = pv.UnstructuredGrid(offset, cells, celltypes, nodes, deep=True)

        # Store original ANSYS element and node information
        grid.point_data["ansys_node_num"] = nnum
        grid.cell_data["ansys_elem_num"] = self.enum
        grid.cell_data["ansys_real_constant"] = self.elem_real_constant
        grid.cell_data["ansys_material_type"] = self.material_type
        grid.cell_data["ansys_etype"] = self._ans_etype
        grid.cell_data["ansys_elem_type_num"] = self.etype

        # add components
        # Add element components to unstructured grid
        for key, item in self.element_components.items():
            mask = np.in1d(self.enum, item, assume_unique=True)
            grid.cell_data[key] = mask

        # Add node components to unstructured grid
        for key, item in self.node_components.items():
            mask = np.in1d(nnum, item, assume_unique=True)
            grid.point_data[key] = mask

        # store node angles
        if angles is not None:
            if angles.shape[1] == 3:
                grid.point_data["angles"] = angles

        if not null_unallowed:
            grid = grid.extract_cells(grid.celltypes != 0)

        if force_linear:
            # only run if the grid has points or cells
            if grid.n_points:
                grid = grid.linear_copy()

        # map over element types
        # Add tracker for original node numbering
        ind = np.arange(grid.n_points)
        grid.point_data["origid"] = ind
        grid.point_data["VTKorigID"] = ind
        return grid
