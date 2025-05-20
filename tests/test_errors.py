# Copyright (C) 2016 - 2025 ANSYS, Inc. and/or its affiliates.
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
    MapdlException,
    MapdlInvalidRoutineError,
    MapdlRuntimeError,
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
def test_raise_output_errors(mapdl, cleared, response, expected_error):
    if expected_error:
        with pytest.raises(expected_error):
            mapdl._raise_output_errors(response)
    else:
        mapdl._raise_output_errors(response)


def get_error_classes():
    from ansys.mapdl.core import errors

    def is_exception_class(obj):
        try:
            return issubclass(obj, MapdlException)
        except TypeError:
            return False

    errors_to_tests = []
    for each in dir(errors):
        obj = getattr(errors, each)
        if not each.startswith("_") and is_exception_class(obj):
            errors_to_tests.append(obj)
    return errors_to_tests


@pytest.mark.parametrize("error_class", get_error_classes())
def test_exception_classes(error_class):
    message = "Exception message"
    with pytest.raises(error_class, match=message):
        raise error_class(message)


def test_error_handler(mapdl, cleared):
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
    "message,condition,context",
    [
        (None, None, NullContext()),
        ("My custom error", None, NullContext()),
        ("my error", None, pytest.raises(ValueError)),
        (None, None, NullContext()),
        (None, True, NullContext()),
        (None, False, pytest.raises(ValueError)),
        ("my error", False, pytest.raises(ValueError)),
        ("my error", True, pytest.raises(ValueError)),
        ("My custom error", False, pytest.raises(ValueError)),
        ("My custom error", True, NullContext()),
    ],
    # Test ids
    ids=[
        "Match any message. No condition",
        "Match message. No condition",
        "Raises an exception. No condition (raise internal exception)",
        "No message. No condition",
        "No message. True condition",
        "No message. False condition (raise internal exception)",
        "Different error message. False condition (raise internal exception)",
        "Different error message. True condition (raise internal exception)",
        "Same error message. False condition (raise internal exception)",
        "Same error message. True condition",
    ],
)
def test_protect_from(message, condition, context):
    class myclass:
        @protect_from(ValueError, message, condition)
        def raising(self):
            raise ValueError("My custom error")

    with context:
        myobj = myclass()
        myobj.raising()
