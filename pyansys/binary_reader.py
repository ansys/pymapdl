"""
Used v150/ansys/customize/user/ResRd.F to help build this interface

"""
import vtk
import struct
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
from pyansys.elements import valid_types
from vtkInterface.common import AxisRotation

# Create logger
log = logging.getLogger(__name__)
log.setLevel('DEBUG')

np.seterr(divide='ignore', invalid='ignore')


def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z


# Pointer information from ansys interface manual
# =============================================================================
# Individual element index table
ELEMENT_INDEX_TABLE_KEYS = ['ptrEMS', 'ptrENF', 'ptrENS', 'ptrENG', 'ptrEGR',
                            'ptrEEL', 'ptrEPL', 'ptrECR', 'ptrETH', 'ptrEUL',
                            'ptrEFX', 'ptrELF', 'ptrEMN', 'ptrECD', 'ptrENL',
                            'ptrEHC', 'ptrEPT', 'ptrESF', 'ptrEDI', 'ptrETB',
                            'ptrECT', 'ptrEXY', 'ptrEBA', 'ptrESV', 'ptrMNL']

ELEMENT_INDEX_TABLE_INFO = {
    'EMS': 'misc. data',
    'ENF': 'nodal forces',
    'ENS': 'nodal stresses',
    'ENG': 'volume and energies',
    'EGR': 'nodal gradients',
    'EEL': 'elastic strains',
    'EPL': 'plastic strains',
    'ECR': 'creep strains',
    'ETH': 'thermal strains',
    'EUL': 'euler angles',
    'EFX': 'nodal fluxes',
    'ELF': 'local forces',
    'EMN': 'misc. non-sum values',
    'ECD': 'element current densities',
    'ENL': 'nodal nonlinear data',
    'EHC': 'calculated heat generations',
    'EPT': 'element temperatures',
    'ESF': 'element surface stresses',
    'EDI': 'diffusion strains',
    'ETB': 'ETABLE items',
    'ECT': 'contact data',
    'EXY': 'integration point locations',
    'EBA': 'back stresses',
    'ESV': 'state variables',
    'MNL': 'material nonlinear record'
}


SOLUTION_HEADER_KEYS = ['pv3num', 'nelm', 'nnod', 'mask', 'itime',
                        'iter', 'ncumit', 'nrf', 'cs_LSC', 'nmast',
                        'ptrNSL', 'ptrESL', 'ptrRF', 'ptrMST', 'ptrBC',
                        'rxtrap', 'mode', 'isym', 'kcmplx', 'numdof',
                        'DOFS', 'DOFS', 'DOFS', 'DOFS', 'DOFS',
                        'DOFS', 'DOFS', 'DOFS', 'DOFS', 'DOFS',
                        'DOFS', 'DOFS', 'DOFS', 'DOFS', 'DOFS',
                        'DOFS', 'DOFS', 'DOFS', 'DOFS', 'DOFS',
                        'DOFS', 'DOFS', 'DOFS', 'DOFS', 'DOFS',
                        'DOFS', 'DOFS', 'DOFS', 'DOFS', 'DOFS',
                        'title', 'title', 'title', 'title', 'title',
                        'title', 'title', 'title', 'title', 'title',
                        'title', 'title', 'title', 'title', 'title',
                        'title', 'title', 'title', 'title', 'title',
                        'stitle', 'stitle', 'stitle', 'stitle', 'stitle',
                        'stitle', 'stitle', 'stitle', 'stitle', 'stitle',
                        'stitle', 'stitle', 'stitle', 'stitle', 'stitle',
                        'stitle', 'stitle', 'stitle', 'stitle', 'stitle',
                        'dbmtim', 'dbmdat', 'dbfncl', 'soltim', 'soldat',
                        'ptrOND', 'ptrOEL', 'nfldof', 'ptrEXA', 'ptrEXT',
                        'ptrEXAl', 'ptrEXAh', 'ptrEXTl', 'ptrEXTh', 'ptrNSLl',
                        'ptrNSLh', 'ptrRFl', 'ptrRFh', 'ptrMSTl', 'ptrMSTh',
                        'ptrBCl', 'ptrBCh', 'ptrTRFl', 'ptrTRFh', 'ptrONDl',
                        'ptrONDh', 'ptrOELl', 'ptrOELh', 'ptrESLl', 'ptrESLh',
                        'ptrOSLl', 'ptrOSLh', '0', '0', '0',
                        'PrinKey', 'numvdof', 'numadof', '0', '0',
                        'ptrVSLl', 'ptrVSLh', 'ptrASLl', 'ptrASLh', '0',
                        '0', '0', '0', 'numRotCmp', '0',
                        'ptrRCMl', 'ptrRCMh', 'nNodStr', '0', 'ptrNDSTRl',
                        'ptrNDSTRh', 'AvailData', 'geomID', 'ptrGEOl', 'ptrGEOh']

GEOMETRY_HEADER_KEYS = ['__unused', 'maxety', 'maxrl', 'nnod', 'nelm',
                        'maxcsy', 'ptrETY', 'ptrREL', 'ptrLOC', 'ptrCSY',
                        'ptrEID', 'maxsec', 'secsiz', 'maxmat', 'matsiz',
                        'ptrMAS', 'csysiz', 'elmsiz', 'etysiz', 'rlsiz',
                        'ptrETYl', 'ptrETYh', 'ptrRELl', 'ptrRELh', 'ptrCSYl',
                        'ptrCSYh', 'ptrLOCl', 'ptrLOCh', 'ptrEIDl', 'ptrEIDh',
                        'ptrMASl', 'ptrMASh', 'ptrSECl', 'ptrSECh', 'ptrMATl',
                        'ptrMATh', 'ptrCNTl', 'ptrCNTh', 'ptrNODl', 'ptrNODh',
                        'ptrELMl', 'ptrELMh', 'Glbnnod', 'ptrGNODl', 'ptrGNODh',
                        'maxn', 'NodesUpd',  'lenbac', 'maxcomp', 'compsiz',
                        'ptrCOMPl', 'ptrCOMPh']

RESULT_HEADER_KEYS = ['fun12', 'maxn', 'nnod', 'resmax', 'numdof',
                      'maxe', 'nelm', 'kan', 'nsets', 'ptrend',
                      'ptrDSIl', 'ptrTIMl', 'ptrLSPl', 'ptrELMl', 'ptrNODl',
                      'ptrGEOl', 'ptrCYCl', 'CMSflg', 'csEls', 'units',
                      'nSector', 'csCord', 'ptrEnd8', 'ptrEnd8', 'fsiflag',
                      'pmeth', 'noffst', 'eoffst', 'nTrans', 'ptrTRANl',
                      'PrecKey', 'csNds', 'cpxrst', 'extopt', 'nlgeom',
                      'AvailData', 'mmass', 'kPerturb', 'XfemKey', 'rstsprs',
                      'ptrDSIh', 'ptrTIMh', 'ptrLSPh', 'ptrCYCh', 'ptrELMh',
                      'ptrNODh', 'ptrGEOh', 'ptrTRANh', 'Glbnnod', 'ptrGNODl',
                      'ptrGNODh', 'qrDmpKy', 'MSUPkey', 'PSDkey', 'cycMSUPkey',
                      'XfemCrkPropTech']


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

    def LoadKM(self, as_sparse=True, sort=False):
        """
        Load and construct mass and stiffness matrices from an ANSYS full file.

        Parameters
        ----------
        as_sparse : bool, optional
            Outputs the mass and stiffness matrices as scipy csc sparse arrays
            when True by default.

        sort : bool, optional
            Rearranges the k and m matrices such that the rows correspond to
            to the sorted rows and columns in dor_ref.  Also sorts dor_ref.

        Returns
        -------
        dof_ref : (n x 2) np.int32 array
            This array contains the node and degree corresponding to each row
            and column in the mass and stiffness matrices.  In a 3 DOF
            analysis the dof intergers will correspond to:
            0 - x
            1 - y
            2 - z
            Sort these values by node number and DOF by enabling the sort
            parameter.

        k : (n x n) np.float or scipy.csc array
            Stiffness array

        m : (n x n) np.float or scipy.csc array
            Mass array

        Notes
        -----
        Constrained entries are removed from the mass and stiffness matrices.

        Constrained dof can be accessed with self.const, which returns the node
        number and DOF constrained in ANSYS.

        """
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
        ntermM = self.header[34]  # number of terms in mass matrix
        ptrDOF = self.header[36]  # pointer to DOF info

        # DOF information
        ptrDOF = self.header[36]  # pointer to DOF info
        with open(self.filename, 'rb') as f:
            ReadTable(f, skip=True)  # standard header
            ReadTable(f, skip=True)  # full header
            ReadTable(f, skip=True)  # number of degrees of freedom
            neqv = ReadTable(f)  # Nodal equivalence table

            f.seek(ptrDOF*4)
            ndof = ReadTable(f)
            const = ReadTable(f)

        # degree of freedom reference and number of degress of freedom per node
        dof_ref = [ndof, neqv]
        self.ndof = ndof

        # Read k and m blocks (see help(ReadArray) for block description)
        if ntermK:
            krow, kcol, kdata = _rstHelper.ReadArray(self.filename,
                                                     ptrSTF,
                                                     ntermK,
                                                     neqn,
                                                     const)
        else:
            warnings.warn('Missing stiffness matrix')
            kdata = None

        if ntermM:
            mrow, mcol, mdata = _rstHelper.ReadArray(self.filename,
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
        dof_ref, index, nref, dref = _rstHelper.SortNodalEqlv(neqn, neqv, ndof)

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


def ResultReader(filename):
    """
    Reads a binary ANSYS result file.

    Parameters
    ----------
    filename : string
        Filename of the ANSYS binary result file.

    """
    if not os.path.isfile(filename):
        raise Exception('%s is not a file or cannot be found' % str(filename))

    # determine if file is a result file
    standard_header = ReadStandardHeader(filename)
    if standard_header['file format'] != 12:
        raise Exception('Binary file is not a result file.')

    # determine if cyclic
    with open(filename, 'rb') as f:
        f.seek(103 * 4)
        result_header = ParseHeader(ReadTable(f), RESULT_HEADER_KEYS)

    if result_header['nSector'] == 1:
        log.debug('Initializing standard result')
        return Result(filename)
    else:
        log.debug('Initializing cyclic result')
        return CyclicResult(filename)


class Result(object):
    """
    Reads a binary ANSYS result file.

    Parameters
    ----------
    filename : string
        Filename of the ANSYS binary result file.

    """
    def __init__(self, filename):
        """
        Loads basic result information from result file and initializes result
        object.

        """
        # Store filename result header items
        self.filename = filename
        self.resultheader = GetResultInfo(filename)

        # Get the total number of results and log it
        self.nsets = len(self.resultheader['rpointers'])
        string = 'There are %d results in this file' % self.nsets
        log.debug(string)

        # Get indices to resort nodal and element results
        self.sidx = np.argsort(self.resultheader['neqv'])
        self.sidx_elem = np.argsort(self.resultheader['eeqv'])

        # Store node numbering in ANSYS
        self.nnum = self.resultheader['neqv'][self.sidx]
        self.enum = self.resultheader['eeqv'][self.sidx_elem]

        # store geometry for later retrival
        self.StoreGeometry()

    def Plot(self, **kwargs):
        """ plots result geometry """
        return self.grid.Plot(**kwargs)

    def PlotNodalSolution(self, rnum, comp='norm', label='',
                          colormap=None, flipscalars=None, cpos=None,
                          screenshot=None, interactive=True, **kwargs):
        """
        Plots a nodal result.

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a list containing
            (step, substep) of the requested result.

        comp : str, optional
            Display component to display.  Options are 'x', 'y', 'z', and
            'norm', corresponding to the x directin, y direction, z direction,
            and the combined direction (x**2 + y**2 + z**2)**0.5

        label : str, optional
            Annotation string to add to scalar bar in plot.

        colormap : str, optional
           Colormap string.  See available matplotlib colormaps.

        flipscalars : bool, optional
            Flip direction of colormap.

        cpos : list, optional
            List of camera position, focal point, and view up.  Plot first, then
            output the camera position and save it.

        screenshot : str, optional
            Setting this to a filename will save a screenshot of the plot before
            closing the figure.

        interactive : bool, optional
            Default True.  Setting this to False makes the plot generate in the
            background.  Useful when generating plots in a batch mode automatically.

        Returns
        -------
        cpos : list
            Camera position from vtk render window.

        """
        # Load result from file
        rnum = self.ParseStepSubstep(rnum)
        nnum, result = self.NodalSolution(rnum)

        # Process result
        if comp == 'x':
            d = result[:, 0]
            stitle = 'X {:s}\n'.format(label)

        elif comp == 'y':
            d = result[:, 1]
            stitle = 'Y {:s}\n'.format(label)

        elif comp == 'z':
            d = result[:, 2]
            stitle = 'Z {:s}\n'.format(label)

        else:
            # Normalize displacement
            d = result[:, :3]
            d = (d*d).sum(1)**0.5

            stitle = 'Normalized\n%s\n' % label

        # sometimes there are less nodes in the result than in the geometry
        npoints = self.grid.GetNumberOfPoints()
        if nnum.size != npoints:
            scalars = np.empty(npoints)
            scalars[:] = np.nan
            nnum_grid = self.grid.GetPointScalars('ANSYSnodenum')
            mask = np.in1d(nnum_grid, nnum)
            scalars[mask] = d
            d = scalars

        return self.PlotPointScalars(d, rnum, stitle, colormap, flipscalars,
                                     screenshot, cpos, interactive=interactive, **kwargs)

    # for legacy
    def GetTimeValues(self):
        return self.resultheader['time_values']

    @property
    def time_values(self):
        return self.resultheader['time_values']

    # for legacy
    @property
    def tvalues(self):
        return self.resultheader['time_values']

    def AnimateNodalSolution(self, rnum, comp='norm', max_disp=0.1,
                             auto_start=True, autoclose=True, nangles=100, show_phase=True,
                             show_result_info=True, interpolatebeforemap=True,
                             cpos=None, **kwargs):
        """
        Animate nodal solution.  Assumes nodal solution is a displacement array from
        a modal solution.

        rnum : int or list
            Cumulative result number with zero based indexing, or a list containing
            (step, substep) of the requested result.

        comp : str, optional
            Display component to display.  Options are 'x', 'y', 'z', and
            'norm', corresponding to the x directin, y direction, z direction,
            and the combined direction (x**2 + y**2 + z**2)**0.5

        max_disp : float, optional
            Maximum displacement in the units of the model.  Default 0.1

        auto_start : bool, optional
            Automatically starts animating.

        autoclose : bool, optional
            Enabled by default.  Exits plotting session when user closes the
            window.

        nangles : int, optional
            Number of "frames" between each full cycle.

        show_phase : bool, optional
            Shows the phase at each frame.

        show_result_info : bool, optional
            Includes result information at the bottom left-hand corner of the plot.

        interpolatebeforemap : bool, optional
            Leaving this at default generally results in a better plot.

        cpos : list, optional
            List of camera position, focal point, and view up.

        kwargs : optional keyword arguments, optional
            See help(vtkInterface.Plot) for additional keyword arguments.

        """
        # normalize nodal solution
        nnum, disp = self.NodalSolution(rnum)
        disp /= (np.abs(disp).max()/max_disp)
        disp = disp.reshape(-1, 3)
        
        if comp == 'x':
            axis = 0
        elif comp == 'y':
            axis = 1
        elif comp == 'z':
            axis = 2
        else:
            axis = None

        if axis is not None:
            scalars = disp[:, axis]
        else:
            scalars = (disp*disp).sum(1)**0.5

        orig_pt = self.grid.points

        if show_result_info:
            result_info = self.TextResultTable(rnum)

        plobj = vtkInterface.PlotClass()
        plobj.AddMesh(self.grid.Copy(), scalars=np.real(scalars),
                      interpolatebeforemap=interpolatebeforemap, **kwargs)
        plobj.UpdateCoordinates(orig_pt, render=False)
        if show_phase:
            text = plobj.AddText('%s\nPhase 0.0 Degrees' % result_info, fontsize=30)
        if cpos:
            plobj.SetCameraPosition(cpos)

        # run until q is pressed
        plobj.Plot(interactive=not auto_start, autoclose=False, interactive_update=True)
        while not plobj.q_pressed:
            for angle in np.linspace(0, np.pi*2, nangles):
                mag_adj = np.sin(angle)
                disp_adj = disp*mag_adj

                if axis is not None:
                    scalars = disp_adj[:, axis]
                else:
                    scalars = (disp_adj*disp_adj).sum(1)**0.5

                plobj.UpdateScalars(scalars, render=False)
                plobj.UpdateCoordinates(orig_pt + disp_adj, render=False)
                if show_phase:
                    plobj.textActor.SetInput('%s\nPhase %.1f Degrees' %
                                             (result_info, (angle*180/np.pi)))
                plobj.Update(30, force_redraw=True)
                if plobj.q_pressed:
                    break

        if autoclose:
            return plobj.Close()
        else:
            return plobj.Plot()

    def NodalSolution(self, rnum, in_nodal_coord_sys=False):
        """
        Returns the DOF solution for each node in the global cartesian
        coordinate system or nodal coordinate system.

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a list containing
            (step, substep) of the requested result.

        sort : bool, optional
            Resorts the results so that the results correspond to the sorted
            node numbering (self.nnum) (default).  If left unsorted, results
            correspond to the nodal equivalence array self.resultheader['neqv']

        in_nodal_coord_sys : bool, optional
            When True, returns results in the nodal coordinate system.  Default False.

        Returns
        -------
        nnum : int np.ndarray
            Node numbers associated with the results.

        result : float np.ndarray
            Result is (nnod x numdof), or number of nodes by degrees of freedom

        """
        # convert to cumulative index
        rnum = self.ParseStepSubstep(rnum)

        # Get info from result header
        endian = self.resultheader['endian']
        numdof = self.resultheader['numdof']
        nnod = self.resultheader['nnod']
        rpointers = self.resultheader['rpointers']

        # Read a result
        with open(self.filename, 'rb') as f:

            # Seek to result table and to get pointer to DOF results of result table
            f.seek((rpointers[rnum] + 12) * 4)  # item 11
            ptrNSLl = np.fromfile(f, endian + 'i', 1)[0]

            # Seek and read DOF results
            f.seek((rpointers[rnum] + ptrNSLl + 2) * 4)
            nitems = nnod * numdof
            result = np.fromfile(f, endian + 'd', nitems)

            f.close()

        # Reshape to number of degrees of freedom
        r = result.reshape((-1, numdof))

        # Reorder based on sorted indexing
        r = r.take(self.sidx, 0)

        if not in_nodal_coord_sys:
            # ansys writes the results in the nodal coordinate system.
            # Convert this to the global coordinate system  (in degrees)
            euler_angles = self.geometry['nodes'][self.insolution, 3:].T
            theta_xy, theta_yz, theta_zx = euler_angles

            if np.any(theta_xy):
                vtkInterface.common.AxisRotation(r, theta_xy, inplace=True, axis='z')

            if np.any(theta_yz):
                vtkInterface.common.AxisRotation(r, theta_yz, inplace=True, axis='x')

            if np.any(theta_zx):
                vtkInterface.common.AxisRotation(r, theta_zx, inplace=True, axis='y')

        # also include nodes in output
        return self.nnum, r

    def StoreGeometry(self):
        """ Stores the geometry from the result file """
        # read in the geometry from the result file
        with open(self.filename, 'rb') as f:

            # read geometry header
            f.seek(self.resultheader['ptrGEO']*4)
            table = ReadTable(f)
            geometry_header = ParseHeader(table, GEOMETRY_HEADER_KEYS)
            self.geometry_header = geometry_header

            # Node information
            nnod = geometry_header['nnod']
            nnum = np.empty(nnod, np.int32)
            nloc = np.empty((nnod, 6), np.float)
            _rstHelper.LoadNodes(self.filename, geometry_header['ptrLOC'],
                                 nnod, nloc, nnum)

            # Element Information
            nelm = geometry_header['nelm']
            maxety = geometry_header['maxety']

            # pointer to the element type index table
            f.seek((geometry_header['ptrETY'] + 2) * 4)
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
                f.seek((geometry_header['ptrETY'] + e_type_table[i] + 2) * 4)
                einfo = np.fromfile(f, self.resultheader['endian'] + 'i', 2)
                etype_ref = einfo[0]
                etype_ID[i] = einfo[1]
                ekey.append(einfo)

                f.seek((geometry_header['ptrETY'] + e_type_table[i] + 2 + 60) * 4)
                nodelm[etype_ref] = np.fromfile(
                    f, self.resultheader['endian'] + 'i', 1)

                f.seek((geometry_header['ptrETY'] + e_type_table[i] + 2 + 62) * 4)
                nodfor[etype_ref] = np.fromfile(
                    f, self.resultheader['endian'] + 'i', 1)

                f.seek((geometry_header['ptrETY'] + e_type_table[i] + 2 + 93) * 4)
                nodstr[etype_ref] = np.fromfile(
                    f, self.resultheader['endian'] + 'i', 1)

            # store element table data
            self.element_table = {'nodelm': nodelm,
                                  'nodfor': nodfor,
                                  'nodstr': nodstr}

            # get the element description table
            f.seek((geometry_header['ptrEID'] + 2) * 4)
            e_disp_table = np.empty(nelm, np.int32)
            e_disp_table[:] = np.fromfile(
                f, self.resultheader['endian'] + 'i8', nelm)

            # get pointer to start of element table and adjust element pointers
            ptr = geometry_header['ptrEID'] + e_disp_table[0]
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

        mtype = np.empty(nelm, np.int32)
        rcon = np.empty(nelm, np.int32)

        # load elements
        _rstHelper.LoadElements(self.filename, ptr, nelm, e_disp_table, elem,
                                etype, mtype, rcon)
        enum = self.resultheader['eeqv']

        element_type = np.zeros_like(etype)
        for key, typekey in ekey:
            element_type[etype == key] = typekey

        # store geometry dictionary
        self.geometry = {'nnum': nnum,
                         'nodes': nloc,
                         'etype': etype,
                         'elem': elem,
                         'enum': enum,
                         'ekey': np.asarray(ekey, ctypes.c_int),
                         'e_rcon': rcon,
                         'mtype': mtype,
                         'Element Type': element_type}

        # store the reference array
        # Allow quadradic and null unallowed
        parsed = _parser.Parse(self.geometry, False, valid_types, True)
        cells = parsed['cells']
        offset = parsed['offset']
        cell_type = parsed['cell_type']
        self.numref = parsed['numref']        

        # catch -1
        cells[cells == -1] = 0

        # identify nodes that are actually in the solution
        self.insolution = np.in1d(self.geometry['nnum'], self.resultheader['neqv'])

        # Create vtk object
        nodes = nloc[:, :3]
        self.quadgrid = vtkInterface.UnstructuredGrid(offset, cells,
                                                      cell_type, nodes)
        self.quadgrid.AddCellScalars(enum, 'ANSYS_elem_num')
        self.quadgrid.AddPointScalars(nnum, 'ANSYSnodenum')
        self.quadgrid.AddCellScalars(element_type, 'Element Type')
        self.grid = self.quadgrid.LinearGridCopy()

    def ElementSolutionHeader(self, rnum):
        """ Get element solution header information """
        # Get the header information from the header dictionary
        # endian = self.resultheader['endian']
        rpointers = self.resultheader['rpointers']
        nelm = self.resultheader['nelm']
        nodstr = self.element_table['nodstr']
        etype = self.geometry['etype']

        # Check if result is available
        # if rnum > self.nsets - 1:
        #     raise Exception(
        #         'There are only {:d} results in the result file.'.format(
        #             self.nsets))

        # Read a result
        with open(self.filename, 'rb') as f:
            f.seek((rpointers[rnum]) * 4)  # item 20
            solution_header = ParseHeader(ReadTable(f), SOLUTION_HEADER_KEYS)

            # key to extrapolate integration
            # = 0 - move
            # = 1 - extrapolate unless active
            # non-linear
            # = 2 - extrapolate always
            if solution_header['rxtrap'] == 0:
                warnings.warn('Strains and stresses are being evaluated at ' +
                              'gauss points and not extrapolated')

            # 64-bit pointer to element solution
            if not solution_header['ptrESL']:
                f.close()
                raise Exception('No element solution in result set %d\n' % (rnum + 1) +
                                'Try running with "MXPAND,,,,YES"')

            # Seek to element result header
            element_rst_ptr = rpointers[rnum] + solution_header['ptrESL']
            f.seek(element_rst_ptr * 4)
            ele_ind_table = ReadTable(f, 'i8', nelm) + element_rst_ptr

            # boundary conditions
            # ptr = rpointers[rnum] + solution_header['ptrBC']
            # f.seek(ptr*4)
            # table = ReadTable(f, 'i')

        return ele_ind_table, nodstr, etype

    def NodalStress(self, rnum):
        """
        Equivalent ANSYS command: PRNSOL, S

        Retrieves the component stresses for each node in the solution.

        The order of the results corresponds to the sorted node numbering.

        This algorithm, like ANSYS, computes the nodal stress by averaging the
        stress for each element at each node.  Due to the discontinunities
        across elements, stresses will vary based on the element they are
        evaluated from.

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a list containing
            (step, substep) of the requested result.

        Returns
        -------
        nodenum : numpy.ndarray
            Node numbers of the result.

        stress : numpy.ndarray
            Stresses at Sx Sy Sz Sxy Syz Sxz averaged at each corner node.
            For the corresponding node numbers, see
            where result is the result object.

        Notes
        -----
        Nodes without a stress value will be NAN.

        """
        # element header
        rnum = self.ParseStepSubstep(rnum)
        ele_ind_table, nodstr, etype = self.ElementSolutionHeader(rnum)

        if self.resultheader['rstsprs'] != 0:
            nitem = 6
        else:
            nitem = 11

        # certain element types do not output stress
        elemtype = self.geometry['Element Type'].astype(np.int32)
        validmask = np.in1d(elemtype, validENS).astype(np.int32)

        # if cyclic rotor
        if ele_ind_table.size != self.grid.GetNumberOfCells():
            if not hasattr(self, 'nsector'):
                raise Exception('Element table size does not match number of cells')
            ind = self.grid.GetCellScalars('vtkOriginalCellIds')
            ele_ind_table = ele_ind_table[ind]

        data, ncount = _rstHelper.ReadNodalValues(self.filename,
                                                  self.grid.celltypes,
                                                  ele_ind_table + 2,
                                                  self.grid.offset,
                                                  self.grid.cells,
                                                  nitem,
                                                  validmask.astype(np.int32),
                                                  self.grid.GetNumberOfPoints(),
                                                  nodstr,
                                                  etype,
                                                  elemtype)

        if nitem != 6:
            data = data[:, :6]

        nnum = self.grid.GetPointScalars('ANSYSnodenum')
        stress = data/ncount.reshape(-1, 1)

        return nnum, stress

    @property
    def version(self):
        """ returns the vesion of ansys used to save this result file """
        return float(self.resultheader['verstring'])


    def ElementStress(self, rnum, principal=False):
        """
        Equivalent ANSYS command: PRESOL, S

        Retrives the component stresses for each node in the solution.

        This algorithm, like ANSYS, computes the nodal stress by averaging the
        stress for each element at each node.  Due to the discontinuities
        across elements, stresses at nodes will vary based on the element
        they are evaluated from.

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a list containing
            (step, substep) of the requested result.

        principal : bool, optional
            Returns principal stresses instead of component stresses.  Default False.

        Returns
        -------
        element_stress : list
            Stresses at each element for each node for Sx Sy Sz Sxy Syz Sxz.
            or SIGMA1, SIGMA2, SIGMA3, SINT, SEQV when principal is True.

        enum : np.ndarray
            ANSYS element numbers corresponding to each element.

        enode : list
            Node numbers corresponding to each element's stress results.  One
            list entry for each element

        """
        rnum = self.ParseStepSubstep(rnum)
        header = self.ElementSolutionHeader(rnum)
        ele_ind_table, nodstr, etype = header

        # certain element types do not output stress
        elemtype = self.geometry['Element Type'].astype(np.int32)
        validmask = np.in1d(elemtype, validENS).astype(np.int32)

        # shell181 store their stresses in the direction of the element coordinate
        # system.
        # rot_mask = np.zeros(elemtype.size, np.int32)
        # if 181 in self.geometry['ekey'][:, 1]:
        #     rot_mask[elemtype == 181] = True

        etype = etype.astype(c_int64)

        # load in raw results
        nnode = nodstr[etype]
        nelemnode = nnode.sum()

        # bitmask (might use this at some point)
        # bitmask = bin(int(hex(self.resultheader['rstsprs']), base=16)).lstrip('0b')
        # description maybe in resucm.inc

        if self.version >= 14.5:
            if self.resultheader['rstsprs'] != 0:
                nitem = 6
            else:
                nitem = 11
            ele_data_arr = np.empty((nelemnode, nitem), np.float32)
            ele_data_arr[:] = np.nan

            _rstHelper.ReadElementStress(self.filename,
                                         ele_ind_table + 2,
                                         nodstr.astype(c_int64),
                                         etype,
                                         ele_data_arr,
                                         nitem, validmask, elemtype)
            if nitem != 6:
                ele_data_arr = ele_data_arr[:, :6]


# filename, int64_t [::1] ele_ind_table, 
#                       int64_t [::1] nodstr, int64_t [::1] etype,
#                       float [:, ::1] ele_data_arr, int nitem, int32_t [::1] validmask,
#                       int32_t [::1] element_type):
#     """ Read element results from ANSYS directly into a numpy array """
#     cdef int64_t i, j, k, ind, nread

        else:
            raise Exception('Not implemented for ANSYS older than v14.5')

        if principal:
            ele_data_arr, isnan = _rstHelper.ComputePrincipalStress(ele_data_arr)
            ele_data_arr[isnan] = np.nan

        splitind = np.cumsum(nnode)
        element_stress = np.split(ele_data_arr, splitind[:-1])

        # reorder list using sorted indices
        enum = self.grid.GetCellScalars('ANSYS_elem_num')
        sidx = np.argsort(enum)
        element_stress = [element_stress[i] for i in sidx]

        elem = self.geometry['elem']
        enode = []
        for i in sidx:
            enode.append(elem[i, :nnode[i]])

        # Get element numbers
        elemnum = self.geometry['enum'][self.sidx_elem]
        return element_stress, elemnum, enode

    def ElementSolutionData(self, rnum, datatype, sort=True):
        """
        Retrives element solution data.  Similar to ETABLE.

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a list containing
            (step, substep) of the requested result.

        datatype : str
            Element data type to retreive.

            - EMS: misc. data
            - ENF: nodal forces
            - ENS: nodal stresses
            - ENG: volume and energies
            - EGR: nodal gradients
            - EEL: elastic strains
            - EPL: plastic strains
            - ECR: creep strains
            - ETH: thermal strains
            - EUL: euler angles
            - EFX: nodal fluxes
            - ELF: local forces
            - EMN: misc. non-sum values
            - ECD: element current densities
            - ENL: nodal nonlinear data
            - EHC: calculated heat generations
            - EPT: element temperatures
            - ESF: element surface stresses
            - EDI: diffusion strains
            - ETB: ETABLE items
            - ECT: contact data
            - EXY: integration point locations
            - EBA: back stresses
            - ESV: state variables
            - MNL: material nonlinear record

        Returns
        -------
        element_data : list
            List with one data item for each element.

        Notes
        -----
        See ANSYS element documentation for available items for each element type.

        """

        table_ptr = 'ptr%s' % str(datatype).upper()
        if table_ptr not in ELEMENT_INDEX_TABLE_KEYS:
            err_str = 'Data type %s is invalid\n' % str(datatype)
            err_str += '\nAvailable types:\n'
            for key in ELEMENT_INDEX_TABLE_KEYS:
                key = key[3:]
                err_str += '\t%s: %s\n' % (key, ELEMENT_INDEX_TABLE_INFO[key])

            raise Exception(err_str)

        table_index = ELEMENT_INDEX_TABLE_KEYS.index(table_ptr)

        rnum = self.ParseStepSubstep(rnum)
        ele_ind_table, nodstr, etype = self.ElementSolutionHeader(rnum)

        element_data = []
        f = open(self.filename, 'rb')
        for ind in ele_ind_table:
            # read element table index
            f.seek(ind*4)
            table = ReadTable(f)

            ptr = table[table_index]
            if ptr <= 0:
                element_data.append(None)
            else:
                f.seek((ind + ptr)*4)
                data = ReadTable(f, 'f')  # TODO: Verify datatype
                element_data.append(data)

        enum = self.grid.GetCellScalars('ANSYS_elem_num')
        if sort:
            sidx = np.argsort(enum)
            enum = enum[sidx]
            element_data = [element_data[i] for i in sidx]        

        return enum, element_data

    def PrincipalNodalStress(self, rnum):
        """
        Computes the principal component stresses for each node in the
        solution.

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a list containing
            (step, substep) of the requested result.

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

        pstress, isnan = _rstHelper.ComputePrincipalStress(stress)
        pstress[isnan] = np.nan
        return nodenum, pstress

    def PlotPrincipalNodalStress(self, rnum, stype, colormap=None, flipscalars=None,
                                 cpos=None, screenshot=None, interactive=True,
                                 **kwargs):
        """
        Plot the principal stress at each node in the solution.

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a list containing
            (step, substep) of the requested result.

        stype : string
            Stress type to plot.  S1, S2, S3 principal stresses, SINT stress
            intensity, and SEQV equivalent stress.

            Stress type must be a string from the following list:

            ['S1', 'S2', 'S3', 'SINT', 'SEQV']

        colormap : str, optional
           Colormap string.  See available matplotlib colormaps.  Only applicable for
           when displaying scalars.  Defaults None (rainbow).  Requires matplotlib.

        flipscalars : bool, optional
            Flip direction of colormap.

        cpos : list, optional
            List of camera position, focal point, and view up.  Plot first, then
            output the camera position and save it.

        screenshot : str, optional
            Setting this to a filename will save a screenshot of the plot before
            closing the figure.  Default None.

        interactive : bool, optional
            Default True.  Setting this to False makes the plot generate in the
            background.  Useful when generating plots in a batch mode automatically.

        Returns
        -------
        cpos : list
            VTK camera position.

        stress : np.ndarray
            Array used to plot stress.

        """
        rnum = self.ParseStepSubstep(rnum)
        stress = self.PrincipleStressForPlotting(rnum, stype)

        # Generate plot
        stitle = 'Nodal Stress\n%s\n' % stype
        cpos = self.PlotPointScalars(stress, rnum, stitle, colormap, flipscalars,
                                     screenshot, cpos, interactive, **kwargs)
        return cpos, stress

    def PlotPointScalars(self, scalars, rnum=None, stitle='', colormap=None,
                         flipscalars=None, screenshot=None, cpos=None,
                         interactive=True, grid=None, add_text=True, **kwargs):
        """
        Plot a result

        Parameters
        ----------
        rnum : int
            Cumulative result number.

        scalars : np.ndarray
            Node scalars to plot.

        stitle : str
            Title of the scalar bar.

        colormap : str
            See matplotlib colormaps:
            matplotlib.org/examples/color/colormaps_reference.html

        flipscalars : bool
            Reverses the direction of the colormap.

        screenshot : str
            When a filename, saves screenshot to disk.

        cpos : list
            3x3 list describing the camera position.  Obtain it by getting the output
            of PlotPointScalars first.

        interactive : bool
            Allows user to interact with the plot when True.  Default True.

        grid : vtkInterface PolyData or UnstructuredGrid, optional
            Uses self.grid by default.  When specified, uses this grid instead.

        Returns
        -------
        cpos : list
            Camera position.

        """
        if grid is None:
            grid = self.grid

        # make colormap match default ansys
        if colormap is None and flipscalars is None:
            flipscalars = False

        if 'window_size' in kwargs:
            window_size = kwargs['window_size']
            del kwargs['window_size']
        else:
            window_size = [1024, 768]

        if 'full_screen' in kwargs:
            full_screen = kwargs['full_screen']
            del kwargs['full_screen']
        else:
            full_screen = False

        # Plot off screen when not interactive
        plobj = vtkInterface.PlotClass(off_screen=not(interactive))
        plobj.AddMesh(grid, scalars=scalars, stitle=stitle, colormap=colormap,
                      flipscalars=flipscalars, interpolatebeforemap=True, **kwargs)

        # NAN/missing data are white
        plobj.mapper.GetLookupTable().SetNanColor(1, 1, 1, 1)

        if cpos:
            plobj.SetCameraPosition(cpos)

        # add table
        if add_text and rnum is not None:
            plobj.AddText(self.TextResultTable(rnum), fontsize=20)

        if screenshot:
            cpos = plobj.Plot(autoclose=False, interactive=interactive,
                              window_size=window_size,
                              full_screen=full_screen)
            if screenshot is True:
                img = plobj.TakeScreenShot()
            else:
                plobj.TakeScreenShot(screenshot)
            plobj.Close()
        else:
            cpos = plobj.Plot(interactive=interactive, window_size=window_size,
                              full_screen=full_screen)

        if screenshot is True:
            return cpos, img
        else:
            return cpos

    def TextResultTable(self, rnum):
        """ Returns a text result table for plotting """
        ls_table = self.resultheader['ls_table']
        timevalue = self.GetTimeValues()[rnum]
        text = 'Cumulative Index: {:3d}\n'.format(ls_table[rnum, 2])
        if self.resultheader['nSector'] > 1:
            hindex = self.resultheader['hindex'][rnum]
            text += 'Harmonic Index    {:3d}\n'.format(hindex)
        text += 'Loadstep:         {:3d}\n'.format(ls_table[rnum, 0])
        text += 'Substep:          {:3d}\n'.format(ls_table[rnum, 1])
        text += 'Time Value:     {:10.4f}'.format(timevalue)

        return text

    def PrincipleStressForPlotting(self, rnum, stype):
        """
        returns stress used to plot

        """
        stress_types = ['S1', 'S2', 'S3', 'SINT', 'SEQV']
        if stype.upper() not in stress_types:
            raise Exception('Stress type not in \n' + str(stress_types))

        sidx = stress_types.index(stype)

        _, stress = self.PrincipalNodalStress(rnum)
        return stress[:, sidx]

    def PlotNodalStress(self, rnum, stype, colormap=None, flipscalars=None,
                        cpos=None, screenshot=None, interactive=True, **kwargs):
        """
        Plots the stresses at each node in the solution.

        The order of the results corresponds to the sorted node numbering.
        This algorthim, like ANSYS, computes the node stress by averaging the
        stress for each element at each node.  Due to the discontinunities
        across elements, stresses will vary based on the element they are
        evaluated from.

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a list containing
            (step, substep) of the requested result.

        stype : string
            Stress type from the following list: [Sx Sy Sz Sxy Syz Sxz]

        colormap : str, optional
           Colormap string.  See available matplotlib colormaps.

        flipscalars : bool, optional
            Flip direction of colormap.

        cpos : list, optional
            List of camera position, focal point, and view up.  Plot first, then
            output the camera position and save it.

        screenshot : str, optional
            Setting this to a filename will save a screenshot of the plot before
            closing the figure.

        interactive : bool, optional
            Default True.  Setting this to False makes the plot generate in the
            background.  Useful when generating plots in a batch mode automatically.

        Returns
        -------
        cpos : list
            3 x 3 vtk camera position.
        """
        rnum = self.ParseStepSubstep(rnum)
        stress_types = ['sx', 'sy', 'sz', 'sxy', 'syz', 'sxz', 'seqv']
        stype = stype.lower()
        if stype not in stress_types:
            raise Exception('Stress type not in: \n' + str(stress_types))

        sidx = stress_types.index(stype)

        # Populate with nodal stress at edge nodes
        nnum, stress = self.NodalStress(rnum)
        stress = stress[:, sidx]

        stitle = 'Nodal Stress\n{:s}'.format(stype.capitalize())
        cpos = self.PlotPointScalars(stress, rnum, stitle, colormap, flipscalars,
                                     screenshot, cpos, interactive, **kwargs)

        return cpos

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
            _, val = self.NodalSolution(i)
            grid.AddPointScalars(val, 'NodalSolution{:03d}'.format(i))

            # Populate with nodal stress at edge nodes
            nodenum = self.grid.GetPointScalars('ANSYSnodenum')
            _, stress = self.NodalStress(i)
            grid.AddPointScalars(stress, 'NodalStress{:03d}'.format(i))

        grid.Write(filename)

    def GetNodalResult(self, i, sort=None):
        warnings.warn('GetNodalResult is depreciated.  Use NodalSolution instead')
        return self.NodalSolution(i)

    def WriteTables(self, filename):
        """ Write binary tables to ASCII.  Assumes int32  """
        rawresult = open(self.filename, 'rb')
        with open(filename, 'w') as f:
            while True:
                try:
                    table = ReadTable(rawresult)
                    f.write('*** %d ***\n' % len(table))
                    for item in table:
                        f.write(str(item) + '\n')
                    f.write('\n\n')
                except:
                    break
        rawresult.close()

    def ParseStepSubstep(self, user_input):
        """ Converts (step, substep) to a cumulative index """
        if IsInt(user_input):
            # check if result exists
            if user_input > self.nsets - 1:
                raise Exception('There are only %d results in the result file.' % self.nsets)
            return user_input

        elif isinstance(user_input, list) or isinstance(user_input, tuple):
            if len(user_input) != 2:
                raise Exception('Input must contain (step, loadstep) using  ' +
                                '1 based indexing (e.g. (1, 1)).')
            ls_table = self.resultheader['ls_table']
            step, substep = user_input
            mask = np.logical_and(ls_table[:, 0] == step,
                                  ls_table[:, 1] == substep)

            if not np.any(mask):
                raise Exception('Load step table does not contain ' +
                                'step %d and substep %d' % tuple(user_input))

            index = mask.nonzero()[0]
            assert index.size == 1, 'Multiple cumulative index matches'
            return index[0]
        else:
            raise Exception('Input must be either an int or a list')


class CyclicResult(Result):
    """ adds cyclic functionality to the result reader in pyansys """

    def __init__(self, filename):
        """ Initializes object """
        super(CyclicResult, self).__init__(filename)

        # sanity check
        if self.resultheader['nSector'] == 1:
            raise Exception('Result is not a cyclic model')

        # Add cyclic properties
        self.AddCyclicProperties()

    def AddCyclicProperties(self, tol=1E-5):
        """
        Adds cyclic properties to result object

        Makes the assumption that all the cyclic nodes are within tol
        """
        if self.resultheader['csCord'] != 1:
            warnings.warn('Cyclic coordinate system %d' % self.resultheader['csCord'])
            # raise Exception('Can only read cyclic models with CSYS 1 (for now)')

        # idenfity the sector based on number of elements in master sector
        mask = self.quadgrid.GetCellScalars('ANSYS_elem_num') <= self.resultheader['csEls']
        # node_mask = self.geometry['nnum'] <= self.resultheader['csNds']
        node_mask = self.nnum <= self.resultheader['csNds']

        self.master_cell_mask = mask
        self.grid = self.grid.ExtractSelectionCells(np.nonzero(mask)[0])

        # number of nodes in sector may not match number of nodes in geometry
        self.mas_ind = np.nonzero(node_mask)[0]

        # duplicate sector may not exist
        if not np.any(self.geometry['nnum'] > self.resultheader['csNds']):
            self.dup_ind = None
        else:
            shift = (self.geometry['nnum'] < self.resultheader['csNds']).sum()
            self.dup_ind = self.mas_ind + shift + 1

        # import pdb; pdb.set_trace()

        # create full rotor
        self.nsector = self.resultheader['nSector']

        # Create rotor of sectors
        vtkappend = vtk.vtkAppendFilter()
        rang = 360.0 / self.nsector
        for i in range(self.nsector):

            # Transform mesh
            sector = self.grid.Copy()
            sector.RotateZ(rang * i)
            vtkappend.AddInputData(sector)

        vtkappend.Update()
        self.rotor = vtkInterface.UnstructuredGrid(vtkappend.GetOutput())

    def NodalSolution(self, rnum, phase=0, full_rotor=False, as_complex=False,
                      in_nodal_coord_sys=False):
        """
        Returns the DOF solution for each node in the global cartesian coordinate system.

        Parameters
        ----------
        rnum : interger
            Cumulative result number.  Zero based indexing.

        phase : float, optional
            Phase to rotate sector result.

        full_rotor : bool, optional
            Expands the single sector solution for the full rotor.  Sectors are rotated
            counter-clockwise about the axis of rotation.  Default False.

        as_complex : bool, optional
            Returns result as a complex number, otherwise as the real part rotated by
            phase.  Default False.

        in_nodal_coord_sys : bool, optional
            When True, returns results in the nodal coordinate system.  Default False.

        Returns
        -------
        nnum : np.ndarray
            Node numbers of master sector.

        result : np.ndarray
            Result is (nnod x numdof), nnod is the number of nodes in a sector
            and numdof is the number of degrees of freedom.  When full_rotor is True
            the array will be (nSector x nnod x numdof).

        Notes
        -----
        Somewhere between v15.0 and v18.2 ANSYS stopped writing the duplicate 
        sector to the result file and instead results in pairs (i.e. harmonic
        index 1, -1).  This decreases their result file size since harmonic
        pairs contain the same information as the duplicate sector.
        """
        # get the nodal result
        nnum, result = super(CyclicResult, self).NodalSolution(rnum,
                                                               in_nodal_coord_sys=in_nodal_coord_sys)
        result_mas = result[self.mas_ind]
        nnum = nnum[self.mas_ind]  # only concerned with the master sector

        # combine or expand result if not modal
        if self.resultheader['kan'] == 2:  # modal analysis
            # combine modal solution results
            hindex_table = self.resultheader['hindex']
            hindex = hindex_table[rnum]

            # if repeated mode
            last_repeated = False
            if self.resultheader['nSector'] % 2:
                last_repeated = hindex == int(self.resultheader['nSector']/2)

            # use duplicate sector if it exists
            if self.dup_ind is not None:
                result_dup = result[self.dup_ind]
                # import pdb; pdb.set_trace()

            # otherwise, use the harmonic pair
            elif hindex != 0 or last_repeated:
                hmask = np.abs(hindex_table) == abs(hindex)
                hmatch = np.nonzero(hmask)[0]

                even = not (hmatch.size % 2)
                assert even, 'Harmonic result missing matching pair'
                match_loc = np.where(hmatch == rnum)[0][0]
                
                if match_loc % 2:
                    rnum_dup = rnum - 1
                else:
                    rnum_dup = rnum + 1

                # get repeated result and combine
                _, result_dup = super(CyclicResult, self).NodalSolution(rnum_dup)

            else:
                result_dup = np.zeros_like(result)

            expanded_result = self.ExpandCyclicModal(result_mas, result_dup, hindex, phase, as_complex, full_rotor)

        if self.resultheader['kan'] == 0:  # static analysis
            expanded_result = ExpandCyclicResults(result, self.mas_ind,
                                                  self.dup_ind,
                                                  self.nsector, phase,
                                                  as_complex, full_rotor)

        return nnum, expanded_result

    def ExpandCyclicModal(self, result, result_r, hindex, phase, as_complex,
                          full_rotor):
        """ Combines repeated results from ANSYS """
        if as_complex or full_rotor:
            result_combined = result + result_r*1j
            if phase:
                result_combined *= 1*np.cos(phase) - 1j*np.sin(phase)
        else:  # convert to real
            result_combined = result*np.cos(phase) - result_r*np.sin(phase)

        # just return single sector
        if not full_rotor:
            return result_combined

        # Generate full rotor solution
        result_expanded = []
        angles = np.linspace(0, 2*np.pi, self.nsector + 1)[:-1] + phase
        for angle in angles:
            # need to rotate solution and rotate direction
            result_expanded.append(AxisRotation(result_combined, angle, deg=False,
                                                axis='z'))

        result_expanded = np.asarray(result_expanded)

        # scale
        # if hindex == 0 or hindex == self.nsector/2:
        #     result_expanded /= self.nsector**0.5
        # else:
        #     result_expanded /= (self.nsector/2)**0.5

        # adjust phase of the full result based on the harmonic index
        f_arr = np.zeros(self.nsector)
        f_arr[hindex] = 1
        jang = np.fft.ifft(f_arr)[:self.nsector]*self.nsector
        cjang = jang * (np.cos(phase) - np.sin(phase) * 1j)

        result_expanded *= cjang.reshape(-1, 1, 1)
        if as_complex:
            return result_expanded
        else:
            return np.real(result_expanded)

    def ExpandCyclicModalStress(self, result, result_r, hindex, phase, as_complex,
                                full_rotor, scale=True):
        """ Combines repeated results from ANSYS """
        if self.dup_ind is not None:
            result = result[self.mas_ind]
            result_r = result_r[self.mas_ind]

        if as_complex or full_rotor:
            result_combined = result + result_r*1j
            if phase:
                result_combined *= 1*np.cos(phase) - 1j*np.sin(phase)
        else:  # convert to real
            result_combined = result*np.cos(phase) - result_r*np.sin(phase)

        # just return single sector
        if not full_rotor:
            return result_combined

        # Generate full rotor solution
        result_expanded = np.empty((self.nsector, result.shape[0], result.shape[1]),
                                   np.complex128)
        # result_expanded = np.asarray(result_expanded)
        result_expanded[:] = result_combined

        # scale
        # if scale:
        #     if hindex == 0 or hindex == self.nsector/2:
        #         result_expanded /= self.nsector**0.5
        #     else:
        #         result_expanded /= (self.nsector/2)**0.5

        f_arr = np.zeros(self.nsector)
        f_arr[hindex] = 1
        jang = np.fft.ifft(f_arr)[:self.nsector]*self.nsector
        cjang = jang * (np.cos(phase) - np.sin(phase) * 1j)
        result_expanded = np.real(result_expanded*cjang.reshape(-1, 1, 1))

        # rotate cyclic result inplace
        angles = np.linspace(0, 2*np.pi, self.nsector + 1)[:-1] + phase
        for i, angle in enumerate(angles):
            isnan = _rstHelper.TensorRotateZ(result_expanded[i], angle)
            result_expanded[i, isnan] = np.nan

        return result_expanded

    def HarmonicIndexToCumulative(self, hindex, mode):
        """
        Converts a harmonic index and a 0 index mode number to a cumulative result
        index.

        Harmonic indices are stored as positive and negative pairs for modes other
        than 0 and N/nsectors.

        Parameters
        ----------
        hindex : int
            Harmonic index.  Must be less than or equal to nsectors/2.  May be
            positive or negative

        mode : int
            Mode number.  0 based indexing.  Access mode pairs by with a negative/positive
            harmonic index.

        Returns
        -------
        rnum : int
            Cumulative index number.  Zero based indexing.

        """
        hindex_table = self.resultheader['hindex']
        if not np.any(abs(hindex) == np.abs(hindex_table)):
            raise Exception('Invalid harmonic index.\n' +
                            'Available indices: %s' % np.unique(hindex_table))

        mask = np.logical_and(hindex == hindex_table,
                              mode == self.mode_table)

        if not mask.any():
            mode_mask = abs(hindex) == np.abs(hindex_table)
            avail_modes = np.unique(self.mode_table[mode_mask])
            raise Exception('Invalid mode for harmonic index %d\n' % hindex +
                            'Available modes: %s' % avail_modes)

        index = mask.nonzero()[0]
        assert index.size == 1, 'Multiple cumulative index matches'
        return index[0]

    @property
    def mode_table(self):
        """ unique modes for cyclic results """
        hindex_table = self.resultheader['hindex']
        diff = np.diff(np.abs(hindex_table))
        freqs = self.time_values
        mode_table = [0]
        c = 0
        for i in range(1, freqs.size):
            if diff[i - 1]:
                c = 0
                mode_table.append(c)
            elif np.isclose(freqs[i], freqs[i - 1]):
                mode_table.append(c)
            else:
                c += 1
                mode_table.append(c)
        return np.asarray(mode_table)

    def NodalStress(self, rnum, phase=0, as_complex=False, full_rotor=False):
        nnum, stress = super(CyclicResult, self).NodalStress(rnum)
        nnum = nnum[self.mas_ind]

        if self.resultheader['kan'] == 2:  # modal analysis
            # combine modal solution results
            hindex_table = self.resultheader['hindex']
            hindex = hindex_table[rnum]

            # if repeated mode
            if hindex != 0 and -hindex in hindex_table:
                if hindex < 0:
                    rnum_r = rnum - 1
                else:
                    rnum_r = rnum + 1

                # get repeated result and combine
                _, stress_r = super(CyclicResult, self).NodalStress(rnum_r)

            else:
                stress_r = np.zeros_like(stress)

            expanded_result = self.ExpandCyclicModalStress(stress, stress_r, hindex,
                                                           phase, as_complex, full_rotor)

        elif self.resultheader['kan'] == 0:  # static result
            stress_r = np.zeros_like(stress)
            expanded_result = self.ExpandCyclicModalStress(stress, stress_r, 0,
                                                           phase, as_complex,
                                                           full_rotor, scale=False)

            # expanded_result = ExpandCyclicStress(stress, self.mas_ind,
            #                                       self.dup_ind,
            #                                       self.nsector, phase,
            #                                       as_complex, full_rotor)
        else:
            raise Exception('Unsupported analysis type')

        return nnum, expanded_result

    def PrincipalNodalStress(self, rnum, phase=0, as_complex=False,
                             full_rotor=False):
        """
        Returns principal nodal stress for a cumulative result

        """
        if as_complex and full_rotor:
            raise Exception('Cannot be complex and full rotor')
        
        # get component stress
        nnum, stress = self.NodalStress(rnum, phase, as_complex, full_rotor)

        # compute principle stress
        if as_complex:
            stress_r = np.imag(stress).astype(np.float32)
            stress = np.real(stress).astype(np.float32)

            pstress, isnan = _rstHelper.ComputePrincipalStress(stress)
            pstress[isnan] = np.nan
            pstress_r, isnan = _rstHelper.ComputePrincipalStress(stress_r)
            pstress_r[isnan] = np.nan

            return nnum, pstress + 1j*pstress_r

        elif full_rotor:
            if stress.dtype != np.float32:
                stress = stress.astype(np.float32)

            # compute principle stress
            pstress = np.empty((self.nsector, stress.shape[1], 5), np.float32)
            for i in range(stress.shape[0]):
                pstress[i], isnan = _rstHelper.ComputePrincipalStress(stress[i])
                pstress[i, isnan] = np.nan
            return nnum, pstress

        else:
            if stress.dtype != np.float32:
                stress = stress.astype(np.float32)

            pstress, isnan = _rstHelper.ComputePrincipalStress(stress)
            pstress[isnan] = np.nan
            return nnum, pstress

    def PlotNodalSolution(self, rnum, comp='norm', label='',
                          colormap=None, flipscalars=None, cpos=None,
                          screenshot=None, interactive=True, full_rotor=True,
                          phase=0, **kwargs):
        """
        Plots a nodal result.

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a list containing
            (step, substep) of the requested result.

        comp : str, optional
            Display component to display.  Options are 'x', 'y', 'z', and
            'norm', corresponding to the x directin, y direction, z direction,
            and the combined direction (x**2 + y**2 + z**2)**0.5

        label : str, optional
            Annotation string to add to scalar bar in plot.

        colormap : str, optional
           Colormap string.  See available matplotlib colormaps.

        flipscalars : bool, optional
            Flip direction of colormap.

        cpos : list, optional
            List of camera position, focal point, and view up.  Plot first, then
            output the camera position and save it.

        screenshot : str, optional
            Setting this to a filename will save a screenshot of the plot before
            closing the figure.

        interactive : bool, optional
            Default True.  Setting this to False makes the plot generate in the
            background.  Useful when generating plots in a batch mode automatically.

        full_rotor : bool, optional
            Expand sector solution to full rotor.

        phase : float, optional
            Phase angle of the modal result in radians.  Only valid when full_rotor
            is True.  Default 0

        Returns
        -------
        cpos : list
            Camera position from vtk render window.

        """
        # Load result from file
        if not full_rotor:
            return super(CyclicResult, self).PlotNodalSolution(rnum)

        rnum = self.ParseStepSubstep(rnum)
        nnum, result = self.NodalSolution(rnum, phase, full_rotor, as_complex=False)

        # Process result
        if label == '':
            label = 'Cyclic Rotor\nDisplacement'

        if comp == 'x':
            d = result[:, :, 0]
            stitle = 'X {:s}\n'.format(label)
        elif comp == 'y':
            d = result[:, :, 1]
            stitle = 'Y {:s}\n'.format(label)
        elif comp == 'z':
            d = result[:, :, 2]
            stitle = 'Z {:s}\n'.format(label)
        else:
            # Normalize displacement
            d = (result*result).sum(2)**0.5
            stitle = 'Normalized\n%s\n' % label

        # sometimes there are less nodes in the result than in the geometry
        npoints = self.grid.GetNumberOfPoints()
        if nnum.size != npoints:
            scalars = np.empty_like((self.nsector, npoints))
            scalars[:] = np.nan
            nnum_grid = self.grid.GetPointScalars('ANSYSnodenum')
            mask = np.in1d(nnum_grid, nnum)
            scalars[:, mask] = d
            d = scalars

        return self.PlotPointScalars(d, rnum, stitle, colormap, flipscalars,
                                     screenshot, cpos, interactive, self.rotor,
                                     **kwargs)

    def PlotNodalStress(self, rnum, stype, label='',
                        colormap=None, flipscalars=None, cpos=None,
                        screenshot=None, interactive=True, full_rotor=True,
                        phase=0, **kwargs):
        """
        Plots a nodal result.

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a list containing
            (step, substep) of the requested result.

        stype : string
            Stress type from the following list: [Sx Sy Sz Sxy Syz Sxz]

        label : str, optional
            Annotation string to add to scalar bar in plot.

        colormap : str, optional
           Colormap string.  See available matplotlib colormaps.

        flipscalars : bool, optional
            Flip direction of colormap.

        cpos : list, optional
            List of camera position, focal point, and view up.  Plot first, then
            output the camera position and save it.

        screenshot : str, optional
            Setting this to a filename will save a screenshot of the plot before
            closing the figure.

        interactive : bool, optional
            Default True.  Setting this to False makes the plot generate in the
            background.  Useful when generating plots in a batch mode automatically.

        full_rotor : bool, optional
            Expand sector solution to full rotor.

        phase : float, optional
            Phase angle of the modal result in radians.  Only valid when full_rotor
            is True.  Default 0

        Returns
        -------
        cpos : list
            Camera position from vtk render window.

        """
        if not full_rotor:  # Plot sector
            return super(CyclicResult, self).PlotNodalStress(rnum,
                                                             stype,
                                                             label=label,
                                                             colormap=colormap,
                                                             flipscalars=flipscalars,
                                                             cpos=cpos,
                                                             screenshot=screenshot,
                                                             interactive=interactive,
                                                             **kwargs)

        rnum = self.ParseStepSubstep(rnum)
        stress_types = ['sx', 'sy', 'sz', 'sxy', 'syz', 'sxz']
        stype = stype.lower()
        if stype not in stress_types:
            raise Exception('Stress type not in: \n' + str(stress_types))
        sidx = stress_types.index(stype)

        # Populate with nodal stress at edge nodes
        nnum, stress = self.NodalStress(rnum, phase, False, full_rotor=True)
        scalars = stress[:, :, sidx]

        stitle = 'Cyclic Rotor\nNodal Stress\n{:s}\n'.format(stype.capitalize())
        return self.PlotPointScalars(scalars, rnum, stitle, colormap, flipscalars,
                                     screenshot, cpos, interactive, self.rotor,
                                     **kwargs)

    def PlotPrincipalNodalStress(self, rnum, stype, colormap=None, flipscalars=None,
                                 cpos=None, screenshot=None, interactive=True,
                                 full_rotor=True, phase=0,
                                 **kwargs):
        """
        Plot the principal stress at each node in the solution.

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a list containing
            (step, substep) of the requested result.

        stype : string
            Stress type to plot.  S1, S2, S3 principal stresses, SINT stress
            intensity, and SEQV equivalent stress.

            Stress type must be a string from the following list:

            ['S1', 'S2', 'S3', 'SINT', 'SEQV']

        colormap : str, optional
           Colormap string.  See available matplotlib colormaps.  Only applicable for
           when displaying scalars.  Defaults None (rainbow).  Requires matplotlib.

        flipscalars : bool, optional
            Flip direction of colormap.

        cpos : list, optional
            List of camera position, focal point, and view up.  Plot first, then
            output the camera position and save it.

        screenshot : str, optional
            Setting this to a filename will save a screenshot of the plot before
            closing the figure.  Default None.

        interactive : bool, optional
            Default True.  Setting this to False makes the plot generate in the
            background.  Useful when generating plots in a batch mode automatically.

        full_rotor : bool, optional
            Expand sector solution to full rotor.

        phase : float, optional
            Phase angle of the modal result in radians.  Only valid when full_rotor
            is True.  Default 0

        Returns
        -------
        cpos : list
            VTK camera position.

        stress : np.ndarray
            Array used to plot stress.

        """
        stype = stype.upper()
        if not full_rotor:  # Plot sector
            return super(CyclicResult, self).PlotPrincipalNodalStress(rnum, stype)

        # check inputs
        stress_types = ['S1', 'S2', 'S3', 'SINT', 'SEQV']
        if stype not in stress_types:
            raise Exception('Stress type not in \n' + str(stress_types))
        sidx = stress_types.index(stype)
        rnum = self.ParseStepSubstep(rnum)

        # full rotor component stress
        _, pstress = self.PrincipalNodalStress(rnum, phase, full_rotor=True)

        scalars = pstress[:, :, sidx]
        stitle = 'Cyclic Rotor\nPrincipal Nodal Stress\n' +\
                 '%s\n' % stype.capitalize()
        return self.PlotPointScalars(scalars, rnum, stitle, colormap, flipscalars,
                                     screenshot, cpos, interactive, self.rotor,
                                     **kwargs)

    def AnimateNodalSolution(self, rnum, comp='norm', max_disp=0.1, show_phase=True,
                             auto_start=True, autoclose=True, nangles=180,
                             show_result_info=True, interpolatebeforemap=True,
                             cpos=None, **kwargs):
        """
        Animate nodal solution.  Assumes nodal solution is a displacement array from
        a modal solution.

        rnum : int or list
            Cumulative result number with zero based indexing, or a list containing
            (step, substep) of the requested result.

        comp : str, optional
            Display component to display.  Options are 'x', 'y', 'z', and
            'norm', corresponding to the x directin, y direction, z direction,
            and the combined direction (x**2 + y**2 + z**2)**0.5

        max_disp : float, optional
            Maximum displacement in the units of the model.  Default 0.1

        auto_start : bool, optional
            Automatically starts animating.

        autoclose : bool, optional
            Enabled by default.  Exits plotting session when user closes the
            window.

        nangles : int, optional
            Number of "frames" between each full cycle.

        show_phase : bool, optional
            Shows the phase at each frame.

        show_result_info : bool, optional
            Includes result information at the bottom left-hand corner of the plot.

        interpolatebeforemap : bool, optional
            Leaving this at default generally results in a better plot.

        cpos : list, optional
            List of camera position, focal point, and view up.

        ncolors : int, optional
            Number of colors to use when displaying scalars.  Default 256.

        kwargs : optional keyword arguments, optional
            See help(vtkInterface.Plot) for additional keyword arguments.

        """
        # normalize nodal solution
        nnum, complex_disp = self.NodalSolution(rnum, as_complex=True,
                                                full_rotor=True)
        complex_disp /= (np.abs(complex_disp).max()/max_disp)
        complex_disp = complex_disp.reshape(-1, 3)
        
        if comp == 'x':
            axis = 0
        elif comp == 'y':
            axis = 1
        elif comp == 'z':
            axis = 2
        else:
            axis = None

        if axis is not None:
            scalars = complex_disp[:, axis]
        else:
            scalars = (complex_disp*complex_disp).sum(1)**0.5

        orig_pt = self.rotor.points

        if show_result_info:
            result_info = self.TextResultTable(rnum)

        plobj = vtkInterface.PlotClass()
        plobj.AddMesh(self.rotor.Copy(), scalars=np.real(scalars),
                      interpolatebeforemap=interpolatebeforemap, **kwargs)
        plobj.UpdateCoordinates(orig_pt + np.real(complex_disp), render=False)
        if show_phase:
            text = plobj.AddText('%s\nPhase 0.0 Degrees' % result_info, fontsize=30)
        if cpos:
            plobj.SetCameraPosition(cpos)

        # run until q is pressed
        plobj.Plot(interactive=not auto_start, autoclose=False, interactive_update=True)

        while not plobj.q_pressed:
            for angle in np.linspace(0, np.pi*2, nangles):
                padj = 1*np.cos(angle) - 1j*np.sin(angle)
                complex_disp_adj = np.real(complex_disp*padj)

                if axis is not None:
                    scalars = complex_disp_adj[:, axis]
                else:
                    scalars = (complex_disp_adj*complex_disp_adj).sum(1)**0.5

                plobj.UpdateScalars(scalars, render=False)
                plobj.UpdateCoordinates(orig_pt + complex_disp_adj, render=False)

                if show_phase:
                    plobj.textActor.SetInput('%s\nPhase %.1f Degrees' %
                                             (result_info, (angle*180/np.pi)))
                plobj.Update(30, force_redraw=True)
                if plobj.q_pressed:
                    break

        if autoclose:
            return plobj.Close()
        else:
            return plobj.Plot()


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
    standard_header = ReadStandardHeader(filename)
    endian = standard_header['endian']

    with open(filename, 'rb') as f:
        # Read .RST FILE HEADER
        f.seek(103 * 4)
        header = ParseHeader(ReadTable(f), RESULT_HEADER_KEYS)
        resultheader = merge_two_dicts(header, standard_header)

        # Read nodal equivalence table
        f.seek(resultheader['ptrNOD']*4)
        resultheader['neqv'] = ReadTable(f)

        # Read nodal equivalence table
        f.seek(resultheader['ptrELM']*4)
        resultheader['eeqv'] = ReadTable(f)

        # Read table of pointers to locations of results
        nsets = resultheader['nsets']
        f.seek((resultheader['ptrDSI'] + 2) * 4)  # Start of pointer, then empty, then data

        # Data sets index table. This record contains the record pointers
        # for the beginning of each data set. The first resmax records are
        # the first 32 bits of the index, the second resmax records are
        # the second 32 bits f.seek((ptrDSIl + 0) * 4)
        raw0 = f.read(resultheader['resmax']*4)
        raw1 = f.read(resultheader['resmax']*4)
        subraw0 = [raw0[i*4:(i+1)*4] for i in range(nsets)]
        subraw1 = [raw1[i*4:(i+1)*4] for i in range(nsets)]
        longraw = [subraw0[i] + subraw1[i] for i in range(nsets)]
        longraw = b''.join(longraw)
        rpointers = np.frombuffer(longraw, 'i8')

        assert np.all(rpointers >= 0), 'Data set index table has negative pointers'
        resultheader['rpointers'] = rpointers

        # read in time values
        f.seek(resultheader['ptrTIMl']*4)
        table = ReadTable(f, 'd', resultheader['nsets'])
        resultheader['time_values'] = table

        # load harmonic index of each result
        if resultheader['ptrCYC']:
            f.seek((resultheader['ptrCYC'] + 2) * 4)
            hindex = np.fromfile(f, 'i', count=resultheader['nsets'])

            # ansys 15 doesn't track negative harmonic indices
            if not np.any(hindex < -1):
                # check if duplicate frequencies
                tvalues = resultheader['time_values']
                for i in range(tvalues.size - 1):
                    if np.isclose(tvalues[i], tvalues[i + 1]):  # adjust tolarance(?)
                        hindex[i + 1] *= -1

            resultheader['hindex'] = hindex

        # load step table with columns:
        # [loadstep, substep, and cumulative]
        f.seek((resultheader['ptrLSP'] + 2) * 4)  # Start of pointer, then empty, then data
        table = np.fromfile(f, endian + 'i', count=resultheader['nsets'] * 3)
        resultheader['ls_table'] = table.reshape((-1, 3))

    return resultheader


def ReadTable(f, dtype='i', nread=None, skip=False, get_nread=True):
    """ read fortran style table """
    if get_nread:
        n = np.fromfile(f, 'i', 1)
        if not n:
            raise Exception('end of file')

        tablesize = n[0]
        f.seek(4, 1)  # skip padding

    # override
    if nread:
        tablesize = nread

    if skip:
        f.seek((tablesize + 1)*4, 1)
        return
    else:
        if dtype == 'double':
            tablesize //= 2
        table = np.fromfile(f, dtype, tablesize)
    f.seek(4, 1)  # skip padding
    return table


def TwoIntsToLong(intl, inth):
    """ Interpert two ints as one long """
    longint = struct.pack(">I", inth) + struct.pack(">I", intl)
    return struct.unpack('>q', longint)[0]


def Pol2Cart(rho, phi):
    """ Convert cylindrical to cartesian """
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)

    return x, y


def ParseHeader(table, keys):
    """ parses a header from a table """
    header = {}
    for i, key in enumerate(keys):
        header[key] = table[i]

    for key in keys:
        if 'ptr' in key and key[-1] == 'h':
            basekey = key[:-1]
            intl = header[basekey + 'l']
            inth = header[basekey + 'h']
            header[basekey] = TwoIntsToLong(intl, inth)

    return header


def ReadStandardHeader(filename):
    """ Reads standard header """
    # f = open(filename, 'rb')
    with open(filename, 'rb') as f:

        endian = '<'
        if np.fromfile(f, dtype='<i', count=1) != 100:

            # Check if big enos
            f.seek(0)
            if np.fromfile(f, dtype='>i', count=1) == 100:
                endian = '>'

            # Otherwise, it's probably not a result file
            else:
                raise Exception('Unable to determine endian type.  ' +
                                'Possibly not an ANSYS binary file')

        f.seek(0)

        header = {}
        header['endian'] = endian
        header['file number'] = ReadTable(f, nread=1, get_nread=False)[0]
        header['file format'] = ReadTable(f, nread=1, get_nread=False)[0]
        int_time = str(ReadTable(f, nread=1, get_nread=False)[0])
        header['time'] = ':'.join([int_time[0:2], int_time[2:4], int_time[4:]])
        int_date = str(ReadTable(f, nread=1, get_nread=False)[0])
        if int_date == '-1':
            header['date'] = ''
        else:
            header['date'] = '/'.join([int_date[0:4], int_date[4:6], int_date[6:]])

        unit_types = {0: 'User Defined',
                      1: 'SI',
                      2: 'CSG',
                      3: 'U.S. Customary units (feet)',
                      4: 'U.S. Customary units (inches)',
                      5: 'MKS',
                      6: 'MPA',
                      7: 'uMKS'}
        header['units'] = unit_types[ReadTable(f, nread=1, get_nread=False)[0]]

        f.seek(11 * 4)
        version = ReadStringFromBinary(f, 1).strip()

        header['verstring'] = version
        header['mainver'] = int(version[:2])
        header['subver'] = int(version[-1])

        # there's something hidden at 12
        f.seek(4, 1)

        # f.seek(13 * 4)
        header['machine'] = ReadStringFromBinary(f, 3).strip()
        header['jobname'] = ReadStringFromBinary(f, 2).strip()
        header['product'] = ReadStringFromBinary(f, 2).strip()
        header['special'] = ReadStringFromBinary(f, 1).strip()
        header['username'] = ReadStringFromBinary(f, 3).strip()

        # Items 23-25 The machine identifier in integer form (three four-character strings)
        # this contains license information
        header['machine_identifier'] = ReadStringFromBinary(f, 3).strip()

        # Item 26 The system record size
        header['system record size'] = ReadTable(f, nread=1, get_nread=False)[0]

        # Item 27 The maximum file length
        # header['file length'] = ReadTable(f, nread=1, get_nread=False)[0]

        # Item 28 The maximum record number
        # header['the maximum record number'] = ReadTable(f, nread=1, get_nread=False)[0]

        # Items 31-38 The Jobname (eight four-character strings)
        f.seek(32*4)
        header['jobname2'] = ReadStringFromBinary(f, 8).strip()

        # Items 41-60 The main analysis title in integer form (20 four-character strings)
        f.seek(42*4)
        header['title'] = ReadStringFromBinary(f, 20).strip()

        # Items 61-80 The first subtitle in integer form (20 four-character strings)
        header['subtitle'] = ReadStringFromBinary(f, 20).strip()

        # Item 95 The split point of the file (0 means the file will not split)
        f.seek(96*4)
        header['split point'] = ReadTable(f, nread=1, get_nread=False)[0]

        # Items 97-98 LONGINT of the maximum file length (bug here)
        # ints = ReadTable(f, nread=2, get_nread=False)
        # header['file length'] = TwoIntsToLong(ints[0], ints[1])

    return header


def ReadStringFromBinary(f, n):
    """ Read n 4 character binary strings from a file opend in binary mode """
    string = b''
    for i in range(n):
        string += f.read(4)[::-1]

    try:
        return string.decode('utf')
    except:
        return string


def IsInt(value):
    """ Return true if can be parsed as an int """
    try:
        int(value)
        return True
    except:
        return False


def ExpandCyclicResults(result, mas_ind, dup_ind, nsector, phase, as_complex=False,
                        full_rotor=False):
    """
    Expand cyclic results given an array of results and the master/duplicate
    sector indices
    """

    # master and duplicate sector solutions
    u_mas = result[mas_ind]

    # just return single sector
    if not full_rotor:
        return u_mas

    # otherwise rotate results (CYC, 1 only)
    sectors = []
    angles = np.linspace(0, 2*np.pi, nsector + 1)[:-1] + phase
    for angle in angles:
        sectors.append(AxisRotation(u_mas, angle, deg=False, axis='z'))

    return np.asarray(sectors)
