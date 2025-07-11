# Copyright (C) 2016 - 2025 ANSYS, Inc. and/or its affiliates.
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

from enum import Enum

from ansys.mapdl.core import _HAS_VISUALIZER
from ansys.mapdl.core.plotting.consts import (
    BC_D,
    BC_F,
    BCS,
    FIELDS,
    FIELDS_ORDERED_LABELS,
    POINT_SIZE,
)
from ansys.mapdl.core.plotting.consts import ALLOWED_TARGETS  # noqa: F401


class GraphicsBackend(Enum):
    """Graphics backend for PyMAPDL.

    This enum is used to set the graphics backend for PyMAPDL.
    """

    PYVISTA: str = "pyvista"
    MAPDL: str = "mapdl"


if _HAS_VISUALIZER:
    from ansys.mapdl.core.plotting.theme import MapdlTheme  # noqa: F401
