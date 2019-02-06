"""
Module to read ANSYS ASCII block formatted CDB files

USAGE

# load module
import pyansys

# load ANSYS cdb file
archive = pyansys.Archive('example.cdb')

# Parse the raw data into a VTK unstructured grid
grid = archive.parse_vtk()

# Plot the result
grid.plot()

"""
import warnings
import sys
import logging
import os

import numpy as np
import vtk
from vtk import VTK_TETRA
from vtk import VTK_QUADRATIC_TETRA
from vtk import VTK_PYRAMID
from vtk import VTK_QUADRATIC_PYRAMID
from vtk import VTK_WEDGE
from vtk import VTK_QUADRATIC_WEDGE
from vtk import VTK_HEXAHEDRON
from vtk import VTK_QUADRATIC_HEXAHEDRON
import vtki

from pyansys import _reader
from pyansys import _relaxmidside
from pyansys import _parser
from pyansys.elements import valid_types

log = logging.getLogger(__name__)
log.setLevel('CRITICAL')


class Archive(object):
    """
    Initialize cdb object by reading raw cdb from file

    Parameters
    ----------
    filename : string
        Filename of block formatted cdb file

    """

    def __init__(self, filename):
        """ Initializes a cdb object """
        self.raw = _reader.Read(filename)

    def parse_vtk(self, force_linear=False, allowable_types=None,
                  null_unallowed=False):
        """
        Parses raw data from cdb file to VTK format.

        Parameters
        ----------
        force_linear : bool, optional
            This parser creates quadradic elements if available.  Set this to
            True to always create linear elements.  Defaults to False.

        allowable_types : list, optional
            Allowable element types.  Defaults to:
            ['45', '95', '185', '186', '92', '187']

            See help(pyansys.elements) for available element types.

        null_unallowed : bool, optional
            Elements types not matching element types will be stored as empty
            (null) elements.  Useful for debug or tracking element numbers.
            Default False.

        Returns
        -------
        uGrid : vtk.vtkUnstructuredGrid
            VTK unstructured grid from archive file.
        """
        if self.check_raw():
            raise Exception('Invalid file or missing key data.  ' +
                            'Cannot parse into unstructured grid')

        # Convert to vtk style arrays
        if allowable_types is None:
            # allowable_types = ['45', '95', '185', '186', '92', '187']
            allowable_types = valid_types
        else:
            assert isinstance(allowable_types, list), \
                   'allowable_types must be a list'
            for eletype in allowable_types:
                if str(eletype) not in valid_types:
                    raise Exception('Element type "%s" ' % eletype +
                                    'cannot be parsed in pyansys')

        # parse raw output
        parsed = _parser.Parse(self.raw, force_linear, allowable_types, null_unallowed)
        cells = parsed['cells']
        offset = parsed['offset']
        cell_type = parsed['cell_type']
        numref = parsed['numref']
        enum = parsed['enum']

        # Check for missing midside nodes
        if force_linear or np.all(cells != -1):
            nodes = self.raw['nodes'][:, :3].copy()
            nnum = self.raw['nnum']
        else:
            mask = cells == -1

            nextra = mask.sum()
            maxnum = numref.max() + 1
            cells[mask] = np.arange(maxnum, maxnum + nextra)

            nnodes = self.raw['nodes'].shape[0]
            nodes = np.zeros((nnodes + nextra, 3))
            nodes[:nnodes] = self.raw['nodes'][:, :3]

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
            nodes = np.zeros((nnodes + nextra, 3))
            nodes[:nnodes] = self.raw['nodes'][:, :3]
            nodes[nnodes:] = unique_nodes

            # Add extra node numbers
            nnum = np.hstack((self.raw['nnum'],
                              np.ones(nextra, np.int32) * -1))

        # Create unstructured grid
        grid = vtki.UnstructuredGrid(offset, cells, cell_type, nodes)

        # Store original ANSYS element and cell information
        grid.point_arrays['ansys_node_num'] = nnum
        grid.cell_arrays['ansys_elem_num'] = enum
        grid.cell_arrays['ansys_elem_type_num'] = parsed['etype']
        grid.cell_arrays['ansys_real_constant'] = parsed['rcon']
        grid.cell_arrays['ansys_material_type'] = parsed['mtype']
        grid.cell_arrays['ansys_etype'] = parsed['ansys_etype']

        # Add element components to unstructured grid
        for comp in self.raw['elem_comps']:
            mask = np.in1d(enum, self.raw['elem_comps'][comp], assume_unique=True)
            grid.cell_arrays[comp.strip()] = mask

        # Add node components to unstructured grid
        for comp in self.raw['node_comps']:
            mask = np.in1d(nnum, self.raw['node_comps'][comp], assume_unique=True)
            grid.point_arrays[comp.strip()] = mask

        # Add tracker for original node numbering
        ind = np.arange(grid.number_of_points)
        grid.point_arrays['origid'] = ind
        grid.point_arrays['VTKorigID'] = ind

        self.vtkuGrid = grid
        return grid

    def check_raw(self):
        """ Check if raw data can be converted into an unstructured grid """
        try:
            self.raw['elem'][0, 0]
            self.raw['enum'][0]
        except BaseException:
            return 1

        return 0


def chunks(l, n):
    """ Yield successive n-sized chunks from l """
    for i in range(0, len(l), n):
        yield l[i:i + n]


def unique_rows(a):
    """ Returns unique rows of a and indices of those rows """
    if not a.flags.c_contiguous:
        a = np.ascontiguousarray(a)

    b = a.view(np.dtype((np.void, a.dtype.itemsize * a.shape[1])))
    _, idx, idx2 = np.unique(b, True, True)

    return a[idx], idx, idx2


def save_as_archive(filename, grid, mtype_start=1, etype_start=1,
                    real_constant_start=1, mode='w',
                    nblock=True, enum_start=1, nnum_start=1,
                    include_etype_header=True, line_ending=None,
                    reset_etype=False, allow_missing=True):
    """
    Writes FEM as an ANSYS APDL archive file.  This function supports the
    following element types:
    
        - vtk.VTK_TETRA
        - vtk.VTK_QUADRATIC_TETRA
        - vtk.VTK_PYRAMID
        - vtk.VTK_QUADRATIC_PYRAMID
        - vtk.VTK_WEDGE
        - vtk.VTK_QUADRATIC_WEDGE
        - vtk.VTK_HEXAHEDRON
        - vtk.VTK_QUADRATIC_HEXAHEDRON    

    Will automatically renumber nodes and elements if the FEM does not
    contain ANSYS node or element numbers.  Node numbers are stored as
    a point array "ansys_node_num", and cell numbers are stored as cell
    array "ansys_elem_num".

    Parameters
    ----------
    filename : str
       Filename to write archive file.

    grid : vtk.UnstructuredGrid
        VTK UnstructuredGrid to convert to an APDL archive file.

    mtype_start : int, optional
        Material number to assign to elements.  Can be set manually by
        adding the cell array "mtype" to the unstructured grid.

    etype_start : int, optional
        Starting element type number.  Can be manually set by adding the
        cell array "ansys_etype" to the unstructured grid.

    real_constant_start : int, optional
        Starting real constant to assign to unset cells.  Can be manually
        set by adding the cell array "ansys_real_constant" to the
        unstructured grid.

    mode : str, optional
        File mode.  See help(open)

    nblock : bool, optional
        Write node block when writing archive file.

    enum_start : int, optional
        Starting element number to assign to unset cells.  Can be manually
        set by adding the cell array "ansys_elem_num" to the
        unstructured grid.

    nnum_start : int, optional
        Starting element number to assign to unset points.  Can be manually
        set by adding the point array "ansys_node_num" to the
        unstructured grid.

    include_etype_header : bool, optional
        For each element type, includes element type command (e.g. "ET, 1, 186")
        in the archive file.

    line_ending : str, optional
        Defaults to windows line ending.

    reset_etype : bool, optional
        Resets element type.  Element types will automatically be determined 
        by the shape of the element (i.e. quadradic tetrahedrals will be saved
        as SOLID187, linear hexahedrals as SOLID185).  Default True.

    """
    if line_ending is None:
        # line_ending = os.linesep
        line_ending = '\r\n'

    header = '/PREP7%s' % line_ending

    # node numbers
    if 'ansys_node_num' in grid.point_arrays:
        nodenum = grid.point_arrays['ansys_node_num']
    else:
        log.info('No ANSYS node numbers set in input.  ' +
                 'Adding default range')
        nodenum = np.arange(1, grid.number_of_points + 1)

    if np.any(nodenum == -1):
        if not allow_missing:
            raise Exception('Missing node numbers.  Exiting due "allow_missing=False"')
        start_num = nodenum.max() + 1
        if nnum_start > start_num:
           start_num = nnum_start
        nadd = np.sum(nodenum == -1)
        end_num = start_num + nadd
        log.info('FEM missing some node numbers.  Adding node numbering ' +
                 'from %d to %d' % (start_num, end_num))
        nodenum[nodenum == -1] = np.arange(start_num, end_num)

    # element block
    ncells = grid.number_of_cells
    if 'ansys_elem_num' in grid.cell_arrays:
        enum = grid.cell_arrays['ansys_elem_num']
    else:
        if not allow_missing:
            raise Exception('Missing node numbers.  Exiting due "allow_missing=False"')
        log.info('No ANSYS element numbers set in input.  ' +
                 'Adding default range starting from %d' % enum_start)
        enum = np.arange(1, ncells + 1)
 
    if np.any(enum == -1):
        if not allow_missing:
            raise Exception('-1 encountered in "ansys_elem_num".\n'
                            + 'Exiting due "allow_missing=False"')

        start_num = enum.max() + 1
        if enum_start > start_num:
           start_num = enum_start
        nadd = np.sum(enum == -1)
        end_num = start_num + nadd
        log.info('FEM missing some cell numbers.  Adding numbering ' +
                 'from %d to %d' % (start_num, end_num))
        enum[enum == -1] = np.arange(start_num, end_num)

    # material type
    if 'ansys_material_type' in grid.cell_arrays:
        mtype = grid.cell_arrays['ansys_material_type']
    else:
        log.info('No ANSYS element numbers set in input.  ' +
                 'Adding default range starting from %d' % mtype_start)
        mtype = np.arange(1, ncells + 1)

    if np.any(mtype == -1):
        log.info('FEM missing some material type numbers.  Adding...')
        mtype[mtype == -1] = mtype_start

    # real constant    
    if 'ansys_real_constant' in grid.cell_arrays:
        rcon = grid.cell_arrays['ansys_real_constant']
    else:
        log.info('No ANSYS element numbers set in input.  ' +
                 'Adding default range starting from %d' % real_constant_start)
        rcon = np.arange(1, ncells + 1)

    if np.any(rcon == -1):
        log.info('FEM missing some material type numbers.  Adding...')
        rcon[rcon == -1] = real_constant_start

    # element type
    invalid = False
    if 'ansys_etype' in grid.cell_arrays and not reset_etype:
        missing = False
        typenum = grid.cell_arrays['ansys_elem_type_num']
        etype = grid.cell_arrays['ansys_etype']
        if np.any(etype == -1):
            log.warning('Some elements are missing element type numbers.')
            invalid = True

        if include_etype_header and not invalid:
            _, ind = np.unique(etype, return_index=True)
            for idx in ind:
                header += 'ET, %d, %d%s' % (etype[idx], typenum[idx], line_ending)
    else:
        missing = True

    # check if valid
    if not missing:
        mask = grid.celltypes < 20
        if np.any(grid.cell_arrays['ansys_elem_type_num'][mask] == 186):
            invalid = True
            log.warning('Invalid ANSYS element types.')

    if invalid or missing:
        if not allow_missing:
            raise Exception('Invalid or missing data in "ansys_elem_type_num"' +
                            ' or "ansys_etype".  Exiting due "allow_missing=False"')

        log.info('No ANSYS element type or invalid data input.  ' +
                 'Adding default range starting from %d' % etype_start)

        etype = np.empty(grid.number_of_cells, np.int32)
        etype_185 = etype_start + 2
        etype[grid.celltypes == VTK_TETRA] = etype_185
        etype[grid.celltypes == VTK_HEXAHEDRON] = etype_185
        etype[grid.celltypes == VTK_WEDGE] = etype_185
        etype[grid.celltypes == VTK_PYRAMID] = etype_185

        etype_186 = etype_start
        etype[grid.celltypes == VTK_QUADRATIC_HEXAHEDRON] = etype_186
        etype[grid.celltypes == VTK_QUADRATIC_WEDGE] = etype_186
        etype[grid.celltypes == VTK_QUADRATIC_PYRAMID] = etype_186

        etype_187 = etype_start + 1
        etype[grid.celltypes == VTK_QUADRATIC_TETRA] = etype_187

        typenum = np.empty_like(etype)
        typenum[etype == etype_185] = 185
        typenum[etype == etype_186] = 186
        typenum[etype == etype_187] = 187

        header += 'ET, %d, 185%s' % (etype_185, line_ending)
        header += 'ET, %d, 186%s' % (etype_186, line_ending)
        header += 'ET, %d, 187%s' % (etype_187, line_ending)

    # if np.any(etype == -1):
    #     log.info('Some elements are missing element type numbers.  Adding...')
    #     if etype_start > etype.max():
    #         etype_start = etype.max()

    #     missing_mask = etype == -1
    #     missing_etype = etype[missing_mask]

    #     etype_185 = etype_start + 2
    #     missing_etype[grid.celltypes == VTK_TETRA] = etype_185
    #     missing_etype[grid.celltypes == VTK_HEXAHEDRON] = etype_185
    #     missing_etype[grid.celltypes == VTK_WEDGE] = etype_185
    #     missing_etype[grid.celltypes == VTK_PYRAMID] = etype_185

    #     etype_186 = etype_start
    #     missing_etype[grid.celltypes == VTK_QUADRATIC_HEXAHEDRON] = etype_186
    #     missing_etype[grid.celltypes == VTK_QUADRATIC_WEDGE] = etype_186
    #     missing_etype[grid.celltypes == VTK_QUADRATIC_PYRAMID] = etype_186

    #     etype_187 = etype_start + 1
    #     missing_etype[grid.celltypes == VTK_QUADRATIC_TETRA] = etype_187

    #     etype[missing_mask] = missing_etype

    #     typenum[missing_mask][missing_etype == etype_185] = 185
    #     typenum[missing_mask][missing_etype == etype_186] = 186
    #     typenum[missing_mask][missing_etype == etype_187] = 187

    #     header += 'ET, %d, 185%s' % (etype_185, line_ending)
    #     header += 'ET, %d, 186%s' % (etype_186, line_ending)
    #     header += 'ET, %d, 187%s' % (etype_187, line_ending)

    # number of nodes written per element
    elem_nnodes = np.empty(etype.size, np.int32)
    elem_nnodes[typenum == 185] = 8
    elem_nnodes[typenum == 186] = 20
    elem_nnodes[typenum == 187] = 10

    with open(str(filename), mode) as f:
        f.write(header)

        # write node block
        if write_nblock:
            write_nblock(f, nodenum, grid.points, line_ending=line_ending)

        # eblock header
        h = ''
        h += 'EBLOCK,19,SOLID,{:10d},{:10d}\r\n'.format(enum[-1], ncells)
        h += '(19i8)\r\n'
        f.write(h)

        # nnode = tets.shape[1]
        cells = grid.cells
        celltypes = grid.celltypes
        offset = grid.offset
        for i in range(ncells):
            c = offset[i]
            nnode = cells[c]
            c += 1

            # get nodes as a tuple
            nodes = nodenum[cells[c:c + nnode]]

            cellinfo = (mtype[i],          # Field 1: material reference number
                        etype[i],          # Field 2: element type number
                        rcon[i],           # Field 3: real constant reference number
                        1,                 # Field 4: section number
                        0,                 # Field 5: element coordinate system
                        0,                 # Field 6: Birth/death flag
                        0,                 # Field 7: 
                        0,                 # Field 8: 
                        elem_nnodes[i],    # Field 9: Number of nodes
                        0,                 # Field 10: Not Used
                        enum[i])           # Field 11: Element number
            line = '%8d%8d%8d%8d%8d%8d%8d%8d%8d%8d%8d' % cellinfo

            if celltypes[i] == VTK_QUADRATIC_TETRA:
                if typenum[i] == 187:
                    line += '%8d%8d%8d%8d%8d%8d%8d%8d\r\n%8d%8d\r\n' % tuple(nodes)
                else:  # must be 186
                    writenodes = (nodes[0],  # 0,  I
                                  nodes[1],  # 1,  J
                                  nodes[2],  # 2,  K
                                  nodes[2],  # 3,  L (duplicate of K)
                                  nodes[3],  # 4,  M
                                  nodes[3],  # 5,  N (duplicate of M)
                                  nodes[3],  # 6,  O (duplicate of M)
                                  nodes[3],  # 7,  P (duplicate of M)
                                  nodes[4],  # 8,  Q
                                  nodes[5],  # 9,  R
                                  nodes[3],  # 10, S (duplicate of K)
                                  nodes[6],  # 11, T
                                  nodes[3],  # 12, U (duplicate of M)
                                  nodes[3],  # 13, V (duplicate of M)
                                  nodes[3],  # 14, W (duplicate of M)
                                  nodes[3],  # 15, X (duplicate of M)
                                  nodes[7],  # 16, Y
                                  nodes[8],  # 17, Z
                                  nodes[9],  # 18, A
                                  nodes[9])  # 19, B (duplicate of A)

                    line += '%8d%8d%8d%8d%8d%8d%8d%8d\r\n' % writenodes[:8]
                    line += '%8d%8d%8d%8d%8d%8d%8d%8d%8d%8d%8d%8d\r\n' % writenodes[8:]


            elif celltypes[i] == VTK_TETRA:
                writenodes = (nodes[0],  # 0,  I
                              nodes[1],  # 1,  J
                              nodes[2],  # 2,  K
                              nodes[2],  # 3,  L (duplicate of K)
                              nodes[3],  # 4,  M
                              nodes[3],  # 5,  N (duplicate of M)
                              nodes[3],  # 6,  O (duplicate of M)
                              nodes[3])  # 7,  P (duplicate of M)
                line += '%8d%8d%8d%8d%8d%8d%8d%8d\r\n' % writenodes

            elif celltypes[i] == VTK_WEDGE:
                writenodes = (nodes[2],  # 0,  I
                              nodes[1],  # 1,  J
                              nodes[0],  # 2,  K
                              nodes[0],  # 3,  L (duplicate of K)
                              nodes[5],  # 4,  M
                              nodes[4],  # 5,  N
                              nodes[3],  # 6,  O
                              nodes[3])  # 7,  P (duplicate of O)
                line += '%8d%8d%8d%8d%8d%8d%8d%8d\r\n' % writenodes

            elif celltypes[i] == VTK_QUADRATIC_WEDGE:
                writenodes = (nodes[2],  # 0,  I
                              nodes[1],  # 1,  J
                              nodes[0],  # 2,  K
                              nodes[0],  # 3,  L (duplicate of K)
                              nodes[5],  # 4,  M
                              nodes[4],  # 5,  N
                              nodes[3],  # 6,  O
                              nodes[3],  # 7,  P (duplicate of O)
                              nodes[7],  # 8,  Q
                              nodes[6],  # 9,  R
                              nodes[0],  # 10, S   (duplicate of K)
                              nodes[8],  # 11, T
                              nodes[10], # 12, U
                              nodes[9],  # 13, V
                              nodes[3],  # 14, W (duplicate of O)
                              nodes[11], # 15, X
                              nodes[14], # 16, Y
                              nodes[13], # 17, Z
                              nodes[12], # 18, A
                              nodes[12]) # 19, B (duplicate of A)
                line += '%8d%8d%8d%8d%8d%8d%8d%8d\r\n' % writenodes[:8]
                line += '%8d%8d%8d%8d%8d%8d%8d%8d%8d%8d%8d%8d\r\n' % writenodes[8:]

            elif celltypes[i] == VTK_QUADRATIC_PYRAMID:
                writenodes = (nodes[0],  # 0,  I
                              nodes[1],  # 1,  J
                              nodes[2],  # 2,  K
                              nodes[3],  # 3,  L
                              nodes[4],  # 4,  M
                              nodes[4],  # 5,  N (duplicate of M)
                              nodes[4],  # 6,  O (duplicate of M)
                              nodes[4],  # 7,  P (duplicate of M)
                              nodes[5],  # 8,  Q
                              nodes[6],  # 9,  R
                              nodes[7],  # 10, S
                              nodes[8],  # 11, T
                              nodes[4],  # 12, U (duplicate of M)
                              nodes[4],  # 13, V (duplicate of M)
                              nodes[4],  # 14, W (duplicate of M)
                              nodes[4],  # 15, X (duplicate of M)
                              nodes[9],  # 16, Y
                              nodes[10], # 17, Z
                              nodes[11], # 18, A
                              nodes[12]) # 19, B (duplicate of A)

                line += '%8d%8d%8d%8d%8d%8d%8d%8d\r\n' % writenodes[:8]
                line += '%8d%8d%8d%8d%8d%8d%8d%8d%8d%8d%8d%8d\r\n' % writenodes[8:]

            elif celltypes[i] == VTK_PYRAMID:
                writenodes = (nodes[0],  # 0,  I
                              nodes[1],  # 1,  J
                              nodes[2],  # 2,  K
                              nodes[3],  # 3,  L
                              nodes[4],  # 4,  M
                              nodes[4],  # 5,  N (duplicate of M)
                              nodes[4],  # 6,  O (duplicate of M)
                              nodes[4])  # 7,  P (duplicate of M)
                line += '%8d%8d%8d%8d%8d%8d%8d%8d\r\n' % writenodes[:8]

            elif celltypes[i] == VTK_HEXAHEDRON:
                line += '%8d%8d%8d%8d%8d%8d%8d%8d\r\n' % tuple(nodes)

            elif celltypes[i] == VTK_QUADRATIC_HEXAHEDRON:
                line += '%8d%8d%8d%8d%8d%8d%8d%8d\r\n' % tuple(nodes[:8])
                line += '%8d%8d%8d%8d%8d%8d%8d%8d%8d%8d%8d%8d\r\n' % tuple(nodes[8:])

            else:
                raise Exception('Invalid write cell type %d' % celltypes[i])

            f.write(line)

        f.write('      -1\r\n')


def write_nblock(filename, node_id, pos, raw=None, writeangle=None,
                line_ending=None):
    """
    Numpy implementation of WriteNBLOCK that also includes the original node
    angles according to the raw cdb data if writeangle is enabled

    Parameters
    ----------
    filename : str or file handle
        Filename to write node block to.

    node_id : np.ndarray
        ANSYS Node numbers.

    pos : np.ndarray
        Node coordinates.

    raw : dict, optional
        Raw dictionary of original archive.

    writeangle : bool, optional
        Writes the node angles for each node.  Requires raw.

    line_ending : str, optional
        Line ending.

    """
    if line_ending is None:
        line_ending = os.linesep

    if not raw and writeangle:
        raise Exception('Cannot write angles without archive file')

    assert pos.ndim == 2 and pos.shape[1] == 3, 'Invalid position array'

    # Header Tell ANSYS to start reading the node block with 6 fields,
    # associated with a solid, the maximum node number and the number
    # of lines in the node block
    h = '/PREP7 \r\n'
    h += 'NBLOCK,6,SOLID,{:10d},{:10d}\r\n'.format(np.max(node_id), pos.shape[0])
    h += '(3i8,6e20.13)'

    # Make footer
    f = 'N,R5.3,LOC,       -1, \r\n'

    # Sort input data
    ind = np.argsort(node_id)
    node_id = node_id[ind]
    pos = pos[ind]

    # Write nodes using numpy
    if writeangle:
        # Create an empty array of node positions and angles
        posang = np.zeros((node_id.size, 6))
        posang[:, :3] = pos  # populate existing positions

        # Mask of raw nodes containing non-zero angles
        anglemask = np.any(raw['nodes'][:, -3:], 1)

        # Cross correlate those node ids with node_ids from current data
        maskA = np.in1d(node_id, raw['nnum'][anglemask])
        maskB = np.in1d(raw['nnum'][anglemask], node_id)
        posang[maskA, -3:] = raw['nodes'][anglemask][maskB, -3:]

        # stack node IDs and positions
        n = np.hstack((node_id.reshape(-1, 1), posang))
        np.savetxt(
            filename,
            n,
            '%8d       0       0' +
            '%20.13E' *
            6,
            header=h,
            footer=f,
            comments='',
            newline='\r\n')
    else:
        # stack node IDs and positions
        n = np.hstack((node_id.reshape(-1, 1), pos))
        np.savetxt(
            filename,
            n,
            '%8d       0       0' +
            '%20.13E' *
            3,
            header=h,
            footer=f,
            comments='',
            newline='\r\n')


def write_cmblock(filename, items, comp_name, comp_type, digit_width=10):
    """
    Writes a component block, CMBLOCK, to a file.

    Parameters
    ----------
    filename : str or file handle
        File to write CMBLOCK component to

    items : list or np.ndarray
        Element or node numbers to write.

    comp_name : str
        Name of the component

    comp_type : str
        Component type to write.  Should be either 'element' or 'node'.
    
    digit_width : int, optional
        Default 10
    """
    items = np.unique(items)

    toprint = []
    toprint.append(items[0])
    for i, value in enumerate(np.diff(items)):
        if value == 1:
            continue
        else:
            if items[i - 1] + 1 == items[i]:
                toprint.append(-items[i])
                toprint.append(items[i + 1])
            else:
                toprint.append(items[i + 1])

    # catch if last item is part of a list
    if toprint[-1] != abs(items[-1]):
        toprint.append(-items[i + 1])

    nitems = len(toprint)
    lines = []
    lines.append('CMBLOCK,%s,%s,%8d  ! from pyansys' % (comp_name.upper(),
                                                        comp_type.upper(),
                                                        nitems))
    lines.append('(8i%d)' % digit_width)
    digit_formatter = '%' + '%d' % digit_width + 'd'
    
    for chunk in chunks(toprint, 8):
        lines.append(''.join([digit_formatter] * len(chunk)) % tuple(chunk))

    lines.append('')

    # write file
    if sys.version_info[0] == 3:
        string_types = str
    else:
        string_types = basestring

    text = '\r\n'.join(lines)

    # either write to file or file object
    if isinstance(filename, string_types):
        open(filename, 'w').write(text)
    else:
        filename.write(text)
