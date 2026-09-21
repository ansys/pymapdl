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


"""The selection commands MAPDL extended mixin."""

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


class _ExtendedSelectionCommandsMixin(_ExtendedMixinBase):
    """Static responsibility mixin for the extended MAPDL facade."""

    @wraps(_MapdlCore.set)
    def set(
        self,
        lstep="",
        sbstep="",
        fact="",
        kimg="",
        time="",
        angle="",
        nset="",
        order="",
        **kwargs,
    ):
        """Wraps SET to return a Command listing

        Returns
        -------
        CommandListingOutput or str
            Command listing output when LIST is specified, otherwise MAPDL command output.
        """
        output = super().set(
            lstep, sbstep, fact, kimg, time, angle, nset, order, **kwargs
        )

        if (
            isinstance(lstep, str)
            and lstep.upper() == "LIST"
            and not sbstep
            and not fact
        ):
            return CommandListingOutput(
                output,
                magicwords=["SET", "TIME/FREQ"],
                columns_names=[
                    "SET",
                    "TIME/FREQ",
                    "LOAD STEP",
                    "SUBSTEP",
                    "CUMULATIVE",
                ],
            )
        else:
            return output

    @wraps(_MapdlCore.vsel)
    def vsel(self, *args, **kwargs) -> str:
        """Wraps superclassed VSEL to allow to use a list/tuple/array for vmin.

        It will raise an error in case vmax or vinc are used too.

        Returns
        -------
        str
            Command output from MAPDL.
        """
        sel_func = getattr(
            super(), "vsel"
        )  # using super() inside the wrapped function confuses the references

        @allow_pickable_entities(entity="volu", plot_function="vplot")
        @allow_iterables_vmin(entity="volume")
        def wrapped(self, *args, **kwargs):
            return sel_func(*args, **kwargs)

        return wrapped(self, *args, **kwargs)

    @wraps(_MapdlCore.nsel)
    def nsel(self, *args, **kwargs) -> str:
        """Wraps previons NSEL to allow to use a list/tuple/array for vmin.

        It will raise an error in case vmax or vinc are used too.

        Returns
        -------
        str
            Command output from MAPDL.
        """
        sel_func = getattr(
            super(), "nsel"
        )  # using super() inside the wrapped function confuses the references

        @allow_pickable_entities()
        @allow_iterables_vmin(entity="node")
        def wrapped(self, *args, **kwargs):
            return sel_func(*args, **kwargs)

        return wrapped(self, *args, **kwargs)

    @wraps(_MapdlCore.esel)
    def esel(self, *args, **kwargs) -> str:
        """Wraps previons ESEL to allow to use a list/tuple/array for vmin.

        It will raise an error in case vmax or vinc are used too.

        Returns
        -------
        str
            Command output from MAPDL.
        """
        sel_func = getattr(
            super(), "esel"
        )  # using super() inside the wrapped function confuses the references

        @allow_pickable_entities(entity="elem", plot_function="eplot")
        @allow_iterables_vmin(entity="elem")
        def wrapped(self, *args, **kwargs):
            return sel_func(*args, **kwargs)

        return wrapped(self, *args, **kwargs)

    @wraps(_MapdlCore.ksel)
    def ksel(self, *args, **kwargs) -> str:
        """Wraps superclassed KSEL to allow to use a list/tuple/array for vmin.

        It will raise an error in case vmax or vinc are used too.

        Returns
        -------
        str
            Command output from MAPDL.
        """
        sel_func = getattr(
            super(), "ksel"
        )  # using super() inside the wrapped function confuses the references

        @allow_pickable_entities(entity="kp", plot_function="kplot")
        @allow_iterables_vmin(entity="kp")
        def wrapped(self, *args, **kwargs):
            return sel_func(*args, **kwargs)

        return wrapped(self, *args, **kwargs)

    @wraps(_MapdlCore.lsel)
    def lsel(self, *args, **kwargs) -> str:
        """Wraps superclassed LSEL to allow to use a list/tuple/array for vmin.

        It will raise an error in case vmax or vinc are used too.

        Returns
        -------
        str
            Command output from MAPDL.
        """
        sel_func = getattr(
            super(), "lsel"
        )  # using super() inside the wrapped function confuses the references

        @allow_pickable_entities(entity="line", plot_function="lplot")
        @allow_iterables_vmin(entity="line")
        def wrapped(self, *args, **kwargs):
            return sel_func(*args, **kwargs)

        return wrapped(self, *args, **kwargs)

    @wraps(_MapdlCore.asel)
    def asel(self, *args, **kwargs) -> str:
        """Wraps superclassed ASEL to allow to use a list/tuple/array for vmin.

        It will raise an error in case vmax or vinc are used too.

        Returns
        -------
        str
            Command output from MAPDL.
        """
        sel_func = getattr(
            super(), "asel"
        )  # using super() inside the wrapped function confuses the references

        @allow_pickable_entities(entity="area", plot_function="aplot")
        @allow_iterables_vmin(entity="area")
        def wrapped(self, *args, **kwargs):
            return sel_func(*args, **kwargs)

        return wrapped(self, *args, **kwargs)

    @wraps(_MapdlCore.clear)
    def clear(self, read: str = "NOSTART", **kwargs):
        """Wraps the MAPDL ``CLEAR`` command to use `NOSTART` with mute=True"""
        if self.is_grpc:
            self._create_session()
        kwargs.setdefault("mute", True)
        getattr(super(), "clear")(read=read, **kwargs)

    @wraps(_MapdlCore.cmlist)
    def cmlist(self, *args, **kwargs):
        from ansys.mapdl.core.commands import ComponentListing

        return ComponentListing(super().cmlist(*args, **kwargs))
