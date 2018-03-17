from libc.stdint cimport int32_t, int64_t

cdef inline double HexLinJac(int64_t [::1] cellarr, int c, double [:, ::1] pts) nogil

