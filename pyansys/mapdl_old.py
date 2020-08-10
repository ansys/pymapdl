"""
Contains the _MapdlOld class and dependent functions.  To be inherited
by MapdlCorba and MapdlConsole for interfacing with MAPDL without the
use of gRPC.
"""
import glob
import os
import re

import numpy as np

from pyansys.mapdl import _MapdlCore
import pyansys
from pyansys.misc import is_float, supress_logging, chunks


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


# test for png file
PNG_TEST = re.compile('WRITTEN TO FILE(.*).png')


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
        super().__init__(loglevel)
        self._path = run_location

        self._local = True  # always local when using Console or CORBA
        self._exec_file = exec_file
        self._jobname = jobname
        self._archive_cache = None

        # these are stored internally for open_gui and launch
        self._start_timeout = start_timeout
        self._nproc = nproc
        self._additional_switches = additional_switches

        self.non_interactive = self._non_interactive(self)
        self._redirected_commands = {'*LIS': self._list}

        # perhaps directly from MAPDL...
        self._version = re.findall(r'\d\d\d', self._exec_file)[0]

        # start local instance of MAPDL
        self._launch()

        if log_apdl:
            filename = os.path.join(self.path, 'log.inp')
            self.open_apdl_log(filename, mode=log_apdl)

    def _reset_cache(self):
        """Reset cached items"""
        self._archive_cache = None

    @property
    @supress_logging
    def _mesh(self):
        """Write entire archive to ASCII and read it in as a pyansys.Archive """
        if self._archive_cache is None:
            # write database to an archive file
            arch_filename = os.path.join(self.path, 'tmp.cdb')
            self.cdwrite('db', arch_filename)
            self._archive_cache = pyansys.Archive(arch_filename, parse_vtk=True,
                                                  name='Mesh')
        return self._archive_cache

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

    def _display_plot(self, text):
        """Display the last generated plot (*.png) from MAPDL"""
        png_found = PNG_TEST.findall(text)
        if png_found:
            # flush graphics writer
            self.show('CLOSE')
            self.show('PNG')

            # get last filename based on the current jobname
            filenames = glob.glob(os.path.join(self.path, '%s*.png' % self.jobname))
            filenames.sort()
            filename = filenames[-1]

            import matplotlib.pyplot as plt
            import matplotlib.image as mpimg

            if os.path.isfile(filename):
                img = mpimg.imread(filename)
                plt.imshow(img)
                plt.axis('off')
                if self._show_matplotlib_figures:
                    plt.show()  # consider in-line plotting
            else:
                self._log.error('Unable to find screenshot at %s' % filename)

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

        # there may be multiple result files at this location (if not
        # combining results)
        if not os.path.isfile(result_path):
            raise FileNotFoundError('No results found at %s' % result_path)
        return pyansys.read_binary(result_path)

    def _get(self, *args, **kwargs):
        """Simply use the default get method"""
        return self.get(*args, **kwargs)

    def load_array(self, arr, name):
        """Load a numpy array or python list directly to MAPDL

        Writes the numpy array to disk and then reads it in within MAPDL
        using *VREAD.

        Parameters
        ----------
        arr : np.ndarray or List

        name : str
            Name of the array to write to within MAPDL.

        Examples
        --------
        Load a 1D numpy array into MAPDL

        >>> arr = np.array([10, 20, 30])
        >>> mapdl.load_array(arr, 'MYARR')
        >>> parm, mapdl_arrays = mapdl.load_parameters()
        >>> mapdl_arrays['MYARR']
        array([10., 20., 30.])

        Load a 2D numpy array into MAPDL

        >>> arr = np.random.random((5, 3))
        >>> mapdl.load_array(arr, 'MYARR')
        >>> parm, mapdl_arrays = mapdl.load_parameters()
        >>> mapdl_arrays['MYARR']
        array([[0.39806635, 0.15060953, 0.3990557 ],
               [0.26837768, 0.02033222, 0.15655861],
               [0.46110226, 0.06381489, 0.20068533],
               [0.20122863, 0.5727896 , 0.85636037],
               [0.68126612, 0.67460878, 0.3678797 ]])

        Load a python list into MAPDL

        >>> mapdl.load_array([10, -1, 8, 4, 10], 'MYARR')
        >>> parm, mapdl_arrays = mapdl.load_parameters()
        >>> mapdl_arrays['MYARR']
        array([10., -1.,  8.,  4., 10.])

        """
        # type checks
        arr = np.array(arr)
        if not np.issubdtype(arr.dtype, np.number):
            raise TypeError('Only numerical arrays or lists are supported')
        if arr.ndim > 3:
            raise ValueError('MAPDL VREAD only supports a arrays with a'
                             ' maximum of 3 dimensions.')

        name = name.upper()
        # disable logging for this function
        prior_log_level = self._log.level
        self._log.setLevel('CRITICAL')

        idim, jdim, kdim = arr.shape[0], 0, 0
        if arr.ndim >= 2:
            jdim = arr.shape[1]
        if arr.ndim == 3:
            kdim = arr.shape[2]

        # write array from numpy to disk:
        filename = os.path.join(self.path, '_tmp.dat')
        if arr.dtype != np.double:
            arr = arr.astype(np.double)
        pyansys._reader.write_array(filename.encode(), arr.ravel('F'))

        self.dim(name, imax=idim, jmax=jdim, kmax=kdim)
        with self.non_interactive:
            self.vread('%s(1, 1),%s,,,IJK, %d, %d, %d' % (name, filename,
                                                          idim, jdim, kdim))
            self.run('(1F20.12)')

        self._log.setLevel(prior_log_level)

    @supress_logging
    def load_array(self, arr, name):
        """Load a numpy array or python list directly to MAPDL

        Writes the numpy array to disk and then reads it in within MAPDL
        using *VREAD.

        Parameters
        ----------
        arr : np.ndarray or List

        name : str
            Name of the array to write to within MAPDL.

        Examples
        --------
        Load a 1D numpy array into MAPDL

        >>> arr = np.array([10, 20, 30])
        >>> mapdl.load_array(arr, 'MYARR')
        >>> parm, mapdl_arrays = mapdl.load_parameters()
        >>> mapdl_arrays['MYARR']
        array([10., 20., 30.])

        Load a 2D numpy array into MAPDL

        >>> arr = np.random.random((5, 3))
        >>> mapdl.load_array(arr, 'MYARR')
        >>> parm, mapdl_arrays = mapdl.load_parameters()
        >>> mapdl_arrays['MYARR']
        array([[0.39806635, 0.15060953, 0.3990557 ],
               [0.26837768, 0.02033222, 0.15655861],
               [0.46110226, 0.06381489, 0.20068533],
               [0.20122863, 0.5727896 , 0.85636037],
               [0.68126612, 0.67460878, 0.3678797 ]])

        Load a python list into MAPDL

        >>> mapdl.load_array([10, -1, 8, 4, 10], 'MYARR')
        >>> parm, mapdl_arrays = mapdl.load_parameters()
        >>> mapdl_arrays['MYARR']
        array([10., -1.,  8.,  4., 10.])

        """
        # type checks
        arr = np.array(arr)
        if not np.issubdtype(arr.dtype, np.number):
            raise TypeError('Only numerical arrays or lists are supported')
        if arr.ndim > 3:
            raise ValueError('MAPDL VREAD only supports a arrays with a'
                             ' maximum of 3 dimensions.')

        name = name.upper()

        idim, jdim, kdim = arr.shape[0], 0, 0
        if arr.ndim >= 2:
            jdim = arr.shape[1]
        if arr.ndim == 3:
            kdim = arr.shape[2]

        # write array from numpy to disk:
        filename = os.path.join(self.path, '_tmp.dat')
        if arr.dtype != np.double:
            arr = arr.astype(np.double)
        pyansys._reader.write_array(filename.encode(), arr.ravel('F'))

        self.dim(name, imax=idim, jmax=jdim, kmax=kdim)
        with self.non_interactive:
            self.vread('%s(1, 1),%s,,,IJK, %d, %d, %d' % (name, filename,
                                                          idim, jdim, kdim))
            self.run('(1F20.12)')

    # TODO: path needs to be a dynamic property


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

    for array_name in arrays:
        arrays[array_name] = np.squeeze(arrays[array_name])
    return parameters, arrays
