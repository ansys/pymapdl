# Copyright (C) 2016 - 2026 ANSYS, Inc. and/or its affiliates.
# Copyright (C) 2016 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


"""The selection MAPDL core responsibility mixin."""

from functools import wraps

from ansys.mapdl.core.commands import (
    CMD_XSEL,
    XSEL_DOCSTRING_INJECTION,
    Commands,
    inject_docs,
)
from ansys.mapdl.core.plotting.picker import MapdlPicker

from . import _CoreMixinBase

# XSEL command -> (owner attribute, ID attribute) of the selected entities.
_XSEL_OUTPUT = {
    "NSEL": ("mesh", "nnum"),
    "ESEL": ("mesh", "enum"),
    "KSEL": ("geometry", "knum"),
    "LSEL": ("geometry", "lnum"),
    "ASEL": ("geometry", "anum"),
    "VSEL": ("geometry", "vnum"),
    "ESLN": ("mesh", "enum"),
    "NSLE": ("mesh", "nnum"),
}


def _is_interactive_xsel(args, kwargs) -> bool:
    """Return ``True`` when an XSEL command uses the interactive ``P`` item."""
    if len(args) >= 2 and isinstance(args[1], str) and args[1].upper() == "P":
        return True
    return "item" in kwargs and kwargs["item"].upper() == "P"


_TMP_COMP = {
    "KP": "cmp_kp",
    "LINE": "cmp_line",
    "AREA": "cmp_area",
    "VOLU": "cmp_volu",
    "NODE": "cmp_node",
    "ELEM": "cmp_elem",
}

ENTITIES_TO_SELECTION_MAPPING = {
    "KP": "ksel",
    "LINE": "lsel",
    "AREA": "asel",
    "VOLU": "vsel",
    "NODE": "nsel",
    "ELEM": "esel",
}


class _CoreSelectionMixin(_CoreMixinBase):
    """Static responsibility mixin for the MAPDL core facade."""

    @property
    def save_selection(self):
        """Save selection

        Save the current selection (nodes, elements, keypoints, lines, areas,
        volumes and components) before entering in the context manager, and
        when exit returns to that selection.
        """
        if self._save_selection_obj is None:
            from ansys.mapdl.core.contexts.save_selection import _SaveSelectionContext

            self._save_selection_obj = _SaveSelectionContext(self)
        return self._save_selection_obj

    def _wrap_xsel_commands(self):
        # Wrapping XSEL commands.
        if self.is_console:
            return

        for name in dir(self):
            if name[0:4].upper() in CMD_XSEL and name in dir(
                Commands
            ):  # avoid matching Mapdl properties which starts with same letters as MAPDL commands.
                method = self.__getattribute__(name)
                setattr(self, name, self._wrap_xsel_function(method))

    def _wrap_xsel_function(self, func):
        """Wrap an XSEL command so it returns the selected entity IDs."""
        if hasattr(func, "__func__"):
            func.__func__.__doc__ = inject_docs(
                func.__func__.__doc__, XSEL_DOCSTRING_INJECTION
            )
        else:  # pragma: no cover
            func.__doc__ = inject_docs(func.__doc__, XSEL_DOCSTRING_INJECTION)

        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            # in interactive mode (item='p'), the output is not suppressed
            if self._store_commands:
                # In non-interactive mode, execute the wrapped function and return its result.
                return func(*args, **kwargs)

            return_mapdl_output = kwargs.pop(
                "return_mapdl_output", self._xsel_mapdl_output
            )
            if _is_interactive_xsel(args, kwargs):
                return_mapdl_output = True

            output = func(*args, **kwargs)
            if not return_mapdl_output:
                output = self._xsel_selected_ids(func)
            return output

        return inner_wrapper

    def _xsel_selected_ids(self, method):
        """Return the IDs selected by an XSEL command."""
        if not self.geometry:
            # Cases where the geometry module is not loaded
            return None

        source, attribute = _XSEL_OUTPUT.get(
            method.__func__.__name__.upper(), (None, None)
        )
        if source is None:
            return None
        return getattr(getattr(self, source), attribute)

    def _get_selected_(self, entity):
        """Get list of selected entities."""
        allowed_values = ["NODE", "ELEM", "KP", "LINE", "AREA", "VOLU"]
        if entity.upper() not in allowed_values:
            raise ValueError(
                f"The value '{entity}' is not allowed.Only {allowed_values} are allowed"
            )

        entity = entity.upper()

        if entity == "NODE":
            return self.mesh.nnum.copy()
        elif entity == "ELEM":
            return self.mesh.enum.copy()
        elif entity == "KP":
            return self.geometry.knum
        elif entity == "LINE":
            return self.geometry.lnum
        elif entity == "AREA":
            return self.geometry.anum
        elif entity == "VOLU":
            return self.geometry.vnum

    def _enable_picking_entities(
        self, entity, pl, type_, previous_picked_entities, **kwargs
    ):
        """Resolve PyVista picks through the MAPDL picker."""
        return MapdlPicker(self).pick(
            entity, pl, type_, previous_picked_entities, **kwargs
        )

    def _perform_entity_list_selection(
        self, entity, selection_function, type_, item, comp, vmin, kabs
    ):
        """Select entities using CM, and the supplied selection function."""
        # Getting new selection
        for id_, each_ in enumerate(vmin):
            if type_ == "S" or not type_:
                type__ = "S" if id_ == 0 else "A"
            # R is an issue, because first iteration will clean up the rest.
            elif type_ == "R":
                raise NotImplementedError("Mode R is not supported.")
            else:
                type__ = type_

            selection_function(self, type__, item, comp, each_, "", "", kabs)
