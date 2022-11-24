  .. _ref_guide_wsl:


PyAnsys libraries on a Windows Subsystem for Linux and Docker
#############################################################

This page shows you how to use a PyAnsys library, more specifically PyMAPDL,
in the Windows Subsystem for Linux (WSL). WSL is a compatibility layer for
running Linux binary executables natively on Windows 10, Windows 11, and
Windows Server 2019. For more information, see `Wikipedia WSL <WikipediaWSL_>`_.

Sections on this page walk you through the installation of WSL on Windows and then
show how to use it together with MAPDL, PyMAPDL, and Docker.

For more information about WSL, see 
`What is the Windows Subsystem for Linux <What_is_the_Windows_Subsystem_for_Linux_>`_.

.. warning::
   This approach hasn't been fully tested with a VPN connection. If you
   experience any problems connecting WSL to the internet, try to
   disconnect from the VPN.


Run PyMAPDL on WSL 
******************

Install WSL
===========

Install WSL by following Microsoft's directions at 
`Microsoft: Install WSL <install_wsl_microsoft_>`_.

Currently there are two versions of WSL: WSL1 and WSL2. Because WSL2 is
the latest and includes many improvements over WSL1, using WSL2 is highly recommended.

Install CentOS 7 WSL distribution
=================================

Install CentOS 7 WSL distribution
=================================

You should use the CentOS 7 WSL distribution for working with PyAnsys
libraries.

You can install it using an unofficial WSL distribution from
`CentOS-WSL <gh_centos_wsl_1_>`_ or
`CentOS WSL <gh_centos_wsl_2_>`_ .

Optionally, you can try Ubuntu, but it has not been tested yet in the context of WSL.


Install Ansys products in WSL CentOS 7
======================================

Prerequisites
-------------
If you are using CentOS 7, before installing MAPDL, you must install some
required libraries:

.. code:: bash
   
   sudo yum install openssl openssh-clients mesa-libGL mesa-libGLU motif libgfortran


If you are using Ubuntu, follow the instructions in `Run MAPDL: Ubuntu <pymapdl_run_ubuntu_>`_ .


Install Ansys products
----------------------

To install Ansys products in WSL Linux:

1. Download the **Ansys Structures** image from the customer portal (`Current
   Release <ansys_current_release_>`_).  If you are
   downloading the image on a Windows machine, you should later copy it from
   you downloads folder to  WSL.

2. Decompress the source code file (``tar.gz``) with:

   .. code:: bash
   
       tar xvzf STRUCTURES_2021R2_LINX64.tgz


3. To install MAPDL, go into the uncompressed folder and type:

   .. code:: bash
   
       sudo ./INSTALL -silent -install_dir /usr/ansys_inc/ -mechapdl

   where: 

   - ``-silent`` : Initiates a silent installation (no GUI).

   - ``-install_dir /path/`` : Specifies the directory to which the product or
     license manager is to be installed. If you want to install to the default
     location, you can omit the ``-install_dir`` argument. The default
     location is ``/ansys_inc`` if the symbolic link is set. Otherwise, it
     defaults to ``/usr/ansys_inc``.

   - ``-<product_flag>`` : Specifies one or more specific products to install.
     If you omit this argument, all products are installed.
     See the list of valid product flags in Chapter 6 of the *ANSYS
     Inc. Installation Guides* PDF. In this case, only MAPDL (`-mechapdl`) is
     needed.

After installing MAPDL directly in ``/ansys_inc`` or in ``/usr/ansys_inc``,
create a symbolic link with:

.. code:: bash

    sudo ln -s /usr/ansys_inc /ansys_inc

By default, PyMAPDL expects the MAPDL executable to be in
``/usr/ansys_inc``. Whether you install it there or not, you should link that directory,
using a symbolic link, to your Ansys installation directory (``/*/ansys_inc``).


Post-installation setup
=======================

Open ports
----------

**Theory:** 
You should open the ports ``1055`` and ``2325`` for the license server
communication in **Windows Firewall Advanced**. You can see the steps in 
`How to open port in Windows 10 Firewall <open_port_windows_10_>`_.

**Reality:**
This works if you want to run a Docker image using WSL Linux image to host that
Docker image. The Docker image successfully communicates with the Windows
License Server using these ports if you use the ``'-p'`` flag when running the
Docker image and these ports are open. 
See `Run MAPDL on a local Docker image`_.


If you want to run MAPDL in the CentOS 7 image and use the Windows license
server, opening the ports might not work properly because the Windows firewall
seems to block all traffic coming from WSL. For security purposes, you should
still try to open ports ``1055`` and ``2325`` in the firewall and see if your
MAPDL installation can communicate with the Windows hosts. If you are having
problems after setting the firewall rules, you might have to turn off the Windows
firewall for the WSL ethernet virtual interface. This might pose some unknown
side effects and security risk so use it with caution.
See `Disabling Firewall on WSL Ethernet <disabling_firewall_on_wsl_>`_.


Set up an environmental variable in WSL that points to Windows host license server
----------------------------------------------------------------------------------

The Windows host IP address is given in the WSL file ``/etc/hosts`` before the name
``host.docker.internal``.


.. note::
   This ``host.docker.internal`` definition might not be available if Docker is
   not installed.


**Example /etc/hosts/ file**
.. vale off


.. code-block:: bash
   :emphasize-lines: 8

   # This file was automatically generated by WSL.
   # To stop automatic generation of this file, add the following entry to /etc/wsl.conf:
   # [network]
   # generateHosts = false
   127.0.0.1       localhost
   127.0.1.1       AAPDDqVK5WqNLve.win.ansys.com   AAPDDqVK5WqNLve

   192.168.0.12    host.docker.internal
   192.168.0.12    gateway.docker.internal
   127.0.0.1       kubernetes.docker.internal

   # The following lines are desirable for IPv6 capable hosts
   ::1     ip6-localhost ip6-loopback
   fe00::0 ip6-localnet
   ff00::0 ip6-mcastprefix
   ff02::1 ip6-allnodes
   ff02::2 ip6-allrouters


.. vale on

You can add the next lines to your WSL ``~/.bashrc`` file to create an
environment variable with this IP address:

.. vale off

.. code:: bash

    winhostIP=$(grep -m 1 host.docker.internal /etc/hosts | awk '{print $1}')
    export ANSYSLMD_LICENSE_FILE=1055@$winhostIP


.. vale off


Run MAPDL on a local Docker image
*********************************

To run a Docker image, you must follow all steps in `Run PyMAPDL on WSL`_ .

Additionally, you run a Docker image of PyMAPDL with:

.. code:: pwsh

    docker run -e ANSYSLMD_LICENSE_FILE=1055@host.docker.internal --restart always --name mapdl -p 50053:50052 ghcr.io/pyansys/pymapdl/mapdl -smp > log.txt

Successive runs should restart the container or just delete it and rerun it using:

.. code:: pwsh

    docker stop mapdl
    docker container prune

    docker run -e ANSYSLMD_LICENSE_FILE=1055@host.docker.internal --restart always --name mapdl -p 50053:50052 ghcr.io/pyansys/pymapdl/mapdl -smp > log.txt


This creates a log file (``log.txt``) in your current directory location.


.. note:: Ensure that your port ``50053`` is open in your firewall.

You should use a script file (batch ``'.bat'`` or PowerShell ``'.ps'``)
to run the preceding commands all at once.

Notice that the WSL internal gRPC port (``50052``) is being mapped to a
different Windows host port (``50053``) to avoid ports conflicts.

This image is ready to be connected to from WSL or Windows Host but the port
and IP should be specified as:

.. code:: python

    from ansys.mapdl.core import launch_mapdl

    mapdl = launch_mapdl(ip='127.0.0.1', port=50053, start_instance=False) 

Or:

.. code:: python 

    from ansys.mapdl.core import Mapdl
    
    mapdl = Mapdl(ip='127.0.0.1', port=50053)


You can also specify the port and IP address using environment variables that are read when
launching the MAPDL instance:

.. code:: bash

    export PYMAPDL_START_INSTANCE=False
    export PYMAPDL_PORT=50053
    export PYMAPDL_IP=127.0.0.1


Launch Docker with UPF capabilities
===================================

If you want to specify a custom Python UPF routine, you must have the
environment variables ``ANS_USER_PATH`` and ``ANS_USE_UPF`` defined. The
former should be equal to the path where the UPF routines are located, and the
latter should be equal to ``TRUE``.

In WSL, you can do this using:

.. code:: bash

    export ANS_USER_PATH=/home/user/UPFs # Use your own path to your UPF files.
    export ANS_USE_UPF=TRUE

You can then run the Docker image with:

.. code:: bash

    docker run -e ANSYSLMD_LICENSE_FILE=1055@host.docker.internal -e ANS_USER_PATH='/ansys_jobs/upf' -e ANS_USE_UPF='TRUE' --restart always --name mapdl -p 50053:50052 ghcr.io/pyansys/pymapdl/mapdl -smp  1>log.txt

.. warning:: The use of UPFs with Docker images or PyMAPDL is still in the alpha state.


Notes
=====

The specified IP address ``127.0.0.1`` in `Run MAPDL on a local Docker image`_ is
the IP address of WSL CentOS from the WSL perspective, whereas the Windows host IP address is
normally ``127.0.1.1``. Docker builds the PyMAPDL images using the WSL
distribution as the base. Hence, PyMAPDL is running on a Linux WSL
distribution, which is running on a Windows host. Because the Docker image
shares resources with WSL, it also shares the internal IP address with the WSL
distribution.


Additional notes
****************


Other Ansys installation flags
==============================

You can obtain license server information with one of the following, inspecting
the last lines of the ``INSTALL`` file:

.. code:: bash
    
    ./INSTALL --help

Or:

.. code:: bash

    cat ./INSTALL


``-licserverinfo``
------------------

Specifies information to be used by the client for the license server. 
Valid only in conjunction with a silent installation (INSTALL). 
  
The format for a **single license server** is:

.. code:: bash

   -licserverinfo LI_port_number:FLEXlm_port_number:hostname

Example:

.. code:: bash
    
   ./INSTALL -silent -install_dir /ansys_inc/ -mechapdl -licserverinfo 2325:1055:winhostIP

The format for **three license servers** is:

.. code:: bash

   -licserverinfo LI_port_number:FLEXlm_port_number:hostname1,hostname2,hostname3
    
Example:
    
.. code:: bash

   ./INSTALL -silent -install_dir /ansys_inc/ -mechapdl -licserverinfo 2325:1055:abc,def,xyz


``-lang``
---------
Specifies a language to use for the installation of the product.


``-productfile``
----------------
You can specify an `options` file that lists the products that you want to
install. To do so, you must provide a full path to the file containing the
products to install.


IP addresses in WSL and the Windows host
========================================

Theory
------

You should be able to access the Windows host using the IP address specified in ``/etc/hosts``,
which normally is ``127.0.1.1``. This means that the local WSL IP address is
``127.0.0.1``.

Reality
-------

It is almost impossible to use ``127.0.1.1`` for connecting to the Windows
host. However, it is possible to use the ``host.docker.internal`` hostname in the
same file (``/etc/hosts``). This is an IP address that is randomly allocated, which is
an issue when you define the license server. However, if you update ``.bashrc``
as mentioned earlier, this issue is solved.



Disable firewall on WSL ethernet
==================================
This method shows a notification:

.. code:: pwsh

    Set-NetFirewallProfile -DisabledInterfaceAliases "vEthernet (WSL)"

This method does not show a notification:

.. code:: pwsh

    powershell.exe -Command "Set-NetFirewallProfile -DisabledInterfaceAliases \"vEthernet (WSL)\""


Link: `Disabling Firewall on WSL Ethernet <disabling_firewall_on_wsl_>`_

Windows 10 port forwarding
==========================


Link ports between WSL and Windows
----------------------------------

.. code:: pwsh

    netsh interface portproxy add v4tov4 listenport=1055 listenaddress=0.0.0.0 connectport=1055 connectaddress=XXX.XX.XX.XX


PowerShell command to view all forwards
---------------------------------------

.. code:: pwsh

    netsh interface portproxy show v4tov4


Delete port forwarding
----------------------

.. code:: pwsh

    netsh interface portproxy delete v4tov4 listenport=1055 listenaddres=0.0.0.0 protocol=tcp


Reset Windows network adapters
==============================

.. code:: pwsh

    netsh int ip reset all
    netsh winhttp reset proxy
    ipconfig /flushdns
    netsh winsock reset


Restart WSL service
===================

.. code:: pwsh

    Get-Service LxssManager | Restart-Service

Kill all processes with a given name
====================================

.. code:: pwsh

   Get-Process "ANSYS212" | Stop-Process


Install ``xvfb`` in CentOS 7
============================

If you want to replicate the CI/CD behavior, ``xvfb`` is needed. For more
information, see the ``.ci`` folder.

.. code:: bash

   yum install xorg-x11-server-Xvfb


Notes
*****

- PyMAPDL only works for shared-memory parallel (SMP) when running on WSL. This
  is why the flag ``-smp`` should be included.

- Because there are some incompatibilities between VPN and INTEL MPI, use the
  flag ``-mpi msmpi`` when calling MAPDL.

