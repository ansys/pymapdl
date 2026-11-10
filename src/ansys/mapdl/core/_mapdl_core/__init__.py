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


"""Private mapdl core mixins."""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from typing import Protocol, TextIO

    from ansys.mapdl.reader import Archive

    from ansys.mapdl.core.mapdl_geometry import Geometry, LegacyGeometry
    from ansys.mapdl.core.plugin import ansPlugin
    from ansys.mapdl.core.post import PostProcessing

    class _CoreMixinBase(Protocol):
        """Type-only base for cooperative MAPDL core mixins."""

        _apdl_log: TextIO | None
        _archive_cache: Archive | None
        _geometry: Geometry | LegacyGeometry | None
        _plugin: ansPlugin | None
        _post_object: PostProcessing | None
        _remove_tmp: bool
        _version: float | None

        def __getattr__(self, name: str) -> Any: ...

else:
    _CoreMixinBase = object
