"""Strip captured output (``sections``) from pytest-reportlog JSONL files.

Each record written by ``pytest --report-log`` may contain a ``sections`` field
holding the captured stdout, stderr and log output of the test. This field can
grow to almost the full size of the report (gigabytes), while the CI consumer
(``.ci/pytest_summary.py``) only needs ``nodeid``, ``outcome``, ``when`` and
``duration``.

This script removes the ``sections`` field from every record in place, keeping
every line and every other field. Lines that are not valid JSON are written
back unchanged so that downstream behaviour on malformed files is preserved.

Usage::

    python .ci/strip_report_sections.py report1.jsonl [report2.jsonl ...]
"""

import argparse
import json
import os


def strip_file(path: str) -> None:
    """Remove the ``sections`` field from each JSON line of ``path`` in place."""
    size_before = os.path.getsize(path)
    tmp_path = f"{path}.tmp"

    # ``newline=""`` and ``surrogateescape`` keep unparsable lines byte-identical,
    # even if they contain invalid UTF-8.
    enc, errs = "utf-8", "surrogateescape"
    with (
        open(path, "r", encoding=enc, errors=errs, newline="") as src,
        open(tmp_path, "w", encoding=enc, errors=errs, newline="") as dst,
    ):
        for line in src:
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                # Keep malformed lines unchanged.
                dst.write(line)
                continue

            if isinstance(record, dict):
                record.pop("sections", None)
            dst.write(json.dumps(record) + "\n")

    os.replace(tmp_path, path)

    size_after = os.path.getsize(path)
    print(f"{path}: {size_before:,} bytes -> {size_after:,} bytes")


def main() -> None:
    """Parse the command line and strip each given report file."""
    parser = argparse.ArgumentParser(
        description="Strip captured output ('sections') from pytest-reportlog files."
    )
    parser.add_argument(
        "paths", nargs="+", help="Path(s) to pytest-reportlog JSONL files."
    )
    args = parser.parse_args()

    for path in args.paths:
        if not os.path.isfile(path):
            print(f"{path}: file not found, skipping.")
            continue
        strip_file(path)


if __name__ == "__main__":
    main()
