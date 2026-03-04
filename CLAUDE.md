# PyMAPDL — Claude Code Instructions

This file gives Claude Code persistent context for the PyMAPDL project.
See `AGENTS.md` for the full project overview and workflow.

## Agents

Four specialized agents are defined in `.github/agents/`. Reference them
by name when delegating tasks:

- **developer** — Feature implementation, bug fixes, API design
  @.github/agents/developer.agent.md

- **tester** — Test coverage, mocking strategies, test infrastructure
  @.github/agents/tester.agent.md

- **documentation** — Docstring reviews, style compliance, vale/codespell
  @.github/agents/documentation.agent.md

- **reviewer** — PR reviews and quality gates
  @.github/agents/reviewer.agent.md

## Workflow

Developer → Tester → Documentation Specialist → Reviewer → Merge

Every new feature must achieve ≥90% test coverage before merge.

## Quick Reference

### Running without a live MAPDL instance

```sh
# Windows
SET PYMAPDL_START_INSTANCE=False
uv run pytest

# Linux/macOS
export PYMAPDL_START_INSTANCE=False
uv run pytest
```

### Code quality

```sh
uv run pre-commit run --all-files   # Run all checks (mandatory before commit)
```

### Key constraints

- Do **not** modify `src/ansys/mapdl/core/_commands/` (auto-generated)
- Override MAPDL commands in `_MapdlCommandExtended` in `mapdl_extended.py`
- Use `uv` to run Python; fall back to `.venv` if needed
- All public methods need **numpydoc**-style docstrings
- Nested context managers must use the grouped `with (...):` form
- Avoid bare or overly broad exceptions
