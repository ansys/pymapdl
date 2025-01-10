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

# Subprocess is needed to start the backend. But
# the input is controlled by the library. Excluding bandit check.
import subprocess  # nosec B404
from typing import Dict, Optional

from ansys.mapdl.core import LOG
from ansys.mapdl.core.launcher.local import processing_local_arguments
from ansys.mapdl.core.launcher.tools import (
    generate_start_parameters,
    get_port,
    submitter,
)
from ansys.mapdl.core.licensing import LicenseChecker
from ansys.mapdl.core.mapdl_grpc import MapdlGrpc


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

        try:
            #
            process = launch_grpc(
                cmd=cmd,
                run_location=args["run_location"],
                env_vars=env_vars,
                launch_on_hpc=args.get("launch_on_hpc"),
                mapdl_output=args.get("mapdl_output"),
            )

            # Local mapdl launch check
            check_mapdl_launch(
                process, args["run_location"], args["start_timeout"], cmd
            )

        except Exception as exception:
            LOG.error("An error occurred when launching MAPDL.")

            jobid: int = start_parm.get("jobid", "Not found")

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


def launch_grpc(
    cmd: list[str],
    run_location: str = None,
    env_vars: Optional[Dict[str, str]] = None,
    launch_on_hpc: bool = False,
    mapdl_output: Optional[str] = None,
) -> subprocess.Popen:
    """Start MAPDL locally in gRPC mode.

    Parameters
    ----------
    cmd : str
        Command to use to launch the MAPDL instance.

    run_location : str, optional
        MAPDL working directory.  The default is the temporary working
        directory.

    env_vars : dict, optional
        Dictionary with the environment variables to inject in the process.

    launch_on_hpc : bool, optional
        If running on an HPC, this needs to be :class:`True` to avoid the
        temporary file creation on Windows.

    mapdl_output : str, optional
        Whether redirect MAPDL console output (stdout and stderr) to a file.

    Returns
    -------
    subprocess.Popen
        Process object
    """
    if env_vars is None:
        env_vars = {}

    # disable all MAPDL pop-up errors:
    env_vars.setdefault("ANS_CMD_NODIAG", "TRUE")

    cmd_string = " ".join(cmd)
    if "sbatch" in cmd:
        header = "Running an MAPDL instance on the Cluster:"
        shell = os.name != "nt"
        cmd_ = cmd_string
    else:
        header = "Running an MAPDL instance"
        shell = False  # To prevent shell injection
        cmd_ = cmd

    LOG.info(
        "\n============"
        "\n============\n"
        f"{header}\nLocation:\n{run_location}\n"
        f"Command:\n{cmd_string}\n"
        f"Env vars:\n{env_vars}"
        "\n============"
        "\n============"
    )

    if mapdl_output:
        stdout = open(str(mapdl_output), "wb", 0)
        stderr = subprocess.STDOUT
    else:
        stdout = subprocess.PIPE
        stderr = subprocess.PIPE

    if os.name == "nt":
        # getting tmp file name
        if not launch_on_hpc:
            # if we are running on an HPC cluster (case not considered), we will
            # have to upload/create this file because it is needed for starting.
            tmp_inp = cmd[cmd.index("-i") + 1]
            with open(os.path.join(run_location, tmp_inp), "w") as f:
                f.write("FINISH\r\n")
                LOG.debug(
                    f"Writing temporary input file: {tmp_inp} with 'FINISH' command."
                )

    LOG.debug("MAPDL starting in background.")
    return submitter(
        cmd_,
        shell=shell,  # sbatch does not work without shell.
        cwd=run_location,
        stdin=subprocess.DEVNULL,
        stdout=stdout,
        stderr=stderr,
        env_vars=env_vars,
    )
