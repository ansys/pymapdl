"""Module for launching MAPDL locally or connecting to a remote instance with gRPC."""
import platform
from glob import glob
import re
import warnings
import os
import appdirs
import tempfile
import socket
import time
import subprocess

from ansys.mapdl import core as pymapdl
from ansys.mapdl.core.misc import is_float, random_string, create_temp_dir, threaded
from ansys.mapdl.core.errors import LockFileException, VersionError
from ansys.mapdl.core.mapdl_grpc import MapdlGrpc

# settings directory
SETTINGS_DIR = appdirs.user_data_dir('ansys_mapdl_core')
if not os.path.isdir(SETTINGS_DIR):
    try:
        os.makedirs(SETTINGS_DIR)
    except:
        warnings.warn('Unable to create settings directory.\n' +
                      'Will be unable to cache ANSYS executable location')

CONFIG_FILE = os.path.join(SETTINGS_DIR, 'config.txt')
ALLOWABLE_MODES = ['corba', 'console', 'grpc']

LOCALHOST = '127.0.0.1'
MAPDL_DEFAULT_PORT = 50052


def _is_ubuntu():
    """Determine if running as Ubuntu

    It's a bit complicated because sometimes the distribution is
    Ubuntu, but the kernel has been recompiled and no longer has the
    word "ubuntu" in it.

    """
    # must be running linux for this to be True
    if os.name != 'posix':
        return False

    # try lsb_release as this is more reliable
    try:
        import lsb_release
        if lsb_release.get_distro_information()['ID'].lower() == 'ubuntu':
            return True
    except ImportError:
        return 'ubuntu' in platform.platform().lower()


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
    matches = re.findall(r'v(\d\d\d).ansys', path.replace('\\', '/'),
                         re.IGNORECASE)
    if not matches:
        raise RuntimeError(f'Unable to extract Ansys version from {path}')
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
    """
    if port_range is None:
        port_range = range(50000, 50200)

    @threaded
    def close_mapdl(port):
        try:
            mapdl = MapdlGrpc(port=port, set_no_abort=False)
            mapdl.exit()
        except OSError:
            pass

    ports = check_ports(port_range)
    for port, state in ports.items():
        if state:
            close_mapdl(port)


def check_ports(port_range, ip='localhost'):
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


def launch_grpc(exec_file='', jobname='file', nproc=2, ram=None,
                run_location=None, port=MAPDL_DEFAULT_PORT,
                additional_switches='', custom_bin=None,
                override=True, timeout=20, verbose=False) -> tuple:
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
        Additional switches for MAPDL, for example aa_r, and academic
        research license, would be added with:

        - ``additional_switches="-aa_r"``

        Avoid adding switches like -i -o or -b as these are already
        included to start up the MAPDL server.  See the notes
        section for additional details.

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

    Returns
    -------
    port : int
        Returns the port number that the gRPC instance started on.

    Examples
    --------
    Launch MAPDL using the default configuration.

    >>> from ansys.mapdl import launch_mapdl
    >>> mapdl = launch_mapdl()

    Run MAPDL with shared memory parallel and specify the location of
    the ansys binary.

    >>> exec_file = 'C:/Program Files/ANSYS Inc/v202/ansys/bin/win64/ANSYS202.exe'
    >>> mapdl = launch_mapdl(exec_file, additional_switches='-smp')

    Notes
    -----
    These are the MAPDL switch options as of 2020R2 applicable for
    running MAPDL as a service via gRPC.  Excluded switches such as
    ``"-j"`` either not applicable or are set via keyword arguments.

    -acc <device> : Enables the use of GPU hardware.  See GPU
     Accelerator Capability in the Parallel Processing Guide for more
     information.

    -amfg : Enables the additive manufacturing capability.  Requires
     an additive manufacturing license. For general information about
     this feature, see AM Process Simulation in ANSYS Workbench.

    -ansexe <executable> :  Activates a custom mechanical APDL executable.
     In the ANSYS Workbench environment, activates a custom
     Mechanical APDL executable.

    -custom <executable> : Calls a custom Mechanical APDL executable
     See Running Your Custom Executable in the Programmer's Reference
     for more information.

    -db value : Initial memory allocation
     Defines the portion of workspace (memory) to be used as the
     initial allocation for the database. The default is 1024
     MB. Specify a negative number to force a fixed size throughout
     the run; useful on small memory systems.

    -dis : Enables Distributed ANSYS
     See the Parallel Processing Guide for more information.

    -dvt : Enables ANSYS DesignXplorer advanced task (add-on).
     Requires DesignXplorer.

    -l <language> : Specifies a language file to use other than English
     This option is valid only if you have a translated message file
     in an appropriately named subdirectory in
     ``/ansys_inc/v201/ansys/docu`` or
     ``Program Files\\ANSYS\\Inc\\V201\\ANSYS\\docu``

    -m <workspace> : Specifies the total size of the workspace
     Workspace (memory) in megabytes used for the initial
     allocation. If you omit the ``-m`` option, the default is 2 GB
     (2048 MB). Specify a negative number to force a fixed size
     throughout the run.

    -machines <IP> : Specifies the distributed machines
     Machines on which to run a Distributed ANSYS analysis. See
     Starting Distributed ANSYS in the Parallel Processing Guide for
     more information.

    -mpi <value> : Specifies the type of MPI to use.
     See the Parallel Processing Guide for more information.

    -mpifile <appfile> : Specifies an existing MPI file
     Specifies an existing MPI file (appfile) to be used in a
     Distributed ANSYS run. See Using MPI Files in the Parallel
     Processing Guide for more information.

    -na <value>: Specifies the number of GPU accelerator devices
     Number of GPU devices per machine or compute node when running
     with the GPU accelerator feature. See GPU Accelerator Capability
     in the Parallel Processing Guide for more information.

    -name <value> : Defines Mechanical APDL parameters
     Set mechanical APDL parameters at program start-up. The parameter
     name must be at least two characters long. For details about
     parameters, see the ANSYS Parametric Design Language Guide.

    -p <productname> : ANSYS session product
     Defines the ANSYS session product that will run during the
     session. For more detailed information about the ``-p`` option,
     see Selecting an ANSYS Product via the Command Line.

    -ppf <license feature name> : HPC license
     Specifies which HPC license to use during a parallel processing
     run. See HPC Licensing in the Parallel Processing Guide for more
     information.

    -smp : Enables shared-memory parallelism.
     See the Parallel Processing Guide for more information.
    """
    # disable all MAPDL pop-up errors:
    os.environ['ANS_CMD_NODIAG'] = 'TRUE'

    # use temporary directory if run_location is unspecified
    if run_location is None:
        run_location = create_temp_dir()
    elif not os.path.isdir(run_location):
        os.mkdir(run_location)

    if not os.access(run_location, os.W_OK):
        raise IOError('Unable to write to ``run_location`` "%s"' % run_location)

    # verify version
    if _version_from_path(exec_file) < 202:
        raise VersionError('The MAPDL gRPC interface requires MAPDL 20.2 or later')

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

    cpu_sw = '-np %d' % nproc
    if ram:
        ram_sw = '-m %d' % int(1024*ram)
    else:
        ram_sw = ''

    job_sw = '-j %s' % jobname
    port_sw = '-port %d' % port
    grpc_sw = '-grpc'

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
                    raise IOError(f'Unable to remove {filename}.  There might be '
                                  'an instance of MAPDL running at running at '
                                  f'"{run_location}"')

    # Windows will spawn a new window, special treatment
    if os.name == 'nt':
        tmp_inp = '.__tmp__.inp'
        with open(os.path.join(run_location, tmp_inp), 'w') as f:
            f.write('FINISH\r\n')

        # must start in batch mode on windows to hide APDL window
        command_parm = ['"%s"' % exec_file, job_sw, cpu_sw, ram_sw, '-b',
                        '-i', tmp_inp, '-o', '.__tmp__.out',
                        additional_switches, port_sw, grpc_sw]
        command = ' '.join(command_parm)

    else:  # linux
        command_parm = []
        command_parm.extend(['"%s"' % exec_file, job_sw, cpu_sw,
                            ram_sw, additional_switches, port_sw,
                            grpc_sw])
        command = ' '.join(command_parm)

    if verbose:
        print(f'Running {command}')
        subprocess.Popen(command,
                         shell=os.name != 'nt',
                         cwd=run_location)
    else:
        subprocess.Popen(command,
                         shell=os.name != 'nt',
                         cwd=run_location,
                         stdin=subprocess.DEVNULL,
                         stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL)


    # watch for the creation of temporary files at the run_directory.
    # This lets us know that the MAPDL process has at least started
    sleep_time = 0.1
    for _ in range(int(timeout/sleep_time)):
        # check if any error files have been created.  This is
        # more reliable than using the lock file

        files = os.listdir(run_location)
        has_ans = any([filename for filename in files if ".err" in filename])
        if has_ans:
            break
        time.sleep(sleep_time)

    return port, run_location


def get_start_instance(start_instance_default=True):
    """Check if the environment variable PYMAPDL_START_INSTANCE exists and is valid."""
    if 'PYMAPDL_START_INSTANCE' in os.environ:
        if os.environ['PYMAPDL_START_INSTANCE'].lower() not in ['true', 'false']:
            val = os.environ['PYMAPDL_START_INSTANCE']
            raise OSError(f'Invalid value "{val}" for PYMAPDL_START_INSTANCE\n'
                          'PYMAPDL_START_INSTANCE should be either "TRUE" or "FALSE"')
        return os.environ['PYMAPDL_START_INSTANCE'].lower() == 'true'
    return start_instance_default


def _get_available_base_ansys():
    """Return a dictionary of available ANSYS versions with their base paths.

    Returns
    -------
    Return all installed ANSYS paths in Windows

    >>> _get_available_base_ansys()
    {194: 'C:\\Program Files\\ANSYS INC\\v194',
     202: 'C:\\Program Files\\ANSYS INC\\v202',
     211: 'C:\\Program Files\\ANSYS INC\\v211'}

    Within Linux

    >>> _get_available_base_ansys()
    {194: '/usr/ansys_inc/v194',
     202: '/usr/ansys_inc/v202',
     211: '/usr/ansys_inc/v211'}
    """
    base_path = None
    if os.name == 'nt':
        supported_versions = [194, 202, 211, 212, 221]
        awp_roots = {ver: os.environ.get(f'AWP_ROOT{ver}', '') for ver in supported_versions}
        installed_versions = {ver: path for ver, path in awp_roots.items() if path and os.path.isdir(path)}
        if installed_versions:
            return installed_versions
        else:
            base_path = os.path.join(os.environ['PROGRAMFILES'], 'ANSYS INC')
    elif os.name == 'posix':
        for path in ['/usr/ansys_inc', '/ansys_inc']:
            if os.path.isdir(path):
                base_path = path
    else:
        raise OSError(f'Unsupported OS {os.name}')

    if base_path is None:
        return {}

    paths = glob(os.path.join(base_path, 'v*'))

    if not paths:
        return {}

    ansys_paths = {}
    for path in paths:
        ver_str = path[-3:]
        if is_float(ver_str):
            ansys_paths[int(ver_str)] = path

    return ansys_paths


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

    >>> from ansys.mapdl.core.misc import find_ansys
    >>> find_ansys()
    'C:/Program Files/ANSYS Inc/v211/ANSYS/bin/winx64/ansys211.exe', 21.1

    Within Linux

    >>> find_ansys()
    (/usr/ansys_inc/v211/ansys/bin/ansys211, 21.1)
    """
    versions = _get_available_base_ansys()
    if not versions:
        return '', ''
    version = max(versions.keys())
    ans_path = versions[version]
    if os.name == 'nt':
        ansys_bin = os.path.join(ans_path,  'ansys', 'bin', 'winx64',
                                 f'ansys{version}.exe')
    else:
        ansys_bin = os.path.join(ans_path,  'ansys', 'bin', f'ansys{version}')
    return ansys_bin, version/10


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
    """ Checks if a valid version of ANSYS is installed and preconfigured """
    ansys_bin = get_ansys_path(allow_input=False)
    if ansys_bin is not None:
        version = _version_from_path(ansys_bin)
        return not(version < 170 and os.name != 'posix')
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
        with open(CONFIG_FILE, 'w') as f:
            f.write(exe_loc)
    else:
        raise FileNotFoundError('File %s is invalid or does not exist' % exe_loc)


def save_ansys_path(exe_loc=''):
    """ Find ANSYS path or query user """
    # if exe_loc.strip():
    #     print('Cached ANSYS executable %s not found' % exe_loc)
    # else:
    #     print('Cached ANSYS executable not found')
    exe_loc, ver = find_ansys()
    if os.path.isfile(exe_loc):
        # automatically cache this path
        # print('Found ANSYS at %s' % exe_loc)
        # resp = input('Use this location?  [Y/n]')
        # if resp != 'n':
        change_default_ansys_path(exe_loc)
        return exe_loc

    if exe_loc is not None:
        if os.path.isfile(exe_loc):
            return exe_loc

    # otherwise, query user for the location
    with open(CONFIG_FILE, 'w') as f:
        print('Cached ANSYS executable not found')
        try:
            exe_loc = raw_input('Enter location of ANSYS executable: ')
        except NameError:
            exe_loc = input('Enter location of ANSYS executable: ')
        if not os.path.isfile(exe_loc):
            raise FileNotFoundError('ANSYS executable not found at this location:\n%s' % exe_loc)

        f.write(exe_loc)

    return exe_loc


def check_lock_file(path, jobname, override):
    # Check for lock file
    lockfile = os.path.join(path, jobname + '.lock')
    if os.path.isfile(lockfile):
        if not override:
            raise LockFileException('\nLock file exists for jobname "%s"' % jobname +
                                    ' at\n"%s"\n\n' % lockfile +
                                    'Set ``override=True`` to or delete the lock file '
                                    'to start MAPDL')
        else:
            try:
                os.remove(lockfile)
            except PermissionError:
                raise LockFileException('Unable to remove lock file.  '
                                        'Another instance of MAPDL might be '
                                        'running at "%s"' % path)


def launch_mapdl(exec_file=None, run_location=None, jobname='file',
                 nproc=2, ram=None, mode=None, override=False,
                 loglevel='ERROR', additional_switches='',
                 start_timeout=120, port=None,
                 custom_bin=None, cleanup_on_exit=True,
                 start_instance=True, ip=LOCALHOST,
                 clear_on_connect=True, log_apdl=False,
                 verbose_mapdl=False, **kwargs):
    """Start MAPDL locally in gRPC mode.

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
        Used only when ``start_instance`` is ``False``.  Defaults to
        ``'127.0.0.1'``. You can also override the default behavior of
        this keyword argument with the environment variable
        "PYMAPDL_IP=FALSE".

    clear_on_connect : bool, optional
        Used only when ``start_instance`` is ``False``.  Defaults to
        ``True``, giving you a fresh environment when connecting to
        MAPDL.

    remove_temp_files : bool, optional
        Removes temporary files on exit.  Default ``False``.

    verbose_mapdl : bool, optional
        Enable printing of all output when launching and running
        MAPDL.  This should be used for debugging only as output can
        be tracked within pymapdl.  Default ``False``.

    Examples
    --------
    Launch MAPDL using the best protocol.

    >>> from ansys.mapdl.core import launch_mapdl
    >>> mapdl = launch_mapdl()

    Run MAPDL with shared memory parallel and specify the location of
    the ansys binary.

    >>> exec_file = 'C:/Program Files/ANSYS Inc/v201/ansys/bin/win64/ANSYS201.exe'
    >>> mapdl = launch_mapdl(exec_file, additional_switches='-smp')

    Connect to an existing instance of MAPDL at IP 192.168.1.30 and
    port 50001.  This is only available using the latest ``'grpc'``
    mode.

    >>> mapdl = launch_mapdl(start_instance=False, ip='192.168.1.30',
                             port=50001)

    Force the usage of the CORBA protocol.

    >>> mapdl = launch_mapdl(mode='corba')

    Run MAPDL using the console mode (available only on Linux).

    >>> mapdl = launch_mapdl('/ansys_inc/v194/ansys/bin/ansys194',
                              mode='console')

    Notes
    -----
    These are the MAPDL switch options as of 2020R2 applicable for
    running MAPDL as a service via gRPC.  Excluded switches such as
    ``"-j"`` either not applicable or are set via keyword arguments.

    -acc <device> : Enables the use of GPU hardware.  See GPU
     Accelerator Capability in the Parallel Processing Guide for more
     information.

    -amfg : Enables the additive manufacturing capability.  Requires
     an additive manufacturing license. For general information about
     this feature, see AM Process Simulation in ANSYS Workbench.

    -ansexe <executable> :  Activates a custom mechanical APDL executable.
     In the ANSYS Workbench environment, activates a custom
     Mechanical APDL executable.

    -custom <executable> : Calls a custom Mechanical APDL executable
     See Running Your Custom Executable in the Programmer's Reference
     for more information.

    -db value : Initial memory allocation
     Defines the portion of workspace (memory) to be used as the
     initial allocation for the database. The default is 1024
     MB. Specify a negative number to force a fixed size throughout
     the run; useful on small memory systems.

    -dis : Enables Distributed ANSYS
     See the Parallel Processing Guide for more information.

    -dvt : Enables ANSYS DesignXplorer advanced task (add-on).
     Requires DesignXplorer.

    -l <language> : Specifies a language file to use other than English
     This option is valid only if you have a translated message file
     in an appropriately named subdirectory in
     ``/ansys_inc/v201/ansys/docu`` or
     ``Program Files\\ANSYS\\Inc\\V201\\ANSYS\\docu``

    -m <workspace> : Specifies the total size of the workspace
     Workspace (memory) in megabytes used for the initial
     allocation. If you omit the ``-m`` option, the default is 2 GB
     (2048 MB). Specify a negative number to force a fixed size
     throughout the run.

    -machines <IP> : Specifies the distributed machines
     Machines on which to run a Distributed ANSYS analysis. See
     Starting Distributed ANSYS in the Parallel Processing Guide for
     more information.

    -mpi <value> : Specifies the type of MPI to use.
     See the Parallel Processing Guide for more information.

    -mpifile <appfile> : Specifies an existing MPI file
     Specifies an existing MPI file (appfile) to be used in a
     Distributed ANSYS run. See Using MPI Files in the Parallel
     Processing Guide for more information.

    -na <value>: Specifies the number of GPU accelerator devices
     Number of GPU devices per machine or compute node when running
     with the GPU accelerator feature. See GPU Accelerator Capability
     in the Parallel Processing Guide for more information.

    -name <value> : Defines Mechanical APDL parameters
     Set mechanical APDL parameters at program start-up. The parameter
     name must be at least two characters long. For details about
     parameters, see the ANSYS Parametric Design Language Guide.

    -p <productname> : ANSYS session product
     Defines the ANSYS session product that will run during the
     session. For more detailed information about the ``-p`` option,
     see Selecting an ANSYS Product via the Command Line.

    -ppf <license feature name> : HPC license
     Specifies which HPC license to use during a parallel processing
     run. See HPC Licensing in the Parallel Processing Guide for more
     information.

    -smp : Enables shared-memory parallelism.
     See the Parallel Processing Guide for more information.
    """
    # These parameters are partially used for unit testing
    set_no_abort = kwargs.get('set_no_abort', True)
    ip = os.environ.get('PYMAPDL_IP', ip)
    if 'PYMAPDL_PORT' in os.environ:
        port = int(os.environ.get('PYMAPDL_PORT'))
    if port is None:
        port = MAPDL_DEFAULT_PORT

    # connect to an existing instance if enabled
    if not get_start_instance(start_instance):
        mapdl = MapdlGrpc(ip=ip, port=port, cleanup_on_exit=False,
                          loglevel=loglevel, set_no_abort=set_no_abort)
        if clear_on_connect:
            mapdl.clear()
        return mapdl

    # verify executable
    if exec_file is None:
        # Load cached path
        exec_file = get_ansys_path()
        if exec_file is None:
            raise FileNotFoundError('Invalid or path or cannot load cached '
                                    'ansys path.  Enter one manually using '
                                    'launch_mapdl(exec_file=)')
    else:  # verify ansys exists at this location
        if not os.path.isfile(exec_file):
            raise FileNotFoundError('Invalid ANSYS executable at "%s"\n'
                                    % exec_file + 'Enter one manually using '
                                    'launch_mapdl(exec_file=)')

    # verify run location
    if run_location is None:
        temp_dir = tempfile.gettempdir()
        run_location = os.path.join(temp_dir, 'ansys_%s' % random_string(10))
        if not os.path.isdir(run_location):
            try:
                os.mkdir(run_location)
            except:
                raise RuntimeError('Unable to create the temporary working '
                                   f'directory "{run_location}"\n'
                                   'Please specify run_location=')
    else:
        if not os.path.isdir(run_location):
            raise FileNotFoundError(f'"{run_location}" is not a valid directory')

    # verify no lock file and the mode is valid
    check_lock_file(run_location, jobname, override)
    mode = check_mode(mode, _version_from_path(exec_file))

    # known issue with distributed memory parallel
    # Ubuntu ANSYS fails to launch without I_MPI_SHM_LMT
    if 'smp' not in additional_switches:
        if _is_ubuntu():
            os.environ['I_MPI_SHM_LMT'] = 'shm'

    # cache start parameters
    if mode in ['console', 'corba']:
        start_parm = {'exec_file': exec_file,
                      'run_location': run_location,
                      'jobname': jobname,
                      'nproc': nproc,
                      'additional_switches': additional_switches,
                      'start_timeout': start_timeout}
    else:
        start_parm = {'exec_file': exec_file,
                      'jobname': jobname,
                      'nproc': nproc,
                      'ram': ram,
                      'run_location': run_location,
                      'additional_switches': additional_switches,
                      'custom_bin': custom_bin,
                      'override': override,
                      'timeout': start_timeout}

    if mode == 'console':
        from ansys.mapdl.core.mapdl_console import MapdlConsole
        mapdl = MapdlConsole(loglevel=loglevel, log_apdl=log_apdl,
                             **start_parm)
    elif mode == 'corba':
        try:
            # pending deprication to ansys-mapdl-corba
            from ansys.mapdl.core.mapdl_corba import MapdlCorba
        except ImportError:
            raise ImportError('To use this feature, install the MAPDL CORBA package'
                              ' with:\n\n'
                              '    pip install ansys_corba')

        broadcast = kwargs.get('log_broadcast', False)
        mapdl = MapdlCorba(loglevel=loglevel, log_apdl=log_apdl,
                           log_broadcast=broadcast, verbose=verbose_mapdl,
                           **start_parm)
    elif mode == 'grpc':
        port, actual_run_location = launch_grpc(port=port, verbose=verbose_mapdl,
                                                **start_parm)
        mapdl = MapdlGrpc(ip=LOCALHOST, port=port,
                          cleanup_on_exit=cleanup_on_exit,
                          loglevel=loglevel, set_no_abort=set_no_abort,
                          remove_temp_files=kwargs.pop('remove_temp_files', False),
                          **start_parm)
        if run_location is None:
            mapdl._path = actual_run_location
    else:
        raise ValueError('Invalid mode %s' % mode)

    return mapdl


def check_mode(mode, version):
    """Check if the MAPDL server mode matches the allowable version

    If ``None``, the newest mode will be selected.

    Returns a value from ``ALLOWABLE_MODES``.
    """
    if isinstance(mode, str):
        mode = mode.lower()
        if mode == 'grpc':
            if version < 211:
                if version < 202 and os.name == 'nt':
                    raise VersionError('gRPC mode requires MAPDL 2020R2 or newer '
                                       'on Windows.')
                elif os.name == 'posix':
                    raise VersionError('gRPC mode requires MAPDL 2021R1 or newer.')
        elif mode == 'corba':
            if version < 170:
                raise VersionError('CORBA AAS mode requires MAPDL v17.0 or newer.')
            if version >= 211:
                raise VersionError('Console mode not supported for 2021R1 or newer.  '
                                   'Use the default "grpc" mode.')
        elif mode == 'console':
            if os.name == 'nt':
                raise ValueError('Console mode requires Linux')
            if version >= 211:
                raise VersionError('Console mode not supported for 2021R1 or newer.  '
                                   'Use the default "grpc" mode.')
        else:
            raise ValueError(f'Invalid MAPDL server mode "{mode}".\n\n'
                             f'Use one of the following modes:\n{ALLOWABLE_MODES}')

    else:  # auto-select based on best version
        if version >= 211:
            mode = 'grpc'
        elif version == 202 and os.name == 'nt':
            # Windows supports it as of 2020R2
            mode = 'grpc'
        elif version >= 170:
            mode = 'corba'
        else:
            if os.name == 'nt':
                raise VersionError('Running MAPDL as a service requires '
                                   'v17.0 or greater on Windows.')
            mode = 'console'

    if version < 130:
        warnings.warn('MAPDL as a service has not been tested on MAPDL < v13')

    return mode
