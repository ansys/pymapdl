---
name: tester
description: >
  Expert in Python testing, test coverage, mocking strategies, and PyMAPDL test
  infrastructure. Use for writing tests, improving coverage, fixing flaky tests,
  and reviewing test quality.
---

# Test Engineer Agent

## Coverage target

Minimum **90%** — run with:
```sh
uv run pytest --cov=src/ansys/mapdl/core --cov-report=term
```

## MAPDL instances are expensive — mock whenever possible

```python
from unittest.mock import Mock, patch


def test_feature_without_mapdl():
    mock_mapdl = Mock()
    mock_mapdl.some_method.return_value = expected_value
    ...
```

Existing fixtures are in `tests/conftest.py` (especially the `mapdl` fixture).

## Conditional skipping

Use `requires()` from `conftest.py` instead of `pytest.mark.skipif`:

```python
from conftest import requires


@requires("local")
def test_local_feature(mapdl): ...


@requires("remote")
def test_remote_feature(mapdl): ...
```

Accepted strings: `"local"`, `"remote"`, `"grpc"`, `"console"`, `"dpf"`, `"linux"`, `"nolinux"`, `"windows"`, `"nowindows"`, `"xserver"`, `"cicd"`, `"nocicd"`, `"gui"`, or any importable package name.

## Key env vars

| Variable | Purpose |
|---|---|
| `PYMAPDL_START_INSTANCE=False` | Connect to existing instance instead of launching one |
| `PYMAPDL_PORT` | gRPC server port (default `50052`) |
| `PYMAPDL_IP` | gRPC server IP (default `127.0.0.1`) |
| `ON_LOCAL` | Force `local` mode detection |
| `ON_CI` | Marks run as CI; some tests skip |

## pytest config

Configured with `--maxfail=2` in `pyproject.toml`. Override locally:
```sh
uv run pytest -p no:randomly --maxfail=100
```

## CI-like testing via tox + Docker

Same tox envs as documented in the developer agent. For testers, typical workflow:

If running test locally against local Docker images:
```sh
export PYMAPDL_PORT=50052
export PYMAPDL_START_INSTANCE=True
uvx tox -e docker-run-mapdl
pytest -v
uvx tox -e docker-stop-mapdl # Stop MAPDL
```

If running test locally inside a container (mirroring CI):
```sh
uvx tox -e docker-test-local    # or docker-test-remote to mirror CI exactly
```

Each directory that needs env vars contains an `example.env`. Copy to `.env` — tox loads it automatically.
