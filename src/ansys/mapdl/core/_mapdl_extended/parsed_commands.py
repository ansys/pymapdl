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


"""The parsed commands MAPDL extended mixin."""

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


class _ExtendedParsedCommandsMixin(_ExtendedMixinBase):
    """Static responsibility mixin for the extended MAPDL facade."""

    @wraps(_MapdlCore.osresult)
    def osresult(self, item="", comp="", freq="", cname="", **kwargs) -> CommandOutput:
        result = getattr(super(), "osresult")(item, comp, freq, cname, **kwargs)
        if item.upper().strip() == "STATUS":
            from ansys.mapdl.core.misc import expand_all_inner_lists

            columns_names = ["ITEM", "FREQUENCY", "COMPONENT"]
            result = CommandListingOutput(result)
            table_match = re.search(
                r"ITEM\s+FREQUENCY\s+COMPONENT(.*)", result, flags=re.DOTALL
            )
            if table_match:
                table = table_match.group(1)
                table = [each.split() for each in table.splitlines() if each.strip()]
                table = expand_all_inner_lists(
                    table, target_length=len(columns_names), fill_value=""
                )

                result._columns_names = columns_names
                result._cache = np.array(table)
        return result

    @wraps(_MapdlCore.aflist)
    def aflist(self, **kwargs):
        # Running in non-interactive to avoid the `aflist.tmp` command being locked
        # because of `/INPUT` issue on MAPDL side. See #4390 for more details.
        with self.non_interactive:
            return super().aflist(**kwargs)

    @wraps(_MapdlCore.a)
    def a(self, *args, **kwargs):
        return parse.parse_a(super().a(*args, **kwargs))

    @wraps(_MapdlCore.al)
    def al(self, *args, **kwargs):
        return parse.parse_a(super().al(*args, **kwargs))

    @wraps(_MapdlCore.aadd)
    def aadd(self, *args, **kwargs):
        return parse.parse_output_areas(super().aadd(*args, **kwargs))

    @wraps(_MapdlCore.asba)
    def asba(self, *args, **kwargs):
        return parse.parse_output_volume_area(super().asba(*args, **kwargs))

    @wraps(_MapdlCore.et)
    def et(self, *args, **kwargs):
        return parse.parse_et(super().et(*args, **kwargs))

    @wraps(_MapdlCore.e)
    def e(self, *args, **kwargs):
        return parse.parse_e(super().e(*args, **kwargs))

    @wraps(_MapdlCore.k)
    def k(self, *args, **kwargs):
        return parse.parse_k(super().k(*args, **kwargs))

    @wraps(_MapdlCore.kbetw)
    def kbetw(self, *args, **kwargs):
        return parse.parse_kpoint(super().kbetw(*args, **kwargs))

    @wraps(_MapdlCore.kcenter)
    def kcenter(self, *args, **kwargs):
        return parse.parse_kpoint(super().kcenter(*args, **kwargs))

    @wraps(_MapdlCore.kdist)
    def kdist(self, *args, **kwargs):
        return parse.parse_kdist(super().kdist(*args, **kwargs))

    @wraps(_MapdlCore.kl)
    def kl(self, *args, **kwargs):
        return parse.parse_kl(super().kl(*args, **kwargs))

    @wraps(_MapdlCore.knode)
    def knode(self, *args, **kwargs):
        return parse.parse_knode(super().knode(*args, **kwargs))

    @wraps(_MapdlCore.bsplin)
    def bsplin(self, *args, **kwargs):
        return parse.parse_line_no(super().bsplin(*args, **kwargs))

    @wraps(_MapdlCore.circle)
    def circle(self, *args, **kwargs):
        return parse.parse_line_nos(super().circle(*args, **kwargs))

    @wraps(_MapdlCore.l)
    def l(self, *args, **kwargs):
        return parse.parse_line_no(super().l(*args, **kwargs))

    @wraps(_MapdlCore.l2ang)
    def l2ang(self, *args, **kwargs):
        return parse.parse_line_no(super().l2ang(*args, **kwargs))

    @wraps(_MapdlCore.l2tan)
    def l2tan(self, *args, **kwargs):
        return parse.parse_line_no(super().l2tan(*args, **kwargs))

    @wraps(_MapdlCore.lang)
    def lang(self, *args, **kwargs):
        return parse.parse_line_no(super().lang(*args, **kwargs))

    @wraps(_MapdlCore.larc)
    def larc(self, *args, **kwargs):
        return parse.parse_line_no(super().larc(*args, **kwargs))

    @wraps(_MapdlCore.larea)
    def larea(self, *args, **kwargs):
        return parse.parse_line_no(super().larea(*args, **kwargs))

    @wraps(_MapdlCore.lcomb)
    def lcomb(self, *args, **kwargs):
        return parse.parse_line_no(super().lcomb(*args, **kwargs))

    @wraps(_MapdlCore.lextnd)
    def lextnd(self, *args, **kwargs):
        return parse.parse_line_no(super().lextnd(*args, **kwargs))

    @wraps(_MapdlCore.lfillt)
    def lfillt(self, *args, **kwargs):
        return parse.parse_line_no(super().lfillt(*args, **kwargs))

    @wraps(_MapdlCore.lstr)
    def lstr(self, *args, **kwargs):
        return parse.parse_line_no(super().lstr(*args, **kwargs))

    @wraps(_MapdlCore.ltan)
    def ltan(self, *args, **kwargs):
        return parse.parse_line_no(super().ltan(*args, **kwargs))

    @wraps(_MapdlCore.spline)
    def spline(self, *args, **kwargs):
        return parse.parse_line_nos(super().spline(*args, **kwargs))

    @wraps(_MapdlCore.n)
    def n(self, *args, **kwargs):
        return parse.parse_n(super().n(*args, **kwargs))

    @wraps(_MapdlCore.ndist)
    def ndist(self, *args, **kwargs):
        return parse.parse_ndist(super().ndist(*args, **kwargs))

    @wraps(_MapdlCore.blc4)
    def blc4(self, *args, **kwargs):
        return parse.parse_output_volume_area(super().blc4(*args, **kwargs))

    @wraps(_MapdlCore.blc5)
    def blc5(self, *args, **kwargs):
        return parse.parse_output_volume_area(super().blc5(*args, **kwargs))

    @wraps(_MapdlCore.block)
    def block(self, *args, **kwargs):
        return parse.parse_output_volume_area(super().block(*args, **kwargs))

    @wraps(_MapdlCore.con4)
    def con4(self, *args, **kwargs):
        return parse.parse_output_volume_area(super().con4(*args, **kwargs))

    @wraps(_MapdlCore.cone)
    def cone(self, *args, **kwargs):
        return parse.parse_output_volume_area(super().cone(*args, **kwargs))

    @wraps(_MapdlCore.cyl4)
    def cyl4(self, *args, **kwargs):
        return parse.parse_output_volume_area(super().cyl4(*args, **kwargs))

    @wraps(_MapdlCore.cyl5)
    def cyl5(self, *args, **kwargs):
        return parse.parse_output_volume_area(super().cyl5(*args, **kwargs))

    @wraps(_MapdlCore.cylind)
    def cylind(self, *args, **kwargs):
        return parse.parse_output_volume_area(super().cylind(*args, **kwargs))

    @wraps(_MapdlCore.pcirc)
    def pcirc(self, *args, **kwargs):
        return parse.parse_output_volume_area(super().pcirc(*args, **kwargs))

    @wraps(_MapdlCore.rectng)
    def rectng(self, *args, **kwargs):
        return parse.parse_output_volume_area(super().rectng(*args, **kwargs))

    @wraps(_MapdlCore.sph4)
    def sph4(self, *args, **kwargs):
        return parse.parse_output_volume_area(super().sph4(*args, **kwargs))

    @wraps(_MapdlCore.sph5)
    def sph5(self, *args, **kwargs):
        return parse.parse_output_volume_area(super().sph5(*args, **kwargs))

    @wraps(_MapdlCore.sphere)
    def sphere(self, *args, **kwargs):
        return parse.parse_output_volume_area(super().sphere(*args, **kwargs))

    @wraps(_MapdlCore.torus)
    def torus(self, *args, **kwargs):
        return parse.parse_output_volume_area(super().torus(*args, **kwargs))

    @wraps(_MapdlCore.v)
    def v(self, *args, **kwargs):
        return parse.parse_v(super().v(*args, **kwargs))

    @wraps(_MapdlCore.va)
    def va(self, *args, **kwargs):
        return parse.parse_v(super().va(*args, **kwargs))
