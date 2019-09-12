import re


def parse_k(msg):
    """Parse create keypoint message and return keypoint number"""
    # grab requested keypoint number
    command = msg.splitlines()[0]
    npt = command.split(',')[1].strip()

    if re.search(r"[0-9]+", npt) and not npt == "0":
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


geometry_commands = {'K': parse_k,
                     'L': parse_l,
                     'A': parse_a,
}
