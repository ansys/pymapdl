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

"""MAPDL selection-preserving context manager."""

import weakref

from ansys.mapdl.core._mapdl_core.selection import (
    _TMP_COMP,
    ENTITIES_TO_SELECTION_MAPPING,
)
from ansys.mapdl.core.misc import random_string


class _SaveSelectionContext:
    """Restore the MAPDL selection after a block exits."""

    def __init__(self, parent):
        self._parent = weakref.ref(parent)
        self.selection = []

    def __enter__(self):
        mapdl = self._parent()
        mapdl._log.debug("Entering saving selection context")
        selection = {"cmsel": mapdl.components._comp}
        identifier = random_string(5)
        for entity_type, component_name in _TMP_COMP.items():
            component_name = f"__{component_name}{identifier}__"
            selection[entity_type] = component_name
            mapdl.cm(component_name, entity_type, mute=True)

        self.selection.append(selection)

    def __exit__(self, *args):
        mapdl = self._parent()
        mapdl._log.debug("Exiting saving selection context")
        selection = self.selection.pop()
        components = selection.pop("cmsel")

        try:
            mapdl.allsel()
            mapdl.cmsel("None")

            if components:
                for component_name, component_type in components.items():
                    mapdl.cmsel("a", component_name, component_type, mute=True)

            for entity_type, component_name in selection.items():
                mapdl.cmsel("a", component_name, entity_type, mute=True)
                selection_function = getattr(
                    mapdl, ENTITIES_TO_SELECTION_MAPPING[entity_type.upper()]
                )
                selection_function("s", vmin=component_name, mute=True)
                mapdl.cmdele(component_name, mute=True)
        except Exception:
            if args and args[0] is not None:
                mapdl._log.exception("Unable to restore the saved selection.")
                return None
            raise
