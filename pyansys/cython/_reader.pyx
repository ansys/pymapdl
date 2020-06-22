# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True

""" Cython implementation of a CDB reader """
from libc.stdio cimport fopen, FILE, fclose, sscanf, fscanf, fread, fseek
from libc.stdio cimport fgets, printf, SEEK_CUR, SEEK_END, ftell, SEEK_SET
from libc.stdlib cimport atoi, atof
from libc.stdlib cimport malloc, free
from libc.string cimport strncpy, strcmp
from libc.stdint cimport int64_t
ctypedef unsigned char uint8_t

import ctypes

import numpy as np
cimport numpy as np


cdef extern from "reader.h":
    int read_nblock(char*, int*, double*, int, int*, int, int*)
    int read_eblock(char*, int*, int*, int, int, int*)

cdef extern from 'vtk_support.h':
    int ans_to_vtk(int, int*, int*, int*, int, int*, int64_t*, int64_t*, uint8_t*, int)

cdef int myfgets(char *outstr, char *instr, int *n, int fsize):
    """Copies a single line from instr to outstr starting from position n """
    
    cdef int k = n[0]
    
    # Search line at a maximum of 10000 characters
    cdef int i, c
    c = n[0]
    for i in range(1000):
        # check if end of file
        if c > fsize:
            return 1
            
        # Add null character if at end of line
        if instr[c] == '\r':
            n[0] += i + 2
            outstr[i] = '\0'
            return 0
        elif instr[c] == '\n':
            n[0] += i + 1
            outstr[i] = '\0'
            return 0
            
        # Otherwise, store data to output string
        outstr[i] = instr[c]
        c += 1
        
    # Line exceeds 1000 char (unlikely with ANSYS CDB formatting)
    return 1


def read(filename, read_parameters=False, debug=False):
    """
    Read blocked ansys archive file.
    """
    badstr = 'Badly formatted cdb file'
    filename_byte_string = filename.encode("UTF-8")
    cdef char* fname = filename_byte_string
    parameters = {}
    # Check file exists
    cdef FILE* cfile
    cfile = fopen(fname, 'r')

    if cfile == NULL:
        raise Exception("No such file or directory: '%s'" % filename)

    # Load entire file to memory
    fseek(cfile, 0, SEEK_END)
    cdef int fsize = ftell(cfile)
    fseek(cfile, 0, SEEK_SET)
    cdef char *raw = < char * >malloc(fsize*sizeof(char))
    fread(raw, 1, fsize, cfile)
    fclose(cfile)
    
    # File counter
    cdef int tmpval, start_pos
    cdef int n = 0
    
    # Define variables
    cdef size_t l = 0
    cdef ssize_t read
    cdef int[5] blocksz
    cdef int i, j, linelen, isz, tempint
    cdef float tempflt

    # Size temp char array
    cdef char line[1000]
    cdef char tempstr[100]
    
    # Get element types
    elem_type = []
    rnum = []
    rdat = []

    # NBLOCK
    cdef int nnodes = 0
    cdef int [::1] nnum = np.empty(0, ctypes.c_int)
    cdef double [:, ::1] nodes = np.empty((0, 0))

    # EBLOCK
    cdef int nelem = 0
    cdef int elem_sz = 0
    cdef int [::1] elem = np.empty(0, ctypes.c_int)
    cdef int [::1] elem_off = np.empty(0, ctypes.c_int)

    # CMBLOCK
    cdef int ncomp
    cdef int [::1] component
    cdef int [::1] d_size
    cdef int nblock
    node_comps = {}
    elem_comps = {}

    nodes_read = False
    eblock_read = False

    # keyopt
    keyopt = {}

    # Read data up to and including start of NBLOCK
    while 1:
        if myfgets(line, raw, &n, fsize):
            break

        # Record element types
        if 'E' == line[0]:
            if b'ET' in line:
                if debug:
                    print('reading ET')


                # element number
                # element type
                et_val = line.decode().split(',')
                elem_type.append([int(et_val[1]), int(et_val[2])])
                # elem_type.append([int(line[3:line.find(b',', 5)]),
                                  # int(line[line.find(b',', 5) + 1:])])

            elif b'EBLOCK' in line:
                if debug:
                    print('reading EBLOCK')
                eblock_read = True

                # Get size of EBLOCK
                nelem = int(line[line.rfind(b',') + 1:])
                if nelem == 0:
                    raise Exception('Unable to read element block')

                # Get interger block size
                myfgets(line, raw, &n, fsize)
                isz = int(line[line.find(b'i') + 1:line.find(b')')])

                # Populate element field data and connectivity
                elem = np.empty(nelem*30, dtype=ctypes.c_int)
                elem_off = np.empty(nelem + 1, dtype=ctypes.c_int)
                elem_sz = read_eblock(raw, &elem_off[0], &elem[0], nelem, isz, &n)

        elif b'K' == line[0]:
            if b'KEYOP' in line:
                if debug:
                    print('reading KEYOP')

                try:
                    entry = []
                    for item in line.split(b',')[1:]:
                        entry.append(int(item))
                except:
                    continue

                key_num = int(entry[0])
                if key_num in keyopt:
                    keyopt[key_num].append(entry[1:])
                else:
                    keyopt[key_num] = [entry[1:]]

        elif 'R' == line[0]:
            if b'RLBLOCK' in line:
                if debug:
                    print('reading RLBLOCK')

                # Get number of sets
                ist = line.find(b',') + 1
                ien = line[ist:].find(b',') + ist
                nset = int(line[ist:ien])

                # Skip Format1 and Format2 (always 2i8,6g16.9 and 7g16.9)
                if myfgets(line, raw, &n, fsize): raise Exception(badstr)
                if myfgets(line, raw, &n, fsize): raise Exception(badstr)

                # Read data
                c_set = 0
                while True:
                    if myfgets(line, raw, &n, fsize): raise Exception(badstr)
                    rcon = [] # real constants
                    c_set += 1
                    if c_set > nset:
                        break

                    # Get real constant number
                    rnum.append(int(line[:8]))

                    # Number of constants
                    ncon = int(line[8:16])

                    # Get constant data
                    if ncon > 6: # if multiple lines
                        for i in range(6):
                            rcon.append(float(line[16 + 16*i:32 + 16*i]))
                            ncon -= 1
                            
                        # advance line
                        if myfgets(line, raw, &n, fsize): raise Exception(badstr)
                        
                        # read next line
                        while True:
                            if ncon > 7:
                                for i in range(7):
                                    rcon.append(float(line[16*i:16*(i + 1)]))
                                    ncon -= 1
                                # advance
                                if myfgets(line, raw, &n, fsize): raise Exception(badstr)
                                
                            else:
                                for i in range(ncon):
                                    try: 
                                        rcon.append(float(line[16*i:16 + 16*i]))  
                                    # account for empty 0 values
                                    except:
                                        rcon.append(0.0)
                                    
                                break
                            
                    # If only one in constant data
                    else:
                        for i in range(ncon):
                            rcon.append(float(line[16 + 16*i:32 + 16*i]))   
            
                    rdat.append(rcon)

        elif 'N' == line[0]: # Test is faster than next line
            # if line contains the start of the node block
            if b'NBLOCK' in line:
                start_pos = n
                if debug:
                    print('reading NBLOCK')

                nodes_read = True
                # Get size of NBLOCK
                nnodes = int(line[line.rfind(b',') + 1:])
                # this value may be wrong... 

                # Get format of NBLOCK
                if myfgets(line, raw, &n, fsize):
                    raise Exception('Unable to read nblock format line or '
                                    'at end of file.')
                d_size, f_size, nfld, nexp = node_block_format(line)
                nnum = np.empty(nnodes, dtype=ctypes.c_int)
                nodes = np.empty((nnodes, 6))

                n = read_nblock(raw, &nnum[0], &nodes[0, 0], nnodes,
                                &d_size[0], f_size, &n)

                # verify at the end of the block
                if myfgets(line, raw, &n, fsize):
                    raise Exception('Unable to read end of nblock or at end of file')

                if 'N,R5.3,LOC' not in line.decode().replace(' ', ''):
                    if debug:
                        print('N,R5.3,LOC not at end of block')
                    # need to reread the number of nodes
                    n = start_pos
                    if myfgets(line, raw, &n, fsize): raise Exception(badstr)
                    nnodes = 0
                    while True:
                        if myfgets(line, raw, &n, fsize): raise Exception(badstr)
                        if 'N,R5.3,LOC' not in line.decode().replace(' ', ''):
                            break
                        nnodes += 1

                    # reread nodes
                    n = start_pos
                    if myfgets(line, raw, &n, fsize): raise Exception(badstr)
                    d_size, f_size, nfld, nexp = node_block_format(line)
                    nnum = np.empty(nnodes, dtype=ctypes.c_int)
                    nodes = np.zeros((nnodes, 6))

                    n = read_nblock(raw, &nnum[0], &nodes[0, 0], nnodes,
                                    &d_size[0], f_size, &n)


        elif 'C' == line[0]:  # component
            if b'CMBLOCK' in line:  # component
                if debug:
                    print('reading CMBLOCK')

                line_comp_type = line.split(b',')[2]
                # Get Component name
                ind1 = line.find(b',') + 1
                ind2 = line.find(b',', ind1)
                comname = line[ind1:ind2].decode()

                # Get number of items
                ncomp = int(line[line.rfind(b',') + 1:line.find(b'!')])
                component = np.empty(ncomp, ctypes.c_int)

                # Get interger size
                myfgets(line, raw, &n, fsize)
                isz = int(line[line.find(b'i') + 1:line.find(b')')])
                tempstr[isz] = '\0'

                # Number of intergers per line
                nblock = int(line[line.find(b'(') + 1:line.find(b'i')])

                # Extract nodes
                for i in range(ncomp):

                    # Read new line if at the end of the line
                    if i%nblock == 0:
                        myfgets(line, raw, &n, fsize)

                    strncpy(tempstr, line + isz*(i%nblock), isz)
                    component[i] = atoi(tempstr)

                # Convert component to array and store
                if b'NODE' in line_comp_type:
                    node_comps[comname] = component_interperter(component)

                elif b'ELEM' in line_comp_type:
                    elem_comps[comname] = component_interperter(component)

        elif '*' == line[0] and read_parameters:  # dim
            if b'DIM' in line:
                _, name, _, dim0, dim1, dim2, _ = line.decode().split(',')

                # dim = []
                # for d in [dim0, dim1, dim2]:
                #     if d.strip():
                #         dim.append(int(d))

                # while dim[-1] == 1:
                #     if len(dim) == 1:
                #         break
                #     del dim[-1]

                # init_arr = np.zeros(np.prod(dim))

                myfgets(line, raw, &n, fsize)
                if b'PREAD' in line:
                    if debug:
                        print('reading PREAD')

                    _, name, arr_size = line.decode().split(',')
                    name = name.strip()
                    st = n
                    en = raw.find(b'END PREAD', n)
                    if debug:
                        print(st, en)
                    if st != -1 and en != -1:
                        lines = raw[st:en].split()
                        arr = np.genfromtxt(raw[st:en].split())
                        # init_arr[arr.size] = arr
                        parameters[name] = arr

    # if the node block was not read for some reason
    if not nodes_read:
        n = 0
        while 1:
            if myfgets(line, raw, &n, fsize):
                break

            if 'N' == line[0]: # Test is faster than next line
                # if line contains the start of the node block
                if b'NBLOCK' in line:
                    # Get size of NBLOCK
                    nnodes = int(line[line.rfind(b',') + 1:])

                    # Get format of NBLOCK
                    if myfgets(line, raw, &n, fsize): raise Exception(badstr)
                    d_size, f_size, nfld, nexp = node_block_format(line)
                    nnum = np.empty(nnodes, dtype=ctypes.c_int)
                    nodes = np.empty((nnodes, 6))

                    n = read_nblock(raw, &nnum[0], &nodes[0, 0], nnodes,
                                    &d_size[0], f_size, &n)

    # if eblock was not read for some reason
    if not eblock_read:
        n = 0
        while 1:
            if myfgets(line, raw, &n, fsize):
                break

            if 'E' == line[0]:  # faster to test one character
                if b'EBLOCK' in line:
                    if debug:
                        print('reading EBLOCK')

                    # Get size of EBLOCK
                    nelem = int(line[line.rfind(b',') + 1:])

                    # Get interger block size
                    myfgets(line, raw, &n, fsize)
                    isz = int(line[line.find(b'i') + 1:line.find(b')')])

                    if debug:
                        print('nelem:', nelem)
                        print('isz:', isz)

                    # Initialize element data array.  Use number of lines
                    # as nelem is unknown
                    # Populate element field data and connectivity
                    elem = np.empty(nelem*30, dtype=ctypes.c_int)
                    elem_off = np.empty(nelem + 1, dtype=ctypes.c_int)
                    elem_sz = read_eblock(raw, &elem_off[0], &elem[0], nelem, isz,
                                               &n)

                    if nelem == 0:
                        raise Exception('Unable to read element block')

    # Free memory
    free(raw)

    return {'rnum': np.asarray(rnum),
            'rdat': np.asarray(rdat),
            'ekey': np.asarray(elem_type, ctypes.c_int),
            'nnum': np.asarray(nnum),
            'nodes': np.asarray(nodes),
            'elem': np.array(elem[:elem_sz]),
            'elem_off': np.array(elem_off),
            'node_comps': node_comps,
            'elem_comps': elem_comps,
            'keyopt': keyopt,
            'parameters': parameters
            }


def node_block_format(string):
    """ Get node block format

    Example formats:
    (3i9,6e21.13e3)
    3 ints, all 9 digits wide followed by 6 floats

    (1i7,2i9,6e21.13)
    1 int 7 digits wide, 2 ints, 9 digits wide, 6 floats
    """
    string = string.decode().replace('(', '').replace(')', '')
    fields = string.split(',')

    # double and float size
    d_size = np.empty(3, np.int32)
    nexp = 2  # default when missing
    nfields = 6
    f_size = 21
    c = 0 
    for field in fields:
        if 'i' in field:
            items = field.split('i')
            for n in range(int(items[0])):
                d_size[c] = int(items[1])
                c += 1
        elif 'e' in field:
            f_size = int(field.split('e')[1].split('.')[0])

            # get number of possible intergers in the float scientific notation
            if 'e' in field.split('.')[1]:
                nexp = int(field.split('.')[1].split('e')[1])

            nfields = int(field.split('e')[0])

    return d_size, f_size, nfields, nexp


def component_interperter(component):
    """If a node is negative, it is describing a list from the
    previous node.  This is ANSYS's way of saving file size when
    writing components.

    This function has not been optimized.

    """
    f_new = []
    for i in range(len(component)):
        if component[i] > 0: # Append if positive
            f_new.append(component[i])
        else: # otherwise, append list
            f_new.append(range(abs(component[i - 1]) + 1, abs(component[i]) + 1))
    
    return np.hstack(f_new).astype(ctypes.c_int)


def ans_vtk_convert(int [::1] elem, int [::1] elem_off, int [::1] type_ref,
                    int [::1] nnum, int build_offset):
    """Convert ansys style connectivity to VTK connectivity"""
    cdef int nelem = elem_off.size - 1
    cdef int64_t [::1] offset = np.empty(nelem, ctypes.c_int64)
    cdef uint8_t [::1] celltypes = np.empty(nelem, dtype='uint8')

    # Allocate connectivity
    # max cell size is 20 (VTK_HEXAHEDRAL) and cell header is 1
    cdef int64_t [::1] cells = np.empty(nelem*21, ctypes.c_int64)
    cdef int loc = ans_to_vtk(nelem, &elem[0], &elem_off[0],
                              &type_ref[0], nnum.size, &nnum[0],
                              &offset[0], &cells[0], &celltypes[0],
                              build_offset)

    return np.asarray(offset), np.asarray(celltypes), np.asarray(cells[:loc])
