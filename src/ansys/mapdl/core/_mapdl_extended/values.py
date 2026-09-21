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


"""The values MAPDL extended mixin."""

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
    requires_graphics,
    supress_logging,
)
from ansys.mapdl.core.plotting import GraphicsBackend  # noqa: F401

from . import _ExtendedMixinBase


class _ExtendedValueMixin(_ExtendedMixinBase):
    """Static responsibility mixin for the extended MAPDL facade."""

    def get_etable(
        self,
        item: str,
        comp: str = "",
        option: str = "",
        lab: str = "",
    ) -> NDArray[np.float64]:
        """Create an element table column and return its values.

        Parameters
        ----------
        item : str
            Label identifying the result item.
        comp : str, optional
            Component or sequence number for the result item.
        option : str, optional
            Element table storage option, such as ``"MIN"``, ``"MAX"``,
            or ``"AVG"``.
        lab : str, optional
            Label for the element table column. If omitted, a hidden temporary
            label is used and erased after the values are retrieved. If
            provided, the column remains available in MAPDL.

        Returns
        -------
        numpy.ndarray
            Values from the element table column for the selected elements.

        Notes
        -----
        This method uses :meth:`Mapdl.etable` to create the column and
        :meth:`Mapdl.get_array` to retrieve it. As with
        :meth:`Mapdl.get_array`, it cannot be used inside the
        :attr:`Mapdl.non_interactive` context.

        Examples
        --------
        Retrieve sequence-number element results:

        >>> moment_i = mapdl.get_etable("SMISC", 3, lab="MOMY_I")
        >>> moment_j = mapdl.get_etable("SMISC", 16, lab="MOMY_J")

        Retrieve a component-name result with a temporary element table
        column:

        >>> displacement_x = mapdl.get_etable("U", "X")
        """
        temporary_label = not lab
        if temporary_label:
            # Preserve the legacy public patch point after moving this method.
            from ansys.mapdl.core import mapdl_extended

            label = f"__{mapdl_extended.random_string(4)}__"
        else:
            label = lab
        self.etable(label, item, comp, option)
        try:
            values = self.get_array("ELEM", "", "ETAB", label)
        finally:
            if temporary_label:
                self.etable(label, "ERAS")
        return values

    def get_value(
        self,
        entity: str = "",
        entnum: str = "",
        item1: str = "",
        it1num: MapdlFloat = "",
        item2: str = "",
        it2num: MapdlFloat = "",
        item3: MapdlFloat = "",
        it3num: MapdlFloat = "",
        item4: MapdlFloat = "",
        it4num: MapdlFloat = "",
        **kwargs: KwargDict,
    ) -> Union[float, str]:
        """Runs the MAPDL GET command and returns a Python value.

        This method uses :func:`Mapdl.get`.

        See the full MAPDL command documentation at `*GET
        <https://www.mm.bme.hu/~gyebro/files/ans_help_v182/ans_cmd/Hlp_C_GET.html>`_

        .. note::
           This method is not available when within the
           :func:`Mapdl.non_interactive`
           context manager.

        Parameters
        ----------
        entity : str
            Entity keyword. Valid keywords are ``"NODE"``, ``"ELEM"``,
            ``"KP"``, ``"LINE"``, ``"AREA"``, ``"VOLU"``, ``"PDS"``,
            etc.

        entnum : str, int, optional
            The number or label for the entity. In some cases, a zero
            (or blank ``""``) ``entnum`` represents all entities of
            the set.

        item1 : str, optional
            The name of a particular item for the given entity.

        it1num : str, int, optional
            The number (or label) for the specified Item1 (if
            any). Some Item1 labels do not require an IT1NUM value.

        item2 : str, optional
            A second set of item labels and numbers to further qualify the item
            for which data are to be retrieved. Most items do not require this
            level of information.

        it2num : str, int, optional
            The number (or label) for the specified ``item2`` (if
            any). Some ``item2`` labels do not require an ``it2num``
            value.

        item3 : str, optional
            A third set of item labels and numbers to further qualify the item
            for which data are to be retrieved. Most items do not require this
            level of information.

        it3num : str, int, optional
            The number (or label) for the specified ``item3`` (if
            any). Some ``item3`` labels do not require an ``it3num``
            value.

        item4 : str, optional
            A fourth set of item labels and numbers to further qualify the item
            for which data are to be retrieved. Most items do not require this level of information.

        it4num : str, int, optional
            The number (or label) for the specified ``item4`` (if
            any). Some ``item4`` labels do not require an ``it4num``
            value.

        Returns
        -------
        float
            Floating point value of the parameter.

        Examples
        --------
        Retrieve the number of nodes.

        >>> value = mapdl.get_value('node', '', 'count')
        >>> value
        3003

        Retrieve the number of nodes using keywords.

        >>> value = mapdl.get_value(entity='node', item1='count')
        >>> value
        3003
        """
        return self._get(
            entity=entity,
            entnum=entnum,
            item1=item1,
            it1num=it1num,
            item2=item2,
            it2num=it2num,
            item3=item3,
            it3num=it3num,
            item4=item4,
            it4num=it4num,
            **kwargs,
        )
