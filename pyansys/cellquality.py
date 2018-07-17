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
    cells = grid.GetNumpyCells(ctypes.c_int64)

    offset = grid.offset
    if offset.dtype != ctypes.c_int64:
        offset = offset.astype(ctypes.c_int64)

    celltypes = grid.celltypes

    points = grid.points
    if not points.flags.c_contiguous:
        points = np.ascontiguousarray(points)

    if points.dtype == ctypes.c_float:
        return _cellqualfloat.CompScJac_quad(cells, points)  # TODO: update
    elif points.dtype == ctypes.c_double:
        return _cellqual.ComputeQuality(cells, offset, celltypes, points)
    else:
        raise Exception('Invalid point precision %s.  ' % points.dtype +
                        'Must be either float or double')
