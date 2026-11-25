# Tear down MAPDL in a fixed, idempotent order that is safe from `__del__`

`MapdlGrpc._release_resources` is the single cleanup path for `exit()` and `__del__`, and its ordering encodes several decisions. `exit()` calls the idempotent `_disconnect_but_leave_mapdl_running` even when `exited` is already true, because the gRPC error handlers set `_exited` on a crash without performing any cleanup. During GC-driven teardown (`cleanup_loggers=False`) a local MAPDL is stopped with `_close_process` and cached process data, and no RPCs, because the garbage collector may interrupt gRPC itself. `_exited` is set before `_remove_temp_dir_on_exit`, so its `directory` fallback cannot query the dead server. Logger handlers are cleaned up only when `cleanup_loggers` is true, because they are shared process-wide and GC-driven teardown could race with another live `Mapdl` instance logging through them. In `_close_process`, `_kill_child_processes` runs before `_kill_process`: child and MPI worker processes inherit the stdout/stderr PIPE write ends, so if they are alive when the PIPEs close, drainer threads blocked in `readline()` never see EOF and `stream.close()` deadlocks on the reader's lock. As a further guard, `_terminate_process` closes PIPEs via `_close_process_pipes` on a daemon thread joined with a 5 s timeout, so a close blocked by an untracked grandchild cannot hang the caller.

## Consequences

- Calling `exit()` repeatedly, or after a crash, is safe and still releases resources.
- `__del__` never issues RPCs and never touches shared logger handlers.
- A stuck PIPE close is abandoned after 5 s and only logged at debug level.
- Reordering the steps in `_release_resources` or `_close_process` can reintroduce hangs or server queries after death.
