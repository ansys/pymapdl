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
NumPy compatibility module.

This module provides compatibility shims for NumPy functions that have been
removed or deprecated in newer versions.

NumPy 2.0+ Compatibility
=========================

NumPy removed in1d in version 2.0 (replaced by numpy.isin), but some of our
dependencies may still reference it, causing AttributeError on import.

This module monkey-patches numpy to restore the in1d function as an alias to
isin, providing backward compatibility.

This can be removed once all dependencies have been updated to use isin.
"""

import numpy as np


def _apply_numpy_compatibility_patches():
    """
    Apply compatibility patches for NumPy functions.

    This function checks for missing NumPy functions and restores them
    as compatibility shims when needed.
    """
    if not hasattr(np, "in1d"):
        # Monkey-patch numpy to restore in1d as an alias to isin
        def _in1d_compat(ar1, ar2, assume_unique=False, invert=False):
            """
            Compatibility wrapper for deprecated numpy.in1d function.

            This function was removed in NumPy 2.0 in favor of numpy.isin.

            Parameters
            ----------
            ar1 : array_like
                Input array.
            ar2 : array_like
                The values against which to test each value of ar1.
            assume_unique : bool, optional
                If True, the input arrays are both assumed to be unique.
            invert : bool, optional
                If True, the values in the returned array are inverted.

            Returns
            -------
            in1d : ndarray, bool
                The values ar1[in1d] are in ar2.
            """
            return np.isin(ar1, ar2, assume_unique=assume_unique, invert=invert)

        np.in1d = _in1d_compat


# Apply compatibility patches on module import
_apply_numpy_compatibility_patches()
