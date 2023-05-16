PyMAPDL
=======
|pyansys| |pypi| |PyPIact| |GH-CI| |codecov| |zenodo| |MIT| |black| |pre-commit|

.. |pyansys| image:: https://img.shields.io/badge/Py-Ansys-ffc107.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAABDklEQVQ4jWNgoDfg5mD8vE7q/3bpVyskbW0sMRUwofHD7Dh5OBkZGBgW7/3W2tZpa2tLQEOyOzeEsfumlK2tbVpaGj4N6jIs1lpsDAwMJ278sveMY2BgCA0NFRISwqkhyQ1q/Nyd3zg4OBgYGNjZ2ePi4rB5loGBhZnhxTLJ/9ulv26Q4uVk1NXV/f///////69du4Zdg78lx//t0v+3S88rFISInD59GqIH2esIJ8G9O2/XVwhjzpw5EAam1xkkBJn/bJX+v1365hxxuCAfH9+3b9/+////48cPuNehNsS7cDEzMTAwMMzb+Q2u4dOnT2vWrMHu9ZtzxP9vl/69RVpCkBlZ3N7enoDXBwEAAA+YYitOilMVAAAAAElFTkSuQmCC
   :target: https://docs.pyansys.com/
   :alt: PyAnsys

.. |pypi| image:: https://img.shields.io/pypi/v/ansys-mapdl-core.svg?logo=python&logoColor=white
   :target: https://pypi.org/project/ansys-mapdl-core/

.. |PyPIact| image:: https://img.shields.io/pypi/dm/ansys-mapdl-core.svg?label=PyPI%20downloads
   :target: https://pypi.org/project/ansys-mapdl-core/

.. |codecov| image:: https://codecov.io/gh/pyansys/pymapdl/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/pyansys/pymapdl

.. |GH-CI| image:: https://github.com/pyansys/pymapdl/actions/workflows/ci.yml/badge.svg
   :target: https://github.com/pyansys/pymapdl/actions/workflows/ci.yml

.. |zenodo| image:: https://zenodo.org/badge/70696039.svg
   :target: https://zenodo.org/badge/latestdoi/70696039

.. |MIT| image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg?style=flat
  :target: https://github.com/psf/black
  :alt: black

.. |pre-commit| image:: https://results.pre-commit.ci/badge/github/pyansys/pymapdl/main.svg
   :target: https://results.pre-commit.ci/latest/github/pyansys/pymapdl/main
   :alt: pre-commit.ci status

Overview
--------
The PyMAPDL project supports Pythonic access to MAPDL to be able to
communicate with the MAPDL process directly from Python. The latest
``ansys-mapdl-core`` package enables a more comprehensive interface with
MAPDL and supports:

- All the features of the original module (for example, Pythonic commands
  and interactive sessions).
- Remote connections to MAPDL from anywhere via gRPC.
- Direct access to MAPDL arrays, meshes, and geometry as Python
  objects.
- Low-level access to the MAPDL solver through APDL math in a SciPy-
  like interface.

Here's a quick demo of PyMAPDL within Visual Studio Code:

.. image:: https://github.com/pyansys/pymapdl/raw/main/doc/landing_page_demo.gif

PyMAPDL works within Jupyter Notebooks, the standard Python console,
or in batch mode on Windows, Linux, and even Mac OS.

Documentation and issues
------------------------
For more information, see the `Documentation <https://mapdl.docs.pyansys.com>`_ page.
For some examples, see the `Examples gallery <https://mapdl.docs.pyansys.com/examples/index.html>`_.

Feel free to post issues and other questions at `PyMAPDL Issues
<https://github.com/pyansys/pymapdl/issues>`_.  This is the best place
to post questions and code.



Project transition - legacy support
-----------------------------------
This project was formerly known as ``pyansys``, and we'd like to thank
all the early adopters, contributors, and users who submitted issues,
gave feedback, and contributed code through the years.  The
``pyansys`` project has been taken up at Ansys and is being leveraged in
creating new Pythonic, cross-platform, and multi-language service-based
interfaces for Ansys's products.  Your contributions to
``pyansys`` has shaped it into a better solution.

The ``pyansys`` project is expanding beyond just MAPDL, and while
there are many new features and changes to the original Python module,
many steps have been taken to ensure compatibility with legacy code
while supporting new features.  The original python module has been
split up into the following projects and modules:

- `ansys.mapdl.core <https://github.com/pyansys/pymapdl>`_
- `ansys.mapdl.reader <https://github.com/pyansys/pymapdl-reader>`_
- `ansys.mapdl.corba <https://github.com/pyansys/pymapdl-corba>`_

For more information on each project, visit their GitHub pages.


Installation
------------
The ``ansys-mapdl-core`` package currently supports Python 3.7 through
Python 3.10 on Windows, Mac OS, and Linux.

Install the latest release from `PyPi
<https://pypi.org/project/ansys-mapdl-core/>`_ with:

.. code:: console

   pip install ansys-mapdl-core

Alternatively, install the latest from `PyMAPDL GitHub
<https://github.com/pyansys/pymapdl/issues>`_ via:

.. code:: console

   pip install git+https://github.com/pyansys/pymapdl.git


For a local "development" version, install with (requires pip >= 22.0):

.. code:: console

   git clone https://github.com/pyansys/pymapdl.git
   cd pymapdl
   pip install -e .


Offline installation
~~~~~~~~~~~~~~~~~~~~
If you lack an internet connection on your install machine, the recommended way
of installing PyMAPDL is downloading the wheelhouse archive from the `Releases
Page <https://github.com/pyansys/pymapdl/releases>`_ for your corresponding
machine architecture.

Each wheelhouse archive contains all the python wheels necessary to install
PyMAPDL from scratch on Windows and Linux for Python 3.7 and 3.9. You can install
this on an isolated system with a fresh python or on a virtual environment.

For example, on Linux with Python 3.7, unzip it and install it with the following:

.. code:: console

   unzip PyMAPDL-v0.62.dev1-wheelhouse-Linux-3.7.zip wheelhouse
   pip install ansys-mapdl-core -f wheelhouse --no-index --upgrade --ignore-installed

If you're on Windows with Python 3.9, unzip to a ``wheelhouse`` directory and
install using the same command as above.

Consider installing using a `virtual environment
<https://docs.python.org/3/library/venv.html>`_.


Dependencies
------------
You must have a local licenced copy of Ansys to run MAPDL prior and
including 2021R1.  If you have the latest version of 2021R1 you do
not need MAPDL installed locally and can connect to a remote instance.


Getting started
---------------

Launch MAPDL locally
~~~~~~~~~~~~~~~~~~~~
You can launch MAPDL locally directly from Python using ``launch_mapdl``:

.. code:: python

    from ansys.mapdl.core import launch_mapdl

    mapdl = launch_mapdl()

This automatically searches for the latest local version of MAPDL,
launches it as a background process, and immediately connects to it.
You can then start sending python commands to MAPDL.


Launching manually or connecting to a remote instance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you want to connect to a session of MAPDL on a remote computer
(either locally the LAN or through the internet), first ensure you
have MAPDL started in gRPC server mode.  This example assumes that you
are launching an instance locally from Windows, but it can be easily
adapted to run from Linux, or the LAN provided the necessary ports are
open. This example specifies the port with ``-port 50052``, but this
option can be left out if you plan on using the default port 50052.

.. code:: pwsh-session

    start "MAPDL" "%ANSYS211_DIR%\bin\winx64\ANSYS211.exe" -port 50052 -grpc

Next, connect to the instance of MAPDL from python with:

.. code:: pycon

    >>> from ansys.mapdl.core import Mapdl
    >>> ip = "127.0.0.1"
    >>> mapdl = Mapdl(ip=ip, port=50052, start_instance=False)
    >>> print(mapdl)


A successful connection returns:

.. code:: output

    Product:             ANSYS Mechanical Enterprise
    MAPDL Version:       RELEASE  2020 R2           BUILD 20.2TEST  UPDATE 20200601
    ansys.mapdl.core Version: 0.57.0


Should you want to connect to this instance of MAPDL from a remote
computer, you substitute ``ip=`` with the LAN or WAN address of the
computer you wish to connect to.  Depending on your network settings,
you may have to open local ports or enable port redirection across the
WAN.


Basic usage
~~~~~~~~~~~
You run MAPDL commands via:

.. code:: python

    mapdl.run("/PREP7")


Nearly all the built-in MAPDL commands have an associated pythonic
method mapped to it.  For example, `/PREP7` is:

.. code:: python

    mapdl.prep7()


There are also non-mapdl commands such as ``mapdl.eplot`` which plot
elements using ``vtk`` and ``pyvista`` rather than relying on MAPDL's
graphics server.  Another is ``mapdl.vget``, which leverages gRPC to
rapidly exchange binary arrays from MAPDL to Python rather than
relying on file IO to exchange data.

Additionally, there are the ``post_processing``, ``geometry``, and
``mesh`` properties, which you can use to perform remote (or local)
post processing without result file exchange, display geometry
properties, or view mesh statistics.  Additionally, there's the
``parameters`` property which shows the active MAPDL parameters, and
you can use to send or receive arrays between MAPDL and Python.

For more information, see the full documentation at `PyMAPDL Documentation
<https://mapdl.docs.pyansys.com>`_.

Citing this module
-------------------
If you use ``PyMAPDL`` for research and would like to cite the module
and source, you can visit `pyansys Zenodo
<https://zenodo.org/badge/latestdoi/70696039>`_ and generate the
correct citation.  For example, the BibTex citation is:

.. code:: bibtex

    @software{alexander_kaszynski_2020_4009467,
      author       = {Alexander Kaszynski},
      title        = {{pyansys: Python Interface to MAPDL and Associated 
                       Binary and ASCII Files}},
      month        = aug,
      year         = 2020,
      publisher    = {Zenodo},
      version      = {0.43.2},
      doi          = {10.5281/zenodo.4009467},
      url          = {https://doi.org/10.5281/zenodo.4009467}
    }

Because the citation here might not be current, visit the link above to obtain
the most recent citation.


License and acknowledgments
---------------------------
``PyMAPDL`` is licensed under
`the MIT license <https://github.com/pyansys/pymapdl/blob/main/LICENSE>`_.

``ansys-mapdl-core`` package makes no commercial claim over Ansys
whatsoever.  This tool extends the functionality of ``MAPDL`` by
adding a Python interface to the MAPDL service without changing the
core behavior or license of the original software.  The use of the
interactive APDL control of ``PyMAPDL`` requires a legally licensed
local copy of Ansys.

To get a copy of Ansys, visit `Ansys <https://www.ansys.com/>`_.
