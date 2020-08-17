"""Functions for launching MAPDL locally
interface.
"""
import re
import warnings
import os
import appdirs
import tempfile
import socket
import pexpect
from pexpect import popen_spawn


from pyansys.misc import is_float
from pyansys.errors import LockFileException, PrivateModuleImportError

# settings directory
SETTINGS_DIR = appdirs.user_data_dir('pyansys')
if not os.path.isdir(SETTINGS_DIR):
    try:
        os.makedirs(SETTINGS_DIR)
    except:
        warnings.warn('Unable to create settings directory.\n' +
                      'Will be unable to cache ANSYS executable location')

CONFIG_FILE = os.path.join(SETTINGS_DIR, 'config.txt')
ALLOWABLE_MODES = ['grpc', 'corba', 'console']

LOCALHOST = '127.0.0.1'
MAPDL_DEFAULT_PORT = 50052


def port_in_use(port, ip='localhost'):
    """Returns True when a port is in use at the given ip"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((ip, port)) == 0


def find_ansys():
    """Searches for ansys path within environmental variables.

    Reutrns
    -------
    ansys_exe_path : str
        Full path to ANSYS executable

    version : float
        Version of ANSYS
    """
    ansys_sysdir_var = 'ANSYS_SYSDIR'
    paths = {}
    for var in os.environ:
        if 'ANSYS' in var and '_DIR' in var:
            # add path if valid
            path = os.environ[var]
            if os.path.isdir(path):

                # add path if version number is in path
                version_str = var[5:8]
                if is_float(version_str):
                    paths[int(version_str)] = path

    if not paths:
        return '', ''

    # check through all available paths and return the latest version
    while paths:
        version = max(paths.keys())
        ansys_path = paths[version]

        if ansys_sysdir_var in os.environ:
            sysdir = os.environ[ansys_sysdir_var]
            ansys_bin_path = os.path.join(ansys_path, 'bin', sysdir)
            if 'win' in sysdir:
                ansys_exe = 'ansys%d.exe' % version
            else:
                ansys_exe = 'ansys%d' % version
        else:
            ansys_bin_path = os.path.join(ansys_path, 'bin')
            ansys_exe = 'ansys%d' % version

        ansys_exe_path = os.path.join(ansys_bin_path, ansys_exe)
        if os.path.isfile(ansys_exe_path):
            break
        else:
            paths.pop(version)
            paths.remove(ansys_path)

    version_float = float(version)/10.0
    return ansys_exe_path, version_float


def get_ansys_path(allow_input=True):
    """ Acquires ANSYS Path from a cached file or user input """
    exe_loc = None
    if os.path.isfile(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            exe_loc = f.read()
        # verify
        if not os.path.isfile(exe_loc) and allow_input:
            exe_loc = save_ansys_path()
    elif allow_input:  # create configuration file
        exe_loc = save_ansys_path()

    return exe_loc


def check_valid_ansys():
    """ Checks if a valid version of ANSYS is installed and preconfigured """
    ansys_bin = get_ansys_path(allow_input=False)
    if ansys_bin is not None:
        version = int(re.findall(r'\d\d\d', ansys_bin)[0])
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
    Change default ansys location on Linux

    >>> import pyansys
    >>> pyansys.change_default_ansys_path('/ansys_inc/v201/ansys/bin/ansys201')
    >>> pyansys.mapdl.get_ansys_path()
    '/ansys_inc/v201/ansys/bin/ansys201'

    Change default ansys location on Windows
    >>> ans_pth = 'C:/Program Files/ANSYS Inc/v193/ansys/bin/win64/ANSYS193.exe'
    >>> pyansys.change_default_ansys_path(ans_pth)
    >>> pyansys.mapdl.check_valid_ansys()
    True

    """
    if os.path.isfile(exe_loc):
        with open(CONFIG_FILE, 'w') as f:
            f.write(exe_loc)
    else:
        raise FileNotFoundError('File %s is invalid or does not exist' % exe_loc)


def save_ansys_path(exe_loc=''):
    """ Find ANSYS path or query user """
    if exe_loc.strip():
        print('Cached ANSYS executable %s not found' % exe_loc)
    else:
        print('Cached ANSYS executable not found')
    exe_loc, ver = find_ansys()
    if os.path.isfile(exe_loc):
        print('Found ANSYS at %s' % exe_loc)
        resp = input('Use this location?  [Y/n]')
        if resp != 'n':
            change_default_ansys_path(exe_loc)
            return exe_loc

    if exe_loc is not None:
        if os.path.isfile(exe_loc):
            return exe_loc

    # otherwise, query user for the location
    with open(CONFIG_FILE, 'w') as f:
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
            raise FileExistsError('\nLock file exists for jobname "%s"' % jobname +
                                  ' at\n"%s"\n\n' % lockfile +
                                  'Set ``override=True`` to or delete the lock file '
                                  'to start MAPDL')
        else:
            try:
                os.remove(lockfile)
            except PermissionError:
                raise PermissionError('Unable to remove lock file.  '
                                      'Another instance of MAPDL might be '
                                      'running at "%s"' % path)


def launch_mapdl(exec_file=None, run_location=None, mode=None, jobname='file',
                 nproc=2, override=False, loglevel='INFO',
                 additional_switches='', start_timeout=120,
                 log_apdl=False, **kwargs):
    """This class launches a local instance of MAPDL in the background
    and allows commands to be passed to a persistent session.

    Parameters
    ----------
    exec_file : str, optional
        The location of the MAPDL executable.  Will use the cached
        location when left at the default ``None``.

    run_location : str, optional
        MAPDL working directory.  Defaults to a temporary working
        directory.

    mode : str, optional
        Mode to launch MAPDL.  Must be one of the following:

        - ``'grpc'``
        - ``'corba'``
        - ``'console'``

    jobname : str, optional
        MAPDL jobname.  Defaults to ``'file'``.

    nproc : int, optional
        Number of processors.  Defaults to 2.

    ram : int, optional
        RAM to allocate for the process.  Default None (unlimited).
        Only valid when creating a gRPC process.

    override : bool, optional
        Attempts to delete the lock file at the run_location.
        Useful when a prior MAPDL session has exited prematurely and
        the lock file has not been deleted.

    wait : bool, optional
        When True, waits until MAPDL has been initialized before
        initializing the python ansys object.  Set this to False for
        debugging.

    loglevel : str, optional
        Sets which messages are printed to the console.  Default
        'INFO' prints out all MAPDL messages, 'WARNING` prints only
        messages containing MAPDL warnings, and 'ERROR' prints only
        error messages.

    additional_switches : str, optional
        Additional switches for MAPDL, for example aa_r, and academic
        research license, would be added with:

        - additional_switches="-aa_r"

        Avoid adding switches like -i -o or -b as these are already
        included to start up the MAPDL server.  See the notes
        section for additional details.

    start_timeout : float, optional
        Time to wait before raising an error that MAPDL is unable to
        start.

    log_broadcast : bool, optional
        Additional logging for ansys solution progress.  Default True
        and visible at log level 'INFO'.  Only applicable when ``mode=corba``

    log_apdl : str, optional
        Opens an APDL log file in the current MAPDL working directory
        to log all MAPDL commands to file.  Default False.  Set to 'a'
        to append to an existing log or 'w' to write a new log.

    port : int, optional
        Port to open the gRPC server on.  Only applicable when ``mode='grpc'``

    cleanup_on_exit : bool, optional
        Shutdown the server when the Python object is deleted or
        Python exits.  Only applicable when ``mode='grpc'``.

    Examples
    --------
    >>> import pyansys
    >>> mapdl = pyansys.Mapdl()

    Run MAPDL with the smp switch and specify the location of the
    ansys binary.

    >>> import pyansys
    >>> mapdl = pyansys.Mapdl('/ansys_inc/v194/ansys/bin/ansys194',
                              additional_switches='-smp')

    Notes
    -----
    MAPDL has the following command line options as of v20.1 (2020R1)

    -aas : Enables server mode
     When enabling server mode, a custom name for the keyfile can be
     specified using the ``-iorFile`` option.  This is the CORBA that
     pyansys uses for ``mode='corba'``.

    -acc <device> : Enables the use of GPU hardware.  Enables the use of
     GPU hardware to accelerate the analysis. See GPU Accelerator
     Capability in the Parallel Processing Guide for more information.

    -amfg : Enables the additive manufacturing capability.
     Requires an additive manufacturing license. For general
     information about this feature, see AM Process Simulation in
     ANSYS Workbench.

    -ansexe <executable> :  activates a custom mechanical APDL executable.
     In the ANSYS Workbench environment, activates a custom
     Mechanical APDL executable.

    -b <list or nolist> : Activates batch mode
     The options ``-b`` list or ``-b`` by itself cause the input
     listing to be included in the output. The ``-b`` nolist option
     causes the input listing not to be included. For more information
     about running Mechanical APDL in batch mode, see Batch Mode.

    -custom <executable> : Calls a custom Mechanical APDL executable
     See Running Your Custom Executable in the Programmer's Reference
     for more information.

    -d <device> : Specifies the type of graphics device
     This option applies only to interactive mode. For Linux systems,
     graphics device choices are X11, X11C, or 3D. For Windows
     systems, graphics device options are WIN32 or WIN32C, or 3D.

    -db value : Initial memory allocation
     Defines the portion of workspace (memory) to be used as the
     initial allocation for the database. The default is 1024
     MB. Specify a negative number to force a fixed size throughout
     the run; useful on small memory systems.

    -dir <path> : Defines the initial working directory
     Using the ``-dir`` option overrides the
     ``ANSYS201_WORKING_DIRECTORY`` environment variable.

    -dis : Enables Distributed ANSYS
     See the Parallel Processing Guide for more information.

    -dvt : Enables ANSYS DesignXplorer advanced task (add-on).
     Requires DesignXplorer.

    -g : Launches the Mechanical APDL program with the GUI
     Graphical User Interface (GUI) on. If you select this option, an
     X11 graphics device is assumed for Linux unless the ``-d`` option
     specifies a different device. This option is not used on Windows
     systems. To activate the GUI after Mechanical APDL has started,
     enter two commands in the input window: /SHOW to define the
     graphics device, and /MENU,ON to activate the GUI. The ``-g`` option
     is valid only for interactive mode.  Note: If you start
     Mechanical APDL via the ``-g`` option, the program ignores any /SHOW
     command in the start.ans file and displays a splash screen
     briefly before opening the GUI windows.

    -i <inputname> : Specifies the name of the file to read
     Inputs an input file into Mechanical APDL for batch
     processing.

    -iorFile <keyfile_name> : Specifies the name of the server keyfile
     Name of the server keyfile when enabling server mode. If this
     option is not supplied, the default name of the keyfile is
     ``aas_MapdlID.txt``. For more information, see Mechanical APDL as
     a Server Keyfile in the Mechanical APDL as a Server User's Guide.

    -j <Jobname> : Specifies the initial jobname
     A name assigned to all files generated by the program for a
     specific model. If you omit the ``-j`` option, the jobname is assumed
     to be file.

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
     Nubmer of GPU devices per machine or compute node when running
     with the GPU accelerator feature. See GPU Accelerator Capability
     in the Parallel Processing Guide for more information.

    -name <value> : Defines Mechanical APDL parameters
     Set mechanical APDL parameters at program start-up. The parameter
     name must be at least two characters long. For details about
     parameters, see the ANSYS Parametric Design Language Guide.

    -np <value> : Specifies the number of processors
     Number of processors to use when running Distributed ANSYS or
     Shared-memory ANSYS. See the Parallel Processing Guide for more
     information.

    -o <outputname> : Output file
     Specifies the name of the file to store the output from a batch
     execution of Mechanical APDL

    -p <productname> : ANSYS session product
     Defines the ANSYS session product that will run during the
     session. For more detailed information about the ``-p`` option,
     see Selecting an ANSYS Product via the Command Line.

    -ppf <license feature name> : HPC license
     Specifies which HPC license to use during a parallel processing
     run. See HPC Licensing in the Parallel Processing Guide for more
     information.

    -rcopy <path> : Path to remote copy of files
     On a Linux cluster, specifies the full path to the program used
     to perform remote copy of files. The default value is
     ``/usr/bin/scp``.

    -s <read or noread> : Read startup file
     Specifies whether the program reads the ``start.ans`` file at
     start-up. If you omit the ``-s`` option, Mechanical APDL reads the
     start.ans file in interactive mode and not in batch mode.

    -schost <host>: Coupling service host
     Specifies the host machine on which the coupling service is
     running (to which the co-simulation participant/solver must
     connect) in a System Coupling analysis.

    -scid <value> : System Coupling analysis licensing ID
     Specifies the licensing ID of the System Coupling analysis.

    -sclic <port@host> : System Coupling analysis host
     Specifies the licensing port and host to use for the System
     Coupling analysis.

    -scname <solver> : Name of the co-simulation participant
     Specifies the unique name used by the co-simulation participant
     to identify itself to the coupling service in a System Coupling
     analysis. For Linux systems, you need to quote the name to have
     the name recognized if it contains a space: (e.g.
     ``-scname "Solution 1"``)

    -scport <port> : Coupling service port
     Specifies the port on the host machine upon which the coupling
     service is listening for connections from co-simulation
     participants in a System Coupling analysis.

    -smp : Enables shared-memory parallelism.
     See the Parallel Processing Guide for more information.

    -usersh : Enable MPI remote shell.
     Directs the MPI software (used by Distributed ANSYS) to use the
     remote shell (rsh) protocol instead of the default secure shell
     (ssh) protocol. See Configuring Distributed ANSYS in the Parallel
     Processing Guide for more information.

    -v : Return version info
     Returns the Mechanical APDL release number, update number,
     copyright date, customer number, and license manager version
     number.
    """
    # depreciated options
    if 'prefer_pexpect' in kwargs:
        raise NotImplementedError('"prefer_pexpect" is depreciated.  '
                                  'Please use: ``mode="console"``')

    if exec_file is None:
        # Load cached path
        exec_file = get_ansys_path()
        if exec_file is None:
            raise FileNotFoundError('Invalid or path or cannot load cached '
                                    'ansys path.  Enter one manually using '
                                    'pyansys.Mapdl(exec_file=...)')
    else:  # verify ansys exists at this location
        if not os.path.isfile(exec_file):
            raise FileNotFoundError('Invalid ANSYS executable at "%s"\n'
                                    % exec_file + 'Enter one manually using '
                                    'pyansys.Mapdl(exec_file=)')

    if run_location is None:
        temp_dir = tempfile.gettempdir()
        run_location = os.path.join(temp_dir, 'ansys')
        if not os.path.isdir(run_location):
            try:
                os.mkdir(run_location)
            except:
                raise RuntimeError('Unable to create temporary working '
                                   'directory %s\n' % run_location +
                                   'Please specify run_location=')
    else:
        if not os.path.isdir(run_location):
            raise FileNotFoundError('"%s" is not a valid directory' % run_location)

    check_lock_file(run_location, jobname, override)

    # NOTE: version may or may not be within the full exec_path
    version = int(re.findall(r'\d\d\d', exec_file)[0])
    mode = check_mode(mode, version)

    if mode == 'console':
        from pyansys.mapdl_console import MapdlConsole
        return MapdlConsole(exec_file,
                            run_location,
                            jobname=jobname,
                            nproc=nproc,
                            override=override,
                            loglevel=loglevel,
                            additional_switches=additional_switches,
                            start_timeout=start_timeout,
                            log_apdl=log_apdl)
    elif mode == 'corba':
        from pyansys.mapdl_corba import MapdlCorba
        return MapdlCorba(exec_file,
                          run_location,
                          jobname=jobname,
                          nproc=nproc,
                          override=override,
                          loglevel=loglevel,
                          additional_switches=additional_switches,
                          start_timeout=start_timeout,
                          log_apdl=log_apdl,
                          **kwargs)
    elif mode == 'grpc':
        # check if grpc package is available
        try:
            from ansys.mapdl import Mapdl
        except ImportError:
            raise PrivateModuleImportError

        port = launch_grpc(exec_file, jobname, nproc, ram=kwargs.pop('ram', None),
                           run_location=run_location, port=MAPDL_DEFAULT_PORT,
                           additional_switches=additional_switches,
                           override=True, timeout=start_timeout)

        # attempt to connect to the gRPC instance
        kwargs['jobname'] = jobname
        kwargs['run_location'] = run_location
        return Mapdl(LOCALHOST, port, loglevel=loglevel, log_apdl=log_apdl,
                     **kwargs)


def launch_grpc(exec_path, jobname, n_cpu, ram, run_location=None,
                port=MAPDL_DEFAULT_PORT, additional_switches='',
                override=True, timeout=10):
    """Start MAPDL in gRPC mode locally

    Returns
    -------
    port : int
        Returns the port number that the gRPC instance started on.

    """
    if run_location is None:
        run_location = os.getcwd()
    elif not os.path.isdir(run_location):
        raise RuntimeError('Directory %s does not exist' % run_location)

    if not os.access(run_location, os.W_OK):
        raise IOError('Unable to write to run_location "%s"' % run_location)

    # verify lock file does not exist
    lock_file = os.path.join(run_location, '%s.lock' % jobname)
    if os.path.isfile(lock_file):
        if override:
            os.remove(lock_file)
        else:
            raise LockFileException

    # get the next available port
    while port_in_use(port, LOCALHOST):
        port += 1

    cpu_sw = '-np %d' % n_cpu
    if ram:
        ram_sw = '-m %d' % int(1024*ram)
    else:
        ram_sw = ''

    # different treatment for windows vs. linux due to v202 build issues
    custom_sw = ''
    if os.name == 'posix':
        try:
            import ansys.mapdl_bin
        except ImportError:
            raise ImportError('Please install ``ansys.mapdl_bin`` to use the '
                              'gRPC mode on Linux for 2020R2')

        custom_bin = ansys.mapdl_bin.bin_path

        if not os.path.isfile(custom_bin):
            raise FileNotFoundError('Unable to locate the custom MAPDL executable')
        
        custom_sw = '-custom %s' % custom_bin

    job_sw = '-j %s' % jobname
    port_sw = '-port %d' % port
    grpc_sw = '-grpc'
    exec_path = '"%s"' % exec_path

    command = ' '.join([exec_path, custom_sw, job_sw, cpu_sw, ram_sw,
                        additional_switches, port_sw, grpc_sw])

    # if os.name == 'nt':
    #     # Start in a hidden window
    #     breakpoint()
    #     command = 'START /B "MAPDL" %s' % command

    # self._log.debug('Starting MAPDL in gRPC mode with:\n"%s"', command)

    # Windows will spawn a new window, only linux will let you use pexpect...
    process = popen_spawn.PopenSpawn(command,
                                     timeout=timeout,
                                     cwd=run_location)
    # if os.name == 'nt':

    try:
        idx = process.expect(['Server listening',
                              'Another ANSYS job with the same job name',
                              'PRESS <CR> OR <ENTER> TO CONTINUE',
                              'ERROR'])

        if idx == 1:
            raise LockFileException()
        if idx == 2:
            process.sendline('')  # enter to continue
            process.expect('Server listening', timeout=1)
        elif idx > 2:
            msg = process.read().decode()
            raise RuntimeError('Failed to start local mapdl instance:\n"%s"' % msg)
    except pexpect.EOF:
        msg = process.read().decode()
        raise RuntimeError('Failed to start local mapdl instance:\n"%s"' % msg)
    except pexpect.TIMEOUT:
        msg = process.before.decode()
        raise RuntimeError('Failed to start local mapdl instance:\n"%s"' % msg)

    return port


def check_mode(mode, version):
    """Check if the MAPDL server mode matches the allowable version

    If ``None``, the newest mode will be selected.
    """

    is_win = os.name == 'nt'

    if isinstance(mode, str):
        mode = mode.lower()
        if mode not in ALLOWABLE_MODES:
            raise ValueError('Invalid MAPDL server mode.  '
                             'Use one of the following:\n' + ALLOWABLE_MODES)

        # There's no interface for 2020R1
        if mode == 'grpc':
            if version < 202:
                raise ValueError('gRPC mode requires MAPDL 2020R2 or newer.')
        elif mode == 'corba':
            if version < 170:
                raise ValueError('CORBA AAS mode requires MAPDL v17.0 or newer.')
            elif version > 199:
                raise ValueError('CORBA AAS mode requires MAPDL < 2020R1.')
        elif mode == 'console' and is_win:
            raise ValueError('Console mode requires Linux')

    else:  # auto-select based on best version
        if version >= 202:  # handles all types
            mode = 'grpc'
        elif version >= 170:
            mode = 'corba'
        else:
            if os.name == 'nt':
                raise RuntimeError('Running MAPDL as a service requires '
                                   'v17.0 or greater on Windows.')
            mode = 'console'

    if version < 130:
        warnings.warn('MAPDL as a service has not been tested on MAPDL < v13')

    return mode
