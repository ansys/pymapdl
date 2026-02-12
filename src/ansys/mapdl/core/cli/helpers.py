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

"""
Helper functions shared across CLI modules.
"""


def can_access_process(proc):
    """Check if we have permission to access and interact with a process.

    Returns True if:
    1. We can access the process information (no AccessDenied)
    2. The process belongs to the current user

    Parameters
    ----------
    proc : psutil.Process
        The process to check

    Returns
    -------
    bool
        True if we can safely access the process
    """
    import getpass
    import platform

    import psutil

    try:
        # Check if we can access basic process info and if it belongs to current user
        current_user = getpass.getuser()
        process_user = proc.username()
        if platform.system() == "Windows" and "\\" in process_user:
            return current_user == process_user.split("\\")[-1]
        return process_user == current_user
    except (psutil.AccessDenied, psutil.NoSuchProcess):
        # Cannot access process or process doesn't exist
        return False
