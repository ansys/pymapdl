# PyMAPDL Repository AI Agents

This repository uses structured AI agents for development governance and quality assurance.

## Agents

Individual agent configurations are in the `.github/agents/` directory:

- **[Developer](.github/agents/developer.agent.md)** - Feature implementation, bug fixes, performance optimization, API design
- **[Documentation Specialist](.github/agents/documentation.agent.md)** - Documentation changes, docstring reviews, style guide compliance, vale/codespell issues
- **[Tester](.github/agents/tester.agent.md)** - Test coverage, mocking strategies, test infrastructure, flaky tests
- **[Reviewer](.github/agents/reviewer.agent.md)** - Comprehensive PR reviews and quality gates

**Workflow:** Developer → Tester → Documentation Specialist → Reviewer → Merge

Every new feature must achieve ≥90% test coverage before merge.

## Code Quality Principles

- Follow **PEP 8** (enforced by black, flake8, isort)
- Follow **Google style** for documentation prose
- Follow **numpydoc** for Python docstrings
- Target **90% test coverage**
- Use **mocking** to avoid unnecessary MAPDL launches
- Maintain **backward compatibility** (or properly deprecate)
- **Pre-commit hooks are mandatory**: Install with `uv run pre-commit install`, run manually with `uv run pre-commit run --all-files`

## General Instructions (All Agents)

### Tools
- Use `uv` to run Python. If issues arise, use the virtual environment in the repository (normally `.venv`)
- When creating tests, avoid running new MAPDL instances. Leverage `Mock` and `patch` functions to fake MAPDL instances

### Code Style
- Avoid bare exceptions or overly broad exception handling
- When using nested context managers, group them as follows:
  ```python
  with (
      context_manager_0 as cm0,
      context_manager_1 as cm1,
  ):
      do_something()
  ```

### PyMAPDL Modes

PyMAPDL can connect to MAPDL in two connectivity modes:
- **local** - MAPDL running locally
- **remote** - MAPDL running remotely

And two connection types:
- **grpc** - Default and recommended
- **console** - Uses `pexpect`, Linux-only, discouraged


### Key environment variables

| Variable | Purpose |
|---|---|
| `PYMAPDL_START_INSTANCE` | `False` → connect to an existing instance instead of launching one |
| `PYMAPDL_PORT` | Port of the MAPDL gRPC server (default `50052`) |
| `PYMAPDL_IP` | IP of the MAPDL gRPC server (default `127.0.0.1`) |
| `ON_LOCAL` | Force `local` mode detection (`true`/`false`) |
| `TESTING_MINIMAL` | `YES` → skip tests requiring heavy dependencies or live MAPDL |
| `ON_CI` | Marks the run as CI environment; some tests skip on CI |
| `PYMAPDL_DEBUG_TESTING` | `true` → enable DEBUG logging + write `pymapdl.log` |

## Testing

Test configurations by connectivity: `local`, `remote`, `local-min` (minimal dependencies), `local-console` (console connection type).

### Running tests without a live MAPDL instance

Most tests require a running MAPDL process. To run only unit tests that don't need one:

```sh
# Linux/macOS
export PYMAPDL_START_INSTANCE=False
export TESTING_MINIMAL=YES

# Windows
SET PYMAPDL_START_INSTANCE=False
SET TESTING_MINIMAL=YES
```

Then run pytest:
```sh
uv run pytest
```

Pytest is configured with `--maxfail=2` in `pyproject.toml`. Override locally:
```sh
uv run pytest --maxfail=100 tests/test_foo.py
```

### Conditional test skipping

Use the `requires()` helper from `tests/conftest.py` instead of `pytest.mark.skipif`:

```python
from conftest import requires


@requires("local")
def test_something_local(mapdl): ...


@requires("remote")
def test_something_remote(mapdl): ...
```

Accepted strings: `"local"`, `"remote"`, `"grpc"`, `"dpf"`, `"linux"`, `"nolinux"`, `"windows"`, `"nowindows"`, `"xserver"`, `"cicd"`, `"nocicd"`, `"console"`, `"gui"`, or any importable package name.

## Developing

### Mapdl class

You cannot change files in `src/ansys/mapdl/core/_commands`. To modify command behavior, overwrite in `_MapdlCommandExtended` class in `src/ansys/mapdl/core/mapdl_extended.py`.

## Pre-commit hooks

Pre-commit is mandatory and runs automatically on every `git commit`:

```sh
uv run pre-commit install          # Install once
uv run pre-commit run --all-files  # Run manually
```

To skip spelling checks, add words to `doc/styles/config/vocabularies/ANSYS/accept.txt`.

## Docstrings

All public functions and methods must have **numpydoc**-style docstrings. Active validation checks are in `[tool.numpydoc_validation]` in `pyproject.toml`.

## Dependency Management

Runtime dependencies are in `pyproject.toml` under the `dependencies` list in the `[project]` section. Test and doc extras are under `[project.optional-dependencies]` and use exact version pins (`==`).

To add or upgrade dependencies, update `pyproject.toml` directly.

## How to Use These Agents

See [.github/HOW_TO_USE_AGENTS.md](.github/HOW_TO_USE_AGENTS.md) for detailed instructions on invoking agents in different IDEs (VS Code, Cursor, JetBrains, etc.).
