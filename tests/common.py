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

"""Shared testing module"""
from collections import namedtuple
import os
import subprocess
import time
from typing import Dict, List

import psutil

from ansys.mapdl.core import LOG, Mapdl
from ansys.mapdl.core.errors import MapdlConnectionError, MapdlExitedError
from ansys.mapdl.core.launcher import (
    _is_ubuntu,
    is_ansys_process,
    launch_mapdl,
)

PROCESS_OK_STATUS = [
    psutil.STATUS_RUNNING,  #
    psutil.STATUS_SLEEPING,  #
    psutil.STATUS_DISK_SLEEP,
    psutil.STATUS_DEAD,
    psutil.STATUS_PARKED,  # (Linux)
    psutil.STATUS_IDLE,  # (Linux, macOS, FreeBSD)
]

Node = namedtuple("Node", ["number", "x", "y", "z", "thx", "thy", "thz"])
Element = namedtuple(
    "Element",
    [
        "number",
        "material",
        "type",
        "real_const",
        "coord_system",
        "section",
        "node_numbers",
    ],
)


# Set if on local
def is_on_local():
    if os.environ.get("ON_LOCAL"):
        return os.environ.get("ON_LOCAL").lower() == "true"

    if os.environ.get("ON_REMOTE"):
        return os.environ.get("ON_REMOTE").lower() == "true"

    if os.environ.get("PYMAPDL_START_INSTANCE"):
        return (
            os.environ.get("PYMAPDL_START_INSTANCE").lower() != "false"
        )  # default is false

    from ansys.tools.path import find_mapdl

    _, rver = find_mapdl()

    if rver:
        return True
    else:
        return False


# Set if on CI
def is_on_ci():
    return os.environ.get("ON_CI", "").lower() == "true"


# Set if on ubuntu
def is_on_ubuntu():
    envvar = os.environ.get("ON_UBUNTU")

    if envvar is not None:
        return envvar.lower() == "true"

    return _is_ubuntu()


def has_grpc():
    envvar = os.environ.get("HAS_GRPC")

    if envvar is not None:
        return envvar.lower().strip() == "true"

    if testing_minimal():
        return True

    try:
        from ansys.tools.path import find_mapdl
    except ModuleNotFoundError:
        return True

    _, rver = find_mapdl()

    if rver:
        rver = int(rver * 10)
        return int(rver) >= 211
    else:
        return True  # In remote mode, assume gRPC by default.


def has_dpf():
    return bool(os.environ.get("HAS_DPF", "false").lower() == "true")


def is_smp():
    return os.environ.get("DISTRIBUTED_MODE", "smp").lower().strip() == "smp"


def support_plotting():
    envvar = os.environ.get("SUPPORT_PLOTTING")

    if envvar is not None:
        return envvar.lower().strip() == "true"

    if testing_minimal():
        return False

    try:
        import pyvista

        return pyvista.system_supports_plotting()

    except ModuleNotFoundError:
        return False


def is_running_on_student():
    return os.environ.get("ON_STUDENT", "NO").upper().strip() in ["YES", "TRUE"]


def testing_minimal():
    return os.environ.get("TESTING_MINIMAL", "NO").upper().strip() in ["YES", "TRUE"]


def debug_testing() -> bool:
    if "PYMAPDL_DEBUG_TESTING" in os.environ:
        debug_testing = os.environ["PYMAPDL_DEBUG_TESTING"]

        if debug_testing.lower() in ["true", "false", "yes", "no"]:
            return debug_testing.lower() in ["true", "yes"]
        else:
            return debug_testing

    else:
        return False


def testing_dpf_backend() -> bool:
    return os.environ.get("TEST_DPF_BACKEND", "NO").upper().strip() in ["YES", "TRUE"]


def is_float(s: str) -> bool:
    try:
        float(s)
        return True
    except ValueError:
        return False


def is_just_floats(s: str, delimiter=None):
    if delimiter is None:
        entries = s.split()
    else:
        entries = s.split(delimiter)
    if not entries:
        return False
    for entry in entries:
        if not is_float(entry.strip()):
            return False
    return True


def get_details_of_nodes(mapdl_) -> Dict[int, Node]:
    string = mapdl_.nlist("ALL")
    rows = string.split("\n")
    nodes = {}
    for row in rows:
        if is_just_floats(row):
            row_values = [v for v in row.split(" ") if v != ""]
            node = int(row_values[0])
            nodes[node] = Node(node, *[float(rv) for rv in row_values[1:]])
    return nodes


def get_details_of_elements(mapdl_) -> Dict[int, Node]:
    string = mapdl_.elist("ALL")
    # string = string.split(' ELEM ')[1]
    # string = string.split('\n', 1)[1]
    rows = string.split("\n")
    elements = {}
    for row in rows:
        if is_just_floats(row):
            row_values = [v for v in row.split(" ") if v != ""]
            args = [int(rv) for rv in row_values[:6]]
            # todo: Node numbers can go over multiple lines, which makes
            #  parsing them properly a real pain. So for now I'll leave
            #  this as is and work on a better version in the future
            if len(args) == 6:
                elements[args[0]] = Element(*args, node_numbers=None)  # type: ignore
    return elements


def log_start_test(mapdl: Mapdl, test_name: str) -> None:
    """Print the current test to the MAPDL log file and console output."""
    # To see it also in MAPDL terminal output
    if len(test_name) > 75:
        # terminal output is limited to 75 characters
        test_name_ = test_name.split("::")
        if len(test_name_) > 2:
            types_ = ["File path", "Test class", "Method"]
        else:
            types_ = ["File path", "Test function"]

        mapdl.com("Running test in:", mute=True)

        for type_, name_ in zip(types_, test_name_):
            mapdl.com(f"    {type_}: {name_}", mute=True)

    else:
        mapdl.com(f"Running test: {test_name}", mute=True)


def log_end_test(mapdl: Mapdl, test_name: str) -> None:
    mapdl.com("!", mute=True)
    mapdl.com(f"! End of test: {test_name.split('::')[1]}"[:639], mute=True)
    mapdl.com("!", mute=True)


def restart_mapdl(mapdl: Mapdl, test_name: str = "") -> Mapdl:
    """Restart MAPDL after a failed test"""
    from conftest import ON_LOCAL

    def is_exited(mapdl: Mapdl):
        try:
            _ = mapdl._ctrl("VERSION")
            return False
        except MapdlExitedError:
            return True

    LOG.debug("Checking if MAPDL is exited...")
    if mapdl.exited or is_exited(mapdl):

        if ON_LOCAL:
            # First we try to reconnect
            try:
                LOG.debug("Reconnecting to MAPDL...")
                mapdl.reconnect_to_mapdl(timeout=5)
                assert mapdl.finish()

                LOG.debug("Reconnected to MAPDL successfully.")
                return mapdl

            except MapdlConnectionError as e:
                LOG.warning(
                    f"Failed to reconnect to MAPDL... Attempting to relaunch MAPDL.\n{str(e)}"
                )

            # Killing the instance (just in case)
            try:

                LOG.debug("Exiting MAPDL...")
                mapdl.exit(force=True)
            except Exception as e:
                LOG.warning(f"Failed to exit MAPDL: {str(e)}")

            # Relaunching MAPDL
            LOG.debug("Relaunching MAPDL...")
            new_mapdl = launch_mapdl(
                port=mapdl._port,
                override=True,
                run_location=mapdl._path,
                cleanup_on_exit=mapdl._cleanup,
                license_server_check=False,
                start_timeout=10,
            )
            LOG.info("MAPDL died during testing, relaunched.")

            LOG.debug("Closing old channel...")
            new_mapdl.channel.close()  # close the old channel
            del new_mapdl  # delete the old mapdl instance

            # Restoring the configuration
            mapdl._exited = False

        else:
            # In remote mode, we just try to reconnect
            LOG.debug("Remote MAPDL is exited, trying to reconnect...")
            mapdl.reconnect_to_mapdl(timeout=10)

        assert mapdl.finish()
        assert mapdl.prep7()

        LOG.info("Successfully relaunched/re-connected to MAPDL")

    return mapdl


def make_sure_not_instances_are_left_open(valid_ports: List) -> None:
    """Make sure we leave no MAPDL running behind"""

    if is_on_local():
        for proc in psutil.process_iter():
            try:
                if (
                    psutil.pid_exists(proc.pid)
                    and proc.status() in PROCESS_OK_STATUS
                    and is_ansys_process(proc)
                ):
                    cmdline = proc.cmdline()
                    port = int(cmdline[cmdline.index("-port") + 1])

                    if port not in valid_ports:
                        subprocess.run(["pymapdl", "stop", "--port", f"{port}"])
                        time.sleep(1)
            except psutil.NoSuchProcess:
                continue
