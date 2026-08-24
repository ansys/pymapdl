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

"""``pymapdl skills`` sub-command group."""

from dataclasses import dataclass, field
import pathlib
import re
import sys
from typing import Any, Dict, List, Optional, Sequence, Tuple

import click

from ansys.mapdl.core.cli.constants import GLOBAL_UNSUPPORTED, SUPPORTED_ENVS

# Directories inside a skill that are never installed.
_EXCLUDED_DIRECTORIES = ("evals", "workspace")

_INCOMPLETE_PLAN_ERROR = (
    "The installation plan is missing paths required by the {env!r} environment."
)


class UnknownSkillError(ValueError):
    """Raised when the requested skill is not bundled with PyMAPDL.

    Parameters
    ----------
    skill_name : str
        Identifier that could not be resolved.
    available : sequence of str
        Identifiers of the skills that are available.
    """

    def __init__(self, skill_name: str, available: Sequence[str]) -> None:
        self.skill_name = skill_name
        self.available = list(available)
        super().__init__(
            f"Unknown skill {skill_name!r}. "
            "Run 'pymapdl skills list' to see available skills."
        )


class UnsupportedScopeError(ValueError):
    """Raised when an environment does not support the requested scope.

    Parameters
    ----------
    env : str
        AI coding environment.
    scope : str
        Requested installation scope.
    """

    def __init__(self, env: str, scope: str) -> None:
        self.env = env
        self.scope = scope
        super().__init__(f"--{scope} is not supported for the '{env}' environment.")


@dataclass(frozen=True)
class SkillInfo:
    """Metadata of a bundled skill.

    Parameters
    ----------
    name : str
        Skill identifier.
    description : str
        One-line description taken from the skill frontmatter.
    path : pathlib.Path
        Path to the ``SKILL.md`` file of the skill.
    """

    name: str
    description: str
    path: pathlib.Path


@dataclass(frozen=True)
class SkillInstallPlan:
    """Files an installation is going to create or update.

    Parameters
    ----------
    skill_name : str
        Skill identifier.
    env : str
        AI coding environment the skill is installed into.
    scope : str
        Either ``"local"`` or ``"global"``.
    skill_dir : pathlib.Path
        Directory holding the bundled skill files.
    skill_md_text : str
        Full content of the ``SKILL.md`` file.
    description : str
        Description taken from the skill frontmatter.
    body : str
        Content of ``SKILL.md`` without its frontmatter.
    actions : list of str
        Human-readable description of the planned file operations.
    dest_dir : pathlib.Path, optional
        Directory the skill files are copied to.
    dest_file : pathlib.Path, optional
        Single file the skill is written to.
    config_file : pathlib.Path, optional
        Configuration file of the environment that gets a reference appended.
    config_line : str, optional
        Reference line used to detect an already installed skill.
    config_text : str, optional
        Full text appended to *config_file*.
    section_header : str, optional
        Markdown heading used to detect an already installed skill.
    """

    skill_name: str
    env: str
    scope: str
    skill_dir: pathlib.Path
    skill_md_text: str
    description: str
    body: str
    actions: List[str] = field(default_factory=list)
    dest_dir: Optional[pathlib.Path] = None
    dest_file: Optional[pathlib.Path] = None
    config_file: Optional[pathlib.Path] = None
    config_line: Optional[str] = None
    config_text: Optional[str] = None
    section_header: Optional[str] = None

    @property
    def summary(self) -> str:
        """Return the planned file operations as a multi-line string."""
        return "\n".join(self.actions)


def list_skills(skills_dir: Optional[pathlib.Path] = None) -> List[SkillInfo]:
    """List the skills bundled with this PyMAPDL installation.

    Parameters
    ----------
    skills_dir : pathlib.Path, optional
        Directory holding one sub-directory per skill. Defaults to the
        directory bundled with the package.

    Returns
    -------
    list of SkillInfo
        Available skills, sorted by directory name. Empty when no skill is
        bundled.

    Examples
    --------
    Print the name of every bundled skill:

    >>> from ansys.mapdl.core.cli.skills import list_skills
    >>> [skill.name for skill in list_skills()]
    ['pymapdl-cli']

    """
    if skills_dir is None:
        skills_dir = _find_skills_dir()

    skills: List[SkillInfo] = []
    if not skills_dir.exists():
        return skills

    for entry in sorted(skills_dir.iterdir()):
        skill_md = entry / "SKILL.md"
        if not entry.is_dir() or not skill_md.exists():
            continue

        meta, _ = _parse_frontmatter(skill_md.read_text(encoding="utf-8"))
        skills.append(
            SkillInfo(
                name=meta.get("name", entry.name),
                description=meta.get("description", ""),
                path=skill_md,
            )
        )

    return skills


def show_skill(skill_name: str, skills_dir: Optional[pathlib.Path] = None) -> str:
    """Return the full ``SKILL.md`` content of a bundled skill.

    Parameters
    ----------
    skill_name : str
        Skill identifier, as reported by :func:`list_skills`.
    skills_dir : pathlib.Path, optional
        Directory holding one sub-directory per skill. Defaults to the
        directory bundled with the package.

    Returns
    -------
    str
        Content of the ``SKILL.md`` file, frontmatter included.

    Raises
    ------
    UnknownSkillError
        When *skill_name* is not bundled with PyMAPDL.

    Examples
    --------
    >>> from ansys.mapdl.core.cli.skills import show_skill
    >>> print(show_skill("pymapdl-cli"))

    """
    if skills_dir is None:
        skills_dir = _find_skills_dir()

    skill_md = skills_dir / skill_name / "SKILL.md"
    if not skill_md.exists():
        raise UnknownSkillError(
            skill_name, [skill.name for skill in list_skills(skills_dir)]
        )

    return skill_md.read_text(encoding="utf-8")


def plan_skill_install(
    skill_name: str,
    env: str,
    scope: str = "local",
    skills_dir: Optional[pathlib.Path] = None,
) -> SkillInstallPlan:
    """Resolve the file operations needed to install a skill.

    Nothing is written to disk. Pass the result to
    :func:`apply_skill_install` to perform the installation.

    Parameters
    ----------
    skill_name : str
        Skill identifier, as reported by :func:`list_skills`.
    env : str
        AI coding environment. One of :data:`SUPPORTED_ENVS`.
    scope : str, default: "local"
        Either ``"local"`` to install into the current working directory, or
        ``"global"`` to install into the home directory of the user.
    skills_dir : pathlib.Path, optional
        Directory holding one sub-directory per skill. Defaults to the
        directory bundled with the package.

    Returns
    -------
    SkillInstallPlan
        The files that are created or updated by the installation.

    Raises
    ------
    UnknownSkillError
        When *skill_name* is not bundled with PyMAPDL.
    UnsupportedScopeError
        When *env* does not support *scope*.
    ValueError
        When *env* is not a supported environment.

    Examples
    --------
    Inspect what a local Claude installation would do:

    >>> from ansys.mapdl.core.cli.skills import plan_skill_install
    >>> print(plan_skill_install("pymapdl-cli", "claude").summary)

    """
    if env not in SUPPORTED_ENVS:
        raise ValueError(
            f"Unknown environment {env!r}. "
            f"Supported environments are: {', '.join(SUPPORTED_ENVS)}."
        )

    if skills_dir is None:
        skills_dir = _find_skills_dir()

    skill_dir = skills_dir / skill_name
    if not skill_dir.exists() or not (skill_dir / "SKILL.md").exists():
        raise UnknownSkillError(
            skill_name, [skill.name for skill in list_skills(skills_dir)]
        )

    if scope == "global" and env in GLOBAL_UNSUPPORTED:
        raise UnsupportedScopeError(env, scope)

    skill_md_text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    meta, body = _parse_frontmatter(skill_md_text)

    common: Dict[str, Any] = {
        "skill_name": skill_name,
        "env": env,
        "scope": scope,
        "skill_dir": skill_dir,
        "skill_md_text": skill_md_text,
        "description": meta.get("description", ""),
        "body": body,
    }

    root = pathlib.Path.cwd() if scope == "local" else pathlib.Path.home()

    if env == "claude":
        dest_dir = root / ".claude" / "skills" / skill_name
        config_file = (
            root / "CLAUDE.md" if scope == "local" else root / ".claude" / "CLAUDE.md"
        )
        config_line = f"@.claude/skills/{skill_name}/SKILL.md"
        return SkillInstallPlan(
            dest_dir=dest_dir,
            config_file=config_file,
            config_line=config_line,
            config_text=(
                f"<!-- You can find the {skill_name} instructions and usage in"
                f" .claude/skills/{skill_name}/SKILL.md -->\n"
                f"{config_line}"
            ),
            actions=[
                f"  Copy skill files to: {dest_dir}",
                f"  Update config file:  {config_file}",
                f"  Add reference:       {config_line}",
            ],
            **common,
        )

    if env == "copilot":
        dest_file = pathlib.Path.cwd() / ".github" / "skills" / skill_name / "SKILL.md"
        return SkillInstallPlan(
            dest_file=dest_file,
            actions=[f"  Write skill file to: {dest_file}"],
            **common,
        )

    if env == "codex":
        dest_dir = root / ".codex" / "skills" / skill_name
        config_file = root / "AGENTS.md"
        section_header = f"## Skill: {skill_name}"
        return SkillInstallPlan(
            dest_dir=dest_dir,
            config_file=config_file,
            section_header=section_header,
            actions=[
                f"  Copy skill files to: {dest_dir}",
                f"  Update config file:  {config_file}",
                f"  Append section:      {section_header}",
            ],
            **common,
        )

    dest_file = root / ".cursor" / "rules" / f"{skill_name}.mdc"
    return SkillInstallPlan(
        dest_file=dest_file,
        actions=[f"  Write skill file to: {dest_file}"],
        **common,
    )


def apply_skill_install(plan: SkillInstallPlan) -> List[str]:
    """Perform the installation described by *plan*.

    Parameters
    ----------
    plan : SkillInstallPlan
        Plan built by :func:`plan_skill_install`.

    Returns
    -------
    list of str
        Human-readable log of what has been written or skipped.

    Raises
    ------
    ValueError
        When *plan* does not hold every path its environment needs.

    Examples
    --------
    >>> from ansys.mapdl.core.cli.skills import apply_skill_install, plan_skill_install
    >>> apply_skill_install(plan_skill_install("pymapdl-cli", "cursor"))
    ['  wrote /home/user/.cursor/rules/pymapdl-cli.mdc']

    """
    if plan.env == "claude":
        if (
            plan.dest_dir is None
            or plan.config_file is None
            or plan.config_line is None
        ):
            raise ValueError(_INCOMPLETE_PLAN_ERROR.format(env=plan.env))

        _copy_skill_files(plan.skill_dir, plan.dest_dir)
        plan.config_file.parent.mkdir(parents=True, exist_ok=True)
        if _append_if_missing(plan.config_file, plan.config_line, plan.config_text):
            return [f"  updated {plan.config_file}"]
        return [f"  notice: reference already present in {plan.config_file}, skipping."]

    if plan.env == "codex":
        if (
            plan.dest_dir is None
            or plan.config_file is None
            or plan.section_header is None
        ):
            raise ValueError(_INCOMPLETE_PLAN_ERROR.format(env=plan.env))

        _copy_skill_files(plan.skill_dir, plan.dest_dir)
        plan.config_file.parent.mkdir(parents=True, exist_ok=True)
        section = f"\n{plan.section_header}\n\n{plan.body}\n"
        if _append_if_missing(plan.config_file, plan.section_header, section):
            return [f"  updated {plan.config_file}"]
        return [f"  notice: section already present in {plan.config_file}, skipping."]

    if plan.dest_file is None:
        raise ValueError(_INCOMPLETE_PLAN_ERROR.format(env=plan.env))

    if plan.env == "copilot":
        content = plan.skill_md_text
    else:
        content = f"---\ndescription: {plan.description}\n---\n{plan.body}"

    plan.dest_file.parent.mkdir(parents=True, exist_ok=True)
    plan.dest_file.write_text(content, encoding="utf-8")
    return [f"  wrote {plan.dest_file}"]


def install_skill(
    skill_name: str,
    env: str,
    scope: str = "local",
    skills_dir: Optional[pathlib.Path] = None,
) -> List[str]:
    """Install a bundled skill into an AI coding environment.

    All files in the skill directory, except ``evals/`` and ``workspace/``,
    are copied to the target location, and a reference is added to the main
    configuration file of the environment so that the AI tool discovers the
    skill. Running the function twice is safe: existing references are not
    duplicated.

    Parameters
    ----------
    skill_name : str
        Skill identifier, as reported by :func:`list_skills`.
    env : str
        AI coding environment. One of :data:`SUPPORTED_ENVS`.
    scope : str, default: "local"
        Either ``"local"`` to install into the current working directory, or
        ``"global"`` to install into the home directory of the user.
    skills_dir : pathlib.Path, optional
        Directory holding one sub-directory per skill. Defaults to the
        directory bundled with the package.

    Returns
    -------
    list of str
        Human-readable log of what has been written or skipped.

    Raises
    ------
    UnknownSkillError
        When *skill_name* is not bundled with PyMAPDL.
    UnsupportedScopeError
        When *env* does not support *scope*.

    Examples
    --------
    Install the ``pymapdl-cli`` skill for Claude in the current project:

    >>> from ansys.mapdl.core.cli.skills import install_skill
    >>> install_skill("pymapdl-cli", env="claude")
    ['  updated /home/user/project/CLAUDE.md']

    """
    return apply_skill_install(
        plan_skill_install(skill_name, env=env, scope=scope, skills_dir=skills_dir)
    )


def _find_skills_dir() -> pathlib.Path:
    """Find the bundled skills directory.

    Returns
    -------
    pathlib.Path
        Path to the bundled ``skills/`` directory inside the installed package.
    """
    try:
        import importlib.resources

        ref = importlib.resources.files("ansys.mapdl.core.skills")
        return pathlib.Path(str(ref))
    except Exception:
        return pathlib.Path(__file__).parent.parent.parent / "skills"


def _parse_frontmatter(text: str) -> Tuple[Dict[str, str], str]:
    """Parse YAML frontmatter from a markdown string.

    Parameters
    ----------
    text : str
        Full content of a markdown file that may begin with a
        ``---`` frontmatter block.

    Returns
    -------
    tuple[dict, str]
        A two-element tuple of ``(metadata_dict, body_text)``.
        If no frontmatter is found, *metadata_dict* is empty and
        *body_text* is the original *text*.
    """
    m = re.match(r"^---\s*\n(.*?)\n---(.*)$", text, re.DOTALL)
    if not m:
        return {}, text
    fm_block = m.group(1)
    body = m.group(2).lstrip("\n")
    meta = {}
    for line in fm_block.splitlines():
        if ":" in line:
            key, _, val = line.partition(":")
            meta[key.strip()] = val.strip()
    return meta, body


def _copy_skill_files(src_dir: pathlib.Path, dst_dir: pathlib.Path) -> None:
    """Copy all files from *src_dir* to *dst_dir*, excluding ``evals/`` and ``workspace/``.

    Parameters
    ----------
    src_dir : pathlib.Path
        Source skill directory.
    dst_dir : pathlib.Path
        Destination directory (will be created if it does not exist).
    """
    import shutil

    dst_dir.mkdir(parents=True, exist_ok=True)
    for src_file in src_dir.rglob("*"):
        if src_file.is_dir():
            continue
        rel = src_file.relative_to(src_dir)
        if any(part in _EXCLUDED_DIRECTORIES for part in rel.parts):
            continue
        dst_file = dst_dir / rel
        dst_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_file, dst_file)


def _append_if_missing(
    file_path: pathlib.Path, line: str, text: Optional[str] = None
) -> bool:
    """Append *text* to *file_path* if *line* is not already present.

    Parameters
    ----------
    file_path : pathlib.Path
        File to check and potentially update.
    line : str
        Sentinel string used to detect whether the content has already been
        added.  The check is a simple substring search on the file contents.
    text : str, optional
        The full text block to append.  When omitted, *line* itself is
        appended.  Use this to attach a descriptive comment together with the
        reference line while still deduplicating on the reference alone.

    Returns
    -------
    bool
        ``True`` if the text was appended, ``False`` if it was already present.
    """
    existing = file_path.read_text(encoding="utf-8") if file_path.exists() else ""
    if line in existing:
        return False
    payload = text if text is not None else line
    with open(file_path, "a", encoding="utf-8") as fh:
        if existing and not existing.endswith("\n"):
            fh.write("\n")
        fh.write(payload + "\n")
    return True


# ---------------------------------------------------------------------------
# Click wrappers
# ---------------------------------------------------------------------------


@click.group(short_help="Manage and install PyMAPDL AI skills.")
def skills():
    """Manage and install bundled PyMAPDL AI skills.

    Use the sub-commands to list available skills, inspect their content,
    and install them into your AI coding environment.
    """


def _abort_unknown_skill(error: UnknownSkillError) -> None:
    """Report an unknown skill on stderr and exit with a non-zero code.

    Parameters
    ----------
    error : UnknownSkillError
        Error raised while resolving the skill name.
    """
    click.echo(click.style("ERROR:", fg="red") + f" {error}", err=True)
    if error.available:
        click.echo("Available skills: " + ", ".join(error.available), err=True)
    sys.exit(1)


@skills.command(
    name="list",
    short_help="List all bundled skills.",
    help="""List all skills bundled with this PyMAPDL installation.

    Prints each skill's name and a one-line description to stdout.""",
)
def list_skills_cli() -> None:
    """List all skills bundled with this PyMAPDL installation.

    Prints each skill's name and a one-line description to stdout.

    Examples
    --------
    List all bundled skills:

        pymapdl skills list

    """
    entries = list_skills()
    if not entries:
        click.echo("No skills are bundled with this PyMAPDL installation.")
        return

    click.echo("")
    click.echo(click.style("Available skills:", bold=True))
    for skill in entries:
        click.echo(f"- {skill.name}")

    click.echo("")
    for skill in entries:
        click.echo(skill.name)
        click.echo("-" * len(skill.name))
        if skill.description:
            click.echo(skill.description)


@skills.command(
    name="show",
    short_help="Print a skill's SKILL.md to stdout.",
    help="""Print the full content of a skill's SKILL.md to stdout.

SKILL_NAME is the skill identifier as shown by ``pymapdl skills list``
(e.g. ``pymapdl-cli``).  Redirect stdout to capture the file locally:

\b
Example:
    pymapdl skills show pymapdl-cli > SKILL.md
    """,
)
@click.argument("skill_name")
def show_skill_cli(skill_name: str) -> None:
    """Print the full content of a skill's SKILL.md to stdout.

    SKILL_NAME is the skill identifier as shown by ``pymapdl skills list``
    (e.g. ``pymapdl-cli``).  Redirect stdout to capture the file locally:

    Parameters
    ----------
    skill_name : str
        Identifier of the skill to show, as shown by ``pymapdl skills list``
        (e.g. ``pymapdl-cli``).

    Examples
    --------
    Print the SKILL.md for the 'pymapdl-cli' skill to the console:

        pymapdl skills show pymapdl-cli

    Save the SKILL.md for the 'pymapdl-cli' skill to a local file:

        pymapdl skills show pymapdl-cli > SKILL.md

    """
    try:
        click.echo(show_skill(skill_name))
    except UnknownSkillError as err:
        _abort_unknown_skill(err)


@skills.command(
    name="install",
    short_help="Install a skill into an AI environment.",
    help="""Install a skill's files into an AI coding environment.

SKILL_NAME is the skill identifier as shown by ``pymapdl skills list``
(e.g. ``pymapdl-cli``).

All files in the skill directory (except ``evals/``) are copied to
the target location.  A reference line is also appended to the
environment's main configuration file so the AI tool can discover
the skill automatically.  Running twice is safe — existing references
are not duplicated.

Omit ``--yes`` to preview the planned actions before committing.

\b
Examples:

Install the 'pymapdl-cli' skill into the current directory for use with
Copilot:

    pymapdl skills install pymapdl-cli --env copilot

Install the 'pymapdl-cli' skill globally for use with Claude:

    pymapdl skills install pymapdl-cli --env claude --global

    """,
)
@click.argument("skill_name")
@click.option(
    "--env",
    required=True,
    type=click.Choice(SUPPORTED_ENVS),
    help=(
        "AI coding environment to install the skill into.  "
        "Each environment receives a copy of the skill files (excluding "
        "``evals/``) and a reference is added to its main configuration file."
    ),
)
@click.option(
    "--local",
    "scope",
    flag_value="local",
    default=True,
    help="Install into the current working directory (default).",
)
@click.option(
    "--global",
    "scope",
    flag_value="global",
    help="Install into the user's home directory instead of the CWD.",
)
@click.option(
    "--yes",
    "-y",
    is_flag=True,
    default=False,
    help="Skip the confirmation prompt and proceed immediately.",
)
def install_skill_cli(skill_name: str, env: str, scope: str, yes: bool) -> None:
    """Install a skill's files into an AI coding environment.

    SKILL_NAME is the skill identifier as shown by ``pymapdl skills list``
    (e.g. ``pymapdl-cli``).

    All files in the skill directory (except ``evals/``) are copied to
    the target location.  A reference line is also appended to the
    environment's main configuration file so the AI tool can discover
    the skill automatically.  Running twice is safe — existing references
    are not duplicated.

    Parameters
    ----------
    skill_name : str
        Identifier of the skill to install, as shown by ``pymapdl skills list`
        (e.g. ``pymapdl-cli``).
    env : str
        AI coding environment to install the skill into. The available
        environments are: "claude", "copilot", "codex" and "cursor".
        Each environment receives a copy of the skill files
        (excluding ``evals/``) and a reference is added to its main
        configuration file.
    scope : str
        Installation scope.  Use ``--local`` to install into the current working
        directory, or ``--global`` to install into the user's home
        directory instead.  Note that some environments do not support global
        installation. Default is ``--local``.
    yes : bool
        When ``False``, show a preview of the planned file operations and ask for
        confirmation before proceeding.  When ``True``, skip the confirmation
        prompt and proceed immediately. Default is ``False``.

    Examples
    --------
    Install the 'pymapdl-cli' skill into the current directory for use with
    Copilot:

      pymapdl skills install pymapdl-cli --env copilot

    Install the 'pymapdl-cli' skill globally for use with Claude:

      pymapdl skills install pymapdl-cli --env claude --global

    """
    try:
        plan = plan_skill_install(skill_name, env=env, scope=scope)
    except UnknownSkillError as err:
        _abort_unknown_skill(err)
    except UnsupportedScopeError as err:
        click.echo(click.style("ERROR:", fg="red") + f" {err}", err=True)
        sys.exit(1)

    click.echo(f"Installing skill '{skill_name}' for env '{env}' ({scope}):")
    click.echo(plan.summary)

    if not yes:
        click.confirm("Proceed?", default=False, abort=True)

    for message in apply_skill_install(plan):
        click.echo(message)

    click.echo(click.style("Done.", fg="green"))
