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
