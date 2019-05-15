"""Supports reading cyclic strucutral result files from ANSYS

"""
import logging

import vtk
import numpy as np
from pyvista.common import axis_rotation
import pyvista as pv

from pyansys.rst import ResultFile, trans_to_matrix
from pyansys import (_parsefull, _binary_reader, _parser)
from pyansys._binary_reader import cells_with_any_nodes, cells_with_all_nodes


# Create logger
log = logging.getLogger(__name__)
log.setLevel('DEBUG')

np.seterr(divide='ignore', invalid='ignore')


class CyclicResult(ResultFile):
    """ Adds cyclic functionality to the result reader in pyansys """

    def __init__(self, filename):
        """ Initializes object """
        super(CyclicResult, self).__init__(filename)

        # sanity check
        if self.header['nSector'] == 1:
            raise Exception('Result is not a cyclic model')

        self._add_cyclic_properties()

    def plot(self, color='w', show_edges=True, **kwargs):
        """
        Plot full geometry.

        Parameters
        ----------
        color : string or 3 item list, optional, defaults to white
            Either a string, rgb list, or hex color string.  For
            example:
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
                ``style='surface'``
                ``style='wireframe'``
                ``style='points'``

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
        cs_cord = self.resultheader['csCord']
        if cs_cord > 1:
            matrix = self.cs_4x4(cs_cord, as_vtk_matrix=True)
            i_matrix = self.cs_4x4(cs_cord, as_vtk_matrix=True)
            i_matrix.Invert()
        else:
            matrix = vtk.vtkMatrix4x4()
            i_matrix = vtk.vtkMatrix4x4()

        off_screen = kwargs.pop('off_screen', False)
        window_size = kwargs.pop('window_size', None)
        plotter = pv.Plotter(off_screen, window_size)
        rang = 360.0 / self.n_sector
        for i in range(self.n_sector):
            actor = plotter.add_mesh(self.grid.copy(False),
                                     color=color,
                                     show_edges=show_edges, **kwargs)

            # transform to standard position, rotate about Z axis,
            # transform back
            transform = vtk.vtkTransform()
            transform.RotateZ(rang*i)
            transform.Update()
            rot_matrix = transform.GetMatrix()

            if cs_cord > 1:
                temp_matrix = vtk.vtkMatrix4x4()
                rot_matrix.Multiply4x4(i_matrix, rot_matrix, temp_matrix)
                rot_matrix.Multiply4x4(temp_matrix, matrix, rot_matrix)
                transform.SetMatrix(rot_matrix)

            actor.SetUserTransform(transform)

        cpos = kwargs.pop('cpos', None)
        if cpos is None:
            cpos = plotter.get_default_cam_pos()
            plotter.camera_position = cpos
            plotter.camera_set = False
        else:
            plotter.camera_position = cpos

        return plotter.plot()

    def _add_cyclic_properties(self):
        """
        Adds cyclic properties to result object

        Makes the assumption that all the cyclic nodes are within tol
        """
        self.n_sector = self.resultheader['nSector']

        # idenfity the sector based on number of elements in master sector
        cs_els = self.resultheader['csEls']
        mask = self.quadgrid.cell_arrays['ansys_elem_num'] <= cs_els

        self.master_cell_mask = mask
        self.mas_grid = self.grid.extract_cells(mask)

        # number of nodes in sector may not match number of nodes in geometry
        # node_mask = self.geometry['nnum'] <= self.resultheader['csNds']
        node_mask = self.nnum <= self.resultheader['csNds']
        self.mas_ind = np.nonzero(node_mask)[0]

    def cs_4x4(self, cs_cord, as_vtk_matrix=False):
        """ return a 4x4 transformation array for a given coordinate system """
        # assemble 4 x 4 matrix
        csys = self.geometry['coord systems'][cs_cord]
        trans = np.hstack((csys['transformation matrix'],
                           csys['origin'].reshape(-1, 1)))
        matrix = trans_to_matrix(trans)
        if as_vtk_matrix:
            return matrix
        else:
            return pv.trans_from_matrix(matrix)

    def nodal_solution(self, rnum, phase=0, full_rotor=False, as_complex=False,
                       in_nodal_coord_sys=False):
        """Returns the DOF solution for each node in the global
        cartesian coordinate system.

        Parameters
        ----------
        rnum : interger
            Cumulative result number.  Zero based indexing.

        phase : float, optional
            Phase to rotate sector result.

        full_rotor : bool, optional
            Expands the single sector solution for the full rotor.
            Sectors are rotated counter-clockwise about the axis of
            rotation.  Default False.

        as_complex : bool, optional
            Returns result as a complex number, otherwise as the real
            part rotated by phase.  Default False.

        in_nodal_coord_sys : bool, optional
            When True, returns results in the nodal coordinate system.
            Default False.

        Returns
        -------
        nnum : np.ndarray
            Node numbers of master sector.

        result : np.ndarray
            Result is (nnod x numdof), nnod is the number of nodes in
            a sector and numdof is the number of degrees of freedom.
            When full_rotor is True the array will be (nSector x nnod
            x numdof).

        Notes
        -----
        Somewhere between v15.0 and v18.2 ANSYS stopped writing the
        duplicate sector to the result file and instead results in
        pairs (i.e. harmonic index 1, -1).  This decreases their
        result file size since harmonic pairs contain the same
        information as the duplicate sector.

        """
        # get the nodal result
        rnum = self.parse_step_substep(rnum)
        nnum, result = super(CyclicResult, self).nodal_solution(rnum,
                                                                in_nodal_coord_sys)
        result = result[self.mas_ind]
        nnum = nnum[self.mas_ind]  # only concerned with the master sector

        # combine or expand result if not modal
        if self.resultheader['kan'] == 2:  # modal analysis
            # combine modal solution results
            hindex_table = self.resultheader['hindex']
            hindex = hindex_table[rnum]

            # if repeated mode
            last_index = hindex == int(self.resultheader['nSector']/2)
            if hindex == 0 or last_index:
                result_dup = np.zeros_like(result)
            else:  # otherwise, use the harmonic pair
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
                _, result_dup = super(CyclicResult, self).nodal_solution(rnum_dup)

            result_dup = result_dup[self.mas_ind]

            expanded_result = self.expand_cyclic_modal(result,
                                                       result_dup,
                                                       hindex, phase,
                                                       as_complex,
                                                       full_rotor)

        if self.resultheader['kan'] == 0:  # static analysis
            expanded_result = self.expand_cyclic_static(result)

        return nnum, expanded_result

    def expand_cyclic_static(self, result, tensor=False):
        """ expands cyclic static results """
        cs_cord = self.resultheader['csCord']
        if cs_cord > 1:
            matrix = self.cs_4x4(cs_cord, as_vtk_matrix=True)
            i_matrix = self.cs_4x4(cs_cord, as_vtk_matrix=True)
            i_matrix.Invert()
        else:
            matrix = vtk.vtkMatrix4x4()
            i_matrix = vtk.vtkMatrix4x4()

        shp = (self.n_sector, result.shape[0], result.shape[1])
        full_result = np.empty(shp)
        full_result[:] = result

        rang = 360.0 / self.n_sector
        for i in range(self.n_sector):
            # transform to standard position, rotate about Z axis,
            # transform back
            transform = vtk.vtkTransform()
            transform.RotateZ(rang*i)
            transform.Update()
            rot_matrix = transform.GetMatrix()

            if cs_cord > 1:
                temp_matrix = vtk.vtkMatrix4x4()
                rot_matrix.Multiply4x4(i_matrix, rot_matrix, temp_matrix)
                rot_matrix.Multiply4x4(temp_matrix, matrix, rot_matrix)

            trans = pv.trans_from_matrix(rot_matrix)
            if tensor:
                _binary_reader.tensor_arbitrary(full_result[i], trans)
            else:
                _binary_reader.affline_transform_double(full_result[i], trans)

        return full_result

    def expand_cyclic_modal(self, result, result_r, hindex, phase, as_complex,
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
        angles = np.linspace(0, 2*np.pi, self.n_sector + 1)[:-1] + phase
        for angle in angles:
            # need to rotate solution and rotate direction
            result_expanded.append(axis_rotation(result_combined, angle, deg=False,
                                                axis='z'))

        result_expanded = np.asarray(result_expanded)

        # ANSYS scales the result
        if hindex == 0 or hindex == self.n_sector/2:
            result_expanded /= self.n_sector**0.5
        else:
            result_expanded /= (self.n_sector/2)**0.5

        # adjust phase of the full result based on the harmonic index
        f_arr = np.zeros(self.n_sector)
        f_arr[hindex] = 1
        jang = np.fft.ifft(f_arr)[:self.n_sector]*self.n_sector
        cjang = jang * (np.cos(phase) - np.sin(phase) * 1j)

        result_expanded *= cjang.reshape(-1, 1, 1)
        if as_complex:
            return result_expanded
        else:
            return np.real(result_expanded)

    def expand_cyclic_modal_stress(self, result, result_r, hindex, phase, as_complex,
                                   full_rotor, scale=True):
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
        result_expanded = np.empty((self.n_sector, result.shape[0], result.shape[1]),
                                   np.complex128)
        result_expanded[:] = result_combined

        # scale
        # if scale:
        #     if hindex == 0 or hindex == self.n_sector/2:
        #         result_expanded /= self.n_sector**0.5
        #     else:
        #         result_expanded /= (self.n_sector/2)**0.5

        f_arr = np.zeros(self.n_sector)
        f_arr[hindex] = 1
        jang = np.fft.ifft(f_arr)[:self.n_sector]*self.n_sector
        cjang = jang * (np.cos(phase) - np.sin(phase) * 1j)
        full_result = np.real(result_expanded*cjang.reshape(-1, 1, 1))

        # # rotate cyclic result inplace
        # angles = np.linspace(0, 2*np.pi, self.n_sector + 1)[:-1] + phase
        # for i, angle in enumerate(angles):
        #     isnan = _binary_reader.tensor_rotate_z(result_expanded[i], angle)
        #     result_expanded[i, isnan] = np.nan

        cs_cord = self.resultheader['csCord']
        if cs_cord > 1:
            matrix = self.cs_4x4(cs_cord, as_vtk_matrix=True)
            i_matrix = self.cs_4x4(cs_cord, as_vtk_matrix=True)
            i_matrix.Invert()
        else:
            matrix = vtk.vtkMatrix4x4()
            i_matrix = vtk.vtkMatrix4x4()

        shp = (self.n_sector, result.shape[0], result.shape[1])
        full_result = np.empty(shp)
        full_result[:] = result

        rang = 360.0 / self.n_sector
        for i in range(self.n_sector):
            # transform to standard position, rotate about Z axis,
            # transform back
            transform = vtk.vtkTransform()
            transform.RotateZ(rang*i)
            transform.Update()
            rot_matrix = transform.GetMatrix()

            if cs_cord > 1:
                temp_matrix = vtk.vtkMatrix4x4()
                rot_matrix.Multiply4x4(i_matrix, rot_matrix, temp_matrix)
                rot_matrix.Multiply4x4(temp_matrix, matrix, rot_matrix)

            trans = pv.trans_from_matrix(rot_matrix)
            _binary_reader.tensor_arbitrary(full_result[i], trans)

        return full_result

    def harmonic_index_to_cumulative(self, hindex, mode):
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

    def nodal_stress(self, rnum, phase=0, as_complex=False, full_rotor=False):
        """
        Equivalent ANSYS command: PRNSOL, S

        Retrieves the component stresses for each node in the
        solution.

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

        phase : float
            Phase adjustment of the stress in degrees.

        as_complex : bool, optional
            Reports stess as a complex result.  Real and imaginary
            stresses correspond to the stress of the main and repeated
            sector.  Stress can be "rotated" using the phase
            parameter.

        full_rotor : bool, optional
            Expands the results to the full rotor when True.  Default
            False.

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
        nnum, stress = super(CyclicResult, self).nodal_stress(rnum)
        # nnum = nnum[self.mas_ind]
        # stress = stress[self.mas_ind]

        if self.resultheader['kan'] == 0:  # static result
            expanded_result = self.expand_cyclic_static(stress, tensor=True)
        elif self.resultheader['kan'] == 2:  # modal analysis
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
                _, stress_r = super(CyclicResult, self).nodal_stress(rnum_r)

            else:
                stress_r = np.zeros_like(stress)

            expanded_result = self.expand_cyclic_modal_stress(stress,
                                                              stress_r,
                                                              hindex,
                                                              phase,
                                                              as_complex,
                                                              full_rotor)
        else:
            raise Exception('Unsupported analysis type')

        return nnum, expanded_result

    def principal_nodal_stress(self, rnum, phase=0, as_complex=False,
                               full_rotor=False):
        """
        Returns principal nodal stress for a cumulative result

        """
        if as_complex and full_rotor:
            raise Exception('complex and full_rotor cannot both be True')
        
        # get component stress
        nnum, stress = self.nodal_stress(rnum, phase, as_complex, full_rotor)

        # compute principle stress
        if as_complex:
            stress_r = np.imag(stress).astype(np.float32)
            stress = np.real(stress).astype(np.float32)

            pstress, isnan = _binary_reader.ComputePrincipalStress(stress)
            pstress[isnan] = np.nan
            pstress_r, isnan = _binary_reader.ComputePrincipalStress(stress_r)
            pstress_r[isnan] = np.nan

            return nnum, pstress + 1j*pstress_r

        elif full_rotor:
            if stress.dtype != np.float32:
                stress = stress.astype(np.float32)

            # compute principle stress
            pstress = np.empty((self.n_sector, stress.shape[1], 5), np.float32)
            for i in range(stress.shape[0]):
                pstress[i], isnan = _binary_reader.ComputePrincipalStress(stress[i])
                pstress[i, isnan] = np.nan
            return nnum, pstress

        else:
            if stress.dtype != np.float32:
                stress = stress.astype(np.float32)

            pstress, isnan = _binary_reader.ComputePrincipalStress(stress)
            pstress[isnan] = np.nan
            return nnum, pstress

    def plot_nodal_solution(self, rnum, comp='norm', label='',
                            cmap=None, flip_scalars=None, cpos=None,
                            screenshot=None, interactive=True,
                            full_rotor=True, phase=0,
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

        full_rotor : bool, optional
            Expand sector solution to full rotor.

        phase : float, optional
            Phase angle of the modal result in radians.  Only valid
            when full_rotor is True.  Default 0

        node_components : list, optional
            Accepts either a string or a list strings of node
            components to plot.  For example: 
            ``['MY_COMPONENT', 'MY_OTHER_COMPONENT]``

        Returns
        -------
        cpos : list
            Camera position from vtk render window.

        """

        # Load result from file
        if not full_rotor:
            return super(CyclicResult, self).plot_nodal_solution(rnum,
                                                                 comp,
                                                                 label,
                                                                 cmap,
                                                                 flip_scalars,
                                                                 cpos,
                                                                 screenshot,
                                                                 interactive,
                                                                 node_components,
                                                                 sel_type_all,
                                                                 **kwargs)

        rnum = self.parse_step_substep(rnum)
        nnum, result = self.nodal_solution(rnum, phase, full_rotor, as_complex=False)

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
        scalars = d

        # sometimes there are less nodes in the result than in the geometry
        # npoints = self.grid.number_of_points
        # grid = self.grid
        # if nnum.size != npoints:
        #     scalars = np.empty_like((self.n_sector, npoints))
        #     scalars[:] = np.nan
        #     nnum_grid = self.grid.point_arrays['ansys_node_num']
        #     mask = np.in1d(nnum_grid, nnum)
        #     scalars[:, mask] = d
        #     d = scalars

        grid = self.mas_grid
        if node_components:
            grid, ind = self._extract_node_components(node_components,
                                                      sel_type_all)
            scalars = scalars[:, ind]

        return self.plot_point_scalars(scalars, rnum, stitle, cmap, flip_scalars,
                                       screenshot, cpos, interactive, grid,
                                       **kwargs)

    def plot_nodal_stress(self, rnum, stype, label='', cmap=None,
                          flip_scalars=None, cpos=None, screenshot=None,
                          interactive=True, full_rotor=True, phase=0,
                          node_components=None, sel_type_all=True,
                          **kwargs):
        """
        Plots a nodal result.

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        stype : string
            Stress type from the following list: [Sx Sy Sz Sxy Syz Sxz]

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

        full_rotor : bool, optional
            Expand sector solution to full rotor.

        phase : float, optional
            Phase angle of the modal result in radians.  Only valid
            when full_rotor is True.  Default 0

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
        # if not full_rotor:  # Plot sector
        #     super(CyclicResult, self).plot_nodal_stress(rnum,
        #                                                 stype,
        #                                                 cmap,
        #                                                 flip_scalars,
        #                                                 cpos,
        #                                                 screenshot,
        #                                                 interactive,node_components,
        #                                                 sel_type_all,
        #                                                 **kwargs)

        rnum = self.parse_step_substep(rnum)
        stress_types = ['sx', 'sy', 'sz', 'sxy', 'syz', 'sxz']
        stype = stype.lower()
        if stype not in stress_types:
            raise Exception('Stress type not in: \n' + str(stress_types))

        _, stress = self.nodal_stress(rnum, phase, False, full_rotor=True)
        stress = stress[:, self.mas_ind]
        sidx = stress_types.index(stype)
        scalars = stress[:, :, sidx]
        grid = self.mas_grid

        if node_components:
            grid, ind = self._extract_node_components(node_components,
                                                      sel_type_all)
            scalars = scalars[ind]

        # breakpoint()
        # scalars[np.isnan(scalars)] = 0
        stitle = 'Cyclic Rotor\nNodal Stress\n%s\n' % stype.capitalize()
        if full_rotor:
            return self.plot_point_scalars(scalars, rnum, stitle, cmap, flip_scalars,
                                           screenshot, cpos, interactive, grid,
                                           **kwargs)
        else:
            return super(CyclicResult,
                         self).plot_point_scalars(scalars[0],
                                                  rnum, stitle, cmap,
                                                  flip_scalars, screenshot,
                                                  cpos, interactive, grid,
                                                  **kwargs)


    def plot_principal_nodal_stress(self, rnum, stype, cmap=None,
                                    flip_scalars=None, cpos=None,
                                    screenshot=None, interactive=True,
                                    full_rotor=True, phase=0,
                                    node_components=None,
                                    sel_type_all=True, **kwargs):
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

        full_rotor : bool, optional
            Expand sector solution to full rotor.

        phase : float, optional
            Phase angle of the modal result in radians.  Only valid
            when full_rotor is True.  Default 0

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
        stype = stype.upper()
        if not full_rotor:  # Plot sector
            return super(CyclicResult, self).plot_principal_nodal_stress(rnum, stype)

        # check inputs
        stress_types = ['S1', 'S2', 'S3', 'SINT', 'SEQV']
        if stype not in stress_types:
            raise Exception('Stress type not in \n' + str(stress_types))
        sidx = stress_types.index(stype)
        rnum = self.parse_step_substep(rnum)

        # full rotor component stress
        _, pstress = self.principal_nodal_stress(rnum, phase, full_rotor=True)
        pstress = pstress[:, self.mas_ind]

        scalars = pstress[:, :, sidx]
        stitle = 'Cyclic Rotor\nPrincipal Nodal Stress\n' +\
                 '%s\n' % stype.capitalize()
        grid = self.mas_grid

        if node_components:
            grid, ind = self._extract_node_components(node_components,
                                                      sel_type_all, self.mas_grid)
            scalars = scalars[ind]

        return self.plot_point_scalars(scalars, rnum, stitle, cmap,
                                       flip_scalars, screenshot, cpos,
                                       interactive, grid, **kwargs)

    def animate_nodal_solution(self, rnum, comp='norm', max_disp=0.1,
                               nangles=180, show_phase=True,
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
            See help(pyvista.plot) for additional keyword arguments.

        """
        # normalize nodal solution
        nnum, complex_disp = self.nodal_solution(rnum, as_complex=True,
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

        full_rotor = self._gen_full_rotor()
        orig_pt = full_rotor.points

        if show_result_info:
            result_info = self.text_result_table(rnum)

        plotter = pv.Plotter(off_screen=not interactive)
        plotter.add_mesh(full_rotor.copy(), scalars=np.real(scalars),
                      interpolate_before_map=interpolate_before_map, **kwargs)
        plotter.update_coordinates(orig_pt + np.real(complex_disp), render=False)

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
                padj = 1*np.cos(angle) - 1j*np.sin(angle)
                complex_disp_adj = np.real(complex_disp*padj)

                if axis is not None:
                    scalars = complex_disp_adj[:, axis]
                else:
                    scalars = (complex_disp_adj*complex_disp_adj).sum(1)**0.5

                plotter.update_scalars(scalars, render=False)
                plotter.update_coordinates(orig_pt + complex_disp_adj,
                                        render=False)

                if show_phase:
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

    def _gen_full_rotor(self):
        """ Create full rotor vtk unstructured grid """
        grid = self.mas_grid.copy()
        # transform to standard coordinate system
        cs_cord = self.resultheader['csCord']
        if cs_cord > 1:
            matrix = self.cs_4x4(cs_cord, as_vtk_matrix=True)
            grid.transform(matrix)

        vtkappend = vtk.vtkAppendFilter()
        rang = 360.0 / self.n_sector
        for i in range(self.n_sector):
            # Transform mesh
            sector = grid.copy()
            sector.rotate_z(rang * i)
            vtkappend.AddInputData(sector)

        vtkappend.Update()
        full_rotor = pv.wrap(vtkappend.GetOutput())

        if cs_cord > 1:
            matrix.Invert()
            full_rotor.transform(matrix)

        return full_rotor

    def plot_point_scalars(self, scalars, rnum=None, stitle='', cmap=None,
                           flip_scalars=None, screenshot=None, cpos=None,
                           interactive=True, grid=None, add_text=True, **kwargs):
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
            grid = self.mas_grid

        # make cmap match default ansys
        if cmap is None and flip_scalars is None:
            flip_scalars = False

        window_size = kwargs.pop('window_size', None)
        full_screen = kwargs.pop('full_screen', False)
        off_screen = not interactive

        # Plot off screen when not interactive
        plotter = pv.Plotter(off_screen=not(interactive))
        if 'show_axes' in kwargs:
            plotter.add_axes()
        # plotter.add_axes_at_origin()
        # breakpoint()

        if 'background' in kwargs:
            plotter.background_color = kwargs['background']

        rng = [np.nanmin(scalars), np.nanmax(scalars)]

        cs_cord = self.resultheader['csCord']
        if cs_cord > 1:
            matrix = self.cs_4x4(cs_cord, as_vtk_matrix=True)
            i_matrix = self.cs_4x4(cs_cord, as_vtk_matrix=True)
            i_matrix.Invert()
        else:
            matrix = vtk.vtkMatrix4x4()
            i_matrix = vtk.vtkMatrix4x4()

        rang = 360.0 / self.n_sector
        for i in range(self.n_sector):

            actor = plotter.add_mesh(grid.copy(False),
                                     scalars=scalars[i], stitle=stitle,
                                     cmap=cmap, flip_scalars=flip_scalars,
                                     interpolate_before_map=True, rng=rng,
                                     **kwargs)

            # for transparency issues
            # plotter.renderers[0].SetUseDepthPeeling(1)

            # NAN/missing data are white
            plotter.mapper.GetLookupTable().SetNanColor(1, 1, 1, 1)

            # transform to standard position, rotate about Z axis,
            # transform back
            transform = vtk.vtkTransform()
            transform.RotateZ(rang*i)
            transform.Update()
            rot_matrix = transform.GetMatrix()

            if cs_cord > 1:
                temp_matrix = vtk.vtkMatrix4x4()
                rot_matrix.Multiply4x4(i_matrix, rot_matrix, temp_matrix)
                rot_matrix.Multiply4x4(temp_matrix, matrix, rot_matrix)
                transform.SetMatrix(rot_matrix)

            actor.SetUserTransform(transform)

        if cpos:
            plotter.camera_position = cpos

        # add table
        if add_text and rnum is not None:
            plotter.add_text(self.text_result_table(rnum), font_size=20,
                             position=[0, 0])

        if screenshot:
            cpos = plotter.show(auto_close=False, interactive=interactive,
                                window_size=window_size,
                                full_screen=full_screen)
            if screenshot is True:
                img = plotter.screenshot()
            else:
                plotter.screenshot(screenshot)
            plotter.close()
        else:
            cpos = plotter.plot(interactive=interactive, window_size=window_size,
                                full_screen=full_screen)

        if screenshot is True:
            return cpos, img
        else:
            return cpos
