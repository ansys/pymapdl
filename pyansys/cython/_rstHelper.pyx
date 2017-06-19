# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True

from libc.stdio cimport fopen, FILE, fclose, fread, fseek
from libc.stdio cimport SEEK_CUR, ftell, SEEK_SET

def LoadNodes(filename, int ptrLOC, int nnod, double [:, ::1] nodes, 
              int [::1] nnum_arr):
    """
    Function signature
    def LoadNodes(filename, int ptrLOC, int nnod, double [:, ::1] nodes, 
       int [::1] nnum_arr):
        
    """
    
    cdef int i
    cdef int j = 0
    
    # open file
    cdef FILE* cfile
    cdef bytes py_bytes = filename.encode()
    cdef char* c_filename = py_bytes
    cfile = fopen(c_filename, 'r')

    # Seek to start of node information
    fseek(cfile, (ptrLOC + 2)*4, SEEK_CUR)

    cdef double val
    for i in range(nnod):
        fread(&val, sizeof(double), 1, cfile)
        nnum_arr[i] = <int>val
        
        fread(&nodes[i, j], sizeof(double), 6, cfile)
        
        # skip next 3 ints
        fseek(cfile, 12, SEEK_CUR)

    fclose(cfile)
    
    
def LoadElements(filename, int ptrEID, int nelm, long [::1] e_disp_table,
                 int [:, ::1] elem, int [::1] etype):
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
    
    cdef int i
    cdef int j = 0
    
    cdef FILE* cfile
    cdef bytes py_bytes = filename.encode()
    cdef char* c_filename = py_bytes
    cfile = fopen(c_filename, 'r')

    cdef int nread
    for i in range(nelm - 1):
        
        # seek to start of element information
        fseek(cfile, (ptrEID + e_disp_table[i] + 3)*4, SEEK_SET)

        # Store element type
        fread(&etype[i], sizeof(int), 1, cfile)
        
        # Seek and store element node numbers
        fseek(cfile, 32, SEEK_CUR)
        
        # number of elements to read is dependent on the distance between
        # element entries
        nread = e_disp_table[i + 1] - e_disp_table[i] - 13
        fread(&elem[i, j], sizeof(int), nread, cfile)
        
        
    #==================
    # last entry
    #==================
    i += 1
    # get number to read from fortran nread entry
    fseek(cfile, (ptrEID + e_disp_table[i])*4, SEEK_SET)
    fread(&nread, sizeof(int), 1, cfile)
    nread -= 10
    
    # Store element type
    fseek(cfile, 8, SEEK_CUR)
    fread(&etype[i], sizeof(int), 1, cfile)
    
    # Seek and store element node numbers
    fseek(cfile, 32, SEEK_CUR)
    fread(&elem[i, j], sizeof(int), nread, cfile)

    fclose(cfile)
    
    
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
