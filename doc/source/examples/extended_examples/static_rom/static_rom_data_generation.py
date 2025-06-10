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
Creating training data for a 3D Static reduced order model (ROM)
----------------------------------------------------------------

This example is an extension of the example, :ref:`ref_3d_plane_stress_concentration`.
It shows how a parametric sweep may be run and the output displacement and stress data exported into
the format required to build a Static ROM with Ansys Twin Builder.
"""

import json
from pathlib import Path

from ansys.dpf import core as dpf
import numpy as np
from pytwin import write_binary

from ansys.mapdl.core import Mapdl, launch_mapdl
from ansys.mapdl.core.examples.downloads import download_example_data


def compress_id_list(id_list: np.ndarray):
    """
    Compress array of consecutive IDs.

    Compress array by replacing runs of three or more consecutive integers with ``start, -1, end``.

    Example
    -------
    >>> input = np.array([0, 1, 2, 3, 4, 5, 6, 28, 29, 30, 31, 13, 15, 17, 18, 19, 20])
    >>> compress_id_list(input)
    [0, -1, 6, 28, -1, 31, 13, 15, 17, -1, 20]
    """
    if id_list.size == 0:
        return []

    # Find breaks in consecutive sequences.
    breaks = np.where(np.diff(id_list) != 1)[0]

    # Add endpoints to form run boundaries
    run_starts = np.insert(breaks + 1, 0, 0)
    run_ends = np.append(breaks, len(id_list) - 1)

    result = []
    for start, end in zip(run_starts, run_ends):
        length = end - start + 1
        if length >= 3:
            result.extend([int(id_list[start]), -1, int(id_list[end])])
        else:
            result.extend(id_list[start : end + 1].tolist())
    return result


def write_settings(
    path: str | Path, field: dpf.Field, name: str, is_deformation: bool = False
):
    """Write the settings.json file."""

    if field.component_count == 1 or field.component_count == 3:
        dimensionality = [field.component_count]
        symmetricalDim = False
    elif field.component_count == 6:
        dimensionality = [3, 3]
        symmetricalDim = True
    else:
        raise ValueError(f"Unsupported field dimensionality {field.component_count}")

    settings = {
        "pointsCoordinates": False,
        "ids": compress_id_list(field.scoping.ids),
        "location": "Nodal",
        "unit": field.unit,
        "unitDimension": {},
        "unitFactor": 1.0,
        "name": name,
        "deformation": is_deformation,
        "dimensionality": dimensionality,
        "symmetricalDim": symmetricalDim,
        "namedSelections": {},
    }

    with open(Path(path).joinpath("settings.json"), "w") as fw:
        # Set default to convert Numpy int to int
        json.dump(settings, fw, default=int, indent=4)


def get_scoping(model: dpf.Model):
    """Return scoping of unique node IDs connected to elements in model."""
    op = dpf.operators.scoping.connectivity_ids(
        mesh_scoping=model.metadata.meshed_region.elements.scoping,
        mesh=model.metadata.meshed_region,
        take_mid_nodes=True,
    )
    # Get output data
    connected_nodes_scoping = op.outputs.mesh_scoping()
    # Compress the list to only keep unique IDs
    connected_nodes_scoping.ids = list(set(op.outputs.mesh_scoping().ids))
    return connected_nodes_scoping


def write_points(model: dpf.Model, scoping: dpf.Scoping, output_folder: str | Path):
    """Write points.bin file."""
    nodes = model.metadata.meshed_region.nodes
    scoped_node_indices, _ = nodes.map_scoping(scoping)
    points_coordinates = nodes.coordinates_field.data[scoped_node_indices]
    write_binary(Path(output_folder).joinpath("points.bin"), points_coordinates)


def write_doe_headers(output_folder: str | Path, name: str, parameters: dict):
    """Write blank doe.csv file with headers."""
    with open(Path(output_folder).joinpath("doe.csv"), "w") as fw:
        parameter_headers = ",".join([str(key) for key in parameters.keys()])
        fw.write(f"{name},{parameter_headers}\n")


def write_doe_entry(output_folder: str | Path, snapshot_name: str, parameters: dict):
    """Write entry to doe.csv file."""
    with open(Path(output_folder).joinpath("doe.csv"), "a") as fw:
        parameter_values = ",".join([str(value) for value in parameters.values()])
        fw.write(f"{snapshot_name},{parameter_values}\n")


def export_static_ROM_data(
    model: dpf.Model,
    scoping: dpf.Scoping,
    name: str,
    output_folder: str | Path,
    parameters: dict,
    snap_idx: int = 0,
    new_metadata: bool = False,
):
    # Create the output folder
    output_folder = Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)

    is_deformation = False
    if name == "displacement":
        result = model.results.displacement
        is_deformation = True
    elif name == "stress":
        result = model.results.stress
    else:
        raise ValueError(f"Unsupported result type: {name}")

    # Retrieve displacement and stress at last result set.
    scoped_result = result.on_last_time_freq.on_mesh_scoping(scoping)

    # Result must be sorted by scoping to ensure consistency across outputs.
    sorted_result = dpf.operators.logic.ascending_sort_fc(
        scoped_result, sort_by_scoping=True
    )
    result_field = sorted_result.outputs.fields_container()[0]

    if new_metadata:
        write_points(model, scoping, output_folder)
        write_doe_headers(output_folder, name, parameters)
        write_settings(output_folder, result_field, name, is_deformation=is_deformation)

    # Write snapshots
    snapshot_folder = output_folder.joinpath("snapshots")
    snapshot_folder.mkdir(parents=True, exist_ok=True)
    snap_name = f"file{snap_idx}.bin"
    write_doe_entry(output_folder, snap_name, parameters)
    write_binary(snapshot_folder.joinpath(snap_name), result_field.data)


def solve_design_point(mapdl: Mapdl, force_load: float):
    """Solve the MAPDL model."""
    mapdl.run("/SOLU")
    mapdl.cmsel("S", "load_node", "NODE")
    mapdl.fdele("ALL", "FX")
    mapdl.f("ALL", "FX", force_load)
    mapdl.allsel()
    mapdl.antype("STATIC")
    mapdl.solve()
    mapdl.finish(mute=True)
    rst_path = mapdl.result_file
    return rst_path


def run_doe():
    # First, start MAPDL as a service and disable all but error messages.
    mapdl = launch_mapdl(loglevel="ERROR")

    # Download the example database: notch_file is the path to the downloaded file.
    notch_file = download_example_data(
        filename="3d_notch.db", directory="pymapdl/static_ROM_data_generation"
    )

    mapdl.resume(notch_file, mute=True)

    # Define folders for output.
    rom_folder = Path(mapdl.directory).joinpath("Static_ROM")
    for idx, force_load in enumerate([250]):
        # Solve the MAPDL model
        rst_path = solve_design_point(mapdl, force_load)

        # Load the results to DPF and create scoping.
        model = dpf.Model(rst_path)
        scoping = get_scoping(model)

        # Only create points.bin and settings.json on first design point.
        new_metadata = idx == 0

        # Set current parameters and export displacement and stress data.
        parameters = {"force[N]": force_load}
        for name in ["displacement", "stress"]:
            output_folder = rom_folder.joinpath(name)
            export_static_ROM_data(
                model,
                scoping,
                name,
                output_folder,
                parameters=parameters,
                snap_idx=idx,
                new_metadata=new_metadata,
            )
        print(rom_folder)
    mapdl.exit()


if __name__ == "__main__":
    run_doe()
