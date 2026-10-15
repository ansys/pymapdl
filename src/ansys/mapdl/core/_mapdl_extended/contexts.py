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


"""The contexts MAPDL extended mixin."""

from typing import TYPE_CHECKING
import weakref

from ansys.mapdl.core.errors import MapdlDoLoopLimitError
from ansys.mapdl.core.mapdl_types import KwargDict, MapdlFloat

TMP_VAR = "__tmpvar__"

# MAPDL only allows a limited number of nested do-loops.
MAX_DO_LOOP_LEVEL = 20


from . import _ExtendedMixinBase

if TYPE_CHECKING:
    from ansys.mapdl.core.mapdl_extended import _MapdlExtended


class _ExtendedContextMixin(_ExtendedMixinBase):
    """Static responsibility mixin for the extended MAPDL facade."""

    class _DoLoop:
        """Context manager backing :meth:`Mapdl.do` and :meth:`Mapdl.dowhile`.

        It opens the loop (``*DO`` or ``*DOWHILE``) on ``__enter__`` and
        closes it (``*ENDDO``) on ``__exit__``, automatically entering
        :attr:`Mapdl.non_interactive` (unless it is already active) so the
        whole loop is sent to MAPDL as a single block. It also keeps track
        of how many loops are currently nested so the
        :data:`MAX_DO_LOOP_LEVEL` limit imposed by MAPDL can be enforced.

        On ``__enter__``, the number of commands already buffered in
        ``mapdl._stored_commands`` is recorded in ``_stored_commands_len``.
        If an exception is raised inside the ``with`` block, ``__exit__``
        truncates ``mapdl._stored_commands`` back to that length instead of
        emitting ``*ENDDO``. This discards only the (incomplete, and
        potentially invalid since it is missing its ``*ENDDO``) commands
        buffered by this loop, without erasing commands legitimately
        buffered before it, which matters when this loop is nested inside
        an outer ``non_interactive`` block or an outer ``do``/``dowhile``
        loop that did not fail and whose buffered commands must be
        preserved.
        """

        def __init__(self, parent: "_MapdlExtended", command: str, **kwargs):
            self._parent = weakref.ref(parent)
            self._command = command
            self._kwargs = kwargs
            self._non_interactive_cm = None
            self._stored_commands_len = 0

        def __enter__(self):
            mapdl = self._parent()

            if mapdl._do_loop_level >= MAX_DO_LOOP_LEVEL:
                raise MapdlDoLoopLimitError(
                    "Cannot open another APDL do-loop: MAPDL only supports "
                    f"{MAX_DO_LOOP_LEVEL} levels of nested '*DO'/'*DOWHILE' "
                    "loops. Reduce the number of nested 'mapdl.do' or "
                    "'mapdl.dowhile' context managers."
                )

            mapdl._do_loop_level += 1
            mapdl._log.debug(
                f"Entering do-loop level {mapdl._do_loop_level}: {self._command}"
            )

            if not mapdl._store_commands:
                self._non_interactive_cm = mapdl.non_interactive
                self._non_interactive_cm.__enter__()

            self._stored_commands_len = len(mapdl._stored_commands)

            mapdl.run(self._command, **self._kwargs)
            return self

        def __exit__(self, *args):
            mapdl = self._parent()
            mapdl._do_loop_level -= 1
            mapdl._log.debug(f"Exiting do-loop level {mapdl._do_loop_level + 1}")

            try:
                if args[0] is None:
                    mapdl.run("*ENDDO")
                else:
                    # An exception was raised: discard only the commands
                    # buffered by this loop (which are incomplete since
                    # they are missing their '*ENDDO'), keeping whatever
                    # was legitimately buffered before it.
                    mapdl._stored_commands = mapdl._stored_commands[
                        : self._stored_commands_len
                    ]
            finally:
                if self._non_interactive_cm is not None:
                    self._non_interactive_cm.__exit__(*args)

    def do(
        self,
        par: str,
        ival: MapdlFloat = "",
        fval: MapdlFloat = "",
        inc: MapdlFloat = "",
        **kwargs: KwargDict,
    ) -> "_MapdlExtended._DoLoop":
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
        return self._DoLoop(self, command, **kwargs)

    def dowhile(
        self,
        par: str,
        **kwargs: KwargDict,
    ) -> "_MapdlExtended._DoLoop":
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
        return self._DoLoop(self, command, **kwargs)
