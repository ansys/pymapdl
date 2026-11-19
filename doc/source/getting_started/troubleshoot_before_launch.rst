.. _ref_troubleshooting_before_launch:

Issues before launching MAPDL
=============================

This page covers problems with the Ansys installation, the location of the
MAPDL executable file, and the system dependencies that prevent MAPDL from
launching. For other problems, see :ref:`ref_troubleshooting`.

Installation issues
-------------------

.. _ref_updating_mapdl_installation:

Updating MAPDL installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~

When you update or reinstall MAPDL, PyMAPDL may still reference the old installation path
because it caches the location of the MAPDL executable.
If you uninstall MAPDL and install a new version (or move the installation), PyMAPDL might fail
to launch MAPDL due to the outdated cached path.

To resolve this, update the cached executable location as described in
:ref:`ref_default_location_executable`.
Use the :func:`save_ansys_path() <ansys.mapdl.core.save_ansys_path>` function to set the correct path to your new MAPDL installation.
This ensures PyMAPDL can find and launch the updated MAPDL version.


.. _missing_dependencies_on_linux:

Missing dependencies on Linux
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Some Linux installations might be missing required dependencies. If
you get errors like ``libXp.so.6: cannot open shared object file: No
such file or directory``, you are likely missing some necessary
dependencies.


.. tab-set::

    .. tab-item:: CentOS 7 and Rocky 8

        On CentOS 7, you can install missing dependencies with:

        .. code:: console

            user@machine:~$  yum install openssl openssh-clients mesa-libGL mesa-libGLU motif libgfortran

    .. tab-item:: Ubuntu 22.04

        On Ubuntu 22.04, use this code to install the needed dependencies:

        .. code:: console

            user@machine:~$ apt-get update

            # Install dependencies
            user@machine:~$ apt-get install -y \
                openssh-client \
                libgl1 \
                libglu1 \
                libxm4 \
                libxi6

        The preceding code takes care of everything except for ``libxp6``, which you must install
        using this code:

        .. code:: console

            # This is a workaround
            # Source: https://bugs.launchpad.net/ubuntu/+source/libxp/+bug/1517884
            user@machine:~$ apt install -y software-properties-common
            user@machine:~$ add-apt-repository -y ppa:zeehio/libxp
            user@machine:~$ apt-get update
            user@machine:~$ apt-get install -y libxp6

    .. tab-item:: Ubuntu 20.04 through 18.04

        If you are using Ubuntu 20.04 through 18.04, you can install missing dependencies with:

        .. code:: console

            user@machine:~$ apt-get update

            # Install dependencies
            user@machine:~$ apt-get install -y \
                openssh-client \
                libgl1 \
                libglu1 \
                libxm4 \
                libxi6


        The preceding code takes care of everything except for ``libxp6``, which you must
        manually download and install.

        Because ``libxpl6`` pre-depends on ``multiarch-support``, which is
        also outdated, it must be removed. Otherwise you will have a broken
        package configuration. The following code downloads and modifies the
        ``libxp6`` package to remove the ``multiarch-support`` dependency and
        then installs it via the ``dpkg`` package.

        .. code:: console

            cd /tmp
            wget http://ftp.br.debian.org/debian/pool/main/libx/libxp/libxp6_1.0.2-2_amd64.deb
            ar x libxp6_1.0.2-2_amd64.deb
            sudo tar xzf control.tar.gz
            sudo sed '/Pre-Depends/d' control -i
            sudo bash -c "tar c postinst postrm md5sums control | gzip -c > control.tar.gz"
            sudo ar rcs libxp6_1.0.2-2_amd64_mod.deb debian-binary control.tar.gz data.tar.xz
            sudo dpkg -i ./libxp6_1.0.2-2_amd64_mod.deb


    .. tab-item:: Ubuntu 16.04 and older

        If you are using Ubuntu 16.04, you can install missing dependencies with:

        .. code:: console

            user@machine:~$ apt-get update

            # Install dependencies
            user@machine:~$ apt-get install -y \
                openssh-client \
                libgl1 \
                libglu1 \
                libxm4 \
                libxi6 \
                libxp6


A useful resource is `HOW TO - Install Ansys' Required Linux Packages & Libraries <simutech_linux_dependencies_>`_.


.. _conflicts_student_version:

Conflicts with student version
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Although you can install Ansys together with other Ansys products or versions, on Windows, you
should not install a student version of an Ansys product together with its non-student version.
For example, installing both the Ansys MAPDL 2022 R2 Student Version and Ansys MAPDL 2022
R2 might cause license conflicts due to overwriting of environment variables. Having different
versions, for example the Ansys MAPDL 2022 R2 Student Version and Ansys MAPDL 2021 R1,
is fine.

If you experience issues, edit these environment variables to remove any
reference to the student version: ``ANSYSXXX_DIR``, ``AWP_ROOTXXX``, and
``CADOE_LIBDIRXXX``.
Visit :ref:`Incorrect environment variables <ref_incorrect_env_vars>` for information on how to set these environment variables
to the correct location.

.. note::
   By default if a student version is detected, PyMAPDL launches the MAPDL instance in
   ``SMP`` mode, unless another MPI option is specified.


Location of the executable file
-------------------------------

Manually set the location of the executable file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you have a non-standard install, PyMAPDL might be unable to find
your MAPDL installation. If this is the case, provide the location of MAPDL
as the first parameter to the :func:`launch_mapdl() <ansys.mapdl.core.launcher.launch_mapdl>`
function.


.. tab-set::

    .. tab-item:: Windows
        :sync: oskey

        .. code:: pycon

            >>> from ansys.mapdl.core import launch_mapdl
            >>> exec_loc = "C:/Program Files/ANSYS Inc/v241/ansys/bin/winx64/ANSYS241.exe"
            >>> mapdl = launch_mapdl(exec_loc)

    .. tab-item:: Linux
        :sync: oskey

        .. code:: pycon

            >>> from ansys.mapdl.core import launch_mapdl
            >>> exec_loc = "/usr/ansys_inc/v241/ansys/bin/ansys241"
            >>> mapdl = launch_mapdl(exec_loc)

.. _ref_default_location_executable:

Default location of the executable file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The first time that you run PyMAPDL, it detects the available Ansys installations.

Ansys installations are normally under:

.. tab-set::

    .. tab-item:: Windows
        :sync: oskey

        .. code:: text

            C:/Program Files/ANSYS Inc/vXXX

    .. tab-item:: Linux
        :sync: oskey

        .. code:: text

            /usr/ansys_inc/vXXX

        Or under:

        .. code:: text

            /ansys_inc/vXXX


By default, the Ansys installer uses the former one (``/usr/ansys_inc``) but also creates a symbolic link to the latter one (``/ansys_inc``).

.. _ref_updating_mapdl_location:

Update the cached executable location
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The first time PyMAPDL finds a valid Ansys installation, it caches its
path in the configuration file, ``config.txt``. The path for this file
is shown in this code:

.. code:: pycon

    >>> from ansys.mapdl.core.launcher import CONFIG_FILE
    >>> print(CONFIG_FILE)
    'C:\\Users\\user\\AppData\\Local\\ansys_mapdl_core\\ansys_mapdl_core\\config.txt'


In certain cases, this configuration file might become obsolete. For example, when a new
Ansys version is installed and an earlier installation is removed.

To update this configuration file with the latest path, use:

.. code:: pycon

    >>> from ansys.mapdl.core import save_ansys_path
    >>> save_ansys_path(r"C:\Program Files\ANSYS Inc\v241\ansys\bin\winx64\ansys241.exe")
    'C:\\Program Files\\ANSYS Inc\\v241\\ansys\\bin\\winx64\\ansys241.exe'

If you want to see which Ansys installations PyMAPDL has detected, use:

.. code:: pycon

    >>> from ansys.mapdl.core import get_available_ansys_installations
    >>> get_available_ansys_installations()
    {242: 'C:\\Program Files\\ANSYS Inc\\v242',
    241: 'C:\\Program Files\\ANSYS Inc\\v241',
    -242: 'C:\\Program Files\\ANSYS Inc\\ANSYS Student\\v242'}

Student versions are provided as **negative** versions because the Python dictionary
does not accept two equal keys. The result of the
:func:`get_available_ansys_installations() <ansys.tools.common.path.get_available_ansys_installations>`
method lists higher versions first and student versions last.

.. warning::
    You should not have the same Ansys product version and student version installed. For more
    information, see :ref:`conflicts_student_version`.
