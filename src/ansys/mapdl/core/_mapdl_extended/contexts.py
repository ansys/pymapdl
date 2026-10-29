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
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""APDL loop contexts used by the extended MAPDL facade."""

from ansys.mapdl.core.contexts.loops import _do, _DoLoopContext, _dowhile
from ansys.mapdl.core.mapdl_types import KwargDict, MapdlFloat

from . import _ExtendedMixinBase


class _ExtendedLoopContextMixin(_ExtendedMixinBase):
    """Create APDL loop contexts for the extended MAPDL facade."""

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
        return _do(self, par, ival, fval, inc, **kwargs)

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
        return _dowhile(self, par, **kwargs)
