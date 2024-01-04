# Copyright (C) 2024 ANSYS, Inc. and/or its affiliates.
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


class ProcessControls:
    def wait(self, dtime="", **kwargs):
        """APDL Command: /WAIT

        Causes a delay before the reading of the next command.

        Parameters
        ----------
        dtime
            Time delay (in seconds). Maximum time delay is 59 seconds.

        Notes
        -----
        You should consider using ``time.sleep(dtime)``

        The command following the /WAIT will not be processed until the
        specified wait time increment has elapsed.  Useful when reading from a
        prepared input file to cause a pause, for example, after a display
        command so that the display can be reviewed for a period of time.
        Another "wait" feature is available via the ``*ASK`` command.

        This command is valid in any processor.
        """
        command = f"/WAIT,{dtime}"
        return self.run(command, **kwargs)
