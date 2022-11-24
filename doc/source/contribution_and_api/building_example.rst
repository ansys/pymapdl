.. _ref_building_example:


===================
Building an example
===================

.. currentmodule:: ansys.mapdl.core.building_example

To run the documentation, you need to have the correct versions of each tool. To do so, execute the
following instruction.

.. code:: bash

    pip install -r requirements/requirements_docs.txt


The Sphinx configuration is in the file ``conf.py`` in ``doc/source``.

To run the sphinx tool:

.. code:: bash

    doc\make.bat html



There are three types of examples: dynamic, static, and semi-static.


Dynamic examples
----------------

The dynamic examples are based on Python files and must be able to run in under three minutes.

They are in the ``examples`` directory in this repository.

.. vale off

Example: `2d_plate_with_a_hole.py <https://github.com/pyansys/pymapdl/blob/main/examples/00-mapdl-examples/2d_plate_with_a_hole.py>`_
.. vale on

Here is a link to this dynamic example: 
`MAPDL 2D Plane Stress Concentration Analysis <https://mapdl.docs.pyansys.com/examples/gallery_examples/00-mapdl-examples/2d_plate_with_a_hole.html#sphx-glr-examples-gallery-examples-00-mapdl-examples-2d-plate-with-a-hole-py>`_

When an example is executed, **Total running time of the script** appears at the end of
the document.


Static examples
---------------

Static examples are based on RST files and are not executed. 

They are in the ``doc\source`` directory.

.. vale off

Example: `krylov_example.rst <https://raw.githubusercontent.com/pyansys/pymapdl/main/doc/source/examples/extended_examples/Krylov/krylov_example.rst>`_
.. vale on

Here is a link to this static example: `Harmonic analysis using the frequency-sweep Krylov method <https://mapdl.docs.pyansys.com/examples/extended_examples/Krylov/krylov_example.html>`_


Semi-dynamic examples
---------------------

Semi-dynamic examples are RST files that execute Python code using this RST directive:

.. code:: bash

    .. jupyter-execute::
    :hide-code:


.. vale off

Example: `tecfricstir.rst <https://raw.githubusercontent.com/pyansys/pymapdl/main/doc/source/examples/technology_showcase_examples/techdemo-28/ex_28-tecfricstir.rst>`_
.. vale on

Here is a link to this semi-dynamic example: `Friction Stir Welding (FSW) Simulation <https://mapdl.docs.pyansys.com/examples/technology_showcase_examples/techdemo-28/ex_28-tecfricstir.html>`_


Recommendations
---------------

As dynamic examples must run each time documentation is built, make sure that they are very short.
To get around the problem of execution time, feel free to use static or semi-static examples.