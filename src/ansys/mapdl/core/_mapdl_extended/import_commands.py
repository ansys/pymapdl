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


"""The import commands MAPDL extended mixin."""

from functools import wraps  # noqa: F401
import os  # noqa: F401
import pathlib  # noqa: F401
import re  # noqa: F401
import shutil  # noqa: F401
import tempfile  # noqa: F401
from typing import Union  # noqa: F401
import warnings  # noqa: F401
import weakref  # noqa: F401

import numpy as np  # noqa: F401
from numpy.typing import DTypeLike, NDArray  # noqa: F401

from ansys.mapdl.core import LOG as logger  # noqa: F401
from ansys.mapdl.core import parse  # noqa: F401
from ansys.mapdl.core.commands import CommandListingOutput, CommandOutput  # noqa: F401
from ansys.mapdl.core.errors import (  # noqa: F401
    CommandDeprecated,
    ComponentDoesNotExits,
    IncorrectWorkingDirectory,
    MapdlCommandIgnoredError,
    MapdlDoLoopLimitError,
    MapdlRuntimeError,
)
from ansys.mapdl.core.mapdl_core import _MapdlCore  # noqa: F401
from ansys.mapdl.core.mapdl_types import KwargDict, MapdlFloat  # noqa: F401
from ansys.mapdl.core.misc import (  # noqa: F401
    allow_iterables_vmin,
    allow_pickable_entities,
    check_deprecated_vtk_kwargs,
    random_string,
    requires_graphics,
    supress_logging,
)
from ansys.mapdl.core.plotting import GraphicsBackend  # noqa: F401

from . import _ExtendedMixinBase


class _ExtendedImportCommandsMixin(_ExtendedMixinBase):
    """Static responsibility mixin for the extended MAPDL facade."""

    @wraps(_MapdlCore.catiain)
    def catiain(self, name="", extension="", path="", blank="", **kwargs):
        """Wrap the ``catiain`` method to take advantage of the gRPC methods.

        Returns
        -------
        str
            Command output from MAPDL.
        """
        if self.platform == "windows":
            raise OSError(
                "The command 'catiain' is not supported on Windows. Use the 'mapdl.cat5in' method instead to import Catia v5 files."
            )
        return super().catiain(
            name=name, extension=extension, path=path, blank=blank, **kwargs
        )

    @wraps(_MapdlCore.cat5in)
    def cat5in(
        self,
        name="",
        extension="",
        path="",
        entity="",
        fmt="",
        nocl="",
        noan="",
        **kwargs,
    ):
        """Wrap the ``cat5in`` method to take advantage of the gRPC methods."""
        if self.platform == "linux":
            raise OSError(
                "The command 'cat5in' is not supported on Linux. Use the 'mapdl.catiain' method instead to import Catia v4 files."
            )

        fname = name
        if path:
            fname = os.path.join(path, name)
        fname = self._get_file_name(fname, extension, "CATPart")
        fname = self._get_file_path(fname, False)
        name, extension, path = self._decompose_fname(fname)

        path = "" if path == path.parent else str(path)

        # wrapping path in single quotes because of #2286
        path = f"'{path}'"
        self.finish()
        return super().cat5in(
            name=name,
            extension=extension,
            path=path,
            entity=entity,
            fmt=fmt,
            nocl=nocl,
            noan=noan,
            **kwargs,
        )

    @wraps(_MapdlCore.igesin)
    def igesin(self, fname, ext="", **kwargs):
        """Wrap the IGESIN command to handle the remote case."""

        fname = self._get_file_name(fname=fname, ext=ext)
        filename = self._get_file_path(fname, progress_bar=False)

        # Entering aux15 preprocessor
        self.aux15()

        if " " not in fname:
            return super().igesin(fname=filename, **kwargs)

        # Bug in reading file paths with whitespaces.
        # https://github.com/ansys/pymapdl/issues/1601

        msg_ = f"Applying \\IGESIN whitespace patch.\nSee #1601 issue in PyMAPDL repository.\nReading file {fname}"
        self.input_strings("\n".join([f"! {each}" for each in msg_.splitlines()]))
        self._log.debug(msg_)

        cmd = f"*dim,__iges_file__,string,248\n*set,__iges_file__(1), '{filename}'"
        self.input_strings(cmd)

        out = super().igesin(fname="__iges_file__(1)", **kwargs)
        self.run("__iges_file__ =")  # cleaning array.
        self.run("! Ending \\IGESIN whitespace patch.")
        return out

    @wraps(_MapdlCore.satin)
    def satin(
        self,
        name,
        extension="",
        path="",
        entity="",
        fmt="",
        nocl="",
        noan="",
        **kwargs,
    ):
        """Wraps ~SATIN command"""
        fname = name
        if path:
            fname = os.path.join(path, name)
        fname = self._get_file_name(fname, extension, "sat")
        fname = self._get_file_path(fname, False)
        name, extension, path = self._decompose_fname(fname)

        path = "" if path == path.parent else str(path)

        # wrapping path in single quotes because of #2286
        path = f"'{path}'"
        return super().satin(
            name=name,
            extension=extension,
            path=path,
            entity=entity,
            fmt=fmt,
            nocl=nocl,
            noan=noan,
            **kwargs,
        )

    @wraps(_MapdlCore.parain)
    def parain(
        self,
        name,
        extension="",
        path="",
        entity="",
        fmt="",
        scale="",
        **kwargs,
    ):
        """Wraps ~parain command"""
        fname = name
        if path:
            fname = os.path.join(path, name)
        fname = self._get_file_name(fname, extension, "x_t")
        fname = self._get_file_path(fname, False)
        name, extension, path = self._decompose_fname(fname)

        path = "" if path == path.parent else str(path)

        # wrapping path in single quotes because of #2286
        path = f"'{path}'"
        return super().parain(
            name=name,
            extension=extension,
            path=path,
            entity=entity,
            fmt=fmt,
            scale=scale,
            **kwargs,
        )
