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

"""Tests for the ``.ci/check_no_comments.py`` ratchet lint rule."""

import importlib.util
import json
from pathlib import Path

import pytest

_SCRIPT = Path(__file__).resolve().parents[1] / ".ci" / "check_no_comments.py"
_spec = importlib.util.spec_from_file_location("check_no_comments", _SCRIPT)
assert _spec is not None and _spec.loader is not None
check = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(check)


@pytest.mark.parametrize(
    "source,expected",
    [
        ("# header\n# header\n\nx = 1\n", 0),
        ("x = 1\n# narration\ny = 2  # trailing\n", 2),
        ("import os  # noqa: F401\nx = 1  # type: ignore\n", 0),
        ("#: Sphinx attribute doc\nx = 1\n", 0),
        ("def f():  # numpydoc ignore=RT01\n    pass\n", 0),
        ('s = "# not a comment"\n', 0),
    ],
)
def test_count_comments(source, expected):
    assert check.count_comments(source) == expected


@pytest.fixture
def repo(tmp_path, monkeypatch):
    scope = tmp_path / "src" / "ansys" / "mapdl" / "core"
    (scope / "_commands").mkdir(parents=True)
    (tmp_path / ".ci").mkdir()
    monkeypatch.setattr(check, "ROOT", tmp_path)
    monkeypatch.setattr(check, "SCOPE", scope)
    monkeypatch.setattr(check, "EXCLUDED", (scope / "_commands",))
    monkeypatch.setattr(check, "BASELINE", tmp_path / ".ci" / "baseline.json")
    return scope


def test_ratchet(repo, capsys):
    mod = repo / "mod.py"
    mod.write_text("x = 1  # one\n# two\n")
    (repo / "_commands" / "gen.py").write_text("# generated\n\nx = 1  # ignored\n")

    assert check.main(["--update"]) == 0
    assert json.loads(check.BASELINE.read_text()) == {"src/ansys/mapdl/core/mod.py": 2}
    assert check.main([]) == 0

    mod.write_text("x = 1  # one\n# two\n# three\n")
    assert check.main([]) == 1
    assert "baseline allows 2" in capsys.readouterr().out

    mod.write_text("x = 1\n")
    assert check.main([]) == 1
    assert "--update" in capsys.readouterr().out
    assert check.main(["--update"]) == 0
    assert check.main([]) == 0
