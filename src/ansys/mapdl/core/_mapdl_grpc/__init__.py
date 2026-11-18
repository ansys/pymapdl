# Copyright (C) 2016 - 2026 ANSYS, Inc. and/or its affiliates.
# Copyright (C) 2016 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
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

"""Private gRPC MAPDL mixins composed by :class:`ansys.mapdl.core.mapdl_grpc.MapdlGrpc`."""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pathlib import Path
    import subprocess  # nosec B404
    import threading
    from typing import Callable

    from ansys.api.mapdl.v0 import mapdl_pb2_grpc as mapdl_grpc
    from ansys.platform.instancemanagement import Instance as PIM_Instance
    import grpc

    from ansys.mapdl.core.database import MapdlDb
    from ansys.mapdl.core.xpl import ansXpl

    class _GrpcMixinBase:
        """Type-only base for cooperative gRPC MAPDL mixins.

        Declares state assigned by ``MapdlGrpc`` for sibling mixins. This is
        a nominal type-only base: Protocol subclasses infer new member types
        from assignments instead of retaining the inherited declarations.
        Methods and state owned by ``MapdlBase`` remain late-bound.
        """

        # Connection and transport.
        _channel: grpc.Channel | None
        _channel_state: grpc.ChannelConnectivity
        _connectivity_callback: Callable[[Any], None] | None
        _ip: str | None
        _port: int | None
        _server_version_cache: tuple[int, int, int] | None
        _state: grpc.Future | None
        _stub: mapdl_grpc.MapdlServiceStub | None
        _timeout: int
        certs_dir: Path | None
        transport_mode: str | None
        uds_dir: Path

        @property
        def _connected_stub(self) -> mapdl_grpc.MapdlServiceStub: ...

        # In-flight call tracking and liveness.
        _current_call: grpc.Future | None
        _current_call_lock: threading.Lock
        _exited: bool | None
        _exiting: bool

        # Local process, working directory and teardown.
        _jobname: str
        _launched: bool
        _local: bool
        _mapdl_on_hpc: bool
        _mapdl_process: subprocess.Popen | None
        _path: str | None
        _pids: list[int | None]
        _process_close_lock: threading.Lock
        _remote_instance: PIM_Instance | None
        _start_instance: str | None
        finish_job_on_exit: bool
        remove_temp_dir_on_exit: bool

        # Queries, file transfer and lazily built accessors.
        _db: MapdlDb | None
        _get_lock: threading.Lock
        _lazy_array_counter: int
        _lazy_array_parameters: set[str]
        _lazy_array_prefix: str
        _prioritize_thermal: bool
        _vget_lock: threading.Lock
        _xpl: ansXpl | None

        def __getattr__(self, name: str) -> Any: ...

else:
    _GrpcMixinBase = object
