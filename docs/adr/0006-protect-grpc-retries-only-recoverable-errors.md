# Retry only recoverable gRPC errors in `protect_grpc`

`protect_grpc` in `errors.py` wraps every gRPC method and retries `grpc.RpcError` with exponential backoff and reconnection. Some failures cannot be repaired by replaying the call, so they are raised immediately: `RESOURCE_EXHAUSTED` "Received message larger than max" (a response-size limit) raises `MapdlgRPCError` suggesting `PYMAPDL_MAX_MESSAGE_LENGTH`, and `UNIMPLEMENTED` raises `MapdlgRPCError` without marking MAPDL as exited, since the server is alive and only that method is refused. `grpc.FutureCancelledError`, raised when `MapdlGrpc._watched_call` cancels an in-flight call after the connectivity callback reports `TRANSIENT_FAILURE`/`SHUTDOWN` (ADR 0005), becomes `MapdlConnectionError` so the call fails fast instead of hanging. When every reconnection attempt fails, `mapdl._exited` is set to `True` to stop further execution.

## Consequences

- Response-size and unimplemented-method errors cost no retry delay.
- After an `UNIMPLEMENTED` error, other commands keep working on the same instance.
- After exhausted retries the instance is unusable and raises `MapdlExitedError` on later commands; teardown still runs on `exit()` (ADR 0008).
- `is_alive`, called during retries, must not itself go through `protect_grpc` (ADR 0007).
