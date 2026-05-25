# Full MAPDL Workflow from the Command Line Using PyMAPDL CLI

The `pymapdl` CLI tool is primarily a **management utility** — it can start, stop, and list MAPDL instances, but it is **not** a full interactive APDL command processor. You cannot send arbitrary APDL commands (like `BLOCK`, `VMESH`, `SOLVE`, etc.) directly through the `pymapdl` CLI.

Here's how to accomplish what you want:

---

## Step 1: Start MAPDL with the CLI

```bash
pymapdl start
```

This launches a local MAPDL gRPC instance. You can specify options like:

```bash
pymapdl start --port 50052 --start-timeout 60
```

Use `pymapdl list` to verify it's running:

```bash
pymapdl list
```

---

## Step 2: Run Your APDL Commands

The `pymapdl` CLI **cannot** execute APDL modeling commands directly. You have two options for "no Python scripting":

### Option A: Use a Classic APDL Input File with MAPDL Directly

Create a file called `model.inp` with standard APDL commands:

```apdl
/PREP7
! Define element type and material
ET,1,SOLID185
MP,EX,1,2.1E11        ! Young's modulus (steel, Pa)
MP,PRXY,1,0.3          ! Poisson's ratio

! Create a block (x1,x2, y1,y2, z1,z2)
BLOCK,0,1,0,1,0,1

! Mesh controls and meshing
ESIZE,0.25
VMESH,ALL

FINISH

/SOLU
! Apply constraints - fix one face (area 1)
DA,1,ALL,0

! Apply pressure load on opposite face (area 6)
SFA,6,1,PRES,1E6

! Solve
SOLVE
FINISH

/POST1
! Review results
SET,LAST
PRNSOL,U,SUM          ! Print displacement summary
PRNSOL,S,EQV          ! Print von Mises stress
FINISH
```

Then run it directly through the MAPDL executable (not `pymapdl`):

```bash
ansys251 -b -i model.inp -o model.out
```

> Replace `ansys251` with your installed version (e.g., `ansys242`, `ansys241`). The `-b` flag runs in batch mode.

### Option B: Pipe Commands via PyMAPDL's Python One-Liners

If you specifically want to use `pymapdl` tooling from the CLI without writing a `.py` script file:

```bash
python -c "
from ansys.mapdl.core import launch_mapdl
mapdl = launch_mapdl()
mapdl.prep7()
mapdl.et(1, 'SOLID185')
mapdl.mp('EX', 1, 2.1e11)
mapdl.mp('PRXY', 1, 0.3)
mapdl.block(0, 1, 0, 1, 0, 1)
mapdl.esize(0.25)
mapdl.vmesh('ALL')
mapdl.slashsolu()
mapdl.da(1, 'ALL', 0)
mapdl.sfa(6, 1, 'PRES', 1e6)
mapdl.solve()
mapdl.finish()
mapdl.post1()
mapdl.set('LAST')
print(mapdl.prnsol('U', 'SUM'))
print(mapdl.prnsol('S', 'EQV'))
mapdl.exit()
"
```

---

## Step 3: Stop MAPDL with the CLI

If you started MAPDL using `pymapdl start` in Step 1:

```bash
pymapdl stop
```

Or to stop a specific instance:

```bash
pymapdl stop --port 50052
```

---

## Summary

| Step | Command | Tool |
|---|---|---|
| Start MAPDL | `pymapdl start` | PyMAPDL CLI |
| Model/Solve | `ansys251 -b -i model.inp -o model.out` | Native MAPDL batch |
| Stop MAPDL | `pymapdl stop` | PyMAPDL CLI |

The `pymapdl` CLI handles the **lifecycle** (start/stop/list) of MAPDL instances. For the actual modeling, meshing, solving, and post-processing, you need either:

1. **Classic APDL input files** run via the MAPDL executable in batch mode (true "no Python" approach), or
2. **Python one-liners** using PyMAPDL's Python API from the command line.

There is no `pymapdl solve` or `pymapdl mesh` type of CLI command — the CLI was not designed to be an APDL command relay.
