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


"""The files MAPDL core responsibility mixin."""

import logging
import os
import pathlib

# Subprocess is needed to start the backend. But
# the input is controlled by the library. Excluding bandit check.
from typing import TYPE_CHECKING, Any, Dict, List, Literal, Optional, Tuple, Union
from uuid import uuid4
from warnings import warn

from ansys.mapdl import core as pymapdl
from ansys.mapdl.core import _HAS_DPF
from ansys.mapdl.core.errors import MapdlExitedError, MapdlRuntimeError
from ansys.mapdl.core.misc import run_as, supress_logging

if TYPE_CHECKING:  # pragma: no cover
    if _HAS_DPF:
        pass


from . import _CoreMixinBase
from .constants import SESSION_ID_NAME


class _CoreFileMixin(_CoreMixinBase):
    """Static responsibility mixin for the MAPDL core facade."""

    def _wrap_directory(self, path: Union[str, pathlib.Path]) -> pathlib.PurePath:
        if self.platform is None:
            # MAPDL is not initialized yet so returning the path as is.
            return pathlib.PurePath(path)

        if self.platform == "windows":
            # Windows path
            return pathlib.PureWindowsPath(path)
        elif self.platform == "linux":
            # Linux path
            return pathlib.PurePosixPath(path)
        else:
            # Other OS path
            warn(
                f"MAPDL is running on an unknown OS '{self.platform}'. "
                "Using PurePosixPath as default.",
                UserWarning,
            )
            # Default to PurePosixPath
            # This is a fallback, it should not happen.
            # If it does, it is probably a bug.
            return pathlib.PurePosixPath(path)

    @property
    @supress_logging
    def directory(self) -> pathlib.PurePath:
        """
        Current MAPDL directory.

        Examples
        --------
        Directory on Linux

        >>> mapdl.directory
        '/tmp/ansys'

        Directory on Windows

        >>> mapdl.directory
        'C:/temp_directory/'

        Setting the directory

        >>> mapdl.directory = 'C:/temp_directory/'
        None

        In case the directory does not exist or it is not
        accessible, ``cwd`` (:func:`MapdlBase.cwd`) will raise
        a warning.
        """
        # Inside inquire there is already a retry mechanisim
        path = None
        try:
            path = self.inquire("", "DIRECTORY")
        except MapdlExitedError:
            # Let's return the cached path
            pass

        # os independent path format
        if path:  # self.inquire might return ''.
            path = path.replace("\\", "/")
            # new line to fix path issue, see #416
            path = repr(path)[1:-1]
            self._path = self._wrap_directory(path)

        elif not self._path:
            raise MapdlRuntimeError(
                f"MAPDL could NOT provide a path using /INQUIRE or the cached path ('{self._path}')."
            )

        return self._path

    @directory.setter
    @supress_logging
    def directory(self, path: Union[str, pathlib.Path]) -> None:
        """Change the directory using ``Mapdl.cwd``"""
        self.cwd(path)
        self._path = self._wrap_directory(path)

    def open_apdl_log(
        self, filename: Union[str, pathlib.Path], mode: Literal["w", "a", "x"] = "w"
    ) -> None:
        """Start writing all APDL commands to an MAPDL input file.

        Parameters
        ----------
        filename : str
            Filename of the log.
        mode : str, optional
            Python file modes (for example, ``'a'``, ``'w'``).  Should
            be either write or append.

        Examples
        --------
        Begin writing APDL commands to ``"log.inp"``.

        >>> mapdl.open_apdl_log("log.inp")
        """
        if self._apdl_log is not None:  # type: ignore[has-type]  # Set by _MapdlCore.__init__.
            raise MapdlRuntimeError("APDL command logging already enabled")
        self._log.debug("Opening ANSYS log file at %s", filename)

        if mode not in ["w", "a", "x"]:
            raise ValueError(
                "File mode should either be write, append, or exclusive"
                " creation ('w', 'a', or 'x')."
            )

        self._apdl_log = open(filename, mode=mode, buffering=1)  # type: ignore[misc,no-redef]  # line buffered
        if self._apdl_log is None:
            raise MapdlRuntimeError("Failed to open APDL log file.")
        self._apdl_log.write(
            f"! APDL log script generated using PyMAPDL (ansys.mapdl.core {pymapdl.__version__})\n"
        )

    @supress_logging
    @run_as("PREP7")
    def _generate_iges(self):
        """Save IGES geometry representation to disk"""
        filename = self.directory / "_tmp.iges"
        self.igesout(filename, att=1, mute=True)
        return filename

    def _launch(self, *args, **kwargs):  # pragma: no cover
        raise NotImplementedError("Implemented by child class")

    def _close_apdl_log(self):
        """Closes the APDL log"""
        if self._apdl_log is not None:
            self._apdl_log.close()
        self._apdl_log = None

    def add_file_handler(self, filepath, append=False, level="DEBUG"):
        """Add a file handler to the mapdl log.  This allows you to
        redirect the APDL logging to a file.

        Parameters
        ----------
        filepath : str
            Filename of the log.

        append : bool
            When ``True``, appends to an existing log file.  When
            ``False``, overwrites the log file if it already exists.

        level : str
            Log level.  Must be one of: ``'DEBUG', 'INFO', 'WARNING', 'ERROR'``.

        Examples
        --------
        Start writing the log to a new file named "mapdl.log"

        >>> mapdl.add_file_handler('mapdl.log')
        """
        if append:
            mode = "a"
        else:
            mode = "w"

        self._log_filehandler = logging.FileHandler(filepath)
        formatstr = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"

        self._log_filehandler = logging.FileHandler(filepath, mode=mode)
        self._log_filehandler.setFormatter(logging.Formatter(formatstr))
        if isinstance(level, str):
            level = level.upper()
        self._log_filehandler.setLevel(level)
        self._log.logger.addHandler(self._log_filehandler)
        self._log.info("Added file handler at %s", filepath)

    def remove_file_handler(self):
        """Removes the filehander from the log"""
        self._log.removeHandler(self._log_filehandler)
        self._log.info("Removed file handler")

    def _cleanup_loggers(self):
        """Clean up all the loggers.

        Notes
        -----
        Only ever call this from the explicit, deterministic :meth:`exit`
        path (through ``_release_resources(cleanup_loggers=True)``), never
        from ``__del__``/garbage collection. This instance's logger and its
        handlers are shared, process-wide ``logging`` state (see
        :class:`ansys.mapdl.core.logging.Logger`), so closing them from
        non-deterministic GC-driven code can race with another, still-alive
        ``Mapdl`` instance still logging through the same handler.
        """
        logger = self._log
        logger.setLevel(logging.CRITICAL + 1)

        if logger.hasHandlers():
            for each_handler in logger.logger.handlers:
                if each_handler.stream and not each_handler.stream.closed:
                    logger.logger.removeHandler(each_handler)

        if logger.file_handler:
            logger.file_handler.close()
            logger.file_handler = None

        if logger.std_out_handler:
            logger.std_out_handler.close()
            logger.std_out_handler = None

    def _check_mapdl_os(self):
        platform = self.get_value("active", 0, "platform").strip()
        if "l" in platform.lower():
            self._platform = "linux"
        elif "w" in platform.lower():  # pragma: no cover
            self._platform = "windows"
        else:  # pragma: no cover
            raise MapdlRuntimeError("Unknown platform: {}".format(platform))
        self.logger.debug(f"MAPDL is running on {self._platform} OS.")

    def _check_on_docker(self):
        """Check if MAPDL is running on docker."""
        # self.get_mapdl_envvar("ON_DOCKER") # for later
        if not self.is_grpc:  # pragma: no cover
            return False

        if self.platform == "linux":
            self.sys(
                r"if grep -sq 'docker\|lxc' /proc/1/cgroup; then echo 'true' > __outputcmd__.txt; else echo 'false' > __outputcmd__.txt;fi;"
            )
        elif self.platform == "windows":  # pragma: no cover
            return False  # TODO: check if it is running a windows docker container. So far it is not supported.

        if not self.is_local:
            sys_output = self._download_as_raw("__outputcmd__.txt").decode().strip()

        else:
            file_ = self.directory / "__outputcmd__.txt"
            with open(file_, "r") as f:
                sys_output = f.read().strip()

        self._log.debug(f"The output of sys command is: '{sys_output}'.")
        self.slashdelete("__outputcmd__.txt")  # cleaning
        return sys_output == "true"

    def _decompose_fname(
        self, fname: Union[str, pathlib.Path]
    ) -> Tuple[str, str, pathlib.Path]:
        """Decompose a file name (with or without path) into filename and extension.

        Parameters
        ----------
        fname : str or pathlib.Path
            File name with or without path.

        Returns
        -------
        str
            File name (without extension or path)

        str
            File extension (without dot)

        pathlib.Path
            File path
        """
        fname_path = pathlib.Path(fname)
        return (fname_path.stem, fname_path.suffix.replace(".", ""), fname_path.parent)

    def _parse_cmlist(
        self, cmlist: Optional[str] = None
    ) -> Tuple[Dict[str, Any], Dict[str, List[str]]]:
        from ansys.mapdl.core.component import _parse_cmlist

        if not cmlist:
            cmlist = self.cmlist()

        return _parse_cmlist(cmlist)

    def _parse_cmlist_indiv(
        self, cmname: str, cmtype: str, cmlist: Optional[str] = None
    ) -> List[int]:
        from ansys.mapdl.core.component import _parse_cmlist_indiv

        if not cmlist:
            cmlist = self.cmlist(cmname, 1)

        return _parse_cmlist_indiv(cmname, cmtype, cmlist)

    def _get_file_path(self, fname: str, progress_bar: bool = False) -> str:
        """Find files in the Python and MAPDL working directories.

        **The priority is for the Python directory.**

        Hence if the same file is in the Python directory and in the MAPDL directory,
        PyMAPDL will upload a copy from the Python directory to the MAPDL directory,
        overwriting the MAPDL directory copy.
        """

        if os.path.isdir(fname):
            raise ValueError(
                f"`fname` should be a full file path or name, not the directory '{fname}'."
            )

        fPath = pathlib.Path(fname)

        fpath = os.path.dirname(fname)
        fname = fPath.name
        fext = fPath.suffix

        # if there is no dirname, we are assuming the file is
        # in the python working directory.
        if not fpath:
            fpath = os.getcwd()

        ffullpath = os.path.join(fpath, fname)

        if os.path.exists(ffullpath) and self._local:
            return ffullpath

        if self._local:
            if os.path.isfile(fname):
                # And it exists
                filename = os.path.join(os.getcwd(), fname)
            elif not self._store_commands and fname in self.list_files():
                # It exists in the Mapdl working directory
                filename = self.directory / fname
            elif self._store_commands:
                # Assuming that in non_interactive we have uploaded the file
                # manually.
                filename = self.directory / fname
            else:
                # Finally
                raise FileNotFoundError(f"Unable to locate filename '{fname}'")

        else:  # Non-local
            # upload the file if it exists locally
            if os.path.isfile(ffullpath):
                self.upload(ffullpath, progress_bar=progress_bar)
                filename = fname

            elif not self._store_commands and fname in self.list_files():
                # It exists in the Mapdl working directory
                filename = fname

            elif self._store_commands:
                # Assuming that in non_interactive, the file exists already in
                # the Mapdl working directory
                filename = fname

            else:
                raise FileNotFoundError(f"Unable to locate filename '{fname}'")

        return filename

    def _get_file_name(
        self,
        fname: str | pathlib.PurePath,
        ext: Optional[str] = None,
        default_extension: Optional[str] = None,
    ) -> str:
        """Get file name from fname and extension arguments.

        fname can be the full path.

        Parameters
        ----------
        fname : str
            File name (with or without extension). It can be a full path.

        ext : str, optional
            File extension. The default is None.

        default_extension : str
            Default filename extension. The default is None.
        """

        # the old behaviour is to supplied the name and the extension separately.
        # to make it easier let's going to allow names with extensions
        if not isinstance(fname, str):
            fname = str(fname)

        # Sanitizing ext
        while ext and ext[0] == ".":
            ext = ext[1:]

        if ext:
            fname = fname + "." + ext
        else:
            basename = os.path.basename(fname)

            if len(basename.split(".")) == 1 and default_extension:
                # there is no extension in the main name.
                fname = fname + "." + default_extension

        return fname

    def list_files(self, refresh_cache: bool = True) -> List[str]:
        """List the files in the working directory of MAPDL.

        Parameters
        ----------
        refresh_cache : bool, optional
            If local, refresh local cache by querying MAPDL for its
            current path.

        Returns
        -------
        list
            List of files in the working directory of MAPDL.

        Examples
        --------
        >>> files = mapdl.list_files()
        >>> for file in files: print(file)
        file.lock
        file0.bat
        file0.err
        file0.log
        file0.page
        file1.err
        file1.log
        file1.out
        file1.page
        """
        if self._local:  # simply return a python list of files
            if refresh_cache:
                local_path = self.directory
            else:
                local_path = self._directory
            if local_path and os.path.isdir(local_path):
                return os.listdir(local_path)
            return []

        elif self.exited:
            raise MapdlExitedError("Cannot list remote files since MAPDL has exited")

        # this will sometimes return 'LINUX x6', 'LIN', or 'L'
        if "L" in self.parameters.platform[:1]:
            cmd = "ls"
        else:
            cmd = "dir /b /a"

        files = self.sys(cmd).splitlines()
        if not files:
            warn("No files listed")
        return files

    def _create_session(self):
        """Generate a session ID."""
        id_ = uuid4()
        id_ = str(id_)[:31].replace("-", "")
        self._session_id_ = id_
        self._run(f"{SESSION_ID_NAME}='{id_}'")

    @property
    def _session_id(self):
        """Return the session ID."""
        return self._session_id_

    def _check_session_id(self):
        """Verify that the local session ID matches the remote MAPDL session ID."""
        if self._checking_session_id_ or not self._strict_session_id_check:
            # To avoid recursion error
            return

        pymapdl_session_id = self._session_id
        if not pymapdl_session_id:
            # We return early if pymapdl_session is not fixed yet.
            return

        self._checking_session_id_ = True
        self._mapdl_session_id = self._get_mapdl_session_id()

        self._checking_session_id_ = False

        if pymapdl_session_id is None or self._mapdl_session_id is None:
            return
        elif self._strict_session_id_check:
            if pymapdl_session_id != self._mapdl_session_id:
                self._log.error("The session ids do not match")

            else:
                self._log.debug("The session ids match")
                return True
        else:
            return pymapdl_session_id == self._mapdl_session_id

    def _get_mapdl_session_id(self):
        """Retrieve MAPDL session ID."""
        from ansys.mapdl.core.parameters import interp_star_status

        try:
            parameter = interp_star_status(
                self._run(f"*STATUS,{SESSION_ID_NAME}", mute=False)
            )
        except AttributeError:
            return None

        if parameter:
            return parameter[SESSION_ID_NAME]["value"]
        return None
