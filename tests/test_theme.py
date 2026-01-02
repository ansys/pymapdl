# Copyright (C) 2016 - 2026 ANSYS, Inc. and/or its affiliates.
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

import pytest

from conftest import has_dependency

if not has_dependency("pyvista"):
    pytest.skip(
        allow_module_level=True, reason="Skipping because 'pyvista' is not installed"
    )

import matplotlib
import numpy as np

from ansys.mapdl.core.plotting.theme import (
    MapdlTheme,
    _apply_default_theme,
    get_ansys_cmap,
    get_ansys_color_cycle,
    get_ansys_colors,
)


def test_load_theme():
    MapdlTheme()


def test_apply_default_theme():
    _apply_default_theme()


def test_get_ansys_cmap():
    assert isinstance(get_ansys_cmap(11), matplotlib.colors.LinearSegmentedColormap)


def test_get_ansys_colors():
    assert len(get_ansys_colors(10)) == 10
    assert len(get_ansys_colors(100)) == 100
    assert np.unique(get_ansys_colors(100), axis=0).shape[0] == 100


def test_get_ansys_color_cycle():
    assert len(get_ansys_color_cycle(10)) == 10
    assert len(get_ansys_color_cycle(100)) == 100
    assert np.unique(get_ansys_color_cycle(100), axis=0).shape[0] == 9
