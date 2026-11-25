# Keep `mapdl_core.py` and `mapdl_extended.py` as backward-compatible re-export facades

`_MapdlCore` and `_MapdlExtended` were split into responsibility mixins under `_mapdl_core/` and `_mapdl_extended/`. Code outside the package imported constants, helpers, errors and classes directly from `ansys.mapdl.core.mapdl_core` and `ansys.mapdl.core.mapdl_extended`. Both modules therefore list those names in `__all__` (for example `_MapdlCore`, `_MapdlPurePosixPath`, `_sanitize_start_parm`, `_MapdlCommandExtended`, `MAX_DO_LOOP_LEVEL`, `CommandListingOutput`) so existing imports keep working after the split.

## Consequences

- Removing a name from either `__all__` is a breaking change.
- The imports in these modules may look unused but exist for re-export.
