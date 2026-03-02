# PyMAPDL Agent instructions file

- Use `uv` to run python. If there is any issue, use the virtual environment in the repository (normally `.venv`).
- When creating tests, avoid running new MAPDL instances. Leverage `Mock` and `patch` functions to fake MAPDL instances.


## Style

- Avoid bare exceptions or too broad.
- when using nested context manager, prefer group them all as follows:

  ```py
  with (
      context_manager_0 as cm0,
      context_manager_1 as cm1,
  ):
      do_something()
  ```

## PyMAPDL modes

### Connectivity

PyMAPDL can connect to an MAPDL running locally (`local` mode) or running remote (`remote` mode).

### Connection type

PyMAPDL can connect to an MAPDL instance using:

- `grpc` connection: The default and recommended.
- `console` uses `pexpect` library and it is only compatible with linux. Discouraged.


## Testing

There are two main setup for testing based on the connectivity type: `local` and `remote`.

Additionally we test:
- local with minimal dependencies (`local-min`)
- local using console connection type (`local-console`).

### Running tests without a live MAPDL instance

Most tests require a running MAPDL process. To run only the unit tests that do
not need one, set the following environment variables before calling `pytest`:

```sh
export PYMAPDL_START_INSTANCE=False
export TESTING_MINIMAL=YES
```

On Windows:

```bat
SET PYMAPDL_START_INSTANCE=False
SET TESTING_MINIMAL=YES
```

`pytest` is configured in `pyproject.toml` with `--maxfail=2`, so the run
aborts after two failures. When iterating locally you may want to override
this: `uv run pytest -p no:randomly --maxfail=100 tests/test_foo.py`.

### Key environment variables

| Variable | Purpose |
|---|---|
| `PYMAPDL_START_INSTANCE` | `False` → connect to an existing instance instead of launching one |
| `PYMAPDL_PORT` | Port of the MAPDL gRPC server (default `50052`) |
| `PYMAPDL_IP` | IP of the MAPDL gRPC server (default `127.0.0.1`) |
| `ON_LOCAL` | Force `local` mode detection (`true`/`false`) |
| `TESTING_MINIMAL` | `YES` → skip tests that require heavy dependencies or a live MAPDL |
| `ON_CI` | Marks the run as a CI environment; some tests skip on CI |
| `PYMAPDL_DEBUG_TESTING` | `true` → enable DEBUG logging + write `pymapdl.log` |

### Conditional test skipping

Use the `requires()` helper from `tests/conftest.py` rather than writing
`pytest.mark.skipif` expressions by hand. Accepted string arguments:

`"local"`, `"remote"`, `"grpc"`, `"dpf"`, `"linux"`, `"nolinux"`,
`"windows"`, `"nowindows"`, `"xserver"`, `"cicd"`, `"nocicd"`,
`"console"`, `"gui"`, or any importable package name.

```python
from conftest import requires


@requires("local")
def test_something_local(mapdl): ...
```

## Developing

### Mapdl class

You cannot change the files in `src\ansys\mapdl\caore\_commands` directory.
If you need to update its behaviour, overwrite that command in the class ``_MapdlCommandExtended``
in ``src\ansys\mapdl\core\mapdl_extended.py``.

## Pre-commit hooks

Pre-commit is mandatory. Install once, then it runs on every `git commit`:

```sh
uv run pre-commit install
```

To run all checks manually:

```sh
uv run pre-commit run --all-files
```
`codespell` checks the spelling. If a word needs to be skipped add it to ``doc\styles\config\vocabularies\ANSYS\accept.txt``.

## Docstrings

All public functions and methods must have a **numpydoc**-style docstring.
The active validation checks are listed in `[tool.numpydoc_validation]` in
`pyproject.toml`.

## Dependency management

Runtime dependencies are pinned in `pyproject.toml` under `[project.dependencies]`.
Test and doc extras use exact version pins (`==`). Lock file is `uv.lock`.

To add or upgrade a dependency, edit `pyproject.toml` then run:

```sh
uv lock
```

Do **not** commit `uv.lock` changes as a side-effect of unrelated work.
