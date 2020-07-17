"""Supports reading cyclic structural result files from ANSYS"""
from functools import wraps

from vtk import vtkMatrix4x4, vtkTransform, vtkAppendFilter
import numpy as np
from pyvista.core.common import axis_rotation
import pyvista as pv

from pyansys.common import STRESS_TYPES, PRINCIPAL_STRESS_TYPES
from pyansys.rst import ResultFile, trans_to_matrix, check_comp
from pyansys import _binary_reader

np.seterr(divide='ignore', invalid='ignore')


class CyclicResult(ResultFile):
    """Adds cyclic functionality to the result class"""

    def __init__(self, filename):
        """ Initializes object """
        super().__init__(filename)

        # sanity check
        if self.n_sector == 1:
            raise RuntimeError('Result is not a cyclic model')

        self._animating = False
        self._add_cyclic_properties()
        self._positive_cyclic_dir = False
        self._rotor_cache = None

    @property
    def positive_cyclic_dir(self):
        """Rotor results are default anit-clockwise.  Set this to
        `True` if cyclic results to not look correct.
        """
        return self._positive_cyclic_dir

    @positive_cyclic_dir.setter
    def positive_cyclic_dir(self, value):
        self._positive_cyclic_dir = bool(value)

    def plot(self, color='w', show_edges=True, **kwargs):
        """Plot the full rotor geometry.

        Parameters
        ----------
        color : string or 3 item list, optional, defaults to white
            Either a string, rgb list, or hex color string.  For
            example:

            - ``color='white'``
            - ``color='w'``
            - ``color=[1, 1, 1]``
            - ``color='#FFFFFF'``

            Color will be overridden when scalars are input.

        show_edges : bool, optional
            Shows the edges of a mesh.  Does not apply to a wireframe
            representation.

        style : string, optional
            Visualization style of the vtk mesh.  One for the
            following:

            - ``style='surface'``
            - ``style='wireframe'``
            - ``style='points'``

            Defaults to ``'surface'``

        off_screen : bool
            Plots off screen when True.  Helpful for saving
            screenshots without a window popping up.

        full_screen : bool, optional
            Opens window in full screen.  When enabled, ignores
            window_size.  Default False.

        screenshot : str or bool, optional
            Saves screenshot to file when enabled.  See:
            ``help(pyvista.Plotter.screenshot)``.  Default disabled.

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
        cs_cord = self._resultheader['csCord']
        if cs_cord > 1:
            matrix = self.cs_4x4(cs_cord, as_vtk_matrix=True)
            i_matrix = self.cs_4x4(cs_cord, as_vtk_matrix=True)
            i_matrix.Invert()
        else:
            matrix = vtkMatrix4x4()
            i_matrix = vtkMatrix4x4()

        off_screen = kwargs.pop('off_screen', None)
        window_size = kwargs.pop('window_size', None)
        plotter = pv.Plotter(off_screen, window_size)
        rang = 360.0 / self.n_sector
        for i in range(self.n_sector):
            actor = plotter.add_mesh(self.grid.copy(False),
                                     color=color,
                                     show_edges=show_edges, **kwargs)

            # transform to standard position, rotate about Z axis,
            # transform back
            transform = vtkTransform()
            transform.RotateZ(rang*i)
            transform.Update()
            rot_matrix = transform.GetMatrix()

            if cs_cord > 1:
                temp_matrix = vtkMatrix4x4()
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

        return plotter.show()

    def _add_cyclic_properties(self):
        """Add cyclic properties"""

        # idenfity the sector based on number of elements in master sector
        cs_els = self._resultheader['csEls']
        mask = self.quadgrid.cell_arrays['ansys_elem_num'] <= cs_els

        self.master_cell_mask = mask
        self._mas_grid = self.grid.extract_cells(mask)

        # NOTE: number of nodes in sector may not match number of
        # nodes in geometry
        node_mask = self._neqv[self._sidx] <= self._resultheader['csNds']
        self._mas_ind = np.nonzero(node_mask)[0]
        self._dup_ind = np.nonzero(~node_mask)[0]

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
        nnum : numpy.ndarray
            Node numbers of master sector.

        result : numpy.ndarray
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
        full_nnum, full_result = super().nodal_solution(rnum,
                                                        in_nodal_coord_sys)

        # only concerned with the master sector
        result = full_result[self._mas_ind]
        nnum = full_nnum[self._mas_ind]

        # combine or expand result if not modal
        if self._resultheader['kan'] == 2:  # modal analysis
            # combine modal solution results
            hindex_table = self._resultheader['hindex']
            hindex = hindex_table[rnum]

            # if repeated mode
            # last_index = hindex == int(self._resultheader['nSector']/2)
            last_index = False
            if hindex == 0 or last_index:
                result_dup = np.zeros_like(result)
            else:  # otherwise, use the harmonic pair
                hmask = np.abs(hindex_table) == abs(hindex)
                hmatch = np.nonzero(hmask)[0]

                if hmatch.size % 2:
                    # combine the matching sector
                    result_dup = full_result[self._dup_ind]
                else:
                    match_loc = np.where(hmatch == rnum)[0][0]

                    if match_loc % 2:
                        rnum_dup = rnum - 1
                    else:
                        rnum_dup = rnum + 1

                    # get repeated result and combine
                    _, full_result_dup = super().nodal_solution(rnum_dup)
                    result_dup = full_result_dup[self._mas_ind]

            expanded_result = self._expand_cyclic_modal(result,
                                                        result_dup,
                                                        hindex, phase,
                                                        as_complex,
                                                        full_rotor)

        if self._resultheader['kan'] == 0:  # static analysis
            expanded_result = self._expand_cyclic_static(result)

        return nnum, expanded_result

    @wraps(nodal_solution)
    def nodal_displacement(self, *args, **kwargs):
        """wraps nodal_solution"""
        return self.nodal_solution(*args, **kwargs)

    def _expand_cyclic_static(self, result, tensor=False, stress=True):
        """ expands cyclic static results """
        cs_cord = self._resultheader['csCord']
        if cs_cord > 1:
            matrix = self.cs_4x4(cs_cord, as_vtk_matrix=True)
            i_matrix = self.cs_4x4(cs_cord, as_vtk_matrix=True)
            i_matrix.Invert()
        else:
            matrix = vtkMatrix4x4()
            i_matrix = vtkMatrix4x4()

        shp = (self.n_sector, result.shape[0], result.shape[1])
        full_result = np.empty(shp)
        full_result[:] = result

        rang = 360.0 / self.n_sector
        for i in range(self.n_sector):
            # transform to standard position, rotate about Z axis,
            # transform back
            transform = vtkTransform()
            transform.RotateZ(rang*i)
            transform.Update()
            rot_matrix = transform.GetMatrix()

            if cs_cord > 1:
                temp_matrix = vtkMatrix4x4()
                rot_matrix.Multiply4x4(i_matrix, rot_matrix, temp_matrix)
                rot_matrix.Multiply4x4(temp_matrix, matrix, rot_matrix)

            trans = pv.trans_from_matrix(rot_matrix)
            if tensor:
                if stress:
                    _binary_reader.tensor_arbitrary(full_result[i], trans)
                else:
                    _binary_reader.tensor_strain_arbitrary(full_result[i], trans)
            else:
                _binary_reader.affline_transform(full_result[i], trans)

        return full_result

    def _expand_cyclic_modal(self, result, result_r, hindex, phase, as_complex,
                             full_rotor):
        """ Combines repeated results from ANSYS """
        if as_complex or full_rotor:
            # Matches ansys direction
            if self._positive_cyclic_dir:
                result_combined = result + result_r*1j
            else:
                result_combined = result - result_r*1j
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
            result_expanded.append(axis_rotation(result_combined,
                                                 angle, deg=False,
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

    def _expand_cyclic_modal_tensor(self, result, result_r, hindex,
                                    phase, as_complex, full_rotor, stress=True):
        """Combines repeated results from ANSYS and optionally
        duplicates/rotates it around the axis of rotation"""
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

        f_arr = np.zeros(self.n_sector)
        f_arr[hindex] = 1
        jang = np.fft.ifft(f_arr)[:self.n_sector]*self.n_sector
        cjang = jang * (np.cos(phase) - np.sin(phase) * 1j)
        full_result = np.real(result_expanded*cjang.reshape(-1, 1, 1))

        cs_cord = self._resultheader['csCord']
        if cs_cord > 1:
            matrix = self.cs_4x4(cs_cord, as_vtk_matrix=True)
            i_matrix = self.cs_4x4(cs_cord, as_vtk_matrix=True)
            i_matrix.Invert()
        else:
            matrix = vtkMatrix4x4()
            i_matrix = vtkMatrix4x4()

        shp = (self.n_sector, result.shape[0], result.shape[1])
        full_result = np.empty(shp)
        full_result[:] = result

        rang = 360.0 / self.n_sector
        for i in range(self.n_sector):
            # transform to standard position, rotate about Z axis,
            # transform back
            transform = vtkTransform()
            transform.RotateZ(rang*i)
            transform.Update()
            rot_matrix = transform.GetMatrix()

            if cs_cord > 1:
                temp_matrix = vtkMatrix4x4()
                rot_matrix.Multiply4x4(i_matrix, rot_matrix, temp_matrix)
                rot_matrix.Multiply4x4(temp_matrix, matrix, rot_matrix)

            trans = pv.trans_from_matrix(rot_matrix)
            if stress:  # transformation different for strain/stress
                _binary_reader.tensor_arbitrary(full_result[i], trans)
            else:
                _binary_reader.tensor_strain_arbitrary(full_result[i], trans)

        return full_result

    def harmonic_index_to_cumulative(self, hindex, mode):
        """Converts a harmonic index and a 0 index mode number to a
        cumulative result index.

        Harmonic indices are stored as positive and negative pairs for
        modes other than 0 and N/nsectors.

        Parameters
        ----------
        hindex : int
            Harmonic index.  Must be less than or equal to nsectors/2.
            May be positive or negative

        mode : int
            Mode number.  0 based indexing.  Access mode pairs by with
            a negative/positive harmonic index.

        Returns
        -------
        rnum : int
            Cumulative index number.  Zero based indexing.

        """
        hindex_table = self._resultheader['hindex']
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
        """Unique modes for cyclic results"""
        hindex_table = self._resultheader['hindex']
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

    @property
    def harmonic_indices(self):
        """Harmonic indices of the result file.

        Harmonic index is simply the Nodal Diameter of the mode.  This
        is defined as the number of complete sine waves that pass
        through the circumference.

        Examples
        --------
        >>> rst = pyansys.read_binary('file.rst')
        >>> rst.harmonic_indices
        array([ 0,  0,  0,  0,  0,  0, -1,  1, -1,  1,  1, -1,
               -2,  2, -2,  2, -2,  2,  3,  3,  3,  3,  3,  3], dtype=int32)
        """
        return self._resultheader['hindex']

    def nodal_stress(self, rnum, phase=0, as_complex=False, full_rotor=False):
        """Retrieves the component stresses for each node in the
        solution.

        The order of the results corresponds to the sorted node
        numbering.

        Computes the nodal stress by averaging the stress for each
        element at each node.  Due to the discontinuities across
        elements, stresses will vary based on the element they are
        evaluated from.

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        phase : float
            Phase adjustment of the stress in degrees.

        as_complex : bool, optional
            Reports stress as a complex result.  Real and imaginary
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

        Examples
        --------
        >>> import pyansys
        >>> rst = pyansys.read_binary('file.rst')
        >>> nnum, stress = rst.nodal_stress(0)

        Notes
        -----
        Nodes without a stress value will be NAN.

        """
        rnum = self.parse_step_substep(rnum)
        nnum, stress = super().nodal_stress(rnum)
        nnum = nnum[self._mas_ind]
        stress = stress[self._mas_ind]

        if self._resultheader['kan'] == 0:  # static result
            expanded_result = self._expand_cyclic_static(stress, tensor=True)
        elif self._resultheader['kan'] == 2:  # modal analysis
            # combine modal solution results
            hindex_table = self._resultheader['hindex']
            hindex = hindex_table[rnum]

            # if repeated mode
            if hindex != 0 and -hindex in hindex_table:
                if hindex < 0:
                    rnum_r = rnum - 1
                else:
                    rnum_r = rnum + 1

                # get repeated result and combine
                _, stress_r = super().nodal_stress(rnum_r)

            else:
                stress_r = np.zeros_like(stress)

            expanded_result = self._expand_cyclic_modal_tensor(stress,
                                                               stress_r,
                                                               hindex,
                                                               phase,
                                                               as_complex,
                                                               full_rotor)
        else:
            raise RuntimeError('Unsupported analysis type')

        return nnum, expanded_result

    def nodal_elastic_strain(self, rnum, phase=0, as_complex=False, full_rotor=False):
        """Nodal component elastic strains.  This record contains
        strains in the order X, Y, Z, XY, YZ, XZ, EQV.

        Elastic strains can be can be nodal values extrapolated from
        the integration points or values at the integration points
        moved to the nodes.

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        phase : float
            Phase adjustment of the stress in degrees.

        as_complex : bool, optional
            Reports stress as a complex result.  Real and imaginary
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

        elastic_strain : numpy.ndarray
            Nodal component elastic strains.  Array is in the order
            X, Y, Z, XY, YZ, XZ, EEL.

        Examples
        --------
        Load the nodal elastic strain for the first result.

        >>> import pyansys
        >>> rst = pyansys.read_binary('file.rst')
        >>> nnum, elastic_strain = rst.nodal_stress(0)

        Notes
        -----
        Nodes without a strain will be NAN.

        """
        rnum = self.parse_step_substep(rnum)
        nnum, stress = super().nodal_elastic_strain(rnum)
        nnum = nnum[self._mas_ind]
        stress = stress[self._mas_ind]

        if self._resultheader['kan'] == 0:  # static result
            expanded_result = self._expand_cyclic_static(stress, tensor=True,
                                                        stress=False)
        elif self._resultheader['kan'] == 2:  # modal analysis
            # combine modal solution results
            hindex_table = self._resultheader['hindex']
            hindex = hindex_table[rnum]

            # if repeated mode
            if hindex != 0 and -hindex in hindex_table:
                if hindex < 0:
                    rnum_r = rnum - 1
                else:
                    rnum_r = rnum + 1

                # get repeated result and combine
                _, stress_r = super().nodal_elastic_strain(rnum_r)

            else:
                stress_r = np.zeros_like(stress)

            expanded_result = self._expand_cyclic_modal_tensor(stress,
                                                               stress_r,
                                                               hindex,
                                                               phase,
                                                               as_complex,
                                                               full_rotor,
                                                               stress=False)
        else:
            raise RuntimeError('Unsupported analysis type')

        return nnum, expanded_result

    def plot_nodal_elastic_strain(self, rnum,
                                  comp=None, phase=0,
                                  full_rotor=True,
                                  show_displacement=False,
                                  displacement_factor=1,
                                  node_components=None,
                                  element_components=None,
                                  sel_type_all=True,
                                  add_text=True,
                                  overlay_wireframe=False,
                                  **kwargs):
        """Plot nodal elastic strain.

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        comp : str, optional
            Elastic strain component to display.  Available options:
            - ``"X"``
            - ``"Y"``
            - ``"Z"``
            - ``"XY"``
            - ``"YZ"``
            - ``"XZ"``
            - ``"EQV"``

        phase : float, optional
            Phase angle of the modal result in radians.  Only valid
            when full_rotor is True.  Default 0

        full_rotor : bool, optional
            Expand the sector solution to the full rotor.

        show_displacement : bool, optional
            Deforms mesh according to the result.

        displacement_factor : float, optional
            Increases or decreases displacement by a factor.

        node_components : list, optional
            Accepts either a string or a list strings of node
            components to plot.  For example:
            ``['MY_COMPONENT', 'MY_OTHER_COMPONENT]``

        element_components : list, optional
            Accepts either a string or a list strings of element
            components to plot.  For example:
            ``['MY_COMPONENT', 'MY_OTHER_COMPONENT]``

        sel_type_all : bool, optional
            If node_components is specified, plots those elements
            containing all nodes of the component.  Default True.

        Returns
        -------
        cpos : list
            Camera position from vtk render window.

        Examples
        --------
        Plot nodal elastic strain for an academic rotor

        >>> import pyansys
        >>> result = pyansys.download_academic_rotor()
        >>> result.plot_nodal_elastic_strain(0)

        """
        idx = check_comp(STRESS_TYPES, comp)
        _, strain = self.nodal_elastic_strain(rnum, phase, False, full_rotor)
        scalars = strain[:, :, idx]

        kwargs.setdefault('stitle', '%s Nodal Elastic Strain' % comp)
        kwargs['node_components'] = node_components
        kwargs['element_components'] = element_components
        kwargs['show_displacement'] = show_displacement
        kwargs['displacement_factor'] = displacement_factor
        kwargs['overlay_wireframe'] = overlay_wireframe
        kwargs['add_text'] = add_text
        kwargs['node_components'] = node_components
        kwargs['element_components'] = element_components
        kwargs['sel_type_all'] = sel_type_all
        kwargs['phase'] = phase
        return self._plot_cyclic_point_scalars(scalars, rnum, **kwargs)

    def principal_nodal_stress(self, rnum, phase=0, as_complex=False,
                               full_rotor=False):
        """Computes the principal component stresses for each node in
        the solution.

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        phase : float
            Phase adjustment of the stress in degrees.

        as_complex : bool, optional
            Returns result as a complex number, otherwise as the real
            part rotated by phase.  Default False.

        full_rotor : bool, optional
            Expand sector solution to full rotor.

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
        if as_complex and full_rotor:
            raise ValueError('complex and full_rotor cannot both be True')

        # get component stress
        nnum, stress = self.nodal_stress(rnum, phase, as_complex, full_rotor)

        # compute principle stress
        if as_complex:
            stress_r = np.imag(stress)
            stress = np.real(stress)

            pstress, isnan = _binary_reader.compute_principal_stress(stress)
            pstress[isnan] = np.nan
            pstress_r, isnan = _binary_reader.compute_principal_stress(stress_r)
            pstress_r[isnan] = np.nan

            return nnum, pstress + 1j*pstress_r

        elif full_rotor:
            # compute principle stress for each sector
            pstress = np.empty((self.n_sector, stress.shape[1], 5), np.float64)
            for i in range(stress.shape[0]):
                pstress[i], isnan = _binary_reader.compute_principal_stress(stress[i])
                pstress[i, isnan] = np.nan
            return nnum, pstress

        else:
            pstress, isnan = _binary_reader.compute_principal_stress(stress)
            pstress[isnan] = np.nan
            return nnum, pstress

    def plot_nodal_solution(self, rnum, comp='norm',
                            phase=0,
                            full_rotor=True,
                            show_displacement=False,
                            displacement_factor=1.0,
                            node_components=None,
                            element_components=None,
                            overlay_wireframe=False,
                            add_text=True,
                            sel_type_all=True,
                            **kwargs):
        """Plot the nodal solution (generally displacement).

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        comp : str, optional
            Display component to display.  Options are 'x', 'y', 'z',
            and 'norm', corresponding to the x directin, y direction,
            z direction, and the normalized direction:
            ``(x**2 + y**2 + z**2)**0.5``

        full_rotor : bool, optional
            Expand sector solution to full rotor.

        phase : float, optional
            Phase angle of the modal result in radians.  Only valid
            when full_rotor is True.  Default 0

        node_components : list, optional
            Accepts either a string or a list strings of node
            components to plot.  For example:
            ``['MY_COMPONENT', 'MY_OTHER_COMPONENT]``

        element_components : list, optional
            Accepts either a string or a list strings of element
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
        if not full_rotor:
            return super().plot_nodal_solution(rnum,
                                               comp,
                                               show_displacement=show_displacement,
                                               displacement_factor=displacement_factor,
                                               node_components=node_components,
                                               element_components=element_components,
                                               sel_type_all=sel_type_all,
                                               **kwargs)

        rnum = self.parse_step_substep(rnum)
        _, result = self.nodal_solution(rnum, phase, full_rotor, as_complex=False)

        # Process result
        label = 'Cyclic Rotor\nDisplacement'
        if comp == 'x':
            scalars = result[:, :, 0]
            stitle = 'X {:s}\n'.format(label)
        elif comp == 'y':
            scalars = result[:, :, 1]
            stitle = 'Y {:s}\n'.format(label)
        elif comp == 'z':
            scalars = result[:, :, 2]
            stitle = 'Z {:s}\n'.format(label)
        else:
            # Normalize displacement
            scalars = (result*result).sum(2)**0.5
            stitle = 'Normalized\n%s\n' % label
        kwargs.setdefault('stitle', stitle)

        kwargs['node_components'] = node_components
        kwargs['element_components'] = element_components
        kwargs['show_displacement'] = show_displacement
        kwargs['displacement_factor'] = displacement_factor
        kwargs['overlay_wireframe'] = overlay_wireframe
        kwargs['add_text'] = add_text
        kwargs['node_components'] = node_components
        kwargs['element_components'] = element_components
        kwargs['sel_type_all'] = sel_type_all
        kwargs['phase'] = phase
        return self._plot_cyclic_point_scalars(scalars, rnum, **kwargs)

    def plot_nodal_stress(self, rnum,
                          comp=None,
                          phase=0,
                          full_rotor=True,
                          show_displacement=False,
                          displacement_factor=1,
                          node_components=None,
                          element_components=None,
                          overlay_wireframe=False,
                          add_text=True,
                          sel_type_all=True, **kwargs):
        """Plot nodal stress of a given component

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        comp : str, optional
            Stress component to display.  Available options:
            - ``"X"``
            - ``"Y"``
            - ``"Z"``
            - ``"XY"``
            - ``"YZ"``
            - ``"XZ"``

        phase : float, optional
            Phase angle of the modal result in radians.  Only valid
            when full_rotor is True.  Default 0

        full_rotor : bool, optional
            Expand the sector solution to the full rotor.

        show_displacement : bool, optional
            Deforms mesh according to the result.

        displacement_factor : float, optional
            Increases or decreases displacement by a factor.

        node_components : list, optional
            Accepts either a string or a list strings of node
            components to plot.  For example:
            ``['MY_COMPONENT', 'MY_OTHER_COMPONENT]``

        element_components : list, optional
            Accepts either a string or a list strings of element
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
        if not full_rotor:
            super().plot_nodal_stress(rnum, comp,
                                      show_displacement,
                                      displacement_factor,
                                      node_components,
                                      element_components,
                                      sel_type_all, **kwargs)

        idx = check_comp(STRESS_TYPES, comp)
        _, stress = self.nodal_stress(rnum, phase, False, full_rotor=True)
        scalars = stress[:, :, idx]

        kwargs.setdefault('stitle', 'Cyclic Rotor\nNodal Stress\n%s\n' % comp)
        kwargs['node_components'] = node_components
        kwargs['element_components'] = element_components
        kwargs['show_displacement'] = show_displacement
        kwargs['displacement_factor'] = displacement_factor
        kwargs['overlay_wireframe'] = overlay_wireframe
        kwargs['add_text'] = add_text
        kwargs['node_components'] = node_components
        kwargs['element_components'] = element_components
        kwargs['sel_type_all'] = sel_type_all
        kwargs['phase'] = phase
        return self._plot_cyclic_point_scalars(scalars, rnum, **kwargs)

    def plot_principal_nodal_stress(self, rnum,
                                    comp=None,
                                    phase=0,
                                    full_rotor=True,
                                    show_displacement=False,
                                    displacement_factor=1,
                                    node_components=None,
                                    element_components=None,
                                    sel_type_all=True,
                                    add_text=True,
                                    overlay_wireframe=False,
                                    **kwargs):
        """Plot the nodal principal stress.

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        comp : string
            Stress component to plot.  S1, S2, S3 principal stresses, SINT
            stress intensity, and SEQV equivalent stress.

            Stress type must be a string from the following list:
            ``['S1', 'S2', 'S3', 'SINT', 'SEQV']``

        phase : float, optional
            Phase angle of the modal result in radians.  Only valid
            when full_rotor is True.  Default 0

        full_rotor : bool, optional
            Expand sector solution to full rotor.

        show_displacement : bool, optional
            Deforms mesh according to the result.

        displacement_factor : float, optional
            Increases or decreases displacement by a factor.

        node_components : list, optional
            Accepts either a string or a list strings of node
            components to plot.  For example:
            ``['MY_COMPONENT', 'MY_OTHER_COMPONENT]``

        sel_type_all : bool, optional
            If node_components is specified, plots those elements
            containing all nodes of the component.  Default True.

        kwargs : keyword arguments
            Additional keyword arguments.  See ``help(pyvista.plot)``

        Returns
        -------
        cpos : list
            VTK camera position.

        """
        if not full_rotor:
            return super().plot_principal_nodal_stress(rnum, comp,
                                                       show_displacement,
                                                       displacement_factor,
                                                       node_components,
                                                       element_components,
                                                       sel_type_all, **kwargs)

        # get the correct component of the principal stress for the rotor
        idx = check_comp(PRINCIPAL_STRESS_TYPES, comp)
        _, pstress = self.principal_nodal_stress(rnum, phase, full_rotor=True)
        scalars = pstress[:, :, idx]

        kwargs.setdefault('stitle',
                          'Cyclic Rotor\nPrincipal Nodal Stress\n%s\n' % comp)
        kwargs['node_components'] = node_components
        kwargs['element_components'] = element_components
        kwargs['show_displacement'] = show_displacement
        kwargs['displacement_factor'] = displacement_factor
        kwargs['overlay_wireframe'] = overlay_wireframe
        kwargs['add_text'] = add_text
        kwargs['node_components'] = node_components
        kwargs['element_components'] = element_components
        kwargs['sel_type_all'] = sel_type_all
        kwargs['phase'] = phase
        self._plot_cyclic_point_scalars(scalars, rnum, **kwargs)

    def nodal_temperature(self, rnum, full_rotor=True):
        """Retrieves the temperature for each node in the
        solution.

        The order of the results corresponds to the sorted node
        numbering.

        Equivalent MAPDL commands:
        PRNSOL, TEMP
        PRNSOL, BFE

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        full_rotor : bool, optional
            Expand sector solution to full rotor.

        Returns
        -------
        nnum : numpy.ndarray
            Node numbers of the result.

        temperature : numpy.ndarray
            Tempature at each node.

        Examples
        --------
        >>> import pyansys
        >>> rst = pyansys.read_binary('file.rst')
        >>> nnum, stress = rst.nodal_temperature(0)

        Notes
        -----
        If there are multiple material types for each node, this will
        output the last material value. 
        """
        nnum, temp = super()._nodal_result(rnum, 'EPT')
        nnum = nnum[self._mas_ind]
        temp = temp[self._mas_ind]
        if not full_rotor:  # return only the master sector
            return nnum, temp.ravel()

        # otherwise, duplicate and repeat as temperature is constant across sectors
        return nnum, temp.T.repeat(self.n_sector, axis=0)

    def plot_nodal_temperature(self, rnum,
                               phase=0,
                               full_rotor=True,
                               show_displacement=False,
                               displacement_factor=1.0,
                               node_components=None,
                               overlay_wireframe=False,
                               add_text=True,
                               element_components=None,
                               sel_type_all=True,
                               **kwargs):
        """Plot the nodal temperature.

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        full_rotor : bool, optional
            Expand the sector solution and plot the full rotor.

        phase : float, optional
            Phase angle of the modal result in radians.  Only valid
            when full_rotor is True.  Default 0

        node_components : list, optional
            Accepts either a string or a list strings of node
            components to plot.  For example:
            ``['MY_COMPONENT', 'MY_OTHER_COMPONENT]``

        element_components : list, optional
            Accepts either a string or a list strings of element
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
        if not full_rotor:
            return super().plot_nodal_temperature(rnum,
                                                  show_displacement=show_displacement,
                                                  displacement_factor=displacement_factor,
                                                  node_components=node_components,
                                                  element_components=element_components,
                                                  sel_type_all=sel_type_all,
                                                  **kwargs)

        _, temp = self.nodal_temperature(rnum, True)

        kwargs['node_components'] = node_components
        kwargs['element_components'] = element_components
        kwargs['show_displacement'] = show_displacement
        kwargs['displacement_factor'] = displacement_factor
        kwargs['overlay_wireframe'] = overlay_wireframe
        kwargs['add_text'] = add_text
        kwargs['node_components'] = node_components
        kwargs['element_components'] = element_components
        kwargs['sel_type_all'] = sel_type_all
        kwargs['phase'] = phase
        return self._plot_cyclic_point_scalars(temp, rnum, **kwargs)

    def animate_nodal_solution(self, rnum, comp='norm', max_disp=0.1,
                               nangles=180, show_phase=True,
                               add_text=True, loop=True,
                               interpolate_before_map=True, cpos=None,
                               movie_filename=None, off_screen=None,
                               **kwargs):
        """Animate nodal solution.  Assumes nodal solution is a
        displacement array from a modal solution.

        rnum : int or list
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

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

        add_text : bool, optional
            Includes result information at the bottom left-hand corner
            of the plot.

        interpolate_before_map : bool, optional
            Leaving this at default generally results in a better plot.

        cpos : list, optional
            List of camera position, focal point, and view up.

        movie_filename : str, optional
            Filename of the movie to open.  Filename should end in mp4,
            but other filetypes may be supported.  See "imagio.get_writer".
            A single loop of the mode will be recorded.

        off_screen : bool, optional
            Can be used in conjunction with movie_filename to generate a
            movie non-interactively.

        kwargs : optional keyword arguments, optional
            See help(pyvista.plot) for additional keyword arguments.

        """
        # if kwargs.pop('smooth_shading', False):
        #     raise Exception('"smooth_shading" is not yet supported')

        # normalize nodal solution
        _, complex_disp = self.nodal_solution(rnum, as_complex=True,
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

        result_info = ''
        if add_text:
            result_info = self.text_result_table(rnum)

        # need only the surface of the full rotor
        full_rotor = self.full_rotor
        plot_mesh = full_rotor.extract_surface()
        orig_pt = plot_mesh.points

        # reduce the complex displacement to just the surface points
        ind = plot_mesh.point_arrays['vtkOriginalPointIds']
        complex_disp = np.take(complex_disp, ind, axis=0)

        if axis is not None:
            scalars = complex_disp[:, axis]
        else:
            scalars = (complex_disp*complex_disp).sum(1)**0.5

        plotter = pv.Plotter(off_screen=off_screen)

        if kwargs.pop('show_axes', True):
            plotter.add_axes()

        plotter.add_mesh(plot_mesh, scalars=np.real(scalars),
                         interpolate_before_map=interpolate_before_map, **kwargs)

        # setup text
        plotter.add_text(' ', font_size=20, position=[0, 0])

        if cpos:
            plotter.camera_position = cpos

        if movie_filename:
            plotter.open_movie(movie_filename)

        self._animating = True
        def q_callback():
            """exit when user wants to leave"""
            self._animating = False

        plotter.add_key_event("q", q_callback)

        # run until q is pressed
        plotter.show(interactive=False, auto_close=False,
                     interactive_update=True)
        first_loop = True
        while self._animating:
            for angle in np.linspace(0, np.pi*2, nangles):
                padj = 1*np.cos(angle) - 1j*np.sin(angle)
                complex_disp_adj = np.real(complex_disp*padj)

                if axis is not None:
                    scalars = complex_disp_adj[:, axis]
                else:
                    scalars = (complex_disp_adj*complex_disp_adj).sum(1)**0.5

                plotter.update_scalars(scalars, render=False)
                plot_mesh.points[:] = orig_pt + complex_disp_adj

                if show_phase:
                    if add_text:
                        plotter.textActor.SetInput('%s\nPhase %.1f Degrees' %
                                                   (result_info, (angle*180/np.pi)))

                plotter.update(1, force_redraw=True)

                if movie_filename and first_loop:
                    plotter.write_frame()

                if not self._animating:
                    break

            first_loop = False

            if not loop:
                break

        plotter.close()
        return plotter.camera_position

    def _gen_full_rotor(self):
        """ Create full rotor vtk unstructured grid """
        grid = self._mas_grid.copy()
        # transform to standard coordinate system
        cs_cord = self._resultheader['csCord']
        if cs_cord > 1:
            matrix = self.cs_4x4(cs_cord, as_vtk_matrix=True)
            grid.transform(matrix)

        # consider forcing low and high to be exact
        # self._mas_grid.point_arrays['CYCLIC_M01H'] --> rotate and match

        vtkappend = vtkAppendFilter()
        # vtkappend.MergePointsOn()
        # vtkappend.SetTolerance  # not available until vtk 9+
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

    @property
    def full_rotor(self):
        """UnstructuredGrid of the full replicated rotor"""
        if self._rotor_cache is None:
            self._rotor_cache = self._gen_full_rotor()
        return self._rotor_cache

    def _plot_cyclic_point_scalars(self, scalars, rnum,
                                   show_displacement=False,
                                   displacement_factor=1,
                                   overlay_wireframe=False,
                                   add_text=True,
                                   node_components=None,
                                   element_components=None,
                                   sel_type_all=True,
                                   phase=None,
                                   **kwargs):
        """Plot point scalars on active mesh.

        Parameters
        ----------
        scalars : numpy.ndarray
            Node scalars to plot.

        rnum : int, optional
            Cumulative result number.  Used for adding informative
            text.

        grid : pyvista.PolyData or pyvista.UnstructuredGrid, optional
            Uses self.grid by default.  When specified, uses this grid
            instead.

        show_displacement : bool, optional
            Deforms mesh according to the result.

        displacement_factor : float, optional
            Increases or decreases displacement by a factor.

        overlay_wireframe : bool, optional
            Overlay a wireframe of the original undeformed mesh.

        add_text : bool, optional
            Adds information about the result when rnum is given.

        kwargs : keyword arguments
            Additional keyword arguments.  See ``help(pyvista.plot)``

        Returns
        -------
        cpos : list
            Camera position.

        """
        # extract a sub-component of the grid if requested
        grid = self._mas_grid
        if node_components:
            grid, ind = self._extract_node_components(node_components,
                                                      sel_type_all)
            scalars = scalars[:, ind]

        elif element_components:
            grid, ind = self._extract_element_components(element_components)
            scalars = scalars[:, ind]

        # must be removed before add_mesh **kwargs
        window_size = kwargs.pop('window_size', None)
        full_screen = kwargs.pop('full_screen', False)
        screenshot = kwargs.pop('screenshot', None)
        kwargs.setdefault('cmap', 'jet')
        kwargs.setdefault('rng', [np.nanmin(scalars), np.nanmax(scalars)])

        # Plot off screen when not interactive
        off_screen = kwargs.pop('off_screen', None)
        plotter = pv.Plotter(off_screen=off_screen)

        # various plotting properties that must be removed before add_mesh
        if kwargs.pop('show_axes', True):
            plotter.add_axes()
        plotter.background_color = kwargs.pop('background', None)
        plotter.camera_position = kwargs.pop('cpos', None)

        cs_cord = self._resultheader['csCord']
        if cs_cord > 1:
            matrix = self.cs_4x4(cs_cord, as_vtk_matrix=True)
            i_matrix = self.cs_4x4(cs_cord, as_vtk_matrix=True)
            i_matrix.Invert()
        else:
            matrix = vtkMatrix4x4()
            i_matrix = vtkMatrix4x4()

        if overlay_wireframe:
            rang = 360.0 / self.n_sector
            for i in range(self.n_sector):
                actor = plotter.add_mesh(grid.copy(False), color='w',
                                         style='wireframe',
                                         opacity=0.5, **kwargs)

                # transform to standard position, rotate about Z axis,
                # transform back
                transform = vtkTransform()
                transform.RotateZ(rang*i)
                transform.Update()
                rot_matrix = transform.GetMatrix()

                if cs_cord > 1:
                    temp_matrix = vtkMatrix4x4()
                    rot_matrix.Multiply4x4(i_matrix, rot_matrix, temp_matrix)
                    rot_matrix.Multiply4x4(temp_matrix, matrix, rot_matrix)
                    transform.SetMatrix(rot_matrix)

                actor.SetUserTransform(transform)

        # add main mesh
        if show_displacement:
            _, disp = self.nodal_solution(rnum, phase, full_rotor=True)
            disp *= displacement_factor
            if node_components:
                _, ind = self._extract_node_components(node_components, sel_type_all)
                disp = disp[:, ind]
            elif element_components:
                _, ind = self._extract_element_components(element_components)
                disp = disp[:, ind]

            disp = disp.reshape(-1, 3)

            rotor = self.full_rotor.copy()
            rotor.points += disp
            actor = plotter.add_mesh(rotor,
                                     scalars=scalars.reshape(-1, 3),
                                     **kwargs)

        else:
            rang = 360.0 / self.n_sector
            for i in range(self.n_sector):
                actor = plotter.add_mesh(grid.copy(False),
                                         scalars=scalars[i],
                                         **kwargs)

                # NAN/missing data are white
                plotter.mapper.GetLookupTable().SetNanColor(1, 1, 1, 1)

                # transform to standard position, rotate about Z axis,
                # transform back
                transform = vtkTransform()
                transform.RotateZ(rang*i)
                transform.Update()
                rot_matrix = transform.GetMatrix()

                if cs_cord > 1:
                    temp_matrix = vtkMatrix4x4()
                    rot_matrix.Multiply4x4(i_matrix, rot_matrix, temp_matrix)
                    rot_matrix.Multiply4x4(temp_matrix, matrix, rot_matrix)
                    transform.SetMatrix(rot_matrix)

                actor.SetUserTransform(transform)

        # add table
        if add_text and rnum is not None:
            rnum = self.parse_step_substep(rnum)
            plotter.add_text(self.text_result_table(rnum), font_size=20,
                             position=[0, 0])

        if screenshot:
            cpos = plotter.show(auto_close=False,
                                window_size=window_size,
                                full_screen=full_screen)
            if screenshot is True:
                img = plotter.screenshot()
            else:
                plotter.screenshot(screenshot)
            plotter.close()
        else:
            cpos = plotter.show(window_size=window_size, full_screen=full_screen)

        if screenshot is True:
            return cpos, img
        else:
            return cpos
