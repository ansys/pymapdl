# PR #3649 — Refactor launcher module (essence)

## Intent / Motivation
- Break up the monolithic launcher into a clearer, testable package with single‑purpose modules.
- Make local, remote, console, gRPC, HPC/SLURM, and PyPIM flows explicit and easier to reason about.
- Consolidate shared launch/validation utilities in one place to reduce duplication and improve correctness.
- Improve test coverage by splitting launcher tests into focused units that mirror the new module layout.

## High‑level design changes
- **New package layout:** `ansys.mapdl.core.launcher` is now a package with multiple modules rather than a single `launcher.py` file.
- **Central orchestration:** `launch_mapdl` is now in `launcher/launcher.py`, calling dedicated helpers for local vs remote, gRPC vs console, and SLURM/PyPIM paths.
- **Shared utilities consolidated:** Low‑level helpers (port/IP selection, env var processing, exec discovery, slurm detection, etc.) moved into `launcher/tools.py`.
- **Specialized entrypoints:** New/clarified top‑level entrypoints for gRPC, console, remote connection, and HPC runs.

## New modules and their roles
- `src/ansys/mapdl/core/launcher/launcher.py`
  - Main `launch_mapdl` implementation: argument packing, validation, PyPIM delegation, SLURM routing, and final launch/connect.
- `src/ansys/mapdl/core/launcher/tools.py`
  - Shared utilities previously embedded in the old launcher: argument validation/packing, port/IP/version/exec discovery, lock‑file handling, env var merging, `generate_mapdl_launch_command`, `check_mapdl_launch`, etc.
- `src/ansys/mapdl/core/launcher/grpc.py`
  - gRPC‑specific launch path (`launch_mapdl_grpc`) and `launch_grpc` subprocess start.
- `src/ansys/mapdl/core/launcher/console.py`
  - Console‑mode launch (`launch_mapdl_console`) and console‑specific start parameter filtering.
- `src/ansys/mapdl/core/launcher/remote.py`
  - Dedicated `connect_to_mapdl` for remote connections (enforces a reduced, valid argument surface).
- `src/ansys/mapdl/core/launcher/local.py`
  - `processing_local_arguments` consolidates local start‑instance checks, environment setup, and validation.
- `src/ansys/mapdl/core/launcher/hpc.py`
  - SLURM/HPC helpers: detect SLURM env, compute resources, submit jobs, and resolve job/host info.
- `src/ansys/mapdl/core/launcher/pim.py`
  - PyPIM integration helpers (`is_ready_for_pypim`, `launch_remote_mapdl`).
- `src/ansys/mapdl/core/launcher/jupyter.py`
  - JupyterHub‑cluster launcher moved from `core/jupyter.py` into the launcher package.

## Public API and behavior changes
- `launch_mapdl` now orchestrates via modular helpers and includes explicit handling for:
  - **PyPIM:** if configured and `exec_file` is not provided, launch is delegated to PyPIM.
  - **SLURM/HPC:** detects SLURM, processes scheduler options, and wraps commands using `sbatch` when requested.
  - **Remote vs local:** `start_instance=False` goes through a dedicated remote connection path and preserves the `clear_on_connect` behavior.
- New **explicit connection API**: `connect_to_mapdl` in `launcher/remote.py` to connect to an existing instance with a constrained argument set.
- New **explicit gRPC/console helpers**: `launch_mapdl_grpc` and `launch_mapdl_console` provide clearly scoped launch functions.
- **`clear_on_connect` is now an allowed start parameter** in `MapdlGrpc` startup flow (added to `_ALLOWED_START_PARM`).

## Notable internal changes (key functions touched)
- `MapdlGrpc` now imports `get_start_instance` and stdout utilities from `launcher.tools` to avoid circular imports.
- `MapdlGrpc.__del__` includes a guard to skip cleanup if `start_instance` is false (avoid acting on remote connections).
- `misc.check_has_mapdl` now uses `launcher.tools.check_valid_ansys` after the refactor.
- `pool.py` and CLI stop tooling are updated to import functions from `launcher.tools`.

## Tests and validation updates
- Tests are **reorganized** into a new `tests/test_launcher/` directory, mirroring the new launcher package structure.
- New test modules cover:
  - gRPC launcher flow
  - console launcher flow
  - HPC/SLURM launch paths and resource parsing
  - local argument processing
  - remote connection constraints
  - JupyterHub launcher logic
  - shared tool utilities
- Existing launcher tests were updated to use the new import locations and to validate the refactored behavior.

## Files touched (high‑level)
- **New package files:** `src/ansys/mapdl/core/launcher/*` (multiple new modules listed above).
- **Moved files:** `src/ansys/mapdl/core/jupyter.py` → `src/ansys/mapdl/core/launcher/jupyter.py`.
- **Refactored/updated:**
  - `src/ansys/mapdl/core/__init__.py`
  - `src/ansys/mapdl/core/mapdl_core.py`
  - `src/ansys/mapdl/core/mapdl_grpc.py`
  - `src/ansys/mapdl/core/pool.py`
  - `src/ansys/mapdl/core/misc.py`
  - `src/ansys/mapdl/core/cli/stop.py`
- **Tests:** `tests/test_launcher.py` updated, plus many new tests in `tests/test_launcher/`.
- **Changelog:** `doc/changelog.d/3649.miscellaneous.md` added.

## Merge conflict hotspots to watch
- `src/ansys/mapdl/core/launcher.py` was **renamed and split** into a package. Expect conflicts if main added launcher changes in the old single file.
- Imports of launcher helpers throughout `core/` and `tests/` now point to `launcher.tools` or module‑specific files.
- `jupyter.py` move can cause path conflicts if main touched JupyterHub support.
- `MapdlGrpc` and `mapdl_core` changes affect initialization/start parameters and cleanup logic.
- Tests moved into a new subdirectory structure; any main‑branch changes in launcher tests may need manual reconciliation.

## One‑line summary
This PR refactors the MAPDL launcher into a modular package with dedicated local/remote/console/gRPC/HPC/PyPIM flows, centralizes shared utilities, updates imports and lifecycle handling, and reorganizes tests accordingly.
