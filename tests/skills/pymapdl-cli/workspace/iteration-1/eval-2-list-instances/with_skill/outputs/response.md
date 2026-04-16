# Running MAPDL Instances

To list only the main MAPDL instances (excluding child processes) with their PID and port, run:

```
pymapdl list -i
```

The `-i` (`--instances`) flag filters out child processes and shows only parent instances.

## Current Output

```
Name    Status    gRPC port    PID
------  --------  -----------  -----
```

**There are no MAPDL instances currently running on your machine.**

## Notes

- If you start a new instance with `pymapdl start`, it will appear in this list.
- For more detail (command line, working directory), add `-l` for the long format: `pymapdl list -i -l`.
