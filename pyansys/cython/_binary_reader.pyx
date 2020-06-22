# cython: embedsignature=True
# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True

import ctypes
import numpy as np

from libc.math cimport sqrt, fabs, sin, cos
from libc.stdio cimport (fopen, FILE, fclose, fread, fseek, SEEK_CUR,
                         ftell, SEEK_SET)
from libc.string cimport memcpy
from libc.stdint cimport int64_t
from libc.stdlib cimport malloc, free

# debug
from libc.stdio cimport printf


from cython.parallel import prange
ctypedef unsigned char uint8


cdef extern from "<iostream>" namespace "std" nogil:
     cdef cppclass ostream:
          ostream& write(const char*, int) except +
     cdef cppclass istream:
          istream& read(const char*, int) except +
     cdef cppclass ifstream(istream):
          ifstream(const char *, open_mode) except +


cdef extern from "<fstream>" namespace "std" nogil:          
     cdef cppclass filebuf:
          pass
        
     cdef cppclass fstream:
          void close()
          bint is_open()
          void open(const char*, open_mode)
          void open(const char&, open_mode)
          filebuf* rdbuf() const
          filebuf* rdbuf(filebuf* sb)

     cdef cppclass ifstream(istream):
          # void close()
          ifstream(const char*) except +
          ifstream(const char*, open_mode) except+

cdef extern from "<iostream>" namespace "std::ios_base" nogil:
     cdef cppclass open_mode:
          pass
     cdef open_mode binary


cdef extern from "numpy/npy_math.h" nogil:
    bint npy_isnan(double x)

cdef extern from 'binary_reader.h' nogil:
    void read_nodes(const char*, int64_t, int, int*, double*)
    void* read_record(const char*, int64_t, int*, int*, int*, int*)
    void read_record_stream(ifstream*, int64_t, void*, int*, int*, int*)


# VTK numbering for vtk cells
cdef uint8 VTK_EMPTY_CELL = 0
cdef uint8 VTK_VERTEX = 1
cdef uint8 VTK_LINE = 3

cdef uint8 VTK_TRIANGLE = 5
cdef uint8 VTK_QUAD = 9
cdef uint8 VTK_QUADRATIC_TRIANGLE = 22
cdef uint8 VTK_QUADRATIC_QUAD = 23

cdef uint8 VTK_TETRA = 10
cdef uint8 VTK_HEXAHEDRON = 12
cdef uint8 VTK_WEDGE = 13
cdef uint8 VTK_PYRAMID = 14
cdef uint8 VTK_QUADRATIC_TETRA = 24
cdef uint8 VTK_QUADRATIC_PYRAMID = 27
cdef uint8 VTK_QUADRATIC_WEDGE = 26
cdef uint8 VTK_QUADRATIC_HEXAHEDRON = 25

cdef double DEG2RAD = 0.017453292519943295

ctypedef fused index_type:
    int
    int64_t

ctypedef fused float_or_double:
    float
    double


###############################################################################
from libc.stdlib cimport free
from cpython cimport PyObject, Py_INCREF

import numpy as np  # Python-level symbols of numpy
cimport numpy as np  # C-level symbols of numpy

# Numpy must be initialized. When using numpy from C or Cython you must
# _always_ do that, or you will have segfaults
np.import_array()


cdef class ArrayWrapper:
    """Array wrapper class to deallocate our array when the Python
    object is deleted."""
    cdef void* data_ptr
    cdef int size
    cdef int my_dtype

    cdef set_data(self, int size, void* data_ptr, int my_dtype=0):
        """Set the data of the array.

        This cannot be done in the constructor as it must recieve C-level
        arguments.

        Parameters
        ----------
        size : int
            Length of the array

        data_ptr : void*
            Pointer to the data            
        """
        self.data_ptr = data_ptr
        self.size = size        
        self.my_dtype = my_dtype

    def __array__(self):
        """ Here we use the __array__ method, that is called when numpy
            tries to get an array from the object."""
        cdef np.npy_intp shape[1]
        shape[0] = <np.npy_intp> self.size
        # Create a 1D array, of length 'size'
        if self.my_dtype == 0:
            ndarray = np.PyArray_SimpleNewFromData(1, shape,
                                                   np.NPY_INT16, self.data_ptr)
        elif self.my_dtype == 1:
            ndarray = np.PyArray_SimpleNewFromData(1, shape,
                                                   np.NPY_INT32, self.data_ptr)
        elif self.my_dtype == 2:
            ndarray = np.PyArray_SimpleNewFromData(1, shape,
                                                   np.NPY_FLOAT32, self.data_ptr)
        else:
            ndarray = np.PyArray_SimpleNewFromData(1, shape,
                                                   np.NPY_FLOAT64, self.data_ptr)

        return ndarray

    def __dealloc__(self):
        """ Frees the array. This is called by Python when all the
        references to the object are gone. """
        free(<void*>self.data_ptr)


###############################################################################
# element result location pointers
cdef int PTR_ENS_IDX = 2
cdef int PTR_EUL_IDX = 9


cdef inline double get_double(char * array) nogil:
    cdef double result
    memcpy(&result, array, sizeof(result))
    return result


cdef inline double get_float(char * array) nogil:
    cdef float result
    memcpy(&result, array, sizeof(result))
    return result


cdef inline int get_int(char * array) nogil:
    cdef int result
    memcpy(&result, array, sizeof(result))
    return result


def load_nodes(filename, int ptr_loc, int nnod, double [:, ::1] nloc, 
              int [::1] nnum):
    """Wrapper for cpp function

    """    
    cdef bytes buf, flags_buf
    cdef bytes py_bytes = filename.encode()
    cdef char* c_filename = py_bytes
    read_nodes(c_filename, ptr_loc, nnod, &nnum[0], &nloc[0, 0])


def c_read_record(filename, int64_t ptr, int return_bufsize=0):
    """Read an ANSYS record and return a numpy array"""
    cdef bytes py_bytes = filename.encode()
    cdef char* c_filename = py_bytes

    cdef int prec_flag, type_flag, size, my_dtype, bufsize
    cdef void* c_ptr
    c_ptr = read_record(c_filename, ptr, &prec_flag, &type_flag, &size, &bufsize)
    cdef np.ndarray ndarray = wrap_array(c_ptr, size, type_flag, prec_flag)

    if return_bufsize:
        return ndarray, bufsize
    else:
        return ndarray


cdef np.ndarray wrap_array(void* c_ptr, int size, int type_flag, int prec_flag):
    """wrap a c array as a numpy array"""
    cdef int my_dtype

    if type_flag:
        if prec_flag:
            my_dtype = 0
        else:
            my_dtype = 1
    else:
        if prec_flag:
            my_dtype = 2
        else:
            my_dtype = 3

    # wrap c_array 
    array_wrapper = ArrayWrapper()
    array_wrapper.set_data(size, c_ptr, my_dtype)

    cdef np.ndarray ndarray
    ndarray = np.array(array_wrapper, copy=False)

    # Assign our object to the 'base' of the ndarray object
    ndarray.base = <PyObject*> array_wrapper

    # Increment the reference count, as the above assignement was done in
    # C, and Python does not know that there is this additional reference
    Py_INCREF(array_wrapper)

    return ndarray


def load_elements(filename, int64_t loc, int nelem, int64_t [::1] e_disp_table):
    """Load elements from an ansys result file.

    filename : str
        Filename containing the result file.

    loc : int64_t
        Pointer to the element table

    e_disp_table : int64_t [::1]
        Array containing pointers to the individual elements relative to ``loc``.

    The following is stored for each element
    0 - mat     - material reference number
    1 - type    - element type number
    2 - real    - real constant reference number
    3 - secnum  - section number
    4 - esys    - element coordinate system
    5 - death   - death flat (1 live, 0 dead)
    6 - solidm  - solid model reference
    7 - shape   - coded shape key
    8 - elnum   - element number
    9 - baseeid - base element number
    10 - NODES   - node numbers defining the element
    """
    cdef int i, j

    cdef int prec_flag, type_flag, size, bufsize
    cdef void* c_ptr

    cdef bytes py_bytes = filename.encode()
    cdef char* c_filename = py_bytes
    cdef int* element
    cdef short* s_element

    cdef int val, nread
    cdef int64_t elem_loc

    # elem connectivity and info (10 fields + maximum of 20 nodes per element)
    cdef int [::1] elem = np.empty(nelem*30, np.int32)
    cdef int [::1] elem_off = np.empty(nelem + 1, np.int32)

    cdef int c = 0  # cell position counter
    for i in range(nelem):
        # load element
        elem_loc = loc + e_disp_table[i]
        c_ptr = read_record(c_filename, elem_loc, &prec_flag, &type_flag,
                            &size, &bufsize)

        # start of the element
        elem_off[i] = c

        # read in entire element
        if prec_flag:
            s_element = <short*>c_ptr
            for j in range(size):
                elem[c + j] = s_element[j]
        else:
            element = <int*>c_ptr
            for j in range(size):
                elem[c + j] = element[j]
        c += size

    # add final position here for parser to know the size of the last element
    elem_off[nelem] = c

    return np.array(elem[:c]), np.array(elem_off)


def read_element_stress(filename, int64_t [::1] ele_ind_table, 
                        int64_t [::1] nodstr, int [::1] etype,
                        double [:, ::1] ele_data_arr, int nitem,
                        int [::1] element_type, int64_t ptr_off,
                        int as_global=1):
    """Read element results from ANSYS directly into a numpy array

    ele_ind_table : int64_t [::1]
        Pointer to the result header of an element relative to the
        result index.

    ptr_off : int
        ``ele_ind_table`` offset from the file head.

    as_global : int, optional
        Rotates stresses from the element coordinate system to the global
        cartesian coordinate system.  Default True.
    """
    cdef bytes py_bytes = filename.encode()
    cdef char* c_filename = py_bytes
    cdef ifstream* binfile = new ifstream(c_filename, binary)

    cdef int i
    cdef int c = 0
    for i in range(len(ele_ind_table)):
        nnode_elem = nodstr[etype[i]]

        if ele_ind_table[i] != 0:
            read_element_result(binfile, ele_ind_table[i] + ptr_off,
                                PTR_ENS_IDX, nnode_elem, nitem,
                                &ele_data_arr[c, 0], element_type[i], as_global)
            c += nnode_elem
    

cdef inline int read_element_result(ifstream *binfile, int64_t ele_table,
                                    int result_index,
                                    int nnode_elem, int nitem, double *arr,
                                    int element_type, int as_global=1):
    """Populate array with results from a single element"""
    cdef int i, j, k, c, nitems
    cdef int [4096] pointers  # tmp array of pointers
    cdef int prec_flag, type_flag, size
    cdef int64_t ptr, eul_ptr
    cdef char [131072] tmp_data_buffer  # 2**17
    cdef double [512] euler_angles  # 8*3*20 --> 512
    cdef short* spointers = <short*>pointers

    # store elemenet element result pointers
    read_record_stream(binfile, ele_table, <void*>&pointers,
                       &prec_flag, &type_flag, &size)
    # expect size to be 25 here as of v19.1

    # always cast 
    if prec_flag:
        ptr = spointers[result_index]
        eul_ptr = spointers[PTR_EUL_IDX]
    else:
        ptr = pointers[result_index]
        eul_ptr = pointers[PTR_EUL_IDX]

    if ptr == 0:  # 0 means skip
        return 1
    if ptr < 0:  # negative pointer means missing data
        # skip this element
        for j in range(nnode_elem):
            for k in range(nitem):
                arr[j*nitem + k] = 0  # consider putting NAN instead
    else:
        # read the results evaluated at the integration points or nodes
        read_record_stream(binfile, ele_table + ptr, <void*>tmp_data_buffer,
                           &prec_flag, &type_flag, &size)

        # if size < 0:
        #     raise MemoryError('Negative array size')

        # copy to main array
        if prec_flag:
            for i in range(size):
                arr[i] = <double>(<float*>tmp_data_buffer)[i]
        else:
            # EFFICIENCY WARNING: we don't need to copy here
            for i in range(size):
                arr[i] = (<double*>tmp_data_buffer)[i]

        # rotate out of element coordinate system
        if as_global and eul_ptr > 0 and result_index == PTR_ENS_IDX:
            # read in euler angles
            read_record_stream(binfile, ele_table + eul_ptr,
                               <void*>tmp_data_buffer, &prec_flag, &type_flag, &size)

            # copy to main array
            if prec_flag:
                for i in range(size):
                    euler_angles[i] = <double>(<float*>tmp_data_buffer)[i]
            else:  # we don't need to copy here...
                for i in range(size):
                    euler_angles[i] = (<double*>tmp_data_buffer)[i]            

            if size == 3:
                # --For uniform reduced integration lower-order 
                # elements (e.g. PLANE182, KEYOPT(1)=1 and
                # SOLID185 KEYOPT(2)=1):
                # the angles are at the centroid and the number
                # of items is 3.
                # if element_type == 181 or element_type == 281:
                    # euler_rotate_shell(arr, euler_angles, nitem)
                # else:
                euler_rotate(arr, euler_angles, nitem, nnode_elem)
            else:
                for i in range(nnode_elem):
                    euler_rotate(&arr[i*nitem], &euler_angles[3*i], nitem, 1)
                # --For other formulations of lower-order 
                # elements (e.g. PLANE182 and SOLID185) and
                # the higher-order elements
                # (e.g. PLANE183, SOLID186, and SOLID187):
                # The number of items in this record is
                # (nodstr*3).

            # TODO: NOT IMPLEMENTED
            # --For layered solid elements, add NL values,
            # so that the number of items in this record 
            # is (nodstr*3)+NL.

    return 0


cdef inline void euler_rotate_shell(float_or_double *arr,
                                    float_or_double [64] eulerangles, int nitem) nogil:
    """Performs a 3-1-2 euler rotation given thxy, thyz, thzx in
    ``eulerangles``

    Acts on rows 0 - 3 relative to row

    Specific to shell181 elements

    # used sympy to generate these equations
    tensor = np.matrix([[s_xx, s_xy, s_xz], 
                        [s_xy, s_yy, s_yz], 
                        [s_xz, s_yz, s_zz]])

    # always zero for shell elements...
    s_xz = 0
    s_yz = 0
    s_zz = 0

    from sympy import Matrix, symbols

    c1, c2, c3, s1, s2, s3, s_xx, s_yy, s_xy = symbols('c1 c2 c3 s1 s2 s3 s_xx s_yy s_xy')
    tensor = np.matrix([[s_xx, s_xy, 0], [s_xy, s_yy, 0], [0, 0, 0]])
    

    R = Matrix([[c1*c3 - s1*s2*s3, s1*c3 + c1*s2*s3, -s3*c2],
                [-s1*c2, c1*c2, s2],
                [c1*s3 + s1*s2*c3, s1*s3 - c1*c3*s2, c2*c3]])

    ans = R.T*tensor*R
    """    
    cdef double s_xx, s_xy, s_yy
    cdef double c1 = cos(DEG2RAD*eulerangles[0])
    cdef double c2 = cos(DEG2RAD*eulerangles[1])
    cdef double c3 = cos(DEG2RAD*eulerangles[2])
    cdef double s1 = sin(DEG2RAD*eulerangles[0])
    cdef double s2 = sin(DEG2RAD*eulerangles[1])
    cdef double s3 = sin(DEG2RAD*eulerangles[2])

    cdef int i
    for i in range(4):
        # grab the element component stresses
        s_xx = arr[i*nitem + 0]
        s_yy = arr[i*nitem + 1]
        s_xy = arr[i*nitem + 3]
        # the rest are zero (no out of plane stress)

        arr[i*nitem + 0] = -c2*s1*(-c2*s1*s_yy + s_xy*(c1*c3 - s1*s2*s3)) + (c1*c3 - s1*s2*s3)*(-c2*s1*s_xy + s_xx*(c1*c3 - s1*s2*s3))
        arr[i*nitem + 1] = c1*c2*(c1*c2*s_yy + s_xy*(c1*s2*s3 + c3*s1)) + (c1*c2*s_xy + s_xx*(c1*s2*s3 + c3*s1))*(c1*s2*s3 + c3*s1)
        arr[i*nitem + 2] = -c2*s3*(-c2*s3*s_xx + s2*s_xy) + s2*(-c2*s3*s_xy + s2*s_yy)
        arr[i*nitem + 3] = c1*c2*(-c2*s1*s_yy + s_xy*(c1*c3 - s1*s2*s3)) + (c1*s2*s3 + c3*s1)*(-c2*s1*s_xy + s_xx*(c1*c3 - s1*s2*s3))
        arr[i*nitem + 4] = -c2*s3*(c1*c2*s_xy + s_xx*(c1*s2*s3 + c3*s1)) + s2*(c1*c2*s_yy + s_xy*(c1*s2*s3 + c3*s1))
        arr[i*nitem + 5] = -c2*s3*(-c2*s1*s_xy + s_xx*(c1*c3 - s1*s2*s3)) + s2*(-c2*s1*s_yy + s_xy*(c1*c3 - s1*s2*s3))


cdef inline void euler_rotate(float_or_double *arr,
                              float_or_double [64] eulerangles, int nitem,
                              int n_node):
    """Performs a 3-1-2 euler rotation given thxy, thyz, thzx in
    ``eulerangles`` on the stress values in ``arr``

    Notes
    -----
    Used sympy to generate these equations
    import numpy as np
    from sympy import Matrix, symbols
    c1, c2, c3, s1, s2, s3 = symbols('c1 c2 c3 s1 s2 s3')
    s_xx, s_xy, s_yy, s_xz, s_yz, s_zz = symbols('s_xx s_xy s_yy s_xz s_yz s_zz')

    tensor = np.matrix([[s_xx, s_xy, s_xz],
                        [s_xy, s_yy, s_yz],
                        [s_xz, s_yz, s_zz]])

    # from: https://www.simutechgroup.com/tips-and-tricks/fea-articles/286-fea-tips-tricks-ansys-rotation-convention
    R = Matrix([[c1*c3 - s1*s2*s3, s1*c3 + c1*s2*s3, -s3*c2],
                [-s1*c2, c1*c2, s2],
                [c1*s3 + s1*s2*c3, s1*s3 - c1*c3*s2, c2*c3]])

    ans = R.T*tensor*R


    print('XX', ans[0, 0])
    print('YY', ans[1, 1])
    print('ZZ', ans[2, 2])

    print('XY', ans[0, 1])
    print('YZ', ans[1, 2])
    print('XZ', ans[0, 2])
    """    
    cdef double s_xx, s_xy, s_yy, s_xz, s_yz, s_zz
    cdef double c1 = cos(DEG2RAD*eulerangles[0])
    cdef double c2 = cos(DEG2RAD*eulerangles[1])
    cdef double c3 = cos(DEG2RAD*eulerangles[2])
    cdef double s1 = sin(DEG2RAD*eulerangles[0])
    cdef double s2 = sin(DEG2RAD*eulerangles[1])
    cdef double s3 = sin(DEG2RAD*eulerangles[2])

    # rotate each node in the element
    cdef int i
    for i in range(n_node):
        # grab the node component stresses
        s_xx = arr[i*nitem + 0]
        s_yy = arr[i*nitem + 1]
        s_zz = arr[i*nitem + 2]
        s_xy = arr[i*nitem + 3]
        s_yz = arr[i*nitem + 4]
        s_xz = arr[i*nitem + 5]

        # store rotated component stresses 
        # XX
        arr[i*nitem + 0] = -c2*s1*(-c2*s1*s_yy + s_xy*(c1*c3 - s1*s2*s3) + s_yz*(c1*s3 + c3*s1*s2)) + (c1*c3 - s1*s2*s3)*(-c2*s1*s_xy + s_xx*(c1*c3 - s1*s2*s3) + s_xz*(c1*s3 + c3*s1*s2)) + (c1*s3 + c3*s1*s2)*(-c2*s1*s_yz + s_xz*(c1*c3 - s1*s2*s3) + s_zz*(c1*s3 + c3*s1*s2))

        # YY
        arr[i*nitem + 1] = c1*c2*(c1*c2*s_yy + s_xy*(c1*s2*s3 + c3*s1) + s_yz*(-c1*c3*s2 + s1*s3)) + (-c1*c3*s2 + s1*s3)*(c1*c2*s_yz + s_xz*(c1*s2*s3 + c3*s1) + s_zz*(-c1*c3*s2 + s1*s3)) + (c1*s2*s3 + c3*s1)*(c1*c2*s_xy + s_xx*(c1*s2*s3 + c3*s1) + s_xz*(-c1*c3*s2 + s1*s3))

        # ZZ
        arr[i*nitem + 2] = c2*c3*(c2*c3*s_zz - c2*s3*s_xz + s2*s_yz) - c2*s3*(c2*c3*s_xz - c2*s3*s_xx + s2*s_xy) + s2*(c2*c3*s_yz - c2*s3*s_xy + s2*s_yy)

        # XY
        arr[i*nitem + 3] = c1*c2*(-c2*s1*s_yy + s_xy*(c1*c3 - s1*s2*s3) + s_yz*(c1*s3 + c3*s1*s2)) + (-c1*c3*s2 + s1*s3)*(-c2*s1*s_yz + s_xz*(c1*c3 - s1*s2*s3) + s_zz*(c1*s3 + c3*s1*s2)) + (c1*s2*s3 + c3*s1)*(-c2*s1*s_xy + s_xx*(c1*c3 - s1*s2*s3) + s_xz*(c1*s3 + c3*s1*s2))

        # YZ
        arr[i*nitem + 4] = c2*c3*(c1*c2*s_yz + s_xz*(c1*s2*s3 + c3*s1) + s_zz*(-c1*c3*s2 + s1*s3)) - c2*s3*(c1*c2*s_xy + s_xx*(c1*s2*s3 + c3*s1) + s_xz*(-c1*c3*s2 + s1*s3)) + s2*(c1*c2*s_yy + s_xy*(c1*s2*s3 + c3*s1) + s_yz*(-c1*c3*s2 + s1*s3))

        # XZ
        arr[i*nitem + 5] = c2*c3*(-c2*s1*s_yz + s_xz*(c1*c3 - s1*s2*s3) + s_zz*(c1*s3 + c3*s1*s2)) - c2*s3*(-c2*s1*s_xy + s_xx*(c1*c3 - s1*s2*s3) + s_xz*(c1*s3 + c3*s1*s2)) + s2*(-c2*s1*s_yy + s_xy*(c1*c3 - s1*s2*s3) + s_yz*(c1*s3 + c3*s1*s2))


def read_nodal_values(filename, uint8 [::1] celltypes,
                      int64_t [::1] ele_ind_table,
                      int64_t [::1] offsets,
                      int64_t [::1] cells,
                      int nitems,
                      int npoints,
                      int [::1] nodstr,
                      int [::1] etype,
                      int [::1] element_type,
                      int result_index,
                      int64_t ptr_off):
    """Read nodal results from ANSYS directly into a numpy array

    element_type : int [::1] np.ndarray
        Array of ANSYS element types.

    ptr_off : int64_t
        Pointer offset

    result_index : int
        EMS - 0 : misc. data
        ENF - 1 : nodal forces
        ENS - 2 : nodal stresses
        ENG - 3 : volume and energies
        EGR - 4 : nodal gradients
        EEL - 5 : elastic strains
        EPL - 6 : plastic strains
        ECR - 7 : creep strains
        ETH - 8 : thermal strains
        EUL - 9 : euler angles
        EFX - 10 : nodal fluxes
        ELF - 11 : local forces
        EMN - 12 : misc. non-sum values
        ECD - 13 : element current densities
        ENL - 14 : nodal nonlinear data
        EHC - 15 : calculated heat
        EPT - 16 : element temperatures
        ESF - 17 : element surface stresses
        EDI - 18 : diffusion strains
        ETB - 19 : ETABLE items
        ECT - 20 : contact data
        EXY - 21 : integration point locations
        EBA - 22 : back stresses
        ESV - 23 : state variables
        MNL - 24 : material nonlinear record
    """
    cdef int64_t i, j, k, ind, nread, offset
    cdef int64_t ncells = ele_ind_table.size

    cdef bytes py_bytes = filename.encode()
    cdef char* c_filename = py_bytes
    cdef ifstream* binfile = new ifstream(c_filename, binary)

    cdef int [::1] ncount = np.zeros(npoints, ctypes.c_int32)

    # point data
    cdef double [:, ::1] data = np.zeros((npoints, nitems), np.float64)

    # temp buffer to hold data read from element
    cdef double [:, ::1] bufferdata = np.zeros((20, nitems), np.float64)

    cdef int64_t ele_table, nnode_elem
    cdef int ptr_result, skip
    cdef int c = 0
    cdef uint8 celltype
    for i in range(ncells):

        # read element data
        nnode_elem = nodstr[etype[i]]
        if ele_ind_table[i] == 0:  # element contains no data
            continue
        else:
            skip = read_element_result(binfile, ele_ind_table[i] + ptr_off,
                                       result_index, nnode_elem, nitems,
                                       &bufferdata[0, 0], element_type[i])
            if skip:
                continue

        # Get the nodes in the element
        celltype = celltypes[i]
        offset = offsets[i] + 1

        if celltype == VTK_LINE:  # untested
            read_element(cells, offset, ncount, data, bufferdata, nitems, 2)
        elif celltype == VTK_TRIANGLE:  # untested
            read_element(cells, offset, ncount, data, bufferdata, nitems, 3)
        elif celltype == VTK_QUAD or celltype == VTK_QUADRATIC_QUAD:
            read_element(cells, offset, ncount, data, bufferdata, nitems, 4)
        elif celltype == VTK_HEXAHEDRON:
            read_element(cells, offset, ncount, data, bufferdata, nitems, 8)
        elif celltype == VTK_PYRAMID:
            read_element(cells, offset, ncount, data, bufferdata, nitems, 5)
        elif celltype == VTK_TETRA:  # dependent on element type
            if nodstr[etype[i]] == 4:
                read_element(cells, offset, ncount, data, bufferdata, nitems, 4)
            else:
                read_tetrahedral(cells, offset, ncount, data, bufferdata, nitems)
        elif celltype == VTK_WEDGE:
            read_wedge(cells, offset, ncount, data, bufferdata, nitems)
    del binfile

    return np.asarray(data), np.asarray(ncount)


# indices of a wedge must be reordered (see _parser.store_weg)
cdef int64_t [6] wedge_ind
wedge_ind[0] = 2
wedge_ind[1] = 1
wedge_ind[2] = 0
wedge_ind[3] = 6
wedge_ind[4] = 5
wedge_ind[5] = 4

cdef inline void read_wedge(int64_t [::1] cells, int64_t index, int [::1] ncount,
                           float_or_double [:, ::1] data,
                            float_or_double [:, ::1] bufferdata,
                           int nitems) nogil:
    """
    [0, 1, 2, 2, 3, 4, 5, 5]
    [0, 1, 2,  , 4, 5, 6,  ]
    """
    cdef int64_t i, j, cell, idx
    cdef int nread = nitems*8
    
    for i in range(6):
        cell = cells[index + i]
        ncount[cell] += 1
        idx = wedge_ind[i]
        for j in range(nitems):
            data[cell, j] += bufferdata[idx, j]


# indices of a 186 tetrahedral must be reordered (see _parser.StoreWeg)
cdef int64_t [6] tet_ind
tet_ind[0] = 0
tet_ind[1] = 1
tet_ind[2] = 2
tet_ind[3] = 4

cdef inline void read_tetrahedral(int64_t [::1] cells, int64_t index, int [::1] ncount,
                                  float_or_double [:, ::1] data, float_or_double [:, ::1] bufferdata,
                                  int nitems) nogil:
    """
    # see documentation at _parser.StoreTet
    """
    cdef int64_t i, j, cell, idx
    cdef int nread

    nread = nitems*5

    for i in range(4):
        cell = cells[index + i]
        ncount[cell] += 1
        idx = tet_ind[i]
        for j in range(nitems):
            data[cell, j] += bufferdata[idx, j]


cdef inline void read_element(int64_t [::1] cells, int64_t index, int [::1] ncount,
                              float_or_double [:, ::1] data,
                              float_or_double [:, ::1] bufferdata,
                              int nitems, int nnode) nogil:
    """
    Reads a generic element type in a linear fashion.  Works for:
    Hexahedron 95 or 186
    Pyramid 95 or 186
    Tetrahedral 187
    """
    cdef int64_t i, j, cell, idx

    for i in range(nnode):
        cell = cells[index + i]
        ncount[cell] += 1
        for j in range(nitems):
            data[cell, j] += bufferdata[i, j]


def read_array(filename, int ptr, int nterm, int neqn, int [::1] const):
    """Reads stiffness or mass matrices from ANSYS fortran files

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
        
    const : numpy int array
        If DOF is fixed

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
    """

    cdef int i, j, k, ind
    cdef bytes buf
    with open(filename, "rb") as f:
        f.seek(ptr*4)
        buf = f.read((neqn*6 + nterm*3)*4)

    cdef char * p = buf # python to c character array pointer
    cdef int loc = 0 # location long buffer

    # Number of terms is the number of terms stored in the upper triangle
    cdef int [::1] krow = np.empty(nterm, np.int32)
    cdef int [::1] kcol = np.empty(nterm, np.int32)
    cdef double [::1] kdata = np.empty(nterm)

    cdef int [::1] kdiag = np.empty(neqn, np.int32)
    cdef double [::1] kdata_diag = np.empty(neqn)

    cdef int c = 0 # index counter
    cdef int d = 0 # data counter
    cdef int c_diag = 0 # diag counter
    cdef int row, col, nitems, intval
    cdef double val

    for i in range(neqn):
        col = i

        # number of items to read
        nitems = get_int(&p[loc]); loc += 4
        loc += 4

        # Read indices
        for j in range(nitems):
            # get row number
            row = get_int(&p[loc]) - 1; loc += 4 # convert to c indexing

            if row < col:
                krow[c] = row
                kcol[c] = col
            else:
                krow[c] = col
                kcol[c] = row
            c += 1

        loc += 12
            
        # Read data
        for j in range(nitems):
            # Store data
            kdata[d] = get_double(&p[loc]); loc += 8
            d += 1

        # seek past end of data
        loc += 4

    return np.asarray(krow)[:c], np.asarray(kcol)[:c], np.asarray(kdata)[:c]


def sort_nodal_eqlv(int neqn, int [::1] neqv, int [::1] ndof):
    """Read in full file details required for the assembly of the mass
    and stiffness matrices.

    The reference arrays are sorted by default, though this increases
    the bandwidth of the mass and stiffness matrices.

    Parameters
    ----------
    neqn : int
        Number of equations in full file.

    ndof : int [::1]
        Degrees of freedom for each node.

    neqv : int [::1]
        Nodal equivalance array.

    Returns
    -------
    dof_ref: numpy np.int32 array
        Sorted degree of freedom reference array.
        
    index_arr : numpy np.int32 array
        Index array to sort rows and columns.

    """
    cdef int i, j, ind

    # create sorting array
    cdef int nnodes = ndof.size
    cdef int [::1] cumdof = np.empty(nnodes, np.int32)
    cdef int csum = 0
    for i in range(nnodes):
        cumdof[i] = csum
        csum += ndof[i]
        
    cdef int [::1] s_neqv_dof = np.empty(neqn, np.int32)
    cdef int [::1] nref = np.empty(neqn, np.int32)
    cdef int [::1] dref = np.empty(neqn, np.int32)
    cdef int c = 0
    cdef int val
    for i in range(nnodes):
        val = neqv[i]
        for j in range(ndof[i]):
            nref[c] = val
            dref[c] = j
            c += 1

    # sort nodal equivalance array
    cdef int [::1] sidx = np.argsort(neqv).astype(np.int32)
    cdef int [::1] ndof_sort = np.empty(nnodes, np.int32)
    for i in range(nnodes):
        ndof_sort[i] = ndof[sidx[i]]

    cdef int d = 0
    # create an index array.  This tells the array readers where
    # to place each row and col when it's sorted
    cdef int [::1] index_arr = np.empty(neqn, np.int32)
    for i in range(nnodes):
        ind = sidx[i]
        c = cumdof[ind]
        for j in range(ndof[ind]):
            s_neqv_dof[d] = c + j
            index_arr[c + j] = d
            d += 1

    # sort node and dof references
    cdef int [:, ::1] dof_ref = np.empty((neqn, 2), np.int32)
    for i in range(neqn):
        ind = s_neqv_dof[i]
        dof_ref[i, 0] = nref[ind]
        dof_ref[i, 1] = dref[ind]

    return np.asarray(dof_ref), np.asarray(index_arr), np.asarray(nref), \
           np.asarray(dref)


def tensor_arbitrary(double [:, ::1] stress, double [:, :] trans):
    """Rotates a 3D stress tensor by theta about the Z axis

    Notes:
    -----
    Used
    from sympy import Matrix, symbols
    s_xx, s_yy, s_zz, s_xy, s_yz, s_xz = symbols('s_xx s_yy s_zz s_xy s_yz s_xz')
    c0, c1, c2, c3, c4, c5, c6, c7, c8 = symbols('c0 c1 c2 c3 c4 c5 c6 c7 c8')
    
    R = Matrix([[c0, c1, c2], [c3, c4, c5], [c6, c7, c8]])
    tensor = Matrix([[s_xx, s_xy, s_xz], [s_xy, s_yy, s_yz], [s_xz, s_yz, s_zz]])
    R*tensor*R.T
    """
    cdef int nnode = stress.shape[0]
    cdef int i

    cdef uint8 [::1] isnan = np.zeros(nnode, np.uint8)
    cdef double s_xx, s_yy, s_zz, s_xy, s_yz, s_xz
    cdef double c0 = trans[0, 0]
    cdef double c1 = trans[0, 1]
    cdef double c2 = trans[0, 2]
    cdef double c3 = trans[1, 0]
    cdef double c4 = trans[1, 1]
    cdef double c5 = trans[1, 2]
    cdef double c6 = trans[2, 0]
    cdef double c7 = trans[2, 1]
    cdef double c8 = trans[2, 2]

    cdef double r0, r1, r2, r3, r4, r5, r6, r7, r8

    for i in range(nnode):
        s_xx = stress[i, 0]
        if npy_isnan(s_xx):  # skip
            isnan[i] = 1
        else:
            s_yy = stress[i, 1]
            s_zz = stress[i, 2]
            s_xy = stress[i, 3]
            s_yz = stress[i, 4]
            s_xz = stress[i, 5]

        r0 = c0*(c0*s_xx + c1*s_xy + c2*s_xz) + c1*(c0*s_xy + c1*s_yy + c2*s_yz) + c2*(c0*s_xz + c1*s_yz + c2*s_zz)

        r1 = c3*(c0*s_xx + c1*s_xy + c2*s_xz) + c4*(c0*s_xy + c1*s_yy + c2*s_yz) + c5*(c0*s_xz + c1*s_yz + c2*s_zz)

        r4 = c3*(c3*s_xx + c4*s_xy + c5*s_xz) + c4*(c3*s_xy + c4*s_yy + c5*s_yz) + c5*(c3*s_xz + c4*s_yz + c5*s_zz)

        r5 = c6*(c3*s_xx + c4*s_xy + c5*s_xz) + c7*(c3*s_xy + c4*s_yy + c5*s_yz) + c8*(c3*s_xz + c4*s_yz + c5*s_zz)

        r6 = c0*(c6*s_xx + c7*s_xy + c8*s_xz) + c1*(c6*s_xy + c7*s_yy + c8*s_yz) + c2*(c6*s_xz + c7*s_yz + c8*s_zz)

        r8 = c6*(c6*s_xx + c7*s_xy + c8*s_xz) + c7*(c6*s_xy + c7*s_yy + c8*s_yz) + c8*(c6*s_xz + c7*s_yz + c8*s_zz)

        stress[i, 0] = r0
        stress[i, 1] = r4
        stress[i, 2] = r8
        stress[i, 3] = r1
        stress[i, 4] = r5
        stress[i, 5] = r6

    return np.asarray(isnan, np.bool)


def tensor_rotate_z(double [:, :] stress, float theta_z):
    """Rotates a 3D stress tensor by theta about the Z axis

    Notes:
    -----
    Used 
    from sympy import Matrix, symbols
    c, s, s_xx, s_yy, s_zz, s_xy, s_yz, s_xz = symbols('c s s_xx s_yy s_zz s_xy s_yz s_xz')

    R = Matrix([[c, -s, 0], [s, c, 0], [0, 0, 1]])
    tensor = Matrix([[s_xx, s_xy, s_xz], [s_xy, s_yy, s_yz], [s_xz, s_yz, s_zz]])
    R*tensor*R.T
    """
    cdef int nnode = stress.shape[0]
    cdef int i
    cdef uint8 [::1] isnan = np.zeros(nnode, np.uint8)
    cdef double c, s, s_xx, s_yy, s_zz, s_xy, s_yz, s_xz

    c = cos(theta_z)
    s = sin(theta_z)

    for i in range(nnode):
        s_xx = stress[i, 0]
        if npy_isnan(s_xx):
            isnan[i] = 1
        else:
            s_yy = stress[i, 1]
            s_zz = stress[i, 2]
            s_xy = stress[i, 3]
            s_yz = stress[i, 4]
            s_xz = stress[i, 5]

        stress[i, 0] = c*(c*s_xx - s*s_xy) - s*(c*s_xy - s*s_yy)
        stress[i, 1] = c*(c*s_yy + s*s_xy) + s*(c*s_xy + s*s_xx)
        stress[i, 2] = s_zz
        stress[i, 3] = c*(c*s_xy - s*s_yy) + s*(c*s_xx - s*s_xy)
        stress[i, 4] = c*s_yz + s*s_xz
        stress[i, 5] = c*s_xz - s*s_yz

    return np.asarray(isnan, dtype=np.bool)


def compute_principal_stress(double [:, ::1] stress):
    """Returns the principal stresses based on component stresses.

    Parameters
    ----------
    stress : numpy.ndarray (double)
        Stresses at Sx Sy Sz Sxy Syz Sxz averaged at each corner node.

    Returns
    -------
    pstress : numpy.ndarray
        Principal stresses, stress intensity, and equivalant stress.
        [sigma1, sigma2, sigma3, sint, seqv]

    Notes
    -----
    ANSYS equivalant of:
    PRNSOL, S, PRIN

    Which returns:
    S1, S2, S3 principal stresses, SINT stress intensity, and SEQV
    equivalent stress.
    """
    # reshape the stress array into 3x3 stress tensor arrays
    cdef int nnode = stress.shape[0]
    cdef double [:, :, ::1] stress_tensor = np.empty((nnode, 3, 3), np.float64)
    cdef double s_xx, x_yy, s_zz, s_xy, s_yz, s_xz
    cdef int i

    cdef uint8 [::1] isnan = np.zeros(nnode, np.uint8)

    for i in range(nnode):
        s_xx = stress[i, 0]
        if npy_isnan(s_xx):
            s_xx = 0
            s_yy = 0
            s_zz = 0
            s_xy = 0
            s_yz = 0
            s_xz = 0
            isnan[i] = 1
        else:
            s_yy = stress[i, 1]
            s_zz = stress[i, 2]
            s_xy = stress[i, 3]
            s_yz = stress[i, 4]
            s_xz = stress[i, 5]

        # populate lower triangle of stress tensor
        stress_tensor[i, 0, 0] = s_xx
        # stress_tensor[i, 0, 1] = s_xy
        # stress_tensor[i, 0, 2] = s_xz
        stress_tensor[i, 1, 0] = s_xy
        stress_tensor[i, 1, 1] = s_yy
        # stress_tensor[i, 1, 2] = s_yz
        stress_tensor[i, 2, 0] = s_xz
        stress_tensor[i, 2, 1] = s_yz
        stress_tensor[i, 2, 2] = s_zz

    # compute principle stresses
    # w =  np.linalg.eigvalsh(stress_tensor)  # default uses lower triangle
    # wrapped lapack libaray (slightly faster than above)$
    w = np.linalg._umath_linalg.eigvalsh_lo(stress_tensor)
    w[:, ::-1].sort(1)

    temp = np.empty((nnode, 5), np.float64)
    temp[:, :3] = w

    cdef double [:, ::1] pstress = temp
    cdef double p1, p2, p3, c1, c2, c3

    # compute stress intensity and von mises (equivalent) stress
    for i in range(nnode):
        p1 = pstress[i, 0]
        p2 = pstress[i, 1]
        p3 = pstress[i, 2]

        c1 = fabs(p1 - p2)
        c2 = fabs(p2 - p3)
        c3 = fabs(p3 - p1)

        if c1 > c2:
            if c1 > c3:
                pstress[i, 3] = c1
            else:
                pstress[i, 3] = c3
        else:
            if c2 > c3:
                pstress[i, 3] = c2
            else:
                pstress[i, 3] = c3

        pstress[i, 4] = sqrt(0.5*(c1**2 + c2**2 + c3**2))

    return np.asarray(pstress), np.asarray(isnan, np.bool)


def affline_transform(float_or_double [:, ::1] points, float_or_double [:, ::1] t):
    """ Rigidly transforms points based on a 4x4 transform matrix """
    cdef int npoints = points.shape[0]
    cdef int i, j
    cdef float_or_double x, y, z
    cdef float_or_double xnew, ynew, znew

    cdef float_or_double t00 = t[0, 0]
    cdef float_or_double t01 = t[0, 1]
    cdef float_or_double t02 = t[0, 2]
    cdef float_or_double t03 = t[0, 3]

    cdef float_or_double t10 = t[1, 0]
    cdef float_or_double t11 = t[1, 1]
    cdef float_or_double t12 = t[1, 2]
    cdef float_or_double t13 = t[1, 3]

    cdef float_or_double t20 = t[2, 0]
    cdef float_or_double t21 = t[2, 1]
    cdef float_or_double t22 = t[2, 2]
    cdef float_or_double t23 = t[2, 3]

    for i in prange(npoints, nogil=True):
        x = points[i, 0]
        y = points[i, 1]
        z = points[i, 2]

        points[i, 0] = t00*x + t01*y + t02*z + t03
        points[i, 1] = t10*x + t11*y + t12*z + t13
        points[i, 2] = t20*x + t21*y + t22*z + t23


cdef inline int cell_lookup(uint8 celltype) nogil:
    if celltype == VTK_HEXAHEDRON or celltype == VTK_QUADRATIC_HEXAHEDRON:
        return 8
    elif celltype == VTK_TETRA or celltype == VTK_QUADRATIC_TETRA:
        return 4
    elif celltype == VTK_PYRAMID or celltype == VTK_QUADRATIC_PYRAMID:
        return 5
    elif celltype == VTK_WEDGE or celltype == VTK_QUADRATIC_WEDGE:
        return 6


def cells_with_all_nodes(index_type [::1] offset, index_type [::1] cells,
                         uint8 [::1] celltypes, uint8 [::1] point_mask):
    """
    Updates mask of cells containing all points in the point indices
    or mask.
    """
    cdef int ncells = celltypes.size
    cdef uint8 celltype
    cdef int ncell_points, i, j
    cdef index_type cell_offset
    cdef uint8 [::1] cell_mask = np.ones(ncells, np.uint8)

    with nogil:
        for i in range(ncells):
            celltype = celltypes[i]
            ncell_points = cell_lookup(celltype)
            cell_offset = offset[i] + 1
            for j in range(cell_offset, cell_offset + ncell_points):
                if point_mask[cells[j]] != 1:
                    cell_mask[i] = 0

    return np.asarray(cell_mask, dtype=np.bool)


def cells_with_any_nodes(index_type [::1] offset, index_type [::1] cells,
                         uint8 [::1] celltypes, uint8 [::1] point_mask):
    """
    Updates mask of cells containing at least one point in the point
    indices or mask.
    """
    cdef int ncells = celltypes.size
    cdef uint8 celltype
    cdef int ncell_points
    cdef index_type cell_offset
    cdef int i, j

    cdef uint8 [::1] cell_mask = np.zeros(ncells, np.uint8)

    with nogil:
        for i in range(ncells):
            celltype = celltypes[i]
            ncell_points = cell_lookup(celltype)
            cell_offset = offset[i] + 1
            for j in range(cell_offset, cell_offset + ncell_points):
                if point_mask[cells[j]] == 1:
                    cell_mask[i] = 1
                    break

    return np.asarray(cell_mask, dtype=np.bool)


def midside_mask(uint8 [::1] celltypes, index_type [::1] cells,
                 index_type [::1] offset, int npoints):
    """Returns a mask of midside nodes

    Parameters
    ----------
    celltypes : uint8 [::1]
        VTK style celltype array

    cells : int32 or int64 [::1]
        VTK style cell array

    offset : int32 or int64 [::1]
        VTK style offset array

    npoints : int
        Number of points

    Returns
    -------
    mask : bool np.ndarray
        True when a midside node.
    """
    cdef uint8 [::1] mask = np.zeros(npoints, ctypes.c_uint8)
    cdef int i, j, c
    cdef int ncells = celltypes.size
    cdef uint8 celltype

    for i in range(ncells):
        # get start location of each cell
        c = offset[i] + 1
        celltype = celltypes[i]
    
        if celltype == VTK_QUADRATIC_TETRA:
            for j in range(c + 4, c + 10):
                mask[cells[j]] = 1

        elif celltype == VTK_QUADRATIC_PYRAMID:
            for j in range(c + 5, c + 13):
                mask[cells[j]] = 1

        elif celltype == VTK_QUADRATIC_WEDGE:
            for j in range(c + 6, c + 15):
                mask[cells[j]] = 1

        elif celltype == VTK_QUADRATIC_HEXAHEDRON:   
            for j in range(c + 8, c + 20):
                mask[cells[j]] = 1

    # return as a bool array without copying
    return np.asarray(mask).view(np.bool)
