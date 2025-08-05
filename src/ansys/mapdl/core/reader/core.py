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
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Iterable,
    Literal,
)
import weakref

# from ansys.dpf import post
import numpy as np

from ansys.mapdl.core import _HAS_DPF, _HAS_PYVISTA, LOG, Logger, Mapdl  # type: ignore
from ansys.mapdl.core.errors import MapdlRuntimeError
from ansys.mapdl.core.misc import check_valid_ip, get_local_ip, parse_ip_route

if _HAS_DPF:
    from ansys.dpf import core as dpf
    from ansys.dpf.core import Model
    from ansys.dpf.core.errors import DPFServerException

if TYPE_CHECKING and _HAS_PYVISTA:
    import pyvista as pv

from ansys.mapdl.core.reader.constants import (
    COMPONENTS,
    LOCATION_MAPPING,
    MATERIAL_PROPERTIES,
    NOT_AVAILABLE_ARGUMENT,
    NOT_AVAILABLE_METHOD,
)
from ansys.mapdl.core.reader.types import (
    Elements,
    Entities,
    EntityType,
    Ids,
    Locations,
    Nodes,
    P,
    ResultField,
    ReturnData,
    Rnum,
)


class ResultNotFound(MapdlRuntimeError):
    """Exception raised when a result is not found.

    Parameters
    ----------
    msg
        Error message to display.
    """

    def __init__(self, msg: str = ""):
        """Initialize ResultNotFound exception.

        Parameters
        ----------
        msg
            Error message to display.
        """
        MapdlRuntimeError.__init__(self, msg)


class NotImplementedInDPFBackend(MapdlRuntimeError, NotImplementedError):
    """Exception raised when a method is not implemented in the DPF backend.

    Parameters
    ----------
    method : str
        Name of the method that is not implemented.
    """

    def __init__(self, method: str = "", argument: str = ""):
        """Initialize NotImplementedInDPFBackend exception.

        Parameters
        ----------
        method : str
            Name of the method that is not implemented.
        """
        if argument:
            msg = NOT_AVAILABLE_ARGUMENT.format(argument=argument)
        else:
            msg = NOT_AVAILABLE_METHOD.format(method=method)
        MapdlRuntimeError.__init__(self, msg)


def update_result(function: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorator to wrap :class:`DPFResult <ansys.mapdl.core.reader.result.DPFResult>`
    methods to force update the RST when accessed the first time.

    Parameters
    ----------
    function : callable
        Function to decorate.

    Returns
    -------
    Callable[..., Any]
        Decorated function
    """

    @wraps(function)
    def wrapper(self, *args: P.args, **kwargs: P.kwargs):
        if self._update_required or not self._loaded or self._cached_dpf_model is None:
            self.update()
            self.logger.debug("RST file updated.")
        return function(self, *args, **kwargs)

    return wrapper


class DPFResultCore:
    """
    Result object based on DPF library.


    This class replaces the class Result in PyMAPDL-Reader.

    The

    Parameters
    ----------
    rst_file : str
        Path to the RST file.

    mapdl : _MapdlCore
        Mapdl instantiated object.

    rst_is_on_remote : bool, optional
        If True, the RST file is located on the remote server already.
        If False, the RST file is located on the local machine, and it will be
        uploaded to the DPF server

    logger
        Logger instance to use for logging.
    """

    def __init__(
        self,
        *,
        rst_file: str | None = None,
        mapdl: "Mapdl | None" = None,
        rst_is_on_remote: bool = False,
        logger: Logger | None = None,
    ) -> None:
        """Initialize Result instance

        Parameters
        ----------
        rst_file
            Path to the RST file.

        mapdl
            Mapdl instantiated object.

        rst_is_on_remote
            If True, the RST file is located on the remote server already.
            If False, the RST file is located on the local machine, and it will be
            uploaded to the DPF server.

        logger
            Logger instance to use for logging.
        """

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

        if rst_file is not None and mapdl is not None:
            raise ValueError(
                "Only one the arguments must be supplied: 'rst_file' or 'mapdl'."
            )

        elif rst_file is not None:
            # Using RST file only allows for one RST file at the time.
            if not rst_is_on_remote and not os.path.exists(rst_file):
                raise FileNotFoundError(
                    f"The RST file '{rst_file}' could not be found."
                )
            elif rst_is_on_remote:
                self._server_file_path = rst_file

            self.logger.debug("Initializing DPFResult class in RST mode.")
            self._mode_rst = True

            self.__rst_directory = os.path.dirname(rst_file)
            self.__rst_name = os.path.basename(rst_file)

        elif mapdl is not None:
            # Using MAPDL instance allows to switch between RST files.
            if not isinstance(mapdl, Mapdl):  # pragma: no cover # type: ignore
                raise TypeError("Must be initialized using Mapdl instance")

            self.logger.debug("Initializing DPFResult class in MAPDL mode.")
            self._mapdl_weakref = weakref.ref(mapdl)
            self._mode_rst = False

        else:
            raise ValueError(
                "One of the following kwargs must be supplied: 'rst_file' or 'mapdl'"
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
        """Check if the DPF server is running on a remote machine.

        Returns
        -------
        bool
            True if the DPF server is running on a remote machine, False otherwise.
        """
        if not hasattr(self.server, "ip"):
            return False

        own_ip = get_local_ip()
        dpf_ip = self.server.ip if self.server else ""
        return own_ip != dpf_ip

    def _get_is_same_machine(self) -> bool | None:
        """
        Check if the MAPDL and the DPF instances are running on the same machine.

        Returns
        -------
        bool | None
            True if MAPDL and DPF are running on the same machine, False otherwise.
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
        """Returns True if we are connected to the DPF Server using a gRPC connection to a remote IP.

        Returns
        -------
        bool
            True if we are connected to the DPF Server using a gRPC connection to a remote IP, False otherwise.
        """
        if self._dpf_is_remote is None:
            self._dpf_is_remote = self._get_is_remote()
        return self._dpf_is_remote

    @property
    def _mapdl(self) -> "Mapdl | None":
        """Return the weakly referenced instance of MAPDL.

        Returns
        -------
        Mapdl | None
            The weakly referenced instance of MAPDL, or None if it is not applicable.
        """
        if self._mapdl_weakref:
            return self._mapdl_weakref()

    @property
    def mapdl(self):
        """Return the MAPDL instance

        Returns
        -------
        Mapdl | None
            The weakly referenced instance of MAPDL, or None if it is not applicable.
        """
        return self._mapdl

    @property
    def _log(self) -> Logger:
        """Alias for mapdl logger.

        Returns
        -------
        Logger
            The logger instance.
        """
        if self._logger is None:
            self._logger = LOG
        return self._logger

    @property
    def logger(self) -> Logger:
        """Logger instance

        Returns
        -------
        Logger
            The logger instance.
        """
        return self._log

    @logger.setter
    def logger(self, logger: Logger) -> None:
        """Set the logger instance.

        Parameters
        ----------
        logger : Logger
            The logger instance to set.
        """
        if self.mode_mapdl:
            raise ValueError(
                "Cannot set logger in MAPDL mode. Use the MAPDL instance methods to set the logger instead."
            )
        self._logger = logger

    @property
    def mode(self) -> str:
        """Return the current mode.

        Returns
        -------
        str
            The current mode. Either RST or MAPDL
        """
        return "RST" if self._mode_rst else "MAPDL"

    @property
    def mode_rst(self) -> bool:
        """Return True if the current mode is RST.

        Returns
        -------
        bool
            True if the current mode is RST, False otherwise.
        """
        return bool(self._mode_rst)

    @property
    def mode_mapdl(self) -> bool:
        """Return True if the current mode is MAPDL.

        Returns
        -------
        bool
            True if the current mode is MAPDL, False otherwise.
        """
        return not self._mode_rst

    @property
    def _mapdl_dpf_on_same_machine(self) -> bool:
        """True if the DPF server is running on the same machine as MAPDL.

        Returns
        -------
        bool
            True if the DPF server is running on the same machine as MAPDL, False otherwise.
        """
        if self.__mapdl_and_dpf_on_same_machine is None:
            self.__mapdl_and_dpf_on_same_machine = self._get_is_same_machine()
        return self.__mapdl_and_dpf_on_same_machine

    @property
    def _is_thermal(self) -> bool:
        """Return True if there are TEMP DOF in the solution.

        Returns
        -------
        bool
            True if there are TEMP results in the solution, False otherwise.
        """
        return hasattr(self.model.results, "temperature")

    @property
    def _is_distributed(self) -> bool:
        # raise NotImplementedError("To be implemented by DPF")
        return False  # Hardcoded until DPF exposure

    @property
    def is_distributed(self) -> bool:
        """True when this result file is part of a distributed result

        Only True when Global number of nodes does not equal the
        number of nodes in this file.

        Returns
        -------
        bool
            True if the result file is distributed, False otherwise.

        Notes
        -----
        Not a reliable indicator if a cyclic result.
        """
        return self._is_distributed

    @property
    def _rst(self) -> str:
        if self.mode_mapdl:
            # because it might be remote
            return self.mapdl.result_file

        else:
            return os.path.join(self._rst_directory, self._rst_name)

    @property
    def mapdl_is_local(self) -> bool | None:
        """Return True if the MAPDL instance is local.

        Returns
        -------
        bool | None
            True if the MAPDL instance is local, False otherwise. If the MAPDL instance is not set, None is returned.
        """
        if self._mapdl is not None:
            return self._mapdl.is_local
        return None

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
        self._update(progress_bar=progress_bar, chunk_size=chunk_size)

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
        progress_bar
            Whether print or not the progress bar during the RST file uploading

        chunk_size
            The value of the size of the chunk used to upload the file.

        save
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
        """Returns the DPF model object.

        Returns
        -------
        dpf.model.Model
            DPF model object.
        """
        if self._cached_dpf_model is None or self._update_required:
            self._update()

        return self._cached_dpf_model

    @property
    def metadata(self) -> "dpf.model.Metadata":
        """Metadata from DPF model.

        Returns
        -------
        dpf.model.Metadata
            Metadata from DPF model.
        """
        return self.model.metadata

    @property
    def mesh(self) -> "dpf.MeshedRegion":
        """Mesh from result file.

        Returns
        -------
        dpf.MeshedRegion
            Mesh from result file.
        """
        # TODO: this should be a class equivalent to reader.mesh class.
        return self.model.metadata.meshed_region

    @property
    def grid(self) -> "pv.UnstructuredGrid":
        return self.mesh.grid

    def _get_entities_ids(
        self,
        entities: Entities,
        entity_type: EntityType = "Nodal",
    ) -> Iterable[int | float] | None:
        """Get entities ids given their ids, or component names.

        If a list is given it checks can be int, floats, or list/tuple of int/floats, or
        components (strs, or iterable[strings])

        Parameters
        ----------
        entities : str | int | Iterable[str | int]
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
            entity_type_ = entity_type.title()  # Sanity check

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
            if scoping.location != entity_type_:
                raise ValueError(
                    f"The named selection '{each_named_selection}' does not contain {entity_type_} information."
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

    def _extract_data(self, op: "dpf.Operator") -> ReturnData:
        fc: dpf.Field = op.outputs.fields_as_fields_container()[  # type: ignore
            0
        ]  # This index 0 is the step indexing.

        # When we destroy the operator, we might lose access to the array, that is why we copy.
        ids = fc.scoping.ids.copy()
        data = fc.data.copy()
        return ids, data

    def _extract_field(self, op: "dpf.Operator") -> dpf.Field:
        """Returns the first field from the operator's output."""
        return op.outputs.fields_as_fields_container()[0]

    def _set_rescope(self, op: "dpf.Operator", scope_ids: list[int]) -> "dpf.Operator":
        fc: dpf.FieldsContainer = op.outputs.fields_container()

        rescope = dpf.operators.scoping.rescope()
        rescope.inputs.mesh_scoping(sorted(scope_ids))
        rescope.inputs.fields(fc)
        return rescope

    def _set_mesh_scoping(
        self,
        op: "dpf.Operator",
        mesh: "dpf.MeshedRegion",
        requested_location: EntityType,
        scope_ids: Iterable[int | float] | None = None,
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

    def _set_element_results(self, op: "dpf.Operator", mesh: "dpf.MeshedRegion"):

        fc = op.outputs.fields_container()

        op2 = dpf.operators.averaging.to_elemental_fc(collapse_shell_layers=True)
        op2.inputs.fields_container.connect(fc)
        op2.inputs.mesh.connect(mesh)

        return op2

    def _set_input_timestep_scope(self, op: "dpf.Operator", rnum: Rnum):

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

    def _get_operator(self, result_field: ResultField):
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
        rnum: Rnum,
        result_type: ResultField,
        *,
        in_nodal_coord_sys: bool | None = False,
        nodes: Nodes = None,
        return_operator: bool = False,
        return_field: bool = False,
    ):
        return self._get_result(
            rnum,
            result_type,
            requested_location="Nodal",
            scope_ids=nodes,
            result_in_entity_cs=in_nodal_coord_sys,
            return_operator=return_operator,
            return_field=return_field,
        )

    def _get_elem_result(
        self,
        rnum: Rnum,
        result_type: ResultField,
        *,
        in_element_coord_sys: bool = False,
        elements: Elements = None,
        return_operator: bool = False,
        return_field: bool = False,
    ):
        return self._get_result(
            rnum,
            result_type,
            requested_location="Elemental",
            scope_ids=elements,
            result_in_entity_cs=in_element_coord_sys,
            return_operator=return_operator,
            return_field=return_field,
        )

    def _get_elemnodal_result(
        self,
        rnum: Rnum,
        result_type: ResultField,
        *,
        in_element_coord_sys: bool = False,
        elements: Elements = None,
        return_operator: bool = False,
        return_field: bool = False,
    ):
        return self._get_result(
            rnum,
            result_type,
            requested_location="Elemental_Nodal",
            scope_ids=elements,
            result_in_entity_cs=in_element_coord_sys,
            return_operator=return_operator,
            return_field=return_field,
        )

    @update_result
    def _get_result(
        self,
        *,
        rnum: Rnum,
        result_field: ResultField,
        requested_location: Locations = "Nodal",
        scope_ids: Ids = None,
        result_in_entity_cs: bool = False,
        return_operator: bool = False,
        return_field: bool = False,
    ) -> "dpf.Operator | ReturnData":
        """
        Get elemental/nodal/elementalnodal results.

        Parameters
        ----------
        rnum
            Result step/set

        result_field
            Result type, for example "stress", "strain", "displacement", etc.

        requested_location
            Results given at which type of entity, by default "Nodal"

        scope_ids
            List of entities (nodal/elements) to get the results from, by default None

        result_in_entity_cs
            Obtain the results in the entity coordinate system, by default False

        return_operator
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
        if return_field and return_operator:
            raise ValueError("Cannot return both field and operator.")

        # todo: accepts components in nodes.
        mesh: dpf.MeshedRegion = self.metadata.meshed_region  # type: ignore

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
        scope_ids_ = self._get_entities_ids(scope_ids, requested_location)

        # Set type of return
        ids = self._set_mesh_scoping(op, mesh, requested_location, scope_ids_)  # type: ignore

        if requested_location.lower() == "elemental":
            op = self._set_element_results(
                op, mesh
            )  # overwrite op to be the elemental results OP

        # Applying rescope to make sure the order is right
        if not isinstance(ids, list):
            ids = ids.astype(int).tolist()

        op = self._set_rescope(op, ids)

        if return_operator:
            return op
        elif return_field:
            return self._extract_field(op)
        else:
            return self._extract_data(op)

    @property
    def n_results(self) -> int:
        """Number of results.

        Returns
        -------
        int
            The number of results.
        """
        return self.model.metadata.result_info.n_results

    @property
    def filename(self) -> str:
        """String form of the filename.

        This property can not be changed.

        Returns
        -------
        str
            The string form of the filename.
        """
        return self._rst  # in the reader, this contains the complete path.

    @property
    def pathlib_filename(self) -> pathlib.Path:
        """Return the ``pathlib.Path`` version of the filename.

        This property can not be changed.

        Returns
        -------
        pathlib.Path
            The ``pathlib.Path`` version of the filename.
        """
        return pathlib.Path(self._rst)

    @property
    def nsets(self) -> int:
        """Number of result sets.

        Returns
        -------
        int
            The number of result sets.
        """
        return self.metadata.time_freq_support.n_sets

    def parse_step_substep(self, user_input: int | list[int] | tuple[int, int]) -> int:
        """Converts (step, substep) to a cumulative index.

        Parameters
        ----------
        user_input : int | list[int] | tuple[int, int]
            The input to convert, either a single step number or a (step, substep) tuple.

        Returns
        -------
        int
            The cumulative index corresponding to the input.
        """
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
    def version(self) -> float:
        """The version of MAPDL used to generate this result file.

        Returns
        -------
        float
            The version of MAPDL used to generate this result file.

        Examples
        --------
        >>> mapdl.result.version
        20.1
        """
        return float(self.model.metadata.result_info.solver_version)

    @property
    def n_sector(self) -> int | None:
        """Number of sectors.

        Returns
        -------
        int | None
            The number of sectors, or None if not applicable.
        """
        if self.model.metadata.result_info.has_cyclic:
            return self.model.metadata.result_info.cyclic_support.num_sectors()

    @property
    def num_stages(self) -> int | None:
        """Number of cyclic stages in the model.

        Returns
        -------
        int | None
            The number of cyclic stages, or None if not applicable.
        """
        if self.model.metadata.result_info.has_cyclic:
            return self.model.metadata.result_info.cyclic_support.num_stages

    @property
    def title(self) -> str:
        """Title of model in database

        Returns
        -------
        str
            The title of the model.
        """
        return self.model.metadata.result_info.main_title

    @property
    def is_cyclic(self) -> bool:
        """Indicates if the model is cyclic.

        Returns
        -------
        bool
            True if the model is cyclic, False otherwise.
        """
        return self.model.metadata.result_info.has_cyclic

    @property
    def units(self) -> str:
        """Units of the model.

        Returns
        -------
        str
            The unit system name.
        """
        return self.model.metadata.result_info.unit_system_name

    def __repr__(self) -> str:
        """Representation of the result object.

        Returns
        -------
        str
            A string representation of the result object.
        """
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

    @property
    def available_results(self) -> str:
        """Available result types.

        .. versionchanged:: 0.64
           From 0.64, the MAPDL data labels (i.e. NSL for nodal displacements,
           ENS for nodal stresses, etc) are not included in the output of this command.

        Returns
        -------
        str
            A list of available result types.

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
    def time_values(self) -> list[float]:
        """Values for the time/frequency.

        Returns
        -------
        list[float]
            The time or frequency values.
        """
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

    @property
    def _elements(self):
        return self.mesh.elements.scoping.ids

    def element_lookup(self, element_id: int) -> int:
        """Index of the element within the result mesh.

        Parameters
        ----------
        element_id : int
            The element ID to look up.

        Returns
        -------
        int
            The index of the element within the result mesh.
        """
        mapping = dict(zip(self._elements, np.arange(self.mesh.elements.n_elements)))
        if element_id not in mapping:
            raise KeyError(
                f"Element ID {element_id} not found in the result mesh. "
                f"Available element IDs: {list(mapping.keys())}"
            )

        return int(mapping[element_id])

    def solution_info(self, rnum: Rnum) -> dict[str, Any]:
        """Return an informative dictionary of solution data for a
        result.

        .. warning:: This method has not been ported to the new DPF-based Results backend
           and it is kept here for future references.
           If you still want to use it, you can switch to 'pymapdl-reader' backend by setting
           `mapdl.use_reader_backend=True`.

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
        raise NotImplementedInDPFBackend(method="solution_info")

    @property
    def subtitle(self) -> str:
        """Subtitle of the model in the database.

        .. warning:: This method has not been ported to the new DPF-based Results backend
           and it is kept here for future references.
           If you still want to use it, you can switch to 'pymapdl-reader' backend by setting
           `mapdl.use_reader_backend=True`.

        Returns
        -------
        str
            Subtitle of the model.
        """
        raise NotImplementedInDPFBackend(method="subtitle")

    def _get_comp_dict(self, entity: str) -> dict[str, tuple[int]]:
        """Get a dictionary of components given an entity

        Parameters
        ----------
        entity
            The entity type to retrieve components for. Valid options are
            "NODE" and "ELEM".

        Returns
        -------
        dict
            Dictionary of components.  Keys are the component names,
            and values are tuples of the entity IDs in the component.
        """
        entity_comp = {}
        for each_comp in self.mesh.available_named_selections:
            scoping = self.mesh.named_selection(each_comp)
            if scoping.location == LOCATION_MAPPING[entity]:
                entity_comp[each_comp] = tuple(scoping.ids.tolist())

        return entity_comp

    @property
    def node_components(self) -> dict[str, np.ndarray]:
        """Dictionary of ansys node components from the result file.

        Returns
        -------
        dict
            Dictionary of node components.  Keys are the component
            names, and values are the node numbers in the component.

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
    def element_components(self) -> dict[str, np.ndarray]:
        """Dictionary of ansys element components from the result file.

        Returns
        -------
        dict
            Dictionary of element components.  Keys are the component
            names, and values are the element numbers in the component.

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

    def _component_selector(
        self, fc: dpf.Field, component: str | int | None = None
    ) -> "dpf.Field":
        """Selects a component from a field.

        Parameters
        ----------
        fc : dpf.Field
            The field to select the component from.

        component : str or int, optional
            The component name or index to select. If None, it defaults to the first component (generally X)

        Returns
        -------
        dpf.Field
            The selected component field.
        """
        if component is None:
            component = 0

        if isinstance(component, str):
            if component not in COMPONENTS:
                raise ValueError(
                    f"The component '{component}' is not a valid component. "
                    f"Available components are: {COMPONENTS}"
                )

            component = COMPONENTS.index(component)

        return dpf.operators.logic.component_selector(
            field=fc, component_number=component
        ).eval()
