# Copyright (C) 2016 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#
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

"""Database setup command extensions."""

from functools import wraps

from ansys.mapdl.core.mapdl_core import _MapdlCore

from .. import _ExtendedMixinBase


class _ExtendedDatabaseSetupMixin(_ExtendedMixinBase):
    """Extended database setup commands."""

    @wraps(_MapdlCore.clear)
    def clear(self, read: str = "NOSTART", **kwargs):
        """Wraps the MAPDL ``CLEAR`` command to use `NOSTART` with mute=True"""
        if self.is_grpc:
            self._create_session()
        kwargs.setdefault("mute", True)
        getattr(super(), "clear")(read=read, **kwargs)
