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

"""No-MAPDL unit tests for helpers extracted from the core mixins and picker."""

from contextlib import nullcontext
import logging
import os
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, Mock, patch

import numpy as np
import pytest

from ansys.mapdl.core._mapdl_core import selection as core_selection
from ansys.mapdl.core._mapdl_core import subsystems as core_subsystems
from ansys.mapdl.core._mapdl_core.execution import _CoreExecutionMixin
from ansys.mapdl.core._mapdl_core.plotting import _CorePlottingMixin
from ansys.mapdl.core._mapdl_core.selection import _CoreSelectionMixin
from ansys.mapdl.core._mapdl_core.subsystems import _CoreSubsystemsMixin
from ansys.mapdl.core.errors import MapdlRuntimeError
from ansys.mapdl.core.mapdl_core import _MapdlCore
from ansys.mapdl.core.plotting import picker
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


def test_skip_xsel_ids_is_scoped_and_restored_after_error():
    core = object.__new__(_MapdlCore)
    core._store_commands = False
    core._xsel_mapdl_output = False
    core._xsel_selected_ids = Mock(return_value=[1])

    def nsel(*args, **kwargs):
        """Select nodes."""

    wrapped = core._wrap_xsel_function(nsel)

    with pytest.raises(RuntimeError, match="body failed"):
        with core._skip_xsel_ids():
            assert wrapped("S", "NODE", mute=True) is None
            raise RuntimeError("body failed")

    core._xsel_selected_ids.assert_not_called()
    assert wrapped("S", "NODE") == [1]


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
    text = picker.MapdlPicker._picking_text(pl, "node", "A", [1, 2], True)
    assert "left mouse button" in text
    assert "Adding to selection" in text
    assert "Mouse selection: Unselecting" in text
    assert text.endswith("Current node selection: 2, 1")


def test_picker_mesh_helpers():
    pl = Mock()
    picked = []

    picker.MapdlPicker._add_picked_mesh(pl, picked, 5, ["m0", "m1"])
    picker.MapdlPicker._add_picked_mesh(pl, picked, 5, ["m0", "m1"])
    assert picked == [5]
    assert pl.scene.add_mesh.call_count == 2

    picker.MapdlPicker._remove_picked_mesh(pl, picked, 5, ["m0", "m1"])
    picker.MapdlPicker._remove_picked_mesh(pl, picked, 5, ["m0", "m1"])
    assert picked == []
    assert pl.scene.remove_actor.call_count == 2


def test_picker_show_picked_points():
    pl = Mock()
    mesh = Mock(points=np.zeros((3, 3)))

    picker.MapdlPicker._show_picked_points(pl, mesh, [0, 1])
    pl.scene.add_mesh.assert_called_once()

    picker.MapdlPicker._show_picked_points(pl, mesh, [])
    pl.scene.remove_actor.assert_called_once_with("_picked_entities")


def test_picker_entity_number():
    mesh = Mock(cell_data={"entity_num": np.array([7, 7])})
    assert picker.MapdlPicker._entity_number(mesh) == 7


# --------------------------------------------------------------------------
# filesystem, result, logging, and selection behavior
# --------------------------------------------------------------------------


def test_list_reads_file_and_logs_only_first_ten_lines(tmp_path):
    lines = [f"line {index}" for index in range(12)]
    listing = tmp_path / "listing.txt"
    listing.write_text("\n".join(lines))
    log = Mock()
    client = SimpleNamespace(directory=tmp_path, _log=log)

    _CoreExecutionMixin._list(client, "/LIST,listing,txt")

    assert client._response == "\n".join(lines)
    log.info.assert_called_once_with("\n".join(lines[:10]))


def test_flush_stored_writes_and_reads_real_temporary_files(tmp_path):
    client = _bare_core()
    client._stored_commands = ["/PREP7", "N,1,0,0,0"]
    client._store_commands = True
    client._response = None

    def send_input(input_file, write_to_log):
        command_file = Path(input_file)
        commands = command_file.read_text()
        output_file = Path(commands.splitlines()[0].split(", ", 1)[1])
        output_file.write_text("MAPDL response\nsecond line")
        assert write_to_log is False
        return "input accepted"

    client.input = Mock(side_effect=send_input)
    apdl_log_path = tmp_path / "apdl.log"
    with (
        patch(
            "ansys.mapdl.core._mapdl_core.execution.tempfile.gettempdir",
            return_value=str(tmp_path),
        ),
        patch(
            "ansys.mapdl.core._mapdl_core.execution.random_string",
            side_effect=["output", "input"],
        ),
        patch("ansys.mapdl.core._mapdl_core.execution.time.sleep"),
        open(apdl_log_path, "w") as apdl_log,
    ):
        client._apdl_log = apdl_log
        _CoreExecutionMixin._flush_stored(client)

    expected_commands = (
        f"/OUTPUT, {tmp_path / 'tmp_output.out'}\n/PREP7\nN,1,0,0,0\n/OUTPUT"
    )
    assert (tmp_path / "tmp_input.inp").read_text() == expected_commands
    assert apdl_log_path.read_text() == expected_commands + "\n"
    assert (tmp_path / "tmp_output.out").read_text() == "MAPDL response\nsecond line"
    assert client._response == "\nMAPDL response\nsecond line"
    assert client._stored_commands == []
    assert client._store_commands is False
    client.input.assert_called_once_with(
        str(tmp_path / "tmp_input.inp"), write_to_log=False
    )


def test_flush_stored_without_commands_disables_storage():
    client = _bare_core()
    client._stored_commands = []
    client._store_commands = True

    _CoreExecutionMixin._flush_stored(client)

    assert client._store_commands is False


@pytest.mark.parametrize("append", [False, True])
def test_file_handler_writes_at_level_and_can_be_removed(tmp_path, append):
    log_path = tmp_path / "mapdl.log"
    if append:
        log_path.write_text("existing entry\n")

    logger = logging.Logger(f"mapdl-split-{append}")
    logger.setLevel(logging.DEBUG)
    client = _bare_core()
    client._log = SimpleNamespace(
        logger=logger, info=logger.info, removeHandler=logger.removeHandler
    )

    client.add_file_handler(log_path, append=append, level="INFO")
    try:
        logger.debug("filtered debug entry")
        logger.info("visible info entry")
        client.remove_file_handler()
        logger.info("entry after removal")
    finally:
        client._log_filehandler.close()

    contents = log_path.read_text()
    assert ("existing entry\n" in contents) is append
    assert "visible info entry" in contents
    assert "filtered debug entry" not in contents
    assert "entry after removal" not in contents
    assert client._log_filehandler not in logger.handlers


def test_selected_mesh_ids_are_independent_copies():
    nodes = np.array([2, 4])
    elements = np.array([8, 9])
    geometry = SimpleNamespace(
        knum=np.array([1]), lnum=np.array([2]), anum=np.array([3]), vnum=np.array([4])
    )
    client = SimpleNamespace(
        mesh=SimpleNamespace(nnum=nodes, enum=elements), geometry=geometry
    )

    selected_nodes = _CoreSelectionMixin._get_selected_(client, "node")
    selected_elements = _CoreSelectionMixin._get_selected_(client, "elem")
    assert selected_nodes.tolist() == [2, 4]
    assert selected_elements.tolist() == [8, 9]
    assert selected_nodes is not nodes
    assert selected_elements is not elements
    selected_nodes[0] = 99
    selected_elements[0] = 99
    assert nodes.tolist() == [2, 4]
    assert elements.tolist() == [8, 9]
    assert _CoreSelectionMixin._get_selected_(client, "kp") is geometry.knum
    assert _CoreSelectionMixin._get_selected_(client, "line") is geometry.lnum
    assert _CoreSelectionMixin._get_selected_(client, "area") is geometry.anum
    assert _CoreSelectionMixin._get_selected_(client, "volu") is geometry.vnum

    with pytest.raises(ValueError, match="not allowed"):
        _CoreSelectionMixin._get_selected_(client, "unknown")


def test_entity_list_selection_appends_and_rejects_replace_mode():
    client = SimpleNamespace()
    select = Mock()

    _CoreSelectionMixin._perform_entity_list_selection(
        client, "NODE", select, "S", "NODE", "", [3, 7], ""
    )

    assert [call.args[1:5] for call in select.call_args_list] == [
        ("S", "NODE", "", 3),
        ("A", "NODE", "", 7),
    ]
    with pytest.raises(NotImplementedError, match="Mode R is not supported"):
        _CoreSelectionMixin._perform_entity_list_selection(
            client, "NODE", select, "R", "NODE", "", [3], ""
        )


def test_distributed_result_file_uses_numeric_suffix_and_latest_file(tmp_path):
    thermal_file = tmp_path / "run7_0.rth"
    structural_file = tmp_path / "run7_0.rst"
    thermal_file.write_text("thermal results")
    structural_file.write_text("structural results")
    os.utime(thermal_file, (1_700_000_000, 1_700_000_000))
    os.utime(structural_file, (1_700_000_010, 1_700_000_010))
    inquire = Mock(return_value="run7")
    client = SimpleNamespace(directory=tmp_path, inquire=inquire, jobname="unused")

    result_file = _CoreSubsystemsMixin._distributed_result_file.fget(client)

    assert result_file == structural_file
    inquire.assert_called_once_with("", "RSTFILE")


@pytest.mark.parametrize("inquire_raises", [False, True])
def test_distributed_result_file_falls_back_to_jobname(tmp_path, inquire_raises):
    result_file = tmp_path / "fallback8_0.rst"
    result_file.write_text("result")
    inquire = Mock(
        side_effect=RuntimeError("inquire unavailable") if inquire_raises else None,
        return_value=None,
    )
    client = SimpleNamespace(directory=tmp_path, inquire=inquire, jobname="fallback8")

    assert _CoreSubsystemsMixin._distributed_result_file.fget(client) == result_file


@pytest.mark.parametrize("extension", ["rth", "rst", None])
def test_distributed_result_file_selects_single_existing_file(tmp_path, extension):
    if extension:
        (tmp_path / f"model0.{extension}").write_text("result")
    client = SimpleNamespace(
        directory=tmp_path, inquire=Mock(return_value="model"), jobname="model"
    )

    result_file = _CoreSubsystemsMixin._distributed_result_file.fget(client)

    assert result_file == (tmp_path / f"model0.{extension}" if extension else None)


@pytest.mark.parametrize(
    ("prioritize_thermal", "expected"),
    [(True, "model.rth"), (False, "model.rst")],
)
def test_result_file_selects_thermal_or_latest_existing_file(
    tmp_path, prioritize_thermal, expected
):
    thermal_file = tmp_path / "model.rth"
    structural_file = tmp_path / "model.rst"
    thermal_file.write_text("thermal")
    structural_file.write_text("structural")
    os.utime(thermal_file, (1_700_000_000, 1_700_000_000))
    os.utime(structural_file, (1_700_000_010, 1_700_000_010))
    inquire = Mock(
        side_effect=lambda _group, item: "model" if item == "RSTFILE" else ""
    )
    client = SimpleNamespace(
        directory=tmp_path,
        inquire=inquire,
        run_as_routine=lambda _routine: nullcontext(),
        jobname="model",
        _local=True,
        _prioritize_thermal=prioritize_thermal,
    )

    assert _CoreSubsystemsMixin._result_file.fget(client) == tmp_path / expected


def test_result_file_uses_reported_extension(tmp_path):
    result_file = tmp_path / "model.rst"
    result_file.write_text("result")
    inquire = Mock(
        side_effect=lambda _group, item: "model" if item == "RSTFILE" else "rst"
    )
    client = SimpleNamespace(
        directory=tmp_path,
        inquire=inquire,
        run_as_routine=lambda _routine: nullcontext(),
        jobname="model",
        _local=True,
        _prioritize_thermal=False,
    )

    assert _CoreSubsystemsMixin._result_file.fget(client) == result_file


@pytest.mark.parametrize(
    ("extension", "prioritize_thermal", "expected"),
    [("rth", True, "model.rth"), ("rst", True, "model.rst"), (None, False, None)],
)
def test_result_file_returns_only_available_thermal_or_structural_file(
    tmp_path, extension, prioritize_thermal, expected
):
    if extension:
        (tmp_path / f"model.{extension}").write_text("result")
    inquire = Mock(
        side_effect=lambda _group, item: "model" if item == "RSTFILE" else ""
    )
    client = SimpleNamespace(
        directory=tmp_path,
        inquire=inquire,
        run_as_routine=lambda _routine: nullcontext(),
        jobname="model",
        _local=True,
        _prioritize_thermal=prioritize_thermal,
    )

    result_file = _CoreSubsystemsMixin._result_file.fget(client)

    assert result_file == (tmp_path / expected if expected else None)


@requires("ansys-mapdl-reader")
@pytest.mark.parametrize(
    ("distributed", "standard", "cyclic", "expected"),
    [
        ("distributed.rst", "standard.rst", True, "standard.rst"),
        ("distributed.rst", "standard.rst", False, "standard.rst"),
        ("distributed.rst", None, False, "distributed.rst"),
        (None, "standard.rst", False, "standard.rst"),
        (None, None, False, None),
    ],
)
def test_result_reads_selected_file_or_reports_missing_results(
    tmp_path, monkeypatch, distributed, standard, cyclic, expected
):
    distributed_path = tmp_path / distributed if distributed else None
    standard_path = tmp_path / standard if standard else None
    for result_path in (distributed_path, standard_path):
        if result_path is not None:
            result_path.write_text("result")
    if distributed_path is not None and standard_path is not None:
        os.utime(distributed_path, (1_700_000_000, 1_700_000_000))
        os.utime(standard_path, (1_700_000_010, 1_700_000_010))

    result_constructor = Mock(return_value=SimpleNamespace(_is_cyclic=cyclic))
    read_binary = Mock(side_effect=lambda path: f"parsed {Path(path).name}")
    monkeypatch.setattr(core_subsystems, "_HAS_DPF", False)
    monkeypatch.setattr("ansys.mapdl.reader.rst.Result", result_constructor)
    monkeypatch.setattr("ansys.mapdl.reader.read_binary", read_binary)
    client = SimpleNamespace(
        _use_reader_backend=True,
        _local=True,
        _distributed_result_file=distributed_path,
        _result_file=standard_path,
        directory=tmp_path,
    )

    if expected is None:
        with pytest.raises(FileNotFoundError, match="No result file"):
            _CoreSubsystemsMixin.result.fget(client)
    else:
        assert _CoreSubsystemsMixin.result.fget(client) == f"parsed {expected}"
        read_binary.assert_called_once_with(tmp_path / expected)
