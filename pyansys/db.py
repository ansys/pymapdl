"""contains classes and methos to read in an ansys database file"""
import mmap
import warnings

import numpy as np

from pyansys import _db_reader
from pyansys.common import read_table, parse_header, read_standard_header
from pyansys.vtk_helper import raw_to_grid
from pyansys._reader import component_interperter


DB_HEADER_KEYS = ['fun16',
                  '',
                  'nmax',
                  'emax',
                  '',
                  '',
                  '',
                  '',
                  'netype',
]


# special ANSYS identifiers for element and node blocks
# import struct
# MAGIC_NUMBER = 39780477
# magic_str = struct.pack("<I", MAGIC_NUMBER)

MAGIC_NODE_STR = b'}\x00_\x02\x00\x00\x00\x00'  # 39780477
MAGIC_ELEM_STR = b'\x96\x00_\x02\x00\x00\x00'  # 39780502
MAGIC_ETYPE_STR = b'\n\x00_\x02\x00\x00\x00'  # 39780362
MAGIC_ECOMP_STR = b'\x08\x00_\x02\x00\x00\x00'


class Database():
    """read ansys *.db files"""

    def __init__(self, filename, debug=False):
        """Initialize database"""
        self.filename = filename
        self.header = read_db_header(filename)
        n_ncomp, n_ecomp = get_n_comp(filename)
        

        # read element and node blocks
        has_components = n_ncomp or n_ecomp
        nblock_ptr, elem_ptr, etype_ptr, ecomp_ptr = find_ptr(filename, get_ecomp_ptr=has_components)

        if debug == True:
            print('read_etype')

        self.ekey = None
        if etype_ptr != -1:
            self.ekey = read_etype(filename, etype_ptr, self.header['netype'])

        if debug == True:
            print('read_db_nodes')
        self.nnum, self.nodes = None, None
        if nblock_ptr != -1:
            self.nnum, self.nodes = _db_reader.read_db_nodes(filename, nblock_ptr, self.header['nmax'])

        if debug == True:
            print('read_db_elements')
        
        self.enum, self.elem, self.etype, self.mtype = None, None, None, None
        if elem_ptr != -1:
            self.enum, self.elem, self.etype, self.mtype = _db_reader.read_db_elements(filename,
                                                                                       elem_ptr,
                                                                                       self.header['emax'])

        if debug == True:
            print('read_db_components')

        self.node_comps = []
        self.elem_comps = []
        if ecomp_ptr != -1 and has_components:
            max_size = etype_ptr - ecomp_ptr
            self.node_comps, self.elem_comps = read_db_components(filename, ecomp_ptr, n_ncomp, n_ecomp, max_size)

        self.grid = None

    def parse_vtk(self, force_linear=False, allowable_types=None,
                  null_unallowed=False):
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
        # TODO: placeholders
        e_rcon = np.empty(0, np.int32)
        keyopt = []

        if self.nodes is None or self.elem is None:
            raise RuntimeError('Unable to parse to unstructured grid.  Missing node or element block')

        raw = {'keyopt': keyopt,
               'rnum': [],
               'rdat': [],
               'ekey': self.ekey,
               'nnum': self.nnum,
               'nodes': self.nodes,
               'enum': self.enum,
               'elem': self.elem,
               'etype': self.etype,
               'e_rcon': e_rcon,
               'mtype': self.mtype,
               'elem_comps': self.elem_comps,
               'node_comps': self.node_comps,
        }
        self.grid = raw_to_grid(raw, allowable_types, force_linear, null_unallowed)
        self.grid.point_arrays['angles'] = np.zeros_like(self.grid.points)
        return self.grid



# # def read_database_header(filename):
# #     """Reads database header"""


#     with open(filename, 'rb') as f:
#         # Read .RST FILE HEADER
#         f.seek(103 * 4)
#         header = parse_header(read_table(f), RESULT_HEADER_KEYS)
#         resultheader = merge_two_dicts(header, standard_header)


def find_ptr(filename, get_ecomp_ptr=True):
    """Identify node and element block pointers within a database file"""
    with open(filename, 'rb') as f:
        s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)

        etype_ptr = s.find(MAGIC_ETYPE_STR)
        if etype_ptr == -1:
             warnings.warn('Unable to find element type pointer.  File may be missing elements')

        if get_ecomp_ptr:
            ecomp_ptr = s.rfind(MAGIC_ECOMP_STR)
        else:
            ecomp_ptr = -1

        elem_ptr = s.find(MAGIC_ELEM_STR)
        if elem_ptr == -1:
            warnings.warn('Unable to find element block.  File may be missing elements')

        nblock_ptr = s.find(MAGIC_NODE_STR)
        if nblock_ptr == -1:
            warnings.warn('Unable to find node block. File may be missing nodes')

    return nblock_ptr, elem_ptr, etype_ptr, ecomp_ptr


def read_etype(filename, etype_ptr, n_etype):
    """Read etypes from ansys binary database file"""
    with open(filename, 'rb') as f:
        f.seek(etype_ptr + 4*14)
        buf = f.read(4*211*n_etype)

    loc = 0
    etypes = []
    for _ in range(n_etype):
        # entire record length is 200 ints
        etypes.append(np.frombuffer(buf[loc:], np.int32, 2))
        loc += 4*211 

    return np.asarray(etypes)


def read_db_header(filename):
    with open(filename, 'rb') as f:
        f.seek(103 * 4)
        return parse_header(read_table(f), DB_HEADER_KEYS)


def get_n_comp(filename):
    """Get the number of node and element components"""
    with open(filename, 'rb') as f:
        f.seek(103 * 4)

        for _ in range(200):
            tablesize = read_table(f, skip=True)
            # print(tablesize)
            if tablesize == 1240:
                break

        if tablesize == 1240:
            for _ in range(6):
                read_table(f, skip=True)

        return read_table(f, nread=2)

    raise Exception('Can not find node and element component length table')


def read_db_components(filename, ecomp_ptr, n_ncomp, n_ecomp, max_size):
    """Read node and element componetns from a database binary"""

    with open(filename, 'rb') as f:
        f.seek(ecomp_ptr + 4*4)
        buf = f.read(max_size)

    def read_component(loc):
        """ read a component given a buffer"""
        if np.frombuffer(buf[loc + 4*4:], np.int32, 1)[0] != 71827464:
            raise Exception('Unable to read component')
        nread = np.frombuffer(buf[loc + 4*6:], np.int32, 1)[0]
        comp_buf = buf[loc + 4*10:loc + 4*(nread + 10)]
        loc += 4*(nread + 11)
        name, component = parse_component_from_raw(comp_buf)
        return name, component, loc 

    elem_comp = {}
    loc = 0
    for _ in range(n_ecomp):
        name, component, loc = read_component(loc)
        elem_comp[name] = component

    node_comp = {}
    for _ in range(n_ncomp):
        name, component, loc = read_component(loc)
        node_comp[name] = component

    return node_comp, elem_comp


def parse_component_from_raw(comp_buf):
    name = comp_buf[:32].decode('utf')
    name =  name[:4][::-1] + name[4:8][::-1] + name[8:12][::-1] +\
            name[12:16][::-1] + name[16:20][::-1] + name[20:24][::-1] +\
            name[24:28][::-1] + name[28:32][::-1]
    name = name.strip()
    data = np.frombuffer(comp_buf[32:], np.int32)

    if data.size:
        comp = component_interperter(data)
    else:
        comp = np.empty(0, np.int32)

    return name, comp


# seek and read in first element definition
def py_read_elements(filename, elem_ptr, emax):
    with open(filename, 'rb') as f:
        f.seek(elem_ptr - 4)
        buf = f.read(emax*552)

    # breakpoint()
    loc = 0
    for i in range(2):
        print()
        print('iter', i)
        loc += 4*8
        print('elemnum', np.frombuffer(buf[loc:], np.int32, 1)) # element number?
        loc += 4*15

        print('mtype', np.frombuffer(buf[loc:], np.int32, 1)) # etype
        loc += 4
        print('etype', np.frombuffer(buf[loc:], np.int32, 1)) # etype

        loc += 32*4
        n_shift = np.frombuffer(buf[loc:], np.int32, 1)[0]
        print('nshift', n_shift)
        loc += 4*(9 + n_shift)

        loc += 4*4
        for j in range(nnodes):
            print('nodenum', j, np.frombuffer(buf[loc:], np.int32, 1))  # element nodes
            loc += 4

        loc += 140

