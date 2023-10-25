"""Run some vm manuals"""
from ansys.mapdl.core import launch_mapdl
from ansys.mapdl.core.examples import vmfiles

mapdl = launch_mapdl()

vms = list(vmfiles.keys())

for i, vm in enumerate(vms[:2]):
    mapdl.clear()
    print(f"Running the vm {i}: {vm}")
    output = mapdl.input(vmfiles[vm])
    print(f"Running the vm {i}: Successfully completed")
mapdl.exit()
