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
    # Get cells and points from grid
    cells = grid.GetNumpyCells(ctypes.c_long)
    points = grid.points
    if not points.flags.c_contiguous:
        points = np.ascontiguousarray(points)

    if points.dtype == ctypes.c_float:
        return _cellqualfloat.CompScJac_quad(cells, points)
    elif points.dtype == ctypes.c_double:
        return _cellqual.CompScJac_quad(cells, points)
    else:
        raise Exception('Invalid point precision %s.  ' % points.dtype +
                        'Must be either float or double')
