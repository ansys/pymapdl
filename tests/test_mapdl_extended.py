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

"""Exercise extended MAPDL behavior without a live solver."""

from unittest.mock import MagicMock, Mock

import numpy as np
import pytest

from ansys.mapdl.core.errors import MapdlRuntimeError
from ansys.mapdl.core.mapdl_extended import _MapdlCommandExtended, _MapdlExtended
from conftest import requires


def _make_mock_mapdl(get_array_return=None):
    """Return a MagicMock carrying what ``get_etable`` needs as ``self``."""
    mock = MagicMock(spec=_MapdlExtended)
    mock._etable_lab_counter = 0

    if get_array_return is None:
        get_array_return = np.array([1.0, 2.0, 3.0])
    mock.get_array.return_value = get_array_return
    return mock


def test_get_etable_default_label_is_hidden_and_cleaned_up():
    mock = _make_mock_mapdl()

    result = _MapdlExtended.get_etable(mock, "S", "X")

    # The column is filled and then erased: two calls to `etable`.
    assert mock.etable.call_count == 2
    fill_call, erase_call = mock.etable.call_args_list

    lab = fill_call.args[0]
    assert fill_call.args == (lab, "S", "X", "")

    # The temporary label must be a valid (<=8 characters) ETABLE label and
    # must not be exposed to the user.
    assert isinstance(lab, str)
    assert 0 < len(lab) <= 8

    # Cleanup issues `ETABLE,Lab,ERAS` and must be muted.
    assert erase_call.args == (lab, "ERAS")
    assert erase_call.kwargs.get("mute") is True

    # The array is retrieved from the same label that was just filled.
    mock.get_array.assert_called_once_with("ELEM", 1, "ETAB", lab)
    np.testing.assert_array_equal(result, np.array([1.0, 2.0, 3.0]))


def test_get_etable_user_label_is_preserved_and_not_erased():
    mock = _make_mock_mapdl()

    result = _MapdlExtended.get_etable(mock, "S", "X", lab="MYLAB")

    # Only one call to `etable`: the fill. No cleanup/erase call is issued
    # since the user explicitly asked to keep the label.
    mock.etable.assert_called_once_with("MYLAB", "S", "X", "")
    mock.get_array.assert_called_once_with("ELEM", 1, "ETAB", "MYLAB")
    np.testing.assert_array_equal(result, np.array([1.0, 2.0, 3.0]))


def test_get_etable_forwards_option_argument():
    mock = _make_mock_mapdl()

    _MapdlExtended.get_etable(mock, "EPTH", "EQV", option="MAX", lab="LAB1")

    mock.etable.assert_called_once_with("LAB1", "EPTH", "EQV", "MAX")


@pytest.mark.parametrize("option", ["MIN", "MAX", "AVG", ""])
def test_get_etable_forwards_option_argument_temp_label(option):
    mock = _make_mock_mapdl()

    _MapdlExtended.get_etable(mock, "S", "X", option=option)

    fill_call = mock.etable.call_args_list[0]
    assert fill_call.args[1:] == ("S", "X", option)


def test_get_etable_forwards_extra_kwargs_to_etable():
    mock = _make_mock_mapdl()

    _MapdlExtended.get_etable(mock, "S", "X", lab="LAB1", mute=True)

    mock.etable.assert_called_once_with("LAB1", "S", "X", "", mute=True)


def test_get_etable_cleans_up_temp_label_even_if_get_array_fails():
    mock = _make_mock_mapdl()
    mock.get_array.side_effect = MapdlRuntimeError("boom")

    with pytest.raises(MapdlRuntimeError, match="boom"):
        _MapdlExtended.get_etable(mock, "S", "X")

    # The fill and the cleanup (erase) calls both still happened, in spite
    # of `get_array` raising in between.
    assert mock.etable.call_count == 2
    fill_call, erase_call = mock.etable.call_args_list
    lab = fill_call.args[0]
    assert erase_call.args == (lab, "ERAS")
    assert erase_call.kwargs.get("mute") is True


def test_get_etable_does_not_erase_user_label_on_failure():
    mock = _make_mock_mapdl()
    mock.get_array.side_effect = MapdlRuntimeError("boom")

    with pytest.raises(MapdlRuntimeError, match="boom"):
        _MapdlExtended.get_etable(mock, "S", "X", lab="KEEPME")

    # Only the fill call happened; the user-supplied label is never erased,
    # even when the retrieval fails.
    mock.etable.assert_called_once_with("KEEPME", "S", "X", "")


def test_get_etable_temp_labels_are_unique_across_calls():
    mock = _make_mock_mapdl()

    _MapdlExtended.get_etable(mock, "S", "X")
    _MapdlExtended.get_etable(mock, "S", "Y")

    # 2 calls (fill+erase) per invocation => 4 calls total, fills are the
    # 1st and 3rd calls.
    fill_calls = [mock.etable.call_args_list[0], mock.etable.call_args_list[2]]
    labels = [c.args[0] for c in fill_calls]

    assert labels[0] != labels[1]
    assert all(len(lab) <= 8 for lab in labels)


@pytest.mark.parametrize("cls", [_MapdlCommandExtended, _MapdlExtended])
@pytest.mark.parametrize("parr, expected", [("", 42), ("norm_result", 84)])
def test_nrm_returns_the_requested_parameter(cls, parr, expected):
    """Return the computed norm rather than the MAPDL command output."""
    instance = object.__new__(cls)
    instance._parameters = {"__temp_par__": 42, "norm_result": 84}
    instance.run = Mock(return_value="MAPDL command output")

    assert instance.nrm(parr=parr) == expected


@pytest.mark.parametrize("cls", [_MapdlCommandExtended, _MapdlExtended])
@pytest.mark.parametrize(
    "print_com, global_mute, command_mute, expected",
    [
        (True, False, None, "/COM,Testing comment\n"),
        (False, False, None, ""),
        (True, True, None, ""),
        (True, False, True, ""),
        (True, True, False, ""),
    ],
)
def test_comment_printing_respects_mute(
    cls, print_com, global_mute, command_mute, expected, capsys
):
    """Global and command muting both suppress printed comments."""
    instance = object.__new__(cls)
    instance._print_com = print_com
    instance.mute = global_mute
    instance.run = Mock()
    kwargs = {} if command_mute is None else {"mute": command_mute}

    instance.com("Testing comment", **kwargs)

    assert capsys.readouterr().out == expected


def test_aplot_area_labels_reject_mixed_entities():
    """Reject surfaces that cannot be assigned one unambiguous area label."""
    from ansys.mapdl.core._mapdl_extended.plotting_commands import (
        _ExtendedPlottingCommandsMixin,
    )

    surface = MagicMock()
    surface.__getitem__.return_value = np.array([3, 3])
    surface.extract_cells.return_value = Mock(center=(0.5, 0.5, 0.0))

    labels = _ExtendedPlottingCommandsMixin._aplot_area_labels([surface], np.array([3]))
    assert labels["labels"].tolist() == [3]
    assert labels["points"].tolist() == [[0.5, 0.5, 0.0]]

    surface.__getitem__.return_value = np.array([3, 4])
    with pytest.raises(RuntimeError, match="contains entities"):
        _ExtendedPlottingCommandsMixin._aplot_area_labels([surface], np.array([3]))


@requires("matplotlib")
def test_aplot_area_colors_validate_per_area_values():
    """Normalize named colors and reject incomplete per-area colors."""
    from ansys.mapdl.core._mapdl_extended.plotting_commands import (
        _ExtendedPlottingCommandsMixin,
    )

    colors = _ExtendedPlottingCommandsMixin._aplot_area_colors
    areas = np.array([1, 2])

    np.testing.assert_array_equal(colors(areas, "red"), [[1, 0, 0, 1]])
    np.testing.assert_array_equal(
        colors(areas, ["red", "blue"]), [[1, 0, 0, 1], [0, 0, 1, 1]]
    )
    with pytest.raises(ValueError, match="should be the same"):
        colors(areas, ["red"])
