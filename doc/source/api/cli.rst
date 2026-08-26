.. _ref_cli_api:

Command line interface
=======================

Every ``pymapdl`` sub-command is a thin `Click <click_docs_>`_ wrapper
(``<name>_cli``) around a plain function (``<name>``) that lives in the same
module, for example :func:`ansys.mapdl.core.cli.start.start`. Import the plain
function to get the behavior of a command from Python, without going through a
shell.

The plain functions return data and raise exceptions, they never print or
exit the interpreter. For an introduction with examples, see
:ref:`ref_cli_programmatic`.

.. note::

   :func:`stop() <ansys.mapdl.core.launcher.connection.stop>` is the one
   exception: it lives in :mod:`ansys.mapdl.core.launcher.connection` instead
   of :mod:`ansys.mapdl.core.cli.stop`, because it is also used internally by
   :func:`close_all_local_instances()
   <ansys.mapdl.core.launcher.connection.close_all_local_instances>`. It is
   still re-exported as ``ansys.mapdl.core.cli.stop.stop`` and
   ``ansys.mapdl.core.launcher.stop`` for convenience, and the ``pymapdl
   stop`` command wraps it the same way as every other sub-command.

Manage instances
-----------------

.. autosummary::
   :toctree: _autosummary

   ansys.mapdl.core.cli.start.start
   ansys.mapdl.core.launcher.connection.stop
   ansys.mapdl.core.cli.list_instances.list_instances
   ansys.mapdl.core.cli.check.check
   ansys.mapdl.core.cli.exec.exec_commands


Convert and document APDL code
--------------------------------

.. autosummary::
   :toctree: _autosummary

   ansys.mapdl.core.cli.convert.convert
   ansys.mapdl.core.cli.help.help_command


Manage the bundled skills
---------------------------

.. autosummary::
   :toctree: _autosummary

   ansys.mapdl.core.cli.skills.list_skills
   ansys.mapdl.core.cli.skills.show_skill
   ansys.mapdl.core.cli.skills.plan_skill_install
   ansys.mapdl.core.cli.skills.apply_skill_install
   ansys.mapdl.core.cli.skills.install_skill


Helpers
--------

.. autosummary::
   :toctree: _autosummary

   ansys.mapdl.core.cli.check.format_info
   ansys.mapdl.core.cli.exec.resolve_command_block
   ansys.mapdl.core.cli.convert.resolve_graphics_backend
   ansys.mapdl.core.cli.helpers.connect_to_instance
   ansys.mapdl.core.cli.helpers.get_mapdl_instances
   ansys.mapdl.core.cli.helpers.silence_logging
