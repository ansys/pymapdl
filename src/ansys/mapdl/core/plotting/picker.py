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
from ansys.mapdl.core.plotting.consts import POINT_SIZE  # noqa: F401


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

        PICKING_USING_LEFT_CLICKING = False

        q = self.queries
        picked_entities = []
        picked_ids = []
        entity = entity.lower()

        if entity in ["kp", "node"]:
            selector = getattr(q, entity)
        else:
            # We need to come out with a different thing.
            pass

        # adding selection inversor
        pl.scene._inver_mouse_click_selection = False

        selection_text = {
            "S": "New selection",
            "A": "Adding to selection",
            "R": "Reselecting from the selection",
            "U": "Unselecting",
        }

        def gen_text(picked_entities=None):
            """Generate helpful text for the render window."""
            sel_ = (
                "Unselecting" if pl.scene._inver_mouse_click_selection else "Selecting"
            )
            type_text = selection_text[type_]
            button_ = "left" if PICKING_USING_LEFT_CLICKING else "right"
            text = (
                f"Please use the {button_} mouse button to pick the {entity}s.\n"
                f"Press the key 'u' to change between mouse selecting and unselecting.\n"
                f"Type: {type_} - {type_text}\n"
                f"Mouse selection: {sel_}\n"
            )

            picked_entities_str = ""
            if picked_entities:
                # reverse picked point order, exclude the brackets, and limit
                # to 40 characters
                picked_entities_str = str(picked_entities[::-1])[1:-1]
                if len(picked_entities_str) > 40:
                    picked_entities_str = picked_entities_str[:40]
                    idx = picked_entities_str.rfind(",") + 2
                    picked_entities_str = picked_entities_str[:idx] + "..."

            return text + f"Current {entity} selection: {picked_entities_str}"

        def callback_points(mesh, id_):
            from ansys.mapdl.core.plotting.consts import POINT_SIZE

            point = mesh.points[id_]
            node_id = selector(
                point[0], point[1], point[2]
            )  # This will only return one node. Fine for now.

            if not pl.scene._inver_mouse_click_selection:
                # Updating MAPDL entity mapping
                if node_id not in picked_entities:
                    picked_entities.append(node_id)
                # Updating pyvista entity mapping
                if id_ not in picked_ids:
                    picked_ids.append(id_)
            else:
                # Updating MAPDL entity mapping
                if node_id in picked_entities:
                    picked_entities.remove(node_id)
                # Updating pyvista entity mapping
                if id_ in picked_ids:
                    picked_ids.remove(id_)

            # remov etitle and update text
            pl.scene.remove_actor("title")
            pl.scene._picking_text = pl.scene.add_text(
                gen_text(picked_entities),
                font_size=GUI_FONT_SIZE,
                name="_entity_picking_message",
            )
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

        def callback_mesh(mesh):
            def get_entnum(mesh):
                return int(np.unique(mesh.cell_data["entity_num"])[0])

            mesh_id = get_entnum(mesh)

            # Getting meshes with that entity_num.
            meshes = pl.get_meshes_from_plotter()

            meshes = [each for each in meshes if get_entnum(each) == mesh_id]

            if not pl.scene._inver_mouse_click_selection:
                # Updating MAPDL entity mapping
                if mesh_id not in picked_entities:
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

            else:
                # Updating MAPDL entity mapping
                if mesh_id in picked_entities:
                    picked_entities.remove(mesh_id)

                    for i, each in enumerate(meshes):
                        pl.scene.remove_actor(f"_picked_entity_{mesh_id}_{i}")

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
            lines_pl = self.lplot(return_plotter=True, color="w")
            lines_meshes = lines_pl.get_meshes_from_plotter()

            for each_mesh in lines_meshes:
                pl.scene.add_mesh(
                    each_mesh,
                    pickable=False,
                    color="w",
                    # name="lines"
                )

            # Picking points
            pl.scene.enable_point_picking(
                callback=callback_points,
                use_mesh=True,
                show_message=gen_text(),
                show_point=True,
                left_clicking=PICKING_USING_LEFT_CLICKING,
                font_size=GUI_FONT_SIZE,
                tolerance=kwargs.get("tolerance", 0.025),
            )
        else:
            # Picking meshes
            pl.scene.enable_mesh_picking(
                callback=callback_mesh,
                use_mesh=True,
                show=False,  # This should be false to avoid a warning.
                show_message=gen_text(),
                left_clicking=PICKING_USING_LEFT_CLICKING,
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

        picked_entities = set(
            picked_entities
        )  # removing duplicates (although there should be none)

        if type_ == "S":
            pass
        elif type_ == "R":
            picked_entities = previous_picked_entities.intersection(picked_entities)
        elif type_ == "A":
            picked_entities = previous_picked_entities.union(picked_entities)
        elif type_ == "U":
            picked_entities = previous_picked_entities.difference(picked_entities)

        return list(picked_entities)
