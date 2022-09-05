"""Test the DPF implementation"""
import os

from ansys.dpf import core as dpf_core

DPF_PORT = os.environ.get("DPF_PORT", 21002)


def test_dpf_connection():
    # uses 127.0.0.1 and port 50054 by default
    try:
        grpc_con = dpf_core.connect_to_server(port=DPF_PORT)
        assert grpc_con.live
        assert True
    except OSError:
        assert False
