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

import os
import pathlib

# Subprocess is needed to start the backend. But
# the input is controlled by the library. Excluding bandit check.
from typing import TYPE_CHECKING, Any, Dict, List, Literal, Optional, Tuple, Union
from warnings import warn

from ansys.mapdl.core import _HAS_DPF
from ansys.mapdl.core.errors import MapdlExitedError, MapdlRuntimeError
from ansys.mapdl.core.misc import supress_logging

if TYPE_CHECKING:  # pragma: no cover
    if _HAS_DPF:
        pass


from . import _CoreMixinBase


class _CoreFileMixin(_CoreMixinBase):
    """Static responsibility mixin for the MAPDL core facade."""
    @property
    def _lockfile(self):
        """Lockfile path"""
        path = self.directory
        if path is not None:
            return path / f"{self.jobname}.lock"

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

