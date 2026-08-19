.. _ref_devcontainer:

=====================
Develop on containers
=====================

This guide describes how to develop PyMAPDL features or fix bugs in a
`development container <vscode_devcontainers_containers_>`_. The container
configurations are in the `.devcontainer directory
<pymapdl_devcontainer_directory_>`_.


About the MAPDL container
=========================

The local development container is based on an Ansys MAPDL image. You must
have access to that image and a valid MAPDL license to use it. If you need to
create your own MAPDL image, see :ref:`ref_make_container`.


License
-------

Configure the image to reach your license server before starting the
container. Do not commit license-server addresses or other site-specific
settings.


.. _develop_on_remote_containers:

Use a local development container
=================================

To use the local container, install the following software:

* `Visual Studio Code <vscode_>`_
* `Docker <docker_main_>`_ or an equivalent container runtime
* The `Dev Containers extension <vscode_devcontainers_remote_extension_>`_

Clone the PyMAPDL repository and open it in Visual Studio Code. Open the
Command Palette with :kbd:`Ctrl` + :kbd:`Shift` + :kbd:`P` on Windows and
Linux, or :kbd:`Cmd` + :kbd:`Shift` + :kbd:`P` on macOS. Select **Dev
Containers: Open Folder in Container** and then select
**PyMAPDL-DevContainer (Local)**.

The configuration is in the
`local devcontainer configuration <pymapdl_devcontainer_configuration_>`_. It
builds the `Dockerfile <pymapdl_devcontainer_dockerfile_>`_ from the same
directory and mounts the repository according to its
`docker-compose.yml <pymapdl_build_docker_compose_>`_ file. The initial build
can take several minutes while Docker downloads the base image and installs
dependencies.

Customize the local development container
-----------------------------------------

To use a custom MAPDL image, update the ``FROM`` instruction in the
`Dockerfile <pymapdl_devcontainer_dockerfile_>`_. Update
`docker-compose.yml <pymapdl_build_docker_compose_>`_ when your image requires
different volumes, ports, environment variables, or other Docker settings.

Keep site-specific changes outside your pull request. The development
container files are shared project configuration.

Use GitHub Codespaces
=====================

The repository also provides separate configurations for development and
documentation in GitHub Codespaces:

* :file:`.devcontainer/codespaces-dev/devcontainer.json` configures the
  development environment.
* :file:`.devcontainer/codespaces-docs/devcontainer.json` adds the tools
  needed to build the documentation.

Select the appropriate configuration when you create a codespace. See `the
Visual Studio Code Dev Containers documentation
<vscode_devcontainers_containers_getting_started_>`_ for more information.
