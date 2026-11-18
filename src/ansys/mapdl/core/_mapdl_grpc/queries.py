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

"""Value queries, parameter arrays and lazy array lifetimes."""

import time
from typing import (
    TYPE_CHECKING,
    Union,
)

from ansys.api.mapdl.v0 import mapdl_pb2 as pb_types
import numpy as np
from numpy.typing import NDArray

from ansys.mapdl.core.common_grpc import parse_chunks
from ansys.mapdl.core.constants import ANSYS_VALUE_TYPE
from ansys.mapdl.core.errors import (
    MapdlError,
    MapdlRuntimeError,
    protect_grpc,
)
from ansys.mapdl.core.lazy_array import LazyArray
from ansys.mapdl.core.mapdl_core import MAX_PARAM_CHARS
from ansys.mapdl.core.mapdl_types import KwargDict, MapdlFloat

if TYPE_CHECKING:  # pragma: no cover

    from ansys.mapdl.core.xpl import ansXpl

from . import _GrpcMixinBase


class _GrpcQueryMixin(_GrpcMixinBase):
    """Value queries, parameter arrays and lazy array lifetimes."""

    @protect_grpc
    def _get(  # numpydoc ignore=RT01
        self,
        entity: str = "",
        entnum: str = "",
        item1: str = "",
        it1num: MapdlFloat = "",
        item2: str = "",
        it2num: MapdlFloat = "",
        item3: MapdlFloat = "",
        it3num: MapdlFloat = "",
        item4: MapdlFloat = "",
        it4num: MapdlFloat = "",
        **kwargs: KwargDict,
    ) -> Union[float, str]:
        """Sends gRPC *Get request.

        .. warning::
           Not thread safe.  Uses ``_get_lock`` to ensure multiple
           request are not evaluated simultaneously.
        """
        if self._session_id is not None:
            self._check_session_id()

        if self._store_commands:
            raise MapdlRuntimeError(
                "Cannot use `mapdl.get_value` when in `non_interactive` mode. "
                "Exit non_interactive mode before using this method.\n\n"
                "Alternatively you can use `mapdl.get` to specify the name of "
                "the MAPDL parameter where to store the retrieved value.\n"
            )

        cmd = f"{entity},{entnum},{item1},{it1num},{item2},{it2num},{item3}, {it3num}, {item4}, {it4num}"

        # not threadsafe; don't allow multiple get commands
        timeout_ = kwargs.pop("timeout", 2)
        timeout = time.time() + timeout_
        while self._get_lock:
            time.sleep(0.001)
            if time.time() > timeout:
                raise MapdlRuntimeError(
                    f"PyMAPDL couldn't obtain 'get_lock' in {timeout_} seconds "
                    "and PyMAPDL cannot issue multiple get commands simultaneously."
                )

        self._get_lock = True
        try:
            if self._stub is None:
                raise MapdlRuntimeError("MAPDL stub not initialized")
            response = self._stub.Get(pb_types.GetRequest(getcmd=cmd))
        finally:
            self._get_lock = False

        if response.type == 0:
            self._log.debug(
                "The 'grpc' get method seems to have failed. Trying old implementation for more verbose output."
            )

            response = self.run("*GET,__temp__," + cmd, mute=False)
            self._log.debug(f"Default *get output:\n{response}")

            if response:
                from ansys.mapdl.core.misc import is_float

                if "VALUE=" in response:
                    response = response.split("VALUE=")[1].strip()

                if is_float(response):
                    return float(response)
                else:
                    return response
            else:
                raise MapdlError(
                    f"Error when processing '*get' request output.\n{response}"
                )

        if response.type == 1:
            return response.dval
        elif response.type == 2:
            return response.sval

        raise MapdlRuntimeError(f"Unsupported type {response.type} response from MAPDL")

    def _get_array_from_service(
        self,
        entity,
        entnum,
        item1,
        it1num,
        item2,
        it2num,
        kloop,
    ) -> NDArray[np.float64]:
        """Return an eager ``*VGET`` result through the gRPC service."""
        while self._vget_lock:
            time.sleep(0.001)
        self._vget_lock = True

        cmd = f"{entity},{entnum},{item1},{it1num},{item2},{it2num},{kloop}"
        try:
            if self._stub is None:
                raise MapdlRuntimeError("MAPDL stub not initialized")
            chunks = self._stub.VGet2(pb_types.GetRequest(getcmd=cmd))
            return parse_chunks(chunks)
        finally:
            self._vget_lock = False

    @protect_grpc
    def _get_array(
        self,
        entity="",
        entnum="",
        item1="",
        it1num="",
        item2="",
        it2num="",
        kloop="",
        **kwargs,
    ) -> Union[NDArray[np.float64], LazyArray]:
        """Populate a private MAPDL parameter and return it lazily.

        The ``*VGET`` command is issued immediately so the result reflects the
        selection at call time, even if the selection changes before the values
        are used. Only the download is deferred. On first use, the values are
        read with a binary ``*GET`` plus ``mwrite`` rather than by parsing
        ``*STATUS,PRM_`` output.
        """
        if "parm" in kwargs:
            raise ValueError("Parameter name `parm` not supported with gRPC")
        if str(item1).strip().upper() == "ETAB":
            return self._get_array_from_service(
                entity, entnum, item1, it1num, item2, it2num, kloop
            )
        parameter_name = self._new_lazy_array_parameter()
        try:
            output = self.starvget(
                parameter_name,
                entity,
                entnum,
                item1,
                it1num,
                item2,
                it2num,
                kloop,
                mute=False,
            )
        except Exception as error:
            try:
                self._delete_lazy_array_parameter(parameter_name)
            except Exception as cleanup_error:
                raise cleanup_error from error
            raise

        if "the dimension number 1 is 0" in output:
            self._delete_lazy_array_parameter(parameter_name)
            return np.empty(0)

        return LazyArray(
            self,
            parameter_name,
            cleanup=lambda: self._delete_lazy_array_parameter(parameter_name),
            fetch=lambda: self._read_owned_array_parameter(parameter_name),
            flatten=True,
        )

    @protect_grpc
    def scalar_param(self, pname: str) -> float:
        """Return a scalar parameter as a float.

        If parameter does not exist, returns ``None``.

        Returns
        -------
        float or None
            The value of the parameter as a float or ``None`` if the
            parameter does not exist.
        """
        request = pb_types.ParameterRequest(name=pname, array=False)
        if self._stub is None:
            raise MapdlRuntimeError("MAPDL stub not initialized")
        presponse = self._stub.GetParameter(request)
        if presponse.val:
            return float(presponse.val[0])

    # TODO: not fully tested/implemented
    @protect_grpc
    def Param(self, pname):
        presponse = self._stub.GetParameter(pb_types.ParameterRequest(name=pname))
        return presponse.val

    # TODO: not fully tested/implemented
    @protect_grpc
    def Var(self, num):
        presponse = self._stub.GetVariable(pb_types.VariableRequest(inum=num))
        return presponse.val

    @property
    def math(self):
        """Interface to launch PyAnsys Math from PyMAPDL.

         Returns
        -------
        :class:`MapdlMath <ansys.mapdl.core.math.MapdlMath>`
            MAPDL Math interface.

        Examples
        --------
        Get the stiffness matrix from MAPDL
        >>> mm = mapdl.math
        >>> k = mm.stiff()
        >>> k.asarray()
        <60x60 sparse matrix of type '<class 'numpy.float64'>'
            with 1734 stored elements in Compressed Sparse Row format>

        Get the mass matrix from MAPDL
        >>> mm = mapdl.math
        >>> m = mm.stiff()
        >>> m.asarray()
        <60x60 sparse matrix of type '<class 'numpy.float64'>'
            with 1734 stored elements in Compressed Sparse Row format>
        """
        if self._math is None:
            from ansys.math.core.math import AnsMath

            self._math = AnsMath(self)

        return self._math

    @property
    def krylov(self):
        """APDL krylov interface.

        For more information, see the :class:`KrylovSolver <ansys.mapdl.core.krylov.KrylovSolver>`

        Returns
        -------
        :class:`Krylov class <ansys.mapdl.core.krylov.KrylovSolver>`
            An instance of :class:`Krylov class <ansys.mapdl.core.krylov.KrylovSolver>`
        """
        if self._krylov is None:
            from ansys.mapdl.core.krylov import KrylovSolver

            self._krylov = KrylovSolver(self)

        return self._krylov

    @property
    def db(self):
        """
        MAPDL database interface.

        Returns
        -------
        :class:`MapdlDb <ansys.mapdl.core.database.MapdlDb>`
            MAPDL database interface.

        Examples
        --------
        Create a nodes instance.

        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> # create nodes...
        >>> nodes = mapdl.db.nodes
        >>> print(nodes)
        MAPDL Database Nodes
            Number of nodes:          270641
            Number of selected nodes: 270641
            Maximum node number:      270641

        >>> mapdl.nsel("NONE")
        >>> print(nodes)
        MAPDL Database Nodes
            Number of nodes:          270641
            Number of selected nodes: 0
            Maximum node number:      270641

        Return the selection status and the coordinates of node 22.

        >>> nodes = mapdl.db.nodes
        >>> sel, coord = nodes.coord(22)
        >>> coord
        (1.0, 0.5, 0.0, 0.0, 0.0, 0.0)
        """
        from ansys.mapdl.core.database import MapdlDb

        if self._db is None:
            self._db = MapdlDb(self)
            self._db.start()

        return self._db

    @property
    def xpl(self) -> "ansXpl":
        """MAPDL file explorer

        Iteratively navigate through MAPDL files.

        Returns
        -------
        :class:`ansXpl <ansys.mapdl.core.xpl.ansXpl>`
            An instance of :class:`ansXpl <ansys.mapdl.core.xpl.ansXpl>`.

        Examples
        --------
        Read the MASS record from the "file.full" file

        >>> from ansys import Mapdl
        >>> mapdl = Mapdl()
        >>> xpl = mapdl.xpl
        >>> xpl.open('file.full')
        >>> vec = xpl.read('MASS')
        >>> vec.asarray()
        array([ 4,  7, 10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43, 46, 49, 52,
               55, 58,  1], dtype=int32)
        """
        if self._xpl is None:
            from ansys.mapdl.core.xpl import ansXpl

            self._xpl = ansXpl(self)
        return self._xpl

    @protect_grpc
    def _data_info(self, pname):  # numpydoc ignore=RT01
        """Returns the data type of a parameter

        APDLMATH vectors only.
        """
        request = pb_types.ParameterRequest(name=pname)
        return self._stub.GetDataInfo(request)

    @protect_grpc
    def _vec_data(self, pname):  # numpydoc ignore=RT01
        """Downloads vector data from a MAPDL MATH parameter"""
        dtype = ANSYS_VALUE_TYPE[self._data_info(pname).stype]
        request = pb_types.ParameterRequest(name=pname)
        chunks = self._stub.GetVecData(request)
        return parse_chunks(chunks, dtype)

    @protect_grpc
    def _mat_data(self, pname, raw=False):  # numpydoc ignore=RT01
        """Downloads matrix data from a parameter and returns a scipy sparse array"""
        try:
            from scipy import sparse
        except ImportError:  # pragma: no cover
            raise ImportError("Install ``scipy`` to use this feature") from None

        minfo = self._data_info(pname)
        stype = ANSYS_VALUE_TYPE[minfo.stype]
        mtype = minfo.objtype
        shape = (minfo.size1, minfo.size2)

        if mtype == 2:  # dense
            request = pb_types.ParameterRequest(name=pname)
            chunks = self._stub.GetMatData(request)
            values = parse_chunks(chunks, stype)
            return np.transpose(np.reshape(values, shape[::-1]))
        elif mtype == 3:  # sparse
            indptr = self._vec_data(pname + "::ROWS")
            indices = self._vec_data(pname + "::COLS")
            vals = self._vec_data(pname + "::VALS")
            if raw:  # for debug
                return vals, indices, indptr, shape
            else:
                return sparse.csr_matrix(
                    (vals, indices, indptr), dtype=stype, shape=shape
                )

        raise ValueError(f'Invalid matrix type "{mtype}"')

    def _new_lazy_array_parameter(self) -> str:
        """Reserve an unused, valid MAPDL parameter name for a lazy result."""
        prefix = self._lazy_array_prefix
        while True:
            self._lazy_array_counter += 1
            candidate = f"{prefix}{self._lazy_array_counter:016X}"
            if len(candidate) > MAX_PARAM_CHARS:  # pragma: no cover
                raise MapdlRuntimeError("Unable to generate a valid lazy-array name.")

            # Include parameters hidden by display settings while checking so
            # a user parameter cannot be overwritten.
            with self.parameters.full_parameters_output:
                if candidate not in self.parameters:
                    self._lazy_array_parameters.add(candidate)
                    return candidate

    def _delete_lazy_array_parameter(self, parameter_name: str) -> None:
        """Delete an owned lazy-result parameter and unregister it."""
        self.run(f"{parameter_name}=", mute=True)
        self._lazy_array_parameters.remove(parameter_name)

    def _cleanup_lazy_array_parameters(self) -> None:
        """Delete every unresolved lazy-result parameter."""
        for parameter_name in tuple(getattr(self, "_lazy_array_parameters", ())):
            self._delete_lazy_array_parameter(parameter_name)

    def _read_owned_array_parameter(self, parameter_name: str) -> NDArray[np.float64]:
        """Download an owned column-vector parameter without parsing ``*STATUS``.

        The row count is read with a binary ``*GET`` query and the values are
        streamed with ``mwrite``, so this avoids the version-fragile
        ``*STATUS,PRM_`` listing that
        :meth:`Parameters.__getitem__ <ansys.mapdl.core.parameters.Parameters.__getitem__>`
        performs to discover the array shape.

        The result keeps the ``(rows, 1)`` shape that ``Parameters`` returns for
        ``*VGET`` parameters, so ``get_variable`` results are unchanged.
        ``get_array`` flattens it through ``LazyArray(flatten=True)``.
        """
        rows = int(self.get_value("PARM", parameter_name, "DIM", 1))
        if rows == 0:
            return np.empty(0)
        return self.parameters._get_parameter_array(parameter_name, (rows, 1))
