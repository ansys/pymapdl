.. _docker:

**************************
Using MAPDL Through Docker
**************************
You can run MAPDL within a container on any OS using `docker` and
connect to it via PyMAPDL.

There are several situations in which it is advantageous to run MAPDL
in a containerized environment (e.g. Docker or singularity):

- Run in a consistent environment regardless of the host OS.
- Portability and ease of install.
- Large scale cluster deployment using Kubernetes
- Genuine application isolation through containerization.


Installing the MAPDL Image
--------------------------
There is a docker image hosted on the `PyMAPDL GitHub
<https://https://github.com/pyansys/pymapdl>`_ repository that you
can download using your GitHub credentials.

Assuming you have docker installed, you can get started by
authorizing docker to access this repository using a personal access
token.  Create a GH personal access token with ``packages read`` permissions
according to `Creating a personal access token <https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token>`_

Save that token to a file with:

.. code::

   echo XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX > GH_TOKEN.txt


This lets you send the token to docker without leaving the token value
in your history.  Next, authorize docker to access this repository
with:

.. code::

    GH_USERNAME=<my-github-username>
    cat GH_TOKEN.txt | docker login ghcr.io -u $GH_USERNAME --password-stdin


You can now launch MAPDL directly from docker with a short script or
directly from the command line.  Since this image contains no license
server, you need to enter in your license server IP address the
``LICENSE_SERVER`` environment variable.  With that, you can launch
MAPDL with:

.. code::

    LICENSE_SERVER=1055@XXX.XXX.XXX.XXX
    VERSION=v21.1.0

    IMAGE=ghcr.io/pyansys/pymapdl/mapdl:$VERSION
    docker run -e ANSYSLMD_LICENSE_FILE=$LICENSE_SERVER -p 50052:50052 $IMAGE -smp


Note that port `50052` (local to the container) is being mapped to
50052 on the host.  This makes it possible to launch several MAPDL
instances with different port mappings to allow for multiple instances
of MAPDL.

Once you've launched MAPDL you should see:

.. code::

    Start GRPC Server

    ##############################
    ### START GRPC SERVER      ###
    ##############################

    Server Executable   : MapdlGrpc Server
    Server listening on : 0.0.0.0:50052

Connecting to the MAPDL Container from Python
---------------------------------------------

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

Additional Considerations
-------------------------

Appending MAPDL options to the container process
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the command:

.. code::

    IMAGE=ghcr.io/pyansys/pymapdl/mapdl:$VERSION
    docker run -e ANSYSLMD_LICENSE_FILE=$LICENSE_SERVER -p 50052:50052 $IMAGE -smp

You can provide additional command line parameters to MAPDL by simply
appending to the docker command.  For example, you can increase the
number of processors (up to the number available on the host machine)
with the `-np` switch.  For example:

.. code::

    IMAGE=ghcr.io/pyansys/pymapdl/mapdl:$VERSION
    docker run -e ANSYSLMD_LICENSE_FILE=$LICENSE_SERVER -p 50052:50052 $IMAGE -np 4

For additional command line arguments please see the ansys
documentation at `ANSYS help <https://ansyshelp.ansys.com>`_.  Also,
be sure to have the appropriate license for additional HPC features.

Using ``--restart`` policy with MAPDL products
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default, MAPDL creates a ``LOCK`` file at the working directory when starts
and deletes it if it exits normally. This file is used to avoid overwriting the
files such as database files (``db``) or result files (``rst``) when starting
MAPDL after an abnormal termination.

Because of this behaviour, when using the docker flag ``--restart`` in ``docker run``,
you might enter in an infinite loop if you specify the docker image to reboot after an
abnormal termination (i.e. ``--restart always``). 
Because of the presence of the ``LOCK``, MAPDL exits attempting to not overwrite
the files from the previous crash, while the docker process keeps attempting to
restart the MAPDL container (and the MAPDL process with it).

In those cases, it is recommended to not use the ``--restart`` option.
In case you really need to use that option, you can avoid MAPDL checks and create
the lock file by starting the process with the environment variable ``ANSYS_LOCK``
set to ``"OFF"``. 
You can do that in your ``docker run`` command as:

.. code:: bash

  docker run \
      --restart always \
      -e ANSYSLMD_LICENSE_FILE=1055@$LICENSE_SERVER \
      -e ANSYS_LOCK="OFF" \
      -p 50052:50052 \
      $IMAGE


Using ``ANS_DEBUG_CRASH`` environment variable for debugging
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

*This an internal procedure not intended for public use, please be cautious*

You can run the MAPDL process with the environment variable ``ANS_DEBUG_CRASH=1``,
in that case, MAPDL creates a crash file named after the jobname (i.e. ``file.crash``).
This file contains information about the crash such as the memory object and files called.
An example of this file is noted below:

.. code:: text

  Dumping the crash data for the current analysis.
      /ansys_inc/v211/ansys/lib/linx64/libansys.so(+0x4432f8c) [0x7fa3b1fa5f8c]
      /ansys_inc/v211/ansys/lib/linx64/libansys.so(+0xc63bbb6) [0x7fa3ba1aebb6]
      /ansys_inc/v211/ansys/lib/linx64/libansys.so(sytrap7_+0x13) [0x7fa3b6c60483]
      /ansys_inc/v211/tp/IntelCompiler/2019.3.199/linx64/lib/intel64/libifport.so.5(portlib_handler+0x2d) [0x7fa3d7e8c1bd]
      /lib64/libc.so.6(+0x36400) [0x7fa39b29a400]
      /ansys_inc/v211/commonfiles/MPI/Intel/2018.3.222/linx64/lib/release/libmpi.so.12(+0x12f287) [0x7fa399fa5287]
      /ansys_inc/v211/commonfiles/MPI/Intel/2018.3.222/linx64/lib/release/libmpi.so.12(+0x12dea6) [0x7fa399fa3ea6]
      /ansys_inc/v211/commonfiles/MPI/Intel/2018.3.222/linx64/lib/release/libmpi.so.12(+0x13fcbc) [0x7fa399fb5cbc]
      /ansys_inc/v211/commonfiles/MPI/Intel/2018.3.222/linx64/lib/release/libmpi.so.12(+0x35e6a0) [0x7fa39a1d46a0]
      /ansys_inc/v211/commonfiles/MPI/Intel/2018.3.222/linx64/lib/release/libmpi.so.12(PMPI_Send+0x40f) [0x7fa39a2c1acf]
      /ansys_inc/v211/ansys/lib/linx64/libansys.so(cMPI_Send+0x98) [0x7fa3b314efd8]
      /ansys_inc/v211/ansys/lib/linx64/libansys.so(cansMPI_Send+0x6) [0x7fa3b2b84926]
      /ansys_inc/v211/ansys/lib/linx64/libansys.so(+0x8112003) [0x7fa3b5c85003]
      /ansys_inc/v211/ansys/lib/linx64/libansys.so(+0xab4c4a0) [0x7fa3b86bf4a0]
      /ansys_inc/v211/ansys/lib/linx64/libansys.so(+0x560133c) [0x7fa3b317433c]
      /ansys_inc/v211/ansys/lib/linx64/libansys.so(fastbegin_+0x142) [0x7fa3b5d41592]
      /ansys_inc/v211/ansys/lib/linx64/libansys.so(+0xbea4fdf) [0x7fa3b9a17fdf]
      /ansys_inc/v211/ansys/lib/linx64/libansys.so(+0xc558a96) [0x7fa3ba0cba96]
      /ansys_inc/v211/ansys/lib/linx64/libansys.so(slvrun_+0x792) [0x7fa3b9c2c9b2]
      /ansys_inc/v211/ansys/lib/linx64/libansys.so(solvcl_+0x2086) [0x7fa3b9ce9b36]
      /ansys_inc/v211/ansys/lib/linx64/libansys.so(slvdriver_+0x1d) [0x7fa3b9c0885d]
      /ansys_inc/v211/ansys/lib/linx64/libansys.so(modcmd_+0x18b) [0x7fa3b7916fdb]
      /ansys_inc/v211/ansys/bin/linx64/ansys.e() [0x410d15]
      /ansys_inc/v211/ansys/bin/linx64/ansys.e(MAIN__+0xe8) [0x4102e8]
      /ansys_inc/v211/ansys/bin/linx64/ansys.e(main+0x32) [0x4101e2]
      /lib64/libc.so.6(__libc_start_main+0xf5) [0x7fa39b286555]
      /ansys_inc/v211/ansys/bin/linx64/ansys.e() [0x4100f9]

To include this feature in your docker image just add the ``ANS_DEBUG_CRASH``
environment variable to your ``docker run`` command as:

.. code:: bash

  docker run \
      --restart always \
      -e ANSYSLMD_LICENSE_FILE=1055@$LICENSE_SERVER \
      -e ANS_DEBUG_CRASH=1 \
      -p 50052:50052 \
      $IMAGE

Getting useful files after abnormal termination
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In some cases, MAPDL container might crash after the MAPDL process experience an
abnormal termination.
In those cases it is interesting to retrieve log files, output files, etc.
Docker provides you the required tools to do that.

Firstly you need to get the docker container name.

.. code:: pwsh

  PS docker ps
  CONTAINER ID   IMAGE                                   COMMAND                  CREATED          STATUS          PORTS                      NAMES
  c14560bff70f   ghcr.io/pyansys/pymapdl/mapdl:v22.2.0   "/ansys_inc/ansys/bi…"   9 seconds ago    Up 8 seconds    0.0.0.0:50053->50052/tcp   mapdl

The container should be running to appear in ``docker ps``.
You can then use the ``name`` in the following command:

.. code:: pwsh

  PS docker exec -it mapdl /bin/bash

This command execute the command shell (``/bin/bash``) of the container and attach your current terminal to it (interactive ``-it``).

.. code:: pwsh
  PS C:\Users\user> docker exec -it mapdl /bin/bash
  [root@c14560bff70f /]#

Now you can commands inside the docker image an navigate inside it.

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

You can copy the noted files using the following script:

.. code:: pwsh

  docker cp mapdl:/file0.err .
  docker cp mapdl:/file1.err .
  docker cp mapdl:/file1.out .

In case you want to retrieve multiple files, the most efficient approach is to get back inside the docker container:

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

Then you can copy all the folder content at once:

.. code:: pwsh

  docker cp mapdl:/mapdl_logs/. .


  





