PyMAPDL
=======
.. image:: https://img.shields.io/pypi/v/ansys-mapdl-core.svg
    :target: https://pypi.org/project/ansys-mapdl-core/

.. image:: https://dev.azure.com/pyansys/pyansys/_apis/build/status/pyansys.pymapdl?branchName=master
    :target: https://dev.azure.com/pyansys/pyansys/_build/latest?definitionId=5&branchName=master

.. image:: https://zenodo.org/badge/70696039.svg
   :target: https://zenodo.org/badge/latestdoi/70696039


Documentation and Issues
------------------------
See the `Documentation <https://mapdldocs.pyansys.com>`_ page for more
details, and the `Examples gallery
<https://mapdldocs.pyansys.com/pyansys/examples/index.html>`_ for some
examples.

Please feel free to post issues and other questions at `PyMAPDL Issues
<https://github.com/pyansys/pymapdl/issues>`_.  This is the best place
to post questions and code.


Project Transition - Legacy Support
-----------------------------------
This project was formerly known as ``pyansys``, and we'd like to thank
all the early adopters, contributors, and users who submitted issues,
gave feedback, and contributed code through the years.  The
``pyansys`` project has been taken up Ansys and will be leveraged in
creating new Pythonic, cross-platform, and multi-language service
based interfaces for Ansys's products.  Your contributions to
``pyansys`` has shaped it into a better solution.

The ``pyansys`` project is expanding beyond just MAPDL, and while
there are many new features and changes to the original Python module,
many steps have been taken to ensure compatibility with legacy code
while supporting new features.  The original python module has been
split up into the following projects and modules:

 - `ansys.mapdl.core <https://github.com/pyansys/pymapdl>`_
 - `ansys.mapdl.reader <https://github.com/pyansys/pymapdl-reader>`_
 - `ansys.mapdl.corba <https://github.com/pyansys/pymapdl-corba>`_

Please visit the GitHub pages for further details regarding each project.


Installation
------------
The ``ansys-mapdl-core`` package currently supports Python 3.6 through
Python 3.8 on Windows, Mac OS, and Linux.

Install the latest release from `PyPi
<https://pypi.org/project/ansys-mapdl-core/>`_ with:

.. code::

   pip install ansys-mapdl-core

Alternatively, install the latest from `PyMAPDL GitHub
<https://github.com/pyansys/pymapdl/issues>`_ via:

.. code::

   pip install git+https://github.com/pyansys/pymapdl.git


For a local "development" version, install with:

.. code::

   git clone https://github.com/pyansys/pymapdl.git
   cd mapdl
   pip install -e .


Dependencies
------------
You will need a local licenced copy of ANSYS to run MAPDL prior and
including 2021R1.  If you have the latest version of 2021R1, you can
connect to a remote instance of MAPDL and do not need MAPDL installed
locally and can connect to a remote instance via gRPC.


Getting Started
---------------

Launch MAPDL Locally
~~~~~~~~~~~~~~~~~~~~
You can launch MAPDL locally directly from Python using ``launch_mapdl``:

.. code:: python

    from ansys.mapdl.core import launch_mapdl
    mapdl = launch_mapdl()

This automatically searches for the latest local version of MAPDL,
launches it as a background process, and immediately connects to it.
You can then start sending python commands to MAPDL.


Launching Manually or Connecting to a Remote Instance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you wish to connect to a session of MAPDL on a remote computer
(either locally the LAN or through the internet), first ensure you
have MAPDL started in gRPC server mode.  This example assumes you will
be launching an instance locally from Windows, but can be easily
adapted to run from Linux, or the LAN provided the necessary ports are
open.  This example specifies the port with ``-port 50052``, but this
option can be left out if you plan on using the default port 50052.

.. code::

    start "MAPDL" "%ANSYS211_DIR%\bin\winx64\ANSYS211.exe" -port 50052 -grpc

Next, connect to the instance of MAPDL from python with:

.. code:: python

    >>> from ansys.mapdl.core import Mapdl
    >>> ip = '127.0.0.1'
    >>> mapdl = Mapdl(ip=ip, port=50052, request_instance=False)
    >>> print(mapdl)


A successful connection returns:

.. code::

    Product:             ANSYS Mechanical Enterprise
    MAPDL Version:       RELEASE  2020 R2           BUILD 20.2TEST  UPDATE 20200601
    ansys.mapdl.core Version: 0.57.0


Should you wish to connect to this instance of MAPDL from a remote
computer, you substitute ``ip=`` with the LAN or WAN address of the
computer you wish to connect to.  Depending on your network settings,
you may have to open local ports or enable port redirection across the
WAN.


Basic Usage
~~~~~~~~~~~
You run MAPDL commands via:

.. code:: python

    mapdl.run('/PREP7')


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

See the full documentation at `PyMAPDL Documentation
<https://mapdldocs.pyansys.com>`_ for more details.


Run on Docker
~~~~~~~~~~~~~
Run MAPDL within a container on any OS with ``docker``!

See `MAPDL on Docker README
<https://github.com/pyansys/pymapdl/blob/master/docker/README.md>`_
for details regarding using MAPDL within a container.


Citing this Module
-------------------
If you use ``PyMAPDL`` for research and would like to cite the module
and source, you can visit `pyansys Zenodo
<https://zenodo.org/badge/latestdoi/70696039>`_ and generate the
correct citation.  For example, the BibTex citation is:

.. code::

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

Please visit the link above for the most recent citation as the
citation here may not be current.


License and Acknowledgments
---------------------------
``PyMAPDL`` is licensed under the MIT license.

This module, ``ansys-mapdl-core`` makes no commercial claim over Ansys
whatsoever.  This tool extends the functionality of ``MAPDL`` by
adding a Python interface to the MAPDL service without changing the
core behavior or license of the original software.  The use of the
interactive APDL control of ``PyMAPDL`` requires a legally licensed
local copy of Ansys.

To get a copy of Ansys, please visit `Ansys <https://www.ansys.com/>`_.
