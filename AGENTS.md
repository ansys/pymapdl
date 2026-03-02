# PyMAPDL Repository AI Agents

This repository uses structured AI agents for development governance and quality assurance.

## Agents

Individual agent configurations are in the `.agents/` directory:

- **[Developer](.agents/developer.md)** - Feature implementation, bug fixes, performance optimization, API design
- **[Documentation Specialist](.agents/documentation.md)** - Documentation changes, docstring reviews, style guide compliance, vale/codespell issues
- **[Tester](.agents/tester.md)** - Test coverage, mocking strategies, test infrastructure, flaky tests
- **[Reviewer](.agents/reviewer.md)** - Comprehensive PR reviews and quality gates

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

## Pre-commit hooks

Pre-commit is mandatory and runs automatically on every `git commit`:

```sh
uv run pre-commit install          # Install once
uv run pre-commit run --all-files  # Run manually
```

To skip spelling checks, add words to `doc\styles\config\vocabularies\ANSYS\accept.txt`.

## Docstrings

All public functions and methods must have **numpydoc**-style docstrings. Active validation checks are in `[tool.numpydoc_validation]` in `pyproject.toml`.

## Dependency Management

Runtime dependencies are in `pyproject.toml` under `[project.dependencies]`. Test and doc extras use exact version pins (`==`). Lock file is `uv.lock`.

To add or upgrade dependencies:

```sh
uv lock
```

Do **not** commit `uv.lock` changes as side-effects of unrelated work.
