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
from typing import IO, Dict, List, Optional, Union

from ansys.mapdl.core import LOG
from ansys.mapdl.core.errors import MapdlDidNotStart

from .environment import is_wsl
from .models import LaunchConfig, ProcessInfo


def launch_mapdl_process(config: LaunchConfig, env_vars: Dict[str, str]) -> ProcessInfo:
    """Launch MAPDL process locally and wait for it to be ready.

    Creates the subprocess with proper I/O handling, sets up monitoring,
    and waits for the process to reach a ready state (indicated by creation
    of error file and/or gRPC server ready message).

    Parameters
    ----------
    config : LaunchConfig
        Complete launch configuration with executable path, working directory,
        resource settings, etc.
    env_vars : Dict[str, str]
        Environment variables to pass to the MAPDL process

    Returns
    -------
    ProcessInfo
        Process information containing process handle, PID, connection port and IP

    Raises
    ------
    MapdlDidNotStart
        If process fails to start, exits unexpectedly, or doesn't reach
        ready state within timeout

    Examples
    --------
    Launch MAPDL locally:

    >>> from ansys.mapdl.core.launcher.models import LaunchConfig
    >>> from ansys.mapdl.core.launcher.process import launch_mapdl_process
    >>> from ansys.mapdl.core.launcher.environment import prepare_environment
    >>> config = LaunchConfig(...)
    >>> env_config = prepare_environment(config)
    >>> process_info = launch_mapdl_process(config, env_config.variables)
    >>> print(f"MAPDL running with PID: {process_info.pid}")

    Notes
    -----
    - Creates temporary input file on Windows (.__tmp__.inp, .__tmp__.out)
    - Monitors stdout on Linux (posix) systems for gRPC server ready message
    - Waits for error file (.err) creation to confirm startup
    - Uses background thread to monitor stdout without blocking
    - On Windows, MAPDL runs in batch mode with temporary input/output files
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
    """Wait for MAPDL process to reach ready state.

    Monitors multiple indicators to ensure MAPDL is fully initialized:
    1. Verifies process is still alive
    2. Waits for run_location directory to be ready (network drive support)
    3. Checks for error file creation in run_location
    4. (Linux only) Validates gRPC server listening message in stdout

    Parameters
    ----------
    process : subprocess.Popen[bytes]
        Running subprocess handle
    run_location : str
        MAPDL working directory path
    timeout : int
        Maximum wait time in seconds
    cmd : List[str]
        Command used to launch process (for error messages)

    Returns
    -------
    None

    Raises
    ------
    MapdlDidNotStart
        If process dies, timeout is exceeded, or error file not created

    Examples
    --------
    Wait for process ready (typically called by launch_mapdl_process):

    >>> from ansys.mapdl.core.launcher.process import wait_for_process_ready
    >>> import subprocess
    >>> process = subprocess.Popen(...)
    >>> wait_for_process_ready(process, "/tmp/mapdl", timeout=60, cmd=cmd)

    Notes
    -----
    - Called automatically by launch_mapdl_process()
    - Checks directory ready to handle network drive delays
    - On Linux non-WSL: monitors stdout for gRPC server message
    - Raises immediately if process exits unexpectedly
    """
    LOG.debug("Checking MAPDL process startup")

    # Set up stdout monitoring
    stdout_queue = _monitor_stdout(process.stdout)

    # Check process alive
    if process.poll() is not None:
        raise MapdlDidNotStart("MAPDL process died immediately after launch")

    # Wait for the directory to be ready (handles potential delays in file system availability)
    _wait_directory_ready(run_location, timeout)

    # Check error file created
    _wait_for_error_file(run_location, timeout)

    # Linux: Check gRPC server message
    if os.name == "posix" and not is_wsl() and stdout_queue is not None:
        _check_grpc_server_ready(stdout_queue, timeout)

    LOG.info("MAPDL successfully started")


def _generate_launch_command(config: LaunchConfig) -> List[str]:
    """Generate MAPDL launch command from configuration.

    Constructs the complete command line for launching MAPDL including
    executable path, job name, processor count, port, RAM, switches, and
    platform-specific options.

    Parameters
    ----------
    config : LaunchConfig
        Launch configuration

    Returns
    -------
    List[str]
        Command components as list of strings (ready for subprocess)

    Raises
    ------
    None

    Examples
    --------
    Generate launch command:

    >>> from ansys.mapdl.core.launcher.models import LaunchConfig
    >>> from ansys.mapdl.core.launcher.process import _generate_launch_command
    >>> config = LaunchConfig(
    ...     exec_file="/usr/ansys/bin/mapdl",
    ...     jobname="job1",
    ...     nproc=4,
    ...     port=50052
    ... )
    >>> cmd = _generate_launch_command(config)
    >>> ' '.join(cmd)
    '/usr/ansys/bin/mapdl -j job1 -np 4 -port 50052 -grpc'

    Notes
    -----
    - Internal utility function
    - Always includes -grpc flag
    - Includes Windows-specific temp file arguments
    - Command is logged at DEBUG level
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
    """Start subprocess with proper I/O handling and environment.

    Creates subprocess with specified working directory, environment,
    and output redirection. Sets up stdin as DEVNULL and properly
    configures stdout/stderr handling.

    Parameters
    ----------
    cmd : List[str]
        Command to execute as list of strings
    cwd : str
        Working directory for subprocess
    env : Dict[str, str]
        Environment variables for subprocess
    output_file : Optional[str]
        Path to file for stdout/stderr redirection, or None for PIPE

    Returns
    -------
    subprocess.Popen[bytes]
        Running subprocess handle

    Raises
    ------
    FileNotFoundError
        If executable not found
    OSError
        If cannot start process (permission, etc.)

    Examples
    --------
    Start subprocess:

    >>> from ansys.mapdl.core.launcher.process import _start_subprocess
    >>> cmd = ["/usr/ansys/bin/mapdl", "-j", "job1", "-np", "4"]
    >>> process = _start_subprocess(
    ...     cmd=cmd,
    ...     cwd="/tmp/mapdl",
    ...     env={...},
    ...     output_file=None
    ... )

    Notes
    -----
    - Internal utility function
    - Disables shell for security (no shell injection possible)
    - STDIN is DEVNULL (subprocess cannot receive input)
    - Command is logged at INFO level
    - Process PID is logged at DEBUG level
    """
    # Set up output redirection
    stdout_arg: Union[int, IO[bytes]]
    stderr_arg: int

    if output_file:
        stdout_arg = open(output_file, "wb", 0)  # todo: handle file closing
        stderr_arg = subprocess.STDOUT
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
    """Create temporary input file for Windows MAPDL batch mode.

    Creates a minimal APDL input file (.__tmp__.inp) containing just
    FINISH command. This is required for Windows MAPDL batch execution.

    Parameters
    ----------
    run_location : str
        MAPDL working directory where temp file will be created

    Returns
    -------
    None

    Raises
    ------
    OSError
        If file cannot be created or written

    Examples
    --------
    Create temp input file:

    >>> from ansys.mapdl.core.launcher.process import _create_temp_input_file
    >>> _create_temp_input_file("/tmp/mapdl")

    Notes
    -----
    - Internal utility for Windows only
    - Creates .__tmp__.inp with FINISH\\r\\n
    - Called automatically by launch_mapdl_process on Windows
    - File is removed by MAPDL after processing
    """
    tmp_inp_path = os.path.join(run_location, ".__tmp__.inp")
    with open(tmp_inp_path, "w") as f:
        f.write("FINISH\r\n")
    LOG.debug(f"Created temporary input file: {tmp_inp_path}")


def _monitor_stdout(stdout: Optional[object]) -> Optional[Queue]:
    """Set up background thread to monitor subprocess stdout.

    Starts a daemon thread that reads lines from subprocess stdout and
    puts them into a thread-safe queue for asynchronous processing.
    Returns immediately without blocking.

    Parameters
    ----------
    stdout : Optional[object]
        Subprocess stdout stream from Popen

    Returns
    -------
    Optional[Queue]
        Queue for reading stdout lines, or None if stdout is not available

    Raises
    ------
    None

    Examples
    --------
    Monitor subprocess stdout:

    >>> from ansys.mapdl.core.launcher.process import _monitor_stdout
    >>> import subprocess
    >>> process = subprocess.Popen(..., stdout=subprocess.PIPE)
    >>> stdout_queue = _monitor_stdout(process.stdout)
    >>> if stdout_queue:
    ...     line = stdout_queue.get(timeout=1)

    Notes
    -----
    - Internal utility function
    - Runs in background daemon thread (won't block process exit)
    - Returns None if stdout cannot be monitored
    - Thread closes stdout when end-of-stream reached
    - Gracefully handles process termination
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


def _wait_directory_ready(run_location: str, timeout: int) -> None:
    """Wait for run_location directory to be ready and accessible.

    Handles delays in file system availability, particularly important for
    network-mounted drives where directory visibility may be delayed. Polls
    at 100ms intervals until timeout.

    Parameters
    ----------
    run_location : str
        Directory path to check
    timeout : int
        Maximum wait time in seconds

    Returns
    -------
    None

    Raises
    ------
    MapdlDidNotStart
        If directory is not ready within timeout

    Examples
    --------
    Wait for directory ready:

    >>> from ansys.mapdl.core.launcher.process import _wait_directory_ready
    >>> _wait_directory_ready("/tmp/mapdl", timeout=10)

    Notes
    -----
    - Internal utility function
    - Polls with 0.1 second sleep intervals
    - Logs DEBUG message when directory becomes ready
    - Logs path in error message for debugging
    """
    sleep_time = 0.1
    iterations = int(timeout / sleep_time)

    for i in range(iterations):
        if os.path.isdir(run_location):
            LOG.debug(f"Run location directory is ready: {run_location}")
            return
        time.sleep(sleep_time)

    raise MapdlDidNotStart(
        f"MAPDL failed to start within {timeout} seconds. "
        f"Run location directory not ready: {run_location}"
    )


def _wait_for_error_file(run_location: str, timeout: int) -> None:
    """Wait for MAPDL to create error file (.err) indicating startup.

    The creation of the .err file indicates that MAPDL has successfully
    initialized. Polls the run_location directory with 100ms intervals.

    Parameters
    ----------
    run_location : str
        MAPDL working directory to monitor
    timeout : int
        Maximum wait time in seconds

    Returns
    -------
    None

    Raises
    ------
    MapdlDidNotStart
        If error file not created within timeout

    Examples
    --------
    Wait for error file:

    >>> from ansys.mapdl.core.launcher.process import _wait_for_error_file
    >>> _wait_for_error_file("/tmp/mapdl", timeout=30)

    Notes
    -----
    - Internal utility function
    - Checks for any file containing ".err" in name
    - Polls with 0.1 second sleep intervals
    - Handles OSError when directory is inaccessible
    - Logs DEBUG message when file is found
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
    """Check for gRPC server ready message in subprocess stdout.

    Reads lines from stdout queue and searches for message indicating
    MAPDL gRPC server is listening. Must find both "GRPC SERVER" and
    "Server listening on" patterns.

    Parameters
    ----------
    stdout_queue : Queue
        Queue receiving stdout lines from subprocess
    timeout : int
        Maximum wait time in seconds

    Returns
    -------
    None

    Raises
    ------
    MapdlDidNotStart
        If server ready message not found within timeout

    Examples
    --------
    Check for gRPC server ready:

    >>> from ansys.mapdl.core.launcher.process import _check_grpc_server_ready
    >>> from queue import Queue
    >>> queue = Queue()
    >>> _check_grpc_server_ready(queue, timeout=30)

    Notes
    -----
    - Internal utility function, Linux (posix) only
    - Accumulates stdout output for pattern matching
    - Polls queue with 0.1 second timeout
    - Matches patterns: "GRPC SERVER" and "Server listening on"
    - Logs DEBUG message on success
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
