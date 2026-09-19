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

"""Tests for the coordinate-based node selector (#3845)."""

from contextlib import nullcontext
import gc
import logging
from unittest.mock import MagicMock

import numpy as np
import pytest

from ansys.mapdl.core.mapdl_extended import _MapdlExtended
from ansys.mapdl.core.selector import NodeSelector


class _FakeMapdl(_MapdlExtended):
    """Lightweight double recording MAPDL commands without sending them."""

    def __init__(self):
        self._do_loop_level = 0
        self._store_commands = False
        self._stored_commands = []
        self.sent_commands = []
        self._log = MagicMock()
        self._log.logger.level = logging.WARNING
        self._mesh_mock = MagicMock()
        self._mesh_mock.nnum = np.array([1, 2, 3])
        self._mesh_mock.n_node = 3

    @property
    def mesh(self):
        """Return the test mesh."""
        return self._mesh_mock

    @property
    def save_selection(self):
        """Provide a no-op selection context for command-generation tests."""
        return nullcontext()

    def run(self, command, **kwargs):
        """Record a generated MAPDL command."""
        if self._store_commands:
            self._stored_commands.append(command)
            return None
        self.sent_commands.append(command)
        return command


def _mock_mapdl():
    """Return a MAPDL mock with an existing selected-node result."""
    mapdl = MagicMock()
    mapdl.mesh.nnum = np.array([1, 2, 3])
    mapdl.mesh.n_node = 3
    return mapdl


def _component_names(mapdl):
    """Return component names created by the selector."""
    return [call.args[0] for call in mapdl.cm.call_args_list]


class TestSelectValidation:
    def test_no_criteria_raises_without_mapdl_command(self):
        mapdl = _mock_mapdl()

        with pytest.raises(ValueError, match="requires at least one"):
            NodeSelector(mapdl).select()

        assert mapdl.method_calls == []

    @pytest.mark.parametrize("kwargs", [{"w": 1}, {"x": 1, "X": 2}])
    def test_invalid_keyword_criteria_raise_without_mapdl_command(self, kwargs):
        mapdl = _mock_mapdl()

        with pytest.raises((TypeError, ValueError)):
            NodeSelector(mapdl).select(**kwargs)

        assert mapdl.method_calls == []

    @pytest.mark.parametrize(
        "criterion",
        [
            [],
            (),
            (1,),
            (1, 2, 3),
            (5, 1),
            [1, "not-a-coordinate"],
            True,
            "1",
            {"vmin": 1, "vmax": 2},
            range(1, 3),
            np.array(1),
            np.array([[1, 2]]),
        ],
    )
    def test_invalid_criterion_raises_without_mapdl_command(self, criterion):
        mapdl = _mock_mapdl()

        with pytest.raises((TypeError, ValueError)):
            NodeSelector(mapdl).select(x=criterion)

        assert mapdl.method_calls == []

    @pytest.mark.parametrize("criterion", [np.inf, -np.inf, np.nan, [1, np.nan]])
    def test_non_finite_criterion_raises_without_mapdl_command(self, criterion):
        mapdl = _mock_mapdl()

        with pytest.raises(ValueError, match="finite"):
            NodeSelector(mapdl).select(x=criterion)

        assert mapdl.method_calls == []

    def test_validation_is_atomic_across_axes(self):
        mapdl = _mock_mapdl()

        with pytest.raises(TypeError):
            NodeSelector(mapdl).select(x=17.25, y=[-3, "not-a-coordinate"])

        assert mapdl.method_calls == []


class TestSelectCommandGeneration:
    def test_selection_is_saved_and_restored_after_success(self):
        mapdl = _mock_mapdl()
        selection_context = MagicMock()
        selection_context.__exit__.return_value = False
        mapdl.save_selection = selection_context

        NodeSelector(mapdl).select(x=7)

        selection_context.__enter__.assert_called_once_with()
        selection_context.__exit__.assert_called_once_with(None, None, None)

    def test_scalar_criterion_uses_select(self):
        mapdl = _mock_mapdl()

        result = NodeSelector(mapdl).select(x=7)

        mapdl.nsel.assert_called_once_with("S", "LOC", "X", 7)
        mapdl.cm.assert_not_called()
        assert result is mapdl.mesh.nnum

    def test_list_values_are_selected_with_or_semantics(self):
        mapdl = _mock_mapdl()

        NodeSelector(mapdl).select(y=[11, 23, 42])

        assert [call.args for call in mapdl.nsel.call_args_list] == [
            ("S", "LOC", "Y", 11),
            ("A", "LOC", "Y", 23),
            ("A", "LOC", "Y", 42),
        ]

    @pytest.mark.parametrize(
        ("criterion", "expected"),
        [
            ({42, 7, 19}, [7, 19, 42]),
            (frozenset({42, 7, 19}), [7, 19, 42]),
            (np.array([3, 6]), [3, 6]),
        ],
    )
    def test_sample_collections_are_selected_with_or_semantics(
        self, criterion, expected
    ):
        mapdl = _mock_mapdl()

        NodeSelector(mapdl).select(z=criterion)

        assert [call.args[3] for call in mapdl.nsel.call_args_list] == expected

    def test_tuple_criterion_uses_a_single_inclusive_command(self):
        mapdl = _mock_mapdl()

        NodeSelector(mapdl).select(x=(-4, 9.5))

        mapdl.nsel.assert_called_once_with("S", "LOC", "X", -4, 9.5)

    def test_multiple_axes_use_components_to_preserve_intersection(self):
        mapdl = _mock_mapdl()

        NodeSelector(mapdl).select(x=17.25, y=[-3, 8], z=(100, 125))

        names = _component_names(mapdl)
        assert len(names) == 3
        assert len(set(names)) == 3
        assert [call.args for call in mapdl.cmsel.call_args_list] == [
            ("S", names[0]),
            ("R", names[1]),
            ("R", names[2]),
        ]
        assert {call.args[0] for call in mapdl.cmdele.call_args_list} == set(names)

    def test_axis_order_is_deterministic_regardless_of_keyword_order(self):
        mapdl = _mock_mapdl()

        NodeSelector(mapdl).select(z=(4, 5), x=1)

        names = _component_names(mapdl)
        assert [call.args for call in mapdl.cmsel.call_args_list] == [
            ("S", names[0]),
            ("R", names[1]),
        ]
        assert [call.args[2] for call in mapdl.nsel.call_args_list] == ["X", "Z"]

    def test_empty_selection_uses_server_side_count_without_clearing_again(self):
        mapdl = _mock_mapdl()
        mapdl.mesh.n_node = 0
        mapdl.mesh.nnum = np.empty(0, dtype=np.int32)

        result = NodeSelector(mapdl).select(x=1, y=2)

        assert result is mapdl.mesh.nnum
        mapdl.cm.assert_not_called()
        mapdl.cmsel.assert_not_called()
        assert all(call.args != ("NONE",) for call in mapdl.nsel.call_args_list)

    def test_case_insensitive_axis_alias_has_identical_behavior(self):
        lower_mapdl = _mock_mapdl()
        NodeSelector(lower_mapdl).select(x=5)

        upper_mapdl = _mock_mapdl()
        NodeSelector(upper_mapdl).select(X=5)

        assert lower_mapdl.nsel.call_args_list == upper_mapdl.nsel.call_args_list


class TestSelectCleanup:
    def test_selection_is_restored_after_selection_failure(self):
        mapdl = _mock_mapdl()
        selection_context = MagicMock()
        selection_context.__exit__.return_value = False
        mapdl.save_selection = selection_context
        mapdl.nsel.side_effect = RuntimeError("selection failed")

        with pytest.raises(RuntimeError, match="selection failed"):
            NodeSelector(mapdl).select(x=1)

        selection_context.__exit__.assert_called_once()
        assert selection_context.__exit__.call_args.args[0] is RuntimeError

    def test_temporary_components_are_deleted_after_success(self):
        mapdl = _mock_mapdl()

        NodeSelector(mapdl).select(x=1, y=2)

        names = _component_names(mapdl)
        assert {call.args[0] for call in mapdl.cmdele.call_args_list} == set(names)

    def test_cleanup_runs_after_component_creation_failure(self):
        mapdl = _mock_mapdl()
        mapdl.cm.side_effect = [None, RuntimeError("component creation failed")]

        with pytest.raises(RuntimeError, match="component creation failed"):
            NodeSelector(mapdl).select(x=1, y=2)

        first_component = mapdl.cm.call_args_list[0].args[0]
        assert [call.args[0] for call in mapdl.cmdele.call_args_list] == [
            first_component
        ]

    def test_cleanup_runs_after_combination_failure(self):
        mapdl = _mock_mapdl()
        mapdl.cmsel.side_effect = RuntimeError("combination failed")

        with pytest.raises(RuntimeError, match="combination failed"):
            NodeSelector(mapdl).select(x=1, y=2)

        assert len(mapdl.cmdele.call_args_list) == 2

    def test_cleanup_failure_is_reported_after_successful_selection(self):
        mapdl = _mock_mapdl()
        mapdl.cmdele.side_effect = RuntimeError("cleanup failed")

        with pytest.raises(RuntimeError, match="cleanup failed"):
            NodeSelector(mapdl).select(x=1, y=2)

        assert mapdl.cmdele.call_count == 2


class TestSelectorProperty:
    def test_property_returns_a_cached_selector(self):
        mapdl = _FakeMapdl()

        first = mapdl.selector
        second = mapdl.selector

        assert isinstance(first, NodeSelector)
        assert first is second

    def test_property_does_not_change_nsel_behavior(self):
        mapdl = _FakeMapdl()

        _ = mapdl.selector
        mapdl.nsel("S", "LOC", "X", 1, 2)

        assert mapdl.sent_commands == ["NSEL,S,LOC,X,1,2,,"]

    def test_selector_generates_transport_neutral_commands(self):
        mapdl = _FakeMapdl()

        result = mapdl.selector.select(x=1, y=[2, 3])

        assert result is mapdl.mesh.nnum
        assert mapdl.sent_commands[0] == "NSEL,S,LOC,X,1,,,"
        assert mapdl.sent_commands[2:4] == [
            "NSEL,S,LOC,Y,2,,,",
            "NSEL,A,LOC,Y,3,,,",
        ]
        assert mapdl.sent_commands[1].startswith("CM,PYSEL_X_")
        assert mapdl.sent_commands[4].startswith("CM,PYSEL_Y_")
        assert mapdl.sent_commands[5].startswith("CMSEL,S,PYSEL_X_")
        assert mapdl.sent_commands[6].startswith("CMSEL,R,PYSEL_Y_")
        assert mapdl.sent_commands[7].startswith("CMDELE,PYSEL_X_")
        assert mapdl.sent_commands[8].startswith("CMDELE,PYSEL_Y_")

    def test_selector_raises_after_bound_mapdl_is_collected(self):
        mapdl = _mock_mapdl()
        selector = NodeSelector(mapdl)
        del mapdl
        gc.collect()

        with pytest.raises(RuntimeError, match="no longer exists"):
            selector.select(x=1)
