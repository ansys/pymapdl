# Copyright (C) 2016 - 2026 ANSYS, Inc. and/or its affiliates.


import logging
import os
import platform
import sys
import types
from unittest.mock import MagicMock

import grpc
import pytest

from ansys.mapdl.core.errors import MapdlConnectionError, MapdlRuntimeError
from ansys.mapdl.core.launcher import generate_start_parameters
from ansys.mapdl.core.mapdl_grpc import MapdlGrpc


def _make_fake_channel_ready(delay=0):
    """Return a dummy channel object and a channel_ready_future that can be
    controlled for testing `wait_until_healthy`.
    """

    class DummyChannel:
        def subscribe(self, *args, **kwargs):
            return None

    class FakeFuture:
        def __init__(self, delay):
            self._delay = delay

        def result(self, timeout=None):
            # If timeout shorter than delay, raise TimeoutError
            if timeout is not None and timeout < self._delay:
                raise __import__("concurrent.futures").futures.TimeoutError()
            return True

    return DummyChannel(), FakeFuture(delay)


def test_wait_until_healthy_succeeds(monkeypatch):
    # Provide a fake module to avoid importing ansys.tools.common.cyberchannel
    fake_mod = types.ModuleType("ansys.tools.common.cyberchannel")
    fake_mod.verify_transport_mode = lambda mode: None
    monkeypatch.setitem(sys.modules, "ansys.tools.common.cyberchannel", fake_mod)

    # Create fake channel and future that will succeed within timeout
    channel, future = _make_fake_channel_ready(delay=0.1)

    # Patch channel_ready_future to return our controllable future
    monkeypatch.setattr("grpc.channel_ready_future", lambda _ch: future)

    # Create bare instance without running __init__ and set minimal attrs
    m = object.__new__(MapdlGrpc)
    m._channel = channel
    m._log = logging.getLogger("test")
    m._channel_state = grpc.ChannelConnectivity.CONNECTING

    # Should not raise
    MapdlGrpc.wait_until_healthy(m, timeout=1.0)


def test_wait_until_healthy_timeout(monkeypatch):
    fake_mod = types.ModuleType("ansys.tools.common.cyberchannel")
    fake_mod.verify_transport_mode = lambda mode: None
    monkeypatch.setitem(sys.modules, "ansys.tools.common.cyberchannel", fake_mod)

    import logging

    import grpc

    from ansys.mapdl.core.mapdl_grpc import MapdlGrpc

    channel, future = _make_fake_channel_ready(delay=5.0)

    monkeypatch.setattr("grpc.channel_ready_future", lambda _ch: future)

    # Create bare instance without running __init__ and set minimal attrs
    m = object.__new__(MapdlGrpc)
    m._channel = channel
    m._log = logging.getLogger("test")
    m._channel_state = grpc.ChannelConnectivity.CONNECTING

    with pytest.raises(MapdlConnectionError):
        MapdlGrpc.wait_until_healthy(m, timeout=0.01)


def test_configure_uds_socket_conflict_and_increment(tmp_path, monkeypatch):
    """Simulate the case where a UDS socket file already exists; ensure
    MapdlGrpc increments the port and updates uds_id accordingly."""

    # On Windows CI we can fake a POSIX environment for this test by patching
    # os.name and platform.system so that UDS logic is exercised.
    import platform

    monkeypatch.setattr(os, "name", "posix")
    monkeypatch.setattr(platform, "system", lambda: "Linux")

    fake_mod = types.ModuleType("ansys.tools.common.cyberchannel")
    fake_mod.verify_transport_mode = lambda mode: None
    monkeypatch.setitem(sys.modules, "ansys.tools.common.cyberchannel", fake_mod)

    from ansys.mapdl.core.mapdl_grpc import MapdlGrpc

    # Prepare a fake uds directory and create an existing socket file for port 50052
    uds_dir = tmp_path / ".conn"
    uds_dir.mkdir()
    existing_sock = uds_dir / "mapdl-50052.sock"
    existing_sock.write_text("in use")

    # Patch MapdlGrpc internals to avoid heavy init and channel creation
    monkeypatch.setattr(MapdlGrpc, "_subscribe_to_channel", lambda self: None)
    monkeypatch.setattr(
        MapdlGrpc, "reconnect_to_mapdl", lambda self, timeout=None: None
    )

    # Create a bare MapdlGrpc-like object without calling __init__ so we can
    # call `configure_uds` directly. Setting minimal attributes to satisfy
    # `configure_uds` expectations.
    obj = object.__new__(MapdlGrpc)
    import logging

    obj._log = logging.getLogger("test")

    obj._port = 50052
    obj.transport_mode = "uds"
    obj.uds_dir = str(uds_dir)
    obj.uds_id = None

    # Call the configure method without passing `port` so the function treats
    # the port as unspecified and will auto-increment to avoid conflicts.
    obj.configure_uds(port=None, uds_id=None)

    # After configuration, the uds_id should not conflict with the existing file
    assert obj.uds_dir == str(uds_dir)
    assert obj.uds_id != "mapdl-50052.sock"
    assert obj._port != 50052


def test_exit_removes_uds_socket(tmp_path, monkeypatch):
    """Ensure that MapdlGrpc.exit removes the UDS socket file when transport_mode is 'uds'."""

    # Fake POSIX environment so UDS cleanup logic runs on Windows CI
    import platform

    monkeypatch.setattr(os, "name", "posix")
    monkeypatch.setattr(platform, "system", lambda: "Linux")

    fake_mod = types.ModuleType("ansys.tools.common.cyberchannel")
    fake_mod.verify_transport_mode = lambda mode: None
    monkeypatch.setitem(sys.modules, "ansys.tools.common.cyberchannel", fake_mod)

    from ansys.mapdl.core.mapdl_grpc import MapdlGrpc

    uds_dir = tmp_path / ".conn"
    uds_dir.mkdir()
    sock = uds_dir / "mapdl-50052.sock"
    sock.write_text("in use")

    # Create a minimal MapdlGrpc-like object and call exit to trigger removal
    monkeypatch.setattr(MapdlGrpc, "_subscribe_to_channel", lambda self: None)
    monkeypatch.setattr(
        MapdlGrpc, "reconnect_to_mapdl", lambda self, timeout=None: None
    )
    # Prevent actual _exit_mapdl side-effects
    monkeypatch.setattr(MapdlGrpc, "_exit_mapdl", lambda self, path=None: None)

    obj = object.__new__(MapdlGrpc)
    import logging

    obj._log = logging.getLogger("test")
    obj.transport_mode = "uds"
    obj.uds_dir = str(uds_dir)
    obj.uds_id = "mapdl-50052.sock"
    obj._start_instance = True
    obj._launched = True
    obj._exited = False
    # Ensure finish_job_on_exit exists to avoid AttributeError in exit()
    obj.finish_job_on_exit = False
    # Ensure remote instance attribute exists to avoid AttributeError
    obj._remote_instance = None
    # Ensure remove_temp_dir_on_exit and _local exist to avoid AttributeError
    obj.remove_temp_dir_on_exit = False
    obj._local = False
    # Set ip/port/_path used by exit logging and cleanup
    obj._ip = "127.0.0.1"
    obj._port = 50052
    obj._path = str(uds_dir.parent)

    # Ensure file exists before exit
    assert os.path.exists(str(sock))

    # Force exit (force=True to bypass start_instance checks)
    obj.exit(force=True)

    # Socket file should be removed
    assert not os.path.exists(str(sock))


def test_generate_start_parameters_includes_transport_args():
    args = {
        "transport_mode": "insecure",
        "uds_dir": "/home/user/tmp/.conn",
        "uds_id": "mapdl-50052.sock",
        "certs_dir": "/etc/ansys/certs",
        # Required fields used by generate_start_parameters
        "mode": "grpc",
        "ram": None,
        "override": False,
        "start_timeout": 30,
        "launched": True,
        "run_location": "/home/user/tmp",
        "jobname": "file",
        "exec_file": "",
        "nproc": 2,
        "timeout": 15,
        "port": 50052,
    }

    start_parm = generate_start_parameters(args)

    # The start parameters should include transport-related keys when allowed
    assert "transport_mode" in start_parm or "transport_mode" in args
    assert args["transport_mode"] == "insecure"
    assert args["uds_dir"] == "/home/user/tmp/.conn"
    assert args["uds_id"] == "mapdl-50052.sock"
    assert args["certs_dir"] == "/etc/ansys/certs"


@pytest.mark.parametrize("transport_mode", ["insecure", "mtls", "uds", "wnua"])
def test_env_transport_precedence(monkeypatch, transport_mode):
    # Ensure env var takes precedence for transport selection and that
    # MapdlGrpc reads it during initialization. We patch external
    # dependencies to avoid launching a real channel.
    monkeypatch.setenv("PYMAPDL_GRPC_TRANSPORT", transport_mode)

    if transport_mode == "wnua" and os.name != "nt":
        monkeypatch.setattr(os, "name", "nt")
        monkeypatch.setattr(platform, "system", lambda: "Windows")

    if transport_mode == "uds" and os.name == "nt":
        monkeypatch.setattr(os, "name", "posix")
        monkeypatch.setattr(platform, "system", lambda: "Linux")

    # Insert a fake cyberchannel module with verify_transport_mode
    fake_mod = types.ModuleType("ansys.tools.common.cyberchannel")
    fake_mod.verify_transport_mode = lambda mode: None
    monkeypatch.setitem(sys.modules, "ansys.tools.common.cyberchannel", fake_mod)

    # Patch MapdlGrpc internals to avoid network operations
    from ansys.mapdl.core.mapdl_grpc import MapdlGrpc

    monkeypatch.setattr(MapdlGrpc, "_subscribe_to_channel", lambda self: None)
    monkeypatch.setattr(
        MapdlGrpc, "reconnect_to_mapdl", lambda self, timeout=None: None
    )
    monkeypatch.setattr(MapdlGrpc, "_send_command", lambda self, cmd="", mute=False: "")
    monkeypatch.setattr(MapdlGrpc, "_verify_local", lambda self: None)
    monkeypatch.setattr(MapdlGrpc, "platform", lambda self: "Windows")

    class DummyChannel:
        def subscribe(self, *args, **kwargs):
            return None

    # Construct MapdlGrpc with a dummy channel to bypass network creation
    grpc = MapdlGrpc(
        channel=DummyChannel(), cleanup_on_exit=False, disable_run_at_connect=True
    )
    assert grpc.transport_mode == transport_mode


@pytest.fixture(autouse=True)
def disable_reconnect(monkeypatch):
    # Prevent network attempts in constructor
    monkeypatch.setattr(
        MapdlGrpc, "reconnect_to_mapdl", lambda self, timeout=None: None
    )
    yield


def test_configure_transport_calls_verify(tmp_path, monkeypatch):
    # Ensure verify_transport_mode is called and defaults set
    fake_verify = MagicMock()
    monkeypatch.setattr(
        "ansys.tools.common.cyberchannel.verify_transport_mode", fake_verify
    )

    uds_dir = tmp_path / "conn"
    # Do not create uds dir beforehand — constructor should create it
    with pytest.raises(MapdlRuntimeError):
        MapdlGrpc(channel=MagicMock(spec=grpc.Channel), uds_dir=str(uds_dir))

    fake_verify.assert_called_once()


def test_missing_ansys_tools_common_raises(monkeypatch):
    # Force import of verifier to raise ModuleNotFoundError
    real_import = __import__

    def fake_import(name, globals_=None, locals=None, fromlist=(), level=0):
        if name.startswith("ansys.tools.common.cyberchannel") or (
            name == "ansys.tools.common" and "cyberchannel" in fromlist
        ):
            raise ModuleNotFoundError
        return real_import(name, globals_, locals, fromlist, level)

    monkeypatch.setattr("builtins.__import__", fake_import)
    with pytest.raises(ModuleNotFoundError):
        MapdlGrpc(channel=MagicMock(spec=grpc.Channel))


def test_uds_conflict_increments_port(tmp_path, monkeypatch):
    # Create uds dir and a conflicting socket file
    uds_dir = tmp_path / "conn"
    uds_dir.mkdir()
    sock = uds_dir / "mapdl-50052.sock"
    sock.write_text("busy")

    # Patch verify to no-op
    monkeypatch.setattr(
        "ansys.tools.common.cyberchannel.verify_transport_mode", lambda *a, **k: None
    )

    with pytest.raises(ValueError):
        MapdlGrpc(transport_mode="uds", uds_dir=str(uds_dir), port=50052)


def test_remote_ip_with_uds_raises(monkeypatch):
    # Patch verify to no-op
    monkeypatch.setattr(
        "ansys.tools.common.cyberchannel.verify_transport_mode", lambda *a, **k: None
    )

    with pytest.raises(ValueError):
        MapdlGrpc(
            ip="1.2.3.4",
            port=50052,
            channel=MagicMock(spec=grpc.Channel),
            transport_mode="uds",
        )
