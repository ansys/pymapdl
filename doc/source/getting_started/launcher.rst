

.. _ref_launch_pymapdl:

==============
Launch PyMAPDL
==============

PyMAPDL can start MAPDL locally, or it can connect to a session already running locally or
on a remote machine.

* :ref:`launch_pymapdl_local`
  * :ref:`launching_pymapdl_without_client`
* :ref:`connect_pymapdl_to_a_local_mapdl_instance`
  * :ref:`launch_grpc_mapdl_session`
  * :ref:`connect_grpc_mapdl_session`
* :ref:`connect_grpc_remote_mapdl_session`
* :ref:`setting_mapdl_location`
* :ref:`securing_pymapdl_connection`

If you have any problem launching PyMAPDL, see :ref:`Launching issues <ref_launching_issue>`.


.. _launch_pymapdl_local:

Launch PyMAPDL with a local MAPDL instance
==========================================

You can use the :func:`launch_mapdl() <ansys.mapdl.core.launcher.launch_mapdl>`
function to start MAPDL and automatically connect to it:

.. code:: pycon

    >>> from ansys.mapdl.core import launch_mapdl
    >>> mapdl = launch_mapdl()
    >>> print(mapdl)
    Product:             Ansys Mechanical Enterprise
    MAPDL Version:       24.1
    ansys.mapdl Version: 0.68.0


While this is the easiest and fastest way to get PyMAPDL up and running.
you must be able to launch MAPDL locally.

If PyMAPDL cannot find your local installation, see
`Setting the MAPDL location in PyMAPDL`_.

For more information on controlling how MAPDL launches locally, see the
description of the :func:`launch_mapdl() <ansys.mapdl.core.launcher.launch_mapdl>` function.


.. _launching_pymapdl_without_client:

Launch MAPDL process without creating a client
----------------------------------------------

Sometimes you may want to launch a MAPDL process without immediately creating a
client connection. This is useful for:

* Starting MAPDL from the command-line interface
* Managing multiple MAPDL instances programmatically
* Launching MAPDL in a separate process for later connection

For these scenarios, you can use the :func:`launch_mapdl_process() <ansys.mapdl.core.launcher.launch_mapdl_process>`
function, which starts MAPDL and returns connection information without creating a client:

.. code:: pycon

    >>> from ansys.mapdl.core.launcher import launch_mapdl_process
    >>> ip, port, pid = launch_mapdl_process(nproc=4, port=50052)
    >>> print(f"MAPDL is running at {ip}:{port} (PID: {pid})")
    MAPDL is running at 127.0.0.1:50052 (PID: 12345)

You can later connect to this instance using the :class:`Mapdl <ansys.mapdl.core.Mapdl>` class:

.. code:: pycon

    >>> from ansys.mapdl.core import Mapdl
    >>> mapdl = Mapdl(ip=ip, port=port)

This approach gives you more control over the MAPDL process lifecycle and allows
you to manage the process independently from the client connection.

.. note::
   The :func:`launch_mapdl_process() <ansys.mapdl.core.launcher.launch_mapdl_process>`
   function always starts a new MAPDL instance. It cannot be used to connect to
   an existing instance. Use :func:`launch_mapdl() <ansys.mapdl.core.launcher.launch_mapdl>`
   with ``start_instance=False`` for that purpose.


.. _connect_pymapdl_to_a_local_mapdl_instance:

Connect PyMAPDL to a local MAPDL instance
=========================================

Connect to a local MAPDL instance requires two steps: launching a
local MAPDL session and connect to it.

.. _launch_grpc_mapdl_session:

Launch a local gRPC MAPDL session
---------------------------------

You can start MAPDL from the command line and then connect to it.

To launch MAPDL, use this command:

.. tab-set::

    .. tab-item:: Windows
        :sync: key1

        .. code:: pwsh-session

            (.venv) PS C:\Users\user\pymapdl> C:/Program Files/ANSYS Inc/v241/ansys/bin/winx64/ANSYS241.exe -grpc

    .. tab-item:: Linux
        :sync: key1

        .. code:: console

            (.venv) user@machine:~$ /usr/ansys_inc/v241/ansys/bin/ansys241 -grpc

When launching MAPDL on Windows, it is assumed that Ansys is installed in the
:file:`C:/Program Files/ANSYS Inc/v241` directory and, on Linux, it is assumed
that Ansys is installed in the :file:`/usr/ansys_inc` directory.

This starts MAPDL in gRPC mode. MAPDL should display this output:

.. code:: output

     Start GRPC Server

     ##############################
     ### START GRPC SERVER      ###
     ##############################

     Server Executable   : MapdlGrpc Server
     Server listening on : 0.0.0.0:50052

You can configure the port that MAPDL starts on with the ``-port`` argument.
For example, you can start the server to listen for connections at
port 50005 with this command:

.. tab-set::

    .. tab-item:: Windows
        :sync: key1

        .. code:: pwsh-session

            (.venv) PS C:\Users\user\pymapdl> C:/Program Files/ANSYS Inc/v241/ansys/bin/winx64/ANSYS241.exe -port 50005  -grpc

    .. tab-item:: Linux
        :sync: key1

        .. code:: console

            (.venv) user@machine:~$ /usr/ansys_inc/v241/ansys/bin/ansys241 -port 50005  -grpc


From version v0.68, you can use a command line interface to launch, stop, and list
local MAPDL instances.
For more information, see :ref:`ref_cli`.


.. _connect_grpc_mapdl_session:

Connect to the local MAPDL instance
-----------------------------------

An MAPDL gRPC server can be connected to from the same host by using
this code:

.. code:: pycon

    >>> from ansys.mapdl.core import Mapdl
    >>> mapdl = Mapdl()

The preceding code assumes that your MAPDL service is running locally on the default IP address
(``127.0.0.1``) and on the default port (``50052``).

You can also use the :func:`launch_mapdl() <ansys.mapdl.core.launcher.launch_mapdl>` method to connect to an already launched MAPDL instance by setting the ``start_instance`` argument to ``False``:

.. code:: pycon

    >>> from ansys.mapdl.core import launch_mapdl
    >>> mapdl = launch_mapdl(start_instance=False)

If you are connecting to an MAPDL Docker image, the procedure is the same.
Just make sure that you specify the mapped port instead of the internal MAPDL port.
For more information, see :ref:`pymapdl_docker`.


.. _connect_grpc_remote_mapdl_session:

Connect PyMAPDL to a remote MAPDL instance
==========================================

If you want to connect to a **remote** MAPDL instance, you must know the IP
address of that instance.
For example, if on your local network at IP address ``192.168.0.1`` there is a
computer running MAPDL on the port ``50052``, you can connect to it with this code:

.. code:: pycon

    >>> mapdl = Mapdl("192.168.0.1", port=50052)

Alternatively, you can use a hostname:

.. code:: pycon

    >>> mapdl = Mapdl("myremotemachine", port=50052)

Note that you must have started an MAPDL instance in gRPC mode on the computer with
the referenced IP address and hostname for this to work because PyMAPDL cannot launch remote instances.


.. _setting_mapdl_location:

Setting the MAPDL location in PyMAPDL
=====================================

To run, PyMAPDL must know the location of the MAPDL binary.
Most of the time this can be automatically determined, but
the location of MAPDL must be provided for non-standard installations.
When running for the first time, PyMAPDL requests the
location of the MAPDL executable if it cannot automatically find it.

You can test your installation of PyMAPDL and set it up by running
the :func:`launch_mapdl() <ansys.mapdl.core.launcher.launch_mapdl>` function:

.. code:: python

    from ansys.mapdl.core import launch_mapdl

    mapdl = launch_mapdl()

Python automatically attempts to detect your MAPDL binary based on
environmental variables.
You can specify an MAPDL installation using one of two environment
variables:

* ``AWP_ROOTXXX``, where ``XXX``` is the three-digit version. This environment variable
  contains the path of the Ansys installation with the version matching ``XXX``.
  For example, ``AWP_ROOT241=/ansys_inc`` contains the path to an Ansys 2024 R1 installation.

* ``PYMAPDL_MAPDL_EXEC`` contains the path to the Ansys MAPDL executable file.
  For example, ``PYMAPDL_MAPDL_EXEC=/ansys_inc/v241/ansys/bin/ansys241``.

If PyMAPDL is unable to find a copy of MAPDL, you
are prompted for the location of the MAPDL executable.

Here is the prompt with an example response for Windows:

.. code:: output

    Enter location of MAPDL executable: C:\Program Files\ANSYS Inc\v241\ANSYS\bin\winx64\ansys241.exe

Here is the prompt with an example response for Linux:

.. code:: output

    Enter location of MAPDL executable: /usr/ansys_inc/v241/ansys/bin/ansys241

The settings file is stored locally, which means that you are not prompted
to enter the path again. If you must change the default Ansys path
(meaning change the default version of MAPDL), run this code:

.. code:: python

    from ansys.mapdl import core as pymapdl

    new_path = "C:\\Program Files\\ANSYS Inc\\v241\\ANSYS\\bin\\winx64\\ansys241.exe"
    pymapdl.change_default_ansys_path(new_path)

For more information, see the :func:`change_default_ansys_path() <ansys.mapdl.core.change_default_ansys_path>` method and the :func:`find_mapdl() <ansys.mapdl.core.find_mapdl>` method.

Additionally, it is possible to specify the executable in each PyMAPDL script using the ``exec_file`` keyword argument.


.. tab-set::

    .. tab-item:: Windows
        :sync: key1

        .. code:: python

            from ansys.mapdl.core import launch_mapdl

            mapdl = launch_mapdl(
                exec_file="C://Program Files//ANSYS Inc//v241//ANSYS//bin//winx64//ansys241.exe"
            )

    .. tab-item:: Linux
        :sync: key1

        .. code:: python

            from ansys.mapdl.core import launch_mapdl

            mapdl = launch_mapdl(exec_file="/usr/ansys_inc/v241/ansys/bin/ansys241")


You could also specify a custom executable made from a custom MAPDL compilation by adding the correspondent flag (``-custom``) to the ``additional_switches``
keyword argument:


.. tab-set::

    .. tab-item:: Windows
        :sync: key1

        .. code:: python

            from ansys.mapdl.core import launch_mapdl

            custom_exec = "C://Program Files//ANSYS Inc//v241//ANSYS//bin//winx64//ansys241.exe"
            add_switch = f" -custom {custom_exec}"
            mapdl = launch_mapdl(additional_switches=add_switch)


    .. tab-item:: Linux
        :sync: key1

        .. code:: python

            from ansys.mapdl.core import launch_mapdl

            custom_exec = "/usr/ansys_inc/v241/ansys/bin/ansys241t"
            add_switch = f" -custom {custom_exec}"
            mapdl = launch_mapdl(additional_switches=add_switch)


.. _securing_pymapdl_connection:

Securing your PyMAPDL connection
================================

PyMAPDL supports four gRPC transport modes: ``insecure``, ``uds``, ``wnua``, and ``mtls``.
When no transport mode is specified, PyMAPDL selects the most secure available mode automatically
based on the operating system:

* **Linux** → ``uds`` (Unix Domain Socket)
* **Windows** → ``wnua`` (Windows Named User Authentication)
* **macOS and other platforms** → ``insecure`` (with a warning)

To override the automatic selection, pass the ``transport_mode`` argument to
:func:`launch_mapdl() <ansys.mapdl.core.launcher.launch_mapdl>`, or set the
:envvar:`PYMAPDL_GRPC_TRANSPORT` environment variable before starting Python.


Insecure
--------

The ``insecure`` transport mode sends gRPC traffic without any encryption or
authentication. It is supported on all platforms and can be used for both local and
remote connections.

This is the default transport mode on older MAPDL versions, before Ansys MAPDL 2024 R2.

.. warning::

   Do not use insecure mode over untrusted or remote networks. All traffic between
   PyMAPDL and MAPDL is sent in plain text and can be intercepted. For local
   connections, prefer ``uds`` on Linux/macOS or ``wnua`` on Windows. For remote
   connections, use ``mtls``.

.. code-block:: python

    from ansys.mapdl.core import launch_mapdl

    mapdl = launch_mapdl(transport_mode="insecure")

Alternatively, set the environment variable before running your script:

.. tab-set::

    .. tab-item:: Linux/macOS
        :sync: key1

        .. code-block:: console

            export PYMAPDL_GRPC_TRANSPORT=insecure

    .. tab-item:: Windows
        :sync: key2

        .. code-block:: pwsh-session

            $env:PYMAPDL_GRPC_TRANSPORT = "insecure"


Unix Domain Socket (UDS)
------------------------

The ``uds`` transport mode uses a Unix domain socket file instead of a TCP connection.
Because the socket lives only on the local filesystem, no network traffic is exposed and
the connection cannot be accessed from outside the machine. This mode is the default on
Linux.

This mode is not supported on Windows.

MAPDL names its socket file ``mapdl-<PORT>.sock`` and places it in the directory
pointed to by the :envvar:`ANSYS_MAPDL_UDS_PATH` environment variable. If that
variable is not set, PyMAPDL uses ``~/.conn`` by default.

.. code-block:: python

    from ansys.mapdl.core import launch_mapdl

    mapdl = launch_mapdl(transport_mode="uds")

To use a custom socket directory, pass the ``uds_dir`` argument:

.. code-block:: python

    from ansys.mapdl.core import launch_mapdl

    mapdl = launch_mapdl(transport_mode="uds", uds_dir="/tmp/mapdl-sockets")

Alternatively, set the environment variables before running your script:

.. tab-set::

    .. tab-item:: Linux/macOS
        :sync: key1

        .. code-block:: console

            export PYMAPDL_GRPC_TRANSPORT=uds
            export ANSYS_MAPDL_UDS_PATH=/tmp/mapdl-sockets

.. note::

   UDS does not support remote connections. For remote connections, use
   ``mtls`` instead.


Windows Named User Authentication (WNUA)
----------------------------------------

The ``wnua`` transport mode authenticates the connection
using the identity of the logged-in Windows user. Only the same user who launched the
MAPDL process can connect to it, providing access control without requiring certificates
or any additional configuration. This mode is the default on Windows.

This mode is only supported on Windows.

.. code-block:: python

    from ansys.mapdl.core import launch_mapdl

    mapdl = launch_mapdl(transport_mode="wnua")

Alternatively, set the environment variable before running your script:

.. tab-set::

    .. tab-item:: Windows
        :sync: key2

        .. code-block:: pwsh-session

            $env:PYMAPDL_GRPC_TRANSPORT = "wnua"

.. note::

   WNUA does not support remote connections. For remote connections, use
   ``mtls`` instead.


Mutual Transport Layer Security (mTLS)
---------------------------------------

The ``mtls`` transport mode encrypts all gRPC traffic and requires both PyMAPDL and
MAPDL to present certificates signed by a shared Certificate Authority (CA). This mutual
authentication ensures that only trusted clients can connect to trusted servers. It is
the recommended mode for remote connections and production deployments.

.. code-block:: python

    from ansys.mapdl.core import launch_mapdl

    mapdl = launch_mapdl(
        transport_mode="mtls",
        certs_dir="/path/to/certs",
    )

Alternatively, set the environment variables before running your script:

.. tab-set::

    .. tab-item:: Linux/macOS
        :sync: key1

        .. code-block:: console

            export PYMAPDL_GRPC_TRANSPORT=mtls
            export ANSYS_GRPC_CERTIFICATES=/path/to/certs

    .. tab-item:: Windows
        :sync: key2

        .. code-block:: pwsh-session

            $env:PYMAPDL_GRPC_TRANSPORT = "mtls"
            $env:ANSYS_GRPC_CERTIFICATES = "C:\path\to\certs"

For full setup instructions, including certificate generation and launching MAPDL with
mTLS enabled, see :ref:`ref_tls_guide`.


Transport mode comparison
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 14 15 20 15 36

   * - Mode
     - Encryption
     - OS support
     - Remote support
     - Recommended use case
   * - ``insecure``
     - None
     - All
     - Yes (discouraged)
     - Testing and development on trusted local networks only
   * - ``uds``
     - Filesystem isolation
     - Linux
     - No
     - Default local mode on Linux; same-machine connections
   * - ``wnua``
     - User authentication
     - Windows only
     - No
     - Default local mode on Windows; same-machine connections
   * - ``mtls``
     - TLS + mutual auth
     - All
     - Yes
     - Production deployments, remote connections, and HPC
