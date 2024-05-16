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

"""PyHPS interface to HPC clusters"""
import json
import logging
import os
import time
from typing import Any, Optional, Union
from warnings import warn

from ansys.hps.client import Client
from ansys.hps.client.jms import (
    File,
    HpcResources,
    JmsApi,
    Job,
    JobDefinition,
    Project,
    ProjectApi,
    ResourceRequirements,
    Software,
    TaskDefinition,
)

logger = logging.getLogger()


def get_value_from_json_or_default(
    arg: str, json_file: str, key: str, default_value: Optional[Union[str, Any]] = None
):
    if arg is not None:
        logger.debug(f"Using '{arg}' for {key}")
        return arg

    if os.path.exists(json_file):
        if os.path.getsize(json_file) > 0:
            with open(json_file, "r") as fid:
                config = json.load(fid)

            if key in config:
                logger.debug(f"Using '{config[key]}' for {key}")
                return config[key]

    if default_value is None:
        raise ValueError(
            f"The argument {arg} is not given through the CLI or config file."
        )

    logger.debug(f"Using '{default_value}' for {key}")
    return default_value


def create_project(
    client,
    name="My PyMAPDL job",
) -> Project:
    jms_api = JmsApi(client)

    proj = Project(name=name, priority=1, active=True)
    return jms_api.create_project(proj)


def add_files(project_api: ProjectApi, input_files: list, output_files: list):

    # Checks:
    if not all([os.path.exists(each) for each in input_files]):
        raise ValueError("One or more input files do not exist.")

    input_files_ = [os.path.basename(each) for each in input_files]

    input_files = [
        File(
            name=os.path.basename(each_file),
            evaluation_path=os.path.basename(each_file),
            type="text/plain",
            src=each_file,
        )
        for each_file in input_files
    ]

    output_files = [
        File(
            name=os.path.basename(each_file),
            evaluation_path=os.path.basename(each_file),
            type="text/plain",
            collect=True,
            monitor=True,
        )
        for each_file in output_files
    ]

    files = input_files + output_files

    for each in files:
        logger.debug(each)

    files = project_api.create_files(files)

    f_inp = {}
    f_out = {}
    for f in files:
        if f.name in input_files_:
            f_inp[f.name] = f.id
        else:
            f_out[f.name] = f.id

    logger.debug(f"Input files IDs: {f_inp}")
    logger.debug(f"Output files IDs: {f_out}")
    return f_inp, f_out


def create_input_parameters(project_api, input_params=None):
    if input_params is not None:
        raise NotImplementedError("'Input_parameters' is not implemented.")
    else:
        input_params = []
        logger.debug("Setting empty input parameters.")
    return project_api.create_parameter_definitions(input_params)


def create_output_parameters(project_api, output_params=None):
    if output_params is not None:
        raise NotImplementedError("'Output_parameters' is not implemented.")
    else:
        output_params = []
        logger.debug("Setting empty output parameters.")
    return project_api.create_parameter_definitions(output_params)


def create_param_mappings(project_api, param_mappings=None):
    if param_mappings is not None:
        raise NotImplementedError("'param_mappings' is not implemented.")
    else:
        param_mappings = []
        logger.debug("Setting empty parameter mappings.")
    return project_api.create_parameter_mappings(param_mappings)


def create_task(
    project_api,
    main_file,
    file_input_ids,
    file_output_ids,
    num_cores,
    memory,
    disk_space,
    exclusive,
    max_execution_time,
):

    software = Software(name="Bash", version="0.1")  # Overwriting
    execution_command = f"%executable% %file:{os.path.basename(main_file)}%"
    logger.debug(f"Using executable: '{execution_command}'")

    # Process step
    task_def = TaskDefinition(
        name="PyMAPDL_task",
        software_requirements=[software],
        execution_command=execution_command,
        resource_requirements=ResourceRequirements(
            num_cores=int(num_cores),
            memory=int(memory) * 1024 * 1024,
            disk_space=int(disk_space) * 1024 * 1024,
            # distributed=True,
            hpc_resources=HpcResources(exclusive=exclusive),
        ),
        max_execution_time=max_execution_time,
        execution_level=0,
        num_trials=1,
        input_file_ids=list(file_input_ids.values()),
        output_file_ids=list(file_output_ids.values()),
    )
    logger.debug(f"Task definition: {task_def}")

    return project_api.create_task_definitions([task_def])[0]


def create_job_definition(
    project_api,
    task_def,
    input_params,
    output_params,
    param_mappings,
):
    job_def = JobDefinition(name="JobDefinition.1", active=True)
    params = input_params + output_params

    job_def.task_definition_ids = [task_def.id]
    job_def.parameter_definition_ids = [pd.id for pd in params]
    job_def.parameter_mapping_ids = [pm.id for pm in param_mappings]

    logger.debug(f"Job definition: {job_def}")
    job_def = project_api.create_job_definitions([job_def])[0]

    # Refresh the parameters
    params = project_api.get_parameter_definitions(id=job_def.parameter_definition_ids)
    return job_def


def create_jobs(project_api, job_def):
    jobs = [
        Job(name="Job", values={}, eval_status="pending", job_definition_id=job_def.id)
    ]
    logger.debug(f"jobs: {jobs}")
    return project_api.create_jobs(jobs)


def get_project_api(client, proj):
    return ProjectApi(client, proj.id)


def wait_for_completion(project_api, evaluated=True, failed=False, running=False):
    eval_status = []

    if evaluated:
        eval_status.append("evaluated")

    if failed:
        eval_status.append("evaluated")

    if running:
        eval_status.append("running")

    logger.debug(f"Waiting on project {proj.id} with criteria: {eval_status}")
    while not project_api.get_jobs(eval_status=eval_status):
        time.sleep(2)


def _create_tmp_file(file_name, content):
    import tempfile
    import uuid

    dir_ = tempfile.gettempdir()
    sub_dir = str(uuid.uuid4())

    tmp_file = os.path.join(dir_, sub_dir, file_name)
    os.makedirs(os.path.join(dir_, sub_dir))

    with open(tmp_file, "w") as fid:
        fid.write(content)

    return tmp_file


def create_pymapdl_pyhps_job(
    main_file: str,
    name: str = None,
    url: str = None,
    user: str = None,
    password: str = None,
    python: float = None,
    output_files: Optional[Union[str, list]] = None,
    shell_file: str = None,
    requirements_file: str = None,
    extra_files: Optional[Union[str, list]] = None,
    config_file: str = None,
    num_cores: int = None,
    memory: int = None,
    disk_space: int = None,
    exclusive: bool = None,
    max_execution_time: int = None,
):

    if python not in [2.7, 3.5, 3.6, 3.7, 3.8, 3.9, 3.10, 3.11, 3.12]:
        warn("Version of Python might not be supported by the cluster.")

    if not os.path.exists(main_file):
        raise ValueError(f"The Python file {main_file} must exist.")

    logger.debug(f"Main Python file is in: {main_file}.")

    if not requirements_file:
        import pkg_resources

        content = "\n".join(
            [str(p.as_requirement()) for p in pkg_resources.working_set]
        )
        requirements_file = _create_tmp_file("requirements.txt", content)
        logger.debug(f"Requirements file in: {requirements_file}")

    if not shell_file:
        content = f"""
echo "Starting"

# Start venv
python{python} -m venv .venv
source .venv/bin/activate

# Install requirements
pip install -r {os.path.basename(requirements_file)}

# Run script
python {os.path.basename(main_file)}
    """

        shell_file = _create_tmp_file("main.sh", content)
        logger.debug(f"Shell file in: {shell_file}")

    if isinstance(extra_files, str):
        extra_files = extra_files.split(",")
    elif extra_files is None:
        extra_files = []

    if extra_files and not all([os.path.exists(each) for each in extra_files]):
        raise ValueError("One or more extra files does not exist.")

    input_files = extra_files
    input_files.append(requirements_file)
    input_files.append(shell_file)
    input_files.append(main_file)

    if not output_files:
        output_files = []
    elif isinstance(output_files, str):
        output_files = output_files.split(",")

    # Log in
    client = Client(url=url, username=user, password=password)

    # Setting project
    proj = create_project(client, name)
    project_api = get_project_api(client, proj)

    # Setting files
    file_input_ids, file_output_ids = add_files(project_api, input_files, output_files)

    # Set parameters
    input_params = create_input_parameters(project_api)
    output_params = create_output_parameters(project_api)
    param_mappings = create_param_mappings(project_api)

    # Set tasks
    task_def = create_task(
        project_api,
        shell_file,
        file_input_ids,
        file_output_ids,
        num_cores,
        memory,
        disk_space,
        exclusive,
        max_execution_time,
    )

    # Set jobs
    job_def = create_job_definition(
        project_api, task_def, input_params, output_params, param_mappings
    )
    jobs = create_jobs(project_api, job_def)
    logger.debug(f"Jobs: {jobs}")
    logger.debug("Project submitted.")

    return proj, project_api
