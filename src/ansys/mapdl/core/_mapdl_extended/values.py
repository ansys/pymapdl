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

from typing import Union

import numpy as np
from numpy.typing import NDArray

from ansys.mapdl.core.mapdl_types import KwargDict, MapdlFloat

from . import _ExtendedMixinBase


class _ExtendedValueMixin(_ExtendedMixinBase):
    """Static responsibility mixin for the extended MAPDL facade."""

    def get_etable(
        self,
        item: str,
        comp: str = "",
        option: str = "",
        lab: str = "",
        **kwargs: KwargDict,
    ) -> NDArray[np.float64]:
        """Retrieve an element-table column as a NumPy array.

        This method wraps the standard ``ETABLE``-then-``*VGET`` workflow:
        it calls :func:`Mapdl.etable() <ansys.mapdl.core.Mapdl.etable>` to
        fill an element-table column with ``item``/``comp`` for the
        currently selected elements, and then calls
        :func:`Mapdl.get_array() <ansys.mapdl.core.Mapdl.get_array>` with
        ``ELEM``/``ETAB`` to retrieve that column as a NumPy array.

        Parameters
        ----------
        item : str
            Label identifying the item. See the ``Item`` argument of
            :func:`Mapdl.etable() <ansys.mapdl.core.Mapdl.etable>` for the
            available labels.
        comp : str, optional
            Component of the item, if required.
        option : str, optional
            Option for storing element table data. One of ``"MIN"``,
            ``"MAX"``, or ``"AVG"`` (default). See
            :func:`Mapdl.etable() <ansys.mapdl.core.Mapdl.etable>` for
            details.
        lab : str, optional
            Element-table label (the ``Lab`` argument of ``ETABLE``) used
            to store the retrieved item. If omitted (default), a unique
            hidden temporary label is generated, the column is erased
            (``ETABLE,Lab,ERAS``) right after the values are retrieved,
            and no trace of it is left in MAPDL. If you supply ``lab``,
            the column is kept in the element table under that name so
            you can reuse it in subsequent MAPDL operations (for example
            ``SADD`` or ``SMULT``).

        Returns
        -------
        numpy.ndarray
            Array containing the requested element-table values. The
            underlying ``*VGET`` operation iterates over sequential
            element numbers regardless of selection, so the array can
            include entries for unselected or undefined elements. Use
            :attr:`Mapdl.post_processing.element_values
            <ansys.mapdl.core.post.PostProcessing.element_values>` to
            retrieve values for only the currently selected elements.

        Notes
        -----
        This method fills (and, for a temporary label, empties) an
        element-table column as a side effect, so it should be called
        after all the commands that must run beforehand have already
        been executed, consistent with the restrictions documented in
        :func:`Mapdl.get_array() <ansys.mapdl.core.Mapdl.get_array>`.

        Examples
        --------
        Retrieve the averaged element centroid value of the X component
        stress for the current result set, using a temporary label.

        >>> mapdl.post1()
        >>> mapdl.set(1, 1)
        >>> mapdl.get_etable("S", "X")
        array([-1.12618148, -0.93902147, -0.88121128, ...,  0.        ,
                0.        ,  0.        ])

        Retrieve the maximum element thermal equivalent strain, keeping
        the resulting element-table column under the ``"EPTHEQV"`` label
        for later use.

        >>> mapdl.get_etable("EPTH", "EQV", "MAX", lab="EPTHEQV")
        array([0., 0., 0., ..., 0., 0., 0.])
        >>> mapdl.get_array("ELEM", 1, "ETAB", "EPTHEQV")
        array([0., 0., 0., ..., 0., 0., 0.])
        """
        keep_lab = bool(lab)
        if not keep_lab:
            lab = f"_ET{self._etable_lab_counter:05d}"
            self._etable_lab_counter += 1

        self.etable(lab, item, comp, option, **kwargs)

        try:
            return self.get_array("ELEM", 1, "ETAB", lab)
        finally:
            if not keep_lab:
                self.etable(lab, "ERAS", mute=True)

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
