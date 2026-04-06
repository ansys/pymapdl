# Full MAPDL Workflow from the Command Line

You can do the entire workflow — launch, model, mesh, constrain, load, solve, shutdown — using only the `pymapdl` CLI. No Python scripting required.

## Step 1: Start MAPDL

```bash
pymapdl start
```

This launches a local MAPDL gRPC instance on the default port (50052). You'll see output confirming the PID and address. If you want a custom port or more CPUs:

```bash
pymapdl start --port 50055 --nproc 4
```

## Step 2: Enter the Preprocessor and Define the Element Type

```bash
pymapdl exec -c /prep7 -c "ET,1,186"
```

- `/prep7` enters the preprocessor.
- `ET,1,186` defines element type 1 as SOLID186 (a 3D 20-node structural solid element).

## Step 3: Define Material Properties

```bash
pymapdl exec -c "MP,EX,1,2.1e11" -c "MP,PRXY,1,0.3"
```

- `MP,EX,1,2.1e11` sets Young's modulus (steel, ~210 GPa).
- `MP,PRXY,1,0.3` sets Poisson's ratio.

## Step 4: Create the Block Geometry

```bash
pymapdl exec -c "BLOCK,0,1,0,1,0,1"
```

This creates a unit cube block from (0,0,0) to (1,1,1).

## Step 5: Mesh the Block

```bash
pymapdl exec -c "ESIZE,0.25" -c "VMESH,ALL"
```

- `ESIZE,0.25` sets the global element edge length to 0.25.
- `VMESH,ALL` meshes all volumes.

## Step 6: Apply Constraints (Fixed Support on One Face)

```bash
pymapdl exec -c "NSEL,S,LOC,X,0" -c "D,ALL,ALL,0" -c "ALLSEL"
```

- `NSEL,S,LOC,X,0` selects all nodes at x = 0 (one face of the cube).
- `D,ALL,ALL,0` applies zero displacement (fixed) on all DOFs for those nodes.
- `ALLSEL` reselects everything so subsequent commands apply to the full model.

## Step 7: Apply Loads (Pressure on the Opposite Face)

```bash
pymapdl exec -c "NSEL,S,LOC,X,1" -c "SF,ALL,PRES,1e6" -c "ALLSEL"
```

- `NSEL,S,LOC,X,1` selects all nodes at x = 1 (the opposite face).
- `SF,ALL,PRES,1e6` applies a surface pressure of 1 MPa.
- `ALLSEL` reselects all entities.

## Step 8: Solve

```bash
pymapdl exec -c /solu -c SOLVE -c FINISH
```

- `/solu` enters the solution processor.
- `SOLVE` runs the analysis.
- `FINISH` exits the solution processor.

## Step 9: Shut Down MAPDL

```bash
pymapdl stop
```

This cleanly terminates the MAPDL instance on the default port. If you started on a custom port, specify it:

```bash
pymapdl stop --port 50055
```

---

## All-in-One (Single Command)

If you prefer to send everything at once, you can chain all the APDL commands in a single `pymapdl exec` call:

```bash
pymapdl exec \
  -c /prep7 \
  -c "ET,1,186" \
  -c "MP,EX,1,2.1e11" \
  -c "MP,PRXY,1,0.3" \
  -c "BLOCK,0,1,0,1,0,1" \
  -c "ESIZE,0.25" \
  -c "VMESH,ALL" \
  -c "NSEL,S,LOC,X,0" \
  -c "D,ALL,ALL,0" \
  -c "ALLSEL" \
  -c "NSEL,S,LOC,X,1" \
  -c "SF,ALL,PRES,1e6" \
  -c "ALLSEL" \
  -c FINISH \
  -c /solu \
  -c SOLVE \
  -c FINISH
```

All `-c` values are joined with newlines and sent as a single block to the solver for maximum performance.

---

## Key Notes

- **State persists between calls.** Since `--clear-on-connect` is off by default, each `pymapdl exec` call builds on the previous one. You don't lose your model between steps.
- **Output goes to stdout**, errors to stderr — so you can pipe or log results easily.
- **No Python needed.** The `pymapdl` CLI wraps PyMAPDL's Python API so you can stay entirely in the terminal.
- **Use `pymapdl list -i`** at any time to see running MAPDL instances and their ports/PIDs.
