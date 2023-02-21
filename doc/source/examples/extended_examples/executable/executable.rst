.. _executable_example:


===============================================
Create your own Python command line application
===============================================

This example shows how to create your own command line interface (CLI)
python application which uses PyMAPDL to perform some simulations.
This usage is quite convenient when aiming to automate workflows.
One could build different PyMAPDL applications which can be called
from the CLI with different arguments.


Simulation configuration
========================

Let's start from a given script called :download:`Original rotor.py script <rotor.py>` which calculates the
first natural frequency of a rotor with a given number of
blades and material specification.

.. literalinclude:: rotor.py


Converting a script to a Python application
===========================================

The above script needs to be converted to a Python application in order
to be used from the terminal.
In this case, this application uses a CLI to provide the options to PyMAPDL.
To specify the options, the package `Click <https://click.palletsprojects.com>`_
is used. Another suitable package is the builtin package
`argparse <https://docs.python.org/3/library/argparse.html>`_.


Firstly, we need to convert the whole script into a function.
This can be easily accomplished by using the input arguments
in a function signature. 
In our case, we want to specify the following arguments:

* ``n_blades``: Number of blades.
* ``blade_length``: Length of each blade.
* ``elastic_modulus``: Elastic modulus of the material.
* ``density``: Density of the material.

The function is then defined as:

.. literalinclude:: cli_rotor.py
   :linenos:
   :lines: 5,6, 20-31

The value of these parameters are introduced by adding the following code
at the top of the script:


.. literalinclude:: cli_rotor.py
   :linenos:
   :lines: 1,2,9-20

In addition you need to add the call to the newly created function as the following way:


.. literalinclude:: cli_rotor.py
   :linenos:
   :lines: 144-

This ensure the new function is called when we are executing the python script.

Now you can call your function from the command line using:

.. code:: bash

   $ python rotor.py 4
   Initializing script with values:
   Number of blades: 4
   Blade length: 0.2 m
   Elastic modulus: 200.0 GPa
   Density: 7850 Kg/m3
   Solving...
   The first natural frequency is 1146.2 Hz.

Here ``4`` is the number of blades.
You can also input other arguments such as:

.. code:: bash

   $ python cli_rotor.py 4 --density 7000
   Initializing script with values:
   Number of blades: 4
   Blade length: 0.2 m
   Elastic modulus: 200.0 GPa
   Density: 7000 Kg/m3
   Solving...
   The first natural frequency is 1213.8 Hz.



Additional files
================

You can download the following files:

* :download:`Original rotor.py script <rotor.py>`
* :download:`Application cli_rotor.py <cli_rotor.py>`