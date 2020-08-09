"""gRPC specific class and methods for the MAPDL gRPC client
"""
import threading
import weakref
import io
import time
import logging
import os
import socket
from threading import Timer
from functools import wraps

import grpc
import numpy as np
from tqdm import tqdm

from pyansys.mapdl import _MapdlCore
from pyansys.errors import MapdlRuntimeError
from pyansys.common_grpc import (parse_chunks,
                                 ANSYS_VALUE_TYPE,
                                 DEFAULT_CHUNKSIZE,
                                 DEFAULT_FILE_CHUNK_SIZE,
                                 check_vget_input)

from ansys.grpc.mapdl import mapdl_pb2 as pb_types
from ansys.grpc.mapdl import mapdl_pb2_grpc as mapdl_grpc
from ansys.grpc.mapdl import ansys_kernel_pb2 as anskernel

logger = logging.getLogger(__name__)

VOID_REQUEST = anskernel.EmptyRequest()

NP_VALUE_TYPE = {value: key for key, value in ANSYS_VALUE_TYPE.items()}


def chunk_raw(raw, save_as):
    with io.BytesIO(raw) as f:
        while True:
            piece = f.read(DEFAULT_FILE_CHUNK_SIZE)
            length = len(piece)
            if length == 0:
                return
            yield pb_types.UploadFileRequest(file_name=os.path.basename(save_as),
                                             chunk=anskernel.Chunk(payload=piece,
                                                                   size=length))


def get_file_chunks(filename, progress_bar=False):
    """Serializes a file into chunks"""
    pbar = None
    if progress_bar:
        n_bytes = os.path.getsize(filename)

        base_name = os.path.basename(filename)
        pbar = tqdm(total=n_bytes, desc='Uploading %s' % base_name,
                    unit='B', unit_scale=True, unit_divisor=1024)

    with open(filename, 'rb') as f:
        while True:
            piece = f.read(DEFAULT_FILE_CHUNK_SIZE)
            length = len(piece)
            if length == 0:
                if pbar is not None:
                    pbar.close()
                return

            if pbar is not None:
                pbar.update(length)

            chunk = anskernel.Chunk(payload=piece, size=length)
            yield pb_types.UploadFileRequest(file_name=os.path.basename(filename),
                                             chunk=chunk)


def save_chunks_to_file(chunks, filename, progress_bar=True,
                        file_size=None, target_name=''):
    """Saves chunks to a local file"""
    pbar = None
    if progress_bar:
        pbar = tqdm(total=file_size, desc='Downloading %s' % target_name,
                    unit='B', unit_scale=True, unit_divisor=1024)

    with open(filename, 'wb') as f:
        for chunk in chunks:
            f.write(chunk.payload)
            if pbar is not None:
                pbar.update(len(chunk.payload))

    if pbar is not None:
        pbar.close()


def chunk_commands(l, n):
    """Yield successive n-sized cmdrequests from iterator l"""
    for i in range(0, len(l), n):
        line_block = ''.join(l[i:i + n])
        if '/EXIT' in line_block:
            raise Exception('Invalid command "/EXIT" in input file')
        yield pb_types.CmdRequest(command=line_block)


def chunk_lines(lines, n):
    for i in range(0, len(lines), n):
        line_block = ''.join(lines[i:i + n])
        if '/EXIT' in line_block:
            raise Exception('Invalid command "/EXIT" in input file')
        yield pb_types.CmdRequest(command=line_block)


def chunk_by_lines(file_object, nlines):
    """ Read in a file by line chunks

    Parameters
    ----------
    file_object : Python file object
        Python file object to chunk

    nlines : int
        Number of lines to read at a time.  Optimally between 10 and
        100

    Returns
    -------
    chunks : generator
        Generator containing chunks of the file object.
    """
    return chunk_commands(file_object.readlines(), nlines)


class RepeatingTimer(Timer):
    def run(self):
        while not self.finished.is_set():
            self.function(*self.args, **self.kwargs)
            self.finished.wait(self.interval)


def get_nparray_chunks(name, nparray):
    """Serializes a numpy array into chunks"""
    vsize = nparray.size
    dt = nparray.dtype
    csize = DEFAULT_FILE_CHUNK_SIZE
    itemsize = nparray.itemsize
    nvals = int(csize/itemsize)
    type = NP_VALUE_TYPE[dt.type]
    first = 0
    last = -1
    while True:
        first = last+1
        last = min(vsize, first+nvals)
        if first >= last:
            return
        piece = nparray[first:last]
        length = len(piece)*itemsize
        chunk = anskernel.Chunk(payload=piece.tobytes(), size=length)
        yield pb_types.SetVecDataRequest(vname=name, stype=type, size=vsize,
                                         chunk=chunk)


def check_valid_ip(ip):
    """Check for valid IP address"""
    if ip != 'localhost':
        ip = ip.replace('"', '').replace("'", '')
        socket.inet_aton(ip)


class MapdlGrpc(_MapdlCore):
    """This class connects to a GRPC MAPDL server and allows commands
    to be passed to a persistent session.

    Parameters
    ----------
    ip : str, optional
        IP address to connnect to the server.  Defaults to 'localhost'.

    port : int, optional
        Port to connect to the mapdl server.  Defaults to 50052.

    timeout : float
        Maximum allowable time to connect to the MAPDL server.

    loglevel : str, optional
        Sets which messages are printed to the console.  Default
        'INFO' prints out all ANSYS messages, 'WARNING` prints only
        messages containing ANSYS warnings, and 'ERROR' prints only
        error messages.

    cleanup_on_exit : bool, optional
        Exit MAPDL when python exits or the mapdl Python instance is
        garbage collected.

    Examples
    --------
    Connect to an instance of MAPDL running on localhost

    >>> from pyansys.mapdl_grpc import MapdlGrpc
    >>> MapdlGrpc('127.0.0.1', port=50052)

    Connect to an instance of MAPDL running on the LAN

    >>> from pyansys.mapdl_grpc import MapdlGrpc
    >>> MapdlGrpc('192.168.1.101', port=50052)

    """

    def __init__(self, ip='127.0.0.1', port=50052, timeout=15, loglevel='INFO',
                 cleanup_on_exit=True, **kwargs):
        """Initialize connection to the mapdl server"""
        super().__init__(loglevel)
        self._vget_lock = False
        self._get_lock = False

        self._stub = None
        self._cleanup = cleanup_on_exit
        self._jobname = kwargs.pop('jobname', 'file')
        self._path = kwargs.pop('run_location', None)

        check_valid_ip(ip)
        self._local = ip in ['127.0.0.1', '127.0.1.1', 'localhost']

        self._redirected_commands = {}

        self._channel_str = '%s:%d' % (ip, port)
        self._log.debug('Opening insecure channel at %s', self._channel_str)

        self.channel = grpc.insecure_channel(self._channel_str)
        self._state = grpc.channel_ready_future(self.channel)
        self._stub = mapdl_grpc.MapdlServiceStub(self.channel)

        # verify connection
        tstart = time.time()
        while ((time.time() - tstart) < timeout) and not self._state._matured:
            time.sleep(0.01)

        if not self._state._matured:
            raise IOError('Unable to connect to MAPDL gRPC instance at %s' %
                          self._channel_str)
        self._log.debug('Established connection to MAPDL gRPC')

        # keeps mapdl session alive
        self._timer = None
        if not self._local:
            self._initialised = threading.Event()
            self._t_trigger = time.time()
            self._t_delay = 30
            self._timer = threading.Thread(target=MapdlGrpc._threaded_heartbeat,
                                           args=(weakref.proxy(self), ))
            self._timer.daemon = True
            self._timer.start()

        # import needs to be here to avoid recursive import
        from pyansys.geometry_grpc import GeometryGrpc
        self._geometry = GeometryGrpc(self)

    def _reset_cache(self):
        """Reset cached items"""
        self._geometry._reset_cache()

    @property
    def mesh(self):
        """MAPDL geometry"""
        return self._geometry

    def _run(self, cmd, stream=False, verbose=False, mute=False):
        """Sends a command and returns the response as a string.

        Parameters
        ----------
        cmd : str
            Valid MAPDL command.

        stream : bool, optional
            Stream the response of a command.  Useful when sending
            long running commands like ``"SOLVE"``.

        verbose : bool, optional
            Print the response of a command.  Best when combined with
            ``stream=True`` to stream a command in real-time.

        mute : bool, optional
            Request that no output be generated from the gRPC server.
        """
        if self._exited:
            raise MapdlException('MAPDL session ended')

        if stream:
            return self._send_command_stream(cmd, verbose)
        return self._send_command(cmd, verbose, mute=mute)

    def _send_command(self, cmd, verbose=False, mute=False):
        """Send a MAPDL command and return the response as a string"""
        opt = ''
        if mute:
            opt = 'MUTE'  # supress any output

        request = pb_types.CmdRequest(command=cmd, opt=opt)
        try:
            cmd_response = self._stub.SendCommand(request)
        except Exception as exception:
            if 'status = StatusCode.UNAVAILABLE' in str(exception):
                raise Exception('Server connection terminated')
            else:
                raise exception

        response = cmd_response.response
        if verbose:
            print(response)
        return response

    def _send_command_stream(self, cmd, verbose=False):
        """Send a command and expect a streaming response"""
        request = pb_types.CmdRequest(command=cmd)
        metadata = [('time_step_stream', '100')]
        stream = self._stub.SendCommandS(request, metadata=metadata)
        response = []
        for item in stream:
            cmdout = '\n'.join(item.cmdout)
            if verbose:
                print(cmdout)
            response.append(cmdout)

        return ''.join(response)

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

    def exit(self):
        """Exit MAPDL instance

        Examples
        --------
        >>> mapdl.exit()
        """
        self._log.debug('Exiting MAPDL')
        if not self._exited:
            try:  # allow this to fail
                self._ctrl('EXIT')
            except:
                pass
            self._exited = True

        # remove the lock file if local
        if self._local:
            if os.path.isfile(self._lockfile):
                os.remove(self._lockfile)

    def list_files(self):
        """List the files in the working directory of the remote mapdl
        instance

        Examples
        --------
        >>> files = mapdl.list_files()
        """
        tmp_file = 'tmp_file'
        if self._os == 'nt':
            cmd = 'ls'
        else:
            cmd = 'dir'
        self.sys('ls > %s' % (cmd, tmp_file))
        return self.download_as_raw(tmp_file).decode().splitlines()

    def _ctrl(self, cmd):
        """Issue control command to the mapdl server

        Available commands:

        - 'EXIT'
            Calls exit(0) on the server.

        - 'set_verb'
            Enables verbose mode on the server.

        Unavailable/Flaky:

        - 'time_stats'
            Prints a table for time stats on the server.
            This command appears to be disabled/broken.

        - 'mem-stats'
            To be added

        """
        self._log.debug('Issuing CtrlRequest "%s"', cmd)
        request = anskernel.CtrlRequest(ctrl=cmd)

        # handle socket closing upon exit
        if cmd.lower() == 'exit':
            try:
                self._stub.Ctrl(request)
            except:  # this always returns an error as the connection is closed
                pass
            return

        # otherwise, simply send command
        self._stub.Ctrl(request)

    @wraps(_MapdlCore.cdread)
    def cdread(self, *args, **kwargs):
        """Wraps CDREAD"""
        option = kwargs.get('option', args[0])
        if option == 'ALL':
            raise ValueError('Option "ALL" not supported in gRPC mode.  Please '
                             'Input the geometry and mesh files separately '
                             'with "\INPUT" or ``mapdl.input``')

        fname = kwargs.get('fname', args[1])
        kwargs.setdefault('verbose', False)
        kwargs.setdefault('progress_bar', False)
        self.input(fname, **kwargs)

    def input(self, fname, verbose=True, progress_bar=True, mute=False):
        """Stream a local input file to a remote mapdl instance.
        Stream the response back and deserialize the output.

        Parameters
        ----------
        fname : str
            MAPDL input file to stream to the MAPDL grpc server.

        Returns
        -------
        response : str
            Response from MAPDL.

        Notes
        -----
        RPC calls are

        rpc InputFile(  InputFileRequest) returns ( stream kernel.v0.Chunk);
        rpc InputFileS( InputFileRequest) returns ( stream CmdOutput);

        """
        if not self._local:
            self.upload(fname, progress_bar=progress_bar)
            filename = os.path.basename(fname)
        else:
            # file is local then
            if not os.path.dirname(fname):
                filename = os.path.join(os.getcwd(), fname)
            else:
                filename = fname

        # opt = ''
        # if mute:
            # opt = 'MUTE'
        request = pb_types.InputFileRequest(filename=filename)
                                            # opt=opt)
        metadata = [('time_step_stream', '200'), ('chunk_size', '512')]

        # if mute:
        #     cmd_output = self._stub.InputFile(request, metadata=metadata)
        #     chunks = [chunk for chunk in cmd_output]
        #     responses = [chunk.payload.decode('latin-1') for chunk in chunks]
        # else:

        strouts = self._stub.InputFileS(request, metadata=metadata)
        response = []
        responses = []
        for strout in strouts:
            cmdout = strout.cmdout
            for line in cmdout:
                response.append(line)
                if verbose:  # print out input as it is being run
                    print('\n'.join(response))
            responses.extend(response)

        response = '\n'.join(responses)
        return response

    def _get(self, cmd):
        """Sends gRPC get request

        WARNING: Not thread SAFE.

        """
        while self._get_lock:
            time.sleep(0.001)

        self._get_lock = True
        getresponse = self._stub.Get(pb_types.GetRequest(getcmd=cmd))
        self._get_lock = False

        if (getresponse.type == 1):
            return getresponse.dval
        elif (getresponse.type == 2):
            return getresponse.sval


    ###########################################################################

    def Param(self, pname):
        presponse = self._stub.GetParameter(pb_types.ParameterRequest(name=pname))
        return presponse.val

    def Var(self, num):
        presponse = self._stub.GetVariable(pb_types.VariableRequest(inum=num))
        return presponse.val

    def input_text(self, text, line_chunks=20, join=True):
        """Stream a chunk of text to MAPDl and process the commands.

        Stream the response back and deserialize the output.

        Parameters
        ----------
        fname : str
            MAPDL input file to stream to the MAPDL grpc server.

        line_chunks : int
            Number of lines to send at a time.

        Returns
        -------
        response : str
            Response from MAPDL.
        """
        chunks = chunk_lines(text, line_chunks)
        response = self._stub.InputFileLocal(chunks)

        # deserialize and return test response
        payloads = [chunk.payload for chunk in response]

        if join:
            return b''.join(payloads).decode('latin-1')
        return [payload.decode('latin-1') for payload in payloads]

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
        cmd = check_vget_input(entity, item, itnum)
        return self._vget(cmd)

    def _vget(self, cmd, dtype=None):
        """gRPC VGET request.

        Send a vget request, receive a bytes stream, and return it as
        a numpy array.

        WARNING: Not thread SAFE.

        Parameters
        ----------
        cmd : str
            VGET command formatted as: ``*VGET, {entity}, , {item}, {itnum}``

            Where:

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
                within the *VGET command reference in your ANSYS manual.

            itnum : str, int
                The number (or label) for the specified item (if
                any). Valid it1num values are as shown in the IT1NUM
                columns of the tables in the command reference section for
                the *VGET command in your ANSYS manual. Some Item1 labels
                do not require an IT1NUM value.

        dtype : np.dtype, optional
            ``numpy`` data type to parse to

        Returns
        -------
        values : np.ndarray
            Numpy 1D array containing the requested *VGET item and entity.
        """
        while self._vget_lock:
            time.sleep(0.001)
        self._vget_lock = True
        chunks = self._stub.VGet2(pb_types.GetRequest(getcmd=cmd))
        values = parse_chunks(chunks, dtype)
        self._vget_lock = False
        return values

    def upload(self, in_file_name, progress_bar=True):
        """Upload a file to the grpc instance"""
        chunks_generator = get_file_chunks(in_file_name, progress_bar=progress_bar)
        response = self._stub.UploadFile(chunks_generator)

        if not response.length:
            raise IOError('File failed to upload')

    def upload_raw(self, raw, save_as):
        chunks = chunk_raw(raw, save_as)
        response = self._stub.UploadFile(chunks)
        if response.length != len(raw):
            raise IOError('File failed to upload')

    def download(self, target_name, out_file_name=None, chunk_size=1024*64,
                 progress_bar=True):
        """Download a file from the grpc instance"""
        if out_file_name is None:
            out_file_name = target_name

        request = pb_types.DownloadFileRequest(name=target_name)
        metadata = [('time_step_stream', '200'), ('chunk_size', str(chunk_size))]
        chunks = self._stub.DownloadFile(request, metadata=metadata)
        save_chunks_to_file(chunks, out_file_name, progress_bar=progress_bar,
                            target_name=target_name)

    def download_as_raw(self, target_name):
        """Download a file from the grpc instance as a binary
        string"""
        request = pb_types.DownloadFileRequest(name=target_name)
        chunks = self._stub.DownloadFile(request)
        return b''.join([chunk.payload for chunk in chunks])

    def scalar_param(self, pname):
        """Return a scalar parameter as a float"""
        request = pb_types.ParameterRequest(name=pname, array=False)
        presponse = self._stub.GetParameter(request)
        return float(presponse.val[0])
 
    def data_info(self, pname):
        """Returns the data type of a parameter"""
        request = pb_types.ParameterRequest(name=pname)
        return self._stub.GetDataInfo(request)

    def vec_data(self, pname):
        """Downloads vector data from a parameter"""
        presponse = self.data_info(pname)
        type = ANSYS_VALUE_TYPE[presponse.stype]
        request = pb_types.ParameterRequest(name=pname)
        chunks = self._stub.GetVecData(request)
        values = parse_chunks(chunks, type)
        return values

    def set_vec(self, vname, nparray):
        """Set a vector within the MAPDL server"""
        chunks_generator = get_nparray_chunks(vname, nparray)
        self._stub.SetVecData(chunks_generator)

    def mat_data(self, pname):
        """Downloads matrix data from a parameter"""
        try:
            from scipy import sparse
        except ImportError:
            raise ImportError('Install ``scipy`` to use this feature')

        presponse = self.data_info(pname)
        stype = ANSYS_VALUE_TYPE[presponse.stype]
        mtype = presponse.objtype
        size1 = presponse.size1
        size2 = presponse.size1

        if mtype == 2:
            request = pb_types.ParameterRequest(name=pname)
            chunks = self._stub.GetMatData(request)
            values = parse_chunks(chunks, stype)
            return np.reshape(values, (size1, size2))
        elif mtype == 3:
            request = pb_types.ParameterRequest(name=pname + "::ROWS")
            chunks = self._stub.GetVecData(request)
            indptr = parse_chunks(chunks, np.int32)
            request = pb_types.ParameterRequest(name=pname + "::COLS")
            chunks = self._stub.GetVecData(request)
            indices = parse_chunks(chunks, np.int32)
            request = pb_types.ParameterRequest(name=pname + "::VALS")
            chunks = self._stub.GetVecData(request)
            vals = parse_chunks(chunks, np.float64)
            return sparse.csr_matrix((vals, indices, indptr), shape=(size1, size2))
