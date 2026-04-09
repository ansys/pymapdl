#!/usr/bin/env python3
"""Sync .github/skills/ into src/ansys/mapdl/core/skills/ for packaging.

Run from the repository root:
    python scripts/sync_skills.py
"""

import pathlib
import shutil

REPO_ROOT = pathlib.Path(__file__).parent.parent
SRC = REPO_ROOT / ".github" / "skills"
DST = REPO_ROOT / "src" / "ansys" / "mapdl" / "core" / "skills"


def _should_exclude(path: pathlib.Path) -> bool:
    return any(part == "evals" for part in path.parts)


def sync():
    DST.mkdir(parents=True, exist_ok=True)
    for src_file in SRC.rglob("*"):
        if src_file.is_dir():
            continue
        rel = src_file.relative_to(SRC)
        if _should_exclude(rel):
            continue
        dst_file = DST / rel
        dst_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_file, dst_file)
        print(f"  copied  {rel}")
    print("Done.")


if __name__ == "__main__":
    sync()
