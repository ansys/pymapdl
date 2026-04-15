---
name: pymapdl-cli
description: How to use the PyMAPDL command-line interface to start, stop, list, and execute commands on MAPDL instances from a terminal. Use this skill whenever the user wants to control MAPDL from the command line, run APDL commands via the shell, manage running MAPDL processes, script MAPDL workflows without writing Python, or pipe APDL into a running solver — even if they don't explicitly say "CLI".
---

# PyMAPDL CLI

The `pymapdl` CLI lets you manage MAPDL instances and execute APDL commands
directly from the terminal. It is installed automatically with the
`ansys-mapdl-core` Python package and requires the `click` dependency (included
by default).

A typical session looks like this:

```
pymapdl start                          # launch a solver instance
pymapdl exec -c /prep7 -c "K,1,0,0,0" # send commands to it
pymapdl exec --file model.inp          # or send a whole script
pymapdl stop                           # shut it down
```

All commands print human-readable output to **stdout** and errors to **stderr**.
Exit code is **0** on success, **1** on failure.

## Commands at a glance

| Command | Purpose |
|---------|---------|
| `pymapdl start`   | Launch a new local MAPDL instance |
| `pymapdl stop`    | Kill one or all running instances |
| `pymapdl list`    | Show running MAPDL processes |
| `pymapdl exec`    | Send APDL commands to a running instance |
| `pymapdl convert` | Translate an APDL script to Python |

---

## `pymapdl start`

Launch a new MAPDL gRPC server. Prints the IP, port, and PID on success.

```
pymapdl start [OPTIONS]
```

### Key options

| Option | Default | Description |
|--------|---------|-------------|
| `--port` | 50052 (or `PYMAPDL_PORT`) | gRPC port; first available port at or after this value |
| `--exec_file` | auto-detected | Path to the MAPDL executable |
| `--run_location` | temp dir | Working directory for the MAPDL process |
| `--jobname` | `file` | MAPDL jobname |
| `--nproc` | 2 | Number of processors |
| `--ram` | all available | Fixed memory in MB |
| `--override` | off | Delete stale lock files before starting |
| `--additional_switches` | none | Extra MAPDL command-line switches (e.g. `aa_r` for academic license) |
| `--start_timeout` | 45 | Seconds to wait for the server to become ready |
| `--license_type` | none | License name (e.g. `meba`, `ansys`) or description (e.g. `enterprise`) |
| `--version` | latest | MAPDL version to launch (e.g. `241`, `24.1`) |

**Example — start on a custom port with 4 CPUs:**

```
pymapdl start --port 50055 --nproc 4
# Success: Launched a MAPDL instance (PID=12345) at 127.0.0.1:50055
```

---

## `pymapdl stop`

Stop running MAPDL instances. By default targets port 50052.

```
pymapdl stop [OPTIONS]
```

### Options

| Option | Description |
|--------|-------------|
| `--port PORT` | Stop instances listening on this port |
| `--pid PID` | Stop the process (and its children) with this PID |
| `--all` | Stop every MAPDL instance on the machine |

**Examples:**

```
pymapdl stop                  # stop instance on default port 50052
pymapdl stop --port 50055     # stop instance on port 50055
pymapdl stop --pid 12345      # stop a specific process tree
pymapdl stop --all            # stop all MAPDL processes
```

---

## `pymapdl list`

List MAPDL processes currently running on the machine.

```
pymapdl list [OPTIONS]
```

### Options

| Option | Short | Description |
|--------|-------|-------------|
| `--instances` | `-i` | Show only parent instances (hide child processes) |
| `--long` | `-l` | Show all columns (command line + working directory) |
| `--cmd` | `-c` | Include the command-line column |
| `--location` | `-cwd` | Include the working-directory column |

**Example:**

```
pymapdl list -i
# Name          Status    gRPC port    PID
# ANSYS241.exe  running       50052  41644
```

---

## `pymapdl exec`

Send APDL commands to an **already running** MAPDL instance and print the
solver output. This command never starts a new instance — use `pymapdl start`
first.

```
pymapdl exec [OPTIONS] [-]
```

### Three input modes (mutually exclusive)

1. **Repeated `-c` / `--command`** (recommended for scripting and LLM use):

   ```
   pymapdl exec -c /prep7 -c "BLOCK,0,1,0,1,0,1" -c SAVE
   ```

   Each `-c` value is one APDL command. They are joined with newlines and sent
   as a single `input_strings()` block for maximum performance.

2. **File** with `--file` / `-f`:

   ```
   pymapdl exec --file model.inp
   ```

3. **Stdin** by passing `-` as a positional argument:

   ```bash
   # Linux / macOS
   cat model.inp | pymapdl exec -

   # Windows PowerShell
   Get-Content model.inp | pymapdl exec -
   ```

### Options

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--command` | `-c` | — | APDL command (repeatable) |
| `--file` | `-f` | — | Path to an APDL script file |
| `--port` | — | 50052 (or `PYMAPDL_PORT`) | gRPC port of the target instance |
| `--ip` | — | 127.0.0.1 (or `PYMAPDL_IP`) | IP of the target instance |
| `--timeout` | — | 10 | Connection timeout in seconds |
| `--clear-on-connect` | — | off | Clear MAPDL database before sending commands |

### Behavior notes

- **Successive calls share state.** Because `--clear-on-connect` is off by
  default, you can split a workflow across multiple `pymapdl exec` invocations
  and the model/mesh/results persist between them.
- **Output goes to stdout**, errors to stderr — ideal for piping, logging, or
  LLM consumption.
- **Windows paths are safe.** Backslash sequences like `C:\new\file` are
  preserved verbatim; no mangling occurs.

---

## `pymapdl convert`

Convert an APDL script to a PyMAPDL Python script.

```
pymapdl convert [OPTIONS]
```

### Key options

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--file` | `-f` | stdin | APDL input file |
| `--output` | `-o` | stdout | Output Python file |
| `--macros_as_functions` | `-mf` | True | Convert macros to Python functions |
| `--use_function_names` | `-fn` | True | Use method names (`mapdl.k`) instead of `mapdl.run('K')` |
| `--only_commands` | `-oc` | off | Emit only MAPDL calls (no imports/header/exit) |
| `--add_imports` | `-ai` | True | Add `launch_mapdl()` boilerplate |
| `--comment_solve` | `-cs` | off | Comment out SOLVE / /EOF lines |

**Example:**

```
pymapdl convert -f model.inp -o model.py
```

---

## Environment variables

| Variable | Used by | Purpose |
|----------|---------|---------|
| `PYMAPDL_PORT` | `start`, `exec` | Default gRPC port when `--port` is omitted |
| `PYMAPDL_IP` | `exec` | Default IP when `--ip` is omitted |
| `PYMAPDL_MAPDL_EXEC` | `start` | Path to MAPDL executable |

---

## Common workflows

### Interactive modeling session

```bash
pymapdl start --port 50055
pymapdl exec --port 50055 -c /prep7
pymapdl exec --port 50055 -c "ET,1,186" -c "BLOCK,0,1,0,1,0,1" -c "VMESH,ALL"
pymapdl exec --port 50055 --file boundary_conditions.inp
pymapdl exec --port 50055 -c /solu -c SOLVE
pymapdl stop --port 50055
```

### Run a full script in one shot

```bash
pymapdl start
pymapdl exec --file full_model.inp
pymapdl stop
```

### Pipe commands from another tool

```bash
# Generate APDL dynamically and pipe it in
python generate_mesh.py | pymapdl exec -
```

### Fresh database each time

```bash
pymapdl exec --clear-on-connect -c /prep7 -c "K,1,0,0,0"
```
