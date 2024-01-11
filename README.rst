.. raw:: html

    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://github.com/ansys/pymapdl/blob/main/doc/source/_static/logo_dark.png">
      <source media="(prefers-color-scheme: light)" srcset="https://github.com/ansys/pymapdl/blob/main/doc/source/_static/logo_light.png">
      <img alt="pymapdl" >
    </picture>

.. raw:: html
   
   <p align="center">
      <picture>
         <source media="(prefers-color-scheme: dark)" srcset="https://github.com/ansys/pymapdl/blob/main/doc/source/_static/logo_dark.png">
         <source media="(prefers-color-scheme: light)" srcset="https://github.com/ansys/pymapdl/blob/main/doc/source/_static/logo_light.png">
         <img alt="PyMAPDL Logo" src="https://github.com/ansys/pymapdl/blob/main/doc/source/_static/logo_light.png">
      </picture>
   </p>

|pyansys| |pypi| |PyPIact| |GH-CI| |codecov| |zenodo| |MIT| |black| |pre-commit|

.. |pyansys| image:: https://img.shields.io/badge/Py-Ansys-ffc107.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAABDklEQVQ4jWNgoDfg5mD8vE7q/3bpVyskbW0sMRUwofHD7Dh5OBkZGBgW7/3W2tZpa2tLQEOyOzeEsfumlK2tbVpaGj4N6jIs1lpsDAwMJ278sveMY2BgCA0NFRISwqkhyQ1q/Nyd3zg4OBgYGNjZ2ePi4rB5loGBhZnhxTLJ/9ulv26Q4uVk1NXV/f///////69du4Zdg78lx//t0v+3S88rFISInD59GqIH2esIJ8G9O2/XVwhjzpw5EAam1xkkBJn/bJX+v1365hxxuCAfH9+3b9/+////48cPuNehNsS7cDEzMTAwMMzb+Q2u4dOnT2vWrMHu9ZtzxP9vl/69RVpCkBlZ3N7enoDXBwEAAA+YYitOilMVAAAAAElFTkSuQmCC
   :target: https://docs.pyansys.com/
   :alt: PyAnsys

.. |pypi| image:: https://img.shields.io/pypi/v/ansys-mapdl-core.svg?logo=python&logoColor=white
   :target: https://pypi.org/project/ansys-mapdl-core/

.. |PyPIact| image:: https://img.shields.io/pypi/dm/ansys-mapdl-core.svg?label=PyPI%20downloads
   :target: https://pypi.org/project/ansys-mapdl-core/

.. |codecov| image:: https://codecov.io/gh/ansys/pymapdl/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/ansys/pymapdl

.. |GH-CI| image:: https://github.com/ansys/pymapdl/actions/workflows/ci.yml/badge.svg
   :target: https://github.com/ansys/pymapdl/actions/workflows/ci.yml

.. |zenodo| image:: https://zenodo.org/badge/70696039.svg
   :target: https://zenodo.org/badge/latestdoi/70696039

.. |MIT| image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg?style=flat
  :target: https://github.com/psf/black
  :alt: black

.. |pre-commit| image:: https://results.pre-commit.ci/badge/github/ansys/pymapdl/main.svg
   :target: https://results.pre-commit.ci/latest/github/ansys/pymapdl/main
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

.. image:: https://github.com/ansys/pymapdl/raw/main/doc/source/_static/landing_page_demo.gif

PyMAPDL works within Jupyter Notebooks, the standard Python console,
or in batch mode on Windows, Linux, and even Mac OS.

Documentation and issues
------------------------
Documentation for the latest stable release of PyMAPDL is hosted at `PyMAPDL Documentation
<https://mapdl.docs.pyansys.com>`_.

In the upper right corner of the documentation's title bar, there is an option for switching from
viewing the documentation for the latest stable release to viewing the documentation for the
development version or previously released versions.

You can also `view <https://cheatsheets.docs.pyansys.com/pymapdl_cheat_sheet.png>`_ or
`download <https://cheatsheets.docs.pyansys.com/pymapdl_cheat_sheet.pdf>`_ the
PyMAPDL cheat sheet. This one-page reference provides syntax rules and commands
for using PyMAPDL. 

For troubleshooting, visit
`Troubleshooting PyMAPDL <https://mapdl.docs.pyansys.com/version/stable/user_guide/troubleshoot.html#troubleshooting-pymapdl>`_

On the `PyMAPDL Issues <https://github.com/ansys/pymapdl/issues>`_ page,
you can create issues to report bugs and request new features. On the `PyMAPDL Discussions
<https://github.com/ansys/pymapdl/discussions>`_ page or the `Discussions <https://discuss.ansys.com/>`_
page on the Ansys Developer portal, you can post questions, share ideas, and get community feedback. 

To reach the project support team, email `PyAnsys Core team <pyansys.core@ansys.com>`_.
Unfortunately, this team cannot answer specific library questions or issues. You must
use the `PyMAPDL Issues <https://github.com/ansys/pymapdl/issues>`_
and `PyMAPDL Discussions <https://github.com/ansys/pymapdl/discussions>`_ pages
for raising issues, request new features, and asking questions.

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
while supporting new features.  The original Python module has been
split up into the following projects and modules:

- `ansys.mapdl.core <https://github.com/ansys/pymapdl>`_
- `ansys.mapdl.reader <https://github.com/ansys/pymapdl-reader>`_
- `ansys.mapdl.corba <https://github.com/ansys/pymapdl-corba>`_

For more information on each project, visit their GitHub pages.


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
`the MIT license <https://github.com/ansys/pymapdl/blob/main/LICENSE>`_.

``ansys-mapdl-core`` package makes no commercial claim over Ansys
whatsoever.  This tool extends the functionality of ``MAPDL`` by
adding a Python interface to the MAPDL service without changing the
core behavior or license of the original software.  The use of the
interactive APDL control of ``PyMAPDL`` requires a legally licensed
local copy of Ansys.

To get a copy of Ansys, visit `Ansys <https://www.ansys.com/>`_.
