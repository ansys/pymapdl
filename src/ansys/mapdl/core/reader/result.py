# Copyright (C) 2016 - 2025 ANSYS, Inc. and/or its affiliates.
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

"""
Replacing Result in PyMAPDL.
"""


"""
COMMENTS
========


TODO's
======
* Check #todos
* Allow (step, substep) in rnum
* Component support
* Check what happens when a node does not have results in all the steps. In DPF is it zero?
* Adding 'principal' support ("SIGMA1, SIGMA2, SIGMA3, SINT, SEQV when principal is True.")
* Check DPF issues

"""

from functools import wraps
import logging
import os
import pathlib
import tempfile
from typing import TYPE_CHECKING, Any, Callable, Iterable, Literal
import uuid
import weakref

from ansys.mapdl.reader.rst import Result

# from ansys.dpf import post
import numpy as np

from ansys.mapdl.core import LOG as logger
from ansys.mapdl.core import Logger, Mapdl
from ansys.mapdl.core import _HAS_DPF, _HAS_PYVISTA
from ansys.mapdl.core.errors import MapdlRuntimeError
from ansys.mapdl.core.misc import check_valid_ip, random_string

COMPONENTS: list[str] = ["X", "Y", "Z", "XY", "YZ", "XZ"]

if _HAS_DPF:
    from ansys.dpf import core as dpf
    from ansys.dpf.core import Model
    from ansys.dpf.core.errors import DPFServerException


if TYPE_CHECKING:
    from ansys.mapdl.core import Mapdl

    if _HAS_PYVISTA:
        import pyvista as pv


class ResultNotFound(MapdlRuntimeError):
    """Results not found"""

    def __init__(self, msg=""):
        MapdlRuntimeError.__init__(self, msg)


def update_result(function: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorator to wrap :class:`DPFResult <ansys.mapdl.core.reader.result.DPFResult>`
    methods to force update the RST when accessed the first time.

    Parameters
    ----------
    update : bool, optional
        If ``True``, the class information is updated by calling ``/STATUS``
        before accessing the methods. By default ``False``
    """

    @wraps(function)
    def wrapper(self, *args, **kwargs):
        if self._update_required or not self._loaded or self._cached_dpf_model is None:
            self.update()
            self.logger.debug("RST file updated.")
        return function(self, *args, **kwargs)

    return wrapper


def generate_session_id(length: int = 10):
    """Generate an unique ssesion id.

    It can be shorten by the argument 'length'."""
    uid = uuid.uuid4()
    return "".join(str(uid).split("-")[:-1])[:length]


class DPFResult(Result):
    """
    Result object based on DPF library.


    This class replaces the class Result in PyMAPDL-Reader.

    The

    Parameters
    ----------
    rst_file_path : str
        Path to the RST file.

    mapdl : _MapdlCore
        Mapdl instantiated object.

    """

    def __init__(
        self, rst_file_path: str | None = None, mapdl: "Mapdl | None" = None
    ) -> None:
        """Initialize Result instance"""

        if not _HAS_DPF:
            raise ModuleNotFoundError(
                "The DPF library is not installed. Please install it using 'pip install ansys-dpf-core'."
            )

        self._mapdl_weakref = None
        self._server_file_path = None  # In case DPF is remote.
        self._session_id = None
        self._logger: Logger | None = None

        if rst_file_path is not None and mapdl is not None:
            raise ValueError(
                "Only one the arguments must be supplied: 'rst_file_path' or 'mapdl'."
            )

        elif rst_file_path is not None:
            if not os.path.exists(rst_file_path):
                raise FileNotFoundError(
                    f"The RST file '{rst_file_path}' could not be found."
                )

            logger.debug("Initializing DPFResult class in RST mode.")
            self._mode_rst = True

        elif mapdl is not None:
            from ansys.mapdl.core import Mapdl

            if not isinstance(mapdl, Mapdl):  # pragma: no cover # type: ignore
                raise TypeError("Must be initialized using Mapdl instance")

            logger.debug("Initializing DPFResult class in MAPDL mode.")
            self._mapdl_weakref = weakref.ref(mapdl)
            self._mode_rst = False
            rst_file_path = mapdl.result_file
            if rst_file_path is None:
                raise ValueError(
                    "RST file path is None. Please check the MAPDL instance."
                )

            # self._session_id = f"__{uuid.uuid4()}__"
            # self.mapdl.parameters[self._session_id] = 1

        else:
            raise ValueError(
                "One of the following kwargs must be supplied: 'rst_file_path' or 'mapdl'"
            )

        self.__rst_directory: str = os.path.dirname(rst_file_path)
        self.__rst_name: str = os.path.basename(rst_file_path)

        # dpf
        self._loaded: bool = False
        self._update_required: bool = (
            False  # if true, it triggers a update on the RST file
        )
        self._cached_dpf_model = None
        self._connected = False
        self._is_remote = (
            False  # Default false, unless using self.connect or the env var are set.
        )
        self._connection: Any | None = None

        self.connect_to_server()

        # old attributes
        ELEMENT_INDEX_TABLE_KEY = None  # todo: To fix
        ELEMENT_RESULT_NCOMP = None  # todo: to fix

        # these will be removed once the reader class has been fully substituted.
        # then we will inheritate from object.
        self._update()
        super().__init__(self._rst, read_mesh=False)

    def _generate_session_id(self, length: int = 10):
        """Generate an unique ssesion id.

        It can be shorten by the argument 'length'."""
        return "__" + generate_session_id(length)

    def _connect_to_dpf_using_mode(
        self,
        mode: Literal["InProcess", "LocalGrpc", "RemoteGrpc"] = "InProcess",
        external_ip: str | None = None,
        external_port: int | None = None,
    ):
        if mode == "InProcess":
            dpf.server.set_server_configuration(
                dpf.server_factory.AvailableServerConfigs.InProcessServer
            )
            srvr = dpf.server.start_local_server()
        elif mode == "LocalGrpc":
            dpf.server.set_server_configuration(
                dpf.server_factory.AvailableServerConfigs.GrpcServer
            )
            srvr = dpf.server.start_local_server()
        elif mode == "RemoteGrpc":
            dpf.server.set_server_configuration(
                dpf.server_factory.AvailableServerConfigs.GrpcServer
            )
            if external_ip is not None and external_port is not None:
                srvr = dpf.server.connect_to_server(ip=external_ip, port=external_port)
            else:
                raise Exception(
                    "external_ip and external_port should be provided for RemoteGrpc communication"
                )
        self._connection = srvr

    def _try_connect_inprocess(self) -> None:
        try:
            self._connect_to_dpf_using_mode(mode="InProcess")
            self._connected = True
        except DPFServerException:  # type: ignore # probably should filter a bit here
            self._connected = False

    def _try_connect_localgrpc(self) -> None:
        try:
            self._connect_to_dpf_using_mode(mode="LocalGrpc")
            self._connected = True
        except DPFServerException:  # type: ignore # probably should filter a bit here
            self._connected = False

    def _try_connect_remote_grpc(self, dpf_ip: str, dpf_port: int) -> None:
        try:
            self._connect_to_dpf_using_mode(
                mode="RemoteGrpc", external_ip=dpf_ip, external_port=dpf_port
            )
            self._connected = True
            self._is_remote = True
        except DPFServerException:  # type: ignore
            self._connected = False

    def _iterate_connections(self, dpf_ip: str, dpf_port: int) -> None:

        if not self._connected:
            self._try_connect_inprocess()

        if not self._connected:
            self._try_connect_localgrpc()

        if not self._connected:
            self._try_connect_remote_grpc(dpf_ip, dpf_port)

        if self._connected:
            return
        else:
            raise DPFServerException(
                "Could not connect to DPF server after trying all the available options."
            )

    def _set_dpf_env_vars(
        self, ip: str | None = None, port: int | None = None
    ) -> tuple[str, int]:
        if ip is not None:
            dpf_ip = ip
        elif "DPF_IP" in os.environ:
            dpf_ip = os.environ["DPF_IP"]
        elif self.mapdl:
            dpf_ip = self.mapdl.ip
        else:
            dpf_ip = "127.0.0.1"

        if port is not None:
            dpf_port = port
        elif "DPF_PORT" in os.environ:
            dpf_port = int(os.environ["DPF_PORT"])
        elif self.mapdl:
            dpf_port = self.mapdl.port + 3
        else:
            dpf_port = 50055

        return dpf_ip, dpf_port

    def _connect_to_dpf(self, ip: str, port: int) -> None:

        if not self._mode_rst and self._mapdl and not self._mapdl.is_local:
            self._try_connect_remote_grpc(ip, port)

        else:
            # any connection method is supported because the file local.
            self._iterate_connections(ip, port)

    def connect_to_server(self, ip: str | None = None, port: int | None = None) -> None:
        """
        Connect to the DPF Server.


        Parameters
        ----------
        ip : str, optional
            IP address of the server, by default "127.0.0.1"
        port : int, optional
            Server Port, by default 50054

        Returns
        -------
        dpf.server_types.GrpcServer
            Return the server connection.

        Raises
        ------
        MapdlRuntimeError
            If it cannot connect to an instance at the specified IP and port.

        Notes
        -----
        You can also set the ``ip`` and ``port`` values using the environment variables
        ``DPF_PORT`` and ``DPF_IP``.
        In case these variables are set, and the inputs of this function are not ``None``,
        the priority order is:

        1. Values supplied to this function.
        2. The environment variables
        3. The MAPDL stored values (if working on MAPDL mode)
        3. The default values

        """

        ip, port = self._set_dpf_env_vars(ip, port)
        check_valid_ip(ip)

        self.logger.debug(f"Attempting to connect to DPF server using: {ip}:{port}")

        self._connect_to_dpf(ip, port)

    def _dpf_remote_envvars(self):
        """Return True if any of the env variables are set"""
        return "DPF_IP" in os.environ or "DPF_PORT" in os.environ

    @property
    def is_remote(self) -> bool:
        """Returns True if we are connected to the DPF Server using a gRPC connection to a remote IP."""
        return self._is_remote

    @property
    def _mapdl(self) -> "Mapdl | None":
        """Return the weakly referenced instance of MAPDL"""
        if self._mapdl_weakref:
            return self._mapdl_weakref()

    @property
    def mapdl(self):
        """Return the MAPDL instance"""
        return self._mapdl

    @property
    def _log(self) -> Logger:
        """Alias for mapdl logger"""
        if self._mapdl:
            return self._mapdl._log
        else:
            if self._logger is None:
                self._logger = Logger(
                    level=logging.ERROR, to_file=False, to_stdout=True
                )
            return self._logger

    @property
    def logger(self) -> Logger:
        """Logger property"""
        return self._log

    @logger.setter
    def logger(self, logger: Logger) -> None:
        if self.mode_mapdl:
            raise ValueError(
                "Cannot set logger in MAPDL mode. Use the MAPDL instance methods to set the logger instead."
            )
        else:
            self._logger = logger

    @property
    def mode(self):
        if self._mode_rst:
            return "RST"
        else:
            return "MAPDL"

    @property
    def mode_rst(self):
        if self._mode_rst:
            return True
        else:
            return False

    @property
    def mode_mapdl(self):
        if not self._mode_rst:
            return True
        else:
            return False

    @property
    def same_machine(self):
        """True if the DPF server is running on the same machine as MAPDL"""
        if self.is_remote:
            # Some logic should be added here for cases where DPF is in different
            # remote machine than MAPDL.
            return True
        else:
            return True

    @property
    def _is_thermal(self):
        """Return True if there are TEMP DOF in the solution."""
        return hasattr(self.model.results, "temperature")

    @property
    def _is_distributed(self):
        # raise NotImplementedError("To be implemented by DPF")
        return False  # Hardcoded until DPF exposure

    @property
    def is_distributed(self):
        """True when this result file is part of a distributed result

        Only True when Global number of nodes does not equal the
        number of nodes in this file.

        Notes
        -----
        Not a reliabile indicator if a cyclic result.
        """
        return self._is_distributed

    @property
    def _rst(self):
        return os.path.join(self._rst_directory, self._rst_name)

    @property
    def local(self):
        if self._mapdl:
            return self._mapdl.is_local

    @property
    def _rst_directory(self) -> str:
        if self.mode_mapdl:
            # Update
            if self._mapdl is None:
                raise ValueError("MAPDL instance is None")

            if self.local:
                self.__rst_directory: str = self._mapdl.directory  # type: ignore

            else:
                self.__rst_directory: str = os.path.join(  # type: ignore
                    tempfile.gettempdir(), random_string()
                )
                if not os.path.exists(self.__rst_directory):
                    os.mkdir(self.__rst_directory)

        return self.__rst_directory  # type: ignore

    @property
    def _rst_name(self) -> str:
        return self.__rst_name

    def update(
        self, progress_bar: bool | None = None, chunk_size: int | None = None
    ) -> None:
        """Update the DPF Model.

        It does trigger an update on the underlying RST file.

        Parameters
        ----------
        progress_bar : _type_, optional
            Show progress br, by default None
        chunk_size : _type_, optional
            _description_, by default None

        Returns
        -------
        _type_
            _description_
        """
        return self._update(progress_bar=progress_bar, chunk_size=chunk_size)

    def _update(
        self, progress_bar: bool | None = None, chunk_size: int | None = None
    ) -> None:
        if self._mapdl:
            self._update_rst(progress_bar=progress_bar, chunk_size=chunk_size)

        # Upload it to DPF if we are not in local
        if self.is_remote and not self.same_machine:
            # self.connect_to_server()
            self._upload_to_dpf()

        # Updating model
        self._build_dpf_object()

        # Resetting flag
        self._loaded = True
        self._update_required = False

    def _upload_to_dpf(self):
        if self.same_machine:
            self._server_file_path = os.path.join(
                self._mapdl.directory, self._mapdl.result_file
            )
        else:
            # Upload to DPF is broken on Ubuntu: https://github.com/ansys/pydpf-core/issues/2254
            # self._server_file_path = dpf.upload_file_in_tmp_folder(self._rst)
            raise NotImplementedError(
                "Uploading to DPF is not implemented yet. "
                "Please use the local mode for now."
            )

    def _update_rst(
        self,
        progress_bar: bool | None = None,
        chunk_size: int | None = None,
        save: bool = True,
    ) -> None:
        # Saving model
        if save:
            self._mapdl.save()  # type: ignore

        if self.local is False:
            self._log.debug("Updating the local copy of remote RST file.")
            # download file
            self._mapdl.download(  # type: ignore
                self._rst_name,
                self._rst_directory,
                progress_bar=progress_bar,
                chunk_size=chunk_size,
            )

    def _build_dpf_object(self):
        if self._log:
            self._log.debug("Building/Updating DPF Model object.")

        if self.is_remote:
            self._cached_dpf_model = Model(self._server_file_path)
        else:
            self._cached_dpf_model = Model(self._rst)

    @property
    def model(self):
        """Returns the DPF model object."""
        if self._cached_dpf_model is None or self._update_required:
            self._update()

        return self._cached_dpf_model

    @property
    def metadata(self) -> "dpf.model.Metadata":
        return self.model.metadata

    @property
    def mesh(self) -> "dpf.MeshedRegion":
        """Mesh from result file."""
        # TODO: this should be a class equivalent to reader.mesh class.
        return self.model.metadata.meshed_region

    @property
    def grid(self) -> "pv.UnstructuredGrid":
        return self.mesh.grid

    def _get_entities_ids(
        self,
        entities: str | int | float | Iterable[str | int | float],
        entity_type: str = "Nodal",
    ) -> Iterable[int | float]:
        """Get entities ids given their ids, or component names.

        If a list is given it checks can be int, floats, or list/tuple of int/floats, or
        components (strs, or iterable[strings])

        Parameters
        ----------
        entities : str | int | float | Iterable[str | int | float]
            Entities ids or components

        entity_type : str, optional
            Type of entity, by default "Nodal"

        Returns
        -------
        list
            List of entities ids.

        Raises
        ------
        ValueError
            The argument 'entity_type' can only be 'Nodal' or 'Elemental'
        TypeError
            Only ints, floats, strings or iterable of the previous ones are allowed.
        ValueError
            The named selection '{each_named_selection}' does not exist.
        ValueError
            The named selection '{each_named_selection}' does not contain {entity_type} information.
        """
        if entity_type.lower() not in ["nodal", "elemental"]:
            raise ValueError(
                "The argument 'entity_type' can only be 'Nodal' or 'Elemental'. "
            )
        else:
            entity_type = entity_type.title()  # Sanity check

        if entities is None:
            return entities

        elif isinstance(entities, (int, float, str)):
            entities = [entities]

        if isinstance(entities, Iterable):  # type: ignore
            if all([isinstance(each, (int, float)) for each in entities]):
                return entities  # type: ignore
            elif all([isinstance(each, str) for each in entities]):
                # Need to map the components to the ids.
                pass
            else:
                raise ValueError("Strings and numbers are not allowed together.")

        else:
            raise TypeError(
                "Only ints, floats, strings or iterable of the previous ones are allowed."
            )

        # For components selections:
        entities_: list[int] = []
        available_ns: list[str] = self.mesh.available_named_selections

        for each_named_selection in entities:
            if each_named_selection not in available_ns:
                raise ValueError(
                    f"The named selection '{each_named_selection}' does not exist."
                )

            scoping = self.mesh.named_selection(each_named_selection)
            if scoping.location != entity_type:
                raise ValueError(
                    f"The named selection '{each_named_selection}' does not contain {entity_type} information."
                )

            entities_.append(scoping.ids.tolist())

        return entities_

    def _get_principal(self, op: "dpf.Operator") -> np.ndarray[Any, Any]:
        fc: dpf.FieldsContainer = op.outputs.fields_as_fields_container()[
            0
        ]  # This index 0 is the step indexing.

        op1 = dpf.operators.invariant.principal_invariants()
        op1.inputs.field.connect(fc)
        # Get output data
        result_field_eig_1 = op.outputs.field_eig_1()
        result_field_eig_2 = op.outputs.field_eig_2()
        result_field_eig_3 = op.outputs.field_eig_3()

        op2 = dpf.operators.invariant.invariants()
        op2.inputs.field.connect(fc)

        # Get output data
        result_field_int = op.outputs.field_int()
        result_field_eqv = op.outputs.field_eqv()
        # result_field_max_shear = op.outputs.field_max_shear()

        return np.hstack(
            (
                result_field_eig_1,
                result_field_eig_2,
                result_field_eig_3,
                result_field_int,
                result_field_eqv,
            )
        )

    def _extract_data(
        self, op: "dpf.Operator"
    ) -> tuple[np.ndarray[Any, Any], np.ndarray[Any, Any]]:
        fc = op.outputs.fields_as_fields_container()[
            0
        ]  # This index 0 is the step indexing.

        # When we destroy the operator, we might lose access to the array, that is why we copy.
        ids = fc.scoping.ids.copy()
        data = fc.data.copy()
        return ids, data

    def _set_rescope(self, op: "dpf.Operator", scope_ids: list[int]) -> "dpf.Operator":
        fc = op.outputs.fields_container()

        rescope = dpf.operators.scoping.rescope()
        rescope.inputs.mesh_scoping(sorted(scope_ids))
        rescope.inputs.fields(fc)
        return rescope

    def _set_mesh_scoping(
        self,
        op: "dpf.Operator",
        mesh: "dpf.MeshedRegion",
        requested_location: Literal["nodal", "elemental_nodal", "elemental"],
        scope_ids: list[int] | None = None,
    ):

        scop = dpf.Scoping()
        requested_location = requested_location.lower()  # type: ignore

        if requested_location == "nodal":
            scop.location = dpf.locations.nodal
            if scope_ids:
                scop.ids = scope_ids
            else:
                scop.ids = mesh.nodes.scoping.ids

        elif requested_location == "elemental_nodal":
            if scope_ids:
                scop.ids = scope_ids
            else:
                scop.ids = mesh.elements.scoping.ids

        elif requested_location == "elemental":
            scop.location = dpf.locations.elemental
            if scope_ids:
                scop.ids = scope_ids
            else:
                scop.ids = mesh.elements.scoping.ids
        else:
            raise ValueError(
                f"The 'requested_location' value ({requested_location}) is not allowed."
            )
        op.inputs.mesh_scoping.connect(scop)
        return scop.ids

    def _set_element_results(self, op, mesh):

        fc = op.outputs.fields_container()

        op2 = dpf.operators.averaging.to_elemental_fc(collapse_shell_layers=True)
        op2.inputs.fields_container.connect(fc)
        op2.inputs.mesh.connect(mesh)

        return op2

    def _set_input_timestep_scope(self, op, rnum):

        if not rnum:
            rnum = [int(1)]
        else:
            if isinstance(rnum, (int, float)):
                rnum = [rnum]
            elif isinstance(rnum, (list, tuple)):
                rnum = [self.parse_step_substep(rnum)]
            else:
                raise TypeError(
                    "Only 'int' and 'float' are supported to define the steps."
                )

        my_time_scoping = dpf.Scoping()
        my_time_scoping.location = "time_freq_steps"  # "time_freq"
        my_time_scoping.ids = rnum

        op.inputs.time_scoping.connect(my_time_scoping)

    def _get_operator(self, result_field):
        if not hasattr(self.model.results, result_field):
            list_results = "\n    ".join(
                [each for each in dir(self.model.results) if not each.startswith("_")]
            )
            raise ResultNotFound(
                f"The result '{result_field}' cannot be found on the RST file. "
                f"The current results are:\n    {list_results}"
            )

        # Getting field
        return getattr(self.model.results, result_field)()

    def _get_nodes_result(
        self,
        rnum,
        result_type,
        in_nodal_coord_sys=False,
        nodes=None,
        return_operator=False,
    ):
        return self._get_result(
            rnum,
            result_type,
            requested_location="Nodal",
            scope_ids=nodes,
            result_in_entity_cs=in_nodal_coord_sys,
            return_operator=return_operator,
        )

    def _get_elem_result(
        self,
        rnum,
        result_type,
        in_element_coord_sys=False,
        elements=None,
        return_operator=False,
    ):
        return self._get_result(
            rnum,
            result_type,
            requested_location="Elemental",
            scope_ids=elements,
            result_in_entity_cs=in_element_coord_sys,
            return_operator=return_operator,
        )

    def _get_elemnodal_result(
        self,
        rnum,
        result_type,
        in_element_coord_sys=False,
        elements=None,
        return_operator=False,
    ):
        return self._get_result(
            rnum,
            result_type,
            requested_location="Elemental_Nodal",
            scope_ids=elements,
            result_in_entity_cs=in_element_coord_sys,
            return_operator=return_operator,
        )

    @update_result
    def _get_result(
        self,
        rnum,
        result_field,
        requested_location="Nodal",
        scope_ids=None,
        result_in_entity_cs=False,
        return_operator=False,
    ):
        """
        Get elemental/nodal/elementalnodal results.

        Parameters
        ----------
        rnum : int
            Result step/set
        result_field : str
            Result type, for example "stress", "strain", "displacement", etc.
        requested_location : str, optional
            Results given at which type of entity, by default "Nodal"
        scope_ids : Union([int, floats, List[int]]), optional
            List of entities (nodal/elements) to get the results from, by default None
        result_in_entity_cs : bool, optional
            Obtain the results in the entity coordinate system, by default False
        return_operator : bool, optional
            Return the last used operator (most of the times it will be a Rescope operator).
            Defaults to ``False``.

        Returns
        -------
        np.array
            Ids of the entities (nodes or elements)
        np.array
            Values of the entities for the requested solution
        dpf.Operator
            If ``return_operator`` is ``True``, then it will return the last instantiated
            operator (most of the times a

            `Rescope operator<https://dpf.docs.pyansys.com/api/ansys.dpf.core.operators.scoping.rescope.html>`_

            :class:`rescope <ansys.dpf.core.operators.scoping.rescope.rescope>`
            .)

        Raises
        ------
        ResultNotFound
            The given result (stress, strain, ...) could not be found in the RST file.
        TypeError
            Only floats and ints are allowed to scope steps/time.
        NotImplementedError
            Component input selection is still not supported.
        """

        # todo: accepts components in nodes.
        mesh: dpf.MeshedRegion = self.metadata.meshed_region

        if isinstance(scope_ids, np.ndarray):
            scope_ids = scope_ids.tolist()

        op = self._get_operator(result_field)

        # CS output
        if not result_in_entity_cs:
            op.inputs.bool_rotate_to_global.connect(True)
        else:
            op.inputs.bool_rotate_to_global.connect(False)

        # Setting time steps
        self._set_input_timestep_scope(op, rnum)

        # getting the ids of the entities scope
        entity_type = "elemental" if "elemental" in requested_location else "nodal"
        scope_ids = self._get_entities_ids(scope_ids, requested_location)

        # Set type of return
        ids = self._set_mesh_scoping(op, mesh, requested_location, scope_ids)

        if requested_location.lower() == "elemental":
            op = self._set_element_results(
                op, mesh
            )  # overwrite op to be the elemental results OP

        # Applying rescope to make sure the order is right
        op = self._set_rescope(op, ids.astype(int).tolist())

        fc = op.outputs.fields_as_fields_container()[0]
        if fc.shell_layers is not dpf.shell_layers.nonelayer:
            # check
            pass

        if return_operator:
            return op
        else:
            return self._extract_data(op)

    def nodal_displacement(self, rnum, in_nodal_coord_sys=None, nodes=None):
        """Returns the DOF solution for each node in the global
        cartesian coordinate system or nodal coordinate system.

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        in_nodal_coord_sys : bool, optional
            When ``True``, returns results in the nodal coordinate
            system.  Default ``False``.

        nodes : str, sequence of int or str, optional
            Select a limited subset of nodes.  Can be a nodal
            component or array of node numbers.  For example

            * ``"MY_COMPONENT"``
            * ``['MY_COMPONENT', 'MY_OTHER_COMPONENT]``
            * ``np.arange(1000, 2001)``

        Returns
        -------
        nnum : int np.ndarray
            Node numbers associated with the results.

        result : float np.ndarray
            Array of nodal displacements.  Array
            is (``nnod`` x ``sumdof``), the number of nodes by the
            number of degrees of freedom which includes ``numdof`` and
            ``nfldof``

        Examples
        --------
        Return the nodal solution (in this case, displacement) for the
        first result of ``"file.rst"``

        >>> from ansys.mapdl.core.reader import DPFResult as Result
        >>> rst = Result('file.rst')
        >>> nnum, data = rst.nodal_solution(0)

        Return the nodal solution just for the nodal component
        ``'MY_COMPONENT'``.

        >>> nnum, data = rst.nodal_solution(0, nodes='MY_COMPONENT')

        Return the nodal solution just for the nodes from 20 through 50.

        >>> nnum, data = rst.nodal_solution(0, nodes=range(20, 51))

        Notes
        -----
        Some solution results may not include results for each node.
        These results are removed by and the node numbers of the
        solution results are reflected in ``nnum``.
        """
        return self._get_nodes_result(rnum, "displacement", in_nodal_coord_sys, nodes)

    def nodal_solution(self, rnum, in_nodal_coord_sys=None, nodes=None):
        """Returns the DOF solution for each node in the global
        cartesian coordinate system or nodal coordinate system.

        Solution may be nodal temperatures or nodal displacements
        depending on the type of the solution.

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        in_nodal_coord_sys : bool, optional
            When ``True``, returns results in the nodal coordinate
            system.  Default ``False``.

        nodes : str, sequence of int or str, optional
            Select a limited subset of nodes.  Can be a nodal
            component or array of node numbers.  For example

            * ``"MY_COMPONENT"``
            * ``['MY_COMPONENT', 'MY_OTHER_COMPONENT]``
            * ``np.arange(1000, 2001)``

        Returns
        -------
        nnum : int np.ndarray
            Node numbers associated with the results.

        result : float np.ndarray
            Array of nodal displacements or nodal temperatures.  Array
            is (``nnod`` x ``sumdof``), the number of nodes by the
            number of degrees of freedom which includes ``numdof`` and
            ``nfldof``

        Examples
        --------
        Return the nodal solution (in this case, displacement) for the
        first result of ``"file.rst"``

        >>> from ansys.mapdl.core.reader import DPFResult as Result
        >>> rst = Result('file.rst')
        >>> nnum, data = rst.nodal_solution(0)

        Return the nodal solution just for the nodal component
        ``'MY_COMPONENT'``.

        >>> nnum, data = rst.nodal_solution(0, nodes='MY_COMPONENT')

        Return the nodal solution just for the nodes from 20 through 50.

        >>> nnum, data = rst.nodal_solution(0, nodes=range(20, 51))

        Notes
        -----
        Some solution results may not include results for each node.
        These results are removed by and the node numbers of the
        solution results are reflected in ``nnum``.
        """

        if hasattr(self.model.results, "displacement"):
            return self.nodal_displacement(rnum, in_nodal_coord_sys, nodes)
        elif hasattr(self.model.results, "temperature"):
            return self.nodal_temperature(rnum, nodes)
        else:
            raise ResultNotFound(
                "The current analysis does not have 'displacement' or 'temperature' results."
            )

    def nodal_temperature(self, rnum, nodes=None):
        """Retrieves the temperature for each node in the
        solution.

        The order of the results corresponds to the sorted node
        numbering.

        Equivalent MAPDL command: PRNSOL, TEMP

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        nodes : str, sequence of int or str, optional
            Select a limited subset of nodes.  Can be a nodal
            component or array of node numbers.  For example

            * ``"MY_COMPONENT"``
            * ``['MY_COMPONENT', 'MY_OTHER_COMPONENT]``
            * ``np.arange(1000, 2001)``

        Returns
        -------
        nnum : numpy.ndarray
            Node numbers of the result.

        temperature : numpy.ndarray
            Temperature at each node.

        Examples
        --------
        >>> from ansys.mapdl.core.reader import DPFResult as Result
        >>> rst = Result('file.rst')
        >>> nnum, temp = rst.nodal_temperature(0)

        Return the temperature just for the nodal component
        ``'MY_COMPONENT'``.

        >>> nnum, temp = rst.nodal_stress(0, nodes='MY_COMPONENT')

        Return the temperature just for the nodes from 20 through 50.

        >>> nnum, temp = rst.nodal_solution(0, nodes=range(20, 51))

        """
        return self._get_nodes_result(rnum, "temperature", nodes)

    def nodal_voltage(self, rnum, in_nodal_coord_sys=None, nodes=None):
        """Retrieves the voltage for each node in the
        solution.

        The order of the results corresponds to the sorted node
        numbering.

        Equivalent MAPDL command: PRNSOL, VOLT

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        nodes : str, sequence of int or str, optional
            Select a limited subset of nodes.  Can be a nodal
            component or array of node numbers.  For example

            * ``"MY_COMPONENT"``
            * ``['MY_COMPONENT', 'MY_OTHER_COMPONENT]``
            * ``np.arange(1000, 2001)``

        Returns
        -------
        nnum : numpy.ndarray
            Node numbers of the result.

        voltage : numpy.ndarray
            voltage at each node.

        Examples
        --------
        >>> from ansys.mapdl.core.reader import DPFResult as Result
        >>> rst = Result('file.rst')
        >>> nnum, temp = rst.nodal_voltage(0)

        Return the voltage just for the nodal component
        ``'MY_COMPONENT'``.

        >>> nnum, temp = rst.nodal_stress(0, nodes='MY_COMPONENT')

        """
        return self._get_nodes_result(
            rnum, "electric_potential", in_nodal_coord_sys, nodes
        )

    def element_stress(
        self, rnum, principal=None, in_element_coord_sys=None, elements=None, **kwargs
    ):
        """Retrieves the element component stresses.

        Equivalent ANSYS command: PRESOL, S

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        principal : bool, optional
            Returns principal stresses instead of component stresses.
            Default False.

        in_element_coord_sys : bool, optional
            Returns the results in the element coordinate system.
            Default False and will return the results in the global
            coordinate system.

        elements : str, sequence of int or str, optional
            Select a limited subset of elements.  Can be a element
            component or array of element numbers.  For example

            * ``"MY_COMPONENT"``
            * ``['MY_COMPONENT', 'MY_OTHER_COMPONENT]``
            * ``np.arange(1000, 2001)``

        **kwargs : optional keyword arguments
            Hidden options for distributed result files.

        Returns
        -------
        enum : np.ndarray
            ANSYS element numbers corresponding to each element.

        element_stress : list
            Stresses at each element for each node for Sx Sy Sz Sxy
            Syz Sxz or SIGMA1, SIGMA2, SIGMA3, SINT, SEQV when
            principal is True.

        enode : list
            Node numbers corresponding to each element's stress
            results.  One list entry for each element.

        Examples
        --------
        Element component stress for the first result set.

        >>> rst.element_stress(0)

        Element principal stress for the first result set.

        >>> enum, element_stress, enode = result.element_stress(0, principal=True)

        Notes
        -----
        Shell stresses for element 181 are returned for top and bottom
        layers.  Results are ordered such that the top layer and then
        the bottom layer is reported.
        """
        if principal:
            op = self._get_elem_result(
                rnum,
                "stress",
                in_element_coord_sys=in_element_coord_sys,
                elements=elements,
                return_operator=True,
                **kwargs,
            )
            return self._get_principal(op)
        else:
            return self._get_elem_result(
                rnum, "stress", in_element_coord_sys, elements, **kwargs
            )

    def element_nodal_stress(
        self, rnum, principal=None, in_element_coord_sys=None, elements=None, **kwargs
    ):
        """Retrieves the nodal stresses for each element.

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a list containing
            (step, substep) of the requested result.

        principal : bool, optional
            Returns principal stresses instead of component stresses.
            Default False.

        in_element_coord_sys : bool, optional
            Returns the results in the element coordinate system if ``True``.
            Else, it returns the results in the global coordinate system.
            Default False

        elements : str, sequence of int or str, optional
            Select a limited subset of elements.  Can be a element
            component or array of element numbers.  For example:

            * ``"MY_COMPONENT"``
            * ``['MY_COMPONENT', 'MY_OTHER_COMPONENT]``
            * ``np.arange(1000, 2001)``

        **kwargs : optional keyword arguments
            Hidden options for distributed result files.

        Returns
        -------
        enum : np.ndarray
            ANSYS element numbers corresponding to each element.

        element_stress : list
            Stresses at each element for each node for Sx Sy Sz Sxy
            Syz Sxz or SIGMA1, SIGMA2, SIGMA3, SINT, SEQV when
            principal is True.

        enode : list
            Node numbers corresponding to each element's stress
            results.  One list entry for each element.

        Examples
        --------
        Element component stress for the first result set.

        >>> rst.element_stress(0)

        Element principal stress for the first result set.

        >>> enum, element_stress, enode = result.element_stress(0, principal=True)

        Notes
        -----
        Shell stresses for element 181 are returned for top and bottom
        layers.  Results are ordered such that the top layer and then
        the bottom layer is reported.
        """
        if principal:
            op = self._get_elemnodal_result(
                rnum,
                "stress",
                in_element_coord_sys=in_element_coord_sys,
                elements=elements,
                return_operator=True,
                **kwargs,
            )
            return self._get_principal(op)
        else:
            return self._get_elemnodal_result(
                rnum, "stress", in_element_coord_sys, elements, **kwargs
            )

    def nodal_elastic_strain(self, rnum, in_nodal_coord_sys=False, nodes=None):
        """Nodal component elastic strains.  This record contains
        strains in the order ``X, Y, Z, XY, YZ, XZ, EQV``.

        Elastic strains can be can be nodal values extrapolated from
        the integration points or values at the integration points
        moved to the nodes.

        Equivalent MAPDL command: ``PRNSOL, EPEL``

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        nodes : str, sequence of int or str, optional
            Select a limited subset of nodes.  Can be a nodal
            component or array of node numbers.  For example

            * ``"MY_COMPONENT"``
            * ``['MY_COMPONENT', 'MY_OTHER_COMPONENT]``
            * ``np.arange(1000, 2001)``

        Returns
        -------
        nnum : np.ndarray
            MAPDL node numbers.

        elastic_strain : np.ndarray
            Nodal component elastic strains.  Array is in the order
            ``X, Y, Z, XY, YZ, XZ, EQV``.

            .. versionchanged:: 0.64
                The nodes with no values are now equals to zero.
                The results of the midnodes are also calculated and
                presented.

        Examples
        --------
        Load the nodal elastic strain for the first result.

        >>> from ansys.mapdl.core.reader import DPFResult as Result
        >>> rst = Result('file.rst')
        >>> nnum, elastic_strain = rst.nodal_elastic_strain(0)

        Return the nodal elastic strain just for the nodal component
        ``'MY_COMPONENT'``.

        >>> nnum, elastic_strain = rst.nodal_elastic_strain(0, nodes='MY_COMPONENT')

        Return the nodal elastic strain just for the nodes from 20 through 50.

        >>> nnum, elastic_strain = rst.nodal_elastic_strain(0, nodes=range(20, 51))

        Notes
        -----
        Nodes without a strain will be NAN.

        ..
        """
        return self._get_nodes_result(
            rnum, "elastic_strain", in_nodal_coord_sys=in_nodal_coord_sys, nodes=nodes
        )

    def nodal_plastic_strain(self, rnum, in_nodal_coord_sys=False, nodes=None):
        """Nodal component plastic strains.

        This record contains strains in the order:
        ``X, Y, Z, XY, YZ, XZ, EQV``.

        Plastic strains are always values at the integration points
        moved to the nodes.

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        nodes : str, sequence of int or str, optional
            Select a limited subset of nodes.  Can be a nodal
            component or array of node numbers.  For example

            * ``"MY_COMPONENT"``
            * ``['MY_COMPONENT', 'MY_OTHER_COMPONENT]``
            * ``np.arange(1000, 2001)``

        Returns
        -------
        nnum : np.ndarray
            MAPDL node numbers.

        plastic_strain : np.ndarray
            Nodal component plastic strains.  Array is in the order
            ``X, Y, Z, XY, YZ, XZ, EQV``.

        Examples
        --------
        Load the nodal plastic strain for the first solution.

        >>> from ansys.mapdl.core.reader import DPFResult as Result
        >>> rst = Result('file.rst')
        >>> nnum, plastic_strain = rst.nodal_plastic_strain(0)

        Return the nodal plastic strain just for the nodal component
        ``'MY_COMPONENT'``.

        >>> nnum, plastic_strain = rst.nodal_plastic_strain(0, nodes='MY_COMPONENT')

        Return the nodal plastic strain just for the nodes from 20
        through 50.

        >>> nnum, plastic_strain = rst.nodal_plastic_strain(0, nodes=range(20, 51))

        """
        return self._get_nodes_result(rnum, "plastic_strain", in_nodal_coord_sys, nodes)

    def nodal_acceleration(self, rnum, in_nodal_coord_sys=None, nodes=None):
        """Nodal velocities for a given result set.

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        in_nodal_coord_sys : bool, optional
            When ``True``, returns results in the nodal coordinate
            system.  Default False.

        Returns
        -------
        nnum : int np.ndarray
            Node numbers associated with the results.

        result : float np.ndarray
            Array of nodal accelerations.  Array is (``nnod`` x
            ``sumdof``), the number of nodes by the number of degrees
            of freedom which includes ``numdof`` and ``nfldof``

        Examples
        --------
        >>> from ansys.mapdl.core.reader import DPFResult as Result
        >>> rst = Result('file.rst')
        >>> nnum, data = rst.nodal_acceleration(0)

        Notes
        -----
        Some solution results may not include results for each node.
        These results are removed by and the node numbers of the
        solution results are reflected in ``nnum``.
        """
        return self._get_nodes_result(rnum, "acceleration", in_nodal_coord_sys, nodes)

    def nodal_reaction_forces(self, rnum, in_nodal_coord_sys=False, nodes=None):
        """Nodal reaction forces.

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        Returns
        -------
        rforces : np.ndarray
            Nodal reaction forces for each degree of freedom.

        nnum : np.ndarray
            Node numbers corresponding to the reaction forces.  Node
            numbers may be repeated if there is more than one degree
            of freedom for each node.

        dof : np.ndarray
            Degree of freedom corresponding to each node using the
            MAPDL degree of freedom reference table.  See
            ``rst.result_dof`` for the corresponding degrees of
            freedom for a given solution.

        Examples
        --------
        Get the nodal reaction forces for the first result and print
        the reaction forces of a single node.

        >>> from ansys.mapdl.core.reader import DPFResult as Result
        >>> rst = Result('file.rst')
        >>> rforces, nnum, dof = rst.nodal_reaction_forces(0)
        >>> dof_ref = rst.result_dof(0)
        >>> rforces[:3], nnum[:3], dof[:3], dof_ref
        (array([  24102.21376091, -109357.01854005,   22899.5303263 ]),
         array([4142, 4142, 4142]),
         array([1, 2, 3], dtype=int32),
         ['UX', 'UY', 'UZ'])

        """
        return self._get_nodes_result(rnum, "reaction_force", in_nodal_coord_sys, nodes)

    def nodal_stress(self, rnum, in_nodal_coord_sys=False, nodes=None):
        """Retrieves the component stresses for each node in the
        solution.

        The order of the results corresponds to the sorted node
        numbering.

        Computes the nodal stress by averaging the stress for each
        element at each node.  Due to the discontinuities across
        elements, stresses will vary based on the element they are
        evaluated from.

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        nodes : str, sequence of int or str, optional
            Select a limited subset of nodes.  Can be a nodal
            component or array of node numbers.  For example

            * ``"MY_COMPONENT"``
            * ``['MY_COMPONENT', 'MY_OTHER_COMPONENT]``
            * ``np.arange(1000, 2001)``

        Returns
        -------
        nnum : numpy.ndarray
            Node numbers of the result.

        stress : numpy.ndarray
            Stresses at ``X, Y, Z, XY, YZ, XZ`` averaged at each corner
            node.

        Examples
        --------
        >>> from ansys.mapdl.core.reader import DPFResult as Result
        >>> rst = Result('file.rst')
        >>> nnum, stress = rst.nodal_stress(0)

        Return the nodal stress just for the nodal component
        ``'MY_COMPONENT'``.

        >>> nnum, stress = rst.nodal_stress(0, nodes='MY_COMPONENT')

        Return the nodal stress just for the nodes from 20 through 50.

        >>> nnum, stress = rst.nodal_solution(0, nodes=range(20, 51))

        Notes
        -----
        Nodes without a stress value will be NAN.
        Equivalent ANSYS command: PRNSOL, S
        """
        return self._get_nodes_result(rnum, "stress", in_nodal_coord_sys, nodes)

    def nodal_thermal_strain(self, rnum, in_nodal_coord_sys=False, nodes=None):
        """Nodal component thermal strain.

        This record contains strains in the order X, Y, Z, XY, YZ, XZ,
        EQV, and eswell (element swelling strain).  Thermal strains
        are always values at the integration points moved to the
        nodes.

        Equivalent MAPDL command: PRNSOL, EPTH, COMP

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        nodes : str, sequence of int or str, optional
            Select a limited subset of nodes.  Can be a nodal
            component or array of node numbers.  For example

            * ``"MY_COMPONENT"``
            * ``['MY_COMPONENT', 'MY_OTHER_COMPONENT]``
            * ``np.arange(1000, 2001)``

        Returns
        -------
        nnum : np.ndarray
            MAPDL node numbers.

        thermal_strain : np.ndarray
            Nodal component plastic strains.  Array is in the order
            ``X, Y, Z, XY, YZ, XZ, EQV, ESWELL``

        Examples
        --------
        Load the nodal thermal strain for the first solution.

        >>> from ansys.mapdl.core.reader import DPFResult as Result
        >>> rst = Result('file.rst')
        >>> nnum, thermal_strain = rst.nodal_thermal_strain(0)

        Return the nodal thermal strain just for the nodal component
        ``'MY_COMPONENT'``.

        >>> nnum, thermal_strain = rst.nodal_thermal_strain(0, nodes='MY_COMPONENT')

        Return the nodal thermal strain just for the nodes from 20 through 50.

        >>> nnum, thermal_strain = rst.nodal_thermal_strain(0, nodes=range(20, 51))
        """
        return self._get_nodes_result(rnum, "thermal_strain", in_nodal_coord_sys, nodes)

    def nodal_velocity(self, rnum, in_nodal_coord_sys=False, nodes=None):
        """Nodal velocities for a given result set.

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        in_nodal_coord_sys : bool, optional
            When ``True``, returns results in the nodal coordinate
            system.  Default False.

        Returns
        -------
        nnum : int np.ndarray
            Node numbers associated with the results.

        result : float np.ndarray
            Array of nodal velocities.  Array is (``nnod`` x
            ``sumdof``), the number of nodes by the number of degrees
            of freedom which includes ``numdof`` and ``nfldof``

        Examples
        --------
        >>> from ansys.mapdl.core.reader import DPFResult as Result
        >>> rst = Result('file.rst')
        >>> nnum, data = rst.nodal_velocity(0)

        Notes
        -----
        Some solution results may not include results for each node.
        These results are removed by and the node numbers of the
        solution results are reflected in ``nnum``.
        """
        return self._get_nodes_result(rnum, "velocity", in_nodal_coord_sys, nodes)

    def nodal_static_forces(self, rnum, in_nodal_coord_sys=False, nodes=None):
        """Return the nodal forces averaged at the nodes.

        Nodal forces are computed on an element by element basis, and
        this method averages the nodal forces for each element for
        each node.

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        nodes : str, sequence of int or str, optional
            Select a limited subset of nodes.  Can be a nodal
            component or array of node numbers.  For example

            * ``"MY_COMPONENT"``
            * ``['MY_COMPONENT', 'MY_OTHER_COMPONENT]``
            * ``np.arange(1000, 2001)``

        Returns
        -------
        nnum : np.ndarray
            MAPDL node numbers.

        forces : np.ndarray
           Averaged nodal forces.  Array is sized ``[nnod x numdof]``
           where ``nnod`` is the number of nodes and ``numdof`` is the
           number of degrees of freedom for this solution.

        Examples
        --------
        Load the nodal static forces for the first result using the
        example hexahedral result file.

        >>> from ansys.mapdl import reader as pymapdl_reader
        >>> from ansys.mapdl.reader import examples
        >>> rst = pymapdl_reader.read_binary(examples.rstfile)
        >>> nnum, forces = rst.nodal_static_forces(0)

        Return the nodal static forces just for the nodal component
        ``'MY_COMPONENT'``.

        >>> nnum, forces = rst.nodal_static_forces(0, nodes='MY_COMPONENT')

        Return the nodal static forces just for the nodes from 20 through 50.

        >>> nnum, forces = rst.nodal_static_forces(0, nodes=range(20, 51))

        Notes
        -----
        Nodes without a a nodal will be NAN.  These are generally
        midside (quadratic) nodes.
        """
        return self._get_nodes_result(rnum, "nodal_force", in_nodal_coord_sys, nodes)

    def principal_nodal_stress(self, rnum, in_nodal_coord_sys=False, nodes=None):
        """Computes the principal component stresses for each node in
        the solution.

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        Returns
        -------
        nodenum : numpy.ndarray
            Node numbers of the result.

        pstress : numpy.ndarray
            Principal stresses, stress intensity, and equivalent stress.
            [sigma1, sigma2, sigma3, sint, seqv]

        Examples
        --------
        Load the principal nodal stress for the first solution.

        >>> from ansys.mapdl.core.reader import DPFResult as Result
        >>> rst = Result('file.rst')
        >>> nnum, stress = rst.principal_nodal_stress(0)

        Notes
        -----
        ANSYS equivalent of:
        PRNSOL, S, PRIN

        which returns:
        S1, S2, S3 principal stresses, SINT stress intensity, and SEQV
        equivalent stress.

        Internal averaging algorithm averages the component values
        from the elements at a common node and then calculates the
        principal using the averaged value.

        See the MAPDL ``AVPRIN`` command for more details.
        ``ansys-mapdl-reader`` uses the default ``AVPRIN, 0`` option.

        """
        op = self._get_nodes_result(
            rnum,
            "stress",
            in_nodal_coord_sys=in_nodal_coord_sys,
            nodes=nodes,
            return_operator=True,
        )
        return self._get_principal(op)

    @property
    def n_results(self):
        """Number of results"""
        return self.model.metadata.result_info.n_results

    @property
    def filename(self) -> str:
        """String form of the filename. This property is read-only."""
        return self._rst  # in the reader, this contains the complete path.

    @property
    def pathlib_filename(self) -> pathlib.Path:
        """Return the ``pathlib.Path`` version of the filename. This property can not be set."""
        return pathlib.Path(self._rst)

    def nsets(self):
        return self.metadata.time_freq_support.n_sets

    def parse_step_substep(self, user_input):
        """Converts (step, substep) to a cumulative index"""
        if isinstance(user_input, int):
            return self.metadata.time_freq_support.get_cumulative_index(
                user_input
            )  # 0 based indexing

        elif isinstance(user_input, (list, tuple)):
            return self.metadata.time_freq_support.get_cumulative_index(
                user_input[0], user_input[1]
            )

        else:
            raise TypeError("Input must be either an int or a list")

    @property
    def version(self):
        """The version of MAPDL used to generate this result file.

        Examples
        --------
        >>> mapdl.result.version
        20.1
        """
        return float(self.model.metadata.result_info.solver_version)

    @property
    def available_results(self):
        """Available result types.

        .. versionchanged:: 0.64
           From 0.64, the MAPDL data labels (i.e. NSL for nodal displacements,
           ENS for nodal stresses, etc) are not included in the output of this command.

        Examples
        --------
        >>> mapdl.result.available_results
        Available Results:
        Nodal Displacement
        Nodal Velocity
        Nodal Acceleration
        Nodal Force
        ElementalNodal Element nodal Forces
        ElementalNodal Stress
        Elemental Volume
        Elemental Energy-stiffness matrix
        Elemental Hourglass Energy
        Elemental thermal dissipation energy
        Elemental Kinetic Energy
        Elemental co-energy
        Elemental incremental energy
        ElementalNodal Strain
        ElementalNodal Thermal Strains
        ElementalNodal Thermal Strains eqv
        ElementalNodal Swelling Strains
        ElementalNodal Temperature
        Nodal Temperature
        ElementalNodal Heat flux
        ElementalNodal Heat flux
        """
        text = "Available Results:\n"
        for each_available_result in self.model.metadata.result_info.available_results:
            text += (  # TODO: Missing label data NSL, VSL, etc
                each_available_result.native_location
                + " "
                + each_available_result.physical_name
                + "\n"
            )
        return text

    @property
    def n_sector(self):
        """Number of sectors"""
        if self.model.metadata.result_info.has_cyclic:
            return self.model.metadata.result_info.cyclic_support.num_sectors()

    @property
    def num_stages(self):
        """Number of cyclic stages in the model"""
        if self.model.metadata.result_info.has_cyclic:
            return self.model.metadata.result_info.cyclic_support.num_stages

    @property
    def title(self):
        """Title of model in database"""
        return self.model.metadata.result_info.main_title

    @property
    def is_cyclic(self):
        return self.model.metadata.result_info.has_cyclic

    @property
    def units(self):
        return self.model.metadata.result_info.unit_system_name

    def __repr__(self):
        if self.is_distributed:
            rst_info = ["PyMAPDL Reader Distributed Result"]
        else:
            rst_info = ["PyMAPDL Result"]

        rst_info.append("{:<12s}: {:s}".format("title".capitalize(), self.title))
        # rst_info.append("{:<12s}: {:s}".format("subtitle".capitalize(), self.subtitle)) #TODO: subtitle is not implemented in DPF.
        rst_info.append("{:<12s}: {:s}".format("units".capitalize(), self.units))

        rst_info.append("{:<12s}: {}".format("Version", self.version))
        rst_info.append("{:<12s}: {}".format("Cyclic", self.is_cyclic))
        rst_info.append("{:<12s}: {:d}".format("Result Sets", self.nsets))

        rst_info.append("{:<12s}: {:d}".format("Nodes", self.mesh.nodes.n_nodes))
        rst_info.append(
            "{:<12s}: {:d}".format("Elements", self.mesh.elements.n_elements)
        )

        rst_info.append("\n")
        rst_info.append(self.available_results)
        return "\n".join(rst_info)

    def nodal_time_history(self, solution_type="NSL", in_nodal_coord_sys=None):
        """The DOF solution for each node for all result sets.

        The nodal results are returned returned in the global
        cartesian coordinate system or nodal coordinate system.

        Parameters
        ----------
        solution_type: str, optional
            The solution type.  Must be either nodal displacements
            (``'NSL'``), nodal velocities (``'VEL'``) or nodal
            accelerations (``'ACC'``).

        in_nodal_coord_sys : bool, optional
            When ``True``, returns results in the nodal coordinate system.
            Default ``False``.

        Returns
        -------
        nnum : int np.ndarray
            Node numbers associated with the results.

        result : float np.ndarray
            Nodal solution for all result sets.  Array is sized
            ``rst.nsets x nnod x Sumdof``, which is the number of
            time steps by number of nodes by degrees of freedom.
        """
        if not isinstance(solution_type, str):
            raise TypeError("Solution type must be a string")

        if solution_type == "NSL":
            func = self.nodal_solution
        elif solution_type == "VEL":
            func = self.nodal_velocity
        elif solution_type == "ACC":
            func = self.nodal_acceleration
        else:
            raise ValueError(
                "Argument 'solution type' must be either 'NSL', " "'VEL', or 'ACC'"
            )

        # size based on the first result
        nnum, sol = func(0, in_nodal_coord_sys)
        data = np.empty((self.nsets, sol.shape[0], sol.shape[1]), np.float64)
        data[0] = sol
        for i in range(1, self.nsets):
            data[i] = func(i, in_nodal_coord_sys)[1]

        return nnum, data

    def element_components(self):
        """Dictionary of ansys element components from the result file.

        Examples
        --------
        >>> from ansys.mapdl import reader as pymapdl_reader
        >>> from ansys.mapdl.reader import examples
        >>> rst = pymapdl_reader.read_binary(examples.rstfile)
        >>> rst.element_components
        {'ECOMP1': array([17, 18, 21, 22, 23, 24, 25, 26, 27, 28, 29,
                30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40], dtype=int32),
        'ECOMP2': array([ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13,
                14, 15, 16, 17, 18, 19, 20, 23, 24], dtype=int32),
        'ELEM_COMP': array([ 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
                16, 17, 18, 19, 20], dtype=int32)}
        """
        element_components_ = {}
        for each_named_selection in self.mesh.available_named_selections:
            scoping = self.mesh.named_selection(each_named_selection)
            element_components_[each_named_selection] = np.array(
                scoping.ids, dtype=np.int32
            )

        return element_components_

    @property
    def time_values(self):
        "Values for the time/frequency"
        return self.metadata.time_freq_support.time_frequencies.data_as_list

    def plot_nodal_stress(
        self,
        rnum,
        comp=None,
        show_displacement=False,
        displacement_factor=1,
        node_components=None,
        element_components=None,
        sel_type_all=True,
        treat_nan_as_zero=True,
        **kwargs,
    ):
        """Plots the stresses at each node in the solution.

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        comp : str, optional
            Stress component to display.  Available options:
            - ``"X"``
            - ``"Y"``
            - ``"Z"``
            - ``"XY"``
            - ``"YZ"``
            - ``"XZ"``

        node_components : list, optional
            Accepts either a string or a list strings of node
            components to plot.  For example:
            ``['MY_COMPONENT', 'MY_OTHER_COMPONENT]``

        element_components : list, optional
            Accepts either a string or a list strings of element
            components to plot.  For example:
            ``['MY_COMPONENT', 'MY_OTHER_COMPONENT]``

        sel_type_all : bool, optional
            If node_components is specified, plots those elements
            containing all nodes of the component.  Default ``True``.

        treat_nan_as_zero : bool, optional
            Treat NAN values (i.e. stresses at midside nodes) as zero
            when plotting.

        kwargs : keyword arguments
            Additional keyword arguments.  See ``help(pyvista.plot)``

        Returns
        -------
        cpos : list
            3 x 3 vtk camera position.

        Examples
        --------
        Plot the X component nodal stress while showing displacement.

        >>> rst.plot_nodal_stress(0, comp='x', show_displacement=True)
        """
        if not comp:
            comp = "X"

        ind = COMPONENTS.index(comp)

        op = self._get_nodes_result(
            rnum,
            "stress",
            nodes=node_components,
            in_nodal_coord_sys=False,
            return_operator=True,
        )
        fc = op.outputs.fields_as_fields_container()[0]

        raise Exception()

    # def save_as_vtk(
    #     self, filename, rsets=None, result_types=["ENS"], progress_bar=True
    # ):
    #     """Writes results to a vtk readable file.

    #     Nodal results will always be written.

    #     The file extension will select the type of writer to use.
    #     ``'.vtk'`` will use the legacy writer, while ``'.vtu'`` will
    #     select the VTK XML writer.

    #     Parameters
    #     ----------
    #     filename : str, pathlib.Path
    #         Filename of grid to be written.  The file extension will
    #         select the type of writer to use.  ``'.vtk'`` will use the
    #         legacy writer, while ``'.vtu'`` will select the VTK XML
    #         writer.

    #     rsets : collections.Iterable
    #         List of result sets to write.  For example ``range(3)`` or
    #         [0].

    #     result_types : list
    #         Result type to write.  For example ``['ENF', 'ENS']``
    #         List of some or all of the following:

    #         - EMS: misc. data
    #         - ENF: nodal forces
    #         - ENS: nodal stresses
    #         - ENG: volume and energies
    #         - EGR: nodal gradients
    #         - EEL: elastic strains
    #         - EPL: plastic strains
    #         - ECR: creep strains
    #         - ETH: thermal strains
    #         - EUL: euler angles
    #         - EFX: nodal fluxes
    #         - ELF: local forces
    #         - EMN: misc. non-sum values
    #         - ECD: element current densities
    #         - ENL: nodal nonlinear data
    #         - EHC: calculated heat generations
    #         - EPT: element temperatures
    #         - ESF: element surface stresses
    #         - EDI: diffusion strains
    #         - ETB: ETABLE items
    #         - ECT: contact data
    #         - EXY: integration point locations
    #         - EBA: back stresses
    #         - ESV: state variables
    #         - MNL: material nonlinear record

    #     progress_bar : bool, optional
    #         Display a progress bar using ``tqdm``.

    #     Notes
    #     -----
    #     Binary files write much faster than ASCII, but binary files
    #     written on one system may not be readable on other systems.
    #     Binary can only be selected for the legacy writer.

    #     Examples
    #     --------
    #     Write nodal results as a binary vtk file.

    #     >>> rst.save_as_vtk('results.vtk')

    #     Write using the xml writer

    #     >>> rst.save_as_vtk('results.vtu')

    #     Write only nodal and elastic strain for the first result

    #     >>> rst.save_as_vtk('results.vtk', [0], ['EEL', 'EPL'])

    #     Write only nodal results (i.e. displacements) for the first result.

    #     >>> rst.save_as_vtk('results.vtk', [0], [])

    #     """
    #     # This should probably be included a part of the ansys.dpf.post.result_data.ResultData class
    #     raise NotImplementedError("To be implemented by DPF")

    # @property
    # def subtitle(self):
    #     raise NotImplementedError("To be implemented by DPF")

    # def cs_4x4(self, cs_cord, as_vtk_matrix=False):
    #     """return a 4x4 transformation array for a given coordinate system"""
    #     raise NotImplementedError("To be implemented by DPF.")

    # def cylindrical_nodal_stress(self):
    #     """Retrieves the stresses for each node in the solution in the
    #     cylindrical coordinate system as the following values:

    #     ``R``, ``THETA``, ``Z``, ``RTHETA``, ``THETAZ``, and ``RZ``

    #     The order of the results corresponds to the sorted node
    #     numbering.

    #     Computes the nodal stress by averaging the stress for each
    #     element at each node.  Due to the discontinuities across
    #     elements, stresses will vary based on the element they are
    #     evaluated from.

    #     Parameters
    #     ----------
    #     rnum : int or list
    #         Cumulative result number with zero based indexing, or a
    #         list containing (step, substep) of the requested result.

    #     nodes : str, sequence of int or str, optional
    #         Select a limited subset of nodes.  Can be a nodal
    #         component or array of node numbers.  For example

    #         * ``"MY_COMPONENT"``
    #         * ``['MY_COMPONENT', 'MY_OTHER_COMPONENT]``
    #         * ``np.arange(1000, 2001)``

    #     Returns
    #     -------
    #     nnum : numpy.ndarray
    #         Node numbers of the result.

    #     stress : numpy.ndarray
    #         Stresses at ``R, THETA, Z, RTHETA, THETAZ, RZ`` averaged
    #         at each corner node where ``R`` is radial.

    #     Examples
    #     --------
    #     >>> from ansys.mapdl.core.reader import DPFResult as Result
    #     >>> rst = Result('file.rst')
    #     >>> nnum, stress = rst.cylindrical_nodal_stress(0)

    #     Return the cylindrical nodal stress just for the nodal component
    #     ``'MY_COMPONENT'``.

    #     >>> nnum, stress = rst.cylindrical_nodal_stress(0, nodes='MY_COMPONENT')

    #     Return the nodal stress just for the nodes from 20 through 50.

    #     >>> nnum, stress = rst.cylindrical_nodal_stress(0, nodes=range(20, 51))

    #     Notes
    #     -----
    #     Nodes without a stress value will be NAN.
    #     Equivalent ANSYS commands:
    #     RSYS, 1
    #     PRNSOL, S
    #     """
    #     raise NotImplementedError("This should be implemented by DPF")

    # def element_lookup(self, element_id):
    #     """Index of the element within the result mesh"""
    #     # We need to get the mapping between the mesh.grid and the results.elements.
    #     # Probably DPF already has that mapping.
    #     raise NotImplementedError("This should be implemented by DPF")

    # def element_solution_data(self):
    #     pass

    # def materials(self):
    #     pass

    # def quadgrid(self):
    #     pass

    # def read_record(self):
    #     pass

    # def result_dof(self):
    #     pass

    # def section_data(self):
    #     pass

    # def solution_info(self):
    #     pass

    # def text_result_table(self):
    #     pass

    # def write_table(self):
    #     pass

    # def nodal_boundary_conditions(self):
    #     pass

    # def nodal_input_force(self):
    #     pass

    # def nodal_static_forces(self):
    #     pass

    # def node_components(self):
    #     pass

    # def parse_coordinate_system(self):
    #     pass


#### overwriting
# def overwrite_element_solution_record(self):
#     pass

# def overwrite_element_solution_records(self):
#     pass

### plotting

# def animate_nodal_displacement(self):
#     pass

# def animate_nodal_solution(self):
#     pass

# def animate_nodal_solution_set(self):
#     pass

# def plot(self):
#     pass

# def plot_cylindrical_nodal_stress(self):
#     pass

# def plot_element_result(self):
#     pass

# def plot_nodal_displacement(self,
#     rnum,
#     comp=None,
#     show_displacement=False,
#     displacement_factor=1.0,
#     node_components=None,
#     element_components=None,
#     **kwargs):
#     pass

#     if kwargs.pop("sel_type_all", None):
#         warn(f"The kwarg 'sel_type_all' is being deprecated.")

#     if kwargs.pop("treat_nan_as_zero", None):
#         warn(f"The kwarg 'treat_nan_as_zero' is being deprecated.")

#     if isinstance(rnum, list):
#         set_ = rnum[0]  # todo: implement subresults
#     elif isinstance(rnum, (int, float)):
#         set_ = rnum
#     else:
#         raise ValueError(f"Please use 'int', 'float' or  'list' for the parameter 'rnum'.")

#     disp = self.model.displacement(set=set_)
#     if not comp:
#         comp = 'norm'
#     disp_dir = getattr(disp, comp)
#     disp_dir.plot_contour(**kwargs)

# def plot_nodal_elastic_strain(self):
#     pass

# def plot_nodal_plastic_strain(self):
#     pass

# def plot_nodal_solution(self):
#     pass

# def plot_nodal_stress(self):
#     pass

# def plot_nodal_temperature(self):
#     pass

# def plot_nodal_thermal_strain(self):
#     pass

# def plot_principal_nodal_stress(self):
#     pass


class DPFResultRST(DPFResult):
    """Interface to the DPF result class based on the RST file format."""

    def connect(self):
        pass


class DPFResultMAPDL(DPFResult):
    """Interface to the DPF result class based on the MAPDL instance"""

    def connect(self):
        pass
