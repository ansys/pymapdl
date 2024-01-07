
=========================================================
Welcome to GitHub PyMAPDL Codespaces for documentarian 📚
=========================================================


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

This Codespace has been set for helping developers to document and write examples
in PyMAPDL in the easiest way. It contains all the OS and Python dependencies
for running PyMAPDL and building the documentation in HTML and PDF.

Some of the available Python dependencies are:

* NumPy
* Pandas
* PyVista
* Sphinx
* Plotly


🧐 How to
==========

Before you start documenting PyMAPDL, see
`Write documentation <https://mapdl.docs.pyansys.com/version/dev/getting_started/write_documentation.html>`_,
which describes the necessary steps.

You can see the latest documentation on using Codespaces with PyMAPDL in
`Develop on containers <https://mapdl.docs.pyansys.com/version/dev/getting_started/devcontainer_link.html>`_.

Build the documentation
-----------------------

To build the documentation as html use the following command:

.. code:: console

    $ make html
    On codespaces. Using xvfb.
    Running Sphinx v7.2.6
    Using pandoc version: 3.1.9 to convert rst text blocks to markdown for .ipynb files
    loading pickled environment... done
    [autosummary] generating autosummary for: 404.rst, api/_autosummary/ansys.mapdl.core.Mapdl.add_file_handler.rst, api/_autosummary/ansys.mapdl.core.Mapdl.aplot.rst, ...

As you can see, ``Make`` already takes care of using ``xvfb`` before building the documentation.
Remember you can use ``make clean`` to clear the previous built.


Preview the built webpages
--------------------------

If you want to preview the built html pages, you can run a web server from the Codespace,
and access it from your local browser using the following command:

.. code:: console

    $ make start-webserver
    Starting Python server.
    You can find the webserver log in: /Users/german.ayuso/pymapdl/doc/webserver.log
    The pid of the webserver is 71867
    Starting...
    Server started at port 8000.
    If you don't see a pop up with 'Open in browser',
    you can open the port from the 'PORTS' tab by
    clicking on the 'world' icon in the port 8000.

This webserver always uses the port 8000. If you have the Python extension, Visual Studio Code should detect
that available port and offer you to open it in a tab.
If not, you can see the forwarded ports in the *PORTS* terminal tab.

To stop all webservers use the following command:

.. code:: console

    $ make stop-webserver
    Stopping webserver
    All webservers stopped

For more information, visit `Forwarding ports in your codespace <https://docs.github.com/en/codespaces/developing-in-a-codespace/forwarding-ports-in-your-codespace>`_.


😊 Finally
==========

We hope you enjoy this Codespace. 


**Happy coding! 💻**


See also
========

* `Learning PyMAPDL <https://mapdl.docs.pyansys.com/version/dev/getting_started/learning.html>`_. 
* `Contributing <https://mapdl.docs.pyansys.com/version/dev/getting_started/contribution.html#contributing>`_
