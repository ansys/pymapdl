# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True

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
                 int [::1] e_disp_table, int [:, ::1] elem, int [::1] etype):
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
    
    
def LoadStress(filename, int table_index, int [::1] ele_ind_table, int [::1] nodstr,
               int [::1] etype, int nitem, 
               float [:, ::1] ele_data_arr, int [::1] edge_idx):
    
    cdef int i, j, k, ind
    
    cdef FILE* cfile
    cdef bytes py_bytes = filename.encode()
    cdef char* c_filename = py_bytes
    cfile = fopen(c_filename, 'r')
    
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
    
    
