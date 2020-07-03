"""Read ANSYS binary result files *.rst

Used:
/usr/ansys_inc/v150/ansys/customize/include/fdresu.inc
"""
from collections.abc import Iterable
from itertools import compress
import time
import warnings
import logging
from threading import Thread
from functools import wraps

import vtk
import numpy as np
import pyvista as pv

from pyansys import _binary_reader, _reader
from pyansys.geometry import Geometry
from pyansys._binary_reader import (cells_with_any_nodes, cells_with_all_nodes)
from pyansys._rst_keys import (geometry_header_keys, element_index_table_info,
                               solution_data_header_keys, solution_header_keys_dp,
                               result_header_keys)
from pyansys._mp_keys import mp_keys
from pyansys.common import (read_table, parse_header, AnsysBinary,
                            read_standard_header, rotate_to_global)
from pyansys.misc import vtk_cell_info

VTK9 = vtk.vtkVersion().GetVTKMajorVersion() >= 9

# Create logger
LOG = logging.getLogger(__name__)
LOG.setLevel('DEBUG')

np.seterr(divide='ignore', invalid='ignore')


# Pointer information from ansys interface manual
# =============================================================================
# Individual element index table
ELEMENT_INDEX_TABLE_KEYS = ['EMS', 'ENF', 'ENS', 'ENG', 'EGR',
                            'EEL', 'EPL', 'ECR', 'ETH', 'EUL',
                            'EFX', 'ELF', 'EMN', 'ECD', 'ENL',
                            'EHC', 'EPT', 'ESF', 'EDI', 'ETB',
                            'ECT', 'EXY', 'EBA', 'ESV', 'MNL']

ELEMENT_RESULT_NCOMP = {'ENS': 6,
                        'EEL': 7,
                        'EPL': 7,
                        'ECR': 7,
                        'ETH': 8,
                        'ENL': 10,
                        'EDI': 7}


class ResultFile(AnsysBinary):
    """Reads a binary ANSYS result file.

    Parameters
    ----------
    filename : str, optional
        Filename of the ANSYS binary result file.

    ignore_cyclic : bool, optional
        Ignores any cyclic properties.

    read_geometry : bool, optional
        Debug parameter.  Set to False to disable reading in the
        geometry.

    Examples
    --------
    >>> import pyansys
    >>> rst = pyansys.read_binary('file.rst')
    """

    def __init__(self, filename, read_geometry=True, **kwargs):
        """Loads basic result information from result file and
        initializes result object.
        """
        self.filename = filename
        self._resultheader = self._read_result_header()
        self._animating = False

        # Get the total number of results and log it
        self.nsets = len(self._resultheader['rpointers'])
        LOG.debug('There are %d result(s) in this file', self.nsets)

        # Get indices to resort nodal and element results
        self._sidx = np.argsort(self._resultheader['neqv'])
        self._sidx_elem = np.argsort(self._resultheader['eeqv'])

        # Store node numbering in ANSYS
        self._neqv = self._resultheader['neqv']
        self._eeqv = self._resultheader['eeqv']  # unsorted

        # store geometry for later retrival
        self.geometry = None
        if read_geometry:
            self._store_geometry()

        self.header = parse_header(self.read_record(103), result_header_keys)
        self._geometry_header = {}
        self._materials = None
        self._section_data = None

    @property
    def n_sector(self):
        """Number of sectors"""
        return self._resultheader['nSector']

    def _read_result_header(self):
        """Returns pointers used to access results from an ANSYS result file.

        Parameters
        ----------
        filename : string
            Filename of result file.

        Returns
        -------
        resultheader : dictionary
            Result header
        """
        # consider moving this to the main class
        standard_header = read_standard_header(self.filename)

        # Read .RST FILE HEADER
        header = parse_header(self.read_record(103), result_header_keys)
        resultheader = merge_two_dicts(header, standard_header)

        # Read nodal equivalence table
        resultheader['neqv'] = self.read_record(resultheader['ptrNOD'])

        # Read nodal equivalence table
        resultheader['eeqv'] = self.read_record(resultheader['ptrELM'])

        # Read table of pointers to locations of results
        nsets = resultheader['nsets']

        # Data sets index table. This record contains the record pointers
        # for the beginning of each data set. The first resmax records are
        # the first 32 bits of the index, the second resmax records are
        # the second 32 bits f.seek((ptrDSIl + 0) * 4)
        record = self.read_record(resultheader['ptrDSI'])
        raw0 = record[:resultheader['resmax']].tobytes()
        raw1 = record[resultheader['resmax']:].tobytes()

        # this combines the two ints, not that efficient
        subraw0 = [raw0[i*4:(i+1)*4] for i in range(nsets)]
        subraw1 = [raw1[i*4:(i+1)*4] for i in range(nsets)]
        longraw = [subraw0[i] + subraw1[i] for i in range(nsets)]
        longraw = b''.join(longraw)
        rpointers = np.frombuffer(longraw, 'i8')

        assert (rpointers >= 0).all(), 'Data set index table has negative pointers'
        resultheader['rpointers'] = rpointers

        # read in time values
        record = self.read_record(resultheader['ptrTIM'])
        resultheader['time_values'] = record[:resultheader['nsets']]

        # load harmonic index of each result
        if resultheader['ptrCYC']:
            record = self.read_record(resultheader['ptrCYC'])
            hindex = record[:resultheader['nsets']]

            # ansys 15 doesn't track negative harmonic indices
            if not np.any(hindex < -1):
                # check if duplicate frequencies
                tvalues = resultheader['time_values']
                for i in range(tvalues.size - 1):
                    # adjust tolarance(?)
                    if np.isclose(tvalues[i], tvalues[i + 1]):  
                        hindex[i + 1] *= -1

            resultheader['hindex'] = hindex

        # load step table with columns:
        # [loadstep, substep, and cumulative]
        record = self.read_record(resultheader['ptrLSP'])
        resultheader['ls_table'] = record[:resultheader['nsets']*3].reshape(-1, 3)

        return resultheader

    def parse_coordinate_system(self):
        """Reads in coordinate system information from a binary result
        file.

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
        maxcsy = self._geometry_header['maxcsy']

        # load coordinate system index table
        ptr_csy = self._geometry_header['ptrCSY']
        if ptr_csy:
            csy = self.read_record(ptr_csy)

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
            if not csy[i]:
                c_system = None
            else:
                data = self.read_record(ptr_csy + csy[i])
                c_system = {'transformation matrix': np.array(data[:9].reshape(-1, 3)),
                            'origin': np.array(data[9:12]),
                            'PAR1': data[12],
                            'PAR2': data[13],
                            'euler angles': data[15:18],  # may not be euler
                            'theta singularity': data[18],
                            'phi singularity': data[19],
                            'type': int(data[20]),
                            'reference num': int(data[21],)
                            }
            c_systems.append(c_system)

        return c_systems

    def _load_materials(self):
        """Reads the material properties from the result file.

        Materials property table is stored at ptrMAT, which contains
        pointers to each material property array for each material.
        Each array contains a material property (e.g. EX, or elastic
        modulus in the X direction) and there may be one or many
        values for each material (up to 101).
        """

        def read_mat_data(ptr):
            """reads double precision material data given an offset from ptrMAT"""
            arr = self.read_record(self._geometry_header['ptrMAT'] + ptr)
            arr = arr[arr != 0]
            if arr.size == 1:
                return arr[0]

        mat_table = self.read_record(self._geometry_header['ptrMAT'])
        self._materials = {}
        for i in range(self._geometry_header['nummat']):
            # pointers to the material data for each material
            mat_data_ptr = mat_table[3 + 176*i:3 + 176*i + 159]
            material = {}
            for j, key in enumerate(mp_keys):
                ptr = mat_data_ptr[j + 1]
                if ptr:
                    material[key] = read_mat_data(ptr)

            # store by material number
            self._materials[mat_data_ptr[0]] = material

    @property
    def materials(self):
        """Result file material properties.

        Returns
        -------
        materials : dict
            Dictionary of Materials.  Keys are the material numbers,
            and each material is a dictionary of the material
            properrties of that material with only the valid entries filled.

        NOTES
        -----
        Material properties:

        - EX : Elastic modulus, element x direction (Force/Area)
        - EY : Elastic modulus, element y direction (Force/Area)
        - EZ : Elastic modulus, element z direction (Force/Area)
        - ALPX : Coefficient of thermal expansion, element x direction (Strain/Temp)
        - ALPY : Coefficient of thermal expansion, element y direction (Strain/Temp)
        - ALPZ : Coefficient of thermal expansion, element z direction (Strain/Temp)
        - REFT : Reference temperature (as a property) [TREF]
        - PRXY : Major Poisson's ratio, x-y plane
        - PRYZ : Major Poisson's ratio, y-z plane
        - PRX  Z : Major Poisson's ratio, x-z plane
        - NUXY : Minor Poisson's ratio, x-y plane
        - NUYZ : Minor Poisson's ratio, y-z plane
        - NUXZ : Minor Poisson's ratio, x-z plane
        - GXY : Shear modulus, x-y plane (Force/Area)
        - GYZ : Shear modulus, y-z plane (Force/Area)
        - GXZ : Shear modulus, x-z plane (Force/Area)
        - DAMP : K matrix multiplier for damping [BETAD] (Time)
        - MU : Coefficient of friction (or, for FLUID29 and FLUID30 
               elements, boundary admittance)
        - DENS : Mass density (Mass/Vol)
        - C : Specific heat (Heat/Mass*Temp)
        - ENTH : Enthalpy (e DENS*C d(Temp)) (Heat/Vol)
        - KXX : Thermal conductivity, element x direction
                (Heat*Length / (Time*Area*Temp))
        - KYY : Thermal conductivity, element y direction
                (Heat*Length / (Time*Area*Temp))
        - KZZ : Thermal conductivity, element z direction
                (Heat*Length / (Time*Area*Temp))
        - HF : Convection (or film) coefficient (Heat / (Time*Area*Temp))
        - EMIS : Emissivity
        - QRATE : Heat generation rate (MASS71 element only) (Heat/Time)
        - VISC : Viscosity (Force*Time / Length2)
        - SONC : Sonic velocity (FLUID29 and FLUID30 elements only) (Length/Time)
        - RSVX : Electrical resistivity, element x direction (Resistance*Area / Length)
        - RSVY : Electrical resistivity, element y direction (Resistance*Area / Length)
        - RSVZ : Electrical resistivity, element z direction (Resistance*Area / Length)
        - PERX : Electric permittivity, element x direction (Charge2 / (Force*Length))
        - PERY : Electric permittivity, element y direction (Charge2 / (Force*Length))
        - PERZ : Electric permittivity, element z direction (Charge2 / (Force*Length))
        - MURX : Magnetic relative permeability, element x direction
        - MURY : Magnetic relative permeability, element y direction
        - MURZ : Magnetic relative permeability, element z direction
        - MGXX : Magnetic coercive force, element x direction (Charge / (Length*Time))
        - MGYY : Magnetic coercive force, element y direction (Charge / (Length*Time))
        - MGZZ : Magnetic coercive force, element z direction (Charge / (Length*Time))
        """
        if self._materials is None:
            self._load_materials()
        return self._materials

    def _load_section_data(self):
        """Loads the section data from the result file"""
        ptr_sec = self._geometry_header['ptrSEC']
        sec_table = self.read_record(ptr_sec)

        self._section_data = {}
        for offset in sec_table:
            if offset:
                table = self.read_record(ptr_sec + offset)
                self._section_data[int(table[0])] = table[1:]

        # it might be possible to interpert the section data...
        # sec[3] # total thickness
        # sec[4] # number of layers (?)
        # sec[5] # total integration points (?)

        # sec[29] # start of a layer (thickness)
        # - MatID
        # - Ori. Angle
        # - Num Intg.
        # sec[33] # start of another layer
        # sec[37] # start of another layer

    @property
    def section_data(self):
        """The section data from the result file

        Returns
        -------
        section_data : dict
            Dictionary of the section data with the section numbers as
            keys.

        Notes
        -----
        There is limited documentation on how ANSYS stores the
        sections within a result file, and as such it may be difficult
        to interpret the section data for a given model.
        """
        if self._section_data is None:
            self._load_section_data()
        return self._section_data

    def plot(self, node_components=None, element_components=None,
             sel_type_all=True, **kwargs):
        """Plot result geometry

        Parameters
        ----------
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

        **kwargs : keyword arguments
            Optional keyword arguments.  See help(pyvista.plot)

        Returns
        -------
        cpos : list
            List of camera position, focal point, and view up.

        Examples
        --------
        >>> import pyansys
        >>> rst = pyansys.read_binary('file.rst')
        >>> rst.plot()

        Plot just the element component 'ROTOR_SHAFT'

        >>> rst.plot(element_components='ROTOR_SHAFT')

        Plot two node components
        >>> rst.plot(node_components=['MY_COMPONENT', 'MY_OTHER_COMPONENT'])
        """
        kwargs.setdefault('show_edges', True)

        if node_components:
            grid, _ = self._extract_node_components(node_components, sel_type_all)
        elif element_components:
            grid, _ = self._extract_element_components(element_components)
        else:
            grid = self.grid

        return self._plot_point_scalars(None, grid=grid, **kwargs)

    def plot_nodal_solution(self, rnum, comp='norm',
                            show_displacement=False,
                            displacement_factor=1.0,
                            node_components=None,
                            element_components=None,
                            sel_type_all=True,
                            **kwargs):
        """Plots the nodal solution.

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        comp : str, optional
            Display component to display.  Options are ``'x'``,
            ``'y'``, ``'z'``, or ``'norm'``.  This corresponds to the
            x directin, y direction, z direction, and the normalized
            result.

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
        Plot the nodal solution result 0 of verification manual
        example

        >>> import pyansys
        >>> result = pyansys.download_verification_result(33)
        >>> result.plot_nodal_solution(0)

        Plot with a white background and showing edges

        >>> result.plot_nodal_solution(0, background='w', show_edges=True)

        """
        # Load result from file
        rnum = self.parse_step_substep(rnum)
        nnum, result = self.nodal_solution(rnum)
        label = 'Displacement'

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

        ind = None
        if node_components:
            grid, ind = self._extract_node_components(node_components, sel_type_all)
            scalars = scalars[ind]
        elif element_components:
            grid, ind = self._extract_element_components(element_components)
            scalars = scalars[ind]
        else:
            grid = self.grid

        return self._plot_point_scalars(scalars, rnum=rnum, grid=grid,
                                        stitle=stitle,
                                        show_displacement=show_displacement,
                                        displacement_factor=displacement_factor,
                                        node_components=node_components,
                                        element_components=element_components,
                                        sel_type_all=sel_type_all,
                                        **kwargs)

    @wraps(plot_nodal_solution)
    def plot_nodal_displacement(self, *args, **kwargs):
        """wraps plot_nodal_solution"""
        return self.plot_nodal_solution(*args, **kwargs)

    @property
    def node_components(self):
        """Dictionary of ansys node components from the result file.

        Examples
        --------
        >>> import pyansys
        >>> from pyansys import examples
        >>> rst = pyansys.read_binary(examples.rstfile)
        >>> rst.node_components.keys()
        dict_keys(['ECOMP1', 'ECOMP2', 'ELEM_COMP'])
        >>> rst.node_components['NODE_COMP']
        array([ 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
              20], dtype=int32)
        """
        return self.geometry.node_components

    @property
    def element_components(self):
        """Dictionary of ansys element components from the result file.

        Examples
        --------
        >>> import pyansys
        >>> from pyansys import examples
        >>> rst = pyansys.read_binary(examples.rstfile)
        >>> rst.element_components
        {'ECOMP1': array([17, 18, 21, 22, 23, 24, 25, 26, 27, 28, 29,
                30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40], dtype=int32),
        'ECOMP2': array([ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13,
                14, 15, 16, 17, 18, 19, 20, 23, 24], dtype=int32),
        'ELEM_COMP': array([ 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
                16, 17, 18, 19, 20], dtype=int32)}
        """
        return self.geometry.element_components

    def _extract_node_components(self, node_components,
                                 sel_type_all=True, grid=None):
        """Return the part of the grid matching node components """
        if grid is None:
            grid = self.grid

        if not self.geometry.node_components:  # pragma: no cover
            raise Exception('Missing component information.\n' +
                            'Either no components have been stored, or ' +
                            'the version of this result file is <18.2')

        if isinstance(node_components, str):
            node_components = [node_components]

        mask = np.zeros(grid.n_points, np.bool)
        for component in node_components:
            component = component.upper()
            if component not in grid.point_arrays:
                raise KeyError('Result file does not contain node ' +
                               'component "%s"' % component)

            mask += grid.point_arrays[component].view(np.bool)

        # need to extract the mesh
        cells, offset = vtk_cell_info(grid)
        if sel_type_all:
            cell_mask = cells_with_all_nodes(offset, cells, grid.celltypes,
                                             mask.view(np.uint8))
        else:
            cell_mask = cells_with_any_nodes(offset, cells, grid.celltypes,
                                             mask.view(np.uint8))

        if not cell_mask.any():
            raise RuntimeError('Empty component')
        reduced_grid = grid.extract_cells(cell_mask)

        if not reduced_grid.n_cells:
            raise RuntimeError('Empty mesh due to component selection\n' +
                               'Try "sel_type_all=False"')

        ind = reduced_grid.point_arrays['vtkOriginalPointIds']
        if not ind.any():
            raise RuntimeError('Invalid selection.\n' +
                               'Try ``sel_type_all=False``')

        return reduced_grid, ind

    def _extract_element_components(self, element_components, grid=None):
        """Return the part of the grid matching element components"""
        if grid is None:
            grid = self.grid

        if not self.geometry.element_components:  # pragma: no cover
            raise Exception('Missing component information.\n' +
                            'Either no components have been stored, or ' +
                            'the version of this result file is <18.2')

        if isinstance(element_components, str):
            element_components = [element_components]

        cell_mask = np.zeros(grid.n_cells, np.bool)
        for component in element_components:
            component = component.upper()
            if component not in grid.cell_arrays:
                raise KeyError('Result file does not contain element ' +
                               'component "%s"' % component)
            cell_mask += grid.cell_arrays[component].view(np.bool)

        if not cell_mask.any():
            raise RuntimeError('Empty component')
        reduced_grid = grid.extract_cells(cell_mask)

        ind = reduced_grid.point_arrays['vtkOriginalPointIds']
        if not ind.any():
            raise RuntimeError('Invalid component')

        return reduced_grid, ind

    @property
    def time_values(self):
        return self._resultheader['time_values']

    def animate_nodal_solution(self, rnum, comp='norm',
                               node_components=None,
                               element_components=None,
                               sel_type_all=True, add_text=True,
                               max_disp=0.1, nangles=100, loop=True,
                               movie_filename=None, **kwargs):
        """Animate nodal solution.  Assumes nodal solution is a
        displacement array from a modal solution.

        rnum : int or list
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        comp : str, optional
            Scalar component to display.  Options are ``'x'``,
            ``'y'``, ``'z'``, and ``'norm'``, and ``None``.

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

        add_text : bool, optional
            Adds information about the result when rnum is given.

        max_disp : float, optional
            Maximum displacement in the units of the model.  Default
            0.1

        nangles : int, optional
            Number of "frames" between each full cycle.

        movie_filename : str, optional
            Filename of the movie to open.  Filename should end in
            ``'mp4'``, but other filetypes may be supported.  See
            ``imagio.get_writer``.  A single loop of the mode will be
            recorded.

        kwargs : optional keyword arguments, optional
            See help(pyvista.Plot) for additional keyword arguments.

        Examples
        --------
        Animate first result

        >>> rst.animate_nodal_solution(0)

        Animate second result while displaying the x scalars
        without looping

        >>> rst.animate_nodal_solution(1, comp='x', loop=False)

        Animate second result and save as a movie

        >>> rst.animate_nodal_solution(0, movie_filename='disp.mp4')
        """
        scalars = None
        if comp:
            _, disp = self.nodal_solution(rnum)
            disp = disp[:, :3]

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

        if node_components:
            grid, ind = self._extract_node_components(node_components, sel_type_all)
            if comp:
                scalars = scalars[ind]
        elif element_components:
            grid, ind = self._extract_element_components(element_components)
            if comp:
                scalars = scalars[ind]
        else:
            grid = self.grid

        return self._plot_point_scalars(scalars, rnum=rnum, grid=grid,
                                        add_text=add_text,
                                        animate=True,
                                        node_components=node_components,
                                        element_components=element_components,
                                        sel_type_all=sel_type_all,
                                        nangles=nangles,
                                        movie_filename=movie_filename,
                                        max_disp=max_disp, loop=loop, **kwargs)

    @wraps(animate_nodal_solution)
    def animate_nodal_displacement(self, *args, **kwargs):
        """wraps animate_nodal_solution"""
        self.animate_nodal_solution(*args, **kwargs)

    def nodal_time_history(self, solution_type='NSL', in_nodal_coord_sys=False):
        """Returns the DOF solution for each node in the global
        cartesian coordinate system or nodal coordinate system.

        Parameters
        ----------
        solution_type: str, optional
            Specify, whether nodal displacements (``'NSL'``), nodal
            velocities (``'VEL'``) or nodal accelerations (``'ACC'``)
            will be read.

        in_nodal_coord_sys : bool, optional
            When True, returns results in the nodal coordinate system.
            Default False.

        Returns
        -------
        nnum : int np.ndarray
            Node numbers associated with the results.

        result : float np.ndarray
            Result is ``self.nsets x nnod x Sumdof``, or number of
            time steps by number of nodes by degrees of freedom.
        """
        if solution_type not in ('NSL', 'VEL', 'ACC'):
            raise ValueError("Argument 'solution type' must be either 'NSL', 'VEL', or 'ACC'")

        # Get info from result header
        rpointers = self._resultheader['rpointers']
        nsets = self.nsets

        # Read a result
        # with open(self.filename, 'rb') as f:
        # get first solution header and assume, following solution
        # headers are equal
        record = self.read_record(rpointers[0])
        solution_header = parse_header(record, solution_data_header_keys)

        mask = solution_header['mask']
        # PDBN = bool(mask & 0b1<<10)
        pdnsl = bool(solution_header['AvailData'] & 0b1 << 27)
        PDVEL = bool(mask & 0b1 << 27)
        PDACC = bool(mask & 0b1 << 28)

        if solution_type == 'NSL' and not pdnsl:
            raise Exception("Result file does not contain nodal displacements.")

        if solution_type == 'VEL' and not PDVEL:
            raise Exception("Result file does not contain nodal velocities.")

        if solution_type == 'ACC' and not PDACC:
            raise Exception("Result file does not contain nodal accelerations.")

        nnod = solution_header['nnod']
        numdof = solution_header['numdof']
        nfldof = solution_header['nfldof']
        sumdof = numdof + nfldof

        #numvdof = solution_header['numvdof'] # does not seem to be set in transient analysis
        #if not numvdof: numvodf = sumdof 
        #numadof = solution_header['numadof'] # does not seem to be set in transient analysis
        #if not numadof: numadof = sumdof 

        # iterate over all loadsteps
        results = np.zeros((nsets, nnod, sumdof))
        for rnum in range(self.nsets):
            # Seek to result table and to get pointer to DOF
            # results of result table
            rsol_header = parse_header(self.read_record(rpointers[rnum]),
                                       solution_data_header_keys)
            if solution_type == 'NSL':  # Nodal Displacements
                ptr_sl = rsol_header['ptrNSL']
            elif solution_type == 'VEL':  # Nodal Velocities
                ptr_sl = rsol_header['ptrVSL']
            elif solution_type == 'ACC':  # Nodal Accelerations
                ptr_sl = rsol_header['ptrASL']

            record, sz = self.read_record(rpointers[rnum] + ptr_sl,
                                          return_bufsize=True)
            # nitems = record.size
            result = record.reshape((-1, sumdof))

            # PDBN should be set if only a subset of nodes was output
            # PDBN is set only when solution type: nodal solution/displacement
            # PDBN is not set when solution type: acceleration, velocities
            if record.size != sumdof*nnod:
                # read the next record to the internal indexing reording
                nodlist = self.read_record(rpointers[rnum] + ptr_sl + sz)

                # convert to zero index
                sidx = nodlist -1

            else:
                # Reorder based on sorted indexing
                sidx = self._sidx

            results[rnum, sidx, :] = result

        if not in_nodal_coord_sys:
            euler_angles = self.geometry.node_angles[self._insolution].T

            for rnum in range(nsets):
                result = results[rnum, :, :]
                rotate_to_global(result, euler_angles)

        # check for invalid values
        # mapdl writes invalid values as 2*100
        results[results == 2**100] = 0

        # also include nodes in output
        return self._neqv[self._sidx], results

    def nodal_solution(self, rnum, in_nodal_coord_sys=False):
        """Returns the DOF solution for each node in the global
        cartesian coordinate system or nodal coordinate system.

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        in_nodal_coord_sys : bool, optional
            When True, returns results in the nodal coordinate system.
            Default False.

        Returns
        -------
        nnum : int np.ndarray
            Node numbers associated with the results.

        result : float np.ndarray
            Result is (``nnod`` x ``sumdof``), or number of nodes by degrees
            of freedom which includes ``numdof`` and ``nfldof``.

        Examples
        --------
        >>> import pyansys
        >>> rst = pyansys.read_binary('file.rst')
        >>> nnum, data = rst.nodal_solution(0)

        Notes
        -----
        Some solution results may not include all node numbers.  This
        is reflected in the ``result`` and ``nnum`` arrays.

        """
        # convert to cumulative index
        rnum = self.parse_step_substep(rnum)

        # result pointer
        ptr_rst = self._resultheader['rpointers'][rnum]
        result_solution_header = parse_header(self.read_record(ptr_rst),
                                              solution_data_header_keys)

        nnod = result_solution_header['nnod']
        numdof = result_solution_header['numdof']
        nfldof = result_solution_header['nfldof']
        sumdof = numdof + nfldof

        ptr_nsl = result_solution_header['ptrNSL']

        # Read the nodal solution
        result, bufsz = self.read_record(ptr_nsl + ptr_rst, True)
        result = result.reshape(-1, sumdof)

        # additional entries are sometimes written for no discernible
        # reason
        if result.shape[0] > nnod:
            result = result[:nnod]

        # # it's possible that not all results are written
        if result.shape[0] != nnod:
            # read second buffer containing the node indices of the
            # results and convert from fortran to zero indexing
            sidx = self.read_record(ptr_nsl + ptr_rst + bufsz) - 1
            unsort_nnum = self._resultheader['neqv'][sidx]

            # now, sort using the new sorted node numbers indices
            new_sidx = np.argsort(unsort_nnum)
            nnum = unsort_nnum[new_sidx]
            result = result[new_sidx]

            # these are the associated nodal locations
            # sidx_inv = np.argsort(self._sidx)
            # nodes = self.geometry['nodes'][sidx_inv][sidx][:, :3]
        else:
            nnum = self._neqv[self._sidx]
            result = result.take(self._sidx, 0)

        # Convert result to the global coordinate system
        if not in_nodal_coord_sys:
            euler_angles = self.geometry.node_angles[self._insolution].T
            rotate_to_global(result, euler_angles)

        # check for invalid values (mapdl writes invalid values as 2*100)
        result[result == 2**100] = 0
        return nnum, result

    @wraps(nodal_solution)
    def nodal_displacement(self, *args, **kwargs):
        """wraps plot_nodal_solution"""
        return self.nodal_solution(*args, **kwargs)

    def _read_components(self):
        """Read components from an ANSYS result file

        Returns
        -------
        components : dict
            Dictionary of components

        Notes
        -----
        Only available as of ~v194 and newer.

        From fdresu.inc:

        Component/assembly data.  The first word will describe the
        type of component or assembly (1=node component, 2=elem
        component, 11->15 assembly) For components, values 2->9 are
        the component name converted to integers.  The remaining
        values are the list of nodes/elems in the component.  For
        assemblies, the remaining values (in groups of 8) are the
        component names converted to integers.
        """
        node_comp = {}
        elem_comp = {}
        ncomp = self._geometry_header['maxcomp']

        # Read through components
        file_ptr = self._geometry_header['ptrCOMP']
        for _ in range(ncomp):
            table, sz = self.read_record(file_ptr, True)
            file_ptr += sz  # increment file_pointer

            name = table[1:9].tobytes().split(b'\x00')[0].decode('utf')
            name = name[:4][::-1] + name[4:8][::-1] + name[8:12][::-1] +\
                   name[12:16][::-1] + name[16:20][::-1] + name[20:24][::-1] +\
                   name[24:28][::-1] + name[28:32][::-1]
            name = name.strip()
            data = table[9:]
            if data.any():
                if table[0] == 1:  # node component
                    node_comp[name] = _reader.component_interperter(data)
                elif table[0] == 2:
                    elem_comp[name] = _reader.component_interperter(data)

        return node_comp, elem_comp

    def _store_geometry(self):
        """Store the geometry from the result file"""
        # read geometry header
        table = self.read_record(self._resultheader['ptrGEO'])
        geometry_header = parse_header(table, geometry_header_keys)
        self._geometry_header = geometry_header

        # Node information
        nnod = geometry_header['nnod']
        nnum = np.empty(nnod, np.int32)
        nodes = np.empty((nnod, 6), np.float)
        _binary_reader.load_nodes(self.filename, geometry_header['ptrLOC'],
                                  nnod, nodes, nnum)

        # Element information
        nelm = geometry_header['nelm']
        maxety = geometry_header['maxety']

        # pointer to the element type index table
        e_type_table = self.read_record(geometry_header['ptrETY'])

        # store information for each element type
        # make these arrays large so you can reference a value via element
        # type numbering

        # number of nodes for this element type
        nodelm = np.empty(10000, np.int32)

        # number of nodes per element having nodal forces
        nodfor = np.empty(10000, np.int32)

        # number of nodes per element having nodal stresses
        nodstr = np.empty(10000, np.int32)
        # etype_id = np.empty(maxety, np.int32)
        ekey = []
        keyopts = np.zeros((10000, 11), np.int16)
        for i in range(maxety):
            if not e_type_table[i]:
                continue

            ptr = geometry_header['ptrETY'] + e_type_table[i]
            einfo = self.read_record(ptr)

            etype_ref = einfo[0]
            ekey.append(einfo[:2])

            # Items 3-14 - element type option keys (keyopts)
            keyopts[etype_ref] = einfo[2:13]

            # Item 61 - number of nodes for this element type (nodelm)
            nodelm[etype_ref] = einfo[60]

            # Item 63 - number of nodes per element having nodal
            # forces, etc. (nodfor)
            nodfor[etype_ref] = einfo[62]

            # Item 94 - number of nodes per element having nodal
            # stresses, etc. (nodstr).  This number is the number
            # of corner nodes for higher-ordered elements.
            nodstr[etype_ref] = einfo[93]

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

        # the element description table
        # must view this record as int64, even though ansys reads
        # it in as a 32 bit int
        ptr_eid = geometry_header['ptrEID']
        e_disp_table = self.read_record(ptr_eid).view(np.int64)

        # get pointer to start of element table and adjust element pointers
        ptr_elem = geometry_header['ptrEID'] + e_disp_table[0]
        e_disp_table -= e_disp_table[0]

        # read in coordinate systems, material properties, and sections
        self._c_systems = self.parse_coordinate_system()

        # load elements
        elem, elem_off = _binary_reader.load_elements(self.filename, ptr_elem,
                                                      nelm, e_disp_table)

        # Store geometry and parse to VTK quadradic and null unallowed
        ncomp, ecomp = self._read_components()
        self.geometry = Geometry(nnum, nodes, elem, elem_off, np.array(ekey),
                                 node_comps=ncomp, elem_comps=ecomp)
        self.quadgrid = self.geometry._parse_vtk(null_unallowed=True,
                                                 fix_midside=False)
        self.grid = self.quadgrid.linear_copy()

        # identify nodes that are actually in the solution
        self._insolution = np.in1d(self.geometry.nnum, self._resultheader['neqv'],
                                   assume_unique=True)

    def solution_info(self, rnum):
        """Return an informative dictionary of solution data for a
        result.

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        Returns
        -------
        header : dict
            Double precision solution header data.

        Notes
        -----
        The keys of the solution header are described below:

        - timfrq : Time value (or frequency value, for a modal or
                   harmonic analysis)
        - lfacto : the "old" load factor (used in ramping a load
                    between old and new values)
        - lfactn  : The "new" load factor
        - cptime  : Elapsed CPU time (in seconds)
        - tref    : The reference temperature
        - tunif   : The uniform temperature
        - tbulk   : Bulk temp for FLOTRAN film coefs.
        - VolBase : Initial total volume for VOF
        - tstep   : Time Step size for FLOTRAN analysis
        - 0.0     : Position not used
        - accel   : Linear acceleration terms
        - omega   : Angular velocity (first 3 terms) and angular acceleration
                    (second 3 terms)
        - omegacg : Angular velocity (first 3 terms) and angular
                    acceleration (second 3 terms) these
                    velocity/acceleration terms are computed about the
                    center of gravity
        - cgcent  : (X,y,z) location of center of gravity
        - fatjack : Fatjack ocean wave data (wave height and period)
        - dval1   : If pmeth=0: FATJACK ocean wave direction
                    if pmeth=1: p-method convergence values
        - pCnvVal : P-method convergence values
        """
        # convert to cumulative index
        rnum = self.parse_step_substep(rnum)

        # skip pointers table
        ptr = self._resultheader['rpointers'][rnum]
        _, sz = self.read_record(ptr, True)

        table = self.read_record(ptr + sz)
        return parse_header(table, solution_header_keys_dp)

    def _element_solution_header(self, rnum):
        """Return the element solution header information.

        Parameters
        ----------
        rnum : int
            Result number.

        Returns
        -------
        ele_ind_table :
            A table of pointers relative to the element result table
            offset containing element result pointers.

        nodstr : np.ndarray
            Array containing the number of nodes with values for each element.

        etype : np.ndarray
            Element type array

        element_rst_ptr : int
            Offset to the start of the element result table.
        """
        # Get the header information from the header dictionary

        rpointers = self._resultheader['rpointers']
        nodstr = self.element_table['nodstr']

        # read result solution header
        record = self.read_record(rpointers[rnum])
        solution_header = parse_header(record, solution_data_header_keys)

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
            raise ValueError('No element solution in result set %d\n'
                             % (rnum + 1) + 'Try running with "MXPAND,,,,YES"')

        # Seek to element result header
        element_rst_ptr = rpointers[rnum] + solution_header['ptrESL']
        ele_ind_table = self.read_record(element_rst_ptr).view(np.int64)
        # ele_ind_table += element_rst_ptr

        # boundary conditions
        # bc = self.read_record(rpointers[rnum] + solution_header['ptrBC'])

        return ele_ind_table, nodstr, self.geometry._ans_etype, element_rst_ptr

    @property
    def version(self):
        """ The version of ANSYS used to generate this result file """
        return float(self._resultheader['verstring'])

    def element_stress(self, rnum, principal=False, in_element_coord_sys=False):
        """Retrives the element component stresses.

        Equivalent ANSYS command: PRESOL, S

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
            Syz Sxz or SIGMA1, SIGMA2, SIGMA3, SINT, SEQV when
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
        ele_ind_table, nodstr, etype, ptr_off = self._element_solution_header(rnum)

        # certain element types do not output stress
        elemtype = self.geometry.etype

        # load in raw results
        nnode = nodstr[etype]
        nelemnode = nnode.sum()

        # bitmask (might use this at some point)
        # bitmask = bin(int(hex(self._resultheader['rstsprs']), base=16)).lstrip('0b')
        # description maybe in resucm.inc

        if self.version >= 14.5:
            if self._resultheader['rstsprs'] != 0:
                nitem = 6
            else:
                nitem = 11

            # add extra elements to data array.  Sometimes there are
            # more items than listed in the result header (or there's
            # a mistake here)
            ele_data_arr = np.empty((nelemnode + 50, nitem), np.float64)
            ele_data_arr[:] = np.nan  # necessary?  should do this in read stress

            _binary_reader.read_element_stress(self.filename,
                                               ele_ind_table,
                                               nodstr.astype(np.int64),
                                               etype, ele_data_arr,
                                               nitem, elemtype,
                                               ptr_off,
                                               as_global=not in_element_coord_sys)

            if nitem != 6:
                ele_data_arr = ele_data_arr[:, :6]

        else:
            raise NotImplementedError('Not implemented for ANSYS older than v14.5')

        # trim off extra data
        ele_data_arr = ele_data_arr[:nelemnode]

        if principal:
            ele_data_arr, isnan = _binary_reader.compute_principal_stress(ele_data_arr)
            ele_data_arr[isnan] = np.nan

        splitind = np.cumsum(nnode)
        element_stress = np.split(ele_data_arr, splitind[:-1])

        # reorder list using sorted indices
        enum = self._eeqv
        sidx = np.argsort(enum)
        element_stress = [element_stress[i] for i in sidx]

        enode = []
        for i in sidx:
            enode.append(self.geometry.elem[i][10:10+nnode[i]])

        # Get element numbers
        elemnum = self._eeqv[self._sidx_elem]
        return element_stress, elemnum, enode

    def element_solution_data(self, rnum, datatype, sort=True):
        """Retrives element solution data.  Similar to ETABLE.

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
        enum : np.ndarray
            Element numbers.

        element_data : list
            List with one data item for each element.

        Notes
        -----
        See ANSYS element documentation for available items for each element type.

        ENG - Element volume and energies.
            volume: Element volume
            senergy: Element energy associated with the stiffness matrix
            aenergy: Artificial hourglass energy
            kenergy: Kinetic energy
            coenergy: Co-energy (magnetics)
            incenergy: Position not used
            position not used
            thenergy: Thermal dissipation energy (see ThermMat, shell131/132 only)
            position not used
            position not used
        """
        table_ptr = datatype.upper()
        if table_ptr not in ELEMENT_INDEX_TABLE_KEYS:
            err_str = 'Data type %s is invalid\n' % str(datatype)
            err_str += '\nAvailable types:\n'
            for key in ELEMENT_INDEX_TABLE_KEYS:
                err_str += '\t%s: %s\n' % (key, element_index_table_info[key])

            raise ValueError(err_str)

        # location of data pointer within each element result table
        table_index = ELEMENT_INDEX_TABLE_KEYS.index(table_ptr)

        rnum = self.parse_step_substep(rnum)
        ele_ind_table, _, _, ptr_off = self._element_solution_header(rnum)

        # read element data
        element_data = []
        for ind in ele_ind_table:
            if ind == 0:
                element_data.append(None)
            else:
                # read element table index pointer to data
                ptr = self.read_record(ind + ptr_off)[table_index]
                if ptr > 0:
                    record = self.read_record(ptr_off + ind + ptr)
                    element_data.append(record)
                else:
                    element_data.append(None)

        enum = self._eeqv
        if sort:
            sidx = np.argsort(enum)
            enum = enum[sidx]
            element_data = [element_data[i] for i in sidx]

        return enum, element_data

    def principal_nodal_stress(self, rnum):
        """Computes the principal component stresses for each node in
        the solution.

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        Returns
        -------
        nodenum : numpy.ndarray
            Node numbers of the result.

        pstress : numpy.ndarray
            Principal stresses, stress intensity, and equivalent stress.
            [sigma1, sigma2, sigma3, sint, seqv]

        Examples
        --------
        Load the principal nodal stress for the first solution.

        >>> import pyansys
        >>> rst = pyansys.read_binary('file.rst')
        >>> nnum, stress = rst.principal_nodal_stress(0)

        Notes
        -----
        ANSYS equivalent of:
        PRNSOL, S, PRIN

        which returns:
        S1, S2, S3 principal stresses, SINT stress intensity, and SEQV
        equivalent stress.
        """
        # get component stress
        nodenum, stress = self.nodal_stress(rnum)
        pstress, isnan = _binary_reader.compute_principal_stress(stress)
        pstress[isnan] = np.nan
        return nodenum, pstress

    def plot_principal_nodal_stress(self, rnum, stype=None,
                                    node_components=None,
                                    element_components=None,
                                    sel_type_all=True, **kwargs):
        """Plot the principal stress at each node in the solution.

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
                            "['1', '2', '3', 'INT', 'EQV']")
        stype = stype.upper()

        rnum = self.parse_step_substep(rnum)
        stress = self.principle_stress_for_plotting(rnum, stype)

        if node_components:
            grid, ind = self._extract_node_components(node_components, sel_type_all)
            stress = stress[ind]
        elif element_components:
            grid, ind = self._extract_element_components(element_components)
            stress = stress[ind]
        else:
            grid = self.grid

        if 'stitle' not in kwargs:
            stype_stitle_map = {'1': 'Principal Stress 1',
                                '2': 'Principal Stress 2',
                                '3': 'Principal Stress 3',
                                'INT': 'Stress Intensity',
                                'EQV': 'von Mises Stress'}
            kwargs['stitle'] = stype_stitle_map[stype]

        return self._plot_point_scalars(stress, rnum=rnum, grid=grid, **kwargs)

    def cs_4x4(self, cs_cord, as_vtk_matrix=False):
        """ return a 4x4 transformation array for a given coordinate system """
        # assemble 4 x 4 matrix
        csys = self._c_systems[cs_cord]
        trans = np.hstack((csys['transformation matrix'],
                           csys['origin'].reshape(-1, 1)))
        matrix = trans_to_matrix(trans)

        if as_vtk_matrix:
            return matrix

        return pv.trans_from_matrix(matrix)

    def _plot_point_scalars(self, scalars, rnum=None, grid=None,
                            show_displacement=False, displacement_factor=1,
                            add_text=True, animate=False, nangles=100,
                            overlay_wireframe=False, node_components=None,
                            element_components=None,
                            sel_type_all=True, movie_filename=None,
                            max_disp=0.1, **kwargs):
        """Plot point scalars on active mesh.

        Parameters
        ----------
        scalars : np.ndarray
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

        add_text : bool, optional
            Adds information about the result when rnum is given.

        overlay_wireframe : bool, optional
            Overlay a wireframe of the original undeformed mesh.

        kwargs : keyword arguments
            Additional keyword arguments.  See ``help(pyvista.plot)``

        Returns
        -------
        cpos : list
            Camera position.
        """
        loop = kwargs.pop('loop', False)

        if grid is None:
            grid = self.grid

        disp = None
        if show_displacement and not animate:
            disp = self.nodal_solution(rnum)[1][:, :3]*displacement_factor
            if node_components:
                _, ind = self._extract_node_components(node_components, sel_type_all)
                disp = disp[ind]
            elif element_components:
                _, ind = self._extract_element_components(element_components)
                disp = disp[ind]
            new_points = disp + grid.points
            grid = grid.copy()
            grid.points = new_points

        elif animate:
            disp = self.nodal_solution(rnum)[1][:, :3]

        # extract mesh surface
        mapped_indices = None
        if 'vtkOriginalPointIds' in grid.point_arrays:
            mapped_indices = grid.point_arrays['vtkOriginalPointIds']

        mesh = grid.extract_surface()
        ind = mesh.point_arrays['vtkOriginalPointIds']
        if disp is not None:
            if mapped_indices is not None:
                disp = disp[mapped_indices][ind]
            else:
                disp = disp[ind]

            if animate:  # scale for max displacement
                disp /= (np.abs(disp).max()/max_disp)

        if scalars is not None:
            if scalars.ndim == 2:
                scalars = scalars[:, ind]
            else:
                scalars = scalars[ind]

            if animate:
                smax = np.abs(scalars).max()
                rng = kwargs.pop('rng', [-smax, smax])
            else:
                rng = kwargs.pop('rng', [scalars.min(), scalars.max()])
        else:
            rng = kwargs.pop('rng', None)

        cmap = kwargs.pop('cmap', 'jet')
        smooth_shading = kwargs.pop('smooth_shading', True)
        window_size = kwargs.pop('window_size', [1024, 768])
        full_screen = kwargs.pop('full_screen', False)
        notebook = kwargs.pop('notebook', False)
        off_screen = kwargs.pop('off_screen', None)
        cpos = kwargs.pop('cpos', None)
        screenshot = kwargs.pop('screenshot', None)
        color = kwargs.pop('color', 'w')
        interpolate_before_map = kwargs.pop('interpolate_before_map', True)
        interactive = kwargs.pop('interactive', True)
        stitle = kwargs.pop('stitle', None)

        # coordinate transformation for cyclic replication
        cs_cord = self._resultheader['csCord']
        if cs_cord > 1:
            matrix = self.cs_4x4(cs_cord, as_vtk_matrix=True)
            i_matrix = self.cs_4x4(cs_cord, as_vtk_matrix=True)
            i_matrix.Invert()
        else:
            matrix = vtk.vtkMatrix4x4()
            i_matrix = vtk.vtkMatrix4x4()

        plotter = pv.Plotter(off_screen=off_screen, notebook=notebook)

        # set axes
        if kwargs.pop('show_axes', True):
            plotter.add_axes()

        # set background
        plotter.background_color = kwargs.pop('background', None)

        n_sector = 1
        if np.any(scalars):
            if self.n_sector > 1:
                if scalars.ndim != 2:
                    n_sector = 1
                    scalars = [scalars]
                elif scalars.ndim == 1:
                    scalars = [scalars]
                else:
                    n_sector = self.n_sector
            elif scalars.ndim == 1:
                scalars = [scalars]
        else:
            if self.n_sector > 1:
                if kwargs.pop('full_rotor', True):
                    n_sector = self.n_sector
                    scalars = [None]*n_sector
                else:
                    scalars = [None]
            else:
                scalars = [None]

        rang = 360.0 / self.n_sector

        # remove extra keyword args
        kwargs.pop('node_components', None)
        kwargs.pop('sel_type_all', None)

        if overlay_wireframe:
            plotter.add_mesh(self.grid, color='w', style='wireframe',
                             opacity=0.5, **kwargs)

        for i in range(n_sector):
            copied_mesh = mesh.copy(False)
            actor = plotter.add_mesh(copied_mesh,
                                     color=color,
                                     scalars=scalars[i],
                                     rng=rng,
                                     smooth_shading=smooth_shading,
                                     interpolate_before_map=interpolate_before_map,
                                     stitle=stitle,
                                     cmap=cmap,
                                     **kwargs)

            # transform to standard position, rotate about Z axis,
            # transform back
            vtk_transform = vtk.vtkTransform()
            vtk_transform.RotateZ(rang*i)
            vtk_transform.Update()
            rot_matrix = vtk_transform.GetMatrix()

            if cs_cord > 1:
                temp_matrix = vtk.vtkMatrix4x4()
                rot_matrix.Multiply4x4(i_matrix, rot_matrix, temp_matrix)
                rot_matrix.Multiply4x4(temp_matrix, matrix, rot_matrix)
                vtk_transform.SetMatrix(rot_matrix)

            actor.SetUserTransform(vtk_transform)

        # plotter.add_scalar_bar()

        # NAN/missing data are white
        # plotter.renderers[0].SetUseDepthPeeling(1)  # <-- for transparency issues
        plotter.mapper.GetLookupTable().SetNanColor(1, 1, 1, 1)

        if cpos:
            plotter.camera_position = cpos

        if movie_filename:
            if movie_filename.strip()[-3:] == 'gif':
                plotter.open_gif(movie_filename)
            else:
                plotter.open_movie(movie_filename)

        # add table
        if add_text and rnum is not None:
            result_text = self.text_result_table(rnum)
            actor = plotter.add_text(result_text, font_size=20)

        if animate:
            orig_pts = copied_mesh.points.copy()
            plotter.show(interactive=False, auto_close=False,
                         interactive_update=not off_screen)

            self._animating = True

            def q_callback():
                """exit when user wants to leave"""
                self._animating = False

            plotter.add_key_event("q", q_callback)

            first_loop = True
            cached_normals = [None for _ in range(nangles)]
            while self._animating:
                for j, angle in enumerate(np.linspace(0, np.pi*2, nangles + 1)[:-1]):
                    mag_adj = np.sin(angle)
                    if scalars[0] is not None:
                        copied_mesh.active_scalars[:] = scalars[0]*mag_adj

                    copied_mesh.points[:] = orig_pts + disp*mag_adj

                    # normals have to be updated on the fly
                    if smooth_shading:
                        if cached_normals[j] is None:
                            copied_mesh.compute_normals(cell_normals=False,
                                                        inplace=True)
                            cached_normals[j] = copied_mesh.point_arrays['Normals']
                        else:
                            copied_mesh.point_arrays['Normals'][:] = cached_normals[j]

                    if add_text:
                        # 2 maps to vtk.vtkCornerAnnotation.UpperLeft
                        plotter.textActor.SetText(2, '%s\nPhase %.1f Degrees' %
                                                  (result_text, (angle*180/np.pi)))

                    # at max supported framerate
                    plotter.update(1, force_redraw=True)
                    if not self._animating:
                        break

                    if movie_filename and first_loop:
                        plotter.write_frame()

                first_loop = False
                if not loop:
                    break
            plotter.close()

        elif screenshot:
            cpos = plotter.show(auto_close=False, interactive=interactive,
                                window_size=window_size,
                                full_screen=full_screen)
            if screenshot is True:
                img = plotter.screenshot()
            else:
                plotter.screenshot(screenshot)
            plotter.close()
        else:
            cpos = plotter.show(interactive=interactive,
                                window_size=window_size,
                                full_screen=full_screen)

        if screenshot is True:
            return cpos, img

        return cpos

    def text_result_table(self, rnum):
        """ Returns a text result table for plotting """
        ls_table = self._resultheader['ls_table']
        timevalue = self.time_values[rnum]
        text = 'Cumulative Index: {:3d}\n'.format(ls_table[rnum, 2])
        if self._resultheader['nSector'] > 1:
            hindex = self._resultheader['hindex'][rnum]
            text += 'Harmonic Index    {:3d}\n'.format(hindex)
        text += 'Loadstep:         {:3d}\n'.format(ls_table[rnum, 0])
        text += 'Substep:          {:3d}\n'.format(ls_table[rnum, 1])
        text += 'Time Value:     {:10.4f}'.format(timevalue)

        return text

    def principle_stress_for_plotting(self, rnum, stype):
        """
        returns stress used to plot

        """
        stress_types = ['1', '2', '3', 'INT', 'EQV']
        if stype.upper() not in stress_types:
            raise Exception('Stress type not in \n' + str(stress_types))

        sidx = stress_types.index(stype)

        _, stress = self.principal_nodal_stress(rnum)
        return stress[:, sidx]

    def plot_nodal_stress(self, rnum, comp=None,
                          show_displacement=False,
                          displacement_factor=1,
                          node_components=None,
                          element_components=None,
                          sel_type_all=True, **kwargs):
        """Plots the stresses at each node in the solution.

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        comp : str, optional
            Thermal strain component to display.  Available options:
            - ``"X"``
            - ``"Y"``
            - ``"Z"``
            - ``"XY"``
            - ``"YZ"``
            - ``"XZ"``

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

        kwargs : keyword arguments
            Additional keyword arguments.  See help(pyvista.plot)

        Returns
        -------
        cpos : list
            3 x 3 vtk camera position.

        Examples
        --------
        Plot the X component nodal stress while showing displacement.

        >>> rst.plot_nodal_stress(0, comp='x', show_displacement=True)
        """
        available_comps = ['X', 'Y', 'Z', 'XY', 'YZ', 'XZ']

        if comp is None:
            raise ValueError('Missing "comp" parameter.  Please select'
                             ' from the following:\n%s' % available_comps)
        kwargs['stitle'] = '%s Component Nodal Stress' % comp
        self._plot_nodal_result(rnum, 'ENS', comp, available_comps,
                                show_displacement,
                                displacement_factor, node_components,
                                element_components,
                                sel_type_all, **kwargs)

    def save_as_vtk(self, filename, rsets=None, result_types=['ENS']):
        """Writes results to a vtk readable file.

        The file extension will select the type of writer to use.
        ``'.vtk'`` will use the legacy writer, while ``'.vtu'`` will
        select the VTK XML writer.

        Parameters
        ----------
        filename : str
            Filename of grid to be written.  The file extension will
            select the type of writer to use.  ``'.vtk'`` will use the
            legacy writer, while ``'.vtu'`` will select the VTK XML
            writer.

        rsets : collections.Iterable
            List of result sets to write.  For example ``range(3)``

        result_types : list
            Result type to write.  For example ``['ENF', 'ENS']``
            List of some or all of the following:

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

        Notes
        -----
        Binary files write much faster than ASCII, but binary files
        written on one system may not be readable on other systems.
        Binary can only be selected for the legacy writer.

        Examples
        --------
        Write in binary

        >>> rst.save_as_vtk('results.vtk')

        Write using the xml writer

        >>> rst.save_as_vtk('results.vtu')

        Write only nodal and elastic strain for the first result

        >>> rst.save_as_vtk('results.vtk', [0], ['EEL', 'EPL']

        """
        # Copy grid as to not write results to original object
        grid = self.grid.copy()

        if rsets is None:
            rsets = range(self.nsets)
        elif isinstance(rsets, int):
            rsets = [rsets]
        elif not isinstance(rsets, Iterable):
            raise TypeError('rsets must be an iterable like [0, 1, 2] or range(3)')

        if result_types is None:
            result_types = ELEMENT_INDEX_TABLE_KEYS
        elif not isinstance(result_types, list):
            raise TypeError('result_types must be a list of solution types')
        else:
            for item in result_types:
                if item not in ELEMENT_INDEX_TABLE_KEYS:
                    raise ValueError('Invalid result type "%s" % item')

        try:
            from tqdm import tqdm
            pbar = tqdm(total=len(rsets), desc='Saving to file')
        except ImportError:
            pbar = None

        for i in rsets:
            # Nodal results
            _, val = self.nodal_solution(i)
            grid.point_arrays['Nodal Solution {:d}'.format(i)] = val

            # Nodal results
            for rtype, rtype_desc in self.available_results.items():
                if rtype in result_types:
                    _, values = self._nodal_result(i, rtype)
                    grid.point_arrays['{:s} {:d}'.format(rtype_desc, i)] = values

            if pbar is not None:
                pbar.update(1)

        grid.save(filename)
        if pbar is not None:
            pbar.close()

    def write_tables(self, filename):
        """Write binary tables to ASCII.  Assumes int32

        Parameters
        ----------
        filename : str
            Filename to write the tables to.

        Examples
        --------
        >>> rst.write_tables('tables.txt')
        """
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

        elif isinstance(user_input, (list, tuple)):
            if len(user_input) != 2:
                raise Exception('Input must contain (step, loadstep) using  ' +
                                '1 based indexing (e.g. (1, 1)).')
            ls_table = self._resultheader['ls_table']
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

    def __str__(self):
        rst_info = ['PyANSYS MAPDL Result file object']
        keys = ['title', 'subtitle', 'units']
        for key in keys:
            value = self._resultheader[key]
            if value:
                rst_info.append('{:<12s}: {:s}'.format(key.capitalize(), value))

        value = self._resultheader['verstring']
        rst_info.append('{:<12s}: {:s}'.format('Version', value))

        value = str(self._resultheader['nSector'] > 1)
        rst_info.append('{:<12s}: {:s}'.format('Cyclic', value))

        value = self._resultheader['nsets']
        rst_info.append('{:<12s}: {:d}'.format('Result Sets', value))

        value = self._resultheader['nnod']
        rst_info.append('{:<12s}: {:d}'.format('Nodes', value))

        value = self._resultheader['nelm']
        rst_info.append('{:<12s}: {:d}'.format('Elements', value))

        rst_info.append('\nAvailable Results:')
        for key, value in self.available_results.items():
            rst_info.append('{:<4s}: {:s}'.format(key, value))

        return '\n'.join(rst_info)

    def _nodal_result(self, rnum, result_type):
        """Generic load nodal result

        Parameters
        ----------
        rnum : int
            Result number.

        result_type : int
            EMS: misc. data
            ENF: nodal forces
            ENS: nodal stresses
            ENG: volume and energies
            EGR: nodal gradients
            EEL: elastic strains
            EPL: plastic strains
            ECR: creep strains
            ETH: thermal strains
            EUL: euler angles
            EFX: nodal fluxes
            ELF: local forces
            EMN: misc. non-sum values
            ECD: element current densities
            ENL: nodal nonlinear data
            EHC: calculated heat
            EPT: element temperatures
            ESF: element surface stresses
            EDI: diffusion strains
            ETB: ETABLE items(post1 only
            ECT: contact data
            EXY: integration point locations
            EBA: back stresses
            ESV: state variables
            MNL: material nonlinear record

        Returns
        -------
        nnum : np.ndarray
            ANSYS node numbers

        result : np.ndarray
            Array of result data
        """
        # element header
        rnum = self.parse_step_substep(rnum)
        ele_ind_table, nodstr, etype, ptr_off = self._element_solution_header(rnum)

        result_type = result_type.upper()
        if self._resultheader['rstsprs'] == 0 and result_type == 'ENS':
            nitem = 11
        elif result_type in ELEMENT_RESULT_NCOMP:
            nitem = ELEMENT_RESULT_NCOMP[result_type]
        else:
            nitem = 1

        result_index = ELEMENT_INDEX_TABLE_KEYS.index(result_type)

        # Element types for nodal averaging
        cells, offset = vtk_cell_info(self.grid)
        data, ncount = _binary_reader.read_nodal_values(self.filename,
                                                        self.grid.celltypes,
                                                        ele_ind_table,
                                                        offset,
                                                        cells,
                                                        nitem,
                                                        self.grid.number_of_points,
                                                        nodstr,
                                                        etype,
                                                        self.geometry.etype,
                                                        result_index,
                                                        ptr_off)

        if result_type == 'ENS' and nitem != 6:
            data = data[:, :6]

        nnum = self.grid.point_arrays['ansys_node_num']
        if np.isnan(data).all():
            raise ValueError('Result file contains no %s records for result %d' %
                             (element_index_table_info[result_type.upper()], rnum))

        # average across nodes
        result = data/ncount.reshape(-1, 1)
        return nnum, result

    def nodal_stress(self, rnum):
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

        Returns
        -------
        nnum : numpy.ndarray
            Node numbers of the result.

        stress : numpy.ndarray
            Stresses at X, Y, Z, XY, YZ, and XZ Sxz averaged at each corner
            node.

        Examples
        --------
        >>> import pyansys
        >>> rst = pyansys.read_binary('file.rst')
        >>> nnum, stress = rst.nodal_stress(0)

        Notes
        -----
        Nodes without a stress value will be NAN.
        Equivalent ANSYS command: PRNSOL, S
        """
        return self._nodal_result(rnum, 'ENS')

    def nodal_temperature(self, rnum):
        """Retrieves the temperature for each node in the
        solution.

        The order of the results corresponds to the sorted node
        numbering.

        Equivalent MAPDL command: PRNSOL, TEMP

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

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
        """
        nnum, temp = self._nodal_result(rnum, 'EPT')
        temp = temp.ravel()
        return nnum, temp

    def plot_nodal_temperature(self, rnum, show_displacement=False,
                               displacement_factor=1, node_components=None,
                               element_components=None, sel_type_all=True,
                               **kwargs):
        """Plot nodal temperature

        Parameters
        ----------
        rnum : int
            Result number

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

        **kwargs : keyword arguments
            Optional keyword arguments.  See help(pyvista.plot)

        Examples
        --------
        Plot thermal strain of a sample file

        >>> import pyansys
        >>> result = pyansys.read_binary('file.rst')
        >>> result.plot_nodal_temperature(0)

        Plot while showing edges and disabling lighting

        >>> result.plot_nodal_temperature(0, show_edges=True, lighting=False)
        """
        _, scalars = self.nodal_temperature(rnum)

        grid = self.grid
        if node_components:
            grid, ind = self._extract_node_components(node_components, sel_type_all)
            scalars = scalars[ind]
        elif element_components:
            grid, ind = self._extract_element_components(element_components)
            scalars = scalars[ind]

        return self._plot_point_scalars(scalars, grid=grid, rnum=rnum,
                                        show_displacement=show_displacement,
                                        displacement_factor=displacement_factor,
                                        stitle='Nodal Tempature',
                                        **kwargs)

    def nodal_thermal_strain(self, rnum):
        """Nodal component plastic strains.  This record contains
        strains in the order X, Y, Z, XY, YZ, XZ, EQV, and eswell
        (element swelling strain).  Plastic strains are always values
        at the integration points moved to the nodes.

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        Returns
        -------
        nnum : np.ndarray
            ANSYS node numbers.

        thermal_strain : np.ndarray
            Nodal component plastic strains.  Array is in the order
            X, Y, Z, XY, YZ, XZ, EQV, ESWELL

        Examples
        --------
        Load the nodal thermal strain for the first solution

        >>> import pyansys
        >>> rst = pyansys.read_binary('file.rst')
        >>> nnum, thermal_strain = rst.nodal_thermal_strain(0)
        """
        return self._nodal_result(rnum, 'ETH')

    def plot_nodal_thermal_strain(self, rnum, comp,
                                  stitle='Nodal Thermal Strain',
                                  show_displacement=False,
                                  displacement_factor=1,
                                  node_components=None,
                                  element_components=None,
                                  sel_type_all=True, **kwargs):
        """Plot nodal component plastic strains.

        Parameters
        ----------
        rnum : int
            Result number

        comp : str, optional
            Thermal strain component to display.  Available options:
            - ``"X"``
            - ``"Y"``
            - ``"Z"``
            - ``"XY"``
            - ``"YZ"``
            - ``"XZ"``
            - ``"EQV"``
            - ``"ESWELL"``

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

        **kwargs : keyword arguments
            Optional keyword arguments.  See ``help(pyvista.plot)``

        Examples
        --------
        Plot thermal strain for result 0 of verification manual example 33

        >>> import pyansys
        >>> result = pyansys.download_verification_result(33)
        >>> result.plot_nodal_thermal_strain(0)
        """
        available_comps = ['X', 'Y', 'Z', 'XY', 'YZ', 'XZ', 'EQV', 'ESWELL']
        return self._plot_nodal_result(rnum, 'ETH', comp, available_comps,
                                       show_displacement=show_displacement,
                                       displacement_factor=displacement_factor,
                                       node_components=node_components,
                                       sel_type_all=sel_type_all,
                                       stitle=stitle,
                                       **kwargs)

    def nodal_elastic_strain(self, rnum):
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

        Returns
        -------
        nnum : np.ndarray
            ANSYS node numbers.

        elastic_strain : np.ndarray
            Nodal component elastic strains.  Array is in the order
            X, Y, Z, XY, YZ, XZ, EEL.

        Examples
        --------
        Load the nodal elastic strain for the first solution.

        >>> import pyansys
        >>> rst = pyansys.read_binary('file.rst')
        >>> nnum, elastic_strain = rst.nodal_elastic_strain(0)
        """
        return self._nodal_result(rnum, 'EEL')

    def plot_nodal_elastic_strain(self, rnum, comp,
                                  stitle='Nodal Elastic Strain',
                                  show_displacement=False,
                                  displacement_factor=1,
                                  node_components=None,
                                  element_components=None,
                                  sel_type_all=True, **kwargs):
        """Plot nodal elastic strain.

        Parameters
        ----------
        rnum : int
            Result number

        comp : str, optional
            Thermal strain component to display.  Available options:
            - ``"X"``
            - ``"Y"``
            - ``"Z"``
            - ``"XY"``
            - ``"YZ"``
            - ``"XZ"``
            - ``"EQV"``

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

        **kwargs : keyword arguments
            Optional keyword arguments.  See help(pyvista.plot)

        Examples
        --------
        Plot thermal strain for a static pontoon model

        >>> import pyansys
        >>> result = pyansys.download_pontoon()
        >>> result.plot_nodal_elastic_strain(0)
        """
        available_comps = ['X', 'Y', 'Z', 'XY', 'YZ', 'XZ', 'EQV']
        stitle = ' '.join([comp.upper(), stitle])
        return self._plot_nodal_result(rnum, 'EEL',
                                       comp,
                                       available_comps,
                                       show_displacement=show_displacement,
                                       displacement_factor=displacement_factor,
                                       node_components=node_components,
                                       element_components=element_components,
                                       sel_type_all=sel_type_all,
                                       stitle=stitle,
                                       **kwargs)

    def nodal_plastic_strain(self, rnum):
        """Nodal component plastic strains.  This record contains
        strains in the order X, Y, Z, XY, YZ, XZ, EQV.  

        Plastic strains are always values at the integration points
        moved to the nodes.

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        Returns
        -------
        nnum : np.ndarray
            ANSYS node numbers.

        plastic_strain : np.ndarray
            Nodal component plastic strains.  Array is in the order
            X, Y, Z, XY, YZ, XZ, EEL.

        Examples
        --------
        Load the nodal plastic strain for the first solution.

        >>> import pyansys
        >>> rst = pyansys.read_binary('file.rst')
        >>> nnum, plastic_strain = rst.nodal_plastic_strain(0)
        """
        return self._nodal_result(rnum, 'EPL')

    def plot_nodal_plastic_strain(self, rnum, comp,
                                  stitle='Nodal Plastic Strain',
                                  show_displacement=False,
                                  displacement_factor=1,
                                  node_components=None,
                                  element_components=None,
                                  sel_type_all=True, **kwargs):
        """Plot nodal component plastic strains.

        Parameters
        ----------
        rnum : int
            Result number

        comp : str, optional
            Thermal strain component to display.  Available options:
            - ``"X"``
            - ``"Y"``
            - ``"Z"``
            - ``"XY"``
            - ``"YZ"``
            - ``"XZ"``
            - ``"EQV"``

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

        **kwargs : keyword arguments
            Optional keyword arguments.  See help(pyvista.plot)

        Examples
        --------
        Plot plastic strain for a static pontoon model

        >>> import pyansys
        >>> result = pyansys.download_pontoon()
        >>> result.plot_nodal_plastic_strain(0)

        """
        available_comps = ['X', 'Y', 'Z', 'XY', 'YZ', 'XZ', 'EQV']
        stitle = ' '.join([comp.upper(), stitle])
        return self._plot_nodal_result(rnum, 'EPL',
                                       comp,
                                       available_comps,
                                       show_displacement=show_displacement,
                                       displacement_factor=displacement_factor,
                                       node_components=node_components,
                                       sel_type_all=sel_type_all,
                                       stitle=stitle,
                                       **kwargs)

    def _plot_nodal_result(self, rnum, result_type, comp, available_comps,
                           show_displacement=False, displacement_factor=1,
                           node_components=None, element_components=None,
                           sel_type_all=True, **kwargs):
        """Plot nodal results"""
        comp = comp.upper()
        if comp not in available_comps:
            raise ValueError('Invalid component.  Pick one of the following: %s' %
                             str(available_comps))
        component_index = available_comps.index(comp)

        _, result = self._nodal_result(rnum, result_type)
        scalars = result[:, component_index]

        if node_components:
            grid, ind = self._extract_node_components(node_components, sel_type_all)
            scalars = scalars[ind]
        elif element_components:
            grid, ind = self._extract_element_components(element_components)
            scalars = scalars[ind]
        else:
            grid = self.grid

        return self._plot_point_scalars(scalars, grid=grid, rnum=rnum,
                                        show_displacement=show_displacement,
                                        displacement_factor=displacement_factor,
                                        **kwargs)

    def _animate_time_solution(self, result_type, index=0, frame_rate=10,
                               show_displacement=True, displacement_factor=1,
                               off_screen=None):
        """Animate time solution result"""
        # load all results
        results = []
        for i in range(self.nsets):
            results.append(self._nodal_result(i, result_type)[1][:, index])

        if show_displacement:
            disp = []
            for i in range(self.nsets):
                disp.append(self.nodal_solution(i)[1][:, :3]*displacement_factor)

        mesh = self.grid.copy()
        results = np.array(results)
        if np.all(np.isnan(results)):
            raise ValueError('Result file contains no %s records' %
                             element_index_table_info[result_type.upper()])

        # prepopulate mesh with data
        mesh['data'] = results[0]

        # set default range
        rng = [results.min(), results.max()]
        t_wait = 1/frame_rate

        def q_callback():
            """exit when user wants to leave"""
            self._animating = False

        self._animating = True
        def plot_thread():
            plotter = pv.Plotter(off_screen=off_screen)
            plotter.add_key_event("q", q_callback)
            plotter.add_mesh(mesh, scalars='data', rng=rng)
            plotter.show(auto_close=False, interactive_update=True, interactive=False)
            text_actor = plotter.add_text('Result 1')
            while self._animating:
                for i in range(self.nsets):
                    mesh['data'] = results[i]

                    if show_displacement:
                        mesh.points = self.grid.points + disp[i]

                    # if interactive:
                    plotter.update(30, force_redraw=True)
                    if hasattr(text_actor, 'SetInput'):
                        text_actor.SetInput('Result %d' % (i + 1))
                    else:
                        text_actor.SetText(0, 'Result %d' % (i + 1))

                    time.sleep(t_wait)

                if off_screen:
                    break

            plotter.close()

        thread = Thread(target=plot_thread)
        thread.start()

    @property
    def available_results(self):
        """Prints available element result types and returns those keys"""
        try:
            ele_ind_table, _, _, ptr_off = self._element_solution_header(0)
        except ValueError:
            return {}

        # get the keys from the first element (not perfect...)
        n_rec = len(ELEMENT_INDEX_TABLE_KEYS)
        mask = self.read_record(ele_ind_table[0] + ptr_off)[:n_rec] > 0
        keys = list(compress(ELEMENT_INDEX_TABLE_KEYS, mask))
        return {key: element_index_table_info[key] for key in keys}


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


def trans_to_matrix(trans):
    """ Convert a numpy.ndarray to a vtk.vtkMatrix4x4 """
    matrix = vtk.vtkMatrix4x4()
    for i in range(trans.shape[0]):
        for j in range(trans.shape[1]):
            matrix.SetElement(i, j, trans[i, j])
    return matrix


def transform(points, trans):
    """In-place 3d transformation of a points array given a 4x4
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

    _binary_reader.affline_transform(points, trans)


def merge_two_dicts(x, y):
    merged = x.copy()   # start with x's keys and values
    merged.update(y)    # modifies z with y's keys and values & returns None
    return merged
