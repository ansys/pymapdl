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
import psutil
from threading import Thread
import numpy as np

from ansys_corba import CORBA


def FindANSYS():
    """ Searches for ansys based on enviornmental variables """
    versions = []
    paths = []
    for var in os.environ:
        if 'ANSYS' in var:
            if '_DIR' in var:
                # import pdb; pdb.set_trace()
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

continue_idx = ready_items.index(b'YES,NO OR CONTINUOUS\)\=')
warning_idx = ready_items.index(b'executed\?')
error_idx = ready_items.index(b'SHOULD INPUT PROCESSING BE SUSPENDED\?')
prompt_idx = ready_items.index(b'ENTER FORMAT for')

nitems = len(ready_items)
expect_list = []
for item in ready_items:
    expect_list.append(re.compile(item))

# idenfity ignored commands
# ignored = re.compile('\s+'.join(['WARNING', 'command', 'ignored']))
ignored = re.compile('[\s\S]+'.join(['WARNING', 'command', 'ignored']))
# ignored = re.compile('[\s\S]+'.join(['WARNING', 'command', 'ignored']))
# re.DOTALL = True
# ignored = re.compile('(?:.|\n)+'.join(['WARNING', 'ignored']))
# ignored = re.compile('[\s\S]+'.join(['WARNING', 'ignored']))
# print(ignored.search(response))



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


def GetANSYSPath():
    """ Acquires ANSYS Path from a cached file or user input """
    if os.path.isfile(config_file):
        with open(config_file) as f:
            exe_loc = f.read()
        # verify
        if not os.path.isfile(exe_loc):
            print('Cached ANSYS executable %s not found' % exe_loc)
            exe_loc = SaveANSYSPath()
    else:  # create configuration file
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

    def __init__(self, exec_file=None, run_location=None, jobname='file', nproc=2,
                 override=False, loglevel='INFO', additional_switches='',
                 start_timeout=20):
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

        self.StartBroadcastLogger()

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
        def Listen():
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
                self.log.error(e)

        thread = Thread(target=Listen)
        thread.daemon = True  # allow ansys to be collected when finished
        thread.start()

    def SendCommand(self, command, threaded=False):
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
            import pdb; pdb.set_trace()
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

        if text:
            text = text.replace('\\n', '\n')
            self.log.info(text)

        if additional_text:
            additional_text = additional_text.replace('\\n', '\n')
            self.log.debug(additional_text)

        return text, additional_text

    def Run(self, command, return_response=False, block=True,
            continue_on_error=False, ignore_prompt=False, timeout=None):
        """ Sends command and returns ANSYS's response """
        return self.SendCommand(command)

        # if ignore_prompt:
            # self.log.debug('... with ignore_prompt=True')
        # self.process.sendline(command)
        

        # if block:
        #     self.log.debug('Waiting: TIMEOUT %s' % str(timeout))
        #     while True:
        #         i = self.process.expect_list(expect_list, timeout=timeout)
        #         response = self.process.before.decode('utf-8')
        #         if i >= continue_idx and i < warning_idx:  # continue
        #             self.log.debug('Continue: Response index %i.  Matched %s'
        #                            % (i, ready_items[i].decode('utf-8')))
        #             self.log.info(response + ready_items[i].decode('utf-8'))
        #             if self.auto_continue:
        #                 user_input = 'y'
        #             else:
        #                 user_input = input('Response: ')
        #             self.process.sendline(user_input)

        #         elif i >= warning_idx and i < error_idx:  # warning
        #             self.log.debug('Prompt: Response index %i.  Matched %s'
        #                            % (i, ready_items[i].decode('utf-8')))
        #             self.log.warning(response + ready_items[i].decode('utf-8'))
        #             if self.auto_continue:
        #                 user_input = 'y'
        #             else:
        #                 user_input = input('Response: ')
        #             self.process.sendline(user_input)

        #         elif i >= error_idx and i < prompt_idx:  # error
        #             self.log.debug('Error index %i.  Matched %s'
        #                            % (i, ready_items[i].decode('utf-8')))
        #             self.log.error(response)
        #             response += ready_items[i].decode('utf-8')
        #             if continue_on_error:
        #                 self.process.sendline(user_input)
        #             else:
        #                 raise Exception(response)

        #         elif i >= prompt_idx:  # prompt
        #             self.log.debug('Prompt index %i.  Matched %s'
        #                            % (i, ready_items[i].decode('utf-8')))
        #             self.log.info(response + ready_items[i].decode('utf-8'))
        #             if ignore_prompt:
        #                 self.log.debug('Ignoring prompt')
        #                 # time.sleep(0.1)
        #                 break
        #             else:
        #                 user_input = input('Response: ')
        #                 self.process.sendline(user_input)

        #         else:  # continue item
        #             self.log.debug('continue index %i.  Matched %s'
        #                            % (i, ready_items[i].decode('utf-8')))
        #             break

        #     # handle response
        #     if '*** ERROR ***' in response:  # flag error
        #         self.log.error(response)
        #         if not continue_on_error:
        #             raise Exception(response)
        #     elif ignored.search(response):  # flag ignored command
        #         if not self.allow_ignore:
        #             self.log.error(response)
        #             raise Exception(response)
        #         else:
        #             self.log.warning(response)
        #     else:  # all else
        #         self.log.info(response)

        #     if return_response:
        #         response = self.process.before.decode('utf-8')
        #         return response

    # def last_message(self):
    #     """ Returns the last output from ANSYS """
    #     return self.process.before.decode('utf-8')

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
                self.log.debug('Killing process %d' % self.process.pid)
                KillProcess(self.process.pid)
                self.log.debug('Killed' % self.process.pid)

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

