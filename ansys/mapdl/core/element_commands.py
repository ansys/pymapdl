import re


def parse_e(msg):
    """Parse create element message and return element number"""
    res = re.search(r"(ELEMENT\s*)([0-9]+)", msg)
    if res is not None:
        result = int(res.group(2))
    else:
        result = None
    return result


def parse_et(msg):
    """
    Parse local element type number definition message
    and return element type number
    """
    res = re.search(r"(ELEMENT TYPE\s*)([0-9]+)", msg)
    if res is not None:
        result = int(res.group(2))
    else:
        result = None
    return result


element_commands = {'E': parse_e,
                    'ET': parse_et,
}
