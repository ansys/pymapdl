"""
Cyclic result files are distributed differently than non-cyclic
results.  It appears that the cyclic results are organized such that
they contain the full geometry and a portion of the harmonic indices
for each solution.

The DistributedCyclicResult must act as a mapper to correctly map the
cumulative result to the correct individual result file.

"""


from pyansys.dis_result import find_dis_files
from pyansys.cyclic_reader import CyclicResult

import numpy as np

class DistributedCyclicResult(CyclicResult):
    """Distributed cyclic result file

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
        super().__init__(main_file)
        self._results = [CyclicResult(main_file)]

        # # Global number of nodes must not equal the number of nodes in this file
        # if not self._main_result._is_distributed:
        #     raise RuntimeError('Result file is not part of a distributed result')

        if not self._main_result._is_main:
            raise RuntimeError('DistributedResult must be created from the main '
                               'result file')

        # load and verify
        ptr = self._main_result._resultheader['ptrGNOD']
        gl_nnum = self._main_result.read_record(ptr)

        # mask = np.in1d(gl_nnum, self._main_result.mesh.nnum, assume_unique=True)
        # for index in range(1, len(filenames)):
        #     result = CyclicResult(filenames[index])
        #     new_mask = np.in1d(gl_nnum, result.mesh.nnum, assume_unique=True)
        #     if not new_mask.any():
        #         raise RuntimeError('File %s not part of the distributed result'
        #                            % filenames[index])
        #     mask += new_mask
        #     self._results.append(result)

        # if not np.all(mask):
        #     filenames = '\n'.join([result.filename for result in self._results])
        #     raise RuntimeError('Total nodes loaded from the individual result '
        #                        'files does not match the number in the global index.  '
        #                        'Filenames include:\n\n%s' %
        #                        filenames)

        # # assemble the global mesh
        # vtkappend = vtkAppendFilter()
        # vtkappend.MergePointsOn()
        # st = 0
        # for i, result in enumerate(self._results):
        #     # map the merged node numbering with the individual mappings
        #     result.grid['_dist_idx'] = np.arange(st, st + result.grid.n_points)
        #     st += result.grid.n_points
        #     vtkappend.AddInputData(result.grid)

        # vtkappend.Update()
        # self.grid = pv.wrap(vtkappend.GetOutput())

        # elem = np.hstack(result.mesh._elem for result in self._results)
        # glb_elem_off = []
        # for result in self._results:
        #     elem_off = result.mesh._elem_off
        #     if len(glb_elem_off):
        #         off = glb_elem_off[-1][-1]
        #         glb_elem_off.append(elem_off[1:] + off)
        #     else:
        #         glb_elem_off.append(elem_off)

        # glb_elem_off = np.hstack(glb_elem_off)
        # self._mesh = Mesh(self.grid['ansys_node_num'], self.grid.points,
        #                   elem, glb_elem_off, self._main_result.mesh.ekey)
        #                   # node_comps=ncomp, elem_comps=ecomp)

        # # from the individual mappings
        # self._glb_idx = self.grid['_dist_idx']

    @property
    def _main_result(self):
        """Main result instance"""
        return self._results[0]

    # @property
    # @wraps(Result.mesh)
    # def mesh(self):
    #     """Assembled global mesh is an assembly of the individual result file meshes"""
    #     return self._mesh

    # @wraps(Result.nodal_solution)
    # def nodal_solution(self, *args, **kwargs):
    #     this_function_name = inspect.currentframe().f_code.co_name
    #     return self._dis_solution(this_function_name, *args, **kwargs)

    # def _dis_solution(self, func_name, *args, **kwargs):
    #     """Get the distributed solution for a given function"""
    #     glb_sol = []
    #     for result in self._results:
    #         func = getattr(result, func_name)
    #         glb_sol.append(func(*args, **kwargs)[1])
    #     return self.mesh.nnum, np.vstack(glb_sol)[self._glb_idx]


# rst = DistributedCyclicResult('/tmp/ansys_hwvlknisom/file0.rst')
# rst0 = CyclicResult('/tmp/ansys_hwvlknisom/file0.rst')
# rst1 = CyclicResult('/tmp/ansys_hwvlknisom/file1.rst')


# rst0.harmonic_indices
# rst1.harmonic_indices
