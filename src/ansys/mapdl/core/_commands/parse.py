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

"""These commands are used to parse responses from MAPDL"""
import re
from typing import Optional

NUMERIC_CONST_PATTERN = r"""
[-+]? # optional sign
(?:
(?: \d* \. \d+ ) # .1 .12 .123 etc 9.1 etc 98.1 etc
|
(?: \d+ \.? ) # 1. 12. 123. etc 1 12 123 etc
)
# followed by optional exponent part if desired
(?: [Ee] [+-]? \d+ ) ?
"""


NUM_PATTERN = re.compile(NUMERIC_CONST_PATTERN, re.VERBOSE)


def parse_kdist(msg):
    """Parse the keypoint value from a keypoint message"""
    finds = re.findall(NUM_PATTERN, msg)[-4:]
    if len(finds) == 4:
        return [float(val) for val in finds]


def parse_et(msg: Optional[str]) -> Optional[int]:
    """Parse local element type number definition message
    and return element type number.
    """
    if msg:
        res = re.search(r"(ELEMENT TYPE\s*)([0-9]+)", msg)
        if res is not None:
            return int(res.group(2))


def parse_e(msg: Optional[str]) -> Optional[int]:
    """Parse create element message and return element number."""
    if msg:
        res = re.search(r"(ELEMENT\s*)([0-9]+)", msg)
        if res is not None:
            return int(res.group(2))


def parse_kpoint(msg):
    """Parse create keypoint message and return keypoint number."""
    if msg:
        res = re.search(r"kpoint=\s+(\d+)\s+", msg)
        if res is not None:
            return int(res.group(1))


def parse_output_areas(msg):
    """Parse create area message and return area number."""
    if msg:
        res = re.search(r"(OUTPUT AREAS =\s*)([0-9]+)", msg)
        if res is not None:
            return int(res.group(2))
        res = re.search(r"(OUTPUT AREA\(S\) =\s*)([0-9]+)", msg)
        if res is not None:
            return int(res.group(2))


def parse_a(msg):
    """Parse create area message and return area number."""
    if msg:
        res = re.search(r"(AREA NUMBER =\s*)([0-9]+)", msg)
        if res is not None:
            return int(res.group(2))


def parse_line_no(msg):
    """Parse create line message and return line number."""
    if msg:
        res = re.search(r"LINE NO[.]=\s+(\d+)", msg)
        if res is not None:
            return int(res.group(1))


def parse_line_nos(msg):
    if msg:
        matches = re.findall(r"LINE NO[.]=\s*(\d*)", msg)
        if matches:
            return [int(match) for match in matches]


def parse_v(msg):
    """Parse volume message and return volume number"""
    if msg:
        res = re.search(r"(VOLUME NUMBER =\s*)([0-9]+)", msg)
        if res is not None:
            return int(res.group(2))


def parse_output_volume_area(msg):
    """Parse create area message and return area or volume number"""
    if msg:
        res = re.search(r"OUTPUT (AREA|VOLUME|AREAS) =\s*([0-9]+)", msg)
        if res is not None:
            return int(res.group(2))


def parse_ndist(msg):
    """Parse the node value from a node message"""
    finds = re.findall(NUM_PATTERN, msg)[-4:]
    if len(finds) == 4:
        return [float(val) for val in finds]
