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

If you do not have an MAPDL docker image, you can create one in a linux
machine using the instructions given in :ref:`ref_make_container`.


If you have already an MAPDL docker image you can launch MAPDL using:

.. code:: zsh

    docker 

Then you can connect to the MAPDL instance following :ref:`connect_grpc_madpl_session`.


