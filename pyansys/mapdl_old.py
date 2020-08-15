"""Contains the _MapdlOld class and dependent functions.  To be
inherited by MapdlCorba and MapdlConsole for interfacing with MAPDL
without the use of gRPC.
"""
import os
import re

import numpy as np

from pyansys import Archive
from pyansys.mapdl import _MapdlCore
from pyansys.misc import supress_logging


class _MapdlOld(_MapdlCore):
    """This class opens ANSYS in the background and allows commands to
    be passed to a persistent session.

    This class contains methods in common to MapdlConsole and
    MapdlCorba and uses the old, non-gRPC interface to exchange data
    to MAPDL.

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
                 start_timeout, log_apdl):
        """ Initialize connection with ANSYS program """
        super().__init__(loglevel, log_apdl=log_apdl)
        self._path = run_location

        self._local = True  # always local when using Console or CORBA
        self._exec_file = exec_file
        self._jobname = jobname
        self._archive_cache = None
        self._vget_arr_counter = 0

        # these are stored internally for open_gui and launch
        self._start_timeout = start_timeout
        self._nproc = nproc
        self._additional_switches = additional_switches

        # perhaps use self.parameters.revision
        self._version = re.findall(r'\d\d\d', self._exec_file)[0]

        # start local instance of MAPDL
        self._launch()

    def _reset_cache(self):
        """Reset cached items"""
        self._archive_cache = None

    @property
    @supress_logging
    def _mesh(self):
        """Write entire archive to ASCII and read it in as a ``pyansys.Archive``"""
        if self._archive_cache is None:
            # write database to an archive file
            arch_filename = os.path.join(self.path, '_tmp.cdb')
            nblock_filename = os.path.join(self.path, 'nblock.cdb')
            # must have all nodes elements are using selected
            with self.chain_commands:
                self.cm('__NODE__', 'NODE')
                self.nsle('S')
                self.cdwrite('db', arch_filename)
                self.cmsel('S', '__NODE__', 'NODE')

                self.cm('__ELEM__', 'ELEM')
                self.esel('NONE')
                self.cdwrite('db', nblock_filename)
                self.cmsel('S', '__ELEM__', 'ELEM')

            self._archive_cache = Archive(arch_filename, parse_vtk=False,
                                          name='Mesh')
            grid = self._archive_cache._parse_vtk(additional_checking=True)
            self._archive_cache._grid = grid

            # overwrite nodes in archive
            nblock = Archive(nblock_filename, parse_vtk=False)
            self._archive_cache._nodes = nblock._nodes
            self._archive_cache._nnum = nblock._nnum
            self._archive_cache._node_coord = None

        return self._archive_cache

    def load_parameters(self):  # pragma: no cover
        """Depreciated in favor of ``mapdl.parameters``"""
        raise NotImplementedError('``load_parameters`` is  Depreciated.  '
                                  '\n\nInstead, please use:\n'
                                  '``mapdl.parameters``')

    def _get(self, *args, **kwargs):
        """Simply use the default get method"""
        return self.get(*args, **kwargs)

    def _get_array(self, entity='', entnum='', item1='', it1num='', item2='',
                   it2num='', kloop='', dtype=None, **kwargs):
        """Uses the VGET command to get an array from ANSYS"""
        parm_name = kwargs.pop('parm', None)

        if parm_name is None:
            parm_name = '__vget_tmp_%d__' % self._vget_arr_counter
            self._vget_arr_counter += 1

        out = self.starvget(parm_name, entity, entnum, item1, it1num, item2,
                            it2num, kloop)

        # check if empty array
        if 'the dimension number 1 is 0' in out:
            return np.empty(0)

        with self.non_interactive:
            self.vwrite('%s(1)' % parm_name)
            self.run('(F20.12)')

        array = np.fromstring(self.last_response, sep='\n')
        if dtype:
            return array.astype(dtype)
        else:
            return array
