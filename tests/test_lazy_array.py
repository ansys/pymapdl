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

"""Unit tests for ansys.mapdl.core.lazy_array.LazyArray (issue #4190).

These tests use a mocked ``Mapdl`` object (via ``mapdl.parameters``) and do
not require a running MAPDL instance.
"""

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
    """Create the small portion of MapdlGrpc needed by the VGET wrapper."""
    mapdl = object.__new__(MapdlGrpc)
    mapdl._store_commands = False
    mapdl._lazy_array_counter = 0
    mapdl._lazy_array_snapshots = set()
    mapdl._parameters = MagicMock()
    mapdl._parameters.__contains__.return_value = False
    mapdl._parameters.full_parameters_output = MagicMock()
    mapdl._parameters._parm = {
        "NODE": {"type": "ARRAY", "shape": (2, 1, 1)},
    }
    mapdl.dim = MagicMock()
    mapdl.mfun = MagicMock()
    mapdl.run = MagicMock()
    return mapdl


def test_unresolved_vgets_use_distinct_server_snapshots(monkeypatch):
    """Repeated VGET calls must not alias an unresolved result."""
    mapdl = _mock_grpc_mapdl()
    monkeypatch.setattr(MapdlBase, "vget", lambda self, **kwargs: None)

    before = mapdl.vget(par="NODE")
    after = mapdl.vget(par="NODE")

    assert before._parameter_name != after._parameter_name
    assert mapdl.dim.call_args_list == [
        call(
            before._parameter_name,
            type_="ARRAY",
            imax=2,
            jmax=1,
            kmax=1,
            mute=True,
        ),
        call(
            after._parameter_name,
            type_="ARRAY",
            imax=2,
            jmax=1,
            kmax=1,
            mute=True,
        ),
    ]
    assert mapdl.mfun.call_args_list == [
        call(before._parameter_name, "COPY", "NODE", mute=True),
        call(after._parameter_name, "COPY", "NODE", mute=True),
    ]
    assert mapdl._lazy_array_snapshots == {
        before._parameter_name,
        after._parameter_name,
    }

    values = {
        before._parameter_name: np.array([1.0, 2.0]),
        after._parameter_name: np.array([4.0, 7.0]),
    }
    mapdl.parameters.__getitem__.side_effect = values.__getitem__

    np.testing.assert_array_equal(np.asarray(before), [1.0, 2.0])
    np.testing.assert_array_equal(np.asarray(after), [4.0, 7.0])
    np.testing.assert_array_equal(after - before, [3.0, 5.0])
    assert mapdl.run.call_count == 2
    assert not mapdl._lazy_array_snapshots


def test_lazy_array_close_deletes_unused_snapshot():
    """An unused snapshot can be released without downloading its values."""
    mapdl = _mock_grpc_mapdl()
    snapshot = "_PYMAPDL_LAZY_0000000000000001"
    mapdl._lazy_array_snapshots.add(snapshot)
    lazy = LazyArray(
        mapdl,
        snapshot,
        cleanup=lambda: mapdl._delete_lazy_array_snapshot(snapshot),
    )

    lazy.close()

    mapdl.run.assert_called_once_with(f"{snapshot}=", mute=True)
    mapdl.parameters.__getitem__.assert_not_called()
    assert not mapdl._lazy_array_snapshots


def test_snapshot_names_skip_existing_parameters():
    """Snapshot names must be bounded and avoid existing MAPDL parameters."""
    mapdl = _mock_grpc_mapdl()
    mapdl.parameters.__contains__.side_effect = [True, False]

    name = mapdl._new_lazy_array_snapshot()

    assert name == "_PYMAPDL_LAZY_0000000000000002"
    assert len(name) <= 32


def test_snapshot_cleanup_propagates_errors():
    """Cleanup errors must remain visible to the caller."""
    mapdl = _mock_grpc_mapdl()
    mapdl._lazy_array_snapshots.add("_PYMAPDL_LAZY_0000000000000001")
    mapdl.run.side_effect = RuntimeError("delete failed")

    with pytest.raises(RuntimeError, match="delete failed"):
        mapdl._cleanup_lazy_array_snapshots()

    assert mapdl._lazy_array_snapshots


def test_vget_preserves_store_commands(monkeypatch):
    """Command storage must not add a server snapshot."""
    mapdl = _mock_grpc_mapdl()
    mapdl._store_commands = True
    monkeypatch.setattr(MapdlBase, "vget", lambda self, **kwargs: None)

    assert mapdl.vget(par="NODE") is None
    mapdl.mfun.assert_not_called()
    assert not mapdl._lazy_array_snapshots


def test_temporary_result_wrappers_materialize_snapshots(monkeypatch):
    """NSOL, ESOL, and RPSD retain their ndarray-returning API."""
    mapdl = _mock_grpc_mapdl()
    mapdl.parameters.__getitem__.return_value = np.array([1.0, 2.0])
    mapdl.vget = MagicMock(
        side_effect=lambda *args, **kwargs: LazyArray(mapdl, "SNAPSHOT")
    )

    for wrapper, command in (("nsol", "nsol"), ("esol", "esol"), ("rpsd", "rpsd")):
        monkeypatch.setattr(MapdlBase, command, lambda self, **kwargs: None)
        result = getattr(MapdlGrpc, wrapper)(mapdl)
        np.testing.assert_array_equal(result, [1.0, 2.0])

    assert mapdl.parameters.__getitem__.call_count == 3


def test_get_variable_deletes_source_after_vget():
    """Deleting the temporary VGET parameter must not invalidate its result."""
    mapdl = _mock_grpc_mapdl()
    snapshot = "_PYMAPDL_LAZY_0000000000000001"
    mapdl.parameters.__getitem__.return_value = np.array([1.0, 2.0])
    mapdl.vget = MagicMock(return_value=LazyArray(mapdl, snapshot))

    result = MapdlGrpc.get_variable(mapdl, ir=2)

    np.testing.assert_array_equal(result, [1.0, 2.0])
    mapdl.parameters.__getitem__.assert_called_once_with(snapshot)
    mapdl.vget.assert_called_once_with(par="temp_var", ir=2, tstrt="", kcplx="")
    mapdl.parameters.__delitem__.assert_called_once_with("temp_var")
