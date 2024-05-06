
.. _ref_hpc:


********************************
High performance computing (HPC)
********************************

This page provides an overview on how to use PyMAPDL in HPC clusters.
While it only considers the SLURM scheduler, many of the assumptions for this scheduler might apply to other schedulers, such as PBS, SGE, or LSF.



.. _ref_hpc_slurm:

=================
SLURM HPC cluster
=================

Introduction
============

High performance computing (HPC) clusters are powerful systems designed to handle
computationally intensive tasks efficiently. SLURM (Simple Linux Utility for Resource
Management) is one of the most widely used job schedulers in HPC environments. This
page provides an overview of job submission using PyMAPDL and
SLURM on HPC clusters.


What is SLURM?
==============

SLURM is an open source workload manager and job scheduler designed for Linux
clusters of all sizes. It efficiently allocates resources (compute nodes, CPU
cores, memory, and GPUs) to jobs submitted by users.

For more information on SLURM, see the `SLURM documentation <slurm_docs_>`_.

Basic terms
===========

Descriptions follow of basic terms.

- **Nodes**: Individual computing servers within the cluster.
- **Compute node**: A type of node used only for running processes.
  It is not accessible from outside the cluster.
- **Login node**: A type of node used only for login and job submission.
  No computation should be performed on it. It is sometimes referred to as
  *virtual desktop infrastructure* (VDI).
- **Partition**: A logical grouping of nodes with similar characteristics (for 
  example, CPU architecture and memory size). 
- **Job**: A task submitted to SLURM for execution. 
- **Queue**: A waiting area where jobs are held until resources become available. 
- **Scheduler**: The component responsible for deciding which job gets 
  executed and when and where it gets executed.


Regular job submission workflow
===============================

.. _ref_hpc_login:

Log into the cluster
--------------------

You need access credentials and permissions to log in and submit jobs on the HPC cluster.
Depending on the login node configuration, you can log in using Virtual Network
Computing (VNC) applications or a terminal.

For example, you can log in to a login node using the terminal:

.. code-block:: console

    user@machine:~$ ssh username@login-node-hostname


Writing a SLURM batch script
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
Notice how comments in the file prefixed with ``#SBATCH`` describe the job configuration.
For more information on available ``srun`` and ``sbatch``
arguments, see `Slurm Workload Manager - srun <slurm_srun_>`_ and
`Slurm Workload Manager - sbatch <slurm_sbatch_>`_.

Submitting a job
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

.. warning:: **Command line arguments versus in-file arguments**:
    Command line arguments do **NOT** overwrite the equivalent arguments
    written in the bash file. Hence, you must ensure that the argument that you 
    want to pass using the command line is not already present in the bash file.


.. _ref_hpc_pymapdl_job:

Submit a PyMAPDL job
====================

Using PyMAPDL in an HPC environment managed by SLURM scheduler has certain requirements:

* **An Ansys installation must be accessible from all the compute nodes**.
  This normally implies that the ``ANSYS`` installation directory is in a
  shared drive or directory. Your HPC cluster administrator
  should provide you with the path to the ``ANSYS`` directory.

* **A compatible Python installation must be accessible from all the compute nodes**.
  For compatible Python versions, see :ref:`ref_pymapdl_installation`.

Additionally, you must perform a few key steps to ensure efficient job
execution and resource utilization. Subsequent topics describe these steps.

Check the Python installation
-----------------------------

The PyMAPDL Python package (``ansys-mapdl-core``) must be installed in a virtual
environment that is accessible from the compute nodes.

To see where your Python distribution is installed, use this code:

.. code-block:: console

    user@machine:~$ which python3
    /usr/bin/python3

To print the version of Python you have available, use this code:

.. code-block:: console

    user@machine:~$ python3 --version
    Python 3.9.16

You should be aware that your machine might have installed other Python versions.
To find out if those installations are already in the ``PATH`` environment variable,
you can press the **Tab** key to use autocomplete:

.. code-block:: console

    user@machine:~$ which python3[TAB]
    python3             python3-intel64     python3.10-config   python3.11          python3.12          python3.8           python3.8-intel64   python3.9-config  
    python3-config      python3.10          python3.10-intel64  python3.11-config   python3.12-config   python3.8-config    python3.9 
    $ which python3.10
    /usr/bin/python3.10

You should use a Python version that is compatible with PyMAPDL.
For more information, see:ref:`ref_pymapdl_installation`.

The ``which`` command returns the path where the Python executable is installed.
You can use that executable to create your own Python virtual environment in a directory
that is accessible from all the compute nodes.
For most HPC clusters, the ``/home/$user`` directory is generally available to all nodes.
You can then create the virtual environment in the ``/home/user/.venv`` directory:

.. code-block:: console

    user@machine:~$ python3 -m venv /home/user/.venv

After activating the virtual environment, you can install PyMAPDL.


Install PyMAPDL
---------------

To install PyMAPDL on the activated virtual environment, run the following commands:

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

To test if this virtual environment is accessible from the compute nodes,
run this ``test.sh`` bash script:

.. code-block:: bash

    #!/bin/bash
    #SBATCH --job-name=myjob
    #SBATCH --nodes=1
    #SBATCH --ntasks-per-node=4
    #SBATCH --time=01:00:00

    # Commands to run
    echo "Testing Python!"
    source /home/user/.venv/bin/activate
    python -c "from ansys.mapdl import core;print(f'PyMAPDL version {core.__version__} was successfully imported.')"

then you can run that script using: 

.. code-block:: console

    user@machine:~$ srun test.sh

This command might take a minute or two to complete, depending on the amount of free
resources available in the cluster.
On the console, you should see this output:

.. code-block:: text

    Testing Python!
    PyMAPDL version 0.68.1 was successfully imported.

If you see an error in the output, see :ref:`ref_hpc_troubleshooting`, especially
:ref:`ref_python_venv_not_accesible`.

Submit a PyMAPDL job
--------------------

To submit a PyMAPDL job, you must create two files:

- Python script with the PyMAPDL code
- Bash script that activates the virtual environment and calls the Python script

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

To start the simulation, you use this code:

.. code-block:: console

    user@machine:~$ srun job.sh


The bash script allows you to customize the environment before running the Python script.
This bash script performs such tasks as creating environment variables, moving to
different directories, and printing to ensure your configuration is correct. However,
this bash script is not mandatory.
You can avoid having the ``job.sh`` bash script if the virtual environment is activated
and you pass all the environment variables to the job:

.. code-block:: console

    user@machine:~$ source /home/user/.venv/bin/activate
    (.venv) user@machine:~$ srun python pymapdl_script.py --export=ALL


The ``--export=ALL`` argument might not be needed, depending on the cluster configuration.
Furthermore, you can omit the Python call in the preceding command if you include the
Python shebang (``#!/usr/bin/python3``) in the first line of the ``pymapdl_script.py`` script.

.. code-block:: console

    user@machine:~$ source /home/user/.venv/bin/activate
    (.venv) user@machine:~$ srun pymapdl_script.py --export=ALL

If you prefer to run the job in the background, you can use the ``sbatch``
command instead of the ``srun`` command. However, in this case, the Bash file is needed:

.. code-block:: console

    user@machine:~$ sbatch job.sh
    Submitted batch job 1

Here is the expected output of the job:

.. code-block:: text

    Number of CPUs: 10.0


Examples
========

For an example that uses a machine learning genetic algorithm in
an HPC system managed by SLURM scheduler, see :ref:`hpc_ml_ga_example`.


Monitoring jobs
===============

View the job queue
------------------

The ``squeue`` command displays information about jobs that are currently queued or
running on the system.

**Basic usage:**

.. code-block:: bash

    squeue

**To see jobs from a specific user:**

.. code-block:: bash

    squeue -u username

**To filter jobs by partition:**

.. code-block:: bash

    squeue -p partition_name

**Common options:**

- ``-l`` or ``--long``: Displays detailed information about each job.
- ``--start``: Predicts and shows the start times for pending jobs.

Control the jobs and configuration
----------------------------------

The ``scontrol`` command provides a way to view and modify the SLURM configuration and state.
It's a versatile tool for managing jobs, nodes, partitions, and more.

**Show information about a job:**

.. code-block:: bash

    scontrol show job <jobID>

**Show information about a node:**

.. code-block:: bash

    scontrol show node nodename

**Hold and release jobs:**

- To hold a job (stop it from starting): ``scontrol hold <jobID>``
- To release a job on hold: ``scontrol release <jobID>``

Cancel jobs
-----------

The ``scancel`` command cancels a running or pending job.

**Cancel a specific job:**

.. code-block:: bash

    scancel <jobID>

**Cancel all jobs of a specific user:**

.. code-block:: bash

    scancel -u username

**Cancel jobs by partition:**

.. code-block:: bash

    scancel -p partition_name

**Common options:**

- ``--name=jobname``: Cancels all jobs with a specific name.
- ``--state=pending``: Cancels all jobs in a specific state,
  such as all pending jobs as shown.

Report accounting Information
-----------------------------

The ``sacct`` account reports job or job step accounting information
about active or completed jobs.

**Basic usage:**

.. code-block:: bash

    sacct

**To see information about jobs from a specific user:**

.. code-block:: bash

    sacct -u username

**To show information about a specific job or job range:**

.. code-block:: bash

    sacct -j <jobID>
    sacct -j <jobID_1>,<jobID_2>

**Common options:**

- ``--format``: Specifies which fields to display.
  For example, ``--format=JobID,JobName,State``.
- ``-S`` and ``-E``: Sets the start and end times for the report.
  For example, ``-S 2023-01-01 -E 2023-01-31``.

For more information, see the SLURM documentation
or use the ``man`` command (for example, ``man squeue``) to explore all available
options and their usage.


Best practices
==============
- Optimize resource usage to minimize job wait times and maximize cluster efficiency.
- Regularly monitor job queues and system resources to identify potential bottlenecks.
- Follow naming conventions for batch scripts and job names to maintain organization.
- Keep batch scripts and job submissions concise and well-documented 
  for reproducibility and troubleshooting.

.. _ref_hpc_troubleshooting:

Troubleshooting
===============

Debugging jobs
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
is not using the virtual environment (``/home/user/.venv``):

.. code-block:: console

    user@machine:~$ srun test.sh
    Testing Python!
    Traceback (most recent call last):
    File "<string>", line 1, in <module>
    ImportError: No module named ansys.mapdl

This could be for a number of reasons. One of them is that the system Python distribution
used to create the virtual environment is not accessible from the compute nodes
due to one of these reasons:

- The virtual environment has been created in a
  directory that is not accessible from the nodes.
- The virtual environment has been created from a Python
  executable that is not available to the compute nodes.
  Hence, the virtual environment is not activated. For
  example, you might be creating the virtual environment
  using Python 3.10, but only Python 3.8 is available
  from the compute nodes.

You can test which Python executable the cluster is using by starting an interactive session in
a compute node with this code:

.. code-block:: console

    user@machine:~$ srun --pty /bin/bash
    user@compute_node_01:~$ compgen -c | grep python # List all commands starting with python

.. the approach to solve this comes from:
   https://stackoverflow.com/questions/64188693/problem-with-python-environment-and-slurm-srun-sbatch

Many HPC infrastructures use environment managers to load and unload
software packages using modules and environment variables. 
Hence, you might want to make sure that the correct module is loaded in your script.
For information on two of the most common environment managers, see the
`Modules documentation <modules_docs_>`_ and `Lmod documentation <lmod_docs_>`_.
Check your cluster documentation to know which environment
manager is being using and how to load Python with it.
If you find any issue, you should contact your cluster administrator.

If there is not a suitable Python version accessible from the
compute nodes, you might have to request your HPC cluster
administrator to have a suitable Python version installed on all
compute nodes.
If this is not an option, see :ref:`ref_ansys_provided_python`.

.. _ref_ansys_provided_python:

Using the Ansys-provided Python installation
--------------------------------------------

**For development purposes only**

In certain HPC environments the possibility of installing a different Python version
is limited for security reasons. In such cases, the Python distribution available in
the Ansys installation can be used.
This Python distribution is a customized Python (CPython)
version for Ansys products use only. Its use is **discouraged**
except for very advanced users and special use cases.

This Python distribution is in the following directory, where
``%MAPDL_VERSION%`` is the three-digit Ansys version:

.. code-block:: text

    /ansys_inc/v%MAPDL_VERSION%/commonfiles/CPython/3_10/linx64/Release/python

For example, here is the directory for Ansys 2024 R2:

.. code-block:: text

    /ansys_inc/v242/commonfiles/CPython/3_10/linx64/Release/python


In Ansys 2024 R1 and later, the unified installer includes CPython 3.10.
Earlier versions include CPython 3.7 (``/commonfiles/CPython/3_7/linx64/Release/python``).

Because the Ansys installation must be available to all
the compute nodes to run simulations using them, this
Python distribution is normally also available to the
compute nodes. Hence, you can use it to create your
own virtual environment.

Due to the particularities of this Python distribution, you must
follow these steps to create a virtual environment accessible to
the compute nodes:

#. Set the Python path environment variable:

   .. code-block:: console

      user@machine:~$ export PY_PATH=/ansys_inc/v241/commonfiles/CPython/3_10/linx64/Release/Python

#. For only Ansys 2024 R1 and earlier, patch the ``PATH`` and ``LD_LIBRARY_PATH``
   environment variables:

   .. code-block:: console

      user@machine:~$ PATH=$PY_PATH/bin:$PATH  # Patching path
      user@machine:~$ LD_LIBRARY_PATH=$PY_PATH/lib:$LD_LIBRARY_PATH  # Patching LD_LIBRARY_PATH

#. On the same terminal, create your own virtual
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

The following topics provide some advanced ideas for you to
explore when using PyMAPDL on HPC clusters.

Advanced job management
-----------------------

Job dependencies
~~~~~~~~~~~~~~~~
Specify dependencies between jobs using the ``--dependency`` flag.
Jobs can depend on completion, failure, or other criteria of previously submitted jobs.

Array jobs
~~~~~~~~~~

Submit multiple jobs as an array using the ``--array`` flag. Each array
element corresponds to a separate job, allowing for parallel execution of similar tasks.

Job arrays with dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Combine array jobs with dependencies for complex job
scheduling requirements. This allows for parallel execution while maintaining dependencies
between individual tasks.

Resource allocation and request
-------------------------------

Specify resources
~~~~~~~~~~~~~~~~~
Use SLURM directives in batch scripts to specify required
resources such as number of nodes, CPU cores, memory, and time limit.

Request resources
~~~~~~~~~~~~~~~~~
Use the ``--constraint`` flag to request specific hardware
configurations (for example, CPU architecture) or the ``--gres`` flag for requesting generic
resources like GPUs.

Resource Limits
~~~~~~~~~~~~~~~
Set resource limits for individual jobs using directives such as
``--cpus-per-task``, ``--mem``, and ``--time``.

