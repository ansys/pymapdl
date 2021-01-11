"""Small or misc tests that don't fit in other test modules"""
import numpy as np
import pyvista as pv

import pytest
from pyvista.plotting import system_supports_plotting

import ansys.mapdl.core as pymapdl
from ansys.mapdl.core import examples


def test_quality():
    archive = pymapdl.Archive(examples.hexarchivefile)
    grid = archive.grid
    qual = pymapdl.quality(grid)
    assert (qual == 1).all()


def test_quality_struct():
    x = np.arange(-10, 10, 5)
    y = np.arange(-10, 10, 5)
    z = np.arange(-10, 10, 5)
    x, y, z = np.meshgrid(x, y, z)
    grid = pv.StructuredGrid(x, y, z)
    qual = pymapdl.quality(grid)
    assert (qual == 1).all()


def test_quality_type_error():
    with pytest.raises(TypeError):
        pymapdl.quality(pv.PolyData())


def test_report():
    report = pymapdl.Report(gpu=system_supports_plotting())
    assert 'PyMAPDL Software and Environment Report' in str(report)
