.. _using_standard_install:

******************************************
Use PyMAPDL from the standard installation
******************************************

The PyAnsys ``ansys-mapdl-core`` package requires either a local or
remote instance of MAPDL to communicate with it. This section covers
launching and interfacing with MAPDL from a local instance by
launching it from Python.

Install MAPDL
-------------

MAPDL is installed by default from the Ansys standard installer. When
installing Ansys, verify that the **Mechanical Products** checkbox is
selected under the **Structural Mechanics** option. While the standard
installer options can change, see the following figure for reference.

.. figure:: ../images/unified_install_2019R1.jpg
    :width: 400pt


Launch MAPDL
------------

Launch MAPDL locally
~~~~~~~~~~~~~~~~~~~~

You can use the ``launch_mapdl`` method to have Python start MAPDL and
automatically connect to it:

.. code:: python

    >>> from ansys.mapdl.core import launch_mapdl
    >>> mapdl = launch_mapdl()
    >>> print(mapdl)

    Product:             ANSYS Mechanical Enterprise
    MAPDL Version:       RELEASE  2021 R1           BUILD 21.0
    PyMAPDL Version:     Version: 0.57.0


This is the easiest and fastest way to get PyMAPDL up and running. 
But you need to have an ANSYS license server installed locally. 

Launch a gRPC MAPDL session
~~~~~~~~~~~~~~~~~~~~~~~~~~~
You can start MAPDL from the command line and then connect to it.

To launch MAPDL on Windows (assuming a ``C:/Program Files/ANSYS Inc/v211`` installation), use:

.. code::

    C:/Program Files/ANSYS Inc/v211/ansys/bin/winx64/ANSYS211.exe -grpc

To launch MAPDL on Linux (assuming a ``/usr/ansys_inc`` installation), use:

.. code::

    /usr/ansys_inc/v211/ansys/bin/ansys211 -grpc

This starts up MAPDL in gRPC mode, and MAPDL should output:

.. code::

     Start GRPC Server

     ##############################
     ### START GRPC SERVER      ###
     ##############################

     Server Executable   : MapdlGrpc Server
     Server listening on : 0.0.0.0:50052

You can configure the port that MAPDL starts on with the ``-port`` argument.
For example, you can start the server to listen for connections at 
port 50005 with:

.. code::

    /usr/ansys_inc/v211/ansys/bin/ansys211 -port 50005 -grpc

You can also configure the IP address. 
However, because of an Ansys limitation to receive
strings from a command line, the IP address must be read from an external file 
named ``mylocal.ip``. This file is read automatically from the directory where 
MAPDL is running.

You can then set up the IP address.

In Windows PowerShell or Command Prompt, use:

.. code::
    
    echo "127.0.0.1" > mylocal.ip
    C:/Program Files/ANSYS Inc/v211/ansys/bin/winx64/ANSYS211.exe -grpc


In Linux, use:

.. code::
    
    echo "127.0.0.1" > mylocal.ip
    /usr/ansys_inc/v211/ansys/bin/ansys211 -grpc


Connect to a gRPC MAPDL session
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A MAPDL gRPC server can be connected to from either the same host or an
external host. For example, you can connect to a MAPDL service
running **locally** with:

.. code::

    >>> from ansys.mapdl.core import Mapdl
    >>> mapdl = Mapdl()


This assumes that your MAPDL service is running locally on the default IP address 
(127.0.0.1) and on the default port (50052).

If you want to connect to a **remote** instance of MAPDL and you know the IP 
address of that instance, you can connect to it.
For example, if on your local network at IP address ``192.168.0.1`` there is a
computer running MAPDL on the port 50052, you can connect to it with:

.. code::

    >>> mapdl = Mapdl('192.168.0.1', port=50052)

Alternatively you can use a hostname:

.. code:: python

    >>> mapdl = Mapdl('myremotemachine', port=50052)

Note that you must have started MAPDL in gRPC mode on the computer with
the mentioned IP address/hostname for this to work.
If you have MAPDL installed on your local host, you
can use the ``launch_mapdl`` method to both start and connect to MAPDL.

If you have any problem launching PyMAPDL, see :ref:`debugging_launch_mapdl`
