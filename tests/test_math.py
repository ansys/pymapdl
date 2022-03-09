"""Test APDL Math functionality"""
import os
import re
from shutil import copy

import numpy as np
import pytest
from scipy import sparse

from ansys.mapdl.core.errors import ANSYSDataTypeError
import ansys.mapdl.core.math as apdl_math

# skip entire module unless HAS_GRPC
pytestmark = pytest.mark.skip_grpc


@pytest.fixture(scope="module")
def mm(mapdl):
    return mapdl.math


def test_ones(mm):
    v = mm.ones(10)
    assert v.size == 10
    assert v[0] == 1


def test_rand(mm):
    w = mm.rand(10)
    assert w.size == 10


def test_asarray(mm):
    v = mm.ones(10)
    assert np.allclose(v.asarray(), np.ones(10))


def test_add(mm):
    v = mm.ones(10)
    w = mm.ones(10)
    z = v + w
    assert np.allclose(z.asarray(), 2)


def test_norm(mm):
    v = mm.ones(10)
    assert np.isclose(v.norm(), np.linalg.norm(v))
    assert np.isclose(mm.norm(v), v.norm())


def test_inplace_add(mm):
    v = mm.ones(10)
    w = mm.ones(10)
    w += v
    assert w[0] == 2


def test_inplace_mult(mm):
    v = mm.ones(10)
    v *= 2
    assert v[0] == 2


def test_set_vec_large(mm):
    # send a vector larger than the gRPC size limit of 4 MB
    sz = 1000000
    a = np.random.random(1000000)  # 7.62 MB (as FLOAT64)
    assert a.nbytes > 4 * 1024**2
    ans_vec = mm.set_vec(a)
    assert a[sz - 1] == ans_vec[sz - 1]
    assert np.allclose(a, ans_vec.asarray())


def test_dot(mm):
    a = np.arange(10000, dtype=np.float)
    b = np.arange(10000, dtype=np.float)
    np_rst = a.dot(b)

    vec_a = mm.set_vec(a)
    vec_b = mm.set_vec(b)
    assert np.allclose(vec_a.dot(vec_b), np_rst)
    assert np.allclose(mm.dot(vec_a, vec_b), np_rst)


def test_invalid_dtype(mm):
    with pytest.raises(ANSYSDataTypeError):
        mm.vec(10, dtype=np.uint8)


def test_vec_from_name(mm):
    vec0 = mm.vec(10)
    vec1 = mm.vec(name=vec0.id)
    assert np.allclose(vec0, vec1)


def test_vec__mul__(mm):
    # version check must be performed at runtime
    if mm._server_version[1] >= 4:
        a = mm.vec(10)
        b = mm.vec(10)
        assert np.allclose(a * b, np.asarray(a) * np.asarray(b))

        with pytest.raises(ValueError):
            mm.vec(10) * mm.vec(11)

        with pytest.raises(TypeError):
            mm.vec(10) * np.ones(10)


def test_numpy_max(mm):
    apdl_vec = mm.vec(10, init="rand")
    assert np.isclose(apdl_vec.asarray().max(), np.max(apdl_vec))


def test_shape(mm):
    shape = (10, 8)
    m1 = mm.rand(*shape)
    assert m1.shape == shape


def test_matrix(mm):
    sz = 5000
    mat = sparse.random(sz, sz, density=0.05, format="csr")
    assert mat.data.nbytes // 1024**2 > 4, "Must test over gRPC message limit"

    name = "TMP_MATRIX"
    ans_mat = mm.matrix(mat, name)
    assert ans_mat.id == name

    mat_back = ans_mat.asarray()
    assert np.allclose(mat.data, mat_back.data)
    assert np.allclose(mat.indices, mat_back.indices)
    assert np.allclose(mat.indptr, mat_back.indptr)


def test_matrix_fail(mm):
    mat = sparse.random(10, 10, density=0.05, format="csr")

    with pytest.raises(ValueError, match='":" is not permitted'):
        mm.matrix(mat, "my:mat")

    with pytest.raises(TypeError):
        mm.matrix(mat.astype(np.int8))


def test_matrix_addition(mm):
    m1 = mm.rand(10, 10)
    m2 = mm.rand(10, 10)
    m3 = m1 + m2
    assert np.allclose(m1.asarray() + m2.asarray(), m3.asarray())


def test_mul(mm):
    m1 = mm.rand(10, 10)
    w = mm.rand(10)
    with pytest.raises(AttributeError):
        m1 * w


# test kept for the eventual inclusion of mult
# def test_matrix_mult(mm):
#     m1 = mm.rand(10, 10)
#     w = mm.rand(10)
#     v = m1.w
#     assert np.allclose(w.asarray() @ m1.asarray(), v.asarray())

#     m1 = mm.rand(10, 10)
#     m2 = mm.rand(10, 10)
#     m3 = m1*m2
#     assert np.allclose(m1.asarray() @ m2.asarray(), m3.asarray())


def test_getitem(mm):
    size_i, size_j = (3, 3)
    mat = mm.rand(size_i, size_j)
    np_mat = mat.asarray()

    for i in range(size_i):
        vec = mat[i]
        for j in range(size_j):
            # recall that MAPDL uses fortran order
            assert vec[j] == np_mat[j, i]


def test_load_stiff_mass(mm, cube_solve, tmpdir):
    k = mm.stiff()
    m = mm.mass()
    assert k.shape == m.shape


def test_load_stiff_mass_different_location(mm, cube_solve, tmpdir):
    full_files = mm._mapdl.download("*.full")
    assert os.path.exists(full_files[0])
    full_path = os.path.join(os.getcwd(), full_files[0])
    copy(full_path, tmpdir)
    fname_ = os.path.join(tmpdir, full_files[0])
    assert os.path.exists(fname_)

    k = mm.stiff(fname=fname_)
    m = mm.mass(fname=fname_)
    assert k.shape == m.shape
    assert all([each > 0 for each in k.shape])
    assert all([each > 0 for each in m.shape])


def test_load_stiff_mass_as_array(mm, cube_solve):
    k = mm.stiff(asarray=True)
    m = mm.mass(asarray=True)

    assert sparse.issparse(k)
    assert sparse.issparse(m)
    assert all([each > 0 for each in k.shape])
    assert all([each > 0 for each in m.shape])


def test_stiff_mass_as_array(mm, cube_solve):
    k = mm.stiff()
    m = mm.mass()

    k = k.asarray()
    m = m.asarray()

    assert sparse.issparse(k)
    assert sparse.issparse(m)
    assert all([each > 0 for each in k.shape])
    assert all([each > 0 for each in m.shape])


@pytest.mark.parametrize(
    "dtype_",
    [
        np.int64,
        np.double,
        pytest.param(np.complex64, marks=pytest.mark.xfail),
        pytest.param("Z", marks=pytest.mark.xfail),
        "D",
        pytest.param("dummy", marks=pytest.mark.xfail),
        pytest.param(np.int8, marks=pytest.mark.xfail),
    ],
)
def test_load_stiff_mass_different_dtype(mm, cube_solve, dtype_):
    # AnsMat object do not support dtype assignment, you need to convert them to array first.
    k = mm.stiff(asarray=True, dtype=dtype_)
    m = mm.mass(asarray=True, dtype=dtype_)

    if isinstance(dtype_, str):
        if dtype_ == "Z":
            dtype_ = np.complex_
        else:
            dtype_ = np.double

    assert sparse.issparse(k)
    assert sparse.issparse(m)
    assert all([each > 0 for each in k.shape])
    assert all([each > 0 for each in m.shape])
    assert k.dtype == dtype_
    assert m.dtype == dtype_

    k = mm.stiff(dtype=dtype_)
    m = mm.mass(dtype=dtype_)

    k = k.asarray(dtype=dtype_)
    m = m.asarray(dtype=dtype_)

    assert sparse.issparse(k)
    assert sparse.issparse(m)
    assert all([each > 0 for each in k.shape])
    assert all([each > 0 for each in m.shape])
    assert k.dtype == dtype_
    assert m.dtype == dtype_


def test_load_matrix_from_file_incorrect_mat_id(mm, cube_solve):
    with pytest.raises(
        ValueError, match=r"The 'mat_id' parameter supplied.*is not allowed."
    ):
        mm.load_matrix_from_file(fname="file.full", mat_id="DUMMY")


def test_mat_from_name(mm):
    mat0 = mm.mat(10, 10)
    mat1 = mm.mat(name=mat0.id)
    assert np.allclose(mat0, mat1)


def test_mat_from_name_sparse(mm):
    scipy_mat = sparse.random(5, 5, density=1, format="csr")
    mat0 = mm.matrix(scipy_mat)
    mat1 = mm.mat(name=mat0.id)
    assert np.allclose(mat0, mat1)


def test_mat_invalid_dtype(mm):
    with pytest.raises(ValueError):
        mm.mat(10, 10, dtype=np.uint8)


def test_mat_invalid_init(mm):
    with pytest.raises(ValueError, match="Invalid init method"):
        mm.mat(10, 10, init="foo")


def test_solve(mm, cube_solve):
    k = mm.stiff()
    m = mm.mass()

    nev = 10
    a = mm.mat(k.nrow, nev)
    ev = mm.eigs(nev, k, m, phi=a)
    assert ev.size == nev


# alternative solve using math.solve
def test_solve_alt(mm, cube_solve):
    k = mm.stiff()
    b = mm.rand(k.nrow)
    eig_val = apdl_math.solve(k, b)
    assert eig_val.size == k.nrow


def test_solve_eigs_km(mapdl, mm, cube_solve):
    mapdl.post1()
    resp = mapdl.set("LIST")
    w_n = np.array(re.findall(r"\s\d*\.\d\s", resp), np.float32)

    k = mm.stiff()
    m = mm.mass()
    vec = mm.eigs(w_n.size, k, m, fmin=1)
    eigval = vec.asarray()
    assert np.allclose(w_n, eigval, atol=0.1)


def test_solve_py(mapdl, mm, cube_solve):
    mapdl.post1()
    resp = mapdl.set("LIST")
    w_n = np.array(re.findall(r"\s\d*\.\d\s", resp), np.float32)

    # load by default from file.full
    k = mm.stiff()
    m = mm.mass()

    # convert to numpy
    k_py = k.asarray()
    m_py = m.asarray()

    mapdl.clear()
    my_stiff = mm.matrix(k_py, triu=True)
    my_mass = mm.matrix(m_py, triu=True)

    nmode = w_n.size
    a = mm.mat(my_stiff.nrow, nmode)  # for eigenvectors
    vec = mm.eigs(nmode, my_stiff, my_mass, phi=a, fmin=1)
    eigval = vec.asarray()
    assert np.allclose(w_n, eigval, atol=0.1)


def test_dense_solver(mm):
    dim = 1000
    m2 = mm.rand(dim, dim)
    m3 = m2.copy()
    solver = mm.factorize(m2)

    v = mm.ones(dim)
    solver.solve(v)
    # TODO: we need to verify this works


def test_solve_py(mapdl, mm, cube_solve):
    rhs0 = mm.get_vec()
    rhs1 = mm.rhs()
    assert np.allclose(rhs0, rhs1)


def test_get_vector(mm):
    vec = mm.ones(10)
    arr = vec.asarray()
    assert np.allclose(arr, 1)


def test_vector_add(mm):
    vec0 = mm.ones(10)
    vec1 = mm.ones(10)
    assert np.allclose(vec0 + vec1, mm.add(vec0, vec1))


def test_vector_subtract(mm):
    vec0 = mm.ones(10)
    vec1 = mm.ones(10)
    assert np.allclose(vec0 - vec1, mm.subtract(vec0, vec1))


def test_vector_neg_index(mm):
    vec = mm.ones(10)
    with pytest.raises(ValueError):
        vec[-1]


def test_vec_itruediv(mm):
    vec = mm.ones(10)
    vec /= 2
    assert np.allclose(vec, 0.5)


def test_vec_const(mm):
    vec = mm.ones(10)
    vec.const(2)
    assert np.allclose(vec, 2)


@pytest.mark.parametrize("pname", ["vector", "my_vec"])
@pytest.mark.parametrize("vec", [np.random.random(10), [1, 2, 3, 4]])
def test_set_vector(mm, vec, pname):
    ans_vec = mm.set_vec(vec, pname)
    assert np.allclose(ans_vec.asarray(), vec)
    assert "APDLMath Vector Size" in repr(ans_vec)
    assert "" in str(vec[0])[:4]  # output from *PRINT


def test_set_vector_catch(mm):

    with pytest.raises(ValueError, match='":" is not permitted'):
        mm.set_vec(np.ones(10), "my:vec")

    with pytest.raises(TypeError):
        mm.set_vec(np.ones(10, dtype=np.int16))

    with pytest.raises(TypeError):
        mm.set_vec(np.array([1, 2, 3], np.uint8))


def test_get_dense(mm):
    ans_mat = mm.ones(10, 10)
    assert np.allclose(ans_mat.asarray(), 1)

    ans_mat = mm.zeros(10, 10)
    assert np.allclose(ans_mat.asarray(), 0)


def test_zeros_vec(mm):
    assert isinstance(mm.zeros(10), apdl_math.AnsVec)


def test_get_sparse(mm):
    k = mm.stiff()
    matrix = k.asarray()
    assert isinstance(matrix, sparse.csr.csr_matrix)
    assert np.any(matrix.data)


def test_copy(mm):
    k = mm.stiff()
    kcopy = k.copy()
    assert np.allclose(k, kcopy)


def test_sparse_repr(mm):
    k = mm.stiff()
    assert "Sparse APDLMath Matrix" in repr(k)


def test_invalid_matrix_size(mm):
    mat = sparse.random(10, 9, density=0.05, format="csr")
    with pytest.raises(ValueError):
        mm.matrix(mat, "NUMPY_MAT")


def test_transpose(mm):
    mat = sparse.random(5, 5, density=1, format="csr")
    apdl_mat = mm.matrix(mat)
    apdl_mat_t = apdl_mat.T
    assert np.allclose(apdl_mat.asarray().todense().T, apdl_mat_t.asarray().todense())


def test_dense(mm):
    # version check must be performed at runtime
    if mm._server_version[1] >= 4:
        # test if a APDLMath object can treated as an array
        array = np.random.random((5, 5))
        apdl_mat = mm.matrix(array)
        assert isinstance(apdl_mat, apdl_math.AnsMat)
        assert np.allclose(array, apdl_mat)

        with pytest.raises(TypeError):
            apdl_mat = mm.matrix(array.astype(np.uint8))

        assert "Dense APDLMath Matrix" in repr(apdl_mat)

        # check transpose
        assert np.allclose(apdl_mat.T, array.T)

        # check dot (vector and matrix)
        ones = mm.ones(apdl_mat.nrow)
        assert np.allclose(apdl_mat.dot(ones), np.dot(array, np.ones(5)))
        assert np.allclose(apdl_mat.dot(apdl_mat), np.dot(array, array))


def test_invalid_sparse_type(mm):
    mat = sparse.random(10, 10, density=0.05, format="csr", dtype=np.uint8)
    with pytest.raises(TypeError):
        mm._send_sparse("pytest01", mat, False, None, 100)


def test_invalid_sparse_name(mm):
    mat = sparse.random(10, 10, density=0.05, format="csr", dtype=np.uint8)
    with pytest.raises(TypeError, match="must be a string"):
        mm.matrix(mat, name=1)


def test_invalid_init():
    with pytest.raises(TypeError):
        apdl_math.MapdlMath(None)


def test_free(mm):
    my_mat = mm.ones(10)
    mm.free()
    with pytest.raises(RuntimeError, match="This vector has been deleted"):
        my_mat.size


def test_repr(mm):
    assert mm._status == repr(mm)


def test_status(mm):
    mm.status()
