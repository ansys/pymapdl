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

from unittest.mock import MagicMock

import numpy as np
import pytest

from ansys.mapdl.core.lazy_array import LazyArray


@pytest.fixture
def mock_mapdl():
    """Return a mock MAPDL instance with a mocked ``parameters`` mapping."""
    mapdl = MagicMock()
    mapdl.parameters = MagicMock()
    mapdl.parameters.__getitem__ = MagicMock(
        return_value=np.array([1.0, 2.0, 3.0])
    )
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
