"""
Used v150/ansys/customize/user/ResRd.F to help build this interface

"""
import struct
import os
import warnings
import logging
import ctypes

import vtk
from vtki.common import axis_rotation
import vtki
import numpy as np

import pyansys
from pyansys import _parsefull
from pyansys import _binary_reader
from pyansys import _parser
from pyansys.elements import valid_types

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


# element types with stress outputs (consider not including this)
# validENS = [45, 92, 95, 181, 182, 183, 185, 186, 187]


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

    def load_km(self, as_sparse=True, sort=False):
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
            krow, kcol, kdata = _binary_reader.ReadArray(self.filename,
                                                     ptrSTF,
                                                     ntermK,
                                                     neqn,
                                                     const)
        else:
            warnings.warn('Missing stiffness matrix')
            kdata = None

        if ntermM:
            mrow, mcol, mdata = _binary_reader.ReadArray(self.filename,
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
        dof_ref, index, nref, dref = _binary_reader.SortNodalEqlv(neqn, neqv, ndof)

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
    standard_header = read_standard_header(filename)
    if standard_header['file format'] != 12:
        raise Exception('Binary file is not a result file.')

    # determine if cyclic
    with open(filename, 'rb') as f:
        f.seek(103 * 4)
        result_header = parse_header(read_table(f), RESULT_HEADER_KEYS)

    if result_header['nSector'] == 1:
        log.debug('Initializing standard result')
        return Result(filename)
    else:
        log.debug('Initializing cyclic result')
        return pyansys.CyclicResult(filename)


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
        self.resultheader = result_info(filename)

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
        self.store_geometry()

    def plot(self, color='w', show_edges=True, **kwargs):
        """ plots result geometry """
        return self.grid.plot(color=color, show_edges=show_edges, **kwargs)

    def plot_nodal_solution(self, rnum, comp='norm', label='',
                          cmap=None, flip_scalars=None, cpos=None,
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

        cmap : str, optional
           Cmap string.  See available matplotlib cmaps.

        flip_scalars : bool, optional
            Flip direction of cmap.

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
        rnum = self.parse_step_substep(rnum)
        nnum, result = self.nodal_solution(rnum)

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
        npoints = self.grid.number_of_points
        if nnum.size != npoints:
            scalars = np.empty(npoints)
            scalars[:] = np.nan
            nnum_grid = self.grid.point_arrays['ansys_node_num']
            mask = np.in1d(nnum_grid, nnum)
            scalars[mask] = d
            d = scalars

        return self.plot_point_scalars(d, rnum, stitle, cmap,
                                       flip_scalars, screenshot, cpos,
                                       interactive=interactive,
                                       **kwargs)

    @property
    def time_values(self):
        return self.resultheader['time_values']

    def animate_nodal_solution(self, rnum, comp='norm', max_disp=0.1,
                               nangles=100, show_phase=True,
                               show_result_info=True,
                               interpolate_before_map=True, cpos=None,
                               movie_filename=None, interactive=True,
                               **kwargs):
        """
        Animate nodal solution.  Assumes nodal solution is a displacement 
        array from a modal solution.

        rnum : int or list
            Cumulative result number with zero based indexing, or a list 
            containing (step, substep) of the requested result.

        comp : str, optional
            Display component to display.  Options are 'x', 'y', 'z', and
            'norm', corresponding to the x directin, y direction, z direction,
            and the combined direction (x**2 + y**2 + z**2)**0.5

        max_disp : float, optional
            Maximum displacement in the units of the model.  Default 0.1

        nangles : int, optional
            Number of "frames" between each full cycle.

        show_phase : bool, optional
            Shows the phase at each frame.

        show_result_info : bool, optional
            Includes result information at the bottom left-hand corner of the
            plot.

        interpolate_before_map : bool, optional
            Leaving this at default generally results in a better plot.

        cpos : list, optional
            List of camera position, focal point, and view up.

        movie_filename : str, optional
            Filename of the movie to open.  Filename should end in mp4,
            but other filetypes may be supported.  See "imagio.get_writer".
            A single loop of the mode will be recorded.

        interactive : bool, optional
            Can be used in conjunction with movie_filename to generate a
            movie non-interactively.

        kwargs : optional keyword arguments, optional
            See help(vtki.Plot) for additional keyword arguments.

        """
        # normalize nodal solution
        nnum, disp = self.nodal_solution(rnum)
        disp /= (np.abs(disp).max()/max_disp)
        # disp = disp.reshape(-1, 3)
        
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

        if disp.shape[1] == 2:
            disp = np.hstack((disp, np.zeros((disp.shape[0], 1))))

        orig_pt = self.grid.points

        if show_result_info:
            result_info = self.text_result_table(rnum)

        plobj = vtki.Plotter(off_screen=not interactive)
        plobj.add_mesh(self.grid.copy(), scalars=np.real(scalars),
                      interpolate_before_map=interpolate_before_map, **kwargs)
        plobj.update_coordinates(orig_pt, render=False)

        # setup text
        plobj.add_text(' ', font_size=30)

        if cpos:
            plobj.camera_position = cpos

        if movie_filename:
            plobj.open_movie(movie_filename)

        # run until q is pressed
        plobj.plot(interactive=False, auto_close=False,
                   interactive_update=True)
        first_loop = True
        while not plobj.q_pressed:
            for angle in np.linspace(0, np.pi*2, nangles):
                mag_adj = np.sin(angle)
                disp_adj = disp*mag_adj

                if axis is not None:
                    scalars = disp_adj[:, axis]
                else:
                    scalars = (disp_adj*disp_adj).sum(1)**0.5

                plobj.update_scalars(scalars, render=False)
                plobj.update_coordinates(orig_pt + disp_adj, render=False)
                if show_phase:
                    plobj.textActor.SetInput('%s\nPhase %.1f Degrees' %
                                             (result_info, (angle*180/np.pi)))

                if interactive:
                    plobj.update(30, force_redraw=True)

                if plobj.q_pressed:
                    break

                if movie_filename and first_loop:
                    plobj.write_frame()

            first_loop = False
            if not interactive:
                break

        return plobj.close()

    def nodal_solution(self, rnum, in_nodal_coord_sys=False):
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
        rnum = self.parse_step_substep(rnum)

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
                vtki.common.axis_rotation(r, theta_xy, inplace=True, axis='z')

            if np.any(theta_yz):
                vtki.common.axis_rotation(r, theta_yz, inplace=True, axis='x')

            if np.any(theta_zx):
                vtki.common.axis_rotation(r, theta_zx, inplace=True, axis='y')

        # also include nodes in output
        return self.nnum, r

    def store_geometry(self):
        """ Stores the geometry from the result file """
        # read in the geometry from the result file
        with open(self.filename, 'rb') as f:

            # read geometry header
            f.seek(self.resultheader['ptrGEO']*4)
            table = read_table(f)
            geometry_header = parse_header(table, GEOMETRY_HEADER_KEYS)
            self.geometry_header = geometry_header

            # Node information
            nnod = geometry_header['nnod']
            nnum = np.empty(nnod, np.int32)
            nloc = np.empty((nnod, 6), np.float)
            _binary_reader.load_nodes(self.filename, geometry_header['ptrLOC'],
                                      nnod, nloc, nnum)

            # Element information
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
            keyopts = np.zeros((10000, 11), np.int16)
            for i in range(maxety):
                f.seek((geometry_header['ptrETY'] + e_type_table[i] + 2)*4)
                einfo = np.fromfile(f, self.resultheader['endian'] + 'i', 2)
                etype_ref = einfo[0]
                etype_ID[i] = einfo[1]
                ekey.append(einfo)

                # Items 3-14 - element type option keys (keyopts)
                f.seek((geometry_header['ptrETY'] + e_type_table[i] + 1 + 3)*4)
                keyopts[etype_ref] = np.fromfile(
                    f, self.resultheader['endian'] + 'i', 11)

                # Item 61 - number of nodes for this element type (nodelm)
                f.seek((geometry_header['ptrETY'] + e_type_table[i] + 1 + 61)*4)
                nodelm[etype_ref] = np.fromfile(
                    f, self.resultheader['endian'] + 'i', 1)

                # Item 63 - number of nodes per element having nodal
                # forces, etc. (nodfor)
                f.seek((geometry_header['ptrETY'] + e_type_table[i] + 1 + 63)*4)
                nodfor[etype_ref] = np.fromfile(
                    f, self.resultheader['endian'] + 'i', 1)

                # Item 94 - number of nodes per element having nodal
                # stresses, etc. (nodstr).  This number is the number
                # of corner nodes for higher-ordered elements.
                f.seek((geometry_header['ptrETY'] + e_type_table[i] + 1 + 94)*4)
                nodstr[etype_ref] = np.fromfile(
                    f, self.resultheader['endian'] + 'i', 1)

                # with KEYOPT(8)=0, the record contains stresses at
                # each corner node (first at the bottom shell surface,
                # then the top surface)
                #
                # Only valid for SHELL181 or SHELL281 elements.
                if einfo[1] == 181 or einfo[1] == 281:
                    if keyopts[etype_ref, 7] == 0:
                        nodstr[etype_ref] *= 2

            # store element table data
            self.element_table = {'nodelm': nodelm,
                                  'nodfor': nodfor,
                                  'nodstr': nodstr,
                                  'keyopts': keyopts}

            # get the element description table
            f.seek((geometry_header['ptrEID'] + 2)*4)
            e_disp_table = np.empty(nelm, np.int32)
            e_disp_table[:] = np.fromfile(
                f, self.resultheader['endian'] + 'i8', nelm)

            # get pointer to start of element table and adjust element pointers
            ptr = geometry_header['ptrEID'] + e_disp_table[0]
            e_disp_table -= e_disp_table[0]

            # read in coordinate systems
            c_systems = parse_coordinate_system(f, geometry_header)

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
        _binary_reader.LoadElements(self.filename, ptr, nelm, e_disp_table, elem,
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
                         'Element Type': element_type,
                         'coord systems': c_systems}

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
        self.quadgrid = vtki.UnstructuredGrid(offset, cells,
                                                      cell_type, nodes)
        self.quadgrid.cell_arrays['ansys_elem_num'] = enum
        self.quadgrid.point_arrays['ansys_node_num'] = nnum
        self.quadgrid.cell_arrays['Element Type'] = element_type
        self.grid = self.quadgrid.linear_copy()

    def element_solution_header(self, rnum):
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
            solution_header = parse_header(read_table(f), SOLUTION_HEADER_KEYS)

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
            ele_ind_table = read_table(f, 'i8', nelm) + element_rst_ptr

            # boundary conditions
            # ptr = rpointers[rnum] + solution_header['ptrBC']
            # f.seek(ptr*4)
            # table = read_table(f, 'i')

        return ele_ind_table, nodstr, etype

    def nodal_stress(self, rnum):
        """
        Equivalent ANSYS command: PRNSOL, S

        Retrieves the component stresses for each node in the solution.

        The order of the results corresponds to the sorted node
        numbering.

        This algorithm, like ANSYS, computes the nodal stress by
        averaging the stress for each element at each node.  Due to
        the discontinuities across elements, stresses will vary based
        on the element they are evaluated from.

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
        rnum = self.parse_step_substep(rnum)
        ele_ind_table, nodstr, etype = self.element_solution_header(rnum)

        if self.resultheader['rstsprs'] != 0:
            nitem = 6
        else:
            nitem = 11

        # certain element types do not output stress
        elemtype = self.geometry['Element Type'].astype(np.int32)
        # validmask = np.in1d(elemtype, validENS).astype(np.int32)

        # if cyclic rotor
        if ele_ind_table.size != self.grid.number_of_cells:
            if not hasattr(self, 'nsector'):
                raise Exception('Element table size does not match number of cells')
            ind = self.grid.cell_arrays['vtkOriginalCellIds']
            ele_ind_table = ele_ind_table[ind]

        data, ncount = _binary_reader.read_nodal_values(self.filename,
                                                    self.grid.celltypes,
                                                    ele_ind_table + 2,
                                                    self.grid.offset,
                                                    self.grid.cells,
                                                    nitem,
                                                    self.grid.number_of_points,
                                                    nodstr,
                                                    etype,
                                                    elemtype)

        if nitem != 6:
            data = data[:, :6]

        nnum = self.grid.point_arrays['ansys_node_num']
        stress = data/ncount.reshape(-1, 1)

        return nnum, stress

    @property
    def version(self):
        """ returns the vesion of ansys used to save this result file """
        return float(self.resultheader['verstring'])

    def element_stress(self, rnum, principal=False, in_element_coord_sys=False):
        """
        Equivalent ANSYS command: PRESOL, S

        Retrives the element component stresses.

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a list 
            containing (step, substep) of the requested result.

        principal : bool, optional
            Returns principal stresses instead of component stresses.  Default
            False.

        in_element_coord_sys : bool, optional
            Returns the results in the element coordinate system.  Default
            False and will return the results in the global coordinate system.

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

        Notes
        -----
        Shell stresses for element 181 are returned for top and bottom layers.
        Results are ordered such that the top layer and then the bottom layer
        is reported.

        """
        rnum = self.parse_step_substep(rnum)
        ele_ind_table, nodstr, etype = self.element_solution_header(rnum)

        # certain element types do not output stress
        elemtype = self.geometry['Element Type'].astype(np.int32)
        etype = etype.astype(ctypes.c_int64)

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

            _binary_reader.read_element_stress(self.filename,
                                               ele_ind_table + 2,
                                               nodstr.astype(np.int64),
                                               etype,
                                               ele_data_arr,
                                               nitem,
                                               elemtype,
                                               as_global=not in_element_coord_sys)
            if nitem != 6:
                ele_data_arr = ele_data_arr[:, :6]

        else:
            raise Exception('Not implemented for ANSYS older than v14.5')

        if principal:
            ele_data_arr, isnan = _binary_reader.ComputePrincipalStress(ele_data_arr)
            ele_data_arr[isnan] = np.nan

        splitind = np.cumsum(nnode)
        element_stress = np.split(ele_data_arr, splitind[:-1])

        # reorder list using sorted indices
        # enum = self.grid.cell_arrays['ansys_elem_num']
        enum = self.geometry['enum']
        sidx = np.argsort(enum)
        element_stress = [element_stress[i] for i in sidx]

        elem = self.geometry['elem']
        enode = []
        for i in sidx:
            enode.append(elem[i, :nnode[i]])

        # Get element numbers
        elemnum = self.geometry['enum'][self.sidx_elem]
        return element_stress, elemnum, enode

    def element_solution_data(self, rnum, datatype, sort=True):
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

        rnum = self.parse_step_substep(rnum)
        ele_ind_table, nodstr, etype = self.element_solution_header(rnum)

        element_data = []
        f = open(self.filename, 'rb')
        for ind in ele_ind_table:
            # read element table index
            f.seek(ind*4)
            table = read_table(f)

            ptr = table[table_index]
            if ptr <= 0:
                element_data.append(None)
            else:
                f.seek((ind + ptr)*4)
                data = read_table(f, 'f')  # TODO: Verify datatype
                element_data.append(data)

        enum = self.grid.cell_arrays['ansys_elem_num']
        if sort:
            sidx = np.argsort(enum)
            enum = enum[sidx]
            element_data = [element_data[i] for i in sidx]        

        return enum, element_data

    def principal_nodal_stress(self, rnum):
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
        nodenum, stress = self.nodal_stress(rnum)

        # compute principle stress
        if stress.dtype != np.float32:
            stress = stress.astype(np.float32)

        pstress, isnan = _binary_reader.ComputePrincipalStress(stress)
        pstress[isnan] = np.nan
        return nodenum, pstress

    def plot_principal_nodal_stress(self, rnum, stype=None,
                                 cmap=None, flip_scalars=None,
                                 cpos=None, screenshot=None,
                                 interactive=True, **kwargs):
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

        cmap : str, optional
           Cmap string.  See available matplotlib cmaps.  Only applicable for
           when displaying scalars.  Defaults None (rainbow).  Requires matplotlib.

        flip_scalars : bool, optional
            Flip direction of cmap.

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
        if stype is None:
            raise Exception("Stress type must be a string from the following list:\n" +
                            "['S1', 'S2', 'S3', 'SINT', 'SEQV']")

        rnum = self.parse_step_substep(rnum)
        stress = self.principle_stress_for_plotting(rnum, stype)

        # Generate plot
        stitle = 'Nodal Stress\n%s\n' % stype
        cpos = self.plot_point_scalars(stress, rnum, stitle, cmap, flip_scalars,
                                     screenshot, cpos, interactive, **kwargs)
        return cpos, stress

    def plot_point_scalars(self, scalars, rnum=None, stitle='', cmap=None,
                         flip_scalars=None, screenshot=None, cpos=None,
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

        cmap : str
            See matplotlib cmaps:
            matplotlib.org/examples/color/cmaps_reference.html

        flip_scalars : bool
            Reverses the direction of the cmap.

        screenshot : str
            When a filename, saves screenshot to disk.

        cpos : list
            3x3 list describing the camera position.  Obtain it by getting the output
            of plot_point_scalars first.

        interactive : bool
            Allows user to interact with the plot when True.  Default True.

        grid : vtki PolyData or UnstructuredGrid, optional
            Uses self.grid by default.  When specified, uses this grid instead.

        Returns
        -------
        cpos : list
            Camera position.

        """
        if grid is None:
            grid = self.grid

        # make cmap match default ansys
        if cmap is None and flip_scalars is None:
            flip_scalars = False

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

        # need to ignore cells containing all nan
        # breakpoint()

        # cell_mask = np.empty(grid.n_cells, np.bool)
        offset = grid.offset.astype(np.int32)
        cells = grid.cells.astype(np.int32)
        
        # need special treatment for quatratic plane elements
        # breakpoint()
        # scalars = scalars.ravel().astype(np.double)
        # relax_plane_scalars(grid.celltypes, cells, offset, scalars)
        # ngrid = grid.extract_cells(grid.celltypes == 12)

        # Plot off screen when not interactive
        plobj = vtki.Plotter(off_screen=not(interactive))
        if 'show_axes' in kwargs:
            plobj.add_axes()

        plobj.add_mesh(grid, scalars=scalars, stitle=stitle,
                       cmap=cmap, flip_scalars=flip_scalars,
                       interpolate_before_map=True, **kwargs)

        # NAN/missing data are white
        plobj.mapper.GetLookupTable().SetNanColor(1, 1, 1, 1)

        if cpos:
            plobj.camera_position = cpos

        # add table
        if add_text and rnum is not None:
            plobj.add_text(self.text_result_table(rnum), font_size=20)

        if screenshot:
            cpos = plobj.plot(auto_close=False, interactive=interactive,
                              window_size=window_size,
                              full_screen=full_screen)
            if screenshot is True:
                img = plobj.screenshot()
            else:
                plobj.screenshot(screenshot)
            plobj.close()
        else:
            cpos = plobj.plot(interactive=interactive, window_size=window_size,
                              full_screen=full_screen)

        if screenshot is True:
            return cpos, img
        else:
            return cpos

    def text_result_table(self, rnum):
        """ Returns a text result table for plotting """
        ls_table = self.resultheader['ls_table']
        timevalue = self.time_values[rnum]
        text = 'Cumulative Index: {:3d}\n'.format(ls_table[rnum, 2])
        if self.resultheader['nSector'] > 1:
            hindex = self.resultheader['hindex'][rnum]
            text += 'Harmonic Index    {:3d}\n'.format(hindex)
        text += 'Loadstep:         {:3d}\n'.format(ls_table[rnum, 0])
        text += 'Substep:          {:3d}\n'.format(ls_table[rnum, 1])
        text += 'Time Value:     {:10.4f}'.format(timevalue)

        return text

    def principle_stress_for_plotting(self, rnum, stype):
        """
        returns stress used to plot

        """
        stress_types = ['S1', 'S2', 'S3', 'SINT', 'SEQV']
        if stype.upper() not in stress_types:
            raise Exception('Stress type not in \n' + str(stress_types))

        sidx = stress_types.index(stype)

        _, stress = self.principal_nodal_stress(rnum)
        return stress[:, sidx]

    def plot_nodal_stress(self, rnum, stype, cmap=None, flip_scalars=None,
                        cpos=None, screenshot=None, interactive=True, **kwargs):
        """
        Plots the stresses at each node in the solution.

        The order of the results corresponds to the sorted node numbering.
        This algorithm, like ANSYS, computes the node stress by averaging the
        stress for each element at each node.  Due to the discontinuities
        across elements, stresses will vary based on the element they are
        evaluated from.

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a list containing
            (step, substep) of the requested result.

        stype : string
            Stress type from the following list: [Sx Sy Sz Sxy Syz Sxz]

        cmap : str, optional
           Cmap string.  See available matplotlib cmaps.

        flip_scalars : bool, optional
            Flip direction of cmap.

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
        rnum = self.parse_step_substep(rnum)
        stress_types = ['sx', 'sy', 'sz', 'sxy', 'syz', 'sxz', 'seqv']
        stype = stype.lower()
        if stype not in stress_types:
            raise Exception('Stress type not in: \n' + str(stress_types))

        sidx = stress_types.index(stype)

        # Populate with nodal stress at edge nodes
        nnum, stress = self.nodal_stress(rnum)
        stress = stress[:, sidx]

        stitle = 'Nodal Stress\n{:s}'.format(stype.capitalize())
        cpos = self.plot_point_scalars(stress, rnum, stitle, cmap, flip_scalars,
                                     screenshot, cpos, interactive, **kwargs)

        return cpos

    def save_as_vtk(self, filename, binary=True):
        """
        Appends all results to an unstructured grid and writes it to
        disk.

        The file extension will select the type of writer to use.
        '.vtk' will use the legacy writer, while '.vtu' will select
        the VTK XML writer.

        Parameters
        ----------
        filename : str
            Filename of grid to be written.  The file extension will
            select the type of writer to use.  '.vtk' will use the
            legacy writer, while '.vtu' will select the VTK XML
            writer.

        binary : bool, optional
            Writes as a binary file by default.  Set to False to write
            ASCII

        Notes
        -----
        Binary files write much faster than ASCII, but binary files
        written on one system may not be readable on other systems.
        Binary can only be selected for the legacy writer.
        """
        # Copy grid as to not write results to original object
        grid = self.grid.copy()

        for i in range(self.nsets):
            # Nodal results
            _, val = self.nodal_solution(i)
            grid.point_arrays['nodal_solution{:03d}'.format(i)] = val

            # Populate with nodal stress at edge nodes
            nodenum = self.grid.point_arrays['ansys_node_num']
            _, stress = self.nodal_stress(i)
            grid.point_arrays['nodal_stress{:03d}'.format(i)] = stress

        grid.save(filename)

    def write_tables(self, filename):
        """ Write binary tables to ASCII.  Assumes int32  """
        rawresult = open(self.filename, 'rb')
        with open(filename, 'w') as f:
            while True:
                try:
                    table = read_table(rawresult)
                    f.write('*** %d ***\n' % len(table))
                    for item in table:
                        f.write(str(item) + '\n')
                    f.write('\n\n')
                except:
                    break
        rawresult.close()

    def parse_step_substep(self, user_input):
        """ Converts (step, substep) to a cumulative index """
        if is_int(user_input):
            # check if result exists
            if user_input > self.nsets - 1:
                raise Exception('Only %d result(s) in the result file.' % self.nsets)
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


def result_info(filename):
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
    standard_header = read_standard_header(filename)
    endian = standard_header['endian']

    with open(filename, 'rb') as f:
        # Read .RST FILE HEADER
        f.seek(103 * 4)
        header = parse_header(read_table(f), RESULT_HEADER_KEYS)
        resultheader = merge_two_dicts(header, standard_header)

        # Read nodal equivalence table
        f.seek(resultheader['ptrNOD']*4)
        resultheader['neqv'] = read_table(f)

        # Read nodal equivalence table
        f.seek(resultheader['ptrELM']*4)
        resultheader['eeqv'] = read_table(f)

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
        table = read_table(f, 'd', resultheader['nsets'])
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


def read_table(f, dtype='i', nread=None, skip=False, get_nread=True):
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


def two_ints_to_long(intl, inth):
    """ Interpert two ints as one long """
    longint = struct.pack(">I", inth) + struct.pack(">I", intl)
    return struct.unpack('>q', longint)[0]


def pol2cart(rho, phi):
    """ Convert cylindrical to cartesian """
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return x, y


def parse_header(table, keys):
    """ parses a header from a table """
    header = {}
    for i, key in enumerate(keys):
        header[key] = table[i]

    for key in keys:
        if 'ptr' in key and key[-1] == 'h':
            basekey = key[:-1]
            intl = header[basekey + 'l']
            inth = header[basekey + 'h']
            header[basekey] = two_ints_to_long(intl, inth)

    return header


def read_standard_header(filename):
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
        header['file number'] = read_table(f, nread=1, get_nread=False)[0]
        header['file format'] = read_table(f, nread=1, get_nread=False)[0]
        int_time = str(read_table(f, nread=1, get_nread=False)[0])
        header['time'] = ':'.join([int_time[0:2], int_time[2:4], int_time[4:]])
        int_date = str(read_table(f, nread=1, get_nread=False)[0])
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
        header['units'] = unit_types[read_table(f, nread=1, get_nread=False)[0]]

        f.seek(11 * 4)
        version = read_string_from_binary(f, 1).strip()

        header['verstring'] = version
        header['mainver'] = int(version[:2])
        header['subver'] = int(version[-1])

        # there's something hidden at 12
        f.seek(4, 1)

        # f.seek(13 * 4)
        header['machine'] = read_string_from_binary(f, 3).strip()
        header['jobname'] = read_string_from_binary(f, 2).strip()
        header['product'] = read_string_from_binary(f, 2).strip()
        header['special'] = read_string_from_binary(f, 1).strip()
        header['username'] = read_string_from_binary(f, 3).strip()

        # Items 23-25 The machine identifier in integer form (three four-character strings)
        # this contains license information
        header['machine_identifier'] = read_string_from_binary(f, 3).strip()

        # Item 26 The system record size
        header['system record size'] = read_table(f, nread=1, get_nread=False)[0]

        # Item 27 The maximum file length
        # header['file length'] = read_table(f, nread=1, get_nread=False)[0]

        # Item 28 The maximum record number
        # header['the maximum record number'] = read_table(f, nread=1, get_nread=False)[0]

        # Items 31-38 The Jobname (eight four-character strings)
        f.seek(32*4)
        header['jobname2'] = read_string_from_binary(f, 8).strip()

        # Items 41-60 The main analysis title in integer form (20 four-character strings)
        f.seek(42*4)
        header['title'] = read_string_from_binary(f, 20).strip()

        # Items 61-80 The first subtitle in integer form (20 four-character strings)
        header['subtitle'] = read_string_from_binary(f, 20).strip()

        # Item 95 The split point of the file (0 means the file will not split)
        f.seek(96*4)
        header['split point'] = read_table(f, nread=1, get_nread=False)[0]

        # Items 97-98 LONGINT of the maximum file length (bug here)
        # ints = read_table(f, nread=2, get_nread=False)
        # header['file length'] = two_ints_to_long(ints[0], ints[1])

    return header


def read_string_from_binary(f, n):
    """ Read n 4 character binary strings from a file opend in binary mode """
    string = b''
    for i in range(n):
        string += f.read(4)[::-1]

    try:
        return string.decode('utf')
    except:
        return string


def is_int(value):
    """ Return true if can be parsed as an int """
    try:
        int(value)
        return True
    except:
        return False


def parse_coordinate_system(f, geometry_header):
    """
    Reads in coordinate system information from a binary result file.

    Parameters
    ----------
    f : file object
        Open binary result file.

    geometry_header, dict
        Dictionary containing pointers to geometry items in the ansys
        result.

    Returns
    -------
    c_systems : dict
        Dictionary containing one entry for each defined coordinate
        system.  If no non-standard coordinate systems have been
        defined, there will be only one None.  First coordinate system
        is assumed to be global cartesian.

    Notes
    -----
    euler angles : [THXY, THYZ, THZX]

    - First rotation about local Z (positive X toward Y).
    - Second rotation about local X (positive Y toward Z).
    - Third rotation about local Y (positive Z toward X).

    PAR1
    Used for elliptical, spheroidal, or toroidal systems. If KCS = 1
    or 2, PAR1 is the ratio of the ellipse Y-axis radius to X-axis
    radius (defaults to 1.0 (circle)). If KCS = 3, PAR1 is the major
    radius of the torus.

    PAR2
    Used for spheroidal systems. If KCS = 2, PAR2 = ratio of ellipse
    Z-axis radius to X-axis radius (defaults to 1.0 (circle)).

    Coordinate system type:
        - 0: Cartesian
        - 1: Cylindrical (circular or elliptical)
        - 2: Spherical (or spheroidal)
        - 3: Toroidal
    """
    # number of coordinate systems
    maxcsy = geometry_header['maxcsy']

    # load coordinate system index table
    ptr_csy = geometry_header['ptrCSYl']
    f.seek((ptr_csy + 2) * 4)
    csy = np.fromfile(f, 'i', maxcsy)

    # parse each coordinate system
    # The items stored in each record:
    # * Items 1-9  are the transformation matrix.
    # * Items 10-12 are the coordinate system origin (XC,YC,ZC).
    # * Items 13-14 are the coordinate system parameters (PAR1, PAR2).
    # * Items 16-18 are the angles used to define the coordinate system.
    # * Items 19-20 are theta and phi singularity keys.
    # * Item 21 is the coordinate system type (0, 1, 2, or 3).
    # * Item 22 is the coordinate system reference number.
    c_systems = [None]
    for i in range(maxcsy):
        f.seek((ptr_csy + csy[i] + 2) * 4)
        data = np.fromfile(f, 'd', 22)
        c_system = {'transformation matrix': np.array(data[:9].reshape(-1, 3)),
                    'origin': np.array(data[9:12]),
                    'PAR1': data[12],
                    'PAR2': data[13],
                    'euler angles': data[15:18], # may not be euler
                    'theta singularity' : data[18],
                    'phi singularity' : data[19],
                    'type' : int(data[20]),
                    'reference num' : int(data[21],)
                    }
        c_systems.append(c_system)

    return c_systems


def trans_to_matrix(trans):
    """ Convert a numpy.ndarray to a vtk.vtkMatrix4x4 """
    matrix = vtk.vtkMatrix4x4()
    for i in range(trans.shape[0]):
        for j in range(trans.shape[1]):
            matrix.SetElement(i, j, trans[i, j])
    return matrix


def transform(points, trans):
    """
    In-place 3d transformation of a points array given a 4x4 
    transformation matrix.

    Parameters
    ----------
    points : np.ndarray or vtk.vtkTransform
        Points to transform.

    transform : np.ndarray or vtk.vtkTransform
        4x4 transformation matrix.

    """
    if isinstance(trans, vtk.vtkMatrix4x4):
        trans = vtki.trans_from_matrix(trans)

    if points.dtype == np.float32:
        _binary_reader.affline_transform_float(points, trans)
    else:
        _binary_reader.affline_transform_double(points, trans)
