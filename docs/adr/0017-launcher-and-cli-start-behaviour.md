# Make launcher configuration explicit and the CLI process-only

In `resolve_start_instance` in `launcher/config.py`, the `PYMAPDL_START_INSTANCE` environment variable (priority 2) takes precedence over inferring `start_instance=False` from an `ip` argument or `PYMAPDL_IP` (priority 3), so an explicit `PYMAPDL_START_INSTANCE=True` is not silently overridden when `PYMAPDL_IP` is also set. In `launcher/process.py`, when `Popen` fails, closing the stdout file handle is best-effort (an `OSError` is swallowed) so the original `Popen` exception is always the one re-raised. `pymapdl start` in `cli/start.py` accepts every `launch_mapdl` argument for parity, but collects client-side ones (`mode`, `cleanup_on_exit`, `start_instance`, `ip`, `clear_on_connect`, `log_apdl`, ...) in `ignored_arguments`, because the CLI only starts the MAPDL process and never builds a client. `pymapdl exec` in `cli/exec.py` calls `silence_logging()` so stdout contains only MAPDL output and can be piped.

## Consequences

- An explicit `start_instance` argument still beats the environment variable.
- Launch failures report the real `Popen` error.
- Passing client-side options to `pymapdl start` has no effect.
- `pymapdl exec` output is safe to pipe into other tools.
