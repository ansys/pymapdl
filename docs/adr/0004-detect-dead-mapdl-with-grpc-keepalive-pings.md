# Detect a dead MAPDL peer with HTTP/2 keepalive pings, not call deadlines

A MAPDL server can stop answering (crash, network partition, silently dropped connection) while the client is idle or blocked in a long call, and the OS may take a long time to notice the broken TCP connection. PyMAPDL configures HTTP/2 keepalive pings in `DEFAULT_GRPC_OPTIONS` in `mapdl_grpc.py` (`grpc.keepalive_time_ms` = `KEEPALIVE_TIME_MS`, `grpc.keepalive_timeout_ms` = 10 s, `grpc.keepalive_permit_without_calls`, `grpc.http2.min_time_between_pings_ms`, `grpc.http2.max_pings_without_data`) instead of bounding how long any individual call may run. A dead peer then flips `channel_state` to `TRANSIENT_FAILURE` within roughly `keepalive_time_ms` + `keepalive_timeout_ms`, while long calls such as `SOLVE` are never cut off. `KEEPALIVE_TIME_MS` is 330 000 ms: grpc-core's default server-side ping-abuse policy requires at least 5 minutes between "no data" pings while a call is in flight and sends `GOAWAY` (`too_many_pings`) on the third closer ping, so a shorter interval drops long calls; the extra 10% keeps timer jitter from landing a ping just inside the 5-minute window.

## Considered options

- Per-call deadlines: rejected, because they would bound legitimate long-running commands such as `SOLVE`.
- Resetting the ping strike counter with a background RPC: rejected, because MAPDL mixes up the replies of concurrent calls (a `Ctrl` reply replaces the output of a running command) and can crash under such load.

## Consequences

- Dead-peer detection latency is about 5.5 minutes plus 10 s, not seconds.
- Detection surfaces as a channel state change; the connectivity callback and liveness checks (ADR 0005, ADR 0007) act on it.
- Lowering `KEEPALIVE_TIME_MS` below 5 minutes breaks long calls against default gRPC servers.
