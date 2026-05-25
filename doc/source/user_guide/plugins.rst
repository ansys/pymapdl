.. _ref_plugin_user_guide:

Plugin manager overview
=======================

MAPDL plugins extend the solver with additional commands at runtime. The
:class:`ansPlugin <ansys.mapdl.core.plugin.ansPlugin>` class, accessed via
``mapdl.plugins``, lets you load, inspect, and unload plugins from a
running MAPDL session without leaving Python.

.. warning::
   Plugin support requires MAPDL 25.2 or later.

.. note::
   To create your own plugins, visit MAPDL documentation or contact ANSYS support.

Accessing the plugin manager
-----------------------------

The plugin manager is available as a property on every
:class:`Mapdl <ansys.mapdl.core.mapdl.MapdlBase>` instance:

.. code:: pycon

   >>> from ansys.mapdl.core import launch_mapdl
   >>> mapdl = launch_mapdl()
   >>> plugins = mapdl.plugins
   >>> plugins
   MAPDL Plugins
   ----------------
     (no plugins loaded)

Loading a plugin
----------------

Use :meth:`load() <ansys.mapdl.core.plugin.ansPlugin.load>` with the plugin
name and an optional feature string:

.. code:: pycon

   >>> mapdl.plugins.load("my_plugin", feature="advanced")

After loading, each command that the plugin registers is injected as an
attribute on the ``mapdl`` object. Characters that are not valid Python
identifiers are transformed: ``*`` becomes ``star`` and ``/`` becomes
``slash``.

Listing loaded plugins
----------------------

:meth:`list() <ansys.mapdl.core.plugin.ansPlugin.list>` returns the names of
all currently loaded plugins:

.. code:: pycon

   >>> mapdl.plugins.list()
   ['my_plugin']

.. note::
   Plugin tracking is session-scoped. :meth:`list()
   <ansys.mapdl.core.plugin.ansPlugin.list>` first tries ``*PLUG,LIST`` on
   the MAPDL server. When the server returns no output, for example, after
   reconnecting to an already-running MAPDL instance, it falls back to the
   internal state that was built up during the current Python session.

Inspecting plugin commands
--------------------------

:meth:`commands() <ansys.mapdl.core.plugin.ansPlugin.commands>` returns the
attribute names that a plugin registered on the ``mapdl`` object:

.. code:: pycon

   >>> mapdl.plugins.commands("my_plugin")
   ['my_command', 'another_command']

Printing a summary
------------------

Printing ``mapdl.plugins`` (or calling :func:`str() <str>` on it) shows a
table with each loaded plugin, its feature string, and how many commands it
registered:

.. code:: pycon

   >>> print(mapdl.plugins)
   MAPDL Plugins
   ----------------
   my_plugin                    : advanced  [2 commands]

Unloading a plugin
------------------

Use :meth:`unload() <ansys.mapdl.core.plugin.ansPlugin.unload>` to remove a
plugin and clean up all the commands it added:

.. code:: pycon

   >>> mapdl.plugins.unload("my_plugin")
   >>> mapdl.plugins.list()
   []

For the full API reference, see :ref:`ref_plugin_api`.
