"""Handle result files from a distributed MAPDL analysis"""
from inspect import currentframe
import glob
import os
from functools import wraps

import pyvista as pv
import numpy as np
from vtk import vtkAppendFilter

from pyansys.misc import is_float, vtk_cell_info
from pyansys.mesh import Mesh
from pyansys.rst import Result, ELEMENT_INDEX_TABLE_KEYS
from pyansys.errors import NoDistributedFiles
from pyansys._binary_reader import (read_nodal_values_dist,
                                    populate_surface_element_result)
from pyansys._rst_keys import element_index_table_info


def find_dis_files(main_file):
    """Find the individual distributed result files given a main result file"""
    basename = os.path.basename(main_file)
    jobname = basename[:basename.rfind('0')]
    ext = basename.split('.')[1]
    dirname = os.path.dirname(main_file)

    if dirname is None:
        dirname = os.getcwd()

    # get all files matching the jobname
    filenames = {}
    for filename in glob.glob('%s/%s*.%s' % (dirname, jobname, ext)):
        index = os.path.basename(filename).replace(jobname, '')[:-4]
        if is_float(index):
            filenames[int(index)] = filename

    if not filenames:
        raise NoDistributedFiles

    if max(filenames.keys()) + 1 != len(filenames):
        raise FileNotFoundError('Unable to find all the result files of a '
                                'distributed result')

    return filenames


class DistributedResult(Result):
    """Distributed result file

    Parameters
    ----------
    main_file : str
        Path of main result file

    """

    def __init__(self, main_file):
        """Initialize from a series of distributed files"""
        # find remainder of distributed results
        filenames = find_dis_files(main_file)

        # load initial result
        super().__init__(main_file, read_mesh=False)
        self._results = [Result(main_file)]

        # Global number of nodes must not equal the number of nodes in this file
        if not self._main_result._is_distributed:
            raise RuntimeError('Result file is not part of a distributed result')

        if not self._main_result._is_main:  # pragma: no cover
            raise RuntimeError('DistributedResult must be created from the main '
                               'result file')

        # load and verify
        ptr = self._main_result._resultheader['ptrGNOD']
        gl_nnum = self._main_result.read_record(ptr)

        mask = np.in1d(gl_nnum, self._main_result.mesh.nnum, assume_unique=True)
        for index in range(1, len(filenames)):
            result = Result(filenames[index])
            new_mask = np.in1d(gl_nnum, result.mesh.nnum, assume_unique=True)
            if not new_mask.any():  # pragma: no cover
                raise RuntimeError('File %s not part of the distributed result'
                                   % filenames[index])
            mask += new_mask
            self._results.append(result)

        if not np.all(mask):
            filenames = '\n'.join([result.filename for result in self._results])
            raise FileNotFoundError('Total nodes loaded from the individual result '
                                    'files does not match the number in the global '
                                    'index.  \n\nResult files found include:\n\n%s' %
                                    filenames)

        # assemble the global mesh
        vtkappend = vtkAppendFilter()
        vtkappend.MergePointsOn()
        st = 0
        for i, result in enumerate(self._results):
            # map the merged node numbering with the individual mappings
            result.grid['_dist_idx'] = np.arange(st, st + result.grid.n_points)
            _result_idx = np.empty(result.grid.n_cells, np.int32)
            _result_idx[:] = i
            result.grid.cell_arrays['_result_idx'] = _result_idx
            st += result.grid.n_points
            vtkappend.AddInputData(result.grid)

        self._total_sol_nodes = st  # total nodes in all result files

        vtkappend.Update()
        grid = pv.wrap(vtkappend.GetOutput())
        # nodes are not sorted here

        # Map nodes from individual results to the global mesh
        self._glb_idx = grid['_dist_idx']

        # start of each section of the grid
        # elem_split_ind = np.diff(self.grid['_result_idx']).nonzero()[0]
        # self._elem_split = np.hstack(([0], elem_split_ind))

        elem = np.hstack(result.mesh._elem for result in self._results)
        glb_elem_off = []
        for result in self._results:
            elem_off = result.mesh._elem_off
            if len(glb_elem_off):
                off = glb_elem_off[-1][-1]
                glb_elem_off.append(elem_off[1:] + off)
            else:
                glb_elem_off.append(elem_off)

        # TODO: Add node and element components
        # resort node numbers
        self._dist_sort_idx = np.argsort(grid['ansys_node_num'])
        self._sorted_nnum = grid['ansys_node_num'][self._dist_sort_idx]
        nodes = grid.points[self._dist_sort_idx]

        glb_elem_off = np.hstack(glb_elem_off)
        self._mesh = Mesh(self._sorted_nnum, nodes, elem, glb_elem_off,
                          self._main_result.mesh.ekey)
                          # node_comps=ncomp, elem_comps=ecomp)

        self.quadgrid = self._mesh._parse_vtk(fix_midside=False)
        self.grid = self.quadgrid.linear_copy()

        # self._neqv = self._resultheader['neqv']  # may not need this
        self._eeqv = self.grid.cell_arrays['ansys_elem_num']

    @property
    def _main_result(self):
        """Main result instance"""
        return self._results[0]

    @property
    @wraps(Result.mesh)
    def mesh(self):
        """Assembled global mesh is an assembly of the individual result file meshes"""
        return self._mesh

    @wraps(Result.nodal_solution)
    def nodal_solution(self, *args, **kwargs):
        return self._dis_solution(currentframe().f_code.co_name, *args, **kwargs)

    def _dis_solution(self, func_name, *args, **kwargs):
        """Get the distributed solution for a given function"""
        glb_nnum = []
        glb_sol = []
        for result in self._results:
            func = getattr(result, func_name)
            rst_nnum, rst_sol = func(*args, **kwargs)
            glb_nnum.append(rst_nnum)
            glb_sol.append(rst_sol)

        # resort and organize stacked solutions
        glb_sol = np.vstack(glb_sol)
        if glb_sol.shape[0] == self._total_sol_nodes:
            # not all values from the global solution are unique and
            # we need to pare this down (due to merging to meshes)
            glb_sol = glb_sol[self._glb_idx]
            return self._sorted_nnum, glb_sol[self._dist_sort_idx]

            # return self.mesh.nnum, glb_sol
        else:  # limited subset of solution
            # must remap due to how the subset of nodes relate to the
            # global mesh solution
            nnum = np.hstack(glb_nnum)
            u_nnum, idx = np.unique(nnum, return_index=True)
            return u_nnum, glb_sol[idx]

    def _nodal_result(self, rnum, result_type, **kwargs):
        """Load generic nodal result

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
        # check result exists
        if not self.available_results[result_type]:
            raise ValueError('Result %s is not available in this result file'
                             % result_type)

        # element header
        rnum = self.parse_step_substep(rnum)

        result_type = result_type.upper()
        nitem = self._result_nitem(rnum, result_type)
        result_index = ELEMENT_INDEX_TABLE_KEYS.index(result_type)

        # Element types for nodal averaging from the global mesh
        n_points = self.grid.n_points
        cells, offset = vtk_cell_info(self.grid)
        data = np.zeros((n_points, nitem), np.float64)
        ncount = np.zeros(n_points, np.int32)

        c = 0  # global cell index counter
        for result in self._results:
            ele_ind_table, nodstr, etype, ptr_off = result._element_solution_header(rnum)
            # we return c here since it is copied to C, not passed by reference
            c = read_nodal_values_dist(result.filename,
                                       self.grid.celltypes,
                                       ele_ind_table,
                                       offset,
                                       cells,
                                       nitem,
                                       n_points,
                                       nodstr,
                                       etype,
                                       self._mesh.etype,
                                       result_index,
                                       ptr_off,
                                       ncount,
                                       data,
                                       c)

        if result_type == 'ENS' and nitem != 6:
            data = data[:, :6]

        if not np.any(ncount):
            raise ValueError('Result file contains no %s records for result %d' %
                             (element_index_table_info[result_type.upper()], rnum))

        # average across nodes
        data /= ncount.reshape(-1, 1)
        return self.grid.point_arrays['ansys_node_num'], data

    @wraps(Result.element_solution_data)
    def element_solution_data(self, *args, **kwargs):
        """Accumulate the element solution individual results from each result"""
        sort = kwargs.get('sort', True)
        glb_element_data = []
        for result in self._results:
            element_data = result.element_solution_data(*args, is_dist_rst=True,
                                                        **kwargs)
            glb_element_data.extend(element_data)

        # Assemble and sort (args[0] is rnum)
        _, nodstr, etype, _ = self._element_solution_header(args[0])

        enum = self._eeqv
        enode = []
        nnode = nodstr[etype]
        if sort:
            sidx = np.argsort(enum)
            enum = enum[sidx]
            glb_element_data = [glb_element_data[i] for i in sidx]

            for i in sidx:
                enode.append(self._mesh.elem[i][10:10+nnode[i]])

        else:
            for i in range(enum.size):
                enode.append(self._mesh.elem[i][10:10+nnode[i]])

        return enum, glb_element_data, enode

    @wraps(Result.element_stress)
    def element_stress(self, *args, **kwargs):
        """Accumulate the element solution individual results from each result"""
        sort = kwargs.get('sort', True)
        glb_stress = []
        for result in self._results:
            element_data = result.element_stress(*args, is_dist_rst=True, **kwargs)
            glb_stress.extend(element_data)

        # Assemble and sort (args[0] is rnum)
        _, nodstr, etype, _ = self._element_solution_header(args[0])

        enum = self._eeqv
        enode = []
        nnode = nodstr[etype]

        if sort:
            sidx = np.argsort(enum)
            enum = enum[sidx]
            glb_element_data = [glb_stress[i] for i in sidx]

            for i in sidx:
                enode.append(self._mesh.elem[i][10:10+nnode[i]])

        else:
            for i in range(enum.size):
                enode.append(self._mesh.elem[i][10:10+nnode[i]])

        return enum, glb_element_data, enode

    def plot_element_result(self, rnum, result_type, item_index,
                            in_element_coord_sys=False, **kwargs):
        """Plot an element result.

        Parameters
        ----------
        rnum : int
            Result number.

        result_type : str
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

        item_index : int
            Index of the data item for each node within the element.

        in_element_coord_sys : bool, optional
            Returns the results in the element coordinate system.
            Default False and will return the results in the global
            coordinate system.

        Returns
        -------
        nnum : np.ndarray
            ANSYS node numbers

        result : np.ndarray
            Array of result data

        Examples
        --------
        # >>> rst.plot_element_result(
        """
        # check result exists
        result_type = result_type.upper()
        if not self.available_results[result_type]:
            raise ValueError('Result %s is not available in this result file'
                             % result_type)

        if result_type not in ELEMENT_INDEX_TABLE_KEYS:
            raise ValueError('Result "%s" is not an element result' % result_type)

        bsurfs = []
        for result in self._results:
            bsurf = result._extract_surface_element_result(rnum,
                                                           result_type,
                                                           item_index,
                                                           in_element_coord_sys)
            bsurfs.append(bsurf)

        desc = self.available_results.description[result_type].capitalize()
        kwargs.setdefault('stitle', desc)
        return pv.plot(bsurfs, scalars='_scalars', **kwargs)
