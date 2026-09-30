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

"""High-level, generic coordinate-based node selector.

This module provides a small convenience layer on top of the existing
``NSEL``, ``CM`` and ``CMSEL`` MAPDL commands so that a caller can select
nodes using arbitrary ``X``/``Y``/``Z`` coordinate criteria without having to
manually translate the request into a sequence of low-level select commands.

See the :class:`NodeSelector <ansys.mapdl.core.selector.NodeSelector>` class
for the public API.
"""

from collections.abc import Mapping
import math
from numbers import Real
import string
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    List,
    Literal,
    NamedTuple,
    NoReturn,
    Optional,
    Tuple,
    Union,
)
import weakref

import numpy as np
from numpy.typing import NDArray

from ansys.mapdl.core.misc import random_string

if TYPE_CHECKING:  # pragma: no cover
    from ansys.mapdl.core.mapdl import MapdlBase

#: Axes supported by :meth:`NodeSelector.select`, in the order in which they
#: are always processed (regardless of keyword-argument order).
_AXES: Tuple[str, ...] = ("x", "y", "z")


#: Python container types treated as an explicit "OR of discrete values".
#: Tuples are excluded because they represent inclusive intervals.
_SAMPLE_COLLECTION_TYPES = (list, set, frozenset, np.ndarray)

#: Prefix used for temporary ``NODE`` components combining multiple axes.
_COMPONENT_PREFIX = "PYSEL"


class _AxisSelection(NamedTuple):
    """Normalized, internal representation of a single axis criterion.

    Attributes
    ----------
    kind : str
        Either ``"values"`` (an *OR* of discrete coordinate values) or
        ``"interval"`` (an inclusive ``[vmin, vmax]`` range).
    values : tuple
        For ``kind == "values"``, the ordered, non-empty tuple of numeric
        values to ``OR`` together. For ``kind == "interval"``, the
        ``(vmin, vmax)`` pair.
    """

    kind: Literal["values", "interval"]
    values: Tuple[Union[int, float], ...]


def _reject(axis: str, message: str, *, error: type[Exception] = TypeError) -> NoReturn:
    """Raise a validation error with a consistent, axis-qualified message."""
    raise error(f"select(): invalid criterion for axis {axis.upper()!r}: {message}")


def _normalize_value(axis: str, value: Any) -> Union[int, float]:
    """Validate a single scalar entry of a criterion.

    Booleans are rejected even though :class:`bool` is a subclass of
    :class:`int` in Python, since they are never meaningful coordinates.
    """
    if isinstance(value, bool):
        _reject(axis, f"boolean value {value!r} is not a valid coordinate.")
    if not isinstance(value, Real):
        _reject(axis, f"non-numeric value {value!r} is not a valid coordinate.")
    if not math.isfinite(value):
        _reject(axis, f"coordinate value {value!r} must be finite.", error=ValueError)
    return value


def _normalize_axis_criterion(axis: str, value: Any) -> _AxisSelection:
    """Normalize and validate a single axis criterion.

    Parameters
    ----------
    axis : str
        Lower-case axis name (``"x"``, ``"y"`` or ``"z"``), only used to
        produce clear error messages.
    value : Any
        The raw criterion supplied by the caller.

    Returns
    -------
    _AxisSelection
        The normalized, internal representation of the criterion.
    """
    if isinstance(value, range):
        _reject(
            axis,
            "a bare 'range' is not accepted because its exclusive stop bound "
            "differs from MAPDL's inclusive selection ranges; use a two-value "
            "tuple for a bounded range instead.",
        )

    if isinstance(value, bool):
        _reject(axis, f"boolean value {value!r} is not a valid coordinate.")

    if isinstance(value, str):
        _reject(axis, f"a string ({value!r}) is not a valid coordinate criterion.")

    if isinstance(value, Mapping):
        _reject(axis, f"a mapping ({value!r}) is not a valid coordinate criterion.")

    if isinstance(value, Real):
        return _AxisSelection(kind="values", values=(_normalize_value(axis, value),))

    if isinstance(value, tuple):
        if len(value) != 2:
            _reject(
                axis,
                "a tuple criterion must contain exactly two coordinate bounds.",
                error=ValueError,
            )
        vmin, vmax = (_normalize_value(axis, bound) for bound in value)
        if vmin > vmax:
            _reject(
                axis,
                f"interval bounds are reversed: vmin ({vmin}) must not be "
                f"greater than vmax ({vmax}).",
                error=ValueError,
            )
        return _AxisSelection(kind="interval", values=(vmin, vmax))

    if isinstance(value, _SAMPLE_COLLECTION_TYPES):
        if isinstance(value, np.ndarray) and value.ndim != 1:
            _reject(axis, "a NumPy array criterion must be one-dimensional.")
        try:
            items = list(value)
        except TypeError:
            _reject(axis, "a NumPy array criterion must be one-dimensional.")
        if not items:
            _reject(
                axis,
                "an empty collection is not a valid criterion.",
                error=ValueError,
            )
        values = tuple(_normalize_value(axis, item) for item in items)
        if isinstance(value, (set, frozenset)):
            values = tuple(sorted(values))
        return _AxisSelection(kind="values", values=values)

    _reject(
        axis,
        f"unsupported criterion type {type(value).__name__!r}. Use a number, "
        "a list/set/frozenset/one-dimensional NumPy array of numbers, or a "
        "two-value tuple of numbers.",
    )


def _component_name(axis: str) -> str:
    """Build a unique, valid MAPDL component name for a temporary axis set."""
    suffix = random_string(8, letters=string.ascii_uppercase + string.digits)
    return f"{_COMPONENT_PREFIX}_{axis.upper()}_{suffix}"


class NodeSelector:
    """High-level, generic coordinate-based node selector.

    ``NodeSelector`` is a thin convenience layer over the existing
    ``NSEL``/``CM``/``CMSEL``/``CMDELE`` MAPDL commands. It is not meant to
    be instantiated directly: use the lazily created, cached
    :attr:`Mapdl.selector <ansys.mapdl.core.Mapdl.selector>`
    property instead.

    Parameters
    ----------
    mapdl : ansys.mapdl.core.mapdl.MapdlBase
        MAPDL instance to which this selector is bound.

    Examples
    --------
    Select every node at ``x == 1``.

    >>> mapdl.selector.select(x=1)  # doctest: +SKIP

    Select every node with ``x == 1`` and ``y`` in ``{1, 2}``.

    >>> mapdl.selector.select(x=1, y=[1, 2])  # doctest: +SKIP

    Select every node with ``0 <= z <= 5``.

    >>> mapdl.selector.select(z=(0, 5))  # doctest: +SKIP
    """

    def __init__(self, mapdl: "MapdlBase") -> None:
        self._mapdl_weakref: "weakref.ReferenceType[MapdlBase]" = weakref.ref(mapdl)

    @property
    def _mapdl(self) -> "MapdlBase":
        """Return the weakly referenced Mapdl instance."""
        mapdl = self._mapdl_weakref()
        if mapdl is None:  # pragma: no cover - requires the owner to be collected
            raise RuntimeError(
                "The MAPDL instance bound to this selector no longer exists."
            )
        return mapdl

    def select(
        self,
        x: Optional[Any] = None,
        y: Optional[Any] = None,
        z: Optional[Any] = None,
        **kwargs: Any,
    ) -> NDArray[np.int32]:
        """Select nodes matching the given coordinate criteria.

        Each of ``x``, ``y`` and ``z`` (and their case-insensitive aliases
        ``X``, ``Y`` and ``Z``, supplied through ``**kwargs``) accepts one of:

        * a scalar number, which selects nodes at that coordinate;
        * a list, set, frozenset, or one-dimensional :class:`numpy.ndarray`
          of numbers, which selects nodes matching *any* of those values;
          empty collections are not valid criteria;
        * a two-value tuple of numbers, which selects nodes whose coordinate
          lies within the inclusive ``[vmin, vmax]`` bounds.

        A tuple must contain exactly two finite numeric bounds in ascending
        order. Open-ended intervals are not supported because an omitted
        MAPDL ``NSEL`` bound has different semantics from an unbounded
        interval.

        Criteria supplied on different axes are combined with *AND*. For
        multiple axes, each axis's set is materialized into a uniquely named
        temporary ``NODE`` component. The axes are then combined with
        ``CMSEL,S`` for the first axis and ``CMSEL,R`` for every subsequent
        axis, always processed in ``x``, ``y``, ``z`` order regardless of
        keyword order. Every temporary component is deleted before returning.

        The caller's previous active selection is restored before this method
        returns. The returned node IDs are evaluated while the coordinate
        selection is active.

        Parameters
        ----------
        x : number, collection of numbers, or tuple of two numbers, optional
            Criterion for the ``X`` coordinate. Lists, sets, frozensets, and
            one-dimensional NumPy arrays represent discrete coordinate values.
        y : number, collection of numbers, or tuple of two numbers, optional
            Criterion for the ``Y`` coordinate. Lists, sets, frozensets, and
            one-dimensional NumPy arrays represent discrete coordinate values.
        z : number, collection of numbers, or tuple of two numbers, optional
            Criterion for the ``Z`` coordinate. Lists, sets, frozensets, and
            one-dimensional NumPy arrays represent discrete coordinate values.
        **kwargs : dict, optional
            Case-insensitive aliases for ``x``, ``y`` and ``z`` (that is,
            ``X``, ``Y`` and ``Z``). Supplying two non-``None`` criteria for
            the same axis (for example ``x`` and ``X``) is ambiguous and
            raises :class:`ValueError`. Any other keyword raises
            :class:`TypeError`.

        Returns
        -------
        numpy.ndarray
            One-dimensional array of ``int32`` MAPDL node numbers, that is
            ``mapdl.mesh.nnum`` evaluated after the final combination step.
            The array is empty when no node satisfies the criteria.

        Raises
        ------
        TypeError
            If an unsupported keyword argument is supplied, or if a
            criterion has an unsupported type (for example a string, a
            mapping, a bare :class:`range`, a boolean, or a collection
            containing a non-numeric entry).
        ValueError
            If no criteria are supplied at all, if two non-``None`` criteria
            specify the same axis through its case-insensitive aliases, if a
            tuple does not contain exactly two values, a collection is empty,
            or a coordinate or interval bound is not finite.

        Examples
        --------
        Select every node at ``x == 1``.

        >>> mapdl.selector.select(x=1)  # doctest: +SKIP

        Select every node with ``x == 1`` and ``y`` in ``{1, 2}`` and
        ``0 <= z <= 5``.

        >>> mapdl.selector.select(x=1, y=[1, 2], z=(0, 5))  # doctest: +SKIP
        """
        raw_criteria = self._collect_criteria(x, y, z, kwargs)

        # Normalize and validate every axis before issuing a MAPDL command so
        # an invalid later axis never leaves a partial selection or an orphaned
        # temporary component behind.
        normalized: Dict[str, _AxisSelection] = {
            axis: _normalize_axis_criterion(axis, raw_criteria[axis])
            for axis in _AXES
            if axis in raw_criteria
        }

        return self._apply_selection(normalized)

    @staticmethod
    def _collect_criteria(
        x: Optional[Any],
        y: Optional[Any],
        z: Optional[Any],
        kwargs: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Merge the named ``x``/``y``/``z`` parameters and their aliases.

        Raises
        ------
        TypeError
            If ``kwargs`` contains a keyword that is not a case-insensitive
            alias of ``x``, ``y`` or ``z``.
        ValueError
            If the same axis is supplied twice (once through the named
            parameter, once through an alias, or through two differently
            cased aliases), or if no criterion at all is supplied.
        """
        raw_criteria: Dict[str, Any] = {}
        for axis, value in zip(_AXES, (x, y, z)):
            if value is not None:
                raw_criteria[axis] = value

        for key, value in kwargs.items():
            axis = key.lower()
            if axis not in _AXES:
                raise TypeError(f"select() got an unexpected keyword argument {key!r}.")
            if value is None:
                continue
            if axis in raw_criteria:
                raise ValueError(
                    f"select() received ambiguous, duplicate criteria for axis "
                    f"{axis.upper()!r} (both {axis!r} and {key!r} were supplied)."
                )
            raw_criteria[axis] = value

        if not raw_criteria:
            raise ValueError(
                "select() requires at least one of 'x', 'y' or 'z' criteria."
            )

        return raw_criteria

    def _apply_selection(
        self, normalized: Dict[str, _AxisSelection]
    ) -> NDArray[np.int32]:
        """Translate normalized criteria into MAPDL commands and return the result."""
        mapdl = self._mapdl

        with mapdl.save_selection:
            if len(normalized) == 1:
                axis, criterion = next(iter(normalized.items()))
                self._select_axis(mapdl, axis, criterion)
                return mapdl.mesh.nnum

            created_components: List[str] = []
            selection_failed = False
            try:
                for axis, criterion in normalized.items():
                    self._select_axis(mapdl, axis, criterion)

                    if mapdl.mesh.n_node == 0:
                        return mapdl.mesh.nnum

                    name = _component_name(axis)
                    mapdl.cm(name, "NODE")
                    created_components.append(name)

                for i, name in enumerate(created_components):
                    mapdl.cmsel("S" if i == 0 else "R", name)

                return mapdl.mesh.nnum
            except BaseException:
                selection_failed = True
                raise
            finally:
                cleanup_error = None
                for name in created_components:
                    try:
                        mapdl.cmdele(name)
                    except Exception as error:
                        if cleanup_error is None:
                            cleanup_error = error
                if cleanup_error is not None and not selection_failed:
                    raise cleanup_error

    @staticmethod
    def _select_axis(
        mapdl: "MapdlBase",
        axis: str,
        criterion: _AxisSelection,
    ) -> None:
        """Issue the ``NSEL`` command(s) selecting one axis from the full model."""
        axis_label = axis.upper()

        if criterion.kind == "interval":
            vmin, vmax = criterion.values
            mapdl.nsel("S", "LOC", axis_label, vmin, vmax)
            return

        for i, value in enumerate(criterion.values):
            mapdl.nsel("S" if i == 0 else "A", "LOC", axis_label, value)
