
.. _ref_hpc_pymapdl_job:

=======================
PyMAPDL on HPC Clusters
=======================


Introduction
============

PyMAPDL communicates with MAPDL using the gRPC protocol.
This protocol offers many advantages and features, for more information
see :ref:`ref_project_page`.
One of these features is that it is not required to have both,
PyMAPDL and MAPDL processes, running on the same machine.
This possibility open the door to many configurations, depending
on whether you run them both or not on the HPC compute nodes.
Additionally, you might to be able interact with them (``interactive`` mode)
or not (``batch`` mode).

Currently, the supported configurations are:

* :ref:`ref_pymapdl_batch_in_cluster_hpc`


Since v0.68.5, PyMAPDL can take advantage of the tight integration
between the scheduler and MAPDL to read the job configuration and
launch an MAPDL instance that can use all the resources allocated
to that job.
For instance, if a SLURM job has allocated 8 nodes with 4 cores each,
then PyMAPDL launches an MAPDL instance which uses 32 cores
spawning across those 8 nodes.
This behaviour can turn off if passing the environment variable
:envvar:`PYMAPDL_ON_SLURM` or passing the argument `detect_HPC=False`
to :func:`launch_mapdl() <ansys.mapdl.core.launcher.launch_mapdl>`.


.. _ref_pymapdl_batch_in_cluster_hpc:

Submit a PyMAPDL batch job to the cluster from the entrypoint node
==================================================================

Many HPC clusters allow their users to login in a machine using
``ssh``, ``vnc``, ``rdp``, or similar technologies and submit a job
to the cluster from there.
This entrypoint machine, sometimes known as *head node* or *entrypoint node*,
might be a virtual machine (VDI/VM).

In such cases, once the Python virtual environment with PyMAPDL is already
set and is accessible to all the compute nodes, launching a
PyMAPDL job is very easy to do using ``sbatch`` command.
No changes are needed on a PyMAPDL script to run it on an SLURM cluster.

First the virtual environment must be activated in the current terminal.

.. code-block:: console

    user@entrypoint-machine:~$ export VENV_PATH=/my/path/to/the/venv
    user@entrypoint-machine:~$ source $VENV_PATH/bin/activate

Once the virtual environment has been activated, you can launch any Python
script if they do have the proper Python shebang (``#!/usr/bin/env python3``).

For instance, to launch the following Python script ``main.py``:

.. code-block:: python
    :caption: main.py

    #!/usr/bin/env python3

    from ansys.mapdl.core import launch_mapdl

    mapdl = launch_mapdl(run_location="/home/ubuntu/tmp/tmp/mapdl", loglevel="debug")

    print(mapdl.prep7())
    print(f'Number of CPU: {mapdl.get_value("ACTIVE", 0, "NUMCPU")}')

    mapdl.exit()

You can just run in your console:

.. code-block:: console

    (venv) user@entrypoint-machine:~$ sbatch main.py

Alternatively, you can remove the shebang from the python file and use a
Python executable call:

.. code-block:: console

    (venv) user@entrypoint-machine:~$ sbatch python main.py

Additionally, you can change the amount of cores used in your
job, by setting the :envvar:`PYMAPDL_NPROC` to the desired value.

.. code-block:: console

    (venv) user@entrypoint-machine:~$ PYMAPDL_NPROC=4 sbatch main.py

You can also add ``sbatch`` options to the command:

.. code-block:: console

    (venv) user@entrypoint-machine:~$ PYMAPDL_NPROC=4 sbatch  main.py


For instance, to launch a PyMAPDL job which start a four cores MAPDL instance
on a 10 CPU SLURM job, you can use:

.. code-block:: console

    (venv) user@entrypoint-machine:~$ PYMAPDL_NPROC=4 sbatch --partition=qsmall --nodes=10 --ntasks-per-node=1 main.py


Using a submission script
-------------------------

In case you need to customize more your job, you can create a SLURM
submission script to submit a PyMAPDL job.
In this case, you must create two files:

- Python script with the PyMAPDL code
- Bash script that activates the virtual environment and calls the
  Python script.

.. code-block:: python
    :caption: main.py

    from ansys.mapdl.core import launch_mapdl

    # Number of processors must be lower than the
    # number of CPU allocated for the job.
    mapdl = launch_mapdl(nproc=10)

    mapdl.prep7()
    n_proc = mapdl.get_value("ACTIVE", 0, "NUMCPU")
    print(f"Number of CPU: {n_proc}")

    mapdl.exit()


.. code-block:: bash
   :caption: job.sh

   source /home/user/.venv/bin/activate
   python main.py

To start the simulation, you use this code:

.. code-block:: console

    user@machine:~$ sbatch job.sh

In this case, the Python virtual environment does not need to be activated
before submission since it is activated later in the script.

The expected output of the job is

.. code-block:: text

    Number of CPU: 10.0


The bash script allows you to customize the environment before running the
Python script.
This bash script performs tasks such as creating environment variables,
moving files to different directories, and printing to ensure your
configuration is correct.
