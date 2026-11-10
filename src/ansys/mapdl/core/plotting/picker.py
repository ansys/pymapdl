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

"""PyVista-based MAPDL entity picking."""

import weakref

import numpy as np

from ansys.mapdl.core._mapdl_core.constants import GUI_FONT_SIZE
from ansys.mapdl.core.plotting.consts import POINT_SIZE

_SELECTION_TEXT = {
    "S": "New selection",
    "A": "Adding to selection",
    "R": "Reselecting from the selection",
    "U": "Unselecting",
}

_MAX_PICKED_TEXT_LENGTH = 40


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


class MapdlPicker:
    """Resolve PyVista point or cell picks to MAPDL entity numbers."""

    def __init__(self, mapdl):
        self._mapdl = weakref.ref(mapdl)

    def __getattr__(self, name):
        mapdl = self._mapdl()
        if mapdl is None:
            raise ReferenceError("The MAPDL parent no longer exists")
        return getattr(mapdl, name)

    def pick(self, entity, pl, type_, previous_picked_entities, **kwargs):
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
            self._show_picked_points(pl, mesh, picked_ids)

        def callback_mesh(mesh):
            mesh_id = self._entity_number(mesh)

            # Getting meshes with that entity_num.
            meshes = [
                each
                for each in pl.get_meshes_from_plotter()
                if self._entity_number(each) == mesh_id
            ]

            if not pl.scene._inver_mouse_click_selection:
                self._add_picked_mesh(pl, picked_entities, mesh_id, meshes)
            else:
                self._remove_picked_mesh(pl, picked_entities, mesh_id, meshes)

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
            pl.scene._inver_mouse_click_selection = (
                not pl.scene._inver_mouse_click_selection
            )
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

    @staticmethod
    def _entity_number(mesh) -> int:
        """Return the MAPDL entity number stored in a picked mesh."""
        return int(np.unique(mesh.cell_data["entity_num"])[0])

    @staticmethod
    def _show_picked_points(pl, mesh, picked_ids) -> None:
        """Highlight the picked points, or clear the highlight if there are none."""
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

    @staticmethod
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

    @staticmethod
    def _remove_picked_mesh(pl, picked_entities, mesh_id, meshes) -> None:
        """Forget a picked mesh entity and remove its highlight."""
        if mesh_id not in picked_entities:
            return
        picked_entities.remove(mesh_id)
        for i, _ in enumerate(meshes):
            pl.scene.remove_actor(f"_picked_entity_{mesh_id}_{i}")

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
