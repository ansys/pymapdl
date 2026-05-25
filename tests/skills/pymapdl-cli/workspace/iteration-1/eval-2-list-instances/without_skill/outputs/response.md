# Listing Running MAPDL Instances

Use the `pymapdl list` command with the `-i` flag to show only main instances (filtering out child processes):

```bash
pymapdl list -i
```

This displays a table with **Name**, **Status**, **gRPC port**, and **PID** for each main MAPDL instance owned by your user.

## Other Useful Options

| Flag | Description |
|------|-------------|
| `pymapdl list` | List all MAPDL processes (including child processes) |
| `pymapdl list -i` | Only main instances (≥2 child processes) |
| `pymapdl list -l` | Long format — includes command line and working directory |
| `pymapdl list -c` | Include the full command line |
| `pymapdl list -cwd` | Include the working directory |

## How It Works

Under the hood, PyMAPDL uses `psutil` to scan for processes whose name contains `"ansys"` or `"mapdl"`, verifies they have the `-grpc` flag in their command line, and extracts the port from the `-port` argument. A process is considered a **main instance** if it has 2 or more child processes; otherwise it's classified as a child/sub-process.
