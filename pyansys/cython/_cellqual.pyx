# cython: language_level=3
# cython: infer_types=True
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True
# cython: nonecheck=False

# cython imports
from libc.math cimport sqrt
ctypedef unsigned char uint8
from libc.stdint cimport int64_t
from cython.parallel import prange

import numpy as np
cimport numpy as np
import ctypes


cdef uint8 VTK_HEXAHEDRON = 12
cdef uint8 VTK_PYRAMID = 14
cdef uint8 VTK_TETRA = 10
cdef uint8 VTK_WEDGE = 13
cdef uint8 VTK_QUADRATIC_TETRA = 24
cdef uint8 VTK_QUADRATIC_PYRAMID = 27
cdef uint8 VTK_QUADRATIC_WEDGE = 26
cdef uint8 VTK_QUADRATIC_HEXAHEDRON = 25


cdef double div_fac = 1/3.0
cdef double div_fac6 = 1/6.0
cdef double TAU_WEG = (4/5.0)*(1 - 2**0.5*1.0/39**(1/4.0))

# NAN
cdef double d_nan = np.nan

# maximum number of threads
cdef int MAX_THREADS = 4


cdef inline double dabs(double x) nogil:
    """ Double absolute value """
    if x > 0.0:
        return x
    else:
        return -x


cdef inline double fabs(float x) nogil:
    """ Float absolute value """
    if x > 0.0:
        return x
    else:
        return -x


cdef inline void vector_sub(double [3] e0, double [3] e1, double [3] e2) nogil:
    """ Vector subtraction """
    e2[0] = e0[0] - e1[0]
    e2[1] = e0[1] - e1[1]
    e2[2] = e0[2] - e1[2]


cdef inline void vector_sub_float(float [3] e0, float [3] e1, float [3] e2) nogil:
    """ Vector subtraction """
    e2[0] = e0[0] - e1[0]
    e2[1] = e0[1] - e1[1]
    e2[2] = e0[2] - e1[2]


cdef inline double triple_product(double [3] ab, double [3] bc, double [3] cd) nogil:
    return ab[0] * (bc[1] * cd[2] - bc[2] * cd[1]) -\
           bc[0] * (ab[1] * cd[2] - ab[2] * cd[1]) +\
           cd[0] * (ab[1] * bc[2] - ab[2] * bc[1])


cdef inline float triple_product_float(float [3] ab, float [3] bc, float [3] cd) nogil:
    return ab[0] * (bc[1] * cd[2] - bc[2] * cd[1]) -\
           bc[0] * (ab[1] * cd[2] - ab[2] * cd[1]) +\
           cd[0] * (ab[1] * bc[2] - ab[2] * bc[1])


cdef inline void cross(double [3] e0, double [3] e1, double [3] vec) nogil:
    vec[0] = e0[1]*e1[2] - e0[2]*e1[1]
    vec[1] = e0[2]*e1[0] - e0[0]*e1[2]
    vec[2] = e0[0]*e1[1] - e0[1]*e1[0]


cdef inline void cross_float(float [3] e0, float [3] e1, float [3] vec) nogil:
    vec[0] = e0[1]*e1[2] - e0[2]*e1[1]
    vec[1] = e0[2]*e1[0] - e0[0]*e1[2]
    vec[2] = e0[0]*e1[1] - e0[1]*e1[0]


cdef inline double vector_norm(double [3] vec) nogil:
    return sqrt(vec[0]**2 + vec[1]**2 + vec[2]**2)


cdef inline float vector_norm_float(float [3] vec) nogil:
    return sqrt(vec[0]**2 + vec[1]**2 + vec[2]**2)


#==============================================================================
# Quadratic element relaxation functions
#==============================================================================
cdef inline void tet_relax_mid(int64_t [::1] cells, int c, double [:, ::1] pts,
                              double rfac) nogil:
    """
    Resets the midside nodes of the tetrahedral starting at index c
    
    relaxation factor rfac
    
    midedge nodes between
    (0,1), (1,2), (2,0), (0,3), (1,3), and (2,3)
    
    """
    cdef int ind0 = cells[c + 0]
    cdef int ind1 = cells[c + 1]
    cdef int ind2 = cells[c + 2]
    cdef int ind3 = cells[c + 3]
    cdef int ind4 = cells[c + 4]
    cdef int ind5 = cells[c + 5]
    cdef int ind6 = cells[c + 6]
    cdef int ind7 = cells[c + 7]
    cdef int ind8 = cells[c + 8]
    cdef int ind9 = cells[c + 9]

    for j in range(3):
        pts[ind4, j] = pts[ind4, j]*(1 - rfac) + (pts[ind0, j] + pts[ind1, j])*0.5*rfac
        pts[ind5, j] = pts[ind5, j]*(1 - rfac) + (pts[ind1, j] + pts[ind2, j])*0.5*rfac
        pts[ind6, j] = pts[ind6, j]*(1 - rfac) + (pts[ind2, j] + pts[ind0, j])*0.5*rfac
        pts[ind7, j] = pts[ind7, j]*(1 - rfac) + (pts[ind0, j] + pts[ind3, j])*0.5*rfac
        pts[ind8, j] = pts[ind8, j]*(1 - rfac) + (pts[ind1, j] + pts[ind3, j])*0.5*rfac
        pts[ind9, j] = pts[ind9, j]*(1 - rfac) + (pts[ind2, j] + pts[ind3, j])*0.5*rfac


cdef inline void pyr_relax_mid(int64_t [::1] cells, int c, double [:, ::1] pts,
                              double rfac) nogil:
    """
    
    5 (0, 1)
    6 (1, 2)
    7 (2, 3)
    8 (3, 0)
    9 (0, 4)
    10(1, 4)
    11(2, 4)
    12(3, 4)
    
    """
    cdef int ind0 = cells[c + 0]
    cdef int ind1 = cells[c + 1]
    cdef int ind2 = cells[c + 2]
    cdef int ind3 = cells[c + 3]
    cdef int ind4 = cells[c + 4]
    cdef int ind5 = cells[c + 5]
    cdef int ind6 = cells[c + 6]
    cdef int ind7 = cells[c + 7]
    cdef int ind8 = cells[c + 8]
    cdef int ind9 = cells[c + 9]
    cdef int ind10= cells[c + 10]
    cdef int ind11= cells[c + 11]
    cdef int ind12= cells[c + 12]

    cdef int j

    for j in range(3):
        pts[ind5, j]  = pts[ind5,  j]*(1 - rfac) + (pts[ind0, j] + pts[ind1, j])*0.5*rfac
        pts[ind6, j]  = pts[ind6,  j]*(1 - rfac) + (pts[ind1, j] + pts[ind2, j])*0.5*rfac
        pts[ind7, j]  = pts[ind7,  j]*(1 - rfac) + (pts[ind2, j] + pts[ind3, j])*0.5*rfac
        pts[ind8, j]  = pts[ind8,  j]*(1 - rfac) + (pts[ind3, j] + pts[ind0, j])*0.5*rfac
        pts[ind9, j]  = pts[ind9,  j]*(1 - rfac) + (pts[ind0, j] + pts[ind4, j])*0.5*rfac
        pts[ind10, j] = pts[ind10, j]*(1 - rfac) + (pts[ind1, j] + pts[ind4, j])*0.5*rfac
        pts[ind11, j] = pts[ind11, j]*(1 - rfac) + (pts[ind2, j] + pts[ind4, j])*0.5*rfac
        pts[ind12, j] = pts[ind12, j]*(1 - rfac) + (pts[ind3, j] + pts[ind4, j])*0.5*rfac


cdef inline void weg_relax_mid(int64_t [::1] cells, int c, double [:, ::1] pts,
                              double rfac) nogil:
    """
    
    6  (0,1)
    7  (1,2)
    8  (2,0)
    9  (3,4)
    10 (4,5)
    11 (5,3)
    12 (0,3)
    13 (1,4)
    14 (2,5)
    """
    cdef int ind0 = cells[c + 0]
    cdef int ind1 = cells[c + 1]
    cdef int ind2 = cells[c + 2]
    cdef int ind3 = cells[c + 3]
    cdef int ind4 = cells[c + 4]
    cdef int ind5 = cells[c + 5]
    cdef int ind6 = cells[c + 6]
    cdef int ind7 = cells[c + 7]
    cdef int ind8 = cells[c + 8]
    cdef int ind9 = cells[c + 9]
    cdef int ind10= cells[c + 10]
    cdef int ind11= cells[c + 11]
    cdef int ind12= cells[c + 12]
    cdef int ind13= cells[c + 13]
    cdef int ind14= cells[c + 14]
    
    cdef int j

    for j in range(3):
        pts[ind6, j]  = pts[ind6,  j]*(1 - rfac) + (pts[ind0, j] + pts[ind1, j])*0.5*rfac
        pts[ind7, j]  = pts[ind7,  j]*(1 - rfac) + (pts[ind1, j] + pts[ind2, j])*0.5*rfac
        pts[ind8, j]  = pts[ind8,  j]*(1 - rfac) + (pts[ind2, j] + pts[ind0, j])*0.5*rfac
        pts[ind9, j]  = pts[ind9,  j]*(1 - rfac) + (pts[ind3, j] + pts[ind4, j])*0.5*rfac
        pts[ind10, j] = pts[ind10, j]*(1 - rfac) + (pts[ind4, j] + pts[ind5, j])*0.5*rfac
        pts[ind11, j] = pts[ind11, j]*(1 - rfac) + (pts[ind5, j] + pts[ind3, j])*0.5*rfac
        pts[ind12, j] = pts[ind12, j]*(1 - rfac) + (pts[ind0, j] + pts[ind3, j])*0.5*rfac
        pts[ind13, j] = pts[ind13, j]*(1 - rfac) + (pts[ind1, j] + pts[ind4, j])*0.5*rfac
        pts[ind14, j] = pts[ind14, j]*(1 - rfac) + (pts[ind2, j] + pts[ind5, j])*0.5*rfac


cdef inline void hex_relax_mid(int64_t [::1] cells, int c, double [:, ::1] pts,
                              double rfac) nogil:

    """
    
    8  (0,1)
    9  (1,2)
    10 (2,3)
    11 (3,0)
    12 (4,5)
    13 (5,6)
    14 (6,7)
    15 (7,4)
    16 (0,4)
    17 (1,5)
    18 (2,6)
    19 (3,7)
    
    """
    
    cdef int ind0 = cells[c + 0]
    cdef int ind1 = cells[c + 1]
    cdef int ind2 = cells[c + 2]
    cdef int ind3 = cells[c + 3]
    cdef int ind4 = cells[c + 4]
    cdef int ind5 = cells[c + 5]
    cdef int ind6 = cells[c + 6]
    cdef int ind7 = cells[c + 7]
    cdef int ind8 = cells[c + 8]
    cdef int ind9 = cells[c + 9]
    cdef int ind10= cells[c + 10]
    cdef int ind11= cells[c + 11]
    cdef int ind12= cells[c + 12]
    cdef int ind13= cells[c + 13]
    cdef int ind14= cells[c + 14]
    cdef int ind15= cells[c + 15]
    cdef int ind16= cells[c + 16]
    cdef int ind17= cells[c + 17]
    cdef int ind18= cells[c + 18]
    cdef int ind19= cells[c + 19]

    cdef int j

    for j in range(3):
        pts[ind8, j]  = pts[ind8,  j]*(1 - rfac) + (pts[ind0, j] + pts[ind1, j])*0.5*rfac
        pts[ind9, j]  = pts[ind9,  j]*(1 - rfac) + (pts[ind1, j] + pts[ind2, j])*0.5*rfac
        pts[ind10, j] = pts[ind10, j]*(1 - rfac) + (pts[ind2, j] + pts[ind3, j])*0.5*rfac
        pts[ind11, j] = pts[ind11, j]*(1 - rfac) + (pts[ind3, j] + pts[ind0, j])*0.5*rfac
        pts[ind12, j] = pts[ind12, j]*(1 - rfac) + (pts[ind4, j] + pts[ind5, j])*0.5*rfac
        pts[ind13, j] = pts[ind13, j]*(1 - rfac) + (pts[ind5, j] + pts[ind6, j])*0.5*rfac
        pts[ind14, j] = pts[ind14, j]*(1 - rfac) + (pts[ind6, j] + pts[ind7, j])*0.5*rfac
        pts[ind15, j] = pts[ind15, j]*(1 - rfac) + (pts[ind7, j] + pts[ind4, j])*0.5*rfac
        pts[ind16, j] = pts[ind16, j]*(1 - rfac) + (pts[ind0, j] + pts[ind4, j])*0.5*rfac
        pts[ind17, j] = pts[ind17, j]*(1 - rfac) + (pts[ind1, j] + pts[ind5, j])*0.5*rfac
        pts[ind18, j] = pts[ind18, j]*(1 - rfac) + (pts[ind2, j] + pts[ind6, j])*0.5*rfac
        pts[ind19, j] = pts[ind19, j]*(1 - rfac) + (pts[ind3, j] + pts[ind7, j])*0.5*rfac


# Wedge
cdef int [6][3] weg_dual_ind
weg_dual_ind[0][0] = 0
weg_dual_ind[0][1] = 1
weg_dual_ind[0][2] = 3

weg_dual_ind[1][0] = 0
weg_dual_ind[1][1] = 2
weg_dual_ind[1][2] = 1

weg_dual_ind[2][0] = 0
weg_dual_ind[2][1] = 3
weg_dual_ind[2][2] = 2

weg_dual_ind[3][0] = 4
weg_dual_ind[3][1] = 3
weg_dual_ind[3][2] = 1

weg_dual_ind[4][0] = 4
weg_dual_ind[4][1] = 1
weg_dual_ind[4][2] = 2

weg_dual_ind[5][0] = 4
weg_dual_ind[5][1] = 2
weg_dual_ind[5][2] = 3


# Pyramid
cdef int [5][2] pyr_face_ind
pyr_face_ind[1][0] = 0
pyr_face_ind[1][1] = 1

pyr_face_ind[2][0] = 1
pyr_face_ind[2][1] = 2

pyr_face_ind[3][0] = 2
pyr_face_ind[3][1] = 3

pyr_face_ind[4][0] = 3
pyr_face_ind[4][1] = 0

cdef int [4][2] pyr_dual_ind
pyr_dual_ind[0][0] = 1
pyr_dual_ind[0][1] = 4

pyr_dual_ind[1][0] = 2
pyr_dual_ind[1][1] = 1

pyr_dual_ind[2][0] = 3
pyr_dual_ind[2][1] = 2

pyr_dual_ind[3][0] = 4
pyr_dual_ind[3][1] = 3


cdef int [4][3] tet_face_ind
tet_face_ind[0][0] = 0
tet_face_ind[0][1] = 1
tet_face_ind[0][2] = 2

tet_face_ind[1][0] = 0
tet_face_ind[1][1] = 1
tet_face_ind[1][2] = 3

tet_face_ind[2][0] = 1
tet_face_ind[2][1] = 2
tet_face_ind[2][2] = 3

tet_face_ind[3][0] = 2
tet_face_ind[3][1] = 0
tet_face_ind[3][2] = 3


cdef int [4][3] tet_dual_ind
tet_dual_ind[0][0] = 0
tet_dual_ind[0][1] = 1
tet_dual_ind[0][2] = 3

tet_dual_ind[1][0] = 0
tet_dual_ind[1][1] = 2
tet_dual_ind[1][2] = 1

tet_dual_ind[2][0] = 0
tet_dual_ind[2][1] = 3
tet_dual_ind[2][2] = 2

tet_dual_ind[3][0] = 1
tet_dual_ind[3][1] = 2
tet_dual_ind[3][2] = 3


# ============================================================================
# Linear shape checking functions
# Tetrahedral edges  
cdef int [4][3] tet_edges
tet_edges[0][0] = 1
tet_edges[0][1] = 2
tet_edges[0][2] = 3

tet_edges[1][0] = 2
tet_edges[1][1] = 0
tet_edges[1][2] = 3

tet_edges[2][0] = 0
tet_edges[2][1] = 1
tet_edges[2][2] = 3

tet_edges[3][0] = 0
tet_edges[3][1] = 2
tet_edges[3][2] = 1

# Pyramid edges
cdef int [4][3] pyr_edges

pyr_edges[0][0] = 1
pyr_edges[0][1] = 3
pyr_edges[0][2] = 4

pyr_edges[1][0] = 2
pyr_edges[1][1] = 0
pyr_edges[1][2] = 4

pyr_edges[2][0] = 3
pyr_edges[2][1] = 1
pyr_edges[2][2] = 4

pyr_edges[3][0] = 0
pyr_edges[3][1] = 2
pyr_edges[3][2] = 4

# Populate wedge edges
cdef int [6][3] weg_edges
weg_edges[0][0] = 2
weg_edges[0][1] = 1
weg_edges[0][2] = 3

weg_edges[1][0] = 0
weg_edges[1][1] = 2
weg_edges[1][2] = 4

weg_edges[2][0] = 1
weg_edges[2][1] = 0
weg_edges[2][2] = 5

weg_edges[3][0] = 4
weg_edges[3][1] = 5
weg_edges[3][2] = 0

weg_edges[4][0] = 5
weg_edges[4][1] = 3
weg_edges[4][2] = 1

weg_edges[5][0] = 3
weg_edges[5][1] = 4
weg_edges[5][2] = 2

# populate hex edges  
cdef int [8][3] hex_edges
hex_edges[0][0] = 1
hex_edges[0][1] = 3
hex_edges[0][2] = 4

hex_edges[1][0] = 2
hex_edges[1][1] = 0
hex_edges[1][2] = 5

hex_edges[2][0] = 3
hex_edges[2][1] = 1
hex_edges[2][2] = 6

hex_edges[3][0] = 0
hex_edges[3][1] = 2
hex_edges[3][2] = 7

hex_edges[4][0] = 7
hex_edges[4][1] = 5
hex_edges[4][2] = 0

hex_edges[5][0] = 4
hex_edges[5][1] = 6
hex_edges[5][2] = 1

hex_edges[6][0] = 5
hex_edges[6][1] = 7
hex_edges[6][2] = 2

hex_edges[7][0] = 6
hex_edges[7][1] = 4
hex_edges[7][2] = 3


cdef inline double repair_weg(double [8][3] temp_fpos,
                              double [8][3] cell_points) nogil:
    """ Compute optimized wedge shape based on GETMe"""
    cdef int indA, indB, indC
    cdef int i, j
    cdef double [8][3] temp_dual_cent, temp_face_cent, temp_norm
    cdef double old_vol, new_vol, volscale, vt0_new, vt1_new, vt2_new
    cdef double vt0_old, vt1_old, vt2_old, fpos_mean, cpos_mean
    cdef double[3] e0, e1, e2, v01, v12, v24, v04, v42, v25, v45, v53

    # Determine element face centroids
    # Face 1: (1, 2, 3)
    for j in range(3):
        temp_face_cent[0][j] = (cell_points[0][j] +
                                cell_points[1][j] +
                                cell_points[2][j])*div_fac
    
    # Face 2: (1, 2, 5, 4)
    for j in range(3):
        temp_face_cent[1][j] = (cell_points[0][j] +
                                cell_points[1][j] +
                                cell_points[4][j] +
                                cell_points[3][j])*0.25
    
    # Face 3: (2, 3, 6, 5)
    for j in range(3):
        temp_face_cent[2][j] = (cell_points[1][j] +
                                cell_points[2][j] +
                                cell_points[5][j] +
                                cell_points[4][j])*0.25
    
    # Face 4: (3, 1, 4, 6)
    for j in range(3):
        temp_face_cent[3][j] = (cell_points[2][j] +
                                cell_points[0][j] +
                                cell_points[3][j] +
                                cell_points[5][j])*0.25
    
    # Face 5: (4, 6, 5)
    for j in range(3):
        temp_face_cent[4][j] = (cell_points[3][j] +
                                cell_points[5][j] +
                                cell_points[4][j])*div_fac
    
    #==========================================================================
    # Dual Element
    #==========================================================================
    # These face centers are the points of the dual element
    # the projection centers are then the mean of these points
    for i in range(6):
        # Compute means
        for j in range(3):
            temp_dual_cent[i][j] = (1 - TAU_WEG)*temp_face_cent[weg_dual_ind[i][0]][j] + \
                                        TAU_WEG*(temp_face_cent[weg_dual_ind[i][1]][j] + 
                                                 temp_face_cent[weg_dual_ind[i][2]][j])*0.5

    #### Compute normal vector extending from the dual faces ####
    # Triangular faces
    for i in range(6):
        vector_sub(temp_face_cent[weg_dual_ind[i][2]], temp_face_cent[weg_dual_ind[i][0]], e0)
        vector_sub(temp_face_cent[weg_dual_ind[i][1]], temp_face_cent[weg_dual_ind[i][0]], e1)
    
        # Perform cross product to get dual element face normal vector
        cross(e0, e1, temp_norm[i])
    
        # Scale normals
        normscale = 2.0/sqrt(vector_norm(temp_norm[i]))

        # add dual normal to face center to get new cell position
        for j in range(3):
            temp_fpos[i][j] = temp_norm[i][j]*normscale + temp_dual_cent[i][j]

    # Scale new element to match volume of old element
    old_vol = volume_weg(cell_points)
    new_vol = volume_weg(temp_fpos)
    volscale = (old_vol/new_vol)**div_fac

    # Determine the mean position of the original element
    for j in range(3):
        cpos_mean = (cell_points[0][j] +
                     cell_points[1][j] +
                     cell_points[2][j] +
                     cell_points[3][j] +
                     cell_points[4][j] +
                     cell_points[5][j])*div_fac6

        fpos_mean = (temp_fpos[0][j] +
                     temp_fpos[1][j] +
                     temp_fpos[2][j] +
                     temp_fpos[3][j] +
                     temp_fpos[4][j] +
                     temp_fpos[5][j])*div_fac6

        # Scale all nodes of the element
        for i in range(6):
            temp_fpos[i][j] = cpos_mean + volscale*(temp_fpos[i][j] - fpos_mean)

    return old_vol


cdef inline float repair_weg_float(float [8][3] temp_fpos,
                                    float [8][3] cell_points) nogil:
    """ Compute optimized wedge shape based on GETMe"""
    cdef int indA, indB, indC
    cdef int i, j
    cdef float [8][3] temp_dual_cent, temp_face_cent, temp_norm
    cdef float old_vol, new_vol, volscale, vt0_new, vt1_new, vt2_new
    cdef float vt0_old, vt1_old, vt2_old, fpos_mean, cpos_mean
    cdef float[3] e0, e1, e2, v01, v12, v24, v04, v42, v25, v45, v53

    # Determine element face centroids
    # Face 1: (1, 2, 3)
    for j in range(3):
        temp_face_cent[0][j] = (cell_points[0][j] +
                                cell_points[1][j] +
                                cell_points[2][j])*div_fac
    
    # Face 2: (1, 2, 5, 4)
    for j in range(3):
        temp_face_cent[1][j] = (cell_points[0][j] +
                                cell_points[1][j] +
                                cell_points[4][j] +
                                cell_points[3][j])*0.25
    
    # Face 3: (2, 3, 6, 5)
    for j in range(3):
        temp_face_cent[2][j] = (cell_points[1][j] +
                                cell_points[2][j] +
                                cell_points[5][j] +
                                cell_points[4][j])*0.25
    
    # Face 4: (3, 1, 4, 6)
    for j in range(3):
        temp_face_cent[3][j] = (cell_points[2][j] +
                                cell_points[0][j] +
                                cell_points[3][j] +
                                cell_points[5][j])*0.25
    
    # Face 5: (4, 6, 5)
    for j in range(3):
        temp_face_cent[4][j] = (cell_points[3][j] +
                                cell_points[5][j] +
                                cell_points[4][j])*div_fac
    
    #==========================================================================
    # Dual Element
    #==========================================================================
    # These face centers are the points of the dual element
    # the projection centers are then the mean of these points
    for i in range(6):
        # Compute means
        for j in range(3):
            temp_dual_cent[i][j] = (1 - TAU_WEG)*temp_face_cent[weg_dual_ind[i][0]][j] + \
                                        TAU_WEG*(temp_face_cent[weg_dual_ind[i][1]][j] + 
                                                 temp_face_cent[weg_dual_ind[i][2]][j])*0.5

    #### Compute normal vector extending from the dual faces ####
    # Triangular faces
    for i in range(6):
        vector_sub_float(temp_face_cent[weg_dual_ind[i][2]], temp_face_cent[weg_dual_ind[i][0]], e0)
        vector_sub_float(temp_face_cent[weg_dual_ind[i][1]], temp_face_cent[weg_dual_ind[i][0]], e1)
    
        # Perform cross product to get dual element face normal vector
        cross_float(e0, e1, temp_norm[i])
    
        # Scale normals
        normscale = 2.0/sqrt(vector_norm_float(temp_norm[i]))

        # add dual normal to face center to get new cell position
        for j in range(3):
            temp_fpos[i][j] = temp_norm[i][j]*normscale + temp_dual_cent[i][j]

    # Scale new element to match volume of old element
    old_vol = volume_weg_float(cell_points)
    new_vol = volume_weg_float(temp_fpos)
    volscale = (old_vol/new_vol)**div_fac

    # Determine the mean position of the original element
    for j in range(3):
        cpos_mean = (cell_points[0][j] +
                     cell_points[1][j] +
                     cell_points[2][j] +
                     cell_points[3][j] +
                     cell_points[4][j] +
                     cell_points[5][j])*div_fac6

        fpos_mean = (temp_fpos[0][j] +
                     temp_fpos[1][j] +
                     temp_fpos[2][j] +
                     temp_fpos[3][j] +
                     temp_fpos[4][j] +
                     temp_fpos[5][j])*div_fac6

        # Scale all nodes of the element
        for i in range(6):
            temp_fpos[i][j] = cpos_mean + volscale*(temp_fpos[i][j] - fpos_mean)

    return old_vol


cdef inline double tet_lin_qual(int64_t [::1] cells, int c, double [:, ::1] pts) nogil:
    """ Returns minimum scaled jacobian of a tetrahedral cell's edge nodes """
    
    cdef int indS, ind0, ind1, ind2    
    cdef double [3] e0
    cdef double [3] e1
    cdef double [3] e2

    cdef int i, j
    cdef double normjac, tnorm
    cdef double jac = 1.1
    
    for i in range(4):
        indS = cells[c + i]
        ind0 = cells[c + tet_edges[i][0]]
        ind1 = cells[c + tet_edges[i][1]]
        ind2 = cells[c + tet_edges[i][2]]
        
        for j in range(3):
            e0[j] = pts[ind0, j] - pts[indS, j]
            e1[j] = pts[ind1, j] - pts[indS, j]
            e2[j] = pts[ind2, j] - pts[indS, j]
           
        # normalize the determinant of the jacobian
        tnorm = (vector_norm(e0)*vector_norm(e1)*vector_norm(e2))            
        normjac = triple_product(e1, e2, e0)/tnorm

        # Track minimum jacobian
        if normjac < jac:
            jac = normjac
            
    return jac*1.414213562373095


cdef inline float tet_lin_qual_float(int64_t [::1] cells, int c,
                                      float [:, ::1] pts) nogil:
    """ Returns minimum scaled jacobian of a tetrahedral cell's edge nodes """
    
    cdef int indS, ind0, ind1, ind2    
    cdef float [3] e0
    cdef float [3] e1
    cdef float [3] e2

    cdef int i, j
    cdef float normjac, tnorm
    cdef float jac = 1.1
    
    for i in range(4):
        indS = cells[c + i]
        ind0 = cells[c + tet_edges[i][0]]
        ind1 = cells[c + tet_edges[i][1]]
        ind2 = cells[c + tet_edges[i][2]]
        
        for j in range(3):
            e0[j] = pts[ind0, j] - pts[indS, j]
            e1[j] = pts[ind1, j] - pts[indS, j]
            e2[j] = pts[ind2, j] - pts[indS, j]
           
        # normalize the determinant of the jacobian
        tnorm = (vector_norm_float(e0)*vector_norm_float(e1)*vector_norm_float(e2))            
        normjac = triple_product_float(e1, e2, e0)/tnorm

        # Track minimum jacobian
        if normjac < jac:
            jac = normjac
            
    return jac*1.414213562373095


cdef inline double pyr_lin_qual(int64_t [::1] cells, int c,
                             double [:, ::1] pts) nogil:
    """ Returns minimum scaled jacobian of a pyramid cell's edge nodes  """
        
    cdef int indS, ind0, ind1, ind2    
        
    cdef double [3] e0
    cdef double [3] e1
    cdef double [3] e2

    cdef int i, j
    cdef double normjac, tnorm
    cdef double jac = 1.1
    
    for i in range(4):
        indS = cells[c + i]
        ind0 = cells[c + pyr_edges[i][0]]
        ind1 = cells[c + pyr_edges[i][1]]
        ind2 = cells[c + pyr_edges[i][2]]
        
        for j in range(3):
            e0[j] = pts[ind0, j] - pts[indS, j]
            e1[j] = pts[ind1, j] - pts[indS, j]
            e2[j] = pts[ind2, j] - pts[indS, j]
           
        # normalize the determinant of the jacobian
        tnorm = (vector_norm(e0)*vector_norm(e1)*vector_norm(e2))            
        normjac = triple_product(e1, e2, e0)/tnorm

        # Track minimum jacobian
        if normjac < jac:
            jac = normjac
            
    return jac*1.14


cdef inline float pyr_lin_qual_float(int64_t [::1] cells, int c,
                                     float [:, ::1] pts) nogil:
    """ Returns minimum scaled jacobian of a pyramid cell's edge nodes  """
    cdef int indS, ind0, ind1, ind2    
    cdef float [3] e0
    cdef float [3] e1
    cdef float [3] e2
    cdef int i, j
    cdef float normjac, tnorm
    cdef float jac = 1.1
    
    for i in range(4):
        indS = cells[c + i]
        ind0 = cells[c + pyr_edges[i][0]]
        ind1 = cells[c + pyr_edges[i][1]]
        ind2 = cells[c + pyr_edges[i][2]]

        for j in range(3):
            e0[j] = pts[ind0, j] - pts[indS, j]
            e1[j] = pts[ind1, j] - pts[indS, j]
            e2[j] = pts[ind2, j] - pts[indS, j]

        # normalize the determinant of the jacobian
        tnorm = (vector_norm_float(e0)*vector_norm_float(e1)*vector_norm_float(e2))
        normjac = triple_product_float(e1, e2, e0)/tnorm

        # Track minimum jacobian
        if normjac < jac:
            jac = normjac
    return jac*1.14


cdef inline double weg_lin_qual(int64_t [::1] cells, int c,
                             double [:, ::1] pts) nogil:
    """ Returns minimum scaled jacobian of a wedge cell's edge nodes  """
        
    cdef int indS, ind0, ind1, ind2    
        
    cdef double [3] e0
    cdef double [3] e1
    cdef double [3] e2

    cdef int i, j
    cdef double normjac, tnorm
    cdef double jac = 1.1
    
    for i in range(6):
        indS = cells[c + i]
        ind0 = cells[c + weg_edges[i][0]]
        ind1 = cells[c + weg_edges[i][1]]
        ind2 = cells[c + weg_edges[i][2]]
        
        for j in range(3):
            e0[j] = pts[ind0, j] - pts[indS, j]
            e1[j] = pts[ind1, j] - pts[indS, j]
            e2[j] = pts[ind2, j] - pts[indS, j]
           
        # normalize the determinant of the jacobian
        tnorm = (vector_norm(e0)*vector_norm(e1)*vector_norm(e2))            
        normjac = triple_product(e1, e2, e0)/tnorm

        # Track minimum jacobian
        if normjac < jac:
            jac = normjac

    return jac*1.154


cdef inline float weg_lin_qual_float(int64_t [::1] cells, int c,
                                     float [:, ::1] pts) nogil:
    """ Returns minimum scaled jacobian of a wedge cell's edge nodes  """
    cdef int indS, ind0, ind1, ind2    
    cdef float [3] e0
    cdef float [3] e1
    cdef float [3] e2
    cdef int i, j
    cdef float normjac, tnorm
    cdef float jac = 1.1
    
    for i in range(6):
        indS = cells[c + i]
        ind0 = cells[c + weg_edges[i][0]]
        ind1 = cells[c + weg_edges[i][1]]
        ind2 = cells[c + weg_edges[i][2]]
        
        for j in range(3):
            e0[j] = pts[ind0, j] - pts[indS, j]
            e1[j] = pts[ind1, j] - pts[indS, j]
            e2[j] = pts[ind2, j] - pts[indS, j]
           
        # normalize the determinant of the jacobian
        tnorm = (vector_norm_float(e0)*vector_norm_float(e1)*vector_norm_float(e2))            
        normjac = triple_product_float(e1, e2, e0)/tnorm

        # Track minimum jacobian
        if normjac < jac:
            jac = normjac

    return jac*1.154


cdef inline double hex_lin_qual(int64_t [::1] cells, int c, double [:, ::1] pts) nogil:
    """ Returns minimum scaled jacobian of a hexahedrals cell's edge nodes  """
    cdef int indS, ind0, ind1, ind2    
        
    cdef double [3] e0
    cdef double [3] e1
    cdef double [3] e2

    cdef int i, j
    cdef double normjac, tnorm
    cdef double jac = 1.1
    
    for i in range(8):
        indS = cells[c + i]
        ind0 = cells[c + hex_edges[i][0]]
        ind1 = cells[c + hex_edges[i][1]]
        ind2 = cells[c + hex_edges[i][2]]
        
        for j in range(3):
            e0[j] = pts[ind0, j] - pts[indS, j]
            e1[j] = pts[ind1, j] - pts[indS, j]
            e2[j] = pts[ind2, j] - pts[indS, j]

        # normalize the determinant of the jacobian
        tnorm = vector_norm(e0)*vector_norm(e1)*vector_norm(e2)
        normjac = triple_product(e1, e2, e0)/tnorm

        # Track minimum jacobian
        if normjac < jac:
            jac = normjac

    return jac


cdef inline float hex_lin_qual_float(int64_t [::1] cells, int c,
                                      float [:, ::1] pts) nogil:
    """ Returns minimum scaled jacobian of a hexahedrals cell's edge nodes  """
    cdef int indS, ind0, ind1, ind2    
        
    cdef float [3] e0
    cdef float [3] e1
    cdef float [3] e2

    cdef int i, j
    cdef float normjac, tnorm
    cdef float jac = 1.1
    
    for i in range(8):
        indS = cells[c + i]
        ind0 = cells[c + hex_edges[i][0]]
        ind1 = cells[c + hex_edges[i][1]]
        ind2 = cells[c + hex_edges[i][2]]
        
        for j in range(3):
            e0[j] = pts[ind0, j] - pts[indS, j]
            e1[j] = pts[ind1, j] - pts[indS, j]
            e2[j] = pts[ind2, j] - pts[indS, j]

        # normalize the determinant of the jacobian
        tnorm = vector_norm_float(e0)*vector_norm_float(e1)*vector_norm_float(e2)
        normjac = triple_product_float(e1, e2, e0)/tnorm

        # Track minimum jacobian
        if normjac < jac:
            jac = normjac

    return jac


#==============================================================================
# Quadradic shape Checking functions
#==============================================================================
cdef inline double tet_quad_qual(int64_t [::1] cells, int c,
                              double [:, ::1] pts) nogil:
    """
    Shape function checking code generated by the following comments.  Shape
    functions generated from "scratch"

    import numpy as np
    import sympy
    
    isopts = np.array([[1, 0, 0, 0], # edge node 0
              [0, 1, 0, 0], # edge node 1
              [0, 0, 1, 0], # edge node 2
              [0, 0, 0, 1], # edge node 3
              [0.5, 0.5, 0, 0], # midside node 4 (between 0 and 1)
              [0, 0.5, 0.5, 0], # midside node 5 (between 1 and 2)
              [0.5, 0, 0.5, 0], # midside node 6 (between 0 and 2)
              [0.5, 0, 0, 0.5], # midside node 7 (between 0 and 3)
              [0, 0.5, 0, 0.5], # midside node 8 (between 1 and 3)
              [0, 0, 0.5, 0.5]]) # midside node 9 (between 2 and 3)
    
    zeta0, zeta1, zeta2, zeta3 = sympy.symbols('zeta0, zeta1, zeta2, zeta3')
    
    shape_functions = [zeta0*(2*zeta0 - 1), # edge node 0
                       zeta1*(2*zeta1 - 1), # edge node 1
                       zeta2*(2*zeta2 - 1), # edge node 2
                       zeta3*(2*zeta3 - 1), # edge node 3
                       4*zeta0*zeta1,       # midside node 4
                       4*zeta1*zeta2,       # midside node 5
                       4*zeta2*zeta0,       # midside node 6
                       4*zeta0*zeta3,       # midside node 7
                       4*zeta1*zeta3,       # midside node 8
                       4*zeta2*zeta3]       # midside node 9
    
    # Take the differental of each shape function evaluated at the intergration
    # point with respect to the natural shape coordinate system
    variables = [zeta0, zeta1, zeta2, zeta3]
    nfun = len(shape_functions)
    nvar = len(variables)
    nprime = np.empty((nvar, nfun), np.object)
    for i in range(nfun):
        for j in range(nvar):
             nprime[j, i] = sympy.diff(shape_functions[i], variables[j])
    
    
    # This is the N_prime functions with the isopts subbed into them
    pre_j = np.empty((nfun*nvar, nfun))
    for i in range(nfun):
        for j in range(nvar):
            for k in range(nfun):
                pre_j[i*nvar + j, k] = nprime[j, k].subs([(zeta0, isopts[i, 0]),
                                                          (zeta1, isopts[i, 1]),
                                                          (zeta2, isopts[i, 2]),
                                                          (zeta3, isopts[i, 3])])
    
    subtract first row to get square system for each jacobian
    
    for example, for edge node 0 the pre_j is:
    N 0  1  2  3  4  5  6  7  8  9
    [ 3  0  0  0  0  0  0  0  0  0] # N/dzeta0
    [ 0 -1  0  0  4  0  0  0  0  0] # N/dzeta1
    [ 0  0 -1  0  0  0  4  0  0  0] # N/dzeta2
    [ 0  0  0 -1  0  0  0  4  0  0] # N/dzeta3
    
    # vectors to form jacobian are
    e0 = 4*Node4 - Node1 - 3*Node0
    e1 = 4*Node6 - Node2 - 3*Node0
    e2 = 4*Node7 - Node3 - 3*Node0
    
    
    
    # example imperfect tetrahedral
    pts = np.array([[ 8.54211689,  0.3652738 ,  3.41738048],
                    [ 8.47148386,  0.36139067,  3.43469913],
                    [ 8.50658017,  0.39327835,  3.43790835],
                    [ 8.48195083,  0.41016419,  3.35366513],
                    [ 8.50680038,  0.36333224,  3.42603981],
                    [ 8.48903202,  0.37733451,  3.43630374],
                    [ 8.52434853,  0.37927608,  3.42764442],
                    [ 8.51203386,  0.38771899,  3.3855228 ],
                    [ 8.47671735,  0.38577743,  3.39418213],
                    [ 8.4942655 ,  0.40172127,  3.39578674]])    
    
    # Programmatically this was difficult as the first column always had to be
    # subtracted and it made it difficult to program in consistent edge indices.
    # Found it best just to print out the indices
    e0 = np.empty(3)
    e1 = np.empty(3)
    e2 = np.empty(3)
    
    ind0 = 0
    ind1 = 1
    ind2 = 2
    ind3 = 3
    ind4 = 4
    ind5 = 5
    ind6 = 6
    ind7 = 7
    ind8 = 8
    ind9 = 9
    
    #==============================================================================
    # FOLLOWING CODE PRINTED
    #==============================================================================
    for j in range(10):
        print '# Node {:d}'.format(j)
        print 'for j in range(3):'
        endtxt = ''
        k = pre_j[4*j].astype(np.int)
        for i in np.nonzero(k)[0].tolist():
            if k[i] == -1:
                endtxt += ' + pts[ind{:d}, j]'.format(i)
            elif k[i] == 1:
                endtxt += ' - pts[ind{:d}, j]'.format(i)
            elif k[i] < 0:
                endtxt += ' + {:d}*pts[ind{:d}, j]'.format(k[i], i)
            elif k[i] > 0:
                endtxt += ' - {:d}*pts[ind{:d}, j]'.format(k[i], i)
        
        
        for m in range(1, 4):
            txt = 'e{:d}[j] ='.format(m - 1)
            k = pre_j[4*j + m].astype(np.int)
            for i in np.nonzero(k)[0].tolist():
                if k[i] == 1:
                    txt += ' + pts[ind{:d}, j]'.format(i)
                elif k[i] == -1:
                    txt += ' - pts[ind{:d}, j]'.format(i)
                elif k[i] > 0:
                    txt += ' + {:d}*pts[ind{:d}, j]'.format(k[i], i)
                elif k[i] < 0:
                    txt += ' - {:d}*pts[ind{:d}, j]'.format(k[i], i)
            print '    ' + txt + endtxt
        print 

    """
    
    cdef double [3] e0
    cdef double [3] e1
    cdef double [3] e2

    cdef int j
    cdef double normjac, tnorm
    
    cdef int ind0 = cells[c + 0]
    cdef int ind1 = cells[c + 1]
    cdef int ind2 = cells[c + 2]
    cdef int ind3 = cells[c + 3]
    cdef int ind4 = cells[c + 4]
    cdef int ind5 = cells[c + 5]
    cdef int ind6 = cells[c + 6]
    cdef int ind7 = cells[c + 7]
    cdef int ind8 = cells[c + 8]
    cdef int ind9 = cells[c + 9]

    ######################### Edge node 0 #########################
    for j in range(3):
        e0[j] = 4*pts[ind4, j] - pts[ind1, j] - 3*pts[ind0, j]
        e1[j] = 4*pts[ind6, j] - pts[ind2, j] - 3*pts[ind0, j]
        e2[j] = 4*pts[ind7, j] - pts[ind3, j] - 3*pts[ind0, j]

    # normalize the determinant of the jacobian
    tnorm = (vector_norm(e0)*vector_norm(e1)*vector_norm(e2))            

    # Store this as minimum jacobian so far
    cdef double jac = triple_product(e1, e2, e0)/tnorm

    ######################### Edge node 1 #########################
    for j in range(3):
        e0[j] = 3*pts[ind1, j] - 4*pts[ind4, j] + pts[ind0, j]
        e1[j] = 4*pts[ind5, j] - pts[ind2, j] - 4*pts[ind4, j] + pts[ind0, j]
        e2[j] = 4*pts[ind8, j] - pts[ind3, j] - 4*pts[ind4, j] + pts[ind0, j]

    # normalize the determinant of the jacobian
    tnorm = (vector_norm(e0)*vector_norm(e1)*vector_norm(e2))            
    normjac = triple_product(e1, e2, e0)/tnorm

    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
              
    ######################### Edge node 2 #########################
    for j in range(3):
        e0[j] = 4*pts[ind5, j] - pts[ind1, j] - 4*pts[ind6, j] + pts[ind0, j]
        e1[j] = 3*pts[ind2, j]                - 4*pts[ind6, j] + pts[ind0, j]
        e2[j] = 4*pts[ind9, j] - pts[ind3, j] - 4*pts[ind6, j] + pts[ind0, j]
        
    # normalize the determinant of the jacobian
    tnorm = (vector_norm(e0)*vector_norm(e1)*vector_norm(e2))            
    normjac = triple_product(e1, e2, e0)/tnorm

    # Track minimum jacobian
    if normjac < jac:
        jac = normjac

    ######################### edge node 3 #########################
    for j in range(3):
        e0[j] = 4*pts[ind8, j] - pts[ind1, j] - 4*pts[ind7, j] + pts[ind0, j]
        e1[j] = 4*pts[ind9, j] - pts[ind2, j] - 4*pts[ind7, j] + pts[ind0, j]
        e2[j] = 3*pts[ind3, j] - 4*pts[ind7, j] + pts[ind0, j]
        
    # normalize the determinant of the jacobian
    tnorm = (vector_norm(e0)*vector_norm(e1)*vector_norm(e2))            
    normjac = triple_product(e1, e2, e0)/tnorm

    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
               
    ######################### Midside node 4 #########################
    for j in range(3):
        e0[j] = + pts[ind1, j] + 2*pts[ind4, j] - pts[ind0, j] - 2*pts[ind4, j]
        e1[j] = - pts[ind2, j] + 2*pts[ind5, j] + 2*pts[ind6, j] - pts[ind0, j] - 2*pts[ind4, j]
        e2[j] = - pts[ind3, j] + 2*pts[ind7, j] + 2*pts[ind8, j] - pts[ind0, j] - 2*pts[ind4, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm(e0)*vector_norm(e1)*vector_norm(e2))            
    normjac = triple_product(e1, e2, e0)/tnorm

    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    ######################### Midside node 5 #########################
    for j in range(3):
        e0[j] = + pts[ind1, j] + 2*pts[ind5, j] + pts[ind0, j] - 2*pts[ind4, j] - 2*pts[ind6, j]
        e1[j] = + pts[ind2, j] + 2*pts[ind5, j] + pts[ind0, j] - 2*pts[ind4, j] - 2*pts[ind6, j]
        e2[j] = - pts[ind3, j] + 2*pts[ind8, j] + 2*pts[ind9, j] + pts[ind0, j] - 2*pts[ind4, j] - 2*pts[ind6, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm(e0)*vector_norm(e1)*vector_norm(e2))            
    normjac = triple_product(e1, e2, e0)/tnorm

    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
               
    ######################### Midside node 6 #########################
    for j in range(3):
        e0[j] = - pts[ind1, j] + 2*pts[ind4, j] + 2*pts[ind5, j] - pts[ind0, j] - 2*pts[ind6, j]
        e1[j] = + pts[ind2, j] + 2*pts[ind6, j] - pts[ind0, j] - 2*pts[ind6, j]
        e2[j] = - pts[ind3, j] + 2*pts[ind7, j] + 2*pts[ind9, j] - pts[ind0, j] - 2*pts[ind6, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm(e0)*vector_norm(e1)*vector_norm(e2))            
    normjac = triple_product(e1, e2, e0)/tnorm

    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
               
    ######################### Midside node 7 #########################
    for j in range(3):
        e0[j] = - pts[ind1, j] + 2*pts[ind4, j] + 2*pts[ind8, j] - pts[ind0, j] - 2*pts[ind7, j]
        e1[j] = - pts[ind2, j] + 2*pts[ind6, j] + 2*pts[ind9, j] - pts[ind0, j] - 2*pts[ind7, j]
        e2[j] = + pts[ind3, j] + 2*pts[ind7, j] - pts[ind0, j] - 2*pts[ind7, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm(e0)*vector_norm(e1)*vector_norm(e2))            
    normjac = triple_product(e1, e2, e0)/tnorm

    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
               
    ######################### Midside node 8 #########################
    for j in range(3):
        e0[j] = + pts[ind1, j] + 2*pts[ind8, j] + pts[ind0, j] - 2*pts[ind4, j] - 2*pts[ind7, j]
        e1[j] = - pts[ind2, j] + 2*pts[ind5, j] + 2*pts[ind9, j] + pts[ind0, j] - 2*pts[ind4, j] - 2*pts[ind7, j]
        e2[j] = + pts[ind3, j] + 2*pts[ind8, j] + pts[ind0, j] - 2*pts[ind4, j] - 2*pts[ind7, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm(e0)*vector_norm(e1)*vector_norm(e2))            
    normjac = triple_product(e1, e2, e0)/tnorm

    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
               
    ######################### Midside node 9 #########################
    for j in range(3):
        e0[j] = - pts[ind1, j] + 2*pts[ind5, j] + 2*pts[ind8, j] + pts[ind0, j] - 2*pts[ind6, j] - 2*pts[ind7, j]
        e1[j] = + pts[ind2, j] + 2*pts[ind9, j] + pts[ind0, j] - 2*pts[ind6, j] - 2*pts[ind7, j]
        e2[j] = + pts[ind3, j] + 2*pts[ind9, j] + pts[ind0, j] - 2*pts[ind6, j] - 2*pts[ind7, j]

    # normalize the determinant of the jacobian
    tnorm = (vector_norm(e0)*vector_norm(e1)*vector_norm(e2))            
    normjac = triple_product(e1, e2, e0)/tnorm

    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # adjust jacobian
    # return jac*1.414213562373095
    return jac


cdef inline float tet_quad_qual_float(int64_t [::1] cells, int c,
                                       float [:, ::1] pts) nogil:
    cdef float [3] e0
    cdef float [3] e1
    cdef float [3] e2

    cdef int j
    cdef float normjac, tnorm
    
    cdef int ind0 = cells[c + 0]
    cdef int ind1 = cells[c + 1]
    cdef int ind2 = cells[c + 2]
    cdef int ind3 = cells[c + 3]
    cdef int ind4 = cells[c + 4]
    cdef int ind5 = cells[c + 5]
    cdef int ind6 = cells[c + 6]
    cdef int ind7 = cells[c + 7]
    cdef int ind8 = cells[c + 8]
    cdef int ind9 = cells[c + 9]

    ######################### Edge node 0 #########################
    for j in range(3):
        e0[j] = 4*pts[ind4, j] - pts[ind1, j] - 3*pts[ind0, j]
        e1[j] = 4*pts[ind6, j] - pts[ind2, j] - 3*pts[ind0, j]
        e2[j] = 4*pts[ind7, j] - pts[ind3, j] - 3*pts[ind0, j]

    # normalize the determinant of the jacobian
    tnorm = (vector_norm_float(e0)*vector_norm_float(e1)*vector_norm_float(e2))            

    # Store this as minimum jacobian so far
    cdef float jac = triple_product_float(e1, e2, e0)/tnorm

    ######################### Edge node 1 #########################
    for j in range(3):
        e0[j] = 3*pts[ind1, j] - 4*pts[ind4, j] + pts[ind0, j]
        e1[j] = 4*pts[ind5, j] - pts[ind2, j] - 4*pts[ind4, j] + pts[ind0, j]
        e2[j] = 4*pts[ind8, j] - pts[ind3, j] - 4*pts[ind4, j] + pts[ind0, j]

    # normalize the determinant of the jacobian
    tnorm = (vector_norm_float(e0)*vector_norm_float(e1)*vector_norm_float(e2))            
    normjac = triple_product_float(e1, e2, e0)/tnorm

    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
              
    ######################### Edge node 2 #########################
    for j in range(3):
        e0[j] = 4*pts[ind5, j] - pts[ind1, j] - 4*pts[ind6, j] + pts[ind0, j]
        e1[j] = 3*pts[ind2, j]                - 4*pts[ind6, j] + pts[ind0, j]
        e2[j] = 4*pts[ind9, j] - pts[ind3, j] - 4*pts[ind6, j] + pts[ind0, j]
        
    # normalize the determinant of the jacobian
    tnorm = (vector_norm_float(e0)*vector_norm_float(e1)*vector_norm_float(e2))            
    normjac = triple_product_float(e1, e2, e0)/tnorm

    # Track minimum jacobian
    if normjac < jac:
        jac = normjac

    ######################### edge node 3 #########################
    for j in range(3):
        e0[j] = 4*pts[ind8, j] - pts[ind1, j] - 4*pts[ind7, j] + pts[ind0, j]
        e1[j] = 4*pts[ind9, j] - pts[ind2, j] - 4*pts[ind7, j] + pts[ind0, j]
        e2[j] = 3*pts[ind3, j] - 4*pts[ind7, j] + pts[ind0, j]
        
    # normalize the determinant of the jacobian
    tnorm = (vector_norm_float(e0)*vector_norm_float(e1)*vector_norm_float(e2))            
    normjac = triple_product_float(e1, e2, e0)/tnorm

    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
               
    ######################### Midside node 4 #########################
    for j in range(3):
        e0[j] = + pts[ind1, j] + 2*pts[ind4, j] - pts[ind0, j] - 2*pts[ind4, j]
        e1[j] = - pts[ind2, j] + 2*pts[ind5, j] + 2*pts[ind6, j] - pts[ind0, j] - 2*pts[ind4, j]
        e2[j] = - pts[ind3, j] + 2*pts[ind7, j] + 2*pts[ind8, j] - pts[ind0, j] - 2*pts[ind4, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm_float(e0)*vector_norm_float(e1)*vector_norm_float(e2))            
    normjac = triple_product_float(e1, e2, e0)/tnorm

    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    ######################### Midside node 5 #########################
    for j in range(3):
        e0[j] = + pts[ind1, j] + 2*pts[ind5, j] + pts[ind0, j] - 2*pts[ind4, j] - 2*pts[ind6, j]
        e1[j] = + pts[ind2, j] + 2*pts[ind5, j] + pts[ind0, j] - 2*pts[ind4, j] - 2*pts[ind6, j]
        e2[j] = - pts[ind3, j] + 2*pts[ind8, j] + 2*pts[ind9, j] + pts[ind0, j] - 2*pts[ind4, j] - 2*pts[ind6, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm_float(e0)*vector_norm_float(e1)*vector_norm_float(e2))            
    normjac = triple_product_float(e1, e2, e0)/tnorm

    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
               
    ######################### Midside node 6 #########################
    for j in range(3):
        e0[j] = - pts[ind1, j] + 2*pts[ind4, j] + 2*pts[ind5, j] - pts[ind0, j] - 2*pts[ind6, j]
        e1[j] = + pts[ind2, j] + 2*pts[ind6, j] - pts[ind0, j] - 2*pts[ind6, j]
        e2[j] = - pts[ind3, j] + 2*pts[ind7, j] + 2*pts[ind9, j] - pts[ind0, j] - 2*pts[ind6, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm_float(e0)*vector_norm_float(e1)*vector_norm_float(e2))            
    normjac = triple_product_float(e1, e2, e0)/tnorm

    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
               
    ######################### Midside node 7 #########################
    for j in range(3):
        e0[j] = - pts[ind1, j] + 2*pts[ind4, j] + 2*pts[ind8, j] - pts[ind0, j] - 2*pts[ind7, j]
        e1[j] = - pts[ind2, j] + 2*pts[ind6, j] + 2*pts[ind9, j] - pts[ind0, j] - 2*pts[ind7, j]
        e2[j] = + pts[ind3, j] + 2*pts[ind7, j] - pts[ind0, j] - 2*pts[ind7, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm_float(e0)*vector_norm_float(e1)*vector_norm_float(e2))            
    normjac = triple_product_float(e1, e2, e0)/tnorm

    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
               
    ######################### Midside node 8 #########################
    for j in range(3):
        e0[j] = + pts[ind1, j] + 2*pts[ind8, j] + pts[ind0, j] - 2*pts[ind4, j] - 2*pts[ind7, j]
        e1[j] = - pts[ind2, j] + 2*pts[ind5, j] + 2*pts[ind9, j] + pts[ind0, j] - 2*pts[ind4, j] - 2*pts[ind7, j]
        e2[j] = + pts[ind3, j] + 2*pts[ind8, j] + pts[ind0, j] - 2*pts[ind4, j] - 2*pts[ind7, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm_float(e0)*vector_norm_float(e1)*vector_norm_float(e2))            
    normjac = triple_product_float(e1, e2, e0)/tnorm

    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
               
    ######################### Midside node 9 #########################
    for j in range(3):
        e0[j] = - pts[ind1, j] + 2*pts[ind5, j] + 2*pts[ind8, j] + pts[ind0, j] - 2*pts[ind6, j] - 2*pts[ind7, j]
        e1[j] = + pts[ind2, j] + 2*pts[ind9, j] + pts[ind0, j] - 2*pts[ind6, j] - 2*pts[ind7, j]
        e2[j] = + pts[ind3, j] + 2*pts[ind9, j] + pts[ind0, j] - 2*pts[ind6, j] - 2*pts[ind7, j]

    # normalize the determinant of the jacobian
    tnorm = (vector_norm_float(e0)*vector_norm_float(e1)*vector_norm_float(e2))            
    normjac = triple_product_float(e1, e2, e0)/tnorm

    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # adjust jacobian
    return jac*1.414213562373095


cdef inline double pyr_quad_qual(int64_t [::1] cells, int c,
                                 double [:, ::1] pts) nogil:
    """
    Shape function checking code generated by printing the following code using
    the quadradic hexahedral indices in hex_quad_qual and replacing them with:
    
    # Map wedge indices to hexahedral indices
    # ANSYS   [I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z, A, B]
    pyr_map = [0, 1, 2, 3, 4, 4, 4, 4, 5, 6, 7, 8, 4, 4, 4, 4, 9,10,11,12]
    for i in range(len(pyr_map)):
        hex_quad_edges[hex_quad_edges == i] = pyr_map[i]
    
    for i in range(4):
        print '# Node {:d}'.format(i)
        print 'for j in range(3):'
        print '    e0[j]  = 4*pts[ind{:d}, j] - pts[ind{:d}, j] - 3*pts[ind{:d}, j]'.format(hex_quad_edges[i][1][0], hex_quad_edges[i][0][0], i)
        print '    e1[j]  = 4*pts[ind{:d}, j] - pts[ind{:d}, j] - 3*pts[ind{:d}, j]'.format(hex_quad_edges[i][1][1], hex_quad_edges[i][0][1], i)
        print '    e2[j]  = 4*pts[ind{:d}, j] - pts[ind{:d}, j] - 3*pts[ind{:d}, j]'.format(hex_quad_edges[i][1][2], hex_quad_edges[i][0][2], i)
        print 
        print '# normalize the determinant of the jacobian'
        print 'tnorm = (vector_norm(e0)*vector_norm(e1)*vector_norm(e2))' 
        print 'normjac = triple_product(e1, e2, e0)/tnorm'
        print 
        print '# Track minimum jacobian'
        print 'if normjac < jac:'
        print '    jac = normjac'
        print 
        print 'print normjac'
        
    
    # midside nodes along x moving edges
    for i in [8, 9, 10, 11, 16, 17, 18, 19]:
        print '# Node {:d}'.format(i)
        print 'for j in range(3):'
        print '    e0[j] = pts[ind{:d}, j] - pts[ind{:d}, j]'.format(hex_quad_edges[i][0][0], hex_quad_edges[i][0][1])
        print
        
        print '    e1[j] = 2*pts[ind{:d}, j] + \\'.format(hex_quad_edges[i][1][0])
        print '         2*pts[ind{:d}, j] - \\'.format(hex_quad_edges[i][1][1])
        print '           pts[ind{:d}, j] - \\'.format(hex_quad_edges[i][1][2])
        print '           pts[ind{:d}, j] - \\'.format(hex_quad_edges[i][1][3])
        print '           pts[ind{:d}, j] - \\'.format(hex_quad_edges[i][1][4])
        print '           pts[ind{:d}, j] - \\'.format(hex_quad_edges[i][1][5])
        print '           pts[ind{:d}, j] + \\'.format(hex_quad_edges[i][1][6])
        print '           pts[ind{:d}, j]'.format(hex_quad_edges[i][1][7])
        print
        print '    e2[j] = 2*pts[ind{:d}, j] + \\'.format(hex_quad_edges[i][2][0])
        print '         2*pts[ind{:d}, j] - \\'.format(hex_quad_edges[i][2][1])
        print '           pts[ind{:d}, j] - \\'.format(hex_quad_edges[i][2][2])
        print '           pts[ind{:d}, j] - \\'.format(hex_quad_edges[i][2][3])
        print '           pts[ind{:d}, j] - \\'.format(hex_quad_edges[i][2][4])
        print '           pts[ind{:d}, j] - \\'.format(hex_quad_edges[i][2][5])
        print '           pts[ind{:d}, j] + \\'.format(hex_quad_edges[i][2][6])
        print '           pts[ind{:d}, j]'.format(hex_quad_edges[i][2][7])
        print 
        print '# normalize the determinant of the jacobian'
        print 'tnorm = (vector_norm(e0)*vector_norm(e1)*vector_norm(e2))' 
        print 'normjac = triple_product(e1, e2, e0)/tnorm'
        print 
        print '# Track minimum jacobian'
        print 'if normjac < jac:'
        print '    jac = normjac'
        print 
        print 'print normjac'    
    
    
    """

    cdef double [3] e0
    cdef double [3] e1
    cdef double [3] e2

    cdef int i, j    
    cdef double normjac, tnorm

    cdef int ind0 = cells[c + 0]
    cdef int ind1 = cells[c + 1]
    cdef int ind2 = cells[c + 2]
    cdef int ind3 = cells[c + 3]
    cdef int ind4 = cells[c + 4]
    cdef int ind5 = cells[c + 5]
    cdef int ind6 = cells[c + 6]
    cdef int ind7 = cells[c + 7]
    cdef int ind8 = cells[c + 8]
    cdef int ind9 = cells[c + 9]
    cdef int ind10 = cells[c + 10]
    cdef int ind11 = cells[c + 11]
    cdef int ind12 = cells[c + 12]
    
    # Node 0
    for j in range(3):
        e0[j]  = 4*pts[ind5, j] - pts[ind1, j] - 3*pts[ind0, j]
        e1[j]  = 4*pts[ind8, j] - pts[ind3, j] - 3*pts[ind0, j]
        e2[j]  = 4*pts[ind9, j] - pts[ind4, j] - 3*pts[ind0, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm(e0)*vector_norm(e1)*vector_norm(e2))
    cdef double jac = triple_product(e1, e2, e0)/tnorm
    
    
    # Node 1
    for j in range(3):
        e0[j]  = 4*pts[ind6, j] - pts[ind2, j] - 3*pts[ind1, j]
        e1[j]  = 4*pts[ind5, j] - pts[ind0, j] - 3*pts[ind1, j]
        e2[j]  = 4*pts[ind10, j] - pts[ind4, j] - 3*pts[ind1, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm(e0)*vector_norm(e1)*vector_norm(e2))
    normjac = triple_product(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 2
    for j in range(3):
        e0[j]  = 4*pts[ind7, j] - pts[ind3, j] - 3*pts[ind2, j]
        e1[j]  = 4*pts[ind6, j] - pts[ind1, j] - 3*pts[ind2, j]
        e2[j]  = 4*pts[ind11, j] - pts[ind4, j] - 3*pts[ind2, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm(e0)*vector_norm(e1)*vector_norm(e2))
    normjac = triple_product(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 3
    for j in range(3):
        e0[j]  = 4*pts[ind8, j] - pts[ind0, j] - 3*pts[ind3, j]
        e1[j]  = 4*pts[ind7, j] - pts[ind2, j] - 3*pts[ind3, j]
        e2[j]  = 4*pts[ind12, j] - pts[ind4, j] - 3*pts[ind3, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm(e0)*vector_norm(e1)*vector_norm(e2))
    normjac = triple_product(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 8
    for j in range(3):
        e0[j] = pts[ind1, j] - pts[ind0, j]
    
        e1[j] = 2*pts[ind6, j] + \
             2*pts[ind8, j] - \
               pts[ind0, j] - \
               pts[ind1, j] - \
               pts[ind2, j] - \
               pts[ind3, j] - \
               pts[ind5, j] + \
               pts[ind7, j]
    
        e2[j] = 2*pts[ind9, j] + \
             2*pts[ind10, j] - \
               pts[ind0, j] - \
               pts[ind1, j] - \
               pts[ind4, j] - \
               pts[ind4, j] - \
               pts[ind5, j] + \
               pts[ind4, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm(e0)*vector_norm(e1)*vector_norm(e2))
    normjac = triple_product(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 9
    for j in range(3):
        e0[j] = pts[ind2, j] - pts[ind1, j]
    
        e1[j] = 2*pts[ind5, j] + \
             2*pts[ind7, j] - \
               pts[ind0, j] - \
               pts[ind1, j] - \
               pts[ind2, j] - \
               pts[ind3, j] - \
               pts[ind6, j] + \
               pts[ind8, j]
    
        e2[j] = 2*pts[ind10, j] + \
             2*pts[ind11, j] - \
               pts[ind1, j] - \
               pts[ind2, j] - \
               pts[ind4, j] - \
               pts[ind4, j] - \
               pts[ind6, j] + \
               pts[ind4, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm(e0)*vector_norm(e1)*vector_norm(e2))
    normjac = triple_product(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 10
    for j in range(3):
        e0[j] = pts[ind3, j] - pts[ind2, j]
    
        e1[j] = 2*pts[ind6, j] + \
             2*pts[ind8, j] - \
               pts[ind0, j] - \
               pts[ind1, j] - \
               pts[ind2, j] - \
               pts[ind3, j] - \
               pts[ind7, j] + \
               pts[ind5, j]
    
        e2[j] = 2*pts[ind11, j] + \
             2*pts[ind12, j] - \
               pts[ind2, j] - \
               pts[ind3, j] - \
               pts[ind4, j] - \
               pts[ind4, j] - \
               pts[ind7, j] + \
               pts[ind4, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm(e0)*vector_norm(e1)*vector_norm(e2))
    normjac = triple_product(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 11
    for j in range(3):
        e0[j] = pts[ind3, j] - pts[ind0, j]
    
        e1[j] = 2*pts[ind9, j] + \
             2*pts[ind12, j] - \
               pts[ind0, j] - \
               pts[ind3, j] - \
               pts[ind4, j] - \
               pts[ind4, j] - \
               pts[ind8, j] + \
               pts[ind4, j]
    
        e2[j] = 2*pts[ind5, j] + \
             2*pts[ind7, j] - \
               pts[ind0, j] - \
               pts[ind1, j] - \
               pts[ind2, j] - \
               pts[ind3, j] - \
               pts[ind8, j] + \
               pts[ind6, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm(e0)*vector_norm(e1)*vector_norm(e2))
    normjac = triple_product(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 16
    for j in range(3):
        e0[j] = pts[ind0, j] - pts[ind4, j]
    
        e1[j] = 2*pts[ind8, j] + \
             2*pts[ind4, j] - \
               pts[ind0, j] - \
               pts[ind3, j] - \
               pts[ind4, j] - \
               pts[ind4, j] - \
               pts[ind9, j] + \
               pts[ind12, j]
    
        e2[j] = 2*pts[ind5, j] + \
             2*pts[ind4, j] - \
               pts[ind0, j] - \
               pts[ind1, j] - \
               pts[ind4, j] - \
               pts[ind4, j] - \
               pts[ind9, j] + \
               pts[ind10, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm(e0)*vector_norm(e1)*vector_norm(e2))
    normjac = triple_product(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    
    # Node 17
    for j in range(3):
        e0[j] = pts[ind1, j] - pts[ind4, j]
    
        e1[j] = 2*pts[ind5, j] + \
             2*pts[ind4, j] - \
               pts[ind0, j] - \
               pts[ind1, j] - \
               pts[ind4, j] - \
               pts[ind4, j] - \
               pts[ind10, j] + \
               pts[ind9, j]
    
        e2[j] = 2*pts[ind6, j] + \
             2*pts[ind4, j] - \
               pts[ind1, j] - \
               pts[ind2, j] - \
               pts[ind4, j] - \
               pts[ind4, j] - \
               pts[ind10, j] + \
               pts[ind11, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm(e0)*vector_norm(e1)*vector_norm(e2))
    normjac = triple_product(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    
    # Node 18
    for j in range(3):
        e0[j] = pts[ind2, j] - pts[ind4, j]
    
        e1[j] = 2*pts[ind6, j] + \
             2*pts[ind4, j] - \
               pts[ind1, j] - \
               pts[ind2, j] - \
               pts[ind4, j] - \
               pts[ind4, j] - \
               pts[ind11, j] + \
               pts[ind10, j]
    
        e2[j] = 2*pts[ind7, j] + \
             2*pts[ind4, j] - \
               pts[ind2, j] - \
               pts[ind3, j] - \
               pts[ind4, j] - \
               pts[ind4, j] - \
               pts[ind11, j] + \
               pts[ind12, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm(e0)*vector_norm(e1)*vector_norm(e2))
    normjac = triple_product(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 19
    for j in range(3):
        e0[j] = pts[ind3, j] - pts[ind4, j]
    
        e1[j] = 2*pts[ind7, j] + \
             2*pts[ind4, j] - \
               pts[ind2, j] - \
               pts[ind3, j] - \
               pts[ind4, j] - \
               pts[ind4, j] - \
               pts[ind12, j] + \
               pts[ind11, j]
    
        e2[j] = 2*pts[ind8, j] + \
             2*pts[ind4, j] - \
               pts[ind0, j] - \
               pts[ind3, j] - \
               pts[ind4, j] - \
               pts[ind4, j] - \
               pts[ind12, j] + \
               pts[ind9, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm(e0)*vector_norm(e1)*vector_norm(e2))
    normjac = triple_product(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac

    return jac*1.14


cdef inline float pyr_quad_qual_float(int64_t [::1] cells, int c,
                                      float [:, ::1] pts) nogil:
    cdef float [3] e0
    cdef float [3] e1
    cdef float [3] e2

    cdef int i, j    
    cdef float normjac, tnorm

    cdef int ind0 = cells[c + 0]
    cdef int ind1 = cells[c + 1]
    cdef int ind2 = cells[c + 2]
    cdef int ind3 = cells[c + 3]
    cdef int ind4 = cells[c + 4]
    cdef int ind5 = cells[c + 5]
    cdef int ind6 = cells[c + 6]
    cdef int ind7 = cells[c + 7]
    cdef int ind8 = cells[c + 8]
    cdef int ind9 = cells[c + 9]
    cdef int ind10 = cells[c + 10]
    cdef int ind11 = cells[c + 11]
    cdef int ind12 = cells[c + 12]
    
    # Node 0
    for j in range(3):
        e0[j]  = 4*pts[ind5, j] - pts[ind1, j] - 3*pts[ind0, j]
        e1[j]  = 4*pts[ind8, j] - pts[ind3, j] - 3*pts[ind0, j]
        e2[j]  = 4*pts[ind9, j] - pts[ind4, j] - 3*pts[ind0, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm_float(e0)*vector_norm_float(e1)*vector_norm_float(e2))
    cdef float jac = triple_product_float(e1, e2, e0)/tnorm
    
    
    # Node 1
    for j in range(3):
        e0[j]  = 4*pts[ind6, j] - pts[ind2, j] - 3*pts[ind1, j]
        e1[j]  = 4*pts[ind5, j] - pts[ind0, j] - 3*pts[ind1, j]
        e2[j]  = 4*pts[ind10, j] - pts[ind4, j] - 3*pts[ind1, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm_float(e0)*vector_norm_float(e1)*vector_norm_float(e2))
    normjac = triple_product_float(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 2
    for j in range(3):
        e0[j]  = 4*pts[ind7, j] - pts[ind3, j] - 3*pts[ind2, j]
        e1[j]  = 4*pts[ind6, j] - pts[ind1, j] - 3*pts[ind2, j]
        e2[j]  = 4*pts[ind11, j] - pts[ind4, j] - 3*pts[ind2, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm_float(e0)*vector_norm_float(e1)*vector_norm_float(e2))
    normjac = triple_product_float(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 3
    for j in range(3):
        e0[j]  = 4*pts[ind8, j] - pts[ind0, j] - 3*pts[ind3, j]
        e1[j]  = 4*pts[ind7, j] - pts[ind2, j] - 3*pts[ind3, j]
        e2[j]  = 4*pts[ind12, j] - pts[ind4, j] - 3*pts[ind3, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm_float(e0)*vector_norm_float(e1)*vector_norm_float(e2))
    normjac = triple_product_float(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 8
    for j in range(3):
        e0[j] = pts[ind1, j] - pts[ind0, j]
    
        e1[j] = 2*pts[ind6, j] + \
             2*pts[ind8, j] - \
               pts[ind0, j] - \
               pts[ind1, j] - \
               pts[ind2, j] - \
               pts[ind3, j] - \
               pts[ind5, j] + \
               pts[ind7, j]
    
        e2[j] = 2*pts[ind9, j] + \
             2*pts[ind10, j] - \
               pts[ind0, j] - \
               pts[ind1, j] - \
               pts[ind4, j] - \
               pts[ind4, j] - \
               pts[ind5, j] + \
               pts[ind4, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm_float(e0)*vector_norm_float(e1)*vector_norm_float(e2))
    normjac = triple_product_float(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 9
    for j in range(3):
        e0[j] = pts[ind2, j] - pts[ind1, j]
    
        e1[j] = 2*pts[ind5, j] + \
             2*pts[ind7, j] - \
               pts[ind0, j] - \
               pts[ind1, j] - \
               pts[ind2, j] - \
               pts[ind3, j] - \
               pts[ind6, j] + \
               pts[ind8, j]
    
        e2[j] = 2*pts[ind10, j] + \
             2*pts[ind11, j] - \
               pts[ind1, j] - \
               pts[ind2, j] - \
               pts[ind4, j] - \
               pts[ind4, j] - \
               pts[ind6, j] + \
               pts[ind4, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm_float(e0)*vector_norm_float(e1)*vector_norm_float(e2))
    normjac = triple_product_float(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 10
    for j in range(3):
        e0[j] = pts[ind3, j] - pts[ind2, j]
    
        e1[j] = 2*pts[ind6, j] + \
             2*pts[ind8, j] - \
               pts[ind0, j] - \
               pts[ind1, j] - \
               pts[ind2, j] - \
               pts[ind3, j] - \
               pts[ind7, j] + \
               pts[ind5, j]
    
        e2[j] = 2*pts[ind11, j] + \
             2*pts[ind12, j] - \
               pts[ind2, j] - \
               pts[ind3, j] - \
               pts[ind4, j] - \
               pts[ind4, j] - \
               pts[ind7, j] + \
               pts[ind4, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm_float(e0)*vector_norm_float(e1)*vector_norm_float(e2))
    normjac = triple_product_float(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 11
    for j in range(3):
        e0[j] = pts[ind3, j] - pts[ind0, j]
    
        e1[j] = 2*pts[ind9, j] + \
             2*pts[ind12, j] - \
               pts[ind0, j] - \
               pts[ind3, j] - \
               pts[ind4, j] - \
               pts[ind4, j] - \
               pts[ind8, j] + \
               pts[ind4, j]
    
        e2[j] = 2*pts[ind5, j] + \
             2*pts[ind7, j] - \
               pts[ind0, j] - \
               pts[ind1, j] - \
               pts[ind2, j] - \
               pts[ind3, j] - \
               pts[ind8, j] + \
               pts[ind6, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm_float(e0)*vector_norm_float(e1)*vector_norm_float(e2))
    normjac = triple_product_float(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 16
    for j in range(3):
        e0[j] = pts[ind0, j] - pts[ind4, j]
    
        e1[j] = 2*pts[ind8, j] + \
             2*pts[ind4, j] - \
               pts[ind0, j] - \
               pts[ind3, j] - \
               pts[ind4, j] - \
               pts[ind4, j] - \
               pts[ind9, j] + \
               pts[ind12, j]
    
        e2[j] = 2*pts[ind5, j] + \
             2*pts[ind4, j] - \
               pts[ind0, j] - \
               pts[ind1, j] - \
               pts[ind4, j] - \
               pts[ind4, j] - \
               pts[ind9, j] + \
               pts[ind10, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm_float(e0)*vector_norm_float(e1)*vector_norm_float(e2))
    normjac = triple_product_float(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    
    # Node 17
    for j in range(3):
        e0[j] = pts[ind1, j] - pts[ind4, j]
    
        e1[j] = 2*pts[ind5, j] + \
             2*pts[ind4, j] - \
               pts[ind0, j] - \
               pts[ind1, j] - \
               pts[ind4, j] - \
               pts[ind4, j] - \
               pts[ind10, j] + \
               pts[ind9, j]
    
        e2[j] = 2*pts[ind6, j] + \
             2*pts[ind4, j] - \
               pts[ind1, j] - \
               pts[ind2, j] - \
               pts[ind4, j] - \
               pts[ind4, j] - \
               pts[ind10, j] + \
               pts[ind11, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm_float(e0)*vector_norm_float(e1)*vector_norm_float(e2))
    normjac = triple_product_float(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    
    # Node 18
    for j in range(3):
        e0[j] = pts[ind2, j] - pts[ind4, j]
    
        e1[j] = 2*pts[ind6, j] + \
             2*pts[ind4, j] - \
               pts[ind1, j] - \
               pts[ind2, j] - \
               pts[ind4, j] - \
               pts[ind4, j] - \
               pts[ind11, j] + \
               pts[ind10, j]
    
        e2[j] = 2*pts[ind7, j] + \
             2*pts[ind4, j] - \
               pts[ind2, j] - \
               pts[ind3, j] - \
               pts[ind4, j] - \
               pts[ind4, j] - \
               pts[ind11, j] + \
               pts[ind12, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm_float(e0)*vector_norm_float(e1)*vector_norm_float(e2))
    normjac = triple_product_float(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 19
    for j in range(3):
        e0[j] = pts[ind3, j] - pts[ind4, j]
    
        e1[j] = 2*pts[ind7, j] + \
             2*pts[ind4, j] - \
               pts[ind2, j] - \
               pts[ind3, j] - \
               pts[ind4, j] - \
               pts[ind4, j] - \
               pts[ind12, j] + \
               pts[ind11, j]
    
        e2[j] = 2*pts[ind8, j] + \
             2*pts[ind4, j] - \
               pts[ind0, j] - \
               pts[ind3, j] - \
               pts[ind4, j] - \
               pts[ind4, j] - \
               pts[ind12, j] + \
               pts[ind9, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm_float(e0)*vector_norm_float(e1)*vector_norm_float(e2))
    normjac = triple_product_float(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac

    return jac*1.14


cdef inline double weg_quad_qual(int64_t [::1] cells, int c,
                                 double [:, ::1] pts) nogil:
    """
    Compute the cell quality of a single quadratic cell
    """
    cdef double [3] e0
    cdef double [3] e1
    cdef double [3] e2

    cdef int i, j    
    cdef double normjac, tnorm
    
    cdef int ind0 = cells[c + 0]
    cdef int ind1 = cells[c + 1]
    cdef int ind2 = cells[c + 2]
    cdef int ind3 = cells[c + 3]
    cdef int ind4 = cells[c + 4]
    cdef int ind5 = cells[c + 5]
    cdef int ind6 = cells[c + 6]
    cdef int ind7 = cells[c + 7]
    cdef int ind8 = cells[c + 8]
    cdef int ind9 = cells[c + 9]
    cdef int ind10 = cells[c + 10]
    cdef int ind11 = cells[c + 11]
    cdef int ind12 = cells[c + 12]
    cdef int ind13 = cells[c + 13]
    cdef int ind14 = cells[c + 14]
    
    # Node 0
    for j in range(3):
        e0[j] = 4*pts[ind6, j] - pts[ind1, j] - 3*pts[ind0, j]
        e1[j] = 4*pts[ind8, j] - pts[ind2, j] - 3*pts[ind0, j]
        e2[j] = 4*pts[ind12, j] - pts[ind3, j] - 3*pts[ind0, j]
    
    tnorm = (vector_norm(e0)*vector_norm(e1)*vector_norm(e2))   

    # Store current minimum jacobian
    cdef double jac = -triple_product(e1, e2, e0)/tnorm

    # Node 1
    for j in range(3):
        e0[j] = 4*pts[ind7, j] - pts[ind2, j] - 3*pts[ind1, j]
        e1[j] = 4*pts[ind6, j] - pts[ind0, j] - 3*pts[ind1, j]
        e2[j] = 4*pts[ind13, j] - pts[ind4, j] - 3*pts[ind1, j]

    tnorm = (vector_norm(e0)*vector_norm(e1)*vector_norm(e2))   
    normjac = -triple_product(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 2
    # Since node 3 doesn't exist, special treatment for node 2
    for j in range(3):
        e0[j] = 4*pts[ind8, j] - pts[ind0, j] - 3*pts[ind2, j]
        e1[j] = 4*pts[ind7, j] - pts[ind1, j] - 3*pts[ind2, j]
        e2[j] = 4*pts[ind14, j] - pts[ind5, j] - 3*pts[ind2, j]
    
    tnorm = (vector_norm(e0)*vector_norm(e1)*vector_norm(e2))   
    normjac = -triple_product(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    
    # Node 4
    for j in range(3):
        e0[j] = 4*pts[ind11, j] - pts[ind5, j] - 3*pts[ind3, j]
        e1[j] = 4*pts[ind9, j] - pts[ind4, j] - 3*pts[ind3, j]
        e2[j] = 4*pts[ind12, j] - pts[ind0, j] - 3*pts[ind3, j]
    
    tnorm = (vector_norm(e0)*vector_norm(e1)*vector_norm(e2))   
    normjac = -triple_product(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    
    # Node 5
    for j in range(3):
        e0[j] = 4*pts[ind9, j] - pts[ind3, j] - 3*pts[ind4, j]
        e1[j] = 4*pts[ind10, j] - pts[ind5, j] - 3*pts[ind4, j]
        e2[j] = 4*pts[ind13, j] - pts[ind1, j] - 3*pts[ind4, j]
    
    tnorm = (vector_norm(e0)*vector_norm(e1)*vector_norm(e2))   
    normjac = -triple_product(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 6
    # Since node 3 doesn't exist, special treatment for node 2
    for j in range(3):
        e0[j] = 4*pts[ind10, j] - pts[ind4, j] - 3*pts[ind5, j]
        e1[j] = 4*pts[ind11, j] - pts[ind3, j] - 3*pts[ind5, j]
        e2[j] = 4*pts[ind14, j] - pts[ind2, j] - 3*pts[ind5, j]
    
    tnorm = (vector_norm(e0)*vector_norm(e1)*vector_norm(e2))   
    normjac = -triple_product(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 8
    for j in range(3):
        e0[j] = pts[ind1, j] - pts[ind0, j]
    
        e1[j] = 2*pts[ind7, j] + \
                2*pts[ind8, j] - \
                  pts[ind0, j] - \
                  pts[ind1, j] - \
                  pts[ind2, j] - \
                  pts[ind2, j] - \
                  pts[ind6, j] + \
                  pts[ind2, j]
    
        e2[j] = 2*pts[ind12, j] + \
                2*pts[ind13, j] - \
                  pts[ind0, j] - \
                  pts[ind1, j] - \
                  pts[ind3, j] - \
                  pts[ind4, j] - \
                  pts[ind6, j] + \
                  pts[ind9, j]
    
    tnorm = (vector_norm(e0)*vector_norm(e1)*vector_norm(e2))   
    normjac = -triple_product(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 9
    for j in range(3):
        e0[j] = pts[ind2, j] - pts[ind1, j]
    
        e1[j] = 2*pts[ind6, j] + \
                2*pts[ind2, j] - \
                  pts[ind0, j] - \
                  pts[ind1, j] - \
                  pts[ind2, j] - \
                  pts[ind2, j] - \
                  pts[ind7, j] + \
                  pts[ind8, j]
    
        e2[j] = 2*pts[ind13, j] + \
                2*pts[ind14, j] - \
                  pts[ind1, j] - \
                  pts[ind2, j] - \
                  pts[ind4, j] - \
                  pts[ind5, j] - \
                  pts[ind7, j] + \
                  pts[ind10, j]
    
    tnorm = (vector_norm(e0)*vector_norm(e1)*vector_norm(e2))   
    normjac = -triple_product(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 11
    for j in range(3):
        e0[j] = pts[ind2, j] - pts[ind0, j]
    
        e1[j] = 2*pts[ind12, j] + \
                2*pts[ind14, j] - \
                  pts[ind0, j] - \
                  pts[ind2, j] - \
                  pts[ind3, j] - \
                  pts[ind5, j] - \
                  pts[ind8, j] + \
                  pts[ind11, j]
    
        e2[j] = 2*pts[ind6, j] + \
                2*pts[ind2, j] - \
                  pts[ind0, j] - \
                  pts[ind1, j] - \
                  pts[ind2, j] - \
                  pts[ind2, j] - \
                  pts[ind8, j] + \
                  pts[ind7, j]
    
    tnorm = (vector_norm(e0)*vector_norm(e1)*vector_norm(e2))   
    normjac = -triple_product(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 12
    for j in range(3):
        e0[j] = pts[ind3, j] - pts[ind4, j]
    
        e1[j] = 2*pts[ind10, j] + \
                2*pts[ind11, j] - \
                  pts[ind3, j] - \
                  pts[ind4, j] - \
                  pts[ind5, j] - \
                  pts[ind5, j] - \
                  pts[ind9, j] + \
                  pts[ind5, j]
    
        e2[j] = 2*pts[ind12, j] + \
                2*pts[ind13, j] - \
                  pts[ind0, j] - \
                  pts[ind1, j] - \
                  pts[ind3, j] - \
                  pts[ind4, j] - \
                  pts[ind9, j] + \
                  pts[ind6, j]
    
    tnorm = (vector_norm(e0)*vector_norm(e1)*vector_norm(e2))   
    normjac = -triple_product(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 13
    for j in range(3):
        e0[j] = pts[ind4, j] - pts[ind5, j]
    
        e1[j] = 2*pts[ind9, j] + \
                2*pts[ind5, j] - \
                  pts[ind3, j] - \
                  pts[ind4, j] - \
                  pts[ind5, j] - \
                  pts[ind5, j] - \
                  pts[ind10, j] + \
                  pts[ind11, j]
    
        e2[j] = 2*pts[ind13, j] + \
                2*pts[ind14, j] - \
                  pts[ind1, j] - \
                  pts[ind2, j] - \
                  pts[ind4, j] - \
                  pts[ind5, j] - \
                  pts[ind10, j] + \
                  pts[ind7, j]
    
    tnorm = (vector_norm(e0)*vector_norm(e1)*vector_norm(e2))   
    normjac = -triple_product(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 15
    for j in range(3):
        e0[j] = pts[ind5, j] - pts[ind3, j]
    
        e1[j] = 2*pts[ind5, j] + \
                2*pts[ind9, j] - \
                  pts[ind3, j] - \
                  pts[ind4, j] - \
                  pts[ind5, j] - \
                  pts[ind5, j] - \
                  pts[ind11, j] + \
                  pts[ind10, j]
    
        e2[j] = 2*pts[ind12, j] + \
                2*pts[ind14, j] - \
                  pts[ind0, j] - \
                  pts[ind2, j] - \
                  pts[ind3, j] - \
                  pts[ind5, j] - \
                  pts[ind11, j] + \
                  pts[ind8, j]
    
    tnorm = (vector_norm(e0)*vector_norm(e1)*vector_norm(e2))   
    normjac = -triple_product(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 16
    for j in range(3):
        e0[j] = pts[ind0, j] - pts[ind3, j]
    
        e1[j] = 2*pts[ind8, j] + \
                2*pts[ind11, j] - \
                  pts[ind0, j] - \
                  pts[ind2, j] - \
                  pts[ind3, j] - \
                  pts[ind5, j] - \
                  pts[ind12, j] + \
                  pts[ind14, j]
    
        e2[j] = 2*pts[ind6, j] + \
                2*pts[ind9, j] - \
                  pts[ind0, j] - \
                  pts[ind1, j] - \
                  pts[ind3, j] - \
                  pts[ind4, j] - \
                  pts[ind12, j] + \
                  pts[ind13, j]
    
    tnorm = (vector_norm(e0)*vector_norm(e1)*vector_norm(e2))   
    normjac = -triple_product(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 17
    for j in range(3):
        e0[j] = pts[ind1, j] - pts[ind4, j]
    
        e1[j] = 2*pts[ind6, j] + \
                2*pts[ind9, j] - \
                  pts[ind0, j] - \
                  pts[ind1, j] - \
                  pts[ind3, j] - \
                  pts[ind4, j] - \
                  pts[ind13, j] + \
                  pts[ind12, j]
    
        e2[j] = 2*pts[ind7, j] + \
                2*pts[ind10, j] - \
                  pts[ind1, j] - \
                  pts[ind2, j] - \
                  pts[ind4, j] - \
                  pts[ind5, j] - \
                  pts[ind13, j] + \
                  pts[ind14, j]
    
    tnorm = (vector_norm(e0)*vector_norm(e1)*vector_norm(e2))   
    normjac = -triple_product(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Special treatment for midside node 14 (combine responses from 18 and 19 on hex)
    # Node 17
    for j in range(3):
        e0[j] = pts[ind2, j] - pts[ind5, j]
    
        e1[j] = 2*pts[ind7, j] + \
                2*pts[ind10, j] - \
                  pts[ind1, j] - \
                  pts[ind2, j] - \
                  pts[ind4, j] - \
                  pts[ind5, j] - \
                  pts[ind14, j] + \
                  pts[ind13, j]
    
        e2[j] = 2*pts[ind8, j] + \
                2*pts[ind11, j] - \
                  pts[ind0, j] - \
                  pts[ind2, j] - \
                  pts[ind3, j] - \
                  pts[ind5, j] - \
                  pts[ind14, j] + \
                  pts[ind12, j]
    
    tnorm = (vector_norm(e0)*vector_norm(e1)*vector_norm(e2))   
    normjac = -triple_product(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    return jac*1.154


cdef inline float weg_quad_qual_float(int64_t [::1] cells, int c,
                                      float [:, ::1] pts) nogil:
    """
    Compute the cell quality of a single quadratic cell
    """
    cdef float [3] e0
    cdef float [3] e1
    cdef float [3] e2

    cdef int i, j    
    cdef float normjac, tnorm
    
    cdef int ind0 = cells[c + 0]
    cdef int ind1 = cells[c + 1]
    cdef int ind2 = cells[c + 2]
    cdef int ind3 = cells[c + 3]
    cdef int ind4 = cells[c + 4]
    cdef int ind5 = cells[c + 5]
    cdef int ind6 = cells[c + 6]
    cdef int ind7 = cells[c + 7]
    cdef int ind8 = cells[c + 8]
    cdef int ind9 = cells[c + 9]
    cdef int ind10 = cells[c + 10]
    cdef int ind11 = cells[c + 11]
    cdef int ind12 = cells[c + 12]
    cdef int ind13 = cells[c + 13]
    cdef int ind14 = cells[c + 14]
    
    # Node 0
    for j in range(3):
        e0[j] = 4*pts[ind6, j] - pts[ind1, j] - 3*pts[ind0, j]
        e1[j] = 4*pts[ind8, j] - pts[ind2, j] - 3*pts[ind0, j]
        e2[j] = 4*pts[ind12, j] - pts[ind3, j] - 3*pts[ind0, j]
    
    tnorm = (vector_norm_float(e0)*vector_norm_float(e1)*vector_norm_float(e2))   

    # Store current minimum jacobian
    cdef float jac = -triple_product_float(e1, e2, e0)/tnorm

    # Node 1
    for j in range(3):
        e0[j] = 4*pts[ind7, j] - pts[ind2, j] - 3*pts[ind1, j]
        e1[j] = 4*pts[ind6, j] - pts[ind0, j] - 3*pts[ind1, j]
        e2[j] = 4*pts[ind13, j] - pts[ind4, j] - 3*pts[ind1, j]

    tnorm = (vector_norm_float(e0)*vector_norm_float(e1)*vector_norm_float(e2))   
    normjac = -triple_product_float(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 2
    # Since node 3 doesn't exist, special treatment for node 2
    for j in range(3):
        e0[j] = 4*pts[ind8, j] - pts[ind0, j] - 3*pts[ind2, j]
        e1[j] = 4*pts[ind7, j] - pts[ind1, j] - 3*pts[ind2, j]
        e2[j] = 4*pts[ind14, j] - pts[ind5, j] - 3*pts[ind2, j]
    
    tnorm = (vector_norm_float(e0)*vector_norm_float(e1)*vector_norm_float(e2))   
    normjac = -triple_product_float(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    
    # Node 4
    for j in range(3):
        e0[j] = 4*pts[ind11, j] - pts[ind5, j] - 3*pts[ind3, j]
        e1[j] = 4*pts[ind9, j] - pts[ind4, j] - 3*pts[ind3, j]
        e2[j] = 4*pts[ind12, j] - pts[ind0, j] - 3*pts[ind3, j]
    
    tnorm = (vector_norm_float(e0)*vector_norm_float(e1)*vector_norm_float(e2))   
    normjac = -triple_product_float(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    
    # Node 5
    for j in range(3):
        e0[j] = 4*pts[ind9, j] - pts[ind3, j] - 3*pts[ind4, j]
        e1[j] = 4*pts[ind10, j] - pts[ind5, j] - 3*pts[ind4, j]
        e2[j] = 4*pts[ind13, j] - pts[ind1, j] - 3*pts[ind4, j]
    
    tnorm = (vector_norm_float(e0)*vector_norm_float(e1)*vector_norm_float(e2))   
    normjac = -triple_product_float(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 6
    # Since node 3 doesn't exist, special treatment for node 2
    for j in range(3):
        e0[j] = 4*pts[ind10, j] - pts[ind4, j] - 3*pts[ind5, j]
        e1[j] = 4*pts[ind11, j] - pts[ind3, j] - 3*pts[ind5, j]
        e2[j] = 4*pts[ind14, j] - pts[ind2, j] - 3*pts[ind5, j]
    
    tnorm = (vector_norm_float(e0)*vector_norm_float(e1)*vector_norm_float(e2))   
    normjac = -triple_product_float(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 8
    for j in range(3):
        e0[j] = pts[ind1, j] - pts[ind0, j]
    
        e1[j] = 2*pts[ind7, j] + \
                2*pts[ind8, j] - \
                  pts[ind0, j] - \
                  pts[ind1, j] - \
                  pts[ind2, j] - \
                  pts[ind2, j] - \
                  pts[ind6, j] + \
                  pts[ind2, j]
    
        e2[j] = 2*pts[ind12, j] + \
                2*pts[ind13, j] - \
                  pts[ind0, j] - \
                  pts[ind1, j] - \
                  pts[ind3, j] - \
                  pts[ind4, j] - \
                  pts[ind6, j] + \
                  pts[ind9, j]
    
    tnorm = (vector_norm_float(e0)*vector_norm_float(e1)*vector_norm_float(e2))   
    normjac = -triple_product_float(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 9
    for j in range(3):
        e0[j] = pts[ind2, j] - pts[ind1, j]
    
        e1[j] = 2*pts[ind6, j] + \
                2*pts[ind2, j] - \
                  pts[ind0, j] - \
                  pts[ind1, j] - \
                  pts[ind2, j] - \
                  pts[ind2, j] - \
                  pts[ind7, j] + \
                  pts[ind8, j]
    
        e2[j] = 2*pts[ind13, j] + \
                2*pts[ind14, j] - \
                  pts[ind1, j] - \
                  pts[ind2, j] - \
                  pts[ind4, j] - \
                  pts[ind5, j] - \
                  pts[ind7, j] + \
                  pts[ind10, j]
    
    tnorm = (vector_norm_float(e0)*vector_norm_float(e1)*vector_norm_float(e2))   
    normjac = -triple_product_float(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 11
    for j in range(3):
        e0[j] = pts[ind2, j] - pts[ind0, j]
    
        e1[j] = 2*pts[ind12, j] + \
                2*pts[ind14, j] - \
                  pts[ind0, j] - \
                  pts[ind2, j] - \
                  pts[ind3, j] - \
                  pts[ind5, j] - \
                  pts[ind8, j] + \
                  pts[ind11, j]
    
        e2[j] = 2*pts[ind6, j] + \
                2*pts[ind2, j] - \
                  pts[ind0, j] - \
                  pts[ind1, j] - \
                  pts[ind2, j] - \
                  pts[ind2, j] - \
                  pts[ind8, j] + \
                  pts[ind7, j]
    
    tnorm = (vector_norm_float(e0)*vector_norm_float(e1)*vector_norm_float(e2))   
    normjac = -triple_product_float(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 12
    for j in range(3):
        e0[j] = pts[ind3, j] - pts[ind4, j]
    
        e1[j] = 2*pts[ind10, j] + \
                2*pts[ind11, j] - \
                  pts[ind3, j] - \
                  pts[ind4, j] - \
                  pts[ind5, j] - \
                  pts[ind5, j] - \
                  pts[ind9, j] + \
                  pts[ind5, j]
    
        e2[j] = 2*pts[ind12, j] + \
                2*pts[ind13, j] - \
                  pts[ind0, j] - \
                  pts[ind1, j] - \
                  pts[ind3, j] - \
                  pts[ind4, j] - \
                  pts[ind9, j] + \
                  pts[ind6, j]
    
    tnorm = (vector_norm_float(e0)*vector_norm_float(e1)*vector_norm_float(e2))   
    normjac = -triple_product_float(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 13
    for j in range(3):
        e0[j] = pts[ind4, j] - pts[ind5, j]
    
        e1[j] = 2*pts[ind9, j] + \
                2*pts[ind5, j] - \
                  pts[ind3, j] - \
                  pts[ind4, j] - \
                  pts[ind5, j] - \
                  pts[ind5, j] - \
                  pts[ind10, j] + \
                  pts[ind11, j]
    
        e2[j] = 2*pts[ind13, j] + \
                2*pts[ind14, j] - \
                  pts[ind1, j] - \
                  pts[ind2, j] - \
                  pts[ind4, j] - \
                  pts[ind5, j] - \
                  pts[ind10, j] + \
                  pts[ind7, j]
    
    tnorm = (vector_norm_float(e0)*vector_norm_float(e1)*vector_norm_float(e2))   
    normjac = -triple_product_float(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 15
    for j in range(3):
        e0[j] = pts[ind5, j] - pts[ind3, j]
    
        e1[j] = 2*pts[ind5, j] + \
                2*pts[ind9, j] - \
                  pts[ind3, j] - \
                  pts[ind4, j] - \
                  pts[ind5, j] - \
                  pts[ind5, j] - \
                  pts[ind11, j] + \
                  pts[ind10, j]
    
        e2[j] = 2*pts[ind12, j] + \
                2*pts[ind14, j] - \
                  pts[ind0, j] - \
                  pts[ind2, j] - \
                  pts[ind3, j] - \
                  pts[ind5, j] - \
                  pts[ind11, j] + \
                  pts[ind8, j]
    
    tnorm = (vector_norm_float(e0)*vector_norm_float(e1)*vector_norm_float(e2))   
    normjac = -triple_product_float(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 16
    for j in range(3):
        e0[j] = pts[ind0, j] - pts[ind3, j]
    
        e1[j] = 2*pts[ind8, j] + \
                2*pts[ind11, j] - \
                  pts[ind0, j] - \
                  pts[ind2, j] - \
                  pts[ind3, j] - \
                  pts[ind5, j] - \
                  pts[ind12, j] + \
                  pts[ind14, j]
    
        e2[j] = 2*pts[ind6, j] + \
                2*pts[ind9, j] - \
                  pts[ind0, j] - \
                  pts[ind1, j] - \
                  pts[ind3, j] - \
                  pts[ind4, j] - \
                  pts[ind12, j] + \
                  pts[ind13, j]
    
    tnorm = (vector_norm_float(e0)*vector_norm_float(e1)*vector_norm_float(e2))   
    normjac = -triple_product_float(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 17
    for j in range(3):
        e0[j] = pts[ind1, j] - pts[ind4, j]
    
        e1[j] = 2*pts[ind6, j] + \
                2*pts[ind9, j] - \
                  pts[ind0, j] - \
                  pts[ind1, j] - \
                  pts[ind3, j] - \
                  pts[ind4, j] - \
                  pts[ind13, j] + \
                  pts[ind12, j]
    
        e2[j] = 2*pts[ind7, j] + \
                2*pts[ind10, j] - \
                  pts[ind1, j] - \
                  pts[ind2, j] - \
                  pts[ind4, j] - \
                  pts[ind5, j] - \
                  pts[ind13, j] + \
                  pts[ind14, j]
    
    tnorm = (vector_norm_float(e0)*vector_norm_float(e1)*vector_norm_float(e2))   
    normjac = -triple_product_float(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Special treatment for midside node 14 (combine responses from 18 and 19 on hex)
    # Node 17
    for j in range(3):
        e0[j] = pts[ind2, j] - pts[ind5, j]
    
        e1[j] = 2*pts[ind7, j] + \
                2*pts[ind10, j] - \
                  pts[ind1, j] - \
                  pts[ind2, j] - \
                  pts[ind4, j] - \
                  pts[ind5, j] - \
                  pts[ind14, j] + \
                  pts[ind13, j]
    
        e2[j] = 2*pts[ind8, j] + \
                2*pts[ind11, j] - \
                  pts[ind0, j] - \
                  pts[ind2, j] - \
                  pts[ind3, j] - \
                  pts[ind5, j] - \
                  pts[ind14, j] + \
                  pts[ind12, j]
    
    tnorm = (vector_norm_float(e0)*vector_norm_float(e1)*vector_norm_float(e2))   
    normjac = -triple_product_float(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    return jac*1.154


cdef inline double hex_quad_qual(int64_t [::1] cells, int c,
                              double [:, ::1] pts) nogil:
    """
    Quadradic shape functions derived and then printed in pre-index form using
    the following code:
    
    import sympy
    import numpy as np

    # idea node locations for quadradic hexahedral    
    edgept = np.array([[-1, -1, -1],
                       [ 1, -1, -1],
                       [ 1,  1, -1],
                       [-1,  1, -1],
                       [-1, -1,  1],
                       [ 1, -1,  1],
                       [ 1,  1,  1],
                       [-1,  1,  1]])
    
    # midside node indices             
    idx = np.array([[0, 1], # 8
                    [1, 2],# 9
                    [2, 3],# 10
                    [3, 0],# 11
                    [4, 5],# 12
                    [5, 6],# 13
                    [6, 7],# 14
                    [7, 4],# 15
                    [0, 4],# 16
                    [1, 5],# 17
                    [2, 6],# 18
                    [3, 7]], np.int)# 19
    
    midpt = (edgept[idx[:, 0]] + edgept[idx[:, 1]])/2
    
    isopts = np.empty((20, 3))
    isopts[:8] = edgept
    isopts[8:] = midpt
    
                       
    # Shape function evaluated at sampling locations
    u = np.empty((20, 20))
    for i in range(20):
        zi, eta, zeta = isopts[i]
    #    eta  = isopts[i, 1]
    #    zeta = isopts[i, 2]
        u[i] = [1, zi, eta, zeta, zi**2, eta**2, zeta**2,
                zi*eta, eta*zeta, zeta*zi,
                zi**2*eta, zi*eta**2, eta**2*zeta, eta*zeta**2, zeta**2*zi,
                zeta*zi**2, zi*eta*zeta,
                zi**2*eta*zeta, zi*eta**2*zeta, zi*eta*zeta**2]
    
    
    zi, eta, zeta = sympy.symbols('zi eta zeta', real=True)
    shp = [1,
          zi,
          eta,
          zeta,
          zi**2,
          eta**2,
          zeta**2,
          eta*zi,
          eta*zeta,
          zeta*zi,
          eta*zi**2,
          eta**2*zi,
          eta**2*zeta,
          eta*zeta**2,
          zeta**2*zi,
          zeta*zi**2,
          eta*zeta*zi,
          eta*zeta*zi**2,
          eta**2*zeta*zi,
          eta*zeta**2*zi]
    
    shape_functions = np.array(np.matrix(shp)*np.matrix(np.linalg.inv(u))).ravel()
    
    # Take the differental of each shape function evaluated at the intergration
    # point with respect to the natural shape coordinate system
    nprime = np.empty((3, 20), np.object)
    variables = [zi, eta, zeta]
    for i in range(20):
        for j in range(3):
             nprime[j, i] = sympy.diff(shape_functions[i], variables[j])
    
    
    # This is the N_prime functions with the isopts subbed into them
    pre_j = np.empty((60, 20))
    for i in range(20):
        for j in range(3):
            for k in range(20):
                pre_j[i*3 + j, k] = nprime[j, k].subs([(zi,   isopts[i, 0]),
                                                       (eta,  isopts[i, 1]),
                                                       (zeta, isopts[i, 2])])
                                                       

    hex_quad_edges = np.empty((20, 3, 8), np.int32)
    hex_quad_edges[0][0][0] = 1
    hex_quad_edges[0][0][1] = 3
    hex_quad_edges[0][0][2] = 4
    hex_quad_edges[0][1][0] = 8
    hex_quad_edges[0][1][1] = 11
    hex_quad_edges[0][1][2] = 16
    
    hex_quad_edges[1][0][0] = 2
    hex_quad_edges[1][0][1] = 0
    hex_quad_edges[1][0][2] = 5
    hex_quad_edges[1][1][0] = 9
    hex_quad_edges[1][1][1] = 8
    hex_quad_edges[1][1][2] = 17
    
    hex_quad_edges[2][0][0] = 3
    hex_quad_edges[2][0][1] = 1
    hex_quad_edges[2][0][2] = 6
    hex_quad_edges[2][1][0] = 10
    hex_quad_edges[2][1][1] = 9
    hex_quad_edges[2][1][2] = 18
    
    hex_quad_edges[3][0][0] = 0
    hex_quad_edges[3][0][1] = 2
    hex_quad_edges[3][0][2] = 7
    hex_quad_edges[3][1][0] = 11
    hex_quad_edges[3][1][1] = 10
    hex_quad_edges[3][1][2] = 19
    
    hex_quad_edges[4][0][0] = 7
    hex_quad_edges[4][0][1] = 5
    hex_quad_edges[4][0][2] = 0
    hex_quad_edges[4][1][0] = 15
    hex_quad_edges[4][1][1] = 12
    hex_quad_edges[4][1][2] = 16
    
    hex_quad_edges[5][0][0] = 4
    hex_quad_edges[5][0][1] = 6
    hex_quad_edges[5][0][2] = 1
    hex_quad_edges[5][1][0] = 12
    hex_quad_edges[5][1][1] = 13
    hex_quad_edges[5][1][2] = 17
    
    hex_quad_edges[6][0][0] = 5
    hex_quad_edges[6][0][1] = 7
    hex_quad_edges[6][0][2] = 2
    hex_quad_edges[6][1][0] = 13
    hex_quad_edges[6][1][1] = 14
    hex_quad_edges[6][1][2] = 18
    
    hex_quad_edges[7][0][0] = 6
    hex_quad_edges[7][0][1] = 4
    hex_quad_edges[7][0][2] = 3
    hex_quad_edges[7][1][0] = 14
    hex_quad_edges[7][1][1] = 15
    hex_quad_edges[7][1][2] = 19
        
    
    # Node 8 (between edges 0 and 1)
    hex_quad_edges[8][0][0] = 1
    hex_quad_edges[8][0][1] = 0
    
    hex_quad_edges[8][1][0] = 9
    hex_quad_edges[8][1][1] = 11
    hex_quad_edges[8][1][2] = 0
    hex_quad_edges[8][1][3] = 1
    hex_quad_edges[8][1][4] = 2
    hex_quad_edges[8][1][5] = 3
    hex_quad_edges[8][1][6] = 8
    hex_quad_edges[8][1][7] = 10
    
    hex_quad_edges[8][2][0] = 16
    hex_quad_edges[8][2][1] = 17
    hex_quad_edges[8][2][2] = 0
    hex_quad_edges[8][2][3] = 1
    hex_quad_edges[8][2][4] = 4
    hex_quad_edges[8][2][5] = 5
    hex_quad_edges[8][2][6] = 8
    hex_quad_edges[8][2][7] = 12
    
    
    # Node 9 (between edges 1 and 2)
    hex_quad_edges[9][1][0] = 8
    hex_quad_edges[9][1][1] = 10
    hex_quad_edges[9][1][2] = 0
    hex_quad_edges[9][1][3] = 1
    hex_quad_edges[9][1][4] = 2
    hex_quad_edges[9][1][5] = 3
    hex_quad_edges[9][1][6] = 9
    hex_quad_edges[9][1][7] = 11
    
    hex_quad_edges[9][0][0] = 2
    hex_quad_edges[9][0][1] = 1
    
    hex_quad_edges[9][2][0] = 17
    hex_quad_edges[9][2][1] = 18
    hex_quad_edges[9][2][2] = 1
    hex_quad_edges[9][2][3] = 2
    hex_quad_edges[9][2][4] = 5
    hex_quad_edges[9][2][5] = 6
    hex_quad_edges[9][2][6] = 9
    hex_quad_edges[9][2][7] = 13
    
    
    # Node 10 (between edges 2 and 3)
    hex_quad_edges[10][0][0] = 3
    hex_quad_edges[10][0][1] = 2
    
    hex_quad_edges[10][1][0] = 9
    hex_quad_edges[10][1][1] = 11
    hex_quad_edges[10][1][2] = 0
    hex_quad_edges[10][1][3] = 1
    hex_quad_edges[10][1][4] = 2
    hex_quad_edges[10][1][5] = 3
    hex_quad_edges[10][1][6] = 10
    hex_quad_edges[10][1][7] = 8
    
    hex_quad_edges[10][2][0] = 18
    hex_quad_edges[10][2][1] = 19
    hex_quad_edges[10][2][2] = 2
    hex_quad_edges[10][2][3] = 3
    hex_quad_edges[10][2][4] = 6
    hex_quad_edges[10][2][5] = 7
    hex_quad_edges[10][2][6] = 10
    hex_quad_edges[10][2][7] = 14
    
    
    
    # Node 11 (between edge nodes 0 and 3)
    hex_quad_edges[11][0][0] = 3
    hex_quad_edges[11][0][1] = 0
    
    hex_quad_edges[11][1][0] = 16
    hex_quad_edges[11][1][1] = 19
    hex_quad_edges[11][1][2] = 0
    hex_quad_edges[11][1][3] = 3
    hex_quad_edges[11][1][4] = 4
    hex_quad_edges[11][1][5] = 7
    hex_quad_edges[11][1][6] = 11
    hex_quad_edges[11][1][7] = 15
    
    hex_quad_edges[11][2][0] = 8
    hex_quad_edges[11][2][1] = 10
    hex_quad_edges[11][2][2] = 0
    hex_quad_edges[11][2][3] = 1
    hex_quad_edges[11][2][4] = 2
    hex_quad_edges[11][2][5] = 3
    hex_quad_edges[11][2][6] = 11
    hex_quad_edges[11][2][7] = 9
    
    
    # Node 12 (between edges 3 and 0)
    hex_quad_edges[12][0][0] = 4
    hex_quad_edges[12][0][1] = 5
    
    hex_quad_edges[12][1][0] = 13
    hex_quad_edges[12][1][1] = 15
    hex_quad_edges[12][1][2] = 4
    hex_quad_edges[12][1][3] = 5
    hex_quad_edges[12][1][4] = 6
    hex_quad_edges[12][1][5] = 7
    hex_quad_edges[12][1][6] = 12
    hex_quad_edges[12][1][7] = 14
    
    hex_quad_edges[12][2][0] = 16
    hex_quad_edges[12][2][1] = 17
    hex_quad_edges[12][2][2] = 0
    hex_quad_edges[12][2][3] = 1
    hex_quad_edges[12][2][4] = 4
    hex_quad_edges[12][2][5] = 5
    hex_quad_edges[12][2][6] = 12
    hex_quad_edges[12][2][7] = 8
    
    
    # Node 13 (between edges 1 and 2)
    hex_quad_edges[13][1][0] = 12
    hex_quad_edges[13][1][1] = 14
    hex_quad_edges[13][1][2] = 4
    hex_quad_edges[13][1][3] = 5
    hex_quad_edges[13][1][4] = 6
    hex_quad_edges[13][1][5] = 7
    hex_quad_edges[13][1][6] = 13
    hex_quad_edges[13][1][7] = 15
    
    hex_quad_edges[13][0][0] = 5
    hex_quad_edges[13][0][1] = 6
    
    hex_quad_edges[13][2][0] = 17
    hex_quad_edges[13][2][1] = 18
    hex_quad_edges[13][2][2] = 1
    hex_quad_edges[13][2][3] = 2
    hex_quad_edges[13][2][4] = 5
    hex_quad_edges[13][2][5] = 6
    hex_quad_edges[13][2][6] = 13
    hex_quad_edges[13][2][7] = 9
    
    
    # Node 14 (between edges 2 and 3)
    hex_quad_edges[14][0][0] = 6
    hex_quad_edges[14][0][1] = 7
    
    hex_quad_edges[14][1][0] = 13
    hex_quad_edges[14][1][1] = 15
    hex_quad_edges[14][1][2] = 4
    hex_quad_edges[14][1][3] = 5
    hex_quad_edges[14][1][4] = 6
    hex_quad_edges[14][1][5] = 7
    hex_quad_edges[14][1][6] = 14
    hex_quad_edges[14][1][7] = 12
    
    hex_quad_edges[14][2][0] = 18
    hex_quad_edges[14][2][1] = 19
    hex_quad_edges[14][2][2] = 2
    hex_quad_edges[14][2][3] = 3
    hex_quad_edges[14][2][4] = 6
    hex_quad_edges[14][2][5] = 7
    hex_quad_edges[14][2][6] = 14
    hex_quad_edges[14][2][7] = 10
    
    
    # Node 15 (between edges 1 and 2)
    hex_quad_edges[15][1][0] = 14
    hex_quad_edges[15][1][1] = 12
    hex_quad_edges[15][1][2] = 4
    hex_quad_edges[15][1][3] = 5
    hex_quad_edges[15][1][4] = 6
    hex_quad_edges[15][1][5] = 7
    hex_quad_edges[15][1][6] = 15
    hex_quad_edges[15][1][7] = 13
    
    hex_quad_edges[15][0][0] = 7
    hex_quad_edges[15][0][1] = 4
    
    hex_quad_edges[15][2][0] = 16
    hex_quad_edges[15][2][1] = 19
    hex_quad_edges[15][2][2] = 0
    hex_quad_edges[15][2][3] = 3
    hex_quad_edges[15][2][4] = 4
    hex_quad_edges[15][2][5] = 7
    hex_quad_edges[15][2][6] = 15
    hex_quad_edges[15][2][7] = 11
    
    # Node 16 (between edges 4 and 0)
    hex_quad_edges[16][0][0] = 0
    hex_quad_edges[16][0][1] = 4
    
    hex_quad_edges[16][1][0] = 11
    hex_quad_edges[16][1][1] = 15
    hex_quad_edges[16][1][2] = 0
    hex_quad_edges[16][1][3] = 3
    hex_quad_edges[16][1][4] = 4
    hex_quad_edges[16][1][5] = 7
    hex_quad_edges[16][1][6] = 16
    hex_quad_edges[16][1][7] = 19
    
    hex_quad_edges[16][2][0] = 8
    hex_quad_edges[16][2][1] = 12
    hex_quad_edges[16][2][2] = 0
    hex_quad_edges[16][2][3] = 1
    hex_quad_edges[16][2][4] = 4
    hex_quad_edges[16][2][5] = 5
    hex_quad_edges[16][2][6] = 16
    hex_quad_edges[16][2][7] = 17
    
    
    # Node 17 (between edges 4 and 0)
    hex_quad_edges[17][0][0] = 1
    hex_quad_edges[17][0][1] = 5
    
    hex_quad_edges[17][1][0] = 8
    hex_quad_edges[17][1][1] = 12
    hex_quad_edges[17][1][2] = 0
    hex_quad_edges[17][1][3] = 1
    hex_quad_edges[17][1][4] = 4
    hex_quad_edges[17][1][5] = 5
    hex_quad_edges[17][1][6] = 17
    hex_quad_edges[17][1][7] = 16
    
    hex_quad_edges[17][2][0] = 9
    hex_quad_edges[17][2][1] = 13
    hex_quad_edges[17][2][2] = 1
    hex_quad_edges[17][2][3] = 2
    hex_quad_edges[17][2][4] = 5
    hex_quad_edges[17][2][5] = 6
    hex_quad_edges[17][2][6] = 17
    hex_quad_edges[17][2][7] = 18
    
    
    # Node 18 (between edges 4 and 0)
    hex_quad_edges[18][0][0] = 2
    hex_quad_edges[18][0][1] = 6
    
    hex_quad_edges[18][1][0] = 9
    hex_quad_edges[18][1][1] = 13
    hex_quad_edges[18][1][2] = 1
    hex_quad_edges[18][1][3] = 2
    hex_quad_edges[18][1][4] = 5
    hex_quad_edges[18][1][5] = 6
    hex_quad_edges[18][1][6] = 18
    hex_quad_edges[18][1][7] = 17
    
    hex_quad_edges[18][2][0] = 10
    hex_quad_edges[18][2][1] = 14
    hex_quad_edges[18][2][2] = 2
    hex_quad_edges[18][2][3] = 3
    hex_quad_edges[18][2][4] = 6
    hex_quad_edges[18][2][5] = 7
    hex_quad_edges[18][2][6] = 18
    hex_quad_edges[18][2][7] = 19
    
    
    # Node 19 (between edges 4 and 0)
    hex_quad_edges[19][0][0] = 3
    hex_quad_edges[19][0][1] = 7
    
    hex_quad_edges[19][1][0] = 10
    hex_quad_edges[19][1][1] = 14
    hex_quad_edges[19][1][2] = 2
    hex_quad_edges[19][1][3] = 3
    hex_quad_edges[19][1][4] = 6
    hex_quad_edges[19][1][5] = 7
    hex_quad_edges[19][1][6] = 19
    hex_quad_edges[19][1][7] = 18
    
    hex_quad_edges[19][2][0] = 11
    hex_quad_edges[19][2][1] = 15
    hex_quad_edges[19][2][2] = 0
    hex_quad_edges[19][2][3] = 3
    hex_quad_edges[19][2][4] = 4
    hex_quad_edges[19][2][5] = 7
    hex_quad_edges[19][2][6] = 19
    hex_quad_edges[19][2][7] = 16
    
    
    
    for i in range(20):
        print 'cdef int ind{:d} = cells[c + {:d}]'.format(i, i)
    
    
    
    for i in range(8):
        print '# Node {:d}'.format(i)
        print 'for j in range(3):'
        print '    e0[j]  = 4*pts[ind{:d}, j] - pts[ind{:d}, j] - 3*pts[ind{:d}, j]'.format(hex_quad_edges[i][1][0], hex_quad_edges[i][0][0], i)
        print '    e1[j]  = 4*pts[ind{:d}, j] - pts[ind{:d}, j] - 3*pts[ind{:d}, j]'.format(hex_quad_edges[i][1][1], hex_quad_edges[i][0][1], i)
        print '    e2[j]  = 4*pts[ind{:d}, j] - pts[ind{:d}, j] - 3*pts[ind{:d}, j]'.format(hex_quad_edges[i][1][2], hex_quad_edges[i][0][2], i)
        print 
        print '# normalize the determinant of the jacobian'
        print 'tnorm = (vector_norm(e0)*vector_norm(e1)*vector_norm(e2))' 
        print 'normjac = triple_product(e1, e2, e0)/tnorm'
        print 
        print '# Track minimum jacobian'
        print 'if normjac < jac:'
        print '    jac = normjac'
        print 
    
    
    # midside nodes along x moving edges
    for i in range(8, 20):
        print '# Node {:d}'.format(i)
        print 'for j in range(3):'
        print '    e0[j] = pts[ind{:d}, j] - pts[ind{:d}, j]'.format(hex_quad_edges[i][0][0], hex_quad_edges[i][0][1])
        print
        
        print '    e1[j] = 2*pts[ind{:d}, j] + \\'.format(hex_quad_edges[i][1][0])
        print '         2*pts[ind{:d}, j] - \\'.format(hex_quad_edges[i][1][1])
        print '           pts[ind{:d}, j] - \\'.format(hex_quad_edges[i][1][2])
        print '           pts[ind{:d}, j] - \\'.format(hex_quad_edges[i][1][3])
        print '           pts[ind{:d}, j] - \\'.format(hex_quad_edges[i][1][4])
        print '           pts[ind{:d}, j] - \\'.format(hex_quad_edges[i][1][5])
        print '           pts[ind{:d}, j] + \\'.format(hex_quad_edges[i][1][6])
        print '           pts[ind{:d}, j]'.format(hex_quad_edges[i][1][7])
        print
        print '    e2[j] = 2*pts[ind{:d}, j] + \\'.format(hex_quad_edges[i][2][0])
        print '         2*pts[ind{:d}, j] - \\'.format(hex_quad_edges[i][2][1])
        print '           pts[ind{:d}, j] - \\'.format(hex_quad_edges[i][2][2])
        print '           pts[ind{:d}, j] - \\'.format(hex_quad_edges[i][2][3])
        print '           pts[ind{:d}, j] - \\'.format(hex_quad_edges[i][2][4])
        print '           pts[ind{:d}, j] - \\'.format(hex_quad_edges[i][2][5])
        print '           pts[ind{:d}, j] + \\'.format(hex_quad_edges[i][2][6])
        print '           pts[ind{:d}, j]'.format(hex_quad_edges[i][2][7])
        print 
        print '# normalize the determinant of the jacobian'
        print 'tnorm = (vector_norm(e0)*vector_norm(e1)*vector_norm(e2))' 
        print 'normjac = triple_product(e1, e2, e0)/tnorm'
        print 
        print '# Track minimum jacobian'
        print 'if normjac < jac:'
        print '    jac = normjac'
        print 
    
    """

    cdef double jac = 1.1

    cdef double [3] e0
    cdef double [3] e1
    cdef double [3] e2

    cdef int i, j    
    cdef double normjac, tnorm
    
    # Store cell indices
    cdef int ind0 = cells[c + 0]
    cdef int ind1 = cells[c + 1]
    cdef int ind2 = cells[c + 2]
    cdef int ind3 = cells[c + 3]
    cdef int ind4 = cells[c + 4]
    cdef int ind5 = cells[c + 5]
    cdef int ind6 = cells[c + 6]
    cdef int ind7 = cells[c + 7]
    cdef int ind8 = cells[c + 8]
    cdef int ind9 = cells[c + 9]
    cdef int ind10 = cells[c + 10]
    cdef int ind11 = cells[c + 11]
    cdef int ind12 = cells[c + 12]
    cdef int ind13 = cells[c + 13]
    cdef int ind14 = cells[c + 14]
    cdef int ind15 = cells[c + 15]
    cdef int ind16 = cells[c + 16]
    cdef int ind17 = cells[c + 17]
    cdef int ind18 = cells[c + 18]
    cdef int ind19 = cells[c + 19]
    
    # Node 0
    for j in range(3):
        e0[j]  = 4*pts[ind8, j] - pts[ind1, j] - 3*pts[ind0, j]
        e1[j]  = 4*pts[ind11, j] - pts[ind3, j] - 3*pts[ind0, j]
        e2[j]  = 4*pts[ind16, j] - pts[ind4, j] - 3*pts[ind0, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm(e0)*vector_norm(e1)*vector_norm(e2))
    normjac = triple_product(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 1
    for j in range(3):
        e0[j]  = 4*pts[ind9, j] - pts[ind2, j] - 3*pts[ind1, j]
        e1[j]  = 4*pts[ind8, j] - pts[ind0, j] - 3*pts[ind1, j]
        e2[j]  = 4*pts[ind17, j] - pts[ind5, j] - 3*pts[ind1, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm(e0)*vector_norm(e1)*vector_norm(e2))
    normjac = triple_product(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 2
    for j in range(3):
        e0[j]  = 4*pts[ind10, j] - pts[ind3, j] - 3*pts[ind2, j]
        e1[j]  = 4*pts[ind9, j] - pts[ind1, j] - 3*pts[ind2, j]
        e2[j]  = 4*pts[ind18, j] - pts[ind6, j] - 3*pts[ind2, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm(e0)*vector_norm(e1)*vector_norm(e2))
    normjac = triple_product(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 3
    for j in range(3):
        e0[j]  = 4*pts[ind11, j] - pts[ind0, j] - 3*pts[ind3, j]
        e1[j]  = 4*pts[ind10, j] - pts[ind2, j] - 3*pts[ind3, j]
        e2[j]  = 4*pts[ind19, j] - pts[ind7, j] - 3*pts[ind3, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm(e0)*vector_norm(e1)*vector_norm(e2))
    normjac = triple_product(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 4
    for j in range(3):
        e0[j]  = 4*pts[ind15, j] - pts[ind7, j] - 3*pts[ind4, j]
        e1[j]  = 4*pts[ind12, j] - pts[ind5, j] - 3*pts[ind4, j]
        e2[j]  = 4*pts[ind16, j] - pts[ind0, j] - 3*pts[ind4, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm(e0)*vector_norm(e1)*vector_norm(e2))
    normjac = triple_product(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 5
    for j in range(3):
        e0[j]  = 4*pts[ind12, j] - pts[ind4, j] - 3*pts[ind5, j]
        e1[j]  = 4*pts[ind13, j] - pts[ind6, j] - 3*pts[ind5, j]
        e2[j]  = 4*pts[ind17, j] - pts[ind1, j] - 3*pts[ind5, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm(e0)*vector_norm(e1)*vector_norm(e2))
    normjac = triple_product(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 6
    for j in range(3):
        e0[j]  = 4*pts[ind13, j] - pts[ind5, j] - 3*pts[ind6, j]
        e1[j]  = 4*pts[ind14, j] - pts[ind7, j] - 3*pts[ind6, j]
        e2[j]  = 4*pts[ind18, j] - pts[ind2, j] - 3*pts[ind6, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm(e0)*vector_norm(e1)*vector_norm(e2))
    normjac = triple_product(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 7
    for j in range(3):
        e0[j]  = 4*pts[ind14, j] - pts[ind6, j] - 3*pts[ind7, j]
        e1[j]  = 4*pts[ind15, j] - pts[ind4, j] - 3*pts[ind7, j]
        e2[j]  = 4*pts[ind19, j] - pts[ind3, j] - 3*pts[ind7, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm(e0)*vector_norm(e1)*vector_norm(e2))
    normjac = triple_product(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 8
    for j in range(3):
        e0[j] = pts[ind1, j] - pts[ind0, j]
    
        e1[j] = 2*pts[ind9, j] + \
             2*pts[ind11, j] - \
               pts[ind0, j] - \
               pts[ind1, j] - \
               pts[ind2, j] - \
               pts[ind3, j] - \
               pts[ind8, j] + \
               pts[ind10, j]
    
        e2[j] = 2*pts[ind16, j] + \
             2*pts[ind17, j] - \
               pts[ind0, j] - \
               pts[ind1, j] - \
               pts[ind4, j] - \
               pts[ind5, j] - \
               pts[ind8, j] + \
               pts[ind12, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm(e0)*vector_norm(e1)*vector_norm(e2))
    normjac = triple_product(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 9
    for j in range(3):
        e0[j] = pts[ind2, j] - pts[ind1, j]
    
        e1[j] = 2*pts[ind8, j] + \
             2*pts[ind10, j] - \
               pts[ind0, j] - \
               pts[ind1, j] - \
               pts[ind2, j] - \
               pts[ind3, j] - \
               pts[ind9, j] + \
               pts[ind11, j]
    
        e2[j] = 2*pts[ind17, j] + \
             2*pts[ind18, j] - \
               pts[ind1, j] - \
               pts[ind2, j] - \
               pts[ind5, j] - \
               pts[ind6, j] - \
               pts[ind9, j] + \
               pts[ind13, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm(e0)*vector_norm(e1)*vector_norm(e2))
    normjac = triple_product(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 10
    for j in range(3):
        e0[j] = pts[ind3, j] - pts[ind2, j]
    
        e1[j] = 2*pts[ind9, j] + \
             2*pts[ind11, j] - \
               pts[ind0, j] - \
               pts[ind1, j] - \
               pts[ind2, j] - \
               pts[ind3, j] - \
               pts[ind10, j] + \
               pts[ind8, j]
    
        e2[j] = 2*pts[ind18, j] + \
             2*pts[ind19, j] - \
               pts[ind2, j] - \
               pts[ind3, j] - \
               pts[ind6, j] - \
               pts[ind7, j] - \
               pts[ind10, j] + \
               pts[ind14, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm(e0)*vector_norm(e1)*vector_norm(e2))
    normjac = triple_product(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 11
    for j in range(3):
        e0[j] = pts[ind3, j] - pts[ind0, j]
    
        e1[j] = 2*pts[ind16, j] + \
             2*pts[ind19, j] - \
               pts[ind0, j] - \
               pts[ind3, j] - \
               pts[ind4, j] - \
               pts[ind7, j] - \
               pts[ind11, j] + \
               pts[ind15, j]
    
        e2[j] = 2*pts[ind8, j] + \
             2*pts[ind10, j] - \
               pts[ind0, j] - \
               pts[ind1, j] - \
               pts[ind2, j] - \
               pts[ind3, j] - \
               pts[ind11, j] + \
               pts[ind9, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm(e0)*vector_norm(e1)*vector_norm(e2))
    normjac = triple_product(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 12
    for j in range(3):
        e0[j] = pts[ind4, j] - pts[ind5, j]
    
        e1[j] = 2*pts[ind13, j] + \
             2*pts[ind15, j] - \
               pts[ind4, j] - \
               pts[ind5, j] - \
               pts[ind6, j] - \
               pts[ind7, j] - \
               pts[ind12, j] + \
               pts[ind14, j]
    
        e2[j] = 2*pts[ind16, j] + \
             2*pts[ind17, j] - \
               pts[ind0, j] - \
               pts[ind1, j] - \
               pts[ind4, j] - \
               pts[ind5, j] - \
               pts[ind12, j] + \
               pts[ind8, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm(e0)*vector_norm(e1)*vector_norm(e2))
    normjac = triple_product(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 13
    for j in range(3):
        e0[j] = pts[ind5, j] - pts[ind6, j]
    
        e1[j] = 2*pts[ind12, j] + \
             2*pts[ind14, j] - \
               pts[ind4, j] - \
               pts[ind5, j] - \
               pts[ind6, j] - \
               pts[ind7, j] - \
               pts[ind13, j] + \
               pts[ind15, j]
    
        e2[j] = 2*pts[ind17, j] + \
             2*pts[ind18, j] - \
               pts[ind1, j] - \
               pts[ind2, j] - \
               pts[ind5, j] - \
               pts[ind6, j] - \
               pts[ind13, j] + \
               pts[ind9, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm(e0)*vector_norm(e1)*vector_norm(e2))
    normjac = triple_product(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 14
    for j in range(3):
        e0[j] = pts[ind6, j] - pts[ind7, j]
    
        e1[j] = 2*pts[ind13, j] + \
             2*pts[ind15, j] - \
               pts[ind4, j] - \
               pts[ind5, j] - \
               pts[ind6, j] - \
               pts[ind7, j] - \
               pts[ind14, j] + \
               pts[ind12, j]
    
        e2[j] = 2*pts[ind18, j] + \
             2*pts[ind19, j] - \
               pts[ind2, j] - \
               pts[ind3, j] - \
               pts[ind6, j] - \
               pts[ind7, j] - \
               pts[ind14, j] + \
               pts[ind10, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm(e0)*vector_norm(e1)*vector_norm(e2))
    normjac = triple_product(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 15
    for j in range(3):
        e0[j] = pts[ind7, j] - pts[ind4, j]
    
        e1[j] = 2*pts[ind14, j] + \
             2*pts[ind12, j] - \
               pts[ind4, j] - \
               pts[ind5, j] - \
               pts[ind6, j] - \
               pts[ind7, j] - \
               pts[ind15, j] + \
               pts[ind13, j]
    
        e2[j] = 2*pts[ind16, j] + \
             2*pts[ind19, j] - \
               pts[ind0, j] - \
               pts[ind3, j] - \
               pts[ind4, j] - \
               pts[ind7, j] - \
               pts[ind15, j] + \
               pts[ind11, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm(e0)*vector_norm(e1)*vector_norm(e2))
    normjac = triple_product(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 16
    for j in range(3):
        e0[j] = pts[ind0, j] - pts[ind4, j]
    
        e1[j] = 2*pts[ind11, j] + \
             2*pts[ind15, j] - \
               pts[ind0, j] - \
               pts[ind3, j] - \
               pts[ind4, j] - \
               pts[ind7, j] - \
               pts[ind16, j] + \
               pts[ind19, j]
    
        e2[j] = 2*pts[ind8, j] + \
             2*pts[ind12, j] - \
               pts[ind0, j] - \
               pts[ind1, j] - \
               pts[ind4, j] - \
               pts[ind5, j] - \
               pts[ind16, j] + \
               pts[ind17, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm(e0)*vector_norm(e1)*vector_norm(e2))
    normjac = triple_product(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 17
    for j in range(3):
        e0[j] = pts[ind1, j] - pts[ind5, j]
    
        e1[j] = 2*pts[ind8, j] + \
             2*pts[ind12, j] - \
               pts[ind0, j] - \
               pts[ind1, j] - \
               pts[ind4, j] - \
               pts[ind5, j] - \
               pts[ind17, j] + \
               pts[ind16, j]
    
        e2[j] = 2*pts[ind9, j] + \
             2*pts[ind13, j] - \
               pts[ind1, j] - \
               pts[ind2, j] - \
               pts[ind5, j] - \
               pts[ind6, j] - \
               pts[ind17, j] + \
               pts[ind18, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm(e0)*vector_norm(e1)*vector_norm(e2))
    normjac = triple_product(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 18
    for j in range(3):
        e0[j] = pts[ind2, j] - pts[ind6, j]
    
        e1[j] = 2*pts[ind9, j] + \
             2*pts[ind13, j] - \
               pts[ind1, j] - \
               pts[ind2, j] - \
               pts[ind5, j] - \
               pts[ind6, j] - \
               pts[ind18, j] + \
               pts[ind17, j]
    
        e2[j] = 2*pts[ind10, j] + \
             2*pts[ind14, j] - \
               pts[ind2, j] - \
               pts[ind3, j] - \
               pts[ind6, j] - \
               pts[ind7, j] - \
               pts[ind18, j] + \
               pts[ind19, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm(e0)*vector_norm(e1)*vector_norm(e2))
    normjac = triple_product(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 19
    for j in range(3):
        e0[j] = pts[ind3, j] - pts[ind7, j]
    
        e1[j] = 2*pts[ind10, j] + \
             2*pts[ind14, j] - \
               pts[ind2, j] - \
               pts[ind3, j] - \
               pts[ind6, j] - \
               pts[ind7, j] - \
               pts[ind19, j] + \
               pts[ind18, j]
    
        e2[j] = 2*pts[ind11, j] + \
             2*pts[ind15, j] - \
               pts[ind0, j] - \
               pts[ind3, j] - \
               pts[ind4, j] - \
               pts[ind7, j] - \
               pts[ind19, j] + \
               pts[ind16, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm(e0)*vector_norm(e1)*vector_norm(e2))
    normjac = triple_product(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    return jac


cdef inline float hex_quad_qual_float(int64_t [::1] cells, int c,
                                      float [:, ::1] pts) nogil:
    cdef float jac = 1.1
    cdef float [3] e0
    cdef float [3] e1
    cdef float [3] e2
    cdef int i, j    
    cdef float normjac, tnorm
    
    # Store cell indices
    cdef int ind0 = cells[c + 0]
    cdef int ind1 = cells[c + 1]
    cdef int ind2 = cells[c + 2]
    cdef int ind3 = cells[c + 3]
    cdef int ind4 = cells[c + 4]
    cdef int ind5 = cells[c + 5]
    cdef int ind6 = cells[c + 6]
    cdef int ind7 = cells[c + 7]
    cdef int ind8 = cells[c + 8]
    cdef int ind9 = cells[c + 9]
    cdef int ind10 = cells[c + 10]
    cdef int ind11 = cells[c + 11]
    cdef int ind12 = cells[c + 12]
    cdef int ind13 = cells[c + 13]
    cdef int ind14 = cells[c + 14]
    cdef int ind15 = cells[c + 15]
    cdef int ind16 = cells[c + 16]
    cdef int ind17 = cells[c + 17]
    cdef int ind18 = cells[c + 18]
    cdef int ind19 = cells[c + 19]
    
    # Node 0
    for j in range(3):
        e0[j]  = 4*pts[ind8, j] - pts[ind1, j] - 3*pts[ind0, j]
        e1[j]  = 4*pts[ind11, j] - pts[ind3, j] - 3*pts[ind0, j]
        e2[j]  = 4*pts[ind16, j] - pts[ind4, j] - 3*pts[ind0, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm_float(e0)*vector_norm_float(e1)*vector_norm_float(e2))
    normjac = triple_product_float(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 1
    for j in range(3):
        e0[j]  = 4*pts[ind9, j] - pts[ind2, j] - 3*pts[ind1, j]
        e1[j]  = 4*pts[ind8, j] - pts[ind0, j] - 3*pts[ind1, j]
        e2[j]  = 4*pts[ind17, j] - pts[ind5, j] - 3*pts[ind1, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm_float(e0)*vector_norm_float(e1)*vector_norm_float(e2))
    normjac = triple_product_float(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 2
    for j in range(3):
        e0[j]  = 4*pts[ind10, j] - pts[ind3, j] - 3*pts[ind2, j]
        e1[j]  = 4*pts[ind9, j] - pts[ind1, j] - 3*pts[ind2, j]
        e2[j]  = 4*pts[ind18, j] - pts[ind6, j] - 3*pts[ind2, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm_float(e0)*vector_norm_float(e1)*vector_norm_float(e2))
    normjac = triple_product_float(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 3
    for j in range(3):
        e0[j]  = 4*pts[ind11, j] - pts[ind0, j] - 3*pts[ind3, j]
        e1[j]  = 4*pts[ind10, j] - pts[ind2, j] - 3*pts[ind3, j]
        e2[j]  = 4*pts[ind19, j] - pts[ind7, j] - 3*pts[ind3, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm_float(e0)*vector_norm_float(e1)*vector_norm_float(e2))
    normjac = triple_product_float(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 4
    for j in range(3):
        e0[j]  = 4*pts[ind15, j] - pts[ind7, j] - 3*pts[ind4, j]
        e1[j]  = 4*pts[ind12, j] - pts[ind5, j] - 3*pts[ind4, j]
        e2[j]  = 4*pts[ind16, j] - pts[ind0, j] - 3*pts[ind4, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm_float(e0)*vector_norm_float(e1)*vector_norm_float(e2))
    normjac = triple_product_float(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 5
    for j in range(3):
        e0[j]  = 4*pts[ind12, j] - pts[ind4, j] - 3*pts[ind5, j]
        e1[j]  = 4*pts[ind13, j] - pts[ind6, j] - 3*pts[ind5, j]
        e2[j]  = 4*pts[ind17, j] - pts[ind1, j] - 3*pts[ind5, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm_float(e0)*vector_norm_float(e1)*vector_norm_float(e2))
    normjac = triple_product_float(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 6
    for j in range(3):
        e0[j]  = 4*pts[ind13, j] - pts[ind5, j] - 3*pts[ind6, j]
        e1[j]  = 4*pts[ind14, j] - pts[ind7, j] - 3*pts[ind6, j]
        e2[j]  = 4*pts[ind18, j] - pts[ind2, j] - 3*pts[ind6, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm_float(e0)*vector_norm_float(e1)*vector_norm_float(e2))
    normjac = triple_product_float(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 7
    for j in range(3):
        e0[j]  = 4*pts[ind14, j] - pts[ind6, j] - 3*pts[ind7, j]
        e1[j]  = 4*pts[ind15, j] - pts[ind4, j] - 3*pts[ind7, j]
        e2[j]  = 4*pts[ind19, j] - pts[ind3, j] - 3*pts[ind7, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm_float(e0)*vector_norm_float(e1)*vector_norm_float(e2))
    normjac = triple_product_float(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 8
    for j in range(3):
        e0[j] = pts[ind1, j] - pts[ind0, j]
    
        e1[j] = 2*pts[ind9, j] + \
             2*pts[ind11, j] - \
               pts[ind0, j] - \
               pts[ind1, j] - \
               pts[ind2, j] - \
               pts[ind3, j] - \
               pts[ind8, j] + \
               pts[ind10, j]
    
        e2[j] = 2*pts[ind16, j] + \
             2*pts[ind17, j] - \
               pts[ind0, j] - \
               pts[ind1, j] - \
               pts[ind4, j] - \
               pts[ind5, j] - \
               pts[ind8, j] + \
               pts[ind12, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm_float(e0)*vector_norm_float(e1)*vector_norm_float(e2))
    normjac = triple_product_float(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 9
    for j in range(3):
        e0[j] = pts[ind2, j] - pts[ind1, j]
    
        e1[j] = 2*pts[ind8, j] + \
             2*pts[ind10, j] - \
               pts[ind0, j] - \
               pts[ind1, j] - \
               pts[ind2, j] - \
               pts[ind3, j] - \
               pts[ind9, j] + \
               pts[ind11, j]
    
        e2[j] = 2*pts[ind17, j] + \
             2*pts[ind18, j] - \
               pts[ind1, j] - \
               pts[ind2, j] - \
               pts[ind5, j] - \
               pts[ind6, j] - \
               pts[ind9, j] + \
               pts[ind13, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm_float(e0)*vector_norm_float(e1)*vector_norm_float(e2))
    normjac = triple_product_float(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 10
    for j in range(3):
        e0[j] = pts[ind3, j] - pts[ind2, j]
    
        e1[j] = 2*pts[ind9, j] + \
             2*pts[ind11, j] - \
               pts[ind0, j] - \
               pts[ind1, j] - \
               pts[ind2, j] - \
               pts[ind3, j] - \
               pts[ind10, j] + \
               pts[ind8, j]
    
        e2[j] = 2*pts[ind18, j] + \
             2*pts[ind19, j] - \
               pts[ind2, j] - \
               pts[ind3, j] - \
               pts[ind6, j] - \
               pts[ind7, j] - \
               pts[ind10, j] + \
               pts[ind14, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm_float(e0)*vector_norm_float(e1)*vector_norm_float(e2))
    normjac = triple_product_float(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 11
    for j in range(3):
        e0[j] = pts[ind3, j] - pts[ind0, j]
    
        e1[j] = 2*pts[ind16, j] + \
             2*pts[ind19, j] - \
               pts[ind0, j] - \
               pts[ind3, j] - \
               pts[ind4, j] - \
               pts[ind7, j] - \
               pts[ind11, j] + \
               pts[ind15, j]
    
        e2[j] = 2*pts[ind8, j] + \
             2*pts[ind10, j] - \
               pts[ind0, j] - \
               pts[ind1, j] - \
               pts[ind2, j] - \
               pts[ind3, j] - \
               pts[ind11, j] + \
               pts[ind9, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm_float(e0)*vector_norm_float(e1)*vector_norm_float(e2))
    normjac = triple_product_float(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 12
    for j in range(3):
        e0[j] = pts[ind4, j] - pts[ind5, j]
    
        e1[j] = 2*pts[ind13, j] + \
             2*pts[ind15, j] - \
               pts[ind4, j] - \
               pts[ind5, j] - \
               pts[ind6, j] - \
               pts[ind7, j] - \
               pts[ind12, j] + \
               pts[ind14, j]
    
        e2[j] = 2*pts[ind16, j] + \
             2*pts[ind17, j] - \
               pts[ind0, j] - \
               pts[ind1, j] - \
               pts[ind4, j] - \
               pts[ind5, j] - \
               pts[ind12, j] + \
               pts[ind8, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm_float(e0)*vector_norm_float(e1)*vector_norm_float(e2))
    normjac = triple_product_float(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 13
    for j in range(3):
        e0[j] = pts[ind5, j] - pts[ind6, j]
    
        e1[j] = 2*pts[ind12, j] + \
             2*pts[ind14, j] - \
               pts[ind4, j] - \
               pts[ind5, j] - \
               pts[ind6, j] - \
               pts[ind7, j] - \
               pts[ind13, j] + \
               pts[ind15, j]
    
        e2[j] = 2*pts[ind17, j] + \
             2*pts[ind18, j] - \
               pts[ind1, j] - \
               pts[ind2, j] - \
               pts[ind5, j] - \
               pts[ind6, j] - \
               pts[ind13, j] + \
               pts[ind9, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm_float(e0)*vector_norm_float(e1)*vector_norm_float(e2))
    normjac = triple_product_float(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 14
    for j in range(3):
        e0[j] = pts[ind6, j] - pts[ind7, j]
    
        e1[j] = 2*pts[ind13, j] + \
             2*pts[ind15, j] - \
               pts[ind4, j] - \
               pts[ind5, j] - \
               pts[ind6, j] - \
               pts[ind7, j] - \
               pts[ind14, j] + \
               pts[ind12, j]
    
        e2[j] = 2*pts[ind18, j] + \
             2*pts[ind19, j] - \
               pts[ind2, j] - \
               pts[ind3, j] - \
               pts[ind6, j] - \
               pts[ind7, j] - \
               pts[ind14, j] + \
               pts[ind10, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm_float(e0)*vector_norm_float(e1)*vector_norm_float(e2))
    normjac = triple_product_float(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 15
    for j in range(3):
        e0[j] = pts[ind7, j] - pts[ind4, j]
    
        e1[j] = 2*pts[ind14, j] + \
             2*pts[ind12, j] - \
               pts[ind4, j] - \
               pts[ind5, j] - \
               pts[ind6, j] - \
               pts[ind7, j] - \
               pts[ind15, j] + \
               pts[ind13, j]
    
        e2[j] = 2*pts[ind16, j] + \
             2*pts[ind19, j] - \
               pts[ind0, j] - \
               pts[ind3, j] - \
               pts[ind4, j] - \
               pts[ind7, j] - \
               pts[ind15, j] + \
               pts[ind11, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm_float(e0)*vector_norm_float(e1)*vector_norm_float(e2))
    normjac = triple_product_float(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 16
    for j in range(3):
        e0[j] = pts[ind0, j] - pts[ind4, j]
    
        e1[j] = 2*pts[ind11, j] + \
             2*pts[ind15, j] - \
               pts[ind0, j] - \
               pts[ind3, j] - \
               pts[ind4, j] - \
               pts[ind7, j] - \
               pts[ind16, j] + \
               pts[ind19, j]
    
        e2[j] = 2*pts[ind8, j] + \
             2*pts[ind12, j] - \
               pts[ind0, j] - \
               pts[ind1, j] - \
               pts[ind4, j] - \
               pts[ind5, j] - \
               pts[ind16, j] + \
               pts[ind17, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm_float(e0)*vector_norm_float(e1)*vector_norm_float(e2))
    normjac = triple_product_float(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 17
    for j in range(3):
        e0[j] = pts[ind1, j] - pts[ind5, j]
    
        e1[j] = 2*pts[ind8, j] + \
             2*pts[ind12, j] - \
               pts[ind0, j] - \
               pts[ind1, j] - \
               pts[ind4, j] - \
               pts[ind5, j] - \
               pts[ind17, j] + \
               pts[ind16, j]
    
        e2[j] = 2*pts[ind9, j] + \
             2*pts[ind13, j] - \
               pts[ind1, j] - \
               pts[ind2, j] - \
               pts[ind5, j] - \
               pts[ind6, j] - \
               pts[ind17, j] + \
               pts[ind18, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm_float(e0)*vector_norm_float(e1)*vector_norm_float(e2))
    normjac = triple_product_float(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 18
    for j in range(3):
        e0[j] = pts[ind2, j] - pts[ind6, j]
    
        e1[j] = 2*pts[ind9, j] + \
             2*pts[ind13, j] - \
               pts[ind1, j] - \
               pts[ind2, j] - \
               pts[ind5, j] - \
               pts[ind6, j] - \
               pts[ind18, j] + \
               pts[ind17, j]
    
        e2[j] = 2*pts[ind10, j] + \
             2*pts[ind14, j] - \
               pts[ind2, j] - \
               pts[ind3, j] - \
               pts[ind6, j] - \
               pts[ind7, j] - \
               pts[ind18, j] + \
               pts[ind19, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm_float(e0)*vector_norm_float(e1)*vector_norm_float(e2))
    normjac = triple_product_float(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    # Node 19
    for j in range(3):
        e0[j] = pts[ind3, j] - pts[ind7, j]
    
        e1[j] = 2*pts[ind10, j] + \
             2*pts[ind14, j] - \
               pts[ind2, j] - \
               pts[ind3, j] - \
               pts[ind6, j] - \
               pts[ind7, j] - \
               pts[ind19, j] + \
               pts[ind18, j]
    
        e2[j] = 2*pts[ind11, j] + \
             2*pts[ind15, j] - \
               pts[ind0, j] - \
               pts[ind3, j] - \
               pts[ind4, j] - \
               pts[ind7, j] - \
               pts[ind19, j] + \
               pts[ind16, j]
    
    # normalize the determinant of the jacobian
    tnorm = (vector_norm_float(e0)*vector_norm_float(e1)*vector_norm_float(e2))
    normjac = triple_product_float(e1, e2, e0)/tnorm
    
    # Track minimum jacobian
    if normjac < jac:
        jac = normjac
    
    return jac


cdef inline double volume_weg(double [8][3] cell_points) nogil:
    """ Compute the volume of a wedge element """
    cdef double[3] e0, e1, e2

    vector_sub(cell_points[0], cell_points[1], e0)
    vector_sub(cell_points[1], cell_points[2], e1)
    vector_sub(cell_points[2], cell_points[4], e2)
    cdef double volume = triple_product(e0, e1, e2)
    
    vector_sub(cell_points[0], cell_points[4], e0)
    vector_sub(cell_points[4], cell_points[2], e1)
    vector_sub(cell_points[2], cell_points[5], e2)
    volume += triple_product(e0, e1, e2)
    
    vector_sub(cell_points[4], cell_points[5], e1)
    vector_sub(cell_points[5], cell_points[3], e2)
    volume += triple_product(e0, e1, e2)
    return dabs(volume)


cdef inline float volume_weg_float(float [8][3] cell_points) nogil:
    """ Compute the volume of a wedge element """
    cdef float[3] e0, e1, e2

    vector_sub_float(cell_points[0], cell_points[1], e0)
    vector_sub_float(cell_points[1], cell_points[2], e1)
    vector_sub_float(cell_points[2], cell_points[4], e2)
    cdef float volume = triple_product_float(e0, e1, e2)
    
    vector_sub_float(cell_points[0], cell_points[4], e0)
    vector_sub_float(cell_points[4], cell_points[2], e1)
    vector_sub_float(cell_points[2], cell_points[5], e2)
    volume += triple_product_float(e0, e1, e2)
    
    vector_sub_float(cell_points[4], cell_points[5], e1)
    vector_sub_float(cell_points[5], cell_points[3], e2)
    volume += triple_product_float(e0, e1, e2)
    return fabs(volume)


cdef inline double volume_hex(double [8][3] points) nogil:
    """
    Compute the volume of a hexahedral element

    From:
    Efficient computation of volume of hexahedral cells
    http://www.osti.gov/scitech/servlets/purl/632793
    """
    cdef int i
    cdef double vol
    cdef double[8] x
    cdef double[8] y
    cdef double[8] z

    # inefficiency
    for i in range(8):
        x[i] = points[i][0]
        y[i] = points[i][1]
        z[i] = points[i][2]

    vol = \
         (x[6]-x[0])*((y[3]-y[0])*(z[2]-z[7]) - (y[2]-y[7])*(z[3]-z[0])) + \
         (x[3]-x[0])*((y[2]-y[7])*(z[6]-z[0]) - (y[6]-y[0])*(z[2]-z[7])) + \
         (x[2]-x[7])*((y[6]-y[0])*(z[3]-z[0]) - (y[3]-y[0])*(z[6]-z[0])) + \
         + \
         (x[6]-x[0])*((y[4]-y[0])*(z[7]-z[5]) - (y[7]-y[5])*(z[4]-z[0])) + \
         (x[4]-x[0])*((y[7]-y[5])*(z[6]-z[0]) - (y[6]-y[0])*(z[7]-z[5])) + \
         (x[7]-x[5])*((y[6]-y[0])*(z[4]-z[0]) - (y[4]-y[0])*(z[6]-z[0])) + \
         + \
         (x[6]-x[0])*((y[1]-y[0])*(z[5]-z[2]) - (y[5]-y[2])*(z[1]-z[0])) + \
         (x[1]-x[0])*((y[5]-y[2])*(z[6]-z[0]) - (y[6]-y[0])*(z[5]-z[2])) + \
         (x[5]-x[2])*((y[6]-y[0])*(z[1]-z[0]) - (y[1]-y[0])*(z[6]-z[0]))

    return dabs(vol)*0.125


cdef inline float volume_hex_float(float [8][3] points) nogil:
    """
    Compute the volume of a hexahedral element

    From:
    Efficient computation of volume of hexahedral cells
    http://www.osti.gov/scitech/servlets/purl/632793
    """
    cdef int i
    cdef float vol
    cdef float[8] x
    cdef float[8] y
    cdef float[8] z

    # inefficiency
    for i in range(8):
        x[i] = points[i][0]
        y[i] = points[i][1]
        z[i] = points[i][2]

    vol = \
         (x[6]-x[0])*((y[3]-y[0])*(z[2]-z[7]) - (y[2]-y[7])*(z[3]-z[0])) + \
         (x[3]-x[0])*((y[2]-y[7])*(z[6]-z[0]) - (y[6]-y[0])*(z[2]-z[7])) + \
         (x[2]-x[7])*((y[6]-y[0])*(z[3]-z[0]) - (y[3]-y[0])*(z[6]-z[0])) + \
         + \
         (x[6]-x[0])*((y[4]-y[0])*(z[7]-z[5]) - (y[7]-y[5])*(z[4]-z[0])) + \
         (x[4]-x[0])*((y[7]-y[5])*(z[6]-z[0]) - (y[6]-y[0])*(z[7]-z[5])) + \
         (x[7]-x[5])*((y[6]-y[0])*(z[4]-z[0]) - (y[4]-y[0])*(z[6]-z[0])) + \
         + \
         (x[6]-x[0])*((y[1]-y[0])*(z[5]-z[2]) - (y[5]-y[2])*(z[1]-z[0])) + \
         (x[1]-x[0])*((y[5]-y[2])*(z[6]-z[0]) - (y[6]-y[0])*(z[5]-z[2])) + \
         (x[5]-x[2])*((y[6]-y[0])*(z[1]-z[0]) - (y[1]-y[0])*(z[6]-z[0]))

    return fabs(vol)*0.125


def cell_quality(int64_t [::1] cells, int64_t [::1] offset,
                 uint8 [::1] celltypes, double [:, ::1] pts, int as_linear=0):
    """    
    Returns the minimum scaled jacobian for each cell given a cell array from
    a vtk unstructured grid.  Accounts for midside nodes.
    
    Parameters
    ----------
    cells : int64_t [::1]
        Cell array from VTK

    offset :

    celltypes :

    pts : double [:, ::1]
        Points of the unstructured grid.

    as_linear : int
        Checks only the linear cell quality.

    Returns
    -------
    quality : np.ndarray
        Minimum scaled jacobian for each valid cell.
    
    Notes
    -----
    Checks the quality of the following cell types:

       - VTK_HEXAHEDRON
       - VTK_PYRAMID
       - VTK_TETRA
       - VTK_WEDGE
       - VTK_QUADRATIC_TETRA
       - VTK_QUADRATIC_PYRAMID
       - VTK_QUADRATIC_WEDGE
       - VTK_QUADRATIC_HEXAHEDRON

    """
    cdef int i
    cdef int ncells = celltypes.size
    cdef double [::1] quality = np.empty(ncells)
    cdef uint8 celltype

    for i in prange(ncells, nogil=True, num_threads=MAX_THREADS):
        celltype = celltypes[i]
        if celltype == VTK_HEXAHEDRON:
            quality[i] = hex_lin_qual(cells, offset[i] + 1, pts)

        elif celltype == VTK_TETRA:
            quality[i] = tet_lin_qual(cells, offset[i] + 1, pts)

        elif celltype == VTK_PYRAMID:
            quality[i] = pyr_lin_qual(cells, offset[i] + 1, pts)

        elif celltype == VTK_WEDGE:
            quality[i] = weg_lin_qual(cells, offset[i] + 1, pts)

        elif celltype == VTK_QUADRATIC_HEXAHEDRON:
            if as_linear:
                quality[i] = hex_lin_qual(cells, offset[i] + 1, pts)
            else:
                quality[i] = hex_quad_qual(cells, offset[i] + 1, pts)

        elif celltype == VTK_QUADRATIC_TETRA:
            if as_linear:
                quality[i] = tet_lin_qual(cells, offset[i] + 1, pts)
            else:
                quality[i] = tet_quad_qual(cells, offset[i] + 1, pts)

        elif celltype == VTK_QUADRATIC_PYRAMID:
            if as_linear:
                quality[i] = pyr_lin_qual(cells, offset[i] + 1, pts)
            else:
                quality[i] = pyr_quad_qual(cells, offset[i] + 1, pts)

        elif celltype == VTK_QUADRATIC_WEDGE:
            if as_linear:
                quality[i] = weg_lin_qual(cells, offset[i] + 1, pts)
            else:
                quality[i] = weg_quad_qual(cells, offset[i] + 1, pts)

        else:
            quality[i] = d_nan

    return np.asarray(quality)



def cell_quality_float(int64_t [::1] cells, int64_t [::1] offset,
                       uint8 [::1] celltypes, float [:, ::1] pts, int as_linear=0):
    """    
    Returns the minimum scaled jacobian for each cell given a cell
    array from a vtk unstructured grid.  Accounts for midside nodes.

    Parameters
    ----------
    cells : int64_t [::1]
        Cell array from VTK

    offset :

    celltypes :

    pts : float [:, ::1]
        Points of the unstructured grid.

    as_linear : int
        Checks only the linear cell quality.

    Returns
    -------
    quality : np.ndarray
        Minimum scaled jacobian for each valid cell.
    
    Notes
    -----
    Checks the quality of the following cell types:

       - VTK_HEXAHEDRON
       - VTK_PYRAMID
       - VTK_TETRA
       - VTK_WEDGE
       - VTK_QUADRATIC_TETRA
       - VTK_QUADRATIC_PYRAMID
       - VTK_QUADRATIC_WEDGE
       - VTK_QUADRATIC_HEXAHEDRON

    """
    cdef int i
    cdef int ncells = celltypes.size
    cdef float [::1] quality = np.empty(ncells, np.float32)
    cdef uint8 celltype

    for i in prange(ncells, nogil=True, num_threads=MAX_THREADS):
        celltype = celltypes[i]
        if celltype == VTK_HEXAHEDRON:
            quality[i] = hex_lin_qual_float(cells, offset[i] + 1, pts)

        elif celltype == VTK_TETRA:
            quality[i] = tet_lin_qual_float(cells, offset[i] + 1, pts)

        elif celltype == VTK_PYRAMID:
            quality[i] = pyr_lin_qual_float(cells, offset[i] + 1, pts)

        elif celltype == VTK_WEDGE:
            quality[i] = weg_lin_qual_float(cells, offset[i] + 1, pts)

        elif celltype == VTK_QUADRATIC_HEXAHEDRON:
            if as_linear:
                quality[i] = hex_lin_qual_float(cells, offset[i] + 1, pts)
            else:
                quality[i] = hex_quad_qual_float(cells, offset[i] + 1, pts)

        elif celltype == VTK_QUADRATIC_TETRA:
            if as_linear:
                quality[i] = tet_lin_qual_float(cells, offset[i] + 1, pts)
            else:
                quality[i] = tet_quad_qual_float(cells, offset[i] + 1, pts)

        elif celltype == VTK_QUADRATIC_PYRAMID:
            if as_linear:
                quality[i] = pyr_lin_qual_float(cells, offset[i] + 1, pts)
            else:
                quality[i] = pyr_quad_qual_float(cells, offset[i] + 1, pts)

        elif celltype == VTK_QUADRATIC_WEDGE:
            if as_linear:
                quality[i] = weg_lin_qual_float(cells, offset[i] + 1, pts)
            else:
                quality[i] = weg_quad_qual_float(cells, offset[i] + 1, pts)

        else:
            quality[i] = d_nan

    return np.asarray(quality)
