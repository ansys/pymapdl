# TEMPORARY diagnostic probe for Remote v25.2.0 is_alive failures. Do not merge.
"""Does Ctrl("VERSION") fail on fresh channels while RunCmd succeeds?"""
from collections import Counter

import grpc

from ansys.api.mapdl.v0 import ansys_kernel_pb2 as anskernel
from ansys.api.mapdl.v0 import mapdl_pb2 as pb_types
from ansys.api.mapdl.v0 import mapdl_pb2_grpc as mapdl_grpc
from conftest import requires

N_CHANNELS = 100


def _call(fn):
    try:
        fn()
        return "OK"
    except grpc.RpcError as e:
        return f"{e.code().name} | {e.details()!r} | {e.debug_error_string()}"


@requires("remote")
def test_probe_ctrl_on_fresh_channels(mapdl, cleared):
    results = []
    for i in range(N_CHANNELS):
        with grpc.insecure_channel(mapdl._channel_str) as channel:
            grpc.channel_ready_future(channel).result(timeout=10)
            stub = mapdl_grpc.MapdlServiceStub(channel)
            version = lambda: stub.Ctrl(anskernel.CtrlRequest(ctrl="VERSION"), timeout=5)
            run = lambda: stub.SendCommand(pb_types.CmdRequest(command="/COM,probe"), timeout=5)

            for step, fn in (("ctrl-1", version), ("run", run), ("ctrl-2", version)):
                results.append((i, step, _call(fn)))

    failures = [r for r in results if r[2] != "OK"]
    print(Counter((step, out.split(" | ")[0]) for _, step, out in results))
    for r in failures[:20]:
        print(r)
    assert not failures, f"{len(failures)} failed calls out of {len(results)}"
