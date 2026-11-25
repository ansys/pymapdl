# Copyright (C) 2016 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Ratchet lint rule that bans new code comments in ``src/ansys/mapdl/core``.

Each file may hold at most the number of comments recorded in
``.ci/no_comments_baseline.json``. Adding a comment fails; removing one
passes and asks you to lower the baseline with ``--update``.

Not counted: the license header, tool directives (``noqa``, ``type: ignore``,
``pragma``, ``fmt:``, ``nosec``, ``isort:``, ``numpydoc ignore``,
``codespell``) and Sphinx ``#:`` attribute doc comments.
See ``docs/adr/0022-ban-code-comments-with-a-ratchet.md``.
"""

import argparse
import io
import json
from pathlib import Path
import re
import sys
import tokenize

ROOT = Path(__file__).resolve().parents[1]
SCOPE = ROOT / "src" / "ansys" / "mapdl" / "core"
EXCLUDED = (SCOPE / "_commands",)
BASELINE = ROOT / ".ci" / "no_comments_baseline.json"
ALLOWED = re.compile(
    r"#(:|!|\s*(noqa|type:|pragma|fmt:|nosec|isort:|numpydoc ignore|codespell))"
)


def count_comments(source: str) -> int:
    """Count banned comments in Python ``source``."""
    lines = source.splitlines()
    header = 0
    while header < len(lines) and lines[header].startswith("#"):
        header += 1
    count = 0
    for token in tokenize.generate_tokens(io.StringIO(source).readline):
        if token.type != tokenize.COMMENT or token.start[0] <= header:
            continue
        if not ALLOWED.match(token.string):
            count += 1
    return count


def scan() -> dict[str, int]:
    """Return ``{relative_path: comment_count}`` for every file in scope."""
    counts = {}
    for path in sorted(SCOPE.rglob("*.py")):
        if any(path.is_relative_to(excluded) for excluded in EXCLUDED):
            continue
        count = count_comments(path.read_text(encoding="utf-8"))
        if count:
            counts[path.relative_to(ROOT).as_posix()] = count
    return counts


def main(argv: list[str] | None = None) -> int:
    """Compare current comment counts against the baseline."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--update", action="store_true", help="Rewrite the baseline file."
    )
    args = parser.parse_args(argv)

    current = scan()
    if args.update:
        BASELINE.write_bytes((json.dumps(current, indent=2) + "\n").encode("utf-8"))
        print(f"Baseline updated: {sum(current.values())} comments.")
        return 0

    baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
    grew = {f: n for f, n in current.items() if n > baseline.get(f, 0)}
    shrank = {f: n for f, n in current.items() if n < baseline.get(f, 0)}
    shrank.update({f: 0 for f in baseline if f not in current})

    for path, n in grew.items():
        print(
            f"{path}: {n} comments, baseline allows {baseline.get(path, 0)}. "
            "Express it in code, a docstring, or an ADR in docs/adr/."
        )
    if shrank:
        print(
            f"{len(shrank)} file(s) dropped below the baseline. Lock it in with: "
            "python .ci/check_no_comments.py --update"
        )
    return 1 if grew or shrank else 0


if __name__ == "__main__":
    sys.exit(main())
