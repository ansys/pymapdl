"""Module to support MAPDL CAD geometry"""
import re

import numpy as np

from ansys.mapdl.core import _HAS_PYVISTA

if _HAS_PYVISTA:
    import pyvista as pv

from ansys.mapdl.core.misc import run_as_prep7, supress_logging

VALID_TYPE_MSG = """- 'S' : Select a new set (default)
- 'R' : Reselect a set from the current set.
- 'A' : Additionally select a set and extend the current set.
- 'U' : Unselect a set from the current set.
"""

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


def merge_polydata(items):
    """Merge list of polydata or unstructured grids"""

    # lazy import here for faster module loading
    try:
        from pyvista._vtk import vtkAppendPolyData
    except:
        from vtk import vtkAppendPolyData

    afilter = vtkAppendPolyData()
    for item in items:
        afilter.AddInputData(item)
        afilter.Update()

    return pv.wrap(afilter.GetOutput())


def get_elements_per_area(resp):
    """Get the number of elements meshed for each area given the response
    from ``AMESH``.

    GENERATE NODES AND ELEMENTS   IN  ALL  SELECTED AREAS
        ** AREA     1 MESHED WITH      64 QUADRILATERALS,        0 TRIANGLES **
        ** AREA     2 MESHED WITH      64 QUADRILATERALS,        0 TRIANGLES **
        ** AREA     3 MESHED WITH      64 QUADRILATERALS,        0 TRIANGLES **
        ** AREA     4 MESHED WITH      64 QUADRILATERALS,        0 TRIANGLES **
        ** AREA     5 MESHED WITH      64 QUADRILATERALS,        0 TRIANGLES **
        ** AREA     6 MESHED WITH      64 QUADRILATERALS,        0 TRIANGLES **
        ** AREA     7 MESHED WITH      64 QUADRILATERALS,        0 TRIANGLES **
        ** AREA     8 MESHED WITH      64 QUADRILATERALS,        0 TRIANGLES **
        ** AREA     9 MESHED WITH      64 QUADRILATERALS,        0 TRIANGLES **
        ** AREA    10 MESHED WITH      64 QUADRILATERALS,        0 TRIANGLES **
        ** AREA    11 MESHED WITH      64 QUADRILATERALS,        0 TRIANGLES **
        ** AREA    12 MESHED WITH      64 QUADRILATERALS,        0 TRIANGLES **

     NUMBER OF AREAS MESHED     =         12
     MAXIMUM NODE NUMBER        =        772
     MAXIMUM ELEMENT NUMBER     =        768

    Returns
    -------
    list
        List of tuples, each containing the area number and number of
        elements per area.

    """
    # MAPDL changed their output at some point.  Check for both output types.
    reg = re.compile(r"Meshing of area (\d*) completed \*\* (\d*) elements")
    groups = reg.findall(resp)
    if groups:
        groups = [[int(anum), int(nelem)] for anum, nelem in groups]
    else:
        reg = re.compile(r"AREA\s*(\d*).*?(\d*)\s*QUADRILATERALS,\s*(\d*) TRIANGLES")
        groups = reg.findall(resp)
        groups = [(int(anum), int(nquad) + int(ntri)) for anum, nquad, ntri in groups]

    return groups


class Geometry:
    """Pythonic representation of MAPDL CAD geometry

    Contains advanced methods to extend geometry building and
    selection within MAPDL.

    """

    def __init__(self, mapdl):
        from ansys.mapdl.core.mapdl import _MapdlCore

        if not isinstance(mapdl, _MapdlCore):
            raise TypeError("Must be initialized using a gRPC MAPDL class")

        self._mapdl = mapdl
        self._keypoints_cache = None
        self._lines_cache = None
        self._log = self._mapdl._log

    def _set_log_level(self, level):
        return self._mapdl.set_log_level(level)

    def _load_iges(self):
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

    def _reset_cache(self):
        self._keypoints_cache = None
        self._lines_cache = None

    @property
    def _keypoints(self):
        """Returns keypoints cache"""
        if self._keypoints_cache is None:
            self._keypoints_cache = self._load_keypoints()
        return self._keypoints_cache

    @property
    def keypoints(self):
        """Keypoint coordinates"""
        return np.asarray(self._keypoints.points)

    @property
    def _lines(self):
        """Returns lines cache"""
        if self._lines_cache is None:
            self._lines_cache = self._load_lines()
        return self._lines_cache

    @property
    def lines(self):
        """Active lines as a pyvista.PolyData"""
        return self._lines

    def areas(self, quality=4, merge=False):
        """List of areas from MAPDL represented as ``pyvista.PolyData``.

        Parameters
        ----------
        quality : int, optional
            quality of the mesh to display.  Varies between 1 (worst)
            to 10 (best).

        merge : bool, optional
            Option to merge areas into a single mesh. Default
            ``False`` to return a list of areas.  When ``True``,
            output will be a single mesh.

        Returns
        -------
        list of pyvista.UnstructuredGrid
            List of ``pyvista.UnstructuredGrid`` meshes representing
            the active surface areas selected by ``ASEL``.  If
            ``merge=True``, areas are returned as a single merged
            UnstructuredGrid.

        Examples
        --------
        Return a list of areas as indiviudal grids

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
        quality = int(quality)
        if quality > 10:
            raise ValueError("``quality`` parameter must be a value between 0 and 10")
        surf = self.generate_surface(11 - quality)
        if merge:
            return surf

        entity_num = surf["entity_num"]
        areas = []
        anums = np.unique(entity_num)
        for anum in anums:
            areas.append(surf.extract_cells(entity_num == anum))

        return areas

    @supress_logging
    @run_as_prep7
    def generate_surface(self, density=4, amin=None, amax=None, ninc=None):
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
        # store initially selected areas and elements
        with self._mapdl.non_interactive:
            self._mapdl.cm("__tmp_elem__", "ELEM")
            self._mapdl.cm("__tmp_area__", "AREA")
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
        groups = get_elements_per_area(resp)

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
        self._mapdl.cmsel("S", "__tmp_area__", "AREA", mute=True)
        self._mapdl.cmsel("S", "__tmp_elem__", "ELEM", mute=True)

        # store the area number used for each element
        entity_num = np.empty(grid.n_cells, dtype=np.int32)
        if grid and groups:
            # add anum info
            i = 0
            for index, (anum, nelem) in enumerate(groups):
                # have to use original area numbering here as the
                # duplicated areas numbers are inaccurate
                entity_num[i : i + nelem] = orig_anum[index]
                i += nelem
        else:
            entity_num[:] = 0

        pd["entity_num"] = entity_num
        return pd

    @property
    def n_volu(self):
        """
        Number of volumes currently selected.

        Examples
        --------
        >>> mapdl.n_volu
        1
        """
        return self._item_count("VOLU")

    @property
    def n_area(self):
        """
        Number of areas currently selected.

        Examples
        --------
        >>> mapdl.n_area
        1
        """
        return self._item_count("AREA")

    @property
    def n_line(self):
        """
        Number of lines currently selected.

        Examples
        --------
        >>> mapdl.n_line
        1
        """
        return self._item_count("LINE")

    @property
    def n_keypoint(self):
        """
        Number of keypoints currently selected.

        Examples
        --------
        >>> mapdl.n_keypoint
        1
        """
        return self._item_count("KP")

    @supress_logging
    def _item_count(self, entity):
        """Return item count for a given entity."""
        return int(self._mapdl.get(entity=entity, item1="COUNT"))

    @property
    def knum(self):
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
    def lnum(self):
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
    def anum(self):
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
    def vnum(self):
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
    def _load_lines(self):
        """Load lines from MAPDL using IGES"""
        # ignore volumes
        self._mapdl.cm("__tmp_volu__", "VOLU", mute=True)
        self._mapdl.cm("__tmp_line__", "LINE", mute=True)
        self._mapdl.cm("__tmp_area__", "AREA", mute=True)
        self._mapdl.cm("__tmp_keyp__", "KP", mute=True)
        self._mapdl.ksel("ALL", mute=True)
        self._mapdl.lsel("ALL", mute=True)
        self._mapdl.asel("ALL", mute=True)
        self._mapdl.vsel("NONE", mute=True)

        iges = self._load_iges()

        self._mapdl.cmsel("S", "__tmp_volu__", "VOLU", mute=True)
        self._mapdl.cmsel("S", "__tmp_area__", "AREA", mute=True)
        self._mapdl.cmsel("S", "__tmp_line__", "LINE", mute=True)
        self._mapdl.cmsel("S", "__tmp_keyp__", "KP", mute=True)

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
                    line = line.to_vtk(resolution=100)
                    line.cell_data["entity_num"] = entity_num
                    lines.append(line)

        if lines:
            lines = merge_polydata(lines)
            lines["entity_num"] = lines["entity_num"].astype(np.int32)
        else:
            lines = pv.PolyData()

        return lines

    def _load_keypoints(self):
        """Load keypoints from MAPDL using IGES"""
        # write only keypoints
        self._mapdl.cm("__tmp_volu__", "VOLU", mute=True)
        self._mapdl.cm("__tmp_area__", "AREA", mute=True)
        self._mapdl.cm("__tmp_line__", "LINE", mute=True)
        self._mapdl.vsel("NONE", mute=True)
        self._mapdl.asel("NONE", mute=True)
        self._mapdl.lsel("NONE", mute=True)

        iges = self._load_iges()

        self._mapdl.cmsel("S", "__tmp_volu__", "VOLU", mute=True)
        self._mapdl.cmsel("S", "__tmp_area__", "AREA", mute=True)
        self._mapdl.cmsel("S", "__tmp_line__", "LINE", mute=True)

        keypoints = []
        kp_num = []
        for kp in iges.points():
            keypoints.append([kp.x, kp.y, kp.z])
            kp_num.append(int(kp.d["entity_subs_num"]))

        # self._kp_num = np.array(self._kp_num)
        keypoints_pd = pv.PolyData(keypoints)
        keypoints_pd["entity_num"] = kp_num
        return keypoints_pd

    def __str__(self):
        """Current geometry info"""
        info = "MAPDL Selected Geometry\n"
        info += "Keypoints:  %d\n" % self.n_keypoint
        info += "Lines:      %d\n" % self.n_line
        info += "Areas:      %d\n" % self.n_area
        info += "Volumes:    %d\n" % self.n_volu
        return info

    def keypoint_select(self, items, sel_type="S", return_selected=False):
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
        list
            List of keypoint numbers if ``return_selected=True``.

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

    def line_select(self, items, sel_type="S", return_selected=False):
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
        list
            List of the selected lines if ``return_selected=True``.

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

    def area_select(self, items, sel_type="S", return_selected=False):
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
        list
            List of the selected areas if ``return_selected=True``.

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

    def volume_select(self, items, sel_type="S", return_selected=False):
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
        list
            List of the selected volumes if ``return_selected=True``.

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

    def _select_items(self, items, item_type, sel_type):
        """Select items using FLST

        Parameters
        ----------
        areas : sequence
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
        valid_sel_type = ["S", "R", "A", "U"]
        if sel_type not in valid_sel_type:
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
