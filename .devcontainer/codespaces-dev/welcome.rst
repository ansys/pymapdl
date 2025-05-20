
======================================================
Welcome to GitHub PyMAPDL Codespaces for developers 💻
======================================================


🛑 Disclaimer
=============

**You must use this Codespace only for developing, contributing, documenting, and
writing examples for PyMAPDL**.

Additionally, this Codespace is using an MAPDL Student version. For information on how Ansys
supports your learning Ansys software, see the
`Ansys for Students <https://www.ansys.com/academic/students>`_ page on the Ansys website.
The Ansys Student version has some limitations. For more information, see the
`Ansys Student - Free Software Download <https://www.ansys.com/academic/students/ansys-student>`_
page on the Ansys website.


📖 Codespace configuration
==========================

This codespace has been set for helping developers to work in PyMAPDL in the
easiest way. This codespace contains all the OS and Python dependencies
for running PyMAPDL.

Some of the available Python dependencies are:

* NumPy
* Pandas
* PyVista
* Pytest


🧐 How to
=========

To start developing PyMAPDL, see
`Develop code - Getting started <https://mapdl.docs.pyansys.com/version/dev/getting_started/develop_pymapdl.html>`_
which describes the necessary steps.

You can see the latest documentation on using Codespaces with PyMAPDL in
`here <https://mapdl.docs.pyansys.com/version/dev/getting_started/devcontainer_link.html>`_.

Testing
-------

To test new features and check their compatibility with the current library,
you need to implement unit tests.
Details on how to implement unit tests can be found in
`Unit testing <https://mapdl.docs.pyansys.com/version/dev/getting_started/develop_pymapdl.html#unit-testing>`_.
But remember to use ``xvfb-run`` when you call the ``pytest`` library.

.. code:: console

    (.venv) mapdl@machine:~/pymapdl$ xvfb-run pytest
    ====================================== test session starts ======================================
    platform linux -- Python 3.10.12, pytest-7.4.4, pluggy-1.3.0
    rootdir: /home/mapdl/pymapdl
    configfile: pyproject.toml
    ...

For more information visit `Develop code <https://mapdl.docs.pyansys.com/version/dev/getting_started/develop_pymapdl.html#develop-pymapdl>`_.


Issues
======

For troubleshooting, visit
`Troubleshooting PyMAPDL <https://mapdl.docs.pyansys.com/version/stable/user_guide/troubleshoot.html#troubleshooting-pymapdl>`_

On the `PyMAPDL Issues <https://github.com/ansys/pymapdl/issues>`_ page,
you can create issues to report bugs and request new features.
On the `PyMAPDL Discussions <https://github.com/ansys/pymapdl/discussions>`_ page or
the `Discussions <https://discuss.ansys.com/>`_ page on the Ansys Developer portal,
you can post questions, share ideas, and get community feedback. 


😊 Finally
==========

We hope you enjoy this Codespace.


**Happy coding! 💻**


See also
========

* `Learning PyMAPDL <https://mapdl.docs.pyansys.com/version/dev/getting_started/learning.html>`_
* `Develop on Codespaces <https://mapdl.docs.pyansys.com/version/dev/getting_started/codespaces.html#develop-on-codespaces>`_
* `Contributing <https://mapdl.docs.pyansys.com/version/dev/getting_started/contribution.html#contributing>`_
