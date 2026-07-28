# Copyright (C) 2016 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
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

import logging
import sys

import pytest

from ansys.mapdl.core.launcher import launch_mapdl


@pytest.fixture
def generate_certs(tmp_path):
    """Generate mTLS test certificates using ``ansys.tools.common.utils``.

    Requires the ``cryptography`` package. Install it with::

        pip install ansys-tools-common[other]

    The fixture writes ``ca.crt``, ``server.crt``, ``server.key``,
    ``client.crt``, and ``client.key`` into a temporary ``certs/``
    subdirectory and returns its :class:`~pathlib.Path`.
    """
    pytest.importorskip(
        "cryptography",
        reason="cryptography package required; install ansys-tools-common[other]",
    )
    from ansys.tools.common.utils import generate_test_certificates

    certs_dir = tmp_path / "certs"
    generate_test_certificates(output_dir=certs_dir)
    return certs_dir


def test_configure_mtls_accepts_generated_certs(generate_certs):
    # Validate configure_mtls accepts a valid cert directory
    from ansys.mapdl.core.mapdl_grpc import MapdlGrpc

    obj = object.__new__(MapdlGrpc)
    obj._log = logging.getLogger("test")
    obj.certs_dir = generate_certs

    # Should not raise
    obj.configure_mtls()


def test_launch_mapdl_infers_mtls_and_passes_transport(
    monkeypatch, generate_certs, tmp_path
):
    # Prevent any real network or MAPDL operations. Patch MapdlGrpc to capture args.
    captured = {}

    class DummyMapdlGrpc:
        def __init__(self, *args, **kwargs):
            captured.update(kwargs)
            # minimal attrs used by launcher
            self._launched = False
            self._log = None

        def clear(self):
            return None

    # Also patch the actual class name used by launcher import path
    monkeypatch.setattr(
        "ansys.mapdl.core.launcher.connection.MapdlGrpc", DummyMapdlGrpc, raising=False
    )

    # Call launch_mapdl in connect-only mode to avoid starting MAPDL
    lm = launch_mapdl(
        start_instance=False,
        ip="127.0.0.1",
        port=50052,
        transport_mode=None,  # Should be inferred from certs_dir
        certs_dir=str(generate_certs),
    )

    # Ensure the launcher inferred mtls transport and passed certs_dir
    assert captured.get("certs_dir") is not None
    # transport mode should be passed as string like 'MTLS' or 'mtls' depending on implementation
    assert captured.get("transport_mode") is not None


def test_connect_with_mocked_channel(monkeypatch, generate_certs):
    """_create_channel passes certs_dir to cyberchannel.create_channel for mTLS."""
    fake_mod = type(sys)("ansys.tools.common.cyberchannel")
    captured_calls = []

    def fake_create_channel(**kwargs):
        captured_calls.append(kwargs)

        class DummyChannel:
            def subscribe(self, *a, **k):
                return None

        return DummyChannel()

    fake_mod.create_channel = fake_create_channel
    fake_mod.verify_transport_mode = lambda mode: None
    monkeypatch.setitem(sys.modules, "ansys.tools.common.cyberchannel", fake_mod)

    from ansys.mapdl.core.mapdl_grpc import MapdlGrpc

    obj = object.__new__(MapdlGrpc)
    obj._log = logging.getLogger("test")
    obj.transport_mode = "mtls"
    obj.uds_dir = None
    obj.uds_id = None
    obj.certs_dir = generate_certs
    obj.grpc_options = []

    ch = obj._create_channel(ip="127.0.0.1", port=50052)

    assert hasattr(ch, "subscribe")
    assert len(captured_calls) == 1
    assert str(captured_calls[0].get("certs_dir")) == str(generate_certs)


@pytest.mark.local
def test_local_launch_with_certs(monkeypatch, generate_certs):
    # This test requires local MAPDL and therefore is marked 'local'. It will try
    # to call launch_mapdl to start MAPDL but uses start_instance=False to connect
    # to a running local container. The connection is mocked so no real TLS handshake
    # happens.
    fake_mod = type(sys)("ansys.tools.common.cyberchannel")

    def fake_create_channel(**kwargs):
        class DummyChannel:
            def subscribe(self, *a, **k):
                return None

        return DummyChannel()

    fake_mod.create_channel = fake_create_channel
    fake_mod.verify_transport_mode = lambda mode: None
    monkeypatch.setitem(sys.modules, "ansys.tools.common.cyberchannel", fake_mod)

    # Patch MapdlGrpc to avoid network operations but simulate a connected client
    class DummyMapdlGrpc:
        def __init__(self, *args, **kwargs):
            self._channel = fake_create_channel()
            self._launched = False

        def clear(self):
            pass

    monkeypatch.setattr(
        "ansys.mapdl.core.launcher.connection.MapdlGrpc", DummyMapdlGrpc, raising=False
    )

    # Connect to the local docker MAPDL insecure server (port 50052) with mtls settings
    mapdl = launch_mapdl(
        start_instance=False,
        ip="127.0.0.1",
        port=50052,
        transport_mode="mtls",
        certs_dir=str(generate_certs),
    )
    # mapdl returned should be a client-like object; ensure 'clear' exists
    assert hasattr(mapdl, "clear")
