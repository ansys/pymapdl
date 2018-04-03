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


cdef inline double GetDouble(char * array) nogil:
    cdef double result
    memcpy(&result, array, sizeof(result))
    return result


cdef inline double GetFloat(char * array) nogil:
    cdef float result
    memcpy(&result, array, sizeof(result))
    return result


cdef inline int GetInt(char * array) nogil:
    cdef int result
    memcpy(&result, array, sizeof(result))
    return result


def LoadNodes(filename, int ptrLOC, int nnod, double [:, ::1] nloc, 
              int [::1] nnum):
    """
    Function signature
    def LoadNodes(filename, int ptrLOC, int nnod, double [:, ::1] nloc, 
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
        nnum[i] = <int>GetDouble(&p[loc])
        loc += 8
        for j in range(6):
            nloc[i, j] = GetDouble(&p[loc + j*8])
    
    
def LoadElements(filename, int ptr, int nelm, 
                 e_disp_table_py, int [:, ::1] elem, int [::1] etype):
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
        nread = GetInt(&p[loc])
        
        # read in element type
        etype[i] = GetInt(&p[loc + 12])
        
        # read in nodes
        for j in range(12, nread + 2):
            elem[i, j - 12] = GetInt(&p[loc + 4*j])


# def AssembleEdges(int nelm, int [::1] etype, int [:, ::1] elem,
#                   int [::1] numref, int [::1] edge_idx, int [::1] nodstr):
    
#     cdef int i, j, nnod
#     cdef int c = 0
#     for i in range(nelm):
#         nnod = nodstr[etype[i]]
#         for j in range(nnod):
#             edge_idx[c] = numref[elem[i, j]]
#             c += 1


# def LoadElementStress(filename, py_table_index, int64_t [::1] ele_ind_table, 
#                       int64_t [::1] nodstr,int64_t [::1] etype, py_nitem, 
#                       float [:, ::1] ele_data_arr, int64_t [::1] edge_idx):
#                       # int32_t [::1] validmask):
#     """ Read element results from ANSYS directly into a numpy array """
    
#     cdef int64_t i, j, k, ind
#     cdef int64_t table_index = py_table_index
#     cdef int64_t nitem = py_nitem
    
#     cdef FILE* cfile
#     cdef bytes py_bytes = filename.encode()
#     cdef char* c_filename = py_bytes
#     cfile = fopen(c_filename, 'rb')
    
#     cdef int64_t ele_table, ptr, nnode_elem
#     cdef float [1000] ele_data
#     cdef int64_t c = 0
#     for i in range(len(ele_ind_table)):
        
#         # get location of pointers to element data
#         ele_table = ele_ind_table[i]
#         fseek(cfile, (ele_table + table_index)*4, SEEK_SET)
#         fread(&ptr, sizeof(int), 1, cfile)

#         # Get the nodes in the element    
#         nnode_elem = nodstr[etype[i]]

#         # read the stresses evaluated at the intergration points or nodes
#         fseek(cfile, (ele_table + ptr)*4, SEEK_SET)

#         # read the values if the element has stress
#         # if validmask[i]:
#         fread(&ele_data_arr[c, 0], sizeof(float), nnode_elem*nitem, cfile)

#         c += nnode_elem

#     fclose(cfile)


# def LoadElementStressDouble(filename, py_table_index, int64_t [::1] ele_ind_table, 
#                             int64_t [::1] nodstr, int64_t [::1] etype, int64_t nitem, 
#                             double [:, ::1] ele_data_arr, int64_t [::1] edge_idx):
#     """ Read element results from ANSYS directly into a numpy array """
#     cdef int64_t i, j, k, ind
#     cdef int64_t table_index = py_table_index
    
#     cdef FILE* cfile
#     cdef bytes py_bytes = filename.encode()
#     cdef char* c_filename = py_bytes
#     cfile = fopen(c_filename, 'rb')
    
#     cdef int64_t ele_table, ptr, nnode_elem
#     cdef double [1000] ele_data
#     cdef int64_t c = 0
#     for i in range(len(ele_ind_table)):
        
#         # get location of pointers to element data
#         ele_table = ele_ind_table[i]
#         fseek(cfile, (ele_table + table_index)*4, SEEK_SET)
#         fread(&ptr, sizeof(int), 1, cfile)

#         # Get the nodes in the element    
#         nnode_elem = nodstr[etype[i]]

#         # read the stresses evaluated at the intergration points or nodes
#         fseek(cfile, (ele_table + ptr)*4, SEEK_SET)

#         # fread(&ele_data, sizeof(float), nnode_elem*nitem, cfile)
#         fread(&ele_data_arr[c, 0], sizeof(float), nnode_elem*nitem, cfile)
#         c += nnode_elem

#     fclose(cfile)



def ReadElementStress(filename, py_table_index, int64_t [::1] ele_ind_table, 
                      int64_t [::1] nodstr, int64_t [::1] etype,
                      float [:, ::1] ele_data_arr, int nitem, int32_t [::1] validmask):
    """ Read element results from ANSYS directly into a numpy array """
    cdef int64_t i, j, k, ind, nread
    cdef int64_t table_index = py_table_index
    
    cdef FILE* cfile
    cdef bytes py_bytes = filename.encode()
    cdef char* c_filename = py_bytes
    cfile = fopen(c_filename, 'rb')
    
    cdef int64_t ele_table, nnode_elem
    cdef int32_t ptrENS
    cdef int64_t c = 0
    for i in range(len(ele_ind_table)):
        # get location of pointers to element data
        ele_table = ele_ind_table[i]
        fseek(cfile, (ele_table + table_index)*4, SEEK_SET)
        fread(&ptrENS, sizeof(int32_t), 1, cfile)

        # Get the nodes in the element
        nnode_elem = nodstr[etype[i]]
        nread = nnode_elem*nitem

        if ptrENS < 0:
            # skip this element
            for j in range(nnode_elem):
                for k in range(nitem):
                    ele_data_arr[c + j, k] = 0
        elif validmask[i]:
            # read the stresses evaluated at the intergration points or nodes
            fseek(cfile, (ele_table + ptrENS)*4, SEEK_SET)
            fread(&ele_data_arr[c, 0], sizeof(float), nread, cfile)

        c += nnode_elem

    fclose(cfile)


def ReadNodalValues(filename, py_table_index, uint8 [::1] celltypes,
                    int64_t [::1] ele_ind_table,
                    int64_t [::1] offsets, int64_t [::1] cells,
                    int nitems, int32_t [::1] validmask, int npoints,
                    int32_t [::1] nodstr, int32_t [::1] etype):
    """ Read element results from ANSYS directly into a numpy array """
    cdef int64_t i, j, k, ind, nread, offset
    cdef int64_t ncells = ele_ind_table.size
    cdef int64_t table_index = py_table_index

    cdef FILE* cfile
    cdef bytes py_bytes = filename.encode()
    cdef char* c_filename = py_bytes
    cfile = fopen(c_filename, 'rb')

    cdef int32_t [::1] ncount = np.zeros(npoints, ctypes.c_int32)
    cdef float [:, ::1] data = np.zeros((npoints, nitems), np.float32)
    cdef float [:, ::1] bufferdata = np.zeros((20, nitems), np.float32)

    cdef int64_t ele_table, nnode_elem
    cdef int32_t ptrENS
    cdef int64_t c = 0
    cdef uint8 celltype
    for i in range(ncells):

        # skip if not valid type
        if not validmask[i]:
            continue
        
        # get location of element data
        ele_table = ele_ind_table[i]
        fseek(cfile, (ele_table + table_index)*4, SEEK_SET)
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

        if celltype == VTK_LINE:  # untested
            ReadElement(cells, offset, ncount, data, bufferdata, nitems, cfile, 2)
        elif celltype == VTK_TRIANGLE:  # untested
            ReadElement(cells, offset, ncount, data, bufferdata, nitems, cfile, 3)
        elif celltype == VTK_QUAD:  # untested
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
        nitems = GetInt(&p[loc]); loc += 4
        loc += 4

        # Read indices
        for j in range(nitems):
            # get row number
            row = GetInt(&p[loc]) - 1; loc += 4 # convert to c indexing

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
            kdata[d] = GetDouble(&p[loc]); loc += 8
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


def TensorRotateZ(double [:, :] stress, float theta_z):
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


from numpy cimport ndarray
from cpython cimport list

def CleanDuplicates(list element_stress, list enodes):
    """
    This will be optimized in the future

    Removes duplicate nodes in element results
    """
    cdef int i
    for i, enode in enumerate(enodes):
        if unique_cython_int(enode) < len(enode):  # don't run unless it's not unique
            unode, idx = np.unique(enode, return_index=True)
        # if idx.size != enode.size:
            enodes[i] = unode
            element_stress[i] = element_stress[i][idx]


cdef int unique_cython_int(ndarray[np.int32_t] a):
    cdef int i
    cdef int n = len(a)
    cdef set s = set()
    cdef set idx = set()
    for i in range(n):
        s.add(a[i])
    return len(s)
