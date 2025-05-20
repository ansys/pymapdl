import json
import os
from typing import Any, TypedDict

import click
import numpy as np
from numpy.typing import NDArray

BIG_WIDTH = 80
SMALL_WIDTH = 8


class TEST_STATS_TYPE(TypedDict):
    durations: list[str | float]
    n_tests: int


def find_json_files(base_dir: str) -> list[str]:
    """Recursively find all JSON files in subdirectories."""
    json_files: list[str] = []
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".jsonl"):
                json_files.append(os.path.join(root, file))
    return json_files


def read_json_file(file_path: str) -> list[dict[str, str]]:
    """Read a JSON file and return its content as a list of test configurations."""
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            data = [json.loads(line) for line in f]
            return data
        except json.JSONDecodeError as e:
            print(f"Error reading {file_path}: {e}")
            return []


def extract_tests_with_tags(json_files: list[str]) -> list[dict[str, str | list[str]]]:
    """Extract test data and assign a tag based on the directory name."""
    tests: list[dict[str, str | list[str]]] = []

    for file_path in json_files:
        directory_name = os.path.basename(os.path.dirname(file_path))
        test_data = read_json_file(file_path)

        for test in test_data:
            if test.get("outcome", "").lower() == "passed" and test.get("duration"):
                nodeid: str = test.get("nodeid", "")

                if nodeid.startswith("tests/"):
                    nodeid = nodeid[6:]

                when: str = test.get("when", "")
                duration: str = test["duration"]
                tags: list[str] = directory_name.split("-")

                if "logs" in tags:
                    tags.remove("logs")

                id_ = f"{nodeid}({when})"

                tests.append(
                    {
                        "tags": tags,
                        "id": id_,
                        "nodeid": nodeid,
                        "duration": duration,
                        "when": when,
                    }
                )
    return tests


def compute_statistics(
    tests: list[dict[str, str | list[str]]],
) -> list[dict[str, str | float]]:
    """Compute average duration and standard deviation per test ID."""
    test_stats: dict[str, TEST_STATS_TYPE] = {}

    for test in tests:
        test_id: str = test["id"]
        if test_id not in test_stats:
            test_stats[test_id] = {
                "durations": [],
                "n_tests": 0,
            }

        test_stats[test_id]["durations"].append(test["duration"])
        test_stats[test_id]["n_tests"] += 1

    summary: list[dict[str, Any]] = []

    for test_id, data in test_stats.items():
        durations: NDArray[Any] = np.array(data["durations"])

        if durations.size == 0:
            continue

        avg_duration = np.mean(durations)
        std_dev = np.std(durations)

        mask_99 = durations < np.percentile(durations, 99)
        if mask_99.sum() == 0:
            avg_duration_minus_one = np.nan
            std_dev_minus_one = np.nan
        else:
            avg_duration_minus_one = np.mean(durations[mask_99])
            std_dev_minus_one = np.std(durations[mask_99])

        mask_75 = durations < np.percentile(durations, 75)
        if mask_75.sum() == 0:
            avg_duration_minus_34 = np.nan
            std_dev_minus_34 = np.nan
        else:
            avg_duration_minus_34 = np.mean(durations[mask_75])
            std_dev_minus_34 = np.std(durations[mask_75])

        summary.append(
            {
                "id": test_id,
                "n_tests": data["n_tests"],
                "average_duration": avg_duration,
                "std_dev": std_dev,
                "avg_duration_minus_one": avg_duration_minus_one,
                "std_dev_minus_one": std_dev_minus_one,
                "avg_duration_minus_34": avg_duration_minus_34,
                "std_dev_minus_34": std_dev_minus_34,
            }
        )

    return summary


def print_table(
    data: list[dict[str, str | float]],
    keys: list[str],
    headers: list[str],
    title: str = "",
):
    JUNCTION = "|"

    def make_bold(s: str) -> str:
        return click.style(s, bold=True)

    h = [headers[0].ljust(BIG_WIDTH)]
    h.extend([each.center(SMALL_WIDTH)[:SMALL_WIDTH] for each in headers[1:]])

    len_h = len("| " + " | ".join(h) + " |")

    sep = (
        f"{JUNCTION}-"
        + f"-{JUNCTION}-".join(["-" * len(each) for each in h])
        + f"-{JUNCTION}"
    )
    # top_sep: str = f"{JUNCTION}" + "-" * (len_h - 2) + f"{JUNCTION}"

    if title:
        # click.echo(top_sep)
        click.echo(
            "| " + make_bold(f"Top {len(data)} {title}".center(len_h - 4)) + " |"
        )
        click.echo(sep)

    click.echo("| " + " | ".join([make_bold(each) for each in h]) + " |")
    click.echo(sep)

    for test in data:
        s: list[str] = []
        for i, each_key in enumerate(keys):

            if i == 0:
                id_: str = test[each_key]

                id_ = (
                    id_.replace("(", r"(")
                    .replace(")", r")")
                    .replace("[", r"[")
                    .replace("]", r"]")
                )
                if len(id_) >= BIG_WIDTH:
                    id_ = id_[: BIG_WIDTH - 15] + "..." + id_[-12:]

                s.append(f"{id_}".ljust(BIG_WIDTH)[0:BIG_WIDTH])

            elif each_key == "n_tests":
                s.append(f"{int(test[each_key])}".center(SMALL_WIDTH))
            else:
                if np.isnan(test[each_key]):
                    s.append("N/A".center(SMALL_WIDTH))
                else:
                    s.append(f"{test[each_key]:.4f}".center(SMALL_WIDTH))

        click.echo("| " + " | ".join(s) + " |")
    # click.echo(sep)


def print_summary(summary: list[dict[str, str | float]], num: int = 10):
    """Print the top N longest tests and the top N most variable tests."""
    longest_tests = sorted(summary, key=lambda x: -x["average_duration"])[:num]
    most_variable_tests = sorted(summary, key=lambda x: -x["std_dev"])[:num]

    print(f"\n## Top {num} Longest Running Tests\n")
    print_table(
        longest_tests,
        ["id", "n_tests", "average_duration", "std_dev"],
        ["Test ID", "N. tests", "Avg", "STD"],
        # "Longest Running Tests",
    )

    print("")
    print(f"\n## Top {num} Most Variable Running Tests\n")
    print_table(
        most_variable_tests,
        [
            "id",
            "n_tests",
            "std_dev",
            "average_duration",
            "std_dev_minus_one",
            "avg_duration_minus_one",
            "std_dev_minus_34",
            "avg_duration_minus_34",
        ],
        [
            "Test ID",
            "N. tests",
            "Std",
            "Avg",
            "Std-99%",
            "Avg-99%",
            "Std-75%",
            "Avg-75%",
        ],
        # "Most Variable Running Tests",
    )


@click.command()
@click.option(
    "--directory",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    default=None,
)
@click.option(
    "--num",
    type=int,
    default=10,
    help="Number of top tests to display.",
    show_default=True,
)
@click.option(
    "--save-file",
    default=None,
    type=click.Path(exists=False, dir_okay=False),
    help="File to save the test durations. Default 'tests_durations.json'.",
    show_default=True,
)
def analyze_tests(directory: str, num: int, save_file: str):
    directory = directory or os.getcwd()  # Change this to your base directory
    json_files = find_json_files(directory)
    tests = extract_tests_with_tags(json_files)

    if save_file:
        with open(save_file, "a+") as f:
            for each_line in tests:
                json.dump(each_line, f, indent=2)

    summary = compute_statistics(tests)
    print_summary(summary, num=num)


if __name__ == "__main__":
    analyze_tests()
