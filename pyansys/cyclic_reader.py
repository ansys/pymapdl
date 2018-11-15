import vtk
import struct
import os
import numpy as np
import warnings
import logging
import ctypes
from ctypes import c_int64

from vtki.common import axis_rotation

import vtki
from pyansys import _parsefull
from pyansys import _rstHelper
from pyansys import _parser
from pyansys.elements import valid_types
from pyansys import Result

# Create logger
log = logging.getLogger(__name__)
log.setLevel('DEBUG')

np.seterr(divide='ignore', invalid='ignore')


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
            warnings.warn('Cyclic coordinate system %d' %
                          self.resultheader['csCord'])

        # idenfity the sector based on number of elements in master sector
        cs_els = self.resultheader['csEls']
        mask = self.quadgrid.cell_arrays['ansys_elem_num'] <= cs_els
        # node_mask = self.geometry['nnum'] <= self.resultheader['csNds']
        node_mask = self.nnum <= self.resultheader['csNds']

        self.master_cell_mask = mask
        self.grid = self.grid.extract_cells(mask)

        # number of nodes in sector may not match number of nodes in geometry
        self.mas_ind = np.nonzero(node_mask)[0]

        # duplicate sector may not exist
        if not np.any(self.geometry['nnum'] > self.resultheader['csNds']):
            self.dup_ind = None
        else:
            shift = (self.geometry['nnum'] < self.resultheader['csNds']).sum()
            self.dup_ind = self.mas_ind + shift + 1

        # create full rotor
        self.nsector = self.resultheader['nSector']

        # Create rotor of sectors
        vtkappend = vtk.vtkAppendFilter()
        rang = 360.0 / self.nsector
        for i in range(self.nsector):

            # Transform mesh
            sector = self.grid.copy()
            sector.rotate_z(rang * i)
            vtkappend.AddInputData(sector)

        vtkappend.Update()
        self.rotor = vtki.UnstructuredGrid(vtkappend.GetOutput())

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
            result_expanded.append(axis_rotation(result_combined, angle, deg=False,
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
        npoints = self.grid.number_of_points
        if nnum.size != npoints:
            scalars = np.empty_like((self.nsector, npoints))
            scalars[:] = np.nan
            nnum_grid = self.grid.point_arrays['ansys_node_num']
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

    def AnimateNodalSolution(self, rnum, comp='norm', max_disp=0.1,
                             nangles=180, show_phase=True,
                             show_result_info=True,
                             interpolatebeforemap=True, cpos=None,
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

        interpolatebeforemap : bool, optional
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

        plobj = vtki.Plotter(off_screen=not interactive)
        plobj.add_mesh(self.rotor.copy(), scalars=np.real(scalars),
                      interpolatebeforemap=interpolatebeforemap, **kwargs)
        plobj.update_coordinates(orig_pt + np.real(complex_disp), render=False)

        # setup text
        plobj.add_text(' ', fontsize=30)

        if cpos:
            plobj.camera_position = cpos

        if movie_filename:
            plobj.open_movie(movie_filename)

        # run until q is pressed
        plobj.plot(interactive=False, autoclose=False,
                   interactive_update=True)
        first_loop = True
        while not plobj.q_pressed:
            for angle in np.linspace(0, np.pi*2, nangles):
                padj = 1*np.cos(angle) - 1j*np.sin(angle)
                complex_disp_adj = np.real(complex_disp*padj)

                if axis is not None:
                    scalars = complex_disp_adj[:, axis]
                else:
                    scalars = (complex_disp_adj*complex_disp_adj).sum(1)**0.5

                plobj.update_scalars(scalars, render=False)
                plobj.update_coordinates(orig_pt + complex_disp_adj,
                                        render=False)

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
        sectors.append(axis_rotation(u_mas, angle, deg=False, axis='z'))

    return np.asarray(sectors)
