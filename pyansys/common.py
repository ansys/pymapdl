"""Methods common to binary files
Documentation taken from:
https://www.sharcnet.ca/Software/Ansys/16.2.3/en-us/help/ans_prog/Hlp_P_INT1_1.html

"""
import struct
import os
from collections import Counter

import numpy as np
import pyvista as pv

from pyansys._binary_reader import c_read_record
from pyansys import _binary_reader

STRESS_TYPES = ['X', 'Y', 'Z', 'XY', 'YZ', 'XZ']
PRINCIPAL_STRESS_TYPES = ['S1', 'S2', 'S3', 'SINT', 'SEQV']
STRAIN_TYPES = ['X', 'Y', 'Z', 'XY', 'YZ', 'XZ', 'EQV']
THERMAL_STRAIN_TYPES = ['X', 'Y', 'Z', 'XY', 'YZ', 'XZ', 'EQV', 'ESWELL']

ANSYS_BINARY_FILE_TYPES = {2: 'Element Matrix File',
                           3: 'Element Save Data file',
                           4: 'Full stiffness-mass matrix File',
                           8: 'Substructure Matrices File',
                           9: 'Modal Results File',
                           10: 'Reduced Displacement File',
                           12: 'Result File',
                           16: 'Database File',
                           45: 'Component Mode Synthesis Matrices (CMS) File'}



# c *** standard usage of the block number (buffers) and file unit number(FUN)
# c     for the ansys files
# c
# c     File     FileName   Unit File    Block      Description
# c     EMAT ->    EMATNM       FUN02        2      element matrices
# c     ESAV ->    ESAVNM       FUN03        1      element save data
# c     R000 ->    R000NM       FUN03        7      element save data
# c     FULL ->    FULLNM       FUN04        3      full matrices
# c     EROT ->    EROTNM       FUN07        4      element matrices
# c     SUB  ->    SUBNM        FUN08        8/7    substructuring
# c     MODE ->    MODENM       FUN09        8 (7)  mode file
# c     RDSP ->    RDSPNM       FUN10        7      Reduced displacement file
# c     RFRQ ->    RFRQNM       FUN10        7      Reduced complex displacement (MSUP)
# c     TRI  ->    TRINM        FUN11        3      tri stiffness
# c     RST  ->    RSTNM        FUN12        6      results
# c     DSUB ->    DSUBNM       FUN13        5      displacement substructure
# c                             FUN14               input file?
# c                             FUN15               output file?
# c     RDB  ->                 FUN16               back up file
# c                             FUN17               temporary file (used in different cases)
# c     MODEL->    MODENM_LEFT  FUN19       19      mode file for left eigen modes
# c     SCR1 ->                 FUN22               scratch file
# c     SCR2 ->                 FUN23               scratch file
# c     SCR3 ->                 FUN24               scratch file
# c     SCR4 ->                 FUN26               scratch file
# c     TMP  ->                 FUN28               temporary file used for rewrite a file
# c     OPT  ->                 FUN36               optimization data file
# c     LN40 ->                 FUN40               Boeing reduced matrix
# c     LN41 ->                 FUN41               Boeing reduced matrix
# c     LN42 ->                 FUN42               Boeing reduced matrix
# c     MLV  ->                 FUN43        8      load vector file (substructure)
# c                             FUN44               ?
# c     IST  ->                 FUN63               initial stress file
# c     ASI  ->    ASIRSTNM     FUN66        9      asi results


class AnsysBinary():
    """ANSYS binary file class"""
    filename = None

    def read_record(self, pointer, return_bufsize=False):
        """Reads a record at a given position.

        Because ANSYS 19.0+ uses compression by default, you must use
        this method rather than ``np.fromfile``.

        Parameters
        ----------
        pointer : int
            ANSYS file position (n words from start of file).  A word
            is four bytes.

        return_bufsize : bool, optional
            Returns the number of words read (includes header and
            footer).  Useful for determining the new position in the
            file after reading a record.

        Returns
        -------
        record : np.ndarray
            The record read as a ``n x 1`` numpy array.

        bufsize : float, optional
            When ``return_bufsize`` is enabled, returns the number of
            words read.

        """
        return c_read_record(self.filename, pointer, return_bufsize)


def read_binary(filename, **kwargs):
    """Reads ANSYS-written binary files:
    - Jobname.RST: Result file from structural analysis
    - Jobname.RTH: Result file from a thermal analysis
    - Jobname.EMAT: Stores data related to element matrices
    - Jobname.FULL: Stores the full stiffness-mass matrix

    Parameters
    ----------
    filename : str
        Filename to read.

    **kwargs : keyword arguments
        See the individual classes for additional keyword arguments.

    Examples
    --------
    >>> import pyansys
    >>> result = pyansys.read_binary('file.rst')
    >>> result = pyansys.read_binary('file.rst')
    >>> full_file = pyansys.read_binary('file.full')
    >>> emat_file = pyansys.read_binary('file.emat')

    Notes
    -----
    The following file types are unsupported
    - Jobname.DSUB file, storing displacements related to substructure
      matrices
    - Jobname.SUB file, storing data related to substructure matrices
    - Jobname.RFRQ file, storing data related to a mode-superposition
      harmonic analysis
    - The Jobname.RDSP file, storing data related to a
      mode-superposition transient analysis.
    - Jobname.MODE file, storing data related to a modal analysis
    - Jobname.RMG A magnetic analysis
    - Jobname.RFL A FLOTRAN analysis (a legacy results file)
    """
    if not os.path.isfile(filename):
        raise FileNotFoundError('%s is not a file or cannot be found' %
                                str(filename))

    # return BinaryFile(filename)
    file_format = read_standard_header(filename)['file format']

    if file_format == 2:
        from pyansys.emat import EmatFile
        return EmatFile(filename, **kwargs)
    elif file_format == 4:
        from pyansys.full import FullFile
        return FullFile(filename, **kwargs)
    elif file_format == 12:
        from pyansys.rst import ResultFile
        read_mesh = kwargs.pop('read_mesh', True)
        result = ResultFile(filename, read_mesh=False, **kwargs)

        # check if it's a cyclic result file
        ignore_cyclic = kwargs.pop('ignore_cyclic', False)
        if result.header['nSector'] != 1 and not ignore_cyclic:
            from pyansys.cyclic_reader import CyclicResult
            return CyclicResult(filename)

        if read_mesh:
            result._store_mesh()

        return result

    # elif file_format == 16:
    #     from pyansys.db import Database
    #     return Database(filename, debug=kwargs.pop('debug', False))

    # No file matches
    file_type = ANSYS_BINARY_FILE_TYPES.get(file_format, str(file_format))
    raise RuntimeError('ANSYS binary "%s" not supported' % file_type)


def read_table(f, dtype='i', nread=None, skip=False, get_nread=True, cython=False):
    """ read fortran style table """
    if cython:
        arr, bufsz = c_read_record(f.name, f.tell()//4, True)
        f.seek(bufsz*4, 1)
        return arr

    if get_nread:
        n = np.fromfile(f, 'i', 1)
        if not n:
            raise Exception('end of file')

        tablesize = n[0]
        if dtype is None:  # read flags to get data type
            # ansys_dtype = np.fromfile(f, 'i', 1)
            flags = f.read(4)[-1]
            type_flag = flags >> 0 & 1
            prec_flag = flags >> 1 & 1
            # zlib_flag = flags >> 2 & 1
            sparse_flag = flags >> 3 & 1
            if sparse_flag:
                raise NotImplementedError('Cannot read sparse results.\nPlease run with "/FCOMP,RST,0" to disable writing sparse results')

            if type_flag:
                if prec_flag:
                    dtype = 'short'
                else:
                    dtype = 'i'
            else:
                if prec_flag:
                    dtype = 'float'
                else:
                    dtype = 'double'
        else:
            f.seek(4, 1)  # skip padding

    # override
    if nread:
        tablesize = nread

    if skip:
        f.seek((tablesize + 1)*4, 1)
        return tablesize
    else:
        if dtype == 'double':
            tablesize //= 2
        table = np.fromfile(f, dtype, tablesize)
    f.seek(4, 1)  # skip padding
    return table


def read_string_from_binary(f, n):
    """Read n 4 character binary strings from a file opend in binary
    mode
    """
    string = b''
    for _ in range(n):
        string += f.read(4)[::-1]

    try:
        return string.decode('utf')
    except:
        return string


def parse_header(table, keys):
    """ parses a header from a table """
    header = {}
    max_entry = len(table) - 1
    # some keys occure multiple times and refer to arrays of some sort
    counter = Counter(keys)
    del counter['0']

    # initialize lists/arrays
    for key, count in counter.items():
        if count > 1:
            header[key] = []

    for i, key in enumerate(keys):
        if i > max_entry:
            header[key] = 0
        else:
            if counter[key]>1:  # multiple items in the header -> list/array
                if table[i]:  # skip zeros
                    header[key].append(table[i])
            else:
                header[key] = table[i] 

    for key in keys:
        if 'ptr' in key and key[-1] == 'h':
            basekey = key[:-1]
            intl = header[basekey + 'l']
            inth = header[basekey + 'h']
            header[basekey] = two_ints_to_long(intl, inth)

    # remove empty entries
    header.pop('_', None)
    return header


def two_ints_to_long(intl, inth):
    """ Interpert two ints as one long """
    longint = struct.pack(">I", inth) + struct.pack(">I", intl)
    return struct.unpack('>q', longint)[0]


def read_standard_header(filename):
    """ Reads standard header """
    with open(filename, 'rb') as f:

        endian = '<'
        if np.fromfile(f, dtype='<i', count=1) != 100:

            # Check if big enos
            f.seek(0)
            if np.fromfile(f, dtype='>i', count=1) == 100:
                endian = '>'

            # Otherwise, it's probably not a result file
            else:
                raise Exception('Unable to determine endian type.  ' +
                                'Possibly not an ANSYS binary file')

        f.seek(0)

        header = {}
        header['endian'] = endian
        header['file number'] = read_table(f, nread=1, get_nread=False)[0]
        header['file format'] = read_table(f, nread=1, get_nread=False)[0]
        int_time = str(read_table(f, nread=1, get_nread=False)[0])
        header['time'] = ':'.join([int_time[0:2], int_time[2:4], int_time[4:]])
        int_date = str(read_table(f, nread=1, get_nread=False)[0])
        if int_date == '-1':
            header['date'] = ''
        else:
            header['date'] = '/'.join([int_date[0:4], int_date[4:6], int_date[6:]])

        unit_types = {0: 'User Defined',
                      1: 'SI',
                      2: 'CSG',
                      3: 'U.S. Customary units (feet)',
                      4: 'U.S. Customary units (inches)',
                      5: 'MKS',
                      6: 'MPA',
                      7: 'uMKS'}
        header['units'] = unit_types[read_table(f, nread=1, get_nread=False)[0]]

        f.seek(11 * 4)
        version = read_string_from_binary(f, 1).strip()

        header['verstring'] = version
        header['mainver'] = int(version[:2])
        header['subver'] = int(version[-1])

        # there's something hidden at 12
        f.seek(4, 1)

        # f.seek(13 * 4)
        header['machine'] = read_string_from_binary(f, 3).strip()
        header['jobname'] = read_string_from_binary(f, 2).strip()
        header['product'] = read_string_from_binary(f, 2).strip()
        header['special'] = read_string_from_binary(f, 1).strip()
        header['username'] = read_string_from_binary(f, 3).strip()

        # Items 23-25 The machine identifier in integer form (three four-character strings)
        # this contains license information
        header['machine_identifier'] = read_string_from_binary(f, 3).strip()

        # Item 26 The system record size
        header['system record size'] = read_table(f, nread=1, get_nread=False)[0]

        # Item 27 The maximum file length
        # header['file length'] = read_table(f, nread=1, get_nread=False)[0]

        # Item 28 The maximum record number
        # header['the maximum record number'] = read_table(f, nread=1, get_nread=False)[0]

        # Items 31-38 The Jobname (eight four-character strings)
        f.seek(32*4)
        header['jobname2'] = read_string_from_binary(f, 8).strip()

        # Items 41-60 The main analysis title in integer form (20 four-character strings)
        f.seek(42*4)
        header['title'] = read_string_from_binary(f, 20).strip()

        # Items 61-80 The first subtitle in integer form (20 four-character strings)
        header['subtitle'] = read_string_from_binary(f, 20).strip()

        # Item 95 The split point of the file (0 means the file will not split)
        f.seek(96*4)
        header['split point'] = read_table(f, nread=1, get_nread=False)[0]

        # Items 97-98 LONGINT of the maximum file length (bug here)
        # ints = read_table(f, nread=2, get_nread=False)
        # header['file length'] = two_ints_to_long(ints[0], ints[1])

    return header


def midside_mask(grid):
    """Returns a mask of midside nodes

    Parameters
    ----------
    grid : pyvista.UnstructuredGrid
        Grid to check.

    Returns
    -------
    mask : bool np.ndarray
        True when a midside node.
    """
    return _binary_reader.midside_mask(grid.celltypes,
                                       grid.cells,
                                       grid.offset,
                                       grid.number_of_points)


def rotate_to_global(result, euler_angles):
    """Rotate a result set to the global coordinate system

    ANSYS writes the results in the nodal coordinate system and
    they use the ZXY euler rotation method.

    Rotates results in-place.

    Parameters
    ----------
    result : np.ndarray
        Nodal result set to rotate.  Sized ``n_node`` x ``ndof``

    euler_angles : np.ndarray
        Array of euler angles sized 3 x ``n_node`` in degrees.

    """
    theta_xy, theta_yz, theta_zx = euler_angles
    if np.any(theta_xy):
        pv.common.axis_rotation(result, theta_xy, inplace=True, axis='z')

    if np.any(theta_yz):
        pv.common.axis_rotation(result, theta_yz, inplace=True, axis='x')

    if np.any(theta_zx):
        pv.common.axis_rotation(result, theta_zx, inplace=True, axis='y')
