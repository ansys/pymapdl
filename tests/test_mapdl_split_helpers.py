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

"""No-MAPDL unit tests for helpers extracted from the core and extended mixins."""

import os
from unittest.mock import MagicMock, Mock, patch

import numpy as np
import pytest

from ansys.mapdl.core._mapdl_core import selection as core_selection
from ansys.mapdl.core._mapdl_core import selection as picker
from ansys.mapdl.core._mapdl_core.execution import _CoreExecutionMixin
from ansys.mapdl.core._mapdl_core.plotting import _CorePlottingMixin
from ansys.mapdl.core._mapdl_extended.plotting_commands import (
    _ExtendedPlottingCommandsMixin,
)
from ansys.mapdl.core.errors import MapdlRuntimeError
from ansys.mapdl.core.mapdl_core import _MapdlCore
from conftest import requires


def _bare_core():
    """Return a ``_MapdlCore`` without running its initializer."""
    instance = object.__new__(_MapdlCore)
    instance._log = MagicMock()
    instance._apdl_log = None
    instance._file_type_for_plots = "PNG"
    return instance


# --------------------------------------------------------------------------
# execution.run helpers
# --------------------------------------------------------------------------


def test_pop_run_kwargs_defaults_and_drops_empty_values():
    kwargs = {"empty": ""}
    assert _CoreExecutionMixin._pop_run_kwargs(kwargs) == (False, False, False)
    assert kwargs == {}


def test_pop_run_kwargs_warns_about_unused_arguments():
    kwargs = {"verbose": True, "savefig": "a.png", "unknown": 1}
    with pytest.warns(UserWarning, match="unknown"):
        result = _CoreExecutionMixin._pop_run_kwargs(kwargs)
    assert result == (True, "a.png", False)


@pytest.mark.parametrize(
    "command,expected",
    [
        ("/CLE", "/CLE,NOSTART"),
        ("/PREP7", "/PREP7"),
    ],
)
def test_preprocess_command_rewrites_clear(command, expected):
    assert _bare_core()._preprocess_command(command, False) == expected


def test_preprocess_command_tracks_show_device():
    core = _bare_core()
    core._preprocess_command("/SHOW,jpeg", False)
    assert core._file_type_for_plots == "JPEG"


@pytest.mark.parametrize("command", ["*IF,A,EQ,1", "/EOF"])
def test_preprocess_command_raises_on_invalid_command(command):
    with pytest.raises(MapdlRuntimeError, match="Invalid PyMAPDL command"):
        _bare_core()._preprocess_command(command, False)


def test_preprocess_command_replaces_silently_ignored_command():
    with patch.dict(
        "ansys.mapdl.core._mapdl_core.execution.INVAL_COMMANDS_SILENT",
        {"/FAKE": "not needed"},
    ):
        command = _bare_core()._preprocess_command("/FAKE,1", False)
    assert command.startswith("/com, PyMAPDL: /FAKE is ignored")


def test_preprocess_command_writes_apdl_log(tmp_path):
    core = _bare_core()
    with open(tmp_path / "apdl.log", "w") as log:
        core._apdl_log = log
        core._preprocess_command("/PREP7", True)
    assert (tmp_path / "apdl.log").read_text() == "/PREP7\n"


@pytest.mark.parametrize(
    "cmd_,checked",
    [("ARG", True), ("/COM", False), ("/TIT", False), ("/SYS", False)],
)
def test_check_parameter_assignment(cmd_, checked):
    core = _bare_core()
    core._check_parameter_name = Mock()
    core._check_parameter_assignment("ARG = 1", cmd_)
    assert core._check_parameter_name.called is checked


def test_process_run_response_handles_empty_text():
    core = _bare_core()
    assert core._process_run_response("", "K", False) is None
    assert core._response is None


def test_process_run_response_returns_response_and_checks_errors():
    core = _bare_core()
    core._ignore_errors = False
    core._raise_errors = Mock()

    response = core._process_run_response(" line1\\nline2 ", "K", False)

    assert response == "line1\nline2"
    core._raise_errors.assert_called_once()


def test_process_run_response_takes_screenshot_for_plot_commands():
    core = _bare_core()
    core._ignore_errors = True
    core.screenshot = Mock(return_value="plot.png")

    with patch("ansys.mapdl.core._mapdl_core.plotting.PLOT_COMMANDS", ["KPLO"]):
        assert core._process_run_response("output", "KPLO", "a.png") == "plot.png"

    core.screenshot.assert_called_once_with(savefig="a.png", default_name="plot")


# --------------------------------------------------------------------------
# plotting.open_gui helpers
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "include_result,inplace,expected",
    [
        (None, None, (True, False)),
        (None, True, (False, True)),
        (False, False, (False, False)),
        (True, None, (True, False)),
    ],
)
def test_resolve_open_gui_options(include_result, inplace, expected):
    result = _CorePlottingMixin._resolve_open_gui_options(include_result, inplace)
    assert result == expected


def test_resolve_open_gui_options_rejects_incompatible_values():
    with pytest.raises(ValueError, match="not compatible"):
        _CorePlottingMixin._resolve_open_gui_options(True, True)


def test_prepare_gui_run_dir_inplace_uses_run_location():
    core = _bare_core()
    core._start_parm = {"run_location": "/my/dir"}
    assert core._prepare_gui_run_dir(True) == "/my/dir"


def test_prepare_gui_run_dir_creates_temporary_directory(tmp_path):
    core = _bare_core()
    with patch("tempfile.gettempdir", return_value=str(tmp_path)):
        run_dir = core._prepare_gui_run_dir(False)
    assert os.path.isdir(run_dir)
    assert os.path.dirname(run_dir) == str(tmp_path)


def test_write_gui_start_files(tmp_path):
    files = _CorePlottingMixin._write_gui_start_files(str(tmp_path), 251)
    assert [os.path.basename(each) for each in files] == ["start251.ans", "start.ans"]
    for each in files:
        assert open(each).read() == "RESUME\n"


def test_resolve_gui_exec_file_prefers_argument():
    assert _bare_core()._resolve_gui_exec_file("/bin/mapdl") == "/bin/mapdl"


def test_resolve_gui_exec_file_falls_back_to_start_parm():
    core = _bare_core()
    core._start_parm = {"exec_file": "/opt/mapdl"}
    with patch("ansys.mapdl.core._HAS_ATC", False):
        assert core._resolve_gui_exec_file(None) == "/opt/mapdl"


def test_resolve_gui_exec_file_raises_when_missing():
    core = _bare_core()
    core._start_parm = {}
    with (
        patch("ansys.mapdl.core._HAS_ATC", False),
        pytest.raises(MapdlRuntimeError, match="executable was not found"),
    ):
        core._resolve_gui_exec_file(None)


# --------------------------------------------------------------------------
# selection XSEL helpers
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "args,kwargs,expected",
    [
        (("S", "P"), {}, True),
        (("S", "p"), {}, True),
        (("S", "NODE"), {}, False),
        (("S",), {"item": "P"}, True),
        ((), {"item": "NODE"}, False),
        ((), {}, False),
    ],
)
def test_is_interactive_xsel(args, kwargs, expected):
    assert core_selection._is_interactive_xsel(args, kwargs) is expected


@pytest.mark.parametrize(
    "command,source,attribute",
    [
        ("nsel", "mesh", "nnum"),
        ("esel", "mesh", "enum"),
        ("ksel", "geometry", "knum"),
        ("lsel", "geometry", "lnum"),
        ("asel", "geometry", "anum"),
        ("vsel", "geometry", "vnum"),
        ("esln", "mesh", "enum"),
        ("nsle", "mesh", "nnum"),
    ],
)
def test_xsel_selected_ids(command, source, attribute):
    core = object.__new__(_MapdlCore)
    method = Mock()
    method.__func__ = Mock(__name__=command)
    expected = np.array([1, 2])
    owner = MagicMock(**{attribute: expected})

    with (
        patch.object(_MapdlCore, "geometry", owner if source == "geometry" else True),
        patch.object(_MapdlCore, "mesh", owner, create=True),
    ):
        assert core._xsel_selected_ids(method) is expected


def test_xsel_selected_ids_without_geometry_or_unknown_command():
    core = object.__new__(_MapdlCore)
    method = Mock()
    method.__func__ = Mock(__name__="other")

    with patch.object(_MapdlCore, "geometry", None):
        assert core._xsel_selected_ids(method) is None
    with patch.object(_MapdlCore, "geometry", True):
        assert core._xsel_selected_ids(method) is None


def test_wrap_xsel_function_returns_ids_or_mapdl_output():
    core = object.__new__(_MapdlCore)
    core._store_commands = False
    core._xsel_mapdl_output = False
    core._xsel_selected_ids = Mock(return_value=[1])

    def nsel(*args, **kwargs):
        """Select nodes."""
        return "MAPDL output"

    wrapped = core._wrap_xsel_function(nsel)

    assert wrapped("S", "NODE") == [1]
    assert wrapped("S", "P") == "MAPDL output"
    assert wrapped("S", "NODE", return_mapdl_output=True) == "MAPDL output"

    core._store_commands = True
    assert wrapped("S", "NODE") == "MAPDL output"


# --------------------------------------------------------------------------
# extended aplot helpers
# --------------------------------------------------------------------------


@requires("matplotlib")
def test_aplot_area_colors_variants():
    anums = np.array([1, 2])
    colors = _ExtendedPlottingCommandsMixin._aplot_area_colors

    assert len(colors(anums, True)) == 2
    assert colors(anums, "red").shape == (1, 4)
    assert len(colors(anums, ["red", "blue"])) == 2
    rgb = [[1, 0, 0], [0, 1, 0]]
    assert colors(anums, rgb) is rgb

    with pytest.raises(ValueError, match="should be the same"):
        colors(anums, ["red"])


@requires("matplotlib")
def test_aplot_area_meshes_default_and_colored():
    surfs = ["s1", "s2"]
    anums = np.array([1, 2])
    instance = object.__new__(_ExtendedPlottingCommandsMixin)

    default = instance._aplot_area_meshes(surfs, anums, False, {"color": "grey"})
    assert default == [
        {"mesh": "s1", "color": "grey"},
        {"mesh": "s2", "color": "grey"},
    ]

    colored = instance._aplot_area_meshes(
        surfs, anums, np.array([[1, 0, 0], [0, 1, 0]]), {}
    )
    assert [each["mesh"] for each in colored] == surfs
    assert np.allclose(colored[1]["color"], [0, 1, 0])


def test_aplot_area_labels_and_sanity_check():
    surf = MagicMock()
    surf.__getitem__.return_value = np.array([3, 3])
    surf.extract_cells.return_value = Mock(center=(0.5, 0.5, 0.0))

    labels = _ExtendedPlottingCommandsMixin._aplot_area_labels([surf], np.array([3]))
    assert labels["labels"].tolist() == [3]
    assert labels["points"].tolist() == [[0.5, 0.5, 0.0]]

    surf.__getitem__.return_value = np.array([3, 4])
    with pytest.raises(RuntimeError, match="contains entities"):
        _ExtendedPlottingCommandsMixin._aplot_area_labels([surf], np.array([3]))


def test_aplot_add_lines():
    instance = object.__new__(_ExtendedPlottingCommandsMixin)
    lines = MagicMock()
    lines.points = np.zeros((200, 3))
    lines.__getitem__.return_value = np.array([1.0, 2.0])
    instance.lsla = Mock()
    geometry = Mock(get_lines=Mock(return_value=lines))
    meshes, labels, kwargs = [], [], {}

    with (
        patch.object(type(instance), "save_selection", MagicMock(), create=True),
        patch.object(type(instance), "geometry", geometry, create=True),
    ):
        instance._aplot_add_lines(meshes, labels, True, True, kwargs)

    assert kwargs["line_width"] == 2
    assert meshes == [{"mesh": lines, "color": "k"}]
    assert labels[0]["labels"].tolist() == [1, 2]
    instance.lsla.assert_called_once_with("S", mute=True)


# --------------------------------------------------------------------------
# picker helpers
# --------------------------------------------------------------------------


def test_format_picked_entities():
    assert picker._format_picked_entities([]) == ""
    assert picker._format_picked_entities([1, 2, 3]) == "3, 2, 1"

    long_text = picker._format_picked_entities(list(range(100)))
    assert long_text.endswith("...")
    assert len(long_text) <= picker._MAX_PICKED_TEXT_LENGTH + 3


def test_update_membership():
    items = [1]
    picker._update_membership(items, 2, True)
    picker._update_membership(items, 2, True)
    assert items == [1, 2]
    picker._update_membership(items, 1, False)
    picker._update_membership(items, 1, False)
    assert items == [2]


@pytest.mark.parametrize(
    "type_,expected",
    [("S", {2, 3}), ("R", {2}), ("A", {1, 2, 3}), ("U", {1})],
)
def test_combine_selection(type_, expected):
    assert picker._combine_selection(type_, {1, 2}, {2, 3}) == expected


def test_picking_text():
    pl = Mock()
    pl.scene._inver_mouse_click_selection = True
    text = core_selection._CoreSelectionMixin._picking_text(
        pl, "node", "A", [1, 2], True
    )
    assert "left mouse button" in text
    assert "Adding to selection" in text
    assert "Mouse selection: Unselecting" in text
    assert text.endswith("Current node selection: 2, 1")


def test_picker_mesh_helpers():
    pl = Mock()
    picked = []

    picker._add_picked_mesh(pl, picked, 5, ["m0", "m1"])
    picker._add_picked_mesh(pl, picked, 5, ["m0", "m1"])
    assert picked == [5]
    assert pl.scene.add_mesh.call_count == 2

    picker._remove_picked_mesh(pl, picked, 5, ["m0", "m1"])
    picker._remove_picked_mesh(pl, picked, 5, ["m0", "m1"])
    assert picked == []
    assert pl.scene.remove_actor.call_count == 2


def test_picker_show_picked_points():
    pl = Mock()
    mesh = Mock(points=np.zeros((3, 3)))

    picker._show_picked_points(pl, mesh, [0, 1])
    pl.scene.add_mesh.assert_called_once()

    picker._show_picked_points(pl, mesh, [])
    pl.scene.remove_actor.assert_called_once_with("_picked_entities")


def test_picker_entity_number():
    mesh = Mock(cell_data={"entity_num": np.array([7, 7])})
    assert picker._entity_number(mesh) == 7
