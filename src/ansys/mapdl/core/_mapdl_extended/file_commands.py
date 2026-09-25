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


"""The file commands MAPDL extended mixin."""

import os
import pathlib
import shutil
from functools import wraps

from ansys.mapdl.core.errors import (
    IncorrectWorkingDirectory,
    MapdlCommandIgnoredError,
    MapdlRuntimeError,
)
from ansys.mapdl.core.mapdl_core import _MapdlCore

from . import _ExtendedMixinBase


class _ExtendedFileCommandsMixin(_ExtendedMixinBase):
    """Static responsibility mixin for the extended MAPDL facade."""

    @wraps(_MapdlCore.file)
    def file(self, fname: str = "", ext: str = "", **kwargs) -> str:
        """Wraps file to upload the file to the MAPDL working directory."""
        fname = self._get_file_name(fname, ext, "cdb")
        fname = self._get_file_path(fname, kwargs.get("progress_bar", False))
        file_, ext_, path_ = self._decompose_fname(fname)

        if self._local:
            return getattr(super(), "file")(fname=path_ / file_, ext=ext_, **kwargs)
        else:
            return getattr(super(), "file")(fname=file_, ext=ext_, **kwargs)

    @wraps(_MapdlCore.lsread)
    def lsread(self, *args, **kwargs):
        """Wraps the ``LSREAD`` which does not work in interactive mode.

        Parameters
        ----------
        *args : tuple
            Positional arguments to pass to the LSREAD command.
        **kwargs : dict
            Keyword arguments to pass to the LSREAD command.

        Returns
        -------
        str
            Command output from MAPDL.
        """
        self._log.debug("Forcing 'LSREAD' to run in non-interactive mode.")
        with self.non_interactive:
            super().lsread(*args, **kwargs)
        return self._response.strip()

    @wraps(_MapdlCore.use)
    def use(self, *args, **kwargs):
        """Wrap the use command.

        Parameters
        ----------
        *args : tuple
            Positional arguments to pass to the USE command.
        **kwargs : dict
            Keyword arguments to pass to the USE command.

        Returns
        -------
        str
            Command output from MAPDL.
        """
        # Because of `name` can be a macro file or a macro block on a macro library
        # file, we are going to test if the file exists locally first, then remote,
        # and if not, silently assume that it is a macro in a macro library.
        # I do not think there is a way to check if the macro exists before use it.
        if "name" in kwargs:
            name = kwargs.pop("name")
        else:
            if len(args) < 1:
                raise ValueError("Missing `name` argument")
            name = args[0]

        base_name = os.path.basename(name)

        # Check if it is a file local
        if os.path.exists(name):
            self.upload(name)

        elif base_name in self.list_files():
            # the file exists in the MAPDL working directory, so do nothing.
            pass

        else:
            if os.path.dirname(name):
                # It seems you provided a path (or something like that)
                raise FileNotFoundError(
                    f"The name supplied to 'mapdl.use' ('{name}') is not a file in the Python "
                    "working directory, nor in the MAPDL working directory. "
                )
            # Preferring logger.warning over warn (from warnings), since it is less intrusive.
            self._log.warning(
                f"The name supplied to 'mapdl.use' ('{name}') is not a file in the Python "
                "working directory, nor in the MAPDL working directory. "
                "PyMAPDL will assume it is a macro block inside a macro library "
                "file previously defined using 'mapdl.ulib'."
            )
            # If MAPDL cannot find named macro file, it will throw a runtime error.

        # Update arg because the path is no longer needed
        args = (base_name, *args[1:])

        with self.non_interactive:
            super().use(*args, **kwargs)

        return self._response  # returning last response

    @wraps(_MapdlCore.mpwrite)
    def mpwrite(
        self,
        fname="",
        ext="",
        lib="LIB",
        mat="",
        download_file=False,
        progress_bar=False,
        **kwargs,
    ):
        fname_ = fname + "." + ext
        if not self._local:
            if os.path.dirname(fname_):
                raise IOError(
                    "Only writing files to the MAPDL working directory is allowed. "
                    f"The supplied path {fname_} is not allowed."
                )

        output = super().mpwrite(fname, ext, lib=lib, mat=mat, **kwargs)
        if download_file:
            self.download(os.path.basename(fname_), progress_bar=progress_bar)

        return output

    def mpread(self, fname="", ext="", lib="", **kwargs):
        """APDL Command: MPREAD

        Reads a file containing material properties.

        Parameters
        ----------
        fname
            File name and directory path (248 characters maximum,
            including directory). If you do not specify the ``LIB``
            option, the default directory is the current working
            directory. If you specify the ``LIB`` option, the default is
            the following search path: the current working directory,
            the user's home directory, ``MPLIB_DIR`` (as specified by the
            ``/MPLIB,READ,PATH`` command) and ``/ansys_dir/matlib`` (as
            defined by installation). If you use the default for your
            directory, you can use all 248 characters for the file
            name.

        ext
            Filename extension (eight-character maximum).

        lib
            Reads material library files previously written with the
            MPWRITE command.  (See the description of the ``LIB`` option
            for the ``MPWRITE`` command.)  The only allowed value for ``LIB``
            is ``LIB``.

            .. note:: The argument "LIB" is not supported by the MAPDL gRPC server.

        Notes
        -----
        Material properties written to a file without the ``LIB`` option
        do not support nonlinear properties.  Also, properties written
        to a file without the ``LIB`` option are restored in the same
        material number as originally defined.  To avoid errors, use
        ``MPREAD`` with the ``LIB`` option only when reading files written
        using MPWRITE with the ``LIB`` option.

        If you omit the ``LIB`` option for ``MPREAD``, this command supports
        only linear properties.

        Material numbers are hardcoded.  If you write a material file
        without specifying the ``LIB`` option, then read that file in
        using the ``MPREAD`` command with the ``LIB`` option, the ANSYS
        program will not write the file to a new material number.
        Instead, it will write the file to the "old" material number
        (the number specified on the MPWRITE command that created the
        file.)

        This command is also valid in SOLUTION.
        """
        if lib:
            raise NotImplementedError(
                "The 'lib' argument is not supported by the MAPDL gRPC server."
            )

        fname = self._get_file_name(fname, ext, "mp")
        fname = self._get_file_path(fname, kwargs.get("progress_bar", False))
        file_, ext_, path_ = self._decompose_fname(fname)
        with self.non_interactive:
            # Use not interactive to avoid gRPC issues. See #975
            if self._local:
                # If local, we can use the full path
                super().mpread(fname=path_ / file_, ext=ext_, lib=lib, **kwargs)
            else:
                super().mpread(fname=file_, ext=ext_, lib=lib, **kwargs)

        return self.last_response

    @wraps(_MapdlCore.cwd)
    def cwd(self, *args, **kwargs):
        """Wraps cwd.

        Returns
        -------
        str
            Command output from MAPDL.
        """
        try:
            output = super().cwd(*args, mute=False, **kwargs)
        except MapdlCommandIgnoredError as e:
            raise IncorrectWorkingDirectory(e.args[0])

        self._path = self._wrap_directory(args[0])  # caching
        return output

    @wraps(_MapdlCore.list)
    def list(self, filename, ext=""):
        if hasattr(self, "_local"):  # gRPC
            if not self._local:
                return self._download_as_raw(filename).decode()

        path = pathlib.Path(filename)
        if path.parent != ".":
            path = self.directory / filename

        path = str(path) + ext
        with open(path) as fid:
            return fid.read()

    @wraps(_MapdlCore.parres)
    def parres(self, lab="", fname="", ext="", **kwargs):
        """Wraps the original /PARRES function"""
        if not fname:
            fname = self.jobname

        fname = self._get_file_name(
            fname=fname, ext=ext, default_extension="parm"
        )  # Although documentation says `PARM`

        # Getting the path for local/remote
        filename = self._get_file_path(fname, progress_bar=False)

        return self.input(filename)

    @wraps(_MapdlCore.lgwrite)
    def lgwrite(self, fname="", ext="", kedit="", remove_grpc_extra=True, **kwargs):
        """Wraps original /LGWRITE"""
        if not fname:
            fname = self.jobname

        fname = self._get_file_name(fname=fname, ext=ext, default_extension="lgw")

        if self.is_local:
            fname_ = fname
        else:
            file_, ext_, _ = self._decompose_fname(fname)
            fname_ = self._get_file_name(fname=file_, ext=ext_)

        # generate the log and download if necessary
        output = super().lgwrite(fname=fname_, ext="", kedit=kedit, **kwargs)

        # Let's download the file to the location
        if self.is_local:
            src = pathlib.Path(self.directory / fname_)
            dst = pathlib.Path(fname).resolve()
            if src.resolve() != dst:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(src, fname)
        else:
            self._download(fname_, fname)
        fname_ = fname  # Update path

        # remove extra grpc /OUT commands
        REMOVE_LINES = ("/OUT", "/OUT,anstmp")
        REMOVE_LINES_STARTING = (
            "*SET,__PYMAPDL_SESSION_ID__",
            "! *STATUS,__PYMAPDL_SESSION_ID__",
            "*STATUS,__PYMAPDL_SESSION_ID__",
        )

        if remove_grpc_extra and self.is_grpc:
            with open(fname_, "r") as fid:
                lines = [
                    line.strip() + "\n"
                    for line in fid
                    if (
                        line.strip() not in REMOVE_LINES
                        and not line.startswith(REMOVE_LINES_STARTING)
                    )
                ]

            with open(fname_, "w") as fid:
                fid.writelines(lines)

        return output

    @wraps(_MapdlCore.vwrite)
    def vwrite(
        self,
        par1="",
        par2="",
        par3="",
        par4="",
        par5="",
        par6="",
        par7="",
        par8="",
        par9="",
        par10="",
        par11="",
        par12="",
        par13="",
        par14="",
        par15="",
        par16="",
        par17="",
        par18="",
        par19="",
        **kwargs,
    ):
        """Wrapping *VWRITE"""

        # cannot be run in interactive mode
        if not self._store_commands:
            raise MapdlRuntimeError(
                "*VWRITE cannot run interactively.  \n\nPlease use "
                "``with mapdl.non_interactive:``"
            )

        return super().vwrite(
            par1=par1,
            par2=par2,
            par3=par3,
            par4=par4,
            par5=par5,
            par6=par6,
            par7=par7,
            par8=par8,
            par9=par9,
            par10=par10,
            par11=par11,
            par12=par12,
            par13=par13,
            par14=par14,
            par15=par15,
            par16=par16,
            par17=par17,
            par18=par18,
            par19=par19,
            **kwargs,
        )

    @wraps(_MapdlCore.mwrite)
    def mwrite(
        self, parr="", fname="", ext="", label="", n1="", n2="", n3="", **kwargs
    ):
        """Wrapping *MWRITE"""

        # cannot be run in interactive mode
        if not self._store_commands:
            raise MapdlRuntimeError(
                "*MWRITE cannot run interactively.  \n\nPlease use "
                "``with mapdl.non_interactive:``"
            )

        return super().mwrite(
            parr=parr,
            fname=fname,
            ext=ext,
            label=label,
            n1=n1,
            n2=n2,
            n3=n3,
            **kwargs,
        )
