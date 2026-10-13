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

"""Forced MAPDL output context manager."""

import weakref


class _ForceOutputContext:
    """Temporarily force MAPDL text output."""

    def __init__(self, parent):
        self._parent = weakref.ref(parent)

    def __enter__(self):
        parent = self._parent()
        parent._log.debug("Entering force-output mode")
        if parent.wrinqr(1) == 0:
            self._in_nopr = True
            parent._run("/gopr")
        else:
            self._in_nopr = False

        self._previous_mute, parent._mute = parent._mute, False

    def __exit__(self, *args):
        parent = self._parent()
        parent._log.debug("Exiting force-output mode")
        try:
            if self._in_nopr:
                parent._run("/nopr")
        finally:
            parent._mute = self._previous_mute
