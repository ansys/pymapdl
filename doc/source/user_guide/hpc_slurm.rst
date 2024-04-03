
.. _ref_hpc_slurm:

=============
SLURM cluster
=============

What is SLURM?
==============

SLURM is an open-source workload manager and job scheduler designed for Linux
clusters of all sizes. It efficiently allocates resources (compute nodes, CPU
cores, memory, GPUs) to jobs submitted by users.


Basic concepts
==============

- **Nodes**: Individual computing servers within the cluster. 
- **Partition**: A logical grouping of nodes with similar characteristics
  (e.g., CPU architecture, memory size). 
- **Job**: A task submitted to SLURM for execution. 
- **Queue**: A waiting area where jobs are held until resources become available. 
- **Scheduler**: The component responsible for deciding which job gets executed
  when and where.
- **Compute node**: A type of node used only for running processes. It is not accessible from outside the cluster.
- **Login nodes**: A type of node which is used only for login and job submission. No computation should be performed on it. It is sometimes referred to as 'virtual desktop infrastructure' (VDI).


Regular job submission workflow
===============================

Login into the cluster
----------------------

You need access credentials and permissions to log in and submit jobs on the HPC cluster.
Depending on the login node configuration, you can login using GUI based tools like VNC or just a terminal.

For example, you can login using terminal in a machine using:

.. code:: console

    user@machine:~$ ssh username@machine-hostname


Writing a SLURM Batch Script
----------------------------

A SLURM batch script is a shell script that specifies
job parameters and commands to execute. Here's a basic example:

.. code:: bash
    
    #!/bin/bash
    #SBATCH --job-name=myjob
    #SBATCH --nodes=1
    #SBATCH --ntasks-per-node=4
    #SBATCH --time=01:00:00

    # Commands to run
    echo "Hello, SLURM!"
    srun my_executable


Submitting a Job
----------------
To submit a job, use the `sbatch` command followed by the name of
the batch script:

.. code:: console
    
    user@machine:~$ sbatch my_batch_script.sh


Submit a PyMAPDL job
====================

Using PyMAPDL (Python interface for ANSYS Mechanical APDL) in a high-performance
computing (HPC) environment managed by SLURM scheduler involves a few key steps
to ensure efficient job execution and resource utilization. Below is a guide
outlining the process:


Install PyMAPDL
---------------

PyMAPDL Python package (``ansys-mapdl-core``) needs to be installed in a virtual environment which is accessible from the compute nodes.

To do that you can find where your python distribution is installed using:

.. code:: console

    user@machine:~$ which python3
    /usr/bin/python3

You can check which version of Python you have by doing:

.. code:: console

    user@machine:~$ /usr/bin/python3 --version
    Python 3.8.10

.. note:: 
    You should be aware that your machine might have installed other Python versions.
    If those installations are already in the ``PATH``, you can use autocomplete (``TAB``)
    to find out:

    .. console:: console

        $ which python3[tab]
        python3             python3-intel64     python3.10-config   python3.11          python3.12          python3.8           python3.8-intel64   python3.9-config  
        python3-config      python3.10          python3.10-intel64  python3.11-config   python3.12-config   python3.8-config    python3.9 
        $ which python3.10

The ``which`` command returns the path where your OS Python is installed.
You can use that distribution to create your own Python virtual environment in the directory ``/home/user/.venv`` or wherever you prefer:

.. code:: console

    user@machine:~$ python3 -m venv /home/user/.venv

Then you can install PyMAPDL after activating the virtual environment:

.. code:: console

    user@machine:~$ source /home/user/.venv/bin/activate
    (.venv) user@machine:~$ pip install ansys-mapdl-core
    Collecting ansys-mapdl-core
    Downloading ansys_mapdl_core-0.68.1-py3-none-any.whl (26.9 MB)
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 26.9/26.9 MB 37.3 MB/s eta 0:00:00
    Collecting pexpect>=4.8.0
    Using cached pexpect-4.9.0-py2.py3-none-any.whl (63 kB)
    Collecting click>=8.1.3
    ...

Then you can test if this virtual environment is accessible from the compute nodes by
running the following bash script:

.. code:: bash

    #!/bin/bash
    #SBATCH --job-name=myjob
    #SBATCH --nodes=1
    #SBATCH --ntasks-per-node=4
    #SBATCH --time=01:00:00

    # Commands to run
    echo "Testing Python!"
    source /home/user/.venv/bin/activate
    python -c "from ansys.mapdl import core;print(core.__version__)"

This 

Monitoring Jobs
===============

- **squeue**: View the status of all jobs in the queue. 
- **sacct**: View accounting information for completed jobs. 
- **scontrol show job<job_id>**: View detailed information about a specific job.


Advanced Job Management
=======================

Job Dependencies
----------------
Specify dependencies between jobs using the `--dependency` flag.
Jobs can depend on completion, failure, or other criteria of previously submitted jobs.

Array Jobs
----------
Submit multiple jobs as an array using the `--array` flag. Each array
element corresponds to a separate job, allowing for parallel execution of similar tasks.

Job Arrays with Dependencies
----------------------------
Combine array jobs with dependencies for complex job
scheduling requirements. This allows for parallel execution while maintaining dependencies
between individual tasks.

Resource Allocation and Request
===============================

Specifying Resources
--------------------
Use SLURM directives in batch scripts to specify required
resources such as number of nodes, CPU cores, memory, and time limit.

Requesting Resources
--------------------
Use the `--constraint` flag to request specific hardware
configurations (e.g., CPU architecture) or the `--gres` flag for requesting generic
resources like GPUs.

Resource Limits
---------------
Set resource limits for individual jobs using directives such as
`--cpus-per-task`, `--mem`, and `--time`.

Troubleshooting and Best Practices
==================================

Debugging Jobs
--------------
- Use `--output` and `--error` directives in batch scripts to capture
  standard output and error messages. 

- Check SLURM logs for error messages and debugging information.

Best Practices
--------------
- Optimize resource usage to minimize job wait times and maximize cluster efficiency.
- Regularly monitor job queues and system resources to identify potential bottlenecks.
- Follow naming conventions for batch scripts and job names to maintain organization.
- Keep batch scripts and job submissions concise and well-documented 
  for reproducibility and troubleshooting.
