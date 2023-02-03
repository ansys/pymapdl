
===========================================
Ansys PyMAPDL Developing-on-Container Guide
===========================================

Hello! Welcome to the Ansys PyMAPDL Developing-on-Container Guide! :smile:

This guide should guide you on how to develop PyMAPDL features or fix bugs using
a `remote container <https://code.visualstudio.com/docs/devcontainers/containers>`_
or `Codespaces <https://github.com/features/codespaces>`_.

The files for setting up the container can be found in the 
`.devcontainer directory <https://github.com/pyansys/pymapdl/tree/main/.devcontainer>`_.


Using a Remote Container
========================

To use remote containers locally, you need to install:

* `VS Code <https://code.visualstudio.com>`_
* `Docker <https://www.docker.com>`_.
  It is recommended to use Windows Subsystem Linux (WSL) backend to run docker containers.
  See `https://code.visualstudio.com/docs/devcontainers/containers#_getting-started`_ for
  more information.
* `Remove Development VS Code extension <https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack>`_

Once you have everything installed you can open the current folder (or repository) using
``ctr/cmd`` + ``shift`` + ``p`` to open the VSCode *Command palette*.
Then select ``Dev Containers: Open Folder in Container``.
Because the configuration is available in ``.devcontainer`` directory, VS Code will automatically
launch the MAPDL Ubuntu container with the desired configuration.

Licensing
---------

You will need to have a valid license to run MAPDL.

When you launch the container, the file ``script.sh`` automatically checks if the environment
variable ``ANSYSLMD_LICENSE_FILE`` exists.
This environment variable sets the port and IP address of the license server.

If you do not have set this env var before launching the container, you will be asked to enter
your license server port and address.

You can set your license using the environment variable ``ANSYSLMD_LICENSE_FILE`` before launching
VS Code.
For example, if you have a license server at the address ``123.45.67.89``, you can set the license using:

.. code:: bash
  
   export ANSYSLMD_LICENSE_FILE="1055@123.45.65.89" # set license env var
   code . # launch VS Code

And then open the folder in the container using the *Command palette*.


Using Codespaces
================

Codespaces launch a container which already contains the latest MAPDL image. 
This is the easiest way to get started with PyMAPDL development.

You can launch a Codespace by clicking on the ``Code`` button on the top right of the repository and then clicking on ``Open with Codespaces``.

.. image:: https://github.com/pyansys/pymapdl/raw/main/doc/source/images/devcontainer/open_codespaces.png
   :alt: Open with Codespaces

After a moment, you will see a fully functional Codespace with the latest MAPDL image and the latest PyMAPDL repository cloned.

.. image:: https://github.com/pyansys/pymapdl/raw/main/doc/source/images/devcontainer/codespaces_main.png
   :alt: Codespaces main

You can now start developing PyMAPDL!


Licensing
---------

Codespaces are free for public repositories. However, you will need to have a valid license to run MAPDL.
You can set your license using the environment variable ``ANSYSLMD_LICENSE_FILE``.
For example, if you have a license server at the address ``123.45.67.89``, you can set the license using:

.. code:: bash
  
   export ANSYSLMD_LICENSE_FILE="1055@123.45.65.89"

However a **better approach** is to use *Codespaces secrets* to store this env var.
You can set it in your Github profile settings in
``Developer settings`` -> ``Code, planning, and automation`` -> ``Codespaces`` -> ``Codespaces secrets``.
You can add there a secret named ``ANSYSLMD_LICENSE_FILE`` with the value of your license server port and address.

