"""CORBA implementation of the MAPDL interface"""
import atexit
from threading import Thread
import time
import re
import os
import subprocess

from pyansys.mapdl import _Mapdl
from pyansys.misc import kill_process

try:
    from ansys_corba import CORBA
except:
    raise ImportError('Missing ansys_corba libaries.\n' +
                      'Only supported on Python3.5 - Python3.8 for '
                      'Linux and Windows\n')

INSTANCES = []

# Windows has issues when closing
@atexit.register
def cleanup():
    if os.name == 'nt':
        for instance in INSTANCES:
            instance.kill()


def threaded(fn):
    """ calls a function using a thread """
    def wrapper(*args, **kwargs):
        thread = Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper


def tail(filename, nlines):
    """ Read the last nlines of a text file """
    with open(filename) as qfile:
        qfile.seek(0, os.SEEK_END)
        endf = position = qfile.tell()
        linecnt = 0
        while position >= 0:
            qfile.seek(position)
            next_char = qfile.read(1)
            if next_char == "\n" and position != endf-1:
                linecnt += 1

            if linecnt == nlines:
                break
            position -= 1

        if position < 0:
            qfile.seek(0)

        return qfile.read()


class MapdlCorba(_Mapdl):
    """CORBA implementation of the MAPDL interface"""

    def __init__(self, exec_file, run_location,
                 jobname='file', nproc=2, override=False,
                 loglevel='INFO', additional_switches='',
                 start_timeout=120, interactive_plotting=False,
                 check_version=True,
                 prefer_pexpect=True, log_apdl='w',
                 log_broadcast=False):
        self._broadcast_logger = None
        self._server = None
        self._log_broadcast = log_broadcast

        # CORBA/AAS was introduced in v17
        version = int(re.findall(r'\d\d\d', exec_file)[0])
        if version < 170:
            raise RuntimeError('MAPDL AAS CORBA server requires '
                               'v17.0 or greater.')

        # this will launch MAPDL
        super().__init__(exec_file, run_location, jobname, nproc,
                         override, loglevel, additional_switches,
                         start_timeout, interactive_plotting,
                         log_apdl)
        INSTANCES.append(self)

    @property
    def _broadcast_file(self):
        return os.path.join(self.path, 'mapdl_broadcasts.txt')

    def _launch(self):
        """Open a connection to ANSYS via a CORBA interface"""
        # Using stored parameters so launch command can be run from a
        # cached state (when launching the GUI)
        self._log.info('Connecting to ANSYS via CORBA')

        # create a dummy input file for getting NON-INTERACTIVE without
        # running /BATCH
        tmp_inp = os.path.join(self.path, 'tmp.inp')
        with open(tmp_inp, 'w') as f:
            f.write('FINISH')

        # command must include "aas" flag to start MAPDL server
        command = '"%s" -aas -j %s -b -i tmp.inp -o out.txt -np %d %s' % (self._exec_file, self._jobname, self._nproc, self._additional_switches)

        # remove the broadcast file if it exists as the key will be
        # output here when ansys server is available
        if os.path.isfile(self._broadcast_file):
            os.remove(self._broadcast_file)

        # add run location to command
        self._log.debug('Spawning shell process with: "%s"', command)
        self._log.debug('At "%s"', self.path)

        # after v19, this is the only way this will work...
        if os.name == 'nt':
            command = 'START /B "MAPDL" %s' % command

        # set stdout
        if self._log.level < 20:  # < INFO            
            self._process = subprocess.Popen(command, shell=True, 
                                             cwd=self.path)
        else:
            self._process = subprocess.Popen(command, shell=True, 
                                             cwd=self.path,
                                             stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE)

        # listen for broadcast file
        self._log.debug('Waiting for valid key in %s', self._broadcast_file)
        telapsed = 0
        tstart = time.time()
        while telapsed < self._start_timeout:
            try:
                if os.path.isfile(self._broadcast_file):
                    with open(self._broadcast_file, 'r') as f:
                        text = f.read()
                        if 'visited:collaborativecosolverunitior' in text:
                            self._log.debug('Initialized ANSYS')
                            break
                time.sleep(0.1)
                telapsed = time.time() - tstart

            except KeyboardInterrupt:
                raise KeyboardInterrupt

        # exit if timed out
        if telapsed > self._start_timeout:
            err_msg = 'Unable to start ANSYS within %.1f seconds' % self._start_timeout
            self._log.error(err_msg)
            raise TimeoutError(err_msg)

        # open server
        keyfile = os.path.join(self.path, 'aaS_MapdlId.txt')
        with open(keyfile) as f:
            key = f.read()

        orb = CORBA.ORB_init()
        self._server = orb.string_to_object(key)

        # set to non-interactive
        # if os.name != 'nt':
            # text = self._server.executeCommandToString('/BATCH')

        try:
            self._server.getComponentName()
        except:
            raise RuntimeError('Unable to connect to APDL server')

        self._log.debug('Connected to ANSYS using CORBA interface with key %s', key)

        # separate logger for broadcast file
        if self._log_broadcast:
            self._broadcast_logger = self._start_broadcast_logger()

    @threaded
    def _start_broadcast_logger(self, update_rate=1.0):
        """ separate logger using broadcast_file """
        # listen to broadcast file
        loadstep = 0
        overall_progress = 0
        try:
            old_tail = ''
            old_size = 0
            while self.is_alive:
                new_size = os.path.getsize(self._broadcast_file)
                if new_size != old_size:
                    old_size = new_size
                    new_tail = tail(self._broadcast_file, 4)
                    if new_tail != old_tail:
                        lines = new_tail.split('>>')
                        for line in lines:
                            line = line.strip().replace('<<broadcast::', '')
                            if "current-load-step" in line:
                                n = int(re.search(r'\d+', line).group())
                                if n > loadstep:
                                    loadstep = n
                                    overall_progress = 0
                                    self._log.info(line)
                            elif "overall-progress" in line:
                                n = int(re.search(r'\d+', line).group())
                                if n > overall_progress:
                                    overall_progress = n
                                    self._log.info(line)
                        old_tail = new_tail
                time.sleep(update_rate)
        except Exception as e:
            pass

    def exit(self, close_log=True, timeout=3):
        """Exit MAPDL process"""
        self._log.debug('Exiting ANSYS')
        if self._server is not None:
            self._server.terminate()
            self._server = None

        if close_log:
            self._close_apdl_log()

        # wait for lockfile to be removed
        if timeout:
            tstart = time.time()
            while os.path.isfile(self._lockfile):
                time.sleep(0.05)
                telap = tstart - time.time()
                if telap > timeout:
                    return 1

    def kill(self):
        """Forces ANSYS process to end and removes lock file"""
        try:
            self.exit()
        except:
            pass

        if self._process is not None and os.name == 'linux':
            kill_process(self._process.pid)

        try:
            self._close_apdl_log()
        except:
            pass

        try:
            self._remove_lockfile()
        except:
            pass

    def _run(self, command):
        """Sends a command to the mapdl server via the CORBA interface"""
        if self._server is None:
            raise RuntimeError('ANSYS exited')

        # cleanup command
        command = command.strip()
        if not command:
            raise Exception('Empty command')

        if command[:4].lower() == 'cdre':
            with self.non_interactive:
                return self.run(command)

        if command[:4].lower() == '/com':
            split_command = command.split(',')
            if len(split_command) < 2:
                return ''
            elif not split_command[1]:
                return ''
            elif split_command[1]:
                if not split_command[1].strip():
                    return ''

        # /OUTPUT not redirected properly in corba
        if command[:4].lower() == '/out':
            items = command.split(',')
            if len(items) < 2:  # empty comment
                return ''
            elif not items[1]:  # empty comment
                return ''
            elif items[1]:
                if not items[1].strip():    # empty comment
                    return ''

            items = command.split(',')
            if len(items) > 1:  # redirect to file
                if len(items) > 2:
                    if items[2].strip():
                        filename = '.'.join(items[1:3]).strip()
                    else:
                        filename = '.'.join(items[1:2]).strip()
                else:
                    filename = items[1]

                if filename:
                    if os.path.basename(filename) == filename:
                        filename = os.path.join(self.path, filename)
                    self._output = filename
                    if len(items) == 5:
                        if items[4].lower().strip() == 'append':
                            self._outfile = open(filename, 'a')
                    else:
                        self._outfile = open(filename, 'w')
            else:
                self._output = ''
                if self._outfile:
                    self._outfile.close()
                self._outfile = None
            return ''

        # include error checking
        text = ''
        additional_text = ''

        self._log.debug('Running command %s' % command)
        text = self._server.executeCommandToString(command)

        # print supressed output
        additional_text = self._server.executeCommandToString('/GO')

        if 'is not a recognized' in text:
            if not self.allow_ignore:
                text = text.replace('This command will be ignored.', '')
                text += '\n\nIgnore these messages by setting allow_ignore=True'
                raise Exception(text)

        if text:
            text = text.replace('\\n', '\n')
            if '*** ERROR ***' in text:
                self._log.error(text)
                raise Exception(text)

        if additional_text:
            additional_text = additional_text.replace('\\n', '\n')
            if '*** ERROR ***' in additional_text:
                self._log.error(additional_text)
                raise Exception(additional_text)

        if self._interactive_plotting:
            self._display_plot('%s\n%s' % (text, additional_text))

        # return text, additional_text
        if text == additional_text:
            additional_text = ''
        return '%s\n%s' % (text, additional_text)
