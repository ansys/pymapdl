# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True

import numpy as np
cimport numpy as np
import ctypes               

from libc.stdint cimport int32_t, int64_t
ctypedef unsigned char uint8

# VTK numbering for vtk cells
cdef uint8 VTK_EMPTY_CELL = 0
cdef uint8 VTK_VERTEX = 1
cdef uint8 VTK_LINE = 3
cdef uint8 VTK_TRIANGLE = 5
cdef uint8 VTK_QUAD = 9
cdef uint8 VTK_QUADRATIC_TRIANGLE = 22
cdef uint8 VTK_QUADRATIC_QUAD = 23
cdef uint8 VTK_HEXAHEDRON = 12
cdef uint8 VTK_PYRAMID = 14
cdef uint8 VTK_TETRA = 10
cdef uint8 VTK_WEDGE = 13
cdef uint8 VTK_QUADRATIC_TETRA = 24
cdef uint8 VTK_QUADRATIC_PYRAMID = 27
cdef uint8 VTK_QUADRATIC_WEDGE = 26
cdef uint8 VTK_QUADRATIC_HEXAHEDRON = 25

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


cdef inline void StoreLine(int64_t [::1] offset, int64_t *ecount, int64_t *ccount, 
                           int64_t [::1] cells, uint8 [::1] cell_type,
                           int64_t [::1] numref, int [:, ::1] elem, int i, int lin):
    """
    Stores surface triangle vtk cell.  Element may be quadradic or linear
    """
    # Populate offset array
    offset[ecount[0]] = ccount[0]
    
    if lin:
        cells[ccount[0]] = 2; ccount[0] += 1
        
        # Populate cell array while renumbering nodes
        for j in range(2):
            cells[ccount[0]] = numref[elem[i, j]]; ccount[0] += 1
        
        # Populate cell type array
        cell_type[ecount[0]] = VTK_LINE

    ecount[0] += 1

cdef inline void StoreSurfTri(int64_t [::1] offset, int64_t *ecount, int64_t *ccount, 
                              int64_t [::1] cells, uint8 [::1] cell_type,
                              int64_t [::1] numref, int [:, ::1] elem, int i, int lin):
    """
    Stores surface triangle vtk cell.  Element may be quadradic or linear
    """
    # Populate offset array
    offset[ecount[0]] = ccount[0]
    
    if lin:
        cells[ccount[0]] = 3; ccount[0] += 1
        
        # Populate cell array while renumbering nodes
        for j in range(3):
            cells[ccount[0]] = numref[elem[i, j]]; ccount[0] += 1
        
        # Populate cell type array
        cell_type[ecount[0]] = VTK_TRIANGLE
        
    else:
        cells[ccount[0]] = 6; ccount[0] += 1
        
        # Populate cell array while renumbering nodes
        cells[ccount[0]] = numref[elem[i, 0]]; ccount[0] += 1
        cells[ccount[0]] = numref[elem[i, 1]]; ccount[0] += 1
        cells[ccount[0]] = numref[elem[i, 2]]; ccount[0] += 1
        cells[ccount[0]] = numref[elem[i, 4]]; ccount[0] += 1
        cells[ccount[0]] = numref[elem[i, 5]]; ccount[0] += 1
        cells[ccount[0]] = numref[elem[i, 7]]; ccount[0] += 1
        
        # Populate cell type array
        cell_type[ecount[0]] = VTK_QUADRATIC_TRIANGLE
        
    # increment element counter
    ecount[0] += 1



cdef inline void StoreSurfQuad(int64_t [::1] offset, int64_t *ecount, int64_t *ccount, 
                               int64_t [::1] cells, uint8 [::1] cell_type,
                               int64_t [::1] numref, int [:, ::1] elem, int i, int lin):
    """
    Stores surface quad in vtk cell array.  Element may be quadradic or linear


    """
    # Populate offset array
    offset[ecount[0]] = ccount[0]
    
    if lin:
        cells[ccount[0]] = 4; ccount[0] += 1
        
        # Populate cell array while renumbering nodes
        for j in range(4):
            cells[ccount[0]] = numref[elem[i, j]]; ccount[0] += 1
        
        # Populate cell type array
        cell_type[ecount[0]] = VTK_QUAD
        
    else:
        cells[ccount[0]] = 8; ccount[0] += 1
        
        # Populate cell array while renumbering nodes
        for j in range(8):
            cells[ccount[0]] = numref[elem[i, j]]; ccount[0] += 1
        
        # Populate cell type array
        cell_type[ecount[0]] = VTK_QUADRATIC_QUAD
        
    # increment element counter
    ecount[0] += 1
    

cdef inline void StoreTet_TypeB(int64_t [::1] offset, int64_t *ecount, int64_t *ccount, 
                          int64_t [::1] cells, uint8 [::1] cell_type,
                          int64_t [::1] numref, int [:, ::1] elem, int i, int lin):
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
        cell_type[ecount[0]] = VTK_TETRA
        
    else:
        cells[ccount[0]] = 10; ccount[0] += 1
        
        # Populate cell array while renumbering nodes
        for j in range(10):
            cells[ccount[0]] = numref[elem[i, j]]; ccount[0] += 1
        
        # Populate cell type array
        cell_type[ecount[0]] = VTK_QUADRATIC_TETRA
        
    # increment element counter
    ecount[0] += 1
    

cdef inline void StoreTet(int64_t [::1] offset, int64_t *ecount, int64_t *ccount, 
                          int64_t [::1] cells, uint8 [::1] cell_type,
                          int64_t [::1] numref, int [:, ::1] elem, int i, int lin):
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
        cell_type[ecount[0]] = VTK_TETRA
        
    else:
        cells[ccount[0]] = 10; ccount[0] += 1
        cell_type[ecount[0]] = VTK_QUADRATIC_TETRA
        

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
        

cdef inline void StorePyr(int64_t [::1] offset, int64_t *ecount, int64_t *ccount, 
                          int64_t [::1] cells, uint8 [::1] cell_type,
                          int64_t [::1] numref, int [:, ::1] elem, int i, int lin):
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
        cell_type[ecount[0]] = VTK_PYRAMID
    else:
        cells[ccount[0]] = 13; ccount[0] += 1
        cell_type[ecount[0]] = VTK_QUADRATIC_PYRAMID
    
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

        
cdef inline void StoreWeg(int64_t [::1] offset, int64_t *ecount, int64_t *ccount, 
                          int64_t [::1] cells, uint8 [::1] cell_type,
                          int64_t [::1] numref, int [:, ::1] elem, int i, int lin):
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
        cell_type[ecount[0]] = VTK_WEDGE

    else:
        cells[ccount[0]] = 15; ccount[0] += 1
        cell_type[ecount[0]] = VTK_QUADRATIC_WEDGE

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


cdef inline void StoreHex(int64_t [::1] offset, int64_t *ecount, int64_t *ccount, 
                          int64_t [::1] cells, uint8 [::1] cell_type,
                          int64_t [::1] numref, int [:, ::1] elem, int i, int lin):
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
        cell_type[ecount[0]] = VTK_HEXAHEDRON

        for k in range(8):
            cells[ccount[0]] = numref[elem[i, k]]
            ccount[0] += 1

    else:
        cells[ccount[0]] = 20; ccount[0] += 1
        cell_type[ecount[0]] = VTK_QUADRATIC_HEXAHEDRON
        
        for k in range(20):
            cells[ccount[0]] = numref[elem[i, k]]
            ccount[0] += 1

    ecount[0] += 1


def Parse(raw, pyforce_linear, allowable_types, py_null_unallowed):
    """
    Parses raw cdb data from downstream conversion to a vtk unstructured grid
    """
    cdef int force_linear = pyforce_linear
    cdef int null_unallowed = py_null_unallowed
    cdef int i, j, k, lin

    # ANSYS element type definitions
    cdef int [4] typeA

    # Legacy mixed elements
    if '45' in allowable_types:
        typeA[0] = 45
    else:
        typeA[0] = -1

    if '95' in allowable_types:
        typeA[1] = 95
    else:
        typeA[1] = -1

    # Current mixed elements
    if '185' in allowable_types:
        typeA[2] = 185
    else:
        typeA[2] = -1

    if '186' in allowable_types:
        typeA[3] = 186
    else:
        typeA[3] = -1

    # Tetrahedrals (legacy and current)
    cdef int [2] typeB
    if '92' in allowable_types:
        typeB[0] = 92
    else:
        typeB[0] = -1

    if '187' in allowable_types:
        typeB[1] = 187
    else:
        typeB[1] = -1

    # shell types
    planetype = ['42', '82', '154', '181', '182', '183']
    cdef int [6] typeC
    for i, atype in enumerate(planetype):
        if atype in allowable_types:
            typeC[i] = int(atype)
        else:
            typeC[i] = -1

    # line elements
    cdef int [1] linetype
    for i, atype in enumerate(['188']):
        if atype in allowable_types:
            linetype[i] = int(atype)

    # arrays (efficiency warning astype is copying)
    cdef int [:, ::1] ekey = raw['ekey'].astype(ctypes.c_int)
    cdef int [:, ::1] elem = raw['elem'].astype(ctypes.c_int)
    cdef int [::1] etype = raw['etype'].astype(ctypes.c_int)
    cdef int [::1] nnum = raw['nnum'].astype(ctypes.c_int)
    cdef int [::1] raw_enum = raw['enum'].astype(ctypes.c_int)
    cdef int [::1] raw_rcon = raw['e_rcon'].astype(ctypes.c_int)
    
    cdef int nelem = elem.shape[0]
    cdef int nnode = nnum.shape[0]

    # arrays for element numbering, type, and real constants
    cdef int [::1] enum = np.empty(nelem, ctypes.c_int)
    cdef int [::1] etype_out = np.empty(nelem, ctypes.c_int)
    cdef int [::1] rcon = np.empty(nelem, ctypes.c_int)

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
    cdef int64_t [::1] offset = np.empty(nelem, ctypes.c_int64)
    cdef uint8 [::1] cell_type = np.empty(nelem, dtype='uint8')
    
    # different array sizes depending on midside nodes
    cdef int64_t [::1] cells = np.empty(nelem*21, ctypes.c_int64)  # max cell is 20 and header is 1
    
    # Find the highest node number
    cdef int maxnodenum = 0
    for i in range(nnode):
        if nnum[i] > maxnodenum:
            maxnodenum = nnum[i]
            
    # Create reference array for node renumbering
    cdef int64_t n
    cdef int64_t [::1] numref = np.empty(maxnodenum + 2, ctypes.c_int64)
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
    cdef int64_t ccount = 0 # cell/offset counter
    cdef int64_t ecount = 0 # element number counter
    cdef int64_t cstart
    cdef int elem_etype
    for i in range(nelem):
        elem_etype = elem_type[etype[i]]
        cstart = ccount

        for j in range(4):
            if elem_etype == typeA[j]:
                enum[ecount] = raw_enum[i]
                etype_out[ecount] = elem_etype
                rcon[ecount] = raw_rcon[i]
                
                # Set to read quadradic nodes
                if force_linear:
                    lin = 1
                else:
                    # Check if linear (missing midside nodes)
                    lin = elem[i, 8] == -1
                    
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
            if elem_etype == typeB[j]:
                enum[ecount] = raw_enum[i]
                etype_out[ecount] = elem_etype
                rcon[ecount] = raw_rcon[i]

                if force_linear:
                    lin = 1
                else:
                    lin = elem[i, 8] == -1

                StoreTet_TypeB(offset, &ecount, &ccount, cells, cell_type, 
                               numref, elem, i, lin)

                break  # Continue to next element

        # test if surface element
        for j in range(6):  # length needs to be equal to typeC
            if elem_etype == typeC[j]:
                enum[ecount] = raw_enum[i]
                etype_out[ecount] = elem_etype
                rcon[ecount] = raw_rcon[i]

                if force_linear:
                    lin = 1
                else:
                    lin = elem[i, 4] == -1

                # check if this is a triangle
                if elem[i, 2] == elem[i, 3]:
                    StoreSurfTri(offset, &ecount, &ccount, cells, cell_type, 
                                 numref, elem, i, lin)
                else:
                    StoreSurfQuad(offset, &ecount, &ccount, cells, cell_type, 
                                  numref, elem, i, lin)
                break  # Continue to next element
            # continue

        # test if line element
        for j in range(1):
            if elem_etype == linetype[j]:
                enum[ecount] = raw_enum[i]
                etype_out[ecount] = elem_etype
                rcon[ecount] = raw_rcon[i]

                lin = 1
                StoreLine(offset, &ecount, &ccount, cells, cell_type, 
                             numref, elem, i, lin)

        # If permitted, add null element if element isn't in the allowable types
        if cstart == ccount and null_unallowed:
            enum[ecount] = raw_enum[i]
            etype_out[ecount] = elem_etype
            rcon[ecount] = raw_rcon[i]
            offset[ecount] = ccount

            # add null cell
            cells[ccount] = 0; ccount += 1
        
            cell_type[ecount] = VTK_EMPTY_CELL
            ecount += 1


    return np.asarray(cells[:ccount]), np.asarray(offset[:ecount]), \
           np.asarray(cell_type[:ecount]), np.asarray(numref), \
           np.asarray(enum[:ecount]), np.asarray(etype_out[:ecount]), \
           np.asarray(rcon[:ecount])
