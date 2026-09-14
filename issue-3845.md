# Issue #3845: Add a high-level MAPDL selector

## Summary

Issue #3845 requests an easier Python interface for selecting nodes by their
location. The current PyMAPDL API exposes the low-level MAPDL `NSEL` command,
but users must manually translate a spatial condition into several MAPDL
commands.

The issue proposes a call shaped like:

```python
mapdl.selector.select(X=1, y=[1, 2], z=range(1, 2))
```

The numbers in this example are illustrative. The feature must work with
arbitrary coordinate values and with any nodes in the model; it must not be
hard-coded to `X=1`, `Y=1/2`, or a particular region.

## Requested behavior

The primary feature is a generic, coordinate-based node selector:

- a scalar coordinate criterion selects nodes at that coordinate;
- multiple values select nodes matching any of those values;
- an interval selects nodes between its bounds;
- criteria supplied for multiple axes are combined so that a node must satisfy
  every supplied axis criterion;
- the resulting selection is applied to MAPDL's current node selection.

For example, a user should be able to express an axis-aligned region using
values appropriate for the current model, rather than writing a sequence of
`NSEL,LOC` commands manually.

The first version is concerned with nodes and Cartesian location criteria. It
is not a request for a hard-coded selection of particular node numbers or for
an arbitrary geometric predicate. Selecting explicit node IDs is already
available through the existing `mapdl.nsel()` iterable support.

## Current gap

PyMAPDL already supports low-level location selection, for example:

```python
mapdl.nsel("S", "LOC", "X", 1)
mapdl.nsel("R", "LOC", "Y", 1, 2)
mapdl.nsel("R", "LOC", "Z", 1, 2)
```

However, this interface:

- exposes MAPDL's positional command syntax;
- does not provide a single high-level selector object;
- does not directly express a disjoint set of coordinate values together with
  constraints on other axes;
- requires callers to handle selection-mode composition themselves.

The new API should be a convenience layer over the existing MAPDL capabilities
and must not change the behavior of `mapdl.nsel()` or other selection commands.

## Related request in the issue discussion

The issue also contains a separate suggestion for a material convenience API:

```python
mapdl.materials.new(id=2, ex=1.2e9, nu=0.3)
```

This would wrap existing commands such as:

```python
mapdl.mp("EX", 2, 1.2e9)
mapdl.mp("NUXY", 2, 0.3)
```

The material request is related in that it asks for a more Pythonic interface,
but it is independent of coordinate-based node selection. It requires its own
property-label mapping and material-model scope, so it should be treated as a
separate follow-up unless the issue owner explicitly expands the acceptance
criteria.

## Acceptance criteria

The selector work is complete when:

1. A public high-level API can select nodes using arbitrary X, Y, and Z
   criteria.
2. Scalar, multiple-value, and interval criteria have documented, tested
   semantics.
3. Combined criteria produce the intersection across axes and the union of
   alternatives within one axis.
4. The selection is reflected in MAPDL and existing selection commands remain
   backward compatible.
5. Invalid or ambiguous criteria produce a clear validation error.
6. The API has tests and user-facing documentation.
