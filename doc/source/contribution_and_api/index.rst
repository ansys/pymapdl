.. _ref_contributing:

====================
Contributing and API
====================

Overall guidance on contributing to a PyAnsys library appears in the
`Contributing <dev_guide_contributing_>`_ topic
in the *PyAnsys Developer's Guide*. Ensure that you are thoroughly familiar
with it and all `Coding style <dev_guide_coding_style_>`_ before attempting to
contribute to PyMAPDL.
 
The following contribution information is specific to PyMAPDL.


Cloning the PyMAPDL repository
==============================

Run this code to clone and install the latest version of PyMAPDL in development mode:

.. code::

    git clone https://github.com/pyansys/pymapdl
    cd pymapdl
    pip install pip -U
    pip install -e .


Posting issues
==============

Use the `PyMAPDL Issues <pymapdl_issues_>`_
page to submit questions, report bugs, and request new features. When possible,
use these issue templates:

* Bug report template
* Feature request template

If your issue does not fit into one of these categories, create your own issue.

To reach the project support team, email `pyansys.support@ansys.com <pyansys_support_>`_.

Viewing PyMAPDL documentation
=============================

Documentation for the latest stable release of PyMAPDL is hosted at
`PyMAPDL Documentation <pymapdl_docs_>`_.

Documentation for the latest development version, which tracks the
``main`` branch, is hosted at 
`Development PyMAPDL Documentation <pymapdl_dev_docs_>`_.
This version is automatically kept up to date via GitHub actions.

Testing MAPDL
=============

If you do not have MAPDL installed locally but still want to run the
unit testing, you must set up the following environment variables.

In Windows, use:

.. code::

    SET PYMAPDL_START_INSTANCE=False
    SET PYMAPDL_PORT=<MAPDL Port> (default 50052)
    SET PYMAPDL_IP=<MAPDL IP> (default 127.0.0.1)

In Linux, use:

.. code::

    export PYMAPDL_START_INSTANCE=False
    export PYMAPDL_PORT=<MAPDL Port> (default 50052)
    export PYMAPDL_IP=<MAPDL IP> (default 127.0.0.1)

This tells ``ansys.mapdl.core`` to attempt to connect to the existing
MAPDL service by default when the ``launch_mapdl`` function is used.


Code style
==========

PyMAPDL follows PEP8 standard as outlined in the `PyAnsys Development Guide
<dev_guide_pyansys_>`_ and implements style checking using
`pre-commit <precommit_>`_.

To ensure your code meets minimum code styling standards, run::

  pip install pre-commit
  pre-commit run --all-files

You can also install this as a pre-commit hook by running::

  pre-commit install

This way, it's not possible for you to push code that fails the style checks. For example::

  $ pre-commit install
  $ git commit -am "added my cool feature"
  black....................................................................Passed
  isort....................................................................Passed
  flake8...................................................................Passed
  codespell................................................................Passed


.. _ref_index_api:

API reference
=============
This page gives an overview of the API of several public PyMAPDL
classes, functions, and attributes. You can find them
on the left sidebar.

While these methods might include some MAPDL commands, they are generally
specific to PyMAPDL methods and classes. PyMAPDL methods extend existing
MAPDL methods in a Pythonic manner. For a mapping of MAPDL commands to
PyMAPDL, see :ref:`ref_mapdl_commands`.


.. toctree::
   :maxdepth: 2
   :hidden:

   commands
   database
   geometry
   helper
   inline
   krylov
   logging
   mapdl
   math
   mesh
   parameters
   plotting
   pool
   post
   solution
   xpl
   building_example
   unit_testing
