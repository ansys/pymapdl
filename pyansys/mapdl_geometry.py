"""Module to support MAPDL CAD geometry"""
import os

import pyiges
import numpy as np
import pyvista as pv
from vtk import vtkAppendPolyData

from pyansys.misc import supress_logging


class Geometry():
    """Pythonic representation of MAPDL CAD geometry"""

    def __init__(self, mapdl):
        from pyansys.mapdl import _MapdlCore
        if not isinstance(mapdl, _MapdlCore):
            raise TypeError('Must be initialized using a MAPDL class')

        self._mapdl = mapdl

    def _load_iges(self):
        """Loads the iges file from MAPDL as a pyiges class"""
        return pyiges(self._generate_iges())

    @property
    def keypoints(self):
        """Keypoint coordinates"""
        if self._keypoints is None:
            self._load_keypoints()
        return np.asarray(self._keypoints.points)

    @property
    def knum(self):
        """Keypoint numbers"""
        if self._keypoints is None:
            self._load_keypoints()
        return self._keypoints['entity_num']

    @property
    def lines(self):
        """Active lines as a pyvista.PolyData"""
        if self._lines is None:
            self._load_lines()
        return self._lines

    @property
    def _lnum(self):
        """Active lines as a pyvista.PolyData"""
        if self._lines is None:
            self._load_lines()
        return self._lines['entity_num'].astype(np.int32)

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
        anums = np.unique(surf['area_num'])
        for anum in anums:
            areas.append(surf.extract_cells(surf['area_num'] == anum))
        return areas

    @supress_logging
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
            Steps to 
        """

        # disable logging for this function (make this a fixture)
        prior_log_level = self._log.level
        self._log.setLevel('CRITICAL')

        # store initially selected areas
        self.cm('__tmp_area__', 'AREA')

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

            self.asel('R', 'AREA', vmin=amin, vmax=amax, vinc=ninc)

        # duplicate areas to avoid affecting existing areas
        anum_lst = self.anum
        a_num = int(self.get(entity='AREA', item1='NUM', it1num='MAXD'))
        self.numstr('AREA', a_num)
        self.agen(2, 'ALL', noelem=1)
        a_max = int(self.get(entity='AREA', item1='NUM', it1num='MAXD'))
        self.asel('S', 'AREA', vmin=a_num + 1, vmax=a_max)

        # create a temporary etype
        etype_tmp = int(self.get(entity='ETYP', item1='NUM', it1num='MAX'))

        self.et(etype_tmp, 'MESH200', 4)

        self.shpp('off')
        self.smrtsize(density)
        out = self.amesh('all')

        # must know the number of elements in each area
        reg = re.compile('Meshing of area (\d*) completed \*\* (\d*) elements')
        groups = reg.findall(out)
        groups = [[int(anum), int(nelem)] for anum, nelem in groups]
        self.esla('S')

        archive = self._transfer_archive()

        # delete all temporary meshes and clean up settings
        self.aclear('ALL')
        self.adele('ALL', kswp=1)
        self.numstr('AREA', 1)
        self.cmsel('S', '__tmp_area__', 'AREA')
        self.etdele(etype_tmp)
        self.shpp('ON')
        self.smrtsize('OFF')

        self.cmsel('S', '__tmp_area__', 'AREA')

        filename = os.path.join(self.path, 'tmp.cdb')
        self.cdwrite('DB', filename)

        self._log.setLevel(prior_log_level)

        grid = archive._parse_vtk(fix_midside=False, additional_checking=True)
        if grid:
            # add anum info
            i = 0
            area_num = np.empty(grid.n_cells, dtype=np.int32)
            for anum, nelem in groups:
                area_num[i:i+nelem] = anum
                i+= nelem

            grid['area_num'] = area_num
            return grid

    @property
    def n_area(self):
        """Number of areas currently selected

        Examples
        --------
        >>> mapdl.n_area
        1
        """
        return int(self._mapdl.get(entity='AREA', item1='COUNT'))

    @property
    def n_keypoint(self):
        """Number of keypoints currently selected

        Examples
        --------
        >>> mapdl.n_keypoint
        1
        """
        return int(self._mapdl.get(entity='KP', item1='COUNT'))

    @property
    @supress_logging
    def anum(self):
        """List of area numbers"""
        anum = []
        for line in self.alist().splitlines():
            try:
                anum.append(int(line.split()[0]))
            except:
                pass
        return anum

    @property
    @supress_logging
    def lnum(self):
        """List of area numbers"""
        lnum = []
        for line in self.llist().splitlines():
            try:
                lnum.append(int(line.split()[0]))
            except:
                pass
        return lnum

    @supress_logging
    def _load_lines(self):
        """Load lines from MAPDL using IGES"""
        # ignore volumes
        self.cm('__tmp_volu__', 'VOLU')
        self.cm('__tmp_area__', 'AREA')
        self.cm('__tmp_keyp__', 'KP')
        self.asel('S', 'ALL')
        self.ksel('S', 'ALL')
        self.vsel('NONE')
        iges = self._load_iges()

        self.cmsel('S', '__tmp_volu__', 'VOLU')
        self.cmsel('S', '__tmp_area__', 'AREA')
        self.cmsel('S', '__tmp_keyp__', 'KP')

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
            [afilter.AddInputData(line) for line in lines]
            afilter.Update()
            self._lines = pv.wrap(afilter.GetOutput())
        else:
            lines = pv.PolyData()

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

        iges = self._mapdl._load_iges()

        self.cmsel('S', '__tmp_volu__', 'VOLU')
        self.cmsel('S', '__tmp_area__', 'AREA')
        self.cmsel('S', '__tmp_line__', 'LINE')

        keypoints = []
        kp_num = []
        for kp in iges.points():
            keypoints.append([kp.x, kp.y, kp.z])
            kp_num.append(int(kp.d['entity_subs_num']))

        # self._kp_num = np.array(self._kp_num)
        self._keypoints = pv.PolyData(keypoints)
        self._keypoints['entity_num'] = kp_num


# geom = Geometry(mapdl)
# geom._load_keypoints()
