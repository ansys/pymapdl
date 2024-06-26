# Copyright (C) 2024 ANSYS, Inc. and/or its affiliates.
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

"""Submit PyHPS jobs to a cluster"""

import logging
import os
from typing import Optional, Union

import click

logger = logging.getLogger()


@click.command(
    short_help="Submit jobs to an HPC cluster using PyHPS.",
    help="""
    Submit jobs to an HPC cluster using PyHPS.


Example

$ pymapdl submit my_file_01.py --requirements_file=requirements.txt --shell_file=main.sh --name="my job" --user=user --password=password --url="https://123.456.789.101:3000/hps"
""",
)
@click.argument("main_file")
@click.option(
    "--name",
    default=None,
    type=str,
    help="""Name of the PyHPS project to create.""",
)
@click.option(
    "--url",
    default=None,
    type=str,
    help="""URL where the HPS cluster is deployed. For example: "https://myserver:3000/hps".
If it is not input, there is a chain of places where PyMAPDL looks for an URL.
First, it checks if the URL is given in the file specified by the argument ``--config_file``.
If that file does not have an URL or does not exist, then it checks the default user credentials stored with ``pymapdl login --default`` CLI command.
If no URL is found, an exception is raised.""",
)
@click.option(
    "--user",
    default=None,
    type=str,
    help="""Username for logging into the HPC cluster.
If it is not input, there is a chain of places where PyMAPDL looks for an username.
First, it checks if the username is given in the file specified by the argument ``--config_file``.
If that file does not have an username or does not exist, then it checks the username configured using ``pymapdl login`` CLI command, for the given HPS cluster URL.
If there is no user credential stored for that HPS cluster URL, then it checks the default user credentials stored with ``pymapdl login --default`` CLI command.
If no user is found, an exception is raised.
""",
)
@click.option(
    "--password",
    default=None,
    type=str,
    help="""Password for logging into the HPC cluster.
If it is not input, there is a chain of places where PyMAPDL looks for a password.
First, it checks if the password is given in the file specified by the argument ``--config_file``.
If that file does not have a password or does not exist, then it checks the password configured using ``pymapdl login`` CLI command, for the given HPS cluster URL.
If there is no user credential stored for that HPS cluster URL, then it checks the default user credentials stored with ``pymapdl login --default`` CLI command.
If no password is found, an exception is raised.
""",
)
@click.option(
    "--python",
    default=None,
    type=float,
    help="""Python version to use to create the virtual environment and
run the Python file. Python3 is used by default in the cluster.""",
)
@click.option(
    "--inputs",
    default=None,
    type=str,
    help="""
Input arguments for the simulation. Because you can specify several arguments by
joining them with commas, strings defined in this way cannot contain
commas. Only integers, floats, and strings are allowed.
PyMAPDL converts these inputs to integer or float values when possible.
Otherwise, they remain as strings. You can change these arguments on the
HPS website. For example, ``--inputs="force=123,value='mystring'"``.
    """,
)
@click.option(
    "--outputs",
    default=None,
    type=str,
    help="""Output parameters. You can specify several arguments
by joining them with commas.
For example, ``--outputs="displacements,nodes"``.""",
)
@click.option(
    "--output_files",
    default=None,
    type=str,
    help="""Output files to monitor. Because you use commas to separate
filenames, the names cannot contain commas. For example,
``--output_files="results.out,data.xls"``.""",
)
@click.option(
    "--shell_file",
    default=None,
    type=str,
    help="""Optional shell script to execute instead of
the Python file. You can call your Python file from it if you want. By default,
this option is not used.""",
)
@click.option(
    "--requirements_file",
    default=None,
    type=str,
    help="""Optional created virtual environment to install with the
libraries specified in this requirements file. If not, the activated virtual environment is
cloned through a temporary ``pip list`` file. If you are using an editable package,
you should attach your own requirement file using ``pip freeze``.""",
)
@click.option(
    "--extra_files",
    default=None,
    type=str,
    help="""Extra files to upload that can be called from your main Python file
(or from the shell file).""",
)
@click.option(
    "--config_file",
    default=None,
    type=str,
    help="""File to load the job configuration from.""",
)
@click.option(
    "--save_config_file",
    default=False,
    type=bool,
    is_flag=False,
    flag_value=True,
    help="""
Whether to write the configuration to the configuration file (specified
using the ``config_file`` argument) after the job has been successfully submitted.
The default is ``False``. If ``True``, and the file already exists, the configuration file is overwritten.""",
)
@click.option(
    "--num_cores",
    default=None,
    type=str,
    help="""Number of CPU cores reserved for the job. The default is ``1``""",
)
@click.option(
    "--memory",
    default=None,
    type=str,
    help="""Amount of memory (RAM) in MB reserved for the job. The default is ``100 MB``.""",
)
@click.option(
    "--disk_space",
    default=None,
    type=str,
    help="""Amount of hard drive space in MB reserved for the job. The default is ``100 MB``.""",
)
@click.option(
    "--exclusive",
    default=None,
    type=str,
    is_flag=False,
    flag_value=True,
    help="""Whether the job is to run on a machine that is running no other jobs running. The default is ``False``.""",
)
@click.option(
    "--max_execution_time",
    default=None,
    type=int,
    help="""Maximum execution time for the job. The default is zero (unlimited).""",
)
@click.option(
    "--wait",
    default=None,
    type=str,
    is_flag=False,
    flag_value=True,
    help="""Whether the terminal is to wait for job completion before returning control to the user. """,
)
@click.option(
    "--mode",
    default=None,
    type=str,
    help="""
Force the job submission to behave as if the main file was a Python,
shell, or APDL file, regardless of its extension type. Allowed values are
``"python"``, ``"shell"``, and ``"apdl"``.
By default, PyMAPDL detects the type of file from its extension.
""",
)
@click.option(
    "--to_json",
    default=None,
    type=str,
    is_flag=False,
    flag_value=True,
    help="""Print the output values to the terminal as json. It automatically set ``--wait`` to ``True``.""",
)
@click.option(
    "--debug",
    default=False,
    type=bool,
    is_flag=False,
    flag_value=True,
    help="""Whether PyMAPDL is to print debug logging to the console.""",
)
def submit(
    main_file: str,
    name: str = None,
    url: str = None,
    user: str = None,
    password: str = None,
    python: Optional[float] = None,
    inputs: Optional[str] = None,
    outputs: Optional[str] = None,
    output_files: Optional[Union[str, list]] = None,
    shell_file: str = None,
    requirements_file: str = None,
    extra_files: Optional[Union[str, list]] = None,
    config_file: str = None,
    save_config_file: bool = False,
    num_cores: int = None,
    memory: int = None,
    disk_space: int = None,
    exclusive: bool = None,
    max_execution_time: int = None,
    wait: bool = False,
    debug: bool = False,
    mode: Optional[Union["python", "shell", "apdl"]] = None,
    to_json: Optional[bool] = False,
):
    from ansys.mapdl.core.hpc.login import access, get_default_url

    if to_json:
        import json

        wait = True

    from ansys.mapdl.core.hpc.pyhps import (
        PyMAPDLJobSubmission,
        get_value_from_json_or_default,
    )

    if debug:
        logging.basicConfig(
            format="[%(asctime)s | %(levelname)s] %(message)s", level=logging.DEBUG
        )

    if config_file is None:
        config_file = os.path.join(os.getcwd(), "hps_config.json")
        if not os.path.exists(config_file):
            config_file = None
        logger.debug(f"Using default HPS configuration file: {config_file}")

    # Getting cluster login configuration from CLI or file
    url = get_value_from_json_or_default(
        url, config_file, "url", None, raise_if_none=False
    )
    url = url or get_default_url()  # using default URL stored.

    # allow retrieving user from the configuration
    user = get_value_from_json_or_default(
        user, config_file, "user", raise_if_none=False
    )

    # Getting access token
    token = access(url, user, password)

    # Getting other configuration from CLI or file
    python = get_value_from_json_or_default(python, config_file, "python", 3)
    name = get_value_from_json_or_default(name, config_file, "name", "My PyMAPDL job")

    num_cores = get_value_from_json_or_default(num_cores, config_file, "num_cores", 1)
    memory = get_value_from_json_or_default(memory, config_file, "memory", 100)
    disk_space = get_value_from_json_or_default(
        disk_space, config_file, "disk_space", 100
    )
    exclusive = get_value_from_json_or_default(
        exclusive, config_file, "exclusive", False
    )
    max_execution_time = get_value_from_json_or_default(
        max_execution_time, config_file, "max_execution_time", 0
    )

    job = PyMAPDLJobSubmission(
        url=url,
        token=token,
        main_file=main_file,
        mode=mode,
        inputs=inputs,
        outputs=outputs,
        requirements_file=requirements_file,
        shell_file=shell_file,
        extra_files=extra_files,
        output_files=output_files,
        python=python,
        num_cores=num_cores,
        memory=memory,
        disk_space=disk_space,
        exclusive=exclusive,
        max_execution_time=max_execution_time,
        name=name,
    )

    job.submit()

    if save_config_file:
        config = {
            "url": url,
            "user": user,
            "password": password,
            "python": python,
            "name": name,
            "num_cores": num_cores,
            "memory": memory,
            "disk_space": disk_space,
            "exclusive": exclusive,
            "max_execution_time": max_execution_time,
        }

        logger.debug(
            f"Saving the following configuration to the config file ({config_file}):\n{config}."
        )
        with open(config_file, "w") as fid:
            json.dump(config, fid)

    proj = job.project
    if not to_json:
        print(
            f"You can check your project by visiting: {url}/projects#/projects/{proj.id}/jobs"
        )

    if wait:
        if not to_json:
            print(
                f"Waiting for project {name} (id: {proj.id}) evaluation to complete..."
            )
        job.wait_for_completion(evaluated=True, failed=True)

    if to_json:
        if len(job.outputs) == 1:
            print(job.output_values[0][job.outputs[0]])
        else:
            print(json.dumps(job.output_values))


def list_jobs():
    pass


def stop_job():
    pass
