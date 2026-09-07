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

"""Lazily-evaluated array proxy for MAPDL parameters.

See issue #4190: some MAPDL commands (for example ``VGET``) only need to
run server-side to produce a value, but the corresponding PyMAPDL wrapper
downloads that value immediately, even if the caller never uses it. The
:class:`LazyArray` class defers that download until the value is actually
used.
"""

from typing import TYPE_CHECKING, Any, Optional

import numpy as np
from numpy.lib.mixins import NDArrayOperatorsMixin
from numpy.typing import NDArray

if TYPE_CHECKING:  # pragma: no cover
    from ansys.mapdl.core.mapdl import MapdlBase


class LazyArray(NDArrayOperatorsMixin):
    """Array-like object whose data is fetched from MAPDL only when used.

    An instance of this class is returned instead of a
    :class:`numpy.ndarray` by methods that populate an APDL array
    parameter server-side (for example :meth:`Mapdl.vget
    <ansys.mapdl.core.Mapdl.vget>`). The underlying MAPDL command has
    already run and the parameter exists in the MAPDL database, but its
    values are not downloaded until this object is used as an array
    (indexing, iteration, ``len()``, ``repr()``, or any NumPy operation).

    This avoids the network and CPU cost of downloading the parameter
    values when the caller does not use the returned value, while keeping
    the common usage patterns (indexing, NumPy functions, arithmetic)
    working exactly as they would with a plain :class:`numpy.ndarray`.

    The resolved value is cached after the first use, so repeated access
    does not trigger repeated downloads. Because of this cache, if the
    underlying MAPDL parameter is overwritten between the creation of a
    :class:`LazyArray` and its first use, only the value present at the
    time of the first use is captured.

    .. note::
        Unlike a real :class:`numpy.ndarray`, ``isinstance(value,
        np.ndarray)`` is ``False`` for a :class:`LazyArray`. Use
        ``np.asarray(value)`` to obtain an actual array when needed.

    Parameters
    ----------
    mapdl : Mapdl
        MAPDL instance the parameter belongs to.
    parameter_name : str
        Name of the APDL parameter to retrieve lazily.

    Examples
    --------
    >>> arr = mapdl.vget(par="A", ir=2)  # no data downloaded yet
    >>> arr[0]  # doctest: +SKIP
    0.0  # downloads the parameter values on first use
    """

    def __init__(self, mapdl: "MapdlBase", parameter_name: str) -> None:
        self._mapdl = mapdl
        self._parameter_name = parameter_name
        self._cached: Optional[NDArray[np.float64]] = None

    def _resolve(self) -> NDArray[np.float64]:
        """Download and cache the actual parameter values."""
        if self._cached is None:
            self._cached = self._mapdl.parameters[self._parameter_name]
        return self._cached

    def __array__(self, dtype: Any = None) -> NDArray[np.float64]:
        array = self._resolve()
        return array.astype(dtype) if dtype is not None else array

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        """Delegate NumPy ufuncs (arithmetic operators) to the resolved array.

        This is what allows expressions such as ``lazy_array + 1`` or
        ``lazy_array * other_array`` to work transparently, resolving
        (and caching) the underlying data on first use.
        """
        resolved_inputs = tuple(
            input_.resolve() if isinstance(input_, LazyArray) else input_
            for input_ in inputs
        )
        return getattr(ufunc, method)(*resolved_inputs, **kwargs)

    def resolve(self) -> NDArray[np.float64]:
        """Download and cache the actual parameter values.

        Returns
        -------
        numpy.ndarray
            Resolved array retrieved from the MAPDL parameter.

        Examples
        --------
        >>> arr = mapdl.vget(par="A", ir=2)  # no data downloaded yet
        >>> arr.resolve()  # doctest: +SKIP
        array([0., 1., 2.])
        """
        return self._resolve()

    def __getitem__(self, index: Any) -> Any:
        return self._resolve()[index]

    def __len__(self) -> int:
        return len(self._resolve())

    def __iter__(self):
        return iter(self._resolve())

    def __eq__(self, other: Any) -> Any:
        return self._resolve() == other

    def __repr__(self) -> str:
        return repr(self._resolve())
