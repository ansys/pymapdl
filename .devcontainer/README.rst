
=======================================
Ansys PyMAPDL Developer Container Guide
=======================================

Hello! Welcome to the Ansys PyMAPDL Developer Container Guide! :smile:

This guide should guide you on how to do development on PyMAPDL using
`Codespaces <https://github.com/features/codespaces>`_ or
a `remote container <https://code.visualstudio.com/docs/devcontainers/containers>`_.

In the ``.devcontainer`` directory, the files for setting up the container can be found.


Using a Remote Container
========================


Licensing
---------

Codespaces are free for public repositories. However, you will need to have a valid license to run MAPDL.
You can set your license using the environment variable ``ANSYSLMD_LICENSE_FILE``.
For example, if you have a license server at the address ``123.45.67.89``, you can set the license using:

.. code:: bash
  
   export ANSYSLMD_LICENSE_FILE="1055@123.45.65.89"

If you want you can also store this environment variable value in your user codespaces secrets.
You can set them in your Github settings under
``Developer settings`` -> ``Code, planning, and automation`` -> ``Codespaces`` -> ``Codespaces secrets``.
You can add there a secret named ``ANSYSLMD_LICENSE_FILE`` with the value of your license server port and address.



Using Codespaces
================

Codespaces launch a container which already contains the latest MAPDL image. 
This is the easiest way to get started with PyMAPDL development.

You can launch a Codespace by clicking on the ``Code`` button on the top right of the repository and then clicking on ``Open with Codespaces``.

.. image:: .. image:: https://github.com/pyansys/pymapdl/raw/main/doc/source/images/devcontainer/open_codespaces.png
   :alt: Open with Codespaces

After some time allowed to load, you can see a fully functional Codespace with the latest MAPDL image and the latest PyMAPDL repository cloned.

.. image:: .. image:: https://github.com/pyansys/pymapdl/raw/main/doc/source/images/devcontainer/codespaces_main.png
   :alt: Codespaces main

You can now start developing PyMAPDL!

Licensing
---------

Codespaces are free for public repositories. However, you will need to have a valid license to run MAPDL.
You can set your license using the environment variable ``ANSYSLMD_LICENSE_FILE``.
For example, if you have a license server at the address ``123.45.67.89``, you can set the license using:

.. code:: bash
  
   export ANSYSLMD_LICENSE_FILE="1055@123.45.65.89"

If you want you can also store this environment variable value in your user codespaces secrets.
You can set them in your Github settings under
``Developer settings`` -> ``Code, planning, and automation`` -> ``Codespaces`` -> ``Codespaces secrets``.
You can add there a secret named ``ANSYSLMD_LICENSE_FILE`` with the value of your license server port and address.

