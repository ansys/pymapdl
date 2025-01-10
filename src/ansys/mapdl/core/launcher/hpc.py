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

import os
import socket
import subprocess
import time
from typing import Any, Callable, Dict, List, Optional, Union

from ansys.mapdl.core import LOG
from ansys.mapdl.core.errors import MapdlDidNotStart
from ansys.mapdl.core.launcher.grpc import launch_grpc
from ansys.mapdl.core.launcher.tools import submitter
from ansys.mapdl.core.mapdl_grpc import MapdlGrpc

LAUNCH_ON_HCP_ERROR_MESSAGE_IP = (
    "PyMAPDL cannot ensure a specific IP will be used when launching "
    "MAPDL on a cluster. Hence the 'ip' argument is not compatible. "
    "If you want to connect to an already started MAPDL instance, "
    "just connect normally as you would with a remote instance. "
    "For example:\n\n"
    ">>> mapdl = launch_mapdl(start_instance=False, ip='123.45.67.89')\n\n"
    "where '123.45.67.89' is the IP of the machine where MAPDL is running."
)


def is_running_on_slurm(args: Dict[str, Any]) -> bool:
    running_on_hpc_env_var = os.environ.get("PYMAPDL_RUNNING_ON_HPC", "True")

    is_flag_false = running_on_hpc_env_var.lower() == "false"

    # Let's require the following env vars to exist to go into slurm mode.
    args["running_on_hpc"] = bool(
        args["running_on_hpc"]
        and not is_flag_false  # default is true
        and os.environ.get("SLURM_JOB_NAME")
        and os.environ.get("SLURM_JOB_ID")
    )
    return args["running_on_hpc"]


def kill_job(jobid: int) -> subprocess.Popen:
    """Kill SLURM job"""
    submitter(["scancel", str(jobid)])


def send_scontrol(args: str) -> subprocess.Popen:
    cmd = f"scontrol {args}".split(" ")
    return submitter(cmd)


def check_mapdl_launch_on_hpc(
    process: subprocess.Popen, start_parm: Dict[str, str]
) -> int:
    """Check if the job is ready on the HPC

    Check if the job has been successfully submitted, and additionally, it does
    retrieve the BathcHost hostname which is the IP to connect to using the gRPC
    interface.

    Parameters
    ----------
    process : subprocess.Popen
        Process used to submit the job. The stdout is read from there.
    start_parm : Dict[str, str]
        To store the job ID, the BatchHost hostname and IP into.

    Returns
    -------
    int :
        The jobID

    Raises
    ------
    MapdlDidNotStart
        The job submission failed.
    """
    stdout = process.stdout.read().decode()
    if "Submitted batch job" not in stdout:
        stderr = process.stderr.read().decode()
        raise MapdlDidNotStart(
            "PyMAPDL failed to submit the sbatch job:\n"
            f"stdout:\n{stdout}\nstderr:\n{stderr}"
        )

    jobid = get_jobid(stdout)
    LOG.info(f"HPC job successfully submitted. JobID: {jobid}")
    return jobid


def get_job_info(
    start_parm: Dict[str, str], jobid: Optional[int] = None, timeout: int = 30
) -> None:
    """Get job info like BatchHost IP and hostname

    Get BatchHost hostname and ip and stores them in the start_parm argument

    Parameters
    ----------
    start_parm : Dict[str, str]
        Starting parameters for MAPDL.
    jobid : int
        Job ID
    timeout : int
        Timeout for checking if the job is ready. Default checks for
        'start_instance' key in the 'start_parm' argument, if none
        is found, it passes :class:`None` to
        :func:`ansys.mapdl.core.launcher.hpc.get_hostname_host_cluster`.
    """
    timeout = timeout or start_parm.get("start_instance")

    jobid = jobid or start_parm["jobid"]

    batch_host, batch_ip = get_hostname_host_cluster(jobid, timeout=timeout)

    start_parm["ip"] = batch_ip
    start_parm["hostname"] = batch_host
    start_parm["jobid"] = jobid


def get_hostname_host_cluster(job_id: int, timeout: int = 30) -> str:
    options = f"show jobid -dd {job_id}"
    LOG.debug(f"Executing the command 'scontrol {options}'")

    ready = False
    time_start = time.time()
    counter = 0
    while not ready:
        proc = send_scontrol(options)

        stdout = proc.stdout.read().decode()
        if "JobState=RUNNING" not in stdout:
            counter += 1
            time.sleep(1)
            if (counter % 3 + 1) == 0:  # print every 3 seconds. Skipping the first.
                LOG.debug("The job is not ready yet. Waiting...")
                print("The job is not ready yet. Waiting...")
        else:
            ready = True
            break

        # Exit by raising exception
        if time.time() > time_start + timeout:
            state = get_state_from_scontrol(stdout)

            # Trying to get the hostname from the last valid message
            try:
                host = get_hostname_from_scontrol(stdout)
                if not host:
                    # If string is empty, go to the exception clause.
                    raise IndexError()

                hostname_msg = f"The BatchHost for this job is '{host}'"
            except (IndexError, AttributeError):
                hostname_msg = "PyMAPDL couldn't get the BatchHost hostname"

            # Raising exception
            raise MapdlDidNotStart(
                f"The HPC job (id: {job_id}) didn't start on time (timeout={timeout}). "
                f"The job state is '{state}'. "
                f"{hostname_msg}. "
                "You can check more information by issuing in your console:\n"
                f" scontrol show jobid -dd {job_id}"
            )

    LOG.debug(f"The 'scontrol' command returned:\n{stdout}")
    batchhost = get_hostname_from_scontrol(stdout)
    LOG.debug(f"Batchhost: {batchhost}")

    # we should validate
    batchhost_ip = socket.gethostbyname(batchhost)
    LOG.debug(f"Batchhost IP: {batchhost_ip}")

    LOG.info(
        f"Job {job_id} successfully allocated and running in '{batchhost}'({batchhost_ip})"
    )
    return batchhost, batchhost_ip


def get_jobid(stdout: str) -> int:
    """Extract the jobid from a command output"""
    job_id = stdout.strip().split(" ")[-1]

    try:
        job_id = int(job_id)
    except ValueError:
        LOG.error(f"The console output does not seems to have a valid jobid:\n{stdout}")
        raise ValueError("PyMAPDL could not retrieve the job id.")

    LOG.debug(f"The job id is: {job_id}")
    return job_id


def generate_sbatch_command(
    cmd: Union[str, List[str]], scheduler_options: Optional[Union[str, Dict[str, str]]]
) -> List[str]:
    """Generate sbatch command for a given MAPDL launch command."""

    def add_minus(arg: str):
        if not arg:
            return ""

        arg = str(arg)

        if not arg.startswith("-"):
            if len(arg) == 1:
                arg = f"-{arg}"
            else:
                arg = f"--{arg}"
        elif not arg.startswith("--") and len(arg) > 2:
            # missing one "-" for a long argument
            arg = f"-{arg}"

        return arg

    if scheduler_options:
        if isinstance(scheduler_options, dict):
            scheduler_options = " ".join(
                [
                    f"{add_minus(key)}='{value}'"
                    for key, value in scheduler_options.items()
                ]
            )
    else:
        scheduler_options = ""

    if "wrap" in scheduler_options:
        raise ValueError(
            "The sbatch argument 'wrap' is used by PyMAPDL to submit the job."
            "Hence you cannot use it as sbatch argument."
        )
    LOG.debug(f"The additional sbatch arguments are: {scheduler_options}")

    if isinstance(cmd, list):
        cmd = " ".join(cmd)

    cmd = ["sbatch", scheduler_options, "--wrap", f"'{cmd}'"]
    cmd = [each for each in cmd if bool(each)]
    return cmd


def get_hostname_from_scontrol(stdout: str) -> str:
    return stdout.split("BatchHost=")[1].splitlines()[0].strip()


def get_state_from_scontrol(stdout: str) -> str:
    return stdout.split("JobState=")[1].splitlines()[0].strip()


def launch_mapdl_on_cluster(
    nproc: int,
    *,
    scheduler_options: Union[str, Dict[str, str]] = None,
    **launch_mapdl_args: Dict[str, Any],
) -> MapdlGrpc:
    """Launch MAPDL on a HPC cluster

    Launches an interactive MAPDL instance on an HPC cluster.

    Parameters
    ----------
    nproc : int
        Number of CPUs to be used in the simulation.

    scheduler_options : Dict[str, str], optional
        A string or dictionary specifying the job configuration for the
        scheduler. For example ``scheduler_options = "-N 10"``.

    Returns
    -------
    MapdlGrpc
        Mapdl instance running on the HPC cluster.

    Examples
    --------
    Run a job with 10 nodes and 2 tasks per node:

    >>> from ansys.mapdl.core import launch_mapdl
    >>> scheduler_options = {"nodes": 10, "ntasks-per-node": 2}
    >>> mapdl = launch_mapdl(
            launch_on_hpc=True,
            nproc=20,
            scheduler_options=scheduler_options
            )

    """
    from ansys.mapdl.core.launcher import launch_mapdl

    # Processing the arguments
    launch_mapdl_args["launch_on_hpc"] = True

    if launch_mapdl_args.get("mode", "grpc") != "grpc":
        raise ValueError(
            "The only mode allowed for launch MAPDL on an HPC cluster is gRPC."
        )

    if launch_mapdl_args.get("ip"):
        raise ValueError(LAUNCH_ON_HCP_ERROR_MESSAGE_IP)

    if not launch_mapdl_args.get("start_instance", True):
        raise ValueError(
            "The 'start_instance' argument must be 'True' when launching on HPC."
        )

    return launch_mapdl(
        nproc=nproc,
        scheduler_options=scheduler_options,
        **launch_mapdl_args,
    )


def launch_mapdl_grpc():
    args = processing_local_arguments(locals())
    if args.get("mode", "grpc") != "grpc":
        raise ValueError("Invalid 'mode'.")
    args["port"] = get_port(args["port"], args["start_instance"])

    start_parm = generate_start_parameters(args)

    # Early exit for debugging.
    if args["_debug_no_launch"]:
        # Early exit, just for testing
        return args  # type: ignore

    # Check the license server
    if args["license_server_check"]:
        LOG.debug("Checking license server.")
        lic_check = LicenseChecker(timeout=args["start_timeout"])
        lic_check.start()

    ########################################
    # Launch MAPDL with gRPC
    # ----------------------
    #
    cmd = generate_mapdl_launch_command(
        exec_file=args["exec_file"],
        jobname=args["jobname"],
        nproc=args["nproc"],
        ram=args["ram"],
        port=args["port"],
        additional_switches=args["additional_switches"],
    )

    # wrapping command if on HPC
    cmd = generate_sbatch_command(cmd, scheduler_options=args.get("scheduler_options"))

    try:
        #
        process = launch_grpc(
            cmd=cmd,
            run_location=args["run_location"],
            env_vars=env_vars,
            launch_on_hpc=args.get("launch_on_hpc"),
            mapdl_output=args.get("mapdl_output"),
        )

        start_parm["jobid"] = check_mapdl_launch_on_hpc(process, start_parm)
        get_job_info(start_parm=start_parm, timeout=args["start_timeout"])

    except Exception as exception:
        LOG.error("An error occurred when launching MAPDL.")

        jobid: int = start_parm.get("jobid", "Not found")

        if (
            args["launch_on_hpc"]
            and start_parm.get("finish_job_on_exit", True)
            and jobid not in ["Not found", None]
        ):

            LOG.debug(f"Killing HPC job with id: {jobid}")
            kill_job(jobid)

        if args["license_server_check"]:
            LOG.debug("Checking license server.")
            lic_check.check()

        raise exception

    if args["just_launch"]:
        out = [args["ip"], args["port"]]
        if hasattr(process, "pid"):
            out += [process.pid]
        return out

    ########################################
    # Connect to MAPDL using gRPC
    # ---------------------------
    #
    try:
        mapdl = MapdlGrpc(
            cleanup_on_exit=args["cleanup_on_exit"],
            loglevel=args["loglevel"],
            set_no_abort=args["set_no_abort"],
            remove_temp_dir_on_exit=args["remove_temp_dir_on_exit"],
            log_apdl=args["log_apdl"],
            process=process,
            use_vtk=args["use_vtk"],
            **start_parm,
        )

    except Exception as exception:
        LOG.error("An error occurred when connecting to MAPDL.")
        raise exception

    return mapdl


def get_slurm_options(
    args: Dict[str, Any],
    kwargs: Dict[str, Any],
) -> Dict[str, Any]:
    def get_value(
        variable: str,
        kwargs: Dict[str, Any],
        default: Optional[Union[str, int, float]] = 1,
        astype: Optional[Callable[[Any], Any]] = int,
    ):
        value_from_env_vars = os.environ.get(variable)
        value_from_kwargs = kwargs.pop(variable, None)
        value = value_from_kwargs or value_from_env_vars or default
        if astype and value:
            return astype(value)
        else:
            return value

    ## Getting env vars
    SLURM_NNODES = get_value("SLURM_NNODES", kwargs)
    LOG.info(f"SLURM_NNODES: {SLURM_NNODES}")
    # ntasks is for mpi
    SLURM_NTASKS = get_value("SLURM_NTASKS", kwargs)
    LOG.info(f"SLURM_NTASKS: {SLURM_NTASKS}")
    # Sharing tasks across multiple nodes (DMP)
    # the format of this envvar is a bit tricky. Avoiding it for the moment.
    # SLURM_TASKS_PER_NODE = int(
    #     kwargs.pop(
    #         "SLURM_TASKS_PER_NODE", os.environ.get("SLURM_TASKS_PER_NODE", 1)
    #     )
    # )

    # cpus-per-task is for multithreading,
    # sharing tasks across multiple CPUs in same node (SMP)
    SLURM_CPUS_PER_TASK = get_value("SLURM_CPUS_PER_TASK", kwargs)
    LOG.info(f"SLURM_CPUS_PER_TASK: {SLURM_CPUS_PER_TASK}")

    # Set to value of the --ntasks option, if specified. See SLURM_NTASKS.
    # Included for backwards compatibility.
    SLURM_NPROCS = get_value("SLURM_NPROCS", kwargs)
    LOG.info(f"SLURM_NPROCS: {SLURM_NPROCS}")

    # Number of CPUs allocated to the batch step.
    SLURM_CPUS_ON_NODE = get_value("SLURM_CPUS_ON_NODE", kwargs)
    LOG.info(f"SLURM_CPUS_ON_NODE: {SLURM_CPUS_ON_NODE}")

    SLURM_MEM_PER_NODE = get_value(
        "SLURM_MEM_PER_NODE", kwargs, default="", astype=str
    ).upper()
    LOG.info(f"SLURM_MEM_PER_NODE: {SLURM_MEM_PER_NODE}")

    SLURM_NODELIST = get_value(
        "SLURM_NODELIST", kwargs, default="", astype=None
    ).lower()
    LOG.info(f"SLURM_NODELIST: {SLURM_NODELIST}")

    if not args["exec_file"]:
        args["exec_file"] = os.environ.get("PYMAPDL_MAPDL_EXEC")

    if not args["exec_file"]:
        # We should probably make a way to find it.
        # We will use the module thing
        pass
    LOG.info(f"Using MAPDL executable in: {args['exec_file']}")

    if not args["jobname"]:
        args["jobname"] = os.environ.get("SLURM_JOB_NAME", "file")
    LOG.info(f"Using jobname: {args['jobname']}")

    # Checking specific env var
    if not args["nproc"]:
        ## Attempt to calculate the appropriate number of cores:
        # Reference: https://stackoverflow.com/a/51141287/6650211
        # I'm assuming the env var makes sense.
        #
        # - SLURM_CPUS_ON_NODE is a property of the cluster, not of the job.
        #
        options = max(
            [
                # 4,  # Fall back option
                SLURM_CPUS_PER_TASK * SLURM_NTASKS,  # (CPUs)
                SLURM_NPROCS,  # (CPUs)
                # SLURM_NTASKS,  # (tasks) Not necessary the number of CPUs,
                # SLURM_NNODES * SLURM_TASKS_PER_NODE * SLURM_CPUS_PER_TASK,  # (CPUs)
                SLURM_CPUS_ON_NODE * SLURM_NNODES,  # (cpus)
            ]
        )
        LOG.info(f"On SLURM number of processors options {options}")

        args["nproc"] = int(os.environ.get("PYMAPDL_NPROC", options))

    LOG.info(f"Setting number of CPUs to: {args['nproc']}")

    if not args["ram"]:
        if SLURM_MEM_PER_NODE:
            # RAM argument is in MB, so we need to convert
            units = None
            if SLURM_MEM_PER_NODE[-1].isalpha():
                units = SLURM_MEM_PER_NODE[-1]
                ram = SLURM_MEM_PER_NODE[:-1]
            else:
                units = None
                ram = SLURM_MEM_PER_NODE

            if not units:
                args["ram"] = int(ram)
            elif units == "T":  # tera
                args["ram"] = int(ram) * (2**10) ** 2
            elif units == "G":  # giga
                args["ram"] = int(ram) * (2**10) ** 1
            elif units == "M":  # mega
                args["ram"] = int(ram)
            elif units == "K":  # kilo
                args["ram"] = int(ram) * (2**10) ** (-1)
            else:  # Mega
                raise ValueError(
                    "The memory defined in 'SLURM_MEM_PER_NODE' env var("
                    f"'{SLURM_MEM_PER_NODE}') is not valid."
                )

    LOG.info(f"Setting RAM to: {args['ram']}")

    # We use "-dis " (with space) to avoid collision with user variables such
    # as `-distro` or so
    if "-dis " not in args["additional_switches"] and not args[
        "additional_switches"
    ].endswith("-dis"):
        args["additional_switches"] += " -dis"

    # Finally set to avoid timeouts
    args["license_server_check"] = False
    args["start_timeout"] = 2 * args["start_timeout"]

    return args
