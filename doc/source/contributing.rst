.. _contributing:

============
Contributing
============
Overall guidance on contributing to a PyAnsys library appears in the
`Contributing <https://dev.docs.pyansys.com/overview/contributing.html>`_ topic
in the *PyAnsys Developer's Guide*. Ensure that you are thoroughly familiar
with it and all `Guidelines and Best Practices <https://dev.docs.pyansys.com/guidelines/index.html>`_
before attempting to contribute to PyMAPDL.
 
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
Documentation for the latest stable release of PyAEDT is hosted at
`PyMAPDL Documentation <https://mapdldocs.pyansys.com>`_, and latest development documentation at `PyMAPDL Development Documentation <https://dev.mapdldocs.pyansys.com>`_.  

Logging in PyMAPDL
------------------

To make the logging of events consistent, PyMAPDL 0.60 introduced a specific logging architecture
with two main logging levels: global and instance. 

For these two types of loggers, the default log message format is:

.. code:: python

    >>> from ansys.mapdl.core import launch_mapdl
    >>> mapdl = launch_mapdl()
    >>> mapdl._log.info('This is an useful message')
      LEVEL - INSTANCE NAME - MODULE - FUNCTION - MESSAGE
      INFO - GRPC_127.0.0.1:50052 -  test - <module> - This is an useful message

The ``instance_name`` field depends on the name of the MAPDL instance, which might not be set
yet when the log record is created (for example, during the initialization of the library).
If an MAPDL instance is not yet created, this field might be empty.

Because both types of loggers are based in the Python module ``logging``, you can use any of
the tools provided in this module to extend or modify these loggers.

For more information, see the module ``logging`` under ``ansys.mapdl.core``. 


Global Logger
~~~~~~~~~~~~~

There is a global logger called ``pymapdl_global`` that is initialized when PyMAPDL is imported.
This logger can be retrieved using:

.. code:: python

   from ansys.mapdl.core import LOG


This ``Logger`` is a custom class that wraps a ``logging.Logger`` object and gives extra
functionalities, such as a predefined file and stdout handlers and pointers.
You can access the underlying ``logging.Logger`` object using ``LOG.logger``.

To use this logger anywhere in the code, use:

.. code:: python

   from ansys.mapdl.core import LOG
   LOG.debug('This is an useful debug message')

The default logging level of ``LOG`` is ``ERROR``. To change this and output
lower-level messages, use:

.. code:: python

   LOG.logger.setLevel('DEBUG')
   LOG.file_handler.setLevel('DEBUG')  # If present. 
   LOG.stdout_handler.setLevel('DEBUG')  # If present.


Alternatively, you can use:

.. code:: python

   LOG.setLevel('DEBUG')


This alternative method ensures all handlers are set to the input log level. 

By default, the global logger does not log to a file. If you want it to do so, you can add
a file handler using:

.. code:: python

   import os
   file_path = os.path.join(os.getcwd(), 'pymapdl.log')
   LOG.log_to_file(file_path)


This sets the logger to be redirected to this file also. 
If you want to change the characteristics of the global logger from the beginning of the execution, 
you must edit the file ``__init__`` in the directory ``ansys.mapdl.core``. 


Instance Logger
~~~~~~~~~~~~~~~

There is also another type of logger provided within PyMAPDL that is specially designed for instances.
It tracks the MAPDL instance by pointing to its name (which should be unique) and logs to the file
``_MapdlCore._log``. You can access it using:

.. code:: python

   from ansys.mapdl.core import launch_mapdl
   mapdl = launch_mapdl()
   instance_logger = mapdl._log


This logger is completely independent from the global logger.
However, when it is initialized, it copies the handlers from the global logger to centralize the
logs in a terminal or file. You can access the underlying ``logging.Logger`` using:

.. code:: python

   logger = instance_logger.logger 

The way this logger works is very similar to the global logger. 
If you want to add a file handler, you use the method ``log_to_file`` or change the log level using
the method ``setLevel``.

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
