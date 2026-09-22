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

Some MAPDL commands populate an internal array parameter server-side, but
their result does not need to cross the client connection unless the caller
uses it. :class:`LazyArray` retains the backing parameter until first use,
then downloads and caches its values.
"""

from typing import TYPE_CHECKING, Any, Callable, Optional

import numpy as np
from numpy.lib.mixins import NDArrayOperatorsMixin
from numpy.typing import NDArray

if TYPE_CHECKING:  # pragma: no cover
    from ansys.mapdl.core.mapdl import MapdlBase


class LazyArray(NDArrayOperatorsMixin):
    """Array-like object whose data is fetched from MAPDL only when used.

    An instance of this class is returned by methods such as
    :meth:`Mapdl.get_variable <ansys.mapdl.core.Mapdl.get_variable>` and
    :meth:`Mapdl.get_array <ansys.mapdl.core.Mapdl.get_array>`. Their MAPDL
    commands have already run and populated a private parameter, but its
    values are not downloaded until this object is used as an array
    (indexing, iteration, ``len()``, ``repr()``, or any NumPy operation).

    This avoids the network and CPU cost of downloading parameter values when
    the caller does not use the result, while keeping common usage patterns
    (indexing, NumPy functions, arithmetic, and ndarray methods) working as
    they do with a plain :class:`numpy.ndarray`.

    The resolved value is cached after the first use, so repeated access does
    not trigger repeated downloads. After a successful download, the private
    MAPDL parameter is released.

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
        Callback used to release the owned server-side backing parameter. The
        callback is called after materialization or when
        :meth:`close() <ansys.mapdl.core.lazy_array.LazyArray.close>` is called.
    flatten : bool, default: False
        Return a one-dimensional view after resolution. This preserves the
        ``get_array()`` result shape while retaining MAPDL parameter storage.

    Examples
    --------
    >>> arr = mapdl.get_variable(ir=2)  # doctest: +SKIP
    >>> arr[0]  # doctest: +SKIP
    0.0
    """

    def __init__(
        self,
        mapdl: "MapdlBase",
        parameter_name: str,
        cleanup: Optional[Callable[[], None]] = None,
        flatten: bool = False,
    ) -> None:
        self._mapdl = mapdl
        self._parameter_name = parameter_name
        self._cleanup = cleanup
        self._flatten = flatten
        self._cached: Optional[NDArray[np.float64]] = None

    def _resolve(self) -> NDArray[np.float64]:
        """Download and cache the actual parameter values."""
        if self._cached is None:
            value = self._mapdl.parameters[self._parameter_name]
            self._cached = np.ravel(value) if self._flatten else value
        # If cleanup failed after a successful download, retry it on the next
        # access rather than silently retaining the server-side parameter.
        self._release_parameter()
        return self._cached

    def _release_parameter(self) -> None:
        """Release the owned server-side backing parameter, if present."""
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
        outputs = kwargs.get("out")
        if outputs is not None:
            kwargs["out"] = tuple(
                output.resolve() if isinstance(output, LazyArray) else output
                for output in outputs
            )

        resolved_inputs = tuple(
            input_.resolve() if isinstance(input_, LazyArray) else input_
            for input_ in inputs
        )
        result = getattr(ufunc, method)(*resolved_inputs, **kwargs)
        if outputs is not None:
            return outputs[0] if len(outputs) == 1 else outputs
        return result

    def __getattr__(self, name: str) -> Any:
        """Delegate ndarray attribute access after materialization."""
        return getattr(self._resolve(), name)

    def resolve(self) -> NDArray[np.float64]:
        """Download and cache the actual parameter values.

        Returns
        -------
        numpy.ndarray
            Resolved array retrieved from the MAPDL parameter.

        Examples
        --------
        >>> arr = mapdl.get_variable(ir=2)  # doctest: +SKIP
        >>> arr.resolve()  # doctest: +SKIP
        array([0., 1., 2.])
        """
        return self._resolve()

    def close(self) -> None:
        """Release an unresolved server-side backing parameter.

        This method does not download the array. It is useful when a lazy
        result is known not to be needed before the associated MAPDL
        connection is closed.

        Raises
        ------
        Exception
            Any exception raised while deleting the server-side backing
            parameter.
        """
        self._release_parameter()

    def __getitem__(self, index: Any) -> Any:
        return self._resolve()[index]

    def __setitem__(self, index: Any, value: Any) -> None:
        self._resolve()[index] = value

    def __len__(self) -> int:
        return len(self._resolve())

    def __bool__(self) -> bool:
        return bool(self._resolve())

    def __iter__(self):
        return iter(self._resolve())

    def __eq__(self, other: Any) -> Any:
        return self._resolve() == other

    def __repr__(self) -> str:
        return repr(self._resolve())
