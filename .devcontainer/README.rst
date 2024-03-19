

======================
Develop on a container
======================

This guide guides you on how to develop PyMAPDL features or fix bugs using
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


Develop on a remote container
=============================

.. note:: If you are an Ansys employee or collaborator and want to use this development method, please email `PyAnsys Core team <pyansys_core_>`_.

To use a `remote container <https://code.visualstudio.com/docs/devcontainers/containers>`_, you must install:

* `VS Code <https://code.visualstudio.com>`_
* `Docker software <https://www.docker.com>`_ or equivalent.
  It is recommended to use Windows Subsystem Linux (WSL) backend to run Linux docker containers.
  See `Developing inside a Container Getting started <https://code.visualstudio.com/docs/devcontainers/containers#_getting-started>`_
  for more information.
* `Remove Development VS Code extension pack <https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack>`_

As mentioned before, you must have your own Docker image with MAPDL installed locally available or hosted in an 
online registry, i.e. GitHub `ghcr.io <https://github.com/features/packages>`_.
For the purpose of this document, assume your image is hosted at ``ghcr.io/myaccount/mapdlimage:mytag``.

You must then modify the file `docker-compose.yml <https://github.com/ansys/pymapdl/tree/main/.devcontainer/docker-compose.yml>`_
with your custom image:

.. code-block:: yaml
   :emphasize-lines: 4

   ports:
      - '50052:50052'
      - '50055:50055'
   image: 'ghcr.io/myaccount/mapdlimage:mytag'
   user: "0:0"


.. warning:: Also you might need to change some environment variables or Docker options to adjust to your image configuration.
   For example you might need to change the :envvar:`AWP_ROOT222` if you MAPDL container does not have the installation in the default directory.
   Be careful to not commit those changes in your PRs.

You can now open the current folder (or PyMAPDL repository) using
:kbd:`ctr/cmd` + :kbd:`shift` + :kbd:`p` to open the VSCode *Command palette*.
Then select ``Dev Containers: Open Folder in Container``.
Because the configuration is available in :file:`.devcontainer` directory, VS Code will automatically
launch the MAPDL container with the desired configuration.

You can now work normally, but you will be, in fact, working from inside the container.
Because VSCode mount the local directory into the docker container, you don't lose your changes if accidentally
delete your container.
However, this mounting process might have a significant impact on the container performance, especially noticeable
if you are using MacOS.
You can avoid that by cloning the repository inside the container.
Visit `Quick start: Open a Git repository or GitHub PR in an isolated container volume <https://code.visualstudio.com/docs/devcontainers/containers#_quick-start-open-a-git-repository-or-github-pr-in-an-isolated-container-volume>`_
for more information.


License
-------

As mentioned before, you must have a valid license to run MAPDL.
When you launch the container, the file :file:`script.sh` automatically
checks if the environment variable :envvar:`ANSYSLMD_LICENSE_FILE` exists.
This environment variable sets the port and IP address of the license server.
If you do not have set this environment variable before launching the
container, you are prompt to enter your license server port and address.

You can set the environment variable :envvar:`ANSYSLMD_LICENSE_FILE`
from the terminal before launching VS Code.
This is recommended if you are using Windows OS.
For example, if you have a license server at the address ``123.45.67.89``,
you can set the license using:

.. code:: pwsh-session
  
   $env:ANSYSLMD_LICENSE_FILE = '1055@123.45.65.89'
   code . # launch VS Code

On Linux

.. code:: bash

   $ export ANSYSLMD_LICENSE_FILE =1055@123.45.65.89
   code . # launch VS Code

And then open the folder in the container using the *Command palette*.


Develop on Codespaces
=====================

Codespaces is a virtual delopment environment provided by GitHub.
You can launch a container which all the required tools and start to work in couple of minutes.
This is an easy way to get started with PyMAPDL development.

.. warning:: This method is only applicable and allowed to Ansys employees or collaborators.
   If you are an Ansys employee and wants use this development method, please email `PyAnsys Core team <pyansys_core_>`_.

