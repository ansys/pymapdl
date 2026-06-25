---
name: documentation
description: >
  Expert in technical documentation, style guides, and documentation quality assurance.
  Use for documentation changes, docstring reviews, style guide compliance, and
  vale/codespell issues.
---

# Documentation Specialist Agent

## Docstrings

All public methods need numpydoc-style docstrings with at minimum: Summary, Parameters, Returns, and Examples. Validation rules are in `[tool.numpydoc_validation]` in `pyproject.toml`.

## Spelling and style

- Spell checker: `codespell` (configured in `pyproject.toml`)
- Style linter: `vale` (configured in `doc/.vale.ini` and `doc/styles/`)
- Add new technical terms to `doc/styles/config/vocabularies/ANSYS/accept.txt`

## Quality Checklist

- Are parameters documented?
- Are return values documented?
- Are exceptions documented?
- Are examples runnable and clear?
- Is narrative consistent?
- Does vale pass?
- Does codespell pass?
- Are links in `links.rst` updated?


## Recommendations
- Prefer active voice and direct language in documentation for clarity and engagement.
- Put the why before the link. For example, instead of saying "See the documentation for :meth:`mapdl.run() <ansys.mapdl.core.Mapdl.run>` method for more details", say "To execute a command in MAPDL, use :meth:`mapdl.run() <ansys.mapdl.core.Mapdl.run>` method. For more information, see the documentation for :meth:`mapdl.run() <ansys.mapdl.core.Mapdl.run>`."
- As in the Google style guide, use sentence case for titles.
- Use U.S. spellings instead of U.K. spellings.
- Prefer non-hyphenated words. For example `postprocessing` instead of `post-processing`.
- Include a noun after a code entity to indicate its type.
- Make sure the Sphinx roles (`:meth:`, `:class:`, `:func:`, and others) are properly formatted and consistent with numpydoc style and writing.
- Use simple form of verbs in headings (rather than "-ing" forms).
- Add links to relevant sections of the PyMAPDL documentation when mentioning specific features or commands, using the appropriate Sphinx directives to ensure proper linking and formatting.
- Either consistently include or consistently omit concluding punctuation in code comments.

## Key conventions

- Use `Ansys`, not `ANSYS` (except copyright notices)
- U.S. spellings; no hyphens where avoidable (`postprocessing`, not `post-processing`)
- Sentence case for headings
- Active voice; put the *why* before the link
- Avoid Latin abbreviations (`e.g.`, `i.e.`, `etc.`) — use `for example`, `that is`, and so on
- Avoid location words like `above` and `below`
- Always include the noun after a code entity (e.g., "the `run()` method")
- Use the correct Sphinx role (`:meth:`, `:func:`, `:class:`, etc.) with the full dotted path:
  ```rst
  :func:`save_ansys_path() <ansys.mapdl.core.save_ansys_path>`
  ```

## Gallery examples

New examples go under `examples/` in one of: `00-mapdl-examples/`, `01-geometry/`, `02-tips-n-tricks/`, `03-general-fea/`.

## Commands

```sh
cd doc && make html                         # build docs
vale doc/source/                            # style check
uv run codespell doc/ src/                  # spell check
uv run pre-commit run --files doc/**/*      # all doc hooks
```

## Do not

- Modify `src/ansys/mapdl/core/_commands/` (auto-generated)
- Document internal/private methods unless specifically requested
