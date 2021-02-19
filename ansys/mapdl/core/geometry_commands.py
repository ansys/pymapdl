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

def parse_circle(msg):
    """Parse the message from CIRCLE and return the line numbers"""
    matches = re.findall(r"LINE NO.=\s*(\d*)", msg)
    if matches:
        return [int(match) for match in matches]


def parse_k(msg):
    """Parse create keypoint message and return keypoint number"""
    if not re.search(r"KEYPOINT NUMBER", msg):
        res = re.search(r"(KEYPOINT\s*)([0-9]+)", msg)
    else:
        res = re.search(r"(KEYPOINT NUMBER =\s*)([0-9]+)", msg)

    if res:
        result = int(res.group(2))
    else:
        result = None

    return result


def parse_l(msg):
    """Parse create line message and return line number"""
    res = re.search(r"(LINE NO\.=\s*)([0-9]+)", msg)
    if res is not None:
        result = int(res.group(2))
    else:
        result = None
    return result


def parse_a(msg):
    """Parse create area message and return area number"""
    res = re.search(r"(AREA NUMBER =\s*)([0-9]+)", msg)
    if res is not None:
        result = int(res.group(2))
    else:
        result = None
    return result


def parse_output_area(msg):
    """Parse create area message and return area number"""
    res = re.search(r"(OUTPUT AREA =\s*)([0-9]+)", msg)
    if res is not None:
        return int(res.group(2))


def parse_output_areas(msg):
    """Parse create area message and return area number"""
    res = re.search(r"(OUTPUT AREAS =\s*)([0-9]+)", msg)
    if res is not None:
        return int(res.group(2))


def parse_v(msg):
    """Parse create volume message and return volume number"""
    res = re.search(r"(VOLUME NUMBER =\s*)([0-9]+)", msg)
    if res is not None:
        result = int(res.group(2))
    else:
        result = None
    return result


def parse_n(msg):
    """Parse create node message and return node number"""
    res = re.search(r"(NODE\s*)([0-9]+)", msg)
    if res is not None:
        return int(res.group(2))


def parse_al(msg):
    """Parse create area message and return area number"""
    return parse_a(msg)


def parse_bsplin(msg):
    """Parse create bsplin line message and return line number"""
    return parse_l(msg)


def parse_kpoint(msg):
    res = re.search(r'kpoint=\s+(\d+)\s+', msg)
    if res is not None:
        return int(res.group(1))


def parse_kdist(msg):
    """Return xyz distance from KDIST

    For example:
    The distance between keypoints 10 and 11 in coordinate system 0
    is:
    DIST              DX (KP2-KP1)      DY (KP2-KP1)      DZ (KP2-KP1)
    1.0000000000E+10 -1.0000000000E+10   0.000000000       0.000000000

    Will return: [-10000000000.0, 0.0, 0.0]

    """
    finds = re.findall(NUM_PATTERN, msg)[-3:]
    if len(finds) == 3:
        return [float(val) for val in finds]


def parse_kl(msg):
    """Return keypoint number from ``kl``

    MAPDL message
    GENERATE KEYPOINT ON LINE      1 AT RATIO=  0.500000

    KEYPOINT    26   X,Y,Z=   5.00000       0.00000       0.00000      IN CSYS=  0

    Return: 25

    """
    res = re.search(r'KEYPOINT\s+(\d+)\s+', msg)
    if res is not None:
        return int(res.group(1))


geometry_commands = {'K': parse_k,
                     'L': parse_l,
                     'A': parse_a,
                     'V': parse_v,
                     'N': parse_n,
                     'AL': parse_al,
                     'BLC4': parse_output_area,
                     'CYL4': parse_output_area,
                     'ASBA': parse_output_areas,
                     'BSPL': parse_bsplin,
                     'CIRC': parse_circle,
                     'KBET': parse_kpoint,
                     'KCEN': parse_kpoint,
                     'KDIS': parse_kdist,
                     'KL': parse_kl,
}
