# Copyright (C) 2016 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
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

from typing import Any, Optional


class CommandsBase:
    """Base class for MAPDL command mixin classes.

    This class declares the interface that command mixin classes rely on.
    The actual implementation of the run method is provided by the parent
    MAPDL class when these command mixins are combined via multiple inheritance.
    """

    def run(
        self,
        command: str,
        write_to_log: bool = True,
        mute: Optional[bool] = None,
        **kwargs: Any,
    ) -> str:
        """Run a single APDL command.

        This method is implemented by the parent MAPDL class.
        Command mixins can call this method to execute APDL commands.

        Parameters
        ----------
        command : str
            ANSYS APDL command.
        write_to_log : bool, optional
            Whether to write command to log. Default ``True``.
        mute : bool, optional
            Whether to mute command output.
        **kwargs : Any
            Additional keyword arguments.

        Returns
        -------
        str
            Command output from MAPDL.
        """
        raise NotImplementedError(
            "The run method must be provided by the parent MAPDL class"
        )
