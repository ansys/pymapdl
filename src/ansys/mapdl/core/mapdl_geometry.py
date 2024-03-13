# Copyright (C) 2024 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Module to support MAPDL CAD geometry"""
from functools import wraps
from typing import TYPE_CHECKING, Any, Iterable, List, Optional, Sequence, Tuple, Union

import numpy as np
from numpy.typing import NDArray

from ansys.mapdl.core import _HAS_PYVISTA, Mapdl
from ansys.mapdl.core.errors import VersionError

if _HAS_PYVISTA:
    import pyvista as pv

if TYPE_CHECKING:  # pragma: no cover
    from pyiges import Iges

from ansys.mapdl.core.misc import requires_package, run_as_prep7, supress_logging
from ansys.mapdl.core.theme import MapdlTheme

VALID_SELECTION_TYPE = ["S", "R", "A", "U"]
VALID_SELECTION_ENTYTY = ["VOLU", "AREA", "LINE", "KP", "ELEM", "NODE"]

from ansys.mapdl.core.mapdl_core import (
    DEBUG_LEVELS,
    VALID_SELECTION_ENTITY_TP,
    VALID_SELECTION_TYPE_TP,
)

FLST_LOOKUP = {
    "NODE": 1,  # node numbers
    "ELEM": 2,  # element numbers
    "KP": 3,  # keypoint numbers
    "LINE": 4,  # line numbers
    "AREA": 5,  # area numbers
    "VOLU": 6,  # volume numbers
    "TRACE": 7,  # trace points
    "COORD": 8,  # coordinate locations
}

VALID_TYPE_MSG = """- 'S' : Select a new set (default)
- 'R' : Reselect a set from the current set.
- 'A' : Additionally select a set and extend the current set.
- 'U' : Unselect a set from the current set.
"""

VERSION_ERROR = """
In PyMAPDL 0.66.0 and later, the new geometry module does not allow calls on
``geometry.keypoints``, ``geometry.lines``, or ```geometry.areas```.

You can activate the old API like this:
>>> mapdl.legacy_geometry = True

For more information, see `Mesh and geometry <https://mapdl.docs.pyansys.com/version/stable/user_guide/mesh_geometry.html>`_.
"""


if _HAS_PYVISTA:

    class Multiblock(pv.MultiBlock):
        def __call__(self, *args, **kwargs):
            raise VersionError(VERSION_ERROR)

        @wraps(pv.MultiBlock.plot)
        def plot(self, *args, **kwargs):
            color = kwargs.pop("color", "white")
            return super().plot(*args, color=color, theme=MapdlTheme(), **kwargs)

    @requires_package("pyvista")
    def merge_polydata(items: Iterable["pv.PolyData"]) -> "pv.PolyData":
        """Merge list of polydata or unstructured grids"""

        # lazy import here for faster module loading
        from vtkmodules.vtkFiltersCore import vtkAppendPolyData

        afilter = vtkAppendPolyData()
        for item in items:
            afilter.AddInputData(item)
            afilter.Update()

        return pv.wrap(afilter.GetOutput())


class Geometry:
    """Pythonic representation of MAPDL CAD geometry

    Contains advanced methods to extend geometry building and
    selection within MAPDL.

    """

    def __init__(self, mapdl: Mapdl):
        """Geometry manager

        Class to help to manage geometry representations in an
        :class:`Mapdl instance <ansys.mapdl.core.Mapdl>` instance.

        Parameters
        ----------
        mapdl : ansys.mapdl.core.Mapdl
            Mapdl instance which this class references to.
        """
        from ansys.mapdl.core.mapdl import MapdlBase

        if not isinstance(mapdl, MapdlBase):
            raise TypeError("Must be initialized using a gRPC MAPDL class")

        self._mapdl = mapdl
        self._keypoints_cache = None
        self._lines_cache = None
        self._log = self._mapdl._log

    def _set_log_level(self, level: DEBUG_LEVELS) -> None:
        return self._mapdl.set_log_level(level)

    @requires_package("pyiges")
    def _load_iges(self) -> "Iges":
        """Loads the iges file from MAPDL as a pyiges class"""
        # Lazy import here for speed and stability
        # possible to exclude this import in the future
        try:
            from pyiges import Iges
        except ImportError:
            raise ImportError(
                "Please install pyiges to use this feature with:\n" "pip install pyiges"
            )
        return Iges(self._mapdl._generate_iges())

    def _reset_cache(self) -> None:
        self._keypoints_cache = None
        self._lines_cache = None

    def __setitem__(self, key: Any, value: Any):
        raise NotImplementedError("This method has not been implemented yet")

    @requires_package("pyvista")
    def __getitem__(self, name: str):
        name = name.lower()
        if "kp" in name:
            return self.keypoints[name]
        elif "line" in name:
            return self.lines[name]
        elif "area" in name:
            return self.areas[name]
        elif "volume" in name:
            return self.volumes[name]
        else:
            raise ValueError(
                f"The entity named '{name}' does not exist as a geometry entity."
            )

    @property
    @requires_package("pyiges")
    def _keypoints(self) -> Tuple[NDArray, NDArray]:
        """Returns keypoints cache"""
        if self._keypoints_cache is None:
            self._keypoints_cache = self._load_keypoints()
        return self._keypoints_cache

    @property
    @requires_package("pyvista")
    def keypoints(self) -> "pv.MultiBlock":
        """Obtain the keypoints geometry.

        Obtain the selected keypoints as a :class:`pyvista.MultiBlock` object.

        Returns
        -------
        pv.MultiBlock

        Examples
        --------

        >>> mapdl.geometry.keypoints
        MultiBlock (0x147a78220)
          N Blocks    26
          X Bounds    -0.016, 0.016
          Y Bounds    -0.008, 0.018
          Z Bounds    -0.003, 0.015

        You can plot the entities:

        >>> mapdl.geometry.keypoints.plot()

        You can access the individual keypoints using indexing:

        >>> keypoint0 = mapdl.geometry.keypoints[0]
        >>> keypoint0
        pyvista_ndarray([ 0.     ,  0.01778, -0.00318])

        You can use the entity name:

        >>> kp1 = mapdl.geometry.keypoints["kp 1"]
        >>> kp1
        pyvista_ndarray([ 0.     ,  0.01778, -0.00318])

        You can iterate the different elements:

        >>> points = mapdl.geometry.keypoints
        >>> for each_point in points:
                print(each_point.points[0])
        pyvista_ndarray([ 0.     ,  0.01778, -0.00318])
        ...

        Alternatively, to iterate you can use :meth:`Mapdl.geometry.get_keypoints`.

        >>> points = mapdl.geometry.get_keypoints(return_as_array=True)
        >>> for each_point in points:
                print(each_point)
        [ 0.     ,  0.01778, -0.00318]
        ...

        """
        mb = Multiblock(self.get_keypoints(return_as_list=True))
        # Setting names
        for ind, each_block in enumerate(mb):
            mapdl_index = int(each_block["entity_num"][0])
            mb.set_block_name(index=ind, name=f"kp {mapdl_index}")
        return mb

    @requires_package("pyvista")
    def get_keypoints(
        self,
        return_as_list: bool = False,
        return_as_array: bool = False,
        return_ids_in_array: bool = False,
    ) -> Union[NDArray[Any], "pv.PolyData", List["pv.PolyData"]]:
        """Obtain the keypoints geometry.

        Obtain the selected keypoints as a :class:`pyvista.PolyData` object or
        a list of :class:`pyvista.PolyData`.

        Parameters
        ----------
        return_as_list : bool, optional
            Whether to return the data as a list. The default is ``False``, in which case the data is returned as a PyVista :class:`PolyData<pyvista.PolyData>` object.
        return_as_array : bool, optional
            Whether to return the data as a :class:`numpy array <numpy.ndarray>`. The default  is ``False``, in which case the data is returned as a PyVista :class:`PolyData <pyvista.PolyData>` object.
        return_ids_in_array : bool, optional
            Whether to return the keypoint IDs in the output array. The default is
            ``False``, in which case the data is as a :class:`numpy array <numpy.ndarray>` object with only the coordinates. This parameter is only valid when ``return_as_array=True``.

        Returns
        -------
        Union[NDArray[Any], pv.PolyData, list[pv.PolyData]]

        Examples
        --------

        Return a single merged mesh.

        >>> kps = mapdl.geometry.get_keypoints()
        >>> kps
        PolyData (0x147d5b580)
          N Cells:    26
          N Points:   26
          N Strips:   0
          X Bounds:   -1.588e-02, 1.588e-02
          Y Bounds:   -7.620e-03, 1.778e-02
          Z Bounds:   -3.180e-03, 1.524e-02
          N Arrays:   1

        Return a list of keypoints as individual grids

        >>> keypoints = mapdl.geometry.get_keypoints(return_as_list=True)
        >>> keypoints
        [PolyData (0x147ca4be...rrays:   1, PolyData (0x147d5b8e...rrays:   1, PolyData (0x1491a42e...rrays:   1, PolyData (0x1491a440...rrays:   1, PolyData (0x1491a47c...rrays:   1, PolyData (0x1491a470...rrays:   1, PolyData (0x1491a4b2...rrays:   1, PolyData (0x1491a4e2...rrays:   1, PolyData (0x1491a49a...rrays:   1, PolyData (0x1491a4f4...rrays:   1, PolyData (0x1491a458...rrays:   1, PolyData (0x1491a4b8...rrays:   1, PolyData (0x1491a4dc...rrays:   1, PolyData (0x1491a506...rrays:   1, ...]

        Return the keypoints coordinates as a numpy array:

        >>> keypoints = mapdl.geometry.get_keypoints(return_as_array=True)
        array([[ 0.00000000e+00,  1.77800000e-02, -3.18000000e-03],
               [ 0.00000000e+00, -7.62000000e-03, -3.18000000e-03],
               [ 1.58750000e-02,  1.77800000e-02, -3.18000000e-03],
               [ 1.58750000e-02, -7.62000000e-03, -3.18000000e-03],
               [ 0.00000000e+00, -7.62000000e-03,  0.00000000e+00],
        ...

        When returning an array, you can also choose to output the keypoint
        ids as the first column:

        >>> keypoints = mapdl.geometry.get_keypoints(return_ids_in_array=True)
        array([[ 1.00000000e+00,  0.00000000e+00,  1.77800000e-02,
                -3.18000000e-03],
               [ 2.00000000e+00,  0.00000000e+00, -7.62000000e-03,
                -3.18000000e-03],
               [ 3.00000000e+00,  1.58750000e-02,  1.77800000e-02,
                -3.18000000e-03],
               [ 4.00000000e+00,  1.58750000e-02, -7.62000000e-03,
                -3.18000000e-03],
               [ 5.00000000e+00,  0.00000000e+00, -7.62000000e-03,
                 0.00000000e+00],
               [ 6.00000000e+00,  1.58750000e-02, -7.62000000e-03,
        ...

        """
        if return_as_array or return_ids_in_array:
            if return_ids_in_array:
                keyp = np.array(self._keypoints[0])
                keyp_num = np.array(self._keypoints[1])
                return np.hstack((keyp_num.reshape((-1, 1)), keyp))
            else:
                return np.array(self._keypoints[0])

        keypoints, kp_num = self._keypoints

        if return_as_list:
            keypoints_ = []

            for each_point, each_id in zip(keypoints, kp_num):
                keypoints_ps = pv.PolyData([each_point])
                keypoints_ps["entity_num"] = np.array(each_id).reshape((1))
                keypoints_.append(keypoints_ps)

            return keypoints_

        else:
            keypoints_pd = pv.PolyData(keypoints)
            keypoints_pd["entity_num"] = kp_num
            return keypoints_pd

    @property
    def _lines(self) -> List["pv.PolyData"]:
        """Cache of the lines."""
        if self._lines_cache is None:
            self._lines_cache = self._load_lines()
        return self._lines_cache

    @property
    @requires_package("pyvista")
    def lines(self) -> "pv.MultiBlock":
        """Geometry of the lines.

        Obtain the selected lines as a :class:`pyvista.MultiBlock` object.

        Returns
        -------
        pv.MultiBlock

        Examples
        --------

        >>> mapdl.geometry.lines
        MultiBlock (0x147b77e20)
          N Blocks    45
          X Bounds    -0.016, 0.016
          Y Bounds    -0.008, 0.018
          Z Bounds    -0.003, 0.015

        You can plot the entities:

        >>> mapdl.geometry.lines.plot()

        You can access the individual lines using indexing:

        >>> line0 = mapdl.geometry.lines[0]
        >>> line0
        PolyData (0x147d5b220)
          N Cells:    1
          N Points:   100
          N Strips:   0
          X Bounds:   0.000e+00, 0.000e+00
          Y Bounds:   -7.620e-03, 1.778e-02
          Z Bounds:   -3.180e-03, -3.180e-03
          N Arrays:   1

        You can use the entity name:

        >>> line1 = mapdl.geometry.lines["line 1"]
        >>> line1
        PolyData (0x147d5b220)
          N Cells:    1
          N Points:   100
          N Strips:   0
          X Bounds:   0.000e+00, 0.000e+00
          Y Bounds:   -7.620e-03, 1.778e-02
          Z Bounds:   -3.180e-03, -3.180e-03
          N Arrays:   1

        You can iterate the different elements:

        >>> points = mapdl.geometry.lines
        >>> for each_line in points:
                print(each_line)
        PolyData (0x147d5b220)
          N Cells:    1
          N Points:   100
          N Strips:   0
          X Bounds:   0.000e+00, 0.000e+00
          Y Bounds:   -7.620e-03, 1.778e-02
          Z Bounds:   -3.180e-03, -3.180e-03
          N Arrays:   1
        ...

        """
        mb = Multiblock(self._lines)
        # Setting names
        for ind, each_block in enumerate(mb):
            mapdl_index = int(each_block["entity_num"][0])
            mb.set_block_name(index=ind, name=f"line {mapdl_index}")
        return mb

    @requires_package("pyvista")
    def get_lines(
        self, return_as_list: bool = False
    ) -> Union["pv.PolyData", List["pv.PolyData"]]:
        """Obtain line geometry

        Obtain the active lines as a :class:`pyvista.PolyData` object or
        a list of :class:`pyvista.PolyData` objects.

        Parameters
        ----------
        return_as_list : bool, optional
            Whether to return the lines in a list. The default is ``False``.

        Returns
        -------
        Union[pv.PolyData, List[pv.PolyData]]

        Examples
        --------

        Return a single merged mesh.

        >>> line_mesh = mapdl.geometry.get_lines()
        >>> line_mesh
        PolyData (0x14917e740)
          N Cells:    45
          N Points:   4500
          N Strips:   0
          X Bounds:   -1.588e-02, 1.588e-02
          Y Bounds:   -7.620e-03, 1.778e-02
          Z Bounds:   -3.180e-03, 1.524e-02
          N Arrays:   1

        Return a list of lines as individual grids

        >>> lines = mapdl.geometry.get_lines(return_as_list=True)
        >>> lines
        [PolyData (0x1492ee7a...rrays:   1, PolyData (0x1491a404...rrays:   1, PolyData (0x1491068c...rrays:   1, PolyData (0x14910662...rrays:   1, PolyData (0x14910632...rrays:   1, PolyData (0x1492eeb0...rrays:   1, PolyData (0x1492eec8...rrays:   1, PolyData (0x1492eee0...rrays:   1, PolyData (0x1492eef8...rrays:   1, PolyData (0x1492ef10...rrays:   1, PolyData (0x1492ef28...rrays:   1, PolyData (0x1492ef40...rrays:   1, PolyData (0x1492ef58...rrays:   1, PolyData (0x1492ef70...rrays:   1, ...]

        """
        if return_as_list:
            return self._lines
        else:
            return merge_polydata(self._lines)

    @property
    @requires_package("pyvista")
    def areas(self) -> "pv.MultiBlock":
        """Geometry of the areas.

        Obtain the selected areas as a :class:`pyvista.MultiBlock` object.

        Returns
        -------
        pv.MultiBlock

        Examples
        --------

        >>> mapdl.geometry.areas
        MultiBlock (0x147ca7640)
          N Blocks    28
          X Bounds    -0.016, 0.016
          Y Bounds    -0.008, 0.018
          Z Bounds    -0.003, 0.015

        You can plot the entities:

        >>> mapdl.geometry.areas.plot()

        You can access the individual areas using indexing:

        >>> area0 = mapdl.geometry.areas[0]
        >>> area0
        UnstructuredGrid (0x147ca4340)
          N Cells:    10
          N Points:   18
          X Bounds:   0.000e+00, 1.588e-02
          Y Bounds:   -7.620e-03, 1.778e-02
          Z Bounds:   -3.180e-03, -3.180e-03
          N Arrays:   3

        You can use the entity name:

        >>> area1 = mapdl.geometry.areas["area 1"]
        >>> area1
        UnstructuredGrid (0x147ca4340)
          N Cells:    10
          N Points:   18
          X Bounds:   0.000e+00, 1.588e-02
          Y Bounds:   -7.620e-03, 1.778e-02
          Z Bounds:   -3.180e-03, -3.180e-03
          N Arrays:   3

        You can iterate the different elements:

        >>> points = mapdl.geometry.areas
        >>> for each_line in points:
                print(each_line)
        UnstructuredGrid (0x147ca4340)
          N Cells:    10
          N Points:   18
          X Bounds:   0.000e+00, 1.588e-02
          Y Bounds:   -7.620e-03, 1.778e-02
          Z Bounds:   -3.180e-03, -3.180e-03
          N Arrays:   3
        ...

        """
        mb = Multiblock(self.get_areas(return_as_list=True))
        # Setting names
        for ind, each_block in enumerate(mb):
            mapdl_index = int(each_block["entity_num"][0])
            mb.set_block_name(index=ind, name=f"area {mapdl_index}")
        return mb

    @requires_package("pyvista")
    def get_areas(
        self, quality: int = 1, return_as_list: Optional[bool] = False
    ) -> Union[List["pv.UnstructuredGrid"], "pv.PolyData"]:
        """Get active areas from MAPDL represented as :class:`pyvista.PolyData` or a list of :class:`pyvista.UnstructuredGrid`.

        Parameters
        ----------
        quality : int, optional
            Quality of the mesh to display.  Values are between 1 (worst)
            and10 (best).

        Returns
        -------
        pv.PolyData or List[pv.UnstructuredGrid]
            pv.PolyData grouping all meshes representing
            the active surface areas selected by ``ASEL``.  If
            ``return_as_list=True``, areas are returned as a
            list of ``pv.UnstructuredGrid``.

        Examples
        --------

        Return a single merged mesh.

        >>> area_mesh = mapdl.geometry.get_areas(quality=3)
        >>> area_mesh
        UnstructuredGrid (0x7f14add95ca0)
          N Cells:	24
          N Points:	30
          X Bounds:	-2.000e+00, 2.000e+00
          Y Bounds:	0.000e+00, 1.974e+00
          Z Bounds:	5.500e-01, 5.500e-01
          N Arrays:	4

        Return a list of areas as individual grids

        >>> areas = mapdl.geometry.get_areas(quality=3, return_as_list=True)
        >>> areas
        [UnstructuredGrid (0x7f14add95040)
          N Cells:	12
          N Points:	20
          X Bounds:	-2.000e+00, 2.000e+00
          Y Bounds:	0.000e+00, 1.974e+00
          Z Bounds:	0.000e+00, 0.000e+00
          N Arrays:	4,
        UnstructuredGrid (0x7f14add95ca0)
          N Cells:	12
          N Points:	20
          X Bounds:	-2.000e+00, 2.000e+00
          Y Bounds:	0.000e+00, 1.974e+00
          Z Bounds:	5.500e-01, 5.500e-01
          N Arrays:	4,
        ...

        """
        quality = int(quality)
        if quality > 10:
            raise ValueError(
                "The ``quality`` parameter must be a value between 0 and 10."
            )

        surf = self.generate_surface(11 - quality)

        if not return_as_list:
            return surf

        entity_num = surf["entity_num"]

        areas = []
        anums = np.unique(entity_num)
        for anum in anums:
            areas.append(surf.extract_cells(entity_num == anum))

        return areas

    @supress_logging
    @run_as_prep7
    @requires_package("pyvista")
    def generate_surface(
        self,
        density: int = 4,
        amin: Optional[int] = None,
        amax: Optional[int] = None,
        ninc: Optional[int] = None,
    ) -> "pv.PolyData":
        """
        Generate an all-triangular surface of the active surfaces.

        Parameters
        ----------
        density : int, optional
            APDL smart sizing option.  Ranges from 1 (worst) to 10
            (best).

        amin : int, optional
            Minimum APDL numbered area to select.  See
            ``mapdl.anum`` for available areas.

        amax : int, optional
            Maximum APDL numbered area to select.  See
            ``mapdl.anum`` for available areas.

        ninc : int, optional
            Steps to between amin and amax.

        """
        with self._mapdl.save_selection:
            orig_anum = self.anum

            # reselect from existing selection to mimic APDL behavior
            if amin or amax:
                if amax is None:
                    amax = amin

                if amin is None:  # amax is non-zero
                    amin = 1

                if ninc is None:
                    ninc = ""

                self._mapdl.asel("R", "AREA", vmin=amin, vmax=amax, vinc=ninc)

            # duplicate areas to avoid affecting existing areas
            a_num = int(self._mapdl.get(entity="AREA", item1="NUM", it1num="MAXD"))
            self._mapdl.numstr("AREA", a_num, mute=True)
            self._mapdl.agen(2, "ALL", noelem=1, mute=True)
            a_max = int(self._mapdl.get(entity="AREA", item1="NUM", it1num="MAXD"))

            self._mapdl.asel("S", "AREA", vmin=a_num + 1, vmax=a_max, mute=True)
            # necessary to reset element/area meshing association
            self._mapdl.aatt(mute=True)

            # create a temporary etype
            etype_max = int(self._mapdl.get(entity="ETYP", item1="NUM", it1num="MAX"))
            etype_old = self._mapdl.parameters.type
            etype_tmp = etype_max + 1

            old_routine = self._mapdl.parameters.routine

            self._mapdl.et(etype_tmp, "MESH200", 6, mute=True)
            self._mapdl.shpp("off", mute=True)
            self._mapdl.smrtsize(density, mute=True)
            self._mapdl.type(etype_tmp, mute=True)

            if old_routine != "PREP7":
                self._mapdl.prep7(mute=True)

            # Mesh and get the number of elements per area
            resp = self._mapdl.amesh("all")
            elements_per_area = self.get_elements_per_area()

            self._mapdl.esla("S")
            grid = self._mapdl.mesh._grid.linear_copy()
            pd = pv.PolyData(grid.points, grid.cells, n_faces=grid.n_cells)

            # pd['ansys_node_num'] = grid['ansys_node_num']
            # pd['vtkOriginalPointIds'] = grid['vtkOriginalPointIds']
            # pd.clean(inplace=True)  # OPTIONAL

            # delete all temporary meshes and clean up settings
            self._mapdl.aclear("ALL", mute=True)
            self._mapdl.adele("ALL", kswp=1, mute=True)
            self._mapdl.numstr("AREA", 1, mute=True)
            self._mapdl.type(etype_old, mute=True)
            self._mapdl.etdele(etype_tmp, mute=True)
            self._mapdl.shpp("ON", mute=True)
            self._mapdl.smrtsize("OFF", mute=True)

        # store the area number used for each element
        entity_num = np.empty(grid.n_cells, dtype=np.int32)
        if grid and len(elements_per_area) != 0:
            # add anum info
            i = 0
            for index, (anum, nelem) in enumerate(elements_per_area):
                # have to use original area numbering here as the
                # duplicated areas numbers are inaccurate
                entity_num[i : i + nelem] = orig_anum[index]
                i += nelem
        else:
            entity_num[:] = 0

        pd["entity_num"] = entity_num
        return pd

    @property
    def n_volu(self) -> int:
        """
        Number of volumes currently selected.

        Examples
        --------
        >>> mapdl.n_volu
        1
        """
        return self._item_count("VOLU")

    @property
    def n_area(self) -> int:
        """
        Number of areas currently selected.

        Examples
        --------
        >>> mapdl.n_area
        1
        """
        return self._item_count("AREA")

    @property
    def n_line(self) -> int:
        """
        Number of lines currently selected.

        Examples
        --------
        >>> mapdl.n_line
        1
        """
        return self._item_count("LINE")

    @property
    def n_keypoint(self) -> int:
        """
        Number of keypoints currently selected.

        Examples
        --------
        >>> mapdl.n_keypoint
        1
        """
        return self._item_count("KP")

    @supress_logging
    def _item_count(self, entity: str) -> int:
        """Return item count for a given entity."""
        return int(self._mapdl.get(entity=entity, item1="COUNT"))

    @property
    def knum(self) -> NDArray[np.int32]:
        """
        Array of keypoint numbers.

        Examples
        --------
        >>> mapdl.block(0, 1, 0, 1, 0, 1)
        >>> mapdl.knum
        array([1, 2, 3, 4, 5, 6, 7, 8], dtype=int32)
        """
        if self._mapdl.geometry.n_keypoint == 0:
            return np.array([], dtype=np.int32)

        return self._mapdl.get_array("KP", item1="KLIST").astype(np.int32)

    @property
    def lnum(self) -> NDArray[np.int32]:
        """Array of line numbers.

        Examples
        --------
        >>> mapdl.block(0, 1, 0, 1, 0, 1)
        >>> mapdl.lnum
        array([ 1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12], dtype=int32)
        """
        # For clean exit when there is no lines.
        if self._mapdl.geometry.n_line == 0:
            return np.array([], dtype=np.int32)

        # this (weirdly) sometimes fails
        for _ in range(5):
            lnum = self._mapdl.get_array("LINES", item1="LLIST")
            if lnum.size == self.n_line:
                break
        return lnum.astype(np.int32)

    @property
    def anum(self) -> NDArray[np.int32]:
        """Array of area numbers.

        Examples
        --------
        >>> mapdl.block(0, 1, 0, 1, 0, 1)
        >>> mapdl.anum
        array([1, 2, 3, 4, 5, 6], dtype=int32)
        """
        # Clean exit
        if self._mapdl.geometry.n_area == 0:
            return np.array([], dtype=np.int32)

        return self._mapdl.get_array("AREA", item1="ALIST").astype(np.int32)

    @property
    def vnum(self) -> NDArray[np.int32]:
        """Array of volume numbers.

        Examples
        --------
        >>> mapdl.block(0, 1, 0, 1, 0, 1)
        >>> mapdl.vnum
        array([1], dtype=int32)
        """
        if self._mapdl.geometry.n_volu == 0:
            return np.array([], dtype=np.int32)

        return self._mapdl.get_array("VOLU", item1="VLIST").astype(np.int32)

    @supress_logging
    @requires_package("pyvista")
    @requires_package("pyiges")
    def _load_lines(self) -> List["pv.PolyData"]:
        """Load lines from MAPDL using IGES"""
        # ignore volumes
        with self._mapdl.save_selection:
            self._mapdl.ksel("ALL", mute=True)
            self._mapdl.lsel("ALL", mute=True)
            self._mapdl.asel("ALL", mute=True)
            self._mapdl.vsel("NONE", mute=True)

            iges = self._load_iges()

        selected_lnum = self.lnum
        lines = []
        entity_nums = []
        for bspline in iges.bsplines():
            # allow only 10001 as others appear to be construction entities
            if bspline.d["status_number"] in [1, 10001]:
                entity_num = int(bspline.d["entity_subs_num"])
                if entity_num not in entity_nums and entity_num in selected_lnum:
                    entity_nums.append(entity_num)
                    line = bspline.to_vtk()
                    line.cell_data["entity_num"] = entity_num
                    lines.append(line)

        entities = iges.lines() + iges.circular_arcs()
        for line in entities:
            if line.d["status_number"] == 1:
                entity_num = int(line.d["entity_subs_num"])
                if entity_num not in entity_nums and entity_num in selected_lnum:
                    entity_nums.append(entity_num)
                    line = line.to_vtk(resolution=1)
                    line.cell_data["entity_num"] = entity_num
                    lines.append(line)

        lines_ = []
        for line in lines:
            lines_.append(line)

        return lines_

    @requires_package("pyiges")
    def _load_keypoints(self) -> Tuple[NDArray, NDArray]:
        """Load keypoints from MAPDL using IGES."""
        # write only keypoints
        with self._mapdl.save_selection:
            self._mapdl.vsel("NONE", mute=True)
            self._mapdl.asel("NONE", mute=True)
            self._mapdl.lsel("NONE", mute=True)
            iges = self._load_iges()

        keypoints = []
        kp_num = []
        for kp in iges.points():
            keypoints.append([kp.x, kp.y, kp.z])
            kp_num.append(int(kp.d["entity_subs_num"]))

        return keypoints, kp_num

    def __str__(self) -> str:
        """Current geometry info"""
        info = "MAPDL Selected Geometry\n"
        info += "Keypoints:  %d\n" % self.n_keypoint
        info += "Lines:      %d\n" % self.n_line
        info += "Areas:      %d\n" % self.n_area
        info += "Volumes:    %d\n" % self.n_volu
        return info

    def keypoint_select(
        self,
        items: Optional[Sequence[int]] = None,
        sel_type: VALID_SELECTION_TYPE_TP = "S",
        return_selected: bool = False,
    ) -> Optional[NDArray[np.int32]]:
        """Select keypoints using a sequence of items.

        Parameters
        ----------
        items : sequence or None
            List, range, or sequence of integers of the keypoints you want
            to select.  If ``None`` or ``'NONE'``, no keypoints will be
            selected.  If 'ALL', selects all keypoints.

        sel_type : str, optional
            Selection type.  May be one of the following:

            * ``'S'``: Select a new set (default)
            * ``'R'``: Reselect a set from the current set.
            * ``'A'``: Additionally select a set and extend the current set.
            * ``'U'``: Unselect a set from the current set.

        return_selected : bool, optional
            Return the keypoint numbers selected.  Optional, and can be
            disabled for performance.  Default ``False``.

        Returns
        -------
        np.array
            Numpy array of keypoint numbers if ``return_selected=True``.

        Examples
        --------
        Create a new selection of keypoints [1, 5, 10]

        >>> mapdl.geometry.keypoint_select([1, 5, 10])

        Create a new selection of keypoints from 1 through 20

        >>> mapdl.geometry.keypoint_select(range(1, 21))

        Unselect keypoints 1 through 20

        >>> mapdl.geometry.keypoint_select(range(1, 21), sel_type='U')

        Append to an existing selection of keypoints

        >>> mapdl.geometry.keypoint_select([1, 2, 3], sel_type='A')

        Reselect from the existing selection of keypoints

        >>> mapdl.geometry.keypoint_select([3, 4, 5], sel_type='R')

        Select no keypoints

        >>> mapdl.geometry.keypoint_select(None)

        Select all keypoints

        >>> mapdl.geometry.keypoint_select('ALL')

        """
        if isinstance(items, str):
            items = items.upper()

        # special cases
        if items is None or items == "NONE":
            self._mapdl.ksel("NONE")
            return

        if items == "ALL":
            self._mapdl.ksel("ALL")
            if return_selected:
                return self.knum
            return

        self._select_items(items, "KP", sel_type)

        if return_selected:
            return self.knum

    def line_select(
        self,
        items: Optional[Sequence[int]],
        sel_type: VALID_SELECTION_TYPE_TP = "S",
        return_selected: bool = False,
    ) -> Optional[NDArray[np.int32]]:
        """Select lines using a sequence of items.

        Parameters
        ----------
        items : sequence or None
            List, range, or sequence of integers of the lines you want
            to select.  If ``None`` or ``'NONE'``, no lines will be
            selected.  If 'ALL', selects all lines.

        sel_type : str, optional
            Selection type.  May be one of the following:

            * ``'S'``: Select a new set (default)
            * ``'R'``: Reselect a set from the current set.
            * ``'A'``: Additionally select a set and extend the current set.
            * ``'U'``: Unselect a set from the current set.

        return_selected : bool, optional
            Return the line numbers selected.  Optional, and can be
            disabled for performance.  Default ``False``.

        Returns
        -------
        np.array
            Numpy array of keypoint numbers if ``return_selected=True``.

        Examples
        --------
        Create a new selection of lines [1, 5, 10]

        >>> mapdl.geometry.line_select([1, 5, 10])

        Create a new selection of lines from 1 through 20

        >>> mapdl.geometry.line_select(range(1, 21))

        Unselect lines 1 through 20

        >>> mapdl.geometry.line_select(range(1, 21), sel_type='U')

        Append to an existing selection of lines

        >>> mapdl.geometry.line_select([1, 2, 3], sel_type='A')

        Reselect from the existing selection of lines

        >>> mapdl.geometry.line_select([3, 4, 5], sel_type='R')

        Select no lines

        >>> mapdl.geometry.line_select(None)

        Select all lines

        >>> mapdl.geometry.line_select('ALL')

        """
        if isinstance(items, str):
            items = items.upper()

        # special cases
        if items is None or items == "NONE":
            self._mapdl.lsel("NONE")
            return

        if items == "ALL":
            self._mapdl.lsel("ALL")
            if return_selected:
                return self.lnum
            return

        self._select_items(items, "LINE", sel_type)

        if return_selected:
            return self.lnum

    def area_select(
        self,
        items: Optional[Sequence[int]],
        sel_type: VALID_SELECTION_TYPE_TP = "S",
        return_selected: bool = False,
    ) -> Optional[NDArray[np.int32]]:
        """Select areas using a sequence of items.

        Parameters
        ----------
        items : sequence, str, None
            List, range, or sequence of integers of the areas you want
            to select.  If ``None`` or ``'NONE'``, no areas will be
            selected.  If 'ALL', selects all areas.

        sel_type : str, optional
            Selection type.  May be one of the following:

            * ``'S'``: Select a new set (default)
            * ``'R'``: Reselect a set from the current set.
            * ``'A'``: Additionally select a set and extend the current set.
            * ``'U'``: Unselect a set from the current set.

        return_selected : bool, optional
            Return the area numbers selected.  Optional, and can be
            disabled for performance.  Default ``False``.

        Returns
        -------
        np.array
            Numpy array of keypoint numbers if ``return_selected=True``.

        Examples
        --------
        Create a new selection of areas [1, 5, 10]

        >>> mapdl.geometry.area_select([1, 5, 10])

        Create a new selection of areas from 1 through 20

        >>> mapdl.geometry.area_select(range(1, 21))

        Unselect areas 1 through 20

        >>> mapdl.geometry.area_select(range(1, 21), sel_type='U')

        Append to an existing selection of areas

        >>> mapdl.geometry.area_select([1, 2, 3], sel_type='A')

        Reselect from the existing selection of areas

        >>> mapdl.geometry.area_select([3, 4, 5], sel_type='R')

        Select no areas

        >>> mapdl.geometry.area_select(None)

        Select all areas

        >>> mapdl.geometry.area_select('ALL')

        """
        if isinstance(items, str):
            items = items.upper()

        # special cases
        if items is None or items == "NONE":
            self._mapdl.asel("NONE")
            return

        if items == "ALL":
            self._mapdl.asel("ALL")
            if return_selected:
                return self.anum
            return

        self._select_items(items, "AREA", sel_type)

        if return_selected:
            return self.anum

    @property
    @requires_package("pyvista")
    def volumes(self) -> "pv.MultiBlock":
        """Obtain the volumes geometry

        Obtain the selected volumes as a :class:`pyvista.MultiBlock` object.

        Returns
        -------
        pv.MultiBlock

        Examples
        --------

        >>> mapdl.geometry.volumes
        MultiBlock (0x147ca4100)
          N Blocks    6
          X Bounds    -0.016, 0.016
          Y Bounds    -0.008, 0.018
          Z Bounds    -0.003, 0.015

        You can plot the entities:

        >>> mapdl.geometry.volumes.plot()

        You can access the individual volumes using indexing:

        >>> volume0 = mapdl.geometry.volumes[0]
        >>> volume0
        UnstructuredGrid (0x149107340)
          N Cells:    34
          N Points:   36
          X Bounds:   0.000e+00, 1.588e-02
          Y Bounds:   -7.620e-03, 1.778e-02
          Z Bounds:   -3.180e-03, 0.000e+00
          N Arrays:   3

        You can use the entity name:

        >>> volume1 = mapdl.geometry.volumes["volume 1"]
        >>> volume1
        UnstructuredGrid (0x149107340)
          N Cells:    34
          N Points:   36
          X Bounds:   0.000e+00, 1.588e-02
          Y Bounds:   -7.620e-03, 1.778e-02
          Z Bounds:   -3.180e-03, 0.000e+00
          N Arrays:   3

        You can iterate the different elements:

        >>> points = mapdl.geometry.volumes
        >>> for each_line in points:
                print(each_line)
        UnstructuredGrid (0x149107340)
          N Cells:    34
          N Points:   36
          X Bounds:   0.000e+00, 1.588e-02
          Y Bounds:   -7.620e-03, 1.778e-02
          Z Bounds:   -3.180e-03, 0.000e+00
          N Arrays:   3
        ...

        """
        mb = Multiblock(self.get_volumes(return_as_list=True))
        # Setting names
        # Because the volume mapping is made through the areas, the default
        # "entity_num" field is not applicable here.
        for ind, each_block in enumerate(mb):
            mapdl_index = int(each_block.entity_num)
            mb.set_block_name(index=ind, name=f"volume {mapdl_index}")
        return mb

    @requires_package("pyvista")
    def get_volumes(
        self, return_as_list: bool = False, quality: int = 4
    ) -> Union[List["pv.PolyData"], "pv.PolyData"]:
        """Get active volumes from MAPDL represented as a :class:`pyvista.PolyData` object
        or a list of :class:`pyvista.UnstructuredGrid` objects.

        Parameters
        ----------
        quality : int, optional
            Quality of the mesh to display.  Values are 1 (worst)
            to 10 (best).

        Returns
        -------
        pv.PolyData or List[pv.UnstructuredGrid]
            pv.PolyData grouping all meshes representing
            the active surface volumes selected by ``VSEL``.  If
            ``return_as_list=True``, volumes are returned as a
            list of ``pv.UnstructuredGrid``.

        Examples
        --------

        Return a single merged mesh.

        >>> volume_mesh = mapdl.geometry.get_volumes(quality=3)
        >>> volume_mesh
        UnstructuredGrid (0x7f14add95ca0)
          N Cells:	24
          N Points:	30
          X Bounds:	-2.000e+00, 2.000e+00
          Y Bounds:	0.000e+00, 1.974e+00
          Z Bounds:	5.500e-01, 5.500e-01
          N Arrays:	4

        Return a list of volumes as individual grids.

        >>> volumes = mapdl.geometry.get_volumes(quality=3, return_as_list=True)
        >>> volumes
        [UnstructuredGrid (0x7f14add95040)
          N Cells:	12
          N Points:	20
          X Bounds:	-2.000e+00, 2.000e+00
          Y Bounds:	0.000e+00, 1.974e+00
          Z Bounds:	0.000e+00, 0.000e+00
          N Arrays:	4,
        UnstructuredGrid (0x7f14add95ca0)
          N Cells:	12
          N Points:	20
          X Bounds:	-2.000e+00, 2.000e+00
          Y Bounds:	0.000e+00, 1.974e+00
          Z Bounds:	5.500e-01, 5.500e-01
          N Arrays:	4,
        ...

        """
        quality = int(quality)
        if quality > 10:
            raise ValueError("``quality`` parameter must be a value between 0 and 10")

        volumes_ = []
        surf = self.generate_surface(11 - quality)

        if not return_as_list:
            return surf

        # Cache current selection
        with self._mapdl.save_selection:
            area_num = surf["entity_num"].astype(int)

            for each_volu in self.vnum:
                self._mapdl.vsel("S", vmin=each_volu)
                self._mapdl.aslv("S")
                unstruct = surf.extract_cells(np.in1d(area_num, self.anum))
                unstruct.entity_num = int(each_volu)
                volumes_.append(unstruct)

        return volumes_

    def volume_select(
        self,
        items: Optional[Union[str, Sequence[int]]],
        sel_type: VALID_SELECTION_TYPE_TP = "S",
        return_selected: bool = False,
    ) -> Optional[int]:
        """Select volumes using a sequence of items.

        Parameters
        ----------
        items : sequence, str, or None
            List, range, or sequence of integers of the volumes you want
            to select.  If ``None`` or ``'NONE'``, no volumes will be
            selected.  If 'ALL', selects all volumes.

        sel_type : str, optional
            Selection type.  May be one of the following:

            * ``'S'``: Select a new set (default)
            * ``'R'``: Reselect a set from the current set.
            * ``'A'``: Additionally select a set and extend the current set.
            * ``'U'``: Unselect a set from the current set.

        return_selected : bool, optional
            Return the volume numbers selected.  Optional, and can be
            disabled for performance.  Default ``False``.

        Returns
        -------
        np.array
            Numpy array of keypoint numbers if ``return_selected=True``.

        Examples
        --------
        Create a new selection of volumes [1, 5, 10]

        >>> mapdl.geometry.volume_select([1, 5, 10])

        Create a new selection of volumes from 1 through 20

        >>> mapdl.geometry.volume_select(range(1, 21))

        Unselect volumes 1 through 20

        >>> mapdl.geometry.volume_select(range(1, 21), sel_type='U')

        Append to an existing selection of volumes

        >>> mapdl.geometry.volume_select([1, 2, 3], sel_type='A')

        Reselect from the existing selection of volumes

        >>> mapdl.geometry.volume_select([3, 4, 5], sel_type='R')

        Select no volumes

        >>> mapdl.geometry.volume_select(None)

        Select all volumes

        >>> mapdl.geometry.volume_select('ALL')

        """
        if isinstance(items, str):
            items = items.upper()

        # special cases
        if items is None or items == "NONE":
            self._mapdl.vsel("NONE")
            return

        if items == "ALL":
            self._mapdl.vsel("ALL")
            if return_selected:
                return self.vnum
            return

        self._select_items(items, "VOLU", sel_type)

        if return_selected:
            return self.vnum

    def _select_items(
        self,
        items: Sequence[int],
        item_type: VALID_SELECTION_ENTITY_TP,
        sel_type: VALID_SELECTION_TYPE_TP,
    ) -> None:
        """Select items using FLST.

        Parameters
        ----------
        items : sequence
            Sequence of items.

        item_type : str
            Item lookup type.  One of:

               * 'NODE' : node numbers
               * 'ELEM' : element numbers
               * 'KP' : keypoint numbers
               * 'LINE' : line numbers
               * 'AREA' : area numbers
               * 'VOLU' : volume numbers
               * 'TRACE' : trace points
               * 'COORD' : coordinate locations

        sel_type : str, optional
            Selection type.  Must be one of the following:

            * ``'S'``: Select a new set (default)
            * ``'R'``: Reselect a set from the current set.
            * ``'A'``: Additionally select a set and extend the current set.
            * ``'U'``: Unselect a set from the current set.

        """
        if item_type not in FLST_LOOKUP:
            raise KeyError(f'Invalid ``item_type`` "{item_type}"')

        sel_type = sel_type.upper()
        if sel_type not in VALID_SELECTION_TYPE:
            raise ValueError(
                f'Invalid ``sel_type`` "{sel_type}"\n\n'
                f"Use one of the following:\n{VALID_TYPE_MSG}"
            )

        # convert to a flat array as it's easier for type checking
        items = np.asarray(items)
        if not np.issubdtype(items.dtype, np.number):
            raise TypeError("Item numbers must be a numeric type")
        items = items.ravel().astype(np.int_, copy=False)

        # We can use list or arrays for vmin
        if item_type == "NODE":
            self._mapdl.nsel(sel_type, vmin=items, return_mapdl_output=True)
        elif item_type == "ELEM":
            self._mapdl.esel(sel_type, vmin=items, return_mapdl_output=True)
        elif item_type == "KP":
            self._mapdl.ksel(sel_type, vmin=items, return_mapdl_output=True)
        elif item_type == "LINE":
            self._mapdl.lsel(sel_type, vmin=items, return_mapdl_output=True)
        elif item_type == "AREA":
            self._mapdl.asel(sel_type, vmin=items, return_mapdl_output=True)
        elif item_type == "VOLU":
            self._mapdl.vsel(sel_type, vmin=items, return_mapdl_output=True)
        else:
            raise ValueError(f'Unable to select "{item_type}"')

    def get_elements_per_area(self) -> NDArray[np.int32]:
        """Get the number of elements meshed for each area.

        Returns
        -------
        np.ndarray
            An array with the area id for the first column, and the number of
            elements per each area on the second column.

        """
        anum = self.anum.ravel()

        elem_per_areas = self._mapdl.get_array("area", "", "ATTR", "NELM")
        elem_per_areas = elem_per_areas[anum - 1].ravel()

        return np.vstack((anum, elem_per_areas)).T.astype(np.int32)


class LegacyGeometry(Geometry):
    """Legacy Pythonic representation of the MAPDL CAD geometry.

    This class contains advanced methods for extending geometry building and
    selection within MAPDL.
    """

    def __init__(self, mapdl: Mapdl):
        """Legacy geometry manager

        Class to help to manage geometry representations in an
        :class:`Mapdl instance <ansys.mapdl.core.Mapdl>` instance.

        Parameters
        ----------
        mapdl : ansys.mapdl.core.Mapdl
            Mapdl instance which this class references to.
        """
        super().__init__(mapdl)

    def keypoints(self) -> np.array:  # type: ignore
        """Keypoint coordinates."""
        return super().get_keypoints(return_as_array=True)

    @requires_package("pyvista")
    def lines(self) -> "pv.PolyData":
        """Active lines as a ``pyvista.PolyData`` object."""
        return super().get_lines()  # type: ignore

    @requires_package("pyvista")
    def areas(
        self, quality=1, merge=False
    ) -> Union["pv.PolyData", List["pv.UnstructuredGrid"]]:
        """List of areas from MAPDL represented as a ``pyvista.PolyData`` object.

        Parameters
        ----------
        quality : int, optional
            Quality of the mesh to display.  Values are 1 (worst)
            to 10 (best).

        merge : bool, optional
            Whether to merge areas into a single mesh. The default
            is ``False``, in which case a list of areas is returned.  When ``True``,
            the output is a single mesh.

        Returns
        -------
        list of pyvista.UnstructuredGrid
            List of :class:`pyvista.UnstructuredGrid <pyvista.UnstructuredGrid>` meshes representing
            the active surface areas selected by ``ASEL``.  If
            ``merge=True``, areas are returned as a single merged
            :class:`pyvista.UnstructuredGrid <pyvista.UnstructuredGrid>`.

        Examples
        --------
        Return a list of areas as individual grids.

        >>> areas = mapdl.areas(quality=3)
        >>> areab
        [UnstructuredGrid (0x7f14add95040)
          N Cells:	12
          N Points:	20
          X Bounds:	-2.000e+00, 2.000e+00
          Y Bounds:	0.000e+00, 1.974e+00
          Z Bounds:	0.000e+00, 0.000e+00
          N Arrays:	4,
        UnstructuredGrid (0x7f14add95ca0)
          N Cells:	12
          N Points:	20
          X Bounds:	-2.000e+00, 2.000e+00
          Y Bounds:	0.000e+00, 1.974e+00
          Z Bounds:	5.500e-01, 5.500e-01
          N Arrays:	4,
        ...

        Return a single merged mesh.

        >>> area_mesh = mapdl.areas(quality=3)
        >>> area_mesh
        UnstructuredGrid (0x7f14add95ca0)
          N Cells:	24
          N Points:	30
          X Bounds:	-2.000e+00, 2.000e+00
          Y Bounds:	0.000e+00, 1.974e+00
          Z Bounds:	5.500e-01, 5.500e-01
          N Arrays:	4
        """
        return super().get_areas(quality=quality, return_as_list=not merge)
