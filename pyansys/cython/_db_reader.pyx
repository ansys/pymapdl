# cython: boundscheck=False
# cython: wraparound=False

import ctypes
import numpy as np

from libc.math cimport sqrt, fabs, sin, cos
from libc.stdio cimport (fopen, FILE, fclose, fread, fseek, SEEK_CUR,
                         ftell, SEEK_SET)
from libc.string cimport memcpy
from libc.stdint cimport int64_t


cdef inline double get_double(char * array) nogil:
    cdef double result
    memcpy(&result, array, sizeof(result))
    return result


cdef inline double get_float(char * array) nogil:
    cdef float result
    memcpy(&result, array, sizeof(result))
    return result


cdef inline int get_int(char * array) nogil:
    cdef int result
    memcpy(&result, array, sizeof(result))
    return result



def read_db_nodes(filename, int nblock_loc, int nmax):
    """
    """
    cdef int i = 0

    cdef bytes py_bytes = filename.encode()
    cdef char* c_filename = py_bytes
    # cdef FILE* cfile = fopen(c_filename, 'rb')

    cdef int [::1] nnum = np.empty(nmax, np.int32)
    cdef double [:, ::1] nodes = np.empty((nmax, 3), np.double)

    # seek to start of nblock
    # fseek(cfile, nblock_loc + 12 + 16, SEEK_SET)

    cdef bytes buf
    with open(filename, "rb") as f:
        f.seek(nblock_loc + 12 + 16)
        buf = f.read(nmax*232)

    cdef int loc = 0
    cdef char *p = buf

    while True:
        nnum[i] = get_int(&p[loc])

        loc += 156 + 4
        nodes[i, 0] = get_double(&p[loc]); loc += 8
        nodes[i, 1] = get_double(&p[loc]); loc += 8
        nodes[i, 2] = get_double(&p[loc]); loc += 8

        # print(i, nnum[i], np.asarray(nodes[i]))

        loc += 32+16 

        # for j in range(100):
        #     print(get_int(&p[loc]), loc)
        #     loc += 4

        # break

        # if i == 340:
        #     break

        # # read node number
        # fread(&nnum[i], sizeof(int), 1, cfile)

        # # seek to node position and read it
        # fseek(cfile, 156, SEEK_CUR)
        # fread(&nodes[i, 0], sizeof(double), 3, cfile)
        # fseek(cfile, 32 + 16, SEEK_CUR)  # seek past end of data

        if nnum[i] == nmax:
            break

        i += 1

    # while True:
    #     # read node number
    #     fread(&nnum[i], sizeof(int), 1, cfile)

    #     # seek to node position and read it
    #     fseek(cfile, 156, SEEK_CUR)
    #     fread(&nodes[i, 0], sizeof(double), 3, cfile)
    #     fseek(cfile, 32 + 16, SEEK_CUR)  # seek past end of data

    #     if nnum[i] == nmax:
    #         break

    #     i += 1

    # fclosexo(cfile)
    # free(buf)

    i += 1
    return np.array(nnum[:i]), np.array(nodes[:i])


def read_db_elements(filename, int eblock_ptr, int emax):
    """
    """
    cdef int i = 0
    cdef int j

    cdef int [::1] enum = np.empty(emax, np.int32)
    cdef int [::1] mtype = np.empty(emax, np.int32)
    cdef int [::1] etype = np.empty(emax, np.int32)
    cdef int [:, ::1] elements = np.empty((emax, 20), np.int32)
    elements[:] = -1

    cdef bytes buf
    with open(filename, "rb") as f:
        f.seek(eblock_ptr - 4)
        buf = f.read(emax*552)

    cdef int loc = 0
    cdef char *p = buf
    cdef int nnod_elem, n_shift

    while True:
        loc += 4*8#; print(loc)
        enum[i] = get_int(&p[loc])

        # read element type
        loc += 4*15
        mtype[i] = get_int(&p[loc])

        loc += 4
        etype[i] = get_int(&p[loc])

        loc += 32*4
        n_shift = get_int(&p[loc])
        loc += 4*(9 + n_shift)

        nnod_elem = get_int(&p[loc])

        # print(enum[i], etype[i], nnod_elem)

        loc += 4*4
        for j in range(nnod_elem):
            elements[i, j] = get_int(&p[loc])
            # print(elements[i, j])
            loc += 4

        loc += 140

        if enum[i] == emax:
            break

        # if i == 2:
            # break

        i += 1

    i += 1
    return np.array(enum[:i]), np.array(elements[:i]), np.array(etype[:i]), np.array(mtype[:i])
