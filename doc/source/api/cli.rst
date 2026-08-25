.. _ref_cli_api:

Command line interface
=======================

Every ``pymapdl`` sub-command is a thin `Click <click_docs_>`_ wrapper
(``<name>_cli``) around a plain function (``<name>``) that lives in the same
module, for example :func:`ansys.mapdl.core.cli.stop.stop`. Import the plain
function to get the behavior of a command from Python, without going through a
shell.

The plain functions return data and raise exceptions, they never print or
exit the interpreter. For an introduction with examples, see
:ref:`ref_cli_programmatic`.

Manage instances
-----------------

.. autosummary::
   :toctree: _autosummary

   ansys.mapdl.core.cli.start.start
   ansys.mapdl.core.cli.stop.stop
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
