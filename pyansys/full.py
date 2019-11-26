"""
Used fortran header file for item definitions
/usr/ansys_inc/v150/ansys/customize/include/fdfull.inc

"""
import os
import warnings

import numpy as np

from pyansys import _binary_reader
from pyansys.common import read_table, AnsysBinary, parse_header, two_ints_to_long


FRONTAL_FULL_HEADER_KEYS = ['fun04', 'neqn', 'nmrow', 'nmatrx', 'kan',
                    'wfmax', 'lenbac', 'numdof', 'jcgtrmL', 'jcgtrmH',
                    'lumpm', 'jcgeqn', 'jcgtrm', 'keyuns', 'extopt',
                    'keyse', 'sclstf', 'nxrows', 'ptrIDXl', 'ptrIDXh',
                    'ncefull', 'ncetrm', 'ptrENDl', 'ptrENDh', '0',]

SYMBOLIC_FULL_HEADER_KEYS = ['fun04', 'neqn', 'nmrow', 'nmatrx', 'kan',
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
                             'ptrVrtBCl', 'ptrVrtBCh', 'ptrMRKl', 'ptrMRKh']


class FullFile(AnsysBinary):
    """Stores the results of an ANSYS full file.

    Parameters
    ----------
    filename : str
        Filename of the full file to read.

    Examples
    --------
    >>> full = pyansys.read_binary('file.rst')
    """

    def __init__(self, filename):
        """Loads full header on initialization.

        See ANSYS programmer's reference manual full header section for
        definitions of each header.

        """
        self.krow = None
        self.kcol = None
        self.kdata = None
        self.mrow = None
        self.mcol = None
        self.mdata = None
        self.ndof = None
        self.const = None

        self.filename = filename
        self.header = parse_header(self.read_record(103), SYMBOLIC_FULL_HEADER_KEYS)

        # if not self.header['fun04'] < 0:
            # raise NotImplementedError("Unable to read a frontal assembly full file")

        # Check if lumped (item 11)
        if self.header['lumpm']:
            raise NotImplementedError("Unable to read a lumped mass matrix")

        # Check if arrays are unsymmetric (item 14)
        if self.header['keyuns']:
            raise NotImplementedError("Unable to read an unsymmetric mass/stiffness matrix")

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
            In a 3 DOF analysis the dof intergers will correspond to:
            0 - x
            1 - y
            2 - z
            Sort these values by node number and DOF by enabling the
            sort parameter.

        k : (n x n) np.float or scipy.csc array
            Stiffness array

        m : (n x n) np.float or scipy.csc array
            Mass array

        Notes
        -----
        Constrained entries are removed from the mass and stiffness
        matrices.

        Constrained DOF can be accessed with self.const, which returns
        the node number and DOF constrained in ANSYS.
        """
        if not os.path.isfile(self.filename):
            raise Exception('%s not found' % self.filename)

        # see if
        if as_sparse:
            try:
                from scipy.sparse import csc_matrix, coo_matrix
            except BaseException:
                raise Exception('Unable to load scipy, use "as_sparse=False"')

        # Get header details
        neqn = self.header['neqn']  # Number of equations

        # number of terms in stiffness matrix
        ntermK = two_ints_to_long(self.header['ntermKl'], self.header['ntermKh'])

        ptrSTF = self.header['ptrSTF']  # Location of stiffness matrix
        ptrMAS = self.header['ptrMAS']  # Location in file to mass matrix

        # number of terms in mass matrix
        ntermM = two_ints_to_long(self.header['ntermMl'], self.header['ntermMh'])
        ptrDOF = self.header['ptrDOF']  # pointer to DOF info

        # DOF information
        with open(self.filename, 'rb') as f:
            read_table(f, skip=True)  # standard header
            read_table(f, skip=True)  # full header
            read_table(f, skip=True)  # number of degrees of freedom
            neqv = read_table(f)  # Nodal equivalence table

            f.seek(ptrDOF*4)
            ndof = read_table(f)
            const = read_table(f)

        # degree of freedom reference and number of degress of freedom per node
        dof_ref = [ndof, neqv]
        self.ndof = ndof

        # Read k and m blocks (see help(ReadArray) for block description)
        if ntermK:
            krow, kcol, kdata = _binary_reader.read_array(self.filename,
                                                          ptrSTF,
                                                          ntermK,
                                                          neqn,
                                                          const)
        else:
            warnings.warn('Missing stiffness matrix')
            kdata = None

        if ntermM:
            mrow, mcol, mdata = _binary_reader.read_array(self.filename,
                                                          ptrMAS,
                                                          ntermM,
                                                          neqn,
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
        dof_ref, index, nref, dref = _binary_reader.sort_nodal_eqlv(neqn, neqv, ndof)

        # store constrained dof information
        unsort_dof_ref = np.vstack((nref, dref)).T
        self.const = unsort_dof_ref[const < 0]

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
            self.krow = krow
            self.kcol = kcol
            self.kdata = kdata
        if mdata is not None:
            self.mrow = mrow
            self.mcol = mcol
            self.mdata = mdata

        # output as a sparse matrix
        if as_sparse:

            if kdata is not None:
                k = coo_matrix((neqn,) * 2)
                k.data = kdata  # data has to be set first
                k.row = krow
                k.col = kcol

                # convert to csc matrix (generally faster for sparse solvers)
                k = csc_matrix(k)
            else:
                k = None

            if mdata is not None:
                m = coo_matrix((neqn,) * 2)
                m.data = mdata
                m.row = mrow
                m.col = mcol

                # convert to csc matrix (generally faster for sparse solvers)
                m = csc_matrix(m)
            else:
                m = None

        else:
            if kdata is not None:
                k = np.zeros((neqn,) * 2)
                k[krow, kcol] = kdata
            else:
                k = None

            if mdata is not None:
                m = np.zeros((neqn,) * 2)
                m[mrow, mcol] = mdata
            else:
                m = None

        return dof_ref, k, m
