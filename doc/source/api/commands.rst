.. _ref_commands_api:

Commands output
===============

Various PyMAPDL classes and commands which helps in data post-processing.

All these classes are subclasses of :py:class:`str` class, hence they inherit all the
methods and attributes of :class:`string`.

.. currentmodule:: ansys.mapdl.core

.. We should add the line ':toctree: _autosummary' to the following classes autosummary 
   to remove the warning during building, however, it shows only the methods links in the
   sidebar (toctree), not the classes, and since both classes have the same method name, it
   is confusing.


.. autosummary::
   :toctree: _autosummary

   commands.CommandListingOutput
   commands.BoundaryConditionsListingOutput
