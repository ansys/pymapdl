"""Test the DPF implementation"""
import os

import pytest

from conftest import skip_if_no_has_dpf

try:
    from ansys.dpf import core as dpf
    from ansys.dpf.core.server_types import DPF_DEFAULT_PORT
except ImportError:
    skip_if_no_has_dpf = pytest.mark.skipif(
        True,
        reason="""DPF couldn't be imported.""",
    )
    DPF_DEFAULT_PORT = None


DPF_PORT = os.environ.get("DPF_PORT", DPF_DEFAULT_PORT)  # Set in ci.yaml


@skip_if_no_has_dpf
def test_dpf_connection():
    # uses 127.0.0.1 and port 50054 by default
    try:
        grpc_con = dpf.connect_to_server(port=DPF_PORT)
        assert grpc_con.live
        assert True
    except OSError:
        assert False


@skip_if_no_has_dpf
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
