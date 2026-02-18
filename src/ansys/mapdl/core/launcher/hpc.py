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

"""HPC cluster integration for MAPDL launcher.

Functions for launching MAPDL on HPC clusters using SLURM scheduler.
Currently supports SLURM only.
"""

import os
import shlex
import socket
import subprocess  # nosec B404
import time
from typing import Any, Dict, List, Optional

from ansys.mapdl.core import LOG
from ansys.mapdl.core.errors import MapdlDidNotStart

from .models import HPCJobInfo, LaunchConfig, ProcessInfo


def launch_on_hpc(config: LaunchConfig, env_vars: Dict[str, str]) -> ProcessInfo:
    """Launch MAPDL on HPC cluster via SLURM scheduler.

    Submits a job to the SLURM scheduler, waits for the job to enter the
    RUNNING state, retrieves the compute node information, and returns
    connection details for accessing the MAPDL instance.

    Parameters
    ----------
    config : LaunchConfig
        Launch configuration with HPC-specific settings including
        scheduler_options, timeout, and port
    env_vars : Dict[str, str]
        Environment variables to pass to the SLURM job

    Returns
    -------
    ProcessInfo
        Process information containing job ID, hostname, IP address,
        and port for connecting to MAPDL on HPC

    Raises
    ------
    MapdlDidNotStart
        If job submission fails, job allocation times out, or job reaches
        a failed state (FAILED, CANCELLED, TIMEOUT, NODE_FAIL)

    Examples
    --------
    Launch MAPDL on HPC cluster:

    >>> from ansys.mapdl.core.launcher.models import LaunchConfig
    >>> from ansys.mapdl.core.launcher.hpc import launch_on_hpc
    >>> config = LaunchConfig(launch_on_hpc=True, ...)
    >>> env_vars = {"ANS_CMD_NODIAG": "TRUE"}
    >>> process_info = launch_on_hpc(config, env_vars)
    >>> print(f"Job ID: {process_info.jobid}")
    >>> print(f"Host: {process_info.hostname}")

    Notes
    -----
    - SLURM scheduler must be available on the system
    - Scheduler options are passed directly to sbatch command
    - Job ID can be used to monitor and cancel job with scontrol/scancel
    - The returned ProcessInfo has process=None since it's remote
    - Timeout applies to waiting for job to reach RUNNING state
    """
    # Generate base MAPDL command
    mapdl_cmd = _generate_mapdl_command(config)

    # Wrap in sbatch command
    sbatch_cmd = _generate_sbatch_command(mapdl_cmd, config.scheduler_options)

    # Submit job
    jobid = _submit_job(sbatch_cmd)

    # Wait for job to start and get host info
    job_info = _wait_for_job_ready(jobid, config.timeout)

    LOG.info(
        f"MAPDL job {jobid} successfully started on HPC: "
        f"{job_info.hostname} ({job_info.ip})"
    )

    return ProcessInfo(
        process=None,  # No local process handle
        port=config.port,
        ip=job_info.ip,
        pid=None,
        jobid=jobid,
        hostname=job_info.hostname,
    )


def detect_slurm_environment() -> bool:
    """Detect if running in a SLURM environment.

    Checks for the presence of SLURM environment variables that are
    set when running inside a SLURM job.

    Returns
    -------
    bool
        True if SLURM environment variables are detected, False otherwise

    Examples
    --------
    Check if running under SLURM:

    >>> from ansys.mapdl.core.launcher.hpc import detect_slurm_environment
    >>> if detect_slurm_environment():
    ...     print("Running on SLURM cluster")
    ... else:
    ...     print("Not in SLURM environment")

    Notes
    -----
    - Checks for presence of SLURM_JOB_NAME and SLURM_JOB_ID
    - Returns False on systems without SLURM
    - Returns False when not currently in a SLURM job allocation
    """
    return bool(os.environ.get("SLURM_JOB_NAME") and os.environ.get("SLURM_JOB_ID"))


def resolve_slurm_resources(config: LaunchConfig) -> LaunchConfig:
    """Resolve resource allocation from SLURM environment.

    Overrides nproc and RAM settings in the configuration based on
    current SLURM job allocation. Useful when launching MAPDL within
    an existing SLURM allocation to prevent over-subscription.

    Parameters
    ----------
    config : LaunchConfig
        Initial launch configuration

    Returns
    -------
    LaunchConfig
        Updated configuration with SLURM resources applied

    Raises
    ------
    None

    Examples
    --------
    Resolve SLURM resources:

    >>> from ansys.mapdl.core.launcher.models import LaunchConfig
    >>> from ansys.mapdl.core.launcher.hpc import resolve_slurm_resources
    >>> config = LaunchConfig(nproc=4, ram=8192)
    >>> updated = resolve_slurm_resources(config)
    >>> # If running under SLURM allocation with 16 CPUs:
    >>> # updated.nproc == 16 (from SLURM_NTASKS or similar)

    Notes
    -----
    - Respects SLURM_NTASKS, SLURM_CPUS_PER_TASK environment variables
    - Converts SLURM_MEM_PER_NODE from various units (K, M, G, T) to MB
    - Only updates fields where SLURM provides values
    - Returns original config unchanged if not in SLURM environment
    """
    # Get SLURM resources
    slurm_nproc = _calculate_slurm_nproc()
    slurm_ram = _calculate_slurm_ram()

    # Create updated config (immutable, so must create new)
    from dataclasses import replace

    if slurm_nproc is not None and slurm_ram is not None:
        LOG.info(f"Using SLURM allocated CPUs: {slurm_nproc}")
        LOG.info(f"Using SLURM allocated RAM: {slurm_ram} MB")
        return replace(config, nproc=slurm_nproc, ram=slurm_ram)
    elif slurm_nproc is not None:
        LOG.info(f"Using SLURM allocated CPUs: {slurm_nproc}")
        return replace(config, nproc=slurm_nproc)
    elif slurm_ram is not None:
        LOG.info(f"Using SLURM allocated RAM: {slurm_ram} MB")
        return replace(config, ram=slurm_ram)

    return config


def _generate_mapdl_command(config: LaunchConfig) -> List[str]:
    """Generate MAPDL launch command for HPC submission.

    Constructs the complete MAPDL command line based on configuration,
    including executable path, job name, processor count, port, and
    additional switches.

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
    Generate command for HPC:

    >>> from ansys.mapdl.core.launcher.models import LaunchConfig
    >>> config = LaunchConfig(exec_file="/usr/ansys/bin/mapdl", ...)
    >>> cmd = _generate_mapdl_command(config)
    >>> ' '.join(cmd)
    '/usr/ansys/bin/mapdl -j job1 -np 16 -port 50052 -grpc'

    Notes
    -----
    - Internal function for HPC submission
    - Always includes -grpc flag for consistency
    - Adds -dis flag to additional_switches if not present
    - Returns command as list for safe subprocess execution
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
        # Ensure -dis flag is present
        add_sw = config.additional_switches
        if "-dis " not in add_sw and not add_sw.endswith("-dis"):
            add_sw += " -dis"
        cmd.extend(add_sw.split())

    return cmd


def _generate_sbatch_command(
    mapdl_cmd: List[str], options: Optional[Dict[str, Any]]
) -> List[str]:
    """Generate sbatch submission command with proper shell escaping.

    Constructs a sbatch command that wraps the MAPDL command, applying
    scheduler options. Uses shlex.quote() to safely escape each command
    component, protecting against shell injection from special characters
    in jobname, exec_file, or additional_switches.

    Parameters
    ----------
    mapdl_cmd : List[str]
        MAPDL command components as list of strings
    options : Optional[Dict[str, Any]]
        SLURM scheduler options (e.g., {'nodes': '1', 'cpus-per-task': '4'})

    Returns
    -------
    List[str]
        sbatch command as list of strings

    Raises
    ------
    ValueError
        If 'wrap' option is found in options (reserved by PyMAPDL)

    Examples
    --------
    Generate sbatch command:

    >>> from ansys.mapdl.core.launcher.hpc import _generate_sbatch_command
    >>> mapdl_cmd = ['/usr/ansys/bin/mapdl', '-j', 'job1', '-np', '16']
    >>> options = {'nodes': '1', 'cpus-per-task': '4'}
    >>> sbatch = _generate_sbatch_command(mapdl_cmd, options)
    >>> ' '.join(sbatch)
    "sbatch --nodes=1 --cpus-per-task=4 --wrap='/usr/ansys/bin/mapdl -j job1 -np 16'"

    Notes
    -----
    - Each scheduler option key is automatically prefixed with - or --
    - Single character keys get single dash, multi-character get double dash
    - Uses shlex.quote() for proper shell escaping
    - The 'wrap' option is reserved and cannot be used
    """
    cmd = ["sbatch"]

    # Add scheduler options
    if options:
        for key, value in options.items():
            if key.lower() == "wrap":
                raise ValueError(
                    "The 'wrap' option is reserved by PyMAPDL. Please remove it."
                )

            # Format option with proper dashes
            if not key.startswith("-"):
                if len(key) == 1:
                    key = f"-{key}"
                else:
                    key = f"--{key}"

            cmd.append(f"{key}={value}")

    # Add wrapped command with proper escaping
    # Use shlex.quote() on each component to safely handle special characters
    # (e.g., single quotes in jobname or exec_file)
    quoted_mapdl_cmd = [shlex.quote(component) for component in mapdl_cmd]
    mapdl_cmd_str = " ".join(quoted_mapdl_cmd)
    cmd.extend(["--wrap", mapdl_cmd_str])

    LOG.debug(f"Generated sbatch command: {' '.join(cmd)}")
    return cmd


def _submit_job(cmd: List[str]) -> int:
    """Submit job to SLURM scheduler and extract job ID.

    Runs sbatch command and parses the response to extract the job ID.
    The SLURM scheduler returns "Submitted batch job <ID>" on success.

    Parameters
    ----------
    cmd : List[str]
        sbatch command as list of strings

    Returns
    -------
    int
        Job ID assigned by SLURM scheduler

    Raises
    ------
    MapdlDidNotStart
        If sbatch command fails or output cannot be parsed

    Examples
    --------
    Submit job to SLURM:

    >>> from ansys.mapdl.core.launcher.hpc import _submit_job
    >>> sbatch_cmd = ['sbatch', '--nodes=1', '--wrap=/path/to/mapdl']
    >>> job_id = _submit_job(sbatch_cmd)
    >>> print(f"Submitted job: {job_id}")

    Notes
    -----
    - Internal function used by launch_on_hpc()
    - Joins command into string and executes with shell
    - Parses "Submitted batch job XXXXX" format from sbatch
    """
    # Join command for shell execution
    cmd_str = " ".join(cmd)
    LOG.info(f"Submitting HPC job: {cmd_str}")

    try:
        result = subprocess.run(
            cmd_str,
            capture_output=True,
            text=True,
            shell=True,  # nosec B602 - sbatch requires shell
            check=True,
        )

        output = result.stdout.strip()

        # Parse job ID from "Submitted batch job 12345"
        if "Submitted batch job" not in output:
            raise MapdlDidNotStart(f"Unexpected sbatch output: {output}")

        jobid = int(output.split()[-1])
        LOG.info(f"HPC job submitted with ID: {jobid}")
        return jobid

    except subprocess.CalledProcessError as e:
        raise MapdlDidNotStart(
            f"Failed to submit HPC job:\n" f"Command: {cmd_str}\n" f"Error: {e.stderr}"
        )
    except ValueError as e:
        raise MapdlDidNotStart(f"Could not parse job ID from sbatch output: {e}")


def _wait_for_job_ready(jobid: int, timeout: int) -> HPCJobInfo:
    """Wait for SLURM job to reach RUNNING state.

    Polls the job status using scontrol until the job reaches RUNNING state
    or timeout is exceeded. Extracts batch host and resolves its IP address.

    Parameters
    ----------
    jobid : int
        SLURM job ID to monitor

    timeout : int
        Maximum time in seconds to wait for job to start

    Returns
    -------
    HPCJobInfo
        Job information including job ID, state, hostname, and IP address

    Raises
    ------
    MapdlDidNotStart
        If job doesn't reach RUNNING state within timeout or enters failed state

    Examples
    --------
    Wait for job to start:

    >>> from ansys.mapdl.core.launcher.hpc import _wait_for_job_ready
    >>> job_info = _wait_for_job_ready(12345, timeout=600)
    >>> print(f"Job running on {job_info.hostname} ({job_info.ip})")

    Notes
    -----
    - Internal function used by launch_on_hpc()
    - Polls every 1 second
    - Recognizes failed states: FAILED, CANCELLED, TIMEOUT, NODE_FAIL
    - Uses scontrol show jobid command for job status
    - Resolves hostname to IP using socket.gethostbyname()
    """
    LOG.info(f"Waiting for HPC job {jobid} to start (timeout: {timeout}s)")

    start_time = time.time()
    last_state = "UNKNOWN"

    while time.time() - start_time < timeout:
        # Query job status
        try:
            result = subprocess.run(  # nosec B603, B607
                ["scontrol", "show", "jobid", "-dd", str(jobid)],
                capture_output=True,
                text=True,
                check=True,
                timeout=10,
            )

            output = result.stdout

            # Parse state
            state = _parse_job_state(output)
            if state != last_state:
                LOG.debug(f"Job {jobid} state: {state}")
                last_state = state

            # Check if running
            if state == "RUNNING":
                # Extract hostname and IP
                hostname = _parse_batch_host(output)
                ip = socket.gethostbyname(hostname)

                return HPCJobInfo(jobid=jobid, state=state, hostname=hostname, ip=ip)

            # Check for failed states
            if state in ("FAILED", "CANCELLED", "TIMEOUT", "NODE_FAIL"):
                raise MapdlDidNotStart(
                    f"HPC job {jobid} failed with state: {state}. "
                    f"Check job logs for details."
                )

        except subprocess.TimeoutExpired:
            LOG.warning("scontrol command timed out, retrying...")
        except subprocess.CalledProcessError as e:
            LOG.warning(f"scontrol error: {e.stderr}")

        time.sleep(1)

    # Timeout reached
    raise MapdlDidNotStart(
        f"HPC job {jobid} did not start within {timeout} seconds. "
        f"Last known state: {last_state}. "
        f"Check job status with: scontrol show jobid -dd {jobid}"
    )


def _parse_batch_host(scontrol_output: str) -> str:
    """Extract BatchHost from scontrol command output.

    Parses the output of 'scontrol show jobid' to find the BatchHost
    field which specifies the compute node where the job is running.

    Parameters
    ----------
    scontrol_output : str
        Raw output from scontrol command

    Returns
    -------
    str
        Batch host name (e.g., 'compute-node-05')

    Raises
    ------
    ValueError
        If BatchHost field not found in output

    Examples
    --------
    Parse batch host:

    >>> from ansys.mapdl.core.launcher.hpc import _parse_batch_host
    >>> output = '''JobID=12345 ArrayJobID=N/A
    ... BatchHost=compute-node-05
    ... JobState=RUNNING'''
    >>> _parse_batch_host(output)
    'compute-node-05'

    Notes
    -----
    - Searches for line containing "BatchHost=" prefix
    - Internal utility function
    """
    for line in scontrol_output.split("\n"):
        if "BatchHost=" in line:
            host = line.split("BatchHost=")[1].split()[0].strip()
            return host

    raise ValueError("BatchHost not found in scontrol output")


def _parse_job_state(scontrol_output: str) -> str:
    """Extract JobState from scontrol command output.

    Parses the output of 'scontrol show jobid' to find the JobState
    field which indicates the current state of the job.

    Parameters
    ----------
    scontrol_output : str
        Raw output from scontrol command

    Returns
    -------
    str
        Job state string (e.g., 'PENDING', 'RUNNING', 'FAILED')

    Raises
    ------
    ValueError
        If JobState field not found in output

    Examples
    --------
    Parse job state:

    >>> from ansys.mapdl.core.launcher.hpc import _parse_job_state
    >>> output = '''JobID=12345 ArrayJobID=N/A
    ... JobState=RUNNING
    ... BatchHost=compute-node-05'''
    >>> _parse_job_state(output)
    'RUNNING'

    Notes
    -----
    - Searches for line containing "JobState=" prefix
    - Internal utility function
    - Common states: PENDING, RUNNING, COMPLETED, FAILED, CANCELLED, TIMEOUT
    """
    for line in scontrol_output.split("\n"):
        if "JobState=" in line:
            state = line.split("JobState=")[1].split()[0].strip()
            return state

    raise ValueError("JobState not found in scontrol output")


def _calculate_slurm_nproc() -> Optional[int]:
    """Calculate processor count from SLURM environment variables.

    Determines the number of processors from SLURM_NTASKS and
    SLURM_CPUS_PER_TASK environment variables, with fallback to
    individual values if only one is available.

    Returns
    -------
    Optional[int]
        Number of processors, or None if SLURM variables not set

    Raises
    ------
    None

    Examples
    --------
    Calculate SLURM processors:

    >>> from ansys.mapdl.core.launcher.hpc import _calculate_slurm_nproc
    >>> # If SLURM_NTASKS=4, SLURM_CPUS_PER_TASK=4
    >>> _calculate_slurm_nproc()
    16

    Notes
    -----
    - Internal utility function
    - Used by resolve_slurm_resources()
    - Priority: ntasks * cpus_per_task > ntasks > cpus_per_task
    """
    ntasks = os.environ.get("SLURM_NTASKS")
    cpus_per_task = os.environ.get("SLURM_CPUS_PER_TASK")

    if ntasks and cpus_per_task:
        return int(ntasks) * int(cpus_per_task)
    elif ntasks:
        return int(ntasks)
    elif cpus_per_task:
        return int(cpus_per_task)

    return None


def _calculate_slurm_ram() -> Optional[int]:
    """Calculate RAM allocation from SLURM environment variables.

    Parses SLURM_MEM_PER_NODE environment variable and converts to MB.
    Supports various memory units (K, M, G, T).

    Returns
    -------
    Optional[int]
        RAM allocation in MB, or None if not set or cannot be parsed

    Examples
    --------
    Calculate SLURM RAM:

    >>> from ansys.mapdl.core.launcher.hpc import _calculate_slurm_ram
    >>> # If SLURM_MEM_PER_NODE="8G"
    >>> _calculate_slurm_ram()
    8192

    >>> # If SLURM_MEM_PER_NODE="2048M"
    >>> _calculate_slurm_ram()
    2048

    Notes
    -----
    - Internal utility function
    - Used by resolve_slurm_resources()
    - Supports: K (kilobytes), M (megabytes), G (gigabytes), T (terabytes)
    - Defaults to MB if no unit specified
    - Returns None and logs warning on parse errors
    """
    mem = os.environ.get("SLURM_MEM_PER_NODE")
    if not mem:
        return None

    # Parse memory with unit (e.g., "8G", "4096M")
    try:
        if mem[-1].isalpha():
            unit = mem[-1].upper()
            value = int(mem[:-1])

            # Convert to MB
            if unit == "T":
                return value * 1024 * 1024
            elif unit == "G":
                return value * 1024
            elif unit == "M":
                return value
            elif unit == "K":
                return value // 1024
        else:
            # Assume MB if no unit
            return int(mem)
    except (ValueError, IndexError):
        LOG.warning(f"Could not parse SLURM_MEM_PER_NODE: {mem}")

    return None
