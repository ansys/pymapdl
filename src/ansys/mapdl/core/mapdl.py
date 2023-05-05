"""Module to control interaction with MAPDL through Python"""

import atexit
from functools import wraps
import glob
import logging
import os
import pathlib
import re
from shutil import copyfile, rmtree
from subprocess import DEVNULL, call
import tempfile
import time
import warnings
from warnings import warn
import weakref

import numpy as np

from ansys.mapdl import core as pymapdl
from ansys.mapdl.core import LOG as logger
from ansys.mapdl.core import _HAS_PYVISTA
from ansys.mapdl.core.commands import (
    CMD_BC_LISTING,
    CMD_LISTING,
    CMD_XSEL,
    XSEL_DOCSTRING_INJECTION,
    BoundaryConditionsListingOutput,
    CommandListingOutput,
    Commands,
    StringWithLiteralRepr,
    inject_docs,
)
from ansys.mapdl.core.errors import (
    IncorrectWorkingDirectory,
    MapdlCommandIgnoredError,
    MapdlInvalidRoutineError,
    MapdlRuntimeError,
)
from ansys.mapdl.core.inline_functions import Query
from ansys.mapdl.core.misc import (
    Information,
    allow_pickable_points,
    check_valid_routine,
    last_created,
    load_file,
    random_string,
    requires_package,
    run_as_prep7,
    supress_logging,
    wrap_point_SEL,
)

if _HAS_PYVISTA:
    from ansys.mapdl.core.plotting import general_plotter

from ansys.mapdl.core.post import PostProcessing

_PERMITTED_ERRORS = [
    r"(\*\*\* ERROR \*\*\*).*(?:[\r\n]+.*)+highly distorted.",
    r"(\*\*\* ERROR \*\*\*).*[\r\n]+.*is turning inside out.",
    r"(\*\*\* ERROR \*\*\*).*[\r\n]+.*The distributed memory parallel solution does not support KRYLOV method",
]

# test for png file
PNG_TEST = re.compile("WRITTEN TO FILE(.*).png")

VWRITE_REPLACEMENT = """
Cannot use *VWRITE directly as a command in MAPDL
service mode.  Instead, run it as ``non_interactive``.

For example:

with self.non_interactive:
    self.vwrite('%s(1)' % parm_name)
    self.run('(F20.12)')
"""

## Invalid commands in interactive mode.
INVAL_COMMANDS = {
    "*VWR": VWRITE_REPLACEMENT,
    "*CFO": "Run CFOPEN as ``non_interactive``",
    "*CRE": "Create a function within python or run as non_interactive",
    "*END": "Create a function within python or run as non_interactive",
    "/EOF": "Unsupported command.  Use ``exit`` to stop the server.",
    "*ASK": "Unsupported command.  Use python ``input`` instead.",
    "*IF": "Use a python ``if`` or run as non_interactive",
    "CMAT": "Run `CMAT` as ``non_interactive``.",
    "*REP": "Run '*REPEAT' in ``non_interactive``.",
    "LSRE": "Run 'LSREAD' in ``non_interactive``.",
}

## Soft-invalid commands
# Invalid commands in interactive mode but their execution is just ignored.
# The correspondent command is replaced by a comment using the command '\COM'
# and a warning is recorded in the logger
#
# This commands can still be executed in ``non_interactive`` mode or using
# ``Mapdl._run`` method.
#
# Format of the message:
# f"{CMD} is ignored: {INVAL_COMMANDS_SILENT[CMD]}.
#
# NOTE
# Obtain the command from the string supplied using
#
#    string.split(',')[0].upper()
#
# This way to get the command is different from the one used in ``INVAL_COMMANDS``.
#
INVAL_COMMANDS_SILENT = {
    "/NOPR": "Suppressing console output is not recommended, use ``Mute`` parameter instead. This command is disabled in interactive mode."
}

PLOT_COMMANDS = ["NPLO", "EPLO", "KPLO", "LPLO", "APLO", "VPLO", "PLNS", "PLES"]
MAX_COMMAND_LENGTH = 600  # actual is 640, but seems to fail above 620


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


def setup_logger(loglevel="INFO", log_file=True, mapdl_instance=None):
    """Setup logger"""

    # return existing log if this function has already been called
    if hasattr(setup_logger, "log"):
        return setup_logger.log
    else:
        setup_logger.log = logger.add_instance_logger("MAPDL", mapdl_instance)

    return setup_logger.log


_ALLOWED_START_PARM = [
    "additional_switches",
    "exec_file",
    "ip",
    "jobname",
    "local",
    "nproc",
    "override",
    "port",
    "print_com",
    "process",
    "ram",
    "run_location",
    "start_timeout" "timeout",
]


def _sanitize_start_parm(start_parm):
    for each_key in start_parm:
        if each_key not in _ALLOWED_START_PARM:
            raise ValueError(f"The argument '{each_key}' is not recognaised.")


class _MapdlCore(Commands):
    """Contains methods in common between all Mapdl subclasses"""

    def __init__(
        self,
        loglevel="DEBUG",
        use_vtk=None,
        log_apdl=None,
        log_file=False,
        local=True,
        print_com=False,
        **start_parm,
    ):
        """Initialize connection with MAPDL."""
        atexit.register(self.__del__)  # registering to exit properly
        self._name = None  # For naming the instance.
        self._show_matplotlib_figures = True  # for testing
        self._query = None
        self._exited = False
        self._ignore_errors = False
        self._apdl_log = None
        self._store_commands = False
        self._stored_commands = []
        self._response = None
        self._mode = None
        self._mapdl_process = None
        self._launched = False
        self._stderr = None
        self._stdout = None

        if _HAS_PYVISTA:
            if use_vtk is not None:  # pragma: no cover
                self._use_vtk = use_vtk
            else:
                self._use_vtk = True
        else:  # pragma: no cover
            if use_vtk:
                raise ModuleNotFoundError(
                    f"Using the keyword argument 'use_vtk' requires having Pyvista installed."
                )
            else:
                self._use_vtk = False

        self._log_filehandler = None
        self._version = None  # cached version
        self._local = local
        self._cleanup = True
        self._vget_arr_counter = 0
        self._cached_routine = None
        self._geometry = None
        self._krylov = None
        self._on_docker = None
        self._platform = None

        _sanitize_start_parm(start_parm)
        self._start_parm = start_parm
        self._jobname = start_parm.get("jobname", "file")
        self._path = start_parm.get("run_location", None)
        self._print_com = print_com  # print the command /COM input.

        # Setting up loggers
        self._log = logger.add_instance_logger(
            self.name, self, level=loglevel
        )  # instance logger
        # adding a file handler to the logger
        if log_file:
            if not isinstance(log_file, str):
                log_file = "instance.log"
            self._log.log_to_file(filename=log_file, level=loglevel)

        self._log.debug("Logging set to %s", loglevel)

        from ansys.mapdl.core.parameters import Parameters

        self._parameters = Parameters(self)

        from ansys.mapdl.core.solution import Solution

        self._solution = Solution(self)

        from ansys.mapdl.core.xpl import ansXpl

        self._xpl = ansXpl(self)

        if log_apdl:
            self.open_apdl_log(log_apdl, mode="w")

        self._post = PostProcessing(self)

        # Wrapping listing functions for "to_array" methods
        self._wrap_listing_functions()

        # Wrapping XSEL commands to return ids.
        self._xsel_mapdl_output = False
        self._wrap_xsel_commands()

        self._info = Information(self)

    @property
    def print_com(self):
        return self._print_com

    @print_com.setter
    def print_com(self, value):
        if isinstance(value, bool):
            status = "activated" if value else "deactivated"
            self._log.debug(f"The print of '/COM' commands has been {status}.")
            self._print_com = value
        else:
            raise ValueError(
                f"The property ``print_com`` only allows booleans, but type {type(value)} was supplied."
            )

    @property
    def mode(self):
        """Return the type of instance, namely: grpc, corba or console."""
        return self._mode

    @property
    def is_grpc(self):
        """Return true if using grpc to connect to the MAPDL instance."""
        return self._mode == "grpc"

    @property
    def is_corba(self):
        """Return true if using corba to connect to the MAPDL instance."""
        return self._mode == "corba"

    @property
    def is_console(self):
        """Return true if using console to connect to the MAPDL instance."""
        return self._mode == "console"

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

    def _wrap_xsel_commands(self):
        # Wrapping XSEL commands.
        def wrap_xsel_function(func):
            if hasattr(func, "__func__"):
                func.__func__.__doc__ = inject_docs(
                    func.__func__.__doc__, XSEL_DOCSTRING_INJECTION
                )
            else:  # pragma: no cover
                func.__doc__ = inject_docs(func.__doc__, XSEL_DOCSTRING_INJECTION)

            def wrap_xsel_function_output(method):
                # Injecting doc string modification
                name = method.__func__.__name__.upper()
                if name == "NSEL":
                    return self.mesh.nnum
                elif name == "ESEL":
                    return self.mesh.enum
                elif name == "KSEL":
                    return self.geometry.knum
                elif name == "LSEL":
                    return self.geometry.lnum
                elif name == "ASEL":
                    return self.geometry.anum
                elif name == "VSEL":
                    return self.geometry.vnum
                else:
                    return None

            @wraps(func)
            def inner_wrapper(*args, **kwargs):
                # in interactive mode (item='p'), the output is not suppressed
                is_interactive_arg = (
                    True
                    if len(args) >= 2
                    and isinstance(args[1], str)
                    and args[1].upper() == "P"
                    else False
                )
                is_interactive_kwarg = (
                    True
                    if "item" in kwargs and kwargs["item"].upper() == "P"
                    else False
                )

                return_mapdl_output = kwargs.pop(
                    "return_mapdl_output", self._xsel_mapdl_output
                )
                if is_interactive_arg or is_interactive_kwarg:
                    return_mapdl_output = True

                output = func(*args, **kwargs)
                if not return_mapdl_output:
                    output = wrap_xsel_function_output(func)
                return output

            return inner_wrapper

        for name in dir(self):
            if name[0:4].upper() in CMD_XSEL and name in dir(
                Commands
            ):  # avoid matching Mapdl properties which starts with same letters as MAPDL commands.
                method = self.__getattribute__(name)
                setattr(self, name, wrap_xsel_function(method))

    @property
    def name(self):  # pragma: no cover
        raise NotImplementedError("Implemented by child classes.")

    @name.setter
    def name(self, name):  # pragma: no cover
        raise AttributeError("The name of an instance cannot be changed.")

    @property
    def queries(self):
        """Get instance of Query class containing inline functions of APDL.

        Most of the results of these methods are shortcuts for specific
        combinations of arguments supplied to :func:`ansys.mapdl.core.Mapdl.get`.

        Currently implemented functions:

        - ``centrx(e)`` - get the centroid x-coordinate of element `e`
        - ``centry(e)`` - get the centroid y-coordinate of element `e`
        - ``centrz(e)`` - get the centroid z-coordinate of element `e`
        - ``nx(n)`` - get the x-coordinate of node `n`
        - ``ny(n)`` - get the y-coordinate of node `n`
        - ``nz(n)`` - get the z-coordinate of node `n`
        - ``kx(k)`` - get the x-coordinate of keypoint `k`
        - ``ky(k)`` - get the y-coordinate of keypoint `k`
        - ``kz(k)`` - get the z-coordinate of keypoint `k`
        - ``lx(n, lfrac)`` - X-coordinate of line ``n`` at length fraction ``lfrac``
        - ``ly(n, lfrac)`` - Y-coordinate of line ``n`` at length fraction ``lfrac``
        - ``lz(n, lfrac)`` - Z-coordinate of line ``n`` at length fraction ``lfrac``
        - ``lsx(n, lfrac)`` - X-slope of line ``n`` at length fraction ``lfrac``
        - ``lsy(n, lfrac)`` - Y-slope of line ``n`` at length fraction ``lfrac``
        - ``lsz(n, lfrac)`` - Z-slope of line ``n`` at length fraction ``lfrac``
        - ``ux(n)`` - get the structural displacement at node `n` in x
        - ``uy(n)`` - get the structural displacement at node `n` in y
        - ``uz(n)`` - get the structural displacement at node `n` in z
        - ``rotx(n)`` - get the rotational displacement at node `n` in x
        - ``roty(n)`` - get the rotational displacement at node `n` in y
        - ``rotz(n)`` - get the rotational displacement at node `n` in z
        - ``nsel(n)`` - get the selection status of node `n`
        - ``ksel(k)`` - get the selection status of keypoint `k`
        - ``lsel(n)`` - get the selection status of line `n`
        - ``asel(a)`` - get the selection status of area `a`
        - ``esel(n)`` - get the selection status of element `e`
        - ``vsel(v)`` - get the selection status of volume `v`
        - ``ndnext(n)`` - get the next selected node with a number greater than `n`.
        - ``kpnext(k)`` - get the next selected keypoint with a number greater than `k`.
        - ``lsnext(n)`` - get the next selected line with a number greater than `n`.
        - ``arnext(a)`` - get the next selected area with a number greater than `a`.
        - ``elnext(e)`` - get the next selected element with a number greater than `e`.
        - ``vlnext(v)`` - get the next selected volume with a number greater than `v`.
        - ``node(x, y, z)`` - get the node closest to coordinate (x, y, z)
        - ``kp(x, y, z)`` - get the keypoint closest to coordinate (x, y, z)

        Returns
        -------
        :class:`ansys.mapdl.core.inline_functions.Query`
            Instance of the Query class

        Examples
        --------
        In this example we construct a solid box and mesh it. Then we use
        the ``Query`` methods ``nx``, ``ny``, and ``nz`` to find the
        cartesian coordinates of the first node.

        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> mapdl.et(1, 'SOLID5')
        >>> mapdl.block(0, 10, 0, 20, 0, 30)
        >>> mapdl.esize(2)
        >>> mapdl.vmesh('ALL')
        >>> q = mapdl.queries
        >>> q.nx(1), q.ny(1), q.nz(1)
        0.0 20.0 0.0


        """
        if self._query is None:
            self._query = Query(self)
        return self._query

    @property
    def non_interactive(self):
        """Non-interactive context manager.

        Allow to execute code without user interaction or waiting
        between PyMAPDL responses.
        It can also be used to execute some commands which are not
        supported in interactive mode. For a complete list of commands
        visit :ref:`ref_unsupported_interactive_commands`.

        View the last response with :attr:`Mapdl.last_response` method.

        Notes
        -----
        All the commands executed inside this context manager are not
        executed until the context manager exits which then execute them
        all at once in the MAPDL instance.

        This command uses :func:`Mapdl.input() <ansys.mapdl.core.Mapdl.input>`
        method.

        Examples
        --------
        Use the non-interactive context manager for the VWRITE (
        :func:`Mapdl.vwrite() <ansys.mapdl.core.Mapdl.vwrite>`)
        command.

        >>> with mapdl.non_interactive:
        ...    mapdl.run("*VWRITE,LABEL(1),VALUE(1,1),VALUE(1,2),VALUE(1,3)")
        ...    mapdl.run("(1X,A8,'   ',F10.1,'  ',F10.1,'   ',1F5.3)")
        >>> mapdl.last_response

        """
        return self._non_interactive(self)

    @property
    def force_output(self):
        """Force text output globally by turning the ``Mapdl.mute`` attribute to False
        and activating text output (``/GOPR``)

        You can still do changes to those inside this context.

        """
        return self._force_output(self)

    @property
    def solution(self):
        """Solution parameters of MAPDL.

        Returns
        -------
        :class:`ansys.mapdl.core.solution.Solution`

        Examples
        --------
        Check if a solution has converged.

        >>> mapdl.solution.converged
        """
        if self._exited:
            raise MapdlRuntimeError("MAPDL exited.")
        return self._solution

    @property
    def _distributed(self):
        """MAPDL is running in distributed mode."""
        return "-smp" not in self._start_parm.get("additional_switches", "")

    @property
    def post_processing(self):
        """Post-process an active MAPDL session.

        Examples
        --------
        Get the nodal displacement in the X direction for the first
        result set.

        >>> mapdl.set(1, 1)
        >>> disp_x = mapdl.post_processing.nodal_displacement('X')
        array([1.07512979e-04, 8.59137773e-05, 5.70690047e-05, ...,
               5.70333124e-05, 8.58600402e-05, 1.07445726e-04])
        """
        if self._exited:
            raise MapdlRuntimeError(
                "MAPDL exited.\n\nCan only postprocess a live " "MAPDL instance."
            )
        return self._post

    @property
    def chain_commands(self):
        """Chain several mapdl commands.

        Commands can be separated with ``"$"`` in MAPDL rather than
        with a line break, so you could send multiple commands to
        MAPDL with:

        ``mapdl.run("/PREP7$K,1,1,2,3")``

        This method is merely a convenience context manager to allow
        for easy chaining of PyMAPDL commands to speed up sending
        commands to MAPDL.

        View the response from MAPDL with :attr:`Mapdl.last_response`.

        Notes
        -----
        Distributed Ansys cannot properly handle condensed data input
        and chained commands are not permitted in distributed ansys.

        Examples
        --------
        >>> with mapdl.chain_commands:
            mapdl.prep7()
            mapdl.k(1, 1, 2, 3)

        """
        if self._distributed:
            raise MapdlRuntimeError(
                "Chained commands are not permitted in distributed ansys."
            )
        return self._chain_commands(self)

    def _chain_stored(self):
        """Send a series of commands to MAPDL"""
        # there's to be an limit to 640 characters per command, so
        # when chaining commands they must be shorter than 640 (minus
        # some overhead).
        c = 0
        chained_commands = []
        chunk = []
        for command in self._stored_commands:
            len_command = len(command) + 1  # include sep var
            if len_command + c > MAX_COMMAND_LENGTH:
                chained_commands.append("$".join(chunk))
                chunk = [command]
                c = 0
            else:
                chunk.append(command)
                c += len_command

        # join the last
        chained_commands.append("$".join(chunk))
        self._stored_commands = []

        responses = [self._run(command) for command in chained_commands]
        self._response = "\n".join(responses)

    @property
    def parameters(self):
        """Collection of MAPDL parameters.

        Notes
        -----
        See :ref:`ref_special_named_param` for additional notes regarding parameter naming in MAPDL.

        Examples
        --------
        Simply list all parameters except for MAPDL MATH parameters.

        >>> mapdl.parameters
        ARR                              : ARRAY DIM (3, 1, 1)
        PARM_FLOAT                       : 20.0
        PARM_INT                         : 10.0
        PARM_LONG_STR                    : "stringstringstringstringstringst"
        PARM_STR                         : "string"
        PORT                             : 50052.0

        Get a parameter

        >>> mapdl.parameters['PARM_FLOAT']
        20.0

        Get an array parameter

        >>> mapdl.parameters['ARR']
        array([1., 2., 3.])

        """
        return self._parameters

    class _non_interactive:
        """Allows user to enter commands that need to run non-interactively."""

        def __init__(self, parent):
            self._parent = weakref.ref(parent)

        def __enter__(self):
            self._parent()._log.debug("Entering non-interactive mode")
            self._parent()._store_commands = True

        def __exit__(self, *args):
            self._parent()._log.debug("Exiting non-interactive mode")
            self._parent()._flush_stored()
            self._parent()._store_commands = False

    class _chain_commands:
        """Store MAPDL commands and send one chained command."""

        def __init__(self, parent):
            self._parent = weakref.ref(parent)

        def __enter__(self):
            self._parent()._log.debug("Entering chained command mode")
            self._parent()._store_commands = True

        def __exit__(self, *args):
            self._parent()._log.debug("Entering chained command mode")
            self._parent()._chain_stored()
            self._parent()._store_commands = False

    class _RetainRoutine:
        """Store MAPDL's routine when entering and reverts it when exiting."""

        def __init__(self, parent, routine):
            self._parent = weakref.ref(parent)

            # check the routine is valid since we're muting the output
            check_valid_routine(routine)
            self._requested_routine = routine

        def __enter__(self):
            """Store the current routine and enter the requested routine."""
            self._cached_routine = self._parent().parameters.routine
            self._parent()._log.debug("Caching routine %s", self._cached_routine)
            if self._requested_routine.lower() != self._cached_routine.lower():
                self._enter_routine(self._requested_routine)

        def __exit__(self, *args):
            """Restore the original routine."""
            self._parent()._log.debug("Restoring routine %s", self._cached_routine)
            self._enter_routine(self._cached_routine)

        def _enter_routine(self, routine):
            """Enter a routine."""
            if routine.lower() == "begin level":
                self._parent().finish(mute=True)
            else:
                self._parent().run(f"/{routine}", mute=True)

    def run_as_routine(self, routine):
        """
        Runs a command or commands at a routine and then revert to the prior routine.

        This can be useful to avoid constantly changing between routines.

        Parameters
        ----------
        routine : str
            A MAPDL routine. For example, ``"PREP7"`` or ``"POST1"``.

        Examples
        --------
        Enter ``PREP7`` and run ``numvar``, which requires ``POST26``, and
        revert to the prior routine.

        >>> mapdl.prep7()
        >>> mapdl.parameters.routine
        'PREP7'
        >>> with mapdl.run_as_routine('POST26'):
        ...     mapdl.numvar(200)
        >>> mapdl.parameters.routine
        'PREP7'

        """
        return self._RetainRoutine(self, routine)

    @property
    def last_response(self):
        """Returns the last response from MAPDL.

        Examples
        --------
        >>> mapdl.last_response
        'KEYPOINT      1   X,Y,Z=   1.00000       1.00000       1.00000'
        """
        return self._response

    def clear(self, *args, **kwargs):
        """Clear the database.

        APDL Command: ``/CLEAR``

        Resets the ANSYS database to the conditions at the beginning
        of the problem.  Sets the import and Boolean options back to
        the ANSYS default. All items are deleted from the database and
        memory values are set to zero for items derived from database
        information.  All files are left intact.  This command is
        useful between multiple analyses in the same run, or between
        passes of a multi-pass analysis (such as between the
        substructure generation, use, and expansion passes).  Should
        not be used in a do-loop since loop counters will be reset.
        on the same line as the ``/CLEAR`` command.

        ``/CLEAR`` resets the jobname to match the currently open
        session .LOG and .ERR files. This will return the jobname to
        its original value, or to the most recent value specified on
        ``/FILNAME`` with KEY = 1.

        This command is valid only at the Begin level.

        Examples
        --------
        >>> mapdl.clear()

        """
        self.run("/CLE,NOSTART", mute=True)

    @supress_logging
    def __str__(self):
        return self.info.__str__()

    @property
    def info(self):
        """General information"""
        return self._info

    @property
    @requires_package("pyvista", softerror=True)
    def geometry(self):
        """Geometry information.

        See :class:`ansys.mapdl.core.mapdl_geometry.Geometry`

        Examples
        --------
        Print the current status of the geometry.

        >>> print(mapdl.geometry)
        MAPDL Selected Geometry
        Keypoints:  8
        Lines:      12
        Areas:      6
        Volumes:    1

        Return the number of lines.

        >>> mapdl.geometry.n_line
        12

        Return the number of areas.

        >>> mapdl.geometry.n_area
        6

        Select a list of keypoints.

        >>> mapdl.geometry.keypoint_select([1, 5, 10])

        Append to an existing selection of lines.

        >>> mapdl.geometry.line_select([1, 2, 3], sel_type='A')

        Reselect from the existing selection of lines.

        >>> mapdl.geometry.line_select([3, 4, 5], sel_type='R')

        """
        if self._geometry is None:
            self._geometry = self._create_geometry()
        return self._geometry

    def _create_geometry(self):  # pragma: no cover
        """Return geometry cache"""
        from ansys.mapdl.core.mapdl_geometry import Geometry

        return Geometry(self)

    @property
    @requires_package("pyvista", softerror=True)
    def mesh(self):
        """Mesh information.

        Returns
        -------
        :class:`Mapdl.Mesh <ansys.mapdl.core.mesh_grpc.Mesh>`

        Examples
        --------
        Return an array of the active nodes

        >>> mapdl.mesh.nodes
        array([[ 1.,  0.,  0.],
               [ 2.,  0.,  0.],
               [ 3.,  0.,  0.],
               [ 4.,  0.,  0.],
               [ 5.,  0.,  0.],
               [ 6.,  0.,  0.],
               [ 7.,  0.,  0.],
               [ 8.,  0.,  0.],
               [ 9.,  0.,  0.],
               [10.,  0.,  0.]])

        Return an array of the node numbers of the active nodes

        >>> mapdl.mesh.nnum
        array([ 1,  2,  3,  4,  5,  6,  7,  8,  9, 10], dtype=int32)

        Simply query and print the geometry

        >>> print(mapdl.mesh)
          ANSYS Mapdl Mesh
          Number of Nodes:              321
          Number of Elements:           40
          Number of Element Types:      1
          Number of Node Components:    2
          Number of Element Components: 2

        Access the geometry as a VTK object

        >>> mapdl.mesh.grid

        """
        return self._mesh

    @property
    @requires_package("ansys.mapdl.reader", softerror=True)
    @supress_logging
    def _mesh(self):
        """Write entire archive to ASCII and read it in as an
        ``ansys.mapdl.core.Archive``"""
        # lazy import here to avoid loading pyvista and vtk
        from ansys.mapdl.reader import Archive

        if self._archive_cache is None:
            # write database to an archive file
            arch_filename = os.path.join(self.directory, "_tmp.cdb")
            nblock_filename = os.path.join(self.directory, "nblock.cdb")

            # must have all nodes elements are using selected
            if hasattr(self, "mute"):
                old_mute = self.mute
                self.mute = True

            self.cm("__NODE__", "NODE", mute=True)
            self.nsle("S", mute=True)
            self.cdwrite("db", arch_filename, mute=True)
            self.cmsel("S", "__NODE__", "NODE", mute=True)

            self.cm("__ELEM__", "ELEM", mute=True)
            self.esel("NONE", mute=True)
            self.cdwrite("db", nblock_filename, mute=True)
            self.cmsel("S", "__ELEM__", "ELEM", mute=True)

            if hasattr(self, "mute"):
                self.mute = old_mute

            self._archive_cache = Archive(arch_filename, parse_vtk=False, name="Mesh")
            grid = self._archive_cache._parse_vtk(additional_checking=True)
            self._archive_cache._grid = grid

            # rare bug
            if grid is not None:
                if grid.n_points != self._archive_cache.n_node:
                    self._archive_cache = Archive(
                        arch_filename, parse_vtk=True, name="Mesh"
                    )

            # overwrite nodes in archive
            nblock = Archive(nblock_filename, parse_vtk=False)
            self._archive_cache._nodes = nblock._nodes
            self._archive_cache._nnum = nblock._nnum
            self._archive_cache._node_coord = None

        return self._archive_cache

    def _reset_cache(self):
        """Reset cached items"""
        self._archive_cache = None

    @property
    def allow_ignore(self):
        """Invalid commands will be ignored rather than exceptions

        A command executed in the wrong processor will raise an
        exception when ``allow_ignore=False``.  This is the default
        behavior.

        Examples
        --------
        >>> mapdl.post1()
        >>> mapdl.k(1, 0, 0, 0)
        Exception:  K is not a recognized POST1 command, abbreviation, or macro.

        Ignore these messages by setting allow_ignore=True

        >>> mapdl.allow_ignore = True
        2020-06-08 21:39:58,094 [INFO] : K is not a
        recognized POST1 command, abbreviation, or macro.  This
        command will be ignored.

        *** WARNING *** CP = 0.372 TIME= 21:39:58
        K is not a recognized POST1 command, abbreviation, or macro.
        This command will be ignored.

        """
        warn(
            "'allow_ignore' is being deprecated and will be removed in a future release. "
            "Use ``mapdl.ignore_errors`` instead.",
            DeprecationWarning,
        )
        return self._ignore_errors

    @allow_ignore.setter
    def allow_ignore(self, value):
        """Set allow ignore"""
        warn(
            "'allow_ignore' is being deprecated and will be removed in a future release. "
            "Use ``mapdl.ignore_errors`` instead.",
            DeprecationWarning,
        )
        self._ignore_errors = bool(value)

    def open_apdl_log(self, filename, mode="w"):
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
        if self._apdl_log is not None:
            raise MapdlRuntimeError("APDL command logging already enabled")
        self._log.debug("Opening ANSYS log file at %s", filename)

        if mode not in ["w", "a", "x"]:
            raise ValueError(
                "File mode should either be write, append, or exclusive"
                " creation ('w', 'a', or 'x')."
            )

        self._apdl_log = open(filename, mode=mode, buffering=1)  # line buffered
        self._apdl_log.write(
            f"! APDL log script generated using PyMapdl (ansys.mapdl.core {pymapdl.__version__})\n"
        )

    @supress_logging
    @run_as_prep7
    def _generate_iges(self):
        """Save IGES geometry representation to disk"""
        filename = os.path.join(self.directory, "_tmp.iges")
        self.igesout(filename, att=1, mute=True)
        return filename

    def open_gui(self, include_result=None, inplace=None):  # pragma: no cover
        """Save the existing database and open it up in the MAPDL GUI.

        Parameters
        ----------
        include_result : bool, optional
            Allow the result file to be post processed in the GUI.  It is
            ignored if ``inplace`` is ``True``.  By default, ``True``.

        inplace : bool, optional
            Open the GUI on the current MAPDL working directory, instead of
            creating a new temporary directory and coping the results files
            over there.  If ``True``, ignores ``include_result`` parameter.  By
            default, this ``False``.

        Examples
        --------
        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()

        Create a square area using keypoints.

        >>> mapdl.prep7()
        >>> mapdl.k(1, 0, 0, 0)
        >>> mapdl.k(2, 1, 0, 0)
        >>> mapdl.k(3, 1, 1, 0)
        >>> mapdl.k(4, 0, 1, 0)
        >>> mapdl.l(1, 2)
        >>> mapdl.l(2, 3)
        >>> mapdl.l(3, 4)
        >>> mapdl.l(4, 1)
        >>> mapdl.al(1, 2, 3, 4)

        Open up the gui.

        >>> mapdl.open_gui()

        Resume where you left off.

        >>> mapdl.et(1, 'MESH200', 6)
        >>> mapdl.amesh('all')
        >>> mapdl.eplot()
        """
        # lazy load here to avoid circular import
        from ansys.mapdl.core.launcher import get_ansys_path

        if not self._local:
            raise MapdlRuntimeError(
                "``open_gui`` can only be called from a local MAPDL instance."
            )

        if inplace and include_result:
            raise ValueError(
                "'inplace' and 'include_result' kwargs are not compatible."
            )

        if inplace and include_result is None:
            include_result = False

        if include_result is None:
            include_result = True

        if not inplace:
            inplace = False

        name = self.jobname

        # specify a path for the temporary database if any.
        if inplace:
            run_dir = self._start_parm["run_location"]

        else:
            temp_dir = tempfile.gettempdir()
            run_dir = os.path.join(temp_dir, f"ansys_{random_string(10)}")

            # Sanity checks
            if os.path.isdir(run_dir):
                rmtree(run_dir)
            os.mkdir(run_dir)

        database_file = os.path.join(run_dir, f"{name}.db")
        if os.path.isfile(database_file) and not inplace:
            os.remove(database_file)

        # cache result file, version, and routine before closing
        resultfile = self._result_file
        version = self.version
        self._cache_routine()

        # finish, save and exit the server
        self.finish(mute=True)
        self.save(database_file, mute=True)

        # Exit and do not remove the temporary directory. This is backwards
        # compatible with CONSOLE and CORBA modes.
        remove_tmp = False
        if hasattr(self, "_remove_tmp"):
            remove_tmp = self._remove_tmp
        self._remove_tmp = False
        self.exit()

        # copy result file to temp directory
        if not inplace:
            if include_result and self._result_file is not None:
                if os.path.isfile(resultfile):
                    tmp_resultfile = os.path.join(run_dir, "%s.rst" % name)
                    copyfile(resultfile, tmp_resultfile)

        # write temporary input file
        start_file = os.path.join(run_dir, f"start{version}.ans")
        with open(start_file, "w") as f:
            f.write("RESUME\n")

        # some versions of ANSYS just look for "start.ans" when starting
        other_start_file = os.path.join(run_dir, "start.ans")
        with open(other_start_file, "w") as f:
            f.write("RESUME\n")

        # issue system command to run ansys in GUI mode
        cwd = os.getcwd()
        os.chdir(run_dir)
        exec_file = self._start_parm.get("exec_file", get_ansys_path(allow_input=False))
        nproc = self._start_parm.get("nproc", 2)
        add_sw = self._start_parm.get("additional_switches", "")

        if inplace:
            warn(
                "MAPDL GUI has been opened using 'inplace' kwarg. "
                f"The changes you make will overwrite the files in {run_dir}."
            )

        call(
            f'cd "{run_dir}" && "{exec_file}" -g -j {name} -np {nproc} {add_sw}',
            shell=True,
            stdout=DEVNULL,
        )

        # Going back
        os.chdir(cwd)

        # Clearing
        os.remove(start_file)
        os.remove(other_start_file)

        # reattach to a new session and reload database
        self._launch(self._start_parm)
        self.resume(database_file, mute=True)

        # restore remove tmp state
        self._remove_tmp = remove_tmp

    def _cache_routine(self):
        """Cache the current routine."""
        self._cached_routine = self.parameters.routine

    def _resume_routine(self):
        """Resume the cached routine."""
        if self._cached_routine is not None:
            if "BEGIN" not in self._cached_routine:
                self.run(f"/{self._cached_routine}", mute=True)
            else:
                self.finish(mute=True)
            self._cached_routine = None

    def _launch(self, *args, **kwargs):  # pragma: no cover
        raise NotImplementedError("Implemented by child class")

    def _close_apdl_log(self):
        """Closes the APDL log"""
        if self._apdl_log is not None:
            self._apdl_log.close()
        self._apdl_log = None

    def nplot(self, nnum="", vtk=None, **kwargs):
        """APDL Command: NPLOT

        Displays nodes.

        .. note::
           PyMAPDL plotting commands with ``vtk=True`` ignore any
           values set with the ``PNUM`` command.

        Parameters
        ----------
        nnum : bool, int, optional
            Node number key:

            - ``False`` : No node numbers on display (default).
            - ``True`` : Include node numbers on display.

            .. note::
               This parameter is only valid when ``vtk==True``

        vtk : bool, optional
            Plot the currently selected nodes using ``pyvista``.
            Defaults to current ``use_vtk`` setting as set on the
            initialization of MAPDL.

        plot_bc : bool, optional
            Activate the plotting of the boundary conditions.
            Defaults to ``False``.

            .. warning:: This is in alpha state.

        plot_bc_legend : bool, optional
            Shows the boundary conditions legend.
            Defaults to ``False``

        plot_bc_labels : bool, optional
            Shows the boundary conditions label per node.
            Defaults to ``False``.

        bc_labels : List[str], Tuple(str), optional
            List or tuple of strings with the boundary conditions
            to plot, i.e. ``["UX", "UZ"]``.
            You can obtain the allowed boundary conditions by
            evaluating ``ansys.mapdl.core.plotting.BCS``.
            You can use also the following shortcuts:

            * **'mechanical'**
              To plot the following mechanical boundary conditions: ``'UX'``,
              ``'UY'``, ``'UZ'``, ``'FX'``, ``'FY'``, and ``'FZ'``.  Rotational
              or momentum boundary conditions are not allowed.

            * ``'thermal'``
              To plot the following boundary conditions: 'TEMP' and
              'HEAT'.

            * ``'electrical'``
              To plot the following electrical boundary conditions:
              ``'VOLT'``, ``'CHRGS'``, and ``'AMPS'``.

            Defaults to all the allowed boundary conditions present
            in the responses of :func:`ansys.mapdl.core.Mapdl.dlist`
            and :func:`ansys.mapdl.core.Mapdl.flist()`.

        bc_target : List[str], Tuple(str), optional
            Specify the boundary conditions target
            to plot, i.e. "Nodes", "Elements".
            You can obtain the allowed boundary conditions target by
            evaluating ``ansys.mapdl.core.plotting.ALLOWED_TARGETS``.
            Defaults to only ``"Nodes"``.

        bc_glyph_size : float, optional
            Specify the size of the glyph used for the boundary
            conditions plotting.
            By default is ratio of the bounding box dimensions.

        bc_labels_font_size : float, optional
            Size of the text on the boundary conditions labels.
            By default it is 16.

        Examples
        --------
        Plot using VTK while showing labels and changing the background.

        >>> mapdl.prep7()
        >>> mapdl.n(1, 0, 0, 0)
        >>> mapdl.n(11, 10, 0, 0)
        >>> mapdl.fill(1, 11, 9)
        >>> mapdl.nplot(
        ...     nnum=True,
        ...     vtk=True,
        ...     background='w',
        ...     color='k',
        ...     show_bounds=True
        ... )

        Plot without using VTK.

        >>> mapdl.prep7()
        >>> mapdl.n(1, 0, 0, 0)
        >>> mapdl.n(11, 10, 0, 0)
        >>> mapdl.fill(1, 11, 9)
        >>> mapdl.nplot(vtk=False)

        Plot nodal boundary conditions.

        >>> mapdl.nplot(
        ...     plot_bc=True,
        ...     plot_bc_labels=True,
        ...     bc_labels="mechanical",
        ... )

        """
        if vtk is None:
            vtk = self._use_vtk

        if vtk is True:
            if _HAS_PYVISTA:
                # lazy import here to avoid top level import
                import pyvista as pv
            else:  # pragma: no cover
                raise ModuleNotFoundError(
                    f"Using the keyword argument 'vtk' requires having Pyvista installed."
                )

        if "knum" in kwargs:
            raise ValueError("`knum` keyword deprecated.  Please use `nnum` instead.")

        if vtk:
            kwargs.setdefault("title", "MAPDL Node Plot")
            if not self.mesh.n_node:
                warnings.warn("There are no nodes to plot.")
                return general_plotter([], [], [], mapdl=self, **kwargs)

            labels = []
            if nnum:
                # must eliminate duplicate points or labeling fails miserably.
                pcloud = pv.PolyData(self.mesh.nodes)
                pcloud["labels"] = self.mesh.nnum
                pcloud.clean(inplace=True)

                labels = [{"points": pcloud.points, "labels": pcloud["labels"]}]
            points = [{"points": self.mesh.nodes}]
            return general_plotter([], points, labels, mapdl=self, **kwargs)

        # otherwise, use the built-in nplot
        if isinstance(nnum, bool):
            nnum = int(nnum)

        self._enable_interactive_plotting()
        return super().nplot(nnum, **kwargs)

    def eplot(self, show_node_numbering=False, vtk=None, **kwargs):
        """Plots the currently selected elements.

        APDL Command: EPLOT

        .. note::
            PyMAPDL plotting commands with ``vtk=True`` ignore any
            values set with the ``PNUM`` command.

        Parameters
        ----------
        vtk : bool, optional
            Plot the currently selected elements using ``pyvista``.
            Defaults to current ``use_vtk`` setting.

        show_node_numbering : bool, optional
            Plot the node numbers of surface nodes.

        plot_bc : bool, optional
            Activate the plotting of the boundary conditions.
            Defaults to ``False``.

            .. warning:: This is in alpha state.

        plot_bc_legend : bool, optional
            Shows the boundary conditions legend.
            Defaults to ``False``

        plot_bc_labels : bool, optional
            Shows the boundary conditions label per node.
            Defaults to ``False``.

        bc_labels : List[str], Tuple(str), optional
            List or tuple of strings with the boundary conditions
            to plot, i.e. ``["UX", "UZ"]``.
            You can obtain the allowed boundary conditions by
            evaluating ``ansys.mapdl.core.plotting.BCS``.
            You can use also the following shortcuts:

            * **'mechanical'**
              To plot the following mechanical boundary conditions: ``'UX'``,
              ``'UY'``, ``'UZ'``, ``'FX'``, ``'FY'``, and ``'FZ'``.  Rotational
              or momentum boundary conditions are not allowed.

            * ``'thermal'``
              To plot the following boundary conditions: 'TEMP' and
              'HEAT'.

            * ``'electrical'``
              To plot the following electrical boundary conditions:
              ``'VOLT'``, ``'CHRGS'``, and ``'AMPS'``.

            Defaults to all the allowed boundary conditions present
            in the responses of :func:`ansys.mapdl.core.Mapdl.dlist`
            and :func:`ansys.mapdl.core.Mapdl.flist()`.

        bc_target : List[str], Tuple(str), optional
            Specify the boundary conditions target
            to plot, i.e. "Nodes", "Elements".
            You can obtain the allowed boundary conditions target by
            evaluating ``ansys.mapdl.core.plotting.ALLOWED_TARGETS``.
            Defaults to only ``"Nodes"``.

        bc_glyph_size : float, optional
            Specify the size of the glyph used for the boundary
            conditions plotting.
            By default is ratio of the bounding box dimensions.

        bc_labels_font_size : float, optional
            Size of the text on the boundary conditions labels.
            By default it is 16.

        **kwargs
            See ``help(ansys.mapdl.core.plotter.general_plotter)`` for more
            keyword arguments related to visualizing using ``vtk``.

        Examples
        --------
        >>> mapdl.clear()
        >>> mapdl.prep7()
        >>> mapdl.block(0, 1, 0, 1, 0, 1)
        >>> mapdl.et(1, 186)
        >>> mapdl.esize(0.1)
        >>> mapdl.vmesh('ALL')
        >>> mapdl.vgen(2, 'all')
        >>> mapdl.eplot(show_edges=True, smooth_shading=True,
                        show_node_numbering=True)

        Save a screenshot to disk without showing the plot

        >>> mapdl.eplot(background='w', show_edges=True, smooth_shading=True,
                        window_size=[1920, 1080], savefig='screenshot.png',
                        off_screen=True)

        """
        if vtk is None:
            vtk = self._use_vtk
        elif vtk is True:
            if not _HAS_PYVISTA:  # pragma: no cover
                raise ModuleNotFoundError(
                    f"Using the keyword argument 'vtk' requires having Pyvista installed."
                )

        if vtk:
            kwargs.setdefault("title", "MAPDL Element Plot")
            if not self._mesh.n_elem:
                warnings.warn("There are no elements to plot.")
                return general_plotter([], [], [], mapdl=self, **kwargs)

            # TODO: Consider caching the surface
            esurf = self.mesh._grid.linear_copy().extract_surface().clean()
            kwargs.setdefault("show_edges", True)

            # if show_node_numbering:
            labels = []
            if show_node_numbering:
                labels = [{"points": esurf.points, "labels": esurf["ansys_node_num"]}]

            return general_plotter(
                [{"mesh": esurf, "style": kwargs.pop("style", "surface")}],
                [],
                labels,
                mapdl=self,
                **kwargs,
            )

        # otherwise, use MAPDL plotter
        self._enable_interactive_plotting()
        return self.run("EPLOT", **kwargs)

    def vplot(
        self,
        nv1="",
        nv2="",
        ninc="",
        degen="",
        scale="",
        vtk=None,
        quality=4,
        show_area_numbering=False,
        show_line_numbering=False,
        color_areas=False,
        show_lines=True,
        **kwargs,
    ):
        """Plot the selected volumes.

        APDL Command: VPLOT

        .. note::
            PyMAPDL plotting commands with ``vtk=True`` ignore any
            values set with the ``PNUM`` command.

        Parameters
        ----------
        nv1, nv2, ninc
            Display volumes from NV1 to NV2 (defaults to NV1) in steps
            of NINC (defaults to 1).  If NV1 = ALL (default), NV2 and
            NINC are ignored and all selected volumes [VSEL] are
            displayed.  Ignored when ``vtk=True``.

        degen
            Degeneracy marker.  ``"blank"`` No degeneracy marker is
            used (default), or ``"DEGE"``.  A red star is placed on
            keypoints at degeneracies (see the Modeling and Meshing
            Guide).  Not available if /FACET,WIRE is set.  Ignored
            when ``vtk=True``.

        scale
            Scale factor for the size of the degeneracy-marker star.  The scale
            is the size in window space (-1 to 1 in both directions) (defaults
            to .075).  Ignored when ``vtk=True``.

        vtk : bool, optional
            Plot the currently selected volumes using ``pyvista``.  As
            this creates a temporary surface mesh, this may have a
            long execution time for large meshes.

        quality : int, optional
            quality of the mesh to display.  Varies between 1 (worst)
            to 10 (best).  Applicable when ``vtk=True``.

        show_numbering : bool, optional
            Display line and keypoint numbers when ``vtk=True``.

        **kwargs
            See :meth:`ansys.mapdl.core.plotting.general_plotter` for
            more keyword arguments applicable when visualizing with
            ``vtk=True``.

        Examples
        --------
        Plot while displaying area numbers.

        >>> mapdl.vplot(show_area_numbering=True)

        """
        if vtk is None:
            vtk = self._use_vtk
        elif vtk is True:
            if not _HAS_PYVISTA:  # pragma: no cover
                raise ModuleNotFoundError(
                    f"Using the keyword argument 'vtk' requires having Pyvista installed."
                )

        if vtk:
            kwargs.setdefault("title", "MAPDL Volume Plot")
            if not self.geometry.n_volu:
                warnings.warn(
                    "Either no volumes have been selected or there is nothing to plot."
                )
                return general_plotter([], [], [], **kwargs)

            cm_name = "__tmp_area2__"
            self.cm(cm_name, "AREA", mute=True)
            self.aslv("S", mute=True)  # select areas attached to active volumes
            out = self.aplot(
                vtk=vtk,
                color_areas=color_areas,
                quality=quality,
                show_area_numbering=show_area_numbering,
                show_line_numbering=show_line_numbering,
                show_lines=show_lines,
                **kwargs,
            )
            self.cmsel("S", cm_name, "AREA", mute=True)
            return out
        else:
            self._enable_interactive_plotting()
            return super().vplot(
                nv1=nv1, nv2=nv2, ninc=ninc, degen=degen, scale=scale, **kwargs
            )

    def aplot(
        self,
        na1="",
        na2="",
        ninc="",
        degen="",
        scale="",
        vtk=None,
        quality=4,
        show_area_numbering=False,
        show_line_numbering=False,
        color_areas=False,
        show_lines=False,
        **kwargs,
    ):
        """Display the selected areas.

        Displays the selected areas from ``na1`` to ``na2`` in steps
        of ``ninc``.

        APDL Command: ``APLOT``

        .. note::
            PyMAPDL plotting commands with ``vtk=True`` ignore any
            values set with the ``PNUM`` command.

        Parameters
        ----------
        na1 : int, optional
            Minimum area to display.

        na2 : int, optional
            Maximum area to display.

        ninc : int, optional
            Increment between minimum and maximum area.

        degen, str, optional
            Degeneracy marker.  This option is ignored when ``vtk=True``.

        scale : float, optional
            Scale factor for the size of the degeneracy-marker star.
            The scale is the size in window space (-1 to 1 in both
            directions) (defaults to 0.075).  This option is ignored
            when ``vtk=True``.

        vtk : bool, optional
            Plot the currently selected areas using ``pyvista``.  As
            this creates a temporary surface mesh, this may have a
            long execution time for large meshes.

        quality : int, optional
            Quality of the mesh to display.  Varies between 1 (worst)
            to 10 (best) when ``vtk=True``.

        show_area_numbering : bool, optional
            Display area numbers when ``vtk=True``.

        show_line_numbering : bool, optional
            Display line numbers when ``vtk=True``.

        color_areas : np.array, optional
            Only used when ``vtk=True``.
            If ``color_areas`` is a bool, randomly color areas when ``True`` .
            If ``color_areas`` is an array or list, it colors each area with
            the RGB colors, specified in that array or list.

        show_lines : bool, optional
            Plot lines and areas.  Change the thickness of the lines
            with ``line_width=``

        **kwargs
            See :meth:`ansys.mapdl.core.plotting.general_plotter` for
            more keyword arguments applicable when visualizing with
            ``vtk=True``.

        Examples
        --------
        Plot areas between 1 and 4 in increments of 2.

        >>> mapdl.block(0, 1, 0, 1, 0, 1)
        >>> mapdl.aplot(1, 4, 2)

        Plot all areas and randomly color the areas.  Label center of
        areas by their number.

        >>> mapdl.aplot(show_area_numbering=True, color_areas=True)

        Return the plotting instance and modify it.

        >>> mapdl.aplot()
        >>> pl = mapdl.aplot(return_plotter=True)
        >>> pl.show_bounds()
        >>> pl.set_background('black')
        >>> pl.add_text('my text')
        >>> pl.show()

        """
        if vtk is None:
            vtk = self._use_vtk
        elif vtk is True:
            if not _HAS_PYVISTA:  # pragma: no cover
                raise ModuleNotFoundError(
                    f"Using the keyword argument 'vtk' requires having Pyvista installed."
                )

        if vtk:
            kwargs.setdefault("show_scalar_bar", False)
            kwargs.setdefault("title", "MAPDL Area Plot")
            kwargs.setdefault("scalar_bar_args", {"title": "Scalar Bar Title"})

            if not self.geometry.n_area:
                warnings.warn(
                    "Either no areas have been selected or there is nothing to plot."
                )
                return general_plotter([], [], [], **kwargs)

            if quality > 10:
                quality = 10
            if quality < 1:
                quality = 1
            surf = self.geometry.generate_surface(11 - quality, na1, na2, ninc)
            meshes = []
            labels = []

            # individual surface isolation is quite slow, so just
            # color individual areas
            if color_areas:  # pragma: no cover
                if isinstance(color_areas, bool):
                    anum = surf["entity_num"]
                    size_ = max(anum) + 1
                    # Because this is only going to be used for plotting purpuses, we don't need to allocate
                    # a huge vector with random numbers (colours).
                    # By default `pyvista.DataSetMapper.set_scalars` `n_colors` argument is set to 256, so let
                    # do here the same.
                    # We will limit the number of randoms values (colours) to 256
                    #
                    # Link: https://docs.pyvista.org/api/plotting/_autosummary/pyvista.DataSetMapper.set_scalars.html#pyvista.DataSetMapper.set_scalars
                    size_ = min([256, size_])
                    # Generating a colour array,
                    # Size = number of areas.
                    # Values are random between 0 and min(256, number_areas)
                    area_color = np.random.choice(range(size_), size=(len(anum), 3))
                else:
                    if len(surf["entity_num"]) != len(color_areas):
                        raise ValueError(
                            f"The length of the parameter array 'color_areas' should be the same as the number of areas."
                        )
                    area_color = color_areas
                meshes.append({"mesh": surf, "scalars": area_color})
            else:
                meshes.append({"mesh": surf, "color": kwargs.get("color", "white")})

            if show_area_numbering:
                anums = np.unique(surf["entity_num"])
                centers = []
                for anum in anums:
                    area = surf.extract_cells(surf["entity_num"] == anum)
                    centers.append(area.center)

                labels.append({"points": np.array(centers), "labels": anums})

            if show_lines or show_line_numbering:
                kwargs.setdefault("line_width", 2)
                # subselect lines belonging to the current areas
                self.cm("__area__", "AREA", mute=True)
                self.lsla("S", mute=True)

                lines = self.geometry.lines
                self.cmsel("S", "__area__", "AREA", mute=True)

                if show_lines:
                    meshes.append(
                        {"mesh": lines, "color": kwargs.get("edge_color", "k")}
                    )
                if show_line_numbering:
                    labels.append(
                        {
                            "points": lines.points[50::101],
                            "labels": lines["entity_num"],
                        }
                    )

            return general_plotter(meshes, [], labels, **kwargs)

        self._enable_interactive_plotting()
        return super().aplot(
            na1=na1, na2=na2, ninc=ninc, degen=degen, scale=scale, **kwargs
        )

    @supress_logging
    def _enable_interactive_plotting(self, pixel_res=1600):
        """Enables interactive plotting.  Requires matplotlib

        Parameters
        ----------
        pixel_res : int
            Pixel resolution.  Valid values are from 256 to 2400.
            Lowering the pixel resolution produces a "fuzzier" image.
            Increasing the resolution produces a "sharper" image but
            takes longer to render.
        """
        if not self._has_matplotlib:
            raise ImportError(
                "Install matplotlib to display plots from MAPDL ,"
                "from Python.  Otherwise, plot with vtk with:\n"
                "``vtk=True``"
            )

        if not self._png_mode:
            self.show("PNG", mute=True)
            self.gfile(pixel_res, mute=True)

    @property
    def _has_matplotlib(self):
        try:
            import matplotlib  # noqa: F401

            return True
        except ImportError:
            return False

    @property
    def _png_mode(self):
        """Returns True when MAPDL is set to write plots as png to file."""
        return "PNG" in self.show(mute=False)

    def set_log_level(self, loglevel):
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
            loglevel = loglevel.upper()
        setup_logger(loglevel=loglevel)

    def _list(self, command):
        """Replaces *LIST command"""
        items = command.split(",")
        filename = os.path.join(self.directory, ".".join(items[1:]))
        if os.path.isfile(filename):
            self._response = open(filename).read()
            self._log.info(self._response)
        else:
            raise Exception("Cannot run:\n{command}\n\nFile does not exist")

    def lplot(
        self,
        nl1="",
        nl2="",
        ninc="",
        vtk=None,
        show_line_numbering=True,
        show_keypoint_numbering=False,
        color_lines=False,
        **kwargs,
    ):
        """Display the selected lines.

        APDL Command: LPLOT

        .. note::
            PyMAPDL plotting commands with ``vtk=True`` ignore any
            values set with the ``PNUM`` command.

        Parameters
        ----------
        nl1, nl2, ninc
            Display lines from NL1 to NL2 (defaults to NL1) in steps
            of NINC (defaults to 1).  If NL1 = ALL (default), NL2 and
            NINC are ignored and display all selected lines [LSEL].

        vtk : bool, optional
            Plot the currently selected lines using ``pyvista``.

        show_line_numbering : bool, optional
            Display line and keypoint numbers when ``vtk=True``.

        show_keypoint_numbering : bool, optional
            Number keypoints.  Only valid when ``show_keypoints=True``

        **kwargs
            See :meth:`ansys.mapdl.core.plotting.general_plotter` for
            more keyword arguments applicable when visualizing with
            ``vtk=True``.

        Notes
        -----
        Mesh divisions on plotted lines are controlled by the ``ldiv``
        option of the ``psymb`` command when ``vtk=False``.
        Otherwise, line divisions are controlled automatically.

        This command is valid in any processor.

        Examples
        --------
        >>> mapdl.lplot(vtk=True, cpos='xy', line_width=10)
        """
        if vtk is None:
            vtk = self._use_vtk
        elif vtk is True:
            if not _HAS_PYVISTA:  # pragma: no cover
                raise ModuleNotFoundError(
                    f"Using the keyword argument 'vtk' requires having Pyvista installed."
                )

        if vtk:
            kwargs.setdefault("show_scalar_bar", False)
            kwargs.setdefault("title", "MAPDL Line Plot")
            if not self.geometry.n_line:
                warnings.warn(
                    "Either no lines have been selected or there is nothing to plot."
                )
                return general_plotter([], [], [], **kwargs)

            lines = self.geometry.lines
            meshes = [{"mesh": lines}]
            if color_lines:
                meshes[0]["scalars"] = np.random.random(lines.n_cells)

            labels = []
            if show_line_numbering:
                labels.append(
                    {
                        "points": lines.points[50::101],
                        "labels": lines["entity_num"],
                    }
                )

            if show_keypoint_numbering:
                labels.append(
                    {
                        "points": self.geometry.keypoints,
                        "labels": self.geometry.knum,
                    }
                )

            return general_plotter(meshes, [], labels, **kwargs)
        else:
            self._enable_interactive_plotting()
            return super().lplot(nl1=nl1, nl2=nl2, ninc=ninc, **kwargs)

    def kplot(
        self,
        np1="",
        np2="",
        ninc="",
        lab="",
        vtk=None,
        show_keypoint_numbering=True,
        **kwargs,
    ):
        """Display the selected keypoints.

        APDL Command: KPLOT

        .. note::
            PyMAPDL plotting commands with ``vtk=True`` ignore any
            values set with the ``PNUM`` command.

        Parameters
        ----------
        np1, np2, ninc
            Display keypoints from NP1 to NP2 (defaults to NP1) in
            steps of NINC (defaults to 1).  If NP1 = ALL (default),
            NP2 and NINC are ignored and all selected keypoints [KSEL]
            are displayed.

        lab
            Determines what keypoints are plotted (one of the following):

            (blank) - Plots all keypoints.

            HPT - Plots only those keypoints that are hard points.

        vtk : bool, optional
            Plot the currently selected lines using ``pyvista``.

        show_keypoint_numbering : bool, optional
            Display keypoint numbers when ``vtk=True``.



        Notes
        -----
        This command is valid in any processor.
        """
        if vtk is None:
            vtk = self._use_vtk
        elif vtk is True:
            if not _HAS_PYVISTA:  # pragma: no cover
                raise ModuleNotFoundError(
                    f"Using the keyword argument 'vtk' requires having Pyvista installed."
                )

        if vtk:
            kwargs.setdefault("title", "MAPDL Keypoint Plot")
            if not self.geometry.n_keypoint:
                warnings.warn(
                    "Either no keypoints have been "
                    "selected or there are no keypoints in "
                    "the database."
                )
                return general_plotter([], [], [], **kwargs)

            keypoints = self.geometry.keypoints
            points = [{"points": keypoints}]

            labels = []
            if show_keypoint_numbering:
                labels.append({"points": keypoints, "labels": self.geometry.knum})

            return general_plotter([], points, labels, **kwargs)

        # otherwise, use the legacy plotter
        self._enable_interactive_plotting()
        return super().kplot(np1=np1, np2=np2, ninc=ninc, lab=lab, **kwargs)

    @property
    @requires_package("ansys.mapdl.reader", softerror=True)
    def result(self):
        """Binary interface to the result file using :class:`ansys.mapdl.reader.rst.Result`.

        Returns
        -------
        :class:`ansys.mapdl.reader.rst.Result`.
            Result reader class.  See `Legacy PyMAPDL Reader <https://readerdocs.pyansys.com/>`.

        Examples
        --------
        >>> mapdl.solve()
        >>> mapdl.finish()
        >>> result = mapdl.result
        >>> print(result)
        PyMAPDL-Reader Result file object
        Units       : User Defined
        Version     : 18.2
        Cyclic      : False
        Result Sets : 1
        Nodes       : 3083
        Elements    : 977
        ...
        Available Results:
        EMS : Miscellaneous summable items (normally includes face pressures)
        ENF : Nodal forces
        ENS : Nodal stresses
        ENG : Element energies and volume
        EEL : Nodal elastic strains
        ETH : Nodal thermal strains (includes swelling strains)
        EUL : Element euler angles
        EMN : Miscellaneous nonsummable items
        EPT : Nodal temperatures
        NSL : Nodal displacements
        RF  : Nodal reaction forces
        """
        from ansys.mapdl.reader import read_binary
        from ansys.mapdl.reader.rst import Result

        if not self._local:
            # download to temporary directory
            save_path = os.path.join(tempfile.gettempdir())
            result_path = self.download_result(save_path)
        else:
            if self._distributed_result_file and self._result_file:
                result_path = self._distributed_result_file
                result = Result(result_path, read_mesh=False)
                if result._is_cyclic:
                    result_path = self._result_file
                else:  # pragma: no cover
                    # return the file with the last access time
                    filenames = [
                        self._distributed_result_file,
                        self._result_file,
                    ]
                    result_path = last_created(filenames)
                    if result_path is None:  # if same return result_file
                        result_path = self._result_file

            elif self._distributed_result_file:
                result_path = self._distributed_result_file
                result = Result(result_path, read_mesh=False)
                if result._is_cyclic:
                    if not os.path.isfile(self._result_file):
                        raise MapdlRuntimeError(
                            "Distributed Cyclic result not supported"
                        )
                    result_path = self._result_file
            else:
                result_path = self._result_file

        if result_path is None:
            raise FileNotFoundError("No result file(s) at %s" % self.directory)
        if not os.path.isfile(result_path):
            raise FileNotFoundError("No results found at %s" % result_path)

        return read_binary(result_path)

    @property
    def result_file(self):
        """Return the RST file path."""
        return self._result_file

    @property
    def _result_file(self):
        """Path of the non-distributed result file"""
        try:
            with self.run_as_routine("POST1"):
                filename = self.inquire("", "RSTFILE")
        except Exception:  # pragma: no cover
            filename = self.jobname

        try:
            with self.run_as_routine("POST1"):
                ext = self.inquire("", "RSTEXT")
        except Exception:  # pragma: no cover
            ext = "rst"

        if self._local:  # pragma: no cover
            if ext == "":
                # Case where there is RST extension because it is thermal for example
                filename = self.jobname

                rth_file = os.path.join(self.directory, f"{filename}.rth")
                rst_file = os.path.join(self.directory, f"{filename}.rst")

                if self._prioritize_thermal and os.path.isfile(rth_file):
                    return rth_file

                if os.path.isfile(rth_file) and os.path.isfile(rst_file):
                    return last_created([rth_file, rst_file])
                elif os.path.isfile(rth_file):
                    return rth_file
                elif os.path.isfile(rst_file):
                    return rst_file
            else:
                filename = os.path.join(self.directory, f"{filename}.{ext}")
                if os.path.isfile(filename):
                    return filename
        else:
            return f"{filename}.{ext}"

    @property
    def _distributed_result_file(self):
        """Path of the distributed result file"""
        try:
            filename = self.inquire("", "RSTFILE")
            if not filename:
                filename = self.jobname
        except Exception:
            filename = self.jobname

        # ansys decided that a jobname ended in a number needs a bonus "_"
        if filename[-1].isnumeric():
            filename += "_"

        rth_basename = "%s0.%s" % (filename, "rth")
        rst_basename = "%s0.%s" % (filename, "rst")

        rth_file = os.path.join(self.directory, rth_basename)
        rst_file = os.path.join(self.directory, rst_basename)
        if os.path.isfile(rth_file) and os.path.isfile(rst_file):
            return last_created([rth_file, rst_file])
        elif os.path.isfile(rth_file):
            return rth_file
        elif os.path.isfile(rst_file):
            return rst_file

    def _get(self, *args, **kwargs):
        """Simply use the default get method"""
        return self.get(*args, **kwargs)

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

    def _flush_stored(self):  # pragma: no cover
        """Writes stored commands to an input file and runs the input file.

        Used with ``non_interactive``.

        Overridden by gRPC.

        """
        self._log.debug("Flushing stored commands")
        rnd_str = random_string()
        tmp_out = os.path.join(tempfile.gettempdir(), f"tmp_{rnd_str}.out")
        self._stored_commands.insert(0, "/OUTPUT, f'{tmp_out}'")
        self._stored_commands.append("/OUTPUT")
        commands = "\n".join(self._stored_commands)
        if self._apdl_log:
            self._apdl_log.write(commands + "\n")

        # write to a temporary input file
        tmp_inp = os.path.join(tempfile.gettempdir(), f"tmp_{rnd_str}.inp")
        self._log.debug(
            "Writing the following commands to a temporary " "apdl input file:\n%s",
            commands,
        )

        with open(tmp_inp, "w") as f:
            f.writelines(commands)

        self._store_commands = False
        self._stored_commands = []

        # interactive result
        _ = self.input(tmp_inp, write_to_log=False)
        time.sleep(0.1)  # allow MAPDL to close the file
        if os.path.isfile(tmp_out):
            self._response = "\n" + open(tmp_out).read()

        if self._response is None:
            self._log.warning("Unable to read response from flushed commands")
        else:
            self._log.info(self._response)

    def get_value(
        self,
        entity="",
        entnum="",
        item1="",
        it1num="",
        item2="",
        it2num="",
        item3="",
        it3num="",
        item4="",
        it4num="",
        **kwargs,
    ):
        """Runs the MAPDL GET command and returns a Python value.

        This method uses :func:`Mapdl.get`.

        See the full MADPL command documentation at `*GET
        <https://www.mm.bme.hu/~gyebro/files/ans_help_v182/ans_cmd/Hlp_C_GET.html>`_

        .. note::
           This method is not available when within the
           :func:`Mapdl.non_interactive`
           context manager.

        Parameters
        ----------
        entity : str
            Entity keyword. Valid keywords are ``"NODE"``, ``"ELEM"``,
            ``"KP"``, ``"LINE"``, ``"AREA"``, ``"VOLU"``, ``"PDS"``,
            etc.

        entnum : str, int, optional
            The number or label for the entity. In some cases, a zero
            (or blank ``""``) ``entnum`` represents all entities of
            the set.

        item1 : str, optional
            The name of a particular item for the given entity.

        it1num : str, int, optional
            The number (or label) for the specified Item1 (if
            any). Some Item1 labels do not require an IT1NUM value.

        item2 : str, optional
            A second set of item labels and numbers to further qualify the item
            for which data are to be retrieved. Most items do not require this
            level of information.

        it2num : str, int, optional
            The number (or label) for the specified ``item2`` (if
            any). Some ``item2`` labels do not require an ``it2num``
            value.

        item3 : str, optional
            A third set of item labels and numbers to further qualify the item
            for which data are to be retrieved. Most items do not require this
            level of information.

        it3num : str, int, optional
            The number (or label) for the specified ``item3`` (if
            any). Some ``item3`` labels do not require an ``it3num``
            value.

        item4 : str, optional
            A fourth set of item labels and numbers to further qualify the item
            for which data are to be retrieved. Most items do not require this level of information.

        it4num : str, int, optional
            The number (or label) for the specified ``item4`` (if
            any). Some ``item4`` labels do not require an ``it4num``
            value.

        Returns
        -------
        float
            Floating point value of the parameter.

        Examples
        --------
        Retrieve the number of nodes.

        >>> value = ansys.get_value('node', '', 'count')
        >>> value
        3003

        Retrieve the number of nodes using keywords.

        >>> value = ansys.get_value(entity='node', item1='count')
        >>> value
        3003
        """
        return self._get(
            entity=entity,
            entnum=entnum,
            item1=item1,
            it1num=it1num,
            item2=item2,
            it2num=it2num,
            item3=item3,
            it3num=it3num,
            item4=item4,
            it4num=it4num,
            **kwargs,
        )

    def get(
        self,
        par="__floatparameter__",
        entity="",
        entnum="",
        item1="",
        it1num="",
        item2="",
        it2num="",
        item3="",
        it3num="",
        item4="",
        it4num="",
        **kwargs,
    ):
        """Retrieves a value and stores it as a scalar parameter or part of an array parameter.

        APDL Command: ``*GET``

        See the full MADPL command at `*GET
        <https://www.mm.bme.hu/~gyebro/files/ans_help_v182/ans_cmd/Hlp_C_GET.html>`_

        GET retrieves a value for a specified item and stores the
        value as a scalar parameter, or as a value in a user-named
        array parameter. An item is identified by various keyword,
        label, and number combinations.  Usage is similar to the SET
        command except that the parameter values are retrieved from
        previously input or calculated results. For example,
        ``GET,A,ELEM,5,CENT,X`` returns the centroid x-location of element
        5 and stores the result as parameter A. GET command
        operations, along with the associated Get functions return
        values in the active coordinate system unless stated
        otherwise. A Get function is an alternative in- line function
        that can be used to retrieve a value instead of the GET
        command (see Using In-line Get Functions for more
        information).

        Both GET and VGET retrieve information from the active data
        stored in memory. The database is often the source, and
        sometimes the information is retrieved from common memory
        blocks that the program uses to manipulate
        information. Although POST1 and POST26 operations use a .rst
        file, GET data is accessed from the database or from the
        common blocks. Get operations do not access the .rst file
        directly. For repeated gets of sequential items, such as from
        a series of elements, see the VGET command.

        Most items are stored in the database after they are
        calculated and are available anytime thereafter. Items are
        grouped according to where they are usually first defined or
        calculated. Preprocessing data will often not reflect the
        calculated values generated from section data. Do not use GET
        to obtain data from elements that use calculated section data,
        such as beams or shells. Most of the general items listed
        below are available from all modules.

        Parameters
        ----------
        par : str, optional
            The name of the resulting parameter. See \*SET for name
            restrictions.

        entity
            Entity keyword. Valid keywords are NODE, ELEM, KP, LINE,
            AREA, VOLU, PDS, etc., as shown for Entity = in the tables
            below.

        entnum
            The number or label for the entity (as shown for ENTNUM =
            in the tables below). In some cases, a zero (or blank)
            ENTNUM represents all entities of the set.

        item1
            The name of a particular item for the given entity.

        it1num
            The number (or label) for the specified Item1 (if
            any). Valid IT1NUM values are as shown in the IT1NUM
            columns of the tables below. Some Item1 labels do not
            require an IT1NUM value.

        item2, it2num
            A second set of item labels and numbers to further qualify
            the item for which data are to be retrieved. Most items do
            not require this level of information.

        item3
            A third set of item labels to further qualify
            the item for which data are to be retrieved. Almost all items do
            not require this level of information.

        item3 : str, optional
            A third set of item labels and numbers to further qualify the item
            for which data are to be retrieved. Most items do not require this
            level of information.

        it3num : str, int, optional
            The number (or label) for the specified ``item3`` (if
            any). Some ``item3`` labels do not require an ``it3num``
            value.

        item4 : str, optional
            A fourth set of item labels and numbers to further qualify the item
            for which data are to be retrieved. Most items do not require this level of information.

        it4num : str, int, optional
            The number (or label) for the specified ``item4`` (if
            any). Some ``item4`` labels do not require an ``it4num``
            value.

        Returns
        -------
        float
            Floating point value of the parameter.

        Examples
        --------
        Retrieve the number of nodes

        >>> value = mapdl.get('val', 'node', '', 'count')
        >>> value
        3003

        Retrieve the number of nodes using keywords.  Note that the
        parameter name is optional.

        >>> value = mapdl.get(entity='node', item1='count')
        >>> value
        3003

        """

        self._check_parameter_name(par)

        command = f"*GET,{par},{entity},{entnum},{item1},{it1num},{item2},{it2num},{item3},{it3num},{item4},{it4num}"
        kwargs["mute"] = False

        # Checking printout is not suppressed by checking "wrinqr" flag.
        with self.force_output:
            response = self.run(command, **kwargs)

        value = response.split("=")[-1].strip()
        if item3:
            self._log.info(
                f"The command '{command}' is showing the next message: '{value.splitlines()[1].strip()}'"
            )
            value = value.splitlines()[0]

        try:  # always either a float or string
            return float(value)
        except ValueError:
            return value

    @property
    def jobname(self) -> str:
        """
        MAPDL job name.

        This is requested from the active mapdl instance.
        """
        try:
            self._jobname = self.inquire("", "JOBNAME")
        except Exception:
            pass
        return self._jobname

    @jobname.setter
    def jobname(self, new_jobname: str):
        """Set the jobname"""
        self.finish(mute=True)
        self.filname(new_jobname, mute=True)
        self._jobname = new_jobname

    def modal_analysis(
        self,
        method="lanb",
        nmode="",
        freqb="",
        freqe="",
        cpxmod="",
        nrmkey="",
        modtype="",
        memory_option="",
        mxpand="",
        elcalc=False,
    ) -> str:
        """Run a modal with basic settings analysis

        Parameters
        ----------
        method : str
            Mode-extraction method to be used for the modal analysis.
            Defaults to lanb (block lanczos).  Must be one of the following:

            - LANB : Block Lanczos
            - LANPCG : PCG Lanczos
            - SNODE : Supernode modal solver
            - SUBSP : Subspace algorithm
            - UNSYM : Unsymmetric matrix
            - DAMP : Damped system
            - QRDAMP : Damped system using QR algorithm
            - VT : Variational Technology

        nmode : int, optional
            The number of modes to extract. The value can depend on
            the value supplied for Method. NMODE has no default and
            must be specified. If Method = LANB, LANPCG, or SNODE, the
            number of modes that can be extracted can equal the DOFs
            in the model after the application of all boundary
            conditions.

        freqb : float, optional
            The beginning, or lower end, of the frequency range of
            interest.

        freqe : float, optional
            The ending, or upper end, of the frequency range of
            interest (in Hz). The default for Method = SNODE is
            described below. The default for all other methods is to
            calculate all modes, regardless of their maximum
            frequency.

        cpxmod : str, optional
            Complex eigenmode key. Valid only when ``method='QRDAMP'``
            or ``method='unsym'``

            - AUTO : Determine automatically if the eigensolutions are
              real or complex and output them accordingly. This is
              the default for ``method='UNSYM'``.  Not supported for
              Method = QRDAMP.
            - ON or CPLX : Calculate and output complex eigenmode
              shapes.
            - OFF or REAL : Do not calculate complex eigenmode
              shapes. This is required if a mode-
              superposition analysis is intended after the
              modal analysis for Method = QRDAMP. This is the
              default for this method.

        nrmkey : bool, optional
            Mode shape normalization key.  When ``True`` (default),
            normalize the mode shapes to the mass matrix.  When False,
            Normalize the mode shapes to unity instead of to the mass
            matrix.  If a subsequent spectrum or mode-superposition
            analysis is planned, the mode shapes should be normalized
            to the mass matrix.

        modtype : str, optional
            Type of modes calculated by the eigensolver. Only
            applicable to the unsymmetric eigensolver.

            - Blank : Right eigenmodes. This value is the default.
            - BOTH : Right and left eigenmodes. The left eigenmodes are
              written to Jobname.LMODE.  This option must be
              activated if a mode-superposition analysis is intended.

        memory_option : str, optional
            Memory allocation option:

            * ``DEFAULT`` - Default Memory mode
                      Use the default memory allocation strategy for
                      the sparse solver. The default strategy attempts
                      to run in the INCORE memory mode. If there is
                      not enough available physical memory when the
                      solver starts to run in the ``INCORE`` memory
                      mode, the solver will then attempt to run in the
                      ``OUTOFCORE`` memory mode.

            * ``INCORE`` - In-core memory mode
                     Use a memory allocation strategy in the sparse
                     solver that will attempt to obtain enough memory
                     to run with the entire factorized matrix in
                     memory. This option uses the most amount of
                     memory and should avoid doing any I/O. By
                     avoiding I/O, this option achieves optimal solver
                     performance. However, a significant amount of
                     memory is required to run in this mode, and it is
                     only recommended on machines with a large amount
                     of memory. If the allocation for in-core memory
                     fails, the solver will automatically revert to
                     out-of-core memory mode.

            * ``OUTOFCORE`` - Out of core memory mode.
                        Use a memory allocation strategy in the sparse
                        solver that will attempt to allocate only
                        enough work space to factor each individual
                        frontal matrix in memory, but will store the
                        entire factorized matrix on disk. Typically,
                        this memory mode results in poor performance
                        due to the potential bottleneck caused by the
                        I/O to the various files written by the
                        solver.

        mxpand : bool, optional
            Number of modes or array name (enclosed in percent signs)
            to expand and write.  If -1, do not expand and do not
            write modes to the results file during the
            analysis. Default ``""``.
        elcalc : bool, optional
            Calculate element results, reaction forces, energies, and
            the nodal degree of freedom solution.  Default ``False``.

        Returns
        -------
        str
            Output from MAPDL SOLVE command.

        Notes
        -----
        For models that involve a non-symmetric element stiffness
        matrix, as in the case of a contact element with frictional
        contact, the QRDAMP eigensolver (MODOPT, QRDAMP) extracts
        modes in the modal subspace formed by the eigenmodes from the
        symmetrized eigenproblem. The QRDAMP eigensolver symmetrizes
        the element stiffness matrix on the first pass of the
        eigensolution, and in the second pass, eigenmodes are
        extracted in the modal subspace of the first eigensolution
        pass. For such non- symmetric eigenproblems, you should verify
        the eigenvalue and eigenmode results using the non-symmetric
        matrix eigensolver (MODOPT,UNSYM).

        The DAMP and QRDAMP options cannot be followed by a subsequent
        spectrum analysis. The UNSYM method supports spectrum analysis
        when eigensolutions are real.

        Examples
        --------
        Modal analysis using default parameters for the first 6 modes

        >>> mapdl.modal_analysis(nmode=6)

        """
        if nrmkey:
            if nrmkey.upper() != "OFF":
                nrmkey = "ON"
        nrmkey = "OFF"

        self.slashsolu(mute=True)
        self.antype(2, "new", mute=True)
        self.modopt(method, nmode, freqb, freqe, cpxmod, nrmkey, modtype, mute=True)
        self.bcsoption(memory_option, mute=True)

        if mxpand:
            self.mxpand(mute=True)
        if elcalc:
            self.mxpand(elcalc="YES", mute=True)

        out = self.solve()
        self.finish(mute=True)
        return out

    def run_multiline(self, commands) -> str:
        """Run several commands as a single block

        .. deprecated:: 0.61.0
           This function is being deprecated. Please use `input_strings`
           instead.

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

        warnings.warn(
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

    def run(self, command, write_to_log=True, mute=None, **kwargs) -> str:
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
        if mute is None:
            if hasattr(self, "mute"):
                mute = self.mute
            else:  # if not gRPC
                mute = False

        # check if multiline
        if "\n" in command or "\r" in command:
            raise ValueError("Use ``input_strings`` for multi-line commands")

        # check if we want to avoid the current non-interactive context.
        avoid_non_interactive = kwargs.pop("avoid_non_interactive", False)

        if self._store_commands and not avoid_non_interactive:
            # If we are using NBLOCK on input, we should not strip the string
            self._stored_commands.append(command)
            return

        command = command.strip()

        # always reset the cache
        self._reset_cache()

        # address MAPDL /INPUT level issue
        if command[:4].upper() == "/CLE":
            # Address gRPC issue
            # https://github.com/pyansys/pymapdl/issues/380
            command = "/CLE,NOSTART"

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

        if "=" in command:
            # We are storing a parameter.
            param_name = command.split("=")[0].strip()

            if "/COM" not in cmd_ and "/TITLE" not in cmd_:
                # Edge case. `\title, 'par=1234' `
                self._check_parameter_name(param_name)

        verbose = kwargs.get("verbose", False)
        text = self._run(command, verbose=verbose, mute=mute)

        if mute:
            return

        text = text.replace("\\r\\n", "\n").replace("\\n", "\n")
        if text:
            self._response = StringWithLiteralRepr(text.strip())
            self._log.info(self._response)
        else:
            self._response = None
            return self._response

        if not self.ignore_errors:
            self._raise_errors(text)

        # special returns for certain geometry commands
        short_cmd = parse_to_short_cmd(command)

        if short_cmd in PLOT_COMMANDS:
            return self._display_plot(self._response)

        return self._response

    @property
    def ignore_errors(self) -> bool:
        """Invalid commands will be ignored rather than exceptions

        Normally, any string containing "*** ERROR ***" from MAPDL
        will trigger a ``MapdlRuntimeError``.  Set this to ``True`` to
        ignore these errors.

        For example, a command executed in the wrong processor will
        raise an exception when ``ignore_errors=False``.
        This is the default behavior.

        Examples
        --------
        >>> mapdl.post1()
        >>> mapdl.k(1, 0, 0, 0)
        Exception:  K is not a recognized POST1 command, abbreviation, or macro.

        Ignore these messages by setting ignore_errors=True

        >>> mapdl.ignore_errors = True
        2020-06-08 21:39:58,094 [INFO] : K is not a
        recognized POST1 command, abbreviation, or macro.  This
        command will be ignored.

        *** WARNING *** CP = 0.372 TIME= 21:39:58
        K is not a recognized POST1 command, abbreviation, or macro.
        This command will be ignored.

        """
        return self._ignore_errors

    @ignore_errors.setter
    def ignore_errors(self, value):
        self._ignore_errors = bool(value)

    def load_array(self, name, array):
        """
        Load an array from Python to MAPDL.

        Uses ``VREAD`` to transfer the array.
        The format of the numbers used in the intermediate file is F24.18.

        Parameters
        ----------
        name : str
            An alphanumeric name used to identify this table.  Name
            may be up to 32 characters, beginning with a letter and
            containing only letters, numbers, and underscores.
            Examples: ``"ABC" "A3X" "TOP_END"``.

        array : np.ndarray or list
            List as a table or ``numpy`` array.

        Examples
        --------
        >>> my_conv = np.array([[0, 0.001],
        ...                     [120, 0.001],
        ...                     [130, 0.005],
        ...                     [700, 0.005],
        ...                     [710, 0.002],
        ...                     [1000, 0.002]])
        >>> mapdl.load_array('MY_ARRAY', my_conv)
        >>> mapdl.parameters['MY_ARRAY']
        array([[0.0e+00, 1.0e-03],
                [1.2e+02, 1.0e-03],
                [1.3e+02, 5.0e-03],
                [7.0e+02, 5.0e-03],
                [7.1e+02, 2.0e-03],
                [1.0e+03, 2.0e-03]])
        """
        if not isinstance(array, np.ndarray):
            array = np.asarray(array)

        if array.ndim > 2:
            raise NotImplementedError(
                "Only loading of 1D or 2D arrays is supported at the moment."
            )

        jmax = 1
        kmax = ""

        if array.ndim > 0:
            imax = array.shape[0]

        if array.ndim > 1:
            jmax = array.shape[1]

        self.dim(name, "ARRAY", imax=imax, jmax=jmax, kmax="")

        base_name = random_string() + ".txt"
        filename = os.path.join(tempfile.gettempdir(), base_name)
        self._log.info(f"Generating file for table in {filename}")
        np.savetxt(
            filename,
            array,
            delimiter=",",
            header="File generated by PyMAPDL:load_array",
            fmt="%24.18e",
        )

        if not self._local:
            self.upload(filename, progress_bar=False)
            filename = base_name

        with self.non_interactive:
            label = "jik"
            n1 = jmax
            n2 = imax
            n3 = kmax
            self.vread(name, filename, n1=n1, n2=n2, n3=n3, label=label, nskip=1)
            fmt = "(" + ",',',".join(["E24.18" for i in range(jmax)]) + ")"
            logger.info("Using *VREAD with format %s in %s", fmt, filename)
            self.run(fmt)

        if self._local:
            os.remove(filename)
        else:
            self.slashdelete(filename)

    def load_table(self, name, array, var1="", var2="", var3="", csysid=""):
        """Load a table from Python to into MAPDL.

        Uses :func:`tread <Mapdl.tread>` to transfer the table.

        Parameters
        ----------
        name : str
            An alphanumeric name used to identify this table.  Name
            may be up to 32 characters, beginning with a letter and
            containing only letters, numbers, and underscores.
            Examples: ``"ABC" "A3X" "TOP_END"``.

        array : numpy.ndarray or List
            List as a table or :class:`numpy.ndarray` array.

        var1 : str, optional
            Variable name corresponding to the first dimension (row).
            Default ``"Row"``.

            A primary variable (listed below) or can be an independent
            parameter. If specifying an independent parameter, then you must
            define an additional table for the independent parameter. The
            additional table must have the same name as the independent
            parameter and may be a function of one or more primary variables or
            another independent parameter. All independent parameters must
            relate to a primary variable.

            - ``"TIME"``: Time
            - ``"FREQ"``: Frequency
            - ``"X"``: X-coordinate location
            - ``"Y"``: Y-coordinate location
            - ``"Z"``: Z-coordinate location
            - ``"TEMP"``: Temperature
            - ``"VELOCITY"``: Velocity
            - ``"PRESSURE"``: Pressure
            - ``"GAP"``: Geometric gap/penetration
            - ``"SECTOR"``: Cyclic sector number
            - ``"OMEGS"``: Amplitude of the rotational velocity vector
            - ``"ECCENT"``: Eccentricity
            - ``"THETA"``: Phase shift
            - ``"ELEM"``: Element number
            - ``"NODE"``: Node number
            - ``"CONC"``: Concentration

        var2 : str, optional
            Variable name corresponding to the first dimension (column).
            See ``var1``.  Default column.

        var3 : str, optional
            Variable name corresponding to the first dimension (plane).
            See ``var1``. Default Plane.

        csysid : str, optional
            An integer corresponding to the coordinate system ID number.
            APDL Default = 0 (global Cartesian)

        Examples
        --------
        Transfer a table to MAPDL. The first column is time values and must be
        ascending in order.

        >>> my_conv = np.array([[0, 0.001],
                                [120, 0.001],
                                [130, 0.005],
                                [700, 0.005],
                                [710, 0.002],
                                [1000, 0.002]])
        >>> mapdl.load_table('MY_TABLE', my_conv, 'TIME')
        >>> mapdl.parameters['MY_TABLE']
        array([[0.001],
               [0.001],
               [0.005],
               [0.005],
               [0.002],
               [0.002]])
        """
        if not isinstance(array, np.ndarray):
            raise ValueError("The table should be a Numpy array")
        if array.shape[0] < 2 or array.shape[1] < 2:
            raise ValueError(
                "One or two of the array dimensions are too small to create a table."
            )

        if array.ndim == 2:
            self.dim(
                name,
                "TABLE",
                imax=array.shape[0],
                jmax=array.shape[1] - 1,
                kmax="",
                var1=var1,
                var2=var2,
                var3=var3,
                csysid=csysid,
            )
        else:
            raise ValueError(
                f"Expecting only a 2D table, but input contains\n{array.ndim} dimensions"
            )

        if not np.all(array[:-1, 0] <= array[1:, 0]):
            raise ValueError(
                "The underlying ``TREAD`` command requires that the first column is in "
                "ascending order."
            )

        # weird bug where MAPDL ignores the first row when there are greater than 2 columns
        if array.shape[1] > 2:
            array = np.vstack((array[0], array))

        base_name = random_string() + ".txt"
        filename = os.path.join(tempfile.gettempdir(), base_name)
        np.savetxt(filename, array, header="File generated by PyMAPDL:load_table")

        if not self._local:
            self.upload(filename, progress_bar=False)
            filename = base_name
        # skip the first line its a header we wrote in np.savetxt
        self.tread(name, filename, nskip=1, mute=True)

        if self._local:
            os.remove(filename)
        else:
            self.slashdelete(filename)

    def _display_plot(self, *args, **kwargs):  # pragma: no cover
        raise NotImplementedError("Implemented by child class")

    def _run(self, *args, **kwargs):  # pragma: no cover
        raise NotImplementedError("Implemented by child class")

    @property
    def version(self) -> float:
        """
        MAPDL build version.

        Examples
        --------
        >>> mapdl.version
        20.2
        """
        return self.parameters.revision

    @property
    @supress_logging
    def directory(self) -> str:
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
        accessible, ``cwd`` (:func:`_MapdlCore.cwd`) will raise
        a warning.
        """
        # always attempt to cache the path
        i = 0
        while (not self._path and i > 5) or i == 0:
            try:
                self._path = self.inquire("", "DIRECTORY")
            except Exception:  # pragma: no cover
                pass
            i += 1
            if not self._path:  # pragma: no cover
                time.sleep(0.1)

        # os independent path format
        if self._path:  # self.inquire might return ''.
            self._path = self._path.replace("\\", "/")
            # new line to fix path issue, see #416
            self._path = repr(self._path)[1:-1]
        else:  # pragma: no cover
            raise IOError(
                f"The directory returned by /INQUIRE is not valid ('{self._path}')."
            )

        return self._path

    @directory.setter
    @supress_logging
    def directory(self, path):
        """Change the directory using ``Mapdl.cwd``"""
        self.cwd(path)

    @property
    def _lockfile(self):
        """lockfile path"""
        path = self.directory
        if path is not None:
            return os.path.join(path, self.jobname + ".lock").replace("\\", "/")

    def exit(self):  # pragma: no cover
        """Exit from MAPDL"""
        raise NotImplementedError("Implemented by child class")

    def __del__(self):  # pragma: no cover
        """Clean up when complete"""
        if self._cleanup:
            try:
                self.exit()
            except Exception as e:
                try:  # logger might be closed
                    if self._log is not None:
                        self._log.error("exit: %s", str(e))
                except Exception:
                    pass

    @supress_logging
    def get_array(
        self,
        entity="",
        entnum="",
        item1="",
        it1num="",
        item2="",
        it2num="",
        kloop="",
        **kwargs,
    ):
        """Uses the ``*VGET`` command to Return an array from ANSYS as a
        Python array.

        See `VGET
        <https://www.mm.bme.hu/~gyebro/files/ans_help_v182/ans_cmd/Hlp_C_VGET_st.html>`
        for more details.

        Parameters
        ----------
        entity
            Entity keyword.  Valid keywords are NODE, ELEM, KP, LINE,
            AREA, VOLU, etc

        entnum
            The number of the entity.

        item1
            The name of a particular item for the given entity.  Valid
            items are as shown in the Item1 columns of the tables
            below.

        it1num
            The number (or label) for the specified Item1 (if any).
            Valid IT1NUM values are as shown in the IT1NUM columns of
            the tables below.  Some Item1 labels do not require an
            IT1NUM value.

        item2, it2num
            A second set of item labels and numbers to further qualify
            the item for which data is to be retrieved.  Most items do
            not require this level of information.

        kloop
            Field to be looped on:

            - 0 or 2 : Loop on the ENTNUM field (default).
            - 3 : Loop on the Item1 field.
            - 4 : Loop on the IT1NUM field. Successive items are as shown with IT1NUM.
            - 5 : Loop on the Item2 field.
            - 6 : Loop on the IT2NUM field. Successive items are as shown with IT2NUM.

        Notes
        -----
        Please reference your Ansys help manual ``*VGET`` command tables
        for all the available ``*VGET`` values.

        Examples
        --------
        List the current selected node numbers

        >>> mapdl.get_array('NODE', item1='NLIST')
        array([  1.,   2.,   3.,   4.,   5.,   6.,   7.,   8.,
              ...
              314., 315., 316., 317., 318., 319., 320., 321.])

        List the displacement in the X direction for the first result

        >>> mapdl.post1()
        >>> mapdl.set(1, 1)
        >>> disp_x = mapdl.get_array('NODE', item1='U', it1num='X')
        array([ 0.01605306, -0.01605306,  0.00178402, -0.01605306,
               ...
               -0.00178402, -0.01234851,  0.01234851, -0.01234851])

        """
        arr = self._get_array(entity, entnum, item1, it1num, item2, it2num, kloop)

        # edge case where corba refuses to return the array
        ntry = 0
        while arr.size == 1 and arr[0] == -1:
            arr = self._get_array(entity, entnum, item1, it1num, item2, it2num, kloop)
            if ntry > 5:
                raise MapdlRuntimeError("Unable to get array for %s" % entity)
            ntry += 1
        return arr

    def _get_array(
        self,
        entity="",
        entnum="",
        item1="",
        it1num="",
        item2="",
        it2num="",
        kloop="",
        dtype=None,
        **kwargs,
    ):
        """Uses the VGET command to get an array from ANSYS"""
        parm_name = kwargs.pop("parm", None)

        if parm_name is None:
            parm_name = "__vget_tmp_%d__" % self._vget_arr_counter
            self._vget_arr_counter += 1

        out = self.starvget(
            parm_name,
            entity,
            entnum,
            item1,
            it1num,
            item2,
            it2num,
            kloop,
            mute=False,
        )

        # check if empty array
        if "the dimension number 1 is 0" in out:
            return np.empty(0)

        with self.non_interactive:
            self.vwrite("%s(1)" % parm_name)
            self.run("(F20.12)")

        array = np.fromstring(self.last_response, sep="\n")
        if dtype:
            return array.astype(dtype)
        else:
            return array

    def _display_plot(self, text):
        """Display the last generated plot (*.png) from MAPDL"""
        import scooby

        self._enable_interactive_plotting()
        png_found = PNG_TEST.findall(text)
        if png_found:
            # flush graphics writer
            self.show("CLOSE", mute=True)
            self.show("PNG", mute=True)

            import matplotlib.image as mpimg
            import matplotlib.pyplot as plt

            filename = self._screenshot_path()

            if os.path.isfile(filename):
                img = mpimg.imread(filename)
                plt.imshow(img)
                plt.axis("off")
                if self._show_matplotlib_figures:  # pragma: no cover
                    plt.show()  # consider in-line plotting
                if scooby.in_ipython():
                    from IPython.display import display

                    display(plt.gcf())
            else:  # pragma: no cover
                self._log.error("Unable to find screenshot at %s", filename)

    def _screenshot_path(self):
        """Return last filename based on the current jobname"""
        filenames = glob.glob(os.path.join(self.directory, f"{self.jobname}*.png"))
        filenames.sort()
        return filenames[-1]

    def _set_log_level(self, level):
        """alias for set_log_level"""
        self.set_log_level(level)

    def list(self, filename, ext=""):
        """Displays the contents of an external, coded file.

        APDL Command: ``/LIST``

        Parameters
        ----------
        fname : str
            File name and directory path. An unspecified directory
            path defaults to the working directory.

        ext : str, optional
            Filename extension
        """
        if hasattr(self, "_local"):  # gRPC
            if not self._local:
                return self._download_as_raw(filename).decode()

        path = pathlib.Path(filename)
        if path.parent != ".":
            path = os.path.join(self.directory, filename)

        path = str(path) + ext
        with open(path) as fid:
            return fid.read()

    @wraps(Commands.cwd)
    def cwd(self, *args, **kwargs):
        """Wraps cwd."""
        output = super().cwd(*args, mute=False, **kwargs)

        if output is not None:
            if "*** WARNING ***" in output:
                raise IncorrectWorkingDirectory(
                    "\n" + "\n".join(output.splitlines()[1:])
                )

        return output

    def get_nodal_loads(self, label=None):
        """
        Get the applied nodal loads.

        Uses ``FLIST``.

        Parameters
        ----------
        label : [str], optional
            If given, the output nodal loads are filtered to correspondent given label.
            Example of labels are ``FX``, ``FZ``, ``CHRGS`` or ``CSGZ``. By default None

        Returns
        -------
        List[List[Str]] or numpy.array
            If parameter ``label`` is give, the output is converted to a
            numpy array instead of a list of list of strings.
        """
        loads = self.flist().to_list()
        if label:
            loads = np.array(
                [[each[0], each[2], each[3]] for each in loads if each[1] == label]
            )
        return loads

    def get_nodal_constrains(self, label=None):
        """
        Get the applied nodal constrains:

        Uses ``DLIST``.

        Parameters
        ----------
        label : [str], optional
            If given, the output nodal constrains are filtered to correspondent given label.
            Example of labels are ``UX``, ``UZ``, ``VOLT`` or ``TEMP``. By default None

        Returns
        -------
        List[List[Str]] or numpy.array
            If parameter ``label`` is give, the output is converted to a
            numpy array instead of a list of list of strings.
        """
        constrains = self.dlist().to_list()
        if label:
            constrains = np.array(
                [[each[0], each[2], each[3]] for each in constrains if each[1] == label]
            )
        return constrains

    def _check_parameter_name(self, param_name):
        """Checks if a parameter name is allowed or not."""
        param_name = param_name.strip()

        match_valid_parameter_name = r"^[a-zA-Z_][a-zA-Z\d_\(\),\s\%]{0,31}$"
        # Using % is allowed, because of substitution, but it is very likely MAPDL will complain.
        if not re.search(match_valid_parameter_name, param_name):
            raise ValueError(
                f"The parameter name `{param_name}` is an invalid parameter name."
                "Only letters, numbers and `_` are permitted, up to 32 characters long."
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
            r"^_[a-zA-Z\d_\(\),\s_]{1,31}[a-zA-Z\d\(\),\s]$"
        )
        # If it also ends in underscore, this won't be triggered.
        if re.search(match_reserved_leading_underscored_parameter_name, param_name):
            raise ValueError(
                f"It is discouraged the use of parameters starting with underscore ('_'). "
                "This convention is reserved for parameters used by the GUI and/or Mechanical APDL-provided macros."
            )

        # invalid parameter (using ARGXX or ARXX)
        match_reserved_arg_parameter_name = r"^(AR|ARG)(\d{1,3})$"
        if re.search(
            match_reserved_arg_parameter_name, param_name
        ):  # invalid parameter (using ARGXX or ARXX)
            raise ValueError(
                f"The parameters 'ARGXX' and 'ARXX' where 'XX' are integers, are reserved for functions and macros local parameters."
                "Hence its use is not recommended outside them."
                "You might run in unexpected behaviours, for example, parameters not being show in `mapdl.parameters`."
            )

    @wraps(Commands.mpread)
    def mpread(self, fname="", ext="", lib="", **kwargs):
        if lib:
            raise NotImplementedError(
                "The option 'lib' is not supported by the MAPDL gRPC server."
            )

        fname_ = fname + "." + ext
        fname = load_file(self, fname_)
        self._log.info("Bypassing 'MPREAD' with 'INPUT'.")
        return self.input(fname)

    @wraps(Commands.mpwrite)
    def mpwrite(
        self,
        fname="",
        ext="",
        lib="",
        mat="",
        download_file=False,
        progress_bar=True,
        **kwargs,
    ):
        fname_ = fname + "." + ext
        if not self._local:
            if os.path.dirname(fname_):
                raise IOError(
                    "Only writing files to the MAPDL working directory is allowed. "
                    f"The supplied path {fname_} is not allowed."
                )

        output = super().mpwrite(fname, ext, lib, mat, **kwargs)
        if download_file:
            self.download(os.path.basename(fname_), progress_bar=progress_bar)

        return output

    @wraps(Commands.dim)
    def dim(
        self,
        par="",
        type_="",
        imax="",
        jmax="",
        kmax="",
        var1="",
        var2="",
        var3="",
        csysid="",
        **kwargs,
    ):
        self._check_parameter_name(par)  # parameter name check
        if "(" in par or ")" in par:
            raise ValueError(
                "Parenthesis are not allowed as parameter name in 'mapdl.dim'."
            )

        return super().dim(
            par, type_, imax, jmax, kmax, var1, var2, var3, csysid, **kwargs
        )

    def _get_selected_(self, entity):  # pragma: no cover
        """Get list of selected entities."""
        allowed_values = ["NODE", "ELEM", "KP", "LINE", "AREA", "VOLU"]
        if entity.upper() not in allowed_values:
            raise ValueError(
                f"The value '{entity}' is not allowed."
                f"Only {allowed_values} are allowed"
            )

        entity = entity.upper()

        if entity == "NODE":
            return self.mesh.nnum.copy()
        elif entity == "ELEM":
            return self.mesh.enum.copy()
        elif entity == "KP":
            return self.geometry.knum
        elif entity == "LINE":
            return self.geometry.lnum
        elif entity == "AREA":
            return self.geometry.anum
        elif entity == "VOLU":
            return self.geometry.vnum

    def _pick_points(self, entity, pl, type_, previous_picked_points, **kwargs):
        """Show a plot and get the selected points."""
        _debug = kwargs.pop("_debug", False)  # for testing purposes
        previous_picked_points = set(previous_picked_points)

        q = self.queries
        picked_points = []
        picked_ids = []

        selector = getattr(q, entity.lower())

        # adding selection inversor
        pl._inver_mouse_click_selection = False

        selection_text = {
            "S": "New selection",
            "A": "Adding to selection",
            "R": "Reselecting from the selection",
            "U": "Unselecting",
        }

        def gen_text(picked_points=None):
            """Generate helpful text for the render window."""
            sel_ = "Unselecting" if pl._inver_mouse_click_selection else "Selecting"
            type_text = selection_text[type_]
            text = (
                f"Please use the left mouse button to pick the {entity}s.\n"
                f"Press the key 'u' to change between mouse selecting and unselecting.\n"
                f"Type: {type_} - {type_text}\n"
                f"Mouse selection: {sel_}\n"
            )

            picked_points_str = ""
            if picked_points:
                # reverse picked point order, exclude the brackets, and limit
                # to 40 characters
                picked_points_str = str(picked_points[::-1])[1:-1]
                if len(picked_points_str) > 40:
                    picked_points_str = picked_points_str[:40]
                    idx = picked_points_str.rfind(",") + 2
                    picked_points_str = picked_points_str[:idx] + "..."

            return text + f"Current {entity} selection: {picked_points_str}"

        def callback_(mesh, id_):
            point = mesh.points[id_]
            node_id = selector(
                point[0], point[1], point[2]
            )  # This will only return one node. Fine for now.

            if not pl._inver_mouse_click_selection:
                # Updating MAPDL points mapping
                if node_id not in picked_points:
                    picked_points.append(node_id)
                # Updating pyvista points mapping
                if id_ not in picked_ids:
                    picked_ids.append(id_)
            else:
                # Updating MAPDL points mapping
                if node_id in picked_points:
                    picked_points.remove(node_id)
                # Updating pyvista points mapping
                if id_ in picked_ids:
                    picked_ids.remove(id_)

            # remov etitle and update text
            pl.remove_actor("title")
            pl._picking_text = pl.add_text(
                gen_text(picked_points),
                font_size=10,
                name="_point_picking_message",
            )
            if picked_ids:
                pl.add_mesh(
                    mesh.points[picked_ids],
                    color="red",
                    point_size=10,
                    name="_picked_points",
                    pickable=False,
                    reset_camera=False,
                )
            else:
                pl.remove_actor("_picked_points")

        pl.enable_point_picking(
            callback=callback_,
            use_mesh=True,
            show_message=gen_text(),
            show_point=True,
            left_clicking=True,
            font_size=10,
            tolerance=kwargs.get("tolerance", 0.025),
        )

        def callback_u():
            # inverting bool
            pl._inver_mouse_click_selection = not pl._inver_mouse_click_selection
            pl._picking_text = pl.add_text(
                gen_text(picked_points),
                font_size=10,
                name="_point_picking_message",
            )

        pl.add_key_event("u", callback_u)

        if not _debug:  # pragma: no cover
            pl.show()
        else:
            _debug(pl)

        picked_points = set(
            picked_points
        )  # removing duplicates (although there should be none)

        if type_ == "S":
            pass
        elif type_ == "R":
            picked_points = previous_picked_points.intersection(picked_points)
        elif type_ == "A":
            picked_points = previous_picked_points.union(picked_points)
        elif type_ == "U":
            picked_points = previous_picked_points.difference(picked_points)

        return list(picked_points)

    def _perform_entity_list_selection(
        self, entity, selection_function, type_, item, comp, vmin, kabs
    ):
        """Select entities using CM, and the supplied selection function."""
        self.cm(f"__temp_{entity}s__", f"{entity}")  # Saving previous selection

        # Getting new selection
        for id_, each_ in enumerate(vmin):
            selection_function(
                self, "S" if id_ == 0 else "A", item, comp, each_, "", "", kabs
            )

        self.cm(f"__temp_{entity}s_1__", f"{entity}")

        self.cmsel("S", f"__temp_{entity}s__")
        self.cmsel(type_, f"__temp_{entity}s_1__")

        # Cleaning
        self.cmdele(f"__temp_{entity}s__")
        self.cmdele(f"__temp_{entity}s_1__")

    @wraps(Commands.nsel)
    def nsel(self, *args, **kwargs):
        """Wraps previons NSEL to allow to use a list/tuple/array for vmin.

        It will raise an error in case vmax or vinc are used too.
        """
        sel_func = (
            super().nsel
        )  # using super() inside the wrapped function confuses the references

        @allow_pickable_points()
        @wrap_point_SEL(entity="node")
        def wrapped(self, *args, **kwargs):
            return sel_func(*args, **kwargs)

        return wrapped(self, *args, **kwargs)

    @wraps(Commands.esel)
    def esel(self, *args, **kwargs):
        """Wraps previons ESEL to allow to use a list/tuple/array for vmin.

        It will raise an error in case vmax or vinc are used too.
        """
        sel_func = (
            super().esel
        )  # using super() inside the wrapped function confuses the references

        # @allow_pickable_points()
        @wrap_point_SEL(entity="elem")
        def wrapped(self, *args, **kwargs):
            return sel_func(*args, **kwargs)

        return wrapped(self, *args, **kwargs)

    @wraps(Commands.ksel)
    def ksel(self, *args, **kwargs):
        """Wraps superclassed KSEL to allow to use a list/tuple/array for vmin.

        It will raise an error in case vmax or vinc are used too.
        """
        sel_func = (
            super().ksel
        )  # using super() inside the wrapped function confuses the references

        @allow_pickable_points(entity="kp", plot_function="kplot")
        @wrap_point_SEL(entity="kp")
        def wrapped(self, *args, **kwargs):
            return sel_func(*args, **kwargs)

        return wrapped(self, *args, **kwargs)

    @wraps(Commands.lsel)
    def lsel(self, *args, **kwargs):
        """Wraps superclassed LSEL to allow to use a list/tuple/array for vmin.

        It will raise an error in case vmax or vinc are used too.
        """
        sel_func = (
            super().lsel
        )  # using super() inside the wrapped function confuses the references

        # @allow_pickable_points(entity="line", plot_function="lplot")
        @wrap_point_SEL(entity="line")
        def wrapped(self, *args, **kwargs):
            return sel_func(*args, **kwargs)

        return wrapped(self, *args, **kwargs)

    @wraps(Commands.asel)
    def asel(self, *args, **kwargs):
        """Wraps superclassed ASEL to allow to use a list/tuple/array for vmin.

        It will raise an error in case vmax or vinc are used too.
        """
        sel_func = (
            super().asel
        )  # using super() inside the wrapped function confuses the references

        # @allow_pickable_points(entity="area", plot_function="aplot")
        @wrap_point_SEL(entity="area")
        def wrapped(self, *args, **kwargs):
            return sel_func(*args, **kwargs)

        return wrapped(self, *args, **kwargs)

    @wraps(Commands.vsel)
    def vsel(self, *args, **kwargs):
        """Wraps superclassed VSEL to allow to use a list/tuple/array for vmin.

        It will raise an error in case vmax or vinc are used too.
        """
        sel_func = (
            super().vsel
        )  # using super() inside the wrapped function confuses the references

        # @allow_pickable_points(entity="volume", plot_function="vplot")
        @wrap_point_SEL(entity="volume")
        def wrapped(self, *args, **kwargs):
            return sel_func(*args, **kwargs)

        return wrapped(self, *args, **kwargs)

    def _raise_errors(self, text):
        # to make sure the following error messages are caught even if a breakline is in between.
        flat_text = " ".join([each.strip() for each in text.splitlines()])

        if "is not a recognized" in flat_text:
            text = text.replace("This command will be ignored.", "")
            text += "\n\nIgnore these messages by setting 'ignore_errors'=True"
            raise MapdlInvalidRoutineError(text)

        if "command is ignored" in flat_text:
            text += "\n\nIgnore these messages by setting 'ignore_errors'=True"
            raise MapdlCommandIgnoredError(text)

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
                    self._log.warn("PERMITTED ERROR: " + permited_error_message.string)
                    continue
                else:
                    # We don't need to log exception because they already included in the main logger.
                    # logger.error(response)
                    # However, exceptions are recorded in the global logger which do not record
                    # information of the instances name, hence we edit the error message.
                    raise MapdlRuntimeError(
                        f"\n\nError in instance {self.name}\n\n" + error_message
                    )

    @wraps(Commands.lsread)
    def lsread(self, *args, **kwargs):
        """Wraps the ``LSREAD`` which does not work in interactive mode."""
        self._log.debug("Forcing 'LSREAD' to run in non-interactive mode.")
        with self.non_interactive:
            super().lsread(*args, **kwargs)
        return self._response.strip()

    def file(self, fname="", ext="", **kwargs):
        """Specifies the data file where results are to be found.

        APDL Command: FILE

        Parameters
        ----------
        fname : str
            File name and directory path (248 characters maximum, including the
            characters needed for the directory path).  An unspecified
            directory path defaults to the working directory; in this case, you
            can use all 248 characters for the file name.

        ext : str, default: "rst"
            Filename extension (eight-character maximum). If ``fname`` has an
            extension this is ignored.

        Notes
        -----
        Specifies the Ansys data file where the results are to be found for
        postprocessing.

        Examples
        --------
        Load a result file that is outside of the current working directory.

        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> mapdl.post1()
        >>> mapdl.file('/tmp/file.rst')

        """
        fname = self._get_file_name(fname, ext, "rst")
        fname = self._get_file_path(fname, kwargs.get("progress_bar", False))
        file_, ext_ = self._decompose_fname(fname)
        return self._file(file_, ext_, **kwargs)

    def _file(self, filename, extension, **kwargs):
        """Run the MAPDL ``file`` command with a proper filename."""
        return self.run(f"FILE,{filename},{extension}", **kwargs)

    @wraps(Commands.use)
    def use(self, *args, **kwargs):
        """Wrap the use command."""
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
        return super().use(*args, **kwargs)

    @wraps(Commands.set)
    def set(
        self,
        lstep="",
        sbstep="",
        fact="",
        kimg="",
        time="",
        angle="",
        nset="",
        order="",
        **kwargs,
    ):
        """Wraps SET to return a Command listing"""
        output = super().set(
            lstep, sbstep, fact, kimg, time, angle, nset, order, **kwargs
        )

        if (
            isinstance(lstep, str)
            and lstep.upper() == "LIST"
            and not sbstep
            and not fact
        ):
            return CommandListingOutput(
                output,
                magicwords=["SET", "TIME/FREQ"],
                columns_names=[
                    "SET",
                    "TIME/FREQ",
                    "LOAD STEP",
                    "SUBSTEP",
                    "CUMULATIVE",
                ],
            )
        else:
            return output

    def _check_mapdl_os(self):
        platform = self.get_value("active", 0, "platform").strip()
        if "l" in platform.lower():
            self._platform = "linux"
        elif "w" in platform.lower():  # pragma: no cover
            self._platform = "windows"
        else:  # pragma: no cover
            raise MapdlRuntimeError("Unknown platform: {}".format(platform))

    @property
    def platform(self):
        """Return the platform where MAPDL is running."""
        if self._platform is None:
            self._check_mapdl_os()
        return self._platform

    def _check_on_docker(self):
        """Check if MAPDL is running on docker."""
        # self.get_mapdl_envvar("ON_DOCKER") # for later
        if not self.is_grpc:  # pragma: no cover
            return False

        if self.platform == "linux":
            self.sys(
                "if grep -sq 'docker\|lxc' /proc/1/cgroup; then echo 'true' > __outputcmd__.txt; else echo 'false' > __outputcmd__.txt;fi;"
            )
        elif self.platform == "windows":  # pragma: no cover
            return False  # TODO: check if it is running a windows docker container. So far it is not supported.

        if not self.is_local:
            sys_output = self._download_as_raw("__outputcmd__.txt").decode().strip()

        else:  # pragma: no cover
            file_ = os.path.join(self.directory, "__outputcmd__.txt")
            with open(file_, "r") as f:
                sys_output = f.read().strip()

        self._log.debug(f"The output of sys command is: '{sys_output}'.")
        self.slashdelete("__outputcmd__.txt")  # cleaning
        return sys_output == "true"

    @property
    def on_docker(self):
        """Check if MAPDL is running on docker."""
        if self._on_docker is None:
            self._on_docker = self._check_on_docker()
        return self._on_docker

    @property
    def is_local(self):
        """Check if the instance is running locally or remotely."""
        return self._local

    @property
    def launched(self):
        """Check if the MAPDL instance has been launched by PyMAPDL."""
        return self._launched

    def _decompose_fname(self, fname):
        """Decompose a file name (with or without path) into filename and extension.

        Parameters
        ----------
        fname : str
            File name with or without path.

        Returns
        -------
        str
            File name (without extension or path)

        str
            File extension (without dot)
        """
        fname = pathlib.Path(fname)
        return fname.stem, fname.suffix.replace(".", "")

    class _force_output:
        """Allows user to enter commands that need to run with forced text output."""

        def __init__(self, parent):
            self._parent = weakref.ref(parent)

        def __enter__(self):
            self._parent()._log.debug("Entering force-output mode")

            if self._parent().wrinqr(1) != 1:  # using wrinqr is more reliable than *get
                self._in_nopr = True
                self._parent()._run("/gopr")  # Going to PR mode
            else:
                self._in_nopr = False

            self._previous_mute, self._parent()._mute = self._parent()._mute, False

        def __exit__(self, *args):
            self._parent()._log.debug("Exiting force-output mode")
            if self._in_nopr:
                self._parent()._run("/nopr")
            self._parent()._mute = self._previous_mute

    def _parse_rlist(self):
        # mapdl.rmore(*list)
        with self.force_output:
            rlist = self.rlist()

        # removing ueless part
        rlist = rlist.replace(
            """   *****MAPDL VERIFICATION RUN ONLY*****
     DO NOT USE RESULTS FOR PRODUCTION
""",
            "",
        )
        constants_ = re.findall(
            r"REAL CONSTANT SET.*?\n\n", rlist + "\n\n", flags=re.DOTALL
        )

        const_ = {}
        for each in constants_:
            values = [0 for i in range(18)]
            set_ = int(re.match(r"REAL CONSTANT SET\s+(\d+)\s+", each).groups()[0])
            limits = (
                int(re.match(r".*ITEMS\s+(\d+)\s+", each).groups()[0]),
                int(re.match(r".*TO\s+(\d+)\s*", each).groups()[0]),
            )
            values_ = [float(i) for i in each.strip().splitlines()[1].split()]

            if not set_ in const_.keys():
                const_[set_] = values

            for i, jlimit in enumerate(range(limits[0] - 1, limits[1])):
                const_[set_][jlimit] = values_[i]

        return const_
