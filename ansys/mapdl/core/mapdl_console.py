"""Module to control interaction with an ANSYS shell instance.

Used when launching Mapdl via pexpect on Linux when <= 17.0
"""
import os
import time
import re

# from ansys.mapdl.core.misc import kill_process
from ansys.mapdl.core.mapdl import _MapdlCore
from ansys.mapdl.core.errors import MapdlExitedError

ready_items = [
    rb'BEGIN:',
    rb'PREP7:',
    rb'SOLU_LS[0-9]+:',
    rb'POST1:',
    rb'POST26:',
    rb'RUNSTAT:',
    rb'AUX2:',
    rb'AUX3:',
    rb'AUX12:',
    rb'AUX15:',
    # continue
    rb'YES,NO OR CONTINUOUS\)\=',
    rb'executed\?',
    # errors
    rb'SHOULD INPUT PROCESSING BE SUSPENDED\?',
    # prompts
    rb'ENTER FORMAT for',
]

CONTINUE_IDX = ready_items.index(rb'YES,NO OR CONTINUOUS\)\=')
WARNING_IDX = ready_items.index(rb'executed\?')
ERROR_IDX = ready_items.index(rb'SHOULD INPUT PROCESSING BE SUSPENDED\?')
PROMPT_IDX = ready_items.index(rb'ENTER FORMAT for')

nitems = len(ready_items)
expect_list = []
for item in ready_items:
    expect_list.append(re.compile(item))
ignored = re.compile(r'[\s\S]+'.join(['WARNING', 'command', 'ignored']))


def launch_pexpect(exec_file=None, run_location=None, jobname=None, nproc=None,
                   additional_switches='', start_timeout=60):
    """Launch MAPDL as a pexpect process.

    Limited to only a linux instance
    """
    import pexpect
    command = '%s -j %s -np %d %s' % (exec_file, jobname, nproc,
                                      additional_switches)
    process = pexpect.spawn(command, cwd=run_location)
    process.delaybeforesend = None

    try:
        index = process.expect(['BEGIN:', 'CONTINUE'],
                               timeout=start_timeout)
    except:  # capture failure
        raise RuntimeError(process.before.decode('utf-8'))

    if index:  # received ... press enter to continue
        process.sendline('')
        process.expect('BEGIN:', timeout=start_timeout)

    return process


class MapdlConsole(_MapdlCore):
    """Control interaction with an ANSYS shell instance.

    Only works on Linux.
    """

    def __init__(self, loglevel='INFO', log_apdl='w', use_vtk=True,
                 **start_parm):
        """Opens an ANSYS process using pexpect"""
        self._auto_continue = True
        self._continue_on_error = False
        self._process = None
        self._launch(start_parm)
        super().__init__(loglevel=loglevel, use_vtk=use_vtk, log_apdl=log_apdl,
                         **start_parm)

    def _launch(self, start_parm):
        """Connect to MAPDL process using pexpect"""
        self._process = launch_pexpect(**start_parm)

    def _run(self, command, **kwargs):
        """Sends command and returns ANSYS's response"""
        self._reset_cache()

        if not self._process.isalive():
            raise MapdlExitedError('ANSYS exited')

        command = command.strip()
        if not command:
            raise ValueError('Cannot run empty command')

        if command[:4].lower() == '/out':
            items = command.split(',')
            if len(items) > 1:
                self._output = '.'.join(items[1:])
            else:
                self._output = ''

        # send the command
        self._log.debug('Sending command %s', command)
        self._process.sendline(command)

        # do not expect
        if '/MENU' in command:
            self._log.info('Enabling GUI')
            self._process.sendline(command)
            return

        full_response = ''
        while True:
            i = self._process.expect_list(expect_list, timeout=None)
            response = self._process.before.decode('utf-8')
            full_response += response
            if i >= CONTINUE_IDX and i < WARNING_IDX:  # continue
                self._log.debug('Continue: Response index %i.  Matched %s',
                                i, ready_items[i].decode('utf-8'))
                self._log.info(response + ready_items[i].decode('utf-8'))
                if self._auto_continue:
                    user_input = 'y'
                else:
                    user_input = input('Response: ')
                self._process.sendline(user_input)

            elif i >= WARNING_IDX and i < ERROR_IDX:  # warning
                self._log.debug('Prompt: Response index %i.  Matched %s',
                                i, ready_items[i].decode('utf-8'))
                self._log.warning(response + ready_items[i].decode('utf-8'))
                if self._auto_continue:
                    user_input = 'y'
                else:
                    user_input = input('Response: ')
                self._process.sendline(user_input)

            elif i >= ERROR_IDX and i < PROMPT_IDX:  # error
                self._log.debug('Error index %i.  Matched %s',
                                i, ready_items[i].decode('utf-8'))
                self._log.error(response)
                response += ready_items[i].decode('utf-8')
                raise Exception(response)

            elif i >= PROMPT_IDX:  # prompt
                self._log.debug('Prompt index %i.  Matched %s',
                                i, ready_items[i].decode('utf-8'))
                self._log.info(response + ready_items[i].decode('utf-8'))
                raise RuntimeError('User input expected.  '
                                   'Try using ``with mapdl.non_interactive``')
            else:  # continue item
                self._log.debug('continue index %i.  Matched %s',
                                i, ready_items[i].decode('utf-8'))
                break

        # return last response and all preceding responses
        return full_response

    def exit(self, close_log=True, timeout=3):
        """Exit MAPDL process.

        Parameters
        ----------
        timeout : float
            Maximum time to wait for MAPDL to exit.  Set to 0 or
            ``None`` to not wait until MAPDL stops.
        """
        self._log.debug('Exiting ANSYS')
        if self._process is not None:
            try:
                self._process.sendline('FINISH')
                self._process.sendline('EXIT')
            except:
                pass

        if close_log:
            self._close_apdl_log()

        self._exited = True

        # edge case: need to wait until process dies, otherwise future
        # commands might talk to a dead process...
        if timeout:
            tstart = time.time()
            while self._process.isalive():
                time.sleep(0.05)
                telap = tstart - time.time()
                if telap > timeout:
                    return 1

        return 0

    def kill(self):
        """ Forces ANSYS process to end and removes lock file """
        if self._process is not None:
            try:
                self.exit()
            except:
                try:
                    os.kill(self._process.pid, 9)
                except:
                    self._log.warning('Unable to kill process %d', self._process.pid)
                self._log.debug('Killed process %d', self._process.pid)
