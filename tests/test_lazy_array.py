# Copyright (C) 2016 - 2026 ANSYS, Inc. and/or its affiliates.
# Copyright (C) 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
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

"""Unit tests for lazy MAPDL array retrieval without a MAPDL instance."""

from unittest.mock import MagicMock, call

import numpy as np
import pytest

from ansys.mapdl.core.lazy_array import LazyArray
from ansys.mapdl.core.mapdl import MapdlBase
from ansys.mapdl.core.mapdl_grpc import MapdlGrpc


@pytest.fixture
def mock_mapdl():
    """Return a mock MAPDL instance with a mocked ``parameters`` mapping."""
    mapdl = MagicMock()
    mapdl.parameters = MagicMock()
    mapdl.parameters.__getitem__ = MagicMock(return_value=np.array([1.0, 2.0, 3.0]))
    return mapdl


def test_no_download_on_creation(mock_mapdl):
    """Creating a LazyArray must not trigger any parameter retrieval."""
    LazyArray(mock_mapdl, "A")
    mock_mapdl.parameters.__getitem__.assert_not_called()


def test_resolve_on_array_conversion(mock_mapdl):
    """np.asarray(...) must trigger exactly one retrieval."""
    lazy = LazyArray(mock_mapdl, "A")

    result = np.asarray(lazy)

    np.testing.assert_array_equal(result, [1.0, 2.0, 3.0])
    mock_mapdl.parameters.__getitem__.assert_called_once_with("A")


def test_resolve_is_cached(mock_mapdl):
    """Repeated usage must only download the parameter once."""
    lazy = LazyArray(mock_mapdl, "A")

    np.asarray(lazy)
    _ = lazy[0]
    _ = len(lazy)
    list(lazy)
    repr(lazy)

    mock_mapdl.parameters.__getitem__.assert_called_once_with("A")


def test_getitem(mock_mapdl):
    lazy = LazyArray(mock_mapdl, "A")

    assert lazy[0] == 1.0
    assert lazy[1] == 2.0


def test_len(mock_mapdl):
    lazy = LazyArray(mock_mapdl, "A")

    assert len(lazy) == 3


def test_iter(mock_mapdl):
    lazy = LazyArray(mock_mapdl, "A")

    assert list(lazy) == [1.0, 2.0, 3.0]


def test_repr(mock_mapdl):
    lazy = LazyArray(mock_mapdl, "A")

    assert repr(lazy) == repr(np.array([1.0, 2.0, 3.0]))


def test_numpy_operations(mock_mapdl):
    """LazyArray must behave like a ndarray for common NumPy operations."""
    lazy = LazyArray(mock_mapdl, "A")

    assert np.sum(lazy) == 6.0
    assert np.mean(lazy) == 2.0
    np.testing.assert_array_equal(lazy + 1, [2.0, 3.0, 4.0])


def test_inplace_ufunc_writes_to_lazy_output(mock_mapdl):
    """In-place ufuncs must update the resolved array without recursion."""
    lazy = LazyArray(mock_mapdl, "A")

    lazy += 1

    np.testing.assert_array_equal(np.asarray(lazy), [2.0, 3.0, 4.0])
    mock_mapdl.parameters.__getitem__.assert_called_once_with("A")


def test_setitem_delegates_to_resolved_array(mock_mapdl):
    lazy = LazyArray(mock_mapdl, "A")

    lazy[0] = 9.0

    np.testing.assert_array_equal(np.asarray(lazy), [9.0, 2.0, 3.0])
    mock_mapdl.parameters.__getitem__.assert_called_once_with("A")


def test_bool_delegates_to_resolved_array(mock_mapdl):
    mock_mapdl.parameters.__getitem__.return_value = np.array([0.0])
    lazy = LazyArray(mock_mapdl, "A")

    assert not lazy

    mock_mapdl.parameters.__getitem__.return_value = np.array([1.0, 2.0])
    with pytest.raises(ValueError, match="truth value"):
        bool(LazyArray(mock_mapdl, "B"))


def test_ndarray_method_delegation(mock_mapdl):
    """ndarray methods used by existing get_array callers must resolve lazily."""
    lazy = LazyArray(mock_mapdl, "A")

    assert lazy.max() == 3.0
    assert lazy.shape == (3,)
    mock_mapdl.parameters.__getitem__.assert_called_once_with("A")


def test_dtype_conversion(mock_mapdl):
    lazy = LazyArray(mock_mapdl, "A")

    result = np.asarray(lazy, dtype=np.int32)

    assert result.dtype == np.int32
    np.testing.assert_array_equal(result, [1, 2, 3])


def test_not_instance_of_ndarray(mock_mapdl):
    """LazyArray is intentionally not an ndarray subclass (see docstring)."""
    lazy = LazyArray(mock_mapdl, "A")

    assert not isinstance(lazy, np.ndarray)


def _mock_grpc_mapdl():
    """Create the portion of MapdlGrpc needed by lazy retrieval methods."""
    mapdl = object.__new__(MapdlGrpc)
    mapdl._log = MagicMock()
    mapdl._log.level = "WARNING"
    mapdl._set_log_level = MagicMock()
    mapdl._store_commands = False
    mapdl._lazy_array_counter = 0
    mapdl._lazy_array_parameters = set()
    mapdl._parameters = MagicMock()
    mapdl._parameters.__contains__.return_value = False
    mapdl._parameters.full_parameters_output = MagicMock()
    mapdl.run = MagicMock()
    mapdl.starvget = MagicMock(return_value="")
    return mapdl


def test_vget_downloads_values_eagerly(monkeypatch):
    """VGET must retain its caller-owned, eager-result semantics."""
    mapdl = _mock_grpc_mapdl()
    commands = []
    first = np.array([1.0, 2.0])
    second = np.array([4.0, 7.0])
    mapdl.parameters.__getitem__.side_effect = [first, second]
    monkeypatch.setattr(
        MapdlBase, "vget", lambda self, **kwargs: commands.append(kwargs)
    )

    before = mapdl.vget(par="A", ir=1)
    after = mapdl.vget(par="A", ir=2)

    np.testing.assert_array_equal(before, first)
    np.testing.assert_array_equal(after, second)
    assert commands == [
        {"par": "A", "ir": 1, "tstrt": "", "kcplx": ""},
        {"par": "A", "ir": 2, "tstrt": "", "kcplx": ""},
    ]
    assert not mapdl._lazy_array_parameters
    mapdl.starvget.assert_not_called()


def test_vget_preserves_store_commands(monkeypatch):
    """VGET must not retrieve a parameter while storing commands."""
    mapdl = _mock_grpc_mapdl()
    mapdl._store_commands = True
    monkeypatch.setattr(MapdlBase, "vget", lambda self, **kwargs: None)

    assert mapdl.vget(par="NODE") is None
    mapdl.parameters.__getitem__.assert_not_called()
    assert not mapdl._lazy_array_parameters


def test_get_variable_uses_distinct_private_parameters(monkeypatch):
    """Outstanding variable retrievals must not alias each other."""
    mapdl = _mock_grpc_mapdl()
    commands = []
    monkeypatch.setattr(
        MapdlBase, "vget", lambda self, **kwargs: commands.append(kwargs)
    )

    before = mapdl.get_variable(ir=1)
    after = mapdl.get_variable(ir=2)

    assert before._parameter_name != after._parameter_name
    assert commands == [
        {"par": before._parameter_name, "ir": 1, "tstrt": "", "kcplx": ""},
        {"par": after._parameter_name, "ir": 2, "tstrt": "", "kcplx": ""},
    ]
    assert mapdl._lazy_array_parameters == {
        before._parameter_name,
        after._parameter_name,
    }
    mapdl.parameters.__getitem__.assert_not_called()

    values = {
        before._parameter_name: np.array([1.0, 2.0]),
        after._parameter_name: np.array([4.0, 7.0]),
    }
    mapdl.parameters.__getitem__.side_effect = values.__getitem__

    np.testing.assert_array_equal(np.asarray(before), [1.0, 2.0])
    np.testing.assert_array_equal(np.asarray(after), [4.0, 7.0])
    assert mapdl.run.call_args_list == [
        call(f"{before._parameter_name}=", mute=True),
        call(f"{after._parameter_name}=", mute=True),
    ]
    assert not mapdl._lazy_array_parameters


def test_lazy_array_close_deletes_unused_backing_parameter():
    """close() releases a backing parameter without downloading it."""
    mapdl = _mock_grpc_mapdl()
    parameter_name = mapdl._new_lazy_array_parameter()
    lazy = LazyArray(
        mapdl,
        parameter_name,
        cleanup=lambda: mapdl._delete_lazy_array_parameter(parameter_name),
    )

    lazy.close()

    mapdl.run.assert_called_once_with(f"{parameter_name}=", mute=True)
    mapdl.parameters.__getitem__.assert_not_called()
    assert not mapdl._lazy_array_parameters


def test_failed_download_keeps_backing_parameter_for_retry():
    """A download error must not delete the only remaining result source."""
    mapdl = _mock_grpc_mapdl()
    parameter_name = mapdl._new_lazy_array_parameter()
    lazy = LazyArray(
        mapdl,
        parameter_name,
        cleanup=lambda: mapdl._delete_lazy_array_parameter(parameter_name),
    )
    mapdl.parameters.__getitem__.side_effect = [
        RuntimeError("download failed"),
        np.array([1.0]),
    ]

    with pytest.raises(RuntimeError, match="download failed"):
        lazy.resolve()

    assert mapdl._lazy_array_parameters == {parameter_name}

    np.testing.assert_array_equal(lazy.resolve(), [1.0])
    assert not mapdl._lazy_array_parameters


def test_get_array_creates_lazy_private_parameter():
    """gRPC get_array must defer parameter download and avoid VGet2."""
    mapdl = _mock_grpc_mapdl()

    lazy = mapdl.get_array("NODE", item1="NLIST")

    assert isinstance(lazy, LazyArray)
    mapdl.starvget.assert_called_once_with(
        lazy._parameter_name,
        "NODE",
        "",
        "NLIST",
        "",
        "",
        "",
        "",
        mute=False,
    )
    mapdl.parameters.__getitem__.assert_not_called()


def test_get_array_materialization_deletes_private_parameter():
    """gRPC get_array must download once and then release its source."""
    mapdl = _mock_grpc_mapdl()

    lazy = mapdl.get_array("NODE", item1="NLIST")
    parameter_name = lazy._parameter_name
    mapdl.parameters.__getitem__.return_value = np.array([1.0, 2.0])

    np.testing.assert_array_equal(np.asarray(lazy), [1.0, 2.0])
    mapdl.parameters.__getitem__.assert_called_once_with(parameter_name)
    mapdl.run.assert_called_once_with(f"{parameter_name}=", mute=True)
    assert not mapdl._lazy_array_parameters


def test_get_array_population_failure_cleans_up_private_parameter():
    """Failed *VGET commands must not retain an unused private parameter."""
    mapdl = _mock_grpc_mapdl()
    mapdl.starvget.side_effect = RuntimeError("VGET failed")

    with pytest.raises(RuntimeError, match="VGET failed"):
        mapdl.get_array("NODE", item1="NLIST")

    mapdl.run.assert_called_once_with("PYMAPDL_LAZY_0000000000000001=", mute=True)
    assert not mapdl._lazy_array_parameters


def test_owned_parameter_cleanup_propagates_errors():
    """Cleanup errors must remain visible and retain the tracked parameter."""
    mapdl = _mock_grpc_mapdl()
    parameter_name = mapdl._new_lazy_array_parameter()
    mapdl.run.side_effect = RuntimeError("delete failed")

    with pytest.raises(RuntimeError, match="delete failed"):
        mapdl._cleanup_lazy_array_parameters()

    assert mapdl._lazy_array_parameters == {parameter_name}


def test_temporary_result_wrappers_remain_eager(monkeypatch):
    """NSOL, ESOL, and RPSD must preserve their ndarray-returning API."""
    mapdl = _mock_grpc_mapdl()
    values = np.array([1.0, 2.0])
    mapdl.vget = MagicMock(return_value=values)

    for wrapper, command in (("nsol", "nsol"), ("esol", "esol"), ("rpsd", "rpsd")):
        monkeypatch.setattr(MapdlBase, command, lambda self, **kwargs: None)
        result = getattr(MapdlGrpc, wrapper)(mapdl)
        np.testing.assert_array_equal(result, values)

    assert mapdl.vget.call_count == 3
