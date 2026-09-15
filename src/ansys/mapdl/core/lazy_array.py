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

from typing import TYPE_CHECKING, Any, Callable, Optional

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
    does not trigger repeated downloads. A caller that creates the proxy
    directly from a mutable MAPDL parameter observes the value present when
    the proxy is first used. Commands such as ``VGET`` provide a private
    server-side snapshot so that their results remain independent of later
    changes to the user-visible parameter.

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
    cleanup : callable, optional
        Callback used to release a private server-side snapshot. The callback
        is called after materialization or when
        :meth:`close() <ansys.mapdl.core.lazy_array.LazyArray.close>` is called.

    Examples
    --------
    >>> arr = mapdl.vget(par="A", ir=2)  # doctest: +SKIP
    >>> arr[0]  # doctest: +SKIP
    0.0
    """

    def __init__(
        self,
        mapdl: "MapdlBase",
        parameter_name: str,
        cleanup: Optional[Callable[[], None]] = None,
    ) -> None:
        self._mapdl = mapdl
        self._parameter_name = parameter_name
        self._cleanup = cleanup
        self._cached: Optional[NDArray[np.float64]] = None

    def _resolve(self) -> NDArray[np.float64]:
        """Download and cache the actual parameter values."""
        if self._cached is None:
            try:
                value = self._mapdl.parameters[self._parameter_name]
            except Exception as exc:
                try:
                    self._release_snapshot()
                except Exception as cleanup_exc:
                    raise cleanup_exc from exc
                raise
            self._cached = value
        # If cleanup failed after a successful download, retry it on the next
        # access rather than silently retaining the server-side snapshot.
        self._release_snapshot()
        return self._cached

    def _release_snapshot(self) -> None:
        """Release the server-side snapshot, if this proxy owns one."""
        if self._cleanup is not None:
            cleanup = self._cleanup
            cleanup()
            self._cleanup = None

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
        >>> arr = mapdl.vget(par="A", ir=2)  # doctest: +SKIP
        >>> arr.resolve()  # doctest: +SKIP
        array([0., 1., 2.])
        """
        return self._resolve()

    def close(self) -> None:
        """Release an unused server-side snapshot.

        This method does not download the array. It is useful when a lazy
        result is known not to be needed before the associated MAPDL
        connection is closed.

        Raises
        ------
        Exception
            Any exception raised while deleting the server-side snapshot.
        """
        self._release_snapshot()

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
