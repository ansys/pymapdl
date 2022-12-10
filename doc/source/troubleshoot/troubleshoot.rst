

.. _debugging_launch_mapdl:

=======================
Troubleshooting PyMAPDL
=======================


*****************
Launching MAPDL
*****************

For any number of reasons, Python may fail to launch MAPDL. Here are
some approaches for debugging:

In some cases, it may be necessary to run the launch command manually from the command line.

**On Windows**

Open up a command prompt and run the version-dependent command:

.. code::

    "C:\Program Files\ANSYS Inc\v211\ansys\bin\winx64\ANSYS211.exe"

.. note::
   PowerShell users can run the preceding command without quotes.


**On Linux**

Run the version-dependent command:

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


There are many issues that can cause MAPDL not to launch, including:

- License server setup
- Running behind a VPN
- Missing dependencies
- Conflicts with a student version


Licensing issues
================

Incorrect license server configuration can prevent MAPDL from being able to get a valid license.
In such cases, you might see output **similar** to:

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


PADT has a great blog regarding ANSYS issues, and licensing is always a common issue. For 
example, see `Changes to Licensing at ANSYS 2020R1 <padt_licensing_>`_. If you are responsible
for maintaining Ansys licensing or have a personal install of Ansys, see the online
`Ansys Installation and Licensing documentation <ansys_installation_and_licensing_>`_.

For more comprehensive information, download the `ANSYS Licensing Guide <licensing_guide_pdf_>`.


Virtual private network (VPN) issues
====================================

From ANSYS 2022 R2 to ANSYS 2021 R1, MAPDL has issues launching when VPN software is running.
One issue stems from MPI communication and can be solved by either passing
the ``-smp`` option to set the execution mode to "Shared Memory
Parallel" which disables the default "Distributed Memory Parallel".
Or using a different MPI compilation, for example, if you are using Windows, you can pass
``-mpi msmpi`` to use the Microsoft MPI library instead of the default Intel MPI library.
This issue does not affect the Linux version of MAPDL.

.. note:: In you are using Windows in any of the versions from ANSYS 2022 R2 to ANSYS 2021 R1,
   the default compiler is Microsoft MPI when the MAPDL instance is launched by PyMAPDL.

.. code::

    >>> from ansys.mapdl.core import launch_mapdl
    >>> mapdl = launch_mapdl(additional_switches='-smp')

While this approach has the disadvantage of using the potentially slower shared
memory parallel mode, you'll at least be able to run MAPDL.
For more information on shared versus distributed memory, see
`High-Performance Computing for Mechanical Simulations using ANSYS <ansys_parallel_computing_guide_>`_.


In addition, if your device is inside a VPN, MAPDL might not be able to correctly
resolve the IP of the license server. Verify that the hostname or IP address of the license server
is correct.

On Windows, you can find the license configuration file that points to the license server in:

.. code:: text

    C:\Program Files\ANSYS Inc\Shared Files\Licensing\ansyslmd.ini


Incorrect environment variables
===============================

The license server can be also specified using the environment variable ``ANSYSLMD_LICENSE_FILE``.
The following code examples show how you can see the value of this environment variable on
either Windows or Linux.

**On Windows**

  .. code:: pwsh
    
    $env:ANSYSLMD_LICENSE_FILE
    1055@1.1.1.1


**On Linux**

  .. code:: bash

    printenv | grep ANSYSLMD_LICENSE_FILE


.. _missing_dependencies_on_linux:

Missing dependencies on Linux
=============================

Some Linux installations might be missing required dependencies. If
you get errors like ``libXp.so.6: cannot open shared object file: No
such file or directory``, you are likely missing some necessary
dependencies.



.. _installing_mapdl_on_centos7:

CentOS 7
--------

On CentOS 7, you can install missing dependencies with:

.. code::

    yum install openssl openssh-clients mesa-libGL mesa-libGLU motif libgfortran



.. _installing_mapdl_on_ubuntu:

Ubuntu
------

On Ubuntu 22.04, use this code to install the needed dependencies:

.. code::

    apt-get update

    # Install dependencies
    apt-get install -y \
    openssh-client \
    libgl1 \
    libglu1 \
    libxm4 \
    libxi6

The preceding code takes care of everything except for ``libxp6``, which you must install
using this code:

.. code:: bash

    # This is a workaround
    # Source: https://bugs.launchpad.net/ubuntu/+source/libxp/+bug/1517884
    apt install -y software-properties-common
    add-apt-repository -y ppa:zeehio/libxp
    apt-get update
    apt-get install -y libxp6


Ubuntu 20.04 and older
----------------------

If you are using Ubuntu 16.04, you can install ``libxp16`` with this code:

.. code:: bash

   sudo apt install libxp6. 
   
However, if you are using Ubuntu 18.04 through 20.04, you must manually
download and install the package.

Because ``libxpl6`` pre-depends on ``multiarch-support``, which is
also outdated, it must be removed. Otherwise you'll have a broken
package configuration. The following code downloads and modifies the
``libxp6`` package to remove the ``multiarch-support`` dependency and
then installs it via the ``dpkg`` package.

.. code::

    cd /tmp
    wget http://ftp.br.debian.org/debian/pool/main/libx/libxp/libxp6_1.0.2-2_amd64.deb
    ar x libxp6_1.0.2-2_amd64.deb
    sudo tar xzf control.tar.gz
    sudo sed '/Pre-Depends/d' control -i
    sudo bash -c "tar c postinst postrm md5sums control | gzip -c > control.tar.gz"
    sudo ar rcs libxp6_1.0.2-2_amd64_mod.deb debian-binary control.tar.gz data.tar.xz
    sudo dpkg -i ./libxp6_1.0.2-2_amd64_mod.deb


.. _conflicts_student_version:

Conflicts with student version
==============================

Although you can install Ansys together with other Ansys products or versions, on Windows, you
should not install a student version of an Ansys product together with its non-student version.
For example, installing both the Ansys MAPDL 2022 R2 Student Version and Ansys MAPDL 2022
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
    PS $env:AWP_ROOT222 = "C:\Program Files\ANSYS Inc\v222"  # This overwrites the env var for the terminal session only.
    PS [System.Environment]::SetEnvironmentVariable('AWP_ROOT222','C:\Program Files\ANSYS Inc\v222',[System.EnvironmentVariableTarget]::User)  # This changes the env var permanently.
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


.. note:: Launching MAPDL Student Version
   By default if a student version is detected, PyMAPDL launches the MAPDL instance in
   ``SMP`` mode, unless another MPI option is specified.

*****************
Launching PyMAPDL
*****************

Even if you are able to successfully launch MAPDL, PyMAPDL itself might not launch
successfully.


Manually set the location of the executable file
================================================
If you have a non-standard install, PyMAPDL might be unable find
your MAPDL installation. If this is the case, provide the location of MAPDL
as the first parameter to :func:`launch_mapdl() <ansys.mapdl.core.launch_mapdl>`.

**On Windows**

.. code:: python

    >>> from ansys.mapdl.core import launch_mapdl
    >>> exec_loc = 'C:/Program Files/ANSYS Inc/v211/ansys/bin/winx64/ANSYS211.exe'
    >>> mapdl = launch_mapdl(exec_loc)

**On Linux**

.. code:: python

    >>> from ansys.mapdl.core import launch_mapdl
    >>> exec_loc = '/usr/ansys_inc/v211/ansys/bin/ansys211'
    >>> mapdl = launch_mapdl(exec_loc)



Default Location of the executable file
=======================================

The first time that you run PyMAPDL, it detects the
available Ansys installations.

**On Windows**

Ansys installations are normally under:

.. code:: text

    C:/Program Files/ANSYS Inc/vXXX

**On Linux**
Ansys installations are normally under:

.. code:: text

    /usr/ansys_inc/vXXX
    
Or under:

.. code:: text

   /ansys_inc/vXXX

By default, Ansys installer uses the former one (``/usr/ansys_inc``) but also creates a symbolic to later one (``/ansys_inc``).

If PyMAPDL finds a valid Ansys installation, it caches its
path in the configuration file, ``config.txt``. The path for this file
is shown in this code:

.. code:: python

    >>> from ansys.mapdl.core.launcher import CONFIG_FILE
    >>> print(CONFIG_FILE)
    'C:\\Users\\user\\AppData\\Local\\ansys_mapdl_core\\ansys_mapdl_core\\config.txt'


In certain cases, this configuration file might become obsolete. For example, when a new
Ansys version is installed and an earlier installation is removed.

To update this configuration file with the latest path, use:

.. code:: python

    >>> from ansys.mapdl.core import save_ansys_path
    >>> save_ansys_path(r"C:\Program Files\ANSYS Inc\v222\ansys\bin\winx64\ansys222.exe")
    'C:\\Program Files\\ANSYS Inc\\v222\\ansys\\bin\\winx64\\ansys222.exe'

If you want to see which Ansys installations PyMAPDL has detected, use:

.. code:: python

    >>> from ansys.mapdl.core.launcher import get_available_ansys_installations
    >>> get_available_ansys_installations()
    {222: 'C:\\Program Files\\ANSYS Inc\\v222',
    212: 'C:\\Program Files\\ANSYS Inc\\v212',
    -222: 'C:\\Program Files\\ANSYS Inc\\ANSYS Student\\v222'}

Student versions are provided as **negative** versions because the Python dictionary
does not accept two equal keys. The result of the
:func:`get_available_ansys_installations() <ansys.mapdl.core.get_available_ansys_installations>`
method lists higher versions first and student versions last.

.. warning::
    You should not have the same Ansys product version and student version installed. For more
    information, see :ref:`conflicts_student_version`.



.. _ref_pymapdl_stability:

*****************
PyMAPDL stability
*****************

Recommendations
===============

When connecting to an instance of MAPDL using gRPC (default), there are some cases
where the MAPDL server might exit unexpectedly. There
are several ways to improve performance and stability of MADPL:

- When possible, pass ``mute=True`` to individual MAPDL commands or
  set it globally with the :func:`Mapdl.mute
  <ansys.mapdl.core.mapdl_grpc.MapdlGrpc>` method. This disables streaming
  back the response from MAPDL for each command and marginally
  improves performance and stability. Consider having a debug flag in
  your program or script so you can turn on or turn off logging and
  verbosity when needed.


Issues
======

.. note::
   MAPDL 2021 R1 has a stability issue with the :func:`Mapdl.input()
   <ansys.mapdl.core.Mapdl.input>` method. Avoid using input files if
   possible. Attempt to use the :func:`Mapdl.upload()
   <ansys.mapdl.core.Mapdl.upload>` method to upload nodes and elements and read them
   in via the :func:`Mapdl.nread() <ansys.mapdl.core.Mapdl.nread>` and
   :func:`Mapdl.eread() <ansys.mapdl.core.Mapdl.eread>` methods.





.. _ref_pymapdl_limitations:

*******************
PyMAPDL limitations
*******************


.. _ref_numpy_arrays_in_mapdl:

Issues when importing and exporting numpy arrays in MAPDL
=========================================================

Because of the way MAPDL is designed, there is no way to store an
array where one or more dimensions are zero.
This can happens in numpy arrays, where its first dimension can be
set to zero. For example:

.. code:: python

   >>> import numpy
   >>> from ansys.mapdl.core import launch_mapdl
   >>> mapdl = launch_mapdl()
   >>> my_array = np.reshape([1, 2, 3, 4], (4,))
   >>> my_array
   array([1, 2, 3, 4])


These types of array dimensions are always converted to ``1``.

For example:

.. code:: python

   >>> mapdl.parameters['mapdlarray'] = my_array
   >>> mapdl.parameters['mapdlarray']
   array([[1.],
      [2.],
      [3.],
      [4.]])
   >>> mapdl.parameters['mapdlarray'].shape
   (4, 1)

This means that when you pass two arrays, one with the second axis equal
to zero (for example, ``my_array``) and another one with the second axis equal
to one, have the same shape if later retrieved.

.. code:: python

   >>> my_other_array = np.reshape([1, 2, 3, 4], (4,1))
   >>> my_other_array
   array([[1],
      [2],
      [3],
      [4]])
   >>> mapdl.parameters['mapdlarray_b'] = my_other_array
   >>> mapdl.parameters['mapdlarray_b']
   array([[1.],
      [2.],
      [3.],
      [4.]])
   >>> np.allclose(mapdl.parameters['mapdlarray'], mapdl.parameters['mapdlarray_b'])
   True