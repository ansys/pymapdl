# Copyright (C) 2016 - 2026 ANSYS, Inc. and/or its affiliates.
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

This example shows how to run a parametric sweep on a MAPDL model and export the output displacement
and stress data into the format required to build a static ROM with Ansys Twin Builder.
"""

import csv
import json
from pathlib import Path
import tempfile

from ansys.dpf import core as dpf
import numpy as np
from pytwin import write_binary

from ansys.mapdl.core import launch_mapdl
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
    """Write the ``settings.json`` file."""

    if field.component_count in [1, 3]:
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
    connected_nodes_scoping.ids = sorted(list(set(connected_nodes_scoping.ids)))
    return connected_nodes_scoping


def write_points(model: dpf.Model, scoping: dpf.Scoping, output_folder: str | Path):
    """Write the ``points.bin`` file."""
    nodes = model.metadata.meshed_region.nodes
    scoped_node_indices, _ = nodes.map_scoping(scoping)
    points_coordinates = nodes.coordinates_field.data[scoped_node_indices]
    write_binary(Path(output_folder).joinpath("points.bin"), points_coordinates)


def write_doe_headers(output_folder: str | Path, name: str, parameters: dict):
    """Write a blank ``doe.csv`` file with headers."""
    with open(Path(output_folder).joinpath("doe.csv"), "w", newline="") as fw:
        writer = csv.writer(fw)
        writer.writerow([name] + list(parameters.keys()))


def write_doe_entry(output_folder: str | Path, snapshot_name: str, parameters: dict):
    """Write an entry to the ``doe.csv`` file."""
    with open(Path(output_folder).joinpath("doe.csv"), "a", newline="") as fw:
        writer = csv.writer(fw)
        writer.writerow([snapshot_name] + list(parameters.values()))


def export_static_ROM_variation(
    model: dpf.Model,
    scoping: dpf.Scoping,
    name: str,
    output_folder: str | Path,
    parameters: dict,
    snap_idx: int = 0,
    new_metadata: bool = False,
):
    """
    Export static ROM data for one parameter variation.

    Parameters
    ----------
    model : dpf.Model
        DPF model with results data loaded.
    scoping : dpf.Scoping
        DPF nodal scoping for result export.
    name : str
        Result quantity to export. Options are ``displacement`` and ``stress``.
    output_folder : str|Path
        Folder to store exported data in. Use separate folders for each physics type.
    parameters : dict
        Dictionary of name-value pairs for the input parameters used to generate the current
        results.
    snap_idx : int, default = 0
        Unique ID for the current results.
    new_metadata : bool, default = False
        Whether to trigger the creation of the following files for a given
        data generation run, overwriting any existing ones:  ``points.bin``,
        ``settings.json``, and ``doe.csv``.
    """
    # Create the output folder
    output_folder = Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)

    # Modify this section to export additional result types
    is_deformation = False
    if name == "displacement":
        result = model.results.displacement
        is_deformation = True
    elif name == "stress":
        result = model.results.stress
    else:
        raise ValueError(f"Unsupported result type: {name}")

    # Retrieve displacement and stress at last result set
    scoped_result = result.on_last_time_freq.on_mesh_scoping(scoping)

    # Result must be sorted by scoping to ensure consistency across outputs
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


def export_static_ROM_data(
    mapdl_results: list[tuple[str, dict]], output_folder: str | Path
):
    """
    Export static ROM data to output folder.

    Parameters
    ----------
    mapdl_results: list[tuple[str, dict]]
        List of tuples of the MAPDL result file path and the parameter values for each variation
        solved.
    output_folder: str|Path
        Path to the folder to store ROM output data in.
    """
    for idx, (rst_path, parameters) in enumerate(mapdl_results):
        # Load the results to DPF and create scoping.
        model = dpf.Model(rst_path)
        scoping = get_scoping(model)

        # Only create 'points.bin' and 'settings.json' files on first design point
        new_metadata = idx == 0

        # Export displacement and stress data
        for name in ["displacement", "stress"]:
            data_folder = Path(output_folder).joinpath(name)
            export_static_ROM_variation(
                model,
                scoping,
                name,
                data_folder,
                parameters=parameters,
                snap_idx=idx,
                new_metadata=new_metadata,
            )


def run_mapdl_variations():
    """
    Run the MAPDL model parametric variations.

    Returns
    -------
    list[tuple[str, dict]]
        List of tuples of the MAPDL result file path (on the platform where MAPDL was executed) and
        the parameter values for each variation solved.
    """
    # Specify the force load variations
    forces = [250, 500, 750, 1000]

    # Start MAPDL and disable all but error messages
    mapdl = launch_mapdl(loglevel="ERROR")

    # Download the example database
    notch_file = download_example_data(
        filename="3d_notch.db", directory="pymapdl/static_ROM_data_generation"
    )

    mapdl.resume(notch_file, mute=True)

    # Initialize the outputs
    outputs = []

    # Solve the parameter variations
    for idx, force_load in enumerate(forces):
        # Rename the job, change log, and error log files
        mapdl.filname(f"variation_{idx}")
        mapdl.run("/SOLU")
        mapdl.cmsel("S", "load_node", "NODE")
        mapdl.fdele("ALL", "FX")
        mapdl.f("ALL", "FX", force_load)
        mapdl.allsel()
        mapdl.antype("STATIC")
        mapdl.solve()
        mapdl.finish(mute=True)
        rst_path = mapdl.result_file
        outputs.append((rst_path, {"force[N]": force_load}))
    print(f"MAPDL run in: {mapdl.directory}")
    mapdl.exit()
    return outputs


def run():
    # Define a folder for output
    rom_folder = Path(tempfile.gettempdir()).joinpath("ansys_pymapdl_Static_ROM")
    mapdl_results = run_mapdl_variations()
    export_static_ROM_data(mapdl_results, rom_folder)
    print(f"ROM data exported to: {rom_folder}")


if __name__ == "__main__":
    run()
