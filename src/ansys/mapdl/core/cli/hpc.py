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

from ansys.mapdl.core.cli import main

logger = logging.getLogger()


@main.command(
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
    help="""URL where the HPS cluster is deployed. For example: "https://myserver:3000/hps" """,
)
@click.option(
    "--user", default=None, type=str, help="Username to login into the HPC cluster."
)
@click.option(
    "--password",
    default=None,
    type=str,
    help="Password for logging into the HPC cluster.",
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
    Input arguments for the simulation. You can specify several arguments by joining them with commas, therefore, strings defined this way cannot contain commas.
    PyMAPDL will try to convert, whenever possible, these inputs to ints or floats, otherwise, they remind as strings. These arguments can be changed in the HPS website. For example: --inputs="force=123,value='mystring'"
    """,
)
@click.option(
    "--outputs",
    default=None,
    type=str,
    help="""Output parameters. You can specify several arguments by joining them with commas. For example: --outputs="displacements,nodes".""",
)
@click.option(
    "--output_files",
    default=None,
    type=str,
    help="""Output files to monitor. They can be specified as comma separated file names (so their names cannot contain commas). For example: --output_files="results.out,data.xls". """,
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
you should attach your own requirement file using ``pip freeze`` """,
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
Whether to write the configuration to the configuration file (specified using ``config_file`` argument) after the job has been successfully submitted.
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
    "--save_config_file",
    default=False,
    type=bool,
    is_flag=False,
    flag_value=True,
    help="""Whether to write the configuration to the configuration file after successfully
submitting the job. The default is ``False``. If ``True``, the configuration file is overwritten.
You use the ``config_file`` argument to give the path for the configuration file.""",
)
@click.option(
    "--mode",
    default=None,
    type=str,
    help="""
Force the job submission to behave as if the main file was a python,
shell or APDL file, regardless of its extension type. Allowed values are: "python", "shell", and "apdl".
By default, PyMAPDL detects the type of file from its extension.
""",
)
@click.option(
    "--debug",
    default=False,
    type=bool,
    is_flag=False,
    flag_value=True,
    help="""Whether PyMAPDL is to print debug logging to the console output.""",
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
):
    import json

    from ansys.mapdl.core.hpc.pyhps import (
        create_pymapdl_pyhps_job,
        get_value_from_json_or_default,
        wait_for_completion,
    )

    if debug:
        logging.basicConfig(
            format="[%(asctime)s | %(levelname)s] %(message)s", level=logging.DEBUG
        )

    if config_file is None:
        config_file = os.path.join(os.getcwd(), "hps_config.json")
        logger.debug(f"Using default HPS configuration file: {config_file}")

    url = get_value_from_json_or_default(url, config_file, "url", None)
    user = get_value_from_json_or_default(user, config_file, "user", None)
    password = get_value_from_json_or_default(password, config_file, "password", None)
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

    proj, _ = create_pymapdl_pyhps_job(
        main_file=main_file,
        name=name,
        url=url,
        user=user,
        password=password,
        python=python,
        inputs=inputs,
        outputs=outputs,
        output_files=output_files,
        shell_file=shell_file,
        requirements_file=requirements_file,
        extra_files=extra_files,
        config_file=config_file,
        num_cores=num_cores,
        memory=memory,
        disk_space=disk_space,
        exclusive=exclusive,
        max_execution_time=max_execution_time,
        mode=mode,
    )

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
            f"Saving the following configuration to the config file ({config_file}):\n{config}"
        )
        with open(config_file, "w") as fid:
            json.dump(config, fid)

    print(
        f"You can check your project by visiting: {url}/projects#/projects/{proj.id}/jobs"
    )

    if wait:
        print(f"Waiting for project {name} (id: {proj.id}) evaluation to complete...")
        wait_for_completion(proj, evaluated=True, failed=True)


def list_jobs():
    pass


def stop_job():
    pass
