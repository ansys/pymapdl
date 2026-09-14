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

"""Tests for the high-level, generic coordinate-based node selector (#3845).

These tests pin down the public contract that
``ansys.mapdl.core.selector`` and the lazy ``mapdl.selector`` property must
satisfy. The contract was established test-first before the implementation was
added, and the tests remain focused on behavior rather than implementation
details.

Assumed contract (see ``issue-3845.md`` / ``plan-3845.md``)
-------------------------------------------------------------
* ``ansys.mapdl.core.selector.Interval(vmin=None, vmax=None)`` is a small,
  explicit, inclusive-bounds container used to represent an interval
  criterion. It is intentionally distinct from a plain list/tuple/set/array
  (which always means "OR of discrete values"), and from a bare
  ``range(...)`` object (whose exclusive-stop semantics differ from MAPDL's
  inclusive selection and is therefore rejected with a clear ``TypeError``).
  At least one bound must be supplied, and ``vmin`` must not be greater than
  ``vmax`` when both are given.

* ``ansys.mapdl.core.selector.NodeSelector`` is a small, non-generated class
  that keeps a reference to the owning MAPDL instance and exposes
  ``select(x=None, y=None, z=None, **kwargs)``:

  - Case-insensitive aliases ``X``, ``Y``, ``Z`` are also accepted through
    ``**kwargs``; supplying both cases for the same axis (e.g. ``x`` and
    ``X``) is ambiguous and raises ``ValueError``. Any other keyword raises
    ``TypeError``.
  - Calling ``select()`` with no criteria at all raises ``ValueError`` and
    must not issue *any* MAPDL command.
  - All criteria are validated *before* any MAPDL command is generated, so a
    validation error never leaves a partial selection or an orphaned
    temporary component behind.
  - A scalar numeric criterion selects nodes at that coordinate.
  - A list/tuple/set/``numpy.ndarray`` of numeric values selects nodes
    matching *any* of those values (OR), using MAPDL's own coordinate
    tolerance (``NSEL,S,LOC,...`` then ``NSEL,A,LOC,...`` for the following
    values). Strings, mappings, and empty collections are rejected. Bare
    ``bool`` values are rejected (they are not meaningful coordinates, even
    though ``bool`` is a ``int`` subclass in Python).
  - An ``Interval`` criterion selects nodes whose coordinate lies within the
    inclusive bounds using a single ``NSEL,S,LOC,<axis>,vmin,vmax`` call.
  - Criteria supplied on different axes are combined with AND. Because a
    naive ``NSEL,A`` / ``NSEL,R`` sequence cannot express "OR within an axis,
    AND across axes" without losing the intersection with earlier axes, each
    axis's OR-set is first materialized independently (from the full model)
    into a uniquely named temporary component (``CM``) when more than one
    axis is supplied, and the axes are then combined with ``CMSEL,S`` (first
    axis) followed by ``CMSEL,R`` (every subsequent axis, in ``x``, ``y``,
    ``z`` order regardless of keyword order). Every temporary component is
    deleted with ``CMDELE`` afterwards, both when the call succeeds and when
    an exception occurs while building a later axis (whatever temporary
    components already exist are cleaned up, and the original exception still
    propagates).
  - The method does not restore the caller's previous selection: the
    AND-of-axes selection remains the active MAPDL node selection after the
    call returns.
  - The method returns the selected node numbers, i.e. ``mapdl.mesh.nnum``
    evaluated after the final selection operation.

* ``mapdl.selector`` is a lazily created, cached property (mirroring
  ``mapdl.components``) returning a ``NodeSelector`` bound to that MAPDL
  instance. Adding it must not alter the existing, already-public
  ``mapdl.nsel()`` behavior in any way.
"""

import logging
from unittest.mock import MagicMock, call

import numpy as np
import pytest

from ansys.mapdl.core.errors import ComponentNoData
from ansys.mapdl.core.mapdl_extended import _MapdlExtended
from ansys.mapdl.core.selector import Interval, NodeSelector


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
class _FakeMapdl(_MapdlExtended):
    """Lightweight double bypassing ``_MapdlCore.__init__``.

    Mirrors the ``FakeMapdl`` pattern used in ``tests/test_mapdl.py``: it
    keeps the real, generated ``nsel``/``cm``/``cmsel``/``cmdele`` command
    building machinery (inherited from ``Commands``/``_MapdlExtended``)
    while recording the resulting command strings instead of sending them
    to a real MAPDL instance.
    """

    def __init__(self):
        self._do_loop_level = 0
        self._store_commands = False
        self._stored_commands = []
        self.sent_commands = []
        self._log = MagicMock()
        self._log.logger.level = logging.WARNING
        self._mesh_mock = MagicMock()
        self._mesh_mock.nnum = np.array([1, 2, 3])

    @property
    def mesh(self):
        return self._mesh_mock

    def run(self, command, **kwargs):
        if self._store_commands:
            self._stored_commands.append(command)
            return None
        self.sent_commands.append(command)
        return command


def _mock_mapdl():
    """A bare mock MAPDL instance suitable for unit-testing ``NodeSelector``
    in isolation (no real/launched MAPDL involved)."""
    mock_mapdl = MagicMock()
    mock_mapdl.mesh.nnum = np.array([1, 2, 3])
    return mock_mapdl


def _cm_names(mock_mapdl):
    """Return the component names used in every ``cm(name, "NODE")`` call."""
    return [c.args[0] for c in mock_mapdl.cm.call_args_list]


# ---------------------------------------------------------------------------
# Interval
# ---------------------------------------------------------------------------
class TestInterval:
    def test_both_bounds(self):
        interval = Interval(1, 5)
        assert interval.vmin == 1
        assert interval.vmax == 5

    def test_open_ended_upper(self):
        interval = Interval(vmin=1)
        assert interval.vmin == 1
        assert interval.vmax is None

    def test_open_ended_lower(self):
        interval = Interval(vmax=5)
        assert interval.vmin is None
        assert interval.vmax == 5

    def test_requires_at_least_one_bound(self):
        with pytest.raises(ValueError):
            Interval()

    def test_rejects_reversed_bounds(self):
        with pytest.raises(ValueError):
            Interval(5, 1)

    def test_equality(self):
        assert Interval(1, 2) == Interval(1, 2)
        assert Interval(1, 2) != Interval(1, 3)

    def test_floating_point_bounds(self):
        interval = Interval(-1.5, 2.75)
        assert interval.vmin == -1.5
        assert interval.vmax == 2.75

    @pytest.mark.parametrize("value", [np.inf, -np.inf, np.nan])
    def test_rejects_non_finite_bounds(self, value):
        with pytest.raises(ValueError, match="finite"):
            Interval(vmin=value)


# ---------------------------------------------------------------------------
# Validation errors (no MAPDL command should ever be issued)
# ---------------------------------------------------------------------------
class TestSelectValidation:
    def test_no_criteria_raises(self):
        mock_mapdl = _mock_mapdl()
        selector = NodeSelector(mock_mapdl)

        with pytest.raises(ValueError):
            selector.select()

        assert mock_mapdl.method_calls == []

    def test_unsupported_keyword_raises_type_error(self):
        mock_mapdl = _mock_mapdl()
        selector = NodeSelector(mock_mapdl)

        with pytest.raises(TypeError):
            selector.select(w=1)

        assert mock_mapdl.method_calls == []

    def test_duplicate_axis_alias_raises(self):
        mock_mapdl = _mock_mapdl()
        selector = NodeSelector(mock_mapdl)

        # ``x`` and ``X`` both refer to the same axis: ambiguous.
        with pytest.raises(ValueError):
            selector.select(x=1, X=2)

        assert mock_mapdl.method_calls == []

    def test_empty_collection_raises(self):
        mock_mapdl = _mock_mapdl()
        selector = NodeSelector(mock_mapdl)

        with pytest.raises(ValueError):
            selector.select(x=[])

        assert mock_mapdl.method_calls == []

    def test_non_numeric_entry_raises_type_error(self):
        mock_mapdl = _mock_mapdl()
        selector = NodeSelector(mock_mapdl)

        with pytest.raises(TypeError):
            selector.select(x=[1, "a"])

        assert mock_mapdl.method_calls == []

    def test_validation_is_atomic_across_axes(self):
        """A bad criterion must not leave a valid earlier axis selected."""
        mock_mapdl = _mock_mapdl()
        selector = NodeSelector(mock_mapdl)

        with pytest.raises(TypeError):
            selector.select(x=17.25, y=[-3, "not-a-coordinate"])

        assert mock_mapdl.method_calls == []

    def test_string_criterion_raises_type_error(self):
        mock_mapdl = _mock_mapdl()
        selector = NodeSelector(mock_mapdl)

        # A string is iterable but must never be treated as a collection of
        # coordinate values (that would silently iterate its characters).
        with pytest.raises(TypeError):
            selector.select(x="1")

        assert mock_mapdl.method_calls == []

    def test_mapping_criterion_raises_type_error(self):
        mock_mapdl = _mock_mapdl()
        selector = NodeSelector(mock_mapdl)

        with pytest.raises(TypeError):
            selector.select(x={"vmin": 1, "vmax": 2})

        assert mock_mapdl.method_calls == []

    def test_boolean_criterion_raises_type_error(self):
        mock_mapdl = _mock_mapdl()
        selector = NodeSelector(mock_mapdl)

        # ``bool`` is a subclass of ``int`` in Python but is never a
        # meaningful coordinate value.
        with pytest.raises(TypeError):
            selector.select(x=True)

        assert mock_mapdl.method_calls == []

    def test_bare_range_raises_type_error(self):
        mock_mapdl = _mock_mapdl()
        selector = NodeSelector(mock_mapdl)

        # ``range``'s exclusive stop bound differs from MAPDL's inclusive
        # selection ranges, so it must not be silently accepted.
        with pytest.raises(TypeError):
            selector.select(x=range(14, 18))

        assert mock_mapdl.method_calls == []

    @pytest.mark.parametrize("value", [np.inf, -np.inf, np.nan])
    def test_non_finite_scalar_raises_value_error(self, value):
        mock_mapdl = _mock_mapdl()
        selector = NodeSelector(mock_mapdl)

        with pytest.raises(ValueError, match="finite"):
            selector.select(x=value)

        assert mock_mapdl.method_calls == []

    def test_zero_dimensional_array_raises_clear_type_error(self):
        mock_mapdl = _mock_mapdl()
        selector = NodeSelector(mock_mapdl)

        with pytest.raises(TypeError, match="one-dimensional"):
            selector.select(x=np.array(1))

        assert mock_mapdl.method_calls == []

    def test_multi_dimensional_array_raises_clear_type_error(self):
        mock_mapdl = _mock_mapdl()
        selector = NodeSelector(mock_mapdl)

        with pytest.raises(TypeError, match="one-dimensional"):
            selector.select(x=np.array([[1, 2]]))

        assert mock_mapdl.method_calls == []

    def test_reversed_plain_tuple_is_not_an_interval(self):
        """A plain 2-tuple/list is *not* an interval: it means "OR of two
        discrete values" and therefore (5, 1) is perfectly valid -- it is
        not a "reversed bound" error, unlike ``Interval(5, 1)``."""
        mock_mapdl = _mock_mapdl()
        selector = NodeSelector(mock_mapdl)

        selector.select(x=(5, 1))

        mock_mapdl.nsel.assert_any_call("S", "LOC", "X", 5)
        mock_mapdl.nsel.assert_any_call("A", "LOC", "X", 1)


# ---------------------------------------------------------------------------
# Command generation semantics
# ---------------------------------------------------------------------------
class TestSelectCommandGeneration:
    def test_single_scalar_criterion(self):
        mock_mapdl = _mock_mapdl()
        selector = NodeSelector(mock_mapdl)

        result = selector.select(x=7)

        mock_mapdl.nsel.assert_any_call("S", "LOC", "X", 7)
        mock_mapdl.cm.assert_not_called()
        mock_mapdl.cmsel.assert_not_called()
        mock_mapdl.cmdele.assert_not_called()
        assert result is mock_mapdl.mesh.nnum

    def test_multiple_discrete_values_are_or_within_axis(self):
        mock_mapdl = _mock_mapdl()
        selector = NodeSelector(mock_mapdl)

        selector.select(y=[11, 23, 42])

        mock_mapdl.nsel.assert_any_call("S", "LOC", "Y", 11)
        mock_mapdl.nsel.assert_any_call("A", "LOC", "Y", 23)
        mock_mapdl.nsel.assert_any_call("A", "LOC", "Y", 42)
        # never reselect/unselect for a single-axis OR-only criterion
        for c in mock_mapdl.nsel.call_args_list:
            assert c.args[0] in ("S", "A")

    def test_numpy_array_is_accepted_as_or_values(self):
        mock_mapdl = _mock_mapdl()
        selector = NodeSelector(mock_mapdl)

        selector.select(z=np.array([3, 6]))

        mock_mapdl.nsel.assert_any_call("S", "LOC", "Z", 3)
        mock_mapdl.nsel.assert_any_call("A", "LOC", "Z", 6)

    def test_set_values_are_applied_in_deterministic_order(self):
        mock_mapdl = _mock_mapdl()
        selector = NodeSelector(mock_mapdl)

        selector.select(x={42, 7, 19})

        calls = [
            call.args[3]
            for call in mock_mapdl.nsel.call_args_list
            if call.args[1:3] == ("LOC", "X")
        ]
        assert calls == [7, 19, 42]

    def test_interval_criterion_is_a_single_inclusive_command(self):
        mock_mapdl = _mock_mapdl()
        selector = NodeSelector(mock_mapdl)

        selector.select(x=Interval(-4, 9.5))

        mock_mapdl.nsel.assert_any_call("S", "LOC", "X", -4, 9.5)
        # No separate NSEL call should be needed to express the upper bound.
        loc_x_calls = [
            c for c in mock_mapdl.nsel.call_args_list if c.args[1:3] == ("LOC", "X")
        ]
        assert len(loc_x_calls) == 1

    @pytest.mark.parametrize(
        ("interval", "extent_item", "extent"),
        [
            (Interval(vmin=2), "MXLOC", 100),
            (Interval(vmax=5), "MNLOC", -100),
        ],
    )
    def test_open_ended_interval(self, interval, extent_item, extent):
        mock_mapdl = _mock_mapdl()
        mock_mapdl.get_value.return_value = extent
        selector = NodeSelector(mock_mapdl)

        selector.select(x=interval)

        mock_mapdl.get_value.assert_called_once_with("NODE", 0, extent_item, "X")
        mock_mapdl.nsel.assert_any_call("ALL", mute=True)
        loc_x_calls = [
            c for c in mock_mapdl.nsel.call_args_list if c.args[1:3] == ("LOC", "X")
        ]
        assert loc_x_calls == [
            call(
                "S",
                "LOC",
                "X",
                2 if interval.vmin is not None else -100,
                100 if interval.vmax is None else 5,
            )
        ]

    @pytest.mark.parametrize("extent", ["not-a-number", np.nan])
    def test_invalid_model_extent_raises(self, extent):
        mock_mapdl = _mock_mapdl()
        mock_mapdl.get_value.return_value = extent
        selector = NodeSelector(mock_mapdl)

        with pytest.raises(RuntimeError, match="extent"):
            selector.select(x=Interval(vmin=2))

        mock_mapdl.cm.assert_not_called()

    def test_open_ended_interval_outside_model_is_empty(self):
        mock_mapdl = _mock_mapdl()
        mock_mapdl.get_value.return_value = 1
        selector = NodeSelector(mock_mapdl)

        selector.select(x=Interval(vmin=2))

        mock_mapdl.nsel.assert_any_call("NONE")
        loc_x_calls = [
            c for c in mock_mapdl.nsel.call_args_list if c.args[1:3] == ("LOC", "X")
        ]
        assert loc_x_calls == []

    def test_case_insensitive_axis_alias(self):
        mock_mapdl_lower = _mock_mapdl()
        NodeSelector(mock_mapdl_lower).select(x=5)

        mock_mapdl_upper = _mock_mapdl()
        NodeSelector(mock_mapdl_upper).select(X=5)

        assert (
            mock_mapdl_lower.nsel.call_args_list == mock_mapdl_upper.nsel.call_args_list
        )

    def test_two_axes_are_anded_via_components(self):
        mock_mapdl = _mock_mapdl()
        selector = NodeSelector(mock_mapdl)

        selector.select(x=17.25, y=[-3, 8])

        # A temporary component must be created per axis with criteria.
        assert mock_mapdl.cm.call_count == 2
        names = _cm_names(mock_mapdl)
        assert len(set(names)) == 2  # unique names
        for c in mock_mapdl.cm.call_args_list:
            assert c.args[1] == "NODE"

        name_x, name_y = names

        # Combination: start with the x-set, then intersect with the y-set.
        assert len(mock_mapdl.cmsel.call_args_list) == 2
        assert mock_mapdl.cmsel.call_args_list[0].args == ("S", name_x)
        assert mock_mapdl.cmsel.call_args_list[1].args == ("R", name_y)

        # And every temporary component gets removed afterwards.
        deleted = [c.args[0] for c in mock_mapdl.cmdele.call_args_list]
        assert set(deleted) == {name_x, name_y}

    def test_axis_order_is_deterministic_regardless_of_kwarg_order(self):
        mock_mapdl = _mock_mapdl()
        selector = NodeSelector(mock_mapdl)

        # ``z`` and ``x`` supplied out of natural order.
        selector.select(z=Interval(4, 5), x=1)

        names = _cm_names(mock_mapdl)
        assert len(names) == 2
        name_x, name_z = names

        # x is still processed (and combined) before z.
        assert mock_mapdl.cmsel.call_args_list[0].args == ("S", name_x)
        assert mock_mapdl.cmsel.call_args_list[1].args == ("R", name_z)

        nsel_axes_in_order = [
            c.args[2] for c in mock_mapdl.nsel.call_args_list if c.args[1] == "LOC"
        ]
        assert nsel_axes_in_order.index("X") < nsel_axes_in_order.index("Z")

    def test_three_axes_mixed_discrete_and_interval(self):
        mock_mapdl = _mock_mapdl()
        selector = NodeSelector(mock_mapdl)

        selector.select(x=17.25, y=[-3, 8], z=Interval(100, 125))

        assert mock_mapdl.cm.call_count == 3
        names = _cm_names(mock_mapdl)
        assert len(set(names)) == 3
        name_x, name_y, name_z = names

        assert [c.args for c in mock_mapdl.cmsel.call_args_list] == [
            ("S", name_x),
            ("R", name_y),
            ("R", name_z),
        ]

        deleted = {c.args[0] for c in mock_mapdl.cmdele.call_args_list}
        assert deleted == {name_x, name_y, name_z}

    def test_skips_unspecified_axes(self):
        mock_mapdl = _mock_mapdl()
        selector = NodeSelector(mock_mapdl)

        selector.select(x=13, z=-6)

        used_axes = {
            c.args[2] for c in mock_mapdl.nsel.call_args_list if c.args[1] == "LOC"
        }
        assert used_axes == {"X", "Z"}
        assert mock_mapdl.cm.call_count == 2

    def test_returns_current_mesh_node_numbers(self):
        mock_mapdl = _mock_mapdl()
        mock_mapdl.mesh.nnum = np.array([9, 10, 11])
        selector = NodeSelector(mock_mapdl)

        result = selector.select(x=1)

        assert result is mock_mapdl.mesh.nnum


# ---------------------------------------------------------------------------
# Cleanup semantics
# ---------------------------------------------------------------------------
class TestSelectCleanup:
    def test_temporary_components_are_deleted_after_success(self):
        mock_mapdl = _mock_mapdl()

        # Record the relative order in which cmsel/cmdele are invoked,
        # without disturbing the normal call-recording/return behavior.
        order = []
        mock_mapdl.cmsel.side_effect = lambda *a, **k: order.append("cmsel")
        mock_mapdl.cmdele.side_effect = lambda *a, **k: order.append("cmdele")

        selector = NodeSelector(mock_mapdl)
        selector.select(x=1, y=2)

        names = _cm_names(mock_mapdl)
        deleted = [c.args[0] for c in mock_mapdl.cmdele.call_args_list]
        assert sorted(deleted) == sorted(names)

        # Cleanup happens only once the combination has taken place.
        assert order == ["cmsel", "cmsel", "cmdele", "cmdele"]

    def test_cleanup_runs_and_error_propagates_on_failure(self):
        mock_mapdl = _mock_mapdl()

        # The first axis (``x``) is built successfully and stored in a
        # component; building the second axis (``y``) then fails.
        mock_mapdl.cm.side_effect = [None, RuntimeError("boom")]

        selector = NodeSelector(mock_mapdl)

        with pytest.raises(RuntimeError, match="boom"):
            selector.select(x=1, y=2)

        # The combination step must never have been reached.
        mock_mapdl.cmsel.assert_not_called()

        # But the component that *was* successfully created must still be
        # cleaned up.
        name_x = mock_mapdl.cm.call_args_list[0].args[0]
        deleted = [c.args[0] for c in mock_mapdl.cmdele.call_args_list]
        assert deleted == [name_x]

    def test_cleanup_runs_when_combination_step_fails(self):
        mock_mapdl = _mock_mapdl()
        mock_mapdl.cmsel.side_effect = RuntimeError("combination failed")

        selector = NodeSelector(mock_mapdl)

        with pytest.raises(RuntimeError, match="combination failed"):
            selector.select(x=1, y=2)

        names = _cm_names(mock_mapdl)
        deleted = [c.args[0] for c in mock_mapdl.cmdele.call_args_list]
        assert sorted(deleted) == sorted(names)

    def test_cleanup_failure_is_reported_after_successful_selection(self):
        mock_mapdl = _mock_mapdl()
        mock_mapdl.cmdele.side_effect = RuntimeError("cleanup failed")

        selector = NodeSelector(mock_mapdl)

        with pytest.raises(RuntimeError, match="cleanup failed"):
            selector.select(x=1, y=2)

        # Cleanup is attempted for every temporary component even when the
        # first deletion reports an error.
        assert mock_mapdl.cmdele.call_count == 2

    def test_empty_axis_selection_remains_empty_and_cleans_prior_components(self):
        mock_mapdl = _mock_mapdl()
        mock_mapdl.cm.side_effect = [None, ComponentNoData("empty selection")]

        selector = NodeSelector(mock_mapdl)
        result = selector.select(x=1, y=2)

        assert result is mock_mapdl.mesh.nnum
        mock_mapdl.nsel.assert_any_call("NONE")
        mock_mapdl.cmsel.assert_not_called()
        name_x = mock_mapdl.cm.call_args_list[0].args[0]
        assert [call.args[0] for call in mock_mapdl.cmdele.call_args_list] == [name_x]

    def test_empty_axis_selection_is_detected_without_component_error(self):
        mock_mapdl = _mock_mapdl()
        mock_mapdl.mesh.nnum = np.empty(0, dtype=np.int32)

        selector = NodeSelector(mock_mapdl)
        result = selector.select(x=1, y=2)

        assert result is mock_mapdl.mesh.nnum
        mock_mapdl.nsel.assert_any_call("NONE")
        mock_mapdl.cm.assert_not_called()
        mock_mapdl.cmsel.assert_not_called()


# ---------------------------------------------------------------------------
# ``mapdl.selector`` lazy property + backward compatibility with ``nsel``
# ---------------------------------------------------------------------------
class TestSelectorProperty:
    def test_property_returns_node_selector_bound_to_mapdl(self):
        fake = _FakeMapdl()

        selector = fake.selector

        assert isinstance(selector, NodeSelector)

    def test_property_is_lazily_cached(self):
        fake = _FakeMapdl()

        first = fake.selector
        second = fake.selector

        assert first is second

    def test_property_does_not_change_nsel_behavior(self):
        """Accessing ``mapdl.selector`` must be a pure addition: existing
        ``mapdl.nsel()`` behavior is unaffected."""
        fake = _FakeMapdl()

        _ = fake.selector  # trigger lazy creation

        fake.nsel("S", "LOC", "X", 1, 2)

        assert fake.sent_commands == ["NSEL,S,LOC,X,1,2,,"]

    def test_nsel_unaffected_without_ever_touching_selector(self):
        """Baseline regression check: ``nsel`` keeps working identically
        whether or not ``.selector`` is ever accessed on the instance."""
        fake = _FakeMapdl()

        fake.nsel("S", "LOC", "Y", 3)

        assert fake.sent_commands == ["NSEL,S,LOC,Y,3,,,"]

    def test_selector_uses_transport_neutral_generated_commands(self):
        fake = _FakeMapdl()

        result = fake.selector.select(x=1, y=[2, 3])

        assert result is fake.mesh.nnum
        assert fake.sent_commands[0] == "NSEL,S,LOC,X,1,,,"
        assert fake.sent_commands[2:4] == [
            "NSEL,S,LOC,Y,2,,,",
            "NSEL,A,LOC,Y,3,,,",
        ]
        assert fake.sent_commands[1].startswith("CM,PYSEL_X_")
        assert fake.sent_commands[4].startswith("CM,PYSEL_Y_")
        assert fake.sent_commands[5].startswith("CMSEL,S,PYSEL_X_")
        assert fake.sent_commands[6].startswith("CMSEL,R,PYSEL_Y_")
        assert fake.sent_commands[7].startswith("CMDELE,PYSEL_X_")
        assert fake.sent_commands[8].startswith("CMDELE,PYSEL_Y_")
