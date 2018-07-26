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
import pyansys
import subprocess
from threading import Thread
import weakref

import numpy as np
import psutil
from ansys_corba import CORBA

try:    
    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg
    matplotlib_loaded = True
except:
    matplotlib_loaded = False


def FindANSYS():
    """ Searches for ansys based on enviornmental variables """
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

png_test = re.compile('WRITTEN TO FILE file\d\d\d.png')
error_test = re.compile('')


def CheckValidANSYS():
    """ Checks if a valid version of ANSYS is installed and preconfigured """
    ansys_bin = GetANSYSPath(allow_input=False)
    if ansys_bin is not None:
        version = int(re.findall('\d\d\d', ansys_bin)[0])
        if version >= 170:
            return True

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


class ANSYS(object):
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

    Examples
    --------
    >>> import pyansys
    >>> ansys = pyansys.ANSYS()

    """
    # default settings
    allow_ignore = False
    block_override = None
    process = None
    lockfile = ''
    _interactive_plotting = False

    def __init__(self, exec_file=None, run_location=None, jobname='file', nproc=2,
                 override=False, loglevel='INFO', additional_switches='',
                 start_timeout=20, interactive_plotting=False, log_broadcast=True,
                 check_version=False):
        """ Initialize connection with ANSYS program """
        self.log = SetupLogger(loglevel.upper())

        if exec_file is None:
            # Load cached path
            try:
                exec_file = GetANSYSPath()
            except:
                raise Exception('Invalid or path or cannot load cached ansys path' +
                                'Enter one manually using pyansys.ANSYS(exec_file=...)')
        else:  # verify ansys exists at this location
            if not os.path.isfile(exec_file):
                raise Exception('Invalid ANSYS executable at %s' % exec_file +
                                'Enter one manually using pyansys.ANSYS(exec_file="")')

        # check ansys version
        if check_version:
            version = int(re.findall('\d\d\d', exec_file)[0])
            if version < 170:
                raise Exception('ANSYS MAPDL server requires version 17.0 or greater')

        # spawn temporary directory
        if run_location is None:
            temp_dir = tempfile.gettempdir()
            run_location = os.path.join(temp_dir, 'ansys')
            if not os.path.isdir(run_location):
                try:
                    os.mkdir(run_location)
                except:
                    raise Exception('Unable to create temporary working '
                                    'directory %s\n' % run_location +
                                    'Please specify run_location')
        else:
            if not os.path.isdir(run_location):
                raise Exception('%s is not a valid folder' % run_location)

        self.path = run_location

        # initialize ANSYS process
        self.lockfile = os.path.join(self.path, jobname + '.lock')
        if os.path.isfile(self.lockfile):
            if not override:
                raise Exception('Lock file exists for jobname %s \n' % jobname +
                                ' at %s' % self.lockfile +
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

        # command must include "aas" flag to start MAPDL server
        command = '"%s" -j %s -aas -i tmp.inp -o out.txt -b' % (exec_file, jobname)        
        if nproc:
            command += ' -np %d' % nproc

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
        while telapsed < start_timeout:
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
        if telapsed > start_timeout:
            err_msg = 'Unable to start ANSYS within %.1f seconds' % start_timeout
            self.log.error(err_msg)
            raise TimeoutError(err_msg)

        # open server
        keyfile = os.path.join(self.path, 'aaS_MapdlId.txt')
        with open(keyfile) as f:
            key = f.read()

        self.log.debug('Creating CORBA object with key %s' % key)
        orb = CORBA.ORB_init()
        self.mapdl = orb.string_to_object(key)

        # quick test
        try:
            self.mapdl.getComponentName()
        except:
            raise Exception('Unable to connect to APDL server')

        # store for later reference
        self.exec_file = exec_file
        self.jobname = jobname

        # setup plotting for PNG
        if interactive_plotting:
            self.EnableInteractivePlotting()

        # separate logger for broadcast file
        self.log_broadcast = log_broadcast
        if self.log_broadcast:
            self.broadcast_logger = Thread(target=ANSYS.StartBroadcastLogger,
                                           args=(weakref.proxy(self),))
            self.broadcast_logger.start()

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

    def RunCommand(**args):
        warnings.warn('Depreciated.  Use Run instead')

    @property
    def is_alive(self):
        if self.process is None:
            return False
        else:
            return self.process.poll() is None

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

    def SendCommand(self, command):
        """ Sends a command to the mapdl server """
        if not self.is_alive:
            raise Exception('ANSYS process has been terminated')

        # cleanup command
        command = command.strip()
        if not command:
            raise Exception('Empty command')

        # calling output kills the server
        if '/output' in command.lower():
            raise Exception('Cannot switch output in APDL server mode')        

        # include error checking
        text = ''
        additional_text = ''
        try:
            self.log.info('Running command %s' % command)
            text = self.mapdl.executeCommandToString(command)
            # print supressed output
            additional_text = self.mapdl.executeCommandToString('/GO')

        except Exception as e:
            error = str(e)
            if 'omniORB.TRANSIENT_ConnectFailed' in error:
                self.log.error(error)
                raise Exception('Unable to send command')
            elif 'WaitingForReply' in error:
                log.warning(error)

        if 'is not a recognized' in text:
            if not self.allow_ignore:
                text = text.replace('This command will be ignored.', '')
                text += '\n\nIgnore these messages by setting allow_ignore=True'
                raise Exception(text)

        return text, additional_text

    def Run(self, command):
        """ Sends command and returns ANSYS's response """
        text, additional_text = self.SendCommand(command)

        if text:
            text = text.replace('\\n', '\n')
            if '*** ERROR ***' in text:
                self.log.error(text)
                raise Exception(text)
            else:
                self.log.info(text)

        if additional_text:
            additional_text = additional_text.replace('\\n', '\n')
            if '*** ERROR ***' in additional_text:
                self.log.error(additional_text)
                raise Exception(additional_text)
            else:
                self.log.debug(additional_text)

        if self._interactive_plotting:
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

        return text, additional_text

    def __del__(self):
        # clean up when complete
        self.Kill()

    def __exit__(self, exc_type, exc_val, exc_tb):
        # clean up when complete
        self.Exit()

    def Exit(self):
        """
        Exit ANSYS process without attempting to kill the process.
        """
        self.log.debug('Terminating ANSYS')
        try:
            self.mapdl.terminate()
        except Exception as e:
            if 'WaitingForReply' not in str(e):
                raise Exception(e)

        self.log.info('ANSYS exited')

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

