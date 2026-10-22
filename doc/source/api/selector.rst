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
commands. Instead of manually translating a spatial condition into several
MAPDL commands, you can express it directly in terms of ``X``, ``Y`` and
``Z`` coordinate criteria. The same generated command sequence works for
local and remote MAPDL sessions.

Criteria
--------
The :meth:`NodeSelector.select <ansys.mapdl.core.selector.NodeSelector.select>`
method accepts any subset of the ``x``, ``y`` and ``z`` coordinates. A scalar
selects nodes at one coordinate. A list, set, frozenset, or one-dimensional
NumPy array selects nodes at any of its supplied coordinates. A tuple
containing exactly two finite numbers selects nodes in the inclusive coordinate
interval bounded by those numbers. Axis names are case-insensitive, so ``X``,
``Y`` and ``Z`` are also accepted. Interval bounds must be in ascending order.
A bare Python :class:`range` is not accepted because its exclusive stop value
does not match MAPDL's inclusive range semantics. Coordinate matching uses
MAPDL's existing ``SELTOL`` tolerance rather than an exact Python comparison.

Criteria on different axes are intersected, so every selected node must
satisfy all supplied axes. To preserve the intersection when an axis contains
multiple discrete values, the selector materializes every axis set into a
temporary MAPDL component, then combines them with ``CMSEL,S`` and ``CMSEL,R``.
Temporary components are deleted before the method returns.

Selection state
---------------
The method returns the selected node numbers as a one-dimensional NumPy array
of ``int32`` values and restores MAPDL's previous selection before returning.
It uses :attr:`Mapdl.save_selection <ansys.mapdl.core.Mapdl.save_selection>`
while evaluating the criteria. Existing user-defined components are not
redefined. If no node satisfies the criteria, the returned array is empty.

For explicit node IDs, continue to use the
:meth:`Mapdl.nsel() <ansys.mapdl.core.Mapdl.nsel>`
method directly. The selector interprets criteria as coordinates, not node
IDs.

.. autosummary::
   :toctree: _autosummary

   selector.NodeSelector

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

   >>> mapdl.selector.select(z=(0, 5))
