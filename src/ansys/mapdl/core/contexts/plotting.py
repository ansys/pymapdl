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

"""MAPDL plotting-device context manager."""

import sys
from typing import Literal
import weakref

VALID_FILE_TYPE_FOR_PLOT_LITERAL = Literal["PNG", "TIFF", "VRML", "TERM"]
from ansys.mapdl.core.errors import MapdlRuntimeError
from ansys.mapdl.core.misc import requires_graphics


class _InteractivePlottingContext:
    """Redirect plots to MAPDL plots."""

    def __init__(self, parent, pixel_res: int) -> None:
        self._parent = weakref.ref(parent)
        self._pixel_res = pixel_res

    @requires_graphics
    def __enter__(self) -> None:
        parent = self._parent()
        if parent is None:
            raise MapdlRuntimeError("Parent reference is None")

        parent._log.debug("Entering in 'WithInterativePlotting' mode")
        self._active = not parent._store_commands
        if not self._active:
            return

        self.previous_device = parent.file_type_for_plots
        entered = False
        try:
            if not parent._png_mode:
                parent.show("PNG", mute=True)
                parent.gfile(self._pixel_res, mute=True)

            if parent.file_type_for_plots not in ["PNG", "TIFF", "PNG", "VRML"]:
                parent.show(parent.default_file_type_for_plots)
            entered = True
        finally:
            if not entered:
                _restore_plot_device(
                    parent,
                    self.previous_device,
                    primary_exception=sys.exc_info()[1],
                    use_property=True,
                )

    @requires_graphics
    def __exit__(self, *args) -> None:
        parent = self._parent()
        if parent is None:
            raise MapdlRuntimeError("Parent reference is None")

        parent._log.debug("Exiting in 'WithInterativePlotting' mode")
        if not self._active:
            return

        try:
            parent.show("close", mute=True)
            if not parent._store_commands and not parent._png_mode:
                parent.show("PNG", mute=True)
                parent.gfile(self._pixel_res, mute=True)
        finally:
            _restore_plot_device(
                parent,
                self.previous_device,
                primary_exception=sys.exc_info()[1],
                use_property=True,
            )


def _restore_plot_device(
    mapdl,
    previous_device: VALID_FILE_TYPE_FOR_PLOT_LITERAL,
    primary_exception: BaseException | None,
    *,
    use_property: bool = False,
) -> None:
    try:
        if use_property:
            mapdl.file_type_for_plots = previous_device
        else:
            mapdl.show(previous_device)
    except Exception:
        if primary_exception is None:
            raise
        mapdl._log.exception("Unable to restore the previous plotting device.")
