import numpy as np
cimport numpy as np

# Definitions from c header
cdef extern from "parsefull.h":
    int return_fheader(char*, int*)
    
    void read_full(int*, int*, int*, int*, int*, double*, int*, int*, double*,
                   int*, char*);


def ReturnHeader(filename):
    """ Just reads in the header """
    # Convert python string to char array
    cdef bytes py_bytes = filename.encode()
    cdef char* c_filename = py_bytes
    
    # Read header
    cdef int [::1] fheader = np.empty(101, np.int32)
    return_fheader(c_filename, &fheader[0])
    
    return np.asarray(fheader)
    
    
def ReturnFull_KM(filename):
    """
    Reads an ANSYS full file and returns indices to construct symmetric, real, 
    and sparse mass and stiffness matrices
    """
    
    # Convert python string to char array
    cdef bytes py_bytes = filename.encode()
    cdef char* c_filename = py_bytes
    
    # Read header
    cdef int [::1] fheader = np.empty(101, np.int32)
    cdef int rst = return_fheader(c_filename, &fheader[0])

    cdef int neqn = fheader[2];    #  Number of equations
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
    read_full(&numdat[0], &nref[0], &dref[0], &krows[0], &kcols[0], &kdata[0],
              &mrows[0], &mcols[0], &mdata[0], &fheader[0], c_filename)

    # Grab array sizes
    nfree = numdat[0]
    kentry = numdat[1]
    mentry = numdat[2]

    # Return these to python
    return (np.asarray(nref)[:nfree],
           np.asarray(dref)[:nfree],
           np.asarray(krows)[:kentry], 
           np.asarray(kcols)[:kentry],
           np.asarray(kdata)[:kentry],
           np.asarray(mrows)[:mentry],
           np.asarray(mcols)[:mentry],
           np.asarray(mdata)[:mentry])









