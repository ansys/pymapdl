# Keep plotting cheap and layout stable

Several plotting paths trade detail for speed or rely on call order. In `_mapdl_extended/plotting_commands.py`, per-entity colour arrays for `lplot` (`color_lines`) and `aplot` (`color_areas=True`) are capped at 256 colours with `get_ansys_colors(min(256, n))`, matching the default `n_colors` of `pyvista.DataSetMapper.set_scalars`, because they only serve plotting and a huge random colour vector is unnecessary. `_aplot_area_meshes` colours each area mesh as a whole, because individual surface isolation is too slow. In `MapdlPlotter.plot` in `plotting/visualizer.py`, the title is added after meshes, labels and boundary conditions so labels do not overlap it. The `file_type_for_plots` setter in `_mapdl_core/plotting.py` issues `/SHOW` through `self._run` instead of `self.show`, because `show()` itself updates `file_type_for_plots`, which would recurse.

## Consequences

- Models with more than 256 lines or areas reuse colours.
- Area colouring is per area, never per surface.
- Moving the `add_title` call earlier regresses the layout.
- Changing the setter to call `show()` causes infinite recursion.
