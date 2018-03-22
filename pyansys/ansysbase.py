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
import pexpect
import time
import pyansys

# settings directory
settings_dir = appdirs.user_data_dir('pyansys')
if not os.path.isdir(settings_dir):
    try:
        os.mkdir(settings_dir)
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


def SaveANSYSPath():
    # try:
    # check to see if the ansys path is stored as an env_var
    # for env_var in os.environ:
    #     if 'ANSYS' in env_var:
    #         if os.environ[env_var][-5:] == 'ANSYS':
    #             exe_loc = os.environ[env_var] + env_var[-4:]
    #             print('Found ANSYS at %s' % exe_loc)
    #             resp = input('Use this location?  [Y/n]')
    #             if resp != 'n':
    #                 return exe_loc

    # otherwise, query user for the location
    with open(config_file, 'w') as f:
        try:
            exe_loc = raw_input('Enter location of ANSYS executable: ')
        except NameError:
            exe_loc = input('Enter location of ANSYS executable: ')
        if not os.path.isfile(exe_loc):
            raise Exception('ANSYS executable not found at this location:\n%s' % exe_loc)

        f.write(exe_loc)
        # config = configparser.ConfigParser()
        # config['DEFAULT'] = {'ansys_app': exe_loc}
        # config.write(f)

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
        Number of processors.  Defaults to None, which for ANSYS this is usually 2.

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

    Examples
    --------
    >>> import pyansys
    >>> ansys = pyansys.ANSYS()

    """
    # default settings
    allow_ignore = False
    auto_continue = True
    block_override = None

    def __init__(self, exec_file=None, run_location=None, jobname='file', nproc=None,
                 override=False, wait=True, loglevel='INFO'):
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

        # initialize ANSYS process
        self.lockfile = os.path.join(run_location, jobname + '.lock')
        if os.path.isfile(self.lockfile):
            if not override:
                raise Exception('Lock file exists for jobname %s \n' % jobname +
                                'Set override=True to delete lock and start ANSYS')
            else:
                os.remove(self.lockfile)

        command = '%s -j %s ' % (exec_file, jobname)
        if nproc:
            command += '-np %d ' % nproc

        # add run location to command
        # command += '-dir "%s" ' % run_location
        self.log.debug('Spawning shell process with: "%s"' % command)
        self.log.debug('At "%s"' % run_location)
        if os.name == 'nt':
            from pexpect import popen_spawn
            self.process = popen_spawn.PopenSpawn(command, cwd=run_location)
        else:
            self.process = pexpect.spawn(command, cwd=run_location)
        self.process.delaybeforesend = None
        self.log.debug('Waiting')
        if wait:
            self.process.expect('CONTINUE')
            self.process.sendline('')  # enter to continue
            self.process.expect('BEGIN:')
            self.log.debug('Initialized ANSYS')
            self.log.debug(self.process.before.decode('utf-8'))

        # store for later reference
        self.path = run_location
        self.exec_file = exec_file
        self.jobname = jobname

    def SetLogLevel(self, loglevel):
        """ Sets log level """
        SetupLogger(loglevel=loglevel.upper())

    def __enter__(self):
        return self

    def RunCommand(self, command, return_response=False, block=True,
                   continue_on_error=False, ignore_prompt=False, timeout=None):
        """ Sends command and returns ANSYS's response """
        if not self.process.isalive():
            raise Exception('ANSYS process closed')

        if self.block_override is not None:
            block = self.block_override

        # send the command
        self.log.debug('Sending command %s' % command)
        if ignore_prompt:
            self.log.debug('... with ignore_prompt=True')
        self.process.sendline(command)

        if block:
            self.log.debug('Waiting: TIMEOUT %s' % str(timeout))
            while True:
                i = self.process.expect_list(expect_list, timeout=timeout)
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
                    if continue_on_error:
                        self.process.sendline(user_input)
                    else:
                        raise Exception(response)

                elif i >= prompt_idx:  # prompt
                    self.log.debug('Prompt index %i.  Matched %s'
                                   % (i, ready_items[i].decode('utf-8')))
                    self.log.info(response + ready_items[i].decode('utf-8'))
                    if ignore_prompt:
                        self.log.debug('Ignoring prompt')
                        # time.sleep(0.1)
                        break
                    else:
                        user_input = input('Response: ')
                        self.process.sendline(user_input)

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
            else:  # all else
                self.log.info(response)

            if return_response:
                response = self.process.before.decode('utf-8')
                return response

    def last_message(self):
        """ Returns the last output from ANSYS """
        return self.process.before.decode('utf-8')

    def __del__(self):
        self.process.sendline('FINISH')
        self.process.sendline('EXIT')

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.Exit()

    def Exit(self, twait=10):
        """
        Gracefully ANSYS process

        Returns True when process is still active.

        """
        self.process.sendline('FINISH')
        self.process.sendline('EXIT')
        t = time.time()
        wait_til = t + twait
        while self.process.isalive() and time.time() < wait_til:
            time.sleep(0.01)

        return self.process.isalive()

    def Kill(self):
        """ Forces ANSYS process to end and removes lock file """
        if self.process.terminate(True):
            if os.path.isfile:
                try:
                    os.remove(self.lockfile)
                except:
                    self.log.warning('Unable to remove lock file %s ' % self.lockfile)
        else:
            self.log.warning('Unable to terminate')
            return True

        return False

    @property
    def results(self):
        """ Returns a binary interface to the result file """
        resultfile = os.path.join(self.path, '%s.rst' % self.jobname)
        if not os.path.isfile(resultfile):
            raise Exception('No results found at %s' % resultfile)

        return pyansys.ResultReader(resultfile)

    def __call__(self, command, **kwargs):
        self.RunCommand(command, **kwargs)

