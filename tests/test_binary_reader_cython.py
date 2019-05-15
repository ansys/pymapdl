import pyvista as pv
import vtk
from pyansys import _binary_reader
import numpy as np

# test stress tensors from
# Sx Sy Sz Sxy Syz Sxz
stress = np.array([ -2.21786547,  99.05487823, -11.42874718,  -4.69416809,
                    23.24783707,   0.4061397 ])

# known results when rotating about a vector with angle 20 degrees
# using apsg
stress_rot_x = np.array([-2.21786547, 71.18732452, 16.43880463, -4.54998303,
                         53.31763077, -1.22385347])

stress_rot_y = np.array([ -3.03427238,  99.05487823, -10.61234027,   3.54015345,
                          23.45132099,  -2.64919926])

stress_rot_z = np.array([ 12.64614819,  84.19086457, -11.42874718, -36.1443738 ,
                          21.9847289 ,  -7.56958209])


def test_tensor_rotation_x():
    transform = vtk.vtkTransform()
    transform.RotateX(20)
    transform.Update()
    rot_matrix = transform.GetMatrix()
    # rot_matrix.Invert()  # <-- this should not be necessary
    trans = pv.trans_from_matrix(rot_matrix)

    s_test = stress.copy().reshape(1, -1)
    _binary_reader.tensor_arbitrary(s_test, trans)
    assert np.allclose(s_test, stress_rot_x)


def test_tensor_rotation_y():
    transform = vtk.vtkTransform()
    transform.RotateY(20)
    transform.Update()
    rot_matrix = transform.GetMatrix()
    # rot_matrix.Invert()  # <-- this should not be necessary
    trans = pv.trans_from_matrix(rot_matrix)

    s_test = stress.copy().reshape(1, -1)
    _binary_reader.tensor_arbitrary(s_test, trans)
    assert np.allclose(s_test, stress_rot_y)


def test_tensor_rotation_z():
    transform = vtk.vtkTransform()
    transform.RotateZ(20)
    transform.Update()
    rot_matrix = transform.GetMatrix()
    # rot_matrix.Invert()  # <-- this should not be necessary
    trans = pv.trans_from_matrix(rot_matrix)

    s_test = stress.copy().reshape(1, -1)
    _binary_reader.tensor_arbitrary(s_test, trans)
    assert np.allclose(s_test, stress_rot_z)
