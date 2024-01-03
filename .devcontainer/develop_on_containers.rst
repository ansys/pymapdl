.. _develop_on_remote_containers:

Develop on a remote container
=============================

.. note:: This approach requires to have a docker image with MAPDL installed.
   The one listed in the 
   `repository development container configuration files <pymapdl_devcontainer_configuration_>`_ 
   is not for public usage due to licensing issues.
   However, you are invited to `create your own docker image <ref_make_container_>`
   and use this file as template for setting your own local development container.

To use a `remote container <vscode_devcontainers_containers_>`_, you must install:

* `VS Code <vscode_>`_
* `Docker software <docker_>`_ or equivalent.
  It is recommended to use Windows Subsystem Linux (WSL) backend to run Linux
  docker containers.
  See `Developing inside a Container Getting started <vscode_devcontainers_containers_getting_started_>`_
  for more information.
* `Remove Development VS Code extension pack <vscode_devcontainers_remote_extension_>`_

As mentioned before, you must have your own Docker image with MAPDL installed
locally available or hosted in an online registry, i.e. GitHub `ghcr.io <ghcr_>`_.
For the purpose of this document, assume your image is hosted at
``ghcr.io/myaccount/mapdlimage:mytag``.

You must then modify the file
`docker-compose.yml <pymapdl_build_docker_compose_>`_ with your custom image:

.. code-block:: yaml
   :emphasize-lines: 4

   ports:
      - '50052:50052'
      - '50055:50055'
   image: 'ghcr.io/myaccount/mapdlimage:mytag'
   user: "0:0"


.. warning:: Also you might need to change some environment variables or Docker
   options to adjust to your image configuration.
   For example you might need to change the :envvar:`AWP_ROOT222` if you MAPDL
   container does not have the installation in the default directory.
   Be careful to not commit those changes in your PRs.

You can now open the current folder (or PyMAPDL repository) using
:kbd:`ctr/cmd` + :kbd:`shift` + :kbd:`p` to open the Visual Code `Command palette`.
Then select ``Dev Containers: Open Folder in Container``.
You will be prompted to select one of the multiple devcontainer configurations,
select `PyMAPDL-DevContainer (Local)`.
Because the configuration is available in :file:`.devcontainer/devcontainer-local` directory,
VS Code will automatically launch the MAPDL container with the desired configuration.

.. note:: First time you launch the devcontainer it might take a long time to get ready,
   since it needs to pull the container image from the registry.

You can now work normally, but you will be, in fact, working from
inside the container.
Because Visual Code mount the local directory into the docker container,
you don't lose your changes if accidentally delete your container.
However, this mounting process might have a significant impact on
the container performance, especially noticeable if you are using MacOS.
You can avoid that by cloning the repository inside the container.
Visit `Quick start: Open a Git repository or GitHub PR in an isolated container volume <vscode_open_a_repository_in_container_>`_
for more information.

