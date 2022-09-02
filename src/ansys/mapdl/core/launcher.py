"""Module for launching MAPDL locally or connecting to a remote instance with gRPC."""

import atexit
from glob import glob
import os
import platform
import re
import socket
import subprocess
import tempfile
import time
import warnings

try:
    import ansys.platform.instancemanagement as pypim

    _HAS_PIM = True
except ModuleNotFoundError:  # pragma: no cover
    _HAS_PIM = False

import appdirs

from ansys.mapdl import core as pymapdl
from ansys.mapdl.core import LOG
from ansys.mapdl.core._version import SUPPORTED_ANSYS_VERSIONS
from ansys.mapdl.core.errors import LockFileException, MapdlDidNotStart, VersionError
from ansys.mapdl.core.licensing import ALLOWABLE_LICENSES, LicenseChecker
from ansys.mapdl.core.mapdl import _MapdlCore
from ansys.mapdl.core.mapdl_grpc import MAX_MESSAGE_LENGTH, MapdlGrpc
from ansys.mapdl.core.misc import (
    check_valid_ip,
    check_valid_port,
    check_valid_start_instance,
    create_temp_dir,
    is_float,
    random_string,
    threaded,
)

# settings directory
SETTINGS_DIR = appdirs.user_data_dir("ansys_mapdl_core")
if not os.path.isdir(SETTINGS_DIR):
    try:
        os.makedirs(SETTINGS_DIR)
    except:
        warnings.warn(
            "Unable to create settings directory.\n"
            "Will be unable to cache MAPDL executable location"
        )

CONFIG_FILE = os.path.join(SETTINGS_DIR, "config.txt")
ALLOWABLE_MODES = ["corba", "console", "grpc"]

LOCALHOST = "127.0.0.1"
MAPDL_DEFAULT_PORT = 50052

INTEL_MSG = """Due to incompatibilities between 'DMP', Windows and VPN connections,
the flat '-mpi INTELMPI' is overwritten by '-mpi msmpi'.

If you still want to use 'INTEL', set:

launch_mapdl(..., force_intel=True, additional_switches='-mpi INTELMPI')

Be aware of possible errors or unexpected behavior with this configuration.
"""

GALLERY_INSTANCE = [None]


def _cleanup_gallery_instance():  # pragma: no cover
    """This cleans up any left over instances of MAPDL from building the gallery."""
    if GALLERY_INSTANCE[0] is not None:
        mapdl = MapdlGrpc(
            ip=GALLERY_INSTANCE[0]["ip"],
            port=GALLERY_INSTANCE[0]["port"],
        )
        mapdl.exit(force=True)


atexit.register(_cleanup_gallery_instance)


def _is_ubuntu():
    """Determine if running as Ubuntu.

    It's a bit complicated because sometimes the distribution is
    Ubuntu, but the kernel has been recompiled and no longer has the
    word "ubuntu" in it.

    """
    # must be running linux for this to be True
    if os.name != "posix":
        return False

    # gcc is installed by default
    proc = subprocess.Popen("gcc --version", shell=True, stdout=subprocess.PIPE)
    if "ubuntu" in proc.stdout.read().decode().lower():
        return True

    # try lsb_release as this is more reliable
    try:
        import lsb_release

        if lsb_release.get_distro_information()["ID"].lower() == "ubuntu":
            return True
    except ImportError:
        # finally, check platform
        return "ubuntu" in platform.platform().lower()


def _version_from_path(path):
    """Extract ansys version from a path.  Generally, the version of
    ANSYS is contained in the path:

    C:/Program Files/ANSYS Inc/v202/ansys/bin/win64/ANSYS202.exe

    /usr/ansys_inc/v211/ansys/bin/mapdl

    Note that if the MAPDL executable, you have to rely on the version
    in the path.

    Parameters
    ----------
    path : str
        Path to the MAPDL executable

    Returns
    -------
    int
        Integer version number (e.g. 211).

    """
    # expect v<ver>/ansys
    # replace \\ with / to account for possible windows path
    matches = re.findall(r"v(\d\d\d).ansys", path.replace("\\", "/"), re.IGNORECASE)
    if not matches:
        raise RuntimeError(f"Unable to extract Ansys version from {path}")
    return int(matches[-1])


def close_all_local_instances(port_range=None):
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
    def close_mapdl(port, name="Closing mapdl thread."):
        try:
            mapdl = MapdlGrpc(port=port, set_no_abort=False)
            mapdl.exit()
        except OSError:
            pass

    ports = check_ports(port_range)
    for port, state in ports.items():
        if state:
            close_mapdl(port)


def check_ports(port_range, ip="localhost"):
    """Check the state of ports in a port range"""
    ports = {}
    for port in port_range:
        ports[port] = port_in_use(port, ip)
    return ports


def port_in_use(port, host=LOCALHOST):
    """Returns True when a port is in use at the given host.

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


def create_ip_file(ip, path):
    """Create 'mylocal.ip' file required for ansys to change the IP of the gRPC server."""

    file_name = os.path.join(path, "mylocal.ip")
    with open(file_name, "w") as f:
        f.write(ip)


def launch_grpc(
    exec_file="",
    jobname="file",
    nproc=2,
    ram=None,
    run_location=None,
    port=MAPDL_DEFAULT_PORT,
    ip=LOCALHOST,
    additional_switches="",
    override=True,
    timeout=20,
    verbose=False,
    add_env_vars=None,
    replace_env_vars=None,
    **kwargs,
) -> tuple:  # pragma: no cover
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

    custom_bin : str, optional
        Path to the MAPDL custom executable.

    override : bool, optional
        Attempts to delete the lock file at the run_location.
        Useful when a prior MAPDL session has exited prematurely and
        the lock file has not been deleted.

    verbose : bool, optional
        Print all output when launching and running MAPDL.  Not
        recommended unless debugging the MAPDL start.  Default
        ``False``.

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

    >>> exec_file = 'C:/Program Files/ANSYS Inc/v202/ansys/bin/win64/ANSYS202.exe'
    >>> mapdl = launch_mapdl(exec_file, additional_switches='-smp')

    """
    # disable all MAPDL pop-up errors:
    os.environ["ANS_CMD_NODIAG"] = "TRUE"

    # use temporary directory if run_location is unspecified
    if run_location is None:
        run_location = create_temp_dir()
    elif not os.path.isdir(run_location):
        os.mkdir(run_location)

    if not os.access(run_location, os.W_OK):
        raise IOError('Unable to write to ``run_location`` "%s"' % run_location)

    # verify version
    if _version_from_path(exec_file) < 202:
        raise VersionError("The MAPDL gRPC interface requires MAPDL 20.2 or later")

    # verify lock file does not exist
    check_lock_file(run_location, jobname, override)

    # get the next available port
    if port is None:
        if not pymapdl._LOCAL_PORTS:
            port = MAPDL_DEFAULT_PORT
        else:
            port = max(pymapdl._LOCAL_PORTS) + 1

    while port_in_use(port) or port in pymapdl._LOCAL_PORTS:
        port += 1
    pymapdl._LOCAL_PORTS.append(port)

    # setting ip for the grpc server
    if ip != LOCALHOST:  # Default local ip is 127.0.0.1
        create_ip_file(ip, run_location)

    cpu_sw = "-np %d" % nproc

    if ram:
        ram_sw = "-m %d" % int(1024 * ram)
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

    env_vars = update_env_vars(add_env_vars, replace_env_vars)

    LOG.info(f"Running in {ip}:{port} the following command: '{command}'")

    if verbose:  # pragma: no cover
        subprocess.Popen(command, shell=os.name != "nt", cwd=run_location, env=env_vars)

    else:
        subprocess.Popen(
            command,
            shell=os.name != "nt",
            cwd=run_location,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            env=env_vars,
        )

    # watch for the creation of temporary files at the run_directory.
    # This lets us know that the MAPDL process has at least started
    sleep_time = 0.1
    for _ in range(int(timeout / sleep_time)):
        # check if any error files have been created.  This is
        # more reliable than using the lock file

        files = os.listdir(run_location)
        has_ans = any([filename for filename in files if ".err" in filename])
        if has_ans:
            LOG.info("MAPDL session successfully started (Error file found)")
            break
        time.sleep(sleep_time)

    if not has_ans:
        raise MapdlDidNotStart(
            f"MAPDL failed to start (No err file generated in '{run_location}')"
        )

    return port, run_location


def launch_remote_mapdl(
    version=None,
    cleanup_on_exit=True,
) -> _MapdlCore:
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
    ansys.mapdl.core.mapdl._MapdlCore
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
        channel=channel, cleanup_on_exit=cleanup_on_exit, remote_instance=instance
    )


def get_start_instance(start_instance_default=True):
    """Check if the environment variable ``PYMAPDL_START_INSTANCE`` exists and is valid.

    Parameters
    ----------
    start_instance_default : bool
        Value to return when ``PYMAPDL_START_INSTANCE`` is unset.

    Returns
    -------
    bool
        ``True`` when the ``PYMAPDL_START_INSTANCE`` environment variable is
        true, ``False`` when PYMAPDL_START_INSTANCE is false. If unset,
        returns ``start_instance_default``.

    Raises
    ------
    OSError
        Raised when ``PYMAPDL_START_INSTANCE`` is not either true or false
        (case independent).

    """
    if "PYMAPDL_START_INSTANCE" in os.environ:
        if os.environ["PYMAPDL_START_INSTANCE"].lower() not in ["true", "false"]:
            val = os.environ["PYMAPDL_START_INSTANCE"]
            raise OSError(
                f'Invalid value "{val}" for PYMAPDL_START_INSTANCE\n'
                'PYMAPDL_START_INSTANCE should be either "TRUE" or "FALSE"'
            )
        return os.environ["PYMAPDL_START_INSTANCE"].lower() == "true"
    return start_instance_default


def _get_available_base_ansys():
    """Return a dictionary of available Ansys versions with their base paths.

    Notes
    -----

    On Windows, It uses the environment variable ``AWP_ROOTXXX``.

    The student versions are returned at the end of the dict and with negative value for the version.

    Returns
    -------
    Return all installed Ansys paths in Windows.

    >>> _get_available_base_ansys()
    {222: 'C:\\Program Files\\ANSYS Inc\\v222',
     212: 'C:\\Program Files\\ANSYS Inc\\v212',
     -222: 'C:\\Program Files\\ANSYS Inc\\ANSYS Student\\v222'}

    Return all installed Ansys paths in Linux.

    >>> _get_available_base_ansys()
    {194: '/usr/ansys_inc/v194',
     202: '/usr/ansys_inc/v202',
     211: '/usr/ansys_inc/v211'}
    """
    base_path = None
    if os.name == "nt":  # pragma: no cover
        supported_versions = SUPPORTED_ANSYS_VERSIONS
        # The student version overwrites the AWP_ROOT env var (if it is installed later)
        # However the priority should be given to the non-student version.
        awp_roots = []
        awp_roots_student = []

        for ver in supported_versions:
            path_ = os.environ.get(f"AWP_ROOT{ver}", "")
            path_non_student = path_.replace("\\ANSYS Student", "")

            if "student" in path_.lower() and os.path.exists(path_non_student):
                # Check if also exist a non-student version
                awp_roots.append([ver, path_non_student])
                awp_roots_student.insert(0, [-1 * ver, path_])

            else:
                awp_roots.append([ver, path_])

        awp_roots.extend(awp_roots_student)
        installed_versions = {
            ver: path for ver, path in awp_roots if path and os.path.isdir(path)
        }

        if installed_versions:
            return installed_versions
        else:  # pragma: no cover
            LOG.debug(
                "No installed ANSYS found using 'AWP_ROOT' environments. Let's suppose a base path."
            )
            base_path = os.path.join(os.environ["PROGRAMFILES"], "ANSYS INC")
            if not os.path.exists(base_path):
                LOG.debug(
                    f"The supposed 'base_path'{base_path} does not exist. No available ansys found."
                )
                return {}
    elif os.name == "posix":
        for path in ["/usr/ansys_inc", "/ansys_inc"]:
            if os.path.isdir(path):
                base_path = path
    else:  # pragma: no cover
        raise OSError(f"Unsupported OS {os.name}")

    if base_path is None:
        return {}

    paths = glob(os.path.join(base_path, "v*"))

    # Testing for ANSYS STUDENT version
    if not paths:  # pragma: no cover
        paths = glob(os.path.join(base_path, "ANSYS*"))

    if not paths:
        return {}

    ansys_paths = {}
    for path in paths:
        ver_str = path[-3:]
        if is_float(ver_str):
            ansys_paths[int(ver_str)] = path

    return ansys_paths


def get_available_ansys_installations():
    """Return a dictionary of available Ansys versions with their base paths.

    Notes
    -----

    On Windows, It uses the environment variable ``AWP_ROOTXXX``.

    The student versions are returned at the end of the dict and with negative value for the version.

    Returns
    -------
    Return all installed Ansys paths in Windows.

    >>> get_available_ansys_installations()
    {222: 'C:\\Program Files\\ANSYS Inc\\v222',
     212: 'C:\\Program Files\\ANSYS Inc\\v212',
     -222: 'C:\\Program Files\\ANSYS Inc\\ANSYS Student\\v222'}

    Return all installed Ansys paths in Linux.

    >>> get_available_ansys_installations()
    {194: '/usr/ansys_inc/v194',
     202: '/usr/ansys_inc/v202',
     211: '/usr/ansys_inc/v211'}
    """
    return _get_available_base_ansys()


def find_ansys():
    """Searches for ansys path within the standard install location
    and returns the path of the latest version.

    Returns
    -------
    ansys_path : str
        Full path to ANSYS executable.

    version : float
        Version float.  For example, 21.1 corresponds to 2021R1.

    Examples
    --------
    Within Windows

    >>> from ansys.mapdl.core.launcher import find_ansys
    >>> find_ansys()
    'C:/Program Files/ANSYS Inc/v211/ANSYS/bin/winx64/ansys211.exe', 21.1

    Within Linux

    >>> find_ansys()
    (/usr/ansys_inc/v211/ansys/bin/ansys211, 21.1)
    """
    versions = _get_available_base_ansys()
    if not versions:
        return "", ""
    version = max(versions.keys())
    ans_path = versions[version]
    version = abs(version)
    if os.name == "nt":
        ansys_bin = os.path.join(
            ans_path, "ansys", "bin", "winx64", f"ansys{version}.exe"
        )
    else:
        ansys_bin = os.path.join(ans_path, "ansys", "bin", f"ansys{version}")
    return ansys_bin, version / 10


def get_ansys_path(allow_input=True):
    """Acquires ANSYS Path from a cached file or user input"""
    exe_loc = None
    if os.path.isfile(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            exe_loc = f.read()
        # verify
        if not os.path.isfile(exe_loc) and allow_input:
            exe_loc = save_ansys_path()
    elif allow_input:  # create configuration file
        exe_loc = save_ansys_path()
    if exe_loc is None:
        exe_loc = find_ansys()[0]
        if not exe_loc:
            exe_loc = None

    return exe_loc


def check_valid_ansys():
    """Checks if a valid version of ANSYS is installed and preconfigured"""
    ansys_bin = get_ansys_path(allow_input=False)
    if ansys_bin is not None:
        version = _version_from_path(ansys_bin)
        return not (version < 170 and os.name != "posix")
    return False


def change_default_ansys_path(exe_loc):
    """Change your default ansys path.

    Parameters
    ----------
    exe_loc : str
        Ansys executable path.  Must be a full path.

    Examples
    --------
    Change default Ansys location on Linux

    >>> from ansys.mapdl.core import launcher
    >>> launcher.change_default_ansys_path('/ansys_inc/v201/ansys/bin/ansys201')
    >>> launcher.get_ansys_path()
    '/ansys_inc/v201/ansys/bin/ansys201'

    Change default Ansys location on Windows

    >>> ans_pth = 'C:/Program Files/ANSYS Inc/v193/ansys/bin/win64/ANSYS193.exe'
    >>> launcher.change_default_ansys_path(ans_pth)
    >>> launcher.check_valid_ansys()
    True

    """
    if os.path.isfile(exe_loc):
        with open(CONFIG_FILE, "w") as f:
            f.write(exe_loc)
    else:
        raise FileNotFoundError("File %s is invalid or does not exist" % exe_loc)


def save_ansys_path(exe_loc=None):  # pragma: no cover
    """Find MAPDL's path or query user.

    If no ``exe_loc`` argument is supplied, this function attempt
    to obtain the MAPDL executable from (and in order):

    - The default ansys paths (i.e. ``'C:/Program Files/Ansys Inc/vXXX/ansys/bin/ansysXXX'``)
    - The configuration file
    - User input

    If ``exe_loc`` is supplied, this function does some checks.
    If successful, it will write that ``exe_loc`` into the config file.

    Parameters
    ----------
    exe_loc : str, optional
        Path of the MAPDL executable ('ansysXXX'), by default ``None``.

    Returns
    -------
    str
        Path of the MAPDL executable.

    Notes
    -----
    The configuration file location (``config.txt``) can be found in
    ``appdirs.user_data_dir("ansys_mapdl_core")``. For example:

    .. code:: python

        >>> import appdirs
        >>> import os
        >>> print(os.path.join(appdirs.user_data_dir("ansys_mapdl_core"), "config.txt"))
        C:/Users/user/AppData/Local/ansys_mapdl_core/ansys_mapdl_core/config.txt

    Examples
    --------
    You can change the default ``exe_loc`` either by modifying the mentioned
    ``config.txt`` file or by executing:

    >>> from ansys.mapdl.core import save_ansys_path
    >>> save_ansys_path('/new/path/to/executable')

    """
    if exe_loc is None:
        exe_loc, _ = find_ansys()

    if is_valid_executable_path(exe_loc):  # pragma: not cover
        if not is_common_executable_path(exe_loc):
            warn_uncommon_executable_path(exe_loc)

        change_default_ansys_path(exe_loc)
        return exe_loc

    if exe_loc is not None:
        if is_valid_executable_path(exe_loc):
            return exe_loc  # pragma: no cover

    # otherwise, query user for the location
    print("Cached ANSYS executable not found")
    print(
        "You are about to enter manually the path of the ANSYS MAPDL executable (ansysXXX, where XXX is the version"
        "This file is very likely to contained in path ending in 'vXXX/ansys/bin/ansysXXX', but it is not required.\n"
        "\nIf you experience problems with the input path you can overwrite the configuration file by typing:\n"
        ">>> from ansys.mapdl.core.launcher import save_ansys_path\n"
        ">>> save_ansys_path('/new/path/to/executable/')\n"
    )
    need_path = True
    while need_path:  # pragma: no cover
        exe_loc = input("Enter the location of an ANSYS executable (ansysXXX):")

        if is_valid_executable_path(exe_loc):
            if not is_common_executable_path(exe_loc):
                warn_uncommon_executable_path(exe_loc)
            with open(CONFIG_FILE, "w") as f:
                f.write(exe_loc)
            need_path = False
        else:
            print(
                "The supplied path is either: not a valid file path, or does not match 'ansysXXX' name."
            )

    return exe_loc


def is_valid_executable_path(exe_loc):  # pragma: no cover
    return (
        os.path.isfile(exe_loc)
        and re.search("ansys\d\d\d", os.path.basename(os.path.normpath(exe_loc)))
        is not None
    )


def is_common_executable_path(exe_loc):  # pragma: no cover
    path = os.path.normpath(exe_loc)
    path = path.split(os.sep)
    if (
        re.search("v(\d\d\d)", exe_loc) is not None
        and re.search("ansys(\d\d\d)", exe_loc) is not None
    ):
        equal_version = (
            re.search("v(\d\d\d)", exe_loc)[1] == re.search("ansys(\d\d\d)", exe_loc)[1]
        )
    else:
        equal_version = False

    return (
        is_valid_executable_path(exe_loc)
        and re.search("v\d\d\d", exe_loc)
        and "ansys" in path
        and "bin" in path
        and equal_version
    )


def warn_uncommon_executable_path(exe_loc):  # pragma: no cover
    warnings.warn(
        f"The supplied path ('{exe_loc}') does not match the usual ansys executable path style"
        "('directory/vXXX/ansys/bin/ansysXXX'). "
        "You might have problems at later use."
    )


def check_lock_file(path, jobname, override):
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
            except PermissionError:
                raise LockFileException(
                    "Unable to remove lock file.  "
                    "Another instance of MAPDL might be "
                    f"running at '{path}'"
                )


def _validate_add_sw(add_sw, exec_path, force_intel=False):
    """Validate additional switches.

    Parameters
    ----------
    add_sw : str
        Additional swtiches.
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
    add_sw = add_sw.lower()

    # known issues with distributed memory parallel (DMP)
    if "smp" not in add_sw:  # pragma: no cover
        # Ubuntu ANSYS fails to launch without I_MPI_SHM_LMT
        if _is_ubuntu():
            os.environ["I_MPI_SHM_LMT"] = "shm"
        if os.name == "nt" and not force_intel:
            # Workaround to fix a problem when launching ansys in 'dmp' mode in the
            # recent windows version and using VPN.
            #
            # There doesn't appear to be an easy way to check if we
            # are running VPN in Windows in python, it seems we will
            # need to know a local address where to ping but that will
            # change for each client/person using the VPN.
            #
            # Adding '-mpi msmpi' to the launch parameter fix it.

            if "intelmpi" in add_sw:
                # Remove intel flag.
                regex = "(-mpi)( *?)(intelmpi)"
                add_sw = re.sub(regex, "", add_sw)
                warnings.warn(INTEL_MSG)

            if _version_from_path(exec_path) >= 210:
                add_sw += " -mpi msmpi"

    return add_sw


def launch_mapdl(
    exec_file=None,
    run_location=None,
    jobname="file",
    nproc=2,
    ram=None,
    mode=None,
    override=False,
    loglevel="ERROR",
    additional_switches="",
    start_timeout=120,
    port=None,
    cleanup_on_exit=True,
    start_instance=None,
    ip=None,
    clear_on_connect=True,
    log_apdl=None,
    remove_temp_files=False,
    verbose_mapdl=False,
    license_server_check=True,
    license_type=None,
    print_com=False,
    add_env_vars=None,
    replace_env_vars=None,
    **kwargs,
) -> _MapdlCore:
    """Start MAPDL locally.

    Parameters
    ----------
    exec_file : str, optional
        The location of the MAPDL executable.  Will use the cached
        location when left at the default ``None``.

    run_location : str, optional
        MAPDL working directory.  Defaults to a temporary working
        directory.  If directory doesn't exist, will create one.

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
        - ``'corba'``
        - ``'console'``

        The ``'grpc'`` mode is available on ANSYS 2021R1 or newer and
        provides the best performance and stability.  The ``'corba'``
        mode is available from v17.0 and newer and is given legacy
        support.  This mode requires the additional
        ``ansys_corba`` module.  Finally, the ``'console'`` mode
        is for legacy use only Linux only prior to v17.0.  This console
        mode is pending depreciation.

    override : bool, optional
        Attempts to delete the lock file at the run_location.
        Useful when a prior MAPDL session has exited prematurely and
        the lock file has not been deleted.

    loglevel : str, optional
        Sets which messages are printed to the console.  ``'INFO'``
        prints out all ANSYS messages, ``'WARNING``` prints only
        messages containing ANSYS warnings, and ``'ERROR'`` logs only
        error messages.

    additional_switches : str, optional
        Additional switches for MAPDL, for example ``'aa_r'``, the
        academic research license, would be added with:

        - ``additional_switches="-aa_r"``

        Avoid adding switches like -i -o or -b as these are already
        included to start up the MAPDL server.  See the notes
        section for additional details.

    start_timeout : float, optional
        Maximum allowable time to connect to the MAPDL server.

    port : int
        Port to launch MAPDL gRPC on.  Final port will be the first
        port available after (or including) this port.  Defaults to
        50052.  You can also override the default behavior of this
        keyword argument with the environment variable
        ``PYMAPDL_PORT=<VALID PORT>``

    custom_bin : str, optional
        Path to the MAPDL custom executable.  On release 2020R2 on
        Linux, if ``None``, will check to see if you have
        ``ansys.mapdl_bin`` installed and use that executable.

    cleanup_on_exit : bool, optional
        Exit MAPDL when python exits or the mapdl Python instance is
        garbage collected.

    start_instance : bool, optional
        When False, connect to an existing MAPDL instance at ``ip``
        and ``port``, which default to ``'127.0.0.1'`` at 50052.
        Otherwise, launch a local instance of MAPDL.  You can also
        override the default behavior of this keyword argument with
        the environment variable ``PYMAPDL_START_INSTANCE=FALSE``.

    ip : bool, optional
        Used only when ``start_instance`` is ``False``. If provided,
        it will force ``start_instance`` to be ``False``.
        You can also provide a hostname as an alternative to an IP address.
        Defaults to ``'127.0.0.1'``. You can also override the
        default behavior of this keyword argument with the
        environment variable "PYMAPDL_IP=FALSE".

    clear_on_connect : bool, optional
        Defaults to ``True``, giving you a fresh environment when
        connecting to MAPDL. When if ``start_instance`` is specified
        it defaults to ``False``.

    log_apdl : str, optional
        Enables logging every APDL command to the local disk.  This
        can be used to "record" all the commands that are sent to
        MAPDL via PyMAPDL so a script can be run within MAPDL without
        PyMAPDL. This string is the path of the output file (e.g.
        ``log_apdl='pymapdl_log.txt'``). By default this is disabled.

    remove_temp_files : bool, optional
        When ``run_location`` is ``None``, this launcher creates a new MAPDL
        working directory within the user temporary directory, obtainable with
        ``tempfile.gettempdir()``. When this parameter is
        ``True``, this directory will be deleted when MAPDL is exited. Default
        ``False``.

    verbose_mapdl : bool, optional
        Enable printing of all output when launching and running
        MAPDL.  This should be used for debugging only as output can
        be tracked within pymapdl.  Default ``False``.

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
        The provided dictionary will be used to extend the system or process
        environment variables. If you want to control all of the environment
        variables, use ``replace_env_vars``. Defaults to ``None``.

    replace_env_vars : dict, optional
        The provided dictionary will be used to replace all the system or process
        environment variables. To just add some environment variables to the MAPDL
        process, use ``add_env_vars``. Defaults to ``None``.

    Returns
    -------
    ansys.mapdl.core.mapdl._MapdlCore
        An instance of Mapdl.  Type depends on the selected ``mode``.

    Notes
    -----
    These are the MAPDL switch options as of 2020R2 applicable for
    running MAPDL as a service via gRPC.  Excluded switches such as
    ``"-j"`` either not applicable or are set via keyword arguments.

    \-acc <device>
        Enables the use of GPU hardware.  See GPU
        Accelerator Capability in the Parallel Processing Guide for more
        information.

    \-amfg
        Enables the additive manufacturing capability.  Requires
        an additive manufacturing license. For general information about
        this feature, see AM Process Simulation in ANSYS Workbench.

    \-ansexe <executable>
        Activates a custom mechanical APDL executable.
        In the ANSYS Workbench environment, activates a custom
        Mechanical APDL executable.

    \-custom <executable>
        Calls a custom Mechanical APDL executable
        See Running Your Custom Executable in the Programmer's Reference
        for more information.

    \-db value
        Initial memory allocation
        Defines the portion of workspace (memory) to be used as the
        initial allocation for the database. The default is 1024
        MB. Specify a negative number to force a fixed size throughout
        the run; useful on small memory systems.

    \-dis
        Enables Distributed ANSYS
        See the Parallel Processing Guide for more information.

    \-dvt
        Enables ANSYS DesignXplorer advanced task (add-on).
        Requires DesignXplorer.

    \-l <language>
        Specifies a language file to use other than English
        This option is valid only if you have a translated message file
        in an appropriately named subdirectory in
        ``/ansys_inc/v201/ansys/docu`` or
        ``Program Files\\ANSYS\\Inc\\V201\\ANSYS\\docu``

    \-m <workspace>
        Specifies the total size of the workspace
        Workspace (memory) in megabytes used for the initial
        allocation. If you omit the ``-m`` option, the default is 2 GB
        (2048 MB). Specify a negative number to force a fixed size
        throughout the run.

    \-machines <IP>
        Specifies the distributed machines
        Machines on which to run a Distributed ANSYS analysis. See
        Starting Distributed ANSYS in the Parallel Processing Guide for
        more information.

    \-mpi <value>
        Specifies the type of MPI to use.
        See the Parallel Processing Guide for more information.

    \-mpifile <appfile>
        Specifies an existing MPI file
        Specifies an existing MPI file (appfile) to be used in a
        Distributed ANSYS run. See Using MPI Files in the Parallel
        Processing Guide for more information.

    \-na <value>
        Specifies the number of GPU accelerator devices
        Number of GPU devices per machine or compute node when running
        with the GPU accelerator feature. See GPU Accelerator Capability
        in the Parallel Processing Guide for more information.

    \-name <value>
        Defines Mechanical APDL parameters
        Set mechanical APDL parameters at program start-up. The parameter
        name must be at least two characters long. For details about
        parameters, see the ANSYS Parametric Design Language Guide.

    \-p <productname>
        ANSYS session product
        Defines the ANSYS session product that will run during the
        session. For more detailed information about the ``-p`` option,
        see Selecting an ANSYS Product via the Command Line.

    \-ppf <license feature name>
        HPC license
        Specifies which HPC license to use during a parallel processing
        run. See HPC Licensing in the Parallel Processing Guide for more
        information.

    \-smp
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

    >>> exec_file = 'C:/Program Files/ANSYS Inc/v201/ansys/bin/win64/ANSYS201.exe'
    >>> mapdl = launch_mapdl(exec_file, additional_switches='-smp')

    Connect to an existing instance of MAPDL at IP 192.168.1.30 and
    port 50001.  This is only available using the latest ``'grpc'``
    mode.

    >>> mapdl = launch_mapdl(start_instance=False, ip='192.168.1.30',
    ...                      port=50001)

    Force the usage of the CORBA protocol.

    >>> mapdl = launch_mapdl(mode='corba')

    Run MAPDL using the console mode (available only on Linux).

    >>> mapdl = launch_mapdl('/ansys_inc/v194/ansys/bin/ansys194',
    ...                       mode='console')

    """
    # These parameters are partially used for unit testing
    set_no_abort = kwargs.get("set_no_abort", True)

    if ip is None:
        ip = os.environ.get("PYMAPDL_IP", LOCALHOST)
    else:  # pragma: no cover
        start_instance = False
        ip = socket.gethostbyname(ip)  # Converting ip or hostname to ip

    check_valid_ip(ip)  # double check

    if port is None:
        port = int(os.environ.get("PYMAPDL_PORT", MAPDL_DEFAULT_PORT))
        check_valid_port(port)

    # Start MAPDL with PyPIM if the environment is configured for it
    # and the user did not pass a directive on how to launch it.
    if _HAS_PIM and exec_file is None and pypim.is_configured():
        LOG.info("Starting MAPDL remotely. The startup configuration will be ignored.")
        return launch_remote_mapdl(cleanup_on_exit=cleanup_on_exit)

    # connect to an existing instance if enabled
    if start_instance is None:
        start_instance = check_valid_start_instance(
            os.environ.get("PYMAPDL_START_INSTANCE", True)
        )

        # special handling when building the gallery outside of CI. This
        # creates an instance of mapdl the first time if PYMAPDL start instance
        # is False.
        if pymapdl.BUILDING_GALLERY:  # pragma: no cover
            # launch an instance of pymapdl if it does not already exist and
            # we're allowed to start instances
            if start_instance and GALLERY_INSTANCE[0] is None:
                mapdl = launch_mapdl(
                    start_instance=True,
                    cleanup_on_exit=False,
                    loglevel=loglevel,
                    set_no_abort=set_no_abort,
                )
                GALLERY_INSTANCE[0] = {"ip": mapdl._ip, "port": mapdl._port}
                return mapdl

                # otherwise, connect to the existing gallery instance if available
            elif GALLERY_INSTANCE[0] is not None:
                mapdl = MapdlGrpc(
                    ip=GALLERY_INSTANCE[0]["ip"],
                    port=GALLERY_INSTANCE[0]["port"],
                    cleanup_on_exit=False,
                    loglevel=loglevel,
                    set_no_abort=set_no_abort,
                )
                if clear_on_connect:
                    mapdl.clear()
                return mapdl

                # finally, if running on CI/CD, connect to the default instance
            else:
                mapdl = MapdlGrpc(
                    ip=ip,
                    port=port,
                    cleanup_on_exit=False,
                    loglevel=loglevel,
                    set_no_abort=set_no_abort,
                )
            if clear_on_connect:
                mapdl.clear()
            return mapdl

    if not start_instance:
        if clear_on_connect is None:  # pragma: no cover
            clear_on_connect = False

        mapdl = MapdlGrpc(
            ip=ip,
            port=port,
            cleanup_on_exit=False,
            loglevel=loglevel,
            set_no_abort=set_no_abort,
        )
        if clear_on_connect:
            mapdl.clear()
        return mapdl

    # verify executable
    if exec_file is None:
        # Load cached path
        exec_file = get_ansys_path()
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
        temp_dir = tempfile.gettempdir()
        run_location = os.path.join(temp_dir, "ansys_%s" % random_string(10))
        if not os.path.isdir(run_location):
            try:
                os.mkdir(run_location)
            except:
                raise RuntimeError(
                    "Unable to create the temporary working "
                    f'directory "{run_location}"\n'
                    "Please specify run_location="
                )
    else:
        if not os.path.isdir(run_location):
            raise FileNotFoundError(f'"{run_location}" is not a valid directory')
        if remove_temp_files:
            LOG.info("`run_location` set. Disabling the removal of temporary files.")
            remove_temp_files = False

    # verify no lock file and the mode is valid
    check_lock_file(run_location, jobname, override)
    mode = check_mode(mode, _version_from_path(exec_file))

    # cache start parameters
    additional_switches = _validate_add_sw(
        additional_switches, exec_file, kwargs.pop("force_intel", False)
    )

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
                f"The keyword argument 'license_type' value ('{license_type}') is not a recognized license name or has been deprecated.\n"
                + "Still PyMAPDL will try to use it but in older versions you might experience problems connecting to the server.\n"
                + f"Recognized license names: {' '.join(allow_lics)}"
            )
            warnings.warn(warn_text, UserWarning)

        additional_switches += " -p " + license_type
        LOG.debug(
            f"Using specified license name '{license_type}' in the 'license_type' keyword argument."
        )

    elif "-p " in additional_switches:
        # There is already a license request in additional switches.
        license_type = re.findall(r"-p \b(\w*)", additional_switches)[
            0
        ]  # getting only the first product license.

        if license_type not in ALLOWABLE_LICENSES:
            allow_lics = [f"'{each}'" for each in ALLOWABLE_LICENSES]
            warn_text = (
                f"The additional switch product value ('-p {license_type}') is not a recognized license name or has been deprecated.\n"
                + "Still PyMAPDL will try to use it but in older versions you might experience problems connecting to the server.\n"
                + f"Recognized license names: {' '.join(allow_lics)}"
            )
            warnings.warn(warn_text, UserWarning)
            LOG.warning(warn_text)

        LOG.debug(
            f"Using specified license name '{license_type}' in the additional switches parameter."
        )

    elif license_type is not None:
        raise TypeError("The argument 'license_type' does only accept str or None.")

    start_parm = {
        "exec_file": exec_file,
        "run_location": run_location,
        "additional_switches": additional_switches,
        "jobname": jobname,
        "nproc": nproc,
        "print_com": print_com,
    }

    if mode in ["console", "corba"]:
        start_parm["start_timeout"] = start_timeout
    else:
        start_parm["ram"] = ram
        start_parm["override"] = override
        start_parm["timeout"] = start_timeout

    # Check the license server
    if license_server_check:
        # configure timeout to be 90% of the wait time of the startup
        # time for Ansys.
        lic_check = LicenseChecker(timeout=start_timeout * 0.9, verbose=verbose_mapdl)
        lic_check.start()

    try:
        if mode == "console":
            from ansys.mapdl.core.mapdl_console import MapdlConsole

            mapdl = MapdlConsole(loglevel=loglevel, log_apdl=log_apdl, **start_parm)
        elif mode == "corba":
            try:
                # pending deprecation to ansys-mapdl-corba
                from ansys.mapdl.core.mapdl_corba import MapdlCorba
            except ModuleNotFoundError:  # pragma: no cover
                raise ModuleNotFoundError(
                    "To use this feature, install the MAPDL CORBA package"
                    " with:\n\npip install ansys_corba"
                ) from None

            broadcast = kwargs.get("log_broadcast", False)
            mapdl = MapdlCorba(
                loglevel=loglevel,
                log_apdl=log_apdl,
                log_broadcast=broadcast,
                verbose=verbose_mapdl,
                **start_parm,
            )
        elif mode == "grpc":
            port, actual_run_location = launch_grpc(
                port=port,
                verbose=verbose_mapdl,
                ip=ip,
                add_env_vars=add_env_vars,
                replace_env_vars=replace_env_vars,
                **start_parm,
            )
            mapdl = MapdlGrpc(
                ip=ip,
                port=port,
                cleanup_on_exit=cleanup_on_exit,
                loglevel=loglevel,
                set_no_abort=set_no_abort,
                remove_temp_files=remove_temp_files,
                log_apdl=log_apdl,
                **start_parm,
            )
            if run_location is None:
                mapdl._path = actual_run_location
    except Exception as exception:
        # Failed to launch for some reason.  Check if failure was due
        # to the license check
        if license_server_check:
            lic_check.check()
            # pass
        raise exception

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
            if version < 170:
                raise VersionError("CORBA AAS mode requires MAPDL v17.0 or newer.")
            if version >= 211:
                warnings.warn(
                    "CORBA AAS mode not recommended in MAPDL 2021R1 or newer.\n"
                    "Recommend using gRPC mode instead."
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
        elif version >= 170:
            mode = "corba"
        else:
            if os.name == "nt":
                raise VersionError(
                    "Running MAPDL as a service requires "
                    "v17.0 or greater on Windows."
                )
            mode = "console"

    if version < 130:
        warnings.warn("MAPDL as a service has not been tested on MAPDL < v13")

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
        return add_env_vars

    elif replace_env_vars:
        if not isinstance(replace_env_vars, dict):
            raise TypeError(
                "The variable 'replace_env_vars' should be a dict with env vars."
            )

        return replace_env_vars
