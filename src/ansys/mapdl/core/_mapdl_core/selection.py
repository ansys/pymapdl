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

import numpy as np

from ansys.mapdl.core.commands import (
    CMD_XSEL,
    XSEL_DOCSTRING_INJECTION,
    Commands,
    inject_docs,
)

from . import _CoreMixinBase
from .constants import GUI_FONT_SIZE

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

_SELECTION_TEXT = {
    "S": "New selection",
    "A": "Adding to selection",
    "R": "Reselecting from the selection",
    "U": "Unselecting",
}

_MAX_PICKED_TEXT_LENGTH = 40


def _is_interactive_xsel(args, kwargs) -> bool:
    """Return ``True`` when an XSEL command uses the interactive ``P`` item."""
    if len(args) >= 2 and isinstance(args[1], str) and args[1].upper() == "P":
        return True
    return "item" in kwargs and kwargs["item"].upper() == "P"


def _format_picked_entities(picked_entities) -> str:
    """Return the most recent picks as a short, comma-separated string."""
    if not picked_entities:
        return ""

    # Reverse picked order, exclude the brackets, and limit the length.
    text = str(picked_entities[::-1])[1:-1]
    if len(text) > _MAX_PICKED_TEXT_LENGTH:
        text = text[:_MAX_PICKED_TEXT_LENGTH]
        idx = text.rfind(",") + 2
        text = text[:idx] + "..."
    return text


def _update_membership(items: list, item, add: bool) -> None:
    """Add ``item`` to ``items`` if missing, or remove it if present."""
    if add and item not in items:
        items.append(item)
    elif not add and item in items:
        items.remove(item)


def _combine_selection(type_: str, previous: set, picked: set) -> set:
    """Combine the new picks with the previous selection according to ``type_``."""
    if type_ == "R":
        return previous.intersection(picked)
    if type_ == "A":
        return previous.union(picked)
    if type_ == "U":
        return previous.difference(picked)
    return picked


def _entity_number(mesh) -> int:
    """Return the MAPDL entity number stored in a picked mesh."""
    return int(np.unique(mesh.cell_data["entity_num"])[0])


def _show_picked_points(pl, mesh, picked_ids) -> None:
    """Highlight the picked points, or clear the highlight if there are none."""
    from ansys.mapdl.core.plotting.consts import POINT_SIZE

    if picked_ids:
        pl.scene.add_mesh(
            mesh.points[picked_ids],
            color="red",
            point_size=POINT_SIZE + 10,
            name="_picked_entities",
            pickable=False,
            reset_camera=False,
        )
    else:
        pl.scene.remove_actor("_picked_entities")


def _add_picked_mesh(pl, picked_entities, mesh_id, meshes) -> None:
    """Record a picked mesh entity and highlight its meshes."""
    if mesh_id in picked_entities:
        return
    picked_entities.append(mesh_id)
    for i, each in enumerate(meshes):
        pl.scene.add_mesh(
            each,
            color="red",
            point_size=10,
            name=f"_picked_entity_{mesh_id}_{i}",
            pickable=False,
            reset_camera=False,
        )


def _remove_picked_mesh(pl, picked_entities, mesh_id, meshes) -> None:
    """Forget a picked mesh entity and remove its highlight."""
    if mesh_id not in picked_entities:
        return
    picked_entities.remove(mesh_id)
    for i, _ in enumerate(meshes):
        pl.scene.remove_actor(f"_picked_entity_{mesh_id}_{i}")


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
            self._save_selection_obj = self._save_selection(self)
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
        """Show a plot and get the selected entity."""
        _debug = kwargs.pop("_debug", False)  # for testing purposes
        previous_picked_entities = set(previous_picked_entities)

        picking_using_left_clicking = False

        picked_entities: list = []
        picked_ids: list = []
        entity = entity.lower()

        # adding selection inversor
        pl.scene._inver_mouse_click_selection = False

        def gen_text(picked_entities=None):
            """Generate helpful text for the render window."""
            return self._picking_text(
                pl, entity, type_, picked_entities, picking_using_left_clicking
            )

        def callback_points(mesh, id_):
            point = mesh.points[id_]
            # This only returns one node. Fine for now.
            node_id = getattr(self.queries, entity)(point[0], point[1], point[2])

            adding = not pl.scene._inver_mouse_click_selection
            _update_membership(picked_entities, node_id, adding)
            _update_membership(picked_ids, id_, adding)

            # remove title and update text
            pl.scene.remove_actor("title")
            pl.scene._picking_text = pl.scene.add_text(
                gen_text(picked_entities),
                font_size=GUI_FONT_SIZE,
                name="_entity_picking_message",
            )
            _show_picked_points(pl, mesh, picked_ids)

        def callback_mesh(mesh):
            mesh_id = _entity_number(mesh)

            # Getting meshes with that entity_num.
            meshes = [
                each
                for each in pl.get_meshes_from_plotter()
                if _entity_number(each) == mesh_id
            ]

            if not pl.scene._inver_mouse_click_selection:
                _add_picked_mesh(pl, picked_entities, mesh_id, meshes)
            else:
                _remove_picked_mesh(pl, picked_entities, mesh_id, meshes)

            # Removing only-first time actors
            pl.scene.remove_actor("title")
            pl.scene.remove_actor("_point_picking_message")

            if "_entity_picking_message" in pl.actors:
                pl.scene.remove_actor("_entity_picking_message")

            pl._picking_text = pl.add_text(
                gen_text(picked_entities),
                font_size=GUI_FONT_SIZE,
                name="_entity_picking_message",
            )

        if entity in ["kp", "node"]:
            self._enable_point_picking(
                pl, callback_points, gen_text(), picking_using_left_clicking, kwargs
            )
        else:
            # Picking meshes
            pl.scene.enable_mesh_picking(
                callback=callback_mesh,
                use_mesh=True,
                show=False,  # This should be false to avoid a warning.
                show_message=gen_text(),
                left_clicking=picking_using_left_clicking,
                font_size=GUI_FONT_SIZE,
            )

        def callback_u():
            # inverting bool
            pl.scene._inver_mouse_click_selection = not pl._inver_mouse_click_selection
            pl.scene.remove_actor("_entity_picking_message")

            pl.scene._picking_text = pl.add_text(
                gen_text(picked_entities),
                font_size=GUI_FONT_SIZE,
                name="_entity_picking_message",
            )

        pl.scene.add_key_event("u", callback_u)

        if not _debug:  # pragma: no cover
            pl.scene.show()
        else:
            _debug(pl)

        # removing duplicates (although there should be none)
        return list(
            _combine_selection(type_, previous_picked_entities, set(picked_entities))
        )

    @staticmethod
    def _picking_text(pl, entity, type_, picked_entities, left_clicking):
        """Return the instructions displayed in the render window."""
        sel_ = "Unselecting" if pl.scene._inver_mouse_click_selection else "Selecting"
        button_ = "left" if left_clicking else "right"
        text = (
            f"Please use the {button_} mouse button to pick the {entity}s.\n"
            f"Press the key 'u' to change between mouse selecting and unselecting.\n"
            f"Type: {type_} - {_SELECTION_TEXT[type_]}\n"
            f"Mouse selection: {sel_}\n"
        )
        return (
            text
            + f"Current {entity} selection: {_format_picked_entities(picked_entities)}"
        )

    def _enable_point_picking(
        self, pl, callback, message, left_clicking, kwargs
    ) -> None:
        """Draw the lines as context and enable point picking."""
        lines_pl = self.lplot(return_plotter=True, color="w")
        for each_mesh in lines_pl.get_meshes_from_plotter():
            pl.scene.add_mesh(each_mesh, pickable=False, color="w")

        pl.scene.enable_point_picking(
            callback=callback,
            use_mesh=True,
            show_message=message,
            show_point=True,
            left_clicking=left_clicking,
            font_size=GUI_FONT_SIZE,
            tolerance=kwargs.get("tolerance", 0.025),
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
