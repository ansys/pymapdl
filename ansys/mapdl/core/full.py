"""
Used fortran header file for item definitions
/usr/ansys_inc/v150/ansys/customize/include/fdfull.inc

"""
import os
import warnings

import numpy as np

from pyansys import _binary_reader
from pyansys.common import (read_table, AnsysBinary, parse_header, two_ints_to_long,
                            read_standard_header)


FRONTAL_FULL_HEADER_KEYS = [
    'fun04', 'neqn', 'nmrow', 'nmatrx', 'kan',
    'wfmax', 'lenbac', 'numdof', 'jcgtrmL', 'jcgtrmH',
    'lumpm', 'jcgeqn', 'jcgtrm', 'keyuns', 'extopt',
    'keyse', 'sclstf', 'nxrows', 'ptrIDXl', 'ptrIDXh',
    'ncefull', 'ncetrm', 'ptrENDl', 'ptrENDh', '0'
]

SYMBOLIC_FULL_HEADER_KEYS = [
    'fun04', 'neqn', 'nmrow', 'nmatrx', 'kan',
    'wfmax', 'lenbac', 'numdof', 'ntermKl', 'ntermKh',  # (10)
    'lumpm', 'nmrow', 'ntermK_', 'keyuns', 'extopt',
    'keyse', 'sclstf', 'nxrows', 'ptrSTFl', 'ptrSTFh',  # (20)
    'ncefull', 'ntermMh', 'ptrENDl', 'ptrENDh', 'ptrIRHSl',
    'ptrIRHSh', 'ptrMASl', 'ptrMASh', 'ptrDMPl', 'ptrDMPh',  # (30)
    'ptrCEl', 'ptrCEh', 'nNodes', 'ntermMl', 'ntermDl',
    'ptrDOFl', 'ptrDOFh', 'ptrRHSl', 'ptrRHSh', 'ntermDh',   # (40)
    'ngMaxNZ', 'ptrNGPHl', 'ptrNGPHh', 'minKdiag', 'maxKdiag',
    'minMdiag', 'maxMdiag', 'minDdiag', 'maxDdiag', 'ngTerml',  # (50)
    'ngTermh', 'ngTermCl', 'ngTermCh', 'ptrDIAGKl', 'ptrDIAGKh',
    'ptrDIAGMl', 'ptrDIAGMh', 'ptrDIAGCl', 'ptrDIAGCh', 'ptrSCLKl',  # (60)
    'ptrSCLKh', 'Glbneqn', 'distKey', 'ngTermFl', 'ngTermFh',
    'GlbnNodes', 'GlbnVars', 'GlbfAcCE', 'lcAcLen', 'GlbfCE',   # (70)
    'ptrGmtl', 'ptrGmth', 'nceGprime', 'numA12A11', 'strctChg',
    'ntermGl', 'ntermGh', 'ptrDensel', 'ptrDenseh', 'nVirtBCs',  # (80)
    'ptrVrtBCl', 'ptrVrtBCh', 'ptrMRKl', 'ptrMRKh'
]


class FullFile(AnsysBinary):
    """Stores the results of an ANSYS full file.

    Parameters
    ----------
    filename : str
        Filename of the full file to read.

    Examples
    --------
    >>> import pyansys
    >>> full = pyansys.read_binary('file.rst')
    >>> print(full)
    PyANSYS - MAPDL Full File
    Title                    : Demo
    Version                  : 20.1
    Platform                 : WINDOWS x64
    Jobname                  : file
    Matrices                 : 2
    Equations                : 345
    Nodes                    : 115
    Degrees of Freedom       : 3

    """

    def __init__(self, filename):
        """Loads full header on initialization.

        See ANSYS programmer's reference manual full header section
        for definitions of each header.

        """
        self._const = None
        self._krow = None
        self._kcol = None
        self._kdata = None
        self._mrow = None
        self._mcol = None
        self._mdata = None
        self._k = None
        self._m = None
        self._dof_ref = None

        self.filename = filename
        self._standard_header = read_standard_header(self.filename)
        self._header = parse_header(self.read_record(103), SYMBOLIC_FULL_HEADER_KEYS)

        # if not self._header['fun04'] < 0:
            # raise NotImplementedError("Unable to read a frontal assembly full file")

        # Check if lumped (item 11)
        if self._header['lumpm']:
            raise NotImplementedError("Unable to read a lumped mass matrix")

        # Check if arrays are unsymmetric (item 14)
        if self._header['keyuns']:
            raise NotImplementedError("Unable to read an unsymmetric mass/stiffness matrix")

    @property
    def k(self):
        """Stiffness Matrix corresponding to sorted DOF.

        Examples
        --------
        >>> import pyansys
        >>> full = pyansys.read_binary('file.rst')
        >>> print(full.k)
        <345x345 sparse matrix of type '<class 'numpy.float64'>'
                with 7002 stored elements in Compressed Sparse Column format>
        """
        if self._k is None:
            self._load_km()
        return self._k

    @property
    def m(self):
        """Mass Matrix corresponding to sorted DOF.

        Examples
        --------
        >>> import pyansys
        >>> full = pyansys.read_binary('file.rst')
        >>> full.m
        <345x345 sparse matrix of type '<class 'numpy.float64'>'
                with 2883 stored elements in Compressed Sparse Column format>
        """
        if self._m is None:
            self._load_km()
        return self._m

    @property
    def dof_ref(self):
        """Sorted degree of freedom reference.

        Examples
        --------
        >>> import pyansys
        >>> full = pyansys.read_binary('file.rst')
        >>> full.dof_ref
        array([[  1,   0],
               [  1,   1],
               [  1,   2],
               [115,   0],
               [115,   1],
               [115,   2]], dtype=int32)

        Notes
        -----
        Obtain the unsorted degree of freedom reference with
        >>> dof_ref, k, m = sparse_full.load_km(sort=False)
        """
        if self._dof_ref is None:
            self._load_km()
        return self._dof_ref

    @property
    def const(self):
        """Constrained DOF
        Returns the node number and DOF constrained in ANSYS.

        Examples
        --------
        >>> full.const
        array([], shape=(0, 2), dtype=int32)
        """
        if self._const is None:
            self._load_km()
        return self._const

    def load_km(self, as_sparse=True, sort=False):
        """Load and construct mass and stiffness matrices from an
        ANSYS full file.

        Parameters
        ----------
        as_sparse : bool, optional
            Outputs the mass and stiffness matrices as scipy csc
            sparse arrays when True by default.

        sort : bool, optional
            Rearranges the k and m matrices such that the rows
            correspond to to the sorted rows and columns in dor_ref.
            Also sorts dor_ref.

        Returns
        -------
        dof_ref : (n x 2) np.int32 array
            This array contains the node and degree corresponding to
            each row and column in the mass and stiffness matrices.
            In a 3 DOF analysis the dof integers will correspond to:
            0 - x
            1 - y
            2 - z
            Sort these values by node number and DOF by enabling the
            sort parameter.

        k : (n x n) np.float or scipy.csc array
            Stiffness array

        m : (n x n) np.float or scipy.csc array
            Mass array

        Examples
        --------
        >>> import pyansys
        >>> full = pyansys.read_binary('file.rst')
        >>> dof_ref, k, m = full.load_km()
        >>> print(k)
        (0, 0)       163408119.6581276
        (0, 1)               0.0423270
        (1, 1)       163408119.6581276
        :	:
        (342, 344)     6590544.8717949
        (343, 344)    -6590544.8717950
        (344, 344)    20426014.9572689

        Notes
        -----
        Constrained entries are removed from the mass and stiffness
        matrices.

        Constrained DOF can be accessed from ``const``, which returns
        the node number and DOF constrained in ANSYS.
        """
        if not os.path.isfile(self.filename):
            raise Exception('%s not found' % self.filename)

        if as_sparse:
            try:
                from scipy.sparse import csc_matrix, coo_matrix
            except ImportError:
                raise ImportError('Unable to load scipy, use ``load_km`` with '
                                  '``as_sparse=False``')

        # number of terms in stiffness matrix
        ntermK = two_ints_to_long(self._header['ntermKl'], self._header['ntermKh'])

        ptrSTF = self._header['ptrSTF']  # Location of stiffness matrix
        ptrMAS = self._header['ptrMAS']  # Location in file to mass matrix

        # number of terms in mass matrix
        ntermM = two_ints_to_long(self._header['ntermMl'], self._header['ntermMh'])
        ptrDOF = self._header['ptrDOF']  # pointer to DOF info

        # DOF information
        with open(self.filename, 'rb') as f:
            read_table(f, skip=True)  # standard header
            read_table(f, skip=True)  # full header
            read_table(f, skip=True)  # number of degrees of freedom

            # Nodal equivalence table
            neqv = read_table(f, cython=True)

            # read number of degrees of freedom for each node and constant tables
            f.seek(ptrDOF*4)
            ndof = read_table(f, cython=True)
            const = read_table(f, cython=True)

        # degree of freedom reference and number of degress of freedom per node
        dof_ref = [ndof, neqv]
        self.ndof = ndof

        # Read k and m blocks (see help(ReadArray) for block description)
        if ntermK:
            krow, kcol, kdata = _binary_reader.read_array(self.filename,
                                                          ptrSTF,
                                                          ntermK,
                                                          self.neqn,
                                                          const)
        else:
            warnings.warn('Missing stiffness matrix')
            kdata = None

        if ntermM:
            mrow, mcol, mdata = _binary_reader.read_array(self.filename,
                                                          ptrMAS,
                                                          ntermM,
                                                          self.neqn,
                                                          const)
        else:
            warnings.warn('Missing mass matrix')
            mdata = None

        # remove constrained entries
        if np.any(const < 0):
            if kdata is not None:
                remove = np.nonzero(const < 0)[0]
                mask = ~np.logical_or(np.in1d(krow, remove), np.in1d(kcol, remove))
                krow = krow[mask]
                kcol = kcol[mask]
                kdata = kdata[mask]

            if mdata is not None:
                mask = ~np.logical_or(np.in1d(mrow, remove), np.in1d(mcol, remove))
                mrow = mrow[mask]
                mcol = mcol[mask]
                mdata = mdata[mask]


        # sort nodal equivalence
        dof_ref, index, nref, dref = _binary_reader.sort_nodal_eqlv(self.neqn,
                                                                    neqv, ndof)

        # store constrained dof information
        unsort_dof_ref = np.vstack((nref, dref)).T
        self._const = unsort_dof_ref[const < 0]

        if sort:  # make sorting the same as ANSYS rdfull would output
            # resort to make in upper triangle
            krow = index[krow]
            kcol = index[kcol]
            krow, kcol = np.sort(np.vstack((krow, kcol)), 0)

            if mdata is not None:
                mrow = index[mrow]
                mcol = index[mcol]
                mrow, mcol = np.sort(np.vstack((mrow, mcol)), 0)

        else:
            dof_ref = unsort_dof_ref

        # store data for later reference
        if kdata is not None:
            self._krow = krow
            self._kcol = kcol
            self._kdata = kdata
        if mdata is not None:
            self._mrow = mrow
            self._mcol = mcol
            self._mdata = mdata

        # output as a sparse matrix
        if as_sparse:

            if kdata is not None:
                k = coo_matrix((self.neqn,) * 2)
                k.data = kdata  # data has to be set first
                k.row = krow
                k.col = kcol

                # convert to csc matrix (generally faster for sparse solvers)
                k = csc_matrix(k)
            else:
                k = None

            if mdata is not None:
                m = coo_matrix((self.neqn,) * 2)
                m.data = mdata
                m.row = mrow
                m.col = mcol

                # convert to csc matrix (generally faster for sparse solvers)
                m = csc_matrix(m)
            else:
                m = None

        else:
            if kdata is not None:
                k = np.zeros((self.neqn,) * 2)
                k[krow, kcol] = kdata
            else:
                k = None

            if mdata is not None:
                m = np.zeros((self.neqn,) * 2)
                m[mrow, mcol] = mdata
            else:
                m = None

        return dof_ref, k, m

    @property
    def neqn(self):
        """Number of equations

        Examples
        --------
        >>> full.neqn
        963
        """
        return self._header['neqn']

    @property
    def load_vector(self):
        """The load vector

        Examples
        --------
        >>> full.load_vector
        array([0., 0., 0., ..., 0., 0., 0.])
        """
        return self.read_record(self._header['ptrRHS'])[:self.neqn]

    def _load_km(self):
        """Loads the matrices with sorted DOF"""
        self._dof_ref, self._k, self._m = self.load_km(sort=True)

    def __str__(self):
        rst_info = ['PyANSYS - MAPDL Full File']

        def add_info(key, value):
            rst_info.append('{:<25s}: {:s}'.format(key, str(value)))

        keys = ['title', 'subtitle']
        for key in keys:
            value = self._standard_header[key]
            if value:
                add_info(key.capitalize(), value)

        add_info('Version', self._standard_header['verstring'])
        add_info('Platform', self._standard_header['machine'])
        add_info('Jobname', self._standard_header['jobname'])
        add_info('Matrices', self._header['nmatrx'])
        add_info('Equations', self._header['neqn'])
        add_info('Nodes', self._header['nNodes'])
        add_info('Degrees of Freedom', self._header['numdof'])

        return '\n'.join(rst_info)
