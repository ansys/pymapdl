# Copyright (C) 2016 - 2026 ANSYS, Inc. and/or its affiliates.
# Copyright (C) 2016 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
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
from typing import Any

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

    PYVISTA = "pyvista"
    MAPDL = "mapdl"


def __getattr__(name: str) -> Any:
    """Lazily import :class:`MapdlTheme <ansys.mapdl.core.plotting.theme.MapdlTheme>`.

    ``MapdlTheme`` pulls in PyVista, Matplotlib, and pandas, which are slow to
    import and are only needed by code that actually plots something. Most of
    ``ansys.mapdl.core`` only needs :class:`GraphicsBackend` from this module,
    so ``MapdlTheme`` is imported on first access instead of at module load
    time, following :pep:`562`.
    """
    if name == "MapdlTheme" and _HAS_VISUALIZER:
        from ansys.mapdl.core.plotting.theme import MapdlTheme

        return MapdlTheme

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
