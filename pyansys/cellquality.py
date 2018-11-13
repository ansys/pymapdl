"""
Cell quality module
"""
import ctypes
import numpy as np

from pyansys import _cellqual, _cellqualfloat


def CellQuality(grid):
    """
    Given a vtk unstructured grid, returns the minimum scaled jacobian cell
    quality for each cell.  Unstructured grid can only contain the following
    elements
        tetrahedral
        pyramid
        wedge
        hexahedral

    Elements may be linear or quadradic

    """
    cells = grid.cells
    offset = grid.offset
    celltypes = grid.celltypes
    points = grid.points
    if points.dtype != np.double:
        points = points.astype(np.double)

    return _cellqual.ComputeQuality(cells, offset, celltypes, points)
