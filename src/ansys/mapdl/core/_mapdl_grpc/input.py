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

"""Input-file streaming and the commands that run through it."""

from functools import wraps
import os
import tempfile

from ansys.api.mapdl.v0 import mapdl_pb2 as pb_types

from ansys.mapdl.core.constants import DEFAULT_CHUNKSIZE
from ansys.mapdl.core.errors import protect_grpc
from ansys.mapdl.core.mapdl import MapdlBase
from ansys.mapdl.core.misc import random_string

from . import _GrpcMixinBase


class _GrpcInputMixin(_GrpcMixinBase):
    """Input-file streaming and the commands that run through it."""

    def input(
        self,
        fname="",
        ext="",
        dir_="",
        line="",
        log="",
        *,
        verbose=False,
        progress_bar=False,
        time_step_stream=None,
        chunk_size=512,
        orig_cmd="/INP",
        write_to_log=True,
        **kwargs,
    ):
        """Stream a local input file to a remote mapdl instance.
        Stream the response back and deserialize the output.

        .. versionchanged:: 0.65
            From version 0.65 you can use the APDL commands arguments (``ext``, ``dir``, ``line``)
            in within this command.
            However, the gRPC implementation does *not* uses the APDL ``/INPUT`` command,
            rather the gRPC input method with the appropriate configuration to replicate
            ``/INPUT`` behaviour.

        Parameters
        ----------
        fname : str, optional
            MAPDL input file to stream to the MAPDL gRPC server.
            File name and directory path.
            An unspecified directory path defaults to the Python working
            directory; in this case, you can use all 248 characters for the file name.
            The file name defaults to the current ``Jobname`` if ``Ext`` is specified.

        ext : str, optional
            Filename extension (eight-character maximum).

        dir_ : str, optional
            Directory path. The default is the current working directory.

        line : int, optional
            A value indicating either a line number in the file from which to
            begin reading the input file. The first line is the zero line (Python
            convention).

            (blank), or 0
                Begins reading from the top of the file. Default.

            LINE_NUMBER
                Begins reading from the specified line number in the file.

        log : optional
            Not supported in the gRPC implementation.

        time_step_stream : int, optional
            Time to wait between streaming updates to send back chunks
            from the listener file.  Larger values mean more data per
            chunk and less chunks, but if the command is short, will
            wait until time_step_stream is finished leading to a long
            execution time.

            Due to stability issues, the default time_step_stream is
            dependent on the OS MAPDL is running on.  The defaults are:

            - Windows: ``time_step_stream=500``
            - Linux: ``time_step_stream=100``

            These defaults will be ignored if ``time_step_stream`` is
            manually set. See the *Examples* section to learn how to change
            the default value globally.

        orig_cmd : str, optional
            Original command. There are some cases, were input is
            used to send the file to the grpc server but then we want
            to run something different than ``/INPUT``, for example
            ``CDREAD``.

        Returns
        -------
        str
            Response from MAPDL.

        Notes
        -----
        This method does not use the APDL ``/INPUT`` command.
        However its usage is very similar to it. See *Examples* section.

        If you want to use ``/INPUT`` for some reason, although it is not
        recommended, you can write the desired input file, upload it using
        :func:`Mapdl.upload <ansys.mapdl.core.Mapdl.upload>`, and then use
        run command :func:`Mapdl.run('/INPUT,<FILE>,<EXT>) <ansys.mapdl.core.Mapdl.run>`.
        This does not avoid to use the gRPC input method, but it allows you to
        use the APDL ``/INPUT`` command from the generated input file.
        See *Examples* section for more information.

        Examples
        --------
        Load a simple ``"ds.dat"`` input file generated from Ansys
        Workbench.

        >>> output = mapdl.input('ds.dat')

        Load that same file while streaming the output in real-time.

        >>> output = mapdl.input('ds.dat', verbose=True)

        Use the default APDL ``/INPUT`` command:

        >>> with open('myinput.inp','w').write("/finish\\n/prep7\\n/com, my commands")
        >>> with open('inputtrigger.inp','w').write("/input,myinput,inp")
        >>> mapdl.upload("myinput.inp")
        Uploading myinput.inp: 100%|█████████████████████████████████████████████████| 26.0/26.0 [00:00<00:00, 5.86kB/s]
        'myinput.inp'
        >>> mapdl.upload("inputtrigger.inp")
        Uploading inputtrigger.inp: 100%|████████████████████████████████████████████| 32.0/32.0 [00:00<00:00, 8.92kB/s]
        'inputtrigger.inp'
        >>> with mapdl.non_interactive:
                mapdl.run("/input,inputtrigger,inp") # This inputs 'myinput.inp'

        You can also change them globably using:

        >>> from ansys.mapdl.core import mapdl_grpc
        >>> mapdl_grpc.DEFAULT_TIME_STEP_STREAM=100 # in milliseconds
        """
        self._check_blocked_commands(orig_cmd)
        return self._stream_input(
            fname,
            ext,
            dir_,
            line,
            log,
            verbose=verbose,
            progress_bar=progress_bar,
            time_step_stream=time_step_stream,
            chunk_size=chunk_size,
            orig_cmd=orig_cmd,
            write_to_log=write_to_log,
            **kwargs,
        )

    @protect_grpc
    def _stream_input(
        self,
        fname="",
        ext="",
        dir_="",
        line="",
        log="",
        *,
        verbose=False,
        progress_bar=False,
        time_step_stream=None,
        chunk_size=512,
        orig_cmd="/INP",
        write_to_log=True,
        **kwargs,
    ):
        # Checking compatibility
        # Checking the user is not reusing old api:
        #
        # fname,
        # verbose=False,
        # progress_bar=False,
        # time_step_stream=None,
        # chunk_size=512,
        # orig_cmd="/INP",
        # write_to_log=True,

        msg_compat = "\nThe 'mapdl.input' method API changed in v0.65. Please check the documentation for information about the new arguments."

        if log:
            raise ValueError(
                "'log' argument is not supported in the gRPC implementation."
            )

        if not isinstance(ext, (str)) and ext is not None:
            raise ValueError(
                "Only strings are allowed in 'ext' argument.\n" + msg_compat
            )

        if not isinstance(dir_, (str)) and dir_ is not None:
            raise ValueError(
                "Only strings are allowed in 'dir_' argument.\n" + msg_compat
            )

        # Getting arguments rights
        if not fname and ext:
            fname = self.jobname

        if not fname:
            raise ValueError("A file name must be supplied.")

        fname = self._get_file_name(fname=fname, ext=ext)

        if not dir_:
            self._log.debug(f"Using python working directory as 'dir_' value.")
            dir_ = os.getcwd()
        else:
            fname = os.path.join(dir_, fname)

        if not line:
            line = 0
        else:
            try:
                line = int(line)
            except ValueError:
                raise ValueError(
                    "Only integers are supported for 'line' argument. Labels are not supported on the gRPC implementation."
                )

        if line != 0:
            # Trimming file
            tmp_modified_file = os.path.join(
                tempfile.gettempdir(), os.path.basename(fname)
            )
            with open(tmp_modified_file, "w") as fid, open(fname, "r") as fid2:
                fid.writelines(fid2.readlines()[line:])

            fname = tmp_modified_file

        # Running method
        #
        is_cdread = "CDRE" in orig_cmd.upper()
        cd_read_option = kwargs.get("cd_read_option", "COMB").upper()
        is_cdread_all = is_cdread and cd_read_option == "ALL"

        if is_cdread:
            # CDREAD already uploads the file, and since the priority in
            # `_get_file_path` is for the files in the python working directory,
            # we skip that function here.
            self._log.debug(
                f"Avoid uploading the file {fname} because `CDREAD` should have upload it already."
            )
            filename = fname

        else:
            # Always check if file is present as the grpc and MAPDL errors
            # are unclear
            filename = self._get_file_path(fname, progress_bar)

        time_step_stream = self._get_time_step_stream(time_step_stream)

        metadata = [
            ("time_step_stream", str(time_step_stream)),
            ("chunk_size", str(chunk_size)),
        ]

        if verbose and not is_cdread_all:
            # For 'DB'/'SOLID'/'COMB', the archive itself is a valid sequence
            # of APDL commands, so it can be streamed and run directly.
            # 'ALL' cannot take this shortcut: it first needs the IGES
            # archive imported through '/AUX15' before the CDB file is read,
            # so it always goes through the multi-command driver file below.
            request = pb_types.InputFileRequest(filename=filename)
            strouts = self._stub.InputFileS(request, metadata=metadata)
            responses = []
            for strout in strouts:
                lines = strout.cmdout
                # print out input as it is being run
                print("\n".join(lines))
                responses.extend(lines)
            response = "\n".join(responses)
            return response.strip()

        ##
        # Otherwise, not verbose (or 'CDREAD,ALL', which always needs the
        # multi-command driver file below, even when 'verbose' is requested)

        # since we can't directly run /INPUT, we have to write a
        # temporary input file that tells MAPDL to read the input
        # file.
        id_ = random_string()
        tmp_name = f"_input_tmp_{id_}_.inp"
        tmp_out = f"_input_tmp_{id_}_.out"

        if is_cdread_all:
            # 'CDREAD,ALL' restores two archives: the solid-model geometry
            # and loads (IGES format) and the rest of the database (CDB
            # format).  MAPDL itself performs this as a sequence of
            # commands, so we replicate it explicitly here instead of
            # relying on 'CDREAD' to locate the second file, since the gRPC
            # implementation is the one responsible for uploading and
            # locating both archives:
            #   /AUX15            (enter the IGES file-transfer processor)
            #   IGESIN            (import the solid-model/loads archive)
            #   FINISH            (leave /AUX15)
            #   /INPUT            (read the CDB database archive)
            #   /PREP7            (CDREAD leaves the user in /PREP7)
            fnamei = kwargs.get("fnamei")
            if not fnamei:
                raise ValueError(
                    "The 'fnamei' argument (the IGES archive) must be "
                    "supplied when using 'CDREAD' with the 'ALL' option."
                )
            tmp_dat = (
                f"/OUT,{tmp_out}\n"
                "/AUX15\n"
                f"IGESIN,'{fnamei}'\n"
                "FINISH\n"
                f"/INPUT,'{filename}'\n"
                "/PREP7\n"
                "/RMTMP\n"
                "/OUT,"
            )
            delete_uploaded_files = False

        elif is_cdread:
            # Using CDREAD
            tmp_dat = (
                f"/OUT,{tmp_out}\n{orig_cmd},'{cd_read_option}','{filename}'\n/OUT,"
            )
            delete_uploaded_files = False

        else:
            # Using default INPUT
            tmp_dat = f"/OUT,{tmp_out}\n{orig_cmd},'{filename}'\n/OUT,"
            delete_uploaded_files = True

        if write_to_log and self._apdl_log is not None:
            if not self._apdl_log.closed:
                self._apdl_log.write(tmp_dat)

        # Escaping early if inside non_interactive context. The commands are
        # executed when the context exits, so there is no need to write or
        # upload a temporary input file.
        if self._store_commands:
            # Excludes the leading and trailing '/OUT' redirection lines,
            # keeping every command in between (a single one for 'DB',
            # 'SOLID', 'COMB', and plain '/INPUT'; several for 'ALL').
            self._stored_commands.extend(tmp_dat.splitlines()[1:-1])
            return None

        if self._local:
            local_path = self.directory
            tmp_name_path = os.path.join(local_path, tmp_name)
            with open(tmp_name_path, "w") as f:
                f.write(tmp_dat)
        else:
            self._upload_raw(tmp_dat.encode(), tmp_name)

        request = pb_types.InputFileRequest(filename=tmp_name, opt="MUTE")

        # even though we don't care about the output, we still
        # need to check.  otherwise, since inputfile is
        # non-blocking, we could corrupt the service
        chunks = self._stub.InputFileS(request, metadata=metadata)
        _ = [chunk.cmdout for chunk in chunks]  # unstable

        # all output (unless redirected) has been written to a temp output
        if self._local:
            tmp_out_path = os.path.join(local_path, tmp_out)
            with open(tmp_out_path) as f:
                output = f.read()

            # delete the files to avoid overwriting:
            try:
                os.remove(tmp_name_path)
            except OSError:
                pass

            try:
                os.remove(tmp_out_path)
            except OSError:
                pass

        # otherwise, read remote file
        else:
            output = self._download_as_raw(tmp_out).decode("latin-1")

            # Deleting the previous files
            self.slashdelete(tmp_name)
            self.slashdelete(tmp_out)
            if filename in self.list_files() and delete_uploaded_files:
                self.slashdelete(filename)

        if verbose:
            # 'CDREAD,ALL' redirects its output to a file (see 'tmp_dat'
            # above) instead of streaming it, so it cannot be printed line by
            # line as it runs. Print it once fully captured instead.
            print(output)

        return output

    @wraps(MapdlBase.cdread)
    def cdread(
        self, option="", fname="", ext="", fnamei="", exti="", **kwargs
    ):  # numpydoc ignore=RT01
        """Wraps CDREAD"""
        option = option.strip().upper()

        if option not in ["ALL", "DB", "SOLID", "COMB"]:
            raise ValueError(
                f'Option "{option}" is not supported.  Please '
                "Input the geometry and mesh files separately "
                r'with "\INPUT" or ``mapdl.input``'
            )

        kwargs.setdefault("verbose", False)
        kwargs.setdefault("progress_bar", False)
        kwargs.setdefault("orig_cmd", "CDREAD")
        kwargs.setdefault("cd_read_option", option)

        cdb_fname = self._get_file_name(fname, ext, "cdb")
        cdb_fname = self._get_file_path(cdb_fname, kwargs["progress_bar"])

        if option == "ALL":
            # 'ALL' reads two archives: the command/database file resolved
            # above (``cdb_fname``), and a solid-model/IGES archive.  Per
            # CDREAD documented defaults, 'fnamei' defaults to the *original*
            # 'fname' argument (not the already-suffixed 'cdb_fname'), and
            # 'exti' defaults to 'iges' when omitted.
            iges_fname = self._get_file_name(fnamei or fname, exti, "iges")
            iges_fname = self._get_file_path(iges_fname, kwargs["progress_bar"])
            kwargs["fnamei"] = iges_fname

        return self.input(cdb_fname, **kwargs)

    @wraps(MapdlBase.tbft)
    def tbft(  # numpydoc ignore=RT01
        self,
        oper="",
        id_="",
        option1="",
        option2="",
        option3="",
        option4="",
        option5="",
        option6="",
        option7="",
        **kwargs,
    ):
        """Wraps ``MapdlBase.tbft``."""
        extra_info = ""
        if oper.lower() == "eadd":
            # Option 2 is a file and option 4 is the directory.
            # Option 3 is be extension
            option3 = option3.replace(".", "")
            fname = option2 if not option3 else option2 + "." + option3
            filename = os.path.join(option4, fname)

            fname = self._get_file_name(fname=option2, ext=option3)
            if option4:  # if directory is supplied
                fname = os.path.join(option4, fname)

            filename = self._get_file_path(fname, progress_bar=False)

            # since we upload the file, we dont need the full path: not in option2 nor option4.
            if not self._local:
                extra_info = f"PyMAPDL has upload the file {option2} to the MAPDL instance, hence the options for 'TBFT' command have changed."
                option2 = filename
                option3 = ""  # the extension is now included in filename
                option4 = ""

        if extra_info:
            self.com("")
            self._log.debug(extra_info)

        return super().tbft(
            oper,
            id_,
            option1,
            option2,
            option3,
            option4,
            option5,
            option6,
            option7,
            **kwargs,
        )

    @wraps(MapdlBase.cmatrix)
    def cmatrix(  # numpydoc ignore=RT01
        self,
        symfac="",
        condname="",
        numcond="",
        grndkey="",
        capname="",
        **kwargs,
    ):
        """Run CMATRIX in non-interactive mode and return the response from file."""

        # The CMATRIX command needs to run in non-interactive mode
        if not self._store_commands:
            with self.non_interactive:
                super().cmatrix(symfac, condname, numcond, grndkey, capname, **kwargs)
            self._response = self._download_as_raw("cmatrix.out").decode()
            return self._response

        # otherwise, simply run cmatrix as we're already in
        # non-interactive and there's no output to return
        super().cmatrix(symfac, condname, numcond, grndkey, capname, **kwargs)

    def _flush_stored(self):
        """Writes stored commands to an input file and runs the input
        file.  Used with non_interactive.
        """
        if not self._stored_commands:
            self._log.debug("There is no commands to be flushed.")
            self._store_commands = False
            return

        self._log.debug("Flushing stored commands")

        commands = "\n".join(self._stored_commands)
        if self._apdl_log:
            self._apdl_log.write(commands + "\n")

        self._log.debug(
            "Writing the following commands to a temporary apdl input file:\n%s",
            commands,
        )

        # write to a temporary input file
        def build_rand_tmp():
            return os.path.join(tempfile.gettempdir(), f"tmp_{random_string()}.inp")

        # rare case of duplicated tmpfile (birthday problem)
        tmp_filename = build_rand_tmp()
        while os.path.isfile(tmp_filename):
            tmp_filename = build_rand_tmp()

        with open(tmp_filename, "w") as fid:
            fid.writelines(commands)

        self._store_commands = False
        self._stored_commands = []

        # run the stored commands
        # already checked by run() and input_strings() when stored
        out = self._stream_input(
            tmp_filename,
            write_to_log=False,
            verbose=False,
            chunk_size=DEFAULT_CHUNKSIZE,
            progress_bar=False,
        )
        # skip the first line as it simply states that it's reading an input file
        self._response = out[out.find("LINE=       0") + 13 :]
        response_ = "\n".join(self._response.splitlines()[:20])
        self._log.info(response_)

        if not self._ignore_errors:
            self._raise_errors(self._response)

        # try/except here because MAPDL might have not closed the temp file
        try:
            os.remove(tmp_filename)
        except:
            self._log.warning("Unable to remove temporary file %s", tmp_filename)
