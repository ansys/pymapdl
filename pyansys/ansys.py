#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module to control interaction with an ANSYS shell instance.
Built using ansys documentation from
https://www.sharcnet.ca/Software/Ansys/

This module makes no claim to own any rights to ANSYS.  It's merely an interface to
software owned by ANSYS.

"""
import re
import os
import tempfile
import appdirs
import warnings
import logging
import time
import subprocess
from threading import Thread
import weakref

import pyansys
import pexpect
import numpy as np
import psutil
from ansys_corba import CORBA
from pyansys.ansys_functions import _InternalANSYS
from pyansys.convert import IsFloat

try:
    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg
    matplotlib_loaded = True
except:
    matplotlib_loaded = False


def FindANSYS():
    """ Searches for ansys path within enviornmental variables """
    versions = []
    paths = []
    for var in os.environ:
        if 'ANSYS' in var:
            if '_DIR' in var:
                try:
                    versions.append(int(var[5:8]))
                except:
                    continue
                path = os.environ[var]
                if os.path.isdir(path):
                    paths.append(path)

    if not paths:
        return None, None

    maxver_ind = np.argmax(versions)
    maxver = versions[maxver_ind]
    ansys_path = paths[maxver_ind]
    ansys_sysdir_var = 'ANSYS_SYSDIR'
    if ansys_sysdir_var in os.environ:
        sysdir = os.environ[ansys_sysdir_var]
    else:
        sysdir = ''

    ansys_bin_path = os.path.join(ansys_path, 'bin', sysdir)
    if 'win' in sysdir:
        ansys_bin = 'ansys%d.exe' % maxver
    else:
        ansys_bin = 'ansys%d' % maxver

    version = float(maxver)/10.0
    return os.path.join(ansys_bin_path, ansys_bin), version


def Tail(filename, nlines):
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


def KillProcess(proc_pid):
    """ kills a process with extreme prejudice """
    process = psutil.Process(proc_pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()


# settings directory
settings_dir = appdirs.user_data_dir('pyansys')
if not os.path.isdir(settings_dir):
    try:
        os.makedirs(settings_dir)
    except:
        warnings.warn('Unable to create settings directory.\n' +
                      'Will be unable to cache ANSYS executable location')

config_file = os.path.join(settings_dir, 'config.txt')

# specific to pexpect process
###############################################################################
ready_items = [b'BEGIN:',
               b'PREP7:',
               b'SOLU_LS[0-9]+:',
               b'POST1:',
               b'POST26:',
               b'RUNSTAT:',
               b'AUX2:',
               b'AUX3:',
               b'AUX12:',
               b'AUX15:',
               # continue
               b'YES,NO OR CONTINUOUS\)\=',
               b'executed\?',
               # errors
               b'SHOULD INPUT PROCESSING BE SUSPENDED\?',
               # prompts
               b'ENTER FORMAT for',
]

continue_idx = ready_items.index(b'YES,NO OR CONTINUOUS\)\=')
warning_idx = ready_items.index(b'executed\?')
error_idx = ready_items.index(b'SHOULD INPUT PROCESSING BE SUSPENDED\?')
prompt_idx = ready_items.index(b'ENTER FORMAT for')

nitems = len(ready_items)
expect_list = []
for item in ready_items:
    expect_list.append(re.compile(item))
ignored = re.compile('[\s\S]+'.join(['WARNING', 'command', 'ignored']))
###############################################################################

# test for png file
png_test = re.compile('WRITTEN TO FILE file\d\d\d.png')

INVAL_COMMANDS = {'*vwr':  'Use "with ansys.non_interactive:\n\t*ansys.Run("VWRITE(..."',
                  '*cfo': '',
                  '*CRE': 'Create a function within python or run as non_interactive',
                  '*END': 'Create a function within python or run as non_interactive',
                  '*IF': 'Use a python if or run as non_interactive'}


def CheckValidANSYS():
    """ Checks if a valid version of ANSYS is installed and preconfigured """
    ansys_bin = GetANSYSPath(allow_input=False)
    if ansys_bin is not None:
        version = int(re.findall('\d\d\d', ansys_bin)[0])
        return not(version < 170 and os.name != 'posix')

    return False


def SetupLogger(loglevel='INFO'):
    """ Setup logger """

    # return existing log if this function has already been called
    if hasattr(SetupLogger, 'log'):
        SetupLogger.log.setLevel(loglevel)
        ch = SetupLogger.log.handlers[0]
        ch.setLevel(loglevel)
        return SetupLogger.log

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
    SetupLogger.log = log

    return log


def GetANSYSPath(allow_input=True):
    """ Acquires ANSYS Path from a cached file or user input """
    exe_loc = None
    if os.path.isfile(config_file):
        with open(config_file) as f:
            exe_loc = f.read()
        # verify
        if not os.path.isfile(exe_loc) and allow_input:
            print('Cached ANSYS executable %s not found' % exe_loc)
            exe_loc = SaveANSYSPath()
    elif allow_input:  # create configuration file
        exe_loc = SaveANSYSPath()

    return exe_loc


def ChangeDefaultANSYSPath(exe_loc):
    """
    Change your default ansys path

    Parameters
    ----------
    exe_loc : str
        Ansys executable.  Must be a full path.

    """
    if os.path.isfile(exe_loc):
        with open(config_file, 'w') as f:
            f.write(exe_loc)
    else:
        raise Exception('File %s is invalid or does not exist' % exe_loc)


def SaveANSYSPath(exe_loc=''):
    """ Find ANSYS path or query user """
    print('Cached ANSYS executable %s not found' % exe_loc)
    exe_loc, ver = FindANSYS()
    if os.path.isfile(exe_loc):
        print('Found ANSYS at %s' % exe_loc)
        resp = input('Use this location?  [Y/n]')
        if resp != 'n':
            return exe_loc

    if exe_loc is not None:
        if os.path.isfile(exe_loc):
            return exe_loc

    # otherwise, query user for the location
    with open(config_file, 'w') as f:
        try:
            exe_loc = raw_input('Enter location of ANSYS executable: ')
        except NameError:
            exe_loc = input('Enter location of ANSYS executable: ')
        if not os.path.isfile(exe_loc):
            raise Exception('ANSYS executable not found at this location:\n%s' % exe_loc)

        f.write(exe_loc)

    return exe_loc


class ANSYS(_InternalANSYS):
    """
    This class opens ANSYS in the background and allows commands to be
    passed to a persistent session.

    Parameters
    ----------
    exec_file : str, optional
        The location of the ANSYS executable.  Will use the cached location when
        left at the default None.

    run_location : str, optional
        ANSYS working directory.  Defaults to a temporary working directory.

    jobname : str, optional
        ANSYS jobname.  Defaults to 'file'.

    nproc : int, optional
        Number of processors.  Defaults to 2.

    override : bool, optional
        Attempts to delete the *.lock file at the run_location.  Useful when a prior
        ANSYS session has exited prematurely and the lock file has not been deleted.

    wait : bool, optional
        When True, waits until ANSYS has been initialized before initializing the
        python ansys object.  Set this to False for debugging.

    loglevel : str, optional
        Sets which messages are printed to the console.  Default 'INFO' prints out
        all ANSYS messages, 'WARNING` prints only messages containing ANSYS warnings,
        and 'ERROR' prints only error messages.

    additional_switches : str, optional
        Additional switches for ANSYS, for example aa_r, and academic research license,
        would be added with:

        - additional_switches="-aa_r"

        Avoid adding switches like -i -o or -b as these are already included to
        start up the ANSYS MAPDL server.

    start_timeout : float, optional
        Time to wait before raising error that ANSYS is unable to start.

    interactive_plotting : bool, optional
        Enables interactive plotting using matplotlib.  Install matplotlib first.
        Default False.

    log_broadcast : bool, optional
        Additional logging for ansys solution progress.  Default True and visible
        at log level 'INFO'.

    check_version : bool, optional
        Check version of binary file and raise exception when invalid.

    prefer_pexpect : bool, optional
        When enabled, will avoid using ansys APDL in CORBA server mode
        and will spawn a process and control it using pexpect.  Default False.

    log_apdl : bool, optional
        Opens an APDL log file named "log.inp" in the current ANSYS working
        directory.

    Examples
    --------
    >>> import pyansys
    >>> ansys = pyansys.ANSYS()

    """

    def __init__(self, exec_file=None, run_location=None, jobname='file', nproc=2,
                 override=False, loglevel='INFO', additional_switches='',
                 start_timeout=120, interactive_plotting=False, log_broadcast=False, #True,
                 check_version=True, prefer_pexpect=False, log_apdl=True):
        """ Initialize connection with ANSYS program """
        self.log = SetupLogger(loglevel.upper())
        self.jobname = jobname
        self.non_interactive = self._non_interactive(self)
        self.redirected_commands = {'*LIS': self._List}

        # default settings
        self.allow_ignore = False
        self.process = None
        self.lockfile = ''
        self._interactive_plotting = False
        self.using_corba = None
        self.auto_continue = True
        self.apdl_log = None
        self._store_commands = False
        self._stored_commands = []
        self.response = None
        self._output = ''
        self._outfile = None

        if exec_file is None:
            # Load cached path
            exec_file = GetANSYSPath()
            if exec_file is None:
                raise Exception('Invalid or path or cannot load cached ansys path' +
                                'Enter one manually using pyansys.ANSYS(exec_file=...)')

        else:  # verify ansys exists at this location
            if not os.path.isfile(exec_file):
                raise Exception('Invalid ANSYS executable at %s' % exec_file +
                                'Enter one manually using pyansys.ANSYS(exec_file="")')
        self.exec_file = exec_file

        # check ansys version
        if check_version:
            version = int(re.findall('\d\d\d', self.exec_file)[0])
            if version < 170 and os.name != 'posix':
                raise Exception('ANSYS MAPDL server requires version 17.0 or greater ' +
                                'for windows')

        # create temporary directory
        self.path = run_location
        if self.path is None:
            temp_dir = tempfile.gettempdir()
            self.path = os.path.join(temp_dir, 'ansys')
            if not os.path.isdir(self.path):
                try:
                    os.mkdir(self.path)
                except:
                    raise Exception('Unable to create temporary working '
                                    'directory %s\n' % self.path +
                                    'Please specify run_location')
        else:
            if not os.path.isdir(self.path):
                raise Exception('%s is not a valid folder' % self.path)

        # Check for lock file
        self.lockfile = os.path.join(self.path, self.jobname + '.lock')
        if os.path.isfile(self.lockfile):
            if not override:
                raise Exception('Lock file exists for jobname %s \n' % self.jobname +
                                ' at %s\n' % self.lockfile +
                                'Set override=True to delete lock and start ANSYS')
            else:
                os.remove(self.lockfile)

        # key will be output here when ansys server is available
        self.broadcast_file = os.path.join(self.path, 'mapdl_broadcasts.txt')
        if os.path.isfile(self.broadcast_file):
            os.remove(self.broadcast_file)

        # create a dummy input file
        tmp_inp = os.path.join(self.path, 'tmp.inp')
        with open(tmp_inp, 'w') as f:
            f.write('FINISH')

        # open a connection to ANSYS
        if (version < 170 and os.name == 'posix') or prefer_pexpect:
            self.OpenProcess(nproc, start_timeout)
        else:  # use corba
            self.OpenCorba(nproc, start_timeout)

            # separate logger for broadcast file
            self.log_broadcast = log_broadcast
            if self.log_broadcast:
                self.broadcast_logger = Thread(target=ANSYS.StartBroadcastLogger,
                                               args=(weakref.proxy(self),))
                self.broadcast_logger.start()

        # setup plotting for PNG
        if interactive_plotting:
            self.EnableInteractivePlotting()

        if log_apdl:
            if isinstance(log_apdl, str):
                filename = log_apdl
            else:
                filename = os.path.join(self.path, 'log.inp')
            self.OpenAPDLLog(filename)

    def OpenAPDLLog(self, filename):
        """
        Starts writing all APDL commands to an ANSYS input

        Parameters
        ----------
        filename : str
            Filename of the log

        """
        if self.apdl_log is not None:
            raise Exception('APDL command logging already enabled.\n')

        self.log.debug('Opening ANSYS log file at %s' % filename)
        self.apdl_log = open(filename, 'w', 1)  # line buffered
        self.apdl_log.write('! APDL script generated using pyansys %s\n' %
                            pyansys.__version__)

    def CloseAPDLLog(self):
        """ Closes APDL log """
        if self.apdl_log is not None:
            self.apdl_log.close()
        self.apdl_log = None

    def OpenProcess(self, nproc, timeout):
        """ Opens an ANSYS process using pexpect """
        command = '%s -j %s -np %d' % (self.exec_file, self.jobname, nproc)
        self.log.debug('Spawning shell process using pexpect')
        self.log.debug('Command: "%s"' % command)
        self.log.debug('At "%s"' % self.path)
        self.process = pexpect.spawn(command, cwd=self.path)
        self.process.delaybeforesend = None
        self.log.debug('Waiting for ansys to start...')
        self.process.expect('CONTINUE')
        self.process.sendline('')  # enter to continue
        self.process.expect('BEGIN:', timeout=timeout)
        self.log.debug('ANSYS Initialized')
        self.log.debug(self.process.before.decode('utf-8'))
        self.using_corba = False

    def EnableInteractivePlotting(self):
        """ Enables interactive plotting.  Requires matplotlib """
        if matplotlib_loaded:
            self.Show('PNG')
            self._interactive_plotting = True
        else:
            raise Exception('Install matplotlib to use enable interactive plotting\n' +
                            'or turn interactive plotting off with:\n' +
                            'interactive_plotting=False')

    def SetLogLevel(self, loglevel):
        """ Sets log level """
        SetupLogger(loglevel=loglevel.upper())

    def __enter__(self):
        return self

    @property
    def is_alive(self):
        if self.process is None:
            return False
        else:
            if self.using_corba:
                return self.process.poll() is None
            else:
                return self.process.isalive()

    def StartBroadcastLogger(self, update_rate=1.0):
        """ separate logger using broadcast_file """

        # listen to broadcast file
        try:
            old_tail = ''
            old_size = 0
            while self.is_alive:
                new_size = os.path.getsize(self.broadcast_file)
                if new_size != old_size:
                    old_size = new_size
                    new_tail = Tail(self.broadcast_file, 4)
                    if new_tail != old_tail:
                        lines = new_tail.split('>>')
                        for line in lines:
                            line = line.strip().replace('<<broadcast::', '')
                            if line:
                                self.log.info(line)
                        old_tail = new_tail
                time.sleep(update_rate)
        except Exception as e:
            pass

    def Run(self, command, write_to_log=True):
        """
        Runs APDL command(s)

        Parameters
        ----------
        command : str
            ANSYS APDL command.  
            
            These commands will be written to a temporary input file and then run
            using /INPUT.

        write_to_log : bool, optional
            Overrides APDL log writing.  Default True.  When set to False, will
            not write command to log even through APDL command logging is enabled.

        Returns
        -------
        command_output : str
            Command output from ANSYS.

        Notes
        -----
        When two or more commands need to be run non-interactively
        (i.e. *VWRITE) then use
        
        >>> with ansys.non_interactive:
        >>>     ansys.Run("*VWRITE,LABEL(1),VALUE(1,1),VALUE(1,2),VALUE(1,3)")
        >>>     ansys.Run("(1X,A8,'   ',F10.1,'  ',F10.1,'   ',1F5.3)")
        """
        if self._store_commands:
            self._stored_commands.append(command)
            return
        elif command[:3].upper() in INVAL_COMMANDS:
            import pdb; pdb.set_trace()
            exception = Exception('Invalid pyansys command "%s"\n\n%s' %
                                  (command, INVAL_COMMANDS[command[:3]]))
            raise exception
        elif command[:4].upper() in INVAL_COMMANDS:
            exception = Exception('Invalid pyansys command "%s"\n\n%s' %
                                  (command, INVAL_COMMANDS[command[:4]]))
            raise exception
        elif write_to_log and self.apdl_log is not None:
            self.apdl_log.write('%s\n' % command)

        if command[:4] in self.redirected_commands:
            function = self.redirected_commands[command[:4]]
            return function(command)

        text = self._Run(command)
        if text:
            self.response = text.strip()
        else:
            self.response = ''

        if self.response:
            self.log.info(self.response)
            if self._outfile:
                self._outfile.write('%s\n' % self.response)
        return self.response

    def _Run(self, command):
        if self.using_corba:
            # check if it's a single non-interactive command
            if command[:4].lower() == 'cdre':
                with self.non_interactive:
                    return self.Run(command)
            else:
                return self.RunCorbaCommand(command)
        else:
            return self.RunProcessCommand(command)

    def _List(self, command):
        """ Replaces *LIST command """
        items = command.split(',')
        filename = os.path.join(self.path, '.'.join(items[1:]))
        if os.path.isfile(filename):
            self.response = open(filename).read()
            self.log.info(self.response)
        else:
            raise Exception('Cannot run:\n%s\n' % command + 'File does not exist')

    def RunProcessCommand(self, command, return_response=True):
        """ Sends command and returns ANSYS's response """
        if not self.process.isalive():
            raise Exception('ANSYS process closed')

        if command[:4].lower() == '/out':
            items = command.split(',')
            if len(items) > 1:
                self._output = '.'.join(items[1:])
            else:
                self._output = ''

        # send the command
        self.log.debug('Sending command %s' % command)
        self.process.sendline(command)

        # do not expect
        if '/MENU' in command:
            self.log.info('Enabling GUI')
            self.process.sendline(command)
            return

        while True:
            i = self.process.expect_list(expect_list, timeout=None)
            response = self.process.before.decode('utf-8')
            if i >= continue_idx and i < warning_idx:  # continue
                self.log.debug('Continue: Response index %i.  Matched %s'
                               % (i, ready_items[i].decode('utf-8')))
                self.log.info(response + ready_items[i].decode('utf-8'))
                if self.auto_continue:
                    user_input = 'y'
                else:
                    user_input = input('Response: ')
                self.process.sendline(user_input)

            elif i >= warning_idx and i < error_idx:  # warning
                self.log.debug('Prompt: Response index %i.  Matched %s'
                               % (i, ready_items[i].decode('utf-8')))
                self.log.warning(response + ready_items[i].decode('utf-8'))
                if self.auto_continue:
                    user_input = 'y'
                else:
                    user_input = input('Response: ')
                self.process.sendline(user_input)

            elif i >= error_idx and i < prompt_idx:  # error
                self.log.debug('Error index %i.  Matched %s'
                               % (i, ready_items[i].decode('utf-8')))
                self.log.error(response)
                response += ready_items[i].decode('utf-8')
                raise Exception(response)

            elif i >= prompt_idx:  # prompt
                self.log.debug('Prompt index %i.  Matched %s'
                               % (i, ready_items[i].decode('utf-8')))
                self.log.info(response + ready_items[i].decode('utf-8'))
                # user_input = input('Response: ')
                # self.process.sendline(user_input)
                raise Exception('User input expected.  Try using non_interactive')

            else:  # continue item
                self.log.debug('continue index %i.  Matched %s'
                               % (i, ready_items[i].decode('utf-8')))
                break

            # handle response
            if '*** ERROR ***' in response:  # flag error
                self.log.error(response)
                if not continue_on_error:
                    raise Exception(response)
            elif ignored.search(response):  # flag ignored command
                if not self.allow_ignore:
                    self.log.error(response)
                    raise Exception(response)
                else:
                    self.log.warning(response)
            else:
                self.log.info(response)

        return self.process.before.decode('utf-8')

    def RunCorbaCommand(self, command):
        """
        Sends a command to the mapdl server

        """
        if not self.is_alive:
            raise Exception('ANSYS process has been terminated')

        # cleanup command
        command = command.strip()
        if not command:
            raise Exception('Empty command')

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

        self.log.debug('Running command %s' % command)
        text = self.mapdl.executeCommandToString(command)

        # print supressed output
        additional_text = self.mapdl.executeCommandToString('/GO')

        if 'is not a recognized' in text:
            if not self.allow_ignore:
                text = text.replace('This command will be ignored.', '')
                text += '\n\nIgnore these messages by setting allow_ignore=True'
                raise Exception(text)

        if text:
            text = text.replace('\\n', '\n')
            if '*** ERROR ***' in text:
                self.log.error(text)
                raise Exception(text)

        if additional_text:
            additional_text = additional_text.replace('\\n', '\n')
            if '*** ERROR ***' in additional_text:
                self.log.error(additional_text)
                raise Exception(additional_text)

        if self._interactive_plotting:
            self.DisplayPlot('%s\n%s' % (text, additional_text))

        # return text, additional_text
        if text == additional_text:
            additional_text = ''
        return '%s\n%s' % (text, additional_text)

    def LoadParameters(self):
        # load ansys parameters to python
        self.Parsav('all')  # saves to file.parm by default
        filename = os.path.join(self.path, 'file.parm')
        self.parameters, self.arrays = LoadParameters(filename)

    def AddFileHandler(self, filepath, append):
        """ Adds a file handler to the log """
        # import pdb; pdb.set_trace()
        if append:
            mode = 'a'
        else:
            mode = 'w'

        self.fileHandler = logging.FileHandler(filepath)
        formatstr = '%(asctime)s [%(levelname)s] %(name)s: %(message)s'

        # self.fileHandler.setFormatter(logging.Formatter(formatstr))
        # self.log.addHandler(self.fileHandler)

        self.fileHandler = logging.FileHandler(filepath, mode=mode)
        self.fileHandler.setFormatter(logging.Formatter(formatstr))
        self.fileHandler.setLevel(logging.DEBUG)
        self.log.addHandler(self.fileHandler)
        self.log.info('Added file handler at %s' % filepath)

    def RemoveFileHandler(self):
        self.log.removeHandler(self.fileHandler)
        self.log.info('Removed file handler')

    def DisplayPlot(self, text):
        """ Check if plot exists based on command output """
        png_found = png_test.findall(text)
        if png_found:
            # flush graphics writer
            self.Show('CLOSE')
            self.Show('PNG')
            filename = png_found[0][-11:]
            fullfile = os.path.join(self.path, filename)
            if os.path.isfile(fullfile):
                img = mpimg.imread(fullfile)
                imgplot = plt.imshow(img)
                plt.axis('off')
                plt.show()  # consider in-line plotting
            else:
                log.error('Unable to find screenshot at %s' % fullfile)

    def __del__(self):
        # clean up when complete
        self.Kill()
        self.CloseAPDLLog()

    def __exit__(self, exc_type, exc_val, exc_tb):
        # clean up when complete
        self.Exit()

    def Exit(self):
        """
        Exit ANSYS process without attempting to kill the process.
        """
        self.log.debug('Terminating ANSYS')
        try:
            if self.using_corba:
                self.mapdl.terminate()
            else:
                self.process.sendline('FINISH')
                self.process.sendline('EXIT')

        except Exception as e:
            if 'WaitingForReply' not in str(e):
                raise Exception(e)

        self.log.info('ANSYS exited')
        self.apdl_log.close()

    def Kill(self):
        """ Forces ANSYS process to end and removes lock file """
        if self.is_alive:
            try:
                self.Exit()
            except:
                KillProcess(self.process.pid)
                self.log.debug('Killed process %d' % self.process.pid)

        if os.path.isfile(self.lockfile):
            try:
                os.remove(self.lockfile)
            except:
                self.log.warning('Unable to remove lock file %s ' % self.lockfile)

    @property
    def results(self):
        """ Returns a binary interface to the result file """
        warnings.warn('Depreciated.  Use "result" instead')
        return self.result

    @property
    def result(self):
        """ Returns a binary interface to the result file """
        resultfile = os.path.join(self.path, '%s.rst' % self.jobname)
        if not os.path.isfile(resultfile):
            raise Exception('No results found at %s' % resultfile)
        return pyansys.ResultReader(resultfile)

    def __call__(self, command, **kwargs):
        return self.Run(command, **kwargs)

    def OpenCorba(self, nproc, timeout):
        """
        Open a connection to ANSYS via a CORBA interface
        """
        self.log.info('Connecting to ANSYS via CORBA')

        # command must include "aas" flag to start MAPDL server
        command = '"%s" -j %s -aas -i tmp.inp -o out.txt -b -np %d' % (self.exec_file,
                                                                       self.jobname, nproc)       

        # add run location to command
        self.log.debug('Spawning shell process with: "%s"' % command)
        self.log.debug('At "%s"' % self.path)
        old_path = os.getcwd()
        os.chdir(self.path)
        self.process = subprocess.Popen(command,
                                        shell=True,
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        os.chdir(old_path)

        # listen for broadcast file
        self.log.debug('Waiting for valid key in %s' % self.broadcast_file)
        telapsed = 0
        tstart = time.time()
        while telapsed < timeout:
            try:
                if os.path.isfile(self.broadcast_file):
                    with open(self.broadcast_file, 'r') as f:
                        text = f.read()
                        if 'visited:collaborativecosolverunitior' in text:
                            self.log.debug('Initialized ANSYS')
                            break
                time.sleep(0.1)
                telapsed = time.time() - tstart

            except KeyboardInterrupt:
                raise KeyboardInterrupt

        # exit if timed out
        if telapsed > timeout:
            err_msg = 'Unable to start ANSYS within %.1f seconds' % timeout
            self.log.error(err_msg)
            raise TimeoutError(err_msg)

        # open server
        keyfile = os.path.join(self.path, 'aaS_MapdlId.txt')
        with open(keyfile) as f:
            key = f.read()

        orb = CORBA.ORB_init()
        self.mapdl = orb.string_to_object(key)

        # quick test
        try:
            self.mapdl.getComponentName()
        except:
            raise Exception('Unable to connect to APDL server')

        self.using_corba = True
        self.log.debug('Connected to ANSYS using CORBA interface')
        self.log.debug('Key %s' % key)

    class _non_interactive:
        """ 
        Allows user to enter commands that need to run non-interactively

        Examples
        --------
        To use an non-interactive command like *VWRITE, use:

        with ansys.non_interactive:
            ansys.Run("*VWRITE,LABEL(1),VALUE(1,1),VALUE(1,2),VALUE(1,3)")
            ansys.Run("(1X,A8,'   ',F10.1,'  ',F10.1,'   ',1F5.3)")

        """
        def __init__(self, parent):
            self.parent = parent
        def __enter__(self):
            self.parent.log.debug('entering non-interactive mode')
            self.parent._store_commands = True
        def __exit__(self, type, value, traceback):
            self.parent.log.debug('entering non-interactive mode')
            self.parent._FlushStored()

    def _FlushStored(self):
        """
        Writes stored commands to an input file and runs the input file.
        Used with non_interactive.
        """
        self.log.debug('Flushing stored commands')
        temp_out = os.path.join(self.path, 'tmp.out')
        self._stored_commands.insert(0, '/OUTPUT, %s' % temp_out)
        self._stored_commands.append('/OUTPUT')
        commands = '\n'.join(self._stored_commands)
        self.apdl_log.write(commands + '\n')

        # write to an input file
        base_name = 'tmp.inp'
        filename = os.path.join(self.path, 'tmp.inp')
        self.log.debug('Writing the following commands to a temporary ' +
                       'apdl input file:\n%s' % commands)
        with open(filename, 'w') as f:
            f.writelines(commands)

        # import pdb; pdb.set_trace()
        self._store_commands = False
        self._stored_commands = []
        self.Run('/INPUT, %s' % filename, write_to_log=False)
        self.response = '\n' + open(temp_out).read()

        # clean up output file
        self.Run('/OUTPUT, %s, , , APPEND' % self._output)
        for line in open(temp_out).readlines():
            self.Run('/COM,%s\n' % line[:74])

        self.log.info(self.response)


def LoadParameters(filename):
    """ load parameters """
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
                    arrays[append_varname] = np.genfromtxt(values).reshape(shp, order='F')
                else:
                    append_text.append(line.replace('\n', '').replace('\r', ''))

            elif '*DIM' in line:
                # *DIM, Par, Type, IMAX, JMAX, KMAX, Var1, Var2, Var3, CSYSID
                st = line.find(',') + 1
                varname = line[st:st+8].strip()
                split_line = line.split(',')
                arr_type = split_line[2]
                imax = int(split_line[3])
                jmax = int(split_line[4])
                kmax = int(split_line[5])

                if arr_type == 'CHAR':
                    arrays[varname] = np.empty((imax, jmax, kmax), dtype='<U8', order='F')
                if arr_type == 'ARRAY':
                    arrays[varname] = np.empty((imax, jmax, kmax), np.double, order='F')
                else:
                    arrays[varname] = np.empty((imax, jmax, kmax), np.object, order='F')

            elif '*SET' in line:
                st = line.find(',') + 1
                varname = line[st:st+8].strip()
                if varname in arrays:
                    st = line.find('(') + 1
                    en = line.find(')')
                    ind = line[st:en].split(',')
                    i = int(ind[0]) - 1
                    j = int(ind[1]) - 1
                    k = int(ind[2]) - 1
                    value = line[en+2:].strip().replace("'", '')
                    arrays[varname][i, j, k] = value
                else:
                    # break
                    st = line.find(',', st)
                    value = line[st + 1:].strip()
                    if IsFloat(value):
                        parameters[varname] = float(value)
                    else:
                        parameters[varname] = value

            elif '*PREAD' in line:
                # read a series of values
                st = line.find(',') + 1
                append_varname = line[st:st+8].strip()
                append_mode = True

    return parameters, arrays
