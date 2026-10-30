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
import threading

from ansys.api.mapdl.v0 import ansys_kernel_pb2 as anskernel
from ansys.api.mapdl.v0 import mapdl_pb2 as pb_types
from ansys.api.mapdl.v0 import mapdl_pb2_grpc as mapdl_grpc
import grpc

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
            version = lambda: stub.Ctrl(
                anskernel.CtrlRequest(ctrl="VERSION"), timeout=5
            )
            run = lambda: stub.SendCommand(
                pb_types.CmdRequest(command="/COM,probe"), timeout=5
            )

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
        version = lambda: mapdl._stub.Ctrl(
            anskernel.CtrlRequest(ctrl="VERSION"), timeout=5
        )
        results.append((i, _call(version)))

    failures = [r for r in results if r[1] != "OK"]
    print(Counter(out.split(" | ")[0] for _, out in results))
    for r in failures[:20]:
        print(r)
    assert not failures, f"{len(failures)} failed VERSION calls out of {len(results)}"


N_CONCURRENT = 2000


@requires("remote")
def test_probe_concurrent_ctrl_and_status(mapdl, cleared):
    """Two threads share one raw channel: one loops Ctrl(VERSION), the other
    loops *STATUS. Any reply carrying the other call's payload is a swap."""
    with grpc.insecure_channel(mapdl._channel_str) as channel:
        grpc.channel_ready_future(channel).result(timeout=10)
        stub = mapdl_grpc.MapdlServiceStub(channel)
        version = lambda: stub.Ctrl(anskernel.CtrlRequest(ctrl="VERSION"), timeout=5)
        status = lambda: stub.SendCommand(
            pb_types.CmdRequest(command="*STATUS"), timeout=5
        )

        stub.SendCommand(pb_types.CmdRequest(command="PRBPARM=1"), timeout=5)
        ref_version = version().response.strip()
        assert ref_version and "PARAMETER STATUS" in status().response

        def classify_version():
            out = version().response.strip()
            if out == ref_version:
                return "OK"
            return "SWAP" if "PARAMETER STATUS" in out else f"OTHER {out[:80]!r}"

        def classify_status():
            out = status().response
            if "PARAMETER STATUS" in out:
                return "OK"
            return "SWAP" if out.strip() == ref_version else f"OTHER {out[:80]!r}"

        results = {"version": [], "status": []}
        barrier = threading.Barrier(2)

        def loop(name, fn):
            barrier.wait()
            for i in range(N_CONCURRENT):
                try:
                    results[name].append((i, fn()))
                except grpc.RpcError as e:
                    results[name].append((i, f"{e.code().name} | {e.details()!r}"))

        threads = [
            threading.Thread(target=loop, args=("version", classify_version)),
            threading.Thread(target=loop, args=("status", classify_status)),
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

    # Does the server reject Ctrl on connections opened afterwards (sample 2 state)?
    with grpc.insecure_channel(mapdl._channel_str) as channel:
        grpc.channel_ready_future(channel).result(timeout=10)
        stub = mapdl_grpc.MapdlServiceStub(channel)
        after = _call(
            lambda: stub.Ctrl(anskernel.CtrlRequest(ctrl="VERSION"), timeout=5)
        )

    print(f"ref_version={ref_version!r} fresh-channel VERSION after: {after}")
    for name, res in results.items():
        print(name, Counter(out.split(" | ")[0].split(" ")[0] for _, out in res))
        for r in [r for r in res if r[1] != "OK"][:10]:
            print(" ", name, r)
    bad = sum(out != "OK" for res in results.values() for _, out in res)
    assert not bad and after == "OK", f"{bad} bad replies; fresh VERSION after: {after}"
