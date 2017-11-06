import os
import numpy as np
import warnings
import logging
import ctypes

from pyansys import _parsefull
from pyansys import _rstHelper

from pyansys import CDBparser


# attempt to load vtk
try:
    import vtkInterface
    import vtk
    vtkloaded = True

except BaseException:
    warnings.warn('Cannot load vtk\nWill be unable to display results.')
    vtkloaded = False


#==============================================================================
# Pointer information from ansys interface manual
#==============================================================================
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
ptrETB - pointer to ETABLE items(post1 only
ptrECT - pointer to contact data
ptrEXY - pointer to integration point locations
ptrEBA - pointer to back stresses
ptrESV - pointer to state variables
ptrMNL - pointer to material nonlinear record


"""


class FullReader(object):
    """
    Object to store the results of an ANSYS full file

    NOTES:
    Currently only supports symmetric and real stiffness matrices as well as
    non-lumped mass matrices.

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

        #// Check if lumped (item 11)
        if self.header[11]:
            raise Exception(
                "Unable to read a lumped mass matrix.  Terminating.")

        # Check if arrays are unsymmetric (item 14)
        if self.header[14]:
            raise Exception(
                "Unable to read an unsymmetric mass/stiffness matrix.")


# Dead setting
#        sort : bool, optional
#            By default, this setting sorts the rows and columns such that the
#            nodes are in order.  ANSYS stores the mass and stiffness matrices
#            such that the bandwidth of the arrays is minimized.  Therefore, to
#            minimize the bandwidth of the arrays, make this setting False.
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

        Notes
        -----


        """
        # check file still exists
        if not os.path.isfile(self.filename):
            raise Exception('{:s} not found'.format(self.filename))

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
        k_block = _rstHelper.ReadArray(self.filename, ptrSTF, ntermK, neqn,
                                       index_arr)

        m_block = _rstHelper.ReadArray(self.filename, ptrMAS, ntermM, neqn,
                                       index_arr)
        k_diag = k_block[3]
        k_data_diag = k_block[4]

        m_diag = m_block[3]
        m_data_diag = m_block[4]

        self.m_block = m_block
        self.k_block = k_block

        # assemble data
        if utri:
            # stiffness matrix
            krow = np.hstack((k_block[1], k_diag))  # row and diag
            kcol = np.hstack((k_block[0], k_diag))  # col and diag
            kdata = np.hstack((k_block[2], k_data_diag))  # data and diag

            # mass matrix
            mrow = np.hstack((m_block[1], m_diag))  # row and diag
            mcol = np.hstack((m_block[0], m_diag))  # col and diag
            mdata = np.hstack((m_block[2], m_data_diag))  # data and diag

        else:
            # stiffness matrix
            krow = np.hstack(
                (k_block[0], k_block[1], k_diag))  # row, col and diag
            kcol = np.hstack((k_block[1], k_block[0], k_diag))  # col and diag
            kdata = np.hstack(
                (k_block[2], k_block[2], k_data_diag))  # data and diag

            # mass matrix
            mrow = np.hstack(
                (m_block[0], m_block[1], m_diag))  # row, col and diag
            mcol = np.hstack((m_block[1], m_block[0], m_diag))  # col and diag
            mdata = np.hstack(
                (m_block[2], m_block[2], m_data_diag))  # data and diag

        # store data for later reference
        self.krow = krow
        self.kcol = kcol
        self.kdata = kdata
        self.mrow = mrow
        self.mcol = mcol
        self.mdata = mdata

        # number of dimentions
        ndim = nref.size

        # output as a sparse matrix
        if as_sparse:

            k = coo_matrix((ndim,) * 2)
            k.data = kdata  # data has to be set first
            k.row = krow
            k.col = kcol

            # convert to csc matrix (generally faster for sparse solvers)
            k = csc_matrix(k)

            m = coo_matrix((ndim,) * 2)
            m.data = mdata
            m.row = mrow
            m.col = mcol

            # convert to csc matrix (generally faster for sparse solvers)
            m = csc_matrix(m)

        else:
            k = np.zeros((ndim,) * 2)
            k[krow, kcol] = kdata

            m = np.zeros((ndim,) * 2)
            m[mrow, mcol] = mdata

        # store if constrained and number of degrees of freedom per node
        self.const = const < 0
        self.ndof = ndof

        return dof_ref, k, m


class ResultReader(object):
    """
    Object to control the reading of ANSYS results written to fortran file
    """

    def __init__(self, filename, logger=False, load_geometry=True):
        """
        Loads basic result information from result file and initializes result
        object.

        Parameters
        ----------
        filename : string
            Filename of the ANSYS binary result file.

        logger : bool, optional
            Enables logging if True.  Debug feature.

        load_geometry : bool, optional
            Loads geometry using vtk by default

        Returns
        -------
        None

        """

        # set logging level depending on settings
        if logger:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.CRITICAL)

        # store logger pointer
        self.logger = logging.getLogger(__name__)

        # Store filename result header items
        self.filename = filename
        self.resultheader = GetResultInfo(filename)

        # Get the total number of results and log it
        self.nsets = len(self.resultheader['rpointers'])
        string = 'There are {:d} results in this file'.format(self.nsets)
        self.logger.debug(string)

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

    def AddCyclicProperties(self):
        """ Adds cyclic properties to result object """
        # ansys's duplicate sector contains nodes from the second half of the node
        # numbering
        #
        # ansys node numbering for the duplicate sector is
        # nnum.min() + nnum.max()
        # where nnum is the node numbering for the master sector

#        if not vtkloaded:
#            raise Exception('Unable to add ')

        # master sector max node number
        num_master_max = self.nnum[int(self.nnum.size / 2) - 1]

        # identify master and duplicate cyclic sectors
        cells = np.arange(self.enum.size)
        dup_cells = np.where(
            np.any(
                self.geometry['elem'] > num_master_max,
                1))[0]
        mas_cells = np.setdiff1d(cells, dup_cells)
        self.sector = self.uGrid.ExtractSelectionCells(mas_cells)
        dup_sector = self.uGrid.ExtractSelectionCells(dup_cells)

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
        self.rotor = vtkappend.GetOutput()
        vtkInterface.GridAddExtraFunctions(self.rotor)

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


        Notes
        -----
        None

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

                # adjust the "direction" of the x and y vectors as they're being
                # rotated
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
        del plobj

    def ResultsProperties(self):
        """
        Logs results available in the result file and returns a dictionary
        of available results

        Logging must be enabled for the results of the check to be shown in the
        console.

        Parameters
        ----------
        None

        Returns
        -------
        result_check : dictionary
            Dictionary indicating the availability of results.

        Notes
        -----
        None

        """

        # check number of results
        self.logger.debug(
            'There are {:d} results in this file'.format(
                self.nsets))

        if self.resultheader['nSector'] > 1:
            self.logger.debug('Contains results from a cyclic analysis with:')
            self.logger.debug(
                '\t{:d} sectors'.format(
                    self.resultheader['nSector']))

        return {'Number of Results': self.nsets}

    def PlotNodalResult(self, rnum, comp='norm', as_abs=False, label=''):
        """
        Plots a nodal result.

        Parameters
        ----------
        rnum : interger
            Cumulative result number.  Zero based indexing.

        comp : string, optional
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

        Notes
        -----
        None

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

        # Generate plot
#        text = 'Result {:d} at {:f}'.format(rnum + 1, self.tvalues[rnum])

        # setup text
        ls_table = self.resultheader['ls_table']
        freq = self.GetTimeValues()[rnum]
        text = 'Cumulative Index: {:3d}\n'.format(ls_table[rnum, 2])
        text += 'Loadstep:         {:3d}\n'.format(ls_table[rnum, 0])
        text += 'Substep:          {:3d}\n'.format(ls_table[rnum, 1])
#        text += 'Harmonic Index:   {:3d}\n'.format(hindex)
        text += 'Frequency:      {:10.4f} Hz'.format(freq)

        plobj = vtkInterface.PlotClass()
        plobj.AddMesh(self.uGrid, no_copy=True, scalars=d, stitle=stitle,
                      flipscalars=True, interpolatebeforemap=True)
        plobj.AddText(text, fontsize=20)
        cpos = plobj.Plot()  # store camera position
        del plobj

        return cpos

    def GetTimeValues(self):
        """
        Returns table of time values for results.  For a modal analysis, this
        corresponds to the frequencies of each mode.


        Parameters
        ----------
        None


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


        Notes
        -----
        None

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

        f = open(self.filename, 'rb')
        f.seek((self.resultheader['ptrGEO'] + 2) * 4)
        geotable = np.fromfile(f, self.resultheader['endian'] + 'i', 80)
        geotable.tolist()

        ptrLOC = geotable[26]

        #======================================================================
        # Node information
        #======================================================================
        nnod = self.resultheader['nnod']
        nnum = np.empty(nnod, np.int32)
        nloc = np.empty((nnod, 6), np.float)
        _rstHelper.LoadNodes(self.filename, ptrLOC, nnod, nloc, nnum)

        #======================================================================
        # Element Information
        #======================================================================
        nelm = geotable[4]
        ptrEID = geotable[28]
        maxety = geotable[1]

        # pointer to the element type index table
        ptrETYP = geotable[20]
        f.seek((ptrETYP + 2) * 4)
        e_type_table = np.fromfile(
            f, self.resultheader['endian'] + 'i', maxety)

        # store information for each element type
        # make these arrays large so you can reference a value via element type numbering
#        etype_arr = np.empty(10000, np.int32)
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

        f.close()

        # The following is stored for each element
        """
        mat     - material reference number
        type    - element type number
        real    - real constant reference number
        secnum  - section number
        esys    - element coordinate system
        death   - death flat (1 live, 0 dead)
        solidm  - solid model reference
        shape   - coded shape key
        elnum   - element number
        baseeid - base element number
        NODES   - node numbers defining the element
        """

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
                         'ekey': np.asarray(ekey, ctypes.c_long)}

        # store the reference array
        cells, offset, cell_type, self.numref = CDBparser.Parse(
            self.geometry, True)

        # Create vtk object if vtk installed
        if vtkloaded:
            nodes = nloc[:, :3]
            self.uGrid = vtkInterface.MakeuGrid(
                offset, cells, cell_type, nodes)

        # get edge nodes
        nedge = nodstr[etype].sum()
        self.edge_idx = np.empty(nedge, np.int32)
        _rstHelper.AssembleEdges(
            nelm, etype, elem, self.numref.astype(
                np.int32), self.edge_idx, nodstr)

        # store edge node numbers and indices to the node array
        self.edge_node_num_idx = np.unique(self.edge_idx)

        # catch the disassociated node bug
#        try:
#            self.edge_node_num = self.geometry['nnum'][self.edge_node_num_idx]
#        except:
#            logging.warning('unable to generate edge_node_num')

    def NodalStress(self, rnum):
        """
        Retrives the component stresses for each node in the solution.

        The order of the results corresponds to the sorted node numbering.

        This algorthim, like ANSYS, computes the nodal stress by averaging the
        stress for each element at each node.  Due to the discontinunities
        across elements, stresses will vary based on the element they are
        evaluated from.

        Parameters
        ----------
        rnum : interger
            Result set to load using zero based indexing.

        Returns
        -------
        stress : array
            Stresses at Sx Sy Sz Sxy Syz Sxz averaged at each corner node.
            For the corresponding node numbers, see "edge_node_num"

        Notes
        -----
        None

        """

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
        f = open(self.filename, 'rb')

        # Seek to result table and to get pointer to DOF results of result
        # table
        f.seek((rpointers[rnum] + 13) * 4)  # item 12

        # 32-bit pointer to element solution
        ptrESL = np.fromfile(f, endian + 'i', 1)[0]

        if not ptrESL:
            f.close()
            raise Exception(
                'No element solution in result set {:d}'.format(
                    rnum + 1))

        # Seek to element result header
        element_rst_ptr = rpointers[rnum] + ptrESL + 2
        f.seek(element_rst_ptr * 4)

        # element index table
        ele_ind_table = np.fromfile(f, endian + 'i8', nelm).astype(np.int32)
        ele_ind_table += element_rst_ptr

        # Each element header contains 25 records for the individual results
        # get the location of the nodal stress
        table_index = e_table.index('ptrENS')

        # check number of records to read (differs with each version)
        f.seek((ele_ind_table[0] + table_index) * 4)
        ptrENS = np.fromfile(f, endian + 'i', 1)[0]

        nnode_elem = nodstr[etype[0]]
        f.seek((ele_ind_table[0] + ptrENS - 2) * 4)
        nitem = np.fromfile(f, endian + 'i', 1)[0] / nnode_elem
        f.close()

        # number of nodes
        nnod = self.resultheader['nnod']

        # different behavior depending on version of ANSYS
        # v15 seems to use floating point while < v14.5 uses double and stores
        # principle values
        if nitem == 6:  # single precision >= v14.5
            ele_data_arr = np.zeros((nnod, 6), np.float32)
            _rstHelper.LoadStress(self.filename, table_index, ele_ind_table,
                                  nodstr, etype, nitem, ele_data_arr,
                                  self.edge_idx)
        elif nitem == 22:  # double precision < v14.5
            nitem = 11
            ele_data_arr = np.zeros((nnod, 6), np.float64)
            _rstHelper.LoadStressDouble(self.filename, table_index,
                                        ele_ind_table, nodstr, etype, nitem,
                                        ele_data_arr, self.edge_idx)

        elif nitem == 11:  # single precision < v14.5
            ele_data_arr = np.zeros((nnod, 6), np.float32)
            _rstHelper.LoadStress(self.filename, table_index, ele_ind_table,
                                  nodstr, etype, nitem, ele_data_arr,
                                  self.edge_idx)

        else:
            raise Exception('Invalid nitem.  Unable to load nodal stresses')

        # Average based on the edges of elements
        enode = self.edge_node_num_idx
        ntimes = np.bincount(self.edge_idx)[enode]
        s_node = ele_data_arr[enode]
        s_node /= ntimes.reshape((-1, 1))

        return s_node

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
        None

        """

        stress_types = ['Sx', 'Sy', 'Sz', 'Sxy', 'Syz', 'Sxz', 'Seqv']
        if stype not in stress_types:
            raise Exception('Stress type not in \n' +
                            "['Sx', 'Sy', 'Sz', 'Sxy', 'Syz', 'Sxz']")

        sidx = ['Sx', 'Sy', 'Sz', 'Sxy', 'Syz', 'Sxz'].index(stype)

        # create a zero array for all nodes
        stress = np.zeros(self.resultheader['nnod'])

        # Populate with nodal stress at edge nodes
        stress[self.edge_node_num_idx] = self.NodalStress(rnum)[:, sidx]
        stitle = 'Nodal Stress\n{:s}'.format(stype)

        # Generate plot
        plobj = vtkInterface.PlotClass()
        plobj.AddMesh(self.uGrid, scalars=stress, stitle=stitle, no_copy=True,
                      flipscalars=True, interpolatebeforemap=True)

        text = 'Result {:d} at {:f}'.format(rnum + 1, self.tvalues[rnum])
        plobj.AddText(text)

        cpos = plobj.Plot()  # store camera position
        del plobj

        return cpos

    def SaveAsVTK(self, filename, binary=True):
        """
        Writes all appends all results to an unstructured grid and writes it to
        disk.

        The file extension will select the type of writer to use.  *.vtk will
        use the legacy writer, while *.vtu will select the VTK XML writer.


        Parameters
        ----------
        filename : str
            Filename of grid to be written.  The file extension will select the
            type of writer to use.  *.vtk will use the legacy writer, while
            *.vtu will select the VTK XML writer.
        binary : bool, optional
            Writes as a binary file by default.  Set to False to write ASCII


        Notes
        -----
        Binary files write much faster than ASCII, but binary files written on
        one system may not be readable on other systems.  Binary can only be
        selected for the legacy writer.


        """

        # Copy grid as to not write results to original object
        grid = self.uGrid.Copy()

        for i in range(self.nsets):
            # Nodal Results
            val = self.GetNodalResult(i)
            grid.AddPointScalars(val, 'NodalResult{:03d}'.format(i))

            # Nodal Stress values are only valid
            stress = self.NodalStress(i)
            val = np.zeros((grid.GetNumberOfPoints(), stress.shape[1]))
            val[self.edge_node_num_idx] = stress
            grid.AddPointScalars(val, 'NodalStress{:03d}'.format(i))

        # Write to file and clean up
        grid.WriteGrid(filename)
        del grid


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

    #======================
    # Read .RST FILE HEADER
    #======================
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


# =============================================================================
# load stress debug using numpy
# =============================================================================
#        #%% numpy debug
#        f = open(self.filename)
#        nstresses = self.edge_idx.size
#        stresses = np.empty((nstresses, 6), np.float32)
#        c = 0
#        for i in range(len(ele_ind_table)):
#            # Element nodal stresses, ptrENS, is the third item in the table
#            f.seek((ele_ind_table[i] + table_index)*4)
#            ptrENS = np.fromfile(f, endian + 'i', 1)[0]
#
#            # read the stresses evaluated at the intergration points or nodes
#            nnode_elem = nodstr[etype[i]]
#
#            f.seek((ele_ind_table[i] + ptrENS)*4)
#            stress = np.fromfile(f, endian + 'f', nnode_elem*nitem).reshape((-1, nitem))#[:, sidx]
#
#            # store stresses
#            stresses[c:c + nnode_elem] = stress[:, :6]
#            c += nnode_elem
#
#        # close file
#        f.close()
#
#        # Average the stresses for each element at each node
#        enode = self.edge_node_num_idx
#        s_node = np.empty((enode.size, 6), np.float32)
#        for i in range(6):
#            s_node[:, i] = np.bincount(self.edge_idx, weights=stresses[:, i])[enode]
#        ntimes = np.bincount(self.edge_idx)[enode]
#        s_node /= ntimes.reshape((-1, 1))
