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
from ansys.mapdl.core._mapdl_extended.analysis import (
    _ExtendedAnalysisMixin,
)
from ansys.mapdl.core._mapdl_extended.arrays import _ExtendedArrayMixin
from ansys.mapdl.core._mapdl_extended.explicit_commands import (
    _ExtendedExplicitCommandsMixin,
)
from ansys.mapdl.core._mapdl_extended.file_commands import (
    _ExtendedFileCommandsMixin,
)
from ansys.mapdl.core._mapdl_extended.import_commands import (
    _ExtendedImportCommandsMixin,
)
from ansys.mapdl.core._mapdl_extended.parameter_commands import (
    _ExtendedParameterCommandsMixin,
)
from ansys.mapdl.core._mapdl_extended.parameter_commands import TMP_VAR  # noqa: F401
from ansys.mapdl.core._mapdl_extended.parsed_commands import (
    _ExtendedParsedCommandsMixin,
)
from ansys.mapdl.core._mapdl_extended.plotting_commands import (
    _ExtendedPlottingCommandsMixin,
)
from ansys.mapdl.core._mapdl_extended.selection_commands import (
    _ExtendedSelectionCommandsMixin,
)
from ansys.mapdl.core._mapdl_extended.values import _ExtendedValueMixin
from ansys.mapdl.core.commands import CommandListingOutput, CommandOutput  # noqa: F401
from ansys.mapdl.core.contexts.do_loop import (
    _DoLoopContext,
)
from ansys.mapdl.core.contexts.do_loop import MAX_DO_LOOP_LEVEL  # noqa: F401
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


class _MapdlCommandExtended(
    _ExtendedFileCommandsMixin,
    _ExtendedSelectionCommandsMixin,
    _ExtendedPlottingCommandsMixin,
    _ExtendedParameterCommandsMixin,
    _ExtendedExplicitCommandsMixin,
    _ExtendedImportCommandsMixin,
    _ExtendedParsedCommandsMixin,
    _MapdlCore,
):
    """Class that extended MAPDL capabilities by wrapping or overwriting commands"""

    def __init__(self, *args, **kwargs):
        """Initialize the MAPDL command extended class.

        Parameters
        ----------
        *args : list
            Positional arguments to pass to the base class.

        **kwargs : dict
            Keyword arguments to pass to the base class.
        """
        super().__init__(*args, **kwargs)
        self._graphics_backend = GraphicsBackend.PYVISTA
        # Number of currently nested ``*DO``/``*DOWHILE`` loops opened
        # through :meth:`do` or :meth:`dowhile`.
        self._do_loop_level: int = 0

    @wraps(_MapdlCore.nrm)
    def nrm(self, name="", normtype="", parr="", normalize="", **kwargs):
        """Wraps *NRM"""
        if not parr:
            parr = "__temp_par__"
        super().nrm(
            name=name, normtype=normtype, parr=parr, normalize=normalize, **kwargs
        )
        return self.parameters[parr]

    @wraps(_MapdlCore.com)
    def com(self, comment="", **kwargs):
        """Wraps /COM"""
        if self.print_com and not self.mute and not kwargs.get("mute", False):
            print("/COM,%s" % (str(comment)))

        return super().com(comment=comment, **kwargs)

    @wraps(_MapdlCore.lssolve)
    def lssolve(self, lsmin="", lsmax="", lsinc="", **kwargs):
        """Wraps LSSOLVE"""
        with self.non_interactive:
            super().lssolve(lsmin=lsmin, lsmax=lsmax, lsinc=lsinc, **kwargs)
        return self.last_response


class _MapdlExtended(
    _ExtendedArrayMixin,
    _ExtendedAnalysisMixin,
    _ExtendedValueMixin,
    _MapdlCommandExtended,
):
    def do(
        self,
        par: str,
        ival: MapdlFloat = "",
        fval: MapdlFloat = "",
        inc: MapdlFloat = "",
        **kwargs: KwargDict,
    ) -> _DoLoopContext:
        r"""Context manager for an APDL ``*DO`` loop.

        Mechanical APDL Command: `\*DO <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_DO.html>`_

        The block of commands issued inside the ``with`` block is sent to
        MAPDL once and executed repeatedly by MAPDL itself, similarly to
        how the ``*DO``/``*ENDDO`` commands work when typed directly into
        MAPDL. This is fundamentally different from a Python ``for`` loop:
        the body of the ``with`` block is only evaluated once by Python to
        build up the block of APDL commands, and MAPDL performs the actual
        looping.

        This method automatically uses the :attr:`Mapdl.non_interactive
        <ansys.mapdl.core.Mapdl.non_interactive>` context manager (unless
        it is already active) so the whole loop is sent to MAPDL as a
        single block.

        MAPDL allows a maximum of 20 levels of nested do-loops (shared
        between ``*DO`` and ``*DOWHILE``). Attempting to nest more loops
        than that raises a
        :class:`MapdlDoLoopLimitError <ansys.mapdl.core.errors.MapdlDoLoopLimitError>`.

        If an exception is raised inside the ``with`` block, the ``*ENDDO``
        is never sent and the (incomplete) commands buffered by this loop
        are discarded, without affecting commands legitimately buffered
        before entering the loop, for example by an outer ``non_interactive``
        block or an outer ``do``/``dowhile`` loop.

        Parameters
        ----------
        par : str
            The name of the scalar parameter used as the loop index. Any
            existing parameter of the same name is redefined.

        ival : str, optional
            Initial value assigned to ``par``.

        fval : str, optional
            Final value. If ``ival`` exceeds ``fval`` and ``inc`` is
            positive, the loop is not executed.

        inc : str, optional
            Increment applied to ``par`` for each successive loop. Defaults
            to 1 in MAPDL. Negative increments and non-integer numbers are
            allowed.

        Returns
        -------
        contextlib.AbstractContextManager
            Context manager that opens the ``*DO`` loop on entry and closes
            it with ``*ENDDO`` on exit.

        Examples
        --------
        Create 10 nodes along the X axis.

        >>> with mapdl.do("i", 1, 10):
        ...     mapdl.n("i", "i", 0, 0)

        """
        command = f"*DO,{par},{ival},{fval},{inc}"
        return _DoLoopContext(self, command, **kwargs)

    def dowhile(
        self,
        par: str,
        **kwargs: KwargDict,
    ) -> _DoLoopContext:
        r"""Context manager for an APDL ``*DOWHILE`` loop.

        Mechanical APDL Command: `\*DOWHILE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_DOWHILE.html>`_

        The loop repeats as long as the ``par`` parameter is truthy
        (greater than 0.0) in MAPDL. Because MAPDL, not Python, performs
        the looping, ``par`` must be a parameter that already exists (or is
        set right before entering the loop) in MAPDL, and it must be
        updated from within the ``with`` block using APDL commands so
        MAPDL can re-evaluate it on every pass.

        This method automatically uses the :attr:`Mapdl.non_interactive
        <ansys.mapdl.core.Mapdl.non_interactive>` context manager (unless
        it is already active) so the whole loop is sent to MAPDL as a
        single block.

        MAPDL allows a maximum of 20 levels of nested do-loops (shared
        between ``*DO`` and ``*DOWHILE``). Attempting to nest more loops
        than that raises a
        :class:`MapdlDoLoopLimitError <ansys.mapdl.core.errors.MapdlDoLoopLimitError>`.

        If an exception is raised inside the ``with`` block, the ``*ENDDO``
        is never sent and the (incomplete) commands buffered by this loop
        are discarded, without affecting commands legitimately buffered
        before entering the loop, for example by an outer ``non_interactive``
        block or an outer ``do``/``dowhile`` loop.

        Parameters
        ----------
        par : str
            Name of the scalar parameter checked before every pass. The
            loop terminates once ``par`` is less than or equal to 0.0.

        Returns
        -------
        contextlib.AbstractContextManager
            Context manager that opens the ``*DOWHILE`` loop on entry and
            closes it with ``*ENDDO`` on exit.

        Examples
        --------
        Loop while the ``cont`` parameter is truthy, decrementing it on
        every pass.

        >>> mapdl.parameters["cont"] = 5
        >>> with mapdl.dowhile("cont"):
        ...     mapdl.n("cont", "cont", 0, 0)
        ...     mapdl.run("cont = cont - 1")

        """
        command = f"*DOWHILE,{par}"
        return _DoLoopContext(self, command, **kwargs)

    def set_graphics_backend(self, backend: GraphicsBackend):
        """Set the graphics backend to use for plotting."""
        self._graphics_backend = backend
