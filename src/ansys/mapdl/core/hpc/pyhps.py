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
    FloatParameterDefinition,
    HpcResources,
    JmsApi,
    Job,
    JobDefinition,
    ParameterMapping,
    Project,
    ProjectApi,
    ResourceRequirements,
    Software,
    StringParameterDefinition,
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


class PythonTask(TaskDefinition):
    def __init__(self, *args, **kwargs):
        # Get the names of the parameters of the TaskDefinition __init__ method
        param_names = list(
            TaskDefinition.__init__.__code__.co_varnames[
                1 : TaskDefinition.__init__.__code__.co_argcount
            ]
        )

        # Convert positional arguments to keyword arguments
        for i, arg in enumerate(args):
            kwargs[param_names[i]] = arg

        kwargs["name"] = "Python Task"
        kwargs["software"] = [Software(name="Bash", version="0.1")]

        # Call the parent constructor with the updated kwargs
        super().__init__(**kwargs)


class APDLTask(TaskDefinition):
    def __init__(self, *args, **kwargs):
        # Get the names of the parameters of the TaskDefinition __init__ method
        param_names = list(
            TaskDefinition.__init__.__code__.co_varnames[
                1 : TaskDefinition.__init__.__code__.co_argcount
            ]
        )

        # Convert positional arguments to keyword arguments
        for i, arg in enumerate(args):
            kwargs[param_names[i]] = arg

        kwargs["name"] = "APDL Task"
        kwargs["software"] = [Software(name="Ansys Mechanical APDL", version="2024 R2")]

        # Call the parent constructor with the updated kwargs
        super().__init__(**kwargs)


class ShellTask(TaskDefinition):
    def __init__(self, *args, **kwargs):
        # Get the names of the parameters of the TaskDefinition __init__ method
        param_names = list(
            TaskDefinition.__init__.__code__.co_varnames[
                1 : TaskDefinition.__init__.__code__.co_argcount
            ]
        )

        # Convert positional arguments to keyword arguments
        for i, arg in enumerate(args):
            kwargs[param_names[i]] = arg

        kwargs["name"] = "Shell Task"
        kwargs["software"] = [Software(name="Bash", version="0.1")]

        # Call the parent constructor with the updated kwargs
        super().__init__(**kwargs)


class JobSubmission:

    def __init__(
        self,
        url,
        user,
        password,
        main_file,
        mode: Optional[str] = None,
        inputs: Optional[Union[List[str]]] = None,
        outputs: Optional[Union[List[str]]] = None,
        requirements_file: Optional[str] = None,
        shell_file: Optional[str] = None,
        extra_files: Optional[Union[List[str]]] = None,
        output_files: Optional[Union[List[str]]] = None,
        python: Optional[float] = None,
        num_cores: Optional[int] = None,
        memory: Optional[int] = None,
        disk_space: Optional[int] = None,
        exclusive: Optional[bool] = None,
        max_execution_time: Optional[int] = None,
        name: Optional[str] = None,
    ):
        self._url = url
        self._user = user
        self._password = password
        self._main_file = self._validate_main_file(main_file)
        self._mode = self._validate_mode(mode)

        self._output_parms_file = "output.output"
        self._input_file = "input.inputs"
        self._wrapper_python_file = "python_wrapper.py"
        self.input_files = []

        self._task_definition = None
        self._job_definition = None
        self._jobs = None

        # Pre-populating
        self._inputs = self._validate_inputs(inputs)
        self._outputs = self._validate_outputs(outputs)
        self._requirements_file = self._validate_requirements_file(requirements_file)
        self._shell_file = self._validate_shell_file(shell_file)
        self._extra_files = self._validate_extra_files(extra_files)
        self._python = self._validate_python(python)
        self._num_cores = self._validate_num_cores(num_cores)
        self._memory = self._validate_memory(memory)
        self._disk_space = self._validate_disk_space(disk_space)
        self._exclusive = self._validate_exclusive(exclusive)
        self._max_execution_time = self._validate_max_execution_time(max_execution_time)
        self._name = self._validate_name(name)
        self._output_files = self._validate_output_files(output_files)

    @property
    def url(self):
        return self._url

    @property
    def user(self):
        return self._user

    @property
    def password(self):
        return self._password

    @property
    def mode(self):
        return self._mode

    @property
    def inputs(self):
        return self._inputs

    @inputs.setter
    def inputs(self, inputs: Union[str, List[str]]):
        self._inputs = self._validate_inputs(inputs)

    @property
    def outputs(self):
        return self._outputs

    @outputs.setter
    def outputs(self, outputs: Union[str, List[str]]):
        self._outputs = self._validate_outputs(outputs)

    @property
    def main_file(self):
        return self._main_file

    @main_file.setter
    def main_file(self, main_file: str):
        self._main_file = self._validate_main_file(main_file)

    @property
    def requirements_file(self):
        return self._requirements_file

    @requirements_file.setter
    def requirements_file(self, requirements_file: str):
        self._requirements_file = self._validate_requirements_file(requirements_file)

    @property
    def shell_file(self):
        return self._shell_file

    @shell_file.setter
    def shell_file(self, shell_file):
        self._shell_file = self._validate_shell_file(shell_file)

    @property
    def extra_files(self):
        return self._extra_files

    @extra_files.setter
    def extra_files(self, extra_files):
        self._extra_files = self._validate_extra_files(extra_files)

    @property
    def output_files(self):
        return self._output_files

    @output_files.setter
    def output_files(self, output_files):
        self._output_files = self._validate_output_files(output_files)

    @property
    def python(self):
        return self._python

    @python.setter
    def python(self, python: float):
        self._python = self._validate_python(python)

    @property
    def num_cores(self):
        return self._num_cores

    @num_cores.setter
    def num_cores(self, num_cores: int):
        self._num_cores = self._validate_num_cores(num_cores)

    @property
    def memory(self):
        return self._memory

    @memory.setter
    def memory(self, memory: int):
        self._memory = self._validate_memory(memory)

    @property
    def disk_space(self):
        return self._disk_space

    @disk_space.setter
    def disk_space(self, disk_space: int):
        self._disk_space = self._validate_disk_space(disk_space)

    @property
    def exclusive(self):
        return self._exclusive

    @exclusive.setter
    def exclusive(self, exclusive: bool):
        self._exclusive = self._validate_exclusive(exclusive)

    @property
    def max_execution_time(self):
        return self._max_execution_time

    @max_execution_time.setter
    def max_execution_time(self, max_execution_time: int):
        self._max_execution_time = self._validate_max_execution_time(max_execution_time)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = self._validate_name(name)

    ## To bypass implemented tasks, job definitions and jobs.
    @property
    def task_definition(self):
        return self._task_definition

    @task_definition.setter
    def task_definition(self, task_definition: TaskDefinition):
        self._task_definition = task_definition

    @property
    def job_definition(self):
        return self._job_definition

    @job_definition.setter
    def job_definition(self, job_definition: JobDefinition):
        self._job_definition = job_definition

    @property
    def jobs(self):
        return self._jobs

    @jobs.setter
    def jobs(self, jobs: list[JobDefinition]):
        self._jobs = jobs

    ## Validate inputs
    def _validate_inputs(self, inputs):
        """Validate inputs inputs"""

        if self.mode != "python":
            raise ValueError("Inputs are not supported when using APDL or shell files.")

        if inputs is None:
            inputs = []

        if isinstance(inputs, str):
            inputs = inputs.split(",")

        return inputs

    def _validate_outputs(self, outputs):
        """Validate outputs inputs"""

        if self.mode != "python":
            raise warn(
                f"""Outputs are not directly supported when using APDL or shell files.
                However you can still write the parameters you want to the
                file {self._output_parms_file} using the python format
                ('PARAMETER=VALUE')."""
            )

        if outputs is None:
            outputs = []

        if isinstance(outputs, str):
            outputs = outputs.split(",")

        return outputs

    def _validate_main_file(self, main_file):
        """Validate main_file input"""

        if not os.path.exists(main_file):
            raise ValueError(f"The file {main_file} must exist.")

        logger.debug(f"Main file is in: {main_file}.")
        return main_file

    def _validate_shell_file(self, shell_file):
        """Validate shell_file input"""
        return shell_file

    def _validate_extra_files(self, extra_files):
        """Validate extra_files input"""
        if isinstance(extra_files, str):
            extra_files = extra_files.split(",")
        elif extra_files is None:
            extra_files = []

        if extra_files and not all([os.path.exists(each) for each in extra_files]):
            raise ValueError("One or more extra files does not exist.")

        return extra_files

    def _validate_output_files(self, output_files):
        """Validate output_files input"""
        if not output_files:
            output_files = []
        elif isinstance(output_files, str):
            output_files = output_files.split(",")

        return output_files

    def _validate_requirements_file(self, requirements_file):
        """Validate requirements_file input"""
        return requirements_file

    def _validate_python(self, python):
        """Validate python inputs"""
        if python not in [2, 2.7, 3, 3.5, 3.6, 3.7, 3.8, 3.9, 3.10, 3.11, 3.12]:
            warn(f"Version of Python {python} might not be supported by the cluster.")
        return python

    def _validate_num_cores(self, num_cores: int):
        """Validate num_cores inputs"""
        if not num_cores:
            num_cores = 0

        return int(num_cores)

    def _validate_memory(self, memory: int):
        """Validate memory inputs"""
        if not memory:
            memory = 0

        return int(memory)

    def _validate_disk_space(self, disk_space: float):
        """Validate disk_space inputs"""
        if not disk_space:
            disk_space = 0

        return float(disk_space)

    def _validate_exclusive(self, exclusive: bool):
        """Validate exclusive inputs"""
        if exclusive is None:
            exclusive = False

        return bool(exclusive)

    def _validate_max_execution_time(self, max_execution_time):
        """Validate max_execution_time inputs"""
        if not max_execution_time:
            max_execution_time = 0

        return float(max_execution_time)

    def _validate_name(self, name):
        """Validate name inputs"""
        if name is None:
            if self.mode == "python":
                name = "My PyMAPDL project"
            elif self.mode == "apdl":
                name = "My APDL project"
            elif self.mode == "shell":
                name = "My shell project"
            else:
                name = "My project"
        return name

    def _validate_mode(self, mode):
        _, file_extension = os.path.splitext(self._main_file)

        if mode is None:
            if file_extension.lower() in [".sh"]:
                mode = "shell"
            elif file_extension.lower() in [".py"]:
                mode = "python"
            elif file_extension.lower() in [".inp", ".mac"]:
                mode = "apdl"
        else:
            if mode.lower() not in ["python", "shell", "apdl"]:
                raise Exception("File type not supported.")

        logger.debug(f"Mode '{mode}' because of main file ({main_file}) extension.")

        return mode

    def submit(self):
        if self.inputs:
            self._prepare_input_file()

        self._executed_pyscript = os.path.basename(self.main_file)

        # Prepare python wrapper file for input/output injection/extraction
        if self.inputs or self.outputs:
            self._executed_pyscript = self._wrapper_python_file
            self._prepare_python_wrapper()

        # Prepare requirement file
        if self.mode == "python" and not self.requirements_file:
            self._prepare_requirements_file()
        elif self.mode != "python" and self.requirements_file:
            raise ValueError(
                """Using a requirement file when the main file is
                    not a Python file is not compatible.
                    Avoid specifying the argument '--requirement_file'."""
            )

        # Prepare shell file
        if self.mode == "python" and not self.shell_file:
            self._prepare_shell_file()

        # Shell cases
        elif self.mode == "shell":
            if self.shell_file:
                raise ValueError(
                    """Using a shell file and specifying a shell file as main file is not compatible.
                    Avoid specifying the argument '--shell_file'."""
                )
            else:
                self.shell_file = self.main_file

        self._add_files()

        # TODO: To check this
        if self.mode != "python":
            self.shell_file = self.main_file

        # Log in
        self._client = Client(
            url=self.url, username=self.user, password=self.password, verify=False
        )

        # Initializing project
        self._proj = self._create_project()
        self._project_api = self._get_project_api()

        # Setting files
        file_input_ids, file_output_ids = self._add_files_to_project()

        if self.inputs:
            self._input_file_id = file_input_ids[os.path.basename(self.input_file)]
        else:
            self._input_file_id = None

        if self.outputs:
            self._output_parms_file_id = file_output_ids[
                os.path.basename(self._output_parms_file)
            ]
        else:
            self._output_parms_file_id = None

        # Set parameters
        self._input_params, self._output_params, self._param_mappings = (
            self._create_parameters(
                self._project_api,
                inputs=self.inputs,
                input_file_id=self._input_file_id,
                outputs=self.outputs,
                output_file_id=self._output_parms_file_id,
            )
        )

        self._task_def = self._create_task(file_input_ids, file_output_ids)

        # Set jobs
        self._job_def = self._create_job_definition()
        self._jobs = self._create_jobs()
        logger.debug(f"Jobs: {self._jobs}")
        logger.debug("Project submitted.")

        return None

    def _create_jobs(self):
        if not self.jobs:
            self.jobs = [
                Job(
                    name="Job",
                    values={},
                    eval_status="pending",
                    job_definition_id=self._job_def.id,
                )
            ]
        logger.debug(f"jobs: {jobs}")
        return self._project_api.create_jobs(jobs)

    def _create_job_definition(self):
        if not self.job_definition:
            self.job_definition = JobDefinition(name="JobDefinition.1", active=True)
        params = self._input_params + self._output_params

        self.job_definition.task_definition_ids = [self.task_definition.id]
        self.job_definition.parameter_definition_ids = [pd.id for pd in params]
        self.job_definition.parameter_mapping_ids = [
            pm.id for pm in self._param_mappings
        ]

        logger.debug(f"Job definition: {self.job_definition}")
        self.job_definition = self._project_api.create_job_definitions(
            [self.job_definition]
        )[0]

        # Refresh the parameters
        params = self._project_api.get_parameter_definitions(
            id=job_def.parameter_definition_ids
        )
        return job_def

    def _create_task(self, file_input_ids, file_output_ids):

        if self.mode == "apdl":
            task_class = APDLTask
        elif self.mode == "python":
            task_class = PythonTask
        else:
            task_class = ShellTask

        execution_command = f"%executable% %file:{os.path.basename(self.main_file)}%"
        logger.debug(f"Using executable: '{execution_command}'")

        # Process step
        if not self.task_definition:
            self.task_definition = task_class(
                execution_command=execution_command,
                resource_requirements=ResourceRequirements(
                    num_cores=self.num_cores,
                    memory=self.memory * 1024 * 1024,
                    disk_space=self.disk_space * 1024 * 1024,
                    # distributed=True,
                    hpc_resources=HpcResources(exclusive=self.exclusive),
                ),
                max_execution_time=self.max_execution_time,
                execution_level=0,
                num_trials=1,
                input_file_ids=list(file_input_ids.values()),
                output_file_ids=list(file_output_ids.values()),
            )

        logger.debug(f"Task definition: {self.task_definition }")
        return self._project_api.create_task_definitions([self.task_definition])[0]

    def _create_parameters(
        self,
        project_api,
        inputs: Optional[list[str]] = None,
        input_file_id: str = None,
        outputs: Optional[list[str]] = None,
        output_file_id: str = None,
    ):
        if inputs is None:
            inputs = []
            logger.debug("Setting empty input parameters.")

        def is_float(num):
            try:
                float(num)
                return True
            except ValueError:
                return False

        input_params = []
        param_mappings = []

        for each_input_parm in inputs:
            name, value = each_input_parm.split("=")
            if is_float(value):
                parm = FloatParameterDefinition(
                    name=name,
                    display_text=name,
                    default=value,
                )
            else:
                parm = StringParameterDefinition(
                    name=name,
                    display_text=name,
                    default=value,
                )

            # Mapping
            param_map = ParameterMapping(
                key_string=name,
                tokenizer="=",
                parameter_definition_id=parm.id,
                file_id=input_file_id,
            )

            logger.debug(f"Output parameter: {name}\n{parm}\nMapping: {param_map}")
            input_params.append(parm)
            param_mappings.append(param_map)

        logger.debug(f"Input parameters:\n{input_params}")
        input_params = project_api.create_parameter_definitions(input_params)

        output_params = []
        for each_output_parm in outputs:
            # output
            name = each_output_parm
            outparm = StringParameterDefinition(name=name, display_text=name)

            output_params.append(outparm)

        logger.debug(f"Output parameters:\n{output_params}")
        output_params = project_api.create_parameter_definitions(output_params)

        for each_output_parm, outparm in zip(outputs, output_params):
            name = each_output_parm
            # mapping
            parm_map = ParameterMapping(
                key_string=name,
                tokenizer="=",
                parameter_definition_id=outparm.id,
                file_id=output_file_id,
            )
            logger.debug(f"Output parameter: {name}\n{outparm}\nMapping: {parm_map}")

            param_mappings.append(parm_map)

        logger.debug(f"Mapping parameters:\n{param_mappings}")
        param_mappings = project_api.create_parameter_mappings(param_mappings)

        return input_params, output_params, param_mappings

    def _add_files_to_project(self):

        # Checks:
        if not all([os.path.exists(each) for each in self.input_files]):
            raise ValueError("One or more input files do not exist.")

        input_files_ = [os.path.basename(each) for each in self.input_files]

        workdir = os.path.dirname(os.path.realpath(self._main_file))

        input_files = []
        for each_file in self.input_files:
            if workdir in each_file:
                # File in the same location as the main file or in a
                # subdirectory
                file_path = os.path.relpath(each_file, workdir)
            else:
                file_path = os.path.basename(each_file)

            file = File(
                name=os.path.basename(each_file),
                evaluation_path=file_path,
                type="text/plain",
                src=each_file,
            )

            input_files.append(file)

        output_files = [
            File(
                name=os.path.basename(each_file),
                evaluation_path=os.path.basename(each_file),
                type="text/plain",
                collect=True,
                monitor=True,
            )
            for each_file in self.output_files
        ]

        files = input_files + output_files

        for each in files:
            logger.debug(f"Added file:\n{each}")

        files = self._project_api.create_files(files)

        # Getting IDs
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

    def _get_project_api(self):
        return ProjectApi(self._client, self._proj.id)

    def _create_project(self) -> Project:
        jms_api = JmsApi(self._client)
        proj = Project(name=self.name, priority=1, active=True)
        return jms_api.create_project(proj)

    def _add_files(self):
        # Reset
        self.input_files = []

        self.input_files.append(self.main_file)

        if self.inputs:
            self.input_files.append(self._input_file)

        if self.outputs:
            self.output_files.append(self._output_parms_file)

        if self.mode == "python":
            self.input_files.append(self.requirements_file)
            self.input_files.append(self.shell_file)

        if self.inputs or self.outputs:
            self.input_files.append(self._wrapper_python_file)

        if self.extra_files:
            self.input_files.extend(self.extra_files)

    def _prepare_shell_file(self):
        content = f"""
echo "Starting"

# Start venv
python{self.python} -m venv .venv
source .venv/bin/activate

# Install requirements
pip install -r {os.path.basename(self.requirements_file)}

# Run script
python {self._executed_pyscript}
    """

        self.shell_file = self._create_tmp_file("main.sh", content)
        logger.debug(f"Shell file in: {self.shell_file}")

    def _prepare_requirements_file(self):
        import pkg_resources

        content = "\n".join(
            [str(p.as_requirement()) for p in pkg_resources.working_set]
        )
        self.requirements_file = self._create_tmp_file("requirements.txt", content)
        logger.debug(f"Requirements file in: {self.requirements_file}")

    def _prepare_python_wrapper(self):

        content = ""

        if self.inputs:
            content += f"""
# Reading inputs
exec(open("{os.path.basename(self._input_file)}").read())
"""

        content += f"""
# Executing main file
exec(open("{os.path.basename(self.main_file)}").read())
"""

        if self.outputs:
            content += f"""
# Writing output data
with open("{self._output_parms_file}", "w") as fid:
"""
            b0 = "{"
            b1 = "}"

            for each in self.outputs:
                content += f"""    fid.write(f"{each}={b0}{each}{b1}")\n"""

        self._wrapper_python_file = self._create_tmp_file(
            self._wrapper_python_file, content
        )
        logger.debug(f"Wrapper file in: {self._wrapper_python_file}")

    def _prepare_input_file(self):
        if self.inputs:
            content = "\n".join(inputs)
            self._input_file = self._create_tmp_file(self._input_file, content)
            logger.debug(f"Input file in: {self._input_file}")

    def _create_tmp_file(self, file_name, content):
        import tempfile
        import uuid

        dir_ = tempfile.gettempdir()
        sub_dir = str(uuid.uuid4())

        tmp_file = os.path.join(dir_, sub_dir, file_name)
        os.makedirs(os.path.join(dir_, sub_dir))

        with open(tmp_file, "w") as fid:
            fid.write(content)

        return tmp_file


class PyMAPDLJobSubmission(JobSubmission):
    pass


if __name__ == "__main__":

    logging.basicConfig(
        format="[%(asctime)s | %(levelname)s] %(message)s", level=logging.DEBUG
    )

    # from ansys.mapdl.core.hpc import PyMAPDLJobSubmission
    # Test 1
    main_file = "/Users/german.ayuso/pymapdl/src/ansys/mapdl/core/hpc/main.py"
    job = PyMAPDLJobSubmission(
        url="https://10.231.106.91:3000/hps",
        user="repuser",
        password="repuser",
        main_file=main_file,
    )
    job.extra_files.append(
        "/Users/german.ayuso/pymapdl/src/ansys/mapdl/core/hpc/tmp/tmp2.py"
    )

    job.submit()

    # Test2

    # main_file = "main.py"
    # job1 = PyMAPDLJobSubmission(
    #     url="https://10.231.106.91:3000/hps",
    #     user="repuser",
    #     password="repuser",
    #     main_file=main_file
    # )
    # job1.shell_file = "shell_script.py"
    # job1.requirements_file = "requirements.txt"
    # job.extra_files.append("module/tmp2.py")
