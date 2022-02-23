.. _ref_contributing:

============
Contributing
============
Overall guidance on contributing to a PyAnsys library appears in the
`Contributing <https://dev.docs.pyansys.com/overview/contributing.html>`_ topic
in the *PyAnsys Developer's Guide*. Ensure that you are thoroughly familiar
with it and all `Guidelines and Best Practices
<https://dev.docs.pyansys.com/guidelines/index.html>`_ before attempting to
contribute to PyMAPDL.
 
The following contribution information is specific to PyMAPDL.

Cloning the PyMAPDL Repository
------------------------------
Run this code to clone and install the latest version of PyMAPDL in development mode:

.. code::

    git clone https://github.com/pyansys/pymapdl
    cd pymapdl
    pip install -e .


Posting Issues
--------------
Use the `PyMAPDL Issues <https://github.com/pyansys/pymapdl/issues>`_
page to submit questions, report bugs, and request new features. When possible, we
recommend that you use these issue templates:

* Bug report template
* Feature request template

If your issue does not fit into one of these categories, create your own issue.

To reach the project support team, email `pyansys.support@ansys.com <pyansys.support@ansys.com>`_.

Viewing PyMAPDL Documentation
-----------------------------
Documentation for the latest stable release of PyMAPDL is hosted at
`PyMAPDL Documentation <https://mapdldocs.pyansys.com>`_.

Documentation for the latest development version, which tracks the
``main`` branch, is hosted at  `Development PyMAPDL Documentation <https://dev.mapdldocs.pyansys.com/>`_.
This version is automatically kept up to date via GitHub actions.

Testing MAPDL
-------------
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
