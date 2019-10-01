import logging

import numpy as np
import pyvista as pv

from pyansys.elements import valid_types
from pyansys import _relaxmidside, _parser

log = logging.getLogger(__name__)
log.setLevel('CRITICAL')


def raw_to_grid(raw, allowable_types, force_linear, null_unallowed):
    """Parses raw data into to VTK format.

    Parameters
    ----------
    force_linear : bool, optional
        This parser creates quadratic elements if available.  Set
        this to True to always create linear elements.  Defaults
        to False.

    allowable_types : list, optional
        Allowable element types.  Defaults to all valid element
        types in ``from pyansys.elements.valid_types``

        See help(pyansys.elements) for available element types.

    null_unallowed : bool, optional
        Elements types not matching element types will be stored
        as empty (null) elements.  Useful for debug or tracking
        element numbers.  Default False.

    Returns
    -------
    grid : vtk.vtkUnstructuredGrid
        VTK unstructured grid from archive file.
    """
    # Convert to vtk style arrays
    if allowable_types is None:
        allowable_types = valid_types
    else:
        assert isinstance(allowable_types, list), \
               'allowable_types must be a list'
        for eletype in allowable_types:
            if str(eletype) not in valid_types:
                raise Exception('Element type "%s" ' % eletype +
                                'cannot be parsed in pyansys')

    # construct keyoption array
    keyopts = np.zeros((10000, 20), np.int16)

    for keyopt_key in raw['keyopt']:
        for index, value in raw['keyopt'][keyopt_key]:
            keyopts[keyopt_key, index] = value

    # parse raw output
    parsed = _parser.parse(raw, force_linear, allowable_types,
                           null_unallowed, keyopts)

    cells = parsed['cells']
    offset = parsed['offset']
    cell_type = parsed['cell_type']
    numref = parsed['numref']
    enum = parsed['enum']

    # Check for missing midside nodes
    if force_linear or np.all(cells != -1):
        nodes = raw['nodes'][:, :3].copy()
        nnum = raw['nnum']
        angles = raw['nodes'][:, 3:]
    else:
        mask = cells == -1

        nextra = mask.sum()
        maxnum = numref.max() + 1
        cells[mask] = np.arange(maxnum, maxnum + nextra)

        nnodes = raw['nodes'].shape[0]
        nodes = np.zeros((nnodes + nextra, 3))
        nodes[:nnodes] = raw['nodes'][:, :3]

        # Set new midside nodes directly between their edge nodes
        temp_nodes = nodes.copy()
        _relaxmidside.reset_midside(cells, cell_type, offset, temp_nodes)
        nodes[nnodes:] = temp_nodes[nnodes:]

        # merge nodes
        new_nodes = temp_nodes[nnodes:]
        unique_nodes, idxA, idxB = unique_rows(new_nodes)

        # rewrite node numbers
        cells[mask] = idxB + maxnum
        nextra = idxA.shape[0]
        nodes = np.empty((nnodes + nextra, 3))
        nodes[:nnodes] = raw['nodes'][:, :3]
        nodes[nnodes:] = unique_nodes

        angles = np.empty((nnodes + nextra, 3))
        angles[:nnodes] = raw['nodes'][:, 3:]
        angles[nnodes:] = 0

        # Add extra node numbers
        nnum = np.hstack((raw['nnum'], np.ones(nextra, np.int32) * -1))

    # Create unstructured grid
    grid = pv.UnstructuredGrid(offset, cells, cell_type, nodes)

    # Store original ANSYS element and cell information
    grid.point_arrays['ansys_node_num'] = nnum
    grid.cell_arrays['ansys_elem_num'] = enum
    grid.cell_arrays['ansys_elem_type_num'] = parsed['etype']
    grid.cell_arrays['ansys_real_constant'] = parsed['rcon']
    grid.cell_arrays['ansys_material_type'] = parsed['mtype']
    grid.cell_arrays['ansys_etype'] = parsed['ansys_etype']

    # Add element components to unstructured grid
    for comp in raw['elem_comps']:
        mask = np.in1d(enum, raw['elem_comps'][comp],
                       assume_unique=True)
        grid.cell_arrays[comp.strip()] = mask

    # Add node components to unstructured grid
    for comp in raw['node_comps']:
        mask = np.in1d(nnum, raw['node_comps'][comp],
                       assume_unique=True)
        grid.point_arrays[comp.strip()] = mask

    # Add tracker for original node numbering
    ind = np.arange(grid.number_of_points)
    grid.point_arrays['origid'] = ind
    grid.point_arrays['VTKorigID'] = ind

    # store node angles
    grid.point_arrays['angles'] = angles
    return grid


def check_raw(raw):
    """ Check if raw data can be converted into an unstructured grid """
    try:
        raw['elem'][0, 0]
        raw['enum'][0]
    except Exception:
        # return True
        raise Exception('Invalid file or missing key data.  ' +
                        'Cannot parse into unstructured grid')


def unique_rows(a):
    """ Returns unique rows of a and indices of those rows """
    if not a.flags.c_contiguous:
        a = np.ascontiguousarray(a)

    b = a.view(np.dtype((np.void, a.dtype.itemsize * a.shape[1])))
    _, idx, idx2 = np.unique(b, True, True)

    return a[idx], idx, idx2
