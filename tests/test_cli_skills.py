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

"""Tests for the ``pymapdl skills`` CLI command group."""

import pathlib
from unittest.mock import patch

from click.testing import CliRunner
import pytest

from ansys.mapdl.core.cli.skills import _parse_frontmatter, skills

MOCK_SKILL_CONTENT = """\
---
name: pymapdl-cli
description: Test skill description.
---

# Test Skill

Test content here.
"""


def _make_mock_skills_dir(tmp_path: pathlib.Path) -> pathlib.Path:
    """Create a minimal fake skills directory for tests."""
    skill_dir = tmp_path / "pymapdl-cli"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(MOCK_SKILL_CONTENT, encoding="utf-8")
    return tmp_path


# ---------------------------------------------------------------------------
# _parse_frontmatter unit tests
# ---------------------------------------------------------------------------


def test_parse_frontmatter_basic():
    meta, body = _parse_frontmatter(MOCK_SKILL_CONTENT)
    assert meta["name"] == "pymapdl-cli"
    assert meta["description"] == "Test skill description."
    assert "# Test Skill" in body


def test_parse_frontmatter_no_frontmatter():
    text = "# Just a heading\n\nSome content."
    meta, body = _parse_frontmatter(text)
    assert meta == {}
    assert body == text


# ---------------------------------------------------------------------------
# pymapdl skills list
# ---------------------------------------------------------------------------


def test_skills_list(tmp_path):
    mock_dir = _make_mock_skills_dir(tmp_path)
    runner = CliRunner()
    with patch("ansys.mapdl.core.cli.skills._find_skills_dir", return_value=mock_dir):
        result = runner.invoke(skills, ["list"])
    assert result.exit_code == 0
    assert "pymapdl-cli" in result.output
    assert "Test skill description." in result.output


def test_skills_list_no_skills(tmp_path):
    runner = CliRunner()
    with patch("ansys.mapdl.core.cli.skills._find_skills_dir", return_value=tmp_path):
        result = runner.invoke(skills, ["list"])
    assert result.exit_code == 0
    assert "No skills" in result.output


# ---------------------------------------------------------------------------
# pymapdl skills show
# ---------------------------------------------------------------------------


def test_skills_show_known(tmp_path):
    mock_dir = _make_mock_skills_dir(tmp_path)
    runner = CliRunner()
    with patch("ansys.mapdl.core.cli.skills._find_skills_dir", return_value=mock_dir):
        result = runner.invoke(skills, ["show", "pymapdl-cli"])
    assert result.exit_code == 0
    assert "# Test Skill" in result.output
    assert "Test content here." in result.output


def test_skills_show_unknown(tmp_path):
    mock_dir = _make_mock_skills_dir(tmp_path)
    runner = CliRunner()
    with patch("ansys.mapdl.core.cli.skills._find_skills_dir", return_value=mock_dir):
        result = runner.invoke(skills, ["show", "nonexistent-skill"])
    assert result.exit_code != 0
    assert "ERROR" in result.stderr
    assert "pymapdl skills list" in result.stderr or "list" in result.stderr


# ---------------------------------------------------------------------------
# pymapdl skills install — claude (local)
# ---------------------------------------------------------------------------


def test_skills_install_claude_local(tmp_path):
    mock_dir = _make_mock_skills_dir(tmp_path)
    runner = CliRunner()
    with runner.isolated_filesystem():
        with patch(
            "ansys.mapdl.core.cli.skills._find_skills_dir", return_value=mock_dir
        ):
            result = runner.invoke(
                skills,
                ["install", "pymapdl-cli", "--env", "claude", "--local", "--yes"],
            )
    assert result.exit_code == 0, result.output + (result.stderr or "")


def test_skills_install_claude_local_files(tmp_path):
    mock_dir = _make_mock_skills_dir(tmp_path)
    runner = CliRunner()
    with runner.isolated_filesystem() as iso_dir:
        iso = pathlib.Path(iso_dir)
        with patch(
            "ansys.mapdl.core.cli.skills._find_skills_dir", return_value=mock_dir
        ):
            result = runner.invoke(
                skills,
                ["install", "pymapdl-cli", "--env", "claude", "--local", "--yes"],
            )
        assert result.exit_code == 0, result.output
        dest_skill_md = iso / ".claude" / "skills" / "pymapdl-cli" / "SKILL.md"
        assert dest_skill_md.exists(), "SKILL.md should be copied to .claude/skills/"
        claude_md = iso / "CLAUDE.md"
        assert claude_md.exists(), "CLAUDE.md should be created"
        assert "@.claude/skills/pymapdl-cli/SKILL.md" in claude_md.read_text()


# ---------------------------------------------------------------------------
# pymapdl skills install — claude (global)
# ---------------------------------------------------------------------------


def test_skills_install_claude_global(tmp_path):
    mock_dir = _make_mock_skills_dir(tmp_path)
    fake_home = tmp_path / "fake_home"
    fake_home.mkdir()
    runner = CliRunner()
    with patch("ansys.mapdl.core.cli.skills._find_skills_dir", return_value=mock_dir):
        with patch("pathlib.Path.home", return_value=fake_home):
            result = runner.invoke(
                skills,
                ["install", "pymapdl-cli", "--env", "claude", "--global", "--yes"],
            )
    assert result.exit_code == 0, result.output + (result.stderr or "")
    dest = fake_home / ".claude" / "skills" / "pymapdl-cli" / "SKILL.md"
    assert dest.exists(), "SKILL.md should be in global ~/.claude/skills/"


# ---------------------------------------------------------------------------
# pymapdl skills install — copilot (local)
# ---------------------------------------------------------------------------


def test_skills_install_copilot_local(tmp_path):
    mock_dir = _make_mock_skills_dir(tmp_path)
    runner = CliRunner()
    with runner.isolated_filesystem() as iso_dir:
        iso = pathlib.Path(iso_dir)
        with patch(
            "ansys.mapdl.core.cli.skills._find_skills_dir", return_value=mock_dir
        ):
            result = runner.invoke(
                skills,
                ["install", "pymapdl-cli", "--env", "copilot", "--yes"],
            )
        assert result.exit_code == 0, result.output + (result.stderr or "")
        skill_md = iso / ".github" / "skills" / "pymapdl-cli" / "SKILL.md"
        assert skill_md.exists(), "SKILL.md should be written to .github/skills/"
        copilot_instructions = iso / ".github" / "copilot-instructions.md"
        assert (
            not copilot_instructions.exists()
        ), "copilot-instructions.md should not be created"


# ---------------------------------------------------------------------------
# pymapdl skills install — codex (local)
# ---------------------------------------------------------------------------


def test_skills_install_codex_local(tmp_path):
    mock_dir = _make_mock_skills_dir(tmp_path)
    runner = CliRunner()
    with runner.isolated_filesystem() as iso_dir:
        iso = pathlib.Path(iso_dir)
        with patch(
            "ansys.mapdl.core.cli.skills._find_skills_dir", return_value=mock_dir
        ):
            result = runner.invoke(
                skills,
                ["install", "pymapdl-cli", "--env", "codex", "--yes"],
            )
        assert result.exit_code == 0, result.output + (result.stderr or "")
        agents_md = iso / "AGENTS.md"
        assert agents_md.exists(), "AGENTS.md should be created"
        content = agents_md.read_text()
        assert "## Skill: pymapdl-cli" in content
        assert "Test content here." in content


# ---------------------------------------------------------------------------
# pymapdl skills install — cursor (local)
# ---------------------------------------------------------------------------


def test_skills_install_cursor_local(tmp_path):
    mock_dir = _make_mock_skills_dir(tmp_path)
    runner = CliRunner()
    with runner.isolated_filesystem() as iso_dir:
        iso = pathlib.Path(iso_dir)
        with patch(
            "ansys.mapdl.core.cli.skills._find_skills_dir", return_value=mock_dir
        ):
            result = runner.invoke(
                skills,
                ["install", "pymapdl-cli", "--env", "cursor", "--yes"],
            )
        assert result.exit_code == 0, result.output + (result.stderr or "")
        mdc_file = iso / ".cursor" / "rules" / "pymapdl-cli.mdc"
        assert mdc_file.exists(), ".mdc file should be created"
        content = mdc_file.read_text()
        assert "description: Test skill description." in content
        assert "# Test Skill" in content


# ---------------------------------------------------------------------------
# pymapdl skills install — copies files but excludes evals/
# ---------------------------------------------------------------------------


def test_skills_install_copies_all_files_except_evals(tmp_path):
    mock_dir = _make_mock_skills_dir(tmp_path)
    # Add an extra file and an evals/ dir to the skill
    skill_dir = mock_dir / "pymapdl-cli"
    (skill_dir / "extra.md").write_text("extra content", encoding="utf-8")
    evals_dir = skill_dir / "evals"
    evals_dir.mkdir()
    (evals_dir / "eval1.yaml").write_text("eval: data", encoding="utf-8")

    runner = CliRunner()
    with runner.isolated_filesystem() as iso_dir:
        iso = pathlib.Path(iso_dir)
        with patch(
            "ansys.mapdl.core.cli.skills._find_skills_dir", return_value=mock_dir
        ):
            result = runner.invoke(
                skills,
                ["install", "pymapdl-cli", "--env", "claude", "--yes"],
            )
        assert result.exit_code == 0, result.output
        dest = iso / ".claude" / "skills" / "pymapdl-cli"
        assert (dest / "SKILL.md").exists()
        assert (dest / "extra.md").exists(), "extra.md should be copied"
        assert not (dest / "evals").exists(), "evals/ should NOT be copied"


# ---------------------------------------------------------------------------
# Confirmation prompt behavior
# ---------------------------------------------------------------------------


def test_skills_install_confirmation_prompt_abort(tmp_path):
    mock_dir = _make_mock_skills_dir(tmp_path)
    runner = CliRunner()
    with runner.isolated_filesystem() as iso_dir:
        iso = pathlib.Path(iso_dir)
        with patch(
            "ansys.mapdl.core.cli.skills._find_skills_dir", return_value=mock_dir
        ):
            result = runner.invoke(
                skills,
                ["install", "pymapdl-cli", "--env", "claude"],
                input="n\n",
            )
        # User said 'n' — should abort
        assert result.exit_code != 0
        assert not (iso / ".claude").exists(), "Nothing should be written on abort"


def test_skills_install_yes_flag_skips_prompt(tmp_path):
    mock_dir = _make_mock_skills_dir(tmp_path)
    runner = CliRunner()
    with runner.isolated_filesystem() as iso_dir:
        iso = pathlib.Path(iso_dir)
        with patch(
            "ansys.mapdl.core.cli.skills._find_skills_dir", return_value=mock_dir
        ):
            result = runner.invoke(
                skills,
                ["install", "pymapdl-cli", "--env", "claude", "--yes"],
            )
        assert result.exit_code == 0, result.output
        assert (iso / ".claude" / "skills" / "pymapdl-cli" / "SKILL.md").exists()


# ---------------------------------------------------------------------------
# Idempotency
# ---------------------------------------------------------------------------


def test_skills_install_idempotent(tmp_path):
    mock_dir = _make_mock_skills_dir(tmp_path)
    runner = CliRunner()
    with runner.isolated_filesystem() as iso_dir:
        iso = pathlib.Path(iso_dir)
        with patch(
            "ansys.mapdl.core.cli.skills._find_skills_dir", return_value=mock_dir
        ):
            # First install
            r1 = runner.invoke(
                skills,
                ["install", "pymapdl-cli", "--env", "claude", "--yes"],
            )
            assert r1.exit_code == 0, r1.output
            # Second install
            r2 = runner.invoke(
                skills,
                ["install", "pymapdl-cli", "--env", "claude", "--yes"],
            )
            assert r2.exit_code == 0, r2.output

        claude_md = iso / "CLAUDE.md"
        content = claude_md.read_text()
        occurrences = content.count("@.claude/skills/pymapdl-cli/SKILL.md")
        assert (
            occurrences == 1
        ), f"Reference should appear exactly once, found {occurrences}"


# ---------------------------------------------------------------------------
# --global unsupported for copilot
# ---------------------------------------------------------------------------


def test_skills_install_global_unsupported_env(tmp_path):
    mock_dir = _make_mock_skills_dir(tmp_path)
    runner = CliRunner()
    with patch("ansys.mapdl.core.cli.skills._find_skills_dir", return_value=mock_dir):
        result = runner.invoke(
            skills,
            ["install", "pymapdl-cli", "--env", "copilot", "--global", "--yes"],
        )
    assert result.exit_code != 0
    assert "ERROR" in result.stderr
    assert "not supported" in result.stderr


# ---------------------------------------------------------------------------
# `pymapdl skill` / `pymapdl skills` alias parity
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "sub_args",
    [
        ["list"],
        ["show", "pymapdl-cli"],
        ["install", "pymapdl-cli", "--env", "claude", "--yes"],
    ],
    ids=["list", "show", "install"],
)
def test_skill_and_skills_alias_produce_identical_output(sub_args, tmp_path):
    """``pymapdl skill <sub>`` and ``pymapdl skills <sub>`` must behave identically.

    Both spellings route through ``_AliasedGroup`` in ``cli/__init__.py``.
    This test invokes the top-level ``main`` group with each spelling and
    asserts that exit codes and normalized stdout are the same.  Absolute
    paths printed by sub-commands (e.g. ``install``) are replaced with a
    ``<CWD>`` placeholder before comparison so that differing temp directories
    do not cause spurious failures.
    """
    import re

    from ansys.mapdl.core.cli import main

    runner = CliRunner()

    singular_mock = _make_mock_skills_dir(tmp_path / "singular")
    plural_mock = _make_mock_skills_dir(tmp_path / "plural")

    def _run(args, mock_dir):
        with runner.isolated_filesystem() as iso:
            with patch(
                "ansys.mapdl.core.cli.skills._find_skills_dir",
                return_value=mock_dir,
            ):
                result = runner.invoke(main, args)
            # Normalise the CWD path so outputs are comparable
            normalized = re.sub(re.escape(iso), "<CWD>", result.output)
        return result.exit_code, normalized

    singular_code, singular_out = _run(["skill"] + sub_args, singular_mock)
    plural_code, plural_out = _run(["skills"] + sub_args, plural_mock)

    assert singular_code == plural_code, (
        f"Exit codes differ: 'skill' exited {singular_code}, "
        f"'skills' exited {plural_code}"
    )
    assert singular_out == plural_out, (
        "'pymapdl skill' and 'pymapdl skills' produced different output:\n"
        f"  skill:  {singular_out!r}\n"
        f"  skills: {plural_out!r}"
    )
