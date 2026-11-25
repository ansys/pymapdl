
.. _ref_materials_user_guide:

Read materials back
===================

The :attr:`Mapdl.materials <ansys.mapdl.core.Mapdl.materials>` attribute
returns every Material defined in the session as plain numbers. Use it to
check what MAPDL solves with, to compare two Materials, or to assert a model
setup in a test.

Each Material holds:

- Material Properties: one temperature table for each ``MP`` label, such as
  ``EX`` or ``PRXY``.
- Data Tables: one entry for each ``TB`` block, such as ``BISO`` or ``MISO``.
  Each entry holds the constants or points at each temperature.

Define a Material and read it back:

.. code:: pycon

   >>> from ansys.mapdl.core import launch_mapdl
   >>> mapdl = launch_mapdl()
   >>> mapdl.prep7()
   >>> mapdl.mptemp(1, 20, 100)
   >>> mapdl.mpdata("EX", 1, 1, 2.1e11, 2.0e11)
   >>> mapdl.mp("PRXY", 1, 0.3)
   >>> mapdl.tb("BISO", 1, 2)
   >>> mapdl.tbtemp(20)
   >>> mapdl.tbdata(1, 250e6, 2e9)
   >>> mapdl.tbtemp(200)
   >>> mapdl.tbdata(1, 200e6, 1.5e9)
   >>> mapdl.mp("EX", 4, 70e9)
   >>> materials = mapdl.materials
   >>> materials
   MaterialsSnapshot(ids=[1, 4])

The result is a read-only mapping keyed by material ID. It supports ``in``,
``len()``, and iteration, and raises ``KeyError`` for an undefined ID:

.. code:: pycon

   >>> list(materials), 1 in materials, len(materials)
   ([1, 4], True, 2)
   >>> materials[99]
   KeyError: 99


Material Properties
-------------------

The ``properties`` attribute of a
:class:`Material <ansys.mapdl.core._materials.Material>` maps each ``MP``
label to a :class:`PropertyTable <ansys.mapdl.core._materials.PropertyTable>`
with ``temperatures`` and ``values`` arrays. A constant set with the
:meth:`Mapdl.mp() <ansys.mapdl.core.Mapdl.mp>` method is a one-point table at
temperature ``0.0``:

.. code:: pycon

   >>> ex = materials[1].properties["EX"]
   >>> ex.temperatures, ex.values
   (array([ 20., 100.]), array([2.1e+11, 2.0e+11]))
   >>> prxy = materials[1].properties["PRXY"]
   >>> prxy.temperatures, prxy.values
   (array([0.]), array([0.3]))


Data Tables
-----------

The ``tables`` attribute lists each
:class:`DataTable <ansys.mapdl.core._materials.DataTable>` in the order MAPDL
writes them. A Data Table keeps its label and ``TBOPT`` value exactly as MAPDL
writes them, and fills either ``constants`` or ``points`` with one array for
each temperature:

.. code:: pycon

   >>> biso = materials[1].tables[0]
   >>> biso.label, biso.temperatures
   ('BISO', array([ 20., 200.]))
   >>> biso.constants
   [array([2.5e+08, 2.0e+09]), array([2.0e+08, 1.5e+09])]

Data Tables defined with ``TBPT``, such as ``MISO``, return ``(n, 2)`` arrays
in ``points``. Data Tables written in the newer format, such as
``TB,PLAS,,,,MISO``, also expose their raw ``TBIN`` settings in ``options``
and any ``TBFIELD`` values other than temperature in ``fields``.


Compare Materials in pandas
---------------------------

The :meth:`to_dataframe() <ansys.mapdl.core._materials.MaterialsSnapshot.to_dataframe>`
method returns the Material Properties of every Material as a long-format
pandas DataFrame, with one row for each temperature point. Data Tables are not
included because their shapes vary. This method requires pandas.

.. code:: pycon

   >>> df = materials.to_dataframe()
   >>> df
      material label  temperature         value
   0         1    EX         20.0  2.100000e+11
   1         1    EX        100.0  2.000000e+11
   2         1  PRXY          0.0  3.000000e-01
   3         4    EX          0.0  7.000000e+10


Snapshots and limits
--------------------

- Each access to :attr:`Mapdl.materials <ansys.mapdl.core.Mapdl.materials>`
  reads MAPDL once with ``CDWRITE,MAT``. The returned objects never change, so
  read the attribute again to see later changes.
- The read works from any processor, keeps the active processor, prints
  nothing, and leaves no file in the MAPDL working directory.
- The read is not available inside
  :func:`Mapdl.non_interactive <ansys.mapdl.core.Mapdl.non_interactive>`.
- The attribute is read only. To define Materials, use the existing methods,
  such as :meth:`Mapdl.mp() <ansys.mapdl.core.Mapdl.mp>` and
  :meth:`Mapdl.tb() <ansys.mapdl.core.Mapdl.tb>`.


Raw values, not Material Models
-------------------------------

PyMAPDL returns the raw values that MAPDL holds. It does not interpret them.
For PyMAPDL, a ``BISO`` Data Table is a label with two constants. It does not
name them as a yield stress and a tangent modulus. To work with interpreted Material Models, such as isotropic
hardening with a named yield stress, use
`Ansys Materials Manager <materials_manager_docs_>`_.

For the classes returned by this attribute, see :ref:`ref_materials_api`.
