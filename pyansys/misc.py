import psutil

import numpy as np
import vtk

VTK9 = vtk.vtkVersion().GetVTKMajorVersion() >= 9

def vtk_cell_info(grid):
    """Returns version consistent connectivity and cell offset arrays.

    Notes
    -----
    VTKv9 changed the connectivity and offset arrays:

    Topology:
    ---------
    Cell 0: Triangle | point ids: {0, 1, 2}
    Cell 1: Triangle | point ids: {5, 7, 2}
    Cell 2: Quad     | point ids: {3, 4, 6, 7}
    Cell 4: Line     | point ids: {5, 8}

    VTKv9
    =====
    Offsets:      {0, 3, 6, 10, 12}
    Connectivity: {0, 1, 2, 5, 7, 2, 3, 4, 6, 7, 5, 8}

    Prior to VTKv9
    ==============
    Offsets:      {0, 4, 8, 13, 16}
    Connectivity: {3, 0, 1, 2, 3, 5, 7, 2, 4, 3, 4, 6, 7, 2, 5, 8}

    """
    if VTK9:
        # for pyvista < 0.25.0
        if not hasattr(grid, 'cell_connectivity'):
            carr = grid.GetCells()
            cells = vtk.util.numpy_support.vtk_to_numpy(carr.GetConnectivityArray())
        else:
            cells = grid.cell_connectivity
        offset = grid.offset - 1
    else:
        cells, offset = grid.cells, grid.offset

    if cells.dtype != np.int64:
        cells = cells.astype(np.int64)

    if offset.dtype != np.int64:
        offset = offset.astype(np.int64)

    return cells, offset


def kill_process(proc_pid):
    """ kills a process with extreme prejudice """
    process = psutil.Process(proc_pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()
