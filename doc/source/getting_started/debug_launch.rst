.. _ref_debug_launching_issues:

Debug launching issues
======================

When MAPDL fails to launch, PyMAPDL usually raises a generic error such as
``MapdlDidNotStart`` or ``LaunchError``. The cause is normally recorded in the
PyMAPDL log and in the files that MAPDL writes to its working directory.
To find it, follow these steps.

Step 1: Record the PyMAPDL log
------------------------------

Write the log at the ``DEBUG`` level to a file *before* calling the
:func:`launch_mapdl() <ansys.mapdl.core.launcher.launch_mapdl>` function:

.. code:: python

    from ansys.mapdl.core import LOG, launch_mapdl

    LOG.setLevel("DEBUG")
    LOG.log_to_file("pymapdl_launch.log")

    mapdl = launch_mapdl(loglevel="DEBUG")

The log contains the resolved configuration (executable file, version, port,
and number of processors), the working directory, and the exact command used
to start MAPDL.

Step 2: Find the working directory
----------------------------------

MAPDL writes its files, including the error and output files, to its working
directory. By default, PyMAPDL creates a new temporary directory for each
launch, named ``ansys_`` followed by a random string, and does not delete it
on exit. You can find it in one of these ways:

* **Set it yourself.** Use the ``run_location`` argument to launch MAPDL in a
  known directory:

  .. code:: python

      import os

      run_location = os.path.join(os.getcwd(), "mapdl_debug")
      mapdl = launch_mapdl(run_location=run_location, loglevel="DEBUG")

  If a previous session ended abnormally, a ``file.lock`` file might block
  the new launch. Delete it, use a new directory, or pass ``override=True``.

* **Read it from the log.** Search for the ``Location:`` entry.
* **Query it from a running session.** Use the
  :attr:`Mapdl.directory <ansys.mapdl.core.Mapdl.directory>` property.
* **Look in the system temporary directory.** Find the most recently modified
  ``ansys_*`` directory.

Step 3: Inspect the files in the working directory
--------------------------------------------------

Some files start with a dot (``.``), so they might be hidden. Use ``ls -a`` on
Linux. The ``file`` prefix is the job name, which you can change with the
``jobname`` argument.

* ``.__tmp__.out`` (Windows only): MAPDL console output. If the launch is
  successful, it contains the ``START GRPC SERVER`` banner described in
  :ref:`ref_debug_pymapdl`. Otherwise, it usually contains the reason for the
  failure, such as licensing or MPI errors.
* ``.__tmp__.inp`` (Windows only): Temporary input file that starts MAPDL in
  batch mode. It contains only the ``FINISH`` command.
* ``file.err`` and ``file0.err``: MAPDL error and warning messages. In
  distributed memory parallel (DMP) mode, each process writes its own file.
* ``file.out`` and ``file0.out``: MAPDL output files.
* ``file.lock``: Lock file that exists while MAPDL is running. If MAPDL is not
  running and the file is present, the previous session ended abnormally.

Search these files for ``*** ERROR ***`` messages. If they contain
``UDS socket file already exists``, see :ref:`ref_uds_socket_file_exists`.

On Linux, PyMAPDL does not write the MAPDL console output to a file by
default. To capture it, use the ``mapdl_output`` argument:

.. code:: python

    mapdl = launch_mapdl(
        run_location="mapdl_debug",
        mapdl_output="mapdl_console_output.txt",
        loglevel="DEBUG",
    )

If the working directory is empty, MAPDL probably failed before it started.
Check the launch command in the next step.

Step 4: Inspect the launch command
----------------------------------

The log shows the exact command in the ``Generated MAPDL command`` and
``Command:`` entries. Check that:

* The executable path exists and points to the expected MAPDL version. If it
  does not, see :ref:`ref_updating_mapdl_installation`.
* The number of processors (``-np``), memory (``-m``), and license type
  (``-p``) are correct.
* The port (``-port``) is not used by another process.
* The ``additional_switches`` argument and the
  :envvar:`PYMAPDL_ADDITIONAL_SWITCHES` environment variable do not conflict.

To reproduce the issue outside PyMAPDL, run the command from the working
directory. The log shows the arguments joined by spaces, without shell
quoting, so you must quote paths that contain spaces:

.. tab-set::

    .. tab-item:: Windows
        :sync: oskey

        In PowerShell, quote the path and use the call operator (``&``):

        .. code:: pwsh-session

            PS C:\Users\user\AppData\Local\Temp\ansys_ymjqvmeyww> & "C:\Program Files\ANSYS Inc\v242\ansys\bin\winx64\ansys242.exe" -j file -np 2 -port 50052 -grpc -b -i .__tmp__.inp -o .__tmp__.out

        In ``cmd.exe``, quote the path only. The ``-i .__tmp__.inp`` argument
        requires that file in the working directory. If it does not exist,
        create it with a single ``FINISH`` line.

    .. tab-item:: Linux
        :sync: oskey

        .. code:: console

            user@machine:/tmp/ansys_ymjqvmeyww$ /usr/ansys_inc/v242/ansys/bin/ansys242 -j file -np 2 -port 50052 -grpc

For more information, see :ref:`ref_testing_mapdl_launching`.

Step 5: Inspect the environment variables
-----------------------------------------

PyMAPDL does not log the environment variables because they might contain
sensitive information. Depending on the arguments of the
:func:`launch_mapdl() <ansys.mapdl.core.launcher.launch_mapdl>` function,
PyMAPDL builds the MAPDL environment in one of these ways:

* **Default, or with the** ``add_env_vars`` **argument:** MAPDL inherits the
  environment of the Python process. PyMAPDL then applies these changes in
  order, so later changes override earlier ones:

  #. On Ubuntu, sets ``I_MPI_SHM_LMT`` to ``shm``.
  #. Sets ``ANS_CMD_NODIAG`` to ``TRUE``.
  #. Adds the variables in ``add_env_vars``, overriding any variable with the
     same name, including the two preceding ones.
  #. With the ``mtls`` transport mode, sets ``ANSYS_GRPC_CERTIFICATES`` to the
     ``certs_dir`` argument. Without it, PyMAPDL keeps the existing value or
     defaults to the ``certs`` directory in the current directory.

* **With the** ``replace_env_vars`` **argument:** MAPDL receives *only* the
  variables in this argument. PyMAPDL does not set any of the preceding
  variables, so you must provide everything MAPDL needs, such as ``PATH`` and
  the license server variables.

To print the environment, working directory, and command without starting
MAPDL, run the following code with the same arguments you pass to the
:func:`launch_mapdl() <ansys.mapdl.core.launcher.launch_mapdl>` function:

.. code:: python

    from ansys.mapdl.core.launcher.config import resolve_launch_config
    from ansys.mapdl.core.launcher.environment import prepare_environment
    from ansys.mapdl.core.launcher.process import _generate_launch_command

    config = resolve_launch_config(nproc=2, run_location="mapdl_debug")

    print("Working directory:", config.run_location)
    print("Command:", " ".join(_generate_launch_command(config)))

    env = prepare_environment(config).variables
    for key, value in sorted(env.items()):
        if key.startswith(("ANS", "AWP", "PYMAPDL", "I_MPI")):
            print(f"{key}={value}")

.. warning::
   These functions are internal to PyMAPDL and might change without notice.
   Use them only for debugging.

Check, in particular, ``ANSYSLMD_LICENSE_FILE`` and ``ANSYSLI_SERVERS``
(see :ref:`ref_licensing_issues`), ``AWP_ROOT<version>``, ``ANSYS_LOCK``,
the ``PYMAPDL_*`` variables, and the ``I_MPI_*`` variables
(see :ref:`ref_mpi_issues`). For more information, see
:ref:`ref_incorrect_env_vars`.

Step 6: Share the information
-----------------------------

If you still cannot identify the issue, open a discussion on the
`PyMAPDL Discussions <pymapdl_discussions_>`_ page or an issue on the
`PyMAPDL Issues <pymapdl_issues_>`_ page. Attach the PyMAPDL log and the
``.__tmp__.out``, ``file*.err``, and ``file*.out`` files.

.. warning::
   Before sharing these files, remove any sensitive information, such as
   license server addresses, usernames, and paths.
