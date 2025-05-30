# Copyright (C) 2016 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Module to control interaction with an ANSYS shell instance.

Used when launching Mapdl via pexpect on Linux when <= 17.0
"""
import os
import re
import time
from warnings import warn

from ansys.mapdl.core import LOG
from ansys.mapdl.core.errors import MapdlExitedError, MapdlRuntimeError
from ansys.mapdl.core.mapdl import MapdlBase
from ansys.mapdl.core.misc import requires_package

ready_items = [
    rb"BEGIN:",
    rb"PREP7:",
    rb"SOLU_LS[0-9]+:",
    rb"POST1:",
    rb"POST26:",
    rb"RUNSTAT:",
    rb"AUX2:",
    rb"AUX3:",
    rb"AUX12:",
    rb"AUX15:",
    # continue
    rb"YES,NO OR CONTINUOUS\)\=",
    rb"executed\?",
    # errors
    rb"SHOULD INPUT PROCESSING BE SUSPENDED\?",
    rb"ANSYS Traceback",
    rb"eMPIChildJob",
    # prompts
    rb"ENTER FORMAT for",
]

CONTINUE_IDX = ready_items.index(rb"YES,NO OR CONTINUOUS\)\=")
WARNING_IDX = ready_items.index(rb"executed\?")
ERROR_IDX = ready_items.index(rb"SHOULD INPUT PROCESSING BE SUSPENDED\?")
PROMPT_IDX = ready_items.index(rb"ENTER FORMAT for")


nitems = len(ready_items)
expect_list = []
for item in ready_items:
    expect_list.append(re.compile(item))
ignored = re.compile(r"[\s\S]+".join(["WARNING", "command", "ignored"]))


def launch_pexpect(
    exec_file=None,
    run_location=None,
    jobname=None,
    nproc=None,
    additional_switches="",
    start_timeout=60,
):
    """Launch MAPDL as a pexpect process.

    Limited to only a linux instance
    """
    import pexpect

    command = "%s -j %s -np %d %s" % (
        exec_file,
        jobname,
        nproc,
        additional_switches,
    )
    process = pexpect.spawn(command, cwd=run_location, use_poll=True)
    process.delaybeforesend = None

    try:
        index = process.expect(["BEGIN:", "CONTINUE"], timeout=start_timeout)
    except Exception as err:  # capture failure
        raise RuntimeError(process.before.decode("utf-8") or err)

    if index:  # received ... press enter to continue
        process.sendline("")
        process.expect("BEGIN:", timeout=start_timeout)

    return process


class MapdlConsole(MapdlBase):
    """Control interaction with an ANSYS shell instance.

    Only works on Linux.
    """

    def __init__(
        self,
        loglevel="INFO",
        log_apdl=None,
        graphics_backend=True,
        print_com=False,
        set_no_abort=True,
        **start_parm,
    ):
        """Opens an ANSYS process using pexpect"""
        self._auto_continue = True
        self._continue_on_error = False
        self._process = None
        self._name = None
        self._session_id = None
        self._cleanup = None
        self.clean_response = True

        self._launch(start_parm)
        super().__init__(
            loglevel=loglevel,
            graphics_backend=graphics_backend,
            log_apdl=log_apdl,
            print_com=print_com,
            mode="console",
            **start_parm,
        )
        if set_no_abort:
            self.nerr(abort=-1, mute=True)

    def _launch(self, start_parm):
        """Connect to MAPDL process using pexpect"""
        self._process = launch_pexpect(**start_parm)

    def _run(self, command, **kwargs):
        """Sends command and returns ANSYS's response"""
        self._reset_cache()

        if not self._process.isalive():
            raise MapdlExitedError("ANSYS exited")

        command = command.strip()
        if not command:
            raise ValueError("Cannot run empty command")

        if command[:4].lower() == "/out":
            items = command.split(",")
            if len(items) > 1:
                self._output = ".".join(items[1:])
            else:
                self._output = ""

        # send the command
        self._log.debug("Sending command %s", command)
        self._process.sendline(command)

        # do not expect
        if "/MENU" in command:
            self._log.info("Enabling GUI")
            self._process.sendline(command)
            return

        full_response = ""
        while True:
            i = self._process.expect_list(expect_list, timeout=None)
            response = self._process.before.decode("utf-8")

            if self.clean_response:
                # Cleaning up responses
                response = response.strip().splitlines()
                if (
                    isinstance(response, list)
                    and len(response) > 0
                    and response[0].upper() == command.upper()
                ):
                    response = response[1:]

                response = "\n".join(response)

            full_response += response
            if i >= CONTINUE_IDX and i < WARNING_IDX:  # continue
                self._log.debug(
                    "Continue: Response index %i.  Matched %s",
                    i,
                    ready_items[i].decode("utf-8"),
                )
                self._log.info(response + ready_items[i].decode("utf-8"))
                if self._auto_continue:
                    user_input = "y"
                else:
                    user_input = input("Response: ")
                self._process.sendline(user_input)

            elif i >= WARNING_IDX and i < ERROR_IDX:  # warning
                self._log.debug(
                    "Prompt: Response index %i.  Matched %s",
                    i,
                    ready_items[i].decode("utf-8"),
                )
                self._log.warning(response + ready_items[i].decode("utf-8"))
                if self._auto_continue:
                    user_input = "y"
                else:
                    user_input = input("Response: ")
                self._process.sendline(user_input)

            elif i >= ERROR_IDX and i < PROMPT_IDX:  # error
                self._log.debug(
                    "Error index %i.  Matched %s",
                    i,
                    ready_items[i].decode("utf-8"),
                )
                self._log.error(response)
                response += ready_items[i].decode("utf-8")
                raise Exception(response)

            elif i >= PROMPT_IDX:  # prompt
                self._log.debug(
                    "Prompt index %i.  Matched %s",
                    i,
                    ready_items[i].decode("utf-8"),
                )
                self._log.info(response + ready_items[i].decode("utf-8"))
                raise MapdlRuntimeError(
                    "User input expected.  " "Try using ``with mapdl.non_interactive``"
                )
            else:  # continue item
                self._log.debug(
                    "continue index %i.  Matched %s",
                    i,
                    ready_items[i].decode("utf-8"),
                )
                break

        # return last response and all preceding responses
        return full_response

    @property
    @requires_package("ansys.mapdl.reader", softerror=True)
    @requires_package("pyvista", softerror=True)
    def mesh(self):
        """Mesh information.

        Returns
        -------
        :class:`Mapdl.Mesh <ansys.mapdl.core.mesh_grpc.Mesh>`

        Examples
        --------
        Return an array of the active nodes

        >>> mapdl.mesh.nodes
        array([[ 1.,  0.,  0.],
               [ 2.,  0.,  0.],
               [ 3.,  0.,  0.],
               [ 4.,  0.,  0.],
               [ 5.,  0.,  0.],
               [ 6.,  0.,  0.],
               [ 7.,  0.,  0.],
               [ 8.,  0.,  0.],
               [ 9.,  0.,  0.],
               [10.,  0.,  0.]])

        Return an array of the node numbers of the active nodes

        >>> mapdl.mesh.nnum
        array([ 1,  2,  3,  4,  5,  6,  7,  8,  9, 10], dtype=int32)

        Simply query and print the geometry

        >>> print(mapdl.mesh)
          ANSYS Mapdl Mesh
          Number of Nodes:              321
          Number of Elements:           40
          Number of Element Types:      1
          Number of Node Components:    2
          Number of Element Components: 2

        Access the geometry as a VTK object

        >>> mapdl.mesh.grid

        """
        return self._mesh

    def __del__(self):
        """Garbage cleaning the class"""
        self._exit()

    def _exit(self):
        """Minimal exit command. No logging or cleanup so it does not raise
        exceptions"""
        if self._process is not None:
            try:
                self._process.sendline("FINISH")
                self._process.sendline("EXIT")
            except Exception as e:
                LOG.warning(f"Unable to exit ANSYS MAPDL: {e}")

    def exit(self, close_log=True, timeout=3):
        """Exit MAPDL process.

        Parameters
        ----------
        timeout : float
            Maximum time to wait for MAPDL to exit.  Set to 0 or
            ``None`` to not wait until MAPDL stops.
        """
        self._log.debug("Exiting ANSYS")
        self._exit()

        if close_log:
            self._close_apdl_log()

        self._exited = True

        # edge case: need to wait until process dies, otherwise future
        # commands might talk to a dead process...
        if timeout:
            tstart = time.time()
            while self._process.isalive():
                time.sleep(0.05)
                if (time.time() - tstart) > timeout:
                    if self._process.isalive():
                        warn("MAPDL couldn't be exited on time.")
                        return

    def kill(self):
        """Forces ANSYS process to end and removes lock file"""
        if self._process is not None:
            try:
                self.exit()
            except:
                try:
                    os.kill(self._process.pid, 9)
                except:
                    self._log.warning("Unable to kill process %d", self._process.pid)
                self._log.debug("Killed process %d", self._process.pid)

    @MapdlBase.name.getter
    def name(self):
        """Instance unique identifier."""
        if not self._name:
            self._name = f"Console_PID_{self._process.pid}"
        return self._name

    def scalar_param(self, parm_name):
        response = self.starstatus(parm_name)
        response = response.splitlines()[-1]
        if parm_name.upper() not in response:
            raise ValueError(f"Parameter {parm_name} not found")
        return float(response.split()[1].strip())
