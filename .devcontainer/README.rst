.. _develop_on_containers:

=======================
Develop on containers
=====================

This guide describes how to develop PyMAPDL features or fix bugs using
a `remote container <https://code.visualstudio.com/docs/devcontainers/containers>`_
or `Codespaces <https://github.com/features/codespaces>`_.
The files for setting up the container can be found in the 
`.devcontainer directory <https://github.com/ansys/pymapdl/tree/main/.devcontainer>`_.


About the MAPDL container
=========================

Because MAPDL software is not open source, the GPL license does not allow to
distribute a docker container to users.
Having a docker container with MAPDL installed is a requirement to use
any of the development methods mentioned on this section.
If you want to build your own docker image, visit the following link
:ref:`ref_make_container`.


License
-------

As mentioned before, you must have a valid license to run MAPDL.
When you launch the container, the file :file:`script.sh` automatically
checks if the environment variable :envvar:`ANSYSLMD_LICENSE_FILE` exists.
This environment variable sets the port and IP address of the license server.
If you do not have set this environment variable before launching the
container, you are prompt to enter your license server port and address.

You can set the :envvar:`ANSYSLMD_LICENSE_FILE` environment variable 
from the terminal before launching VS Code.
For example, if you have a license server at the address ``123.45.67.89``,
you can set the license on Windows using:

.. code:: pwsh-session
  
   $env:ANSYSLMD_LICENSE_FILE = '1055@123.45.65.89'
   code . # launch VS Code

On Linux

.. code:: bash

   $ export ANSYSLMD_LICENSE_FILE =1055@123.45.65.89
   code . # launch VS Code

And then open the folder in the container using the `Command palette`.
