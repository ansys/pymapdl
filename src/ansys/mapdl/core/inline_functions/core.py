# Copyright (C) 2024 ANSYS, Inc. and/or its affiliates.
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

from enum import IntEnum
from typing import Union
import warnings

from ansys.mapdl.core.errors import MapdlRuntimeError

QUERY_NAME = "__QUERY_PARM__"


class SelectionStatus(IntEnum):
    """Enumeration class for selection status information.

    This class is used with methods on the ``Query`` class and has the
    following options.

    UNSELECTED = -1
    UNDEFINED = 0
    SELECTED = 1

    Examples
    --------
    The following example is taken from ``Query.nsel`` and demonstrates
    how `SelectionSatus` appears in PyMAPDL.

    Here we create a single node and interrogate its selection
    status.

    >>> from ansys.mapdl.core import launch_mapdl
    >>> from ansys.mapdl.core.inline_functions import Query
    >>> mapdl = launch_mapdl()
    >>> mapdl.prep7()
    >>> n1 = mapdl.n(1, 0, 0, 0)
    >>> n1
    1

    We can use ``Query.nsel`` to interrogate the selection status
    of the node. We can get the ``Query`` object from the
    ``mapdl.queries`` property. The response is an
    ``enum.IntEnum`` object. If you query a node that does not
    exist, it will return a status ``SelectionStatus.UNDEFINED``.

    >>> q = mapdl.queries
    >>> q.nsel(n1)
    <SelectionStatus.SELECTED: 1>
    >>> mapdl.nsel('NONE')
    >>> q.nsel(n1)
    <SelectionStatus.UNSELECTED: -1>
    >>> q.nsel(0)
    <SelectionStatus.UNDEFINED: 0>
    """

    UNSELECTED = -1
    UNDEFINED = 0
    SELECTED = 1


class _QueryExecution:
    def _run_query(self, command: str, integer: bool) -> Union[int, float]:
        # import here to avoid circular import
        from ansys.mapdl.core.mapdl_grpc import MapdlGrpc

        # non_interactive mode won't work with these commands
        if self._mapdl._store_commands:
            raise MapdlRuntimeError(
                "Inline MAPDL functions are incompatible with the "
                "non_interactive mode."
            )

        # use the underlying gRPC method if available to avoid parsing the string
        resp = self._mapdl._run(f"{QUERY_NAME}={command}")
        if isinstance(self._mapdl, MapdlGrpc):
            value = self._mapdl.scalar_param(QUERY_NAME)
            if value is None:
                raise MapdlRuntimeError(resp)
            if integer:
                return int(value)
            return value
        else:
            if integer:
                return self._parse_parameter_integer_response(resp)
            return self._parse_parameter_float_response(resp)

    def _parse_parameter_integer_response(self, response) -> int:
        """Parse integer response."""
        return int(self._parse_parameter_float_response(response))

    @staticmethod
    def _parse_parameter_float_response(response) -> float:
        if "PARAMETER" not in response or "=" not in response:
            raise TypeError(f"Parameter response not recognised: " f'"{response}"')
        parts = response.rsplit("=", 1)
        if "WARNING" in parts[0]:
            warnings.warn(parts[0])

        number = parts[1].strip()
        return float(number)
