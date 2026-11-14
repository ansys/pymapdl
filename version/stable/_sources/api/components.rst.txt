.. _ref_componentmanager_api:

Components
==========

.. currentmodule:: ansys.mapdl.core

.. autosummary::
   :toctree: _autosummary

   component.ComponentManager

The :class:`~ansys.mapdl.core.component.Component` class represents a single
named component and subclasses the built-in ``tuple`` type to store the
selected entity IDs. Because it inherits directly from ``tuple``, it also
exposes the standard ``tuple`` API (such as ``count()`` and ``index()``),
which is documented in the Python standard library and isn't duplicated here.
The ``type`` and ``items`` properties are specific to this class and are
documented on this page instead of being generated as separate pages.

.. autoclass:: ansys.mapdl.core.component.Component
   :members: type, items
   :show-inheritance:
