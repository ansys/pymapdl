===============
Getting started
===============
To use PyMAPDL, you must have a local installation of Ansys. The
version of Ansys installed dictates the interface and features
available to you.

For more information on getting a licensed copy of Ansys, visit
`Ansys <ansys_>`_ .

You can also try the Student Version of Ansys products in
`Ansys Student Versions <ansys_student_version_>`_.
The Student Version is valid during a calendar year with limited capabilities,
such as on the number of nodes and elements.

.. toctree::
   :hidden:
   :maxdepth: 2

   running_mapdl
   versioning
   docker
   using_julia
   wsl

************
Installation
************

Python module
~~~~~~~~~~~~~
The ``ansys.mapdl.core`` package currently supports Python 3.7 through
Python 3.10 on Windows, Mac OS, and Linux.

Install the latest release from 
`PyPi <pymapdl_pypi_>`_ with:

.. code::

   pip install ansys-mapdl-core

Alternatively, install the latest from 
`PyMAPDL GitHub <pymapdl_issues_>`_ via:

.. code::

   pip install git+https://github.com/pyansys/pymapdl.git


For a local "development" version, install with:

.. code::

   git clone https://github.com/pyansys/pymapdl.git
   cd pymapdl
   pip install -e .

This allows you to install the ``ansys-mapdl-core`` module
and modify it locally and have the changes reflected in your setup
after restarting the Python kernel.


Offline installation
~~~~~~~~~~~~~~~~~~~~
If you lack an internet connection on your install machine, the recommended way
of installing PyMAPDL is downloading the wheelhouse archive from the 
`Releases Page <pymapdl_releases_>`_ for your corresponding
machine architecture.

Each wheelhouse archive contains all the Python wheels necessary to install
PyMAPDL from scratch on Windows and Linux for Python 3.7 and 3.9. You can install
this on an isolated system with a fresh Python or on a virtual environment.

For example, on Linux with Python 3.7, unzip it and install it with the following:

.. code::

   unzip PyMAPDL-v0.62.dev1-wheelhouse-Linux-3.7.zip wheelhouse
   pip install ansys-mapdl-core -f wheelhouse --no-index --upgrade --ignore-installed

If you're on Windows with Python 3.9, unzip to a ``wheelhouse`` directory and
install using the preceding command.

Consider installing using a `virtual environment <using_venv_>`_.


Ansys software requirements
~~~~~~~~~~~~~~~~~~~~~~~~~~~
For the latest features, you must have a copy of Ansys 2021 R1
installed locally. However, PyMAPDL is compatible with Ansys 17.0 and later
on Windows and with Ansys 13.0 on Linux.

.. note::

    The latest versions of Ansys provide significantly better support
    and features. Certain features, such as APDL Math, are not supported
    on earlier Ansys versions.


Verify your installation
~~~~~~~~~~~~~~~~~~~~~~~~
Check that you can start MAPDL from Python by running:

.. code:: python

    >>> from ansys.mapdl.core import launch_mapdl
    >>> mapdl = launch_mapdl()
    >>> print(mapdl)

    Product:             ANSYS Mechanical Enterprise
    MAPDL Version:       RELEASE  2021 R1           BUILD 21.0
    PyMAPDL Version:     Version: 0.58.0

If you see a response from the server, congratulations. You're ready
to get started using MAPDL as a service. For information on the
PyMAPDL interface, see :ref:`ref_mapdl_user_guide`.
