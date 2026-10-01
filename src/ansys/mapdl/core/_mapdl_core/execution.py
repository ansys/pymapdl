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


"""The execution MAPDL core responsibility mixin."""

from functools import wraps
import os
import re

# Subprocess is needed to start the backend. But
# the input is controlled by the library. Excluding bandit check.
import sys
import tempfile
import time
from typing import TYPE_CHECKING, Optional
from warnings import warn

from ansys.mapdl.core import LOG as logger
from ansys.mapdl.core import _HAS_DPF
from ansys.mapdl.core.commands import (
    CMD_BC_LISTING,
    CMD_LISTING,
    BoundaryConditionsListingOutput,
    CommandListingOutput,
    Commands,
    StringWithLiteralRepr,
    inject_docs,
)
from ansys.mapdl.core.errors import (
    ComponentNoData,
    MapdlCommandIgnoredError,
    MapdlExitedError,
    MapdlFileNotFoundError,
    MapdlInvalidRoutineError,
    MapdlRuntimeError,
)
from ansys.mapdl.core.mapdl_types import MapdlFloat
from ansys.mapdl.core.misc import random_string, supress_logging

if TYPE_CHECKING:  # pragma: no cover
    if _HAS_DPF:
        pass


from .constants import (
    _PERMITTED_ERRORS,
    DEBUG_LEVELS,
    INVAL_COMMANDS,
    INVAL_COMMANDS_SILENT,
    MAX_PARAM_CHARS,
    PLOT_COMMANDS,
)


def setup_logger(loglevel="INFO", log_file=True, mapdl_instance=None):
    """Setup logger."""
    if hasattr(setup_logger, "log"):
        return setup_logger.log
    setup_logger.log = logger.add_instance_logger("MAPDL", mapdl_instance)
    return setup_logger.log


def parse_to_short_cmd(command):
    """Takes any MAPDL command and returns the first 4 characters of
    the command

    Examples
    --------
    >>> parse_to_short_cmd('K,,1,0,0,')
    'K'

    >>> parse_to_short_cmd('VPLOT, ALL')
    'VPLO'
    """
    try:
        short_cmd = command.split(",")[0]
        return short_cmd[:4].upper()
    except Exception:  # pragma: no cover
        return


def _plot_commands():
    """Return plot commands while honoring the legacy facade patch target.

    ``PLOT_COMMANDS`` remains defined by :mod:`._mapdl_core.constants`, but
    older callers patch ``mapdl_core.PLOT_COMMANDS`` directly.  Resolve that
    compatibility alias at the point of use without importing the public
    facade during module initialization.
    """
    facade = sys.modules.get("ansys.mapdl.core.mapdl_core")
    if facade is not None:
        return getattr(facade, "PLOT_COMMANDS", PLOT_COMMANDS)
    return PLOT_COMMANDS


from . import _CoreMixinBase


class _CoreExecutionMixin(_CoreMixinBase):
    """Static responsibility mixin for the MAPDL core facade."""

    def _wrap_listing_functions(self):
        # Wrapping LISTING FUNCTIONS.
        def wrap_listing_function(func):
            # Injecting doc string modification
            if hasattr(func, "__func__"):
                func.__func__.__doc__ = inject_docs(func.__func__.__doc__)
            else:  # pragma: no cover
                func.__doc__ = inject_docs(func.__doc__)

            @wraps(func)
            def inner_wrapper(*args, **kwargs):
                return CommandListingOutput(func(*args, **kwargs))

            return inner_wrapper

        def wrap_bc_listing_function(func):
            # Injecting doc string modification
            if hasattr(func, "__func__"):
                func.__func__.__doc__ = inject_docs(func.__func__.__doc__)
            else:  # pragma: no cover
                func.__doc__ = inject_docs(func.__doc__)

            @wraps(func)
            def inner_wrapper(*args, **kwargs):
                return BoundaryConditionsListingOutput(func(*args, **kwargs))

            return inner_wrapper

        for name in dir(self):
            if name[0:4].upper() in CMD_LISTING and name in dir(
                Commands
            ):  # avoid matching Mapdl properties which starts with same letters as MAPDL commands.
                func = self.__getattribute__(name)
                setattr(self, name, wrap_listing_function(func))

            if name[0:4].upper() in CMD_BC_LISTING and name in dir(Commands):
                func = self.__getattribute__(name)
                setattr(self, name, wrap_bc_listing_function(func))

    @supress_logging
    def __str__(self):
        return self.info.__str__()

    def set_log_level(self, loglevel: DEBUG_LEVELS) -> None:
        """Sets log level

        Parameters
        ----------
        loglevel : str, int
            Log level.  Must be one of: ``'DEBUG', 'INFO', 'WARNING', 'ERROR'``.

        Examples
        --------
        Set the log level to debug

        >>> mapdl.set_log_level('DEBUG')

        Set the log level to info

        >>> mapdl.set_log_level('INFO')

        Set the log level to warning

        >>> mapdl.set_log_level('WARNING')

        Set the log level to error

        >>> mapdl.set_log_level('ERROR')
        """
        if isinstance(loglevel, str):
            loglevel = loglevel.upper()  # type: ignore[assignment]
        setup_logger(loglevel=loglevel)

    def _set_log_level(self, level):
        """Alias for set_log_level"""
        self.set_log_level(level)

    def _list(self, command):
        """Replaces *LIST command"""
        items = command.split(",")
        filename = self.directory / ".".join(items[1:])
        if os.path.isfile(filename):
            self._response = open(filename).read()
            response_ = "\n".join(self._response.splitlines()[:10])
            self._log.info(response_)
        else:
            raise Exception("Cannot run:\n{command}\n\nFile does not exist")

    def _get(self, *args, **kwargs) -> MapdlFloat:
        """Simply use the default get method"""
        return self.get(*args, **kwargs)

    def _flush_stored(self):
        """Writes stored commands to an input file and runs the input file.

        Used with ``non_interactive``.

        Overridden by gRPC.
        """
        if not self._stored_commands:
            self._log.debug("There is no commands to be flushed.")
            self._store_commands = False
            return

        self._log.debug("Flushing stored commands")

        rnd_str = random_string()
        tmp_out = os.path.join(tempfile.gettempdir(), f"tmp_{rnd_str}.out")
        self._stored_commands.insert(0, f"/OUTPUT, {tmp_out}")
        self._stored_commands.append("/OUTPUT")
        commands = "\n".join(self._stored_commands)
        if self._apdl_log:
            self._apdl_log.write(commands + "\n")

        self._store_commands = False
        self._stored_commands = []

        # write to a temporary input file
        self._log.debug(
            "Writing the following commands to a temporary " "apdl input file:\n%s",
            commands,
        )

        tmp_inp = os.path.join(tempfile.gettempdir(), f"tmp_{random_string()}.inp")
        with open(tmp_inp, "w") as f:
            f.writelines(commands)

        # interactive result
        _ = self.input(tmp_inp, write_to_log=False)

        time.sleep(0.1)  # allow MAPDL to close the file
        if os.path.isfile(tmp_out):
            self._response = "\n" + open(tmp_out).read()

        if self._response is None:  # pragma: no cover
            self._log.warning("Unable to read response from flushed commands")
        else:
            response_ = "\n".join(self._response.splitlines()[:10])
            self._log.debug(f"Printing truncated response: {response_}")

    def run_multiline(self, commands) -> str:
        """Run several commands as a single block

        .. deprecated:: 0.61.0
           This function is being deprecated. Please use `input_strings`
           instead.

        Allows to run multiple mapdl commands in different lines in one go.

        Parameters
        ----------
        commands : str
            Commands separated by new lines.  See example.

        Returns
        -------
        str
            Command output from MAPDL.  Includes the output from
            running every command, as if it was an input file.

        Examples
        --------
        Run several commands from Python multi-line string.

        >>> cmd = '''/prep7
        ! Mat
        MP,EX,1,200000
        MP,NUXY,1,0.3
        MP,DENS,1,7.85e-09
        ! Elements
        et,1,186
        et,2,154
        ! Geometry
        BLC4,0,0,1000,100,10
        ! Mesh
        esize,5
        vmesh,all
        nsel,s,loc,x,0
        d,all,all
        nsel,s,loc,x,999,1001
        type,2
        esurf
        esel,s,type,,2
        nsle
        sfe,all,3,pres,,-10
        allsel
        /solu
        antype,0
        solve
        /post1
        set,last
        plnsol,u,sum
        '''
        >>> resp = mapdl.run_multiline(cmd)
        >>> resp
        MATERIAL          1     EX   =   200000.0
        MATERIAL          1     NUXY =  0.3000000
        MATERIAL          1     DENS =  0.7850000E-08
        ELEMENT TYPE          1 IS SOLID186     3-D 20-NODE STRUCTURAL SOLID
         KEYOPT( 1- 6)=        0      0      0        0      0      0
         KEYOPT( 7-12)=        0      0      0        0      0      0
         KEYOPT(13-18)=        0      0      0        0      0      0
        output continues...
        """

        warn(
            "'run_multiline()' is being deprecated in future versions.\n Please use 'input_strings'.",
            DeprecationWarning,
        )
        return self.input_strings(commands=commands)

    def input_strings(self, commands) -> str:
        """
        Run several commands as a single block.

        These commands are all in a single string or in list of strings.

        Parameters
        ----------
        commands : str or list of str
            Commands separated by new lines, or a list of commands strings.
            See example.

        Returns
        -------
        str
            Command output from MAPDL.  Includes the output from
            running every command, as if it was an input file.

        Examples
        --------
        Run several commands from Python multi-line string.

        >>> cmd = '''/prep7
        ! Mat
        MP,EX,1,200000
        MP,NUXY,1,0.3
        MP,DENS,1,7.85e-09
        ! Elements
        et,1,186
        et,2,154
        ! Geometry
        BLC4,0,0,1000,100,10
        ! Mesh
        esize,5
        vmesh,all
        '''
        >>> resp = mapdl.input_strings(cmd)
        >>> resp
        MATERIAL          1     EX   =   200000.0
        MATERIAL          1     NUXY =  0.3000000
        MATERIAL          1     DENS =  0.7850000E-08
        ELEMENT TYPE          1 IS SOLID186     3-D 20-NODE STRUCTURAL SOLID
         KEYOPT( 1- 6)=        0      0      0        0      0      0
         KEYOPT( 7-12)=        0      0      0        0      0      0
         KEYOPT(13-18)=        0      0      0        0      0      0
        """
        if isinstance(commands, str):
            commands = commands.splitlines()

        self._stored_commands.extend(commands)
        if self._store_commands:
            return None
        else:
            self._flush_stored()
            return self._response

    def run(
        self,
        command: str,
        write_to_log: bool = True,
        mute: Optional[bool] = None,
        **kwargs,
    ) -> str:
        """
        Run single APDL command.

        For multiple commands, use :func:`Mapdl.input_strings()
        <ansys.mapdl.core.Mapdl.input_strings>`.

        Parameters
        ----------
        command : str
            ANSYS APDL command.

        write_to_log : bool, optional
            Overrides APDL log writing.  Default ``True``.  When set
            to ``False``, will not write command to log, even if APDL
            command logging is enabled.

        kwargs : dict, optional
            These keyword arguments are interface specific or for
            development purposes.

            avoid_non_interactive : :class:`bool`
              *(Development use only)*
              Avoids the non-interactive mode for this specific command.
              Defaults to ``False``.

            verbose : :class:`bool`
              Prints the command to the screen before running it.
              Defaults to ``False``.

        Returns
        -------
        str
            Command output from MAPDL.

        Notes
        -----

        **Running non-interactive commands**

        When two or more commands need to be run non-interactively
        (i.e. ``*VWRITE``) use

        >>> with mapdl.non_interactive:
        ...     mapdl.run("*VWRITE,LABEL(1),VALUE(1,1),VALUE(1,2),VALUE(1,3)")
        ...     mapdl.run("(1X,A8,'   ',F10.1,'  ',F10.1,'   ',1F5.3)")

        Alternatively, you can simply run a block of commands with:

        >>> mapdl.input_strings(cmd)

        Examples
        --------
        >>> mapdl.run('/PREP7')

        Equivalent Pythonic method:

        >>> mapdl.prep7()
        """
        if self.exited:
            raise MapdlExitedError(
                f"The MAPDL instance has been exited before running the command: {command}"
            )

        # check if multiline
        if "\n" in command or "\r" in command:
            raise ValueError("Use ``input_strings`` for multi-line commands")

        if len(command) > 639:  # CMD_MAX_LENGTH
            # If using mapdl_grpc, this check is redundant on purpose.
            # Console probably do not have this limitation, but I'm not certain.
            raise ValueError("Maximum command length must be less than 640 characters")

        # Check kwargs
        verbose = kwargs.pop("verbose", False)
        savefig = kwargs.pop("savefig", False)

        # Check if you want to avoid the current non-interactive context.
        avoid_non_interactive = kwargs.pop("avoid_non_interactive", False)

        # Check if there is an unused keyword argument. If there is, it
        # might be because you wrote a wrong argument name.
        #
        # Remove empty string kwargs
        for key, value in list(kwargs.items()):
            if value == "":
                kwargs.pop(key)

        if kwargs:
            warn(
                "The following keyword arguments are not used:\n"
                f"{', '.join(kwargs.keys())}\n"
                "Make sure you are using the intended keyword arguments.",
                UserWarning,
            )

        # Early exit if on non-interactive.
        if self._store_commands and not avoid_non_interactive:
            # If you are using NBLOCK on input, you should not strip the string
            self._stored_commands.append(command)
            return

        if mute is None:
            if hasattr(self, "mute"):
                mute = self.mute
            else:  # if not gRPC
                mute = False

        command = command.strip()

        is_comment = command.startswith("!") or command.upper().startswith("/COM")

        # always reset the cache
        self._reset_cache()

        # address MAPDL /INPUT level issue
        if command[:4].upper() == "/CLE":
            # Address gRPC issue
            # https://github.com/ansys/pymapdl/issues/380
            command = "/CLE,NOSTART"

        # Tracking output device
        if command[:4].upper() == "/SHO" and "," in command:
            self._file_type_for_plots = command.split(",")[1].upper()  # type: ignore[assignment]

        # Invalid commands silently ignored.
        cmd_ = command.split(",")[0].upper()
        if cmd_ in INVAL_COMMANDS_SILENT:
            msg = f"{cmd_} is ignored: {INVAL_COMMANDS_SILENT[cmd_]}."
            self._log.info(msg)

            # This, very likely, won't be recorded anywhere.
            # But just in case, I'm adding info as /com
            command = (
                f"/com, PyMAPDL: {msg}"  # Using '!' makes the output of '_run' empty
            )

        if command[:3].upper() in INVAL_COMMANDS:
            exception = MapdlRuntimeError(
                'Invalid PyMAPDL command "%s"\n\n%s'
                % (command, INVAL_COMMANDS[command[:3].upper()])
            )
            raise exception
        elif command[:4].upper() in INVAL_COMMANDS:
            exception = MapdlRuntimeError(
                'Invalid PyMAPDL command "%s"\n\n%s'
                % (command, INVAL_COMMANDS[command[:4].upper()])
            )
            raise exception
        elif write_to_log and self._apdl_log is not None:
            if not self._apdl_log.closed:
                self._apdl_log.write("%s\n" % command)

        if command[:4].upper() == "/LIS":
            # simply return the contents of the file
            return self.list(*command.split(",")[1:])

        if "=" in command and not is_comment:
            # We are storing a parameter.
            param_name = command.split("=")[0].strip()

            if cmd_[:4].upper() not in ["/COM", "/TIT", "/SYS"]:
                # Edge case. `\title, 'par=1234' `
                self._check_parameter_name(param_name)

        self._before_run(command)

        short_cmd = parse_to_short_cmd(command)
        self._log.debug(f"Running (verbose: {verbose}, mute={mute}): '{command}'")
        text = self._run(command, verbose=verbose, mute=mute)

        self._after_run(command)

        if mute:
            return

        text = text.replace("\\r\\n", "\n").replace("\\n", "\n")
        if text:
            self._response = StringWithLiteralRepr(text.strip())
            if self._response is None:
                raise MapdlRuntimeError("MAPDL did not return any response.")
            response_ = "\n".join(self._response.splitlines()[:20])
            self._log.info(response_)
        else:
            self._response = None
            return self._response

        if not self.ignore_errors:
            self._raise_errors(text)

        # special returns for certain geometry commands
        if short_cmd in _plot_commands():
            self._log.debug("It is a plot command.")
            return self.screenshot(savefig=savefig, default_name="plot")

        return self._response

    def _run(self, *args, **kwargs):  # pragma: no cover
        raise NotImplementedError("Implemented by child class")

    def exit(self):  # pragma: no cover
        """Exit from MAPDL"""
        raise NotImplementedError("Implemented by child class")

    def _raise_errors(self, text):
        # to make sure the following error messages are caught even if a breakline is in between.
        flat_text = " ".join([each.strip() for each in text.splitlines()])
        base_error_msg = "\n\nIgnore these messages by setting 'ignore_errors'=True.\n"

        if "unable to open file" in flat_text or (
            "unable to open" in flat_text and "file" in flat_text
        ):
            text += base_error_msg
            raise MapdlFileNotFoundError(text)

        if "is not a recognized" in flat_text:
            text = text.replace("This command will be ignored.", "")
            text += base_error_msg
            raise MapdlInvalidRoutineError(text)

        if "command is ignored" in flat_text:
            text += base_error_msg
            raise MapdlCommandIgnoredError(text)

        if (
            "The component definition of" in flat_text
            and "contains no data." in flat_text
        ):
            text += base_error_msg
            raise ComponentNoData(text)

        if "is not part of the currently active set." in flat_text:
            text += base_error_msg
            raise MapdlCommandIgnoredError(text)

        if "No nodes defined." in flat_text:
            text += base_error_msg
            raise MapdlCommandIgnoredError(text)

        if "For element type = " in flat_text and "is invalid." in flat_text:
            if "is normal behavior when a CDB file is used." in flat_text:
                warn(text, UserWarning)
            else:
                text += base_error_msg
                raise MapdlCommandIgnoredError(text)

        if "Cannot create another with the same name" in flat_text:
            # When overriding constitutive models. See 'test_tbft'
            warn(text, UserWarning)

        # flag errors
        if "*** ERROR ***" in flat_text:
            self._raise_output_errors(text)

    def _raise_output_errors(self, response):
        """Raise errors in the MAPDL response.

        Parameters
        ----------
        response : str
            Response from MAPDL.

        Raises
        ------
        MapdlRuntimeError
            For most of the errors.
        """
        # The logic is to iterate for each line. If the error header is found,
        # we analyse the following 'lines_number' in other to get the full error method.
        # Then with regex, we collect the error message, and raise it.
        for index, each_line in enumerate(response.splitlines()):
            if "*** ERROR ***" in each_line:
                error_is_fine = False

                # Extracting only the first 'lines_number' lines.
                # This is important. Regex has problems parsing long messages.
                lines_number = 20
                if len(response.splitlines()) <= lines_number:
                    partial_output = response
                else:
                    partial_output = "\n".join(
                        response.splitlines()[index : (index + lines_number)]
                    )

                # Find the error message.
                # Either ends with the beginning of another error message or with double empty line.
                error_message = re.search(
                    r"(\*\*\* ERROR \*\*\*.*?).*(?=\*\*\*|.*\n\n)",  # we might consider to use only one \n.
                    partial_output,
                    re.DOTALL,
                )

                if not error_message:
                    # Since we couldn't find an error message, the full partial message (10 lines) is analysed
                    self._log.debug(
                        f"PyMAPDL could not identify the error message, the full partial message ({lines_number} lines) is analysed"
                    )
                    error_message = partial_output
                else:
                    # Catching only the first error.
                    error_message = error_message.group(0)

                # Trimming empty lines
                error_message = "\n".join(
                    [each for each in error_message.splitlines() if each]
                )

                # Checking for permitted error.
                for each_error in _PERMITTED_ERRORS:
                    permited_error_message = re.search(each_error, error_message)

                    if permited_error_message:
                        error_is_fine = True
                        break

                # Raising errors
                if error_is_fine:
                    self._log.warning(
                        "PERMITTED ERROR: " + permited_error_message.string
                    )
                    continue
                else:
                    # We don't need to log exception because they already included in the main logger.
                    # logger.error(response)
                    # However, exceptions are recorded in the global logger which do not record
                    # information of the instances name, hence we edit the error message.
                    raise MapdlRuntimeError(
                        f"\n\nError in instance {self.name}\n\n" + error_message
                    )

    def _check_parameter_name(self, param_name):
        """Checks if a parameter name is allowed or not."""
        if not self.check_parameter_names:
            return

        param_name = param_name.strip()

        match_valid_parameter_name = (
            r"^[a-zA-Z_][a-zA-Z\d_\(\),\s\%]{0," + f"{MAX_PARAM_CHARS-1}" + r"}$"
        )
        # Using % is allowed, because of substitution, but it is very likely MAPDL will complain.
        if not re.search(match_valid_parameter_name, param_name):
            raise ValueError(
                f"The parameter name `{param_name}` is an invalid parameter name. "
                f"Only letters, numbers and `_` are permitted, up to {MAX_PARAM_CHARS} characters long. "
                "It cannot start with a number either."
            )

        if "(" in param_name or ")" in param_name:
            if param_name.count("(") != param_name.count(")"):
                raise ValueError(
                    "The parameter name should have all the parenthesis in pairs (closed)."
                )

            if param_name[-1] != ")":
                raise ValueError(
                    "If using parenthesis (indexing), you cannot use any character after the closing parenthesis."
                )

            # Check recursively the parameter name without parenthesis.
            # This is the real parameter name, however it must already exists to not raise an error.
            sub_param_name = re.findall(r"^(.*)\(", param_name)
            if sub_param_name:
                self._check_parameter_name(sub_param_name[0])
                return  # Following checks should not run against the parenthesis

        # Using leading underscored parameters
        match_reserved_leading_underscored_parameter_name = (
            r"^_[a-zA-Z\d_\(\),\s_]{1," + f"{MAX_PARAM_CHARS}" + r"}[a-zA-Z\d\(\),\s]$"
        )
        # If it also ends in underscore, this won't be triggered.
        if re.search(match_reserved_leading_underscored_parameter_name, param_name):
            raise ValueError(
                "It is discouraged the use of parameters starting with underscore ('_'). "
                "This convention is reserved for parameters used by the GUI and/or Mechanical APDL-provided macros."
            )

        # invalid parameter (using ARGXX or ARXX)
        match_reserved_arg_parameter_name = r"^(AR|ARG)(\d{1,3})$"
        if re.search(
            match_reserved_arg_parameter_name, param_name
        ):  # invalid parameter (using ARGXX or ARXX)
            raise ValueError(
                "The parameters 'ARGXX' and 'ARXX' where 'XX' are integers, are reserved for functions and macros local parameters."
                "Hence its use is not recommended outside them."
                "You might run in unexpected behaviours, for example, parameters not being show in `mapdl.parameters`."
            )
