# Sending an APDL Script to a Running MAPDL Instance

The quickest way from your terminal is a short Python one-liner using PyMAPDL's `Mapdl` class:

```bash
python -c "
from ansys.mapdl.core import Mapdl
mapdl = Mapdl(port=50060)
mapdl.input('thermal_model.inp')
"
```

## Step-by-step explanation

1. **Connect** to the already-running instance on port 50060 using `Mapdl(port=50060)`.
2. **Send the script** with `mapdl.input('thermal_model.inp')` — this reads the `.inp` file and executes every APDL command in it on the remote instance.

## Alternative: interactive Python session

If you want to inspect results afterwards:

```python
from ansys.mapdl.core import Mapdl

mapdl = Mapdl(port=50060)
output = mapdl.input("thermal_model.inp")
print(output)
```

## Environment-variable approach

You can also set environment variables so PyMAPDL connects automatically without launching a new instance:

```bash
# Windows
SET PYMAPDL_START_INSTANCE=False
SET PYMAPDL_PORT=50060

# Linux / macOS
export PYMAPDL_START_INSTANCE=False
export PYMAPDL_PORT=50060
```

Then in Python, `launch_mapdl()` will connect to the existing instance instead of starting a new one:

```python
from ansys.mapdl.core import launch_mapdl

mapdl = launch_mapdl()  # connects to localhost:50060
mapdl.input("thermal_model.inp")
```

## Notes

- Make sure `thermal_model.inp` is in your current working directory, or provide the full path.
- The `mapdl.input()` method returns the MAPDL output as a string, so you can capture and inspect it.
- If MAPDL is on a remote host, add the `ip` parameter: `Mapdl(ip="192.168.1.100", port=50060)`.
