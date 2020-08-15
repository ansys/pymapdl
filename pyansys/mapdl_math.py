"""Contains the MapdlMath classes, allowing for math operations within
mapdl from Python.  """
import string
import random
from enum import Enum

import numpy as np

import pyansys


MYCTYPE = {np.int32: 'I',
           np.int64: 'L',
           np.double: 'D'}


ANSYSTYPEERROR = ValueError('Invalid datatype.  Must be one of the following:\n' +
                            'np.int32, np.int64, or np.double')


def id_generator(size=6, chars=string.ascii_uppercase):
    """Generate a random string"""
    return ''.join(random.choice(chars) for _ in range(size))


class ObjType(Enum):
    """Generic APDLMath Object ( Shared features between Vec Mat and
    Solver components """
    GEN = 1
    VEC = 2
    DMAT = 3
    SMAT = 4


class MapdlMath():
    """Abstract mapdl math class.  Created from a ``Mapdl`` instance.

    Examples
    --------
    Create an instance from an existing mapdl instance

    >>> import ansys
    >>> mapdl = ansys.Mapdl()
    >>> mm = mapdl.math()

    Alternatively:

    >>> from ansys.mapdl.math import MapdlMath
    >>> mm = MapdlMath(mapdl)  # from mapdl above

    Vector addition

    >>> v1 = mm.ones(10)
    >>> v2 = mm.ones(10)
    >>> v3 = v1 + v2

    Matrix multiplcation

    >>> v1 = mm.ones(10)
    >>> m1 = mm.rand(10, 10)
    >>> v2 = m1*v1

    """

    def __init__(self, mapdl):
        if not isinstance(mapdl, pyansys.mapdl._MapdlCore):
            raise TypeError('"mapdl" must be a Mapdl instance')
        self._mapdl = mapdl

    def __repr__(self):
        return mapdl.starstatus('MATH')

    def free(self):
        """Delete all vectors"""
        self._mapdl.run("*FREE,ALL")

    def vec(self, size=0, dtype=np.double, init=None, name=None):
        """Create a vector

        Parameters
        ----------
        size : int
            Size of the vector
        dtype : np.dtype, optional
            Datatype of the vector.  Must be either np.int32, np.int64, or np.double
        init : str, optional
            Initialization options.  Can be ones, zeros, or rand.

        Returns
        -------
        vector : ansys.mapdl.math.AnsVec
            ANSYS Vector
        """
        if dtype not in MYCTYPE:
            raise ANSYSTYPEERROR

        if not name:
            name = id_generator()
            self._mapdl.run("*VEC," + name + "," + MYCTYPE[dtype] + ",ALLOC," + str(size))
            return AnsVec(name, self._mapdl, dtype, init)
        else:
            return AnsVec(name, self._mapdl)
    
    def mat(self, nrow=0, ncol=0, dtype=np.double, init=None, name=None):
        """Create matrix

        Parameters
        ----------
        nrow : int
            Number of rows.

        ncol : int
            Number of columns.

        dtype : np.dtype, optional
            Datatype of the vector.  Must be either np.int32, np.int64, or np.double

        init : str, optional
            Initialization options.  Can be ones, zeros, or rand.

        Returns
        -------
        matrix : ansys.math.AnsMat
            ANSYS matrix
        """
        if dtype not in MYCTYPE:
            raise ValueError('Invalid datatype.  Must be one of the following:\n' +
                             'np.int32, np.int64, or np.double')

        if not name:
            name = id_generator()
            cmd = "*DMAT," + name + "," + MYCTYPE[dtype] + ",ALLOC," + str(nrow) + "," + str(ncol)
            self._mapdl.run(cmd)
            m = AnsMat(name, self._mapdl)

            if (init == "rand"):
                m.rand()
            elif (init == "ones"):
                m.ones()
            elif (init == "zeros"):
                m.zeros()
            elif init is not None:
                raise RuntimeError("Invalid init method")
        else:
            info = self._mapdl._data_info(name)
            mtype = info.objtype
            if mtype == 2:
                return AnsMat(name, self._mapdl, type=ObjType.DMAT)
            else:
                return AnsMat(name, self._mapdl, type=ObjType.SMAT)

        return m

    def zeros(self, nrow, ncol=None, dtype=np.double):
        """Create a vector or matrix containing all zeros

        nrow : int
            Number of rows.

        ncol : int, optional
            Number of columns.  If specified, returns a matrix.

        dtype : np.dtype, optional
            Datatype of the vector.  Must be either np.int32, np.int64, or np.double

        Returns
        -------
        ans_vec_mat : ansys.AnsVec or ansys.AnsMat
            ANSYS vector or matrix depending on if "ncol" is specified

        Examples
        --------
        Create a zero vector

        >>> import ansys
        >>> mapdl = ansys.Mapdl()
        >>> mm = mapdl.math()
        >>> vec = mm.zeros(10)

        Create a zero matrix

        >>> mat = mm.zeros(10, 10)
        """
        if dtype not in MYCTYPE:
            raise ANSYSTYPEERROR

        if not ncol:
            return self.vec(nrow, dtype, init="zeros")
        else:
            return self.mat(nrow, ncol, dtype, init="zeros")

    def ones(self, nrow, ncol=None, dtype=np.double):
        """Create a vector or matrix containing all ones

        nrow : int
            Number of rows.

        ncol : int, optional
            Number of columns.  If specified, returns a matrix.

        dtype : np.dtype, optional
            Datatype of the vector.  Must be either np.int32, np.int64, or np.double

        Returns
        -------
        ans_vec_mat : ansys.AnsVec or ansys.AnsMat
            ANSYS vector or matrix depending on if "ncol" is specified

        Examples
        --------
        Create a ones vector

        >>> import ansys
        >>> mapdl = ansys.Mapdl()
        >>> mm = mapdl.math()
        >>> vec = mm.ones(10)

        Create a ones matrix

        >>> mat = mm.ones(10, 10)
        """

        if not ncol:
            return self.vec(nrow, dtype, init="ones")
        else:
            return self.mat(nrow, ncol, dtype, init="ones")

    def rand(self, nrow, ncol=None, dtype=np.double):
        """Create a vector or matrix containing all random values

        nrow : int
            Number of rows.

        ncol : int, optional
            Number of columns.  If specified, returns a matrix.

        dtype : np.dtype, optional
            Datatype of the vector.  Must be either np.int32, np.int64, or np.double

        Returns
        -------
        ans_vec_mat : ansys.AnsVec or ansys.AnsMat
            ANSYS vector or matrix depending on if "ncol" is specified

        Examples
        --------
        Create a random vector

        >>> import ansys
        >>> mapdl = ansys.Mapdl()
        >>> mm = mapdl.math()
        >>> vec = mm.rand(10)

        Create a random matrix

        >>> mat = mm.rand(10, 10)
        """

        if not ncol:
            return self.vec(nrow, dtype, init="rand")
        else:
            return self.mat(nrow, ncol, dtype, init="rand")

    def load_matrix_from_file(self, type=np.double, fname="file.full", matId="STIFF"):
        """Load a matrix from a file
        """
        name = id_generator()
        self._mapdl.log.info(f"Calling MAPDL to extract the %s matrix from %s",
                            matId, fname)
        self._mapdl.run("*SMAT," + name + "," + MYCTYPE[type] + ",IMPORT,FULL," + fname + "," + matId)
        return AnsMat(name, self._mapdl, ObjType.SMAT)

    def stiff(self, type=np.double, fname="file.full"):
        """Load the stiffness matrix from the full file"""
        return self.load_matrix_from_file(type, fname, "STIFF")

    def mass(self, type=np.double, fname="file.full"):
        """Load the mass matrix from the full file"""
        return self.load_matrix_from_file(type, fname, "MASS")

    def damp(self, type=np.double, fname="file.full"):
        """Load the damping matrix from the full file"""
        return self.load_matrix_from_file(type, fname, "DAMP")

    def getVec(self, type=np.double, fname="file.full", matId="RHS"):
        """Load a vector from a file"""
        name = id_generator()
        self._mapdl.log.info(f">> Call MAPDL to extract the {matId} vector from the file {fname}")
#        print(">> Call MAPDL to extract the " + matId + " vector from the file " + fname)
        self._mapdl.run("*VEC," + name + "," + MYCTYPE[type] + ",IMPORT,FULL," + fname + "," + matId)
        return AnsVec(name, self._mapdl)

    def set_vec(self, vname, data):
        """Push a numpy array or Python list to the MAPDL Memory
        Workspace.

        Parameters
        ----------
        vname : str
            APDLMath vector name

        data : np.ndarray, list
            Numpy array or Python list to push to MAPDL.  Must be 1
            dimensional.

        Returns
        -------
        vec : ansys.mapdl.math.AnsVec
            MAPDL vector instance generated from the pushed vector.

        Examples
        --------
        >>> data = np.random.random(10)
        >>> vec = mm.set_vec('NewVec', data)
        >>> np.isclose(vec.asarray(), data)
        True
        """
        self._mapdl._set_vec(vname, data)
        return AnsVec('NewVec', self._mapdl)

    def rhs(self, type=np.double, fname="file.full"):
        return self.getVec(type, fname, "RHS")

    def eigs(self, nev, k, m=None, c=None, phi=None, algo=None,
             fmin=None, fmax=None):
        """Solve an eigenproblem

        Parameters
        ----------
        nev : int
            Number of eigenvalues to compute.

        K : ansys.AnsMat
            An array representing the operation ``A * x`` where A is a
            square matrix.

        M : ansys.AnsMat, optional
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
            fmin = ''
        if not fmax:
            fmax = ''

        cid = ''

        if not c:
            if (k.sym() and m.sym()):
                if not algo:
                    algo = "LANB"
            else:
                algo = "UNSYM"
        else:
            cid = c.id
            algo = "DAMP"

        self._mapdl.run("/SOLU")
        self._mapdl.run("antype,modal")
        self._mapdl.run("modopt," + algo + "," + str(nev) + "," + str(fmin) + "," + str(fmax))
        ev = self.vec()

        phistr = '' if not phi else phi.id
        self._mapdl.run("*EIG," + k.id + "," + m.id + "," + cid + "," + ev.id + "," + phistr)

        return ev

    def dot(self, obj1, obj2):
        """Dot product between two ANSYS vector objects.

        Parameters
        ----------
        vec1 : ansys.mapdl.math.AnsVec
            Ansys vector object.

        vec1 : ansys.mapdl.math.AnsVec
            Ansys vector object.

        Returns
        -------
        dot_product : float
            Dot product between the two vectors.

        """
        return dot(obj1, obj2)

    def factorize(self, mat):
        """Factorize a matrix"""
        solver = AnsSolver(id_generator(), self._mapdl)
        solver.factorize(mat)
        return solver


class ApdlMathObj:
    def __init__(self, id, mapdl, type=ObjType.GEN):
        self.id = id
        self._mapdl = mapdl
        self.type = type

    def __repr__(self):
        return "APDLMath Object %s" % str(self.id)

    def __str__(self):
        return self._mapdl.run("*PRINT," + self.id)

    def copy(self):
        """Returns the name of the copy of this object"""
        name = id_generator()  # internal name of the new vector
        if self.type == ObjType.VEC:
            acmd = "*VEC"
        elif self.type == ObjType.DMAT:
            acmd = "*DMAT"
        elif self.type == ObjType.SMAT:
            acmd = "*SMAT"
        else:
            raise TypeError("Unknown obj type: operation aborted")

        # APDLMath cmd to COPY vin to vout
        self._mapdl.run(acmd + "," + name + ",D,COPY," + self.id)
        return name

    def _init(self, method):
        cmd = "*INIT," + self.id + "," + method
        self._mapdl.run(cmd)

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
        return self._init("CONST," + str(value))

    def nrm(self, nrmtype="nrm2"):
        """Norm of the vector"""
        val_name = 'py_val'
        self._mapdl.run("*NRM," + self.id + "," + nrmtype + ",%s" % val_name)
        return self._mapdl.scalar_param(val_name)

    def axpy(self, op, val1, val2):
        cmd = "*AXPY," + str(val1) + ",0," + op.id + "," + str(val2) + ",0," + self.id
        self._mapdl.log.info(f">> Call Mapdl to perform AXPY operation")
        self._mapdl.run(cmd)
        return self

    def __add__(self, op2):
        opout = self.copy()
        self._mapdl.log.info(f">> Call Mapdl to perform AXPY operation")
        self._mapdl.run("*AXPY,1,0," + op2.id + ",1,0," + opout.id)
        return opout

    def __iadd__(self, op):
        return self.axpy(op, 1, 1)

    def __isub__(self, op):
        return self.axpy(op, -1, 1)

    def __imul__(self, val):
        self._mapdl.log.info("Call Mapdl to scale the object")
        self._mapdl.run("*SCAL," + self.id + "," + str(val))
        return self

    def get(self):
        """Get values from Mapdl into a numpy.array"""
        raise NotImplementedError

    def put(self):
        """Put values from Python to Mapdl"""
        raise NotImplementedError


class AnsVec(ApdlMathObj):
    """APDLMath Vector Object"""
    def __init__(self, id, mapdl, dtype=np.double, init=None):
        ApdlMathObj.__init__(self, id, mapdl, ObjType.VEC)

        if init not in ['ones', 'zeros', 'rand', None]:
            raise ValueError('Invalid init option.  Should be "ones", "zeros", "rand", or None')

        if (init == "rand"):
            self.rand()
        elif (init == "ones"):
            self.ones()
        elif (init == "zeros"):
            self.zeros()

    @property
    def size(self):
        return int(self._mapdl.scalar_param(self.id + "_DIM"))

    def __repr__(self):
        return "APDLMath Vector Size %s" % self.size

    def __getitem__(self, num):
        cmd = "pyval=" + self.id + "(" + str(num+1) + ")"
        self._mapdl.run(cmd)
        return self._mapdl.scalar_param("pyval")

    def __mul__(self, vec2):
        cmd = "*DOT," + self.id + "," + vec2.id + ",py_val"
        self._mapdl.run(cmd)
        return self._mapdl.scalar_param("py_val")

    def copy(self):
        """Return a copy of this vector"""
        return AnsVec(ApdlMathObj.copy(self), self._mapdl)

    def dot(self, vec):
        """Dot product with another ansys vector object

        Parameters
        ----------
        vec : ansys.mapdl.math.AnsVec
            Ansys vector object.

        Returns
        -------
        dot_product : float
            Dot product between this vector and the other vector.
        """
        if not isinstance(vec, AnsVec):
            raise TypeError('Must be an Ansys vector object')

        cmd = "*DOT," + self.id + "," + vec.id + ",py_val"
        self._mapdl.run(cmd)
        return self._mapdl.scalar_param("py_val")

    def asarray(self):
        """Returns vector as a numpy array

        Examples
        --------
        >>> from ansys.mapdl import Mapdl
        >>> mm = mapdl.math()
        >>> v = mm.ones(10)
        >>> v.asarray()
        [1. 1. 1. 1. 1. 1. 1. 1. 1. 1.]
        """
        return self._mapdl._vec_data(self.id)


class AnsMat(ApdlMathObj):
    """APDLMath Matrix Object"""

    def __init__(self, id, mapdl, type=ObjType.DMAT):
        ApdlMathObj.__init__(self, id, mapdl, type)

    @property
    def nrow(self):
        return int(self._mapdl.scalar_param(self.id + "_ROWDIM"))

    @property
    def ncol(self):
        return int(self._mapdl.scalar_param(self.id + "_COLDIM"))

    @property
    def size(self):
        return self.nrow*self.ncol

    @property
    def shape(self):
        """Returns a numpy-like shape.

        Tuple of (rows and columns)
        """
        return (self.nrow, self.ncol)

    def sym(self):
        return True

    def __repr__(self):
        return "APDLMath Matrix %d x %d" % (self.nrow, self.ncol)

    def __mul__(self, vec):
        vout = vec.copy()
        cmd = "*MULT," + self.id + ",," + vec.id + ",," + vout.id
        self._mapdl.log.info("Call Mapdl to perform MV Product")
        self._mapdl.run(cmd)
        return vout

    def copy(self):
        """Return a copy of this matrix"""
        return AnsMat(ApdlMathObj.copy(self), self._mapdl, self.type)

    def __getitem__(self, num):
        name = id_generator()
        cmd = "*VEC," + name + ",D,LINK," + self.id + "," + str(num+1)
        self._mapdl.run(cmd)
        return AnsVec(name, self._mapdl)

    def asarray(self):
        """Returns matrix as a numpy array

        Examples
        --------
        >>> from ansys.mapdl import Mapdl
        >>> mm = mapdl.math()
        >>> m = mm.ones(2,2)
        >>> m.asarray()
        """
        return self._mapdl._mat_data(self.id)


class AnsSolver(ApdlMathObj):
    """APDLMath Solver Class"""
    def __repr__(self):
        return "APDLMath Linear Solver"

    def __del__(self):
        self._mapdl.log.debug("Deleting the MAPDL Solver Object")
        self._mapdl.run("*FREE," + self.id)

    def factorize(self, M, Algo=None):
        """Factorize a matrix"""
        if not Algo:
            if (M.type == ObjType.DMAT):
                Algo = "LAPACK"
            elif (M.type == ObjType.SMAT):
                Algo = "DSP"
        self._mapdl.run("*LSENGINE," + Algo + "," + self.id + "," + M.id)
        self._mapdl.log.info("Factorizing using " + Algo + " Package ..")
        self._mapdl.run("*LSFACTOR," + self.id)

    def solve(self, B, X=None):
        if not X:
            X = B.copy()
        self._mapdl.log.info("Solving")
        self._mapdl.run("*LSBAC," + self.id + "," + B.id + "," + X.id)
        return X


def rand(obj):
    """Set all values of a mapdl math object to random values

    Parameters
    ----------
    obj : ansys.math.MapdlMath object
        MapdlMath object
    """
    obj._mapdl.cmd("*INIT," + obj.id + ",RAND")


def solve(Mat, B, X=None, Algo=None):
    # print(">> Call Mapdl Solver:")
    Solver = AnsSolver(id_generator(), Mat._mapdl)
    Solver.factorize(Mat, Algo)
    if not X:
        X = B.copy()
    X = Solver.solve(B, X)
    # print(">> Done")

    del Solver
    return X


def dot(vec1, vec2):
    """Dot product between two ANSYS vector objects

    Parameters
    vec1 : ansys.mapdl.math.AnsVec
        Ansys vector object.

    vec1 : ansys.mapdl.math.AnsVec
        Ansys vector object.

    Returns
    -------
    dot_product : float
        Dot product between the two vectors

    """
    if (vec1.type != ObjType.VEC or vec2.type != ObjType.VEC):
        raise Exception("Both objects must be ANSYS vectors")

    mapdl = vec1._mapdl
    mapdl.run("*DOT," + vec1.id + "," + vec2.id + ",py_val")
    return mapdl.scalar_param("py_val")
