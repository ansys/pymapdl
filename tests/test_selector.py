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
import ansys.mapdl.core.selector as selector_module
from ansys.mapdl.core.selector import NodeSelector
from conftest import requires


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


class _FailingNselMapdl(_FakeMapdl):
    """Fake whose ``NSEL,A`` command for ``Y`` is recorded and then fails."""

    def run(self, command, **kwargs):
        if command.startswith("NSEL,A,LOC,Y,"):
            self.sent_commands.append(command)
            raise RuntimeError("NSEL failed")
        return super().run(command, **kwargs)


@pytest.fixture
def fixed_component_name(monkeypatch):
    """Make the temporary component name deterministic."""
    monkeypatch.setattr(selector_module, "random_string", lambda *args, **kwargs: "TMP")


class TestSelectValidation:
    def test_no_criteria_raises_without_mapdl_command(self):
        mapdl = _FakeMapdl()

        with pytest.raises(ValueError, match="requires at least one"):
            NodeSelector(mapdl).select()

        assert mapdl.sent_commands == []

    def test_unknown_keyword_raises_without_mapdl_command(self):
        mapdl = _FakeMapdl()

        with pytest.raises(TypeError):
            NodeSelector(mapdl).select(w=1)

        assert mapdl.sent_commands == []

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
        mapdl = _FakeMapdl()

        with pytest.raises((TypeError, ValueError)):
            NodeSelector(mapdl).select(x=criterion)

        assert mapdl.sent_commands == []

    @pytest.mark.parametrize("criterion", [np.inf, -np.inf, np.nan, [1, np.nan]])
    def test_non_finite_criterion_raises_without_mapdl_command(self, criterion):
        mapdl = _FakeMapdl()

        with pytest.raises(ValueError, match="finite"):
            NodeSelector(mapdl).select(x=criterion)

        assert mapdl.sent_commands == []

    def test_validation_is_atomic_across_axes(self):
        mapdl = _FakeMapdl()

        with pytest.raises(TypeError):
            NodeSelector(mapdl).select(x=17.25, y=[-3, "not-a-coordinate"])

        assert mapdl.sent_commands == []


class TestSelectCommandGeneration:
    def test_scalar_criterion_sends_one_nsel(self):
        mapdl = _FakeMapdl()

        result = NodeSelector(mapdl).select(x=7)

        assert mapdl.sent_commands == ["NSEL,S,LOC,X,7,,,"]
        np.testing.assert_array_equal(result, [1, 2, 3])

    def test_list_values_are_selected_with_or_semantics(self):
        mapdl = _FakeMapdl()

        NodeSelector(mapdl).select(y=[11, 23, 42])

        assert mapdl.sent_commands == [
            "NSEL,S,LOC,Y,11,,,",
            "NSEL,A,LOC,Y,23,,,",
            "NSEL,A,LOC,Y,42,,,",
        ]

    @pytest.mark.parametrize(
        ("criterion", "expected"),
        [
            (
                {42, 7, 19},
                ["NSEL,S,LOC,Z,7,,,", "NSEL,A,LOC,Z,19,,,", "NSEL,A,LOC,Z,42,,,"],
            ),
            (
                frozenset({42, 7, 19}),
                ["NSEL,S,LOC,Z,7,,,", "NSEL,A,LOC,Z,19,,,", "NSEL,A,LOC,Z,42,,,"],
            ),
            (np.array([3, 6]), ["NSEL,S,LOC,Z,3,,,", "NSEL,A,LOC,Z,6,,,"]),
        ],
    )
    def test_sample_collections_are_selected_with_or_semantics(
        self, criterion, expected
    ):
        mapdl = _FakeMapdl()

        NodeSelector(mapdl).select(z=criterion)

        assert mapdl.sent_commands == expected

    def test_tuple_criterion_sends_one_inclusive_nsel(self):
        mapdl = _FakeMapdl()

        NodeSelector(mapdl).select(x=(-4, 9.5))

        assert mapdl.sent_commands == ["NSEL,S,LOC,X,-4,9.5,,"]

    def test_single_and_multi_value_axes_need_no_component(self):
        mapdl = _FakeMapdl()

        NodeSelector(mapdl).select(x=1, y=[1, 2], z=(0, 5))

        assert mapdl.sent_commands == [
            "NSEL,S,LOC,Y,1,,,",
            "NSEL,A,LOC,Y,2,,,",
            "NSEL,R,LOC,X,1,,,",
            "NSEL,R,LOC,Z,0,5,,",
        ]

    def test_second_multi_value_axis_intersects_through_a_component(
        self, fixed_component_name
    ):
        mapdl = _FakeMapdl()

        NodeSelector(mapdl).select(x=[1, 2], y=[2, 3])

        assert mapdl.sent_commands == [
            "NSEL,S,LOC,X,1,,,",
            "NSEL,A,LOC,X,2,,,",
            "CM,PYSEL_Y_TMP,NODE,,",
            "NSEL,S,LOC,Y,2,,,",
            "NSEL,A,LOC,Y,3,,,",
            "CMSEL,R,PYSEL_Y_TMP,",
            "CMDELE,PYSEL_Y_TMP",
        ]

    def test_multi_value_axes_run_first_in_axis_order(self):
        mapdl = _FakeMapdl()

        NodeSelector(mapdl).select(z=(4, 5), y=[1, 2], x=7)

        assert mapdl.sent_commands == [
            "NSEL,S,LOC,Y,1,,,",
            "NSEL,A,LOC,Y,2,,,",
            "NSEL,R,LOC,X,7,,,",
            "NSEL,R,LOC,Z,4,5,,",
        ]

    def test_empty_intermediate_selection_sends_no_component(self):
        mapdl = _FakeMapdl()
        mapdl._mesh_mock.n_node = 0
        mapdl._mesh_mock.nnum = np.empty(0, dtype=np.int32)

        result = NodeSelector(mapdl).select(x=[1, 2], y=[2, 3])

        assert mapdl.sent_commands == ["NSEL,S,LOC,X,1,,,", "NSEL,A,LOC,X,2,,,"]
        assert result.size == 0


class TestSelectTemporaryComponent:
    def test_component_is_deleted_when_second_multi_value_nsel_fails(
        self, fixed_component_name
    ):
        mapdl = _FailingNselMapdl()

        with pytest.raises(RuntimeError, match="NSEL failed"):
            NodeSelector(mapdl).select(x=[1, 2], y=[2, 3])

        assert mapdl.sent_commands == [
            "NSEL,S,LOC,X,1,,,",
            "NSEL,A,LOC,X,2,,,",
            "CM,PYSEL_Y_TMP,NODE,,",
            "NSEL,S,LOC,Y,2,,,",
            "NSEL,A,LOC,Y,3,,,",
            "CMDELE,PYSEL_Y_TMP",
        ]


@requires("grpc")
def test_select_with_live_mapdl_restores_prior_node_selection(
    mapdl, clear_at_start_and_end
):
    nodes = {
        10: (1, 2, 0),
        11: (1, 3, 1),
        12: (1, 2, 2),
        13: (1, 4, 1),
        14: (2, 2, 1),
        15: (1, 3, 3),
        99: (-1, -1, -1),
    }
    for node_id, coordinates in nodes.items():
        mapdl.n(node_id, *coordinates)

    mapdl.nsel("S", "NODE", vmin=99)
    prior_selection = np.array([99], dtype=np.int32)
    np.testing.assert_array_equal(mapdl.mesh.nnum, prior_selection)

    selected = mapdl.selector.select(x=1, y=[2, 3], z=(0, 2))
    np.testing.assert_array_equal(selected, np.array([10, 11, 12], dtype=np.int32))
    np.testing.assert_array_equal(mapdl.mesh.nnum, prior_selection)

    # Two multi-value axes take the temporary component path.
    selected = mapdl.selector.select(x=[1, 2], y=[2, 3])
    np.testing.assert_array_equal(
        selected, np.array([10, 11, 12, 14, 15], dtype=np.int32)
    )
    np.testing.assert_array_equal(mapdl.mesh.nnum, prior_selection)

    # Two multi-value axes with no matching node hit the n_node == 0 early stop.
    selected = mapdl.selector.select(x=[1000, 2000], y=[2, 3])
    np.testing.assert_array_equal(selected, np.empty(0, dtype=np.int32))
    np.testing.assert_array_equal(mapdl.mesh.nnum, prior_selection)


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

    def test_selector_raises_after_bound_mapdl_is_collected(self):
        mapdl = _FakeMapdl()
        selector = NodeSelector(mapdl)
        del mapdl
        gc.collect()

        with pytest.raises(RuntimeError, match="no longer exists"):
            selector.select(x=1)
