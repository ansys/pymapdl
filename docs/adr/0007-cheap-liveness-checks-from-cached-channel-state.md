# Guard each command with the cached channel state, not an `is_alive` round-trip

`MapdlGrpc.run` checks liveness before every command. It reads `channel_state`, the value cached by the connectivity callback, because `is_alive` would issue a `_ctrl("VERSION")` round-trip on every single command. Only `SHUTDOWN` (channel closed) and `TRANSIENT_FAILURE` (channel could not connect) set `_exited` and raise `MapdlExitedError`; `CONNECTING` is a normal transient and must not permanently mark the instance as exited. `run` sets `_busy` around the command and clears it in a `finally` block, because `is_alive` short-circuits to `True` on `_busy`; leaving it set would permanently disable the guard. `is_alive` probes with `_ctrl_raw` rather than `_ctrl`, because `protect_grpc` calls `is_alive` while retrying and a retried probe would recurse until `RecursionError`.

## Consequences

- The per-command guard costs no network traffic.
- A dead peer is caught by the guard only after keepalive flips the channel state (ADR 0004).
- `_ctrl_raw` used by `is_alive` must stay outside `protect_grpc`.
