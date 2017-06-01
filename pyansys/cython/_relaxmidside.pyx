# cython: infer_types=True
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True
# cython: nonecheck=False

#==============================================================================
# Quadratic element relaxation functions
#==============================================================================
cdef inline void RelaxMid_Tet(long [::1] cellarr, int c, double [:, ::1] pts,
                              double rfac):
    """
    Resets the midside nodes of the tetrahedral starting at index c
    
    relaxation factor rfac
    
    midedge nodes between
    (0,1), (1,2), (2,0), (0,3), (1,3), and (2,3)
    
    """
    
    cdef int ind0 = cellarr[c + 0]
    cdef int ind1 = cellarr[c + 1]
    cdef int ind2 = cellarr[c + 2]
    cdef int ind3 = cellarr[c + 3]
    cdef int ind4 = cellarr[c + 4]
    cdef int ind5 = cellarr[c + 5]
    cdef int ind6 = cellarr[c + 6]
    cdef int ind7 = cellarr[c + 7]
    cdef int ind8 = cellarr[c + 8]
    cdef int ind9 = cellarr[c + 9]

    cdef int j

    for j in range(3):
        pts[ind4, j] = pts[ind4, j]*(1 - rfac) + (pts[ind0, j] + pts[ind1, j])*0.5*rfac
        pts[ind5, j] = pts[ind5, j]*(1 - rfac) + (pts[ind1, j] + pts[ind2, j])*0.5*rfac
        pts[ind6, j] = pts[ind6, j]*(1 - rfac) + (pts[ind2, j] + pts[ind0, j])*0.5*rfac
        pts[ind7, j] = pts[ind7, j]*(1 - rfac) + (pts[ind0, j] + pts[ind3, j])*0.5*rfac
        pts[ind8, j] = pts[ind8, j]*(1 - rfac) + (pts[ind1, j] + pts[ind3, j])*0.5*rfac
        pts[ind9, j] = pts[ind9, j]*(1 - rfac) + (pts[ind2, j] + pts[ind3, j])*0.5*rfac


cdef inline void RelaxMid_Pyr(long [::1] cellarr, int c, double [:, ::1] pts,
                              double rfac):
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

    cdef int ind0 = cellarr[c + 0]
    cdef int ind1 = cellarr[c + 1]
    cdef int ind2 = cellarr[c + 2]
    cdef int ind3 = cellarr[c + 3]
    cdef int ind4 = cellarr[c + 4]
    cdef int ind5 = cellarr[c + 5]
    cdef int ind6 = cellarr[c + 6]
    cdef int ind7 = cellarr[c + 7]
    cdef int ind8 = cellarr[c + 8]
    cdef int ind9 = cellarr[c + 9]
    cdef int ind10= cellarr[c + 10]
    cdef int ind11= cellarr[c + 11]
    cdef int ind12= cellarr[c + 12]

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


cdef inline void RelaxMid_Weg(long [::1] cellarr, int c, double [:, ::1] pts,
                              double rfac):
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
    cdef int ind0 = cellarr[c + 0]
    cdef int ind1 = cellarr[c + 1]
    cdef int ind2 = cellarr[c + 2]
    cdef int ind3 = cellarr[c + 3]
    cdef int ind4 = cellarr[c + 4]
    cdef int ind5 = cellarr[c + 5]
    cdef int ind6 = cellarr[c + 6]
    cdef int ind7 = cellarr[c + 7]
    cdef int ind8 = cellarr[c + 8]
    cdef int ind9 = cellarr[c + 9]
    cdef int ind10= cellarr[c + 10]
    cdef int ind11= cellarr[c + 11]
    cdef int ind12= cellarr[c + 12]
    cdef int ind13= cellarr[c + 13]
    cdef int ind14= cellarr[c + 14]
    
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


cdef inline void RelaxMid_Hex(long [::1] cellarr, int c, double [:, ::1] pts,
                              double rfac):

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
    
    cdef int ind0 = cellarr[c + 0]
    cdef int ind1 = cellarr[c + 1]
    cdef int ind2 = cellarr[c + 2]
    cdef int ind3 = cellarr[c + 3]
    cdef int ind4 = cellarr[c + 4]
    cdef int ind5 = cellarr[c + 5]
    cdef int ind6 = cellarr[c + 6]
    cdef int ind7 = cellarr[c + 7]
    cdef int ind8 = cellarr[c + 8]
    cdef int ind9 = cellarr[c + 9]
    cdef int ind10= cellarr[c + 10]
    cdef int ind11= cellarr[c + 11]
    cdef int ind12= cellarr[c + 12]
    cdef int ind13= cellarr[c + 13]
    cdef int ind14= cellarr[c + 14]
    cdef int ind15= cellarr[c + 15]
    cdef int ind16= cellarr[c + 16]
    cdef int ind17= cellarr[c + 17]
    cdef int ind18= cellarr[c + 18]
    cdef int ind19= cellarr[c + 19]

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
           
           
def ResetMidside(long [::1] cellarr, double [:, ::1] pts):
    """
    SIGNATURE
    (long [::1] cellarr, double [:, ::1] pts)
    
    
    DESCRIPTION
    Resets positions of midside nodes to directly between edge nodes.
    
    
    INPUTS
    cellarr (long [::1])
        VTK formatted cell array
        
    pts (double [:, ::1])
        3D double point array.
        
        
    OUTPUTS
    NONE
    
    """

    cdef int c = 0
    cdef double cellarr_sz = cellarr.size

    while c < cellarr_sz:
    
        # Quadradic tetrahedral
        if cellarr[c] == 10:
            RelaxMid_Tet(cellarr, c + 1, pts, 1)
            
        # Quadradic pyramid
        elif cellarr[c] == 13:
            RelaxMid_Pyr(cellarr, c + 1, pts, 1)

        # Quadradic wedge       
        elif cellarr[c] == 15:
            RelaxMid_Weg(cellarr, c + 1, pts, 1)
                        
        # If quadradic hexahedral
        elif cellarr[c] == 20:   
            RelaxMid_Hex(cellarr, c + 1, pts, 1)    
                
        c += cellarr[c] + 1