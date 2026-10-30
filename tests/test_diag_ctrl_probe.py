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

# TEMPORARY diagnostic probe for Remote v25.2.0 is_alive failures. Do not merge.
"""Does Ctrl("VERSION") fail on fresh channels while RunCmd succeeds?"""
from collections import Counter

import grpc

from ansys.api.mapdl.v0 import ansys_kernel_pb2 as anskernel
from ansys.api.mapdl.v0 import mapdl_pb2 as pb_types
from ansys.api.mapdl.v0 import mapdl_pb2_grpc as mapdl_grpc
from conftest import requires, restore_connection

N_CHANNELS = 100
N_REBUILDS = 50


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


@requires("remote")
def test_probe_ctrl_after_channel_rebuild(mapdl, cleared):
    """Replay the captured failure: exit() on an exited instance closes the
    channel, teardown reconnects, /PREP7 works, then the first VERSION fails."""
    results = []
    for i in range(N_REBUILDS):
        mapdl._exited = True
        mapdl.exit()  # 'Already exited' path: closes the channel, MAPDL keeps running
        mapdl._exited = False
        restore_connection(mapdl)
        mapdl.prep7()
        version = lambda: mapdl._stub.Ctrl(anskernel.CtrlRequest(ctrl="VERSION"), timeout=5)
        results.append((i, _call(version)))

    failures = [r for r in results if r[1] != "OK"]
    print(Counter(out.split(" | ")[0] for _, out in results))
    for r in failures[:20]:
        print(r)
    assert not failures, f"{len(failures)} failed VERSION calls out of {len(results)}"
