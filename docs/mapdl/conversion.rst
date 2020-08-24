Translating Scripts
-------------------
The ``pyansys`` module contains a few basic functions to translate
existing MAPDL scripts into ``pyansys`` scripts.  Ideally, all math
and variable setting would take place within Python as much as
possible as APDL math is much less transparent and more difficult to
debug.  These examples only show an automatic translation of a
verification file and not optimized code.  Should it be necessary to
pull parameters or arrays from ansys, use the ``get_value`` command,
which is quite similar to the MAPDL ``GET`` command:

.. code:: python

   >>> mapdl.get_value('NODE' , 2, 'U' ,'Y')
   4.532094298033

Alternatively, if a parameter is already defined, you can access it
using ``mapdl.parameters`` with:

.. code:: python

    >>> mapdl.parameters
    ARR                              : ARRAY DIM (3, 1, 1)
    PARM_FLOAT                       : 20.0
    PARM_INT                         : 10.0
    PARM_LONG_STR                    : "stringstringstringstringstringst"
    PARM_STR                         : "string"
    DEF_Y                            : 4.532094298033

    >>> mapdl.parameters['DEF_Y']
    4.532094298033

Existing ANSYS scripts can be translated using:

.. code:: python

    import pyansys
    inputfile = 'ansys_inputfile.inp'
    pyscript = 'pyscript.py'
    pyansys.convert_script(inputfile, pyscript)

Of particular note in the following examples is how most of the
commands can be called as a method to the ansys object rather than
sending a string as a command.  Additionally, take note that some
commands require the ``with mapdl.non_interactive:`` directive since
some commands require and will break the CORBA server connection.
Also note that APDL macros that use ``*CREATE`` have been replaced
with a python function.  This will make the code easier to debug
should it be necessary to insert a break point in the code.


Convert Script Description
--------------------------
.. autofunction:: pyansys.convert.convert_script
