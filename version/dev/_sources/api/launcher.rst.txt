.. _ref_launcher_api:

Launcher
========
Various PyMAPDL specific launcher commands.
Most of these commands are called from the
library `ansys-tools-common.path <ansys_tools_common_>`_.

.. currentmodule:: ansys.mapdl.core.launcher

.. autosummary::
   :toctree: _autosummary

   launch_mapdl
   launch_mapdl_process
   close_all_local_instances
   stop

.. note::

   :func:`stop() <ansys.mapdl.core.launcher.stop>` is also exposed at the top
   level of the package as :func:`stop_mapdl() <ansys.mapdl.core.stop_mapdl>`,
   for consistency with :func:`launch_mapdl()
   <ansys.mapdl.core.launcher.launch_mapdl>`.

.. currentmodule:: ansys.mapdl.core

.. autosummary::
   :toctree: _autosummary

   stop_mapdl


``ansys-tools-common.path`` functions
--------------------------------------

.. currentmodule:: ansys.tools.common.path

.. autosummary::
   :toctree: _autosummary

   change_default_ansys_path
   find_mapdl
   save_ansys_path
   get_available_ansys_installations
