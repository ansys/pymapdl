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


## Historical-order replay after isolated checks passed

Run 44103847097 passed all 40 original test items on both historical and
current source, with all 80 initial liveness assertions True. Each arm made
180 existing VERSION calls, with no raw Ctrl exception. The matched dependency
snapshot from that run is committed in `ctrl-path-constraints.txt` for this
throwaway replay only; it is not a change to normal project requirements.

The second workflow replays two bounded historical sequences on both client
revisions, at most two remote jobs at once:

- November 9: the last 20 unique completed predecessors before the first
  generic-exception failure, that generic test once, all 21 intervening items,
  and the connect-via-channel test once: 43 items.
- November 10: the corresponding 20 predecessors, generic test once, all 11
  intervening items, and connect test once: 33 items.

This is 152 planned items over four arms, unless an earlier failure stops an
arm. Original retry attempts are not replayed; pytest retries remain disabled.
The two target IDs receive one diagnostic parameter; all other original item
IDs and the recorded relative order are retained. The trace collection event
and pytest reports must confirm this order. A historical skipped body may
remain skipped; a collected item is not necessarily an executed test body.

This is not a replay of the preceding 3,000-4,000 full-suite items. Passing a
bounded sequence cannot rule out a longer-lived state or resource dependency.


### Corrected exit-state telemetry

Independent raw-data QA found that the first 80-item run recorded `exited=null`:
`_exited` is an inherited property backed by `_MapdlCore__exited`, not a direct
`_exited` dict entry. Its raw RPC and actual initial `is_alive=True` return
observations remain valid, but the missing flag must not be interpreted as
False. The ordering observer reads the real backing key directly and is tested
against the real class property without running its constructor. This is a
telemetry-only correction, not a library/liveness change. The observer hash
therefore changes between the initial comparison and the replay; all four
replay arms still share identical observer bytes.


## Final larger comparison in this pass

The four bounded replays in run 44108874952 all passed: 152 collected items,
146 passed calls, six skipped items, eight initial liveness returns True, and
no raw Ctrl error. Corrected exit-state snapshots were False at all eight
initial checks. Shared constraints and all 169 non-project packages matched
the initial comparison.

The final planned comparison replays the complete November 9 recorded prefix:
3,939 unique completed predecessors plus the first generic-exception target,
once on each pinned client source (3,940 planned items per arm). The historical
predecessors were 3,795 passed, 140 skipped and four xfailed items, with no
prior failed or rerun attempt. Retain all selectors and their recorded order;
repeat neither historical retries nor the later connect failure.

The RPC observer logic, shared frozen dependencies, image, DEBUG mode and
no-retry/first-failure rules are unchanged from the bounded replay.
This reproduces recorded item order, not original random data, CPU scheduling,
wall time or every external condition. It is not a claim of bit-for-bit process
reproduction. If no failure is captured, do not launch more CI blindly: report
the negative results and remaining uncertainty for a next diagnostic decision.


### Hold the original test tree fixed for the full prefix

Current tests renamed seven plotting selectors present in the historical log;
a current-tree collect-only check correctly rejected those selectors. None
was silently dropped or renamed. For the final pair, both arms therefore run
the entire original historical test tree at `94466b37...`; only the complete
installed library changes between the two pinned revisions. This also holds
the original DEBUG fixture/restart helper fixed, unlike earlier phases which
used each revision's own tests. The metadata separately records library source,
actual test source, and their hashes. No old test body is edited or copied into
a current test module. The observer's RPC/return tracing is unchanged; only its
provenance header is extended to describe the separate test tree.


The full-prefix command also explicitly retains the original remote CI's
`--ignore_image_cache` flag. This replay is not an image-regression experiment.
Coverage remains disabled because it conflicts with Python tracing; the
original jobs had coverage enabled, so instrumentation/performance is still
an explicit difference from their execution.
