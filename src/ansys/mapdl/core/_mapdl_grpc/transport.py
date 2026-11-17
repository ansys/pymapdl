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

"""Module-level gRPC transport helpers: channel options and file chunking."""

import io
import json
import os

from ansys.api.mapdl.v0 import ansys_kernel_pb2 as anskernel
from ansys.api.mapdl.v0 import mapdl_pb2 as pb_types

from ansys.mapdl.core import _HAS_TQDM
from ansys.mapdl.core.common_grpc import DEFAULT_FILE_CHUNK_SIZE
from ansys.mapdl.core.constants import MAX_MESSAGE_LENGTH

# Checking if tqdm is installed.
# If it is, the default value for progress_bar is true.
if _HAS_TQDM:
    from tqdm import tqdm


VOID_REQUEST = anskernel.EmptyRequest()


# Retry policy for gRPC calls.
SERVICE_DEFAULT_CONFIG = {
    # see https://github.com/grpc/proposal/blob/master/A6-client-retries.md#retry-policy-capabilities
    "methodConfig": [
        {
            # Match all packages and services.
            # Otherwise: "name": [{"service": "<package>.<service>"}],
            "name": [{}],
            "retryPolicy": {
                "maxAttempts": 5,
                "initialBackoff": "0.01s",
                "maxBackoff": "3s",
                "backoffMultiplier": 3,
                "retryableStatusCodes": ["UNAVAILABLE", "RESOURCE_EXHAUSTED"],
            },
        }
    ]
}


# Interval between HTTP/2 keepalive pings. grpc-core's default server-side
# ping-abuse policy requires at least 5 minutes between two "no data" pings
# while a call is in flight and sends a 'GOAWAY' ('too_many_pings') on the
# 3rd closer ping, so a shorter interval drops long calls such as 'SOLVE'.
# The ping strike counter must not be reset with a background RPC instead:
# MAPDL mixes up the replies of concurrent calls (a 'Ctrl' reply replaces the
# output of a running command) and can crash under such load. The extra 10%
# keeps timer jitter from landing a ping just inside the 5-minute window.
KEEPALIVE_TIME_MS = 330_000


DEFAULT_GRPC_OPTIONS = [
    ("grpc.max_receive_message_length", MAX_MESSAGE_LENGTH),
    ("grpc.service_config", json.dumps(SERVICE_DEFAULT_CONFIG)),
    # HTTP/2 keepalive pings: detect a peer that stopped answering (crashed,
    # network partition, silently dropped connection) even while no RPC is
    # exchanging data, without bounding how long any individual call (such as
    # 'SOLVE') is allowed to run. A dead peer flips 'channel_state' to
    # 'TRANSIENT_FAILURE' within roughly 'keepalive_time_ms' +
    # 'keepalive_timeout_ms', instead of relying on the OS to eventually
    # notice the broken TCP connection.
    ("grpc.keepalive_time_ms", KEEPALIVE_TIME_MS),
    ("grpc.keepalive_timeout_ms", 10_000),
    ("grpc.keepalive_permit_without_calls", 1),
    ("grpc.http2.min_time_between_pings_ms", KEEPALIVE_TIME_MS),
    ("grpc.http2.max_pings_without_data", 0),
]


def chunk_raw(raw, save_as):
    with io.BytesIO(raw) as f:
        while True:
            piece = f.read(DEFAULT_FILE_CHUNK_SIZE)
            length = len(piece)
            if length == 0:
                return
            yield pb_types.UploadFileRequest(
                file_name=os.path.basename(save_as),
                chunk=anskernel.Chunk(payload=piece, size=length),
            )


def get_file_chunks(filename, progress_bar=False):
    """Serializes a file into chunks"""
    pbar = None
    if progress_bar:
        if not _HAS_TQDM:  # pragma: no cover
            raise ModuleNotFoundError(
                "To use the keyword argument 'progress_bar', you need to have "
                "installed the `tqdm` package. "
                "To avoid this message set `progress_bar=False`."
            )

        n_bytes = os.path.getsize(filename)

        base_name = os.path.basename(filename)
        pbar = tqdm(
            total=n_bytes,
            desc=f"Uploading {base_name}",
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
        )

    with open(filename, "rb") as f:
        while True:
            piece = f.read(DEFAULT_FILE_CHUNK_SIZE)
            length = len(piece)
            if length == 0:
                if pbar is not None:
                    pbar.close()
                return

            if pbar is not None:
                pbar.update(length)

            chunk = anskernel.Chunk(payload=piece, size=length)
            yield pb_types.UploadFileRequest(
                file_name=os.path.basename(filename), chunk=chunk
            )


def save_chunks_to_file(
    chunks, filename, progress_bar=False, file_size=None, target_name=""
):
    """Saves chunks to a local file

    Returns
    -------
    file_size : int
        File size saved in bytes.  ``0`` means no file was written.
    """
    pbar = None
    if progress_bar:
        if not _HAS_TQDM:  # pragma: no cover
            raise ModuleNotFoundError(
                f"To use the keyword argument 'progress_bar', you need to have installed the 'tqdm' package."
                "To avoid this message you can set 'progress_bar=False'."
            )

        pbar = tqdm(
            total=file_size,
            desc="Downloading %s" % target_name,
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
        )

    file_size = 0
    with open(filename, "wb") as f:
        for chunk in chunks:
            f.write(chunk.payload)
            payload_size = len(chunk.payload)
            file_size += payload_size
            if pbar is not None:
                pbar.update(payload_size)

    if pbar is not None:
        pbar.close()

    return file_size
