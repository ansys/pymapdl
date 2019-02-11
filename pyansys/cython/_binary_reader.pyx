# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True

import ctypes
import numpy as np
cimport numpy as np

from libc.math cimport sqrt, fabs, sin, cos
from libc.stdio cimport fopen, FILE, fclose, fread, fseek
from libc.stdio cimport SEEK_CUR, ftell, SEEK_SET
from libc.string cimport memcpy
from libc.stdint cimport int16_t, int32_t, int64_t

from cython.parallel import prange
ctypedef unsigned char uint8

cdef extern from "numpy/npy_math.h":
    bint npy_isnan(double x)

# VTK numbering for vtk cells
cdef uint8 VTK_EMPTY_CELL = 0
cdef uint8 VTK_VERTEX = 1
cdef uint8 VTK_LINE = 3

cdef uint8 VTK_TRIANGLE = 5
cdef uint8 VTK_QUAD = 9
cdef uint8 VTK_QUADRATIC_TRIANGLE = 22
cdef uint8 VTK_QUADRATIC_QUAD = 23

cdef uint8 VTK_TETRA = 10
cdef uint8 VTK_HEXAHEDRON = 12
cdef uint8 VTK_WEDGE = 13
cdef uint8 VTK_PYRAMID = 14
cdef uint8 VTK_QUADRATIC_TETRA = 24
cdef uint8 VTK_QUADRATIC_PYRAMID = 27
cdef uint8 VTK_QUADRATIC_WEDGE = 26
cdef uint8 VTK_QUADRATIC_HEXAHEDRON = 25

# cdef float DEG2RAD = 0.0174532925
cdef double DEG2RAD = 0.0174532925

# ELEMENT_INDEX_TABLE_KEYS = ['ptrEMS', 'ptrENF', 'ptrENS', 'ptrENG', 'ptrEGR',
#                             'ptrEEL', 'ptrEPL', 'ptrECR', 'ptrETH', 'ptrEUL',
#                             'ptrEFX', 'ptrELF', 'ptrEMN', 'ptrECD', 'ptrENL',
#                             'ptrEHC', 'ptrEPT', 'ptrESF', 'ptrEDI', 'ptrETB',
#                             'ptrECT', 'ptrEXY', 'ptrEBA', 'ptrESV', 'ptrMNL']

cdef int PTR_ENS_IDX = 2
cdef int PTR_EUL_IDX = 9


# from numpy cimport ndarray
# from cpython cimport list


# def CleanDuplicates(list element_stress, list enodes):
#     """
#     This will be optimized in the future

#     Removes duplicate nodes in element results
#     """
#     cdef int i
#     for i, enode in enumerate(enodes):
#         if unique_cython_int(enode) < len(enode):  # don't run unless it's not unique
#             unode, idx = np.unique(enode, return_index=True)
#         # if idx.size != enode.size:
#             enodes[i] = unode
#             element_stress[i] = element_stress[i][idx]


# cdef int unique_cython_int(ndarray[np.int32_t] a):
#     cdef int i
#     cdef int n = len(a)
#     cdef set s = set()
#     cdef set idx = set()
#     for i in range(n):
#         s.add(a[i])
#     return len(s)


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


def load_nodes(filename, int ptrLOC, int nnod, double [:, ::1] nloc, 
              int [::1] nnum):
    """
    Function signature
    def load_nodes(filename, int ptrLOC, int nnod, double [:, ::1] nloc, 
       int [::1] nnum):
        
    """
    
    cdef int i
    cdef int j
    
    cdef bytes buf
    with open(filename, "rb") as f:
        f.seek((ptrLOC + 2)*4)
        buf = f.read(nnod*68)
    
    cdef char * p = buf
    cdef int loc
    for i in range(nnod):
        # get node number (stored as double, cast to int)
        loc = i*68
        nnum[i] = <int>get_double(&p[loc])
        loc += 8
        for j in range(6):
            nloc[i, j] = get_double(&p[loc + j*8])


def LoadElements(filename, int ptr, int nelm, 
                 e_disp_table_py, int [:, ::1] elem, int [::1] etype, int [::1] mtype,
                 int [::1] rcon):
    """
    The following is stored for each element
    mat     - material reference number
    type    - element type number
    real    - real constant reference number
    secnum  - section number
    esys    - element coordinate system
    death   - death flat (1 live, 0 dead)
    solidm  - solid model reference
    shape   - coded shape key
    elnum   - element number
    baseeid - base element number
    NODES   - node numbers defining the element
    """
    
    cdef int i, j
    
    cdef int [::1] e_disp_table = e_disp_table_py.astype(ctypes.c_int)
    
    cdef bytes buf
    with open(filename, "rb") as f:
        f.seek(ptr*4)
        buf = f.read((e_disp_table[nelm - 1] + 32)*4)
        
    cdef char * p = buf
    cdef int loc
    
    cdef int val
    cdef int nread
    for i in range(nelm):
        # location in element table
        loc = e_disp_table[i]*4

        # determine number of nodes in element by getting entries in fortran header
        nread = get_int(&p[loc])
        # blank
        mtype[i] = get_int(&p[loc + 8])  # material type
        etype[i] = get_int(&p[loc + 12])  # element type
        rcon[i] = get_int(&p[loc + 16])  # real constant reference number

        # read in nodes
        for j in range(12, nread + 2):
            elem[i, j - 12] = get_int(&p[loc + 4*j])


def read_element_stress(filename, int64_t [::1] ele_ind_table, 
                        int64_t [::1] nodstr, int64_t [::1] etype,
                        float [:, ::1] ele_data_arr, int nitem,
                        int32_t [::1] element_type,
                        int as_global=1):
    """
    Read element results from ANSYS directly into a numpy array

    as_global : int, optional
        Rotates stresses from the element coordinate system to the global
        cartesian coordinate system.  Default True.

    """
    cdef int64_t i, j, k, ind, nread
    
    cdef FILE* cfile
    cdef bytes py_bytes = filename.encode()
    cdef char* c_filename = py_bytes
    cfile = fopen(c_filename, 'rb')

    cdef float [3] eulerangles
    
    cdef int64_t ele_table, nnode_elem
    cdef int32_t ptrENS, ptrEUL
    cdef int64_t c = 0
    for i in range(len(ele_ind_table)):
        # get location of element result pointers
        ele_table = ele_ind_table[i]

        # element stress pointer
        fseek(cfile, (ele_table + PTR_ENS_IDX)*4, SEEK_SET)
        fread(&ptrENS, sizeof(int32_t), 1, cfile)

        # Get the nodes in the element
        nnode_elem = nodstr[etype[i]]

        # if shell and keyopt 8 is 0, read top and bottom
        nread = nnode_elem*nitem

        if ptrENS < 0:  # negative pointer means missing data
            # skip this element
            for j in range(nnode_elem):
                for k in range(nitem):
                    ele_data_arr[c + j, k] = 0  # consider putting NAN instead
        else:
            # read the stresses evaluated at the intergration points or nodes
            fseek(cfile, (ele_table + ptrENS)*4, SEEK_SET)
            fread(&ele_data_arr[c, 0], sizeof(float), nread, cfile)

            # this will undoubtedly need to be generalized
            # element euler angle pointer
            if element_type[i] == 181 or element_type[i] == 281:
                fseek(cfile, (ele_table + PTR_EUL_IDX)*4, SEEK_SET)
                fread(&ptrEUL, sizeof(int32_t), 1, cfile)

                # only read the first three euler angles (thxy, thyz, thzx)
                fseek(cfile, (ele_table + ptrEUL)*4, SEEK_SET)
                fread(&eulerangles, sizeof(float), 3, cfile)

                # rotate the first four nodal results
                if as_global:
                    EulerRotate(ele_data_arr, eulerangles, c)

        c += nnode_elem

    fclose(cfile)


# this will have to be generalized at some point
cdef inline void EulerRotate(float [:, ::1] ele_data_arr,
                             float [3] eulerangles, int row):
    """
    Performs a 3-1-2 euler rotation given thxy, thyz, thzx in eulerangles

    Acts on rows 0 - 3 relative to row

    Specific to shell181 elements

    # used sympy to generate these equations
    tensor = np.matrix([[s_xx, s_xy, s_xz], 
                        [s_xy, s_yy, s_yz], 
                        [s_xz, s_yz, s_zz]])

    # always zero for shell elements...
    s_xz = 0
    s_zz = 0
    s_yz = 0

    from sympy import Matrix, symbols

    c1, c2, c3, s1, s2, s3, s_xx, s_yy, s_xy = symbols('c1 c2 c3 s1 s2 s3 s_xx s_yy s_xy')
    tensor = np.matrix([[s_xx, s_xy, 0], [s_xy, s_yy, 0], [0, 0, 0]])
    

    R = Matrix([[c1*c3 - s1*s2*s3, s1*c3 + c1*s2*s3, -s3*c2],
                [-s1*c2, c1*c2, s2],
                [c1*s3 + s1*s2*c3, s1*s3 - c1*c3*s2, c2*c3]])

    ans = R.T*tensor*R
    

    """    
    cdef double c1 = cos(DEG2RAD*eulerangles[0])
    cdef double c2 = cos(DEG2RAD*eulerangles[1])
    cdef double c3 = cos(DEG2RAD*eulerangles[2])

    cdef double s1 = sin(DEG2RAD*eulerangles[0])
    cdef double s2 = sin(DEG2RAD*eulerangles[1])
    cdef double s3 = sin(DEG2RAD*eulerangles[2])


    cdef double s_xx, s_xy, s_yy

    cdef int i, c
    for i in range(4):
        c = i + row

        # grab the element component stresses
        s_xx = ele_data_arr[c, 0]
        s_yy = ele_data_arr[c, 1]
        s_xy = ele_data_arr[c, 3]

        # the rest are zero (no out of plane stress)
        ele_data_arr[c, 0] = -c2*s1*(-c2*s1*s_yy + s_xy*(c1*c3 - s1*s2*s3)) + (c1*c3 - s1*s2*s3)*(-c2*s1*s_xy + s_xx*(c1*c3 - s1*s2*s3))
        ele_data_arr[c, 1] = c1*c2*(c1*c2*s_yy + s_xy*(c1*s2*s3 + c3*s1)) + (c1*c2*s_xy + s_xx*(c1*s2*s3 + c3*s1))*(c1*s2*s3 + c3*s1)
        ele_data_arr[c, 2] = -c2*s3*(-c2*s3*s_xx + s2*s_xy) + s2*(-c2*s3*s_xy + s2*s_yy)
        ele_data_arr[c, 3] = c1*c2*(-c2*s1*s_yy + s_xy*(c1*c3 - s1*s2*s3)) + (c1*s2*s3 + c3*s1)*(-c2*s1*s_xy + s_xx*(c1*c3 - s1*s2*s3))
        ele_data_arr[c, 4] = -c2*s3*(c1*c2*s_xy + s_xx*(c1*s2*s3 + c3*s1)) + s2*(c1*c2*s_yy + s_xy*(c1*s2*s3 + c3*s1))
        ele_data_arr[c, 5] = -c2*s3*(-c2*s1*s_xy + s_xx*(c1*c3 - s1*s2*s3)) + s2*(-c2*s1*s_yy + s_xy*(c1*c3 - s1*s2*s3))


def read_nodal_values(filename, uint8 [::1] celltypes,
                      int64_t [::1] ele_ind_table,
                      int64_t [::1] offsets, int64_t [::1] cells,
                      int nitems,
                      # int32_t [::1] validmask,
                      int npoints,
                      int32_t [::1] nodstr, int32_t [::1] etype,
                      int32_t [::1] element_type):
    """ Read element results from ANSYS directly into a numpy array """
    cdef int64_t i, j, k, ind, nread, offset
    cdef int64_t ncells = ele_ind_table.size

    cdef FILE* cfile
    cdef bytes py_bytes = filename.encode()
    cdef char* c_filename = py_bytes
    cfile = fopen(c_filename, 'rb')

    cdef int32_t [::1] ncount = np.zeros(npoints, ctypes.c_int32)
    cdef float [:, ::1] data = np.zeros((npoints, nitems), np.float32)
    cdef float [:, ::1] bufferdata = np.zeros((20, nitems), np.float32)

    cdef float [3] eulerangles

    cdef int64_t ele_table, nnode_elem
    cdef int32_t ptrENS, ptrEUL
    cdef int64_t c = 0
    cdef uint8 celltype
    for i in range(ncells):

        # skip if not valid type
        # if not validmask[i]:
            # continue
        
        # get location of element data
        ele_table = ele_ind_table[i]
        fseek(cfile, (ele_table + PTR_ENS_IDX)*4, SEEK_SET)
        fread(&ptrENS, sizeof(int32_t), 1, cfile)

        # Get the nodes in the element
        celltype = celltypes[i]
        offset = offsets[i] + 1
        
        nnode_elem = nodstr[etype[i]]
        # skip this element
        if ptrENS < 0:  # all zeros
            for j in range(nnode_elem):
                for k in range(nitems):
                    bufferdata[j, k] = 0
        else:
            fseek(cfile, (ele_table + ptrENS)*4, SEEK_SET)
            fread(&bufferdata[0, 0], sizeof(float), nnode_elem*nitems, cfile)        

            #### this will undoubtedly need to be generalized ####
            # element euler angle pointer
            if element_type[i] == 181:
                fseek(cfile, (ele_table + PTR_EUL_IDX)*4, SEEK_SET)
                fread(&ptrEUL, sizeof(int32_t), 1, cfile)

                # only read the first three euler angles (thxy, thyz, thzx)
                fseek(cfile, (ele_table + ptrEUL)*4, SEEK_SET)
                fread(&eulerangles, sizeof(float), 3, cfile)

                # rotate the first four nodal results
                EulerRotate(bufferdata, eulerangles, c)

        if celltype == VTK_LINE:  # untested
            ReadElement(cells, offset, ncount, data, bufferdata, nitems, cfile, 2)
        elif celltype == VTK_TRIANGLE:  # untested
            ReadElement(cells, offset, ncount, data, bufferdata, nitems, cfile, 3)
        elif celltype == VTK_QUAD or celltype == VTK_QUADRATIC_QUAD:
            ReadElement(cells, offset, ncount, data, bufferdata, nitems, cfile, 4)
        elif celltype == VTK_HEXAHEDRON:
            ReadElement(cells, offset, ncount, data, bufferdata, nitems, cfile, 8)
        elif celltype == VTK_PYRAMID:
            ReadElement(cells, offset, ncount, data, bufferdata, nitems, cfile, 5)
        elif celltype == VTK_TETRA:  # dependent on element type
            if nodstr[etype[i]] == 4:
                ReadElement(cells, offset, ncount, data, bufferdata, nitems, cfile, 4)
            else:
                ReadTetrahedral(cells, offset, ncount, data, bufferdata, nitems, cfile)
        elif celltype == VTK_WEDGE:
            ReadWedge(cells, offset, ncount, data, bufferdata, nitems, cfile)

    fclose(cfile)

    return np.asarray(data), np.asarray(ncount)

# indices of a wedge must be reordered (see _parser.StoreWeg)
cdef int64_t [6] wedge_ind
wedge_ind[0] = 2
wedge_ind[1] = 1
wedge_ind[2] = 0
wedge_ind[3] = 6
wedge_ind[4] = 5
wedge_ind[5] = 4

cdef inline void ReadWedge(int64_t [::1] cells, int64_t index, int32_t [::1] ncount,
                           float [:, ::1] data, float [:, ::1] bufferdata,
                           int nitems, FILE* cfile) nogil:
    """
    [0, 1, 2, 2, 3, 4, 5, 5]
    [0, 1, 2,  , 4, 5, 6,  ]
    """
    cdef int64_t i, j, cell, idx
    cdef int nread = nitems*8
    # fread(&bufferdata[0, 0], sizeof(float), nread, cfile)
    
    for i in range(6):
        cell = cells[index + i]
        ncount[cell] += 1
        idx = wedge_ind[i]
        for j in range(nitems):
            data[cell, j] += bufferdata[idx, j]


# indices of a 186 tetrahedral must be reordered (see _parser.StoreWeg)
cdef int64_t [6] tet_ind
tet_ind[0] = 0
tet_ind[1] = 1
tet_ind[2] = 2
tet_ind[3] = 4

cdef inline void ReadTetrahedral(int64_t [::1] cells, int64_t index, int32_t [::1] ncount,
                                 float [:, ::1] data, float [:, ::1] bufferdata,
                                 int nitems, FILE* cfile) nogil:
    """
    # see documentation at _parser.StoreTet
    """
    cdef int64_t i, j, cell, idx
    cdef int nread

    nread = nitems*5
    # fread(&bufferdata[0, 0], sizeof(float), nread, cfile)

    for i in range(4):
        cell = cells[index + i]
        ncount[cell] += 1
        idx = tet_ind[i]
        for j in range(nitems):
            data[cell, j] += bufferdata[idx, j]


cdef inline void ReadElement(int64_t [::1] cells, int64_t index, int32_t [::1] ncount,
                             float [:, ::1] data, float [:, ::1] bufferdata,
                             int nitems, FILE* cfile, int nnode) nogil:
    """
    Reads a generic element type in a linear fashion.  Works for:
    Hexahedron 95 or 186
    Pyramid 95 or 186
    Tetrahedral 187
    """
    cdef int64_t i, j, cell, idx
    # fread(&bufferdata[0, 0], sizeof(float), nitems*nnode, cfile)

    for i in range(nnode):
        cell = cells[index + i]
        ncount[cell] += 1
        for j in range(nitems):
            data[cell, j] += bufferdata[i, j]



def ReadArray(filename, int ptr, int nterm, int neqn, int [::1] const):
    """
    Reads stiffness or mass matrices from ANSYS fortran files

    Parameters
    ----------
    filename : string
        Full filename
        
    ptr: int
        Pointer to start of block
        
    nterm : int
        Number of terms to read.
        
    neqn : int
        Number of equations
        
    const : numpy int array
        If DOF is fixed

    Returns
    -------
    rows : numpy int32 array
        Row indices
    
    cols : numpy int32 array
        Column indices
    
    data : numpy double array
        Data belonging to (row, col)
    
    diag : numpy int32 array
        Indices along the diag (diag[i], diag[i])
    
    data_diag : numpy double array
        Data belonging to the diag entries
    
    
    Notes
    -----
    Function signature    
    ReadArray(filename, int ptrSTF, int nread, int nterm, int neqn,
              int [::1] const)
    """

    cdef int i, j, k, ind
    cdef bytes buf
    with open(filename, "rb") as f:
        f.seek(ptr*4)
        buf = f.read((neqn*6 + nterm*3)*4)

    cdef char * p = buf # python to c character array pointer
    cdef int loc = 0 # location long buffer
    
    # Number of terms is the number of terms stored in the upper triangle
    cdef int [::1] krow = np.empty(nterm, np.int32)
    cdef int [::1] kcol = np.empty(nterm, np.int32)
    cdef double [::1] kdata = np.empty(nterm)
    
    cdef int [::1] kdiag = np.empty(neqn, np.int32)
    cdef double [::1] kdata_diag = np.empty(neqn)
    
    cdef int c = 0 # index counter
    cdef int d = 0 # data counter
    cdef int c_diag = 0 # diag counter
    cdef int row, col, nitems, intval
    cdef double val
    
    for i in range(neqn):
        col = i
        
        # number of items to read
        nitems = get_int(&p[loc]); loc += 4
        loc += 4

        # Read indices
        for j in range(nitems):
            # get row number
            row = get_int(&p[loc]) - 1; loc += 4 # convert to c indexing

            if row < col:
                krow[c] = row
                kcol[c] = col
            else:
                krow[c] = col
                kcol[c] = row
            c += 1

        loc += 12
            
        # Read data
        for j in range(nitems):
            # Store data
            kdata[d] = get_double(&p[loc]); loc += 8
            d += 1

        # seek past end of data
        loc += 4
                    
    return np.asarray(krow)[:c], np.asarray(kcol)[:c], np.asarray(kdata)[:c]


def SortNodalEqlv(int neqn, int [::1] neqv, int [::1] ndof):
    """
    Reads in full file details required for the assembly of the mass and 
    stiffness matrices.

    The reference arrays are sorted by default, though this increases the
    bandwidth of the mass and stiffness matrices.

    Parameters
    ----------
    neqn : int
        Number of equations in full file.

    ndof : int [::1]
        Degrees of freedom for each node.

    neqv : int [::1]
        Nodal equivalance array.

    Returns
    -------
    dof_ref: numpy np.int32 array
        Sorted degree of freedom reference array.
        
    index_arr : numpy np.int32 array
        Index array to sort rows and columns.

    """
    cdef int i, j, ind

    # create sorting array
    cdef int nNodes = ndof.size
    cdef int [::1] cumdof = np.empty(nNodes, np.int32)
    cdef int csum = 0
    for i in range(nNodes):
        cumdof[i] = csum
        csum += ndof[i]
        
    cdef int [::1] s_neqv_dof = np.empty(neqn, np.int32)
    cdef int [::1] nref = np.empty(neqn, np.int32)
    cdef int [::1] dref = np.empty(neqn, np.int32)
    cdef int c = 0
    cdef int val
    for i in range(nNodes):
        val = neqv[i]
        for j in range(ndof[i]):
            nref[c] = val
            dref[c] = j
            c += 1

    # sort nodal equivalance array
    cdef int [::1] sidx = np.argsort(neqv).astype(np.int32)
    cdef int [::1] ndof_sort = np.empty(nNodes, np.int32)
    for i in range(nNodes):
        ndof_sort[i] = ndof[sidx[i]]

    cdef int d = 0
    # create an index array.  this tells the array readers where
    # to place each row and col when it's sorted
    cdef int [::1] index_arr = np.empty(neqn, np.int32)
    for i in range(nNodes):
        ind = sidx[i]
        c = cumdof[ind]
        for j in range(ndof[i]):
            s_neqv_dof[d] = c + j
            index_arr[c + j] = d
            d += 1

    # sort node and dof references
    cdef int [:, ::1] dof_ref = np.empty((neqn, 2), np.int32)
    for i in range(neqn):
        ind = s_neqv_dof[i]
        dof_ref[i, 0] = nref[ind]
        dof_ref[i, 1] = dref[ind]

    return np.asarray(dof_ref), np.asarray(index_arr), np.asarray(nref), \
           np.asarray(dref)


def tensor_arbitrary(double [:, :] stress, double [:, :] trans):
    """
    Rotates a 3D stress tensor by theta about the Z axis

    Notes:
    -----
    Used
    from sympy import Matrix, symbols
    s_xx, s_yy, s_zz, s_xy, s_yz, s_xz = symbols('s_xx s_yy s_zz s_xy s_yz s_xz')
    c0, c1, c2, c3, c4, c5, c6, c7, c8 = symbols('c0 c1 c2 c3 c4 c5 c6 c7 c8')
    
    R = Matrix([[c0, c1, c2], [c3, c4, c5], [c6, c7, c8]])
    tensor = Matrix([[s_xx, s_xy, s_xz], [s_xy, s_yy, s_yz], [s_xz, s_yz, s_zz]])
    R*tensor*R.T
    """
    cdef int nnode = stress.shape[0]
    cdef int i

    cdef int16_t [::1] isnan = np.zeros(nnode, np.int16)
    cdef double s_xx, s_yy, s_zz, s_xy, s_yz, s_xz
    cdef double c0 = trans[0, 0]
    cdef double c1 = trans[1, 0]
    cdef double c2 = trans[2, 0]
    cdef double c3 = trans[0, 1]
    cdef double c4 = trans[1, 1]
    cdef double c5 = trans[2, 1]
    cdef double c6 = trans[0, 2]
    cdef double c7 = trans[1, 2]
    cdef double c8 = trans[2, 2]

    cdef double r0, r1, r2, r3, r4, r5, r6, r7, r8

    for i in range(nnode):
        s_xx = stress[i, 0]
        if npy_isnan(s_xx):  # skip
            isnan[i] = 1
        else:
            s_yy = stress[i, 1]
            s_zz = stress[i, 2]
            s_xy = stress[i, 3]
            s_yz = stress[i, 4]
            s_xz = stress[i, 5]

        r0 = c0*(c0*s_xx + c1*s_xy + c2*s_xz) + c1*(c0*s_xy + c1*s_yy + c2*s_yz) + c2*(c0*s_xz + c1*s_yz + c2*s_zz)

        r1 = c3*(c0*s_xx + c1*s_xy + c2*s_xz) + c4*(c0*s_xy + c1*s_yy + c2*s_yz) + c5*(c0*s_xz + c1*s_yz + c2*s_zz)

        # r2 = c6*(c0*s_xx + c1*s_xy + c2*s_xz) + c7*(c0*s_xy + c1*s_yy + c2*s_yz) + c8*(c0*s_xz + c1*s_yz + c2*s_zz)

        # r3 = c0*(c3*s_xx + c4*s_xy + c5*s_xz) + c1*(c3*s_xy + c4*s_yy + c5*s_yz) + c2*(c3*s_xz + c4*s_yz + c5*s_zz)

        r4 = c3*(c3*s_xx + c4*s_xy + c5*s_xz) + c4*(c3*s_xy + c4*s_yy + c5*s_yz) + c5*(c3*s_xz + c4*s_yz + c5*s_zz)

        r5 = c6*(c3*s_xx + c4*s_xy + c5*s_xz) + c7*(c3*s_xy + c4*s_yy + c5*s_yz) + c8*(c3*s_xz + c4*s_yz + c5*s_zz)

        r6 = c0*(c6*s_xx + c7*s_xy + c8*s_xz) + c1*(c6*s_xy + c7*s_yy + c8*s_yz) + c2*(c6*s_xz + c7*s_yz + c8*s_zz)

        # r7 = c3*(c6*s_xx + c7*s_xy + c8*s_xz) + c4*(c6*s_xy + c7*s_yy + c8*s_yz) + c5*(c6*s_xz + c7*s_yz + c8*s_zz)

        r8 = c6*(c6*s_xx + c7*s_xy + c8*s_xz) + c7*(c6*s_xy + c7*s_yy + c8*s_yz) + c8*(c6*s_xz + c7*s_yz + c8*s_zz)

        stress[i, 0] = r0
        stress[i, 1] = r4
        stress[i, 2] = r8
        stress[i, 3] = r1
        stress[i, 4] = r5
        stress[i, 5] = r6

    return np.asarray(isnan).astype(np.bool)


def tensor_rotate_z(double [:, :] stress, float theta_z):
    """
    Rotates a 3D stress tensor by theta about the Z axis

    Notes:
    -----
    Used 
    from sympy import Matrix, symbols
    c, s, s_xx, s_yy, s_zz, s_xy, s_yz, s_xz = symbols('c s s_xx s_yy s_zz s_xy s_yz s_xz')

    R = Matrix([[c, -s, 0], [s, c, 0], [0, 0, 1]])
    tensor = Matrix([[s_xx, s_xy, s_xz], [s_xy, s_yy, s_yz], [s_xz, s_yz, s_zz]])
    R*tensor*R.T
    """
    cdef int nnode = stress.shape[0]
    cdef int i
    # cdef float [:, ::1] stress_rot = np.empty_like(stress)
    cdef int16_t [::1] isnan = np.zeros(nnode, np.int16)
    cdef double c, s, s_xx, s_yy, s_zz, s_xy, s_yz, s_xz

    c = cos(theta_z)
    s = sin(theta_z)

    for i in range(nnode):
        s_xx = stress[i, 0]
        if npy_isnan(s_xx):
            # stress_rot[i, 0] = 0
            # stress_rot[i, 1] = 0
            # stress_rot[i, 2] = 0
            # stress_rot[i, 3] = 0
            # stress_rot[i, 4] = 0
            # stress_rot[i, 5] = 0
            isnan[i] = 1
        else:
            s_yy = stress[i, 1]
            s_zz = stress[i, 2]
            s_xy = stress[i, 3]
            s_yz = stress[i, 4]
            s_xz = stress[i, 5]

        stress[i, 0] = c*(c*s_xx - s*s_xy) - s*(c*s_xy - s*s_yy)
        stress[i, 1] = c*(c*s_yy + s*s_xy) + s*(c*s_xy + s*s_xx)
        stress[i, 2] = s_zz
        stress[i, 3] = c*(c*s_xy - s*s_yy) + s*(c*s_xx - s*s_xy)
        stress[i, 4] = c*s_yz + s*s_xz
        stress[i, 5] = c*s_xz - s*s_yz

    return np.asarray(isnan).astype(np.bool)


def ComputePrincipalStress(float [:, ::1] stress):
    """
    Returns the principal stresses based on component stresses.

    Parameters
    ----------
    stress : numpy.ndarray
        Stresses at Sx Sy Sz Sxy Syz Sxz averaged at each corner node.

    Returns
    -------
    pstress : numpy.ndarray
        Principal stresses, stress intensity, and equivalant stress.
        [sigma1, sigma2, sigma3, sint, seqv]

    Notes
    -----
    ANSYS equivalant of:
    PRNSOL, S, PRIN

    Which returns:
    S1, S2, S3 principal stresses, SINT stress intensity, and SEQV
    equivalent stress.
    """
    # reshape the stress array into 3x3 stress tensor arrays
    cdef int nnode = stress.shape[0]
    cdef float [:, :, ::1] stress_tensor = np.empty((nnode, 3, 3), np.float32)
    cdef float s_xx, x_yy, s_zz, s_xy, s_yz, s_xz
    cdef int i

    cdef int16_t [::1] isnan = np.zeros(nnode, np.int16)

    for i in range(nnode):
        s_xx = stress[i, 0]
        if npy_isnan(s_xx):
            s_xx = 0
            s_yy = 0
            s_zz = 0
            s_xy = 0
            s_yz = 0
            s_xz = 0
            isnan[i] = 1
        else:
            s_yy = stress[i, 1]
            s_zz = stress[i, 2]
            s_xy = stress[i, 3]
            s_yz = stress[i, 4]
            s_xz = stress[i, 5]

        # populate lower triangle of stress tensor
        stress_tensor[i, 0, 0] = s_xx
        # stress_tensor[i, 0, 1] = s_xy
        # stress_tensor[i, 0, 2] = s_xz
        stress_tensor[i, 1, 0] = s_xy
        stress_tensor[i, 1, 1] = s_yy
        # stress_tensor[i, 1, 2] = s_yz
        stress_tensor[i, 2, 0] = s_xz
        stress_tensor[i, 2, 1] = s_yz
        stress_tensor[i, 2, 2] = s_zz

    # compute principle stresses
    # w =  np.linalg.eigvalsh(stress_tensor)  # default uses lower triangle
    # Access wrapped lapack libaray (slightly faster than above)
    w =  np.linalg._umath_linalg.eigvalsh_lo(stress_tensor)
    w[:, ::-1].sort(1)

    temp = np.empty((nnode, 5), np.float32)
    temp[:, :3] = w

    cdef float [:, ::1] pstress = temp
    cdef float p1, p2, p3, c1, c2, c3

    # compute stress intensity and von mises (equivalent) stress
    for i in range(nnode):
        p1 = pstress[i, 0]
        p2 = pstress[i, 1]
        p3 = pstress[i, 2]

        c1 = fabs(p1 - p2)
        c2 = fabs(p2 - p3)
        c3 = fabs(p3 - p1)

        if c1 > c2:
            if c1 > c3:
                pstress[i, 3] = c1
            else:
                pstress[i, 3] = c3
        else:
            if c2 > c3:
                pstress[i, 3] = c2
            else:
                pstress[i, 3] = c3

        pstress[i, 4] = sqrt(0.5*(c1**2 + c2**2 + c3**2))

    return np.asarray(pstress), np.asarray(isnan).astype(np.bool)




def affline_transform_double(double [:, ::1] points, double [:, ::1] t):
    """ Rigidly transforms points based on a 4x4 transform matrix """
    cdef int npoints = points.shape[0]
    cdef int i, j
    cdef double x, y, z
    cdef double xnew, ynew, znew

    cdef double t00 = t[0, 0]
    cdef double t01 = t[0, 1]
    cdef double t02 = t[0, 2]
    cdef double t03 = t[0, 3]

    cdef double t10 = t[1, 0]
    cdef double t11 = t[1, 1]
    cdef double t12 = t[1, 2]
    cdef double t13 = t[1, 3]

    cdef double t20 = t[2, 0]
    cdef double t21 = t[2, 1]
    cdef double t22 = t[2, 2]
    cdef double t23 = t[2, 3]

    for i in prange(npoints, nogil=True):
        x = points[i, 0]
        y = points[i, 1]
        z = points[i, 2]

        points[i, 0] = t00*x + t01*y + t02*z + t03
        points[i, 1] = t10*x + t11*y + t12*z + t13
        points[i, 2] = t20*x + t21*y + t22*z + t23


def affline_transform_float(float [:, ::1] points, double [:, ::1] t):
    """ Rigidly transforms points based on transform matrix t """
    cdef int npoints = points.shape[0]
    cdef int i
    cdef float x, y, z
    cdef float xnew, ynew, znew

    cdef float t00 = t[0, 0]
    cdef float t01 = t[0, 1]
    cdef float t02 = t[0, 2]
    cdef float t03 = t[0, 3]

    cdef float t10 = t[1, 0]
    cdef float t11 = t[1, 1]
    cdef float t12 = t[1, 2]
    cdef float t13 = t[1, 3]

    cdef float t20 = t[2, 0]
    cdef float t21 = t[2, 1]
    cdef float t22 = t[2, 2]
    cdef float t23 = t[2, 3]

    for i in prange(npoints, nogil=True):
        x = points[i, 0]
        y = points[i, 1]
        z = points[i, 2]

        points[i, 0] = t00*x + t01*y + t02*z + t03
        points[i, 1] = t10*x + t11*y + t12*z + t13
        points[i, 2] = t20*x + t21*y + t22*z + t23
