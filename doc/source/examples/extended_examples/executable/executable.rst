.. _executable_example:


========================================
Create your own command line application
========================================

This example shows how to create your own command line interface
python application which uses PyMAPDL to perform some simulations.

Let's start from a given script which calculates the
first natural frequency of a rotor with a given number of
blades and material specification.

.. literalinclude:: rotor.py
   :language: python
   :emphasize-lines: 12-19,117
   :linenos:

   The input and the output values are highlighted.

This application uses a command line interface to provide the options to PyMAPDL.
To specify the options, the package `Click <https://click.palletsprojects.com>`_
is used. Other suitable package is the builtin package
`argparse <https://docs.python.org/3/library/argparse.html>`_.


