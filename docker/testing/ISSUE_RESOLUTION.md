# Issue Resolution Summary

## Problem
The test `test_wait_for_job_ready_pending_then_running` was failing with a `StopIteration` error in the `ansys.mapdl.core.launcher.hpc` module tests.

### Root Cause
The test mocked `time.time()` globally with `side_effect = [0, 1, 2]`, expecting only 3 calls:
1. Start time (0)
2. First loop iteration (1)
3. Second loop iteration (2)

However, Python's logging module internally calls `time.time()` when creating log records. The `LOG.debug()` statement in `hpc.py` at line 470 triggered additional `time.time()` calls that exhausted the mock's side_effect list, causing `StopIteration`.

## Solution
The fix has been implemented in commits on the `refactor/launcher.py` branch:
- `922080eb0`: Initial fix improving time mocking
- `5de55cadf`: Final fix using module-specific patching

### Key Changes
Changed from patching globally to patching at module level:

**Before:**
```python
with patch("time.time") as mock_time, patch("time.sleep"):
    pass
```

**After:**
```python
with patch("ansys.mapdl.core.launcher.hpc.time.time") as mock_time, patch(
    "ansys.mapdl.core.launcher.hpc.time.sleep"
):
    pass
```

This ensures only `time` module calls within `hpc.py` are mocked, not those in Python's logging module or other parts of the codebase.

## Status
✅ **FIXED** on `refactor/launcher.py` branch in commits:
- 922080eb0: fix: improve time mocking in TestWaitForJobReady for accurate timeout simulation
- 5de55cadf: fix: update time patching in TestWaitForJobReady to use module-specific references

## Branch Compatibility Note
The `refactor/launcher.py` branch has a restructured launcher module (directory structure) that is incompatible with the current `fix/pytest-not-failing` branch (which has launcher.py as a single file). The fix cannot be directly cherry-picked without resolving structural conflicts.

## Files Affected (on refactor/launcher.py branch)
- `tests/test_launcher/test_hpc.py` (lines 557-558, 582-583)
