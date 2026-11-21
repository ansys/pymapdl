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

.. note::
   To debug launching issues, follow the step-by-step guide in
   :ref:`ref_debug_launching_issues`.

If MAPDL still does not launch, see :ref:`Launching issues <ref_launching_issue>` for more information on
common issues and their solutions.

If after examining all the log files you cannot identify the issue, open a
discussion on the `PyMAPDL Discussions <pymapdl_discussions_>`_ page.
If you believe you have found a bug, create an issue on the `PyMAPDL Issues <pymapdl_issues_>`_ page.
You can attach the log file to the bug report for further investigation.


Troubleshooting guides
----------------------

Select the guide that matches your problem:

* :ref:`Issues before launching MAPDL <ref_troubleshooting_before_launch>`:
  Ansys installation, executable location, missing dependencies, and student
  version conflicts.
* :ref:`Launching issues <ref_launching_issue>`: step-by-step guide to debug
  a launch failure, the UDS socket error, connection timeouts, and environment
  variables.
* :ref:`Connection, licensing, and runtime issues <ref_troubleshooting_runtime>`:
  licensing, MPI, VPN, proxy, firewall, NumPy arrays, and stability.

If you cannot find your issue, see `More help needed?`_.

.. toctree::
   :maxdepth: 1
   :hidden:

   troubleshoot_before_launch
   troubleshoot_launch
   troubleshoot_runtime


Ansys developer ecosystem resources
-----------------------------------

Ansys has an extensive developer ecosystem where you can find assistance for a variety of issues.

- `Developer Portal <developer_portal_>`_: Blog posts, documentation, and guide
- `Developer Forum <developer_forum_>`_: Scripting and usage support for PyAnsys and other Ansys developer tools
- `Ansys Innovation Space <ansys_innovation_space_>`_: Product support forum and training materials
- `GitHub <pymapdl_repo_>`_: Development support, bug reporting, feature requests, and more.
- `Ansys Learning Hub <ansys_learning_hub_>`_: Training, courses and learning plans


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
