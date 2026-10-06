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

"""MAPDL routine context manager."""

import weakref

from ansys.mapdl.core.misc import check_valid_routine


class _RunAsRoutineContext:
    """Restore MAPDL's routine after a block exits."""

    def __init__(self, parent, routine):
        self._parent = weakref.ref(parent)
        self._requested_routine = routine

    def __enter__(self):
        parent = self._parent()
        parent._cache_routine()
        parent._log.debug(f"Caching routine {self._cached_routine}")

        if (
            self._requested_routine.lower().strip()
            != self._cached_routine.lower().strip()
        ):
            parent._enter_routine(self._requested_routine)

    def __exit__(self, *args):
        parent = self._parent()
        parent._log.debug(f"Restoring routine '{self._cached_routine}'")
        parent._resume_routine()

    @property
    def _cached_routine(self):
        return self._parent()._cached_routine


def _enter_routine(mapdl, routine):
    check_valid_routine(routine)

    if routine.lower() in ["begin level", "finish"]:
        mapdl.finish(mute=True)
    else:
        if not routine.startswith("/"):
            routine = f"/{routine}"
        mapdl.run(routine, mute=True)


def _cache_routine(mapdl):
    """Cache the current routine."""
    mapdl._cached_routine = mapdl.parameters.routine


def _resume_routine(mapdl):
    """Resume the cached routine."""
    if mapdl._cached_routine is not None:
        mapdl._enter_routine(mapdl._cached_routine)
        mapdl._cached_routine = None
