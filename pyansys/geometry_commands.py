"""Parse the entity numbers from various MAPDL geometry commands"""

import re


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
        result = int(res.group(2))
    else:
        result = None
    return result


def parse_al(msg):
    """Parse create area message and return area number"""
    return parse_a(msg)


def parse_bsplin(msg):
    """Parse create bsplin line message and return line number"""
    return parse_l(msg)


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
}
