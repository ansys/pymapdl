# Retry `LazyArray` server-side cleanup on every access

`LazyArray` in `lazy_array.py` downloads a MAPDL parameter on first access and caches it in `_cached`. `_resolve` calls `_release_parameter` on every access, even after the values are cached, so a cleanup that failed after a successful download is retried on the next access instead of silently retaining the server-side parameter. `_release_parameter` clears `_cleanup` once it succeeds, so later calls are no-ops.

## Consequences

- A transient cleanup failure does not leak the server-side parameter permanently.
- A cleanup error can surface on a later access, not only the first.
