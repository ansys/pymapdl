# Copyright (C) 2016 - 2026 ANSYS, Inc. and/or its affiliates.
# Copyright (C) 2016 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
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

"""Tests for the plain functions behind the ``pymapdl`` CLI commands.

Each ``pymapdl`` sub-command is a thin Click wrapper (``<name>_cli``) around a
plain function (``<name>``) that lives in the same module, for example
:func:`ansys.mapdl.core.cli.stop.stop`. These tests exercise the plain
functions directly, without going through Click.
"""

import getpass
import pathlib
from unittest.mock import MagicMock, patch

import psutil
import pytest

from ansys.mapdl.core.cli.check import check, format_info
from ansys.mapdl.core.cli.convert import convert, resolve_graphics_backend
from ansys.mapdl.core.cli.exec import exec_commands, resolve_command_block
from ansys.mapdl.core.cli.help import help_command
from ansys.mapdl.core.cli.list_instances import list_instances
from ansys.mapdl.core.cli.skills import (
    UnknownSkillError,
    UnsupportedScopeError,
    install_skill,
    list_skills,
    plan_skill_install,
    show_skill,
)
from ansys.mapdl.core.cli.start import start
from ansys.mapdl.core.cli.stop import stop
from ansys.mapdl.core.errors import MapdlConnectionError, MapdlRuntimeError
from ansys.mapdl.core.plotting import GraphicsBackend

MOCK_SKILL_CONTENT = """\
---
name: pymapdl-cli
description: Test skill description.
---

# Test Skill

Test content here.
"""


def _make_mock_skills_dir(tmp_path: pathlib.Path) -> pathlib.Path:
    """Create a minimal fake skills directory."""
    skill_dir = tmp_path / "pymapdl-cli"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(MOCK_SKILL_CONTENT, encoding="utf-8")
    return tmp_path


def _make_mapdl_process(pid: int, port: int = 50052, name: str = "ansys251"):
    """Return a mock MAPDL process owned by the current user."""
    proc = MagicMock(spec=psutil.Process)
    proc.pid = pid
    proc.name.return_value = name
    proc.info = {"name": name}
    proc.status.return_value = psutil.STATUS_RUNNING
    proc.username.return_value = getpass.getuser()
    proc.cmdline.return_value = ["ansys251", "-grpc", "-port", str(port)]
    proc.children.return_value = []
    proc.cwd.return_value = "/cwd/of/ansys251"
    return proc


# ---------------------------------------------------------------------------
# Plain functions are not Click commands
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "func", [check, convert, exec_commands, help_command, list_instances, start, stop]
)
def test_plain_functions_are_not_click_commands(func):
    """The plain function is a regular callable, not a ``click.Command``."""
    assert not hasattr(func, "callback"), f"{func.__name__} must not be a Click command"
    assert not hasattr(func, "main"), f"{func.__name__} must not be a Click command"


# ---------------------------------------------------------------------------
# stop
# ---------------------------------------------------------------------------


def test_stop_defaults_to_the_default_port():
    """Without arguments, the instance on port 50052 is targeted."""
    from ansys.mapdl.core.cli.constants import MAPDL_DEFAULT_PORT

    with patch("ansys.mapdl.core.cli.stop.get_ansys_process_from_port") as mock_get:
        mock_get.return_value = None
        assert stop() == []

    mock_get.assert_called_once_with(MAPDL_DEFAULT_PORT)


def test_stop_returns_the_killed_pid():
    """The PID of the instance stopped by port is returned."""
    proc = _make_mapdl_process(pid=4321)

    with (
        patch(
            "ansys.mapdl.core.cli.stop.get_ansys_process_from_port",
            return_value=proc,
        ),
        patch("ansys.mapdl.core.cli.stop._kill_process") as mock_kill,
    ):
        assert stop(port=50053) == [4321]

    mock_kill.assert_called_once_with(proc)


def test_stop_all_returns_every_killed_pid():
    """``all=True`` stops every MAPDL process owned by the current user."""
    procs = [_make_mapdl_process(pid=1), _make_mapdl_process(pid=2)]

    with (
        patch("psutil.process_iter", return_value=procs),
        patch("psutil.pid_exists", return_value=True),
        patch("ansys.mapdl.core.cli.stop._kill_process"),
    ):
        assert stop(all=True) == [1, 2]


def test_stop_all_takes_precedence_over_port():
    """``all=True`` wins over an explicit port."""
    with (
        patch("psutil.process_iter", return_value=[]),
        patch("ansys.mapdl.core.cli.stop.get_ansys_process_from_port") as mock_get,
    ):
        assert stop(port=50055, all=True) == []

    mock_get.assert_not_called()


def test_stop_by_pid_kills_children_first():
    """Children are killed before the parent process."""
    child = MagicMock(spec=psutil.Process)
    child.pid = 99
    parent = MagicMock(spec=psutil.Process)
    parent.children.return_value = [child]

    killed = []

    with (
        patch("psutil.Process", return_value=parent),
        patch(
            "ansys.mapdl.core.cli.stop._kill_process",
            side_effect=lambda proc: killed.append(proc),
        ),
    ):
        stopped = stop(pid=12345)

    assert killed == [child, parent]
    assert stopped == [99, 12345]


def test_stop_by_pid_omits_a_surviving_process():
    """A process that outlives the kill is not reported as stopped."""
    parent = MagicMock(spec=psutil.Process)
    parent.children.return_value = []
    parent.wait.side_effect = psutil.TimeoutExpired(5)

    with (
        patch("psutil.Process", return_value=parent),
        patch("ansys.mapdl.core.cli.stop._kill_process"),
    ):
        assert stop(pid=12345) == []


# ---------------------------------------------------------------------------
# list_instances
# ---------------------------------------------------------------------------


def test_list_instances_returns_a_table():
    """The table holds one row per running instance."""
    with patch("psutil.process_iter", return_value=[_make_mapdl_process(pid=777)]):
        table = list_instances()

    assert "gRPC port" in table
    assert "777" in table
    assert "Command line" not in table


def test_list_instances_long_adds_every_column():
    """``long=True`` implies both the command line and the working directory."""
    with patch("psutil.process_iter", return_value=[_make_mapdl_process(pid=777)]):
        table = list_instances(long=True)

    assert "Command line" in table
    assert "Working directory" in table
    assert "/cwd/of/ansys251" in table


def test_list_instances_only_instances():
    """``instances=True`` hides the child processes and the extra column."""
    proc = _make_mapdl_process(pid=777)
    proc.children.return_value = []

    with patch("psutil.process_iter", return_value=[proc]):
        table = list_instances(instances=True)

    assert "Is Instance" not in table
    assert "777" not in table


# ---------------------------------------------------------------------------
# convert
# ---------------------------------------------------------------------------


def test_convert_returns_python_code():
    """APDL commands are converted to PyMAPDL calls."""
    assert convert("/prep7", only_commands=True).strip() == "mapdl.prep7()"


@pytest.mark.parametrize("backend", ["pyvista", "PYVISTA", "pyVISTa"])
def test_resolve_graphics_backend_accepts_any_case(backend):
    """Backend names are case insensitive."""
    assert resolve_graphics_backend(backend) is GraphicsBackend.PYVISTA


def test_resolve_graphics_backend_passes_members_through():
    """An already resolved member is returned unchanged."""
    assert resolve_graphics_backend(GraphicsBackend.MAPDL) is GraphicsBackend.MAPDL


def test_resolve_graphics_backend_rejects_unknown_names():
    """An unknown backend name raises ValueError."""
    with pytest.raises(ValueError, match="Invalid graphics backend"):
        resolve_graphics_backend("no_exists")


def test_resolve_graphics_backend_none():
    """``None`` means the MAPDL default is kept."""
    assert resolve_graphics_backend(None) is None


# ---------------------------------------------------------------------------
# start
# ---------------------------------------------------------------------------


def test_start_always_launches_a_new_instance():
    """``start`` forces ``start_instance=True`` and returns the address."""
    with patch("ansys.mapdl.core.launcher.launch_mapdl_process") as mock_launch:
        mock_launch.return_value = ("127.0.0.1", 50054, 4242)

        assert start(port=50054, nproc=8) == ("127.0.0.1", 50054, 4242)

    kwargs = mock_launch.call_args.kwargs
    assert kwargs["start_instance"] is True
    assert kwargs["port"] == 50054
    assert kwargs["nproc"] == 8


# ---------------------------------------------------------------------------
# check
# ---------------------------------------------------------------------------


def test_check_returns_the_information_dictionary():
    """``check`` connects and returns the diagnostic dictionary."""
    info = {"connection": {"ip": "127.0.0.1", "port": 50052}}

    with (
        patch("ansys.mapdl.core.cli.check.connect_to_instance") as mock_connect,
        patch("ansys.mapdl.core.information.get_mapdl_info", return_value=info),
    ):
        assert check(port=50052) == info

    assert mock_connect.call_args.kwargs["port"] == 50052


def test_check_propagates_connection_errors():
    """A connection failure surfaces as MapdlConnectionError."""
    with patch(
        "ansys.mapdl.core.cli.check.connect_to_instance",
        side_effect=MapdlConnectionError("refused"),
    ):
        with pytest.raises(MapdlConnectionError):
            check()


def test_format_info_renders_sections_and_subsections():
    """Nested dictionaries become indented subsections."""
    report = format_info(
        {
            "connection": {"ip": "127.0.0.1", "is_local": True},
            "information": {"units": {"length": "meter"}},
        }
    )
    lines = report.splitlines()

    assert "Connection" in lines
    assert "  Units" in lines

    ip_line = next(line for line in lines if line.strip().startswith("Ip"))
    assert ip_line.startswith("  ") and ip_line.endswith("127.0.0.1")

    length_line = next(line for line in lines if line.strip().startswith("Length"))
    assert length_line.startswith("    ") and length_line.endswith("meter")


def test_format_info_reports_section_errors():
    """A section holding an error only shows that error."""
    report = format_info({"mesh": {"error": "not available"}})

    assert "Error" in report
    assert "not available" in report


def test_format_info_applies_the_style_callback():
    """Section titles go through the style callable."""
    report = format_info({"mesh": {"n_node": 4}}, style=lambda text: f"<{text}>")

    assert "<Mesh>" in report


# ---------------------------------------------------------------------------
# exec_commands
# ---------------------------------------------------------------------------


def test_resolve_command_block_joins_commands():
    """Several commands are joined with newlines."""
    assert resolve_command_block(commands=["/prep7", "SAVE"]) == "/prep7\nSAVE"


def test_resolve_command_block_reads_a_script(tmp_path):
    """The content of a script file is used as is."""
    script = tmp_path / "script.inp"
    script.write_text("/prep7\nSAVE\n")

    assert "SAVE" in resolve_command_block(script_file=str(script))


def test_resolve_command_block_rejects_several_sources(tmp_path):
    """Only one command source may be given at a time."""
    script = tmp_path / "script.inp"
    script.write_text("/prep7\n")

    with pytest.raises(ValueError, match="Only one input source"):
        resolve_command_block(commands=["/prep7"], script_file=str(script))


def test_resolve_command_block_rejects_no_source():
    """At least one command source is required."""
    with patch("ansys.mapdl.core.cli.exec._stdin_has_data", return_value=False):
        with pytest.raises(ValueError, match="Provide commands"):
            resolve_command_block()


def test_resolve_command_block_rejects_empty_input():
    """Blank commands are rejected."""
    with pytest.raises(ValueError, match="input is empty"):
        resolve_command_block(commands=["   "])


def test_exec_commands_returns_the_mapdl_output():
    """The MAPDL output of the command block is returned."""
    mapdl = MagicMock()
    mapdl.input_strings.return_value = "output"

    with patch("ansys.mapdl.core.cli.exec.connect_to_instance", return_value=mapdl):
        assert exec_commands(commands=["/prep7"]) == "output"

    mapdl.input_strings.assert_called_once_with("/prep7")


def test_exec_commands_wraps_execution_errors():
    """An MAPDL failure is reported as MapdlRuntimeError."""
    mapdl = MagicMock()
    mapdl.input_strings.side_effect = RuntimeError("bad command")

    with patch("ansys.mapdl.core.cli.exec.connect_to_instance", return_value=mapdl):
        with pytest.raises(MapdlRuntimeError, match="Command execution failed"):
            exec_commands(commands=["/prep7"])


# ---------------------------------------------------------------------------
# help_command
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("command", ["/PREP7", "K", "*ABBR", r"\*ABBR"])
def test_help_command_returns_a_docstring(command):
    """Known MAPDL commands resolve to a rendered docstring."""
    pytest.importorskip("rich_rst")

    assert help_command(command).strip()


def test_help_command_rejects_unknown_commands():
    """An unknown MAPDL command raises ValueError."""
    pytest.importorskip("rich_rst")

    with pytest.raises(ValueError, match="No PyMAPDL method found"):
        help_command("UNKNOWNCMD999")


def test_help_command_prefix_is_significant():
    """``PREP7`` without the slash is not a command name."""
    pytest.importorskip("rich_rst")

    with pytest.raises(ValueError, match="No PyMAPDL method found"):
        help_command("PREP7")


# ---------------------------------------------------------------------------
# skills
# ---------------------------------------------------------------------------


def test_list_skills_reads_the_frontmatter(tmp_path):
    """Name and description come from the skill frontmatter."""
    skills = list_skills(_make_mock_skills_dir(tmp_path))

    assert [skill.name for skill in skills] == ["pymapdl-cli"]
    assert skills[0].description == "Test skill description."


def test_list_skills_missing_directory(tmp_path):
    """A missing skills directory yields no skill."""
    assert list_skills(tmp_path / "does-not-exist") == []


def test_show_skill_returns_the_file_content(tmp_path):
    """The full ``SKILL.md`` is returned, frontmatter included."""
    content = show_skill("pymapdl-cli", _make_mock_skills_dir(tmp_path))

    assert "# Test Skill" in content
    assert "name: pymapdl-cli" in content


def test_show_skill_unknown(tmp_path):
    """An unknown skill raises UnknownSkillError listing the alternatives."""
    with pytest.raises(UnknownSkillError) as excinfo:
        show_skill("nope", _make_mock_skills_dir(tmp_path))

    assert excinfo.value.available == ["pymapdl-cli"]


def test_plan_skill_install_does_not_touch_the_disk(tmp_path, monkeypatch):
    """Planning only reports the file operations."""
    monkeypatch.chdir(tmp_path)
    skills_dir = _make_mock_skills_dir(tmp_path / "skills")

    plan = plan_skill_install("pymapdl-cli", env="claude", skills_dir=skills_dir)

    assert plan.dest_dir == tmp_path / ".claude" / "skills" / "pymapdl-cli"
    assert plan.config_file == tmp_path / "CLAUDE.md"
    assert "Copy skill files to" in plan.summary
    assert not (tmp_path / ".claude").exists()


def test_plan_skill_install_rejects_unknown_env(tmp_path):
    """An unsupported environment raises ValueError."""
    with pytest.raises(ValueError, match="Unknown environment"):
        plan_skill_install(
            "pymapdl-cli", env="notepad", skills_dir=_make_mock_skills_dir(tmp_path)
        )


def test_plan_skill_install_rejects_global_for_copilot(tmp_path):
    """Copilot only supports a local installation."""
    with pytest.raises(UnsupportedScopeError):
        plan_skill_install(
            "pymapdl-cli",
            env="copilot",
            scope="global",
            skills_dir=_make_mock_skills_dir(tmp_path),
        )


def test_install_skill_writes_the_files(tmp_path, monkeypatch):
    """A local Claude installation copies the skill and updates CLAUDE.md."""
    monkeypatch.chdir(tmp_path)
    skills_dir = _make_mock_skills_dir(tmp_path / "skills")

    messages = install_skill("pymapdl-cli", env="claude", skills_dir=skills_dir)

    assert (tmp_path / ".claude" / "skills" / "pymapdl-cli" / "SKILL.md").exists()
    claude_md = (tmp_path / "CLAUDE.md").read_text()
    assert "@.claude/skills/pymapdl-cli/SKILL.md" in claude_md
    assert any("updated" in message for message in messages)


def test_install_skill_is_idempotent(tmp_path, monkeypatch):
    """Installing twice does not duplicate the reference."""
    monkeypatch.chdir(tmp_path)
    skills_dir = _make_mock_skills_dir(tmp_path / "skills")

    install_skill("pymapdl-cli", env="claude", skills_dir=skills_dir)
    messages = install_skill("pymapdl-cli", env="claude", skills_dir=skills_dir)

    claude_md = (tmp_path / "CLAUDE.md").read_text()
    assert claude_md.count("@.claude/skills/pymapdl-cli/SKILL.md") == 1
    assert any("already present" in message for message in messages)


def test_install_skill_cursor_writes_a_rule(tmp_path, monkeypatch):
    """The cursor environment gets a single ``.mdc`` rule file."""
    monkeypatch.chdir(tmp_path)
    skills_dir = _make_mock_skills_dir(tmp_path / "skills")

    install_skill("pymapdl-cli", env="cursor", skills_dir=skills_dir)

    rule = tmp_path / ".cursor" / "rules" / "pymapdl-cli.mdc"
    assert "description: Test skill description." in rule.read_text()


# ---------------------------------------------------------------------------
# connect_to_instance
# ---------------------------------------------------------------------------


def test_connect_to_instance_wraps_connection_failures():
    """Failures while connecting are reported as MapdlConnectionError."""
    from ansys.mapdl.core.cli.helpers import connect_to_instance

    with patch(
        "ansys.mapdl.core.launcher.connection.connect_to_existing",
        side_effect=ConnectionError("refused"),
    ):
        with pytest.raises(MapdlConnectionError, match="Could not connect to MAPDL"):
            connect_to_instance(ip="127.0.0.1", port=50052)


def test_connect_to_instance_wraps_configuration_failures():
    """Failures while resolving the configuration are reported too."""
    from ansys.mapdl.core.cli.helpers import connect_to_instance

    with patch(
        "ansys.mapdl.core.launcher.config.resolve_launch_config",
        side_effect=ValueError("bad port"),
    ):
        with pytest.raises(MapdlConnectionError, match="Could not resolve"):
            connect_to_instance(port=-1)


def test_connect_to_instance_attaches_the_original_error_as_a_note():
    """The low-level error is kept as a note instead of being appended inline."""
    from ansys.mapdl.core.cli.helpers import connect_to_instance

    with patch(
        "ansys.mapdl.core.launcher.connection.connect_to_existing",
        side_effect=ConnectionError("refused"),
    ):
        with pytest.raises(MapdlConnectionError) as excinfo:
            connect_to_instance(ip="127.0.0.1", port=50052)

    assert excinfo.value.notes == "refused"


def test_connect_to_instance_suppresses_the_original_traceback():
    """The re-raised error hides the low-level traceback, showing only its message."""
    from ansys.mapdl.core.cli.helpers import connect_to_instance

    with patch(
        "ansys.mapdl.core.launcher.connection.connect_to_existing",
        side_effect=ConnectionError("refused"),
    ):
        with pytest.raises(MapdlConnectionError) as excinfo:
            connect_to_instance(ip="127.0.0.1", port=50052)

    assert excinfo.value.__cause__ is None
    assert excinfo.value.__suppress_context__ is True


@pytest.mark.parametrize("error", [KeyError("boom"), AttributeError("boom")])
def test_connect_to_instance_does_not_mask_unexpected_configuration_errors(error):
    """Errors unrelated to configuration resolution are not disguised as connection errors."""
    from ansys.mapdl.core.cli.helpers import connect_to_instance

    with patch(
        "ansys.mapdl.core.launcher.config.resolve_launch_config", side_effect=error
    ):
        with pytest.raises(type(error)):
            connect_to_instance()


@pytest.mark.parametrize("error", [KeyError("boom"), RuntimeError("boom")])
def test_connect_to_instance_does_not_mask_unexpected_connection_errors(error):
    """Errors unrelated to the connection attempt are not disguised as connection errors."""
    from ansys.mapdl.core.cli.helpers import connect_to_instance

    with patch(
        "ansys.mapdl.core.launcher.connection.connect_to_existing", side_effect=error
    ):
        with pytest.raises(type(error)):
            connect_to_instance()


def test_connect_to_instance_does_not_double_wrap_mapdl_connection_errors():
    """A MapdlConnectionError raised by the client itself is not wrapped again."""
    from ansys.mapdl.core.cli.helpers import connect_to_instance

    original = MapdlConnectionError("gRPC handshake failed")
    with patch(
        "ansys.mapdl.core.launcher.connection.connect_to_existing",
        side_effect=original,
    ):
        with pytest.raises(MapdlConnectionError) as excinfo:
            connect_to_instance()

    assert excinfo.value is original
