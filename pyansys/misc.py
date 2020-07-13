"""Module for miscellaneous functions and methods"""
import sys

from pyvista.utilities.errors import GPUInfo
import scooby

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
    """Kill a process with extreme prejudice"""
    import psutil  # imported here to avoid import errors when unused
    process = psutil.Process(proc_pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()


class Report(scooby.Report):
    """A class for custom scooby.Report."""

    def __init__(self, additional=None, ncol=3, text_width=80, sort=False,
                 gpu=True):
        """Generate a :class:`scooby.Report` instance.

        Parameters
        ----------
        additional : list(ModuleType), list(str)
            List of packages or package names to add to output information.

        ncol : int, optional
            Number of package-columns in html table; only has effect if
            ``mode='HTML'`` or ``mode='html'``. Defaults to 3.

        text_width : int, optional
            The text width for non-HTML display modes

        sort : bool, optional
            Alphabetically sort the packages

        gpu : bool
            Gather information about the GPU. Defaults to ``True`` but if
            experiencing renderinng issues, pass ``False`` to safely generate
            a report.

        """
        # Mandatory packages.
        core = ['pyansys', 'pyvista', 'vtk', 'numpy',
                'appdirs', 'psutil', 'pexpect']

        if sys.platform != 'darwin':
            core.append('pyansys')

        # Optional packages.
        optional = ['scipy', 'matplotlib']

        # Information about the GPU - bare except in case there is a rendering
        # bug that the user is trying to report.
        if gpu:
            try:
                extra_meta = [(t[1], t[0]) for t in GPUInfo().get_info()]
            except:
                extra_meta = ("GPU Details", "error")
        else:
            extra_meta = ("GPU Details", "None")

        scooby.Report.__init__(self, additional=additional, core=core,
                               optional=optional, ncol=ncol,
                               text_width=text_width, sort=sort,
                               extra_meta=extra_meta)
