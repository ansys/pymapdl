"""Test the DPF implementation"""
from ansys.dpf import core as dpf_core


def test_dpf_connection():
    # uses 127.0.0.1 and port 50054 by default
    try:
        dpf_core.connect_to_server()
        assert True
    except OSError:
        assert False
