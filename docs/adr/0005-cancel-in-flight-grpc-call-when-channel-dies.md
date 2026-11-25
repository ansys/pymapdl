# Cancel the in-flight gRPC call from a weakly referenced connectivity callback

A gRPC call blocked on a connection that has died never completes on its own; it hangs until MAPDL answers or the OS notices the broken connection. `MapdlGrpc` keeps a handle to the call currently in flight in `_current_call`, guarded by `_current_call_lock` because it is written from the calling thread and read/cancelled from the gRPC connectivity callback thread. `_watched_call` tracks the call via `_track_call`/`_untrack_call`, and the callback registered in `_subscribe_to_channel` calls `_cancel_call_if_pending` only when the state is in `dead_states` (`TRANSIENT_FAILURE`, `SHUTDOWN`), the states in which the transport is confirmed unusable. The callback captures `self` through `weakref.ref`, because the gRPC `_poll_connectivity` daemon thread keeps the callback alive for as long as the subscription lasts; a strong reference creates an uncollectable cycle (thread -> state -> callback -> mapdl -> channel -> state) that prevents `__del__` from ever running, leaking both the instance and the polling thread.

## Consequences

- Cancellation does not bound how long a call may run while the channel stays healthy; `SOLVE` is unaffected.
- A cancelled call raises `grpc.FutureCancelledError`, which `protect_grpc` converts into `MapdlConnectionError` (ADR 0006).
- The callback must tolerate `self_ref()` returning `None` and do nothing.
- Other states, including `CONNECTING` and `IDLE`, never cancel a call.
