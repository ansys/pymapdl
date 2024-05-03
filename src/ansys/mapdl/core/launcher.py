# Copyright (C) 2024 ANSYS, Inc. and/or its affiliates.
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

"""Module for launching MAPDL locally or connecting to a remote instance with gRPC."""

import atexit
import os
import platform
from queue import Empty, Queue
import re
import socket
import subprocess
import tempfile
import threading
import time
from typing import TYPE_CHECKING, Dict, List, Optional, Tuple, Union
import warnings

import psutil

try:
    import ansys.platform.instancemanagement as pypim

    _HAS_PIM = True
except ModuleNotFoundError:  # pragma: no cover
    _HAS_PIM = False

try:
    from ansys.tools.path import find_ansys, get_ansys_path, version_from_path

    _HAS_ATP = True
except ModuleNotFoundError:
    _HAS_ATP = False

from ansys.mapdl import core as pymapdl
from ansys.mapdl.core import LOG
from ansys.mapdl.core._version import SUPPORTED_ANSYS_VERSIONS
from ansys.mapdl.core.errors import (
    DeprecationError,
    LockFileException,
    MapdlDidNotStart,
    MapdlRuntimeError,
    NotEnoughResources,
    PortAlreadyInUse,
    PortAlreadyInUseByAnMAPDLInstance,
    VersionError,
)
from ansys.mapdl.core.licensing import ALLOWABLE_LICENSES, LicenseChecker
from ansys.mapdl.core.mapdl_core import _ALLOWED_START_PARM
from ansys.mapdl.core.mapdl_grpc import MAX_MESSAGE_LENGTH, MapdlGrpc
from ansys.mapdl.core.misc import (
    check_valid_ip,
    check_valid_port,
    create_temp_dir,
    random_string,
    threaded,
)

if TYPE_CHECKING:  # pragma: no cover
    from ansys.mapdl.core.mapdl_console import MapdlConsole

# settings directory
SETTINGS_DIR = pymapdl.USER_DATA_PATH
if not os.path.isdir(SETTINGS_DIR):
    try:
        os.makedirs(SETTINGS_DIR)
        LOG.debug(f"Created settings directory: {SETTINGS_DIR}")
    except:
        warnings.warn(
            "Unable to create settings directory.\n"
            "Will be unable to cache MAPDL executable location"
        )

CONFIG_FILE = os.path.join(SETTINGS_DIR, "config.txt")
ALLOWABLE_MODES = ["console", "grpc"]

ON_WSL = os.name == "posix" and (
    bool(os.environ.get("WSL_DISTRO_NAME", None))
    or bool(os.environ.get("WSL_INTEROP", None))
)

if ON_WSL:
    LOG.info("On WSL: Running on WSL detected.")

LOCALHOST = "127.0.0.1"
MAPDL_DEFAULT_PORT = 50052

INTEL_MSG = """Due to incompatibilities between this MAPDL version, Windows, and VPN connections,
the flat '-mpi INTELMPI' is overwritten by '-mpi msmpi'.

If you still want to use 'INTEL', set:

launch_mapdl(..., force_intel=True, additional_switches='-mpi INTELMPI')

Be aware of possible errors or unexpected behavior with this configuration.
"""

GALLERY_INSTANCE = [None]


def _cleanup_gallery_instance() -> None:  # pragma: no cover
    """This cleans up any left over instances of MAPDL from building the gallery."""
    if GALLERY_INSTANCE[0] is not None:
        mapdl = MapdlGrpc(
            ip=GALLERY_INSTANCE[0]["ip"],
            port=GALLERY_INSTANCE[0]["port"],
        )
        mapdl.exit(force=True)


atexit.register(_cleanup_gallery_instance)


def _is_ubuntu() -> bool:
    """Determine if running as Ubuntu.

    It's a bit complicated because sometimes the distribution is
    Ubuntu, but the kernel has been recompiled and no longer has the
    word "ubuntu" in it.

    """
    # must be running linux for this to be True
    if os.name != "posix":
        return False

    proc = subprocess.Popen(
        "awk -F= '/^NAME/{print $2}' /etc/os-release",
        shell=True,
        stdout=subprocess.PIPE,
    )
    if "ubuntu" in proc.stdout.read().decode().lower():
        return True

    # try lsb_release as this is more reliable, but not always available.
    try:
        import lsb_release

        if lsb_release.get_distro_information()["ID"].lower() == "ubuntu":
            return True
    except ImportError:
        # finally, check platform
        return "ubuntu" in platform.platform().lower()


def close_all_local_instances(port_range: range = None) -> None:
    """Close all MAPDL instances within a port_range.

    This function can be used when cleaning up from a failed pool or
    batch run.

    Parameters
    ----------
    port_range : list, optional
        Defaults to ``range(50000, 50200)``.  Expand this range if
        there are many potential instances of MAPDL in gRPC mode.

    Examples
    --------
    Close all instances on in the range of 50000 and 50199.

    >>> import ansys.mapdl.core as pymapdl
    >>> pymapdl.close_all_local_instances()

    """
    if port_range is None:
        port_range = range(50000, 50200)

    @threaded
    def close_mapdl(port: Union[int, str], name: str = "Closing mapdl thread."):
        # Name argument is used by the threaded decorator.
        try:
            mapdl = MapdlGrpc(port=port, set_no_abort=False)
            mapdl.exit()
        except OSError:
            pass

    ports = check_ports(port_range)
    for port, state in ports.items():
        if state:
            close_mapdl(port)


def check_ports(port_range: range, ip: str = "localhost") -> List[int]:
    """Check the state of ports in a port range"""
    ports = {}
    for port in port_range:
        ports[port] = port_in_use(port, ip)
    return ports


def port_in_use(port: Union[int, str], host: str = LOCALHOST) -> bool:
    """Returns True when a port is in use at the given host.

    Must actually "bind" the address.  Just checking if we can create
    a socket is insufficient as it's possible to run into permission
    errors like:

    - An attempt was made to access a socket in a way forbidden by its
      access permissions.
    """
    return port_in_use_using_socket(port, host) or port_in_use_using_psutil(port)


def port_in_use_using_socket(port: Union[int, str], host: str) -> bool:
    """Returns True when a port is in use at the given host using socket library.

    Must actually "bind" the address.  Just checking if we can create
    a socket is insufficient as it's possible to run into permission
    errors like:

    - An attempt was made to access a socket in a way forbidden by its
      access permissions.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.bind((host, port))
            return False
        except:
            return True


def is_ansys_process(proc: psutil.Process) -> bool:
    """Check if the given process is an Ansys MAPDL process"""
    return (
        bool(proc)
        and proc.name().lower().startswith(("ansys", "mapdl"))
        and "-grpc" in proc.cmdline()
    )


def get_process_at_port(port) -> Optional[psutil.Process]:
    """Get the process (psutil.Process) running at the given port"""
    for proc in psutil.process_iter():
        try:
            connections = proc.connections(
                kind="inet"
            )  # just to check if we can access the
        except psutil.AccessDenied:
            continue

        for conns in connections:
            if conns.laddr.port == port:
                return proc

    return None


def port_in_use_using_psutil(port: Union[int, str]) -> bool:
    """Returns True when a port is in use at the given host using psutil.

    This function iterate over all the process, and their connections until
    it finds one using the given port.
    """
    if get_process_at_port(port):
        return True
    else:
        return False


def launch_grpc(
    exec_file: str = "",
    jobname: str = "file",
    nproc: int = 2,
    ram: Optional[int] = None,
    run_location: str = None,
    port: int = MAPDL_DEFAULT_PORT,
    additional_switches: str = "",
    override: bool = True,
    timeout: int = 20,
    verbose: Optional[bool] = None,
    add_env_vars: Optional[Dict[str, str]] = None,
    replace_env_vars: Optional[Dict[str, str]] = None,
    **kwargs,  # to keep compatibility with corba and console interface.
) -> Tuple[int, str, subprocess.Popen]:
    """Start MAPDL locally in gRPC mode.

    Parameters
    ----------
    exec_file : str, optional
        The location of the MAPDL executable.  Will use the cached
        location when left at the default ``None``.

    jobname : str, optional
        MAPDL jobname.  Defaults to ``'file'``.

    nproc : int, optional
        Number of processors.  Defaults to 2.

    ram : float, optional
        Fixed amount of memory to request for MAPDL.  If ``None``,
        then MAPDL will use as much as available on the host machine.

    run_location : str, optional
        MAPDL working directory.  Defaults to a temporary working
        directory.

    port : int
        Port to launch MAPDL gRPC on.  Final port will be the first
        port available after (or including) this port.

    additional_switches : str, optional
        Additional switches for MAPDL, for example ``"-p aa_r"``, the
        academic research license, would be added with:

        - ``additional_switches="-p aa_r"``

        Avoid adding switches like ``"-i"`` ``"-o"`` or ``"-b"`` as
        these are already included to start up the MAPDL server.  See
        the notes section for additional details.

    override : bool, optional
        Attempts to delete the lock file at the run_location.
        Useful when a prior MAPDL session has exited prematurely and
        the lock file has not been deleted.

    verbose : bool, optional
        Print all output when launching and running MAPDL.  Not
        recommended unless debugging the MAPDL start.  Default
        ``False``.

        .. deprecated:: v0.65.0
           The ``verbose`` argument is deprecated and will be completely
           removed in a future release.
           Use a logger instead. See :ref:`api_logging` for more details.

    kwargs : dict
        Not used. Added to keep compatibility between Mapdl_grpc and
        launcher_grpc ``start_parm``s.

    Returns
    -------
    int
        Returns the port number that the gRPC instance started on.

    Notes
    -----
    If ``PYMAPDL_START_INSTANCE`` is set to FALSE, this ``launch_mapdl`` will
    look for an existing instance of MAPDL at ``PYMAPDL_IP`` on port
    ``PYMAPDL_PORT``, with defaults 127.0.0.1 and 50052 if unset. This is
    typically used for automated documentation and testing.

    These are the MAPDL switch options as of 2020R2 applicable for
    running MAPDL as a service via gRPC.  Excluded switches such as
    ``"-j"`` either not applicable or are set via keyword arguments.

    -acc <device>
        Enables the use of GPU hardware.  See GPU
        Accelerator Capability in the Parallel Processing Guide for more
        information.

    -amfg
        Enables the additive manufacturing capability.  Requires
        an additive manufacturing license. For general information about
        this feature, see AM Process Simulation in ANSYS Workbench.

    -ansexe <executable>
         Activates a custom mechanical APDL executable.
        In the ANSYS Workbench environment, activates a custom
        Mechanical APDL executable.

    -custom <executable>
        Calls a custom Mechanical APDL executable
        See Running Your Custom Executable in the Programmer's Reference
        for more information.

    -db value
        Initial memory allocation
        Defines the portion of workspace (memory) to be used as the
        initial allocation for the database. The default is 1024
        MB. Specify a negative number to force a fixed size throughout
        the run; useful on small memory systems.

    -dis
        Enables Distributed ANSYS
        See the Parallel Processing Guide for more information.

    -dvt
        Enables ANSYS DesignXplorer advanced task (add-on).
        Requires DesignXplorer.

    -l <language>
        Specifies a language file to use other than English
        This option is valid only if you have a translated message file
        in an appropriately named subdirectory in
        ``/ansys_inc/v201/ansys/docu`` or
        ``Program Files\\ANSYS\\Inc\\V201\\ANSYS\\docu``

    -m <workspace>
        Specifies the total size of the workspace
        Workspace (memory) in megabytes used for the initial
        allocation. If you omit the ``-m`` option, the default is 2 GB
        (2048 MB). Specify a negative number to force a fixed size
        throughout the run.

    -machines <IP>
        Specifies the distributed machines
        Machines on which to run a Distributed ANSYS analysis. See
        Starting Distributed ANSYS in the Parallel Processing Guide for
        more information.

    -mpi <value>
        Specifies the type of MPI to use.
        See the Parallel Processing Guide for more information.

    -mpifile <appfile>
        Specifies an existing MPI file
        Specifies an existing MPI file (appfile) to be used in a
        Distributed ANSYS run. See Using MPI Files in the Parallel
        Processing Guide for more information.

    -na <value>
        Specifies the number of GPU accelerator devices
        Number of GPU devices per machine or compute node when running
        with the GPU accelerator feature. See GPU Accelerator Capability
        in the Parallel Processing Guide for more information.

    -name <value>
        Defines Mechanical APDL parameters
        Set mechanical APDL parameters at program start-up. The parameter
        name must be at least two characters long. For details about
        parameters, see the ANSYS Parametric Design Language Guide.

    -p <productname>
        ANSYS session product
        Defines the ANSYS session product that will run during the
        session. For more detailed information about the ``-p`` option,
        see Selecting an ANSYS Product via the Command Line.

    -ppf <license feature name>
        HPC license
        Specifies which HPC license to use during a parallel processing
        run. See HPC Licensing in the Parallel Processing Guide for more
        information.

    -smp
        Enables shared-memory parallelism.
        See the Parallel Processing Guide for more information.

    Examples
    --------
    Launch MAPDL using the default configuration.

    >>> from ansys.mapdl.core import launch_mapdl
    >>> mapdl = launch_mapdl()

    Run MAPDL with shared memory parallel and specify the location of
    the ansys binary.

    >>> exec_file = 'C:/Program Files/ANSYS Inc/v202/ansys/bin/winx64/ANSYS202.exe'
    >>> mapdl = launch_mapdl(exec_file, additional_switches='-smp')

    """
    LOG.debug("Starting 'launch_mapdl'.")
    # disable all MAPDL pop-up errors:
    os.environ["ANS_CMD_NODIAG"] = "TRUE"

    if verbose:
        raise DeprecationError(
            "The ``verbose`` argument is deprecated and will be completely removed in a future release. Use a logger instead. "
            "See https://mapdl.docs.pyansys.com/version/stable/api/logging.html for more details."
        )

    # use temporary directory if run_location is unspecified
    if run_location is None:
        run_location = create_temp_dir()
        LOG.debug(f"Using temporary directory for MAPDL run location: {run_location}")
    elif not os.path.isdir(run_location):
        os.mkdir(run_location)
        LOG.debug(f"Creating directory for MAPDL run location: {run_location}")

    if not os.access(run_location, os.W_OK):
        raise IOError('Unable to write to ``run_location`` "%s"' % run_location)

    # verify version
    if _HAS_ATP:
        if version_from_path("mapdl", exec_file) < 202:
            raise VersionError("The MAPDL gRPC interface requires MAPDL 20.2 or later")

    # verify lock file does not exist
    check_lock_file(run_location, jobname, override)

    # get the next available port
    if port is None:
        if not pymapdl._LOCAL_PORTS:
            port = MAPDL_DEFAULT_PORT
            LOG.debug(f"Using default port: {port}")
        else:
            port = max(pymapdl._LOCAL_PORTS) + 1
            LOG.debug(f"Using next available port: {port}")

        while port_in_use(port) or port in pymapdl._LOCAL_PORTS:
            port += 1
            LOG.debug(f"Port in use.  Incrementing port number. port={port}")

    else:
        if port_in_use(port):
            proc = get_process_at_port(port)
            if proc:
                if is_ansys_process(proc):
                    raise PortAlreadyInUseByAnMAPDLInstance
                else:
                    raise PortAlreadyInUse

    pymapdl._LOCAL_PORTS.append(port)

    cpu_sw = "-np %d" % nproc

    if ram:
        ram_sw = "-m %d" % int(1024 * ram)
        LOG.debug(f"Setting RAM: {ram_sw}")
    else:
        ram_sw = ""

    job_sw = "-j %s" % jobname
    port_sw = "-port %d" % port
    grpc_sw = "-grpc"

    # remove any temporary error files at the run location.  This is
    # important because we need to know if MAPDL is already running
    # here and because we're looking for any temporary files that are
    # created to tell when the process has started
    for filename in os.listdir(run_location):
        if ".err" == filename[-4:] and jobname in filename:
            if os.path.isfile(filename):
                try:
                    os.remove(filename)
                    LOG.debug(f"Removing temporary error file: {filename}")
                except:
                    raise IOError(
                        f"Unable to remove {filename}.  There might be "
                        "an instance of MAPDL running at running at "
                        f'"{run_location}"'
                    )

    # Windows will spawn a new window, special treatment
    if os.name == "nt":
        tmp_inp = ".__tmp__.inp"
        with open(os.path.join(run_location, tmp_inp), "w") as f:
            f.write("FINISH\r\n")
            LOG.debug(f"Writing temporary input file: {tmp_inp} with 'FINISH' command.")

        # must start in batch mode on windows to hide APDL window
        command_parm = [
            '"%s"' % exec_file,
            job_sw,
            cpu_sw,
            ram_sw,
            "-b",
            "-i",
            tmp_inp,
            "-o",
            ".__tmp__.out",
            additional_switches,
            port_sw,
            grpc_sw,
        ]
        command = " ".join(command_parm)

    else:  # linux
        command_parm = []
        command_parm.extend(
            [
                '"%s"' % exec_file,
                job_sw,
                cpu_sw,
                ram_sw,
                additional_switches,
                port_sw,
                grpc_sw,
            ]
        )
        command = " ".join(command_parm)

    LOG.debug(f"Starting MAPDL with command: {command}")

    env_vars = update_env_vars(add_env_vars, replace_env_vars)

    LOG.info(
        f"Running a local instance at port {port} the following command: '{command}'"
    )

    LOG.debug("MAPDL starting in background.")
    process = subprocess.Popen(
        command,
        shell=os.name != "nt",
        cwd=run_location,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env_vars,
    )

    LOG.debug("Generating queue object for stdout")
    stdout_queue, _ = _create_queue_for_std(process.stdout)

    # Checking connection
    try:
        LOG.debug("Checking process is alive")
        _check_process_is_alive(process, run_location)

        LOG.debug("Checking file error is created")
        _check_file_error_created(run_location, timeout)

        if os.name == "posix" and not ON_WSL:
            LOG.debug("Checking if gRPC server is alive.")
            _check_server_is_alive(stdout_queue, run_location, timeout)

    except MapdlDidNotStart as e:  # pragma: no cover
        msg = (
            str(e)
            + f"\nRun location: {run_location}"
            + f"\nCommand line used: {command}\n\n"
        )

        terminal_output = "\n".join(_get_std_output(std_queue=stdout_queue)).strip()
        if terminal_output.strip():
            msg = msg + "The full terminal output is:\n\n" + terminal_output

        raise MapdlDidNotStart(msg) from e

    # Ending thread
    # Todo: Ending queue thread
    return port, run_location, process


def _check_process_is_alive(process, run_location):
    if process.poll() is not None:  # pragma: no cover
        msg = f"MAPDL process died."
        raise MapdlDidNotStart(msg)


def _check_file_error_created(run_location, timeout):
    # watch for the creation of temporary files at the run_directory.
    # This lets us know that the MAPDL process has at least started
    sleep_time = 0.1
    for _ in range(int(timeout / sleep_time)):
        # check if any error files have been created.  This is
        # more reliable than using the lock file

        files = os.listdir(run_location)
        has_ans = any([filename for filename in files if ".err" in filename])
        if has_ans:
            LOG.debug("MAPDL session successfully started (Error file found)")
            break
        time.sleep(sleep_time)

    if not has_ans:
        msg = f"MAPDL failed to start.\nNo error file (.err) generated in working directory."
        raise MapdlDidNotStart(msg)


def _check_server_is_alive(stdout_queue, run_location, timeout):
    t0 = time.time()
    empty_attemps = 3
    empty_i = 0
    terminal_output = ""

    while time.time() < (t0 + timeout):
        terminal_output += "\n".join(_get_std_output(std_queue=stdout_queue)).strip()

        if not terminal_output and empty_i < empty_attemps:
            # For stability reasons.
            empty_i += 1
            time.sleep(0.1)
            continue

        if (
            "START GRPC SERVER" in terminal_output
            and "Server listening on" in terminal_output
        ):
            listening_on = terminal_output.splitlines()[-1].split(":")
            listening_on = ":".join(listening_on[1:]).strip()
            LOG.debug(f"MAPDL gRPC server successfully launched at: {listening_on}")
            break

    else:
        raise MapdlDidNotStart("MAPDL failed to start the gRPC server")


def _get_std_output(std_queue, timeout=1):
    lines = []
    reach_empty = False
    t0 = time.time()
    while (not reach_empty) or (time.time() < (t0 + timeout)):
        try:
            message = std_queue.get_nowait().decode(encoding="utf-8", errors="replace")
            lines.append(message)
        except Empty:
            reach_empty = True

    return lines


def _create_queue_for_std(std):
    """Create a queue and thread objects for a given PIPE std"""

    def enqueue_output(out, queue):
        try:
            for line in iter(out.readline, b""):
                queue.put(line)
            out.close()
        except ValueError:
            # When killing main process, a ValueError is show:
            # ValueError: PyMemoryView_FromBuffer(): info -> buf must not be NULL
            pass

    q = Queue()
    t = threading.Thread(target=enqueue_output, args=(std, q))
    t.daemon = True  # thread dies with the program
    t.start()

    return q, t


def launch_remote_mapdl(
    version=None,
    cleanup_on_exit=True,
) -> MapdlGrpc:
    """Start MAPDL remotely using the product instance management API.

    When calling this method, you need to ensure that you are in an environment where PyPIM is configured.
    This can be verified with :func:`pypim.is_configured <ansys.platform.instancemanagement.is_configured>`.

    Parameters
    ----------
    version : str, optional
        The MAPDL version to run, in the 3 digits format, such as "212".

        If unspecified, the version will be chosen by the server.

    cleanup_on_exit : bool, optional
        Exit MAPDL when python exits or the mapdl Python instance is
        garbage collected.

        If unspecified, it will be cleaned up.

    Returns
    -------
    ansys.mapdl.core.mapdl.MapdlBase
        An instance of Mapdl.
    """
    if not _HAS_PIM:  # pragma: no cover
        raise ModuleNotFoundError(
            "The package 'ansys-platform-instancemanagement' is required to use this function."
        )

    pim = pypim.connect()
    instance = pim.create_instance(product_name="mapdl", product_version=version)
    instance.wait_for_ready()
    channel = instance.build_grpc_channel(
        options=[
            ("grpc.max_receive_message_length", MAX_MESSAGE_LENGTH),
        ]
    )
    return MapdlGrpc(
        channel=channel,
        cleanup_on_exit=cleanup_on_exit,
        remote_instance=instance,
    )


def get_start_instance(start_instance: bool = True):
    """Check if the environment variable ``PYMAPDL_START_INSTANCE`` exists and is valid.

    Parameters
    ----------
    start_instance : bool
        Value to return when ``PYMAPDL_START_INSTANCE`` is unset.

    Returns
    -------
    bool
        ``True`` when the ``PYMAPDL_START_INSTANCE`` environment variable is
        true, ``False`` when PYMAPDL_START_INSTANCE is false. If unset,
        returns ``start_instance``.

    Raises
    ------
    OSError
        Raised when ``PYMAPDL_START_INSTANCE`` is not either true or false
        (case independent).

    Notes
    -----
    If the environment variable ``PYMAPDL_START_INSTANCE`` is set,
    hence the argument ``start_instance`` is overwritten.

    """
    if "PYMAPDL_START_INSTANCE" in os.environ and os.environ["PYMAPDL_START_INSTANCE"]:
        # It should not be empty
        if isinstance(start_instance, bool):
            warnings.warn(
                "The environment variable 'PYMAPDL_START_INSTANCE' is set, "
                "hence the argument 'start_instance' is overwritten."
            )
        start_instance = os.environ["PYMAPDL_START_INSTANCE"]
    else:
        LOG.debug(
            f"PYMAPDL_START_INSTANCE is unset. Using default value {start_instance}."
        )

    if isinstance(start_instance, str):
        start_instance = start_instance.lower().strip()
        if start_instance not in ["true", "false"]:
            raise OSError(
                f'Invalid value "{start_instance}" for "start_instance" (or "PYMAPDL_START_INSTANCE"\n'
                '"start_instance" should be either "TRUE" or "FALSE"'
            )

        LOG.debug(f"PYMAPDL_START_INSTANCE is set to {start_instance}")
        return start_instance == "true"

    elif isinstance(start_instance, bool):
        return start_instance

    elif start_instance is None:
        LOG.debug(
            "'PYMAPDL_START_INSTANCE' is unset, and there is no supplied value. Using default, which is 'True'."
        )
        return True  # Default is true
    else:
        raise ValueError("Only booleans are allowed as arguments.")


def get_default_ansys():
    """Searches for ansys path within the standard install location
    and returns the path and version of the latest MAPDL version installed.

    Returns
    -------
    ansys_path : str
        Full path to ANSYS executable.

    version : float
        Version float.  For example, 21.1 corresponds to 2021R1.

    Examples
    --------
    Within Windows

    >>> from ansys.mapdl.core.launcher import get_default_ansys
    >>> get_default_ansys()
    'C:/Program Files/ANSYS Inc/v211/ANSYS/bin/winx64/ansys211.exe', 21.1

    Within Linux

    >>> get_default_ansys()
    (/usr/ansys_inc/v211/ansys/bin/ansys211, 21.1)
    """
    return find_ansys(supported_versions=SUPPORTED_ANSYS_VERSIONS)


def get_default_ansys_path():
    """Searches for ansys path within the standard install location
    and returns the path of the latest MAPDL version installed.

    Returns
    -------
    str
        Full path to ANSYS executable.

    Examples
    --------
    Within Windows

    >>> from ansys.mapdl.core.launcher import get_default_ansys
    >>> get_default_ansys_path()
    'C:/Program Files/ANSYS Inc/v211/ANSYS/bin/winx64/ansys211.exe'

    Within Linux

    >>> get_default_ansys_path()
    '/usr/ansys_inc/v211/ansys/bin/ansys211'
    """
    return get_default_ansys()[0]


def get_default_ansys_version():
    """Searches for ansys path within the standard install location
    and returns the version of the latest MAPDL version installed.

    Returns
    -------
    float
        Version float.  For example, 21.1 corresponds to 2021R1.

    Examples
    --------
    Within Windows

    >>> from ansys.mapdl.core.launcher import get_default_ansys
    >>> get_default_ansys_version()
    21.1

    Within Linux

    >>> get_default_ansys_version()
    21.1
    """
    return get_default_ansys()[1]


def check_valid_ansys():
    """Checks if a valid version of ANSYS is installed and preconfigured"""
    ansys_bin = get_ansys_path(allow_input=False)
    if ansys_bin is not None:
        version = version_from_path("mapdl", ansys_bin)
        return not (version < 170 and os.name != "posix")
    return False


def check_lock_file(path, jobname, override):
    LOG.debug("Checking for lock file")
    # Check for lock file
    lockfile = os.path.join(path, jobname + ".lock")
    if os.path.isfile(lockfile):
        if not override:
            raise LockFileException(
                '\nLock file exists for jobname "%s"' % jobname
                + ' at\n"%s"\n\n' % lockfile
                + "Set ``override=True`` to or delete the lock file "
                "to start MAPDL"
            )
        else:
            try:
                os.remove(lockfile)
                LOG.debug("Removed lock file")
            except PermissionError:
                raise LockFileException(
                    "Unable to remove lock file.  "
                    "Another instance of MAPDL might be "
                    f"running at '{path}'"
                )


def _validate_MPI(add_sw, exec_path, force_intel=False):
    """Validate MPI configuration.

    Enforce Microsoft MPI in version 21.0 or later, to fix a
    VPN issue on Windows.

    Parameters
    ----------
    add_sw : str
        Additional switches.
    exec_path : str
        Path to the MAPDL executable.
    force_intel : bool, optional
        Force the usage of intelmpi. The default is ``False``.

    Returns
    -------
    str
        Validated additional switches.

    """
    # Converting additional_switches to lower case to avoid mismatches.
    add_sw_lower_case = add_sw.lower()

    # known issues with distributed memory parallel (DMP)
    if "smp" not in add_sw_lower_case:  # pragma: no cover
        # Ubuntu ANSYS fails to launch without I_MPI_SHM_LMT
        if _is_ubuntu():
            LOG.debug("Ubuntu system detected. Adding 'I_MPI_SHM_LMT' env var.")
            os.environ["I_MPI_SHM_LMT"] = "shm"

        if _HAS_ATP:
            condition = (
                os.name == "nt"
                and not force_intel
                and (222 > version_from_path("mapdl", exec_path) >= 210)
            )
        else:
            if os.name == "nt":
                warnings.warn(
                    "Because 'ansys-tools-path' is not installed, PyMAPDL cannot check\n"
                    "if this Ansys version requires the MPI fix, so if you are on Windows,\n"
                    "the fix is applied by default.\n"
                    "Use 'force_intel=True' to not apply the fix."
                )
            condition = os.name == "nt" and not force_intel

        if condition:
            # Workaround to fix a problem when launching ansys in 'dmp' mode in the
            # recent windows version and using VPN.
            # This is due to the intel compiler, and only affects versions between
            # 210 and 222.
            #
            # There doesn't appear to be an easy way to check if we
            # are running VPN in Windows in python, it seems we will
            # need to know a local address where to ping but that will
            # change for each client/person using the VPN.
            #
            # Adding '-mpi msmpi' to the launch parameter fix it.
            if "intelmpi" in add_sw_lower_case:
                LOG.debug(
                    "Intel MPI flag detected. Removing it, if you want to enforce it, use ``force_intel`` keyword argument."
                )
                # Remove intel flag.
                regex = "(-mpi)( *?)(intelmpi)"
                add_sw = re.sub(regex, "", add_sw, flags=re.IGNORECASE)
                warnings.warn(INTEL_MSG)

            LOG.debug("Forcing Microsoft MPI (MSMPI) to avoid VPN issues.")
            add_sw += " -mpi msmpi"

    return add_sw


def _force_smp_student_version(add_sw, exec_path):
    """Force SMP in student version.

    Parameters
    ----------
    add_sw : str
        Additional switches.
    exec_path : str
        Path to the MAPDL executable.

    Returns
    -------
    str
        Validated additional switches.

    """
    # Converting additional_switches to lower case to avoid mismatches.
    add_sw_lower_case = add_sw.lower()

    if (
        "-mpi" not in add_sw_lower_case
        and "-dmp" not in add_sw_lower_case
        and "-smp" not in add_sw_lower_case
    ):  # pragma: no cover
        if "student" in exec_path.lower():
            add_sw += " -smp"
            LOG.debug("Student version detected, using '-smp' switch by default.")
    return add_sw


def launch_mapdl(
    exec_file: Optional[str] = None,
    run_location: Optional[str] = None,
    jobname: str = "file",
    nproc: Optional[int] = None,
    ram: Optional[Union[int, str]] = None,
    mode: Optional[str] = None,
    override: bool = False,
    loglevel: str = "ERROR",
    additional_switches: str = "",
    start_timeout: int = 45,
    port: Optional[int] = None,
    cleanup_on_exit: bool = True,
    start_instance: Optional[bool] = None,
    ip: Optional[str] = None,
    clear_on_connect: bool = True,
    log_apdl: Optional[Union[bool, str]] = None,
    remove_temp_files: Optional[bool] = None,
    remove_temp_dir_on_exit: bool = False,
    verbose_mapdl: Optional[bool] = None,
    license_server_check: bool = True,
    license_type: Optional[bool] = None,
    print_com: bool = False,
    add_env_vars: Optional[Dict[str, str]] = None,
    replace_env_vars: Optional[Dict[str, str]] = None,
    version: Optional[Union[int, str]] = None,
    **kwargs,
) -> Union[MapdlGrpc, "MapdlConsole"]:
    """Start MAPDL locally.

    Parameters
    ----------
    exec_file : str, optional
        The location of the MAPDL executable.  Will use the cached
        location when left at the default ``None`` and no environment
        variable is set.

        .. note::

           The executable path can be also set through the environment variable
           ``PYMAPDL_MAPDL_EXEC``. For example:

           .. code:: console

              export PYMAPDL_MAPDL_EXEC=/ansys_inc/v211/ansys/bin/mapdl

    run_location : str, optional
        MAPDL working directory.  Defaults to a temporary working
        directory.  If directory doesn't exist, one is created.

    jobname : str, optional
        MAPDL jobname.  Defaults to ``'file'``.

    nproc : int, optional
        Number of processors.  Defaults to 2.

    ram : float, optional
        Fixed amount of memory to request for MAPDL.  If ``None``,
        then MAPDL will use as much as available on the host machine.

    mode : str, optional
        Mode to launch MAPDL.  Must be one of the following:

        - ``'grpc'``
        - ``'console'``

        The ``'grpc'`` mode is available on ANSYS 2021R1 or newer and
        provides the best performance and stability.
        The ``'console'`` mode is for legacy use only Linux only prior to 2020R2.
        This console mode is pending depreciation.
        Visit :ref:`versions_and_interfaces` for more information.

    override : bool, optional
        Attempts to delete the lock file at the ``run_location``.
        Useful when a prior MAPDL session has exited prematurely and
        the lock file has not been deleted.

    loglevel : str, optional
        Sets which messages are printed to the console.  ``'INFO'``
        prints out all ANSYS messages, ``'WARNING'`` prints only
        messages containing ANSYS warnings, and ``'ERROR'`` logs only
        error messages.

    additional_switches : str, optional
        Additional switches for MAPDL, for example ``'aa_r'``, the
        academic research license, would be added with:

        - ``additional_switches="-aa_r"``

        Avoid adding switches like ``-i``, ``-o`` or ``-b`` as these are already
        included to start up the MAPDL server.  See the notes
        section for additional details.

    start_timeout : float, optional
        Maximum allowable time to connect to the MAPDL server.

    port : int
        Port to launch MAPDL gRPC on.  Final port will be the first
        port available after (or including) this port.  Defaults to
        50052.  You can also override the port default with the
        environment variable ``PYMAPDL_PORT=<VALID PORT>``
        This argument has priority over the environment variable.

    cleanup_on_exit : bool, optional
        Exit MAPDL when python exits or the mapdl Python instance is
        garbage collected.

    start_instance : bool, optional
        When False, connect to an existing MAPDL instance at ``ip``
        and ``port``, which default to ip ``'127.0.0.1'`` at port 50052.
        Otherwise, launch a local instance of MAPDL.  You can also
        override the default behavior of this keyword argument with
        the environment variable ``PYMAPDL_START_INSTANCE=FALSE``.

    ip : str, optional
        Used only when ``start_instance`` is ``False``. If provided,
        and ``start_instance`` (or its correspondent environment variable
        ``PYMAPDL_START_INSTANCE``) is ``True`` then, an exception is raised.
        Specify the IP address of the MAPDL instance to connect to.
        You can also provide a hostname as an alternative to an IP address.
        Defaults to ``'127.0.0.1'``. You can also override the
        default behavior of this keyword argument with the
        environment variable ``PYMAPDL_IP=<IP>``. If this environment variable
        is empty, it is as it is not set.

    clear_on_connect : bool, optional
        Defaults to ``True``, giving you a fresh environment when
        connecting to MAPDL. When if ``start_instance`` is specified
        it defaults to ``False``.

    log_apdl : str, optional
        Enables logging every APDL command to the local disk.  This
        can be used to "record" all the commands that are sent to
        MAPDL via PyMAPDL so a script can be run within MAPDL without
        PyMAPDL. This argument is the path of the output file (e.g.
        ``log_apdl='pymapdl_log.txt'``). By default this is disabled.

    remove_temp_files : bool, optional
        When ``run_location`` is ``None``, this launcher creates a new MAPDL
        working directory within the user temporary directory, obtainable with
        ``tempfile.gettempdir()``. When this parameter is
        ``True``, this directory will be deleted when MAPDL is exited. Default
        ``False``.

        .. deprecated:: 0.64.0
           Use argument ``remove_temp_dir_on_exit`` instead.

    remove_temp_dir_on_exit : bool, optional
        When ``run_location`` is ``None``, this launcher creates a new MAPDL
        working directory within the user temporary directory, obtainable with
        ``tempfile.gettempdir()``. When this parameter is
        ``True``, this directory will be deleted when MAPDL is exited. Default
        ``False``.
        If you change the working directory, PyMAPDL does not delete the original
        working directory nor the new one.

    verbose_mapdl : bool, optional
        Enable printing of all output when launching and running
        MAPDL.  This should be used for debugging only as output can
        be tracked within pymapdl.  Default ``False``.

        .. deprecated:: v0.65.0
           The ``verbose_mapdl`` argument is deprecated and will be completely
           removed in a future release.
           Use a logger instead. See :ref:`api_logging` for more details.

    license_server_check : bool, optional
        Check if the license server is available if MAPDL fails to
        start.  Only available on ``mode='grpc'``. Defaults ``True``.

    license_type : str, optional
        Enable license type selection. You can input a string for its
        license name (for example ``'meba'`` or ``'ansys'``) or its description
        ("enterprise solver" or "enterprise" respectively).
        You can also use legacy licenses (for example ``'aa_t_a'``) but it will
        also raise a warning. If it is not used (``None``), no specific license
        will be requested, being up to the license server to provide a specific
        license type. Default is ``None``.

    print_com : bool, optional
        Print the command ``/COM`` arguments to the standard output.
        Default ``False``.

    add_env_vars : dict, optional
        The provided dictionary will be used to extend the MAPDL process
        environment variables. If you want to control all of the environment
        variables, use the argument ``replace_env_vars``. Defaults to ``None``.

    replace_env_vars : dict, optional
        The provided dictionary will be used to replace all the MAPDL process
        environment variables. It replace the system environment variables
        which otherwise would be used in the process.
        To just add some environment variables to the MAPDL
        process, use ``add_env_vars``. Defaults to ``None``.

    version : float, optional
        Version of MAPDL to launch. If ``None``, the latest version is used.
        Versions can be provided as integers (i.e. ``version=222``) or
        floats (i.e. ``version=22.2``).
        To retrieve the available installed versions, use the function
        :meth:`ansys.tools.path.path.get_available_ansys_installations`.

        .. note::

           The default version can be also set through the environment variable
           ``PYMAPDL_MAPDL_VERSION``. For example:

           .. code:: console

              export PYMAPDL_MAPDL_VERSION=22.2

    kwargs : dict, optional
        These keyword arguments are interface specific or for
        development purposes. See Notes for more details.

        set_no_abort : :class:`bool`
          *(Development use only)*
          Sets MAPDL to not abort at the first error within /BATCH mode.
          Defaults to ``True``.

        force_intel : :class:`bool`
          *(Development use only)*
          Forces the use of Intel message pass interface (MPI) in versions between
          Ansys 2021R0 and 2022R2, where because of VPNs issues this MPI is deactivated
          by default. See :ref:`vpn_issues_troubleshooting` for more information.
          Defaults to ``False``.

    Returns
    -------
    Union[MapdlGrpc, MapdlConsole]
        An instance of Mapdl.  Type depends on the selected ``mode``.

    Notes
    -----

    **Ansys Student Version**

    If an Ansys Student version is detected, PyMAPDL will launch MAPDL in
    shared-memory parallelism (SMP) mode unless another option is specified.

    **Additional switches**

    These are the MAPDL switch options as of 2020R2 applicable for
    running MAPDL as a service via gRPC.  Excluded switches such as
    ``"-j"`` either not applicable or are set via keyword arguments.

    \\-acc <device>
        Enables the use of GPU hardware.  See GPU
        Accelerator Capability in the Parallel Processing Guide for more
        information.

    \\-amfg
        Enables the additive manufacturing capability.  Requires
        an additive manufacturing license. For general information about
        this feature, see AM Process Simulation in ANSYS Workbench.

    \\-ansexe <executable>
        Activates a custom mechanical APDL executable.
        In the ANSYS Workbench environment, activates a custom
        Mechanical APDL executable.

    \\-custom <executable>
        Calls a custom Mechanical APDL executable
        See Running Your Custom Executable in the Programmer's Reference
        for more information.

    \\-db value
        Initial memory allocation
        Defines the portion of workspace (memory) to be used as the
        initial allocation for the database. The default is 1024
        MB. Specify a negative number to force a fixed size throughout
        the run; useful on small memory systems.

    \\-dis
        Enables Distributed ANSYS
        See the Parallel Processing Guide for more information.

    \\-dvt
        Enables ANSYS DesignXplorer advanced task (add-on).
        Requires DesignXplorer.

    \\-l <language>
        Specifies a language file to use other than English
        This option is valid only if you have a translated message file
        in an appropriately named subdirectory in
        ``/ansys_inc/v201/ansys/docu`` or
        ``Program Files\\ANSYS\\Inc\\V201\\ANSYS\\docu``

    \\-m <workspace>
        Specifies the total size of the workspace
        Workspace (memory) in megabytes used for the initial
        allocation. If you omit the ``-m`` option, the default is 2 GB
        (2048 MB). Specify a negative number to force a fixed size
        throughout the run.

    \\-machines <IP>
        Specifies the distributed machines
        Machines on which to run a Distributed ANSYS analysis. See
        Starting Distributed ANSYS in the Parallel Processing Guide for
        more information.

    \\-mpi <value>
        Specifies the type of MPI to use.
        See the Parallel Processing Guide for more information.

    \\-mpifile <appfile>
        Specifies an existing MPI file
        Specifies an existing MPI file (appfile) to be used in a
        Distributed ANSYS run. See Using MPI Files in the Parallel
        Processing Guide for more information.

    \\-na <value>
        Specifies the number of GPU accelerator devices
        Number of GPU devices per machine or compute node when running
        with the GPU accelerator feature. See GPU Accelerator Capability
        in the Parallel Processing Guide for more information.

    \\-name <value>
        Defines Mechanical APDL parameters
        Set mechanical APDL parameters at program start-up. The parameter
        name must be at least two characters long. For details about
        parameters, see the ANSYS Parametric Design Language Guide.

    \\-p <productname>
        ANSYS session product
        Defines the ANSYS session product that will run during the
        session. For more detailed information about the ``-p`` option,
        see Selecting an ANSYS Product via the Command Line.

    \\-ppf <license feature name>
        HPC license
        Specifies which HPC license to use during a parallel processing
        run. See HPC Licensing in the Parallel Processing Guide for more
        information.

    \\-smp
        Enables shared-memory parallelism.
        See the Parallel Processing Guide for more information.

    If the environment is configured to use `PyPIM <https://pypim.docs.pyansys.com>`_
    and ``start_instance`` is ``True``, then starting the instance will be delegated to PyPIM.
    In this event, most of the options will be ignored and the server side configuration will
    be used.

    Examples
    --------
    Launch MAPDL using the best protocol.

    >>> from ansys.mapdl.core import launch_mapdl
    >>> mapdl = launch_mapdl()

    Run MAPDL with shared memory parallel and specify the location of
    the Ansys binary.

    >>> exec_file = 'C:/Program Files/ANSYS Inc/v231/ansys/bin/winx64/ANSYS231.exe'
    >>> mapdl = launch_mapdl(exec_file, additional_switches='-smp')

    Connect to an existing instance of MAPDL at IP 192.168.1.30 and
    port 50001.  This is only available using the latest ``'grpc'``
    mode.

    >>> mapdl = launch_mapdl(start_instance=False, ip='192.168.1.30',
    ...                      port=50001)

    Run MAPDL using the console mode (not recommended, and available only on Linux).

    >>> mapdl = launch_mapdl('/ansys_inc/v194/ansys/bin/ansys194',
    ...                       mode='console')

    Run MAPDL with additional environment variables.

    >>> my_env_vars = {"my_var":"true", "ANSYS_LOCK":"FALSE"}
    >>> mapdl = launch_mapdl(add_env_vars=my_env_vars)

    Run MAPDL with our own set of environment variables. It replace the system
    environment variables which otherwise would be used in the process.

    >>> my_env_vars = {"my_var":"true",
        "ANSYS_LOCK":"FALSE",
        "ANSYSLMD_LICENSE_FILE":"1055@MYSERVER"}
    >>> mapdl = launch_mapdl(replace_env_vars=my_env_vars)
    """
    if remove_temp_files is not None:
        warnings.warn(
            "The option ``remove_temp_files`` is being deprecated and it will be removed by PyMAPDL version 0.66.0.\n"
            "Please use ``remove_temp_dir_on_exit`` instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        remove_temp_dir_on_exit = remove_temp_files
        remove_temp_files = None

    if verbose_mapdl is not None:
        raise DeprecationError(
            "The ``verbose_mapdl`` argument is deprecated and will be completely removed in a future release. Use a logger instead. "
            "See https://mapdl.docs.pyansys.com/version/stable/api/logging.html for more details."
        )

    # These parameters are partially used for unit testing
    set_no_abort = kwargs.pop("set_no_abort", True)

    # Extract arguments:
    force_intel = kwargs.pop("force_intel", False)
    broadcast = kwargs.pop("log_broadcast", False)
    if broadcast:
        raise ValueError(
            "The CORBA interface has been deprecated from 0.67."
            "Hence this argument is not valid."
        )
    use_vtk = kwargs.pop("use_vtk", None)
    just_launch = kwargs.pop("just_launch", None)
    _debug_no_launch = kwargs.pop("_debug_no_launch", None)

    # Transferring MAPDL arguments to start_parameters:
    start_parm = {}

    kwargs_keys = list(kwargs.keys())
    for each_par in kwargs_keys:
        if each_par in _ALLOWED_START_PARM:
            start_parm[each_par] = kwargs.pop(each_par)

    # Raising error if using non-allowed arguments
    if kwargs:
        ms_ = ", ".join([f"'{each}'" for each in kwargs.keys()])
        raise ValueError(f"The following arguments are not recognized: {ms_}")

    # Getting IP from env var
    ip_env_var = os.environ.get("PYMAPDL_IP", "")
    if ip_env_var != "":
        if ip:
            warnings.warn(
                "The env var 'PYMAPDL_IP' is set, hence the 'ip' argument is overwritten."
            )

        ip = ip_env_var
        LOG.debug(f"An IP ({ip}) has been set using 'PYMAPDL_IP' env var.")

    ip = None if ip == "" else ip  # Making sure the variable is not empty

    # Getting "start_instance" using "True" as default.
    if (ip is not None) and (start_instance is None):
        # An IP has been supplied. By default, 'start_instance' is equal
        # false, unless it is set through the env vars.
        start_instance = get_start_instance(start_instance=False)
    else:
        start_instance = get_start_instance(start_instance=start_instance)

    LOG.debug("Using 'start_instance' equal to %s.", start_instance)

    if ip is None:
        if ON_WSL:
            ip = _get_windows_host_ip()
            if ip:
                LOG.debug(
                    f"On WSL: Using the following IP address for the Windows OS host: {ip}"
                )
            else:
                raise MapdlDidNotStart(
                    "You seems to be working from WSL.\n"
                    "Unfortunately, PyMAPDL could not find the IP address of the Windows host machine."
                )

        if not ip:
            LOG.debug(
                f"No IP address was supplied. Using the default IP address: {LOCALHOST}"
            )
            ip = LOCALHOST

    else:
        LOG.debug(
            "Because 'PYMAPDL_IP' is not None, an attempt is made to connect to"
            " a remote session ('START_INSTANCE' is set to 'False')."
        )
        if ON_WSL:
            LOG.debug("On WSL: Allowing 'start_instance' and 'ip' arguments together.")
        else:
            if start_instance is True:
                raise ValueError(
                    "When providing a value for the argument 'ip', the argument "
                    "'start_instance' cannot be 'True'.\n"
                    "Make sure the corresponding environment variables are not setting "
                    "those argument values.\n"
                    "For more information visit https://github.com/ansys/pymapdl/issues/2910"
                )

        ip = socket.gethostbyname(ip)  # Converting ip or hostname to ip

    check_valid_ip(ip)  # double check

    if port is None:
        port = int(os.environ.get("PYMAPDL_PORT", MAPDL_DEFAULT_PORT))
        check_valid_port(port)
        LOG.debug(f"Using default port {port}")

    # verify version
    if exec_file and version:
        raise ValueError("Cannot specify both ``exec_file`` and ``version``.")

    if version is None:
        version = os.getenv("PYMAPDL_MAPDL_VERSION", None)

    # Start MAPDL with PyPIM if the environment is configured for it
    # and the user did not pass a directive on how to launch it.
    if _HAS_PIM and exec_file is None and pypim.is_configured():
        LOG.info("Starting MAPDL remotely. The startup configuration will be ignored.")
        if version:
            version = str(version)
        else:
            version = None

        return launch_remote_mapdl(cleanup_on_exit=cleanup_on_exit, version=version)

    version = _verify_version(version)  # return a int version or none

    if start_instance:
        # special handling when building the gallery outside of CI. This
        # creates an instance of mapdl the first time.
        if pymapdl.BUILDING_GALLERY:  # pragma: no cover
            LOG.debug("Building gallery.")
            # launch an instance of pymapdl if it does not already exist and
            # we're allowed to start instances
            if GALLERY_INSTANCE[0] is None:
                LOG.debug("Loading first MAPDL instance for gallery building.")
                GALLERY_INSTANCE[0] = "Loading..."
                mapdl = launch_mapdl(
                    start_instance=True,
                    cleanup_on_exit=False,
                    loglevel=loglevel,
                    set_no_abort=set_no_abort,
                    **start_parm,
                )
                GALLERY_INSTANCE[0] = {"ip": mapdl._ip, "port": mapdl._port}
                return mapdl

            # otherwise, connect to the existing gallery instance if available, but it needs to be fully loaded.
            elif GALLERY_INSTANCE[0] != "Loading...":
                LOG.debug(
                    "Connecting to an existing MAPDL instance for gallery building."
                )
                mapdl = MapdlGrpc(
                    ip=GALLERY_INSTANCE[0]["ip"],
                    port=GALLERY_INSTANCE[0]["port"],
                    cleanup_on_exit=False,
                    loglevel=loglevel,
                    set_no_abort=set_no_abort,
                    use_vtk=use_vtk,
                    **start_parm,
                )
                if clear_on_connect:
                    mapdl.clear()
                return mapdl

            else:
                LOG.debug("Bypassing Gallery building flag for the first time.")

    else:
        LOG.debug("Connecting to an existing instance of MAPDL at %s:%s", ip, port)

        if just_launch:
            print(f"There is an existing MAPDL instance at: {ip}:{port}")
            return

        if _debug_no_launch:
            return pack_parameters(
                port,
                ip,
                add_env_vars,
                replace_env_vars,
                cleanup_on_exit,
                loglevel,
                set_no_abort,
                remove_temp_dir_on_exit,
                log_apdl,
                use_vtk,
                start_parm,
                start_instance,
                version,
            )

        mapdl = MapdlGrpc(
            ip=ip,
            port=port,
            cleanup_on_exit=False,
            loglevel=loglevel,
            set_no_abort=set_no_abort,
            use_vtk=use_vtk,
            **start_parm,
        )
        if clear_on_connect:
            mapdl.clear()
        return mapdl

    # verify executable
    if exec_file is None:
        exec_file = os.getenv("PYMAPDL_MAPDL_EXEC", None)

    if exec_file is None:
        if not _HAS_ATP:
            raise ModuleNotFoundError(
                "If you don't have 'ansys-tools-path' library installed, you need to input the executable path ('exec_path')."
            )

        LOG.debug("Using default executable.")
        # Load cached path
        if _debug_no_launch:
            exec_file = ""
        else:
            exec_file = get_ansys_path(version=version)

        if exec_file is None:
            raise FileNotFoundError(
                "Invalid exec_file path or cannot load cached "
                "mapdl path.  Enter one manually by specifying "
                "exec_file="
            )
    else:  # verify ansys exists at this location
        if not os.path.isfile(exec_file):
            raise FileNotFoundError(
                f'Invalid MAPDL executable at "{exec_file}"\n'
                "Enter one manually using exec_file="
            )

    # verify run location
    if run_location is None:
        LOG.debug("Using default run location.")
        temp_dir = tempfile.gettempdir()
        run_location = os.path.join(temp_dir, "ansys_%s" % random_string(10))
        if not os.path.isdir(run_location):
            try:
                os.mkdir(run_location)
                LOG.debug("Created run location at %s", run_location)
            except:
                raise MapdlRuntimeError(
                    "Unable to create the temporary working "
                    f'directory "{run_location}"\n'
                    "Please specify run_location="
                )
    else:
        if not os.path.isdir(run_location):
            raise FileNotFoundError(f'"{run_location}" is not a valid directory')
        if remove_temp_dir_on_exit:
            LOG.info("`run_location` set. Disabling the removal of temporary files.")
            remove_temp_dir_on_exit = False

    LOG.debug("Using run location at %s", run_location)

    # verify no lock file and the mode is valid
    check_lock_file(run_location, jobname, override)

    if _HAS_ATP and not _debug_no_launch:
        mode = check_mode(mode, version_from_path("mapdl", exec_file))
        LOG.debug("Using mode %s", mode)
    else:
        mode = "grpc"

    # Setting SMP by default if student version is used.
    additional_switches = _force_smp_student_version(additional_switches, exec_file)

    #
    additional_switches = _validate_MPI(
        additional_switches, exec_file, force_intel=force_intel
    )

    additional_switches = _check_license_argument(license_type, additional_switches)
    LOG.debug(f"Using additional switches {additional_switches}.")

    # Setting number of processors
    machine_cores = psutil.cpu_count(logical=False)
    if not nproc:
        if machine_cores < 2:  # default required cores
            nproc = machine_cores  # to avoid starting issues
        else:
            nproc = 2
    else:
        if machine_cores < int(nproc):
            raise NotEnoughResources

    start_parm.update(
        {
            "exec_file": exec_file,
            "run_location": run_location,
            "additional_switches": additional_switches,
            "jobname": jobname,
            "nproc": nproc,
            "print_com": print_com,
        }
    )

    if mode == "console":
        start_parm["start_timeout"] = start_timeout

    else:
        start_parm["ram"] = ram
        start_parm["override"] = override
        start_parm["timeout"] = start_timeout

    LOG.debug(f"Using start parameters {start_parm}")

    # Check the license server
    if license_server_check:
        LOG.debug("Checking license server.")
        lic_check = LicenseChecker(timeout=start_timeout)
        lic_check.start()

    try:
        LOG.debug("Starting MAPDL")
        if mode == "console":
            from ansys.mapdl.core.mapdl_console import MapdlConsole

            mapdl = MapdlConsole(
                loglevel=loglevel, log_apdl=log_apdl, use_vtk=use_vtk, **start_parm
            )

        elif mode == "grpc":
            if _debug_no_launch:
                # Early exit, just for testing
                return pack_parameters(
                    port,
                    ip,
                    add_env_vars,
                    replace_env_vars,
                    cleanup_on_exit,
                    loglevel,
                    set_no_abort,
                    remove_temp_dir_on_exit,
                    log_apdl,
                    use_vtk,
                    start_parm,
                    start_instance,
                    version,
                )

            port, actual_run_location, process = launch_grpc(
                port=port,
                add_env_vars=add_env_vars,
                replace_env_vars=replace_env_vars,
                **start_parm,
            )

            if just_launch:
                out = [ip, port]
                if hasattr(process, "pid"):
                    out += [process.pid]
                return out

            mapdl = MapdlGrpc(
                ip=ip,
                port=port,
                cleanup_on_exit=cleanup_on_exit,
                loglevel=loglevel,
                set_no_abort=set_no_abort,
                remove_temp_dir_on_exit=remove_temp_dir_on_exit,
                log_apdl=log_apdl,
                process=process,
                use_vtk=use_vtk,
                **start_parm,
            )
            if run_location is None:
                mapdl._path = actual_run_location

        # Setting launched property
        mapdl._launched = True

    except Exception as exception:
        # Failed to launch for some reason.  Check if failure was due
        # to the license check
        if license_server_check:
            LOG.debug("Checking license server.")
            lic_check.check()

        raise exception

    # Stopping license checker
    if license_server_check:
        LOG.debug("Stopping license server check.")
        lic_check.is_connected = True

    return mapdl


def check_mode(mode, version):
    """Check if the MAPDL server mode matches the allowable version

    If ``None``, the newest mode will be selected.

    Returns a value from ``ALLOWABLE_MODES``.
    """
    if isinstance(mode, str):
        mode = mode.lower()
        if mode == "grpc":
            if version < 211:
                if version < 202 and os.name == "nt":
                    raise VersionError(
                        "gRPC mode requires MAPDL 2020R2 or newer " "on Windows."
                    )
                elif os.name == "posix":
                    raise VersionError("gRPC mode requires MAPDL 2021R1 or newer.")
        elif mode == "corba":
            raise DeprecationError(
                "The CORBA interface has been deprecated with the"
                " v0.67 release. Please use the gRPC interface instead.\n"
                "For more information visit: "
                "https://mapdl.docs.pyansys.com/version/0.66/getting_started/versioning.html#corba-interface"
            )

        elif mode == "console":
            if os.name == "nt":
                raise ValueError("Console mode requires Linux.")
            if version >= 211:
                warnings.warn(
                    "Console mode not recommended in MAPDL 2021R1 or newer.\n"
                    "Recommend using gRPC mode instead."
                )
        else:
            raise ValueError(
                f'Invalid MAPDL server mode "{mode}".\n\n'
                f"Use one of the following modes:\n{ALLOWABLE_MODES}"
            )

    else:  # auto-select based on best version
        if version >= 211:
            mode = "grpc"
        elif version == 202 and os.name == "nt":
            # Windows supports it as of 2020R2
            mode = "grpc"
        else:
            if os.name == "nt":
                raise VersionError(
                    "Running MAPDL as a service requires "
                    "MAPDL 2020R2 or greater on Windows."
                )
            mode = "console"

    if version < 130:
        warnings.warn("MAPDL as a service has not been tested on MAPDL < v13")
        mode = "console"

    return mode


def update_env_vars(add_env_vars, replace_env_vars):
    """
    Update environment variables for the MAPDL process.

    Parameters
    ----------
    add_env_vars : dict, None
        Dictionary with a mapping of env variables.
    replace_env_vars : dict, None
        Dictionary with a mapping of env variables.

    Raises
    ------
    TypeError
        'add_env_vars' and 'replace_env_vars' are incompatible. Please provide only one.
    TypeError
        The variable 'add_env_vars' should be a dict with env vars.
    TypeError
        The variable 'replace_env_vars' should be a dict with env vars.
    """

    # Expanding/replacing env variables for the process.
    if add_env_vars and replace_env_vars:
        raise ValueError(
            "'add_env_vars' and 'replace_env_vars' are incompatible. Please provide only one."
        )

    elif add_env_vars:
        if not isinstance(add_env_vars, dict):
            raise TypeError(
                "The variable 'add_env_vars' should be a dict with env vars."
            )

        add_env_vars.update(os.environ)
        LOG.debug(f"Updating environment variables with: {add_env_vars}")
        return add_env_vars

    elif replace_env_vars:
        if not isinstance(replace_env_vars, dict):
            raise TypeError(
                "The variable 'replace_env_vars' should be a dict with env vars."
            )
        LOG.debug(f"Replacing environment variables with: {replace_env_vars}")
        return replace_env_vars


def _check_license_argument(license_type, additional_switches):
    if isinstance(license_type, str):
        # In newer license server versions an invalid license name just get discarded and produces no effect or warning.
        # For example:
        # ```bash
        # mapdl.exe -p meba    # works fine because 'meba' is a valid license in ALLOWABLE_LICENSES.
        # mapdl.exe -p yoyoyo  # The -p flag is ignored and it run the default license.
        # ```
        #
        # In older versions probably it might raise an error. But not sure.
        license_type = license_type.lower().strip()

        if "enterprise" in license_type and "solver" not in license_type:
            license_type = "ansys"

        elif "enterprise" in license_type and "solver" in license_type:
            license_type = "meba"

        elif "premium" in license_type:
            license_type = "mech_2"

        elif "pro" in license_type:
            license_type = "mech_1"

        elif license_type not in ALLOWABLE_LICENSES:
            allow_lics = [f"'{each}'" for each in ALLOWABLE_LICENSES]
            warn_text = (
                f"The keyword argument 'license_type' value ('{license_type}') is not a recognized\n"
                "license name or has been deprecated.\n"
                "Still PyMAPDL will try to use it but in older versions you might experience\n"
                "problems connecting to the server.\n"
                f"Recognized license names: {' '.join(allow_lics)}"
            )
            warnings.warn(warn_text, UserWarning)

        additional_switches += " -p " + license_type
        LOG.debug(
            f"Using specified license name '{license_type}' in the 'license_type' keyword argument."
        )

    elif "-p " in additional_switches:
        # There is already a license request in additional switches.
        license_type = re.findall(r"-p\s+\b(\w*)", additional_switches)[
            0
        ]  # getting only the first product license.

        if license_type not in ALLOWABLE_LICENSES:
            allow_lics = [f"'{each}'" for each in ALLOWABLE_LICENSES]
            warn_text = (
                f"The additional switch product value ('-p {license_type}') is not a recognized\n"
                "license name or has been deprecated.\n"
                "Still PyMAPDL will try to use it but in older versions you might experience\n"
                "problems connecting to the server.\n"
                f"Recognized license names: {' '.join(allow_lics)}"
            )
            warnings.warn(warn_text, UserWarning)
            LOG.warning(warn_text)

        LOG.debug(
            f"Using specified license name '{license_type}' in the additional switches parameter."
        )

    elif license_type is not None:
        raise TypeError("The argument 'license_type' does only accept str or None.")

    return additional_switches


def _verify_version(version):
    """Verify the MAPDL version is valid."""
    if isinstance(version, float):
        version = int(version * 10)

    if isinstance(version, str):
        if version.lower().strip() == "latest":
            return None  # Default behaviour is latest

        elif version.upper().strip() in [
            str(each) for each in SUPPORTED_ANSYS_VERSIONS.keys()
        ]:
            version = int(version)
        elif version.upper().strip() in [
            str(each / 10) for each in SUPPORTED_ANSYS_VERSIONS.keys()
        ]:
            version = int(float(version) * 10)
        elif version.upper().strip() in SUPPORTED_ANSYS_VERSIONS.values():
            version = [
                key
                for key, value in SUPPORTED_ANSYS_VERSIONS.items()
                if value == version.upper().strip()
            ][0]

    if version is not None and version not in SUPPORTED_ANSYS_VERSIONS.keys():
        raise ValueError(
            f"MAPDL version must be one of the following: {list(SUPPORTED_ANSYS_VERSIONS.keys())}"
        )

    return version


def _get_windows_host_ip():
    output = _run_ip_route()
    if output:
        return _parse_ip_route(output)


def _run_ip_route():
    from subprocess import run

    try:
        p = run(["ip", "route"], capture_output=True)
    except Exception:
        LOG.debug(
            "Detecting the IP address of the host Windows machine requires being able to execute the command 'ip route'."
        )
        return None

    if p and p.stdout and isinstance(p.stdout, bytes):
        return p.stdout.decode()


def _parse_ip_route(output):
    match = re.findall(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*", output)

    if match:
        return match[0]


def pack_parameters(
    port,
    ip,
    add_env_vars,
    replace_env_vars,
    cleanup_on_exit,
    loglevel,
    set_no_abort,
    remove_temp_dir_on_exit,
    log_apdl,
    use_vtk,
    start_parm,
    start_instance,
    version,
):
    # pack all the arguments in a dict for debugging purposes
    dict_ = {}
    dict_["port"] = port
    dict_["ip"] = ip
    dict_["add_env_vars"] = add_env_vars
    dict_["replace_env_vars"] = replace_env_vars
    dict_["cleanup_on_exit"] = cleanup_on_exit
    dict_["loglevel"] = loglevel
    dict_["set_no_abort"] = set_no_abort
    dict_["remove_temp_dir_on_exit"] = remove_temp_dir_on_exit
    dict_["log_apdl"] = log_apdl
    dict_["use_vtk"] = use_vtk
    dict_["start_parm"] = start_parm
    dict_["start_instance"] = start_instance
    dict_["version"] = version
    return dict_
