---
name: developer
description: >
  Expert PyMAPDL Python developer. Use for implementing new features, fixing bugs,
  performance optimization, and API design tasks in this repository.
---

# PyMAPDL Developer Agent

## Architecture constraints

- **Do not modify** `src/ansys/mapdl/core/_commands/` — auto-generated from MAPDL source.
- Override MAPDL commands in `_MapdlCommandExtended` in `src/ansys/mapdl/core/mapdl_extended.py`.
- Connection modes: `local` vs `remote`; `grpc` (default) vs `console` (console is discouraged, Linux-only).

## Dependencies

- Runtime deps: `[project.dependencies]` in `pyproject.toml`.
- Test/doc extras: exact pins (`==`) under `[project.optional-dependencies]`.
- Run `uv lock` after changes; don't commit unrelated `uv.lock` changes.

## Commands

```sh
uv run pre-commit install           # once
uv run pre-commit run --all-files   # before every commit
uv run pytest                       # tests (set PYMAPDL_START_INSTANCE=False to skip MAPDL)
```

## CI-like testing via tox + Docker

The repo provides tox envs that spin up MAPDL (and optionally DPF) Docker containers and run the full test matrix, matching CI. Use `uvx` so the pinned venv is used, as CI does.

Key envs:

| Env | Purpose |
|---|---|
| `docker-run-mapdl` | Start MAPDL container in background |
| `docker-run-mapdl-dpf` | Start MAPDL + DPF containers |
| `docker-stop-mapdl` | Stop/remove MAPDL containers |
| `docker-stop-mapdl-dpf` | Stop/remove MAPDL+DPF containers |
| `docker-test-local` | Run tests against local Docker images |
| `docker-test-remote` | Run tests mirroring CI (remote images) |
| `docker-test-local-build` | Build local images, then test |
| `docker-test-remote-build` | Trigger remote image build, then test |

Each directory that needs env vars contains an `example.env`. Copy to `.env` and edit — tox loads it automatically.

```sh
# Example (Unix/macOS)
export PYMAPDL_PORT=50052 PYMAPDL_START_INSTANCE=True
uvx tox -e docker-run-mapdl
uvx tox -e docker-test-local
uvx tox -e docker-stop-mapdl
```

## Workflow

1. Implement -> add/update numpydoc docstrings -> run pre-commit again
2. Delegate tests to **tester** agent (≥90% coverage required)
3. Delegate docs (docstring and Sphinx documentation) to **documentation** agent
4. Submit for **reviewer** agent approval
