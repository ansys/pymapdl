"""Module for common class between Archive, and result mesh."""
from ansys.mapdl.reader import _reader, _relaxmidside
from ansys.mapdl.reader.elements import ETYPE_MAP
from ansys.mapdl.reader.misc import unique_rows
import numpy as np
import pyvista as pv

INVALID_ALLOWABLE_TYPES = TypeError(
    "`allowable_types` must be an array " "of ANSYS element types from 1 and 300"
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


def _parse_vtk(
    mesh,
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
    if not mesh._has_nodes or not mesh._has_elements:
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
    type_ref[mesh._ekey[:, 0]] = etype_map[mesh._ekey[:, 1]]

    if allowable_types is None or 200 in allowable_types:
        for etype_ind, etype in mesh._ekey:
            # MESH200
            if etype == 200 and etype_ind in mesh.key_option:
                # keyoption 1 contains various cell types
                # map them to the corresponding type (see elements.py)
                mapped = MESH200_MAP[mesh.key_option[etype_ind][0][1]]
                type_ref[etype_ind] = mapped

            # TARGE170 specifics
            if etype == 170:
                # edge case where missing element within the tshape_key
                if etype_ind not in mesh.tshape_key:  # pragma: no cover
                    continue
                tshape_num = mesh.tshape_key[etype_ind]
                if tshape_num >= 19:  # weird bug when 'PILO' can be 99 instead of 19.
                    tshape_num = 19
                tshape_label = SHAPE_MAP[tshape_num]
                type_ref[etype_ind] = TARGE170_MAP.get(tshape_label, 0)

    nodes, angles, nnum = mesh.nodes, mesh.node_angles, mesh.nnum

    offset, celltypes, cells = _reader.ans_vtk_convert(
        mesh._elem, mesh._elem_off, type_ref, nnum, True
    )  # for reset_midside

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

    grid = pv.UnstructuredGrid(cells, celltypes, nodes, deep=True)

    # Store original ANSYS element and node information
    try:
        grid.point_data["ansys_node_num"] = nnum
    except ValueError:
        grid.point_data["ansys_node_num"] = (
            mesh._mapdl.nlist(kinternal="internal").to_array()[:, 0].astype(np.int32)
        )

    grid.cell_data["ansys_elem_num"] = mesh.enum
    grid.cell_data["ansys_real_constant"] = mesh.elem_real_constant
    grid.cell_data["ansys_material_type"] = mesh.material_type
    grid.cell_data["ansys_etype"] = mesh._ans_etype
    grid.cell_data["ansys_elem_type_num"] = mesh.etype

    # add components
    # Add element components to unstructured grid
    for key, item in mesh.element_components.items():
        mask = np.in1d(mesh.enum, item, assume_unique=True)
        grid.cell_data[key] = mask

    # Add node components to unstructured grid
    for key, item in mesh.node_components.items():
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
