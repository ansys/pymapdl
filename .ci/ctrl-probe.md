# Ctrl diagnostic branch

Branch: `junk/ctrl-unimplemented-probe` (throwaway, based on `154828f5ddff2a849b52bd3ed385a25db6188b02`). This branch changes only step 1 diagnostics. The normal main workflow is not changed. Its branch-local `ci.yml` dispatches only Remote v25.2.0 and uses a unique run concurrency key, avoiding full-matrix cost and cancellation of earlier samples.

The raw `Ctrl(VERSION)` probe runs once at session start and after each test-attempt teardown report, outside the retry plugin's deferred finalizers. Every probe uses `grpc.use_local_subchannel_pool=1`, a new insecure channel (matching this CI job), a two-second RPC deadline and guaranteed context-manager close. It never uses `is_alive`, its fallback, MapdlGrpc construction, or /COM. It does not change library behavior or add retries.

Public `ctrl-diagnostics-remote-v25.2.0` artifacts contain status-only probe JSONL plus numeric per-container TCP-state, socket-descriptor and open-descriptor counts. Existing always-run Docker log capture and encrypted upload are reused; raw Docker logs are not made public. Public pytest-report upload behavior is unchanged (step 5 belongs to OMP).

Read `first_unimplemented=true`. If it occurs at `when=session_start`, no preceding test can be blamed: the state predates execution. Otherwise `nodeid` and `attempt` identify the completed attempt boundary; preserve the preceding OK record and surrounding sequence. A repeatable boundary is a candidate trigger, not proof that the named test alone caused the state. Random boundaries can also reflect accumulated state or unobserved background activity.

The probe deliberately creates thousands of additional connections, so it may itself advance onset. End-of-job counts are a snapshot, not a proof of a server leak; TIME_WAIT differs from live ESTABLISHED/CLOSE_WAIT connections and socket descriptors differ from unique connections. No unsupported 30–50% hit rate is assumed. The job runs serial pytest, not xdist. Ten dispatches are planned in small batches to limit license pressure; extra controls or targeted trigger loops depend on observed results.

Validation: eight offline tests pass, including actual pytest-rerunfailures integration demonstrating the final module teardown precedes the final probe. No local MAPDL instance or license secret is used.
