"""Contains the MapdlMath classes, allowing for math operations within
MAPDL from Python.  """
from enum import Enum
import os
import random
import string
from warnings import warn
import weakref

from ansys.api.mapdl.v0 import ansys_kernel_pb2 as anskernel
from ansys.api.mapdl.v0 import mapdl_pb2 as pb_types
from ansys.tools.versioning import requires_version
from ansys.tools.versioning.utils import server_meets_version
import numpy as np

from ansys.mapdl.core import VERSION_MAP
from ansys.mapdl.core.errors import MapdlRuntimeError, VersionError
from ansys.mapdl.core.misc import load_file

from .common_grpc import ANSYS_VALUE_TYPE, DEFAULT_CHUNKSIZE, DEFAULT_FILE_CHUNK_SIZE
from .errors import ANSYSDataTypeError, protect_grpc
from .mapdl_grpc import MapdlGrpc
from .parameters import interp_star_status

MYCTYPE = {
    np.int32: "I",
    np.int64: "L",
    np.single: "F",
    np.double: "D",
    np.complex64: "C",
    np.complex128: "Z",
}


NP_VALUE_TYPE = {value: key for key, value in ANSYS_VALUE_TYPE.items()}

# for windows LONG vs INT32
if os.name == "nt":
    NP_VALUE_TYPE[np.intc] = 1


def id_generator(size=6, chars=string.ascii_uppercase):
    """Generate a random string"""
    return "".join(random.choice(chars) for _ in range(size))


class ObjType(Enum):
    """Generic APDLMath Object ( Shared features between Vec Mat and
    Solver components"""

    GEN = 1
    VEC = 2
    DMAT = 3
    SMAT = 4


def get_nparray_chunks(name, array, chunk_size=DEFAULT_FILE_CHUNK_SIZE):
    """Serializes a numpy array into chunks"""
    stype = NP_VALUE_TYPE[array.dtype.type]
    arr_sz = array.size
    i = 0  # position counter
    byte_array = array.tobytes()
    while i < len(byte_array):
        piece = byte_array[i : i + chunk_size]
        chunk = anskernel.Chunk(payload=piece, size=len(piece))
        yield pb_types.SetVecDataRequest(
            vname=name, stype=stype, size=arr_sz, chunk=chunk
        )
        i += chunk_size


def get_nparray_chunks_mat(name, array, chunk_size=DEFAULT_FILE_CHUNK_SIZE):
    """Serializes a 2D numpy array into chunks

    Uses the ``SetMatDataRequest``

    """
    stype = NP_VALUE_TYPE[array.dtype.type]
    sh1 = array.shape[0]
    sh2 = array.shape[1]
    i = 0  # position counter
    byte_array = array.tobytes(order="F")
    while i < len(byte_array):
        piece = byte_array[i : i + chunk_size]
        chunk = anskernel.Chunk(payload=piece, size=len(piece))
        yield pb_types.SetMatDataRequest(
            mname=name, stype=stype, nrow=sh1, ncol=sh2, chunk=chunk
        )
        i += chunk_size


def list_allowed_dtypes():
    """Return a list of human readable Mapdl supported datatypes"""
    dtypes = list(NP_VALUE_TYPE.keys())
    if None in dtypes:
        dtypes.remove(None)
    return "\n".join([f"{dtype}" for dtype in dtypes])


class MapdlMath:
    """Abstract mapdl math class.  Created from a ``Mapdl`` instance.

    Examples
    --------
    Create an instance.

    >>> from ansys.mapdl.core import launch_mapdl
    >>> mapdl = launch_mapdl()
    >>> mm = mapdl.math

    Vector addition

    >>> v1 = mm.ones(10)
    >>> v2 = mm.ones(10)
    >>> v3 = v1 + v2

    Matrix multiplcation (not yet available)

    >>> v1 = mm.ones(10)
    >>> m1 = mm.rand(10, 10)
    >>> v2 = m1*v1

    """

    def __init__(self, mapdl):
        if not isinstance(mapdl, MapdlGrpc):
            raise TypeError("``mapdl`` must be a MapdlGrpc instance")
        self._mapdl_weakref = weakref.ref(mapdl)

    @property
    def _mapdl(self):
        """Return the weakly referenced instance of mapdl."""
        return self._mapdl_weakref()

    @property
    def _server_version(self):
        """Return the version of MAPDL."""
        return self._mapdl._server_version

    def free(self):
        """Delete all vectors.

        Examples
        --------
        >>> mm.free()
        """
        self._mapdl.run("*FREE,ALL", mute=True)

    def __repr__(self):
        return self._status

    def status(self):
        """Print out the status of all APDLMath Objects.

        Examples
        --------
        >>> mm.status()
        APDLMATH PARAMETER STATUS-  (      4 PARAMETERS DEFINED)
        Name         Type   Mem. (MB)       Dims            Workspace
        NJHLVM       SMAT   0.011           [126:126]               1
        RMAXLQ       SMAT   0.011           [126:126]               1
        WWYLBR       SMAT   0.011           [126:126]               1
        FIOMZR       VEC    0.001           126                     1

        """
        print(self._status)

    @property
    def _status(self):
        """Print out the status of all APDLMath Objects"""
        return self._mapdl.run("*STATUS,MATH", mute=False)

    @property
    def _parm(self):
        return interp_star_status(self._status)

    def vec(self, size=0, dtype=np.double, init=None, name=None, asarray=False):
        """Create a vector.

        Parameters
        ----------
        size : int
            Size of the vector

        dtype : np.dtype, optional
            Datatype of the vector.  Must be either ``np.int32``,
            ``np.int64``, or ``np.double``.

        init : str, optional
            Initialization options.  Can be ``"ones"``, ``"zeros"``,
            or ``"rand"``.

        name : str, optional
            Give the vector a name.  Otherwise one will be automatically
            generated.

        asarray : bool, optional
            Return a `scipy` array rather than an APDLMath matrix.

        Returns
        -------
        ansys.mapdl.math.AnsVec or numpy.ndarray
            APDLMath Vector or :class:`numpy.ndarray`.
        """
        if dtype not in MYCTYPE:
            raise ANSYSDataTypeError

        if not name:
            name = id_generator()

        if name.upper() not in self._parm:
            self._mapdl.run(f"*VEC,{name},{MYCTYPE[dtype]},ALLOC,{size}", mute=True)

        ans_vec = AnsVec(name, self._mapdl, dtype, init)

        if asarray:
            return self._mapdl._vec_data(ans_vec.id)
        else:
            return ans_vec

    def mat(
        self,
        nrow=0,
        ncol=0,
        dtype=np.double,
        init=None,
        name=None,
        asarray=False,
    ):
        """Create an APDLMath matrix.

        Parameters
        ----------
        nrow : int
            Number of rows.
        ncol : int
            Number of columns.
        dtype : np.dtype, optional
            Datatype of the vector.  Must be either ``np.int32``,
            ``np.int64``, or ``np.double``.
        init : str, optional
            Initialization options.  Can be ``"ones"``, ``"zeros"``,
            or ``"rand"``.
        name : str, optional
            Matrix name.  If given, assigns a MAPDL matrix based on
            the existing named matrix.  Otherwise one will be
            automatically generated.
        asarray : bool, optional
            Return a `scipy` array rather than an APDLMath matrix.

        Returns
        -------
        AnsMat
            APDLMath matrix.
        """
        if dtype not in MYCTYPE:
            raise ValueError(
                "Invalid datatype.  Must be one of the following:\n"
                "np.int32, np.int64, or np.double"
            )

        if not name:
            name = id_generator()
            self._mapdl.run(
                f"*DMAT,{name},{MYCTYPE[dtype]},ALLOC,{nrow},{ncol}", mute=True
            )
            mat = AnsDenseMat(name, self._mapdl)

            if init == "rand":
                mat.rand()
            elif init == "ones":
                mat.ones()
            elif init == "zeros":
                mat.zeros()
            elif init is not None:
                raise ValueError(f"Invalid init method '{init}'")
        else:
            info = self._mapdl._data_info(name)
            if info.objtype == pb_types.DataType.DMAT:
                mat = AnsDenseMat(name, self._mapdl)
            elif info.objtype == pb_types.DataType.SMAT:
                mat = AnsSparseMat(name, self._mapdl)
            else:  # pragma: no cover
                raise ValueError(f"Unhandled MAPDL matrix object type {info.objtype}")

        if asarray:
            mat = mat.asarray()
        return mat

    def zeros(self, nrow, ncol=None, dtype=np.double, name=None, asarray=False):
        """Create a vector or matrix containing all zeros.

        Parameters
        ----------
        nrow : int
            Number of rows.
        ncol : int, optional
            Number of columns.  If specified, returns a matrix.
        dtype : np.dtype, optional
            Datatype of the vector.  Must be either ``np.int32``,
            ``np.int64``, or ``np.double``.
        name : str, optional
            APDLMath matrix name.  Optional and defaults to a random name.
        asarray : bool, optional
            Return a `scipy` array rather than an APDLMath matrix.

        Returns
        -------
        AnsVec or AnsMat
            APDLMath vector or matrix depending on if ``ncol`` is specified.

        Examples
        --------
        Create a zero vector.

        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> mm = mapdl.math()
        >>> vec = mm.zeros(10)

        Create a zero matrix.

        >>> mat = mm.zeros(10, 10)
        """
        if not ncol:
            return self.vec(nrow, dtype, init="zeros", name=name, asarray=asarray)
        return self.mat(nrow, ncol, dtype, init="zeros", name=name, asarray=asarray)

    def ones(self, nrow, ncol=None, dtype=np.double, name=None, asarray=False):
        """Create a vector or matrix containing all ones

        Parameters
        ----------
        nrow : int
            Number of rows.
        ncol : int, optional
            Number of columns.  If specified, returns a matrix.
        dtype : np.dtype, optional
            Datatype of the vector.  Must be either ``np.int32``,
            ``np.int64``, or ``np.double``.
        name : str, optional
            APDLMath matrix name.  Optional and defaults to a random name.
        asarray : bool, optional
            Return a `scipy` array rather than an APDLMath matrix.

        Returns
        -------
        AnsVec or AnsMat
            APDLMath vector or matrix depending on if "ncol" is
            specified.

        Examples
        --------
        Create a ones vector.

        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> mm = mapdl.math()
        >>> vec = mm.ones(10)

        Create a ones matrix.

        >>> mat = mm.ones(10, 10)
        """
        if not ncol:
            return self.vec(nrow, dtype, init="ones", name=name, asarray=asarray)
        else:
            return self.mat(nrow, ncol, dtype, init="ones", name=name, asarray=asarray)

    def rand(self, nrow, ncol=None, dtype=np.double, name=None, asarray=False):
        """Create a vector or matrix containing all random values

        Parameters
        ----------
        nrow : int
            Number of rows.
        ncol : int, optional
            Number of columns.  If specified, returns a matrix.
        dtype : np.dtype, optional
            Datatype of the vector.  Must be either ``np.int32``,
            ``np.int64``, or ``np.double``.
        name : str, optional
            APDLMath matrix name.  Optional and defaults to a random name.
        asarray : bool, optional
            Return a `scipy` array rather than an APDLMath matrix.

        Returns
        -------
        AnsVec or AnsMat
            APDLMath vector or matrix depending on if "ncol" is
            specified.

        Examples
        --------
        Create a random vector.

        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> mm = mapdl.math()
        >>> vec = mm.rand(10)

        Create a random matrix.

        >>> mat = mm.rand(10, 10)
        """
        if not ncol:
            return self.vec(nrow, dtype, init="rand", name=name, asarray=asarray)
        return self.mat(nrow, ncol, dtype, init="rand", name=name, asarray=asarray)

    def matrix(self, matrix, name=None, triu=False):
        """Send a scipy matrix or numpy array to MAPDL.

        Parameters
        ----------
        matrix : np.ndarray
            Numpy array to send as a matrix to MAPDL.
        name : str, optional
            APDLMath matrix name.  Optional and defaults to a random name.
        triu : bool, optional
            ``True`` when the matrix is upper triangular, ``False``
            when unsymmetric.

        Returns
        -------
        AnsMat
            MapdlMath matrix.

        Examples
        --------
        Generate a random sparse matrix.

        >>> from scipy import sparse
        >>> sz = 5000
        >>> mat = sparse.random(sz, sz, density=0.05, format='csr')
        >>> ans_mat = mm.matrix(mat, name)
        >>> ans_mat
        APDLMath Matrix 5000 x 5000

        Transfer the matrix back to Python.

        >>> ans_mat.asarray()
        <500x5000 sparse matrix of type '<class 'numpy.float64'>'
                with 1250000 stored elements in Compressed Sparse Row format>

        """
        if name is None:
            name = id_generator()
        elif not isinstance(name, str):
            raise TypeError("``name`` parameter must be a string")

        from scipy import sparse

        self._set_mat(name, matrix, triu)
        if sparse.issparse(matrix):
            return AnsSparseMat(name, self._mapdl)
        return AnsDenseMat(name, self._mapdl)

    def load_matrix_from_file(
        self,
        dtype=np.double,
        name=None,
        fname="file.full",
        mat_id="STIFF",
        asarray=False,
    ):
        """Import a matrix from an existing FULL file.

        Parameters
        ----------
        dtype : numpy.dtype, optional
            Numpy data type to store the vector as. You can use double ("DOUBLE" or "D"),
            or complex numbers ("COMPLEX" or "Z"). Alternatively you can also supply a
            numpy data type. Defaults to ``np.double``.
        fname : str, optional
            Filename to read the matrix from.  Defaults to ``"file.full"``.
        name : str, optional
            APDLMath matrix name.  Optional and defaults to a random name.
        mat_id : str, optional
            Matrix type.  Defaults to ``"STIFF"``.

            * ``"STIFF"`` - Stiffness matrix
            * ``"MASS"`` - Mass matrix
            * ``"DAMP"`` - Damping matrix
            * ``"GMAT"`` - Constraint equation matrix
            * ``"K_RE"`` - Real part of the stiffness matrix
            * ``"K_IM"`` - Imaginary part of the stiffness matrix
        asarray : bool, optional
            Return a ``scipy`` array rather than an APDLMath matrix.

        Returns
        -------
        scipy.sparse.csr.csr_matrix or AnsMat
            Scipy sparse matrix or APDLMath matrix depending on
            ``asarray``.

        """
        if name is None:
            name = id_generator()
        elif not isinstance(name, str):
            raise TypeError("``name`` parameter must be a string")

        self._mapdl._log.info(
            "Calling MAPDL to extract the %s matrix from %s", mat_id, fname
        )
        quotes = "'"
        allowed_mat_id = (
            "STIFF",
            "MASS",
            "DAMP",
            # "NOD2BCS",  # Not allowed since #990
            # "USR2BCS",
            "GMAT",
            "K_RE",
            "K_IM",
        )
        if mat_id.upper() not in allowed_mat_id:
            raise ValueError(
                f"The 'mat_id' parameter supplied ('{mat_id}') is not allowed. "
                f"Only the following are allowed: \n{', '.join([quotes + each + quotes for each in allowed_mat_id])}"
            )

        if isinstance(dtype, str):
            if dtype.lower() not in ("complex", "double", "d", "z"):
                raise ValueError(
                    f"Data type ({dtype}) not allowed as a string."
                    "Use either: 'double' or 'complex', or a valid numpy data type."
                )
            if dtype.lower() in ("complex", "z"):
                dtype_ = "'Z'"
                dtype = np.complex64
            else:
                dtype_ = "'D'"
                dtype = np.double
        else:
            if dtype not in ANSYS_VALUE_TYPE.values():
                allowables_np_dtypes = ", ".join(
                    [
                        str(each).split("'")[1]
                        for each in ANSYS_VALUE_TYPE.values()
                        if each
                    ]
                )
                raise ValueError(
                    f"Numpy data type not allowed. Only: {allowables_np_dtypes}"
                )
            if "complex" in str(dtype):
                dtype_ = "'Z'"
            else:
                dtype_ = "'D'"

        if dtype_ == "'Z'" and mat_id.upper() in ("STIFF", "MASS", "DAMP"):
            raise ValueError(
                "Reading the stiffness, mass or damping matrices to a complex array is not supported."
            )

        self._mapdl.run(f"*SMAT,{name},{dtype_},IMPORT,FULL,{fname},{mat_id}")
        ans_sparse_mat = AnsSparseMat(name, self._mapdl)
        if asarray:
            return self._mapdl._mat_data(ans_sparse_mat.id).astype(dtype)
        return ans_sparse_mat

    def _load_file(self, fname):
        """
        Provide file to MAPDL instance.

        If in local:
            Checks if the file exists, if not, it raises a FileNotFound exception

        If in not-local:
            Check if the file exists locally or in the working directory, if not, it will raise a FileNotFound exception.
            If the file is local, it will be uploaded.

        """
        return load_file(self._mapdl, fname)

    def stiff(self, dtype=np.double, name=None, fname="file.full", asarray=False):
        """Load the stiffness matrix from a full file.

        Parameters
        ----------
        dtype : numpy.dtype, optional
            Numpy data type to store the vector as. Only applicable if
            ``asarray=True``, otherwise the returned matrix contains
            double float numbers. Defaults to ``np.double``
        name : str, optional
            APDLMath matrix name.  Optional and defaults to a random name.
        fname : str, optional
            Filename to read the matrix from.
        asarray : bool, optional
            Return a `scipy` array rather than an APDLMath matrix.

        Returns
        -------
        scipy.sparse.csr.csr_matrix or AnsMat
            Scipy sparse matrix or APDLMath matrix depending on
            ``asarray``.

        Examples
        --------
        >>> k = mapdl.math.stiff()
        APDLMATH Matrix 60 x 60

        Convert to a scipy array

        >>> mat = k.asarray()
        >>> mat
        <60x60 sparse matrix of type '<class 'numpy.float64'>'
            with 1734 stored elements in Compressed Sparse Row format>
        """
        fname = self._load_file(fname)
        return self.load_matrix_from_file(dtype, name, fname, "STIFF", asarray)

    def mass(self, dtype=np.double, name=None, fname="file.full", asarray=False):
        """Load the mass matrix from a full file.

        Parameters
        ----------
        dtype : numpy.dtype, optional
            Numpy data type to store the vector as. Only applicable if
            ``asarray=True``, otherwise the returned matrix contains
            double float numbers. Defaults to ``np.double``
        name : str, optional
            APDLMath matrix name.  Optional and defaults to a random name.
        fname : str, optional
            Filename to read the matrix from.
        asarray : bool, optional
            Return a `scipy` array rather than an APDLMath matrix.

        Returns
        -------
        scipy.sparse.csr.csr_matrix or AnsMat
            Scipy sparse matrix or APDLMath matrix depending on
            ``asarray``.

        Examples
        --------
        >>> mass = mapdl.math.mass()
        >>> mass
        APDLMATH Matrix 60 x 60

        Convert to a scipy array

        >>> mat = mass.asarray()
        >>> mat
        <60x60 sparse matrix of type '<class 'numpy.float64'>'
            with 1734 stored elements in Compressed Sparse Row format>
        """
        fname = self._load_file(fname)
        return self.load_matrix_from_file(dtype, name, fname, "MASS", asarray)

    def damp(self, dtype=np.double, name=None, fname="file.full", asarray=False):
        """Load the damping matrix from the full file.

        Parameters
        ----------
        dtype : numpy.dtype, optional
            Numpy data type to store the vector as. Only applicable if
            ``asarray=True``, otherwise the returned matrix contains
            double float numbers. Defaults to ``np.double``
        name : str, optional
            APDLMath matrix name.  Optional and defaults to a random name.
        fname : str, optional
            Filename to read the matrix from.
        asarray : bool, optional
            Return a `scipy` array rather than an APDLMath matrix.

        Returns
        -------
        scipy.sparse.csr.csr_matrix or AnsMat
            Scipy sparse matrix or APDLMath matrix depending on
            ``asarray``.

        Examples
        --------
        >>> ans_mat = mapdl.math.damp()
        >>> ans_mat
        APDLMATH Matrix 60 x 60

        Convert to a scipy array

        >>> mat = ans_mat.asarray()
        >>> mat
        <60x60 sparse matrix of type '<class 'numpy.float64'>'
            with 1734 stored elements in Compressed Sparse Row format>

        """
        fname = self._load_file(fname)
        return self.load_matrix_from_file(dtype, name, fname, "DAMP", asarray)

    def get_vec(
        self,
        dtype=None,
        name=None,
        fname="file.full",
        mat_id="RHS",
        asarray=False,
    ):
        """Load a vector from a file.

        Parameters
        ----------
        dtype : numpy.dtype, optional
            Numpy data type to store the vector as.  Defaults to
            ``np.double``.
        name : str, optional
            APDLMath matrix name.  Optional and defaults to a random name.
        fname : str, optional
            Filename to read the vector from.
        mat_id : str, optional
            Vector ID to load.  If loading from a ``"*.full"`` file,
            can be one of the following:

            * ``"RHS"`` - Load vector
            * ``"GVEC"`` - Constraint equation constant terms
            * ``"BACK"`` - nodal mapping vector (internal to user).
              If this is used, the default ``dtype`` is ``np.int32``.
            * ``"FORWARD"`` - nodal mapping vector (user to internal)
              If this is used, the default ``dtype`` is ``np.int32``.
        asarray : bool, optional
            Return a `scipy` array rather than an APDLMath matrix.

        Returns
        -------
        numpy.ndarray or AnsVec
            Numpy array or APDLMath vector depending on ``asarray``.

        Examples
        --------
        >>> vec = mm.get_vec(fname='PRSMEMB.full', mat_id="RHS")
        >>> vec
        APDLMath Vector Size 126

        """
        if name is None:
            name = id_generator()
        elif not isinstance(name, str):
            raise TypeError("``name`` parameter must be a string")

        self._mapdl._log.info(
            "Call MAPDL to extract the %s vector from the file %s",
            mat_id,
            fname,
        )

        if mat_id.upper() not in ["RHS", "GVEC", "BACK", "FORWARD"]:
            raise ValueError(
                f"The 'mat_id' value ({mat_id}) is not allowed."
                'Only "RHS", "GVEC", "BACK", or "FORWARD" are allowed.'
            )

        if mat_id.upper() in ["BACK", "FORWARD"] and not dtype:
            dtype = np.int32
        else:
            dtype = np.double

        fname = self._load_file(fname)
        self._mapdl.run(
            f"*VEC,{name},{MYCTYPE[dtype]},IMPORT,FULL,{fname},{mat_id}",
            mute=True,
        )
        ans_vec = AnsVec(name, self._mapdl)
        if asarray:
            return self._mapdl._vec_data(ans_vec.id).astype(dtype, copy=False)
        return ans_vec

    def set_vec(self, data, name=None):
        """Push a numpy array or Python list to the MAPDL memory workspace.

        Parameters
        ----------
        data : np.ndarray, list
            Numpy array or Python list to push to MAPDL.  Must be 1
            dimensional.
        name : str, optional
            APDLMath vector name.  If unset, one will be automatically
            generated.

        Returns
        -------
        ansys.mapdl.math.AnsVec
            MAPDL vector instance generated from the pushed vector.

        Examples
        --------
        Push a random vector from numpy to MAPDL.

        >>> data = np.random.random(10)
        >>> vec = mm.set_vec(data)
        >>> np.isclose(vec.asarray(), data)
        True
        """
        if name is None:
            name = id_generator()
        self._set_vec(name, data)
        return AnsVec(name, self._mapdl)

    def rhs(self, dtype=np.double, name=None, fname="file.full", asarray=False):
        """Return the load vector from a full file.

        Parameters
        ----------
        dtype : numpy.dtype, optional
            Data type to store the vector as.  Defaults to ``np.double``.
        name : str, optional
            APDLMath matrix name.  Optional and defaults to a random name.
        fname : str, optional
            Filename to read the vector from.  Defaults to ``"file.full"``.
        asarray : bool, optional
            Return a `scipy` array rather than an APDLMath matrix.

        Returns
        -------
        numpy.ndarray or ansys.mapdl.math.AnsVec
            Numpy or APDL vector instance generated from the file.

        Examples
        --------
        >>> rhs = mm.rhs(fname='PRSMEMB.full')
        APDLMath Vector Size 126

        """
        fname = self._load_file(fname)
        return self.get_vec(dtype, name, fname, "RHS", asarray)

    def svd(self, mat, thresh="", sig="", v="", **kwargs):
        """Apply an SVD Algorithm on a matrix.

        The SVD algorithm is only applicable to dense matrices.
        Columns that are linearly dependent on others are removed,
        leaving the independent or basis vectors. The matrix is
        resized according to the new size determined by the algorithm.

        For the SVD algorithm, the singular value decomposition of an
        input matrix is a factorization of the form:

        ``M = U*SIGMA*V.T``

        For more details, see `Singular Value Decomposition
        <https://en.wikipedia.org/wiki/Singular_value_decomposition>`_.

        Parameters
        ----------
        mat : ansys.AnsMat
            The array to compress.
        thresh : float, optional
            Numerical threshold value used to manage the compression.
            Default is 1E-7.
        sig : str, optional
            Name of the vector used to store the ``SIGMA`` values.
        v : str, optional
            Name of the vector used to store the values from ``v``.
            See the equation above.

        Examples
        --------
        Apply SVD on an existing Dense Rectangular Matrix, using
        default threshold.  The matrix is modified in-place.

        >>> mm.svd(mat)
        """
        kwargs.setdefault("mute", True)
        self._mapdl.run(f"*COMP,{mat.id},SVD,{thresh},{sig},{v}", **kwargs)

    def mgs(self, mat, thresh="", **kwargs):
        """Apply Modified Gram-Schmidt algorithm to a matrix.

        The MGS algorithm is only applicable to dense
        matrices. Columns that are linearly dependent on others are
        removed, leaving the independent or basis vectors. The matrix
        is resized according to the new size determined by the
        algorithm.

        Parameters
        ----------
        mat : ansys.mapdl.core.math.AnsMat
            The array to apply Modified Gram-Schmidt algorithm to.
        thresh : float, optional
            Numerical threshold value used to manage the compression.
            The default value is 1E-14 for MGS.

        Examples
        --------
        Apply MGS on an existing Dense Rectangular Matrix, using
        default threshold.  The mat matrix is modified in-situ.

        >>> mm.mgs(mat)
        """
        kwargs.setdefault("mute", True)
        self._mapdl.run(f"*COMP,{mat.id},MGS,{thresh}", **kwargs)

    def sparse(self, mat, thresh="", **kwargs):
        """Sparsify a existing matrix based on a threshold value.

        Parameters
        ----------
        mat : ansys.mapdl.core.math.AnsMat
            The dense matrix to convert to a sparse matrix.
        thresh : float, optional
            Numerical threshold value used to sparsify. The default
            value is 1E-16.
        """
        kwargs.setdefault("mute", True)
        self._mapdl.run(f"*COMP,{mat.id},SPARSE,{thresh}", **kwargs)

    def eigs(
        self,
        nev,
        k,
        m=None,
        c=None,
        phi=None,
        algo=None,
        fmin=None,
        fmax=None,
        cpxmod=None,
    ):
        """Solve an eigenproblem.

        Parameters
        ----------
        nev : int
            Number of eigenvalues to compute.
        k : ansys.AnsMat
            An array representing the operation ``A * x`` where A is a
            square matrix.
        m : ansys.AnsMat, optional
            An array representing the operation ``M * x`` for the
            generalized eigenvalue problem:

            ``K * x = M * x``

        Examples
        --------
        Solve an eigenproblem using the mass and stiffness matrices
        stored from a prior ansys run.

        >>> k = mm.stiff()
        >>> m = mm.mass()
        >>> nev = 10
        >>> a = mm.mat(k.nrow, nev)
        >>> ev = mm.eigs(nev, k, m, phi=a)
        """
        if not fmin:
            fmin = ""
        if not fmax:
            fmax = ""
        if not cpxmod:
            cpxmod = ""

        cid = ""
        if not c:
            if k.sym() and m.sym():
                if not algo:
                    algo = "LANB"
            else:
                algo = "UNSYM"
        else:
            cid = c.id
            algo = "DAMP"

        self._mapdl.run("/SOLU", mute=True)
        self._mapdl.run("antype,modal", mute=True)
        self._mapdl.run(f"modopt,{algo},{nev},{fmin},{fmax},{cpxmod}", mute=True)
        ev = self.vec()

        phistr = "" if not phi else phi.id
        self._mapdl.run(f"*EIG,{k.id},{m.id},{cid},{ev.id},{phistr}", mute=True)
        return ev

    def dot(self, vec_a, vec_b):
        """Dot product between two ANSYS vector objects.

        Parameters
        ----------
        vec_a : ansys.mapdl.math.AnsVec
            Ansys vector object.

        vec_b : ansys.mapdl.math.AnsVec
            Ansys vector object.

        Returns
        -------
        float
            Dot product between the two vectors.

        Examples
        --------
        >>> v = mm.ones(10)
        >>> w = mm.ones(10)
        >>> v.dot(w)
        """
        return dot(vec_a, vec_b)

    def add(self, obj1, obj2):
        """Add two APDLMath vectors or matrices.

        Parameters
        ----------
        obj1 : ansys.mapdl.math.AnsVec or ansys.mapdl.math.AnsMat
            Ansys object.
        obj2 : ansys.mapdl.math.AnsVec or ansys.mapdl.math.AnsMat
            Ansys object.

        Returns
        -------
        AnsVec or AnsMat
            Sum of the two input objects.  Type of the output matches
            type of the input.  Sum of the two vectors/matrices.

        Examples
        --------
        Comupute the sum between two vectors.

        >>> v = mm.ones(10)
        >>> w = mm.ones(10)
        >>> x = mm.add(v, w)
        """
        return obj1 + obj2

    def subtract(self, obj1, obj2):
        """Subtract two ANSYS vectors or matrices.

        Parameters
        ----------
        obj1 : ansys.mapdl.math.AnsVec or ansys.mapdl.math.AnsMat
            Ansys object.
        obj2 : ansys.mapdl.math.AnsVec or ansys.mapdl.math.AnsMat
            Ansys object.

        Returns
        -------
        AnsVec or AnsMat
            Difference of the two input vectors or matrices.  Type of
            the output matches the type of the input.

        Examples
        --------
        Subtract two APDLMath vectors.

        >>> v = mm.ones(10)
        >>> w = mm.ones(10)
        >>> x = mm.subtract(v, w)
        """
        return obj1 - obj2

    def factorize(self, mat, algo=None, inplace=True):
        """Factorize a matrix.

        Parameters
        ----------
        mat : ansys.mapdl.math.AnsMat
            An APDLMath matrix
        algo : str, optional
            Factorization algorithm.  Either ``"LAPACK"`` (default for
            dense matrices) or ``"DSP"`` (default for sparse matrices).
        inplace : bool, optional
            If ``False``, the factorization is performed on a copy
            of the input matrix (``mat`` argument), hence this input
            matrix (``mat``) is not changed. Default is ``True``.

        Returns
        -------
        ansys.mapdl.core.math.AnsSolver
            An Ansys Solver object.


        Examples
        --------
        Factorize a random matrix.

        >>> mm = mapdl.math
        >>> dim = 1000
        >>> m2 = mm.rand(dim, dim)
        >>> m3 = m2.copy()
        >>> mat = mm.factorize(m2)

        """
        solver = AnsSolver(id_generator(), self._mapdl)
        solver.factorize(mat, algo=algo, inplace=inplace)
        return solver

    def norm(self, obj, order="nrm2"):
        """Matrix or vector norm.

        Parameters
        ----------
        obj : ansys.mapdl.math.AnsMat or ansys.mapdl.math.AnsVec
            ApdlMath object to compute the norm from.
        order : str
            Mathematical norm to use.  One of:

            * ``'NRM2'``: L2 (Euclidean or SRSS) norm (default).
            * ``'NRM1'``: L1 (absolute sum) norm (vectors only).
            * ``'NRMINF'`` Maximum norm.
        nrm : float
            Norm of the matrix or vector(s).

        Examples
        --------
        Compute the norm of a APDLMath vector.
        v = mm.ones(10)
        3.1622776601683795
        """
        return obj.norm(nrmtype=order)

    @protect_grpc
    def _set_vec(self, vname, arr, dtype=None, chunk_size=DEFAULT_CHUNKSIZE):
        """Transfer a numpy array to MAPDL as a MAPDL Math vector.

        Parameters
        ----------
        vname : str
            Vector parameter name.  Character ":" is not allowed.
        arr : np.ndarray
            Numpy array to upload
        dtype : np.dtype, optional
            Type to upload array as.  Defaults to the current array type.
        chunk_size : int, optional
            Chunk size in bytes.  Must be less than 4MB.

        """
        if ":" in vname:
            raise ValueError(
                'The character ":" is not permitted in a MAPDL MATH'
                " vector parameter name"
            )
        if not isinstance(arr, np.ndarray):
            arr = np.asarray(arr)

        if dtype is not None:
            if arr.dtype != dtype:
                arr = arr.astype(dtype)

        if arr.dtype not in list(MYCTYPE.keys()):
            raise TypeError(
                f"Invalid array datatype {arr.dtype}\n"
                f"Must be one of the following:\n"
                f"{list_allowed_dtypes()}"
            )

        chunks_generator = get_nparray_chunks(vname, arr, chunk_size)
        self._mapdl._stub.SetVecData(chunks_generator)

    @protect_grpc
    def _set_mat(self, mname, arr, sym=None, dtype=None, chunk_size=DEFAULT_CHUNKSIZE):
        """Transfer a 2D dense or sparse scipy array to MAPDL as a MAPDL Math matrix.

        Parameters
        ----------
        mname : str
            Matrix parameter name.  Character ":" is not allowed.
        arr : np.ndarray or scipy.sparse matrix
            Matrix to upload
        sym : bool
            ``True`` when matrix is symmetric. Unused if Matrix is dense.
        dtype : np.dtype, optional
            Type to upload array as.  Defaults to the current array type.
        chunk_size : int, optional
            Chunk size in bytes.  Must be less than 4MB.

        """
        from scipy import sparse

        if ":" in mname:
            raise ValueError(
                'The character ":" is not permitted in a MAPDL MATH'
                " matrix parameter name"
            )
        if not len(mname):
            raise ValueError("Empty MAPDL matrix name not permitted")

        if isinstance(arr, np.ndarray):
            if arr.ndim == 1:
                raise ValueError(
                    "Input appears to be an array.  " "Use ``set_vec`` instead.)"
                )
            if arr.ndim > 2:
                raise ValueError("Arrays must be 2 dimensional")

        if sparse.issparse(arr):
            self._send_sparse(mname, arr, sym, dtype, chunk_size)
        else:  # must be dense matrix
            self._send_dense(mname, arr, dtype, chunk_size)

    @requires_version((0, 4, 0), VERSION_MAP)
    def _send_dense(self, mname, arr, dtype, chunk_size):
        """Send a dense numpy array/matrix to MAPDL."""
        if dtype is not None:
            if arr.dtype != dtype:
                arr = arr.astype(dtype)

        if arr.dtype not in list(NP_VALUE_TYPE.keys()):
            raise TypeError(
                f"Invalid array datatype {arr.dtype}\n"
                f"Must be one of the following:\n"
                f"{list_allowed_dtypes()}"
            )

        chunks_generator = get_nparray_chunks_mat(mname, arr, chunk_size)
        self._mapdl._stub.SetMatData(chunks_generator)

    def _send_sparse(self, mname, arr, sym, dtype, chunk_size):
        """Send a scipy sparse sparse matrix to MAPDL."""
        if sym is None:
            raise ValueError(
                "The symmetric flag ``sym`` must be set for a sparse " "matrix"
            )
        from scipy import sparse

        arr = sparse.csr_matrix(arr)

        if arr.shape[0] != arr.shape[1]:
            raise ValueError("APDLMath only supports square matrices")

        if dtype is not None:
            if arr.data.dtype != dtype:
                arr.data = arr.data.astype(dtype)

        if arr.dtype not in list(NP_VALUE_TYPE.keys()):
            raise TypeError(
                f"Invalid array datatype {arr.dtype}\n"
                f"Must be one of the following:\n"
                f"{list_allowed_dtypes()}"
            )

        # data vector
        dataname = f"{mname}_DATA"
        ans_vec = self.set_vec(arr.data, dataname)
        if dtype is None:
            info = self._mapdl._data_info(ans_vec.id)
            dtype = ANSYS_VALUE_TYPE[info.stype]

        # indptr vector
        indptrname = f"{mname}_IND"
        indv = arr.indptr.astype("int64") + 1  # FORTRAN indexing
        self.set_vec(indv, indptrname)

        # indices vector
        indxname = f"{mname}_PTR"
        idx = arr.indices + 1  # FORTRAN indexing
        self.set_vec(idx, indxname)

        flagsym = "TRUE" if sym else "FALSE"
        self._mapdl.run(
            f"*SMAT,{mname},{MYCTYPE[dtype]},ALLOC,CSR,{indptrname},{indxname},"
            f"{dataname},{flagsym}"
        )


class ApdlMathObj:
    """Common class for MAPDL Math objects"""

    def __init__(self, id_, mapdl, dtype=ObjType.GEN):
        self.id = id_
        self._mapdl = mapdl
        self.type = dtype

    def __repr__(self):
        return f"APDLMath Object {self.id}"

    def __str__(self):
        return self._mapdl.run(f"*PRINT,{self.id}", mute=False)

    def copy(self):
        """Returns the name of the copy of this object"""
        name = id_generator()  # internal name of the new vector
        info = self._mapdl._data_info(self.id)
        dtype = ANSYS_VALUE_TYPE[info.stype]

        if self.type == ObjType.VEC:
            acmd = "*VEC"
        elif self.type == ObjType.DMAT:
            acmd = "*DMAT"
        elif self.type == ObjType.SMAT:
            acmd = "*SMAT"
        else:
            raise TypeError(f"Copy aborted: Unknown obj type {self.type}")

        # APDLMath cmd to COPY vin to vout
        self._mapdl.run(f"{acmd},{name},{MYCTYPE[dtype]},COPY,{self.id}", mute=True)
        return name

    def _init(self, method):
        self._mapdl.run(f"*INIT,{self.id},{method}", mute=True)

    def zeros(self):
        """Set all values of the vector to zero"""
        return self._init("ZERO")

    def ones(self):
        """Set all values of the vector to one"""
        return self._init("CONST,1")

    def rand(self):
        """Set all values of the vector to a random number"""
        return self._init("RAND")

    def const(self, value):
        """Set all values of the vector to a constant"""
        return self._init(f"CONST,{value}")

    def norm(self, nrmtype="nrm2"):
        """Matrix or vector norm.

        Parameters
        ----------
        nrmtype : str, optional
            Mathematical norm to use.  One of:

            - ``'NRM2'``: L2 (Euclidean or SRSS) norm (default).
            - ``'NRM1'``: L1 (absolute sum) norm (vectors only).
            - ``'NRMINF'`` : Maximum norm.

        Returns
        -------
        float
            Norm of the matrix or vector(s).

        Examples
        --------
        >>> mm = mapdl.math
        >>> dim = 1000
        >>> m2 = mm.rand(dim, dim)
        >>> nrm = mm.norm( m2)
        """
        val_name = "py_val"
        self._mapdl.run(f"*NRM,{self.id},{nrmtype},{val_name}", mute=True)
        return self._mapdl.scalar_param(val_name)

    def axpy(self, op, val1, val2):
        """Perform the matrix operation: ``M2= v*M1 + w*M2``"""
        if not hasattr(op, "id"):
            raise TypeError("Must be an ApdlMathObj")
        self._mapdl._log.info("Call Mapdl to perform AXPY operation")
        self._mapdl.run(f"*AXPY,{val1},0,{op.id},{val2},0,{self.id}", mute=True)
        return self

    def kron(self, obj):
        """Calculates the Kronecker product of two matrices/vectors

        Parameters
        ----------
        obj : ``AnsVec`` or ``AnsMat``
            AnsMath object.

        Returns
        -------
        ``AnsMat`` or ``AnsVec``
            Kronecker product between the two matrices/vectors.

        .. note::
            Requires at least MAPDL version 2023R2.

        Examples
        --------
        >>> mm = mapdl.math
        >>> m1 = mm.rand(3, 3)
        >>> m2 = mm.rand(4,2)
        >>> res = m1.kron(m2)
        """

        mapdl_version = self._mapdl.version
        if mapdl_version < 23.2:  # pragma: no cover
            raise VersionError("``kron`` requires MAPDL version 2023R2")

        if not isinstance(obj, ApdlMathObj):
            raise TypeError("Must be an ApdlMathObj")

        if not isinstance(self, (AnsMat, AnsVec)):
            raise TypeError(f"Kron product aborted: Unknown obj type ({self.type})")
        if not isinstance(obj, (AnsMat, AnsVec)):
            raise TypeError(f"Kron product aborted: Unknown obj type ({obj.type})")

        name = id_generator()  # internal name of the new vector/matrix
        # perform the Kronecker product
        self._mapdl.run(f"*KRON,{self.id},{obj.id},{name}")

        if isinstance(self, AnsVec) and isinstance(obj, AnsVec):
            objout = AnsVec(name, self._mapdl)
        else:
            objout = AnsMat(name, self._mapdl)
        return objout

    def __add__(self, op2):
        if not hasattr(op2, "id"):
            raise TypeError("Must be an ApdlMathObj")

        opout = self.copy()
        self._mapdl._log.info("Call Mapdl to perform AXPY operation")
        self._mapdl.run(f"*AXPY,1,0,{op2.id},1,0,{opout.id}", mute=True)
        return opout

    def __sub__(self, op2):
        if not hasattr(op2, "id"):
            raise TypeError("Must be an ApdlMathObj")

        opout = self.copy()
        self._mapdl._log.info("Call Mapdl to perform AXPY operation")
        self._mapdl.run(f"*AXPY,-1,0,{op2.id},1,0,{opout.id}", mute=True)
        return opout

    def __matmul__(self, op):
        return self.dot(op)

    def __iadd__(self, op):
        return self.axpy(op, 1, 1)

    def __isub__(self, op):
        return self.axpy(op, -1, 1)

    def __imul__(self, val):
        mapdl_version = self._mapdl.version
        self._mapdl._log.info("Call Mapdl to scale the object")

        if isinstance(val, AnsVec):
            if mapdl_version < 23.2:  # pragma: no cover
                raise VersionError(
                    "Scaling by a vector requires MAPDL version 2023R2 or superior."
                )
            else:
                self._mapdl._log.info(f"Scaling ({self.type}) by a vector")
                self._mapdl.run(f"*SCAL,{self.id},{val.id}", mute=False)
        elif isinstance(val, (int, float)):
            self._mapdl.run(f"*SCAL,{self.id},{val}", mute=True)
        else:
            raise TypeError(f"The provided type {type(val)} is not supported.")

        return self

    def __itruediv__(self, val):
        if val == 0:
            raise ZeroDivisionError("division by zero")
        self._mapdl._log.info("Call Mapdl to 1/scale the object")
        self._mapdl.run(f"*SCAL,{self.id},{1/val}", mute=True)
        return self

    @property
    @protect_grpc
    def _data_info(self):
        """Return the data type of a parameter"""
        request = pb_types.ParameterRequest(name=self.id)
        return self._stub.GetDataInfo(request)


class AnsVec(ApdlMathObj):
    """APDLMath Vector Object"""

    def __init__(self, id_, mapdl, dtype=np.double, init=None):
        ApdlMathObj.__init__(self, id_, mapdl, ObjType.VEC)

        if init not in ["ones", "zeros", "rand", None]:
            raise ValueError(
                f"Invalid init option {init}.\n"
                'Should be "ones", "zeros", "rand", or None'
            )

        if init == "rand":
            self.rand()
        elif init == "ones":
            self.ones()
        elif init == "zeros":
            self.zeros()

    @property
    def size(self):
        """Number of items in this vector."""
        sz = self._mapdl.scalar_param(f"{self.id}_DIM")
        if sz is None:
            raise MapdlRuntimeError("This vector has been deleted within MAPDL.")
        return int(sz)

    def __repr__(self):
        return f"APDLMath Vector Size {self.size}"

    def __getitem__(self, num):
        info = self._mapdl._data_info(self.id)
        dtype = ANSYS_VALUE_TYPE[info.stype]
        if num < 0:
            raise ValueError("Negative indices not permitted")

        self._mapdl.run(f"pyval_={self.id}({num+1})", mute=True)
        item_val = self._mapdl.scalar_param("pyval_")

        if MYCTYPE[dtype].upper() in ["C", "Z"]:
            self._mapdl.run(f"pyval_img_={self.id}({num+1},2)", mute=True)
            img_val = self._mapdl.scalar_param("pyval_img_")
            item_val = item_val + img_val * 1j

            # Clean parameters
            self._mapdl.run("item_val =")
            self._mapdl.run("pyval_img_=")

        return item_val

    def __mul__(self, vec):
        """Element-Wise product with another Ansys vector object.

        Also known as Hadamard product.

        .. note::
            Requires at least MAPDL version 2021R2.

        Parameters
        ----------
        vec : ansys.mapdl.math.AnsVec
            Ansys vector object.

        Returns
        -------
        AnsVec
            Hadamard product between this vector and the other vector.
        """
        if not server_meets_version(
            self._mapdl._server_version, (0, 4, 0)
        ):  # pragma: no cover
            raise VersionError("``AnsVec`` requires MAPDL version 2021R2")

        if not isinstance(vec, AnsVec):
            raise TypeError("Must be an Ansys vector object")

        name = id_generator()  # internal name of the new vector/matrix
        info = self._mapdl._data_info(self.id)
        dtype = ANSYS_VALUE_TYPE[info.stype]

        # check size consistency
        if self.size != vec.size:
            raise ValueError("Vectors have inconsistent sizes")

        self._mapdl.run(f"*VEC,{name},{MYCTYPE[dtype]},ALLOC,{info.size1}")
        objout = AnsVec(name, self._mapdl)

        # perform the Hadamard product
        self._mapdl.run(f"*HPROD,{self.id},{vec.id},{name}")
        return objout

    def copy(self):
        """Return a copy of this vector"""
        return AnsVec(ApdlMathObj.copy(self), self._mapdl)

    def dot(self, vec) -> float:
        """Dot product with another APDLMath vector.

        Parameters
        ----------
        vec : ansys.mapdl.math.AnsVec
            Ansys vector object.

        Returns
        -------
        float
            Dot product between this vector and the other vector.
        """
        if not isinstance(vec, AnsVec):
            raise TypeError("Must be an Ansys vector object")

        self._mapdl.run(f"*DOT,{self.id},{vec.id},py_val")
        return self._mapdl.scalar_param("py_val")

    def asarray(self) -> np.ndarray:
        """Returns vector as a numpy array

        Examples
        --------
        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> mm = mapdl.math
        >>> v = mm.ones(10)
        >>> v.asarray()
        [1. 1. 1. 1. 1. 1. 1. 1. 1. 1.]
        """
        return self._mapdl._vec_data(self.id)

    def __array__(self):
        """Allow numpy to access this object as if it was an array"""
        return self.asarray()


class AnsMat(ApdlMathObj):
    """APDLMath Matrix Object"""

    def __init__(self, id_, mapdl, type_=ObjType.DMAT):
        ApdlMathObj.__init__(self, id_, mapdl, type_)

    @property
    def nrow(self) -> int:
        """Number of columns in this matrix."""
        return int(self._mapdl.scalar_param(self.id + "_ROWDIM"))

    @property
    def ncol(self) -> int:
        """Number of rows in this matrix."""
        return int(self._mapdl.scalar_param(self.id + "_COLDIM"))

    @property
    def size(self) -> int:
        """Number of items in this matrix."""
        return self.nrow * self.ncol

    @property
    def shape(self) -> tuple:
        """Returns a numpy-like shape.

        Tuple of (rows and columns).
        """
        return (self.nrow, self.ncol)

    def sym(self) -> bool:
        """Return if matrix is symmetric.

        Returns
        -------
        bool
            ``True`` when this matrix is symmetric.

        """

        info = self._mapdl._data_info(self.id)

        if server_meets_version(
            self._mapdl._server_version, (0, 5, 0)
        ):  # pragma: no cover
            return info.mattype in [
                0,
                1,
                2,
            ]  # [UPPER, LOWER, DIAG] respectively

        warn(
            "Call to ``sym`` cannot evaluate if this matrix "
            "is symmetric with this version of MAPDL."
        )
        return True

    def asarray(self, dtype=None) -> np.ndarray:
        """Returns vector as a numpy array.

        Parameters
        ----------
        dtype : numpy.dtype, optional
            Numpy data type

        Returns
        -------
        np.ndarray
            Numpy array with the defined data type

        Examples
        --------
        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> mm = mapdl.math
        >>> v = mm.ones(10)
        >>> v.asarray()
        [1. 1. 1. 1. 1. 1. 1. 1. 1. 1.]
        >>> v.asarray(dtype=np.int_)
        [1 1 1 1 1 1 1 1 1 1]

        """
        if dtype:
            return self._mapdl._mat_data(self.id).astype(dtype)
        else:
            return self._mapdl._mat_data(self.id)

    def __mul__(self, vec):
        raise AttributeError(
            "Array multiplication is not yet available.  "
            "For dot product, please use `dot()`"
        )

    def dot(self, obj):
        """Perform the matrix multiplication by another vector or matrix.

        Parameters
        ----------
        obj : ansys.mapdl.math.AnsVec or ansys.mapdl.math.AnsMat
            Ansys object.

        Returns
        -------
        AnsVec or AnsMat
            Matrix multiplication result.

        Examples
        --------
        Multiplication of a matrix and vector.

        >>> m1 = mm.rand(10, 10)
        >>> v1 = mm.rand(10)
        >>> v2 = m1.dot(v1)
        >>> assert np.allclose(m1.asarray() @ v1.asarray(), v2)

        """
        name = id_generator()  # internal name of the new vector/matrix
        info = self._mapdl._data_info(self.id)
        dtype = ANSYS_VALUE_TYPE[info.stype]
        if obj.type == ObjType.VEC:
            self._mapdl.run(
                f"*VEC,{name},{MYCTYPE[dtype]},ALLOC,{info.size1}", mute=True
            )
            objout = AnsVec(name, self._mapdl)
        else:
            self._mapdl.run(
                f"*DMAT,{name},{MYCTYPE[dtype]},ALLOC,{info.size1},{info.size2}",
                mute=True,
            )
            objout = AnsDenseMat(name, self._mapdl)

        self._mapdl._log.info("Call Mapdl to perform MV Product")
        self._mapdl.run(f"*MULT,{self.id},,{obj.id},,{name}", mute=True)
        return objout

    def __getitem__(self, num):
        """Return a vector from a given index."""
        name = id_generator()
        info = self._mapdl._data_info(self.id)
        dtype = ANSYS_VALUE_TYPE[info.stype]
        self._mapdl.run(
            f"*VEC,{name},{MYCTYPE[dtype]},LINK,{self.id},{num+1}", mute=True
        )
        return AnsVec(name, self._mapdl)

    @property
    def T(self):
        """Returns the transpose of a MAPDL matrix.

        Examples
        --------
        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> mm = mapdl.math
        >>> mat = mm.rand(2, 3)
        >>> mat_t = mat.T

        """
        info = self._mapdl._data_info(self.id)

        if info.objtype == 2:
            objtype = "*DMAT"
        else:
            objtype = "*SMAT"

        dtype = ANSYS_VALUE_TYPE[info.stype]
        name = id_generator()
        self._mapdl._log.info("Call MAPDL to transpose")
        self._mapdl.run(
            f"{objtype},{name},{MYCTYPE[dtype]},COPY,{self.id},TRANS", mute=True
        )
        if info.objtype == 2:
            mat = AnsDenseMat(name, self._mapdl)
        else:
            mat = AnsSparseMat(name, self._mapdl)
        return mat


class AnsDenseMat(AnsMat):
    """Dense APDLMath Matrix"""

    def __init__(self, uid, mapdl):
        AnsMat.__init__(self, uid, mapdl, ObjType.DMAT)

    def __array__(self):
        """Allow numpy to access this object as if it was an array"""
        return self.asarray()

    def __repr__(self):
        return f"Dense APDLMath Matrix ({self.nrow}, {self.ncol})"

    def copy(self):
        """Return a copy of this matrix"""
        return AnsDenseMat(ApdlMathObj.copy(self), self._mapdl)


class AnsSparseMat(AnsMat):
    """Sparse APDLMath Matrix"""

    def __init__(self, uid, mapdl):
        AnsMat.__init__(self, uid, mapdl, ObjType.SMAT)

    def __repr__(self):
        return f"Sparse APDLMath Matrix ({self.nrow}, {self.ncol})"

    def copy(self):
        """Return a copy of this matrix.

        Matrix remains in MAPDL.

        Examples
        --------
        >>> k
        Sparse APDLMath Matrix (126, 126)

        >>> kcopy = k.copy()
        >>> kcopy
        Sparse APDLMath Matrix (126, 126)

        """
        return AnsSparseMat(ApdlMathObj.copy(self), self._mapdl)

    def todense(self) -> np.ndarray:
        """Return this array as a dense np.ndarray

        Examples
        --------
        >>> k
        Sparse APDLMath Matrix (126, 126)

        >>> mat = k.todense()
        >>> mat
        matrix([[ 2.02925393e-01,  3.78142616e-03,  0.00000000e+00, ...,
                  0.00000000e+00,  0.00000000e+00,  0.00000000e+00],
                [ 0.00000000e+00,  2.00906608e-01,  0.00000000e+00, ...,
                  0.00000000e+00,  0.00000000e+00,  0.00000000e+00],
                [ 0.00000000e+00,  0.00000000e+00,  2.29396542e+03, ...,
                  0.00000000e+00,  0.00000000e+00,  0.00000000e+00],
                ...,
                [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00, ...,
                  2.26431549e+03, -9.11391851e-08,  0.00000000e+00],
                [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00, ...,
                  0.00000000e+00,  3.32179197e+03,  0.00000000e+00],
                [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00, ...,
                  0.00000000e+00,  0.00000000e+00,  2.48282229e-01]])

        """
        return self.asarray().todense()

    def __array__(self):
        """Allow numpy to access this object as if it was an array"""
        return self.todense()


class AnsSolver(ApdlMathObj):
    """APDLMath Solver Class"""

    def __repr__(self):
        return "APDLMath Linear Solver"

    def factorize(self, mat, algo=None, inplace=True):
        """Factorize a matrix

        Perform the numerical factorization of a linear solver system (:math:`A*x=b`).

        .. warning:: By default, factorization modifies the input matrix ``mat``
           in place. This behavior can be changed using the ``inplace`` argument.

        Parameters
        ----------
        mat : ansys.mapdl.math.AnsMat
            An ansys.mapdl.math matrix.
        algo : str, optional
            Factorization algorithm.  Either ``"LAPACK"`` (default for
            dense matrices) or ``"DSP"`` (default for sparse matrices).
        inplace : bool, optional
            If ``False``, the factorization is performed on a copy
            of the input matrix (``mat`` argument), hence this input
            matrix (``mat``) is not changed. Default is ``True``.

        Examples
        --------
        Factorize a random matrix and solve a linear system.

        >>> mm = mapdl.math
        >>> dim = 1000
        >>> m2 = mm.rand(dim, dim)
        >>> solver = mm.factorize(m2)
        >>> b = mm.ones(dim)
        >>> x = solver.solve(b)

        """
        mat_id = mat.id
        if not inplace:
            self._mapdl._log.info("Performing factorization in a copy of the array.")
            copy_mat = mat.copy()
            mat_id = copy_mat.id
        else:
            self._mapdl._log.info(
                "Performing factorization inplace. This changes the input array."
            )

        if not algo:
            if mat.type == ObjType.DMAT:
                algo = "LAPACK"
            elif mat.type == ObjType.SMAT:
                algo = "DSP"

        self._mapdl.run(f"*LSENGINE,{algo},{self.id},{mat_id}", mute=True)
        self._mapdl._log.info(f"Factorizing using the {algo} package")
        self._mapdl.run(f"*LSFACTOR,{self.id}", mute=True)

    def solve(self, b, x=None):
        """Solve a linear system

        Parameters
        ----------
        b : ansys.mapdl.math.AnsVec
            APDLmath vector.
        x : ansys.mapdl.math.AnsVec, optional
            APDLmath vector to place the solution.

        Returns
        -------
        AnsVec
            Solution vector.  Identical to ``x`` if supplied.

        Examples
        --------
        >>> k = mm.stiff(fname='PRSMEMB.full')
        >>> s = mm.factorize(k)
        >>> b = mm.get_vec(fname='PRSMEMB.full', mat_id="RHS")
        >>> x = s.solve(b)
        >>> x
        APDLMath Vector Size 20000

        """
        if not x:
            x = b.copy()
        self._mapdl._log.info("Solving")
        self._mapdl.run(f"*LSBAC,{self.id},{b.id},{x.id}", mute=True)
        return x


def rand(obj):
    """Set all values of a mapdl math object to random values.

    Parameters
    ----------
    obj : ansys.math.MapdlMath object
        MapdlMath object

    Examples
    --------
    >>> vec = mm.ones(10)
    >>> mm.rand(vec)
    """
    obj._mapdl.run(f"*INIT,{obj.id},RAND", mute=True)


def solve(mat, b, x=None, algo=None):
    solver = AnsSolver(id_generator(), mat._mapdl)
    solver.factorize(mat, algo)
    if not x:
        x = b.copy()
    x = solver.solve(b, x)

    del solver
    return x


def dot(vec1, vec2) -> float:
    """Dot product between two APDLMath vectors.

    Parameters
    ----------
    vec1 : ansys.mapdl.math.AnsVec
        APDLMath vector.

    vec1 : ansys.mapdl.math.AnsVec
        APDLMath vector.

    Returns
    -------
    float
        Dot product between the two vectors

    """
    if vec1.type != ObjType.VEC or vec2.type != ObjType.VEC:
        raise TypeError("Both objects must be ANSYS vectors")

    mapdl = vec1._mapdl
    mapdl.run(f"*DOT,{vec1.id},{vec2.id},py_val", mute=True)
    return mapdl.scalar_param("py_val")
