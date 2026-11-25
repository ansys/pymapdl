# Make iterable and multi-axis selections fail before they select anything wrong

Selections built from several MAPDL commands can leave a partial or wrong selection. `NodeSelector.select` in `selector.py` normalizes and validates every axis with `_normalize_axis_criterion` before issuing any MAPDL command, so an invalid later axis never leaves a partial selection; `_apply_selection` then applies multi-value axes first (the stable sort keeps x, y, z order within each group) so single-command axes can narrow the result with `NSEL,R`. When selecting from an iterable, `_mapdl_core/selection.py` issues one command per item, so reselect mode `R` raises `NotImplementedError`: the first reselect would discard the other requested entities. In `allow_iterables_vmin` in `misc.py`, when interactive picking (`Used_P`) returns no entities the wrapper silently returns, because running `NSEL` with an empty list in scripting (`mapdl.nsel("S", "node", "", [])`) deliberately unselects everything.

## Consequences

- Validation errors in `NodeSelector.select` leave the current selection untouched.
- Users needing reselect over an iterable must express it another way.
- An empty interactive pick keeps the current selection, while an empty scripted list still clears it.
