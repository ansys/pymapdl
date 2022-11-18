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

They are based on Python files and must be run under 3 minutes.

They are in the ``examples`` directory inside this repository.

Example: `2d_plate_with_a_hole.py <https://github.com/pyansys/pymapdl/blob/main/examples/00-mapdl-examples/2d_plate_with_a_hole.py>`_

It is published on the following link: 
`MAPDL 2D Plane Stress Concentration Analysis <https://mapdl.docs.pyansys.com/examples/gallery_examples/00-mapdl-examples/2d_plate_with_a_hole.html#sphx-glr-examples-gallery-examples-00-mapdl-examples-2d-plate-with-a-hole-py>`_

They will be executed and the mention **Total running time of the script** will appear at the end of
the document.


Static examples
---------------

They are based on RST files and will not be executed. 

They are in the ``doc\source`` directory.

Example: `krylov_example.rst <https://raw.githubusercontent.com/pyansys/pymapdl/main/doc/source/examples/extended_examples/Krylov/krylov_example.rst>`_

It is published on the following link: `Harmonic analysis using the frequency-sweep Krylov method <https://mapdl.docs.pyansys.com/examples/extended_examples/Krylov/krylov_example.html>`_


Semi-dynamic examples
---------------------

They are RST files which execute Python code using this RST directive:

.. code:: bash

    .. jupyter-execute::
    :hide-code:


Example: `tecfricstir.rst <https://raw.githubusercontent.com/pyansys/pymapdl/main/doc/source/examples/technology_showcase_examples/techdemo-28/ex_28-tecfricstir.rst>`_

It is visible at the following link: `Friction Stir Welding (FSW) Simulation <https://mapdl.docs.pyansys.com/examples/technology_showcase_examples/techdemo-28/ex_28-tecfricstir.html>`_


Recommendations
---------------

As the dynamic examples are examples that have to be run at each Documentation build, make sure to
make them very short. To get around the problem of execution time, feel free to use the static or the
semi-static examples.