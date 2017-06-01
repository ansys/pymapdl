import numpy as np

# VTK cell type numbering from header file

# Linear elements                   
vtktetnum = 10 # VTK_TETRA = 10
vtkpyrnum = 14 # VTK_PYRAMID = 14,
vtkwegnum = 13 # VTK_WEDGE = 13
vtkhexnum = 12 # VTK_HEXAHEDRON = 12

# Quadradic elements
vtkquadtetnum = 24 # VTK_QUADRATIC_TETRA = 24
vtkquadpyrnum = 27 # VTK_QUADRATIC_PYRAMID = 27
vtkquadwegnum = 26 # VTK_QUADRATIC_WEDGE = 26
vtkquadhexnum = 25 # VTK_QUADRATIC_HEXAHEDRON = 25
                   
# ANSYS mixed mesh types             
typeA = np.empty(4, np.int64)
typeA[0] = 45
typeA[1] = 95
typeA[2] = 185
typeA[3] = 186

# ANSYS tetrahedral mesh
typeB = np.empty(2, np.int64)
typeB[0] = 92
typeB[1] = 187

#==============================================================================
# Cell storage
#==============================================================================
def StoreTet_TypeB(offset, ecount, ccount, cells, cell_type, numref, elem, i,
                   lin):
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
    offset[ecount] = ccount
    
    if lin:
        cells[ccount] = 4; ccount += 1
        
        # Populate cell array while renumbering nodes
        for j in range(4):
            cells[ccount] = numref[elem[i, j]]; ccount += 1
        
        # Populate cell type array
        cell_type[ecount] = vtktetnum
        
    else:
        cells[ccount] = 10; ccount += 1
        
        # Populate cell array while renumbering nodes
        for j in range(10):
            cells[ccount] = numref[elem[i, j]]; ccount += 1
        
        # Populate cell type array
        cell_type[ecount] = vtkquadtetnum
        
    ecount += 1
    return ccount, ecount
        

def StoreTet(offset, ecount, ccount, cells, cell_type, numref, elem, i, lin):
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
    offset[ecount] = ccount
    
    # Populate cell type array and 
    if lin:
        cells[ccount] = 4; ccount += 1
        cell_type[ecount] = vtktetnum
        
    else:
        cells[ccount] = 10; ccount += 1
        cell_type[ecount] = vtkquadtetnum
        

    # Populate cell array while renumbering nodes

    # edge nodes
    # [0, 1, 2, 2, 3, 3, 3, 3]
    cells[ccount] = numref[elem[i, 0]]; ccount += 1
    cells[ccount] = numref[elem[i, 1]]; ccount += 1
    cells[ccount] = numref[elem[i, 2]]; ccount += 1
    cells[ccount] = numref[elem[i, 4]]; ccount += 1
        
    # midside nodes
    if not lin:
        cells[ccount] = numref[elem[i,  8]]; ccount += 1
        cells[ccount] = numref[elem[i,  9]]; ccount += 1
        cells[ccount] = numref[elem[i, 11]]; ccount += 1
        cells[ccount] = numref[elem[i, 16]]; ccount += 1
        cells[ccount] = numref[elem[i, 17]]; ccount += 1
        cells[ccount] = numref[elem[i, 18]]; ccount += 1
    
    ecount += 1
    return ccount, ecount
    

def StoreWeg(offset, ecount, ccount, cells, cell_type, numref, elem, i, lin):
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
    offset[ecount] = ccount
    
    if lin:
        cells[ccount] = 6; ccount += 1
        cell_type[ecount] = vtkwegnum

    else:
        cells[ccount] = 15; ccount += 1
        cell_type[ecount] = vtkquadwegnum

    # Populate cell array while renumbering nodes
    # [0, 1, 2, 2, 3, 4, 5, 5]
    cells[ccount] = numref[elem[i, 2]]; ccount += 1
    cells[ccount] = numref[elem[i, 1]]; ccount += 1
    cells[ccount] = numref[elem[i, 0]]; ccount += 1
    cells[ccount] = numref[elem[i, 6]]; ccount += 1
    cells[ccount] = numref[elem[i, 5]]; ccount += 1
    cells[ccount] = numref[elem[i, 4]]; ccount += 1

    if not lin:
        # midside nodes
        cells[ccount] = numref[elem[i,  9]]; ccount += 1
        cells[ccount] = numref[elem[i,  8]]; ccount += 1
        cells[ccount] = numref[elem[i, 11]]; ccount += 1
        cells[ccount] = numref[elem[i, 13]]; ccount += 1
        cells[ccount] = numref[elem[i, 12]]; ccount += 1
        cells[ccount] = numref[elem[i, 15]]; ccount += 1
        cells[ccount] = numref[elem[i, 18]]; ccount += 1
        cells[ccount] = numref[elem[i, 17]]; ccount += 1
        cells[ccount] = numref[elem[i, 16]]; ccount += 1

    ecount += 1
    return ccount, ecount
    

def StorePyr(offset, ecount, ccount, cells, cell_type, numref, elem, i, lin):
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
    (0, 1), (1, 2), (2, 3), (3, 0), (0, 4), (1, 4), (2, 4), (3, 4)
    """

    # Populate offset and cell type arrays
    offset[ecount] = ccount  
    
    # Populate cell array while renumbering nodes
    if lin:
        cells[ccount] = 5; ccount += 1
        cell_type[ecount] = vtkpyrnum
    else:
        cells[ccount] = 13; ccount += 1
        cell_type[ecount] = vtkquadpyrnum
    
    # edge nodes
    # [0, 1, 2, 3, 4, X, X, X]
    for k in range(5):
        cells[ccount] = numref[elem[i, k]]
        ccount += 1
        
    # Populate array
    if not lin:
        for k in range(8, 12):
            cells[ccount] = numref[elem[i, k]]
            ccount += 1
            
        for k in range(16, 20):
            cells[ccount] = numref[elem[i, k]]
            ccount += 1
    
    ecount += 1
    return ccount, ecount


def StoreHex(offset, ecount, ccount, cells, cell_type, numref, elem, i, lin):
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
    offset[ecount] = ccount
    if lin:
        cells[ccount] = 8; ccount += 1
        cell_type[ecount] = vtkhexnum

        for k in range(8):
            cells[ccount] = numref[elem[i, k]]
            ccount += 1

    else:
        cells[ccount] = 20; ccount += 1
        cell_type[ecount] = vtkquadhexnum
        
        for k in range(20):
            cells[ccount] = numref[elem[i, k]]
            ccount += 1

    ecount += 1
    return ccount, ecount
    
#==============================================================================
# Parses raw data without adding fem data
#==============================================================================
def Parse(raw, force_linear):
    """ Pythonic implementation of CDB parser """
    
    # Import from raw dictionary
    ekey = raw['ekey']
    elem = raw['elem']
    etype = raw['etype']
    nnum = raw['nnum']
    
    nelem = elem.shape[0]
    nnode = nnum.shape[0]

    # Find the max element type number
    nekey = ekey.shape[0]
    maxelemtype = 0
    for i in range(nekey):
        if ekey[i, 0] > maxelemtype:
            maxelemtype = ekey[i, 0]
    
    # Create an element type array for indexing
    elem_type = np.empty(maxelemtype + 1, np.int32)
    for i in range(nekey):
        elem_type[ekey[i, 0]] = ekey[i, 1]
    
    # Allocate memory for cell data
    offset = np.empty(nelem, np.int64)
    cell_type = np.empty(nelem, dtype='uint8')
    
    # different array sizes depending on midside nodes
    cells = np.empty(nelem*(20 + 1), np.int64) # max cell is 20 and header is 1
    
    # Find the highest node number
    maxnodenum = 0
    for i in range(nnode):
        if nnum[i] > maxnodenum:
            maxnodenum = nnum[i]
    
    # Create reference array for node renumbering
    numref = np.empty(maxnodenum + 1, np.int64)
    for n in range(nnode):
        numref[nnum[n]] = n
    
    # Loop through each element and check if the element type matches one this code
    # can read
    ccount = 0 # cell/offset counter
    ecount = 0 # element number counter
    for i in range(nelem):
        
        # Test for element type A
        for j in range(4):
            if elem_type[etype[i]] == typeA[j]:
                ##################### Read element type A #####################
                # Determine if linear
                if force_linear:
                    lin = True
                else:
                    lin = elem[i, 8] == -1
            
                if elem[i, 6] != elem[i, 7]: # if hexahedral
                    ccount, ecount = StoreHex(offset, ecount, ccount, cells, 
                                              cell_type, numref, elem, i, lin)
                                 
                elif elem[i, 5] != elem[i, 6]: # if wedge
                    ccount, ecount = StoreWeg(offset, ecount, ccount, cells, 
                                              cell_type, numref, elem, i, lin)

                elif elem[i, 2] != elem[i, 3]: # if pyramid
                    ccount, ecount = StorePyr(offset, ecount, ccount, cells, 
                                              cell_type, numref, elem, i, lin)

                else: # if tetrahedral
                    ccount, ecount = StoreTet(offset, ecount, ccount, cells, 
                                              cell_type, numref, elem, i, lin)
                                              
                break # don't continue testing element types

        # Test for element type B
        for j in range(2):
            if elem_type[etype[i]] == typeB[j]:
                if force_linear:
                    lin = True
                else:
                    lin = elem[i, 4] == -1

                ccount, ecount = StoreTet_TypeB(offset, ecount, ccount, cells,
                                                cell_type, numref, elem, i, 
                                                lin)
                            
                break # don't continue testing element types
                            
        if ecount > i + 1:
            break
                
    # Return spliced arrays
    return np.asarray(cells[:ccount]), np.asarray(offset[:ecount]), np.asarray(cell_type[:ecount]), np.asarray(numref)             

                   
#==============================================================================
# For FEM    
#==============================================================================
## Define cell edges ##
tetedges = np.empty((6, 2), np.int32)
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


pyredges = np.empty((8, 2), np.int32)
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

wegedges = np.empty((9, 2), np.int32)
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

hexedges = np.empty((12, 2), np.int32)
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
wegnum = np.empty(6, np.int32)
wegnum[0] = 2
wegnum[1] = 1
wegnum[2] = 0
wegnum[3] = 6
wegnum[4] = 5
wegnum[5] = 4


# Tetrahedral element
tetnum = np.empty(4, np.int32)
tetnum[0] = 0
tetnum[1] = 1
tetnum[2] = 2
tetnum[3] = 4


# Midside node indices for a type A element
typeAmidind = np.empty((12, 2), np.int32)
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
wegmid = np.empty(9, np.int32)
wegmid[0] = 0
wegmid[1] = 1
wegmid[2] = 3
wegmid[3] = 4
wegmid[4] = 5
wegmid[5] = 7
wegmid[6] = 8
wegmid[7] = 9
wegmid[8] = 10


pyrmid = np.empty(8, np.int32)
pyrmid[0] = 0
pyrmid[1] = 1
pyrmid[2] = 2
pyrmid[3] = 3
pyrmid[4] = 8
pyrmid[5] = 9
pyrmid[6] = 10
pyrmid[7] = 11

tetmid = np.empty(6, np.int32)
tetmid[0] = 0
tetmid[1] = 1
tetmid[2] = 3
tetmid[3] = 8
tetmid[4] = 9
tetmid[5] = 10


typeBmidind = np.empty((6, 2), np.int32)
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

tetmidB = np.empty(6, np.int32)
tetmidB[0] = 4
tetmidB[1] = 5
tetmidB[2] = 6
tetmidB[3] = 7
tetmidB[4] = 8
tetmidB[5] = 9


def ParseForFEM(raw):
    """
    Alternative approach for parsing the raw data from a cdb
    
    Colapses node numbering to 0 for downstream use
    """
    
    ekey = raw['ekey']
    elem = raw['elem']
    etype = raw['etype']
    nnum = raw['nnum']
    
    nelem = elem.shape[0]
    nnode = nnum.shape[0]

    # Find the max element type number
    nekey = ekey.shape[0]
    maxelemtype = 0
    for i in range(nekey):
        if ekey[i, 0] > maxelemtype:
            maxelemtype = ekey[i, 0]
    
    # Create an element type array for indexing
    elem_type = np.empty(maxelemtype + 1, np.int32)
    for i in range(nekey):
        elem_type[ekey[i, 0]] = ekey[i, 1]
    
    # Allocate memory for cell data
    offset = np.empty(nelem, np.int64)
    cell_type = np.empty(nelem, dtype='uint8')
    
    # different array sizes depending on midside nodes
    cells = np.empty(nelem*9, np.int64)  # max cell is 8 and header is 1
    
    # Find the highest node number
    maxnodenum = 0
    for i in range(nnode):
        if nnum[i] > maxnodenum:
            maxnodenum = nnum[i]
    
    # Create reference array for node renumbering
    nodeused = np.zeros(maxnodenum + 1, dtype='uint8')

    # Loop through to see which nodes will be used
    c = 0
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
    c = 0
    for i in range(maxnodenum + 1):
        if nodeused[i]:
            c += 1

    # Track original node numbering        
    orignum = np.empty(nnode, np.int64)
    c = 0
    for i in range(maxnodenum + 1):
        if nodeused[i]:
            orignum[c] = i
            c += 1
        
    # Node reference array relating original node numbering to new node
    # numbering
    numref = np.empty(maxnodenum + 1, np.int64)
    c = 0 # reset counter (this becomes the number of valid nodes)
    for i in range(maxnodenum + 1):
        if nodeused[i]:
            numref[i] = c
            c += 1 # increment counter for next node
        else:
            numref[i] = -1

    # Create edges and square cell type array
    edges = np.empty((nelem*12, 2), np.int64)
    cellarr = np.zeros((nelem, 8), np.int32)
    ncellpts = np.empty(nelem, np.int32)
    
    # Track if elements are used
    elemused = np.zeros(nelem, dtype='uint8')
    
    # Also, track the indices of the midside nodes based on their adjcent edge
    # nodes in the new indexing
    midedgeind = np.empty((nnode, 2), np.int64) # sized for maximum number of nodes, will trim later
    
    # Also track the original midside node indices
    midind = np.empty(nnode, np.int64) # sized for maximum number of nodes, will trim later
    midnode = 0
    
    # Array to track if a midside node has been stored
    midstored = np.zeros(maxnodenum + 1, np.int32)
    
    # Loop through each element and check if the element type matches one this code
    # can read
    ccount = 0 # cell/offset counter
    ecount = 0 # element number counter
    edgenum = 0
    for i in range(nelem):
        ############ Read element typeA ############
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
                    # if it exists (isn't zero because ANSYS is weird) and hasn't been
                    if elem[i, tetmidB[k]] > 0 and midstored[elem[i, tetmidB[k]]]:
                        # Add its adjcent nodes to the index array tracker
                        midedgeind[midnode, 0] = numref[elem[i, typeBmidind[k][0]]]
                        midedgeind[midnode, 1] = numref[elem[i, typeBmidind[k][1]]]
                        midind[midnode] = elem[i, tetmidB[k]]

                        # track as stored and increment
                        midstored[elem[i, tetmidB[k]]] = 1
                        midnode += 1

                
                # Populate cell type array
                cell_type[ecount] = vtkhexnum
                
                # Increment element counter and track that it is used
                ecount += 1   
                elemused[i] = 1                    
                break # proceed to next element        
                    
                    
    # Regenerate node list
    oldnodes = raw['nodes'] # c is the number of valid edge nodes
    nodes = np.empty((c, 6)) # c is the number of valid edge nodes
    nodenum = np.zeros(c, dtype=np.int64) # track if nodes are used

    n = 0 # index for old node numbering system
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
    
