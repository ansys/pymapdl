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

"""Test the DPF implementation"""
import os

import pytest

from ansys.mapdl.core.helpers import is_installed
from conftest import HAS_DPF, ON_LOCAL

if is_installed("ansys-dpf-core"):
    from ansys.dpf import core as dpf
    from ansys.dpf.core.server_types import DPF_DEFAULT_PORT

    DPF_PORT = int(os.environ.get("DPF_PORT", DPF_DEFAULT_PORT))  # Set in ci.yaml


@pytest.fixture()
def dpf_server():
    if not HAS_DPF:
        pytest.skip("DPF is not available.", allow_module_level=True)

    if not is_installed("ansys-dpf-core"):
        pytest.skip(f"'ansys-dpf-core' is not available.", allow_module_level=True)

    # Start the DPF server
    if ON_LOCAL:
        # If running locally, start the server
        dpf_server = dpf.start_local_server(port=DPF_PORT)
        assert not dpf_server.info["server_ip"]

    else:
        # If running in a container or remote, connect to the server
        dpf_server = dpf.connect_to_server(port=DPF_PORT)
        assert dpf_server.info["server_ip"]

    return dpf_server


@pytest.fixture()
def model(dpf_server, mapdl, solved_box, tmpdir):
    # Download RST file
    rst_path = mapdl.download_result(str(tmpdir.mkdir("tmpdir")))

    # Upload RST
    if not dpf_server.local_server:
        rst_path = dpf.upload_file_in_tmp_folder(rst_path, server=dpf_server)

    model = dpf.Model(rst_path)
    assert model.results is not None

    return model


def test_metadata_meshed_region(dpf_server, mapdl, model):
    # Checks
    mapdl.allsel()
    assert mapdl.mesh.n_node == model.metadata.meshed_region.nodes.n_nodes
    assert mapdl.mesh.n_elem == model.metadata.meshed_region.elements.n_elements


def test_displacement(model, mapdl):
    results = model.results
    displacements = results.displacement()

    disp_dpf = displacements.outputs.fields_container()[0].data
    disp_mapdl = mapdl.post_processing.nodal_displacement("all")

    assert disp_dpf.max() == disp_mapdl.max()
    assert disp_dpf.min() == disp_mapdl.min()
