# Targeted client liveness diagnostics (throwaway branch)

This branch is for step 1 only. Do not merge its restricted parent workflow.
It does not include OMP's channel-cleanup or production-visibility fixes.

## Experiment

- Compare the complete historical client/test source at
  `94466b37e4af1b6d82c8ff782ad83659d2f753fa` with complete current-baseline
  source at `154828f5ddff2a849b52bd3ed385a25db6188b02`.
- Build each selected source, run its unchanged original tests and conftest,
  and load only the diagnostic plugin from the controller checkout.
- Run 20 repetitions per original test in one pytest session, alternating
  `test_connect_via_channel` and `test_generic_grpc_exception`.
  This is 40 planned test items per client revision, not pytest retries.
- Keep `PYMAPDL_DEBUG_TESTING=True`, as recorded in both historical failed jobs.
  This retains each revision's own DEBUG fixture/restart behavior.
- Disable random reordering, pytest reruns and coverage; stop at the first
  failing item. Keep the normal 180-second thread-method per-test timeout.
- Pin the server to `ghcr.io/ansys/mapdl:v25.2.0@sha256:c3ce3fa6a49304fd4e083ba2e0b3bc6c32cbb4b91673cfee2775a79c14b84b4c`.
  The tag is retained because the launcher parses the MAPDL release from it;
  Docker resolves the immutable digest.
- Resolve test dependencies once and use that shared constraints artifact for
  both clients. The selected revisions have identical runtime and test extras.
  Install the entire shared resolved environment, then build each client with
  `--no-isolation` so the shared pinned flit backend is used. Record package versions and hashes of the installed library,
  subject test source, controller plugin and constraints.
- Preserve all original fixture lifetimes and cleanup behavior. Do not add
  raw health RPCs, new channel-pool options, sleeps or extra cleanup.

## Trace

`ctrl_path_trace.py` uses Python trace events, without replacing library
functions or stub methods. It records selected constructor/connection/Ctrl
calls, raw exception type and gRPC status, and executed line/return events in
`is_alive`. Match the recorded line to the exact selected source to locate a
False branch. Only scalar private state is sampled; no RPC is issued.

The generic-exception test intentionally injects UNAVAILABLE and later expects
False. Those events are not evidence of a server failure. A passing constructor
followed by an unexpected failing initial assertion is the primary target.
Exception propagation can produce several events for one underlying RPC;
trace event totals are not counts of independent RPCs or failure-rate trials.

Only status, line numbers, flags, package versions, hashes and pytest item IDs
are public. No exception messages, response payloads, endpoints or raw server
logs are copied to the public trace. Existing Docker logs remain encrypted.
The diagnostic artifact has seven-day retention and is uploaded even if the
experiment fails; this does not change ordinary pytest-report upload policy.

Tracing changes timing and does not cover native C-core internals or Python
threads already running when tracing is enabled. Both clients use identical
observer code. Coverage/debugger tracing is rejected, not silently replaced.
The existing 2-second post-test raw Ctrl probe is disabled in this experiment.
Recorder-only failures disable tracing and mark the evidence incomplete. They
are not raised into the observed client; an otherwise passing session receives
a separate diagnostic error exit code. Original test failures remain failures.

No production fix or PR is part of this branch. Negative results do not prove
that the historical failure cannot recur.
