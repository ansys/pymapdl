# Sending an APDL Script to a Running MAPDL Instance

Use the `pymapdl exec` command with the `--file` and `--port` options:

```bash
pymapdl exec --file thermal_model.inp --port 50060
```

This sends the entire `thermal_model.inp` script to the MAPDL instance already running on port 50060 and prints the solver output to your terminal.

**Key points:**

- `pymapdl exec` connects to an **already running** instance — it never starts a new one.
- `--file` (or `-f`) specifies the APDL script file to send.
- `--port` tells it which gRPC port to connect to (default is 50052, so you must specify 50060 explicitly).
- The solver output goes to **stdout** and errors to **stderr**, so you can pipe or redirect as needed.

**Short form:**

```bash
pymapdl exec -f thermal_model.inp --port 50060
```

**Alternative — pipe via stdin:**

```powershell
# PowerShell
Get-Content thermal_model.inp | pymapdl exec --port 50060 -
```

```bash
# Linux / macOS
cat thermal_model.inp | pymapdl exec --port 50060 -
```
