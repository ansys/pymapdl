# Copyright (C) 2016 - 2026 ANSYS, Inc. and/or its affiliates.
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

"""Process management for MAPDL launcher.

Functions for launching MAPDL processes, monitoring their status,
and managing their lifecycle.
"""

import os
from queue import Empty, Queue
import subprocess  # nosec B404
import threading
import time
from typing import Any, Dict, List, Optional, Union

from ansys.mapdl.core import LOG
from ansys.mapdl.core.errors import MapdlDidNotStart

from .environment import is_wsl
from .models import LaunchConfig, ProcessInfo


def launch_mapdl_process(config: LaunchConfig, env_vars: Dict[str, str]) -> ProcessInfo:
    """Launch MAPDL process locally.

    Creates the subprocess, sets up monitoring, and waits for ready state.

    Parameters:
        config: Complete launch configuration
        env_vars: Environment variables for the process

    Returns:
        ProcessInfo with process handle and connection details

    Raises:
        MapdlDidNotStart: If process fails to start or times out

    Examples:
        >>> config = LaunchConfig(...)
        >>> env_config = prepare_environment(config)
        >>> process_info = launch_mapdl_process(config, env_config.variables)
        >>> process_info.pid
        12345
    """
    # Generate command
    cmd = _generate_launch_command(config)

    # Create temp input file (Windows only)
    if os.name == "nt" and not config.launch_on_hpc:
        _create_temp_input_file(config.run_location)

    # Launch process
    process = _start_subprocess(
        cmd=cmd,
        cwd=config.run_location,
        env=env_vars,
        output_file=config.mapdl_output,
    )

    # Wait for ready
    wait_for_process_ready(
        process=process,
        run_location=config.run_location,
        timeout=config.timeout,
        cmd=cmd,
    )

    return ProcessInfo(
        process=process,
        port=config.port,
        ip=config.ip,
        pid=process.pid if process else None,
    )


def wait_for_process_ready(
    process: subprocess.Popen[bytes],
    run_location: str,
    timeout: int,
    cmd: List[str],
) -> None:
    """Wait for MAPDL process to be ready.

    Checks multiple indicators:
    1. Process is still alive
    2. Error file created in run_location
    3. (Linux) gRPC server listening message in stdout

    Parameters:
        process: Running subprocess
        run_location: MAPDL working directory
        timeout: Maximum wait time in seconds
        cmd: Command used to launch (for error messages)

    Raises:
        MapdlDidNotStart: If process fails or times out
    """
    LOG.debug("Checking MAPDL process startup")

    # Set up stdout monitoring
    stdout_queue = _monitor_stdout(process.stdout)

    # Check process alive
    if process.poll() is not None:
        raise MapdlDidNotStart("MAPDL process died immediately after launch")

    # Check error file created
    _wait_for_error_file(run_location, timeout)

    # Linux: Check gRPC server message
    if os.name == "posix" and not is_wsl() and stdout_queue is not None:
        _check_grpc_server_ready(stdout_queue, timeout)

    LOG.info("MAPDL successfully started")


def _generate_launch_command(config: LaunchConfig) -> List[str]:
    """Generate MAPDL launch command from config.

    Parameters:
        config: Launch configuration

    Returns:
        Command as list of strings
    """
    cmd = [config.exec_file]

    # Core arguments
    cmd.extend(["-j", config.jobname])
    cmd.extend(["-np", str(config.nproc)])
    cmd.extend(["-port", str(config.port)])
    cmd.append("-grpc")

    # Resource arguments
    if config.ram:
        cmd.extend(["-m", str(config.ram)])

    # Additional switches
    if config.additional_switches:
        cmd.extend(config.additional_switches.split())

    # Windows-specific temp file arguments
    if os.name == "nt":
        cmd.extend(["-b", "-i", ".__tmp__.inp", "-o", ".__tmp__.out"])

    LOG.debug(f"Generated MAPDL command: {' '.join(cmd)}")
    return cmd


def _start_subprocess(
    cmd: List[str],
    cwd: str,
    env: Dict[str, str],
    output_file: Optional[str],
) -> subprocess.Popen[bytes]:
    """Start subprocess with proper I/O handling.

    Parameters:
        cmd: Command to execute
        cwd: Working directory
        env: Environment variables
        output_file: Optional file to redirect output

    Returns:
        Subprocess handle
    """
    # Set up output redirection
    if output_file:
        stdout_arg: Union[int, Any] = open(output_file, "wb", 0)
        stderr_arg: Union[int, int] = subprocess.STDOUT
    else:
        stdout_arg = subprocess.PIPE
        stderr_arg = subprocess.PIPE

    LOG.info(
        "\n============\n"
        "Running MAPDL instance\n"
        f"Location: {cwd}\n"
        f"Command: {' '.join(cmd)}\n"
        "============"
    )

    # Launch process
    process = subprocess.Popen(
        cmd,
        shell=False,  # Security: avoid shell injection  # nosec B603
        cwd=cwd,
        stdin=subprocess.DEVNULL,
        stdout=stdout_arg,
        stderr=stderr_arg,
        env=env,
    )

    LOG.debug(f"MAPDL process started with PID: {process.pid}")
    return process


def _create_temp_input_file(run_location: str) -> None:
    """Create temporary input file for Windows MAPDL launch.

    Parameters:
        run_location: MAPDL working directory
    """
    tmp_inp_path = os.path.join(run_location, ".__tmp__.inp")
    with open(tmp_inp_path, "w") as f:
        f.write("FINISH\r\n")
    LOG.debug(f"Created temporary input file: {tmp_inp_path}")


def _monitor_stdout(stdout: Optional[object]) -> Optional[Queue]:
    """Set up background thread to monitor stdout.

    Parameters:
        stdout: Subprocess stdout stream

    Returns:
        Queue for reading stdout or None
    """
    if not stdout:
        return None

    queue: Queue = Queue()

    def reader():
        """Background reader thread."""
        try:
            for line in iter(stdout.readline, b""):  # type: ignore
                queue.put(line)
            stdout.close()  # type: ignore
        except (ValueError, AttributeError):
            # Process terminated
            pass

    thread = threading.Thread(target=reader, daemon=True)
    thread.start()

    return queue


def _wait_for_error_file(run_location: str, timeout: int) -> None:
    """Wait for MAPDL to create error file (indicates startup).

    Parameters:
        run_location: MAPDL working directory
        timeout: Maximum wait time

    Raises:
        MapdlDidNotStart: If error file not created in time
    """
    sleep_time = 0.1
    iterations = int(timeout / sleep_time)

    for i in range(iterations):
        try:
            files = os.listdir(run_location)
            has_err = any(".err" in filename for filename in files)
            if has_err:
                LOG.debug("MAPDL error file found - startup confirmed")
                return
        except OSError as e:
            LOG.debug(f"Error checking directory: {e}")

        time.sleep(sleep_time)

    raise MapdlDidNotStart(
        f"MAPDL failed to start within {timeout} seconds. "
        f"No error file (.err) generated in working directory: {run_location}"
    )


def _check_grpc_server_ready(stdout_queue: Queue, timeout: int) -> None:
    """Check for gRPC server ready message in stdout.

    Parameters:
        stdout_queue: Queue receiving stdout
        timeout: Maximum wait time

    Raises:
        MapdlDidNotStart: If server message not found in time
    """
    start_time = time.time()
    output = ""

    LOG.debug("Checking for gRPC server ready message in stdout")

    while time.time() < (start_time + timeout):
        try:
            line = stdout_queue.get(timeout=0.1)
            if isinstance(line, bytes):
                output += line.decode("utf-8", errors="ignore")
            elif isinstance(line, str):
                output += line
        except Empty:
            # No new stdout available within the short timeout; this is expected during polling.
            pass

        # Check for server ready message
        if "GRPC SERVER" in output and "Server listening on" in output:
            LOG.debug("MAPDL gRPC server confirmed ready")
            return

        time.sleep(0.1)

    raise MapdlDidNotStart(
        f"MAPDL gRPC server did not start within {timeout} seconds. "
        f"Server message not found in stdout."
    )
