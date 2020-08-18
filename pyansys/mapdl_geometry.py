"""Module to support MAPDL CAD geometry"""
import re

from pyiges import Iges
import numpy as np
import pyvista as pv
from vtk import vtkAppendPolyData

from pyansys.misc import supress_logging, run_as_prep7


class Geometry():
    """Pythonic representation of MAPDL CAD geometry"""

    def __init__(self, mapdl):
        from pyansys.mapdl import _MapdlCore
        if not isinstance(mapdl, _MapdlCore):
            raise TypeError('Must be initialized using a MAPDL class')

        self._mapdl = mapdl
        self._keypoints_cache = None
        self._lines_cache = None
        self._log = self._mapdl._log

    def _set_log_level(self, level):
        return self._mapdl.set_log_level(level)

    def _load_iges(self):
        """Loads the iges file from MAPDL as a pyiges class"""
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


    def areas(self, quality=7):
        """List of areas from MAPDL represented as ``pyvista.PolyData``.

        Parameters
        ----------
        quality : int, optional
            quality of the mesh to display.  Varies between 1 (worst)
            to 10 (best).

        Returns
        -------
        areas : list
            List of ``pyvista.PolyData`` areas representing the active
            surface areas selected by ``ASEL``.

        """
        surf = self.generate_surface(11 - quality)

        areas = []
        anums = np.unique(surf['entity_num'])
        for anum in anums:
            areas.append(surf.extract_cells(surf['entity_num'] == anum))
        return areas

    @supress_logging
    @run_as_prep7
    def generate_surface(self, density=5, amin=None, amax=None, ninc=None):
        """Generate an-triangular surface of the active surfaces.

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
        self._mapdl.cm('__tmp_area__', 'AREA')
        self._mapdl.cm('__tmp_elem__', 'ELEM')

        # reselect from existing selection to mimic APDL behavior
        if amin or amax:
            if amax is None:
                amax = amin
            else:
                amax = ''

            if amin is None:  # amax is non-zero
                amin = 1

            if ninc is None:
                ninc = ''

            self._mapdl.asel('R', 'AREA', vmin=amin, vmax=amax, vinc=ninc)

        # duplicate areas to avoid affecting existing areas
        a_num = int(self._mapdl.get(entity='AREA', item1='NUM', it1num='MAXD'))
        self._mapdl.numstr('AREA', a_num)
        self._mapdl.agen(2, 'ALL', noelem=1)
        a_max = int(self._mapdl.get(entity='AREA', item1='NUM', it1num='MAXD'))
        self._mapdl.asel('S', 'AREA', vmin=a_num + 1, vmax=a_max)

        # create a temporary etype
        etype_max = int(self._mapdl.get(entity='ETYP', item1='NUM', it1num='MAX'))
        etype_old = self._mapdl.parameters.type
        etype_tmp = etype_max + 1

        with self._mapdl.chain_commands:
            self._mapdl.et(etype_tmp, 'MESH200', 4)
            self._mapdl.shpp('off')
            self._mapdl.smrtsize(density)
            self._mapdl.type(etype_tmp)

        if self._mapdl.parameters.routine != 'PREP7':
            self._mapdl.prep7()

        resp = self._mapdl.amesh('all')

        # must know the number of elements in each area
        reg = re.compile(r'Meshing of area (\d*) completed \*\* (\d*) elements')
        groups = reg.findall(resp)
        if not groups:
            reg = re.compile(r'AREA\s*(\d*).*?,\s*(\d*) TRIANGLES')
            groups = reg.findall(resp)
        groups = [[int(anum), int(nelem)] for anum, nelem in groups]
        self._mapdl.esla('S')

        grid = self._mapdl.mesh._grid
        pd = pv.PolyData(grid.points, grid.cells)

        pd['ansys_node_num'] = grid['ansys_node_num']
        pd['vtkOriginalPointIds'] = grid['vtkOriginalPointIds']
        # pd.clean(inplace=True)  # TODO: Consider

        # delete all temporary meshes and clean up settings
        with self._mapdl.chain_commands:
            self._mapdl.aclear('ALL')
            self._mapdl.adele('ALL', kswp=1)
            self._mapdl.numstr('AREA', 1)
            self._mapdl.type(etype_old)
            self._mapdl.etdele(etype_tmp)
            self._mapdl.shpp('ON')
            self._mapdl.smrtsize('OFF')
            self._mapdl.cmsel('S', '__tmp_area__', 'AREA')
            self._mapdl.cmsel('S', '__tmp_elem__', 'ELEM')

        entity_num = np.empty(grid.n_cells, dtype=np.int32)
        if grid and groups:
            # add anum info
            i = 0
            for anum, nelem in groups:
                entity_num[i:i+nelem] = anum
                i += nelem
        else:
            entity_num[:] = 0

        grid['entity_num'] = entity_num
        return grid

    @property
    def n_volu(self):
        """Number of volumes currently selected

        Examples
        --------
        >>> mapdl.n_area
        1
        """
        return self._item_count('VOLU')

    @property
    def n_area(self):
        """Number of areas currently selected

        Examples
        --------
        >>> mapdl.n_area
        1
        """
        return self._item_count('AREA')

    @property
    def n_line(self):
        """Number of lines currently selected

        Examples
        --------
        >>> mapdl.n_line
        1
        """
        return self._item_count('LINE')

    @property
    def n_keypoint(self):
        """Number of keypoints currently selected

        Examples
        --------
        >>> mapdl.n_keypoint
        1
        """
        return self._item_count('KP')

    @supress_logging
    def _item_count(self, entity):
        """Return item count for a given entity"""
        return int(self._mapdl.get(entity=entity, item1='COUNT'))

    @property
    def knum(self):
        """Array of keypoint numbers.

        Examples
        --------
        >>> mapdl.block(0, 1, 0, 1, 0, 1)
        >>> mapdl.knum
        array([1, 2, 3, 4, 5, 6, 7, 8], dtype=int32)
        """
        return self._mapdl.get_array('KP', item1='KLIST').astype(np.int32)    

    @property
    def lnum(self):
        """Array of line numbers.

        Examples
        --------
        >>> mapdl.block(0, 1, 0, 1, 0, 1)
        >>> mapdl.lnum
        array([ 1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12], dtype=int32)
        """
        # this (weirdly) sometimes fails
        for _ in range(5):
            lnum = self._mapdl.get_array('LINES', item1='LLIST')
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
        return self._mapdl.get_array('AREA', item1='ALIST').astype(np.int32)

    @property
    def vnum(self):
        """Array of volume numbers.

        Examples
        --------
        >>> mapdl.block(0, 1, 0, 1, 0, 1)
        >>> mapdl.vnum
        array([1], dtype=int32)
        """
        return self._mapdl.get_array('VOLU', item1='VLIST').astype(np.int32)

    @supress_logging
    def _load_lines(self):
        """Load lines from MAPDL using IGES"""
        # ignore volumes
        with self._mapdl.chain_commands:
            self._mapdl.cm('__tmp_volu__', 'VOLU')
            self._mapdl.cm('__tmp_area__', 'AREA')
            self._mapdl.cm('__tmp_keyp__', 'KP')
            self._mapdl.asel('S', 'ALL')
            self._mapdl.ksel('S', 'ALL')
            self._mapdl.vsel('NONE')

        iges = self._load_iges()

        with self._mapdl.chain_commands:
            self._mapdl.cmsel('S', '__tmp_volu__', 'VOLU')
            self._mapdl.cmsel('S', '__tmp_area__', 'AREA')
            self._mapdl.cmsel('S', '__tmp_keyp__', 'KP')

        selected_lnum = self.lnum
        lines = []
        entity_nums = []
        for bspline in iges.bsplines():
            # allow only 10001 as others appear to be construction entities
            if bspline.d['status_number'] == 10001:
                entity_num = int(bspline.d['entity_subs_num'])
                if entity_num not in entity_nums and entity_num in selected_lnum:
                    entity_nums.append(entity_num)
                    line = bspline.to_vtk()
                    line.cell_arrays['entity_num'] = entity_num
                    lines.append(line)

        entites = iges.lines() + iges.circular_arcs()
        for line in entites:
            if line.d['status_number'] == 1:
                entity_num = int(line.d['entity_subs_num'])
                if entity_num not in entity_nums and entity_num in selected_lnum:
                    entity_nums.append(entity_num)
                    line = line.to_vtk(resolution=100)
                    line.cell_arrays['entity_num'] = entity_num
                    lines.append(line)

        if lines:
            afilter = vtkAppendPolyData()
            for line in lines:
                afilter.AddInputData(line)
            afilter.Update()
            lines = pv.wrap(afilter.GetOutput())
            lines['entity_num'] = lines['entity_num'].astype(np.int32)
        else:
            lines = pv.PolyData()

        return lines

    def _load_keypoints(self):
        """Load keypoints from MAPDL using IGES"""
        # write only keypoints
        with self._mapdl.chain_commands:
            self._mapdl.cm('__tmp_volu__', 'VOLU')
            self._mapdl.cm('__tmp_area__', 'AREA')
            self._mapdl.cm('__tmp_line__', 'LINE')
            self._mapdl.vsel('NONE')
            self._mapdl.asel('NONE')
            self._mapdl.lsel('NONE')

        iges = self._load_iges()

        with self._mapdl.chain_commands:
            self._mapdl.cmsel('S', '__tmp_volu__', 'VOLU')
            self._mapdl.cmsel('S', '__tmp_area__', 'AREA')
            self._mapdl.cmsel('S', '__tmp_line__', 'LINE')

        keypoints = []
        kp_num = []
        for kp in iges.points():
            keypoints.append([kp.x, kp.y, kp.z])
            kp_num.append(int(kp.d['entity_subs_num']))

        # self._kp_num = np.array(self._kp_num)
        keypoints_pd = pv.PolyData(keypoints)
        keypoints_pd['entity_num'] = kp_num
        return keypoints_pd

    def __str__(self):
        """Current geometry info"""
        info = 'MAPDL Selected Geometry\n'
        info += 'Keypoints:  %d\n' % self.n_keypoint
        info += 'Lines:      %d\n' % self.n_line
        info += 'Areas:      %d\n' % self.n_area
        info += 'Volumes:    %d\n' % self.n_volu
        return info
