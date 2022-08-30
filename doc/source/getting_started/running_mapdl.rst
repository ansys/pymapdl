.. _using_standard_install:

***************************************
Using PyMAPDL from the Standard Install
***************************************

The pyansys ``ansys-mapdl-core`` package requires either a local or
remote instance of MAPDL to communicate with it.  This section covers
launching and interfacing with MAPDL from a local instance by
launching it from Python.

Installing MAPDL
----------------

MAPDL is installed by default from the standard installer.  When
installing ANSYS, verify that the "Mechanical Products" option is
checked under the "Structural Mechanics" option.  The standard
installer options may change, but for reference see the following
figure.

.. figure:: ../images/unified_install_2019R1.jpg
    :width: 400pt


Launching MAPDL
---------------

Launching MAPDL locally
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can use the ``launch_mapdl`` function to have Python startup MAPDL and
automatically connect to it:

.. code:: python

    >>> from ansys.mapdl.core import launch_mapdl
    >>> mapdl = launch_mapdl()
    >>> print(mapdl)

    Product:             ANSYS Mechanical Enterprise
    MAPDL Version:       RELEASE  2021 R1           BUILD 21.0
    PyMAPDL Version:     Version: 0.57.0


This is the easiest and fastest way to get PyMAPDL up and running. 
But you need to have an ANSYS license server installed locally. 

Launching a gRPC MAPDL session
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
You can start MAPDL from the command line and then connect to it.
To launch MAPDL on Windows (assuming a ``C:/Program Files/ANSYS Inc/v211`` installation) use:

.. code::

    C:/Program Files/ANSYS Inc/v211/ansys/bin/winx64/ANSYS211.exe -grpc

Or on Linux (assuming a ``/usr/ansys_inc`` installation):

.. code::

    /usr/ansys_inc/v211/ansys/bin/ansys211 -grpc

This starts up MAPDL in gRPC mode, and MAPDL should output:

.. code::

     Start GRPC Server

     ##############################
     ### START GRPC SERVER      ###
     ##############################

     Server Executable   : MapdlGrpc Server
     Server listening on : 0.0.0.0:50052

You can configure the port MAPDL starts on with the ``-port`` argument.  For
example, you can startup the server to listen for connections at 
port 50005 with:

.. code::

    /usr/ansys_inc/v211/ansys/bin/ansys211 -port 50005 -grpc

You can also configure the IP. 
However because of an ANSYS limitation to receive
strings from command line, the IP needs to be read from an external file 
called ``mylocal.ip``. This file is read automatically from the directory where 
MAPDL is running.

You can then setup the IP in Windows (Powershell and CMD) with:

.. code::
    
    echo "127.0.0.1" > mylocal.ip
    C:/Program Files/ANSYS Inc/v211/ansys/bin/winx64/ANSYS211.exe -grpc


or in Linux with:

.. code::
    
    echo "127.0.0.1" > mylocal.ip
    /usr/ansys_inc/v211/ansys/bin/ansys211 -grpc


Connecting to a gRPC MAPDL session
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A MAPDL gRPC server can be connected to either from the same host, or from an
external host.  For example, you can connect to a MAPDL service
running **locally** with:

.. code::

    >>> from ansys.mapdl.core import Mapdl
    >>> mapdl = Mapdl()


This assumes that your MAPDL service is running locally on the default ip 
(127.0.0.1) and on the default port (50052).  

If you want to connect to a **remote** instance of MAPDL and you know the IP 
address of that instance, you can connect to it.
For example, if on your local network at IP ``192.168.0.1`` there is a
computer running MAPDL on the port 50052, you can connect to it with

.. code::

    >>> mapdl = Mapdl('192.168.0.1', port=50052)

Alternatively you can use a hostname:

.. code:: python

    >>> mapdl = Mapdl('myremotemachine', port=50052)

Please note that you must have started MAPDL in gRPC mode in the PC with
the mentioned IP/hostname for this to work.
If you have MAPDL installed on your local host, you
can use ``launch_mapdl`` to both start and connect to MAPDL.


Debugging Launching MAPDL
-------------------------
For any number of reasons, Python may fail to launch MAPDL.  Here's
some approaches to debug the start:


Manually Set the Executable Location
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
If you have a non-standard install, ``pymapdl`` may be unable find
your installation.  If that's the case, provide the location of MAPDL
as the first parameter to ``launch_mapdl``.  For example, on Windows,
this will be:

.. code:: python

    >>> from ansys.mapdl.core import launch_mapdl
    >>> exec_loc = 'C:/Program Files/ANSYS Inc/v211/ansys/bin/winx64/ANSYS211.exe'
    >>> mapdl = launch_mapdl(exec_loc)

For Linux:

.. code:: python

    >>> from ansys.mapdl.core import launch_mapdl
    >>> exec_loc = '/usr/ansys_inc/v211/ansys/bin/ansys211'
    >>> mapdl = launch_mapdl(exec_loc)

Should this fail to launch or hang while launching, pass
``verbose_mapdl=True`` when using ``launch_mapdl``.  This will print
the output of MAPDL within Python and can be used to debug why MAPDL
isn't launching. On Windows, output is limited due to the way
MAPDL launches.

Default Executable Location
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The first time that you run PyMAPDL, it detects the
available ANSYS installations.

On Windows, Ansys installations are normally under:

.. code:: text

    C:/Program Files/ANSYS Inc/vXXX

On Linux, Ansys installations are normally under:

.. code:: text

    /usr/ansys_inc/vXXX

If PyMAPDL finds a valid ANSYS installation, it caches its
path in the configuration file, ``config.txt``, whose path is shown in the
following code:

.. code:: python

    >>> from ansys.mapdl.core.launcher import CONFIG_FILE
    >>> print(CONFIG_FILE)
    'C:\\Users\\user\\AppData\\Local\\ansys_mapdl_core\\ansys_mapdl_core\\config.txt'


In certain cases, this configuration might become obsolete. For example, when a new
Ansys version is installed and an earlier installation is removed.
To update this configuration file with the latest path, use:

.. code:: python

    >>> from ansys.mapdl.core import save_ansys_path
    >>> save_ansys_path(r"C:\Program Files\ANSYS Inc\v222\ansys\bin\winx64\ansys222.exe")
    'C:\\Program Files\\ANSYS Inc\\v222\\ansys\\bin\\winx64\\ansys222.exe'

If you want to check which Ansys installations PyMAPDL has detected, use:

.. code:: python

    >>> from ansys.mapdl.core.launcher import _get_available_base_ansys
    >>> _get_available_base_ansys()
    {222: 'C:\\Program Files\\ANSYS Inc\\v222',
    212: 'C:\\Program Files\\ANSYS Inc\\v212',
    -222: 'C:\\Program Files\\ANSYS Inc\\ANSYS Student\\v222'}

Student versions are provided as negative versions because the Python dictionary
does not accept two equal keys. The result of the ``_get_available_base_ansys()`` method
lists higher versions first and student versions last.

.. warning::
    You should not have the same Ansys product version and student version installed. For more
    information, see `Debug Launch Issues`_.

Debug Launch Issues
~~~~~~~~~~~~~~~~~~~
In some cases, it may be necessary to debug why MAPDL isn't launching
by running the launch command manually from the command line.  In
Windows, open up a command prompt and run the following (version
dependent) command:

.. code::

    "C:\Program Files\ANSYS Inc\v211\ansys\bin\winx64\ANSYS211.exe"

.. note::
   Powershell users can run the above without quotes.


For Linux:

.. code::

    /usr/ansys_inc/v211/ansys/bin/ansys211

You should start MAPDL in a temporary working directory because MAPDL creates
several temporary files.

You can specify a directory by launching MAPDL from the temporary directory:

.. code:: pwsh

    mkdir temporary_directory
    cd temporary_directory
     & 'C:\Program Files\ANSYS Inc\v222\ansys\bin\winx64\ANSYS222.exe'

Or, you can specify the directory using the ``-dir`` flag:

.. code:: pwsh

    mkdir temporary_directory
    & 'C:\Program Files\ANSYS Inc\v222\ansys\bin\winx64\ANSYS222.exe' -dir "C:\ansys_job\mytest1"


If this command doesn't launch MAPDL, look at the command output:

.. code:: pwsh

    (base) PS C:\Users\user\temp> & 'C:\Program Files\ANSYS Inc\v222\ansys\bin\winx64\ANSYS222.exe'
    *** ERROR ***
    Another Ansys job with the same job name (file) is already running in this
    directory or the file.lock file has not been deleted from an abnormally
    terminated Ansys run. To disable this check, set the ANSYS_LOCK environment
    variable to OFF.


There are many issues that can cause Ansys not to launch, including:

- License server setup
- Running behind a VPN
- Missing dependencies
- Conflicts with a student version


Licensing Issues
----------------

Incorrect license server configuration can prevent Ansys from being able to get a valid license.
In those cases, you might see output **similar** to:

.. code:: pwsh

   (base) PS C:\Users\user\temp> & 'C:\Program Files\ANSYS Inc\v222\ansys\bin\winx64\ANSYS222.exe'

   ANSYS LICENSE MANAGER ERROR:

   Maximum licensed number of demo users already reached.


   ANSYS LICENSE MANAGER ERROR:

   Request name mech_2 does not exist in the licensing pool.
   No such feature exists.
   Feature:          mech_2
   License path:  C:\Users\user\AppData\Local\Temp\\cb0400ba-6edb-4bb9-a333-41e7318c007d;
   FlexNet Licensing error:-5,357


PADT generally has a great blog regarding ANSYS issues, and licensing is always a common issue 
(for example `Changes to Licensing at ANSYS 2020R1 <https://www.padtinc.com/blog/15271-2/>`_).  
Should you be responsible for maintaining Ansys licensing or have a personal install of Ansys,
please check the online Ansys licensing documentation at 
`Installation and Licensing <https://ansyshelp.ansys.com/account/secured?returnurl=/Views/Secured/prod_page.html?pn=Installation%20and%20Licensing&pid=InstallationAndLicensing&lang=en>`_.

For more comprehensive information, download the :download:`ANSYS Licensing Guide <ANSYS_Inc._Licensing_Guide.pdf>`.


VPN Issues
----------
Sometimes, MAPDL has issues starting when VPN software is running.  One
issue stems from MPI communication and can be solved by passing
the ``-smp`` option that sets the execution mode to "Shared Memory
Parallel", rather than the default "Distributed Memory Parallel" mode.

.. code::

    >>> from ansys.mapdl.core import launch_mapdl
    >>> mapdl = launch_mapdl(additional_switches='-smp')

While this approach has the disadvantage of using the potentially slower shared memory parallel mode, you'll at least be able to run MAPDL.  For more details on shared vs distributed memory, see `High-Performance Computing for Mechanical Simulations using ANSYS <https://www.ansys.com/-/media/Ansys/corporate/resourcelibrary/presentation/hpc-for-mechanical-ansys.pdf>`_.


In addition, if your device is inside a virtual private network (VPN), ANSYS might have some problems to correctly
resolve the IP of the license server. Please do check that the hostname or IP of the license server
is correct.
In Windows, you can find the license configuration file that points to the license server in:

.. code:: text

    C:\Program Files\ANSYS Inc\Shared Files\Licensing\ansyslmd.ini


Incorrect environment variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The license server can be also specified using the environment variable ``ANSYSLMD_LICENSE_FILE``.
You can check the value of this environment variable by issuing on Windows:

  .. code:: pwsh
    
    $env:ANSYSLMD_LICENSE_FILE
    1055@1.1.1.1

  And on linux:

  .. code:: bash

    printenv | grep ANSYSLMD_LICENSE_FILE


Missing Dependencies on Linux
-----------------------------
Some Linux installations may be missing required dependencies.  Should
you get errors like ``libXp.so.6: cannot open shared object file: No
such file or directory``, you may be missing some necessary
dependencies.

CentOS
~~~~~~
On CentOS 7, you can install these with:

.. code::

    yum install openssl openssh-clients mesa-libGL mesa-libGLU motif libgfortran


Ubuntu
~~~~~~
Since MAPDL isn't officially supported on Ubuntu, it's a bit more
difficult to setup, but it's still possible.  On Ubuntu 20.04 with
Ansys 2021R1, install the following:

.. code::

    sudo apt-get install libx11-6 libgl1 libxm4 libxt6 libxext6 libxi6 libx11-6 libsm6 libice6 libxxf86vm1 libglu1

This takes care of everything except for ``libxp6``.  Should you be
using Ubuntu 16.04, you can install that simply with ``sudo apt
install libxp6``.  However, on Ubuntu 18.04+, you must manually
download and install the package.

Since ``libxpl6`` also pre-depends on ``multiarch-support``, which is
also outdated, it must be removed, otherwise you'll have a broken
package configuration.  The following step downloads and modifies the
``libxp6`` package to remove the ``multiarch-support`` dependency, and
then installs it via ``dpkg``.

.. code::

    cd /tmp
    wget http://ftp.br.debian.org/debian/pool/main/libx/libxp/libxp6_1.0.2-2_amd64.deb
    ar x libxp6_1.0.2-2_amd64.deb
    sudo tar xzf control.tar.gz
    sudo sed '/Pre-Depends/d' control -i
    sudo bash -c "tar c postinst postrm md5sums control | gzip -c > control.tar.gz"
    sudo ar rcs libxp6_1.0.2-2_amd64_mod.deb debian-binary control.tar.gz data.tar.xz
    sudo dpkg -i ./libxp6_1.0.2-2_amd64_mod.deb



Conflicts with Student Version
------------------------------

Although you can install Ansys together with other Ansys products or versions, on Windows, you
should not install a student version of an Ansys product together with its non-student version.
For example, installing both the Ansys MAPDL 202 2R2 Student Version and Ansys MAPDL 2022
R2 might cause license conflicts due to overwriting of environment variables. Having different
versions, for example the Ansys MAPDL 2022 R2 Student Version and Ansys MAPDL 2021 R1,
is fine.

If you experience issues, you should edit these environment variables to remove any
reference to the student version: ``ANSYSXXX_DIR``, ``AWP_ROOTXXX``, and
``CADOE_LIBDIRXXX``. The three-digit MAPDL version appears where ``XXX`` is
shown. For Ansys MAPDL 2022 R2, ``222`` appears where ``XXX`` is shown.

.. code:: pwsh

    PS echo $env:AWP_ROOT222
    C:\Program Files\ANSYS Inc\ANSYS Student\v222
    PS $env:AWP_ROOT222 = "C:\Program Files\ANSYS Inc\v222"  # This will overwrite the env var for the terminal session only.
    PS [System.Environment]::SetEnvironmentVariable('AWP_ROOT222','C:\Program Files\ANSYS Inc\v222',[System.EnvironmentVariableTarget]::User)  # This will change the env var permanently.
    PS echo $env:AWP_ROOT222
    C:\Program Files\ANSYS Inc\v222

    PS echo $env:ANSYS222_DIR
    C:\Program Files\ANSYS Inc\ANSYS Student\v222\ANSYS
    PS [System.Environment]::SetEnvironmentVariable('ANSYS222_DIR','C:\Program Files\ANSYS Inc\v222\ANSYS',[System.EnvironmentVariableTarget]::User)
    PS echo $env:ANSYS222_DIR
    C:\Program Files\ANSYS Inc\v222\ANSYS

    PS echo $env:CADOE_LIBDIR222
    C:\Program Files\ANSYS Inc\ANSYS Student\v222\CommonFiles\Language\en-us
    PS [System.Environment]::SetEnvironmentVariable('CADOE_LIBDIR222','C:\Program Files\ANSYS Inc\v222\CommonFiles\Language\en-us',[System.EnvironmentVariableTarget]::User)
    PS echo $env:CADOE_LIBDIR222
    C:\Program Files\ANSYS Inc\v222\CommonFiles\Language\en-us
