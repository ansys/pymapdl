

.. _ref_launch_pymapdl:


Launch PyMAPDL
==============

PyMAPDL can start MAPDL locally, or connect to a session already running locally or in a remote machine.

* `Launch PyMAPDL with a local MAPDL instance`_
* `Connect PyMAPDL to a local MAPDL instance`_
* `Connect PyMAPDL to a remote MAPDL instance`_

If you have any problem launching PyMAPDL, see :ref:`Launching issues <ref_launching_issue>`.


Launch PyMAPDL with a local MAPDL instance
------------------------------------------

You can use the :func:`launch_mapdl() <ansys.mapdl.core.launcher.launch_mapdl>`
method to have Python start MAPDL and automatically connect to it:

.. code:: pycon

    >>> from ansys.mapdl.core import launch_mapdl
    >>> mapdl = launch_mapdl()
    >>> print(mapdl)
    Product:             Ansys Mechanical Enterprise
    MAPDL Version:       24.1
    ansys.mapdl Version: 0.68.0


This is the easiest and fastest way to get PyMAPDL up and running. 
But you need to be able to launch MAPDL locally.

If PyMAPDL cannot find your local installation, please refer to
`Setting MAPDL location in PyMAPDL`_.

For more information on controlling how MAPDL launches locally, see the
description of the :func:`launch_mapdl() <ansys.mapdl.core.launcher.launch_mapdl>` function.


Connect PyMAPDL to a local MAPDL instance
-----------------------------------------

.. _launch_grpc_madpl_session:

Launch a local gRPC MAPDL session
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can start MAPDL from the command line and then connect to it.

To launch MAPDL on Windows (assuming a :file:`C:/Program Files/ANSYS Inc/v241` installation), use:

.. code:: pwsh-session

    C:/Program Files/ANSYS Inc/v241/ansys/bin/winx64/ANSYS211.exe -grpc

To launch MAPDL on Linux (assuming ANSYS is installed in :file:`/usr/ansys_inc` installation), use:

.. code:: console

    /usr/ansys_inc/v241/ansys/bin/ansys211 -grpc

This starts up MAPDL in gRPC mode, and MAPDL should output:

.. code:: output

     Start GRPC Server

     ##############################
     ### START GRPC SERVER      ###
     ##############################

     Server Executable   : MapdlGrpc Server
     Server listening on : 0.0.0.0:50052

You can configure the port that MAPDL starts on with the ``-port`` argument.
For example, you can start the server to listen for connections at 
port 50005 with:

.. code:: console

    /usr/ansys_inc/v241/ansys/bin/ansys211 -port 50005 -grpc


.. _connect_grpc_madpl_session:

Connect to the local MAPDL instance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An MAPDL gRPC server can be connected to from the same host by using:

.. code:: pycon

    >>> from ansys.mapdl.core import Mapdl
    >>> mapdl = Mapdl()

This assumes that your MAPDL service is running locally on the default IP address 
(``127.0.0.1``) and on the default port (``50052``).

You can also use the :func:`launch_mapdl() <ansys.mapdl.core.launcher.launch_mapdl>` to connect to an already launched MAPDL instance by setting the ``start_instance`` argument to ``False``.

.. code:: pycon

    >>> from ansys.mapdl.core import launch_mapdl
    >>> mapdl = launch_mapdl(start_instance=False)

If you are connecting to an MAPDL Docker image, the procedure is the same.
Just make sure that you specify the mapped port instead of the internal MAPDL port.
For more information, see :ref:`pymapdl_docker`.


.. _connect_grpc_remote_madpl_session:

Connect PyMAPDL to a remote MAPDL instance
------------------------------------------

If you want to connect to a **remote** MAPDL instance, you must know the IP 
address of that instance, so you can connect to it.
For example, if on your local network at IP address ``192.168.0.1`` there is a
computer running MAPDL on the port 50052, you can connect to it with:

.. code:: pycon

    >>> mapdl = Mapdl("192.168.0.1", port=50052)

Alternatively you can use a hostname:

.. code:: pycon

    >>> mapdl = Mapdl("myremotemachine", port=50052)

Note that you must have started an MAPDL instance in gRPC mode on the computer with
the mentioned IP address/hostname for this to work, since PyMAPDL cannot launch remote instances.


Setting MAPDL location in PyMAPDL
---------------------------------

To run PyMAPDL must know the location of the MAPDL binary. 
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
You can specify MAPDL installation using one of the two following environment
variables:

* ``AWP_ROOTXXX`` where ``XXX``` is the three digits version. This environment variable
  contains the path of the Ansys installation which version match ``XXX``.
  For instance, ``AWP_ROOT222=/ansys_inc`` contains the path of an Ansys 2022R2 installation.

* ``PYMAPDL_MAPDL_EXEC`` contains the path the Ansys MAPDL executable.
  For instance, ``PYMAPDL_MAPDL_EXEC=/ansys_inc/v222/ansys/bin/ansys222``.

If PyMAPDL is unable to find a copy of MAPDL, you
are prompted for the location of the MAPDL executable.

Here is a sample input for Linux:

.. code:: output

    Enter location of MAPDL executable: /usr/ansys_inc/v222/ansys/bin/ansys222

Here is a sample input for Windows:

.. code:: output

    Enter location of MAPDL executable: C:\Program Files\ANSYS Inc\v222\ANSYS\bin\winx64\ansys222.exe

The settings file is stored locally, which means that you are not prompted
to enter the path again. If you must change the default Ansys path
(meaning change the default version of MAPDL), run the following:

.. code:: python

    from ansys.mapdl import core as pymapdl

    new_path = "C:\\Program Files\\ANSYS Inc\\v212\\ANSYS\\bin\\winx64\\ansys222.exe"
    pymapdl.change_default_ansys_path(new_path)

Also see the :func:`change_default_ansys_path() <ansys.mapdl.core.change_default_ansys_path>` method and
the :func:`find_ansys() <ansys.mapdl.core.find_ansys>` method.

Additionally, it is possible to specify the executable in each PyMAPDL script using the keyword argument ``exec_file``. 

In Linux:

.. code:: python

    from ansys.mapdl.core import launch_mapdl

    mapdl = launch_mapdl(exec_file="/usr/ansys_inc/v212/ansys/bin/ansys212")


In Windows:

.. code:: python

    from ansys.mapdl.core import launch_mapdl

    mapdl = launch_mapdl(
        exec_file="C://Program Files//ANSYS Inc//v212//ANSYS//bin//winx64//ansys212.exe"
    )

You could also specify a custom executable made from a custom MAPDL compilation by adding the correspondent flag (``-custom``) to the ``additional_switches``
keyword argument:

.. code:: python

    from ansys.mapdl.core import launch_mapdl

    custom_exec = "/usr/ansys_inc/v212/ansys/bin/ansys212t"
    add_switch = f" -custom {custom_exec}"
    mapdl = launch_mapdl(additional_switches=add_switch)
