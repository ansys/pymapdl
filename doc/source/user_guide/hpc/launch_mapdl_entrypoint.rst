
.. _ref_pymapdl_interactive_in_cluster_hpc:

.. _ref_pymapdl_interactive_in_cluster_hpc_from_login:


Interactive MAPDL instance launched from the login node
=======================================================

Starting the instance
---------------------

If you are already logged in an login node, it is also
possible to launch an MAPDL instance as an SLURM job and
connect to it.
This can be accomplished running the following commands
in your login node.

.. code:: pycon

    >>> from ansys.mapdl.core import launch_mapdl
    >>> mapdl = launch_mapdl(launch_on_hpc=True)

PyMAPDL submits a job to the scheduler using the appropriate commands.
In case of SLURM, it uses ``sbatch`` command with the ``--wrap`` argument
to pass the MAPDL command line need to start.
Other scheduler arguments can be specified using ``scheduler_args``
argument as a Python :class:`dict`:

.. code:: pycon

    >>> from ansys.mapdl.core import launch_mapdl
    >>> scheduler_args = {"nodes": 10, "ntasks-per-node": 2}
    >>> mapdl = launch_mapdl(launch_on_hpc=True, scheduler_args=scheduler_args)

.. note::
    The double minus (``--``) common in the long version of the SLURM commands
    is added automatically if PyMAPDL detects it is missing and the specified
    command is long (length more than 1).
    For instance ``ntasks-per-node`` argument is submitted as ``--ntasks-per-node``.

or as a single Python string (:class:`str`):

.. code:: pycon

    >>> from ansys.mapdl.core import launch_mapdl
    >>> scheduler_args = "-N 10"
    >>> mapdl = launch_mapdl(launch_on_hpc=True, scheduler_args=scheduler_args)

.. warning::
    Because PyMAPDL is already using the ``--wrap`` argument, this argument
    cannot be used again.

The values of each scheduler argument are wrapped with single quotes (`'`).
This might cause parsing issues which can cause the job to fail after successful
submission.

It should be noticed also that PyMAPDL passes all the environment variables of the
user to the new job and to the MAPDL instance.
This is normally convenient, since there are many environmental variables which are
needed to run the job or MAPDL.
For instance the license server is normally stored in :envvar:`ANSYSLMD_LICENSE_FILE` environment variable.
If you prefer not to pass these environment variables to the job, use the SLURM argument
``--export`` to specify the desired environment variables.
For more information, see `SLURM documentation <slurm_docs_>`_.


Working with the instance
-------------------------

Once the :class:`Mapdl <ansys.mapdl.core.mapdl.MapdlBase>` object has been created,
there are no differences with a normal :class:`Mapdl <ansys.mapdl.core.mapdl.MapdlBase>`
instance.
You can retrieve the IP of the MAPDL instance, as well as its hostname.

.. code:: pycon

    >>> mapdl.ip
    '123.45.67.89'
    >>> mapdl.hostname
    'node0'

You can also retrieve the job ID:

.. code:: pycon

    >>> mapdl.jobid
    10001

If you want to check whether the instance has been launched using an scheduler,
you can use :attr:`mapdl_on_hpc <ansys.mapdl.core.mapdl_grpc.MapdlGrpc.mapdl_on_hpc>`

.. code:: pycon

    >>> mapdl.mapdl_on_hpc
    True


Sharing files
^^^^^^^^^^^^^

Most of the HPC cluster share the login node filesystem with the compute nodes,
meaning you do not need to do extra work to upload or download files to the MAPDL
instance, you just need to copy them to the location where MAPDL is running.
This location can be obtained with
:attr:`directory <ansys.mapdl.core.mapdl_grpc.MapdlGrpc.directory>`.

If no location is specified in :func:`launch_mapdl() <ansys.mapdl.core.launcher.launch_mapdl>`,
then a temporal location is selected.
It is a good idea to set the ``run_location`` argument to a directory that is accessible
from all the compute nodes.
Normally anything under ``/home/user`` is available to all compute nodes.
In case you are unsure where you should launch MAPDL, contact your cluster administrator.

Additionally, you can use methods like :meth:`upload <ansys.mapdl.core.mapdl_grpc.MapdlGrpc.upload>`
or :meth:`download <ansys.mapdl.core.mapdl_grpc.MapdlGrpc.download>` to
upload or download files to/from the MAPDL instance respectively.
You do not need other connection like ``ssh`` or similar.
However, for large files, you might want to consider other alternatives.


Exiting MAPDL
-------------

Exiting MAPDL, either intentionally or unintentionally, stop the job.
This behaviour is because MAPDL is the main process at the job, hence when finished
the scheduler considers the job done.

To exit MAPDL, you can use :meth:`exit() <ansys.mapdl.core.Mapdl.exit>` method.
This method exit MAPDL and, additionally, it send a signal to the scheduler to cancel the job.

.. code-block:: python

    mapdl.exit()

When the Python process you are running PyMAPDL on finishes without errors, and you have not
issued :meth:`exit() <ansys.mapdl.core.Mapdl.exit>`, the garbage collector
kills the MAPDL instance and its job. This is intended to save resources.

If you prefer that the job is not killed, set the following attribute in the
:class:`Mapdl <ansys.mapdl.core.mapdl.MapdlBase>` class:

.. code-block:: python

    mapdl.finish_job_on_exit = False


In that case, it is recommended you set a timeout in your job to avoid having the job
running more than needed.


Handling crashes on an HPC
^^^^^^^^^^^^^^^^^^^^^^^^^^

If MAPDL crashes while running on HPC, the job finishes right away.
In that case, MAPDL disconnect from MAPDL.
PyMAPDL retries to reconnect to the MAPDL instance up to 5 times waiting for up to 5s.
If unsuccessful, you might get an error like this:

.. code-block:: text

    MAPDL server connection terminated unexpectedly while running:
    /INQUIRE,,DIRECTORY,,
    called by:
    _send_command

    Suggestions:
    MAPDL *might* have died because it executed a not-allowed command or ran out of memory.
    Check the MAPDL command output for more details.
    Open an issue on GitHub if you need assistance: https://github.com/ansys/pymapdl/issues
    Error:
    failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50052: Failed to connect to remote host: connect: Connection refused (111)
    Full error:
    <_InactiveRpcError of RPC that terminated with:
    status = StatusCode.UNAVAILABLE
    details = "failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50052: Failed to connect to remote host: connect: Connection refused (111)"
    debug_error_string = "UNKNOWN:Error received from peer  {created_time:"2024-10-24T08:25:04.054559811+00:00", grpc_status:14, grpc_message:"failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50052: Failed to connect to remote host: connect: Connection refused (111)"}"
    >

The data of that job is available at :attr:`directory <ansys.mapdl.core.Mapdl.directory>`.
It is recommended you set the run location using ``run_location`` argument.

While handling this exception, PyMAPDL also cancels the job to avoid resources leaking.
Therefore, the only option is to start a new instance by launching a new job using
:func:`launch_mapdl() <ansys.mapdl.core.launcher.launch_mapdl>`.

User case on a SLURM cluster
----------------------------

Assume an user wants to start a remote MAPDL instance in a HPC cluster
to interact with it.

The user would like to request 10 nodes, and 1 task per node (to avoid clashes
between MAPDL instances). He would like to also request 64 GB of memory RAM.
Because of administration logistic, he must use the machines in `Keros` partition.

To make PyMAPDL to launch an instance like that on SLURM, run the following code:

.. code-block:: python

    from ansys.mapdl.core import launch_mapdl
    from ansys.mapdl.core.examples import vmfiles

    scheduler_args = {"nodes": 10, "ntasks-per-node": 1, "partition": "keros", "memory": 64}
    mapdl = launch_mapdl(launch_on_hpc=True, scheduler_args=scheduler_args)

    num_cpu = mapdl.get_value("ACTIVE", 0, "NUMCPU")  # It should be equal to 10

    mapdl.clear()  # Not strictly needed.
    mapdl.prep7()

    # Run an MAPDL script
    mapdl.input(vmfiles["vm1"])

    # Let's solve again to get the solve printout
    mapdl.solution()
    output = mapdl.solve()
    print(output)

    mapdl.exit()  # Kill the MAPDL instance


PyMAPDL automatically sets MAPDL to read the job configuration (machines, number
of cpus, memory, etc) which allows MAPDL to use all the resources allocated
to that job.
