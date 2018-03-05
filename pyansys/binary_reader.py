"""
Used v150/ansys/customize/user/ResRd.F to help build this interface

"""
import os
import numpy as np
import warnings
import logging
import ctypes
from ctypes import c_int64

import vtkInterface
from pyansys import _parsefull
from pyansys import _rstHelper
from pyansys import _parser

try:
    import vtk
    vtkloaded = True
except BaseException:
    warnings.warn('Cannot load vtk\nWill be unable to display results.')
    vtkloaded = False

# Create logger
log = logging.getLogger(__name__)
log.setLevel('DEBUG')


# Pointer information from ansys interface manual
# =============================================================================
# Individual element index table
e_table = ['ptrEMS', 'ptrENF', 'ptrENS', 'ptrENG', 'ptrEGR', 'ptrEEL',
           'ptrEPL', 'ptrECR', 'ptrETH', 'ptrEUL', 'ptrEFX', 'ptrELF',
           'ptrEMN', 'ptrECD', 'ptrENL', 'ptrEHC', 'ptrEPT', 'ptrESF',
           'ptrEDI', 'ptrETB', 'ptrECT', 'ptrEXY', 'ptrEBA', 'ptrESV',
           'ptrMNL']

"""
ptrEMS - pointer to misc. data
ptrENF - pointer to nodal forces
ptrENS - pointer to nodal stresses
ptrENG - pointer to volume and energies
ptrEGR - pointer to nodal gradients
ptrEEL - pointer to elastic strains
ptrEPL - pointer to plastic strains
ptrECR - pointer to creep strains
ptrETH - pointer to thermal strains
ptrEUL - pointer to euler angles
ptrEFX - pointer to nodal fluxes
ptrELF - pointer to local forces
ptrEMN - pointer to misc. non-sum values
ptrECD - pointer to element current densities
ptrENL - pointer to nodal nonlinear data
ptrEHC - pointer to calculated heat generations
ptrEPT - pointer to element temperatures
ptrESF - pointer to element surface stresses
ptrEDI - pointer to diffusion strains
ptrETB - pointer to ETABLE items(post1 only)
ptrECT - pointer to contact data
ptrEXY - pointer to integration point locations
ptrEBA - pointer to back stresses
ptrESV - pointer to state variables
ptrMNL - pointer to material nonlinear record
"""

# element types with stress outputs
validENS = [45, 92, 95, 181, 185, 186, 187]


class FullReader(object):
    """
    Stores the results of an ANSYS full file.

    Parameters
    ----------
    filename : str
        Filename of the full file to read.

    Examples
    --------
    >>> full = FullReader('file.rst')

    """

    def __init__(self, filename):
        """
        Loads full header on initialization

        See ANSYS programmer's reference manual full header section for
        definitions of each header.

        """

        # check if file exists
        if not os.path.isfile(filename):
            raise Exception('{:s} not found'.format(filename))

        self.filename = filename
        self.header = _parsefull.ReturnHeader(filename)

        # Check if lumped (item 11)
        if self.header[11]:
            raise Exception(
                "Unable to read a lumped mass matrix.  Terminating.")

        # Check if arrays are unsymmetric (item 14)
        if self.header[14]:
            raise Exception(
                "Unable to read an unsymmetric mass/stiffness matrix.")

    def LoadKM(self, as_sparse=True, utri=True):
        """
        Load and construct mass and stiffness matrices from an ANSYS full file.

        Parameters
        ----------
        as_sparse : bool, optional
            Outputs the mass and stiffness matrices as scipy csc sparse arrays
            when True by default.

        utri : bool, optional
            Outputs only the upper triangle of both the mass and stiffness
            arrays.

        Returns
        -------
        dof_ref : (n x 2) np.int32 array
            This array contains the node and degree corresponding to each row
            and column in the mass and stiffness matrices.  When the sort
            parameter is set to True this array will be sorted by node number
            first and then by the degree of freedom.  In a 3 DOF analysis the
            intergers will correspond to:
            0 - x
            1 - y
            2 - z

        k : (n x n) np.float or scipy.csc array
            Stiffness array

        m : (n x n) np.float or scipy.csc array
            Mass array
        """
        # check file exists
        if not os.path.isfile(self.filename):
            raise Exception('%s not found' % self.filename)

        # see if
        if as_sparse:
            try:
                from scipy.sparse import csc_matrix, coo_matrix
            except BaseException:
                raise Exception('Unable to load scipy, matricies will be full')
                as_sparse = False

        # Get header details
        neqn = self.header[2]  # Number of equations
        ntermK = self.header[9]  # number of terms in stiffness matrix
        ptrSTF = self.header[19]  # Location of stiffness matrix
        ptrMAS = self.header[27]  # Location in file to mass matrix
        nNodes = self.header[33]  # Number of nodes considered by assembly
        ntermM = self.header[34]  # number of terms in mass matrix
        ptrDOF = self.header[36]  # pointer to DOF info

        # get details for reading the mass and stiffness arrays
        node_info = _rstHelper.FullNodeInfo(self.filename, ptrDOF, nNodes,
                                            neqn)

        nref, dref, index_arr, const, ndof = node_info
        dof_ref = np.vstack((nref, dref)).T  # stack these references

        # Read k and m blocks (see help(ReadArray) for block description)
        if ntermK:
            k_block = _rstHelper.ReadArray(self.filename, ptrSTF, ntermK, neqn,
                                           index_arr)
            k_diag = k_block[3]
            k_data_diag = k_block[4]
        else:
            warnings.warn('Missing stiffness matrix')
            k_block = None

        if ntermM:
            m_block = _rstHelper.ReadArray(self.filename, ptrMAS, ntermM, neqn,
                                           index_arr)
            m_diag = m_block[3]
            m_data_diag = m_block[4]
        else:
            warnings.warn('Missing mass matrix')
            m_block = None

        self.m_block = m_block
        self.k_block = k_block

        # assemble data
        if utri:
            if k_block:
                # stiffness matrix
                krow = np.hstack((k_block[1], k_diag))  # row and diag
                kcol = np.hstack((k_block[0], k_diag))  # col and diag
                kdata = np.hstack((k_block[2], k_data_diag))  # data and diag

            if m_block:
                # mass matrix
                mrow = np.hstack((m_block[1], m_diag))  # row and diag
                mcol = np.hstack((m_block[0], m_diag))  # col and diag
                mdata = np.hstack((m_block[2], m_data_diag))  # data and diag

        else:
            if k_block:
                # stiffness matrix
                krow = np.hstack((k_block[0], k_block[1], k_diag))
                kcol = np.hstack((k_block[1], k_block[0], k_diag))
                kdata = np.hstack((k_block[2], k_block[2], k_data_diag))

            if m_block:
                # mass matrix
                mrow = np.hstack((m_block[0], m_block[1], m_diag))
                mcol = np.hstack((m_block[1], m_block[0], m_diag))
                mdata = np.hstack((m_block[2], m_block[2], m_data_diag))

        # store data for later reference
        if k_block:
            self.krow = krow
            self.kcol = kcol
            self.kdata = kdata
        if m_block:
            self.mrow = mrow
            self.mcol = mcol
            self.mdata = mdata

        # number of dimentions
        ndim = nref.size

        # output as a sparse matrix
        if as_sparse:

            if k_block:
                k = coo_matrix((ndim,) * 2)
                k.data = kdata  # data has to be set first
                k.row = krow
                k.col = kcol

                # convert to csc matrix (generally faster for sparse solvers)
                k = csc_matrix(k)
            else:
                k = None

            if m_block:
                m = coo_matrix((ndim,) * 2)
                m.data = mdata
                m.row = mrow
                m.col = mcol

                # convert to csc matrix (generally faster for sparse solvers)
                m = csc_matrix(m)
            else:
                m = None

        else:
            if k_block:
                k = np.zeros((ndim,) * 2)
                k[krow, kcol] = kdata
            else:
                k = None

            if m_block:
                m = np.zeros((ndim,) * 2)
                m[mrow, mcol] = mdata
            else:
                m = None

        # store if constrained and number of degrees of freedom per node
        self.const = const < 0
        self.ndof = ndof

        return dof_ref, k, m


class ResultReader(object):
    """
    Object to control the reading of ANSYS results written to a fortran
    formatted binary file file

    Parameters
    ----------
    filename : string
        Filename of the ANSYS binary result file.

    logger : bool, optional
        Enables logging if True.  Debug feature.

    load_geometry : bool, optional
        Loads geometry using vtk by default

    """

    def __init__(self, filename, load_geometry=True):
        """
        Loads basic result information from result file and initializes result
        object.

        """
        # Store filename result header items
        self.filename = filename
        self.resultheader = GetResultInfo(filename)

        # Get the total number of results and log it
        self.nsets = len(self.resultheader['rpointers'])
        string = 'There are {:d} results in this file'.format(self.nsets)
        log.debug(string)

        # Get indices to resort nodal and element results
        self.sidx = np.argsort(self.resultheader['neqv'])
        self.sidx_elem = np.argsort(self.resultheader['eeqv'])

        # Store node numbering in ANSYS
        self.nnum = self.resultheader['neqv'][self.sidx]
        self.enum = self.resultheader['eeqv'][self.sidx_elem]

        # Store time values for later retrival
        self.GetTimeValues()

        # store geometry for later retrival
        if load_geometry:
            self.StoreGeometry()

        if self.resultheader['nSector'] > 1 and load_geometry:
            self.iscyclic = True

            # Add cyclic properties
            self.AddCyclicProperties()

    def Plot(self):
        """ plots result geometry """
        self.grid.Plot()

    def AddCyclicProperties(self):
        """ Adds cyclic properties to result object """
        # ansys's duplicate sector contains nodes from the second half of the
        # node numbering
        #
        # ansys node numbering for the duplicate sector is
        # nnum.min() + nnum.max()
        # where nnum is the node numbering for the master sector

        # master sector max node number
        num_master_max = self.nnum[int(self.nnum.size / 2) - 1]

        # identify master and duplicate cyclic sectors
        cells = np.arange(self.enum.size)
        dup_cells = np.where(
            np.any(
                self.geometry['elem'] > num_master_max,
                1))[0]
        mas_cells = np.setdiff1d(cells, dup_cells)
        self.sector = self.grid.ExtractSelectionCells(mas_cells)
        dup_sector = self.grid.ExtractSelectionCells(dup_cells)

        # Store the indices of the master and duplicate nodes
        self.mas_ind = self.sector.GetPointScalars('vtkOriginalPointIds')
        self.dup_ind = dup_sector.GetPointScalars('vtkOriginalPointIds')

        # store cyclic node numbers
        self.cyc_nnum = self.nnum[self.mas_ind]

        # create full rotor
        nSector = self.resultheader['nSector']

        # Copy and translate mesh
        vtkappend = vtk.vtkAppendFilter()
        rang = 360.0 / nSector
        for i in range(nSector):

            # Transform mesh
            sector = self.sector.Copy()
            sector.RotateZ(rang * i)

            vtkappend.AddInputData(sector)

        # Combine meshes and add VTK_Utilities functions
        # vtkappend.MergePointsOn()
        vtkappend.Update()
        self.rotor = vtkInterface.UnstructuredGrid(vtkappend.GetOutput())

    def GetCyclicNodalResult(self, rnum):
        """
        Returns the nodal result given a cumulative result index.

        Parameters
        ----------
        rnum : interger
            Cumulative result number.  Zero based indexing.

        Returns
        -------
        result : numpy.complex128 array
            Result is (nnod x numdof), nnod is the number of nodes in a sector
            and numdof is the number of degrees of freedom.

        Notes
        -----
        Node numbers correspond to self.cyc_nnum, where self is this result
        object

        """
        if not self.iscyclic:
            raise Exception('Result file does not contain cyclic results.')

        # get the nodal result
        r = self.GetNodalResult(rnum)

        return r[self.mas_ind] + r[self.dup_ind] * 1j

    def PlotCyclicNodalResult(
            self,
            rnum,
            phase=0,
            comp='norm',
            as_abs=False,
            label='',
            expand=True):
        """
        Plots a nodal result from a cyclic analysis.

        Parameters
        ----------
        rnum : interger
            Cumulative result number.  Zero based indexing.

        phase : float, optional
            Shifts the phase of the solution.

        comp : string, optional
            Display component to display.  Options are 'x', 'y', 'z', and
            'norm', corresponding to the x directin, y direction, z direction,
            and the combined direction (x**2 + y**2 + z**2)**0.5

        as_abs : bool, optional
            Displays the absolute value of the result.

        label: string, optional
            Annotation string to add to scalar bar in plot.

        expand : bool, optional
            Expands the solution to a full rotor when True.  Enabled by
            default.  When disabled, plots the maximum response of a single
            sector of the cyclic solution in the component of interest.


        Returns
        -------
        cpos : list
            Camera position from vtk render window.
        """

        if 'hindex' not in self.resultheader:
            raise Exception('Result file does not contain cyclic results')

        # harmonic index and number of sectors
        hindex = self.resultheader['hindex'][rnum]
        nSector = self.resultheader['nSector']

        # get the nodal result
        r = self.GetCyclicNodalResult(rnum)

        alpha = (2 * np.pi / nSector)

        if expand:
            grid = self.rotor
            d = np.empty((self.rotor.GetNumberOfPoints(), 3))
            n = self.sector.GetNumberOfPoints()
            for i in range(nSector):
                # adjust the phase of the result
                sec_sol = np.real(r) * np.cos(i * hindex * alpha + phase) -\
                    np.imag(r) * np.sin(i * hindex * alpha + phase)

                # adjust the "direction" of the x and y vectors as they're
                # being rotated
                s_x = sec_sol[:, 0] * np.cos(alpha * i + phase) -\
                    sec_sol[:, 1] * np.sin(alpha * i + phase)
                s_y = sec_sol[:, 0] * np.sin(alpha * i + phase) +\
                    sec_sol[:, 1] * np.cos(alpha * i + phase)
                sec_sol[:, 0] = s_x
                sec_sol[:, 1] = s_y

                d[i * n:(i + 1) * n] = sec_sol

        else:
            # plot the max response for a single sector
            grid = self.sector

            n = np.sum(r * r, 1)

            # rotate the response based on the angle to maximize the highest
            # responding node
            angle = np.angle(n[np.argmax(np.abs(n))])
            d = np.real(r) * np.cos(angle + phase) -\
                np.imag(r) * np.sin(angle + phase)

            d = -d

        # Process result
        if comp == 'x':
            d = d[:, 0]
            stitle = 'X {:s}'.format(label)

        elif comp == 'y':
            d = d[:, 1]
            stitle = 'Y {:s}'.format(label)

        elif comp == 'z':
            d = d[:, 2]
            stitle = 'Z {:s}'.format(label)

        else:
            # Normalize displacement
            d = d[:, :3]
            d = (d * d).sum(1)**0.5

            stitle = 'Normalized\n{:s}'.format(label)

        if as_abs:
            d = np.abs(d)

        # setup text
        ls_table = self.resultheader['ls_table']
        freq = self.GetTimeValues()[rnum]
        text = 'Cumulative Index: {:3d}\n'.format(ls_table[rnum, 2])
        text += 'Loadstep:         {:3d}\n'.format(ls_table[rnum, 0])
        text += 'Substep:          {:3d}\n'.format(ls_table[rnum, 1])
        text += 'Harmonic Index:   {:3d}\n'.format(hindex)
        text += 'Frequency:      {:10.4f} Hz'.format(freq)

        # plot
        plobj = vtkInterface.PlotClass()
        plobj.AddMesh(grid, scalars=d, stitle=stitle, flipscalars=True,
                      interpolatebeforemap=True)
        plobj.AddText(text, fontsize=20)
        plobj.Plot()

    def ResultsProperties(self):
        """
        Logs results available in the result file and returns a dictionary
        of available results

        Logging must be enabled for the results of the check to be shown in the
        console.

        Returns
        -------
        result_check : dict
            Dictionary indicating the availability of results.

        """

        # check number of results
        log.debug(
            'There are {:d} results in this file'.format(
                self.nsets))

        if self.resultheader['nSector'] > 1:
            log.debug('Contains results from a cyclic analysis with:')
            log.debug('\t{:d} sectors'.format(self.resultheader['nSector']))

        return {'Number of Results': self.nsets}

    def PlotNodalResult(self, rnum, comp='norm', as_abs=False, label=''):
        """
        Plots a nodal result.

        Parameters
        ----------
        rnum : int
            Cumulative result number.  Zero based indexing.

        comp : str, optional
            Display component to display.  Options are 'x', 'y', 'z', and
            'norm', corresponding to the x directin, y direction, z direction,
            and the combined direction (x**2 + y**2 + z**2)**0.5

        as_abs : bool, optional
            Displays the absolute value of the result.

        label: string, optional
            Annotation string to add to scalar bar in plot.

        Returns
        -------
        cpos : list
            Camera position from vtk render window.

        """
        if not vtkloaded:
            raise Exception('Cannot plot without VTK')

        # Load result from file
        result = self.GetNodalResult(rnum)

        # Process result
        if comp == 'x':
            d = result[:, 0]
            stitle = 'X {:s}'.format(label)

        elif comp == 'y':
            d = result[:, 1]
            stitle = 'Y {:s}'.format(label)

        elif comp == 'z':
            d = result[:, 2]
            stitle = 'Z {:s}'.format(label)

        else:
            # Normalize displacement
            d = result[:, :3]
            d = (d * d).sum(1)**0.5

            stitle = 'Normalized\n{:s}'.format(label)

        if as_abs:
            d = np.abs(d)

        # setup text
        ls_table = self.resultheader['ls_table']
        timevalue = self.GetTimeValues()[rnum]
        text = 'Cumulative Index: {:3d}\n'.format(ls_table[rnum, 2])
        text += 'Loadstep:        {:3d}\n'.format(ls_table[rnum, 0])
        text += 'Substep:         {:3d}\n'.format(ls_table[rnum, 1])
        text += 'Time Value:      {:10.4f}'.format(timevalue)

        plobj = vtkInterface.PlotClass()
        plobj.AddMesh(self.grid, scalars=d, stitle=stitle,
                      flipscalars=True, interpolatebeforemap=True)
        plobj.AddText(text, fontsize=20)

        # return camera position
        return plobj.Plot()

    def GetTimeValues(self):
        """
        Returns table of time values for results.  For a modal analysis, this
        corresponds to the frequencies of each mode.

        Returns
        -------
        tvalues : np.float64 array
            Table of time values for results.  For a modal analysis, this
            corresponds to the frequencies of each mode.

        """
        endian = self.resultheader['endian']
        ptrTIMl = self.resultheader['ptrTIMl']

        # Load values if not already stored
        if not hasattr(self, 'tvalues'):

            # Seek to start of time result table
            f = open(self.filename, 'rb')

            f.seek(ptrTIMl * 4 + 8)
            self.tvalues = np.fromfile(f, endian + 'd', self.nsets)

            f.close()

        return self.tvalues

    def GetNodalResult(self, rnum, sort=True):
        """
        Returns the nodal result for a result number

        Parameters
        ----------
        rnum : interger
            Cumulative result number.  Zero based indexing.

        sort : bool, optional
            Resorts the results so that the results correspond to the sorted
            node numbering (self.nnum) (default).  If left unsorted, results
            correspond to the nodal equivalence array self.resultheader['neqv']

        Returns
        -------
        result : numpy.float array
            Result is (nnod x numdof), or number of nodes by degrees of freedom

        """
        # Get info from result header
        endian = self.resultheader['endian']
        numdof = self.resultheader['numdof']
        nnod = self.resultheader['nnod']
        rpointers = self.resultheader['rpointers']

        # Check if result is available
        if rnum > self.nsets - 1:
            raise Exception(
                'There are only {:d} results in the result file.'.format(
                    self.nsets))

        # Read a result
        f = open(self.filename, 'rb')

        # Seek to result table and to get pointer to DOF results of result
        # table
        f.seek((rpointers[rnum] + 12) * 4)  # item 11
        ptrNSLl = np.fromfile(f, endian + 'i', 1)[0]

        # Seek and read DOF results
        f.seek((rpointers[rnum] + ptrNSLl + 2) * 4)
        nitems = nnod * numdof
        result = np.fromfile(f, endian + 'd', nitems)

        f.close()

        # Reshape to number of degrees of freedom
        r = result.reshape((-1, numdof))

        # if using a cyclic coordinate system
        if self.resultheader['csCord']:
            # compute sin and cos angles
            if not hasattr(self, 's_angle'):
                # angle of each point
                angle = np.arctan2(
                    self.geometry['nodes'][:, 1], self.geometry['nodes'][:, 0])
                angle = angle[np.argsort(self.sidx)]
                self.s_angle = np.sin(angle)  # [self.sidx]
                self.c_angle = np.cos(angle)  # [self.sidx]

            rx = r[:, 0] * self.c_angle - r[:, 1] * self.s_angle
            ry = r[:, 0] * self.s_angle + r[:, 1] * self.c_angle
            r[:, 0] = rx
            r[:, 1] = ry

        # Reorder based on sorted indexing and return
        if sort:
            r = r.take(self.sidx, 0)

        return r

    def StoreGeometry(self):
        """ Stores the geometry from the result file """

        # read in the geometry from the result file
        with open(self.filename, 'rb') as f:
            # f = open(self.filename, 'rb')
            f.seek((self.resultheader['ptrGEO'] + 2) * 4)
            geotable = np.fromfile(f, self.resultheader['endian'] + 'i', 80)
            # geotable.tolist()

            ptrLOC = geotable[26]

            # Node information
            nnod = self.resultheader['nnod']
            nnum = np.empty(nnod, np.int32)
            nloc = np.empty((nnod, 6), np.float)
            _rstHelper.LoadNodes(self.filename, ptrLOC, nnod, nloc, nnum)

            # Element Information
            nelm = geotable[4]
            ptrEID = geotable[28]
            maxety = geotable[1]

            # pointer to the element type index table
            ptrETYP = geotable[20]
            f.seek((ptrETYP + 2) * 4)
            e_type_table = np.fromfile(
                f, self.resultheader['endian'] + 'i', maxety)

            # store information for each element type
            # make these arrays large so you can reference a value via element
            # type numbering

            # number of nodes for this element type
            nodelm = np.empty(10000, np.int32)

            # number of nodes per element having nodal forces
            nodfor = np.empty(10000, np.int32)

            # number of nodes per element having nodal stresses
            nodstr = np.empty(10000, np.int32)
            etype_ID = np.empty(maxety, np.int32)
            ekey = []
            for i in range(maxety):
                f.seek((ptrETYP + e_type_table[i] + 2) * 4)
                einfo = np.fromfile(f, self.resultheader['endian'] + 'i', 2)
                etype_ref = einfo[0]
                etype_ID[i] = einfo[1]
                ekey.append(einfo)

                f.seek((ptrETYP + e_type_table[i] + 2 + 60) * 4)
                nodelm[etype_ref] = np.fromfile(
                    f, self.resultheader['endian'] + 'i', 1)

                f.seek((ptrETYP + e_type_table[i] + 2 + 62) * 4)
                nodfor[etype_ref] = np.fromfile(
                    f, self.resultheader['endian'] + 'i', 1)

                f.seek((ptrETYP + e_type_table[i] + 2 + 93) * 4)
                nodstr[etype_ref] = np.fromfile(
                    f, self.resultheader['endian'] + 'i', 1)

            # store element table data
            self.element_table = {'nodelm': nodelm,
                                  'nodfor': nodfor,
                                  'nodstr': nodstr}

            # get the element description table
            f.seek((ptrEID + 2) * 4)
            e_disp_table = np.empty(nelm, np.int32)
            e_disp_table[:] = np.fromfile(
                f, self.resultheader['endian'] + 'i8', nelm)

            # get pointer to start of element table and adjust element pointers
            ptr = ptrEID + e_disp_table[0]
            e_disp_table -= e_disp_table[0]

        # The following is stored for each element
        # mat     - material reference number
        # type    - element type number
        # real    - real constant reference number
        # secnum  - section number
        # esys    - element coordinate system
        # death   - death flat (1 live, 0 dead)
        # solidm  - solid model reference
        # shape   - coded shape key
        # elnum   - element number
        # baseeid - base element number
        # NODES   - node numbers defining the element

        # allocate memory for this (a maximum of 21 points per element)
        etype = np.empty(nelm, np.int32)

        elem = np.empty((nelm, 20), np.int32)
        elem[:] = -1

        # load elements
        _rstHelper.LoadElements(self.filename, ptr, nelm, e_disp_table, elem,
                                etype)
        enum = self.resultheader['eeqv']

        # store geometry dictionary
        self.geometry = {'nnum': nnum,
                         'nodes': nloc,
                         'etype': etype,
                         'elem': elem,
                         'enum': enum,
                         'ekey': np.asarray(ekey, ctypes.c_int64),
                         'e_rcon': np.ones_like(enum)}

        # store the reference array
        valid_types = ['45', '95', '185', '186', '92', '187', '154', '181']
        result = _parser.Parse(self.geometry, False, valid_types)
        cells, offset, cell_type, self.numref, _, _, _ = result

        # catch -1
        cells[cells == -1] = 0

        # Create vtk object if vtk installed
        if vtkloaded:

            element_type = np.zeros_like(etype)
            for key, typekey in ekey:
                # if str(typekey) in valid_types:
                element_type[etype == key] = typekey

            # validmask = element_type != 0
            # element_type = element_type[validmask]
            nodes = nloc[:, :3]
            self.quadgrid = vtkInterface.UnstructuredGrid(offset, cells,
                                                          cell_type, nodes)
            self.quadgrid.AddCellScalars(enum, 'ANSYS_elem_num')
            self.quadgrid.AddPointScalars(nnum, 'ANSYSnodenum')
            self.quadgrid.AddCellScalars(element_type, 'Element Type')
            self.grid = self.quadgrid.LinearGridCopy()

        # get edge nodes
        nedge = nodstr[etype].sum()
        self.edge_idx = np.empty(nedge, np.int32)
        _rstHelper.AssembleEdges(
            nelm, etype, elem, self.numref.astype(
                np.int32), self.edge_idx, nodstr)

        # store edge node numbers and indices to the node array
        self.edge_node_num_idx = np.unique(self.edge_idx)

        # catch the disassociated node bug
        try:
            self.edge_node_num = self.geometry['nnum'][self.edge_node_num_idx]
        except:
            logging.warning('unable to generate edge_node_num')

    def ElementSolutionHeader(self, rnum):
        """ Get element solution header information """
        # Get the header information from the header dictionary
        endian = self.resultheader['endian']
        rpointers = self.resultheader['rpointers']
        nelm = self.resultheader['nelm']
        nodstr = self.element_table['nodstr']
        etype = self.geometry['etype']

        # Check if result is available
        if rnum > self.nsets - 1:
            raise Exception(
                'There are only {:d} results in the result file.'.format(
                    self.nsets))

        # Read a result
        with open(self.filename, 'rb') as f:

            f.seek((rpointers[rnum] + 1) * 4)  # item 20
            # solheader = np.fromfile(f, endian + 'i', 200)

            # key to extrapolate integration
            f.seek((rpointers[rnum] + 17) * 4)  # item 16
            rxtrap = np.fromfile(f, endian + 'i', 1)[0]
            # point results to nodes
            # = 0 - move
            # = 1 - extrapolate unless active
            # non-linear
            # = 2 - extrapolate always
            # print(rxtrap)
            if rxtrap == 0:
                warnings.warn('Strains and stresses are moved and not ' +
                              'extrapolated nodal stress calculations will ' +
                              'be incorrect')

            # item 122  64-bit pointer to element solution
            f.seek((rpointers[rnum] + 120) * 4)
            ptrESL = np.fromfile(f, endian + 'i8', 1)[0]

            if not ptrESL:
                f.close()
                raise Exception('No element solution in result set %d' % (rnum + 1))

            # Seek to element result header
            element_rst_ptr = rpointers[rnum] + ptrESL + 2
            f.seek(element_rst_ptr * 4)

            # element index table
            ele_ind_table = np.fromfile(f, endian + 'i8', nelm)
            ele_ind_table += element_rst_ptr
            # Each element header contains 25 records for the individual
            # results.  Get the location of the nodal stress
            table_index = e_table.index('ptrENS')

        return table_index, ele_ind_table, nodstr, etype

    def NodalStress(self, rnum):
        """
        Equivalent ANSYS command: PRNSOL, S

        Retrives the component stresses for each node in the solution.

        The order of the results corresponds to the sorted node numbering.

        This algorithm, like ANSYS, computes the nodal stress by averaging the
        stress for each element at each node.  Due to the discontinunities
        across elements, stresses will vary based on the element they are
        evaluated from.

        Parameters
        ----------
        rnum : interger
            Result set to load using zero based indexing.

        Returns
        -------
        nodenum : numpy.ndarray
            Node numbers of the result.

        stress : numpy.ndarray
            Stresses at Sx Sy Sz Sxy Syz Sxz averaged at each corner node.
            For the corresponding node numbers, see "result.edge_node_num"
            where result is the result object.

        """
        element_stress, elemnum, enode = self.ElementStress(0)

        # nodes for each element
        nnum = np.hstack(enode)
        nodenum = np.unique(nnum)

        # stack the element stresses
        arr = np.vstack(element_stress)

        # determine the number of times each node occurs in the results
        arr_ones = np.ones_like(arr)
        ncount = np.bincount(nnum, weights=arr_ones[:, 0])
        mask = ncount != 0

        # sum and weight the stress at each node
        stress = np.empty((nodenum.size, 6))
        for i in range(6):
            stress[:, i] = np.bincount(nnum, weights=arr[:, i])[mask]

        stress /= ncount[mask].reshape(-1, 1)
        return nodenum, stress

    def ElementStress(self, rnum):
        """
        Equivalent ANSYS command: PRESOL, S

        Retrives the component stresses for each node in the solution.

        This algorithm, like ANSYS, computes the nodal stress by averaging the
        stress for each element at each node.  Due to the discontinuities
        across elements, stresses at nodes will vary based on the element
        they are evaluated from.

        Parameters
        ----------
        rnum : interger
            Result set to load using zero based indexing.

        Returns
        -------
        element_stress : list
            Stresses at each element for each node for Sx Sy Sz Sxy Syz Sxz.

        enum : np.ndarray
            ANSYS element numbers corresponding to each element.

        enode : list
            Node numbers corresponding to each element's stress results.  One
            list entry for each element

        Notes
        -----
        Only elements that output stress will have their stresses reported.
        See the ANSYS element guide.

        """
        result = self.ElementSolutionHeader(rnum)
        table_index, ele_ind_table, nodstr, etype = result

        # certain element types do not output stress
        elemtype = self.grid.GetCellScalars('Element Type')
        validmask = np.in1d(elemtype, validENS)
        validmask[:] = True

        ele_ind_table = ele_ind_table[validmask]
        etype = etype[validmask].astype(c_int64)

        # load in raw results
        nnode = nodstr[etype]
        nelemnode = nnode.sum()
        ver = float(self.resultheader['verstring'])
        if ver >= 14.5:
            if self.resultheader['rstsprs'] != 0:
                nitem = 6
            else:
                nitem = 11
            ele_data_arr = np.empty((nelemnode, nitem), np.float32)
            _rstHelper.ReadElementStress(self.filename, table_index,
                                         ele_ind_table,
                                         nodstr.astype(c_int64),
                                         etype,
                                         ele_data_arr,
                                         self.edge_idx.astype(c_int64),
                                         nitem)
            if nitem != 6:
                ele_data_arr = ele_data_arr[:, :6]

        else:
            ele_data_arr = np.empty((nelemnode, 6), np.float64)
            _rstHelper.ReadElementStressDouble(self.filename, table_index,
                                               ele_ind_table,
                                               nodstr.astype(c_int64),
                                               etype,
                                               ele_data_arr,
                                               self.edge_idx.astype(c_int64))

        splitind = np.cumsum(nnode)
        element_stress = np.split(ele_data_arr, splitind[:-1])

        # reorder list using sorted indices
        enum = self.grid.GetCellScalars('ANSYS_elem_num')[validmask]
        sidx = np.argsort(enum)
        element_stress = [element_stress[i] for i in sidx]

        elem = self.geometry['elem'][validmask]
        enode = []
        for i in sidx:
            enode.append(elem[i, :nnode[i]])

        # Get element numbers
        elemnum = self.geometry['enum'][self.sidx_elem]
        return element_stress, elemnum, enode

    def PrincipalNodalStress(self, rnum):
        """
        Computes the principal component stresses for each node in the
        solution.

        Parameters
        ----------
        rnum : interger
            Result set to load using zero based indexing.

        Returns
        -------
        nodenum : numpy.ndarray
            Node numbers of the result.

        pstress : numpy.ndarray
            Principal stresses, stress intensity, and equivalant stress.
            [sigma1, sigma2, sigma3, sint, seqv]

        Notes
        -----
        ANSYS equivalant of:
        PRNSOL, S, PRIN

        which returns:
        S1, S2, S3 principal stresses, SINT stress intensity, and SEQV
        equivalent stress.

        """
        # get component stress
        nodenum, stress = self.NodalStress(rnum)

        # compute principle stress
        if stress.dtype != np.float32:
            stress = stress.astype(np.float32)
        return nodenum, _rstHelper.ComputePrincipalStress(stress)

    def PlotPrincipalNodalStress(self, rnum, stype):
        """
        Plot the principal stress at each node in the solution.

        Parameters
        ----------
        rnum : interger
            Result set using zero based indexing.

        stype : string
            Stress type to plot.  S1, S2, S3 principal stresses, SINT stress
            intensity, and SEQV equivalent stress.

            Stress type must be a string from the following list:

            ['S1', 'S2', 'S3', 'SINT', 'SEQV']

        Returns
        -------
        cpos : list
            VTK camera position.

        """
        stress = self.PrincipleStressForPlotting(rnum, stype)

        # Generate plot
        stitle = 'Nodal Stress\n{:s}'.format(stype)
        plobj = vtkInterface.PlotClass()
        plobj.AddMesh(self.grid, scalars=stress, stitle=stitle,
                      flipscalars=True, interpolatebeforemap=True)

        text = 'Result %d at %f' % (rnum + 1, self.tvalues[rnum])
        plobj.AddText(text)

        return plobj.Plot(), stress

    def PrincipleStressForPlotting(self, rnum, stype):
        """
        returns stress used to plot

        further documentation forthcoming

        """
        stress_types = ['S1', 'S2', 'S3', 'SINT', 'SEQV']
        if stype not in stress_types:
            raise Exception('Stress type not in \n' + str(stress_types))

        sidx = stress_types.index(stype)

        # don't display elements that can't store stress (!)
        # etype = self.grid.GetCellScalars('Element Type')
        # valid = (np.in1d(etype, validENS)).nonzero()[0]
        # grid = self.grid.ExtractSelectionCells(valid)
        grid = self.grid  # bypassed (for now)

        # Populate with nodal stress at edge nodes
        nodenum = grid.GetPointScalars('ANSYSnodenum')
        stress_nnum, edge_stress = self.PrincipalNodalStress(rnum)
        temp_arr = np.zeros((nodenum.max() + 1, 5))
        temp_arr[stress_nnum] = edge_stress

        # find matching edge nodes
        return temp_arr[nodenum, sidx]

    def PlotNodalStress(self, rnum, stype):
        """
        Plots the stresses at each node in the solution.

        The order of the results corresponds to the sorted node numbering.
        This algorthim, like ANSYS, computes the node stress by averaging the
        stress for each element at each node.  Due to the discontinunities
        across elements, stresses will vary based on the element they are
        evaluated from.

        Parameters
        ----------
        rnum : interger
            Result set using zero based indexing.

        stype : string
            Stress type from the following list: [Sx Sy Sz Sxy Syz Sxz]

        Returns
        -------
        cpos : list
            3 x 3 vtk camera position.
        """

        stress_types = ['sx', 'sy', 'sz', 'sxy', 'syz', 'sxz', 'seqv']
        stype = stype.lower()
        if stype not in stress_types:
            raise Exception('Stress type not in: \n' + str(stress_types))
        sidx = stress_types.index(stype)

        # don't display elements that can't store stress
        # etype = self.grid.GetCellScalars('Element Type')
        # valid = (np.in1d(etype, validENS)).nonzero()[0]
        # grid = self.grid.ExtractSelectionCells(valid)
        grid = self.grid  # bypassed for now

        # Populate with nodal stress at edge nodes
        nodenum = grid.GetPointScalars('ANSYSnodenum')
        stress_nnum, edge_stress = self.NodalStress(rnum)
        temp_arr = np.zeros((nodenum.max() + 1, 6))
        temp_arr[stress_nnum] = edge_stress
        stress = temp_arr[nodenum, sidx]

        # stress[mask] = edge_stress[:, sidx]
        stitle = 'Nodal Stress\n{:s}'.format(stype.capitalize())

        # Generate plot
        plobj = vtkInterface.PlotClass()
        plobj.AddMesh(grid, scalars=stress, stitle=stitle,
                      flipscalars=True, interpolatebeforemap=True)
        text = 'Result %d at %f' % (rnum + 1, self.tvalues[rnum])
        plobj.AddText(text)
        return plobj.Plot()

    def SaveAsVTK(self, filename, binary=True):
        """
        Appends all results to an unstructured grid and writes it to disk.

        The file extension will select the type of writer to use.  '.vtk' will
        use the legacy writer, while '.vtu' will select the VTK XML writer.

        Parameters
        ----------
        filename : str
            Filename of grid to be written.  The file extension will select the
            type of writer to use.  '.vtk' will use the legacy writer, while
            '.vtu' will select the VTK XML writer.

        binary : bool, optional
            Writes as a binary file by default.  Set to False to write ASCII

        Notes
        -----
        Binary files write much faster than ASCII, but binary files written on
        one system may not be readable on other systems.  Binary can only be
        selected for the legacy writer.
        """
        # Copy grid as to not write results to original object
        grid = self.grid.Copy()

        for i in range(self.nsets):
            # Nodal results
            val = self.GetNodalResult(i)
            grid.AddPointScalars(val, 'NodalResult{:03d}'.format(i))

            # Populate with nodal stress at edge nodes
            nodenum = self.grid.GetPointScalars('ANSYSnodenum')
            stress_nnum, edge_stress = self.NodalStress(i)
            temp_arr = np.zeros((nodenum.max() + 1, 6))
            temp_arr[stress_nnum] = edge_stress
            stress = temp_arr[nodenum]

            grid.AddPointScalars(stress, 'NodalStress{:03d}'.format(i))

        grid.Write(filename)


def GetResultInfo(filename):
    """
    Returns pointers used to access results from an ANSYS result file.

    Parameters
    ----------
    filename : string
        Filename of result file.

    Returns
    -------
    resultheader : dictionary
        Result header

    """
    f = open(filename, 'rb')

    # initialize result header dictionary
    resultheader = {}

    # Check if big or small endian
    endian = '<'
    if np.fromfile(f, dtype='<i', count=1) != 100:

        # Check if big enos
        f.seek(0)
        if np.fromfile(f, dtype='>i', count=1) == 100:
            endian = '>'

        # Otherwise, it's probably not a result file
        else:
            raise Exception('Unable to determine endian type.\n\n' +
                            'File is possibly not a result file.')

    resultheader['endian'] = endian

    # Read standard header
    f.seek(0)

    # Get ansys version
    f.seek(11 * 4)
    version = f.read(4)[::-1]

    try:
        resultheader['verstring'] = version
        resultheader['mainver'] = int(version[:2])
        resultheader['subver'] = int(version[-1])
    except BaseException:
        warnings.warn('Unable to parse version')
        resultheader['verstring'] = 'unk'
        resultheader['mainver'] = 15
        resultheader['subver'] = 0

    # Read .RST FILE HEADER
    # 100 is size of standard header, plus extras, 3 is location of pointer in
    # table
    f.seek(105 * 4)
    rheader = np.fromfile(f, endian + 'i', count=55)

    # Number of nodes (item 3)
    resultheader['nnod'] = rheader[2]

    # Number of elements (item 6)
    resultheader['nelm'] = rheader[6]

    # Number of degrees of freedom (item 5)
    resultheader['numdof'] = rheader[4]

    # Number of sets of results
    resultheader['nsets'] = rheader[8]

    # Pointer to results table (item 11)
    ptrDSIl = rheader[10]

    # Pointer to the table of time values for a load step (item 12)
    resultheader['ptrTIMl'] = rheader[11]

    # pointer to load step table (item 13)
    ptrLSP = rheader[12]

    # pointer to element equivalence table (item 14)
    ptrELM = rheader[13]

    # pointer to nodal equivalence table (item 15)
    ptrNODl = rheader[14]

    # pointer to geometry information (item 16)
    resultheader['ptrGEO'] = rheader[15]

    # pointer to cyclic symmetry nodal-diameters for each load step
    resultheader['ptrCYC'] = rheader[16]

    # number of sectors (item 21)
    resultheader['nSector'] = rheader[20]

    # cyclic symmetry coordinate system
    resultheader['csCord'] = rheader[21]

    # bitmask for suppressed items (item 40)
    resultheader['rstsprs'] = rheader[40 - 1]

    # Read nodal equivalence table
    f.seek((ptrNODl + 2) * 4)  # Start of pointer, then empty, then data
    resultheader['neqv'] = np.fromfile(
        f, endian + 'i', count=resultheader['nnod'])

    # Read nodal equivalence table
    f.seek((ptrELM + 2) * 4)  # Start of pointer, then empty, then data
    resultheader['eeqv'] = np.fromfile(
        f, endian + 'i', count=resultheader['nelm'])

    # Read table of pointers to locations of results
    f.seek((ptrDSIl + 2) * 4)  # Start of pointer, then empty, then data
    rpointers = np.fromfile(f, endian + 'i', count=resultheader['nsets'])

    # f.seek((ptrDSIl + 2) * 4)  # Start of pointer, then empty, then data
    # rpointers = np.fromfile(f, endian + 'i', count=resultheader['nsets']*2)

    # construct long from two ints
    nsets = resultheader['nsets']
    f.seek((ptrDSIl + 2) * 4)  # Start of pointer, then empty, then data
    raw0 = f.read(nsets*4)
    raw1 = f.read(nsets*4)
    subraw0 = [raw0[i*4:(i+1)*4] for i in range(nsets)]
    subraw1 = [raw1[i*4:(i+1)*4] for i in range(nsets)]
    longraw = [subraw0[i] + subraw1[i] for i in range(nsets)]
    longraw = b''.join(longraw)
    # rpointers = np.fromstring(longraw, 'l')
    rpointers = np.frombuffer(longraw, 'i8')
    assert np.all(rpointers >= 0), 'Data set index table has negative pointers'
    resultheader['rpointers'] = rpointers

    # load harmonic index of each result
    if resultheader['ptrCYC']:
        f.seek((resultheader['ptrCYC'] + 2) * 4)
        resultheader['hindex'] = np.fromfile(f, endian + 'i',
                                             count=resultheader['nsets'])

    # load step table with columns:
    # [loadstep, substep, and cumulative]
    f.seek((ptrLSP + 2) * 4)  # Start of pointer, then empty, then data
    table = np.fromfile(f, endian + 'i', count=resultheader['nsets'] * 3)
    resultheader['ls_table'] = table.reshape((-1, 3))

    f.close()

    return resultheader


def Unique_Rows(a):
    """ Returns unique rows of a and indices of those rows """
    b = np.ascontiguousarray(a).view(
        np.dtype((np.void, a.dtype.itemsize * a.shape[1])))
    _, idx, ridx = np.unique(b, return_index=True, return_inverse=True)

    return idx, ridx


def delete_row_csc(mat, i):
    """ remove a row from a csc matrix """
#    if not isinstance(mat, scipy.sparse.csr_matrix):
#        raise ValueError("works only for CSR format -- use .tocsr() first")
    n = mat.indptr[i + 1] - mat.indptr[i]
    if n > 0:
        mat.data[mat.indptr[i]:-n] = mat.data[mat.indptr[i + 1]:]
        mat.data = mat.data[:-n]
        mat.indices[mat.indptr[i]:-n] = mat.indices[mat.indptr[i + 1]:]
        mat.indices = mat.indices[:-n]
    mat.indptr[i:-1] = mat.indptr[i + 1:]
    mat.indptr[i:] -= n
    mat.indptr = mat.indptr[:-1]
    mat._shape = (mat._shape[0] - 1, mat._shape[1])
