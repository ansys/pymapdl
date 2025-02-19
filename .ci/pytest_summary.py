import json
import os

import numpy as np

BIG_WIDTH = 75
SMALL_WIDTH = 12


def find_json_files(base_dir):
    """Recursively find all JSON files in subdirectories."""
    json_files = []
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".jsonl"):
                json_files.append(os.path.join(root, file))
    return json_files


def read_json_file(file_path):
    """Read a JSON file and return its content as a list of test configurations."""
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            data = [json.loads(line) for line in f]
            return data
        except json.JSONDecodeError as e:
            print(f"Error reading {file_path}: {e}")
            return []


def extract_tests_with_tags(json_files):
    """Extract test data and assign a tag based on the directory name."""
    tests = []

    for file_path in json_files:
        directory_name = os.path.basename(os.path.dirname(file_path))
        test_data = read_json_file(file_path)

        for test in test_data:
            if test.get("outcome", "").lower() == "passed" and test.get("duration"):
                nodeid = test.get("nodeid")
                when = test.get("when")
                duration = test["duration"]
                tags = directory_name.split("-")
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


def compute_statistics(tests):
    """Compute average duration and standard deviation per test ID."""
    test_stats = {}

    for test in tests:
        test_id = test["id"]
        if test_id not in test_stats:
            test_stats[test_id] = {
                "durations": [],
                "n_tests": 0,
            }

        test_stats[test_id]["durations"].append(test["duration"])
        test_stats[test_id]["n_tests"] += 1

    summary = []

    for test_id, data in test_stats.items():
        durations = np.array(data["durations"])

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


def print_table(data, keys, headers, title=""):
    h = [headers[0].ljust(BIG_WIDTH)]
    h.extend([each.center(SMALL_WIDTH)[:SMALL_WIDTH] for each in headers[1:]])

    len_h = len("| " + " | ".join(h) + " |")

    sep = "+-" + "-+-".join(["-" * len(each) for each in h]) + "-+"
    top_sep = "+" + "-" * (len_h - 2) + "+"

    if title:
        print("\n" + top_sep)
        print("| " + f"Top {len(data)} {title}".center(len_h - 4) + " |")
        print(sep)

    print("| " + " | ".join(h) + " |")
    print(sep)

    for test in data:
        s = []
        for i, each_key in enumerate(keys):

            if i == 0:
                s.append(f"{test[each_key]}".ljust(BIG_WIDTH)[0:BIG_WIDTH])
            elif each_key == "n_tests":
                s.append(f"{int(test[each_key])}".center(SMALL_WIDTH))
            else:
                if np.isnan(test[each_key]):
                    s.append("N/A".center(SMALL_WIDTH))
                else:
                    s.append(f"{test[each_key]:.4f}".center(SMALL_WIDTH))

        print("| " + " | ".join(s) + " |")
    print(sep)


def print_summary(summary, num=10):
    """Print the top N longest tests and the top N most variable tests."""
    longest_tests = sorted(summary, key=lambda x: -x["average_duration"])[:num]
    most_variable_tests = sorted(summary, key=lambda x: -x["std_dev"])[:num]

    print_table(
        longest_tests,
        ["id", "n_tests", "average_duration", "std_dev"],
        ["Test ID", "N. tests", "Avg Duration", "STD"],
        "Longest Running Tests",
    )

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
            "Std (99%)",
            "Avg (99%)",
            "Std (75%)",
            "Avg (75%)",
        ],
        "Most Variable Running Tests",
    )


if __name__ == "__main__":
    base_directory = os.getcwd()  # Change this to your base directory
    json_files = find_json_files(base_directory)
    tests = extract_tests_with_tags(json_files)

    with open("tests_durations.json", "a+") as f:
        for each_line in tests:
            json.dump(each_line, f, indent=2)

    summary = compute_statistics(tests)
    print_summary(summary, num=50)
