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

"""Common gRPC functions"""

import time
from typing import Any, Optional

import grpc
import numpy as np

from ansys.mapdl.core import LOG
from ansys.mapdl.core import constants as _constants
from ansys.mapdl.core.errors import MapdlConnectionError, MapdlRuntimeError

ANSYS_VALUE_TYPE = _constants.ANSYS_VALUE_TYPE
COMP_TYPE = _constants.COMMON_GRPC_COMP_TYPE
DEFAULT_CHUNKSIZE = _constants.DEFAULT_CHUNKSIZE
DEFAULT_FILE_CHUNK_SIZE = _constants.DEFAULT_FILE_CHUNK_SIZE
STRESS_TYPES = _constants.COMMON_GRPC_STRESS_TYPES
VGET_ENTITY_TYPES = _constants.VGET_ENTITY_TYPES
VGET_NODE_ENTITY_TYPES = _constants.VGET_NODE_ENTITY_TYPES


class GrpcError(MapdlRuntimeError):
    """Raised when gRPC fails.

    Parameters
    ----------
    msg : str, optional
        Error message, by default "".
    """

    def __init__(self, msg: str = "") -> None:
        """Initialize GrpcError.

        Parameters
        ----------
        msg : str, optional
            Error message, by default "".
        """
        super().__init__(self, msg=msg)


def check_vget_input(entity: str, item: str, itnum: str) -> str:
    """Verify that entity and item for VGET are valid.

    Raises a ``ValueError`` when invalid.

    Parameters
    ----------
    entity : str
        Entity keyword. Valid keywords are:

        - ``'NODE'``
        - ``'ELEM'``
        - ``'KP'``
        - ``'LINE'``
        - ``'AREA'``
        - ``'VOLU'``
        - ``'CDSY'``
        - ``'RCON'``
        - ``'TLAB'``

    item : str
        The name of a particular item for the given entity. Valid
        items are as shown in the item columns of the tables
        within the ``*VGET`` command reference in your ANSYS manual.

    itnum : str
        The number (or label) for the specified item (if
        any). Valid it1num values are as shown in the IT1NUM
        columns of the tables in the command reference section for
        the ``*VGET`` command in your ANSYS manual. Some Item1 labels
        do not require an IT1NUM value.

    Returns
    -------
    str
        MAPDL formatted vget command after the "VGET, " in the format of:
        "ENTITY, , ITEM, ITNUM"
    """
    entity = entity.upper()
    if item is not None:
        item = item.upper()

    if itnum is not None:
        itnum = itnum.upper()

    if entity not in VGET_ENTITY_TYPES:
        raise ValueError(
            'Entity "%s" not allowed.  Allowed items:\n%s' % entity,
            str(VGET_ENTITY_TYPES),
        )

    if entity == "NODE":
        if item not in VGET_NODE_ENTITY_TYPES:
            allowed_types = list(VGET_NODE_ENTITY_TYPES.keys())
            raise ValueError(
                'item "%s" for "NODE" not allowed.  Allowed items:%s\n'
                % (item, str(allowed_types))
            )

        if itnum not in VGET_NODE_ENTITY_TYPES[item]:
            allowed_types = VGET_NODE_ENTITY_TYPES[item]
            raise ValueError(
                'itnum "%s" for item "%s" not allowed.  Allowed items:\n%s'
                % (itnum, item, str(allowed_types))
            )

    # None is not allowed in MAPDL commands
    if item is None:
        item = ""
    if itnum is None:
        itnum = ""

    return "%s, , %s, %s" % (entity, item, itnum)


def parse_chunks(
    chunks: Any,  # type: ignore[misc]  # gRPC call iterator with custom methods
    dtype: Optional[np.typing.DTypeLike] = None,
) -> np.ndarray:
    """Deserialize gRPC chunks into a numpy array.

    Parameters
    ----------
    chunks : Any
        gRPC response iterator.  Each chunk contains a bytes payload

    dtype : np.dtype
        Numpy data type to interpret chunks as.

    Returns
    -------
    np.ndarray
        Deserialized numpy array.
    """
    timeout = 3  # seconds
    time_step = 0.01
    time_max = timeout + time.time()  # seconds

    while not chunks.is_active() and time.time() < time_max:
        time.sleep(time_step)

    if not chunks.is_active() and chunks.code() != grpc.StatusCode.OK:
        LOG.error("The channel might not alive.")

    try:
        chunk = chunks.next()

    except StopIteration:
        if chunks.code() == grpc.StatusCode.OK:
            return np.empty(0)
        else:
            raise MapdlConnectionError(
                "The chunk couldn't be parsed. The error information is:\n"
                f"code: {chunks.code()}\n"
                f"message: '{chunks.details()}'"
            )

    if not chunk.value_type and dtype is None:
        raise ValueError("Must specify a data type for this record")

    if dtype is None:
        dtype = ANSYS_VALUE_TYPE[chunk.value_type]

    array = np.frombuffer(chunk.payload, dtype)
    if chunks.done():
        return array

    arrays = [array]
    for chunk in chunks:
        arrays.append(np.frombuffer(chunk.payload, dtype))

    return np.hstack(arrays)
