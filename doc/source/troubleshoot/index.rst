.. _ref_troubleshooting:

===============
Troubleshooting
===============

To help overcome any problem that you might have when using PyMAPDL,
some of the most common problems and frequently asked questions are posted here.


.. toctree::
   :maxdepth: 3

   troubleshoot
   faq


Debug in PyMAPDL
----------------

If you are having trouble with PyMAPDL, you can examine the content
of the output file to help to identify any issue. 

You can set the logger output file to be ``mylog.log`` by
running the following commands in a Python terminal or at the beginning of your
script:

.. code:: python

    from ansys.mapdl.core import LOG
    LOG.setLevel("DEBUG")
    LOG.log_to_file("mylog.log")

    from ansys.mapdl.core import launch_mapdl

    mapdl = launch_mapdl(loglevel="DEBUG")

You can attach this file to a bug report in the PyMAPDL GitHub repository for further investigation.
If you are not able to identify the issue, you can open a discussion on the
`PyMAPDL Discussions page <pymapdl_discussions_>`_.
If you believe you have found a bug, open an issue on the
`PyMAPDL Issues page <pymapdl_issues_>`_.

   

More help needed?
-----------------

  *"What do you do if a problem is not listed here?"*  

You can go to `PyMAPDL Repository Discussion <pymapdl_discussions_>`_ and ask about it.

If you think you found a bug or would like to make a feature request, you can do so by
opening an issue in `PyMAPDL Repository Issues <pymapdl_issues_>`_.