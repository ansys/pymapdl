"""Small or misc tests that don't fit in other test modules"""
import numpy as np
import pyvista as pv

import pytest

import pyansys
from pyvista.plotting import system_supports_plotting
from pyansys import examples


def test_quality():
    archive = pyansys.Archive(examples.hexarchivefile)
    grid = archive.grid
    qual = pyansys.quality(grid)
    assert (qual == 1).all()


def test_quality_struct():
    x = np.arange(-10, 10, 5)
    y = np.arange(-10, 10, 5)
    z = np.arange(-10, 10, 5)
    x, y, z = np.meshgrid(x, y, z)
    grid = pv.StructuredGrid(x, y, z)
    qual = pyansys.quality(grid)
    assert (qual == 1).all()


def test_quality_type_error():
    with pytest.raises(TypeError):
        pyansys.quality(pv.PolyData())


def test_report():
    report = pyansys.Report(gpu=system_supports_plotting())
    assert 'pyansys' in str(report)
