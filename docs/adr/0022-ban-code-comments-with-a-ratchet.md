# Ban code comments in `src/` with a ratchet

Code comments in `src/ansys/mapdl/core/` drifted from the code: an audit of 2,660 comments found 1,376 tautologies, 229 stale comments, and 76 that excused a hack instead of fixing it. Only 149 recorded a real decision, and they are now ADRs `0004`–`0021`. We decided to ban new comments with `.ci/check_no_comments.py`, run as the `no-new-comments` pre-commit hook. The hook compares per-file comment counts against `.ci/no_comments_baseline.json`. Removing all comments in one pull request was not possible, because the rest are constraints set by MAPDL, gRPC, or the OS and need code or an ADR to replace them. A ratchet lets the count only go down.

## Consequences

- A change that adds a comment to a file in scope fails pre-commit. Express it in code, a docstring, or an ADR.
- A change that removes comments must lower the baseline with `python .ci/check_no_comments.py --update`, so the reduction cannot be lost.
- Not counted: license headers, tool directives (`noqa`, `type: ignore`, `pragma`, `fmt:`, `nosec`, `isort:`, `numpydoc ignore`, `codespell`), and Sphinx `#:` attribute doc comments.
- `src/ansys/mapdl/core/_commands/` is out of scope because it is generated (ADR `0001`); its comments are fixed in the generator.
- Hacks that comments used to excuse are tracked as tickets, not in the code.
