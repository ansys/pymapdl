"""
Manipulate APDLMath vectors or dense matrices as NumPy Arrays
-------------------------------------------------------------
This example demonstrates how to exchange data between MAPDL and
Python via numpy arrays.

.. note::
    This example requires Ansys 2021R2.

"""
import numpy as np

from ansys.mapdl.core import launch_mapdl

# Start MAPDL as a service and disable all but error messages.
# Create an APDLMath object.
mapdl = launch_mapdl()
mm = mapdl.math


###############################################################################
# Convert an APDLMath Vector into an NumPy Array
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# First, allocate a APDLMath vector with 10 doubles

apdl_vec = mm.ones(10)
print(apdl_vec)

###############################################################################
# Then create an numpy array from this APDLMath vector.
#
# Note that these are two separate objects: memory is
# duplicated. Modifying one object does not modify its clone.
pv = apdl_vec.asarray()
print(pv)


###############################################################################
# You can then manipulate this numpy array with all existing numpy
# features
pv = (pv + 1) ** 2
print(pv)


###############################################################################
# Alternatively, the APDLMath object can be operated on directly with
# numpy with the numpy methods.
print(np.max(apdl_vec))
print(np.linalg.norm(apdl_vec))

###############################################################################
# Note that some methods have APDL correlaries, and these methods are
# more efficient if performed within MAPDL.
#
# For example, the norm method can be performed within MAPDL
print(apdl_vec.norm(), np.linalg.norm(apdl_vec))

###############################################################################
# Copy a NumPy Array to an APDLMath vector
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# You can push back any numpy vector or 2D array to MAPDL.  This
# creates a new APDLMath, which in this case is named ``'NewVec'``.
mm.set_vec(pv, "NewVec")

# verify this vector exists
print(mm)


###############################################################################
# Create a Python handle to this vector by specifying its name
v2 = mm.vec(name="NewVec")
print(v2)


###############################################################################
# Dense Numpy Arrays
# ~~~~~~~~~~~~~~~~~~
# The same features apply to dense APDL matrices and numpy arrays.
#
# Allow allocate an APDLMath Dense Matrix and convert it to a numpy
# array
apdl_mat = mm.rand(3, 3)
np_arr = apdl_mat.asarray()

assert np.allclose(apdl_mat, np_arr)
print(apdl_mat)
print(np_arr)


###############################################################################
# You can load numpy array to APDL with the matrix method
np_rand = np.random.random((4, 4))
ans_mat = mm.matrix(np_rand)

# print the autogenerated name of the this matrix
print(ans_mat.id)


###############################################################################
# Load this matrix from APDL and verify it is identical
from_ans = ans_mat.asarray()
print(np.allclose(from_ans, np_rand))


# stop mapdl
mapdl.exit()