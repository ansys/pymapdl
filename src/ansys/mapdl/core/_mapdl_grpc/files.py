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

"""File transfer between the client and the MAPDL working directory."""

import fnmatch
import glob
import os
from pathlib import Path, PurePath, PurePosixPath
import re
import shutil
import tempfile
from typing import (
    List,
    Literal,
    Optional,
    Tuple,
    Union,
)
from warnings import warn

from ansys.api.mapdl.v0 import mapdl_pb2 as pb_types

from ansys.mapdl.core import _HAS_TQDM
from ansys.mapdl.core._mapdl_grpc.transport import (
    chunk_raw,
    get_file_chunks,
    save_chunks_to_file,
)
from ansys.mapdl.core.constants import DEFAULT_CHUNKSIZE
from ansys.mapdl.core.errors import (
    MapdlExitedError,
    protect_grpc,
)
from ansys.mapdl.core.misc import (
    last_created,
    run_as,
    supress_logging,
)

from . import _GrpcMixinBase


class _GrpcFileMixin(_GrpcMixinBase):
    """File transfer between the client and the MAPDL working directory."""

    def download_result(
        self,
        path: str | Path | None = None,
        progress_bar: bool = False,
        preference: Literal["rst", "rth"] | None = None,
    ) -> str:
        """Download remote result files to a local directory

        Parameters
        ----------
        path
            Path where the files are downloaded, by default the current
            python path (``os.getcwd()``)

        progress_bar
            Show the progress bar or not, default to False.

        preference
            Preferred type for the result file, which is either ``rst`` or ``rth``.
            This parameter is only required when both files are present. The default is ```None``,
            in which case ``"rst"`` is used.

        Returns
        -------
        list[str]
            List of downloaded files.

        Examples
        --------
        Download remote result files into the current working directory

        >>> import os
        >>> mapdl.download_result(os.getcwd())
        """
        if path is None:  # if not path seems to not work in same cases.
            path = os.getcwd()

        def _download(targets: List[str]) -> None:
            for target in targets:
                save_name = os.path.join(path, target)
                self._download(target, save_name, progress_bar=progress_bar)

        if preference:
            if preference not in ["rst", "rth"]:
                raise ValueError("``preference`` must be either 'rst' or 'rth'")

        # result file basename is the jobname
        jobname = self.jobname
        rth_basename = "%s.%s" % (jobname, "rth")
        rst_basename = "%s.%s" % (jobname, "rst")

        remote_files = self.list_files()
        result_file = None

        if self._prioritize_thermal and rth_basename in remote_files:
            result_file = rth_basename
        elif rst_basename in remote_files and rth_basename in remote_files:
            if preference == "rth":
                result_file = rth_basename
            else:
                result_file = rst_basename
        elif rst_basename in remote_files:
            result_file = rst_basename
        elif rth_basename in remote_files:
            result_file = rth_basename

        if result_file:  # found non-distributed result
            save_name = os.path.join(path, result_file)
            self._download(result_file, save_name, progress_bar=progress_bar)
            return save_name

        # otherwise, download all the distributed result files
        if jobname[-1].isnumeric():
            jobname += "_"

        rst_files = []
        rth_files = []
        for filename in remote_files:
            if "rst" in filename and jobname in filename:
                rst_files.append(filename)
            elif "rth" in filename and jobname in filename:
                rth_files.append(filename)

        if self._prioritize_thermal and rth_files:
            targets = rth_files
        else:
            if rst_files and rth_files:
                if preference is None:
                    raise ValueError(
                        "Found both structural and thermal results files."
                        "\nPlease specify which kind to download using:\n"
                        '``preference="rth"`` or ``preference="rst"``'
                    )
                if preference == "rst":
                    targets = rst_files
                elif preference == "rth":
                    targets = rth_files
            elif rst_files:
                preference = "rst"
                targets = rst_files
            elif rth_files:
                preference = "rth"
                targets = rth_files
            else:
                remote_files_str = "\n".join("\t%s" % item for item in remote_files)
                raise FileNotFoundError(
                    "Unable to locate any result file from the "
                    "following remote result files:\n\n" + remote_files_str
                )
        _download(targets)
        return os.path.join(path, jobname + "0." + preference)

    def download_project(
        self,
        extensions: Optional[Union[str, List[str], Tuple[str]]] = None,
        target_dir: Optional[str] = None,
        progress_bar: bool = False,
    ) -> List[str]:
        """Download all the project files located in the MAPDL working directory.

        Parameters
        ----------
        extensions : List[str], Tuple[str], optional
            List of extensions to filter the files before downloading,
            by default None.

        target_dir : str, optional
            Path to downloaded the files will to. The default is ``None``.

        progress_bar : bool, optional
            Display a progress bar using
            ``tqdm`` when ``True``.  Helpful for showing download
            progress. The default is ``False``.

        Returns
        -------
        List[Str]
            List of downloaded files.
        """
        if not extensions:
            list_of_files = self.download(
                files="*", target_dir=target_dir, progress_bar=progress_bar
            )

        else:
            list_of_files = []
            for each_extension in extensions:
                list_of_files.extend(
                    self.download(
                        files="*",
                        target_dir=target_dir,
                        extension=each_extension,
                        progress_bar=progress_bar,
                    )
                )

        return list_of_files

    def download(
        self,
        files: str | list[str] | tuple[str, ...],
        target_dir: str | None = None,
        extension: str | None = None,
        chunk_size: int | None = None,
        progress_bar: bool | None = None,
        recursive: bool = False,
    ) -> list[str]:
        """Download files from the gRPC instance working directory

        .. warning:: This feature is only available for MAPDL 2021R1 or newer.

        Parameters
        ----------
        files
            Name of the file on the server. File must be in the same
            directory as the mapdl instance. A list of string names or
            tuples of string names can also be used.
            List current files with :meth:`Mapdl.list_files <MapdlGrpc.list_files>`.

            Alternatively, you can also specify **glob expressions** to
            match file names. For example: `'file*'` to match every file whose
            name starts with `'file'`.

        target_dir
            Path where the downloaded files will be located. The default is the current
            working directory.

        extension
            Filename with this extension will be considered. The default is None.

        chunk_size
            Chunk size in bytes.  Must be less than 4MB. The default is 256 kB.

        progress_bar
            Display a progress bar using ``tqdm`` when ``True``.
            Helpful for showing download progress.

        recursive
            Whether to use recursion when using glob pattern. The default is ``False``.

        Returns
        -------
        list[str]
            List of downloaded files.

        Notes
        -----
        There are some considerations to keep in mind when using this command:

        * The glob pattern search does not search recursively in remote instances.
        * You can download a specific file located in a subdirectory of the
          MAPDL working directory by giving its relative path, for example
          ``'subdir/file.rst'``.
        * In a remote instance, it is not possible to list or download files in different
          locations than the MAPDL working directory.
        * If you are in local and provide a file path, downloading files
          from a different folder is allowed.
          However it is not a recommended approach.

        Examples
        --------
        Download a single file:

        >>> mapdl.download('file.out')

        Download all the files starting with `'file'`:

        >>> mapdl.download('file*')

        Download every single file in the MAPDL working directory:

        >>> mapdl.download('*.*')

        Alternatively, you can download all the files using
        :func:`Mapdl.download_project <ansys.mapdl.core.mapdl_grpc.MapdlGrpc.download_project>` (recommended):

        >>> mapdl.download_project()
        """
        if chunk_size is None:
            chunk_size = DEFAULT_CHUNKSIZE

        if chunk_size > 4 * 1024 * 1024:  # 4MB
            raise ValueError(
                f"Chunk sizes bigger than 4 MB can generate unstable behaviour in PyMAPDL. "
                "Please decrease ``chunk_size`` value."
            )

        if target_dir:
            try:
                os.mkdir(os.path.abspath(target_dir))
            except FileExistsError:
                pass
        else:
            target_dir = os.getcwd()

        if self._local:
            return self._download_on_local(
                files, target_dir=target_dir, extension=extension, recursive=recursive
            )

        else:  # remote session
            if recursive:
                warn(
                    "The 'recursive' parameter is ignored if the session is non-local."
                )
            return self._download_from_remote(
                files,
                target_dir=target_dir,
                extension=extension,
                chunk_size=chunk_size,
                progress_bar=progress_bar,
            )

    def _download_on_local(  # numpydoc ignore=RT01
        self,
        files: Union[str, List[str], Tuple[str, ...]],
        target_dir: str,
        extension: Optional[str] = None,
        recursive: bool = False,
    ) -> List[str]:
        """Download files when we are on a local session."""
        if isinstance(files, str):
            if not os.path.isdir(self.directory / files):
                list_files = self._validate_files(
                    files, extension=extension, recursive=recursive
                )
            else:
                list_files = [files]

        elif isinstance(files, PurePath):
            list_files = [str(files)]

        elif isinstance(files, (list, tuple)):
            if not all([isinstance(each, str) for each in files]):
                raise ValueError(
                    "The parameter `'files'` can be a list or tuple, but it should only contain strings."
                )
            list_files = []
            for each in files:
                list_files.extend(
                    self._validate_files(each, extension=extension, recursive=recursive)
                )

        else:
            raise ValueError(
                f"The `file` parameter type ({type(files)}) is not supported. "
                "Only strings, tuple of strings or list of strings are allowed."
            )

        return_list_files: list[str] = []
        for file in list_files:
            # file is a complete path
            basename = os.path.basename(file)
            destination = os.path.join(target_dir, basename)
            if os.path.isfile(destination):
                os.remove(destination)
                # the file might have been already downloaded.
                warn(
                    f"The file {file} has been updated in the current working directory."
                )

            if os.path.isdir(self.directory / file):
                if recursive:  # only copy the directory if recursive is true.
                    shutil.copytree(
                        self.directory / file,
                        target_dir,
                        dirs_exist_ok=True,
                    )
                    return_list_files.extend(
                        glob.iglob(target_dir + "/**/*", recursive=recursive)
                    )

            else:
                return_list_files.append(destination)
                shutil.copy(
                    self.directory / file,
                    destination,
                )

        return return_list_files

    def _download_from_remote(  # numpydoc ignore=RT01
        self,
        files: Union[str, List[str], Tuple[str, ...]],
        target_dir: str,
        extension: Optional[str] = None,
        chunk_size: Optional[int] = None,
        progress_bar: Optional[bool] = None,
    ) -> List[str]:
        """Download files when we are connected to a remote session."""

        if isinstance(files, str):
            list_files = self._validate_files(files, extension=extension)

        elif isinstance(files, list):
            if not all([isinstance(each, str) for each in files]):
                raise ValueError(
                    "The parameter `'files'` can be a list or tuple, but it should only contain strings."
                )
            list_files = []
            for each in files:
                list_files.extend(self._validate_files(each, extension=extension))

        else:
            raise ValueError(
                f"The `file` parameter type ({type(files)}) is not supported. "
                "Only strings, tuple of strings or list of strings are allowed."
            )

        for each_file in list_files:
            safe_relative_file = self._validate_remote_relative_path(each_file)
            out_file_name = os.path.join(target_dir, safe_relative_file)
            # 'each_file' might include subdirectories (relative to the
            # MAPDL working directory), which might not exist yet locally.
            os.makedirs(os.path.dirname(out_file_name) or ".", exist_ok=True)
            self._download(
                safe_relative_file,
                out_file_name=out_file_name,
                chunk_size=chunk_size,
                progress_bar=progress_bar,
            )

        return list_files

    @staticmethod
    def _validate_remote_relative_path(path: str) -> str:
        """Validate a relative remote file path to keep downloads in target_dir."""
        normalized_path = os.path.normpath(path.replace("\\", "/"))
        normalized = PurePosixPath(normalized_path)

        if normalized.is_absolute():
            raise ValueError(
                f"Path '{path}' is invalid. Absolute paths are not allowed for remote downloads."
            )

        if ".." in normalized.parts:
            raise ValueError(
                f"Path '{path}' is invalid. Parent directory references are not allowed."
            )

        if normalized.parts and re.match(r"^[a-zA-Z]:$", normalized.parts[0]):
            raise ValueError(
                f"Path '{path}' is invalid. Drive-letter paths are not allowed for remote downloads."
            )

        if str(normalized) in [".", ""]:
            raise ValueError(f"Path '{path}' is invalid.")

        return str(normalized)

    def _validate_files(
        self, file: str, extension: Optional[str] = None, recursive: bool = True
    ) -> List[str]:
        if extension is not None:
            if not isinstance(extension, str):
                raise TypeError(f"The extension {extension} must be a string.")

            if not extension.startswith("."):
                extension = "." + extension

        else:
            extension = ""

        # A glob pattern (with '*', '?' or '[') requires listing the
        # directory content to filter against.
        is_glob = bool(re.search(r"[*?\[]", file))
        # A path with a directory component (for example
        # ``tmp_dir/file.rst``) points inside a subdirectory of the working
        # directory.
        has_subdir = bool(os.path.dirname(file))

        if self.is_local:
            # filtering with glob (accepting *)
            if not os.path.isabs(file):
                # Relative paths (including ones with subdirectories) are
                # resolved against the MAPDL working directory.
                file = str(self.directory / file)
            list_files = glob.glob(file + extension, recursive=recursive)

        elif is_glob or not has_subdir:
            # Either a glob pattern, or a plain filename in the top level of
            # the working directory: both can be validated against
            # ``list_files``.
            base_name = os.path.basename(file + extension)
            self_files = self.list_files()

            list_files = fnmatch.filter(self_files, base_name)

        else:
            # Literal file path inside a subdirectory of the working
            # directory. ``list_files`` only returns the top level of the
            # working directory, so it cannot be used to validate files in
            # subdirectories.
            file_to_check = self._validate_remote_relative_path(file + extension)
            list_files = (
                [file_to_check] if self.inquire("", "EXIST", file_to_check) else []
            )

        # filtering by extension
        list_files = [file for file in list_files if file.endswith(extension)]

        if len(list_files) == 0:
            raise FileNotFoundError(
                f"No file matching '{file}' in the MAPDL session can be found."
            )

        return list_files

    @protect_grpc
    def _download(
        self,
        target_name: str,
        out_file_name: Optional[str] = None,
        chunk_size: int = DEFAULT_CHUNKSIZE,
        progress_bar: bool = False,
    ) -> None:
        """Download a file from the gRPC instance.

        Parameters
        ----------
        target_name : str
            Target file on the server. File must be in the same
            directory as the mapdl instance. List current files with
            ``mapdl.list_files()``

        out_file_name : str, optional
            Save the filename as a different name other than the
            ``target_name``.

        chunk_size : int, optional
            Chunk size in bytes.  Must be less than 4MB.  The default is 256 kB.

        progress_bar : bool, optional
            Display a progress bar using ``tqdm`` when ``True``.
            Helpful for showing download progress. The default is
            ``False`` to avoid excessive command printout.

        Examples
        --------
        Download the remote result file "file.rst" as "my_result.rst"

        >>> mapdl.download('file.rst', 'my_result.rst')
        """

        if progress_bar and _HAS_TQDM:
            progress_bar = True

        if out_file_name is None:
            out_file_name = target_name

        request = pb_types.DownloadFileRequest(name=target_name)
        metadata = [
            ("time_step_stream", "200"),
            ("chunk_size", str(chunk_size)),
        ]
        chunks = self._connected_stub.DownloadFile(request, metadata=metadata)
        file_size = save_chunks_to_file(
            chunks,
            out_file_name,
            progress_bar=progress_bar,
            target_name=target_name,
        )

        if not file_size:
            if target_name not in self.list_files():
                warn(f'File "{target_name}" does not exist.')
            else:
                warn(f'File "{target_name}" is empty.')

    @protect_grpc
    def upload(self, file_name: str, progress_bar: bool = _HAS_TQDM) -> str:
        """Upload a file to the grpc instance

        file_name : str
            Local file to upload.

        progress_bar : bool, optional
            Whether to display a progress bar using ``tqdm``. The default is ``True``.
            This parameter is helpful for showing download progress.

        Returns
        -------
        str
            Base name of the file uploaded.  File can be accessed
            relative to the mapdl instance with this file name.

        Examples
        --------
        Upload "local_file.inp" while disabling the progress bar

        >>> mapdl.upload('local_file.inp', progress_bar=False)
        """
        if not os.path.isfile(file_name):
            raise FileNotFoundError(f"Unable to locate filename {file_name}")
        self._log.debug(f"Uploading file '{file_name}' to the MAPDL instance.")

        chunks_generator = get_file_chunks(file_name, progress_bar=progress_bar)
        response = self._connected_stub.UploadFile(chunks_generator)

        if not response.length:
            raise IOError("File failed to upload")
        return os.path.basename(file_name)

    @protect_grpc
    def _download_as_raw(self, target_name: str) -> str:  # numpydoc ignore=RT01
        """Download a file from the gRPC instance as a binary
        string without saving it to disk.
        """
        request = pb_types.DownloadFileRequest(name=target_name)
        chunks = self._connected_stub.DownloadFile(request)
        return b"".join([chunk.payload for chunk in chunks])

    @protect_grpc
    def _upload_raw(self, raw, save_as):  # consider private
        """Upload a binary string as a file"""
        chunks = chunk_raw(raw, save_as)
        response = self._connected_stub.UploadFile(chunks)
        if response.length != len(raw):
            raise IOError("Raw Bytes failed to upload")

    def _screenshot_path(self):  # numpydoc ignore=RT01
        """Returns the local path of the MAPDL generated screenshot.

        If necessary, downloads the remotely rendered file.
        """
        if self._local:
            return super()._screenshot_path()

        jobname = self.jobname
        filenames = [
            filename
            for filename in self.list_files()
            if filename.endswith(".png") and filename.startswith(jobname)
        ]
        filenames.sort()
        filename = os.path.basename(filenames[-1])

        temp_dir = tempfile.gettempdir()
        save_name = os.path.join(temp_dir, "tmp.png")
        self._download(filename, out_file_name=save_name)
        return save_name

    def list_error_file(self) -> str | None:
        """Listing of errors written in JOBNAME.err

        Returns
        -------
        str
            Contents of the error file or None if not found.
        """
        files = self.list_files()
        jobname = self.jobname
        error_file = None
        for test_file in [f"{jobname}.err", f"{jobname}0.err"]:
            if test_file in files:
                error_file = test_file
                break

        if not error_file:
            return None

        if self._local:
            return open(self.directory / error_file).read()
        elif self._exited:
            raise MapdlExitedError(
                "Cannot list error file when MAPDL Service has exited"
            )

        return self._download_as_raw(error_file).decode("latin-1")

    @supress_logging
    @run_as("PREP7")
    def _generate_iges(self):
        """Save IGES geometry representation to disk.

        Returns
        -------
        str
            The filename of the saved IGES representation.
        """
        basename = "_tmp.iges"
        if self._local:
            filename = self.directory / basename
            self.igesout(basename, att=1)
        else:
            self.igesout(basename, att=1)
            filename = os.path.join(tempfile.gettempdir(), basename)
            self._download(basename, filename, progress_bar=False)
        return filename

    @property
    def _distributed_result_file(self):  # numpydoc ignore=RT01
        """Path of the distributed result file."""
        if not self._distributed:
            return

        try:
            filename = self.inquire("", "RSTFILE")
            if not filename:
                filename = self.jobname
        except:
            filename = self.jobname

        # ansys decided that a jobname ended in a number needs a bonus "_"
        if filename[-1].isnumeric():
            filename += "_"

        rth_basename = "%s0.%s" % (filename, "rth")
        rst_basename = "%s0.%s" % (filename, "rst")

        rth_file = self.directory / rth_basename
        rst_file = self.directory / rst_basename

        if self._prioritize_thermal:
            if not os.path.isfile(rth_file):
                raise FileNotFoundError("Thermal Result not available")
            return rth_file

        if os.path.isfile(rth_file) and os.path.isfile(rst_file):
            return last_created([rth_file, rst_file])
        elif os.path.isfile(rth_file):
            return rth_file
        elif os.path.isfile(rst_file):
            return rst_file
