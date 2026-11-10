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

"""Path objects associated with a MAPDL instance."""

import os
import pathlib
from typing import Any, Optional
import weakref


class _MapdlPathMixin:
    """Add MAPDL-side file queries to a pure path."""

    __slots__ = ()
    _mapdl_ref: weakref.ReferenceType[Any]
    _mapdl_root: pathlib.PurePath

    def __new__(
        cls,
        *pathsegments: os.PathLike[str] | str,
        mapdl: Any,
        mapdl_root: Optional[pathlib.PurePath] = None,
    ):
        self = super().__new__(cls, *pathsegments)
        object.__setattr__(self, "_mapdl_ref", weakref.ref(mapdl))
        if mapdl_root is None:
            pure_path_class = (
                pathlib.PureWindowsPath
                if issubclass(cls, pathlib.PureWindowsPath)
                else pathlib.PurePosixPath
            )
            mapdl_root = pure_path_class(*pathsegments)
        object.__setattr__(self, "_mapdl_root", mapdl_root)
        return self

    def __init__(
        self,
        *pathsegments: os.PathLike[str] | str,
        mapdl: Any,
        mapdl_root: Optional[pathlib.PurePath] = None,
    ) -> None:
        if pathlib.PurePath.__init__ is not object.__init__:
            super().__init__(*pathsegments)

    def _as_pure_path(self) -> pathlib.PurePath:
        if isinstance(self, pathlib.PureWindowsPath):
            return pathlib.PureWindowsPath(str(self))
        return pathlib.PurePosixPath(str(self))

    def _mapdl(self) -> Any:
        mapdl = self._mapdl_ref()
        if mapdl is None:
            raise ReferenceError(
                "The MAPDL instance associated with this path no longer exists."
            )
        return mapdl

    def _derived_path(self, path: pathlib.PurePath):
        if isinstance(path, _MapdlPathMixin) and hasattr(path, "_mapdl_ref"):
            return path
        return type(self)(path, mapdl=self._mapdl(), mapdl_root=self._mapdl_root)

    def with_segments(self, *pathsegments: os.PathLike[str] | str):
        """Construct a derived path while retaining the MAPDL instance."""
        return type(self)(
            *pathsegments, mapdl=self._mapdl(), mapdl_root=self._mapdl_root
        )

    def joinpath(self, *pathsegments: os.PathLike[str] | str):
        """Join path segments while retaining the MAPDL instance."""
        return self._derived_path(self._as_pure_path().joinpath(*pathsegments))

    def __truediv__(self, key: os.PathLike[str] | str):
        try:
            return self.joinpath(key)
        except TypeError:
            return NotImplemented

    @property
    def parent(self):
        """Return the logical parent with the same MAPDL instance."""
        return self._derived_path(self._as_pure_path().parent)

    def with_name(self, name: str):
        """Return a renamed path with the same MAPDL instance."""
        return self._derived_path(self._as_pure_path().with_name(name))

    def with_stem(self, stem: str):
        """Return a path with a new stem and the same MAPDL instance."""
        return self._derived_path(self._as_pure_path().with_stem(stem))

    def with_suffix(self, suffix: str):
        """Return a path with a new suffix and the same MAPDL instance."""
        return self._derived_path(self._as_pure_path().with_suffix(suffix))

    def is_file(self) -> bool:
        """Return whether this path is a file in the MAPDL working directory."""
        if self._as_pure_path().parent != self._mapdl_root:
            raise ValueError(
                "is_file() only supports direct children of the MAPDL "
                "working directory."
            )

        mapdl = self._mapdl()
        if mapdl.is_local:
            return os.path.isfile(str(self))

        filename = self._as_pure_path().name
        files = mapdl.list_files()
        if isinstance(self, pathlib.PureWindowsPath):
            filename = filename.casefold()
            files = [entry.casefold() for entry in files]
        return filename in files


class _MapdlPurePosixPath(_MapdlPathMixin, pathlib.PurePosixPath):
    """Pure POSIX path associated with a MAPDL instance."""

    __slots__ = ("_mapdl_ref", "_mapdl_root")


class _MapdlPureWindowsPath(_MapdlPathMixin, pathlib.PureWindowsPath):
    """Pure Windows path associated with a MAPDL instance."""

    __slots__ = ("_mapdl_ref", "_mapdl_root")
