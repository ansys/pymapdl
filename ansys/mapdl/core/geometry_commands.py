"""Parse the entity numbers from various MAPDL geometry commands"""

import re

numeric_const_pattern = r"""
[-+]? # optional sign
(?:
(?: \d* \. \d+ ) # .1 .12 .123 etc 9.1 etc 98.1 etc
|
(?: \d+ \.? ) # 1. 12. 123. etc 1 12 123 etc
)
# followed by optional exponent part if desired
(?: [Ee] [+-]? \d+ ) ?
"""


NUM_PATTERN = re.compile(numeric_const_pattern, re.VERBOSE)


def parse_kpoint(msg):
    if msg:
        res = re.search(r'kpoint=\s+(\d+)\s+', msg)
        if res is not None:
            return int(res.group(1))


def parse_output_areas(msg):
    """Parse create area message and return area number"""
    if msg:
        res = re.search(r"(OUTPUT AREAS =\s*)([0-9]+)", msg)
        if res is not None:
            return int(res.group(2))


def parse_a(msg):
    """Parse create area message and return area number"""
    if msg:
        res = re.search(r"(AREA NUMBER =\s*)([0-9]+)", msg)
        if res is not None:
            return int(res.group(2))


def parse_line_no(msg):
    """Parse create area message and return area number"""
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


# Wrap MAPDL geometry commands
# class _MapdlGeometryCommands():

