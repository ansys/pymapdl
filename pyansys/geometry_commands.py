import re


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


def parse_bsplin(msg):
    """Parse create bsplin line message and return line number"""
    return parse_l(msg)


def parse_a(msg):
    """Parse create area message and return area number"""
    res = re.search(r"(AREA NUMBER =\s*)([0-9]+)", msg)
    if res is not None:
        result = int(res.group(2))
    else:
        result = None

    return result


def parse_al(msg):
    """Parse create area message and return area number"""
    return parse_a(msg)


geometry_commands = {'K': parse_k,
                     'L': parse_l,
                     'BSPLIN': parse_bsplin,
                     'A': parse_a,
                     'AL': parse_al,
}
