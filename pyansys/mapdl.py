"""Module to control interaction with an ANSYS shell instance.
Built using ANSYS documentation from
https://www.sharcnet.ca/Software/Ansys/

This module makes no claim to own any rights to ANSYS.  It's merely an
interface to software owned by ANSYS.

"""
import time
import glob
import string
import re
import os
import tempfile
import warnings
import logging
import random
from shutil import copyfile, rmtree

import appdirs
import numpy as np

import pyansys
from pyansys.geometry_commands import geometry_commands
from pyansys.element_commands import element_commands
from pyansys.mapdl_functions import _MapdlCommands
from pyansys.convert import is_float

MATPLOTLIB_LOADED = True
try:
    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg
except:
    MATPLOTLIB_LOADED = False


def random_string(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


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


# settings directory
settings_dir = appdirs.user_data_dir('pyansys')
if not os.path.isdir(settings_dir):
    try:
        os.makedirs(settings_dir)
    except:
        warnings.warn('Unable to create settings directory.\n' +
                      'Will be unable to cache ANSYS executable location')

CONFIG_FILE = os.path.join(settings_dir, 'config.txt')

# specific to pexpect process
###############################################################################

# processors = ['/PREP7',
#               '/POST1',
#               '/SOLUTION',
#               '/POST26',
#               '/AUX2',
#               '/AUX3',
#               '/AUX12',
#               '/AUX15',
#               '/MAP',]


###############################################################################

# test for png file
PNG_TEST = re.compile('WRITTEN TO FILE(.*).png')

INVAL_COMMANDS = {'*vwr':  'Use "with ansys.non_interactive:\n\t*ansys.Run("VWRITE(..."',
                  '*cfo': '',
                  '*CRE': 'Create a function within python or run as non_interactive',
                  '*END': 'Create a function within python or run as non_interactive',
                  '*IF': 'Use a python if or run as non_interactive'}


def check_valid_ansys():
    """ Checks if a valid version of ANSYS is installed and preconfigured """
    ansys_bin = get_ansys_path(allow_input=False)
    if ansys_bin is not None:
        version = int(re.findall(r'\d\d\d', ansys_bin)[0])
        return not(version < 170 and os.name != 'posix')

    return False


def setup_logger(loglevel='INFO'):
    """ Setup logger """

    # return existing log if this function has already been called
    if hasattr(setup_logger, 'log'):
        setup_logger.log.setLevel(loglevel)
        ch = setup_logger.log.handlers[0]
        ch.setLevel(loglevel)
        return setup_logger.log

    # create logger
    log = logging.getLogger(__name__)
    log.setLevel(loglevel)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(loglevel)

    # create formatter
    formatstr = '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
    formatter = logging.Formatter(formatstr)

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    log.addHandler(ch)

    # make persistent
    setup_logger.log = log

    return log


def get_ansys_path(allow_input=True):
    """ Acquires ANSYS Path from a cached file or user input """
    exe_loc = None
    if os.path.isfile(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            exe_loc = f.read()
        # verify
        if not os.path.isfile(exe_loc) and allow_input:
            print('Cached ANSYS executable %s not found' % exe_loc)
            exe_loc = save_ansys_path()
    elif allow_input:  # create configuration file
        exe_loc = save_ansys_path()

    return exe_loc


def change_default_ansys_path(exe_loc):
    """
    Change your default ansys path

    Parameters
    ----------
    exe_loc : str
        Ansys executable.  Must be a full path.

    """
    if os.path.isfile(exe_loc):
        with open(CONFIG_FILE, 'w') as f:
            f.write(exe_loc)
    else:
        raise FileNotFoundError('File %s is invalid or does not exist' % exe_loc)


def save_ansys_path(exe_loc=''):
    """ Find ANSYS path or query user """
    print('Cached ANSYS executable %s not found' % exe_loc)
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
            raise FileExistsError('Lock file exists for jobname %s \n'
                                  % jobname +
                                  ' at %s\n' % lockfile +
                                  'Set ``override=True`` to delete lock '
                                  'and start ANSYS')
        else:
            try:
                os.remove(lockfile)
            except PermissionError:
                raise PermissionError('Unable to remove lock file.  '
                                      'Another instance of ANSYS might be '
                                      'running at "%s"' % path)


def launch_mapdl(exec_file=None, run_location=None,
                 jobname='file', nproc=2, override=False,
                 loglevel='INFO', additional_switches='',
                 start_timeout=120, interactive_plotting=False,
                 log_broadcast=False, check_version=True,
                 prefer_pexpect=True, log_apdl='w'):
    """This class opens ANSYS in the background and allows commands to
    be passed to a persistent session.

    Parameters
    ----------
    exec_file : str, optional
        The location of the ANSYS executable.  Will use the cached
        location when left at the default None.

    run_location : str, optional
        ANSYS working directory.  Defaults to a temporary working
        directory.

    jobname : str, optional
        ANSYS jobname.  Defaults to ``'file'``.

    nproc : int, optional
        Number of processors.  Defaults to 2.

    override : bool, optional
        Attempts to delete the lock file at the run_location.
        Useful when a prior ANSYS session has exited prematurely and
        the lock file has not been deleted.

    wait : bool, optional
        When True, waits until ANSYS has been initialized before
        initializing the python ansys object.  Set this to False for
        debugging.

    loglevel : str, optional
        Sets which messages are printed to the console.  Default
        'INFO' prints out all ANSYS messages, 'WARNING` prints only
        messages containing ANSYS warnings, and 'ERROR' prints only
        error messages.

    additional_switches : str, optional
        Additional switches for ANSYS, for example aa_r, and academic
        research license, would be added with:

        - additional_switches="-aa_r"

        Avoid adding switches like -i -o or -b as these are already
        included to start up the ANSYS MAPDL server.  See the notes
        section for additional details.

    start_timeout : float, optional
        Time to wait before raising error that ANSYS is unable to
        start.

    interactive_plotting : bool, optional
        Enables interactive plotting using ``matplotlib``.  Default
        False.

    log_broadcast : bool, optional
        Additional logging for ansys solution progress.  Default True
        and visible at log level 'INFO'.  Only applicable when using
        CORBA.

    check_version : bool, optional
        Check version of binary file and raise exception when invalid.

    prefer_pexpect : bool, optional
        When enabled, will avoid using ansys APDL in CORBA server mode
        and will spawn a process and control it using pexpect.
        Default False.

    log_apdl : str, optional
        Opens an APDL log file in the current ANSYS working directory.
        Default 'w'.  Set to 'a' to append to an existing log.

    Examples
    --------
    >>> import pyansys
    >>> mapdl = pyansys.Mapdl()

    Run MAPDL with the smp switch and specify the location of the
    ansys binary

    >>> import pyansys
    >>> mapdl = pyansys.Mapdl('/ansys_inc/v194/ansys/bin/ansys194',
                              additional_switches='-smp')

    Notes
    -----
    ANSYS MAPDL has the following command line options as of v20.1

    -aas : Enables server mode
     When enabling server mode, a custom name for the keyfile can be
     specified using the ``-iorFile`` option.  This is the CORBA that
     pyansys uses for Windows (and linux when
     ``prefer_pexpect=False``).

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
     ``Program Files\ANSYS\Inc\V201\ANSYS\docu``

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
    if exec_file is None:
        # Load cached path
        exec_file = get_ansys_path()
        if exec_file is None:
            raise FileNotFoundError('Invalid or path or cannot load cached '
                                    'ansys path.  Enter one manually using '
                                    'pyansys.Mapdl(exec_file=...)')
    else:  # verify ansys exists at this location
        if not os.path.isfile(exec_file):
            raise FileNotFoundError('Invalid ANSYS executable at "%s"'
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

    if os.name != 'posix':
        prefer_pexpect = False

    if prefer_pexpect:
        from pyansys.mapdl_console import MapdlConsole
        return MapdlConsole(exec_file,
                            run_location,
                            jobname=jobname,
                            nproc=nproc,
                            override=override,
                            loglevel=loglevel,
                            additional_switches=additional_switches,
                            start_timeout=start_timeout,
                            interactive_plotting=interactive_plotting,
                            log_apdl=log_apdl)
    else:
        from pyansys.mapdl_corba import MapdlCorba
        return MapdlCorba(exec_file,
                          run_location,
                          jobname=jobname,
                          nproc=nproc,
                          override=override,
                          loglevel=loglevel,
                          additional_switches=additional_switches,
                          start_timeout=start_timeout,
                          interactive_plotting=interactive_plotting,
                          log_apdl=log_apdl,
                          log_broadcast=log_broadcast)


class _Mapdl(_MapdlCommands):
    """This class opens ANSYS in the background and allows commands to
    be passed to a persistent session.

    Parameters
    ----------
    exec_file : str, optional
        The location of the ANSYS executable.  Will use the cached
        location when left at the default None.

    run_location : str, optional
        ANSYS working directory.  Defaults to a temporary working
        directory.

    jobname : str, optional
        ANSYS jobname.  Defaults to ``'file'``.

    nproc : int, optional
        Number of processors.  Defaults to 2.

    override : bool, optional
        Attempts to delete the lock file at the run_location.
        Useful when a prior ANSYS session has exited prematurely and
        the lock file has not been deleted.

    wait : bool, optional
        When True, waits until ANSYS has been initialized before
        initializing the python ansys object.  Set this to False for
        debugging.

    loglevel : str, optional
        Sets which messages are printed to the console.  Default
        'INFO' prints out all ANSYS messages, 'WARNING` prints only
        messages containing ANSYS warnings, and 'ERROR' prints only
        error messages.

    additional_switches : str, optional
        Additional switches for ANSYS, for example aa_r, and academic
        research license, would be added with:

        - additional_switches="-aa_r"

        Avoid adding switches like -i -o or -b as these are already
        included to start up the ANSYS MAPDL server.  See the notes
        section for additional details.

    start_timeout : float, optional
        Time to wait before raising error that ANSYS is unable to
        start.

    interactive_plotting : bool, optional
        Enables interactive plotting using ``matplotlib``.  Default
        False.

    check_version : bool, optional
        Check version of binary file and raise exception when invalid.

    prefer_pexpect : bool, optional
        When enabled, will avoid using ansys APDL in CORBA server mode
        and will spawn a process and control it using pexpect.
        Default False.

    log_apdl : str, optional
        Opens an APDL log file in the current ANSYS working directory.
        Default 'w'.  Set to 'a' to append to an existing log.

    Examples
    --------
    >>> import pyansys
    >>> mapdl = pyansys.Mapdl()

    Run MAPDL with the smp switch and specify the location of the
    ansys binary

    >>> import pyansys
    >>> mapdl = pyansys.Mapdl('/ansys_inc/v194/ansys/bin/ansys194',
                              additional_switches='-smp')

    Notes
    -----
    ANSYS MAPDL has the following command line options as of v20.1

    -aas : Enables server mode
     When enabling server mode, a custom name for the keyfile can be
     specified using the ``-iorFile`` option.  This is the CORBA that
     pyansys uses for Windows (and linux when
     ``prefer_pexpect=False``).

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
     ``Program Files\ANSYS\Inc\V201\ANSYS\docu``

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

    def __init__(self, exec_file, run_location,
                 jobname, nproc, override,
                 loglevel, additional_switches,
                 start_timeout, interactive_plotting,
                 log_apdl):
        """ Initialize connection with ANSYS program """
        self.path = run_location
        self._exec_file = exec_file
        self._jobname = jobname
        self._start_timeout = start_timeout
        self._nproc = nproc
        self._additional_switches = additional_switches
        self._allow_ignore = False
        self._interactive_plotting = interactive_plotting
        self._apdl_log = None
        self._store_commands = False
        self._stored_commands = []
        self.response = None
        self._outfile = None
        self._show_matplotlib_figures = True

        self._log = setup_logger(loglevel.upper())
        self.non_interactive = self._non_interactive(self)
        self._redirected_commands = {'*LIS': self._list}
        self.version = re.findall(r'\d\d\d', self._exec_file)[0]

        # launch MAPDL
        self._launch()

        if log_apdl:
            filename = os.path.join(self.path, 'log.inp')
            self.open_apdl_log(filename, mode=log_apdl)

        # setup plotting for PNG
        if self._interactive_plotting:
            self.enable_interactive_plotting()

    @property
    def _lockfile(self):
        """lockfile path"""
        return os.path.join(self.path, self.jobname + '.lock')

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
        2020-06-08 21:39:58,094 [INFO] pyansys.mapdl: K is not a
        recognized POST1 command, abbreviation, or macro.  This
        command will be ignored.

        *** WARNING *** CP = 0.372 TIME= 21:39:58
        K is not a recognized POST1 command, abbreviation, or macro.
        This command will be ignored.

        """
        return self._allow_ignore

    @allow_ignore.setter
    def allow_ignore(self, value):
        """Set allow ignore"""
        self._allow_ignore = bool(value)

    def open_apdl_log(self, filename, mode='w'):
        """Start writing all APDL commands to an ANSYS input file.

        Parameters
        ----------
        filename : str
            Filename of the log.
        """
        if self._apdl_log is not None:
            raise RuntimeError('APDL command logging already enabled.\n')

        self._log.debug('Opening ANSYS log file at %s', filename)
        self._apdl_log = open(filename, mode=mode, buffering=1)  # line buffered
        if mode != 'w':
            self._apdl_log.write('! APDL script generated using pyansys %s\n' %
                                 pyansys.__version__)

    def _close_apdl_log(self):
        """ Closes APDL log """
        if self._apdl_log is not None:
            self._apdl_log.close()
        self._apdl_log = None

    def enable_interactive_plotting(self, pixel_res=1600):
        """Enables interactive plotting.  Requires matplotlib

        Parameters
        ----------
        pixel_res : int
            Pixel resolution.  Valid values are from 256 to 2400.
            Lowering the pixel resolution produces a "fuzzier" image.
            Increasing the resolution produces a "sharper" image but
            takes longer to render.
        """
        if MATPLOTLIB_LOADED:
            self.show('PNG')
            self.gfile(1200)
            self._interactive_plotting = True
        else:
            raise ImportError('Install matplotlib to use enable interactive plotting\n' +
                              'or turn interactive plotting off with:\n' +
                              'interactive_plotting=False')

    def set_log_level(self, loglevel):
        """Sets log level"""
        setup_logger(loglevel=loglevel.upper())

    def run(self, command, write_to_log=True):
        """Runs APDL command(s)

        Parameters
        ----------
        command : str
            ANSYS APDL command.

        write_to_log : bool, optional
            Overrides APDL log writing.  Default True.  When set to
            False, will not write command to log even if APDL
            command logging is enabled.

        Returns
        -------
        command_output : str
            Command output from ANSYS.

        Notes
        -----
        When two or more commands need to be run non-interactively
        (i.e. ``*VWRITE``) use

        >>> with ansys.non_interactive:
        >>>     ansys.run("*VWRITE,LABEL(1),VALUE(1,1),VALUE(1,2),VALUE(1,3)")
        >>>     ansys.run("(1X,A8,'   ',F10.1,'  ',F10.1,'   ',1F5.3)")
        """
        if self._store_commands:
            self._stored_commands.append(command)
            return
        elif command[:3].upper() in INVAL_COMMANDS:
            exception = RuntimeError('Invalid pyansys command "%s"\n\n%s' %
                                     (command, INVAL_COMMANDS[command[:3]]))
            raise exception
        elif command[:4].upper() in INVAL_COMMANDS:
            exception = RuntimeError('Invalid pyansys command "%s"\n\n%s' %
                                     (command, INVAL_COMMANDS[command[:4]]))
            raise exception
        elif write_to_log and self._apdl_log is not None:
            if not self._apdl_log.closed:
                self._apdl_log.write('%s\n' % command)

        if command[:4] in self._redirected_commands:
            function = self._redirected_commands[command[:4]]
            return function(command)

        text = self._run(command)
        if text:
            self.response = text.strip()
        else:
            self.response = ''

        if self.response:
            self._log.info(self.response)
            if self._outfile:
                self._outfile.write('%s\n' % self.response)

        if '*** ERROR ***' in self.response:  # flag error
            self._log.error(self.response)
            # if not continue_on_error:
            raise Exception(self.response)

        # special returns for certain geometry commands
        try:
            short_cmd = command.split(',')[0]
        except:
            short_cmd = None

        if short_cmd in geometry_commands:
            return geometry_commands[short_cmd](self.response)

        if short_cmd in element_commands:
            return element_commands[short_cmd](self.response)

        return self.response

    def _run(self, command):
        raise NotImplementedError('Implemented by child class')

    def _list(self, command):
        """ Replaces *LIST command """
        items = command.split(',')
        filename = os.path.join(self.path, '.'.join(items[1:]))
        if os.path.isfile(filename):
            self.response = open(filename).read()
            self._log.info(self.response)
        else:
            raise Exception('Cannot run:\n%s\n' % command + 'File does not exist')

    @property
    def processor(self):
        """ Returns the current processor """
        msg = self.run('/Status')
        processor = None
        matched_line = [line for line in msg.split('\n') if "Current routine" in line]
        if matched_line:
            # get the processor
            processor = re.findall(r'\(([^)]+)\)', matched_line[0])[0]
        return processor

    def load_parameters(self):
        """Loads and returns all current parameters

        Returns
        -------
        parameters : dict
            Dictionary of single value parameters.

        arrays : dict
            Dictionary of MAPDL arrays.

        Examples
        --------
        >>> parameters, arrays = mapdl.load_parameters()
        >>> print(parameters)
        {'ANSINTER_': 2.0,
        'CID': 3.0,
        'TID': 4.0,
        '_ASMDIAG': 5.363415510271,
        '_MAXELEMNUM': 26357.0,
        '_MAXELEMTYPE': 7.0,
        '_MAXNODENUM': 40908.0,
        '_MAXREALCONST': 1.0}
        """
        # load ansys parameters to python
        filename = os.path.join(self.path, 'parameters.parm')
        self.parsav('all', filename)
        self.parameters, self.arrays = load_parameters(filename)
        return self.parameters, self.arrays

    def add_file_handler(self, filepath, append):
        """ Adds a file handler to the log """
        if append:
            mode = 'a'
        else:
            mode = 'w'

        self.fileHandler = logging.FileHandler(filepath)
        formatstr = '%(asctime)s [%(levelname)s] %(name)s: %(message)s'

        self.fileHandler = logging.FileHandler(filepath, mode=mode)
        self.fileHandler.setFormatter(logging.Formatter(formatstr))
        self.fileHandler.setLevel(logging.DEBUG)
        self._log.addHandler(self.fileHandler)
        self._log.info('Added file handler at %s' % filepath)

    def remove_file_handler(self):
        """Removes the filehander from the log"""
        self._log.removeHandler(self.fileHandler)
        self._log.info('Removed file handler')

    def _display_plot(self, text):
        """Display the last generated plot from ANSYS"""
        png_found = PNG_TEST.findall(text)
        if png_found:
            # flush graphics writer
            self.show('CLOSE')
            self.show('PNG')

            # get last filename based on the current jobname
            filenames = glob.glob(os.path.join(self.path, '%s*.png' % self.jobname))
            filenames.sort()
            filename = filenames[-1]

            if os.path.isfile(filename):
                img = mpimg.imread(filename)
                plt.imshow(img)
                plt.axis('off')
                if self._show_matplotlib_figures:
                    plt.show()  # consider in-line plotting
            else:
                self._log.error('Unable to find screenshot at %s' % filename)

    def __del__(self):
        """Clean up when complete"""
        try:
            self.exit()
        except Exception as e:
            if hasattr(self, '_log'):
                self._log.error('exit: %s', str(e))

        try:
            self.kill()
        except Exception as e:
            if hasattr(self, '_log'):
                self._log.error('kill: %s', str(e))

    def _remove_lockfile(self):
        """Removes lockfile"""
        if os.path.isfile(self._lockfile):
            try:
                os.remove(self._lockfile)
            except:
                pass

    @property
    def result(self):
        """Returns a binary interface to the result file."""
        try:
            result_path = self.inquire('RSTFILE')
        except RuntimeError:
            result_path = ''

        if not result_path:
            result_path = os.path.join(self.path, '%s.rst' % self._jobname)
        elif not os.path.dirname(result_path):
            result_path = os.path.join(self.path, '%s.rst' % result_path)

        if not os.path.isfile(result_path):
            raise FileNotFoundError('No results found at %s' % result_path)
        return pyansys.read_binary(result_path)

    def __call__(self, command, **kwargs):  # pragma: no cover
        raise NotImplementedError('\nDirectly calling the Mapdl class is depreciated'
                                  'Please use ``run`` instead')

    class _non_interactive:
        """Allows user to enter commands that need to run
        non-interactively.

        Examples
        --------
        To use an non-interactive command like *VWRITE, use:

        >>> with ansys.non_interactive:
                ansys.run("*VWRITE,LABEL(1),VALUE(1,1),VALUE(1,2),VALUE(1,3)")
                ansys.run("(1X,A8,'   ',F10.1,'  ',F10.1,'   ',1F5.3)")

        """
        def __init__(self, parent):
            self.parent = parent

        def __enter__(self):
            self.parent._log.debug('entering non-interactive mode')
            self.parent._store_commands = True

        def __exit__(self, type, value, traceback):
            self.parent._log.debug('entering non-interactive mode')
            self.parent._flush_stored()

    def _flush_stored(self):
        """Writes stored commands to an input file and runs the input
        file.  Used with non_interactive.
        """
        self._log.debug('Flushing stored commands')
        tmp_out = os.path.join(appdirs.user_data_dir('pyansys'),
                               'tmp_%s.out' % random_string())
        self._stored_commands.insert(0, "/OUTPUT, '%s'" % tmp_out)
        self._stored_commands.append('/OUTPUT')
        commands = '\n'.join(self._stored_commands)
        self._apdl_log.write(commands + '\n')

        # write to a temporary input file
        filename = os.path.join(appdirs.user_data_dir('pyansys'),
                                'tmp_%s.inp' % random_string())
        self._log.debug('Writing the following commands to a temporary ' +
                       'apdl input file:\n%s' % commands)

        with open(filename, 'w') as f:
            f.writelines(commands)

        self._store_commands = False
        self._stored_commands = []
        self.run("/INPUT, '%s'" % filename, write_to_log=False)
        if os.path.isfile(tmp_out):
            self.response = '\n' + open(tmp_out).read()

        if self.response is None:
            self._log.warning('Unable to read response from flushed commands')
        else:
            self._log.info(self.response)

    def get_float(self, entity="", entnum="", item1="", it1num="",
                  item2="", it2num="", **kwargs):
        """Runs the *GET command with a default parameter

        See `help(get)` for more details.

        Parameters
        ----------
        entity
            Entity keyword. Valid keywords are NODE, ELEM, KP, LINE, AREA,
            VOLU, PDS, etc., as shown for Entity = in the tables below.

        entnum
            The number or label for the entity (as shown for ENTNUM = in the
            tables below). In some cases, a zero (or blank) ENTNUM represents
            all entities of the set.

        item1
            The name of a particular item for the given entity. Valid items are
            as shown in the Item1 columns of the tables below.

        it1num
            The number (or label) for the specified Item1 (if any). Valid
            IT1NUM values are as shown in the IT1NUM columns of the tables
            below. Some Item1 labels do not require an IT1NUM value.

        item2, it2num
            A second set of item labels and numbers to further qualify the item
            for which data are to be retrieved. Most items do not require this
            level of information.

        Returns
        -------
        par : float
            Floating point value of the parameter.

        Examples
        --------
        Retreive the number of nodes.

        >>> value = ansys.get('node', '', 'count')
        >>> value
        3003

        Retreive the number of nodes using keywords.

        >>> value = ansys.get(entity='node', item1='count')
        >>> value
        3003
        """
        return self.get(entity=entity, entnum=entnum, item1=item1, it1num=it1num,
                        item2=item2, it2num=it2num, **kwargs)

    def get(self, par="__floatparameter__", entity="", entnum="",
            item1="", it1num="", item2="", it2num="", **kwargs):
        """APDL Command: *GET

        Retrieves a value and stores it as a scalar parameter or part
        of an array parameter.

        Parameters
        ----------
        par
            The name of the resulting parameter. See *SET for name
            restrictions.

        entity
            Entity keyword. Valid keywords are NODE, ELEM, KP, LINE, AREA,
            VOLU, PDS, etc., as shown for Entity = in the tables below.

        entnum
            The number or label for the entity (as shown for ENTNUM = in the
            tables below). In some cases, a zero (or blank) ENTNUM represents
            all entities of the set.

        item1
            The name of a particular item for the given entity. Valid items are
            as shown in the Item1 columns of the tables below.

        it1num
            The number (or label) for the specified Item1 (if any). Valid
            IT1NUM values are as shown in the IT1NUM columns of the tables
            below. Some Item1 labels do not require an IT1NUM value.

        item2, it2num
            A second set of item labels and numbers to further qualify the item
            for which data are to be retrieved. Most items do not require this
            level of information.

        Returns
        -------
        par : float
            Floating point value of the parameter.

        Examples
        --------
        Retreive the number of nodes

        >>> value = ansys.get('val', 'node', '', 'count')
        >>> value
        3003

        Retreive the number of nodes using keywords.  Note that the
        parameter name is optional.

        >>> value = ansys.get(entity='node', item1='count')
        >>> value
        3003

        Notes
        -----
        *GET retrieves a value for a specified item and stores the value as a
        scalar parameter, or as a value in a user-named array parameter. An
        item is identified by various keyword, label, and number combinations.
        Usage is similar to the *SET command except that the parameter values
        are retrieved from previously input or calculated results. For example,
        *GET,A,ELEM,5,CENT,X returns the centroid x-location of element 5 and
        stores the result as parameter A. *GET command operations, along with
        the associated Get functions return values in the active coordinate
        system unless stated otherwise. A Get function is an alternative in-
        line function that can be used to retrieve a value instead of the *GET
        command (see Using In-line Get Functions for more information).

        Both *GET and *VGET retrieve information from the active data stored in
        memory. The database is often the source, and sometimes the information
        is retrieved from common memory blocks that the program uses to
        manipulate information. Although POST1 and POST26 operations use a
        *.rst file, *GET data is accessed from the database or from the common
        blocks. Get operations do not access the *.rst file directly. For
        repeated gets of sequential items, such as from a series of elements,
        see the *VGET command.

        Most items are stored in the database after they are calculated and are
        available anytime thereafter. Items are grouped according to where they
        are usually first defined or calculated. Preprocessing data will often
        not reflect the calculated values generated from section data. Do not
        use *GET to obtain data from elements that use calculated section data,
        such as beams or shells. Most of the general items listed below are
        available from all modules. Each of the sections for accessing *GET
        parameters are shown in the following order:

        *GET General Entity Items

        *GET Preprocessing Entity Items

        *GET Solution Entity Items

        *GET Postprocessing Entity Items

        *GET Probabilistic Design Entity Items

        The *GET command is valid in any processor.
        """
        command = "*GET,%s,%s,%s,%s,%s,%s,%s" % (str(par),
                                                 str(entity),
                                                 str(entnum),
                                                 str(item1),
                                                 str(it1num),
                                                 str(item2),
                                                 str(it2num))
        response = self.run(command, **kwargs)
        try:
            return float(response.split('=')[-1])
        except:
            return None

    def read_float_parameter(self, parameter_name):
        """Read out the value of a ANSYS parameter to use in python.

        Parameters
        ----------
        parameter_name : str
            Name of the parameter inside ANSYS.

        Returns
        -------
        float
            Value of ANSYS parameter.

        Examples
        --------
        >>> ansys.get('myparm', 'node', '', 'count')
        >>> value = ansys.read_float_parameter('myparm')
        >>> value
        3003

        Retreive the value in an array.  This example creates a block
        of elements and stores the element numbers in an array.  Then
        it retreives the first value of that array

        >>> ansys.prep7()
        >>> ansys.block(0,1,0,1,0,1)
        >>> ansys.et(1, 186)
        >>> ansys.vmesh('all')
        >>> ansys.run('*VGET, ELEM_ARR, ELEM, , elist')
        >>> ansys.read_float_parameter('ELEM_ARR(1)')
        1.0

        You could also retrieve ELEM_ARR with

        >>> values, arrays = ansys.load_parameters()
        >>> arrays
        {'ELEM_ARR': array([1., 2., 3., 4., 5., 6., 7., 8.])}

        """
        try:
            response = self.run(parameter_name + " = " + parameter_name)
        except TypeError:
            raise TypeError('Input variable `parameter_name` should be string')
        return float(response.split('=')[-1])

    def read_float_from_inline_function(self, function_str):
        """Use a APDL inline function to get a float value from ANSYS.
        Take note, that internally an APDL parameter __floatparameter__ is
        created/overwritten.

        Parameters
        ----------
        function_str : str
            String containing an inline function as used in APDL..

        Returns
        -------
        float
            Value returned by inline function..

        Examples
        --------
        >>> inline_function = "node({},{},{})".format(x, y, z)
        >>> node = apdl.read_float_from_inline_function(inline_function)
        """
        self.run("__floatparameter__="+function_str)
        return self.read_float_parameter("__floatparameter__")

    def open_gui(self, include_result=True):
        """Saves existing database and opens up APDL GUI

        Parameters
        ----------
        include_result : bool, optional
            Allow the result file to be post processed in the GUI.
        """

        # specify a path for the temporary database
        temp_dir = tempfile.gettempdir()
        save_path = os.path.join(temp_dir, 'ansys_tmp')
        if os.path.isdir(save_path):
            rmtree(save_path)
        os.mkdir(save_path)

        name = 'tmp'
        tmp_database = os.path.join(save_path, '%s.db' % name)
        if os.path.isfile(tmp_database):
            os.remove(tmp_database)

        # get the state, close, and finish
        prior_processor = self.processor
        self.finish()
        self.save(tmp_database)
        self.exit(close_log=False)

        # copy result file to temp directory
        if include_result:
            resultfile = os.path.join(self.path, '%s.rst' % self.jobname)
            if os.path.isfile(resultfile):
                tmp_resultfile = os.path.join(save_path, '%s.rst' % name)
                copyfile(resultfile, tmp_resultfile)

        # write temporary input file
        start_file = os.path.join(save_path, 'start%s.ans' % self.version)
        with open(start_file, 'w') as f:
            f.write('RESUME\n')

        # some versions of ANSYS just look for "start.ans" when starting
        other_start_file = os.path.join(save_path, 'start.ans')
        with open(other_start_file, 'w') as f:
            f.write('RESUME\n')

        # issue system command to run ansys in GUI mode
        cwd = os.getcwd()
        os.chdir(save_path)
        os.system('cd "%s" && "%s" -g -j %s' % (save_path, self._exec_file, name))
        os.chdir(cwd)

        # must remove the start file when finished
        os.remove(start_file)
        os.remove(other_start_file)

        # reload database when finished
        self._launch()
        self.resume(tmp_database)
        if prior_processor is not None:
            if 'BEGIN' not in prior_processor:
                self.run('/%s' % prior_processor)

    @property
    def jobname(self):
        """MAPDL job name.

        This is requested from the active mapdl instance.
        """
        try:
            self._jobname = self.inquire('JOBNAME')
        except:
            pass
        return self._jobname

    def inquire(self, func):
        """Returns system information.

        Parameters
        ----------
        func : str
           Specifies the type of system information returned.  See the
           notes section for more information.

        Returns
        -------
        value : str
            Value of the inquired item.

        Notes
        -----
        Allowable func entries
        LOGIN - Returns the pathname of the login directory on Linux
        systems or the pathname of the default directory (including
        drive letter) on Windows systems.

        - ``DOCU`` - Pathname of the ANSYS docu directory.
        - ``APDL`` - Pathname of the ANSYS APDL directory.
        - ``PROG`` - Pathname of the ANSYS executable directory.
        - ``AUTH`` - Pathname of the directory in which the license file resides.
        - ``USER`` - Name of the user currently logged-in.
        - ``DIRECTORY`` - Pathname of the current directory.
        - ``JOBNAME`` - Current Jobname.
        - ``RSTDIR`` - Result file directory
        - ``RSTFILE`` - Result file name
        - ``RSTEXT`` - Result file extension
        - ``OUTPUT`` - Current output file name

        Examples
        --------
        Return the job name

        >>> mapdl.inquire('JOBNAME')
        file

        Return the result file name

        >>> mapdl.inquire('RSTFILE')
        file.rst
        """
        response = ''
        try:
            response = self.run('/INQUIRE, , %s' % func)
            return response.split('=')[1].strip()
        except IndexError:
            raise RuntimeError('Cannot parse %s' % response)

    def Run(self, command):  # pragma: no cover
        """Depreciated"""
        raise NotImplementedError('\nCommand "Run" decpreciated.  \n'
                                  'Please use "run" instead')


# TODO: Speed this up with:
# https://tinodidriksen.com/2011/05/cpp-convert-string-to-double-speed/
def load_parameters(filename):
    """Load parameters from a file

    Parameters
    ----------
    filename : str
        Name of the parameter file to read in.

    Returns
    -------
    parameters : dict
        Dictionary of single value parameters

    arrays : dict
        Dictionary of arrays
    """
    parameters = {}
    arrays = {}

    with open(filename) as f:
        append_mode = False
        append_text = []
        for line in f.readlines():
            if append_mode:
                if 'END PREAD' in line:
                    append_mode = False
                    values = ''.join(append_text).split(' ')
                    shp = arrays[append_varname].shape
                    raw_parameters = np.genfromtxt(values)

                    n_entries = np.prod(shp)
                    if n_entries != raw_parameters.size:
                        paratmp = np.zeros(n_entries)
                        paratmp[:raw_parameters.size] = raw_parameters
                        paratmp = paratmp.reshape(shp)
                    else:
                        paratmp = raw_parameters.reshape(shp, order='F')

                    arrays[append_varname] = paratmp.squeeze()
                    append_text.clear()
                else:
                    nosep_line = line.replace('\n', '').replace('\r', '')
                    append_text.append(" " + re.sub(r"(?<=\d)-(?=\d)"," -", nosep_line))

            elif '*DIM' in line:
                # *DIM, Par, Type, IMAX, JMAX, KMAX, Var1, Var2, Var3, CSYSID
                split_line = line.split(',')
                varname = split_line[1].strip()
                arr_type = split_line[2]
                imax = int(split_line[3])
                jmax = int(split_line[4])
                kmax = int(split_line[5])

                if arr_type == 'CHAR':
                    arrays[varname] = np.empty((imax, jmax, kmax), dtype='<U8', order='F')
                elif arr_type == 'ARRAY':
                    arrays[varname] = np.empty((imax, jmax, kmax), np.double, order='F')
                elif arr_type == 'TABLE':
                    arrays[varname] = np.empty((imax+1, jmax+1, kmax), np.double, order='F')
                elif arr_type == 'STRING':
                    arrays[varname] = 'str'
                else:
                    arrays[varname] = np.empty((imax, jmax, kmax), np.object, order='F')

            elif '*SET' in line:
                vals = line.split(',')
                varname = vals[1] + ' '
                varname = varname[:varname.find('(')].strip()
                if varname in arrays:
                    st = line.find('(') + 1
                    en = line.find(')')
                    ind = line[st:en].split(',')
                    i = int(ind[0]) - 1
                    j = int(ind[1]) - 1
                    k = int(ind[2]) - 1
                    value = line[en+2:].strip().replace("'", '').strip()
                    if isinstance(arrays[varname], str):
                        parameters[varname] = value
                        del arrays[varname]
                    else:
                        arrays[varname][i, j, k] = value
                else:
                    value = vals[-1]
                    if is_float(value):
                        parameters[varname] = float(value)
                    else:
                        parameters[varname] = value

            elif '*PREAD' in line:
                # read a series of values
                split_line = line.split(',')
                append_varname = split_line[1].strip()
                append_mode = True

    return parameters, arrays
