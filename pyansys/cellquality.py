"""
Cell quality module
"""
import ctypes
from pyansys import _cellqual


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
    points = grid.GetNumpyPoints(ctypes.c_double)

    return _cellqual.CompScJac_quad(cells, points)
