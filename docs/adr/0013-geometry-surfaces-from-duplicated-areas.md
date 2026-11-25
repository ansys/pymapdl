# Build geometry meshes without modifying the user's areas or numbering

`Geometry.generate_surface` in `mapdl_geometry.py` triangulates areas for plotting. When `amin`/`amax` are given it reselects (`ASEL,R`) from the current selection to mimic native APDL behaviour, instead of selecting from all areas. It meshes duplicated copies of the selected areas (`AGEN`) rather than the originals, so existing areas and their meshes are never modified; the copies are deleted afterwards. Because the duplicated area numbers do not correspond to the user's areas, the per-cell `entity_num` array is filled by position from `orig_anum`. For volumes, `Geometry.volumes` names each block from the `entity_num` attribute set on each volume mesh, because volumes are reconstructed from their areas and the per-cell `entity_num` field holds area numbers, not volume numbers.

## Consequences

- Plotting geometry leaves the model's areas, meshes and selection intact.
- `entity_num` on surfaces refers to the user's original area numbers.
- Volume block names come from the mesh-level attribute, not the cell field.
