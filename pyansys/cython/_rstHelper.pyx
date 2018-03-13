# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True

import ctypes
import numpy as np
cimport numpy as np

from libc.math cimport sqrt, fabs
from libc.stdio cimport fopen, FILE, fclose, fread, fseek
from libc.stdio cimport SEEK_CUR, ftell, SEEK_SET
from libc.string cimport memcpy

from libc.stdint cimport int32_t, int64_t


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
    
    
    
def AssembleEdges(int nelm, int [::1] etype, int [:, ::1] elem,
                  int [::1] numref, int [::1] edge_idx, int [::1] nodstr):
    
    cdef int i, j, nnod
    cdef int c = 0
    for i in range(nelm):
        nnod = nodstr[etype[i]]
        for j in range(nnod):
            edge_idx[c] = numref[elem[i, j]]
            c += 1
    
    


def LoadElementStress(filename, py_table_index, int64_t [::1] ele_ind_table, 
                      int64_t [::1] nodstr,int64_t [::1] etype, py_nitem, 
                      float [:, ::1] ele_data_arr, int64_t [::1] edge_idx):
    """ Read element results from ANSYS directly into a numpy array """
    
    cdef int64_t i, j, k, ind
    cdef int64_t table_index = py_table_index
    cdef int64_t nitem = py_nitem
    
    cdef FILE* cfile
    cdef bytes py_bytes = filename.encode()
    cdef char* c_filename = py_bytes
    cfile = fopen(c_filename, 'rb')
    
    cdef int64_t ele_table, ptr, nnode_elem
    cdef float [1000] ele_data
    cdef int64_t c = 0
    for i in range(len(ele_ind_table)):
        
        # get location of pointers to element data
        ele_table = ele_ind_table[i]
        fseek(cfile, (ele_table + table_index)*4, SEEK_SET)
        fread(&ptr, sizeof(int), 1, cfile)

        # Get the nodes in the element    
        nnode_elem = nodstr[etype[i]]

        # read the stresses evaluated at the intergration points or nodes
        fseek(cfile, (ele_table + ptr)*4, SEEK_SET)

        # fread(&ele_data, sizeof(float), nnode_elem*nitem, cfile)
        fread(&ele_data_arr[c, 0], sizeof(float), nnode_elem*nitem, cfile)
        c += nnode_elem

    fclose(cfile)


def LoadElementStressDouble(filename, py_table_index, int64_t [::1] ele_ind_table, 
                            int64_t [::1] nodstr,int64_t [::1] etype, int64_t nitem, 
                            double [:, ::1] ele_data_arr, int64_t [::1] edge_idx):
    """ Read element results from ANSYS directly into a numpy array """
    cdef int64_t i, j, k, ind
    cdef int64_t table_index = py_table_index
    
    cdef FILE* cfile
    cdef bytes py_bytes = filename.encode()
    cdef char* c_filename = py_bytes
    cfile = fopen(c_filename, 'rb')
    
    cdef int64_t ele_table, ptr, nnode_elem
    cdef double [1000] ele_data
    cdef int64_t c = 0
    for i in range(len(ele_ind_table)):
        
        # get location of pointers to element data
        ele_table = ele_ind_table[i]
        fseek(cfile, (ele_table + table_index)*4, SEEK_SET)
        fread(&ptr, sizeof(int), 1, cfile)

        # Get the nodes in the element    
        nnode_elem = nodstr[etype[i]]

        # read the stresses evaluated at the intergration points or nodes
        fseek(cfile, (ele_table + ptr)*4, SEEK_SET)

        # fread(&ele_data, sizeof(float), nnode_elem*nitem, cfile)
        fread(&ele_data_arr[c, 0], sizeof(float), nnode_elem*nitem, cfile)
        c += nnode_elem

    fclose(cfile)


def ReadElementStress(filename, py_table_index, int64_t [::1] ele_ind_table, 
                      int64_t [::1] nodstr,int64_t [::1] etype,
                      float [:, ::1] ele_data_arr, int64_t [::1] edge_idx,
                      int nitem):
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

        # read the stresses evaluated at the intergration points or nodes
        fseek(cfile, (ele_table + ptrENS)*4, SEEK_SET)

        nread = nnode_elem*nitem
        fread(&ele_data_arr[c, 0], sizeof(float), nread, cfile)
        c += nnode_elem

    fclose(cfile)


def ReadElementStressDouble(filename, py_table_index, int64_t [::1] ele_ind_table, 
                            int64_t [::1] nodstr,int64_t [::1] etype,
                            double [:, ::1] ele_data_arr, int64_t [::1] edge_idx):
    """ Read element results from ANSYS directly into a numpy array """
    cdef int64_t i, j, k, ind, nread
    cdef int64_t table_index = py_table_index
    
    cdef FILE* cfile
    cdef bytes py_bytes = filename.encode()
    cdef char* c_filename = py_bytes
    cfile = fopen(c_filename, 'rb')
    
    cdef int64_t ele_table, ptrENS, nnode_elem
    cdef int64_t c = 0
    for i in range(len(ele_ind_table)):
        # get location of pointers to element data
        ele_table = ele_ind_table[i]
        fseek(cfile, (ele_table + table_index)*4, SEEK_SET)
        fread(&ptrENS, sizeof(int), 1, cfile)

        # Get the nodes in the element    
        nnode_elem = nodstr[etype[i]]

        # read the stresses evaluated at the intergration points or nodes
        fseek(cfile, (ele_table + ptrENS)*4, SEEK_SET)

        nread = nnode_elem*6
        fread(&ele_data_arr[c, 0], sizeof(double), nread, cfile)
        c += nread

    fclose(cfile)


def LoadStress(filename, py_table_index, int64_t [::1] ele_ind_table, 
               int64_t [::1] nodstr,int64_t [::1] etype, int64_t nitem, 
               float [:, ::1] ele_data_arr, int64_t [::1] edge_idx):
    
    cdef int64_t i, j, k, ind
    cdef int64_t table_index = py_table_index
    
    cdef FILE* cfile
    cdef bytes py_bytes = filename.encode()
    cdef char* c_filename = py_bytes
    cfile = fopen(c_filename, 'rb')
    
    cdef int64_t ele_table, ptr, nnode_elem
    cdef float [1000] ele_data
    cdef int64_t c = 0
    for i in range(len(ele_ind_table)):
        
        # get location of pointers to element data
        ele_table = ele_ind_table[i]
        fseek(cfile, (ele_table + table_index)*4, SEEK_SET)
        fread(&ptr, sizeof(int), 1, cfile)

        # Get the nodes in the element    
        nnode_elem = nodstr[etype[i]]

        # read the stresses evaluated at the intergration points or nodes
        fseek(cfile, (ele_table + ptr)*4, SEEK_SET)
        fread(&ele_data, sizeof(float), nnode_elem*nitem, cfile)

        # store these values
        for j in range(nnode_elem):
            # corresponding edge indices for these component stressess
            ind = edge_idx[c]

            # [Sx Sy Sz Sxy Syz Sxz]
            for k in range(6):
                ele_data_arr[ind, k] += ele_data[k + nitem*j]

            c += 1

    fclose(cfile)
    
    
def LoadStressDouble(filename, py_table_index, int64_t [::1] ele_ind_table, 
                   int64_t [::1] nodstr,int64_t [::1] etype, int64_t nitem, 
                   double [:, ::1] ele_data_arr, int64_t [::1] edge_idx):
    
    cdef int64_t i, j, k, ind
    cdef int64_t table_index = py_table_index
    
    cdef FILE* cfile
    cdef bytes py_bytes = filename.encode()
    cdef char* c_filename = py_bytes
    cfile = fopen(c_filename, 'rb')
    
    cdef int64_t ele_table, ptr, nnode_elem
    cdef double [1000] ele_data
    cdef int64_t c = 0
    for i in range(len(ele_ind_table)):
        
        # get location of pointers to element data
        ele_table = ele_ind_table[i]
        fseek(cfile, (ele_table + table_index)*4, SEEK_SET)
        fread(&ptr, sizeof(int), 1, cfile)

        # Get the nodes in the element    
        nnode_elem = nodstr[etype[i]]

        # read the stresses evaluated at the intergration points or nodes
        fseek(cfile, (ele_table + ptr)*4, SEEK_SET)
        fread(&ele_data, sizeof(double), nnode_elem*nitem, cfile)

        # store these values
        for j in range(nnode_elem):
            # corresponding edge indices for these component stressess
            ind = edge_idx[c]

            # [Sx Sy Sz Sxy Syz Sxz]
            for k in range(6):
                ele_data_arr[ind, k] += ele_data[k + nitem*j]

            c += 1


    fclose(cfile)
    
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

    for i in range(nnode):
        s_xx = stress[i, 0]
        s_yy = stress[i, 1]
        s_zz = stress[i, 2]
        s_xy = stress[i, 3]
        s_yz = stress[i, 4]
        s_xz = stress[i, 5]

        # populate stress tensor
        stress_tensor[i, 0, 0] = s_xx
        stress_tensor[i, 0, 1] = s_xy
        stress_tensor[i, 0, 2] = s_xz
        stress_tensor[i, 1, 0] = s_xy
        stress_tensor[i, 1, 1] = s_yy
        stress_tensor[i, 1, 2] = s_yz
        stress_tensor[i, 2, 0] = s_xz
        stress_tensor[i, 2, 1] = s_yz
        stress_tensor[i, 2, 2] = s_zz

    # compute principle stresses
    w, v = np.linalg.eig(np.asarray(stress_tensor))
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

    return np.asarray(pstress)
