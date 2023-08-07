.. _ref_pymapdl_and_macos:

=================
PyMAPDL and MacOS
=================

Install PyMAPDL
===============

PyMAPDL can be installed normally in a MacOS system which fulfill PyMAPDL
requirements using:

.. code:: zsh

    pip install ansys-mapdl-core


PyMAPDL requires to connect an MAPDL live instance to function.
However MAPDL is not compatible with MacOS.

There are two options then:

* **Connect to a remote instance**: You can connect to a remote instance running
in a Windows or Linux machine following :ref:`connect_grpc_madpl_session`.

* **Launch MAPDL locally using docker**: You can run MAPDL in a MacOS machine following


.. _launch_mapdl_on_macos:

Launch MAPDL on MacOS
=====================

If you do not have an MAPDL docker image, you can create one in a Linux
machine using the instructions given in :ref:`ref_make_container`.


If you have already an MAPDL docker image you can launch MAPDL following
the procedure specified in :ref:`run_an_mapdl_image`.

Apple Silicon compatibility
---------------------------

If you are using an Apple Silicon device (for instance M1 or M2), you might see the following
warning:

.. code::  output

    WARNING: The requested image's platform (linux/amd64) does not match the detected host platform (linux/arm64/v8) and no specific platform was requested

This is because the docker image has not been build to run on Apple Silicon architecture (arm64). You add the
following argument ``--platform linux/amd64`` to the `docker run <docker_run_>`_ command:

.. code:: zsh

    ANSYSLMD_LICENSE_FILE=1055@MY_LICENSE_SERVER_IP
    LOCAL_MAPDL_PORT=50053
    MAPDL_DOCKER_REGISTRY_URL=ghcr.io/myuser/myrepo/mymapdldockerimage
    docker run -e ANSYSLMD_LICENSE_FILE=$ANSYSLMD_LICENSE_FILE --restart always --name mapdl -p $LOCAL_MAPDL_PORT:50052 --platform linux/amd64 $MAPDL_DOCKER_REGISTRY_URL -smp > log.txt


Connect to an MAPDL container
=============================

You can connect to the MAPDL instance following :ref:`connect_grpc_madpl_session`.


