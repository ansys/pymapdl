# Wrap listing and selection methods only when they are real MAPDL commands

`_MapdlCore` dynamically wraps methods whose first four letters match a MAPDL command list: `CMD_LISTING`/`CMD_BC_LISTING` in `_mapdl_core/execution.py` (adds `to_array`/`to_dataframe` output) and `CMD_XSEL` in `_mapdl_core/selection.py` (returns selected IDs). The prefix match alone would also catch `Mapdl` properties that start with the same letters, so wrapping additionally requires `name in dir(Commands)`. `CMD_RESULT_LISTING` in `commands.py` deliberately includes undocumented (possibly deprecated) MAPDL commands such as `NLIN` and `PRDI`; since they have no `Mapdl` method they are never wrapped. The XSEL wrapper option `return_mapdl_output` is popped and ignored in `_pop_run_kwargs`, because on console and non-interactive paths it reaches `run()` unwrapped and must not trigger the unknown-keyword error.

## Consequences

- Adding a property whose name shares a command prefix does not get it wrapped.
- Undocumented entries in `CMD_RESULT_LISTING` only affect output parsing, not the public API.
- `return_mapdl_output` is accepted silently by `run()` on every code path.
