# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True

import ctypes
import numpy as np
cimport numpy as np

from libc.stdio cimport fopen, FILE, fclose, fread, fseek
from libc.stdio cimport SEEK_CUR, ftell, SEEK_SET
from libc.string cimport memcpy


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
    
    
def LoadStress(filename, int table_index, int [::1] ele_ind_table, 
               int [::1] nodstr,int [::1] etype, int nitem, 
               float [:, ::1] ele_data_arr, int [::1] edge_idx):
    
    cdef int i, j, k, ind
    
    cdef FILE* cfile
    cdef bytes py_bytes = filename.encode()
    cdef char* c_filename = py_bytes
    cfile = fopen(c_filename, 'rb')
    
    cdef int ele_table, ptr, nnode_elem
    cdef float [1000] ele_data
    cdef int c = 0
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
    
    
def LoadStressDouble(filename, int table_index, int [::1] ele_ind_table, 
                   int [::1] nodstr,int [::1] etype, int nitem, 
                   double [:, ::1] ele_data_arr, int [::1] edge_idx):
    
    cdef int i, j, k, ind
    
    cdef FILE* cfile
    cdef bytes py_bytes = filename.encode()
    cdef char* c_filename = py_bytes
    cfile = fopen(c_filename, 'rb')
    
    cdef int ele_table, ptr, nnode_elem
    cdef double [1000] ele_data
    cdef int c = 0
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
    
def ReadArray(filename, int ptr, int nterm, int neqn, int [::1] index_arr):
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
        
    index_arr : numpy int array
        Indexing array
        
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
              int [::1] index_arr)
    
    """

    cdef int i, j, k, ind
    
    cdef bytes buf
    with open(filename, "rb") as f:
        f.seek(ptr*4)
        buf = f.read((neqn*6 + nterm*3)*4)

    cdef char * p = buf # python to c character array pointer
    cdef int loc = 0 # location long buffer
    
    # Half of the data
    cdef int ntermadj = nterm - neqn # upper triangle (sorta)
    cdef int [::1] krow = np.empty(ntermadj, np.int32)
    cdef int [::1] kcol = np.empty(ntermadj, np.int32)
    cdef double [::1] kdata = np.empty(ntermadj)

    
    cdef int [::1] kdiag = np.empty(neqn, np.int32)
    cdef double [::1] kdata_diag = np.empty(neqn)
    
    cdef int c = 0 # index counter
    cdef int d = 0 # data counter
    cdef int row, col, nitems, intval
    cdef double val
    for i in range(neqn):
        col = index_arr[i]
        
        # number of items to read
        nitems = GetInt(&p[loc]); loc += 4
        loc += 4
        
        # Indices: read in all but diagional term
        for j in range(nitems - 1):
            # get row number
            row = GetInt(&p[loc]) - 1; loc += 4 # convert to c indexing
            
            # store upper triangle
            if index_arr[row] > col:
                krow[c] = index_arr[row]
                kcol[c] = col
            else:
                krow[c] = col
                kcol[c] = index_arr[row]
                
            c += 1
            
        # store diagional term
        row = GetInt(&p[loc]) - 1; loc += 4
        kdiag[i] = index_arr[row]
        loc += 12
        
        # Data: read in all but diagional term
        for j in range(nitems - 1):
            # Store data
            kdata[d] = GetDouble(&p[loc]); loc += 8
            d += 1
            
        # store diagional data term
        kdata_diag[i] = GetDouble(&p[loc]); loc += 8
        
        # seek past end of data
        loc += 4
                    
    return np.asarray(krow), np.asarray(kcol), np.asarray(kdata), \
           np.asarray(kdiag), np.asarray(kdata_diag)
       
    
# consider adding a sorting flag to disable sorting
def FullNodeInfo(filename, int ptrDOF, int nNodes, int neqn):
    """
    
    Reads in full file details required for the assembly of the mass and 
    stiffness matrices.
    
    The reference arrays are sorted by default, though this increases the
    bandwidth of the mass and stiffness matrices.
    
    Parameters
    ----------
    filename : string
        Full file filename
    
    ptrDOF : int
        Location of the DOF block in the full file
        
    nNodes :
        Number of nodes in full file

    neqn : 
        Number of equations in full file
        
    
    Returns
    -------
    nref : numpy np.int32 array
        Sorted nodal reference array
        
    dref: numpy np.int32 array
        Sorted degree of freedom reference array.
        
    index_arr : numpy np.int32 array
        Index array to sort rows and columns.
        
    const : numpy np.int32 array
        Negative if a node's DOF is constrained
        
    ndof : numpy np.int32 array
        Number of degrees of freedom for each node in nref
    """

    cdef int i, j, ind
    cdef int [::1] neqv = np.empty(nNodes, np.int32)
    cdef int [::1] ndof = np.empty(nNodes, np.int32)
    cdef int [::1] const = np.empty(neqn, np.int32)
        
    with open(filename, "rb") as f:

        # nodal equivalency
        f.seek((212 + 2)*4)
        neqv = np.fromfile(f, 'i', nNodes)
        
        # Total DOFs
        f.seek((ptrDOF + 2)*4)
        ndof = np.fromfile(f, 'i', nNodes)
        
        # Constrained DOFs
        f.seek((ptrDOF + 5 + nNodes)*4)
        const = np.fromfile(f, 'i', neqn)
    
    # create sorting array
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
    # create an index array.  this tells the array readers down the line where
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
    cdef int [::1] nref_sort = np.empty(neqn, np.int32)
    cdef int [::1] dref_sort = np.empty(neqn, np.int32)
    cdef int [::1] const_sort = np.empty(neqn, np.int32)
    for i in range(neqn):
        nref_sort[i] = nref[s_neqv_dof[i]]
        dref_sort[i] = dref[s_neqv_dof[i]]
        const_sort[i] = const[s_neqv_dof[i]]
        
    return np.asarray(nref_sort), np.asarray(dref_sort), np.asarray(index_arr), \
           np.asarray(const_sort), np.asarray(ndof)