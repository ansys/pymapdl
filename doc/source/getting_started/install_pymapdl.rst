

.. _ref_pymapdl_installation:

***************
Install PyMAPDL
***************

Python module
~~~~~~~~~~~~~
The ``ansys.mapdl.core`` package currently supports Python 3.8 through
Python 3.11 on Windows, Mac OS, and Linux.

Install the latest release from `PyPi <pymapdl_pypi_>`_ with:

.. code:: console

   pip install ansys-mapdl-core

Alternatively, install the latest from 
`PyMAPDL GitHub <pymapdl_issues_>`_ via:

.. code:: console

   pip install git+https://github.com/ansys/pymapdl.git


For a local *development* version, install with:

.. code:: console

   git clone https://github.com/ansys/pymapdl.git
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
PyMAPDL from scratch on Windows and Linux for Python. You can install
this on an isolated system with a fresh Python or on a virtual environment.

For example, on Linux with Python 3.9, unzip it and install it with the following:

.. code:: console

   unzip PyMAPDL-v0.68.dev1-wheelhouse-Linux-3.9.zip wheelhouse
   pip install ansys-mapdl-core -f wheelhouse --no-index --upgrade --ignore-installed

If you're on Windows with Python 3.9, unzip to a ``wheelhouse`` directory and
install using the preceding command.

Consider installing using a `virtual environment <using_venv_>`_.

Verify your installation
~~~~~~~~~~~~~~~~~~~~~~~~

.. note::
   To use PyMAPDL, you must have a local installation of Ansys. The
   version of Ansys installed dictates the interface and features
   available to you.

   For more information on getting a licensed copy of Ansys, visit
   `Ansys <ansys_>`_.


Check that you have installed correctly the package by importing the module:

.. code:: pycon

    >>> from ansys.mapdl import core as pymapdl


Go to :ref:`ref_launch_pymapdl` to see how to launch PyMAPDL and connect it
to an MAPDL instance.
