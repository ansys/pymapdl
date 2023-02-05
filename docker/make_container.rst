
Create your own MAPDL docker container
======================================

.. warning:: You need a valid Ansys license and an Ansys account to
   follow the steps detailed in this section.

You can create your own MAPDL docker container following
the steps given in this page.
This guide will use a local Ubuntu machine to generate the needed
files for the MAPDL container by installing Ansys products first
and then copy the generated files to the container.


Requirements
============

* A linux machine, preferable with Ubuntu 18.04 or later.
  CentOS Linux distribution is not supported anymore.
  This machine needs to have `Docker <https://www.docker.com>`_ installed.

* A valid Ansys account. Your Ansys reseller should have
  provide you with one.

* The following provided files:
  
  * `Dockerfile <https://github.com/pyansys/pymapdl/tree/main/docker/Dockerfile>`_
  * `.dockerignore <https://github.com/pyansys/pymapdl/tree/main/docker/.dockerignore>`_


Procedure
=========

Downloading Ansys MAPDL installation files
------------------------------------------

Download latest Ansys MAPDL version from the customer portal 
(`Current Release <ansys_current_release_>`_).
You need to have a valid Ansys account with access to
products downloads.

If you lack of an Ansys account, please contact your
IT manager.


Install Ansys MAPDL product
---------------------------

To install Ansys MAPDL product on an Ubuntu machine you can follow 
:ref:`install_mapdl` if you are using the graphical user interface
or :ref:`installing_ansys_in_wsl` for the command line interface.
The later approach can be reused with small differences in a
continuous integration workflow.

Build Docker image
------------------

To build the Docker image, in the working directory, all files
included in the image should be added.
The steps are detailed in the following script, which you should
modify to adapt your needs.

.. code:: bash

    # Creating working directory
    mkdir docker_image
    cd docker_image

    # Copying the docker files
    cp ./some-path/Dockerfile
    cp ./some-path/.dockerignore

    # Creating env vars for the Dockerfile
    export VERSION=222
    export TAG="V222"
    export MAPDL_PATH=/my_path_to_mapld_installation_/ansys_inc

    # Build Docker image
    sudo docker build  -t $TAG --build-arg VERSION=$VERSION --build-arg MAPDL_PATH=$MAPDL_PATH

Not all the installation files are copied, in fact, the files ignored during the copying
are detailed in the file `.dockerignore`.


Summary
=======


* **Step 1:** Download latest Ansys MAPDL version from the customer portal 
  (`Current Release <ansys_current_release_>`_).

* **Step 2:** Install Ansys MAPDL in a known folder. You can reuse your local
  installation if it is updated and the machine is running the same Ubuntu
  version as the targe Ubuntu docker version.

* **Step 3:** Build the docker image with the provided Docker configuration files
  and script.


