
.. _ref_cli:

==============================
PyMAPDL command line interface
==============================

For your convenience, PyMAPDL package includes a command line interface
which allows you to launch, stop, list, and execute commands on MAPDL instances.

The list of available commands can be obtained by typing ``pymapdl --help`` in your
terminal after activating the virtual environment.
For more information about the installation, see :ref:`installation`.


Launch MAPDL instances
======================

To start MAPDL, just type on your activated virtual environment:


.. tab-set::

    .. tab-item:: Windows
        :sync: key1

        .. code:: pwsh-session

            (.venv) PS C:\Users\user\pymapdl> pymapdl start
            Success: Launched an MAPDL instance (PID=23644) at 127.0.0.1:50052

    .. tab-item:: Linux
        :sync: key1

        .. code:: console

            (.venv) user@machine:~$ pymapdl start
            Success: Launched an MAPDL instance (PID=23644) at 127.0.0.1:50052

If you want to specify an argument, for instance the port, then you need to call
`launch_mapdl start`:


.. tab-set::

    .. tab-item:: Windows
        :sync: key1

        .. code:: pwsh-session

            (.venv) PS C:\Users\user\pymapdl> pymapdl start --port 50054
            Success: Launched an MAPDL instance (PID=18238) at 127.0.0.1:50054

    .. tab-item:: Linux
        :sync: key1

        .. code:: console

            (.venv) user@machine:~$ pymapdl start --port 50054
            Success: Launched an MAPDL instance (PID=18238) at 127.0.0.1:50054


This ``pymapdl start`` command uses the
:func:`ansys.mapdl.core.launcher.launch_mapdl_process` function internally
to start MAPDL without creating a client connection. The command returns the
connection information (IP, port, and PID) that you can use to connect later.

Some of the arguments that :func:`ansys.mapdl.core.launcher.launch_mapdl` allows
are also available in the CLI. For instance, you could specify the working directory:

.. tab-set::

    .. tab-item:: Windows
        :sync: key1

        .. code:: pwsh-session

            (.venv) PS C:\Users\user\pymapdl> pymapdl start --run_location C:\Users\user\temp\
            Success: Launched an MAPDL instance (PID=32612) at 127.0.0.1:50052

    .. tab-item:: Linux
        :sync: key1

        .. code:: console

            (.venv) user@machine:~$ pymapdl start --run_location /home/user/tmp
            Success: Launched an MAPDL instance (PID=32612) at 127.0.0.1:50052


For more information about the underlying function, see
:func:`ansys.mapdl.core.launcher.launch_mapdl_process`.


Stop MAPDL instances
====================
You can use the ``pymapdl stop`` command to stop MAPDL instances like this:


.. tab-set::

    .. tab-item:: Windows
        :sync: key1

        .. code:: pwsh-session

            (.venv) PS C:\Users\user\pymapdl> pymapdl stop
            Success: Ansys instances running on port 50052 have been stopped.

    .. tab-item:: Linux
        :sync: key1

        .. code:: console

            (.venv) user@machine:~$ pymapdl stop
            Success: Ansys instances running on port 50052 have been stopped.


By default, the instance running on the port `50052` is stopped.

You can specify the instance running on a different port using `--port` argument:


.. tab-set::

    .. tab-item:: Windows
        :sync: key1

        .. code:: pwsh-session

            (.venv) PS C:\Users\user\pymapdl> pymapdl stop --port 50053
            Success: Ansys instances running on port 50053 have been stopped.

    .. tab-item:: Linux
        :sync: key1

        .. code:: console

            (.venv) user@machine:~$ pymapdl stop --port 50053
            Success: Ansys instances running on port 50053 have been stopped.


Or an instance with a given process id (PID):


.. tab-set::

    .. tab-item:: Windows
        :sync: key1

        .. code:: pwsh-session

            (.venv) PS C:\Users\user\pymapdl> pymapdl stop --pid 40952
            Success: The process with PID 40952 and its children have been stopped.

    .. tab-item:: Linux
        :sync: key1

        .. code:: console

            (.venv) user@machine:~$ pymapdl stop --pid 40952
            Success: The process with PID 40952 and its children has been stopped.


Alternatively, you can stop all the running instances by using:


.. tab-set::

    .. tab-item:: Windows
        :sync: key1

        .. code:: pwsh-session

            (.venv) PS C:\Users\user\pymapdl> pymapdl stop --all
            Success: Ansys instances have been stopped.

    .. tab-item:: Linux
        :sync: key1

        .. code:: console

            (.venv) user@machine:~$ pymapdl stop --all
            Success: Ansys instances have been stopped.


Stop MAPDL instances from Python
---------------------------------

You do not need to shell out to the command-line tool to stop an instance, and you do not
need to have launched it with :func:`launch_mapdl()
<ansys.mapdl.core.launcher.launch_mapdl>` either. Use
:func:`stop() <ansys.mapdl.core.launcher.connection.stop>` directly, with
the same ``port``, ``pid``, and ``all`` options as the command-line tool command:

.. code:: python

    from ansys.mapdl.core.launcher import stop

    # Stop the instance on the default port (50052)
    stop()

    # Stop the instance running on a specific port
    stop(port=50053)

    # Stop a specific process (and its children) by PID
    stop(pid=40952)

    # Stop every MAPDL instance owned by the current user
    stop(all=True)

``stop()`` returns the list of process IDs that were actually stopped, so you
can check whether it found anything to stop:

.. code:: python

    stopped = stop(port=50053)
    if not stopped:
        print("No instance was running on port 50053.")

To stop every local MAPDL instance within a range of ports instead of every
instance owned by the user, use :func:`close_all_local_instances()
<ansys.mapdl.core.launcher.connection.close_all_local_instances>`, which is a
thin wrapper around ``stop()``:

.. code:: python

    import ansys.mapdl.core as pymapdl

    # Stop every local instance
    pymapdl.close_all_local_instances()

    # Only stop instances within a specific port range
    pymapdl.close_all_local_instances(port_range=range(50052, 50200))

If you already hold a connected :class:`Mapdl <ansys.mapdl.core.Mapdl>`
instance, prefer its :meth:`~ansys.mapdl.core.Mapdl.exit` method instead,
because it lets MAPDL shut down gracefully (optionally saving the database)
before the process is terminated:

.. code:: python

    mapdl.exit(save=True)


List MAPDL instances and processes
==================================

You can also list MAPDL instances and processes.
If you want to list MAPDL process, just use the following command:


.. tab-set::

    .. tab-item:: Windows
        :sync: key1

        .. code:: pwsh-session

            (.venv) PS C:\Users\user\pymapdl> pymapdl list
            Name          Is Instance    Status      gRPC port    PID
            ------------  -------------  --------  -----------  -----
            ANSYS.exe     False          running         50052  35360
            ANSYS.exe     False          running         50052  37116
            ANSYS241.exe  True           running         50052  41644

    .. tab-item:: Linux
        :sync: key1

        .. code:: console

            (.venv) user@machine:~$ pymapdl list
            Name          Is Instance    Status      gRPC port    PID
            ------------  -------------  --------  -----------  -----
            ANSYS.exe     False          running         50052  35360
            ANSYS.exe     False          running         50052  37116
            ANSYS241.exe  True           running         50052  41644


If you want, to just list the instances (avoiding listing children MAPDL
processes), just type:


.. tab-set::

    .. tab-item:: Windows
        :sync: key1

        .. code:: pwsh-session

            (.venv) PS C:\Users\user\pymapdl> pymapdl list -i
            Name          Status      gRPC port    PID
            ------------  --------  -----------  -----
            ANSYS241.exe  running         50052  41644

    .. tab-item:: Linux
        :sync: key1

        .. code:: console

            (.venv) user@machine:~$ pymapdl list -i
            Name          Status      gRPC port    PID
            ------------  --------  -----------  -----
            ANSYS241.exe  running         50052  41644


You can also print other fields like the working directory (using `--cwd`)
or the command line (using `-c`).
Additionally, you can also print all the available information by using the
argument `--long` or `-l`:


.. tab-set::

    .. tab-item:: Windows
        :sync: key1

        .. code:: pwsh-session

            (.venv) PS C:\Users\user\pymapdl> pymapdl list -l
            Name          Is Instance    Status      gRPC port    PID  Command line                                                                                                                      Working directory
            ------------  -------------  --------  -----------  -----  --------------------------------------------------------------------------------------------------------------------------------  ---------------------------------------------------
            ANSYS.exe     False          running         50052  35360  C:\Program Files\ANSYS Inc\v241\ANSYS\bin\winx64\ANSYS.EXE -j file -b -i .__tmp__.inp -o .__tmp__.out -port 50052 -grpc           C:\Users\User\AppData\Local\Temp\ansys_ahmfaliakp
            ANSYS.exe     False          running         50052  37116  C:\Program Files\ANSYS Inc\v241\ANSYS\bin\winx64\ANSYS.EXE -j file -b -i .__tmp__.inp -o .__tmp__.out -port 50052 -grpc           C:\Users\User\AppData\Local\Temp\ansys_ahmfaliakp
            ANSYS241.exe  True           running         50052  41644  C:\Program Files\ANSYS Inc\v241\ansys\bin\winx64\ansys241.exe -j file -np 2 -b -i .__tmp__.inp -o .__tmp__.out -port 50052 -grpc  C:\Users\User\AppData\Local\Temp\ansys_ahmfaliakp

    .. tab-item:: Linux
        :sync: key1

        .. code:: console

            (.venv) user@machine:~$ pymapdl list -l
            Name          Is Instance    Status      gRPC port    PID  Command line                                                               Working directory
            ------------  -------------  --------  -----------  -----  -------------------------------------------------------------------------  --------------------------------
            ANSYS         False          running         50052  35360  /ansys_inc/v241/ansys/bin/linx64/ansys -j file -port 50052 -grpc           /home/user/temp/ansys_ahmfaliakp
            ANSYS         False          running         50052  37116  /ansys_inc/v241/ansys/bin/linx64/ansys -j file -port 50052 -grpc           /home/user/temp/ansys_ahmfaliakp
            ANSYS241      True           running         50052  41644  /ansys_inc/v241/ansys/bin/linx64/ansys241 -j file -np 2 -port 50052 -grpc  /home/user/temp/ansys_ahmfaliakp


The converter module has its own command line interface to convert
MAPDL files to PyMAPDL. For more information, see
:ref:`ref_cli_converter`.


.. _ref_cli_exec:

Execute MAPDL commands
======================

Use ``pymapdl exec`` to send APDL commands to a running MAPDL instance and
print the output to stdout. The command always connects to an existing
instance, it never starts a new one. Use ``pymapdl start`` first if needed.

There are three mutually exclusive sources for commands:

**1.** ``-c`` / ``--command`` **options**

Each ``-c`` value is one APDL command; all commands are joined and sent as a
single block. You can pass multiple ``-c`` flags:


.. tab-set::

    .. tab-item:: Windows
        :sync: key1

        .. code:: pwsh-session

            (.venv) PS C:\Users\user\pymapdl> pymapdl exec -c /prep7 -c "BLOCK,0,1,0,1,0,1" -c SAVE

    .. tab-item:: Linux
        :sync: key1

        .. code:: console

            (.venv) user@machine:~$ pymapdl exec -c /prep7 -c "BLOCK,0,1,0,1,0,1" -c SAVE


Or embed multiple commands in a single ``-c`` value using your shell's quoting
to produce real newlines:


.. tab-set::

    .. tab-item:: Windows (PowerShell)
        :sync: key1

        .. code:: pwsh-session

            (.venv) PS C:\Users\user\pymapdl> pymapdl exec -c "/prep7`nBLOCK,0,1,0,1,0,1`nSAVE"

    .. tab-item:: Linux (bash/zsh)
        :sync: key1

        .. code:: console

            (.venv) user@machine:~$ pymapdl exec -c $'/prep7\nBLOCK,0,1,0,1,0,1\nSAVE'


**2. Script file**

Read commands from an APDL script file using ``--file`` / ``-f``:


.. tab-set::

    .. tab-item:: Windows
        :sync: key1

        .. code:: pwsh-session

            (.venv) PS C:\Users\user\pymapdl> pymapdl exec --file my_script.inp

    .. tab-item:: Linux
        :sync: key1

        .. code:: console

            (.venv) user@machine:~$ pymapdl exec --file my_script.inp


**3. Stdin**

Pipe commands in from another program. The ``-`` marker is optional, when
stdin is a pipe ``pymapdl exec`` detects it automatically:


.. tab-set::

    .. tab-item:: Windows
        :sync: key1

        .. code:: pwsh-session

            (.venv) PS C:\Users\user\pymapdl> Get-Content my_script.inp | pymapdl exec
            (.venv) PS C:\Users\user\pymapdl> Get-Content my_script.inp | pymapdl exec -

    .. tab-item:: Linux
        :sync: key1

        .. code:: console

            (.venv) user@machine:~$ cat my_script.inp | pymapdl exec
            (.venv) user@machine:~$ echo "/prep7" | pymapdl exec


.. note::

   ``pymapdl exec`` auto-reads stdin only when it detects a pipe (that is stdin
   is not a terminal).  Running ``pymapdl exec`` interactively with no
   arguments still produces an error rather than hanging.


By default, ``pymapdl exec`` connects without clearing the MAPDL database, so
successive calls share the same model state. Use the ``--clear-on-connect``
flag to clear the database before sending commands:


.. tab-set::

    .. tab-item:: Windows
        :sync: key1

        .. code:: pwsh-session

            (.venv) PS C:\Users\user\pymapdl> pymapdl exec --clear-on-connect -c /prep7

    .. tab-item:: Linux
        :sync: key1

        .. code:: console

            (.venv) user@machine:~$ pymapdl exec --clear-on-connect -c /prep7


A common workflow is to start MAPDL once, send one or more command blocks, and
then stop the instance:


.. tab-set::

    .. tab-item:: Windows
        :sync: key1

        .. code:: pwsh-session

            (.venv) PS C:\Users\user\pymapdl> pymapdl start
            Success: Launched an MAPDL instance (PID=23644) at 127.0.0.1:50052
            (.venv) PS C:\Users\user\pymapdl> pymapdl exec -c /prep7 -c "BLOCK,0,1,0,1,0,1"
            (.venv) PS C:\Users\user\pymapdl> pymapdl exec -c SAVE
            (.venv) PS C:\Users\user\pymapdl> pymapdl stop
            Success: Ansys instances running on port 50052 have been stopped.

    .. tab-item:: Linux
        :sync: key1

        .. code:: console

            (.venv) user@machine:~$ pymapdl start
            Success: Launched an MAPDL instance (PID=23644) at 127.0.0.1:50052
            (.venv) user@machine:~$ pymapdl exec -c /prep7 -c "BLOCK,0,1,0,1,0,1"
            (.venv) user@machine:~$ pymapdl exec -c SAVE
            (.venv) user@machine:~$ pymapdl stop
            Success: Ansys instances running on port 50052 have been stopped.


.. note::

   ``pymapdl exec`` writes command output to stdout and errors to stderr,
   making it suitable for use in shell scripts and pipelines. The process
   exits with code ``0`` on success and ``1`` on failure.

To convert an existing APDL script to Python instead of executing it, see
:ref:`ref_cli_converter`.


.. _ref_cli_help:

Get help
========

The command-line tool provides a generic help command that lists available MAPDL keywords and
functions. The output can be filtered using standard shell tools. For example,
filter for GET-related entries containing NODE and LOC with grep:


.. tab-set::

    .. tab-item:: Windows
        :sync: key1

        .. code:: pwsh-session

            (.venv) PS C:\Users\user\pymapdl> pymapdl help "*GET" | Select-String -Context 3,3 "NODE" | Select-String -Context 3,3 "LOC"
                ┣━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
                ┃ Item1 ┃ IT1NUM   ┃ Description                                                                                       ┃
                ┡━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
                │ LOC   │ X, Y, Z  │ X, Y, Z location in the active coordinate system. Alternative get functions: NX( N ), NY( N ),    │
                │       │          │ NZ( N ). Inverse get function. NODE( x,y,z ) returns the number of the selected node nearest the  │
                │       │          │ x,y,z location (in the active coordinate system, lowest number for coincident nodes).             │
                ├───────┼──────────┼───────────────────────────────────────────────────────────────────────────────────────────────────┤


        .. note:: The `-Context` argument controls the number of lines to print before and after the match (`-Context <n>`)
            which can be helpful to understand the context of the matched keyword.
            You can also control them separately with `-Context <before>,<after>`.

    .. tab-item:: Linux
        :sync: key1

        .. code:: console

            (.venv) user@machine:~$ pymapdl help "*GET" | grep -C 3 NODE | grep -C 3 LOC
                ┣━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
                ┃ Item1 ┃ IT1NUM   ┃ Description                                                                                       ┃
                ┡━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
                │ LOC   │ X, Y, Z  │ X, Y, Z location in the active coordinate system. Alternative get functions: NX( N ), NY( N ),    │
                │       │          │ NZ( N ). Inverse get function. NODE( x,y,z ) returns the number of the selected node nearest the  │
                │       │          │ x,y,z location (in the active coordinate system, lowest number for coincident nodes).             │
                ├───────┼──────────┼───────────────────────────────────────────────────────────────────────────────────────────────────┤


        .. note:: The `-C` / `--context` option of grep shows lines before and after the matched line,
            which can be helpful to understand the context of the matched keyword.

This shows a matched table excerpt; adjust the grep pattern to match the keywords you need.


.. _ref_cli_converter:

Convert APDL code
=================

After you have activated and installed the package as described
in :ref:`installation`, you can use the converter from your terminal.
Here is how you use the ``pymapdl convert`` command:


.. tab-set::

    .. tab-item:: Windows
        :sync: key1

        .. code:: pwsh-session

            (.venv) PS C:\Users\user\pymapdl> pymapdl convert mapdl.dat -o python.py

            The ``mapdl.dat`` file is successfully converted to the ``python.py`` file.


    .. tab-item:: Linux
        :sync: key1

        .. code:: console

            (.venv) user@machine:~$ pymapdl convert mapdl.dat -o python.py

            File mapdl.dat successfully converted to python.py.

To obtain help on converter usage, options, and examples, type this command:


.. tab-set::

    .. tab-item:: Windows
        :sync: key1

        .. code:: pwsh-session

            (.venv) PS C:\Users\user\pymapdl> pymapdl convert --help


            Usage: pymapdl convert [OPTIONS] FILENAME_IN

            PyMAPDL CLI tool for converting MAPDL scripts to PyMAPDL scripts.

            USAGE:

            ...


    .. tab-item:: Linux
        :sync: key1

        .. code:: console

            (.venv) user@machine:~$ pymapdl convert --help

            Usage: pymapdl convert [OPTIONS] FILENAME_IN

            PyMAPDL CLI tool for converting MAPDL scripts to PyMAPDL scripts.

            USAGE:

            ...


The ``pymapdl convert`` command uses the
:func:`convert_script() <ansys.mapdl.core.convert_script>` function.
Hence, this command accepts most of this function's arguments.


.. _ref_cli_programmatic:

Use the commands from Python
============================

Every ``pymapdl`` sub-command is a thin Click wrapper, named ``<name>_cli``,
around a plain function named ``<name>`` that lives in the same module, for
example :func:`ansys.mapdl.core.cli.start.start`. Import the plain function to
get the same behavior from Python, which avoids spawning a shell and parsing
text output.

.. note::

   :func:`stop() <ansys.mapdl.core.launcher.connection.stop>` is the
   exception to the "same module" rule: it lives in
   :mod:`ansys.mapdl.core.launcher.connection` so it can also be used by
   :func:`close_all_local_instances()
   <ansys.mapdl.core.launcher.connection.close_all_local_instances>` without
   depending on the CLI package. Import it with ``from
   ansys.mapdl.core.launcher import stop`` (or the equivalent
   ``ansys.mapdl.core.cli.stop.stop`` alias, kept for backward compatibility).

.. code:: python

    from ansys.mapdl.core.cli.exec import exec_commands
    from ansys.mapdl.core.cli.start import start
    from ansys.mapdl.core.launcher import stop

    ip, port, pid = start(port=50054, nproc=4)
    print(exec_commands(commands=["/prep7", "BLOCK,0,1,0,1,0,1"], port=port))
    stop(pid=pid)

The mapping between commands and functions is direct. Each function takes the
long form of the command options as keyword arguments:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Command
     - Function
   * - ``pymapdl start``
     - :func:`start() <ansys.mapdl.core.cli.start.start>`
   * - ``pymapdl stop``
     - :func:`stop() <ansys.mapdl.core.launcher.connection.stop>`
   * - ``pymapdl list``
     - :func:`list_instances() <ansys.mapdl.core.cli.list_instances.list_instances>`
   * - ``pymapdl check``
     - :func:`check() <ansys.mapdl.core.cli.check.check>`
   * - ``pymapdl exec``
     - :func:`exec_commands() <ansys.mapdl.core.cli.exec.exec_commands>`
   * - ``pymapdl convert``
     - :func:`convert() <ansys.mapdl.core.cli.convert.convert>`
   * - ``pymapdl help``
     - :func:`help_command() <ansys.mapdl.core.cli.help.help_command>`
   * - ``pymapdl skills list``
     - :func:`list_skills() <ansys.mapdl.core.cli.skills.list_skills>`
   * - ``pymapdl skills show``
     - :func:`show_skill() <ansys.mapdl.core.cli.skills.show_skill>`
   * - ``pymapdl skills install``
     - :func:`install_skill() <ansys.mapdl.core.cli.skills.install_skill>`

These functions return data and raise exceptions, they never print to stdout
nor exit the interpreter. Rendering and exit codes are the responsibility of
the Click wrapper. So a failure surfaces as a regular Python exception that
you can handle:

.. code:: python

    from ansys.mapdl.core.cli.check import check
    from ansys.mapdl.core.errors import MapdlConnectionError

    try:
        info = check(port=50052)
    except MapdlConnectionError:
        print("No instance is running on port 50052.")
    else:
        print(info["information"]["mapdl_version"])

Two functions return a string that is meant to be printed rather than parsed:
:func:`list_instances() <ansys.mapdl.core.cli.list_instances.list_instances>`
returns the rendered table, and :func:`help_command()
<ansys.mapdl.core.cli.help.help_command>` returns the docstring with the ANSI
escape sequences of a color terminal. To get the instances as data instead of a
table, use :func:`get_mapdl_instances()
<ansys.mapdl.core.cli.helpers.get_mapdl_instances>`.

For the full signatures, see :ref:`ref_cli_api`.
