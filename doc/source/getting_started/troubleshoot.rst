.. _ref_troubleshooting:


Troubleshooting PyMAPDL
=======================


This page covers common problems and frequently asked questions that you might
encounter when using PyMAPDL.

.. _ref_debug_pymapdl:

Debug PyMAPDL
-------------

If you are having trouble with PyMAPDL, you can record internal logs to a file
using a logger. Examine this file to identify issues.

Also, set the ``run_location`` argument to a known location, such as the current directory,
so that you can find MAPDL log files more easily.

To set the logger output file to ``mylog.log``, run the following commands in a
Python terminal or at the beginning of your script:

.. code:: python

    import os
    from ansys.mapdl.core import LOG

    LOG.setLevel("DEBUG")
    LOG.log_to_file("mylog.log")

    from ansys.mapdl.core import launch_mapdl

    # Using current directory as ``run_location``
    mapdl = launch_mapdl(run_location=os.getcwd(), loglevel="DEBUG")


If you know the location of the executable file, you can set it
as the first parameter of the :func:`launch_mapdl() <ansys.mapdl.core.launcher.launch_mapdl>` function.

.. code:: python

    from ansys.mapdl.core import launch_mapdl

    exec_loc = "C:/Program Files/ANSYS Inc/v241/ansys/bin/winx64/ANSYS241.exe"
    mapdl = launch_mapdl(exec_loc, run_location=os.getcwd(), loglevel="DEBUG")

If you do not specify the location of the executable file, PyMAPDL uses the default location.

.. note:: If MAPDL launches when you specify the location of the executable file but not when you don't specify it,
   the cached executable location is likely outdated. To update it, see :ref:`ref_updating_mapdl_location`.

If MAPDL is not launching, check the content of log files in the current directory
(specified using ``run_location``) for more information on the issue.
The main MAPDL log file is ``.__tmp__.out``. This is the output file specified in the command line.
If the launching is successful, it should show:

.. code-block:: text

   Start GRPC Server

   ##############################
   ### START GRPC SERVER      ###
   ##############################

   Server Executable   : MapdlGrpc Server
   Server listening on : 0.0.0.0:50052

Or, from Ansys MAPDL 2026R1, it should show:

.. code-block:: text

   ################################################
   #####    *INSECURE* GRPC SERVER STARTED    #####
   ################################################
   Transport Mode           : INSECURE
   Server Executable        : MapdlGrpc.Server
   Server listening on      : 0.0.0.0:50052
   Allow remote connections : True

    Press Ctrl-C to stop the server...


Additionally, MAPDL generates other files such as ``file1.out``, ``file1.err``, and ``file1.log``
that can be useful to identify the issue.

The main logger file ``LOG`` (in the example, recorded to ``my_log.log``) also provides
valuable information about startup.
Here is an extract:

.. code-block:: text

   DEBUG - pymapdl_global -  config - resolve_run_location - Created temporary run location: C:\Users\user\AppData\Local\Temp\ansys_ymjqvmeyww
   DEBUG - pymapdl_global -  config - resolve_port - Using default port: 50052
   INFO - pymapdl_global -  __init__ - _launch_mapdl_common - Launching MAPDL locally...
   DEBUG - pymapdl_global -  process - _generate_launch_command - Generated MAPDL command: C:\Program Files\ANSYS Inc\v242\ansys\bin\winx64\ansys242.exe -j file -np 2 -port 50052 -grpc -b -i .__tmp__.inp -o .__tmp__.out
   DEBUG - pymapdl_global -  process - _create_temp_input_file - Created temporary input file: C:\Users\user\AppData\Local\Temp\ansys_ymjqvmeyww\.__tmp__.inp
   INFO - pymapdl_global -  process - _start_subprocess -
   ============
   Running MAPDL instance
   Location: C:\Users\user\AppData\Local\Temp\ansys_ymjqvmeyww
   Command: C:\Program Files\ANSYS Inc\v242\ansys\bin\winx64\ansys242.exe -j file -np 2 -port 50052 -grpc -b -i .__tmp__.inp -o .__tmp__.out
   ============
   DEBUG - pymapdl_global -  process - _start_subprocess - MAPDL process started with PID: 12345

From the preceding information, you can extract the launch location (``C:\Users\user\AppData\Local\Temp\ansys_ymjqvmeyww``)
and the command used (``C:\Program Files\ANSYS Inc\v242\ansys\bin\winx64\ansys242.exe -j file -np 2 -port 50052 -grpc -b -i .__tmp__.inp -o .__tmp__.out``).
This information can also help you find the MAPDL logs or the cause of the issue.
For a step-by-step procedure, see :ref:`ref_debug_launching_issues`.

If MAPDL still does not launch, see `Launching issues`_ for more information on
common issues and their solutions.

If after examining all the log files you cannot identify the issue, open a
discussion on the `PyMAPDL Discussions <pymapdl_discussions_>`_ page.
If you believe you have found a bug, create an issue on the `PyMAPDL Issues <pymapdl_issues_>`_ page.
You can attach the log file to the bug report for further investigation.


.. _ref_launching_issue:

Launching issues
----------------

There are several issues that can cause MAPDL not to launch, including:

- `Debug launching issues`_
- `Error: UDS socket file already exists`_
- `Connection timeout`_
- `Testing MAPDL launching`_
- `Licensing issues`_
- `Virtual private network (VPN) issues`_
- `Missing dependencies on Linux`_
- `Conflicts with student version`_
- `Incorrect environment variables`_
- `Using a proxy server`_
- `Firewall settings`_

If you cannot find your issue, see `More help needed?`_.


.. _ref_debug_launching_issues:

Debug launching issues
~~~~~~~~~~~~~~~~~~~~~~

When MAPDL fails to launch, PyMAPDL usually raises a generic error such as
``MapdlDidNotStart`` or ``LaunchError``. The actual cause is normally recorded
in the PyMAPDL log and in the files that MAPDL writes to its working directory.
To find it, follow these steps.

**Step 1: Record the PyMAPDL log**

Enable the global logger at the ``DEBUG`` level and write it to a file
*before* calling the :func:`launch_mapdl() <ansys.mapdl.core.launcher.launch_mapdl>`
function:

.. code:: python

    from ansys.mapdl.core import LOG

    LOG.setLevel("DEBUG")
    LOG.log_to_file("pymapdl_launch.log")  # Write log to a file
    LOG.log_to_stdout()  # Optional: also print the log to the console

    from ansys.mapdl.core import launch_mapdl

    mapdl = launch_mapdl(loglevel="DEBUG")

The ``pymapdl_launch.log`` file contains, among other information, the
resolved configuration (executable file, version, port, IP address, and
number of processors), the working directory, and the exact command used to
start MAPDL.

**Step 2: Get the MAPDL working directory**

MAPDL writes all its files, including the error and output files, to its
working directory. By default, PyMAPDL creates a new temporary directory
for each launch. This directory is located in the system temporary directory
and its name starts with ``ansys_`` followed by a random string, for example
``C:\Users\user\AppData\Local\Temp\ansys_ymjqvmeyww`` on Windows or
``/tmp/ansys_ymjqvmeyww`` on Linux.

You can get the working directory in several ways:

* **Set it yourself.** This is the easiest approach. Use the ``run_location``
  argument to launch MAPDL in a known directory. If the directory doesn't
  exist, PyMAPDL creates it.

  .. code:: python

      import os
      from ansys.mapdl.core import launch_mapdl

      run_location = os.path.join(os.getcwd(), "mapdl_debug")
      mapdl = launch_mapdl(run_location=run_location, loglevel="DEBUG")

  .. note::
     If a previous MAPDL session in the same directory ended abnormally, a
     ``file.lock`` file might block the new launch. Delete it, use a new
     directory, or pass ``override=True`` to the
     :func:`launch_mapdl() <ansys.mapdl.core.launcher.launch_mapdl>` function.

* **Read it from the PyMAPDL log.** Search the log file for the
  ``Created temporary run location`` or ``Location:`` entries:

  .. code-block:: text

     DEBUG - pymapdl_global -  config - resolve_run_location - Created temporary run location: C:\Users\user\AppData\Local\Temp\ansys_ymjqvmeyww
     ...
     INFO - pymapdl_global -  process - _start_subprocess -
     ============
     Running MAPDL instance
     Location: C:\Users\user\AppData\Local\Temp\ansys_ymjqvmeyww
     Command: C:\Program Files\ANSYS Inc\v242\ansys\bin\winx64\ansys242.exe -j file -np 2 -port 50052 -grpc -b -i .__tmp__.inp -o .__tmp__.out
     ============

* **Query it from a running session.** If MAPDL launches but misbehaves
  afterwards, use the :attr:`Mapdl.directory <ansys.mapdl.core.Mapdl.directory>`
  property:

  .. code:: pycon

      >>> print(mapdl.directory)
      C:\Users\user\AppData\Local\Temp\ansys_ymjqvmeyww

* **Look in the system temporary directory.** If you did not record the log,
  find the most recently modified ``ansys_*`` directory in the system
  temporary directory:

  .. code:: python

      import glob
      import os
      import tempfile

      dirs = glob.glob(os.path.join(tempfile.gettempdir(), "ansys_*"))
      print(max(dirs, key=os.path.getmtime))

By default, PyMAPDL does not delete the temporary working directory when
MAPDL exits (``remove_temp_dir_on_exit=False``), so its content is still
available after a failed launch.

**Step 3: Inspect the files in the working directory**

Open the working directory with your file explorer (File Explorer on Windows
or your file manager on Linux) or a terminal.
Some of the files start with a dot (``.``), so they might be hidden.
On Linux, press :kbd:`Ctrl+H` in most file managers or use ``ls -a`` in a
terminal to show them.

These files are the most useful ones for debugging. The ``file`` prefix is the
job name, which you can change with the ``jobname`` argument.

* ``.__tmp__.out`` (Windows only): MAPDL console output. If the launch is
  successful, it contains the ``START GRPC SERVER`` banner described in
  :ref:`ref_debug_pymapdl`. Otherwise, it usually contains the reason for the
  failure, such as licensing or MPI errors.
* ``.__tmp__.inp`` (Windows only): Temporary input file that PyMAPDL creates
  to start MAPDL in batch mode. It contains only the ``FINISH`` command.
* ``file.err`` and ``file0.err``: MAPDL error and warning messages. In
  distributed memory parallel (DMP) mode, each process writes its own file
  (``file0.err``, ``file1.err``, and so on).
* ``file.out`` and ``file0.out``: MAPDL output files.
* ``file.log``: APDL commands that MAPDL has run.
* ``file.lock``: Lock file that MAPDL creates while it is running. If MAPDL
  is not running and this file is still present, the previous session ended
  abnormally.

Search these files for ``*** ERROR ***`` messages. For example, if the output
files contain ``UDS socket file already exists``, see
:ref:`ref_uds_socket_file_exists`.

On Linux, PyMAPDL does not write the MAPDL console output to a file by
default. To capture it, use the ``mapdl_output`` argument:

.. code:: python

    from ansys.mapdl.core import launch_mapdl

    mapdl = launch_mapdl(
        run_location="mapdl_debug",
        mapdl_output="mapdl_console_output.txt",
        loglevel="DEBUG",
    )

If the working directory is empty or does not exist, MAPDL probably failed
before it could start. In this case, check the executable path and the
launch command, as described in the following step.

**Step 4: Inspect the launch command**

The PyMAPDL log shows the exact command that PyMAPDL uses to start MAPDL in the
``Generated MAPDL command`` and ``Command:`` entries:

.. code-block:: text

   DEBUG - pymapdl_global -  process - _generate_launch_command - Generated MAPDL command: /usr/ansys_inc/v242/ansys/bin/ansys242 -j file -np 2 -port 50052 -grpc

Check that:

* The executable path exists and points to the expected MAPDL version.
  If it does not, see :ref:`ref_updating_mapdl_installation`.
* The number of processors (``-np``), memory (``-m``), and license type
  (``-p``) are correct.
* The port (``-port``) is not used by another process.
* The switches from the ``additional_switches`` argument and from the
  :envvar:`PYMAPDL_ADDITIONAL_SWITCHES` environment variable are correct and do
  not conflict.

To reproduce the issue outside PyMAPDL, open a terminal in the working
directory and run the command there. The log shows the command arguments
joined by spaces, without any shell quoting. If the executable path or any
argument contains spaces, such as ``C:\Program Files\ANSYS Inc``, you must
quote it before running the command:

.. tab-set::

    .. tab-item:: Windows
        :sync: oskey

        In PowerShell, quote the executable path and use the call operator
        (``&``) to run it:

        .. code:: pwsh-session

            PS C:\Users\user\AppData\Local\Temp\ansys_ymjqvmeyww> & "C:\Program Files\ANSYS Inc\v242\ansys\bin\winx64\ansys242.exe" -j file -np 2 -port 50052 -grpc -b -i .__tmp__.inp -o .__tmp__.out

        In the Command Prompt (``cmd.exe``), quote the executable path only:

        .. code:: text

            C:\Users\user\AppData\Local\Temp\ansys_ymjqvmeyww> "C:\Program Files\ANSYS Inc\v242\ansys\bin\winx64\ansys242.exe" -j file -np 2 -port 50052 -grpc -b -i .__tmp__.inp -o .__tmp__.out

        The ``-i .__tmp__.inp`` argument requires the ``.__tmp__.inp`` file
        in the working directory. If the file does not exist, create it with
        a single ``FINISH`` line.

    .. tab-item:: Linux
        :sync: oskey

        .. code:: console

            user@machine:/tmp/ansys_ymjqvmeyww$ /usr/ansys_inc/v242/ansys/bin/ansys242 -j file -np 2 -port 50052 -grpc

        If the path contains spaces, enclose it in quotes.

For more information, see `Testing MAPDL launching`_.

**Step 5: Inspect the environment variables**

PyMAPDL does not write the environment variables to the log because they
might contain sensitive information. PyMAPDL builds the MAPDL environment
in one of these ways, depending on the arguments of the
:func:`launch_mapdl() <ansys.mapdl.core.launcher.launch_mapdl>` function:

* **Default, or with the** ``add_env_vars`` **argument:** MAPDL inherits the
  environment of the Python process. PyMAPDL then applies these changes in
  order, so later changes override earlier ones:

  #. On Ubuntu, sets ``I_MPI_SHM_LMT`` to ``shm``.
  #. Sets ``ANS_CMD_NODIAG`` to ``TRUE``.
  #. Adds the variables in the ``add_env_vars`` argument. These variables
     override any existing variables with the same name, including
     ``I_MPI_SHM_LMT`` and ``ANS_CMD_NODIAG``.
  #. With the ``mtls`` transport mode, sets ``ANSYS_GRPC_CERTIFICATES`` to the
     ``certs_dir`` argument. If you do not provide the ``certs_dir`` argument,
     PyMAPDL keeps the existing value or defaults it to the ``certs`` directory
     in the current directory.

* **With the** ``replace_env_vars`` **argument:** MAPDL receives *only* the
  variables in this argument. PyMAPDL does not inherit the environment of the
  Python process and does not set ``I_MPI_SHM_LMT``, ``ANS_CMD_NODIAG``, or
  ``ANSYS_GRPC_CERTIFICATES``. You must provide all the variables that MAPDL
  needs, such as ``PATH`` and the license server variables.

In both cases, if you use the ``uds`` transport mode on Linux and provide the
``uds_dir`` argument, PyMAPDL sets :envvar:`ANSYS_MAPDL_UDS_PATH` to that
directory unless the variable is already set.

To inspect the environment variables that MAPDL receives, together with the
working directory and the launch command, run the following code. It
reproduces the configuration steps of the
:func:`launch_mapdl() <ansys.mapdl.core.launcher.launch_mapdl>` function
without starting MAPDL. Pass the same arguments that you pass to the
:func:`launch_mapdl() <ansys.mapdl.core.launcher.launch_mapdl>` function.

.. code:: python

    from ansys.mapdl.core.launcher.config import resolve_launch_config
    from ansys.mapdl.core.launcher.environment import prepare_environment
    from ansys.mapdl.core.launcher.process import _generate_launch_command

    # Use the same arguments as in ``launch_mapdl()``
    config = resolve_launch_config(nproc=2)

    print("Working directory:", config.run_location)
    print("Command:", " ".join(_generate_launch_command(config)))

    env = prepare_environment(config).variables
    for key, value in sorted(env.items()):
        if key.startswith(("ANS", "AWP", "PYMAPDL", "I_MPI")):
            print(f"{key}={value}")

.. warning::
   These functions are internal to PyMAPDL and might change without notice.
   Use them only for debugging.

Check, in particular, these variables:

* ``ANSYSLMD_LICENSE_FILE`` and ``ANSYSLI_SERVERS``: License server
  configuration. See `Licensing issues`_.
* ``AWP_ROOT<version>`` and ``ANSYS<version>_DIR``: Ansys installation
  directories, for example ``AWP_ROOT242`` and ``ANSYS242_DIR``.
* ``ANSYS_LOCK``: Lock file behavior.
* ``PYMAPDL_*`` variables, such as :envvar:`PYMAPDL_START_INSTANCE`,
  :envvar:`PYMAPDL_PORT`, :envvar:`PYMAPDL_IP`, and
  :envvar:`PYMAPDL_MAPDL_EXEC`, which change the default launch configuration.
* MPI-related variables, such as ``I_MPI_*``. See
  `Message Passing Interface (MPI) issues`_.

For more information, see `Incorrect environment variables`_.

**Step 6: Share the information**

If you still cannot identify the issue, open a discussion on the
`PyMAPDL Discussions <pymapdl_discussions_>`_ page or an issue on the
`PyMAPDL Issues <pymapdl_issues_>`_ page. Attach the PyMAPDL log file
and the ``.__tmp__.out``, ``file*.err``, and ``file*.out`` files from the
working directory.

.. warning::
   Before sharing these files, remove any sensitive information, such as
   license server addresses, usernames, and paths.


.. _ref_uds_socket_file_exists:

Error: UDS socket file already exists
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

On Linux, MAPDL can use a Unix Domain Socket (UDS) file instead of a TCP
port to communicate with PyMAPDL. MAPDL creates this file in the UDS directory
and names it ``mapdl-<PORT>.sock``, where ``<PORT>`` is the port number. The
default UDS directory is ``~/.conn``. To change the UDS directory, use the
``uds_dir`` argument of the
:func:`launch_mapdl() <ansys.mapdl.core.launcher.launch_mapdl>` function or the
:envvar:`ANSYS_MAPDL_UDS_PATH` environment variable.

If MAPDL does not launch and its output files (``.__tmp__.out``, ``file*.out``,
or the file set with the ``mapdl_output`` argument) contain an error like
this one:

.. code-block:: text

   *** ERROR ***                           ELAPSED TIME =       8.394   TIME= 11:01:03
   UDS socket file already exists at /home/user/.conn/mapdl-50052.sock.
      Another server may already be running on this socket.  Please try
   again to start the server with a different file name by changing the
   port option.

The socket file for that port already exists in the UDS directory. This
happens when either of these conditions is true:

* Another MAPDL instance is running and using that socket file.
* A previous MAPDL instance crashed or was terminated abnormally and left the
  socket file behind.

To check whether a process is using the socket file, run this command:

.. code:: console

    user@machine:~$ lsof ~/.conn/mapdl-50052.sock

If the command does not print anything, no process is using the file.

To solve the issue, use one of these approaches:

* **Delete the socket file.** Do this only if you are certain that no MAPDL
  instance is running or using that file:

  .. code:: console

      user@machine:~$ rm ~/.conn/mapdl-50052.sock

* **Use a different port.** Because the socket filename includes the port
  number, MAPDL creates a new socket file, ``mapdl-<PORT>.sock``, that does not
  conflict with the existing one:

  .. code:: python

      from ansys.mapdl.core import launch_mapdl

      mapdl = launch_mapdl(port=50053)  # Uses ``~/.conn/mapdl-50053.sock``


.. _ref_updating_mapdl_installation:

Updating MAPDL installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~

When you update or reinstall MAPDL, PyMAPDL may still reference the old installation path
because it caches the location of the MAPDL executable.
If you uninstall MAPDL and install a new version (or move the installation), PyMAPDL might fail
to launch MAPDL due to the outdated cached path.

To resolve this, update the cached executable location as described in
:ref:`ref_default_location_executable`.
Use the :func:`save_ansys_path() <ansys.mapdl.core.save_ansys_path>` function to set the correct path to your new MAPDL installation.
This ensures PyMAPDL can find and launch the updated MAPDL version.


Connection timeout
~~~~~~~~~~~~~~~~~~

In some networks, MAPDL might take longer than expected to connect to the license server or to the remote instance.
In those cases, you might see this message:


.. code:: output

    PyMAPDL is taking longer than expected to connect to an MAPDL session. Checking if there are any available licenses...


To increase the starting timeout, use:

.. code:: python

    from ansys.mapdl.core import launch_mapdl

    mapdl = launch_mapdl(start_timeout=60)

If you are connecting to a remote instance, use:

.. code:: python

    from ansys.mapdl.core import Mapdl

    mapdl = Mapdl(timeout=60)


Testing MAPDL launching
~~~~~~~~~~~~~~~~~~~~~~~

In some cases, it may be necessary to run the launch command manually from the command line.


.. tab-set::

    .. tab-item:: Windows
        :sync: oskey

        Open a command prompt and run the version-dependent command:

        .. code:: pwsh-session

            (.venv) PS C:\Users\user\pymapdl> "C:\Program Files\ANSYS Inc\v241\ansys\bin\winx64\ANSYS241.exe"

        .. note:: PowerShell users can run the preceding command without quotes.

    .. tab-item:: Linux
        :sync: oskey

        Run the version-dependent command:

        .. code:: console

            (.venv) user@machine:~$ /usr/ansys_inc/v241/ansys/bin/ansys241


You should start MAPDL in a temporary working directory because MAPDL creates
several temporary files.

You can specify a directory by launching MAPDL from the temporary directory:


.. tab-set::

    .. tab-item:: Windows
        :sync: oskey

        .. code:: pwsh-session

            (.venv) PS C:\Users\user\pymapdl> mkdir temporary_directory
            (.venv) PS C:\Users\user\pymapdl> cd temporary_directory
            (.venv) PS C:\Users\user\pymapdl> & 'C:\Program Files\ANSYS Inc\v241\ansys\bin\winx64\ANSYS241.exe'

        Or, you can specify the directory using the ``-dir`` flag:

        .. code:: pwsh-session

            (.venv) PS C:\Users\user\pymapdl> mkdir temporary_directory
            (.venv) PS C:\Users\user\pymapdl> & 'C:\Program Files\ANSYS Inc\v241\ansys\bin\winx64\ANSYS241.exe' -dir "C:\ansys_job\mytest1"


    .. tab-item:: Linux
        :sync: oskey

        .. code:: console

            (.venv) user@machine:~$ mkdir temporary_directory
            (.venv) user@machine:~$ cd temporary_directory
            (.venv) user@machine: temporary_directory $ /usr/ansys_inc/v241/ansys/bin/ansys241

        Or, you can specify the directory using the ``-dir`` flag:

        .. code:: pwsh-session

            (.venv) PS C:\Users\user\pymapdl> mkdir /tmp/ansys_tmp/job1
            (.venv) PS C:\Users\user\pymapdl> /usr/ansys_inc/v241/ansys/bin/ansys241 -dir /tmp/ansys_tmp/job1


If this command doesn't launch MAPDL, look at the command output:

.. vale off

.. tab-set::

    .. tab-item:: Windows
        :sync: oskey

        .. code:: pwsh-session

            (.venv) PS C:\Users\user\pymapdl> & 'C:\Program Files\ANSYS Inc\v241\ansys\bin\winx64\ANSYS241.exe'
            *** ERROR ***
            Another Ansys job with the same job name (file) is already running in this
            directory or the file.lock file has not been deleted from an abnormally
            terminated Ansys run. To disable this check, set the ANSYS_LOCK environment
            variable to OFF.

    .. tab-item:: Linux
        :sync: oskey

        .. code:: console

            (.venv) user@machine:~$ /usr/ansys_inc/v241/ansys/bin/ansys241
            *** ERROR ***
            Another Ansys job with the same job name (file) is already running in this
            directory or the file.lock file has not been deleted from an abnormally
            terminated Ansys run. To disable this check, set the ANSYS_LOCK environment
            variable to OFF.

.. vale on


Message Passing Interface (MPI) issues
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you are using a distributed memory parallel (DMP) version of MAPDL, you might
experience issues with the Message Passing Interface (MPI) communication libraries when running on AMD processors.
By default, MAPDL uses OpenMPI as the MPI implementation when running on AMD processors.
If OpenMPI has not been installed, or if you are trying to use IntelMPI on AMD processors, you might see an error similar to the following:

.. code:: text

    line 430: mpirun: command not found


To make sure you are using OpenMPI, pass the ``-mpi openmpi`` option to the :func:`launch_mapdl() <ansys.mapdl.core.launcher.launch_mapdl>` function.

.. code:: python

    from ansys.mapdl.core import launch_mapdl

    mapdl = launch_mapdl(additional_switches="-mpi openmpi")

You can also run MAPDL in shared memory parallel (SMP) mode by passing the ``-smp`` option.

.. code:: python

    from ansys.mapdl.core import launch_mapdl

    mapdl = launch_mapdl(additional_switches="-smp")


See also :ref:`vpn_issues_troubleshooting` for incompatibilities between the VPN and the MPI communication.


Licensing issues
~~~~~~~~~~~~~~~~

Incorrect license server configuration can prevent MAPDL from being able to get a valid license.
In such cases, if you try to start MAPDL from the command line you might see an output **similar** to:


.. tab-set::

    .. tab-item:: Windows
        :sync: oskey

        .. code:: pwsh-session

            (.venv) PS C:\Users\user\pymapdl> & 'C:\Program Files\ANSYS Inc\v241\ansys\bin\winx64\ANSYS241.exe'

            ANSYS LICENSE MANAGER ERROR:

            Maximum licensed number of demo users already reached.


            ANSYS LICENSE MANAGER ERROR:

            Request name mech_2 does not exist in the licensing pool.
            No such feature exists.
            Feature:          mech_2
            License path:  C:\Users\user\AppData\Local\Temp\\cb0400ba-6edb-4bb9-a333-41e7318c007d;
            FlexNet Licensing error:-5,357

    .. tab-item:: Linux
        :sync: oskey

        .. code:: console

            (.venv) user@machine:~$ /usr/ansys_inc/v241/ansys/bin/ansys241

            ANSYS LICENSE MANAGER ERROR:

            Maximum licensed number of demo users already reached.


            ANSYS LICENSE MANAGER ERROR:

            Request name mech_2 does not exist in the licensing pool.
            No such feature exists.
            Feature:          mech_2
            FlexNet Licensing error:-5,357


Not enough licenses are available to start MAPDL.
In this case, contact your Ansys license administrator at your organization.

If you are responsible for maintaining Ansys licensing or have a personal installation of Ansys, see the
`Ansys Installation and Licensing documentation <ansys_installation_and_licensing_>`_.
If you cannot find the information you need, open a customer request ticket.

For an example blog post on licensing issues at ANSYS 2020R1, see `Changes to Licensing at ANSYS 2020R1 <padt_licensing_>`_.


Incorrect licensing environment variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The license server can be also specified using the environment variable :envvar:`ANSYSLMD_LICENSE_FILE`.
The following code examples show how you can see the value of this environment variable on
either Windows or Linux.


.. tab-set::

    .. tab-item:: Windows
        :sync: oskey

        .. code:: pwsh-session

            (.venv) PS C:\Users\user\pymapdl> $env:ANSYSLMD_LICENSE_FILE
            1055@1.1.1.1

    .. tab-item:: Linux
        :sync: oskey

        .. code:: console

            (.venv) user@machine:~$ printenv | grep ANSYSLMD_LICENSE_FILE
            1055@1.1.1.1


.. _vpn_issues_troubleshooting:

Virtual private network (VPN) issues
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

From Ansys 2021 R1 to Ansys 2022 R2, MAPDL has issues launching when VPN software is running.
One issue stems from MPI communication. You can work around it by either:

- Passing the ``-smp`` option to set the execution mode to `Shared Memory Parallel`,
  which disables the default `Distributed Memory Parallel`.
- Using a different MPI library. For example, on Windows, pass ``-mpi msmpi`` to use
  the Microsoft MPI library instead of the default Intel MPI library.

This issue does not affect the Linux version of MAPDL.

.. note:: If you are using Windows in any of the versions from Ansys 2021 R1 to Ansys 2022 R2,
   the default MPI library is Microsoft MPI when the MAPDL instance is launched by PyMAPDL.

.. code:: pycon

    >>> from ansys.mapdl.core import launch_mapdl
    >>> mapdl = launch_mapdl(additional_switches="-smp")

While this approach has the disadvantage of using the potentially slower shared
memory parallel mode, you can still run MAPDL.
For more information on shared versus distributed memory, see
`High-Performance Computing for Mechanical Simulations using ANSYS <ansys_parallel_computing_guide_>`_.


In addition, if your device is connected to a VPN, MAPDL might not be able to correctly
resolve the IP of the license server. Verify that the hostname or IP address of the license server
is correct.

On Windows, you can find the license configuration file that points to the license server in ``C:\Program Files\ANSYS Inc\Shared Files\Licensing\ansyslmd.ini``.


.. _missing_dependencies_on_linux:

Missing dependencies on Linux
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Some Linux installations might be missing required dependencies. If
you get errors like ``libXp.so.6: cannot open shared object file: No
such file or directory``, you are likely missing some necessary
dependencies.


.. tab-set::

    .. tab-item:: CentOS 7 and Rocky 8

        On CentOS 7, you can install missing dependencies with:

        .. code:: console

            user@machine:~$  yum install openssl openssh-clients mesa-libGL mesa-libGLU motif libgfortran

    .. tab-item:: Ubuntu 22.04

        On Ubuntu 22.04, use this code to install the needed dependencies:

        .. code:: console

            user@machine:~$ apt-get update

            # Install dependencies
            user@machine:~$ apt-get install -y \
                openssh-client \
                libgl1 \
                libglu1 \
                libxm4 \
                libxi6

        The preceding code takes care of everything except for ``libxp6``, which you must install
        using this code:

        .. code:: console

            # This is a workaround
            # Source: https://bugs.launchpad.net/ubuntu/+source/libxp/+bug/1517884
            user@machine:~$ apt install -y software-properties-common
            user@machine:~$ add-apt-repository -y ppa:zeehio/libxp
            user@machine:~$ apt-get update
            user@machine:~$ apt-get install -y libxp6

    .. tab-item:: Ubuntu 20.04 through 18.04

        If you are using Ubuntu 20.04 through 18.04, you can install missing dependencies with:

        .. code:: console

            user@machine:~$ apt-get update

            # Install dependencies
            user@machine:~$ apt-get install -y \
                openssh-client \
                libgl1 \
                libglu1 \
                libxm4 \
                libxi6


        The preceding code takes care of everything except for ``libxp6``, which you must
        manually download and install.

        Because ``libxpl6`` pre-depends on ``multiarch-support``, which is
        also outdated, it must be removed. Otherwise you will have a broken
        package configuration. The following code downloads and modifies the
        ``libxp6`` package to remove the ``multiarch-support`` dependency and
        then installs it via the ``dpkg`` package.

        .. code:: console

            cd /tmp
            wget http://ftp.br.debian.org/debian/pool/main/libx/libxp/libxp6_1.0.2-2_amd64.deb
            ar x libxp6_1.0.2-2_amd64.deb
            sudo tar xzf control.tar.gz
            sudo sed '/Pre-Depends/d' control -i
            sudo bash -c "tar c postinst postrm md5sums control | gzip -c > control.tar.gz"
            sudo ar rcs libxp6_1.0.2-2_amd64_mod.deb debian-binary control.tar.gz data.tar.xz
            sudo dpkg -i ./libxp6_1.0.2-2_amd64_mod.deb


    .. tab-item:: Ubuntu 16.04 and older

        If you are using Ubuntu 16.04, you can install missing dependencies with:

        .. code:: console

            user@machine:~$ apt-get update

            # Install dependencies
            user@machine:~$ apt-get install -y \
                openssh-client \
                libgl1 \
                libglu1 \
                libxm4 \
                libxi6 \
                libxp6


A useful resource is `HOW TO - Install Ansys' Required Linux Packages & Libraries <simutech_linux_dependencies_>`_.

.. _conflicts_student_version:

Conflicts with student version
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Although you can install Ansys together with other Ansys products or versions, on Windows, you
should not install a student version of an Ansys product together with its non-student version.
For example, installing both the Ansys MAPDL 2022 R2 Student Version and Ansys MAPDL 2022
R2 might cause license conflicts due to overwriting of environment variables. Having different
versions, for example the Ansys MAPDL 2022 R2 Student Version and Ansys MAPDL 2021 R1,
is fine.

If you experience issues, edit these environment variables to remove any
reference to the student version: ``ANSYSXXX_DIR``, ``AWP_ROOTXXX``, and
``CADOE_LIBDIRXXX``.
Visit `Incorrect environment variables`_ for information on how to set these environment variables
to the correct location.

.. note::
   By default if a student version is detected, PyMAPDL launches the MAPDL instance in
   ``SMP`` mode, unless another MPI option is specified.

Incorrect environment variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you are using a non-standard install, you might need to manually set the
environment variables ``ANSYSXXX_DIR``, ``AWP_ROOTXXX``, and
``CADOE_LIBDIRXXX`` to the correct location.
The three-digit MAPDL version appears where ``XXX`` is
shown. For Ansys MAPDL 2024 R2, ``242`` appears where ``XXX`` is shown.


.. vale off


.. tab-set::

    .. tab-item:: AWP_ROOT242
        :sync: envvarskey

        .. code:: pwsh-session

           PS echo $env:AWP_ROOT242
           C:\Program Files\ANSYS Inc\ANSYS Student\v242

    .. tab-item:: ANSYS242_DIR
        :sync: envvarskey

        .. code:: pwsh-session

           PS echo $env:ANSYS242_DIR
           C:\Program Files\ANSYS Inc\ANSYS Student\v242\ANSYS

    .. tab-item:: CADOE_LIBDIR242
        :sync: envvarskey

        .. code:: pwsh-session

           PS echo $env:CADOE_LIBDIR242
           C:\Program Files\ANSYS Inc\ANSYS Student\v242\CommonFiles\Language\en-us


Set these environment variables to custom values for the terminal session:

.. tab-set::

    .. tab-item:: AWP_ROOT242
        :sync: envvarskey

        .. code:: pwsh-session

           PS $env:AWP_ROOT242 = "C:\Program Files\ANSYS Inc\v242"
           PS echo $env:AWP_ROOT242
           C:\Program Files\ANSYS Inc\v242

    .. tab-item:: ANSYS242_DIR
        :sync: envvarskey

        .. code:: pwsh-session

           PS $env:ANSYS242_DIR = "C:\Program Files\ANSYS Inc\v242\ANSYS"
           PS echo $env:ANSYS242_DIR
           C:\Program Files\ANSYS Inc\v242\ANSYS

    .. tab-item:: CADOE_LIBDIR242
        :sync: envvarskey

        .. code:: pwsh-session

           PS $env:CADOE_LIBDIR242 = "C:\Program Files\ANSYS Inc\v242\CommonFiles\Language\en-us"
           PS echo $env:CADOE_LIBDIR242
           C:\Program Files\ANSYS Inc\v242\CommonFiles\Language\en-us


To make these changes permanent:


.. tab-set::

    .. tab-item:: AWP_ROOT242
        :sync: envvarskey

        .. code:: pwsh-session

           PS [System.Environment]::SetEnvironmentVariable('AWP_ROOT242','C:\Program Files\ANSYS Inc\v242',[System.EnvironmentVariableTarget]::User)
           PS echo $env:AWP_ROOT242
           C:\Program Files\ANSYS Inc\v242

    .. tab-item:: ANSYS242_DIR
        :sync: envvarskey

        .. code:: pwsh-session

           PS [System.Environment]::SetEnvironmentVariable('ANSYS242_DIR','C:\Program Files\ANSYS Inc\v242\ANSYS',[System.EnvironmentVariableTarget]::User)
           PS echo $env:ANSYS242_DIR
           C:\Program Files\ANSYS Inc\v242\ANSYS

    .. tab-item:: CADOE_LIBDIR242
        :sync: envvarskey

        .. code:: pwsh-session

           PS [System.Environment]::SetEnvironmentVariable('CADOE_LIBDIR242','C:\Program Files\ANSYS Inc\v242\CommonFiles\Language\en-us',[System.EnvironmentVariableTarget]::User)
           PS echo $env:CADOE_LIBDIR242
           C:\Program Files\ANSYS Inc\v242\CommonFiles\Language\en-us

.. vale on

Using a proxy server
~~~~~~~~~~~~~~~~~~~~

In some rare cases, you might have trouble connecting to the MAPDL instance if you are
using a proxy.
When `gRPC <grpc_>`_ is used in a proxy environment and a local address (``127.0.0.1``)
is specified as the connection destination, the gRPC implementation automatically refers to the proxy address.
In this case, the local address cannot be resolved, resulting in a connection error.
As a workaround, set the environment variable ``NO_PROXY`` to your local address ``127.0.0.1``,
and then run :func:`launch_mapdl() <ansys.mapdl.core.launcher.launch_mapdl>`
to connect to the MAPDL instance.


Firewall settings
~~~~~~~~~~~~~~~~~

MAPDL and Python should have the correct firewall settings to allow communication between the two.
If you are using a firewall, you should allow MAPDL to receive inbound connections to the following ports:

* ``50052`` (TCP) for gRPC connection.
* ``50053+`` (TCP) for extra gRPC connection.
* ``50055`` (TCP) for gRPC connection to the MAPDL database.

Allow the Python process to connect to the mentioned ports (outbound connections).

Most firewall rules focus on inbound connections, so you typically do not need to
configure outbound connections. However, if you are experiencing problems, make sure
the firewall is not blocking outbound connections on the following ports:

* ``5005X`` (TCP) for gRPC connections.
* ``50055`` (TCP) for gRPC connection to the MAPDL database.
* ``1055`` (TCP) for licensing connections.
* ``2325`` (TCP) for licensing connections.

For more information on how to **configure your firewall on Windows**, see
`Ansys forum-Licensing 2022 R2 Linux Ubuntu (and also Windows) <af_licensing_windows_ubuntu_>`_.

For more information on how to **configure your firewall on Ubuntu Linux**, see
`Security-Firewall | Ubuntu <ubuntu_firewall_>`_.


Location of the executable file
-------------------------------

Manually set the location of the executable file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you have a non-standard install, PyMAPDL might be unable to find
your MAPDL installation. If this is the case, provide the location of MAPDL
as the first parameter to the :func:`launch_mapdl() <ansys.mapdl.core.launcher.launch_mapdl>`
function.


.. tab-set::

    .. tab-item:: Windows
        :sync: oskey

        .. code:: pycon

            >>> from ansys.mapdl.core import launch_mapdl
            >>> exec_loc = "C:/Program Files/ANSYS Inc/v241/ansys/bin/winx64/ANSYS241.exe"
            >>> mapdl = launch_mapdl(exec_loc)

    .. tab-item:: Linux
        :sync: oskey

        .. code:: pycon

            >>> from ansys.mapdl.core import launch_mapdl
            >>> exec_loc = "/usr/ansys_inc/v241/ansys/bin/ansys241"
            >>> mapdl = launch_mapdl(exec_loc)

.. _ref_default_location_executable:

Default location of the executable file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The first time that you run PyMAPDL, it detects the available Ansys installations.

Ansys installations are normally under:

.. tab-set::

    .. tab-item:: Windows
        :sync: oskey

        .. code:: text

            C:/Program Files/ANSYS Inc/vXXX

    .. tab-item:: Linux
        :sync: oskey

        .. code:: text

            /usr/ansys_inc/vXXX

        Or under:

        .. code:: text

            /ansys_inc/vXXX


By default, the Ansys installer uses the former one (``/usr/ansys_inc``) but also creates a symbolic link to the latter one (``/ansys_inc``).

.. _ref_updating_mapdl_location:

Update the cached executable location
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The first time PyMAPDL finds a valid Ansys installation, it caches its
path in the configuration file, ``config.txt``. The path for this file
is shown in this code:

.. code:: pycon

    >>> from ansys.mapdl.core.launcher import CONFIG_FILE
    >>> print(CONFIG_FILE)
    'C:\\Users\\user\\AppData\\Local\\ansys_mapdl_core\\ansys_mapdl_core\\config.txt'


In certain cases, this configuration file might become obsolete. For example, when a new
Ansys version is installed and an earlier installation is removed.

To update this configuration file with the latest path, use:

.. code:: pycon

    >>> from ansys.mapdl.core import save_ansys_path
    >>> save_ansys_path(r"C:\Program Files\ANSYS Inc\v241\ansys\bin\winx64\ansys241.exe")
    'C:\\Program Files\\ANSYS Inc\\v241\\ansys\\bin\\winx64\\ansys241.exe'

If you want to see which Ansys installations PyMAPDL has detected, use:

.. code:: pycon

    >>> from ansys.mapdl.core import get_available_ansys_installations
    >>> get_available_ansys_installations()
    {242: 'C:\\Program Files\\ANSYS Inc\\v242',
    241: 'C:\\Program Files\\ANSYS Inc\\v241',
    -242: 'C:\\Program Files\\ANSYS Inc\\ANSYS Student\\v242'}

Student versions are provided as **negative** versions because the Python dictionary
does not accept two equal keys. The result of the
:func:`get_available_ansys_installations() <ansys.tools.common.path.get_available_ansys_installations>`
method lists higher versions first and student versions last.

.. warning::
    You should not have the same Ansys product version and student version installed. For more
    information, see :ref:`conflicts_student_version`.


PyMAPDL usage issues
--------------------

.. _ref_issues_np_mapdl:

Issues when importing and exporting NumPy arrays in MAPDL
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Because of the way MAPDL is designed, there is no way to store an
array where one or more dimensions are zero.
This can happen in NumPy arrays, where the first dimension can be
set to zero. For example:

.. code:: pycon

   >>> import numpy
   >>> from ansys.mapdl.core import launch_mapdl
   >>> mapdl = launch_mapdl()
   >>> my_array = np.reshape([1, 2, 3, 4], (4,))
   >>> my_array
   array([1, 2, 3, 4])


These types of array dimensions are always converted to ``1``.

For example:

.. code:: pycon

   >>> mapdl.parameters["mapdlarray"] = my_array
   >>> mapdl.parameters["mapdlarray"]
   array([[1.],
      [2.],
      [3.],
      [4.]])
   >>> mapdl.parameters["mapdlarray"].shape
   (4, 1)

This means that when you pass two arrays—one with the second axis equal
to zero (for example, ``my_array``) and another with the second axis equal
to one—they have the same shape when later retrieved.

.. code:: pycon

   >>> my_other_array = np.reshape([1, 2, 3, 4], (4, 1))
   >>> my_other_array
   array([[1],
      [2],
      [3],
      [4]])
   >>> mapdl.parameters["mapdlarray_b"] = my_other_array
   >>> mapdl.parameters["mapdlarray_b"]
   array([[1.],
      [2.],
      [3.],
      [4.]])
   >>> np.allclose(mapdl.parameters["mapdlarray"], mapdl.parameters["mapdlarray_b"])
   True


.. _ref_pymapdl_stability:

PyMAPDL stability
-----------------

Recommendations
~~~~~~~~~~~~~~~

When connecting to an instance of MAPDL using gRPC (default), there are some cases
where the MAPDL server might exit unexpectedly. There
are several ways to improve MAPDL performance and stability:

Use ``mute`` to improve stability
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When possible, pass ``mute=True`` to individual MAPDL commands or
set it globally with the :func:`Mapdl.mute <ansys.mapdl.core.mapdl_grpc.MapdlGrpc.mute>`
method. This disables streaming back the response from MAPDL for each command
and marginally improves performance and stability. Consider having a debug flag in
your program or script so that you can turn on and off logging and
verbosity as needed.


Known Issues
~~~~~~~~~~~~

* MAPDL 2021 R1 has a stability issue with the
  :func:`Mapdl.input() <ansys.mapdl.core.Mapdl.input>`
  method. Avoid using input files if possible. Attempt to use the
  :meth:`Mapdl.upload() <ansys.mapdl.core.mapdl_grpc.MapdlGrpc.upload>` method to upload
  nodes and elements and read them in via the
  :func:`Mapdl.nread() <ansys.mapdl.core.Mapdl.nread>` and
  :func:`Mapdl.eread() <ansys.mapdl.core.Mapdl.eread>` methods.


Ansys developer ecosystem resources
-----------------------------------

Ansys has an extensive developer ecosystem where you can find assistance for a variety of issues.

- `Developer Portal <_developer_portal>`: Blog posts, documentation, and guide
- `Developer Forum <_developer_forum>`: Scripting and usage support for PyAnsys and other Ansys developer tools
- `Ansys Innovation Space <_ansys_innovation_space>`: Product support forum and training materials
- `GitHub <_pymapdl_repo>`: Development support, bug reporting, feature requests, and more.
- `Ansys Learning Hub <_ansys_learning_hub>`: Training, courses and learning plans


More help needed?
-----------------

.. vale off

.. epigraph::

   *"What do I do if an issue is not listed here?"*

.. vale on

To see if your issue is already posted, search the `PyMAPDL Issues <pymapdl_issues_>`_ page. If not, do one of the following:

* If you are not sure of the cause or would like some explanation about the
  usage of the function or its documentation, create a discussion on the
  `PyMAPDL Discussions <pymapdl_discussions_>`_ page.

* If you believe you have found a bug or want to create a feature request,
  create an issue on the `PyMAPDL Issues <pymapdl_issues_>`_ page.

For more complex issues or queries, contact the `PyAnsys Core team <pyansys_core_>`_.
