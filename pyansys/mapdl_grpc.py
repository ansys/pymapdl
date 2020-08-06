"""Module to control interaction with grpc mapdl server"""
import tempfile
import weakref
import re
import os
import threading
import socket
from threading import Timer
import time

import pexpect
from pexpect import popen_spawn
import numpy as np
import pyvista as pv
import scooby
from pyansys.geometry import Geometry
from pyansys.mapdl import _MapdlCore
from pyansys.misc import is_float, random_string

# from ansys.mapdl import __version__
# from ansys.mapdl.mapdl_grpc.client import MapdlGrpc
# from ansys.mapdl.misc import get_ip, check_itk
# from ansys.mapdl.common import threaded

MAPDL_DEFAULT_PORT = 50052



REMOVE_LOCK_MSG = 'Another ANSYS job with the same job name is already running in this directory'
              ' or the lock file has not been deleted from an abnormally terminated ANSYS run'

VGET_ENTITY_TYPES = ['NODE', 'ELEM', 'KP', 'LINE', 'AREA', 'VOLU',
                     'CDSY', 'RCON', 'TLAB']

STRESS_TYPES = ['X', 'Y', 'Z', 'XY', 'YZ', 'XZ', '1', '2', '3', 'INT', 'EQV']
COMP_TYPE = ['X', 'Y', 'Z', 'SUM']
VGET_NODE_ENTITY_TYPES = {'U': ['X', 'Y', 'Z'],
                          'S': STRESS_TYPES,
                          'EPTO': STRESS_TYPES,
                          'EPEL': STRESS_TYPES,
                          'EPPL': STRESS_TYPES,
                          'EPCR': STRESS_TYPES,
                          'EPTH': STRESS_TYPES,
                          'EPDI': STRESS_TYPES,
                          'EPSW': [None],
                          'NL': ['SEPL', 'SRAT', 'HPRES', 'EPEQ', 'PSV', 'PLWK'],
                          'HS': ['X', 'Y', 'Z'],
                          'BFE': ['TEMP'],
                          'TG': COMP_TYPE,
                          'TF': COMP_TYPE,
                          'PG': COMP_TYPE,
                          'EF': COMP_TYPE,
                          'D': COMP_TYPE,
                          'H': COMP_TYPE,
                          'B': COMP_TYPE,
                          'FMAG': COMP_TYPE,
                          'NLIST': [None]}


# these commands will be verbose and their response will be streamed by default
STREAM_COMMANDS = []

ITK_PLOTTING = hasattr(pv, 'PlotterITK') and scooby.knowledge.in_ipykernel()


def parse_fortran_index(i=1, j=1, k=1):
    return int(i), int(j), int(k)


class MapdlException(Exception):
    """Raised when MAPDL passes an error"""
    pass


def start_mapdl_local(jobname):
    """Start MAPDL in gRPC mode locally"""
    # get ip of this computer and next available port

    port = MAPDL_DEFAULT_PORT
    while port_in_use(port, ip):
        port += 1

    # launch MAPDL locally
    ram_mb = int(1024*ram)
    if ram_mb:
        self.log.info('Creating local instance with %d MB RAM and %d CPUs', ram_mb, n_cpu)
    else:
        self.log.info('Creating local instance with and %d CPUs', n_cpu)

    # different treatment for windows vs. linux due to v202 build issues
    cmd = '%s -custom /mnt/ansys_inc/grpc/ansys.e201t.DEBUG -m -%d -np %d -smp -port %d -grpc' % (ram_mb, n_cpu, port)
    self.log.debug('Running "%s"', cmd)

    if run_location is None:
        run_location = os.getcwd()

    if not os.access(run_location, os.W_OK):
        raise IOError('Unable to write to run_location "%s"' % run_location)

    # verify lock file does not exist
    lock_file = os.path.join(run_location, 'file.lock')
    if os.path.isfile(lock_file):
        if ignore_lock:
            os.remove(lock_file)
        else:
            raise Exception('Please remove the lock file at "%s"' % run_location
 or pass ignore_lock=True' %
                            run_location)


    self._process = popen_spawn.PopenSpawn(cmd, timeout=10, cwd=run_location)
    self._run_location = run_location

    try:
        idx = self._process.expect(['Server listening',
                                    'Another ANSYS job with the same job name',
                                    'PRESS <CR> OR <ENTER> TO CONTINUE',
                                    'ERROR'])

        if idx == 1:
            raise Exception('\n%s.  Please remove the lock file at the run location' % REMOVE_LOCK)
        if idx == 2:
            self._process.sendline('')  # enter to continue
            self._process.expect('Server listening', timeout=1)
        elif idx > 2:
            msg = self._process.before
            raise RuntimeError('Failed to start local mapdl instance: "%s"' % msg)
    except pexpect.EOF:
        msg = self._process.before
        raise RuntimeError('Failed to start local mapdl instance: "%s"' % msg)
    except pexpect.TIMEOUT:
        msg = self._process.before
        raise RuntimeError('Failed to start local mapdl instance: "%s"' % msg)

    self.log.info('Local MAPDL GRPC server listening on localhost:%d', port)

    

class RepeatingTimer(Timer):
    def run(self):
        while not self.finished.is_set():
            self.function(*self.args, **self.kwargs)
            self.finished.wait(self.interval)


class MapdlgRPC(_MapdlCore):
    """This class connects to a GRPC MAPDL server and allows commands
    to be passed to a persistent session.

    Parameters
    ----------
    loglevel : str, optional
        Sets which messages are printed to the console.  Default
        'INFO' prints out all ANSYS messages, 'WARNING` prints only
        messages containing ANSYS warnings, and 'ERROR' prints only
        error messages.

    timeout : float, optional
        Time to wait before raising error that ANSYS is unable to
        start or connect to the remote instance.  Increase this if
        there is heavy load on the cluster.

    local : bool, optional
        Start up a local instance rather than a remote (cluster)
        instance.  Default False.

    n_cpu : int, optional
        CPUs requested in the mapdl instance.  Default 2

    ram : float, optional
        RAM requested for the mapdl instance in GB.  Default 8

    ignore_lock : bool, optional
        Ignores lock file if present and if running a local instance.

    run_location : str, optional
       Location to run a local instance of the mapdl grpc instance.

    instance_timeout : float, optional
        Remote instance timeout in seconds.  By default, this is 3600
        seconds.  This can be increased up to 86400 seconds (one day).

    print_version : bool, optional
        Prints ANSYS and pyansys version on initialization.  Default
        True.

    Examples
    --------
    >>> import ansys
    >>> mapdl = ansys.Mapdl()

    Request an instance with 4 CPUs and 64 GB of RAM
    >>> mapdl = ansys.Mapdl(n_cpu=4, ram=64)

    Start a local instance of mapdl
    >>> mapdl = ansys.Mapdl(local=True)
    """

    def __init__(self, exec_file=None, run_location=None,
                 jobname='file', nproc=2, ram=None, override=False,
                 loglevel='INFO', additional_switches='',
                 start_timeout=120, interactive_plotting=False,
                 log_apdl='w'):
        """Initialize connection with mapdl"""
        super().__init__(loglevel)

        

        INSTANCES.append(self)

        # self.log = setup_logger(loglevel.upper())
        # self.jobname = 'file'
        # self._quad_grid = None
        # self._grid = None
        # self._solving = False
        # self._busy = True
        # self.port = None
        # self.server = None
        # self._process = None
        # self._local = local
        # self._run_location = None

        # # used by pool and threading
        # self.locked = False
        # self._check_flag = None

        # keep_alive = kwargs.pop('keep_alive', True)
        # ip = kwargs.pop('ip', None)
        # if isinstance(ip, str):
        #     # Check for valid IP address
        #     ip = ip.replace('"', '').replace("'", '')
        #     socket.inet_aton(ip)

        # port = kwargs.pop('port', None)
        # allow_new_nodes = kwargs.pop('allow_new_nodes', True)
        # use_netapp = kwargs.pop('use_netapp', False)
        # custom_command = kwargs.pop('custom_command', None)
        # self._cleanup = kwargs.pop('cleanup', True)

        # # TODO: assert keyword args is empty

        # if local:
        #     request_instance = False

        #     # get ip of this computer and next available port
        #     ip = get_ip()
        #     port = MAPDL_DEFAULT_PORT
        #     while port_in_use(port, ip):
        #         port += 1

        #     # launch MAPDL locally
        #     ram_mb = int(1024*ram)
        #     self.log.info('Creating local instance with %d MB RAM and %d CPUs', ram_mb, n_cpu)
        #     cmd = '/mnt/ansys_inc/v201/ansys/bin/ansys201 -custom /mnt/ansys_inc/grpc/ansys.e201t.DEBUG -m -%d -np %d -smp -port %d -grpc' % (ram_mb, n_cpu, port)
        #     self.log.debug('Running "%s"', cmd)

        #     if run_location is None:
        #         run_location = os.getcwd()

        #     if not os.access(run_location, os.W_OK):
        #         raise IOError('Unable to write to run_location "%s"' % run_location)

        #     # verify lock file does not exist
        #     lock_file = os.path.join(run_location, 'file.lock')
        #     if os.path.isfile(lock_file):
        #         if ignore_lock:
        #             os.remove(lock_file)
        #         else:
        #             raise Exception('Please remove the lock file at "%s" or pass ignore_lock=True' %
        #                             run_location)
                              

        #     self._process = popen_spawn.PopenSpawn(cmd, timeout=10, cwd=run_location)
        #     self._run_location = run_location

        #     try:
        #         idx = self._process.expect(['Server listening',
        #                                     'Another ANSYS job with the same job name',
        #                                     'PRESS <CR> OR <ENTER> TO CONTINUE',
        #                                     'ERROR'])
                
        #         if idx == 1:
        #             raise Exception('\n%s.  Please remove the lock file at the run location' % REMOVE_LOCK)
        #         if idx == 2:
        #             self._process.sendline('')  # enter to continue
        #             self._process.expect('Server listening', timeout=1)
        #         elif idx > 2:
        #             msg = self._process.before
        #             raise Exception('Failed to start local mapdl instance: "%s"' % msg)
        #     except pexpect.EOF:
        #         msg = self._process.before
        #         raise Exception('Failed to start local mapdl instance: "%s"' % msg)
        #     except pexpect.TIMEOUT:
        #         msg = self._process.before
        #         raise Exception('Failed to start local mapdl instance: "%s"' % msg)

        #     self.log.info('Local MAPDL GRPC server listening on localhost:%d', port)


        # if request_instance:
        #     scheduler_ip = ip
        #     if scheduler_ip is None:
        #         # if socket.gethostname() in JUPYTER_HOSTS:
        #         scheduler_ip = INTERNAL_SCHEDULER_IP
        #         # else:
        #             # scheduler_ip = EXTERNAL_SCHEDULER_IP

        #     # assign port when outside the cluster
        #     # assign_port = IN_DEVELOPMENT

        #     manager_port = port
        #     if manager_port is None:
        #         manager_port = MANAGER_PORT

        #     ip, port = request_remote_instance(scheduler_ip,
        #                                        manager_port,
        #                                        n_cpu, ram,
        #                                        custom_command,
        #                                        request_timeout=timeout,
        #                                        instance_timeout=instance_timeout,
        #                                        permit_pending=allow_new_nodes,
        #                                        use_netapp=use_netapp,
        #                                        log=self.log)

        # elif ip is None:
        #     raise ValueError('Must specify an IP and port when request_instance=False')

        # # user has not set a port for a local instance
        # if port is None:
        #     port = MAPDL_DEFAULT_PORT

        # self._processor = 'BEGIN'
        # self._lnum = None
        # self._knum = None

        # # default settings
        # self.allow_ignore = False
        # self._interactive_plotting = False
        # self._store_commands = False
        # self._stored_commands = []
        # self._output = ''
        # self._outfile = None
        # self.continue_on_error = False

        # # Check for valid IP address
        # ip = ip.replace('"', '').replace("'", '')
        
        # socket.inet_aton(ip)

        # # open a connection to the mapdl server
        # self.log.debug(f'Connecting to MAPDL server at {ip}:{port}')
        # server = None
        # for n_attempt in range(10):
        #     try:
        #         server = MapdlGrpc(ip, port)
        #         response = server.send_command('/INQUIRE, , JOBNAME')
        #         job_name = response.split('=')[1].strip()
        #         self.log.info(f'Connected to MAPDL instance with jobname "{job_name}"')
        #     except Exception as exception:
        #         self.log.debug('Connection attempt %d', n_attempt)
        #         time.sleep(0.1)
        #         continue

        #     break

        # if server is None:
        #     server = MapdlGrpc(ip, port)

        # self.server = server
        # self.ip = ip
        # self.port = port
        # self.log.debug('Connected to MAPDL server')
        # self._reader = None

        # # keeps mapdl session alive
        # self._timer = None
        # if keep_alive and not local:
        #     self.initialised = threading.Event()
        #     self._t_trigger = time.time()
        #     self._t_delay = 30
        #     self._timer = threading.Thread(target=Mapdl._threaded_heartbeat,
        #                                    args=(weakref.proxy(self), ))
        #     self._timer.daemon = True
        #     self._timer.start()

        #     while not self.initialised.is_set():
        #         # This loop is necessary to stop the main threading doing anything
        #         # until the exception handler in threaded_func can deal with the
        #         # object being deleted.
        #         pass

        # # print version when requested
        # if print_version:
        #     if request_instance:
        #         print('Acquired remote instance with %d CPUs and %.f GB RAM\n' %
        #               (n_cpu, ram))
        #     print(self)

    @property
    def path(self):
        """Current MAPDL directory"""
        return self.inquire('DIRECTORY')

    @property
    def reader(self):
        """Open mapdl file reader"""
        # send a system command through mapdl to start the mapdl file manager
        from mapdl_file_interface import MapdlFileReader
        if self._reader is None:
            reader_port = 50051
            self.sys(f'/ansys_inc/file_reader/FileMgrReader --address 0.0.0.0 --port {reader_port} &')
            # wait until open
            for _ in range(3):
                try:
                    self._reader = MapdlFileReader(self.ip, reader_port)
                    break
                except:
                    time.sleep(0.1)

        return self._reader

    def _threaded_heartbeat(self):
        """ to be called from a thread"""
        self.initialised.set()
        while True:
            if self._exited:
                break

            try:
                time.sleep(self._t_delay)
                self._heartbeat_tick()
            except ReferenceError:
                break
            except Exception:
                continue

    def list_files(self):
        """List the files in the working directory of the remote mapdl
        instance

        Examples
        --------
        >>> files = mapdl.list_files()
        """
        tmp_file = 'tmp_file'
        self.sys('ls > %s' % tmp_file)
        return self.download_as_raw(tmp_file).decode().splitlines()

    def run(self, command, stream=None, verbose=None):
        """Run a MAPDL command

        Parameters
        ----------
        command : str
            Valid MAPDL command.

        stream : bool, optional
            Stream the response of a command.  Useful when sending
            long running commands like ``"SOLVE"``.

        verbose : bool, optional
            Print the response of a command.  Best when combined with
            ``stream=True`` to print the streamed response of a
            command in real-time.

        Examples
        --------
        >>> mapdl.run('/PREP7')

        Equivalent Pythonic method:

        >>> mapdl.prep7()

        Stream a command

        >>> mapdl.run('SOLVE', stream=True, verbose=True)
        """
        if self._exited:
            raise RuntimeError('MAPDL session ended')

        # TODO: Add command type checking
        return self._run(command, stream=stream, verbose=verbose)

    def _run(self, command, check_response=True, stream=None, verbose=None):
        """Send text command to mapdl server"""
        command_base = command[:4].upper()

        if stream is None:
            verbose = stream = command_base in STREAM_COMMANDS

        self._busy = True
        self._solving = command_base == 'SOLV'
        response = self.server.send_command(command, stream, verbose)

        self._busy = False
        if self._solving:
            self._solving = False

        if check_response:
            self._check_response(response)
        return response

    def _check_response(self, text):
        """Checks test response from ansys and raises an exception or
        warning if applicable
        """
        if 'is not a recognized' in text:
            if not self.allow_ignore:
                lines = text.splitlines()
                for i, line in enumerate(lines):
                    if '*** WARNING ***' in line:
                        break
                try:
                    text = '\n'.join(lines[i+1:-1])
                except:
                    pass

                # this seems more helpful than the default message
                text += '\nThis command may be invalid or you may be in the incorrect processor.'
                raise MapdlException(text)

        elif '*** ERROR ***' in text:  # flag error
            self.log.error(text)
            if not self.continue_on_error:
                raise MapdlException(text)
            elif ignored.search(text):  # flag ignored command
                if not self.allow_ignore:
                    self.log.error(text)
                    raise MapdlException(text)
                else:
                    self.log.warning(text)
            else:
                self.log.info(text)

    @property
    def processor(self):
        """Returns the current processor

        Examples
        --------
        >>> mapdl.processor
        'SOLU'
        """
        msg = self.run('/Status')
        processor = None
        matched_line = [line for line in msg.split('\n') if "Current routine" in line]
        if matched_line:
            # get the processor
            processor = re.findall(r'\(([^)]+)\)', matched_line[0])[0]
        return processor

    def load_parameters(self):
        """Loads and returns all current parameters

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
        self.parsav('all')  # saves to file.parm by default

        fileobj = tempfile.NamedTemporaryFile()
        fileobj.write(self.download_as_raw('file.parm'))
        self.parameters, self.arrays = load_parameters(fileobj.name)
        return self.parameters, self.arrays

    def upload_raw(self, raw, save_as):
        """Uploads a raw stream to a file"""
        self.server.upload_raw(raw, save_as)

    def __del__(self):
        if hasattr(self, '_cleanup'):
            if self._cleanup:
                try:
                    self.exit()
                except:
                    pass

    def _heartbeat_tick(self):
        """Short query to mapdl server to keep connection alive when
        idle.

        Should only be triggered from a thread.
        """
        # only query server when time delay has passed
        if (time.time() - self._t_trigger) > self._t_delay:

            # don't execute when busy
            if self._busy:
                return

            self._t_trigger = time.time()
            self.inquire('JOBNAME')

    @property
    def is_alive(self):
        """True when there is an active connect to the gRPC server"""
        if self._exited:
            return False
        return bool(self.inquire('JOBNAME'))

    @property
    def _result_file(self):
        """Full path to the result file"""
        path = self.inquire('DIRECTORY')
        jobname = self.inquire('JOBNAME')
        return os.path.join(path, f'{jobname}.rst').replace('\\', '/')

    def inquire(self, func):
        """Returns system information

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
        'file'

        Return the result file name

        >>> mapdl.inquire('RSTFILE')
        'file.rst'
        """
        try:
            response = self.run(f'/INQUIRE, , {func}')
            return response.split('=')[1].strip()
        except IndexError:
            raise Exception(f'Cannot parse {response}')

    def __call__(self, command, **kwargs):
        return self.run(command, **kwargs)

    @property
    def keypoints(self):
        """Array of keypoints

        Notes
        -----
        This is directly parsed from the text output of mapdl and is
        not efficient.

        Examples
        --------
        >>> mapdl.k(1, 0, 0, 0)
        >>> mapdl.k(2, 1, 0, 0)
        >>> mapdl.k(3, 0, 1, 0)
        >>> mapdl.k(4, 1, 1, 0)
        >>> mapdl.keypoints
        array([[0., 0., 0.],
               [1., 0., 0.],
               [0., 1., 0.],
               [1., 1., 0.]])
        """
        self.prep7()
        self.header('off', 'off', 'off', 'off', 'off', 'off')
        self.page(10000000)

        lines = self.klist().splitlines()
        if 'No keypoints to list' in lines[2]:
            return None

        for i, line in enumerate(lines):
            values = line.split()
            if values:
                if is_float(values[0]):
                    break

        array = np.genfromtxt(lines[i:], usecols=[0, 1, 2, 3])

        if array.ndim > 1:
            self._knum = array[:, 0].astype(np.int32)
            return array[:, 1:]
        else:
            self._knum = np.array([array[0].astype(np.int32)])
            return array[1:]

    @property
    def knum(self):
        """List keypoint numbers as an array

        Notes
        -----
        This is directly parsed from the text output of mapdl and is
        not efficient.

        Examples
        --------
        >>> mapdl.k(1, 0, 0, 0)
        >>> mapdl.k(2, 1, 0, 0)
        >>> mapdl.k(3, 0, 1, 0)
        >>> mapdl.k(4, 1, 1, 0)
        >>> mapdl.knum
        array([1, 2, 3, 4], dtype=int32)
        """
        self.keypoints
        return self._knum

    def kplot(self, color='k'):
        """Plot keypoints

        Examples
        --------
        >>> mapdl.kplot()
        """
        keypoints = self.keypoints
        if keypoints is None:
            raise Exception('No keypoints to plot')
        points = pv.PolyData(keypoints)

        if ITK_PLOTTING:
            pl = pv.PlotterITK()
        else:
            pl = pv.Plotter()
            pl.add_point_labels(points, self.knum, font_size=18)

        pl.add_points(points, color=color)
        return pl.show()

    @property
    def lines(self):
        """Return an array of lines

        Notes
        -----
        This is directly parsed from the text output of mapdl and is
        not efficient.

        Examples
        --------
        >>> mapdl.k(1, 0, 0, 0)
        >>> mapdl.k(2, 1, 0, 0)
        >>> mapdl.k(3, 0, 1, 0)
        >>> mapdl.k(4, 1, 1, 0)
        >>> mapdl.l(1, 2)
        >>> mapdl.l(2, 3)
        >>> mapdl.l(3, 4)
        >>> mapdl.l(4, 1)
        >>> mapdl.knum
        array([[1, 2],
               [2, 3],
               [3, 4],
               [4, 1]], dtype=int32)
        """
        self.prep7()
        self.header('off', 'off', 'off', 'off', 'off', 'off')
        self.page(10000000)

        raw = self.llist().splitlines()
        for i, line in enumerate(raw):
            values = line.split()
            if values:
                if is_float(values[0]):
                    break

        array = np.genfromtxt(raw[i:], usecols=[0, 1, 2], dtype=np.int32)
        self._lnum = array[:, 0].astype(np.int32)
        return array[:, 1:]

    # @property
    # def lnum(self):
    #     if self._num is None:
    #         self.keypoints()
    #     return self._lnum

    def lplot(self, keypoint_num=True, **kwargs):
        """Plot lines

        Examples
        --------
        >>> mapdl.lplot()
        """
        if self.knum is None:
            raise Exception('No lines to plot')
        ref_arr = np.empty(self.knum.max() + 1, np.int32)
        ref_arr[self.knum] = np.arange(self.knum.size, dtype=np.int32)

        ansys_lines = self.lines  # ansys line numbering
        lines = np.empty((ansys_lines.shape[0], 3), np.int32)
        lines[:, 0] = 2
        lines[:, 1:] = ref_arr[self.lines]

        points = self.keypoints
        plines = pv.PolyData(points, lines)

        if ITK_PLOTTING:
            pl = pv.PlotterITK()
            pl.add_mesh(plines)
        else:
            pl = pv.Plotter()
            pl.show_axes()
            pl.camera_position = 'xy'
            if keypoint_num:
                pl.add_point_labels(points, self.knum, font_size=18)
            pl.add_mesh(plines, style='wireframe')

        return pl.show()

    @property
    def nodes(self):
        """Returns an array of selected nodes from mapdl.

        Examples
        --------
        >>> mapdl.nodes
        array([[3.00547952, 4.655     , 2.33184666],
               [2.71478268, 4.655     , 2.24375556],
               [2.93280531, 4.655     , 2.30982389],
               ...,
               [0.02401957, 3.93939353, 1.33490496],
               [0.9570203 , 4.60965857, 0.70304662],
               [1.09840106, 5.34088837, 1.19770979]])
        """
        if not self.n_node:
            raise RuntimeError('No nodes in model or no nodes selected')

        return self.server.load_nodes()

    @property
    def nnum(self):
        """Array of node numbers from selected nodes in mapdl.

        Examples
        --------
        >>> mapdl.nnum
        array([    1,     2,     3, ..., 40906, 40907, 40908], dtype=int32)

        """
        return self.vget('NODE', 'NLIST').astype(np.int32)

    @property
    def nodal_eqv_stress(self):
        """Return the nodal equivalent stress

        Equilvanent command:
        ``*VGET, TMPVAR, NODE, 1, S, EQV``
        or
        ``PRNSOL, S, EQV``

        Examples
        --------
        >>> mapdl.nodal_eqv_stress
        array([0., 0., 0., ..., 0., 0., 0.])

        Stress from result 2

        >>> mapdl.post1()
        >>> mapdl.set(2)
        >>> mapdl.nodal_eqv_stress
        array([0., 0., 0., ..., 0., 0., 0.])
        """
        return self.vget('NODE', 'S', 'EQV')

    def plot_node_vget(self, item=None, itnum=None, **kwargs):
        """Plot vector data from the MAPDL server.

        Please concult your ANSYS manual for the various VGET outputs.

        Parameters
        ----------
        item : str
            The name of a particular item for the given entity. Valid
            items are as shown in the item columns of the tables
            within the ``*VGET`` command reference in your ANSYS
            manual.

        itnum : str
            The number (or label) for the specified item (if
            any). Valid it1num values are as shown in the IT1NUM
            columns of the tables in the command reference section for
            the ``*VGET`` command in your ANSYS manual. Some Item1
            labels do not require an IT1NUM value.

        Examples
        --------
        Plot node averaged equivalent stress for a model

        >>> mapdl.plot_node_vget('NODE', 'S', 'EQV')

        # Plot displacements in the X direction

        >>> mapdl.plot_node_vget('NODE', 'U', 'X')
        """
        values = self.vget('NODE', item, itnum)
        return self._plot_point_scalars(values, **kwargs)

    def vget(self, entity, item=None, itnum=None):
        """Retrieve vector data from the MAPDL server and return a
        numpy array.

        Please concult your ANSYS manual for the various VGET outputs.

        Parameters
        ----------
        entity : str
            Entity keyword. Valid keywords are:

            - ``'NODE'``
            - ``'ELEM'``
            - ``'KP'``
            - ``'LINE'``
            - ``'AREA'``
            - ``'VOLU'``
            - ``'CDSY'``
            - ``'RCON'``
            - ``'TLAB'``

        item : str
            The name of a particular item for the given entity. Valid
            items are as shown in the item columns of the tables
            within the ``*VGET`` command reference in your ANSYS manual.

        itnum : str
            The number (or label) for the specified item (if
            any). Valid it1num values are as shown in the IT1NUM
            columns of the tables in the command reference section for
            the ``*VGET`` command in your ANSYS manual. Some Item1 labels
            do not require an IT1NUM value.

        Examples
        --------
        Output node averaged equivalent stress for a model

        >>> mapdl.vget('NODE', 'S', 'EQV')

        Nodal displacements in the X direction

        >>> mapdl.vget('NODE', 'U', 'X')
        """
        entity = entity.upper()
        if item is not None:
            item = item.upper()

        if itnum is not None:
            itnum = itnum.upper()

        if entity not in VGET_ENTITY_TYPES:
            raise ValueError(f'Entity "{entity}" not allowed.  Allowed items:\n' +
                             f'{VGET_ENTITY_TYPES}')

        if entity == 'NODE':
            if item not in VGET_NODE_ENTITY_TYPES:
                allowed_types = list(VGET_NODE_ENTITY_TYPES.keys())
                raise ValueError(f'item "{item}" for "NODE" not allowed.  ' +
                                 f'Allowed items:\n{allowed_types}')

            if itnum not in VGET_NODE_ENTITY_TYPES[item]:
                allowed_types = VGET_NODE_ENTITY_TYPES[item]
                raise ValueError(f'itnum "{itnum}" for item "{item}" not allowed.  ' +
                                 f'Allowed items:\n{allowed_types}')

        if item is None:
            item = ""

        if itnum is None:
            itnum = ""

        # self.log.debug('Sending %s', f'*VGET, {entity}, , {item}, {itnum}')
        return self.server.vget(f'{entity}, , {item}, {itnum}')

    @property
    def enum(self):
        """Returns the array of selected element numbers

        Examples
        --------
        >>> mapdl.enum
        array([    1,     2,     3, ..., 26355, 26356, 26357], dtype=int32)
        """
        return self.vget('ELEM', 'ELIST').astype(np.int32)

    def plot_nodal_eqv_stress(self, **kwargs):
        """Plot nodal equivalent stress

        Examples
        --------
        >>> mapdl.plot_nodal_eqv_stress()
        """
        return self._plot_point_scalars(self.nodal_eqv_stress, **kwargs)

    def nodal_displacement(self, component='NORM', **kwargs):
        """Retrieve nodal displacment

        Parameters
        ----------
        component : str
            Displacement component to plot.  Must be 'X', 'Y', 'Z', or
            'NORM'.

        Examples
        --------
        >>> mapdl.nodal_displacement('X')

        Displacement in all dimensions

        >>> mapdl.nodal_displacement('NORM')
        """
        if component.lower() == 'norm':
            x = self.vget('node', 'U', 'x')
            y = self.vget('node', 'U', 'y')
            z = self.vget('node', 'U', 'z')
            scalars = np.linalg.norm(np.vstack((x, y, z)), axis=0)
        else:
            scalars = self.vget('node', 'U', component)

        return scalars

    def plot_nodal_displacement(self, component='NORM', **kwargs):
        """Plot nodal displacment

        Parameters
        ----------
        component : str
            Displacement component to plot.  Must be 'X', 'Y', 'Z', or
            'SUM'.

        Examples
        --------
        >>> mapdl.plot_nodal_displacement('NORM')

        """
        # disp = self.vget('node', 'U', component)
        return self._plot_point_scalars(self.nodal_displacement(component), **kwargs)

    def _plot_point_scalars(self, scalars, grid=None,
                            show_displacement=False,
                            displacement_factor=1,
                            rnum=None,
                            # add_text=True,
                            # animate=False,
                            # nangles=100,
                            # movie_filename=None,
                            # max_disp=0.1,
                            **kwargs):
        """Plot point scalars on active mesh.

        Parameters
        ----------
        scalars : np.ndarray
            Node scalars to plot.

        rnum : int, optional
            Cumulative result number.  Used for adding informative
            text.

        grid : pyvista.PolyData or pyvista.UnstructuredGrid, optional
            Uses self.grid by default.  When specified, uses this grid
            instead.

        show_displacement : bool, optional
            Deforms mesh according to the result.

        displacement_factor : float, optional
            Increases or decreases displacement by a factor.

        add_text : bool, optional
            Adds information about the result when rnum is given.

        kwargs : keyword arguments
            Additional keyword arguments.  See help(pyvista.plot)

        Returns
        -------
        cpos : list
            Camera position.
        """
        if grid is None:
            grid = self.grid

        disp = None
        if show_displacement:  # and not animate:
            nsln = self.nodal_solution(rnum)[:, :3]*displacement_factor
            # disp = self.nodal_solution(rnum)[:, :3]
            new_points = grid.points.copy()
            dofs = set(self.dofs(0))
            if set(['UX', 'UY', 'UZ']).issubset(dofs):
                new_points += nsln
            elif set(['UX', 'UY']).issubset(dofs):
                new_points[:, :2] += nsln[:, :2]
            elif 'UX' in dofs:
                new_points[:, 0] += nsln[:, 0]
            grid = grid.copy()
            grid.points = new_points
        # elif animate:
        #     disp = self.nodal_solution(rnum)[1][:, :3]

        # extract mesh surface
        mapped_indices = None
        if 'vtkOriginalPointIds' in grid.point_arrays:
            mapped_indices = grid.point_arrays['vtkOriginalPointIds']

        mesh = grid.extract_surface()
        ind = mesh.point_arrays['vtkOriginalPointIds']
        if disp is not None:
            if mapped_indices is not None:
                disp = disp[mapped_indices][ind]
            else:
                disp = disp[ind]

            # if animate:  # scale for max displacement
            #     disp /= (np.abs(disp).max()/max_disp)

        if scalars is not None:
            if scalars.ndim == 2:
                scalars = scalars[:, ind]
            else:
                scalars = scalars[ind]

            rng = kwargs.pop('rng', [scalars.min(), scalars.max()])
        else:
            rng = kwargs.pop('rng', None)

        # add_text = kwargs.pop('add_text', True)
        cmap = kwargs.pop('cmap', 'jet')
        smooth_shading = kwargs.pop('smooth_shading', True)
        cpos = kwargs.pop('cpos', None)
        interpolate_before_map = kwargs.pop('interpolate_before_map', True)
        stitle = kwargs.pop('stitle', None)

        if ITK_PLOTTING:
            pl = pv.PlotterITK()
        else:
            pl = pv.Plotter()

        if kwargs.pop('overlay_wireframe', False):
            pl.add_mesh(self.grid,
                        color='w',
                        style='wireframe',
                        opacity=0.5)

        copied_mesh = mesh.copy(False)
        copied_mesh.clear_arrays()
        copied_mesh['stitle'] = scalars
        if ITK_PLOTTING:
            pl.add_mesh(copied_mesh)
        else:
            pl.add_mesh(copied_mesh,
                        rng=rng,
                        smooth_shading=smooth_shading,
                        interpolate_before_map=interpolate_before_map,
                        stitle=stitle,
                        cmap=cmap,
                        **kwargs)
            # if cpos:

        return pl.show()

    def eplot(self, notebook=True, **kwargs):
        """Plot elements

        Parameters
        ----------
        notebook : bool, optional
            When ``True`` plots within the notebook if within a jupyter
            notebook.

        **kwargs : various, optional
            See ``help(pyvista.plot)`` for additional keyword arguments.

        Examples
        --------
        >>> mapdl.eplot()
        """
        if ITK_PLOTTING and notebook:
            check_itk()
            pl = pv.PlotterITK()
        else:
            pl = pv.Plotter()

        pl.add_mesh(self.grid, **kwargs)
        return pl.show()

        # show_edges = kwargs.pop('show_edges', True)

        # if show_nodes:
        #     pl.add_point_labels(self.nodes, self.nnum, font_size=18)
        #     pl.add_mesh(self.grid, show_edges=show_edges, **kwargs)
        #     pl.show()
        # else:
        #     pl.add_mesh(self.grid, show_edges=show_edges)
        #     pl.show()

    def nplot(self, color='k', notebook=True):
        """Plot nodes

        Parameters
        ----------
        color : str
            Color string.  See `matplotlib` colors.

        notebook : bool, optional
            When `True` plots within the notebook if using juptyerlab.

        Examples
        --------
        >>> mapdl.nplot()

        Plot as blue points

        >>> mapdl.nplot('b')
        """
        if ITK_PLOTTING and notebook:
            pl = pv.PlotterITK()
        else:
            pl = pv.Plotter()

        # if show_numbers:
        #     pl.add_point_labels(self.nodes, self.nnum, font_size=18)
        #     pl.plot()
        # else:
        pl.add_points(self.nodes, color=color)
        return pl.show()

    @property
    def grid(self):
        """VTK unstructured grid of MAPDL mesh"""
        if not self.n_elem:
            raise RuntimeError('No elements in model or no elements selected')

        self._quad_grid = self._py_load_vtk_geometry()
        self._grid = self._quad_grid.linear_copy(deep=False)

        return self._grid

    @property
    def elements(self):
        """List of mapdl elements

        Returns
        -------
        elements : list
            Each element contains 10 items plus the nodes belonging to the
            element.  The first 10 items are:

            - mat -  material reference number
            - type - element type number
            - real - real constant reference number
            - secnum - section number
            - esys - element coordinate system
            - death - death flag (0 - alive, 1 - dead)
            - solidm - solid model reference
            - shape - coded shape key
            - elnum - element number
            - baseeid - base element number (applicable to reinforcing
                        elements only) nodes - node numbers defining
                        the element
            - nodes - The nodes belonging to the element

        """
        return self.server.load_elements()

    def _py_load_vtk_geometry(self):
        """Convert raw MAPDL data into a VTK UnstructuredGrid"""
        elem, elem_off = self.server.load_elements_offset()

        edes = self.server.load_elementtypes()
        ekey = np.vstack([einfo[:2] for einfo in edes]).astype(np.int32)
        geometry = Geometry(self.nnum, self.nodes, elem, elem_off, ekey)
        return geometry._parse_vtk()

    def open_result(self, filename=None):
        """Return a mapdl result file as a mapdl file reader object

        Examples
        --------
        >>> result = mapdl.open_result()
        """
        # Check result file exists
        if filename is None:
            filename = self._result_file

        self.reader.open_file(filename)
        return self.reader

    def _kill(self):
        """Causes the mapdl server to exit"""
        self.finish()

        def target():
            try:
                self.run('exit')
            except:
                pass

        thread = threading.Thread(target=target)
        thread.start()

    def input(self, filename, verbose=True, progress_bar=True, mute=False):
        """Run a local input file on the mapdl server.

        Parameters
        ----------
        filename : str
            Local batch file to read.

        verbose : bool, optional
            Stream and print back the response of the input file while
            it is being run.

        progress_bar : bool, optional
            Display a progress bar showing the progress of the file
            upload.

        Notes
        -----
        Avoid the /EXIT command when inputting an input file if you
        would like to continue to interact with the mapdl instance.

        Examples
        --------
        >>> output = mapdl.input(filename)

        Disable printing output while streaming

        >>> output = mapdl.input(filename, verbose=False)
        """
        # must use an absolute path when sending the file
        if not os.path.isabs(filename):
            filename = os.path.join(os.getcwd(), filename)

        if not os.path.isfile(filename):
            raise FileNotFoundError(f"Local file '{filename}' not found")

        self._busy = True
        self.log.info('Running input file %s', filename)

        response = self.server.input_file(filename, verbose, progress_bar, mute)

        self._busy = False

        return response

    def input_text(self, text, chunk_nlines=20, join=True):
        """Run a series of mapdl commands separated by line breaks.

        Parameters
        ----------
        text : str
            MAPDL text commands.

        Notes
        -----
        Avoid the /EXIT command if you would like to continue to
        interact with the mapdl instance.

        Examples
        --------
        >>> text = '/CLEAR\nPREP7\n'
        >>> output = mapdl.input_text(text)

        """
        self._busy = True
        response = self.server.input_text(text, chunk_nlines, join)
        self._busy = False
        return response

    def exit(self):
        """Exit MAPDL instance

        Examples
        --------
        >>> mapdl.exit()
        """
        if hasattr(self, '_exited'):
            if not self._exited:
                self._exit()
                self._exited = True

        # remove the lock file if local
        if hasattr(self, '_local'):
            if self._local:
                try:
                    lock_file = os.path.join(self._run_location, 'file.lock')
                    if os.path.isfile(lock_file):
                        os.remove(lock_file)
                except:
                    pass

    def _exit(self):
        """Send exit command"""
        if self.server:
            # self.log.debug('Sending grpc exit command')
            self.server.ctrl('EXIT')

    def upload(self, filename, progress_bar=True):
        """Upload a local file to the remote mapdl instance

        Parameters
        ----------
        filename : str
            Local file to upload.

        progress_bar : bool, optional
            Display a progress bar showing the progress of the file
            upload.

        Examples
        --------
        Load a local database by uploading it to the remote mapdl instance

        >>> import ansys
        >>> mapdl = ansys.Mapdl()
        >>> mapdl.upload('my_database.db')
        >>> mapdl.resume('my_database.db')
        """
        if not os.path.isfile(filename):
            raise FileNotFoundError('Unable to find local file %s' % filename)
        self.server.upload(filename, progress_bar=progress_bar)

    def download(self, remote_filename, save_as=None, chsize=1024*64,
                 progress_bar=True):
        """Download a remote file

        Parameters
        ----------
        remote_filename : str
            Remote file to upload

        save_as : str, optional
            Optionally specify the save name of the file.  If
            unspecified, saves the file name as the same name as the
            remote file.

        chsize : int, optional
            Size of the chunks sent from the gRPC server.

        Examples
        --------
        >>> mapdl.download('file.rst')
        """
        saved_file = self.server.download(remote_filename, save_as, chsize,
                                          progress_bar=progress_bar)

        # failed downloads result in an empty file
        if not os.path.getsize(saved_file):
            os.remove(saved_file)
            raise FileNotFoundError('File does not exist remotely, or file is empty')

    def download_as_raw(self, target_name):
        """Download a file from the grpc instance as a binary raw
        string.

        Parameters
        ----------
        remote_filename : str
            Remote file to upload

        Returns
        raw_text : str
            File as a binary stream.

        Examples
        --------
        Send a command to the remote mapdl instance and download the response

        >>> mapdl.sys('ls >> tmp.file')
        >>> remote_files = mapdl.download_as_raw('tmp.file')
        """
        return self.server.download_as_raw(target_name)

    def math(self):
        """Returns a mapdl math object

        Examples
        --------
        >>> from ansys import Mapdl
        >>> mapdl = Mapdl()
        >>> mm = mapdl.math()
        """
        from ansys.mapdl import MapdlMath
        return MapdlMath(self)

    def xpl(self):
        """Returns an xpl object, to explore MAPDL Files

        Examples
        --------
        >>> from ansys import Mapdl
        >>> mapdl = Mapdl()
        >>> xpl = mapdl.xpl()
        """
        from ansys.mapdl import ansXpl
        return ansXpl(self)

    def scalar_param(self, pname):
        """Return a scalar parameter

        Notes
        -----
        List of all scalar parameters can be obtained from
        ``mapdl.load_parameters``

        Examples
        --------
        >>> mapdl.scalar_param('_WB_USERFILES_DIR')
        'B:\\databases\\demo\\files\\'
        """
        return self.server.scalar_param(pname)

    def data_info(self, pname):
        """Return infos on an APDLMath Object

        Parameters
        ----------
        pname : str
            APDLMath parameter name

        """
        return self.server.data_info(pname)

    def vec_data(self, pname):
        """Return the values of an APDLMath Vector as a numpy array

        Parameters
        ----------
        pname : str
            APDLMath parameter name

        """
        return self.server.vec_data(pname)

    def set_vec(self, vname, data):
        """Push a numpy array or python list to the MAPDL Memory
        Workspace.

        Parameters
        ----------
        vname : str
            APDLMath vector name

        data : np.ndarray, list
            Numpy array or Python list to push to MAPDL.  Must be 1
            dimensional.

        """
        if isinstance(data, list):
            array = np.array(data)
        elif isinstance(data, np.ndarray):
            array = data
        else:
            raise TypeError('``data`` must be np.ndarray or a list')

        is_1d = sum([dim != 1 for dim in data.shape])
        if not is_1d:
            raise ValueError('``data`` must be a 1 dimensional vector')

        self.server.set_vec(vname, array)

    def mat_data(self, pname):
        """Return the values of an APDLMath Matrix as a numpy array

        Parameters
        ----------
        pname : str
            APDLMath parameter name

        """
        return self.server.mat_data(pname)

    @property
    def version(self):
        """Return ANSYS and pyansys versions

        Examples
        --------
        >>> print(mapdl.version)
        """
        stats = self.slashstatus()
        st = stats.find('BUILD') + 5
        en = stats.find('CUSTOMER')
        ansys_version = stats[st:en].strip()
        return 'ANSYS version:   %s\npyansys version: %s' % (ansys_version, __version__)


    @property
    def n_node(self):
        """Number of currently selected nodes"""
        return int(self.server.Get('NODE, , COUNT'))

    @property
    def n_elem(self):
        """Number of currently selected nodes"""
        return int(self.server.Get('ELEM, , COUNT'))


    def check_available(self, timeout=5):
        """Check if the mapdl instance is available

        Parameters
        ----------
        timeout : float
            Timeout in seconds for the request.

        Returns
        -------
        available : bool
            True when the instance is available.  False when the
            request takes longer than `timeout`.
        """
        # reset check flag
        self._check_flag = False

        # start available checking thread
        self._check_available()
        tstart = time.time()
        while not self._check_flag and not self._exited:
            time.sleep(0.05)

            # exit early when timeout exceeded
            telap = time.time() - tstart
            if telap > timeout:
                break

        return self._check_flag

    @threaded
    def _check_available(self):
        """Attempts to query jobname and verifying that there's a
        connection open to the mapdl instance"""
        try:
            self.inquire('JOBNAME')
            self._check_flag = True
        except Exception as e:
            self.log.error('Instance unavailable', exc_info=True)
            self._exited = True

    def retrieve_parameter(self, parameter):
        """TODO: Write grpc function to retrieve single parameters"""
        response = self.starstatus(parameter)

        value = None
        if response:
            if 'LOCATION' in response:
                return self._parse_array_parameter(parameter, response)

            values = response.split('DIMENSIONS')[-1].split()
            ptype = values[-1]

            value = None
            if len(values) > 2:
                value = values[1]

            if ptype == 'CHARACTER':
                if value is None:
                    value = ''
            elif ptype == 'SCALAR':
                value = float(value)

        return value

    def _parse_array_parameter(self, parameter, response):
        lines = response.splitlines()
        for i, line in enumerate(lines):
            if 'LOCATION' in line:
                i += 1
                break

        para_ind = re.findall(r'\((.*?)\)$', parameter)[0]
        tgt_ind = parse_fortran_index(*para_ind.split(','))

        # searching for a target index
        if tgt_ind:
            for line in lines[i:]:
                # broken up as i_index, j_index, k_index, value, type
                ind = parse_fortran_index(*line.split()[:3])
                if ind == tgt_ind:
                    break

            if ind == tgt_ind:
                items = line.split()[3:]
                if len(items) == 1:
                    value, ptype = None, items[0]
                else:
                    value, ptype = items

                if ptype == '(Char)':
                    if value is None:
                        value = ''
                    return value
                else:
                    raise NotImplementedError
            else:
                return
