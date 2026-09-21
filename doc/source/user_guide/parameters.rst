
.. _ref_parameters:

Setting and retrieving parameters
=================================

MAPDL parameters can be retrieved from an instance of
:class:`Mapdl <ansys.mapdl.core.mapdl.MapdlBase>`
using the :attr:`Mapdl.parameters <ansys.mapdl.core.Mapdl.parameters>`.
For example, if you want to use MAPDL's
:func:`Mapdl.get() <ansys.mapdl.core.Mapdl.get>` method to
populate a parameter, you can then access the parameter with code:

.. code:: pycon

   >>> from ansys.mapdl.core import launch_mapdl
   >>> mapdl = launch_mapdl()
   >>> mapdl.get("DEF_Y", "NODE", 2, "U", "Y")
   >>> mapdl.parameters["DEF_Y"]
   1.0

Alternatively, you could use the
:meth:`Mapdl.parameters.get_value() <ansys.mapdl.core.Mapdl.parameters.get_value>`
method.
This method is a wrapper around the MAPDL
:meth:`Mapdl.get() <ansys.mapdl.core.Mapdl.get>` method
and allows you to retrieve the value of a parameter without
having to store the parameter in an intermediate MAPDL variable.
For example, if you want to retrieve the value of a parameter directly,
you can use:

.. code:: pycon

   >>> mapdl.get_value("NODE", 2, "U", "Y")
   1.0

You can also follow a similar approach to get array parameters from the
MAPDL `*VGET` command.
For example, if you want to store the value of the displacement of all nodes
in the Y direction, you can use the following code:

.. code:: pycon

   >>> mapdl.vget("MY_UY", "NODE", "U", "Y")
   >>> mapdl.parameters["MY_UY"]
   array([1.0, 2.0, 3.0, ...])

Or, if you want to retrieve the value of the array directly, without storing
it in an intermediate MAPDL parameter, you can use the
:func:`Mapdl.get_array() <ansys.mapdl.core.Mapdl.get_array>` method:

.. code:: pycon

   >>> mapdl.get_array("NODE", item1="U", it1num="Y")
   array([1.0, 2.0, 3.0, ...])

You can also use :func:`Mapdl.get_array() <ansys.mapdl.core.Mapdl.get_array>`
to list entities, such as the currently selected node numbers:

.. code:: pycon

   >>> mapdl.get_array("NODE", item1="NLIST")
   array([1., 2., 3., ...])

You can also set both scalar and array parameters from Python objects
using :attr:`Mapdl.parameters <ansys.mapdl.core.Mapdl.parameters>`
with:

.. code:: pycon

   >>> mapdl.parameters["MY_ARRAY"] = np.arange(10000)
   >>> mapdl.parameters["MY_ARRAY"]
   array([0.00000e+00, 1.00000e+00, 2.00000e+00, ..., 9.99997e+05,
          9.99998e+05, 9.99999e+05])

   >>> mapdl.parameters["MY_STRING"] = "helloworld"
   >>> mapdl.parameters["MY_STRING"]
   "helloworld"

You can also access some built-in parameters normally accessed through
the :func:`Mapdl.get() <ansys.mapdl.core.Mapdl.get>` method. For example,
instead of getting the current routine with ``\*GET, ACTIVE, 0,
ROUT``, you can access it with this code:

.. code:: pycon

  >>> mapdl.parameters.routine
  'Begin level'

.. _ref_parameters_retrieval_helpers:

Retrieving POST26 variables and element-table results
-----------------------------------------------------

In addition to :func:`Mapdl.get_array()
<ansys.mapdl.core.Mapdl.get_array>`, PyMAPDL provides two more helpers
for retrieving common categories of MAPDL results directly as
``numpy.ndarray`` objects: :func:`Mapdl.get_variable()
<ansys.mapdl.core.Mapdl.get_variable>` for POST26 time-history variables,
and :func:`Mapdl.get_etable() <ansys.mapdl.core.Mapdl.get_etable>` for
POST1 element-table results.

Use :func:`Mapdl.get_variable() <ansys.mapdl.core.Mapdl.get_variable>` to
retrieve the values of a POST26 variable defined with commands such as
:func:`Mapdl.nsol() <ansys.mapdl.core.Mapdl.nsol>` or
:func:`Mapdl.esol() <ansys.mapdl.core.Mapdl.esol>`. This is equivalent to
the MAPDL `VGET <https://ansyshelp.ansys.com/Views/Secured/corp/v252/en/ans_cmd/Hlp_C_VGET.html>`_
command:

.. code:: pycon

   >>> mapdl.post26()
   >>> mapdl.nsol(2, 1, "U", "X")
   >>> mapdl.get_variable(2)
   array([0.        , 0.00108135, 0.00300901, ..., 0.03407310])

Use :func:`Mapdl.get_etable() <ansys.mapdl.core.Mapdl.get_etable>` to
retrieve an element-table column as an array without having to manage
the underlying `ETABLE
<https://ansyshelp.ansys.com/Views/Secured/corp/v252/en/ans_cmd/Hlp_C_ETABLE.html>`_
label yourself. This method fills the table with
:func:`Mapdl.etable() <ansys.mapdl.core.Mapdl.etable>` and then retrieves
it with :func:`Mapdl.get_array() <ansys.mapdl.core.Mapdl.get_array>`:

.. code:: pycon

   >>> mapdl.post1()
   >>> mapdl.set(1, 1)
   >>> mapdl.get_etable("S", "X")
   array([-1.12618148, -0.93902147, -0.88121128, ...,  0.        ])

By default, :func:`Mapdl.get_etable() <ansys.mapdl.core.Mapdl.get_etable>`
uses a unique hidden label for the element-table column and erases it
after the values are retrieved. If you pass the ``lab`` argument, the
column is kept in the element table under that name so that you can
reuse it in subsequent MAPDL operations, such as ``SADD`` or ``SMULT``:

.. code:: pycon

   >>> mapdl.get_etable("S", "X", lab="SX_TABLE")
   array([-1.12618148, -0.93902147, -0.88121128, ...,  0.        ])
   >>> mapdl.get_array("ELEM", 1, "ETAB", "SX_TABLE")
   array([-1.12618148, -0.93902147, -0.88121128, ...,  0.        ])

.. note::
   Like other data-retrieval helpers, :func:`Mapdl.get_array()
   <ansys.mapdl.core.Mapdl.get_array>`, :func:`Mapdl.get_variable()
   <ansys.mapdl.core.Mapdl.get_variable>`, and :func:`Mapdl.get_etable()
   <ansys.mapdl.core.Mapdl.get_etable>` must be called only after the
   commands that generate the data they retrieve have already run.
   In particular, none of them can be used from inside a
   :func:`Mapdl.non_interactive() <ansys.mapdl.core.Mapdl.non_interactive>`
   context, since commands issued there are not sent to MAPDL until the
   context exits. See :ref:`Running in non-interactive mode
   <ref_non_interactive>` for more details.

For a full list of the methods and attributes available to the
``Parameters`` class, see :ref:`ref_parameters_api`.

For additional information on PyMAPDL array limitations, see
:ref:`Issues when importing and exporting numpy arrays in MAPDL <ref_issues_np_mapdl>`.

.. _ref_special_named_param:

Specially named parameters
--------------------------

Parameters with leading underscores
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Parameters starting with an underscore (``'_'``) are reserved parameters
for MAPDL macros and routines. Their use is discouraged, and in PyMAPDL
you cannot set them directly.

If you need to set one of these parameters, you can use the
:attr:`Mapdl._run <ansys.mapdl.core.Mapdl._run>`
attribute to avoid PyMAPDL parameter name checks:


.. code:: pycon

   >>> mapdl._run("_parameter=123")
   'PARAMETER _PARAMETER =     123.00000000'

By default, this type of parameter cannot be seen when issuing the
:attr:`Mapdl.parameters <ansys.mapdl.core.Mapdl.parameters>` attribute.
However, you can change this by setting the
:attr:`Mapdl.parameters.show_leading_underscore_parameters
<ansys.mapdl.core.Mapdl.parameters.show_leading_underscore_parameters>`
to ``True``:

.. code:: pycon

   >>> mapdl.parameters.show_leading_underscore_parameters = True
   >>> mapdl.parameters
   MAPDL Parameters
   ----------------
   PORT                             : 50053.0
   _RETURN                          : 0.0
   _STATUS                          : 0.0
   _UIQR                            : 17.0


Parameters with trailing underscores
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Parameters ending with an underscore are recommended for user routines
and macros. You can set this type of parameter in PyMAPDL, but by default,
they cannot be seen in the
:attr:`Mapdl.parameters <ansys.mapdl.core.Mapdl.parameters>` attribute unless
the :attr:`Mapdl.parameters.show_trailing_underscore_parameters
<ansys.mapdl.core.Mapdl.parameters.show_trailing_underscore_parameters>` attribute
is set to ``True``:


.. code:: pycon

   >>> mapdl.parameters["param_"] = 1.0
   >>> mapdl.parameters
   MAPDL Parameters
   ----------------
   >>> mapdl.parameters.show_trailing_underscore_parameters = True
   >>> mapdl.parameters
   MAPDL Parameters
   ----------------
   PARAM_                           : 1.0


Parameters with leading and trailing underscores
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Parameters with both leading and trailing underscores are a special type. These parameters
**CANNOT** be seen in the :attr:`Mapdl.parameters <ansys.mapdl.core.Mapdl.parameters>` attribute
under any circumstances. Their use is not recommended.

You can still retrieve these special parameters using any of the normal methods
for retrieving parameters. However, you must know the parameter name:


.. code:: pycon

   >>> mapdl.parameters["_param_"] = 1.0
   >>> mapdl.parameters
   MAPDL Parameters
   ----------------
   >>> print(mapdl.parameters["_param_"])
   1.0
