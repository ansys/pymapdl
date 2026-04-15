# Copyright (C) 2016 - 2026 ANSYS, Inc. and/or its affiliates.
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

"""Static eval tests for ``src/ansys/mapdl/core/skills/pymapdl-cli/SKILL.md``.

These tests verify that ``SKILL.md`` contains all documentation terms required
for the eval assertions in ``evals/evals.json`` to pass.  They run without any
LLM call and catch regressions the moment a contributor removes or renames a
command, flag, or concept in the skill documentation.

How it works
------------
Each eval in ``evals.json`` lists *assertions* of the form::

    {"description": "...", "check": "contains 'pymapdl exec'"}

The ``check`` field describes what an LLM response *should* contain after
reading the skill.  Inverting this logic: if the LLM must respond with
``pymapdl exec``, then ``SKILL.md`` must document ``pymapdl exec``.

``_extract_skill_terms`` filters out prompt-specific values (port numbers,
file names) that would never appear verbatim in skill documentation, leaving
only the general syntax terms to check against ``SKILL.md``.

Running
-------
::

    uv run pytest tests/test_skill_pymapdl_cli.py -v

"""

import json
import pathlib
import re

import pytest

_TESTS_DIR = pathlib.Path(__file__).parent
_SKILL_MD = (
    _TESTS_DIR.parent
    / "src"
    / "ansys"
    / "mapdl"
    / "core"
    / "skills"
    / "pymapdl-cli"
    / "SKILL.md"
)
_EVALS_JSON = _TESTS_DIR / "skills" / "pymapdl-cli" / "evals" / "evals.json"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_PROMPT_SPECIFIC_RE = re.compile(
    r"^\d+$"  # bare number (e.g. port "50060")
    r"|.*\.\w{2,4}$"  # filename with extension (e.g. "thermal_model.inp")
)


def _load_evals() -> list[dict]:
    return json.loads(_EVALS_JSON.read_text(encoding="utf-8"))["evals"]


def _extract_skill_terms(check: str) -> list[str]:
    """Return quoted terms from a ``contains`` assertion that are *not* prompt-specific.

    Parameters
    ----------
    check : str
        Assertion ``check`` string, e.g. ``"contains '--file' and 'thermal_model.inp'"``.

    Returns
    -------
    list of str
        Terms that should be present in ``SKILL.md`` (prompt-specific values
        are filtered out).
    """
    quoted = re.findall(r"'([^']+)'", check)
    return [t for t in quoted if not _PROMPT_SPECIFIC_RE.match(t)]


def _contains_assertion_params() -> list[tuple]:
    """Build pytest.param objects for every ``contains`` assertion in evals.json."""
    params = []
    for eval_case in _load_evals():
        for assertion in eval_case["assertions"]:
            check = assertion["check"]
            if "contains" not in check:
                continue
            terms = _extract_skill_terms(check)
            if not terms:
                continue
            requires_all = " and " in check
            param_id = f"eval{eval_case['id']}-{assertion['description'][:50]}"
            params.append(
                pytest.param(
                    check,
                    terms,
                    requires_all,
                    assertion["description"],
                    id=param_id,
                )
            )
    return params


# ---------------------------------------------------------------------------
# SKILL.md existence / structure
# ---------------------------------------------------------------------------


def test_skill_md_exists() -> None:
    """SKILL.md must exist in the bundled skills directory."""
    assert _SKILL_MD.exists(), f"SKILL.md not found at {_SKILL_MD}"


def test_skill_md_has_frontmatter() -> None:
    """SKILL.md must begin with a YAML frontmatter block containing ``name`` and ``description``."""
    text = _SKILL_MD.read_text(encoding="utf-8")
    assert text.startswith("---"), "SKILL.md must start with '---' frontmatter"
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    assert m, "SKILL.md frontmatter is not properly closed with '---'"
    fm = m.group(1)
    assert "name:" in fm, "Frontmatter missing 'name:' field"
    assert "description:" in fm, "Frontmatter missing 'description:' field"


def test_evals_json_exists() -> None:
    """evals/evals.json must exist next to SKILL.md."""
    assert _EVALS_JSON.exists(), f"evals.json not found at {_EVALS_JSON}"


def test_evals_json_valid() -> None:
    """evals/evals.json must be valid JSON with the expected schema."""
    data = json.loads(_EVALS_JSON.read_text(encoding="utf-8"))
    assert "evals" in data, "evals.json missing top-level 'evals' key"
    assert (
        isinstance(data["evals"], list) and data["evals"]
    ), "'evals' must be a non-empty list"
    for ev in data["evals"]:
        assert "id" in ev, f"Eval entry missing 'id': {ev}"
        assert "prompt" in ev, f"Eval {ev.get('id')} missing 'prompt'"
        assert "assertions" in ev, f"Eval {ev.get('id')} missing 'assertions'"


# ---------------------------------------------------------------------------
# Static content coverage — driven by evals.json assertions
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "check,terms,requires_all,description",
    _contains_assertion_params(),
)
def test_skill_md_covers_eval_assertion(
    check: str, terms: list[str], requires_all: bool, description: str
) -> None:
    """SKILL.md must contain the syntax required by each eval assertion.

    Fails when a contributor edits SKILL.md in a way that removes documented
    commands or flags that the evals depend on.
    """
    skill_text = _SKILL_MD.read_text(encoding="utf-8")
    if requires_all:
        missing = [t for t in terms if t not in skill_text]
        assert not missing, (
            f"SKILL.md is missing the following term(s) required by assertion "
            f"'{description}': {missing!r}\n"
            f"  check: {check!r}"
        )
    else:
        assert any(t in skill_text for t in terms), (
            f"SKILL.md does not contain any of {terms!r} required by assertion "
            f"'{description}'\n"
            f"  check: {check!r}"
        )
