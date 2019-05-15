"""Read ANSYS binary result files *.rst
"""
import warnings
import logging
import ctypes

import vtk
import numpy as np
import pyvista as pv

from pyansys import _binary_reader, _parser, _reader
from pyansys.elements import valid_types
from pyansys._binary_reader import cells_with_any_nodes, cells_with_all_nodes
from pyansys.common import read_table, parse_header, read_standard_header

# Create logger
log = logging.getLogger(__name__)
log.setLevel('DEBUG')

np.seterr(divide='ignore', invalid='ignore')


def merge_two_dicts(x, y):
    merged = x.copy()   # start with x's keys and values
    merged.update(y)    # modifies z with y's keys and values & returns None
    return merged


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
                        'ptrNSL', 'ptrESL', 'ptrRF', 'ptrMST',
                        'ptrBC', 'rxtrap', 'mode', 'isym', 'kcmplx',
                        'numdof', 'DOFS', 'DOFS', 'DOFS', 'DOFS',
                        'DOFS', 'DOFS', 'DOFS', 'DOFS', 'DOFS',
                        'DOFS', 'DOFS', 'DOFS', 'DOFS', 'DOFS',
                        'DOFS', 'DOFS', 'DOFS', 'DOFS', 'DOFS',
                        'DOFS', 'DOFS', 'DOFS', 'DOFS', 'DOFS',
                        'DOFS', 'DOFS', 'DOFS', 'DOFS', 'DOFS',
                        'DOFS', 'title', 'title', 'title', 'title',
                        'title', 'title', 'title', 'title', 'title',
                        'title', 'title', 'title', 'title', 'title',
                        'title', 'title', 'title', 'title', 'title',
                        'title', 'stitle', 'stitle', 'stitle',
                        'stitle', 'stitle', 'stitle', 'stitle',
                        'stitle', 'stitle', 'stitle', 'stitle',
                        'stitle', 'stitle', 'stitle', 'stitle',
                        'stitle', 'stitle', 'stitle', 'stitle',
                        'stitle', 'dbmtim', 'dbmdat', 'dbfncl',
                        'soltim', 'soldat', 'ptrOND', 'ptrOEL',
                        'nfldof', 'ptrEXA', 'ptrEXT', 'ptrEXAl',
                        'ptrEXAh', 'ptrEXTl', 'ptrEXTh', 'ptrNSLl',
                        'ptrNSLh', 'ptrRFl', 'ptrRFh', 'ptrMSTl',
                        'ptrMSTh', 'ptrBCl', 'ptrBCh', 'ptrTRFl',
                        'ptrTRFh', 'ptrONDl', 'ptrONDh', 'ptrOELl',
                        'ptrOELh', 'ptrESLl', 'ptrESLh', 'ptrOSLl',
                        'ptrOSLh', '0', '0', '0', 'PrinKey',
                        'numvdof', 'numadof', '0', '0', 'ptrVSLl',
                        'ptrVSLh', 'ptrASLl', 'ptrASLh', '0', '0',
                        '0', '0', 'numRotCmp', '0', 'ptrRCMl',
                        'ptrRCMh', 'nNodStr', '0', 'ptrNDSTRl',
                        'ptrNDSTRh', 'AvailData', 'geomID', 'ptrGEOl',
                        'ptrGEOh']

GEOMETRY_HEADER_KEYS = ['__unused', 'maxety', 'maxrl', 'nnod', 'nelm',
                        'maxcsy', 'ptrETY', 'ptrREL', 'ptrLOC',
                        'ptrCSY', 'ptrEID', 'maxsec', 'secsiz',
                        'maxmat', 'matsiz', 'ptrMAS', 'csysiz',
                        'elmsiz', 'etysiz', 'rlsiz', 'ptrETYl',
                        'ptrETYh', 'ptrRELl', 'ptrRELh', 'ptrCSYl',
                        'ptrCSYh', 'ptrLOCl', 'ptrLOCh', 'ptrEIDl',
                        'ptrEIDh', 'ptrMASl', 'ptrMASh', 'ptrSECl',
                        'ptrSECh', 'ptrMATl', 'ptrMATh', 'ptrCNTl',
                        'ptrCNTh', 'ptrNODl', 'ptrNODh', 'ptrELMl',
                        'ptrELMh', 'Glbnnod', 'ptrGNODl', 'ptrGNODh',
                        'maxn', 'NodesUpd', 'lenbac', 'maxcomp',
                        'compsiz', 'ptrCOMPl', 'ptrCOMPh']

RESULT_HEADER_KEYS = ['fun12', 'maxn', 'nnod', 'resmax', 'numdof',
                      'maxe', 'nelm', 'kan', 'nsets', 'ptrend',
                      'ptrDSIl', 'ptrTIMl', 'ptrLSPl', 'ptrELMl',
                      'ptrNODl', 'ptrGEOl', 'ptrCYCl', 'CMSflg',
                      'csEls', 'units', 'nSector', 'csCord',
                      'ptrEnd8', 'ptrEnd8', 'fsiflag', 'pmeth',
                      'noffst', 'eoffst', 'nTrans', 'ptrTRANl',
                      'PrecKey', 'csNds', 'cpxrst', 'extopt',
                      'nlgeom', 'AvailData', 'mmass', 'kPerturb',
                      'XfemKey', 'rstsprs', 'ptrDSIh', 'ptrTIMh',
                      'ptrLSPh', 'ptrCYCh', 'ptrELMh', 'ptrNODh',
                      'ptrGEOh', 'ptrTRANh', 'Glbnnod', 'ptrGNODl',
                      'ptrGNODh', 'qrDmpKy', 'MSUPkey', 'PSDkey',
                      'cycMSUPkey', 'XfemCrkPropTech']


class ResultFile(object):
    """Reads a binary ANSYS result file.

    Parameters
    ----------
    filename : str, optional
        Filename of the ANSYS binary result file.

    ignore_cyclic : bool, optional
        Ignores any cyclic properties.
    """

    def __init__(self, filename, ignore_cyclic=False):
        """Loads basic result information from result file and
        initializes result object.
        """
        self.filename = filename
        self.resultheader = result_info(self.filename)

        # Get the total number of results and log it
        self.nsets = len(self.resultheader['rpointers'])
        log.debug('There are %d result(s) in this file' % self.nsets)

        # Get indices to resort nodal and element results
        self.sidx = np.argsort(self.resultheader['neqv'])
        self.sidx_elem = np.argsort(self.resultheader['eeqv'])

        # Store node numbering in ANSYS
        self.nnum = self.resultheader['neqv'][self.sidx]
        self.enum = self.resultheader['eeqv'][self.sidx_elem]

        # store geometry for later retrival
        self.store_geometry()

        with open(self.filename, 'rb') as f:
            f.seek(103*4)  # start of secondary header
            self.header = parse_header(read_table(f), RESULT_HEADER_KEYS)

    def plot(self, color='w', show_edges=True, **kwargs):
        """Plot result geometry

        Parameters
        ----------
        color : string or 3 item list, optional, defaults to white
            Either a string, rgb list, or hex color string.  For example:
                color='white'
                color='w'
                color=[1, 1, 1]
                color='#FFFFFF'

            Color will be overridden when scalars are input.

        show_edges : bool, optional
            Shows the edges of a mesh.  Does not apply to a wireframe
            representation.

        style : string, optional
            Visualization style of the vtk mesh.  One for the
            following:
                style='surface'
                style='wireframe'
                style='points'

            Defaults to 'surface'

        off_screen : bool
            Plots off screen when True.  Helpful for saving
            screenshots without a window popping up.

        full_screen : bool, optional
            Opens window in full screen.  When enabled, ignores
            window_size.  Default False.

        screenshot : str or bool, optional
            Saves screenshot to file when enabled.  See:
            help(pyvista.Plotter.screenshot).  Default disabled.

            When True, takes screenshot and returns numpy array of
            image.

        window_size : list, optional
            Window size in pixels.  Defaults to [1024, 768]

        show_bounds : bool, optional
            Shows mesh bounds when True.  Default False. Alias
            ``show_grid`` also accepted.

        show_axes : bool, optional
            Shows a vtk axes widget.  Enabled by default.

        Returns
        -------
        cpos : list
            List of camera position, focal point, and view up.
        """
        return self.grid.plot(color=color, show_edges=show_edges, **kwargs)
    
    def plot_nodal_solution(self, rnum, comp='norm', label='',
                            cmap=None, flip_scalars=None, cpos=None,
                            screenshot=None, interactive=True,
                            node_components=None, sel_type_all=True,
                            **kwargs):
        """
        Plots a nodal result.

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        comp : str, optional
            Display component to display.  Options are 'x', 'y', 'z',
            and 'norm', corresponding to the x directin, y direction,
            z direction, and the combined direction (x**2 + y**2 +
            z**2)**0.5

        label : str, optional
            Annotation string to add to scalar bar in plot.

        cmap : str, optional
           Cmap string.  See available matplotlib cmaps.

        flip_scalars : bool, optional
            Flip direction of cmap.

        cpos : list, optional
            List of camera position, focal point, and view up.  Plot
            first, then output the camera position and save it.

        screenshot : str, optional
            Setting this to a filename will save a screenshot of the
            plot before closing the figure.

        interactive : bool, optional
            Default True.  Setting this to False makes the plot
            generate in the background.  Useful when generating plots
            in a batch mode automatically.

        node_components : list, optional
            Accepts either a string or a list strings of node
            components to plot.  For example: 
            ``['MY_COMPONENT', 'MY_OTHER_COMPONENT]``

        sel_type_all : bool, optional
            If node_components is specified, plots those elements
            containing all nodes of the component.  Default True.

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
            scalars = result[:, 0]
            stitle = 'X {:s}\n'.format(label)

        elif comp == 'y':
            scalars = result[:, 1]
            stitle = 'Y {:s}\n'.format(label)

        elif comp == 'z':
            scalars = result[:, 2]
            stitle = 'Z {:s}\n'.format(label)

        else:
            # Normalize displacement
            scalars = result[:, :3]
            scalars = (scalars*scalars).sum(1)**0.5

            stitle = 'Normalized\n%s\n' % label

        # sometimes there are less nodes in the result than in the geometry
        npoints = self.grid.number_of_points
        if nnum.size != npoints:
            new_scalars = np.empty(npoints)
            new_scalars[:] = np.nan
            nnum_grid = self.grid.point_arrays['ansys_node_num']
            mask = np.in1d(nnum_grid, nnum)
            new_scalars[mask] = scalars
            scalars = new_scalars

        if node_components:
            grid, ind = self._extract_node_components(node_components,
                                                      sel_type_all)
            scalars = scalars[ind]

        else:
            grid = self.grid

        if hasattr(self, 'n_sector'):
            from pyansys.cyclic_reader import CyclicResult
            return super(CyclicResult, self).plot_point_scalars(scalars,
                                                                rnum,
                                                                stitle,
                                                                cmap,
                                                                flip_scalars,
                                                                screenshot,
                                                                cpos,
                                                                interactive=interactive,
                                                                grid=grid,
                                                                **kwargs)
        else:
            return self.plot_point_scalars(scalars, rnum, stitle, cmap,
                                           flip_scalars, screenshot, cpos,
                                           interactive=interactive,
                                           grid=grid, **kwargs)

    def _extract_node_components(self, node_components,
                                 sel_type_all=True, grid=None):
        """ Returns the part of the grid matching node components """
        if grid is None:
            grid = self.grid

        if not self.geometry['components']:  # pragma: no cover
            raise Exception('Missing component information.\n' +
                            'Either no components have been stored, or ' +
                            'the version of this result file is <18.2')

        if isinstance(node_components, str):
            node_components = [node_components]

        mask = np.zeros(grid.n_points, np.bool)
        for component in node_components:
            component = component.upper()
            if component not in grid.point_arrays:
                raise Exception('Result file does not contain node ' +
                                'component "%s"' % component)

            mask += grid.point_arrays[component].view(np.bool)
            # mask = np.logical_not(mask)

        # need to extract the mesh
        cells = grid.cells
        offset = grid.offset
        if sel_type_all:
            cell_mask = cells_with_all_nodes(offset, cells, grid.celltypes,
                                             mask.view(np.uint8))
        else:
            cell_mask = cells_with_any_nodes(offset, cells, grid.celltypes,
                                             mask.view(np.uint8))

        reduced_grid = grid.extract_cells(cell_mask)

        if not reduced_grid.n_cells:
            raise Exception('Empty mesh due to component selection\n' +
                            'Try "sel_type_all=False"')

        ind = reduced_grid.point_arrays['vtkOriginalPointIds']
        return reduced_grid, ind

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
            See help(pyvista.Plot) for additional keyword arguments.

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

        plotter = pv.Plotter(off_screen=not interactive)
        plotter.add_mesh(self.grid.copy(), scalars=np.real(scalars),
                      interpolate_before_map=interpolate_before_map, **kwargs)
        plotter.update_coordinates(orig_pt, render=False)

        # setup text
        plotter.add_text(' ', font_size=30)

        if cpos:
            plotter.camera_position = cpos

        if movie_filename:
            plotter.open_movie(movie_filename)

        # run until q is pressed
        plotter.plot(interactive=False, auto_close=False,
                   interactive_update=True)
        first_loop = True
        while not plotter.q_pressed:
            for angle in np.linspace(0, np.pi*2, nangles):
                mag_adj = np.sin(angle)
                disp_adj = disp*mag_adj

                if axis is not None:
                    scalars = disp_adj[:, axis]
                else:
                    scalars = (disp_adj*disp_adj).sum(1)**0.5

                plotter.update_scalars(scalars, render=False)
                plotter.update_coordinates(orig_pt + disp_adj, render=False)
                if show_phase and show_result_info:
                    plotter.textActor.SetInput('%s\nPhase %.1f Degrees' %
                                             (result_info, (angle*180/np.pi)))

                if interactive:
                    plotter.update(30, force_redraw=True)

                if plotter.q_pressed:
                    break

                if movie_filename and first_loop:
                    plotter.write_frame()

            first_loop = False
            if not interactive:
                break

        return plotter.close()

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
        result = result.reshape((-1, numdof))

        # Reorder based on sorted indexing
        result = result.take(self.sidx, 0)

        if not in_nodal_coord_sys:
            # ansys writes the results in the nodal coordinate system.
            # Convert this to the global coordinate system  (in degrees)
            euler_angles = self.geometry['nodes'][self.insolution, 3:].T
            theta_xy, theta_yz, theta_zx = euler_angles

            if np.any(theta_xy):
                pv.common.axis_rotation(result, theta_xy, inplace=True, axis='z')

            if np.any(theta_yz):
                pv.common.axis_rotation(result, theta_yz, inplace=True, axis='x')

            if np.any(theta_zx):
                pv.common.axis_rotation(result, theta_zx, inplace=True, axis='y')

        # also include nodes in output
        return self.nnum, result

    def _read_components(self):
        """
        Read components from an ansys result file

        Returns
        components : dict
            Dictionary of components

        """
        components = {}
        ncomp = self.geometry_header['maxcomp']
        if not ncomp:
            return components

        ptr_comp = self.geometry_header['ptrCOMP']
        with open(self.filename, 'rb') as f:
            f.seek(ptr_comp*4)
            for i in range(ncomp):
                table = read_table(f)

                # strings are up to 32 characters
                raw = table[1:9].tobytes().split(b'\x00')[0]

                name = raw.decode('utf')
                name =  name[:4][::-1] + name[4:8][::-1] + name[8:12][::-1] +\
                        name[12:16][::-1] + name[16:20][::-1] + name[20:24][::-1] +\
                        name[24:28][::-1] + name[28:32][::-1]
                name = name.strip()
                components[name] = _reader.component_interperter(table[9:])

        return components

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

        components = self._read_components()

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
                         'coord systems': c_systems,
                         'components': components}

        # store the reference array
        # Allow quadradic and null unallowed
        parsed = _parser.parse(self.geometry, False, valid_types, True,
                               keyopts)
        cells = parsed['cells']
        offset = parsed['offset']
        cell_type = parsed['cell_type']
        self.numref = parsed['numref']        

        # catch -1
        cells[cells == -1] = 0

        # identify nodes that are actually in the solution
        self.insolution = np.in1d(self.geometry['nnum'],
                                  self.resultheader['neqv'])

        # Create vtk object
        nodes = nloc[:, :3]
        self.quadgrid = pv.UnstructuredGrid(offset, cells, cell_type, nodes)
        self.quadgrid.cell_arrays['ansys_elem_num'] = enum
        self.quadgrid.point_arrays['ansys_node_num'] = nnum
        self.quadgrid.cell_arrays['Element Type'] = element_type

        # add node components
        for component_name in components:
            mask = np.in1d(nnum, components[component_name])
            self.quadgrid.point_arrays[component_name] = mask

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
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        Returns
        -------
        nodenum : numpy.ndarray
            Node numbers of the result.

        stress : numpy.ndarray
            Stresses at Sx Sy Sz Sxy Syz Sxz averaged at each corner
            node.  For the corresponding node numbers, see where
            result is the result object.

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
        #     if not hasattr(self, 'n_sector'):
        #         raise Exception('Element table size does not match number of cells')
        #     ind = self.grid.cell_arrays['vtkOriginalCellIds']
        #     ele_ind_table = ele_ind_table[ind]

        # for sector results or if the grid doesn't match the number
        # of table element cells
        # if ele_ind_table.size != self.grid.n_cells:
        #     ind = self.grid.cell_arrays['vtkOriginalCellIds']
        #     ele_ind_table = ele_ind_table[ind]

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
        """ The version of ANSYS used to generate this result file """
        return float(self.resultheader['verstring'])

    def element_stress(self, rnum, principal=False, in_element_coord_sys=False):
        """
        Equivalent ANSYS command: PRESOL, S

        Retrives the element component stresses.

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        principal : bool, optional
            Returns principal stresses instead of component stresses.
            Default False.

        in_element_coord_sys : bool, optional
            Returns the results in the element coordinate system.
            Default False and will return the results in the global
            coordinate system.

        Returns
        -------
        element_stress : list
            Stresses at each element for each node for Sx Sy Sz Sxy
            Syz Sxz.  or SIGMA1, SIGMA2, SIGMA3, SINT, SEQV when
            principal is True.

        enum : np.ndarray
            ANSYS element numbers corresponding to each element.

        enode : list
            Node numbers corresponding to each element's stress
            results.  One list entry for each element.

        Notes
        -----
        Shell stresses for element 181 are returned for top and bottom
        layers.  Results are ordered such that the top layer and then
        the bottom layer is reported.

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

    def plot_principal_nodal_stress(self, rnum, stype=None, cmap=None,
                                    flip_scalars=None, cpos=None,
                                    screenshot=None, interactive=True,
                                    node_components=None, sel_type_all=True,
                                    **kwargs):
        """
        Plot the principal stress at each node in the solution.

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        stype : string
            Stress type to plot.  S1, S2, S3 principal stresses, SINT
            stress intensity, and SEQV equivalent stress.

            Stress type must be a string from the following list:

            ['S1', 'S2', 'S3', 'SINT', 'SEQV']

        cmap : str, optional
           Cmap string.  See available matplotlib cmaps.  Only
           applicable for when displaying scalars.  Defaults None
           (rainbow).  Requires matplotlib.

        flip_scalars : bool, optional
            Flip direction of cmap.

        cpos : list, optional
            List of camera position, focal point, and view up.  Plot
            first, then output the camera position and save it.

        screenshot : str, optional
            Setting this to a filename will save a screenshot of the
            plot before closing the figure.  Default None.

        interactive : bool, optional
            Default True.  Setting this to False makes the plot
            generate in the background.  Useful when generating plots
            in a batch mode automatically.

        node_components : list, optional
            Accepts either a string or a list strings of node
            components to plot.  For example: 
            ``['MY_COMPONENT', 'MY_OTHER_COMPONENT]``

        sel_type_all : bool, optional
            If node_components is specified, plots those elements
            containing all nodes of the component.  Default True.

        kwargs : keyword arguments
            Additional keyword arguments.  See help(pyvista.plot)

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

        if node_components:
            grid, ind = self._extract_node_components(node_components, sel_type_all)
            stress = stress[ind]
        else:
            grid = self.grid

        # Generate plot
        stitle = 'Nodal Stress\n%s\n' % stype
        cpos = self.plot_point_scalars(stress, rnum, stitle, cmap,
                                       flip_scalars, screenshot, cpos,
                                       interactive, grid=grid,
                                       **kwargs)
        return cpos, stress

    def plot_point_scalars(self, scalars, rnum=None, stitle='',
                           cmap=None, flip_scalars=None,
                           screenshot=None, cpos=None,
                           interactive=True, grid=None, add_text=True,
                           **kwargs):
        """
        Plot point scalars on active mesh.
        Parameters
        ----------
        scalars : np.ndarray
            Node scalars to plot.

        rnum : int, optional
            Cumulative result number.  Used for adding informative
            text.

        stitle : str, optional
            Title of the scalar bar.

        cmap : str, optional
            See matplotlib cmaps:
            matplotlib.org/examples/color/cmaps_reference.html

        flip_scalars : bool, optional
            Reverses the direction of the cmap.

        screenshot : str, optional
            When a filename, saves screenshot to disk.

        cpos : list, optional
            3x3 list describing the camera position.  Obtain it by
            getting the output of plot_point_scalars first.

        interactive : bool, optional
            Allows user to interact with the plot when True.  Default
            True.

        grid : pyvista.PolyData or pyvista.UnstructuredGrid, optional
            Uses self.grid by default.  When specified, uses this grid
            instead.

        add_text : bool, optional
            Adds information about the result when rnum is given.

        kwargs : keyword arguments
            Additional keyword arguments.  See help(pyvista.plot)

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

        window_size = kwargs.pop('window_size', [1024, 768])
        full_screen = kwargs.pop('full_screen', False)
        notebook = kwargs.pop('notebook', False)

        # cell_mask = np.empty(grid.n_cells, np.bool)
        # offset = grid.offset.astype(np.int32)
        # cells = grid.cells.astype(np.int32)

        # Plot off screen when not interactive
        plotter = pv.Plotter(off_screen=not(interactive), notebook=notebook)
        if 'show_axes' in kwargs:
            plotter.add_axes()

        if 'background' in kwargs:
            plotter.background_color = kwargs['background']

        plotter.add_mesh(grid, scalars=scalars, stitle=stitle,
                         cmap=cmap, flip_scalars=flip_scalars,
                         interpolate_before_map=True,
                         **kwargs)

        # NAN/missing data are white
        # plotter.renderers[0].SetUseDepthPeeling(1)  # <-- for transparency issues
        plotter.mapper.GetLookupTable().SetNanColor(1, 1, 1, 1)

        if cpos:
            plotter.camera_position = cpos

        # add table
        if add_text and rnum is not None:
            plotter.add_text(self.text_result_table(rnum), font_size=20,
                             position=[0, 0])

        if screenshot:
            cpos = plotter.plot(auto_close=False, interactive=interactive,
                                window_size=window_size,
                                full_screen=full_screen)
            if screenshot is True:
                img = plotter.screenshot()
            else:
                plotter.screenshot(screenshot)
            plotter.close()
        else:
            cpos = plotter.plot(interactive=interactive,
                                window_size=window_size,
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
                          cpos=None, screenshot=None, interactive=True,
                          node_components=None, sel_type_all=True, **kwargs):
        """
        Plots the stresses at each node in the solution.

        The order of the results corresponds to the sorted node
        numbering.  This algorithm, like ANSYS, computes the node
        stress by averaging the stress for each element at each node.
        Due to the discontinuities across elements, stresses will vary
        based on the element they are evaluated from.

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        stype : string
            Stress type from the following list: [Sx Sy Sz Sxy Syz Sxz]

        cmap : str, optional
           Cmap string.  See available matplotlib cmaps.

        flip_scalars : bool, optional
            Flip direction of cmap.

        cpos : list, optional
            List of camera position, focal point, and view up.  Plot
            first, then output the camera position and save it.

        screenshot : str, optional
            Setting this to a filename will save a screenshot of the
            plot before closing the figure.

        interactive : bool, optional
            Default True.  Setting this to False makes the plot
            generate in the background.  Useful when generating plots
            in a batch mode automatically.

        node_components : list, optional
            Accepts either a string or a list strings of node
            components to plot.  For example: 
            ``['MY_COMPONENT', 'MY_OTHER_COMPONENT]``

        sel_type_all : bool, optional
            If node_components is specified, plots those elements
            containing all nodes of the component.  Default True.

        kwargs : keyword arguments
            Additional keyword arguments.  See help(pyvista.plot)

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

        # Get nodal stress at the requested component
        nnum, stress = self.nodal_stress(rnum)
        sidx = stress_types.index(stype)
        stress = stress[:, sidx]

        if node_components:
            grid, ind = self._extract_node_components(node_components, sel_type_all)
            stress = stress[ind]
        else:
            grid = self.grid

        stitle = 'Nodal Stress\n{:s}'.format(stype.capitalize())
        return self.plot_point_scalars(stress, rnum, stitle, cmap, flip_scalars,
                                       screenshot, cpos, interactive, grid=grid,
                                       **kwargs)

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


def pol2cart(rho, phi):
    """ Convert cylindrical to cartesian """
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return x, y


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
        trans = pv.trans_from_matrix(trans)

    if points.dtype == np.float32:
        _binary_reader.affline_transform_float(points, trans)
    else:
        _binary_reader.affline_transform_double(points, trans)
