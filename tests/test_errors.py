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

import pytest

from ansys.mapdl.core.errors import (
    MapdlCommandIgnoredError,
    MapdlDidNotStart,
    MapdlError,
    MapdlException,
    MapdlInfo,
    MapdlInvalidRoutineError,
    MapdlNote,
    MapdlRuntimeError,
    MapdlVersionError,
    MapdlWarning,
    protect_from,
)
from conftest import NullContext

error_shape_error_limits = """

*** ERROR ***                           CP =       0.969   TIME= 13:30:36
 Previous testing revealed that 14 of the 38745 selected elements
 violate shape error limits.  Please review error messages on the
 output or error file (or issue the CHECK command), then delete or
 unselect those elements.

 """  # the last empty line is important!

error_highly_distorted = """

*** ERROR *** CP = 2872.649 TIME= 16:29:51
 One or more elements have become highly distorted. Excessive
 distortion of elements is usually a symptom indicating the need for
 corrective action elsewhere. Try incrementing the load more slowly
 (increase the number of substeps or decrease the time step size). You
 may need to improve your mesh to obtain elements with better aspect
 ratios. Also consider the behavior of materials, contact pairs,
 and/or constraint equations. If this message appears in the first
 iteration of first substep, be sure to perform element shape checking.

"""  # the last empty line is important!

error_inside_out = """

*** ERROR ***                           CP =       0.969   TIME= 13:30:36
 Previous testing revealed that 14 of the 38745 selected elements
 is turning inside out
 output or error file (or issue the CHECK command), then delete or
 unselect those elements.

 """  # Made up example. The last empty line is important!

empty_log = """
***** END OF INPUT ENCOUNTERED *****

 PURGE ALL SOLUTION AND POST DATA
 SAVE ALL MODEL DATA

 ALL CURRENT ANSYS DATA WRITTEN TO FILE NAME= file.db
  FOR POSSIBLE RESUME FROM THIS POINT


 NUMBER OF WARNING MESSAGES ENCOUNTERED=          0
 NUMBER OF ERROR   MESSAGES ENCOUNTERED=          0

+--------- D I S T R I B U T E D   A N S Y S   S T A T I S T I C S ------------+
"""


@pytest.mark.parametrize(
    "response,expected_error",
    [
        pytest.param(
            empty_log,
            None,
            id="Normal output without errors or warns.",
        ),
        pytest.param(
            error_highly_distorted,
            None,
            id="Failed because of highly distorted elements.",
        ),
        pytest.param(
            error_shape_error_limits,
            MapdlRuntimeError,
            id="Failed because of shape error limits.",
        ),
    ],
)
def test_raise_output_errors(mapdl, response, expected_error):
    if expected_error:
        with pytest.raises(expected_error):
            mapdl._raise_output_errors(response)
    else:
        mapdl._raise_output_errors(response)


@pytest.mark.parametrize(
    "error_class",
    [
        MapdlDidNotStart,
        MapdlException,
        MapdlError,
        MapdlWarning,
        MapdlNote,
        MapdlInfo,
        MapdlVersionError,
        MapdlInvalidRoutineError,
        MapdlCommandIgnoredError,
        MapdlRuntimeError,
    ],
)
def test_exception_classes(error_class):
    message = "Exception message"
    with pytest.raises(error_class):
        raise error_class(message)


def test_error_handler(mapdl):
    text = "is not a recognized"
    with pytest.raises(MapdlInvalidRoutineError, match="recognized"):
        mapdl._raise_errors(text)

    text = "command is ignored"
    with pytest.raises(MapdlCommandIgnoredError, match="ignored"):
        mapdl._raise_errors(text)

    text = "*** ERROR ***\n This is my own errorrrr"
    with pytest.raises(MapdlRuntimeError, match="errorrrr"):
        mapdl._raise_errors(text)


@pytest.mark.parametrize(
    # Tests inputs
    "message,context",
    [
        ("", NullContext()),
        ("My custom error", NullContext()),
        pytest.param("my error", pytest.raises(ValueError)),
    ],
    # Test ids
    ids=["Match any message", "Match message", "Raises an exception"],
)
def test_protect_from(message, context):
    class myclass:
        @protect_from(ValueError, message)
        def raising(self):
            raise ValueError("My custom error")

    with context:
        myobj = myclass()
        myobj.raising()
