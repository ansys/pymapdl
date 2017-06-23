import numpy as np
cimport numpy as np

# Definitions from c header
cdef extern from "parsefull.h":
    int return_fheader(char*, int*)
    
    void read_full(int*, int*, int*, int*, int*, double*, int*, int*, double*,
                   int*, char*, int*, int);


def ReturnHeader(filename):
    """ Just reads in the header """
    # Convert python string to char array
    cdef bytes py_bytes = filename.encode()
    cdef char* c_filename = py_bytes
    
    # Read header
    cdef int [::1] fheader = np.empty(101, np.int32)
    return_fheader(c_filename, &fheader[0])
    
    return np.asarray(fheader)
    
    
def Load_KM(filename, is_sorted):
    """
    Reads an ANSYS full file and returns indices to construct symmetric, real, 
    and sparse mass and stiffness matrices
    """
    # convert to int
    cdef int sort = is_sorted
    
    # Convert python string to char array
    cdef bytes py_bytes = filename.encode()
    cdef char* c_filename = py_bytes
    
    # Read header
    cdef int [::1] fheader = np.empty(101, np.int32)
    cdef int rst = return_fheader(c_filename, &fheader[0])

    cdef int neqn = fheader[2];    # Number of equations
    cdef int ntermK = fheader[9];  # number of terms in stiffness matrix
    cdef int nNodes = fheader[33]; # Number of nodes considered by assembly
    cdef int ntermM = fheader[34]; # number of terms in mass matrix

    #### Sanity check ####
    #// Check if lumped (item 11)
    if fheader[11]:
        raise Exception('Unable to read a lumped mass matrix.  Terminating')

    # Check if arrays are unsymmetric (item 14)
    if fheader[14]:
        raise Exception ('Unable to read an unsymmetric mass/stiffness matrix. Terminating')

    # Create numpy memory views so they can be garbage collected later
    cdef int[::1] numdat = np.empty(3, np.int32)
    # tracks array sizes (nfree, kentry, mentry)

    # node and dof reference arrays
    cdef int[::1] sidx = np.empty(nNodes*3, np.int32) # sorting index
    cdef int[::1] nref = np.empty(nNodes*3, np.int32)
    cdef int[::1] dref = np.empty(nNodes*3, np.int32)

    # size mass and stiffness arrays
    cdef int karrsz = 2*ntermK - neqn
    cdef int [::1] krows = np.empty(karrsz, np.int32)
    cdef int [::1] kcols = np.empty(karrsz, np.int32)
    cdef double [::1] kdata = np.empty(karrsz, np.double)

    cdef int marrsz = 2*ntermM - neqn
    cdef int [::1] mrows = np.empty(marrsz, np.int32)
    cdef int [::1] mcols = np.empty(marrsz, np.int32)
    cdef double [::1] mdata = np.empty(marrsz, np.double)

    # Populate these arrays
    cdef int nfull
    read_full(&numdat[0], &nref[0], &dref[0], &krows[0], &kcols[0], &kdata[0],
              &mrows[0], &mcols[0], &mdata[0], &fheader[0], c_filename,
              &sidx[0], sort)

    # Grab array sizes
    nfree = numdat[0]
    kentry = numdat[1]
    mentry = numdat[2]
    
    # Resort degree of freedom references if sorted
    cdef int i, sind
    cdef int[::1] nref_sort = np.empty(nfree, np.int32)
    cdef int[::1] dref_sort = np.empty(nfree, np.int32)
    if sort:
        for i in range(nfree):
            sind = sidx[i]
            nref_sort[i] = nref[sind]
            dref_sort[i] = dref[sind]

        # Return sorted arrays to python
        return (np.asarray(nref_sort),
                np.asarray(dref_sort),
                np.asarray(krows)[:kentry], 
                np.asarray(kcols)[:kentry],
                np.asarray(kdata)[:kentry],
                np.asarray(mrows)[:mentry],
                np.asarray(mcols)[:mentry],
                np.asarray(mdata)[:mentry])            
    else:
        # Return unsorted arrays to python
        return (np.asarray(nref)[:nfree],
                np.asarray(dref)[:nfree],
                np.asarray(krows)[:kentry], 
                np.asarray(kcols)[:kentry],
                np.asarray(kdata)[:kentry],
                np.asarray(mrows)[:mentry],
                np.asarray(mcols)[:mentry],
                np.asarray(mdata)[:mentry])




