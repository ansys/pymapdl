import os

from vtki import examples as vtki_examples
import vtki
import vtk
from vtk import VTK_TETRA
import pytest
import numpy as np

import pyansys
from pyansys import examples


from vtk import VTK_TETRA
from vtk import VTK_QUADRATIC_TETRA
from vtk import VTK_PYRAMID
from vtk import VTK_QUADRATIC_PYRAMID
from vtk import VTK_WEDGE
from vtk import VTK_QUADRATIC_WEDGE
from vtk import VTK_HEXAHEDRON
from vtk import VTK_QUADRATIC_HEXAHEDRON


LINEAR_CELL_TYPES = [VTK_TETRA,
                     VTK_PYRAMID,
                     VTK_WEDGE,
                     VTK_HEXAHEDRON]

QUADRATIC_CELL_TYPES = [VTK_QUADRATIC_TETRA,
                        VTK_QUADRATIC_PYRAMID,
                        VTK_QUADRATIC_WEDGE,
                        VTK_QUADRATIC_HEXAHEDRON]

try:
    test_path = os.path.dirname(os.path.abspath(__file__))
    testfiles_path = os.path.join(test_path, 'test_data')
except:
    testfiles_path = '/home/alex/afrl/python/source/pyansys/tests/archive/test_data'


archive_file = os.path.join(testfiles_path, 'all_solid_cells.cdb')
archive = pyansys.Archive(archive_file)
linear_grid = archive.parse_vtk(force_linear=True)

celltype = VTK_TETRA
mask = linear_grid.celltypes == celltype
assert mask.any()
linear_grid = linear_grid.extract_cells(mask)

try:
    tmp_archive_file = str(tmpdir.mkdir("tmpdir").join('tmp.cdb'))
except:
    tmp_archive_file = '/tmp/nblock.cdb'

pyansys.save_as_archive(tmp_archive_file, linear_grid)
new_archive = pyansys.Archive(tmp_archive_file)
new_linear_grid = new_archive.parse_vtk()
assert np.allclose(linear_grid.cells, new_linear_grid.cells)
assert np.allclose(linear_grid.points, new_linear_grid.points)
