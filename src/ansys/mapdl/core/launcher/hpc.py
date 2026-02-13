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
import socket
import subprocess  # nosec B404
import time
from typing import Any, Dict, List, Optional

from ansys.mapdl.core import LOG
from ansys.mapdl.core.errors import MapdlDidNotStart

from .models import HPCJobInfo, LaunchConfig, ProcessInfo


def launch_on_hpc(config: LaunchConfig, env_vars: Dict[str, str]) -> ProcessInfo:
    """Launch MAPDL on HPC cluster via SLURM.

    Submits job to scheduler, waits for allocation, and returns
    connection info.

    Parameters:
        config: Launch configuration
        env_vars: Environment variables

    Returns:
        ProcessInfo with HPC job details

    Raises:
        MapdlDidNotStart: If job submission or allocation fails

    Examples:
        >>> config = LaunchConfig(launch_on_hpc=True, ...)
        >>> process_info = launch_on_hpc(config, env_vars)
        >>> process_info.jobid
        12345
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
    """Detect if running in SLURM environment.

    Checks for SLURM environment variables.

    Returns:
        True if SLURM environment detected

    Examples:
        >>> detect_slurm_environment()
        False
    """
    return bool(os.environ.get("SLURM_JOB_NAME") and os.environ.get("SLURM_JOB_ID"))


def resolve_slurm_resources(config: LaunchConfig) -> LaunchConfig:
    """Resolve resources from SLURM environment.

    Overrides nproc, ram based on SLURM allocation.

    Parameters:
        config: Initial configuration

    Returns:
        Updated configuration with SLURM resources

    Examples:
        >>> config = LaunchConfig(...)
        >>> updated = resolve_slurm_resources(config)
        >>> updated.nproc  # From SLURM allocation
        16
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
    """Generate MAPDL command for HPC.

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
        # Ensure -dis flag is present
        add_sw = config.additional_switches
        if "-dis " not in add_sw and not add_sw.endswith("-dis"):
            add_sw += " -dis"
        cmd.extend(add_sw.split())

    return cmd


def _generate_sbatch_command(
    mapdl_cmd: List[str], options: Optional[Dict[str, Any]]
) -> List[str]:
    """Generate sbatch submission command.

    Parameters:
        mapdl_cmd: MAPDL command to wrap
        options: Scheduler options

    Returns:
        sbatch command as list
    """
    cmd = ["sbatch"]

    # Add scheduler options
    if options:
        for key, value in options.items():
            if key == "wrap":
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

    # Add wrapped command
    mapdl_cmd_str = " ".join(mapdl_cmd)
    cmd.extend(["--wrap", f"'{mapdl_cmd_str}'"])

    LOG.debug(f"Generated sbatch command: {' '.join(cmd)}")
    return cmd


def _submit_job(cmd: List[str]) -> int:
    """Submit job and extract job ID.

    Parameters:
        cmd: sbatch command

    Returns:
        Job ID

    Raises:
        MapdlDidNotStart: If submission fails
    """
    LOG.info(f"Submitting HPC job: {' '.join(cmd)}")

    try:
        result = subprocess.run(
            cmd,
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
            f"Failed to submit HPC job:\n"
            f"Command: {' '.join(cmd)}\n"
            f"Error: {e.stderr}"
        )
    except ValueError as e:
        raise MapdlDidNotStart(f"Could not parse job ID from sbatch output: {e}")


def _wait_for_job_ready(jobid: int, timeout: int) -> HPCJobInfo:
    """Wait for job to reach RUNNING state.

    Polls scontrol until job is running or timeout.

    Parameters:
        jobid: SLURM job ID
        timeout: Maximum wait time

    Returns:
        HPCJobInfo with batch host details

    Raises:
        MapdlDidNotStart: If job doesn't start in time
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
    """Extract BatchHost from scontrol output.

    Parameters:
        scontrol_output: Output from scontrol command

    Returns:
        Batch host name

    Raises:
        ValueError: If BatchHost not found
    """
    for line in scontrol_output.split("\n"):
        if "BatchHost=" in line:
            host = line.split("BatchHost=")[1].split()[0].strip()
            return host

    raise ValueError("BatchHost not found in scontrol output")


def _parse_job_state(scontrol_output: str) -> str:
    """Extract JobState from scontrol output.

    Parameters:
        scontrol_output: Output from scontrol command

    Returns:
        Job state string

    Raises:
        ValueError: If JobState not found
    """
    for line in scontrol_output.split("\n"):
        if "JobState=" in line:
            state = line.split("JobState=")[1].split()[0].strip()
            return state

    raise ValueError("JobState not found in scontrol output")


def _calculate_slurm_nproc() -> Optional[int]:
    """Calculate nproc from SLURM environment.

    Returns:
        Number of processors or None
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
    """Calculate RAM from SLURM environment.

    Returns:
        RAM in MB or None
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
