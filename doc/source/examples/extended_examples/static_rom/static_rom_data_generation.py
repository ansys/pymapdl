# Copyright (C) 2016 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
.. _ref_static_rom_data_generation:

Creating training data for a 3D Static reduced order model (ROM)
----------------------------------------------------------------

This example is an extension of the example, :ref:`ref_3d_plane_stress_concentration`.
It shows how a parametric sweep may be run and the output displacement and stress data exported into
the format required to build a Static ROM with Ansys Twin Builder.

The final data structure for the ROM building is shown in Figure 1.

.. figure:: images/static_ROM_file_structure.png
    :align: center
    :width: 600
    :alt:  Static ROM creation files.
    :figclass: align-center

    **Figure 1: Organization of files and directories for static ROM creation.**

Additional Packages Used
~~~~~~~~~~~~~~~~~~~~~~~~

* `NumPy <https://numpy.org>`_ is used for using NumPy arrays.
* `PyTwin <https://twin.docs.pyansys.com>`_ is used convert result data to binary snapshots.


"""

# Assumes working locally. See :ref:`ref_dpf_basic_example` for other options.
import json
from pathlib import Path

from ansys.dpf import core as dpf
from pytwin import write_binary

from ansys.mapdl.core import launch_mapdl

###############################################################################
# Launch MAPDL
# ~~~~~~~~~~~~
# First, start MAPDL as a service and disable all but error messages.
mapdl = launch_mapdl(loglevel="ERROR")

###############################################################################
# Download and resume the 3D notch database
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# The 3D notch model was generated as shown in
# :ref:`ref_3d_plane_stress_concentration` and a nodal component, 'load_node',
# was created for the node to which the load is applied, using the commands
# below:
#
# .. code-block:: python
#
#     mapdl.nsel("S", "NODE", vmin=single_node, vmax=single_node)
#     mapdl.cm("load_node", "NODE")

# notch_file = download_example_data(
#     filename="3d_notch.db", directory="pymapdl/notch"
# )
notch_file = Path.cwd().joinpath(r"src\ansys\mapdl\core\examples\3d_notch.db")
mapdl.resume(notch_file, mute=True)

force_load = 500
mapdl.run("/SOLU")
mapdl.cmsel("S", "load_node", "NODE")
mapdl.fdele("ALL", "FX")
mapdl.f("ALL", "FX", force_load)
mapdl.allsel()
mapdl.antype("STATIC")
mapdl.solve()
mapdl.finish(mute=True)

###############################################################################
# from basic DPF exampl
rst_path = mapdl.result_file

model = dpf.Model(rst_path)
dpf.operators.result.stress()


results = model.results

# Ensure displacement scoping and stress scoping are the same by only taking nodes connected to
# elements.
op = dpf.operators.scoping.connectivity_ids(
    mesh_scoping=model.metadata.meshed_region.elements.scoping,
    mesh=model.metadata.meshed_region,
    take_mid_nodes=True,
)
# Get output data
connected_nodes_scoping = op.outputs.mesh_scoping()

# Compress the list to only keep unique IDs
connected_nodes_scoping.ids = sorted(list(set(op.outputs.mesh_scoping().ids)))

# To retrieve displacement and stress at last result set, scoped to corner nodes.
displacement = results.displacement.on_last_time_freq.on_mesh_scoping(
    connected_nodes_scoping
)
stress = results.stress.on_last_time_freq.on_mesh_scoping(connected_nodes_scoping)
sorted_displacement = dpf.operators.logic.ascending_sort_fc(
    displacement, sort_by_scoping=True
)
sorted_stress = dpf.operators.logic.ascending_sort_fc(stress, sort_by_scoping=True)

displacement_field = sorted_displacement.outputs.fields_container()[0]
stress_field = sorted_stress.outputs.fields_container()[0]

nodes = model.metadata.meshed_region.nodes
ind, _ = nodes.map_scoping(connected_nodes_scoping)

# Define folders for output
output_folder = Path(mapdl.directory).joinpath("Static_ROM")

displacement_folder = output_folder.joinpath("displacement")
disp_snap_folder = displacement_folder.joinpath("snapshots")
disp_snap_folder.mkdir(parents=True, exist_ok=True)

stress_folder = output_folder.joinpath("stress")
stress_snap_folder = stress_folder.joinpath("snapshots")
stress_snap_folder.mkdir(parents=True, exist_ok=True)

# Get node locations
nodes = model.metadata.meshed_region.nodes
scoped_node_indices, _ = nodes.map_scoping(connected_nodes_scoping)
points_coordinates = nodes.coordinates_field.data[scoped_node_indices]

# Write points.bin
write_binary(displacement_folder.joinpath("points.bin"), points_coordinates)
write_binary(stress_folder.joinpath("points.bin"), points_coordinates)

# Write doe.csv headers
with open(displacement_folder.joinpath("doe.csv"), "w") as fw:
    fw.write(f"displacement,force[N]\n")
with open(stress_folder.joinpath("doe.csv"), "w") as fw:
    fw.write(f"stress,force[N]\n")

# Write snapshots
snap_idx = 0
snap_file = f"file{snap_idx}.bin"
write_binary(disp_snap_folder.joinpath(snap_file), displacement_field.data)
write_binary(stress_snap_folder.joinpath(snap_file), stress_field.data)

# Write doe.csv entry
with open(displacement_folder.joinpath("doe.csv"), "a") as fw:
    fw.write(f"{snap_file},{force_load}\n")
with open(stress_folder.joinpath("doe.csv"), "a") as fw:
    fw.write(f"{snap_file},{force_load}\n")

# Write settings.json
if displacement_field.component_count == 1 or displacement_field.component_count == 3:
    dimensionality = [displacement_field.component_count]
    symmetricalDim = False
elif displacement_field.component_count == 6:
    dimensionality = [3, 3]
    symmetricalDim = True
else:
    raise ValueError(f"Unsupported dimensionality {displacement_field.component_count}")

displacement_settings = {
    "pointsCoordinates": False,
    "ids": list(connected_nodes_scoping.ids),
    "location": displacement_field.location,
    "unit": displacement_field.unit,
    "unitDimension": {},
    "unitFactor": 1.0,
    "name": "Displacement",
    "deformation": True,
    "dimensionality": dimensionality,
    "symmetricalDim": symmetricalDim,
    "namedSelections": {},
}

with open(displacement_folder.joinpath("settings.json"), "w") as fw:
    # Set default to convert Numpy int to int
    json.dump(displacement_settings, fw, default=int, indent=4)

if stress_field.component_count == 1 or stress_field.component_count == 3:
    dimensionality = [stress_field.component_count]
    symmetricalDim = False
elif stress_field.component_count == 6:
    dimensionality = [3, 3]
    symmetricalDim = True
else:
    raise ValueError(f"Unsupported dimensionality {stress_field.component_count}")

stress_settings = {
    "pointsCoordinates": False,
    "ids": list(connected_nodes_scoping.ids),
    "location": stress_field.location,
    "unit": stress_field.unit,
    "unitDimension": {},
    "unitFactor": 1.0,
    "name": "Stress",
    "deformation": False,
    "dimensionality": dimensionality,
    "symmetricalDim": symmetricalDim,
    "namedSelections": {},
}

with open(stress_folder.joinpath("settings.json"), "w") as fw:
    # Set default to convert Numpy int to int
    json.dump(stress_settings, fw, default=int, indent=4)
