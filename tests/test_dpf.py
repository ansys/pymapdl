# Copyright (C) 2024 ANSYS, Inc. and/or its affiliates.
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

from conftest import HAS_DPF, has_dependency, requires

if not has_dependency("ansys-dpf-core") or not HAS_DPF:
    pytest.skip(allow_module_level=True)

from ansys.dpf import core as dpf
from ansys.dpf.core.server_types import DPF_DEFAULT_PORT

DPF_PORT = os.environ.get("DPF_PORT", DPF_DEFAULT_PORT)  # Set in ci.yaml


@requires("dpf")
@requires("ansys-dpf-core")
def test_dpf_connection():
    # uses 127.0.0.1 and port 50054 by default
    try:
        grpc_con = dpf.connect_to_server(port=DPF_PORT)
        assert grpc_con.live
        assert True
    except OSError:
        assert False


@requires("dpf")
@requires("ansys-dpf-core")
def test_upload(mapdl, solved_box, tmpdir):
    # Download RST file
    rst_path = mapdl.download_result(str(tmpdir.mkdir("tmpdir")))

    # Stabilishing connection
    grpc_con = dpf.connect_to_server(port=DPF_PORT)
    assert grpc_con.live

    # Upload RST
    server_file_path = dpf.upload_file_in_tmp_folder(rst_path)

    # Creating model
    model = dpf.Model(server_file_path)
    assert model.results is not None

    # Checks
    mapdl.allsel()
    assert mapdl.mesh.n_node == model.metadata.meshed_region.nodes.n_nodes
    assert mapdl.mesh.n_elem == model.metadata.meshed_region.elements.n_elements
