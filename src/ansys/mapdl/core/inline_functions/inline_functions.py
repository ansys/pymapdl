from .component_queries import (
    _ComponentQueries,
    _DisplacementComponentQueries,
    _InverseGetComponentQueries,
)
from .connectivity_queries import _ConnectivityQueries
from .geometry_queries import _AngleQueries, _AreaQueries, _DistanceQueries
from .line_queries import _LineFractionCoordinateQueries, _LineFractionSlopeQueries
from .nearest_queries import _EntityNearestEntityQueries
from .normals_queries import _KeypointNormalQueries, _NodeNormalQueries
from .scalar_queries import _ScalarQueries
from .selection_queries import _NextSelectedEntityQueries, _SelectionStatusQueries


class Query(
    _ComponentQueries,
    _InverseGetComponentQueries,
    _DisplacementComponentQueries,
    _SelectionStatusQueries,
    _LineFractionCoordinateQueries,
    _LineFractionSlopeQueries,
    _NextSelectedEntityQueries,
    _NodeNormalQueries,
    _KeypointNormalQueries,
    _EntityNearestEntityQueries,
    _ConnectivityQueries,
    _AngleQueries,
    _AreaQueries,
    _DistanceQueries,
    _ScalarQueries,
):
    """Class containing all the inline functions of APDL.

    Most of the results of these methods are shortcuts for specific
    combinations of arguments supplied to :func:`ansys.mapdl.core.Mapdl.get`.

    Currently implemented functions:

    - ``centrx(e)`` - get the centroid x-coordinate of element `e`
    - ``centry(e)`` - get the centroid y-coordinate of element `e`
    - ``centrz(e)`` - get the centroid z-coordinate of element `e`
    - ``nx(n)`` - get the x-coordinate of node `n`
    - ``ny(n)`` - get the y-coordinate of node `n`
    - ``nz(n)`` - get the z-coordinate of node `n`
    - ``kx(k)`` - get the x-coordinate of keypoint `k`
    - ``ky(k)`` - get the y-coordinate of keypoint `k`
    - ``kz(k)`` - get the z-coordinate of keypoint `k`
    - ``lx(n, lfrac)`` - X-coordinate of line ``n`` at length fraction ``lfrac``
    - ``ly(n, lfrac)`` - Y-coordinate of line ``n`` at length fraction ``lfrac``
    - ``lz(n, lfrac)`` - Z-coordinate of line ``n`` at length fraction ``lfrac``
    - ``lsx(n, lfrac)`` - X-slope of line ``n`` at length fraction ``lfrac``
    - ``lsy(n, lfrac)`` - Y-slope of line ``n`` at length fraction ``lfrac``
    - ``lsz(n, lfrac)`` - Z-slope of line ``n`` at length fraction ``lfrac``
    - ``ux(n)`` - get the structural displacement at node `n` in x
    - ``uy(n)`` - get the structural displacement at node `n` in y
    - ``uz(n)`` - get the structural displacement at node `n` in z
    - ``rotx(n)`` - get the rotational displacement at node `n` in x
    - ``roty(n)`` - get the rotational displacement at node `n` in y
    - ``rotz(n)`` - get the rotational displacement at node `n` in z
    - ``nsel(n)`` - get the selection status of node `n`
    - ``ksel(k)`` - get the selection status of keypoint `k`
    - ``lsel(n)`` - get the selection status of line `n`
    - ``asel(a)`` - get the selection status of area `a`
    - ``esel(n)`` - get the selection status of element `e`
    - ``vsel(v)`` - get the selection status of volume `v`
    - ``ndnext(n)`` - get the next selected node with a number greater than `n`.
    - ``kpnext(k)`` - get the next selected keypoint with a number greater than `k`.
    - ``lsnext(n)`` - get the next selected line with a number greater than `n`.
    - ``arnext(a)`` - get the next selected area with a number greater than `a`.
    - ``elnext(e)`` - get the next selected element with a number greater than `e`.
    - ``vlnext(v)`` - get the next selected volume with a number greater than `v`.
    - ``nnear(n)`` - get the selected node nearest node `n`.
    - ``knear(k)`` - get the selected keypoint nearest keypoint `k`.
    - ``enearn(n)`` - get  the selected element nearest node `n`.
    - ``node(x, y, z)`` - get the node closest to coordinate (x, y, z)
    - ``kp(x, y, z)`` - get the keypoint closest to coordinate (x, y, z)

    Examples
    --------
    In this example we construct a solid box and mesh it. Then we use
    the ``Query`` methods ``nx``, ``ny``, and ``nz`` to find the
    cartesian coordinates of the first node. We can access these
    through the ``mapdl.queries`` property.

    >>> from ansys.mapdl.core import launch_mapdl
    >>> mapdl = launch_mapdl()
    >>> mapdl.prep7()
    >>> mapdl.et(1, 'SOLID5')
    >>> mapdl.block(0, 10, 0, 20, 0, 30)
    >>> mapdl.esize(2)
    >>> mapdl.vmesh('ALL')
    >>> q = mapdl.queries
    >>> q.nx(1), q.ny(1), q.nz(1)
    0.0 20.0 0.0
    """

    def __init__(self, mapdl):
        self._mapdl = mapdl
