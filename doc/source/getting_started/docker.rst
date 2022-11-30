.. _pymapdl_docker:

************************
Use MAPDL through Docker
************************
You can run MAPDL within a container on any OS using Docker and
connect to it via PyMAPDL.

There are several situations in which it is advantageous to run MAPDL
in a containerized environment such as Docker or Singularity:

- Run in a consistent environment regardless of the host OS.
- Portability and ease of install.
- Large-scale cluster deployment using Kubernetes
- Genuine app isolation through containerization.

Configure the Docker registry
=============================

There is a Docker image hosted on the 
`PyMAPDL GitHub <pymapdl_repo_>`_ repository that you
can download using your GitHub credentials.

Assuming that you have Docker installed, you can get started by
authorizing Docker to access this repository using a personal access
token. Create a GitHub personal access token with ``packages read`` permissions
according to `Creating a personal access token <gh_creating_pat_>`_

Save that token to a file with:

.. code::

   echo XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX > GH_TOKEN.txt


This lets you send the token to Docker without leaving the token value
in your history. Next, authorize Docker to access this repository
with:

.. code::

    GH_USERNAME=<my-github-username>
    cat GH_TOKEN.txt | docker login ghcr.io -u $GH_USERNAME --password-stdin


Run the MAPDL image
===================

You can now launch MAPDL directly from Docker with a short script or
directly from the command line. Because this image contains no license
server, you must enter your license server IP address in the
``LICENSE_SERVER`` environment variable. With that, you can launch
MAPDL with:

.. code::

    LICENSE_SERVER=1055@XXX.XXX.XXX.XXX
    VERSION=v21.1.0

    IMAGE=ghcr.io/pyansys/pymapdl/mapdl:$VERSION
    docker run -e ANSYSLMD_LICENSE_FILE=$LICENSE_SERVER -p 50052:50052 $IMAGE -smp

First time you run it, Docker logins into the *ghcr.io* registry and
pulls the image which can take some time.

Note that port `50052` (local to the container) is being mapped to
50052 on the host. This makes it possible to launch several MAPDL
instances with different port mappings to allow for multiple instances
of MAPDL.

You can provide additional command line parameters to MAPDL by simply
appending to the Docker command. 
For example, you can increase the number of processors (up to the
number available on the host machine) with the `-np` switch.

Once you have launched MAPDL you should see:

.. code::

    Start GRPC Server

    ##############################
    ### START GRPC SERVER      ###
    ##############################

    Server Executable   : MapdlGrpc Server
    Server listening on : 0.0.0.0:50052


Using ``docker-compose`` to launch MAPDL
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can also use ``docker-compose`` command to launch MAPDL configured in
a ``docker-compose`` file.
This is useful if you want to load an already configured environment, or
if you want to launch multiple instances of MAPDL or services.

For you convenience, the directory `docker <pymapdl_docker_dir_>`_ 
contains pre-configured ``docker-compose`` files that you can
use:

* `docker-compose.yml <pymapdl_docker_compose_base_>`_: the **base** 
  configuration file which launch a remote instance of MAPDL which you
  can connect to. Similar approach to the one described above.

* `docker-compose.local.yml <pymapdl_docker_compose_base_>`_: 
  This file is an extension of the base configuration file which launch
  an Ubuntu Docker image with MAPDL installed in it. 
  This is useful if you want to run MAPDL locally inside this container
  for example for debugging purposes.
  You can connect your VSCode instance to this container by selecting
  ``Attach to a running container`` option from the command palette.
  For more details visit `Attach to a running container <vscode_attach_to_container_>`_.

* `docker-compose.license_server.yml <pymapdl_docker_compose_license_server_>`_:
  This file is an extension of the base configuration file which launch
  a license server. 
  This is useful if you want to run MAPDL remotely and you don't have 
  access to a license server.
  You need a valid license file to run the license server.
  You can use it together with ``docker-compose.local.yml`` hence you
  can connect to it the same way.
  The call to this docker file should be always the last one in the
  ``docker-compose`` command. For instance:

  .. code:: bash

     docker-compose -f docker-compose.yml -f docker-compose.local.yml -f docker-compose.license_server.yml up
  

.. warning:: About the license server image.
   The license server is not intended to be used in production. 
   It is only intended for testing/debugging purposes.
   Its access is limited to collaborators of the PyAnsys project.
   If you would like to have access to it, please contact PyAnsys support at
   `pyansys.support@ansys.com <pyansys_support_>`_.

Connect to the MAPDL container from Python
==========================================

You can now connect to the instance with:

.. code:: python

    >>> from ansys.mapdl.core import Mapdl
    >>> mapdl = Mapdl()

If you mapped to any other port other than 50052, you should specify
that port when connecting to MAPDL with:

.. code:: python

    >>> mapdl = Mapdl(port=<my-port>)

Verify your connection with:

.. code:: python

    >>> print(mapdl)

    Product:             ANSYS Mechanical Enterprise
    MAPDL Version:       RELEASE  2021 R1           BUILD 21.0
    PyMAPDL Version:     Version: 0.57.0

Additional considerations
=========================

Append MAPDL options to the container
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the command:

.. code::

    IMAGE=ghcr.io/pyansys/pymapdl/mapdl:$VERSION
    docker run -e ANSYSLMD_LICENSE_FILE=$LICENSE_SERVER -p 50052:50052 $IMAGE -smp

You can provide additional command line parameters to MAPDL by simply
appending to the Docker command. For example, you can increase the
number of processors (up to the number available on the host machine)
with the ``-np`` switch:

.. code::

    IMAGE=ghcr.io/pyansys/pymapdl/mapdl:$VERSION
    docker run -e ANSYSLMD_LICENSE_FILE=$LICENSE_SERVER -p 50052:50052 $IMAGE -np 4


For additional command line arguments please see the *Notes* section
within `launch_mapdl <pymapdl_launch_mapdl_>`_.
Also, be sure to have the appropriate license for additional HPC features.

Use ``--restart`` policy with MAPDL products
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default, MAPDL creates a ``LOCK`` file in the working directory when it starts
and deletes this file if it exits normally. The file is used to avoid overwriting files
such as database (DB) files or result (RST) files when starting MAPDL after an
abnormal termination.

Because of this behavior, when using the Docker ``--restart`` flag in the ``docker run``
command, you might enter into an infinite loop if you specify the Docker image to
reboot after an abnormal termination. For example, ``--restart always``. 
Because of the presence of the ``LOCK`` file, MAPDL exits, attempting to not overwrite
the files from the previous crash, while the Docker process keeps attempting to
restart the MAPDL container (and the MAPDL process with it).

In such cases, you should not use the ``--restart`` option. If you really need to use
this option, you can avoid MAPDL checks and create the ``LOCK`` file by starting
the process with the environment variable ``ANSYS_LOCK`` set to ``"OFF"``. 

You can do this in your ``docker run`` command:

.. code:: bash

  docker run \
      --restart always \
      -e ANSYSLMD_LICENSE_FILE=1055@$LICENSE_SERVER \
      -e ANSYS_LOCK="OFF" \
      -p 50052:50052 \
      $IMAGE


Get useful files after abnormal termination
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In some cases, the MAPDL container might crash after the MAPDL process experiences an
abnormal termination. In these cases, you can retrieve log files and output files using 
tools that Docker provides.

First, get the Docker container name:

.. code:: pwsh

  PS docker ps
  CONTAINER ID   IMAGE                                   COMMAND                  CREATED          STATUS          PORTS                      NAMES
  c14560bff70f   ghcr.io/pyansys/pymapdl/mapdl:v22.2.0   "/ansys_inc/ansys/bi…"   9 seconds ago    Up 8 seconds    0.0.0.0:50053->50052/tcp   mapdl

To appear in ``docker ps``, the container should be running.

You can then use the ``name`` in the following command:

.. code:: pwsh

  PS docker exec -it mapdl /bin/bash

This command executes the command shell (``/bin/bash``) of the container and attaches your current terminal to it (interactive ``-it``).

.. code:: pwsh

  PS C:\Users\user> docker exec -it mapdl /bin/bash
  [root@c14560bff70f /]#

Now you can enter commands inside the Docker container and navigate inside it.

.. code:: pwsh

  PS C:\Users\user> docker exec -it mapdl /bin/bash
  [root@c14560bff70f /]# ls
  anaconda-post.log  cleanup-ansys-c14560bff70f-709.sh  file0.err   file1.err  file1.page  file2.out   file3.log   home   media  proc  sbin  tmp
  ansys_inc          dev                                file0.log   file1.log  file2.err   file2.page  file3.out   lib    mnt    root  srv   usr
  bin                etc                                file0.page  file1.out  file2.log   file3.err   file3.page  lib64  opt    run   sys   var

You can then take note of the files you want to retrieve. For example, the error and output files (``file*.err`` and ``file*.out``).

Exit the container terminal using ``exit``:

.. code:: pwsh

  [root@c14560bff70f /]# exit
  exit
  (base) PS C:\Users\user>

You can copy the noted files using this script:

.. code:: pwsh

  docker cp mapdl:/file0.err .
  docker cp mapdl:/file1.err .
  docker cp mapdl:/file1.out .

If you want to retrieve multiple files, the most efficient approach is to get back inside the Docker container:

.. code:: pwsh

  PS C:\Users\user> docker exec -it mapdl /bin/bash
  [root@c14560bff70f /]#

Create a folder where you are going to copy all the desired files:

.. code:: pwsh

  [root@c14560bff70f /]# mkdir -p /mapdl_logs
  [root@c14560bff70f /]# cp -f /file*.out /mapdl_logs
  [root@c14560bff70f /]# cp -f /file*.err /mapdl_logs
  [root@c14560bff70f /]# ls mapdl_logs/
  file0.err  file1.err  file1.out  file2.err  file2.out  file3.err  file3.out

Then copy the entire folder content at once:

.. code:: pwsh

  docker cp mapdl:/mapdl_logs/. .

