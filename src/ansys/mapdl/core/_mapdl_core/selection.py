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

# Subprocess is needed to start the backend. But
# the input is controlled by the library. Excluding bandit check.
from typing import TYPE_CHECKING

import numpy as np

from ansys.mapdl.core import _HAS_DPF
from ansys.mapdl.core.commands import (
    CMD_XSEL,
    XSEL_DOCSTRING_INJECTION,
    Commands,
    inject_docs,
)

if TYPE_CHECKING:  # pragma: no cover
    if _HAS_DPF:
        pass


from . import _CoreMixinBase
from .constants import GUI_FONT_SIZE


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

        def wrap_xsel_function(func):
            if hasattr(func, "__func__"):
                func.__func__.__doc__ = inject_docs(
                    func.__func__.__doc__, XSEL_DOCSTRING_INJECTION
                )
            else:  # pragma: no cover
                func.__doc__ = inject_docs(func.__doc__, XSEL_DOCSTRING_INJECTION)

            def wrap_xsel_function_output(method):
                # Injecting doc string modification
                name = method.__func__.__name__.upper()
                if not self.geometry:
                    # Cases where the geometry module is not loaded
                    return None

                if name == "NSEL":
                    return self.mesh.nnum
                elif name == "ESEL":
                    return self.mesh.enum
                elif name == "KSEL":
                    return self.geometry.knum
                elif name == "LSEL":
                    return self.geometry.lnum
                elif name == "ASEL":
                    return self.geometry.anum
                elif name == "VSEL":
                    return self.geometry.vnum
                elif name == "ESLN":
                    return self.mesh.enum
                elif name == "NSLE":
                    return self.mesh.nnum
                else:
                    return None

            @wraps(func)
            def inner_wrapper(*args, **kwargs):
                # in interactive mode (item='p'), the output is not suppressed
                if self._store_commands:
                    # In non-interactive mode, execute the wrapped function and return its result.
                    return func(*args, **kwargs)

                is_interactive_arg = (
                    True
                    if len(args) >= 2
                    and isinstance(args[1], str)
                    and args[1].upper() == "P"
                    else False
                )
                is_interactive_kwarg = (
                    True
                    if "item" in kwargs and kwargs["item"].upper() == "P"
                    else False
                )

                return_mapdl_output = kwargs.pop(
                    "return_mapdl_output", self._xsel_mapdl_output
                )
                if is_interactive_arg or is_interactive_kwarg:
                    return_mapdl_output = True

                output = func(*args, **kwargs)
                if not return_mapdl_output:
                    output = wrap_xsel_function_output(func)
                return output

            return inner_wrapper

        for name in dir(self):
            if name[0:4].upper() in CMD_XSEL and name in dir(
                Commands
            ):  # avoid matching Mapdl properties which starts with same letters as MAPDL commands.
                method = self.__getattribute__(name)
                setattr(self, name, wrap_xsel_function(method))

    def _get_selected_(self, entity):
        """Get list of selected entities."""
        allowed_values = ["NODE", "ELEM", "KP", "LINE", "AREA", "VOLU"]
        if entity.upper() not in allowed_values:
            raise ValueError(
                f"The value '{entity}' is not allowed."
                f"Only {allowed_values} are allowed"
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
