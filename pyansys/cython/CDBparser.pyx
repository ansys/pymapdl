""" 
Cython module to parse raw data from an ANSYS cdb file.

"""
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True

import numpy as np
cimport numpy as np

# Numpy must be initialized. When using numpy from C or Cython you must
# _always_ do that, or you will have segfaults
np.import_array()

import ctypes                   
         
# Type defintion for an unsigned 8-bit
ctypedef unsigned char uint8
          
# VTK numbering for vtk cells
cdef uint8 vtkhexnum = 12
cdef uint8 vtkpyrnum = 14
cdef uint8 vtktetnum = 10
cdef uint8 vtkwegnum = 13
                   
# Quadradic elements
cdef int vtkquadtetnum = 24 # VTK_QUADRATIC_TETRA = 24
cdef int vtkquadpyrnum = 27 # VTK_QUADRATIC_PYRAMID = 27
cdef int vtkquadwegnum = 26 # VTK_QUADRATIC_WEDGE = 26
cdef int vtkquadhexnum = 25 # VTK_QUADRATIC_HEXAHEDRON = 25                        
                   
# ANSYS element type definitions
cdef int [4] typeA

# Legacy mixed elements
typeA[0] = 45
typeA[1] = 95

# Current mixed elements
typeA[2] = 185
typeA[3] = 186

# Tetrahedrals (legacy and current)
cdef int [4] typeB
typeB[0] = 92
typeB[1] = 187
                   
#==============================================================================
# Store elements
#==============================================================================
cdef inline void StoreTet_TypeB(long [::1] offset, long *ecount, long *ccount, 
                          long [::1] cells, uint8 [::1] cell_type,
                          long [::1] numref, int [:, ::1] elem, int i, int lin):
    """
    Stores tetrahedral element in vtk arrays.  ANSYS elements are ordered
    the same as vtk elements.
    
    VTK DOCUMENTATION
    The tetrahedron is defined by the four points (0-3); where (0,1,2) is the
    base of the tetrahedron which, using the right hand rule, forms a triangle
    whose normal points in the direction of the fourth point.
    
    For quadradic
    The cell includes a mid-edge node on each of the size edges of the 
    tetrahedron. The ordering of the ten points defining the cell is point ids
    (0-3,4-9) where ids 0-3 are the four tetra vertices; and point ids 4-9 are
    the midedge nodes between
    (0,1), (1,2), (2,0), (0,3), (1,3), and (2,3)

    """
    # Populate offset array
    offset[ecount[0]] = ccount[0]
    
    if lin:
        cells[ccount[0]] = 4; ccount[0] += 1
        
        # Populate cell array while renumbering nodes
        for j in range(4):
            cells[ccount[0]] = numref[elem[i, j]]; ccount[0] += 1
        
        # Populate cell type array
        cell_type[ecount[0]] = vtktetnum
        
    else:
        cells[ccount[0]] = 10; ccount[0] += 1
        
        # Populate cell array while renumbering nodes
        for j in range(10):
            cells[ccount[0]] = numref[elem[i, j]]; ccount[0] += 1
        
        # Populate cell type array
        cell_type[ecount[0]] = vtkquadtetnum
        
    # increment element counter
    ecount[0] += 1
    

cdef inline void StoreTet(long [::1] offset, long *ecount, long *ccount, 
                          long [::1] cells, uint8 [::1] cell_type,
                          long [::1] numref, int [:, ::1] elem, int i, int lin):
    """
    Stores tetrahedral element in vtk arrays.  ANSYS elements are ordered
    the same as vtk elements.
    
    VTK DOCUMENTATION:
    Linear
    The tetrahedron is defined by the four points (0-3); where (0,1,2) is the
    base of the tetrahedron which, using the right hand rule, forms a triangle
    whose normal points in the direction of the fourth point.
 
    Quadradic   
    The cell includes a mid-edge node on each of the size edges of the 
    tetrahedron. The ordering of the ten points defining the cell is point ids
    (0-3,4-9) where ids 0-3 are the four tetra vertices; and point ids 4-9 are
    the midedge nodes between
    (0,1), (1,2), (2,0), (0,3), (1,3), and (2,3)

    """
    # Populate offset array
    offset[ecount[0]] = ccount[0]
    
    # Populate cell type array and 
    if lin:
        cells[ccount[0]] = 4; ccount[0] += 1
        cell_type[ecount[0]] = vtktetnum
        
    else:
        cells[ccount[0]] = 10; ccount[0] += 1
        cell_type[ecount[0]] = vtkquadtetnum
        

    # Populate cell array while renumbering nodes

    # edge nodes
    # [0, 1, 2, 2, 3, 3, 3, 3]
    cells[ccount[0]] = numref[elem[i, 0]]; ccount[0] += 1
    cells[ccount[0]] = numref[elem[i, 1]]; ccount[0] += 1
    cells[ccount[0]] = numref[elem[i, 2]]; ccount[0] += 1
    cells[ccount[0]] = numref[elem[i, 4]]; ccount[0] += 1
        
    # midside nodes
    if not lin:
        cells[ccount[0]] = numref[elem[i,  8]]; ccount[0] += 1
        cells[ccount[0]] = numref[elem[i,  9]]; ccount[0] += 1
        cells[ccount[0]] = numref[elem[i, 11]]; ccount[0] += 1
        cells[ccount[0]] = numref[elem[i, 16]]; ccount[0] += 1
        cells[ccount[0]] = numref[elem[i, 17]]; ccount[0] += 1
        cells[ccount[0]] = numref[elem[i, 18]]; ccount[0] += 1

    # increment element counter
    ecount[0] += 1
        

cdef inline void StorePyr(long [::1] offset, long *ecount, long *ccount, 
                          long [::1] cells, uint8 [::1] cell_type,
                          long [::1] numref, int [:, ::1] elem, int i, int lin):
    """
    Stores pyramid element in vtk arrays.  ANSYS elements are ordered in the
    same manner as VTK.    

    VTK DOCUMENTATION
    Linear Pyramid
    The pyramid is defined by the five points (0-4) where (0,1,2,3) is the base
    of the pyramid which, using the right hand rule, forms a quadrilaterial
    whose normal points in the direction of the pyramid apex at vertex #4.
    
    Quadradic Pyramid
    The ordering of the thirteen points defining the cell is point ids
    (0-4,5-12) where point ids 0-4 are the five corner vertices of the pyramid;
    followed by eight midedge nodes (5-12). Note that these midedge nodes 
    correspond lie on the edges defined by:
    (0,1), (1,2), (2,3), (3,0), (4,5), (5,6), (6,7), (7,4), (0,4), (1,5), (2,6), (3,7)
    """

    # Populate offset and cell type arrays
    offset[ecount[0]] = ccount[0]
    
    # Populate cell array while renumbering nodes
    if lin:
        cells[ccount[0]] = 5; ccount[0] += 1
        cell_type[ecount[0]] = vtkpyrnum
    else:
        cells[ccount[0]] = 13; ccount[0] += 1
        cell_type[ecount[0]] = vtkquadpyrnum
    
    # edge nodes
    # [0, 1, 2, 3, 4, X, X, X]
    for k in range(5):
        cells[ccount[0]] = numref[elem[i, k]]
        ccount[0] += 1
        
    # Populate array
    if not lin:
        for k in range(8, 12):
            cells[ccount[0]] = numref[elem[i, k]]
            ccount[0] += 1
            
        for k in range(16, 20):
            cells[ccount[0]] = numref[elem[i, k]]
            ccount[0] += 1
    
    ecount[0] += 1

        
cdef inline void StoreWeg(long [::1] offset, long *ecount, long *ccount, 
                          long [::1] cells, uint8 [::1] cell_type,
                          long [::1] numref, int [:, ::1] elem, int i, int lin):
    """
    Stores wedge element in vtk arrays.  ANSYS elements are ordered differently
    than vtk elements.  ANSYS orders counter-clockwise and VTK orders clockwise
    
    VTK DOCUMENTATION
    Linear Wedge
    The wedge is defined by the six points (0-5) where (0,1,2) is the base of
    the wedge which, using the right hand rule, forms a triangle whose normal
    points outward (away from the triangular face (3,4,5)).

    Quadradic Wedge
    The ordering of the fifteen points defining the cell is point ids
    (0-5,6-14) where point ids 0-5 are the six corner vertices of the wedge,
    defined analogously to the six points in vtkWedge (points (0,1,2) form the
    base of the wedge which, using the right hand rule, forms a triangle whose
    normal points away from the triangular face (3,4,5)); followed by nine
    midedge nodes (6-14). Note that these midedge nodes correspond lie on the
    edges defined by :
    (0,1), (1,2), (2,0), (3,4), (4,5), (5,3), (0,3), (1,4), (2,5)
    """

    # Populate offset and cell type arrays
    offset[ecount[0]] = ccount[0]
    
    if lin:
        cells[ccount[0]] = 6; ccount[0] += 1
        cell_type[ecount[0]] = vtkwegnum

    else:
        cells[ccount[0]] = 15; ccount[0] += 1
        cell_type[ecount[0]] = vtkquadwegnum

    # Populate cell array while renumbering nodes
    # [0, 1, 2, 2, 3, 4, 5, 5]
    cells[ccount[0]] = numref[elem[i, 2]]; ccount[0] += 1
    cells[ccount[0]] = numref[elem[i, 1]]; ccount[0] += 1
    cells[ccount[0]] = numref[elem[i, 0]]; ccount[0] += 1
    cells[ccount[0]] = numref[elem[i, 6]]; ccount[0] += 1
    cells[ccount[0]] = numref[elem[i, 5]]; ccount[0] += 1
    cells[ccount[0]] = numref[elem[i, 4]]; ccount[0] += 1

    if not lin:
        # midside nodes
        cells[ccount[0]] = numref[elem[i,  9]]; ccount[0] += 1
        cells[ccount[0]] = numref[elem[i,  8]]; ccount[0] += 1
        cells[ccount[0]] = numref[elem[i, 11]]; ccount[0] += 1
        cells[ccount[0]] = numref[elem[i, 13]]; ccount[0] += 1
        cells[ccount[0]] = numref[elem[i, 12]]; ccount[0] += 1
        cells[ccount[0]] = numref[elem[i, 15]]; ccount[0] += 1
        cells[ccount[0]] = numref[elem[i, 18]]; ccount[0] += 1
        cells[ccount[0]] = numref[elem[i, 17]]; ccount[0] += 1
        cells[ccount[0]] = numref[elem[i, 16]]; ccount[0] += 1

    ecount[0] += 1
    



cdef inline void StoreHex(long [::1] offset, long *ecount, long *ccount, 
                          long [::1] cells, uint8 [::1] cell_type,
                          long [::1] numref, int [:, ::1] elem, int i, int lin):
    """
    Stores hexahedral element in vtk arrays.  ANSYS elements are ordered in the
    same manner as VTK.    
    
    VTK DOCUMENTATION
    Linear Hexahedral
    The hexahedron is defined by the eight points (0-7) where (0,1,2,3) is the
    base of the hexahedron which, using the right hand rule, forms a
    quadrilaterial whose normal points in the direction of the opposite face
    (4,5,6,7).

    Quadradic Hexahedral
    The ordering of the twenty points defining the cell is point ids
    (0-7, 8-19) where point ids 0-7 are the eight corner vertices of the cube;
    followed by twelve midedge nodes (8-19)
    Note that these midedge nodes correspond lie on the edges defined by:
    Midside   Edge nodes
    8         (0, 1)
    9         (1, 2)
    10        (2, 3)
    11        (3, 0)
    12        (4, 5)
    13        (5, 6)
    14        (6, 7)
    15        (7, 4)
    16        (0, 4)
    17        (1, 5)
    18        (2, 6)
    19        (3, 7)

    """

    # Populate offset, cell type, and cell arrays while renumbering nodes
    offset[ecount[0]] = ccount[0]
    if lin:
        cells[ccount[0]] = 8; ccount[0] += 1
        cell_type[ecount[0]] = vtkhexnum

        for k in range(8):
            cells[ccount[0]] = numref[elem[i, k]]
            ccount[0] += 1

    else:
        cells[ccount[0]] = 20; ccount[0] += 1
        cell_type[ecount[0]] = vtkquadhexnum
        
        for k in range(20):
            cells[ccount[0]] = numref[elem[i, k]]
            ccount[0] += 1

    ecount[0] += 1
        
        
#==============================================================================
# Parse raw data
#==============================================================================
def Parse(raw, pyforce_linear):
    """
    Parses raw cdb data from downstream conversion to a vtk unstructured grid
    """
    cdef int force_linear = pyforce_linear    
    
    cdef long [:, ::1] ekey = raw['ekey']
    cdef int [:, ::1] elem = raw['elem']
    cdef int [::1] etype = raw['etype']
    cdef int [::1] nnum = raw['nnum']
    
    cdef int i, j, k, lin
    cdef int nelem = elem.shape[0]
    cdef int nnode = nnum.shape[0]

    # Find the max element type number
    cdef int nekey = ekey.shape[0]
    maxelemtype = 0
    for i in range(nekey):
        if ekey[i, 0] > maxelemtype:
            maxelemtype = ekey[i, 0]
    
    # Create an element type array for indexing
    cdef int [::1] elem_type = np.empty(maxelemtype + 1, ctypes.c_int)
    for i in range(nekey):
        elem_type[ekey[i, 0]] = ekey[i, 1]
    
    # Allocate memory for cell data
    cdef long [::1] offset = np.empty(nelem, ctypes.c_long)
    cdef uint8 [::1] cell_type = np.empty(nelem, dtype='uint8')
    
    # different array sizes depending on midside nodes
    cdef long [::1] cells = np.empty(nelem*21, ctypes.c_long)  # max cell is 20 and header is 1
    
    # Find the highest node number
    cdef int maxnodenum = 0
    for i in range(nnode):
        if nnum[i] > maxnodenum:
            maxnodenum = nnum[i]
            
    # Create reference array for node renumbering
    cdef long n
    cdef long [::1] numref = np.empty(maxnodenum + 2, ctypes.c_long)
#    numref[0]  = -1 # elements that have missing nodes written as a "0" in cdb
#
#    # elements that have missing nodes, but were written such that those
#    # missing nodes were at the end of the line and were simply not written
#    # will be stored as a -1
#    numref[-1] = -1

    # forcing all to -1 to avoid null references
    numref[:] = -1
          

    for n in range(nnode):
        numref[nnum[n]] = n
    
    # Loop through each element and check if the element type matches one this code
    # can read
    cdef long ccount = 0 # cell/offset counter
    cdef long ecount = 0 # element number counter
    for i in range(nelem):
        for j in range(4):
            if elem_type[etype[i]] == typeA[j]:
                # Set to read quadradic nodes
                if force_linear:
                    lin = 1
                else:
                    # Check if linear (missing midside nodes)
                    lin = elem[i, 8] == -1
                    
                ############ Read element typeA ############
                # Determine element type through logic
                if elem[i, 6] != elem[i, 7]: # check if hexahedral
                    StoreHex(offset, &ecount, &ccount, cells, cell_type, numref,
                             elem, i, lin)

                elif elem[i, 5] != elem[i, 6]: # check if wedge
                    StoreWeg(offset, &ecount, &ccount, cells, cell_type, numref,
                             elem, i, lin)
                    
                elif elem[i, 2] != elem[i, 3]: # check if pyramid
                    StorePyr(offset, &ecount, &ccount, cells, cell_type, numref,
                             elem, i, lin)
                    
                else: # if tetrahedral
                    StoreTet(offset, &ecount, &ccount, cells, cell_type, numref,
                             elem, i, lin)

                break # Continue to next element
                
        # Test for element type B
        for j in range(2):
            if elem_type[etype[i]] == typeB[j]:
                if force_linear:
                    lin = 1
                elif elem[i, 8] != -1:
                    lin = 0
                    
                StoreTet_TypeB(offset, &ecount, &ccount, cells, cell_type, 
                               numref, elem, i, lin)
                               
                break # Continue to next element
                    
                    
    # Return spliced arrays
    return np.asarray(cells[:ccount]), np.asarray(offset[:ecount]), \
           np.asarray(cell_type[:ecount]), np.asarray(numref)
    
    
#==============================================================================
# For FEM    
#==============================================================================
## Define cell edges ##
cdef int [6][2] tetedges
tetedges[0][0] = 0
tetedges[0][1] = 1

tetedges[1][0] = 1
tetedges[1][1] = 2

tetedges[2][0] = 0
tetedges[2][1] = 2

tetedges[3][0] = 0
tetedges[3][1] = 3

tetedges[4][0] = 1
tetedges[4][1] = 3

tetedges[5][0] = 2
tetedges[5][1] = 3


cdef int [8][2] pyredges
pyredges[0][0] = 0
pyredges[0][1] = 1

pyredges[1][0] = 1
pyredges[1][1] = 2

pyredges[2][0] = 2
pyredges[2][1] = 3

pyredges[3][0] = 0
pyredges[3][1] = 3

pyredges[4][0] = 0
pyredges[4][1] = 4

pyredges[5][0] = 1
pyredges[5][1] = 4

pyredges[6][0] = 2
pyredges[6][1] = 4

pyredges[7][0] = 3
pyredges[7][1] = 4


cdef int wegedges[9][2]
wegedges[0][0] = 0
wegedges[0][1] = 1

wegedges[1][0] = 1
wegedges[1][1] = 2

wegedges[2][0] = 2
wegedges[2][1] = 0

wegedges[3][0] = 0
wegedges[3][1] = 3

wegedges[4][0] = 1
wegedges[4][1] = 4

wegedges[5][0] = 2
wegedges[5][1] = 5

wegedges[6][0] = 3
wegedges[6][1] = 4

wegedges[7][0] = 4
wegedges[7][1] = 5

wegedges[8][0] = 3
wegedges[8][1] = 5


cdef int hexedges[12][2]
hexedges[0][0] = 0
hexedges[0][1] = 1

hexedges[1][0] = 1
hexedges[1][1] = 2

hexedges[2][0] = 2
hexedges[2][1] = 3

hexedges[3][0] = 0
hexedges[3][1] = 3

hexedges[4][0] = 0
hexedges[4][1] = 4

hexedges[5][0] = 1
hexedges[5][1] = 5

hexedges[6][0] = 2
hexedges[6][1] = 6

hexedges[7][0] = 3
hexedges[7][1] = 7

hexedges[8][0] = 4
hexedges[8][1] = 5

hexedges[9][0] = 5
hexedges[9][1] = 6

hexedges[10][0] = 6
hexedges[10][1] = 7

hexedges[11][0] = 4
hexedges[11][1] = 7

    
# ANSYS cell numbering for TypeA elements

# Wedge element
# ANSYS defines a wege as [0, 1, 2, 2, 3, 4, 5, 5]
# but VTK needs [2, 1, 0, 6, 5, 4] due to the ordering of the faces
cdef int [6] wegnum
wegnum[0] = 2
wegnum[1] = 1
wegnum[2] = 0
wegnum[3] = 6
wegnum[4] = 5
wegnum[5] = 4


# Tetrahedral element
cdef int [4] tetnum
tetnum[0] = 0
tetnum[1] = 1
tetnum[2] = 2
tetnum[3] = 4


# Midside node indices for a type A element
cdef int [12][2] typeAmidind
typeAmidind [0][0] = 0
typeAmidind [0][1] = 1

typeAmidind [1][0] = 1
typeAmidind [1][1] = 2

typeAmidind [2][0] = 2
typeAmidind [2][1] = 3

typeAmidind [3][0] = 0
typeAmidind [3][1] = 3

typeAmidind [4][0] = 4
typeAmidind [4][1] = 5

typeAmidind [5][0] = 5
typeAmidind [5][1] = 6

typeAmidind [6][0] = 6
typeAmidind [6][1] = 7

typeAmidind [7][0] = 4
typeAmidind [7][1] = 7

typeAmidind [8][0] = 0
typeAmidind [8][1] = 4

typeAmidind [9][0] = 1
typeAmidind [9][1] = 5

typeAmidind [10][0] = 2
typeAmidind [10][1] = 6

typeAmidind [11][0] = 3
typeAmidind [11][1] = 7

# typeA midside node indices are shifted by 8
cdef int [9] wegmid
wegmid[0] = 0
wegmid[1] = 1
wegmid[2] = 3
wegmid[3] = 4
wegmid[4] = 5
wegmid[5] = 7
wegmid[6] = 8
wegmid[7] = 9
wegmid[8] = 10


cdef int [8] pyrmid
pyrmid[0] = 0
pyrmid[1] = 1
pyrmid[2] = 2
pyrmid[3] = 3
pyrmid[4] = 8
pyrmid[5] = 9
pyrmid[6] = 10
pyrmid[7] = 11

cdef int [6] tetmid
tetmid[0] = 0
tetmid[1] = 1
tetmid[2] = 3
tetmid[3] = 8
tetmid[4] = 9
tetmid[5] = 10


cdef int [6][2] typeBmidind
typeBmidind[0][0] = 0
typeBmidind[0][1] = 1

typeBmidind[1][0] = 1
typeBmidind[1][1] = 2

typeBmidind[2][0] = 0
typeBmidind[2][1] = 2

typeBmidind[3][0] = 0
typeBmidind[3][1] = 3

typeBmidind[4][0] = 1
typeBmidind[4][1] = 3

typeBmidind[5][0] = 2
typeBmidind[5][1] = 3

cdef int [6] tetmidB
tetmidB[0] = 4
tetmidB[1] = 5
tetmidB[2] = 6
tetmidB[3] = 7
tetmidB[4] = 8
tetmidB[5] = 9


def ParseForFEM(raw):
    """
    Alternative approach for parsing the raw data from a cdb
    
    Colapses node numbering to 0 for downstream use and generates several other
    arrays to be used for FEA.
    """
    
    # Pull data from 
    cdef long [:, ::1] ekey = raw['ekey']
    cdef int [:, ::1] elem = raw['elem']
    cdef int [::1] etype = raw['etype']
    cdef int [::1] nnum = raw['nnum']
    
    cdef int i, j, k
    cdef int nelem = elem.shape[0]
    cdef int nnode = nnum.shape[0]

    # Find the max element type number
    cdef int nekey = ekey.shape[0]
    maxelemtype = 0
    for i in range(nekey):
        if ekey[i, 0] > maxelemtype:
            maxelemtype = ekey[i, 0]
    
    # Create an element type array for indexing
    cdef int [::1] elem_type = np.empty(maxelemtype + 1, ctypes.c_int)
    for i in range(nekey):
        elem_type[ekey[i, 0]] = ekey[i, 1]
    
    # Allocate memory for cell data
    cdef long [::1] offset = np.empty(nelem, ctypes.c_long)
    cdef uint8 [::1] cell_type = np.empty(nelem, dtype='uint8')
    
    # different array sizes depending on midside nodes
    cdef long [::1] cells = np.empty(nelem*9, ctypes.c_long)  # max cell is 8 and header is 1
    
    # Find the highest node number
    cdef int maxnodenum = 0
    for i in range(nnode):
        if nnum[i] > maxnodenum:
            maxnodenum = nnum[i]
    
    # Create reference array for node renumbering
    cdef uint8 [::1] nodeused = np.zeros(maxnodenum + 1, dtype='uint8')

    # Loop through to see which nodes will be used
    for i in range(nelem):
        for j in range(4):
            if elem_type[etype[i]] == typeA[j]:
                ############ Read element typeA ############
                # Determine element type through logic
                if elem[i, 6] != elem[i, 7]: # check if hexahedral
                    for k in range(8): # Indicate that these nodes are used
                        nodeused[elem[i, k]] = 1
                    
                elif elem[i, 5] != elem[i, 6]: # check if wedge
                    for k in range(6): # Indicate that these nodes are used
                        nodeused[elem[i, wegnum[k]]] = 1
                    
                elif elem[i, 2] != elem[i, 3]: # check if pyramid
                    for k in range(5): # Indicate that these nodes are used
                        nodeused[elem[i, k]] = 1
                    
                else: # if tetrahedral
                    for k in range(4): # Indicate that these nodes are used
                        nodeused[elem[i, wegnum[k]]] = 1
                
                break # Continue to next element
                
        # Test for element type B
        for j in range(2):
            if elem_type[etype[i]] == typeB[j]:
                for k in range(4): # Indicate that these nodes are used
                    nodeused[elem[i, k]] = 1
                break
                    
    # sum nodes used
    cdef int c = 0
    for i in range(maxnodenum + 1):
        if nodeused[i]:
            c += 1

    # Track original node numbering        
    cdef long [::1] orignum = np.empty(nnode, ctypes.c_long)
    c = 0
    for i in range(maxnodenum + 1):
        if nodeused[i]:
            orignum[c] = i
            c += 1
        
    # Node reference array relating original node numbering to new node
    # numbering
    cdef long [::1] numref = np.empty(maxnodenum + 1, ctypes.c_long)
    c = 0 # reset counter (this becomes the number of valid nodes)
    for i in range(maxnodenum + 1):
        if nodeused[i]:
            numref[i] = c
            c += 1 # increment counter for next node
        else:
            numref[i] = -1

    # Create edges and square cell type array
    cdef long [:, ::1] edges = np.empty((nelem*12, 2), ctypes.c_long)
    cdef int [:, ::1] cellarr = np.zeros((nelem, 8), ctypes.c_int)
    cdef int [::1] ncellpts = np.empty(nelem, ctypes.c_int)
    
    # Track if elements are used
    cdef uint8 [::1] elemused = np.zeros(nelem, dtype='uint8')
    
    # Also, track the indices of the midside nodes based on their adjcent edge
    # nodes in the new indexing
    cdef long [:, ::1] midedgeind = np.empty((nnode, 2), ctypes.c_long) # sized for maximum number of nodes, will trim later
    
    # Also track the original midside node indices
    cdef long [::1] midind = np.empty(nnode, ctypes.c_long) # sized for maximum number of nodes, will trim later
    cdef int midnode = 0
    
    # Array to track if a midside node has been stored
    cdef int [::1] midstored = np.zeros(maxnodenum + 1, ctypes.c_int)
    
    # Loop through each element and check if the element type matches one this code
    # can read
    ccount = 0 # cell/offset counter
    ecount = 0 # element number counter
    edgenum = 0
    for i in range(nelem):
        ############ Check if element type A ############
        for j in range(4):
            if elem_type[etype[i]] == typeA[j]:
                # Determine element type through logic
                if elem[i, 6] != elem[i, 7]: # check if hexahedral
                    # Populate offset array
                    offset[ecount] = ccount
                
                    # Populate cell arrays with renumbered nodes
                    cells[ccount] = 8; ccount += 1
                    for k in range(8):
                        cells[ccount] = numref[elem[i, k]]
                        cellarr[ecount, k] = numref[elem[i, k]]
                        ccount += 1
                        
                    # Populate edges
                    for k in range(12):
                        edges[edgenum, 0] = cellarr[ecount, hexedges[k][0]]
                        edges[edgenum, 1] = cellarr[ecount, hexedges[k][1]]
                        edgenum += 1
                        
                    # Poulate midside nodes
                    for k in range(12):
                        # if it exists and has not been stored
                        if elem[i, k + 8] > 0 and not midstored[elem[i, k + 8]]:
                            # Add its adjcent nodes to the index array tracker
                            midedgeind[midnode, 0] = numref[elem[i, typeAmidind[k][0]]]
                            midedgeind[midnode, 1] = numref[elem[i, typeAmidind[k][1]]]
                            midind[midnode] = elem[i, k + 8]
                            
                            # Track as stored and increment
                            midstored[elem[i, k + 8]] = 1 
                            midnode += 1
                        
                    # Populate cell type array and number of cell points
                    cell_type[ecount] = vtkhexnum
                    ncellpts[ecount] = 8
                    
                    
                elif elem[i, 5] != elem[i, 6]: # check if wedge
                #    Wedge: (0-5 are edge, 6-14 are midside)
                #    [0, 1, 2, 2, 3, 4, 5, 5][6, 7, -, 8, 9, 10, -, 11, 12, 13, 14, -]
                #                            [8, 9, -,11,12, 13, -, 15, 16, 17, 18, -]
                    # Populate offset array
                    offset[ecount] = ccount  
                    
                    # Populate cell arrays with renumbered nodes
                    cells[ccount] = 6; ccount += 1
                    for k in range(6):
                        cells[ccount] = numref[elem[i, wegnum[k]]]
                        cellarr[ecount, k] = numref[elem[i, wegnum[k]]]
                        ccount += 1
                        
                    # Populate edges
                    for k in range(9):
                        edges[edgenum, 0] = cellarr[ecount, wegedges[k][0]]
                        edges[edgenum, 1] = cellarr[ecount, wegedges[k][1]]
                        edgenum += 1
                        
                    # Poulate midside nodes
                    for k in range(9):
                        # if it exists
                        if elem[i, wegmid[k] + 8] > 0 and not midstored[elem[i, wegmid[k] + 8]]:
                            # Add its adjcent nodes to the index array tracker
                            midedgeind[midnode, 0] = numref[elem[i, typeAmidind[wegmid[k]][0]]]
                            midedgeind[midnode, 1] = numref[elem[i, typeAmidind[wegmid[k]][1]]]
                            midind[midnode] = elem[i, wegmid[k] + 8]
                            
                            # Track as stored and increment
                            midstored[elem[i, wegmid[k] + 8]] = 1
                            midnode += 1                        
                        
                    # Populate cell type array and number of cell points
                    cell_type[ecount] = vtkwegnum
                    ncellpts[ecount] = 6

                    
                elif elem[i, 2] != elem[i, 3]: # check if pyramid
                    # Pyramid (0-4 are edge, 4-12 are midside)
                    # [0, 1, 2, 3, 4, 4, 4, 4][5, 6, 7, 8, -, -, -, -, 9, 10, 11, 12]
                    #                         [8, 9,10,11, -, -, -, -,16, 17, 18, 19]
                    
                    # Populate offset array
                    offset[ecount] = ccount  
                    
                    # Populate cell array while renumbering nodes
                    cells[ccount] = 5; ccount += 1
                    for k in range(5):
                        cells[ccount] = numref[elem[i, k]]
                        cellarr[ecount, k] = numref[elem[i, k]]
                        ccount += 1
                        
                    # Populate edges
                    for k in range(8):
                        edges[edgenum, 0] = cellarr[ecount, pyredges[k][0]]
                        edges[edgenum, 1] = cellarr[ecount, pyredges[k][1]]
                        edgenum += 1                        
                        
                    # Poulate midside nodes
                    for k in range(8):
                        # if it exists
                        if elem[i, pyrmid[k] + 8] > 0 and not midstored[elem[i, pyrmid[k] + 8]]:
                            # Add its adjcent nodes to the index array tracker
                            midedgeind[midnode, 0] = numref[elem[i, typeAmidind[pyrmid[k]][0]]]
                            midedgeind[midnode, 1] = numref[elem[i, typeAmidind[pyrmid[k]][1]]]
                            midind[midnode] = elem[i, pyrmid[k] + 8]
                            
                            # Track as stored and increment
                            midstored[elem[i, pyrmid[k] + 8]] = 1
                            midnode += 1                             
                        
                    # Populate cell type array and number of cell points
                    cell_type[ecount] = vtkpyrnum
                    ncellpts[ecount] = 5
                    
                    
                else: # if tetrahedral
                    # Tetrahedral (0-3 are edge, 4-9 are midside)
                    # [0, 1, 2, 2, 3, 3, 3, 3][4, 5, -, 6, -, -, -, -, 7, 8, 9, -]
                    #                         [8, 9, -,11, -, -, -, -,16,17,18, -]
                    
                    # Populate offset array
                    offset[ecount] = ccount
                    
                    # Populate cell arrcdef long ay while renumbering nodes
                    cells[ccount] = 4; ccount += 1
                    for k in range(4):
                        cells[ccount] = numref[elem[i, tetnum[k]]]
                        cellarr[ecount, k] = numref[elem[i, tetnum[k]]]
                        ccount += 1
                        
                    # Populate edges
                    for k in range(6):
                        edges[edgenum, 0] = cellarr[ecount, tetedges[k][0]]
                        edges[edgenum, 1] = cellarr[ecount, tetedges[k][1]]
                        edgenum += 1                        
                        
                    # Poulate midside nodes
                    for k in range(6):
                        # if it exists
                        if elem[i, tetmid[k] + 8] > 0 and not midstored[elem[i, tetmid[k] + 8]]:
                            # Add its adjcent nodes to the index array tracker
                            midedgeind[midnode, 0] = numref[elem[i, typeAmidind[tetmid[k]][0]]]
                            midedgeind[midnode, 1] = numref[elem[i, typeAmidind[tetmid[k]][1]]]
                            midind[midnode] = elem[i, tetmid[k] + 8]
                            
                            # track as stored and increment
                            midstored[elem[i, tetmid[k] + 8]] = 1
                            midnode += 1
                                                
                    # Populate cell type array and number of cell points
                    cell_type[ecount] = vtktetnum
                    ncellpts[ecount] = 4
                    
                # Increment element counter and track that it is used
                ecount += 1   
                elemused[i] = 1
                
                break # Continue to next element
                
        # Test for element type B
        for j in range(2):
            if elem_type[etype[i]] == typeB[j]:
                ############ Read element typeB ############
                # Tetrahedral (with 0-3 edge and 4 - 9 midside)
                # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
                # Populate offset array
                offset[ecount] = ccount  
    
                # Populate cell array while renumbering nodes
                cells[ccount] = 4; ccount += 1
                for k in range(4):
                    cells[ccount] = numref[elem[i, k]]
                    cellarr[ecount, k] = numref[elem[i, k]]
                    ccount += 1
                
                # Populate edges
                for k in range(6):
                    edges[edgenum, 0] = cellarr[ecount, tetedges[k][0]]
                    edges[edgenum, 1] = cellarr[ecount, tetedges[k][1]]
                    edgenum += 1                            
                
                # Poulate midside nodes
                for k in range(6):
                    # if it exists
                    if elem[i, tetmidB[k]] > 0 and not midstored[elem[i, tetmidB[k]]]:
                        
                        # Add its adjcent nodes to the index array tracker
                        midedgeind[midnode, 0] = numref[elem[i, typeBmidind[k][0]]]
                        midedgeind[midnode, 1] = numref[elem[i, typeBmidind[k][1]]]
                        midind[midnode] = elem[i, tetmidB[k]]

                        # track as stored and increment
                        midstored[elem[i, tetmidB[k]]] = 1
                        midnode += 1

                # Populate cell type array and number of cell points
                cell_type[ecount] = vtktetnum
                ncellpts[ecount] = 4
                
                # Increment element counter and track that it is used
                ecount += 1   
                elemused[i] = 1                    
                break # proceed to next element                     
                
                    
    # Regenerate node list
    cdef double [:, ::1] oldnodes = raw['nodes'] # c is the number of valid edge nodes
    cdef double [:, ::1] nodes = np.empty((c, 6 )) # c is the number of valid edge nodes
    cdef long [::1] nodenum = np.zeros(c, dtype=ctypes.c_long) # track if nodes are used

    cdef int n = 0 # index for old node numbering system
    for i in range(c):
        # Increment until matched
        while nnum[n] != orignum[i]:
            n += 1
        
        # Copy this node and mark as used
        for j in range(6):
            nodes[i, j] = oldnodes[n, j]
        nodenum[i] = n
                    
                    
    # Regenerate node components
    np_numref = np.asarray(numref)
    node_comps = {}
    for comp in raw['node_comps']:
        t = np_numref[raw['node_comps'][comp]]
        t = t[t != -1]
        if len(t):
            node_comps[comp] = t
    
    # Return spliced arrays
    return {'cells': np.asarray(cells[:ccount]),
            'offset': np.asarray(offset[:ecount]),
            'cell_type': np.asarray(cell_type[:ecount]),
            'edges': np.asarray(edges[:edgenum]),
            'cellarr': np.asarray(cellarr[:ecount]),
            'ncellpts': np.asarray(ncellpts[:ecount]),
            'orignode': np.asarray(orignum)[:c],
            'elemused': np.asarray(elemused),
            'nodenum': np.asarray(nodenum),
            'nodes': np.asarray(nodes),
            'node_comps': node_comps,
            'midnum': np.asarray(midind[:midnode]),
            'midside': np.asarray(midedgeind[:midnode])}
    
