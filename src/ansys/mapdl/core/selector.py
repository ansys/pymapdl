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
for the public API and the :class:`Interval <ansys.mapdl.core.selector.Interval>`
class for the supported interval-criterion representation.
"""

from collections.abc import Mapping
from dataclasses import dataclass
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

from ansys.mapdl.core.errors import ComponentNoData
from ansys.mapdl.core.misc import random_string

if TYPE_CHECKING:  # pragma: no cover
    from ansys.mapdl.core.mapdl import MapdlBase

#: Axes supported by :meth:`NodeSelector.select`, in the order in which they
#: are always processed (regardless of keyword-argument order).
_AXES: Tuple[str, ...] = ("x", "y", "z")

#: Python container types treated as an explicit "OR of discrete values".
#: Strings, mappings, ``range`` and bare numbers are intentionally excluded
#: and handled separately (see :func:`_normalize_axis_criterion`).
_COLLECTION_TYPES = (list, tuple, set, frozenset, np.ndarray)

#: Prefix used for the temporary ``NODE`` components created while combining
#: several axes. It only needs to be short, unique and a valid MAPDL
#: component name (it must start with a letter).
_COMPONENT_PREFIX = "PYSEL"


@dataclass(frozen=True)
class Interval:
    """An explicit, inclusive-bounds interval criterion.

    ``Interval`` is used to request every node whose coordinate lies between
    ``vmin`` and ``vmax`` (both bounds included), as opposed to a plain
    list/tuple/set/frozenset/:class:`numpy.ndarray`, which always means an *OR*
    of discrete values, or a bare :class:`range`, which is rejected because
    its exclusive-stop semantics differ from MAPDL's inclusive selection
    ranges.

    At least one of ``vmin`` or ``vmax`` must be supplied. Leaving one bound
    as ``None`` requests an open-ended interval on that side.
    When used with the
    :meth:`NodeSelector.select <ansys.mapdl.core.selector.NodeSelector.select>`
    method, the missing bound is resolved from the model's coordinate extent.

    Parameters
    ----------
    vmin : int or float, optional
        Inclusive lower bound. ``None`` means "no lower bound".
    vmax : int or float, optional
        Inclusive upper bound. ``None`` means "no upper bound".

    Raises
    ------
    TypeError
        If a supplied bound is not a numeric coordinate.
    ValueError
        If both bounds are omitted, a bound is not finite, or ``vmin`` is
        greater than ``vmax``.

    Examples
    --------
    Select every node with ``1 <= x <= 5``.

    >>> from ansys.mapdl.core.selector import Interval
    >>> mapdl.selector.select(x=Interval(1, 5))  # doctest: +SKIP

    Create an open-ended criterion for ``y >= 2``.

    >>> Interval(vmin=2)
    Interval(vmin=2, vmax=None)
    """

    vmin: Optional[Union[int, float]] = None
    vmax: Optional[Union[int, float]] = None

    def __post_init__(self) -> None:
        if self.vmin is None and self.vmax is None:
            raise ValueError(
                "Interval requires at least one of 'vmin' or 'vmax' to be given."
            )

        for bound_name, bound in (("vmin", self.vmin), ("vmax", self.vmax)):
            if bound is not None and (
                isinstance(bound, bool) or not isinstance(bound, Real)
            ):
                raise TypeError(
                    f"Interval {bound_name} must be a numeric coordinate or None; "
                    f"got {bound!r}."
                )
            if bound is not None and not math.isfinite(bound):
                raise ValueError(
                    f"Interval {bound_name} must be finite; got {bound!r}."
                )

        if self.vmin is not None and self.vmax is not None and self.vmin > self.vmax:
            raise ValueError(
                f"Interval bounds are reversed: vmin ({self.vmin}) must not be "
                f"greater than vmax ({self.vmax})."
            )


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
        ``(vmin, vmax)`` pair, where an open bound is represented by ``""``
        until it is resolved to the corresponding model extent.
    """

    kind: Literal["values", "interval"]
    values: Tuple[Union[int, float, str], ...]


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
    if isinstance(value, Interval):
        vmin = "" if value.vmin is None else value.vmin
        vmax = "" if value.vmax is None else value.vmax
        return _AxisSelection(kind="interval", values=(vmin, vmax))

    if isinstance(value, range):
        _reject(
            axis,
            "a bare 'range' is not accepted because its exclusive stop bound "
            "differs from MAPDL's inclusive selection ranges; use "
            "'Interval(vmin, vmax)' for a bounded range or an explicit list "
            "of values instead.",
        )

    if isinstance(value, bool):
        _reject(axis, f"boolean value {value!r} is not a valid coordinate.")

    if isinstance(value, str):
        _reject(axis, f"a string ({value!r}) is not a valid coordinate criterion.")

    if isinstance(value, Mapping):
        _reject(axis, f"a mapping ({value!r}) is not a valid coordinate criterion.")

    if isinstance(value, Real):
        return _AxisSelection(kind="values", values=(_normalize_value(axis, value),))

    if isinstance(value, _COLLECTION_TYPES):
        if isinstance(value, np.ndarray) and value.ndim != 1:
            _reject(
                axis,
                "a NumPy array criterion must be one-dimensional.",
            )
        try:
            items = list(value)
        except TypeError:
            _reject(
                axis,
                "a NumPy array criterion must be one-dimensional.",
            )
        if len(items) == 0:
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
        "a list/tuple/set/frozenset/numpy.ndarray of numbers, or an "
        "'Interval'.",
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

    >>> from ansys.mapdl.core.selector import Interval
    >>> mapdl.selector.select(z=Interval(0, 5))  # doctest: +SKIP
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
        * a list/tuple/set/frozenset/one-dimensional
          :class:`numpy.ndarray` of numbers, which selects nodes matching
          *any* of those values (an *OR* within the axis); empty collections
          are not valid criteria;
        * an :class:`Interval <ansys.mapdl.core.selector.Interval>`, which
          selects nodes whose coordinate lies
          within the inclusive ``[vmin, vmax]`` bounds.

        For an open-ended :class:`Interval <ansys.mapdl.core.selector.Interval>`,
        the missing bound is obtained from the model extent before the final
        ``NSEL`` command is issued. This avoids relying on MAPDL's omitted-bound
        equality behavior while preserving MAPDL's active selection tolerance.

        Criteria supplied on different axes are combined with *AND*: the
        resulting selection is the intersection across axes of the
        per-axis, *OR*-combined value sets. When criteria are supplied for
        multiple axes, each axis's set is first materialized independently
        (from the full model) into a uniquely named temporary ``NODE``
        component with the
        :meth:`Mapdl.cm() <ansys.mapdl.core.Mapdl.cm>` method. The axes are
        then combined using
        :meth:`Mapdl.cmsel() <ansys.mapdl.core.Mapdl.cmsel>`
        (``"S"`` for the first axis, ``"R"`` for every subsequent one, always
        processed in ``x``, ``y``, ``z`` order regardless of keyword order).
        Every temporary component is deleted with
        :meth:`Mapdl.cmdele() <ansys.mapdl.core.Mapdl.cmdele>`
        before returning, whether the call succeeds or raises.

        The resulting node selection intentionally replaces the caller's
        previous active node selection and remains active after this method
        returns; that previous selection is not restored. Existing
        user-defined components are not redefined. Temporary components
        created by this method are deleted before returning.

        Parameters
        ----------
        x : number, collection of numbers, or Interval, optional
            Criterion for the ``X`` coordinate. Collections can be
            list/tuple/set/frozenset/:class:`numpy.ndarray` instances.
        y : number, collection of numbers, or Interval, optional
            Criterion for the ``Y`` coordinate. Collections can be
            list/tuple/set/frozenset/:class:`numpy.ndarray` instances.
        z : number, collection of numbers, or Interval, optional
            Criterion for the ``Z`` coordinate. Collections can be
            list/tuple/set/frozenset/:class:`numpy.ndarray` instances.
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
            criterion is an empty collection, or if a coordinate or interval
            bound is not finite.
        RuntimeError
            If an :class:`Interval <ansys.mapdl.core.selector.Interval>`
            criterion has an open-ended bound and MAPDL returns a
            non-numeric or non-finite model extent while resolving it.

        Examples
        --------
        Select every node at ``x == 1``.

        >>> mapdl.selector.select(x=1)  # doctest: +SKIP

        Select every node with ``x == 1`` and ``y`` in ``{1, 2}`` and
        ``0 <= z <= 5``.

        >>> from ansys.mapdl.core.selector import Interval
        >>> mapdl.selector.select(
        ...     x=1, y=[1, 2], z=Interval(0, 5)
        ... )  # doctest: +SKIP
        """
        raw_criteria = self._collect_criteria(x, y, z, kwargs)

        # Normalize and validate every axis *before* issuing a single MAPDL
        # command, so that an invalid later axis never leaves a partial
        # selection or an orphaned temporary component behind.
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

        # A single axis does not need a temporary component.  Besides
        # avoiding unnecessary commands (particularly for remote sessions),
        # this also makes an empty single-axis selection independent of CM's
        # error-reporting mode.
        if len(normalized) == 1:
            axis, criterion = next(iter(normalized.items()))
            self._select_axis(mapdl, axis, criterion)
            return mapdl.mesh.nnum

        created_components: List[str] = []
        selection_failed = False
        try:
            for axis, criterion in normalized.items():
                self._select_axis(mapdl, axis, criterion)

                # CM reports an empty selection as ComponentNoData in the
                # usual error mode, but that exception can be suppressed by
                # ``mapdl.ignore_errors``.  Check the selected node array
                # before attempting to create the temporary component so the
                # empty result remains correct in either mode.
                if mapdl.mesh.nnum.size == 0:
                    mapdl.nsel("NONE")
                    return mapdl.mesh.nnum

                name = _component_name(axis)
                try:
                    mapdl.cm(name, "NODE")
                except ComponentNoData:
                    # CM cannot represent an empty set.  The NSEL operation
                    # above has already produced the correct empty selection,
                    # so leave it active rather than turning a valid
                    # no-match criterion into an exception.
                    mapdl.nsel("NONE")
                    return mapdl.mesh.nnum
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
                    # Always attempt to delete every component.  If the
                    # selection itself failed, leave that original exception
                    # as the one propagated to the caller; otherwise expose
                    # a cleanup failure rather than silently leaking it.
                    if cleanup_error is None:
                        cleanup_error = error
            if cleanup_error is not None and not selection_failed:
                raise cleanup_error

    @staticmethod
    def _select_axis(mapdl: "MapdlBase", axis: str, criterion: _AxisSelection) -> None:
        """Issue the ``NSEL`` command(s) selecting one axis from the full model."""
        axis_label = axis.upper()

        if criterion.kind == "interval":
            vmin, vmax = criterion.values
            if vmin == "":
                vmin = NodeSelector._coordinate_extent(mapdl, axis_label, "MNLOC")
            if vmax == "":
                vmax = NodeSelector._coordinate_extent(mapdl, axis_label, "MXLOC")

            # An open-ended interval can be outside the model extent.  Avoid
            # sending a reversed NSEL range in that case; the correct result
            # is an empty active node selection.
            if isinstance(vmin, Real) and isinstance(vmax, Real) and vmin > vmax:
                mapdl.nsel("NONE")
                return

            mapdl.nsel("S", "LOC", axis_label, vmin, vmax)
            return

        for i, value in enumerate(criterion.values):
            mapdl.nsel("S" if i == 0 else "A", "LOC", axis_label, value)

    @staticmethod
    def _coordinate_extent(
        mapdl: "MapdlBase", axis: str, item: str
    ) -> Union[int, float]:
        """Return a selected-model coordinate extent for an open interval."""
        # *GET with MNLOC/MXLOC uses the active node set.  Start from all
        # nodes so that an open interval is not accidentally clipped by the
        # caller's previous selection or by a component created for another
        # axis in this selector call.
        mapdl.nsel("ALL", mute=True)
        extent = mapdl.get_value("NODE", 0, item, axis)
        if isinstance(extent, bool) or not isinstance(extent, Real):
            raise RuntimeError(
                f"MAPDL returned a non-numeric {item} extent for the {axis} axis: "
                f"{extent!r}."
            )
        if not math.isfinite(extent):
            raise RuntimeError(
                f"MAPDL returned a non-finite {item} extent for the {axis} axis: "
                f"{extent!r}."
            )
        return extent
