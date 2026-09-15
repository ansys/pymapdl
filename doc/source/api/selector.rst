.. _ref_nodeselector_api:

Selector
========

.. currentmodule:: ansys.mapdl.core

The :attr:`Mapdl.selector <ansys.mapdl.core.Mapdl.selector>`
property gives access to a high-level, generic coordinate-based node
selector. It is a thin convenience layer over the existing
:meth:`Mapdl.nsel() <ansys.mapdl.core.Mapdl.nsel>`,
:meth:`Mapdl.cm() <ansys.mapdl.core.Mapdl.cm>` and
:meth:`Mapdl.cmsel() <ansys.mapdl.core.Mapdl.cmsel>`
commands: instead of
manually translating a spatial condition into several MAPDL commands, you can
express it directly in terms of ``X``, ``Y`` and ``Z`` coordinate criteria.
The same generated command sequence works for local and remote MAPDL sessions;
the selector does not transfer files.

Criteria
--------
The :meth:`NodeSelector.select <ansys.mapdl.core.selector.NodeSelector.select>`
method accepts any subset of the ``x``, ``y`` and ``z`` coordinates. A scalar
selects nodes at one coordinate, while a list, tuple, set, ``frozenset``, or
one-dimensional NumPy array selects nodes at any of the supplied coordinates.
Axis names are case-insensitive, so ``X``, ``Y`` and ``Z`` are also accepted.
A collection must contain at least one value. Criteria on different axes are
intersected, so every selected node must satisfy all supplied axes.

Use the :class:`Interval <ansys.mapdl.core.selector.Interval>` class for an
inclusive coordinate interval. At least one bound is required; a missing lower
or upper bound creates an open-ended interval. A bare Python :class:`range` is
not accepted because its exclusive stop value does not match MAPDL's inclusive
range semantics. Any supplied bound must be finite, and ``vmin`` cannot be
greater than ``vmax`` when both are provided. Coordinate matching uses
MAPDL's existing ``SELTOL`` tolerance rather than an exact Python comparison.

A missing bound on an open-ended interval is resolved to the current model
extent (``MNLOC`` or ``MXLOC``) before the ``NSEL`` command is issued. If
MAPDL returns a non-numeric or non-finite extent for that axis, the method
raises :class:`RuntimeError`.

Selection state
---------------
The method intentionally replaces MAPDL's current node selection and returns
the selected node numbers as a one-dimensional NumPy array of ``int32``
values. The previous node selection is not restored. Existing user-defined
components are not redefined; temporary components used to intersect
criteria are deleted before the method returns, including when MAPDL reports
an error. If no node satisfies the criteria, the current node selection is
empty and the returned array is empty.

For explicit node IDs, continue to use the
:meth:`Mapdl.nsel() <ansys.mapdl.core.Mapdl.nsel>`
method directly. The selector interprets criteria as coordinates, not node
IDs.

.. autosummary::
   :toctree: _autosummary

   selector.NodeSelector
   selector.Interval

Examples
--------
Select every node at ``x == 1``.

.. code:: pycon

   >>> mapdl.selector.select(x=1)

Select every node with ``x == 1`` and ``y`` in ``{1, 2}``.

.. code:: pycon

   >>> mapdl.selector.select(x=1, y=[1, 2])

Select every node with ``0 <= z <= 5``.

.. code:: pycon

   >>> from ansys.mapdl.core.selector import Interval
   >>> mapdl.selector.select(z=Interval(0, 5))
