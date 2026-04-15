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

import pathlib
import re
import sys

import click


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
        return pathlib.Path(__file__).parent.parent / "skills"


def _parse_frontmatter(text: str) -> tuple:
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


def _list_skills(skills_dir: pathlib.Path) -> list:
    """Return a list of ``(name, description, skill_path)`` for every bundled skill.

    Parameters
    ----------
    skills_dir : pathlib.Path
        Root directory that contains one sub-directory per skill.

    Returns
    -------
    list of tuple[str, str, pathlib.Path]
        Each element is ``(name, description, skill_md_path)``.
    """
    result: list[tuple[str, str, pathlib.Path]] = []
    if not skills_dir.exists():
        return result
    for entry in sorted(skills_dir.iterdir()):
        if not entry.is_dir():
            continue
        skill_md = entry / "SKILL.md"
        if not skill_md.exists():
            continue
        text = skill_md.read_text(encoding="utf-8")
        meta, _ = _parse_frontmatter(text)
        name = meta.get("name", entry.name)
        description = meta.get("description", "")
        result.append((name, description, skill_md))
    return result


# ---------------------------------------------------------------------------
# Click command group
# ---------------------------------------------------------------------------


@click.group(short_help="Manage and install PyMAPDL AI skills.")
def skills():
    """Manage and install bundled PyMAPDL AI skills.

    Use the sub-commands to list available skills, inspect their content,
    and install them into your AI coding environment.
    """


# ---------------------------------------------------------------------------
# pymapdl skills list
# ---------------------------------------------------------------------------


@skills.command(name="list", short_help="List all bundled skills.")
def list_skills():
    """List all skills bundled with this PyMAPDL installation.

    Prints each skill's name and a one-line description to stdout.
    """
    skills_dir = _find_skills_dir()
    entries = _list_skills(skills_dir)
    if not entries:
        click.echo("No skills are bundled with this PyMAPDL installation.")
        return
    for name, description, _ in entries:
        click.echo(f"{name}  —  {description}")


# ---------------------------------------------------------------------------
# pymapdl skills show
# ---------------------------------------------------------------------------


@skills.command(name="show", short_help="Print a skill's SKILL.md to stdout.")
@click.argument("skill_name")
def show_skill(skill_name: str) -> None:
    """Print the full content of a skill's SKILL.md to stdout.

    SKILL_NAME is the skill identifier as shown by ``pymapdl skills list``
    (e.g. ``pymapdl-cli``).  Redirect stdout to capture the file locally:

    \b
      pymapdl skills show pymapdl-cli > SKILL.md
    """
    skills_dir = _find_skills_dir()
    skill_md = skills_dir / skill_name / "SKILL.md"
    if not skill_md.exists():
        available = [e[0] for e in _list_skills(skills_dir)]
        click.echo(
            click.style("ERROR:", fg="red") + f" Unknown skill {skill_name!r}. "
            "Run 'pymapdl skills list' to see available skills.",
            err=True,
        )
        if available:
            click.echo("Available skills: " + ", ".join(available), err=True)
        sys.exit(1)
    click.echo(skill_md.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# pymapdl skills install
# ---------------------------------------------------------------------------

_SUPPORTED_ENVS = ("claude", "copilot", "github-repo", "codex", "cursor")
_GLOBAL_UNSUPPORTED = ("copilot", "github-repo")


def _copy_skill_files(src_dir: pathlib.Path, dst_dir: pathlib.Path) -> None:
    """Copy all files from *src_dir* to *dst_dir*, excluding ``evals/``.

    Parameters
    ----------
    src_dir : pathlib.Path
        Source skill directory.
    dst_dir : pathlib.Path
        Destination directory (will be created if it does not exist).
    """
    dst_dir.mkdir(parents=True, exist_ok=True)
    for src_file in src_dir.rglob("*"):
        if src_file.is_dir():
            continue
        rel = src_file.relative_to(src_dir)
        if any(part in ("evals", "workspace") for part in rel.parts):
            continue
        dst_file = dst_dir / rel
        dst_file.parent.mkdir(parents=True, exist_ok=True)
        import shutil

        shutil.copy2(src_file, dst_file)


def _append_if_missing(file_path: pathlib.Path, line: str) -> bool:
    """Append *line* to *file_path* if it is not already present.

    Parameters
    ----------
    file_path : pathlib.Path
        File to check and potentially update.
    line : str
        Line to append (without trailing newline).

    Returns
    -------
    bool
        ``True`` if the line was appended, ``False`` if it was already present.
    """
    existing = file_path.read_text(encoding="utf-8") if file_path.exists() else ""
    if line in existing:
        return False
    with open(file_path, "a", encoding="utf-8") as fh:
        if existing and not existing.endswith("\n"):
            fh.write("\n")
        fh.write(line + "\n")
    return True


@skills.command(name="install", short_help="Install a skill into an AI environment.")
@click.argument("skill_name")
@click.option(
    "--env",
    required=True,
    type=click.Choice(_SUPPORTED_ENVS),
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
def install_skill(skill_name: str, env: str, scope: str, yes: bool) -> None:
    """Install a skill's files into an AI coding environment.

    SKILL_NAME is the skill identifier as shown by ``pymapdl skills list``
    (e.g. ``pymapdl-cli``).

    All files in the skill directory (except ``evals/``) are copied to
    the target location.  A reference line is also appended to the
    environment's main configuration file so the AI tool can discover
    the skill automatically.  Running twice is safe — existing references
    are not duplicated.

    Omit ``--yes`` to preview the planned actions before committing.
    """
    skills_dir = _find_skills_dir()
    skill_dir = skills_dir / skill_name
    if not skill_dir.exists() or not (skill_dir / "SKILL.md").exists():
        available = [e[0] for e in _list_skills(skills_dir)]
        click.echo(
            click.style("ERROR:", fg="red") + f" Unknown skill {skill_name!r}. "
            "Run 'pymapdl skills list' to see available skills.",
            err=True,
        )
        if available:
            click.echo("Available skills: " + ", ".join(available), err=True)
        sys.exit(1)

    if scope == "global" and env in _GLOBAL_UNSUPPORTED:
        click.echo(
            click.style("ERROR:", fg="red")
            + f" --global is not supported for the '{env}' environment.",
            err=True,
        )
        sys.exit(1)

    skill_md_text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    meta, body = _parse_frontmatter(skill_md_text)
    description = meta.get("description", "")

    cwd = pathlib.Path.cwd()
    home = pathlib.Path.home()

    # Resolve destination paths per env + scope
    if env == "claude":
        if scope == "local":
            dest_dir = cwd / ".claude" / "skills" / skill_name
            config_file = cwd / "CLAUDE.md"
        else:
            dest_dir = home / ".claude" / "skills" / skill_name
            config_file = home / ".claude" / "CLAUDE.md"
        config_line = f"@.claude/skills/{skill_name}/SKILL.md"
        action_desc = (
            f"  Copy skill files to: {dest_dir}\n"
            f"  Update config file:  {config_file}\n"
            f"  Add reference:       {config_line}"
        )
    elif env == "copilot":
        dest_file = cwd / ".github" / "instructions" / f"{skill_name}.instructions.md"
        config_file = cwd / ".github" / "copilot-instructions.md"
        config_line = f"@.github/instructions/{skill_name}.instructions.md"
        action_desc = (
            f"  Write skill file to: {dest_file}\n"
            f"  Update config file:  {config_file}\n"
            f"  Add reference:       {config_line}"
        )
    elif env == "github-repo":
        dest_file = cwd / ".github" / "instructions" / f"{skill_name}.instructions.md"
        action_desc = f"  Write skill file to: {dest_file}"
    elif env == "codex":
        if scope == "local":
            dest_dir = cwd / ".codex" / "skills" / skill_name
            config_file = cwd / "AGENTS.md"
        else:
            dest_dir = home / ".codex" / "skills" / skill_name
            config_file = home / "AGENTS.md"
        section_header = f"## Skill: {skill_name}"
        action_desc = (
            f"  Copy skill files to: {dest_dir}\n"
            f"  Update config file:  {config_file}\n"
            f"  Append section:      {section_header}"
        )
    elif env == "cursor":
        if scope == "local":
            dest_file = cwd / ".cursor" / "rules" / f"{skill_name}.mdc"
        else:
            dest_file = home / ".cursor" / "rules" / f"{skill_name}.mdc"
        action_desc = f"  Write skill file to: {dest_file}"

    click.echo(f"Installing skill '{skill_name}' for env '{env}' ({scope}):")
    click.echo(action_desc)

    if not yes:
        click.confirm("Proceed?", default=False, abort=True)

    # Perform the installation
    if env == "claude":
        _copy_skill_files(skill_dir, dest_dir)
        config_file.parent.mkdir(parents=True, exist_ok=True)
        added = _append_if_missing(config_file, config_line)
        if not added:
            click.echo(
                f"  notice: reference already present in {config_file}, skipping."
            )
        else:
            click.echo(f"  updated {config_file}")
        click.echo(click.style("Done.", fg="green"))

    elif env == "copilot":
        dest_file.parent.mkdir(parents=True, exist_ok=True)
        dest_file.write_text(skill_md_text, encoding="utf-8")
        click.echo(f"  wrote {dest_file}")
        config_file.parent.mkdir(parents=True, exist_ok=True)
        added = _append_if_missing(config_file, config_line)
        if not added:
            click.echo(
                f"  notice: reference already present in {config_file}, skipping."
            )
        else:
            click.echo(f"  updated {config_file}")
        click.echo(click.style("Done.", fg="green"))

    elif env == "github-repo":
        dest_file.parent.mkdir(parents=True, exist_ok=True)
        dest_file.write_text(skill_md_text, encoding="utf-8")
        click.echo(f"  wrote {dest_file}")
        click.echo(click.style("Done.", fg="green"))

    elif env == "codex":
        _copy_skill_files(skill_dir, dest_dir)
        config_file.parent.mkdir(parents=True, exist_ok=True)
        section_header = f"## Skill: {skill_name}"
        existing = (
            config_file.read_text(encoding="utf-8") if config_file.exists() else ""
        )
        if section_header in existing:
            click.echo(f"  notice: section already present in {config_file}, skipping.")
        else:
            with open(config_file, "a", encoding="utf-8") as fh:
                if existing and not existing.endswith("\n"):
                    fh.write("\n")
                fh.write(f"\n{section_header}\n\n{body}\n")
            click.echo(f"  updated {config_file}")
        click.echo(click.style("Done.", fg="green"))

    elif env == "cursor":
        mdc_content = f"---\ndescription: {description}\n---\n{body}"
        dest_file.parent.mkdir(parents=True, exist_ok=True)
        dest_file.write_text(mdc_content, encoding="utf-8")
        click.echo(f"  wrote {dest_file}")
        click.echo(click.style("Done.", fg="green"))
