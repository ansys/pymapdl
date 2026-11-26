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

"""No-MAPDL tests for plot command routing and ``cmplot`` backend kwargs."""

from contextlib import nullcontext
from unittest.mock import MagicMock, patch
import warnings

import pytest

from ansys.mapdl.core._mapdl_core.execution import _CoreExecutionMixin
from ansys.mapdl.core._mapdl_extended.plotting_commands import (
    _ExtendedPlottingCommandsMixin,
)
from ansys.mapdl.core.mapdl_core import PLOT_COMMANDS, parse_to_short_cmd
from ansys.mapdl.core.plotting import GraphicsBackend

# Every single-frame Mechanical APDL display command that writes a PNG.
DISPLAY_COMMANDS = [
    "*VPLOT",
    "/REPLOT",
    "APLOT",
    "CMPLOT",
    "EPLOT",
    "FSPLOT",
    "GPLOT",
    "KPLOT",
    "LAYPLOT",
    "LPLOT",
    "MDPLOT",
    "MPPLOT",
    "NPLOT",
    "PLAS",
    "PLCAMP",
    "PLCFREQ",
    "PLCHIST",
    "PLCINT",
    "PLCKSURF",
    "PLCRACK",
    "PLDISP",
    "PLESOL",
    "PLETAB",
    "PLF2D",
    "PLFAR",
    "PLGEOM",
    "PLLS",
    "PLMAP",
    "PLMC",
    "PLNEAR",
    "PLNSOL",
    "PLORB",
    "PLPAGM",
    "PLPATH",
    "PLSECT",
    "PLTRAC",
    "PLVAR",
    "PLVECT",
    "PLZZ",
    "PSDGRAPH",
    "SECPLOT",
    "SPGRAPH",
    "SPLOT",
    "SUPL",
    "SVPLOT",
    "TBFPLOT",
    "TBPLOT",
    "VPLOT",
]


@pytest.mark.parametrize("command", DISPLAY_COMMANDS)
def test_display_command_is_a_plot_command(command):
    assert parse_to_short_cmd(f"{command},ALL") in PLOT_COMMANDS


@pytest.mark.parametrize(
    "command",
    [
        # Multi-frame animations are not single PNGs.
        "ANCNTR",
        "ANCUT",
        "ANDATA",
        "ANDYNA",
        "ANFLOW",
        "ANHARM",
        "ANIM",
        "ANISOS",
        "ANMODE",
        "ANTIME",
        # Plot settings return status text, not a display.
        "/PLOPTS",
        "PLCPLX",
        "PLTIME",
        # Removed command, must keep raising CommandDeprecated.
        "EDFPLOT",
    ],
)
def test_non_display_command_is_not_a_plot_command(command):
    assert parse_to_short_cmd(f"{command},ALL") not in PLOT_COMMANDS


def test_plot_commands_is_a_sorted_table_without_duplicates():
    assert len(PLOT_COMMANDS) == 47
    assert PLOT_COMMANDS == sorted(set(PLOT_COMMANDS))


@pytest.mark.parametrize(
    "command,expected",
    [
        ("  eplot, all", "EPLO"),
        ("\teplot  ,all", "EPLO"),
        ("/replot,resize", "/REP"),
        ("*vplot,a,b", "*VPL"),
        ("K,,1,0,0,", "K"),
    ],
)
def test_parse_to_short_cmd_ignores_surrounding_whitespace(command, expected):
    assert parse_to_short_cmd(command) == expected


class _ApdlPlotCommands:
    """Generated APDL plot command whose kwargs reach ``run``'s kwarg check."""

    def nplot(self, nnum="", **kwargs):
        _CoreExecutionMixin._pop_run_kwargs(kwargs)


class _OfflineMapdl(_ExtendedPlottingCommandsMixin, _ApdlPlotCommands):
    _graphics_backend = GraphicsBackend.PYVISTA
    components = MagicMock()
    cm = cmsel = MagicMock()

    def _enable_interactive_plotting(self):
        return nullcontext()


@pytest.mark.parametrize(
    "session_backend,call_kwargs",
    [
        (GraphicsBackend.MAPDL, {}),
        (GraphicsBackend.PYVISTA, {"graphics_backend": GraphicsBackend.MAPDL}),
    ],
)
def test_cmplot_mapdl_backend_emits_no_unused_kwarg_warning(
    session_backend, call_kwargs
):
    mapdl = _OfflineMapdl()
    mapdl._graphics_backend = session_backend

    with (
        patch("ansys.mapdl.core.misc._HAS_VISUALIZER", True),
        warnings.catch_warnings(),
    ):
        warnings.simplefilter("error", UserWarning)
        mapdl.cmplot("ALL", "NODE", **call_kwargs)
