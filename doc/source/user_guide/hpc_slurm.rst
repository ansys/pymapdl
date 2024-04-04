
.. _ref_hpc_slurm:

=================
SLURM HPC cluster
=================

Introduction
============

High-Performance Computing (HPC) clusters are powerful systems designed to handle
computationally intensive tasks efficiently. SLURM (Simple Linux Utility for Resource
Management) is one of the most widely used job schedulers in HPC environments. This
guide aims to provide a basic understanding of job submission using PyMAPDL and
SLURM on HPC clusters.


What is SLURM?
==============

SLURM is an open source workload manager and job scheduler designed for Linux
clusters of all sizes. It efficiently allocates resources (compute nodes, CPU
cores, memory, GPUs) to jobs submitted by users.

For more information regarding SLURM, visit `SLURM Documentation <slurm_docs_>`_.

Basic concepts
==============

- **Nodes**: Individual computing servers within the cluster.
- **Compute node**: A type of node used only for running processes.
  It is not accessible from outside the cluster.
- **Login nodes**: A type of node which is used only for login and job submission.
  No computation should be performed on it. It is sometimes referred to as
  'virtual desktop infrastructure' (VDI).
- **Partition**: A logical grouping of nodes with similar characteristics
  (for example CPU architecture, memory size). 
- **Job**: A task submitted to SLURM for execution. 
- **Queue**: A waiting area where jobs are held until resources become available. 
- **Scheduler**: The component responsible for deciding which job gets executed
  when and where.


Regular job submission workflow
===============================

Login into the cluster
----------------------

You need access credentials and permissions to log in and submit jobs on the HPC cluster.
Depending on the login node configuration, you can login using GUI based tools like VNC or just a terminal.

For example, you can log in into a login node using the terminal:

.. code-block:: console

    user@machine:~$ ssh username@login-node-hostname


Writing a SLURM Batch Script
----------------------------

A SLURM batch script is a shell script that specifies
job parameters and commands to execute. Here's a basic example:

**my_script.sh**

.. code-block:: bash
    
    #!/bin/bash
    #SBATCH --job-name=myjob
    #SBATCH --nodes=1
    #SBATCH --ntasks-per-node=4
    #SBATCH --time=01:00:00

    # Commands to run
    echo "Hello, SLURM!"
    srun my_executable


This script is run using ``srun`` and ``sbatch``.
Notice how the job configuration is detailed through comments in the
file prefixed with ``#SBATCH``.
For more information regarding the possible ``srun`` and ``sbatch``
arguments visit `Slurm Workload Manager - srun <slurm_srun_>`_ and
`Slurm Workload Manager - sbatch <slurm_sbatch_>`_.

Submitting a Job
----------------
To submit a job, use the ``srun`` command followed by the name of
the batch script:

.. code-block:: console
    
    user@machine:~$ srun my_script.sh

If you prefer to submit a batch job, you can use the ``sbatch`` command:

.. code-block:: console
    
    user@machine:~$ sbatch my_script.sh

You can specify each job setting using the command line. For example:

.. code-block:: console

    user@machine:~$ srun --nodes=2 my_script.sh

.. warning:: **Command line arguments vs In-file arguments**:
    The command line arguments do **NOT** overwrite the equivalent arguments written
    in the bash file.
    Hence, make sure that the argument you want to pass using the command line is
    not present already in the bash file.

Submit a PyMAPDL job
====================

Using PyMAPDL in an HPC environment managed by SLURM scheduler has certain requirements:

* An **ANSYS installation accessible from all the compute nodes**.
  This normally implies that the ANSYS installation directory is in a
  shared drive or directory. Your HPC cluster administrator
  should provide you with the path to the ANSYS directory.

* A compatible **Python installation accessible from all the compute nodes**.
  The compatible Python versions can be found in :ref:`ref_pymapdl_installation`.

Additionally, it involves a few key steps to ensure efficient job
execution and resource utilization.
The steps are detailed as follows:

Install PyMAPDL
---------------

PyMAPDL Python package (``ansys-mapdl-core``) needs to be installed in a virtual
environment which is accessible from the compute nodes.

To do that you can find where your Python distribution is installed using:

.. code-block:: console

    user@machine:~$ which python3
    /usr/bin/python3

You can print the version of Python you have available by doing:

.. code-block:: console

    user@machine:~$ python3 --version
    Python 3.9.16

You should be aware that your machine might have installed other Python versions.
If those installations are already in the ``PATH``, you can use autocomplete (``TAB``)
to find out:

.. code-block:: console

    user@machine:~$ which python3[TAB]
    python3             python3-intel64     python3.10-config   python3.11          python3.12          python3.8           python3.8-intel64   python3.9-config  
    python3-config      python3.10          python3.10-intel64  python3.11-config   python3.12-config   python3.8-config    python3.9 
    $ which python3.10
    /usr/bin/python3.10

Remember you should use a Python version which is compatible with PyMAPDL.
For more information visit :ref:`ref_pymapdl_installation`.

The ``which`` command returns the path where the Python executable is installed.
You can use that executable to create your own Python virtual environment in a directory
which is accessible from all the compute nodes.
For most of HPC cluster, ``/home/$user`` is generally available to all nodes.
Then the virtual environment can be created in the directory ``/home/user/.venv``:

.. code-block:: console

    user@machine:~$ python3 -m venv /home/user/.venv

Then you can install PyMAPDL after activating the virtual environment:

.. code-block:: console

    user@machine:~$ source /home/user/.venv/bin/activate
    (.venv) user@machine:~$ pip install ansys-mapdl-core
    Collecting ansys-mapdl-core
    Downloading ansys_mapdl_core-0.68.1-py3-none-any.whl (26.9 MB)
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 26.9/26.9 MB 37.3 MB/s eta 0:00:00
    Collecting pexpect>=4.8.0
    Using cached pexpect-4.9.0-py2.py3-none-any.whl (63 kB)
    Collecting click>=8.1.3
    ...

You can test if this virtual environment is accessible from the compute nodes by
running the following bash script ``test.sh``:

.. code-block:: bash

    #!/bin/bash
    #SBATCH --job-name=myjob
    #SBATCH --nodes=1
    #SBATCH --ntasks-per-node=4
    #SBATCH --time=01:00:00

    # Commands to run
    echo "Testing Python!"
    source /home/user/.venv/bin/activate
    python -c "from ansys.mapdl import core;print(f'PyMAPDL version {core.__version__} was successfully imported!')"

using: 

.. code-block:: console

    user@machine:~$ srun test.sh

This command might take around 1-2 minutes to complete depending on the amount of free
resources available in the cluster.
The console output should show:

.. code-block:: text

    Testing Python!
    PyMAPDL version 0.68.1 was successfully imported!

If you see an error in the output, visit :ref:`ref_hpc_troubleshooting`, especially
:ref:`ref_python_venv_not_accesible`.

Submit a PyMAPDL job
--------------------

To submit a PyMAPDL job, you need to create two files: a Python script
with the PyMAPDL code and a bash script which activate the virtual environment
and call the Python script.

**Python script:** ``pymapdl_script.py``

.. code-block:: python

    from ansys.mapdl.core import launch_mapdl

    # Number of processors must be lower than the
    # number of CPUs allocated for the job.
    mapdl = launch_mapdl(nproc=10)

    mapdl.prep7()
    n_proc = mapdl.get_value("ACTIVE", 0, "NUMCPU")
    print(f"Number of CPUs: {n_proc}")

    mapdl.exit()


**Bash script:** ``job.sh``

.. code-block:: bash

    source /home/user/.venv/bin/activate
    python pymapdl_script.py

The simulation is then started using:

.. code-block:: console

    user@machine:~$ srun job.sh


The bash file allow you to customize the environment before running the Python
script (create new environment variables, move to different directories, do some printing
to ensure your configuration is right, etc), however this file is not mandatory.
You can avoid having the bash file ``job.sh`` if the virtual environment is activated,
and you pass all the environment variables to the job:

.. code-block:: console

    user@machine:~$ source /home/user/.venv/bin/activate
    (.venv) user@machine:~$ srun python pymapdl_script.py --export=ALL


The ``--export=ALL`` argument might not be needed, depending on the cluster configuration.
Furthermore, you can omit the ``python`` call in the preceding command, if there is
the Python shebang (``#!/usr/bin/python3``) in the ``pymapdl_script.py`` script first line.

.. code-block:: console

    user@machine:~$ source /home/user/.venv/bin/activate
    (.venv) user@machine:~$ srun pymapdl_script.py --export=ALL

If you prefer to run the job on the background, you can use ``sbatch``
instead of ``srun``, but in that case, the bash file is needed:

.. code-block:: console

    user@machine:~$ sbatch job.sh
    Submitted batch job 1

The expected output of the job should be:

.. code-block:: text

    Number of CPUs: 10.0


Monitoring Jobs
===============

``squeue`` - View Job Queue
---------------------------

The ``squeue`` command displays information about jobs that are currently queued or
running on the system.

**Basic Usage:**

.. code-block:: bash

    squeue

**To see jobs from a specific user:**

.. code-block:: bash

    squeue -u username

**To filter jobs by partition:**

.. code-block:: bash

    squeue -p partition_name

**Common Options:**

- ``-l`` or ``--long``: Displays detailed information about each job.
- ``--start``: Predicts and shows the start times for pending jobs.

``scontrol`` - Control Jobs and Configuration
---------------------------------------------

``scontrol`` provides a way to view and modify SLURM configuration and state.
It's a versatile tool for managing jobs, nodes, partitions, and more.

**Show information about a job:**

.. code-block:: bash

    scontrol show job <jobID>

**Show information about a node:**

.. code-block:: bash

    scontrol show node nodename

**Hold and release jobs:**

- To hold (stop a job from starting): ``scontrol hold <jobID>``
- To release a held job: ``scontrol release <jobID>``

``scancel`` - Cancel Jobs
-------------------------

``scancel`` cancels a running or pending job.

**Cancel a specific job:**

.. code-block:: bash

    scancel <jobID>

**Cancel all jobs of a specific user:**

.. code-block:: bash

    scancel -u username

**Cancel jobs by partition:**

.. code-block:: bash

    scancel -p partition_name

**Common Options:**

- ``--name=jobname``: Cancels all jobs with a specific name.
- ``--state=pending``: Cancels all jobs in a specific state,
  for example, pending jobs.

``sacct`` - Accounting Information
----------------------------------

``sacct`` is used to report job or job step accounting information
about active or completed jobs.

**Basic Usage:**

.. code-block:: bash

    sacct

**To see information about jobs from a specific user:**

.. code-block:: bash

    sacct -u username

**To show information about a specific job or job range:**

.. code-block:: bash

    sacct -j <jobID>
    sacct -j <jobID_1>,<jobID_2>

**Common Options:**

- ``--format``: Specifies which fields to display,
  for example, ``--format=JobID,JobName,State``.
- ``-S`` and ``-E``: Set the start and end time for the report,
  for example, ``-S 2023-01-01 -E 2023-01-31``.

For more detailed information, refer to the official SLURM documentation
or use the `man` command (for example, `man squeue`) to explore all available
options and their usage.


Best Practices
==============
- Optimize resource usage to minimize job wait times and maximize cluster efficiency.
- Regularly monitor job queues and system resources to identify potential bottlenecks.
- Follow naming conventions for batch scripts and job names to maintain organization.
- Keep batch scripts and job submissions concise and well-documented 
  for reproducibility and troubleshooting.

.. _ref_hpc_troubleshooting:

Troubleshooting
===============

Debugging Jobs
--------------
- Use ``--output`` and ``--error`` directives in batch scripts to capture
  standard output and error messages. 

- Check SLURM logs for error messages and debugging information.


.. _ref_python_venv_not_accesible:

Python virtual environment is not accessible
--------------------------------------------
If there is an error while testing the Python installation, it might mean 
that the Python environment is not accessible to the compute nodes.
For example, in the following output, PyMAPDL could not be found, meaning that the script
is not using the virtual environment ``/home/user/.venv``:

.. code-block:: console

    user@machine:~$ srun test.sh
    Testing Python!
    Traceback (most recent call last):
    File "<string>", line 1, in <module>
    ImportError: No module named ansys.mapdl

This could be for a number of reasons. One of them is that the system Python distribution
used to create the virtual environment is not accessible from the compute nodes.
Either because the virtual environment has been created in a directory which is not accessible
from the nodes or because the virtual environment has been created from a Python executable
which is not available to the compute nodes, hence the virtual environment is not activated.
For example, you might be creating the virtual environment using Python 3.10, but only
Python 3.8 is available from the compute nodes.

You can test which Python executable the cluster is using by starting an interactive session in
a compute node using:

.. code-block:: console

    user@machine:~$ srun --pty /bin/bash
    user@compute_node_01:~$ compgen -c | grep python # List all commands starting with python

.. the approach to solve this comes from:
   https://stackoverflow.com/questions/64188693/problem-with-python-environment-and-slurm-srun-sbatch

Many HPC infrastructure uses environment managers to load and unload software package
using modules and environment variables. 
Hence you might want to make sure that the correct module is loaded in your script.
Two of the most common environment managers are
`Modules documentation <modules_docs_>`_ and `Lmod documentation <lmod_docs_>`_.
Check your cluster documentation to know which environment manager is using, and how to
load Python with it. If you find any issue, you should contact your cluster administrator.

If there is not a suitable Python version accessible from the compute nodes, you might need
request to your HPC cluster administrator to have installed in all the compute
nodes a suitable Python version.
If this is not an option, visit :ref:`ref_ansys_provided_python`.

.. _ref_ansys_provided_python:

Using ANSYS provided Python installation
----------------------------------------

**For development purposes only**

In certain HPC environments the possibility of installing a different Python version
is limited for security reasons.

In those cases, the Python distribution available within the ANSYS installation can be used.
This Python distribution is a customized Python (CPython) version for ANSYS products use only, and
its usage is **discouraged** except for very advanced users and user cases.

This Python distribution is in:

.. code-block:: text

    /ansys_inc/v%MAPDL_VERSION%/commonfiles/CPython/3_10/linx64/Release/python

whereas ``%MAPDL_VERSION%`` is the 3 digits ANSYS version. For instance for ANSYS 2024R2:

.. code-block:: text

    /ansys_inc/v242/commonfiles/CPython/3_10/linx64/Release/python


From ANSYS 2024R1, the Python version included in the unified installer is CPython 3.10.
Previous versions were including CPython 3.7 (``/commonfiles/CPython/3_7/linx64/Release/python``).

Because ANSYS installation needs to be available to all the compute nodes to run simulations using them,
this Python distribution is normally also available to the compute nodes.
Hence, you can use it to create your own virtual environment.

Due to the particularities of this Python distribution, you need to follow the following steps to create
a virtual environment accessible to the compute nodes.

1. Set Python path environment variable:

   .. code-block:: console

      user@machine:~$ export PY_PATH=/ansys_inc/v241/commonfiles/CPython/3_10/linx64/Release/Python

2. Patch ``PATH`` and ``LD_LIBRARY_PATH`` *(Only required for ANSYS 2024R1 or older)*:

   .. code-block:: console

      user@machine:~$ PATH=$PY_PATH/bin:$PATH  # Patching path
      user@machine:~$ LD_LIBRARY_PATH=$PY_PATH/lib:$LD_LIBRARY_PATH  # Patching LD_LIBRARY_PATH

3. Then, on the same terminal, you can proceed to create your own virtual
   environment and activate it:

   .. code-block:: console

      user@machine:~$ $PY_PATH -m venv /home/user/.venv
      user@machine:~$ source /home/user/.venv

4. Install PyMAPDL:

   .. code-block:: console 

      (.venv) user@machine:~$ python -m pip install ansys-mapdl-core

5. Use it to launch simulations, using ``srun``:

   .. code-block:: console

      (.venv) user@machine:~$ srun pymapdl_script.py

   or ``sbatch``:

   .. code-block:: console

      (.venv) user@machine:~$ sbatch job.sh
      Submitted batch job 1


Advanced configuration
======================

In this section, some advanced ideas are drafted for you to explore when using
PyMAPDL on HPC clusters.

Advanced Job Management
-----------------------

Job Dependencies
~~~~~~~~~~~~~~~~
Specify dependencies between jobs using the ``--dependency`` flag.
Jobs can depend on completion, failure, or other criteria of previously submitted jobs.

Array Jobs
~~~~~~~~~~

Submit multiple jobs as an array using the ``--array`` flag. Each array
element corresponds to a separate job, allowing for parallel execution of similar tasks.

Job Arrays with Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Combine array jobs with dependencies for complex job
scheduling requirements. This allows for parallel execution while maintaining dependencies
between individual tasks.

Resource Allocation and Request
-------------------------------

Specifying Resources
~~~~~~~~~~~~~~~~~~~~
Use SLURM directives in batch scripts to specify required
resources such as number of nodes, CPU cores, memory, and time limit.

Requesting Resources
~~~~~~~~~~~~~~~~~~~~
Use the ``--constraint`` flag to request specific hardware
configurations (for example, CPU architecture) or the ``--gres`` flag for requesting generic
resources like GPUs.

Resource Limits
~~~~~~~~~~~~~~~
Set resource limits for individual jobs using directives such as
``--cpus-per-task``, ``--mem``, and ``--time``.
