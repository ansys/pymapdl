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

from functools import wraps
import os
import pathlib
import socket
import tempfile
from typing import TYPE_CHECKING, Any, Callable, Iterable, Literal
import weakref

# from ansys.dpf import post
import numpy as np

from ansys.mapdl.core import _HAS_DPF, _HAS_PYVISTA, LOG, Logger, Mapdl  # type: ignore
from ansys.mapdl.core.errors import MapdlRuntimeError
from ansys.mapdl.core.misc import check_valid_ip, get_local_ip, parse_ip_route

COMPONENTS: list[str] = ["X", "Y", "Z", "XY", "YZ", "XZ"]

if _HAS_DPF:
    from ansys.dpf import core as dpf
    from ansys.dpf.core import Model
    from ansys.dpf.core.errors import DPFServerException


if TYPE_CHECKING and _HAS_PYVISTA:
    import pyvista as pv

LOCATION_MAPPING: dict[str, str] = {
    "NODE": "Nodal",
    "ELEM": "Elemental",
}

MATERIAL_PROPERTIES: list[str] = [
    "EX",
    "EY",
    "EZ",
    "ALPX",
    "ALPY",
    "ALPZ",
    "REFT",
    "PRXY",
    "PRYZ",
    "PRX",
    "NUXY",
    "NUYZ",
    "NUXZ",
    "GXY",
    "GYZ",
    "GXZ",
    "DAMP",
    "MU",
    "DENS",
    "C",
    "ENTH",
    "KXX",
    "KYY",
    "KZZ",
    "HF",
    "EMIS",
    "QRATE",
    "VISC",
    "SONC",
    "RSVX",
    "RSVY",
    "RSVZ",
    "PERX",
    "PERY",
    "PERZ",
    "MURX",
    "MURY",
    "MURZ",
    "MGXX",
    "MGYY",
    "MGZZ",
    "XTEN",
    "XCMP",
    "YTEN",
    "YCMP",
    "ZTEN",
    "ZCMP",
    "XY",
    "YZ",
    "XZ",
    "XYCP",
    "YZCP",
    "XZCP",
    "XZIT",
    "XZIC",
    "YZIT",
    "YZIC",
]


NOT_AVAILABLE_METHOD = """The method '{method}' has not been ported to the new DPF-based Results backend.
If you still want to use it, you can switch to 'pymapdl-reader' backend."""


class ResultNotFound(MapdlRuntimeError):
    """Results not found"""

    def __init__(self, msg: str = ""):
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


class DPFResult:
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

    rst_is_on_remote : bool, optional
        If True, the RST file is located on the remote server already.
        If False, the RST file is located on the local machine, and it will be
        uploaded to the DPF server

    """

    def __init__(
        self,
        rst_file_path: str | None = None,
        mapdl: "Mapdl | None" = None,
        rst_is_on_remote: bool = False,
        logger: Logger | None = None,
    ) -> None:
        """Initialize Result instance"""

        if not _HAS_DPF:
            raise ModuleNotFoundError(
                "The DPF library is not installed. Please install it using 'pip install ansys-dpf-core'."
            )

        self._mapdl_weakref: weakref.ref["Mapdl"] | None = None
        self._server_file_path: str | None = None  # In case DPF is remote.
        self._logger: Logger | None = logger

        # RST parameters
        self.__rst_directory: str | None = None
        self.__rst_name: str | None = None
        self._mode_rst: bool

        if rst_file_path is not None and mapdl is not None:
            raise ValueError(
                "Only one the arguments must be supplied: 'rst_file_path' or 'mapdl'."
            )

        elif rst_file_path is not None:
            # Using RST file only allows for one RST file at the time.
            if not rst_is_on_remote and not os.path.exists(rst_file_path):
                raise FileNotFoundError(
                    f"The RST file '{rst_file_path}' could not be found."
                )
            elif rst_is_on_remote:
                self._server_file_path = rst_file_path

            self.logger.debug("Initializing DPFResult class in RST mode.")
            self._mode_rst = True

            self.__rst_directory = os.path.dirname(rst_file_path)
            self.__rst_name = os.path.basename(rst_file_path)

        elif mapdl is not None:
            # Using MAPDL instance allows to switch between RST files.
            if not isinstance(mapdl, Mapdl):  # pragma: no cover # type: ignore
                raise TypeError("Must be initialized using Mapdl instance")

            self.logger.debug("Initializing DPFResult class in MAPDL mode.")
            self._mapdl_weakref = weakref.ref(mapdl)
            self._mode_rst = False

        else:
            raise ValueError(
                "One of the following kwargs must be supplied: 'rst_file_path' or 'mapdl'"
            )

        # dpf
        # If True, it triggers a update on the RST file
        self._update_required: bool = False
        self._loaded: bool = False
        self._cached_dpf_model: "dpf.Model" | None = None
        self._connected: bool = False
        self._server: dpf.server_types.BaseServer | None = None
        self._tmp_dir: str | None = (
            None  # Temporary directory to store the RST file locally
        )
        self.__mapdl_and_dpf_on_same_machine: bool | None = (
            None  # True if the DPF server is running on the same machine as MAPDL
        )
        self._dpf_is_remote: bool | None = None  # Whether DPF is remote or not
        self._dpf_ip: str | None = None
        self._rst_is_on_remote: bool = rst_is_on_remote

        # old attributes
        # ELEMENT_INDEX_TABLE_KEY = None  # todo: To fix
        # ELEMENT_RESULT_NCOMP = None  # todo: to fix

        # Let's try to delay the loading of the RST file until the first access
        # self._update() # Loads the RST file and sets the dpf model

    def _get_is_remote(self) -> bool:
        """Check if the DPF server is running on a remote machine."""
        if not hasattr(self.server, "ip"):
            return False

        own_ip = get_local_ip()
        dpf_ip = self.server.ip if self.server else ""
        return own_ip != dpf_ip

    def _get_is_same_machine(self) -> bool | None:
        """
        Check if the MAPDL and the DPF instances are running on the same machine.

        """
        if self.mapdl is None:
            self.logger.warning(
                "MAPDL instance is not provided. Cannot determine if MAPDL and DPF are running on the same machine."
            )
            return None
        else:
            mapdl = self.mapdl

        # The 'ifconfig' output is reliable in terms of order of the IP address,
        # however it is not installed by default on all systems.
        # The 'hostname -I' command is more widely available, but it may return
        # multiple IP addresses, hence we are going to try both.
        cmds = [
            r"ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'",
            "hostname -I | cut -d' ' -f1",
        ]
        mapdl_ip = None
        for cmd in cmds:
            if output := mapdl.sys(cmd):
                # If the command returns an IP address, it means MAPDL is running on a local machine.
                mapdl_ip = parse_ip_route(output)
                if check_valid_ip(mapdl_ip):
                    break

        self.logger.debug(
            f"MAPDL IP address determined as: {mapdl_ip} using command: {cmd}"
        )
        self._mapdl_ip = mapdl_ip or mapdl.ip
        self.logger.debug(f"Using MAPDL IP address: {self._mapdl_ip}")

        # Get DPF server IP
        dpf_ip = self.dpf_ip

        if mapdl_ip != dpf_ip:
            self.logger.debug(
                f"DPF server IP ({dpf_ip}) is different from MAPDL IP ({mapdl_ip})."
            )
            return False

        # Check MAPDL can find the route
        mapdl_version = str(mapdl.version).replace(".", "")  # Version as 252
        awp_root = (
            mapdl.inquire("", "env", f"AWP_ROOT{mapdl_version}")
            or f"/ansys_inc/v{mapdl_version}"
        )

        dpf_executable = f"{awp_root}/aisol/bin/linx64/Ans.Dpf.Grpc.exe"
        if mapdl.inquire("", "exist", dpf_executable):
            self.logger.debug(
                f"DPF executable found at {dpf_executable}. MAPDL and DPF are running on the same machine."
            )
            return True
        else:
            self.logger.debug(
                f"DPF executable not found at {dpf_executable}. MAPDL and DPF are NOT running on the same machine."
            )
            return False

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
                raise ValueError(
                    "external_ip and external_port should be provided for RemoteGrpc communication"
                )

        self._server = srvr

    def _get_dpf_ip(self) -> str:
        return self.server.ip if self.server and hasattr(self.server, "ip") else ""

    @property
    def dpf_ip(self) -> str:
        if self._dpf_ip is None:
            self._dpf_ip = self._get_dpf_ip()
        return self._dpf_ip

    @property
    def server(self) -> "dpf.server_types.BaseServer":
        """
        Return the DPF server connection.

        Returns
        -------
        dpf.server_types.BaseServer
            The DPF server connection.
        """
        if self._server is None:
            self.connect_to_server()

        return self._server

    @property
    def rst_is_on_remote(self) -> bool:
        return self._rst_is_on_remote

    def _try_connect_inprocess(self) -> None:
        try:
            self._connect_to_dpf_using_mode(mode="InProcess")
            self._connected = True
            self.logger.debug("Connected to DPF server using InProcess.")
        except DPFServerException:  # type: ignore # probably should filter a bit here
            self._connected = False

    def _try_connect_localgrpc(self) -> None:
        try:
            self._connect_to_dpf_using_mode(mode="LocalGrpc")
            self._connected = True
            self.logger.debug("Connected to DPF server using LocalGrpc.")
        except DPFServerException:  # type: ignore # probably should filter a bit here
            self._connected = False

    def _try_connect_remote_grpc(self, dpf_ip: str, dpf_port: int) -> None:
        try:
            self._connect_to_dpf_using_mode(
                mode="RemoteGrpc", external_ip=dpf_ip, external_port=dpf_port
            )
            self._connected = True
            self.logger.debug(
                f"Connected to DPF server using RemoteGrpc on {dpf_ip}:{dpf_port}."
            )
        except DPFServerException:  # type: ignore
            self._connected = False

    def _iterate_connections(self, dpf_ip: str, dpf_port: int) -> None:
        if not self._connected:
            self._try_connect_remote_grpc(dpf_ip, dpf_port)

        if not self._connected:
            self._try_connect_inprocess()

        if not self._connected:
            self._try_connect_localgrpc()

        if self._connected:
            return
        else:
            raise DPFServerException(
                "Could not connect to DPF server after trying all the available options."
            )

    def _get_dpf_env_vars(
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
            self.logger.debug("Connecting to a remote gRPC DPF server")
            self._try_connect_remote_grpc(ip, port)

        else:
            # any connection method is supported because the file local.
            self.logger.debug("Attempting any connection method")
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

        ip, port = self._get_dpf_env_vars(ip, port)

        # resolve ip
        ip = socket.gethostbyname(ip)

        check_valid_ip(ip)

        self._connect_to_dpf(ip, port)

    @property
    def dpf_is_remote(self) -> bool:
        """Returns True if we are connected to the DPF Server using a gRPC connection to a remote IP."""
        if self._dpf_is_remote is None:
            self._dpf_is_remote = self._get_is_remote()
        return self._dpf_is_remote

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
        if self._logger is None:
            self._logger = LOG
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
        self._logger = logger

    @property
    def mode(self):
        return "RST" if self._mode_rst else "MAPDL"

    @property
    def mode_rst(self):
        return bool(self._mode_rst)

    @property
    def mode_mapdl(self):
        return not self._mode_rst

    @property
    def _mapdl_dpf_on_same_machine(self):
        """True if the DPF server is running on the same machine as MAPDL"""
        if self.__mapdl_and_dpf_on_same_machine is None:
            self.__mapdl_and_dpf_on_same_machine = self._get_is_same_machine()
        return self.__mapdl_and_dpf_on_same_machine

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
        if self.mode_mapdl:
            # because it might be remote
            return self.mapdl.result_file

        else:
            return os.path.join(self._rst_directory, self._rst_name)

    @property
    def mapdl_is_local(self):
        if self.mapdl:
            return self._mapdl.is_local

    @property
    def _rst_directory(self) -> str:
        if self.mapdl:
            self.__rst_directory = os.path.dirname(self.mapdl.result_file)  # type: ignore
        return self.__rst_directory  # type: ignore

    @property
    def _rst_name(self) -> str:
        if self.mapdl:
            # update always
            self.__rst_name = os.path.basename(self.mapdl.result_file)
        return self.__rst_name

    def update(
        self, progress_bar: bool | None = None, chunk_size: int | None = None
    ) -> None:
        """Update the DPF Model

        Parameters
        ----------
        progress_bar : bool, optional
            If True, display a progress bar during the update process. If None, the default behavior is used.

        chunk_size : int, optional
            Number of items to process per chunk. If None, the default chunk size is used.
        """
        return self._update(progress_bar=progress_bar, chunk_size=chunk_size)

    def _update(
        self, progress_bar: bool | None = None, chunk_size: int | None = None
    ) -> None:
        if self.mode_mapdl:
            self._update_rst(progress_bar=progress_bar, chunk_size=chunk_size)

            # Upload it to DPF if we are not in local
            if self.dpf_is_remote and not self._mapdl_dpf_on_same_machine:
                self._upload_to_dpf()
        elif self.dpf_is_remote and not self.rst_is_on_remote:
            # If the RST is not on the remote server, we need to upload it
            self._upload_to_dpf()

        # Updating model
        self._build_dpf_object()

        # Resetting flag
        self._loaded = True
        self._update_required = False

    def _upload_to_dpf(self):
        if self.mode_mapdl and self._mapdl_dpf_on_same_machine is True:
            self._log.debug("Updating server file path for DPF model.")
            self._server_file_path = os.path.join(
                self._mapdl.directory, self._mapdl.result_file
            )
        elif self.mode_rst and not self.dpf_is_remote:
            self._server_file_path = self._rst
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
        """Update RST from MAPDL instance

        Parameters
        ----------
        progress_bar: bool
            Whether print or not the progress bar during the RST file uploading

        chunk_size: int
            The value of the size of the chunk used to upload the file.

        save: bool
            Whether save the model or not before update the RST file
        """
        # Saving model
        if save:
            self.mapdl.save()  # type: ignore

        if self.mapdl_is_local:
            rst_file_exists = os.path.exists(self._rst)
        else:
            rst_file_exists = self.mapdl.inquire("", "exist", self._rst)

        if not rst_file_exists:
            raise FileNotFoundError(
                f"The result file could not be found in {self.mapdl.directory}"
            )

        if self.mapdl_is_local is False and self._mapdl_dpf_on_same_machine is False:
            self._log.debug("Updating the local copy of remote RST file.")
            # download file
            self._tmp_dir = tempfile.gettempdir()
            self.mapdl.download(  # type: ignore
                self._rst,
                self._tmp_dir,
                progress_bar=progress_bar,
                chunk_size=chunk_size,
            )

    def _build_dpf_object(self):
        if self._log:
            self._log.debug("Building/Updating DPF Model object.")

        if self.dpf_is_remote and not self._mapdl_dpf_on_same_machine:
            rst = self._server_file_path
        else:
            rst = self._rst

        self._cached_dpf_model = Model(str(rst))

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
        entities: str | int | float | Iterable[str | int | float] | None,
        entity_type: str = "Nodal",
    ) -> Iterable[int | float] | None:
        """Get entities ids given their ids, or component names.

        If a list is given it checks can be int, floats, or list/tuple of int/floats, or
        components (strs, or iterable[strings])

        Parameters
        ----------
        entities : str | int | float | Iterable[str | int | float]
            Entities ids or components. If a mix of strings and numbers is
            provided in the iterable, a ValueError will be raised.

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
            return None

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

            entities_.extend(scoping.ids.tolist())

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
            scop.ids = scope_ids if scope_ids else mesh.nodes.scoping.ids

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
        elif isinstance(rnum, (int, float)):
            rnum = [rnum]
        elif isinstance(rnum, (list, tuple)):
            rnum = [self.parse_step_substep(rnum)]
        else:
            raise TypeError("Only 'int' and 'float' are supported to define the steps.")

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
        scope_ids = self._get_entities_ids(scope_ids, requested_location)

        # Set type of return
        ids = self._set_mesh_scoping(op, mesh, requested_location, scope_ids)

        if requested_location.lower() == "elemental":
            op = self._set_element_results(
                op, mesh
            )  # overwrite op to be the elemental results OP

        # Applying rescope to make sure the order is right
        if not isinstance(ids, list):
            ids = ids.astype(int).tolist()

        op = self._set_rescope(op, ids)

        return op if return_operator else self._extract_data(op)

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

    def nodal_solution(
        self, rnum, in_nodal_coord_sys=None, nodes=None, return_temperature=False
    ):
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

        return_temperature: bool, optional
            When ``True``, returns the nodal temperature instead of
            the displacement.  Default ``False``.

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

        if hasattr(self.model.results, "displacement") and not return_temperature:
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

    @property
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

    @property
    def time_values(self):
        "Values for the time/frequency"
        return self.metadata.time_freq_support.time_frequencies.data_as_list

    @property
    def materials(self) -> dict[int, dict[str, int | float]]:
        """Result file material properties.

        Returns
        -------
        dict
            Dictionary of Materials.  Keys are the material numbers,
            and each material is a dictionary of the material
            properties of that material with only the valid entries filled.

        Notes
        -----
        Material properties:

        - EX : Elastic modulus, element x direction (Force/Area)
        - EY : Elastic modulus, element y direction (Force/Area)
        - EZ : Elastic modulus, element z direction (Force/Area)
        - ALPX : Coefficient of thermal expansion, element x direction (Strain/Temp)
        - ALPY : Coefficient of thermal expansion, element y direction (Strain/Temp)
        - ALPZ : Coefficient of thermal expansion, element z direction (Strain/Temp)
        - REFT : Reference temperature (as a property) [TREF]
        - PRXY : Major Poisson's ratio, x-y plane
        - PRYZ : Major Poisson's ratio, y-z plane
        - PRX  Z : Major Poisson's ratio, x-z plane
        - NUXY : Minor Poisson's ratio, x-y plane
        - NUYZ : Minor Poisson's ratio, y-z plane
        - NUXZ : Minor Poisson's ratio, x-z plane
        - GXY : Shear modulus, x-y plane (Force/Area)
        - GYZ : Shear modulus, y-z plane (Force/Area)
        - GXZ : Shear modulus, x-z plane (Force/Area)
        - DAMP : K matrix multiplier for damping [BETAD] (Time)
        - MU : Coefficient of friction (or, for FLUID29 and FLUID30
               elements, boundary admittance)
        - DENS : Mass density (Mass/Vol)
        - C : Specific heat (Heat/Mass*Temp)
        - ENTH : Enthalpy (e DENS*C d(Temp)) (Heat/Vol)
        - KXX : Thermal conductivity, element x direction
                (Heat*Length / (Time*Area*Temp))
        - KYY : Thermal conductivity, element y direction
                (Heat*Length / (Time*Area*Temp))
        - KZZ : Thermal conductivity, element z direction
                (Heat*Length / (Time*Area*Temp))
        - HF : Convection (or film) coefficient (Heat / (Time*Area*Temp))
        - EMIS : Emissivity
        - QRATE : Heat generation rate (MASS71 element only) (Heat/Time)
        - VISC : Viscosity (Force*Time / Length2)
        - SONC : Sonic velocity (FLUID29 and FLUID30 elements only) (Length/Time)
        - RSVX : Electrical resistivity, element x direction (Resistance*Area / Length)
        - RSVY : Electrical resistivity, element y direction (Resistance*Area / Length)
        - RSVZ : Electrical resistivity, element z direction (Resistance*Area / Length)
        - PERX : Electric permittivity, element x direction (Charge2 / (Force*Length))
        - PERY : Electric permittivity, element y direction (Charge2 / (Force*Length))
        - PERZ : Electric permittivity, element z direction (Charge2 / (Force*Length))
        - MURX : Magnetic relative permeability, element x direction
        - MURY : Magnetic relative permeability, element y direction
        - MURZ : Magnetic relative permeability, element z direction
        - MGXX : Magnetic coercive force, element x direction (Charge / (Length*Time))
        - MGYY : Magnetic coercive force, element y direction (Charge / (Length*Time))
        - MGZZ : Magnetic coercive force, element z direction (Charge / (Length*Time))

        Materials may contain the key ``"stress_failure_criteria"``, which
        contains failure criteria information for temperature-dependent stress
        limits. This includes the following keys:

        - XTEN : Allowable tensile stress or strain in the x-direction. (Must
          be positive.)

        - XCMP : Allowable compressive stress or strain in the
          x-direction. (Defaults to negative of XTEN.)

        - YTEN : Allowable tensile stress or strain in the y-direction. (Must
          be positive.)

        - YCMP : Allowable compressive stress or strain in the
          y-direction. (Defaults to negative of YTEN.)

        - ZTEN : Allowable tensile stress or strain in the z-direction. (Must
          be positive.)

        - ZCMP : Allowable compressive stress or strain in the
          z-direction. (Defaults to negative of ZTEN.)

        - XY : Allowable XY stress or shear strain. (Must be positive.)

        - YZ : Allowable YZ stress or shear strain. (Must be positive.)

        - XZ : Allowable XZ stress or shear strain. (Must be positive.)

        - XYCP : XY coupling coefficient (Used only if Lab1 = S). Defaults to -1.0. [1]

        - YZCP : YZ coupling coefficient (Used only if Lab1 = S). Defaults to -1.0. [1]

        - XZCP : XZ coupling coefficient (Used only if Lab1 = S). Defaults to -1.0. [1]

        - XZIT : XZ tensile inclination parameter for Puck failure index (default =
          0.0)

        - XZIC : XZ compressive inclination parameter for Puck failure index
          (default = 0.0)

        - YZIT : YZ tensile inclination parameter for Puck failure index
          (default = 0.0)

        - YZIC : YZ compressive inclination parameter for Puck failure index
          (default = 0.0)

        Examples
        --------
        Return the material properties from the example result
        file. Note that the keys of ``rst.materials`` is the material
        type.

        >>> from ansys.mapdl import reader as pymapdl_reader
        >>> from ansys.mapdl.reader import examples
        >>> rst = pymapdl_reader.read_binary(examples.rstfile)
        >>> rst.materials
        {1: {'EX': 16900000.0, 'NUXY': 0.31, 'DENS': 0.00041408}}

        """
        mats = self.mesh.property_field("mat")
        mat_prop = dpf.operators.result.mapdl_material_properties()
        mat_prop.inputs.materials.connect(mats)

        mat_prop.connect(0, MATERIAL_PROPERTIES)
        mat_prop.inputs.data_sources.connect(self.model)
        prop_field = mat_prop.outputs.properties_value.get_data()

        # Obtaining materials ids
        mat_ids: set[int] = set()
        for prop in prop_field:
            mat_ids = mat_ids.union(prop.scoping.ids.tolist())

        # Building dictionary of materials
        mats = {}
        for mat_id in mat_ids:
            mats[mat_id] = {}

            for each_label in prop_field.labels:
                field = prop_field.get_fields({each_label: 1})[0]
                data = field.data.tolist()

                if data and len(data) > 0 and data[0] != 0:
                    mats[mat_id][each_label] = data[0] if len(data) == 1 else data
        return mats

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
        # if not comp:
        #     comp = "X"

        # ind = COMPONENTS.index(comp)

        # op = self._get_nodes_result(
        #     rnum,
        #     "stress",
        #     nodes=node_components,
        #     in_nodal_coord_sys=False,
        #     return_operator=True,
        # )
        # fc = op.outputs.fields_as_fields_container()[0]

        raise NotImplementedError("WIP")

    @property
    def _elements(self):
        return self.mesh.elements.scoping.ids

    def element_lookup(self, element_id):
        """Index of the element within the result mesh"""
        mapping = dict(zip(self._elements, np.arange(self.mesh.elements.n_elements)))
        if element_id not in mapping:
            raise KeyError(
                f"Element ID {element_id} not found in the result mesh. "
                f"Available element IDs: {list(mapping.keys())}"
            )

        return mapping[element_id]

    def overwrite_element_solution_record(self, data, rnum, solution_type, element_id):
        """Overwrite element solution record.

        This method replaces solution data for of an element at a
        result index for a given solution type.  The number of items
        in ``data`` must match the number of items in the record.

        If you are not sure how many records are in a given record,
        use ``element_solution_data`` to retrieve all the records for
        a given ``solution_type`` and check the number of items in the
        record.

        Note: The record being replaced cannot be a compressed record.
        If the result file uses compression (default sparse
        compression as of 2019R1), you can disable this within MAPDL
        with:
        ``/FCOMP, RST, 0``

        Parameters
        ----------
        data : list or np.ndarray
            Data that will replace the existing records.

        rnum : int
            Zero based result number.

        solution_type : str
            Element data type to overwrite.

            - EMS: misc. data
            - ENF: nodal forces
            - ENS: nodal stresses
            - ENG: volume and energies
            - EGR: nodal gradients
            - EEL: elastic strains
            - EPL: plastic strains
            - ECR: creep strains
            - ETH: thermal strains
            - EUL: euler angles
            - EFX: nodal fluxes
            - ELF: local forces
            - EMN: misc. non-sum values
            - ECD: element current densities
            - ENL: nodal nonlinear data
            - EHC: calculated heat generations
            - EPT: element temperatures
            - ESF: element surface stresses
            - EDI: diffusion strains
            - ETB: ETABLE items
            - ECT: contact data
            - EXY: integration point locations
            - EBA: back stresses
            - ESV: state variables
            - MNL: material nonlinear record

        element_id : int
            Ansys element number (e.g. ``1``)

        Examples
        --------
        Overwrite the elastic strain record for element 1 for the
        first result with random data.

        >>> from ansys.mapdl import reader as pymapdl_reader
        >>> rst = pymapdl_reader.read_binary('file.rst')
        >>> data = np.random.random(56)
        >>> rst.overwrite_element_solution_data(data, 0, 'EEL', 1)
        """
        raise NotImplementedError(
            NOT_AVAILABLE_METHOD.format(method="overwrite_element_solution_record")
        )

    def overwrite_element_solution_records(self, element_data, rnum, solution_type):
        """Overwrite element solution record.

        This method replaces solution data for a set of elements at a
        result index for a given solution type.  The number of items
        in ``data`` must match the number of items in the record.

        If you are not sure how many records are in a given record,
        use ``element_solution_data`` to retrieve all the records for
        a given ``solution_type`` and check the number of items in the
        record.

        Note: The record being replaced cannot be a compressed record.
        If the result file uses compression (default sparse
        compression as of 2019R1), you can disable this within MAPDL
        with:
        ``/FCOMP, RST, 0``

        Parameters
        ----------
        element_data : dict
            Dictionary of results that will replace the existing records.

        rnum : int
            Zero based result number.

        solution_type : str
            Element data type to overwrite.

            - EMS: misc. data
            - ENF: nodal forces
            - ENS: nodal stresses
            - ENG: volume and energies
            - EGR: nodal gradients
            - EEL: elastic strains
            - EPL: plastic strains
            - ECR: creep strains
            - ETH: thermal strains
            - EUL: euler angles
            - EFX: nodal fluxes
            - ELF: local forces
            - EMN: misc. non-sum values
            - ECD: element current densities
            - ENL: nodal nonlinear data
            - EHC: calculated heat generations
            - EPT: element temperatures
            - ESF: element surface stresses
            - EDI: diffusion strains
            - ETB: ETABLE items
            - ECT: contact data
            - EXY: integration point locations
            - EBA: back stresses
            - ESV: state variables
            - MNL: material nonlinear record

        Examples
        --------
        Overwrite the elastic strain record for elements 1 and 2 with
        for the first result with random data.

        >>> from ansys.mapdl import reader as pymapdl_reader
        >>> rst = pymapdl_reader.read_binary('file.rst')
        >>> data = {1: np.random.random(56),
                    2: np.random.random(56)}
        >>> rst.overwrite_element_solution_data(data, 0, 'EEL')
        """
        raise NotImplementedError(
            NOT_AVAILABLE_METHOD.format(method="overwrite_element_solution_records")
        )

    def read_record(self, pointer, return_bufsize=False):
        """Reads a record at a given position.

        Because ANSYS 19.0+ uses compression by default, you must use
        this method rather than ``np.fromfile``.

        Parameters
        ----------
        pointer : int
            ANSYS file position (n words from start of file).  A word
            is four bytes.

        return_bufsize : bool, optional
            Returns the number of words read (includes header and
            footer).  Useful for determining the new position in the
            file after reading a record.

        Returns
        -------
        record : np.ndarray
            The record read as a ``n x 1`` numpy array.

        bufsize : float, optional
            When ``return_bufsize`` is enabled, returns the number of
            words read.

        """
        raise NotImplementedError(NOT_AVAILABLE_METHOD.format(method="read_record"))

    def text_result_table(self, rnum):
        """Returns a text result table for plotting"""
        raise NotImplementedError(
            NOT_AVAILABLE_METHOD.format(method="text_result_table")
        )

    def write_tables(self, filename: str | pathlib.Path):
        """Write binary tables to ASCII.  Assumes int32

        Parameters
        ----------
        filename : str, pathlib.Path
            Filename to write the tables to.

        Examples
        --------
        >>> rst.write_tables('tables.txt')
        """
        raise NotImplementedError(NOT_AVAILABLE_METHOD.format(method="write_tables"))

    def cs_4x4(self, cs_cord, as_vtk_matrix=False):
        """Return a 4x4 transformation matrix for a given coordinate system.

        Parameters
        ----------
        cs_cord : int
            Coordinate system index.

        as_vtk_matrix : bool, default: False
            Return the transformation matrix as a ``vtkMatrix4x4``.

        Returns
        -------
        np.ndarray | vtk.vtkMatrix4x4
            Matrix or ``vtkMatrix4x4`` depending on the value of ``as_vtk_matrix``.

        Notes
        -----
        Values 11 and greater correspond to local coordinate systems

        Examples
        --------
        Return the transformation matrix for coordinate system 1.

        >>> tmat = rst.cs_4x4(1)
        >>> tmat
        array([[1., 0., 0., 0.],
               [0., 1., 0., 0.],
               [0., 0., 1., 0.],
               [0., 0., 0., 1.]])

        Return the transformation matrix for coordinate system 5. This
        corresponds to ``CSYS, 5``, the cylindrical with global Cartesian Y as
        the axis of rotation.

        >>> tmat = rst.cs_4x4(5)
        >>> tmat
        array([[ 1.,  0.,  0.,  0.],
               [ 0.,  0., -1.,  0.],
               [ 0.,  1.,  0.,  0.],
               [ 0.,  0.,  0.,  1.]])

        """
        raise NotImplementedError(NOT_AVAILABLE_METHOD.format(method="cs_4x4"))

    def solution_info(self, rnum):
        """Return an informative dictionary of solution data for a
        result.

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        Returns
        -------
        header : dict
            Double precision solution header data.

        Examples
        --------
        Extract the solution info from a sample example result file.

        >>> from ansys.mapdl.reader import examples
        >>> rst = examples.download_pontoon()
        >>> rst.solution_info(0)
        {'cgcent': [],
         'fatjack': [],
         'timfrq': 44.85185724963714,
         'lfacto': 1.0,
         'lfactn': 1.0,
         'cptime': 3586.4873046875,
         'tref': 71.6,
         'tunif': 71.6,
         'tbulk': 293.0,
         'volbase': 0.0,
         'tstep': 0.0,
         '__unused': 0.0,
         'accel_x': 0.0,
         'accel_y': 0.0,
         'accel_z': 0.0,
         'omega_v_x': 0.0,
         'omega_v_y': 0.0,
         'omega_v_z': 0.0,
         'omega_a_x': 0.0,
         'omega_a_y': 0.0,
         'omega_a_z': 0.0,
         'omegacg_v_x': 0.0,
         'omegacg_v_y': 0.0,
         'omegacg_v_z': 0.0,
         'omegacg_a_x': 0.0,
         'omegacg_a_y': 0.0,
         'omegacg_a_z': 0.0,
         'dval1': 0.0,
         'pCnvVal': 0.0}


        Notes
        -----
        The keys of the solution header are described below:

        - timfrq : Time value (or frequency value, for a modal or
                   harmonic analysis)
        - lfacto : the "old" load factor (used in ramping a load
                    between old and new values)
        - lfactn  : The "new" load factor
        - cptime  : Elapsed CPU time (in seconds)
        - tref    : The reference temperature
        - tunif   : The uniform temperature
        - tbulk   : Bulk temp for FLOTRAN film coefs.
        - VolBase : Initial total volume for VOF
        - tstep   : Time Step size for FLOTRAN analysis
        - 0.0     : Position not used
        - accel   : Linear acceleration terms
        - omega   : Angular velocity (first 3 terms) and angular acceleration
                    (second 3 terms)
        - omegacg : Angular velocity (first 3 terms) and angular
                    acceleration (second 3 terms) these
                    velocity/acceleration terms are computed about the
                    center of gravity
        - cgcent  : (X,y,z) location of center of gravity
        - fatjack : Fatjack ocean wave data (wave height and period)
        - dval1   : If pmeth=0: FATJACK ocean wave direction
                    if pmeth=1: p-method convergence values
        - pCnvVal : P-method convergence values
        """
        raise NotImplementedError(NOT_AVAILABLE_METHOD.format(method="solution_info"))

    @property
    def subtitle(self):
        raise NotImplementedError(NOT_AVAILABLE_METHOD.format(method="subtitle"))

    def _get_comp_dict(self, entity: str):
        """Get a dictionary of components given an entity"""
        entity_comp = {}
        for each_comp in self.mesh.available_named_selections:
            scoping = self.mesh.named_selection(each_comp)
            if scoping.location == LOCATION_MAPPING[entity]:
                entity_comp[each_comp] = tuple(scoping.ids.tolist())

        return entity_comp

    @property
    def node_components(self):
        """Dictionary of ansys node components from the result file.

        Examples
        --------
        >>> from ansys.mapdl import reader as pymapdl_reader
        >>> from ansys.mapdl.reader import examples
        >>> rst = pymapdl_reader.read_binary(examples.rstfile)
        >>> rst.node_components.keys()
        dict_keys(['ECOMP1', 'ECOMP2', 'ELEM_COMP'])
        >>> rst.node_components['NODE_COMP']
        array([ 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
              20], dtype=int32)
        """
        return self._get_comp_dict("NODE")

    @property
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
        return self._get_comp_dict("ELEM")

    def element_solution_data(self, rnum, datatype, sort=True, **kwargs):
        """Retrieves element solution data.  Similar to ETABLE.

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        datatype : str
            Element data type to retrieve.

            - EMS: misc. data
            - ENF: nodal forces
            - ENS: nodal stresses
            - ENG: volume and energies
            - EGR: nodal gradients
            - EEL: elastic strains
            - EPL: plastic strains
            - ECR: creep strains
            - ETH: thermal strains
            - EUL: euler angles
            - EFX: nodal fluxes
            - ELF: local forces
            - EMN: misc. non-sum values
            - ECD: element current densities
            - ENL: nodal nonlinear data
            - EHC: calculated heat generations
            - EPT: element temperatures
            - ESF: element surface stresses
            - EDI: diffusion strains
            - ETB: ETABLE items
            - ECT: contact data
            - EXY: integration point locations
            - EBA: back stresses
            - ESV: state variables
            - MNL: material nonlinear record

        sort : bool
            Sort results by element number.  Default ``True``.

        **kwargs : optional keyword arguments
            Hidden options for distributed result files.

        Returns
        -------
        enum : np.ndarray
            Element numbers.

        element_data : list
            List with one data item for each element.

        enode : list
            Node numbers corresponding to each element.
            results.  One list entry for each element.

        Notes
        -----
        See ANSYS element documentation for available items for each
        element type.  See:

        https://www.mm.bme.hu/~gyebro/files/ans_help_v182/ans_elem/

        Examples
        --------
        Retrieve "LS" solution results from an PIPE59 element for result set 1

        >>> enum, edata, enode = result.element_solution_data(0, datatype='ENS')
        >>> enum[0]  # first element number
        >>> enode[0]  # nodes belonging to element 1
        >>> edata[0]  # data belonging to element 1
        array([ -4266.19   ,   -376.18857,  -8161.785  , -64706.766  ,
                -4266.19   ,   -376.18857,  -8161.785  , -45754.594  ,
                -4266.19   ,   -376.18857,  -8161.785  ,      0.     ,
                -4266.19   ,   -376.18857,  -8161.785  ,  45754.594  ,
                -4266.19   ,   -376.18857,  -8161.785  ,  64706.766  ,
                -4266.19   ,   -376.18857,  -8161.785  ,  45754.594  ,
                -4266.19   ,   -376.18857,  -8161.785  ,      0.     ,
                -4266.19   ,   -376.18857,  -8161.785  , -45754.594  ,
                -4274.038  ,   -376.62527,  -8171.2603 ,   2202.7085 ,
               -29566.24   ,   -376.62527,  -8171.2603 ,   1557.55   ,
               -40042.613  ,   -376.62527,  -8171.2603 ,      0.     ,
               -29566.24   ,   -376.62527,  -8171.2603 ,  -1557.55   ,
                -4274.038  ,   -376.62527,  -8171.2603 ,  -2202.7085 ,
                21018.164  ,   -376.62527,  -8171.2603 ,  -1557.55   ,
                31494.537  ,   -376.62527,  -8171.2603 ,      0.     ,
                21018.164  ,   -376.62527,  -8171.2603 ,   1557.55   ],
              dtype=float32)

        This data corresponds to the results you would obtain directly
        from MAPDL with ESOL commands:

        >>> ansys.esol(nvar='2', elem=enum[0], node=enode[0][0], item='LS', comp=1)
        >>> ansys.vget(par='SD_LOC1', ir='2', tstrt='1') # store in a variable
        >>> ansys.read_float_parameter('SD_LOC1(1)')
        -4266.19
        """
        raise NotImplementedError(
            NOT_AVAILABLE_METHOD.format(method="element_solution_data")
        )

    def result_dof(self, rnum):
        """Return a list of degrees of freedom for a given result number.

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        Returns
        -------
        dof : list
            List of degrees of freedom.

        Examples
        --------
        >>> rst.result_dof(0)
        ['UX', 'UY', 'UZ']
        """
        # To be done later
        raise NotImplementedError(NOT_AVAILABLE_METHOD.format(method="result_dof"))

    def nodal_input_force(self, rnum):
        """Nodal input force for a given result number.

        Nodal input force is generally set with the APDL command
        ``F``.  For example, ``F, 25, FX, 0.001``

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        Returns
        -------
        nnum : np.ndarray
            Node numbers of the nodes with nodal forces.

        dof : np.ndarray
            Array of indices of the degrees of freedom of the nodes
            with input force.  See ``rst.result_dof`` for the degrees
            of freedom associated with each index.

        force : np.ndarray
            Nodal input force.

        Examples
        --------
        Print the nodal input force where:
        - Node 25 has FX=20
        - Node 26 has FY=30
        - Node 27 has FZ=40

        >>> rst.nodal_input_force(0)
        (array([ 25,  26, 27], dtype=int32),
         array([2, 1, 3], dtype=int32),
         array([30., 20., 40.]))
        """
        # To be done later
        raise NotImplementedError(
            NOT_AVAILABLE_METHOD.format(method="nodal_input_force")
        )
