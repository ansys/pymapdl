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

import ctypes

import numpy as np
cimport numpy as np


cdef extern from "reader.h":
    int read_nblock(char*, int*, double*, int, int, int, int*, int, int)
    int read_eblock(char*, int*, int*, int*, int*, int*, int*, int, int, int*,
                    int)

    
cdef int myfgets(char *outstr, char *instr, int *n, int fsize):
    """ Copies a single line from instr to outstr starting from position n """
    
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
    cdef int EOL
    cdef int n = 0
    
    # Detect end of line character
    # while n < fsize:
    #     if raw[n] == '\r':
    #         EOL = 2
    #         break
    #     elif raw[n] == '\n':
    #         EOL = 1
    #         break
    #     n += 1

    # Reset line position
    # n = 0
    
    # Define variables
    cdef size_t l = 0
    cdef ssize_t read
    cdef int[5] blocksz
    cdef int i, j
    cdef int tempint
    cdef int linelen, isz
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
    cdef int [:, ::1] elem = np.empty((0, 0), ctypes.c_int)
    cdef int [::1] etype = np.empty(0, ctypes.c_int)
    cdef int [::1] elemnum = np.empty(0, ctypes.c_int)
    cdef int [::1] e_rcon = np.empty(0, ctypes.c_int)
    cdef int [::1] mtype = np.empty(0, ctypes.c_int)
    cdef int [::1] sec_id = np.empty(0, ctypes.c_int)

    # CMBLOCK
    cdef int ncomp
    cdef int [::1] component
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
                elem_type.append([int(line[3:line.find(b',', 5)]),
                                  int(line[line.find(b',', 5) + 1:])])

            elif b'EBLOCK' in line:
                if debug:
                    print('reading EBLOCK')
                eblock_read = True

                # Get size of EBLOCK
                nelem = int(line[line.rfind(b',') + 1:])

                # Get interger block size
                myfgets(line, raw, &n, fsize)
                isz = int(line[line.find(b'i') + 1:line.find(b')')])

                # Initialize element data array.  Use number of lines
                # as nelem is unknown
                elem = np.empty((nelem, 20), dtype=ctypes.c_int)
                etype = np.empty(nelem, dtype=ctypes.c_int)
                elemnum = np.empty(nelem, dtype=ctypes.c_int)
                e_rcon = np.empty(nelem, dtype=ctypes.c_int)
                mtype = np.empty(nelem, dtype=ctypes.c_int)
                sec_id = np.empty(nelem, dtype=ctypes.c_int)

                # Call C extention to read eblock
                nelem = read_eblock(raw, &mtype[0], &etype[0],
                                    &e_rcon[0], &sec_id[0],
                                    &elemnum[0], &elem[0, 0], nelem,
                                    isz, &n, EOL)

                if nelem == 0:
                    raise Exception('Unable to read element block')

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
                if debug:
                    print('reading NBLOCK')

                nodes_read = True
                # Get size of NBLOCK
                nnodes = int(line[line.rfind(b',') + 1:])

                # Get format of NBLOCK
                if myfgets(line, raw, &n, fsize): raise Exception(badstr)
                d_size, f_size, nfld, nexp = block_format(line)
                nnum = np.empty(nnodes, dtype=ctypes.c_int)
                nodes = np.empty((nnodes, 6))

                n = read_nblock(raw, &nnum[0], &nodes[0, 0], nnodes,
                                d_size, f_size, &n, EOL, nexp)

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
                    d_size, f_size, nfld, nexp = block_format(line)
                    nnum = np.empty(nnodes, dtype=ctypes.c_int)
                    nodes = np.empty((nnodes, 6))

                    n = read_nblock(raw, &nnum[0], &nodes[0, 0], nnodes,
                                    d_size, f_size, &n, EOL, nexp)

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
                    elem = np.empty((nelem, 20), dtype=ctypes.c_int)
                    etype = np.empty(nelem, dtype=ctypes.c_int)
                    elemnum = np.empty(nelem, dtype=ctypes.c_int)
                    e_rcon = np.empty(nelem, dtype=ctypes.c_int)
                    mtype = np.empty(nelem, dtype=ctypes.c_int)
                    sec_id = np.empty(nelem, dtype=ctypes.c_int)

                    # Call C extention to read eblock
                    nelem = read_eblock(raw, &mtype[0], &etype[0],
                                        &e_rcon[0], &sec_id[0],
                                        &elemnum[0], &elem[0, 0], nelem,
                                        isz, &n, EOL)

                    if nelem == 0:
                        raise Exception('Unable to read element block')

    # Free memory
    free(raw)

    return {'rnum': np.asarray(rnum),
            'rdat': np.asarray(rdat),
            'ekey': np.asarray(elem_type, ctypes.c_int),
            'nnum': np.asarray(nnum),
            'nodes': np.asarray(nodes),
            'enum': np.asarray(elemnum[:nelem]),
            'elem': np.array(elem[:nelem]),
            'etype': np.asarray(etype[:nelem]),
            'e_rcon': np.asarray(e_rcon[:nelem]),
            'node_comps': node_comps,
            'elem_comps': elem_comps,
            'mtype': np.asarray(mtype),  # material type
            'sec_id': np.asarray(sec_id),
            'keyopt': keyopt,
            'parameters': parameters
            }


def block_format(string):
    """ Get node block format """
    # Digit Size
    d_size = int(string[string.find(b'i') + 1:string.find(b',')])
    f_size = int(string[string.find(b'e') + 1:string.find(b'.')])

    # get number of possible intergers in the float scientific notation
    if b'e' in string[string.find(b'.'):]:
        st = string.find(b'.')
        st += string[st:].find(b'e') + 1
        nexp = int(string[st:].replace(b')', b''))
    else:  # sub ANSYS v17
        nexp = 2
    nfields = int(string[string.find(b',') + 1:string.find(b'e')])

    return d_size, f_size, nfields, nexp


def component_interperter(component):
    """
    If a node is negative, it is describing a list from the previous
    node.  This is ANSYS's way of saving file size when writing
    components.

    This function has not been optimized.

    """
    f_new = []
    for i in range(len(component)):
        if component[i] > 0: # Append if positive
            f_new.append(component[i])
        else: # otherwise, append list
            f_new.append(range(abs(component[i - 1]) + 1, abs(component[i]) + 1))
    
    return np.hstack(f_new).astype(ctypes.c_int)
