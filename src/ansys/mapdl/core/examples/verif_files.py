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

"""loads a list of verification files
"""
import glob
import inspect
import os

module_path = os.path.dirname(inspect.getfile(inspect.currentframe()))


def load_vmfiles():
    """load vmfiles and store their filenames"""
    vmfiles = {}
    verif_path = os.path.join(module_path, "verif")
    for filename in glob.glob(os.path.join(verif_path, "*dat")):
        basename = os.path.basename(filename)
        vmname = os.path.splitext(basename)[0]
        vmfiles[vmname] = filename

    return vmfiles


# save the module from failing if the verification files are unavailable.
try:
    vmfiles = load_vmfiles()
except:
    vmfiles = []
