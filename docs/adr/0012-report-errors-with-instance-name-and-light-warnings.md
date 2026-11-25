# Raise MAPDL errors with the instance name and keep non-fatal messages unobtrusive

MAPDL output is scanned for known error strings in `_raise_errors` in `_mapdl_core/execution.py`. Lines are first joined into one flat string so messages split by MAPDL line wrapping are still detected. "Cannot create another with the same name" is emitted as a `UserWarning`, not an error, because it occurs legitimately when overriding constitutive models (see `test_tbft`). Command errors are raised as `MapdlRuntimeError`, not logged, because exceptions already reach the main logger; that global logger does not record the instance name, so the message is prefixed with `Error in instance {self.name}`. To support this, `MapdlGrpc` defines `_ip` and `_port` as class attributes, because `name` can be called before `__init__` has assigned them, and `PymapdlPercentStyle._format` in `logging.py` defaults `instance_name` to an empty string for records logged outside an instance adapter, such as exceptions. `mapdl.use` in `_mapdl_extended/session.py` reports a name that is not a local or remote file with `logger.warning` rather than `warnings.warn`, because it may be a valid macro-library entry and a warning is too intrusive.

## Consequences

- Error detection is robust to MAPDL line wrapping.
- Error messages identify the failing instance even in the global logger.
- `name` and log formatting work on partially initialised instances.
- A missing `mapdl.use` file is only visible in the log.
