"""Handle result files from a distributed MAPDL analysis"""
import inspect
import glob
import os
from functools import wraps

from pyansys.mesh import Mesh
import pyvista as pv
import numpy as np
from vtk import vtkAppendFilter

from pyansys.misc import is_float
from pyansys.rst import Result


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

        if not self._main_result._is_main:
            raise RuntimeError('DistributedResult must be created from the main '
                               'result file')

        # load and verify
        ptr = self._main_result._resultheader['ptrGNOD']
        gl_nnum = self._main_result.read_record(ptr)

        mask = np.in1d(gl_nnum, self._main_result.mesh.nnum, assume_unique=True)
        for index in range(1, len(filenames)):
            result = Result(filenames[index])
            new_mask = np.in1d(gl_nnum, result.mesh.nnum, assume_unique=True)
            if not new_mask.any():
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
            st += result.grid.n_points
            vtkappend.AddInputData(result.grid)

        vtkappend.Update()
        self.grid = pv.wrap(vtkappend.GetOutput())
        # nodes are not sorted here

        elem = np.hstack(result.mesh._elem for result in self._results)
        glb_elem_off = []
        for result in self._results:
            elem_off = result.mesh._elem_off
            if len(glb_elem_off):
                off = glb_elem_off[-1][-1]
                glb_elem_off.append(elem_off[1:] + off)
            else:
                glb_elem_off.append(elem_off)

        glb_elem_off = np.hstack(glb_elem_off)
        self._mesh = Mesh(self.grid['ansys_node_num'], self.grid.points,
                          elem, glb_elem_off, self._main_result.mesh.ekey)
                          # node_comps=ncomp, elem_comps=ecomp)

        # from the sorted individual mappings
        self._dist_sort_idx = np.argsort(self.grid['ansys_node_num'])
        self._glb_idx = self.grid['_dist_idx']

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
        this_function_name = inspect.currentframe().f_code.co_name
        if 'plot_' in inspect.stack()[2][3]:
            # Sorting must be disabled on plotting functions
            kwargs['sort'] = False
        return self._dis_solution(this_function_name, *args, **kwargs)

    def _dis_solution(self, func_name, *args, **kwargs):
        """Get the distributed solution for a given function"""
        sort = kwargs.pop('sort', True)
        glb_sol = []
        for result in self._results:
            func = getattr(result, func_name)
            glb_sol.append(func(*args, **kwargs)[1])

        sol = np.vstack(glb_sol)[self._glb_idx]
        if sort:
            return self.mesh.nnum, sol[self._dist_sort_idx]
        else:
            return self.mesh.nnum[self._dist_sort_idx], sol


# testing...
# rst = DistributedResult('/tmp/ansys_pdxxfbahxy/file0.rth')
# nnum, sol = rst.nodal_solution(0)
# rst.plot_nodal_solution(0)

# rst.nodal_stress(0)

# self = rst

# all_nnum = np.hstack([result.mesh.nnum for result in self._results])
